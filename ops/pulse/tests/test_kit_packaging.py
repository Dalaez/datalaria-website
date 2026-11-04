"""
ops/pulse/tests/test_kit_packaging.py
-------------------------------------
Suite de pruebas automatizadas para el Kit comercial descargable de Datalaria Pulse.
Especificación: Hito 5.6 & 6.3 (specs/apps/pulse/spec.md & plan_hito_6_3_ejecucion_flash.md).

Valida:
1. Estructura, fórmulas e integridad de la plantilla Excel y taxonomía (6 hojas).
2. Migrador de bases de datos de Notion (YAML y exportación directa a Excel .xlsx).
3. Escáner universal de repositorios de contenidos sin dependencias externas.
4. Empaquetado comercial en 3 carpetas numeradas en packages/pulse/ y 00_DISTRIBUCION_LEMONSQUEEZY/.
5. Cumplimiento determinista del embargo comercial del 18 de noviembre y existencia de previews.
"""

import sys
import zipfile
from pathlib import Path
import openpyxl
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ops.pulse.kit.build_pulse_kit import build_pulse_excel
from ops.pulse.kit.package_kit import package_kit, ZIP_OUTPUT_PATH, LEMON_DIST_DIR
from ops.pulse.migrate_notion import migrate_notion, normalize_status, parse_date_str
from ops.pulse.release_18nov import verify_embargo
from packages.pulse.pulse_repo_scanner import scan_directory, audit_seo, parse_simple_front_matter


def test_template_excel_structure(tmp_path):
    """Verifica que la plantilla del Kit comercial contiene las 6 hojas y los 5 ejemplos guiados."""
    excel_path = build_pulse_excel(is_template=True)
    assert excel_path.exists()
    assert excel_path.name == "Pulse_Content_Ops_Template.xlsx"

    wb = openpyxl.load_workbook(excel_path, data_only=False)
    expected_sheets = ["Instrucciones", "Taxonomía", "Activos", "Kanban", "Métricas", "Dashboard"]
    for s in expected_sheets:
        assert s in wb.sheetnames, f"Hoja faltante: {s}"

    # Comprobar hoja Taxonomía
    ws_tax = wb["Taxonomía"]
    assert ws_tax.cell(row=1, column=1).value == "Tipo de Activo"
    assert ws_tax.cell(row=2, column=1).value == "POST"
    assert ws_tax.cell(row=1, column=2).value == "Estado"
    assert ws_tax.cell(row=2, column=2).value == "Idea"

    # Comprobar hoja Activos: 1 cabecera + 5 ejemplos guiados
    ws_act = wb["Activos"]
    assert ws_act.max_row == 6
    assert ws_act.cell(row=2, column=2).value == "POST"
    assert ws_act.cell(row=2, column=3).value == "Published"
    assert ws_act.cell(row=3, column=3).value == "Scheduled"
    assert ws_act.cell(row=4, column=3).value == "Draft"
    assert ws_act.cell(row=5, column=3).value == "Idea"
    assert ws_act.cell(row=6, column=2).value == "KIT"

    # Comprobar fórmulas universales en Dashboard (INV-PULSE-5)
    ws_dash = wb["Dashboard"]
    assert "COUNTA(" in str(ws_dash.cell(row=4, column=4).value)
    assert 'COUNTIF(Activos!C2:C5, "Published")' in str(ws_dash.cell(row=5, column=4).value) or "COUNTIF" in str(ws_dash.cell(row=5, column=4).value)


def test_migrate_notion_csv(tmp_path):
    """Verifica la importación y normalización determinista de un CSV exportado de Notion a YAML."""
    csv_file = tmp_path / "notion_export.csv"
    csv_content = (
        "Name,Status,Date,Category,Tags,Summary\n"
        "Guía de Optimización,En redacción,2026-11-05,Operaciones,\"ops,lean\",Borrador inicial\n"
        "Nuevo Producto B2B,Live,15/10/2026,Estrategia,\"c-level,b2b\",Lanzamiento suite\n"
        "Idea de Podcast,To Do,,Marketing,\"audio\",Explorar podcast semanal\n"
        "Post sobre Machine Learning,Calendarizado,2026-12-01,IA,\"ml,python\",En cola de revisión\n"
    )
    csv_file.write_text(csv_content, encoding="utf-8")

    out_yaml = tmp_path / "backlog_imported.yaml"
    assets = migrate_notion(csv_file, output_path=out_yaml, out_format="yaml")

    assert len(assets) == 4
    assert out_yaml.exists()

    # Mapeo de estados normalizados
    by_title = {a["title_es"]: a for a in assets}
    assert by_title["Guía de Optimización"]["status"] == "draft"
    assert by_title["Guía de Optimización"]["publish_date"] == "2026-11-05"
    assert by_title["Nuevo Producto B2B"]["status"] == "published"
    assert by_title["Nuevo Producto B2B"]["publish_date"] == "2026-10-15"
    assert by_title["Idea de Podcast"]["status"] == "idea"
    assert by_title["Idea de Podcast"]["publish_date"] is None
    assert by_title["Post sobre Machine Learning"]["status"] == "scheduled"
    assert by_title["Post sobre Machine Learning"]["publish_date"] == "2026-12-01"


def test_migrate_notion_xlsx_export(tmp_path):
    """Verifica que el migrador exporta directamente a un libro Excel (.xlsx) estructurado."""
    csv_file = tmp_path / "sample_notion.csv"
    csv_content = (
        "Name,Status,Publish Date,Category,Asset Type,Tags,Title EN,Summary\n"
        "Modelo Financiero Monte Carlo,Published,2026-10-15,Estrategia,post,\"finanzas\",Monte Carlo Financial Model,Guía de simulación estocástica\n"
        "Arquitectura de Microservicios,In Review,2026-11-20,IA,post,\"cloud\",Microservices Architecture,Estrategia multi-cloud\n"
    )
    csv_file.write_text(csv_content, encoding="utf-8")

    out_xlsx = tmp_path / "Migrated_Pulse_Tracker.xlsx"
    assets = migrate_notion(csv_file, output_path=out_xlsx, out_format="xlsx")

    assert len(assets) == 2
    assert out_xlsx.exists()

    wb = openpyxl.load_workbook(out_xlsx, data_only=False)
    assert "Activos" in wb.sheetnames
    assert "Dashboard" in wb.sheetnames
    assert "Kanban" in wb.sheetnames

    ws_act = wb["Activos"]
    assert ws_act.max_row == 3  # 1 cabecera + 2 activos
    assert ws_act.cell(row=2, column=1).value == "modelo-financiero-monte-carlo"
    assert ws_act.cell(row=2, column=3).value == "Published"
    assert ws_act.cell(row=3, column=3).value == "Review"


def test_pulse_repo_scanner(tmp_path):
    """Verifica que el escáner universal detecta front matter, paridad y calcula score SEO."""
    content_dir = tmp_path / "content"
    es_dir = content_dir / "es" / "posts" / "articulo-test"
    en_dir = content_dir / "en" / "posts" / "articulo-test"
    es_dir.mkdir(parents=True, exist_ok=True)
    en_dir.mkdir(parents=True, exist_ok=True)

    # Post ES
    (es_dir / "index.md").write_text(
        "---\n"
        "title: 'Guía Cuantitativa de Prueba para Comités de Dirección'\n"
        "date: '2026-10-20'\n"
        "draft: false\n"
        "categories: ['Estrategia']\n"
        "tags: ['c-level', 'finanzas', 'analitica']\n"
        "summary: 'Este es un resumen estructurado para validar la auditoría de SEO y lectura.'\n"
        "---\n\n"
        "# Introducción\n\n"
        "Contenido de prueba con suficiente longitud para validar el escáner. " * 30 +
        "\n\n[Enlace Interno](/es/apps/) y una imagen ![Grafico](/img/chart.png)\n",
        encoding="utf-8"
    )

    # Post EN (paridad completa)
    (en_dir / "index.md").write_text(
        "---\n"
        "title: 'Quantitative Strategy Guide for Executive Committees'\n"
        "date: '2026-10-20'\n"
        "draft: false\n"
        "---\n\n"
        "# Introduction\n\n"
        "English test content to ensure complete language parity across directories.\n",
        encoding="utf-8"
    )

    results = scan_directory(content_dir)
    assert len(results) == 1
    post = results[0]

    assert post["ID"] == "articulo-test"
    assert post["Paridad"] == "complete"
    assert post["Título (ES)"] == "Guía Cuantitativa de Prueba para Comités de Dirección"
    assert post["Título (EN)"] == "Quantitative Strategy Guide for Executive Committees"
    assert post["Palabras ES"] > 100
    assert post["Score SEO"] >= 60
    assert post["Estado"] == "Published"


def test_package_kit_zip():
    """Verifica que el archivo ZIP comercial se genera correctamente en 3 carpetas numeradas."""
    zip_path = package_kit()
    assert zip_path.exists()
    assert zip_path == ZIP_OUTPUT_PATH
    assert zip_path.stat().st_size > 15000  # Al menos 15 KB con PDF y plantillas

    # Verificar sincronización en 00_DISTRIBUCION_LEMONSQUEEZY
    lemon_zip = LEMON_DIST_DIR / "Datalaria_Pulse_Kit.zip"
    assert lemon_zip.exists(), f"Falta sincronización en {lemon_zip}"
    assert lemon_zip.stat().st_size == zip_path.stat().st_size

    with zipfile.ZipFile(zip_path, "r") as zf:
        bad_file = zf.testzip()
        assert bad_file is None, f"Archivo ZIP corrupto: {bad_file}"
        names = zf.namelist()
        expected_files = [
            "01_Excel_Templates/Pulse_Content_Ops_Template.xlsx",
            "01_Excel_Templates/notion_power_query.m",
            "01_Excel_Templates/git_public_json_power_query.m",
            "02_Migration_Scripts/migrate_notion.py",
            "02_Migration_Scripts/pulse_repo_scanner.py",
            "02_Migration_Scripts/sample_notion_export.csv",
            "03_Documentation/GUIA_EJECUTIVA_PULSE.pdf",
            "03_Documentation/GUIA_PULSE_KIT.md",
            "03_Documentation/ESPECIFICACION_CAMPOS.md",
            "LICENSE.txt"
        ]
        for ef in expected_files:
            assert ef in names, f"Fichero faltante en el ZIP comercial: {ef}"


def test_embargo_18nov_and_previews():
    """Verifica que el embargo comercial hasta el 18-11-2026 se cumple y los assets existen."""
    ok, errors = verify_embargo()
    assert ok, f"Fallos en verificación de embargo: {errors}"

    # Verificar que las imágenes preview de alta resolución existen
    img_es = ROOT_DIR / "static" / "images" / "recursos" / "pulse-preview-es.png"
    img_en = ROOT_DIR / "static" / "images" / "recursos" / "pulse-preview-en.png"
    assert img_es.exists() and img_es.stat().st_size > 50000
    assert img_en.exists() and img_en.stat().st_size > 50000
