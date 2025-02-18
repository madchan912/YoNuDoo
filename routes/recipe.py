from fastapi import APIRouter, HTTPException, Query
from services.recipe_service import (
    create_recipe, get_all_recipes, update_recipe, delete_recipe, create_multiple_recipes, get_filtered_recipes
)
from models.recipe import RecipeCreate
from beanie import PydanticObjectId
from typing import List

router = APIRouter()

# 레시피 생성
@router.post("/", response_model=RecipeCreate)
async def create_recipe_api(recipe: RecipeCreate):
    return await create_recipe(recipe)

# 모든 레시피 조회
@router.get("/all")
async def get_all_recipes_api():
    return await get_all_recipes()

# 특정 레시피 조회
@router.get("/")
async def get_filtered_recipes_api(ingredients: str = Query(None)):
    return await get_filtered_recipes(ingredients)


# 특정 레시피 수정
@router.put("/{recipe_id}")
async def update_recipe_api(recipe_id: PydanticObjectId, updated_data: RecipeCreate):
    recipe = await update_recipe(recipe_id, updated_data)
    if not recipe:
        raise HTTPException(status_code=404, detail="레시피를 찾을 수 없습니다.")
    return recipe

# 특정 레시피 삭제
@router.delete("/{recipe_id}")
async def delete_recipe_api(recipe_id: PydanticObjectId):
    result = await delete_recipe(recipe_id)
    if not result:
        raise HTTPException(status_code=404, detail="레시피를 찾을 수 없습니다.")
    return result

# 여러 개의 레시피 한 번에 추가
@router.post("/bulk")
async def create_multiple_recipes_api(recipes: List[RecipeCreate]):
    return await create_multiple_recipes(recipes)
