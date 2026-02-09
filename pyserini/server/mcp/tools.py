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

import base64
from typing import Any, Dict
from pathlib import Path
from fastmcp.utilities.types import Image

from fastmcp import FastMCP
from pyserini.server.search_controller import SearchController, DenseSearchResult
from pyserini.server.models import INDEX_TYPE, EVAL_METRICS

def register_tools(mcp: FastMCP, controller: SearchController):
    """Register all tools with the MCP server."""

    @mcp.tool()
    def search(
        query: Dict[str, Any],
        index_name: str,
        intruction_config: str = None,
        k: int = 10,
        ef_search: int = 100,
        encoder: str = None,
        query_generator: str = None
    ):
        """
        Search the Pyserini index with the appropriate method for the type of the index provided and return top-k hits.

        Args:
            query: Search query dictionary with format {"qid": "...", "query_txt": "...", "query_img_path": "..."} where query_txt and query_img_path are optional but at least one must be provided (query_img_path can either be a local path of an image or an url to an image)
            index_name: Name of index to search, use the list_indexes tool to see available indexes
            instruction_config: for instruction guided search for multimodal embedding models
            k: Number of results to return (default: 10)
            ef_search: ef_search parameter for HNSW indexes (default: 100)
            encoder: Encoder to use for encoding the query
            query_generator: For sparse (tf) indexes only: how to build the Lucene query. One of: BagOfWords, DisjunctionMax (dismax), QuerySideBm25 (bm25qs), Covid19. Omit or None for default.

        Returns:
            List of search results with docid, score, and raw contents in text or image form
        """

        raw_results = controller.search(
            query, index_name, k,
            ef_search=ef_search,
            encoder=encoder,
            query_generator=query_generator,
            instruction_config=intruction_config
        )

        # Turn dict to list since MCP cannot render images in dicts
        final_output = []
        query_info = raw_results.get('query', {})
        final_output.append(f"Query Results for: {query_info.get('query_txt', 'Visual Query')}")

        if query_info.get('query_img_path'):
            img_format = controller._get_extension(query_info['query_img_path'])
            with open(query_info['query_img_path'], "rb") as f:
                img_bytes = f.read()

            final_output.append(Image(data=img_bytes, format=img_format))

        for cand in raw_results.get('candidates', []):
            final_output.append(f"DocID: {cand['docid']} | Score: {cand['score']}")
        
            if cand.get('document_txt') and cand['document_txt'] != "None":
                final_output.append(cand['document_txt'])
        
            if cand.get('encoded_img'):
                img_format = controller._get_extension(cand['document_img_path'])
                img_bytes = base64.b64decode(cand['encoded_img'])
                final_output.append(Image(data=img_bytes, format=img_format))

        return final_output

    @mcp.tool()
    def get_document(docid: str, index_name: str):
        """
        Retrieve the full text and image (if available) of a document by its ID from a given index.

        Args:
            docid: Document ID to retrieve
            index_name: Name of index to search 

        Returns:
            Document with full text and image (if available)
        """
        doc_data = controller.get_document(docid, index_name)
        results = []

        results.append(doc_data.get('contents', ''))

        if doc_data.get('img_path'):
            extension = Path(doc_data['img_path']).suffix
            if extension.lower() in ['.jpeg', '.jpg']:
                img_format = "jpeg"
            else:
                img_format = extension.lower().replace(".", "") or "png"

            img_bytes = base64.b64decode(doc_data['encoded_img'])
            results.append(
                Image(
                    data=img_bytes,
                    format=img_format
                )
            )

        return results 

    @mcp.tool()
    def list_indexes(index_type: str) -> list[str]:
        f"""
        List all indexes available for search of a given type from Pyserini.

        Args:
            index_type: Type of index out of {INDEX_TYPE.keys()}'

        Returns:
            List of available index names in Pyserini of the given type.
        """
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
        return controller.get_status(index_name)  
    
    @mcp.tool()
    def fuse_search_results(
        hits1: list[DenseSearchResult], 
        hits2: list[DenseSearchResult], 
        k: int = 10
    ) -> list[DenseSearchResult]:
        """
        Performs normalization average fusion on two lists of search results to improve ranking.

        Args:
            hits1: First list of search results to merge with docid and score in the format of [{docid: score}]
            hits2: Second list of search results to merge with docid and score in the format of [{docid: score}]
            k: Number of top results to return (default: 10)
        Returns:
            List of search results with docid and score in the format of [{docid: score}]
        """
        return controller.fuse(hits1, hits2, k)
    
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

        Returns:
            Evaluation score for the given hits and evaluation arguments
        """
        if not metric in EVAL_METRICS.keys():
            raise ValueError(f"{metric} is not a valid evaluation metric! Must be one of {EVAL_METRICS.keys()}")
        return controller.eval_hits(index_name, metric, query_id, hits, cutoff)
