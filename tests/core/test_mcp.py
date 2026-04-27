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
import json
import os
import sys
import tempfile
import unittest

from fastmcp import FastMCP, Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.exceptions import ToolError
from fastmcp.utilities.tests import run_server_async
import yaml

from pyserini.search.faiss import DenseSearchResult

_MCP_INDEX = 'cacm'
_MCP_QUERY = 'information retrieval'
_MCP_TOP_DOCID = 'CACM-3134'


def _make_mcp_server(config_path: str | None = None, *, no_prebuilt_indexes: bool = False):
    """Build the same MCP server as mcpyserini (FastMCP + tools + controller)."""
    from pyserini.server.backend import get_backend
    from pyserini.server.mcp.mcpyserini import create_mcp_server
    return create_mcp_server(
        get_backend(config_path, no_prebuilt_indexes=no_prebuilt_indexes),
        config_path,
    )


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

    @staticmethod
    def _content_texts(result):
        return [part.text for part in result.content if hasattr(part, 'text')]

    def _single_json_content(self, result):
        texts = self._content_texts(result)
        self.assertGreaterEqual(len(texts), 1, 'Expected at least one text content part')
        return json.loads(texts[0])

    async def _call_tool(
        self,
        name,
        arguments,
        *,
        headers=None,
        config_path: str | None = None,
        no_prebuilt_indexes: bool = False,
    ):
        # Create server inside this event loop so server._started is bound to it
        mcp = _make_mcp_server(
            config_path=config_path,
            no_prebuilt_indexes=no_prebuilt_indexes,
        )
        async with run_server_async(
            mcp,
            transport='streamable-http',
        ) as url:
            async with Client(StreamableHttpTransport(url, headers=headers)) as client:
                return await client.call_tool(name, arguments)

    def test_search_tool(self):
        result = self._run_async(self._call_tool('search', {
            'query': {'query_txt': _MCP_QUERY},
            'index': _MCP_INDEX,
            'hits': 3,
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        payload = self._single_json_content(result)
        self.assertIsInstance(payload, list)
        self.assertTrue(any(isinstance(t, str) and t.startswith('Query Results for:') for t in payload))
        doc_lines = [t for t in payload if isinstance(t, str) and t.startswith('DocID: ')]
        self.assertEqual(len(doc_lines), 3)

    def test_get_index_tool(self):
        result = self._run_async(self._call_tool('get_index', {
            'index_name': _MCP_INDEX,
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        payload = self._single_json_content(result)
        self.assertIsInstance(payload, dict)
        self.assertIn('downloaded', payload)

    def test_list_indexes_tool(self):
        result = self._run_async(self._call_tool('list_indexes', {
            'index_type': 'tf',
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        payload = self._single_json_content(result)
        self.assertIsInstance(payload, list)
        self.assertIn(_MCP_INDEX, payload)

    def test_list_indexes_invalid_type_raises_tool_error(self):
        async def call_invalid():
            mcp = _make_mcp_server()
            async with run_server_async(mcp, transport='streamable-http') as url:
                async with Client(StreamableHttpTransport(url)) as client:
                    await client.call_tool('list_indexes', {'index_type': 'not_a_valid_index_type'})

        with self.assertRaises(ToolError) as ctx:
            self._run_async(call_invalid())
        self.assertIn('Index type must be one of', str(ctx.exception))

    def test_get_document_tool(self):
        result = self._run_async(self._call_tool('get_document', {
            'docid': _MCP_TOP_DOCID,
            'index': _MCP_INDEX,
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        payload = self._single_json_content(result)
        self.assertIsInstance(payload, list)
        self.assertGreaterEqual(len(payload), 1)
        self.assertIsInstance(payload[0], str)
        self.assertGreater(len(payload[0]), 0)

    def test_get_document_not_found_raises_tool_error(self):
        async def call_missing():
            mcp = _make_mcp_server()
            async with run_server_async(mcp, transport='streamable-http') as url:
                async with Client(StreamableHttpTransport(url)) as client:
                    await client.call_tool('get_document', {
                        'docid': 'this-docid-does-not-exist',
                        'index': _MCP_INDEX,
                    })

        with self.assertRaises(ToolError) as ctx:
            self._run_async(call_missing())
        self.assertIn('not found', str(ctx.exception).lower())

    def test_fuse_search_results_tool(self):
        results1 = [
            DenseSearchResult('doc_a', 0.9),
            DenseSearchResult('doc_b', 0.5),
        ]
        results2 = [
            DenseSearchResult('doc_a', 0.4),
            DenseSearchResult('doc_c', 0.8),
        ]
        result = self._run_async(self._call_tool('fuse_search_results', {
            'results1': results1,
            'results2': results2,
            'hits': 2,
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        payload = self._single_json_content(result)
        self.assertIsInstance(payload, list)
        self.assertEqual(len(payload), 2)
        self.assertTrue(all(isinstance(x, dict) for x in payload))
        self.assertTrue(all('docid' in x and 'score' in x for x in payload))

    def test_get_qrels_tool(self):
        # Collection id for qrels (not the Lucene index name). Tool schema requires query_id as str.
        result = self._run_async(self._call_tool('get_qrels', {
            'index_name': 'msmarco-v1-passage-dev',
            'query_id': '1048585',
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        payload = self._single_json_content(result)
        self.assertIsInstance(payload, dict)
        self.assertGreater(len(payload), 0)

    def test_get_qrels_unknown_query_id_returns_empty(self):
        result = self._run_async(self._call_tool('get_qrels', {
            'index_name': 'msmarco-v1-passage-dev',
            'query_id': 'definitely-not-a-real-qid',
        }))
        self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
        payload = self._single_json_content(result)
        self.assertEqual(payload, {})

    def test_get_qrels_invalid_collection_raises_tool_error(self):
        async def call_invalid():
            mcp = _make_mcp_server()
            async with run_server_async(mcp, transport='streamable-http') as url:
                async with Client(StreamableHttpTransport(url)) as client:
                    await client.call_tool('get_qrels', {
                        'index_name': 'not-a-real-qrels-collection',
                        'query_id': '1048585',
                    })

        with self.assertRaises(ToolError) as ctx:
            self._run_async(call_invalid())
        self.assertIn('no qrels file', str(ctx.exception))

    def test_auth_enabled_rejects_requests_without_token(self):
        cfg = {'api_keys': ['mcp-auth-test-token']}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            with self.assertRaises(Exception) as ctx:
                self._run_async(
                    self._call_tool(
                        'list_indexes',
                        {'index_type': 'tf'},
                        config_path=path,
                    )
                )
            self.assertTrue(
                '401' in str(ctx.exception) or 'auth' in str(ctx.exception).lower(),
                msg=str(ctx.exception),
            )
        finally:
            os.unlink(path)

    def test_auth_enabled_accepts_valid_bearer_token(self):
        token = 'mcp-auth-test-token-ok'
        cfg = {'api_keys': [token]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            result = self._run_async(
                self._call_tool(
                    'list_indexes',
                    {'index_type': 'tf'},
                    headers={'Authorization': f'Bearer {token}'},
                    config_path=path,
                )
            )
            self.assertFalse(result.is_error, msg=getattr(result, 'content', result))
            payload = self._single_json_content(result)
            self.assertIsInstance(payload, list)
            self.assertIn(_MCP_INDEX, payload)
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_rejects_unconfigured_prebuilt_index(self):
        cfg = {'indexes': {'local': '/tmp'}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            with self.assertRaises(ToolError) as ctx:
                self._run_async(
                    self._call_tool(
                        'search',
                        {
                            'query': {'query_txt': _MCP_QUERY},
                            'index': _MCP_INDEX,
                            'hits': 1,
                        },
                        config_path=path,
                        no_prebuilt_indexes=True,
                    )
                )
            self.assertIn('not configured', str(ctx.exception))
        finally:
            os.unlink(path)

if __name__ == '__main__':
    unittest.main()
