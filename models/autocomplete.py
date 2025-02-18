from beanie import Document
from typing import List
from pydantic import BaseModel, Field

# 자동완성 데이터를 위한 MongoDB 모델
class AutoComplete(Document):
    ingredient: str = Field(..., title="Ingredient", min_length=1)  # 빈 값 방지
    search_keywords: List[str] = Field(..., title="Search Keywords", min_items=1)  # 최소 1개 키워드 필요

    class Settings:
        collection = "autocomplete"  # MongoDB에서 사용할 컬렉션 이름

# API 요청 데이터를 검증할 때 사용하는 모델
class AutoCompleteCreate(BaseModel):
    ingredient: str = Field(..., title="Ingredient", min_length=1)  # 빈 값 방지
    search_keywords: List[str] = Field(..., title="Search Keywords", min_items=1)  # 최소 1개 키워드 필요

    class Config:
        schema_extra = {
            "example": {  # API 문서에서 예제로 표시될 데이터
                "ingredient": "Tomato",
                "search_keywords": ["tom", "tomato", "토마토"]
            }
        }
