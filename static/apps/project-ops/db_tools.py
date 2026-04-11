"""
Agentic PMO Sandbox - Database Tools (Supabase Interface)
=========================================================
All direct interactions with the pmo_analytics schema.
No business logic here. Pure data access layer.
"""
from typing import List, Dict, Any, Optional
from config import supabase, SCHEMA


def _table(name: str) -> str:
    """Returns the fully qualified table name for the pmo_analytics schema."""
    return f"{SCHEMA}.{name}"


# ==========================================
# DIM_PROJECT
# ==========================================

def upsert_project(data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert or update a project. Returns the upserted row."""
    result = supabase.table("dim_project").upsert(
        data, on_conflict="project_code"
    ).execute()
    return result.data[0] if result.data else {}


def get_project_by_code(project_code: str) -> Optional[Dict[str, Any]]:
    """Fetch a single project by its unique code."""
    result = supabase.table("dim_project").select("*").eq(
        "project_code", project_code
    ).execute()
    return result.data[0] if result.data else None


def get_project_by_id(project_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single project by its UUID."""
    result = supabase.table("dim_project").select("*").eq(
        "project_id", project_id
    ).execute()
    return result.data[0] if result.data else None


# ==========================================
# DIM_RESOURCE
# ==========================================

def upsert_resource(data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert or update a resource. Returns the upserted row."""
    result = supabase.table("dim_resource").upsert(
        data, on_conflict="resource_code"
    ).execute()
    return result.data[0] if result.data else {}


def get_resource_by_code(resource_code: str) -> Optional[Dict[str, Any]]:
    """Fetch a single resource by its unique code."""
    result = supabase.table("dim_resource").select("*").eq(
        "resource_code", resource_code
    ).execute()
    return result.data[0] if result.data else None


# ==========================================
# DIM_TASK
# ==========================================

def upsert_task(data: Dict[str, Any], project_id: str) -> Dict[str, Any]:
    """Insert or update a WBS task within a project scope."""
    data["project_id"] = project_id
    result = supabase.table("dim_task").upsert(
        data, on_conflict="project_id,task_code"
    ).execute()
    return result.data[0] if result.data else {}


def get_tasks_by_project(project_id: str) -> List[Dict[str, Any]]:
    """Fetch all WBS tasks for a given project."""
    result = supabase.table("dim_task").select("*").eq(
        "project_id", project_id
    ).order("task_code").execute()
    return result.data if result.data else []


def get_task_by_code(project_id: str, task_code: str) -> Optional[Dict[str, Any]]:
    """Fetch a specific task by project + task code."""
    result = supabase.table("dim_task").select("*").eq(
        "project_id", project_id
    ).eq("task_code", task_code).execute()
    return result.data[0] if result.data else None


# ==========================================
# FACT_TASK_EXECUTION
# ==========================================

def insert_task_execution(data: Dict[str, Any]) -> Dict[str, Any]:
    """Log a single task execution event (hours, cost, progress)."""
    result = supabase.table("fact_task_execution").insert(data).execute()
    return result.data[0] if result.data else {}


def get_executions_by_project(project_id: str) -> List[Dict[str, Any]]:
    """Fetch all execution records for tasks belonging to a project."""
    # First get all task_ids for the project
    tasks = get_tasks_by_project(project_id)
    if not tasks:
        return []
    task_ids = [t["task_id"] for t in tasks]
    result = supabase.table("fact_task_execution").select("*").in_(
        "task_id", task_ids
    ).order("execution_date").execute()
    return result.data if result.data else []


# ==========================================
# FACT_EVM_SNAPSHOT
# ==========================================

def insert_evm_snapshot(data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a daily EVM snapshot for a project."""
    result = supabase.table("fact_evm_snapshot").upsert(
        data, on_conflict="project_id,snapshot_date"
    ).execute()
    return result.data[0] if result.data else {}


def get_evm_snapshots(project_id: str) -> List[Dict[str, Any]]:
    """Fetch all EVM snapshots for a project, ordered by date."""
    result = supabase.table("fact_evm_snapshot").select("*").eq(
        "project_id", project_id
    ).order("snapshot_date").execute()
    return result.data if result.data else []


def get_latest_evm_snapshot(project_id: str) -> Optional[Dict[str, Any]]:
    """Fetch the most recent EVM snapshot for a project."""
    result = supabase.table("fact_evm_snapshot").select("*").eq(
        "project_id", project_id
    ).order("snapshot_date", desc=True).limit(1).execute()
    return result.data[0] if result.data else None
