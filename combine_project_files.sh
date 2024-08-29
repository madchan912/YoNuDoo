#!/bin/bash

# 프로젝트 디렉토리 설정
PROJECT_DIR="/Users/your_username/Cook/YoNuDoo"
OUTPUT_FILE="$PROJECT_DIR/combined_project_files.txt"

# 기존 파일 삭제
if [ -f "$OUTPUT_FILE" ]; then
    rm "$OUTPUT_FILE"
fi

# 파일 결합 시작
echo ".py 파일 및 templates, static 폴더에 있는 파일을 결합합니다..."

# 전체 파일 처리 카운터 초기화
count=0

# C:\Cook\YoNuDoo 디렉토리의 .py 파일을 처리
for file in "$PROJECT_DIR"/*.py; do
    ((count++))
    echo "Processing file $file ($count files processed)"
    echo "File: $file" >> "$OUTPUT_FILE"
    echo "--------" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "--------" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

# templates 폴더의 모든 파일을 처리
for file in "$PROJECT_DIR/templates"/*; do
    if [ -f "$file" ]; then
        ((count++))
        echo "Processing file $file ($count files processed)"
        echo "File: $file" >> "$OUTPUT_FILE"
        echo "--------" >> "$OUTPUT_FILE"
        cat "$file" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "--------" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

# static 폴더의 모든 파일을 처리
for file in "$PROJECT_DIR/static"/*; do
    if [ -f "$file" ]; then
        ((count++))
        echo "Processing file $file ($count files processed)"
        echo "File: $file" >> "$OUTPUT_FILE"
        echo "--------" >> "$OUTPUT_FILE"
        cat "$file" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "--------" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

echo ""
echo ".py 파일 및 templates, static 폴더에 있는 파일이 $OUTPUT_FILE 에 결합되었습니다."
echo "총 $count개의 파일이 처리되었습니다."

# 작업 완료 메시지
echo ""
echo "작업이 완료되었습니다."
