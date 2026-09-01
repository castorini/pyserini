# Pyserini: REST API server (FastAPI)

The Pyserini REST server exposes an **HTTP interface aligned with [Anserini’s REST API](https://github.com/castorini/anserini)** and ships the same **`openapi.yaml`** document (served at **`/openapi.yaml`**). Search and document-fetch routes use `GET`; optional token issuance uses `POST`.

Implementation uses **`SharedSearchBackend`** (`pyserini/server/backend.py`)—the same process-wide search stack as the MCP server. A request may use a **prebuilt index name** (sparse, dense, impact, FAISS, etc., when Pyserini can open it), a **filesystem path** to an index, or an optional **YAML alias** from `--config`.

**v1 limitations:** The public GET API accepts only a **string** `query` parameter. It does **not** expose multimodal payloads, `encoder`, `ef_search`, or sparse `query_generator` options (those exist on the Python API and MCP). Sparse BM25 retrieval uses **k1=0.9** and **b=0.4** by default (same as Anserini). To override BM25, pass **both** `k1` and `b`. For full control over other knobs, use **MCP** or Pyserini directly.

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
- `api_keys` (optional) enables auth on search and document routes.
- Client auth supports either `Authorization: Bearer {api-key}` or `X-API-Key: {api-key}`.

### API token requests and email delivery

Token requests are disabled by default. When enabled, the server claims credentials from a protected
`lookup.json` inventory; it never generates credentials. Only entries with null `name`, `email`, and
`issued_at` fields are available.

Configure a TLS SMTP connection and start the endpoint with both the YAML server config and token pool:

```bash
python -m pyserini.server.rest \
  --config /path/to/server.yaml \
  --enable-token-issuance \
  --token-pool /secure/path/to/lookup.json \
  --token-email-smtp-host smtp.example.edu \
  --token-email-smtp-port 587 \
  --token-email-smtp-security starttls \
  --token-email-smtp-username api@example.edu \
  --token-email-smtp-password-file /secure/path/to/smtp-password \
  --token-email-from api@example.edu \
  --token-email-cc operator@example.edu
```

The password file must be readable only by its owner. At least one individual operator mailbox is
required through `--token-email-cc`; mailing lists and Google Groups are rejected. Omit both SMTP
authentication options when using a trusted relay.

Clients request a token with `POST /v1/token`:

```bash
curl -X POST http://localhost:8081/v1/token \
  -H 'Content-Type: application/json' \
  -d '{"name":"Ada Lovelace","email":"ada@example.edu"}'
```

An accepted request returns **202** with no credential in the response:

```json
{"status":"accepted","message":"Token delivery will be sent by email."}
```

The token is emailed to the requester and the configured service operators. The assignment and
identity are persisted to the protected pool and YAML config, then activated without a restart. The
credential is never returned or written to request logs.

Both `name` and a syntactically valid `email` are required. Anonymous issuance has independent one-hour
cooldowns for the client IP and normalized email by default. A delivery request is accepted only when
neither value has submitted one during the cooldown. Each normalized email owns one token for its
lifetime; an eligible later request resends that same token rather than claiming another. Configure
the interval with `--token-issuance-cooldown`; use `0` to disable it.

Production deployments must serve this endpoint over HTTPS because the request contains personal
identity fields. Protect both the token pool and YAML config as credential stores; neither should be
world- or group-readable.

Disable prebuilt indexes and arbitrary index paths with `--no-prebuilt-indexes`:

```bash
python -m pyserini.server.rest --config /path/to/server.yaml --no-prebuilt-indexes
```

When `--no-prebuilt-indexes` is set, the server only accepts index names declared under `indexes:` in `--config`.

With `api_keys` in `--config`, **`--load-shedding-threshold`** sets the latency threshold (milliseconds, default **3000**) for simple load shedding: if rolling p99 over the last minute is above it, the busiest API key(s) may get **429**. Omitting `api_keys` disables this (and auth) on `/v1/*`.

```bash
python -m pyserini.server.rest --config /path/to/server.yaml --load-shedding-threshold 500
```

The backend uses LRU caching for repeated requests:

- **`--search-cache-size`** (default: **2048**): cache size for search results with string queries
- **`--document-cache-size`** (default: **4096**): cache size for document fetches by docid

```bash
python -m pyserini.server.rest --search-cache-size 4096 --document-cache-size 8192
```

### Logging

REST server logging options:

- `--log-file <path>` writes unified JSONL request logs, one request per line.
- `--keep-uvicorn-logs` keeps uvicorn's default text request access logging. By default,
  uvicorn access logs are disabled because the JSONL request log is the canonical access log.
  If combined with `--log-file`, uvicorn text access lines are appended to the same file.

Each JSONL request record includes the timestamp, request ID, client, method, path, query string
(capped at 1000 characters), status, latency, auth outcome, and a non-reversible API-key fingerprint
when credentials are present. It also includes explicit `qid`, `question`, `retrieval_query`, `run_id`,
`agent`, and `step` fields when clients provide academic trace metadata. Auth failures and load-shedding
responses are written to the same log as successful requests. The server generates a request ID for
each request, logs it, and returns it as `X-Request-ID`.

Example:

```bash
python -m pyserini.server.rest \
  --config /path/to/server.yaml \
  --no-prebuilt-indexes \
  --log-file logs/rest.requests.jsonl
```

To keep uvicorn's text access logs anyway:

```bash
python -m pyserini.server.rest \
  --config /path/to/server.yaml \
  --log-file logs/rest.requests.jsonl \
  --keep-uvicorn-logs
```

In this mode, `logs/rest.requests.jsonl` contains both JSONL request records and uvicorn text access
lines.

Example request log line:

```json
{"auth":"authenticated","client":"127.0.0.1","event":"request","key_id":"7f83b1657ff1","latency_ms":14.217,"method":"GET","path":"/v1/cacm/search","query":"query=information+retrieval&hits=1","query_truncated":false,"request_id":"8dd7f6fa4b7a4a04a029a70c7cf4ec75","status":200,"ts":"2026-05-31T16:42:03.123Z"}
```

## Discovery and documentation

| URL | Purpose |
|-----|---------|
| [`/`](http://localhost:8081/) | Short JSON metadata (name, version, links) |
| [`/openapi.yaml`](http://localhost:8081/openapi.yaml) | OpenAPI 3.0 specification (bundled with the package) |
| [`/docs`](http://localhost:8081/docs) | Swagger UI (FastAPI; may differ slightly from `/openapi.yaml`) |

## API overview (`/v1`)

All search and document routes use the **`GET`** method only. Errors return JSON `{"error": "<message>"}` with a 4xx/5xx status where applicable.

When `api_keys` is configured, search and document routes require authentication; you can use either
`Authorization: Bearer {api-key}` or `X-API-Key: {api-key}`. The optional token-issuance route is
anonymous so that new clients can obtain a credential.

### Optional academic trace metadata

Search and document requests accept optional `qid`, `question`, `run_id`, `agent`, and `step` query
parameters. Clients are encouraged, as a courtesy, to include them whenever the values are known.
They are collected solely for academic research on agent retrieval behavior and do not affect ranking
or response contents.

- `qid`: source-dataset question identifier
- `question`: complete question body the user or agent is answering
- `run_id`: stable identifier shared by requests from one answer attempt
- `agent`: agent or client name and version
- `step`: zero-based retrieval step within the run

The server records these fields alongside the retrieval `query`, request ID, timestamp, API-key
fingerprint, route, status, and latency. Omit unknown values rather than fabricating them. Agents should
propagate the same trace fields to follow-up document fetches.

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
| `k1` | no | `0.9` | BM25 k1 for sparse (TF) indexes. Must be non-negative and sent together with `b`. |
| `b` | no | `0.4` | BM25 b for sparse (TF) indexes. Must be in `[0, 1]`, and sent together with `k1`. |
| `max_doc_length` | no | — | Maximum characters to return for each parsed candidate document. If omitted, return the full document. Requires `parse=true`. |
| `qid` | no | — | Academic trace: source question identifier. |
| `question` | no | — | Academic trace: complete question body. |
| `run_id` | no | — | Academic trace: stable answer-attempt identifier. |
| `agent` | no | — | Academic trace: agent/client name and version. |
| `step` | no | — | Academic trace: zero-based retrieval step. |

**Example**

```bash
curl "http://localhost:8081/v1/msmarco-v1-passage/search?query=what%20is%20a%20lobster%20roll&hits=1"
```

Custom BM25 parameters (sparse indexes only; both required together):

```bash
curl "http://localhost:8081/v1/cacm/search?query=information%20retrieval&hits=5&k1=0.8&b=0.3"
```

Limit document text returned for each hit:

```bash
curl "http://localhost:8081/v1/msmarco-v1-passage/search?query=what%20is%20a%20lobster%20roll&hits=5&max_doc_length=500"
```

`max_doc_length` is measured in characters. For parsed object documents, only `body`, `content`,
`contents`, and `text` are truncated. Other fields are unchanged. Combining `parse=false` with
`max_doc_length` returns **400** to avoid returning malformed JSON strings.

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
| `max_doc_length` | no | — | Maximum characters to return for the parsed document. If omitted, return the full document. Requires `parse=true`. |
| `qid` | no | — | Academic trace: source question identifier. |
| `question` | no | — | Academic trace: complete question body. |
| `run_id` | no | — | Academic trace: stable answer-attempt identifier. |
| `agent` | no | — | Academic trace: agent/client name and version. |
| `step` | no | — | Academic trace: zero-based retrieval step. |

**Example**

```bash
curl "http://localhost:8081/v1/msmarco-v1-passage/doc/7157707"
```

Limit document text returned:

```bash
curl "http://localhost:8081/v1/msmarco-v1-passage/doc/7157707?max_doc_length=500"
```

`max_doc_length` is measured in characters. For parsed object documents, only `body`, `content`,
`contents`, and `text` are limited. Other fields are unchanged. Combining `parse=false` with
`max_doc_length` returns **400** to avoid returning malformed JSON strings.

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
| 202 | Token delivery request accepted; the credential is sent by email and is not returned by HTTP |
| 400 | Invalid parameters (e.g. missing `query`, invalid `hits` or `parse`), or cannot open index |
| 401 | Missing or invalid API credential (when `api_keys` is configured) |
| 429 | Load shedding, or token-request cooldown for the observed client IP or normalized email; `Retry-After` may be set |
| 404 | Unknown route, or document not found for `GET .../doc/{docid}` |
| 405 | Method not allowed (`POST` is required for `/v1/token`; the search and document routes use `GET`) |
| 500 | Unhandled server error |
| 503 | Token delivery is disabled, inventory is exhausted, or email delivery failed |

The full list of operations, parameters, and response schemas is in **`/openapi.yaml`**.
