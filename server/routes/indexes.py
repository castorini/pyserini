from fastapi import APIRouter, Query, Path
from typing import Optional, Dict, Any
from dataclasses import asdict

from task_manager import manager

router = APIRouter(
    prefix="/indexes",
    tags=["indexes"]
)


@router.get("/{index}/status")
async def get_index_status(
    index: str = Path(..., description="Index name")
) -> Dict[str, Any]:
    return {
        "cached": manager.get_status(index)
    }

@router.get("/")
async def list_indexes() -> Dict[str, Dict[str, Any]]:
    return asdict(manager.indexes)

@router.post("/{index}/settings")
async def update_index_settings(
    index: str = Path(..., description="Index name"),
    ef_search: Optional[str] = Query(None, description="EF search parameter"),
    encoder: Optional[str] = Query(None, description="Encoder to use"),
    query_generator: Optional[str] = Query(None, description="Query generator to use")
) -> Dict[str, Any]:
    return manager.update_settings(index, ef_search, encoder, query_generator)

@router.get("/{index}/settings")
async def get_index_settings(
    index: str = Path(..., description="Index name")
) -> Dict[str, Any]:
    return manager.get_settings(index)