@echo off
echo [🔄] MongoDB 데이터 복원 중...
docker cp mongo_backup/YoNuDoo yonudoo-mongo:/restore/YoNuDoo
docker exec -it yonudoo-mongo mongorestore --username root --password 1234 --authenticationDatabase admin --dir /restore/YoNuDoo
echo [✅] 데이터 복원 완료!
