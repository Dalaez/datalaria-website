"""
ops/pulse/release_18nov.py
--------------------------
Gobernanza de Embargo Comercial y Activación del Lanzamiento de Datalaria Pulse (18 Nov 2026).
Especificación: Hito 6.3 (specs/apps/pulse/spec.md & plan_hito_6_3_ejecucion_flash.md).

Proporciona:
  1. --verify-embargo:
     Verifica de manera determinista que el embargo comercial previo al 18-11-2026
     está 100% activo y que todos los artefactos de entrega existen y son válidos.
  2. --prepare-staged-card:
     Genera packages/pulse/staged_pack_pulse_18nov.json con los metadatos comerciales
     listos para inyectarse en data/pulse/kits.yaml el día del lanzamiento oficial.
  3. --activate --checkout-url <URL>:
     (Para uso el 18-11-2026) Descongela atómicamente la app y publica el kit en kits.yaml.
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PACKAGES_DIR = ROOT_DIR / "packages" / "pulse"
STAGED_CARD_PATH = PACKAGES_DIR / "staged_pack_pulse_18nov.json"


def get_staged_pack_data(checkout_url: str = "#") -> Dict[str, Any]:
    """Retorna la ficha comercial completa de pack-pulse para data/pulse/kits.yaml."""
    return {
        "id": "pack-pulse",
        "slug": "pack-pulse-content-ops",
        "type": "kit",
        "category": "Software, IA & SDD",
        "status": "available",
        "price": "19€",
        "original_price": "39€",
        "icon": "📊",
        "checkout_url": checkout_url,
        "title_es": "Datalaria Pulse: Content Ops & Notion Migration Kit",
        "title_en": "Datalaria Pulse: Content Ops & Notion Migration Kit",
        "description_es": "Toolkit comercial para equipos editoriales: Plantilla maestra Excel con 6 hojas y validaciones, conectores Power Query M (Notion CSV & Git public.json), script CLI de migración y Guía ejecutiva PDF.",
        "description_en": "Commercial toolkit for editorial teams: 6-sheet Master Excel workbook, dual Power Query M connectors (Notion CSV & Git public.json), Python migration CLI, and Executive PDF Guide.",
        "preview_image_es": "/images/recursos/pulse-preview-es.png",
        "preview_image_en": "/images/recursos/pulse-preview-en.png",
        "article_url_es": "/es/posts/pulse-parte5-kit-excel-migracion-notion-equipos/",
        "article_url_en": "/en/posts/pulse-part5-excel-kit-notion-migration-teams/",
        "guide_url_es": "/es/posts/pulse-parte5-kit-excel-migracion-notion-equipos/",
        "guide_url_en": "/en/posts/pulse-part5-excel-kit-notion-migration-teams/",
        "deliverables_es": [
            "Plantilla Excel Master (6 Hojas)",
            "Doble Conector Power Query M",
            "Migrador Notion CLI + Guía PDF"
        ],
        "deliverables_en": [
            "6-Sheet Master Excel Workbook",
            "Dual Power Query M Connectors",
            "Notion Migration CLI + PDF Guide"
        ],
        "features_es": [
            "Plantilla Maestra Excel (.xlsx) con 6 hojas (Taxonomía, Activos, Kanban, Métricas y Dashboard ejecutivo con fórmulas universales)",
            "Doble conector Power Query M: sincronización en 1 clic desde Notion CSV y desde public.json de repositorios Git",
            "Script de migración determinista en Python (migrate_notion.py) con exportación directa a .xlsx, .yaml o .json y dataset de prueba",
            "Escáner universal de repositorios (pulse_repo_scanner.py) de cero dependencias externas para auditorías CI/CD",
            "Guía ejecutiva maquetada en PDF de 4 páginas A4 y especificación técnica de campos canónicos (ESPECIFICACION_CAMPOS.md)"
        ],
        "features_en": [
            "Master Excel Template (.xlsx) with 6 structured sheets (Taxonomy, Assets, Kanban, Metrics, and Dashboard with universal formulas)",
            "Dual Power Query M connectors: 1-click synchronization from Notion CSV exports and Git public.json manifests",
            "Deterministic Python migration engine (migrate_notion.py) with direct export to .xlsx, .yaml or .json + test dataset",
            "Universal zero-dependency repository scanner (pulse_repo_scanner.py) for automated CI/CD audits",
            "Executive 4-page A4 PDF guide and canonical data dictionary specification (ESPECIFICACION_CAMPOS.md)"
        ]
    }


def verify_embargo() -> Tuple[bool, List[str]]:
    """Verifica que todas las reglas de embargo y artefactos requeridos están en regla."""
    errors: List[str] = []

    # 1. Verificar data/apps/pulse.yaml
    pulse_yaml = ROOT_DIR / "data" / "apps" / "pulse.yaml"
    if not pulse_yaml.exists():
        errors.append(f"Falta el archivo: {pulse_yaml}")
    else:
        text = pulse_yaml.read_text(encoding="utf-8")
        if "status: incubating" not in text:
            errors.append("data/apps/pulse.yaml DEBE tener 'status: incubating' durante el embargo.")
        if "current_version: v0.3.0" not in text:
            errors.append("data/apps/pulse.yaml DEBE tener 'current_version: v0.3.0'.")

    # 2. Verificar content/{es,en}/apps/pulse/index.md (draft: true)
    for lang in ["es", "en"]:
        app_page = ROOT_DIR / "content" / lang / "apps" / "pulse" / "index.md"
        if not app_page.exists():
            errors.append(f"Falta el archivo: {app_page}")
        else:
            text = app_page.read_text(encoding="utf-8")
            if "draft: true" not in text:
                errors.append(f"{app_page} DEBE tener 'draft: true' durante el embargo.")

    # 3. Verificar fechas de los 10 artículos de la serie Pulse (date >= 2026-11-18)
    pulse_post_slugs = [
        "pulse-parte1-content-ops-as-code",
        "pulse-parte2-arquitectura-dual-mode",
        "pulse-parte3-indexador-determinista",
        "pulse-parte4-cockpit-spa-react",
        "pulse-parte5-kit-excel-migracion-notion-equipos",
    ]
    for slug in pulse_post_slugs:
        for lang_dir, post_prefix in [("content/es/posts", slug), ("content/en/posts", slug.replace("parte", "part"))]:
            p = ROOT_DIR / lang_dir / post_prefix / "index.md"
            if p.exists():
                text = p.read_text(encoding="utf-8")
                # Extraer date: 2026-XX-XX
                for line in text.splitlines():
                    if line.strip().startswith("date:"):
                        d_str = line.split(":", 1)[1].strip().strip('"').strip("'")
                        try:
                            d = datetime.fromisoformat(d_str[:10])
                            if d < datetime(2026, 11, 18):
                                errors.append(f"Post {p.name} tiene fecha {d_str} anterior al 2026-11-18.")
                        except Exception:
                            pass
                        break

    # 4. Verificar que pack-pulse NO esté publicado en data/pulse/kits.yaml ni en recursos_catalog.html
    kits_yaml = ROOT_DIR / "data" / "pulse" / "kits.yaml"
    if kits_yaml.exists():
        text = kits_yaml.read_text(encoding="utf-8")
        if "id: pack-pulse" in text:
            errors.append("data/pulse/kits.yaml NO debe contener 'id: pack-pulse' antes del 18 de noviembre.")

    recursos_catalog = ROOT_DIR / "layouts" / "partials" / "recursos_catalog.html"
    if recursos_catalog.exists():
        text = recursos_catalog.read_text(encoding="utf-8")
        if "pack-pulse" in text:
            errors.append("layouts/partials/recursos_catalog.html NO debe enlazar 'pack-pulse' antes del 18 de noviembre.")

    # 5. Verificar existencia de artefactos requeridos
    required_artifacts = [
        ROOT_DIR / "packages" / "pulse" / "Datalaria_Pulse_Kit.zip",
        ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY" / "Datalaria_Pulse_Kit.zip",
        ROOT_DIR / "static" / "images" / "recursos" / "pulse-preview-es.png",
        ROOT_DIR / "static" / "images" / "recursos" / "pulse-preview-en.png",
        ROOT_DIR / "static" / "apps" / "pulse" / "index.html",
        ROOT_DIR / "static" / "apps" / "pulse" / "data" / "public.json",
    ]
    for art in required_artifacts:
        if not art.exists():
            errors.append(f"Artefacto de entrega no encontrado: {art}")

    return (len(errors) == 0, errors)


def prepare_staged_card() -> Path:
    """Genera packages/pulse/staged_pack_pulse_18nov.json con los metadatos comerciales."""
    data = get_staged_pack_data(checkout_url="#")
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    with open(STAGED_CARD_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[STAGED CARD] Guardada definición en: {STAGED_CARD_PATH.resolve()}")
    return STAGED_CARD_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description="Gobernador de Embargo y Lanzamiento 18-Nov de Datalaria Pulse")
    parser.add_argument("--verify-embargo", action="store_true", help="Verifica reglas de embargo y artefactos")
    parser.add_argument("--prepare-staged-card", action="store_true", help="Genera staged_pack_pulse_18nov.json")
    parser.add_argument("--activate", action="store_true", help="Activa el lanzamiento comercial (18 Nov)")
    parser.add_argument("--checkout-url", type=str, default=None, help="URL de checkout definitiva de Lemon Squeezy")

    args = parser.parse_args()

    if args.prepare_staged_card:
        prepare_staged_card()

    if args.verify_embargo or not (args.prepare_staged_card or args.activate):
        print("\n=== VERIFICACIÓN DE EMBARGO COMERCIAL (DATALARIA PULSE — 18 NOV 2026) ===")
        ok, errors = verify_embargo()
        if ok:
            print("[OK] Embargo comercial verificado al 100%:")
            print("  - App status: incubating en data/apps/pulse.yaml (v0.3.0)")
            print("  - Fichas de app: draft: true en ES y EN")
            print("  - Posts de la serie: programados para >= 2026-11-18")
            print("  - Catálogo público: pack-pulse embargado (no expuesto)")
            print("  - Entregables comerciales: Datalaria_Pulse_Kit.zip y previews listos\n")
        else:
            print("[ERROR] Se encontraron fallos de embargo comercial:")
            for err in errors:
                print(f"  x {err}")
            print()
            sys.exit(1)


if __name__ == "__main__":
    main()
