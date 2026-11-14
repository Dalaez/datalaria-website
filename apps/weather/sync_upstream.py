# -*- coding: utf-8 -*-
"""Sincronizador y verificador de artefactos upstream para Weather Service v3.0 (Dalaez/app_weather)."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import urllib.request
import urllib.error

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

REQUIRED_ROOT_FILES = [
    "index.html",
    "embed.html",
    "manifest.json",
    "sw.js",
    "icon.svg",
    "icon-192.png",
    "icon-512.png",
    "icon-maskable-192.png",
    "icon-maskable-512.png",
    "apple-touch-icon.png",
    "datalaria_logo_transp.png",
    "read_weather.py",
    "build_derived.py",
    "_headers",
    "requirements.txt",
    "ciudades.txt",
    "predicciones.json",
    "city_locations.json",
    "global_summary.json",
    "README.md",
    ".github/workflows/actualizar-clima.yml"
]

REMOTE_BASE_URL = "https://datalaria-app-weather.netlify.app"


def verify_upstream_sync(app_dir: Path | None = None) -> tuple[bool, list[str]]:
    """Verifica que todos los artefactos canónicos existen y cumplen sus contratos."""
    if app_dir is None:
        app_dir = BASE_DIR

    issues: list[str] = []

    for rel_path in REQUIRED_ROOT_FILES:
        target = app_dir / rel_path
        if not target.exists():
            issues.append(f"Falta archivo requerido: {rel_path}")

    # Verificar que global_summary.json es válido
    summary_file = app_dir / "global_summary.json"
    if summary_file.exists():
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or "cities" not in data or len(data["cities"]) < 100:
                issues.append("global_summary.json no contiene al menos 100 ciudades válidas.")
        except Exception as e:
            issues.append(f"global_summary.json corrupto: {e}")

    # Verificar que predicciones.json contiene model_metrics o pred_ia
    pred_file = app_dir / "predicciones.json"
    if pred_file.exists():
        try:
            with open(pred_file, "r", encoding="utf-8") as f:
                preds = json.load(f)
            sample_city = next(iter(preds.values()), {})
            if "model_metrics" not in sample_city and "pred_ia" not in sample_city:
                issues.append("predicciones.json no contiene la estructura esperada.")
        except Exception as e:
            issues.append(f"predicciones.json corrupto: {e}")

    # Verificar derived/*.json agregados (W3.4 / W3.5 / W3.6)
    for fname in ["index.json", "climatology.json", "insights.json", "scorecard.json", "weekly_extremes.json"]:
        d_file = app_dir / "derived" / fname
        if not d_file.exists():
            issues.append(f"derived/{fname} no existe.")
    clim_file = app_dir / "derived" / "climatology.json"
    if clim_file.exists():
        try:
            with open(clim_file, "r", encoding="utf-8") as cf:
                clim_data = json.load(cf)
            if "feature_stats" not in clim_data:
                issues.append("derived/climatology.json no contiene feature_stats (W3.5).")
        except Exception as e:
            issues.append(f"derived/climatology.json corrupto: {e}")

    weekly_file = app_dir / "derived" / "weekly_extremes.json"
    if weekly_file.exists():
        try:
            with open(weekly_file, "r", encoding="utf-8") as wf:
                weekly_data = json.load(wf)
            for req_key in ("window", "hottest", "coldest", "wettest", "scriba_ready_snippets"):
                if req_key not in weekly_data:
                    issues.append(f"derived/weekly_extremes.json no contiene '{req_key}' (W3.6).")
        except Exception as e:
            issues.append(f"derived/weekly_extremes.json corrupto: {e}")

    headers_file = app_dir / "_headers"
    if headers_file.exists():
        try:
            headers_txt = headers_file.read_text(encoding="utf-8")
            if "/embed.html" not in headers_txt or "frame-ancestors" not in headers_txt:
                issues.append("_headers no incluye regla /embed.html con frame-ancestors (W3.6).")
        except Exception as e:
            issues.append(f"Error leyendo _headers: {e}")

    # Verificar datos/ con CSVs
    datos_dir = app_dir / "datos"
    if not datos_dir.exists() or len(list(datos_dir.glob("*.csv"))) < 10:
        issues.append("datos/ no contiene al menos 10 archivos CSV.")

    return len(issues) == 0, issues


def export_to_upstream(app_dir: Path, target_dir: Path, sync_hugo_catalog: bool = False) -> int:
    """Exporta el árbol limpio hacia el clon local de Dalaez/app_weather."""
    ok, issues = verify_upstream_sync(app_dir)
    if not ok:
        print("Error de verificación antes de exportar:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)

    # Copiar archivos raíz requeridos
    for rel_path in REQUIRED_ROOT_FILES:
        src = app_dir / rel_path
        dst = target_dir / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copiado: {rel_path}")

    # Copiar datos/*.csv si existen
    datos_dir = app_dir / "datos"
    if datos_dir.exists():
        datos_dst = target_dir / "datos"
        datos_dst.mkdir(parents=True, exist_ok=True)
        csv_count = 0
        for csv_file in datos_dir.glob("*.csv"):
            target_csv = datos_dst / csv_file.name
            if not target_csv.exists():
                shutil.copy2(csv_file, target_csv)
                csv_count += 1
        print(f"Copiados {csv_count} archivos CSV en datos/")

    # Copiar carpeta derived/
    derived_src = app_dir / "derived"
    if derived_src.exists():
        derived_dst = target_dir / "derived"
        shutil.copytree(derived_src, derived_dst, dirs_exist_ok=True)
        print(f"Copiada carpeta derived/ hacia {derived_dst}")

    # Si target_dir/datos tiene CSVs, asegurar derivados al 100%
    target_datos = target_dir / "datos"
    if target_datos.exists() and len(list(target_datos.glob("*.csv"))) >= 50:
        import subprocess
        build_script = app_dir / "build_derived.py"
        if build_script.exists():
            print("Ejecutando build_derived.py sobre target_dir/datos...")
            cmd = [
                sys.executable,
                str(build_script),
                "--source", str(target_datos),
                "--out", str(target_dir / "derived"),
                "--month-log"
            ]
            if (target_dir / "ciudades.txt").exists():
                cmd.extend(["--ciudades", str(target_dir / "ciudades.txt")])
            if (target_dir / "predicciones.json").exists():
                cmd.extend(["--predicciones", str(target_dir / "predicciones.json")])
            if sync_hugo_catalog:
                catalog_dst = BASE_DIR.parents[1] / "data" / "weather" / "cities_catalog.json"
                cmd.extend(["--hugo-catalog", str(catalog_dst)])
            subprocess.run(cmd, check=True)
            print("Derivados generados en target_dir/derived con éxito.")

    # Sincronizar también hacia static/apps/weather para paridad total con Hugo
    static_weather_dir = BASE_DIR.parents[1] / "static" / "apps" / "weather"
    if static_weather_dir.exists():
        for rel in [
            "index.html",
            "embed.html",
            "manifest.json",
            "sw.js",
            "_headers",
            "icon.svg",
            "icon-192.png",
            "icon-512.png",
            "icon-maskable-192.png",
            "icon-maskable-512.png",
            "apple-touch-icon.png",
        ]:
            if (app_dir / rel).exists():
                shutil.copy2(app_dir / rel, static_weather_dir / rel)
        # INV-WEATHER-6: En static/apps/weather solo copiar los agregados JSON (nunca daily/ ni CSVs)
        app_derived = BASE_DIR / "derived"
        app_derived.mkdir(parents=True, exist_ok=True)
        static_derived = static_weather_dir / "derived"
        static_derived.mkdir(parents=True, exist_ok=True)
        for d_file in ["index.json", "climatology.json", "insights.json", "scorecard.json", "weekly_extremes.json"]:
            src_f = target_dir / "derived" / d_file
            if src_f.exists():
                if target_dir.resolve() != BASE_DIR.resolve():
                    shutil.copy2(src_f, app_derived / d_file)
                shutil.copy2(src_f, static_derived / d_file)
        # Asegurar que daily no existe en static
        if (static_derived / "daily").exists():
            shutil.rmtree(static_derived / "daily", ignore_errors=True)
        print("Sincronizado también hacia static/apps/weather.")

    # Evitar copias obsoletas en public/apps/weather/ que puedan ocultar static/ al previsualizar en local
    public_weather_dir = BASE_DIR.parents[1] / "public" / "apps" / "weather"
    if public_weather_dir.exists():
        shutil.rmtree(public_weather_dir, ignore_errors=True)
        print("Limpiado artefacto obsoleto public/apps/weather/.")

    print(f"\n✅ Exportación upstream completada con éxito en: {target_dir}")
    return 0


def pull_from_remote(app_dir: Path, cities: list[str] | None = None, with_daily: bool = False) -> int:
    """Descarga de Netlify los resúmenes y derivados JSON compactos hacia apps/weather/derived/."""
    derived_dir = app_dir / "derived"
    derived_dir.mkdir(parents=True, exist_ok=True)

    files_to_pull = [
        ("derived/index.json", derived_dir / "index.json"),
        ("derived/climatology.json", derived_dir / "climatology.json"),
        ("derived/insights.json", derived_dir / "insights.json"),
        ("derived/scorecard.json", derived_dir / "scorecard.json"),
        ("derived/weekly_extremes.json", derived_dir / "weekly_extremes.json"),
        ("global_summary.json", app_dir / "global_summary.json"),
        ("predicciones.json", app_dir / "predicciones.json"),
        ("city_locations.json", app_dir / "city_locations.json")
    ]

    print(f"Descargando metadatos y resúmenes desde {REMOTE_BASE_URL}...")
    pulled_count = 0
    for remote_rel, local_path in files_to_pull:
        url = f"{REMOTE_BASE_URL}/{remote_rel}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Datalaria-Sync/3.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                content = resp.read()
                local_path.parent.mkdir(parents=True, exist_ok=True)
                with open(local_path, "wb") as f:
                    f.write(content)
                print(f"  ✓ {remote_rel} ({len(content)} bytes)")
                pulled_count += 1
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  - {remote_rel}: No publicado aún en remoto (HTTP 404, fallback local activo).")
            else:
                print(f"  ! {remote_rel}: Error HTTP {e.code}")
        except Exception as e:
            print(f"  ! {remote_rel}: Error de conexión: {e}")

    # Descarga selectiva de daily si se solicita
    if cities:
        daily_dir = derived_dir / "daily"
        daily_dir.mkdir(parents=True, exist_ok=True)
        for city_slug in cities:
            slug_clean = city_slug.lower().strip()
            remote_rel = f"derived/daily/{slug_clean}.json"
            url = f"{REMOTE_BASE_URL}/{remote_rel}"
            local_path = daily_dir / f"{slug_clean}.json"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Datalaria-Sync/3.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    content = resp.read()
                    with open(local_path, "wb") as f:
                        f.write(content)
                    print(f"  ✓ {remote_rel} ({len(content)} bytes)")
                    pulled_count += 1
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"  - {remote_rel}: No encontrado en remoto (HTTP 404).")
                else:
                    print(f"  ! {remote_rel}: HTTP {e.code}")
            except Exception as e:
                print(f"  ! {remote_rel}: Error: {e}")

    print(f"Sincronización --pull finalizada: {pulled_count} ficheros actualizados.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verificador y sincronizador upstream para Weather Service v3.0.")
    parser.add_argument("--check", action="store_true", help="Verifica la integridad de los archivos canónicos.")
    parser.add_argument("--target", "--export-dir", dest="export_dir", type=str, help="Directorio destino hacia donde exportar los archivos para git push.")
    parser.add_argument("--pull", action="store_true", help="Descarga resúmenes compactos desde producción (Netlify).")
    parser.add_argument("--cities", type=str, default=None, help="Lista separada por comas de ciudades/slugs para --pull.")
    parser.add_argument("--with-daily", action="store_true", help="Descarga series daily para las ciudades especificadas.")
    parser.add_argument("--sync-hugo-catalog", action="store_true", help="Actualiza data/weather/cities_catalog.json al exportar.")

    args = parser.parse_args()

    if args.pull:
        cities_list = [c.strip() for c in args.cities.split(",")] if args.cities else None
        return pull_from_remote(BASE_DIR, cities=cities_list, with_daily=args.with_daily)

    if args.export_dir:
        return export_to_upstream(BASE_DIR, Path(args.export_dir), sync_hugo_catalog=args.sync_hugo_catalog)

    # Por defecto --check
    ok, issues = verify_upstream_sync()
    if ok:
        print("OK: Todos los artefactos canónicos de Weather Service v3.0 están presentes y válidos para upstream.")
        return 0
    else:
        print("FALLO: Se encontraron discrepancias en los artefactos:")
        for issue in issues:
            print(f"  - {issue}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
