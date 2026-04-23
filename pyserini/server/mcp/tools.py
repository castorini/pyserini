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

import logging
from typing import Any, Dict

from fastmcp import FastMCP
from pyserini.search.faiss import DenseSearchResult
from pyserini.server.backend import SharedSearchBackend
from pyserini.server.utils import EVAL_METRICS, INDEX_TYPE
from pyserini.server.mcp.extension import McpSearchExtension

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP, controller: SharedSearchBackend):
    """Register all tools with the MCP server."""
    extension = McpSearchExtension(controller)

    @mcp.tool()
    def search(
        query: str | Dict[str, Any],
        index: str = "msmarco-v2.1-doc-segmented",
        hits: int = 10,
        parse: bool = True,
        ef_search: int = 100,
        encoder: str = "",
        query_generator: str = ""
    ):
        """
        Search the Pyserini index with the appropriate method for the type of the index provided and return top-k hits.
        Image results are returned as FastMCP.Image in the list. It is up to the client, not the LLM, to render them properly, so the LLM should not worry about displaying the images.
        If the LLM can see the images, assume that they are displayed to the user as well. 

        Args:
            query: Search query dictionary with format {"qid": "...", "query_txt": "...", "query_img_path": "..."} 
                where query_txt and query_img_path are optional but at least one must be provided 
                (query_img_path can either be a local path of an image or an url to an image).
                "qid" is also optional but must be a specific format for image search, no need to supply unless given by user.
            index: Name of index to search, use the list_indexes tool to see available indexes. 
                Default is msmarco-v2.1-doc-segmented which is good for retrieval augmented generation for LLMs.
            hits: Number of results to return (default: 10)
            parse: Same semantics as REST: when true, parse JSON-backed Lucene raw fields; when false, return raw stored strings.
            ef_search: ef_search parameter for HNSW indexes (default: 100)
            encoder: Encoder to use for encoding the query
            query_generator: For sparse (tf) indexes only: how to build the Lucene query. One of: BagOfWords, DisjunctionMax (dismax), QuerySideBm25 (bm25qs), Covid19. Omit or None for default.

        Returns:
            List of search results with docid, score, and raw contents in text or image form
        """
        logger.debug('Searching %s for query: %s (parse=%s)', index, query, parse)
        return extension.search_and_render(
            query=query,
            index_name=index,
            hits=hits,
            parse=parse,
            ef_search=ef_search,
            encoder=encoder if encoder else None,
            query_generator=query_generator if query_generator else None,
        )

    @mcp.tool()
    def get_document(docid: str, index: str, parse: bool = True):
        """
        Retrieve the full text and image (if available) of a document by its ID from a given index.

        Args:
            docid: Document ID to retrieve
            index: Name of index to search
            parse: Same semantics as REST: when true, parse JSON-backed Lucene raw fields; when false, return raw stored strings.

        Returns:
            Document with full text and image (if available)
        """
        logger.debug('Retrieving document %s from index %s (parse=%s)', docid, index, parse)
        return extension.document_and_render(docid, index, parse=parse)

    @mcp.tool(
        description=f"""
        List all indexes available for search of a given type from Pyserini.

        Args:
            index_type: Type of index out of {INDEX_TYPE.keys()}

        Returns:
            List of available index names in Pyserini of the given type.
        """
    )
    def list_indexes(index_type: str) -> list[str]:
        logger.debug('Listing indexes of type %s', index_type)
        return controller.get_indexes(index_type)
    
    @mcp.tool()
    def get_index(index_name: str) -> dict[str, Any]:
        """
        Gets the metadata and download status of a given index.

        Args:
            index_name: Name of the index to check, must be a valid index name in Pyserini. Use the list_indexes tool to see available indexes

        Returns:
            Dictionary with index information.
        """
        logger.debug('Getting index information for %s', index_name)
        return controller.get_status(index_name)  
    
    @mcp.tool()
    def fuse_search_results(
        results1: list[DenseSearchResult], 
        results2: list[DenseSearchResult], 
        hits: int = 10
    ) -> list[DenseSearchResult]:
        """
        Performs normalization average fusion on two lists of search results to improve ranking.

        Args:
            results1: First list of search results to merge with docid and score in the format of [{docid: score}]
            results2: Second list of search results to merge with docid and score in the format of [{docid: score}]
            hits: Number of top results to return (default: 10)
        Returns:
            List of search results with docid and score in the format of [{docid: score}]
        """
        logger.debug(
            'Fusing search results with %s hits in results1 and %s hits in results2',
            len(results1),
            len(results2),
        )
        return extension.fuse_search_results(results1, results2, hits)
    
    @mcp.tool()
    def get_qrels(
        index_name: str,
        query_id: str
    ) -> dict[str, str]:
        """
        Returns relevant judgements for a given index and query id.

        Args:
            index_name: Name of the index to get relevant judgements for, must be a valid index name in Pyserini. Use the list_indexes tool to see available indexes
            query_id: Query ID to to get relevant judgements for, must be a valid query id for the index

        Returns:
            Dictionary with docid and relevance judgement in the format of {docid: relevance}
        """
        logger.debug('Getting qrels for index %s and query id %s', index_name, query_id)
        return extension.get_qrels(index_name, query_id)
    
    @mcp.tool(
        name="eval_hits",
        description=f"""
        Evaluates search results with given metric and cutoff.

        Args:
            index_name: Name of the index the search results are from
            metric: Evaluation metric out of {EVAL_METRICS.keys()}
            query_id: Query ID to evaluate search results for
            hits: Search results to evaluate in the format of {{docid: score}}
            cutoff: Number of top results to evaluate (default: 10)

        Returns:
            Evaluation score for the given hits and evaluation arguments
        """
    )
    def eval_hits(
        index_name: str,
        metric: str,
        query_id: str,
        hits: dict[str, float],
        cutoff: int = 10
    ) -> float:
        logger.debug(
            'Evaluating hits for index %s, query id %s, metric %s, and cutoff %s',
            index_name,
            query_id,
            metric,
            cutoff,
        )
        return extension.eval_hits(index_name, metric, query_id, hits, cutoff)
