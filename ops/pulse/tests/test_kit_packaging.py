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
from ops.pulse.release_18nov import verify_embargo, activate_launch, STAGED_CARD_PATH
from packages.pulse.pulse_repo_scanner import scan_directory, audit_seo, parse_simple_front_matter


def test_template_excel_structure(tmp_path):
    """Verifica que la plantilla del Kit comercial contiene las 6 hojas y 10 activos de muestra."""
    excel_path = build_pulse_excel(is_template=True, lang="es")
    assert excel_path.exists()
    assert excel_path.name in ("Pulse_Content_Ops_Template_ES.xlsx", "Pulse_Content_Ops_Template.xlsx")
    assert (excel_path.parent / "Pulse_Content_Ops_Template.xlsx").exists()

    wb = openpyxl.load_workbook(excel_path, data_only=False)
    expected_sheets = ["Instrucciones", "Taxonomía", "Activos", "Kanban", "Métricas", "Dashboard"]
    for s in expected_sheets:
        assert s in wb.sheetnames, f"Hoja faltante: {s}"

    # Comprobar hoja Instrucciones: flujo de trabajo en 3 pasos
    ws_intro = wb["Instrucciones"]
    intro_texts = [
        str(ws_intro.cell(row=r, column=c).value or "")
        for r in range(1, ws_intro.max_row + 1)
        for c in (2, 3)
    ]
    assert any("FLUJO DE TRABAJO RECOMENDADO EN 3 PASOS" in t for t in intro_texts)

    # Comprobar hoja Taxonomía
    ws_tax = wb["Taxonomía"]
    assert ws_tax.cell(row=1, column=1).value == "Tipo de Activo"
    assert ws_tax.cell(row=2, column=1).value == "POST"
    assert ws_tax.cell(row=1, column=2).value == "Estado"
    assert ws_tax.cell(row=2, column=2).value == "Idea"
    assert ws_tax.cell(row=1, column=6).value == "Categoría Canónica"
    assert ws_tax.cell(row=2, column=6).value == "IA, Ingeniería y Proyectos"
    assert ws_tax.cell(row=1, column=7).value == "Tipo Release"
    assert ws_tax.cell(row=2, column=7).value == "major"

    # Comprobar hoja Activos: 1 cabecera + 10 activos representativos
    ws_act = wb["Activos"]
    asset_rows = [r for r in range(2, ws_act.max_row + 1) if ws_act.cell(row=r, column=1).value]
    assert len(asset_rows) == 10

    types = [ws_act.cell(row=r, column=2).value for r in range(2, 12)]
    statuses = {ws_act.cell(row=r, column=3).value for r in range(2, 12)}
    parities = {ws_act.cell(row=r, column=10).value for r in range(2, 12)}
    categories = {ws_act.cell(row=r, column=11).value for r in range(2, 12)}
    seo_scores = [ws_act.cell(row=r, column=15).value for r in range(2, 12)]
    versions = {ws_act.cell(row=r, column=22).value for r in range(2, 12)}

    assert types.count("POST") == 8
    assert types.count("APP") == 1
    assert types.count("KIT") == 1
    assert {"Published", "Scheduled", "Review", "Draft", "Idea"}.issubset(statuses)
    assert "outdated_en" in parities
    assert {
        "IA, Ingeniería y Proyectos",
        "Estrategia y Operaciones",
        "Startups",
        "Pioneros y Referentes",
        "Cultura Tech y Media",
    }.issubset(categories)
    assert 65 in seo_scores
    assert {"v1.0.0", "v0.9.0", "v0.4.0"}.issubset(versions)

    # Verificar al menos un post de alto tráfico sin Kit asociado (Huérfano de monetización)
    # Las visitas reales se registran en Métricas (Col 3) y se vinculan a Activos dinámicamente
    ws_met = wb["Métricas"]
    high_traffic_ids = {
        ws_met.cell(row=r, column=1).value
        for r in range(2, ws_met.max_row + 1)
        if (ws_met.cell(row=r, column=3).value or 0) >= 2000
    }
    orphans = [
        r for r in range(2, 12)
        if ws_act.cell(row=r, column=1).value in high_traffic_ids
        and ws_act.cell(row=r, column=2).value == "POST"
        and not (ws_act.cell(row=r, column=18).value or "")
    ]
    assert len(orphans) >= 1

    # Columnas 22 y 23 de gobernanza de versiones SemVer
    assert ws_act.cell(row=1, column=22).value == "Versión"
    assert ws_act.cell(row=1, column=23).value == "Tipo Release"

    # Comprobar fórmulas universales en Dashboard (INV-PULSE-5)
    ws_dash = wb["Dashboard"]
    assert "COUNTA(" in str(ws_dash.cell(row=4, column=4).value)
    assert 'COUNTIF(Activos!C2:C11, "Published")' in str(ws_dash.cell(row=5, column=4).value) or "COUNTIF" in str(ws_dash.cell(row=5, column=4).value)


def test_sample_notion_csv_and_private_tracker_isolation():
    """Verifica 10 filas representativas en sample_notion_export.csv y aislamiento del tracker privado."""
    import csv

    csv_path = ROOT_DIR / "packages" / "pulse" / "sample_notion_export.csv"
    assert csv_path.exists()
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 10
    cats = {r["Category"] for r in rows}
    assert {
        "IA, Ingeniería y Proyectos",
        "Estrategia y Operaciones",
        "Startups",
        "Pioneros y Referentes",
        "Cultura Tech y Media",
    }.issubset(cats)
    statuses = {r["Status"] for r in rows}
    assert {"Published", "Scheduled", "In Review", "Draft", "Idea"}.issubset(statuses)

    private_path = build_pulse_excel(is_template=False)
    assert private_path == ROOT_DIR / "data" / "pulse" / "private" / "Pulse_Private_Tracker.xlsx"
    assert private_path.exists()
    assert not (ROOT_DIR / "packages" / "pulse" / "Pulse_Private_Tracker.xlsx").exists()


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
    """Verifica que el migrador exporta directamente a un libro Excel (.xlsx) estructurado en ES y EN."""
    csv_file = tmp_path / "sample_notion.csv"
    csv_content = (
        "Name,Status,Publish Date,Category,Asset Type,Tags,Title EN,Summary\n"
        "Modelo Financiero Monte Carlo,Published,2026-10-15,Estrategia,post,\"finanzas\",Monte Carlo Financial Model,Guía de simulación estocástica\n"
        "Arquitectura de Microservicios,In Review,2026-11-20,IA,post,\"cloud\",Microservices Architecture,Estrategia multi-cloud\n"
    )
    csv_file.write_text(csv_content, encoding="utf-8")

    out_xlsx = tmp_path / "Migrated_Pulse_Tracker.xlsx"
    assets = migrate_notion(csv_file, output_path=out_xlsx, out_format="xlsx", lang="es")

    assert len(assets) == 2
    assert out_xlsx.exists()

    wb = openpyxl.load_workbook(out_xlsx, data_only=False)
    assert "Activos" in wb.sheetnames
    assert "Dashboard" in wb.sheetnames
    assert "Kanban" in wb.sheetnames

    ws_act = wb["Activos"]
    asset_rows = [r for r in range(2, ws_act.max_row + 1) if ws_act.cell(row=r, column=1).value]
    assert len(asset_rows) == 2
    assert ws_act.cell(row=2, column=1).value == "modelo-financiero-monte-carlo"
    assert ws_act.cell(row=2, column=3).value == "Published"
    assert ws_act.cell(row=3, column=3).value == "Review"

    # Exportación en inglés
    out_xlsx_en = tmp_path / "Migrated_Pulse_Tracker_EN.xlsx"
    assets_en = migrate_notion(csv_file, output_path=out_xlsx_en, out_format="xlsx", lang="en")
    assert len(assets_en) == 2
    assert out_xlsx_en.exists()
    wb_en = openpyxl.load_workbook(out_xlsx_en, data_only=False)
    assert "Assets" in wb_en.sheetnames
    assert "Metrics" in wb_en.sheetnames
    ws_en = wb_en["Assets"]
    asset_rows_en = [r for r in range(2, ws_en.max_row + 1) if ws_en.cell(row=r, column=1).value]
    assert len(asset_rows_en) == 2


def test_pulse_repo_scanner(tmp_path):
    """Verifica que el escáner universal detecta front matter, paridad y calcula score SEO (ES & EN)."""
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

    results_es = scan_directory(content_dir, lang="es")
    assert len(results_es) == 1
    post_es = results_es[0]
    assert post_es["ID"] == "articulo-test"
    assert post_es["Paridad"] == "complete"
    assert post_es["Título (ES)"] == "Guía Cuantitativa de Prueba para Comités de Dirección"
    assert post_es["Título (EN)"] == "Quantitative Strategy Guide for Executive Committees"
    assert post_es["Palabras ES"] > 100
    assert post_es["Score SEO"] >= 60
    assert post_es["Estado"] == "Published"

    # Verificación en inglés
    results_en = scan_directory(content_dir, lang="en")
    assert len(results_en) == 1
    post_en = results_en[0]
    assert post_en["ID"] == "articulo-test"
    assert post_en["Parity"] == "complete"
    assert post_en["Title (ES)"] == "Guía Cuantitativa de Prueba para Comités de Dirección"
    assert post_en["Title (EN)"] == "Quantitative Strategy Guide for Executive Committees"
    assert post_en["Words ES"] > 100
    assert post_en["SEO Score"] >= 60
    assert post_en["Status"] == "Published"


def test_package_kit_zip():
    """Verifica el empaquetado comercial Dual ES/EN, raíz con onboarding, PDFs de 5 páginas y cero duplicados."""
    import fitz

    zip_path = package_kit()
    assert zip_path.exists()
    assert zip_path == ZIP_OUTPUT_PATH
    assert zip_path.stat().st_size > 15000

    # Garantizar ausencia de duplicado y de tracker privado en packages/pulse/
    packages_dir = ROOT_DIR / "packages" / "pulse"
    assert not (packages_dir / "datalaria-pulse-content-ops-kit-v1.0.zip").exists()
    assert not (packages_dir / "Pulse_Private_Tracker.xlsx").exists()
    zips_in_packages = [p.name for p in packages_dir.glob("*.zip")]
    assert zips_in_packages == ["Datalaria_Pulse_Kit.zip"]

    # Verificar sincronización en 00_DISTRIBUCION_LEMONSQUEEZY
    lemon_zip = LEMON_DIST_DIR / "Datalaria_Pulse_Kit.zip"
    assert lemon_zip.exists(), f"Falta sincronización en {lemon_zip}"
    assert lemon_zip.stat().st_size == zip_path.stat().st_size

    with zipfile.ZipFile(zip_path, "r") as zf:
        bad_file = zf.testzip()
        assert bad_file is None, f"Archivo ZIP corrupto: {bad_file}"
        names = zf.namelist()
        expected_files = [
            # Raíz bilingüe
            "00_EMPIEZA_AQUI_ES.md",
            "00_START_HERE_EN.md",
            "LICENSE_ES.txt",
            "LICENSE_EN.txt",
            "00_EMPIEZA_AQUI_README.md",
            "GUIA_EJECUTIVA_PULSE.pdf",
            "LICENSE.txt",
            # Edición Española (ES/)
            "ES/00_EMPIEZA_AQUI_README.md",
            "ES/GUIA_EJECUTIVA_PULSE_ES.pdf",
            "ES/01_Excel_Templates/Pulse_Content_Ops_Template_ES.xlsx",
            "ES/01_Excel_Templates/notion_power_query_es.m",
            "ES/01_Excel_Templates/git_public_json_power_query_es.m",
            "ES/02_Migration_Scripts/migrate_notion.py",
            "ES/02_Migration_Scripts/pulse_repo_scanner.py",
            "ES/02_Migration_Scripts/sample_notion_export_es.csv",
            "ES/03_Documentation/GUIA_EJECUTIVA_PULSE_ES.pdf",
            "ES/03_Documentation/GUIA_PULSE_KIT_ES.md",
            "ES/03_Documentation/ESPECIFICACION_CAMPOS_ES.md",
            # English Edition (EN/)
            "EN/00_START_HERE_README.md",
            "EN/PULSE_EXECUTIVE_GUIDE_EN.pdf",
            "EN/01_Excel_Templates/Pulse_Content_Ops_Template_EN.xlsx",
            "EN/01_Excel_Templates/notion_power_query_en.m",
            "EN/01_Excel_Templates/git_public_json_power_query_en.m",
            "EN/02_Migration_Scripts/migrate_notion.py",
            "EN/02_Migration_Scripts/pulse_repo_scanner.py",
            "EN/02_Migration_Scripts/sample_notion_export_en.csv",
            "EN/03_Documentation/PULSE_EXECUTIVE_GUIDE_EN.pdf",
            "EN/03_Documentation/PULSE_KIT_GUIDE_EN.md",
            "EN/03_Documentation/FIELD_SPECIFICATION_EN.md",
            # Carpetas legadas
            "01_Excel_Templates/Pulse_Content_Ops_Template.xlsx",
            "01_Excel_Templates/notion_power_query.m",
            "01_Excel_Templates/git_public_json_power_query.m",
            "02_Migration_Scripts/migrate_notion.py",
            "02_Migration_Scripts/pulse_repo_scanner.py",
            "02_Migration_Scripts/sample_notion_export.csv",
            "03_Documentation/GUIA_EJECUTIVA_PULSE.pdf",
            "03_Documentation/GUIA_PULSE_KIT.md",
            "03_Documentation/ESPECIFICACION_CAMPOS.md",
        ]
        for ef in expected_files:
            assert ef in names, f"Fichero faltante en el ZIP comercial: {ef}"

        pdf_bytes_es = zf.read("ES/GUIA_EJECUTIVA_PULSE_ES.pdf")
        pdf_bytes_en = zf.read("EN/PULSE_EXECUTIVE_GUIDE_EN.pdf")

    # Verificar PDF en español
    with fitz.open(stream=pdf_bytes_es, filetype="pdf") as doc_es:
        assert len(doc_es) == 5, f"Se esperaban 5 páginas en el PDF ES, encontradas {len(doc_es)}"
        full_text_es = "\n".join(page.get_text() for page in doc_es)
        assert "\u00b7" not in full_text_es, "Glifo corrupto '·' detectado en el PDF ES"
        assert "€" in full_text_es
        assert "Escenario 1" in full_text_es
        assert "Escenario 2" in full_text_es
        assert "Escenario 3" in full_text_es

    # Verificar PDF en inglés
    with fitz.open(stream=pdf_bytes_en, filetype="pdf") as doc_en:
        assert len(doc_en) == 5, f"Se esperaban 5 páginas en el PDF EN, encontradas {len(doc_en)}"
        full_text_en = "\n".join(page.get_text() for page in doc_en)
        assert "\u00b7" not in full_text_en, "Glifo corrupto '·' detectado en el PDF EN"
        assert "Scenario 1" in full_text_en
        assert "Scenario 2" in full_text_en
        assert "Scenario 3" in full_text_en


def test_embargo_18nov_and_previews():
    """Verifica que el embargo comercial hasta el 18-11-2026 se cumple y los assets existen."""
    ok, errors = verify_embargo()
    assert ok, f"Fallos en verificación de embargo: {errors}"

    # Verificar que las imágenes preview de alta resolución existen
    img_es = ROOT_DIR / "static" / "images" / "recursos" / "pulse-preview-es.png"
    img_en = ROOT_DIR / "static" / "images" / "recursos" / "pulse-preview-en.png"
    assert img_es.exists() and img_es.stat().st_size > 50000
    assert img_en.exists() and img_en.stat().st_size > 50000


def test_staged_card_links_point_to_part1():
    """Verifica que la tarjeta staged_pack_pulse_18nov.json apunta a la Parte 1 y tiene metadata v1.0.0."""
    import json
    assert STAGED_CARD_PATH.exists(), f"Falta la tarjeta staged: {STAGED_CARD_PATH}"
    data = json.loads(STAGED_CARD_PATH.read_text(encoding="utf-8"))

    assert data["id"] == "pack-pulse"
    assert data["status"] == "available"
    assert data["version"] == "v1.0.0"
    assert data["publish_date"] == "2026-11-18"
    assert data["article_url_es"] == "/es/posts/pulse-parte1-adios-notion-content-ops/"
    assert data["article_url_en"] == "/en/posts/pulse-part1-goodbye-notion-content-ops/"
    assert data["guide_url_es"] == "/es/posts/pulse-parte1-adios-notion-content-ops/"
    assert data["guide_url_en"] == "/en/posts/pulse-part1-goodbye-notion-content-ops/"


def test_activate_launch_in_sandbox(tmp_path):
    """Verifica la activación atómica del lanzamiento comercial en un entorno aislado sin tocar disco real."""
    # 1. Preparar archivos mockeados en sandbox
    mock_data_apps = tmp_path / "data" / "apps"
    mock_data_apps.mkdir(parents=True, exist_ok=True)
    (mock_data_apps / "pulse.yaml").write_text(
        "status: incubating\ncurrent_version: v1.0.0\n",
        encoding="utf-8"
    )

    mock_es_apps = tmp_path / "content" / "es" / "apps" / "pulse"
    mock_es_apps.mkdir(parents=True, exist_ok=True)
    (mock_es_apps / "index.md").write_text(
        "---\ntitle: 'Datalaria Pulse'\ndraft: true\n---\nContenido ES",
        encoding="utf-8"
    )

    mock_en_apps = tmp_path / "content" / "en" / "apps" / "pulse"
    mock_en_apps.mkdir(parents=True, exist_ok=True)
    (mock_en_apps / "index.md").write_text(
        "---\ntitle: 'Datalaria Pulse'\ndraft: true\n---\nContent EN",
        encoding="utf-8"
    )

    mock_data_pulse = tmp_path / "data" / "pulse"
    mock_data_pulse.mkdir(parents=True, exist_ok=True)
    (mock_data_pulse / "kits.yaml").write_text(
        "# Kits\n- id: pack-sdd\n  title: SDD Kit\n",
        encoding="utf-8"
    )

    mock_partials = tmp_path / "layouts" / "partials"
    mock_partials.mkdir(parents=True, exist_ok=True)
    (mock_partials / "recursos_catalog.html").write_text(
        'Mostrando 14 Kits (13 Disponibles)\n'
        '<div class="kit-card is-locked" id="pack-sdd">\n'
        '{\n    "id": "pack-sdd",\n'
        '{{- else -}}\n'
        'Showing 14 Kits (13 Available)\n'
        '<div class="kit-card is-locked" id="pack-sdd">\n'
        '{\n    "id": "pack-sdd",\n',
        encoding="utf-8"
    )
    (mock_partials / "index_profile.html").write_text(
        '(dict "slug" "obs-management"\n'
        '(dict "key" "b2b"      "icon" "💼" "label" (cond $isES "Suites B2B & IA Operacional" "B2B Suites & AI")     "count" 1)\n',
        encoding="utf-8"
    )

    # 2. Ejecutar activación atómica
    checkout_url = "https://datalaria.lemonsqueezy.com/buy/test-checkout-pulse"
    changes = activate_launch(checkout_url=checkout_url, root_dir=tmp_path, dry_run=False)

    # 3. Validar mutaciones registradas
    assert changes["pulse_yaml_updated"] is True
    assert len(changes["content_pages_unembargoed"]) == 2
    assert changes["kits_yaml_updated"] is True
    assert changes["recursos_catalog_updated"] is True
    assert changes["index_profile_updated"] is True

    # 4. Validar contenido físico en disco del sandbox
    pulse_text = (mock_data_apps / "pulse.yaml").read_text(encoding="utf-8")
    assert "status: live" in pulse_text
    assert "status: incubating" not in pulse_text

    es_text = (mock_es_apps / "index.md").read_text(encoding="utf-8")
    assert "draft: false" in es_text

    en_text = (mock_en_apps / "index.md").read_text(encoding="utf-8")
    assert "draft: false" in en_text

    kits_text = (mock_data_pulse / "kits.yaml").read_text(encoding="utf-8")
    assert "- id: pack-pulse" in kits_text
    assert checkout_url in kits_text
    assert "/es/posts/pulse-parte1-adios-notion-content-ops/" in kits_text

    cat_text = (mock_partials / "recursos_catalog.html").read_text(encoding="utf-8")
    assert 'id="pack-pulse"' in cat_text
    assert checkout_url in cat_text
    assert "Mostrando 15 Kits (14 Disponibles)" in cat_text

    prof_text = (mock_partials / "index_profile.html").read_text(encoding="utf-8")
    assert '"slug" "pulse"' in prof_text
    assert '"count" 2' in prof_text
