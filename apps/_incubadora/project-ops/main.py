"""
Agentic PMO Sandbox - FastAPI Entrypoint
========================================
The central nervous system of the Agentic PMO.
All endpoints are async. All validation is strict (Pydantic).
All math is delegated to evm_engine.py (The Muscle).
"""
from datetime import date
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from models import IngestResponse, EVMSnapshot, MonteCarloResult
import ingest_service
import evm_engine
import db_tools

app = FastAPI(
    title="Agentic PMO API",
    version="1.0.0",
    description=(
        "Project Operations Engineering Backend. "
        "Event-Driven EVM calculations and Monte Carlo simulations "
        "for C-Level decision intelligence."
    ),
)

# CORS: Allow the Vanilla JS / Tailwind frontend to consume this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Phase 2: Ingestion Endpoints
# ==========================================

@app.post(
    "/api/v1/ingest/excel",
    response_model=IngestResponse,
    summary="Ingest a project Excel payload",
    description=(
        "Accepts an Excel file (.xlsx) with 3 sheets: "
        "'Project', 'Resources', 'Tasks'. "
        "Validates via Pydantic, then injects into the "
        "pmo_analytics Kimball star schema on Supabase."
    ),
)
async def ingest_excel(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename or not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .xlsx or .xls files are accepted."
        )

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file received.")

    try:
        payload = ingest_service.parse_excel(file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    try:
        result = ingest_service.ingest_to_supabase(payload)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database ingestion failed: {e}"
        )

    return result


# ==========================================
# Phase 3: Quantitative Engine Endpoints
# ==========================================

@app.get(
    "/api/v1/evm/{project_id}",
    response_model=EVMSnapshot,
    summary="Calculate real-time EVM snapshot",
    description=(
        "Computes Planned Value, Earned Value, Actual Cost, "
        "CPI and SPI for a project at a given date. "
        "Persists the snapshot to fact_evm_snapshot."
    ),
)
async def get_evm_snapshot(
    project_id: str,
    snapshot_date: Optional[date] = Query(
        default=None,
        description="Date for the EVM calculation. Defaults to today."
    ),
):
    try:
        snapshot = evm_engine.calculate_evm_snapshot(project_id, snapshot_date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return snapshot


@app.get(
    "/api/v1/montecarlo/{project_id}",
    response_model=MonteCarloResult,
    summary="Run Monte Carlo schedule simulation",
    description=(
        "Executes N iterations of PERT-distributed task durations "
        "to predict P50/P85/P95 completion dates and "
        "probability of on-time delivery."
    ),
)
async def run_montecarlo(
    project_id: str,
    iterations: int = Query(
        default=10000,
        ge=1000,
        le=100000,
        description="Number of simulation iterations."
    ),
):
    try:
        result = evm_engine.run_monte_carlo(project_id, iterations)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


# ==========================================
# Utility Endpoints
# ==========================================

@app.get(
    "/api/v1/projects/{project_id}",
    summary="Get project metadata",
)
async def get_project(project_id: str):
    project = db_tools.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@app.get(
    "/api/v1/projects/{project_id}/tasks",
    summary="Get all WBS tasks for a project",
)
async def get_project_tasks(project_id: str):
    tasks = db_tools.get_tasks_by_project(project_id)
    if not tasks:
        raise HTTPException(
            status_code=404, detail="No tasks found for this project."
        )
    return tasks


@app.get(
    "/api/v1/projects/{project_id}/evm-history",
    summary="Get all historical EVM snapshots",
)
async def get_evm_history(project_id: str):
    snapshots = db_tools.get_evm_snapshots(project_id)
    return snapshots


@app.get("/health", summary="Health check")
async def health():
    return {"status": "operational", "engine": "Agentic PMO v1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
