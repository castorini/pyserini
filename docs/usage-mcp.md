# Pyserini: Model Context Protocol (MCP) Server

The Pyserini MCP server exposes search, document retrieval, and evaluation helpers through the [Model Context Protocol](https://modelcontextprotocol.io/), so AI assistants and other MCP clients can use Pyserini’s indexes (sparse, dense, impact, FAISS, etc.).

The server uses the same `SharedSearchBackend` (`pyserini/server/backend.py`) as the REST API: index names, prebuilt indexes, and optional **`--config`** YAML aliases behave the same way.

This guide uses Claude Desktop and Cursor as examples; other MCP clients work too.

## Local Server

To use the Pyserini MCP server locally with Claude Desktop, go to **Claude → Settings → Developer** and edit the config. That opens `claude_desktop_config.json`. Add Pyserini under `mcpServers`:

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

Default transport is **stdio** (no HTTP port). Optional arguments:

| Argument | Description |
|----------|-------------|
| `--transport` | `stdio` (default) or `http` for remote/streamable access |
| `--port PORT` | HTTP port when using `--transport http` (default: 8000) |
| `--config PATH` | YAML server config with index mappings |

Example with a Java path and index aliases:

```json
{
  "mcpServers": {
    "mcpyserini": {
      "command": "/path/to/your/conda/env/bin/python",
      "args": [
        "-m", "pyserini.server.mcp",
      ],
      "env": {
        "JAVA_HOME": "/path/to/your/java/home"
      }
    }
  }
}
```

Restart Claude Desktop after changes. You should see **`mcpyserini`** among the available MCP servers. Prompt the model to use it with a concrete index name and query.

If you hit Java version issues, set **`JAVA_HOME`** explicitly (see above).

More detail: [Claude Desktop MCP quickstart](https://modelcontextprotocol.io/quickstart/user).

## Remote Server

On the machine that runs Pyserini, start HTTP transport (pick a port if needed):

```bash
python -m pyserini.server.mcp --transport http --port 8000
```

From your laptop, forward the port:

```bash
ssh -L 8000:localhost:8000 username@hostname
```

For **Cursor**, add something like this to your MCP config (e.g. under `.cursor`):

```json
{
  "mcpServers": {
    "mcpyserini": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Adjust host/port if you use a different bind address or forwarded port.

See [Cursor MCP documentation](https://docs.cursor.com/context/model-context-protocol).

Claude Desktop’s support for remote MCP servers varies by plan and version; if you need a desktop-only workflow against a remote server, you can use a small local bridge (see below).

<details>
<summary>Claude Desktop with a remote MCP server (bridge script)</summary>
<br/>

Start the server on the remote host as above.

On your local machine, download the bridge script:

```bash
wget https://raw.githubusercontent.com/castorini/pyserini/refs/heads/master/pyserini/server/mcp/pyserini_bridge.py -O pyserini_bridge.py
```

Point Claude at the script:

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

Restart Claude Desktop.
</details>
<br/>

## Available Tools

Tools are registered in `pyserini/server/mcp/tools.py`. The MCP client can list them with full schemas (`tools/list`). Summary:

### `search`

Runs retrieval against a Pyserini index (BM25 for standard sparse indexes; dense / impact / FAISS as appropriate for the index type). Results are returned as a **rich list** (human-readable lines plus optional **`Image`** parts for multimodal indexes), not as a single JSON table.

**Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `query` | `str \| dict[str, Any]` | yes | — | Text query, or multimodal payload such as `{"query_txt": "...", "query_img_path": "..."}` (path or URL where supported). |
| `index` | `str` | no | `msmarco-v2.1-doc-segmented` | Prebuilt index name or alias. Use `list_indexes` to discover names by type. |
| `hits` | `int` | no | `10` | Number of results to return. |
| `parse` | `bool` | no | `true` | Same semantics as REST: when `true`, parse JSON stored `raw` fields; when `false`, return raw stored strings. |
| `ef_search` | `int` | no | `100` | HNSW / dense Lucene HNSW search parameter. |
| `encoder` | `str` | no | `""` | Encoder id when the index requires one (dense / FAISS / etc.). |
| `query_generator` | `str` | no | `""` | Sparse (TF) indexes only: `BagOfWords`, `DisjunctionMax` / `dismax`, `QuerySideBm25` / `bm25qs`, `Covid19`. Omit for downstream default (`BagOfWords`). |

**Returns:** `list[Any]` rich content parts, intentionally returned as a list so MCP clients can render mixed text + images correctly.
Typical layout is:
- query header string: `"Query Results for: ..."` (and optional query `Image` part)
- per hit: descriptor string `"DocID: <docid> | Score: <score>"`, followed by optional document content part, followed by optional document `Image` part

**Example prompt:** *Search “what is a lobster roll” on `msmarco-v1-passage` with 5 hits.*

### `get_document`

Fetch one stored document by id. Returns rich content (text and optional **`Image`** when the document includes an image field).

**Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `docid` | `str` | yes | — | Document id to retrieve. |
| `index` | `str` | yes | — | Index name or alias to read from. |
| `parse` | `bool` | no | `true` | Same semantics as `search`: parse JSON-backed `raw` fields when `true`; return raw strings when `false`. |

**Returns:** `list[Any]` containing document content and optional `Image` parts.

**Example prompt:** *Get document `7157707` from `msmarco-v1-passage`.*

### `list_indexes`

Returns the list of known prebuilt index names for an index family.

**Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `index_type` | `str` | yes | — | One of `tf`, `lucene_flat`, `lucene_hnsw`, `impact`, `faiss`. |

**Returns:** `list[str]` of known prebuilt index names for that family.

### `get_index`

Returns metadata and download status for that prebuilt index.

**Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `index_name` | `str` | yes | — | Prebuilt index name to inspect. |

**Returns:** `dict[str, Any]` index metadata and download status.

### `fuse_search_results`

Fuses two ranked lists of hits.

**Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `results1` | `list[dict[str, float]]` | yes | — | First ranked list to fuse, in the form `[{docid: score}, ...]`. |
| `results2` | `list[dict[str, float]]` | yes | — | Second ranked list to fuse, in the form `[{docid: score}, ...]`. |
| `hits` | `int` | no | `10` | Number of fused results to return. |

**Returns:** `list[dict[str, float]]` fused ranked results, in the form `[{docid: score}, ...]`.

### `get_qrels`

Looks up relevance judgments for a **Pyserini qrels collection id** (e.g. `msmarco-v1-passage-dev`), not necessarily the Lucene index name used for search. Numeric topic ids can be passed as strings (e.g. `"1048585"`).

**Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `index_name` | `str` | yes | — | Pyserini qrels collection id. |
| `query_id` | `str` | yes | — | Query/topic id. |

**Returns:** `dict[str, str]` mapping `docid -> relevance`.

### `eval_hits` (tool name: `eval_hits`)

Evaluates a run using **`trec_eval`** (Java on the classpath).

**Parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `index_name` | `str` | yes | — | Collection id with qrels. |
| `metric` | `str` | yes | — | One of `ndcg`, `recall`, `map`, `recip_rank`. |
| `query_id` | `str` | yes | — | Query/topic id to evaluate. |
| `hits` | `dict[str, float]` | yes | — | Run entries as `docid -> score`. |
| `cutoff` | `int` | no | `10` | Cutoff for metric computation. |

**Returns:** `float` evaluation score.

---

Ask your LLM client for the live tool list and parameter schemas!

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lilyjge](https://github.com/lilyjge) on 2025-06-20 (commit [`88584b9`](https://github.com/castorini/pyserini/commit/88584b982ac9878775be1ffb0b1a8673c0cccd3b))
+ Results reproduced by [@Vik7am10](https://github.com/Vik7am10) on 2025-06-23 (commit [`f7c1077`](https://github.com/castorini/pyserini/commit/f7c10776c486744b8f28f753df29036cdfd28389))
+ Results reproduced by [@suraj-subrahmanyan](https://github.com/suraj-subrahmanyan) on 2025-07-16 (commit [`1915a15`](https://github.com/castorini/pyserini/commit/1915a154326f829b91308f275227a8bbb42eea9b))
+ Results reproduced by [@jjgreen0](https://github.com/JJGreen0) on 2025-07-26 (commit [`44889de`](https://github.com/castorini/pyserini/commit/44889de3d151b2e1317934b405b3ad6badd81308))
+ Results reproduced by [@FarmersWrap](https://github.com/FarmersWrap) on 2025-09-18 (commit [`4189efe`](https://github.com/castorini/pyserini/commit/4189efe9b1f936eda9d4142a039d146d9341deb6))
