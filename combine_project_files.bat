@echo off
setlocal enabledelayedexpansion

REM 프로젝트 디렉토리 설정
set PROJECT_DIR=C:\Cook\YoNuDoo
set OUTPUT_FILE=combined_project_files.txt

REM 기존 파일 삭제
if exist %OUTPUT_FILE% del %OUTPUT_FILE%

REM 파일 결합 시작
echo .py 파일 및 templates, static 폴더에 있는 파일을 결합합니다...

REM 전체 파일 처리 카운터 초기화
set /a count=0

REM C:\Cook\YoNuDoo 디렉토리의 .py 파일을 처리
for %%f in (%PROJECT_DIR%\*.py) do (
    set /a count+=1
    echo Processing file %%f (^%count^% files processed^)
    echo File: %%f >> %OUTPUT_FILE%
    echo -------- >> %OUTPUT_FILE%
    type "%%f" >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
    echo -------- >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
)

REM templates 폴더의 모든 파일을 처리
for /r "%PROJECT_DIR%\templates" %%f in (*) do (
    set /a count+=1
    echo Processing file %%f (^%count^% files processed^)
    echo File: %%f >> %OUTPUT_FILE%
    echo -------- >> %OUTPUT_FILE%
    type "%%f" >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
    echo -------- >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
)

REM static 폴더의 모든 파일을 처리
for /r "%PROJECT_DIR%\static" %%f in (*) do (
    set /a count+=1
    echo Processing file %%f (^%count^% files processed^)
    echo File: %%f >> %OUTPUT_FILE%
    echo -------- >> %OUTPUT_FILE%
    type "%%f" >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
    echo -------- >> %OUTPUT_FILE%
    echo. >> %OUTPUT_FILE%
)

echo.
echo .py 파일 및 templates, static 폴더에 있는 파일이 %OUTPUT_FILE% 에 결합되었습니다.
echo 총 %count%개의 파일이 처리되었습니다.

REM 작업 완료 후 사용자 입력을 기다림
echo.
echo 작업이 완료되었습니다. 아무 키나 눌러 종료하세요...
pause
