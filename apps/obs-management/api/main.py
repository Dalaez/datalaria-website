"""API FastAPI Unificada de Agentic Radar (`obs-management` v2.0.0).

Consolida la ingesta Event-Driven (`/api/v1/webhooks/*`), la telemetría ejecutiva
(`/api/v1/dashboard/risk-metrics`), la evaluación financiera LTB (`/api/v1/ltb/evaluate`)
y el endpoint `/health`, bajo CORS restringido y verificación HMAC/Bearer en webhooks.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

API_DIR = Path(__file__).resolve().parent
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from bom_engine import (  # noqa: E402
    build_default_sandbox_catalog,
    compute_ltb_vs_fff,
    evaluate_catalog_risk,
)
from models import (  # noqa: E402
    CommercialAlert,
    DashboardRiskMetrics,
    HealthResponse,
    InboundEmail,
    LtbComparisonInput,
    LtbComparisonResult,
    WebhookAcceptedResponse,
)

load_dotenv()
logger = logging.getLogger("agentic-radar-api")


def get_allowed_origins() -> list[str]:
    """Lee ALLOWED_ORIGINS desde entorno evitando wildcard '*' en producción (INV-OBS-5)."""
    raw = os.getenv(
        "ALLOWED_ORIGINS",
        "https://datalaria.com,http://127.0.0.1:1313,http://localhost:1313,http://127.0.0.1:8001,http://localhost:8001",
    )
    origins = [o.strip() for o in raw.split(",") if o.strip() and o.strip() != "*"]
    return origins or ["https://datalaria.com"]


app = FastAPI(
    title="Agentic Radar API",
    version="2.0.0",
    description="Unified Supply Chain Obsolescence Engine (IEC 62402 · Schema obs_radar)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-Webhook-Signature", "X-API-Key"],
)


async def verify_webhook_auth(
    request: Request,
    x_webhook_signature: str | None = Header(default=None, alias="X-Webhook-Signature"),
    authorization: str | None = Header(default=None, alias="Authorization"),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    """Valida firma HMAC-SHA256 (`X-Webhook-Signature: sha256=<hex>`) o Bearer/API-Key (INV-OBS-5)."""
    hmac_secret = os.getenv("WEBHOOK_HMAC_SECRET", "").strip()
    api_key = os.getenv("WEBHOOK_API_KEY", "").strip()

    if not hmac_secret and not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Webhook authentication secrets are not configured on server.",
        )

    if hmac_secret and x_webhook_signature:
        body = await request.body()
        expected = "sha256=" + hmac.new(hmac_secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, x_webhook_signature.strip()):
            return

    if api_key:
        bearer = ""
        if authorization and authorization.lower().startswith("bearer "):
            bearer = authorization[7:].strip()
        candidate = x_api_key.strip() if x_api_key else bearer
        if candidate and hmac.compare_digest(api_key, candidate):
            return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing webhook signature / API key.",
    )


def notify_teams(message: str) -> None:
    """Envía notificación de cierre de bucle si TEAMS_WEBHOOK_URL está configurado; si no, registra log."""
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL", "").strip()
    if webhook_url:
        import httpx

        httpx.post(webhook_url, json={"text": message}, timeout=5.0)
    else:
        logger.info("[OUTBOUND WEBHOOK SIMULATION] %s", message[:240])


def process_obsolescence_background(pdn_text: str) -> None:
    """Worker asíncrono: ejecuta CrewAI con payload delimitado sin bloquear la respuesta HTTP."""
    from obsolescence_agent import execute_obsolescence_analysis

    try:
        final_assessment = execute_obsolescence_analysis(pdn_text)
        notify_teams(f"🚨 **Nueva Alerta de Obsolescencia Procesada por IA**\n\n{final_assessment}")
    except Exception as exc:  # pragma: no cover - runtime safety
        logger.error("[BACKGROUND RUNTIME ERROR] %s", exc)


def _load_active_catalog() -> dict[str, Any]:
    """Lee el catálogo de `obs_radar` en Supabase cuando hay credenciales; fallback determinista limpio."""
    if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
        try:
            from supabase_tools import load_catalog_from_supabase

            cat = load_catalog_from_supabase()
            if cat.get("products"):
                return cat
        except Exception as exc:
            logger.warning("Fallback a catálogo Sandbox determinista (%s)", exc)
    return build_default_sandbox_catalog()


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse()


@app.get("/api/v1/dashboard/risk-metrics", response_model=DashboardRiskMetrics)
def get_risk_metrics() -> DashboardRiskMetrics:
    """Calcula métricas ejecutivas en vivo sobre el motor determinista `bom_engine`."""
    catalog = _load_active_catalog()
    return evaluate_catalog_risk(catalog)


@app.post("/api/v1/ltb/evaluate", response_model=LtbComparisonResult)
def evaluate_ltb_decision(payload: LtbComparisonInput) -> LtbComparisonResult:
    """Endpoint determinista para comparar Last Time Buy vs. Rediseño FFF."""
    return compute_ltb_vs_fff(payload)


@app.post(
    "/api/v1/webhooks/commercial-radar",
    response_model=WebhookAcceptedResponse,
    dependencies=[Depends(verify_webhook_auth)],
)
async def commercial_radar_webhook(
    alert: CommercialAlert,
    background_tasks: BackgroundTasks,
) -> WebhookAcceptedResponse:
    """Vector 1: Ingesta JSONs estructurados B2B (ej. SiliconExpert, Accuris) autenticados."""
    if alert.alert_type not in {"PDN", "EOL"}:
        return WebhookAcceptedResponse(status="ignored", message="Only PDN/EOL alerts trigger risk analysis.")

    synthetic_pdn = (
        f"Commercial API Notification. Manufacturer: {alert.manufacturer}. "
        f"Target Part Number: {alert.mpn}. Status: {alert.alert_type}."
    )
    background_tasks.add_task(process_obsolescence_background, synthetic_pdn)
    return WebhookAcceptedResponse(
        status="accepted",
        message=f"Alert for MPN {alert.mpn} queued for Agentic Radar processing.",
    )


@app.post(
    "/api/v1/webhooks/inbound-email",
    response_model=WebhookAcceptedResponse,
    dependencies=[Depends(verify_webhook_auth)],
)
async def inbound_email_webhook(
    email: InboundEmail,
    background_tasks: BackgroundTasks,
) -> WebhookAcceptedResponse:
    """Vector 2: Ingesta correos raw autenticados para extracción semántica segura."""
    pdn_text = f"Subject: {email.subject}\nBody: {email.text}"
    background_tasks.add_task(process_obsolescence_background, pdn_text)
    return WebhookAcceptedResponse(
        status="accepted",
        message="Raw email queued for semantic extraction via Agentic Radar.",
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
