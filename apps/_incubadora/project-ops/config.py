"""
Agentic PMO Sandbox - Configuration Module
===========================================
Centralizes environment loading and the Supabase client singleton.
Zero credentials hardcoded. Zero exceptions tolerated.
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "FATAL: SUPABASE_URL and SUPABASE_KEY must be set in .env. "
        "The Muscle cannot operate without a state backend."
    )

# Singleton Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Schema prefix for all RPC and direct table queries
SCHEMA = "pmo_analytics"
