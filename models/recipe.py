from beanie import Document
from typing import List
from pydantic import BaseModel, Field

# MongoDB 컬렉션을 위한 레시피 모델
class Recipe(Document):
    title: str = Field(..., title="Recipe Title", min_length=1)  # 레시피 제목 (최소 1글자 이상)
    ingredients: List[str] = Field(..., title="Ingredients", min_items=1)  # 재료 목록 (최소 1개 필요)
    url: str = Field(..., title="YouTube URL", pattern="https?://[^\s]+")  # 유효한 유튜브 URL 형식 검증

    class Settings:
        collection = "recipes"  # MongoDB에서 사용할 컬렉션 이름

# API 요청 데이터를 검증할 때 사용하는 모델
class RecipeCreate(BaseModel):
    title: str = Field(..., title="Recipe Title", min_length=1)  # 레시피 제목 (최소 1글자 이상)
    ingredients: List[str] = Field(..., title="Ingredients", min_items=1)  # 재료 목록 (최소 1개 필요)
    url: str = Field(..., title="YouTube URL", pattern="https?://[^\s]+")  # 유효한 유튜브 URL 형식 검증

    class Config:
        schema_extra = {
            "example": {  # API 문서에서 예제로 표시될 데이터
                "title": "Delicious Pasta",
                "ingredients": ["Pasta", "Tomato Sauce", "Cheese"],
                "url": "https://www.youtube.com/watch?v=abcd1234"
            }
        }
