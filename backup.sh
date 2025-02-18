#!/bin/bash
echo "[🔄] 기존 백업 삭제 중..."
rm -rf mongo_backup
echo "[✅] 기존 백업 삭제 완료."

echo "[🔄] MongoDB 데이터 백업 중..."
docker exec -it yonudoo-mongo mongodump --username root --password 1234 --authenticationDatabase admin --db YoNuDoo --out /backup
docker cp yonudoo-mongo:/backup ./mongo_backup
echo "[✅] 백업 완료! 데이터가 'mongo_backup' 폴더에 저장됨."
