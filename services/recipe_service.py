from models.recipe import Recipe, RecipeCreate
from services.autocomplete_service import update_autocomplete
from beanie import PydanticObjectId
from typing import List

# 새로운 레시피 생성 로직
async def create_recipe(recipe_data: RecipeCreate):
    new_recipe = Recipe(**recipe_data.dict())
    await new_recipe.insert()
    await update_autocomplete(recipe_data.ingredients)
    return new_recipe

# 모든 레시피 조회
async def get_all_recipes():
    return await Recipe.find().to_list()

# 특정 레시피 조회
async def get_filtered_recipes(ingredients: str):
    if not ingredients:
        return await get_all_recipes()

    ingredient_list = ingredients.split(",")
    return await Recipe.find({"ingredients": {"$all": ingredient_list}}).to_list()

# 특정 레시피 수정
async def update_recipe(recipe_id: PydanticObjectId, updated_data: RecipeCreate):
    recipe = await Recipe.get(recipe_id)
    if not recipe:
        return None

    update_data = updated_data.dict()
    await recipe.set(update_data)

    # 자동완성 데이터 업데이트(새로운 재료만 추가)
    await update_autocomplete(updated_data.ingredients)

    return recipe

# 특정 레시피 삭제
async def delete_recipe(recipe_id: PydanticObjectId):
    recipe = await Recipe.get(recipe_id)
    if not recipe:
        return None

    await recipe.delete()
    return {"message": "레시피 삭제 성공!"}

# 여러 개의 레시피 한 번에 추가
async def create_multiple_recipes(recipes: List[RecipeCreate]):
    new_recipes = [Recipe(**recipe.dict()) for recipe in recipes]
    await Recipe.insert_many(new_recipes)

    all_ingredients = set(ingredient for recipe in recipes for ingredient in recipe.ingredients)
    await update_autocomplete(list(all_ingredients))

    return {"message": f"{len(new_recipes)}개의 레시피가 추가되었습니다!"}
