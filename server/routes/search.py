from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, Dict, Any

from task_manager import manager

router = APIRouter(
    prefix="/search",
    tags=["search"]
)


@router.get("/")
async def search_index(
    index: str = Query(..., description="Index name"),
    query: str = Query(..., description="Search query"),
    hits: int = Query(default=10, description="Number of hits to return"),
    qid: str = Query(default="", description="Query ID"),
    ef_search: Optional[int] = Query(None, description="EF search parameter"),
    encoder: Optional[str] = Query(None, description="Encoder to use"),
    query_generator: Optional[str] = Query(None, description="Query generator to use"),
    shard: Optional[str] = Query(None, description="Shard identifier")
) -> Dict[str, Any]:
    try:
        return manager.search(query, index, hits, qid, ef_search, encoder, query_generator, shard)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/documents/{docid}")
async def get_document(
    docid: str = Path(..., description="Document ID"),
    index: str = Query(..., description="Index name")
) -> Dict[str, Any]:
    try:
        return manager.get_document(docid, index)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 