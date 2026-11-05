"""
Test Suite: Caso de Estudio #2 Datalaria Helix (MarginGuard B2B — Hito 6.7)
Verifica la documentación del caso de estudio, calidad formal de la especificación (100/100),
invariantes matemáticas de pricing, packaging en el ZIP comercial y preset en el Web Sandbox.
"""
import importlib.util
from pathlib import Path
import zipfile
import pytest

from ops.helix.cli import score_spec_markdown


ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


def test_case_study_02_docs_and_audit_exist():
    """Verifica que el documento de auditoría del Caso de Estudio #2 existe y está documentado."""
    doc_path = ROOT_DIR / "specs" / "audit" / "case-study-02-no-dev-microapp.md"
    assert doc_path.exists(), f"Falta {doc_path}"
    content = doc_path.read_text(encoding="utf-8")
    assert len(content.splitlines()) >= 50
    assert "MarginGuard B2B" in content
    assert "INV-MARGIN-2" in content
    assert "11-qa-verifier" in content
    assert "QA_REJECT" in content
    assert "QA_PASS" in content


def test_margin_guard_spec_achieves_100_quality_score():
    """Verifica que spec.md de MarginGuard alcanza una puntuación de 100/100."""
    spec_path = (
        ROOT_DIR
        / "packages"
        / "helix"
        / "core_kit"
        / "05_Case_Studies_and_Docs"
        / "case_study_02_margin_guard_app"
        / "specs"
        / "apps"
        / "margin-guard"
        / "spec.md"
    )
    assert spec_path.exists(), f"Falta {spec_path}"
    content = spec_path.read_text(encoding="utf-8")
    score_res = score_spec_markdown(content)

    assert score_res["total_score"] == 100, f"Puntuación esperada 100, obtenida: {score_res}"
    assert score_res["passed"] is True
    assert score_res["pillars"]["problem"] == 20
    assert score_res["pillars"]["nongoals"] == 20
    assert score_res["pillars"]["contracts"] == 20
    assert score_res["pillars"]["invariants"] == 20
    assert score_res["pillars"]["gates"] == 20
    assert len(score_res["invariants_found"]) >= 4


def test_margin_guard_engine_math_invariants():
    """Verifica la ejecución determinista de engine.py y las invariantes INV-MARGIN-1 y INV-MARGIN-2."""
    engine_path = (
        ROOT_DIR
        / "packages"
        / "helix"
        / "core_kit"
        / "05_Case_Studies_and_Docs"
        / "case_study_02_margin_guard_app"
        / "engine.py"
    )
    assert engine_path.exists(), f"Falta {engine_path}"

    spec = importlib.util.spec_from_file_location("margin_engine", engine_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    calculate = getattr(module, "calculate_margin_scenario")

    # 1. Caso Viable (INV-MARGIN-1): P=100, C=70 (m=30%), d=10% -> +50% volumen
    res_viable = calculate(100.0, 70.0, 1000, 0.10)
    assert res_viable["value_destruction_zone"] is False
    assert pytest.approx(res_viable["required_volume_increase_pct"], 0.0001) == 0.50
    assert res_viable["required_units"] == 1500.0
    assert abs(res_viable["new_ebitda"] - res_viable["baseline_ebitda"]) < 5.0

    # 2. Caso Veto QA - Igualdad de margen (INV-MARGIN-2): d=30%, m=30%
    res_equal = calculate(100.0, 70.0, 1000, 0.30)
    assert res_equal["value_destruction_zone"] is True
    assert res_equal["required_volume_increase_pct"] is None
    assert res_equal["required_units"] is None

    # 3. Caso Veto QA - Descuento superior (INV-MARGIN-2): d=35%, m=30%
    res_excess = calculate(100.0, 70.0, 1000, 0.35)
    assert res_excess["value_destruction_zone"] is True
    assert res_excess["required_volume_increase_pct"] is None
    assert res_excess["required_units"] is None


def test_margin_guard_web_files_and_bilingual_ui():
    """Verifica la integridad de los archivos estáticos de la micro-app web."""
    app_dir = (
        ROOT_DIR
        / "packages"
        / "helix"
        / "core_kit"
        / "05_Case_Studies_and_Docs"
        / "case_study_02_margin_guard_app"
    )
    html_file = app_dir / "index.html"
    css_file = app_dir / "styles.css"
    js_file = app_dir / "app.js"
    roadmap_file = app_dir / "specs" / "ROADMAP.md"

    for f in (html_file, css_file, js_file, roadmap_file):
        assert f.exists(), f"Falta {f}"
        assert f.stat().st_size > 200, f"Archivo demasiado pequeño: {f}"

    html_content = html_file.read_text(encoding="utf-8")
    assert "MarginGuard B2B" in html_content
    assert "btn-lang" in html_content
    assert "destruction-alert" in html_content

    js_content = js_file.read_text(encoding="utf-8")
    assert "calculateScenario" in js_content
    assert "valueDestruction" in js_content


def test_margin_guard_packaged_in_commercial_zip():
    """Verifica que el ZIP comercial contiene la app y la documentación del caso de estudio."""
    zip_path = ROOT_DIR / "packages" / "helix" / "kit-datalaria-helix-core-v1.0.0.zip"
    assert zip_path.exists(), f"Falta {zip_path}"

    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        expected_files = [
            "05_Case_Studies_and_Docs/CASE_STUDY_02_NO_DEV_MICROAPP.md",
            "05_Case_Studies_and_Docs/case_study_02_margin_guard_app/specs/apps/margin-guard/spec.md",
            "05_Case_Studies_and_Docs/case_study_02_margin_guard_app/specs/apps/margin-guard/design.md",
            "05_Case_Studies_and_Docs/case_study_02_margin_guard_app/specs/ROADMAP.md",
            "05_Case_Studies_and_Docs/case_study_02_margin_guard_app/engine.py",
            "05_Case_Studies_and_Docs/case_study_02_margin_guard_app/index.html",
            "05_Case_Studies_and_Docs/case_study_02_margin_guard_app/styles.css",
            "05_Case_Studies_and_Docs/case_study_02_margin_guard_app/app.js",
        ]
        for exp in expected_files:
            normalized_exp = exp.replace("\\", "/")
            matching = [n for n in namelist if n.replace("\\", "/").endswith(normalized_exp)]
            assert len(matching) > 0, f"No encontrado en el ZIP comercial: {exp}"


def test_margin_guard_preset_in_helix_web_sandbox():
    """Verifica que el preset MarginGuard está integrado en el Web Sandbox de Helix."""
    engine_ts = ROOT_DIR / "apps" / "helix" / "web" / "src" / "engine.ts"
    i18n_ts = ROOT_DIR / "apps" / "helix" / "web" / "src" / "i18n.ts"
    app_tsx = ROOT_DIR / "apps" / "helix" / "web" / "src" / "App.tsx"

    assert engine_ts.exists()
    assert i18n_ts.exists()
    assert app_tsx.exists()

    engine_code = engine_ts.read_text(encoding="utf-8")
    assert "margin:" in engine_code
    assert "margin-guard" in engine_code
    assert "INV-MARGIN-1" in engine_code
    assert "INV-MARGIN-2" in engine_code

    i18n_code = i18n_ts.read_text(encoding="utf-8")
    assert "exampleMargin:" in i18n_code
    assert "MarginGuard B2B" in i18n_code

    app_code = app_tsx.read_text(encoding="utf-8")
    assert "loadExample('margin')" in app_code
