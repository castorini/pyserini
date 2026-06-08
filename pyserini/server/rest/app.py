#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
FastAPI server exposing the same REST surface as Anserini (``openapi.yaml``).

Usage:
    python -m pyserini.server.rest [--host HOST] [--port PORT] [--config PATH] [--no-prebuilt-indexes] 
                                   [--load-shedding-threshold MS] [--search-cache-size N] [--document-cache-size N]

Endpoints:
    GET /openapi.yaml     : OpenAPI specification (same document as Anserini).
    GET /v1/{index}/search?query=...&hits=10&parse=true&k1=0.9&b=0.4
    GET /v1/{index}/doc/{docid}?parse=true
    GET /docs             : Swagger UI (FastAPI).
"""

from __future__ import annotations

import copy
import json
import logging
import hashlib
import threading
import time
from collections import deque
from contextlib import asynccontextmanager
from functools import lru_cache
from importlib import resources

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import yaml

from pyserini.server.backend import SharedSearchBackend
from pyserini.server.config import AcceptedApiTokens, load_server_config
from pyserini.server.rest.routes import v1

logger = logging.getLogger(__name__)
auth_logger = logging.getLogger('pyserini.server.rest.auth')

SERVER_NAME = 'Pyserini API'
API_VERSION = 'v1'
DESCRIPTION = 'REST API aligned with Anserini (Lucene indexes via Pyserini).'
ROUTE_ERROR = 'Expected route /v1/{index}/search or /v1/{index}/doc/{docid}'
AUTH_TOKEN_REQUEST_EMAIL = 'get-pyserini@googlegroups.com'


# Hint for clients when we return 429 (also sent as ``Retry-After`` header).
_LOAD_SHED_RETRY_AFTER_SEC = 1

_LOAD_SHED_ERROR_BODY = (
    'Service temporarily overloaded; retry after a few seconds '
    f'(or wait at least {_LOAD_SHED_RETRY_AFTER_SEC}s). If load persists, back off with jitter.'
)


class RestBackpressure:
    """
    Simple load-shedding policy for authenticated REST API requests.
    
    Algorithm:
    - Tracks all request latencies and per-API-key request counts over a rolling 60-second window.
    - Computes p99 latency from recent samples, refreshing every 250ms.
    - When p99 exceeds the configured threshold, sheds requests from the API key(s) with the highest
      request count in the current window (minimum 2 requests required to shed).
    - Returns HTTP 429 for shed requests; caller can retry later.
    
    This approach provides lightweight overload control without complex rate-limiting state.
    """

    __slots__ = (
        '_load_shedding_threshold_ms',  # float - p99 latency threshold in ms for triggering load shedding
        '_lock',                        # Thread lock for concurrent access
        '_latencies',                   # deque[(timestamp, latency_ms)] - rolling window of request latencies
        '_key_hits',                    # deque[(timestamp, key_id)] - rolling window of API key requests
        '_key_counts',                  # dict[key_id, count] - current count per key in the window
        '_max_count',                   # int - highest request count among all keys in current window
        '_cached_p99_ms',               # float | None - cached p99 latency value
        '_cached_p99_at',               # float - timestamp when p99 was last computed
    )
    _window_sec = 60.0
    _min_latency_samples = 20
    _p99_refresh_sec = 0.25

    def __init__(self, load_shedding_threshold_ms: float) -> None:
        self._load_shedding_threshold_ms = float(load_shedding_threshold_ms)
        self._lock = threading.Lock()
        self._latencies: deque[tuple[float, float]] = deque()
        self._key_hits: deque[tuple[float, str]] = deque()
        self._key_counts: dict[str, int] = {}
        self._max_count = 0
        self._cached_p99_ms: float | None = None
        self._cached_p99_at = 0.0

    def _prune_latencies(self, now: float) -> None:
        cutoff = now - self._window_sec
        while self._latencies and self._latencies[0][0] < cutoff:
            self._latencies.popleft()

    def _prune_key_hits(self, now: float) -> None:
        cutoff = now - self._window_sec
        while self._key_hits and self._key_hits[0][0] < cutoff:
            _, k = self._key_hits.popleft()
            n = self._key_counts.get(k, 0)
            if n <= 1:
                self._key_counts.pop(k, None)
            else:
                self._key_counts[k] = n - 1
        if self._max_count and self._max_count not in self._key_counts.values():
            self._max_count = max(self._key_counts.values(), default=0)

    def _sync_counts_from_hits_if_needed(self) -> None:
        # Preserve testability when fixtures seed _key_hits directly.
        if self._key_counts or not self._key_hits:
            return
        for _, k in self._key_hits:
            self._key_counts[k] = self._key_counts.get(k, 0) + 1
        self._max_count = max(self._key_counts.values(), default=0)

    def _p99_ms(self, now: float) -> float | None:
        if (
            self._cached_p99_ms is not None
            and now - self._cached_p99_at < self._p99_refresh_sec
        ):
            return self._cached_p99_ms
        n = len(self._latencies)
        if n < self._min_latency_samples:
            self._cached_p99_ms = None
        else:
            lat_ms = sorted(ms for _, ms in self._latencies)
            self._cached_p99_ms = float(lat_ms[min(n - 1, int(0.99 * (n - 1)))])
        self._cached_p99_at = now
        return self._cached_p99_ms

    def should_shed(self, key_id: str, now: float) -> bool:
        with self._lock:
            self._sync_counts_from_hits_if_needed()
            self._key_hits.append((now, key_id))
            self._key_counts[key_id] = self._key_counts.get(key_id, 0) + 1
            self._max_count = max(self._max_count, self._key_counts[key_id])
            self._prune_key_hits(now)
            self._prune_latencies(now)
            p99 = self._p99_ms(now)
            if p99 is None:
                return False
            if p99 <= self._load_shedding_threshold_ms:
                return False
            return self._key_counts.get(key_id, 0) == self._max_count and self._max_count >= 2

    def record_latency(self, latency_ms: float, now: float) -> None:
        with self._lock:
            self._latencies.append((now, latency_ms))
            self._prune_latencies(now)


def _log_auth_attribution(event: str, client: str, request: Request, query: str, key_id: str, status: int) -> None:
    auth_logger.info(
        '%s client=%s method=%s path=%s query=%s key_id=%s status=%s',
        event,
        client,
        request.method,
        request.url.path,
        query,
        key_id,
        status,
    )


def _error_message(detail: object) -> str:
    """Coerce exception detail to a single string (``ErrorResponse.error`` is ``type: string``)."""
    if detail is None:
        return ''
    if isinstance(detail, str):
        return detail
    if isinstance(detail, (list, dict)):
        return json.dumps(detail)
    return str(detail)


def _load_openapi_text() -> str:
    return resources.files('pyserini.server.rest').joinpath('openapi.yaml').read_text(encoding='utf-8')


@lru_cache(maxsize=1)
def _load_openapi_schema() -> dict[str, object]:
    payload = yaml.safe_load(_load_openapi_text())
    if not isinstance(payload, dict):
        raise ValueError('Bundled openapi.yaml must decode to an object')
    return payload


def _extract_api_tokens(request: Request) -> list[str]:
    candidates: list[str] = []
    raw = request.headers.get('x-api-key') or request.headers.get('X-API-Key')
    if raw is not None:
        token = str(raw).strip()
        if token:
            candidates.append(token)
    auth = request.headers.get('authorization') or request.headers.get('Authorization')
    if auth and str(auth).lower().startswith('bearer '):
        token = str(auth[7:]).strip()
        if token and token not in candidates:
            candidates.append(token)
    return candidates


def _compute_token_fingerprint(token: str | None) -> str:
    """Stable, non-reversible short identifier for request attribution logs."""
    if token is None:
        return 'missing'
    t = str(token).strip()
    if not t:
        return 'missing'
    return hashlib.sha256(t.encode('utf-8')).hexdigest()[:12]


def _truncate_request_query(request: Request) -> str:
    raw = request.url.query
    if not raw:
        return '-'
    if len(raw) <= 256:
        return raw
    return f'{raw[:256]}...'


def _build_uvicorn_log_config(server_log_file: str | None, auth_log_file: str | None) -> dict[str, object]:
    from uvicorn.config import LOGGING_CONFIG

    config = copy.deepcopy(LOGGING_CONFIG)
    formatters = config.setdefault('formatters', {})
    handlers = config.setdefault('handlers', {})
    loggers = config.setdefault('loggers', {})

    formatters['auth'] = {
        'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }

    if server_log_file:
        handlers['server_default_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': server_log_file,
            'encoding': 'utf-8',
        }
        handlers['server_access_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'access',
            'filename': server_log_file,
            'encoding': 'utf-8',
        }
        if 'uvicorn.error' in loggers:
            loggers['uvicorn.error']['handlers'] = ['server_default_file']
        if 'uvicorn.access' in loggers:
            loggers['uvicorn.access']['handlers'] = ['server_access_file']

    if auth_log_file:
        handlers['auth_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'auth',
            'filename': auth_log_file,
            'encoding': 'utf-8',
        }
        auth_handlers = ['auth_file']
    else:
        handlers['auth_console'] = {
            'class': 'logging.StreamHandler',
            'formatter': 'auth',
            'stream': 'ext://sys.stderr',
        }
        auth_handlers = ['auth_console']

    loggers['pyserini.server.rest.auth'] = {
        'handlers': auth_handlers,
        'level': 'INFO',
        'propagate': False,
    }
    return config


def create_app(
    config_path: str | None = None,
    *,
    no_prebuilt_indexes: bool = False,
    load_shedding_threshold_ms: float = 3000.0,
    search_cache_size: int = 2048,
    document_cache_size: int = 4096,
) -> FastAPI:
    if no_prebuilt_indexes and not config_path:
        raise ValueError('--no-prebuilt-indexes requires a config file path')

    token_strings = None
    if config_path:
        _configured_indexes, token_strings = load_server_config(config_path)
        if no_prebuilt_indexes and not _configured_indexes:
            raise ValueError('--no-prebuilt-indexes requires at least one entry under indexes: in the config file')

    if no_prebuilt_indexes and not token_strings:
        logger.warning(
            'REST --no-prebuilt-indexes is enabled but ``api_keys`` in %s is missing or empty; '
            '/v1/ is not authenticated. Add non-empty ``api_keys`` unless this host is intentionally public.',
            config_path,
        )

    accepted_api_tokens: AcceptedApiTokens | None = None
    if token_strings:
        accepted_api_tokens = AcceptedApiTokens.from_strings(token_strings)

    rest_backpressure: RestBackpressure | None = None
    if accepted_api_tokens is not None:
        rest_backpressure = RestBackpressure(load_shedding_threshold_ms)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.search_backend = SharedSearchBackend(
            config_path,
            no_prebuilt_indexes=no_prebuilt_indexes,
            search_cache_size=search_cache_size,
            document_cache_size=document_cache_size,
        )
        yield
        app.state.search_backend.close_all()

    app = FastAPI(
        title=SERVER_NAME,
        version=API_VERSION,
        description=DESCRIPTION,
        lifespan=lifespan,
    )
    app.state.accepted_api_tokens = accepted_api_tokens  # type: ignore[attr-defined]
    app.state.rest_backpressure = rest_backpressure  # type: ignore[attr-defined]
    app.openapi = lambda: _load_openapi_schema()

    @app.middleware('http')
    async def rest_api_key_and_access_log(request: Request, call_next):
        prefix = f'/{API_VERSION}/'
        tokens: AcceptedApiTokens | None = getattr(request.app.state, 'accepted_api_tokens', None)
        if tokens is None or not request.url.path.startswith(prefix):
            return await call_next(request)

        client = request.client.host if request.client else '-'
        query = _truncate_request_query(request)
        credentials = _extract_api_tokens(request)
        matched_token = next((token for token in credentials if tokens.is_valid(token)), None)
        key_id = _compute_token_fingerprint(matched_token or (credentials[0] if credentials else None))
        if matched_token is None:
            _log_auth_attribution('auth_failed', client, request, query, key_id, 401)
            return JSONResponse(
                status_code=401,
                content={
                    'error': (
                        'Unauthorized. To request an access token, '
                        f'email {AUTH_TOKEN_REQUEST_EMAIL}.'
                    )
                },
            )

        bp: RestBackpressure | None = getattr(request.app.state, 'rest_backpressure', None)
        t0 = time.perf_counter()
        if bp is not None and bp.should_shed(key_id, t0):
            _log_auth_attribution('auth_request', client, request, query, key_id, 429)
            return JSONResponse(
                status_code=429,
                content={'error': _LOAD_SHED_ERROR_BODY},
                headers={'Retry-After': str(_LOAD_SHED_RETRY_AFTER_SEC)},
            )

        status = 500
        response = None
        try:
            response = await call_next(request)
            status = response.status_code
            if bp is not None:
                now = time.perf_counter()
                bp.record_latency((now - t0) * 1000.0, now)
            return response
        except Exception:
            logger.warning(
                'REST /v1 handler raised before response (client=%s path=%s)',
                client,
                request.url.path,
                exc_info=True,
            )
            raise
        finally:
            _log_auth_attribution('auth_request', client, request, query, key_id, status)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception('Unhandled error in REST API')
        return JSONResponse(status_code=500, content={'error': 'Internal server error'})

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            detail = exc.detail
            message = ROUTE_ERROR if detail in (None, 'Not Found') else _error_message(detail)
            return JSONResponse(status_code=404, content={'error': message})
        if exc.status_code == 405:
            return JSONResponse(status_code=405, content={'error': 'Only GET is supported'})
        return JSONResponse(status_code=exc.status_code, content={'error': _error_message(exc.detail)})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=400, content={'error': _error_message(exc.errors())})

    @app.get('/openapi.yaml', include_in_schema=False)
    async def openapi_yaml():
        return PlainTextResponse(_load_openapi_text(), media_type='application/yaml; charset=utf-8')

    @app.get('/')
    async def root():
        return {
            'name': SERVER_NAME,
            'version': API_VERSION,
            'description': DESCRIPTION,
            'openapi': '/openapi.yaml',
            'documentation': '/docs',
        }

    app.include_router(v1.router, prefix=f'/{API_VERSION}')
    return app


app = create_app()

# Backwards compatibility for tests and imports expecting ``VERSION``.
VERSION = API_VERSION


def main():
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser(description='Run the Pyserini REST API server (Anserini-compatible).')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Bind address (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8081, help='Port (default: 8081)')
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='YAML server config with index mappings and API keys',
    )
    parser.add_argument(
        '--no-prebuilt-indexes',
        action='store_true',
        help='Only allow indexes declared in --config (disable prebuilt names and arbitrary filesystem paths).',
    )
    parser.add_argument(
        '--server-log-file',
        type=str,
        default=None,
        help='Optional file path for uvicorn server logs (error/access).',
    )
    parser.add_argument(
        '--auth-log-file',
        type=str,
        default=None,
        help='Optional file path for timestamped auth attribution logs.',
    )
    parser.add_argument(
        '--no-access-log',
        action='store_true',
        help='Disable uvicorn default request access logs.',
    )
    parser.add_argument(
        '--load-shedding-threshold',
        type=float,
        default=3000.0,
        metavar='MS',
        help=(
            'When api_keys is set in --config, shed the busiest key(s) if rolling p99 latency (ms) '
            'over the last minute exceeds this value (default: 3000).'
        ),
    )
    parser.add_argument(
        '--search-cache-size',
        type=int,
        default=2048,
        help='LRU cache size for search results (default: 2048).',
    )
    parser.add_argument(
        '--document-cache-size',
        type=int,
        default=4096,
        help='LRU cache size for document fetches (default: 4096).',
    )
    args = parser.parse_args()

    if args.port <= 0 or args.port > 65535:
        raise SystemExit('Error: --port must be in [1, 65535]')

    if args.no_prebuilt_indexes:
        if not args.config:
            raise SystemExit('Error: --no-prebuilt-indexes requires --config')

    if args.load_shedding_threshold < 0:
        raise SystemExit('Error: --load-shedding-threshold must be >= 0')

    if args.search_cache_size < 0:
        raise SystemExit('Error: --search-cache-size must be >= 0')

    if args.document_cache_size < 0:
        raise SystemExit('Error: --document-cache-size must be >= 0')

    uvicorn.run(
        create_app(
            args.config,
            no_prebuilt_indexes=args.no_prebuilt_indexes,
            load_shedding_threshold_ms=args.load_shedding_threshold,
            search_cache_size=args.search_cache_size,
            document_cache_size=args.document_cache_size,
        ),
        host=args.host,
        port=args.port,
        access_log=not args.no_access_log,
        log_config=_build_uvicorn_log_config(args.server_log_file, args.auth_log_file),
    )


__all__ = ['RestBackpressure', 'app', 'create_app', 'main', 'VERSION', 'API_VERSION']
