"""
FastAPI Server for Asynchronous ML Pipeline Execution (Mission 1-5).
Supports custom_dataset_start, custom_country_images_man, and custom_country_images_woman.
"""

import os
import sys
import json
import logging
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

# Ensure root directory is on sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from step82_backend_exec.image_preprocessor import (
    validate_and_save_image,
    ImageValidationError,
    MAX_FILE_SIZE_BYTES
)
from step82_backend_exec.supabase_service import (
    update_progress,
    get_progress,
    get_results,
    upsert_user_session,
    log_error
)
from step82_backend_exec.pipeline_orchestrator import run_custom_ml_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("cv26_fastapi")

app = FastAPI(
    title="CV26 DSS Marketing Intelligence & Catalog ML Engine",
    version="5.0.0",
    description="Asynchronous ML Execution Server for Catalog Classification & Demographic Matching"
)

# Configure fully permissive CORS for all origins, headers, and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)

CUSTOM_DATA_ROOT = os.path.join(BASE_DIR, "custom_data")
os.makedirs(CUSTOM_DATA_ROOT, exist_ok=True)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "CV26 DSS Backend Execution Server",
        "version": "5.0.0",
        "supportedEndpoints": [
            "GET /api/health",
            "GET /api/progress/{userSessionGUID}",
            "GET /api/results/{userSessionGUID}",
            "POST /api/execute-ml"
        ]
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": os.getenv("APP_TIME", "2026-08-17")}

@app.get("/api/progress/{userSessionGUID}")
def get_progress_endpoint(userSessionGUID: str):
    progress = get_progress(userSessionGUID)
    return {
        "userSessionGUID": userSessionGUID,
        "progress": progress
    }

@app.get("/api/results/{userSessionGUID}")
def get_results_endpoint(userSessionGUID: str):
    results = get_results(userSessionGUID)
    if not results:
        return {"userSessionGUID": userSessionGUID, "status": "pending", "results": None}
    return {
        "userSessionGUID": userSessionGUID,
        "status": "completed",
        "results": results
    }

@app.get("/api/download/{userSessionGUID}/{filename}")
def download_session_file(userSessionGUID: str, filename: str):
    """
    Downloads generated CSV or JSON results for a userSessionGUID.
    Supports result_good_for_new_marketing.csv, result_not_good_for_new_marketing.csv, etc.
    """
    safe_name = os.path.basename(filename)
    session_dir = os.path.join(CUSTOM_DATA_ROOT, userSessionGUID)
    os.makedirs(session_dir, exist_ok=True)
    session_file = os.path.join(session_dir, safe_name)

    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Expose-Headers": "Content-Disposition, Content-Type",
    }

    if os.path.exists(session_file) and os.path.getsize(session_file) > 0:
        return FileResponse(
            path=session_file,
            filename=safe_name,
            media_type="text/csv" if safe_name.endswith(".csv") else "application/json",
            headers=cors_headers
        )

    # Fallback to step5_dss default file if applicable
    step5_fallback = os.path.join(BASE_DIR, 'step5_dss', safe_name)
    if os.path.exists(step5_fallback) and os.path.getsize(step5_fallback) > 0:
        return FileResponse(
            path=step5_fallback,
            filename=safe_name,
            media_type="text/csv" if safe_name.endswith(".csv") else "application/json",
            headers=cors_headers
        )

    # If CSV was requested but empty/not yet written, generate clean empty CSV response
    if safe_name.endswith(".csv"):
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write("item_id,name,category_name,ready_to_sale,product_is_good_for_new_marketing,market_compatibility_score,market_palette_match_distance\n")
        return FileResponse(
            path=session_file,
            filename=safe_name,
            media_type="text/csv",
            headers=cors_headers
        )

    return JSONResponse(
        status_code=404,
        content={"detail": f"File '{safe_name}' not found for session '{userSessionGUID}'."},
        headers=cors_headers
    )

def clear_subfolder_contents(folder_path: str):
    """
    Clears all files and directories inside folder_path.
    """
    if os.path.exists(folder_path):
        import shutil
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                logger.warning(f"Failed to delete {item_path}: {e}")

@app.post("/api/clear-session/{userSessionGUID}")
@app.delete("/api/clear-session/{userSessionGUID}")
def clear_session_endpoint(userSessionGUID: str):
    """
    Explicitly deletes subfolder custom_data/<userSessionGUID> before running new ML steps.
    """
    session_dir = os.path.join(CUSTOM_DATA_ROOT, userSessionGUID)
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }
    if os.path.exists(session_dir):
        import shutil
        shutil.rmtree(session_dir, ignore_errors=True)
        logger.info(f"Deleted subfolder: custom_data/{userSessionGUID}")
        return JSONResponse(content={"status": "ok", "message": f"Deleted subfolder custom_data/{userSessionGUID}"}, headers=cors_headers)
    return JSONResponse(content={"status": "ok", "message": f"Subfolder custom_data/{userSessionGUID} was not present"}, headers=cors_headers)

@app.post("/api/upload-batch")
async def upload_batch(
    userSessionGUID: str = Form(...),
    targetType: str = Form(...),  # "dataset", "man", "woman"
    batchIndex: int = Form(...),  # 1-indexed
    totalBatches: int = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Receives a chunk/batch of files (FILES_PER_1_BATCH=10), sanitizes & auto-optimizes,
    and updates batch ingestion progress.
    """
    session_dir = os.path.join(CUSTOM_DATA_ROOT, userSessionGUID)

    # Delete subfolder custom_data/+userSessionGUID before starting Batch 1 of a new run
    if batchIndex == 1 and targetType == "dataset":
        if os.path.exists(session_dir):
            import shutil
            shutil.rmtree(session_dir, ignore_errors=True)
            logger.info(f"Deleted subfolder custom_data/{userSessionGUID} before new ML run (Batch 1)")
        os.makedirs(session_dir, exist_ok=True)

    if targetType == "dataset":
        target_dir = os.path.join(session_dir, "custom_dataset_start")
    elif targetType == "man":
        target_dir = os.path.join(session_dir, "custom_country_images", "man")
    elif targetType == "woman":
        target_dir = os.path.join(session_dir, "custom_country_images", "woman")
    else:
        target_dir = os.path.join(session_dir, "custom_dataset_start")

    os.makedirs(target_dir, exist_ok=True)

    saved_files = []

    for uf in files:
        if not uf.filename:
            continue
        try:
            content = await uf.read()
            out_p = validate_and_save_image(content, uf.filename, target_dir)
            saved_files.append(out_p)
        except Exception as e:
            logger.warning(f"Error saving batch file '{uf.filename}': {e}")
            log_error(userSessionGUID, str(e), error_type="Warning", details={"filename": uf.filename})

    # Calculate upload progress (0% - 15% reserved for upload stage)
    upload_pct = max(1, min(15, int((batchIndex / max(1, totalBatches)) * 15)))
    batch_detail = f"Batch Progress: Uploaded batch {batchIndex}/{totalBatches} ({targetType.upper()} - {len(saved_files)} files)"
    
    update_progress(
        userSessionGUID,
        percent=upload_pct,
        step_id=0,
        step_name="Batch Ingestion Active",
        details=batch_detail
    )
    logger.info(f"Session {userSessionGUID}: {batch_detail}")

    return {
        "status": "ok",
        "userSessionGUID": userSessionGUID,
        "batchIndex": batchIndex,
        "totalBatches": totalBatches,
        "targetType": targetType,
        "savedCount": len(saved_files),
        "uploadPercent": upload_pct
    }

@app.post("/api/execute-ml")
async def execute_ml(
    background_tasks: BackgroundTasks,
    userSessionGUID: str = Form(...),
    custom_country_name: str = Form("United States"),
    custom_dataset_start: Optional[List[UploadFile]] = File(None),
    custom_country_images_man: Optional[List[UploadFile]] = File(None),
    custom_country_images_woman: Optional[List[UploadFile]] = File(None),
    custom_country_images: Optional[List[UploadFile]] = File(None)  # backward compatibility
):
    """
    Receives custom candidate catalog and target country lookbook photos (men & women),
    validates format and size limits, stores in custom_data/<userSessionGUID>/,
    and triggers asynchronous ML pipeline.
    """
    logger.info(f"Received ML execution request for userSessionGUID='{userSessionGUID}', country='{custom_country_name}'")

    if not userSessionGUID or len(userSessionGUID.strip()) < 5:
        raise HTTPException(status_code=400, detail="Invalid userSessionGUID provided.")

    # Create session folder hierarchy
    session_dir = os.path.join(CUSTOM_DATA_ROOT, userSessionGUID)
    dataset_start_dir = os.path.join(session_dir, "custom_dataset_start")
    country_images_dir = os.path.join(session_dir, "custom_country_images")
    country_man_dir = os.path.join(country_images_dir, "man")
    country_woman_dir = os.path.join(country_images_dir, "woman")

    # Delete subfolder custom_data/<userSessionGUID> before saving direct execute-ml multipart files if provided
    if custom_dataset_start or custom_country_images_man or custom_country_images_woman:
        if os.path.exists(session_dir):
            import shutil
            shutil.rmtree(session_dir, ignore_errors=True)
            logger.info(f"Deleted subfolder custom_data/{userSessionGUID} before direct execution.")

    os.makedirs(session_dir, exist_ok=True)
    os.makedirs(dataset_start_dir, exist_ok=True)
    os.makedirs(country_images_dir, exist_ok=True)
    os.makedirs(country_man_dir, exist_ok=True)
    os.makedirs(country_woman_dir, exist_ok=True)

    # Save country name metadata
    country_meta_path = os.path.join(session_dir, "custom_country_name.json")
    with open(country_meta_path, 'w', encoding='utf-8') as f:
        json.dump({"custom_country_name": custom_country_name, "userSessionGUID": userSessionGUID}, f, indent=2)

    saved_dataset_files = []
    saved_man_files = []
    saved_woman_files = []

    # Process and sanitize candidate catalog files
    if custom_dataset_start:
        for uf in custom_dataset_start:
            if not uf.filename:
                continue
            try:
                content = await uf.read()
                out_path = validate_and_save_image(content, uf.filename, dataset_start_dir)
                saved_dataset_files.append(out_path)
            except Exception as ve:
                logger.warning(f"Warning ingesting catalog file '{uf.filename}': {ve}")
                log_error(userSessionGUID, str(ve), error_type="Warning", details={"filename": uf.filename})

    # Process and sanitize Men lookbook photos
    if custom_country_images_man:
        for uf in custom_country_images_man:
            if not uf.filename:
                continue
            try:
                content = await uf.read()
                out_path = validate_and_save_image(content, uf.filename, country_man_dir)
                saved_man_files.append(out_path)
            except Exception as ve:
                logger.warning(f"Warning ingesting man lookbook file '{uf.filename}': {ve}")
                log_error(userSessionGUID, str(ve), error_type="Warning", details={"filename": uf.filename})

    # Process and sanitize Women lookbook photos
    if custom_country_images_woman:
        for uf in custom_country_images_woman:
            if not uf.filename:
                continue
            try:
                content = await uf.read()
                out_path = validate_and_save_image(content, uf.filename, country_woman_dir)
                saved_woman_files.append(out_path)
            except Exception as ve:
                logger.warning(f"Warning ingesting woman lookbook file '{uf.filename}': {ve}")
                log_error(userSessionGUID, str(ve), error_type="Warning", details={"filename": uf.filename})

    # Backward compatibility for legacy custom_country_images
    if custom_country_images and not (saved_man_files or saved_woman_files):
        for idx, uf in enumerate(custom_country_images):
            if not uf.filename:
                continue
            try:
                content = await uf.read()
                target_sub = country_man_dir if idx % 2 == 0 else country_woman_dir
                out_path = validate_and_save_image(content, uf.filename, target_sub)
                if idx % 2 == 0:
                    saved_man_files.append(out_path)
                else:
                    saved_woman_files.append(out_path)
            except Exception as ve:
                logger.warning(f"Warning ingesting lookbook file '{uf.filename}': {ve}")
                log_error(userSessionGUID, str(ve), error_type="Warning", details={"filename": uf.filename})

    total_country_files = len(saved_man_files) + len(saved_woman_files)
    logger.info(f"Saved {len(saved_dataset_files)} candidate items, {len(saved_man_files)} man images, and {len(saved_woman_files)} woman images for session {userSessionGUID}")

    # Launch background ML pipeline task
    background_tasks.add_task(
        run_custom_ml_pipeline,
        user_session_guid=userSessionGUID,
        session_dir=session_dir,
        custom_country_name=custom_country_name,
        custom_dataset_dir=dataset_start_dir if saved_dataset_files else None,
        custom_country_dir=country_images_dir if total_country_files > 0 else None
    )

    update_progress(
        user_session_guid=userSessionGUID,
        percent=1,
        step_id=0,
        step_name="Request Enqueued",
        details=f"Received {len(saved_dataset_files)} candidate catalog files, {len(saved_man_files)} men lookbook photos, {len(saved_woman_files)} women lookbook photos."
    )

    return {
        "status": "accepted",
        "message": "ML Pipeline execution initiated in background.",
        "userSessionGUID": userSessionGUID,
        "customCountryName": custom_country_name,
        "candidateFilesCount": len(saved_dataset_files),
        "countryImagesManCount": len(saved_man_files),
        "countryImagesWomanCount": len(saved_woman_files),
        "progressUrl": f"/api/progress/{userSessionGUID}",
        "resultsUrl": f"/api/results/{userSessionGUID}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
