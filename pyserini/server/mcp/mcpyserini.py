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
from fastmcp import FastMCP
from fastmcp.server.auth import require_scopes
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.server.middleware import AuthMiddleware

from pyserini.server.backend import SharedSearchBackend, get_backend
from pyserini.server.config import load_server_config
from pyserini.server.mcp.tools import register_tools


_MCP_REQUIRED_SCOPE = 'mcp:access'


def create_mcp_server(backend: SharedSearchBackend, config_path: str | None = None) -> FastMCP:
    """Build MCP server with optional token auth from YAML config."""
    _configured_indexes, token_strings = load_server_config(config_path)
    auth = None
    middleware = None

    if token_strings:
        auth = StaticTokenVerifier(
            tokens={
                token: {
                    'client_id': 'api_key',
                    'scopes': [_MCP_REQUIRED_SCOPE],
                }
                for token in token_strings
            },
            required_scopes=[_MCP_REQUIRED_SCOPE],
        )
        middleware = [AuthMiddleware(auth=require_scopes(_MCP_REQUIRED_SCOPE))]

    mcp = FastMCP('mcpyserini', auth=auth, middleware=middleware)
    register_tools(mcp, backend)
    return mcp


def main():
    """Main entry point for the server."""
    parser = argparse.ArgumentParser(description="MCPyserini Server")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "http"], 
        default="stdio",
        help="Transport mode for the MCP server (default: stdio)"
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

    args = parser.parse_args()

    backend = None
    try:
        backend = get_backend(args.config)
        mcp = create_mcp_server(backend, args.config)

        if args.transport == "http":
            mcp.run(transport=args.transport, port=args.port)
        else:
            mcp.run(transport=args.transport)

    except Exception as e:
        print('Error', e)
        raise
    finally:
        if backend is not None:
            backend.close_all()
