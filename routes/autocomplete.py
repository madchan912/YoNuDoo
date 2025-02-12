from fastapi import APIRouter, Query
from models.autocomplete import AutoComplete

router = APIRouter()

@router.get("/autocomplete")
async def get_autocomplete(query: str = Query(..., min_length=1)):
    results = await AutoComplete.find(
        {"search_keywords": {"$regex": f"^{query}"}}
    ).to_list()

    return [result.ingredient for result in results]