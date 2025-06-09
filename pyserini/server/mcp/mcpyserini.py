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
