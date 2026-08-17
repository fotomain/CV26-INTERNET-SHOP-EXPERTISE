@echo off
REM ==============================================================================
REM Full Pipeline Execution Runner for Windows
REM Runs all calculation steps from Mission 1 to Mission 5 sequentially
REM Displays output to screen and saves it into run_log.txt
REM ==============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

set "LOG_FILE=run_log.txt"

if "%~1"=="--inner-run" goto :run_pipeline

echo ================================================================================
echo    E-COMMERCE PRODUCT CATALOG EXPERTISE ^& DSS PIPELINE (Windows)
echo ================================================================================
echo Starting full pipeline execution...
echo Output will be displayed on screen and saved to: %LOG_FILE%
echo.

REM Run via PowerShell Tee-Object to display on console and record in run_log.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { & cmd.exe /c '\"\"%~f0\"\" --inner-run' } 2>&1 | Tee-Object -FilePath '%LOG_FILE%'"
exit /b %ERRORLEVEL%

:run_pipeline
REM Identify Python executable
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXEC=.venv\Scripts\python.exe"
) else if defined VIRTUAL_ENV (
    set "PYTHON_EXEC=python.exe"
) else (
    set "PYTHON_EXEC=python.exe"
)

echo ================================================================================
echo    E-COMMERCE PRODUCT CATALOG EXPERTISE ^& DSS PIPELINE (Windows)
echo ================================================================================
echo Using Python: !PYTHON_EXEC!
echo.

REM ------------------------------------------------------------------------------
REM STEP 1: Mission 1 - Product Ingestion, Classification & EDA (step1_eda)
REM ------------------------------------------------------------------------------
echo ^>^>^> [1/7] Running Mission 1: Product Ingestion ^& Fashion-MNIST Classification...
!PYTHON_EXEC! step1_eda\process_products.py
if errorlevel 1 goto :error

REM ------------------------------------------------------------------------------
REM STEP 2: Mission 2 - Sales Readiness Evaluation (step2_eda)
REM ------------------------------------------------------------------------------
echo.
echo ^>^>^> [2/7] Running Mission 2: Sales Readiness (ready_to_sale) Check...
!PYTHON_EXEC! step2_eda\process_ready_to_sale.py
if errorlevel 1 goto :error

REM ------------------------------------------------------------------------------
REM STEP 3: Mission 3 - Palette Extraction & Benchmarking (step3_eda)
REM ------------------------------------------------------------------------------
echo.
echo ^>^>^> [3/7] Running Mission 3: Image Palette Extraction ^& Structuring...
!PYTHON_EXEC! step3_eda\extract_palette.py
if errorlevel 1 goto :error

echo.
echo ^>^>^> [4/7] Running Mission 3: Timing Benchmarks ^& 10k/1M Scaling Prognosis...
!PYTHON_EXEC! step3_eda\timing_and_prognosis.py
if errorlevel 1 goto :error

REM ------------------------------------------------------------------------------
REM STEP 4: Mission 4 - Learn Target Market Preferences (step4_learn)
REM ------------------------------------------------------------------------------
echo.
echo ^>^>^> [5/7] Running Mission 4: YOLO + OpenCV Exclusions ^& Market Model Training...
!PYTHON_EXEC! step4_learn\train_marketing_model.py
if errorlevel 1 goto :error

REM ------------------------------------------------------------------------------
REM STEP 5: Mission 5 - Decision Support System & Reporting (step5_dss)
REM ------------------------------------------------------------------------------
echo.
echo ^>^>^> [6/7] Running Mission 5: DSS Marketing Decision Engine...
!PYTHON_EXEC! step5_dss\dss_decision_engine.py
if errorlevel 1 goto :error
!PYTHON_EXEC! step5_dss\dss_analysis.py
if errorlevel 1 goto :error

REM ------------------------------------------------------------------------------
REM STEP 6: Capstone Executive Report & Architecture HTML Generation
REM ------------------------------------------------------------------------------
echo.
echo ^>^>^> [7/7] Generating Executive Web Report (CAPSTONE_REPORT.html ^& HOW_IT_WORKS.html)...
!PYTHON_EXEC! build_capstone_report.py
if errorlevel 1 goto :error
!PYTHON_EXEC! build_how_it_works_html.py
if errorlevel 1 goto :error

echo.
echo ================================================================================
echo [SUCCESS] ALL PIPELINE CALCULATIONS COMPLETED SUCCESSFULLY!
echo   - Mission 1 Outputs: step1_eda\result1.csv, step1_eda\result_categories.csv
echo   - Mission 2 Output : step1_eda\result2.csv (ready_to_sale)
echo   - Mission 3 Outputs: step1_eda\result3.csv, step3_eda\result3_nb.ipynb
echo   - Mission 3 Logs   : duration\duration_log.md, prognose\prognose_time.md
echo   - Mission 4 Outputs: step4_learn\market_model.pkl, step4_learn\market_profile.json
echo                        step4_learn\result4_ml_log.json
echo   - Mission 5 Outputs: step5_dss\result5.csv
echo                        step5_dss\result_good_for_new_marketing.csv
echo                        step5_dss\result_not_good_for_new_marketing.csv
echo                        step5_dss\dss_summary_report.md
echo   - Web Report       : CAPSTONE_REPORT.html
echo   - Web Logic Guide  : HOW_IT_WORKS.html
echo   - Architecture Doc : HOW_IT_WORKS.md
echo   - Pipeline Log     : run_log.txt
echo ================================================================================
goto :eof

:error
echo.
echo [ERROR] Pipeline execution failed at one of the steps.
exit /b 1
