# Pyserini: REST API server (FastAPI)

The Pyserini REST server exposes an **HTTP interface aligned with [Anserini’s REST API](https://github.com/castorini/anserini)** and ships the same **`openapi.yaml`** document (served at **`/openapi.yaml`**). Routes are **GET-only** for search and document fetch.

Implementation uses **`SharedSearchBackend`** (`pyserini/server/backend.py`)—the same process-wide search stack as the MCP server. A request may use a **prebuilt index name** (sparse, dense, impact, FAISS, etc., when Pyserini can open it), a **filesystem path** to an index, or an optional **YAML alias** from `--config`.

**v1 limitations:** The public GET API accepts only a **string** `query` parameter. It does **not** expose multimodal payloads, `encoder`, `ef_search`, or sparse `query_generator` options (those exist on the Python API and MCP). For full control over those knobs, use **MCP** or Pyserini directly.

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

## Config and deployment options

Use `--config` to provide a YAML server config with index mappings and optional API keys:

```yaml
indexes:
  my_tf_alias: /path/to/lucene/index
  my_dense_alias:
    path: /path/to/dense/index
    index_type: faiss
    base_index: my_tf_alias
    encoder: BAAI/bge-base-en-v1.5
api_keys:
  - {api-key}
  - {api-key-2}
```

Start the server with that config:

```bash
python -m pyserini.server.rest --config /path/to/server.yaml
```

With `--config` enabled:

- `indexes` maps alias names to local index configs:
  - short form: `alias: /path/to/index` (defaults to `index_type: tf`)
  - object form: `alias: {path, index_type, ...}`
  - supported `index_type`: `tf`, `lucene_flat`, `lucene_hnsw`, `impact`, `faiss`
  - `encoder` is required for `impact`, `faiss`, `lucene_flat`, `lucene_hnsw` local indexes.
  - optional `base_index` links dense/impact/faiss aliases to the sparse Lucene alias used for stored document fetch.
  - optional `encoder` and `ef_search` provide per-index defaults (request-level values still override them).
- `api_keys` (optional) enables auth on all `/v1/*` routes.
- Client auth supports either `Authorization: Bearer {api-key}` or `X-API-Key: {api-key}`.

Disable prebuilt indexes and arbitrary index paths with `--no-prebuilt-indexes`:

```bash
python -m pyserini.server.rest --config /path/to/server.yaml --no-prebuilt-indexes
```

When `--no-prebuilt-indexes` is set, the server only accepts index names declared under `indexes:` in `--config`.

### Logging

REST server logging options:

- `--server-log-file <path>` writes uvicorn error + access logs to a file.
- `--auth-log-file <path>` writes auth request attribution logs (client, route, status, key fingerprint) to a file.
- `--no-access-log` disables uvicorn request access logging.

Example:

```bash
python -m pyserini.server.rest \
  --config /path/to/server.yaml \
  --no-prebuilt-indexes \
  --server-log-file logs/rest.server.log \
  --auth-log-file logs/rest.auth.log
```

## Discovery and documentation

| URL | Purpose |
|-----|---------|
| [`/`](http://localhost:8081/) | Short JSON metadata (name, version, links) |
| [`/openapi.yaml`](http://localhost:8081/openapi.yaml) | OpenAPI 3.0 specification (bundled with the package) |
| [`/docs`](http://localhost:8081/docs) | Swagger UI (FastAPI; may differ slightly from `/openapi.yaml`) |

## API overview (`/v1`)

All search and document routes use the **`GET`** method only. Errors return JSON `{"error": "<message>"}` with a 4xx/5xx status where applicable.

When `api_keys` is configured, every `/v1/*` route requires authentication; you can use either
`Authorization: Bearer {api-key}` or `X-API-Key: {api-key}` on any endpoint.

### Index parameter `{index}`

The `{index}` path parameter may contain **slashes**, so a relative filesystem path can appear directly under `/v1/` (for example `GET /v1/project/indexes/msmarco/search`).

For an **absolute** filesystem path (leading `/`), use an **extra slash** after `/v1/` so the first URL segment is empty and the index value keeps its leading slash—for example `GET /v1//data/indexes/msmarco/search` for index `/data/indexes/msmarco`.

That value is interpreted in order:

1. **Alias** from `--config`, if that option was passed when starting the server.
2. **Local directory** that exists (path to an index on disk), unless `--no-prebuilt-indexes` is set.
3. **Prebuilt index name** known to Pyserini (e.g. `msmarco-v1-passage`), unless `--no-prebuilt-indexes` is set.

If the index cannot be opened, the API responds with **400** and a message such as `Unable to open index: ...`.

### 1. Search

**Endpoint:** `GET /v1/{index}/search`

**Query parameters**

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `query` | yes | — | Search query string. |
| `hits` | no | `10` | Number of hits (integer ≥ 1). |
| `parse` | no | `true` | If `true`, parse the stored `raw` field when it is JSON (see `format_lucene_document` / Anserini-style formatting); if `false`, return the raw stored string. |


**Example**

```bash
curl "http://localhost:8081/v1/msmarco-v1-passage/search?query=what%20is%20a%20lobster%20roll&hits=1"
```

With API key auth enabled (`api_keys` in `--config`), for example:

```bash
curl -H "Authorization: Bearer {api-key}" \
  "http://localhost:8081/v1/msmarco-v1-passage/search?query=what%20is%20a%20lobster%20roll&hits=1"
```

**Example response (shape)**

Scores are **rounded to six decimal places** internally.

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
      "score": 11.0083,
      "rank": 1,
      "doc": "..."
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
curl "http://localhost:8081/v1/msmarco-v1-passage/doc/7157707"
```

With API key auth enabled (`api_keys` in `--config`), for example:

```bash
curl -H "X-API-Key: {api-key}" \
  "http://localhost:8081/v1/msmarco-v1-passage/doc/7157707"
```

**Example response (shape)**

```json
{
  "api": "v1",
  "index": "msmarco-v1-passage",
  "docid": "7157707",
  "doc": "..."
}
```

### 3. Typical HTTP status codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Invalid parameters (e.g. missing `query`, invalid `hits` or `parse`), or cannot open index |
| 401 | Missing or invalid API credential (when `api_keys` is configured) |
| 404 | Unknown route, or document not found for `GET .../doc/{docid}` |
| 405 | Method not allowed (only **GET** is supported on these routes) |
| 500 | Unhandled server error |

The full list of operations, parameters, and response schemas is in **`/openapi.yaml`**.
