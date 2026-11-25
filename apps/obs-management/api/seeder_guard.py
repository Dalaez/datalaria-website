"""Agentic Radar — Seeder Guard & Tenant Protection Service (ADR-014 / INV-OBS-5).

Garantiza que las cargas sintéticas de BOM (data_loader / generate_dummy_bom) solo puedan
ejecutarse sobre cuentas demo explícitamente autorizadas, bloqueando cualquier cuenta real.
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

ALLOWED_DEMO_EMAILS: set[str] = {
    "datalaria@gmail.com",
    "demo@datalaria.com",
}

ALLOWED_DEMO_UIDS: set[str] = {
    "18d01a19-450b-4099-96f4-66b21714a525",
    "mock-user-obs-datalaria",
}

PROTECTED_REAL_EMAILS: set[str] = {
    "dalaez1@gmail.com",
}


class SeederProtectionError(PermissionError):
    """Se lanza cuando se intenta inyectar un BOM sintético en una cuenta protegida o no autorizada."""


def validate_synthetic_seed_target(user_id: str, email: Optional[str] = None) -> bool:
    """Valida que el destino de seeding sintético pertenezca a la whitelist demo."""
    if not user_id or not user_id.strip():
        raise SeederProtectionError("SECURITY ALERT: Se requiere un user_id explícito para seeding en obs_radar.")

    normalized_email = email.strip().lower() if email else None

    if normalized_email and normalized_email in PROTECTED_REAL_EMAILS:
        msg = f"SECURITY ALERT: Seeding bloqueado para usuario real protegido {normalized_email} ({user_id})."
        logger.error(msg)
        raise SeederProtectionError(msg)

    if normalized_email and normalized_email not in ALLOWED_DEMO_EMAILS:
        msg = f"SECURITY ALERT: Email {normalized_email} fuera de ALLOWED_DEMO_EMAILS."
        logger.error(msg)
        raise SeederProtectionError(msg)

    if user_id.strip() not in ALLOWED_DEMO_UIDS:
        msg = f"SECURITY ALERT: User ID {user_id} fuera de ALLOWED_DEMO_UIDS."
        logger.error(msg)
        raise SeederProtectionError(msg)

    return True
