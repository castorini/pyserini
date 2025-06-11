# Pyserini: Model Context Protocol (MCP) Server

The Pyserini MCP server provides search and document retrieval capabilities through the Model Context Protocol, enabling AI assistants and other MCP clients to access Pyserini's information retrieval features.

## Getting Started


### Starting the MCP Server

The MCP server uses stdio transport and is designed to be launched by MCP clients. 
If you want to run the server manually, you will need the [development](https://github.com/castorini/pyserini/blob/master/docs/installation.md#development-installation) installation of Pyserini. In your project root directory, run:

```bash
python pyserini/server/mcp/mcpyserini.py
```

### Configuration for MCP Clients

#### Claude Desktop Configuration

To use the Pyserini MCP server with Claude Desktop, go to `Claude->Settings->Developer` and click edit config.
This takes you to the Claude config file `claude_desktop_config.json`, where you can add the Pyserini MCP server configuration under the `mcpServers` section:

```json
{
  "mcpServers": {
    "mcpyserini": {
      "command": "/path/to/your/conda/env/bin/python",
      "args": [
        "python -m pyserini.server.mcp"
      ]
    }
  }
}
```

Restart Claude Desktop to apply the changes. You should be able to see `mcpyserini` as an available tool in Claude. To use mcpyserini, simply prompt Claude to use mcpyserini with a specific index and query.

For more details on configuring Claude Desktop, refer to the [Claude Desktop documentation](https://modelcontextprotocol.io/quickstart/user).

## Available Tools

The Pyserini MCP server provides two main tools for information retrieval:

### 1. Search Tool

**Tool Name:** `search`

**Description:** Perform a BM25 search on a given index and return top-k hits with document ID, score, and text snippet.

**Parameters:**
- `query` (string, required): Search query string
- `index_name` (string, required): Name of the index to search
- `k` (integer, optional): Number of results to return (default: 10)

**Returns:** List of search results, each containing:
- `docid`: Document identifier
- `score`: BM25 relevance score
- `contents`: Text snippet from the document
- `index_name`: Name of the index searched

**Example Usage in MCP Client:**

```
Search for "what is a lobster roll" in the msmarco-v1-passage index, returning 5 results.
```

### 2. Get Document Tool

**Tool Name:** `get_document`

**Description:** Retrieve the full text of a document by its document ID from a specified index.

**Parameters:**
- `docid` (string, required): Document ID to retrieve
- `index_name` (string, required): Name of the index containing the document

**Returns:** Document object containing:
- `docid`: Document identifier
- `contents`: Full document text
- `raw`: Raw document representation (if available)

**Example Usage in MCP Client:**

```
Retrieve the full text of document "7157715" from the msmarco-v1-passage index.
```
