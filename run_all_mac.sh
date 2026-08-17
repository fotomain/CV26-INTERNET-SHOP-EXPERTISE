#!/usr/bin/env bash
set -e
set -o pipefail

# ==============================================================================
# Full Pipeline Execution Runner for macOS / Linux
# Runs all calculation steps from Mission 1 to Mission 5 sequentially
# Displays real-time output to the screen and saves it to run_log.txt
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

LOG_FILE="run_log.txt"

# If not running as the inner pipeline, tee all output to the screen and run_log.txt
if [ "$1" != "--inner-run" ]; then
    echo "================================================================================"
    echo "    E-COMMERCE PRODUCT CATALOG EXPERTISE & DSS PIPELINE (macOS / Linux)        "
    echo "================================================================================"
    echo "Starting full pipeline execution..."
    echo "Output will be displayed on screen and saved to: $LOG_FILE"
    echo ""
    "$0" --inner-run 2>&1 | tee "$LOG_FILE"
    exit "${PIPESTATUS[0]}"
fi

echo "================================================================================"
echo "    E-COMMERCE PRODUCT CATALOG EXPERTISE & DSS PIPELINE (macOS / Linux)        "
echo "================================================================================"

# Identify Python executable (prefer virtual environment)
if [ -f ".venv/bin/python" ]; then
    PYTHON_EXEC=".venv/bin/python"
elif [ -n "$VIRTUAL_ENV" ]; then
    PYTHON_EXEC="python"
else
    PYTHON_EXEC="python3"
fi

echo "Using Python: $PYTHON_EXEC"
echo ""

# ------------------------------------------------------------------------------
# STEP 1: Mission 1 - Product Ingestion, Classification & EDA (step1_eda)
# ------------------------------------------------------------------------------
echo ">>> [1/7] Running Mission 1: Product Ingestion & Fashion-MNIST Classification..."
"$PYTHON_EXEC" step1_eda/process_products.py

# ------------------------------------------------------------------------------
# STEP 2: Mission 2 - Sales Readiness Evaluation (step2_eda)
# ------------------------------------------------------------------------------
echo ""
echo ">>> [2/7] Running Mission 2: Sales Readiness (ready_to_sale) Check..."
"$PYTHON_EXEC" step2_eda/process_ready_to_sale.py

# ------------------------------------------------------------------------------
# STEP 3: Mission 3 - Palette Extraction & Benchmarking (step3_eda)
# ------------------------------------------------------------------------------
echo ""
echo ">>> [3/7] Running Mission 3: Image Palette Extraction & Structuring..."
"$PYTHON_EXEC" step3_eda/extract_palette.py

echo ""
echo ">>> [4/7] Running Mission 3: Timing Benchmarks & 10k/1M Scaling Prognosis..."
"$PYTHON_EXEC" step3_eda/timing_and_prognosis.py

# ------------------------------------------------------------------------------
# STEP 4: Mission 4 - Learn Target Market Preferences (step4_learn)
# ------------------------------------------------------------------------------
echo ""
echo ">>> [5/7] Running Mission 4: YOLO + OpenCV Exclusions & Market Model Training..."
"$PYTHON_EXEC" step4_learn/train_marketing_model.py

# ------------------------------------------------------------------------------
# STEP 5: Mission 5 - Decision Support System & Reporting (step5_dss)
# ------------------------------------------------------------------------------
echo ""
echo ">>> [6/7] Running Mission 5: DSS Marketing Decision Engine..."
"$PYTHON_EXEC" step5_dss/dss_decision_engine.py
"$PYTHON_EXEC" step5_dss/dss_analysis.py

# ------------------------------------------------------------------------------
# STEP 6: Capstone Executive Report & Architecture HTML Generation
# ------------------------------------------------------------------------------
echo ""
echo ">>> [7/7] Generating Executive Web Report (CAPSTONE_REPORT.html & HOW_IT_WORKS.html)..."
"$PYTHON_EXEC" build_capstone_report.py
"$PYTHON_EXEC" build_how_it_works_html.py

echo ""
echo "================================================================================"
echo "✓ ALL PIPELINE CALCULATIONS COMPLETED SUCCESSFULLY!"
echo "  - Mission 1 Outputs: step1_eda/result1.csv, step1_eda/result_categories.csv"
echo "  - Mission 2 Output : step1_eda/result2.csv (ready_to_sale)"
echo "  - Mission 3 Outputs: step1_eda/result3.csv, step3_eda/result3_nb.ipynb"
echo "  - Mission 3 Logs   : duration/duration_log.md, prognose/prognose_time.md"
echo "  - Mission 4 Outputs: step4_learn/market_model.pkl, step4_learn/market_profile.json"
echo "                       step4_learn/result4_ml_log.json"
echo "  - Mission 5 Outputs: step5_dss/result5.csv"
echo "                       step5_dss/result_good_for_new_marketing.csv"
echo "                       step5_dss/result_not_good_for_new_marketing.csv"
echo "                       step5_dss/dss_summary_report.md"
echo "  - Web Report       : CAPSTONE_REPORT.html"
echo "  - Web Logic Guide  : HOW_IT_WORKS.html"
echo "  - Architecture Doc : HOW_IT_WORKS.md"
echo "  - Pipeline Log     : run_log.txt"
echo "================================================================================"
