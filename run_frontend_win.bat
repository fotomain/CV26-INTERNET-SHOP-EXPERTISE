@echo off
setlocal
cd /d "%~dp0\step81_frontend_input"

echo ================================================================================
echo    STARTING CV26 STEP 81 FRONTEND (React + TypeScript + Tamagui + Saga)
echo ================================================================================
npm run dev -- --host
