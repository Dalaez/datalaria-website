# -*- coding: utf-8 -*-
"""ops/obs_kit/build_kit.py — Factoría determinista B2B y Gobernanza de Embargo para pack-obs.

Producto: IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit (id: pack-obs · 19 € Early-Bird / PVP 39 €).
Fecha programada de estreno: Miércoles 2026-12-09.

Uso:
  python -m ops.obs_kit.build_kit                  # Construye Excel, PDF, Previews, Portadas, ZIP y SHA-256
  python -m ops.obs_kit.build_kit --verify-embargo # Verifica embargo comercial previo al 2026-12-09 e integridad
  python -m ops.obs_kit.build_kit --activate --checkout-url <URL>  # Activa pack-obs en kits.yaml el Día D
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

from ops.obs_kit.excel_builder import BOM_SAMPLE_ROWS, build_excel_workbook
from ops.obs_kit.pdf_builder import build_pdf_playbook
from ops.obs_kit.visuals_builder import build_composite_preview_1600x980, build_store_cover

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG_DIR = REPO_ROOT / "packages" / "obs_kit"
DIST_DIR = REPO_ROOT / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY"
RECURSOS_IMG_DIR = REPO_ROOT / "static" / "images" / "recursos"
API_DIR = REPO_ROOT / "apps" / "obs-management" / "api"
KITS_YAML = REPO_ROOT / "data" / "pulse" / "kits.yaml"

ZIP_NAME = "Datalaria_IEC62402_Obsolescence_LTB_Kit_Dual.zip"
PKG_ZIP = PKG_DIR / ZIP_NAME
DIST_ZIP = DIST_DIR / ZIP_NAME
MANIFEST_JSON = PKG_DIR / "SHA256_MANIFEST.json"

RELEASE_DATE = "2026-12-09"


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_compatible_bom_csv() -> str:
    """Genera plantilla CSV industrial 100% compatible con el parser de Agentic Radar v2.0."""
    lines = [
        "End_Product_SKU,End_Product_Margin,Assembly_PN,Component_PN,Quantity_per_Assembly,Manufacturer,Manufacturer_PN,Lifecycle"
    ]
    for row in BOM_SAMPLE_ROWS:
        annual_margin = round(float(row["demand"]) * float(row["margin"]), 2)
        lines.append(
            f"{row['sku']},{annual_margin:.2f},{row['sub']},{row['ipn']},{row['qty']},{row['mfg']},{row['mpn']},{row['status']}"
        )
    return "\n".join(lines) + "\n"


def _root_readme() -> str:
    return """# Datalaria · IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit (Dual ES/EN · v2.0.0)

Gracias por adquirir el **IEC 62402 Obsolescence, BOM Risk & Last Time Buy (LTB) Decision Kit**.
Thank you for purchasing the **IEC 62402 Obsolescence, BOM Risk & Last Time Buy (LTB) Decision Kit**.

## Estructura Numerada del Paquete / Package Structure

- `01_EXCEL_MOTOR_BOM_LTB/`
  - `ES/IEC62402_Obsolescencia_BOM_LTB_ES.xlsx` (5 hojas, 0 macros VBA, tablas nativas y gráfico C-Level)
  - `EN/IEC62402_Obsolescence_BOM_LTB_EN.xlsx` (5 sheets, 0 VBA macros, native tables & C-Level chart)
- `02_PLAYBOOK_EJECUTIVO_PDF/`
  - `ES/Playbook_Ejecutivo_IEC62402_LTB_ES.pdf` (Guía vectorial A4 · 5 páginas)
  - `EN/Executive_Playbook_IEC62402_LTB_EN.pdf` (A4 vector executive guide · 5 pages)
- `03_STARTER_BLUEPRINT_TECNICO/`
  - `obs_radar_supabase_schema.sql` (Esquema multi-tenant `obs_radar` con Row-Level Security en 6 tablas)
  - `bom_engine.py` + `models.py` (Motor determinista DAG multinivel anti-ciclos y contratos Pydantic v2)
  - `env.example` (Plantilla segura de variables de entorno sin secretos)
  - `datalaria_bom_industrial_template.csv` (Plantilla BOM importable en 1 clic en https://datalaria.com/apps/obs-management/)
- `SHA256_MANIFEST.txt` — Huellas criptográficas de integridad de todos los entregables.
- `LICENSE.txt` — Licencia comercial B2B interna para equipos de operaciones e ingeniería.

## Diferencia y Complemento con `pack-stock` (Calculadora Stock de Seguridad & ROP)
- **`pack-stock` (APICS / ASCM):** Gobierna compras recurrentes mientras el proveedor está **Activo** (Madurez).
- **`pack-obs` (IEC 62402):** Toma el relevo en el momento en que llega un aviso **PCN/PDN/EOL** (el proveedor cierra la línea): congela el ROP automático, cuantifica el margen P&L expuesto en el BOM y resuelve la decisión **Last Time Buy (LTB) vs. Rediseño FFF (NRE)**.
"""


def _license_txt() -> str:
    return """DATALARIA COMMERCIAL B2B SINGLE-TEAM LICENSE
Product: IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit (v2.0.0)
Copyright (c) 2026 Datalaria (https://datalaria.com)

GRANT OF LICENSE:
You are granted a perpetual, non-exclusive, non-transferable license to use, modify, and deploy
the included Excel workbooks, PDF playbooks, SQL schemas, and Python modules for internal
business operations within your organization or direct client consulting engagements.

RESTRICTIONS:
Redistribution, resale, sublicensing, or public re-upload of the original kit archive or templates
as a competing digital product is strictly prohibited.
"""


def _blueprint_readme() -> str:
    return """# 03 · Starter Blueprint Técnico (`obs_radar` PostgreSQL RLS + `bom_engine.py`)

1. **Importación inmediata sin servidor:** Carga `datalaria_bom_industrial_template.csv` en
   https://datalaria.com/apps/obs-management/ (el análisis se ejecuta 100 % localmente en tu navegador).
2. **Despliegue PostgreSQL / Supabase:** Ejecuta `obs_radar_supabase_schema.sql` para crear el esquema
   aislado `obs_radar` con políticas `ROW LEVEL SECURITY (auth.uid() = user_id)` en las 6 tablas.
3. **Motor Determinista Python:** Integra `bom_engine.py` y `models.py` en tu servidor FastAPI o CI/CD
   para calcular criticidad IEC 62402 y veredicto LTB vs. FFF sin dependencia de LLMs.
4. **Variables de Entorno:** Copia `env.example` a `.env` y completa tus credenciales privadas localmente.
"""


def build_all() -> dict[str, str]:
    """Ejecuta la factoría completa y devuelve el mapa de artefactos generados con sus SHA-256."""
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    staging = PKG_DIR / "_staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    # 1. Excel Dual ES / EN (5 hojas exactas, 0 VBA)
    xlsx_es = build_excel_workbook("es", staging / "01_EXCEL_MOTOR_BOM_LTB" / "ES" / "IEC62402_Obsolescencia_BOM_LTB_ES.xlsx")
    xlsx_en = build_excel_workbook("en", staging / "01_EXCEL_MOTOR_BOM_LTB" / "EN" / "IEC62402_Obsolescence_BOM_LTB_EN.xlsx")
    print(f"[1/5] Excel Dual generado: {xlsx_es.name}, {xlsx_en.name}")

    # 2. Playbooks PDF Vectoriales A4 (5 páginas exactas ES / EN)
    pdf_es = build_pdf_playbook("es", staging / "02_PLAYBOOK_EJECUTIVO_PDF" / "ES" / "Playbook_Ejecutivo_IEC62402_LTB_ES.pdf")
    pdf_en = build_pdf_playbook("en", staging / "02_PLAYBOOK_EJECUTIVO_PDF" / "EN" / "Executive_Playbook_IEC62402_LTB_EN.pdf")
    # Copias directas en packages/obs_kit/ para auditoría rápida
    shutil.copy2(pdf_es, PKG_DIR / pdf_es.name)
    shutil.copy2(pdf_en, PKG_DIR / pdf_en.name)
    print(f"[2/5] Playbooks PDF A4 (5 págs) generados: {pdf_es.name}, {pdf_en.name}")

    # 3. Starter Blueprint Técnico (desde apps/obs-management/api/, 0 secretos reales)
    bp_dir = staging / "03_STARTER_BLUEPRINT_TECNICO"
    bp_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(API_DIR / "supabase_schema.sql", bp_dir / "obs_radar_supabase_schema.sql")
    shutil.copy2(API_DIR / "bom_engine.py", bp_dir / "bom_engine.py")
    shutil.copy2(API_DIR / "models.py", bp_dir / "models.py")
    shutil.copy2(API_DIR / ".env.example", bp_dir / "env.example")
    (bp_dir / "datalaria_bom_industrial_template.csv").write_text(_build_compatible_bom_csv(), encoding="utf-8")
    (bp_dir / "README_BLUEPRINT.md").write_text(_blueprint_readme(), encoding="utf-8")

    (staging / "README.md").write_text(_root_readme(), encoding="utf-8")
    (staging / "LICENSE.txt").write_text(_license_txt(), encoding="utf-8")
    print("[3/5] Starter Blueprint Técnico empaquetado (SQL RLS + bom_engine.py + CSV compatible).")

    # 4. Previews Compuestas 1600x980 y Portadas de Tienda 1200x750 / 1200x630 / 1080x1080
    cover_es_src = REPO_ROOT / "content" / "es" / "apps" / "obs-management" / "cover.png"
    cover_en_src = REPO_ROOT / "content" / "en" / "apps" / "obs-management" / "cover.png"

    prev_es = build_composite_preview_1600x980("es", pdf_es, cover_es_src, RECURSOS_IMG_DIR / "obs-preview-es.png")
    prev_en = build_composite_preview_1600x980("en", pdf_en, cover_en_src, RECURSOS_IMG_DIR / "obs-preview-en.png")

    cov_1200_750_es = build_store_cover(
        "es", 1200, 750, pdf_es, cover_es_src, DIST_DIR / "Images" / "Obsolescence_IEC62402_Cover_1200x750_ES.png"
    )
    cov_1200_750_en = build_store_cover(
        "en", 1200, 750, pdf_en, cover_en_src, DIST_DIR / "Images" / "Obsolescence_IEC62402_Cover_1200x750_EN.png"
    )
    cov_1200_630 = build_store_cover(
        "en", 1200, 630, pdf_en, cover_en_src, DIST_DIR / "Images" / "Obsolescence_IEC62402.png"
    )
    cov_1080_sq = build_store_cover(
        "en", 1080, 1080, pdf_en, cover_en_src, DIST_DIR / "Images_Square" / "Obsolescence_IEC62402.png"
    )
    print(f"[4/5] Visuales generados: {prev_es.name}, {prev_en.name}, {cov_1200_750_es.name}, {cov_1200_750_en.name}.")

    # 5. Manifiesto SHA-256 interno + ZIP Numerado sincronizado a packages/obs_kit/ y packages/00_DISTRIBUCION_LEMONSQUEEZY/
    file_hashes: dict[str, str] = {}
    staged_files = sorted(p for p in staging.rglob("*") if p.is_file())
    for fp in staged_files:
        rel = fp.relative_to(staging).as_posix()
        file_hashes[rel] = _sha256_file(fp)

    manifest_lines = [
        f"# SHA-256 INTEGRITY MANIFEST — {ZIP_NAME}",
        f"# Generated UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
    ]
    for rel, digest in file_hashes.items():
        manifest_lines.append(f"{digest}  {rel}")
    (staging / "SHA256_MANIFEST.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    with zipfile.ZipFile(PKG_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for fp in sorted(p for p in staging.rglob("*") if p.is_file()):
            rel = fp.relative_to(staging).as_posix()
            zf.write(fp, arcname=rel)

    # Validar integridad del ZIP
    with zipfile.ZipFile(PKG_ZIP, "r") as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP corrupto en entrada: {bad}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PKG_ZIP, DIST_ZIP)

    zip_sha = _sha256_file(PKG_ZIP)
    external_manifest = {
        "kit_id": "pack-obs",
        "version": "v2.0.0",
        "release_date": RELEASE_DATE,
        "zip_name": ZIP_NAME,
        "zip_sha256": zip_sha,
        "zip_size_bytes": PKG_ZIP.stat().st_size,
        "files": file_hashes,
        "visuals": {
            "preview_es": _sha256_file(prev_es),
            "preview_en": _sha256_file(prev_en),
            "cover_1200x750_es": _sha256_file(cov_1200_750_es),
            "cover_1200x750_en": _sha256_file(cov_1200_750_en),
            "cover_1200x630": _sha256_file(cov_1200_630),
            "cover_1080x1080": _sha256_file(cov_1080_sq),
        },
    }
    MANIFEST_JSON.write_text(json.dumps(external_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    shutil.rmtree(staging)

    print(f"[5/5] ZIP numerado y sincronizado: {PKG_ZIP.name} ({PKG_ZIP.stat().st_size:,} B · SHA256 {zip_sha[:12]}...).")
    return file_hashes


def verify_embargo() -> int:
    """Verifica determinísticamente el estado de embargo comercial previo al 2026-12-09 e integridad de artefactos."""
    errors: list[str] = []

    required = [
        PKG_ZIP,
        DIST_ZIP,
        MANIFEST_JSON,
        RECURSOS_IMG_DIR / "obs-preview-es.png",
        RECURSOS_IMG_DIR / "obs-preview-en.png",
        DIST_DIR / "Images" / "Obsolescence_IEC62402_Cover_1200x750_ES.png",
        DIST_DIR / "Images" / "Obsolescence_IEC62402_Cover_1200x750_EN.png",
        DIST_DIR / "Images" / "Obsolescence_IEC62402.png",
        DIST_DIR / "Images_Square" / "Obsolescence_IEC62402.png",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"Falta artefacto obligatorio: {p}")

    if PKG_ZIP.exists() and DIST_ZIP.exists():
        if _sha256_file(PKG_ZIP) != _sha256_file(DIST_ZIP):
            errors.append("Desincronización SHA-256 entre packages/obs_kit/ y packages/00_DISTRIBUCION_LEMONSQUEEZY/.")
        with zipfile.ZipFile(PKG_ZIP, "r") as zf:
            if zf.testzip() is not None:
                errors.append("Integridad ZIP fallida.")
            names = zf.namelist()
            for n in names:
                if "private/" in n or n.endswith(".env"):
                    errors.append(f"Fuga de archivo privado o .env dentro del ZIP: {n}")

    # Verificar registro en data/pulse/kits.yaml
    if not KITS_YAML.exists():
        errors.append("No existe data/pulse/kits.yaml")
    else:
        data = yaml.safe_load(KITS_YAML.read_text(encoding="utf-8"))
        kits = data.get("kits", [])
        obs_kit = next((k for k in kits if k.get("id") == "pack-obs"), None)
        if not obs_kit:
            errors.append("Falta entrada 'pack-obs' en data/pulse/kits.yaml")
        else:
            if obs_kit.get("status") != "coming":
                errors.append(f"Embargo violado: pack-obs debe estar en status 'coming' antes del {RELEASE_DATE}, hallado: {obs_kit.get('status')}")
            if str(obs_kit.get("publish_date")) != RELEASE_DATE:
                errors.append(f"publish_date esperado '{RELEASE_DATE}', hallado: {obs_kit.get('publish_date')}")
            if obs_kit.get("price") != "19€":
                errors.append(f"Precio esperado '19€', hallado: {obs_kit.get('price')}")

    # Verificar cero mailto: en static/apps/obs-management/
    static_obs = REPO_ROOT / "static" / "apps" / "obs-management"
    for f in static_obs.glob("*"):
        if f.is_file() and f.suffix in (".html", ".js"):
            if "mailto:" in f.read_text(encoding="utf-8").lower():
                errors.append(f"Violación INV-HELIX-WL-4: mailto: detectado en {f.name}")

    if errors:
        print("EMBARGO_FAIL:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"EMBARGO_PASS: pack-obs verificado en modo coming para {RELEASE_DATE} con 100% de artefactos y SHA-256 sincronizados.")
    return 0


def activate_launch(checkout_url: str) -> int:
    """Descongela pack-obs en data/pulse/kits.yaml el Día D (2026-12-09) inyectando el checkout ?embed=1."""
    if not checkout_url.startswith("https://datalaria.lemonsqueezy.com/checkout/buy/"):
        print("ERROR: checkout_url debe ser una URL válida de Lemon Squeezy.")
        return 1
    if "?embed=1" not in checkout_url:
        checkout_url = f"{checkout_url}?embed=1"

    raw = KITS_YAML.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    updated = False
    for k in data.get("kits", []):
        if k.get("id") == "pack-obs":
            k["status"] = "available"
            k["checkout_url"] = checkout_url
            updated = True
            break
    if not updated:
        print("ERROR: No se encontró 'pack-obs' en data/pulse/kits.yaml.")
        return 1

    KITS_YAML.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"OK --activate: pack-obs activado en data/pulse/kits.yaml con checkout {checkout_url}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Datalaria B2B Kit Factory para pack-obs (IEC 62402 & LTB).")
    parser.add_argument("--verify-embargo", action="store_true", help="Valida embargo comercial e integridad SHA-256.")
    parser.add_argument("--activate", action="store_true", help="Activa pack-obs en kits.yaml el día del lanzamiento.")
    parser.add_argument("--checkout-url", type=str, default="", help="URL de Lemon Squeezy para --activate.")
    args = parser.parse_args()

    if args.verify_embargo:
        return verify_embargo()
    if args.activate:
        return activate_launch(args.checkout_url)

    build_all()
    return 0


if __name__ == "__main__":
    sys.exit(main())
