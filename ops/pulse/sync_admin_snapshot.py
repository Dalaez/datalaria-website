"""
ops/pulse/sync_admin_snapshot.py
--------------------------------
Sincroniza de forma segura el catálogo privado maestro (`data/pulse/private/index.json`)
enriquecido con métricas relativas hacia Supabase (`pulse.private_snapshot`) usando
exclusivamente `SUPABASE_SERVICE_ROLE_KEY`.

Degradación elegante: si no existe `SUPABASE_SERVICE_ROLE_KEY` en el entorno ni en `.env`,
emite aviso y finaliza con código 0 para no bloquear entornos locales/CI sin secreto.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ops.pulse.impact_analyzer import (
    analyze_channel_performance,
    build_channel_category_matrix,
    calculate_ptr_pct,
    summarize_social_platforms,
)
from ops.pulse.publish_public import calculate_relative_metrics

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PRIVATE_INDEX_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
PRIVATE_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "metrics.json"
PRIVATE_IMPACT_REPORT_PATH = ROOT_DIR / "data" / "pulse" / "private" / "impact_report.json"
PRIVATE_CHANNEL_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "channel_metrics.json"
PRIVATE_SOCIAL_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "social_metrics.json"
DEFAULT_SUPABASE_URL = "https://wkbmxekmofrjtcsyytrv.supabase.co"


def _load_env_fallback() -> Dict[str, str]:
    """Lee variables opcionales desde archivos .env locales si existen."""
    values: Dict[str, str] = {}
    for env_path in (ROOT_DIR / ".env", ROOT_DIR / "apps" / "pulse" / "web" / ".env"):
        if not env_path.is_file():
            continue
        try:
            for raw_line in env_path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                values[k.strip()] = v.strip().strip('"').strip("'")
        except Exception:
            continue
    return values


def build_enriched_admin_payload() -> List[Dict[str, Any]]:
    """
    Lee `data/pulse/private/index.json` y enriquece `metrics_relative` sin
    incluir `metrics_absolute`, preservando todos los activos (incluidos draft y embargados).
    """
    if not PRIVATE_INDEX_PATH.is_file():
        raise FileNotFoundError(f"No existe {PRIVATE_INDEX_PATH}. Ejecuta build_index primero.")

    raw_assets: List[Dict[str, Any]] = json.loads(PRIVATE_INDEX_PATH.read_text(encoding="utf-8"))
    metrics: Dict[str, Dict[str, Any]] = {}
    if PRIVATE_METRICS_PATH.is_file():
        metrics = json.loads(PRIVATE_METRICS_PATH.read_text(encoding="utf-8"))

    rel_map = calculate_relative_metrics(raw_assets, metrics)
    enriched: List[Dict[str, Any]] = []
    for item in raw_assets:
        copy_item = dict(item)
        rel = rel_map.get(copy_item["id"])
        copy_item["metrics_relative"] = rel.model_dump(mode="json") if rel else None
        copy_item["metrics_absolute"] = None
        enriched.append(copy_item)
    return enriched


def _safe_load_json(path: Path) -> Any:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_omnichannel_intelligence_payload(
    *,
    index_path: Path = PRIVATE_INDEX_PATH,
    impact_report_path: Path = PRIVATE_IMPACT_REPORT_PATH,
    channel_metrics_path: Path = PRIVATE_CHANNEL_METRICS_PATH,
    social_metrics_path: Path = PRIVATE_SOCIAL_METRICS_PATH,
) -> Dict[str, Any]:
    """
    Construye el bloque privado `omnichannel_intelligence` para `pulse.private_snapshot` (RLS Admin).
    Jamás debe exportarse a `static/apps/pulse/data/public.json` (INV-PULSE-2/9/12).
    """
    raw_assets = _safe_load_json(index_path)
    assets_list: List[Dict[str, Any]] = raw_assets if isinstance(raw_assets, list) else []
    impact_data = _safe_load_json(impact_report_path)
    impact_dict: Dict[str, Any] = impact_data if isinstance(impact_data, dict) else {}
    channel_data = _safe_load_json(channel_metrics_path)
    channel_dict: Optional[Dict[str, Any]] = channel_data if isinstance(channel_data, dict) else None
    social_data = _safe_load_json(social_metrics_path)
    social_dict: Optional[Dict[str, Any]] = social_data if isinstance(social_data, dict) else None

    channel_summary = impact_dict.get("channel_summary")
    if not isinstance(channel_summary, list) or not channel_summary:
        channel_summary = [c.model_dump(mode="json") for c in analyze_channel_performance(channel_dict)]

    social_funnel = impact_dict.get("social_platform_summary")
    if not isinstance(social_funnel, dict) or not social_funnel:
        social_funnel = summarize_social_platforms(social_dict, channel_dict)

    dark_social_alerts = impact_dict.get("dark_social_alerts")
    if not isinstance(dark_social_alerts, list):
        dark_social_alerts = []

    ptr_alerts = impact_dict.get("ptr_leak_alerts")
    if not isinstance(ptr_alerts, list):
        ptr_alerts = []

    hidden_winners = impact_dict.get("hidden_channel_winners")
    if not isinstance(hidden_winners, list):
        hidden_winners = []

    canonical_shield_alerts = impact_dict.get("canonical_shield_alerts")
    if not isinstance(canonical_shield_alerts, list):
        canonical_shield_alerts = []

    # Embudo de 4 capas: Alcance Nativo -> PTR -> Retención/Conversiones GA4 -> Lift GSC
    native_reach = 0
    for plat_key in ("devto", "coderlegion", "linkedin_company"):
        p_info = social_funnel.get(plat_key) if isinstance(social_funnel.get(plat_key), dict) else {}
        native_reach += int(p_info.get("native_views", 0) or p_info.get("total_impressions", 0) or 0)

    social_channels = {"linkedin", "x", "devto", "coderlegion"}
    ga4_social_sessions = 0
    ga4_social_key_events = 0
    weighted_eng_sum = 0.0
    for row in channel_summary:
        if not isinstance(row, dict) or row.get("channel") not in social_channels:
            continue
        sess = int(row.get("sessions_30d", 0) or 0)
        ga4_social_sessions += sess
        ga4_social_key_events += int(row.get("key_events_30d", 0) or 0)
        weighted_eng_sum += float(row.get("avg_engagement_sec", 0.0) or 0.0) * sess

    avg_social_engagement_sec = (
        round(weighted_eng_sum / ga4_social_sessions, 1) if ga4_social_sessions > 0 else 0.0
    )
    avg_ptr_pct = calculate_ptr_pct(ga4_social_sessions, native_reach)

    gsc_clicks_30d = int(impact_dict.get("total_30d_gsc_clicks", 0) or 0)
    gsc_clicks_prev_30d = int(impact_dict.get("gsc_clicks_prev_30d", 0) or 0)
    gsc_lift_pct = (
        round(((gsc_clicks_30d - gsc_clicks_prev_30d) / gsc_clicks_prev_30d) * 100.0, 1)
        if gsc_clicks_prev_30d > 0
        else 0.0
    )

    matrix = build_channel_category_matrix(assets_list, channel_dict)

    category_roi_v2: List[Dict[str, Any]] = []
    for cat_item in (impact_dict.get("category_performance") or []):
        if not isinstance(cat_item, dict):
            continue
        category_roi_v2.append(
            {
                "category": str(cat_item.get("category") or "General"),
                "editorial_roi_score": float(cat_item.get("editorial_roi_score", 0.0) or 0.0),
                "social_traction_score": float(cat_item.get("social_traction_score", 0.0) or 0.0),
                "monetization_coverage_pct": float(cat_item.get("monetization_coverage_pct", 0.0) or 0.0),
                "total_views_30d": int(cat_item.get("total_views_30d", 0) or 0),
                "en_traffic_share_pct": float(cat_item.get("en_traffic_share_pct", 0.0) or 0.0),
            }
        )

    # Top recomendaciones accionables unificadas E02 / E06
    top_recommendations: List[Dict[str, Any]] = []
    for pa in ptr_alerts[:5]:
        if isinstance(pa, dict):
            top_recommendations.append(
                {
                    "id": f"ptr-{pa.get('asset_id')}-{pa.get('platform')}",
                    "agent": "E06",
                    "type": "ptr_leak",
                    "severity": "high",
                    "channel": str(pa.get("platform") or ""),
                    "asset_or_ref": str(pa.get("asset_id") or ""),
                    "action": str(pa.get("recommended_action") or ""),
                }
            )
    for cs in canonical_shield_alerts[:5]:
        if isinstance(cs, dict):
            top_recommendations.append(
                {
                    "id": f"shield-{cs.get('asset_id')}-{cs.get('platform')}",
                    "agent": "E02",
                    "type": "canonical_shield",
                    "severity": "high",
                    "channel": str(cs.get("platform") or ""),
                    "asset_or_ref": str(cs.get("asset_id") or ""),
                    "action": str(cs.get("recommended_action") or ""),
                }
            )
    for hw in hidden_winners[:5]:
        if isinstance(hw, dict):
            top_recommendations.append(
                {
                    "id": f"winner-{hw.get('asset_id')}-{hw.get('channel')}",
                    "agent": "E06",
                    "type": "hidden_winner",
                    "severity": "medium",
                    "channel": str(hw.get("channel") or ""),
                    "asset_or_ref": str(hw.get("asset_id") or ""),
                    "action": str(hw.get("recommended_action") or ""),
                }
            )
    for ds in dark_social_alerts[:5]:
        if isinstance(ds, dict):
            top_recommendations.append(
                {
                    "id": f"dark-{ds.get('dispatch_id') or ds.get('alert_type')}",
                    "agent": "E06",
                    "type": "dark_social",
                    "severity": str(ds.get("severity") or "medium"),
                    "channel": str(ds.get("channel_expected") or "direct"),
                    "asset_or_ref": str(ds.get("dispatch_id") or "direct"),
                    "action": str(ds.get("recommended_action") or ""),
                }
            )

    return {
        "generated_at": impact_dict.get("generated_at") or datetime.now(timezone.utc).isoformat(),
        "is_synthetic": False,
        "roi_formula_version": "v2",
        "x_standby_zero_cost": True,
        "funnel_4_layers": {
            "native_reach": native_reach,
            "avg_ptr_pct": avg_ptr_pct,
            "ga4_social_sessions": ga4_social_sessions,
            "ga4_social_key_events": ga4_social_key_events,
            "avg_social_engagement_sec": avg_social_engagement_sec,
            "gsc_clicks_30d": gsc_clicks_30d,
            "gsc_clicks_prev_30d": gsc_clicks_prev_30d,
            "gsc_lift_pct": gsc_lift_pct,
        },
        "channel_summary": channel_summary,
        "social_funnel": social_funnel,
        "channel_category_matrix": matrix,
        "category_roi_v2": category_roi_v2,
        "dark_social_alerts": dark_social_alerts,
        "ptr_alerts": ptr_alerts,
        "hidden_winners": hidden_winners,
        "canonical_shield_alerts": canonical_shield_alerts,
        "top_recommendations": top_recommendations[:15],
    }


def build_supabase_headers(key: str) -> Dict[str, str]:
    """
    Construye cabeceras REST compatibles tanto con claves modernas `sb_secret_...`
    (opacas: no son JWT, por lo que no se envían como Bearer) como con claves
    legacy JWT `service_role` (3 segmentos `eyJ...`).
    """
    headers: Dict[str, str] = {
        "apikey": key,
        "Content-Type": "application/json",
        "Content-Profile": "pulse",
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }
    if not key.startswith("sb_secret_") and key.count(".") == 2:
        headers["Authorization"] = f"Bearer {key}"
    return headers


def sync_admin_snapshot(
    supabase_url: Optional[str] = None,
    service_role_key: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Ejecuta upsert en `pulse.private_snapshot` (id='master').
    Retorna (synced_ok, message). Nunca falla por falta de credenciales.
    """
    env_file = _load_env_fallback() if service_role_key is None else {}
    url = (
        supabase_url
        or os.environ.get("SUPABASE_URL")
        or env_file.get("SUPABASE_URL")
        or os.environ.get("VITE_SUPABASE_URL")
        or env_file.get("VITE_SUPABASE_URL")
        or DEFAULT_SUPABASE_URL
    ).rstrip("/")
    if service_role_key is not None:
        key = service_role_key.strip()
    else:
        key = (
            os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
            or env_file.get("SUPABASE_SERVICE_ROLE_KEY")
            or ""
        ).strip()

    if not key:
        msg = "[SKIP] SUPABASE_SERVICE_ROLE_KEY no configurada; sincronizacion RLS Admin omitida."
        print(msg)
        return False, msg

    assets = build_enriched_admin_payload()
    omnichannel = build_omnichannel_intelligence_payload()
    now_iso = datetime.now(timezone.utc).isoformat()
    row_body = json.dumps(
        {
            "id": "master",
            "payload": {
                "generated_at": now_iso,
                "total_assets": len(assets),
                "assets": assets,
                "omnichannel_intelligence": omnichannel,
            },
            "updated_at": now_iso,
        },
        ensure_ascii=False,
    ).encode("utf-8")

    endpoint = f"{url}/rest/v1/private_snapshot?on_conflict=id"
    req = urllib.request.Request(
        endpoint,
        data=row_body,
        method="POST",
        headers=build_supabase_headers(key),
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status_code = getattr(resp, "status", 200)
        msg = f"[OK] Snapshot maestro Admin ({len(assets)} activos) sincronizado en Supabase RLS (HTTP {status_code})."
        print(msg)
        return True, msg
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:200]
        msg = f"[WARN] Supabase rechazo el upsert Admin (HTTP {exc.code}): {detail}"
        print(msg)
        return False, msg
    except Exception as exc:
        msg = f"[WARN] Error de red sincronizando snapshot Admin: {exc}"
        print(msg)
        return False, msg


if __name__ == "__main__":
    sync_admin_snapshot()
