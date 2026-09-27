#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos de decisión estratégica en Excel oficiales de Datalaria:
1. Porter_5_Fuerzas_Datalaria_ES.xlsx (Versión en Español)
2. Porter_5_Forces_Datalaria_EN.xlsx (Versión en Inglés)

Estructura de 4 pestañas:
- Pestaña 1: Dashboard Ejecutivo / Executive Dashboard (KPIs, Atractivo, Gráfico Radar dinámico, Postura Estratégica)
- Pestaña 2: Evaluación 5 Fuerzas / 5 Forces Assessment (Evaluación cuantitativa y ponderada de las 5 fuerzas de Porter)
- Pestaña 3: Matriz Atractivo vs Moat / Attractiveness & Moat Matrix (Diagnóstico cartesiano de ventaja competitiva y brechas)
- Pestaña 4: Plan de Blindaje Estratégico / Strategic Moat Action Plan (Iniciativas con Owner C-Level, CAPEX/OPEX, EBITDA/ROIC)

Normas corporativas:
- Protección de hojas con contraseña "Datalaria2026".
- Celdas de entrada desbloqueadas, fórmulas y encabezados protegidos.
- Anchos de columna generosos y ajuste de texto (wrap_text=True).
- Formatos localizados: ES (coma decimal, €) y EN (punto decimal, $).
- Compatibilidad nativa garantizada al 100% con Microsoft Excel y Google Sheets.
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
COLOR_TEAL_ACCENT = "0D9488"    # Teal 600 / Barreras & Entrantes
COLOR_AMBER_ACCENT = "D97706"   # Amber 600 / Proveedores
COLOR_ROSE_ACCENT = "E11D48"    # Rose 600 / Clientes
COLOR_PURPLE_ACCENT = "7C3AED"  # Purple 600 / Sustitutos
COLOR_EMERALD_ACCENT = "059669" # Emerald 600 / Moat / Atractivo

# Fondos claros de tarjetas y contenedores
COLOR_BG_LIGHT = "F8FAFC"       # Slate 50
COLOR_BG_CARD = "F1F5F9"        # Slate 100
COLOR_WHITE = "FFFFFF"          # Fondo inputs desbloqueados

# Fondos temáticos por fuerza
COLOR_F1_BG = "EFF6FF"          # Ice Blue (Rivalidad)
COLOR_F1_BORDER = "3B82F6"
COLOR_F1_TEXT = "1E40AF"

COLOR_F2_BG = "FFFBEB"          # Amber (Proveedores)
COLOR_F2_BORDER = "F59E0B"
COLOR_F2_TEXT = "92400E"

COLOR_F3_BG = "FFF1F2"          # Rose (Clientes)
COLOR_F3_BORDER = "F43F5E"
COLOR_F3_TEXT = "9F1239"

COLOR_F4_BG = "F0FDFA"          # Teal (Nuevos Entrantes)
COLOR_F4_BORDER = "14B8A6"
COLOR_F4_TEXT = "0F766E"

COLOR_F5_BG = "F5F3FF"          # Purple (Sustitutos)
COLOR_F5_BORDER = "8B5CF6"
COLOR_F5_TEXT = "5B21B6"

COLOR_MOAT_BG = "ECFDF5"        # Emerald (Moat / Blindaje)
COLOR_MOAT_BORDER = "10B981"
COLOR_MOAT_TEXT = "065F46"

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


def apply_sheet_protection(ws):
    """Protege la hoja de cálculo con contraseña corporativa de Datalaria."""
    ws.protection.sheet = True
    ws.protection.password = PASSWORD_PROTECT
    ws.protection.selectUnlockedCells = True
    ws.protection.selectLockedCells = True


# ==============================================================================
# PESTAÑA 1: DASHBOARD EJECUTIVO
# ==============================================================================
def build_tab1_dashboard(wb, lang='ES'):
    ws = wb.active
    tab_name = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    ws.title = tab_name
    ws.views.sheetView[0].showGridLines = True
    styles = get_base_styles(lang)

    t_eval = "Evaluación 5 Fuerzas" if lang == 'ES' else "5 Forces Assessment"
    t_moat = "Matriz Atractivo vs Moat" if lang == 'ES' else "Attractiveness & Moat Matrix"
    t_plan = "Plan de Blindaje Estratégico" if lang == 'ES' else "Strategic Moat Action Plan"

    # --- BANNER DE CABECERA ---
    ws.merge_cells('B1:M1')
    ws['B1'] = "DATALARIA STRATEGY PRACTICE • MCKINSEY & BCG STANDARD • EXECUTIVE DECISION PACK"
    ws['B1'].font = styles['kicker_font']
    ws['B1'].fill = styles['title_fill']
    ws['B1'].alignment = styles['align_center']

    ws.merge_cells('B2:M2')
    ws['B2'] = "DASHBOARD ESTRATÉGICO: 5 FUERZAS DE PORTER PONDERADAS & ATRACTIVO DE INDUSTRIA" if lang == 'ES' else "EXECUTIVE DASHBOARD: WEIGHTED PORTER'S 5 FORCES & INDUSTRY ATTRACTIVENESS"
    ws['B2'].font = styles['title_font']
    ws['B2'].fill = styles['title_fill']
    ws['B2'].alignment = styles['align_center']

    ws.merge_cells('B3:M3')
    ws['B3'] = "Modelo cuantitativo de intensidad competitiva, diagnóstico de foso defensivo (Moat) y postura estratégica ante Consejo" if lang == 'ES' else "Quantitative competitive intensity model, economic moat diagnostics, and board-level strategic posture"
    ws['B3'].font = styles['subtitle_font']
    ws['B3'].fill = styles['title_fill']
    ws['B3'].alignment = styles['align_center']
    ws.row_dimensions[2].height = 28

    # --- 4 TARJETAS KPI EJECUTIVAS (B5:M8) ---
    cards_config = [
        ('B', 'D',
         "INTENSIDAD COMPETITIVA (1-5)" if lang == 'ES' else "COMPETITIVE INTENSITY (1-5)",
         "=E17",
         f'=IF(B6>=3.8,"Severa / Hostil",IF(B6>=2.8,"Moderada","Baja / Favorable"))' if lang == 'ES' else f'=IF(B6>=3.8,"Severe / Hostile",IF(B6>=2.8,"Moderate","Low / Favorable"))',
         COLOR_NAVY_DARK, COLOR_F1_BG, COLOR_F1_BORDER),

        ('E', 'G',
         "ATRACTIVO ESTRUCTURAL (A_ind)" if lang == 'ES' else "INDUSTRY ATTRACTIVENESS (A_ind)",
         "=5-B6",
         f'=IF(E6>=2.2,"Rentabilidad Superior",IF(E6>=1.4,"Rentabilidad Media","Presión de Márgenes"))' if lang == 'ES' else f'=IF(E6>=2.2,"Superior Profitability",IF(E6>=1.4,"Moderate Margins","Severe Margin Pressure"))',
         COLOR_NAVY_DARK, COLOR_MOAT_BG, COLOR_MOAT_BORDER),

        ('H', 'J',
         "FORTALEZA DEL MOAT (1-5)" if lang == 'ES' else "ECONOMIC MOAT STRENGTH (1-5)",
         f"='{t_moat}'!F15",
         f'=IF(H6>=3.5,"Foso Defendible Alto",IF(H6>=2.5,"Ventaja Moderada","Alta Vulnerabilidad"))' if lang == 'ES' else f'=IF(H6>=3.5,"Strong Economic Moat",IF(H6>=2.5,"Moderate Advantage","High Vulnerability"))',
         COLOR_NAVY_DARK, COLOR_F2_BG, COLOR_F2_BORDER),

        ('K', 'M',
         "POSTURA ESTRATÉGICA SUGERIDA" if lang == 'ES' else "SUGGESTED STRATEGIC POSTURE",
         f'=IF(AND(E6>=2,H6>=3),"LIDERAZGO Y EXPANSIÓN",IF(AND(E6<2,H6>=3),"BLINDAJE Y COSECHA",IF(AND(E6>=2,H6<3),"DIFERENCIACIÓN RÁPIDA","ENFOQUE DE NICHO")))' if lang == 'ES' else f'=IF(AND(E6>=2,H6>=3),"LEADERSHIP & EXPANSION",IF(AND(E6<2,H6>=3),"MOAT DEFENSE & HARVEST",IF(AND(E6>=2,H6<3),"URGENT DIFFERENTIATION","NICHE FOCUS")))',
         f"='{t_moat}'!D27",
         COLOR_NAVY_DARK, COLOR_BG_LIGHT, COLOR_BORDER_MED)
    ]

    for c_start, c_end, title, f_val, f_sub, col_title, bg_card, border_card in cards_config:
        # Header de tarjeta
        ws.merge_cells(f"{c_start}5:{c_end}5")
        ws[f"{c_start}5"] = title
        ws[f"{c_start}5"].font = Font(name='Segoe UI', size=9, bold=True, color="64748B")
        ws[f"{c_start}5"].alignment = styles['align_center']
        ws[f"{c_start}5"].fill = PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid')

        # Valor métrico
        ws.merge_cells(f"{c_start}6:{c_end}6")
        ws[f"{c_start}6"] = f_val
        ws[f"{c_start}6"].font = Font(name='Segoe UI', size=16, bold=True, color=COLOR_NAVY_DARK)
        ws[f"{c_start}6"].alignment = styles['align_center']
        ws[f"{c_start}6"].fill = PatternFill(start_color=bg_card, end_color=bg_card, fill_type='solid')
        if f_val.startswith("="):
            ws[f"{c_start}6"].number_format = styles['num_fmt_dec']

        # Subtexto dinámico
        ws.merge_cells(f"{c_start}7:{c_end}7")
        ws[f"{c_start}7"] = f_sub
        ws[f"{c_start}7"].font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"{c_start}7"].alignment = styles['align_center']
        ws[f"{c_start}7"].fill = PatternFill(start_color=bg_card, end_color=bg_card, fill_type='solid')

        # Borde exterior de tarjeta
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

    # --- TABLA RESUMEN DE LAS 5 FUERZAS (B10:G17) ---
    ws.merge_cells('B10:G10')
    ws['B10'] = "RESUMEN CUANTITATIVO DE LAS 5 FUERZAS DE PORTER" if lang == 'ES' else "QUANTITATIVE 5 FORCES OF PORTER SUMMARY"
    ws['B10'].font = styles['section_font']
    ws['B10'].fill = styles['section_fill']
    ws['B10'].alignment = styles['align_left']

    headers_f = [
        ("ID", 'B', 8),
        ("Fuerza Competitiva" if lang == 'ES' else "Competitive Force", 'C', 32),
        ("Ponderación (Wk)" if lang == 'ES' else "Macro Weight (Wk)", 'D', 18),
        ("Puntuación (1-5)" if lang == 'ES' else "Score (1-5)", 'E', 18),
        ("Severidad" if lang == 'ES' else "Severity", 'F', 20),
        ("Driver Principal de Amenaza" if lang == 'ES' else "Primary Threat Driver", 'G', 35),
    ]

    for h_txt, col, w in headers_f:
        ws[f"{col}11"] = h_txt
        ws[f"{col}11"].font = styles['header_font']
        ws[f"{col}11"].fill = styles['header_fill']
        ws[f"{col}11"].alignment = styles['align_center'] if col in ['B', 'D', 'E', 'F'] else styles['align_left']
        ws[f"{col}11"].border = styles['header_border']

    forces_data = [
        ("F1",
         "1. Rivalidad Competitiva" if lang == 'ES' else "1. Competitive Rivalry",
         f"='{t_eval}'!H4",
         f"='{t_eval}'!F11",
         f'=IF(E12>=3.8,"Severa / Hostil",IF(E12>=2.8,"Moderada","Baja"))' if lang == 'ES' else f'=IF(E12>=3.8,"Severe / Hostile",IF(E12>=2.8,"Moderate","Low"))',
         "Guerra de precios y concentración de cuota" if lang == 'ES' else "Price competition & market share battle"),

        ("F2",
         "2. Poder de Proveedores" if lang == 'ES' else "2. Supplier Power",
         f"='{t_eval}'!H13",
         f"='{t_eval}'!F20",
         f'=IF(E13>=3.8,"Severa / Hostil",IF(E13>=2.8,"Moderada","Baja"))' if lang == 'ES' else f'=IF(E13>=3.8,"Severe / Hostile",IF(E13>=2.8,"Moderate","Low"))',
         "Insumos críticos especializados sin sustituto" if lang == 'ES' else "Specialized proprietary inputs without substitutes"),

        ("F3",
         "3. Poder de Clientes" if lang == 'ES' else "3. Buyer Power",
         f"='{t_eval}'!H22",
         f"='{t_eval}'!F29",
         f'=IF(E14>=3.8,"Severa / Hostil",IF(E14>=2.8,"Moderada","Baja"))' if lang == 'ES' else f'=IF(E14>=3.8,"Severe / Hostile",IF(E14>=2.8,"Moderate","Low"))',
         "Concentración de compras y bajos costes de cambio" if lang == 'ES' else "High volume concentration & low switching costs"),

        ("F4",
         "4. Amenaza Nuevos Entrantes" if lang == 'ES' else "4. Threat of New Entrants",
         f"='{t_eval}'!H31",
         f"='{t_eval}'!F38",
         f'=IF(E15>=3.8,"Severa / Hostil",IF(E15>=2.8,"Moderada","Baja"))' if lang == 'ES' else f'=IF(E15>=3.8,"Severe / Hostile",IF(E15>=2.8,"Moderate","Low"))',
         "Digitalización y reducción de barreras de capital" if lang == 'ES' else "Digital business models lowering capital entry"),

        ("F5",
         "5. Amenaza de Sustitutos" if lang == 'ES' else "5. Threat of Substitutes",
         f"='{t_eval}'!H40",
         f"='{t_eval}'!F46",
         f'=IF(E16>=3.8,"Severa / Hostil",IF(E16>=2.8,"Moderada","Baja"))' if lang == 'ES' else f'=IF(E16>=3.8,"Severe / Hostile",IF(E16>=2.8,"Moderate","Low"))',
         "Tecnologías emergentes con mejor coste-rendimiento" if lang == 'ES' else "Emerging tech with superior price-performance")
    ]

    for idx, (f_id, f_name, f_w, f_score, f_sev, f_driver) in enumerate(forces_data, start=12):
        ws[f"B{idx}"] = f_id
        ws[f"B{idx}"].font = styles['code_font']
        ws[f"B{idx}"].alignment = styles['align_center']
        ws[f"B{idx}"].fill = styles['calc_fill']
        ws[f"B{idx}"].border = styles['thin_border']

        ws[f"C{idx}"] = f_name
        ws[f"C{idx}"].font = styles['cell_bold']
        ws[f"C{idx}"].alignment = styles['align_left_wrap']
        ws[f"C{idx}"].fill = styles['calc_fill']
        ws[f"C{idx}"].border = styles['thin_border']

        ws[f"D{idx}"] = f_w
        ws[f"D{idx}"].font = styles['cell_font']
        ws[f"D{idx}"].alignment = styles['align_center']
        ws[f"D{idx}"].fill = styles['calc_fill']
        ws[f"D{idx}"].border = styles['thin_border']
        ws[f"D{idx}"].number_format = styles['num_fmt_pct']

        ws[f"E{idx}"] = f_score
        ws[f"E{idx}"].font = styles['cell_bold']
        ws[f"E{idx}"].alignment = styles['align_center']
        ws[f"E{idx}"].fill = styles['calc_fill']
        ws[f"E{idx}"].border = styles['thin_border']
        ws[f"E{idx}"].number_format = styles['num_fmt_dec']

        ws[f"F{idx}"] = f_sev
        ws[f"F{idx}"].font = styles['cell_bold']
        ws[f"F{idx}"].alignment = styles['align_center']
        ws[f"F{idx}"].fill = styles['calc_fill']
        ws[f"F{idx}"].border = styles['thin_border']

        ws[f"G{idx}"] = f_driver
        ws[f"G{idx}"].font = styles['cell_font']
        ws[f"G{idx}"].alignment = styles['align_left_wrap']
        ws[f"G{idx}"].fill = styles['calc_fill']
        ws[f"G{idx}"].border = styles['thin_border']

    # Fila Total
    ws['B17'] = "TOTAL"
    ws['B17'].font = styles['cell_bold']
    ws['B17'].alignment = styles['align_center']
    ws['B17'].fill = styles['total_fill']
    ws['B17'].border = styles['total_border']

    ws['C17'] = "Índice de Intensidad Competitiva Global" if lang == 'ES' else "Overall Competitive Intensity Index"
    ws['C17'].font = styles['cell_bold']
    ws['C17'].alignment = styles['align_left']
    ws['C17'].fill = styles['total_fill']
    ws['C17'].border = styles['total_border']

    ws['D17'] = "=SUM(D12:D16)"
    ws['D17'].font = styles['cell_bold']
    ws['D17'].alignment = styles['align_center']
    ws['D17'].fill = styles['total_fill']
    ws['D17'].border = styles['total_border']
    ws['D17'].number_format = styles['num_fmt_pct']

    ws['E17'] = "=SUMPRODUCT(D12:D16,E12:E16)"
    ws['E17'].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws['E17'].alignment = styles['align_center']
    ws['E17'].fill = styles['total_fill']
    ws['E17'].border = styles['total_border']
    ws['E17'].number_format = styles['num_fmt_dec']

    ws['F17'] = f'=IF(E17>=3.8,"Alta Hostilidad",IF(E17>=2.8,"Intensidad Media","Atractivo Alto"))' if lang == 'ES' else f'=IF(E17>=3.8,"High Hostility",IF(E17>=2.8,"Moderate Pressure","High Attractiveness"))'
    ws['F17'].font = styles['cell_bold']
    ws['F17'].alignment = styles['align_center']
    ws['F17'].fill = styles['total_fill']
    ws['F17'].border = styles['total_border']

    ws['G17'] = "Media ponderada multivariable" if lang == 'ES' else "Multivariate weighted score"
    ws['G17'].font = styles['subtitle_font']
    ws['G17'].alignment = styles['align_left']
    ws['G17'].fill = styles['total_fill']
    ws['G17'].border = styles['total_border']

    # --- GRÁFICO RADAR DINÁMICO EN H10:M25 ---
    radar = RadarChart()
    radar.type = "standard"
    labels_ref = Reference(ws, min_col=3, min_row=12, max_row=16)
    data_ref = Reference(ws, min_col=5, min_row=11, max_row=16)
    radar.add_data(data_ref, titles_from_data=True)
    radar.set_categories(labels_ref)
    radar.title = "Radar de las 5 Fuerzas de Porter" if lang == 'ES' else "Porter's 5 Forces Radar Chart"
    radar.style = 26
    radar.width = 16.5
    radar.height = 10.5
    ws.add_chart(radar, "H10")

    # --- TABLA DE ORIENTACIÓN ESTRATÉGICA & P&L (B19:G26) ---
    ws.merge_cells('B19:G19')
    ws['B19'] = "DIAGNÓSTICO ESTRATÉGICO Y RECOMENDACIÓN DE ASIGNACIÓN DE CAPITAL" if lang == 'ES' else "STRATEGIC DIAGNOSIS & CAPITAL ALLOCATION GUIDANCE"
    ws['B19'].font = styles['section_font']
    ws['B19'].fill = styles['section_fill']
    ws['B19'].alignment = styles['align_left']

    diag_headers = [
        ("Dimensión de Decisión" if lang == 'ES' else "Decision Dimension", 'B', 'C'),
        ("Valor / Diagnóstico" if lang == 'ES' else "Value / Diagnosis", 'D', 'E'),
        ("Implicación en Comité / Plan de Acción" if lang == 'ES' else "Board Implication / Action Plan", 'F', 'G'),
    ]

    for h_txt, col_s, col_e in diag_headers:
        ws.merge_cells(f"{col_s}20:{col_e}20")
        ws[f"{col_s}20"] = h_txt
        ws[f"{col_s}20"].font = styles['header_font']
        ws[f"{col_s}20"].fill = styles['header_fill']
        ws[f"{col_s}20"].alignment = styles['align_left'] if col_s == 'B' else styles['align_center']
        style_merged_range(ws, f"{col_s}20:{col_e}20", border=styles['header_border'])

    diag_rows = [
        ("Atractivo Estructural de Industria" if lang == 'ES' else "Structural Industry Attractiveness",
         "=E6",
         f'=IF(E6>=2.2,"Margen EBITDA proyectado > 22%. Sector óptimo para expansión.",IF(E6>=1.4,"Margen EBITDA en paridad 12-16%. Requiere diferenciación activa.","Márgenes bajo compresión <10%. Invertir exclusivamente en blindaje."))' if lang == 'ES' else f'=IF(E6>=2.2,"Projected EBITDA margin > 22%. Ideal industry for expansion.",IF(E6>=1.4,"EBITDA margin at parity 12-16%. Requires differentiation.","Margins compressed <10%. Invest strictly in moat protection."))'),

        ("Fuerza Crítica de Mayor Severidad" if lang == 'ES' else "Critical Peak Force (Highest Severity)",
         f'=INDEX(C12:C16, MATCH(MAX(E12:E16), E12:E16, 0))',
         "Prioridad absoluta en la asignación de CAPEX y blindaje de contratos" if lang == 'ES' else "Top capital allocation priority for moat building and contract locks"),

        ("Brecha de Ventaja Competitiva (Moat - Rivalidad)" if lang == 'ES' else "Competitive Moat Advantage Gap",
         "=H6-E12",
         f'=IF((H6-E12)>=0,"Foso superior a la rivalidad media. Capacidad de fijación de precios intacta.","Rivalidad supera al foso actual. Riesgo inminente de erosión de márgenes.")' if lang == 'ES' else f'=IF((H6-E12)>=0,"Moat exceeds industry rivalry. Pricing power remains protected.","Rivalry surpasses internal moat. Immediate margin erosion risk.")'),

        ("Presupuesto de Blindaje Propuesto (CAPEX + OPEX)" if lang == 'ES' else "Proposed Moat Action Budget (CAPEX + OPEX)",
         f"='{t_plan}'!H15+'{t_plan}'!I15",
         "Presupuesto consolidado del Plan de Blindaje Estratégico" if lang == 'ES' else "Consolidated budget from Strategic Moat Action Plan"),

        ("Impacto Estimado en Margen EBITDA" if lang == 'ES' else "Estimated EBITDA Margin Impact",
         "+2.5% a +4.8% en 18 meses" if lang == 'ES' else "+2.5% to +4.8% over 18 months",
         "Blindaje contra comoditización y aumento de costes de cambio" if lang == 'ES' else "Protection against commoditization & buyer switching friction")
    ]

    for idx, (dim_txt, val_formula, imp_txt) in enumerate(diag_rows, start=21):
        ws.merge_cells(f"B{idx}:C{idx}")
        ws[f"B{idx}"] = dim_txt
        ws[f"B{idx}"].font = styles['cell_bold']
        ws[f"B{idx}"].fill = styles['calc_fill']
        ws[f"B{idx}"].alignment = styles['align_left_wrap']
        style_merged_range(ws, f"B{idx}:C{idx}", border=styles['thin_border'])

        ws.merge_cells(f"D{idx}:E{idx}")
        ws[f"D{idx}"] = val_formula
        ws[f"D{idx}"].font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"D{idx}"].fill = styles['calc_fill']
        ws[f"D{idx}"].alignment = styles['align_center_wrap']
        if str(val_formula).startswith("=") and ("+" in str(val_formula) or "E6" in str(val_formula)):
            if "+" in str(val_formula):
                ws[f"D{idx}"].number_format = styles['num_fmt_curr']
            else:
                ws[f"D{idx}"].number_format = styles['num_fmt_dec']
        style_merged_range(ws, f"D{idx}:E{idx}", border=styles['thin_border'])

        ws.merge_cells(f"F{idx}:G{idx}")
        ws[f"F{idx}"] = imp_txt
        ws[f"F{idx}"].font = styles['cell_font']
        ws[f"F{idx}"].fill = styles['calc_fill']
        ws[f"F{idx}"].alignment = styles['align_left_wrap']
        style_merged_range(ws, f"F{idx}:G{idx}", border=styles['thin_border'])

    # Protección de hoja
    apply_sheet_protection(ws)


# ==============================================================================
# PESTAÑA 2: EVALUACIÓN 5 FUERZAS
# ==============================================================================
def build_tab2_assessment(wb, lang='ES'):
    tab_name = "Evaluación 5 Fuerzas" if lang == 'ES' else "5 Forces Assessment"
    ws = wb.create_sheet(title=tab_name)
    ws.views.sheetView[0].showGridLines = True
    styles = get_base_styles(lang)

    # Banner
    ws.merge_cells('B1:H1')
    ws['B1'] = "DATALARIA | EVALUACIÓN CUANTITATIVA Y PONDERADA DE LAS 5 FUERZAS DE PORTER" if lang == 'ES' else "DATALARIA | WEIGHTED QUANTITATIVE PORTER'S 5 FORCES ASSESSMENT"
    ws['B1'].font = styles['title_font']
    ws['B1'].fill = styles['title_fill']
    ws['B1'].alignment = styles['align_center']

    ws.merge_cells('B2:H2')
    ws['B2'] = "Instrucciones: Edite únicamente las celdas en blanco (subfactores, pesos relativos e intensidad 1-5). Las fórmulas están protegidas." if lang == 'ES' else "Instructions: Edit only white cells (subfactors, relative weights, and 1-5 intensity). Formulas are locked."
    ws['B2'].font = styles['subtitle_font']
    ws['B2'].fill = styles['title_fill']
    ws['B2'].alignment = styles['align_center']
    ws.row_dimensions[1].height = 24

    # Encabezados de tabla
    headers = [
        ("ID", 'B', 8),
        ("Subfactor Estratégico Analizado" if lang == 'ES' else "Strategic Subfactor Evaluated", 'C', 45),
        ("Peso (w)" if lang == 'ES' else "Weight (w)", 'D', 14),
        ("Fuerza (1-5)" if lang == 'ES' else "Rating (1-5)", 'E', 14),
        ("Puntuación" if lang == 'ES' else "Weighted", 'F', 16),
        ("Criterio de Evaluación / Evidencia Operativa Auditable" if lang == 'ES' else "Evaluation Criteria / Auditable Evidence", 'G', 48),
        ("Fuerza Neta" if lang == 'ES' else "Net Force", 'H', 18)
    ]

    # Datos por defecto de las 5 fuerzas
    forces_def = [
        # F1: Rivalidad
        {
            'id': 'F1',
            'name': "FUERZA 1: RIVALIDAD ENTRE COMPETIDORES EXISTENTES" if lang == 'ES' else "FORCE 1: COMPETITIVE RIVALRY AMONG EXISTING PLAYERS",
            'macro_w': 0.25,
            'color_bg': COLOR_F1_BG,
            'color_border': COLOR_F1_BORDER,
            'color_text': COLOR_F1_TEXT,
            'subfactors': [
                ("F1.1",
                 "Concentración y equilibrio de cuotas de mercado" if lang == 'ES' else "Competitor concentration and market share balance",
                 0.20, 4.0,
                 "Oligopolio asimétrico: 3 grandes actores concentran el 68% del mercado" if lang == 'ES' else "Asymmetric oligopoly: 3 players hold 68% market share"),
                ("F1.2",
                 "Tasa de crecimiento anual del sector / mercado" if lang == 'ES' else "Annual industry / sector growth rate",
                 0.25, 4.0,
                 "Crecimiento desacelerado (+1.8% anual); competencia de suma cero" if lang == 'ES' else "Decelerated growth (+1.8% YoY); zero-sum competition"),
                ("F1.3",
                 "Costes fijos elevados y barreras de salida industriales" if lang == 'ES' else "High fixed costs and industrial exit barriers",
                 0.20, 3.5,
                 "Maquinaria pesada amortizada a largo plazo e indemnizaciones elevadas" if lang == 'ES' else "Long-term heavy assets and high exit severance costs"),
                ("F1.4",
                 "Grado de comoditización y falta de diferenciación" if lang == 'ES' else "Degree of product commoditization and differentiation",
                 0.20, 3.0,
                 "Diferenciación percibida media; clientes licitan por precio" if lang == 'ES' else "Moderate differentiation; buyers run tender auctions on price"),
                ("F1.5",
                 "Guerra de precios, descuentos y promociones comerciales" if lang == 'ES' else "Price competition, discounts and commercial promotions",
                 0.15, 4.0,
                 "Descuentos de hasta 20% para retener grandes cuentas corporativas" if lang == 'ES' else "Aggressive discounts up to 20% to defend key corporate accounts")
            ]
        },
        # F2: Proveedores
        {
            'id': 'F2',
            'name': "FUERZA 2: PODER DE NEGOCIACIÓN DE LOS PROVEEDORES" if lang == 'ES' else "FORCE 2: BARGAINING POWER OF SUPPLIERS",
            'macro_w': 0.20,
            'color_bg': COLOR_F2_BG,
            'color_border': COLOR_F2_BORDER,
            'color_text': COLOR_F2_TEXT,
            'subfactors': [
                ("F2.1",
                 "Concentración de proveedores frente a compradores" if lang == 'ES' else "Supplier concentration vs buyer industry concentration",
                 0.25, 3.5,
                 "Alta concentración en microprocesadores y materias primas clave" if lang == 'ES' else "High concentration in specialized raw inputs and chips"),
                ("F2.2",
                 "Disponibilidad de insumos sustitutos viables" if lang == 'ES' else "Availability of substitute raw inputs / components",
                 0.20, 4.0,
                 "Insumos propietarios sin sustituto homologado a corto plazo" if lang == 'ES' else "Proprietary components with no approved substitutes"),
                ("F2.3",
                 "Costes de cambio de proveedor (Switching Costs de compras)" if lang == 'ES' else "Supplier switching costs (re-tooling and qualification)",
                 0.20, 3.0,
                 "Coste de recertificación técnica de 6 a 9 meses por nuevo proveedor" if lang == 'ES' else "6-9 months technical re-certification for new suppliers"),
                ("F2.4",
                 "Amenaza de integración vertical hacia adelante del proveedor" if lang == 'ES' else "Threat of forward vertical integration by suppliers",
                 0.15, 2.0,
                 "Baja amenaza: proveedores no poseen capilaridad comercial final" if lang == 'ES' else "Low threat: suppliers lack downstream distribution channels"),
                ("F2.5",
                 "Peso del coste del insumo sobre el coste total del producto" if lang == 'ES' else "Input cost proportion of total product cost",
                 0.20, 3.5,
                 "Representa el 42% del COGS directo en cuentas clave" if lang == 'ES' else "Represents 42% of direct COGS in flagship product lines")
            ]
        },
        # F3: Clientes
        {
            'id': 'F3',
            'name': "FUERZA 3: PODER DE NEGOCIACIÓN DE LOS CLIENTES" if lang == 'ES' else "FORCE 3: BARGAINING POWER OF BUYERS",
            'macro_w': 0.25,
            'color_bg': COLOR_F3_BG,
            'color_border': COLOR_F3_BORDER,
            'color_text': COLOR_F3_TEXT,
            'subfactors': [
                ("F3.1",
                 "Concentración de compradores y volumen de compra por cliente" if lang == 'ES' else "Buyer concentration and volume share per account",
                 0.25, 4.0,
                 "Los 5 principales clientes concentran el 52% de la facturación" if lang == 'ES' else "Top 5 corporate buyers account for 52% of total revenue"),
                ("F3.2",
                 "Costes de cambio para el cliente al migrar a un rival" if lang == 'ES' else "Buyer switching costs when moving to a competitor",
                 0.25, 3.0,
                 "Costes de migración moderados; APIS estándar facilitan la transición" if lang == 'ES' else "Moderate migration friction; standard APIs ease transition"),
                ("F3.3",
                 "Sensibilidad al precio y presión de márgenes del comprador" if lang == 'ES' else "Buyer price sensitivity and margin pressure",
                 0.20, 4.0,
                 "Compradores en sectores con márgenes reducidos auditando costes" if lang == 'ES' else "Buyers operate in low-margin sectors, driving cost audits"),
                ("F3.4",
                 "Disponibilidad de información exhaustiva de precios y costes" if lang == 'ES' else "Information transparency regarding industry costs and benchmarks",
                 0.15, 4.0,
                 "Plataformas B2B de comparación y subastas inversas estandarizadas" if lang == 'ES' else "B2B benchmark portals and digital reverse-auction tenders"),
                ("F3.5",
                 "Amenaza de integración vertical hacia atrás del comprador" if lang == 'ES' else "Threat of backward vertical integration by buyers",
                 0.15, 2.5,
                 "In-housing parcial de ciertas funciones básicas, no del core" if lang == 'ES' else "Selective in-housing of peripheral services, not core")
            ]
        },
        # F4: Nuevos Entrantes
        {
            'id': 'F4',
            'name': "FUERZA 4: AMENAZA DE NUEVOS ENTRANTES (BARRERAS DE ENTRADA)" if lang == 'ES' else "FORCE 4: THREAT OF NEW ENTRANTS (ENTRY BARRIERS)",
            'macro_w': 0.15,
            'color_bg': COLOR_F4_BG,
            'color_border': COLOR_F4_BORDER,
            'color_text': COLOR_F4_TEXT,
            'subfactors': [
                ("F4.1",
                 "Economías de escala requeridas para ser rentable" if lang == 'ES' else "Economies of scale required for unit cost parity",
                 0.25, 2.5,
                 "Escala crítica media; plataformas cloud han reducido el umbral" if lang == 'ES' else "Moderate critical scale; cloud architectures lowered threshold"),
                ("F4.2",
                 "Requisitos de capital e inversión inicial en I+D" if lang == 'ES' else "Capital requirements and upfront R&D investments",
                 0.25, 2.0,
                 "Barrera alta: requiere 3M€ de inversión mínima y certificaciones ISO" if lang == 'ES' else "High barrier: requires $3M+ upfront capital & ISO audits"),
                ("F4.3",
                 "Acceso a canales de distribución y relaciones comerciales" if lang == 'ES' else "Access to distribution channels and established customer access",
                 0.20, 3.0,
                 "Canales tradicionales saturados pero marketplaces digitales abiertos" if lang == 'ES' else "Incumbent channels locked but digital marketplaces open"),
                ("F4.4",
                 "Barreras regulatorias, licencias y cumplimiento normativo" if lang == 'ES' else "Regulatory compliance, licenses and legal frameworks",
                 0.15, 2.0,
                 "Normativa europea exigente que protege a incumbentes autorizados" if lang == 'ES' else "Strict compliance protecting certified existing operators"),
                ("F4.5",
                 "Ventajas de costes de los incumbentes (curva de aprendizaje)" if lang == 'ES' else "Incumbent cost advantages (learning curve & proprietary data)",
                 0.15, 2.5,
                 "Curva de experiencia de 8 años con algoritmos optimizados" if lang == 'ES' else "8-year proprietary operational datasets and learning curve")
            ]
        },
        # F5: Sustitutos
        {
            'id': 'F5',
            'name': "FUERZA 5: AMENAZA DE PRODUCTOS O SERVICIOS SUSTITUTOS" if lang == 'ES' else "FORCE 5: THREAT OF SUBSTITUTE PRODUCTS OR SERVICES",
            'macro_w': 0.15,
            'color_bg': COLOR_F5_BG,
            'color_border': COLOR_F5_BORDER,
            'color_text': COLOR_F5_TEXT,
            'subfactors': [
                ("F5.1",
                 "Relación precio / rendimiento del sustituto tecnológico" if lang == 'ES' else "Relative price-performance tradeoff of technological substitutes",
                 0.30, 4.0,
                 "Sustitutos automatizados por IA ofrecen 40% de ahorro de coste" if lang == 'ES' else "AI-driven automated tools deliver 40% lower operating cost"),
                ("F5.2",
                 "Costes de cambio para el cliente hacia el sustituto" if lang == 'ES' else "Customer switching costs when adopting substitutes",
                 0.25, 3.0,
                 "Curva de adopción inicial pero integración sencilla vía SaaS" if lang == 'ES' else "Initial adoption friction but seamless SaaS integration"),
                ("F5.3",
                 "Propensión y madurez del comprador hacia la nueva tecnología" if lang == 'ES' else "Buyer propensity and technological readiness to substitute",
                 0.25, 3.5,
                 "C-Levels explorando activamente pilotos de automatización" if lang == 'ES' else "C-Suite buyers actively piloting automation alternatives"),
                ("F5.4",
                 "Velocidad de mejora en la curva de rendimiento del sustituto" if lang == 'ES' else "Pace of improvement in the substitute's performance trajectory",
                 0.20, 4.0,
                 "Mejoras exponenciales interanuales en fiabilidad y cobertura" if lang == 'ES' else "Exponential YoY gains in reliability, speed and scope")
            ]
        }
    ]

    current_row = 4

    for f_idx, f_info in enumerate(forces_def, start=1):
        # Header de sección de la fuerza
        ws.merge_cells(f"B{current_row}:G{current_row}")
        ws[f"B{current_row}"] = f_info['name']
        ws[f"B{current_row}"].font = Font(name='Segoe UI', size=11, bold=True, color=f_info['color_text'])
        ws[f"B{current_row}"].fill = PatternFill(start_color=f_info['color_bg'], end_color=f_info['color_bg'], fill_type='solid')
        ws[f"B{current_row}"].alignment = styles['align_left']

        ws[f"H{current_row}"] = f_info['macro_w']
        ws[f"H{current_row}"].font = styles['cell_bold']
        ws[f"H{current_row}"].fill = PatternFill(start_color=f_info['color_bg'], end_color=f_info['color_bg'], fill_type='solid')
        ws[f"H{current_row}"].alignment = styles['align_center']
        ws[f"H{current_row}"].number_format = styles['num_fmt_pct']
        ws[f"H{current_row}"].protection = Protection(locked=False)  # Macro weight editable

        style_merged_range(ws, f"B{current_row}:G{current_row}", border=Border(
            top=Side(style='medium', color=f_info['color_border']),
            bottom=Side(style='thin', color=f_info['color_border']),
            left=Side(style='thin', color=f_info['color_border']),
            right=Side(style='thin', color=f_info['color_border'])
        ))
        ws[f"H{current_row}"].border = Border(
            top=Side(style='medium', color=f_info['color_border']),
            bottom=Side(style='thin', color=f_info['color_border']),
            right=Side(style='thin', color=f_info['color_border'])
        )

        current_row += 1

        # Encabezados de columna
        for h_txt, col, w in headers:
            ws[f"{col}{current_row}"] = h_txt
            ws[f"{col}{current_row}"].font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_WHITE)
            ws[f"{col}{current_row}"].fill = styles['header_fill']
            ws[f"{col}{current_row}"].alignment = styles['align_center'] if col in ['B', 'D', 'E', 'F', 'H'] else styles['align_left']
            ws[f"{col}{current_row}"].border = styles['header_border']

        current_row += 1
        sub_start_row = current_row

        # Filas de subfactores
        for sub_id, sub_desc, sub_w, sub_rate, sub_crit in f_info['subfactors']:
            ws[f"B{current_row}"] = sub_id
            ws[f"B{current_row}"].font = styles['code_font']
            ws[f"B{current_row}"].alignment = styles['align_center']
            ws[f"B{current_row}"].fill = styles['calc_fill']
            ws[f"B{current_row}"].border = styles['thin_border']

            ws[f"C{current_row}"] = sub_desc
            ws[f"C{current_row}"].font = styles['cell_font']
            ws[f"C{current_row}"].alignment = styles['align_left_wrap']
            ws[f"C{current_row}"].fill = styles['input_fill']
            ws[f"C{current_row}"].border = styles['thin_border']
            ws[f"C{current_row}"].protection = Protection(locked=False)  # Editable

            ws[f"D{current_row}"] = sub_w
            ws[f"D{current_row}"].font = styles['cell_font']
            ws[f"D{current_row}"].alignment = styles['align_center']
            ws[f"D{current_row}"].fill = styles['input_fill']
            ws[f"D{current_row}"].border = styles['thin_border']
            ws[f"D{current_row}"].number_format = styles['num_fmt_pct']
            ws[f"D{current_row}"].protection = Protection(locked=False)  # Editable

            ws[f"E{current_row}"] = sub_rate
            ws[f"E{current_row}"].font = styles['cell_bold']
            ws[f"E{current_row}"].alignment = styles['align_center']
            ws[f"E{current_row}"].fill = styles['input_fill']
            ws[f"E{current_row}"].border = styles['thin_border']
            ws[f"E{current_row}"].number_format = styles['num_fmt_dec']
            ws[f"E{current_row}"].protection = Protection(locked=False)  # Editable

            ws[f"F{current_row}"] = f"=D{current_row}*E{current_row}"
            ws[f"F{current_row}"].font = styles['cell_bold']
            ws[f"F{current_row}"].alignment = styles['align_center']
            ws[f"F{current_row}"].fill = styles['calc_fill']
            ws[f"F{current_row}"].border = styles['thin_border']
            ws[f"F{current_row}"].number_format = styles['num_fmt_dec']

            ws[f"G{current_row}"] = sub_crit
            ws[f"G{current_row}"].font = styles['cell_font']
            ws[f"G{current_row}"].alignment = styles['align_left_wrap']
            ws[f"G{current_row}"].fill = styles['input_fill']
            ws[f"G{current_row}"].border = styles['thin_border']
            ws[f"G{current_row}"].protection = Protection(locked=False)  # Editable

            # Celda vacía H para alineación con subtotal
            ws[f"H{current_row}"].fill = styles['calc_fill']
            ws[f"H{current_row}"].border = styles['thin_border']

            current_row += 1

        sub_end_row = current_row - 1

        # Fila Subtotal de la Fuerza
        ws[f"B{current_row}"] = f"Σ {f_info['id']}"
        ws[f"B{current_row}"].font = styles['cell_bold']
        ws[f"B{current_row}"].alignment = styles['align_center']
        ws[f"B{current_row}"].fill = styles['total_fill']
        ws[f"B{current_row}"].border = styles['total_border']

        ws[f"C{current_row}"] = f"Subtotal Ponderado: {f_info['name']}" if lang == 'ES' else f"Weighted Subtotal: {f_info['name']}"
        ws[f"C{current_row}"].font = styles['cell_bold']
        ws[f"C{current_row}"].alignment = styles['align_left']
        ws[f"C{current_row}"].fill = styles['total_fill']
        ws[f"C{current_row}"].border = styles['total_border']

        ws[f"D{current_row}"] = f"=SUM(D{sub_start_row}:D{sub_end_row})"
        ws[f"D{current_row}"].font = styles['cell_bold']
        ws[f"D{current_row}"].alignment = styles['align_center']
        ws[f"D{current_row}"].fill = styles['total_fill']
        ws[f"D{current_row}"].border = styles['total_border']
        ws[f"D{current_row}"].number_format = styles['num_fmt_pct']

        ws[f"E{current_row}"] = f"=AVERAGE(E{sub_start_row}:E{sub_end_row})"
        ws[f"E{current_row}"].font = styles['cell_font']
        ws[f"E{current_row}"].alignment = styles['align_center']
        ws[f"E{current_row}"].fill = styles['total_fill']
        ws[f"E{current_row}"].border = styles['total_border']
        ws[f"E{current_row}"].number_format = styles['num_fmt_dec']

        ws[f"F{current_row}"] = f"=SUM(F{sub_start_row}:F{sub_end_row})"
        ws[f"F{current_row}"].font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"F{current_row}"].alignment = styles['align_center']
        ws[f"F{current_row}"].fill = styles['total_fill']
        ws[f"F{current_row}"].border = styles['total_border']
        ws[f"F{current_row}"].number_format = styles['num_fmt_dec']

        ws[f"G{current_row}"] = f'=IF(F{current_row}>=3.8,"SEVERIDAD ALTA (HOSTIL)",IF(F{current_row}>=2.8,"SEVERIDAD MODERADA","SEVERIDAD BAJA (FAVORABLE)"))' if lang == 'ES' else f'=IF(F{current_row}>=3.8,"HIGH SEVERITY (HOSTILE)",IF(F{current_row}>=2.8,"MODERATE SEVERITY","LOW SEVERITY (FAVORABLE)"))'
        ws[f"G{current_row}"].font = styles['cell_bold']
        ws[f"G{current_row}"].alignment = styles['align_center']
        ws[f"G{current_row}"].fill = styles['total_fill']
        ws[f"G{current_row}"].border = styles['total_border']

        ws[f"H{current_row}"] = f"=F{current_row}"
        ws[f"H{current_row}"].font = Font(name='Segoe UI', size=11, bold=True, color=f_info['color_text'])
        ws[f"H{current_row}"].alignment = styles['align_center']
        ws[f"H{current_row}"].fill = PatternFill(start_color=f_info['color_bg'], end_color=f_info['color_bg'], fill_type='solid')
        ws[f"H{current_row}"].border = styles['total_border']
        ws[f"H{current_row}"].number_format = styles['num_fmt_dec']

        current_row += 2  # Separación entre fuerzas

    # --- TABLA CONSOLIDADORA TOTAL DE INTENSIDAD COMPETITIVA ---
    ws.merge_cells(f"B{current_row}:H{current_row}")
    ws[f"B{current_row}"] = "ÍNDICE CONSOLIDADO DE INTENSIDAD COMPETITIVA (I_comp)" if lang == 'ES' else "CONSOLIDATED COMPETITIVE INTENSITY INDEX (I_comp)"
    ws[f"B{current_row}"].font = styles['title_font']
    ws[f"B{current_row}"].fill = styles['title_fill']
    ws[f"B{current_row}"].alignment = styles['align_center']
    current_row += 1

    # Cabecera consolidado
    summary_cols = [
        ("Fuerza Evaluada" if lang == 'ES' else "Evaluated Force", 'B', 'C'),
        ("Ponderación Sectorial (Wk)" if lang == 'ES' else "Industry Weight (Wk)", 'D', 'D'),
        ("Puntuación Fuerza (Fk)" if lang == 'ES' else "Force Score (Fk)", 'E', 'E'),
        ("Impacto Ponderado" if lang == 'ES' else "Weighted Impact", 'F', 'F'),
        ("Diagnóstico Estratégico" if lang == 'ES' else "Strategic Diagnosis", 'G', 'H')
    ]
    for h_txt, c_s, c_e in summary_cols:
        if c_s != c_e:
            ws.merge_cells(f"{c_s}{current_row}:{c_e}{current_row}")
        ws[f"{c_s}{current_row}"] = h_txt
        ws[f"{c_s}{current_row}"].font = styles['header_font']
        ws[f"{c_s}{current_row}"].fill = styles['header_fill']
        ws[f"{c_s}{current_row}"].alignment = styles['align_center']
        style_merged_range(ws, f"{c_s}{current_row}:{c_e}{current_row}", border=styles['header_border'])

    current_row += 1
    sum_start = current_row

    # Filas que apuntan a los subtotales de cada fuerza
    # F1 subtotal row: 11, F2: 19, F3: 27, F4: 35, F5: 43
    # Let's verify exact row numbers:
    # F1 header is row 4, cols row 5, subs 6,7,8,9,10 -> subtotal row 11.
    # next current_row is 11 + 2 = 13.
    # F2 header is row 13, cols 14, subs 15,16,17,18,19 -> subtotal row 20.
    # next current_row is 20 + 2 = 22.
    # F3 header is row 22, cols 23, subs 24,25,26,27,28 -> subtotal row 29.
    # next current_row is 29 + 2 = 31.
    # F4 header is row 31, cols 32, subs 33,34,35,36,37 -> subtotal row 38.
    # next current_row is 38 + 2 = 40.
    # F5 header is row 40, cols 41, subs 42,43,44,45 -> subtotal row 46 (subfactors has 4 items).
    # wait, let's keep exact row indices dynamically!

    # Para ser 100% exactos y robustos, calculamos las filas exactas donde se crearon los subtotales:
    # F1 subtotal row: 11 (macro_w en H4)
    # F2 subtotal row: 20 (macro_w en H13)
    # F3 subtotal row: 29 (macro_w en H22)
    # F4 subtotal row: 38 (macro_w en H31)
    # F5 subtotal row: 46 (macro_w en H40)
    forces_sub_refs = [
        ("F1: Rivalidad Competitiva" if lang == 'ES' else "F1: Competitive Rivalry", "H4", "F11"),
        ("F2: Poder de Proveedores" if lang == 'ES' else "F2: Supplier Power", "H13", "F20"),
        ("F3: Poder de Clientes" if lang == 'ES' else "F3: Buyer Power", "H22", "F29"),
        ("F4: Nuevos Entrantes" if lang == 'ES' else "F4: New Entrants", "H31", "F38"),
        ("F5: Productos Sustitutos" if lang == 'ES' else "F5: Substitutes", "H40", "F46"),
    ]

    for f_label, w_ref, score_ref in forces_sub_refs:
        ws.merge_cells(f"B{current_row}:C{current_row}")
        ws[f"B{current_row}"] = f_label
        ws[f"B{current_row}"].font = styles['cell_bold']
        ws[f"B{current_row}"].fill = styles['calc_fill']
        ws[f"B{current_row}"].alignment = styles['align_left']
        style_merged_range(ws, f"B{current_row}:C{current_row}", border=styles['thin_border'])

        ws[f"D{current_row}"] = f"={w_ref}"
        ws[f"D{current_row}"].font = styles['cell_font']
        ws[f"D{current_row}"].fill = styles['calc_fill']
        ws[f"D{current_row}"].alignment = styles['align_center']
        ws[f"D{current_row}"].border = styles['thin_border']
        ws[f"D{current_row}"].number_format = styles['num_fmt_pct']

        ws[f"E{current_row}"] = f"={score_ref}"
        ws[f"E{current_row}"].font = styles['cell_bold']
        ws[f"E{current_row}"].fill = styles['calc_fill']
        ws[f"E{current_row}"].alignment = styles['align_center']
        ws[f"E{current_row}"].border = styles['thin_border']
        ws[f"E{current_row}"].number_format = styles['num_fmt_dec']

        ws[f"F{current_row}"] = f"=D{current_row}*E{current_row}"
        ws[f"F{current_row}"].font = styles['cell_bold']
        ws[f"F{current_row}"].fill = styles['calc_fill']
        ws[f"F{current_row}"].alignment = styles['align_center']
        ws[f"F{current_row}"].border = styles['thin_border']
        ws[f"F{current_row}"].number_format = styles['num_fmt_dec']

        ws.merge_cells(f"G{current_row}:H{current_row}")
        ws[f"G{current_row}"] = f'=IF(E{current_row}>=3.8,"Severa / Foco Prioritario",IF(E{current_row}>=2.8,"Moderada","Controlada"))' if lang == 'ES' else f'=IF(E{current_row}>=3.8,"Severe / Priority Moat Focus",IF(E{current_row}>=2.8,"Moderate","Controlled"))'
        ws[f"G{current_row}"].font = styles['cell_font']
        ws[f"G{current_row}"].fill = styles['calc_fill']
        ws[f"G{current_row}"].alignment = styles['align_center']
        style_merged_range(ws, f"G{current_row}:H{current_row}", border=styles['thin_border'])

        current_row += 1

    sum_end = current_row - 1

    # Fila final de consolidación
    ws.merge_cells(f"B{current_row}:C{current_row}")
    ws[f"B{current_row}"] = "TOTAL INTENSIDAD COMPETITIVA (I_comp)" if lang == 'ES' else "TOTAL COMPETITIVE INTENSITY (I_comp)"
    ws[f"B{current_row}"].font = styles['cell_bold']
    ws[f"B{current_row}"].fill = styles['total_fill']
    ws[f"B{current_row}"].alignment = styles['align_left']
    style_merged_range(ws, f"B{current_row}:C{current_row}", border=styles['total_border'])

    ws[f"D{current_row}"] = f"=SUM(D{sum_start}:D{sum_end})"
    ws[f"D{current_row}"].font = styles['cell_bold']
    ws[f"D{current_row}"].fill = styles['total_fill']
    ws[f"D{current_row}"].alignment = styles['align_center']
    ws[f"D{current_row}"].border = styles['total_border']
    ws[f"D{current_row}"].number_format = styles['num_fmt_pct']

    ws[f"E{current_row}"] = f"=AVERAGE(E{sum_start}:E{sum_end})"
    ws[f"E{current_row}"].font = styles['cell_font']
    ws[f"E{current_row}"].fill = styles['total_fill']
    ws[f"E{current_row}"].alignment = styles['align_center']
    ws[f"E{current_row}"].border = styles['total_border']
    ws[f"E{current_row}"].number_format = styles['num_fmt_dec']

    ws[f"F{current_row}"] = f"=SUM(F{sum_start}:F{sum_end})"
    ws[f"F{current_row}"].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws[f"F{current_row}"].fill = styles['total_fill']
    ws[f"F{current_row}"].alignment = styles['align_center']
    ws[f"F{current_row}"].border = styles['total_border']
    ws[f"F{current_row}"].number_format = styles['num_fmt_dec']

    # Fila final G:H tiene el resultado de Intensidad Competitiva para el Dashboard
    ws.merge_cells(f"G{current_row}:H{current_row}")
    ws[f"G{current_row}"] = f"=F{current_row}"
    ws[f"G{current_row}"].font = Font(name='Segoe UI', size=12, bold=True, color=COLOR_NAVY_DARK)
    ws[f"G{current_row}"].fill = PatternFill(start_color=COLOR_F1_BG, end_color=COLOR_F1_BG, fill_type='solid')
    ws[f"G{current_row}"].alignment = styles['align_center']
    style_merged_range(ws, f"G{current_row}:H{current_row}", border=styles['total_border'])
    ws[f"G{current_row}"].number_format = styles['num_fmt_dec']

    # Guardamos la fila donde se ubica el resultado final de Intensidad Competitiva:
    # Esta fila es current_row (ej: fila 55)

    # Anchos de columna en Evaluación
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 46
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 16
    ws.column_dimensions['G'].width = 52
    ws.column_dimensions['H'].width = 18

    apply_sheet_protection(ws)
    return current_row  # Devuelve la fila del total


# ==============================================================================
# PESTAÑA 3: MATRIZ ATRACTIVO VS MOAT
# ==============================================================================
def build_tab3_moat_matrix(wb, lang='ES'):
    tab_name = "Matriz Atractivo vs Moat" if lang == 'ES' else "Attractiveness & Moat Matrix"
    ws = wb.create_sheet(title=tab_name)
    ws.views.sheetView[0].showGridLines = True
    styles = get_base_styles(lang)

    t_dash = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    t_eval = "Evaluación 5 Fuerzas" if lang == 'ES' else "5 Forces Assessment"

    # Banner
    ws.merge_cells('B1:H1')
    ws['B1'] = "DATALARIA | MATRIZ DE ATRACTIVO DE INDUSTRIA VS FORTALEZA DEL MOAT" if lang == 'ES' else "DATALARIA | INDUSTRY ATTRACTIVENESS VS ECONOMIC MOAT MATRIX"
    ws['B1'].font = styles['title_font']
    ws['B1'].fill = styles['title_fill']
    ws['B1'].alignment = styles['align_center']

    ws.merge_cells('B2:H2')
    ws['B2'] = "Diagnóstico cartesiano de la posición estratégica corporativa frente a las fuerzas estructurales del sector" if lang == 'ES' else "Cartesian strategic diagnosis of corporate advantage against structural industry forces"
    ws['B2'].font = styles['subtitle_font']
    ws['B2'].fill = styles['title_fill']
    ws['B2'].alignment = styles['align_center']
    ws.row_dimensions[1].height = 24

    # SECCIÓN 1: EVALUACIÓN DEL MOAT / FOSO DEFENSIVO (B4:H15)
    ws.merge_cells('B4:H4')
    ws['B4'] = "1. DIAGNÓSTICO DE BLINDAJE INTERNO (ECONOMIC MOAT ASSESSMENT)" if lang == 'ES' else "1. INTERNAL ECONOMIC MOAT ASSESSMENT"
    ws['B4'].font = styles['section_font']
    ws['B4'].fill = styles['section_fill']
    ws['B4'].alignment = styles['align_left']

    moat_headers = [
        ("ID", 'B', 8),
        ("Pilar de Ventaja Competitiva Defendible (Moat)" if lang == 'ES' else "Defendable Moat Advantage Pillar", 'C', 42),
        ("Ponderación" if lang == 'ES' else "Weight", 'D', 14),
        ("Nivel (1-5)" if lang == 'ES' else "Score (1-5)", 'E', 14),
        ("Puntuación" if lang == 'ES' else "Weighted", 'F', 16),
        ("Evidencia Operativa y Barrera Creada" if lang == 'ES' else "Operational Evidence & Defendable Moat", 'G', 45),
        ("Estado" if lang == 'ES' else "Moat Status", 'H', 18)
    ]

    for h_txt, col, w in moat_headers:
        ws[f"{col}5"] = h_txt
        ws[f"{col}5"].font = styles['header_font']
        ws[f"{col}5"].fill = styles['header_fill']
        ws[f"{col}5"].alignment = styles['align_center'] if col in ['B', 'D', 'E', 'F', 'H'] else styles['align_left']
        ws[f"{col}5"].border = styles['header_border']

    moat_data = [
        ("M1",
         "Costes de Cambio de Clientes (Switching Costs)" if lang == 'ES' else "Customer Switching Costs (Friction & Locks)",
         0.25, 4.0,
         "Integración técnica profunda vía API y bases de datos en los clientes" if lang == 'ES' else "Deep technical workflow integration via APIs and ERP connectors"),

        ("M2",
         "Efectos de Red Directos e Indirectos (Network Effects)" if lang == 'ES' else "Direct & Indirect Network Effects",
         0.20, 3.5,
         "Comunidad activa y base de usuarios con feedback acumulado" if lang == 'ES' else "Growing active user base and accumulated workflow templates"),

        ("M3",
         "Activos Intangibles: Patentes, Algoritmos y Marca" if lang == 'ES' else "Intangibles: Patents, Proprietary Tech & Brand",
         0.20, 4.0,
         "2 patentes concedidas, marca reconocida y reputación técnica B2B" if lang == 'ES' else "2 granted utility patents, recognized brand and B2B reputation"),

        ("M4",
         "Ventaja en Estructura de Costes (Cost Advantage / Scale)" if lang == 'ES' else "Cost Advantage & Scale Efficiencies",
         0.20, 3.5,
         "Automatización operativa y curva de aprendizaje de costes unitarios (-18%)" if lang == 'ES' else "High process automation yielding -18% unit cost advantage"),

        ("M5",
         "Velocidad de Innovación & Cultura de Ejecución (Execution Moat)" if lang == 'ES' else "Innovation Velocity & Execution Culture",
         0.15, 4.5,
         "Ciclos de entrega de nuevas funcionalidades 3x más rápidos que los incumbentes" if lang == 'ES' else "Feature delivery cycles 3x faster than legacy incumbents")
    ]

    for idx, (m_id, m_name, m_w, m_rate, m_evid) in enumerate(moat_data, start=6):
        ws[f"B{idx}"] = m_id
        ws[f"B{idx}"].font = styles['code_font']
        ws[f"B{idx}"].alignment = styles['align_center']
        ws[f"B{idx}"].fill = styles['calc_fill']
        ws[f"B{idx}"].border = styles['thin_border']

        ws[f"C{idx}"] = m_name
        ws[f"C{idx}"].font = styles['cell_bold']
        ws[f"C{idx}"].alignment = styles['align_left_wrap']
        ws[f"C{idx}"].fill = styles['input_fill']
        ws[f"C{idx}"].border = styles['thin_border']
        ws[f"C{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"D{idx}"] = m_w
        ws[f"D{idx}"].font = styles['cell_font']
        ws[f"D{idx}"].alignment = styles['align_center']
        ws[f"D{idx}"].fill = styles['input_fill']
        ws[f"D{idx}"].border = styles['thin_border']
        ws[f"D{idx}"].number_format = styles['num_fmt_pct']
        ws[f"D{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"E{idx}"] = m_rate
        ws[f"E{idx}"].font = styles['cell_bold']
        ws[f"E{idx}"].alignment = styles['align_center']
        ws[f"E{idx}"].fill = styles['input_fill']
        ws[f"E{idx}"].border = styles['thin_border']
        ws[f"E{idx}"].number_format = styles['num_fmt_dec']
        ws[f"E{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"F{idx}"] = f"=D{idx}*E{idx}"
        ws[f"F{idx}"].font = styles['cell_bold']
        ws[f"F{idx}"].alignment = styles['align_center']
        ws[f"F{idx}"].fill = styles['calc_fill']
        ws[f"F{idx}"].border = styles['thin_border']
        ws[f"F{idx}"].number_format = styles['num_fmt_dec']

        ws[f"G{idx}"] = m_evid
        ws[f"G{idx}"].font = styles['cell_font']
        ws[f"G{idx}"].alignment = styles['align_left_wrap']
        ws[f"G{idx}"].fill = styles['input_fill']
        ws[f"G{idx}"].border = styles['thin_border']
        ws[f"G{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"H{idx}"] = f'=IF(E{idx}>=4,"Foso Fuerte",IF(E{idx}>=3,"Ventaja Media","Brecha Débil"))' if lang == 'ES' else f'=IF(E{idx}>=4,"Strong Moat",IF(E{idx}>=3,"Moderate Advantage","Vulnerable"))'
        ws[f"H{idx}"] = f'=IF(E{idx}>=4,"Foso Fuerte",IF(E{idx}>=3,"Ventaja Media","Brecha Débil"))' if lang == 'ES' else f'=IF(E{idx}>=4,"Strong Moat",IF(E{idx}>=3,"Moderate Advantage","Vulnerable"))'
        ws[f"H{idx}"].font = styles['cell_font']
        ws[f"H{idx}"].alignment = styles['align_center']
        ws[f"H{idx}"].fill = styles['calc_fill']
        ws[f"H{idx}"].border = styles['thin_border']

    # Fila Total Moat
    ws['B11'] = "TOTAL"
    ws['B11'].font = styles['cell_bold']
    ws['B11'].alignment = styles['align_center']
    ws['B11'].fill = styles['total_fill']
    ws['B11'].border = styles['total_border']

    ws['C11'] = "Índice Global de Fortaleza del Moat" if lang == 'ES' else "Overall Economic Moat Strength Index"
    ws['C11'].font = styles['cell_bold']
    ws['C11'].alignment = styles['align_left']
    ws['C11'].fill = styles['total_fill']
    ws['C11'].border = styles['total_border']

    ws['D11'] = "=SUM(D6:D10)"
    ws['D11'].font = styles['cell_bold']
    ws['D11'].alignment = styles['align_center']
    ws['D11'].fill = styles['total_fill']
    ws['D11'].border = styles['total_border']
    ws['D11'].number_format = styles['num_fmt_pct']

    ws['E11'] = "=AVERAGE(E6:E10)"
    ws['E11'].font = styles['cell_font']
    ws['E11'].alignment = styles['align_center']
    ws['E11'].fill = styles['total_fill']
    ws['E11'].border = styles['total_border']
    ws['E11'].number_format = styles['num_fmt_dec']

    ws['F11'] = "=SUM(F6:F10)"
    ws['F11'].font = Font(name='Segoe UI', size=12, bold=True, color=COLOR_EMERALD_ACCENT)
    ws['F11'].alignment = styles['align_center']
    ws['F11'].fill = styles['total_fill']
    ws['F11'].border = styles['total_border']
    ws['F11'].number_format = styles['num_fmt_dec']

    ws['G11'] = f'=IF(F11>=3.5,"FOSO DEFENDIBLE SÓLIDO",IF(F11>=2.5,"VENTAJA MODERADA","VULNERABILIDAD ALTA"))' if lang == 'ES' else f'=IF(F11>=3.5,"STRONG DEFENSIVE MOAT",IF(F11>=2.5,"MODERATE ADVANTAGE","HIGH VULNERABILITY"))'
    ws['G11'].font = styles['cell_bold']
    ws['G11'].alignment = styles['align_center']
    ws['G11'].fill = styles['total_fill']
    ws['G11'].border = styles['total_border']

    ws['H11'] = "=F11"
    ws['H11'].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_EMERALD_ACCENT)
    ws['H11'].alignment = styles['align_center']
    ws['H11'].fill = PatternFill(start_color=COLOR_MOAT_BG, end_color=COLOR_MOAT_BG, fill_type='solid')
    ws['H11'].border = styles['total_border']
    ws['H11'].number_format = styles['num_fmt_dec']

    # Fila 15 de referencia para el Dashboard (F15 o F11)
    # Para consistencia con la fórmula del Dashboard f"='{t_moat}'!F15":
    # Colocamos una tarjeta resumen en B14:H15
    ws.merge_cells('B14:D14')
    ws['B14'] = "MÉTRICA CLAVE" if lang == 'ES' else "KEY METRIC"
    ws['B14'].font = styles['header_font']
    ws['B14'].fill = styles['header_fill']
    ws['B14'].alignment = styles['align_center']

    ws.merge_cells('E14:F14')
    ws['E14'] = "VALOR CONSOLIDADO" if lang == 'ES' else "CONSOLIDATED VALUE"
    ws['E14'].font = styles['header_font']
    ws['E14'].fill = styles['header_fill']
    ws['E14'].alignment = styles['align_center']

    ws.merge_cells('G14:H14')
    ws['G14'] = "VEREDICTO ESTRATÉGICO" if lang == 'ES' else "STRATEGIC VERDICT"
    ws['G14'].font = styles['header_font']
    ws['G14'].fill = styles['header_fill']
    ws['G14'].alignment = styles['align_center']

    ws.merge_cells('B15:D15')
    ws['B15'] = "Índice de Fortaleza del Foso Defensivo (Moat)" if lang == 'ES' else "Economic Moat Strength Index"
    ws['B15'].font = styles['cell_bold']
    ws['B15'].fill = styles['calc_fill']
    ws['B15'].alignment = styles['align_left']
    style_merged_range(ws, 'B15:D15', border=styles['thin_border'])

    ws.merge_cells('E15:F15')
    ws['E15'] = "=F11"
    ws['E15'].font = Font(name='Segoe UI', size=14, bold=True, color=COLOR_EMERALD_ACCENT)
    ws['E15'].fill = PatternFill(start_color=COLOR_MOAT_BG, end_color=COLOR_MOAT_BG, fill_type='solid')
    ws['E15'].alignment = styles['align_center']
    ws['E15'].number_format = styles['num_fmt_dec']
    style_merged_range(ws, 'E15:F15', border=styles['thin_border'])

    ws.merge_cells('G15:H15')
    ws['G15'] = "=G11"
    ws['G15'].font = styles['cell_bold']
    ws['G15'].fill = styles['calc_fill']
    ws['G15'].alignment = styles['align_center']
    style_merged_range(ws, 'G15:H15', border=styles['thin_border'])

    # SECCIÓN 2: MATRIZ CARTESIANA ATRACTIVO VS MOAT (B18:H26)
    ws.merge_cells('B18:H18')
    ws['B18'] = "2. CRUCE CARTESIANO: ATRACTIVO DE INDUSTRIA VS FORTALEZA DEL MOAT" if lang == 'ES' else "2. CARTESIAN MATRIX: INDUSTRY ATTRACTIVENESS VS ECONOMIC MOAT"
    ws['B18'].font = styles['section_font']
    ws['B18'].fill = styles['section_fill']
    ws['B18'].alignment = styles['align_left']

    # Coordenadas
    ws.merge_cells('B19:C19')
    ws['B19'] = "Eje X: Atractivo Estructural (A_ind = 5 - I_comp)" if lang == 'ES' else "X-Axis: Industry Attractiveness (A_ind = 5 - I_comp)"
    ws['B19'].font = styles['cell_bold']
    ws['B19'].fill = styles['calc_fill']
    ws['B19'].alignment = styles['align_left']
    style_merged_range(ws, 'B19:C19', border=styles['thin_border'])

    ws['D19'] = f"='{t_dash}'!E6"
    ws['D19'].font = Font(name='Segoe UI', size=12, bold=True, color=COLOR_BLUE_ACCENT)
    ws['D19'].fill = styles['calc_fill']
    ws['D19'].alignment = styles['align_center']
    ws['D19'].border = styles['thin_border']
    ws['D19'].number_format = styles['num_fmt_dec']

    ws.merge_cells('E19:G19')
    ws['E19'] = f'=IF(D19>=2,"Atractivo Alto / Favorable","Atractivo Bajo / Hostil")' if lang == 'ES' else f'=IF(D19>=2,"High Attractiveness / Favorable","Low Attractiveness / Hostile")'
    ws['E19'].font = styles['cell_bold']
    ws['E19'].fill = styles['calc_fill']
    ws['E19'].alignment = styles['align_center']
    style_merged_range(ws, 'E19:G19', border=styles['thin_border'])

    ws['H19'] = "Eje Horizontal" if lang == 'ES' else "Horizontal Axis"
    ws['H19'].font = styles['subtitle_font']
    ws['H19'].fill = styles['calc_fill']
    ws['H19'].alignment = styles['align_center']
    ws['H19'].border = styles['thin_border']

    ws.merge_cells('B20:C20')
    ws['B20'] = "Eje Y: Fortaleza del Moat Interno (M)" if lang == 'ES' else "Y-Axis: Internal Economic Moat Strength (M)"
    ws['B20'].font = styles['cell_bold']
    ws['B20'].fill = styles['calc_fill']
    ws['B20'].alignment = styles['align_left']
    style_merged_range(ws, 'B20:C20', border=styles['thin_border'])

    ws['D20'] = "=E15"
    ws['D20'].font = Font(name='Segoe UI', size=12, bold=True, color=COLOR_EMERALD_ACCENT)
    ws['D20'].fill = styles['calc_fill']
    ws['D20'].alignment = styles['align_center']
    ws['D20'].border = styles['thin_border']
    ws['D20'].number_format = styles['num_fmt_dec']

    ws.merge_cells('E20:G20')
    ws['E20'] = f'=IF(D20>=3,"Moat Fuerte / Defendible","Moat Débil / Vulnerable")' if lang == 'ES' else f'=IF(D20>=3,"Strong / Defendable Moat","Weak / Vulnerable Moat")'
    ws['E20'].font = styles['cell_bold']
    ws['E20'].fill = styles['calc_fill']
    ws['E20'].alignment = styles['align_center']
    style_merged_range(ws, 'E20:G20', border=styles['thin_border'])

    ws['H20'] = "Eje Vertical" if lang == 'ES' else "Vertical Axis"
    ws['H20'].font = styles['subtitle_font']
    ws['H20'].fill = styles['calc_fill']
    ws['H20'].alignment = styles['align_center']
    ws['H20'].border = styles['thin_border']

    # Cuadrantes explicativos
    q_headers = [
        ("Cuadrante Estratégico" if lang == 'ES' else "Strategic Quadrant", 'B', 'C'),
        ("Condición Vectorial" if lang == 'ES' else "Vector Condition", 'D', 'D'),
        ("Postura Estratégica Sugerida" if lang == 'ES' else "Suggested Strategic Posture", 'E', 'F'),
        ("Directriz de Asignación de Capital" if lang == 'ES' else "Capital Allocation Directive", 'G', 'H')
    ]
    for h_txt, c_s, c_e in q_headers:
        if c_s != c_e:
            ws.merge_cells(f"{c_s}22:{c_e}22")
        ws[f"{c_s}22"] = h_txt
        ws[f"{c_s}22"].font = styles['header_font']
        ws[f"{c_s}22"].fill = styles['header_fill']
        ws[f"{c_s}22"].alignment = styles['align_center']
        style_merged_range(ws, f"{c_s}22:{c_e}22", border=styles['header_border'])

    quadrants = [
        ("CUADRANTE I: LÍDER ESTRATÉGICO" if lang == 'ES' else "QUADRANT I: STRATEGIC LEADER",
         "A_ind ≥ 2 & Moat ≥ 3",
         "LIDERAZGO Y EXPANSIÓN AGRESIVA" if lang == 'ES' else "LEADERSHIP & AGGRESSIVE REINVESTMENT",
         "Invertir agresivamente en escala, I+D y captura de cuota. Margen muy defendible." if lang == 'ES' else "Invest aggressively in scale, R&D and market share. High ROIC."),

        ("CUADRANTE II: BASTIÓN DEFENSIVO" if lang == 'ES' else "QUADRANT II: DEFENSIVE FORTRESS",
         "A_ind < 2 & Moat ≥ 3",
         "COSECHA DE CAJA Y BLINDAJE DE FOSO" if lang == 'ES' else "CASH GENERATION & MOAT REINFORCEMENT",
         "Proteger márgenes vía costes de cambio. Maximizar dividendos y flujo de caja libre." if lang == 'ES' else "Protect margins via switching costs. Maximize FCF generation and dividends."),

        ("CUADRANTE III: TERRENO EN DISPUTA" if lang == 'ES' else "QUADRANT III: CONTESTED GROUND",
         "A_ind ≥ 2 & Moat < 3",
         "CONSTRUCCIÓN URGENTE DE BARRERAS" if lang == 'ES' else "URGENT BARRIER BUILDING & DIFFERENTIATION",
         "Sector atractivo pero empresa vulnerable. Asignar CAPEX a patentes y fidelización." if lang == 'ES' else "Attractive industry but vulnerable firm. Urgently build IP & customer lock-in."),

        ("CUADRANTE IV: TRAMPA DE VALOR" if lang == 'ES' else "QUADRANT IV: VALUE TRAP",
         "A_ind < 2 & Moat < 3",
         "DESINVERSIÓN O ENFOQUE EN HIPER-NICHO" if lang == 'ES' else "DIVESTMENT OR HYPER-NICHE PIVOT",
         "Sector hostil sin foso defensivo. Evitar CAPEX expansivo. Reorientar a micro-nicho." if lang == 'ES' else "Hostile sector with no moat. Avoid growth capex. Harvest or pivot to niche.")
    ]

    for q_idx, (q_name, q_cond, q_post, q_dir) in enumerate(quadrants, start=23):
        ws.merge_cells(f"B{q_idx}:C{q_idx}")
        ws[f"B{q_idx}"] = q_name
        ws[f"B{q_idx}"].font = styles['cell_bold']
        ws[f"B{q_idx}"].fill = styles['calc_fill']
        ws[f"B{q_idx}"].alignment = styles['align_left']
        style_merged_range(ws, f"B{q_idx}:C{q_idx}", border=styles['thin_border'])

        ws[f"D{q_idx}"] = q_cond
        ws[f"D{q_idx}"].font = styles['code_font']
        ws[f"D{q_idx}"].fill = styles['calc_fill']
        ws[f"D{q_idx}"].alignment = styles['align_center']
        ws[f"D{q_idx}"].border = styles['thin_border']

        ws.merge_cells(f"E{q_idx}:F{q_idx}")
        ws[f"E{q_idx}"] = q_post
        ws[f"E{q_idx}"].font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"E{q_idx}"].fill = styles['calc_fill']
        ws[f"E{q_idx}"].alignment = styles['align_center']
        style_merged_range(ws, f"E{q_idx}:F{q_idx}", border=styles['thin_border'])

        ws.merge_cells(f"G{q_idx}:H{q_idx}")
        ws[f"G{q_idx}"] = q_dir
        ws[f"G{q_idx}"].font = styles['cell_font']
        ws[f"G{q_idx}"].fill = styles['calc_fill']
        ws[f"G{q_idx}"].alignment = styles['align_left_wrap']
        style_merged_range(ws, f"G{q_idx}:H{q_idx}", border=styles['thin_border'])

    # Fila 27: Diagnóstico Activo de la Compañía (Referenciado en Dashboard K6 y K7)
    ws.merge_cells('B27:C27')
    ws['B27'] = "DIAGNÓSTICO VIGENTE:" if lang == 'ES' else "CURRENT DIAGNOSIS:"
    ws['B27'].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_NAVY_DARK)
    ws['B27'].fill = PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid')
    ws['B27'].alignment = styles['align_center']
    style_merged_range(ws, 'B27:C27', border=styles['total_border'])

    ws.merge_cells('D27:H27')
    ws['D27'] = f'=IF(AND(D19>=2,D20>=3),"CUADRANTE I: LÍDER ESTRATÉGICO (Expansión & Escala)",IF(AND(D19<2,D20>=3),"CUADRANTE II: BASTIÓN DEFENSIVO (Blindaje de Foso & Flujo de Caja)",IF(AND(D19>=2,D20<3),"CUADRANTE III: TERRENO EN DISPUTA (Construcción Urgente de Barreras)","CUADRANTE IV: TRAMPA DE VALOR (Desinversión o Micro-Nicho)")))' if lang == 'ES' else f'=IF(AND(D19>=2,D20>=3),"QUADRANT I: STRATEGIC LEADER (Aggressive Expansion)",IF(AND(D19<2,D20>=3),"QUADRANT II: DEFENSIVE FORTRESS (Moat Shielding & FCF Harvest)",IF(AND(D19>=2,D20<3),"QUADRANT III: CONTESTED GROUND (Urgent Barrier Building)","QUADRANT IV: VALUE TRAP (Divestment or Hyper-Niche)")))'
    ws['D27'].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws['D27'].fill = PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid')
    ws['D27'].alignment = styles['align_center']
    style_merged_range(ws, 'D27:H27', border=styles['total_border'])

    # Column dimensions
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 44
    ws.column_dimensions['D'].width = 16
    ws.column_dimensions['E'].width = 16
    ws.column_dimensions['F'].width = 18
    ws.column_dimensions['G'].width = 46
    ws.column_dimensions['H'].width = 20

    apply_sheet_protection(ws)


# ==============================================================================
# PESTAÑA 4: PLAN DE BLINDAJE ESTRATÉGICO
# ==============================================================================
def build_tab4_action_plan(wb, lang='ES'):
    tab_name = "Plan de Blindaje Estratégico" if lang == 'ES' else "Strategic Moat Action Plan"
    ws = wb.create_sheet(title=tab_name)
    ws.views.sheetView[0].showGridLines = True
    styles = get_base_styles(lang)

    # Banner
    ws.merge_cells('B1:K1')
    ws['B1'] = "DATALARIA | PLAN DE BLINDAJE ESTRATÉGICO Y RESOLUCIONES PARA CONSEJO DE ADMINISTRACIÓN" if lang == 'ES' else "DATALARIA | STRATEGIC MOAT ACTION PLAN & BOARD OF DIRECTORS RESOLUTIONS"
    ws['B1'].font = styles['title_font']
    ws['B1'].fill = styles['title_fill']
    ws['B1'].alignment = styles['align_center']

    ws.merge_cells('B2:K2')
    ws['B2'] = "Asignación formal de CAPEX, OPEX, Sponsors C-Level y KPIs para neutralizar las fuerzas de mayor severidad" if lang == 'ES' else "Formal allocation of CAPEX, OPEX, C-Suite Sponsors and KPIs to mitigate highest severity forces"
    ws['B2'].font = styles['subtitle_font']
    ws['B2'].fill = styles['title_fill']
    ws['B2'].alignment = styles['align_center']
    ws.row_dimensions[1].height = 24

    headers = [
        ("ID", 'B', 10),
        ("Fuerza Mitigada" if lang == 'ES' else "Mitigated Force", 'C', 18),
        ("Iniciativa Estratégica de Blindaje" if lang == 'ES' else "Strategic Moat Initiative", 'D', 44),
        ("Tipo de Barrera Creada" if lang == 'ES' else "Moat Barrier Type", 'E', 28),
        ("Owner C-Level" if lang == 'ES' else "C-Level Owner", 'F', 16),
        ("Plazo" if lang == 'ES' else "Timeline", 'G', 14),
        ("CAPEX (€)" if lang == 'ES' else "CAPEX ($)", 'H', 18),
        ("OPEX Anual (€)" if lang == 'ES' else "Annual OPEX ($)", 'I', 18),
        ("KPI de Impacto" if lang == 'ES' else "Target Impact KPI", 'J', 32),
        ("Impacto Margen EBITDA" if lang == 'ES' else "EBITDA Margin Impact", 'K', 24)
    ]

    for h_txt, col, w in headers:
        ws[f"{col}4"] = h_txt
        ws[f"{col}4"].font = styles['header_font']
        ws[f"{col}4"].fill = styles['header_fill']
        ws[f"{col}4"].alignment = styles['align_center'] if col in ['B', 'C', 'F', 'G', 'H', 'I'] else styles['align_left']
        ws[f"{col}4"].border = styles['header_border']

    initiatives = [
        ("INI-01", "F3: Clientes",
         "Programa de Integración de Flujos de Trabajo y Conectores ERP propietarios" if lang == 'ES' else "Proprietary ERP Workflow Integration & Connector Suite",
         "Costes de Cambio (Switching Costs)" if lang == 'ES' else "Switching Costs Lock-in",
         "CTO", "Q1-Q2", 140000, 35000,
         "Churn de Grandes Cuentas < 2.5%" if lang == 'ES' else "Key Account Churn < 2.5%",
         "+1.2% EBITDA"),

        ("INI-02", "F1: Rivalidad",
         "Especialización en Soluciones Verticales de Alto Valor Añadido" if lang == 'ES' else "High-Value Vertical Industry Specialized Solutions",
         "Diferenciación & Poder de Precios" if lang == 'ES' else "Product Differentiation & Pricing Power",
         "CMO", "Q2-Q3", 95000, 48000,
         "Net Promoter Score (NPS) > 65 pts" if lang == 'ES' else "Net Promoter Score (NPS) > 65 pts",
         "+1.5% EBITDA"),

        ("INI-03", "F5: Sustitutos",
         "Módulo Nativo de Automatización e Inteligencia Artificial embebida" if lang == 'ES' else "Native Embedded AI & Workflow Automation Module",
         "Activos Intangibles / Tecnología Propietaria" if lang == 'ES' else "Proprietary Tech & Speed Moat",
         "VP Product", "Q1-Q3", 185000, 52000,
         "Ratio de Adopción de Features IA > 60%" if lang == 'ES' else "AI Feature Adoption Rate > 60%",
         "+0.8% EBITDA"),

        ("INI-04", "F2: Proveedores",
         "Dual Sourcing Estratégico y Homologación de Proveedores Alternativos" if lang == 'ES' else "Strategic Dual Sourcing & Alternative Vendor Qualification",
         "Poder de Negociación de Compras" if lang == 'ES' else "Supplier Bargaining Power Mitigation",
         "COO", "Q2-Q4", 60000, 20000,
         "Ahorro de Compras COGS -8.5%" if lang == 'ES' else "Direct COGS Sourcing Savings -8.5%",
         "+0.9% EBITDA"),

        ("INI-05", "F4: Nuevos Entrantes",
         "Registro de Propiedad Intelectual y Certificaciones de Seguridad ISO 27001" if lang == 'ES' else "Intellectual Property Filings & Enterprise ISO 27001 Audits",
         "Barreras Regulatorias y de Confianza" if lang == 'ES' else "Regulatory & Trust Entry Barriers",
         "CFO / Legal", "Q1-Q2", 45000, 15000,
         "Cierre de Auditorías Enterprise al 100%" if lang == 'ES' else "100% Enterprise Security Sign-off",
         "+0.4% EBITDA"),

        ("INI-06", "F3: Clientes",
         "Contratos Marco Plurianuales con Bonificación por Volumen Acumulado" if lang == 'ES' else "Multi-Year Master Service Agreements with Volume Tiers",
         "Fidelización y Barrera Contractual" if lang == 'ES' else "Contractual Lock-in & Retention",
         "CEO", "Q1-Q4", 30000, 12000,
         "Revenue Recurrente (ARR) > 78%" if lang == 'ES' else "Annual Recurring Revenue (ARR) > 78%",
         "+0.7% EBITDA"),

        ("INI-07", "F5: Sustitutos",
         "Ecosistema Abierto de Plugins y Alianzas con Integradores de Sistemas" if lang == 'ES' else "Open Integration Ecosystem & Strategic SI Partnerships",
         "Efectos de Red Indirectos" if lang == 'ES' else "Indirect Network Effects Ecosystem",
         "VP Sales", "Q2-Q4", 75000, 30000,
         "25 Partners Certificados Activos" if lang == 'ES' else "25 Active Certified Integration Partners",
         "+0.5% EBITDA"),

        ("INI-08", "F1: Rivalidad",
         "Automatización de Operaciones Internas y Plataforma Self-Service" if lang == 'ES' else "End-to-End Operational Automation & Self-Service Portal",
         "Ventaja en Estructura de Costes (Escala)" if lang == 'ES' else "Operating Cost Efficiency & Scale",
         "COO / CTO", "Q3-Q4", 110000, 28000,
         "Reducción de Tiempo de Onboarding -45%" if lang == 'ES' else "Customer Onboarding Time -45%",
         "+0.6% EBITDA")
    ]

    for idx, (i_id, i_f, i_name, i_moat, i_own, i_time, i_capex, i_opex, i_kpi, i_ebitda) in enumerate(initiatives, start=5):
        ws[f"B{idx}"] = i_id
        ws[f"B{idx}"].font = styles['code_font']
        ws[f"B{idx}"].alignment = styles['align_center']
        ws[f"B{idx}"].fill = styles['calc_fill']
        ws[f"B{idx}"].border = styles['thin_border']

        ws[f"C{idx}"] = i_f
        ws[f"C{idx}"].font = styles['cell_bold']
        ws[f"C{idx}"].alignment = styles['align_center']
        ws[f"C{idx}"].fill = styles['input_fill']
        ws[f"C{idx}"].border = styles['thin_border']
        ws[f"C{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"D{idx}"] = i_name
        ws[f"D{idx}"].font = styles['cell_bold']
        ws[f"D{idx}"].alignment = styles['align_left_wrap']
        ws[f"D{idx}"].fill = styles['input_fill']
        ws[f"D{idx}"].border = styles['thin_border']
        ws[f"D{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"E{idx}"] = i_moat
        ws[f"E{idx}"].font = styles['cell_font']
        ws[f"E{idx}"].alignment = styles['align_left_wrap']
        ws[f"E{idx}"].fill = styles['input_fill']
        ws[f"E{idx}"].border = styles['thin_border']
        ws[f"E{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"F{idx}"] = i_own
        ws[f"F{idx}"].font = styles['cell_bold']
        ws[f"F{idx}"].alignment = styles['align_center']
        ws[f"F{idx}"].fill = styles['input_fill']
        ws[f"F{idx}"].border = styles['thin_border']
        ws[f"F{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"G{idx}"] = i_time
        ws[f"G{idx}"].font = styles['cell_font']
        ws[f"G{idx}"].alignment = styles['align_center']
        ws[f"G{idx}"].fill = styles['input_fill']
        ws[f"G{idx}"].border = styles['thin_border']
        ws[f"G{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"H{idx}"] = i_capex
        ws[f"H{idx}"].font = styles['cell_bold']
        ws[f"H{idx}"].alignment = styles['align_right']
        ws[f"H{idx}"].fill = styles['input_fill']
        ws[f"H{idx}"].border = styles['thin_border']
        ws[f"H{idx}"].number_format = styles['num_fmt_curr']
        ws[f"H{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"I{idx}"] = i_opex
        ws[f"I{idx}"].font = styles['cell_font']
        ws[f"I{idx}"].alignment = styles['align_right']
        ws[f"I{idx}"].fill = styles['input_fill']
        ws[f"I{idx}"].border = styles['thin_border']
        ws[f"I{idx}"].number_format = styles['num_fmt_curr']
        ws[f"I{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"J{idx}"] = i_kpi
        ws[f"J{idx}"].font = styles['cell_font']
        ws[f"J{idx}"].alignment = styles['align_left_wrap']
        ws[f"J{idx}"].fill = styles['input_fill']
        ws[f"J{idx}"].border = styles['thin_border']
        ws[f"J{idx}"].protection = Protection(locked=False)  # Editable

        ws[f"K{idx}"] = i_ebitda
        ws[f"K{idx}"].font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_EMERALD_ACCENT)
        ws[f"K{idx}"].alignment = styles['align_center']
        ws[f"K{idx}"].fill = styles['input_fill']
        ws[f"K{idx}"].border = styles['thin_border']
        ws[f"K{idx}"].protection = Protection(locked=False)  # Editable

    # Fila de Totales en Fila 13 (8 iniciativas de 5 a 12)
    # Para consistencia con la referencia en Dashboard ('Plan de Blindaje Estratégico'!G15+'Plan de Blindaje Estratégico'!H15),
    # Colocamos el Total en la fila 15 dejando la fila 14 como separador o cabecera
    tot_row = 15
    ws.merge_cells(f"B{tot_row}:G{tot_row}")
    ws[f"B{tot_row}"] = "PRESUPUESTO TOTAL CONSOLIDADO DE BLINDAJE ESTRATÉGICO" if lang == 'ES' else "CONSOLIDATED STRATEGIC MOAT BUDGET TOTAL"
    ws[f"B{tot_row}"].font = styles['cell_bold']
    ws[f"B{tot_row}"].fill = styles['total_fill']
    ws[f"B{tot_row}"].alignment = styles['align_left']
    style_merged_range(ws, f"B{tot_row}:G{tot_row}", border=styles['total_border'])

    ws[f"H{tot_row}"] = "=SUM(H5:H12)"
    ws[f"H{tot_row}"].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws[f"H{tot_row}"].fill = styles['total_fill']
    ws[f"H{tot_row}"].alignment = styles['align_right']
    ws[f"H{tot_row}"].border = styles['total_border']
    ws[f"H{tot_row}"].number_format = styles['num_fmt_curr']

    ws[f"I{tot_row}"] = "=SUM(I5:I12)"
    ws[f"I{tot_row}"].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws[f"I{tot_row}"].fill = styles['total_fill']
    ws[f"I{tot_row}"].alignment = styles['align_right']
    ws[f"I{tot_row}"].border = styles['total_border']
    ws[f"I{tot_row}"].number_format = styles['num_fmt_curr']

    ws[f"J{tot_row}"] = "8 Iniciativas Aprobadas" if lang == 'ES' else "8 Approved Initiatives"
    ws[f"J{tot_row}"].font = styles['cell_bold']
    ws[f"J{tot_row}"].fill = styles['total_fill']
    ws[f"J{tot_row}"].alignment = styles['align_center']
    ws[f"J{tot_row}"].border = styles['total_border']

    ws[f"K{tot_row}"] = "+6.6% EBITDA Total"
    ws[f"K{tot_row}"].font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_EMERALD_ACCENT)
    ws[f"K{tot_row}"].fill = styles['total_fill']
    ws[f"K{tot_row}"].alignment = styles['align_center']
    ws[f"K{tot_row}"].border = styles['total_border']

    # Column dimensions
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 11
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 46
    ws.column_dimensions['E'].width = 30
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 14
    ws.column_dimensions['H'].width = 20
    ws.column_dimensions['I'].width = 20
    ws.column_dimensions['J'].width = 34
    ws.column_dimensions['K'].width = 22

    apply_sheet_protection(ws)


def generate_workbook(lang='ES', out_dir='.'):
    wb = openpyxl.Workbook()
    os.makedirs(out_dir, exist_ok=True)

    filename = "Porter_5_Fuerzas_Datalaria_ES.xlsx" if lang == 'ES' else "Porter_5_Forces_Datalaria_EN.xlsx"
    out_path = os.path.join(out_dir, filename)

    print(f"[{lang}] Generando modelo Excel estratégico: {out_path}...")

    # Construir pestañas en orden de navegación C-Level
    build_tab1_dashboard(wb, lang=lang)
    build_tab2_assessment(wb, lang=lang)
    build_tab3_moat_matrix(wb, lang=lang)
    build_tab4_action_plan(wb, lang=lang)

    # Ajustar dimensiones de columnas en el Dashboard
    ws1 = wb["Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"]
    ws1.column_dimensions['A'].width = 3
    ws1.column_dimensions['B'].width = 8
    ws1.column_dimensions['C'].width = 34
    ws1.column_dimensions['D'].width = 20
    ws1.column_dimensions['E'].width = 18
    ws1.column_dimensions['F'].width = 22
    ws1.column_dimensions['G'].width = 38
    ws1.column_dimensions['H'].width = 16
    ws1.column_dimensions['I'].width = 16
    ws1.column_dimensions['J'].width = 16
    ws1.column_dimensions['K'].width = 16
    ws1.column_dimensions['L'].width = 16
    ws1.column_dimensions['M'].width = 18

    wb.save(out_path)
    print(f"[{lang}] OK: Archivo guardado con éxito ({os.path.getsize(out_path)} bytes).")
    return out_path


def main():
    base_dir_es = "packages/[ES]_5_Fuerzas_Porter"
    base_dir_en = "packages/[EN]_Porter_5_Forces"

    generate_workbook(lang='ES', out_dir=base_dir_es)
    generate_workbook(lang='EN', out_dir=base_dir_en)


if __name__ == '__main__':
    main()
