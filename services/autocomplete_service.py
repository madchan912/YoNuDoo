from models.autocomplete import AutoComplete
from typing import List

# 한글 검색 키워드 생성 함수 (초성, 중성 변환)
def generate_search_keywords(ingredient: str) -> List[str]:
    base_code = 0xAC00  # '가'의 유니코드
    CHOSUNG = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ",
               "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
    compound_final_map = {3: 1, 5: 4, 6: 4, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 8, 15: 8, 19: 17}

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
    return list(search_keywords)

# 자동완성 데이터 업데이트 함수 (DB 저장/업데이트 처리)
async def update_autocomplete(ingredients: List[str]):
    for ingredient in ingredients:
        search_keywords = generate_search_keywords(ingredient)

        existing_entry = await AutoComplete.find_one(AutoComplete.ingredient == ingredient)
        if existing_entry:
            existing_entry.search_keywords = list(set(existing_entry.search_keywords + search_keywords))
            await existing_entry.save()
        else:
            new_entry = AutoComplete(ingredient=ingredient, search_keywords=search_keywords)
            await new_entry.insert()

# 자동완성 검색 기능
async def search_autocomplete(query: str):
    results = await AutoComplete.find(
        {"search_keywords": {"$regex": f"^{query}", "$options": "i"}}
    ).to_list()

    return [result.ingredient for result in results]