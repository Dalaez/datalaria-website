"""
LifeOps API — Smart Alerts Router
==================================
Provides real-time evaluated notifications and rules management.
All endpoints require authentication.
"""
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from middleware.auth import AuthenticatedUser, get_current_user
from services.alerts_evaluator import evaluate_user_alerts
from services.supabase_client import db

router = APIRouter(prefix="/api/v1/alerts", tags=["Alerts & Notifications"])


class AlertNotification(BaseModel):
    id: str
    type: str
    severity: str        # 'critical', 'warning', 'info'
    title: str
    message: str
    action_url: str
    action_label: str
    entity_id: str | None = None
    created_at: str


@router.get(
    "/",
    response_model=List[AlertNotification],
    summary="Get active smart alert notifications",
    description="Evaluates user rules in real-time and returns pending alerts.",
)
def get_active_alerts(
    user: AuthenticatedUser = Depends(get_current_user),
):
    alerts = evaluate_user_alerts(user.id)
    return alerts


@router.post(
    "/{alert_id}/dismiss",
    status_code=status.HTTP_200_OK,
    summary="Dismiss or acknowledge an alert",
)
def dismiss_alert(
    alert_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # Optional: store dismissed state in alert_log
    return {"status": "dismissed", "alert_id": alert_id}
