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
from pyserini.server.search_controller import SearchController, DenseSearchResult
from pyserini.server.models import INDEX_TYPE, EVAL_METRICS

def register_tools(mcp: FastMCP, controller: SearchController):
    """Register all tools with the MCP server."""

    @mcp.tool(
        name='search',
        description='Perform search on a given index. Returns top‑k hits with docid, score, and snippet.',
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
    
    @mcp.tool(
        name="fuse_search_results",
        description="Performs normalization fusion on search results to improve ranking."
    )
    def fuse_search_results(
        hits1: list[DenseSearchResult], 
        hits2: list[DenseSearchResult], 
        k: int = 10
    ) -> list[DenseSearchResult]:
        """
        Performs normalization fusion on search results to improve ranking.

        Args:
            hits1: First list of search results to merge with docid and score
            hits2: Second list of search results to merge with docid and score
            k: Number of results to return (default: 10)

        Returns:
            Dictionary with index information.
        """
        return controller.fuse(hits1, hits2, k)
    
    @mcp.tool(
        name="get_qrels",
        description="Returns relevant judgements for a given index and query."
    )
    def get_qrels(
        index_name: str,
        query_id: str
    ) -> dict[str, str]:
        """
        Returns relevant judgements for a given index and query.

        Args:
            index_name: Name of the index to get relevant judgements for
            query_id: Query ID to to get relevant judgements for
        """
        return controller.get_query_qrels(index_name, query_id)
    
    @mcp.tool(
        name="eval_hits",
        description="Evaluates search results with given metric and cutoff."
    )
    def eval_hits(
        index_name: str,
        metric: str,
        query_id: str,
        hits: dict[str, float],
        cutoff: int = 10
    ) -> float:
        f"""
        Evaluates search results with given metric and cutoff.

        Args:
            index_name: Name of the index the search results are from
            metric: Evaluation metric out of {EVAL_METRICS.keys()}
            query_id: Query ID to evaluate search results for
            hits: Search results to evaluate in the format of {{docid: score}}
            cutoff: Number of top results to evaluate (default: 10)
        """
        if not metric in EVAL_METRICS.keys():
            raise ValueError(f"{metric} is not a valid evaluation metric! Must be one of {EVAL_METRICS.keys()}")
        return controller.eval_hits(index_name, metric, query_id, hits, cutoff)