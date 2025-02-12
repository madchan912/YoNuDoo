from fastapi import APIRouter, HTTPException
from models.recipe import Recipe, RecipeCreate
from beanie import PydanticObjectId

router = APIRouter()

# 레시피 추가 API
@router.post("/")
async def create_recipe(recipe: RecipeCreate):
    new_recipe = Recipe(**recipe.dict())
    await new_recipe.insert()
    return {"message": "레시피 추가 성공!", "recipe": new_recipe}

# 모든 레시피 조회 API
@router.get("/")
async def get_all_recipes():
    recipes = await Recipe.find().to_list()
    return recipes


# 특정 레시피 수정 API
@router.put("/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: PydanticObjectId, updated_data: RecipeCreate):
    recipe = await Recipe.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="레시피를 찾을 수 없습니다.")

    update_data = updated_data.dict()
    await recipe.update({"$set": update_data})
    return recipe


# 특정 레시피 삭제 API
@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: PydanticObjectId):
    recipe = await Recipe.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="레시피를 찾을 수 없습니다.")

    await recipe.delete()
    return {"message": "레시피 삭제 성공!"}