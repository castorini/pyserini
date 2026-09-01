# Token issuance and BM25 REST API design

## Purpose and scope

This document specifies the public Pyserini REST service used to issue search credentials and query
the ClimbMix BM25 index. It covers credential inventory, identity binding, anti-spam behavior, email
delivery, authentication, retrieval parameters, traces, logging, failure handling, and operational
security.

The service has two separate responsibilities:

1. `POST /v1/token` assigns and emails an existing pre-generated credential.
2. Authenticated `GET` routes search an allowed index or fetch one stored document.

The server never creates credentials. Token generation is an offline administrative operation in a
private repository.

## Production topology

The public HTTPS reverse proxy forwards requests to one Pyserini process. Production starts Pyserini
with `--no-prebuilt-indexes`, so clients can access only aliases declared in the protected YAML
configuration. The ClimbMix deployment exposes the `climbmix-400b` alias.

The mutable security state is stored outside the source checkout:

| Store | Contents | Required mode |
| --- | --- | --- |
| Token pool JSON | Pre-generated tokens and their assignment state | `0600` |
| Server YAML | Index aliases, active API keys, and new token identities | `0600` |
| SMTP password file | Gmail app password used only by the service | `0600` |
| Request JSONL | Request metadata and non-reversible key fingerprints | Operator-only |

The token pool and YAML config are runtime state. A deployment must preserve their current copies;
restoring an older blank inventory can recycle an already issued credential.

## Token properties and lifecycle

### Credential format

- Each token is 32 random bytes encoded as 64 hexadecimal characters.
- This provides 256 bits of entropy and requires no embedded identity or expiration data.
- Tokens are opaque bearer credentials. The service does not use JWTs and cannot derive identity
  from the token itself.
- Clients send the token in `Authorization: Bearer TOKEN` or `X-API-Key: TOKEN`. Query-string tokens
  are not supported because URLs are commonly logged.

### Inventory schema

Each private `lookup.json` row has this shape:

```json
{
  "token": "64 hexadecimal characters",
  "name": null,
  "email": null,
  "issued_at": null
}
```

A row is available only when `name`, `email`, and `issued_at` are all present and all `null`. Any
legacy or partially populated row is reserved and cannot be claimed. Token strings must be unique.
New rows are appended; existing rows are never deleted or reordered during preallocation.

### Assignment and activation

For a new normalized email, the endpoint performs these steps:

1. Reserve the observed client IP and normalized email in the cooldown table.
2. Atomically claim the first available pool row and write `name`, normalized `email`, and Unix
   `issued_at`.
3. Atomically append the token to `api_keys` in the YAML configuration.
4. Persist `{name, email}` under `api_key_identities[token]`.
5. Add the token to the process's immutable authentication snapshot so it works without restart.
6. Send the token to the requester and configured individual operator CC recipients.

The normalized email owns one token for its lifetime. A later eligible request for the same email
resends the same credential and does not consume another pool row. Existing legacy tokens remain
valid and are not modified.

If activation fails after a pool row is claimed, a retry for the same email recovers that same row.
If email delivery fails after activation, the endpoint returns `503`, releases the cooldown
reservation, and permits a retry that resends the same token.

## Token delivery endpoint

### Request

```http
POST /v1/token
Content-Type: application/json

{"name":"Ada Lovelace","email":"ada@example.org"}
```

- `name` is required, stripped of surrounding whitespace, and limited to 200 characters.
- `email` is required, stripped, case-folded, syntactically validated, and limited to 254 characters.
- Unknown JSON fields are rejected.
- The endpoint itself is anonymous; issued credentials protect the retrieval routes.

### Anti-spam policy

The default cooldown is 3,600 seconds. IP and email checks are independent: a request is accepted
only when both the observed client IP and normalized email are outside their cooldown windows.
Otherwise the endpoint returns `429` with `Retry-After`.

Cooldown state is process-local and resets on restart. Lifetime email ownership is persistent in the
YAML identity map and token pool, so restarts cannot allocate a second token to an existing email.
The reverse proxy must pass the real client address only from a trusted proxy; accepting arbitrary
forwarded-IP headers would let clients bypass the IP check.

### Response contract

Successful delivery returns `202`:

```json
{"status":"accepted","message":"Token delivery will be sent by email."}
```

The response never contains the token and includes `Cache-Control: no-store` and `Pragma: no-cache`.
Errors use `{"error":"..."}`:

| Status | Meaning |
| --- | --- |
| `400` | Missing or invalid identity fields |
| `429` | Client IP or normalized email is cooling down |
| `503` | Issuance disabled, inventory exhausted, persistence failed, or email failed |

### Email delivery

Production uses Gmail SMTP over STARTTLS:

- Host: `smtp.gmail.com`
- Port: `587`
- Username and sender: `castorini.api@gmail.com`
- Authentication: a dedicated Google app password in an owner-only file
- CC: `lingwei.gu@uwaterloo.ca`, `njedidi@uwaterloo.ca`, `jimmylin@uwaterloo.ca`, and
  `l2ge@uwaterloo.ca`

The submitted user is the primary recipient. Operator recipients are explicit individual mailboxes;
mailing lists and `googlegroups.com` CC addresses are rejected. The HTTP response and request log do
not contain the credential. The message states that it is a no-reply email and directs users who need
help to use Reply all so the CC'd service administrators receive their question.

## BM25 and document API

The production base URL is `https://api.castorini.uwaterloo.ca/v1`. The examples below use Bearer
authentication; `X-API-Key` is equivalent.

### Search

```bash
curl --get 'https://api.castorini.uwaterloo.ca/v1/climbmix-400b/search' \
  -H 'Authorization: Bearer TOKEN' \
  --data-urlencode 'query=renewable energy storage' \
  --data-urlencode 'hits=10' \
  --data-urlencode 'parse=true'
```

| Parameter | Required | Default | Contract |
| --- | --- | --- | --- |
| `query` | Yes | None | Non-empty string retrieval query |
| `hits` | No | `10` | Positive result count |
| `parse` | No | `true` | Parse stored JSON when possible; `false` returns the raw stored string |
| `k1` | No | `0.9` | Finite non-negative BM25 term-frequency saturation; supply with `b` |
| `b` | No | `0.4` | Finite value in `[0, 1]`; supply with `k1` |
| `max_doc_length` | No | Full document | Positive character cap; requires `parse=true` |

`k1` and `b` are valid only for sparse TF indexes and must be both present or both omitted. Responses
contain `api`, `index`, `query.text`, and ranked `candidates`; every candidate has `docid`, `score`,
one-based `rank`, and `doc`.

### Document fetch

```bash
curl --get 'https://api.castorini.uwaterloo.ca/v1/climbmix-400b/doc/DOCID' \
  -H 'X-API-Key: TOKEN' \
  --data-urlencode 'parse=true'
```

The document route accepts `parse` and `max_doc_length` with the same semantics as search. A successful
response contains `api`, `index`, `docid`, and `doc`; an unknown document returns `404`.

### Retrieval errors and load shedding

| Status | Meaning |
| --- | --- |
| `200` | Search or document fetch succeeded |
| `400` | Invalid parameters, unavailable index, or BM25 parameters on a non-sparse index |
| `401` | Missing or invalid credential |
| `404` | Document or route not found |
| `429` | Load shedding; honor `Retry-After` and retry with jitter |
| `500` | Internal server failure |

Authenticated requests participate in rolling load shedding. When recent p99 latency exceeds the
configured threshold, the busiest keys in the rolling one-minute window may receive `429`.

## Academic trace metadata and logs

Search and document requests accept optional `qid`, `question`, `run_id`, `agent`, and zero-based
`step` query parameters. Agents should populate them when available. The server records these fields
for academic analysis together with the retrieval `query`; their collection is by courtesy and for
purely academic use.

Each JSONL request record contains timestamp, request ID, observed client, method, path, bounded query
data, response status, latency, authentication outcome, and a 12-character SHA-256 token fingerprint.
It never records the raw credential. `question` is capped at 8,192 characters, retrieval `query` at
4,096, the raw query string at 1,000, and shorter identifiers at 256; truncation flags are explicit.
Every response includes `X-Request-ID` for correlation.

## Operational invariants

- Generate token inventory offline; the server only claims existing rows.
- Preserve every existing assigned row and token value.
- Keep the mutable runtime pool, YAML config, SMTP secret, backups, and logs access-controlled.
- Serve identity submission and bearer credentials only over HTTPS.
- Never print, return, commit, or log Gmail app passwords or issued tokens.
- Back up the runtime pool and YAML config together before restart or deployment.
- Test issuance with one new email and client IP, then verify the emailed token on an authenticated
  BM25 request while confirming an existing token still works.
