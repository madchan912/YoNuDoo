from fastapi import APIRouter, HTTPException
from models.recipe import Recipe, RecipeCreate
from models.autocomplete import AutoComplete
from typing import List
from beanie import PydanticObjectId

router = APIRouter()

# 한글 초성 변환 함수
def get_chosung(text):
    CHOSUNG = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
    HANGUL_START = 0xAC00
    HANGUL_END = 0xD7A3
    CHOSUNG_INTERVAL = 588

    return "".join([
        CHOSUNG[(ord(char) - HANGUL_START) // CHOSUNG_INTERVAL] if HANGUL_START <= ord(char) <= HANGUL_END else char
        for char in text
    ])

# 자동완성 데이터 저장 함수
async def update_autocomplete(ingredients: List[str]):
    for ingredient in ingredients:
        search_keywords = list(set(ingredient) | set(get_chosung(ingredient)))

        existing_entry = await AutoComplete.find_one(AutoComplete.ingredient == ingredient)
        if existing_entry:
            existing_entry.search_keywords = list(set(existing_entry.search_keywords + search_keywords))
            await existing_entry.save()
        else:
            new_entry = AutoComplete(ingredient=ingredient, search_keywords=search_keywords)
            await new_entry.insert()

# 레시피 추가 API
@router.post("/", response_model=Recipe)
async def create_recipe(recipe: RecipeCreate):
    new_recipe = Recipe(**recipe.dict())
    await new_recipe.insert()

    await update_autocomplete(recipe.ingredients)

    return new_recipe

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