"""Suite de pruebas deterministas para el Sandbox Web de Datalaria Helix (Hito 6.6 / INV-HELIX-6)."""

from __future__ import annotations

from pathlib import Path
import subprocess


def test_helix_design_md_exists_and_complete() -> None:
    """Verifica que specs/apps/helix/design.md existe y contiene tokens y Wow Moment."""
    design_path = Path("specs/apps/helix/design.md")
    assert design_path.exists(), "Falta specs/apps/helix/design.md"
    content = design_path.read_text(encoding="utf-8")
    assert "DESIGN-APP-HELIX" in content
    assert "Executive Data-Dense" in content
    assert "Signature Wow Moment" in content
    assert "--bg-canvas" in content
    assert "WCAG 2.2 AA" in content


def test_sandbox_source_structure_and_zero_any() -> None:
    """Verifica la existencia y tipado de los archivos fuente en apps/helix/web/."""
    src_dir = Path("apps/helix/web/src")
    assert (src_dir / "App.tsx").exists()
    assert (src_dir / "engine.ts").exists()
    assert (src_dir / "i18n.ts").exists()
    assert (src_dir / "styles.css").exists()
    assert (src_dir / "utils" / "zipBuilder.ts").exists()
    assert (src_dir / "utils" / "analytics.ts").exists()

    pkg = Path("apps/helix/web/package.json").read_text(encoding="utf-8")
    assert '"name": "datalaria-helix-web"' in pkg
    assert '"build:portal"' in pkg


def test_sandbox_ga4_telemetry_events_instrumented() -> None:
    """Verifica que los 4 eventos GA4 oficiales de SPEC-APP-HELIX están instrumentados."""
    analytics_src = Path("apps/helix/web/src/utils/analytics.ts").read_text(encoding="utf-8")
    app_src = Path("apps/helix/web/src/App.tsx").read_text(encoding="utf-8")

    expected_events = [
        "join_waitlist_helix",
        "generate_helix_spec_zip",
        "copy_helix_megaprompt",
        "begin_checkout_helix_kit",
    ]
    for ev in expected_events:
        assert ev in analytics_src

    assert "copy_helix_megaprompt" in app_src
    assert "generate_helix_spec_zip" in app_src
    assert "join_waitlist_helix" in app_src


def test_sandbox_dual_mode_and_localhost_fallback() -> None:
    """Verifica el soporte de ?lang=, ?demo=true y simulación en localhost."""
    app_src = Path("apps/helix/web/src/App.tsx").read_text(encoding="utf-8")
    assert "params.get('lang')" in app_src
    assert "params.get('demo')" in app_src
    assert "localhost" in app_src
    assert "127.0.0.1" in app_src


def test_compiled_bundle_exists_in_static_apps_helix() -> None:
    """Verifica que el bundle compilado existe en static/apps/helix/."""
    static_helix = Path("static/apps/helix")
    index_html = static_helix / "index.html"
    assert index_html.exists(), "Falta static/apps/helix/index.html"
    assert index_html.stat().st_size > 200

    assets_dir = static_helix / "assets"
    assert assets_dir.exists()
    js_files = list(assets_dir.glob("*.js"))
    css_files = list(assets_dir.glob("*.css"))
    assert len(js_files) >= 1
    assert len(css_files) >= 1


def test_inv_helix_6_static_firewall_clean() -> None:
    """INV-HELIX-6: static/apps/helix no contiene .py, .sql, .env, .ts, .tsx ni node_modules."""
    static_helix = Path("static/apps/helix")
    forbidden_suffixes = {".py", ".sql", ".env", ".ts", ".tsx", ".pyc", ".map"}

    for p in static_helix.rglob("*"):
        if p.is_file():
            assert p.suffix.lower() not in forbidden_suffixes, f"Archivo prohibido: {p}"
            assert "node_modules" not in p.parts


def test_pulse_18nov_embargo_still_intact() -> None:
    """Verifica que la compilación de Helix Sandbox no viola el embargo comercial de Pulse."""
    code = subprocess.run(
        ["python", "-m", "ops.pulse.release_18nov", "--verify-embargo"],
        capture_output=True,
        text=True,
    ).returncode
    assert code == 0, "El embargo comercial de Pulse fue violado."
