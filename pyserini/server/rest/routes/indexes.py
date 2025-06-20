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
Index-related API endpoints for the Pyserini server.

Provides routes for searching indexes, retrieving documents, checking index status, listing indexes, and updating or fetching index settings.
"""

from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional, Dict, Any
from pyserini.server.search_controller import get_controller

router = APIRouter(prefix="/indexes", tags=["indexes"])


@router.get("/{index}/search")
async def search_index(
    index: str = Path(..., description="Index name"),
    query: str = Query(..., description="Search query"),
    hits: int = Query(default=10, description="Number of hits to return"),
    qid: str = Query(default="", description="Query ID"),
    ef_search: Optional[int] = Query(None, description="EF search parameter"),
    encoder: Optional[str] = Query(None, description="Encoder to use"),
    query_generator: Optional[str] = Query(None, description="Query generator to use"),
    shard: Optional[bool] = Query(False, description="Shard identifier"),
) -> Dict[str, Any]:
    try:
        if shard:
            return get_controller().sharded_search(
                query, index, hits, encoder
            )
        return get_controller().search(
            query, index, hits, qid, ef_search, encoder, query_generator
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{index}/documents/{docid}")
async def get_document(
    docid: str = Path(..., description="Document ID"),
    index: str = Path(..., description="Index name"),
) -> Dict[str, Any]:
    try:
        return get_controller().get_document(docid, index)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{index}/status")
async def get_index_status(
    index: str = Path(..., description="Index name")
) -> Dict[str, Any]:
    return {"cached": get_controller().get_status(index)}


@router.get("/")
async def list_indexes() -> Dict[str, Dict[str, Any]]:
    try:
        return get_controller().get_indexes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{index}/settings")
async def update_index_settings(
    index: str = Path(..., description="Index name"),
    ef_search: Optional[int] = Query(None, description="EF search parameter"),
    encoder: Optional[str] = Query(None, description="Encoder to use"),
    query_generator: Optional[str] = Query(None, description="Query generator to use"),
) -> Dict[str, Any]:
    try:
        return get_controller().update_settings(index, ef_search, encoder, query_generator)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{index}/settings")
async def get_index_settings(
    index: str = Path(..., description="Index name")
) -> Dict[str, Any]:
    try:
        return get_controller().get_settings(index)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
