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

from ops.pulse.publish_public import calculate_relative_metrics

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PRIVATE_INDEX_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
PRIVATE_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "metrics.json"
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
    now_iso = datetime.now(timezone.utc).isoformat()
    row_body = json.dumps(
        {
            "id": "master",
            "payload": {
                "generated_at": now_iso,
                "total_assets": len(assets),
                "assets": assets,
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
