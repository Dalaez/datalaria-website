"""
LifeOps API — Project & Task Models (Pydantic)
================================================
Data validation schemas for the professional area:
projects and tasks.
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


# ── Enums ──────────────────────────────────────────

class ProjectStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskStatus(str, Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ── Project ────────────────────────────────────────

class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    priority: Priority = Priority.MEDIUM
    start_date: Optional[date] = None
    target_end_date: Optional[date] = None
    budget: Optional[float] = Field(None, ge=0)
    tags: list[str] = Field(default_factory=list)
    color: str = "#2196F3"


class ProjectUpdate(BaseModel):
    """Schema for updating a project (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[Priority] = None
    start_date: Optional[date] = None
    target_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    budget: Optional[float] = Field(None, ge=0)
    spent: Optional[float] = Field(None, ge=0)
    tags: Optional[list[str]] = None
    color: Optional[str] = None


class ProjectResponse(BaseModel):
    """Schema for project API responses."""
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    priority: Priority
    start_date: Optional[date] = None
    target_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    budget: Optional[float] = None
    spent: float = 0
    tags: list[str] = Field(default_factory=list)
    color: str = "#2196F3"
    created_at: datetime
    updated_at: datetime


# ── Task ───────────────────────────────────────────

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    project_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    due_date: Optional[date] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    tags: list[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    project_id: Optional[str] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    due_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    actual_hours: Optional[float] = Field(None, ge=0)
    tags: Optional[list[str]] = None


class TaskResponse(BaseModel):
    """Schema for task API responses."""
    id: str
    user_id: str
    project_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Priority
    due_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
