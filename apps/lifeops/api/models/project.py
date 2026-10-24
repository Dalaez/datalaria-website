"""
Pydantic models for Projects and Tasks (Phase 3).
"""

import datetime as dt
import enum
import uuid
from typing import Optional
from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────

class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, enum.Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"


# ── Task Comment ───────────────────────────────────

class TaskComment(BaseModel):
    """Schema for a single task progress comment with timestamp."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str = Field(..., min_length=1)
    created_at: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))


class TaskCommentCreate(BaseModel):
    """Schema for adding a new comment to a task."""
    text: str = Field(..., min_length=1)


# ── Project ────────────────────────────────────────

class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    priority: Priority = Priority.MEDIUM
    start_date: Optional[dt.date] = None
    target_end_date: Optional[dt.date] = None
    budget: Optional[float] = Field(None, ge=0)
    tags: list[str] = Field(default_factory=list)
    color: str = "#2196F3"


class ProjectUpdate(BaseModel):
    """Schema for updating a project (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[Priority] = None
    start_date: Optional[dt.date] = None
    target_end_date: Optional[dt.date] = None
    actual_end_date: Optional[dt.date] = None
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
    start_date: Optional[dt.date] = None
    target_end_date: Optional[dt.date] = None
    actual_end_date: Optional[dt.date] = None
    budget: Optional[float] = None
    spent: float = 0
    tags: list[str] = Field(default_factory=list)
    color: str = "#2196F3"
    created_at: dt.datetime
    updated_at: dt.datetime


# ── Task ───────────────────────────────────────────

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    project_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    due_date: Optional[dt.date] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    tags: list[str] = Field(default_factory=list)
    comments: list[TaskComment] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    project_id: Optional[str] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    due_date: Optional[dt.date] = None
    completed_at: Optional[dt.datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    actual_hours: Optional[float] = Field(None, ge=0)
    tags: Optional[list[str]] = None
    comments: Optional[list[TaskComment]] = None


class TaskResponse(BaseModel):
    """Schema for task API responses."""
    id: str
    user_id: str
    project_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Priority
    due_date: Optional[dt.date] = None
    completed_at: Optional[dt.datetime] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    tags: list[str] = Field(default_factory=list)
    comments: list[TaskComment] = Field(default_factory=list)
    created_at: dt.datetime
    updated_at: dt.datetime
