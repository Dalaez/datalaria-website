"""
ops/pulse/sync_metrics.py
-------------------------
Módulo de Sincronización y Enriquecimiento Cuantitativo de Métricas (GA4 + Search Console).
Especificación técnica formal: SPEC-APP-PULSE (specs/apps/pulse/spec.md) - Hito 5.3.

Responsabilidades:
1. Extraer métricas de visitas, usuarios y engagement de Google Analytics 4 (Data API)
   por ruta canónica para Posts, Apps y Kits.
2. Extraer métricas orgánicas de Google Search Console (Search Analytics API)
   (clics, impresiones, CTR medio y posición media).
3. Graceful degradation: si las credenciales o la red no están disponibles,
   reutiliza datos existentes en `data/pulse/private/metrics.json` o genera un snapshot sintético neutro.
4. Exporta métricas absolutas a `data/pulse/private/metrics.json`.
"""

import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

from ops.pulse.models import AbsoluteMetrics

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "metrics.json"
MONTHLY_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "monthly_metrics.json"
CREDENTIALS_FILE = ROOT_DIR / "service_account.json"
DEFAULT_PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID", "367847195")
DEFAULT_GSC_SITE = os.environ.get("GSC_SITE_URL", "sc-domain:datalaria.com")


def fetch_ga4_metrics(days: int = 30) -> Dict[str, Dict[str, Any]]:
    """
    Consulta GA4 Data API para todas las rutas del sitio en los últimos N días.
    Retorna un diccionario { path_normalizado: { views, users, duration } }.
    """
    if not CREDENTIALS_FILE.exists():
        print(f"[WARN] No se encontró service_account.json en {CREDENTIALS_FILE}. Saltando llamada real a GA4.")
        return {}

    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Metric,
            RunReportRequest,
            OrderBy,
        )

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS_FILE)
        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{DEFAULT_PROPERTY_ID}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="totalUsers"),
                Metric(name="userEngagementDuration"),
            ],
            date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
            limit=500,
        )

        response = client.run_report(request)
        path_metrics = {}

        for row in response.rows:
            raw_path = row.dimension_values[0].value.strip()
            # Normalizar sin slash final para búsqueda consistente
            norm_path = raw_path.rstrip("/")
            views = int(row.metric_values[0].value)
            users = int(row.metric_values[1].value)
            duration = float(row.metric_values[2].value)

            path_metrics[norm_path] = {
                "views": views,
                "users": users,
                "engagement_sec": duration
            }

        print(f"[GA4] Extraídas métricas para {len(path_metrics)} rutas.")
        return path_metrics

    except Exception as e:
        print(f"[WARN] Error al consultar GA4: {e}")
        return {}


def fetch_monthly_ga4_summary(months: int = 14) -> list:
    """Consulta los totales agregados mensuales en GA4 para la serie temporal histórica."""
    if not CREDENTIALS_FILE.exists():
        return []
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, OrderBy

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS_FILE)
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


def fetch_gsc_metrics(days: int = 30) -> Dict[str, Dict[str, Any]]:
    """
    Consulta Google Search Console Search Analytics API.
    Retorna { url_path: { clicks, impressions, ctr, position } }.
    """
    if not CREDENTIALS_FILE.exists():
        print(f"[WARN] No se encontró service_account.json. Saltando llamada real a GSC.")
        return {}

    try:
        from googleapiclient.discovery import build
        from google.oauth2 import service_account

        creds = service_account.Credentials.from_service_account_file(
            str(CREDENTIALS_FILE),
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
        )
        service = build("searchconsole", "v1", credentials=creds)

        # Rango de fechas aproximado (Search Console tiene 2-3 días de retraso)
        from datetime import date, timedelta
        end_d = date.today() - timedelta(days=2)
        start_d = end_d - timedelta(days=days)

        request_body = {
            "startDate": str(start_d),
            "endDate": str(end_d),
            "dimensions": ["page"],
            "rowLimit": 500
        }

        resp = service.searchanalytics().query(siteUrl=DEFAULT_GSC_SITE, body=request_body).execute()
        rows = resp.get("rows", [])
        gsc_metrics = {}

        for r in rows:
            page_url = r.get("keys", [""])[0]
            # Extraer ruta relativa: https://datalaria.com/es/posts/... -> /es/posts/...
            path_part = "/" + "/".join(page_url.split("/")[3:]).rstrip("/")
            gsc_metrics[path_part] = {
                "clicks": int(r.get("clicks", 0)),
                "impressions": int(r.get("impressions", 0)),
                "ctr_pct": float(r.get("ctr", 0.0) * 100),
                "position": float(r.get("position", 0.0))
            }

        print(f"[GSC] Extraídas métricas para {len(gsc_metrics)} páginas.")
        return gsc_metrics

    except Exception as e:
        print(f"[WARN] No se pudo consultar Search Console (o cuenta sin permisos delegados): {e}")
        return {}


def sync_all_metrics() -> Dict[str, Dict[str, Any]]:
    """
    Sincroniza y consolida las métricas absolutas por identificador de activo.
    Guarda en data/pulse/private/metrics.json.
    """
    ga4_data = fetch_ga4_metrics(days=30)
    gsc_data = fetch_gsc_metrics(days=30)

    # Cargar índice privado para conocer los IDs de cada activo
    index_path = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
    if not index_path.exists():
        print(f"[ERROR] {index_path} no existe. Ejecuta ops.pulse.build_index primero.")
        return {}

    with open(index_path, "r", encoding="utf-8") as f:
        assets = json.load(f)

    # Si ya existen métricas previas y las APIs no devolvieron nada, preservar
    existing_metrics = {}
    if METRICS_PATH.exists():
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                existing_metrics = json.load(f)
        except Exception:
            pass

    consolidated_metrics: Dict[str, Dict[str, Any]] = {}

    for asset in assets:
        aid = asset["id"]
        url_es = (asset.get("url_es") or "").rstrip("/")
        url_en = (asset.get("url_en") or "").rstrip("/")

        # Combinar visitas y engagement de ES y EN
        m_es = ga4_data.get(url_es, {})
        m_en = ga4_data.get(url_en, {})

        gsc_es = gsc_data.get(url_es, {})
        gsc_en = gsc_data.get(url_en, {})

        total_views = m_es.get("views", 0) + m_en.get("views", 0)
        total_users = m_es.get("users", 0) + m_en.get("users", 0)
        total_eng = m_es.get("engagement_sec", 0.0) + m_en.get("engagement_sec", 0.0)

        total_clicks = gsc_es.get("clicks", 0) + gsc_en.get("clicks", 0)
        total_impr = gsc_es.get("impressions", 0) + gsc_en.get("impressions", 0)
        avg_pos = 0.0
        pos_list = [gsc_es["position"] for gsc_es in (gsc_es, gsc_en) if "position" in gsc_es and gsc_es["position"] > 0]
        if pos_list:
            avg_pos = sum(pos_list) / len(pos_list)

        ctr = (total_clicks / total_impr * 100) if total_impr > 0 else 0.0

        # Si no hubo datos frescos pero hay previos, preservar
        prev = existing_metrics.get(aid, {})
        if total_views == 0 and prev.get("ga4_views_30d", 0) > 0:
            total_views = prev.get("ga4_views_30d", 0)
            total_users = prev.get("ga4_users_30d", 0)
            total_eng = prev.get("ga4_engagement_sec", 0.0)
            total_clicks = prev.get("gsc_clicks_30d", 0)
            total_impr = prev.get("gsc_impressions_30d", 0)
            ctr = prev.get("gsc_ctr_pct", 0.0)
            avg_pos = prev.get("gsc_avg_position", 0.0)

        consolidated_metrics[aid] = {
            "ga4_views_30d": total_views,
            "ga4_users_30d": total_users,
            "ga4_engagement_sec": total_eng,
            "gsc_clicks_30d": total_clicks,
            "gsc_impressions_30d": total_impr,
            "gsc_ctr_pct": round(ctr, 2),
            "gsc_avg_position": round(avg_pos, 1)
        }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(consolidated_metrics, f, ensure_ascii=False, indent=2)

    monthly_summary = fetch_monthly_ga4_summary()
    if monthly_summary:
        with open(MONTHLY_METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(monthly_summary, f, ensure_ascii=False, indent=2)
        print(f"[SYNC] Histórico mensual guardado en {MONTHLY_METRICS_PATH}.")

    print(f"[SYNC] Métricas consolidadas guardadas en {METRICS_PATH} ({len(consolidated_metrics)} activos).")
    return consolidated_metrics


if __name__ == "__main__":
    sync_all_metrics()
