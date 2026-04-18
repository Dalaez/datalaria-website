"""
Agentic PMO Sandbox - Excel Ingestion Service
==============================================
Parses the flat Excel payload into validated Pydantic models,
then injects the structured data into the Supabase star schema.
The Excel is a dumb data vector. All intelligence lives here.
"""
import pandas as pd
from io import BytesIO
from typing import Tuple

from models import (
    FullIngestPayload, ProjectPayload, ResourcePayload,
    TaskPayload, IngestResponse,
)
import db_tools


def parse_excel(file_bytes: bytes) -> FullIngestPayload:
    """
    Reads an Excel file with 3 mandatory sheets:
      - 'Project': Single-row project definition
      - 'Resources': N rows of resource allocations
      - 'Tasks': M rows of WBS breakdown

    Returns a validated FullIngestPayload.
    Raises ValueError on structural or validation errors.
    """
    try:
        xls = pd.ExcelFile(BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Cannot parse the Excel file: {e}")

    required_sheets = {"Project", "Resources", "Tasks"}
    found_sheets = set(xls.sheet_names)
    missing = required_sheets - found_sheets
    if missing:
        raise ValueError(
            f"Missing required Excel sheets: {missing}. "
            f"Found: {found_sheets}"
        )

    # --- Parse Project Sheet (single row) ---
    df_proj = pd.read_excel(xls, sheet_name="Project")
    if df_proj.empty:
        raise ValueError("The 'Project' sheet is empty.")
    proj_row = df_proj.iloc[0].to_dict()
    project = ProjectPayload(**proj_row)

    # --- Parse Resources Sheet ---
    df_res = pd.read_excel(xls, sheet_name="Resources")
    if df_res.empty:
        raise ValueError("The 'Resources' sheet is empty.")
    resources = [ResourcePayload(**row) for _, row in df_res.iterrows()]

    # --- Parse Tasks Sheet (WBS) ---
    df_tasks = pd.read_excel(xls, sheet_name="Tasks")
    if df_tasks.empty:
        raise ValueError("The 'Tasks' sheet is empty.")
    # Pandas reads empty cells as NaN (float); Pydantic needs None for Optional[str]
    df_tasks = df_tasks.where(pd.notna(df_tasks), None)
    tasks = [TaskPayload(**row) for _, row in df_tasks.iterrows()]

    return FullIngestPayload(
        project=project,
        resources=resources,
        tasks=tasks,
    )


def ingest_to_supabase(payload: FullIngestPayload) -> IngestResponse:
    """
    Takes a validated payload and executes transactional inserts
    into the pmo_analytics star schema via Supabase.

    Order of operations:
      1. Upsert dim_project → get project_id
      2. Upsert dim_resource (bulk)
      3. Upsert dim_task (bulk, resolving dependency codes to UUIDs)
    """
    # 1. Project
    proj_data = {
        "project_code": payload.project.project_code,
        "project_name": payload.project.project_name,
        "description": payload.project.description,
        "budget_allocated": payload.project.budget_allocated,
        "status": "PLANNED",
        "start_date": payload.project.start_date.isoformat(),
    }
    if payload.project.end_date:
        proj_data["end_date"] = payload.project.end_date.isoformat()

    project_row = db_tools.upsert_project(proj_data)
    project_id = project_row.get("project_id")
    if not project_id:
        return IngestResponse(
            status="error", message="Failed to upsert project into dim_project."
        )

    # 2. Resources
    res_count = 0
    for res in payload.resources:
        db_tools.upsert_resource({
            "resource_code": res.resource_code,
            "resource_name": res.resource_name,
            "resource_type": res.resource_type,
            "standard_cost_rate": res.standard_cost_rate,
        })
        res_count += 1

    # 3. Tasks (Two-pass: insert first, then resolve dependencies)
    task_map = {}  # task_code -> task_id
    for task in payload.tasks:
        task_data = {
            "task_code": task.task_code,
            "task_name": task.task_name,
            "planned_duration_hours": task.planned_duration_hours,
            "planned_cost": task.planned_cost,
            "status": "PENDING",
        }
        row = db_tools.upsert_task(task_data, project_id)
        task_map[task.task_code] = row.get("task_id")

    # Second pass: resolve dependency_task_code → dependency_task_id
    for task in payload.tasks:
        if task.dependency_task_code and task.dependency_task_code in task_map:
            dep_id = task_map[task.dependency_task_code]
            task_row = db_tools.get_task_by_code(project_id, task.task_code)
            if task_row:
                supabase_update = {
                    "dependency_task_id": dep_id
                }
                from db_tools import _q
                _q("dim_task").update(
                    supabase_update
                ).eq("task_id", task_row["task_id"]).execute()

    return IngestResponse(
        status="success",
        project_id=project_id,
        resources_inserted=res_count,
        tasks_inserted=len(task_map),
        message=f"Project '{payload.project.project_code}' ingested. "
                f"{res_count} resources, {len(task_map)} WBS tasks loaded.",
    )
