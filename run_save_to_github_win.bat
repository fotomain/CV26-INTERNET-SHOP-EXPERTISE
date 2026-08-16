@echo off
setlocal enabledelayedexpansion

REM ==============================================================================
REM Script: run_save_to_github_win.bat
REM Purpose: Saves codebase to GitHub on a new branch named ok_YY-MM-DD-HH-MM
REM Excludes: dataset_start/
REM Remote: https://github.com/fotomain/CV26-INTERNET-SHOP-EXPERTISE.git
REM ==============================================================================

cd /d "%~dp0"

set REMOTE_URL=https://github.com/fotomain/CV26-INTERNET-SHOP-EXPERTISE.git

echo ================================================================================
echo ^>^>^> [1/5] Checking Git Repository ^& Remote Configuration...
echo ================================================================================

if not exist ".git" (
    echo Initializing new Git repository...
    git init
    if errorlevel 1 goto :error
)

if not exist ".gitignore" (
    echo Creating .gitignore to exclude dataset_start/...
    (
        echo # Exclude raw start dataset
        echo dataset_start/
        echo dataset_start/*
        echo .venv/
        echo __pycache__/
        echo .DS_Store
    ) > .gitignore
)

REM Configure remote origin
git remote | findstr /R "^origin$" >nul
if errorlevel 1 (
    echo Adding remote 'origin' -^> %REMOTE_URL%...
    git remote add origin %REMOTE_URL%
) else (
    echo Updating remote 'origin' to %REMOTE_URL%...
    git remote set-url origin %REMOTE_URL%
)

echo.
echo ================================================================================
echo ^>^>^> [2/5] Creating New Branch: ok_YY-MM-DD-HH-MM...
echo ================================================================================

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format 'yy-MM-dd-HH-mm'"') do set TIMESTAMP=%%i
set BRANCH_NAME=ok_%TIMESTAMP%
echo New branch name: %BRANCH_NAME%

git checkout -b %BRANCH_NAME%
if errorlevel 1 goto :error

echo.
echo ================================================================================
echo ^>^>^> [3/5] Staging Project Files (excluding dataset_start/)...
echo ================================================================================

git add .
if errorlevel 1 goto :error

echo.
echo ================================================================================
echo ^>^>^> [4/5] Committing Changes...
echo ================================================================================

git commit -m "Auto save: %BRANCH_NAME%"
if errorlevel 1 (
    echo Creating empty commit tag...
    git commit --allow-empty -m "Auto save: %BRANCH_NAME%"
)

echo.
echo ================================================================================
echo ^>^>^> [5/5] Pushing to GitHub (origin/%BRANCH_NAME%)...
echo ================================================================================

git push -u origin %BRANCH_NAME%
if errorlevel 1 (
    echo [WARNING] git push failed. Please verify internet connection and GitHub authentication.
    goto :error
)

echo.
echo ================================================================================
echo [SUCCESS] Successfully saved and pushed to GitHub!
echo   - Repository : %REMOTE_URL%
echo   - Branch     : %BRANCH_NAME%
echo ================================================================================
goto :eof

:error
echo.
echo [ERROR] Failed to save project to GitHub.
exit /b 1
