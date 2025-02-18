@echo off
setlocal enabledelayedexpansion

:: 작업할 디렉토리 설정 (바탕화면/YoNuDoo)
set TARGET_DIR=%USERPROFILE%\Desktop\YoNuDoo

:: 저장할 txt 파일 경로 설정
set OUTPUT_FILE=%TARGET_DIR%\YoNuDoo_source.txt

:: 기존 파일이 있으면 삭제
if exist "%OUTPUT_FILE%" (
    del "%OUTPUT_FILE%"
)

:: 빈 파일 생성
echo. > "%OUTPUT_FILE%"

:: 특정 파일을 기록하는 함수
call :append_file_content "%TARGET_DIR%\main.py"
call :append_file_content "%TARGET_DIR%\requirements.txt"
call :append_file_content "%TARGET_DIR%\docker-compose.yml"
call :append_file_content "%TARGET_DIR%\Dockerfile"
call :append_file_content "%TARGET_DIR%\.env"

:: 모든 .py 파일들 중 __init__.py 제외하고 .venv와 .git 폴더 제외하며 소스 내용을 output 파일에 저장
for /r "%TARGET_DIR%" %%f in (*.py) do (
    set "filepath=%%f"
    if /i "%%~nxf" neq "__init__.py" (
        echo !filepath! | findstr /i /c:".venv" /c:"\.git" > nul
        if !errorlevel! neq 0 (
            call :append_file_content "%%f"
        )
    )
)

:: 모든 .css 파일들 소스 내용 추가, .venv, .git 폴더 제외
for /r "%TARGET_DIR%" %%f in (*.css) do (
    set "filepath=%%f"
    echo !filepath! | findstr /i /c:".venv" /c:"\.git" > nul
    if !errorlevel! neq 0 (
        call :append_file_content "%%f"
    )
)

:: 모든 .html 파일들 소스 내용 추가, .venv, .git 폴더 제외
for /r "%TARGET_DIR%" %%f in (*.html) do (
    set "filepath=%%f"
    echo !filepath! | findstr /i /c:".venv" /c:"\.git" > nul
    if !errorlevel! neq 0 (
        call :append_file_content "%%f"
    )
)

:: 모든 .js 파일들 소스 내용 추가, .venv, .git 폴더 제외
for /r "%TARGET_DIR%" %%f in (*.js) do (
    set "filepath=%%f"
    echo !filepath! | findstr /i /c:".venv" /c:"\.git" > nul
    if !errorlevel! neq 0 (
        call :append_file_content "%%f"
    )
)

echo 작업이 완료되었습니다.
goto :EOF

:: 파일 내용을 output 파일에 추가하는 함수
:append_file_content
if exist "%~1" (
    echo. >> "%OUTPUT_FILE%"
    echo === [FILE]: %1 === >> "%OUTPUT_FILE%"
    type "%1" >> "%OUTPUT_FILE%"
    echo. >> "%OUTPUT_FILE%"
)
goto :EOF