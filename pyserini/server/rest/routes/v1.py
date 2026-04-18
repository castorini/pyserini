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

"""Anserini OpenAPI v1 routes: ``GET /v1/{index}/search`` and ``GET /v1/{index}/doc/{docid}``.

``{index}`` uses a path-style converter so filesystem paths may contain ``/`` (e.g.
``/v1/project/indexes/msmarco/search``). For an absolute index path, use a URL with an
empty segment after the API prefix, e.g. ``/v1//data/indexes/msmarco/search``.
"""

from __future__ import annotations

import asyncio

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

from pyserini.server.rest.backend import LuceneSearcherRestBackend

router = APIRouter(tags=['v1'])

DEFAULT_HITS = 10


def _error(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={'error': message})


def _parse_bool(raw: str | None, default: bool, name: str) -> tuple[bool | None, JSONResponse | None]:
    if raw is None:
        return default, None
    lowered = raw.strip().lower()
    if lowered == 'true':
        return True, None
    if lowered == 'false':
        return False, None
    return None, _error(400, f"Parameter '{name}' must be 'true' or 'false'")


def _backend(request: Request) -> LuceneSearcherRestBackend:
    return request.app.state.lucene_rest


@router.get('/{index:path}/search')
async def search_v1(
    request: Request,
    index: str,
    query: str | None = Query(None),
    hits: str | None = Query(None),
    parse: str | None = Query(None),
):
    backend = _backend(request)
    index_token = backend.decode_path_segment(index)

    if query is None or not str(query).strip():
        return _error(400, "Parameter 'query' is required")

    hits_val = DEFAULT_HITS
    if hits is not None and str(hits).strip() != '':
        try:
            hits_val = int(hits)
        except ValueError:
            return _error(400, "Parameter 'hits' must be an integer")
        if hits_val <= 0:
            return _error(400, "Parameter 'hits' must be positive")

    parse_flag, bad_parse = _parse_bool(parse, True, 'parse')
    if bad_parse is not None:
        return bad_parse
    assert parse_flag is not None

    payload = await asyncio.to_thread(backend.search, index_token, query, hits_val, parse_flag)
    if payload is None:
        return _error(400, f'Unable to open index: {index_token}')
    return payload


@router.get('/{index:path}/doc/{docid}')
async def get_document_v1(
    request: Request,
    index: str,
    docid: str,
    parse: str | None = Query(None),
):
    backend = _backend(request)
    index_token = backend.decode_path_segment(index)
    docid_token = backend.decode_path_segment(docid)

    if docid_token is None or not str(docid_token).strip():
        return _error(400, "Path parameter 'docid' is required")

    parse_flag, bad_parse = _parse_bool(parse, True, 'parse')
    if bad_parse is not None:
        return bad_parse
    assert parse_flag is not None

    body, index_ok = await asyncio.to_thread(backend.get_document, index_token, docid_token, parse_flag)
    if not index_ok:
        return _error(400, f'Unable to open index: {index_token}')
    if body is None:
        return _error(404, f'Document not found: {docid_token}')
    return body
