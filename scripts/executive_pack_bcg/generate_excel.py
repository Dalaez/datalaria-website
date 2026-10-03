#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos de decisión estratégica en Excel oficiales de Datalaria:
1. packages/[ES]_BCG_Dinamica/BCG_Dinamica_Datalaria_ES.xlsx (Versión en Español)
2. packages/[EN]_Dynamic_BCG/Dynamic_BCG_Datalaria_EN.xlsx (Versión en Inglés)

Estructura de 4 pestañas interconectadas:
- Pestaña 1: "Dashboard Ejecutivo" / "Executive Dashboard"
  (Gráfico de Burbujas dinámico cartesiano CMR vs TCM con tamaño proporcional a ventas,
   Balance Neto de Cash Flow de Cartera, distribución de ingresos por cuadrante y semáforo de sostenibilidad).
- Pestaña 2: "Evaluación Cartera UENs" / "Business Units Assessment"
  (Tabla de hasta 12 Unidades Estratégicas de Negocio con inputs del usuario: Nombre de UEN,
   Facturación propia, Facturación líder competidor, Cuota de mercado relativa calculada,
   Tasa de crecimiento de mercado %, Margen EBITDA % y Generación neta de FCF).
- Pestaña 3: "Matriz & Flujo de Fondos" / "BCG Matrix & Fund Flow"
  (Clasificación matemática automatizada en los 4 cuadrantes: Estrellas, Vacas, Interrogantes y Perros,
   cálculo de superávit/déficit de liquidez y simulación de la regla dorada de reinversión de Henderson).
- Pestaña 4: "Plan de Asignación de Capital" / "Capital Allocation Plan"
  (Iniciativas de reasignación de CAPEX y desinversión con Owner C-Level, plazos Q1-Q4,
   presupuesto reasignado y KPI de impacto en ROIC / margen corporativo).

Estándares de protección ECMA-376:
- Celdas de entrada desbloqueadas (locked=False) y selectUnlockedCells=False.
- Celdas de fórmulas y títulos protegidas (locked=True) y selectLockedCells=False.
- Contraseña oficial: "Datalaria2026".
- Formato numérico adaptado a ES (coma decimal, €) y EN (punto decimal, $).
- Compatibilidad nativa con Microsoft Excel y Google Sheets.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.chart import BubbleChart, Reference, Series

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = "0F172A"      # Slate 900 / Títulos principales y cabeceras
COLOR_NAVY_MED = "1E293B"       # Slate 800 / Subcabeceras
COLOR_BLUE_ACCENT = "2563EB"    # Blue 600 / Azul Consultoría Datalaria
COLOR_TEAL_ACCENT = "0D9488"    # Teal 600 / Vacas Lecheras / Liquidez
COLOR_AMBER_ACCENT = "D97706"   # Amber 600 / Interrogantes / Precaución
COLOR_ROSE_ACCENT = "E11D48"    # Rose 600 / Perros / Desinversión
COLOR_GOLD_ACCENT = "F59E0B"    # Amber 500 / Estrellas / Oro

# Fondos claros de tarjetas y cuadrantes
COLOR_BG_LIGHT = "F8FAFC"       # Slate 50
COLOR_BG_CARD = "F1F5F9"        # Slate 100
COLOR_WHITE = "FFFFFF"          # Blanco / Entradas desbloqueadas

# Cuadrantes temáticos BCG
COLOR_STAR_BG = "EFF6FF"        # Blue 50 (Estrellas)
COLOR_STAR_BORDER = "3B82F6"
COLOR_STAR_TEXT = "1E40AF"

COLOR_COW_BG = "F0FDFA"         # Teal 50 (Vacas)
COLOR_COW_BORDER = "14B8A6"
COLOR_COW_TEXT = "0F766E"

COLOR_QUESTION_BG = "FFFBEB"    # Amber 50 (Interrogantes)
COLOR_QUESTION_BORDER = "F59E0B"
COLOR_QUESTION_TEXT = "92400E"

COLOR_DOG_BG = "FFF1F2"         # Rose 50 (Perros)
COLOR_DOG_BORDER = "F43F5E"
COLOR_DOG_TEXT = "9F1239"

# Bordes
COLOR_BORDER_LIGHT = "CBD5E1"   # Slate 300
COLOR_BORDER_MED = "94A3B8"     # Slate 400

PASSWORD_PROTECT = "Datalaria2026"


def get_base_styles(lang='ES'):
    thin_border = Border(
        left=Side(style='thin', color=COLOR_BORDER_LIGHT),
        right=Side(style='thin', color=COLOR_BORDER_LIGHT),
        top=Side(style='thin', color=COLOR_BORDER_LIGHT),
        bottom=Side(style='thin', color=COLOR_BORDER_LIGHT)
    )
    header_border = Border(
        left=Side(style='thin', color=COLOR_NAVY_MED),
        right=Side(style='thin', color=COLOR_NAVY_MED),
        top=Side(style='medium', color=COLOR_NAVY_DARK),
        bottom=Side(style='medium', color=COLOR_NAVY_DARK)
    )
    total_border = Border(
        top=Side(style='thin', color=COLOR_BORDER_MED),
        bottom=Side(style='double', color=COLOR_NAVY_DARK)
    )

    if lang == 'ES':
        num_fmt_curr = "#,##0 €"
        num_fmt_curr_dec = "#,##0.00 €"
        num_fmt_pct = "0.0%"
        num_fmt_ratio = "0.00\"x\""
        num_fmt_int = "#,##0"
    else:
        num_fmt_curr = "$#,##0"
        num_fmt_curr_dec = "$#,##0.00"
        num_fmt_pct = "0.0%"
        num_fmt_ratio = "0.00\"x\""
        num_fmt_int = "#,##0"

    return {
        'thin_border': thin_border,
        'header_border': header_border,
        'total_border': total_border,
        'font_title': Font(name='Segoe UI', size=16, bold=True, color=COLOR_NAVY_DARK),
        'font_subtitle': Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT),
        'font_meta': Font(name='Segoe UI', size=9, italic=True, color="64748B"),
        'font_section': Font(name='Segoe UI', size=12, bold=True, color=COLOR_NAVY_DARK),
        'font_header': Font(name='Segoe UI', size=10, bold=True, color=COLOR_WHITE),
        'font_subhead': Font(name='Segoe UI', size=9, bold=True, color=COLOR_NAVY_MED),
        'font_regular': Font(name='Segoe UI', size=9.5, color=COLOR_NAVY_DARK),
        'font_bold': Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_NAVY_DARK),
        'font_kpi_val': Font(name='Segoe UI', size=18, bold=True, color=COLOR_NAVY_DARK),
        'font_kpi_lbl': Font(name='Segoe UI', size=8.5, bold=True, color="64748B"),
        'font_badge': Font(name='Segoe UI', size=9, bold=True),
        'fill_navy_hdr': PatternFill(start_color=COLOR_NAVY_DARK, end_color=COLOR_NAVY_DARK, fill_type='solid'),
        'fill_navy_sub': PatternFill(start_color=COLOR_NAVY_MED, end_color=COLOR_NAVY_MED, fill_type='solid'),
        'fill_card_bg': PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid'),
        'fill_light_bg': PatternFill(start_color=COLOR_BG_LIGHT, end_color=COLOR_BG_LIGHT, fill_type='solid'),
        'fill_input': PatternFill(start_color=COLOR_WHITE, end_color=COLOR_WHITE, fill_type='solid'),
        'fill_star': PatternFill(start_color=COLOR_STAR_BG, end_color=COLOR_STAR_BG, fill_type='solid'),
        'fill_cow': PatternFill(start_color=COLOR_COW_BG, end_color=COLOR_COW_BG, fill_type='solid'),
        'fill_question': PatternFill(start_color=COLOR_QUESTION_BG, end_color=COLOR_QUESTION_BG, fill_type='solid'),
        'fill_dog': PatternFill(start_color=COLOR_DOG_BG, end_color=COLOR_DOG_BG, fill_type='solid'),
        'align_center': Alignment(horizontal='center', vertical='center'),
        'align_left': Alignment(horizontal='left', vertical='center'),
        'align_right': Alignment(horizontal='right', vertical='center'),
        'align_left_wrap': Alignment(horizontal='left', vertical='center', wrap_text=True),
        'align_center_wrap': Alignment(horizontal='center', vertical='center', wrap_text=True),
        'num_fmt_curr': num_fmt_curr,
        'num_fmt_curr_dec': num_fmt_curr_dec,
        'num_fmt_pct': num_fmt_pct,
        'num_fmt_ratio': num_fmt_ratio,
        'num_fmt_int': num_fmt_int,
    }


def apply_sheet_protection(ws):
    """
    Aplica protección de hoja según el estándar ECMA-376 / Office OpenXML:
    - ws.protection.sheet = True: activa la protección general.
    - ws.protection.set_password(PASSWORD_PROTECT): hash canónico para 'Datalaria2026'.
    - selectUnlockedCells = False (0 = sin restricción): permite doble clic y edición en celdas desbloqueadas.
    - selectLockedCells = False: permite seleccionar celdas bloqueadas para auditar fórmulas.
    """
    ws.protection.set_password(PASSWORD_PROTECT)
    ws.protection.sheet = True
    ws.protection.objects = True
    ws.protection.scenarios = True
    ws.protection.selectUnlockedCells = False
    ws.protection.selectLockedCells = False


# ==============================================================================
# TAB 1: DASHBOARD EJECUTIVO / EXECUTIVE DASHBOARD
# ==============================================================================
def build_tab1_dashboard(wb, ws, lang='ES'):
    styles = get_base_styles(lang)
    ws.title = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    ws.views.sheetView[0].showGridLines = True

    # 1. Cabecera Corporativa (Filas 2 a 4)
    ws['B2'] = "DATALARIA | EXECUTIVE DECISION PACK"
    ws['B2'].font = styles['font_title']

    ws['B3'] = ("MATRIZ BCG DINÁMICA & ASIGNACIÓN DE CAPITAL DE CARTERA"
                if lang == 'ES' else
                "DYNAMIC BCG PORTFOLIO MATRIX & CAPITAL ALLOCATION")
    ws['B3'].font = styles['font_subtitle']

    ws['B4'] = ("Modelo Cuantitativo de Balance de Fondos (Bruce Henderson) • Grado Consejo de Administración • Versión 2026"
                if lang == 'ES' else
                "Quantitative Cash Flow Balance Model (Bruce Henderson) • Board of Directors Grade • 2026 Edition")
    ws['B4'].font = styles['font_meta']

    # 2. Tarjetas KPI de Resumen Ejecutivo (Filas 6 a 9)
    # Card 1: Facturación Total Cartera
    # Card 2: Flujo Libre de Caja (FCF) Neto
    # Card 3: Margen EBITDA Ponderado
    # Card 4: Superávit de Vacas vs Déficit Crecimiento
    # Card 5: Cuota en Líderes (Estrellas + Vacas)
    kpis = [
        ("B6:C6", "B7:C8", "B9:C9",
         "FACTURACIÓN TOTAL CARTERA" if lang == 'ES' else "TOTAL PORTFOLIO REVENUE",
         "='Evaluación Cartera UENs'!E24" if lang == 'ES' else "='Business Units Assessment'!E24",
         styles['num_fmt_curr']),
        ("D6:E6", "D7:E8", "D9:E9",
         "FLUJO DE CAJA LIBRE (FCF) NETO" if lang == 'ES' else "NET FREE CASH FLOW (FCF)",
         "='Evaluación Cartera UENs'!K24" if lang == 'ES' else "='Business Units Assessment'!K24",
         styles['num_fmt_curr']),
        ("F6:G6", "F7:G8", "F9:G9",
         "MARGEN EBITDA PONDERADO" if lang == 'ES' else "WEIGHTED EBITDA MARGIN",
         "='Evaluación Cartera UENs'!J24/'Evaluación Cartera UENs'!E24" if lang == 'ES' else "='Business Units Assessment'!J24/'Business Units Assessment'!E24",
         styles['num_fmt_pct']),
        ("H6:I6", "H7:I8", "H9:I9",
         "BALANCE DE FONDOS HENDERSON" if lang == 'ES' else "HENDERSON CASH BALANCE",
         "='Matriz & Flujo de Fondos'!F18" if lang == 'ES' else "='BCG Matrix & Fund Flow'!F18",
         styles['num_fmt_curr']),
        ("J6:K6", "J7:K8", "J9:K9",
         "INGRESOS EN LÍDERES (CMR ≥ 1.0)" if lang == 'ES' else "REVENUE IN LEADERS (RMS ≥ 1.0)",
         "=('Matriz & Flujo de Fondos'!C14+'Matriz & Flujo de Fondos'!C15)/'Evaluación Cartera UENs'!E24" if lang == 'ES' else "=('BCG Matrix & Fund Flow'!C14+'BCG Matrix & Fund Flow'!C15)/'Business Units Assessment'!E24",
         styles['num_fmt_pct']),
    ]

    for title_range, val_range, sub_range, title, formula, fmt in kpis:
        ws.merge_cells(title_range)
        ws.merge_cells(val_range)
        t_cell = ws[title_range.split(':')[0]]
        v_cell = ws[val_range.split(':')[0]]

        t_cell.value = title
        t_cell.font = styles['font_kpi_lbl']
        t_cell.alignment = styles['align_center']
        t_cell.fill = styles['fill_card_bg']

        v_cell.value = formula
        v_cell.font = styles['font_kpi_val']
        v_cell.alignment = styles['align_center']
        v_cell.fill = styles['fill_card_bg']
        v_cell.number_format = fmt

        # Aplicar bordes al bloque KPI
        cols = [title_range.split(':')[0][0], title_range.split(':')[1][0]]
        for row in range(6, 9):
            for col in cols:
                ws[f"{col}{row}"].border = styles['thin_border']

    # 3. Sección de Desglose por Cuadrante BCG (Filas 11 a 17)
    ws['B11'] = "RESUMEN EJECUTIVO POR CUADRANTE BCG" if lang == 'ES' else "EXECUTIVE SUMMARY BY BCG QUADRANT"
    ws['B11'].font = styles['font_section']

    headers_quad = [
        ("B12", "Cuadrante Estratégico" if lang == 'ES' else "Strategic Quadrant"),
        ("C12", "Nº UENs" if lang == 'ES' else "SBUs #"),
        ("D12", "Facturación (€)" if lang == 'ES' else "Revenue ($)"),
        ("E12", "% Cartera" if lang == 'ES' else "% Portfolio"),
        ("F12", "EBITDA Total" if lang == 'ES' else "Total EBITDA"),
        ("G12", "FCF Neto (€)" if lang == 'ES' else "Net FCF ($)"),
        ("H12", "Prescripción Estratégica C-Level" if lang == 'ES' else "C-Level Strategic Prescription"),
    ]

    for cell_id, text in headers_quad:
        ws[cell_id] = text
        ws[cell_id].font = styles['font_header']
        ws[cell_id].fill = styles['fill_navy_hdr']
        ws[cell_id].alignment = styles['align_center']
        ws[cell_id].border = styles['header_border']

    tab3_name = 'Matriz & Flujo de Fondos' if lang == 'ES' else 'BCG Matrix & Fund Flow'
    tab2_name = 'Evaluación Cartera UENs' if lang == 'ES' else 'Business Units Assessment'

    quadrant_rows = [
        (13, "⭐ ESTRELLAS" if lang == 'ES' else "⭐ STARS",
         f"='{tab3_name}'!B14", f"='{tab3_name}'!C14", f"=D13/'{tab2_name}'!E24", f"='{tab3_name}'!E14", f"='{tab3_name}'!F14",
         "Invertir agresivamente para consolidar liderazgo" if lang == 'ES' else "Invest aggressively to defend and grow leadership",
         styles['fill_star'], Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_STAR_TEXT)),

        (14, "🐄 VACAS LECHERAS" if lang == 'ES' else "🐄 CASH COWS",
         f"='{tab3_name}'!B15", f"='{tab3_name}'!C15", f"=D14/'{tab2_name}'!E24", f"='{tab3_name}'!E15", f"='{tab3_name}'!F15",
         "Ordeño disciplinado; reinvertir sólo mantenimiento" if lang == 'ES' else "Disciplined milking; fund selective maintenance CAPEX",
         styles['fill_cow'], Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_COW_TEXT)),

        (15, "❓ INTERROGANTES" if lang == 'ES' else "❓ QUESTION MARKS",
         f"='{tab3_name}'!B16", f"='{tab3_name}'!C16", f"=D15/'{tab2_name}'!E24", f"='{tab3_name}'!E16", f"='{tab3_name}'!F16",
         "Selección estricta: inyectar capital o desinvertir" if lang == 'ES' else "Strict selection: aggressive push or prompt divestment",
         styles['fill_question'], Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_QUESTION_TEXT)),

        (16, "🐕 PERROS" if lang == 'ES' else "🐕 DOGS",
         f"='{tab3_name}'!B17", f"='{tab3_name}'!C17", f"=D16/'{tab2_name}'!E24", f"='{tab3_name}'!E17", f"='{tab3_name}'!F17",
         "Cosechar, desinvertir o liquidar para liberar capital" if lang == 'ES' else "Harvest, divest, or liquidate to release capital",
         styles['fill_dog'], Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_DOG_TEXT)),
    ]

    for row_idx, q_name, f_cnt, f_rev, f_pct, f_ebitda, f_fcf, presc, fill_col, font_col in quadrant_rows:
        ws[f"B{row_idx}"] = q_name
        ws[f"B{row_idx}"].font = font_col
        ws[f"B{row_idx}"].fill = fill_col
        ws[f"B{row_idx}"].alignment = styles['align_left']
        ws[f"B{row_idx}"].border = styles['thin_border']

        ws[f"C{row_idx}"] = f_cnt
        ws[f"C{row_idx}"].font = styles['font_bold']
        ws[f"C{row_idx}"].fill = fill_col
        ws[f"C{row_idx}"].alignment = styles['align_center']
        ws[f"C{row_idx}"].border = styles['thin_border']
        ws[f"C{row_idx}"].number_format = styles['num_fmt_int']

        ws[f"D{row_idx}"] = f_rev
        ws[f"D{row_idx}"].font = styles['font_regular']
        ws[f"D{row_idx}"].fill = fill_col
        ws[f"D{row_idx}"].alignment = styles['align_right']
        ws[f"D{row_idx}"].border = styles['thin_border']
        ws[f"D{row_idx}"].number_format = styles['num_fmt_curr']

        ws[f"E{row_idx}"] = f_pct
        ws[f"E{row_idx}"].font = styles['font_bold']
        ws[f"E{row_idx}"].fill = fill_col
        ws[f"E{row_idx}"].alignment = styles['align_center']
        ws[f"E{row_idx}"].border = styles['thin_border']
        ws[f"E{row_idx}"].number_format = styles['num_fmt_pct']

        ws[f"F{row_idx}"] = f_ebitda
        ws[f"F{row_idx}"].font = styles['font_regular']
        ws[f"F{row_idx}"].fill = fill_col
        ws[f"F{row_idx}"].alignment = styles['align_right']
        ws[f"F{row_idx}"].border = styles['thin_border']
        ws[f"F{row_idx}"].number_format = styles['num_fmt_curr']

        ws[f"G{row_idx}"] = f_fcf
        ws[f"G{row_idx}"].font = styles['font_bold']
        ws[f"G{row_idx}"].fill = fill_col
        ws[f"G{row_idx}"].alignment = styles['align_right']
        ws[f"G{row_idx}"].border = styles['thin_border']
        ws[f"G{row_idx}"].number_format = styles['num_fmt_curr']

        ws[f"H{row_idx}"] = presc
        ws[f"H{row_idx}"].font = styles['font_regular']
        ws[f"H{row_idx}"].fill = fill_col
        ws[f"H{row_idx}"].alignment = styles['align_left_wrap']
        ws[f"H{row_idx}"].border = styles['thin_border']

    # Fila Total Cartera
    ws['B17'] = "CONSOLIDADO CARTERA" if lang == 'ES' else "PORTFOLIO TOTAL"
    ws['B17'].font = styles['font_bold']
    ws['B17'].alignment = styles['align_left']
    ws['B17'].border = styles['total_border']

    ws['C17'] = "=SUM(C13:C16)"
    ws['C17'].font = styles['font_bold']
    ws['C17'].alignment = styles['align_center']
    ws['C17'].border = styles['total_border']

    ws['D17'] = "=SUM(D13:D16)"
    ws['D17'].font = styles['font_bold']
    ws['D17'].alignment = styles['align_right']
    ws['D17'].border = styles['total_border']
    ws['D17'].number_format = styles['num_fmt_curr']

    ws['E17'] = "=SUM(E13:E16)"
    ws['E17'].font = styles['font_bold']
    ws['E17'].alignment = styles['align_center']
    ws['E17'].border = styles['total_border']
    ws['E17'].number_format = styles['num_fmt_pct']

    ws['F17'] = "=SUM(F13:F16)"
    ws['F17'].font = styles['font_bold']
    ws['F17'].alignment = styles['align_right']
    ws['F17'].border = styles['total_border']
    ws['F17'].number_format = styles['num_fmt_curr']

    ws['G17'] = "=SUM(G13:G16)"
    ws['G17'].font = styles['font_bold']
    ws['G17'].alignment = styles['align_right']
    ws['G17'].border = styles['total_border']
    ws['G17'].number_format = styles['num_fmt_curr']

    ws['H17'] = ("Equilibrio Dinámico Requerido: Vacas financian Interrogantes"
                 if lang == 'ES' else
                 "Dynamic Balance Required: Cash Cows finance Question Marks")
    ws['H17'].font = styles['font_subhead']
    ws['H17'].alignment = styles['align_left']
    ws['H17'].border = styles['total_border']

    # 4. Tabla de Datos para el Gráfico de Burbujas en el Dashboard (Filas 20 a 33)
    ws['B20'] = "MATRIZ CARTESIANA BCG: POSICIONAMIENTO DE UENs" if lang == 'ES' else "CARTESIAN BCG MATRIX: SBU POSITIONING"
    ws['B20'].font = styles['font_section']

    chart_headers = [
        ("B21", "ID"),
        ("C21", "Unidad Estratégica (UEN)" if lang == 'ES' else "Strategic Business Unit"),
        ("D21", "CMR (Eje X)" if lang == 'ES' else "RMS (X Axis)"),
        ("E21", "TCM % (Eje Y)" if lang == 'ES' else "MGR % (Y Axis)"),
        ("F21", "Ventas (€) (Burbuja)" if lang == 'ES' else "Revenue ($) (Bubble)"),
        ("G21", "FCF (€)" if lang == 'ES' else "FCF ($)"),
        ("H21", "Cuadrante" if lang == 'ES' else "Quadrant"),
    ]

    for cell_id, text in chart_headers:
        ws[cell_id] = text
        ws[cell_id].font = styles['font_header']
        ws[cell_id].fill = styles['fill_navy_sub']
        ws[cell_id].alignment = styles['align_center']
        ws[cell_id].border = styles['header_border']

    for i in range(12):
        row = 22 + i
        src_row = 12 + i
        ws[f"B{row}"] = f"='{tab2_name}'!B{src_row}"
        ws[f"B{row}"].font = styles['font_subhead']
        ws[f"B{row}"].alignment = styles['align_center']
        ws[f"B{row}"].border = styles['thin_border']

        ws[f"C{row}"] = f"='{tab2_name}'!C{src_row}"
        ws[f"C{row}"].font = styles['font_regular']
        ws[f"C{row}"].alignment = styles['align_left']
        ws[f"C{row}"].border = styles['thin_border']

        ws[f"D{row}"] = f"='{tab2_name}'!G{src_row}"
        ws[f"D{row}"].font = styles['font_bold']
        ws[f"D{row}"].alignment = styles['align_center']
        ws[f"D{row}"].border = styles['thin_border']
        ws[f"D{row}"].number_format = styles['num_fmt_ratio']

        ws[f"E{row}"] = f"='{tab2_name}'!H{src_row}"
        ws[f"E{row}"].font = styles['font_bold']
        ws[f"E{row}"].alignment = styles['align_center']
        ws[f"E{row}"].border = styles['thin_border']
        ws[f"E{row}"].number_format = styles['num_fmt_pct']

        ws[f"F{row}"] = f"='{tab2_name}'!E{src_row}"
        ws[f"F{row}"].font = styles['font_regular']
        ws[f"F{row}"].alignment = styles['align_right']
        ws[f"F{row}"].border = styles['thin_border']
        ws[f"F{row}"].number_format = styles['num_fmt_curr']

        ws[f"G{row}"] = f"='{tab2_name}'!K{src_row}"
        ws[f"G{row}"].font = styles['font_regular']
        ws[f"G{row}"].alignment = styles['align_right']
        ws[f"G{row}"].border = styles['thin_border']
        ws[f"G{row}"].number_format = styles['num_fmt_curr']

        ws[f"H{row}"] = f"='{tab2_name}'!M{src_row}"
        ws[f"H{row}"].font = styles['font_bold']
        ws[f"H{row}"].alignment = styles['align_center']
        ws[f"H{row}"].border = styles['thin_border']

    # 5. Gráfico de Burbujas Dinámico Cartesian Bubble Chart en I20:O35
    chart = BubbleChart()
    chart.title = "Matriz BCG Dinámica: Cuota Relativa vs Crecimiento" if lang == 'ES' else "Dynamic BCG Matrix: Relative Share vs Market Growth"
    chart.style = 13
    chart.x_axis.title = "Cuota de Mercado Relativa (CMR)" if lang == 'ES' else "Relative Market Share (RMS)"
    chart.y_axis.title = "Tasa de Crecimiento del Mercado (%)" if lang == 'ES' else "Market Growth Rate (%)"
    chart.width = 19.0
    chart.height = 12.0

    # Referencias de datos: solo las primeras 8 filas activas para visualización impecable
    xvalues = Reference(ws, min_col=4, min_row=22, max_row=29)
    yvalues = Reference(ws, min_col=5, min_row=22, max_row=29)
    size = Reference(ws, min_col=6, min_row=22, max_row=29)
    series = Series(values=yvalues, xvalues=xvalues, zvalues=size, title="Cartera UENs" if lang == 'ES' else "SBU Portfolio")
    chart.series.append(series)

    ws.add_chart(chart, "I20")

    # 6. Semáforo de Sostenibilidad Estratégica (Filas 35 a 40)
    ws['B35'] = "SEMÁFORO DE SOSTENIBILIDAD ESTRATÉGICA Y BALANCE BRUCE HENDERSON" if lang == 'ES' else "STRATEGIC SUSTAINABILITY TRAFFIC LIGHT & BRUCE HENDERSON BALANCE"
    ws['B35'].font = styles['font_section']

    semaforo_items = [
        ("B36:D36", "Superávit Neto de Generación (Vacas)" if lang == 'ES' else "Net Generation Surplus (Cash Cows)",
         f"='{tab3_name}'!F15", styles['num_fmt_curr'], styles['fill_cow']),
        ("B37:D37", "Déficit / Absorción de Crecimiento (Interrogantes)" if lang == 'ES' else "Deficit / Growth Funding (Question Marks)",
         f"='{tab3_name}'!F16", styles['num_fmt_curr'], styles['fill_question']),
        ("B38:D38", "Flujo Neto de Reinversión de Cartera" if lang == 'ES' else "Net Portfolio Reinvestment Balance",
         "=E36+E37", styles['num_fmt_curr'], styles['fill_card_bg']),
        ("B39:D39", "Diagnóstico Ejecutivo para el Comité" if lang == 'ES' else "Executive Boardroom Diagnosis",
         f'=IF(E38>=0, "EQUILIBRADO: El superávit de vacas financia holgadamente la expansión", "DÉFICIT CRÍTICO: Las interrogantes consumen más caja de la generada por las vacas")' if lang == 'ES' else
         f'=IF(E38>=0, "SUSTAINABLE: Cash Cow surplus comfortably funds growth expansion", "CRITICAL DEFICIT: Question Marks consume more cash than Cash Cows generate")',
         None, styles['fill_light_bg']),
    ]

    for rng, label, formula, fmt, fill_color in semaforo_items:
        ws.merge_cells(rng)
        first_cell = ws[rng.split(':')[0]]
        first_cell.value = label
        first_cell.font = styles['font_bold']
        first_cell.alignment = styles['align_left']
        first_cell.fill = fill_color
        first_cell.border = styles['thin_border']

        val_cell = ws[f"E{rng.split(':')[0][1:]}"]
        val_cell.value = formula
        val_cell.font = styles['font_bold']
        val_cell.alignment = styles['align_right'] if fmt else styles['align_left']
        val_cell.fill = fill_color
        val_cell.border = styles['thin_border']
        if fmt:
            val_cell.number_format = fmt

    # Anchos de columna
    col_widths = {
        'A': 4,
        'B': 24,
        'C': 32,
        'D': 18,
        'E': 18,
        'F': 20,
        'G': 18,
        'H': 46,
        'I': 18,
        'J': 18,
        'K': 20,
        'L': 18,
        'M': 18,
        'N': 18,
        'O': 18,
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    apply_sheet_protection(ws)


# ==============================================================================
# TAB 2: EVALUACIÓN CARTERA UENS / BUSINESS UNITS ASSESSMENT
# ==============================================================================
def build_tab2_evaluation(wb, ws, lang='ES'):
    styles = get_base_styles(lang)
    ws.title = "Evaluación Cartera UENs" if lang == 'ES' else "Business Units Assessment"
    ws.views.sheetView[0].showGridLines = True

    # 1. Cabecera
    ws['B2'] = "DATALARIA | EVALUACIÓN CUANTITATIVA DE CARTERA"
    ws['B2'].font = styles['font_title']

    ws['B3'] = ("REGISTRO Y EVALUACIÓN DE UNIDADES ESTRATÉGICAS DE NEGOCIO (UENS)"
                if lang == 'ES' else
                "STRATEGIC BUSINESS UNITS (SBUS) QUANTITATIVE REGISTRY & AUDIT")
    ws['B3'].font = styles['font_subtitle']

    ws['B4'] = ("Introduzca en las celdas en blanco los datos de cada UEN. Las fórmulas clasificarán automáticamente el cuadrante BCG."
                if lang == 'ES' else
                "Enter business unit data into the white unlocked cells. Mathematical formulas will automatically assign the BCG quadrant.")
    ws['B4'].font = styles['font_meta']

    # 2. Encabezados de Tabla (Fila 11)
    headers = [
        ("B11", "ID UEN" if lang == 'ES' else "SBU ID"),
        ("C11", "Nombre de la Unidad Estratégica (UEN)" if lang == 'ES' else "Strategic Business Unit Name"),
        ("D11", "Descripción / Línea de Mercado" if lang == 'ES' else "Description / Market Segment"),
        ("E11", "Facturación Propia (€)" if lang == 'ES' else "Own Revenue ($)"),
        ("F11", "Ventas Líder Comp. (€)" if lang == 'ES' else "Leading Competitor Sales ($)"),
        ("G11", "Cuota Relativa (CMR)" if lang == 'ES' else "Relative Share (RMS)"),
        ("H11", "Tasa Crec. Mercado %" if lang == 'ES' else "Market Growth Rate %"),
        ("I11", "Margen EBITDA %" if lang == 'ES' else "EBITDA Margin %"),
        ("J11", "EBITDA Generado (€)" if lang == 'ES' else "EBITDA Generated ($)"),
        ("K11", "FCF Neto Generado (€)" if lang == 'ES' else "Net FCF Generated ($)"),
        ("L11", "% Ventas Cartera" if lang == 'ES' else "% Portfolio Revenue"),
        ("M11", "Cuadrante BCG" if lang == 'ES' else "BCG Quadrant"),
    ]

    for cell_id, text in headers:
        ws[cell_id] = text
        ws[cell_id].font = styles['font_header']
        ws[cell_id].fill = styles['fill_navy_hdr']
        ws[cell_id].alignment = styles['align_center_wrap']
        ws[cell_id].border = styles['header_border']

    # Datos canónicos de las 8 UENs del Holding Industrial Nexus
    data_es = [
        ("UEN-01", "Robótica Autónoma & Visión IA", "Maquinaria industrial con guiado autónomo e inspección óptica", 18500000, 14800000, 0.185, 0.220, 650000),
        ("UEN-02", "Plataforma SaaS Industrial IoT", "Telemetría cloud y gemelos digitales para plantas fabriles", 12200000, 10500000, 0.240, 0.250, 280000),
        ("UEN-03", "Sistemas Hidráulicos de Potencia", "Cilindros de alta presión y bombas para minería y siderurgia", 32000000, 16000000, 0.035, 0.200, 4850000),
        ("UEN-04", "Motores de Combustión Industrial", "Generadores diésel de emergencia y motores para cogeneración", 24500000, 17500000, 0.020, 0.180, 3200000),
        ("UEN-05", "Baterías de Estado Sólido & Storage", "Celdas de alta densidad energética y módulos de carga rápida", 6500000, 18500000, 0.320, 0.060, -2150000),
        ("UEN-06", "Sensorización Láser Cuántica", "Metrología de submicra y sensores ópticos interferométricos", 3800000, 15200000, 0.210, 0.040, -1450000),
        ("UEN-07", "Cableado Convencional de Cobre", "Arneses eléctricos para maquinaria agrícola y naval", 5200000, 20800000, 0.010, 0.050, -180000),
        ("UEN-08", "Válvulas Neumáticas Analógicas", "Componentes de corte de fluido sin instrumentación digital", 4300000, 14300000, -0.015, 0.070, 90000),
    ]

    data_en = [
        ("SBU-01", "Autonomous Robotics & AI Vision", "Industrial machinery with autonomous guidance and optical inspection", 18500000, 14800000, 0.185, 0.220, 650000),
        ("SBU-02", "Industrial IoT SaaS Platform", "Cloud telemetry and digital twins for manufacturing plants", 12200000, 10500000, 0.240, 0.250, 280000),
        ("SBU-03", "Heavy Hydraulic Power Systems", "High-pressure cylinders and pumps for mining and metallurgy", 32000000, 16000000, 0.035, 0.200, 4850000),
        ("SBU-04", "Industrial Combustion Engines", "Emergency diesel generators and cogeneration thermal engines", 24500000, 17500000, 0.020, 0.180, 3200000),
        ("SBU-05", "Solid-State Batteries & Storage", "High energy density cells and ultra-fast charging modules", 6500000, 18500000, 0.320, 0.060, -2150000),
        ("SBU-06", "Quantum Laser Sensing Systems", "Sub-micron metrology and interferometric optical sensors", 3800000, 15200000, 0.210, 0.040, -1450000),
        ("SBU-07", "Conventional Copper Wiring", "Electrical harnesses for agricultural and marine equipment", 5200000, 20800000, 0.010, 0.050, -180000),
        ("SBU-08", "Analog Pneumatic Valves", "Fluid cutoff valves without digital instrumentation", 4300000, 14300000, -0.015, 0.070, 90000),
    ]

    items = data_es if lang == 'ES' else data_en

    for i in range(12):
        row = 12 + i
        if i < len(items):
            uid, uname, udesc, urev, ucomp, ugro, umarg, ufcf = items[i]
        else:
            uid = f"UEN-{i+1:02d}" if lang == 'ES' else f"SBU-{i+1:02d}"
            uname = ""
            udesc = ""
            urev = 0
            ucomp = 0
            ugro = 0
            umarg = 0
            ufcf = 0

        # Col B: ID (Fórmula o texto bloqueado)
        ws[f"B{row}"] = uid
        ws[f"B{row}"].font = styles['font_subhead']
        ws[f"B{row}"].alignment = styles['align_center']
        ws[f"B{row}"].border = styles['thin_border']
        ws[f"B{row}"].fill = styles['fill_light_bg']

        # Col C: Nombre UEN (INPUT DESBLOQUEADO)
        ws[f"C{row}"] = uname
        ws[f"C{row}"].font = styles['font_bold']
        ws[f"C{row}"].alignment = styles['align_left']
        ws[f"C{row}"].border = styles['thin_border']
        ws[f"C{row}"].fill = styles['fill_input']
        ws[f"C{row}"].protection = Protection(locked=False)

        # Col D: Descripción (INPUT DESBLOQUEADO)
        ws[f"D{row}"] = udesc
        ws[f"D{row}"].font = styles['font_regular']
        ws[f"D{row}"].alignment = styles['align_left_wrap']
        ws[f"D{row}"].border = styles['thin_border']
        ws[f"D{row}"].fill = styles['fill_input']
        ws[f"D{row}"].protection = Protection(locked=False)

        # Col E: Facturación Propia (INPUT DESBLOQUEADO)
        ws[f"E{row}"] = urev
        ws[f"E{row}"].font = styles['font_bold']
        ws[f"E{row}"].alignment = styles['align_right']
        ws[f"E{row}"].border = styles['thin_border']
        ws[f"E{row}"].fill = styles['fill_input']
        ws[f"E{row}"].number_format = styles['num_fmt_curr']
        ws[f"E{row}"].protection = Protection(locked=False)

        # Col F: Ventas Líder Competidor (INPUT DESBLOQUEADO)
        ws[f"F{row}"] = ucomp
        ws[f"F{row}"].font = styles['font_regular']
        ws[f"F{row}"].alignment = styles['align_right']
        ws[f"F{row}"].border = styles['thin_border']
        ws[f"F{row}"].fill = styles['fill_input']
        ws[f"F{row}"].number_format = styles['num_fmt_curr']
        ws[f"F{row}"].protection = Protection(locked=False)

        # Col G: CMR = Ventas Propia / Ventas Líder (FÓRMULA BLOQUEADA)
        ws[f"G{row}"] = f'=IF(F{row}>0, ROUND(E{row}/F{row}, 2), 0)'
        ws[f"G{row}"].font = styles['font_bold']
        ws[f"G{row}"].alignment = styles['align_center']
        ws[f"G{row}"].border = styles['thin_border']
        ws[f"G{row}"].number_format = styles['num_fmt_ratio']

        # Col H: Tasa Crecimiento Mercado % (INPUT DESBLOQUEADO)
        ws[f"H{row}"] = ugro
        ws[f"H{row}"].font = styles['font_bold']
        ws[f"H{row}"].alignment = styles['align_center']
        ws[f"H{row}"].border = styles['thin_border']
        ws[f"H{row}"].fill = styles['fill_input']
        ws[f"H{row}"].number_format = styles['num_fmt_pct']
        ws[f"H{row}"].protection = Protection(locked=False)

        # Col I: Margen EBITDA % (INPUT DESBLOQUEADO)
        ws[f"I{row}"] = umarg
        ws[f"I{row}"].font = styles['font_regular']
        ws[f"I{row}"].alignment = styles['align_center']
        ws[f"I{row}"].border = styles['thin_border']
        ws[f"I{row}"].fill = styles['fill_input']
        ws[f"I{row}"].number_format = styles['num_fmt_pct']
        ws[f"I{row}"].protection = Protection(locked=False)

        # Col J: EBITDA Generado = E * I (FÓRMULA BLOQUEADA)
        ws[f"J{row}"] = f'=ROUND(E{row}*I{row}, 0)'
        ws[f"J{row}"].font = styles['font_regular']
        ws[f"J{row}"].alignment = styles['align_right']
        ws[f"J{row}"].border = styles['thin_border']
        ws[f"J{row}"].number_format = styles['num_fmt_curr']

        # Col K: FCF Neto Generado (INPUT DESBLOQUEADO)
        ws[f"K{row}"] = ufcf
        ws[f"K{row}"].font = styles['font_bold']
        ws[f"K{row}"].alignment = styles['align_right']
        ws[f"K{row}"].border = styles['thin_border']
        ws[f"K{row}"].fill = styles['fill_input']
        ws[f"K{row}"].number_format = styles['num_fmt_curr']
        ws[f"K{row}"].protection = Protection(locked=False)

        # Col L: % Ventas sobre Cartera (FÓRMULA BLOQUEADA)
        ws[f"L{row}"] = f'=IF(E$24>0, E{row}/E$24, 0)'
        ws[f"L{row}"].font = styles['font_bold']
        ws[f"L{row}"].alignment = styles['align_center']
        ws[f"L{row}"].border = styles['thin_border']
        ws[f"L{row}"].number_format = styles['num_fmt_pct']

        # Col M: Clasificación Cuadrante BCG (FÓRMULA BLOQUEADA)
        # Umbral CMR = 1.0, Umbral TCM = 10% (0.10)
        if lang == 'ES':
            ws[f"M{row}"] = f'=IF(E{row}<=0, "-", IF(G{row}>=1.0, IF(H{row}>=0.10, "ESTRELLA", "VACA"), IF(H{row}>=0.10, "INTERROGANTE", "PERRO")))'
        else:
            ws[f"M{row}"] = f'=IF(E{row}<=0, "-", IF(G{row}>=1.0, IF(H{row}>=0.10, "STAR", "CASH COW"), IF(H{row}>=0.10, "QUESTION MARK", "DOG")))'
        ws[f"M{row}"].font = styles['font_bold']
        ws[f"M{row}"].alignment = styles['align_center']
        ws[f"M{row}"].border = styles['thin_border']
        ws[f"M{row}"].fill = styles['fill_light_bg']

    # Fila 24: TOTAL / CONSOLIDADO CARTERA
    ws['B24'] = "TOTAL"
    ws['B24'].font = styles['font_bold']
    ws['B24'].alignment = styles['align_center']
    ws['B24'].border = styles['total_border']

    ws['C24'] = "CONSOLIDADO CARTERA" if lang == 'ES' else "PORTFOLIO TOTAL"
    ws['C24'].font = styles['font_bold']
    ws['C24'].alignment = styles['align_left']
    ws['C24'].border = styles['total_border']

    ws['D24'] = ""
    ws['D24'].border = styles['total_border']

    ws['E24'] = "=SUM(E12:E23)"
    ws['E24'].font = styles['font_bold']
    ws['E24'].alignment = styles['align_right']
    ws['E24'].border = styles['total_border']
    ws['E24'].number_format = styles['num_fmt_curr']

    ws['F24'] = "=SUM(F12:F23)"
    ws['F24'].font = styles['font_bold']
    ws['F24'].alignment = styles['align_right']
    ws['F24'].border = styles['total_border']
    ws['F24'].number_format = styles['num_fmt_curr']

    ws['G24'] = "=IF(F24>0, ROUND(E24/F24, 2), 0)"
    ws['G24'].font = styles['font_bold']
    ws['G24'].alignment = styles['align_center']
    ws['G24'].border = styles['total_border']
    ws['G24'].number_format = styles['num_fmt_ratio']

    ws['H24'] = "=IF(E24>0, SUMPRODUCT(H12:H23, E12:E23)/E24, 0)"
    ws['H24'].font = styles['font_bold']
    ws['H24'].alignment = styles['align_center']
    ws['H24'].border = styles['total_border']
    ws['H24'].number_format = styles['num_fmt_pct']

    ws['I24'] = "=IF(E24>0, J24/E24, 0)"
    ws['I24'].font = styles['font_bold']
    ws['I24'].alignment = styles['align_center']
    ws['I24'].border = styles['total_border']
    ws['I24'].number_format = styles['num_fmt_pct']

    ws['J24'] = "=SUM(J12:J23)"
    ws['J24'].font = styles['font_bold']
    ws['J24'].alignment = styles['align_right']
    ws['J24'].border = styles['total_border']
    ws['J24'].number_format = styles['num_fmt_curr']

    ws['K24'] = "=SUM(K12:K23)"
    ws['K24'].font = styles['font_bold']
    ws['K24'].alignment = styles['align_right']
    ws['K24'].border = styles['total_border']
    ws['K24'].number_format = styles['num_fmt_curr']

    ws['L24'] = "=SUM(L12:L23)"
    ws['L24'].font = styles['font_bold']
    ws['L24'].alignment = styles['align_center']
    ws['L24'].border = styles['total_border']
    ws['L24'].number_format = styles['num_fmt_pct']

    ws['M24'] = "100.0%"
    ws['M24'].font = styles['font_bold']
    ws['M24'].alignment = styles['align_center']
    ws['M24'].border = styles['total_border']

    # Anchos de columna
    col_widths = {
        'A': 4,
        'B': 12,
        'C': 34,
        'D': 44,
        'E': 22,
        'F': 22,
        'G': 18,
        'H': 18,
        'I': 18,
        'J': 20,
        'K': 20,
        'L': 18,
        'M': 20,
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    apply_sheet_protection(ws)


# ==============================================================================
# TAB 3: MATRIZ & FLUJO DE FONDOS / BCG MATRIX & FUND FLOW
# ==============================================================================
def build_tab3_matrix_funds(wb, ws, lang='ES'):
    styles = get_base_styles(lang)
    ws.title = "Matriz & Flujo de Fondos" if lang == 'ES' else "BCG Matrix & Fund Flow"
    ws.views.sheetView[0].showGridLines = True

    # 1. Cabecera
    ws['B2'] = "DATALARIA | DINÁMICA DE CARTERA & MODELO DE FONDOS"
    ws['B2'].font = styles['font_title']

    ws['B3'] = ("CLASIFICACIÓN MATEMÁTICA Y BALANCE DE FONDOS DE BRUCE HENDERSON"
                if lang == 'ES' else
                "MATHEMATICAL CLASSIFICATION & BRUCE HENDERSON CASH FLOW BALANCE")
    ws['B3'].font = styles['font_subtitle']

    ws['B4'] = ("Auditoría del superávit de liquidez y simulación de la regla dorada: Vacas financian Interrogantes con potencial de liderazgo."
                if lang == 'ES' else
                "Cash flow surplus audit and golden rule simulation: Cash Cows finance high-potential Question Marks into Stars.")
    ws['B4'].font = styles['font_meta']

    tab2_name = 'Evaluación Cartera UENs' if lang == 'ES' else 'Business Units Assessment'

    # 2. Tabla de Clasificación Matemática en 4 Cuadrantes (Filas 11 a 19)
    ws['B11'] = "1. DESGLOSE CUANTITATIVO DE FLUJO DE FONDOS POR CUADRANTE" if lang == 'ES' else "1. QUANTITATIVE CASH FLOW BREAKDOWN BY QUADRANT"
    ws['B11'].font = styles['font_section']

    headers_funds = [
        ("B13", "Nº UENs" if lang == 'ES' else "SBUs #"),
        ("C13", "Facturación Total (€)" if lang == 'ES' else "Total Revenue ($)"),
        ("D13", "% Cartera" if lang == 'ES' else "% Portfolio"),
        ("E13", "EBITDA Consolidado (€)" if lang == 'ES' else "Consolidated EBITDA ($)"),
        ("F13", "Flujo Caja Libre (FCF) (€)" if lang == 'ES' else "Free Cash Flow (FCF) ($)"),
        ("G13", "Rol en el Balance de Henderson" if lang == 'ES' else "Role in Henderson Balance"),
    ]

    ws['A13'] = "Cuadrante" if lang == 'ES' else "Quadrant"
    ws['A13'].font = styles['font_header']
    ws['A13'].fill = styles['fill_navy_hdr']
    ws['A13'].alignment = styles['align_center']
    ws['A13'].border = styles['header_border']

    for cell_id, text in headers_funds:
        ws[cell_id] = text
        ws[cell_id].font = styles['font_header']
        ws[cell_id].fill = styles['fill_navy_hdr']
        ws[cell_id].alignment = styles['align_center_wrap']
        ws[cell_id].border = styles['header_border']

    q_labels = [
        (14, "ESTRELLA" if lang == 'ES' else "STAR",
         "⭐ ESTRELLAS (Alta Cuota, Alto Crecimiento)" if lang == 'ES' else "⭐ STARS (High Share, High Growth)",
         "Autosuficiente / Reinversión Alta" if lang == 'ES' else "Self-sufficient / High Reinvestment",
         styles['fill_star'], Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_STAR_TEXT)),

        (15, "VACA" if lang == 'ES' else "CASH COW",
         "🐄 VACAS (Alta Cuota, Bajo Crecimiento)" if lang == 'ES' else "🐄 CASH COWS (High Share, Low Growth)",
         "Generador Masivo de Liquidez (Ordeñar)" if lang == 'ES' else "Massive Cash Generator (Milk)",
         styles['fill_cow'], Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_COW_TEXT)),

        (16, "INTERROGANTE" if lang == 'ES' else "QUESTION MARK",
         "❓ INTERROGANTES (Baja Cuota, Alto Crecimiento)" if lang == 'ES' else "❓ QUESTION MARKS (Low Share, High Growth)",
         "Consumidor Neto de Capital (Decidir)" if lang == 'ES' else "Net Capital Consumer (Decide)",
         styles['fill_question'], Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_QUESTION_TEXT)),

        (17, "PERRO" if lang == 'ES' else "DOG",
         "🐕 PERROS (Baja Cuota, Bajo Crecimiento)" if lang == 'ES' else "🐕 DOGS (Low Share, Low Growth)",
         "Trampa de Liquidez (Desinvertir / Cosechar)" if lang == 'ES' else "Liquidity Trap (Divest / Harvest)",
         styles['fill_dog'], Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_DOG_TEXT)),
    ]

    for row_idx, q_code, q_full_name, role_text, fill_q, font_q in q_labels:
        ws[f"A{row_idx}"] = q_full_name
        ws[f"A{row_idx}"].font = font_q
        ws[f"A{row_idx}"].fill = fill_q
        ws[f"A{row_idx}"].alignment = styles['align_left']
        ws[f"A{row_idx}"].border = styles['thin_border']

        # Nº UENs con COUNTIF
        ws[f"B{row_idx}"] = f'=COUNTIF(\'{tab2_name}\'!M12:M23, "{q_code}")'
        ws[f"B{row_idx}"].font = styles['font_bold']
        ws[f"B{row_idx}"].fill = fill_q
        ws[f"B{row_idx}"].alignment = styles['align_center']
        ws[f"B{row_idx}"].border = styles['thin_border']
        ws[f"B{row_idx}"].number_format = styles['num_fmt_int']

        # Facturación con SUMIF
        ws[f"C{row_idx}"] = f'=SUMIF(\'{tab2_name}\'!M12:M23, "{q_code}", \'{tab2_name}\'!E12:E23)'
        ws[f"C{row_idx}"].font = styles['font_regular']
        ws[f"C{row_idx}"].fill = fill_q
        ws[f"C{row_idx}"].alignment = styles['align_right']
        ws[f"C{row_idx}"].border = styles['thin_border']
        ws[f"C{row_idx}"].number_format = styles['num_fmt_curr']

        # % Cartera
        ws[f"D{row_idx}"] = f'=IF(\'{tab2_name}\'!E24>0, C{row_idx}/\'{tab2_name}\'!E24, 0)'
        ws[f"D{row_idx}"].font = styles['font_bold']
        ws[f"D{row_idx}"].fill = fill_q
        ws[f"D{row_idx}"].alignment = styles['align_center']
        ws[f"D{row_idx}"].border = styles['thin_border']
        ws[f"D{row_idx}"].number_format = styles['num_fmt_pct']

        # EBITDA con SUMIF
        ws[f"E{row_idx}"] = f'=SUMIF(\'{tab2_name}\'!M12:M23, "{q_code}", \'{tab2_name}\'!J12:J23)'
        ws[f"E{row_idx}"].font = styles['font_regular']
        ws[f"E{row_idx}"].fill = fill_q
        ws[f"E{row_idx}"].alignment = styles['align_right']
        ws[f"E{row_idx}"].border = styles['thin_border']
        ws[f"E{row_idx}"].number_format = styles['num_fmt_curr']

        # FCF con SUMIF
        ws[f"F{row_idx}"] = f'=SUMIF(\'{tab2_name}\'!M12:M23, "{q_code}", \'{tab2_name}\'!K12:K23)'
        ws[f"F{row_idx}"].font = styles['font_bold']
        ws[f"F{row_idx}"].fill = fill_q
        ws[f"F{row_idx}"].alignment = styles['align_right']
        ws[f"F{row_idx}"].border = styles['thin_border']
        ws[f"F{row_idx}"].number_format = styles['num_fmt_curr']

        # Rol de Balance
        ws[f"G{row_idx}"] = role_text
        ws[f"G{row_idx}"].font = styles['font_subhead']
        ws[f"G{row_idx}"].fill = fill_q
        ws[f"G{row_idx}"].alignment = styles['align_left']
        ws[f"G{row_idx}"].border = styles['thin_border']

    # Fila 18: TOTAL CONSOLIDADO
    ws['A18'] = "TOTAL CARTERA" if lang == 'ES' else "PORTFOLIO TOTAL"
    ws['A18'].font = styles['font_bold']
    ws['A18'].alignment = styles['align_left']
    ws['A18'].border = styles['total_border']

    ws['B18'] = "=SUM(B14:B17)"
    ws['B18'].font = styles['font_bold']
    ws['B18'].alignment = styles['align_center']
    ws['B18'].border = styles['total_border']
    ws['B18'].number_format = styles['num_fmt_int']

    ws['C18'] = "=SUM(C14:C17)"
    ws['C18'].font = styles['font_bold']
    ws['C18'].alignment = styles['align_right']
    ws['C18'].border = styles['total_border']
    ws['C18'].number_format = styles['num_fmt_curr']

    ws['D18'] = "=SUM(D14:D17)"
    ws['D18'].font = styles['font_bold']
    ws['D18'].alignment = styles['align_center']
    ws['D18'].border = styles['total_border']
    ws['D18'].number_format = styles['num_fmt_pct']

    ws['E18'] = "=SUM(E14:E17)"
    ws['E18'].font = styles['font_bold']
    ws['E18'].alignment = styles['align_right']
    ws['E18'].border = styles['total_border']
    ws['E18'].number_format = styles['num_fmt_curr']

    ws['F18'] = "=SUM(F14:F17)"
    ws['F18'].font = styles['font_bold']
    ws['F18'].alignment = styles['align_right']
    ws['F18'].border = styles['total_border']
    ws['F18'].number_format = styles['num_fmt_curr']

    ws['G18'] = ("Balance Neto Positivo (Superávit de Liquidez)" if lang == 'ES' else "Positive Net Balance (Liquidity Surplus)")
    ws['G18'].font = styles['font_bold']
    ws['G18'].alignment = styles['align_left']
    ws['G18'].border = styles['total_border']

    # 3. Simulación de la Regla Dorada de Reinversión de Henderson (Filas 21 a 28)
    ws['B21'] = "2. PARÁMETROS CANÓNICOS BCG & CURVA DE EXPERIENCIA" if lang == 'ES' else "2. CANONICAL BCG PARAMETERS & EXPERIENCE CURVE"
    ws['B21'].font = styles['font_section']

    params = [
        ("B23:D23", "Umbral de Cuota de Mercado Relativa (CMR)", "1.00x", "CMR ≥ 1.0x define liderazgo en costes por efecto escala"),
        ("B24:D24", "Umbral de Crecimiento del Mercado (TCM)", "10.0%", "TCM ≥ 10% exige reinversión intensiva en capacidad fabril"),
        ("B25:D25", "Tasa de Curva de Aprendizaje (Henderson)", "80.0%", "20% reducción de costes por cada duplicación de volumen acumulado"),
        ("B26:D26", "Coeficiente de Elasticidad de Coste (b)", "=ROUND(-LN(E25)/LN(2), 3)", "Exponente b de la ley de potencias: C(n) = C(1) * n^(-b)"),
    ] if lang == 'ES' else [
        ("B23:D23", "Relative Market Share Threshold (RMS)", "1.00x", "RMS ≥ 1.0x establishes cost leadership via scale economics"),
        ("B24:D24", "Market Growth Rate Threshold (MGR)", "10.0%", "MGR ≥ 10% demands high reinvestment in operational capacity"),
        ("B25:D25", "Learning Curve Progress Ratio (Henderson)", "80.0%", "20% unit cost reduction per doubling of cumulative volume"),
        ("B26:D26", "Cost Learning Elasticity Coefficient (b)", "=ROUND(-LN(E25)/LN(2), 3)", "Power-law exponent b: C(n) = C(1) * n^(-b)"),
    ]

    for rng, p_label, p_val, p_desc in params:
        ws.merge_cells(rng)
        first_cell = ws[rng.split(':')[0]]
        first_cell.value = p_label
        first_cell.font = styles['font_bold']
        first_cell.alignment = styles['align_left']
        first_cell.fill = styles['fill_light_bg']
        first_cell.border = styles['thin_border']

        val_cell = ws[f"E{rng.split(':')[0][1:]}"]
        val_cell.value = p_val
        val_cell.font = styles['font_bold']
        val_cell.alignment = styles['align_center']
        val_cell.fill = styles['fill_input'] if not str(p_val).startswith('=') else styles['fill_card_bg']
        val_cell.border = styles['thin_border']
        if not str(p_val).startswith('='):
            val_cell.protection = Protection(locked=False)

        desc_cell = ws[f"F{rng.split(':')[0][1:]}"]
        ws.merge_cells(f"F{rng.split(':')[0][1:]}:G{rng.split(':')[0][1:]}")
        desc_cell.value = p_desc
        desc_cell.font = styles['font_regular']
        desc_cell.alignment = styles['align_left']
        desc_cell.fill = styles['fill_light_bg']
        desc_cell.border = styles['thin_border']

    # 4. Matriz de Transición Estratégica a 3 Años (Filas 30 a 39)
    ws['B30'] = "3. TRAYECTORIA Y TRANSICIÓN ESTRATÉGICA DE UENS (3 AÑOS)" if lang == 'ES' else "3. SBU STRATEGIC TRANSITION & TRAJECTORY (3-YEAR HORIZON)"
    ws['B30'].font = styles['font_section']

    headers_trans = [
        ("A31", "ID"),
        ("B31", "Unidad Estratégica (UEN)" if lang == 'ES' else "Strategic Business Unit"),
        ("C31", "Cuadrante Actual" if lang == 'ES' else "Current Quadrant"),
        ("D31", "Cuadrante Objetivo a 3 Años" if lang == 'ES' else "3-Year Target Quadrant"),
        ("E31", "Vector de Trayectoria Estratégica" if lang == 'ES' else "Strategic Trajectory Vector"),
        ("F31", "CAPEX / Liquidez Asignada (€)" if lang == 'ES' else "Reallocated CAPEX ($)"),
        ("G31", "Impacto Proyectado en EBITDA (€)" if lang == 'ES' else "Projected EBITDA Impact ($)"),
    ]

    for cell_id, text in headers_trans:
        ws[cell_id] = text
        ws[cell_id].font = styles['font_header']
        ws[cell_id].fill = styles['fill_navy_sub']
        ws[cell_id].alignment = styles['align_center']
        ws[cell_id].border = styles['header_border']

    trans_es = [
        ("UEN-01", "Robótica Autónoma & Visión IA", "ESTRELLA", "VACA LECHERA", "Consolidar cuota en maduración; transición a generador de FCF", 1200000, 1850000),
        ("UEN-02", "Plataforma SaaS Industrial IoT", "ESTRELLA", "ESTRELLA", "Expandir red internacional y retener liderazgo (CMR > 1.3x)", 850000, 1400000),
        ("UEN-03", "Sistemas Hidráulicos de Potencia", "VACA LECHERA", "VACA LECHERA", "Ordeño disciplinado; mantener cuota con CAPEX mínimo", -3500000, 250000),
        ("UEN-04", "Motores de Combustión Industrial", "VACA LECHERA", "VACA LECHERA", "Optimizar capital circulante y ordeñar flujos para I+D", -2200000, 180000),
        ("UEN-05", "Baterías de Estado Sólido & Storage", "INTERROGANTE", "ESTRELLA", "Inyección agresiva de 2,8 M€ para superar cuota del líder (CMR > 1.0x)", 2800000, 2400000),
        ("UEN-06", "Sensorización Láser Cuántica", "INTERROGANTE", "ALIANZA / DESINVERSIÓN", "Buscar socio de coinversión o desinvertir; evitar sangría de caja", -400000, 650000),
        ("UEN-07", "Cableado Convencional de Cobre", "PERRO", "DESINVERSIÓN (VENTA)", "Mandato de venta de activos a competidor; liberar capital circulante", -3200000, 380000),
        ("UEN-08", "Válvulas Neumáticas Analógicas", "PERRO", "COSECHA & CIERRE", "Cosecha acelerada en 2026 y reasignación de ingenieros a robótica", -650000, 220000),
    ]

    trans_en = [
        ("SBU-01", "Autonomous Robotics & AI Vision", "STAR", "CASH COW", "Consolidate share as market matures; transition to FCF engine", 1200000, 1850000),
        ("SBU-02", "Industrial IoT SaaS Platform", "STAR", "STAR", "Scale international partner network and defend RMS > 1.3x", 850000, 1400000),
        ("SBU-03", "Heavy Hydraulic Power Systems", "CASH COW", "CASH COW", "Disciplined milking; preserve share with minimal sustaining CAPEX", -3500000, 250000),
        ("SBU-04", "Industrial Combustion Engines", "CASH COW", "CASH COW", "Optimize net working capital and milk cash to fund innovation", -2200000, 180000),
        ("SBU-05", "Solid-State Batteries & Storage", "QUESTION MARK", "STAR", "Aggressive €2.8M capital injection to cross RMS > 1.0x threshold", 2800000, 2400000),
        ("SBU-06", "Quantum Laser Sensing Systems", "QUESTION MARK", "JV / DIVESTMENT", "Secure joint venture partner or divest; stop liquidity drain", -400000, 650000),
        ("SBU-07", "Conventional Copper Wiring", "DOG", "DIVESTMENT (SALE)", "M&A mandate to sell assets to competitor; release working capital", -3200000, 380000),
        ("SBU-08", "Analog Pneumatic Valves", "DOG", "HARVEST & SUNSET", "Accelerated harvesting in 2026 and redeploy engineering talent", -650000, 220000),
    ]

    trans_data = trans_es if lang == 'ES' else trans_en

    for i, t_row in enumerate(trans_data):
        row = 32 + i
        t_id, t_name, t_cur, t_tgt, t_vec, t_cap, t_eb = t_row

        ws[f"A{row}"] = t_id
        ws[f"A{row}"].font = styles['font_subhead']
        ws[f"A{row}"].alignment = styles['align_center']
        ws[f"A{row}"].border = styles['thin_border']
        ws[f"A{row}"].fill = styles['fill_light_bg']

        ws[f"B{row}"] = t_name
        ws[f"B{row}"].font = styles['font_bold']
        ws[f"B{row}"].alignment = styles['align_left']
        ws[f"B{row}"].border = styles['thin_border']

        ws[f"C{row}"] = t_cur
        ws[f"C{row}"].font = styles['font_bold']
        ws[f"C{row}"].alignment = styles['align_center']
        ws[f"C{row}"].border = styles['thin_border']

        ws[f"D{row}"] = t_tgt
        ws[f"D{row}"].font = styles['font_bold']
        ws[f"D{row}"].alignment = styles['align_center']
        ws[f"D{row}"].border = styles['thin_border']
        ws[f"D{row}"].fill = styles['fill_light_bg']

        ws[f"E{row}"] = t_vec
        ws[f"E{row}"].font = styles['font_regular']
        ws[f"E{row}"].alignment = styles['align_left_wrap']
        ws[f"E{row}"].border = styles['thin_border']

        ws[f"F{row}"] = t_cap
        ws[f"F{row}"].font = styles['font_bold']
        ws[f"F{row}"].alignment = styles['align_right']
        ws[f"F{row}"].border = styles['thin_border']
        ws[f"F{row}"].number_format = styles['num_fmt_curr']

        ws[f"G{row}"] = t_eb
        ws[f"G{row}"].font = styles['font_bold']
        ws[f"G{row}"].alignment = styles['align_right']
        ws[f"G{row}"].border = styles['thin_border']
        ws[f"G{row}"].number_format = styles['num_fmt_curr']

    # Fila Total Transición
    ws['A40'] = "TOTAL"
    ws['A40'].font = styles['font_bold']
    ws['A40'].alignment = styles['align_center']
    ws['A40'].border = styles['total_border']

    ws['B40'] = "REASIGNACIÓN NETA DE FONDOS" if lang == 'ES' else "NET REALLOCATION OF FUNDS"
    ws['B40'].font = styles['font_bold']
    ws['B40'].alignment = styles['align_left']
    ws['B40'].border = styles['total_border']

    ws['C40'] = ""
    ws['C40'].border = styles['total_border']
    ws['D40'] = ""
    ws['D40'].border = styles['total_border']
    ws['E40'] = ""
    ws['E40'].border = styles['total_border']

    ws['F40'] = "=SUM(F32:F39)"
    ws['F40'].font = styles['font_bold']
    ws['F40'].alignment = styles['align_right']
    ws['F40'].border = styles['total_border']
    ws['F40'].number_format = styles['num_fmt_curr']

    ws['G40'] = "=SUM(G32:G39)"
    ws['G40'].font = styles['font_bold']
    ws['G40'].alignment = styles['align_right']
    ws['G40'].border = styles['total_border']
    ws['G40'].number_format = styles['num_fmt_curr']

    # Anchos de columna
    col_widths = {
        'A': 32,
        'B': 34,
        'C': 24,
        'D': 24,
        'E': 36,
        'F': 26,
        'G': 44,
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    apply_sheet_protection(ws)


# ==============================================================================
# TAB 4: PLAN DE ASIGNACIÓN DE CAPITAL / CAPITAL ALLOCATION PLAN
# ==============================================================================
def build_tab4_capital_plan(wb, ws, lang='ES'):
    styles = get_base_styles(lang)
    ws.title = "Plan de Asignación de Capital" if lang == 'ES' else "Capital Allocation Plan"
    ws.views.sheetView[0].showGridLines = True

    # 1. Cabecera
    ws['B2'] = "DATALARIA | ROADMAP DE CAPITAL & GOBERNANZA C-LEVEL"
    ws['B2'].font = styles['font_title']

    ws['B3'] = ("PLAN EJECUTIVO DE REASIGNACIÓN DE CAPITAL Y DESINVERSIÓN (2026)"
                if lang == 'ES' else
                "EXECUTIVE CAPITAL REALLOCATION & DIVESTMENT ROADMAP (2026)")
    ws['B3'].font = styles['font_subtitle']

    ws['B4'] = ("Iniciativas de CAPEX, desinversión de Perros y financiamiento de Interrogantes sujetas a aprobación del Consejo de Administración."
                if lang == 'ES' else
                "CAPEX reallocation, Dog divestment and Question Mark scaling initiatives subject to Board of Directors approval.")
    ws['B4'].font = styles['font_meta']

    # 2. Encabezados de Tabla (Fila 11)
    headers = [
        ("B11", "ID"),
        ("C11", "UEN / Activo Destino" if lang == 'ES' else "Target SBU / Asset"),
        ("D11", "Cuadrante" if lang == 'ES' else "Quadrant"),
        ("E11", "Acción Estratégica" if lang == 'ES' else "Strategic Action"),
        ("F11", "Descripción de la Iniciativa de Capital" if lang == 'ES' else "Capital Initiative Description"),
        ("G11", "Owner C-Level" if lang == 'ES' else "C-Level Owner"),
        ("H11", "Plazo / Hito" if lang == 'ES' else "Timeline / Milestone"),
        ("I11", "Presupuesto (€)" if lang == 'ES' else "Budget ($)"),
        ("J11", "EBITDA Proyectado (€)" if lang == 'ES' else "Projected EBITDA ($)"),
        ("K11", "KPI de Impacto / Criterio de Éxito" if lang == 'ES' else "Impact KPI / Success Metric"),
        ("L11", "Estado" if lang == 'ES' else "Status"),
    ]

    for cell_id, text in headers:
        ws[cell_id] = text
        ws[cell_id].font = styles['font_header']
        ws[cell_id].fill = styles['fill_navy_hdr']
        ws[cell_id].alignment = styles['align_center_wrap']
        ws[cell_id].border = styles['header_border']

    initiatives_es = [
        ("CAP-01", "Robótica Autónoma & Visión IA", "ESTRELLA", "Invertir (CAPEX)",
         "Ampliación de capacidad fabril para líneas de visión artificial y nuevos robots AGV",
         "COO", "Q1-Q2 2026", 1200000, 1850000, "Cuota relativa CMR > 1.35x | ROIC > 22%", "Aprobado Consejo"),

        ("CAP-02", "Plataforma SaaS Industrial IoT", "ESTRELLA", "Invertir (I+D)",
         "Despliegue de red de conectores industriales y gemelos digitales con IA generativa",
         "CTO", "Q2-Q3 2026", 850000, 1400000, "ARR +45% | Churn neto < 4%", "Aprobado Consejo"),

        ("CAP-03", "Baterías Estado Sólido & Storage", "INTERROGANTE", "Escalar (Vaca -> Star)",
         "Inyección estratégica masiva de CAPEX financiada con flujos de UEN-03 para alcanzar liderazgo",
         "CEO", "Q1-Q4 2026", 2800000, 2400000, "CMR pasa de 0.35x a 1.05x | Escala industrial", "Prioridad Máxima"),

        ("CAP-04", "Sensorización Láser Cuántica", "INTERROGANTE", "Joint Venture / Socio",
         "Búsqueda de socio industrial internacional para compartir CAPEX de I+D sin sangría de FCF",
         "CBO", "Q2-Q3 2026", -400000, 650000, "Acuerdo de coinversión del 50% firmado", "En Negociación"),

        ("CAP-05", "Sistemas Hidráulicos de Potencia", "VACA LECHERA", "Ordeñar (FCF)",
         "Optimización de costes operativos y congelación de CAPEX expansivo; retención estricta de cuota",
         "CFO", "Q1-Q4 2026", -3500000, 250000, "Generación neta de FCF > 4.8 M€ transferida a holding", "Ejecución Continua"),

        ("CAP-06", "Motores Combustión Industrial", "VACA LECHERA", "Ordeñar (Circulante)",
         "Reducción de inventario de componentes y renegociación de proveedores para liberar liquidez",
         "COO", "Q1-Q3 2026", -2200000, 180000, "Liberación de 2.2 M€ en NWC antes de Q3", "Ejecución Continua"),

        ("CAP-07", "Cableado Convencional de Cobre", "PERRO", "Desinvertir (M&A)",
         "Mandato formal de venta de maquinaria, patentes e inventario a competidor regional",
         "M&A Lead", "Q2-Q3 2026", -3200000, 380000, "Ingreso de desinversión > 3.0 M€ en caja holding", "Mandato Activo"),

        ("CAP-08", "Válvulas Neumáticas Analógicas", "PERRO", "Cosecha & Cierre",
         "Cese gradual de fabricación, venta de stock residual y recolocación de técnicos en robótica",
         "COO", "Q3-Q4 2026", -650000, 220000, "Cierre ordenado sin indemnizaciones extraordinarias", "Planificado Q3"),
    ]

    initiatives_en = [
        ("CAP-01", "Autonomous Robotics & AI Vision", "STAR", "Invest (CAPEX)",
         "Capacity expansion for optical inspection robotics lines and automated AGVs",
         "COO", "Q1-Q2 2026", 1200000, 1850000, "Relative share RMS > 1.35x | ROIC > 22%", "Board Approved"),

        ("CAP-02", "Industrial IoT SaaS Platform", "STAR", "Invest (R&D)",
         "Deployment of industrial connector ecosystems and generative digital twins",
         "CTO", "Q2-Q3 2026", 850000, 1400000, "ARR +45% | Net churn < 4%", "Board Approved"),

        ("CAP-03", "Solid-State Batteries & Storage", "QUESTION MARK", "Scale (Push to Star)",
         "Massive CAPEX funding powered by Cash Cow cash surplus to cross leadership threshold",
         "CEO", "Q1-Q4 2026", 2800000, 2400000, "RMS shifts from 0.35x to 1.05x | Scale achieved", "Top Priority"),

        ("CAP-04", "Quantum Laser Sensing Systems", "QUESTION MARK", "Joint Venture / Partner",
         "Target strategic co-investor to share R&D capital intensity and stop cash burn",
         "CBO", "Q2-Q3 2026", -400000, 650000, "50% co-investment JV agreement signed", "In Negotiation"),

        ("CAP-05", "Heavy Hydraulic Power Systems", "CASH COW", "Milk (FCF Extraction)",
         "Operational cost freeze and ring-fencing maintenance CAPEX; pure cash harvesting",
         "CFO", "Q1-Q4 2026", -3500000, 250000, "Net FCF generation > $4.8M remitted to holding", "Ongoing Milking"),

        ("CAP-06", "Industrial Combustion Engines", "CASH COW", "Milk (Working Capital)",
         "Lean inventory reduction and supplier payment optimization to free up liquidity",
         "COO", "Q1-Q3 2026", -2200000, 180000, "Release $2.2M working capital before Q3", "Ongoing Milking"),

        ("CAP-07", "Conventional Copper Wiring", "DOG", "Divest (M&A Mandate)",
         "Formal carve-out sale of plant equipment, inventory, and contracts to rival competitor",
         "M&A Lead", "Q2-Q3 2026", -3200000, 380000, "Net divestment proceeds > $3.0M credited to group", "Mandate Active"),

        ("CAP-08", "Analog Pneumatic Valves", "DOG", "Harvest & Sunset",
         "Phased wind-down of legacy lines, stock liquidation, and engineering redeployment to robotics",
         "COO", "Q3-Q4 2026", -650000, 220000, "Clean plant shutdown with zero severance penalties", "Planned Q3"),
    ]

    items = initiatives_es if lang == 'ES' else initiatives_en

    for i, item in enumerate(items):
        row = 12 + i
        cid, ctarget, cquad, cact, cdesc, cown, ctime, cbud, ceb, ckpi, cstat = item

        # Col B: ID
        ws[f"B{row}"] = cid
        ws[f"B{row}"].font = styles['font_subhead']
        ws[f"B{row}"].alignment = styles['align_center']
        ws[f"B{row}"].border = styles['thin_border']
        ws[f"B{row}"].fill = styles['fill_light_bg']

        # Col C: UEN Destino (INPUT DESBLOQUEADO)
        ws[f"C{row}"] = ctarget
        ws[f"C{row}"].font = styles['font_bold']
        ws[f"C{row}"].alignment = styles['align_left']
        ws[f"C{row}"].border = styles['thin_border']
        ws[f"C{row}"].fill = styles['fill_input']
        ws[f"C{row}"].protection = Protection(locked=False)

        # Col D: Cuadrante (INPUT DESBLOQUEADO)
        ws[f"D{row}"] = cquad
        ws[f"D{row}"].font = styles['font_subhead']
        ws[f"D{row}"].alignment = styles['align_center']
        ws[f"D{row}"].border = styles['thin_border']
        ws[f"D{row}"].fill = styles['fill_input']
        ws[f"D{row}"].protection = Protection(locked=False)

        # Col E: Acción Estratégica (INPUT DESBLOQUEADO)
        ws[f"E{row}"] = cact
        ws[f"E{row}"].font = styles['font_bold']
        ws[f"E{row}"].alignment = styles['align_center']
        ws[f"E{row}"].border = styles['thin_border']
        ws[f"E{row}"].fill = styles['fill_input']
        ws[f"E{row}"].protection = Protection(locked=False)

        # Col F: Descripción (INPUT DESBLOQUEADO)
        ws[f"F{row}"] = cdesc
        ws[f"F{row}"].font = styles['font_regular']
        ws[f"F{row}"].alignment = styles['align_left_wrap']
        ws[f"F{row}"].border = styles['thin_border']
        ws[f"F{row}"].fill = styles['fill_input']
        ws[f"F{row}"].protection = Protection(locked=False)

        # Col G: Owner (INPUT DESBLOQUEADO)
        ws[f"G{row}"] = cown
        ws[f"G{row}"].font = styles['font_bold']
        ws[f"G{row}"].alignment = styles['align_center']
        ws[f"G{row}"].border = styles['thin_border']
        ws[f"G{row}"].fill = styles['fill_input']
        ws[f"G{row}"].protection = Protection(locked=False)

        # Col H: Plazo (INPUT DESBLOQUEADO)
        ws[f"H{row}"] = ctime
        ws[f"H{row}"].font = styles['font_subhead']
        ws[f"H{row}"].alignment = styles['align_center']
        ws[f"H{row}"].border = styles['thin_border']
        ws[f"H{row}"].fill = styles['fill_input']
        ws[f"H{row}"].protection = Protection(locked=False)

        # Col I: Presupuesto Reasignado (INPUT DESBLOQUEADO)
        ws[f"I{row}"] = cbud
        ws[f"I{row}"].font = styles['font_bold']
        ws[f"I{row}"].alignment = styles['align_right']
        ws[f"I{row}"].border = styles['thin_border']
        ws[f"I{row}"].fill = styles['fill_input']
        ws[f"I{row}"].number_format = styles['num_fmt_curr']
        ws[f"I{row}"].protection = Protection(locked=False)

        # Col J: EBITDA Proyectado (INPUT DESBLOQUEADO)
        ws[f"J{row}"] = ceb
        ws[f"J{row}"].font = styles['font_bold']
        ws[f"J{row}"].alignment = styles['align_right']
        ws[f"J{row}"].border = styles['thin_border']
        ws[f"J{row}"].fill = styles['fill_input']
        ws[f"J{row}"].number_format = styles['num_fmt_curr']
        ws[f"J{row}"].protection = Protection(locked=False)

        # Col K: KPI de Impacto (INPUT DESBLOQUEADO)
        ws[f"K{row}"] = ckpi
        ws[f"K{row}"].font = styles['font_regular']
        ws[f"K{row}"].alignment = styles['align_left_wrap']
        ws[f"K{row}"].border = styles['thin_border']
        ws[f"K{row}"].fill = styles['fill_input']
        ws[f"K{row}"].protection = Protection(locked=False)

        # Col L: Estado (INPUT DESBLOQUEADO)
        ws[f"L{row}"] = cstat
        ws[f"L{row}"].font = styles['font_subhead']
        ws[f"L{row}"].alignment = styles['align_center']
        ws[f"L{row}"].border = styles['thin_border']
        ws[f"L{row}"].fill = styles['fill_input']
        ws[f"L{row}"].protection = Protection(locked=False)

    # Fila 20: TOTAL PROGRAMA
    ws['B20'] = "TOTAL"
    ws['B20'].font = styles['font_bold']
    ws['B20'].alignment = styles['align_center']
    ws['B20'].border = styles['total_border']

    ws['C20'] = "PROGRAMA DE ASIGNACIÓN" if lang == 'ES' else "CAPITAL ALLOCATION PROGRAM"
    ws['C20'].font = styles['font_bold']
    ws['C20'].alignment = styles['align_left']
    ws['C20'].border = styles['total_border']

    for col in ['D', 'E', 'F', 'G', 'H']:
        ws[f"{col}20"] = ""
        ws[f"{col}20"].border = styles['total_border']

    ws['I20'] = "=SUM(I12:I19)"
    ws['I20'].font = styles['font_bold']
    ws['I20'].alignment = styles['align_right']
    ws['I20'].border = styles['total_border']
    ws['I20'].number_format = styles['num_fmt_curr']

    ws['J20'] = "=SUM(J12:J19)"
    ws['J20'].font = styles['font_bold']
    ws['J20'].alignment = styles['align_right']
    ws['J20'].border = styles['total_border']
    ws['J20'].number_format = styles['num_fmt_curr']

    ws['K20'] = ("Retorno Proyectado en ROIC Corporativo: +320 bps" if lang == 'ES' else "Projected Corporate ROIC Return: +320 bps")
    ws['K20'].font = styles['font_bold']
    ws['K20'].alignment = styles['align_left']
    ws['K20'].border = styles['total_border']

    ws['L20'] = "100% C-Level"
    ws['L20'].font = styles['font_bold']
    ws['L20'].alignment = styles['align_center']
    ws['L20'].border = styles['total_border']

    # Anchos de columna
    col_widths = {
        'A': 4,
        'B': 12,
        'C': 34,
        'D': 18,
        'E': 24,
        'F': 46,
        'G': 16,
        'H': 18,
        'I': 22,
        'J': 22,
        'K': 38,
        'L': 20,
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    apply_sheet_protection(ws)


# ==============================================================================
# GENERACIÓN DE LIBROS DE TRABAJO DUAL (ES & EN)
# ==============================================================================
def generate_workbook(lang='ES', out_path='BCG_Dinamica_Datalaria_ES.xlsx'):
    wb = openpyxl.Workbook()
    # Pestaña 1
    ws1 = wb.active
    # Pestaña 2
    ws2 = wb.create_sheet()
    # Pestaña 3
    ws3 = wb.create_sheet()
    # Pestaña 4
    ws4 = wb.create_sheet()

    # Construir pestañas en orden
    # Nota: ws2 (Evaluación) y ws3 (Matriz) se pueblan antes de los gráficos de ws1
    build_tab2_evaluation(wb, ws2, lang=lang)
    build_tab3_matrix_funds(wb, ws3, lang=lang)
    build_tab1_dashboard(wb, ws1, lang=lang)
    build_tab4_capital_plan(wb, ws4, lang=lang)

    # Asegurar que el directorio de salida existe
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    wb.save(out_path)
    print(f"[OK] Modelo Excel generado exitosamente: {out_path}")


def main():
    dir_packages = "packages"
    dir_es = os.path.join(dir_packages, "[ES]_BCG_Dinamica")
    dir_en = os.path.join(dir_packages, "[EN]_Dynamic_BCG")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    file_es = os.path.join(dir_es, "BCG_Dinamica_Datalaria_ES.xlsx")
    file_en = os.path.join(dir_en, "Dynamic_BCG_Datalaria_EN.xlsx")

    generate_workbook(lang='ES', out_path=file_es)
    generate_workbook(lang='EN', out_path=file_en)


if __name__ == "__main__":
    main()
