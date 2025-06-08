from typing import Dict, List, Optional, Any


from mcp.server.fastmcp import FastMCP      
from task_manager import TaskManager, DEFAULT_INDEX


def register_tools(mcp: FastMCP, manager: TaskManager):
    """Register all tools with the MCP server."""

    @mcp.tool(
        name="search",
        description="Perform a BM25 search on a given index. Returns top‑k hits with docid, score, and snippet."
    )
    def search(query: str, index_name: str = DEFAULT_INDEX, k: int = 10,) -> List[Dict[str, Any]]:
        """
        Search the Pyserini index with BM25 and return top-k hits
        Args:
            query: Search query string
            index_name: Name of index to search (default: use default index)
            k: Number of results to return (default: 10)
        Returns:
            List of search results with docid, score, text snippet, and index name
        """
        return manager.search(query, index_name, k)

    @mcp.tool(
        name="get_document",
        description="Retrieve a full document by its document ID from a given index."
    )
    def get_document(docid: str, index_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the full text of a document by its ID.
        
        Args:
            docid: Document ID to retrieve
            index_name: Name of index to search (default: use default index)
        
        Returns:
            Document with full text, or None if not found
        """
        return manager.get_document(docid, index_name)