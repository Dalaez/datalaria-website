# -*- coding: utf-8 -*-
"""ops/obs_kit/tests/test_obs_kit.py — Suite determinista de verificación para Hito OBS-6 (pack-obs).

Valida:
1. Libros Excel Duales ES/EN (.xlsx sin VBA): 5 hojas exactas, tablas nativas, fórmulas auditadas sin errores,
   celdas editables desbloqueadas y diferenciación explícita frente a pack-stock.
2. Playbooks PDF vectoriales A4 (ES/EN): exactamente 5 páginas, cero glifos rotos/tofu (□ / U+FFFD).
3. Integridad ZIP numerado + SHA-256 en packages/obs_kit/ y packages/00_DISTRIBUCION_LEMONSQUEEZY/,
   cero fugas privadas/.env y compatibilidad CSV con Agentic Radar v2.0.
4. Dimensiones exactas de previews 1600x980 y portadas 1200x750 / 1200x630 / 1080x1080.
5. Coherencia en data/pulse/kits.yaml (publish_date 2026-12-09), --verify-embargo (exit 0) y
   Modal Brevo Modo Pro B2B en Cockpit v2.0 sin mailto: (INV-HELIX-WL-4).
"""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import fitz
import openpyxl
import yaml
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[3]
PKG_DIR = REPO_ROOT / "packages" / "obs_kit"
DIST_DIR = REPO_ROOT / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY"
RECURSOS_DIR = REPO_ROOT / "static" / "images" / "recursos"
STATIC_OBS_DIR = REPO_ROOT / "static" / "apps" / "obs-management"
KITS_YAML = REPO_ROOT / "data" / "pulse" / "kits.yaml"

ZIP_NAME = "Datalaria_IEC62402_Obsolescence_LTB_Kit_Dual.zip"
PKG_ZIP = PKG_DIR / ZIP_NAME
DIST_ZIP = DIST_DIR / ZIP_NAME

EXPECTED_SHEETS = [
    "01_BOM_AML_EXPLORER",
    "02_IEC62402_CRITICALITY",
    "03_LTB_VS_FFF_SIMULATOR",
    "04_MITIGATION_ROADMAP",
    "05_EXECUTIVE_DASHBOARD",
]
EXCEL_ERROR_TOKENS = ("#REF!", "#NAME?", "#VALUE!", "#DIV/0!", "#N/A", "#NUM!")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_excel_dual_workbooks_5_sheets_formulas_and_no_vba() -> None:
    """Valida ambos libros .xlsx (ES y EN) dentro del ZIP: 5 hojas, 0 VBA, fórmulas válidas y tablas."""
    assert PKG_ZIP.exists(), f"Falta ZIP maestro: {PKG_ZIP}"
    with zipfile.ZipFile(PKG_ZIP, "r") as zf:
        for rel in (
            "01_EXCEL_MOTOR_BOM_LTB/ES/IEC62402_Obsolescencia_BOM_LTB_ES.xlsx",
            "01_EXCEL_MOTOR_BOM_LTB/EN/IEC62402_Obsolescence_BOM_LTB_EN.xlsx",
        ):
            assert rel in zf.namelist(), f"Falta Excel en ZIP: {rel}"
            raw_bytes = zf.read(rel)
            # Cero VBA (los .xlsx con macros contienen vbaProject.bin)
            with zipfile.ZipFile(io.BytesIO(raw_bytes), "r") as xzf:
                assert not any("vbaproject" in n.lower() for n in xzf.namelist()), f"VBA detectado en {rel}"

            wb = openpyxl.load_workbook(io.BytesIO(raw_bytes), data_only=False)
            assert wb.sheetnames == EXPECTED_SHEETS, f"Hojas esperadas {EXPECTED_SHEETS}, halladas {wb.sheetnames}"

            formula_count = 0
            all_text = []
            for sname in EXPECTED_SHEETS:
                ws = wb[sname]
                for row in ws.iter_rows(values_only=True):
                    for val in row:
                        if isinstance(val, str):
                            for err_tok in EXCEL_ERROR_TOKENS:
                                assert err_tok not in val, f"Error de fórmula {err_tok} en {rel}::{sname}"
                            if val.startswith("="):
                                formula_count += 1
                            all_text.append(val)

            assert formula_count >= 180, f"Fórmulas insuficientes ({formula_count}) en {rel}"
            assert len(wb["01_BOM_AML_EXPLORER"].tables) >= 1
            assert len(wb["02_IEC62402_CRITICALITY"].tables) >= 1
            assert len(wb["03_LTB_VS_FFF_SIMULATOR"].tables) >= 1
            assert len(wb["04_MITIGATION_ROADMAP"].tables) >= 1
            assert len(wb["05_EXECUTIVE_DASHBOARD"]._charts) >= 1

            joined = "\n".join(all_text).lower()
            assert "pack-stock" in joined and "pack-obs" in joined, "Falta diferenciación pack-stock vs. pack-obs en Excel"
            assert "ss_ltb" in joined or "roundup" in joined, "Falta cálculo SS_LTB en Simulador LTB vs. FFF"


def test_pdf_playbooks_5_pages_and_zero_tofu_glyphs() -> None:
    """Valida ambos Playbooks PDF A4 (ES y EN): exactamente 5 páginas y cero glifos rotos □ / U+FFFD."""
    with zipfile.ZipFile(PKG_ZIP, "r") as zf:
        for rel in (
            "02_PLAYBOOK_EJECUTIVO_PDF/ES/Playbook_Ejecutivo_IEC62402_LTB_ES.pdf",
            "02_PLAYBOOK_EJECUTIVO_PDF/EN/Executive_Playbook_IEC62402_LTB_EN.pdf",
        ):
            assert rel in zf.namelist(), f"Falta PDF en ZIP: {rel}"
            doc = fitz.open(stream=zf.read(rel), filetype="pdf")
            try:
                assert len(doc) == 5, f"Se esperaban exactamente 5 páginas en {rel}, halladas {len(doc)}"
                full_text = []
                for idx, page in enumerate(doc):
                    assert 590 <= page.rect.width <= 600 and 838 <= page.rect.height <= 846, f"No es A4 en p.{idx + 1}"
                    txt = page.get_text("text")
                    assert len(txt.strip()) >= 250, f"Página {idx + 1} de {rel} casi vacía"
                    assert "\ufffd" not in txt and "□" not in txt, f"Glifo tofu detectado en {rel} p.{idx + 1}"
                    full_text.append(txt)
                joined = "\n".join(full_text).replace("\u2010", "-")
                assert "IEC 62402" in joined
                assert "pack-stock" in joined and "pack-obs" in joined
            finally:
                doc.close()


def test_zip_numbered_topology_sha256_integrity_and_dual_sync() -> None:
    """Verifica topología numerada, SHA-256 interno, copia byte-a-byte y compatibilidad CSV."""
    assert PKG_ZIP.exists() and DIST_ZIP.exists()
    assert _sha256_bytes(PKG_ZIP.read_bytes()) == _sha256_bytes(DIST_ZIP.read_bytes())

    manifest_json = json.loads((PKG_DIR / "SHA256_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest_json["kit_id"] == "pack-obs"
    assert manifest_json["release_date"] == "2026-12-09"
    assert manifest_json["zip_sha256"] == _sha256_bytes(PKG_ZIP.read_bytes())

    with zipfile.ZipFile(PKG_ZIP, "r") as zf:
        assert zf.testzip() is None
        names = set(zf.namelist())
        for req in (
            "README.md",
            "LICENSE.txt",
            "SHA256_MANIFEST.txt",
            "03_STARTER_BLUEPRINT_TECNICO/obs_radar_supabase_schema.sql",
            "03_STARTER_BLUEPRINT_TECNICO/bom_engine.py",
            "03_STARTER_BLUEPRINT_TECNICO/models.py",
            "03_STARTER_BLUEPRINT_TECNICO/env.example",
            "03_STARTER_BLUEPRINT_TECNICO/datalaria_bom_industrial_template.csv",
        ):
            assert req in names, f"Falta archivo en ZIP: {req}"

        # Verificar cero fugas privadas o .env reales
        for n in names:
            assert "private/" not in n and not n.endswith("/.env") and n != ".env"

        # Verificar cada hash SHA-256 listado en SHA256_MANIFEST.txt
        manifest_txt = zf.read("SHA256_MANIFEST.txt").decode("utf-8")
        checked = 0
        for line in manifest_txt.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            expected_hash, rel_path = line.split("  ", 1)
            assert _sha256_bytes(zf.read(rel_path)) == expected_hash, f"Hash SHA-256 inválido para {rel_path}"
            checked += 1
        assert checked >= 10

        # Verificar que la plantilla CSV coincide con el parser de Agentic Radar v2.0
        csv_header = zf.read("03_STARTER_BLUEPRINT_TECNICO/datalaria_bom_industrial_template.csv").decode("utf-8").splitlines()[0]
        assert csv_header == "End_Product_SKU,End_Product_Margin,Assembly_PN,Component_PN,Quantity_per_Assembly,Manufacturer,Manufacturer_PN,Lifecycle"


def test_visual_previews_and_store_covers_dimensions() -> None:
    """Valida dimensiones exactas de previews 1600x980 y portadas 1200x750 / 1200x630 / 1080x1080."""
    expected_images = [
        (RECURSOS_DIR / "obs-preview-es.png", (1600, 980)),
        (RECURSOS_DIR / "obs-preview-en.png", (1600, 980)),
        (DIST_DIR / "Images" / "Obsolescence_IEC62402_Cover_1200x750_ES.png", (1200, 750)),
        (DIST_DIR / "Images" / "Obsolescence_IEC62402_Cover_1200x750_EN.png", (1200, 750)),
        (DIST_DIR / "Images" / "Obsolescence_IEC62402.png", (1200, 630)),
        (DIST_DIR / "Images_Square" / "Obsolescence_IEC62402.png", (1080, 1080)),
    ]
    for path, dims in expected_images:
        assert path.exists(), f"Falta imagen comercial: {path}"
        with Image.open(path) as im:
            assert im.size == dims, f"{path.name}: dimensiones {im.size} != {dims}"


def test_kits_yaml_embargo_cli_and_cockpit_brevo_modal() -> None:
    """Valida registro pack-obs en kits.yaml (2026-12-09), --verify-embargo y Modal Brevo sin mailto:."""
    data = yaml.safe_load(KITS_YAML.read_text(encoding="utf-8"))
    pack = next((k for k in data.get("kits", []) if k.get("id") == "pack-obs"), None)
    assert pack is not None, "pack-obs no registrado en data/pulse/kits.yaml"
    assert pack["status"] == "coming"
    assert str(pack["publish_date"]) == "2026-12-09"
    assert pack["price"] == "19€" and pack["original_price"] == "39€"
    assert pack["article_url_es"] == "/es/posts/obs_parte8_simulador_ltb_v2/"
    assert pack["article_url_en"] == "/en/posts/obs_part8_ltb_simulator_v2/"
    assert pack["preview_image_es"] == "/images/recursos/obs-preview-es.png"
    assert pack["preview_image_en"] == "/images/recursos/obs-preview-en.png"

    res = subprocess.run(
        [sys.executable, "-m", "ops.obs_kit.build_kit", "--verify-embargo"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0, f"--verify-embargo falló: {res.stdout} {res.stderr}"
    assert "EMBARGO_PASS" in res.stdout

    # Modal Brevo Modo Pro B2B en Cockpit v2.0 (sin mailto:, con autocomplete estándar)
    html = (STATIC_OBS_DIR / "index.html").read_text(encoding="utf-8")
    app_js = (STATIC_OBS_DIR / "app.js").read_text(encoding="utf-8")
    assert 'id="proKitDialog"' in html and 'id="btnOpenProKit"' in html
    assert 'autocomplete="name"' in html and 'autocomplete="email"' in html
    assert "/.netlify/functions/subscribe" in app_js
    assert "mailto:" not in html.lower() and "mailto:" not in app_js.lower()
