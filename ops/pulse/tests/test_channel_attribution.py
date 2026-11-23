"""
ops/pulse/tests/test_channel_attribution.py
-------------------------------------------
Tests deterministas 100 % offline para el Hito 7.11 (ADR-033 / INV-PULSE-2/11/12):
- Normalización de canales y referrers históricos (lnkd.in, t.co, dev.to, coderlegion.com, etc.).
- Consolidación GA4 Acquisition + Eventos Clave y preservación ante fallo parcial.
- Ventana previa GSC (60d..31d) y bandera `is_brand_query`.
- Detección de Ganadores Ocultos por Canal y Alertas de Dark Social.
- Firewall estricto: cero fuga de métricas de canal ni cifras absolutas a `static/apps/pulse/data/public.json`.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

from ops.pulse.impact_analyzer import (
    analyze_channel_performance,
    detect_dark_social_alerts,
    detect_hidden_channel_winners,
    extract_brand_query_totals,
    generate_impact_report_markdown,
)
from ops.pulse.models import PulseImpactReport
from ops.pulse.sync_metrics import (
    aggregate_gsc_page_query_rows,
    classify_canonical_channel,
    consolidate_asset_metrics,
    consolidate_channel_metrics,
    is_brand_query,
    is_key_conversion_event,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


@pytest.mark.parametrize(
    ("source", "medium", "expected"),
    [
        ("linkedin", "social", "linkedin"),
        ("lnkd.in", "referral", "linkedin"),
        ("linkedin.com", "referral", "linkedin"),
        ("com.linkedin.android", "referral", "linkedin"),
        ("x", "social", "x"),
        ("t.co", "referral", "x"),
        ("x.com", "referral", "x"),
        ("twitter.com", "social", "x"),
        ("devto", "syndication", "devto"),
        ("dev.to", "referral", "devto"),
        ("coderlegion", "syndication", "coderlegion"),
        ("coderlegion.com", "referral", "coderlegion"),
        ("newsletter", "email", "newsletter"),
        ("brevo", "email", "newsletter"),
        ("google", "organic", "google_organic"),
        ("(direct)", "(none)", "direct"),
        ("reddit.com", "referral", "other"),
    ],
)
def test_classify_canonical_channel_normalizes_utms_and_historical_referrers(
    source: str, medium: str, expected: str
) -> None:
    assert classify_canonical_channel(source, medium) == expected


def test_brand_query_and_key_conversion_event_detection() -> None:
    assert is_brand_query("datalaria") is True
    assert is_brand_query("Datalaria Pulse Excel") is True
    assert is_brand_query("leonid kantorovich") is False

    assert is_key_conversion_event("join_waitlist_helix", "/es/posts/sdd/") is True
    assert is_key_conversion_event("home_pack_click", "/es/") is True
    assert is_key_conversion_event("click", "/es/recursos/") is True
    assert is_key_conversion_event("click", "/en/resources/") is True
    assert is_key_conversion_event("scroll", "/es/posts/demo/") is False

    by_page, records = aggregate_gsc_page_query_rows(
        [
            {"keys": ["https://datalaria.com/es/", "datalaria"], "clicks": 15, "impressions": 120, "position": 1.2},
            {"keys": ["https://datalaria.com/en/posts/sdd/", "spec driven"], "clicks": 4, "impressions": 200, "position": 6.5},
        ]
    )
    assert any(r["is_brand_query"] for r in records)
    b_clicks, b_impr = extract_brand_query_totals({"by_page": by_page})
    assert b_clicks == 15
    assert b_impr == 120


def test_consolidate_channel_metrics_and_graceful_degradation_inv_pulse_12() -> None:
    assets = [
        {
            "id": "obs_parte8",
            "url_es": "/es/posts/obs_parte8/",
            "url_en": "/en/posts/obs_part8/",
        },
        {
            "id": "pack_stock",
            "url_es": "/es/recursos/",
            "url_en": "/en/resources/",
        },
    ]
    acq = {
        "current_rows": [
            {
                "path": "/es/posts/obs_parte8",
                "source": "lnkd.in",
                "medium": "referral",
                "campaign": "(not set)",
                "sessions": 12,
                "users": 10,
                "engaged_sessions": 9,
                "engagement_sec": 620.0,
            },
            {
                "path": "/en/posts/obs_part8",
                "source": "dev.to",
                "medium": "referral",
                "campaign": "obs_part8",
                "sessions": 18,
                "users": 16,
                "engaged_sessions": 14,
                "engagement_sec": 960.0,
            },
            {
                "path": "/en/posts/obs_part8",
                "source": "t.co",
                "medium": "referral",
                "campaign": "",
                "sessions": 5,
                "users": 5,
                "engaged_sessions": 4,
                "engagement_sec": 260.0,
            },
            {
                "path": "/en/posts/obs_part8",
                "source": "coderlegion.com",
                "medium": "referral",
                "campaign": "",
                "sessions": 4,
                "users": 4,
                "engaged_sessions": 3,
                "engagement_sec": 240.0,
            },
        ],
        "prev_rows": [
            {"source": "linkedin", "medium": "social", "sessions": 6, "users": 5, "engaged_sessions": 4},
        ],
        "event_rows": [
            {"path": "/es/posts/obs_parte8", "source": "lnkd.in", "medium": "referral", "event_name": "join_waitlist_helix", "count": 2},
            {"path": "/en/posts/obs_part8", "source": "dev.to", "medium": "referral", "event_name": "home_pack_click", "count": 1},
        ],
        "daily_rows": [
            {"date": "2026-11-20", "source": "(direct)", "medium": "(none)", "sessions": 4},
            {"date": "2026-11-21", "source": "(direct)", "medium": "(none)", "sessions": 5},
            {"date": "2026-11-22", "source": "(direct)", "medium": "(none)", "sessions": 18},
            {"date": "2026-11-22", "source": "linkedin", "medium": "social", "sessions": 1},
        ],
    }

    consolidated = consolidate_channel_metrics(assets, acq, acquisition_ok=True, days=30)
    assert consolidated["visibility"] == "private"
    assert consolidated["sources_status"]["x_native"] == "standby_zero_cost"
    assert consolidated["by_channel"]["linkedin"]["sessions_30d"] == 12
    assert consolidated["by_channel"]["linkedin"]["trend_30d_pct"] == 100.0
    assert consolidated["by_channel"]["linkedin"]["key_events_30d"] == 2
    assert consolidated["by_channel"]["devto"]["sessions_en_30d"] == 18
    assert consolidated["by_channel"]["x"]["sessions_30d"] == 5
    assert consolidated["by_channel"]["coderlegion"]["sessions_30d"] == 4
    assert consolidated["by_asset"]["obs_parte8"]["linkedin"]["key_events_30d"] == 2

    # Fallo parcial en siguiente ejecución NO sobrescribe el snapshot válido (INV-PULSE-11/12)
    preserved = consolidate_channel_metrics(
        assets,
        acquisition_data={},
        existing_channel_metrics=consolidated,
        acquisition_ok=False,
        days=30,
    )
    assert preserved["by_channel"]["linkedin"]["sessions_30d"] == 12
    assert preserved["by_channel"]["devto"]["sessions_30d"] == 18


def test_gsc_prev_window_preservation_in_consolidate_asset_metrics() -> None:
    assets = [{"id": "demo", "url_es": "/es/posts/demo/", "url_en": "/en/posts/demo/"}]
    first = consolidate_asset_metrics(
        assets=assets,
        ga4_data={"/es/posts/demo": {"views": 50, "users": 40, "engagement_sec": 300.0, "views_prev": 30}},
        gsc_data={"/es/posts/demo": {"clicks": 10, "impressions": 400, "ctr_pct": 2.5, "position": 8.0}},
        gsc_by_page={},
        gsc_prev_data={"/es/posts/demo": {"clicks": 6, "impressions": 250, "ctr_pct": 2.4, "position": 10.5}},
        ga4_ok=True,
        gsc_ok=True,
        gsc_prev_ok=True,
    )
    assert first["demo"]["gsc_clicks_prev_30d"] == 6
    assert first["demo"]["gsc_impressions_prev_30d"] == 250
    assert first["demo"]["gsc_avg_position_prev"] == 10.5

    # Si falla la ventana previa GSC en un run posterior, preserva los valores previos
    second = consolidate_asset_metrics(
        assets=assets,
        ga4_data={"/es/posts/demo": {"views": 55, "users": 42, "engagement_sec": 310.0, "views_prev": 30}},
        gsc_data={"/es/posts/demo": {"clicks": 12, "impressions": 420, "ctr_pct": 2.86, "position": 7.4}},
        gsc_by_page={},
        existing_metrics=first,
        ga4_ok=True,
        gsc_ok=True,
        gsc_prev_data={},
        gsc_prev_ok=False,
    )
    assert second["demo"]["gsc_clicks_30d"] == 12
    assert second["demo"]["gsc_clicks_prev_30d"] == 6
    assert second["demo"]["gsc_impressions_prev_30d"] == 250


def test_hidden_channel_winners_dark_social_alerts_and_markdown_render(tmp_path: Path) -> None:
    published_posts = [
        {"id": "obs_parte8", "slug": "obs_parte8", "title_es": "Agentic Radar v2.0"}
    ]
    channel_data = {
        "by_channel": {
            "linkedin": {
                "sessions_30d": 12,
                "sessions_es_30d": 8,
                "sessions_en_30d": 4,
                "en_share_pct": 33.3,
                "users_30d": 10,
                "engaged_sessions_30d": 9,
                "engagement_rate_pct": 75.0,
                "avg_engagement_sec": 62.0,
                "key_events_30d": 2,
                "conversion_rate_pct": 16.67,
                "sessions_prev_30d": 6,
                "trend_30d_pct": 100.0,
            },
            "direct": {
                "sessions_30d": 180,
                "sessions_es_30d": 100,
                "sessions_en_30d": 80,
                "en_share_pct": 44.4,
                "users_30d": 150,
                "engaged_sessions_30d": 90,
                "engagement_rate_pct": 50.0,
                "avg_engagement_sec": 30.0,
                "key_events_30d": 0,
                "conversion_rate_pct": 0.0,
                "sessions_prev_30d": 90,
                "trend_30d_pct": 100.0,
            },
        },
        "by_asset": {
            "obs_parte8": {
                "linkedin": {"sessions_30d": 12, "avg_engagement_sec": 62.0, "key_events_30d": 2},
                "devto": {"sessions_30d": 45, "avg_engagement_sec": 55.0, "key_events_30d": 1},
            }
        },
        "daily_by_channel": {
            "2026-11-18": {"direct": 4, "linkedin": 2},
            "2026-11-19": {"direct": 4, "linkedin": 2},
            "2026-11-20": {"direct": 4, "linkedin": 1},
            "2026-11-21": {"direct": 22, "linkedin": 1},
            "2026-11-22": {"direct": 18, "linkedin": 0},
        },
    }

    q_file = tmp_path / "dispatch_queue.yaml"
    q_file.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "entries": [
                    {
                        "id": "obs-v2-es-linkedin",
                        "file_path": "content/es/posts/obs_parte8/index.md",
                        "lang": "es",
                        "wave": "1_es_native",
                        "channels": ["linkedin"],
                        "scheduled_at_utc": "2026-11-21T08:00:00Z",
                        "executed_at_utc": "2026-11-21T08:05:00Z",
                        "status": "completed",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    summary = analyze_channel_performance(channel_data)
    assert len(summary) == 2

    winners = detect_hidden_channel_winners(published_posts, channel_data)
    assert len(winners) == 1
    assert winners[0].asset_id == "obs_parte8"
    assert winners[0].channel == "linkedin"

    alerts = detect_dark_social_alerts(channel_data, dispatch_queue_path=q_file)
    assert any(a.alert_type == "dark_social_spike" and a.dispatch_id == "obs-v2-es-linkedin" for a in alerts)
    assert any(a.alert_type == "high_direct_share" for a in alerts)

    report = PulseImpactReport(
        generated_at=datetime.now(timezone.utc),
        total_published_posts=1,
        total_scheduled_posts=0,
        total_30d_post_views=100,
        median_post_views=50.0,
        p75_post_views=75.0,
        monthly_growth_yoy_pct=10.0,
        category_performance=[],
        quick_wins_ctr=[],
        monetization_orphans=[],
        decay_alerts=[],
        prioritized_backlog=[],
        channel_summary=summary,
        hidden_channel_winners=winners,
        dark_social_alerts=alerts,
    )
    md = generate_impact_report_markdown(report)
    assert "Rendimiento por Canal de Adquisición (ES vs. EN)" in md
    assert "stand-by" in md.lower()
    assert "obs_parte8" in md
    assert "obs-v2-es-linkedin" in md


def test_public_dataset_firewall_zero_channel_metrics_leak_inv_pulse_2_12() -> None:
    """Garantiza INV-PULSE-2 e INV-PULSE-12: cero métricas de canal ni archivos privados en static/."""
    static_pulse_dir = REPO_ROOT / "static" / "apps" / "pulse"
    assert not any("channel_metrics" in p.name for p in static_pulse_dir.rglob("*"))
    assert not any("social_metrics" in p.name for p in static_pulse_dir.rglob("*"))
    assert not any("distribution_ledger" in p.name for p in static_pulse_dir.rglob("*"))

    public_json_path = static_pulse_dir / "data" / "public.json"
    if public_json_path.is_file():
        raw_text = public_json_path.read_text(encoding="utf-8")
        for forbidden_key in (
            '"channel_metrics"',
            '"channel_summary"',
            '"dark_social_alerts"',
            '"hidden_channel_winners"',
            '"gsc_clicks_prev_30d"',
            '"gsc_brand_clicks_30d"',
            '"key_events_breakdown"',
        ):
            assert forbidden_key not in raw_text
        data = json.loads(raw_text)
        for asset in data.get("assets", []):
            assert asset.get("metrics_absolute") is None
