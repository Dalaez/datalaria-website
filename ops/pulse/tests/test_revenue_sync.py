"""
ops/pulse/tests/test_revenue_sync.py
-----------------------------------
Suite determinista offline para Telemetría Financiera y Audiencia (Hito 9.2 / INV-PULSE-13):
- Cero PII en modelos, payloads, reportes locales y snapshot Admin.
- Aislamiento estricto en .gitignore (revenue_metrics.json, executive_state.json, REVENUE_REPORT.md).
- Cero fugas en static/apps/pulse/data/public.json (INV-PULSE-2/13).
- Degradación elegante independiente ante ausencia de API keys o errores HTTP (INV-PULSE-11).
- Generación válida de executive_state.json y REVENUE_REPORT.md.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import pytest
import requests

from ops.pulse.sync_admin_snapshot import build_revenue_intelligence_payload
from ops.pulse.sync_revenue import (
    assert_no_pii_in_payload,
    build_executive_state,
    fetch_brevo_audience_summary,
    fetch_lemon_squeezy_summary,
    sync_all_revenue,
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class _FakeResp:
    def __init__(self, payload: Dict[str, Any], status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self) -> Dict[str, Any]:
        return self._payload


def test_gitignore_blocks_private_financial_artifacts() -> None:
    """INV-PULSE-13: Los 3 ficheros financieros privados deben estar declarados en .gitignore y ser ignorados por Git."""
    gitignore = (ROOT_DIR / ".gitignore").read_text(encoding="utf-8")
    required_entries = (
        "/data/pulse/private/revenue_metrics.json",
        "/data/pulse/private/executive_state.json",
        "/data/pulse/private/REVENUE_REPORT.md",
    )
    for entry in required_entries:
        assert entry in gitignore, f"Falta '{entry}' en .gitignore"
        res = subprocess.run(
            ["git", "check-ignore", entry.lstrip("/")],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
        assert res.returncode == 0, f"git check-ignore no ignoró {entry}: {res.stderr}"


def test_lemon_squeezy_and_brevo_graceful_degradation_when_missing_keys(monkeypatch) -> None:
    """INV-PULSE-11/13: Sin credenciales devuelve unavailable y nunca rompe el pipeline."""
    monkeypatch.delenv("LEMON_SQUEEZY_API_KEY", raising=False)
    monkeypatch.delenv("LEMON_SQUEEZY_STORE_ID", raising=False)
    monkeypatch.delenv("BREVO_API_KEY", raising=False)

    ls_ok, ls_summary = fetch_lemon_squeezy_summary()
    assert ls_ok is False
    assert ls_summary.status == "unavailable"
    assert ls_summary.net_revenue_eur_30d == 0.0

    br_ok, br_summary = fetch_brevo_audience_summary()
    assert br_ok is False
    assert br_summary.status == "unavailable"
    assert br_summary.total_subscribers == 0


def test_sync_revenue_strips_all_pii_and_builds_executive_state(tmp_path, monkeypatch) -> None:
    """INV-PULSE-13: Descarta emails, nombres, IPs y direcciones antes de serializar y calcula agregados exactos."""
    now = datetime(2026, 11, 24, 20, 0, tzinfo=timezone.utc)

    def fake_get(url: str, headers: Dict[str, str], timeout: int = 12):
        if "api.lemonsqueezy.com/v1/orders" in url:
            return _FakeResp(
                {
                    "data": [
                        {
                            "id": "ord_1",
                            "attributes": {
                                "status": "paid",
                                "refunded": False,
                                "test_mode": False,
                                "currency": "EUR",
                                "subtotal": 1900,
                                "tax": 399,
                                "total": 2299,
                                "created_at": "2026-11-20T10:00:00Z",
                                "user_email": "buyer.secret@example.com",
                                "user_name": "Alice Secret Buyer",
                                "ip_address": "203.0.113.42",
                                "billing_address": {"country": "US", "line1": "123 Secret St"},
                                "first_order_item": {
                                    "product_id": 101,
                                    "product_name": "Datalaria Pulse: Content Ops Kit",
                                },
                            },
                        },
                        {
                            "id": "ord_2",
                            "attributes": {
                                "status": "paid",
                                "refunded": False,
                                "test_mode": False,
                                "currency": "EUR",
                                "subtotal": 3900,
                                "tax": 819,
                                "total": 4719,
                                "created_at": "2026-11-22T12:00:00Z",
                                "user_email": "carlos.privado@empresa.es",
                                "user_name": "Carlos Privado",
                                "billing_address": {"country": "ES", "city": "Madrid"},
                                "first_order_item": {
                                    "product_id": 202,
                                    "product_name": "Total Mega Bundle",
                                },
                            },
                        },
                        {
                            "id": "ord_test_ignored",
                            "attributes": {
                                "status": "paid",
                                "test_mode": True,
                                "subtotal": 9900,
                                "created_at": "2026-11-23T10:00:00Z",
                                "user_email": "test@datalaria.com",
                            },
                        },
                    ],
                    "links": {},
                }
            )
        if "api.lemonsqueezy.com/v1/products" in url:
            return _FakeResp(
                {
                    "data": [
                        {"id": "101", "attributes": {"status": "published"}},
                        {"id": "202", "attributes": {"status": "published"}},
                    ],
                    "links": {},
                }
            )
        if "api.lemonsqueezy.com/v1/checkouts" in url:
            return _FakeResp(
                {
                    "data": [
                        {"id": "c1", "attributes": {"created_at": "2026-11-20T09:50:00Z", "completed": True}},
                        {"id": "c2", "attributes": {"created_at": "2026-11-22T11:50:00Z", "completed": True}},
                        {"id": "c3", "attributes": {"created_at": "2026-11-23T15:00:00Z", "completed": False}},
                        {"id": "c4", "attributes": {"created_at": "2026-11-24T08:00:00Z", "completed": False}},
                    ],
                    "links": {},
                }
            )
        if "api.brevo.com/v3/contacts/lists" in url:
            return _FakeResp(
                {
                    "lists": [
                        {"id": 3, "name": "Datalaria Newsletter ES", "totalSubscribers": 40, "uniqueSubscribers": 40},
                        {"id": 4, "name": "Datalaria Newsletter EN", "totalSubscribers": 65, "uniqueSubscribers": 65},
                        {"id": 6, "name": "Helix Waitlist EN", "totalSubscribers": 25, "uniqueSubscribers": 25},
                    ]
                }
            )
        if "api.brevo.com/v3/emailCampaigns" in url:
            return _FakeResp(
                {
                    "campaigns": [
                        {
                            "id": 10,
                            "name": "Pulse Launch EN",
                            "sentDate": "2026-11-18T10:00:00Z",
                            "statistics": {
                                "globalStats": {
                                    "delivered": 100,
                                    "uniqueViews": 48,
                                    "uniqueClicks": 7,
                                    "unsubscriptions": 1,
                                }
                            },
                        }
                    ]
                }
            )
        raise AssertionError(f"URL inesperada en test offline: {url}")

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setenv("LEMON_SQUEEZY_API_KEY", "ls_test_key")
    monkeypatch.setenv("LEMON_SQUEEZY_STORE_ID", "99999")
    monkeypatch.setenv("BREVO_API_KEY", "brevo_test_key")

    rev_path = tmp_path / "revenue_metrics.json"
    exec_path = tmp_path / "executive_state.json"
    rep_path = tmp_path / "REVENUE_REPORT.md"

    report, exec_state = sync_all_revenue(
        dry_run=False,
        output_path=rev_path,
        executive_state_path=exec_path,
        report_path=rep_path,
    )

    assert report.lemon_squeezy.status == "ok"
    assert report.lemon_squeezy.orders_30d == 2
    assert report.lemon_squeezy.net_revenue_eur_30d == 58.0
    assert report.lemon_squeezy.avg_order_value_eur == 29.0
    assert report.lemon_squeezy.checkout_abandonment_pct == 50.0
    assert report.brevo.status == "ok"
    assert report.brevo.total_subscribers == 130
    assert report.brevo.waitlist_helix_subscribers == 25
    assert report.brevo.avg_open_rate_pct == 48.0

    assert exec_state.stage_progress_pct == 11.6
    assert "Estadio 1" in exec_state.stage_label

    raw_rev_text = rev_path.read_text(encoding="utf-8")
    raw_exec_text = exec_path.read_text(encoding="utf-8")
    raw_md_text = rep_path.read_text(encoding="utf-8")
    for sensitive in (
        "buyer.secret@example.com",
        "Alice Secret Buyer",
        "203.0.113.42",
        "123 Secret St",
        "carlos.privado@empresa.es",
        "Carlos Privado",
        "Madrid",
    ):
        assert sensitive not in raw_rev_text
        assert sensitive not in raw_exec_text
        assert sensitive not in raw_md_text

    assert_no_pii_in_payload(json.loads(raw_rev_text))
    assert_no_pii_in_payload(json.loads(raw_exec_text))

    # Verificar que build_revenue_intelligence_payload integra limpiamente para Supabase RLS
    admin_payload = build_revenue_intelligence_payload(
        revenue_metrics_path=rev_path,
        executive_state_path=exec_path,
    )
    assert admin_payload["is_synthetic"] is False
    assert admin_payload["pii_stripped"] is True
    assert admin_payload["lemon_squeezy"]["net_revenue_eur_30d"] == 58.0


def test_sync_revenue_strict_mode_fails_without_keys(monkeypatch) -> None:
    """Con --strict falla explícitamente si faltan credenciales."""
    monkeypatch.delenv("LEMON_SQUEEZY_API_KEY", raising=False)
    monkeypatch.delenv("LEMON_SQUEEZY_STORE_ID", raising=False)
    monkeypatch.delenv("BREVO_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        sync_all_revenue(dry_run=True, strict=True)


def test_public_json_firewall_zero_financial_leak_inv_pulse_13() -> None:
    """INV-PULSE-2/13: static/apps/pulse/data/public.json jamás expone claves financieras o PII."""
    public_json = ROOT_DIR / "static" / "apps" / "pulse" / "data" / "public.json"
    if not public_json.is_file():
        pytest.skip("public.json aún no compilado")

    raw = public_json.read_text(encoding="utf-8")
    for forbidden in (
        "revenue_intelligence",
        "revenue_metrics",
        "net_revenue_eur",
        "lemon_squeezy",
        "checkout_abandonment_pct",
        "executive_state",
        "user_email",
    ):
        assert forbidden not in raw, f"Fuga financiera prohibida '{forbidden}' detectada en public.json"

    parsed = json.loads(raw)
    assert "revenue_intelligence" not in parsed
