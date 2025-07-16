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

from fastapi import APIRouter, Query, Path, Depends, HTTPException
from typing import Any
from pyserini.server.search_controller import get_controller
from pyserini.server.models import INDEX_TYPE, Hits, Document, SearchParams, IndexSettingParams, IndexStatus, IndexSetting

router = APIRouter(prefix='/indexes', tags=['indexes'])
    
@router.get('/{index}/search', response_model=Hits)
async def search_index(
    index: str = Path(..., description='Index name'),
    params: SearchParams = Depends()
) -> Hits:
    try:
        return get_controller().search(
            params.query, index, params.hits, params.qid,
            params.ef_search, params.encoder, params.query_generator
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{index}/documents/{docid}', response_model=Document)
async def get_document(
    docid: str = Path(..., description='Document ID'),
    index: str = Path(..., description='Index name'),
) -> Document:
    try:
        return get_controller().get_document(docid, index)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{index}/status', response_model=IndexStatus)
async def get_index_status(
    index: str = Path(..., description='Index name')
) -> dict[str, Any]:
    return get_controller().get_status(index)


@router.get('/', response_model=list[str])
async def list_indexes(
    index_type: str = Query(..., description=f"Type of index out of {INDEX_TYPE.keys()}")
) -> list[str]:
    try:
        return get_controller().get_indexes(index_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/{index}/settings', response_model=dict[str, str])
async def update_index_settings(
    index: str = Path(..., description='Index name'),
    params: IndexSettingParams = Depends()
) -> dict[str, str]:
    try:
        get_controller().update_settings(index, params.ef_search, params.encoder, params.query_generator)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{index}/settings', response_model=IndexSetting)
async def get_index_settings(
    index: str = Path(..., description='Index name')
) -> IndexSetting:
    try:
        return get_controller().get_settings(index)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
