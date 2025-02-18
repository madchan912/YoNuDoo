@echo off
echo [🔄] MongoDB 데이터 복원 중...

:: 컨테이너 내부에 /restore 폴더 생성
docker exec -it yonudoo-mongo mkdir -p /restore/YoNuDoo

:: 백업 데이터 복사
docker cp mongo_backup/YoNuDoo yonudoo-mongo:/restore/YoNuDoo

:: 데이터 복원
docker exec -it yonudoo-mongo mongorestore --username root --password 1234 --authenticationDatabase admin --dir /restore/YoNuDoo

echo [✅] 데이터 복원 완료!
