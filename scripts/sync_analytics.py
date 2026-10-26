#!/usr/bin/env python3
"""
scripts/sync_analytics.py
Sincroniza las analíticas de Google Analytics 4 (GA4) con Datalaria.
- Extrae los posts más leídos de los últimos 30 días para ES y EN.
- Valida la existencia del contenido en content/{es,en}/posts/.
- Actualiza config.yaml (languages.<lang>.params.homePortal.mostRead).
- Genera data/analytics.json para consumo en plantillas Hugo.
- Muestra un resumen ejecutivo por consola.
"""

import os
import re
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

# Configurar salida UTF-8 en consola de Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"
DATA_ANALYTICS_PATH = ROOT_DIR / "data" / "analytics.json"
CREDENTIALS_FILE = ROOT_DIR / "service_account.json"
DEFAULT_PROPERTY_ID = "367847195"


def check_post_exists(lang: str, slug: str) -> bool:
    """Verifica si existe el archivo del post en content/<lang>/posts/<slug>/."""
    post_dir = ROOT_DIR / "content" / lang / "posts" / slug
    post_file = ROOT_DIR / "content" / lang / "posts" / f"{slug}.md"
    return (post_dir / "index.md").exists() or post_file.exists()


def fetch_ga4_data(property_id: str, days: int = 30):
    """Consulta GA4 Data API para obtener visitas de páginas en los últimos N días."""
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de credenciales en: {CREDENTIALS_FILE}\n"
            "Asegúrate de colocar tu service_account.json en la raíz del proyecto."
        )

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS_FILE)
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="screenPageViews"),
            Metric(name="totalUsers"),
            Metric(name="userEngagementDuration"),
        ],
        date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
        limit=100,
    )

    return client.run_report(request)


def parse_posts_data(response):
    """Filtra y agrupa las métricas por idioma y slug de posts existentes."""
    posts_data = {"es": {}, "en": {}}

    path_pattern = re.compile(r"^/(es|en)/posts/([a-zA-Z0-9_\-]+)/?$")

    for row in response.rows:
        raw_path = row.dimension_values[0].value
        match = path_pattern.match(raw_path)
        if not match:
            continue

        lang, slug = match.group(1), match.group(2)

        # Evitar rutas de listados o paginaciones
        if slug in ("page", "tags", "categories", "index"):
            continue

        if not check_post_exists(lang, slug):
            continue

        views = int(row.metric_values[0].value)
        users = int(row.metric_values[1].value)
        duration_sec = float(row.metric_values[2].value)

        if slug in posts_data[lang]:
            posts_data[lang][slug]["views"] += views
            posts_data[lang][slug]["users"] += users
            posts_data[lang][slug]["duration_sec"] += duration_sec
        else:
            posts_data[lang][slug] = {
                "slug": slug,
                "views": views,
                "users": users,
                "duration_sec": duration_sec,
            }

    # Ordenar por views descendente y calcular rankings
    ranked = {}
    for lang in ("es", "en"):
        sorted_list = sorted(
            posts_data[lang].values(), key=lambda x: x["views"], reverse=True
        )
        for idx, item in enumerate(sorted_list, start=1):
            item["rank"] = idx
            avg_dur = (
                round(item["duration_sec"] / item["views"], 1)
                if item["views"] > 0
                else 0
            )
            item["avg_duration_sec"] = avg_dur
        ranked[lang] = sorted_list

    return ranked


def update_config_yaml(ranked_data, top_n: int = 3):
    """Actualiza la sección mostRead en config.yaml de forma segura preservando comentarios."""
    if not CONFIG_PATH.exists():
        print(f"⚠️ No se encontró config.yaml en {CONFIG_PATH}")
        return False

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    for lang in ("es", "en"):
        top_slugs = [f"/posts/{item['slug']}" for item in ranked_data.get(lang, [])[:top_n]]
        if not top_slugs:
            continue

        yaml_list = "\n".join([f'          - "{slug}"' for slug in top_slugs])

        # Patrón para localizar mostRead dentro del bloque del idioma
        # Buscamos 'languages:\n...  <lang>:\n...    params:\n...      homePortal:\n        mostRead:\n(          - ".*"\n)+'
        pattern = re.compile(
            rf'(languages:\s*\n.*?  {lang}:.*?homePortal:\s*\n\s*mostRead:\s*\n)(?:\s*-\s*"[^"]*"\s*\n)+',
            re.DOTALL,
        )

        replacement = rf"\g<1>{yaml_list}\n"
        content, count = pattern.subn(replacement, content, count=1)
        if count == 0:
            # Si las comillas eran simples o sin comillas
            pattern_alt = re.compile(
                rf'(languages:\s*\n.*?  {lang}:.*?homePortal:\s*\n\s*mostRead:\s*\n)(?:\s*-\s*[^\n]+\s*\n)+',
                re.DOTALL,
            )
            content, count = pattern_alt.subn(replacement, content, count=1)

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def save_analytics_json(ranked_data, days: int = 30):
    """Guarda data/analytics.json para consumo en plantillas Hugo."""
    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "period_days": days,
        "posts": {
            "es": {item["slug"]: item for item in ranked_data.get("es", [])},
            "en": {item["slug"]: item for item in ranked_data.get("en", [])},
        },
    }

    DATA_ANALYTICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_ANALYTICS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def print_summary(ranked_data, days: int = 30):
    """Muestra un resumen ejecutivo por consola."""
    print("\n" + "=" * 78)
    print(f"📊 DATALARIA · REPORTE EJECUTIVO DE VISITAS (Últimos {days} días)")
    print("=" * 78)

    for lang, label in [("es", "🇪🇸 ESPAÑOL"), ("en", "🇬🇧 ENGLISH")]:
        posts = ranked_data.get(lang, [])
        print(f"\n{label} ({len(posts)} artículos con tráfico registrado):")
        print("-" * 78)
        print(f"{'#':<3} | {'Slug del Post':<46} | {'Vistas':<7} | {'Usuarios':<8} | {'Dur. Media'}")
        print("-" * 78)

        if not posts:
            print("   Sin visitas registradas en este periodo.")
        else:
            for item in posts[:5]:
                min_sec = f"{int(item['avg_duration_sec'] // 60)}m {int(item['avg_duration_sec'] % 60)}s"
                print(
                    f"{item['rank']:<3} | "
                    f"{item['slug'][:46]:<46} | "
                    f"{item['views']:<7} | "
                    f"{item['users']:<8} | "
                    f"{min_sec}"
                )

    print("\n" + "=" * 78)


def main():
    property_id = os.environ.get("GA4_PROPERTY_ID", DEFAULT_PROPERTY_ID)
    days = int(os.environ.get("GA4_DAYS", 30))

    print(f"🚀 Conectando con Google Analytics 4 (Propiedad: {property_id})...")

    try:
        response = fetch_ga4_data(property_id, days)
    except Exception as e:
        print(f"❌ Error al consultar GA4: {e}")
        sys.exit(1)

    ranked_data = parse_posts_data(response)
    print_summary(ranked_data, days)

    print("📝 Actualizando config.yaml (sección mostRead)...")
    if update_config_yaml(ranked_data, top_n=3):
        print("   ✅ config.yaml actualizado correctamente.")
    else:
        print("   ⚠️ No se pudo actualizar config.yaml automáticamente.")

    print("💾 Guardando data/analytics.json...")
    save_analytics_json(ranked_data, days)
    print("   ✅ data/analytics.json generado.")

    print("\n✨ Sincronización de analíticas completada con éxito.\n")


if __name__ == "__main__":
    main()
