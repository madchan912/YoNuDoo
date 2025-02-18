#!/bin/bash

# 작업할 디렉토리 설정
TARGET_DIR="/Users/madchan/YoNuDoo"

# 저장할 txt 파일 경로 설정
OUTPUT_FILE="$TARGET_DIR/YoNuDoo_source.txt"

# 기존 파일이 있으면 삭제
if [ -f "$OUTPUT_FILE" ]; then
  rm "$OUTPUT_FILE"
fi

# 빈 파일 생성 (UTF-8 변환 과정 제거)
touch "$OUTPUT_FILE"

# 특정 파일을 기록하는 함수
append_file_content() {
  local file_path="$1"
  echo -e "\n=== [FILE]: $file_path ===\n" >> "$OUTPUT_FILE"  # 파일명 기록
  cat "$file_path" >> "$OUTPUT_FILE"  # 파일 내용 추가
  echo -e "\n" >> "$OUTPUT_FILE"  # 파일 간 구분을 위한 줄바꿈
}

# .py 파일들 중 __init__.py 제외하고 venv 폴더 제외하며 소스 내용을 output 파일에 저장
find "$TARGET_DIR" -type f -name "*.py" ! -name "__init__.py" ! -path "$TARGET_DIR/venv/*" -print | while read file; do
  append_file_content "$file"
done

# static 폴더 내의 css, js 파일들 소스 내용 추가, venv 제외
find "$TARGET_DIR/static" -type f \( -name "*.css" -o -name "*.js" \) ! -path "$TARGET_DIR/venv/*" -print | while read file; do
  append_file_content "$file"
done

# templates 폴더 내의 html 파일들 소스 내용 추가, venv 제외
find "$TARGET_DIR/templates" -type f -name "*.html" ! -path "$TARGET_DIR/venv/*" -print | while read file; do
  append_file_content "$file"
done

# 메인 디렉토리 내의 특정 파일들 내용 추가
for file in .env docker-compose.yml Dockerfile main.py requirements.txt; do
  if [ -f "$TARGET_DIR/$file" ]; then
    append_file_content "$TARGET_DIR/$file"
  fi
done