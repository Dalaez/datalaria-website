"""Contratos de datos Pydantic v2 para Agentic Radar API (SPEC-APP-OBS-MANAGEMENT v2.0.0)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

SeverityBand = Literal["CRITICAL LTB REQUIRED", "EVALUATING INVENTORY", "MONITORED"]
LifecycleStatus = Literal["Active", "NRND", "EOL", "Obsolete"]
LtbVerdict = Literal["EXECUTE_LTB", "REDESIGN_FFF", "HYBRID_BRIDGE"]


class CommercialAlert(BaseModel):
    alert_type: Literal["PDN", "EOL", "PCN"]
    mpn: str = Field(..., min_length=2, max_length=120)
    manufacturer: str = Field(..., min_length=2, max_length=120)
    estimated_eol_date: str | None = None


class InboundEmail(BaseModel):
    subject: str = Field(..., min_length=3, max_length=300)
    text: str = Field(..., min_length=10, max_length=20000)


class AffectedSkuItem(BaseModel):
    sku: str
    trigger_mpn: str
    assembly_path: list[str] = Field(default_factory=list)
    margin_at_risk: float = Field(..., ge=0.0)
    criticality_score: int = Field(..., ge=0, le=100)
    alt_sources_count: int = Field(..., ge=0)
    status: SeverityBand


class DashboardRiskMetrics(BaseModel):
    total_risk_eur: float = Field(..., ge=0.0)
    active_alerts: int = Field(..., ge=0)
    blocked_skus_count: int = Field(..., ge=0)
    estimated_ltb_capital_eur: float = Field(..., ge=0.0)
    affected_skus: list[AffectedSkuItem]
    agent_logs: list[str]
    cycle_detected: bool = False
    generated_at: datetime


class LtbComparisonInput(BaseModel):
    monthly_demand: float = Field(..., gt=0)
    demand_cv: float = Field(0.20, ge=0.0, le=1.0)
    redesign_months: float = Field(..., gt=0, le=60)
    lead_time_months: float = Field(2.0, ge=0.0, le=24)
    current_stock_units: float = Field(0.0, ge=0.0)
    ltb_unit_price_eur: float = Field(..., gt=0)
    fff_unit_price_eur: float = Field(..., gt=0)
    redesign_nre_eur: float = Field(..., ge=0.0)
    annual_holding_wacc_rate: float = Field(0.28, ge=0.0, le=1.0)
    monthly_margin_at_risk_eur: float = Field(..., ge=0.0)
    service_level_z: Literal[1.645, 2.054, 2.326] = 2.054


class LtbComparisonResult(BaseModel):
    safety_stock_units: int
    ltb_order_qty: int
    ltb_working_capital_eur: float
    ltb_total_cost_eur: float
    fff_total_cost_eur: float
    stock_gap_months: float
    savings_eur: float
    breakeven_months: float | None
    verdict: LtbVerdict


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "agentic-radar-api"
    version: str = "2.0.0"
    schema_name: str = "obs_radar"


class WebhookAcceptedResponse(BaseModel):
    status: Literal["accepted", "ignored"]
    message: str
