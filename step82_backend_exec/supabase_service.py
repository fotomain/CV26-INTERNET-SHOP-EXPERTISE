"""
Supabase Integration Service for step82_backend_exec.
Uses Supabase REST API for upserts and error logging on:
- cv26ShopUserSessionTable
- cv26ShopProgressTable
- cv26ShopResultsTable
- cv26ShopErrorsTable
"""

import os
import json
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://czgrxgzdmodkkmbmraub.supabase.co").rstrip('/')
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

logger = logging.getLogger("supabase_service")

# In-memory session store fallback
_in_memory_progress = {}
_in_memory_results = {}
_in_memory_sessions = {}
_in_memory_errors = []

def _get_headers():
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=representation"
    }

def upsert_user_session(user_session_guid: str, start_time: str, finish_time: str = None, duration: str = None, status: str = "running"):
    """
    Upserts user session record into cv26ShopUserSessionTable.
    """
    session_json = {
        "startRunDateTime": start_time,
        "finishRunDateTime": finish_time,
        "runDuration": duration,
        "status": status,
        "lastUpdated": datetime.now(timezone.utc).isoformat()
    }
    
    _in_memory_sessions[user_session_guid] = session_json
    
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return session_json

    endpoint = f"{SUPABASE_URL}/rest/v1/cv26ShopUserSessionTable"
    payload = {
        "userSessionGUID": user_session_guid,
        "userSessionJSON": session_json,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        res = requests.post(endpoint, headers=_get_headers(), json=payload, timeout=5)
        if res.status_code not in (200, 201, 204):
            logger.warning(f"Supabase user session upsert HTTP {res.status_code}: {res.text}")
    except Exception as e:
        logger.warning(f"Failed to upsert to cv26ShopUserSessionTable: {e}")

    return session_json

def update_progress(user_session_guid: str, percent: int, step_id: int, step_name: str, details: str = ""):
    """
    Upserts real-time progress into cv26ShopProgressTable.
    """
    progress_json = {
        "percent": int(percent),
        "stepId": int(step_id),
        "stepName": str(step_name),
        "details": str(details),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    _in_memory_progress[user_session_guid] = progress_json

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return progress_json

    endpoint = f"{SUPABASE_URL}/rest/v1/cv26ShopProgressTable"
    payload = {
        "userSessionGUID": user_session_guid,
        "progressDataJSON": progress_json,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        res = requests.post(endpoint, headers=_get_headers(), json=payload, timeout=5)
        if res.status_code not in (200, 201, 204):
            logger.warning(f"Supabase progress upsert HTTP {res.status_code}: {res.text}")
    except Exception as e:
        logger.warning(f"Failed to upsert to cv26ShopProgressTable: {e}")

    return progress_json

def get_progress(user_session_guid: str) -> dict:
    """
    Retrieves progress from Supabase or fallback memory cache.
    """
    if SUPABASE_URL and SUPABASE_ANON_KEY:
        try:
            endpoint = f"{SUPABASE_URL}/rest/v1/cv26ShopProgressTable?userSessionGUID=eq.{user_session_guid}&select=*"
            res = requests.get(endpoint, headers=_get_headers(), timeout=4)
            if res.status_code == 200:
                data = res.json()
                if data and len(data) > 0:
                    return data[0].get("progressDataJSON", {})
        except Exception:
            pass

    return _in_memory_progress.get(user_session_guid, {
        "percent": 0,
        "stepId": 0,
        "stepName": "Initialized",
        "details": "Ready for execution"
    })

def upsert_results(user_session_guid: str, result_data: dict):
    """
    Upserts full DSS & Capstone result data into cv26ShopResultsTable.
    """
    _in_memory_results[user_session_guid] = result_data

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return result_data

    endpoint = f"{SUPABASE_URL}/rest/v1/cv26ShopResultsTable"
    payload = {
        "userSessionGUID": user_session_guid,
        "resultDataJSON": result_data,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        res = requests.post(endpoint, headers=_get_headers(), json=payload, timeout=10)
        if res.status_code not in (200, 201, 204):
            logger.warning(f"Supabase results upsert HTTP {res.status_code}: {res.text}")
    except Exception as e:
        logger.warning(f"Failed to upsert to cv26ShopResultsTable: {e}")

    return result_data

def get_results(user_session_guid: str) -> dict:
    """
    Retrieves resultDataJSON from Supabase or fallback memory cache.
    """
    if SUPABASE_URL and SUPABASE_ANON_KEY:
        try:
            endpoint = f"{SUPABASE_URL}/rest/v1/cv26ShopResultsTable?userSessionGUID=eq.{user_session_guid}&select=*"
            res = requests.get(endpoint, headers=_get_headers(), timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data and len(data) > 0:
                    return data[0].get("resultDataJSON", {})
        except Exception:
            pass

    return _in_memory_results.get(user_session_guid, {})

def log_error(user_session_guid: str, error_msg: str, error_type: str = "PipelineError", details: dict = None):
    """
    Logs errors to cv26ShopErrorsTable.
    """
    error_json = {
        "errorType": error_type,
        "errorMessage": str(error_msg),
        "details": details or {},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    _in_memory_errors.append({"userSessionGUID": user_session_guid, "errorJSON": error_json})
    logger.error(f"[{user_session_guid}] {error_type}: {error_msg}")

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return error_json

    endpoint = f"{SUPABASE_URL}/rest/v1/cv26ShopErrorsTable"
    payload = {
        "userSessionGUID": user_session_guid,
        "errorJSON": error_json
    }

    try:
        res = requests.post(endpoint, headers=_get_headers(), json=payload, timeout=5)
        if res.status_code not in (200, 201, 204):
            logger.warning(f"Supabase error log HTTP {res.status_code}: {res.text}")
    except Exception as e:
        logger.warning(f"Failed to log error to cv26ShopErrorsTable: {e}")

    return error_json
