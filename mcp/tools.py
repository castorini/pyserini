from typing import Dict, List, Optional, Any

from mcp.server.fastmcp import FastMCP   
from mcpyserini import MCPyserini


def register_tools(mcp: FastMCP, server: MCPyserini):
    """Register all tools with the MCP server."""
    
    @mcp.tool(
        name="pyserini_search_msmarco_v1",
        description="Perform a BM25 search on the msmarco‑v1‑passage index. Returns top‑k hits with docid, score, and snippet."
    )
    def pyserini_search_msmarco_v1(query: str, k: int = 10, index_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search the Pyserini index with BM25 and return top-k hits
        Args:
            query: Search query string
            k: Number of results to return (default: 10)
            index_name: Name of index to search (default: use default index)
        Returns:
            List of search results with docid, score, text snippet, and index name
        """
        return server.search(query, k, index_name)
    
    @mcp.tool(
        name="get_document",
        description="Retrieve a full document by its document ID from a Pyserini index."
    )
    def get_document(docid: str, index_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve the full text of a document by its ID.
        
        Args:
            docid: Document ID to retrieve
            index_name: Name of index to search (default: use default index)
        
        Returns:
            Document with full text, or None if not found
        """
        return server.get_document(docid, index_name)