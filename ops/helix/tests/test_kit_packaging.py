"""
ops/helix/tests/test_kit_packaging.py
-------------------------------------
Pruebas deterministas de validación del empaquetado comercial de Datalaria Helix (Hito 6.8).
Verifica:
  1. Guía ejecutiva PDF de 4 páginas A4 generada con PyMuPDF.
  2. Starter Kit ZIP (9€), estructura de 3 carpetas, 2 agentes esenciales y sincronización Lemon Squeezy.
  3. Core Kit ZIP (19€/39€), 5 carpetas, 12 agentes, CLI, blueprints, casos de estudio y sincronización.
  4. Dimensiones exactas de previews (1600x980) y portadas (1200x750) con Pillow.
  5. Metadatos de data/apps/helix.yaml (incubating, v1.0.0, 6 releases) y fichas staged (draft: true).
  6. Coexistencia limpia de los embargos comerciales: Helix (Enero 2027) y Pulse (18 Nov 2026).
"""

import zipfile
from pathlib import Path
import yaml
from PIL import Image
import pymupdf

from ops.helix.release_jan2027 import verify_embargo as verify_helix_embargo
from ops.pulse.release_18nov import verify_embargo as verify_pulse_embargo

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PACKAGES_HELIX = ROOT_DIR / "packages" / "helix"
PACKAGES_DIST = ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY"


def test_helix_pdf_guide_structure_and_pages():
    pdf_path = PACKAGES_HELIX / "GUIA_EJECUTIVA_HELIX_SDD.pdf"
    assert pdf_path.exists(), f"Falta el PDF: {pdf_path}"
    assert pdf_path.stat().st_size > 5000, "El PDF es sospechosamente pequeño"

    doc = pymupdf.open(str(pdf_path))
    try:
        assert len(doc) == 4, f"Se esperaban exactamente 4 páginas, se encontraron {len(doc)}"

        # Página 1: Portada y Manifiesto
        p1_text = doc[0].get_text().lower()
        assert "datalaria helix" in p1_text
        assert "manual maestro" in p1_text or "guía ejecutiva" in p1_text or "guia ejecutiva" in p1_text
        assert "spec-driven development" in p1_text

        # Página 2: Escuadrón y Triaje
        p2_text = doc[1].get_text().lower()
        assert "escuadron" in p2_text or "escuadrón" in p2_text or "12 agentes" in p2_text
        assert "triaje" in p2_text

        # Página 3: Bucle SDD y SpecQualityScore
        p3_text = doc[2].get_text().lower()
        assert "bucle sdd" in p3_text
        assert "specqualityscore" in p3_text or "invariantes" in p3_text

        # Página 4: Blueprints y Casos de Estudio
        p4_text = doc[3].get_text().lower()
        assert "blueprints" in p4_text
        assert "casos de estudio" in p4_text or "marginguard" in p4_text
    finally:
        doc.close()


def test_starter_kit_zip_structure_and_sync():
    starter_local = PACKAGES_HELIX / "Datalaria_Helix_Starter_Kit.zip"
    starter_dist = PACKAGES_DIST / "Datalaria_Helix_Starter_Kit.zip"

    assert starter_local.exists(), "Falta Datalaria_Helix_Starter_Kit.zip en packages/helix/"
    assert starter_dist.exists(), "Falta Datalaria_Helix_Starter_Kit.zip en packages/00_DISTRIBUCION_LEMONSQUEEZY/"
    assert starter_local.stat().st_size == starter_dist.stat().st_size, "Desincronización de tamaños en Starter Kit"

    with zipfile.ZipFile(starter_local, "r") as zf:
        # Integridad del ZIP
        bad_crc = zf.testzip()
        assert bad_crc is None, f"Archivo ZIP corrupto: {bad_crc}"

        names = zf.namelist()
        # Verificar presencia de las 3 carpetas numeradas
        assert any(n.startswith("01_Executive_Playbook/") for n in names), "Falta 01_Executive_Playbook en Starter Kit"
        assert any(n.startswith("02_Starter_Templates/") for n in names), "Falta 02_Starter_Templates en Starter Kit"
        assert any(n.startswith("03_Essential_2_Agents/") for n in names), "Falta 03_Essential_2_Agents en Starter Kit"

        # Verificar que contiene la Guía PDF
        assert "01_Executive_Playbook/GUIA_EJECUTIVA_HELIX_SDD.pdf" in names

        # Verificar que solo contiene los 2 agentes esenciales
        canonical_agents = [n for n in names if "03_Essential_2_Agents/specs/squad/" in n and n.endswith(".md")]
        agent_basenames = [Path(n).name for n in canonical_agents]
        assert "01-orchestrator.md" in agent_basenames
        assert "02-product-analyst.md" in agent_basenames
        assert "03-architect.md" not in agent_basenames
        # Contamos solo los agentes numerados (excluyendo README.md y triage-rubric.md)
        numbered_agents = [a for a in agent_basenames if a[:2].isdigit()]
        assert len(numbered_agents) == 2, f"El Starter Kit debe contener exactamente 2 agentes numerados, contiene {len(numbered_agents)}"

        # Verificar README raíz
        assert "README.md" in names
        assert "LICENSE.txt" in names


def test_core_kit_zip_structure_and_sync():
    core_local = PACKAGES_HELIX / "Datalaria_Helix_Core_Kit.zip"
    core_dist = PACKAGES_DIST / "Datalaria_Helix_Core_Kit.zip"
    core_versioned = PACKAGES_HELIX / "kit-datalaria-helix-core-v1.0.0.zip"
    core_versioned_dist = PACKAGES_DIST / "kit-datalaria-helix-core-v1.0.0.zip"

    for p in [core_local, core_dist, core_versioned, core_versioned_dist]:
        assert p.exists(), f"Falta archivo Core Kit: {p}"

    with zipfile.ZipFile(core_local, "r") as zf:
        bad_crc = zf.testzip()
        assert bad_crc is None, f"Archivo Core ZIP corrupto: {bad_crc}"

        names = zf.namelist()
        # Verificar 5 carpetas
        for prefix in [
            "01_Constitution_and_Memory/",
            "02_Templates/",
            "03_Squad_12_Agents_and_Adapters/",
            "04_Project_Blueprints/",
            "05_Case_Studies_and_Docs/",
        ]:
            assert any(n.startswith(prefix) for n in names), f"Falta carpeta {prefix} en Core Kit"

        # Verificar Guía PDF inyectada
        assert "05_Case_Studies_and_Docs/GUIA_EJECUTIVA_HELIX_SDD.pdf" in names

        # Verificar CLI helix.py en la raíz
        assert "helix.py" in names

        # Verificar 12 agentes canónicos
        canonical_agents = [
            n for n in names
            if "03_Squad_12_Agents_and_Adapters/specs/squad/" in n
            and n.endswith(".md")
            and Path(n).name[:2].isdigit()
        ]
        assert len(canonical_agents) == 12, f"Se esperaban 12 agentes canónicos, se encontraron {len(canonical_agents)}"

        # Verificar 3 blueprints
        assert any("04_Project_Blueprints/blueprint-01-static-calculator" in n for n in names)
        assert any("04_Project_Blueprints/blueprint-02-react-supabase-rls" in n for n in names)
        assert any("04_Project_Blueprints/blueprint-03-python-quant-engine" in n for n in names)

        # Verificar 2 casos de estudio
        assert "05_Case_Studies_and_Docs/CASE_STUDY_01_PULSE_CRISOL.md" in names
        assert "05_Case_Studies_and_Docs/CASE_STUDY_02_NO_DEV_MICROAPP.md" in names
        assert any("case_study_02_margin_guard_app" in n for n in names)


def test_helix_visual_previews_and_covers_dimensions():
    # Previews de catálogo
    preview_es = ROOT_DIR / "static" / "images" / "recursos" / "helix-preview-es.png"
    preview_en = ROOT_DIR / "static" / "images" / "recursos" / "helix-preview-en.png"
    assert preview_es.exists()
    assert preview_en.exists()

    with Image.open(preview_es) as img_es:
        assert img_es.size == (1600, 980), f"Dimensiones incorrectas en {preview_es}: {img_es.size}"

    with Image.open(preview_en) as img_en:
        assert img_en.size == (1600, 980), f"Dimensiones incorrectas en {preview_en}: {img_en.size}"

    # Portadas de fichas de app
    cover_es = ROOT_DIR / "content" / "es" / "apps" / "helix" / "cover.png"
    cover_en = ROOT_DIR / "content" / "en" / "apps" / "helix" / "cover.png"
    assert cover_es.exists()
    assert cover_en.exists()

    with Image.open(cover_es) as img_cover_es:
        assert img_cover_es.size == (1200, 750), f"Dimensiones incorrectas en {cover_es}: {img_cover_es.size}"

    with Image.open(cover_en) as img_cover_en:
        assert img_cover_en.size == (1200, 750), f"Dimensiones incorrectas en {cover_en}: {img_cover_en.size}"


def test_helix_app_yaml_and_staged_fichas():
    yaml_path = ROOT_DIR / "data" / "apps" / "helix.yaml"
    assert yaml_path.exists()

    with open(yaml_path, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)

    assert meta["slug"] == "helix"
    assert meta["status"] == "incubating"
    assert meta["current_version"] == "v1.0.0"
    assert "releases" in meta and len(meta["releases"]) == 6
    assert meta["releases"][0]["version"] == "v1.0.0"

    # Fichas staged
    for lang in ["es", "en"]:
        md_path = ROOT_DIR / "content" / lang / "apps" / "helix" / "index.md"
        assert md_path.exists()
        text = md_path.read_text(encoding="utf-8")
        assert "draft: true" in text
        assert 'app: "helix"' in text


def test_jan2027_embargo_and_pulse_18nov_embargo_coexistence():
    # Validar Helix Embargo
    ok_helix, errors_helix = verify_helix_embargo()
    assert ok_helix, f"Fallos en embargo comercial de Helix: {errors_helix}"

    # Validar Pulse Embargo
    ok_pulse, errors_pulse = verify_pulse_embargo()
    assert ok_pulse, f"Fallos en embargo comercial de Pulse: {errors_pulse}"
