"""
LifeOps API — Stats Router
============================
Analytics and statistics endpoints.
Aggregated views of personal and professional data.
"""
import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from middleware.auth import AuthenticatedUser, get_current_user
from services.supabase_client import db

router = APIRouter(prefix="/api/v1/stats", tags=["Statistics"])


# ── Response models ───────────────────────────────

class DashboardSummary(BaseModel):
    """Aggregated dashboard data for the authenticated user."""
    # Personal
    total_activities: int = 0
    activities_this_week: int = 0
    activities_this_month: int = 0
    sport_count: int = 0
    books_count: int = 0
    films_count: int = 0
    learning_count: int = 0

    # Professional
    total_projects: int = 0
    active_projects: int = 0
    total_tasks: int = 0
    tasks_todo: int = 0
    tasks_in_progress: int = 0
    tasks_done: int = 0
    tasks_overdue: int = 0

    # Streaks
    active_habits: int = 0


class ActivityBreakdown(BaseModel):
    """Activity counts grouped by type for a given period."""
    period_start: dt.date
    period_end: dt.date
    sport: int = 0
    book: int = 0
    film: int = 0
    learning: int = 0
    journal: int = 0
    total: int = 0


# ── Dashboard Summary ─────────────────────────────

@router.get(
    "/dashboard",
    response_model=DashboardSummary,
    summary="Get dashboard summary",
    description="Returns aggregated counts for the dashboard widgets.",
)
async def get_dashboard_summary(
    user: AuthenticatedUser = Depends(get_current_user),
):
    today = dt.date.today()
    week_start = today - dt.timedelta(days=today.weekday())  # Monday
    month_start = today.replace(day=1)

    # ── Personal area ──
    all_activities = (
        db("activities")
        .select("id, activity_type, date")
        .eq("user_id", user.id)
        .execute()
    )
    activities = all_activities.data or []

    total = len(activities)
    this_week = sum(1 for a in activities if a["date"] >= week_start.isoformat())
    this_month = sum(1 for a in activities if a["date"] >= month_start.isoformat())
    sport = sum(1 for a in activities if a["activity_type"] == "sport")
    books = sum(1 for a in activities if a["activity_type"] == "book")
    films = sum(1 for a in activities if a["activity_type"] == "film")
    learning = sum(1 for a in activities if a["activity_type"] == "learning")

    # ── Professional area ──
    all_projects = (
        db("projects")
        .select("id, status")
        .eq("user_id", user.id)
        .execute()
    )
    projects = all_projects.data or []
    active_projects = sum(1 for p in projects if p["status"] == "active")

    all_tasks = (
        db("tasks")
        .select("id, status, due_date")
        .eq("user_id", user.id)
        .execute()
    )
    tasks = all_tasks.data or []
    todo = sum(1 for t in tasks if t["status"] == "todo")
    in_progress = sum(1 for t in tasks if t["status"] == "in_progress")
    done = sum(1 for t in tasks if t["status"] == "done")
    overdue = sum(
        1 for t in tasks
        if t.get("due_date")
        and t["due_date"] < today.isoformat()
        and t["status"] not in ("done", "cancelled")
    )

    # ── Habits ──
    habits_result = (
        db("habits")
        .select("id")
        .eq("user_id", user.id)
        .eq("is_active", True)
        .execute()
    )
    active_habits = len(habits_result.data or [])

    return DashboardSummary(
        total_activities=total,
        activities_this_week=this_week,
        activities_this_month=this_month,
        sport_count=sport,
        books_count=books,
        films_count=films,
        learning_count=learning,
        total_projects=len(projects),
        active_projects=active_projects,
        total_tasks=len(tasks),
        tasks_todo=todo,
        tasks_in_progress=in_progress,
        tasks_done=done,
        tasks_overdue=overdue,
        active_habits=active_habits,
    )


# ── Activity Breakdown ────────────────────────────

@router.get(
    "/breakdown",
    response_model=ActivityBreakdown,
    summary="Get activity breakdown by type",
    description="Returns activity counts grouped by type for a date range.",
)
async def get_activity_breakdown(
    date_from: Optional[dt.date] = Query(
        None, description="Start date. Defaults to 30 days ago."
    ),
    date_to: Optional[dt.date] = Query(
        None, description="End date. Defaults to today."
    ),
    user: AuthenticatedUser = Depends(get_current_user),
):
    today = dt.date.today()
    start = date_from or (today - dt.timedelta(days=30))
    end = date_to or today

    result = (
        db("activities")
        .select("activity_type")
        .eq("user_id", user.id)
        .gte("date", start.isoformat())
        .lte("date", end.isoformat())
        .execute()
    )
    activities = result.data or []

    counts = {"sport": 0, "book": 0, "film": 0, "learning": 0, "journal": 0}
    for a in activities:
        t = a["activity_type"]
        if t in counts:
            counts[t] += 1

    return ActivityBreakdown(
        period_start=start,
        period_end=end,
        total=len(activities),
        **counts,
    )
