"""
LifeOps API — Projects & Tasks Router
=======================================
CRUD endpoints for the professional area: projects and tasks.
All endpoints require authentication.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from middleware.auth import AuthenticatedUser, get_current_user
from models.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    TaskCreate, TaskUpdate, TaskResponse,
    ProjectStatus, TaskStatus, Priority,
)
from services.supabase_client import db

router = APIRouter(prefix="/api/v1/projects", tags=["Projects & Tasks"])


# ══════════════════════════════════════════════════
# PROJECTS
# ══════════════════════════════════════════════════

@router.get(
    "/",
    response_model=list[ProjectResponse],
    summary="List user projects",
)
async def list_projects(
    project_status: Optional[ProjectStatus] = Query(None, alias="status"),
    priority: Optional[Priority] = None,
    limit: int = Query(50, ge=1, le=200),
    user: AuthenticatedUser = Depends(get_current_user),
):
    query = (
        db("projects")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", desc=True)
        .limit(limit)
    )
    if project_status:
        query = query.eq("status", project_status.value)
    if priority:
        query = query.eq("priority", priority.value)

    result = query.execute()
    return result.data


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
)
async def get_project(
    project_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    result = (
        db("projects")
        .select("*")
        .eq("id", project_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return result.data[0]


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
async def create_project(
    payload: ProjectCreate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    data = payload.model_dump(mode="json")
    data["user_id"] = user.id

    result = db("projects").insert(data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create project")
    return result.data[0]


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
)
async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    update_data = payload.model_dump(mode="json", exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = (
        db("projects")
        .update(update_data)
        .eq("id", project_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return result.data[0]


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Deletes the project. Tasks under this project will have project_id set to NULL.",
)
async def delete_project(
    project_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    result = (
        db("projects")
        .delete()
        .eq("id", project_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")


# ══════════════════════════════════════════════════
# TASKS
# ══════════════════════════════════════════════════

@router.get(
    "/{project_id}/tasks",
    response_model=list[TaskResponse],
    summary="List tasks for a project",
)
async def list_project_tasks(
    project_id: str,
    task_status: Optional[TaskStatus] = Query(None, alias="status"),
    priority: Optional[Priority] = None,
    user: AuthenticatedUser = Depends(get_current_user),
):
    query = (
        db("tasks")
        .select("*")
        .eq("project_id", project_id)
        .eq("user_id", user.id)
        .order("created_at", desc=True)
    )
    if task_status:
        query = query.eq("status", task_status.value)
    if priority:
        query = query.eq("priority", priority.value)

    result = query.execute()
    return result.data


# ── Standalone tasks router (/api/v1/tasks) ───────

tasks_router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@tasks_router.get(
    "/",
    response_model=list[TaskResponse],
    summary="List all user tasks",
    description="Returns all tasks across all projects. Use query params to filter.",
)
async def list_all_tasks(
    task_status: Optional[TaskStatus] = Query(None, alias="status"),
    priority: Optional[Priority] = None,
    project_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user: AuthenticatedUser = Depends(get_current_user),
):
    query = (
        db("tasks")
        .select("*")
        .eq("user_id", user.id)
        .order("due_date", desc=False)  # Closest deadlines first
        .limit(limit)
        .offset(offset)
    )
    if task_status:
        query = query.eq("status", task_status.value)
    if priority:
        query = query.eq("priority", priority.value)
    if project_id:
        query = query.eq("project_id", project_id)

    result = query.execute()
    return result.data


@tasks_router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
)
async def get_task(
    task_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    result = (
        db("tasks")
        .select("*")
        .eq("id", task_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return result.data[0]


@tasks_router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
async def create_task(
    payload: TaskCreate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    data = payload.model_dump(mode="json")
    data["user_id"] = user.id

    result = db("tasks").insert(data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return result.data[0]


@tasks_router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
async def update_task(
    task_id: str,
    payload: TaskUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    update_data = payload.model_dump(mode="json", exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Auto-set completed_at when status changes to done
    if update_data.get("status") == "done" and "completed_at" not in update_data:
        from datetime import datetime, timezone
        update_data["completed_at"] = datetime.now(timezone.utc).isoformat()

    result = (
        db("tasks")
        .update(update_data)
        .eq("id", task_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return result.data[0]


@tasks_router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
async def delete_task(
    task_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    result = (
        db("tasks")
        .delete()
        .eq("id", task_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
