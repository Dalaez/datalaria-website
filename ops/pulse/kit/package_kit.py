"""
ops/pulse/kit/package_kit.py
----------------------------
Empaquetador Automatizado del Kit Comercial Dual de Datalaria Pulse (v1.0.0).
Especificación: Hito P-LAUNCH-3C (specs/apps/pulse/spec.md).

Genera el artefacto comercial final: packages/pulse/Datalaria_Pulse_Kit.zip
organizado en una estructura Dual completa:
  - Raíz: guías de bienvenida bilingües y licencias comerciales
  - ES/: árbol completo en español (01_Excel_Templates, 02_Migration_Scripts, 03_Documentation)
  - EN/: árbol completo en inglés (01_Excel_Templates, 02_Migration_Scripts, 03_Documentation)
  - Carpetas legadas 01_, 02_, 03_ para retrocompatibilidad total
Y lo sincroniza automáticamente en packages/00_DISTRIBUCION_LEMONSQUEEZY/.
"""

import os
import sys
import shutil
import zipfile
import hashlib
from pathlib import Path
from typing import List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

PACKAGES_DIR = ROOT_DIR / "packages" / "pulse"
OPS_PULSE_DIR = ROOT_DIR / "ops" / "pulse"
LEMON_DIST_DIR = ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY"
ZIP_OUTPUT_PATH = PACKAGES_DIR / "Datalaria_Pulse_Kit.zip"

from ops.pulse.kit.build_pulse_kit import build_pulse_excel
from ops.pulse.kit.build_pdf_guide import build_pulse_pdf_guide, build_executive_pdf_guide


def compute_sha256(file_path: Path) -> str:
    """Calcula el hash SHA-256 de un archivo binario."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def package_kit() -> Path:
    """Compila y empaqueta el kit descargable comercial en formato ZIP Dual ES/EN."""
    print("[KIT BUILD] Compilando plantillas maestras de Excel (ES & EN)...")
    excel_es = build_pulse_excel(is_template=True, lang="es")
    excel_en = build_pulse_excel(is_template=True, lang="en")
    excel_legacy = PACKAGES_DIR / "Pulse_Content_Ops_Template.xlsx"

    print("[KIT BUILD] Compilando guías ejecutivas maquetadas en PDF (ES & EN)...")
    pdf_es = build_executive_pdf_guide(PACKAGES_DIR / "GUIA_EJECUTIVA_PULSE_ES.pdf", lang="es")
    pdf_en = build_executive_pdf_guide(PACKAGES_DIR / "PULSE_EXECUTIVE_GUIDE_EN.pdf", lang="en")
    pdf_legacy = PACKAGES_DIR / "GUIA_EJECUTIVA_PULSE.pdf"
    if not pdf_legacy.exists():
        shutil.copy2(pdf_es, pdf_legacy)

    # Archivos a incluir en el ZIP comercial Dual ES/EN
    files_to_pack: List[Tuple[Path, str]] = [
        # --- RAÍZ DEL ENTREGABLE BILINGÜE ---
        (PACKAGES_DIR / "00_EMPIEZA_AQUI_ES.md", "00_EMPIEZA_AQUI_ES.md"),
        (PACKAGES_DIR / "00_START_HERE_EN.md", "00_START_HERE_EN.md"),
        (PACKAGES_DIR / "LICENSE_ES.txt", "LICENSE_ES.txt"),
        (PACKAGES_DIR / "LICENSE_EN.txt", "LICENSE_EN.txt"),
        # Archivos de conveniencia / retrocompatibilidad en raíz
        (PACKAGES_DIR / "00_EMPIEZA_AQUI_README.md", "00_EMPIEZA_AQUI_README.md"),
        (pdf_legacy, "GUIA_EJECUTIVA_PULSE.pdf"),
        (PACKAGES_DIR / "LICENSE.txt", "LICENSE.txt"),

        # --- EDICIÓN EN ESPAÑOL (ES/) ---
        (PACKAGES_DIR / "00_EMPIEZA_AQUI_README.md", "ES/00_EMPIEZA_AQUI_README.md"),
        (pdf_es, "ES/GUIA_EJECUTIVA_PULSE_ES.pdf"),
        # ES/01_Excel_Templates
        (excel_es, "ES/01_Excel_Templates/Pulse_Content_Ops_Template_ES.xlsx"),
        (PACKAGES_DIR / "notion_power_query_es.m", "ES/01_Excel_Templates/notion_power_query_es.m"),
        (PACKAGES_DIR / "git_public_json_power_query_es.m", "ES/01_Excel_Templates/git_public_json_power_query_es.m"),
        # ES/02_Migration_Scripts
        (OPS_PULSE_DIR / "migrate_notion.py", "ES/02_Migration_Scripts/migrate_notion.py"),
        (PACKAGES_DIR / "pulse_repo_scanner.py", "ES/02_Migration_Scripts/pulse_repo_scanner.py"),
        (PACKAGES_DIR / "sample_notion_export_es.csv", "ES/02_Migration_Scripts/sample_notion_export_es.csv"),
        # ES/03_Documentation
        (pdf_es, "ES/03_Documentation/GUIA_EJECUTIVA_PULSE_ES.pdf"),
        (PACKAGES_DIR / "GUIA_PULSE_KIT_ES.md", "ES/03_Documentation/GUIA_PULSE_KIT_ES.md"),
        (PACKAGES_DIR / "ESPECIFICACION_CAMPOS_ES.md", "ES/03_Documentation/ESPECIFICACION_CAMPOS_ES.md"),

        # --- ENGLISH EDITION (EN/) ---
        (PACKAGES_DIR / "00_START_HERE_README.md", "EN/00_START_HERE_README.md"),
        (pdf_en, "EN/PULSE_EXECUTIVE_GUIDE_EN.pdf"),
        # EN/01_Excel_Templates
        (excel_en, "EN/01_Excel_Templates/Pulse_Content_Ops_Template_EN.xlsx"),
        (PACKAGES_DIR / "notion_power_query_en.m", "EN/01_Excel_Templates/notion_power_query_en.m"),
        (PACKAGES_DIR / "git_public_json_power_query_en.m", "EN/01_Excel_Templates/git_public_json_power_query_en.m"),
        # EN/02_Migration_Scripts
        (OPS_PULSE_DIR / "migrate_notion.py", "EN/02_Migration_Scripts/migrate_notion.py"),
        (PACKAGES_DIR / "pulse_repo_scanner.py", "EN/02_Migration_Scripts/pulse_repo_scanner.py"),
        (PACKAGES_DIR / "sample_notion_export_en.csv", "EN/02_Migration_Scripts/sample_notion_export_en.csv"),
        # EN/03_Documentation
        (pdf_en, "EN/03_Documentation/PULSE_EXECUTIVE_GUIDE_EN.pdf"),
        (PACKAGES_DIR / "PULSE_KIT_GUIDE_EN.md", "EN/03_Documentation/PULSE_KIT_GUIDE_EN.md"),
        (PACKAGES_DIR / "FIELD_SPECIFICATION_EN.md", "EN/03_Documentation/FIELD_SPECIFICATION_EN.md"),

        # --- CARPETAS LEGADAS (RETROCOMPATIBILIDAD) ---
        (excel_legacy, "01_Excel_Templates/Pulse_Content_Ops_Template.xlsx"),
        (PACKAGES_DIR / "notion_power_query.m", "01_Excel_Templates/notion_power_query.m"),
        (PACKAGES_DIR / "git_public_json_power_query.m", "01_Excel_Templates/git_public_json_power_query.m"),
        (OPS_PULSE_DIR / "migrate_notion.py", "02_Migration_Scripts/migrate_notion.py"),
        (PACKAGES_DIR / "pulse_repo_scanner.py", "02_Migration_Scripts/pulse_repo_scanner.py"),
        (PACKAGES_DIR / "sample_notion_export.csv", "02_Migration_Scripts/sample_notion_export.csv"),
        (pdf_legacy, "03_Documentation/GUIA_EJECUTIVA_PULSE.pdf"),
        (PACKAGES_DIR / "GUIA_PULSE_KIT.md", "03_Documentation/GUIA_PULSE_KIT.md"),
        (PACKAGES_DIR / "ESPECIFICACION_CAMPOS.md", "03_Documentation/ESPECIFICACION_CAMPOS.md"),
    ]

    # Verificar existencia de todos los archivos
    for src_path, arcname in files_to_pack:
        if not src_path.exists():
            raise FileNotFoundError(f"Archivo requerido para el kit no encontrado: {src_path} (para {arcname})")

    # Crear ZIP
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_OUTPUT_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for src_path, arcname in files_to_pack:
            zf.write(src_path, arcname=arcname)
            sha = compute_sha256(src_path)
            size_kb = round(src_path.stat().st_size / 1024, 1)
            print(f"  + Añadido '{arcname}' ({size_kb} KB) — SHA-256: {sha[:12]}...")

    # Verificar integridad del ZIP generado
    with zipfile.ZipFile(ZIP_OUTPUT_PATH, "r") as zf:
        bad_file = zf.testzip()
        if bad_file:
            raise RuntimeError(f"El archivo ZIP generado está corrupto en: {bad_file}")
        namelist = zf.namelist()

    zip_size_kb = round(ZIP_OUTPUT_PATH.stat().st_size / 1024, 1)
    zip_sha = compute_sha256(ZIP_OUTPUT_PATH)

    print(f"\n[OK] Kit comercial Dual empaquetado con éxito:")
    print(f"  - Destino: {ZIP_OUTPUT_PATH.resolve()}")
    print(f"  - Tamaño total: {zip_size_kb} KB")
    print(f"  - Ficheros incluidos: {len(namelist)}")
    print(f"  - Checksum SHA-256: {zip_sha}")

    # Sincronización en packages/00_DISTRIBUCION_LEMONSQUEEZY/
    LEMON_DIST_DIR.mkdir(parents=True, exist_ok=True)
    lemon_dest = LEMON_DIST_DIR / "Datalaria_Pulse_Kit.zip"
    shutil.copy2(ZIP_OUTPUT_PATH, lemon_dest)
    print(f"  - Sincronizado en distribución Lemon Squeezy: {lemon_dest.resolve()}")

    # Limpieza de artefactos redundantes o privados en packages/pulse/
    for legacy_name in ("datalaria-pulse-content-ops-kit-v1.0.zip", "Pulse_Private_Tracker.xlsx"):
        legacy_file = PACKAGES_DIR / legacy_name
        if legacy_file.exists():
            legacy_file.unlink()
            print(f"  - Eliminado artefacto redundante/privado: {legacy_file.name}")

    print()
    return ZIP_OUTPUT_PATH


if __name__ == "__main__":
    package_kit()
