from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.db.services.shaders import get_shaders_window, get_shaders_total
from app.models import (
    PaginationOptions, 
    PaginationMeta,
    PaginationResponse,
    ShaderView
)

router = APIRouter(prefix="/explore", tags=["explore"])

@router.get("/", response_model=PaginationResponse[ShaderView])
async def get_shaders(pagination: PaginationOptions = Depends(PaginationOptions.as_query), search: str = None):
    result = await get_shaders_window(pagination)
    #print("RESULT:", type(result[0]))
    shader_views = [ShaderView(id=s.id, author=str(s.author_id), title=s.title) for s in result]
    total = await get_shaders_total()
    return PaginationResponse[ShaderView](
        data=shader_views,
        meta=PaginationMeta(
            offset=pagination.offset,
            limit=pagination.limit, 
            total=total
        )
    )
