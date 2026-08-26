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
                                   [--log-file PATH] [--keep-uvicorn-logs] [--load-shedding-threshold MS]
                                   [--search-cache-size N] [--document-cache-size N]
                                   [--enable-token-issuance --token-pool PATH --token-email-smtp-host HOST
                                    --token-email-from ADDRESS]

Endpoints:
    GET /openapi.yaml     : OpenAPI specification (same document as Anserini).
    POST /v1/token        : Request delivery of a pre-generated credential by email.
    GET /v1/{index}/search?query=...&hits=10&parse=true&k1=0.9&b=0.4
    GET /v1/{index}/doc/{docid}?parse=true
    GET /docs             : Swagger UI (FastAPI).
"""

from __future__ import annotations

import asyncio
import copy
import json
import logging
import hashlib
import math
import threading
import time
import uuid
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from functools import lru_cache
from importlib import resources

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator
from starlette.exceptions import HTTPException as StarletteHTTPException
import yaml

from pyserini.server.backend import SharedSearchBackend
from pyserini.server.config import (
    AcceptedApiTokens,
    ApiTokenEmailAlreadyIssuedError,
    ApiTokenPoolExhaustedError,
    ApiTokenStore,
    PreGeneratedApiTokenPool,
    load_server_config,
)
from pyserini.server.rest.routes import v1
from pyserini.server.token_delivery import SmtpTokenEmailSender, TokenEmailSender

logger = logging.getLogger(__name__)
request_logger = logging.getLogger('pyserini.server.rest.request')

SERVER_NAME = 'Pyserini API'
API_VERSION = 'v1'
DESCRIPTION = 'REST API aligned with Anserini (Lucene indexes via Pyserini).'
ROUTE_ERROR = 'Expected route /v1/{index}/search or /v1/{index}/doc/{docid}'
MAX_LOGGED_QUERY_CHARS = 1000
MAX_LOGGED_QID_CHARS = 256
MAX_LOGGED_QUESTION_CHARS = 8192
MAX_LOGGED_RETRIEVAL_QUERY_CHARS = 4096
MAX_LOGGED_RUN_ID_CHARS = 256
MAX_LOGGED_AGENT_CHARS = 256
REQUEST_ID_HEADER = 'X-Request-ID'
TOKEN_ISSUE_PATH = f'/{API_VERSION}/token'


# Hint for clients when we return 429 (also sent as ``Retry-After`` header).
_LOAD_SHED_RETRY_AFTER_SEC = 1

_LOAD_SHED_ERROR_BODY = (
    'Service temporarily overloaded; retry after a few seconds '
    f'(or wait at least {_LOAD_SHED_RETRY_AFTER_SEC}s). If load persists, back off with jitter.'
)


class TokenIssuanceRequest(BaseModel):
    """Required identity fields for anonymous token issuance."""

    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=254)

    @field_validator('email')
    @classmethod
    def normalize_email(cls, value: str) -> str:
        normalized = value.casefold()
        if normalized.count('@') != 1 or any(char.isspace() for char in normalized):
            raise ValueError('email must be a valid address')
        local, domain = normalized.split('@', 1)
        if not local or not domain or domain.startswith('.') or domain.endswith('.') or '..' in domain:
            raise ValueError('email must be a valid address')
        return normalized


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


class TokenIssuanceCooldown:
    """Independent client-IP and email cooldowns for token issuance."""

    __slots__ = ('_interval_sec', '_lock', '_last_issued_by_client', '_last_issued_by_email')

    def __init__(self, interval_sec: float) -> None:
        self._interval_sec = float(interval_sec)
        self._lock = threading.Lock()
        self._last_issued_by_client: dict[str, float] = {}
        self._last_issued_by_email: dict[str, float] = {}

    @staticmethod
    def _prune_expired(entries: dict[str, float], cutoff: float) -> None:
        while entries:
            oldest = next(iter(entries))
            if entries[oldest] >= cutoff:
                break
            entries.pop(oldest)

    def reserve(self, client: str, email: str, now: float) -> tuple[float | None, float | None]:
        """Reserve an issuance slot, returning ``(retry_after, reservation)``."""
        if self._interval_sec <= 0:
            return None, None
        client_key = client or '<unknown>'
        with self._lock:
            cutoff = now - self._interval_sec
            self._prune_expired(self._last_issued_by_client, cutoff)
            self._prune_expired(self._last_issued_by_email, cutoff)
            client_last = self._last_issued_by_client.get(client_key)
            email_last = self._last_issued_by_email.get(email)
            retry_after = 0.0
            if client_last is not None:
                retry_after = max(retry_after, self._interval_sec - (now - client_last))
            if email_last is not None:
                retry_after = max(retry_after, self._interval_sec - (now - email_last))
            if retry_after > 0:
                return retry_after, None
            self._last_issued_by_client[client_key] = now
            self._last_issued_by_email[email] = now
            return None, now

    def release(self, client: str, email: str, reservation: float | None) -> None:
        if reservation is None:
            return
        client_key = client or '<unknown>'
        with self._lock:
            if self._last_issued_by_client.get(client_key) == reservation:
                self._last_issued_by_client.pop(client_key, None)
            if self._last_issued_by_email.get(email) == reservation:
                self._last_issued_by_email.pop(email, None)


def _now_iso8601() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def _log_request_jsonl(entry: dict[str, object]) -> None:
    request_logger.info(json.dumps(entry, sort_keys=True, separators=(',', ':')))


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


def _request_id() -> str:
    return uuid.uuid4().hex


def _request_query_for_log(request: Request) -> tuple[str, bool]:
    query = request.url.query
    if len(query) <= MAX_LOGGED_QUERY_CHARS:
        return query, False
    return query[:MAX_LOGGED_QUERY_CHARS], True


def _query_param_for_log(request: Request, name: str, max_chars: int) -> tuple[str | None, bool]:
    value = request.query_params.get(name)
    if value is None:
        return None, False
    if len(value) <= max_chars:
        return value, False
    return value[:max_chars], True


def _request_trace_for_log(request: Request) -> dict[str, object]:
    qid, qid_truncated = _query_param_for_log(request, 'qid', MAX_LOGGED_QID_CHARS)
    question, question_truncated = _query_param_for_log(
        request,
        'question',
        MAX_LOGGED_QUESTION_CHARS,
    )
    retrieval_query, retrieval_query_truncated = _query_param_for_log(
        request,
        'query',
        MAX_LOGGED_RETRIEVAL_QUERY_CHARS,
    )
    run_id, run_id_truncated = _query_param_for_log(request, 'run_id', MAX_LOGGED_RUN_ID_CHARS)
    agent, agent_truncated = _query_param_for_log(request, 'agent', MAX_LOGGED_AGENT_CHARS)
    step_raw = request.query_params.get('step')
    try:
        step: int | str | None = int(step_raw) if step_raw is not None else None
    except ValueError:
        step = step_raw
    return {
        'qid': qid,
        'qid_truncated': qid_truncated,
        'question': question,
        'question_truncated': question_truncated,
        'retrieval_query': retrieval_query,
        'retrieval_query_truncated': retrieval_query_truncated,
        'run_id': run_id,
        'run_id_truncated': run_id_truncated,
        'agent': agent,
        'agent_truncated': agent_truncated,
        'step': step,
    }


def _build_uvicorn_log_config(
    request_log_file: str | None,
    *,
    keep_uvicorn_logs: bool = False,
) -> dict[str, object]:
    from uvicorn.config import LOGGING_CONFIG

    config = copy.deepcopy(LOGGING_CONFIG)
    formatters = config.setdefault('formatters', {})
    handlers = config.setdefault('handlers', {})
    loggers = config.setdefault('loggers', {})

    formatters['jsonl'] = {
        'format': '%(message)s',
    }

    if request_log_file:
        handlers['request_jsonl_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'jsonl',
            'filename': request_log_file,
            'encoding': 'utf-8',
        }
        request_handlers = ['request_jsonl_file']
    else:
        handlers['request_jsonl_console'] = {
            'class': 'logging.StreamHandler',
            'formatter': 'jsonl',
            'stream': 'ext://sys.stderr',
        }
        request_handlers = ['request_jsonl_console']

    loggers['pyserini.server.rest.request'] = {
        'handlers': request_handlers,
        'level': 'INFO',
        'propagate': False,
    }
    if keep_uvicorn_logs and request_log_file and 'uvicorn.access' in loggers:
        handlers['uvicorn_access_request_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'access',
            'filename': request_log_file,
            'encoding': 'utf-8',
        }
        loggers['uvicorn.access']['handlers'] = ['uvicorn_access_request_file']
    return config


def create_app(
    config_path: str | None = None,
    *,
    no_prebuilt_indexes: bool = False,
    load_shedding_threshold_ms: float = 3000.0,
    search_cache_size: int = 2048,
    document_cache_size: int = 4096,
    enable_token_issuance: bool = False,
    token_issuance_cooldown_sec: float = 3600.0,
    token_pool_path: str | None = None,
    token_email_sender: TokenEmailSender | None = None,
) -> FastAPI:
    if no_prebuilt_indexes and not config_path:
        raise ValueError('--no-prebuilt-indexes requires a config file path')

    token_strings = None
    if config_path:
        _configured_indexes, token_strings = load_server_config(config_path)
        if no_prebuilt_indexes and not _configured_indexes:
            raise ValueError('--no-prebuilt-indexes requires at least one entry under indexes: in the config file')

    if no_prebuilt_indexes and not token_strings and not enable_token_issuance:
        logger.warning(
            'REST --no-prebuilt-indexes is enabled but ``api_keys`` in %s is missing or empty; '
            '/v1/ is not authenticated. Add non-empty ``api_keys`` unless this host is intentionally public.',
            config_path,
        )

    if enable_token_issuance and not config_path:
        raise ValueError('--enable-token-issuance requires a config file path')
    if enable_token_issuance and not token_pool_path:
        raise ValueError('--enable-token-issuance requires a pre-generated token pool')
    if enable_token_issuance and token_email_sender is None:
        raise ValueError('--enable-token-issuance requires an email sender')
    if token_issuance_cooldown_sec < 0:
        raise ValueError('token_issuance_cooldown_sec must be >= 0')

    accepted_api_tokens: AcceptedApiTokens | None = None
    if token_strings or enable_token_issuance:
        accepted_api_tokens = AcceptedApiTokens.from_strings(token_strings or [])

    token_store = ApiTokenStore(config_path) if enable_token_issuance and config_path else None
    token_pool = PreGeneratedApiTokenPool(token_pool_path) if enable_token_issuance and token_pool_path else None
    token_issuance_cooldown = (
        TokenIssuanceCooldown(token_issuance_cooldown_sec) if enable_token_issuance else None
    )

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
    app.state.token_store = token_store  # type: ignore[attr-defined]
    app.state.token_pool = token_pool  # type: ignore[attr-defined]
    app.state.token_email_sender = token_email_sender  # type: ignore[attr-defined]
    app.state.token_issuance_cooldown = token_issuance_cooldown  # type: ignore[attr-defined]
    app.openapi = lambda: _load_openapi_schema()

    @app.middleware('http')
    async def rest_api_key_and_access_log(request: Request, call_next):
        t0 = time.perf_counter()
        client = request.client.host if request.client else ''
        request_id = _request_id()
        query, query_truncated = _request_query_for_log(request)
        log_entry: dict[str, object] = {
            'ts': _now_iso8601(),
            'event': 'request',
            'request_id': request_id,
            'client': client,
            'method': request.method,
            'path': request.url.path,
            'query': query,
            'query_truncated': query_truncated,
            'status': 500,
            'latency_ms': 0.0,
            'auth': 'not_configured',
            'key_id': None,
        }
        log_entry.update(_request_trace_for_log(request))
        prefix = f'/{API_VERSION}/'
        tokens: AcceptedApiTokens | None = getattr(request.app.state, 'accepted_api_tokens', None)
        response = None
        try:
            if request.url.path == TOKEN_ISSUE_PATH:
                log_entry['auth'] = 'token_issuance'
                response = await call_next(request)
            elif tokens is not None and request.url.path.startswith(prefix):
                credentials = _extract_api_tokens(request)
                matched_token = next((token for token in credentials if tokens.is_valid(token)), None)
                key_id = _compute_token_fingerprint(matched_token or (credentials[0] if credentials else None))
                log_entry['key_id'] = key_id
                if matched_token is None:
                    log_entry['auth'] = 'invalid' if credentials else 'missing'
                    response = JSONResponse(
                        status_code=401,
                        content={
                            'error': 'Unauthorized. Request access from the service operator.'
                        },
                        headers={REQUEST_ID_HEADER: request_id},
                    )
                else:
                    log_entry['auth'] = 'authenticated'
                    bp: RestBackpressure | None = getattr(request.app.state, 'rest_backpressure', None)
                    if bp is not None and bp.should_shed(key_id, t0):
                        log_entry['auth'] = 'load_shed'
                        response = JSONResponse(
                            status_code=429,
                            content={'error': _LOAD_SHED_ERROR_BODY},
                            headers={
                                'Retry-After': str(_LOAD_SHED_RETRY_AFTER_SEC),
                                REQUEST_ID_HEADER: request_id,
                            },
                        )
                    else:
                        response = await call_next(request)
                        if bp is not None:
                            now = time.perf_counter()
                            bp.record_latency((now - t0) * 1000.0, now)
            else:
                response = await call_next(request)
            log_entry['status'] = response.status_code
            response.headers[REQUEST_ID_HEADER] = request_id
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
            log_entry['latency_ms'] = round((time.perf_counter() - t0) * 1000.0, 3)
            _log_request_jsonl(log_entry)

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
            if request.url.path == TOKEN_ISSUE_PATH:
                return JSONResponse(status_code=405, content={'error': 'Only POST is supported'})
            return JSONResponse(status_code=405, content={'error': 'Only GET is supported'})
        return JSONResponse(status_code=exc.status_code, content={'error': _error_message(exc.detail)})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = [
            {key: value for key, value in error.items() if key not in ('ctx', 'input')}
            for error in exc.errors()
        ]
        return JSONResponse(status_code=400, content={'error': _error_message(errors)})

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

    @app.post(TOKEN_ISSUE_PATH, status_code=202)
    async def issue_api_token(token_request: TokenIssuanceRequest, request: Request):
        store: ApiTokenStore | None = getattr(request.app.state, 'token_store', None)
        pool: PreGeneratedApiTokenPool | None = getattr(request.app.state, 'token_pool', None)
        email_sender: TokenEmailSender | None = getattr(request.app.state, 'token_email_sender', None)
        cooldown: TokenIssuanceCooldown | None = getattr(request.app.state, 'token_issuance_cooldown', None)
        tokens: AcceptedApiTokens | None = getattr(request.app.state, 'accepted_api_tokens', None)
        if store is None or pool is None or email_sender is None or cooldown is None or tokens is None:
            return JSONResponse(status_code=503, content={'error': 'API token issuance is not enabled'})

        client = request.client.host if request.client else ''
        retry_after, reservation = cooldown.reserve(client, token_request.email, time.monotonic())
        if retry_after is not None:
            retry_after_sec = max(1, math.ceil(retry_after))
            return JSONResponse(
                status_code=429,
                content={'error': 'API token issuance is temporarily rate limited for this client IP or email'},
                headers={'Retry-After': str(retry_after_sec)},
            )

        try:
            token = await asyncio.to_thread(store.token_for_email, token_request.email)
            if token is None:
                token = await asyncio.to_thread(
                    pool.claim,
                    name=token_request.name,
                    email=token_request.email,
                )
                try:
                    token = await asyncio.to_thread(
                        store.activate,
                        token,
                        name=token_request.name,
                        email=token_request.email,
                    )
                except ApiTokenEmailAlreadyIssuedError:
                    token = await asyncio.to_thread(store.token_for_email, token_request.email)
                    if token is None:
                        raise
            tokens.add(token)
            await asyncio.to_thread(
                email_sender.send,
                name=token_request.name,
                email=token_request.email,
                token=token,
            )
        except ApiTokenPoolExhaustedError:
            cooldown.release(client, token_request.email, reservation)
            return JSONResponse(
                status_code=503,
                content={'error': 'Token delivery is temporarily unavailable'},
            )
        except Exception:
            cooldown.release(client, token_request.email, reservation)
            logger.error('Token email delivery failed')
            return JSONResponse(
                status_code=503,
                content={'error': 'Token delivery is temporarily unavailable'},
            )
        return JSONResponse(
            status_code=202,
            content={'status': 'accepted', 'message': 'Token delivery will be sent by email.'},
            headers={'Cache-Control': 'no-store', 'Pragma': 'no-cache'},
        )

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
        '--log-file',
        type=str,
        default=None,
        help='Optional file path for unified JSONL request logs (one request per line).',
    )
    parser.add_argument(
        '--keep-uvicorn-logs',
        action='store_true',
        help='Keep uvicorn text access logs. If --log-file is set, these are appended to the JSONL request log.',
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
    parser.add_argument(
        '--enable-token-issuance',
        action='store_true',
        help='Claim pre-generated tokens and deliver them by email through POST /v1/token.',
    )
    parser.add_argument(
        '--token-issuance-cooldown',
        type=float,
        default=3600.0,
        metavar='SECONDS',
        help='Minimum seconds between token issuances per client (default: 3600; 0 disables).',
    )
    parser.add_argument(
        '--token-pool',
        type=str,
        default=None,
        help='Protected JSON inventory of pre-generated API tokens.',
    )
    parser.add_argument('--token-email-smtp-host', type=str, default=None)
    parser.add_argument(
        '--token-email-smtp-port',
        type=int,
        default=SmtpTokenEmailSender.DEFAULT_STARTTLS_PORT,
    )
    parser.add_argument(
        '--token-email-smtp-security',
        choices=sorted(SmtpTokenEmailSender.VALID_SECURITY_MODES),
        default='starttls',
    )
    parser.add_argument('--token-email-smtp-username', type=str, default=None)
    parser.add_argument('--token-email-smtp-password-file', type=str, default=None)
    parser.add_argument('--token-email-from', type=str, default=None)
    parser.add_argument(
        '--token-email-cc',
        action='append',
        default=None,
        help='Individual CC mailbox for token delivery (required and repeatable; mailing lists are unsafe).',
    )
    parser.add_argument(
        '--token-email-timeout',
        type=float,
        default=SmtpTokenEmailSender.DEFAULT_TIMEOUT_SEC,
        metavar='SECONDS',
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

    if args.enable_token_issuance and not args.config:
        raise SystemExit('Error: --enable-token-issuance requires --config')

    if args.enable_token_issuance and not args.token_pool:
        raise SystemExit('Error: --enable-token-issuance requires --token-pool')

    if args.enable_token_issuance and not args.token_email_smtp_host:
        raise SystemExit('Error: --enable-token-issuance requires --token-email-smtp-host')

    if args.enable_token_issuance and not args.token_email_from:
        raise SystemExit('Error: --enable-token-issuance requires --token-email-from')

    if args.enable_token_issuance and not args.token_email_cc:
        raise SystemExit('Error: --enable-token-issuance requires at least one --token-email-cc')

    if args.token_issuance_cooldown < 0:
        raise SystemExit('Error: --token-issuance-cooldown must be >= 0')

    token_email_sender = None
    if args.enable_token_issuance:
        try:
            token_email_sender = SmtpTokenEmailSender(
                host=args.token_email_smtp_host,
                port=args.token_email_smtp_port,
                sender=args.token_email_from,
                cc=tuple(args.token_email_cc),
                username=args.token_email_smtp_username,
                password_file=args.token_email_smtp_password_file,
                security=args.token_email_smtp_security,
                timeout_sec=args.token_email_timeout,
            )
        except ValueError as exc:
            raise SystemExit(f'Error: {exc}') from exc

    uvicorn.run(
        create_app(
            args.config,
            no_prebuilt_indexes=args.no_prebuilt_indexes,
            load_shedding_threshold_ms=args.load_shedding_threshold,
            search_cache_size=args.search_cache_size,
            document_cache_size=args.document_cache_size,
            enable_token_issuance=args.enable_token_issuance,
            token_issuance_cooldown_sec=args.token_issuance_cooldown,
            token_pool_path=args.token_pool,
            token_email_sender=token_email_sender,
        ),
        host=args.host,
        port=args.port,
        access_log=args.keep_uvicorn_logs,
        log_config=_build_uvicorn_log_config(
            args.log_file,
            keep_uvicorn_logs=args.keep_uvicorn_logs,
        ),
    )


__all__ = [
    'RestBackpressure',
    'TokenIssuanceCooldown',
    'app',
    'create_app',
    'main',
    'VERSION',
    'API_VERSION',
]
