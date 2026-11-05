"""apps/conversor/tests/test_conversor_v2.py
Suite determinista de validación para Conversor de Unidades v2.0.0
Datalaria Helix — Assurance Gate (INV-CONV-1..6)
"""

import json
import math
import subprocess
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
APP_SRC = REPO_ROOT / "apps" / "conversor"
STATIC_CONV = REPO_ROOT / "static" / "apps" / "conversor"
DATA_YAML = REPO_ROOT / "data" / "apps" / "conversor.yaml"
SPEC_FILE = REPO_ROOT / "specs" / "apps" / "conversor" / "spec.md"
DESIGN_FILE = REPO_ROOT / "specs" / "apps" / "conversor" / "design.md"


def run_node_eval(js_code: str):
    """Ejecuta código JS en Node.js importando el motor de apps/conversor."""
    wrapper = f"""
    import * as engine from './engine.js';
    import * as catalog from './catalog.js';

    async function main() {{
        {js_code}
    }}
    main().catch(err => {{
        console.error(err);
        process.exit(1);
    }});
    """
    res = subprocess.run(
        ["node", "--input-type=module", "-e", wrapper],
        cwd=str(APP_SRC),
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if res.returncode != 0:
        raise RuntimeError(f"Node execution failed:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}")
    return res.stdout.strip()


# -------------------------------------------------------------------------
# 1. Invariante INV-CONV-1: Reversibilidad Numérica Estricta
# -------------------------------------------------------------------------

def test_inv_conv_1_linear_reversibility():
    """Verifica que para cualquier magnitud lineal, convert(convert(x, A, B), B, A) == x."""
    js_code = """
    let testsCount = 0;
    const cats = catalog.CATEGORIES;
    for (const [catKey, cat] of Object.entries(cats)) {
        if (!cat.magnitudes) continue;
        for (const [magKey, mag] of Object.entries(cat.magnitudes)) {
            if (mag.isNonLinear || mag.isSpecialRfWav || mag.isSpecialRfPower || !mag.units) continue;
            const units = Object.keys(mag.units);
            for (let i = 0; i < units.length; i++) {
                for (let j = 0; j < units.length; j++) {
                    const uA = units[i];
                    const uB = units[j];
                    const testVal = 42.5;
                    const forward = engine.convertLinear(testVal, uA, uB, mag.units);
                    const backward = engine.convertLinear(forward, uB, uA, mag.units);
                    const relError = Math.abs(backward - testVal) / testVal;
                    if (relError > 1e-9) {
                        throw new Error(`Fallo de reversibilidad en ${catKey}/${magKey}: ${uA} <-> ${uB}. RelError: ${relError}`);
                    }
                    testsCount++;
                }
            }
        }
    }
    console.log(JSON.stringify({ passed: true, count: testsCount }));
    """
    out = run_node_eval(js_code)
    data = json.loads(out)
    assert data["passed"] is True
    assert data["count"] > 100, f"Se esperaban más de 100 pares de prueba lineales, obtenidos: {data['count']}"


def test_inv_conv_1_temperature_reversibility():
    """Verifica conversiones y reversibilidad en la escala termodinámica de temperatura."""
    js_code = """
    const scales = ['c', 'f', 'k', 'r'];
    const testPoints = [-40, 0, 20, 100, 300];
    for (const p of testPoints) {
        for (const sA of scales) {
            for (const sB of scales) {
                const forward = engine.convertTemperature(p, sA, sB);
                const backward = engine.convertTemperature(forward, sB, sA);
                const diff = Math.abs(backward - p);
                if (diff > 1e-7) {
                    throw new Error(`Fallo temperatura ${p} ${sA} <-> ${sB}: recuperado ${backward}, diff: ${diff}`);
                }
            }
        }
    }
    // Puntos fijos canónicos
    const c0_to_f = engine.convertTemperature(0, 'c', 'f');
    if (Math.abs(c0_to_f - 32) > 1e-9) throw new Error('0 C debe ser 32 F');

    const c_minus_40 = engine.convertTemperature(-40, 'c', 'f');
    if (Math.abs(c_minus_40 - (-40)) > 1e-9) throw new Error('-40 C debe ser -40 F');

    const c100_to_k = engine.convertTemperature(100, 'c', 'k');
    if (Math.abs(c100_to_k - 373.15) > 1e-9) throw new Error('100 C debe ser 373.15 K');

    console.log(JSON.stringify({ passed: true }));
    """
    out = run_node_eval(js_code)
    assert json.loads(out)["passed"] is True


def test_inv_conv_1_rf_power_and_wavelength():
    """Verifica fórmulas no lineales de Radiofrecuencia (dBm ⇔ W / mW y λ = c / f)."""
    js_code = """
    // 1. dBm ⇔ W / mW
    // 30 dBm = 1 W = 1000 mW
    const w_from_30dbm = engine.convertRfPower(30, 'dbm', 'w');
    if (Math.abs(w_from_30dbm - 1.0) > 1e-9) throw new Error(`30 dBm debe ser 1 W, obtenido: ${w_from_30dbm}`);

    const mw_from_0dbm = engine.convertRfPower(0, 'dbm', 'mw');
    if (Math.abs(mw_from_0dbm - 1.0) > 1e-9) throw new Error(`0 dBm debe ser 1 mW, obtenido: ${mw_from_0dbm}`);

    const dbm_from_10w = engine.convertRfPower(10, 'w', 'dbm');
    if (Math.abs(dbm_from_10w - 40.0) > 1e-9) throw new Error(`10 W debe ser 40 dBm, obtenido: ${dbm_from_10w}`);

    // Reversibilidad dBm
    for (const testDbm of [-30, -10, 0, 10, 20, 30, 43]) {
        for (const unit of ['w', 'mw', 'kw']) {
            const linearVal = engine.convertRfPower(testDbm, 'dbm', unit);
            const recoveredDbm = engine.convertRfPower(linearVal, unit, 'dbm');
            if (Math.abs(recoveredDbm - testDbm) > 1e-7) {
                throw new Error(`Fallo reversibilidad RF power: ${testDbm} dBm <-> ${unit}`);
            }
        }
    }

    // 2. Frecuencia ⇔ Longitud de onda bidireccional
    // f = 100 MHz -> λ ≈ 2.99792458 m
    const lambda_m = engine.convertRfWavFreq(100, 'freq_to_wav', 'mhz', 'm');
    if (Math.abs(lambda_m - 2.99792458) > 1e-8) {
        throw new Error(`100 MHz debe ser ~2.99792458 m, obtenido: ${lambda_m}`);
    }

    // Bidireccional: λ = 2.99792458 m -> f = 100 MHz
    const f_mhz = engine.convertRfWavFreq(lambda_m, 'wav_to_freq', 'm', 'mhz');
    if (Math.abs(f_mhz - 100) > 1e-6) {
        throw new Error(`2.99792458 m debe ser 100 MHz, obtenido: ${f_mhz}`);
    }

    console.log(JSON.stringify({ passed: true }));
    """
    out = run_node_eval(js_code)
    assert json.loads(out)["passed"] is True


# -------------------------------------------------------------------------
# 2. Invariante INV-CONV-2: Completitud de Unidades sin Contract Drift
# -------------------------------------------------------------------------

def test_inv_conv_2_units_completeness():
    """Verifica la existencia de BTU, IEC vs SI en informática y todas las 6 disciplinas."""
    js_code = """
    const cats = catalog.CATEGORIES;
    const requiredCats = ['dimension', 'energia', 'tiempo', 'mecanica', 'informatica', 'radiofrecuencia', 'scratchpad'];
    for (const r of requiredCats) {
        if (!cats[r]) throw new Error(`Falta categoría requerida: ${r}`);
    }

    // Comprobar BTU
    const energyUnits = cats.energia.magnitudes.energy.units;
    if (!energyUnits.btu) throw new Error('Falta unidad BTU en energía');
    if (Math.abs(energyUnits.btu.factor - 1055.056) > 1e-3) throw new Error('Factor BTU IT debe ser 1055.056 J');

    // Comprobar Informática: IEC vs SI
    const infoMags = cats.informatica.magnitudes;
    if (!infoMags.storage_binary || !infoMags.storage_decimal) {
        throw new Error('Informática debe contener tanto storage_binary (IEC) como storage_decimal (SI)');
    }
    if (infoMags.storage_binary.units.gib.factor !== 1073741824) {
        throw new Error('1 GiB debe ser exactamente 1024^3 bytes');
    }
    if (infoMags.storage_decimal.units.gb.factor !== 1e9) {
        throw new Error('1 GB decimal debe ser exactamente 10^9 bytes');
    }

    // Comprobar Radiofrecuencia RF Power
    const rfMags = cats.radiofrecuencia.magnitudes;
    if (!rfMags.rf_power) throw new Error('Falta módulo rf_power en radiofrecuencia');
    if (!rfMags.wavelength_freq) throw new Error('Falta módulo wavelength_freq en radiofrecuencia');

    console.log(JSON.stringify({ passed: true }));
    """
    out = run_node_eval(js_code)
    assert json.loads(out)["passed"] is True


# -------------------------------------------------------------------------
# 3. Corrección de Bugs Numéricos y Parser Robusto
# -------------------------------------------------------------------------

def test_number_parser_and_formatter():
    """Verifica que el parser no corrompa '1,234' y formatee sin truncamiento prematuro."""
    js_code = """
    // 1. Fix del bug de 1,234 (en la v1 se convertía erróneamente a 1234)
    const parsed_1234 = engine.parseRobustNumber('1,234');
    if (Math.abs(parsed_1234 - 1.234) > 1e-9) {
        throw new Error(`'1,234' debe parsearse como 1.234 decimal, obtenido: ${parsed_1234}`);
    }

    // 2. US formato con miles y decimales
    const parsed_us = engine.parseRobustNumber('1,234.56');
    if (Math.abs(parsed_us - 1234.56) > 1e-9) {
        throw new Error(`'1,234.56' debe parsearse como 1234.56, obtenido: ${parsed_us}`);
    }

    // 3. EU formato con miles y decimales
    const parsed_eu = engine.parseRobustNumber('1.234,56');
    if (Math.abs(parsed_eu - 1234.56) > 1e-9) {
        throw new Error(`'1.234,56' debe parsearse como 1234.56, obtenido: ${parsed_eu}`);
    }

    // 4. Notación científica
    const parsed_sci = engine.parseRobustNumber('1.5e-4');
    if (Math.abs(parsed_sci - 0.00015) > 1e-12) {
        throw new Error(`'1.5e-4' debe parsearse como 0.00015, obtenido: ${parsed_sci}`);
    }

    // 5. Preservación del 4º decimal (evitar truncamiento de toLocaleString)
    // 1 in a m = 0.0254 m (en la v1 toLocaleString lo truncaba a 0,025)
    const formatted_inch = engine.formatEngineeredNumber(0.0254, 'auto', 'es');
    if (formatted_inch !== '0,0254') {
        throw new Error(`0.0254 en ES debe formatearse como '0,0254', obtenido: '${formatted_inch}'`);
    }

    console.log(JSON.stringify({ passed: true }));
    """
    out = run_node_eval(js_code)
    assert json.loads(out)["passed"] is True


def test_batch_scratchpad_processing():
    """Verifica el procesamiento por lotes del Scratchpad con y sin conversión de unidades."""
    js_code = """
    const input = '101325\\n100000\\n200000';
    // Conversión de formato US a EU
    const resFormat = engine.processBatchText(input, { targetFormat: 'eu' });
    if (resFormat.count !== 3 || resFormat.errors !== 0) {
        throw new Error(`Fallo formateo batch: ${JSON.stringify(resFormat)}`);
    }

    // Conversión de unidades en lote: Pa a bar (100000 Pa = 1 bar)
    const cats = catalog.CATEGORIES;
    const flat = {};
    for (const c of Object.values(cats)) {
        if (c.magnitudes) {
            for (const [mk, mo] of Object.entries(c.magnitudes)) flat[mk] = mo;
        }
    }
    const resUnits = engine.processBatchText(input, {
        targetFormat: 'eu',
        convertUnits: true,
        unitCategory: 'pressure',
        fromUnit: 'pa',
        toUnit: 'bar',
        precision: 'auto',
        categoriesCatalog: flat
    });

    if (resUnits.count !== 3) throw new Error('Debe procesar 3 filas');
    const lines = resUnits.output.split('\\n');
    if (lines[1] !== '1') throw new Error(`100000 Pa debe dar '1' bar, dio: '${lines[1]}'`);

    console.log(JSON.stringify({ passed: true }));
    """
    out = run_node_eval(js_code)
    assert json.loads(out)["passed"] is True


# -------------------------------------------------------------------------
# 4. Invariante INV-CONV-3 & INV-CONV-4: Firewall de static/ e Integridad HTML
# -------------------------------------------------------------------------

def test_inv_conv_3_static_firewall():
    """Certifica cero código backend o credenciales en static/apps/conversor/."""
    forbidden_exts = {".py", ".sql", ".env", ".pyc", ".ipynb", ".git"}
    for p in STATIC_CONV.rglob("*"):
        if p.is_file():
            assert p.suffix.lower() not in forbidden_exts, f"Violación del firewall static/: archivo prohibido {p}"


def test_inv_conv_4_shims_and_mecanica_en_fix():
    """Verifica la existencia y validez de los 14 shims y la resolución del bug de mecanica_en.html."""
    assert (STATIC_CONV / "index.html").exists(), "Falta static/apps/conversor/index.html"
    index_html = (STATIC_CONV / "index.html").read_text(encoding="utf-8")
    assert index_html.startswith("<!DOCTYPE html>"), "index.html debe ser un HTML5 válido"
    assert "cdn.tailwindcss.com" not in index_html, "INV-CONV-3: Prohibido cargar cdn.tailwindcss.com"

    shims_es = ["index.html", "dimension.html", "energia.html", "tiempo.html", "mecanica.html", "informatica.html", "radiofrecuencia.html"]
    for s in shims_es:
        path = STATIC_CONV / "es" / s
        assert path.exists(), f"Falta shim ES: {path}"
        content = path.read_text(encoding="utf-8")
        assert content.startswith("<!DOCTYPE html>"), f"Shim ES {s} corrupto"
        assert "<meta http-equiv=\"refresh\"" in content, f"Shim ES {s} debe tener meta refresh"
        assert "/apps/conversor/?lang=es" in content, f"Shim ES {s} debe redirigir a /apps/conversor/?lang=es"

    shims_en = ["index.html", "dimension_en.html", "energia_en.html", "tiempo_en.html", "mecanica_en.html", "informatica_en.html", "radiofrecuencia_en.html"]
    for s in shims_en:
        path = STATIC_CONV / "en" / s
        assert path.exists(), f"Falta shim EN: {path}"
        content = path.read_text(encoding="utf-8")
        assert content.startswith("<!DOCTYPE html>"), f"Shim EN {s} corrupto"
        assert not content.startswith("rset=\"UTF-8\">"), f"Shim EN {s} contiene la corrupción histórica 'rset='UTF-8'>'!"
        assert "<meta http-equiv=\"refresh\"" in content, f"Shim EN {s} debe tener meta refresh"
        assert "/apps/conversor/?lang=en" in content, f"Shim EN {s} debe redirigir a /apps/conversor/?lang=en"


# -------------------------------------------------------------------------
# 5. Invariante INV-CONV-6 & Metadatos SemVer (Constitución Art. 8)
# -------------------------------------------------------------------------

def test_inv_conv_6_metadata_and_spec_alignment():
    """Valida la coherencia de versión v2.0.0 y estado active entre spec.md y conversor.yaml."""
    assert DATA_YAML.exists(), f"Falta {DATA_YAML}"
    data = yaml.safe_load(DATA_YAML.read_text(encoding="utf-8"))

    assert data["slug"] == "conversor"
    assert data["current_version"] == "v2.0.0"
    assert data["status"] == "active"
    assert data["tier"] == "lab"

    # Verificar que v2.0.0 está en releases
    release_versions = [r["version"] for r in data.get("releases", [])]
    assert "v2.0.0" in release_versions, "v2.0.0 debe estar listado en releases de conversor.yaml"

    # Verificar spec.md
    assert SPEC_FILE.exists(), f"Falta {SPEC_FILE}"
    spec_content = SPEC_FILE.read_text(encoding="utf-8")
    assert "v2.0.0" in spec_content
    assert "INV-CONV-1" in spec_content
    assert "INV-CONV-6" in spec_content

    # Verificar design.md
    assert DESIGN_FILE.exists(), f"Falta {DESIGN_FILE}"
    design_content = DESIGN_FILE.read_text(encoding="utf-8")
    assert "DESIGN-APP-CONVERSOR" in design_content


def test_inv_conv_5_header_shell_links():
    """Valida que la barra superior integra los enlaces obligatorios: Ficha de la App, Guía y Kits."""
    app_js = (APP_SRC / "app.js").read_text(encoding="utf-8")
    assert "appSheetUrl" in app_js, "app.js debe definir appSheetUrl hacia la Ficha de la App"
    assert "/apps/conversor/" in app_js, "app.js debe enlazar a la ficha /apps/conversor/"
    assert "postUrl" in app_js, "app.js debe definir postUrl hacia la Guía Técnica"
    assert "resourcesUrl" in app_js, "app.js debe definir resourcesUrl hacia los Kits B2B"

    # Verificar index.html generado
    index_html = (STATIC_CONV / "index.html").read_text(encoding="utf-8")
    assert "appSheetUrl" in index_html
    assert "appSheet" in index_html

