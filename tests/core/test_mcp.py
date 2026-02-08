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

"""
MCP server tests using FastMCP HTTP transport and Client API.

Runs the MCP server in-process over HTTP (streamable-http) via run_server_async,
then uses the FastMCP Client to call tools. No subprocess or stdio.
All server output (uvicorn, FastMCP, CancelledError, etc.) is suppressed during tests.
"""

import asyncio
import os
import sys
import unittest

from fastmcp import FastMCP, Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.utilities.tests import run_server_async


def _make_mcp_server():
    """Build the same MCP server as mcpyserini (FastMCP + tools + controller)."""
    from pyserini.server.mcp.tools import register_tools
    from pyserini.server.search_controller import get_controller
    mcp = FastMCP('mcpyserini')
    register_tools(mcp, get_controller())
    return mcp


class TestMCPyseriniServer(unittest.TestCase):
    """Test MCP server via HTTP transport using FastMCP Client."""

    # Suppress server output during tests, comment out for debugging
    def setUp(self):
        self._devnull = open(os.devnull, "w")
        self._saved_stdout = sys.stdout
        self._saved_stderr = sys.stderr
        sys.stdout = self._devnull
        sys.stderr = self._devnull

    def tearDown(self):
        sys.stdout = self._saved_stdout
        sys.stderr = self._saved_stderr
        self._devnull.close()

    def _run_async(self, coro):
        return asyncio.run(coro)

    async def _call_tool(self, name, arguments):
        # Create server inside this event loop so server._started is bound to it
        mcp = _make_mcp_server()
        async with run_server_async(
            mcp,
            transport='streamable-http',
        ) as url:
            async with Client(StreamableHttpTransport(url)) as client:
                return await client.call_tool(name, arguments)

    def test_search_tool(self):
        result = self._run_async(self._call_tool('search', {
            'query': {'query_txt': 'what is a lobster roll'},
            'index_name': 'msmarco-v1-passage',
            'k': 3,
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        self.assertIsNotNone(result.content)

    def test_get_index_tool(self):
        result = self._run_async(self._call_tool('get_index', {
            'index_name': 'msmarco-v1-passage',
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        self.assertIsNotNone(result.content)

    def test_list_indexes_tool(self):
        result = self._run_async(self._call_tool('list_indexes', {
            'index_type': 'tf',
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        self.assertIsNotNone(result.content)

if __name__ == '__main__':
    unittest.main()
