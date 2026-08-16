@echo off
REM Opens CAPSTONE_REPORT.html or HOW_IT_WORKS.html in default browser on Windows
cd /d "%~dp0"
set TARGET_FILE=%~1
if "%TARGET_FILE%"=="" set TARGET_FILE=CAPSTONE_REPORT.html
echo Opening %TARGET_FILE%...
start "" "%TARGET_FILE%"
