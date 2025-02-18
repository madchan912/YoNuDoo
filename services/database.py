import motor.motor_asyncio
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 설정 (기본값 추가)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:1234@mongo:27017/YoNuDoo?authSource=admin")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "YoNuDoo")

# MongoDB 클라이언트 설정
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]
