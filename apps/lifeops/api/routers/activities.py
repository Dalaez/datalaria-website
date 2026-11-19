"""
LifeOps API — Activities Router
=================================
CRUD endpoints for the personal area: activities, workouts, books, films.
Includes server-side paginated endpoint (/paged) and embedded PostgREST joins
(ADR-030, INV-12..15). All endpoints require authentication.
"""
import logging
import math
from datetime import date
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from middleware.auth import AuthenticatedUser, get_current_user
from models.activity import (
    ActivityCreate, ActivityUpdate, ActivityResponse, ActivityType,
    SportActivityCreate, BookActivityCreate, FilmActivityCreate,
    SportActivityUpdate, BookActivityUpdate, FilmActivityUpdate,
    WorkoutResponse, BookResponse, FilmResponse,
    ALLOWED_PAGE_SIZES, SportSummary, PagedActivitiesResponse,
)
from services.supabase_client import db, rpc

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/activities", tags=["Activities"])


# ── Embedded PostgREST Join Helpers (INV-15) ──────

_EMBEDDED_RELATIONS = (
    ("workouts", "workout"),
    ("books", "book"),
    ("films", "film"),
)


def _resolve_activity_type_value(activity_type: Optional[ActivityType | str]) -> Optional[str]:
    if isinstance(activity_type, ActivityType):
        return activity_type.value
    if isinstance(activity_type, str) and activity_type:
        return activity_type
    return None


def _select_clause_for_type(activity_type_val: Optional[str]) -> str:
    """Return PostgREST embedded select clause avoiding secondary .in_() calls (INV-15)."""
    if activity_type_val == ActivityType.SPORT.value:
        return "*, workouts(*)"
    if activity_type_val == ActivityType.BOOK.value:
        return "*, books(*)"
    if activity_type_val == ActivityType.FILM.value:
        return "*, films(*)"
    return "*, workouts(*), books(*), films(*)"


def _normalize_embedded_activity(row: dict[str, Any]) -> dict[str, Any]:
    """Flatten PostgREST embedded child arrays (workouts/books/films) into singular dicts."""
    item = dict(row)
    for plural_key, singular_key in _EMBEDDED_RELATIONS:
        if plural_key in item:
            rel = item.pop(plural_key)
            if isinstance(rel, list):
                if rel:
                    item[singular_key] = rel[0]
            elif isinstance(rel, dict) and rel:
                item[singular_key] = rel
    return item


def _extract_duration_seconds(row: dict[str, Any]) -> int:
    """Match client getWorkoutTotalSeconds: prefer metadata.duration_seconds, fallback duration_minutes * 60."""
    meta = row.get("metadata") or {}
    if isinstance(meta, dict) and meta.get("duration_seconds") is not None:
        try:
            return int(meta["duration_seconds"])
        except (TypeError, ValueError):
            pass
    dur_min = row.get("duration_minutes")
    if dur_min is not None:
        try:
            return round(float(dur_min) * 60)
        except (TypeError, ValueError):
            pass
    return 0


def _compute_sport_summary(
    user_id: str,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> SportSummary:
    """
    Compute historical sport KPIs across the full filtered dataset (INV-14).
    Prefers SQL RPC lifeops.sport_summary(UUID) when unfiltered (<5 ms in Postgres)
    and falls back deterministically to block-wise embedded projection if RPC is absent
    or date filters are active.
    """
    if date_from is None and date_to is None:
        try:
            res = rpc("sport_summary", {"p_user_id": user_id}).execute()
            raw = res.data
            if isinstance(raw, list) and raw:
                raw = raw[0]
            if isinstance(raw, dict) and "count" in raw:
                return SportSummary(
                    count=int(raw.get("count") or 0),
                    total_km=round(float(raw.get("total_km") or 0.0), 2),
                    total_seconds=int(raw.get("total_seconds") or 0),
                    total_kcal=int(raw.get("total_kcal") or 0),
                    pb_count=int(raw.get("pb_count") or 0),
                )
        except Exception as exc:
            logger.debug("RPC sport_summary unavailable, using block fallback: %s", exc)

    count = 0
    total_km = 0.0
    total_seconds = 0
    total_kcal = 0
    pb_count = 0

    block_size = 1000
    block_start = 0

    while True:
        q = (
            db("activities")
            .select("id, duration_minutes, metadata, workouts(distance_km, calories, personal_best)")
            .eq("user_id", user_id)
            .eq("activity_type", ActivityType.SPORT.value)
        )
        if isinstance(date_from, date):
            q = q.gte("date", date_from.isoformat())
        if isinstance(date_to, date):
            q = q.lte("date", date_to.isoformat())

        rows = (
            q.order("id", desc=False)
            .range(block_start, block_start + block_size - 1)
            .execute()
            .data
            or []
        )
        if not rows:
            break

        for row in rows:
            count += 1
            total_seconds += _extract_duration_seconds(row)
            rel = row.get("workouts")
            if isinstance(rel, list):
                w = rel[0] if rel else {}
            elif isinstance(rel, dict):
                w = rel
            else:
                w = row.get("workout") or {}

            if w.get("distance_km") is not None:
                total_km += float(w["distance_km"])
            if w.get("calories") is not None:
                total_kcal += int(w["calories"])
            if w.get("personal_best"):
                pb_count += 1

        if len(rows) < block_size:
            break
        block_start += block_size

    return SportSummary(
        count=count,
        total_km=round(total_km, 2),
        total_seconds=total_seconds,
        total_kcal=total_kcal,
        pb_count=pb_count,
    )


# ── List Activities ────────────────────────────────

@router.get(
    "/",
    response_model=list[ActivityResponse],
    summary="List user activities",
    description="Returns all activities for the authenticated user, with optional filters.",
)
def list_activities(
    activity_type: Optional[ActivityType] = Query(None, description="Filter by type"),
    date_from: Optional[date] = Query(None, description="Start date (inclusive)"),
    date_to: Optional[date] = Query(None, description="End date (inclusive)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: AuthenticatedUser = Depends(get_current_user),
):
    query = (
        db("activities")
        .select("*")
        .eq("user_id", user.id)
        .order("date", desc=True)
        .limit(limit)
        .offset(offset)
    )

    if activity_type:
        query = query.eq("activity_type", activity_type.value)
    if date_from:
        query = query.gte("date", date_from.isoformat())
    if date_to:
        query = query.lte("date", date_to.isoformat())

    result = query.execute()
    return result.data


# ── List Activities Paginated (ADR-030) ───────────

@router.get(
    "/paged",
    response_model=PagedActivitiesResponse,
    summary="List paginated activities with embedded details and optional historical summary",
    description=(
        "Server-side pagination (12/24/48) with deterministic total ordering, "
        "PostgREST embedded join, exact total count, and decoupled historical KPI summary."
    ),
)
def list_activities_paged(
    activity_type: Optional[ActivityType] = Query(None, description="Filter by type"),
    date_from: Optional[date] = Query(None, description="Start date (inclusive)"),
    date_to: Optional[date] = Query(None, description="End date (inclusive)"),
    page: int = Query(1, ge=1, description="1-indexed page number"),
    page_size: int = Query(12, description="Allowed page sizes: 12, 24, or 48"),
    include_summary: bool = Query(
        True,
        description="Compute historical summary KPIs (set false when navigating pages or prefetching)",
    ),
    user: AuthenticatedUser = Depends(get_current_user),
):
    if page_size not in ALLOWED_PAGE_SIZES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid page_size '{page_size}'. Allowed values: 12, 24, 48.",
        )

    type_val = _resolve_activity_type_value(activity_type)
    select_clause = _select_clause_for_type(type_val)
    offset = (page - 1) * page_size

    query = (
        db("activities")
        .select(select_clause, count="exact")
        .eq("user_id", user.id)
    )
    if type_val:
        query = query.eq("activity_type", type_val)
    if isinstance(date_from, date):
        query = query.gte("date", date_from.isoformat())
    if isinstance(date_to, date):
        query = query.lte("date", date_to.isoformat())

    result = (
        query
        .order("date", desc=True)
        .order("created_at", desc=True)
        .order("id", desc=True)
        .range(offset, offset + page_size - 1)
        .execute()
    )

    raw_items = result.data or []
    total = result.count if isinstance(getattr(result, "count", None), int) else len(raw_items)
    items = [_normalize_embedded_activity(row) for row in raw_items]
    total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1
    has_more = (page * page_size) < total

    summary: Optional[SportSummary] = None
    if include_summary:
        if type_val == ActivityType.SPORT.value:
            summary = _compute_sport_summary(user.id, date_from=date_from, date_to=date_to)
        else:
            summary = SportSummary(count=total)

    return PagedActivitiesResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_more=has_more,
        summary=summary,
    )


# ── List Activities with Details ──────────────────

@router.get(
    "/details",
    summary="List activities with embedded workout, book, or film details",
    description="Returns activities with their child records joined in a single embedded PostgREST request (INV-15).",
)
def list_activities_with_details(
    activity_type: Optional[ActivityType] = Query(None, description="Filter by type"),
    date_from: Optional[date] = Query(None, description="Start date (inclusive)"),
    date_to: Optional[date] = Query(None, description="End date (inclusive)"),
    limit: int = Query(500, ge=1, le=2000),
    user: AuthenticatedUser = Depends(get_current_user),
):
    type_val = _resolve_activity_type_value(activity_type)
    select_clause = _select_clause_for_type(type_val)

    query = (
        db("activities")
        .select(select_clause)
        .eq("user_id", user.id)
    )
    if type_val:
        query = query.eq("activity_type", type_val)
    if isinstance(date_from, date):
        query = query.gte("date", date_from.isoformat())
    if isinstance(date_to, date):
        query = query.lte("date", date_to.isoformat())

    activities = (
        query
        .order("date", desc=True)
        .order("created_at", desc=True)
        .order("id", desc=True)
        .limit(limit)
        .execute()
        .data
        or []
    )

    return [_normalize_embedded_activity(a) for a in activities]


# ── Get Single Activity ───────────────────────────

@router.get(
    "/{activity_id}",
    response_model=ActivityResponse,
    summary="Get activity by ID",
)
def get_activity(
    activity_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    result = (
        db("activities")
        .select("*")
        .eq("id", activity_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Activity not found")
    return result.data[0]


# ── Create Activity ───────────────────────────────

@router.post(
    "/",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new activity",
)
def create_activity(
    payload: ActivityCreate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    data = payload.model_dump(mode="json")
    data["user_id"] = user.id

    result = db("activities").insert(data).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create activity")
    return result.data[0]


# ── Create Sport Activity (with workout detail) ──

@router.post(
    "/sport",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a sport activity with workout details",
)
def create_sport_activity(
    payload: SportActivityCreate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # Force activity_type to sport
    activity_data = payload.activity.model_dump(mode="json")
    activity_data["user_id"] = user.id
    activity_data["activity_type"] = "sport"

    # Insert activity
    activity_result = db("activities").insert(activity_data).execute()
    if not activity_result.data:
        raise HTTPException(status_code=500, detail="Failed to create activity")

    activity = activity_result.data[0]

    # Insert workout detail
    workout_data = payload.workout.model_dump(mode="json")
    workout_data["activity_id"] = activity["id"]
    db("workouts").insert(workout_data).execute()

    return activity


# ── Create Book Activity (with book detail) ───────

@router.post(
    "/book",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book activity with book details",
)
def create_book_activity(
    payload: BookActivityCreate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    activity_data = payload.activity.model_dump(mode="json")
    activity_data["user_id"] = user.id
    activity_data["activity_type"] = "book"

    activity_result = db("activities").insert(activity_data).execute()
    if not activity_result.data:
        raise HTTPException(status_code=500, detail="Failed to create activity")

    activity = activity_result.data[0]

    book_data = payload.book.model_dump(mode="json")
    book_data["activity_id"] = activity["id"]
    db("books").insert(book_data).execute()

    return activity


# ── Create Film Activity (with film detail) ───────

@router.post(
    "/film",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a film activity with film details",
)
def create_film_activity(
    payload: FilmActivityCreate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    activity_data = payload.activity.model_dump(mode="json")
    activity_data["user_id"] = user.id
    activity_data["activity_type"] = "film"

    activity_result = db("activities").insert(activity_data).execute()
    if not activity_result.data:
        raise HTTPException(status_code=500, detail="Failed to create activity")

    activity = activity_result.data[0]

    film_data = payload.film.model_dump(mode="json")
    film_data["activity_id"] = activity["id"]
    db("films").insert(film_data).execute()

    return activity


# ── Update Activity ───────────────────────────────

@router.patch(
    "/{activity_id}",
    response_model=ActivityResponse,
    summary="Update an existing activity",
)
def update_activity(
    activity_id: str,
    payload: ActivityUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # Only include fields that were explicitly set
    update_data = payload.model_dump(mode="json", exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = (
        db("activities")
        .update(update_data)
        .eq("id", activity_id)
        .eq("user_id", user.id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Activity not found")
    return result.data[0]


# ── Update Sport Activity (with workout detail) ──

@router.patch(
    "/{activity_id}/sport",
    response_model=ActivityResponse,
    summary="Update sport activity with workout details",
)
def update_sport_activity(
    activity_id: str,
    payload: SportActivityUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # 1. Update activity fields if provided
    if payload.activity:
        act_data = payload.activity.model_dump(mode="json", exclude_unset=True)
        if act_data:
            db("activities").update(act_data).eq("id", activity_id).eq("user_id", user.id).execute()

    # 2. Update workout fields if provided
    if payload.workout:
        w_data = payload.workout.model_dump(mode="json", exclude_unset=True)
        if w_data:
            db("workouts").update(w_data).eq("activity_id", activity_id).execute()

    # Return updated activity
    res = db("activities").select("*").eq("id", activity_id).eq("user_id", user.id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Activity not found")
    return res.data[0]


# ── Update Book Activity (with book detail) ───────

@router.patch(
    "/{activity_id}/book",
    response_model=ActivityResponse,
    summary="Update book activity with book details",
)
def update_book_activity(
    activity_id: str,
    payload: BookActivityUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    if payload.activity:
        act_data = payload.activity.model_dump(mode="json", exclude_unset=True)
        if act_data:
            db("activities").update(act_data).eq("id", activity_id).eq("user_id", user.id).execute()

    if payload.book:
        b_data = payload.book.model_dump(mode="json", exclude_unset=True)
        if b_data:
            db("books").update(b_data).eq("activity_id", activity_id).execute()

    res = db("activities").select("*").eq("id", activity_id).eq("user_id", user.id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Activity not found")
    return res.data[0]


# ── Update Film Activity (with film detail) ───────

@router.patch(
    "/{activity_id}/film",
    response_model=ActivityResponse,
    summary="Update film activity with film details",
)
def update_film_activity(
    activity_id: str,
    payload: FilmActivityUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    if payload.activity:
        act_data = payload.activity.model_dump(mode="json", exclude_unset=True)
        if act_data:
            db("activities").update(act_data).eq("id", activity_id).eq("user_id", user.id).execute()

    if payload.film:
        f_data = payload.film.model_dump(mode="json", exclude_unset=True)
        if f_data:
            db("films").update(f_data).eq("activity_id", activity_id).execute()

    res = db("activities").select("*").eq("id", activity_id).eq("user_id", user.id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Activity not found")
    return res.data[0]


# ── Delete Activity ───────────────────────────────

@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an activity",
    description="Deletes the activity and all associated detail records (CASCADE).",
)
def delete_activity(
    activity_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    result = (
        db("activities")
        .delete()
        .eq("id", activity_id)
        .eq("user_id", user.id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Activity not found")


# ── Get workout/book/film detail for an activity ──

@router.get(
    "/{activity_id}/workout",
    response_model=WorkoutResponse,
    summary="Get workout details for a sport activity",
)
def get_workout_detail(
    activity_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # Verify activity belongs to user
    activity = (
        db("activities")
        .select("id")
        .eq("id", activity_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not activity.data:
        raise HTTPException(status_code=404, detail="Activity not found")

    result = db("workouts").select("*").eq("activity_id", activity_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="No workout data found")
    return result.data[0]


@router.get(
    "/{activity_id}/book",
    response_model=BookResponse,
    summary="Get book details for a book activity",
)
def get_book_detail(
    activity_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    activity = (
        db("activities")
        .select("id")
        .eq("id", activity_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not activity.data:
        raise HTTPException(status_code=404, detail="Activity not found")

    result = db("books").select("*").eq("activity_id", activity_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="No book data found")
    return result.data[0]


@router.get(
    "/{activity_id}/film",
    response_model=FilmResponse,
    summary="Get film details for a film activity",
)
def get_film_detail(
    activity_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    activity = (
        db("activities")
        .select("id")
        .eq("id", activity_id)
        .eq("user_id", user.id)
        .execute()
    )
    if not activity.data:
        raise HTTPException(status_code=404, detail="Activity not found")

    result = db("films").select("*").eq("activity_id", activity_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="No film data found")
    return result.data[0]
