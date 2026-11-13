"""Suite de verificación determinista para Weather Service v2.0 (INV-WEATHER-1..4)."""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
import tempfile
import pytest

from apps.weather.read_weather import (
    CABECERA_15_COLUMNAS,
    COUNTRY_TO_REGION,
    VALID_REGIONS,
    build_city_summary,
    build_global_summary,
    compute_comfort_index,
    generar_prediccion_ia_ciudad,
    infer_region,
    rebuild_offline,
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATOS_DIR = BASE_DIR / "datos"
CIUDADES_FILE = BASE_DIR / "ciudades.txt"
PRED_FILE = BASE_DIR / "predicciones.json"
MAP_FILE = BASE_DIR / "city_locations.json"
SUMMARY_FILE = BASE_DIR / "global_summary.json"


# ============================================================================
# 1. INV-WEATHER-1: Integridad de Esquema CSV de 15 Columnas
# ============================================================================

def test_inv_weather_1_csv_schema_integrity():
    """Valida que todos los CSVs en datos/ tengan exactamente 15 columnas canónicas."""
    csv_files = list(DATOS_DIR.glob("*.csv"))
    assert len(csv_files) >= 50, f"Se esperaban al menos 50 CSVs de ciudades, encontrados: {len(csv_files)}"

    for csv_file in csv_files:
        with open(csv_file, "r", encoding="utf-8") as f:
            header_line = f.readline().strip()
            cols = [c.strip() for c in header_line.split(",")]
            assert cols == CABECERA_15_COLUMNAS, f"Cabecera inválida en {csv_file.name}: {cols}"

            reader = csv.reader(f)
            first_row = next(reader, None)
            if first_row:
                assert len(first_row) == 15, f"Fila en {csv_file.name} no tiene 15 columnas: {len(first_row)}"


# ============================================================================
# 2. INV-WEATHER-2: Retrocompatibilidad de predicciones.json y city_locations.json
# ============================================================================

def test_inv_weather_2_predictions_and_map_backwards_compatibility():
    """Valida retrocompatibilidad de predicciones.json y city_locations.json."""
    assert PRED_FILE.exists(), f"No se encontró {PRED_FILE}"
    assert MAP_FILE.exists(), f"No se encontró {MAP_FILE}"

    with open(PRED_FILE, "r", encoding="utf-8") as f:
        preds = json.load(f)

    assert isinstance(preds, dict)
    assert len(preds) >= 100, f"Se esperaban al menos 100 ciudades en predicciones.json, encontradas {len(preds)}"

    for city_name, city_data in preds.items():
        assert "pred_owm_5day" in city_data, f"Falta pred_owm_5day en {city_name}"
        assert "pred_ia" in city_data, f"Falta pred_ia en {city_name}"
        ia_pred = city_data["pred_ia"]
        assert all(k in ia_pred for k in ("max", "min", "media", "registros")), f"Claves incompletas en pred_ia de {city_name}"

        # Si tiene modelo entrenado, validar estructura de model_metrics
        if ia_pred["registros"] >= 10 and ia_pred["max"] is not None:
            metrics = city_data.get("model_metrics")
            assert metrics is not None, f"Falta model_metrics para {city_name} con registros >= 10"
            assert "r2_media" in metrics
            assert "mae_30d_c" in metrics
            assert "bias_30d_c" in metrics
            assert "top_features" in metrics

    with open(MAP_FILE, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    assert isinstance(map_data, list)
    assert len(map_data) >= 100
    for entry in map_data:
        assert all(k in entry for k in ("ciudad", "lat", "lon", "temp"))
        assert isinstance(entry["temp"], (int, float))


# ============================================================================
# 3. INV-WEATHER-3: Estacionalidad de Fourier y Coherencia Física ML
# ============================================================================

def test_inv_weather_3_fourier_seasonality_and_physical_coherence():
    """Valida que pred_min <= pred_media <= pred_max y valores finitos."""
    madrid_csv = DATOS_DIR / "Madrid.csv"
    assert madrid_csv.exists(), f"No se encontró {madrid_csv}"

    res = generar_prediccion_ia_ciudad(str(madrid_csv))
    assert res["registros"] >= 10
    p_min = res["min"]
    p_med = res["media"]
    p_max = res["max"]

    assert p_min is not None and p_med is not None and p_max is not None
    assert not math.isnan(p_min) and not math.isnan(p_med) and not math.isnan(p_max)
    # Coherencia física estricta
    assert p_min <= p_med <= p_max, f"Coherencia física violada: min={p_min}, med={p_med}, max={p_max}"

    metrics = res["model_metrics"]
    assert metrics is not None
    assert -1.0 <= metrics["r2_media"] <= 1.0
    assert metrics["mae_30d_c"] >= 0.0
    assert "seasonality_fourier" in metrics["top_features"]
    assert metrics["top_features"]["seasonality_fourier"] >= 0.0


def test_inv_weather_3_insufficient_records_graceful_handling():
    """Valida que con datos insuficientes (<10) devuelva None sin lanzar excepción."""
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(",".join(CABECERA_15_COLUMNAS) + "\n")
        tmp.write("2026-11-01T06:00:00,TestCity,15.0,14.0,10.0,20.0,50,10.0,cielo claro,40.0,-3.0,0,10000,0,0\n")
        tmp_path = tmp.name

    try:
        res = generar_prediccion_ia_ciudad(tmp_path)
        assert res["max"] is None
        assert res["min"] is None
        assert res["media"] is None
        assert res["registros"] < 10
        assert res["model_metrics"] is None
    finally:
        os.remove(tmp_path)


# ============================================================================
# 4. INV-WEATHER-4: Acotación de Confort (0..100) y global_summary.json
# ============================================================================

@pytest.mark.parametrize(
    "temp,feels,hum,wind,clouds,vis,rain,snow,expected_min,expected_max",
    [
        (21.0, 21.0, 50, 10.0, 20, 10000, 0.0, 0.0, 95, 100),   # Condiciones ideales
        (42.0, 48.0, 80, 30.0, 10, 10000, 0.0, 0.0, 0, 45),     # Calor extremo húmedo
        (-25.0, -32.0, 70, 45.0, 90, 2000, 0.0, 5.0, 0, 20),    # Frío polar con viento y nieve
        (18.0, 18.0, 55, 12.0, 30, 10000, 0.0, 0.0, 85, 100),   # Buen día templado
    ]
)
def test_inv_weather_4_comfort_index_bounds(
    temp, feels, hum, wind, clouds, vis, rain, snow, expected_min, expected_max
):
    """Valida que compute_comfort_index permanezca acotado entre 0 y 100 y reaccione a variables."""
    score = compute_comfort_index(
        temp_c=temp,
        feels_c=feels,
        humidity=hum,
        wind_kmh=wind,
        clouds=clouds,
        visibility_m=vis,
        rain_1h=rain,
        snow_1h=snow,
    )
    assert 0 <= score <= 100, f"Score fuera de rango: {score}"
    assert expected_min <= score <= expected_max, f"Score {score} fuera del intervalo esperado [{expected_min}, {expected_max}]"


def test_inv_weather_4_global_summary_integrity():
    """Valida la integridad y contratos de global_summary.json."""
    assert SUMMARY_FILE.exists(), f"No se encontró {SUMMARY_FILE}"

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        summary = json.load(f)

    assert summary["total_cities"] == 168
    assert summary["total_records"] > 30000

    extremes = summary["global_extremes"]
    required_extreme_keys = [
        "hottest", "coldest", "windiest", "wettest",
        "top_positive_anomaly", "top_negative_anomaly", "best_comfort"
    ]
    for k in required_extreme_keys:
        assert k in extremes, f"Falta clave {k} en global_extremes"
        assert extremes[k]["ciudad"] != "", f"Ciudad vacía en {k}"
        assert extremes[k]["val"] is not None, f"Valor nulo en {k}"

    cities = summary["cities"]
    assert len(cities) == 168

    regions_found = set()
    for c in cities:
        assert "ciudad" in c and "query" in c and "country" in c and "region" in c
        assert c["region"] in VALID_REGIONS, f"Región desconocida '{c['region']}' en {c['ciudad']}"
        regions_found.add(c["region"])

        stats = c["stats"]
        assert 0 <= stats["comfort_index"] <= 100
        assert stats["records"] > 0
        assert stats["best_hour_utc"] in (6, 14, 22)

    assert regions_found == VALID_REGIONS, f"No se encontraron todas las 6 regiones: {regions_found}"


# ============================================================================
# 5. Tests de infer_region y Reconstrucción Offline
# ============================================================================

def test_infer_region_coverage():
    """Valida la asignación regional para ciudades de las 6 zonas."""
    assert infer_region("Madrid,ES") == "spain"
    assert infer_region("Paris,FR") == "europe"
    assert infer_region("London,GB") == "europe"
    assert infer_region("Tokyo,JP") == "asia"
    assert infer_region("Bangkok,TH") == "asia"
    assert infer_region("Sydney,AU") == "oceania"
    assert infer_region("Auckland,NZ") == "oceania"
    assert infer_region("New York,US") == "americas"
    assert infer_region("Buenos Aires,AR") == "americas"
    assert infer_region("Cairo,EG") == "africa"
    assert infer_region("Nairobi,KE") == "africa"


def test_rebuild_offline_isolated_execution():
    """Valida rebuild_offline en un entorno temporal aislado."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        datos_tmp = tmp_path / "datos"
        datos_tmp.mkdir()

        # Crear ciudades.txt temporal
        ciudades_tmp = tmp_path / "ciudades.txt"
        ciudades_tmp.write_text("Madrid,ES,40.4168,-3.7038\nParis,FR,48.8566,2.3522\n", encoding="utf-8")

        # Crear dos CSVs sintéticos con 12 días cada uno
        for city_name, lat, lon in [("Madrid", "40.4168", "-3.7038"), ("Paris", "48.8566", "2.3522")]:
            csv_file = datos_tmp / f"{city_name}.csv"
            with open(csv_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(CABECERA_15_COLUMNAS)
                for day in range(1, 15):
                    writer.writerow([
                        f"2026-10-{day:02d}T14:00:00", city_name,
                        18.0 + (day % 3), 17.5, 12.0, 22.0, 55, 10.0,
                        "cielo claro", lat, lon, 10, 10000, 0.0, 0.0
                    ])

        pred_tmp = tmp_path / "predicciones.json"
        map_tmp = tmp_path / "city_locations.json"
        sum_tmp = tmp_path / "global_summary.json"

        preds, map_d, summary = rebuild_offline(
            datos_dir=str(datos_tmp),
            ciudades_file=str(ciudades_tmp),
            predicciones_file=str(pred_tmp),
            mapa_file=str(map_tmp),
            summary_file=str(sum_tmp),
        )

        assert len(preds) == 2
        assert len(map_d) == 2
        assert summary["total_cities"] == 2
        assert pred_tmp.exists() and map_tmp.exists() and sum_tmp.exists()


# ============================================================================
# 6. INV-WEATHER-5: Frontend Executive Cockpit, Tokens, Presets y Deep-Linking
# ============================================================================

def test_inv_weather_5_frontend_contracts_and_tokens():
    """Valida los contratos visuales, tokens CSS, vistas, presets y telemetría de index.html."""
    html_file = BASE_DIR / "index.html"
    assert html_file.exists(), f"No se encontró {html_file}"
    content = html_file.read_text(encoding="utf-8")

    # Tokens CSS canónicos
    assert "--bg-canvas: #0b0f17" in content, "Falta token --bg-canvas: #0b0f17"
    assert "--bg-surface: #111827" in content, "Falta token --bg-surface: #111827"
    assert "--bg-elevated: #1e293b" in content, "Falta token --bg-elevated: #1e293b"
    assert "tabular-nums" in content, "Falta font-variant-numeric: tabular-nums"

    # 3 Vistas
    for view in ("observatory", "arena", "atlas"):
        assert f'data-view="{view}"' in content, f"Falta selector para vista {view}"
        assert f'id="view-{view}"' in content, f"Falta contenedor para vista {view}"

    # 5 Presets en 1 clic
    for preset in ("spain", "global", "extremes", "ai_duel", "comfort"):
        assert f'data-preset="{preset}"' in content, f"Falta botón para preset {preset}"

    # 7 Métricas
    for metric in ("temp", "feels_like", "humidity", "wind", "clouds", "rain", "visibility"):
        assert f'value="{metric}"' in content, f"Falta radio de métrica {metric}"

    # 5 Capas de mapa
    for layer in ("temp", "comfort", "anomaly", "wind", "humidity"):
        assert f'value="{layer}"' in content, f"Falta opción de capa {layer}"

    # Deep-Linking y GA4
    assert "syncUrlParams" in content and "parseUrlParams" in content, "Falta motor de deep-linking URL"
    assert "emitWeatherEvent" in content and "gtag" in content, "Falta helper de telemetría GA4"
    assert "https://datalaria-app-weather.netlify.app/datos/" in content, "Falta fallback de datos Netlify"


def test_inv_weather_5_bilingual_parity_strict():
    """Valida paridad estricta al 100% de claves entre translations.es y translations.en."""
    import re
    import subprocess

    html_file = BASE_DIR / "index.html"
    content = html_file.read_text(encoding="utf-8")
    m = re.search(r"const translations = (\{[\s\S]*?\n\s*\});", content)
    assert m, "No se encontró el objeto translations en index.html"

    # Evaluar con node para garantizar parsing JS exacto
    node_script = f"const translations = {m.group(1)}; console.log(JSON.stringify({{ es: Object.keys(translations.es), en: Object.keys(translations.en) }}));"
    res = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    keys_data = json.loads(res.stdout)

    es_keys = set(keys_data["es"])
    en_keys = set(keys_data["en"])

    assert len(es_keys) >= 50, f"Se esperaban >= 50 claves en es, encontradas {len(es_keys)}"
    assert es_keys == en_keys, f"Disparidad de claves de traducción: {es_keys ^ en_keys}"


# ============================================================================
# 7. INV-WEATHER-6: Higiene y Firewall de /static/apps/weather/
# ============================================================================

def test_inv_weather_6_static_firewall_hygiene():
    """Valida cortafuegos de static/apps/weather/ (cero py, sql, env, git y cero csv en datos/)."""
    repo_root = BASE_DIR.parent.parent
    static_weather_dir = repo_root / "static" / "apps" / "weather"
    assert static_weather_dir.exists(), f"No se encontró {static_weather_dir}"

    for root, dirs, files in os.walk(static_weather_dir):
        for f in files:
            assert not f.endswith((".py", ".pyc", ".sql", ".env")), f"Archivo prohibido en static/: {f}"
        assert ".git" not in dirs, "Metadatos .git prohibidos en static/"

    datos_static = static_weather_dir / "datos"
    if datos_static.exists():
        csv_files = list(datos_static.glob("*.csv"))
        assert len(csv_files) == 0, f"static/apps/weather/datos/ debe estar vacío de CSVs, encontrados {len(csv_files)}"

    # Verificar sincronización de index.html
    static_index = static_weather_dir / "index.html"
    app_index = BASE_DIR / "index.html"
    assert static_index.exists(), "Falta static/apps/weather/index.html"
    assert static_index.read_text(encoding="utf-8") == app_index.read_text(encoding="utf-8"), "static/apps/weather/index.html no está sincronizado con apps/weather/index.html"


# ============================================================================
# 8. Hito 2.6: Fichas Públicas ES/EN, weather.yaml v2.0.0 y Sync Upstream
# ============================================================================

def test_weather_yaml_and_showcase_sheets_v2():
    """Valida que weather.yaml esté en v2.0.0, las fichas ES/EN tengan deep-links y sync_upstream pase."""
    import yaml
    from apps.weather.sync_upstream import verify_upstream_sync

    repo_root = BASE_DIR.parent.parent

    # 1. Validar data/apps/weather.yaml
    yaml_file = repo_root / "data" / "apps" / "weather.yaml"
    assert yaml_file.exists(), f"No se encontró {yaml_file}"
    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["current_version"] in ("v2.0.0", "v3.0.0-beta", "v3.0.0", "v3.1.0", "v3.2.0", "v3.3.0", "v3.3.1", "v3.3.2"), f"current_version inesperada: {data.get('current_version')}"
    assert data["app_url"] == "/apps/weather/"
    assert "preset=extremes" in data.get("demo_url", "")
    assert "view=arena" in data.get("demo_url", "")

    # Releases: primera entrada debe ser v2.0.0..v3.3.2
    releases = data.get("releases", [])
    assert len(releases) >= 4
    first_release = releases[0]
    assert first_release["version"] in ("v2.0.0", "v3.0.0", "v3.1.0", "v3.2.0", "v3.3.0", "v3.3.1", "v3.3.2")
    assert first_release["state"] in ("released", "pre-release")
    assert first_release["type"] in ("release", "patch")

    # 2. Validar fichas content/es/apps/weather/ y content/en/apps/weather/
    es_sheet = repo_root / "content" / "es" / "apps" / "weather" / "index.md"
    en_sheet = repo_root / "content" / "en" / "apps" / "weather" / "index.md"
    assert es_sheet.exists() and en_sheet.exists()

    es_content = es_sheet.read_text(encoding="utf-8")
    en_content = en_sheet.read_text(encoding="utf-8")

    for c in (es_content, en_content):
        assert "?preset=spain" in c
        assert "?preset=global" in c
        assert "?preset=extremes" in c
        assert "?preset=ai_duel&view=arena" in c
        assert "?preset=comfort&view=atlas" in c
        assert "168" in c
        assert "Fourier" in c

    # 3. Validar sync_upstream.py
    ok, issues = verify_upstream_sync(BASE_DIR)
    assert ok, f"sync_upstream falló con issues: {issues}"
