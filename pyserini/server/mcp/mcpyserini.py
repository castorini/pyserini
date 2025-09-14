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
MCPyserini Server
A Model Context Protocol server that provides search functionality using Pyserini.
"""

import argparse
from fastmcp import FastMCP

from pyserini.server.mcp.tools import register_tools
from pyserini.server.search_controller import get_controller


def main():
    """Main entry point for the server."""
    parser = argparse.ArgumentParser(description="MCPyserini Server")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "streamable-http"], 
        default="stdio",
        help="Transport mode for the MCP server (default: stdio)"
    )
    
    args = parser.parse_args()
    
    try:
        mcp = FastMCP('mcpyserini')

        register_tools(mcp, get_controller())

        mcp.run(transport=args.transport)


    except Exception as e:
        print('Error', e)
        raise
