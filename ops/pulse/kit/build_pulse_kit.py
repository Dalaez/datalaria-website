"""
ops/pulse/kit/build_pulse_kit.py
--------------------------------
Generador Programático del Excel Maestro de Datalaria Pulse.
Especificación técnica formal: SPEC-APP-PULSE (specs/apps/pulse/spec.md) - Hitos 5.4 y 5.6.

Genera dos libros Excel:
1. packages/pulse/Pulse_Private_Tracker.xlsx:
   Tracker privado para Daniel Alaez con el 100% de los datos reales del blog
   (posts, apps, kits, métricas cuantitativas absolutas de GA4/GSC, paridad y frescura).
   ¡Sustituto definitivo e instantáneo de Notion!
2. packages/pulse/Pulse_Content_Ops_Template.xlsx:
   Plantilla universal para el Kit de clientes (con ejemplos, validaciones y fórmulas
   compatibles con Excel 2016/2019/365 y Google Sheets - INV-PULSE-5).
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

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
INDEX_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "metrics.json"
OUTPUT_DIR = ROOT_DIR / "packages" / "pulse"


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

# 5 Ejemplos representativos para la Plantilla del Kit
TEMPLATE_EXAMPLE_ASSETS = [
    {
        "id": "guia-estrategica-c-level-ejemplo",
        "asset_type": "post",
        "status": "published",
        "visibility": "public",
        "title_es": "Guía Cuantitativa de Estrategia para Comités de Dirección (Ejemplo)",
        "title_en": "Quantitative Strategy Guide for Executive Committees (Example)",
        "publish_date": "2026-10-15",
        "last_modified_es": "2026-10-15",
        "last_modified_en": "2026-10-15",
        "language_parity": "complete",
        "category": "Estrategia Empresarial",
        "word_count_es": 3500,
        "word_count_en": 3400,
        "reading_time_min": 17,
        "seo_audit": {"score_0_100": 95},
        "freshness_status": "fresh",
        "related_app": "lifeops",
        "related_kit": "pack-estrategia-c-level",
        "price": "49€",
        "sample_views": 1450,
        "sample_users": 980,
        "sample_eng_sec": 245.5,
        "sample_clicks": 320,
        "sample_impr": 4800,
        "sample_ctr": 6.7,
        "sample_pos": 4.2
    },
    {
        "id": "forecasting-demanda-monte-carlo",
        "asset_type": "post",
        "status": "scheduled",
        "visibility": "public",
        "title_es": "Predicción de Demanda y Simulación de Monte Carlo en Cadena de Suministro",
        "title_en": "Demand Forecasting and Monte Carlo Simulation in Supply Chain",
        "publish_date": "2026-11-20",
        "last_modified_es": "2026-10-25",
        "last_modified_en": "2026-10-25",
        "language_parity": "complete",
        "category": "Operaciones",
        "word_count_es": 2800,
        "word_count_en": 2750,
        "reading_time_min": 14,
        "seo_audit": {"score_0_100": 90},
        "freshness_status": "fresh",
        "related_app": "sop-pipeline",
        "related_kit": "pack-sop-forecasting",
        "price": "39€",
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
        "publish_date": "2026-12-05",
        "last_modified_es": "2026-10-27",
        "last_modified_en": "",
        "language_parity": "missing_en",
        "category": "Inteligencia Artificial",
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
        "title_es": "Modelo de Optimización Lineal de Cash Flow para Startups y Scaleups",
        "title_en": "Linear Optimization Model for Cash Flow in Tech Scaleups",
        "publish_date": "",
        "last_modified_es": "2026-10-28",
        "last_modified_en": "",
        "language_parity": "missing_en",
        "category": "Finanzas Cuantitativas",
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
        "id": "executive-pack-decision-suite",
        "asset_type": "kit",
        "status": "published",
        "visibility": "public",
        "title_es": "Executive Decision Pack: Suite Financiera y Operativa para Comités",
        "title_en": "Executive Decision Pack: Financial & Operations Board Suite",
        "publish_date": "2026-09-01",
        "last_modified_es": "2026-10-10",
        "last_modified_en": "2026-10-10",
        "language_parity": "complete",
        "category": "Productos B2B",
        "word_count_es": 1200,
        "word_count_en": 1200,
        "reading_time_min": 6,
        "seo_audit": {"score_0_100": 100},
        "freshness_status": "fresh",
        "related_app": "lifeops",
        "related_kit": "pack-executive-suite",
        "price": "99€",
        "sample_views": 3200,
        "sample_users": 2100,
        "sample_eng_sec": 310.0,
        "sample_clicks": 840,
        "sample_impr": 12500,
        "sample_ctr": 6.72,
        "sample_pos": 3.1
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


def build_pulse_excel(is_template: bool = False) -> Path:
    """
    Construye el libro de trabajo Excel.
    Si is_template=True, genera el archivo del Kit descargable (con ejemplos representativos,
    hoja de taxonomía y validaciones de datos desplegables).
    Si is_template=False, genera el tracker poblado privado para uso interno con los 135+ activos.
    """
    wb = openpyxl.Workbook()
    wb.remove(wb.active) # Eliminar hoja por defecto

    # 1. Cargar datos
    assets = []
    metrics = {}
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

    # ==============================================================================
    # HOJA 1: Instrucciones y Guía
    # ==============================================================================
    ws_intro = wb.create_sheet(title="Instrucciones")
    ws_intro.views.sheetView[0].showGridLines = True
    
    ws_intro.cell(row=2, column=2, value="DATALARIA PULSE — CONTENT OPS MASTER TRACKER").font = Font(name=FONT_FAMILY, size=16, bold=True, color="0F172A")
    ws_intro.cell(row=3, column=2, value="Sistema Operativo de Gobierno Editorial, Paridad Bilingüe y Retorno de Contenido").font = Font(name=FONT_FAMILY, size=11, italic=True, color="64748B")
    
    intro_paragraphs = [
        ("Objetivo del Tracker:", "Gestionar en un único libro auditable todos tus activos (Posts, Apps, Kits), controlando la paridad bilingüe, salud SEO, estado de frescura y métricas de tráfico sin depender de herramientas externas como Notion."),
        ("Hoja 'Activos':", "Tabla maestra con ordenación, filtros y validaciones desplegables. Cada fila consolida un activo bilingüe unificado."),
        ("Hoja 'Kanban':", "Tablero visual distribuido por estado (Idea, Borrador, En Revisión, Programado, Publicado) mediante fórmulas dinámicas."),
        ("Hoja 'Métricas':", "Consolidación de Google Analytics 4 (visitas, usuarios, duración) y Search Console (clics, impresiones, posición)."),
        ("Hoja 'Dashboard':", "Resumen ejecutivo con KPIs clave, cadencia de publicación y totales de rendimiento."),
        ("Hoja 'Taxonomía':", "Catálogo maestro de valores válidos (Tipos, Estados, Visibilidad, Paridad, Frescura) que alimenta los desplegables.")
    ]
    
    r = 5
    for title, desc in intro_paragraphs:
        ws_intro.cell(row=r, column=2, value=title).font = Font(name=FONT_FAMILY, size=11, bold=True, color="1E293B")
        ws_intro.cell(row=r, column=3, value=desc).font = Font(name=FONT_FAMILY, size=11, color="334155")
        ws_intro.row_dimensions[r].height = 24
        r += 1

    ws_intro.column_dimensions["B"].width = 25
    ws_intro.column_dimensions["C"].width = 85

    # ==============================================================================
    # HOJA 2: Taxonomía y Validaciones
    # ==============================================================================
    ws_tax = wb.create_sheet(title="Taxonomía")
    ws_tax.views.sheetView[0].showGridLines = True

    tax_headers = ["Tipo de Activo", "Estado", "Visibilidad", "Paridad Bilingüe", "Estado Frescura"]
    for c_idx, th in enumerate(tax_headers, 1):
        ws_tax.cell(row=1, column=c_idx, value=th)
    style_header_row(ws_tax, 1, len(tax_headers))

    tax_data = {
        1: ["POST", "APP", "KIT"],
        2: ["Idea", "Draft", "Review", "Scheduled", "Published"],
        3: ["public", "private"],
        4: ["complete", "missing_es", "missing_en", "outdated_es", "outdated_en"],
        5: ["fresh", "stale", "review_needed"]
    }

    for col_idx, values in tax_data.items():
        for row_idx, val in enumerate(values, 2):
            c = ws_tax.cell(row=row_idx, column=col_idx, value=val)
            c.font = Font(name=FONT_FAMILY, size=10)
            c.border = THIN_BORDER

    auto_fit_columns(ws_tax, min_width=16)

    # ==============================================================================
    # HOJA 3: Activos (Tabla Maestra)
    # ==============================================================================
    ws_act = wb.create_sheet(title="Activos")
    ws_act.views.sheetView[0].showGridLines = True

    headers = [
        "ID", "Tipo", "Estado", "Visibilidad", "Título (ES)", "Título (EN)",
        "Fecha Pub", "Última Mod (ES)", "Última Mod (EN)", "Paridad",
        "Categoría", "Palabras ES", "Palabras EN", "Lectura (min)", "Score SEO",
        "Frescura", "App Asociada", "Kit Asociado", "Precio", "Visitas 30d", "Usuarios 30d"
    ]
    
    for c_idx, h in enumerate(headers, 1):
        ws_act.cell(row=1, column=c_idx, value=h)
    style_header_row(ws_act, 1, len(headers))

    # Reglas de validación desplegables (DataValidation)
    dv_type = DataValidation(type="list", formula1="=Taxonomía!$A$2:$A$4", allow_blank=True)
    ws_act.add_data_validation(dv_type)
    dv_type.add("B2:B1000")

    dv_status = DataValidation(type="list", formula1="=Taxonomía!$B$2:$B$6", allow_blank=True)
    ws_act.add_data_validation(dv_status)
    dv_status.add("C2:C1000")

    dv_vis = DataValidation(type="list", formula1="=Taxonomía!$C$2:$C$3", allow_blank=True)
    ws_act.add_data_validation(dv_vis)
    dv_vis.add("D2:D1000")

    dv_parity = DataValidation(type="list", formula1="=Taxonomía!$D$2:$D$6", allow_blank=True)
    ws_act.add_data_validation(dv_parity)
    dv_parity.add("J2:J1000")

    dv_fresh = DataValidation(type="list", formula1="=Taxonomía!$E$2:$E$4", allow_blank=True)
    ws_act.add_data_validation(dv_fresh)
    dv_fresh.add("P2:P1000")

    row_num = 2
    for a in assets:
        aid = a["id"]
        m = metrics.get(aid, {})
        
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
        ws_act.cell(row=row_num, column=14, value=a.get("reading_time_min", 0))
        
        # SEO Score
        seo_val = a.get("seo_audit", {}).get("score_0_100", 0)
        s_cell = ws_act.cell(row=row_num, column=15, value=seo_val)
        if seo_val >= 80: s_cell.fill = BADGE_COMPLETE
        elif seo_val >= 60: s_cell.fill = BADGE_WARN
        else: s_cell.fill = BADGE_ALERT

        ws_act.cell(row=row_num, column=16, value=a.get("freshness_status", "fresh"))
        ws_act.cell(row=row_num, column=17, value=a.get("related_app") or "")
        ws_act.cell(row=row_num, column=18, value=a.get("related_kit") or "")
        ws_act.cell(row=row_num, column=19, value=a.get("price") or "")
        ws_act.cell(row=row_num, column=20, value=m.get("ga4_views_30d", 0))
        ws_act.cell(row=row_num, column=21, value=m.get("ga4_users_30d", 0))

        # Estilo de fila
        for col_i in range(1, len(headers) + 1):
            c = ws_act.cell(row=row_num, column=col_i)
            c.font = Font(name=FONT_FAMILY, size=10)
            c.border = THIN_BORDER
            if row_num % 2 == 1 and not c.fill.start_color.rgb:
                c.fill = ZEBRA_FILL

        ws_act.row_dimensions[row_num].height = 20
        row_num += 1

    auto_fit_columns(ws_act)

    # ==============================================================================
    # HOJA 3: Tablero Kanban (Fórmulas compatibles Excel 2016+/Sheets)
    # ==============================================================================
    ws_kanban = wb.create_sheet(title="Kanban")
    ws_kanban.views.sheetView[0].showGridLines = True

    kanban_cols = ["Idea (Backlog)", "Borrador (Draft)", "En Revisión (Review)", "Programado (Scheduled)", "Publicado (Live)"]
    for c_i, k_title in enumerate(kanban_cols, 1):
        ws_kanban.cell(row=1, column=c_i, value=k_title)
    style_header_row(ws_kanban, 1, len(kanban_cols))

    # Agrupar activos en columnas
    status_buckets = {"idea": [], "draft": [], "review": [], "scheduled": [], "published": []}
    for a in assets:
        st = a.get("status", "idea").lower()
        if st in ("available", "live"): st = "published"
        if st in ("coming",): st = "scheduled"
        status_buckets.get(st, status_buckets["published"]).append(a)

    max_items = max([len(v) for v in status_buckets.values()] or [1])
    for r_idx in range(max_items):
        r_row = r_idx + 2
        for c_idx, st_key in enumerate(["idea", "draft", "review", "scheduled", "published"], 1):
            bucket = status_buckets[st_key]
            if r_idx < len(bucket):
                item = bucket[r_idx]
                title = item.get("title_es") or item.get("title_en") or item["id"]
                val = f"{title}\n[{item.get('asset_type', 'post').upper()}] {item.get('category', '')}"
                c = ws_kanban.cell(row=r_row, column=c_idx, value=val)
                c.alignment = Alignment(vertical="top", wrap_text=True)
                c.font = Font(name=FONT_FAMILY, size=9)
                c.border = THIN_BORDER
                ws_kanban.row_dimensions[r_row].height = 36
            else:
                ws_kanban.cell(row=r_row, column=c_idx).border = THIN_BORDER

    for c_i in range(1, len(kanban_cols) + 1):
        ws_kanban.column_dimensions[get_column_letter(c_i)].width = 32

    # ==============================================================================
    # HOJA 4: Métricas Cuantitativas
    # ==============================================================================
    ws_met = wb.create_sheet(title="Métricas")
    ws_met.views.sheetView[0].showGridLines = True

    met_headers = ["ID Activo", "Tipo", "Visitas 30d", "Usuarios Únicos 30d", "Tiempo Medio (s)", "Clics GSC", "Impresiones GSC", "CTR GSC (%)", "Posición Media GSC"]
    for c_i, mh in enumerate(met_headers, 1):
        ws_met.cell(row=1, column=c_i, value=mh)
    style_header_row(ws_met, 1, len(met_headers))

    r_num = 2
    for a in assets:
        aid = a["id"]
        m = metrics.get(aid, {})
        ws_met.cell(row=r_num, column=1, value=aid)
        ws_met.cell(row=r_num, column=2, value=a.get("asset_type", "post").upper())
        ws_met.cell(row=r_num, column=3, value=m.get("ga4_views_30d", 0))
        ws_met.cell(row=r_num, column=4, value=m.get("ga4_users_30d", 0))
        ws_met.cell(row=r_num, column=5, value=round(m.get("ga4_engagement_sec", 0.0), 1))
        ws_met.cell(row=r_num, column=6, value=m.get("gsc_clicks_30d", 0))
        ws_met.cell(row=r_num, column=7, value=m.get("gsc_impressions_30d", 0))
        ws_met.cell(row=r_num, column=8, value=m.get("gsc_ctr_pct", 0.0))
        ws_met.cell(row=r_num, column=9, value=m.get("gsc_avg_position", 0.0))

        for col_i in range(1, len(met_headers) + 1):
            c = ws_met.cell(row=r_num, column=col_i)
            c.font = Font(name=FONT_FAMILY, size=10)
            c.border = THIN_BORDER
        r_num += 1

    auto_fit_columns(ws_met)

    # ==============================================================================
    # HOJA 5: Dashboard de Control
    # ==============================================================================
    ws_dash = wb.create_sheet(title="Dashboard")
    ws_dash.views.sheetView[0].showGridLines = True

    ws_dash.cell(row=2, column=2, value="CUADRO DE MANDO EDITORIAL (CONTENT OPS)").font = Font(name=FONT_FAMILY, size=14, bold=True, color="0F172A")
    
    kpis = [
        ("Total Activos Catalogados", f"=COUNTA(Activos!A2:A{max(row_num-1, 2)})"),
        ("Artículos Publicados (Live)", f'=COUNTIF(Activos!C2:C{max(row_num-1, 2)}, "Published")'),
        ("Activos Programados (Scheduled)", f'=COUNTIF(Activos!C2:C{max(row_num-1, 2)}, "Scheduled")'),
        ("Paridad Bilingüe Completa", f'=COUNTIF(Activos!J2:J{max(row_num-1, 2)}, "complete")'),
        ("Total Visitas 30d", f"=SUM(Activos!T2:T{max(row_num-1, 2)})"),
        ("Total Usuarios 30d", f"=SUM(Activos!U2:U{max(row_num-1, 2)})")
    ]

    r_kpi = 4
    for kpi_title, kpi_formula in kpis:
        ws_dash.cell(row=r_kpi, column=2, value=kpi_title).font = Font(name=FONT_FAMILY, size=11, bold=True, color="475569")
        c_val = ws_dash.cell(row=r_kpi, column=4, value=kpi_formula)
        c_val.font = Font(name=FONT_FAMILY, size=12, bold=True, color="0F172A")
        c_val.alignment = Alignment(horizontal="right")
        ws_dash.row_dimensions[r_kpi].height = 24
        r_kpi += 1

    ws_dash.column_dimensions["B"].width = 35
    ws_dash.column_dimensions["D"].width = 18

    # Guardar
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = "Pulse_Content_Ops_Template.xlsx" if is_template else "Pulse_Private_Tracker.xlsx"
    dest_path = OUTPUT_DIR / filename
    wb.save(dest_path)
    print(f"[EXCEL] Libro generado con éxito: {dest_path}")
    return dest_path


if __name__ == "__main__":
    # 1. Generar tracker privado poblado
    build_pulse_excel(is_template=False)
    # 2. Generar plantilla para el Kit
    build_pulse_excel(is_template=True)
