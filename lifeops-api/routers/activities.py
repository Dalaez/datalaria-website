"""
LifeOps API — Activities Router
=================================
CRUD endpoints for the personal area: activities, workouts, books, films.
All endpoints require authentication.
"""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from middleware.auth import AuthenticatedUser, get_current_user
from models.activity import (
    ActivityCreate, ActivityUpdate, ActivityResponse, ActivityType,
    SportActivityCreate, BookActivityCreate, FilmActivityCreate,
    WorkoutResponse, BookResponse, FilmResponse,
)
from services.supabase_client import db

router = APIRouter(prefix="/api/v1/activities", tags=["Activities"])


# ── List Activities ────────────────────────────────

@router.get(
    "/",
    response_model=list[ActivityResponse],
    summary="List user activities",
    description="Returns all activities for the authenticated user, with optional filters.",
)
async def list_activities(
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


# ── List Activities with Details ──────────────────

@router.get(
    "/details",
    summary="List activities with embedded workout, book, or film details",
    description="Returns activities with their child records joined (single request).",
)
async def list_activities_with_details(
    activity_type: Optional[ActivityType] = Query(None, description="Filter by type"),
    limit: int = Query(50, ge=1, le=200),
    user: AuthenticatedUser = Depends(get_current_user),
):
    query = (
        db("activities")
        .select("*")
        .eq("user_id", user.id)
        .order("date", desc=True)
        .limit(limit)
    )
    if isinstance(activity_type, (str, ActivityType)):
        val = activity_type.value if hasattr(activity_type, "value") else str(activity_type)
        query = query.eq("activity_type", val)

    activities = query.execute().data or []
    if not activities:
        return []

    activity_ids = [a["id"] for a in activities]
    types_present = set(a["activity_type"] for a in activities)
    details_map = {a["id"]: {} for a in activities}

    if "sport" in types_present:
        workouts = db("workouts").select("*").in_("activity_id", activity_ids).execute().data or []
        for w in workouts:
            details_map[w["activity_id"]]["workout"] = w

    if "book" in types_present:
        books = db("books").select("*").in_("activity_id", activity_ids).execute().data or []
        for b in books:
            details_map[b["activity_id"]]["book"] = b

    if "film" in types_present:
        films = db("films").select("*").in_("activity_id", activity_ids).execute().data or []
        for f in films:
            details_map[f["activity_id"]]["film"] = f

    for a in activities:
        a.update(details_map.get(a["id"], {}))

    return activities


# ── Get Single Activity ───────────────────────────

@router.get(
    "/{activity_id}",
    response_model=ActivityResponse,
    summary="Get activity by ID",
)
async def get_activity(
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
async def create_activity(
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
async def create_sport_activity(
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
async def create_book_activity(
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
async def create_film_activity(
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
async def update_activity(
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


# ── Delete Activity ───────────────────────────────

@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an activity",
    description="Deletes the activity and all associated detail records (CASCADE).",
)
async def delete_activity(
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
async def get_workout_detail(
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
async def get_book_detail(
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
async def get_film_detail(
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
