@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXEC=.venv\Scripts\python.exe"
) else if defined VIRTUAL_ENV (
    set "PYTHON_EXEC=python.exe"
) else (
    set "PYTHON_EXEC=python.exe"
)

echo ================================================================================
echo    STARTING CV26 STEP 82 BACKEND (FastAPI + Supabase Sync)
echo ================================================================================
%PYTHON_EXEC% -m uvicorn step82_backend_exec.main:app --host 0.0.0.0 --port 8000 --reload
