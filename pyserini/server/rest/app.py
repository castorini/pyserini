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
    python -m pyserini.server.rest [--host HOST] [--port PORT] [--config PATH] [--deploy]

Endpoints:
    GET /openapi.yaml     : OpenAPI specification (same document as Anserini).
    GET /v1/{index}/search?query=...&hits=10&parse=true
    GET /v1/{index}/doc/{docid}?parse=true
    GET /docs             : Swagger UI (FastAPI).
"""

from __future__ import annotations

import json
import logging
from contextlib import asynccontextmanager
from importlib import resources

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from pyserini.server.backend import SharedSearchBackend
from pyserini.server.config import AcceptedApiTokens, load_server_config
from pyserini.server.rest.routes import v1

logger = logging.getLogger(__name__)

SERVER_NAME = 'Pyserini API'
API_VERSION = 'v1'
DESCRIPTION = 'REST API aligned with Anserini (Lucene indexes via Pyserini).'
ROUTE_ERROR = 'Expected route /v1/{index}/search or /v1/{index}/doc/{docid}'
_AUTH_LOG_IDENTITY = 'authorized'


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


def _extract_api_token(request: Request) -> str | None:
    raw = request.headers.get('x-api-key') or request.headers.get('X-API-Key')
    if raw is not None and str(raw).strip():
        return str(raw).strip()
    auth = request.headers.get('authorization') or request.headers.get('Authorization')
    if auth and str(auth).lower().startswith('bearer '):
        return str(auth[7:]).strip()
    return None


def create_app(
    config_path: str | None = None,
    *,
    deploy: bool = False,
) -> FastAPI:
    accepted_api_tokens: AcceptedApiTokens | None = None
    if deploy:
        if not config_path:
            raise ValueError('Deploy mode requires a config file path')
        aliases, token_strings = load_server_config(config_path)
        if not aliases:
            raise ValueError('Deploy mode requires at least one entry under indexes: in the config file')
        if not token_strings:
            raise ValueError('Deploy mode requires a non-empty api_keys: list in the config file')
        accepted_api_tokens = AcceptedApiTokens.from_strings(token_strings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.search_backend = SharedSearchBackend(config_path, deploy=deploy)
        yield
        app.state.search_backend.close_all()

    app = FastAPI(
        title=SERVER_NAME,
        version=API_VERSION,
        description=DESCRIPTION,
        lifespan=lifespan,
    )
    app.state.accepted_api_tokens = accepted_api_tokens  # type: ignore[attr-defined]

    @app.middleware('http')
    async def rest_api_key_and_access_log(request: Request, call_next):
        prefix = f'/{API_VERSION}/'
        tokens: AcceptedApiTokens | None = getattr(request.app.state, 'accepted_api_tokens', None)
        # Non-deploy: ``accepted_api_tokens`` is unset (None) — middleware still runs but skips auth.
        if tokens is None or not request.url.path.startswith(prefix):
            return await call_next(request)

        credential = _extract_api_token(request)
        if not tokens.is_valid(credential):
            client = request.client.host if request.client else '-'
            logger.info(
                'rest_request client=%s method=%s path=%s identity=%s status=401',
                client,
                request.method,
                request.url.path,
                'unauthorized',
            )
            return JSONResponse(status_code=401, content={'error': 'Unauthorized'})

        request.state.api_identity = _AUTH_LOG_IDENTITY  # type: ignore[attr-defined]
        response = await call_next(request)
        client = request.client.host if request.client else '-'
        logger.info(
            'rest_request client=%s method=%s path=%s identity=%s status=%s',
            client,
            request.method,
            request.url.path,
            _AUTH_LOG_IDENTITY,
            response.status_code,
        )
        return response

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
        help='YAML server config: indexes: alias -> path; with --deploy, api_keys: list of secrets (required)',
    )
    parser.add_argument(
        '--deploy',
        action='store_true',
        help='Production mode: only configured indexes, requires api_keys: in --config, and enforces API auth on /v1/.',
    )
    args = parser.parse_args()

    if args.port <= 0 or args.port > 65535:
        raise SystemExit('Error: --port must be in [1, 65535]')

    if args.deploy:
        if not args.config:
            raise SystemExit('Error: --deploy requires --config')
        aliases, token_strings = load_server_config(args.config)
        if not aliases:
            raise SystemExit('Error: --deploy requires at least one entry under indexes: in the config file')
        if not token_strings:
            raise SystemExit('Error: --deploy requires a non-empty api_keys: list in the config file')

    uvicorn.run(
        create_app(
            args.config,
            deploy=args.deploy,
        ),
        host=args.host,
        port=args.port,
    )


__all__ = ['app', 'create_app', 'main', 'VERSION', 'API_VERSION']
