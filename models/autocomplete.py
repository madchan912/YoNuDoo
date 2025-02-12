from beanie import Document
from typing import List

class AutoComplete(Document):
    ingredient: str  # ✅ 재료명 필드 추가
    search_keywords: List[str]  # ✅ 검색어 목록

    class Settings:
        collection = "autocomplete"