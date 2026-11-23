"""
ops/pulse/tests/test_social_metrics.py
--------------------------------------
Suite de pruebas deterministas 100 % offline para el Hito 7.12 (ADR-024 / ADR-033 / INV-PULSE-2/11/12):
- Idempotencia del Distribution Ledger (`distribution_ledger.json`) desde Autopilot LIVE y `sync_social_metrics.py`.
- Contratos HTTP gratuitos de Dev.to (`api-key`) y CoderLegion (`X-API-Key`, nunca `Bearer` — ADR-024) con respuestas 200, 401, 429 y timeout.
- Degradación elegante independiente entre Dev.to y CoderLegion (`INV-PULSE-11/12`) y estado `standby_zero_cost` para X.
- Cálculo determinista de PTR (`Pull-Through Rate`), alertas de Fuga de Traspaso (`>= 300` vistas, `PTR < 2%`)
  y Escudo Anti-Canibalización Canónica (`>= 500` vistas, `0` imp. GSC tras `> 21d`).
- Firewall estricto: cero fuga de `social_metrics.json` ni `distribution_ledger.json` en `static/apps/pulse/data/public.json`.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock

import pytest
import requests
import openpyxl

from autopilot.src.orchestrator import record_distribution_ledger_entry, run_orchestration
from autopilot.src.social_manager import SocialMediaManager
from ops.pulse.impact_analyzer import (
    calculate_ptr_pct,
    detect_canonical_shield_alerts,
    detect_ptr_leak_alerts,
    generate_impact_report_markdown,
    summarize_social_platforms,
)
from ops.pulse.models import DistributionLedger, PulseImpactReport
from ops.pulse.sync_social_metrics import (
    _refresh_linkedin_token,
    consolidate_social_metrics,
    fetch_coderlegion_posts,
    fetch_devto_published_articles,
    fetch_linkedin_company_api_metrics,
    load_distribution_ledger,
    match_canonical_to_asset,
    parse_linkedin_company_xlsx,
    sync_all_social_metrics,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def test_distribution_ledger_idempotency_and_pydantic_contract(tmp_path: Path) -> None:
    ledger_file = tmp_path / "distribution_ledger.json"

    # 1. Primera inserción de Dev.to y CoderLegion
    e1 = record_distribution_ledger_entry(
        asset_id="sdd_vs_vibe_coding",
        slug="sdd_vs_vibe_coding",
        lang="en",
        channel="devto",
        external_id="1001",
        external_url="https://dev.to/datalaria/sdd-1001",
        canonical_url="https://datalaria.com/en/posts/sdd_vs_vibe_coding/",
        published_at_utc="2026-11-12T10:00:00Z",
        ledger_path=ledger_file,
    )
    assert e1["external_id"] == "1001"

    record_distribution_ledger_entry(
        asset_id="sdd_vs_vibe_coding",
        slug="sdd_vs_vibe_coding",
        lang="en",
        channel="coderlegion",
        external_id="501",
        external_url="https://coderlegion.com/posts/501",
        canonical_url="https://datalaria.com/en/posts/sdd_vs_vibe_coding/",
        published_at_utc="2026-11-12T10:05:00Z",
        ledger_path=ledger_file,
    )

    # 2. Reintento / actualización sobre el mismo slot (channel + lang + slug) NO duplica filas
    record_distribution_ledger_entry(
        asset_id="sdd_vs_vibe_coding",
        slug="sdd_vs_vibe_coding",
        lang="en",
        channel="devto",
        external_id="1001",
        external_url="https://dev.to/datalaria/sdd-1001-updated",
        canonical_url="https://datalaria.com/en/posts/sdd_vs_vibe_coding/",
        published_at_utc="2026-11-12T12:00:00Z",
        ledger_path=ledger_file,
    )

    loaded = load_distribution_ledger(ledger_file)
    validated = DistributionLedger(**loaded)
    assert validated.visibility == "private"
    assert len(validated.entries) == 2
    devto_entry = next(e for e in validated.entries if e.channel == "devto")
    assert devto_entry.external_url == "https://dev.to/datalaria/sdd-1001-updated"


def test_post_to_linkedin_returns_urn_and_live_orchestration_records_ledger(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(url: str, headers=None, json=None, timeout=15):  # noqa: A002
        resp = MagicMock()
        resp.status_code = 201
        resp.content = b'{"id": "urn:li:ugcPost:777888999"}'
        resp.raise_for_status.return_value = None
        if "linkedin.com" in url:
            resp.json.return_value = {"id": "urn:li:ugcPost:777888999"}
        elif "dev.to" in url:
            resp.json.return_value = {"id": 4242, "url": "https://dev.to/datalaria/4242"}
        else:
            resp.json.return_value = {"id": 9191, "url": "https://coderlegion.com/posts/9191"}
        return resp

    monkeypatch.setattr("autopilot.src.social_manager.requests.post", fake_post)
    monkeypatch.setenv("LINKEDIN_COMPANY_ID", "12345")
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "li-token")
    monkeypatch.setenv("DEVTO_API_KEY", "dt-token")
    monkeypatch.setenv("CODERLEGION_API_KEY", "cl-token")
    monkeypatch.setenv("ENABLE_TWITTER", "false")
    monkeypatch.setenv("ENABLE_LINKEDIN", "true")
    monkeypatch.setenv("ENABLE_DEVTO", "true")
    monkeypatch.setenv("ENABLE_CODERLEGION", "true")
    monkeypatch.setenv("CODERLEGION_LANGS", "en")
    monkeypatch.setenv("ENABLE_NEWSLETTER", "false")

    post_dir = tmp_path / "content" / "en" / "posts" / "ledger-demo"
    post_dir.mkdir(parents=True)
    post_file = post_dir / "index.md"
    post_file.write_text(
        "---\ntitle: Ledger Demo Architecture\ntranslationKey: ledger_demo_key\ndate: 2026-11-20\ntags: [SDD, AI, Python]\n---\n\n"
        "## Overview\nDeterministic engineering systems require verified contracts and automated gates in production.\n\n"
        "## Implementation\nCheck our [Resources](/en/resources/) for full templates and schemas.\n",
        encoding="utf-8",
    )

    ledger_path = tmp_path / "distribution_ledger.json"
    res = run_orchestration(
        str(post_file),
        dry_run=False,
        cache_file=str(tmp_path / "cache.json"),
        dist_dir=tmp_path / "dist",
        ledger_path=ledger_path,
    )

    assert set(res["dispatched_channels"]) == {"linkedin", "devto", "coderlegion"}
    assert len(res["ledger_entries"]) == 3
    ledger = DistributionLedger(**load_distribution_ledger(ledger_path))
    assert len(ledger.entries) == 3
    by_ch = {e.channel: e for e in ledger.entries}
    assert by_ch["linkedin"].external_id == "urn:li:ugcPost:777888999"
    assert by_ch["linkedin"].asset_id == "ledger_demo_key"
    assert by_ch["devto"].external_id == "4242"
    assert by_ch["coderlegion"].external_id == "9191"


@pytest.mark.parametrize("status_code", [401, 429])
def test_fetch_devto_and_coderlegion_http_errors_and_timeouts_degrade_gracefully(
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    def fake_get_error(url: str, headers=None, params=None, timeout=15):
        resp = MagicMock()
        resp.status_code = status_code
        http_err = requests.exceptions.HTTPError(f"HTTP {status_code}", response=resp)
        resp.raise_for_status.side_effect = http_err
        return resp

    monkeypatch.setattr("ops.pulse.sync_social_metrics.requests.get", fake_get_error)
    ok_dt, arts = fetch_devto_published_articles(api_key="dt-key")
    assert ok_dt is False
    assert arts == []

    ok_cl, posts = fetch_coderlegion_posts(
        api_key="cl-key",
        ledger_entries=[{"channel": "coderlegion", "external_id": "101"}],
    )
    assert ok_cl is False
    assert posts == []

    # Timeout case
    def fake_get_timeout(url: str, headers=None, params=None, timeout=15):
        raise requests.exceptions.Timeout("Connection timed out")

    monkeypatch.setattr("ops.pulse.sync_social_metrics.requests.get", fake_get_timeout)
    assert fetch_devto_published_articles(api_key="dt-key") == (False, [])
    assert fetch_coderlegion_posts(
        api_key="cl-key",
        ledger_entries=[{"channel": "coderlegion", "external_id": "101"}],
    ) == (False, [])


def test_fetch_devto_and_coderlegion_200_contracts_and_x_api_key_header(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_headers: List[Dict[str, str]] = []

    def fake_get_200(url: str, headers=None, params=None, timeout=15):
        captured_headers.append({"url": url, "headers": dict(headers or {}), "params": dict(params or {})})
        resp = MagicMock()
        resp.status_code = 200
        resp.raise_for_status.return_value = None
        if "dev.to" in url:
            resp.json.return_value = [
                {
                    "id": 3001,
                    "title": "SDD vs Vibe Coding",
                    "slug": "sdd-vs-vibe-coding",
                    "url": "https://dev.to/datalaria/sdd-3001",
                    "canonical_url": "https://datalaria.com/en/posts/sdd_vs_vibe_coding/",
                    "page_views_count": 480,
                    "positive_reactions_count": 22,
                    "public_reactions_count": 25,
                    "comments_count": 6,
                    "reading_time_minutes": 8,
                    "published_at": "2026-11-10T09:00:00Z",
                }
            ]
        elif url.endswith("/posts/701"):
            resp.json.return_value = {
                "data": {
                    "id": 701,
                    "title": "SDD on CoderLegion",
                    "url": "https://coderlegion.com/posts/701",
                    "source_url": "https://datalaria.com/en/posts/sdd_vs_vibe_coding/",
                    "views": 610,
                    "reactions_count": 19,
                    "comments_count": 4,
                    "created_at": "2026-11-11T10:00:00Z",
                }
            }
        else:
            # Backfill page
            resp.json.return_value = {
                "data": [
                    {
                        "id": 702,
                        "title": "PERT on CoderLegion",
                        "source_url": "https://datalaria.com/en/posts/stochastic-3-point-pert-estimation/",
                        "views": 320,
                        "likes": 11,
                        "comments": [{"id": 1}, {"id": 2}],
                    }
                ]
            }
        return resp

    monkeypatch.setattr("ops.pulse.sync_social_metrics.requests.get", fake_get_200)

    ok_dt, dt_articles = fetch_devto_published_articles(api_key="devto-secret")
    assert ok_dt is True
    assert len(dt_articles) == 1
    assert dt_articles[0]["views"] == 480
    assert dt_articles[0]["reactions"] == 25
    assert captured_headers[0]["headers"]["api-key"] == "devto-secret"
    assert "forem.api-v1+json" in captured_headers[0]["headers"]["accept"]

    ok_cl, cl_posts = fetch_coderlegion_posts(
        api_key="cl-secret",
        ledger_entries=[{"channel": "coderlegion", "external_id": "701"}],
        backfill_pages=1,
    )
    assert ok_cl is True
    assert len(cl_posts) == 2
    by_id = {p["external_id"]: p for p in cl_posts}
    assert by_id["701"]["views"] == 610
    assert by_id["702"]["comments"] == 2
    # ADR-024: Must use X-API-Key and NEVER Authorization: Bearer
    for call in captured_headers[1:]:
        assert call["headers"]["X-API-Key"] == "cl-secret"
        assert "Authorization" not in call["headers"]


def test_consolidate_social_metrics_independent_fallback_inv_pulse_11_12(tmp_path: Path) -> None:
    assets = [
        {
            "id": "sdd_vs_vibe_coding",
            "slug": "sdd_vs_vibe_coding",
            "url_es": "/es/posts/sdd_vs_vibe_coding/",
            "url_en": "/en/posts/sdd_vs_vibe_coding/",
        }
    ]
    ledger_file = tmp_path / "distribution_ledger.json"

    first = consolidate_social_metrics(
        assets=assets,
        devto_articles=[
            {
                "external_id": "3001",
                "title": "SDD",
                "url": "https://dev.to/datalaria/3001",
                "canonical_url": "https://datalaria.com/en/posts/sdd_vs_vibe_coding/",
                "views": 480,
                "reactions": 25,
                "comments": 6,
                "published_at": "2026-11-10T09:00:00Z",
            }
        ],
        devto_ok=True,
        coderlegion_posts=[
            {
                "external_id": "701",
                "title": "SDD CL",
                "url": "https://coderlegion.com/posts/701",
                "canonical_url": "https://datalaria.com/en/posts/sdd_vs_vibe_coding/",
                "views": 610,
                "reactions": 19,
                "comments": 4,
                "published_at": "2026-11-11T10:00:00Z",
            }
        ],
        coderlegion_ok=True,
        ledger_path=ledger_file,
        dry_run=False,
    )
    assert first["platforms"]["devto"]["total_views"] == 480
    assert first["platforms"]["coderlegion"]["total_views"] == 610
    assert first["platforms"]["x"]["status"] == "standby_zero_cost"
    assert first["by_asset"]["sdd_vs_vibe_coding"]["devto"]["views"] == 480
    assert first["by_asset"]["sdd_vs_vibe_coding"]["coderlegion"]["views"] == 610
    assert len(load_distribution_ledger(ledger_file)["entries"]) == 2

    # Si CoderLegion falla en la siguiente ejecución pero Dev.to sube a 520 vistas:
    # CoderLegion conserva sus 610 vistas previas (INV-PULSE-11/12).
    second = consolidate_social_metrics(
        assets=assets,
        devto_articles=[
            {
                "external_id": "3001",
                "title": "SDD",
                "url": "https://dev.to/datalaria/3001",
                "canonical_url": "https://datalaria.com/en/posts/sdd_vs_vibe_coding/",
                "views": 520,
                "reactions": 28,
                "comments": 7,
            }
        ],
        devto_ok=True,
        coderlegion_posts=[],
        coderlegion_ok=False,
        existing_social_metrics=first,
        ledger_path=ledger_file,
        dry_run=True,
    )
    assert second["platforms"]["devto"]["total_views"] == 520
    assert second["platforms"]["coderlegion"]["total_views"] == 610
    assert second["by_asset"]["sdd_vs_vibe_coding"]["devto"]["views"] == 520
    assert second["by_asset"]["sdd_vs_vibe_coding"]["coderlegion"]["views"] == 610


def test_ptr_calculation_leak_alerts_canonical_shield_and_markdown_render() -> None:
    assert calculate_ptr_pct(15, 500) == 3.0
    assert calculate_ptr_pct(1, 480) == 0.21
    assert calculate_ptr_pct(10, 0) == 0.0

    published_posts = [
        {
            "id": "sdd_vs_vibe_coding",
            "slug": "sdd_vs_vibe_coding",
            "title_es": "SDD vs Vibe Coding",
            "publish_date": "2026-10-01",
            "url_en": "/en/posts/sdd_vs_vibe_coding/",
        }
    ]
    social_data = {
        "platforms": {
            "devto": {
                "status": "ok",
                "articles_count": 1,
                "matched_assets_count": 1,
                "total_views": 650,
                "total_reactions": 30,
                "total_comments": 5,
            },
            "coderlegion": {
                "status": "ok",
                "articles_count": 1,
                "matched_assets_count": 1,
                "total_views": 400,
                "total_reactions": 18,
                "total_comments": 3,
            },
        },
        "by_asset": {
            "sdd_vs_vibe_coding": {
                "devto": {"views": 650, "reactions": 30, "comments": 5},
                "coderlegion": {"views": 400, "reactions": 18, "comments": 3},
            }
        },
    }
    channel_data = {
        "by_channel": {
            "devto": {"sessions_30d": 2},
            "coderlegion": {"sessions_30d": 40},
        },
        "by_asset": {
            "sdd_vs_vibe_coding": {
                "devto": {"sessions_30d": 2},  # PTR = 0.31% (< 2.0% -> Fuga!)
                "coderlegion": {"sessions_30d": 40},  # PTR = 10.0% (OK)
            }
        },
    }
    metrics = {
        "sdd_vs_vibe_coding": {"gsc_impressions_30d": 0}  # > 21d & 0 imp GSC & 650 vistas -> Escudo Canónico!
    }

    plat_summary = summarize_social_platforms(social_data, channel_data)
    assert plat_summary["devto"]["ptr_pct"] == 0.31
    assert plat_summary["coderlegion"]["ptr_pct"] == 10.0
    assert plat_summary["x"]["status"] == "standby_zero_cost"

    ptr_alerts = detect_ptr_leak_alerts(published_posts, social_data, channel_data)
    assert len(ptr_alerts) == 1
    assert ptr_alerts[0].platform == "devto"
    assert ptr_alerts[0].ptr_pct == 0.31

    shield_alerts = detect_canonical_shield_alerts(published_posts, social_data, metrics)
    assert len(shield_alerts) == 1
    assert shield_alerts[0].platform == "devto"
    assert shield_alerts[0].native_views == 650

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
        social_platform_summary=plat_summary,
        ptr_leak_alerts=ptr_alerts,
        canonical_shield_alerts=shield_alerts,
    )
    md = generate_impact_report_markdown(report)
    assert "Embudo Nativo Comunidades Tech & PTR" in md
    assert "Alertas de Fuga de Traspaso" in md
    assert "Escudo Anti-Canibalización Canónica" in md
    assert "0.31%" in md


def test_public_json_firewall_zero_social_or_ledger_leak_inv_pulse_2_12() -> None:
    static_pulse_dir = REPO_ROOT / "static" / "apps" / "pulse"
    for p in static_pulse_dir.rglob("*"):
        assert "social_metrics" not in p.name
        assert "distribution_ledger" not in p.name
        assert "channel_metrics" not in p.name

    public_json = static_pulse_dir / "data" / "public.json"
    if public_json.is_file():
        raw = public_json.read_text(encoding="utf-8")
        for forbidden in (
            '"social_platform_summary"',
            '"ptr_leak_alerts"',
            '"canonical_shield_alerts"',
            '"distribution_ledger"',
            '"external_id"',
            '"native_views"',
        ):
            assert forbidden not in raw


def test_parse_linkedin_company_xlsx_deterministic_en_and_es(tmp_path: Path) -> None:
    """Valida el parser determinista .xlsx oficial para exportaciones en inglés y español (Hito 7.13)."""
    # 1. Fixture EN: exportación de publicaciones y seguidores
    en_dir = tmp_path / "linkedin_en"
    en_dir.mkdir(parents=True)
    en_wb = openpyxl.Workbook()
    ws_posts = en_wb.active
    ws_posts.title = "All posts"
    ws_posts.append([
        "Post title", "Post link", "Post URN", "Created date",
        "Impressions", "Clicks", "Click through rate (CTR)", "Reactions",
        "Comments", "Shares", "Engagement rate",
    ])
    ws_posts.append([
        "Deterministic SDD Architecture",
        "https://www.linkedin.com/feed/update/urn:li:share:726001/",
        "urn:li:share:726001",
        "2026-11-15",
        1250, 65, 0.052, 35, 6, 4, 0.088,
    ])
    ws_posts.append([
        "Total Summary", "", "", "", 1250, 65, 0.052, 35, 6, 4, 0.088,
    ])  # Fila de totales que debe ser ignorada

    ws_foll = en_wb.create_sheet("Followers")
    ws_foll.append(["Date", "Total followers", "Organic followers"])
    ws_foll.append(["2026-11-15", 210, 210])

    en_file = en_dir / "linkedin_content_en.xlsx"
    en_wb.save(en_file)

    ok_en, data_en = parse_linkedin_company_xlsx(folder_path=en_dir)
    assert ok_en is True
    assert data_en["status"] == "xlsx_import_ok"
    assert data_en["source"] == "xlsx"
    assert data_en["scope"] == "company_page_only"
    assert data_en["total_impressions"] == 1250
    assert data_en["total_clicks"] == 65
    assert data_en["native_ctr_pct"] == 5.2
    assert data_en["total_reactions"] == 35
    assert data_en["total_comments"] == 6
    assert data_en["total_shares"] == 4
    assert data_en["followers_count"] == 210
    assert len(data_en["posts"]) == 1
    assert data_en["posts"][0]["urn"] == "urn:li:share:726001"

    # 2. Fixture ES: exportación en español con 'Todas las publicaciones' y 'Métricas'
    es_dir = tmp_path / "linkedin_es"
    es_dir.mkdir(parents=True)
    es_wb = openpyxl.Workbook()
    ws_es = es_wb.active
    ws_es.title = "Todas las publicaciones"
    ws_es.append([
        "Título de la publicación", "Enlace de la publicación", "URN", "Fecha de creación",
        "Impresiones", "Clics", "Porcentaje de clics (CTR)", "Reacciones",
        "Comentarios", "Veces compartido", "Tasa de interacción",
    ])
    ws_es.append([
        "Arquitectura SDD en Datalaria",
        "https://www.linkedin.com/feed/update/urn:li:ugcPost:726002/",
        "urn:li:ugcPost:726002",
        "16/11/2026",
        800, 48, 0.06, 22, 5, 2, 0.095,
    ])
    ws_met = es_wb.create_sheet("Métricas")
    ws_met.append(["Métrica", "Total"])
    ws_met.append(["Seguidores totales", 175])

    es_file = es_dir / "linkedin_actualizaciones_es.xlsx"
    es_wb.save(es_file)

    ok_es, data_es = parse_linkedin_company_xlsx(folder_path=es_dir)
    assert ok_es is True
    assert data_es["total_impressions"] == 800
    assert data_es["total_clicks"] == 48
    assert data_es["followers_count"] == 175
    assert len(data_es["posts"]) == 1
    assert data_es["posts"][0]["urn"] == "urn:li:ugcPost:726002"


def test_fetch_linkedin_company_api_metrics_200_and_401_403_contracts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifica contratos de LinkedIn Community Management API (200, 401 retry, 403 fallback)."""
    # 1. Veto de seguridad: si no hay credenciales, devuelve (False, {}) de forma limpia
    assert fetch_linkedin_company_api_metrics(company_id="", access_token="tok") == (False, {})
    assert fetch_linkedin_company_api_metrics(company_id="12345", access_token="") == (False, {})

    # 2. Contrato 200 con shares agregados, por URN en ledger y seguidores
    captured_calls: List[Dict[str, Any]] = []

    def fake_get_200(url: str, headers=None, params=None, timeout=15):
        captured_calls.append({"url": url, "params": dict(params or {})})
        resp = MagicMock()
        resp.status_code = 200
        resp.raise_for_status.return_value = None
        if "organizationalEntityShareStatistics" in url:
            if params and "ugcPosts[0]" in params:
                resp.json.return_value = {
                    "elements": [
                        {
                            "totalShareStatistics": {
                                "impressionCount": 420,
                                "clickCount": 21,
                                "likeCount": 11,
                                "commentCount": 2,
                                "shareCount": 1,
                                "engagement": 0.081,
                            },
                            "ugcPost": params["ugcPosts[0]"],
                        }
                    ]
                }
            else:
                resp.json.return_value = {
                    "elements": [
                        {
                            "totalShareStatistics": {
                                "impressionCount": 1500,
                                "clickCount": 75,
                                "likeCount": 30,
                                "commentCount": 5,
                                "shareCount": 8,
                                "engagement": 0.078,
                            },
                            "share": "urn:li:share:726003",
                        }
                    ]
                }
        elif "followerStatistics" in url:
            resp.json.return_value = {
                "elements": [{"organicFollowerCount": 240, "paidFollowerCount": 0}]
            }
        else:
            resp.json.return_value = {"elements": []}
        return resp

    monkeypatch.setattr("ops.pulse.sync_social_metrics.requests.get", fake_get_200)

    ok_api, data_api = fetch_linkedin_company_api_metrics(
        company_id="12345678",
        access_token="valid_access_token",
        ledger_entries=[
            {
                "channel": "linkedin",
                "external_id": "urn:li:ugcPost:726009",
                "canonical_url": "https://datalaria.com/es/posts/sdd_post/",
            }
        ],
    )
    assert ok_api is True
    assert data_api["status"] == "api_ok"
    assert data_api["source"] == "api"
    assert data_api["scope"] == "company_page_only"
    assert data_api["company_id"] == "12345678"
    assert data_api["total_impressions"] == 1500
    assert data_api["total_clicks"] == 75
    assert data_api["native_ctr_pct"] == 5.0
    assert data_api["followers_count"] == 240
    urns_fetched = {p["urn"] for p in data_api["posts"]}
    assert urns_fetched == {"urn:li:share:726003", "urn:li:ugcPost:726009"}
    assert any("ugcPosts[0]" in c["params"] for c in captured_calls)

    # 3. Contrato 403 (Community Management API en revisión): degradación elegante sin romper
    def fake_get_403(url: str, headers=None, params=None, timeout=15):
        resp = MagicMock()
        resp.status_code = 403
        resp.text = '{"message": "Not enough permissions to access organizationalEntityShareStatistics"}'
        return resp

    monkeypatch.setattr("ops.pulse.sync_social_metrics.requests.get", fake_get_403)
    ok_403, data_403 = fetch_linkedin_company_api_metrics(
        company_id="12345678",
        access_token="token_without_scope",
    )
    assert ok_403 is False
    assert data_403 == {}

    # 4. Contrato 401 con renovación exitosa de token
    call_count = {"stats": 0}

    def fake_get_401_then_200(url: str, headers=None, params=None, timeout=15):
        resp = MagicMock()
        if "organizationalEntityShareStatistics" in url:
            call_count["stats"] += 1
            if call_count["stats"] == 1:
                resp.status_code = 401
                return resp
            resp.status_code = 200
            resp.json.return_value = {
                "elements": [
                    {
                        "totalShareStatistics": {"impressionCount": 500, "clickCount": 25},
                        "share": "urn:li:share:726004",
                    }
                ]
            }
            return resp
        resp.status_code = 200
        resp.json.return_value = {"elements": [{"organicFollowerCount": 100}]}
        return resp

    monkeypatch.setattr("ops.pulse.sync_social_metrics.requests.get", fake_get_401_then_200)
    monkeypatch.setattr(
        "ops.pulse.sync_social_metrics._refresh_linkedin_token",
        lambda cid, csec, rtok: "refreshed_access_token",
    )

    ok_refreshed, data_refreshed = fetch_linkedin_company_api_metrics(
        company_id="12345678",
        access_token="expired_token",
        refresh_token="valid_refresh",
        client_id="cid",
        client_secret="csec",
    )
    assert ok_refreshed is True
    assert data_refreshed["total_impressions"] == 500
    assert call_count["stats"] == 2


def test_linkedin_company_consolidation_priority_api_over_xlsx_over_snapshot(
    tmp_path: Path,
) -> None:
    """Valida la prioridad API > XLSX > snapshot previo y el emparejamiento con el Ledger (Hito 7.13)."""
    assets = [
        {
            "id": "sdd_post",
            "slug": "sdd_post",
            "url_es": "/es/posts/sdd_post/",
            "url_en": "/en/posts/sdd_post/",
        }
    ]
    ledger_file = tmp_path / "distribution_ledger.json"
    record_distribution_ledger_entry(
        asset_id="sdd_post",
        slug="sdd_post",
        lang="es",
        channel="linkedin",
        external_id="urn:li:share:726001",
        external_url="https://www.linkedin.com/feed/update/urn:li:share:726001/",
        canonical_url="https://datalaria.com/es/posts/sdd_post/",
        published_at_utc="2026-11-15T12:00:00Z",
        ledger_path=ledger_file,
    )

    # 1. API fresca presente -> gana API
    api_payload = {
        "status": "api_ok",
        "source": "api",
        "scope": "company_page_only",
        "company_id": "12345",
        "total_impressions": 2000,
        "total_clicks": 100,
        "native_ctr_pct": 5.0,
        "total_reactions": 50,
        "total_comments": 10,
        "total_shares": 5,
        "followers_count": 300,
        "posts": [
            {
                "urn": "urn:li:share:726001",
                "impressions": 2000,
                "clicks": 100,
                "reactions": 50,
                "comments": 10,
                "shares": 5,
            }
        ],
    }

    first = consolidate_social_metrics(
        assets=assets,
        devto_articles=[],
        devto_ok=False,
        coderlegion_posts=[],
        coderlegion_ok=False,
        linkedin_company_data=api_payload,
        linkedin_company_ok=True,
        ledger_path=ledger_file,
        dry_run=False,
    )
    assert first["platforms"]["linkedin_company"]["source"] == "api"
    assert first["platforms"]["linkedin_company"]["total_impressions"] == 2000
    assert first["platforms"]["linkedin_company"]["followers_count"] == 300
    assert first["by_asset"]["sdd_post"]["linkedin_company"]["impressions"] == 2000
    assert first["by_asset"]["sdd_post"]["linkedin_company"]["views"] == 2000

    # 2. Si la API falla (HTTP 403), pero entra una exportación .xlsx fresca con 2500 impresiones:
    xlsx_payload = {
        "status": "xlsx_import_ok",
        "source": "xlsx",
        "scope": "company_page_only",
        "file_name": "backup.xlsx",
        "total_impressions": 2500,
        "total_clicks": 125,
        "native_ctr_pct": 5.0,
        "total_reactions": 60,
        "total_comments": 12,
        "total_shares": 6,
        "followers_count": 320,
        "posts": [
            {
                "urn": "urn:li:share:726001",
                "impressions": 2500,
                "clicks": 125,
                "reactions": 60,
                "comments": 12,
                "shares": 6,
            }
        ],
    }

    second = consolidate_social_metrics(
        assets=assets,
        devto_articles=[],
        devto_ok=False,
        coderlegion_posts=[],
        coderlegion_ok=False,
        linkedin_company_data=xlsx_payload,
        linkedin_company_ok=True,
        existing_social_metrics=first,
        ledger_path=ledger_file,
        dry_run=True,
    )
    assert second["platforms"]["linkedin_company"]["source"] == "xlsx"
    assert second["platforms"]["linkedin_company"]["total_impressions"] == 2500
    assert second["by_asset"]["sdd_post"]["linkedin_company"]["impressions"] == 2500

    # 3. Si tanto API como XLSX fallan, se preserva el snapshot previo sin sobrescribir a 0 (INV-PULSE-11/12)
    third = consolidate_social_metrics(
        assets=assets,
        devto_articles=[],
        devto_ok=False,
        coderlegion_posts=[],
        coderlegion_ok=False,
        linkedin_company_data={},
        linkedin_company_ok=False,
        existing_social_metrics=second,
        ledger_path=ledger_file,
        dry_run=True,
    )
    assert third["platforms"]["linkedin_company"]["total_impressions"] == 2500
    assert third["platforms"]["linkedin_company"]["followers_count"] == 320
    assert third["by_asset"]["sdd_post"]["linkedin_company"]["impressions"] == 2500


def test_x_twitter_explicit_standby_zero_cost_contract() -> None:
    """Verifica que X/Twitter permanezca inequívocamente en standby_zero_cost (ADR-033 / INV-PULSE-12)."""
    res = consolidate_social_metrics(
        assets=[],
        devto_articles=[],
        devto_ok=False,
        coderlegion_posts=[],
        coderlegion_ok=False,
    )
    x_plat = res["platforms"]["x"]
    assert x_plat["status"] == "standby_zero_cost"
    assert x_plat["last_synced_at"] is None
    assert "GA4 + UTMs" in x_plat["note"]
    assert "coste 0 EUR" in x_plat["note"]


def test_impact_report_markdown_renders_linkedin_company_and_x_standby() -> None:
    """Verifica la generación del reporte Markdown con LinkedIn Empresa y nota de X (Hito 7.13)."""
    plat_summary = {
        "devto": {
            "platform": "devto",
            "status": "ok",
            "articles_count": 5,
            "matched_assets_count": 5,
            "native_views": 8000,
            "native_reactions": 210,
            "native_comments": 35,
            "ga4_sessions_30d": 120,
            "ptr_pct": 1.5,
        },
        "coderlegion": {
            "platform": "coderlegion",
            "status": "ok",
            "articles_count": 2,
            "matched_assets_count": 2,
            "native_views": 2500,
            "native_reactions": 45,
            "native_comments": 8,
            "ga4_sessions_30d": 40,
            "ptr_pct": 1.6,
        },
        "linkedin_company": {
            "platform": "linkedin_company",
            "status": "api_ok",
            "source": "api",
            "posts_count": 3,
            "matched_assets_count": 3,
            "total_impressions": 2450,
            "total_clicks": 120,
            "native_ctr_pct": 4.9,
            "total_reactions": 65,
            "total_comments": 8,
            "followers_count": 160,
            "ga4_sessions_30d": 95,
            "ptr_pct": 3.88,
        },
        "x": {
            "platform": "x",
            "status": "standby_zero_cost",
            "ga4_sessions_30d": 35,
            "note": "Medición activa vía GA4 + UTMs (Hito 7.11); API nativa X en stand-by por coste > 0 EUR",
        },
    }

    report = PulseImpactReport(
        generated_at=datetime.now(timezone.utc),
        total_published_posts=3,
        total_scheduled_posts=0,
        total_30d_post_views=500,
        median_post_views=150.0,
        p75_post_views=200.0,
        monthly_growth_yoy_pct=15.0,
        category_performance=[],
        quick_wins_ctr=[],
        monetization_orphans=[],
        decay_alerts=[],
        prioritized_backlog=[],
        social_platform_summary=plat_summary,
    )
    md = generate_impact_report_markdown(report)
    assert "linkedin_company" in md
    assert "2,450" in md
    assert "120 (4.9%)" in md
    assert "3.88%" in md
    assert "160 seguidores" in md
    assert "standby_zero_cost" in md
    assert "Solo GA4+UTM" in md


def test_sync_all_social_metrics_api_403_falls_back_to_xlsx_end_to_end(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End-to-end offline: si LinkedIn API da 403, conmuta limpiamente al Carril B (.xlsx) sin romper el pipeline."""
    index_file = tmp_path / "index.json"
    index_file.write_text(
        json.dumps([
            {
                "id": "sdd_post",
                "slug": "sdd_post",
                "url_es": "/es/posts/sdd_post/",
                "url_en": "/en/posts/sdd_post/",
            }
        ]),
        encoding="utf-8",
    )
    ledger_file = tmp_path / "distribution_ledger.json"
    record_distribution_ledger_entry(
        asset_id="sdd_post",
        slug="sdd_post",
        lang="es",
        channel="linkedin",
        external_id="urn:li:share:999001",
        external_url="https://www.linkedin.com/feed/update/urn:li:share:999001/",
        canonical_url="https://datalaria.com/es/posts/sdd_post/",
        published_at_utc="2026-11-20T10:00:00Z",
        ledger_path=ledger_file,
    )

    imports_dir = tmp_path / "imports_linkedin"
    imports_dir.mkdir(parents=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Todas las publicaciones"
    ws.append(["Título", "URN", "Impresiones", "Clics", "Reacciones", "Comentarios"])
    ws.append(["Post SDD en LinkedIn", "urn:li:share:999001", 950, 57, 29, 4])
    ws_f = wb.create_sheet("Seguidores")
    ws_f.append(["Fecha", "Total de seguidores"])
    ws_f.append(["2026-11-20", 188])
    wb.save(imports_dir / "company_export.xlsx")

    def fake_403_get(url: str, headers=None, params=None, timeout=15):
        resp = MagicMock()
        resp.status_code = 403
        resp.text = '{"message":"ACCESS_DENIED"}'
        return resp

    monkeypatch.setattr("ops.pulse.sync_social_metrics.requests.get", fake_403_get)
    monkeypatch.delenv("DEVTO_API_KEY", raising=False)
    monkeypatch.delenv("CODERLEGION_API_KEY", raising=False)
    monkeypatch.setenv("LINKEDIN_COMPANY_ID", "12345")
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "valid-tok")

    out_file = tmp_path / "social_metrics.json"
    res = sync_all_social_metrics(
        dry_run=False,
        index_path=index_file,
        ledger_path=ledger_file,
        output_path=out_file,
        imports_linkedin_dir=imports_dir,
    )

    assert out_file.is_file()
    li = res["platforms"]["linkedin_company"]
    assert li["status"] == "xlsx_import_ok"
    assert li["source"] == "xlsx"
    assert li["total_impressions"] == 950
    assert li["total_clicks"] == 57
    assert li["followers_count"] == 188
    assert res["by_asset"]["sdd_post"]["linkedin_company"]["impressions"] == 950
    assert res["platforms"]["x"]["status"] == "standby_zero_cost"


