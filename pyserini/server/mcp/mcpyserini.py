"""
MCPyserini Server
A Model Context Protocol server that provides search functionality using Pyserini.
"""

from mcp.server.fastmcp import FastMCP
import sys
from pathlib import Path

# Ensure the parent directory is in sys.path for module resolution
#sys.path.append(str(Path(__file__).resolve().parent.parent))

from .tools import register_tools
from ..task_manager import get_manager


def main():
    """Main entry point for the server."""
    try:
        mcp = FastMCP("pyserini-search-server")

        register_tools(mcp, get_manager())

        mcp.run(transport="stdio")

    except Exception as e:
        print("Error", e)
        raise
