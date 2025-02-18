from fastapi import APIRouter, Query
from services.autocomplete_service import search_autocomplete

router = APIRouter()

# 자동완성 검색 API
@router.get("/autocomplete")
async def get_autocomplete(query: str = Query(..., min_length=1)):
    return await search_autocomplete(query)
