"""
ops/pulse/sync_metrics.py
-------------------------
Módulo de Sincronización y Enriquecimiento Cuantitativo de Métricas (GA4 + Search Console).
Especificación técnica formal: SPEC-APP-PULSE v1.4.0 (specs/apps/pulse/spec.md) - Hito 7.7.

Responsabilidades:
1. Extraer métricas de visitas (actual 30d y ventana previa 30d), usuarios y engagement
   de Google Analytics 4 (Data API) por ruta canónica normalizada.
2. Extraer métricas paginadas de Google Search Console (Search Analytics API) para:
   - Páginas (`["page"]`) con agregación segura sin sobreescritura y posición ponderada por impresiones.
   - Consultas por página (`["page", "query"]`) persistidas en `data/pulse/private/gsc_queries.json`.
   - Serie mensual histórica (`["date"]`) fusionada en `data/pulse/private/monthly_metrics.json`.
3. Auto-detectar propiedad GSC verificada vía `sites().list()` y validar en modo CLI `--check-gsc` / `--strict-gsc`.
4. Degradación elegante desacoplada (`INV-PULSE-11`): un fallo en GSC nunca borra métricas previas de GSC
   cuando GA4 sí responde, ni viceversa.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple
from urllib.parse import urlsplit

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "metrics.json"
MONTHLY_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "monthly_metrics.json"
GSC_QUERIES_PATH = ROOT_DIR / "data" / "pulse" / "private" / "gsc_queries.json"
CHANNEL_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "channel_metrics.json"
INDEX_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
CREDENTIALS_FILE = ROOT_DIR / "service_account.json"
DEFAULT_PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID", "367847195")
DEFAULT_GSC_SITE = os.environ.get("GSC_SITE_URL", "sc-domain:datalaria.com")

CANONICAL_CHANNELS: Tuple[str, ...] = (
    "google_organic",
    "linkedin",
    "devto",
    "coderlegion",
    "x",
    "newsletter",
    "direct",
    "other",
)

KEY_CONVERSION_EVENTS = frozenset({
    "join_waitlist_helix",
    "home_pack_click",
    "pack_click",
    "kit_checkout_click",
    "lemon_squeezy_click",
    "resource_cta_click",
    "cta_click",
    "checkout_click",
    "select_item",
    "begin_checkout",
    "generate_lead",
})

_BRAND_QUERY_RE = re.compile(r"\bdatalaria\b|datalaria", re.IGNORECASE)


def classify_canonical_channel(source: Optional[str], medium: Optional[str] = "") -> Literal[
    "linkedin", "x", "devto", "coderlegion", "newsletter", "google_organic", "direct", "other"
]:
    """Normaliza cualquier combinación (sessionSource, sessionMedium) a su canal canónico (ADR-033)."""
    s = str(source or "").strip().lower()
    m = str(medium or "").strip().lower()

    if "linkedin" in s or "lnkd.in" in s:
        return "linkedin"
    if s in ("x", "twitter", "t.co", "x.com", "twitter.com", "mobile.twitter.com", "m.twitter.com") or s.endswith(
        (".twitter.com", ".x.com")
    ):
        return "x"
    if s in ("devto", "dev.to", "www.dev.to") or "dev.to" in s or s == "forem":
        return "devto"
    if "coderlegion" in s:
        return "coderlegion"
    if s in ("newsletter", "brevo", "sendinblue") or "brevo" in s or m == "email":
        return "newsletter"
    if "google" in s and m == "organic":
        return "google_organic"
    if s in ("(direct)", "direct", "") and m in ("(none)", "none", ""):
        return "direct"
    return "other"


def is_brand_query(query: Optional[str]) -> bool:
    """Devuelve True si la consulta de Search Console contiene términos de marca Datalaria."""
    if not query:
        return False
    return bool(_BRAND_QUERY_RE.search(str(query).strip()))


def is_key_conversion_event(event_name: Optional[str], norm_path: str = "") -> bool:
    """Determina si un evento GA4 corresponde a una conversión o intención comercial de Datalaria."""
    ev = str(event_name or "").strip().lower()
    if not ev:
        return False
    if ev in KEY_CONVERSION_EVENTS:
        return True
    if any(token in ev for token in ("waitlist", "checkout", "pack_click", "kit_click", "lemon")):
        return True
    if ev in ("click", "select_content") and (
        norm_path.startswith("/es/recursos") or norm_path.startswith("/en/resources")
    ):
        return True
    return False


def _configure_utf8_stdio() -> None:
    """Evita errores cp1252/charmap en consola Windows al imprimir emojis o caracteres UTF-8."""
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if callable(reconf):
            try:
                reconf(encoding="utf-8", errors="replace")
            except Exception:
                pass


def normalize_url_path(raw_url: Optional[str]) -> str:
    """
    Normaliza una URL completa o ruta relativa al path canónico sin query ni fragmento.
    Home se normaliza a '/'; el resto elimina slash final. Cadenas vacías devuelven ''.
    """
    if not raw_url:
        return ""
    text = str(raw_url).strip()
    if not text:
        return ""
    parsed = urlsplit(text)
    path = parsed.path or "/"
    if not path.startswith("/"):
        path = "/" + path
    if path != "/":
        path = path.rstrip("/") or "/"
    return path


def detect_url_lang(norm_path: str) -> Literal["es", "en", "other"]:
    """Detecta el idioma de una ruta normalizada (/es/... -> 'es', /en/... -> 'en')."""
    if norm_path == "/es" or norm_path.startswith("/es/"):
        return "es"
    if norm_path == "/en" or norm_path.startswith("/en/"):
        return "en"
    return "other"


def _resolve_credentials_path() -> Optional[Path]:
    env_cred = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    if env_cred and Path(env_cred).is_file():
        return Path(env_cred)
    if CREDENTIALS_FILE.is_file():
        return CREDENTIALS_FILE
    return None


def _build_gsc_service() -> Optional[Any]:
    cred_path = _resolve_credentials_path()
    if cred_path is None:
        return None
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        str(cred_path),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
    )
    return build("searchconsole", "v1", credentials=creds)


def resolve_gsc_site_url(service: Any, preferred: Optional[str] = None) -> Optional[str]:
    """
    Auto-detecta la propiedad GSC verificada consultando `service.sites().list()`.
    Prioriza `preferred` / `GSC_SITE_URL`, luego `sc-domain:datalaria.com` y `https://datalaria.com/`.
    """
    resp = service.sites().list().execute()
    entries = resp.get("siteEntry", []) or []
    accessible = [e.get("siteUrl", "") for e in entries if e.get("siteUrl")]
    if not accessible:
        return None

    env_site = os.environ.get("GSC_SITE_URL", "").strip()
    candidates = [
        preferred,
        env_site,
        DEFAULT_GSC_SITE,
        "sc-domain:datalaria.com",
        "https://datalaria.com/",
    ]
    for cand in candidates:
        if cand and cand in accessible:
            return cand

    for site in accessible:
        if "datalaria.com" in site:
            return site
    return accessible[0]


def aggregate_gsc_page_rows(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Agrega filas crudas de Search Console (`dimensions=["page"]`) por ruta normalizada.
    Suma `clicks` e `impressions` y calcula `position` ponderada por impresiones.
    """
    buckets: Dict[str, Dict[str, float]] = {}

    for r in rows:
        keys = r.get("keys") or []
        if not keys:
            continue
        path_part = normalize_url_path(keys[0])
        if not path_part:
            continue

        clicks = int(r.get("clicks", 0) or 0)
        impr = int(r.get("impressions", 0) or 0)
        pos = float(r.get("position", 0.0) or 0.0)

        b = buckets.setdefault(
            path_part,
            {"clicks": 0, "impressions": 0, "weighted_pos_sum": 0.0, "pos_sum": 0.0, "count": 0},
        )
        b["clicks"] += clicks
        b["impressions"] += impr
        if impr > 0 and pos > 0:
            b["weighted_pos_sum"] += pos * impr
        if pos > 0:
            b["pos_sum"] += pos
            b["count"] += 1

    aggregated: Dict[str, Dict[str, Any]] = {}
    for path_part, b in buckets.items():
        tot_clicks = int(b["clicks"])
        tot_impr = int(b["impressions"])
        if tot_impr > 0 and b["weighted_pos_sum"] > 0:
            avg_pos = b["weighted_pos_sum"] / tot_impr
        elif b["count"] > 0:
            avg_pos = b["pos_sum"] / b["count"]
        else:
            avg_pos = 0.0
        ctr_pct = (tot_clicks / tot_impr * 100.0) if tot_impr > 0 else 0.0

        aggregated[path_part] = {
            "clicks": tot_clicks,
            "impressions": tot_impr,
            "ctr_pct": round(ctr_pct, 4),
            "position": round(avg_pos, 4),
        }

    return aggregated


def aggregate_gsc_page_query_rows(
    rows: List[Dict[str, Any]],
    max_rows: int = 10000,
) -> Tuple[Dict[str, List[Dict[str, Any]]], List[Dict[str, Any]]]:
    """
    Agrega filas `["page", "query"]` por `(path_normalizado, query)`.
    Retorna `(by_page, global_top_queries)`.
    """
    pair_buckets: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for r in rows:
        keys = r.get("keys") or []
        if len(keys) < 2:
            continue
        path_part = normalize_url_path(keys[0])
        query_str = str(keys[1]).strip()
        if not path_part or not query_str:
            continue

        clicks = int(r.get("clicks", 0) or 0)
        impr = int(r.get("impressions", 0) or 0)
        pos = float(r.get("position", 0.0) or 0.0)

        pkey = (path_part, query_str)
        b = pair_buckets.setdefault(
            pkey,
            {"clicks": 0, "impressions": 0, "weighted_pos_sum": 0.0, "pos_sum": 0.0, "count": 0},
        )
        b["clicks"] += clicks
        b["impressions"] += impr
        if impr > 0 and pos > 0:
            b["weighted_pos_sum"] += pos * impr
        if pos > 0:
            b["pos_sum"] += pos
            b["count"] += 1

    records: List[Dict[str, Any]] = []
    for (path_part, query_str), b in pair_buckets.items():
        tot_clicks = int(b["clicks"])
        tot_impr = int(b["impressions"])
        if tot_impr > 0 and b["weighted_pos_sum"] > 0:
            avg_pos = b["weighted_pos_sum"] / tot_impr
        elif b["count"] > 0:
            avg_pos = b["pos_sum"] / b["count"]
        else:
            avg_pos = 0.0
        ctr_pct = (tot_clicks / tot_impr * 100.0) if tot_impr > 0 else 0.0

        records.append({
            "path": path_part,
            "query": query_str,
            "lang": detect_url_lang(path_part),
            "clicks": tot_clicks,
            "impressions": tot_impr,
            "ctr_pct": round(ctr_pct, 2),
            "position": round(avg_pos, 1),
            "is_brand_query": is_brand_query(query_str),
        })

    records.sort(key=lambda x: (x["impressions"], x["clicks"]), reverse=True)
    if max_rows > 0:
        records = records[:max_rows]

    by_page: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for rec in records:
        by_page[rec["path"]].append({
            "query": rec["query"],
            "lang": rec["lang"],
            "clicks": rec["clicks"],
            "impressions": rec["impressions"],
            "ctr_pct": rec["ctr_pct"],
            "position": rec["position"],
            "is_brand_query": rec["is_brand_query"],
        })

    return dict(by_page), records


def _query_gsc_paginated(
    service: Any,
    site_url: str,
    start_date: date,
    end_date: date,
    dimensions: List[str],
    page_size: int = 5000,
    max_rows: int = 25000,
) -> List[Dict[str, Any]]:
    """Ejecuta consultas paginadas contra Search Console API (`rowLimit` hasta 5.000 por página)."""
    all_rows: List[Dict[str, Any]] = []
    start_row = 0

    while start_row < max_rows:
        batch_limit = min(page_size, max_rows - start_row, 25000)
        request_body = {
            "startDate": str(start_date),
            "endDate": str(end_date),
            "dimensions": dimensions,
            "rowLimit": batch_limit,
            "startRow": start_row,
        }
        resp = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
        rows = resp.get("rows", []) or []
        if not rows:
            break
        all_rows.extend(rows)
        if len(rows) < batch_limit:
            break
        start_row += len(rows)

    return all_rows


def _fetch_ga4_range(client: Any, start_date: str, end_date: str) -> Dict[str, Dict[str, Any]]:
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        OrderBy,
        RunReportRequest,
    )

    request = RunReportRequest(
        property=f"properties/{DEFAULT_PROPERTY_ID}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="screenPageViews"),
            Metric(name="totalUsers"),
            Metric(name="userEngagementDuration"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
        limit=2000,
    )
    response = client.run_report(request)
    path_metrics: Dict[str, Dict[str, Any]] = {}

    for row in response.rows:
        raw_path = row.dimension_values[0].value.strip()
        norm_path = normalize_url_path(raw_path)
        if not norm_path:
            continue
        views = int(row.metric_values[0].value)
        users = int(row.metric_values[1].value)
        duration = float(row.metric_values[2].value)

        bucket = path_metrics.setdefault(
            norm_path,
            {"views": 0, "users": 0, "engagement_sec": 0.0},
        )
        bucket["views"] += views
        bucket["users"] += users
        bucket["engagement_sec"] += duration

    return path_metrics


def fetch_ga4_metrics(days: int = 30) -> Dict[str, Dict[str, Any]]:
    """
    Consulta GA4 Data API para la ventana actual (`days` días) y la ventana previa (`2*days .. days+1`).
    Retorna `{ path_normalizado: { views, users, engagement_sec, views_prev } }`.
    """
    cred_path = _resolve_credentials_path()
    if cred_path is None:
        print(f"[WARN] No se encontró service_account.json en {CREDENTIALS_FILE}. Saltando llamada real a GA4.")
        return {}

    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_path)
        client = BetaAnalyticsDataClient()

        current_map = _fetch_ga4_range(client, f"{days}daysAgo", "today")
        prev_map: Dict[str, Dict[str, Any]] = {}
        try:
            prev_map = _fetch_ga4_range(client, f"{days * 2}daysAgo", f"{days + 1}daysAgo")
        except Exception as prev_err:
            print(f"[WARN] Error al consultar ventana previa GA4 ({days*2}d..{days+1}d): {prev_err}")

        for p, prev_vals in prev_map.items():
            if p in current_map:
                current_map[p]["views_prev"] = prev_vals.get("views", 0)
            else:
                current_map[p] = {
                    "views": 0,
                    "users": 0,
                    "engagement_sec": 0.0,
                    "views_prev": prev_vals.get("views", 0),
                }

        for vals in current_map.values():
            vals.setdefault("views_prev", 0)

        print(f"[GA4] Extraídas métricas para {len(current_map)} rutas (incluyendo ventana previa {days}d).")
        return current_map

    except Exception as e:
        print(f"[WARN] Error al consultar GA4: {e}")
        return {}


def fetch_monthly_ga4_summary(months: int = 14) -> List[Dict[str, Any]]:
    """Consulta los totales agregados mensuales en GA4 para la serie temporal histórica."""
    cred_path = _resolve_credentials_path()
    if cred_path is None:
        return []
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, OrderBy, RunReportRequest

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_path)
        client = BetaAnalyticsDataClient()
        request = RunReportRequest(
            property=f"properties/{DEFAULT_PROPERTY_ID}",
            dimensions=[Dimension(name="yearMonth")],
            metrics=[Metric(name="screenPageViews"), Metric(name="totalUsers")],
            date_ranges=[DateRange(start_date=f"{months * 30}daysAgo", end_date="today")],
            order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="yearMonth"), desc=False)],
        )
        response = client.run_report(request)
        monthly_data = []
        for row in response.rows:
            ym = row.dimension_values[0].value
            if len(ym) == 6:
                formatted_m = f"{ym[:4]}-{ym[4:]}"
                monthly_data.append({
                    "year_month": ym,
                    "month": formatted_m,
                    "views": int(row.metric_values[0].value),
                    "users": int(row.metric_values[1].value),
                })
        print(f"[GA4] Extraído histórico mensual para {len(monthly_data)} meses.")
        return monthly_data
    except Exception as e:
        print(f"[WARN] Error al consultar histórico mensual GA4: {e}")
        return []


def fetch_ga4_acquisition_metrics(days: int = 30) -> Dict[str, Any]:
    """
    Consulta GA4 Data API para atribución por canal, eventos clave y serie diaria (ADR-033).
    Devuelve diccionario vacío si no hay credenciales o falla la red (INV-PULSE-11/12).
    """
    cred_path = _resolve_credentials_path()
    if cred_path is None:
        print(f"[WARN] No se encontró service_account.json en {CREDENTIALS_FILE}. Saltando GA4 Acquisition.")
        return {}

    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Metric,
            OrderBy,
            RunReportRequest,
        )

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_path)
        client = BetaAnalyticsDataClient()

        # 1. Adquisición por página × fuente × medio × campaña (actual)
        acq_req = RunReportRequest(
            property=f"properties/{DEFAULT_PROPERTY_ID}",
            dimensions=[
                Dimension(name="pagePath"),
                Dimension(name="sessionSource"),
                Dimension(name="sessionMedium"),
                Dimension(name="sessionCampaignName"),
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="engagedSessions"),
                Metric(name="userEngagementDuration"),
            ],
            date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=5000,
        )
        acq_resp = client.run_report(acq_req)
        current_rows: List[Dict[str, Any]] = []
        for row in acq_resp.rows:
            norm_path = normalize_url_path(row.dimension_values[0].value)
            if not norm_path:
                continue
            current_rows.append({
                "path": norm_path,
                "source": row.dimension_values[1].value.strip(),
                "medium": row.dimension_values[2].value.strip(),
                "campaign": row.dimension_values[3].value.strip(),
                "sessions": int(row.metric_values[0].value or 0),
                "users": int(row.metric_values[1].value or 0),
                "engaged_sessions": int(row.metric_values[2].value or 0),
                "engagement_sec": float(row.metric_values[3].value or 0.0),
            })

        # 2. Ventana previa por fuente × medio (para tendencia 30d y baseline Dark Social)
        prev_rows: List[Dict[str, Any]] = []
        try:
            prev_req = RunReportRequest(
                property=f"properties/{DEFAULT_PROPERTY_ID}",
                dimensions=[
                    Dimension(name="sessionSource"),
                    Dimension(name="sessionMedium"),
                ],
                metrics=[
                    Metric(name="sessions"),
                    Metric(name="totalUsers"),
                    Metric(name="engagedSessions"),
                ],
                date_ranges=[DateRange(start_date=f"{days * 2}daysAgo", end_date=f"{days + 1}daysAgo")],
                limit=1000,
            )
            prev_resp = client.run_report(prev_req)
            for row in prev_resp.rows:
                prev_rows.append({
                    "source": row.dimension_values[0].value.strip(),
                    "medium": row.dimension_values[1].value.strip(),
                    "sessions": int(row.metric_values[0].value or 0),
                    "users": int(row.metric_values[1].value or 0),
                    "engaged_sessions": int(row.metric_values[2].value or 0),
                })
        except Exception as prev_err:
            print(f"[WARN] Error al consultar ventana previa GA4 Acquisition: {prev_err}")

        # 3. Eventos clave por página × fuente × medio
        event_rows: List[Dict[str, Any]] = []
        try:
            ev_req = RunReportRequest(
                property=f"properties/{DEFAULT_PROPERTY_ID}",
                dimensions=[
                    Dimension(name="pagePath"),
                    Dimension(name="sessionSource"),
                    Dimension(name="sessionMedium"),
                    Dimension(name="eventName"),
                ],
                metrics=[Metric(name="eventCount")],
                date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
                order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="eventCount"), desc=True)],
                limit=5000,
            )
            ev_resp = client.run_report(ev_req)
            for row in ev_resp.rows:
                norm_path = normalize_url_path(row.dimension_values[0].value)
                ev_name = row.dimension_values[3].value.strip()
                if not norm_path or not is_key_conversion_event(ev_name, norm_path):
                    continue
                event_rows.append({
                    "path": norm_path,
                    "source": row.dimension_values[1].value.strip(),
                    "medium": row.dimension_values[2].value.strip(),
                    "event_name": ev_name,
                    "count": int(row.metric_values[0].value or 0),
                })
        except Exception as ev_err:
            print(f"[WARN] Error al consultar eventos clave GA4 Acquisition: {ev_err}")

        # 4. Serie diaria por fuente × medio (para detección de picos Dark Social 48h)
        daily_rows: List[Dict[str, Any]] = []
        try:
            daily_req = RunReportRequest(
                property=f"properties/{DEFAULT_PROPERTY_ID}",
                dimensions=[
                    Dimension(name="date"),
                    Dimension(name="sessionSource"),
                    Dimension(name="sessionMedium"),
                ],
                metrics=[Metric(name="sessions")],
                date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
                order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"), desc=False)],
                limit=5000,
            )
            daily_resp = client.run_report(daily_req)
            for row in daily_resp.rows:
                raw_d = row.dimension_values[0].value.strip()
                iso_d = f"{raw_d[:4]}-{raw_d[4:6]}-{raw_d[6:8]}" if len(raw_d) == 8 else raw_d
                daily_rows.append({
                    "date": iso_d,
                    "source": row.dimension_values[1].value.strip(),
                    "medium": row.dimension_values[2].value.strip(),
                    "sessions": int(row.metric_values[0].value or 0),
                })
        except Exception as daily_err:
            print(f"[WARN] Error al consultar serie diaria GA4 Acquisition: {daily_err}")

        print(
            f"[GA4-ACQ] Extraídas {len(current_rows)} filas de adquisición, "
            f"{len(event_rows)} filas de eventos clave y {len(daily_rows)} filas diarias."
        )
        return {
            "current_rows": current_rows,
            "prev_rows": prev_rows,
            "event_rows": event_rows,
            "daily_rows": daily_rows,
        }

    except Exception as exc:
        print(f"[WARN] Error al consultar GA4 Acquisition: {exc}")
        return {}


def fetch_gsc_metrics(
    days: int = 30,
    service: Optional[Any] = None,
    site_url: Optional[str] = None,
    offset_days: int = 0,
) -> Dict[str, Dict[str, Any]]:
    """
    Consulta Google Search Console Search Analytics API (`dimensions=["page"]`) con paginación completa.
    Con `offset_days=30` consulta la ventana previa (`60d..31d`) para medir GSC Lift (ADR-033).
    Retorna `{ url_path: { clicks, impressions, ctr_pct, position } }`.
    """
    try:
        svc = service or _build_gsc_service()
        if svc is None:
            print("[WARN] No se encontró service_account.json. Saltando llamada real a GSC.")
            return {}

        target_site = site_url or resolve_gsc_site_url(svc)
        if not target_site:
            print("[WARN] Ninguna propiedad GSC accesible para la Service Account.")
            return {}

        end_d = date.today() - timedelta(days=2 + max(0, int(offset_days)))
        start_d = end_d - timedelta(days=days)

        rows = _query_gsc_paginated(
            svc,
            target_site,
            start_d,
            end_d,
            dimensions=["page"],
            page_size=5000,
            max_rows=25000,
        )
        gsc_metrics = aggregate_gsc_page_rows(rows)
        window_label = f"prev-{days}d" if offset_days > 0 else f"{days}d"
        print(
            f"[GSC] Extraídas métricas ({target_site}, {window_label}) para "
            f"{len(gsc_metrics)} rutas normalizadas ({len(rows)} filas)."
        )
        return gsc_metrics

    except Exception as e:
        print(f"[WARN] No se pudo consultar Search Console (o cuenta sin permisos delegados): {e}")
        return {}


def fetch_gsc_page_queries(
    days: int = 30,
    max_rows: int = 10000,
    service: Optional[Any] = None,
    site_url: Optional[str] = None,
) -> Tuple[Dict[str, List[Dict[str, Any]]], List[Dict[str, Any]]]:
    """
    Extrae consultas por página (`dimensions=["page", "query"]`, máx. `max_rows` ordenadas por impresiones).
    Retorna `(by_page, ordered_records)`.
    """
    try:
        svc = service or _build_gsc_service()
        if svc is None:
            return {}, []

        target_site = site_url or resolve_gsc_site_url(svc)
        if not target_site:
            return {}, []

        end_d = date.today() - timedelta(days=2)
        start_d = end_d - timedelta(days=days)

        rows = _query_gsc_paginated(
            svc,
            target_site,
            start_d,
            end_d,
            dimensions=["page", "query"],
            page_size=5000,
            max_rows=max_rows,
        )
        by_page, ordered_records = aggregate_gsc_page_query_rows(rows, max_rows=max_rows)
        print(f"[GSC] Extraídas {len(ordered_records)} combinaciones página+consulta ({len(by_page)} páginas).")
        return by_page, ordered_records

    except Exception as e:
        print(f"[WARN] Error al consultar queries GSC: {e}")
        return {}, []


def fetch_gsc_monthly_summary(
    months: int = 14,
    service: Optional[Any] = None,
    site_url: Optional[str] = None,
) -> Dict[str, Dict[str, int]]:
    """
    Extrae serie diaria de GSC (`dimensions=["date"]`) y agrega `gsc_clicks` / `gsc_impressions` por `YYYY-MM`.
    """
    try:
        svc = service or _build_gsc_service()
        if svc is None:
            return {}

        target_site = site_url or resolve_gsc_site_url(svc)
        if not target_site:
            return {}

        end_d = date.today() - timedelta(days=2)
        start_d = end_d - timedelta(days=months * 31)

        rows = _query_gsc_paginated(
            svc,
            target_site,
            start_d,
            end_d,
            dimensions=["date"],
            page_size=5000,
            max_rows=5000,
        )
        monthly: Dict[str, Dict[str, int]] = {}
        for r in rows:
            keys = r.get("keys") or []
            if not keys:
                continue
            ym_str = str(keys[0])[:7]
            if len(ym_str) != 7:
                continue
            b = monthly.setdefault(ym_str, {"gsc_clicks": 0, "gsc_impressions": 0})
            b["gsc_clicks"] += int(r.get("clicks", 0) or 0)
            b["gsc_impressions"] += int(r.get("impressions", 0) or 0)

        print(f"[GSC] Extraído histórico mensual GSC para {len(monthly)} meses.")
        return monthly

    except Exception as e:
        print(f"[WARN] Error al consultar histórico mensual GSC: {e}")
        return {}


def consolidate_asset_metrics(
    assets: List[Dict[str, Any]],
    ga4_data: Dict[str, Dict[str, Any]],
    gsc_data: Dict[str, Dict[str, Any]],
    gsc_by_page: Dict[str, List[Dict[str, Any]]],
    existing_metrics: Optional[Dict[str, Dict[str, Any]]] = None,
    ga4_ok: Optional[bool] = None,
    gsc_ok: Optional[bool] = None,
    gsc_prev_data: Optional[Dict[str, Dict[str, Any]]] = None,
    gsc_prev_ok: Optional[bool] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Consolida métricas GA4 y GSC por activo con desglose bilingüe ES/EN, ventana previa GSC (60d..31d),
    posición ponderada por impresiones y fallback estrictamente desacoplado (`INV-PULSE-11`).
    """
    prev_map = existing_metrics or {}
    use_ga4 = bool(ga4_data) if ga4_ok is None else ga4_ok
    use_gsc = bool(gsc_data) if gsc_ok is None else gsc_ok
    gsc_prev_map = gsc_prev_data or {}
    use_gsc_prev = bool(gsc_prev_map) if gsc_prev_ok is None else gsc_prev_ok

    consolidated: Dict[str, Dict[str, Any]] = {}

    for asset in assets:
        aid = asset["id"]
        norm_es = normalize_url_path(asset.get("url_es"))
        norm_en = normalize_url_path(asset.get("url_en"))
        prev = prev_map.get(aid, {})

        # --- Bloque GA4 ---
        if use_ga4:
            m_es = ga4_data.get(norm_es, {}) if norm_es else {}
            m_en = ga4_data.get(norm_en, {}) if (norm_en and norm_en != norm_es) else {}

            views_es = int(m_es.get("views", 0) or 0)
            views_en = int(m_en.get("views", 0) or 0)
            total_views = views_es + views_en
            total_users = int(m_es.get("users", 0) or 0) + int(m_en.get("users", 0) or 0)
            total_eng = float(m_es.get("engagement_sec", 0.0) or 0.0) + float(m_en.get("engagement_sec", 0.0) or 0.0)
            views_prev = int(m_es.get("views_prev", 0) or 0) + int(m_en.get("views_prev", 0) or 0)
        else:
            total_views = int(prev.get("ga4_views_30d", 0) or 0)
            total_users = int(prev.get("ga4_users_30d", 0) or 0)
            total_eng = float(prev.get("ga4_engagement_sec", 0.0) or 0.0)
            views_es = int(prev.get("ga4_views_es_30d", 0) or 0)
            views_en = int(prev.get("ga4_views_en_30d", 0) or 0)
            views_prev = int(prev.get("ga4_views_prev_30d", 0) or 0)

        # --- Bloque GSC (desacoplado de GA4) ---
        if use_gsc:
            g_es = gsc_data.get(norm_es, {}) if norm_es else {}
            g_en = gsc_data.get(norm_en, {}) if (norm_en and norm_en != norm_es) else {}

            clicks_es = int(g_es.get("clicks", 0) or 0)
            clicks_en = int(g_en.get("clicks", 0) or 0)
            impr_es = int(g_es.get("impressions", 0) or 0)
            impr_en = int(g_en.get("impressions", 0) or 0)
            pos_es = float(g_es.get("position", 0.0) or 0.0)
            pos_en = float(g_en.get("position", 0.0) or 0.0)
            ctr_es = float(g_es.get("ctr_pct", (clicks_es / impr_es * 100.0) if impr_es > 0 else 0.0))
            ctr_en = float(g_en.get("ctr_pct", (clicks_en / impr_en * 100.0) if impr_en > 0 else 0.0))

            total_clicks = clicks_es + clicks_en
            total_impr = impr_es + impr_en
            ctr = (total_clicks / total_impr * 100.0) if total_impr > 0 else 0.0

            weighted_pos = 0.0
            impr_with_pos = (impr_es if pos_es > 0 else 0) + (impr_en if pos_en > 0 else 0)
            if impr_with_pos > 0:
                weighted_pos = ((pos_es * impr_es if pos_es > 0 else 0.0) + (pos_en * impr_en if pos_en > 0 else 0.0)) / impr_with_pos
            else:
                pos_vals = [p for p in (pos_es, pos_en) if p > 0]
                weighted_pos = sum(pos_vals) / len(pos_vals) if pos_vals else 0.0

            # Top 5 consultas combinadas ES+EN por activo
            combined_queries: List[Dict[str, Any]] = []
            if norm_es and norm_es in gsc_by_page:
                combined_queries.extend(gsc_by_page[norm_es])
            if norm_en and norm_en != norm_es and norm_en in gsc_by_page:
                combined_queries.extend(gsc_by_page[norm_en])
            combined_queries.sort(key=lambda q: (q.get("impressions", 0), q.get("clicks", 0)), reverse=True)
            top_queries = combined_queries[:5]
        else:
            total_clicks = int(prev.get("gsc_clicks_30d", 0) or 0)
            total_impr = int(prev.get("gsc_impressions_30d", 0) or 0)
            ctr = float(prev.get("gsc_ctr_pct", 0.0) or 0.0)
            weighted_pos = float(prev.get("gsc_avg_position", 0.0) or 0.0)
            clicks_es = int(prev.get("gsc_clicks_es_30d", 0) or 0)
            clicks_en = int(prev.get("gsc_clicks_en_30d", 0) or 0)
            impr_es = int(prev.get("gsc_impressions_es_30d", 0) or 0)
            impr_en = int(prev.get("gsc_impressions_en_30d", 0) or 0)
            ctr_es = float(prev.get("gsc_ctr_es_pct", 0.0) or 0.0)
            ctr_en = float(prev.get("gsc_ctr_en_pct", 0.0) or 0.0)
            pos_es = float(prev.get("gsc_avg_position_es", 0.0) or 0.0)
            pos_en = float(prev.get("gsc_avg_position_en", 0.0) or 0.0)
            top_queries = list(prev.get("gsc_top_queries", []) or [])

        # --- Bloque GSC ventana previa (60d..31d, desacoplado) ---
        if use_gsc_prev:
            gp_es = gsc_prev_map.get(norm_es, {}) if norm_es else {}
            gp_en = gsc_prev_map.get(norm_en, {}) if (norm_en and norm_en != norm_es) else {}
            p_clicks_es = int(gp_es.get("clicks", 0) or 0)
            p_clicks_en = int(gp_en.get("clicks", 0) or 0)
            p_impr_es = int(gp_es.get("impressions", 0) or 0)
            p_impr_en = int(gp_en.get("impressions", 0) or 0)
            p_pos_es = float(gp_es.get("position", 0.0) or 0.0)
            p_pos_en = float(gp_en.get("position", 0.0) or 0.0)

            prev_gsc_clicks = p_clicks_es + p_clicks_en
            prev_gsc_impr = p_impr_es + p_impr_en
            prev_gsc_ctr = (prev_gsc_clicks / prev_gsc_impr * 100.0) if prev_gsc_impr > 0 else 0.0
            p_impr_with_pos = (p_impr_es if p_pos_es > 0 else 0) + (p_impr_en if p_pos_en > 0 else 0)
            if p_impr_with_pos > 0:
                prev_gsc_pos = (
                    (p_pos_es * p_impr_es if p_pos_es > 0 else 0.0)
                    + (p_pos_en * p_impr_en if p_pos_en > 0 else 0.0)
                ) / p_impr_with_pos
            else:
                p_vals = [p for p in (p_pos_es, p_pos_en) if p > 0]
                prev_gsc_pos = sum(p_vals) / len(p_vals) if p_vals else 0.0
        else:
            prev_gsc_clicks = int(prev.get("gsc_clicks_prev_30d", 0) or 0)
            prev_gsc_impr = int(prev.get("gsc_impressions_prev_30d", 0) or 0)
            prev_gsc_ctr = float(prev.get("gsc_ctr_prev_pct", 0.0) or 0.0)
            prev_gsc_pos = float(prev.get("gsc_avg_position_prev", 0.0) or 0.0)

        consolidated[aid] = {
            "ga4_views_30d": total_views,
            "ga4_users_30d": total_users,
            "ga4_engagement_sec": round(total_eng, 1),
            "ga4_views_es_30d": views_es,
            "ga4_views_en_30d": views_en,
            "ga4_views_prev_30d": views_prev,
            "gsc_clicks_30d": total_clicks,
            "gsc_impressions_30d": total_impr,
            "gsc_ctr_pct": round(ctr, 2),
            "gsc_avg_position": round(weighted_pos, 1),
            "gsc_clicks_prev_30d": prev_gsc_clicks,
            "gsc_impressions_prev_30d": prev_gsc_impr,
            "gsc_ctr_prev_pct": round(prev_gsc_ctr, 2),
            "gsc_avg_position_prev": round(prev_gsc_pos, 1),
            "gsc_clicks_es_30d": clicks_es,
            "gsc_clicks_en_30d": clicks_en,
            "gsc_impressions_es_30d": impr_es,
            "gsc_impressions_en_30d": impr_en,
            "gsc_ctr_es_pct": round(ctr_es, 2),
            "gsc_ctr_en_pct": round(ctr_en, 2),
            "gsc_avg_position_es": round(pos_es, 1),
            "gsc_avg_position_en": round(pos_en, 1),
            "gsc_top_queries": top_queries,
        }

    return consolidated


def consolidate_channel_metrics(
    assets: List[Dict[str, Any]],
    acquisition_data: Dict[str, Any],
    existing_channel_metrics: Optional[Dict[str, Any]] = None,
    acquisition_ok: Optional[bool] = None,
    days: int = 30,
) -> Dict[str, Any]:
    """
    Consolida la atribución GA4 por canal canónico, activo e idioma con eventos clave y serie diaria.
    Preserva el snapshot previo ante fallo parcial o ausencia de credenciales (`INV-PULSE-11/12`).
    """
    existing = existing_channel_metrics or {}
    has_fresh = bool(acquisition_data and acquisition_data.get("current_rows"))
    use_fresh = has_fresh if acquisition_ok is None else acquisition_ok

    if not use_fresh:
        if existing:
            return dict(existing)
        return {
            "version": "1.0.0",
            "visibility": "private",
            "days": days,
            "last_synced_at": None,
            "sources_status": {
                "ga4_acquisition": "unavailable",
                "x_native": "standby_zero_cost",
            },
            "by_channel": {},
            "by_asset": {},
            "daily_by_channel": {},
            "records": [],
        }

    # Mapa path normalizado -> asset_id
    path_to_asset: Dict[str, str] = {}
    for asset in assets:
        aid = asset.get("id")
        if not aid:
            continue
        for field in ("url_es", "url_en"):
            norm = normalize_url_path(asset.get(field))
            if norm and norm not in path_to_asset:
                path_to_asset[norm] = aid

    # 1. Eventos clave agregados por (path, channel)
    events_by_path_channel: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for erow in acquisition_data.get("event_rows", []) or []:
        norm_p = normalize_url_path(erow.get("path"))
        if not norm_p:
            continue
        ch = classify_canonical_channel(erow.get("source"), erow.get("medium"))
        ev_name = str(erow.get("event_name") or "").strip()
        cnt = int(erow.get("count", 0) or 0)
        if ev_name and cnt > 0:
            events_by_path_channel[(norm_p, ch)][ev_name] += cnt

    # 2. Ventana previa por canal canónico
    prev_by_channel: Dict[str, int] = defaultdict(int)
    for prow in acquisition_data.get("prev_rows", []) or []:
        ch = classify_canonical_channel(prow.get("source"), prow.get("medium"))
        prev_by_channel[ch] += int(prow.get("sessions", 0) or 0)

    # 3. Agregación actual por (path, channel, source, medium, campaign), por canal y por activo
    channel_buckets: Dict[str, Dict[str, Any]] = {
        ch: {
            "sessions": 0,
            "sessions_es": 0,
            "sessions_en": 0,
            "users": 0,
            "engaged_sessions": 0,
            "engagement_sec": 0.0,
            "key_events": 0,
            "key_events_breakdown": defaultdict(int),
        }
        for ch in CANONICAL_CHANNELS
    }
    asset_channel_buckets: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
    records: List[Dict[str, Any]] = []
    consumed_event_keys: set[Tuple[str, str]] = set()

    for crow in acquisition_data.get("current_rows", []) or []:
        norm_p = normalize_url_path(crow.get("path"))
        if not norm_p:
            continue
        src = str(crow.get("source") or "").strip()
        med = str(crow.get("medium") or "").strip()
        camp = str(crow.get("campaign") or "").strip()
        ch = classify_canonical_channel(src, med)
        lang = detect_url_lang(norm_p)
        aid = path_to_asset.get(norm_p)

        sessions = int(crow.get("sessions", 0) or 0)
        users = int(crow.get("users", 0) or 0)
        engaged = int(crow.get("engaged_sessions", 0) or 0)
        eng_sec = float(crow.get("engagement_sec", 0.0) or 0.0)

        ev_key = (norm_p, ch)
        ev_breakdown: Dict[str, int] = {}
        ev_total = 0
        if ev_key not in consumed_event_keys and ev_key in events_by_path_channel:
            ev_breakdown = dict(events_by_path_channel[ev_key])
            ev_total = sum(ev_breakdown.values())
            consumed_event_keys.add(ev_key)

        cb = channel_buckets[ch]
        cb["sessions"] += sessions
        if lang == "es":
            cb["sessions_es"] += sessions
        elif lang == "en":
            cb["sessions_en"] += sessions
        cb["users"] += users
        cb["engaged_sessions"] += engaged
        cb["engagement_sec"] += eng_sec
        cb["key_events"] += ev_total
        for ev_k, ev_v in ev_breakdown.items():
            cb["key_events_breakdown"][ev_k] += ev_v

        if aid:
            ab = asset_channel_buckets[aid].setdefault(
                ch,
                {
                    "sessions": 0,
                    "sessions_es": 0,
                    "sessions_en": 0,
                    "users": 0,
                    "engaged_sessions": 0,
                    "engagement_sec": 0.0,
                    "key_events": 0,
                    "key_events_breakdown": defaultdict(int),
                },
            )
            ab["sessions"] += sessions
            if lang == "es":
                ab["sessions_es"] += sessions
            elif lang == "en":
                ab["sessions_en"] += sessions
            ab["users"] += users
            ab["engaged_sessions"] += engaged
            ab["engagement_sec"] += eng_sec
            ab["key_events"] += ev_total
            for ev_k, ev_v in ev_breakdown.items():
                ab["key_events_breakdown"][ev_k] += ev_v

        records.append({
            "channel": ch,
            "path": norm_p,
            "asset_id": aid,
            "lang": lang,
            "source": src,
            "medium": med,
            "campaign": camp,
            "sessions": sessions,
            "users": users,
            "engaged_sessions": engaged,
            "engagement_sec": round(eng_sec, 1),
            "key_events": ev_total,
            "key_events_breakdown": ev_breakdown,
        })

    # Añadir eventos huérfanos cuyo (path, channel) no estuvo en current_rows
    for ev_key, ev_map in events_by_path_channel.items():
        if ev_key in consumed_event_keys:
            continue
        norm_p, ch = ev_key
        ev_total = sum(ev_map.values())
        cb = channel_buckets[ch]
        cb["key_events"] += ev_total
        for ev_k, ev_v in ev_map.items():
            cb["key_events_breakdown"][ev_k] += ev_v
        aid = path_to_asset.get(norm_p)
        if aid:
            ab = asset_channel_buckets[aid].setdefault(
                ch,
                {
                    "sessions": 0,
                    "sessions_es": 0,
                    "sessions_en": 0,
                    "users": 0,
                    "engaged_sessions": 0,
                    "engagement_sec": 0.0,
                    "key_events": 0,
                    "key_events_breakdown": defaultdict(int),
                },
            )
            ab["key_events"] += ev_total
            for ev_k, ev_v in ev_map.items():
                ab["key_events_breakdown"][ev_k] += ev_v

    # 4. Serializar resumen por canal
    by_channel_out: Dict[str, Dict[str, Any]] = {}
    for ch, cb in channel_buckets.items():
        sess = int(cb["sessions"])
        sess_prev = int(prev_by_channel.get(ch, 0))
        users = int(cb["users"])
        engaged = int(cb["engaged_sessions"])
        eng_sec = float(cb["engagement_sec"])
        key_ev = int(cb["key_events"])
        lang_tot = cb["sessions_es"] + cb["sessions_en"]
        en_share = round((cb["sessions_en"] / lang_tot * 100.0) if lang_tot > 0 else 0.0, 1)
        eng_rate = round((engaged / sess * 100.0) if sess > 0 else 0.0, 1)
        avg_eng = round((eng_sec / max(users, sess, 1)) if (users > 0 or sess > 0) else 0.0, 1)
        conv_rate = round((key_ev / sess * 100.0) if sess > 0 else 0.0, 2)
        if sess_prev <= 0:
            trend = 100.0 if sess > 0 else 0.0
        else:
            trend = round(max(-100.0, min(500.0, ((sess - sess_prev) / sess_prev) * 100.0)), 1)

        by_channel_out[ch] = {
            "channel": ch,
            "sessions_30d": sess,
            "sessions_es_30d": int(cb["sessions_es"]),
            "sessions_en_30d": int(cb["sessions_en"]),
            "en_share_pct": en_share,
            "users_30d": users,
            "engaged_sessions_30d": engaged,
            "engagement_rate_pct": min(100.0, eng_rate),
            "avg_engagement_sec": avg_eng,
            "key_events_30d": key_ev,
            "key_events_breakdown": dict(cb["key_events_breakdown"]),
            "conversion_rate_pct": conv_rate,
            "sessions_prev_30d": sess_prev,
            "trend_30d_pct": trend,
        }

    # 5. Serializar por activo
    by_asset_out: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for aid, ch_map in asset_channel_buckets.items():
        by_asset_out[aid] = {}
        for ch, ab in ch_map.items():
            sess = int(ab["sessions"])
            users = int(ab["users"])
            eng_sec = float(ab["engagement_sec"])
            by_asset_out[aid][ch] = {
                "sessions_30d": sess,
                "sessions_es_30d": int(ab["sessions_es"]),
                "sessions_en_30d": int(ab["sessions_en"]),
                "users_30d": users,
                "engaged_sessions_30d": int(ab["engaged_sessions"]),
                "avg_engagement_sec": round((eng_sec / max(users, sess, 1)) if (users > 0 or sess > 0) else 0.0, 1),
                "key_events_30d": int(ab["key_events"]),
                "key_events_breakdown": dict(ab["key_events_breakdown"]),
            }

    # 6. Serie diaria por canal (para Dark Social 48h)
    daily_by_channel: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for drow in acquisition_data.get("daily_rows", []) or []:
        iso_d = str(drow.get("date") or "").strip()
        if not iso_d:
            continue
        ch = classify_canonical_channel(drow.get("source"), drow.get("medium"))
        daily_by_channel[iso_d][ch] += int(drow.get("sessions", 0) or 0)

    records.sort(key=lambda r: (r["sessions"], r["key_events"]), reverse=True)

    return {
        "version": "1.0.0",
        "visibility": "private",
        "days": days,
        "last_synced_at": datetime.now(timezone.utc).isoformat(),
        "sources_status": {
            "ga4_acquisition": "ok",
            "x_native": "standby_zero_cost",
        },
        "by_channel": by_channel_out,
        "by_asset": by_asset_out,
        "daily_by_channel": {d: dict(ch_m) for d, ch_m in sorted(daily_by_channel.items())},
        "records": records[:2000],
    }


def _merge_monthly_metrics(
    ga4_monthly: List[Dict[str, Any]],
    gsc_monthly: Dict[str, Dict[str, int]],
    existing_monthly: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Fusiona histórico mensual de GA4 y GSC por `YYYY-MM`, preservando datos previos ante fallos parciales."""
    merged_by_month: Dict[str, Dict[str, Any]] = {}

    for item in existing_monthly:
        m = item.get("month")
        if m:
            merged_by_month[m] = dict(item)

    for item in ga4_monthly:
        m = item.get("month")
        if not m:
            continue
        prev = merged_by_month.get(m, {})
        merged_by_month[m] = {
            **prev,
            "year_month": item.get("year_month", m.replace("-", "")),
            "month": m,
            "views": item.get("views", 0),
            "users": item.get("users", 0),
        }

    for m, g_vals in gsc_monthly.items():
        prev = merged_by_month.get(m, {"year_month": m.replace("-", ""), "month": m, "views": 0, "users": 0})
        prev["gsc_clicks"] = g_vals.get("gsc_clicks", 0)
        prev["gsc_impressions"] = g_vals.get("gsc_impressions", 0)
        merged_by_month[m] = prev

    return [merged_by_month[m] for m in sorted(merged_by_month)]


def check_gsc_connectivity() -> Tuple[bool, str]:
    """Verifica en vivo conectividad, propiedad y muestra mínima sin modificar archivos."""
    try:
        svc = _build_gsc_service()
        if svc is None:
            return False, "No se encontró service_account.json ni GOOGLE_APPLICATION_CREDENTIALS."

        sites_resp = svc.sites().list().execute()
        entries = sites_resp.get("siteEntry", []) or []
        site_url = resolve_gsc_site_url(svc)
        if not site_url:
            return False, f"La cuenta no tiene propiedades accesibles en GSC. siteEntry={entries}"

        end_d = date.today() - timedelta(days=2)
        start_d = end_d - timedelta(days=30)
        smoke = svc.searchanalytics().query(
            siteUrl=site_url,
            body={"startDate": str(start_d), "endDate": str(end_d), "dimensions": ["page"], "rowLimit": 5},
        ).execute()
        rows = smoke.get("rows", []) or []
        perm = next((e.get("permissionLevel") for e in entries if e.get("siteUrl") == site_url), "unknown")
        return True, f"GSC OK · siteUrl={site_url} · permission={perm} · muestra={len(rows)} filas"
    except Exception as exc:
        return False, f"Error de conectividad GSC: {exc}"


def sync_all_metrics(strict_gsc: bool = False) -> Dict[str, Dict[str, Any]]:
    """
    Sincroniza y consolida las métricas absolutas por identificador de activo.
    Guarda en `data/pulse/private/{metrics.json, gsc_queries.json, monthly_metrics.json}`.
    """
    if not INDEX_PATH.exists():
        print(f"[ERROR] {INDEX_PATH} no existe. Ejecuta ops.pulse.build_index primero.")
        return {}

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        assets = json.load(f)

    existing_metrics: Dict[str, Dict[str, Any]] = {}
    if METRICS_PATH.exists():
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                existing_metrics = json.load(f)
        except Exception:
            existing_metrics = {}

    ga4_data = fetch_ga4_metrics(days=30)

    gsc_service = None
    gsc_site: Optional[str] = None
    try:
        gsc_service = _build_gsc_service()
        if gsc_service is not None:
            gsc_site = resolve_gsc_site_url(gsc_service)
    except Exception as exc:
        print(f"[WARN] Error inicializando cliente GSC: {exc}")

    gsc_data = fetch_gsc_metrics(days=30, service=gsc_service, site_url=gsc_site, offset_days=0)
    gsc_prev_data = (
        fetch_gsc_metrics(days=30, service=gsc_service, site_url=gsc_site, offset_days=30)
        if gsc_data
        else {}
    )
    gsc_by_page, gsc_records = (
        fetch_gsc_page_queries(days=30, max_rows=10000, service=gsc_service, site_url=gsc_site)
        if gsc_data
        else ({}, [])
    )

    if strict_gsc and not gsc_data:
        raise RuntimeError("GSC estricto fallido: la consulta Search Console devolvió 0 filas o error de acceso.")

    consolidated_metrics = consolidate_asset_metrics(
        assets=assets,
        ga4_data=ga4_data,
        gsc_data=gsc_data,
        gsc_by_page=gsc_by_page,
        existing_metrics=existing_metrics,
        ga4_ok=bool(ga4_data),
        gsc_ok=bool(gsc_data),
        gsc_prev_data=gsc_prev_data,
        gsc_prev_ok=bool(gsc_prev_data),
    )

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(consolidated_metrics, f, ensure_ascii=False, indent=2)

    # --- Atribución por Canal GA4 + Eventos Clave (ADR-033 / INV-PULSE-12) ---
    existing_channel_metrics: Dict[str, Any] = {}
    if CHANNEL_METRICS_PATH.exists():
        try:
            with open(CHANNEL_METRICS_PATH, "r", encoding="utf-8") as f:
                existing_channel_metrics = json.load(f)
        except Exception:
            existing_channel_metrics = {}

    ga4_acquisition_data = fetch_ga4_acquisition_metrics(days=30)
    consolidated_channels = consolidate_channel_metrics(
        assets=assets,
        acquisition_data=ga4_acquisition_data,
        existing_channel_metrics=existing_channel_metrics,
        acquisition_ok=bool(ga4_acquisition_data and ga4_acquisition_data.get("current_rows")),
        days=30,
    )
    with open(CHANNEL_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(consolidated_channels, f, ensure_ascii=False, indent=2)
    print(f"[SYNC] Métricas de canal GA4 guardadas en {CHANNEL_METRICS_PATH}.")

    if gsc_data:
        # Resumen global por consulta agregada a través de páginas
        query_rollup: Dict[Tuple[str, str], Dict[str, Any]] = {}
        es_impr = en_impr = other_impr = tot_clicks = tot_impr = 0
        brand_clicks = brand_impr = 0
        for rec in gsc_records:
            lang = rec["lang"]
            impr = rec["impressions"]
            clk = rec["clicks"]
            tot_clicks += clk
            tot_impr += impr
            if rec.get("is_brand_query"):
                brand_clicks += clk
                brand_impr += impr
            if lang == "es":
                es_impr += impr
            elif lang == "en":
                en_impr += impr
            else:
                other_impr += impr

            qkey = (rec["query"], lang)
            qb = query_rollup.setdefault(
                qkey,
                {
                    "query": rec["query"],
                    "lang": lang,
                    "clicks": 0,
                    "impressions": 0,
                    "weighted_pos": 0.0,
                    "is_brand_query": bool(rec.get("is_brand_query")),
                },
            )
            qb["clicks"] += clk
            qb["impressions"] += impr
            qb["weighted_pos"] += rec["position"] * impr

        top_global: List[Dict[str, Any]] = []
        for qb in query_rollup.values():
            im = qb["impressions"]
            cl = qb["clicks"]
            top_global.append({
                "query": qb["query"],
                "lang": qb["lang"],
                "clicks": cl,
                "impressions": im,
                "ctr_pct": round((cl / im * 100.0) if im > 0 else 0.0, 2),
                "position": round((qb["weighted_pos"] / im) if im > 0 else 0.0, 1),
                "is_brand_query": qb["is_brand_query"],
            })
        top_global.sort(key=lambda x: (x["impressions"], x["clicks"]), reverse=True)

        gsc_queries_payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "site_url": gsc_site or DEFAULT_GSC_SITE,
            "days": 30,
            "total_rows": len(gsc_records),
            "summary": {
                "total_clicks": tot_clicks,
                "total_impressions": tot_impr,
                "brand_clicks": brand_clicks,
                "brand_impressions": brand_impr,
                "es_impressions": es_impr,
                "en_impressions": en_impr,
                "other_impressions": other_impr,
                "top_queries": top_global[:50],
            },
            "by_page": gsc_by_page,
        }
        with open(GSC_QUERIES_PATH, "w", encoding="utf-8") as f:
            json.dump(gsc_queries_payload, f, ensure_ascii=False, indent=2)
        print(f"[SYNC] Consultas GSC guardadas en {GSC_QUERIES_PATH} ({len(gsc_records)} filas).")

    # Histórico mensual GA4 + GSC
    existing_monthly: List[Dict[str, Any]] = []
    if MONTHLY_METRICS_PATH.exists():
        try:
            with open(MONTHLY_METRICS_PATH, "r", encoding="utf-8") as f:
                existing_monthly = json.load(f)
        except Exception:
            existing_monthly = []

    ga4_monthly = fetch_monthly_ga4_summary()
    gsc_monthly = fetch_gsc_monthly_summary(service=gsc_service, site_url=gsc_site) if gsc_data else {}
    merged_monthly = _merge_monthly_metrics(ga4_monthly, gsc_monthly, existing_monthly)
    if merged_monthly:
        with open(MONTHLY_METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(merged_monthly, f, ensure_ascii=False, indent=2)
        print(f"[SYNC] Histórico mensual guardado en {MONTHLY_METRICS_PATH} ({len(merged_monthly)} meses).")

    print(f"[SYNC] Métricas consolidadas guardadas en {METRICS_PATH} ({len(consolidated_metrics)} activos).")
    return consolidated_metrics


def main() -> int:
    _configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Sincronizador de métricas GA4 + Google Search Console (Datalaria Pulse).")
    parser.add_argument("--check-gsc", action="store_true", help="Verifica conectividad y propiedad GSC sin modificar ficheros.")
    parser.add_argument("--strict-gsc", action="store_true", help="Exige que GSC devuelva filas reales (exit 1 en caso contrario).")
    args = parser.parse_args()

    if args.check_gsc:
        ok, msg = check_gsc_connectivity()
        print(f"[CHECK-GSC] {msg}")
        return 0 if ok else 1

    try:
        sync_all_metrics(strict_gsc=args.strict_gsc)
        return 0
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
