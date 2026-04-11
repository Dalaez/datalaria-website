"""
Agentic PMO Sandbox - Pydantic Models
======================================
Strict data contracts for the API boundary.
Every field is validated before touching the database.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from uuid import UUID


# ==========================================
# Inbound Payload: Excel Row Schemas
# ==========================================

class ProjectPayload(BaseModel):
    """Contract for a single project definition row from the Excel."""
    project_code: str = Field(..., min_length=1, max_length=50)
    project_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    budget_allocated: float = Field(..., gt=0)
    start_date: date
    end_date: Optional[date] = None


class ResourcePayload(BaseModel):
    """Contract for a single resource definition row from the Excel."""
    resource_code: str = Field(..., min_length=1, max_length=50)
    resource_name: str = Field(..., min_length=1, max_length=255)
    resource_type: str = Field(..., pattern=r"^(ENGINEER|MACHINE|VENDOR)$")
    standard_cost_rate: float = Field(..., gt=0)


class TaskPayload(BaseModel):
    """Contract for a single WBS task row from the Excel."""
    project_code: str = Field(..., min_length=1, max_length=50)
    task_code: str = Field(..., min_length=1, max_length=50)
    task_name: str = Field(..., min_length=1, max_length=255)
    planned_duration_hours: float = Field(..., gt=0)
    planned_cost: float = Field(..., gt=0)
    dependency_task_code: Optional[str] = None


class FullIngestPayload(BaseModel):
    """
    The complete Excel payload parsed into structured sections.
    One project, N resources, M tasks (WBS).
    """
    project: ProjectPayload
    resources: List[ResourcePayload]
    tasks: List[TaskPayload]


# ==========================================
# Outbound: API Response Models
# ==========================================

class IngestResponse(BaseModel):
    status: str
    project_id: Optional[str] = None
    resources_inserted: int = 0
    tasks_inserted: int = 0
    message: str


class EVMSnapshot(BaseModel):
    """A single EVM snapshot for a project at a point in time."""
    project_id: str
    snapshot_date: date
    planned_value: float
    earned_value: float
    actual_cost: float
    cpi: float = Field(..., description="Cost Performance Index = EV / AC")
    spi: float = Field(..., description="Schedule Performance Index = EV / PV")


class MonteCarloResult(BaseModel):
    """Output of a Monte Carlo schedule simulation."""
    project_id: str
    iterations: int
    p50_completion_days: float
    p85_completion_days: float
    p95_completion_days: float
    probability_on_time: float = Field(
        ..., ge=0, le=1,
        description="Probability of finishing on or before planned end date"
    )
    cost_overrun_expected: float
