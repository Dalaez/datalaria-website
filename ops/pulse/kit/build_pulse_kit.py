"""
ops/pulse/kit/build_pulse_kit.py
--------------------------------
Generador Programático del Excel Maestro de Datalaria Pulse.
Especificación técnica formal: SPEC-APP-PULSE (specs/apps/pulse/spec.md) - Hitos 5.4, 5.6 y P-LAUNCH-3B.

Genera dos libros Excel:
1. data/pulse/private/Pulse_Private_Tracker.xlsx:
   Tracker privado para Daniel Alaez con el 100% de los datos reales del blog
   (posts, apps, kits, métricas cuantitativas absolutas de GA4/GSC, paridad y frescura).
   ¡Sustituto definitivo e instantáneo de Notion!
2. packages/pulse/Pulse_Content_Ops_Template.xlsx:
   Plantilla universal para el Kit de clientes (con 10 activos de muestra representativos,
   validaciones y fórmulas compatibles con Excel 2016/2019/365 y Google Sheets - INV-PULSE-5).
"""

import os
import json
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Any, Optional

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
INDEX_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "metrics.json"
OUTPUT_DIR = ROOT_DIR / "packages" / "pulse"
PRIVATE_OUTPUT_DIR = ROOT_DIR / "data" / "pulse" / "private"


# Paleta corporativa Datalaria Dark & Tech
FONT_FAMILY = "Segoe UI"
HEADER_FILL = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid") # Slate 800
HEADER_FONT = Font(name=FONT_FAMILY, size=11, bold=True, color="FFFFFF")
ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")  # Slate 50
THIN_BORDER = Border(
    left=Side(style="thin", color="E2E8F0"),
    right=Side(style="thin", color="E2E8F0"),
    top=Side(style="thin", color="E2E8F0"),
    bottom=Side(style="thin", color="E2E8F0")
)
BADGE_COMPLETE = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # Verde
BADGE_WARN = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")     # Amarillo
BADGE_ALERT = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")    # Rojo

# 10 Activos representativos para la Plantilla del Kit (8 post, 1 app, 1 kit)
# Cubren las 5 categorías canónicas, los 5 estados del flujo editorial,
# versiones SemVer (v1.0.0, v0.9.0, v0.4.0) y 3 casos didácticos para el Caso de Uso Scriba.
TEMPLATE_EXAMPLE_ASSETS = [
    {
        "id": "pulse-adios-notion-content-ops",
        "asset_type": "post",
        "status": "published",
        "visibility": "public",
        "title_es": "Adiós Notion: Content Ops as Code en Git con Python y React",
        "title_en": "Goodbye Notion: Content Ops as Code in Git with Python and React",
        "publish_date": "2026-11-18",
        "last_modified_es": "2026-11-18",
        "last_modified_en": "2026-11-18",
        "language_parity": "complete",
        "category": "IA, Ingeniería y Proyectos",
        "version": "v1.0.0",
        "release_type": "major",
        "word_count_es": 2650,
        "word_count_en": 2580,
        "reading_time_min": 13,
        "seo_audit": {"score_0_100": 95},
        "freshness_status": "fresh",
        "related_app": "pulse",
        "related_kit": "pack-pulse",
        "price": "19€",
        "sample_views": 1850,
        "sample_users": 1290,
        "sample_eng_sec": 268.0,
        "sample_clicks": 410,
        "sample_impr": 5200,
        "sample_ctr": 7.88,
        "sample_pos": 3.4
    },
    {
        "id": "framework-porter-estrategia-c-level",
        "asset_type": "post",
        "status": "published",
        "visibility": "public",
        "title_es": "Framework Cuantitativo de Porter y Estrategia C-Level",
        "title_en": "Quantitative Porter Framework and C-Level Strategy",
        "publish_date": "2026-09-20",
        "last_modified_es": "2026-11-10",
        "last_modified_en": "2026-09-15",
        "language_parity": "outdated_en",
        "category": "Estrategia y Operaciones",
        "version": "v1.0.0",
        "release_type": "minor",
        "word_count_es": 3200,
        "word_count_en": 2900,
        "reading_time_min": 16,
        "seo_audit": {"score_0_100": 80},
        "freshness_status": "fresh",
        "related_app": "lifeops",
        "related_kit": "pack-estrategia-c-level",
        "price": "49€",
        "sample_views": 1420,
        "sample_users": 980,
        "sample_eng_sec": 234.5,
        "sample_clicks": 295,
        "sample_impr": 4400,
        "sample_ctr": 6.70,
        "sample_pos": 4.8
    },
    {
        "id": "matriz-riesgos-amfe-fmea",
        "asset_type": "post",
        "status": "published",
        "visibility": "public",
        "title_es": "Matriz de Riesgos AMFE (FMEA) Cuantitativa en Proyectos",
        "title_en": "Quantitative FMEA Risk Matrix in Engineering Projects",
        "publish_date": "2026-10-08",
        "last_modified_es": "2026-10-08",
        "last_modified_en": "2026-10-08",
        "language_parity": "complete",
        "category": "Estrategia y Operaciones",
        "version": "v1.0.0",
        "release_type": "patch",
        "word_count_es": 2100,
        "word_count_en": 2050,
        "reading_time_min": 11,
        "seo_audit": {"score_0_100": 65},
        "freshness_status": "fresh",
        "related_app": "",
        "related_kit": "pack-amfe",
        "price": "19€",
        "sample_views": 680,
        "sample_users": 510,
        "sample_eng_sec": 195.0,
        "sample_clicks": 118,
        "sample_impr": 6200,
        "sample_ctr": 1.90,
        "sample_pos": 9.4
    },
    {
        "id": "ada-lovelace-pioneros-computacion",
        "asset_type": "post",
        "status": "published",
        "visibility": "public",
        "title_es": "Ada Lovelace y los Cimientos de la Ingeniería de Software",
        "title_en": "Ada Lovelace and the Foundations of Software Engineering",
        "publish_date": "2026-10-14",
        "last_modified_es": "2026-10-14",
        "last_modified_en": "2026-10-14",
        "language_parity": "complete",
        "category": "Pioneros y Referentes",
        "version": "v1.0.0",
        "release_type": "minor",
        "word_count_es": 2400,
        "word_count_en": 2320,
        "reading_time_min": 12,
        "seo_audit": {"score_0_100": 90},
        "freshness_status": "fresh",
        "related_app": "",
        "related_kit": "",
        "price": "",
        "sample_views": 2450,
        "sample_users": 1840,
        "sample_eng_sec": 288.0,
        "sample_clicks": 690,
        "sample_impr": 9100,
        "sample_ctr": 7.58,
        "sample_pos": 2.9
    },
    {
        "id": "paradoja-productividad-ia-equipos",
        "asset_type": "post",
        "status": "scheduled",
        "visibility": "public",
        "title_es": "La Paradoja de la Productividad IA en Equipos Híbridos",
        "title_en": "The AI Productivity Paradox in Hybrid Engineering Teams",
        "publish_date": "2026-11-29",
        "last_modified_es": "2026-11-12",
        "last_modified_en": "2026-11-12",
        "language_parity": "complete",
        "category": "Cultura Tech y Media",
        "version": "v1.0.0",
        "release_type": "minor",
        "word_count_es": 2250,
        "word_count_en": 2190,
        "reading_time_min": 11,
        "seo_audit": {"score_0_100": 90},
        "freshness_status": "fresh",
        "related_app": "",
        "related_kit": "pack-pulse",
        "price": "19€",
        "sample_views": 0,
        "sample_users": 0,
        "sample_eng_sec": 0.0,
        "sample_clicks": 0,
        "sample_impr": 0,
        "sample_ctr": 0.0,
        "sample_pos": 0.0
    },
    {
        "id": "unit-economics-startups-saas-b2b",
        "asset_type": "post",
        "status": "review",
        "visibility": "public",
        "title_es": "Unit Economics y Regla del 40 para Startups SaaS B2B",
        "title_en": "Unit Economics and the Rule of 40 for B2B SaaS Startups",
        "publish_date": "2026-12-03",
        "last_modified_es": "2026-11-13",
        "last_modified_en": "2026-11-13",
        "language_parity": "complete",
        "category": "Startups",
        "version": "v0.9.0",
        "release_type": "minor",
        "word_count_es": 2700,
        "word_count_en": 2610,
        "reading_time_min": 14,
        "seo_audit": {"score_0_100": 85},
        "freshness_status": "fresh",
        "related_app": "",
        "related_kit": "pack-startups-saas",
        "price": "19€",
        "sample_views": 0,
        "sample_users": 0,
        "sample_eng_sec": 0.0,
        "sample_clicks": 0,
        "sample_impr": 0,
        "sample_ctr": 0.0,
        "sample_pos": 0.0
    },
    {
        "id": "agentes-ia-automatizacion-sops",
        "asset_type": "post",
        "status": "draft",
        "visibility": "public",
        "title_es": "Arquitectura de Agentes Autónomos para Ejecución de SOPs",
        "title_en": "Autonomous AI Agent Architecture for Standard Operating Procedures",
        "publish_date": "2026-12-10",
        "last_modified_es": "2026-11-11",
        "last_modified_en": "",
        "language_parity": "missing_en",
        "category": "IA, Ingeniería y Proyectos",
        "version": "v0.4.0",
        "release_type": "minor",
        "word_count_es": 1950,
        "word_count_en": 0,
        "reading_time_min": 10,
        "seo_audit": {"score_0_100": 70},
        "freshness_status": "fresh",
        "related_app": "obs-management",
        "related_kit": "",
        "price": "",
        "sample_views": 0,
        "sample_users": 0,
        "sample_eng_sec": 0.0,
        "sample_clicks": 0,
        "sample_impr": 0,
        "sample_ctr": 0.0,
        "sample_pos": 0.0
    },
    {
        "id": "optimizacion-flujo-caja-pymes",
        "asset_type": "post",
        "status": "idea",
        "visibility": "private",
        "title_es": "Modelo de Optimización Lineal de Cash Flow para Scaleups",
        "title_en": "Linear Optimization Model for Cash Flow in Tech Scaleups",
        "publish_date": "",
        "last_modified_es": "2026-11-09",
        "last_modified_en": "",
        "language_parity": "missing_en",
        "category": "Startups",
        "version": "v0.4.0",
        "release_type": "patch",
        "word_count_es": 0,
        "word_count_en": 0,
        "reading_time_min": 0,
        "seo_audit": {"score_0_100": 40},
        "freshness_status": "review_needed",
        "related_app": "",
        "related_kit": "",
        "price": "",
        "sample_views": 0,
        "sample_users": 0,
        "sample_eng_sec": 0.0,
        "sample_clicks": 0,
        "sample_impr": 0,
        "sample_ctr": 0.0,
        "sample_pos": 0.0
    },
    {
        "id": "datalaria-pulse-web-app",
        "asset_type": "app",
        "status": "published",
        "visibility": "public",
        "title_es": "Datalaria Pulse: Content Ops Cockpit v1.0.0",
        "title_en": "Datalaria Pulse: Content Ops Cockpit v1.0.0",
        "publish_date": "2026-11-18",
        "last_modified_es": "2026-11-18",
        "last_modified_en": "2026-11-18",
        "language_parity": "complete",
        "category": "IA, Ingeniería y Proyectos",
        "version": "v1.0.0",
        "release_type": "major",
        "word_count_es": 1400,
        "word_count_en": 1380,
        "reading_time_min": 7,
        "seo_audit": {"score_0_100": 100},
        "freshness_status": "fresh",
        "related_app": "pulse",
        "related_kit": "pack-pulse",
        "price": "19€",
        "sample_views": 1620,
        "sample_users": 1150,
        "sample_eng_sec": 305.0,
        "sample_clicks": 380,
        "sample_impr": 4100,
        "sample_ctr": 9.27,
        "sample_pos": 2.8
    },
    {
        "id": "pack-pulse-content-ops-kit",
        "asset_type": "kit",
        "status": "published",
        "visibility": "public",
        "title_es": "Datalaria Pulse: Content Ops & Notion Migration Kit (19€)",
        "title_en": "Datalaria Pulse: Content Ops & Notion Migration Kit (19€)",
        "publish_date": "2026-11-18",
        "last_modified_es": "2026-11-18",
        "last_modified_en": "2026-11-18",
        "language_parity": "complete",
        "category": "Estrategia y Operaciones",
        "version": "v1.0.0",
        "release_type": "major",
        "word_count_es": 1200,
        "word_count_en": 1200,
        "reading_time_min": 6,
        "seo_audit": {"score_0_100": 100},
        "freshness_status": "fresh",
        "related_app": "pulse",
        "related_kit": "pack-pulse",
        "price": "19€",
        "sample_views": 1180,
        "sample_users": 890,
        "sample_eng_sec": 290.0,
        "sample_clicks": 260,
        "sample_impr": 3400,
        "sample_ctr": 7.65,
        "sample_pos": 3.6
    }
]


def style_header_row(ws, row_idx: int, col_count: int):
    for col in range(1, col_count + 1):
        cell = ws.cell(row=row_idx, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
    ws.row_dimensions[row_idx].height = 28


def auto_fit_columns(ws, min_width: int = 12, max_width: int = 50):
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if "\n" in val_str:
                val_str = max(val_str.split("\n"), key=len)
            max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, min_width), max_width)


def generate_pulse_workbook(
    assets: List[Dict[str, Any]],
    metrics: Optional[Dict[str, Any]] = None,
    is_template: bool = False,
    lang: str = "es"
) -> openpyxl.Workbook:
    """
    Generador centralizado del libro Excel para Datalaria Pulse.
    Produce un libro estructurado de 6 hojas con compatibilidad universal Excel 2016+ / Google Sheets (INV-PULSE-5):
      - Cero macros VBA.
      - Tablas nativas Excel con filtros y ordenación por columna.
      - Fórmulas dinámicas para Kanban, Métricas y Dashboard sin duplicar escritura manual.
      - Paneles congelados (freeze_panes) y pestañas coloreadas temáticamente.
    """
    metrics = metrics or {}
    lang = lang.lower()
    is_es = lang == "es"

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Eliminar hoja por defecto

    # Nombres de hojas canónicos según idioma
    sheet_intro = "Instrucciones" if is_es else "Instructions"
    sheet_tax = "Taxonomía" if is_es else "Taxonomy"
    sheet_act = "Activos" if is_es else "Assets"
    sheet_kanban = "Kanban"
    sheet_met = "Métricas" if is_es else "Metrics"
    sheet_dash = "Dashboard"

    # ==============================================================================
    # HOJA 1: Instrucciones / Instructions (Pestaña Azul 0284C7)
    # ==============================================================================
    ws_intro = wb.create_sheet(title=sheet_intro)
    ws_intro.sheet_properties.tabColor = "0284C7"
    ws_intro.views.sheetView[0].showGridLines = True

    title_text = "DATALARIA PULSE — CONTENT OPS MASTER TRACKER"
    sub_text = (
        "Sistema Operativo de Gobierno Editorial, Paridad Bilingüe y Retorno de Contenido"
        if is_es
        else "Operating System for Editorial Governance, Bilingual Parity & Content ROI"
    )
    ws_intro.cell(row=2, column=2, value=title_text).font = Font(name=FONT_FAMILY, size=16, bold=True, color="0F172A")
    ws_intro.cell(row=3, column=2, value=sub_text).font = Font(name=FONT_FAMILY, size=11, italic=True, color="64748B")

    if is_es:
        intro_paragraphs = [
            ("Objetivo del Tracker:", "Gestionar en un único libro auditable todos tus activos (Posts, Apps, Kits), controlando la paridad bilingüe, salud SEO, estado de frescura y métricas de tráfico sin depender de herramientas externas como Notion."),
            (f"Hoja '{sheet_act}':", "Tabla maestra estructurada con filtros, ordenación y validaciones desplegables. Única fuente de verdad editorial (fórmulas automáticas de lectura y tráfico)."),
            (f"Hoja '{sheet_kanban}':", "Tablero visual en tiempo real. Al cambiar el estado de cualquier activo en 'Activos', la tarjeta se mueve automáticamente sin necesidad de macros."),
            (f"Hoja '{sheet_met}':", "Consolidación analítica de Google Analytics 4 y Search Console. El Tipo y el Título se autocompletan al seleccionar el ID del activo."),
            (f"Hoja '{sheet_dash}':", "Cuadro de mando ejecutivo con KPIs generales, desglose por tipo de activo, salud por las 5 categorías canónicas y radar de alertas accionables."),
            (f"Hoja '{sheet_tax}':", "Catálogo maestro de valores válidos (Tipos, Estados, Visibilidad, Paridad, Frescura, Categorías, Releases) que alimenta los desplegables.")
        ]
        workflow_heading = "FLUJO DE TRABAJO RECOMENDADO EN 3 PASOS"
        workflow_steps = [
            ("Paso 1 · Ingesta Automática:", "Importa tus datos desde Notion con '01_Excel_Templates/notion_power_query_es.m' (o 'migrate_notion.py'), o escanea tu repositorio Markdown con '02_Migration_Scripts/pulse_repo_scanner.py' / 'git_public_json_power_query_es.m'."),
            ("Paso 2 · Gobierno Semanal (Scriba):", f"En la hoja '{sheet_act}', filtra Paridad ('outdated_en' / 'missing_en') para traducir, revisa 'Score SEO < 80' para capturar Quick Wins en Google y detecta posts con alto tráfico sin 'Kit Asociado' ni 'App Asociada'."),
            ("Paso 3 · Métricas y Control Visual:", f"Actualiza la hoja '{sheet_met}' con tus datos de GA4/GSC (se autocompletan Tipo y Título), valida tus flujos pendientes en '{sheet_kanban}' y supervisa los KPIs ejecutivos en tiempo real desde '{sheet_dash}' (fórmulas universales Excel 2016+/Sheets).")
        ]
    else:
        intro_paragraphs = [
            ("Tracker Goal:", "Manage all your assets (Posts, Apps, Kits) in a single auditable workbook, governing bilingual parity, SEO health, freshness status, and traffic metrics with zero external tool dependencies."),
            (f"'{sheet_act}' Sheet:", "Structured master table with column filters, sorting, and dropdown validations. Single source of truth (automatic reading time and traffic lookup formulas)."),
            (f"'{sheet_kanban}' Sheet:", "Real-time visual board. When you change any asset's status in 'Assets', cards update automatically across columns with zero macros."),
            (f"'{sheet_met}' Sheet:", "Quantitative consolidation for GA4 and Search Console. Asset Type and Title auto-populate upon selecting the Asset ID."),
            (f"'{sheet_dash}' Sheet:", "Executive scorecard with core KPIs, breakdown by asset type, health across the 5 canonical categories, and actionable alerts radar."),
            (f"'{sheet_tax}' Sheet:", "Master catalog of valid enum values (Types, Statuses, Visibility, Parity, Freshness, Categories, Releases) powering dropdowns.")
        ]
        workflow_heading = "RECOMMENDED 3-STEP WORKFLOW"
        workflow_steps = [
            ("Step 1 · Automated Ingestion:", "Import your database from Notion via '01_Excel_Templates/notion_power_query_en.m' (or 'migrate_notion.py'), or scan your Markdown repo via '02_Migration_Scripts/pulse_repo_scanner.py' / 'git_public_json_power_query_en.m'."),
            ("Step 2 · Weekly Governance (Scriba):", f"In '{sheet_act}', filter Parity ('outdated_en' / 'missing_en') to translate, review 'SEO Score < 80' to capture Google Quick Wins, and detect high-traffic posts lacking a 'Related Kit' or 'Related App'."),
            ("Step 3 · Metrics & Visual Monitoring:", f"Update '{sheet_met}' with your GA4/GSC numbers (Type and Title auto-populate), verify active pipelines in '{sheet_kanban}', and monitor real-time executive KPIs in '{sheet_dash}' (universal Excel 2016+/Sheets formulas).")
        ]

    r = 5
    for title, desc in intro_paragraphs:
        c_title = ws_intro.cell(row=r, column=2, value=title)
        c_title.font = Font(name=FONT_FAMILY, size=11, bold=True, color="1E293B")
        c_title.alignment = Alignment(vertical="top", wrap_text=True)
        c_desc = ws_intro.cell(row=r, column=3, value=desc)
        c_desc.font = Font(name=FONT_FAMILY, size=10.5, color="334155")
        c_desc.alignment = Alignment(vertical="top", wrap_text=True)
        ws_intro.row_dimensions[r].height = 30
        r += 1

    r += 1
    ws_intro.cell(row=r, column=2, value=workflow_heading).font = Font(name=FONT_FAMILY, size=13, bold=True, color="047857")
    ws_intro.row_dimensions[r].height = 24
    r += 1

    for w_title, w_desc in workflow_steps:
        c_wt = ws_intro.cell(row=r, column=2, value=w_title)
        c_wt.font = Font(name=FONT_FAMILY, size=10.5, bold=True, color="0F172A")
        c_wt.fill = ZEBRA_FILL
        c_wt.border = THIN_BORDER
        c_wt.alignment = Alignment(vertical="top", wrap_text=True)

        c_wd = ws_intro.cell(row=r, column=3, value=w_desc)
        c_wd.font = Font(name=FONT_FAMILY, size=10, color="334155")
        c_wd.fill = ZEBRA_FILL
        c_wd.border = THIN_BORDER
        c_wd.alignment = Alignment(vertical="top", wrap_text=True)
        ws_intro.row_dimensions[r].height = 38
        r += 1

    ws_intro.column_dimensions["B"].width = 30
    ws_intro.column_dimensions["C"].width = 92

    # ==============================================================================
    # HOJA 2: Taxonomía / Taxonomy (Pestaña Azul 0284C7)
    # ==============================================================================
    ws_tax = wb.create_sheet(title=sheet_tax)
    ws_tax.sheet_properties.tabColor = "0284C7"
    ws_tax.views.sheetView[0].showGridLines = True

    if is_es:
        tax_headers = ["Tipo de Activo", "Estado", "Visibilidad", "Paridad Bilingüe", "Estado Frescura", "Categoría Canónica", "Tipo Release"]
    else:
        tax_headers = ["Asset Type", "Status", "Visibility", "Language Parity", "Freshness Status", "Canonical Category", "Release Type"]

    for c_idx, th in enumerate(tax_headers, 1):
        ws_tax.cell(row=1, column=c_idx, value=th)
    style_header_row(ws_tax, 1, len(tax_headers))

    tax_data = {
        1: ["POST", "APP", "KIT"],
        2: ["Idea", "Draft", "Review", "Scheduled", "Published"],
        3: ["public", "private"],
        4: ["complete", "missing_es", "missing_en", "outdated_es", "outdated_en"],
        5: ["fresh", "stale", "review_needed"],
        6: [
            "IA, Ingeniería y Proyectos",
            "Estrategia y Operaciones",
            "Startups",
            "Pioneros y Referentes",
            "Cultura Tech y Media"
        ],
        7: ["major", "minor", "patch"]
    }

    max_tax_rows = 1
    for col_idx, values in tax_data.items():
        max_tax_rows = max(max_tax_rows, len(values) + 1)
        for row_idx, val in enumerate(values, 2):
            c = ws_tax.cell(row=row_idx, column=col_idx, value=val)
            c.font = Font(name=FONT_FAMILY, size=10)
            c.border = THIN_BORDER

    # Tabla nativa con filtros y ordenación
    tax_table_name = "TaxonomiaTable" if is_es else "TaxonomyTable"
    tab_tax = Table(displayName=tax_table_name, ref=f"A1:G{max_tax_rows}")
    tab_tax.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws_tax.add_table(tab_tax)
    ws_tax.freeze_panes = "A2"
    auto_fit_columns(ws_tax, min_width=16)

    # ==============================================================================
    # HOJA 3: Activos / Assets (Pestaña Esmeralda 059669)
    # ==============================================================================
    ws_act = wb.create_sheet(title=sheet_act)
    ws_act.sheet_properties.tabColor = "059669"
    ws_act.views.sheetView[0].showGridLines = True

    if is_es:
        headers = [
            "ID", "Tipo", "Estado", "Visibilidad", "Título (ES)", "Título (EN)",
            "Fecha Pub", "Última Mod (ES)", "Última Mod (EN)", "Paridad",
            "Categoría", "Palabras ES", "Palabras EN", "Lectura (min)", "Score SEO",
            "Frescura", "App Asociada", "Kit Asociado", "Precio", "Visitas 30d", "Usuarios 30d",
            "Versión", "Tipo Release"
        ]
    else:
        headers = [
            "ID", "Type", "Status", "Visibility", "Title (ES)", "Title (EN)",
            "Publish Date", "Last Mod (ES)", "Last Mod (EN)", "Parity",
            "Category", "Words ES", "Words EN", "Read Time (min)", "SEO Score",
            "Freshness", "Related App", "Related Kit", "Price", "Views 30d", "Users 30d",
            "Version", "Release Type"
        ]

    for c_idx, h in enumerate(headers, 1):
        ws_act.cell(row=1, column=c_idx, value=h)
    style_header_row(ws_act, 1, len(headers))

    # Reglas de validación desplegables (DataValidation) alimentadas por Taxonomía
    dv_type = DataValidation(type="list", formula1=f"='{sheet_tax}'!$A$2:$A$4", allow_blank=True)
    ws_act.add_data_validation(dv_type)
    dv_type.add("B2:B500")

    dv_status = DataValidation(type="list", formula1=f"='{sheet_tax}'!$B$2:$B$6", allow_blank=True)
    ws_act.add_data_validation(dv_status)
    dv_status.add("C2:C500")

    dv_vis = DataValidation(type="list", formula1=f"='{sheet_tax}'!$C$2:$C$3", allow_blank=True)
    ws_act.add_data_validation(dv_vis)
    dv_vis.add("D2:D500")

    dv_parity = DataValidation(type="list", formula1=f"='{sheet_tax}'!$D$2:$D$6", allow_blank=True)
    ws_act.add_data_validation(dv_parity)
    dv_parity.add("J2:J500")

    dv_cat = DataValidation(type="list", formula1=f"='{sheet_tax}'!$F$2:$F$6", allow_blank=True)
    ws_act.add_data_validation(dv_cat)
    dv_cat.add("K2:K500")

    dv_fresh = DataValidation(type="list", formula1=f"='{sheet_tax}'!$E$2:$E$4", allow_blank=True)
    ws_act.add_data_validation(dv_fresh)
    dv_fresh.add("P2:P500")

    dv_rel = DataValidation(type="list", formula1=f"='{sheet_tax}'!$G$2:$G$4", allow_blank=True)
    ws_act.add_data_validation(dv_rel)
    dv_rel.add("W2:W500")

    row_num = 2
    for a in assets:
        aid = a["id"]
        
        ws_act.cell(row=row_num, column=1, value=aid)
        ws_act.cell(row=row_num, column=2, value=a.get("asset_type", "post").upper())
        ws_act.cell(row=row_num, column=3, value=a.get("status", "idea").capitalize())
        ws_act.cell(row=row_num, column=4, value=a.get("visibility", "public"))
        ws_act.cell(row=row_num, column=5, value=a.get("title_es") or "")
        ws_act.cell(row=row_num, column=6, value=a.get("title_en") or "")
        ws_act.cell(row=row_num, column=7, value=str(a.get("publish_date") or ""))
        ws_act.cell(row=row_num, column=8, value=str(a.get("last_modified_es") or "")[:10])
        ws_act.cell(row=row_num, column=9, value=str(a.get("last_modified_en") or "")[:10])
        
        # Paridad con estilo badge
        p_cell = ws_act.cell(row=row_num, column=10, value=a.get("language_parity", "complete"))
        if p_cell.value == "complete":
            p_cell.fill = BADGE_COMPLETE
        elif "outdated" in str(p_cell.value):
            p_cell.fill = BADGE_WARN
        else:
            p_cell.fill = BADGE_ALERT

        ws_act.cell(row=row_num, column=11, value=a.get("category", "General"))
        ws_act.cell(row=row_num, column=12, value=a.get("word_count_es", 0))
        ws_act.cell(row=row_num, column=13, value=a.get("word_count_en", 0))

        # Col 14: Lectura en minutos calculada por fórmula universal
        c_read = ws_act.cell(row=row_num, column=14, value=f"=IF(MAX(L{row_num},M{row_num})=0,0,MAX(1,ROUND(MAX(L{row_num},M{row_num})/200,0)))")
        c_read.alignment = Alignment(horizontal="right")
        
        # Col 15: SEO Score
        seo_val = a.get("seo_audit", {}).get("score_0_100", 0)
        s_cell = ws_act.cell(row=row_num, column=15, value=seo_val)
        if seo_val >= 80:
            s_cell.fill = BADGE_COMPLETE
        elif seo_val >= 60:
            s_cell.fill = BADGE_WARN
        else:
            s_cell.fill = BADGE_ALERT

        ws_act.cell(row=row_num, column=16, value=a.get("freshness_status", "fresh"))
        ws_act.cell(row=row_num, column=17, value=a.get("related_app") or "")
        ws_act.cell(row=row_num, column=18, value=a.get("related_kit") or "")
        ws_act.cell(row=row_num, column=19, value=a.get("price") or "")

        # Cols 20 & 21: Visitas y Usuarios 30d vinculados a Métricas vía INDEX/MATCH (cero duplicación)
        c_views = ws_act.cell(row=row_num, column=20, value=f'=IF(A{row_num}="","",IFERROR(INDEX(\'{sheet_met}\'!$C$2:$C$500,MATCH(A{row_num},\'{sheet_met}\'!$A$2:$A$500,0)),0))')
        c_views.alignment = Alignment(horizontal="right")
        c_users = ws_act.cell(row=row_num, column=21, value=f'=IF(A{row_num}="","",IFERROR(INDEX(\'{sheet_met}\'!$D$2:$D$500,MATCH(A{row_num},\'{sheet_met}\'!$A$2:$A$500,0)),0))')
        c_users.alignment = Alignment(horizontal="right")

        ws_act.cell(row=row_num, column=22, value=a.get("version") or "v1.0.0")
        ws_act.cell(row=row_num, column=23, value=a.get("release_type") or "")

        for col_i in range(1, len(headers) + 1):
            c = ws_act.cell(row=row_num, column=col_i)
            c.font = Font(name=FONT_FAMILY, size=10)
            c.border = THIN_BORDER
            if row_num % 2 == 1 and not c.fill.start_color.rgb:
                c.fill = ZEBRA_FILL

        ws_act.row_dimensions[row_num].height = 20
        row_num += 1

    max_act_rows = max(row_num - 1, 2)

    # Columnas auxiliares para Kanban dinámico (Y:AC -> Cols 25..29)
    kanban_helper_headers = ["_K_Idea", "_K_Draft", "_K_Review", "_K_Scheduled", "_K_Published"]
    for idx, kh in enumerate(kanban_helper_headers, 25):
        c_kh = ws_act.cell(row=1, column=idx, value=kh)
        c_kh.font = Font(name=FONT_FAMILY, size=8, color="94A3B8")
        ws_act.column_dimensions[get_column_letter(idx)].width = 9

    # Pre-cargar fórmulas auxiliares en el rango 2..500
    helper_limit = max(max_act_rows + 1, 50)
    for hr in range(2, helper_limit + 1):
        ws_act.cell(row=hr, column=25, value=f'=IF($C{hr}="Idea",COUNTIF($C$2:$C{hr},"Idea"),"")').font = Font(name=FONT_FAMILY, size=8, color="94A3B8")
        ws_act.cell(row=hr, column=26, value=f'=IF($C{hr}="Draft",COUNTIF($C$2:$C{hr},"Draft"),"")').font = Font(name=FONT_FAMILY, size=8, color="94A3B8")
        ws_act.cell(row=hr, column=27, value=f'=IF($C{hr}="Review",COUNTIF($C$2:$C{hr},"Review"),"")').font = Font(name=FONT_FAMILY, size=8, color="94A3B8")
        ws_act.cell(row=hr, column=28, value=f'=IF($C{hr}="Scheduled",COUNTIF($C$2:$C{hr},"Scheduled"),"")').font = Font(name=FONT_FAMILY, size=8, color="94A3B8")
        ws_act.cell(row=hr, column=29, value=f'=IF($C{hr}="Published",COUNTIF($C$2:$C{hr},"Published"),"")').font = Font(name=FONT_FAMILY, size=8, color="94A3B8")

    # Tabla nativa estructurada
    act_table_name = "ActivosTable" if is_es else "AssetsTable"
    tab_act = Table(displayName=act_table_name, ref=f"A1:W{max_act_rows}")
    tab_act.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws_act.add_table(tab_act)
    ws_act.freeze_panes = "B2"
    auto_fit_columns(ws_act)

    # ==============================================================================
    # HOJA 4: Tablero Kanban (Pestaña Esmeralda 059669)
    # ==============================================================================
    ws_kanban = wb.create_sheet(title=sheet_kanban)
    ws_kanban.sheet_properties.tabColor = "059669"
    ws_kanban.views.sheetView[0].showGridLines = True

    if is_es:
        kanban_cols = ["Idea (Backlog)", "Borrador (Draft)", "En Revisión (Review)", "Programado (Scheduled)", "Publicado (Live)"]
    else:
        kanban_cols = ["Idea (Backlog)", "Draft", "In Review", "Scheduled", "Published (Live)"]

    for c_i, k_title in enumerate(kanban_cols, 1):
        ws_kanban.cell(row=1, column=c_i, value=k_title)
    style_header_row(ws_kanban, 1, len(kanban_cols))

    # Fila 2: Contadores dinámicos en vivo
    status_keys = ["Idea", "Draft", "Review", "Scheduled", "Published"]
    for c_idx, st_val in enumerate(status_keys, 1):
        cnt_cell = ws_kanban.cell(row=2, column=c_idx, value=f'="Total: " & COUNTIF(\'{sheet_act}\'!$C$2:$C$500, "{st_val}")')
        cnt_cell.font = Font(name=FONT_FAMILY, size=10, bold=True, color="047857")
        cnt_cell.fill = ZEBRA_FILL
        cnt_cell.border = THIN_BORDER
        cnt_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_kanban.row_dimensions[2].height = 22

    # Filas 3..35: Fórmulas dinámicas que alimentan las tarjetas en vivo
    helper_cols = ["Y", "Z", "AA", "AB", "AC"]
    for r_idx in range(3, 36):
        match_idx = r_idx - 2
        for c_idx in range(1, 6):
            k_col = helper_cols[c_idx - 1]
            if is_es:
                k_formula = (
                    f'=IFERROR("["&INDEX(\'{sheet_act}\'!$B$2:$B$500,MATCH({match_idx},\'{sheet_act}\'!${k_col}$2:${k_col}$500,0))&"] "'
                    f'&INDEX(\'{sheet_act}\'!$E$2:$E$500,MATCH({match_idx},\'{sheet_act}\'!${k_col}$2:${k_col}$500,0))'
                    f'&" ("&INDEX(\'{sheet_act}\'!$A$2:$A$500,MATCH({match_idx},\'{sheet_act}\'!${k_col}$2:${k_col}$500,0))&")","")'
                )
            else:
                k_formula = (
                    f'=IFERROR("["&INDEX(\'{sheet_act}\'!$B$2:$B$500,MATCH({match_idx},\'{sheet_act}\'!${k_col}$2:${k_col}$500,0))&"] "'
                    f'&IF(INDEX(\'{sheet_act}\'!$F$2:$F$500,MATCH({match_idx},\'{sheet_act}\'!${k_col}$2:${k_col}$500,0))<>"","'
                    f'INDEX(\'{sheet_act}\'!$F$2:$F$500,MATCH({match_idx},\'{sheet_act}\'!${k_col}$2:${k_col}$500,0)),'
                    f'INDEX(\'{sheet_act}\'!$E$2:$E$500,MATCH({match_idx},\'{sheet_act}\'!${k_col}$2:${k_col}$500,0)))'
                    f'&" ("&INDEX(\'{sheet_act}\'!$A$2:$A$500,MATCH({match_idx},\'{sheet_act}\'!${k_col}$2:${k_col}$500,0))&")","")'
                )
            c = ws_kanban.cell(row=r_idx, column=c_idx, value=k_formula)
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.font = Font(name=FONT_FAMILY, size=9)
            c.border = THIN_BORDER
        ws_kanban.row_dimensions[r_idx].height = 36

    for c_i in range(1, len(kanban_cols) + 1):
        ws_kanban.column_dimensions[get_column_letter(c_i)].width = 34
    ws_kanban.freeze_panes = "A3"

    # ==============================================================================
    # HOJA 5: Métricas / Metrics (Pestaña Esmeralda 059669)
    # ==============================================================================
    ws_met = wb.create_sheet(title=sheet_met)
    ws_met.sheet_properties.tabColor = "059669"
    ws_met.views.sheetView[0].showGridLines = True

    if is_es:
        met_headers = [
            "ID Activo", "Tipo", "Visitas 30d", "Usuarios Únicos 30d",
            "Tiempo Medio (s)", "Clics GSC", "Impresiones GSC", "Título Activo"
        ]
    else:
        met_headers = [
            "Asset ID", "Type", "Views 30d", "Unique Users 30d",
            "Avg Engagement (s)", "GSC Clicks", "GSC Impressions", "Asset Title"
        ]

    for c_i, mh in enumerate(met_headers, 1):
        ws_met.cell(row=1, column=c_i, value=mh)
    style_header_row(ws_met, 1, len(met_headers))

    # Regla de validación desplegable para seleccionar ID Activo
    dv_aid = DataValidation(type="list", formula1=f"='{sheet_act}'!$A$2:$A$500", allow_blank=True)
    ws_met.add_data_validation(dv_aid)
    dv_aid.add("A2:A500")

    r_num = 2
    for a in assets:
        aid = a["id"]
        m = metrics.get(aid, {})
        ws_met.cell(row=r_num, column=1, value=aid)
        
        # Col 2: Tipo autocompletado por fórmula
        c_tipo = ws_met.cell(row=r_num, column=2, value=f'=IF(A{r_num}="","",IFERROR(INDEX(\'{sheet_act}\'!$B$2:$B$500,MATCH(A{r_num},\'{sheet_act}\'!$A$2:$A$500,0)),""))')
        c_tipo.alignment = Alignment(horizontal="center")

        ws_met.cell(row=r_num, column=3, value=m.get("ga4_views_30d", 0))
        ws_met.cell(row=r_num, column=4, value=m.get("ga4_users_30d", 0))
        ws_met.cell(row=r_num, column=5, value=round(m.get("ga4_engagement_sec", 0.0), 1))
        ws_met.cell(row=r_num, column=6, value=m.get("gsc_clicks_30d", 0))
        ws_met.cell(row=r_num, column=7, value=m.get("gsc_impressions_30d", 0))

        # Col 8: Título Activo autocompletado por fórmula
        if is_es:
            ws_met.cell(row=r_num, column=8, value=f'=IF(A{r_num}="","",IFERROR(INDEX(\'{sheet_act}\'!$E$2:$E$500,MATCH(A{r_num},\'{sheet_act}\'!$A$2:$A$500,0)),""))')
        else:
            ws_met.cell(
                row=r_num,
                column=8,
                value=f'=IF(A{r_num}="","",IFERROR(IF(INDEX(\'{sheet_act}\'!$F$2:$F$500,MATCH(A{r_num},\'{sheet_act}\'!$A$2:$A$500,0))<>"","'
                      f'INDEX(\'{sheet_act}\'!$F$2:$F$500,MATCH(A{r_num},\'{sheet_act}\'!$A$2:$A$500,0)),'
                      f'INDEX(\'{sheet_act}\'!$E$2:$E$500,MATCH(A{r_num},\'{sheet_act}\'!$A$2:$A$500,0))),""))'
            )

        for col_i in range(1, len(met_headers) + 1):
            c = ws_met.cell(row=r_num, column=col_i)
            c.font = Font(name=FONT_FAMILY, size=10)
            c.border = THIN_BORDER
            if r_num % 2 == 1:
                c.fill = ZEBRA_FILL
        r_num += 1

    max_met_rows = max(r_num - 1, 2)
    met_table_name = "MetricasTable" if is_es else "MetricsTable"
    tab_met = Table(displayName=met_table_name, ref=f"A1:H{max_met_rows}")
    tab_met.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws_met.add_table(tab_met)
    ws_met.freeze_panes = "B2"
    auto_fit_columns(ws_met)

    # ==============================================================================
    # HOJA 6: Dashboard Ejecutivo (Pestaña Ámbar D97706)
    # ==============================================================================
    ws_dash = wb.create_sheet(title=sheet_dash)
    ws_dash.sheet_properties.tabColor = "D97706"
    ws_dash.views.sheetView[0].showGridLines = True

    dash_title = (
        "CUADRO DE MANDO EDITORIAL (CONTENT OPS)"
        if is_es
        else "EDITORIAL EXECUTIVE DASHBOARD (CONTENT OPS)"
    )
    ws_dash.cell(row=2, column=2, value=dash_title).font = Font(name=FONT_FAMILY, size=14, bold=True, color="0F172A")

    # Bloque 1: KPIs Clave de Cartera (filas 4..9)
    if is_es:
        kpis = [
            ("Total Activos Catalogados", f"=COUNTA('{sheet_act}'!A2:A{max_act_rows})"),
            ("Artículos Publicados (Live)", f'=COUNTIF(\'{sheet_act}\'!C2:C{max_act_rows}, "Published")'),
            ("Activos Programados (Scheduled)", f'=COUNTIF(\'{sheet_act}\'!C2:C{max_act_rows}, "Scheduled")'),
            ("Paridad Bilingüe Completa", f'=COUNTIF(\'{sheet_act}\'!J2:J{max_act_rows}, "complete")'),
            ("Total Visitas 30d", f"=SUM('{sheet_act}'!T2:T{max_act_rows})"),
            ("Total Usuarios 30d", f"=SUM('{sheet_act}'!U2:U{max_act_rows})")
        ]
    else:
        kpis = [
            ("Total Cataloged Assets", f"=COUNTA('{sheet_act}'!A2:A{max_act_rows})"),
            ("Published Assets (Live)", f'=COUNTIF(\'{sheet_act}\'!C2:C{max_act_rows}, "Published")'),
            ("Scheduled Assets", f'=COUNTIF(\'{sheet_act}\'!C2:C{max_act_rows}, "Scheduled")'),
            ("Complete Language Parity", f'=COUNTIF(\'{sheet_act}\'!J2:J{max_act_rows}, "complete")'),
            ("Total Views 30d", f"=SUM('{sheet_act}'!T2:T{max_act_rows})"),
            ("Total Users 30d", f"=SUM('{sheet_act}'!U2:U{max_act_rows})")
        ]

    r_kpi = 4
    for kpi_title, kpi_formula in kpis:
        c_lbl = ws_dash.cell(row=r_kpi, column=2, value=kpi_title)
        c_lbl.font = Font(name=FONT_FAMILY, size=10.5, bold=True, color="475569")
        c_lbl.border = THIN_BORDER
        c_val = ws_dash.cell(row=r_kpi, column=4, value=kpi_formula)
        c_val.font = Font(name=FONT_FAMILY, size=11.5, bold=True, color="0F172A")
        c_val.alignment = Alignment(horizontal="right")
        c_val.border = THIN_BORDER
        ws_dash.row_dimensions[r_kpi].height = 24
        r_kpi += 1

    # Bloque 2: Distribución por Tipo de Activo (filas 11..15)
    sec2_title = "DISTRIBUCIÓN POR TIPO DE ACTIVO" if is_es else "PORTFOLIO BREAKDOWN BY ASSET TYPE"
    ws_dash.cell(row=11, column=2, value=sec2_title).font = Font(name=FONT_FAMILY, size=11, bold=True, color="047857")
    
    col_type_lbl = "Tipo de Activo" if is_es else "Asset Type"
    col_count_lbl = "Nº Activos" if is_es else "Count"
    col_views_lbl = "Visitas 30d" if is_es else "Views 30d"
    
    ws_dash.cell(row=12, column=2, value=col_type_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=12, column=2).fill = HEADER_FILL
    ws_dash.cell(row=12, column=3, value=col_count_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=12, column=3).fill = HEADER_FILL
    ws_dash.cell(row=12, column=4, value=col_views_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=12, column=4).fill = HEADER_FILL

    for idx, atype in enumerate(["POST", "APP", "KIT"], 13):
        ws_dash.cell(row=idx, column=2, value=atype).font = Font(name=FONT_FAMILY, size=10, bold=True)
        ws_dash.cell(row=idx, column=2).border = THIN_BORDER
        c_c = ws_dash.cell(row=idx, column=3, value=f'=COUNTIF(\'{sheet_act}\'!$B$2:$B${max_act_rows}, "{atype}")')
        c_c.alignment = Alignment(horizontal="right")
        c_c.font = Font(name=FONT_FAMILY, size=10)
        c_c.border = THIN_BORDER
        c_v = ws_dash.cell(row=idx, column=4, value=f'=SUMIF(\'{sheet_act}\'!$B$2:$B${max_act_rows}, "{atype}", \'{sheet_act}\'!$T$2:$T${max_act_rows})')
        c_v.alignment = Alignment(horizontal="right")
        c_v.font = Font(name=FONT_FAMILY, size=10)
        c_v.border = THIN_BORDER

    # Bloque 3: Salud por Categoría Canónica (filas 17..23)
    sec3_title = "SALUD POR CATEGORÍA CANÓNICA" if is_es else "HEALTH BY CANONICAL CATEGORY"
    ws_dash.cell(row=17, column=2, value=sec3_title).font = Font(name=FONT_FAMILY, size=11, bold=True, color="047857")

    col_cat_lbl = "Categoría Canónica" if is_es else "Canonical Category"
    col_seo_lbl = "Score SEO Medio" if is_es else "Avg SEO Score"

    ws_dash.cell(row=18, column=2, value=col_cat_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=18, column=2).fill = HEADER_FILL
    ws_dash.cell(row=18, column=3, value=col_count_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=18, column=3).fill = HEADER_FILL
    ws_dash.cell(row=18, column=4, value=col_views_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=18, column=4).fill = HEADER_FILL
    ws_dash.cell(row=18, column=5, value=col_seo_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=18, column=5).fill = HEADER_FILL

    canonical_cats = [
        "IA, Ingeniería y Proyectos",
        "Estrategia y Operaciones",
        "Startups",
        "Pioneros y Referentes",
        "Cultura Tech y Media"
    ]
    for idx, cname in enumerate(canonical_cats, 19):
        ws_dash.cell(row=idx, column=2, value=cname).font = Font(name=FONT_FAMILY, size=10)
        ws_dash.cell(row=idx, column=2).border = THIN_BORDER
        c_c = ws_dash.cell(row=idx, column=3, value=f'=COUNTIF(\'{sheet_act}\'!$K$2:$K${max_act_rows}, "{cname}")')
        c_c.alignment = Alignment(horizontal="right")
        c_c.font = Font(name=FONT_FAMILY, size=10)
        c_c.border = THIN_BORDER
        c_v = ws_dash.cell(row=idx, column=4, value=f'=SUMIF(\'{sheet_act}\'!$K$2:$K${max_act_rows}, "{cname}", \'{sheet_act}\'!$T$2:$T${max_act_rows})')
        c_v.alignment = Alignment(horizontal="right")
        c_v.font = Font(name=FONT_FAMILY, size=10)
        c_v.border = THIN_BORDER
        c_s = ws_dash.cell(row=idx, column=5, value=f'=IFERROR(ROUND(AVERAGEIF(\'{sheet_act}\'!$K$2:$K${max_act_rows}, "{cname}", \'{sheet_act}\'!$O$2:$O${max_act_rows}), 1), 0)')
        c_s.alignment = Alignment(horizontal="right")
        c_s.font = Font(name=FONT_FAMILY, size=10)
        c_s.border = THIN_BORDER

    # Bloque 4: Radar de Accionables Editoriales (filas 25..30)
    sec4_title = "RADAR DE ACCIONABLES EDITORIALES" if is_es else "EDITORIAL ACTION RADAR"
    ws_dash.cell(row=25, column=2, value=sec4_title).font = Font(name=FONT_FAMILY, size=11, bold=True, color="DC2626")

    col_radar_lbl = "Criterio de Auditoría" if is_es else "Audit Criterion"
    col_alert_lbl = "Alertas Detectadas" if is_es else "Alerts Detected"

    ws_dash.cell(row=26, column=2, value=col_radar_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=26, column=2).fill = HEADER_FILL
    ws_dash.cell(row=26, column=4, value=col_alert_lbl).font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
    ws_dash.cell(row=26, column=4).fill = HEADER_FILL

    if is_es:
        radar_items = [
            ("Brechas de Paridad Bilingüe (missing/outdated)", f'=COUNTIF(\'{sheet_act}\'!$J$2:$J${max_act_rows},"missing_en")+COUNTIF(\'{sheet_act}\'!$J$2:$J${max_act_rows},"outdated_en")+COUNTIF(\'{sheet_act}\'!$J$2:$J${max_act_rows},"missing_es")+COUNTIF(\'{sheet_act}\'!$J$2:$J${max_act_rows},"outdated_es")'),
            ("Quick Wins SEO (Score < 80)", f'=COUNTIFS(\'{sheet_act}\'!$O$2:$O${max_act_rows}, "<80", \'{sheet_act}\'!$O$2:$O${max_act_rows}, ">0")'),
            ("Contenido Desactualizado (stale)", f'=COUNTIF(\'{sheet_act}\'!$P$2:$P${max_act_rows}, "stale")'),
            ("Huérfanos de Monetización (Tráfico >= 1000 sin Kit)", f'=COUNTIFS(\'{sheet_act}\'!$B$2:$B${max_act_rows}, "POST", \'{sheet_act}\'!$C$2:$C${max_act_rows}, "Published", \'{sheet_act}\'!$T$2:$T${max_act_rows}, ">=1000", \'{sheet_act}\'!$R$2:$R${max_act_rows}, "")')
        ]
    else:
        radar_items = [
            ("Bilingual Parity Gaps (missing/outdated)", f'=COUNTIF(\'{sheet_act}\'!$J$2:$J${max_act_rows},"missing_en")+COUNTIF(\'{sheet_act}\'!$J$2:$J${max_act_rows},"outdated_en")+COUNTIF(\'{sheet_act}\'!$J$2:$J${max_act_rows},"missing_es")+COUNTIF(\'{sheet_act}\'!$J$2:$J${max_act_rows},"outdated_es")'),
            ("SEO Quick Wins (Score < 80)", f'=COUNTIFS(\'{sheet_act}\'!$O$2:$O${max_act_rows}, "<80", \'{sheet_act}\'!$O$2:$O${max_act_rows}, ">0")'),
            ("Outdated Content (stale)", f'=COUNTIF(\'{sheet_act}\'!$P$2:$P${max_act_rows}, "stale")'),
            ("Monetization Orphans (Views >= 1000 without Kit)", f'=COUNTIFS(\'{sheet_act}\'!$B$2:$B${max_act_rows}, "POST", \'{sheet_act}\'!$C$2:$C${max_act_rows}, "Published", \'{sheet_act}\'!$T$2:$T${max_act_rows}, ">=1000", \'{sheet_act}\'!$R$2:$R${max_act_rows}, "")')
        ]

    for idx, (crit, form) in enumerate(radar_items, 27):
        ws_dash.cell(row=idx, column=2, value=crit).font = Font(name=FONT_FAMILY, size=10)
        ws_dash.cell(row=idx, column=2).border = THIN_BORDER
        c_a = ws_dash.cell(row=idx, column=4, value=form)
        c_a.alignment = Alignment(horizontal="right")
        c_a.font = Font(name=FONT_FAMILY, size=10.5, bold=True, color="DC2626")
        c_a.border = THIN_BORDER

    ws_dash.column_dimensions["B"].width = 46
    ws_dash.column_dimensions["C"].width = 16
    ws_dash.column_dimensions["D"].width = 20
    ws_dash.column_dimensions["E"].width = 20

    return wb


def build_pulse_excel(is_template: bool = False, lang: str = "es") -> Path:
    """
    Construye y guarda el libro de trabajo Excel.
    Si is_template=True, genera la plantilla comercial del Kit para el idioma solicitado
    (Pulse_Content_Ops_Template_ES.xlsx o Pulse_Content_Ops_Template_EN.xlsx) y un alias compatible.
    Si is_template=False, genera el tracker privado interno en data/pulse/private/Pulse_Private_Tracker.xlsx.
    """
    assets = []
    metrics = {}
    lang = lang.lower()

    if is_template:
        assets = TEMPLATE_EXAMPLE_ASSETS
        metrics = {
            a["id"]: {
                "ga4_views_30d": a["sample_views"],
                "ga4_users_30d": a["sample_users"],
                "ga4_engagement_sec": a["sample_eng_sec"],
                "gsc_clicks_30d": a["sample_clicks"],
                "gsc_impressions_30d": a["sample_impr"],
                "gsc_ctr_pct": a["sample_ctr"],
                "gsc_avg_position": a["sample_pos"]
            }
            for a in TEMPLATE_EXAMPLE_ASSETS
        }
    else:
        if INDEX_PATH.exists():
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                assets = json.load(f)
            if METRICS_PATH.exists():
                with open(METRICS_PATH, "r", encoding="utf-8") as f:
                    metrics = json.load(f)

    wb = generate_pulse_workbook(assets=assets, metrics=metrics, is_template=is_template, lang=lang)

    target_dir = OUTPUT_DIR if is_template else PRIVATE_OUTPUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    if not is_template:
        filename = "Pulse_Private_Tracker.xlsx"
        dest_path = target_dir / filename
        wb.save(dest_path)
    else:
        lang_suffix = lang.upper()
        filename = f"Pulse_Content_Ops_Template_{lang_suffix}.xlsx"
        dest_path = target_dir / filename
        wb.save(dest_path)
        # Mantener alias histórico sin sufijo si es español para retrocompatibilidad
        if lang == "es":
            alias_path = target_dir / "Pulse_Content_Ops_Template.xlsx"
            wb.save(alias_path)

    # Garantizar higiene en packages/pulse/: eliminar cualquier tracker privado residual
    legacy_private = OUTPUT_DIR / "Pulse_Private_Tracker.xlsx"
    if legacy_private.exists():
        legacy_private.unlink()

    print(f"[EXCEL] Libro generado con éxito ({lang.upper()}): {dest_path}")
    return dest_path


if __name__ == "__main__":
    # 1. Tracker privado interno (con datos reales)
    build_pulse_excel(is_template=False, lang="es")
    # 2. Plantillas del Kit comercial (ES & EN)
    build_pulse_excel(is_template=True, lang="es")
    build_pulse_excel(is_template=True, lang="en")
