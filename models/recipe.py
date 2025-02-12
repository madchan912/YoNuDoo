from beanie import Document
from typing import List
from pydantic import BaseModel

# MongoDB 컬렉션을 위한 레시피 모델
class Recipe(Document):
    title: str  # 레시피 제목
    ingredients: List[str]  # 재료 목록
    url: str  # 유튜브 링크

    class Settings:
        collection = "recipes"  # MongoDB에서 사용할 컬렉션 이름

# API에서 요청 데이터를 검증할 때 사용하는 모델
class RecipeCreate(BaseModel):
    title: str
    ingredients: List[str]
    url: str
