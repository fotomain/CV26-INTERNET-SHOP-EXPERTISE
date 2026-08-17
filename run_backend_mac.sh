#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".venv/bin/python" ]; then
    PYTHON_EXEC=".venv/bin/python"
elif [ -n "$VIRTUAL_ENV" ]; then
    PYTHON_EXEC="python"
else
    PYTHON_EXEC="python3"
fi

echo "================================================================================"
echo "    STARTING CV26 STEP 82 BACKEND (FastAPI + Supabase Sync)                      "
echo "================================================================================"
"$PYTHON_EXEC" -m uvicorn step82_backend_exec.main:app --host 0.0.0.0 --port 8000 --reload
