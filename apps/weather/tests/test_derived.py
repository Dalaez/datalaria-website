# -*- coding: utf-8 -*-
"""test_derived.py - Suite determinista para el Data Truth Pipeline (W3.1).

Verifica INV-WEATHER-7 a INV-WEATHER-10, build_derived.py, contratos de JSON derivados,
normalización de slugs, idempotencia de logs de pronóstico, higiene de /static/ y configuración upstream.
CERO peticiones de red (todo con tmp_path y datos sintéticos).
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import pytest
import pandas as pd

from apps.weather.build_derived import (
    slugify,
    aggregate_daily,
    build_climatology,
    append_forecast_log,
    process_derived_pipeline,
    parse_ciudades_txt,
)


BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# 1. Tests de Normalización y Slugs (INV-WEATHER-9)
# ---------------------------------------------------------------------------

def test_slugify():
    """Valida que slugify produce identificadores URL seguros sin acentos ni espacios."""
    assert slugify("Madrid") == "madrid"
    assert slugify("Sao Paulo") == "sao-paulo"
    assert slugify("A Coruña") == "a-coruna"
    assert slugify("Gijón") == "gijon"
    assert slugify("Santa Cruz de Tenerife") == "santa-cruz-de-tenerife"
    assert slugify("Ulán Bator / Ulaanbaatar") == "ulan-bator-ulaanbaatar"
    assert slugify("  Tokyo  ") == "tokyo"


def test_city_name_normalization_inv9():
    """Valida que read_weather.py use la ciudad canónica y no el nombre mutable de la API."""
    read_weather_path = BASE_DIR / "read_weather.py"
    assert read_weather_path.exists()
    content = read_weather_path.read_text(encoding="utf-8")

    assert "ciudad_canonica = nombre_limpio" in content or "ciudad_canonica" in content
    assert "INV-WEATHER-9" in content


# ---------------------------------------------------------------------------
# 2. Tests de Agregación Diaria y Amplitud Térmica Real
# ---------------------------------------------------------------------------

def test_aggregate_daily_amplitude_from_samples():
    """Valida que lecturas con temp_min == temp_max en OWM generen amp > 0 agrupadas por día."""
    synthetic_data = [
        {"fecha_hora": "2026-11-08T06:00:00Z", "temp": 12.0, "temp_min": 12.0, "temp_max": 12.0, "feels_like": 11.5, "humidity": 80, "wind_kmh": 5.0, "clouds": 20, "rain_1h": 0.0},
        {"fecha_hora": "2026-11-08T14:00:00Z", "temp": 22.0, "temp_min": 22.0, "temp_max": 22.0, "feels_like": 21.0, "humidity": 45, "wind_kmh": 12.0, "clouds": 10, "rain_1h": 0.0},
        {"fecha_hora": "2026-11-08T22:00:00Z", "temp": 15.0, "temp_min": 15.0, "temp_max": 15.0, "feels_like": 14.0, "humidity": 70, "wind_kmh": 6.0, "clouds": 0, "rain_1h": 0.0},
    ]
    df = pd.DataFrame(synthetic_data)
    rows = aggregate_daily(df)

    assert len(rows) == 1
    row = rows[0]
    # Columnas: [date, tmin, tmax, tmean, amp, feels, hum, wind, rain, clouds, n]
    date_val, tmin, tmax, tmean, amp, feels, hum, wind, rain, clouds, n = row

    assert date_val == "2026-11-08"
    assert tmin == 12.0
    assert tmax == 22.0
    assert tmean == round((12.0 + 22.0 + 15.0) / 3, 1)
    assert n == 3
    # Crucial: amp debe ser 10.0 (22.0 - 12.0), no 0.0
    assert amp == 10.0


def test_amplitude_null_when_single_sample():
    """Valida que si un día tiene una sola lectura (n < 2), la amplitud sea null."""
    synthetic_data = [
        {"fecha_hora": "2026-11-08T06:00:00Z", "temp": 15.0, "temp_min": 15.0, "temp_max": 15.0, "feels_like": 15.0, "humidity": 60, "wind_kmh": 8.0, "clouds": 0, "rain_1h": 0.0}
    ]
    df = pd.DataFrame(synthetic_data)
    rows = aggregate_daily(df)

    assert len(rows) == 1
    assert rows[0][4] is None  # amp is None
    assert rows[0][10] == 1    # n == 1


# ---------------------------------------------------------------------------
# 3. Tests de Climatología y Coeficientes Fourier
# ---------------------------------------------------------------------------

def test_climatology_month_null_below_10_days():
    """Valida que los meses con menos de 10 días de datos se guarden como null."""
    daily_rows = [
        [f"2026-05-{d:02d}", 10.0, 20.0, 15.0, 10.0, 14.0, 50.0, 10.0, 0.0, 20.0, 3]
        for d in range(1, 6)  # Solo 5 días en mayo
    ]
    climatology = build_climatology({"test-city": daily_rows})
    months = climatology["cities"]["test-city"]["months"]

    # Mayo (mes 5) debe ser null porque 5 < 10
    assert months["5"] is None
    # Mes 1 (sin días) debe ser null
    assert months["1"] is None


def test_fourier_coeffs_shape():
    """Valida que la climatología genere los 5 coeficientes armónicos de Fourier (a0, a1, b1, a2, b2)."""
    import math
    daily_rows = []
    # Generar 60 días sintéticos con patrón sinusoidal
    for doy in range(1, 61):
        temp = 15.0 + 10.0 * math.sin(2.0 * math.pi * doy / 365.25)
        d_str = f"2026-01-{min(31, doy):02d}" if doy <= 31 else f"2026-02-{doy - 31:02d}"
        daily_rows.append([d_str, temp - 4, temp + 4, temp, 8.0, temp, 50.0, 10.0, 0.0, 20.0, 3])

    climatology = build_climatology({"madrid": daily_rows})
    fourier = climatology["cities"]["madrid"]["fourier"]

    assert set(fourier.keys()) == {"a0", "a1", "b1", "a2", "b2"}
    assert isinstance(fourier["a0"], float)
    assert climatology["cities"]["madrid"]["baseline_days"] == 60


# ---------------------------------------------------------------------------
# 4. Tests de Auditoría Predictiva Idempotente
# ---------------------------------------------------------------------------

def test_forecast_log_idempotent(tmp_path: Path):
    """Valida que append_forecast_log no duplique registros para la misma fecha y estación."""
    log_file = tmp_path / "2026-11.csv"
    mock_preds = {
        "Madrid": {
            "pred_ia": {"media": 18.5},
            "pred_owm_5day": [
                {"date": "2026-11-09", "media": 17.0},
                {"date": "2026-11-10", "media": 16.5},
                {"date": "2026-11-11", "media": 16.0},
                {"date": "2026-11-12", "media": 15.5},
                {"date": "2026-11-13", "media": 15.0},
            ]
        }
    }

    # Primera inserción
    count1 = append_forecast_log(mock_preds, log_file)
    assert count1 == 1
    assert log_file.exists()

    # Segunda inserción el mismo día (debe ser idempotente, 0 filas nuevas)
    count2 = append_forecast_log(mock_preds, log_file)
    assert count2 == 0

    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2  # Cabecera + 1 fila


# ---------------------------------------------------------------------------
# 5. Tests de Contrato de Archivos JSON Derivados
# ---------------------------------------------------------------------------

def test_daily_json_contract(tmp_path: Path):
    """Valida el esquema exacto de derived/daily/<slug>.json según §4.6 de la spec."""
    source_dir = tmp_path / "datos"
    out_dir = tmp_path / "derived"
    source_dir.mkdir()

    # Crear CSV de prueba
    csv_file = source_dir / "Madrid.csv"
    csv_file.write_text(
        "fecha_hora,ciudad,temperatura_c,sensacion_c,temp_min,temp_max,humedad_porc,viento_kmh,descripcion_cielo,lat,lon,nubosidad_porc,visibilidad_m,rain_1h,snow_1h\n"
        "2026-11-08T06:00:00Z,Madrid,10.0,9.0,10.0,10.0,80,5.0,cielo claro,40.4168,-3.7038,0,10000,0.0,0.0\n"
        "2026-11-08T14:00:00Z,Madrid,20.0,19.0,20.0,20.0,40,10.0,cielo claro,40.4168,-3.7038,0,10000,0.0,0.0\n",
        encoding="utf-8"
    )
    ciudades_txt = tmp_path / "ciudades.txt"
    ciudades_txt.write_text("Madrid,ES,40.4168,-3.7038\n", encoding="utf-8")

    res = process_derived_pipeline(source_dir, out_dir, ciudades_txt)
    assert res["cities_processed"] == 1

    daily_json_file = out_dir / "daily" / "madrid.json"
    assert daily_json_file.exists()

    with open(daily_json_file, "r", encoding="utf-8") as f:
        daily_data = json.load(f)

    # Verificar claves requeridas
    expected_keys = {"slug", "name", "country", "region", "lat", "lon", "generated_at", "first_date", "last_date", "columns", "rows"}
    assert expected_keys.issubset(set(daily_data.keys()))
    assert daily_data["slug"] == "madrid"
    assert daily_data["columns"] == ["date", "tmin", "tmax", "tmean", "amp", "feels", "hum", "wind", "rain", "clouds", "n"]
    assert len(daily_data["rows"]) == 1
    assert daily_data["rows"][0][4] == 10.0  # amp = 20 - 10


# ---------------------------------------------------------------------------
# 6. Tests de Configuración Upstream y Seguridad
# ---------------------------------------------------------------------------

def test_workflow_has_derived_step_continue_on_error_and_rebase():
    """Valida que actualizar-clima.yml contenga el paso 4b con continue-on-error y rebase antes de push."""
    wf_path = BASE_DIR / ".github" / "workflows" / "actualizar-clima.yml"
    assert wf_path.exists()
    content = wf_path.read_text(encoding="utf-8")

    assert "build_derived.py" in content
    assert "continue-on-error: true" in content
    assert "0 22 * * *" in content
    assert "git pull --rebase" in content


def test_headers_cors():
    """Valida que apps/weather/_headers contenga CORS * y Cache-Control para /derived/* y /*.json."""
    headers_path = BASE_DIR / "_headers"
    assert headers_path.exists()
    content = headers_path.read_text(encoding="utf-8")

    assert "/derived/*" in content
    assert "Access-Control-Allow-Origin: *" in content
    assert "Cache-Control" in content


def test_static_has_no_raw_or_daily_data():
    """Valida INV-WEATHER-6: static/apps/weather no contiene CSVs crudos ni daily/*.json."""
    repo_root = BASE_DIR.parent.parent
    static_weather = repo_root / "static" / "apps" / "weather"

    if static_weather.exists():
        datos_folder = static_weather / "datos"
        if datos_folder.exists():
            csvs = list(datos_folder.glob("*.csv"))
            assert len(csvs) == 0, f"Se encontraron CSVs en static: {csvs}"

        daily_folder = static_weather / "derived" / "daily"
        assert not daily_folder.exists(), "static/apps/weather no debe almacenar derived/daily/"


def test_frontend_remote_first_helper_present():
    """Valida que index.html contenga fetchJSONRemoteFirst y la constante REMOTE_BASE."""
    html_path = BASE_DIR / "index.html"
    assert html_path.exists()
    content = html_path.read_text(encoding="utf-8")

    assert "REMOTE_BASE" in content
    assert "fetchJSONRemoteFirst" in content
    assert "INV-WEATHER-7" in content or "freshness" in content.lower()


# ============================================================================
# W3.2 & W3.3: Focus Mode, Acordeones, PWA & Modo Offline
# ============================================================================

def test_focus_mode_header_and_accordions():
    """Valida cabecera compacta con menú ⋯ y 4 acordeones <details> cerrados por defecto (W3.2)."""
    html_path = BASE_DIR / "index.html"
    content = html_path.read_text(encoding="utf-8")

    # Cabecera Focus Mode
    assert 'id="btn-app-menu-toggle"' in content
    assert 'id="app-options-menu"' in content
    assert 'id="freshness-badge"' in content

    # 4 Acordeones de Divulgación Progresiva
    accordions = [
        "accordion-evolution",
        "accordion-variation",
        "accordion-seasonality",
        "accordion-ai"
    ]
    for acc_id in accordions:
        assert f'id="{acc_id}"' in content
        # Debe ser un tag <details> sin el atributo 'open' por defecto en el HTML inicial
        pattern = rf'<details[^>]*id="{acc_id}"[^>]*>'
        match = re.search(pattern, content)
        assert match is not None, f"No se encontró tag details para {acc_id}"
        assert "open" not in match.group(0), f"El acordeón {acc_id} no debe tener el atributo 'open' por defecto"

    # Puerta de Suficiencia de Datos
    assert "function hasEnoughData" in content
    assert "dataSufficiencyNotice" in content or "Disponible con más datos" in content


def test_mobile_bottom_tabs():
    """Valida barra inferior de pestañas móviles (W3.2)."""
    html_path = BASE_DIR / "index.html"
    content = html_path.read_text(encoding="utf-8")

    assert 'class="mobile-bottom-tabs"' in content
    assert 'data-tab="hoy"' in content
    assert 'data-tab="comparar"' in content
    assert 'data-tab="ranking"' in content
    assert 'data-tab="ia"' in content
    assert "@media (max-width: 768px)" in content


def test_pwa_manifest_and_icons():
    """Valida el manifiesto PWA y la presencia de iconos vectoriales y maskable (W3.3)."""
    for base in [BASE_DIR, BASE_DIR.parent.parent / "static" / "apps" / "weather"]:
        manifest_file = base / "manifest.json"
        assert manifest_file.exists(), f"Falta {manifest_file}"

        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest.get("start_url") == "/apps/weather/?source=pwa"
        assert manifest.get("scope") == "/apps/weather/"
        assert manifest.get("display") == "standalone"
        assert len(manifest.get("icons", [])) >= 2

        assert (base / "icon.svg").exists(), f"Falta icon.svg en {base}"
        assert (base / "icon-192.png").exists(), f"Falta icon-192.png en {base}"
        assert (base / "icon-512.png").exists(), f"Falta icon-512.png en {base}"


def test_sw_cache_rules_and_csv_firewall():
    """Valida reglas de Service Worker: SWR para JSONs y prohibición estricta de CSVs (W3.3 / INV-WEATHER-10)."""
    for base in [BASE_DIR, BASE_DIR.parent.parent / "static" / "apps" / "weather"]:
        sw_file = base / "sw.js"
        assert sw_file.exists(), f"Falta {sw_file}"
        sw_content = sw_file.read_text(encoding="utf-8")

        # Stale-while-revalidate para JSONs
        assert "derived/" in sw_content or ".json" in sw_content
        # Cortafuegos estricto: no cachear .csv (INV-WEATHER-10)
        assert ".csv" in sw_content
        assert "nunca cachear" in sw_content.lower() or "no cachear" in sw_content.lower() or "never cache" in sw_content.lower()

    # index.html contiene offline-banner, pwa-toast y registro de Service Worker
    html_content = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    assert 'id="offline-banner"' in html_content
    assert 'id="pwa-install-toast"' in html_content
    assert "serviceWorker.register" in html_content
    assert "weather_my_cities" in html_content


def test_frontend_inline_js_syntax():
    """Valida sintaxis JavaScript de index.html con node --check (evita SyntaxError en navegador)."""
    import os
    import shutil
    import subprocess
    import tempfile

    node_bin = shutil.which("node")
    if not node_bin:
        pytest.skip("Node.js no está instalado en el entorno")

    html_path = BASE_DIR / "index.html"
    content = html_path.read_text(encoding="utf-8")
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    assert len(scripts) >= 1

    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(scripts[0])
        tmp_name = f.name

    try:
        res = subprocess.run([node_bin, "--check", tmp_name], capture_output=True, text=True, encoding="utf-8")
        assert res.returncode == 0, f"Error de sintaxis JS en index.html:\n{res.stderr}"
    finally:
        os.unlink(tmp_name)


# ---------------------------------------------------------------------------
# 11. Tests de Contrato Real de Producción & Zero-404 Inventory (W3.3-FIX)
# ---------------------------------------------------------------------------

def test_production_derived_inventory_168_cities():
    """Verifica que el inventario completo de 168 ciudades derivadas existe en apps y static."""
    # 1. Verificar index.json y climatology.json en apps/weather y static/apps/weather
    for base in [BASE_DIR, BASE_DIR.parent.parent / "static" / "apps" / "weather"]:
        index_file = base / "derived" / "index.json"
        assert index_file.exists(), f"Falta {index_file}"
        with open(index_file, "r", encoding="utf-8") as f:
            idx_data = json.load(f)

        cities = idx_data.get("cities", [])
        assert len(cities) == 168, f"Esperadas 168 ciudades en {index_file}, obtenidas {len(cities)}"

        climatology_file = base / "derived" / "climatology.json"
        assert climatology_file.exists(), f"Falta {climatology_file}"
        with open(climatology_file, "r", encoding="utf-8") as f:
            clim_data = json.load(f)
        assert len(clim_data.get("cities", {})) == 168

    # 2. Verificar que las 168 ciudades tienen su daily JSON generado en apps/weather/derived/daily/
    daily_dir = BASE_DIR / "derived" / "daily"
    assert daily_dir.exists(), f"Falta {daily_dir}"
    daily_files = list(daily_dir.glob("*.json"))
    assert len(daily_files) == 168, f"Esperados 168 daily JSON en {daily_dir}, encontrados {len(daily_files)}"

    with open(BASE_DIR / "derived" / "index.json", "r", encoding="utf-8") as f:
        idx_data = json.load(f)

    for c in idx_data.get("cities", []):
        slug = c.get("slug")
        city_json = daily_dir / f"{slug}.json"
        assert city_json.exists(), f"Falta daily JSON para ciudad {c.get('name', slug)} (slug {slug}) en {city_json}"
        with open(city_json, "r", encoding="utf-8") as f:
            city_data = json.load(f)
        assert len(city_data.get("rows", [])) >= 1, f"Filas vacías en {city_json}"


def test_presets_and_global_summary_zero_404_contract():
    """Verifica que global_summary.json contiene las 168 ciudades reales y los presets resuelven con 0 errores 404."""
    summary_file = BASE_DIR / "global_summary.json"
    assert summary_file.exists()
    with open(summary_file, "r", encoding="utf-8") as f:
        summary_data = json.load(f)

    assert summary_data.get("total_cities") == 168
    assert summary_data.get("total_records", 0) >= 180000

    # Todos los slugs de los presets 1-clic deben existir en derived/daily/<slug>.json
    preset_slugs = [
        "madrid", "barcelona", "bilbao", "sevilla", "leon",
        "london", "new-york", "tokyo", "singapore",
        "sao-paulo", "sydney", "panama-city", "los-angeles",
        "beijing", "ulaanbaatar"
    ]
    daily_dir = BASE_DIR / "derived" / "daily"
    for slug in preset_slugs:
        target = daily_dir / f"{slug}.json"
        assert target.exists(), f"El slug del preset '{slug}' no existe en {target} (provocaría 404)"


def test_workflow_generates_derived_on_every_event():
    """Verifica que el workflow de CI/CD genera los derivados compactos en push, dispatch y schedule sin bloqueos."""
    workflow_file = BASE_DIR / ".github" / "workflows" / "actualizar-clima.yml"
    assert workflow_file.exists()
    content = workflow_file.read_text(encoding="utf-8")

    assert "build_derived.py --source datos --out derived --month-log" in content
    assert "if: github.event.schedule == '0 22 * * *'" not in content, "El workflow bloquea la generación de derivados en eventos push"


def test_frontend_zero_404_and_instant_kpi_architecture():
    """Verifica la arquitectura frontend Zero-404, el renderizado de KPIs en 0ms y el Service Worker v3.0.2."""
    html_content = (BASE_DIR / "index.html").read_text(encoding="utf-8")

    # 1. derivedIndexSet para prevenir 404s
    assert "derivedIndexSet" in html_content
    assert "derivedIndexSet.has(slug)" in html_content

    # 2. Renderizado instantáneo de KPIs en updateDashboard
    assert "updateKPIs({}, checkedMetric, selectedValues)" in html_content

    # 3. Service Worker versión 3.0.2
    sw_content = (BASE_DIR / "sw.js").read_text(encoding="utf-8")
    assert "weather-v3.0.2" in sw_content



