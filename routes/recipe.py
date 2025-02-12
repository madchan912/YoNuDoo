from fastapi import APIRouter, HTTPException
from models.recipe import Recipe, RecipeCreate
from models.autocomplete import AutoComplete
from typing import List
from beanie import PydanticObjectId

router = APIRouter()

# 자동완성 데이터 저장 함수
async def update_autocomplete(ingredients: List[str]):
    base_code = 0xAC00  # '가'의 유니코드
    CHOSUNG = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ",
               "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
    compound_final_map = {3: 1, 5: 4, 6: 4, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 8, 15: 8, 19: 17}

    for ingredient in ingredients:
        search_keywords = set()

        for char in ingredient:
            if not ('가' <= char <= '힣'):
                search_keywords.add(char)
                continue

            code = ord(char) - base_code
            chosung_index = code // (21 * 28)
            jungsung_index = (code % (21 * 28)) // 28
            jongsung_index = code % 28

            initial = CHOSUNG[chosung_index]
            no_final = chr(base_code + (chosung_index * 21 * 28) + (jungsung_index * 28))

            search_keywords.add(initial)
            search_keywords.add(no_final)

            if jongsung_index != 0:
                if jongsung_index in compound_final_map:
                    first_final_index = compound_final_map[jongsung_index]
                    variant = chr(base_code + (chosung_index * 21 * 28) + (jungsung_index * 28) + first_final_index)
                    search_keywords.add(variant)
                search_keywords.add(char)

        search_keywords.add(ingredient)

        existing_entry = await AutoComplete.find_one(AutoComplete.ingredient == ingredient)
        if existing_entry:
            existing_entry.search_keywords = list(set(existing_entry.search_keywords + list(search_keywords)))
            await existing_entry.save()
        else:
            new_entry = AutoComplete(ingredient=ingredient, search_keywords=list(search_keywords))
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