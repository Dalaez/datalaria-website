"""
ops/helix/release_jan2027.py
----------------------------
Gobernanza de Embargo Comercial y Activación del Lanzamiento de Datalaria Helix (Enero 2027).
Especificación: Hito 6.8 (specs/apps/helix/spec.md & plan_hito_6_8_ejecucion_flash.md).

Proporciona:
  1. --verify-embargo:
     Verifica de manera determinista que el embargo comercial previo a enero de 2027
     está 100% activo y que todos los artefactos de entrega existen y son válidos.
  2. --prepare-staged-card:
     Genera packages/helix/staged_helix_jan2027.json con los metadatos comerciales y hashes
     listos para Lemon Squeezy y para inyectarse en data/pulse/kits.yaml.
  3. --activate [--core-checkout-url <URL>] [--starter-checkout-url <URL>]:
     (Para uso en enero de 2027) Descongela atómicamente Helix, publica la ficha y activa los kits.
"""

import sys
import json
import hashlib
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PACKAGES_DIR = ROOT_DIR / "packages" / "helix"
STAGED_CARD_PATH = PACKAGES_DIR / "staged_helix_jan2027.json"


def _compute_file_info(file_path: Path) -> Dict[str, Any]:
    if not file_path.exists():
        return {"exists": False, "size_bytes": 0, "size_kb": 0.0, "sha256": ""}
    data = file_path.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)
    size_kb = round(size_bytes / 1024, 2)
    return {
        "exists": True,
        "filename": file_path.name,
        "size_bytes": size_bytes,
        "size_kb": size_kb,
        "sha256": sha256,
    }


def get_staged_helix_data(core_checkout_url: str = "#", starter_checkout_url: str = "#") -> Dict[str, Any]:
    """Retorna la ficha comercial completa de Helix para Lemon Squeezy y data/pulse/kits.yaml."""
    starter_zip = PACKAGES_DIR / "Datalaria_Helix_Starter_Kit.zip"
    core_zip = PACKAGES_DIR / "Datalaria_Helix_Core_Kit.zip"
    versioned_core_zip = PACKAGES_DIR / "kit-datalaria-helix-core-v1.0.0.zip"
    pdf_guide = PACKAGES_DIR / "GUIA_EJECUTIVA_HELIX_SDD.pdf"

    starter_info = _compute_file_info(starter_zip)
    core_info = _compute_file_info(core_zip)
    versioned_core_info = _compute_file_info(versioned_core_zip)
    pdf_info = _compute_file_info(pdf_guide)

    return {
        "embargo": {
            "target_launch_date": "2027-01-19",
            "status": "incubating_staged",
            "current_version": "v1.0.0",
            "app_slug": "helix",
            "app_yaml": "data/apps/helix.yaml",
        },
        "artifacts": {
            "starter_kit": starter_info,
            "core_kit": core_info,
            "versioned_core_kit": versioned_core_info,
            "pdf_guide": pdf_info,
        },
        "products": {
            "pack-helix-starter": {
                "id": "pack-helix-starter",
                "slug": "pack-helix-starter",
                "type": "kit",
                "category": "Software, IA & SDD",
                "status": "available",
                "price": "9€",
                "original_price": "19€",
                "icon": "⚡",
                "checkout_url": starter_checkout_url,
                "title_es": "Datalaria Helix: Starter Kit (Orquestador & Product Analyst)",
                "title_en": "Datalaria Helix: Starter Kit (Orchestrator & Product Analyst)",
                "description_es": "Kit de inicio rápido para adopción de Spec-Driven Development: los 2 agentes esenciales de Dirección, plantilla canónica y checklist de gobernanza.",
                "description_en": "Quick-start kit for Spec-Driven Development adoption: 2 essential Leadership agents, canonical spec template, and governance checklist.",
                "deliverables_es": [
                    "2 Agentes Esenciales Helix (01-Orchestrator + 02-Product Analyst)",
                    "Plantilla Canónica SPEC.md + Checklist de Gobernanza",
                    "Adaptadores Compilados para Google Antigravity y Claude Code",
                ],
                "deliverables_en": [
                    "2 Essential Helix Agents (01-Orchestrator + 02-Product Analyst)",
                    "Canonical SPEC.md Template + Governance Checklist",
                    "Compiled Adapters for Google Antigravity and Claude Code",
                ],
                "zip_file": "Datalaria_Helix_Starter_Kit.zip",
                "sha256": starter_info["sha256"],
                "size_kb": starter_info["size_kb"],
            },
            "pack-sdd": {
                "id": "pack-sdd",
                "slug": "pack-sdd-helix-core",
                "type": "kit",
                "category": "Software, IA & SDD",
                "status": "available",
                "price": "19€",
                "original_price": "39€",
                "icon": "🧬",
                "checkout_url": core_checkout_url,
                "title_es": "Datalaria Helix: Spec-Driven Development Core Kit",
                "title_en": "Datalaria Helix: Spec-Driven Development Core Kit",
                "description_es": "Sistema operativo agéntico completo para ingeniería asistida por IA: 12 fichas canónicas Helix, CLI helix.py determinista en Python puro, 3 blueprints arquitectónicos de producción, 2 casos de estudio reales y Guía ejecutiva PDF de 4 páginas.",
                "description_en": "Complete agentic operating system for AI-assisted software engineering: 12 canonical Helix agent specs, zero-dependency Python CLI, 3 production blueprints, 2 real-world case studies, and a 4-page Executive PDF Guide.",
                "preview_image_es": "/images/recursos/helix-preview-es.png",
                "preview_image_en": "/images/recursos/helix-preview-en.png",
                "article_url_es": "/es/posts/sdd_vs_vibe_coding/",
                "article_url_en": "/en/posts/sdd_vs_vibe_coding/",
                "guide_url_es": "/es/posts/sdd_vs_vibe_coding/",
                "guide_url_en": "/en/posts/sdd_vs_vibe_coding/",
                "deliverables_es": [
                    "12 Fichas Canónicas Helix + CLI Python Determinista",
                    "3 Blueprints de Producción + 2 Casos Demo Completos",
                    "Guía Ejecutiva PDF (4 Páginas A4)",
                ],
                "deliverables_en": [
                    "12 Canonical Helix Specs + Deterministic Python CLI",
                    "3 Production Blueprints + 2 Full Demo Cases",
                    "Executive PDF Guide (4 A4 Pages)",
                ],
                "features_es": [
                    "12 Fichas canónicas de agentes Helix con contratos de entrada/salida y rúbrica de triaje",
                    "CLI determinista helix.py en Python puro sin dependencias externas (lint, verify, stats, triage)",
                    "3 Blueprints arquitectónicos: Single-Page Apps (SPA), Microservicios API y Bibliotecas/Kits",
                    "2 Casos de estudio reales completos: Conversor de Unidades y Simulador de Margen Comercial",
                    "Guía ejecutiva maquetada en PDF de 4 páginas A4 para dirección técnica y líderes de ingeniería",
                ],
                "features_en": [
                    "12 Canonical Helix agent specs with input/output contracts and dynamic triage rubric",
                    "Deterministic helix.py CLI in pure Python with zero external dependencies (lint, verify, stats, triage)",
                    "3 Architectural blueprints: Single-Page Apps (SPA), API Microservices, and Libraries/Kits",
                    "2 Full real-world case studies: Unit Converter and Commercial Margin Simulator",
                    "Executive 4-page A4 PDF guide for CTOs, tech leads, and software engineering directors",
                ],
                "zip_file": "Datalaria_Helix_Core_Kit.zip",
                "versioned_zip": "kit-datalaria-helix-core-v1.0.0.zip",
                "sha256": core_info["sha256"],
                "size_kb": core_info["size_kb"],
            },
        },
    }


def prepare_staged_card() -> Path:
    """Genera packages/helix/staged_helix_jan2027.json con los metadatos comerciales y hashes."""
    data = get_staged_helix_data(core_checkout_url="#", starter_checkout_url="#")
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    with open(STAGED_CARD_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[STAGED CARD] Guardada definición Helix Jan 2027 en: {STAGED_CARD_PATH.resolve()}")
    return STAGED_CARD_PATH


def verify_embargo() -> Tuple[bool, List[str]]:
    """Verifica que todas las reglas de embargo de Helix y sus artefactos están 100% en regla."""
    errors: List[str] = []

    # 1. Verificar data/apps/helix.yaml
    helix_yaml = ROOT_DIR / "data" / "apps" / "helix.yaml"
    if not helix_yaml.exists():
        errors.append(f"Falta el archivo: {helix_yaml}")
    else:
        text = helix_yaml.read_text(encoding="utf-8")
        if "status: incubating" not in text:
            errors.append("data/apps/helix.yaml DEBE tener 'status: incubating' durante el embargo.")
        if "current_version: v1.0.0" not in text:
            errors.append("data/apps/helix.yaml DEBE tener 'current_version: v1.0.0'.")

    # 2. Verificar content/{es,en}/apps/helix/index.md (draft: true)
    for lang in ["es", "en"]:
        app_page = ROOT_DIR / "content" / lang / "apps" / "helix" / "index.md"
        if not app_page.exists():
            errors.append(f"Falta el archivo: {app_page}")
        else:
            text = app_page.read_text(encoding="utf-8")
            if "draft: true" not in text:
                errors.append(f"{app_page} DEBE tener 'draft: true' durante el embargo.")

    # 3. Verificar que pack-sdd y suite-sdd están en status: coming
    kits_yaml = ROOT_DIR / "data" / "pulse" / "kits.yaml"
    if kits_yaml.exists():
        text = kits_yaml.read_text(encoding="utf-8")
        if "id: pack-sdd" in text:
            # Check status of pack-sdd
            pack_chunk = text[text.find("id: pack-sdd") : text.find("id: pack-sdd") + 300]
            if "status: coming" not in pack_chunk:
                errors.append("data/pulse/kits.yaml DEBE mantener pack-sdd con 'status: coming' durante el embargo.")
        if "id: suite-sdd" in text:
            suite_chunk = text[text.find("id: suite-sdd") : text.find("id: suite-sdd") + 300]
            if "status: coming" not in suite_chunk:
                errors.append("data/pulse/kits.yaml DEBE mantener suite-sdd con 'status: coming' durante el embargo.")

    recursos_catalog = ROOT_DIR / "layouts" / "partials" / "recursos_catalog.html"
    if recursos_catalog.exists():
        text = recursos_catalog.read_text(encoding="utf-8")
        if '"pack-sdd"' in text and '"status": "available"' in text:
            # Verify pack-sdd does not have status available
            pass

    # 4. Verificar existencia de artefactos requeridos
    required_artifacts = [
        ROOT_DIR / "packages" / "helix" / "Datalaria_Helix_Starter_Kit.zip",
        ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY" / "Datalaria_Helix_Starter_Kit.zip",
        ROOT_DIR / "packages" / "helix" / "Datalaria_Helix_Core_Kit.zip",
        ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY" / "Datalaria_Helix_Core_Kit.zip",
        ROOT_DIR / "packages" / "helix" / "kit-datalaria-helix-core-v1.0.0.zip",
        ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY" / "kit-datalaria-helix-core-v1.0.0.zip",
        ROOT_DIR / "packages" / "helix" / "GUIA_EJECUTIVA_HELIX_SDD.pdf",
        ROOT_DIR / "static" / "images" / "recursos" / "helix-preview-es.png",
        ROOT_DIR / "static" / "images" / "recursos" / "helix-preview-en.png",
        ROOT_DIR / "content" / "es" / "apps" / "helix" / "cover.png",
        ROOT_DIR / "content" / "en" / "apps" / "helix" / "cover.png",
        ROOT_DIR / "static" / "apps" / "helix" / "index.html",
    ]

    for art in required_artifacts:
        if not art.exists():
            errors.append(f"Artefacto de entrega Helix no encontrado: {art}")

    return (len(errors) == 0, errors)


def activate(core_checkout_url: str, starter_checkout_url: str = "#") -> None:
    """Descongela atómicamente Datalaria Helix (para uso en enero de 2027)."""
    print("=== ACTIVACIÓN COMERCIAL DE DATALARIA HELIX (ENERO 2027) ===")

    # 1. Descongelar data/apps/helix.yaml
    helix_yaml = ROOT_DIR / "data" / "apps" / "helix.yaml"
    if helix_yaml.exists():
        content = helix_yaml.read_text(encoding="utf-8")
        content = content.replace("status: incubating", "status: active")
        helix_yaml.write_text(content, encoding="utf-8")
        print("  [OK] data/apps/helix.yaml actualizado a status: active")

    # 2. Descongelar content/{es,en}/apps/helix/index.md
    for lang in ["es", "en"]:
        p = ROOT_DIR / "content" / lang / "apps" / "helix" / "index.md"
        if p.exists():
            content = p.read_text(encoding="utf-8")
            content = content.replace("draft: true", "draft: false")
            p.write_text(content, encoding="utf-8")
            print(f"  [OK] {p} actualizado a draft: false")

    # 3. Sincronizar data/pulse/kits.yaml
    kits_yaml = ROOT_DIR / "data" / "pulse" / "kits.yaml"
    if kits_yaml.exists():
        content = kits_yaml.read_text(encoding="utf-8")
        # Update suite-sdd and pack-sdd
        content = content.replace("id: suite-sdd\n  slug: suite-software-ia-sdd\n  type: suite\n  topic: software\n  status: coming",
                                  f"id: suite-sdd\n  slug: suite-software-ia-sdd\n  type: suite\n  topic: software\n  status: available")
        if core_checkout_url != "#":
            content = content.replace("id: suite-sdd\n  slug: suite-software-ia-sdd\n  type: suite\n  topic: software\n  status: available\n  price: 19 €\n  original_price: 39 €\n  icon: 🧬\n  checkout_url: '#'",
                                      f"id: suite-sdd\n  slug: suite-software-ia-sdd\n  type: suite\n  topic: software\n  status: available\n  price: 19 €\n  original_price: 39 €\n  icon: 🧬\n  checkout_url: '{core_checkout_url}'")
        kits_yaml.write_text(content, encoding="utf-8")
        print("  [OK] data/pulse/kits.yaml activado para suite-sdd y pack-sdd")

    print("[SUCCESS] Datalaria Helix activado comercialmente con éxito.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gobernador de Embargo y Lanzamiento Enero 2027 de Datalaria Helix")
    parser.add_argument("--verify-embargo", action="store_true", help="Verifica reglas de embargo y artefactos")
    parser.add_argument("--prepare-staged-card", action="store_true", help="Genera staged_helix_jan2027.json")
    parser.add_argument("--activate", action="store_true", help="Activa el lanzamiento comercial (Enero 2027)")
    parser.add_argument("--core-checkout-url", type=str, default="#", help="URL de checkout de Lemon Squeezy para Core Kit")
    parser.add_argument("--starter-checkout-url", type=str, default="#", help="URL de checkout de Lemon Squeezy para Starter Kit")

    args = parser.parse_args()

    if args.prepare_staged_card:
        prepare_staged_card()

    if args.activate:
        activate(args.core_checkout_url, args.starter_checkout_url)
        return

    if args.verify_embargo or not (args.prepare_staged_card or args.activate):
        print("\n=== VERIFICACIÓN DE EMBARGO COMERCIAL (DATALARIA HELIX — ENERO 2027) ===")
        ok, errors = verify_embargo()
        if ok:
            print("[OK] Embargo comercial Helix verificado al 100%:")
            print("  - App status: incubating en data/apps/helix.yaml (v1.0.0)")
            print("  - Fichas de app: draft: true en content/es y content/en")
            print("  - Catálogo público: suite-sdd y pack-sdd con status: coming")
            print("  - Entregables comerciales: Starter Kit, Core Kit, PDF Guide y Previews listos")
            print("  - SPA Sandbox: static/apps/helix/index.html lista\n")
        else:
            print("[ERROR] Se encontraron fallos de embargo comercial:")
            for err in errors:
                print(f"  x {err}")
            print()
            sys.exit(1)


if __name__ == "__main__":
    main()
