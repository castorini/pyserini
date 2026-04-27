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
MCPyserini Server
A Model Context Protocol server that provides search functionality using Pyserini.
"""

import argparse
import logging
from fastmcp import FastMCP
from fastmcp.server.auth import require_scopes
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.middleware import AuthMiddleware

from pyserini.server.backend import SharedSearchBackend, get_backend
from pyserini.server.config import load_server_config
from pyserini.server.logging_utils import build_uvicorn_log_config, compute_token_fingerprint
from pyserini.server.mcp.tools import register_tools


_MCP_REQUIRED_SCOPE = 'mcp:access'
auth_logger = logging.getLogger('pyserini.server.mcp.auth')

class _LoggingStaticTokenVerifier(StaticTokenVerifier):
    """Static token verifier with auth-failure attribution logging."""

    async def verify_token(self, token: str):
        verified = await super().verify_token(token)
        if verified is None:
            auth_logger.info(
                'auth_failed key_id=%s status=401',
                compute_token_fingerprint(token),
            )
        return verified


class _McpAuthSuccessAuditMiddleware(Middleware):
    """Logs successful authenticated tool calls with token fingerprint attribution."""

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        response = await call_next(context)
        token = get_access_token()
        key_id = compute_token_fingerprint(token.token if token is not None else None)
        auth_logger.info(
            'auth_tool_call tool=%s key_id=%s status=ok',
            context.message.name,
            key_id,
        )
        return response


def create_mcp_server(backend: SharedSearchBackend, config_path: str | None = None) -> FastMCP:
    """Build MCP server with optional token auth from YAML config."""
    _configured_indexes, token_strings = load_server_config(config_path)
    auth = None
    middleware = None

    if token_strings:
        auth = _LoggingStaticTokenVerifier(
            tokens={
                token: {
                    'client_id': 'api_key',
                    'scopes': [_MCP_REQUIRED_SCOPE],
                }
                for token in token_strings
            },
            required_scopes=[_MCP_REQUIRED_SCOPE],
        )
        middleware = [
            AuthMiddleware(auth=require_scopes(_MCP_REQUIRED_SCOPE)),
            _McpAuthSuccessAuditMiddleware(),
        ]

    mcp = FastMCP('mcpyserini', auth=auth, middleware=middleware)
    register_tools(mcp, backend)
    return mcp


def main():
    """Main entry point for the server."""
    parser = argparse.ArgumentParser(description="MCPyserini Server")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "http"], 
        default="http",
        help="Transport mode for the MCP server (default: http)"
    )

    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port number for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="YAML server config with index mappings and API keys",
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

    args = parser.parse_args()

    if args.no_prebuilt_indexes and not args.config:
        raise SystemExit('Error: --no-prebuilt-indexes requires --config')

    backend = None
    try:
        backend = get_backend(args.config, no_prebuilt_indexes=args.no_prebuilt_indexes)
        mcp = create_mcp_server(backend, args.config)

        if args.transport == "http":
            mcp.run(
                transport=args.transport,
                port=args.port,
                uvicorn_config={
                    'access_log': not args.no_access_log,
                    'log_config': build_uvicorn_log_config(
                        args.server_log_file,
                        args.auth_log_file,
                        auth_logger_name='pyserini.server.mcp.auth',
                    ),
                },
            )
        else:
            mcp.run(transport=args.transport)

    except Exception as e:
        print('Error', e)
        raise
    finally:
        if backend is not None:
            backend.close_all()
