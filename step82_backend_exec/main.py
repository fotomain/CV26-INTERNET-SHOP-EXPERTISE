"""
step82_backend_exec: FastAPI Backend Service for E-Commerce DSS Pipeline.
Handles custom file uploads, image validation, asynchronous ML pipeline execution,
and Supabase real-time progress/results synchronization.
"""

import os
import json
import logging
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment
ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(ENV_PATH)

from step82_backend_exec.supabase_service import (
    update_progress,
    get_progress,
    get_results,
    upsert_user_session,
    log_error
)
from step82_backend_exec.image_preprocessor import validate_and_save_image, ImageValidationError
from step82_backend_exec.pipeline_orchestrator import run_custom_ml_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("step82_backend_exec")

app = FastAPI(
    title="CV26 DSS Marketing Intelligence API",
    description="FastAPI backend for Purchase Manager custom ML catalog scoring and target market style matching.",
    version="5.0.0"
)

# Enable CORS for React frontend
origins_str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000")
origins = [o.strip() for o in origins_str.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in origins else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom storage directory
CUSTOM_DATA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'custom_data'))
os.makedirs(CUSTOM_DATA_ROOT, exist_ok=True)

# Mount custom_data directory for static image serving if needed
app.mount("/static/custom_data", StaticFiles(directory=CUSTOM_DATA_ROOT), name="custom_data")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "step82_backend_exec",
        "version": "5.0.0",
        "supabaseConfigured": bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_ANON_KEY"))
    }

@app.get("/api/progress/{userSessionGUID}")
def fetch_progress(userSessionGUID: str):
    progress = get_progress(userSessionGUID)
    return {
        "userSessionGUID": userSessionGUID,
        "progress": progress
    }

@app.get("/api/results/{userSessionGUID}")
def fetch_results(userSessionGUID: str):
    results = get_results(userSessionGUID)
    if not results:
        return {"userSessionGUID": userSessionGUID, "status": "pending", "results": None}
    return {
        "userSessionGUID": userSessionGUID,
        "status": "completed",
        "results": results
    }

@app.post("/api/execute-ml")
async def execute_ml(
    background_tasks: BackgroundTasks,
    userSessionGUID: str = Form(...),
    custom_country_name: str = Form("United States"),
    custom_dataset_start: Optional[List[UploadFile]] = File(None),
    custom_country_images: Optional[List[UploadFile]] = File(None)
):
    """
    Receives custom dataset files, validates format and size limits,
    stores in custom_data/<userSessionGUID>/, and triggers background ML execution.
    """
    logger.info(f"Received ML execution request for userSessionGUID='{userSessionGUID}', country='{custom_country_name}'")

    if not userSessionGUID or len(userSessionGUID.strip()) < 5:
        raise HTTPException(status_code=400, detail="Invalid userSessionGUID provided.")

    # Create session folder hierarchy
    session_dir = os.path.join(CUSTOM_DATA_ROOT, userSessionGUID)
    dataset_start_dir = os.path.join(session_dir, "custom_dataset_start")
    country_images_dir = os.path.join(session_dir, "custom_country_images")

    os.makedirs(session_dir, exist_ok=True)
    os.makedirs(dataset_start_dir, exist_ok=True)
    os.makedirs(country_images_dir, exist_ok=True)

    # Save country name metadata
    country_meta_path = os.path.join(session_dir, "custom_country_name.json")
    with open(country_meta_path, 'w', encoding='utf-8') as f:
        json.dump({"custom_country_name": custom_country_name, "userSessionGUID": userSessionGUID}, f, indent=2)

    saved_dataset_files = []
    saved_country_files = []

    # Process and sanitize candidate catalog files
    if custom_dataset_start:
        for uf in custom_dataset_start:
            if not uf.filename:
                continue
            content = await uf.read()
            try:
                out_path = validate_and_save_image(content, uf.filename, dataset_start_dir)
                saved_dataset_files.append(out_path)
            except ImageValidationError as ve:
                log_error(userSessionGUID, str(ve), error_type="ValidationError", details={"filename": uf.filename})
                raise HTTPException(status_code=422, detail=str(ve))

    # Process and sanitize target country lookbook files
    if custom_country_images:
        for uf in custom_country_images:
            if not uf.filename:
                continue
            content = await uf.read()
            try:
                out_path = validate_and_save_image(content, uf.filename, country_images_dir)
                saved_country_files.append(out_path)
            except ImageValidationError as ve:
                log_error(userSessionGUID, str(ve), error_type="ValidationError", details={"filename": uf.filename})
                raise HTTPException(status_code=422, detail=str(ve))

    logger.info(f"Saved {len(saved_dataset_files)} candidate items and {len(saved_country_files)} country images for session {userSessionGUID}")

    # Launch background ML pipeline task
    background_tasks.add_task(
        run_custom_ml_pipeline,
        user_session_guid=userSessionGUID,
        session_dir=session_dir,
        custom_country_name=custom_country_name,
        custom_dataset_dir=dataset_start_dir if saved_dataset_files else None,
        custom_country_dir=country_images_dir if saved_country_files else None
    )

    update_progress(
        userSessionGUID,
        percent=5,
        step_id=1,
        step_name="Queueing Execution",
        details=f"Received {len(saved_dataset_files)} catalog items and {len(saved_country_files)} country images."
    )

    return {
        "status": "processing",
        "userSessionGUID": userSessionGUID,
        "message": "ML pipeline execution scheduled.",
        "candidateFilesCount": len(saved_dataset_files),
        "countryImagesCount": len(saved_country_files),
        "targetCountry": custom_country_name
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("step82_backend_exec.main:app", host=host, port=port, reload=True)
