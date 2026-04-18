# Pyserini: REST API server (FastAPI)

The Pyserini REST server exposes an **HTTP interface aligned with [Anserini’s REST API](https://github.com/castorini/anserini)**. It serves **GET-only** routes backed by **Lucene** (`LuceneSearcher` / Java `SimpleSearcher`): prebuilt sparse index names, filesystem paths to Lucene indexes, or optional **YAML aliases**.

For multimodal / dense / FAISS workflows and tooling, use the **MCP server** and `SearchController` APIs elsewhere in Pyserini; they are not the same as this REST surface.

## Starting the server

```bash
python -m pyserini.server.rest
```

Defaults:

- **Host:** `0.0.0.0`
- **Port:** `8081` (base URL [`http://localhost:8081/`](http://localhost:8081/))

```bash
python -m pyserini.server.rest --host 127.0.0.1 --port 8080
```

### Index aliases (optional)

Same idea as Anserini’s `--index-config`: a YAML file mapping short names to absolute or config-relative paths:

```yaml
indexes:
  my_alias: /path/to/lucene/index
```

```bash
python -m pyserini.server.rest --index-config /path/to/indexes.yaml
```

## Discovery and documentation

| URL | Purpose |
|-----|---------|
| [`/`](http://localhost:8081/) | Short JSON metadata (name, version, links) |
| [`/openapi.yaml`](http://localhost:8081/openapi.yaml) | OpenAPI 3.0 specification (bundled with the package) |
| [`/docs`](http://localhost:8081/docs) | Swagger UI (FastAPI; may differ slightly from `/openapi.yaml`) |

## API overview (`/v1`)

All search and document routes use the **`GET`** method only. Errors return JSON `{"error": "<message>"}` with a 4xx/5xx status where applicable.

### Index parameter `{index}`

The `{index}` path parameter may contain **slashes**, so a relative filesystem path can appear directly under `/v1/` (for example `GET /v1/project/indexes/msmarco/search`).

For an **absolute** filesystem path (leading `/`), use an **extra slash** after `/v1/` so the first URL segment is empty and the index value keeps its leading slash—for example `GET /v1//data/indexes/msmarco/search` for index `/data/indexes/msmarco`.

That value is interpreted in order:

1. **Alias** from `--index-config`, if that option was passed when starting the server.
2. **Local directory** that exists (path to a Lucene index on disk).
3. **Prebuilt index name** known to Pyserini (e.g. `msmarco-v1-passage`); the index is downloaded if needed.

If the index cannot be opened, the API responds with **400** and a message such as `Unable to open index: ...`.

### 1. Search

**Endpoint:** `GET /v1/{index}/search`

**Query parameters**

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `query` | yes | — | Search query string. |
| `hits` | no | `10` | Number of hits (integer ≥ 1). |
| `parse` | no | `true` | If `true`, format the stored `raw` field as JSON (see Anserini `CliUtils.formatDocument`); if `false`, return the raw stored string. |

**Example**

```bash
curl -X GET "http://localhost:8081/v1/msmarco-v1-passage/search?query=what%20is%20a%20lobster%20roll&hits=1"
```

**Example response (shape)**

```json
{
  "api": "v1",
  "index": "msmarco-v1-passage",
  "query": {
    "text": "what is a lobster roll"
  },
  "candidates": [
    {
      "docid": "7157707",
      "score": 11.008299827575684,
      "rank": 1,
      "doc": {
        "contents": "..."
      }
    }
  ]
}
```

The `doc` field may be `null`, a string, or a JSON value depending on the index and `parse` (see `DocumentPayload` in `/openapi.yaml`).

### 2. Get document by id

**Endpoint:** `GET /v1/{index}/doc/{docid}`

**Query parameters**

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `parse` | no | `true` | Same meaning as for search. |

**Example**

```bash
curl -X GET "http://localhost:8081/v1/msmarco-v1-passage/doc/7157707"
```

**Example response (shape)**

```json
{
  "api": "v1",
  "index": "msmarco-v1-passage",
  "docid": "7157707",
  "doc": {
    "contents": "..."
  }
}
```

### 3. Typical HTTP status codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Invalid parameters (e.g. missing `query`, invalid `hits` or `parse`), or cannot open index |
| 404 | Unknown route, or document not found for `GET .../doc/{docid}` |
| 405 | Method not allowed (only **GET** is supported on these routes) |
| 500 | Unhandled server error |

The full list of operations, parameters, and response schemas is in **`/openapi.yaml`**.
