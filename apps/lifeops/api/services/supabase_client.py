"""
LifeOps API — Supabase Client Service
======================================
Singleton Supabase client configured for the 'lifeops' schema.
"""
from supabase import create_client, Client
from functools import lru_cache

from config import get_settings


@lru_cache()
def get_supabase_client() -> Client:
    """
    Create and cache the Supabase client.
    Uses the service_role key for full backend access (bypasses RLS).
    RLS is enforced at the API layer via JWT validation.
    """
    settings = get_settings()
    client = create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
    )
    return client


def get_supabase_schema() -> str:
    """Return the configured schema name."""
    return get_settings().supabase_schema


def db(table_name: str):
    """
    Shortcut to query a table in the lifeops schema.

    Usage:
        result = db("activities").select("*").eq("user_id", uid).execute()
    """
    client = get_supabase_client()
    schema = get_supabase_schema()
    return client.schema(schema).table(table_name)
