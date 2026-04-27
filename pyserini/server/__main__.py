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

from __future__ import annotations

import argparse
from contextlib import AsyncExitStack, asynccontextmanager

import uvicorn

from pyserini.server.backend import get_backend
from pyserini.server.logging_utils import build_uvicorn_log_config
from pyserini.server.mcp.mcpyserini import create_mcp_server
from pyserini.server.rest.app import create_app


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Run combined Pyserini REST API and MCP servers on a shared backend.'
    )
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
        '--mcp-path',
        type=str,
        default='/mcp',
        help='HTTP path to mount MCP endpoint (default: /mcp).',
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

    if args.port <= 0 or args.port > 65535:
        raise SystemExit('Error: --port must be in [1, 65535]')
    if args.no_prebuilt_indexes and not args.config:
        raise SystemExit('Error: --no-prebuilt-indexes requires --config')
    if not args.mcp_path.startswith('/'):
        raise SystemExit('Error: --mcp-path must start with "/"')
    if args.mcp_path == '/':
        raise SystemExit('Error: --mcp-path cannot be "/"')

    backend = get_backend(args.config, no_prebuilt_indexes=args.no_prebuilt_indexes)
    app = create_app(
        args.config,
        no_prebuilt_indexes=args.no_prebuilt_indexes,
        shared_backend=backend,
    )

    mcp_server = create_mcp_server(backend, args.config)
    mcp_app = mcp_server.http_app(path='/', transport='http')

    # Ensure both REST and MCP lifespan handlers run when serving the combined app.
    rest_lifespan = app.router.lifespan_context
    mcp_lifespan = mcp_app.router.lifespan_context

    @asynccontextmanager
    async def combined_lifespan(parent_app):
        async with AsyncExitStack() as stack:
            await stack.enter_async_context(rest_lifespan(parent_app))
            await stack.enter_async_context(mcp_lifespan(parent_app))
            yield

    app.router.lifespan_context = combined_lifespan
    app.mount(args.mcp_path, mcp_app)

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        access_log=not args.no_access_log,
        log_config=build_uvicorn_log_config(
            args.server_log_file,
            args.auth_log_file,
            auth_logger_name=['pyserini.server.rest.auth', 'pyserini.server.mcp.auth'],
        ),
    )


if __name__ == '__main__':
    main()
