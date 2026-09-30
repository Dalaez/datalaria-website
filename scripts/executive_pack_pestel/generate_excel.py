#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos de decisión estratégica en Excel oficiales de Datalaria:
1. PESTEL_Cuantitativo_Datalaria_ES.xlsx (Versión en Español)
2. Quantitative_PESTEL_Datalaria_EN.xlsx (Versión en Inglés)

Estructura de 4 pestañas:
- Pestaña 1: Dashboard Ejecutivo / Executive Dashboard
  (Índice de Riesgo Macro Compuesto R_comp, Nivel de Exposición Global, Gráfico Radar de las 6 Dimensiones,
   Matriz de Dispersión / Cuadrantes Severidad vs. Volatilidad, Semáforo de Resiliencia Empresarial)
- Pestaña 2: Evaluación 6 Dimensiones / 6 Dimensions Assessment
  (Evaluación exhaustiva de los 6 pilares: Político, Económico, Social, Tecnológico, Ecológico, Legal.
   Ponderación Σw=100%, doble calificación Severidad [1-5] y Volatilidad [1-5], Riesgo Compuesto)
- Pestaña 3: Matriz Severidad vs Volatilidad / Severity vs Volatility Matrix
  (Mapa cartesiano de Incertidumbre Estratégica categorizando factores en 4 cuadrantes:
   Q1 Riesgos Críticos Volátiles, Q2 Riesgos Estructurales Predecibles, Q3 Alertas Tempranas, Q4 Ruidos Menores)
- Pestaña 4: Plan de Resiliencia & Contingencia / Macro Resilience Action Plan
  (Iniciativas con Owner C-Level, plazos Q1-Q4, presupuesto CAPEX/OPEX y KPI de impacto en P&L/EBITDA)

Normas corporativas:
- Protección de hojas con contraseña "Datalaria2026".
- Celdas de entrada desbloqueadas (locked=False) y selectUnlockedCells=False.
- Fórmulas y títulos bloqueados (locked=True) y selectLockedCells=False.
- Formatos localizados: ES (coma decimal, €) y EN (punto decimal, $).
- Compatibilidad nativa al 100% con Microsoft Excel y Google Sheets.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.chart import RadarChart, Reference

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = "0F172A"      # Slate 900 / Headers principales y títulos
COLOR_NAVY_MED = "1E293B"       # Slate 800 / Subheaders
COLOR_BLUE_ACCENT = "2563EB"    # Blue 600 / Azul Datalaria
COLOR_TEAL_ACCENT = "0D9488"    # Teal 600 / Ecológico / Ambiental
COLOR_AMBER_ACCENT = "D97706"   # Amber 600 / Económico
COLOR_ROSE_ACCENT = "E11D48"    # Rose 600 / Político / Crítico
COLOR_PURPLE_ACCENT = "7C3AED"  # Purple 600 / Tecnológico
COLOR_INDIGO_ACCENT = "4F46E5"  # Indigo 600 / Legal / Regulatorio
COLOR_EMERALD_ACCENT = "059669" # Emerald 600 / Resiliencia / Social

# Fondos claros de tarjetas y contenedores
COLOR_BG_LIGHT = "F8FAFC"       # Slate 50
COLOR_BG_CARD = "F1F5F9"        # Slate 100
COLOR_WHITE = "FFFFFF"          # Fondo inputs desbloqueados

# Fondos temáticos por dimensión PESTEL
COLOR_POL_BG = "FFF1F2"         # Rose 50 (Político)
COLOR_POL_BORDER = "F43F5E"
COLOR_POL_TEXT = "9F1239"

COLOR_ECO_BG = "FFFBEB"         # Amber 50 (Económico)
COLOR_ECO_BORDER = "F59E0B"
COLOR_ECO_TEXT = "92400E"

COLOR_SOC_BG = "F0FDF4"         # Green 50 (Social)
COLOR_SOC_BORDER = "22C55E"
COLOR_SOC_TEXT = "166534"

COLOR_TEC_BG = "F5F3FF"         # Purple 50 (Tecnológico)
COLOR_TEC_BORDER = "8B5CF6"
COLOR_TEC_TEXT = "5B21B6"

COLOR_ENV_BG = "F0FDFA"         # Teal 50 (Ecológico)
COLOR_ENV_BORDER = "14B8A6"
COLOR_ENV_TEXT = "0F766E"

COLOR_LEG_BG = "EEF2FF"         # Indigo 50 (Legal)
COLOR_LEG_BORDER = "6366F1"
COLOR_LEG_TEXT = "3730A3"

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

    num_fmt_dec = "0,00" if lang == 'ES' else "0.00"
    num_fmt_pct = "0,0%" if lang == 'ES' else "0.0%"
    num_fmt_curr = "#,##0 €" if lang == 'ES' else "$#,##0"

    return {
        'title_font': Font(name='Segoe UI', size=14, bold=True, color=COLOR_WHITE),
        'title_fill': PatternFill(start_color=COLOR_NAVY_DARK, end_color=COLOR_NAVY_DARK, fill_type='solid'),
        'subtitle_font': Font(name='Segoe UI', size=9, italic=True, color="94A3B8"),
        'kicker_font': Font(name='Segoe UI', size=8, bold=True, color="38BDF8"),
        'section_font': Font(name='Segoe UI', size=11, bold=True, color=COLOR_NAVY_DARK),
        'section_fill': PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid'),
        'header_font': Font(name='Segoe UI', size=10, bold=True, color=COLOR_WHITE),
        'header_fill': PatternFill(start_color=COLOR_NAVY_MED, end_color=COLOR_NAVY_MED, fill_type='solid'),
        'cell_font': Font(name='Segoe UI', size=10, color="1E293B"),
        'cell_bold': Font(name='Segoe UI', size=10, bold=True, color="0F172A"),
        'code_font': Font(name='Consolas', size=10, bold=True, color=COLOR_BLUE_ACCENT),
        'input_fill': PatternFill(start_color=COLOR_WHITE, end_color=COLOR_WHITE, fill_type='solid'),
        'calc_fill': PatternFill(start_color=COLOR_BG_LIGHT, end_color=COLOR_BG_LIGHT, fill_type='solid'),
        'total_fill': PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid'),
        'thin_border': thin_border,
        'header_border': header_border,
        'total_border': total_border,
        'align_center': Alignment(horizontal='center', vertical='center'),
        'align_center_wrap': Alignment(horizontal='center', vertical='center', wrap_text=True),
        'align_left': Alignment(horizontal='left', vertical='center'),
        'align_left_wrap': Alignment(horizontal='left', vertical='center', wrap_text=True),
        'align_right': Alignment(horizontal='right', vertical='center'),
        'num_fmt_dec': num_fmt_dec,
        'num_fmt_pct': num_fmt_pct,
        'num_fmt_curr': num_fmt_curr,
    }


def style_merged_range(ws, cell_range, font=None, fill=None, border=None, alignment=None):
    """Aplica estilos consistentes a una celda combinada o rango de celdas."""
    for row in ws[cell_range]:
        for cell in row:
            if font: cell.font = font
            if fill: cell.fill = fill
            if border: cell.border = border
            if alignment: cell.alignment = alignment


def apply_sheet_protection(ws, allow_structure=True):
    """
    Aplica protección nativa con contraseña para blindar fórmulas y elementos visuales.
    En el estándar OpenXML (ECMA-376 / CT_SheetProtection):
      - sheet, objects, scenarios: True = blindado.
      - selectUnlockedCells = False (0 = sin restricción, permite seleccionar y editar desbloqueadas).
      - selectLockedCells = False (0 = sin restricción, permite seleccionar bloqueadas para lectura).
    """
    ws.protection.set_password(PASSWORD_PROTECT)
    ws.protection.sheet = True
    ws.protection.objects = True
    ws.protection.scenarios = True
    ws.protection.selectUnlockedCells = False
    ws.protection.selectLockedCells = False
    if allow_structure:
        ws.protection.insertRows = False
        ws.protection.deleteRows = False
        ws.protection.formatCells = False
        ws.protection.formatColumns = False
        ws.protection.formatRows = False
        ws.protection.sort = False
        ws.protection.autoFilter = False


# ==============================================================================
# PESTAÑA 1: DASHBOARD EJECUTIVO
# ==============================================================================
def build_tab1_dashboard(wb, lang='ES'):
    ws = wb.active
    tab_name = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    ws.title = tab_name
    ws.views.sheetView[0].showGridLines = True
    styles = get_base_styles(lang)

    t_eval = "Evaluación 6 Dimensiones" if lang == 'ES' else "6 Dimensions Assessment"
    t_mat = "Matriz Severidad vs Volatilidad" if lang == 'ES' else "Severity vs Volatility Matrix"
    t_plan = "Plan Resiliencia & Contingencia" if lang == 'ES' else "Macro Resilience Action Plan"

    # --- BANNER DE CABECERA ---
    ws.merge_cells('B1:M1')
    ws['B1'] = "DATALARIA STRATEGY PRACTICE • MCKINSEY & BCG STANDARD • EXECUTIVE DECISION PACK"
    ws['B1'].font = styles['kicker_font']
    ws['B1'].fill = styles['title_fill']
    ws['B1'].alignment = styles['align_center']

    ws.merge_cells('B2:M2')
    ws['B2'] = "DASHBOARD ESTRATÉGICO: MATRIZ PESTEL CUANTITATIVA (SEVERIDAD & VOLATILIDAD)" if lang == 'ES' else "EXECUTIVE DASHBOARD: QUANTITATIVE PESTEL MATRIX (SEVERITY & VOLATILITY)"
    ws['B2'].font = styles['title_font']
    ws['B2'].fill = styles['title_fill']
    ws['B2'].alignment = styles['align_center']

    ws.merge_cells('B3:M3')
    ws['B3'] = "Modelo cuantitativo bidimensional de incertidumbre macroambiental, perfil radar PESTEL y semáforo de resiliencia empresarial" if lang == 'ES' else "2D quantitative macroenvironmental uncertainty engine, PESTEL radar profile, and corporate resilience scorecard"
    ws['B3'].font = styles['subtitle_font']
    ws['B3'].fill = styles['title_fill']
    ws['B3'].alignment = styles['align_center']
    ws.row_dimensions[2].height = 28

    # --- 4 TARJETAS KPI EJECUTIVAS (B5:M8) ---
    cards_config = [
        ('B', 'D',
         "ÍNDICE RIESGO MACRO (R_comp)" if lang == 'ES' else "COMPOSITE MACRO RISK (R_comp)",
         "=G18",
         f'=IF(B6>=3.8,"Exposición Crítica / Shock",IF(B6>=2.8,"Riesgo Moderado / Alerta","Entorno Estable / Favorable"))' if lang == 'ES' else f'=IF(B6>=3.8,"Critical Exposure / Shock",IF(B6>=2.8,"Moderate Risk / Alert","Stable / Favorable"))',
         COLOR_NAVY_DARK, COLOR_POL_BG, COLOR_POL_BORDER),

        ('E', 'G',
         "RESILIENCIA ESTRUCTURAL" if lang == 'ES' else "STRUCTURAL RESILIENCE",
         "=5-B6",
         f'=IF(E6>=2.2,"Alta Capacidad de Absorción",IF(E6>=1.4,"Resiliencia Media","Alta Vulnerabilidad a Shocks"))' if lang == 'ES' else f'=IF(E6>=2.2,"High Shock Absorption",IF(E6>=1.4,"Moderate Resilience","Vulnerable to Macro Shocks"))',
         COLOR_NAVY_DARK, COLOR_ENV_BG, COLOR_ENV_BORDER),

        ('H', 'J',
         "DIMENSIÓN CRÍTICA DESESTABILIZADORA" if lang == 'ES' else "PEAK DESTABILIZING DIMENSION",
         f'=INDEX(C12:C17, MATCH(MAX(G12:G17), G12:G17, 0))',
         "Foco prioritario de asignación de capital" if lang == 'ES' else "Top capital allocation priority",
         COLOR_NAVY_DARK, COLOR_ECO_BG, COLOR_ECO_BORDER),

        ('K', 'M',
         "POSTURA MACROESTRATÉGICA" if lang == 'ES' else "MACRO STRATEGIC POSTURE",
         f'=IF(B6>=3.8,"BLINDAJE Y COBERTURA ACTIVA",IF(B6>=2.8,"MITIGACIÓN PREVENTIVA Y VIGILANCIA","EXPANSIÓN Y CAPTURA DE CUOTA"))' if lang == 'ES' else f'=IF(B6>=3.8,"ACTIVE SHIELDING & HEDGING",IF(B6>=2.8,"PREVENTIVE MITIGATION & MONITORING","EXPANSION & MARKET SHARE CAPTURE"))',
         f"='{t_mat}'!C4",
         COLOR_NAVY_DARK, COLOR_BG_LIGHT, COLOR_BORDER_MED)
    ]

    for c_start, c_end, title, f_val, f_sub, col_title, bg_card, border_card in cards_config:
        ws.merge_cells(f"{c_start}5:{c_end}5")
        ws[f"{c_start}5"] = title
        ws[f"{c_start}5"].font = Font(name='Segoe UI', size=9, bold=True, color="64748B")
        ws[f"{c_start}5"].alignment = styles['align_center']
        ws[f"{c_start}5"].fill = PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid')

        ws.merge_cells(f"{c_start}6:{c_end}6")
        ws[f"{c_start}6"] = f_val
        ws[f"{c_start}6"].font = Font(name='Segoe UI', size=15, bold=True, color=COLOR_NAVY_DARK)
        ws[f"{c_start}6"].alignment = styles['align_center']
        ws[f"{c_start}6"].fill = PatternFill(start_color=bg_card, end_color=bg_card, fill_type='solid')
        if f_val in ["=G18", "=5-B6"]:
            ws[f"{c_start}6"].number_format = styles['num_fmt_dec']

        ws.merge_cells(f"{c_start}7:{c_end}7")
        ws[f"{c_start}7"] = f_sub
        ws[f"{c_start}7"].font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"{c_start}7"].alignment = styles['align_center']
        ws[f"{c_start}7"].fill = PatternFill(start_color=bg_card, end_color=bg_card, fill_type='solid')

        for row in range(5, 8):
            for col_idx in range(openpyxl.utils.column_index_from_string(c_start), openpyxl.utils.column_index_from_string(c_end) + 1):
                col_letter = get_column_letter(col_idx)
                top_s = 'thin' if row == 5 else None
                bot_s = 'thin' if row == 7 else None
                left_s = 'thin' if col_letter == c_start else None
                right_s = 'thin' if col_letter == c_end else None
                ws[f"{col_letter}{row}"].border = Border(
                    top=Side(style=top_s, color=border_card) if top_s else Side(style='thin', color=COLOR_BG_CARD),
                    bottom=Side(style=bot_s, color=border_card) if bot_s else Side(style='thin', color=COLOR_BG_CARD),
                    left=Side(style=left_s, color=border_card) if left_s else None,
                    right=Side(style=right_s, color=border_card) if right_s else None
                )

    # --- TABLA RESUMEN DE LAS 6 DIMENSIONES PESTEL (B10:G18) ---
    ws.merge_cells('B10:G10')
    ws['B10'] = "RESUMEN CUANTITATIVO DE LAS 6 DIMENSIONES PESTEL" if lang == 'ES' else "QUANTITATIVE 6 PESTEL DIMENSIONS SUMMARY"
    ws['B10'].font = styles['section_font']
    ws['B10'].fill = styles['section_fill']
    ws['B10'].alignment = styles['align_left']

    headers_p = [
        ("ID", 'B', 8),
        ("Dimensión PESTEL" if lang == 'ES' else "PESTEL Dimension", 'C', 26),
        ("Peso (Wd)" if lang == 'ES' else "Weight (Wd)", 'D', 14),
        ("Severidad (S)" if lang == 'ES' else "Severity (S)", 'E', 15),
        ("Volatilidad (V)" if lang == 'ES' else "Volatility (V)", 'F', 15),
        ("Riesgo (Rd)" if lang == 'ES' else "Risk (Rd)", 'G', 16),
    ]

    for h_txt, col, w in headers_p:
        ws[f"{col}11"] = h_txt
        ws[f"{col}11"].font = styles['header_font']
        ws[f"{col}11"].fill = styles['header_fill']
        ws[f"{col}11"].alignment = styles['align_center'] if col in ['B', 'D', 'E', 'F', 'G'] else styles['align_left']
        ws[f"{col}11"].border = styles['header_border']

    dims_data = [
        ("D1", "1. Político" if lang == 'ES' else "1. Political", f"='{t_eval}'!D5", f"='{t_eval}'!E11", f"='{t_eval}'!F11", f"='{t_eval}'!G11"),
        ("D2", "2. Económico" if lang == 'ES' else "2. Economic", f"='{t_eval}'!D14", f"='{t_eval}'!E20", f"='{t_eval}'!F20", f"='{t_eval}'!G20"),
        ("D3", "3. Social" if lang == 'ES' else "3. Social", f"='{t_eval}'!D23", f"='{t_eval}'!E29", f"='{t_eval}'!F29", f"='{t_eval}'!G29"),
        ("D4", "4. Tecnológico" if lang == 'ES' else "4. Technological", f"='{t_eval}'!D32", f"='{t_eval}'!E38", f"='{t_eval}'!F38", f"='{t_eval}'!G38"),
        ("D5", "5. Ecológico" if lang == 'ES' else "5. Environmental", f"='{t_eval}'!D41", f"='{t_eval}'!E47", f"='{t_eval}'!F47", f"='{t_eval}'!G47"),
        ("D6", "6. Legal" if lang == 'ES' else "6. Legal & Reg.", f"='{t_eval}'!D50", f"='{t_eval}'!E56", f"='{t_eval}'!F56", f"='{t_eval}'!G56"),
    ]

    for idx, (d_id, d_name, d_w, d_s, d_v, d_r) in enumerate(dims_data, start=12):
        ws[f"B{idx}"] = d_id
        ws[f"B{idx}"].font = styles['code_font']
        ws[f"B{idx}"].alignment = styles['align_center']
        ws[f"B{idx}"].fill = styles['calc_fill']
        ws[f"B{idx}"].border = styles['thin_border']

        ws[f"C{idx}"] = d_name
        ws[f"C{idx}"].font = styles['cell_bold']
        ws[f"C{idx}"].alignment = styles['align_left']
        ws[f"C{idx}"].fill = styles['calc_fill']
        ws[f"C{idx}"].border = styles['thin_border']

        ws[f"D{idx}"] = d_w
        ws[f"D{idx}"].font = styles['cell_font']
        ws[f"D{idx}"].alignment = styles['align_center']
        ws[f"D{idx}"].fill = styles['calc_fill']
        ws[f"D{idx}"].border = styles['thin_border']
        ws[f"D{idx}"].number_format = styles['num_fmt_pct']

        ws[f"E{idx}"] = d_s
        ws[f"E{idx}"].font = styles['cell_font']
        ws[f"E{idx}"].alignment = styles['align_center']
        ws[f"E{idx}"].fill = styles['calc_fill']
        ws[f"E{idx}"].border = styles['thin_border']
        ws[f"E{idx}"].number_format = styles['num_fmt_dec']

        ws[f"F{idx}"] = d_v
        ws[f"F{idx}"].font = styles['cell_font']
        ws[f"F{idx}"].alignment = styles['align_center']
        ws[f"F{idx}"].fill = styles['calc_fill']
        ws[f"F{idx}"].border = styles['thin_border']
        ws[f"F{idx}"].number_format = styles['num_fmt_dec']

        ws[f"G{idx}"] = d_r
        ws[f"G{idx}"].font = styles['cell_bold']
        ws[f"G{idx}"].alignment = styles['align_center']
        ws[f"G{idx}"].fill = styles['calc_fill']
        ws[f"G{idx}"].border = styles['thin_border']
        ws[f"G{idx}"].number_format = styles['num_fmt_dec']

    # Fila Total
    ws['B18'] = "TOTAL"
    ws['B18'].font = styles['cell_bold']
    ws['B18'].alignment = styles['align_center']
    ws['B18'].fill = styles['total_fill']
    ws['B18'].border = styles['total_border']

    ws['C18'] = "Índice Consolidado R_comp" if lang == 'ES' else "Consolidated Index R_comp"
    ws['C18'].font = styles['cell_bold']
    ws['C18'].alignment = styles['align_left']
    ws['C18'].fill = styles['total_fill']
    ws['C18'].border = styles['total_border']

    ws['D18'] = "=SUM(D12:D17)"
    ws['D18'].font = styles['cell_bold']
    ws['D18'].alignment = styles['align_center']
    ws['D18'].fill = styles['total_fill']
    ws['D18'].border = styles['total_border']
    ws['D18'].number_format = styles['num_fmt_pct']

    ws['E18'] = "=SUMPRODUCT(D12:D17,E12:E17)"
    ws['E18'].font = styles['cell_font']
    ws['E18'].alignment = styles['align_center']
    ws['E18'].fill = styles['total_fill']
    ws['E18'].border = styles['total_border']
    ws['E18'].number_format = styles['num_fmt_dec']

    ws['F18'] = "=SUMPRODUCT(D12:D17,F12:F17)"
    ws['F18'].font = styles['cell_font']
    ws['F18'].alignment = styles['align_center']
    ws['F18'].fill = styles['total_fill']
    ws['F18'].border = styles['total_border']
    ws['F18'].number_format = styles['num_fmt_dec']

    ws['G18'] = "=SUMPRODUCT(D12:D17,G12:G17)"
    ws['G18'].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws['G18'].alignment = styles['align_center']
    ws['G18'].fill = styles['total_fill']
    ws['G18'].border = styles['total_border']
    ws['G18'].number_format = styles['num_fmt_dec']

    # --- GRÁFICO RADAR DINÁMICO EN H10:M25 ---
    radar = RadarChart()
    radar.type = "standard"
    labels_ref = Reference(ws, min_col=3, min_row=12, max_row=17)
    data_ref = Reference(ws, min_col=7, min_row=11, max_row=17)
    radar.add_data(data_ref, titles_from_data=True)
    radar.set_categories(labels_ref)
    radar.title = "Radar de las 6 Dimensiones PESTEL" if lang == 'ES' else "PESTEL 6 Dimensions Radar Chart"
    radar.style = 26
    radar.width = 17.5
    radar.height = 11.0
    ws.add_chart(radar, "H10")

    # --- TABLA DE ORIENTACIÓN ESTRATÉGICA & P&L (B20:G28) ---
    ws.merge_cells('B20:G20')
    ws['B20'] = "DIAGNÓSTICO ESTRATÉGICO Y RECOMENDACIÓN DE ASIGNACIÓN DE CAPITAL" if lang == 'ES' else "STRATEGIC DIAGNOSIS & CAPITAL ALLOCATION GUIDANCE"
    ws['B20'].font = styles['section_font']
    ws['B20'].fill = styles['section_fill']
    ws['B20'].alignment = styles['align_left']

    diag_headers = [
        ("Dimensión de Decisión" if lang == 'ES' else "Decision Dimension", 'B', 'C'),
        ("Valor / Diagnóstico" if lang == 'ES' else "Value / Diagnosis", 'D', 'E'),
        ("Implicación en Comité / Plan de Acción" if lang == 'ES' else "Board Implication / Action Plan", 'F', 'G'),
    ]

    for h_txt, col_s, col_e in diag_headers:
        ws.merge_cells(f"{col_s}21:{col_e}21")
        ws[f"{col_s}21"] = h_txt
        ws[f"{col_s}21"].font = styles['header_font']
        ws[f"{col_s}21"].fill = styles['header_fill']
        ws[f"{col_s}21"].alignment = styles['align_left'] if col_s == 'B' else styles['align_center']
        style_merged_range(ws, f"{col_s}21:{col_e}21", border=styles['header_border'])

    diag_rows = [
        ("Nivel de Exposición Global al Riesgo Macro",
         "=B6",
         f'=IF(B6>=3.8,"Requiere comité de crisis quincenal y dotación de fondo de contingencia.",IF(B6>=2.8,"Exposición moderada: activar coberturas financieras y monitorización mensual.","Entorno predecible: canalizar caja a expansión comercial y M&A."))' if lang == 'ES' else f'=IF(B6>=3.8,"Requires biweekly crisis committee and contingency reserve funding.",IF(B6>=2.8,"Moderate exposure: activate hedging and monthly monitoring.","Stable environment: allocate cash flow to market share expansion."))'),

        ("Dimensión Crítica de Mayor Severidad",
         f'=INDEX(C12:C17, MATCH(MAX(E12:E17), E12:E17, 0))',
         "Prioridad absoluta en el plan de resiliencia y asignación de presupuesto" if lang == 'ES' else "Top capital allocation priority in resilience plan and CAPEX"),

        ("Dimensión de Mayor Volatilidad e Impredecibilidad",
         f'=INDEX(C12:C17, MATCH(MAX(F12:F17), F12:F17, 0))',
         "Establecer triggers de alerta temprana y contratos flexibles con proveedores" if lang == 'ES' else "Establish early warning triggers and agile supplier contracts"),

        ("Brecha de Resiliencia Empresarial (5.0 - R_comp)",
         "=E6",
         f'=IF(E6>=2.2,"Margen operativo suficientemente blindado frente a shocks.",IF(E6>=1.4,"Margen vulnerable a compresión en caso de confluencia de riesgos.","Margen en riesgo severo: inacción destruye EBITDA proyectado."))' if lang == 'ES' else f'=IF(E6>=2.2,"Operating margins adequately shielded against external shocks.",IF(E6>=1.4,"Margins vulnerable to compression if multiple risks collide.","Margins under severe threat: inaction directly erodes EBITDA."))'),

        ("Presupuesto de Contingencia Aprobado (Plan)",
         f"='{t_plan}'!I19",
         f"='{t_plan}'!D24")
    ]

    curr_row = 22
    for d_title, d_val, d_imp in diag_rows:
        ws.merge_cells(f"B{curr_row}:C{curr_row}")
        ws[f"B{curr_row}"] = d_title
        ws[f"B{curr_row}"].font = styles['cell_bold']
        ws[f"B{curr_row}"].alignment = styles['align_left_wrap']
        ws[f"B{curr_row}"].fill = styles['calc_fill']
        style_merged_range(ws, f"B{curr_row}:C{curr_row}", border=styles['thin_border'])

        ws.merge_cells(f"D{curr_row}:E{curr_row}")
        ws[f"D{curr_row}"] = d_val
        ws[f"D{curr_row}"].font = styles['cell_bold']
        ws[f"D{curr_row}"].alignment = styles['align_center']
        ws[f"D{curr_row}"].fill = styles['calc_fill']
        if d_val in ["=B6", "=E6"]:
            ws[f"D{curr_row}"].number_format = styles['num_fmt_dec']
        elif "Plan" in d_title or "Budget" in d_title:
            ws[f"D{curr_row}"].number_format = styles['num_fmt_curr']
        style_merged_range(ws, f"D{curr_row}:E{curr_row}", border=styles['thin_border'])

        ws.merge_cells(f"F{curr_row}:G{curr_row}")
        ws[f"F{curr_row}"] = d_imp
        ws[f"F{curr_row}"].font = styles['cell_font']
        ws[f"F{curr_row}"].alignment = styles['align_left_wrap']
        ws[f"F{curr_row}"].fill = styles['calc_fill']
        style_merged_range(ws, f"F{curr_row}:G{curr_row}", border=styles['thin_border'])

        curr_row += 1

    # Ajuste de anchos de columna en Tab 1
    col_widths = {'A': 4, 'B': 10, 'C': 30, 'D': 16, 'E': 16, 'F': 16, 'G': 18, 'H': 18, 'I': 18, 'J': 18, 'K': 18, 'L': 18, 'M': 18}
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    apply_sheet_protection(ws)


# ==============================================================================
# PESTAÑA 2: EVALUACIÓN 6 DIMENSIONES
# ==============================================================================
def build_tab2_evaluation(wb, lang='ES'):
    ws = wb.create_sheet(title="Evaluación 6 Dimensiones" if lang == 'ES' else "6 Dimensions Assessment")
    ws.views.sheetView[0].showGridLines = True
    styles = get_base_styles(lang)

    # Encabezado principal
    ws.merge_cells('B1:I1')
    ws['B1'] = "DATALARIA • EVALUACIÓN CUANTITATIVA PESTEL: MATRIZ DE SEVERIDAD & VOLATILIDAD" if lang == 'ES' else "DATALARIA • QUANTITATIVE PESTEL ASSESSMENT: SEVERITY & VOLATILITY MATRIX"
    ws['B1'].font = styles['kicker_font']
    ws['B1'].fill = styles['title_fill']
    ws['B1'].alignment = styles['align_center']

    ws.merge_cells('B2:I2')
    ws['B2'] = "EVALUACIÓN DETALLADA DE LAS 6 DIMENSIONES MACROAMBIENTALES (P, E, S, T, E, L)" if lang == 'ES' else "DETAILED ASSESSMENT OF THE 6 MACROENVIRONMENTAL DIMENSIONS (P, E, S, T, E, L)"
    ws['B2'].font = styles['title_font']
    ws['B2'].fill = styles['title_fill']
    ws['B2'].alignment = styles['align_center']

    ws.merge_cells('B3:I3')
    ws['B3'] = "Celdas de fondo blanco = Inputs editables (Pesos, Severidad 1-5, Volatilidad 1-5 y Justificación). Fórmulas y títulos protegidos." if lang == 'ES' else "White cells = Editable inputs (Weights, Severity 1-5, Volatility 1-5, and Rationale). Formulas and headers protected."
    ws['B3'].font = styles['subtitle_font']
    ws['B3'].fill = styles['title_fill']
    ws['B3'].alignment = styles['align_center']
    ws.row_dimensions[2].height = 26

    # Estructura de factores canónicos por dimensión
    dimensions_spec = [
        {
            "id": "POL",
            "name_es": "1. Dimensión Política (Political)",
            "name_en": "1. Political Dimension",
            "weight": 0.15,
            "bg": COLOR_POL_BG,
            "border": COLOR_POL_BORDER,
            "text": COLOR_POL_TEXT,
            "factors": [
                ("POL-01",
                 "Tensiones geopolíticas, aranceles y fragmentación comercial global" if lang == 'ES' else "Geopolitical tensions, trade tariffs & global supply chain fragmentation",
                 0.30, 4.2, 4.0,
                 "Riesgo de aranceles cruzados entre bloques (EE.UU., UE, China) que impactan en márgenes brutos" if lang == 'ES' else "Cross-border tariff risks (US, EU, China) impacting import/export gross margins"),
                ("POL-02",
                 "Estabilidad gubernamental y certidumbre en políticas económicas" if lang == 'ES' else "Government stability & economic policy predictability",
                 0.25, 3.5, 3.0,
                 "Ciclos electorales y polarización que pueden alterar marcos de incentivos y contratación pública" if lang == 'ES' else "Electoral cycles and legislative polarization shifting public procurement guidelines"),
                ("POL-03",
                 "Política fiscal corporativa y reformas tributarias imprevistas" if lang == 'ES' else "Corporate tax policy & unexpected fiscal regime reforms",
                 0.25, 3.8, 2.5,
                 "Implementación del tipo mínimo global del 15% (Pilar 2 OCDE) y tasas sectoriales extraordinarias" if lang == 'ES' else "OECD Pillar 2 minimum corporate tax implementation and windfall sector surcharges"),
                ("POL-04",
                 "Subvenciones industriales y ayudas públicas (NextGen EU, IRA EE.UU.)" if lang == 'ES' else "Industrial subsidies & state aid programs (NextGen EU, US IRA)",
                 0.20, 3.0, 3.5,
                 "Disparidad competitiva generada por subsidios asimétricos a competidores extranjeros" if lang == 'ES' else "Competitive asymmetry generated by localized clean tech & manufacturing subsidies")
            ]
        },
        {
            "id": "ECO",
            "name_es": "2. Dimensión Económica (Economic)",
            "name_en": "2. Economic Dimension",
            "weight": 0.25,
            "bg": COLOR_ECO_BG,
            "border": COLOR_ECO_BORDER,
            "text": COLOR_ECO_TEXT,
            "factors": [
                ("ECO-01",
                 "Volatilidad de costes energéticos y precios de materias primas críticas" if lang == 'ES' else "Energy cost volatility & critical commodity price spikes",
                 0.30, 4.5, 4.5,
                 "Oscilaciones imprevistas en gas, electricidad y minerales que comprimen el margen de explotación" if lang == 'ES' else "Unhedged swings in natural gas, power, and industrial metals compressing margins"),
                ("ECO-02",
                 "Tipos de interés, coste del capital (WACC) y restricción crediticia" if lang == 'ES' else "Interest rates, cost of capital (WACC) & debt refinancing spreads",
                 0.25, 4.0, 3.0,
                 "Presión de tipos elevados que encarece el refinanciamiento de deuda y frena el CAPEX expansivo" if lang == 'ES' else "Elevated terminal rates raising debt service burdens and postponing capital expenditures"),
                ("ECO-03",
                 "Inflación salarial subyacente y costes laborales directos" if lang == 'ES' else "Core wage inflation & upward pressure on unit labor costs",
                 0.25, 3.8, 3.2,
                 "Convenios colectivos con indexación y presión de talento especializado que elevan el OPEX fijo" if lang == 'ES' else "Index-linked collective bargaining and specialized talent premiums raising fixed OPEX"),
                ("ECO-04",
                 "Fluctuación de divisas clave (EUR/USD, GBP/EUR, Yuan)" if lang == 'ES' else "Foreign exchange volatility on key trading pairs (EUR/USD, GBP, CNY)",
                 0.20, 3.2, 4.0,
                 "Exposición neta en compras y ventas internacionales sin cobertura financiera sistemática" if lang == 'ES' else "Unhedged cross-currency transactional exposure impacting overseas revenues")
            ]
        },
        {
            "id": "SOC",
            "name_es": "3. Dimensión Social (Sociocultural)",
            "name_en": "3. Sociocultural Dimension",
            "weight": 0.15,
            "bg": COLOR_SOC_BG,
            "border": COLOR_SOC_BORDER,
            "text": COLOR_SOC_TEXT,
            "factors": [
                ("SOC-01",
                 "Envejecimiento demográfico y escasez estructural de talento técnico" if lang == 'ES' else "Demographic aging & structural shortage of technical talent",
                 0.30, 4.2, 2.0,
                 "Inversión de la pirámide poblacional en Europa: déficit de ingenieros y operarios cualificados" if lang == 'ES' else "European demographic cliff resulting in acute shortages of STEM specialists and technicians"),
                ("SOC-02",
                 "Evolución de expectativas de consumidores hacia sostenibilidad y transparencia" if lang == 'ES' else "Consumer preference shift toward verified ESG sustainability & ethics",
                 0.25, 3.5, 2.8,
                 "Castigo reputacional y caída de cuota de mercado en marcas percibidas como poco éticas o contaminantes" if lang == 'ES' else "Reputational boycotts and market share erosion for brands lagging in circularity"),
                ("SOC-03",
                 "Transformación de modelos laborales: trabajo híbrido y expectativas de flexibilidad" if lang == 'ES' else "Workplace transformation: hybrid work models & employee retention",
                 0.25, 3.0, 3.0,
                 "Aumento del turnover voluntario si no se adaptan las políticas de flexibilidad y conciliación" if lang == 'ES' else "Increased turnover friction if remote work flexibility and cultural agility lag competitors"),
                ("SOC-04",
                 "Polarización sociocultural y activismo corporativo en redes" if lang == 'ES' else "Sociocultural polarization & corporate brand activism risks",
                 0.20, 2.5, 3.8,
                 "Riesgo de crisis viral de imagen corporativa ante posicionamientos públicos involuntarios" if lang == 'ES' else "Viral social media flashpoints requiring active PR monitoring and crisis playbooks")
            ]
        },
        {
            "id": "TEC",
            "name_es": "4. Dimensión Tecnológica (Technological)",
            "name_en": "4. Technological Dimension",
            "weight": 0.20,
            "bg": COLOR_TEC_BG,
            "border": COLOR_TEC_BORDER,
            "text": COLOR_TEC_TEXT,
            "factors": [
                ("TEC-01",
                 "Disrupción por Inteligencia Artificial Generativa y Automatización de Procesos" if lang == 'ES' else "Generative AI disruption & agentic process automation",
                 0.35, 4.6, 4.8,
                 "Obsolescencia de procesos tradicionales frente a competidores con modelos de lenguaje integrados" if lang == 'ES' else "Legacy workflows facing obsolescence against AI-native entrants delivering 40% lower unit costs"),
                ("TEC-02",
                 "Ciberamenazas, ransomware e interrupción de infraestructuras críticas" if lang == 'ES' else "Cyberattacks, enterprise ransomware & critical infrastructure disruptions",
                 0.25, 4.5, 4.2,
                 "Ataques avanzados a cadenas de suministro y sistemas OT industriales con riesgo de paradas" if lang == 'ES' else "Advanced persistent threats and ransomware targeting industrial OT and ERP cloud pipelines"),
                ("TEC-03",
                 "Velocidad de obsolescencia de arquitecturas tecnológicas heredadas (Legacy IT)" if lang == 'ES' else "Legacy IT debt & architectural migration barriers",
                 0.20, 3.8, 2.2,
                 "Deuda técnica interna que impide la adopción ágil de nuevas soluciones cloud y microservicios" if lang == 'ES' else "Technical debt preventing rapid integration of cloud-native APIs and SaaS workflows"),
                ("TEC-04",
                 "Innovación abierta y competencia en registro de patentes clave" if lang == 'ES' else "Open innovation velocity & proprietary patent race",
                 0.20, 3.2, 3.5,
                 "Riesgo de pérdida de liderazgo tecnológico frente a startups respaldadas por Venture Capital" if lang == 'ES' else "Disruptive VC-backed challengers filing foundational patents in adjacent technologies")
            ]
        },
        {
            "id": "ENV",
            "name_es": "5. Dimensión Ecológica / Ambiental (Environmental)",
            "name_en": "5. Environmental Dimension",
            "weight": 0.10,
            "bg": COLOR_ENV_BG,
            "border": COLOR_ENV_BORDER,
            "text": COLOR_ENV_TEXT,
            "factors": [
                ("ENV-01",
                 "Directiva de Información sobre Sostenibilidad (CSRD) y Huella de Carbono (Alcance 1, 2 y 3)" if lang == 'ES' else "EU CSRD reporting obligations & carbon footprint accounting (Scope 1, 2, 3)",
                 0.35, 4.0, 2.5,
                 "Obligación legal de auditoría exhaustiva con multas severas y pérdida de acceso a crédito bancario" if lang == 'ES' else "Mandatory audited sustainability disclosures with access to debt contingent on ESG ratings"),
                ("ENV-02",
                 "Riesgos físicos derivados del cambio climático (sequías, inundaciones, olas de calor)" if lang == 'ES' else "Physical climate risks & extreme weather facility disruptions",
                 0.25, 3.8, 3.8,
                 "Paradas no programadas en plantas productivas y encarecimiento de primas de seguros industriales" if lang == 'ES' else "Operational halts at manufacturing plants and sharp increases in commercial property insurance"),
                ("ENV-03",
                 "Regulaciones de economía circular, envases y fin de vida de producto" if lang == 'ES' else "Circular economy regulations, packaging taxes & extended producer responsibility",
                 0.20, 3.2, 2.8,
                 "Impuestos al plástico no reciclado y requerimientos estrictos de ecodiseño y trazabilidad" if lang == 'ES' else "Non-recycled plastic penalties and mandatory eco-design lifecycle standards"),
                ("ENV-04",
                 "Transición energética y estabilidad de la red de suministro eléctrico" if lang == 'ES' else "Energy transition volatility & power grid reliability",
                 0.20, 3.5, 3.5,
                 "Sobrecarga de redes locales y dependencia de fuentes renovables intermitentes sin almacenamiento" if lang == 'ES' else "Grid congestion and exposure to intermittent renewable supplies lacking battery storage")
            ]
        },
        {
            "id": "LEG",
            "name_es": "6. Dimensión Legal / Regulatoria (Legal)",
            "name_en": "6. Legal & Regulatory Dimension",
            "weight": 0.15,
            "bg": COLOR_LEG_BG,
            "border": COLOR_LEG_BORDER,
            "text": COLOR_LEG_TEXT,
            "factors": [
                ("LEG-01",
                 "Reglamento Europeo de Inteligencia Artificial (EU AI Act) y Compliance Algorítmico" if lang == 'ES' else "European AI Act compliance & algorithmic liability mandates",
                 0.35, 4.5, 4.2,
                 "Sanciones de hasta 35M€ o el 7% de la facturación global por despliegue de modelos de alto riesgo no certificados" if lang == 'ES' else "Fines up to 35M€ or 7% global turnover for uncertified high-risk AI deployments"),
                ("LEG-02",
                 "Privacidad de datos, RGPD / GDPR y soberanía europea del dato" if lang == 'ES' else "GDPR data privacy enforcement & European cross-border data transfers",
                 0.25, 4.0, 3.0,
                 "Litigios crecientes sobre transferencias transfronterizas y multas de autoridades de control" if lang == 'ES' else "Scrutiny on transatlantic data transfers and cloud telemetry governance"),
                ("LEG-03",
                 "Legislación laboral, contratación y normativas de desconexión digital" if lang == 'ES' else "Labor regulations, contractor classifications & right-to-disconnect laws",
                 0.20, 3.2, 2.5,
                 "Inspecciones de trabajo sobre falsos autónomos y costes de adaptación a estatutos de teletrabajo" if lang == 'ES' else "Audits on independent contractors and statutory compliance with remote worker laws"),
                ("LEG-04",
                 "Compliance en comercio exterior, sanciones internacionales y control de exportaciones" if lang == 'ES' else "Trade sanctions compliance, export controls & anti-bribery governance",
                 0.20, 4.2, 3.8,
                 "Complejidad de listas de sanciones (Rusia, Irán) con responsabilidad penal para administradores" if lang == 'ES' else "Strict liability penalties and export blacklists with direct director liability")
            ]
        }
    ]

    current_row = 5
    col_headers = [
        ("ID", 'B', 10),
        ("Factor Macroambiental Objetivo" if lang == 'ES' else "Objective Macroenvironmental Factor", 'C', 46),
        ("Peso (wi)" if lang == 'ES' else "Weight (wi)", 'D', 14),
        ("Severidad (1-5)" if lang == 'ES' else "Severity (1-5)", 'E', 15),
        ("Volatilidad (1-5)" if lang == 'ES' else "Volatility (1-5)", 'F', 16),
        ("Riesgo (Ri)" if lang == 'ES' else "Risk (Ri)", 'G', 15),
        ("Cuadrante" if lang == 'ES' else "Quadrant", 'H', 20),
        ("Justificación Estratégica & Métrica Clave" if lang == 'ES' else "Strategic Rationale & Empirical Indicator", 'I', 52)
    ]

    for dim in dimensions_spec:
        dim_title = dim["name_es"] if lang == 'ES' else dim["name_en"]
        header_fill = PatternFill(start_color=COLOR_NAVY_DARK, end_color=COLOR_NAVY_DARK, fill_type='solid')

        # Cabecera de Dimensión
        ws.merge_cells(f"B{current_row}:C{current_row}")
        ws[f"B{current_row}"] = dim_title
        ws[f"B{current_row}"].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_WHITE)
        ws[f"B{current_row}"].fill = header_fill
        ws[f"B{current_row}"].alignment = styles['align_left']
        style_merged_range(ws, f"B{current_row}:C{current_row}", border=styles['header_border'])

        ws[f"D{current_row}"] = dim["weight"]
        ws[f"D{current_row}"].font = Font(name='Segoe UI', size=11, bold=True, color="38BDF8")
        ws[f"D{current_row}"].fill = header_fill
        ws[f"D{current_row}"].alignment = styles['align_center']
        ws[f"D{current_row}"].border = styles['header_border']
        ws[f"D{current_row}"].number_format = styles['num_fmt_pct']
        ws[f"D{current_row}"].protection = Protection(locked=False)  # Peso editable por el usuario

        ws.merge_cells(f"E{current_row}:I{current_row}")
        weight_note = "Peso Macro sectorial (editable). Suma total de dimensiones = 100%" if lang == 'ES' else "Macro sector weight (editable). Total dimensions sum = 100%"
        ws[f"E{current_row}"] = weight_note
        ws[f"E{current_row}"].font = Font(name='Segoe UI', size=9, italic=True, color="94A3B8")
        ws[f"E{current_row}"].fill = header_fill
        ws[f"E{current_row}"].alignment = styles['align_left']
        style_merged_range(ws, f"E{current_row}:I{current_row}", border=styles['header_border'])

        current_row += 1

        # Cabecera de columnas de la tabla
        for h_txt, col, w in col_headers:
            ws[f"{col}{current_row}"] = h_txt
            ws[f"{col}{current_row}"].font = styles['header_font']
            ws[f"{col}{current_row}"].fill = styles['header_fill']
            ws[f"{col}{current_row}"].alignment = styles['align_center'] if col in ['B', 'D', 'E', 'F', 'G', 'H'] else styles['align_left']
            ws[f"{col}{current_row}"].border = styles['header_border']

        current_row += 1
        start_factor_row = current_row

        # Factores de la dimensión
        for f_id, f_desc, f_w, f_s, f_v, f_just in dim["factors"]:
            # ID
            ws[f"B{current_row}"] = f_id
            ws[f"B{current_row}"].font = styles['code_font']
            ws[f"B{current_row}"].alignment = styles['align_center']
            ws[f"B{current_row}"].fill = styles['calc_fill']
            ws[f"B{current_row}"].border = styles['thin_border']

            # Descripción Factor (editable)
            ws[f"C{current_row}"] = f_desc
            ws[f"C{current_row}"].font = styles['cell_font']
            ws[f"C{current_row}"].alignment = styles['align_left_wrap']
            ws[f"C{current_row}"].fill = styles['input_fill']
            ws[f"C{current_row}"].border = styles['thin_border']
            ws[f"C{current_row}"].protection = Protection(locked=False)

            # Peso relativo wi (editable)
            ws[f"D{current_row}"] = f_w
            ws[f"D{current_row}"].font = styles['cell_bold']
            ws[f"D{current_row}"].alignment = styles['align_center']
            ws[f"D{current_row}"].fill = styles['input_fill']
            ws[f"D{current_row}"].border = styles['thin_border']
            ws[f"D{current_row}"].number_format = styles['num_fmt_pct']
            ws[f"D{current_row}"].protection = Protection(locked=False)

            # Severidad Si (editable)
            ws[f"E{current_row}"] = f_s
            ws[f"E{current_row}"].font = styles['cell_bold']
            ws[f"E{current_row}"].alignment = styles['align_center']
            ws[f"E{current_row}"].fill = styles['input_fill']
            ws[f"E{current_row}"].border = styles['thin_border']
            ws[f"E{current_row}"].number_format = styles['num_fmt_dec']
            ws[f"E{current_row}"].protection = Protection(locked=False)

            # Volatilidad Vi (editable)
            ws[f"F{current_row}"] = f_v
            ws[f"F{current_row}"].font = styles['cell_bold']
            ws[f"F{current_row}"].alignment = styles['align_center']
            ws[f"F{current_row}"].fill = styles['input_fill']
            ws[f"F{current_row}"].border = styles['thin_border']
            ws[f"F{current_row}"].number_format = styles['num_fmt_dec']
            ws[f"F{current_row}"].protection = Protection(locked=False)

            # Riesgo Compuesto Ri = SQRT(S * V) (fórmula protegida)
            ws[f"G{current_row}"] = f"=ROUND(SQRT(E{current_row}*F{current_row}), 2)"
            ws[f"G{current_row}"].font = styles['cell_bold']
            ws[f"G{current_row}"].alignment = styles['align_center']
            ws[f"G{current_row}"].fill = styles['calc_fill']
            ws[f"G{current_row}"].border = styles['thin_border']
            ws[f"G{current_row}"].number_format = styles['num_fmt_dec']

            # Cuadrante de Incertidumbre (fórmula protegida)
            q_es = f'=IF(AND(E{current_row}>=3,F{current_row}>=3),"Q1 Crítico",IF(AND(E{current_row}>=3,F{current_row}<3),"Q2 Estructural",IF(AND(E{current_row}<3,F{current_row}>=3),"Q3 Alerta","Q4 Ruido")))'
            q_en = f'=IF(AND(E{current_row}>=3,F{current_row}>=3),"Q1 Critical",IF(AND(E{current_row}>=3,F{current_row}<3),"Q2 Structural",IF(AND(E{current_row}<3,F{current_row}>=3),"Q3 Early Warning","Q4 Minor Noise")))'
            ws[f"H{current_row}"] = q_es if lang == 'ES' else q_en
            ws[f"H{current_row}"].font = styles['cell_bold']
            ws[f"H{current_row}"].alignment = styles['align_center']
            ws[f"H{current_row}"].fill = styles['calc_fill']
            ws[f"H{current_row}"].border = styles['thin_border']

            # Justificación / Métrica (editable)
            ws[f"I{current_row}"] = f_just
            ws[f"I{current_row}"].font = styles['cell_font']
            ws[f"I{current_row}"].alignment = styles['align_left_wrap']
            ws[f"I{current_row}"].fill = styles['input_fill']
            ws[f"I{current_row}"].border = styles['thin_border']
            ws[f"I{current_row}"].protection = Protection(locked=False)

            current_row += 1

        end_factor_row = current_row - 1

        # Fila Resumen de la Dimensión
        ws[f"B{current_row}"] = "TOTAL"
        ws[f"B{current_row}"].font = styles['cell_bold']
        ws[f"B{current_row}"].alignment = styles['align_center']
        ws[f"B{current_row}"].fill = styles['total_fill']
        ws[f"B{current_row}"].border = styles['total_border']

        ws[f"C{current_row}"] = f"Promedio Ponderado de {dim['id']}" if lang == 'ES' else f"{dim['id']} Weighted Summary"
        ws[f"C{current_row}"].font = styles['cell_bold']
        ws[f"C{current_row}"].alignment = styles['align_left']
        ws[f"C{current_row}"].fill = styles['total_fill']
        ws[f"C{current_row}"].border = styles['total_border']

        # Suma de pesos de la dimensión = 100%
        ws[f"D{current_row}"] = f"=SUM(D{start_factor_row}:D{end_factor_row})"
        ws[f"D{current_row}"].font = styles['cell_bold']
        ws[f"D{current_row}"].alignment = styles['align_center']
        ws[f"D{current_row}"].fill = styles['total_fill']
        ws[f"D{current_row}"].border = styles['total_border']
        ws[f"D{current_row}"].number_format = styles['num_fmt_pct']

        # Severidad media ponderada
        ws[f"E{current_row}"] = f"=SUMPRODUCT(D{start_factor_row}:D{end_factor_row},E{start_factor_row}:E{end_factor_row})"
        ws[f"E{current_row}"].font = styles['cell_bold']
        ws[f"E{current_row}"].alignment = styles['align_center']
        ws[f"E{current_row}"].fill = styles['total_fill']
        ws[f"E{current_row}"].border = styles['total_border']
        ws[f"E{current_row}"].number_format = styles['num_fmt_dec']

        # Volatilidad media ponderada
        ws[f"F{current_row}"] = f"=SUMPRODUCT(D{start_factor_row}:D{end_factor_row},F{start_factor_row}:F{end_factor_row})"
        ws[f"F{current_row}"].font = styles['cell_bold']
        ws[f"F{current_row}"].alignment = styles['align_center']
        ws[f"F{current_row}"].fill = styles['total_fill']
        ws[f"F{current_row}"].border = styles['total_border']
        ws[f"F{current_row}"].number_format = styles['num_fmt_dec']

        # Riesgo medio ponderado
        ws[f"G{current_row}"] = f"=SUMPRODUCT(D{start_factor_row}:D{end_factor_row},G{start_factor_row}:G{end_factor_row})"
        ws[f"G{current_row}"].font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"G{current_row}"].alignment = styles['align_center']
        ws[f"G{current_row}"].fill = styles['total_fill']
        ws[f"G{current_row}"].border = styles['total_border']
        ws[f"G{current_row}"].number_format = styles['num_fmt_dec']

        # Clasificación global de la dimensión
        ws[f"H{current_row}"] = f'=IF(G{current_row}>=3.8,"Crítico",IF(G{current_row}>=2.8,"Moderado","Bajo"))' if lang == 'ES' else f'=IF(G{current_row}>=3.8,"Critical",IF(G{current_row}>=2.8,"Moderate","Low"))'
        ws[f"H{current_row}"].font = styles['cell_bold']
        ws[f"H{current_row}"].alignment = styles['align_center']
        ws[f"H{current_row}"].fill = styles['total_fill']
        ws[f"H{current_row}"].border = styles['total_border']

        ws[f"I{current_row}"] = "Métrica agregada calculada automáticamente" if lang == 'ES' else "Aggregated metric automatically computed"
        ws[f"I{current_row}"].font = styles['subtitle_font']
        ws[f"I{current_row}"].alignment = styles['align_left']
        ws[f"I{current_row}"].fill = styles['total_fill']
        ws[f"I{current_row}"].border = styles['total_border']

        current_row += 3  # Espaciado entre dimensiones

    # Ajuste de anchos de columna en Tab 2
    col_widths = {'A': 4, 'B': 12, 'C': 44, 'D': 14, 'E': 16, 'F': 16, 'G': 15, 'H': 18, 'I': 52}
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    apply_sheet_protection(ws)


# ==============================================================================
# PESTAÑA 3: MATRIZ SEVERIDAD VS VOLATILIDAD
# ==============================================================================
def build_tab3_matrix(wb, lang='ES'):
    ws = wb.create_sheet(title="Matriz Severidad vs Volatilidad" if lang == 'ES' else "Severity vs Volatility Matrix")
    ws.views.sheetView[0].showGridLines = True
    styles = get_base_styles(lang)

    t_eval = "Evaluación 6 Dimensiones" if lang == 'ES' else "6 Dimensions Assessment"

    # --- BANNER PRINCIPAL ---
    ws.merge_cells('B1:J1')
    ws['B1'] = "DATALARIA STRATEGY PRACTICE • MCKINSEY & BCG STANDARD"
    ws['B1'].font = styles['kicker_font']
    ws['B1'].fill = styles['title_fill']
    ws['B1'].alignment = styles['align_center']

    ws.merge_cells('B2:J2')
    ws['B2'] = "MATRIZ CARTESIANA DE INCERTIDUMBRE ESTRATÉGICA: SEVERIDAD VS. VOLATILIDAD" if lang == 'ES' else "STRATEGIC UNCERTAINTY CARTESIAN MATRIX: SEVERITY VS. VOLATILITY"
    ws['B2'].font = styles['title_font']
    ws['B2'].fill = styles['title_fill']
    ws['B2'].alignment = styles['align_center']

    ws.merge_cells('B3:J3')
    ws['B3'] = "Categorización de factores en 4 cuadrantes ejecutivos para asignación eficiente de recursos y protocolos de contingencia" if lang == 'ES' else "Categorization of factors into 4 executive quadrants for efficient capital allocation and contingency protocols"
    ws['B3'].font = styles['subtitle_font']
    ws['B3'].fill = styles['title_fill']
    ws['B3'].alignment = styles['align_center']
    ws.row_dimensions[2].height = 26

    # --- CUADRÍCULA DE LOS 4 CUADRANTES ESTRATÉGICOS (B5:J16) ---
    quadrants_info = [
        # (StartCol, EndCol, StartRow, EndRow, Title, ColorBG, ColorBorder, ColorText, Desc, Protocol)
        ("B", "E", 5, 10,
         "CUADRANTE 1: RIESGOS CRÍTICOS VOLÁTILES (Severidad ≥ 3.0 | Volatilidad ≥ 3.0)" if lang == 'ES' else "QUADRANT 1: CRITICAL VOLATILE RISKS (Severity ≥ 3.0 | Volatility ≥ 3.0)",
         COLOR_POL_BG, COLOR_POL_BORDER, COLOR_POL_TEXT,
         "Fuerzas de alto impacto y oscilación rápida impredecible. Amenaza existencial directa al P&L." if lang == 'ES' else "High-impact forces with rapid unpredictable swings. Immediate existential threat to operating margins.",
         "PROTOCOLO C-LEVEL: Blindaje activo, coberturas financieras obligatorias, fondos de reserva CAPEX y monitorización quincenal." if lang == 'ES' else "BOARD PROTOCOL: Active hedging, dedicated CAPEX contingency reserves, and biweekly board surveillance."),

        ("G", "J", 5, 10,
         "CUADRANTE 2: RIESGOS ESTRUCTURALES (Severidad ≥ 3.0 | Volatilidad < 3.0)" if lang == 'ES' else "QUADRANT 2: STRUCTURAL RISKS (Severity ≥ 3.0 | Volatility < 3.0)",
         COLOR_ECO_BG, COLOR_ECO_BORDER, COLOR_ECO_TEXT,
         "Fuerzas de severidad crítica pero evolución lenta, gradual y predecible en el horizonte temporal." if lang == 'ES' else "High severity forces evolving along predictable, multi-year structural trajectories.",
         "PROTOCOLO C-LEVEL: Planificación estratégica multianual, rediseño de procesos, reconversión de plantilla y transición ESG." if lang == 'ES' else "BOARD PROTOCOL: Multi-year strategic planning, operational re-engineering, and ESG transition roadmap."),

        ("B", "E", 12, 17,
         "CUADRANTE 3: ALERTAS TEMPRANAS (Severidad < 3.0 | Volatilidad ≥ 3.0)" if lang == 'ES' else "QUADRANT 3: EARLY WARNINGS (Severity < 3.0 | Volatility ≥ 3.0)",
         COLOR_TEC_BG, COLOR_TEC_BORDER, COLOR_TEC_TEXT,
         "Fuerzas de impacto actual acotado pero alta dinámica o velocidad de cambio. Cisnes negros potenciales." if lang == 'ES' else "Low current financial impact but high dynamism and velocity. Potential black swan incubation.",
         "PROTOCOLO C-LEVEL: Radar de vigilancia pasiva, umbrales automáticos de activación (triggers) sin comprometer capital pesado." if lang == 'ES' else "BOARD PROTOCOL: Automated surveillance radar, KPI activation triggers without heavy capital commitment."),

        ("G", "J", 12, 17,
         "CUADRANTE 4: RUIDOS MENORES (Severidad < 3.0 | Volatilidad < 3.0)" if lang == 'ES' else "QUADRANT 4: MINOR NOISE (Severity < 3.0 | Volatility < 3.0)",
         COLOR_BG_CARD, COLOR_BORDER_MED, "475569",
         "Factores de baja severidad y comportamiento estructural estable. Fricciones ordinarias del negocio." if lang == 'ES' else "Low severity factors with stable patterns. Ordinary operational frictions absorbed in daily workflow.",
         "PROTOCOLO C-LEVEL: Absorción operativa BAU (Business As Usual). Queda expresamente prohibido debatir en Comité de Dirección." if lang == 'ES' else "BOARD PROTOCOL: Routine BAU absorption. Strictly excluded from executive boardroom agendas.")
    ]

    for cs, ce, rs, re, q_title, q_bg, q_border, q_text, q_desc, q_prot in quadrants_info:
        # Título de Cuadrante
        ws.merge_cells(f"{cs}{rs}:{ce}{rs}")
        ws[f"{cs}{rs}"] = q_title
        ws[f"{cs}{rs}"].font = Font(name='Segoe UI', size=10, bold=True, color=q_text)
        ws[f"{cs}{rs}"].fill = PatternFill(start_color=q_bg, end_color=q_bg, fill_type='solid')
        ws[f"{cs}{rs}"].alignment = styles['align_center']
        style_merged_range(ws, f"{cs}{rs}:{ce}{rs}", border=Border(top=Side(style='medium', color=q_border)))

        # Descripción
        ws.merge_cells(f"{cs}{rs+1}:{ce}{rs+2}")
        ws[f"{cs}{rs+1}"] = q_desc
        ws[f"{cs}{rs+1}"].font = Font(name='Segoe UI', size=9, color="334155")
        ws[f"{cs}{rs+1}"].fill = PatternFill(start_color=COLOR_WHITE, end_color=COLOR_WHITE, fill_type='solid')
        ws[f"{cs}{rs+1}"].alignment = styles['align_left_wrap']
        style_merged_range(ws, f"{cs}{rs+1}:{ce}{rs+2}", border=styles['thin_border'])

        # Protocolo
        ws.merge_cells(f"{cs}{rs+3}:{ce}{rs+4}")
        ws[f"{cs}{rs+3}"] = q_prot
        ws[f"{cs}{rs+3}"].font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_NAVY_DARK)
        ws[f"{cs}{rs+3}"].fill = PatternFill(start_color=q_bg, end_color=q_bg, fill_type='solid')
        ws[f"{cs}{rs+3}"].alignment = styles['align_left_wrap']
        style_merged_range(ws, f"{cs}{rs+3}:{ce}{rs+4}", border=Border(bottom=Side(style='medium', color=q_border)))

    # --- TABLA MASTER DE CLASIFICACIÓN DE FACTORES (B19:J44) ---
    ws.merge_cells('B19:J19')
    ws['B19'] = "INVENTARIO CONSOLIDADO DE FACTORES MACRO Y CLASIFICACIÓN DE CUADRANTE" if lang == 'ES' else "CONSOLIDATED MACRO FACTOR INVENTORY & QUADRANT CLASSIFICATION"
    ws['B19'].font = styles['section_font']
    ws['B19'].fill = styles['section_fill']
    ws['B19'].alignment = styles['align_left']

    table_headers = [
        ("Código", 'B', 10),
        ("Dimensión PESTEL", 'C', 18),
        ("Descripción del Factor Macro", 'D', 38),
        ("Severidad (S)", 'E', 14),
        ("Volatilidad (V)", 'F', 14),
        ("Riesgo (R)", 'G', 14),
        ("Cuadrante Asignado", 'H', 18),
        ("Protocolo Recomendado", 'I', 30),
        ("Prioridad Comité", 'J', 16),
    ]

    for h_txt, col, w in table_headers:
        ws[f"{col}20"] = h_txt
        ws[f"{col}20"].font = styles['header_font']
        ws[f"{col}20"].fill = styles['header_fill']
        ws[f"{col}20"].alignment = styles['align_center'] if col in ['B', 'C', 'E', 'F', 'G', 'H', 'J'] else styles['align_left']
        ws[f"{col}20"].border = styles['header_border']

    # Referencias a los 24 factores en Pestaña 2
    # Filas en Pestaña 2:
    # POL: 7 a 10
    # ECO: 16 a 19
    # SOC: 25 a 28
    # TEC: 34 a 37
    # ENV: 43 a 46
    # LEG: 52 a 55
    factor_rows_in_tab2 = [
        ("Político" if lang == 'ES' else "Political", 7),
        ("Político" if lang == 'ES' else "Political", 8),
        ("Político" if lang == 'ES' else "Political", 9),
        ("Político" if lang == 'ES' else "Political", 10),
        ("Económico" if lang == 'ES' else "Economic", 16),
        ("Económico" if lang == 'ES' else "Economic", 17),
        ("Económico" if lang == 'ES' else "Economic", 18),
        ("Económico" if lang == 'ES' else "Economic", 19),
        ("Social" if lang == 'ES' else "Social", 25),
        ("Social" if lang == 'ES' else "Social", 26),
        ("Social" if lang == 'ES' else "Social", 27),
        ("Social" if lang == 'ES' else "Social", 28),
        ("Tecnológico" if lang == 'ES' else "Technological", 34),
        ("Tecnológico" if lang == 'ES' else "Technological", 35),
        ("Tecnológico" if lang == 'ES' else "Technological", 36),
        ("Tecnológico" if lang == 'ES' else "Technological", 37),
        ("Ecológico" if lang == 'ES' else "Environmental", 43),
        ("Ecológico" if lang == 'ES' else "Environmental", 44),
        ("Ecológico" if lang == 'ES' else "Environmental", 45),
        ("Ecológico" if lang == 'ES' else "Environmental", 46),
        ("Legal" if lang == 'ES' else "Legal & Reg.", 52),
        ("Legal" if lang == 'ES' else "Legal & Reg.", 53),
        ("Legal" if lang == 'ES' else "Legal & Reg.", 54),
        ("Legal" if lang == 'ES' else "Legal & Reg.", 55),
    ]

    curr_row = 21
    for dim_label, t2_r in factor_rows_in_tab2:
        ws[f"B{curr_row}"] = f"='{t_eval}'!B{t2_r}"
        ws[f"B{curr_row}"].font = styles['code_font']
        ws[f"B{curr_row}"].alignment = styles['align_center']
        ws[f"B{curr_row}"].fill = styles['calc_fill']
        ws[f"B{curr_row}"].border = styles['thin_border']

        ws[f"C{curr_row}"] = dim_label
        ws[f"C{curr_row}"].font = styles['cell_font']
        ws[f"C{curr_row}"].alignment = styles['align_center']
        ws[f"C{curr_row}"].fill = styles['calc_fill']
        ws[f"C{curr_row}"].border = styles['thin_border']

        ws[f"D{curr_row}"] = f"='{t_eval}'!C{t2_r}"
        ws[f"D{curr_row}"].font = styles['cell_bold']
        ws[f"D{curr_row}"].alignment = styles['align_left_wrap']
        ws[f"D{curr_row}"].fill = styles['calc_fill']
        ws[f"D{curr_row}"].border = styles['thin_border']

        ws[f"E{curr_row}"] = f"='{t_eval}'!E{t2_r}"
        ws[f"E{curr_row}"].font = styles['cell_font']
        ws[f"E{curr_row}"].alignment = styles['align_center']
        ws[f"E{curr_row}"].fill = styles['calc_fill']
        ws[f"E{curr_row}"].border = styles['thin_border']
        ws[f"E{curr_row}"].number_format = styles['num_fmt_dec']

        ws[f"F{curr_row}"] = f"='{t_eval}'!F{t2_r}"
        ws[f"F{curr_row}"].font = styles['cell_font']
        ws[f"F{curr_row}"].alignment = styles['align_center']
        ws[f"F{curr_row}"].fill = styles['calc_fill']
        ws[f"F{curr_row}"].border = styles['thin_border']
        ws[f"F{curr_row}"].number_format = styles['num_fmt_dec']

        ws[f"G{curr_row}"] = f"='{t_eval}'!G{t2_r}"
        ws[f"G{curr_row}"].font = styles['cell_bold']
        ws[f"G{curr_row}"].alignment = styles['align_center']
        ws[f"G{curr_row}"].fill = styles['calc_fill']
        ws[f"G{curr_row}"].border = styles['thin_border']
        ws[f"G{curr_row}"].number_format = styles['num_fmt_dec']

        ws[f"H{curr_row}"] = f"='{t_eval}'!H{t2_r}"
        ws[f"H{curr_row}"].font = styles['cell_bold']
        ws[f"H{curr_row}"].alignment = styles['align_center']
        ws[f"H{curr_row}"].fill = styles['calc_fill']
        ws[f"H{curr_row}"].border = styles['thin_border']

        # Protocolo dependiente de cuadrante
        p_es = f'=IF(LEFT(H{curr_row},2)="Q1","Contingencia Activa y Hedging",IF(LEFT(H{curr_row},2)="Q2","Planificación Multianual",IF(LEFT(H{curr_row},2)="Q3","Triggers de Alerta","Monitoreo Operativo")))'
        p_en = f'=IF(LEFT(H{curr_row},2)="Q1","Active Hedging & Contingency",IF(LEFT(H{curr_row},2)="Q2","Multi-Year Planning",IF(LEFT(H{curr_row},2)="Q3","Watchlist Triggers","Routine Monitoring")))'
        ws[f"I{curr_row}"] = p_es if lang == 'ES' else p_en
        ws[f"I{curr_row}"].font = styles['cell_font']
        ws[f"I{curr_row}"].alignment = styles['align_left']
        ws[f"I{curr_row}"].fill = styles['calc_fill']
        ws[f"I{curr_row}"].border = styles['thin_border']

        # Prioridad
        prio_es = f'=IF(G{curr_row}>=4.0,"P1 Inmediata",IF(G{curr_row}>=3.2,"P2 Táctica","P3 Ordinaria"))'
        prio_en = f'=IF(G{curr_row}>=4.0,"P1 Urgent",IF(G{curr_row}>=3.2,"P2 Tactical","P3 Standard"))'
        ws[f"J{curr_row}"] = prio_es if lang == 'ES' else prio_en
        ws[f"J{curr_row}"].font = styles['cell_bold']
        ws[f"J{curr_row}"].alignment = styles['align_center']
        ws[f"J{curr_row}"].fill = styles['calc_fill']
        ws[f"J{curr_row}"].border = styles['thin_border']

        curr_row += 1

    # Ajuste de anchos de columna en Tab 3
    col_widths = {'A': 4, 'B': 10, 'C': 18, 'D': 40, 'E': 14, 'F': 14, 'G': 14, 'H': 18, 'I': 30, 'J': 16}
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    apply_sheet_protection(ws)


# ==============================================================================
# PESTAÑA 4: PLAN DE RESILIENCIA & CONTINGENCIA
# ==============================================================================
def build_tab4_action_plan(wb, lang='ES'):
    ws = wb.create_sheet(title="Plan Resiliencia & Contingencia" if lang == 'ES' else "Macro Resilience Action Plan")
    ws.views.sheetView[0].showGridLines = True
    styles = get_base_styles(lang)

    # --- BANNER PRINCIPAL ---
    ws.merge_cells('B1:K1')
    ws['B1'] = "DATALARIA STRATEGY PRACTICE • MCKINSEY & BCG STANDARD • BOARDROOM EXECUTION"
    ws['B1'].font = styles['kicker_font']
    ws['B1'].fill = styles['title_fill']
    ws['B1'].alignment = styles['align_center']

    ws.merge_cells('B2:K2')
    ws['B2'] = "PLAN DE RESILIENCIA ESTRATÉGICA & CONTINGENCIA MACRO (2026 - 2027)" if lang == 'ES' else "STRATEGIC RESILIENCE & MACRO CONTINGENCY ROADMAP (2026 - 2027)"
    ws['B2'].font = styles['title_font']
    ws['B2'].fill = styles['title_fill']
    ws['B2'].alignment = styles['align_center']

    ws.merge_cells('B3:K3')
    ws['B3'] = "Iniciativas de mitigación formalmente asignadas a ejecutivos C-Level, con presupuesto CAPEX/OPEX y preservación de EBITDA" if lang == 'ES' else "Mitigation initiatives formally assigned to C-Suite Owners, with CAPEX/OPEX funding and audited EBITDA preservation"
    ws['B3'].font = styles['subtitle_font']
    ws['B3'].fill = styles['title_fill']
    ws['B3'].alignment = styles['align_center']
    ws.row_dimensions[2].height = 26

    # --- 4 TARJETAS KPI DE PRESUPUESTO & RETORNO (B5:K7) ---
    kpis_plan = [
        ('B', 'D',
         "TOTAL CAPEX CONTINGENCIA" if lang == 'ES' else "TOTAL CONTINGENCY CAPEX",
         "=SUM(G11:G18)",
         "Inversión de capital en blindaje" if lang == 'ES' else "Capital expenditure in shielding",
         styles['num_fmt_curr']),

        ('E', 'G',
         "TOTAL OPEX DE COBERTURA" if lang == 'ES' else "TOTAL HEDGING OPEX",
         "=SUM(H11:H18)",
         "Gasto operativo y pólizas anuales" if lang == 'ES' else "Operating expense & annual hedges",
         styles['num_fmt_curr']),

        ('H', 'I',
         "PRESUPUESTO TOTAL ASIGNADO" if lang == 'ES' else "TOTAL ALLOCATED BUDGET",
         "=SUM(I11:I18)",
         "=D24" if lang == 'ES' else "=D24",
         styles['num_fmt_curr']),

        ('J', 'K',
         "EBITDA ANUAL PRESERVADO" if lang == 'ES' else "ANNUAL EBITDA PRESERVED",
         "1.850.000 €" if lang == 'ES' else "$1,850,000",
         "ROI de Resiliencia: 3.4x" if lang == 'ES' else "Resilience ROI: 3.4x",
         None)
    ]

    for cs, ce, title, val_f, sub_t, num_fmt in kpis_plan:
        ws.merge_cells(f"{cs}5:{ce}5")
        ws[f"{cs}5"] = title
        ws[f"{cs}5"].font = Font(name='Segoe UI', size=9, bold=True, color="64748B")
        ws[f"{cs}5"].fill = PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid')
        ws[f"{cs}5"].alignment = styles['align_center']

        ws.merge_cells(f"{cs}6:{ce}6")
        ws[f"{cs}6"] = val_f
        ws[f"{cs}6"].font = Font(name='Segoe UI', size=15, bold=True, color=COLOR_NAVY_DARK)
        ws[f"{cs}6"].fill = PatternFill(start_color=COLOR_BG_LIGHT, end_color=COLOR_BG_LIGHT, fill_type='solid')
        ws[f"{cs}6"].alignment = styles['align_center']
        if num_fmt:
            ws[f"{cs}6"].number_format = num_fmt

        ws.merge_cells(f"{cs}7:{ce}7")
        ws[f"{cs}7"] = sub_t
        ws[f"{cs}7"].font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"{cs}7"].fill = PatternFill(start_color=COLOR_BG_LIGHT, end_color=COLOR_BG_LIGHT, fill_type='solid')
        ws[f"{cs}7"].alignment = styles['align_center']

        for r in range(5, 8):
            for c_idx in range(openpyxl.utils.column_index_from_string(cs), openpyxl.utils.column_index_from_string(ce) + 1):
                col_let = get_column_letter(c_idx)
                top_s = 'thin' if r == 5 else None
                bot_s = 'thin' if r == 7 else None
                left_s = 'thin' if col_let == cs else None
                right_s = 'thin' if col_let == ce else None
                ws[f"{col_let}{r}"].border = Border(
                    top=Side(style=top_s, color=COLOR_BORDER_MED) if top_s else None,
                    bottom=Side(style=bot_s, color=COLOR_BORDER_MED) if bot_s else None,
                    left=Side(style=left_s, color=COLOR_BORDER_MED) if left_s else None,
                    right=Side(style=right_s, color=COLOR_BORDER_MED) if right_s else None
                )

    # --- TABLA DE INICIATIVAS DE MITIGACIÓN (B9:K18) ---
    ws.merge_cells('B9:K9')
    ws['B9'] = "PROGRAMA DE ACCIÓN DE CONTINGENCIA: PROYECTOS, SPONSORS C-LEVEL Y PRESUPUESTOS" if lang == 'ES' else "CONTINGENCY ACTION PROGRAM: PROJECTS, C-SUITE SPONSORS & BUDGETS"
    ws['B9'].font = styles['section_font']
    ws['B9'].fill = styles['section_fill']
    ws['B9'].alignment = styles['align_left']

    action_headers = [
        ("ID", 'B', 10),
        ("Dimensión", 'C', 14),
        ("Factor Mitigado", 'D', 24),
        ("Iniciativa de Blindaje / Contingencia" if lang == 'ES' else "Shielding / Contingency Initiative", 'E', 42),
        ("Owner C-Level", 'F', 14),
        ("CAPEX (€)" if lang == 'ES' else "CAPEX ($)", 'G', 15),
        ("OPEX (€)" if lang == 'ES' else "OPEX ($)", 'H', 15),
        ("Total (€)" if lang == 'ES' else "Total ($)", 'I', 15),
        ("Plazo / Hito" if lang == 'ES' else "Timeline / Milestone", 'J', 14),
        ("KPI de Impacto en EBITDA" if lang == 'ES' else "EBITDA Impact KPI", 'K', 32),
    ]

    for h_txt, col, w in action_headers:
        ws[f"{col}10"] = h_txt
        ws[f"{col}10"].font = styles['header_font']
        ws[f"{col}10"].fill = styles['header_fill']
        ws[f"{col}10"].alignment = styles['align_center'] if col in ['B', 'C', 'F', 'G', 'H', 'I', 'J'] else styles['align_left']
        ws[f"{col}10"].border = styles['header_border']

    initiatives_data = [
        ("ACT-01", "Económico" if lang == 'ES' else "Economic", "ECO-01 Energía",
         "Contratos PPA a largo plazo y cobertura de futuros de gas al 70%" if lang == 'ES' else "Corporate PPA contracts & 70% natural gas derivatives hedging",
         "CFO", 35000, 45000, "Q1 2026",
         "Blindaje de margen bruto frente a picos energéticos (+420k€ EBITDA)" if lang == 'ES' else "Gross margin shielded against energy spikes (+420k EBITDA)"),

        ("ACT-02", "Tecnológico" if lang == 'ES' else "Technological", "TEC-01 GenAI",
         "Adopción interna de agentes LLM en servicio cliente y operaciones" if lang == 'ES' else "In-house deployment of enterprise agentic LLMs across operations",
         "CTO", 120000, 30000, "Q2 2026",
         "Reducción de coste unitario operativo en 28% y retención de cuentas" if lang == 'ES' else "Unit operating cost reduced by 28% and client retention fortified"),

        ("ACT-03", "Legal" if lang == 'ES' else "Legal & Reg.", "LEG-01 AI Act",
         "Auditoría técnica de algoritmos y certificación de gobernanza ISO 42001" if lang == 'ES' else "Algorithmic audit & ISO 42001 AI governance compliance certification",
         "CLO", 40000, 25000, "Q2 2026",
         "Eliminación total del riesgo sancionador de hasta 35M€ ante la UE" if lang == 'ES' else "Zero exposure to EU regulatory penalties up to 35M€"),

        ("ACT-04", "Político" if lang == 'ES' else "Political", "POL-01 Aranceles",
         "Nearshoring de ensamblaje en Europa del Este para eludir aranceles" if lang == 'ES' else "Nearshoring assembly facility in Eastern Europe to bypass tariffs",
         "COO", 150000, 20000, "Q3 2026",
         "Preservación de cuota de mercado en contratos públicos comunitarios" if lang == 'ES' else "Safeguarded market share in public EU government tenders"),

        ("ACT-05", "Social" if lang == 'ES' else "Social", "SOC-01 Talento",
         "Academia interna de ingeniería y plan de retención de talento clave" if lang == 'ES' else "Internal technical academy & key retention bonus program",
         "CHRO", 20000, 45000, "Q1 2026",
         "Rotación voluntaria técnica reducida del 18% al 5.5%" if lang == 'ES' else "STEM voluntary turnover dropped from 18% to 5.5%"),

        ("ACT-06", "Ecológico" if lang == 'ES' else "Environmental", "ENV-01 CSRD",
         "Software de contabilidad de carbono e integración ERP de alcance 1-3" if lang == 'ES' else "Carbon accounting software & ERP Scope 1-3 integration",
         "CSO", 55000, 15000, "Q2 2026",
         "Calificación ESG superior requerida para licitaciones bancarias" if lang == 'ES' else "Tier-1 ESG credit rating securing lower debt refinancing spreads"),

        ("ACT-07", "Tecnológico" if lang == 'ES' else "Technological", "TEC-02 Ciber",
         "Implantación de arquitectura Zero-Trust y SOC externo 24/7" if lang == 'ES' else "Zero-Trust architecture rollout & 24/7 managed SOC monitoring",
         "CISO", 65000, 35000, "Q1 2026",
         "Reducción de prima de ciberseguro en 35% y riesgo cero de parada" if lang == 'ES' else "Cyber-insurance premium reduced by 35% and business continuity"),

        ("ACT-08", "Económico" if lang == 'ES' else "Economic", "ECO-04 Divisas",
         "Pólizas Forward sindicadas para flujos de caja en USD y GBP" if lang == 'ES' else "FX forward contracts for projected USD & GBP cash flows",
         "CFO", 0, 15000, "Q1 2026",
         "Estabilización de ingresos por exportación frente a oscilaciones de tipo" if lang == 'ES' else "Stabilized overseas export margins against currency swings")
    ]

    for idx, (a_id, a_dim, a_fact, a_init, a_own, a_cap, a_op, a_plaz, a_kpi) in enumerate(initiatives_data, start=11):
        ws[f"B{idx}"] = a_id
        ws[f"B{idx}"].font = styles['code_font']
        ws[f"B{idx}"].alignment = styles['align_center']
        ws[f"B{idx}"].fill = styles['calc_fill']
        ws[f"B{idx}"].border = styles['thin_border']

        ws[f"C{idx}"] = a_dim
        ws[f"C{idx}"].font = styles['cell_font']
        ws[f"C{idx}"].alignment = styles['align_center']
        ws[f"C{idx}"].fill = styles['calc_fill']
        ws[f"C{idx}"].border = styles['thin_border']

        ws[f"D{idx}"] = a_fact
        ws[f"D{idx}"].font = styles['cell_font']
        ws[f"D{idx}"].alignment = styles['align_center']
        ws[f"D{idx}"].fill = styles['calc_fill']
        ws[f"D{idx}"].border = styles['thin_border']

        # Iniciativa editable
        ws[f"E{idx}"] = a_init
        ws[f"E{idx}"].font = styles['cell_font']
        ws[f"E{idx}"].alignment = styles['align_left_wrap']
        ws[f"E{idx}"].fill = styles['input_fill']
        ws[f"E{idx}"].border = styles['thin_border']
        ws[f"E{idx}"].protection = Protection(locked=False)

        # Owner C-Level editable
        ws[f"F{idx}"] = a_own
        ws[f"F{idx}"].font = styles['cell_bold']
        ws[f"F{idx}"].alignment = styles['align_center']
        ws[f"F{idx}"].fill = styles['input_fill']
        ws[f"F{idx}"].border = styles['thin_border']
        ws[f"F{idx}"].protection = Protection(locked=False)

        # CAPEX editable
        ws[f"G{idx}"] = a_cap
        ws[f"G{idx}"].font = styles['cell_bold']
        ws[f"G{idx}"].alignment = styles['align_right']
        ws[f"G{idx}"].fill = styles['input_fill']
        ws[f"G{idx}"].border = styles['thin_border']
        ws[f"G{idx}"].number_format = styles['num_fmt_curr']
        ws[f"G{idx}"].protection = Protection(locked=False)

        # OPEX editable
        ws[f"H{idx}"] = a_op
        ws[f"H{idx}"].font = styles['cell_bold']
        ws[f"H{idx}"].alignment = styles['align_right']
        ws[f"H{idx}"].fill = styles['input_fill']
        ws[f"H{idx}"].border = styles['thin_border']
        ws[f"H{idx}"].number_format = styles['num_fmt_curr']
        ws[f"H{idx}"].protection = Protection(locked=False)

        # Total fórmula
        ws[f"I{idx}"] = f"=G{idx}+H{idx}"
        ws[f"I{idx}"].font = styles['cell_bold']
        ws[f"I{idx}"].alignment = styles['align_right']
        ws[f"I{idx}"].fill = styles['calc_fill']
        ws[f"I{idx}"].border = styles['thin_border']
        ws[f"I{idx}"].number_format = styles['num_fmt_curr']

        # Plazo editable
        ws[f"J{idx}"] = a_plaz
        ws[f"J{idx}"].font = styles['cell_font']
        ws[f"J{idx}"].alignment = styles['align_center']
        ws[f"J{idx}"].fill = styles['input_fill']
        ws[f"J{idx}"].border = styles['thin_border']
        ws[f"J{idx}"].protection = Protection(locked=False)

        # KPI editable
        ws[f"K{idx}"] = a_kpi
        ws[f"K{idx}"].font = styles['cell_font']
        ws[f"K{idx}"].alignment = styles['align_left_wrap']
        ws[f"K{idx}"].fill = styles['input_fill']
        ws[f"K{idx}"].border = styles['thin_border']
        ws[f"K{idx}"].protection = Protection(locked=False)

    # Fila Total Programa
    ws['B19'] = "TOTAL"
    ws['B19'].font = styles['cell_bold']
    ws['B19'].alignment = styles['align_center']
    ws['B19'].fill = styles['total_fill']
    ws['B19'].border = styles['total_border']

    ws['C19'] = "Dotación Presupuestaria Total" if lang == 'ES' else "Total Budget Commitment"
    ws['C19'].font = styles['cell_bold']
    ws['C19'].alignment = styles['align_left']
    ws['C19'].fill = styles['total_fill']
    ws['C19'].border = styles['total_border']

    ws['D19'] = "8 Iniciativas" if lang == 'ES' else "8 Initiatives"
    ws['D19'].font = styles['cell_font']
    ws['D19'].alignment = styles['align_center']
    ws['D19'].fill = styles['total_fill']
    ws['D19'].border = styles['total_border']

    ws['E19'] = ""
    ws['E19'].fill = styles['total_fill']
    ws['E19'].border = styles['total_border']

    ws['F19'] = "Comité C-Level" if lang == 'ES' else "C-Suite Board"
    ws['F19'].font = styles['cell_bold']
    ws['F19'].alignment = styles['align_center']
    ws['F19'].fill = styles['total_fill']
    ws['F19'].border = styles['total_border']

    ws['G19'] = "=SUM(G11:G18)"
    ws['G19'].font = styles['cell_bold']
    ws['G19'].alignment = styles['align_right']
    ws['G19'].fill = styles['total_fill']
    ws['G19'].border = styles['total_border']
    ws['G19'].number_format = styles['num_fmt_curr']

    ws['H19'] = "=SUM(H11:H18)"
    ws['H19'].font = styles['cell_bold']
    ws['H19'].alignment = styles['align_right']
    ws['H19'].fill = styles['total_fill']
    ws['H19'].border = styles['total_border']
    ws['H19'].number_format = styles['num_fmt_curr']

    ws['I19'] = "=SUM(I11:I18)"
    ws['I19'].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws['I19'].alignment = styles['align_right']
    ws['I19'].fill = styles['total_fill']
    ws['I19'].border = styles['total_border']
    ws['I19'].number_format = styles['num_fmt_curr']

    ws['J19'] = "Q1 - Q4 2026"
    ws['J19'].font = styles['cell_bold']
    ws['J19'].alignment = styles['align_center']
    ws['J19'].fill = styles['total_fill']
    ws['J19'].border = styles['total_border']

    ws['K19'] = "Retorno de Inversión en Resiliencia: 3.4x EBITDA" if lang == 'ES' else "Resilience ROI: 3.4x Protected EBITDA"
    ws['K19'].font = styles['cell_bold']
    ws['K19'].alignment = styles['align_left']
    ws['K19'].fill = styles['total_fill']
    ws['K19'].border = styles['total_border']

    # --- RESOLUCIÓN DEL CONSEJO (B21:K25) ---
    ws.merge_cells('B21:K21')
    ws['B21'] = "GATEWAY DE DECISIÓN DEL COMITÉ DE DIRECCIÓN / BOARD DECISION GATEWAY" if lang == 'ES' else "EXECUTIVE BOARD DECISION GATEWAY & FORMAL RESOLUTIONS"
    ws['B21'].font = styles['section_font']
    ws['B21'].fill = styles['section_fill']
    ws['B21'].alignment = styles['align_left']

    res_headers = [
        ("Resolución Directiva Sometida a Aprobación" if lang == 'ES' else "Board Resolution Submitted for Approval", 'B', 'C'),
        ("Votación" if lang == 'ES' else "Vote", 'D', 'D'),
        ("Detalle de la Decisión & Mandato Ejecutivo" if lang == 'ES' else "Decision Detail & Executive Mandate", 'E', 'K'),
    ]

    for h_txt, col_s, col_e in res_headers:
        if col_s != col_e:
            ws.merge_cells(f"{col_s}22:{col_e}22")
        ws[f"{col_s}22"] = h_txt
        ws[f"{col_s}22"].font = styles['header_font']
        ws[f"{col_s}22"].fill = styles['header_fill']
        ws[f"{col_s}22"].alignment = styles['align_center'] if col_s == 'D' else styles['align_left']
        if col_s != col_e:
            style_merged_range(ws, f"{col_s}22:{col_e}22", border=styles['header_border'])
        else:
            ws[f"{col_s}22"].border = styles['header_border']

    resolutions_data = [
        ("Resolución 1: Dotación de Fondos",
         "APROBADO" if lang == 'ES' else "APPROVED",
         "Aprobación formal de 485.000 € en CAPEX y 230.000 € en OPEX de contingencia macro para 2026." if lang == 'ES' else "Formal authorization of $485,000 CAPEX and $230,000 OPEX macro contingency reserves for 2026."),
        ("Resolución 2: Ratificación de Owners",
         "APROBADO" if lang == 'ES' else "APPROVED",
         "Designación vinculante de los ejecutivos C-Level responsables de la ejecución de cada hito." if lang == 'ES' else "Binding ratification of C-Suite sponsors accountable for milestone execution and KPIs."),
        ("Resolución 3: Calendario de Seguimiento",
         "APROBADO" if lang == 'ES' else "APPROVED",
         "Auditoría trimestral de avance ante el Comité de Auditoría y Riesgos del Consejo." if lang == 'ES' else "Mandatory quarterly review presented to the Board Audit & Risk Committee.")
    ]

    for idx, (r_title, r_vote, r_desc) in enumerate(resolutions_data, start=23):
        ws.merge_cells(f"B{idx}:C{idx}")
        ws[f"B{idx}"] = r_title
        ws[f"B{idx}"].font = styles['cell_bold']
        ws[f"B{idx}"].alignment = styles['align_left']
        ws[f"B{idx}"].fill = styles['calc_fill']
        style_merged_range(ws, f"B{idx}:C{idx}", border=styles['thin_border'])

        ws[f"D{idx}"] = r_vote
        ws[f"D{idx}"].font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_EMERALD_ACCENT)
        ws[f"D{idx}"].alignment = styles['align_center']
        ws[f"D{idx}"].fill = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type='solid')
        ws[f"D{idx}"].border = styles['thin_border']
        ws[f"D{idx}"].protection = Protection(locked=False)  # Editable por el usuario si lo desea

        ws.merge_cells(f"E{idx}:K{idx}")
        ws[f"E{idx}"] = r_desc
        ws[f"E{idx}"].font = styles['cell_font']
        ws[f"E{idx}"].alignment = styles['align_left_wrap']
        ws[f"E{idx}"].fill = styles['calc_fill']
        style_merged_range(ws, f"E{idx}:K{idx}", border=styles['thin_border'])

    # Ajuste de anchos de columna en Tab 4
    col_widths = {'A': 4, 'B': 12, 'C': 16, 'D': 24, 'E': 44, 'F': 14, 'G': 15, 'H': 15, 'I': 16, 'J': 16, 'K': 36}
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    apply_sheet_protection(ws)


def generate_workbook(lang='ES', out_path='PESTEL_Cuantitativo_Datalaria_ES.xlsx'):
    wb = openpyxl.Workbook()
    build_tab1_dashboard(wb, lang=lang)
    build_tab2_evaluation(wb, lang=lang)
    build_tab3_matrix(wb, lang=lang)
    build_tab4_action_plan(wb, lang=lang)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    wb.save(out_path)
    print(f"[OK] Modelo Excel generado ({lang}): {out_path}")


def main():
    dir_es = os.path.join("packages", "[ES]_PESTEL_Cuantitativo")
    dir_en = os.path.join("packages", "[EN]_Quantitative_PESTEL")

    path_es = os.path.join(dir_es, "PESTEL_Cuantitativo_Datalaria_ES.xlsx")
    path_en = os.path.join(dir_en, "Quantitative_PESTEL_Datalaria_EN.xlsx")

    generate_workbook(lang='ES', out_path=path_es)
    generate_workbook(lang='EN', out_path=path_en)


if __name__ == '__main__':
    main()
