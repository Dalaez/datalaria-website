"""
LifeOps API — Seeder Guard & Tenant Protection Service (INV-11)
================================================================
Guarantees that synthetic, demo, benchmark or screenshot data can ONLY EVER
be seeded into explicitly authorized demo accounts (e.g. datalaria@gmail.com).

Strictly blocks and raises SecurityException if any script or test attempts to
seed or mutate records belonging to real production users (e.g. dalaez1@gmail.com).
"""
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Explicit list of authorized demo accounts
ALLOWED_DEMO_EMAILS = {
    "datalaria@gmail.com",
    "demo@datalaria.com",
}

ALLOWED_DEMO_UIDS = {
    "18d01a19-450b-4099-96f4-66b21714a525",  # datalaria@gmail.com Supabase UUID
    "mock-user-datalaria",                    # Local Sandbox / Mock client UID
}

# Explicit list of known protected real accounts (any non-demo is protected by default)
PROTECTED_REAL_EMAILS = {
    "dalaez1@gmail.com",
}

# Known synthetic activity signatures used in blog captures and demo sets
SYNTHETIC_ACTIVITY_SIGNATURES = {
    "Half Marathon Autumn Preparation",
    "Mountain Pass Weekend Ride",
    "10x400m Track Speed Intervals",
    "Upper Body & Core Hypertrophy",
    "12K Aerobic Zone 2 Run",
    "Gravel Trail Endurance Exploration",
    "Deadlift & Posterior Chain Strength",
    "Tempo 8K Progressive Run",
    "Fast 5K Recovery Jog",
    "Rolling Hills 50K Road Ride",
}

SYNTHETIC_PROJECT_SIGNATURES = {
    "LifeOps Cloud & Analytics",
    "Datalaria Growth & Architecture",
}

SYNTHETIC_TASK_SIGNATURES = {
    "Implement 360 Analytics Dashboard Engine",
    "Render Cold-Start SWR Cache Mitigation",
    "Recharts Time-Series & Donut Integration",
    "Executive Series Part 6 Publication",
    "Supabase RLS Multi-Schema Audit",
}


class SeederProtectionError(PermissionError):
    """Raised when an operation attempts to seed synthetic data into a protected user account."""
    pass


def validate_synthetic_seed_target(user_id: str, email: Optional[str] = None) -> bool:
    """
    Validates whether the target user is an authorized demo account.
    Raises SeederProtectionError if the target is a real or unapproved account.

    Usage:
        validate_synthetic_seed_target(user_id, email="dalaez1@gmail.com")
        # -> Raises SeederProtectionError!
    """
    normalized_email = email.strip().lower() if email else None

    # Check 1: Explicit real protected email
    if normalized_email and normalized_email in PROTECTED_REAL_EMAILS:
        msg = f"SECURITY ALERT: Seeding blocked for protected production user {normalized_email} ({user_id})!"
        logger.error(msg)
        raise SeederProtectionError(msg)

    # Check 2: Email whitelist (if provided)
    if normalized_email and normalized_email not in ALLOWED_DEMO_EMAILS:
        msg = f"SECURITY ALERT: Email {normalized_email} is not in ALLOWED_DEMO_EMAILS whitelist!"
        logger.error(msg)
        raise SeederProtectionError(msg)

    # Check 3: UID whitelist
    if user_id not in ALLOWED_DEMO_UIDS:
        msg = f"SECURITY ALERT: User ID {user_id} is not in ALLOWED_DEMO_UIDS whitelist!"
        logger.error(msg)
        raise SeederProtectionError(msg)

    return True


def detect_synthetic_leakage(records: List[Dict[str, Any]], key_field: str = "title") -> List[Dict[str, Any]]:
    """
    Scans a list of activities, tasks or projects to detect if any synthetic signatures are present.
    Returns the list of leaked synthetic records found.
    """
    all_signatures = SYNTHETIC_ACTIVITY_SIGNATURES | SYNTHETIC_PROJECT_SIGNATURES | SYNTHETIC_TASK_SIGNATURES
    leaked = []
    for r in records:
        val = r.get(key_field) or r.get("name")
        if val and val in all_signatures:
            leaked.append(r)
    return leaked
