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
MCP server tests for UniIR-backed m-BEIR behavior.

These tests live in optional because importing the UniIR integration requires the
uniir_for_pyserini optional dependency. Heavy model, index, and document loading
are mocked; the test only verifies that the MCP search tool can route through the
m-BEIR/UniIR backend path.
"""

import asyncio
import json
import os
import sys
import unittest
from unittest.mock import patch

from fastmcp import Client, FastMCP
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.utilities.tests import run_server_async

from pyserini.search.faiss import DenseSearchResult

try:
    from pyserini.encode.optional._uniir import UniIRQueryEncoder  # noqa: F401
    UNIIR_IMPORT_ERROR = None
except Exception as e:
    UNIIR_IMPORT_ERROR = e


def _make_mcp_server():
    """Build the same MCP server as mcpyserini (FastMCP + tools + controller)."""
    from pyserini.server.backend import get_backend
    from pyserini.server.mcp.tools import register_tools

    mcp = FastMCP('mcpyserini')
    register_tools(mcp, get_backend())
    return mcp


@unittest.skipIf(UNIIR_IMPORT_ERROR is not None, f'uniir_for_pyserini unavailable: {UNIIR_IMPORT_ERROR}')
class TestMCPyseriniServerUniIR(unittest.TestCase):
    """Test MCP server paths that require UniIR-backed m-BEIR search."""

    def setUp(self):
        self._devnull = open(os.devnull, 'w')
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

    @staticmethod
    def _content_texts(result):
        return [part.text for part in result.content if hasattr(part, 'text')]

    def _single_json_content(self, result):
        texts = self._content_texts(result)
        self.assertGreaterEqual(len(texts), 1, 'Expected at least one text content part')
        return json.loads(texts[0])

    async def _call_tool(self, name, arguments):
        mcp = _make_mcp_server()
        async with run_server_async(mcp, transport='streamable-http') as url:
            async with Client(StreamableHttpTransport(url)) as client:
                return await client.call_tool(name, arguments)

    def test_mbeir_search_tool_routes_through_uniir(self):
        from pyserini.server.backend import SharedSearchBackend

        class FakeUniIRQueryEncoder:
            def __init__(self, encoder_dir, instruction_config=None, **kwargs):
                self.encoder_dir = encoder_dir
                self.instruction_config = instruction_config

        class FakeFaissSearcher:
            def search(self, query, hits):
                self.query = query
                self.hits = hits
                return [DenseSearchResult('doc1', 1.0)]

        with patch('pyserini.server.backend._get_uniir_query_encoder', return_value=FakeUniIRQueryEncoder), \
                patch('pyserini.server.backend.FaissSearcher.from_prebuilt_index', return_value=FakeFaissSearcher()), \
                patch.object(SharedSearchBackend, '_resolve_mbeir_instruction_config', return_value='instr.yaml'), \
                patch.object(SharedSearchBackend, '_bulk_fetch_and_format_documents', return_value={'doc1': 'doc text'}):
            result = self._run_async(self._call_tool('search', {
                'query': {'query_txt': 'a red dress'},
                'index': 'm-beir-fashioniq_task7.clip-sf-large',
                'hits': 1,
            }))

        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        payload = self._single_json_content(result)
        self.assertIsInstance(payload, list)
        self.assertIn('Query Results for: a red dress', payload)
        self.assertIn('DocID: doc1 | Score: 1.0', payload)
        self.assertIn('doc text', payload)


if __name__ == '__main__':
    unittest.main()
