#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos analíticos de decisión estratégica en Excel oficiales de Datalaria:
1. packages/ES_Matriz_McKinsey_GE_Datalaria.xlsx (Versión en Español)
2. packages/EN_McKinsey_GE_Matrix_Datalaria.xlsx (Versión en Inglés)

Estructura de 3 pestañas estructuradas e interconectadas:
- Pestaña 1: "01_Dashboard_Ejecutivo" / "01_Executive_Dashboard"
- Pestaña 2: "02_Evaluacion_Multifactorial" / "02_Multifactor_Assessment"
- Pestaña 3: "03_Plan_Asignacion_Capital" / "03_Capital_Allocation_Plan"

Estándar de Protección de Celdas ECMA-376 / Office OpenXML (openpyxl):
- Celdas de entrada del usuario (inputs): Protection(locked=False) y fondo marfil (#FFFBEB).
- Celdas con fórmulas, cabeceras, totales y KPIs: Protection(locked=True).
- Protección de hoja:
    ws.protection.set_password("Datalaria2026")
    ws.protection.sheet = True
    ws.protection.objects = True
    ws.protection.scenarios = True
    ws.protection.selectUnlockedCells = False  # 0 = sin restricción (permite clic y edición)
    ws.protection.selectLockedCells = False    # 0 = sin restricción de selección (lectura)
    if allow_structure:
        ws.protection.insertRows = False
        ws.protection.deleteRows = False
        ws.protection.formatCells = False
        ws.protection.formatColumns = False
        ws.protection.formatRows = False
        ws.protection.sort = False
        ws.protection.autoFilter = False
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = "0F172A"       # Slate 900 / Títulos principales y cabeceras
COLOR_NAVY_MED = "1E293B"        # Slate 800 / Subcabeceras
COLOR_NAVY_LIGHT = "334155"      # Slate 700 / Texto secundario
COLOR_BLUE_ACCENT = "2563EB"     # Blue 600 / Azul Consultoría Datalaria
COLOR_BLUE_LIGHT = "EFF6FF"      # Blue 50 / Fondos suaves

# Zonas Estratégicas McKinsey / GE
COLOR_GREEN_BG = "D1FAE5"        # Verde suave (Invest / Grow)
COLOR_GREEN_TEXT = "065F46"      # Verde texto
COLOR_GREEN_BORDER = "10B981"    # Verde acento

COLOR_AMBER_BG = "FEF3C7"        # Ámbar suave (Selectivity / Hold)
COLOR_AMBER_TEXT = "92400E"      # Ámbar texto
COLOR_AMBER_BORDER = "F59E0B"    # Ámbar acento

COLOR_RED_BG = "FEE2E2"          # Rojo suave (Harvest / Divest)
COLOR_RED_TEXT = "991B1B"        # Rojo texto
COLOR_RED_BORDER = "EF4444"      # Rojo acento

COLOR_BG_CARD = "F1F5F9"         # Slate 100 / Totales y cajas resumen
COLOR_BG_LIGHT = "F8FAFC"        # Slate 50 / Celdas calculadas, fórmulas y textos fijos bloqueados
COLOR_WHITE = "FFFFFF"           # Blanco puro para celdas de entrada desbloqueadas
COLOR_BG_INPUT = "FFFFFF"        # Blanco puro para inputs

COLOR_BORDER_LIGHT = "CBD5E1"    # Slate 300
COLOR_BORDER_MED = "94A3B8"      # Slate 400

PASSWORD_PROTECT = "Datalaria2026"
DIR_PACKAGES = "packages"

PROT_UNLOCKED = Protection(locked=False)
PROT_LOCKED = Protection(locked=True)


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
        left=Side(style='thin', color=COLOR_BORDER_LIGHT),
        right=Side(style='thin', color=COLOR_BORDER_LIGHT),
        top=Side(style='thin', color=COLOR_BORDER_MED),
        bottom=Side(style='double', color=COLOR_NAVY_DARK)
    )
    input_border = Border(
        left=Side(style='thin', color=COLOR_BORDER_LIGHT),
        right=Side(style='thin', color=COLOR_BORDER_LIGHT),
        top=Side(style='thin', color=COLOR_BORDER_LIGHT),
        bottom=Side(style='thin', color=COLOR_BORDER_LIGHT)
    )

    if lang == 'ES':
        num_fmt_curr = "#,##0 €"
        num_fmt_curr_dec = "#,##0.00 €"
        num_fmt_pct = "0.0%"
        num_fmt_dec = "0.00"
        num_fmt_int = "#,##0"
    else:
        num_fmt_curr = "$#,##0"
        num_fmt_curr_dec = "$#,##0.00"
        num_fmt_pct = "0.0%"
        num_fmt_dec = "0.00"
        num_fmt_int = "#,##0"

    return {
        'thin_border': thin_border,
        'header_border': header_border,
        'total_border': total_border,
        'input_border': input_border,
        'font_title': Font(name='Segoe UI', size=15, bold=True, color=COLOR_NAVY_DARK),
        'font_subtitle': Font(name='Segoe UI', size=10, bold=True, color=COLOR_BLUE_ACCENT),
        'font_meta': Font(name='Segoe UI', size=9, italic=True, color="64748B"),
        'font_section': Font(name='Segoe UI', size=11, bold=True, color=COLOR_NAVY_DARK),
        'font_header': Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_WHITE),
        'font_subhead': Font(name='Segoe UI', size=9, bold=True, color=COLOR_NAVY_MED),
        'font_regular': Font(name='Segoe UI', size=9, color=COLOR_NAVY_DARK),
        'font_bold': Font(name='Segoe UI', size=9, bold=True, color=COLOR_NAVY_DARK),
        'font_kpi_val': Font(name='Segoe UI', size=16, bold=True, color=COLOR_NAVY_DARK),
        'font_kpi_lbl': Font(name='Segoe UI', size=8, bold=True, color="64748B"),
        'font_badge': Font(name='Segoe UI', size=8.5, bold=True),
        'fill_navy_hdr': PatternFill(start_color=COLOR_NAVY_DARK, end_color=COLOR_NAVY_DARK, fill_type='solid'),
        'fill_navy_sub': PatternFill(start_color=COLOR_NAVY_MED, end_color=COLOR_NAVY_MED, fill_type='solid'),
        'fill_blue_hdr': PatternFill(start_color=COLOR_BLUE_ACCENT, end_color=COLOR_BLUE_ACCENT, fill_type='solid'),
        'fill_card_bg': PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid'),
        'fill_calc': PatternFill(start_color=COLOR_BG_LIGHT, end_color=COLOR_BG_LIGHT, fill_type='solid'),
        'fill_input': PatternFill(start_color=COLOR_WHITE, end_color=COLOR_WHITE, fill_type='solid'),
        'fill_total': PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid'),
        'fill_green_zone': PatternFill(start_color=COLOR_GREEN_BG, end_color=COLOR_GREEN_BG, fill_type='solid'),
        'fill_amber_zone': PatternFill(start_color=COLOR_AMBER_BG, end_color=COLOR_AMBER_BG, fill_type='solid'),
        'fill_red_zone': PatternFill(start_color=COLOR_RED_BG, end_color=COLOR_RED_BG, fill_type='solid'),
        'align_center': Alignment(horizontal='center', vertical='center'),
        'align_left': Alignment(horizontal='left', vertical='center'),
        'align_right': Alignment(horizontal='right', vertical='center'),
        'align_center_wrap': Alignment(horizontal='center', vertical='center', wrap_text=True),
        'align_left_wrap': Alignment(horizontal='left', vertical='center', wrap_text=True),
        'num_fmt_curr': num_fmt_curr,
        'num_fmt_curr_dec': num_fmt_curr_dec,
        'num_fmt_pct': num_fmt_pct,
        'num_fmt_dec': num_fmt_dec,
        'num_fmt_int': num_fmt_int,
    }


def apply_sheet_protection(ws, allow_structure=True):
    """
    Aplica protección nativa con contraseña para blindar fórmulas y elementos visuales.
    En el estándar OpenXML (ECMA-376 / CT_SheetProtection):
      - sheet, objects, scenarios: True = blindado.
      - selectUnlockedCells, selectLockedCells, insertRows, formatCells, etc.:
        representan RESTRICCIONES.
        0 / False = NO restringido (permitido al usuario).
        1 / True  = restringido (bloqueado al usuario).
    """
    # 1. Asignar contraseña y activar blindaje general
    ws.protection.set_password(PASSWORD_PROTECT)
    ws.protection.sheet = True
    ws.protection.objects = True
    ws.protection.scenarios = True

    # 2. CLAVE: Poner en False para PERMITIR seleccionar y editar celdas desbloqueadas
    ws.protection.selectUnlockedCells = False  # Permite seleccionar y editar celdas desbloqueadas
    ws.protection.selectLockedCells = False    # Permite seleccionar celdas bloqueadas (solo lectura/copia)

    # 3. Permisos de estructura para permitir interacción fluida sin romper fórmulas
    if allow_structure:
        ws.protection.insertRows = False      # Permite insertar filas
        ws.protection.deleteRows = False      # Permite borrar filas
        ws.protection.formatCells = False     # Permite dar formato
        ws.protection.formatColumns = False   # Permite ajustar anchos de columna
        ws.protection.formatRows = False      # Permite ajustar altos de fila
        ws.protection.sort = False            # Permite ordenar tablas
        ws.protection.autoFilter = False      # Permite usar filtros desplegables


# ==============================================================================
# TAB 2: EVALUACIÓN MULTIFACTORIAL (MULTIEVALUATION)
# ==============================================================================
def build_tab2_assessment(wb, ws, lang='ES'):
    styles = get_base_styles(lang)
    sheet_name = "02_Evaluacion_Multifactorial" if lang == 'ES' else "02_Multifactor_Assessment"
    ws.title = sheet_name
    ws.views.sheetView[0].showGridLines = True

    # 1. Cabecera Corporativa (Locked)
    for cell_id, text, f_style in [
        ('B2', "DATALARIA | EXECUTIVE DECISION PACK", styles['font_title']),
        ('B3', "MATRIZ MCKINSEY / GE: EVALUACIÓN MULTIFACTORIAL DE CARTERA" if lang == 'ES' else "MCKINSEY / GE MATRIX: MULTIFACTOR PORTFOLIO ASSESSMENT", styles['font_subtitle']),
        ('B4', "Ponderación Cuantitativa y Calificación de Atractivo de Industria (Eje Y) vs. Fortaleza Competitiva (Eje X) • Escala 1.00 a 5.00" if lang == 'ES' else "Quantitative Weighting & Rating of Industry Attractiveness (Y-Axis) vs. Competitive Strength (X-Axis) • Scale 1.00 to 5.00", styles['font_meta'])
    ]:
        ws[cell_id] = text
        ws[cell_id].font = f_style
        ws[cell_id].protection = PROT_LOCKED

    # 2. SECCIÓN 1: ATRACTIVO DE LA INDUSTRIA (EJE Y)
    ws['B6'] = ("1. EVALUACIÓN DE ATRACTIVO DE LA INDUSTRIA (EJE Y)"
                if lang == 'ES' else
                "1. INDUSTRY ATTRACTIVENESS ASSESSMENT (Y-AXIS)")
    ws['B6'].font = styles['font_section']
    ws['B6'].protection = PROT_LOCKED

    headers_ind = [
        ("B7", "Cód" if lang == 'ES' else "Code"),
        ("C7", "Criterio de Atractivo del Sector" if lang == 'ES' else "Industry Attractiveness Criterion"),
        ("D7", "Métrica de Referencia y Fuente Guía" if lang == 'ES' else "Benchmark Metric & Data Source"),
        ("E7", "Peso %" if lang == 'ES' else "Weight %"),
    ]
    for c_idx in range(10):
        col_letter = get_column_letter(6 + c_idx)
        headers_ind.append((f"{col_letter}7", f"UEN-{c_idx+1:02d}"))

    for pos, text in headers_ind:
        cell = ws[pos]
        cell.value = text
        cell.font = styles['font_header']
        cell.fill = styles['fill_navy_hdr']
        cell.alignment = styles['align_center_wrap']
        cell.border = styles['header_border']
        cell.protection = PROT_LOCKED
    ws.row_dimensions[7].height = 28

    crit_ind_es = [
        ("IND-01", "Crecimiento del Mercado (% anual CAGR a 3-5 años)", "Tasa de crecimiento proyectada del sector objetivo", 0.25),
        ("IND-02", "Margen Operativo Medio del Sector (% EBITDA sectorial)", "Rentabilidad operativa agregada de competidores", 0.20),
        ("IND-03", "Barreras de Entrada e Intensidad Competitiva", "Inversión de entrada, concentración y poder de clientes", 0.20),
        ("IND-04", "Estabilidad Regulatoria, Legal y Medioambiental", "Seguridad jurídica, presiones normativas y compliance ESG", 0.15),
        ("IND-05", "Sensibilidad Macroeconómica y Resiliencia Cíclica", "Defensividad ante tipos de interés, inflación y ciclos", 0.20),
    ]
    crit_ind_en = [
        ("IND-01", "Market Growth Rate (% 3-5 yr CAGR)", "Projected expansion rate of addressable industry", 0.25),
        ("IND-02", "Industry Average Operating Margin (% EBITDA)", "Aggregate sector benchmark profitability", 0.20),
        ("IND-03", "Entry Barriers & Competitive Rivalry Intensity", "Capital requirements, supplier/buyer power, rivalry", 0.20),
        ("IND-04", "Regulatory, Legal & Environmental Stability", "Compliance requirements, policy predictability, ESG", 0.15),
        ("IND-05", "Macroeconomic Resilience & Cyclical Defense", "Insulation from interest rates, inflation, macro shocks", 0.20),
    ]
    crit_ind = crit_ind_es if lang == 'ES' else crit_ind_en

    sample_ind_scores = [
        [5.0, 4.8, 4.0, 3.5, 4.2, 2.2, 4.2, 2.8, 1.8, 1.4],
        [4.8, 4.9, 3.6, 3.2, 3.8, 2.5, 4.0, 2.6, 1.9, 1.5],
        [4.5, 4.8, 3.5, 3.0, 2.8, 2.8, 3.8, 2.5, 1.8, 1.6],
        [4.2, 3.8, 4.0, 3.5, 3.2, 2.5, 3.5, 3.0, 2.2, 2.0],
        [4.4, 4.5, 3.5, 3.2, 3.5, 2.2, 3.8, 2.4, 1.9, 1.5],
    ]

    for idx, (code, name, desc, w) in enumerate(crit_ind):
        row = 8 + idx
        # Código (Editable)
        c_code = ws[f'B{row}']
        c_code.value = code
        c_code.font = styles['font_bold']
        c_code.alignment = styles['align_center']
        c_code.fill = styles['fill_input']
        c_code.border = styles['thin_border']
        c_code.protection = PROT_UNLOCKED

        # Nombre Criterio (Editable)
        c_desc = ws[f'C{row}']
        c_desc.value = name
        c_desc.font = styles['font_bold']
        c_desc.alignment = styles['align_left']
        c_desc.fill = styles['fill_input']
        c_desc.border = styles['thin_border']
        c_desc.protection = PROT_UNLOCKED

        # Métrica Guía (Editable)
        c_metric = ws[f'D{row}']
        c_metric.value = desc
        c_metric.font = styles['font_regular']
        c_metric.alignment = styles['align_left']
        c_metric.fill = styles['fill_input']
        c_metric.border = styles['thin_border']
        c_metric.protection = PROT_UNLOCKED

        # Peso % (Editable)
        c_weight = ws[f'E{row}']
        c_weight.value = w
        c_weight.font = styles['font_bold']
        c_weight.alignment = styles['align_right']
        c_weight.number_format = styles['num_fmt_pct']
        c_weight.fill = styles['fill_input']
        c_weight.border = styles['input_border']
        c_weight.protection = PROT_UNLOCKED

        # Puntuaciones UENs (Editables)
        for u_idx in range(10):
            col_letter = get_column_letter(6 + u_idx)
            c_rating = ws[f'{col_letter}{row}']
            c_rating.value = sample_ind_scores[idx][u_idx]
            c_rating.font = styles['font_regular']
            c_rating.alignment = styles['align_center']
            c_rating.number_format = styles['num_fmt_dec']
            c_rating.fill = styles['fill_input']
            c_rating.border = styles['thin_border']
            c_rating.protection = PROT_UNLOCKED

    # Fila 13: Verificación de Suma de Pesos (Fórmula Bloqueada)
    for c in ['B', 'C', 'D']:
        ws[f'{c}13'].border = styles['total_border']
        ws[f'{c}13'].fill = styles['fill_total']
        ws[f'{c}13'].protection = PROT_LOCKED

    ws['C13'] = "CONTROL DE PONDERACIÓN (SUMA DEBE SER 100%)" if lang == 'ES' else "WEIGHTING AUDIT (SUM MUST BE 100%)"
    ws['C13'].font = styles['font_bold']
    ws['C13'].alignment = styles['align_right']

    c_sum1 = ws['E13']
    c_sum1.value = "=SUM(E8:E12)"
    c_sum1.font = styles['font_bold']
    c_sum1.alignment = styles['align_right']
    c_sum1.number_format = styles['num_fmt_pct']
    c_sum1.border = styles['total_border']
    c_sum1.fill = styles['fill_total']
    c_sum1.protection = PROT_LOCKED

    for u_idx in range(10):
        col_letter = get_column_letter(6 + u_idx)
        ws[f'{col_letter}13'].border = styles['total_border']
        ws[f'{col_letter}13'].fill = styles['fill_total']
        ws[f'{col_letter}13'].protection = PROT_LOCKED

    # Fila 14: Puntuación Consolidada Atractivo (Fórmulas Bloqueadas)
    for c in ['B', 'C', 'D', 'E']:
        ws[f'{c}14'].border = styles['total_border']
        ws[f'{c}14'].fill = styles['fill_calc']
        ws[f'{c}14'].protection = PROT_LOCKED

    ws['B14'] = "IA"
    ws['B14'].font = styles['font_bold']
    ws['B14'].alignment = styles['align_center']

    ws['C14'] = ("PUNTUACIÓN ATRACTIVO DE LA INDUSTRIA (ÍNDICE IA)"
                 if lang == 'ES' else
                 "INDUSTRY ATTRACTIVENESS SCORE (INDEX IA)")
    ws['C14'].font = styles['font_bold']
    ws['C14'].alignment = styles['align_left']

    ws['D14'] = ("Fórmula: =SUMAPRODUCTO(Pesos, Puntuaciones)"
                 if lang == 'ES' else
                 "Formula: =SUMPRODUCT(Weights, Scores)")
    ws['D14'].font = styles['font_meta']

    for u_idx in range(10):
        col_letter = get_column_letter(6 + u_idx)
        c_score = ws[f'{col_letter}14']
        c_score.value = f"=SUMPRODUCT($E$8:$E$12, {col_letter}8:{col_letter}12)"
        c_score.font = styles['font_bold']
        c_score.alignment = styles['align_center']
        c_score.number_format = styles['num_fmt_dec']
        c_score.border = styles['total_border']
        c_score.fill = styles['fill_calc']
        c_score.protection = PROT_LOCKED

    # Fila 15: Nivel de Atractivo (Fórmulas Bloqueadas)
    for c in ['B', 'C', 'D', 'E']:
        ws[f'{c}15'].border = styles['thin_border']
        ws[f'{c}15'].fill = styles['fill_calc']
        ws[f'{c}15'].protection = PROT_LOCKED

    ws['C15'] = ("Nivel de Atractivo Sectorial"
                 if lang == 'ES' else
                 "Industry Attractiveness Level")
    ws['C15'].font = styles['font_subhead']

    for u_idx in range(10):
        col_letter = get_column_letter(6 + u_idx)
        c_lvl = ws[f'{col_letter}15']
        if lang == 'ES':
            c_lvl.value = f'=IF({col_letter}14>=3.67, "Alto", IF({col_letter}14>=2.33, "Medio", "Bajo"))'
        else:
            c_lvl.value = f'=IF({col_letter}14>=3.67, "High", IF({col_letter}14>=2.33, "Medium", "Low"))'
        c_lvl.font = styles['font_badge']
        c_lvl.alignment = styles['align_center']
        c_lvl.border = styles['thin_border']
        c_lvl.fill = styles['fill_calc']
        c_lvl.protection = PROT_LOCKED

    # 3. SECCIÓN 2: FORTALEZA COMPETITIVA DE LA UEN (EJE X)
    ws['B17'] = ("2. EVALUACIÓN DE FORTALEZA COMPETITIVA DE LA UEN (EJE X)"
                 if lang == 'ES' else
                 "2. BUSINESS UNIT COMPETITIVE STRENGTH ASSESSMENT (X-AXIS)")
    ws['B17'].font = styles['font_section']
    ws['B17'].protection = PROT_LOCKED

    headers_str = [
        ("B18", "Cód" if lang == 'ES' else "Code"),
        ("C18", "Criterio de Fortaleza Competitiva" if lang == 'ES' else "Business Unit Strength Criterion"),
        ("D18", "Métrica de Referencia y Fuente Guía" if lang == 'ES' else "Benchmark Metric & Data Source"),
        ("E18", "Peso %" if lang == 'ES' else "Weight %"),
    ]
    for c_idx in range(10):
        col_letter = get_column_letter(6 + c_idx)
        headers_str.append((f"{col_letter}18", f"UEN-{c_idx+1:02d}"))

    for pos, text in headers_str:
        cell = ws[pos]
        cell.value = text
        cell.font = styles['font_header']
        cell.fill = styles['fill_navy_hdr']
        cell.alignment = styles['align_center_wrap']
        cell.border = styles['header_border']
        cell.protection = PROT_LOCKED
    ws.row_dimensions[18].height = 28

    crit_str_es = [
        ("STR-01", "Cuota de Mercado Relativa y Liderazgo (CMR vs líder)", "Facturación propia / Facturación líder directo", 0.25),
        ("STR-02", "Ventaja Tecnológica, Patentes y Propiedad Intelectual", "Propiedad de algoritmos, patentes activas y pipeline I+D", 0.20),
        ("STR-03", "Margen Bruto vs Competidores y Eficiencia Operativa", "Diferencial de margen bruto frente a media del sector", 0.20),
        ("STR-04", "Fuerza de Marca, Reputación y Red de Distribución", "NPS, fidelidad de clientes clave y capilaridad comercial", 0.15),
        ("STR-05", "Capacidad Financiera, Talento y Agilidad de Ejecución", "Generación de FCF, retención de talento y tiempo de ciclo", 0.20),
    ]
    crit_str_en = [
        ("STR-01", "Relative Market Share & Leadership (RMS vs leader)", "Own revenues divided by top competitor revenue", 0.25),
        ("STR-02", "Technological Edge, Patents & Proprietary IP", "Algorithmic IP, active patents, and R&D pipeline", 0.20),
        ("STR-03", "Gross Margin vs Peers & Cost Structure Advantage", "Gross margin premium vs industry benchmark average", 0.20),
        ("STR-04", "Brand Equity, Market Reputation & Channel Reach", "NPS score, key account retention, channel access", 0.15),
        ("STR-05", "Financial Strength, Talent & Execution Velocity", "FCF generation, critical talent retention, cycle time", 0.20),
    ]
    crit_str = crit_str_es if lang == 'ES' else crit_str_en

    sample_str_scores = [
        [4.5, 3.2, 4.6, 3.5, 2.2, 4.4, 1.8, 1.9, 2.8, 1.6],
        [5.0, 4.6, 4.2, 3.6, 3.5, 3.8, 2.2, 2.0, 2.2, 1.4],
        [4.7, 4.0, 3.8, 3.4, 2.8, 3.9, 2.0, 1.8, 2.4, 1.5],
        [4.2, 3.5, 4.0, 3.5, 2.4, 4.2, 1.8, 2.1, 2.6, 1.8],
        [4.6, 4.0, 4.2, 3.4, 3.0, 4.0, 2.2, 2.0, 2.5, 1.8],
    ]

    for idx, (code, name, desc, w) in enumerate(crit_str):
        row = 19 + idx
        c_code = ws[f'B{row}']
        c_code.value = code
        c_code.font = styles['font_bold']
        c_code.alignment = styles['align_center']
        c_code.fill = styles['fill_input']
        c_code.border = styles['thin_border']
        c_code.protection = PROT_UNLOCKED

        c_desc = ws[f'C{row}']
        c_desc.value = name
        c_desc.font = styles['font_bold']
        c_desc.alignment = styles['align_left']
        c_desc.fill = styles['fill_input']
        c_desc.border = styles['thin_border']
        c_desc.protection = PROT_UNLOCKED

        c_metric = ws[f'D{row}']
        c_metric.value = desc
        c_metric.font = styles['font_regular']
        c_metric.alignment = styles['align_left']
        c_metric.fill = styles['fill_input']
        c_metric.border = styles['thin_border']
        c_metric.protection = PROT_UNLOCKED

        c_weight = ws[f'E{row}']
        c_weight.value = w
        c_weight.font = styles['font_bold']
        c_weight.alignment = styles['align_right']
        c_weight.number_format = styles['num_fmt_pct']
        c_weight.fill = styles['fill_input']
        c_weight.border = styles['input_border']
        c_weight.protection = PROT_UNLOCKED

        for u_idx in range(10):
            col_letter = get_column_letter(6 + u_idx)
            c_rating = ws[f'{col_letter}{row}']
            c_rating.value = sample_str_scores[idx][u_idx]
            c_rating.font = styles['font_regular']
            c_rating.alignment = styles['align_center']
            c_rating.number_format = styles['num_fmt_dec']
            c_rating.fill = styles['fill_input']
            c_rating.border = styles['thin_border']
            c_rating.protection = PROT_UNLOCKED

    # Fila 24: Verificación de Suma de Pesos (Fórmula Bloqueada)
    for c in ['B', 'C', 'D']:
        ws[f'{c}24'].border = styles['total_border']
        ws[f'{c}24'].fill = styles['fill_total']
        ws[f'{c}24'].protection = PROT_LOCKED

    ws['C24'] = "CONTROL DE PONDERACIÓN (SUMA DEBE SER 100%)" if lang == 'ES' else "WEIGHTING AUDIT (SUM MUST BE 100%)"
    ws['C24'].font = styles['font_bold']
    ws['C24'].alignment = styles['align_right']

    c_sum2 = ws['E24']
    c_sum2.value = "=SUM(E19:E23)"
    c_sum2.font = styles['font_bold']
    c_sum2.alignment = styles['align_right']
    c_sum2.number_format = styles['num_fmt_pct']
    c_sum2.border = styles['total_border']
    c_sum2.fill = styles['fill_total']
    c_sum2.protection = PROT_LOCKED

    for u_idx in range(10):
        col_letter = get_column_letter(6 + u_idx)
        ws[f'{col_letter}24'].border = styles['total_border']
        ws[f'{col_letter}24'].fill = styles['fill_total']
        ws[f'{col_letter}24'].protection = PROT_LOCKED

    # Fila 25: Puntuación Consolidada Fortaleza (Fórmulas Bloqueadas)
    for c in ['B', 'C', 'D', 'E']:
        ws[f'{c}25'].border = styles['total_border']
        ws[f'{c}25'].fill = styles['fill_calc']
        ws[f'{c}25'].protection = PROT_LOCKED

    ws['B25'] = "FC"
    ws['B25'].font = styles['font_bold']
    ws['B25'].alignment = styles['align_center']

    ws['C25'] = ("PUNTUACIÓN FORTALEZA COMPETITIVA (ÍNDICE FC)"
                 if lang == 'ES' else
                 "BUSINESS UNIT STRENGTH SCORE (INDEX FC)")
    ws['C25'].font = styles['font_bold']
    ws['C25'].alignment = styles['align_left']

    ws['D25'] = ("Fórmula: =SUMAPRODUCTO(Pesos, Puntuaciones)"
                 if lang == 'ES' else
                 "Formula: =SUMPRODUCT(Weights, Scores)")
    ws['D25'].font = styles['font_meta']

    for u_idx in range(10):
        col_letter = get_column_letter(6 + u_idx)
        c_score = ws[f'{col_letter}25']
        c_score.value = f"=SUMPRODUCT($E$19:$E$23, {col_letter}19:{col_letter}23)"
        c_score.font = styles['font_bold']
        c_score.alignment = styles['align_center']
        c_score.number_format = styles['num_fmt_dec']
        c_score.border = styles['total_border']
        c_score.fill = styles['fill_calc']
        c_score.protection = PROT_LOCKED

    # Fila 26: Nivel de Fortaleza (Fórmulas Bloqueadas)
    for c in ['B', 'C', 'D', 'E']:
        ws[f'{c}26'].border = styles['thin_border']
        ws[f'{c}26'].fill = styles['fill_calc']
        ws[f'{c}26'].protection = PROT_LOCKED

    ws['C26'] = ("Nivel de Fortaleza Competitiva"
                 if lang == 'ES' else
                 "Competitive Strength Level")
    ws['C26'].font = styles['font_subhead']

    for u_idx in range(10):
        col_letter = get_column_letter(6 + u_idx)
        c_lvl = ws[f'{col_letter}26']
        if lang == 'ES':
            c_lvl.value = f'=IF({col_letter}25>=3.67, "Fuerte", IF({col_letter}25>=2.33, "Media", "Débil"))'
        else:
            c_lvl.value = f'=IF({col_letter}25>=3.67, "Strong", IF({col_letter}25>=2.33, "Medium", "Weak"))'
        c_lvl.font = styles['font_badge']
        c_lvl.alignment = styles['align_center']
        c_lvl.border = styles['thin_border']
        c_lvl.fill = styles['fill_calc']
        c_lvl.protection = PROT_LOCKED

    # 4. SECCIÓN 3: GUÍA DE PUNTUACIÓN Y AUDITORÍA (Bloqueada)
    ws['B28'] = ("3. RANGO DE CALIFICACIÓN Y UMBRALES DE FRONTERA CANÓNICOS"
                 if lang == 'ES' else
                 "3. RATING SCALE & CANONICAL BOUNDARY THRESHOLDS")
    ws['B28'].font = styles['font_section']
    ws['B28'].protection = PROT_LOCKED

    ranges_info = [
        ("B29:D29", "Rango Superior (Alto / Fuerte): 3.67 a 5.00" if lang == 'ES' else "Upper Tier (High / Strong): 3.67 to 5.00",
         "Liderazgo consolidado, alta expansión sectorial (>12% CAGR), barreras elevadas o tecnología puntera.",
         COLOR_GREEN_BG, COLOR_GREEN_TEXT),
        ("B30:D30", "Rango Medio (Medio / Media): 2.33 a 3.66" if lang == 'ES' else "Middle Tier (Medium / Medium): 2.33 to 3.66",
         "Crecimiento sectorial moderado (4-12%), cuota disputada, rentabilidad en línea con la media.",
         COLOR_AMBER_BG, COLOR_AMBER_TEXT),
        ("B31:D31", "Rango Inferior (Bajo / Débil): 1.00 a 2.32" if lang == 'ES' else "Lower Tier (Low / Weak): 1.00 to 2.32",
         "Madurez o estancamiento (<4%), comoditización severa, escala insuficiente frente al líder de mercado.",
         COLOR_RED_BG, COLOR_RED_TEXT),
    ]
    for r_range, r_title, r_desc, bg_color, txt_color in ranges_info:
        r_start = r_range.split(':')[0]
        ws.merge_cells(r_range)
        cell = ws[r_start]
        cell.value = f"{r_title} — {r_desc}"
        cell.font = Font(name='Segoe UI', size=8.5, bold=True, color=txt_color)
        cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type='solid')
        cell.alignment = styles['align_left']
        cell.border = styles['thin_border']
        cell.protection = PROT_LOCKED

    # Auto-ajuste de ancho de columnas
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 48
    ws.column_dimensions['D'].width = 40
    ws.column_dimensions['E'].width = 14
    for u_idx in range(10):
        col_letter = get_column_letter(6 + u_idx)
        ws.column_dimensions[col_letter].width = 13

    apply_sheet_protection(ws, allow_structure=True)


# ==============================================================================
# TAB 3: PLAN DE ASIGNACIÓN DE CAPITAL (CAPITAL ALLOCATION PLAN)
# ==============================================================================
def build_tab3_capital_plan(wb, ws, lang='ES'):
    styles = get_base_styles(lang)
    sheet_name = "03_Plan_Asignacion_Capital" if lang == 'ES' else "03_Capital_Allocation_Plan"
    ws.title = sheet_name
    ws.views.sheetView[0].showGridLines = True

    # 1. Cabecera Corporativa (Locked)
    for cell_id, text, f_style in [
        ('B2', "DATALARIA | EXECUTIVE DECISION PACK", styles['font_title']),
        ('B3', "PLAN ESTRATÉGICO DE ASIGNACIÓN DE CAPITAL & GOBERNANZA C-LEVEL" if lang == 'ES' else "STRATEGIC CAPITAL ALLOCATION PLAN & C-LEVEL GOVERNANCE", styles['font_subtitle']),
        ('B4', "Presupuesto de CAPEX a 36 Meses, Umbrales de Rentabilidad Mínima (Hurdle Rate / TIR) y Mandatos del Consejo de Administración" if lang == 'ES' else "36-Month CAPEX Budget, Hurdle Rates (IRR Thresholds), and Board of Directors Resolutions", styles['font_meta'])
    ]:
        ws[cell_id] = text
        ws[cell_id].font = f_style
        ws[cell_id].protection = PROT_LOCKED

    # 2. POLÍTICA DE ASIGNACIÓN DE CAPITAL (Locked)
    ws['B6'] = ("1. POLÍTICA DE ASIGNACIÓN DE CAPITAL POR ZONA ESTRATÉGICA (TARGET DEL CONSEJO)"
                if lang == 'ES' else
                "1. CORPORATE CAPITAL ALLOCATION POLICY BY STRATEGIC ZONE (BOARD TARGET)")
    ws['B6'].font = styles['font_section']
    ws['B6'].protection = PROT_LOCKED

    pol_headers = [
        ("B7", "Zona Estratégica" if lang == 'ES' else "Strategic Zone"),
        ("C7", "Mandato de Asignación de Capital" if lang == 'ES' else "Capital Allocation Mandate"),
        ("D7", "Rango Objetivo Política" if lang == 'ES' else "Target Policy Range"),
        ("E7", "CAPEX Propuesto (€)" if lang == 'ES' else "Proposed CAPEX ($)"),
        ("F7", "% Real Propuesto" if lang == 'ES' else "% Proposed Actual"),
        ("G7", "TIR Mínima (Hurdle Rate)" if lang == 'ES' else "Minimum Hurdle Rate (IRR)"),
        ("H7", "Dictamen de Cumplimiento" if lang == 'ES' else "Compliance Audit"),
    ]
    for pos, text in pol_headers:
        cell = ws[pos]
        cell.value = text
        cell.font = styles['font_header']
        cell.fill = styles['fill_navy_hdr']
        cell.alignment = styles['align_center_wrap']
        cell.border = styles['header_border']
        cell.protection = PROT_LOCKED
    ws.row_dimensions[7].height = 28

    dash_tab = "'01_Dashboard_Ejecutivo'" if lang == 'ES' else "'01_Executive_Dashboard'"

    pol_rows = [
        ("Invertir / Crecer" if lang == 'ES' else "Invest / Grow",
         "Máxima prioridad CAPEX, crecimiento orgánico, I+D puntero y M&A" if lang == 'ES' else "Top CAPEX priority, organic expansion, leading R&D, and bolt-on M&A",
         "65% - 75%",
         f"={dash_tab}!N12", f"=E8/$E$11", "18.0%",
         '=IF(F8>=0.60, "Conforme a Política", "Aviso: Inversión Insuficiente")' if lang == 'ES' else '=IF(F8>=0.60, "Policy Compliant", "Warning: Underinvested")',
         COLOR_GREEN_BG, COLOR_GREEN_TEXT),
        ("Seleccionar / Proteger" if lang == 'ES' else "Selectivity / Hold",
         "Inversión selectiva autofinanciada, foco en márgenes y nichos" if lang == 'ES' else "Self-funded selective investment, margin protection, and high-value niches",
         "20% - 30%",
         f"={dash_tab}!N15", f"=E9/$E$11", "14.0%",
         '=IF(AND(F9>=0.15, F9<=0.35), "Conforme a Política", "Aviso: Revisar Asignación")' if lang == 'ES' else '=IF(AND(F9>=0.15, F9<=0.35), "Policy Compliant", "Warning: Review Split")',
         COLOR_AMBER_BG, COLOR_AMBER_TEXT),
        ("Cosechar / Desinvertir" if lang == 'ES' else "Harvest / Divest",
         "Congelación de CAPEX no crítico, maximizar FCF residual y carve-out" if lang == 'ES' else "Freeze non-critical CAPEX, harvest residual FCF, and execute carve-out",
         "0% - 5%",
         f"={dash_tab}!N18", f"=E10/$E$11", "10.0%",
         '=IF(F10<=0.08, "Conforme a Política", "Aviso: Exceso de CAPEX en Cosecha")' if lang == 'ES' else '=IF(F10<=0.08, "Policy Compliant", "Warning: Excess CAPEX in Harvest")',
         COLOR_RED_BG, COLOR_RED_TEXT),
    ]

    for idx, (zone, mandate, target, formula_capex, formula_pct, hurdle, compliance, bg, txt) in enumerate(pol_rows):
        row = 8 + idx
        ws[f'B{row}'] = zone
        ws[f'B{row}'].font = Font(name='Segoe UI', size=9, bold=True, color=txt)
        ws[f'B{row}'].fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')
        ws[f'B{row}'].alignment = styles['align_center']
        ws[f'B{row}'].border = styles['thin_border']
        ws[f'B{row}'].protection = PROT_LOCKED

        for col_l, val, fnt, aln, nfmt in [
            ('C', mandate, styles['font_regular'], styles['align_left'], None),
            ('D', target, styles['font_bold'], styles['align_center'], None),
            ('E', formula_capex, styles['font_bold'], styles['align_right'], styles['num_fmt_curr']),
            ('F', formula_pct, styles['font_bold'], styles['align_right'], styles['num_fmt_pct']),
            ('G', hurdle, styles['font_bold'], styles['align_center'], None),
            ('H', compliance, styles['font_badge'], styles['align_center'], None),
        ]:
            cell = ws[f'{col_l}{row}']
            cell.value = val
            cell.font = fnt
            cell.alignment = aln
            if nfmt: cell.number_format = nfmt
            cell.border = styles['thin_border']
            cell.fill = styles['fill_calc']
            cell.protection = PROT_LOCKED

    # Fila 11: Totales Política (Locked)
    for c_let in ['B', 'C', 'D', 'E', 'F', 'G', 'H']:
        ws[f'{c_let}11'].border = styles['total_border']
        ws[f'{c_let}11'].fill = styles['fill_total']
        ws[f'{c_let}11'].protection = PROT_LOCKED

    ws['B11'] = "TOTAL CARTERA" if lang == 'ES' else "TOTAL PORTFOLIO"
    ws['B11'].font = styles['font_bold']

    ws['C11'] = "Presupuesto Consolidado de CAPEX a 36 Meses" if lang == 'ES' else "Consolidated 36-Month Capital Budget"
    ws['C11'].font = styles['font_meta']

    ws['D11'] = "100.0%"
    ws['D11'].font = styles['font_bold']
    ws['D11'].alignment = styles['align_center']

    ws['E11'] = "=SUM(E8:E10)"
    ws['E11'].font = styles['font_bold']
    ws['E11'].alignment = styles['align_right']
    ws['E11'].number_format = styles['num_fmt_curr']

    ws['F11'] = "=SUM(F8:F10)"
    ws['F11'].font = styles['font_bold']
    ws['F11'].alignment = styles['align_right']
    ws['F11'].number_format = styles['num_fmt_pct']

    ws['G11'] = "-"
    ws['G11'].alignment = styles['align_center']

    ws['H11'] = "VINCULANTE" if lang == 'ES' else "BINDING"
    ws['H11'].font = styles['font_bold']
    ws['H11'].alignment = styles['align_center']

    # 3. PLAN DE HITOS Y PRESUPUESTO POR UEN (FILAS 13 A 26)
    ws['B13'] = ("2. PLAN DE HITOS, PRESUPUESTO DE CAPEX (12-24-36 MESES) Y GOBERNANZA POR UEN"
                 if lang == 'ES' else
                 "2. MILESTONE ROADMAP, CAPEX BUDGET (12-24-36 MONTHS) & GOVERNANCE BY SBU")
    ws['B13'].font = styles['font_section']
    ws['B13'].protection = PROT_LOCKED

    plan_headers = [
        ("B14", "Cód" if lang == 'ES' else "Code"),
        ("C14", "Unidad Estratégica de Negocio (UEN)" if lang == 'ES' else "Strategic Business Unit (SBU)"),
        ("D14", "Zona Estratégica" if lang == 'ES' else "Strategic Zone"),
        ("E14", "Iniciativa Estratégica / Hito Clave" if lang == 'ES' else "Strategic Initiative / Key Milestone"),
        ("F14", "CAPEX 12M (€)" if lang == 'ES' else "CAPEX 12M ($)"),
        ("G14", "CAPEX 24M (€)" if lang == 'ES' else "CAPEX 24M ($)"),
        ("H14", "CAPEX 36M (€)" if lang == 'ES' else "CAPEX 36M ($)"),
        ("I14", "CAPEX Total 3A (€)" if lang == 'ES' else "Total 3Y CAPEX ($)"),
        ("J14", "TIR Mínima" if lang == 'ES' else "Hurdle Rate"),
        ("K14", "TIR Est. %" if lang == 'ES' else "Est. IRR %"),
        ("L14", "ROIC 3A %" if lang == 'ES' else "3Y ROIC %"),
        ("M14", "Dictamen Comité" if lang == 'ES' else "Committee Mandate"),
    ]
    for pos, text in plan_headers:
        cell = ws[pos]
        cell.value = text
        cell.font = styles['font_header']
        cell.fill = styles['fill_navy_hdr']
        cell.alignment = styles['align_center_wrap']
        cell.border = styles['header_border']
        cell.protection = PROT_LOCKED
    ws.row_dimensions[14].height = 28

    sbu_initiatives_es = [
        ("Escalado de plataforma GenAI industrial y M&A bolt-on", 9500000, 8000000, 6500000, 0.18, 0.285, 0.312, "Aprobado Vinculante"),
        ("Homologación FDA/CE robótica quirúrgica e I+D", 8000000, 6000000, 4500000, 0.18, 0.260, 0.284, "Aprobado Vinculante"),
        ("Nueva línea automatizada de electrónica de potencia", 7000000, 5000000, 4000000, 0.18, 0.225, 0.240, "Aprobado Vinculante"),
        ("Actualización IoT y sensores industriales estándar", 3000000, 2500000, 2000000, 0.14, 0.175, 0.190, "Aprobado Condicionado"),
        ("Plataforma SaaS telemetría y software flotas", 2000000, 1800000, 1500000, 0.14, 0.160, 0.178, "Aprobado Condicionado"),
        ("Mantenimiento de moldes y optimización térmica HVAC", 1800000, 1500000, 1200000, 0.14, 0.155, 0.165, "Aprobado Condicionado"),
        ("Especialización en aleaciones aeroespaciales de nicho", 2200000, 1500000, 1000000, 0.14, 0.150, 0.158, "Aprobado Condicionado"),
        ("Mantenimiento operativo mínimo; preparar carve-out", 600000, 400000, 200000, 0.10, 0.095, 0.102, "Congelado / Venta Q4"),
        ("Solo CAPEX regulatorio de seguridad; iniciar subasta", 500000, 300000, 0, 0.10, 0.080, 0.085, "Mandato de Carve-Out"),
        ("Cierre de línea analógica y liquidación de inventario", 200000, 0, 0, 0.10, 0.050, 0.055, "Liquidación Ordenada"),
    ]
    sbu_initiatives_en = [
        ("Industrial GenAI platform scaling & bolt-on M&A", 9500000, 8000000, 6500000, 0.18, 0.285, 0.312, "Binding Approval"),
        ("FDA/CE medical surgical robotics clinical trials & R&D", 8000000, 6000000, 4500000, 0.18, 0.260, 0.284, "Binding Approval"),
        ("Automated next-gen power electronics assembly line", 7000000, 5000000, 4000000, 0.18, 0.225, 0.240, "Binding Approval"),
        ("Smart factory sensor connectivity retrofit", 3000000, 2500000, 2000000, 0.14, 0.175, 0.190, "Conditional Approval"),
        ("Fleet telemetry SaaS platform modernization", 2000000, 1800000, 1500000, 0.14, 0.160, 0.178, "Conditional Approval"),
        ("HVAC precision tooling upkeep & thermal efficiency", 1800000, 1500000, 1200000, 0.14, 0.155, 0.165, "Conditional Approval"),
        ("Pivot to high-margin aerospace alloys niche", 2200000, 1500000, 1000000, 0.14, 0.150, 0.158, "Conditional Approval"),
        ("Maintenance only; prepare industrial carve-out", 600000, 400000, 200000, 0.10, 0.095, 0.102, "Frozen / Sale Q4"),
        ("Safety compliance only; launch divestment auction", 500000, 300000, 0, 0.10, 0.080, 0.085, "Carve-Out Mandate"),
        ("Analog switchboard phase-out & inventory liquidation", 200000, 0, 0, 0.10, 0.050, 0.055, "Orderly Liquidation"),
    ]
    sbu_initiatives = sbu_initiatives_es if lang == 'ES' else sbu_initiatives_en

    for idx, (init, c12, c24, c36, hurdle, irr, roic, mandate) in enumerate(sbu_initiatives):
        row = 15 + idx
        sbu_code = f"UEN-{idx+1:02d}"

        # Código (Locked)
        ws[f'B{row}'] = sbu_code
        ws[f'B{row}'].font = styles['font_bold']
        ws[f'B{row}'].alignment = styles['align_center']
        ws[f'B{row}'].border = styles['thin_border']
        ws[f'B{row}'].fill = styles['fill_calc']
        ws[f'B{row}'].protection = PROT_LOCKED

        # Nombre UEN vinculado a Tab 1 (Locked)
        ws[f'C{row}'] = f"={dash_tab}!C{30+idx}"
        ws[f'C{row}'].font = styles['font_bold']
        ws[f'C{row}'].alignment = styles['align_left']
        ws[f'C{row}'].border = styles['thin_border']
        ws[f'C{row}'].fill = styles['fill_calc']
        ws[f'C{row}'].protection = PROT_LOCKED

        # Zona vinculada a Tab 1 (Locked)
        ws[f'D{row}'] = f"={dash_tab}!I{30+idx}"
        ws[f'D{row}'].font = styles['font_badge']
        ws[f'D{row}'].alignment = styles['align_center']
        ws[f'D{row}'].border = styles['thin_border']
        ws[f'D{row}'].fill = styles['fill_calc']
        ws[f'D{row}'].protection = PROT_LOCKED

        # Iniciativa Estratégica (Editable)
        cell_init = ws[f'E{row}']
        cell_init.value = init
        cell_init.font = styles['font_regular']
        cell_init.alignment = styles['align_left']
        cell_init.fill = styles['fill_input']
        cell_init.border = styles['thin_border']
        cell_init.protection = PROT_UNLOCKED

        # CAPEX 12M, 24M, 36M (Editables)
        for col_off, c_val in [(0, c12), (1, c24), (2, c36)]:
            c_col = get_column_letter(6 + col_off)
            cell_c = ws[f'{c_col}{row}']
            cell_c.value = c_val
            cell_c.font = styles['font_regular']
            cell_c.alignment = styles['align_right']
            cell_c.number_format = styles['num_fmt_curr']
            cell_c.fill = styles['fill_input']
            cell_c.border = styles['thin_border']
            cell_c.protection = PROT_UNLOCKED

        # Total 3A = SUM(F:H) (Fórmula Bloqueada)
        cell_tot = ws[f'I{row}']
        cell_tot.value = f"=SUM(F{row}:H{row})"
        cell_tot.font = styles['font_bold']
        cell_tot.alignment = styles['align_right']
        cell_tot.number_format = styles['num_fmt_curr']
        cell_tot.border = styles['thin_border']
        cell_tot.fill = styles['fill_calc']
        cell_tot.protection = PROT_LOCKED

        # Hurdle Rate (Editable para calibrar según política)
        cell_h = ws[f'J{row}']
        cell_h.value = hurdle
        cell_h.font = styles['font_bold']
        cell_h.alignment = styles['align_center']
        cell_h.number_format = styles['num_fmt_pct']
        cell_h.fill = styles['fill_input']
        cell_h.border = styles['thin_border']
        cell_h.protection = PROT_UNLOCKED

        # TIR Proyectada (Editable)
        cell_irr = ws[f'K{row}']
        cell_irr.value = irr
        cell_irr.font = styles['font_bold']
        cell_irr.alignment = styles['align_center']
        cell_irr.number_format = styles['num_fmt_pct']
        cell_irr.fill = styles['fill_input']
        cell_irr.border = styles['thin_border']
        cell_irr.protection = PROT_UNLOCKED

        # ROIC Proyectado (Editable)
        cell_roic = ws[f'L{row}']
        cell_roic.value = roic
        cell_roic.font = styles['font_bold']
        cell_roic.alignment = styles['align_center']
        cell_roic.number_format = styles['num_fmt_pct']
        cell_roic.fill = styles['fill_input']
        cell_roic.border = styles['thin_border']
        cell_roic.protection = PROT_UNLOCKED

        # Dictamen Comité (Editable)
        cell_mand = ws[f'M{row}']
        cell_mand.value = mandate
        cell_mand.font = styles['font_badge']
        cell_mand.alignment = styles['align_center']
        cell_mand.fill = styles['fill_input']
        cell_mand.border = styles['thin_border']
        cell_mand.protection = PROT_UNLOCKED

    # Fila 25: Totales (Fórmulas Bloqueadas)
    for c_let in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
        ws[f'{c_let}25'].border = styles['total_border']
        ws[f'{c_let}25'].fill = styles['fill_total']
        ws[f'{c_let}25'].protection = PROT_LOCKED

    ws['B25'] = "TOTAL"
    ws['B25'].font = styles['font_bold']

    ws['C25'] = "Consolidado 10 UENs" if lang == 'ES' else "Consolidated 10 SBUs"
    ws['C25'].font = styles['font_bold']

    for c_off, c_let in [(0, 'F'), (1, 'G'), (2, 'H'), (3, 'I')]:
        ws[f'{c_let}25'] = f"=SUM({c_let}15:{c_let}24)"
        ws[f'{c_let}25'].font = styles['font_bold']
        ws[f'{c_let}25'].alignment = styles['align_right']
        ws[f'{c_let}25'].number_format = styles['num_fmt_curr']

    ws['J25'] = "-"
    ws['J25'].alignment = styles['align_center']

    ws['K25'] = "=AVERAGE(K15:K24)"
    ws['K25'].font = styles['font_bold']
    ws['K25'].alignment = styles['align_center']
    ws['K25'].number_format = styles['num_fmt_pct']

    ws['L25'] = "=AVERAGE(L15:L24)"
    ws['L25'].font = styles['font_bold']
    ws['L25'].alignment = styles['align_center']
    ws['L25'].number_format = styles['num_fmt_pct']

    ws['M25'] = "CONSENSO" if lang == 'ES' else "CONSENSUS"
    ws['M25'].font = styles['font_bold']
    ws['M25'].alignment = styles['align_center']

    # 4. REGLAS DE GOBERNANZA CORPORATIVA Y FIRMAS (Bloqueadas)
    ws['B27'] = ("3. REGLAS DE GOBERNANZA VINCULANTES DEL CONSEJO DE ADMINISTRACIÓN"
                 if lang == 'ES' else
                 "3. BINDING CORPORATE GOVERNANCE RULES OF THE BOARD OF DIRECTORS")
    ws['B27'].font = styles['font_section']
    ws['B27'].protection = PROT_LOCKED

    gov_rules_es = [
        "Regla 1 (Prioridad de Crecimiento): Solo las UENs en Zona Verde pueden optar a ampliaciones de capital, CAPEX expansivo o M&A.",
        "Regla 2 (Autofinanciación en Selectividad): Las UENs en Zona Ámbar deben autofinanciar sus programas de mejora mediante su propio EBITDA.",
        "Regla 3 (Desinversión en Cosecha): Queda prohibido cualquier CAPEX en UENs Rojas no requerido por normativa. Desinversión o carve-out en <12 meses."
    ]
    gov_rules_en = [
        "Rule 1 (Growth Priority): Only Green Zone SBUs are eligible for expansionary equity, corporate CAPEX, or strategic M&A.",
        "Rule 2 (Self-Funding in Selectivity): Amber Zone SBUs must self-fund all efficiency and niche enhancement programs via internal EBITDA.",
        "Rule 3 (Harvest Divestiture): Any non-regulatory CAPEX in Red Zone SBUs is strictly prohibited. Mandatory carve-out or sale within 12 months."
    ]
    gov_rules = gov_rules_es if lang == 'ES' else gov_rules_en

    for r_idx, rule_txt in enumerate(gov_rules):
        row = 28 + r_idx
        ws.merge_cells(f'B{row}:M{row}')
        cell = ws[f'B{row}']
        cell.value = f"• {rule_txt}"
        cell.font = styles['font_regular']
        cell.alignment = styles['align_left']
        cell.protection = PROT_LOCKED

    # Bloque de Firmas (Bloqueadas)
    ws['B33'] = "4. DICTAMEN FORMAL Y FIRMA DEL COMITÉ DE INVERSIÓN" if lang == 'ES' else "4. FORMAL INVESTMENT COMMITTEE SIGN-OFF"
    ws['B33'].font = styles['font_section']
    ws['B33'].protection = PROT_LOCKED

    sign_boxes = [
        ("B34:D36", "Presidente del Consejo de Administración" if lang == 'ES' else "Chairman of the Board of Directors",
         "[ APROBADO VINCULANTE ]" if lang == 'ES' else "[ BINDING APPROVAL ]"),
        ("E34:G36", "Consejero Delegado / CEO" if lang == 'ES' else "Chief Executive Officer / CEO",
         "[ CONFORME A ESTRATEGIA ]" if lang == 'ES' else "[ STRATEGY COMPLIANT ]"),
        ("H34:J36", "Director Financiero / CFO" if lang == 'ES' else "Chief Financial Officer / CFO",
         "[ VIABILIDAD FINANCIERA ]" if lang == 'ES' else "[ FINANCIALLY VALIDATED ]"),
        ("K34:M36", "Director de Estrategia / CSO" if lang == 'ES' else "Chief Strategy Officer / CSO",
         "[ ASIGNACIÓN MATRIZ GE ]" if lang == 'ES' else "[ GE MATRIX VALIDATED ]"),
    ]
    for s_range, s_title, s_status in sign_boxes:
        s_start = s_range.split(':')[0]
        ws.merge_cells(s_range)
        cell = ws[s_start]
        cell.value = f"{s_title}\n\n{s_status}\nFecha: 2026-10-27"
        cell.font = Font(name='Segoe UI', size=8.5, bold=True, color=COLOR_NAVY_DARK)
        cell.alignment = styles['align_center_wrap']
        cell.fill = styles['fill_card_bg']
        cell.border = styles['thin_border']
        cell.protection = PROT_LOCKED

    # Dimensiones
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 36
    ws.column_dimensions['D'].width = 24
    ws.column_dimensions['E'].width = 46
    ws.column_dimensions['F'].width = 18
    ws.column_dimensions['G'].width = 22
    ws.column_dimensions['H'].width = 24
    ws.column_dimensions['I'].width = 20
    ws.column_dimensions['J'].width = 15
    ws.column_dimensions['K'].width = 15
    ws.column_dimensions['L'].width = 15
    ws.column_dimensions['M'].width = 24

    apply_sheet_protection(ws, allow_structure=True)


# ==============================================================================
# TAB 1: DASHBOARD EJECUTIVO (EXECUTIVE DASHBOARD)
# ==============================================================================
def build_tab1_dashboard(wb, ws, lang='ES'):
    styles = get_base_styles(lang)
    sheet_name = "01_Dashboard_Ejecutivo" if lang == 'ES' else "01_Executive_Dashboard"
    ws.title = sheet_name
    ws.views.sheetView[0].showGridLines = True

    eval_tab = "'02_Evaluacion_Multifactorial'" if lang == 'ES' else "'02_Multifactor_Assessment'"
    cap_tab = "'03_Plan_Asignacion_Capital'" if lang == 'ES' else "'03_Capital_Allocation_Plan'"

    # 1. Cabecera C-Level (Locked)
    for cell_id, text, f_style in [
        ('B2', "DATALARIA | EXECUTIVE DECISION PACK", styles['font_title']),
        ('B3', "MATRIZ MCKINSEY / GE 3x3: ATRACTIVO DE LA INDUSTRIA VS. FORTALEZA COMPETITIVA" if lang == 'ES' else "MCKINSEY / GE 3x3 MATRIX: INDUSTRY ATTRACTIVENESS VS. BUSINESS UNIT STRENGTH", styles['font_subtitle']),
        ('B4', "Modelo Multifactorial de Diagnóstico de Cartera & Asignación de Capital • Grado Consejo de Administración • Versión 2026" if lang == 'ES' else "Multifactor Portfolio Diagnostics & Capital Allocation Model • Board of Directors Grade • 2026 Edition", styles['font_meta'])
    ]:
        ws[cell_id] = text
        ws[cell_id].font = f_style
        ws[cell_id].protection = PROT_LOCKED

    # 2. KPI Cards Ejecutivas (Locked)
    kpi_defs = [
        ("B6:C6", "B7:C8", "FACTURACIÓN TOTAL" if lang == 'ES' else "TOTAL REVENUE",
         "=D40", styles['num_fmt_curr']),
        ("D6:E6", "D7:E8", "EN ZONA INVERTIR (VERDE)" if lang == 'ES' else "IN INVEST ZONE (GREEN)",
         "=M12", styles['num_fmt_pct']),
        ("F6:G6", "F7:G8", "EN ZONA SELECTIVIDAD (ÁMBAR)" if lang == 'ES' else "IN SELECTIVITY ZONE (AMBER)",
         "=M15", styles['num_fmt_pct']),
        ("H6:I6", "H7:I8", "EN ZONA COSECHA (ROJO)" if lang == 'ES' else "IN HARVEST ZONE (RED)",
         "=M18", styles['num_fmt_pct']),
        ("J6:K6", "J7:K8", "CAPEX 3A TOTAL" if lang == 'ES' else "TOTAL 3Y CAPEX",
         "=K40", styles['num_fmt_curr']),
        ("L6:M6", "L7:M8", "ROIC MEDIO PROYECTADO" if lang == 'ES' else "PROJECTED AVG ROIC",
         f"={cap_tab}!L25", styles['num_fmt_pct']),
    ]

    for t_range, v_range, title, formula, fmt in kpi_defs:
        ws.merge_cells(t_range)
        ws.merge_cells(v_range)
        t_cell = ws[t_range.split(':')[0]]
        v_cell = ws[v_range.split(':')[0]]

        t_cell.value = title
        t_cell.font = styles['font_kpi_lbl']
        t_cell.alignment = styles['align_center']
        t_cell.fill = styles['fill_card_bg']
        t_cell.border = styles['thin_border']
        t_cell.protection = PROT_LOCKED

        v_cell.value = formula
        v_cell.font = styles['font_kpi_val']
        v_cell.alignment = styles['align_center']
        v_cell.fill = styles['fill_card_bg']
        v_cell.number_format = fmt
        v_cell.border = styles['thin_border']
        v_cell.protection = PROT_LOCKED

    # 3. CUADRÍCULA VISUAL MCKINSEY 3x3 Y TABLA DE ZONAS (Locked)
    ws['B10'] = ("1. CUADRÍCULA ESTRATÉGICA MCKINSEY / GENERAL ELECTRIC (9-BOX GRID)"
                 if lang == 'ES' else
                 "1. MCKINSEY / GENERAL ELECTRIC STRATEGIC 9-BOX GRID")
    ws['B10'].font = styles['font_section']
    ws['B10'].protection = PROT_LOCKED

    ws['K10'] = ("2. REPARTO DE CARTERA POR ZONA ESTRATÉGICA"
                 if lang == 'ES' else
                 "2. PORTFOLIO BREAKDOWN BY STRATEGIC ZONE")
    ws['K10'].font = styles['font_section']
    ws['K10'].protection = PROT_LOCKED

    # Cabeceras Eje X (Fortaleza Competitiva)
    grid_col_headers = [
        ("C11:D11", "FUERTE (3.67 - 5.00)" if lang == 'ES' else "STRONG (3.67 - 5.00)"),
        ("E11:F11", "MEDIA (2.33 - 3.66)" if lang == 'ES' else "MEDIUM (2.33 - 3.66)"),
        ("G11:H11", "DÉBIL (1.00 - 2.32)" if lang == 'ES' else "WEAK (1.00 - 2.32)"),
    ]
    for r_range, r_txt in grid_col_headers:
        ws.merge_cells(r_range)
        c = ws[r_range.split(':')[0]]
        c.value = r_txt
        c.font = styles['font_header']
        c.fill = styles['fill_navy_hdr']
        c.alignment = styles['align_center']
        c.border = styles['header_border']
        c.protection = PROT_LOCKED

    # Eje Y en Col B
    axis_y_headers = [
        ("B12:B15", "ALTO\n(3.67 - 5.00)" if lang == 'ES' else "HIGH\n(3.67 - 5.00)"),
        ("B16:B19", "MEDIO\n(2.33 - 3.66)" if lang == 'ES' else "MEDIUM\n(2.33 - 3.66)"),
        ("B20:B23", "BAJO\n(1.00 - 2.32)" if lang == 'ES' else "LOW\n(1.00 - 2.32)"),
    ]
    for r_range, r_txt in axis_y_headers:
        ws.merge_cells(r_range)
        c = ws[r_range.split(':')[0]]
        c.value = r_txt
        c.font = Font(name='Segoe UI', size=8.5, bold=True, color=COLOR_WHITE)
        c.fill = styles['fill_navy_sub']
        c.alignment = styles['align_center_wrap']
        c.border = styles['header_border']
        c.protection = PROT_LOCKED

    nine_boxes_es = [
        ("C12:D15", "INVERTIR PARA LIDERAR", "Zona Invertir / Crecer", "UEN-01 (Cloud IA)\nUEN-02 (Robótica Méd.)", COLOR_GREEN_BG, COLOR_GREEN_TEXT),
        ("E12:F15", "INVERTIR P/ DESARROLLAR", "Zona Invertir / Crecer", "UEN-03 (Electrónica Pot.)", COLOR_GREEN_BG, COLOR_GREEN_TEXT),
        ("G12:H15", "SELECTIVIDAD / DOBLAR O SALIR", "Zona Seleccionar", "UEN-07 (Mecanizado Prec.)", COLOR_AMBER_BG, COLOR_AMBER_TEXT),

        ("C16:D19", "CRECER SELECTIVAMENTE", "Zona Invertir / Crecer", "(Foco en Liderazgo)", COLOR_GREEN_BG, COLOR_GREEN_TEXT),
        ("E16:F19", "SELECTIVIDAD / RENTABILIZAR", "Zona Seleccionar", "UEN-04 (Smart Sensors)\nUEN-05 (Telemática)", COLOR_AMBER_BG, COLOR_AMBER_TEXT),
        ("G16:H19", "COSECHAR / REESTRUCTURAR", "Zona Cosechar / Desinvertir", "UEN-08 (Válvulas Hidr.)", COLOR_RED_BG, COLOR_RED_TEXT),

        ("C20:D23", "PROTEGER Y COSECHAR MARGEN", "Zona Seleccionar", "UEN-06 (HVAC Térmico)", COLOR_AMBER_BG, COLOR_AMBER_TEXT),
        ("E20:F23", "COSECHA CONTROLADA", "Zona Cosechar / Desinvertir", "UEN-09 (Cableado)", COLOR_RED_BG, COLOR_RED_TEXT),
        ("G20:H23", "DESINVERTIR / LIQUIDAR", "Zona Cosechar / Desinvertir", "UEN-10 (Medidores Analóg.)", COLOR_RED_BG, COLOR_RED_TEXT),
    ]

    nine_boxes_en = [
        ("C12:D15", "INVEST TO LEAD", "Invest / Grow Zone", "UEN-01 (Cloud AI)\nUEN-02 (Medical Robot.)", COLOR_GREEN_BG, COLOR_GREEN_TEXT),
        ("E12:F15", "INVEST TO BUILD", "Invest / Grow Zone", "UEN-03 (Power Electronics)", COLOR_GREEN_BG, COLOR_GREEN_TEXT),
        ("G12:H15", "SELECTIVITY / DOUBLE OR QUIT", "Selectivity Zone", "UEN-07 (Precision Alloys)", COLOR_AMBER_BG, COLOR_AMBER_TEXT),

        ("C16:D19", "SELECTIVITY / REINFORCE", "Invest / Grow Zone", "(Reinforce Leadership)", COLOR_GREEN_BG, COLOR_GREEN_TEXT),
        ("E16:F19", "SELECTIVITY / MAXIMIZE RETURN", "Selectivity Zone", "UEN-04 (Smart Sensors)\nUEN-05 (Fleet Telematics)", COLOR_AMBER_BG, COLOR_AMBER_TEXT),
        ("G16:H19", "HARVEST / RESTRUCTURE", "Harvest / Divest Zone", "UEN-08 (Hydraulic Valves)", COLOR_RED_BG, COLOR_RED_TEXT),

        ("C20:D23", "PROTECT & HARVEST CASH", "Selectivity Zone", "UEN-06 (HVAC Thermal)", COLOR_AMBER_BG, COLOR_AMBER_TEXT),
        ("E20:F23", "CONTROLLED HARVEST", "Harvest / Divest Zone", "UEN-09 (Commodity Wiring)", COLOR_RED_BG, COLOR_RED_TEXT),
        ("G20:H23", "DIVEST / DIVESTITURE", "Harvest / Divest Zone", "UEN-10 (Analog Meters)", COLOR_RED_BG, COLOR_RED_TEXT),
    ]

    nine_boxes = nine_boxes_es if lang == 'ES' else nine_boxes_en

    for b_range, b_title, b_zone, b_uens, bg_col, txt_col in nine_boxes:
        ws.merge_cells(b_range)
        start_cell = ws[b_range.split(':')[0]]
        start_cell.value = f"{b_title}\n[{b_zone}]\n{b_uens}"
        start_cell.font = Font(name='Segoe UI', size=8, bold=True, color=txt_col)
        start_cell.fill = PatternFill(start_color=bg_col, end_color=bg_col, fill_type='solid')
        start_cell.alignment = styles['align_center_wrap']
        start_cell.border = styles['thin_border']
        start_cell.protection = PROT_LOCKED

    # Etiqueta horizontal Eje X (Locked)
    ws.merge_cells("C24:H24")
    cell_x_lbl = ws["C24"]
    cell_x_lbl.value = ("EJE X: FORTALEZA COMPETITIVA DE LA UEN (Fuerte: 3.67-5.00 | Media: 2.33-3.66 | Débil: 1.00-2.32)"
                        if lang == 'ES' else
                        "X-AXIS: BUSINESS UNIT COMPETITIVE STRENGTH (Strong: 3.67-5.00 | Medium: 2.33-3.66 | Weak: 1.00-2.32)")
    cell_x_lbl.font = Font(name='Segoe UI', size=8, bold=True, color=COLOR_NAVY_DARK)
    cell_x_lbl.alignment = styles['align_center']
    cell_x_lbl.protection = PROT_LOCKED

    # Tabla Resumen de Zonas (Cols K a N, Filas 11 a 23) (Locked)
    zone_headers = [
        ("K11", "Zona Estratégica" if lang == 'ES' else "Strategic Zone"),
        ("L11", "Facturación (€)" if lang == 'ES' else "Revenue ($)"),
        ("M11", "% Ventas" if lang == 'ES' else "% Sales"),
        ("N11", "CAPEX 3A (€)" if lang == 'ES' else "3Y CAPEX ($)"),
    ]
    for pos, text in zone_headers:
        cell = ws[pos]
        cell.value = text
        cell.font = styles['font_header']
        cell.fill = styles['fill_navy_hdr']
        cell.alignment = styles['align_center_wrap']
        cell.border = styles['header_border']
        cell.protection = PROT_LOCKED
    ws.row_dimensions[11].height = 28

    # Fila 12-14: Invertir / Crecer
    ws.merge_cells("K12:K14")
    c_z1 = ws["K12"]
    c_z1.value = "INVERTIR / CRECER\n(Verde / Invest & Grow)" if lang == 'ES' else "INVEST / GROW\n(Green Zone)"
    c_z1.font = Font(name='Segoe UI', size=8.5, bold=True, color=COLOR_GREEN_TEXT)
    c_z1.fill = styles['fill_green_zone']
    c_z1.alignment = styles['align_center_wrap']
    c_z1.border = styles['thin_border']
    c_z1.protection = PROT_LOCKED

    ws.merge_cells("L12:L14")
    c_v1 = ws["L12"]
    c_v1.value = '=SUMIF($I$30:$I$39, "Invertir / Crecer", $D$30:$D$39)' if lang == 'ES' else '=SUMIF($I$30:$I$39, "Invest / Grow", $D$30:$D$39)'
    c_v1.font = styles['font_bold']
    c_v1.alignment = styles['align_right']
    c_v1.number_format = styles['num_fmt_curr']
    c_v1.border = styles['thin_border']
    c_v1.fill = styles['fill_calc']
    c_v1.protection = PROT_LOCKED

    ws.merge_cells("M12:M14")
    c_p1 = ws["M12"]
    c_p1.value = "=L12/$D$40"
    c_p1.font = styles['font_bold']
    c_p1.alignment = styles['align_right']
    c_p1.number_format = styles['num_fmt_pct']
    c_p1.border = styles['thin_border']
    c_p1.fill = styles['fill_calc']
    c_p1.protection = PROT_LOCKED

    ws.merge_cells("N12:N14")
    c_c1 = ws["N12"]
    c_c1.value = '=SUMIF($I$30:$I$39, "Invertir / Crecer", $K$30:$K$39)' if lang == 'ES' else '=SUMIF($I$30:$I$39, "Invest / Grow", $K$30:$K$39)'
    c_c1.font = styles['font_bold']
    c_c1.alignment = styles['align_right']
    c_c1.number_format = styles['num_fmt_curr']
    c_c1.border = styles['thin_border']
    c_c1.fill = styles['fill_calc']
    c_c1.protection = PROT_LOCKED

    # Fila 15-17: Seleccionar / Proteger
    ws.merge_cells("K15:K17")
    c_z2 = ws["K15"]
    c_z2.value = "SELECCIONAR / PROTEGER\n(Ámbar / Hold)" if lang == 'ES' else "SELECTIVITY / HOLD\n(Amber Zone)"
    c_z2.font = Font(name='Segoe UI', size=8.5, bold=True, color=COLOR_AMBER_TEXT)
    c_z2.fill = styles['fill_amber_zone']
    c_z2.alignment = styles['align_center_wrap']
    c_z2.border = styles['thin_border']
    c_z2.protection = PROT_LOCKED

    ws.merge_cells("L15:L17")
    c_v2 = ws["L15"]
    c_v2.value = '=SUMIF($I$30:$I$39, "Seleccionar / Proteger", $D$30:$D$39)' if lang == 'ES' else '=SUMIF($I$30:$I$39, "Selectivity / Hold", $D$30:$D$39)'
    c_v2.font = styles['font_bold']
    c_v2.alignment = styles['align_right']
    c_v2.number_format = styles['num_fmt_curr']
    c_v2.border = styles['thin_border']
    c_v2.fill = styles['fill_calc']
    c_v2.protection = PROT_LOCKED

    ws.merge_cells("M15:M17")
    c_p2 = ws["M15"]
    c_p2.value = "=L15/$D$40"
    c_p2.font = styles['font_bold']
    c_p2.alignment = styles['align_right']
    c_p2.number_format = styles['num_fmt_pct']
    c_p2.border = styles['thin_border']
    c_p2.fill = styles['fill_calc']
    c_p2.protection = PROT_LOCKED

    ws.merge_cells("N15:N17")
    c_c2 = ws["N15"]
    c_c2.value = '=SUMIF($I$30:$I$39, "Seleccionar / Proteger", $K$30:$K$39)' if lang == 'ES' else '=SUMIF($I$30:$I$39, "Selectivity / Hold", $K$30:$K$39)'
    c_c2.font = styles['font_bold']
    c_c2.alignment = styles['align_right']
    c_c2.number_format = styles['num_fmt_curr']
    c_c2.border = styles['thin_border']
    c_c2.fill = styles['fill_calc']
    c_c2.protection = PROT_LOCKED

    # Fila 18-20: Cosechar / Desinvertir
    ws.merge_cells("K18:K20")
    c_z3 = ws["K18"]
    c_z3.value = "COSECHAR / DESINVERTIR\n(Rojo / Divest)" if lang == 'ES' else "HARVEST / DIVEST\n(Red Zone)"
    c_z3.font = Font(name='Segoe UI', size=8.5, bold=True, color=COLOR_RED_TEXT)
    c_z3.fill = styles['fill_red_zone']
    c_z3.alignment = styles['align_center_wrap']
    c_z3.border = styles['thin_border']
    c_z3.protection = PROT_LOCKED

    ws.merge_cells("L18:L20")
    c_v3 = ws["L18"]
    c_v3.value = '=SUMIF($I$30:$I$39, "Cosechar / Desinvertir", $D$30:$D$39)' if lang == 'ES' else '=SUMIF($I$30:$I$39, "Harvest / Divest", $D$30:$D$39)'
    c_v3.font = styles['font_bold']
    c_v3.alignment = styles['align_right']
    c_v3.number_format = styles['num_fmt_curr']
    c_v3.border = styles['thin_border']
    c_v3.fill = styles['fill_calc']
    c_v3.protection = PROT_LOCKED

    ws.merge_cells("M18:M20")
    c_p3 = ws["M18"]
    c_p3.value = "=L18/$D$40"
    c_p3.font = styles['font_bold']
    c_p3.alignment = styles['align_right']
    c_p3.number_format = styles['num_fmt_pct']
    c_p3.border = styles['thin_border']
    c_p3.fill = styles['fill_calc']
    c_p3.protection = PROT_LOCKED

    ws.merge_cells("N18:N20")
    c_c3 = ws["N18"]
    c_c3.value = '=SUMIF($I$30:$I$39, "Cosechar / Desinvertir", $K$30:$K$39)' if lang == 'ES' else '=SUMIF($I$30:$I$39, "Harvest / Divest", $K$30:$K$39)'
    c_c3.font = styles['font_bold']
    c_c3.alignment = styles['align_right']
    c_c3.number_format = styles['num_fmt_curr']
    c_c3.border = styles['thin_border']
    c_c3.fill = styles['fill_calc']
    c_c3.protection = PROT_LOCKED

    # Fila 21-22: Total Zonas
    for c_zcol in ["K", "L", "M", "N"]:
        for r_z in [21, 22]:
            ws[f'{c_zcol}{r_z}'].border = styles['total_border']
            ws[f'{c_zcol}{r_z}'].fill = styles['fill_total']
            ws[f'{c_zcol}{r_z}'].protection = PROT_LOCKED

    ws.merge_cells("K21:K22")
    c_zt = ws["K21"]
    c_zt.value = "TOTAL CARTERA" if lang == 'ES' else "TOTAL PORTFOLIO"
    c_zt.font = styles['font_bold']
    c_zt.alignment = styles['align_center']

    ws.merge_cells("L21:L22")
    c_vt = ws["L21"]
    c_vt.value = "=SUM(L12,L15,L18)"
    c_vt.font = styles['font_bold']
    c_vt.alignment = styles['align_right']
    c_vt.number_format = styles['num_fmt_curr']

    ws.merge_cells("M21:M22")
    c_pt = ws["M21"]
    c_pt.value = "=SUM(M12,M15,M18)"
    c_pt.font = styles['font_bold']
    c_pt.alignment = styles['align_right']
    c_pt.number_format = styles['num_fmt_pct']

    ws.merge_cells("N21:N22")
    c_ct = ws["N21"]
    c_ct.value = "=SUM(N12,N15,N18)"
    c_ct.font = styles['font_bold']
    c_ct.alignment = styles['align_right']
    c_ct.number_format = styles['num_fmt_curr']

    # 4. TABLA RESUMEN DE CARTERA DE UENS (FILAS 28 A 40)
    ws['B27'] = ("3. TABLA RESUMEN DE CARTERA DE UNIDADES ESTRATÉGICAS DE NEGOCIO (UENS)"
                 if lang == 'ES' else
                 "3. STRATEGIC BUSINESS UNITS (SBUS) PORTFOLIO MASTER TABLE")
    ws['B27'].font = styles['font_section']
    ws['B27'].protection = PROT_LOCKED

    sbu_table_headers = [
        ("B28", "Cód" if lang == 'ES' else "Code"),
        ("C28", "Nombre de la UEN" if lang == 'ES' else "Business Unit Name"),
        ("D28", "Facturación (€)" if lang == 'ES' else "Revenue ($)"),
        ("E28", "Margen %" if lang == 'ES' else "EBITDA %"),
        ("F28", "Atractivo (IA)" if lang == 'ES' else "Attractiveness (IA)"),
        ("G28", "Fortaleza (FC)" if lang == 'ES' else "Strength (FC)"),
        ("H28", "Cuadrante Asignado" if lang == 'ES' else "Assigned Quadrant"),
        ("I28", "Zona Estratégica" if lang == 'ES' else "Strategic Zone"),
        ("J28", "Prioridad CAPEX" if lang == 'ES' else "CAPEX Priority"),
        ("K28", "CAPEX 3A (€)" if lang == 'ES' else "3Y CAPEX ($)"),
        ("L28", "% CAPEX" if lang == 'ES' else "% CAPEX"),
        ("M28", "Dictamen Consejo" if lang == 'ES' else "Board Resolution"),
    ]
    for pos, text in sbu_table_headers:
        cell = ws[pos]
        cell.value = text
        cell.font = styles['font_header']
        cell.fill = styles['fill_navy_hdr']
        cell.alignment = styles['align_center_wrap']
        cell.border = styles['header_border']
        cell.protection = PROT_LOCKED
    ws.row_dimensions[28].height = 28

    sample_sbus_es = [
        ("UEN-01", "Plataformas Cloud e IA Industrial", 95000000, 0.285),
        ("UEN-02", "Robótica Médica y Quirúrgica", 72000000, 0.240),
        ("UEN-03", "Electrónica de Potencia e Inversores", 110000000, 0.182),
        ("UEN-04", "Automatización y Sensores Industriales", 68000000, 0.165),
        ("UEN-05", "Telemática y Conectividad de Flotas", 35000000, 0.140),
        ("UEN-06", "Climatización HVAC y Sistemas Térmicos", 42000000, 0.150),
        ("UEN-07", "Mecanizado y Fundición de Precisión", 25000000, 0.110),
        ("UEN-08", "Válvulas Hidráulicas Maquinaria Pesada", 18000000, 0.085),
        ("UEN-09", "Cableado y Conectores Estándar", 12000000, 0.060),
        ("UEN-10", "Cuadros Eléctricos y Medidores Analógicos", 8000000, 0.032),
    ]
    sample_sbus_en = [
        ("UEN-01", "Industrial AI & Cloud Platforms", 95000000, 0.285),
        ("UEN-02", "Surgical & Medical Robotics", 72000000, 0.240),
        ("UEN-03", "Power Electronics & Inverters", 110000000, 0.182),
        ("UEN-04", "Smart Factory Automation & Sensors", 68000000, 0.165),
        ("UEN-05", "Fleet Telematics & IoT Solutions", 35000000, 0.140),
        ("UEN-06", "HVAC & Commercial Thermal Systems", 42000000, 0.150),
        ("UEN-07", "Precision Machining & Aerospace Alloys", 25000000, 0.110),
        ("UEN-08", "Heavy Machinery Hydraulic Valves", 18000000, 0.085),
        ("UEN-09", "Commodity Wiring & Industrial Cabling", 12000000, 0.060),
        ("UEN-10", "Analog Switchboards & Legacy Meters", 8000000, 0.032),
    ]
    sample_sbus = sample_sbus_es if lang == 'ES' else sample_sbus_en

    for idx, (code, name, sales, ebitda) in enumerate(sample_sbus):
        row = 30 + idx
        u_col = get_column_letter(6 + idx)  # Col F a O en Tab 2

        # Código UEN (Editable para código corporativo propio)
        c_code = ws[f'B{row}']
        c_code.value = code
        c_code.font = styles['font_bold']
        c_code.alignment = styles['align_center']
        c_code.fill = styles['fill_input']
        c_code.border = styles['thin_border']
        c_code.protection = PROT_UNLOCKED

        # Nombre UEN (Editable)
        c_name = ws[f'C{row}']
        c_name.value = name
        c_name.font = styles['font_bold']
        c_name.alignment = styles['align_left']
        c_name.fill = styles['fill_input']
        c_name.border = styles['input_border']
        c_name.protection = PROT_UNLOCKED

        # Facturación Anual (Editable)
        c_sales = ws[f'D{row}']
        c_sales.value = sales
        c_sales.font = styles['font_regular']
        c_sales.alignment = styles['align_right']
        c_sales.number_format = styles['num_fmt_curr']
        c_sales.fill = styles['fill_input']
        c_sales.border = styles['thin_border']
        c_sales.protection = PROT_UNLOCKED

        # Margen EBITDA (Editable)
        c_ebitda = ws[f'E{row}']
        c_ebitda.value = ebitda
        c_ebitda.font = styles['font_regular']
        c_ebitda.alignment = styles['align_right']
        c_ebitda.number_format = styles['num_fmt_pct']
        c_ebitda.fill = styles['fill_input']
        c_ebitda.border = styles['thin_border']
        c_ebitda.protection = PROT_UNLOCKED

        # Atractivo (Fórmula Bloqueada vinculada a Tab 2)
        c_ia = ws[f'F{row}']
        c_ia.value = f"={eval_tab}!{u_col}14"
        c_ia.font = styles['font_bold']
        c_ia.alignment = styles['align_center']
        c_ia.number_format = styles['num_fmt_dec']
        c_ia.border = styles['thin_border']
        c_ia.fill = styles['fill_calc']
        c_ia.protection = PROT_LOCKED

        # Fortaleza (Fórmula Bloqueada vinculada a Tab 2)
        c_fc = ws[f'G{row}']
        c_fc.value = f"={eval_tab}!{u_col}25"
        c_fc.font = styles['font_bold']
        c_fc.alignment = styles['align_center']
        c_fc.number_format = styles['num_fmt_dec']
        c_fc.border = styles['thin_border']
        c_fc.fill = styles['fill_calc']
        c_fc.protection = PROT_LOCKED

        # Cuadrante Asignado (Fórmula Bloqueada)
        c_quad = ws[f'H{row}']
        if lang == 'ES':
            c_quad.value = (
                f'=IF(F{row}>=3.67, '
                f'IF(G{row}>=3.67, "Invertir para Liderar", IF(G{row}>=2.33, "Invertir para Desarrollar", "Selectividad / Doblar o Salir")), '
                f'IF(F{row}>=2.33, '
                f'IF(G{row}>=3.67, "Crecer Selectivamente", IF(G{row}>=2.33, "Selectividad / Rentabilizar", "Cosechar / Reestructurar")), '
                f'IF(G{row}>=3.67, "Proteger y Cosechar Margen", IF(G{row}>=2.33, "Cosecha Controlada", "Desinvertir / Liquidar"))))'
            )
        else:
            c_quad.value = (
                f'=IF(F{row}>=3.67, '
                f'IF(G{row}>=3.67, "Invest to Lead", IF(G{row}>=2.33, "Invest to Build", "Selectivity / Double or Quit")), '
                f'IF(F{row}>=2.33, '
                f'IF(G{row}>=3.67, "Selectivity / Reinforce", IF(G{row}>=2.33, "Selectivity / Maximize Return", "Harvest / Restructure")), '
                f'IF(G{row}>=3.67, "Protect & Harvest Cash", IF(G{row}>=2.33, "Controlled Harvest", "Divest / Divestiture"))))'
            )
        c_quad.font = styles['font_bold']
        c_quad.alignment = styles['align_left']
        c_quad.border = styles['thin_border']
        c_quad.fill = styles['fill_calc']
        c_quad.protection = PROT_LOCKED

        # Zona Estratégica (Fórmula Bloqueada)
        c_zone = ws[f'I{row}']
        if lang == 'ES':
            c_zone.value = (
                f'=IF(OR(H{row}="Invertir para Liderar", H{row}="Invertir para Desarrollar", H{row}="Crecer Selectivamente"), "Invertir / Crecer", '
                f'IF(OR(H{row}="Selectividad / Doblar o Salir", H{row}="Selectividad / Rentabilizar", H{row}="Proteger y Cosechar Margen"), "Seleccionar / Proteger", "Cosechar / Desinvertir"))'
            )
        else:
            c_zone.value = (
                f'=IF(OR(H{row}="Invest to Lead", H{row}="Invest to Build", H{row}="Selectivity / Reinforce"), "Invest / Grow", '
                f'IF(OR(H{row}="Selectivity / Double or Quit", H{row}="Selectivity / Maximize Return", H{row}="Protect & Harvest Cash"), "Selectivity / Hold", "Harvest / Divest"))'
            )
        c_zone.font = styles['font_badge']
        c_zone.alignment = styles['align_center']
        c_zone.border = styles['thin_border']
        c_zone.fill = styles['fill_calc']
        c_zone.protection = PROT_LOCKED

        # Prioridad CAPEX (Fórmula Bloqueada)
        c_prio = ws[f'J{row}']
        if lang == 'ES':
            c_prio.value = f'=IF(I{row}="Invertir / Crecer", "Alta (Prioritaria)", IF(I{row}="Seleccionar / Proteger", "Media (Selectiva)", "Nula (Cosecha/Salida)"))'
        else:
            c_prio.value = f'=IF(I{row}="Invest / Grow", "High (Priority)", IF(I{row}="Selectivity / Hold", "Medium (Selective)", "Zero (Harvest/Exit)"))'
        c_prio.font = styles['font_badge']
        c_prio.alignment = styles['align_center']
        c_prio.border = styles['thin_border']
        c_prio.fill = styles['fill_calc']
        c_prio.protection = PROT_LOCKED

        # CAPEX 3A (Fórmula Bloqueada vinculada a Tab 3)
        c_cap = ws[f'K{row}']
        c_cap.value = f"={cap_tab}!I{15+idx}"
        c_cap.font = styles['font_bold']
        c_cap.alignment = styles['align_right']
        c_cap.number_format = styles['num_fmt_curr']
        c_cap.border = styles['thin_border']
        c_cap.fill = styles['fill_calc']
        c_cap.protection = PROT_LOCKED

        # % CAPEX Corporativo (Fórmula Bloqueada)
        c_cpct = ws[f'L{row}']
        c_cpct.value = f"=K{row}/$K$40"
        c_cpct.font = styles['font_bold']
        c_cpct.alignment = styles['align_right']
        c_cpct.number_format = styles['num_fmt_pct']
        c_cpct.border = styles['thin_border']
        c_cpct.fill = styles['fill_calc']
        c_cpct.protection = PROT_LOCKED

        # Dictamen Consejo (Fórmula Bloqueada vinculada a Tab 3)
        c_dec = ws[f'M{row}']
        c_dec.value = f"={cap_tab}!M{15+idx}"
        c_dec.font = styles['font_regular']
        c_dec.alignment = styles['align_center']
        c_dec.border = styles['thin_border']
        c_dec.fill = styles['fill_calc']
        c_dec.protection = PROT_LOCKED

    # Fila 40: Totales de la Cartera (Fórmulas Bloqueadas)
    for c_tot_l in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
        ws[f'{c_tot_l}40'].border = styles['total_border']
        ws[f'{c_tot_l}40'].fill = styles['fill_total']
        ws[f'{c_tot_l}40'].protection = PROT_LOCKED

    ws['B40'] = "TOTAL"
    ws['B40'].font = styles['font_bold']

    ws['C40'] = "Cartera Consolidada (10 UENs)" if lang == 'ES' else "Consolidated Portfolio (10 SBUs)"
    ws['C40'].font = styles['font_bold']

    ws['D40'] = "=SUM(D30:D39)"
    ws['D40'].font = styles['font_bold']
    ws['D40'].alignment = styles['align_right']
    ws['D40'].number_format = styles['num_fmt_curr']

    ws['E40'] = "=SUMPRODUCT(D30:D39, E30:E39)/D40"
    ws['E40'].font = styles['font_bold']
    ws['E40'].alignment = styles['align_right']
    ws['E40'].number_format = styles['num_fmt_pct']

    ws['F40'] = "=AVERAGE(F30:F39)"
    ws['F40'].font = styles['font_bold']
    ws['F40'].alignment = styles['align_center']
    ws['F40'].number_format = styles['num_fmt_dec']

    ws['G40'] = "=AVERAGE(G30:G39)"
    ws['G40'].font = styles['font_bold']
    ws['G40'].alignment = styles['align_center']
    ws['G40'].number_format = styles['num_fmt_dec']

    ws['K40'] = "=SUM(K30:K39)"
    ws['K40'].font = styles['font_bold']
    ws['K40'].alignment = styles['align_right']
    ws['K40'].number_format = styles['num_fmt_curr']

    ws['L40'] = "=SUM(L30:L39)"
    ws['L40'].font = styles['font_bold']
    ws['L40'].alignment = styles['align_right']
    ws['L40'].number_format = styles['num_fmt_pct']

    ws['M40'] = "AUDITADO" if lang == 'ES' else "AUDITED"
    ws['M40'].font = styles['font_bold']
    ws['M40'].alignment = styles['align_center']

    # Dimensiones
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 32
    ws.column_dimensions['D'].width = 18
    ws.column_dimensions['E'].width = 13
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 15
    ws.column_dimensions['H'].width = 26
    ws.column_dimensions['I'].width = 22
    ws.column_dimensions['J'].width = 18
    ws.column_dimensions['K'].width = 18
    ws.column_dimensions['L'].width = 15
    ws.column_dimensions['M'].width = 24
    ws.column_dimensions['N'].width = 18

    apply_sheet_protection(ws, allow_structure=True)


def generate_workbook(lang='ES', out_path=None):
    if out_path is None:
        fname = "ES_Matriz_McKinsey_GE_Datalaria.xlsx" if lang == 'ES' else "EN_McKinsey_GE_Matrix_Datalaria.xlsx"
        out_path = os.path.join(DIR_PACKAGES, fname)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb = openpyxl.Workbook()

    default_sheet = wb.active

    ws_dash = wb.create_sheet()
    ws_eval = wb.create_sheet()
    ws_cap = wb.create_sheet()

    wb.remove(default_sheet)

    build_tab2_assessment(wb, ws_eval, lang=lang)
    build_tab3_capital_plan(wb, ws_cap, lang=lang)
    build_tab1_dashboard(wb, ws_dash, lang=lang)

    wb.active = ws_dash

    wb.save(out_path)
    print(f"[OK] Libro Excel generado con éxito ({lang}): {out_path}")
    return out_path


def main():
    print("Iniciando construcción de modelos Excel McKinsey / GE 3x3...")
    es_path = generate_workbook(lang='ES')
    en_path = generate_workbook(lang='EN')

    dir_es = os.path.join(DIR_PACKAGES, "[ES]_Matriz_McKinsey_GE")
    dir_en = os.path.join(DIR_PACKAGES, "[EN]_McKinsey_GE_Matrix")
    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    generate_workbook(lang='ES', out_path=os.path.join(dir_es, "ES_Matriz_McKinsey_GE_Datalaria.xlsx"))
    generate_workbook(lang='EN', out_path=os.path.join(dir_en, "EN_McKinsey_GE_Matrix_Datalaria.xlsx"))

    print("Construcción completada exitosamente.")


if __name__ == "__main__":
    main()
