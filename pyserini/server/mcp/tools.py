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
Register tools for the MCP server.
"""

from typing import Any

from fastmcp import FastMCP
from pyserini.server.search_controller import SearchController
from pyserini.server.models import INDEX_TYPE

def register_tools(mcp: FastMCP, controller: SearchController):
    """Register all tools with the MCP server."""

    @mcp.tool(
        name='search',
        description='Perform a BM25 search on a given index. Returns top‑k hits with docid, score, and snippet.',
    )
    def search(
        query: str,
        index_name: str,
        k: int = 10,
        ef_search: int = 100,
        encoder: str = None,
        query_generator: str = None
    ) -> dict[str, Any]:
        """
        Search the Pyserini index with BM25 and return top-k hits
        Args:
            query: Search query string
            index_name: Name of index to search (default: use default index)
            k: Number of results to return (default: 10)
        Returns:
            List of search results with docid, score, and raw contents
        """
        return controller.search(query, index_name, k, ef_search=ef_search, encoder=encoder, query_generator=query_generator)

    @mcp.tool(
        name='get_document',
        description='Retrieve a full document by its document ID from a given index.',
    )
    def get_document(docid: str, index_name: str) -> dict[str, Any]:
        """
        Retrieve the full text of a document by its ID.

        Args:
            docid: Document ID to retrieve
            index_name: Name of index to search (default: use default index)

        Returns:
            Document with full text, or ValueError if not found
        """
        return controller.get_document(docid, index_name)
    
    @mcp.tool(
        name='list_all_indexes',
        description='List available indexes of a given type in the Pyserini server.',
    )
    def list_indexes(index_type: str) -> dict[str, Any]:
        f"""
        List indexes available for search of a given type from Pyserini.

        Args:
            index_type: Type of index out of {INDEX_TYPE.keys()}'

        Returns:
            Dictionary of index names to their metadata.
        """
        return {"tf": controller.get_indexes(index_type)}
    
    @mcp.tool(
        name='get_index_status',
        description='Check if the index is downloaded and what size it is.',
    )
    def get_index_status(index_name: str) -> dict[str, Any]:
        """
        Check if the index is downloaded and what size it is.

        Args:
            index_name: Name of the index to check

        Returns:
            Dictionary with index information.
        """
        return controller.get_status(index_name)  