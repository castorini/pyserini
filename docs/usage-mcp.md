# Pyserini: Model Context Protocol (MCP) Server

The Pyserini MCP server provides search and document retrieval capabilities through the Model Context Protocol, enabling AI assistants and other MCP clients to access Pyserini's information retrieval features.

This guide features Claude Desktop and Cursor as clients for our MCP server, but there exists many other clients that could work as well. 

## Local Server

To use the Pyserini MCP server locally with Claude Desktop, go to "Claude" -> "Settings" -> "Developer" and click edit config.
This takes you to the Claude config file `claude_desktop_config.json`, where you can add the Pyserini MCP server configuration under the `mcpServers` section:

```json
{
  "mcpServers": {
    "mcpyserini": {
      "command": "/path/to/your/conda/env/bin/python",
      "args": [
        "-m", "pyserini.server.mcp"
      ]
    }
  }
}
```

Restart Claude Desktop to apply the changes.
You should be able to see `mcpyserini` as an available tool in Claude.
To use mcpyserini, simply prompt Claude to use mcpyserini with a specific index and query.

If you run into Java version issues, one possible solution is to explicitly specify `JAVA_HOME`:

```json
{
  "mcpServers": {
    "mcpyserini": {
      "command": "/path/to/your/conda/env/bin/python",
      "args": [
        "-m", "pyserini.server.mcp"
      ],
      "env": {
        "JAVA_HOME": "/path/to/your/conda/env/"
      }
    }
  }
}
```

For more details on configuring Claude Desktop, refer to the [Claude Desktop documentation](https://modelcontextprotocol.io/quickstart/user).


## Remote Server

To use the Pyserini MCP server remotely, first start the server on your remote machine:

```bash
python -m pyserini.server.mcp --transport streamable-http
```

Run the following on your local machine to forward the port from your remote machine:

```bash
ssh -L 8000:localhost:8000 username@hostname
```

To use it with Cursor, create `mcp.json` with the following and place it in your `.cursor` directory:

```json
{
  "mcpServers": {
    "mcpyserini": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

For more details on configuring Cursor with MCP, refer to the [documentation](https://docs.cursor.com/context/model-context-protocol). 

As of time of writing (July 2025), Claude Desktop does not natively support remote MCP servers with the free plan. 
However, it is probably a more conventional client than Cursor, so we include the following 'hack' for using Claude Desktop with a remote MCP server.

<details>
<summary>Claude Desktop with remote MCP server hack</summary>
<br/>

Start the MCP server on your remote machine with the same instructions as above.

Download our bridging script on your local machine with the following command:

```bash
wget https://raw.githubusercontent.com/castorini/pyserini/refs/heads/master/pyserini/server/mcp/pyserini_bridge.py -O pyserini_bridge.py
```

Modify your Claude Desktop configuration file `claude_desktop_config.json` with the following to point to the script you just downloaded: 

```json
{
  "mcpServers": {
    "mcp_pyserini": {
      "command": "/path/to/your/conda/env/bin/python",
      "args": [
        "path/to/your/pyserini_bridge.py"
      ]
    }
  }
}
```

Restart Claude Desktop and you should be good to go.
</details>
<br/>

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

You can ask your MCP client for a full, detailed list of capabilities. 

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lilyjge](https://github.com/lilyjge) on 2025-06-20 (commit [`88584b9`](https://github.com/castorini/pyserini/commit/88584b982ac9878775be1ffb0b1a8673c0cccd3b))
+ Results reproduced by [@Vik7am10](https://github.com/Vik7am10) on 2025-06-23 (commit [`f7c1077`](https://github.com/castorini/pyserini/commit/f7c10776c486744b8f28f753df29036cdfd28389))
+ Results reproduced by [@suraj-subrahmanyan](https://github.com/suraj-subrahmanyan) on 2025-07-16 (commit [`1915a15`](https://github.com/castorini/pyserini/commit/1915a154326f829b91308f275227a8bbb42eea9b))