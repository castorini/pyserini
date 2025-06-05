"""
Index-related API endpoints for the Pyserini server.

Provides routes for searching indexes, retrieving documents, checking index status, listing indexes, and updating or fetching index settings.
"""
from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional, Dict, Any
from task_manager import manager

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
    shard: Optional[str] = Query(None, description="Shard identifier"),
) -> Dict[str, Any]:
    try:
        return manager.search(
            query, index, hits, qid, ef_search, encoder, query_generator, shard
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
        return manager.get_document(docid, index)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{index}/status")
async def get_index_status(
    index: str = Path(..., description="Index name")
) -> Dict[str, Any]:
    return {"cached": manager.get_status(index)}


@router.get("/")
async def list_indexes() -> Dict[str, Dict[str, Any]]:
    try:
        return manager.get_indexes()
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
        return manager.update_settings(index, ef_search, encoder, query_generator)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{index}/settings")
async def get_index_settings(
    index: str = Path(..., description="Index name")
) -> Dict[str, Any]:
    try:
        return manager.get_settings(index)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
