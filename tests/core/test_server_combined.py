#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi.testclient import TestClient

from pyserini.server.backend import get_backend
from pyserini.server.mcp.mcpyserini import create_mcp_server
from pyserini.server.rest.app import create_app


class TestCombinedServer(unittest.TestCase):
    def test_combined_rest_and_mcp_endpoints_share_process(self):
        backend = get_backend(None)
        app = create_app(shared_backend=backend)
        mcp_server = create_mcp_server(backend, None)
        mcp_app = mcp_server.http_app(path='/', transport='http')

        rest_lifespan = app.router.lifespan_context
        mcp_lifespan = mcp_app.router.lifespan_context

        @asynccontextmanager
        async def combined_lifespan(parent_app):
            async with AsyncExitStack() as stack:
                await stack.enter_async_context(rest_lifespan(parent_app))
                await stack.enter_async_context(mcp_lifespan(mcp_app))
                yield

        app.router.lifespan_context = combined_lifespan
        app.mount('/mcp', mcp_app)

        headers = {'accept': 'application/json, text/event-stream', 'content-type': 'application/json'}
        initialize = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'initialize',
            'params': {
                'protocolVersion': '2025-03-26',
                'capabilities': {},
                'clientInfo': {'name': 'test-client', 'version': '1.0'},
            },
        }
        list_tools = {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {}}

        with TestClient(app) as client:
            rest = client.get('/v1/cacm/search', params={'query': 'information retrieval', 'hits': 1})
            self.assertEqual(rest.status_code, 200, msg=rest.text)

            init_resp = client.post('/mcp/', headers=headers, json=initialize)
            self.assertEqual(init_resp.status_code, 200, msg=init_resp.text)
            session_id = init_resp.headers.get('mcp-session-id')
            self.assertTrue(session_id)

            mcp_headers = dict(headers)
            mcp_headers['mcp-session-id'] = session_id
            tools_resp = client.post('/mcp/', headers=mcp_headers, json=list_tools)
            self.assertEqual(tools_resp.status_code, 200, msg=tools_resp.text)
            self.assertIn('"tools"', tools_resp.text)


if __name__ == '__main__':
    unittest.main()
