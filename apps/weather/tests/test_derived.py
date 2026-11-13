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
    build_weekly_summary,
    build_cities_catalog,
    compute_custom_comfort_score,
    compute_twin_climates,
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

    # 3. Service Worker versión 3.3.1
    sw_content = (BASE_DIR / "sw.js").read_text(encoding="utf-8")
    assert "weather-v3.3.1" in sw_content





# ---------------------------------------------------------------------------
# 5. Tests de W3.4: "Es normal?", Warming Stripes, Marcador y Explicabilidad
# ---------------------------------------------------------------------------

def test_col_map_maps_spanish_min_max_and_rain():
    """Verifica la correccion del bug P0 en col_map (temp_min_c, temp_max_c, lluvia_1h)."""
    from apps.weather.build_derived import aggregate_daily
    df = pd.DataFrame([
        {"fecha_hora": "2026-11-08T06:00:00Z", "temperatura_c": 12.0, "temp_min_c": 8.5, "temp_max_c": 13.0, "lluvia_1h": 1.2},
        {"fecha_hora": "2026-11-08T14:00:00Z", "temperatura_c": 19.5, "temp_min_c": 18.0, "temp_max_c": 21.5, "lluvia_1h": 0.5},
    ])
    rows = aggregate_daily(df)
    assert len(rows) == 1
    # row = [date, tmin, tmax, tmean, amp, feels, hum, wind, rain, clouds, n]
    r = rows[0]
    assert r[1] == 8.5, f"tmin debe ser 8.5, no {r[1]}"
    assert r[2] == 21.5, f"tmax debe ser 21.5, no {r[2]}"
    assert r[4] == round(21.5 - 8.5, 1)  # amp
    assert r[8] == 1.7  # rain acumulada (1.2 + 0.5)


def test_doy_baseline_excludes_target_and_wraps_year():
    """Verifica INV-WEATHER-11: linea base +/- 7 dias excluyendo el dia evaluado y cruzando ano."""
    from apps.weather.build_derived import compute_doy_baseline
    # Sintetizar serie que cruza fin de ano
    rows = [
        ["2025-12-30", 5.0, 10.0, 7.0, 5.0, 6.0, 70, 10, 0, 0, 3],
        ["2025-12-31", 6.0, 11.0, 8.0, 5.0, 7.0, 70, 10, 0, 0, 3],
        ["2026-01-01", 7.0, 12.0, 9.0, 5.0, 8.0, 70, 10, 0, 0, 3],  # target
        ["2026-01-02", 8.0, 13.0, 10.0, 5.0, 9.0, 70, 10, 0, 0, 3],
    ]
    # Para 2026-01-01 (doy 1), debe incluir 2025-12-30 (doy 364), 2025-12-31 (doy 365) y 2026-01-02 (doy 2)
    # y EXCLUIR 2026-01-01 (tmean = 9.0)
    baseline = compute_doy_baseline(rows, "2026-01-01")
    assert baseline is not None
    expected_mean = round((7.0 + 8.0 + 10.0) / 3, 2)
    assert baseline == expected_mean, f"Baseline debe ser {expected_mean}, no {baseline}"


def test_percentile_and_record_requires_20_days():
    """Verifica que el record requiera >= 20 dias en el mes segun INV-WEATHER-11."""
    from apps.weather.build_derived import build_insights
    # Caso 1: Menos de 20 dias en el mes -> record = False
    short_rows = [
        [f"2026-11-{i:02d}", 10.0, 20.0, 15.0 + i, 10.0, 15.0, 60, 5, 0, 0, 3]
        for i in range(1, 15)  # 14 dias
    ]
    ins_short = build_insights({"test-city": short_rows}, {"test-city": [0.0]*14})
    city_res = ins_short["cities"]["test-city"]
    assert city_res["record"] is False, "No debe registrar record con < 20 dias en el mes"

    # Caso 2: >= 20 dias y valor maximo -> record = True
    long_rows = [
        [f"2026-11-{i:02d}", 10.0, 20.0, 10.0 + i, 10.0, 15.0, 60, 5, 0, 0, 3]
        for i in range(1, 26)  # 25 dias
    ]
    ins_long = build_insights({"test-city": long_rows}, {"test-city": [0.0]*25})
    assert ins_long["cities"]["test-city"]["record"] is True
    assert ins_long["cities"]["test-city"]["record_type"] == "warm"
    assert ins_long["cities"]["test-city"]["history_since"] == "oct. 2025"


def test_scorecard_mae_math_and_calibrating_status(tmp_path):
    """Verifica INV-WEATHER-12: status calibrating cuando n < 7 y calculo correcto de MAE."""
    from apps.weather.build_derived import build_scorecard
    log_dir = tmp_path / "forecast_log"
    log_dir.mkdir()
    # Escribir log con 2 emisiones (< 7)
    log_content = (
        "fecha_emision,slug,ia_d1,ia_d2,ia_d3,ia_d4,ia_d5,owm_d1,owm_d2,owm_d3,owm_d4,owm_d5\n"
        "2026-11-01,test-city,15.0,16.0,17.0,18.0,19.0,14.0,15.0,16.0,17.0,18.0\n"
        "2026-11-02,test-city,16.0,17.0,18.0,19.0,20.0,15.0,16.0,17.0,18.0,19.0\n"
    )
    (log_dir / "2026-11.csv").write_text(log_content, encoding="utf-8")

    # Observaciones reales: D+1 para emision 2026-11-01 es 2026-11-02 (tmean=15.5)
    daily_by_slug = {
        "test-city": [
            ["2026-11-01", 10.0, 20.0, 14.0, 10.0, 14.0, 60, 5, 0, 0, 3],
            ["2026-11-02", 10.0, 20.0, 15.5, 10.0, 15.5, 60, 5, 0, 0, 3],
            ["2026-11-03", 10.0, 20.0, 16.5, 10.0, 16.5, 60, 5, 0, 0, 3],
        ]
    }
    scorecard = build_scorecard(log_dir, daily_by_slug, {})
    assert scorecard["status"] == "calibrating"
    assert scorecard["live_horizons"]["d1"]["status"] == "calibrating"
    assert scorecard["live_horizons"]["d1"]["n_audited"] == 2
    # IA D+1: emision 1 -> target 2026-11-02, obs=15.5, pred=15.0, err=0.5
    #         emision 2 -> target 2026-11-03, obs=16.5, pred=16.0, err=0.5
    # mean err IA = 0.5
    assert scorecard["live_horizons"]["d1"]["mae_ia"] == 0.5


def test_forecast_log_upsert_idempotent_5_horizons(tmp_path):
    """Verifica que append_forecast_log haga upsert idempotentemente sobre las 12 columnas."""
    from apps.weather.build_derived import append_forecast_log
    month_file = tmp_path / "forecast_log" / "2026-11.csv"
    preds_v1 = {
        "Madrid": {
            "pred_ia_5day": [{"date": "2026-11-10", "media": 14.0, "min": 10.0, "max": 18.0}],
            "pred_owm_5day": [{"media": 13.5}],
        }
    }
    # Primera ejecucion: anade fila
    count1 = append_forecast_log(preds_v1, month_file)
    assert count1 == 1
    lines1 = month_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines1) == 2  # header + 1 row
    assert "14.0" in lines1[1]

    # Segunda ejecucion con actualizacion para la misma fecha: debe actualizar sin duplicar fila
    preds_v2 = {
        "Madrid": {
            "pred_ia_5day": [{"date": "2026-11-10", "media": 14.5, "min": 10.0, "max": 18.0}],
            "pred_owm_5day": [{"media": 13.5}],
        }
    }
    count2 = append_forecast_log(preds_v2, month_file)
    assert count2 == 0, 'No debe anadir nuevas filas en update'
    lines2 = month_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines2) == 2, "El upsert duplico la fila en vez de actualizarla"
    assert "14.5" in lines2[1]


def test_pred_ia_5day_shape_and_physics():
    """Verifica INV-WEATHER-3: pred_ia_5day tiene 5 horizontes y cumple coherencia min <= media <= max."""
    from apps.weather.read_weather import generar_prediccion_ia_ciudad
    madrid_csv = BASE_DIR / "datos" / "Madrid.csv"
    if not madrid_csv.exists():
        madrid_csv = Path(__file__).resolve().parent.parent.parent.parent / "app_weather" / "datos" / "Madrid.csv"
    if madrid_csv.exists():
        res = generar_prediccion_ia_ciudad(str(madrid_csv))
        assert "pred_ia_5day" in res
        p5 = res["pred_ia_5day"]
        assert len(p5) == 5
        for day in p5:
            assert "date" in day
            assert day["min"] <= day["media"] <= day["max"], f"Coherencia fisica violada: {day}"


def test_explain_contributions_sum_to_prediction():
    """Verifica INV-WEATHER-13: explain contiene inputs, contributions y suma a baseline + delta."""
    from apps.weather.read_weather import generar_prediccion_ia_ciudad
    madrid_csv = BASE_DIR / "datos" / "Madrid.csv"
    if not madrid_csv.exists():
        madrid_csv = Path(__file__).resolve().parent.parent.parent.parent / "app_weather" / "datos" / "Madrid.csv"
    if madrid_csv.exists():
        res = generar_prediccion_ia_ciudad(str(madrid_csv))
        assert "explain" in res and res["explain"] is not None
        exp = res["explain"]
        assert "baseline_c" in exp
        assert "contributions_c" in exp
        assert "contributions_pct" in exp
        base = exp["baseline_c"]
        delta = sum(exp["contributions_c"].values())
        # base + delta debe ser muy cercano al valor medio predicho D+1 (+/- 0.2C por redondeo)
        pred_media = res["media"]
        reconstructed = round(base + delta, 1)
        assert abs(reconstructed - pred_media) <= 0.2, f"Explain no reconstruye media: {reconstructed} vs {pred_media}"


def test_w34_frontend_dom_and_i18n():
    """Verifica integracion DOM de Warming Stripes, Marcador Scorecard y paridad i18n."""
    html_content = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    assert "accordion-stripes" in html_content
    assert "stripesCanvas" in html_content
    assert "scorecard-hero" in html_content
    assert "why-card" in html_content
    assert "weather-normal-chip" in html_content
    assert "renderWarmingStripes" in html_content
    assert "renderScorecardAndExplain" in html_content


def test_inv_weather_14_version_coherence():
    """Verifica INV-WEATHER-14: Version v3.3.1 exacta en YAML, sw.js, catalogo y títulos v3.3."""
    import yaml
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    yaml_file = repo_root / "data" / "apps" / "weather.yaml"
    assert yaml_file.exists()
    ydata = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
    assert ydata["current_version"] == "v3.3.1"
    assert "v3.3" in ydata["title"]["es"]
    assert "v3.3" in ydata["title"]["en"]

    # Primer release debe ser v3.3.1 y released
    assert ydata["releases"][0]["version"] == "v3.3.1"
    assert ydata["releases"][0]["state"] == "released"

    # Service Worker y lista de apps
    sw_txt = (BASE_DIR / "sw.js").read_text(encoding="utf-8")
    assert "weather-v3.3.1" in sw_txt
    apps_list_txt = (repo_root / "layouts" / "apps" / "list.html").read_text(encoding="utf-8")
    assert '"v3.3.1"' in apps_list_txt

    # Fichas Markdown
    es_md = repo_root / "content" / "es" / "apps" / "weather" / "index.md"
    en_md = repo_root / "content" / "en" / "apps" / "weather" / "index.md"
    assert 'title: "Weather Intelligence v3.3"' in es_md.read_text(encoding="utf-8")
    assert 'title: "Weather Intelligence v3.3"' in en_md.read_text(encoding="utf-8")

    # Frontend
    html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    assert "Weather Intelligence v3.3" in html


# ---------------------------------------------------------------------------
# 6. Tests de W3.5: Buscador de Destinos, Clima Gemelo y Deep-Links
# ---------------------------------------------------------------------------

def test_climatology_enriched_fields_and_rain_pct():
    """Verifica que build_climatology incluya amp, hum, wind, clouds, rain_pct normalizado y feature_stats."""
    rows_nov = [
        [f"2025-11-{min(30, d):02d}", 6.0, 16.0, 11.0, 10.0, 10.5, 60.0, 12.0, (1.2 if d <= 9 else 0.0), 30.0, 3]
        for d in range(1, 39)  # 38 días acumulados en noviembre (9 con lluvia -> 23.7%)
    ]
    rows_feb = [
        [f"2026-02-{d:02d}", 4.0, 14.0, 9.0, 10.0, 8.5, 70.0, 15.0, (0.5 if d <= 7 else 0.0), 40.0, 3]
        for d in range(1, 29)  # 28 días en febrero (7 con lluvia -> 25.0%)
    ]
    rows_short = [
        [f"2026-05-{d:02d}", 10.0, 20.0, 15.0, 10.0, 14.5, 50.0, 8.0, 0.0, 10.0, 3]
        for d in range(1, 6)  # 5 < 10 -> null
    ]
    clim = build_climatology({"test-city": rows_nov + rows_feb + rows_short})
    assert "feature_stats" in clim
    fstats = clim["feature_stats"]
    assert fstats["features"] == ["tmean", "amp", "hum", "wind", "rain_pct"]
    for feat in fstats["features"]:
        assert fstats["std"][feat] > 0

    m_nov = clim["cities"]["test-city"]["months"]["11"]
    m_feb = clim["cities"]["test-city"]["months"]["2"]
    assert clim["cities"]["test-city"]["months"]["5"] is None
    for key in ("amp", "hum", "wind", "clouds", "rain_pct"):
        assert key in m_nov and key in m_feb
    assert m_nov["rain_pct"] == pytest.approx(round(100.0 * 9 / 38, 1), abs=0.1)
    assert m_feb["rain_pct"] == pytest.approx(25.0, abs=0.1)


def test_custom_comfort_finder_ranking():
    """Valida INV-WEATHER-15: el ranking personalizado reacciona a ideal_temp, rain_pref y wind_pref."""
    dry_warm = {"tmean": 22.0, "hum": 50.0, "wind": 8.0, "rain_pct": 4.0, "n_days": 30, "rain_days": 1, "comfort": 92}
    wet_windy = {"tmean": 22.0, "hum": 82.0, "wind": 28.0, "rain_pct": 48.0, "n_days": 30, "rain_days": 14, "comfort": 48}
    cold_crisp = {"tmean": 6.0, "hum": 45.0, "wind": 6.0, "rain_pct": 5.0, "n_days": 30, "rain_days": 1, "comfort": 55}

    s_dry = compute_custom_comfort_score(dry_warm, ideal_temp=22.0, rain_pref="dry", wind_pref="calm")
    s_wet = compute_custom_comfort_score(wet_windy, ideal_temp=22.0, rain_pref="dry", wind_pref="calm")
    s_cold_pref = compute_custom_comfort_score(cold_crisp, ideal_temp=6.0, rain_pref="dry", wind_pref="calm")

    assert 0 <= s_wet < s_dry <= 100
    assert s_cold_pref > compute_custom_comfort_score(dry_warm, ideal_temp=6.0, rain_pref="dry", wind_pref="calm")
    assert compute_custom_comfort_score(None) == 0


def test_twin_climate_zscore_euclidean_symmetry():
    """Valida INV-WEATHER-16: Clima Gemelo excluye origen, puntua ~100% ante clon y ordena por z-score."""
    clim = {
        "feature_stats": {
            "features": ["tmean", "amp", "hum", "wind", "rain_pct"],
            "mean": {"tmean": 15.0, "amp": 8.0, "hum": 60.0, "wind": 12.0, "rain_pct": 20.0},
            "std": {"tmean": 8.0, "amp": 3.0, "hum": 15.0, "wind": 5.0, "rain_pct": 15.0},
        },
        "cities": {
            "madrid": {
                "months": {
                    "5": {"tmean": 18.0, "amp": 11.0, "hum": 52.0, "wind": 10.0, "rain_pct": 12.0}
                }
            },
            "clone-dec": {
                "months": {
                    "12": {"tmean": 18.0, "amp": 11.0, "hum": 52.0, "wind": 10.0, "rain_pct": 12.0}
                }
            },
            "polar-dec": {
                "months": {
                    "12": {"tmean": -10.0, "amp": 4.0, "hum": 85.0, "wind": 30.0, "rain_pct": 60.0}
                }
            },
        },
    }
    res = compute_twin_climates(clim, target_slug="madrid", target_month=5, candidate_month=12, top_n=5)
    assert len(res) == 2
    assert all(r["slug"] != "madrid" for r in res)
    assert res[0]["slug"] == "clone-dec"
    assert res[0]["distance"] == 0.0
    assert res[0]["similarity_pct"] == 100
    assert res[1]["slug"] == "polar-dec" and res[1]["similarity_pct"] < 50


def test_w35_climatology_168_cities_contract():
    """Valida contrato real de climatology.json en apps/weather y static/apps/weather (168 ciudades, feature_stats)."""
    repo_root = BASE_DIR.parent.parent
    app_clim = BASE_DIR / "derived" / "climatology.json"
    static_clim = repo_root / "static" / "apps" / "weather" / "derived" / "climatology.json"
    assert app_clim.exists() and static_clim.exists()
    assert app_clim.read_bytes() == static_clim.read_bytes()

    data = json.loads(app_clim.read_text(encoding="utf-8"))
    assert "feature_stats" in data
    assert len(data["cities"]) == 168
    madrid_may = data["cities"]["madrid"]["months"]["5"]
    for key in ("amp", "hum", "wind", "clouds", "rain_pct"):
        assert key in madrid_may

    for fname in ("index.json", "climatology.json", "insights.json", "scorecard.json", "weekly_extremes.json"):
        assert (repo_root / "static" / "apps" / "weather" / "derived" / fname).exists()


def test_w35_frontend_dom_i18n_and_deeplinks():
    """Valida DOM W3.5 dentro de view-atlas, eventos GA4, paridad ES/EN y cero botones extra en cabecera."""
    html_content = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    for token in (
        'id="atlas-subnav"',
        'id="atlas-pane-ranking"',
        'id="atlas-pane-finder"',
        'id="atlas-pane-twin"',
        'ensureClimatologyLoaded',
        'focusCityInObservatory',
        'computeCustomComfortScore',
        'weather_finder_search',
        'weather_twin_search',
        'weather_finder_open_city',
        'weather_deeplink_copy',
        'atlasMode',
    ):
        assert token in html_content, f"Falta token W3.5 en index.html: {token}"

    # Cabecera mantiene exactamente las 3 vistas top-level (sin botón W3.5 en header)
    header_match = re.search(r'<header class="main-header">([\s\S]*?)</header>', html_content)
    assert header_match
    header_html = header_match.group(1)
    assert 'data-atlas-mode' not in header_html


# ---------------------------------------------------------------------------
# 7. Tests de W3.6: Motor de Crecimiento (PNG, Embed, SEO Hugo y Scriba)
# ---------------------------------------------------------------------------

def test_weekly_extremes_summary_and_scriba_snippets():
    """Valida INV-WEATHER-19 & INV-WEATHER-12: extremos 7D reales, desacople scorecard y copys ES/EN <= 240 chars."""
    daily_by_slug = {
        "abuja": [
            ["2026-11-10", 24.0, 35.0, 29.5, 11.0, 30.0, 45.0, 8.0, 0.0, 10.0, 3],
            ["2026-11-11", 25.0, 36.6, 30.8, 11.6, 31.2, 42.0, 7.0, 0.0, 5.0, 3],
        ],
        "ulaanbaatar": [
            ["2026-11-08", -23.0, -9.0, -16.0, 14.0, -21.0, 65.0, 14.0, 0.0, 20.0, 3],
        ],
        "tokyo": [
            ["2026-11-11", 12.0, 18.0, 15.0, 6.0, 14.5, 82.0, 18.0, 22.5, 90.0, 3],
            ["2026-11-12", 13.0, 19.0, 16.0, 6.0, 15.5, 78.0, 12.0, 10.8, 70.0, 3],
        ],
        "madrid": [
            ["2026-11-12", 14.0, 22.0, 18.0, 8.0, 17.8, 50.0, 6.0, 0.0, 10.0, 3],
        ],
    }
    anoms = {
        "abuja": [2.0, 3.1],
        "ulaanbaatar": [-11.0],
        "tokyo": [1.0, 0.5],
        "madrid": [6.5],
    }
    scorecard = {
        "status": "calibrating",
        "min_samples_required": 7,
        "total_audited_pairs": 12,
        "live_horizons": {"d1": {"horizon_days": 1, "mae_ia": 1.6, "mae_owm": 1.2, "n_audited": 12, "status": "ok"}},
        "weekly_wins": {"ia": 5, "owm": 6, "draws": 1, "total_audited": 12},
        "retrospective_ia": {"label": "Retrospectivo 60d (solo IA)", "mae_d1_d5": [1.3, 1.6, 1.8, 1.9, 2.0]},
    }
    meta = {
        "abuja": {"name": "Abuja", "country": "NG", "region": "africa"},
        "ulaanbaatar": {"name": "Ulaanbaatar", "country": "MN", "region": "asia"},
        "tokyo": {"name": "Tokyo", "country": "JP", "region": "asia"},
        "madrid": {"name": "Madrid", "country": "ES", "region": "spain"},
    }
    summary = build_weekly_summary(daily_by_slug, anoms, scorecard=scorecard, slug_to_meta=meta, days=7)
    assert summary["window"]["end_date"] == "2026-11-12"
    assert summary["hottest"][0]["slug"] == "abuja" and summary["hottest"][0]["tmax_c"] == 36.6
    assert summary["coldest"][0]["slug"] == "ulaanbaatar" and summary["coldest"][0]["tmin_c"] == -23.0
    assert summary["wettest"][0]["slug"] == "tokyo" and summary["wettest"][0]["rain_7d_mm"] == 33.3
    assert summary["biggest_positive_anomaly"]["slug"] == "madrid" and summary["biggest_positive_anomaly"]["anomaly_c"] == 6.5
    assert summary["biggest_negative_anomaly"]["slug"] == "ulaanbaatar"
    assert "live_horizons" in summary["scorecard_snapshot"]
    assert "retrospective_ia" in summary["scorecard_snapshot"]
    for lang_key in ("es", "en"):
        snip = summary["scriba_ready_snippets"][lang_key]
        assert len(snip["x_post"]) <= 240
        assert len(snip["linkedin_bullets"]) >= 3
        assert snip["newsletter_box"]


def test_weekly_extremes_168_cities_and_cities_catalog_contract():
    """Valida contrato real de weekly_extremes.json y data/weather/cities_catalog.json (168 estaciones, INV-WEATHER-6)."""
    repo_root = BASE_DIR.parent.parent
    app_weekly = BASE_DIR / "derived" / "weekly_extremes.json"
    static_weekly = repo_root / "static" / "apps" / "weather" / "derived" / "weekly_extremes.json"
    assert app_weekly.exists() and static_weekly.exists()
    assert app_weekly.read_bytes() == static_weekly.read_bytes()

    weekly = json.loads(app_weekly.read_text(encoding="utf-8"))
    for k in ("window", "hottest", "coldest", "wettest", "comfort_leaders", "scorecard_snapshot", "scriba_ready_snippets"):
        assert k in weekly
    assert len(weekly["scriba_ready_snippets"]["es"]["x_post"]) <= 240
    assert len(weekly["scriba_ready_snippets"]["en"]["x_post"]) <= 240

    catalog_file = repo_root / "data" / "weather" / "cities_catalog.json"
    assert catalog_file.exists()
    catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
    assert len(catalog) == 168
    regions = set()
    for row in catalog:
        for field in ("slug", "name", "country", "region", "lat", "lon"):
            assert field in row
        regions.add(row["region"])
    assert regions == {"spain", "europe", "asia", "americas", "africa", "oceania"}

    # INV-WEATHER-6: firewall estático sin daily/ ni CSVs
    assert not (repo_root / "static" / "apps" / "weather" / "derived" / "daily").exists()


def test_embed_widget_and_headers_security():
    """Valida INV-WEATHER-18: embed.html autónomo (< 25 KB), seguro sin XSS, atribución y headers CSP."""
    repo_root = BASE_DIR.parent.parent
    app_embed = BASE_DIR / "embed.html"
    static_embed = repo_root / "static" / "apps" / "weather" / "embed.html"
    assert app_embed.exists() and static_embed.exists()
    assert app_embed.read_bytes() == static_embed.read_bytes()
    assert app_embed.stat().st_size < 25 * 1024

    embed_html = app_embed.read_text(encoding="utf-8")
    assert "^[a-z0-9-]+$" in embed_html
    assert "textContent" in embed_html
    assert "https://datalaria.com/" in embed_html
    assert "https://cdn." not in embed_html

    headers_txt = (BASE_DIR / "_headers").read_text(encoding="utf-8")
    assert "/embed.html" in headers_txt
    assert "Content-Security-Policy: frame-ancestors *;" in headers_txt
    assert "Access-Control-Allow-Origin: *" in headers_txt


def test_share_card_png_and_hugo_seo_landing_dom():
    """Valida INV-WEATHER-20 (PNG 1200x630), Focus Mode intacto y Solución Intermedia SEO Hugo (168 enlaces)."""
    repo_root = BASE_DIR.parent.parent
    index_html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    for token in (
        "shareCityCardPNG",
        "openEmbedModal",
        "w36-embed-modal",
        "canvas.width = 1200",
        "canvas.height = 630",
        "weather_share_card_png",
        "weather_embed_copy",
        "menu-city-explorer-link",
    ):
        assert token in index_html, f"Falta token W3.6 en index.html: {token}"

    # Focus Mode (W3.2): <header> mantiene exactamente 3 vistas top-level sin botones extra
    header_match = re.search(r'<header class="main-header">([\s\S]*?)</header>', index_html)
    assert header_match
    header_html = header_match.group(1)
    assert len(re.findall(r'class="view-btn', header_html)) == 3
    assert "shareCityCardPNG" not in header_html and "openEmbedModal" not in header_html

    es_seo = repo_root / "content" / "es" / "clima-ciudad.md"
    en_seo = repo_root / "content" / "en" / "weather-city.md"
    tpl_seo = repo_root / "layouts" / "weather-city" / "single.html"
    assert es_seo.exists() and en_seo.exists() and tpl_seo.exists()
    assert 'url: "/es/apps/weather/clima/"' in es_seo.read_text(encoding="utf-8")
    assert 'url: "/en/apps/weather/climate/"' in en_seo.read_text(encoding="utf-8")

    tpl_txt = tpl_seo.read_text(encoding="utf-8")
    assert "site.Data.weather.cities_catalog" in tpl_txt
    assert "^[a-z0-9-]+$" in tpl_txt
    assert "weather_city_landing_view" in tpl_txt
    assert "/apps/helix/" not in tpl_txt


def test_w36_ux_card_remove_and_controls_polish():
    """Valida INV-WEATHER-21: botón '✕' en Super-Cards, Choices transparente y filtros alineados."""
    html_txt = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    for token in (
        "card-remove-btn",
        "removeCityFromSelection",
        "clearAllCities",
        "btn-clear-cities",
        "city-count-badge",
        "kpi-empty-state",
        "btn-empty-load-spain",
        "controls-cities-row",
        "controls-filters-row",
        "syncChoiceChipAccents",
        "weather_city_remove",
        "weather_city_clear",
        "btnRemoveCity",
        "btnClearCities",
        "kpiEmptyTitle",
        "btnLoadSpainPreset",
        "choicesMaxItems",
        "choicesNoResults",
    ):
        assert token in html_txt, f"Falta token W3.6-UX en index.html: {token}"

    assert "background-color: transparent !important;" in html_txt
    assert 'onclick="removeCity' not in html_txt
    assert "body.light-mode #city-select-container" in html_txt

