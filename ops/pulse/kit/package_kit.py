"""
ops/pulse/kit/package_kit.py
----------------------------
Empaquetador Automatizado del Kit Comercial de Datalaria Pulse.
Especificación: Hito 5.6 & 6.3 (specs/apps/pulse/spec.md).

Genera el artefacto comercial final: packages/pulse/Datalaria_Pulse_Kit.zip
organizado en 3 carpetas temáticas numeradas para máxima claridad del comprador:
  - 01_Excel_Templates/
  - 02_Migration_Scripts/
  - 03_Documentation/
  - LICENSE.txt
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
from ops.pulse.kit.build_pdf_guide import build_pulse_pdf_guide


def compute_sha256(file_path: Path) -> str:
    """Calcula el hash SHA-256 de un archivo binario."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def package_kit() -> Path:
    """Compila y empaqueta el kit descargable comercial en formato ZIP con 3 carpetas numeradas."""
    print("[KIT BUILD] Compilando plantilla maestra de Excel...")
    template_excel = build_pulse_excel(is_template=True)

    print("[KIT BUILD] Compilando guía ejecutiva maquetada en PDF...")
    pdf_guide = build_pulse_pdf_guide()

    # Archivos a incluir en el ZIP comercial organizados en 3 carpetas numeradas
    files_to_pack: List[Tuple[Path, str]] = [
        # 01_Excel_Templates
        (template_excel, "01_Excel_Templates/Pulse_Content_Ops_Template.xlsx"),
        (PACKAGES_DIR / "notion_power_query.m", "01_Excel_Templates/notion_power_query.m"),
        (PACKAGES_DIR / "git_public_json_power_query.m", "01_Excel_Templates/git_public_json_power_query.m"),
        # 02_Migration_Scripts
        (OPS_PULSE_DIR / "migrate_notion.py", "02_Migration_Scripts/migrate_notion.py"),
        (PACKAGES_DIR / "pulse_repo_scanner.py", "02_Migration_Scripts/pulse_repo_scanner.py"),
        (PACKAGES_DIR / "sample_notion_export.csv", "02_Migration_Scripts/sample_notion_export.csv"),
        # 03_Documentation
        (pdf_guide, "03_Documentation/GUIA_EJECUTIVA_PULSE.pdf"),
        (PACKAGES_DIR / "GUIA_PULSE_KIT.md", "03_Documentation/GUIA_PULSE_KIT.md"),
        (PACKAGES_DIR / "ESPECIFICACION_CAMPOS.md", "03_Documentation/ESPECIFICACION_CAMPOS.md"),
        # Root License
        (PACKAGES_DIR / "LICENSE.txt", "LICENSE.txt"),
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

    print(f"\n[OK] Kit comercial empaquetado con éxito:")
    print(f"  - Destino: {ZIP_OUTPUT_PATH.resolve()}")
    print(f"  - Tamaño total: {zip_size_kb} KB")
    print(f"  - Ficheros incluidos: {len(namelist)}")
    print(f"  - Checksum SHA-256: {zip_sha}")

    # Sincronización en packages/00_DISTRIBUCION_LEMONSQUEEZY/
    LEMON_DIST_DIR.mkdir(parents=True, exist_ok=True)
    lemon_dest = LEMON_DIST_DIR / "Datalaria_Pulse_Kit.zip"
    shutil.copy2(ZIP_OUTPUT_PATH, lemon_dest)
    print(f"  - Sincronizado en distribución Lemon Squeezy: {lemon_dest.resolve()}\n")

    return ZIP_OUTPUT_PATH


if __name__ == "__main__":
    package_kit()
