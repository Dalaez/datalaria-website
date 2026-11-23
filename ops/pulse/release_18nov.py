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
  3. --activate [--checkout-url <URL>] [--dry-run]:
     (Para uso el 18-11-2026) Descongela atómicamente la app y publica el kit en kits.yaml.
"""

import sys
import re
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PACKAGES_DIR = ROOT_DIR / "packages" / "pulse"
STAGED_CARD_PATH = PACKAGES_DIR / "staged_pack_pulse_18nov.json"
DEFAULT_CHECKOUT_URL = "https://datalaria.lemonsqueezy.com/checkout/buy/3aac3253-2081-44b5-af4d-c0ecfc257be0?embed=1"


def get_staged_pack_data(checkout_url: str = DEFAULT_CHECKOUT_URL) -> Dict[str, Any]:
    """Retorna la ficha comercial completa de pack-pulse para data/pulse/kits.yaml."""
    return {
        "id": "pack-pulse",
        "slug": "pack-pulse-content-ops",
        "type": "kit",
        "topic": "software",
        "category": "Software, IA & SDD",
        "category_es": "Software, IA & SDD",
        "category_en": "Software, AI & SDD",
        "status": "available",
        "price": "19€",
        "original_price": "39€",
        "icon": "📊",
        "checkout_url": checkout_url,
        "title_es": "Datalaria Pulse: Content Ops & Notion Migration Kit",
        "title_en": "Datalaria Pulse: Content Ops & Notion Migration Kit",
        "description_es": "Toolkit comercial Dual (ES/EN) para equipos editoriales: Plantillas maestras Excel automatizadas con 6 hojas, tablas nativas y filtros, conectores Power Query M duales (Notion CSV & Git public.json), script CLI de migración y Guía ejecutiva PDF de 5 páginas.",
        "description_en": "Commercial Dual Toolkit (ES/EN) for editorial teams: Automated master Excel workbooks with 6 sheets, native Tables and AutoFilters, dual Power Query M connectors (Notion CSV & Git public.json), Python migration CLI, and 5-page Executive PDF Guide.",
        "preview_image_es": "/images/recursos/pulse-preview-es.png",
        "preview_image_en": "/images/recursos/pulse-preview-en.png",
        "article_url_es": "/es/posts/pulse-parte1-adios-notion-content-ops/",
        "article_url_en": "/en/posts/pulse-part1-goodbye-notion-content-ops/",
        "guide_url_es": "/es/posts/pulse-parte1-adios-notion-content-ops/",
        "guide_url_en": "/en/posts/pulse-part1-goodbye-notion-content-ops/",
        "deliverables_es": [
            "Plantilla Excel Dual Automatizada (ES & EN)",
            "Doble Conector Power Query M (Notion & Git)",
            "Migrador CLI + Guías Ejecutivas PDF (5 págs)"
        ],
        "deliverables_en": [
            "Dual Automated Excel Workbook (ES & EN)",
            "Dual Power Query M Connectors (Notion & Git)",
            "CLI Migration Engine + Executive PDF Guides"
        ],
        "features_es": [
            "Edición Dual completa (ES/EN) con estructura independiente en carpetas ES/ y EN/ para descarga y uso inmediato",
            "Plantillas Maestras Excel (.xlsx) con 6 hojas automatizadas, tablas nativas con filtros por columna, paneles congelados, Kanban dinámico y Dashboard ejecutivo sin macros VBA",
            "Doble conector Power Query M bilingüe: sincronización en 1 clic desde Notion CSV y desde public.json de repositorios Git",
            "Script de migración determinista en Python (migrate_notion.py) con soporte multi-idioma (--lang es/en), exportación directa a .xlsx, .yaml o .json y dataset de prueba",
            "Escáner universal de repositorios (pulse_repo_scanner.py) con cero dependencias externas para auditorías editoriales y CI/CD",
            "Guía ejecutiva maquetada en PDF de 5 páginas A4 y especificaciones técnicas de campos canónicos (ESPECIFICACION_CAMPOS_ES.md y FIELD_SPECIFICATION_EN.md)"
        ],
        "features_en": [
            "Complete Dual Edition (ES/EN) organized into standalone ES/ and EN/ directories for immediate deployment",
            "Automated Master Excel Workbooks (.xlsx) with 6 sheets, native tables with column filters, freeze panes, live Kanban, and executive Dashboard without VBA macros",
            "Bilingual Power Query M connectors: 1-click synchronization from Notion CSV exports and Git public.json manifests",
            "Deterministic Python migration engine (migrate_notion.py) with multi-language support (--lang es/en), direct export to .xlsx, .yaml or .json + test dataset",
            "Universal zero-dependency repository scanner (pulse_repo_scanner.py) for editorial audits and CI/CD pipelines",
            "Executive 5-page A4 PDF guide and canonical data dictionary specifications (ESPECIFICACION_CAMPOS_ES.md & FIELD_SPECIFICATION_EN.md)"
        ],
        "publish_date": "2026-11-18",
        "version": "v1.0.0"
    }


def _check_staged_card_and_artifacts(errors: List[str]) -> None:
    """Valida la definición staged y la existencia física de los artefactos del lanzamiento."""
    if not STAGED_CARD_PATH.exists():
        errors.append(f"Falta el archivo staged card: {STAGED_CARD_PATH}")
    else:
        try:
            staged_json = json.loads(STAGED_CARD_PATH.read_text(encoding="utf-8"))
            if staged_json.get("article_url_es") != "/es/posts/pulse-parte1-adios-notion-content-ops/":
                errors.append(f"staged card article_url_es DEBE apuntar a pulse-parte1, no a {staged_json.get('article_url_es')}")
            if staged_json.get("guide_url_es") != "/es/posts/pulse-parte1-adios-notion-content-ops/":
                errors.append(f"staged card guide_url_es DEBE apuntar a pulse-parte1, no a {staged_json.get('guide_url_es')}")
        except Exception as e:
            errors.append(f"Error leyendo staged card {STAGED_CARD_PATH}: {e}")

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


def verify_live_launch() -> Tuple[bool, List[str]]:
    """Verifica que Datalaria Pulse v1.0.0 está correctamente activado en modo live con su URL real de Lemon Squeezy."""
    errors: List[str] = []
    checkout_id = "3aac3253-2081-44b5-af4d-c0ecfc257be0"

    pulse_yaml = ROOT_DIR / "data" / "apps" / "pulse.yaml"
    if not pulse_yaml.exists():
        errors.append(f"Falta el archivo: {pulse_yaml}")
    else:
        text = pulse_yaml.read_text(encoding="utf-8")
        if "status: live" not in text or "status: incubating" in text:
            errors.append("data/apps/pulse.yaml DEBE tener 'status: live' tras la activación.")
        if not re.search(r"current_version:\s*v1\.\d+\.\d+", text):
            errors.append("data/apps/pulse.yaml DEBE tener una versión 'current_version: v1.x.y' válida.")

    for lang in ["es", "en"]:
        app_page = ROOT_DIR / "content" / lang / "apps" / "pulse" / "index.md"
        if not app_page.exists():
            errors.append(f"Falta el archivo: {app_page}")
        else:
            text = app_page.read_text(encoding="utf-8")
            if "draft: false" not in text:
                errors.append(f"{app_page} DEBE tener 'draft: false' tras la activación.")

    kits_yaml = ROOT_DIR / "data" / "pulse" / "kits.yaml"
    if not kits_yaml.exists():
        errors.append(f"Falta el archivo: {kits_yaml}")
    else:
        text = kits_yaml.read_text(encoding="utf-8")
        if "id: pack-pulse" not in text:
            errors.append("data/pulse/kits.yaml DEBE contener 'id: pack-pulse' tras la activación.")
        if checkout_id not in text:
            errors.append("data/pulse/kits.yaml DEBE incluir la URL oficial de checkout de Lemon Squeezy.")

    recursos_catalog = ROOT_DIR / "layouts" / "partials" / "recursos_catalog.html"
    if not recursos_catalog.exists():
        errors.append(f"Falta el archivo: {recursos_catalog}")
    else:
        text = recursos_catalog.read_text(encoding="utf-8")
        if 'id="pack-pulse"' not in text:
            errors.append("layouts/partials/recursos_catalog.html DEBE contener 'id=\"pack-pulse\"' tras la activación.")
        if checkout_id not in text:
            errors.append("layouts/partials/recursos_catalog.html DEBE incluir la URL oficial de checkout de Lemon Squeezy.")

    index_profile = ROOT_DIR / "layouts" / "partials" / "index_profile.html"
    if index_profile.exists() and '"slug" "pulse"' not in index_profile.read_text(encoding="utf-8"):
        errors.append("layouts/partials/index_profile.html DEBE listar 'pulse' en la sección de Apps.")

    _check_staged_card_and_artifacts(errors)
    return (len(errors) == 0, errors)


def verify_embargo() -> Tuple[bool, List[str]]:
    """Verifica el embargo pre-18N o, si Pulse ya está en status: live, delega en verify_live_launch()."""
    errors: List[str] = []

    # 1. Verificar data/apps/pulse.yaml
    pulse_yaml = ROOT_DIR / "data" / "apps" / "pulse.yaml"
    if not pulse_yaml.exists():
        errors.append(f"Falta el archivo: {pulse_yaml}")
    else:
        text = pulse_yaml.read_text(encoding="utf-8")
        if "status: live" in text:
            return verify_live_launch()
        if "status: incubating" not in text:
            errors.append("data/apps/pulse.yaml DEBE tener 'status: incubating' durante el embargo.")
        if not re.search(r"current_version:\s*v1\.\d+\.\d+", text):
            errors.append("data/apps/pulse.yaml DEBE tener una versión 'current_version: v1.x.y' válida.")

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
    pulse_pairs = [
        ("content/es/posts/pulse-parte1-adios-notion-content-ops", "content/en/posts/pulse-part1-goodbye-notion-content-ops"),
        ("content/es/posts/pulse-parte2-indexador-pydantic-paridad-ci", "content/en/posts/pulse-part2-pydantic-indexer-bilingual-parity-ci"),
        ("content/es/posts/pulse-parte3-tablero-react-tabla-kanban-calendario", "content/en/posts/pulse-part3-react-dashboard-table-kanban-calendar"),
        ("content/es/posts/pulse-parte4-ga4-search-console-automatico", "content/en/posts/pulse-part4-ga4-search-console-automated"),
        ("content/es/posts/pulse-parte5-kit-excel-migracion-notion-equipos", "content/en/posts/pulse-part5-excel-kit-notion-migration-teams"),
    ]
    for es_path, en_path in pulse_pairs:
        for rel_dir in [es_path, en_path]:
            p = ROOT_DIR / rel_dir / "index.md"
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

    # 5 y 6. Validar staged card y artefactos
    _check_staged_card_and_artifacts(errors)

    return (len(errors) == 0, errors)


def prepare_staged_card(checkout_url: str = DEFAULT_CHECKOUT_URL) -> Path:
    """Genera packages/pulse/staged_pack_pulse_18nov.json con los metadatos comerciales."""
    data = get_staged_pack_data(checkout_url=checkout_url)
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    with open(STAGED_CARD_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[STAGED CARD] Guardada definición en: {STAGED_CARD_PATH.resolve()}")
    return STAGED_CARD_PATH


def activate_launch(checkout_url: str = DEFAULT_CHECKOUT_URL, root_dir: Path = ROOT_DIR, dry_run: bool = False) -> Dict[str, Any]:
    """
    Descongela atómicamente la app y publica el kit pack-pulse en kits.yaml, recursos_catalog y index_profile.
    Si dry_run=True, calcula las mutaciones sin escribir en disco.
    """
    changes: Dict[str, Any] = {
        "pulse_yaml_updated": False,
        "content_pages_unembargoed": [],
        "kits_yaml_updated": False,
        "recursos_catalog_updated": False,
        "index_profile_updated": False,
    }

    # 1. data/apps/pulse.yaml -> status: live
    pulse_yaml_file = root_dir / "data" / "apps" / "pulse.yaml"
    if pulse_yaml_file.exists():
        content = pulse_yaml_file.read_text(encoding="utf-8")
        if "status: incubating" in content:
            new_content = content.replace("status: incubating", "status: live")
            if not dry_run:
                pulse_yaml_file.write_text(new_content, encoding="utf-8")
            changes["pulse_yaml_updated"] = True

    # 2. content/{es,en}/apps/pulse/index.md -> draft: false
    for lang in ["es", "en"]:
        p = root_dir / "content" / lang / "apps" / "pulse" / "index.md"
        if p.exists():
            content = p.read_text(encoding="utf-8")
            if "draft: true" in content:
                new_content = content.replace("draft: true", "draft: false")
                if not dry_run:
                    p.write_text(new_content, encoding="utf-8")
                changes["content_pages_unembargoed"].append(
                    str(p.relative_to(root_dir) if p.is_relative_to(root_dir) else p.name)
                )

    # 3. data/pulse/kits.yaml -> insertar pack-pulse antes de pack-sdd
    kits_yaml_file = root_dir / "data" / "pulse" / "kits.yaml"
    if kits_yaml_file.exists():
        kits_text = kits_yaml_file.read_text(encoding="utf-8")
        if "id: pack-pulse" not in kits_text:
            pack_data = get_staged_pack_data(checkout_url=checkout_url)
            pack_yaml_block = (
                f"- id: {pack_data['id']}\n"
                f"  slug: {pack_data['slug']}\n"
                f"  type: {pack_data['type']}\n"
                f"  topic: {pack_data['topic']}\n"
                f"  category_es: {pack_data['category_es']}\n"
                f"  status: {pack_data['status']}\n"
                f"  price: {pack_data['price']}\n"
                f"  original_price: {pack_data['original_price']}\n"
                f"  icon: {pack_data['icon']}\n"
                f"  deliverables_es:\n"
                f"  - {pack_data['deliverables_es'][0]}\n"
                f"  - {pack_data['deliverables_es'][1]}\n"
                f"  - {pack_data['deliverables_es'][2]}\n"
                f"  features_es:\n"
                + "".join([f"  - {f}\n" for f in pack_data['features_es']])
                + f"  checkout_url: {pack_data['checkout_url']}\n"
                f"  title_es: '{pack_data['title_es']}'\n"
                f"  description_es: '{pack_data['description_es']}'\n"
                f"  article_url_es: {pack_data['article_url_es']}\n"
                f"  guide_url_es: {pack_data['guide_url_es']}\n"
                f"  title_en: '{pack_data['title_en']}'\n"
                f"  category_en: {pack_data['category_en']}\n"
                f"  description_en: '{pack_data['description_en']}'\n"
                f"  deliverables_en:\n"
                f"  - {pack_data['deliverables_en'][0]}\n"
                f"  - {pack_data['deliverables_en'][1]}\n"
                f"  - {pack_data['deliverables_en'][2]}\n"
                f"  features_en:\n"
                + "".join([f"  - {f}\n" for f in pack_data['features_en']])
                + f"  article_url_en: {pack_data['article_url_en']}\n"
                f"  guide_url_en: {pack_data['guide_url_en']}\n"
                f"  publish_date: '{pack_data['publish_date']}'\n"
                f"  version: {pack_data['version']}\n"
            )
            if "- id: pack-sdd" in kits_text:
                new_kits_text = kits_text.replace("- id: pack-sdd", pack_yaml_block + "- id: pack-sdd")
            else:
                new_kits_text = kits_text + "\n" + pack_yaml_block
            if not dry_run:
                kits_yaml_file.write_text(new_kits_text, encoding="utf-8")
            changes["kits_yaml_updated"] = True

    # 4. layouts/partials/recursos_catalog.html -> inyectar pack-pulse
    recursos_cat_file = root_dir / "layouts" / "partials" / "recursos_catalog.html"
    if recursos_cat_file.exists():
        cat_text = recursos_cat_file.read_text(encoding="utf-8")
        if "pack-pulse" not in cat_text:
            pack_data = get_staged_pack_data(checkout_url=checkout_url)
            # HTML Card ES
            es_card_html = (
                '<div class="kit-card" id="pack-pulse">\n'
                '<div>\n'
                '<div class="kit-card-head">\n'
                '<div class="kit-card-icon">📊</div>\n'
                '<div class="kit-card-title-wrap">\n'
                '<div class="kit-card-meta">\n'
                '<span class="kit-card-cat">Software, IA & SDD</span>\n'
                '<span class="kit-status-badge avail">🟢 Disponible</span>\n'
                '</div>\n'
                f'<h3 class="kit-card-title">{pack_data["title_es"]}</h3>\n'
                '</div>\n'
                '</div>\n'
                f'<p class="kit-card-desc">{pack_data["description_es"]}</p>\n'
                '<div class="kit-deliverables-row">\n'
                '<span class="deliv-chip">Excel Dual ES/EN</span>\n'
                '<span class="deliv-chip">Power Query M</span>\n'
                '<span class="deliv-chip">Guía PDF 5p + CLI</span>\n'
                '</div>\n'
                '</div>\n'
                '<div class="kit-card-foot">\n'
                '<div class="kit-pricing-box">\n'
                f'<span class="kit-price-curr">{pack_data["price"]}</span>\n'
                f'<span class="kit-price-orig">{pack_data["original_price"]}</span>\n'
                '</div>\n'
                '<div class="kit-btns-group">\n'
                '<button type="button" class="btn-kit-info" onclick="openModal(\'pack-pulse\')">\n'
                'Detalles ℹ️\n'
                '</button>\n'
                f'<a href="{pack_data["article_url_es"]}" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>\n'
                f'<a href="{checkout_url}" class="btn-kit-buy lemonsqueezy-button">Descargar →</a>\n'
                '</div>\n'
                '</div>\n'
                '</div>\n\n'
            )

            # HTML Card EN
            en_card_html = (
                '<div class="kit-card" id="pack-pulse">\n'
                '<div>\n'
                '<div class="kit-card-head">\n'
                '<div class="kit-card-icon">📊</div>\n'
                '<div class="kit-card-title-wrap">\n'
                '<div class="kit-card-meta">\n'
                '<span class="kit-card-cat">Software, AI & SDD</span>\n'
                '<span class="kit-status-badge avail">🟢 Available</span>\n'
                '</div>\n'
                f'<h3 class="kit-card-title">{pack_data["title_en"]}</h3>\n'
                '</div>\n'
                '</div>\n'
                f'<p class="kit-card-desc">{pack_data["description_en"]}</p>\n'
                '<div class="kit-deliverables-row">\n'
                '<span class="deliv-chip">Dual ES/EN Excel</span>\n'
                '<span class="deliv-chip">Power Query M</span>\n'
                '<span class="deliv-chip">5p PDF + CLI</span>\n'
                '</div>\n'
                '</div>\n'
                '<div class="kit-card-foot">\n'
                '<div class="kit-pricing-box">\n'
                f'<span class="kit-price-curr">{pack_data["price"]}</span>\n'
                f'<span class="kit-price-orig">{pack_data["original_price"]}</span>\n'
                '</div>\n'
                '<div class="kit-btns-group">\n'
                '<button type="button" class="btn-kit-info" onclick="openModal(\'pack-pulse\')">\n'
                'Details ℹ️\n'
                '</button>\n'
                f'<a href="{pack_data["article_url_en"]}" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>\n'
                f'<a href="{checkout_url}" class="btn-kit-buy lemonsqueezy-button">Download →</a>\n'
                '</div>\n'
                '</div>\n'
                '</div>\n\n'
            )

            # KITS_DATA JS object ES
            es_js_payload = {
                "id": "pack-pulse",
                "title": pack_data["title_es"],
                "topic": "software",
                "topicLabel": pack_data["category_es"],
                "status": "available",
                "statusLabel": "🟢 DISPONIBLE • Content Ops",
                "price": pack_data["price"],
                "origPrice": pack_data["original_price"],
                "icon": pack_data["icon"],
                "delivs": pack_data["deliverables_es"],
                "desc": pack_data["description_es"],
                "features": pack_data["features_es"],
                "checkoutUrl": checkout_url,
                "guideUrl": pack_data["guide_url_es"],
                "previewImg": pack_data["preview_image_es"],
            }
            es_js_obj = "  " + json.dumps(es_js_payload, indent=2, ensure_ascii=False).replace("\n", "\n  ") + ",\n"

            # KITS_DATA JS object EN
            en_js_payload = {
                "id": "pack-pulse",
                "title": pack_data["title_en"],
                "topic": "software",
                "topicLabel": pack_data["category_en"],
                "status": "available",
                "statusLabel": "🟢 AVAILABLE • Content Ops",
                "price": pack_data["price"],
                "origPrice": pack_data["original_price"],
                "icon": pack_data["icon"],
                "delivs": pack_data["deliverables_en"],
                "desc": pack_data["description_en"],
                "features": pack_data["features_en"],
                "checkoutUrl": checkout_url,
                "guideUrl": pack_data["guide_url_en"],
                "previewImg": pack_data["preview_image_en"],
            }
            en_js_obj = "  " + json.dumps(en_js_payload, indent=2, ensure_ascii=False).replace("\n", "\n  ") + ",\n"

            new_cat_text = cat_text
            # Counters ES
            new_cat_text = new_cat_text.replace("Mostrando 14 Kits (13 Disponibles)", "Mostrando 15 Kits (14 Disponibles)")
            new_cat_text = new_cat_text.replace("✨ Todos los Kits <span class=\"pill-count\">14</span>", "✨ Todos los Kits <span class=\"pill-count\">15</span>")
            new_cat_text = new_cat_text.replace("💻 Software, IA & SDD <span class=\"pill-count\">1</span>", "💻 Software, IA & SDD <span class=\"pill-count\">2</span>")
            new_cat_text = new_cat_text.replace("Todos (14)", "Todos (15)")
            new_cat_text = new_cat_text.replace("🟢 Disponibles (13)", "🟢 Disponibles (14)")

            # Counters EN
            new_cat_text = new_cat_text.replace("Showing 14 Kits (13 Available)", "Showing 15 Kits (14 Available)")
            new_cat_text = new_cat_text.replace("✨ All Kits <span class=\"pill-count\">14</span>", "✨ All Kits <span class=\"pill-count\">15</span>")
            new_cat_text = new_cat_text.replace("💻 Software, AI & SDD <span class=\"pill-count\">1</span>", "💻 Software, AI & SDD <span class=\"pill-count\">2</span>")
            new_cat_text = new_cat_text.replace("All (14)", "All (15)")
            new_cat_text = new_cat_text.replace("🟢 Available (13)", "🟢 Available (14)")

            parts = new_cat_text.split("{{- else -}}")
            if len(parts) == 2:
                es_section = parts[0]
                en_section = parts[1]

                es_section = es_section.replace('<div class="kit-card is-locked" id="pack-sdd">', es_card_html + '<div class="kit-card is-locked" id="pack-sdd">')
                es_section = es_section.replace('{\n    "id": "pack-sdd",', es_js_obj + '{\n    "id": "pack-sdd",')

                en_section = en_section.replace('<div class="kit-card is-locked" id="pack-sdd">', en_card_html + '<div class="kit-card is-locked" id="pack-sdd">')
                en_section = en_section.replace('{\n    "id": "pack-sdd",', en_js_obj + '{\n    "id": "pack-sdd",')

                new_cat_text = es_section + "{{- else -}}" + en_section
            else:
                new_cat_text = new_cat_text.replace('<div class="kit-card is-locked" id="pack-sdd">', es_card_html + '<div class="kit-card is-locked" id="pack-sdd">')
                new_cat_text = new_cat_text.replace('{\n    "id": "pack-sdd",', es_js_obj + '{\n    "id": "pack-sdd",')

            if not dry_run:
                recursos_cat_file.write_text(new_cat_text, encoding="utf-8")
                gen_script = root_dir / "scripts" / "generate_recursos_pages.py"
                if gen_script.exists():
                    subprocess.run([sys.executable, str(gen_script)], cwd=str(root_dir), check=False)
            changes["recursos_catalog_updated"] = True

    # 5. layouts/partials/index_profile.html -> inyectar pulse en $apps y bump b2b
    index_profile_file = root_dir / "layouts" / "partials" / "index_profile.html"
    if index_profile_file.exists():
        prof_text = index_profile_file.read_text(encoding="utf-8")
        if '"slug" "pulse"' not in prof_text and 'slug "pulse"' not in prof_text:
            pulse_app_dict = (
                '  (dict "slug" "pulse" "icon" "📊" "name" "Datalaria Pulse" "url" "/apps/pulse/" "arcade" false\n'
                '        "badge" (cond $isES "IA · B2B" "AI · B2B")\n'
                '        "badgeClass" "dlh-ai"\n'
                '        "desc" (cond $isES "Sistema de Content Ops as Code: gobierno editorial, paridad bilingüe, salud SEO y retorno orgánico sobre Git." "Content Ops as Code system: editorial governance, bilingual parity, SEO health, and organic ROI on Git.")\n'
                '        "cta" (cond $isES "Abrir app ↗" "Open app ↗"))\n'
            )
            target_hook = '(dict "slug" "obs-management"'
            if target_hook in prof_text:
                new_prof_text = prof_text.replace(target_hook, pulse_app_dict + target_hook)
            else:
                new_prof_text = prof_text

            b2b_target = '(dict "key" "b2b"      "icon" "💼" "label" (cond $isES "Suites B2B & IA Operacional" "B2B Suites & AI")     "count" 1)'
            b2b_replace = '(dict "key" "b2b"      "icon" "💼" "label" (cond $isES "Suites B2B & IA Operacional" "B2B Suites & AI")     "count" 2)'
            new_prof_text = new_prof_text.replace(b2b_target, b2b_replace)

            if not dry_run:
                index_profile_file.write_text(new_prof_text, encoding="utf-8")
            changes["index_profile_updated"] = True

    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Gobernador de Embargo y Lanzamiento 18-Nov de Datalaria Pulse")
    parser.add_argument("--verify-embargo", action="store_true", help="Verifica reglas de embargo o estado live si ya se activó")
    parser.add_argument("--verify-live", action="store_true", help="Exige que el lanzamiento live esté activo con checkout URL real")
    parser.add_argument("--prepare-staged-card", action="store_true", help="Genera staged_pack_pulse_18nov.json")
    parser.add_argument("--activate", action="store_true", help="Activa el lanzamiento comercial (18 Nov)")
    parser.add_argument("--checkout-url", type=str, default=None, help="URL de checkout definitiva de Lemon Squeezy")
    parser.add_argument("--dry-run", action="store_true", help="Simula la activación sin modificar archivos en disco")

    args = parser.parse_args()

    if args.prepare_staged_card:
        prepare_staged_card()

    if args.activate:
        checkout = args.checkout_url or DEFAULT_CHECKOUT_URL
        print("\n=== ACTIVACIÓN COMERCIAL (DATALARIA PULSE — 18 NOV 2026) ===")
        print(f"Modo: {'SIMULACIÓN (DRY-RUN)' if args.dry_run else 'EJECUCIÓN REAL'}")
        print(f"Checkout URL: {checkout}")
        res = activate_launch(checkout_url=checkout, root_dir=ROOT_DIR, dry_run=args.dry_run)
        print("Resultados de la activación:")
        for k, v in res.items():
            print(f"  - {k}: {v}")
        print()

    if args.verify_live:
        print("\n=== VERIFICACIÓN DE LANZAMIENTO LIVE (DATALARIA PULSE v1.0.0) ===")
        ok, errors = verify_live_launch()
        if ok:
            print("[OK] Lanzamiento Live verificado al 100%: status=live, draft=false, pack-pulse activo con Lemon Squeezy.\n")
        else:
            print("[ERROR] Fallos en la activación Live:")
            for err in errors:
                print(f"  x {err}")
            print()
            sys.exit(1)

    elif args.verify_embargo or not (args.prepare_staged_card or args.activate):
        is_live = (ROOT_DIR / "data" / "apps" / "pulse.yaml").exists() and "status: live" in (
            ROOT_DIR / "data" / "apps" / "pulse.yaml"
        ).read_text(encoding="utf-8")
        if is_live:
            print("\n=== VERIFICACIÓN POST-EMBARGO / MODO LIVE (DATALARIA PULSE v1.0.0) ===")
            ok, errors = verify_live_launch()
            if ok:
                print("[OK] Pulse activo en modo LIVE y artefactos verificados al 100%:")
                print("  - App status: live en data/apps/pulse.yaml (v1.0.0)")
                print("  - Fichas de app: draft: false en ES y EN")
                print("  - Catálogo público: pack-pulse activo con Lemon Squeezy URL real")
                print("  - Entregables comerciales: Datalaria_Pulse_Kit.zip y previews listos\n")
            else:
                print("[ERROR] Se encontraron fallos en modo LIVE:")
                for err in errors:
                    print(f"  x {err}")
                print()
                sys.exit(1)
        else:
            print("\n=== VERIFICACIÓN DE EMBARGO COMERCIAL (DATALARIA PULSE — 18 NOV 2026) ===")
            ok, errors = verify_embargo()
            if ok:
                print("[OK] Embargo comercial verificado al 100%:")
                print("  - App status: incubating en data/apps/pulse.yaml (v1.0.0)")
                print("  - Fichas de app: draft: true en ES y EN")
                print("  - Posts de la serie: programados para >= 2026-11-18")
                print("  - Catálogo público: pack-pulse embargado (no expuesto)")
                print("  - Staged card: packages/pulse/staged_pack_pulse_18nov.json verificado")
                print("  - Entregables comerciales: Datalaria_Pulse_Kit.zip y previews listos\n")
            else:
                print("[ERROR] Se encontraron fallos de embargo comercial:")
                for err in errors:
                    print(f"  x {err}")
                print()
                sys.exit(1)


if __name__ == "__main__":
    main()
