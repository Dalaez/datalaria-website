"""Tests de contrato deterministas del frontend Executive Risk Cockpit v2.0 (Hito OBS-2).

Cubre: INV-OBS-1 (Zero-CDN & Firewall static/), INV-OBS-2 (Paridad ES/EN 100 %),
INV-OBS-3 (Cero XSS/innerHTML & Modern Web), INV-OBS-4 (Motor DAG sin ciclos & LTB),
INV-OBS-7 (Privacidad CSV local) e INV-OBS-8 (GA4 beacon & Checkout ?embed=1).
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path
import re
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
WEB_DIR = REPO_ROOT / "apps" / "obs-management" / "web"
STATIC_DIR = REPO_ROOT / "static" / "apps" / "obs-management"

EXPECTED_CHECKOUT_URLS = {
    "https://datalaria.lemonsqueezy.com/checkout/buy/513e5cad-9f9f-4b53-a435-b511a846d79e?embed=1",
    "https://datalaria.lemonsqueezy.com/checkout/buy/6eea6aa0-fe9f-440b-8bb9-6f29b303e57a?embed=1",
    "https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1",
}


def _read_static_bundle() -> dict[str, str]:
    files = {}
    for name in ("index.html", "styles.css", "i18n.js", "engine.js", "app.js"):
        p = STATIC_DIR / name
        assert p.exists(), f"Falta artefacto sincronizado en static/: {p}"
        files[name] = p.read_text(encoding="utf-8")
    return files


def test_inv_obs_1_sync_parity_zero_cdn_budget_and_firewall() -> None:
    """INV-OBS-1: paridad fuente->static, 0 CDNs, < 45 KB gzip, 0 archivos prohibidos en static/."""
    res = subprocess.run(
        [sys.executable, str(WEB_DIR / "sync_static.py"), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0, f"sync_static.py --check falló: {res.stdout} {res.stderr}"

    forbidden = {".py", ".sql", ".env", ".pyc", ".txt", ".mdc"}
    for f in STATIC_DIR.rglob("*"):
        if f.is_file():
            assert f.suffix.lower() not in forbidden and f.name != ".env", f"Firewall violado: {f}"

    bundle = _read_static_bundle()
    total_gzip = sum(len(gzip.compress(content.encode("utf-8"), compresslevel=9)) for content in bundle.values())
    assert total_gzip < 45 * 1024, f"Bundle gzip excede 45 KB: {total_gzip / 1024:.2f} KB"

    for name, content in bundle.items():
        lower = content.lower()
        assert "cdn.tailwindcss.com" not in lower, f"Tailwind CDN detectado en {name}"
        assert "unpkg.com" not in lower and "jsdelivr.net" not in lower, f"CDN externo detectado en {name}"
        assert "fonts.googleapis.com" not in lower, f"CDN de fuentes detectado en {name}"


def test_inv_obs_2_bilingual_parity_es_en() -> None:
    """INV-OBS-2: 100 % paridad de claves entre I18N.es e I18N.en y rutas localizadas."""
    node_code = f"""
    import {{ I18N, PORTAL_ROUTES }} from {(WEB_DIR / "i18n.js").as_uri()!r};
    const esKeys = Object.keys(I18N.es).sort();
    const enKeys = Object.keys(I18N.en).sort();
    const missingInEn = esKeys.filter(k => !enKeys.includes(k));
    const missingInEs = enKeys.filter(k => !esKeys.includes(k));
    const enRoutesHasEs = Object.values(PORTAL_ROUTES.en).filter(v => v.startsWith('/es/'));
    console.log(JSON.stringify({{
      esCount: esKeys.length,
      enCount: enKeys.length,
      missingInEn,
      missingInEs,
      enRoutesHasEs,
    }}));
    """
    res = subprocess.run(
        ["node", "--input-type=module", "-e", node_code],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(res.stdout)
    assert data["esCount"] >= 80
    assert data["missingInEn"] == [], f"Claves ausentes en EN: {data['missingInEn']}"
    assert data["missingInEs"] == [], f"Claves ausentes en ES: {data['missingInEs']}"
    assert data["enRoutesHasEs"] == [], f"Rutas EN apuntando a /es/: {data['enRoutesHasEs']}"

    # Verify every data-i18n attribute in index.html exists in I18N.es & I18N.en
    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    used_keys = set(re.findall(r'data-i18n="([^"]+)"', html))
    assert used_keys, "No se encontraron atributos data-i18n en index.html"
    check_keys = f"""
    import {{ I18N }} from {(WEB_DIR / "i18n.js").as_uri()!r};
    const used = {json.dumps(sorted(used_keys))};
    const missing = used.filter(k => !(k in I18N.es) || !(k in I18N.en));
    console.log(JSON.stringify(missing));
    """
    res2 = subprocess.run(["node", "--input-type=module", "-e", check_keys], capture_output=True, text=True, check=True)
    assert json.loads(res2.stdout) == [], f"Claves HTML ausentes en I18N: {res2.stdout}"


def test_inv_obs_3_zero_innerhtml_and_modern_web_primitives() -> None:
    """INV-OBS-3: cero innerHTML, AbortSignal.timeout, native <dialog>, popover, design tokens."""
    bundle = _read_static_bundle()
    for js_name in ("app.js", "engine.js", "i18n.js"):
        assert "innerHTML" not in bundle[js_name], f"Uso prohibido de innerHTML en {js_name}"
        assert "outerHTML" not in bundle[js_name], f"Uso prohibido de outerHTML en {js_name}"

    assert "AbortSignal.timeout(800)" in bundle["app.js"]
    assert ".replaceChildren(" in bundle["app.js"]

    html = bundle["index.html"]
    assert '<dialog id="csvDialog"' in html
    assert 'role="dialog"' not in html
    assert 'aria-modal=' not in html
    assert 'popover="auto"' in html
    assert '<meta name="color-scheme"' in html

    css = bundle["styles.css"]
    for token in (
        "--bg-canvas:#0b0f17" if "--bg-canvas:#0b0f17" in css else "--bg-canvas: #0b0f17",
        "--bg-surface",
        "--accent-primary",
        "--accent-secondary",
        "tabular-nums",
        "scrollbar-color",
        "scrollbar-width",
        "@supports not (scrollbar-color: auto)",
        "prefers-reduced-motion",
        "@container (width < 600px)",
        "overscroll-behavior: contain",
    ):
        assert token in css, f"Falta token/regla UX obligatoria en styles.css: {token}"


def test_inv_obs_4_and_7_deterministic_engine_cycles_ltb_and_local_csv() -> None:
    """INV-OBS-4 & INV-OBS-7: motor BOM sin ciclos, criticidad IEC 62402, LTB vs FFF y CSV local."""
    node_code = f"""
    import {{
      PRESET_SCENARIOS,
      SAMPLE_BOM_CSV,
      computeCriticality,
      computeLtbVsFff,
      evaluateCatalogRisk,
      parseBomCsv,
      traverseBomUpward,
    }} from {(WEB_DIR / "engine.js").as_uri()!r};

    // 1. Cycle protection test
    const cyclicCatalog = {{
      products: [{{ sku: 'SKU-A', name: 'A', gross_margin: 10000 }}],
      bomEdges: [
        {{ parent: 'ASM-1', parentType: 'assembly', child: 'COMP-1', qty: 1 }},
        {{ parent: 'ASM-2', parentType: 'assembly', child: 'ASM-1', qty: 1 }},
        {{ parent: 'ASM-1', parentType: 'assembly', child: 'ASM-2', qty: 1 }},
        {{ parent: 'SKU-A', parentType: 'product', child: 'ASM-2', qty: 1 }},
      ],
      aml: [{{ internal_pn: 'COMP-1', mpn: 'MPN-CYC', manufacturer: 'TI', pref: 'Primary' }}],
      mpns: {{ 'MPN-CYC': {{ mpn: 'MPN-CYC', manufacturer: 'TI', lifecycle: 'EOL', unit_price_eur: 2, monthly_demand: 100 }} }},
    }};
    const cyc = traverseBomUpward(cyclicCatalog, 'MPN-CYC');

    // 2. Preset scenario evaluation
    const droneRisk = evaluateCatalogRisk(PRESET_SCENARIOS['drone-capacitor'].catalog);

    // 3. LTB vs FFF deterministic math
    const ltb = computeLtbVsFff(PRESET_SCENARIOS['drone-capacitor'].catalog.defaultLtb);

    // 4. Local CSV parser
    const csvOk = parseBomCsv(SAMPLE_BOM_CSV);
    const csvBad = parseBomCsv('Foo,Bar\\n1,2');

    // 5. IEC 62402 Criticality
    const crit = computeCriticality('Obsolete', 0, 15000, 15000);

    console.log(JSON.stringify({{ cyc, droneRisk, ltb, csvOkStats: csvOk.stats, csvBad, crit }}));
    """
    res = subprocess.run(["node", "--input-type=module", "-e", node_code], capture_output=True, text=True, check=True)
    out = json.loads(res.stdout)

    assert out["cyc"]["cycleDetected"] is True
    assert out["cyc"]["totalRiskEur"] == 10000
    assert out["droneRisk"]["total_risk_eur"] > 0
    assert out["droneRisk"]["active_alerts"] >= 2
    assert out["ltb"]["verdict"] in {"EXECUTE_LTB", "REDESIGN_FFF", "HYBRID_BRIDGE"}
    assert out["ltb"]["safety_stock_units"] > 0
    assert out["csvOkStats"]["skus"] == 3
    assert out["csvBad"]["ok"] is False and out["csvBad"]["errorType"] == "missing"
    assert out["crit"]["score"] == 100 and out["crit"]["status"] == "CRITICAL LTB REQUIRED"


def test_inv_obs_8_ga4_beacon_and_verified_embed_checkouts() -> None:
    """INV-OBS-8: telemetría GA4 con beacon y las 3 URLs verificadas ?embed=1."""
    bundle = _read_static_bundle()
    assert "transport_type: 'beacon'" in bundle["app.js"]
    for ev in ("obs_sandbox_view", "obs_scenario_select", "obs_pdn_inject", "obs_ltb_calculate", "obs_csv_import", "obs_cta_click"):
        assert ev in bundle["app.js"], f"Falta evento GA4 {ev} en app.js"

    combined = bundle["index.html"] + "\n" + bundle["i18n.js"]
    for url in EXPECTED_CHECKOUT_URLS:
        assert url in combined, f"Falta checkout URL verificada ?embed=1: {url}"


def test_inv_obs_6_pwa_offline_and_manifest() -> None:
    """INV-OBS-6: Manifiesto PWA válido, Service Worker Network-First, iconos y armonización SemVer v2.0.0."""
    manifest_path = STATIC_DIR / "manifest.json"
    assert manifest_path.exists(), "Falta manifest.json en static/apps/obs-management/"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["name"] == "Agentic Radar · Executive Risk Cockpit"
    assert manifest["short_name"] == "Radar"
    assert manifest["display"] == "standalone"
    assert manifest["start_url"] == "./?source=pwa"
    assert manifest["scope"] == "./"
    assert manifest["theme_color"] == "#0b0f17"
    assert len(manifest["icons"]) >= 4

    purposes = {icon.get("purpose", "any") for icon in manifest["icons"]}
    assert "any" in purposes and "maskable" in purposes, "Faltan iconos any y maskable en manifest.json"

    for icon in manifest["icons"]:
        icon_file = STATIC_DIR / icon["src"]
        assert icon_file.exists(), f"Falta archivo de icono referenciado en manifest: {icon['src']}"

    # Service Worker
    sw_path = STATIC_DIR / "sw.js"
    assert sw_path.exists(), "Falta sw.js en static/apps/obs-management/"
    sw_content = sw_path.read_text(encoding="utf-8")
    assert "obs-radar-v2.0.0" in sw_content, "sw.js debe definir la versión de caché obs-radar-v2.0.0"
    assert "skipWaiting" in sw_content and "clients.claim" in sw_content
    assert "lemonsqueezy.com" in sw_content and "google-analytics.com" in sw_content, "sw.js debe excluir APIs y analytics"

    # HTML links
    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    assert '<link rel="manifest" href="./manifest.json">' in html
    assert '<link rel="apple-touch-icon" href="./apple-touch-icon.png">' in html
    assert '<link rel="icon" type="image/svg+xml" href="./icon.svg">' in html

    # app.js PWA register
    app_js = (STATIC_DIR / "app.js").read_text(encoding="utf-8")
    assert "registerPwaServiceWorker" in app_js
    assert "hadController" in app_js

    # SemVer armonizado en data/apps/obs-management.yaml (fuente única Hito 9.4) y layouts/apps/list.html
    yaml_text = (REPO_ROOT / "data" / "apps" / "obs-management.yaml").read_text(encoding="utf-8")
    assert "current_version: v2.0.0" in yaml_text
    assert "version: v2.0.0" in yaml_text
    assert "demo_url: /apps/obs-management/?scenario=ltb-crisis" in yaml_text
    assert "v3.1.0" not in yaml_text, "v3.1.0 no debe estar en obs-management.yaml"
    assert "React" not in yaml_text, "React no debe estar en obs-management.yaml"
    assert "Vanilla JS" in yaml_text and "Zero-CDN CSS" in yaml_text

    list_html = (REPO_ROOT / "layouts" / "apps" / "list.html").read_text(encoding="utf-8")
    assert "site.Data.apps" in list_html, "layouts/apps/list.html debe leer dinámicamente desde site.Data.apps"
    assert "v3.1.0" not in list_html, "No debe haber versiones hardcoded obsoletas en list.html"

