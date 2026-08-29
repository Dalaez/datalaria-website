"""
LifeOps API — Activity Models (Pydantic)
==========================================
Data validation schemas for the personal area:
activities, workouts, books, films.
"""
import datetime as dt
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


# ── Enums ──────────────────────────────────────────

class ActivityType(str, Enum):
    SPORT = "sport"
    BOOK = "book"
    FILM = "film"
    LEARNING = "learning"
    JOURNAL = "journal"


class BookStatus(str, Enum):
    READING = "reading"
    COMPLETED = "completed"
    WISHLIST = "wishlist"
    ABANDONED = "abandoned"


class MediaType(str, Enum):
    MOVIE = "movie"
    SERIES = "series"
    DOCUMENTARY = "documentary"
    ANIME = "anime"


# ── Activity ───────────────────────────────────────

class ActivityCreate(BaseModel):
    """Schema for creating a new activity."""
    activity_type: ActivityType
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    date: dt.date = Field(default_factory=dt.date.today)
    duration_minutes: Optional[int] = Field(None, ge=0)
    rating: Optional[int] = Field(None, ge=1, le=5)
    tags: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class ActivityUpdate(BaseModel):
    """Schema for updating an activity (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    date: Optional[dt.date] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    rating: Optional[int] = Field(None, ge=1, le=5)
    tags: Optional[list[str]] = None
    metadata: Optional[dict] = None


class ActivityResponse(BaseModel):
    """Schema for activity API responses."""
    id: str
    user_id: str
    activity_type: ActivityType
    title: str
    description: Optional[str] = None
    date: dt.date
    duration_minutes: Optional[int] = None
    rating: Optional[int] = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    created_at: dt.datetime
    updated_at: dt.datetime


# ── Workout (Sport detail) ─────────────────────────

class WorkoutCreate(BaseModel):
    """Additional sport-specific data when creating a sport activity."""
    workout_type: str = Field(..., min_length=1)  # running, cycling, gym...
    distance_km: Optional[float] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    avg_heart_rate: Optional[int] = Field(None, ge=30, le=250)
    elevation_m: Optional[int] = Field(None, ge=0)
    personal_best: bool = False
    notes: Optional[str] = None


class WorkoutResponse(WorkoutCreate):
    id: str
    activity_id: str


# ── Book detail ────────────────────────────────────

class BookCreate(BaseModel):
    """Additional book-specific data when creating a book activity."""
    author: str = Field(..., min_length=1)
    pages_total: Optional[int] = Field(None, ge=1)
    pages_read: int = Field(0, ge=0)
    status: BookStatus = BookStatus.READING
    genre: Optional[str] = None
    isbn: Optional[str] = None
    cover_url: Optional[str] = None
    start_date: Optional[dt.date] = None
    finish_date: Optional[dt.date] = None


class BookResponse(BookCreate):
    id: str
    activity_id: str


# ── Film detail ────────────────────────────────────

class FilmCreate(BaseModel):
    """Additional film/series-specific data when creating a film activity."""
    director: Optional[str] = None
    media_type: MediaType = MediaType.MOVIE
    genre: Optional[str] = None
    platform: Optional[str] = None
    year: Optional[int] = Field(None, ge=1888, le=2100)
    season: Optional[int] = Field(None, ge=1)
    episode: Optional[int] = Field(None, ge=1)
    imdb_url: Optional[str] = None


class FilmResponse(FilmCreate):
    id: str
    activity_id: str


# ── Combined create (activity + detail) ────────────

class SportActivityCreate(BaseModel):
    """Create a sport activity with workout details in one request."""
    activity: ActivityCreate
    workout: WorkoutCreate


class BookActivityCreate(BaseModel):
    """Create a book activity with book details in one request."""
    activity: ActivityCreate
    book: BookCreate


class FilmActivityCreate(BaseModel):
    """Create a film activity with film details in one request."""
    activity: ActivityCreate
    film: FilmCreate


# ── Update Schemas (activity + detail) ────────────

class WorkoutUpdate(BaseModel):
    workout_type: Optional[str] = None
    distance_km: Optional[float] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    avg_heart_rate: Optional[int] = Field(None, ge=30, le=250)
    elevation_m: Optional[int] = Field(None, ge=0)
    personal_best: Optional[bool] = None
    notes: Optional[str] = None


class BookUpdate(BaseModel):
    author: Optional[str] = None
    pages_total: Optional[int] = Field(None, ge=1)
    pages_read: Optional[int] = Field(None, ge=0)
    status: Optional[BookStatus] = None
    genre: Optional[str] = None
    isbn: Optional[str] = None
    cover_url: Optional[str] = None
    start_date: Optional[dt.date] = None
    finish_date: Optional[dt.date] = None


class FilmUpdate(BaseModel):
    director: Optional[str] = None
    media_type: Optional[MediaType] = None
    genre: Optional[str] = None
    platform: Optional[str] = None
    year: Optional[int] = Field(None, ge=1888, le=2100)
    season: Optional[int] = Field(None, ge=1)
    episode: Optional[int] = Field(None, ge=1)
    imdb_url: Optional[str] = None


class SportActivityUpdate(BaseModel):
    activity: Optional[ActivityUpdate] = None
    workout: Optional[WorkoutUpdate] = None


class BookActivityUpdate(BaseModel):
    activity: Optional[ActivityUpdate] = None
    book: Optional[BookUpdate] = None


class FilmActivityUpdate(BaseModel):
    activity: Optional[ActivityUpdate] = None
    film: Optional[FilmUpdate] = None

