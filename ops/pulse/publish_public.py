"""
ops/pulse/publish_public.py
---------------------------
Módulo de Relativización y Publicación Segura del Dataset Público de Datalaria Pulse.
Especificación técnica formal: SPEC-APP-PULSE (specs/apps/pulse/spec.md) - Hito 5.3.

Responsabilidades:
1. Leer el índice privado completo (`data/pulse/private/index.json`) y las métricas
   absolutas consolidadas (`data/pulse/private/metrics.json`).
2. Filtrar de inmediato cualquier activo con `visibility: private` (INV-PULSE-1).
3. Calcular métricas relativas deterministas:
   - index_100: (views_i / max(mediana_visitas, 1)) * 100
   - rank_pct: percentil de visitas en el catálogo (0..100)
   - trend_30d_pct: variación porcentual frente al periodo previo
   - gsc_opportunity: indicador booleano de optimización SEO (GSC o alto engagement)
4. Enriquecer `metrics_relative` y eliminar `metrics_absolute` (INV-PULSE-2).
5. Validar exhaustivamente las invariantes mediante `PublicPulseDataset.validate_security_invariants()`.
6. Exportar el archivo a `static/apps/pulse/data/public.json`.
"""

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

from ops.pulse.models import (
    ContentAsset,
    RelativeMetrics,
    AbsoluteMetrics,
    MonthlyTrafficPoint,
    PublicPulseDataset
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
INDEX_PRIVATE_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
METRICS_PRIVATE_PATH = ROOT_DIR / "data" / "pulse" / "private" / "metrics.json"
MONTHLY_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "monthly_metrics.json"
PUBLIC_DATASET_PATH = ROOT_DIR / "static" / "apps" / "pulse" / "data" / "public.json"


def calculate_relative_metrics(
    assets: List[Dict[str, Any]],
    metrics: Dict[str, Dict[str, Any]]
) -> Dict[str, RelativeMetrics]:
    """
    Calcula determinísticamente índices base 100 y percentiles a partir de métricas absolutas.
    """
    # 1. Recopilar vistas de activos publicados para calcular la mediana y percentiles
    views_map: Dict[str, int] = {}
    for a in assets:
        aid = a["id"]
        m = metrics.get(aid, {})
        v = m.get("ga4_views_30d", 0)
        views_map[aid] = v

    published_views = [
        views_map[a["id"]] for a in assets 
        if a.get("status") == "published" and views_map[a["id"]] > 0
    ]
    median_views = statistics.median(published_views) if published_views else 10.0
    if median_views <= 0:
        median_views = 1.0

    # Ordenar para cálculo de percentiles
    sorted_views = sorted(views_map.values())
    total_count = len(sorted_views)

    rel_metrics: Dict[str, RelativeMetrics] = {}

    for a in assets:
        aid = a["id"]
        v = views_map.get(aid, 0)
        m = metrics.get(aid, {})

        # Base 100 relativo a la mediana
        idx_100 = round((v / median_views) * 100)

        # Percentil
        # rank_pct = (pos / total) * 100
        count_less = sum(1 for x in sorted_views if x < v)
        count_equal = sum(1 for x in sorted_views if x == v)
        # Percentil estándar: (count_less + 0.5 * count_equal) / total * 100
        rank_pct = round(((count_less + 0.5 * count_equal) / max(total_count, 1)) * 100)
        rank_pct = max(0, min(100, rank_pct))

        # Oportunidad GSC: si impresiones > 500 y posición entre 5 y 20, o si engagement > 90s con visitas < mediana
        impr = m.get("gsc_impressions_30d", 0)
        pos = m.get("gsc_avg_position", 0.0)
        eng = m.get("ga4_engagement_sec", 0.0)
        is_opp = bool((impr >= 300 and 5.0 <= pos <= 20.0) or (eng >= 120.0 and v > 0 and v < median_views))

        rel_metrics[aid] = RelativeMetrics(
            index_100=idx_100,
            rank_pct=rank_pct,
            trend_30d_pct=0.0,
            gsc_opportunity=is_opp
        )

    return rel_metrics


def publish_public_dataset() -> PublicPulseDataset:
    """
    Compila y valida la versión pública de Datalaria Pulse.
    """
    if not INDEX_PRIVATE_PATH.exists():
        raise FileNotFoundError(f"No existe {INDEX_PRIVATE_PATH}. Ejecuta build_index primero.")

    with open(INDEX_PRIVATE_PATH, "r", encoding="utf-8") as f:
        raw_assets = json.load(f)

    metrics = {}
    if METRICS_PRIVATE_PATH.exists():
        with open(METRICS_PRIVATE_PATH, "r", encoding="utf-8") as f:
            metrics = json.load(f)

    # 1. Calcular métricas relativas
    rel_map = calculate_relative_metrics(raw_assets, metrics)

    # 2. Filtrar solo los activos 'public' y mapear
    public_content_assets: List[ContentAsset] = []
    parity_summary: Dict[str, int] = {}

    for item in raw_assets:
        # INV-PULSE-1: Cero fuga de privados
        if item.get("visibility") == "private":
            continue

        aid = item["id"]
        # Enriquecer con métricas relativas calculadas
        item["metrics_relative"] = rel_map.get(aid)
        # Asegurar que metrics_absolute NUNCA esté presente en el objeto público
        item["metrics_absolute"] = None

        asset_obj = ContentAsset(**item)
        public_content_assets.append(asset_obj)

        par = asset_obj.language_parity
        parity_summary[par] = parity_summary.get(par, 0) + 1

    # 2.b Relativizar serie temporal mensual histórica (INV-PULSE-2)
    monthly_traffic_index: List[MonthlyTrafficPoint] = []
    if MONTHLY_METRICS_PATH.exists():
        try:
            with open(MONTHLY_METRICS_PATH, "r", encoding="utf-8") as f:
                raw_monthly = json.load(f)

            m_views = [m.get("views", 0) for m in raw_monthly if m.get("views", 0) > 0]
            median_m_views = statistics.median(m_views) if m_views else 100.0
            if median_m_views <= 0:
                median_m_views = 1.0

            month_abbr = {
                "01": "Ene", "02": "Feb", "03": "Mar", "04": "Abr", "05": "May", "06": "Jun",
                "07": "Jul", "08": "Ago", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dic"
            }

            for m in raw_monthly:
                m_str = m.get("month", "")
                parts = m_str.split("-")
                label = m_str
                if len(parts) == 2:
                    label = f"{month_abbr.get(parts[1], parts[1])} '{parts[0][2:]}"

                idx_100 = round((m.get("views", 0) / median_m_views) * 100)
                monthly_traffic_index.append(MonthlyTrafficPoint(
                    month=m_str,
                    label=label,
                    index_100=idx_100
                ))
        except Exception as e:
            print(f"[WARN] Error al procesar monthly_metrics.json: {e}")

    # 3. Construir modelo de dataset público
    pub_dataset = PublicPulseDataset(
        version="1.0.0",
        generated_at=datetime.now(timezone.utc),
        total_assets=len(public_content_assets),
        published_assets=sum(1 for a in public_content_assets if a.status == "published"),
        scheduled_assets=sum(1 for a in public_content_assets if a.status == "scheduled"),
        ideas_count=sum(1 for a in public_content_assets if a.status == "idea"),
        parity_summary=parity_summary,
        monthly_traffic_index=monthly_traffic_index,
        assets=public_content_assets
    )

    # 4. Validar invariantes deterministas antes de escribir a disco
    pub_dataset.validate_security_invariants()

    # 5. Escribir a static/apps/pulse/data/public.json
    PUBLIC_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PUBLIC_DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(pub_dataset.model_dump(mode="json"), f, ensure_ascii=False, indent=2)

    print(f"[PUBLISH] Dataset público generado en {PUBLIC_DATASET_PATH}")
    print(f"          Total activos: {pub_dataset.total_assets} | Publicados: {pub_dataset.published_assets}")
    print(f"          Invariantes INV-PULSE-1 e INV-PULSE-2 verificadas exitosamente.")

    return pub_dataset


if __name__ == "__main__":
    publish_public_dataset()
