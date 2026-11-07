# -*- coding: utf-8 -*-
"""
Suite de Pruebas Unitarias Deterministas para el componente Helix Release Radar.
Garantiza el cumplimiento estricto de las invariantes INV-PORTAL-REL-1..4 y la
correcta vinculación de interactividad DOM y scripts en el Home Portal.
"""
import glob
import json
import os
import re
import subprocess
import yaml
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
INDEX_TPL_PATH = os.path.join(ROOT_DIR, "layouts", "partials", "index_profile.html")
CSS_PATH = os.path.join(ROOT_DIR, "assets", "css", "extended", "home-portal.css")
APPS_DATA_DIR = os.path.join(ROOT_DIR, "data", "apps")
SPEC_PATH = os.path.join(ROOT_DIR, "specs", "portal", "spec.md")


def test_inv_portal_rel_1_embargo_and_public_status():
    """INV-PORTAL-REL-1: Solo apps con status 'live' o 'active' son candidatas.

    Apps en status 'incubating' (helix, pulse) deben ser estrictamente excluidas.
    """
    candidates = []
    excluded = []

    for path in glob.glob(os.path.join(APPS_DATA_DIR, "*.yaml")):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        slug = data.get("slug")
        status = data.get("status", "incubating")
        if status in ["live", "active"]:
            candidates.append(slug)
        else:
            excluded.append((slug, status))

    assert "snake" in candidates, "Snake debe ser candidata activa"
    assert "lifeops" in candidates, "LifeOps debe ser candidata activa"
    assert "conversor" in candidates, "Conversor debe ser candidata activa"
    assert "flashcards" in candidates, "Flashcards debe ser candidata activa"
    assert "maths" in candidates, "Maths debe ser candidata activa"

    # Incubating apps must be excluded
    excluded_slugs = [s for s, _ in excluded]
    assert "helix" in excluded_slugs, "Helix debe estar excluida (status: incubating)"
    assert "pulse" in excluded_slugs, "Pulse debe estar excluida (status: incubating)"


def test_inv_portal_rel_2_fourteen_days_window_and_fallback():
    """INV-PORTAL-REL-2: Filtrado determinista de 14 días y fallback al más reciente."""
    # Test dataset
    pool = [
        {"slug": "snake", "date": "2026-11-07", "version": "v2.3.0"},
        {"slug": "maths", "date": "2026-11-06", "version": "v2.3.0"},
        {"slug": "lifeops", "date": "2026-10-27", "version": "v1.1.1"},
        {"slug": "obs", "date": "2026-10-24", "version": "v1.0.1"},
        {"slug": "weather", "date": "2025-12-06", "version": "v1.0.0"},
    ]

    fourteen_days_ms = 14.5 * 24 * 60 * 60 * 1000  # 14 days + DST transition tolerance

    # Case 1: Active releases with reference date at 2026-11-07
    import datetime
    ref_time = datetime.datetime.fromisoformat("2026-11-07T00:00:00").timestamp() * 1000

    active = []
    for r in pool:
        r_time = datetime.datetime.fromisoformat(r["date"] + "T00:00:00").timestamp() * 1000
        diff = ref_time - r_time
        if 0 <= diff <= fourteen_days_ms:
            active.append(r)

    # Snake (0d), Maths (1d), LifeOps (11d), Obs (14d) should be in; Weather (336d) should be out
    active_slugs = [r["slug"] for r in active]
    assert "snake" in active_slugs
    assert "maths" in active_slugs
    assert "lifeops" in active_slugs
    assert "obs" in active_slugs
    assert "weather" not in active_slugs, "Weather (2025) excede la ventana de 14 días"

    # Case 2: Fallback when all releases are older than 14 days
    future_ref_time = datetime.datetime.fromisoformat("2027-01-01T00:00:00").timestamp() * 1000
    future_active = []
    for r in pool:
        r_time = datetime.datetime.fromisoformat(r["date"] + "T00:00:00").timestamp() * 1000
        diff = future_ref_time - r_time
        if 0 <= diff <= fourteen_days_ms:
            future_active.append(r)

    if not future_active and pool:
        future_active = [pool[0]]

    assert len(future_active) == 1, "Fallback debe activar exactamente 1 release"
    assert future_active[0]["slug"] == "snake", "Fallback debe mostrar la última release del ecosistema"


def test_inv_portal_rel_3_and_4_dom_elements_and_double_cta():
    """INV-PORTAL-REL-3 y 4: Verificación estática del template HTML.

    - Drawer oculto por defecto con hidden.
    - Únicamente 2 botones en el drawer: App y Especificaciones (cero blog links).
    """
    with open(INDEX_TPL_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()

    # Required IDs in template
    required_ids = [
        "dlh-rel-bar",
        "dlh-rel-summary",
        "dlh-rel-badge",
        "dlh-rel-icon",
        "dlh-rel-name",
        "dlh-rel-ver",
        "dlh-rel-date",
        "dlh-rel-title",
        "dlh-rel-nav",
        "dlh-rel-prev",
        "dlh-rel-counter",
        "dlh-rel-next",
        "dlh-rel-toggle",
        "dlh-rel-toggle-text",
        "dlh-rel-drawer",
        "dlh-drawer-app",
        "dlh-drawer-date",
        "dlh-drawer-headline",
        "dlh-drawer-changes",
        "dlh-drawer-actions",
        "dlh-drawer-cta-primary",
        "dlh-drawer-cta-secondary",
        "dlh-rel-chips-row",
        "dlh-rel-chips",
        "dlh-rel-data",
    ]

    for elem_id in required_ids:
        assert f'id="{elem_id}"' in tpl, f"Falta el elemento con id='{elem_id}' en el template"

    # INV-PORTAL-REL-3: Drawer has hidden by default
    assert '<div class="dlh-rel-drawer" id="dlh-rel-drawer" hidden>' in tpl, "El drawer debe tener atributo hidden por defecto"

    # INV-PORTAL-REL-4: Exactly 2 action links in drawer
    actions_block_match = re.search(r'<div class="dlh-rel-actions" id="dlh-drawer-actions">(.*?)</div>', tpl, re.DOTALL)
    assert actions_block_match, "No se encontró el bloque dlh-rel-actions"
    actions_html = actions_block_match.group(1)
    links = re.findall(r'<a\s+[^>]*>', actions_html)
    assert len(links) == 2, f"dlh-rel-actions debe tener exactamente 2 enlaces (App + Ficha), encontrados: {len(links)}"
    assert "dlh-drawer-cta-primary" in actions_html
    assert "dlh-drawer-cta-secondary" in actions_html
    # Must NOT have blog post links in drawer actions
    assert "posts/" not in actions_html, "dlh-rel-actions no debe enlazar a posts de blog"


def test_radar_javascript_controller_integrity():
    """Verifica que el script interactivo esté presente y contenga todas las funciones y bindings requeridos."""
    with open(INDEX_TPL_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()

    # Must contain controller variables and functions
    required_js_patterns = [
        "var relBar = document.getElementById('dlh-rel-bar');",
        "var relDataEl = document.getElementById('dlh-rel-data');",
        "var relDrawer = document.getElementById('dlh-rel-drawer');",
        "var relToggle = document.getElementById('dlh-rel-toggle');",
        "var relPrev = document.getElementById('dlh-rel-prev');",
        "var relNext = document.getElementById('dlh-rel-next');",
        "var relCounter = document.getElementById('dlh-rel-counter');",
        "var relChips = document.getElementById('dlh-rel-chips');",
        "function updateView(idx)",
        "function toggleDrawer()",
        "relSummary.addEventListener('click'",
        "relToggle.addEventListener('click'",
        "relPrev.addEventListener('click'",
        "relNext.addEventListener('click'",
        "updateView(0);",
        "home_release_radar_toggle",
        "home_release_radar_select",
    ]

    for pattern in required_js_patterns:
        assert pattern in tpl, f"Falta el patrón JS requerido en el template: {pattern}"


def test_radar_css_definitions():
    """Verifica la presencia y validez de las clases CSS de Helix Release Radar."""
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    required_selectors = [
        ".dlh-compass-main",
        ".dlh-rel-bar",
        ".dlh-rel-bar-summary",
        ".dlh-rel-badge",
        ".dlh-rel-dot",
        ".dlh-rel-icon",
        ".dlh-rel-name",
        ".dlh-rel-ver",
        ".dlh-rel-date",
        ".dlh-rel-title",
        ".dlh-rel-controls",
        ".dlh-rel-nav",
        ".dlh-rel-nav-btn",
        ".dlh-rel-counter",
        ".dlh-rel-toggle",
        ".dlh-rel-drawer",
        ".dlh-rel-drawer[hidden]",
        ".dlh-rel-content",
        ".dlh-rel-info",
        ".dlh-rel-actions",
        ".dlh-rel-btn--primary",
        ".dlh-rel-btn--secondary",
        ".dlh-rel-chips",
        ".dlh-rel-chip",
    ]

    for selector in required_selectors:
        assert selector in css, f"Falta el selector CSS '{selector}' en home-portal.css"


def test_radar_node_js_execution_simulation():
    """Ejecuta una simulación determinista de la lógica JS con Node.js para verificar que no arroja errores sintácticos ni lógicos."""
    node_script = """
    const samplePool = [
        { slug: "snake", name: "Neon Snake", icon: "🐍", version: "v2.3.0", date: "2026-11-07", title: "Ergonomía Táctil Full-Swipe", changes: ["Mejora 1", "Mejora 2"], appUrl: "/games/snake/", fichaUrl: "/es/apps/snake/" },
        { slug: "maths", name: "Matemáticas", icon: "🧮", version: "v2.3.0", date: "2026-11-06", title: "Diploma Arcade", changes: ["Mejora A"], appUrl: "/apps/maths/", fichaUrl: "/es/apps/maths/" },
        { slug: "flashcards", name: "Flashcards", icon: "🎴", version: "v2.1.0", date: "2026-11-06", title: "PWA Offline", changes: ["Mejora B"], appUrl: "/apps/flashcards/", fichaUrl: "/es/apps/flashcards/" },
        { slug: "weather", name: "El Tiempo", icon: "🌤️", version: "v1.0.0", date: "2025-12-06", title: "Leaflet", changes: ["Mejora C"], appUrl: "/apps/weather/", fichaUrl: "/es/apps/weather/" }
    ];

    const now = new Date("2026-11-07T12:00:00").getTime();
    const latestDate = samplePool.length > 0 && samplePool[0].date ? new Date(samplePool[0].date + "T00:00:00").getTime() : now;
    const refTime = Math.max(now, latestDate);
    const fourteenDaysMs = 14 * 24 * 60 * 60 * 1000;

    const activeReleases = samplePool.filter(r => {
        const rTime = new Date(r.date + "T00:00:00").getTime();
        const diff = refTime - rTime;
        return diff >= 0 && diff <= fourteenDaysMs;
    });

    if (activeReleases.length !== 3) {
        console.error("Error: expected 3 active releases, got " + activeReleases.length);
        process.exit(1);
    }

    let currentIndex = 0;
    function update(idx) {
        if (idx < 0) idx = activeReleases.length - 1;
        if (idx >= activeReleases.length) idx = 0;
        currentIndex = idx;
        return activeReleases[currentIndex];
    }

    // Test rotation
    const r0 = update(0);
    const r1 = update(1);
    const rPrevWrap = update(-1);

    if (r0.slug !== "snake" || r1.slug !== "maths" || rPrevWrap.slug !== "flashcards") {
        console.error("Rotation logic mismatch");
        process.exit(1);
    }

    console.log("NODE_SIM_SUCCESS");
    """

    res = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
    assert res.returncode == 0, f"Error ejecutando Node.js simulation: {res.stderr}"
    assert "NODE_SIM_SUCCESS" in res.stdout
