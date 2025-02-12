import motor.motor_asyncio
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MongoDB 연결 정보 가져오기
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# MongoDB 클라이언트 생성
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]  # 사용할 데이터베이스 선택
