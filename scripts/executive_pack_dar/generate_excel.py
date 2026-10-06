#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos analíticos oficiales de Toma de Decisiones y Priorización en Excel de Datalaria:
1. packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa/[ES]_Matriz_DAR/Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx
2. packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa/[EN]_Quantitative_DAR/Quantitative_DAR_Matrix_Datalaria_EN.xlsx

Arquitectura de 4 pestañas interconectadas:
- Pestaña 1: "Dashboard Ejecutivo" / "Executive Dashboard"
- Pestaña 2: "Filtros Veto (Must-Haves)" / "Veto Criteria (Must-Haves)"
- Pestaña 3: "Scoring Ponderado (Wants)" / "Weighted Scoring (Wants)"
- Pestaña 4: "Sensibilidad & Auditoría" / "Sensitivity & Audit Trail"

ESTÁNDAR RIGUROSO DE PROTECCIÓN DE CELDAS, FORMATO Y VISUALIZACIÓN:
- CELDAS SIN FÓRMULA (Entradas del usuario / Datos / Textos editables / Criterios / Pesos / Calificaciones / Actas):
  * locked = False (Totalmente editables)
  * Fondo blanco (#FFFFFF)
- CELDAS CON FÓRMULA (Totales, sumatorios, subtotales, vínculos, rankings, dictámenes):
  * locked = True (Blindadas contra alteraciones accidentales)
  * Fondo gris suave (#F1F5F9 / Slate 100)
- CABECERAS Y TÍTULOS ESTRUCTURALES:
  * locked = True
  * Fondo Azul Marino Slate (#0F172A / #1E293B) con texto blanco
- AJUSTE DE TEXTO Y ANCHO DE COLUMNAS:
  * wrap_text = True activo en todas las celdas de texto, títulos, descripciones, dictámenes y cabeceras
  * Anchos de columna holgados y alturas de fila proporcionales para evitar cualquier recorte de texto
- PROTECCIÓN DE HOJA OPENXML:
  * ws.protection.set_password("Datalaria2026")
  * ws.protection.sheet = True
  * ws.protection.selectUnlockedCells = False (0 en XML: permite doble clic y edición fluida)
  * ws.protection.selectLockedCells = False (0 en XML: permite seleccionar para lectura)
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = "0F172A"       # Slate 900 / Títulos principales y cabeceras
COLOR_NAVY_MED = "1E293B"        # Slate 800 / Subcabeceras
COLOR_NAVY_LIGHT = "334155"      # Slate 700 / Texto secundario
COLOR_BLUE_ACCENT = "2563EB"     # Blue 600 / Azul Consultoría Datalaria
COLOR_BLUE_LIGHT = "EFF6FF"      # Blue 50 / Fondos suaves

# Estados y Alertas
COLOR_GREEN_BG = "D1FAE5"        # Verde suave (Apta / Ganadora)
COLOR_GREEN_TEXT = "065F46"      # Verde texto
COLOR_GREEN_BORDER = "10B981"    # Verde acento

COLOR_AMBER_BG = "FEF3C7"        # Ámbar suave (Segunda Opción / Alerta)
COLOR_AMBER_TEXT = "92400E"      # Ámbar texto
COLOR_AMBER_BORDER = "F59E0B"    # Ámbar acento

COLOR_RED_BG = "FEE2E2"          # Rojo suave (Descalificada / Veto)
COLOR_RED_TEXT = "991B1B"        # Rojo texto
COLOR_RED_BORDER = "EF4444"      # Rojo acento

COLOR_BG_CARD = "F1F5F9"         # Slate 100 / Totales y cajas resumen
COLOR_BG_LIGHT = "F1F5F9"        # Slate 100 / Celdas con fórmulas protegidas (gris suave)
COLOR_WHITE = "FFFFFF"           # Blanco puro (#FFFFFF) para celdas editables sin fórmula
COLOR_BORDER_LIGHT = "CBD5E1"    # Slate 300
COLOR_BORDER_MED = "94A3B8"      # Slate 400

PASSWORD_PROTECT = "Datalaria2026"

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
    card_border = Border(
        left=Side(style='medium', color=COLOR_NAVY_DARK),
        right=Side(style='thin', color=COLOR_BORDER_LIGHT),
        top=Side(style='thin', color=COLOR_BORDER_LIGHT),
        bottom=Side(style='thin', color=COLOR_BORDER_LIGHT)
    )

    if lang == 'ES':
        num_fmt_curr = "#,##0 €"
        num_fmt_curr_dec = "#,##0.00 €"
        num_fmt_pct = "0.0%"
        num_fmt_dec = "0.0"
        num_fmt_score = "0.0"
        num_fmt_int = "#,##0"
    else:
        num_fmt_curr = "$#,##0"
        num_fmt_curr_dec = "$#,##0.00"
        num_fmt_pct = "0.0%"
        num_fmt_dec = "0.0"
        num_fmt_score = "0.0"
        num_fmt_int = "#,##0"

    return {
        'thin_border': thin_border,
        'header_border': header_border,
        'total_border': total_border,
        'card_border': card_border,
        'font_title': Font(name='Segoe UI', size=15, bold=True, color=COLOR_NAVY_DARK),
        'font_subtitle': Font(name='Segoe UI', size=10, bold=True, color=COLOR_BLUE_ACCENT),
        'font_meta': Font(name='Segoe UI', size=9, italic=True, color="64748B"),
        'font_section': Font(name='Segoe UI', size=11, bold=True, color=COLOR_NAVY_DARK),
        'font_header': Font(name='Segoe UI', size=9.5, bold=True, color=COLOR_WHITE),
        'font_subhead': Font(name='Segoe UI', size=9, bold=True, color=COLOR_NAVY_MED),
        'font_regular': Font(name='Segoe UI', size=9, color=COLOR_NAVY_DARK),
        'font_bold': Font(name='Segoe UI', size=9, bold=True, color=COLOR_NAVY_DARK),
        'font_kpi_val': Font(name='Segoe UI', size=16, bold=True, color=COLOR_NAVY_DARK),
        'font_kpi_lbl': Font(name='Segoe UI', size=8.5, bold=True, color="64748B"),
        'font_badge': Font(name='Segoe UI', size=8.5, bold=True),
        'fill_navy_hdr': PatternFill(start_color=COLOR_NAVY_DARK, end_color=COLOR_NAVY_DARK, fill_type='solid'),
        'fill_navy_sub': PatternFill(start_color=COLOR_NAVY_MED, end_color=COLOR_NAVY_MED, fill_type='solid'),
        'fill_blue_hdr': PatternFill(start_color=COLOR_BLUE_ACCENT, end_color=COLOR_BLUE_ACCENT, fill_type='solid'),
        'fill_card_bg': PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid'),
        'fill_calc': PatternFill(start_color=COLOR_BG_LIGHT, end_color=COLOR_BG_LIGHT, fill_type='solid'), # Gris suave fórmulas
        'fill_input': PatternFill(start_color=COLOR_WHITE, end_color=COLOR_WHITE, fill_type='solid'),       # Blanco puro inputs
        'fill_total': PatternFill(start_color=COLOR_BG_CARD, end_color=COLOR_BG_CARD, fill_type='solid'),
        'fill_green_zone': PatternFill(start_color=COLOR_GREEN_BG, end_color=COLOR_GREEN_BG, fill_type='solid'),
        'fill_amber_zone': PatternFill(start_color=COLOR_AMBER_BG, end_color=COLOR_AMBER_BG, fill_type='solid'),
        'fill_red_zone': PatternFill(start_color=COLOR_RED_BG, end_color=COLOR_RED_BG, fill_type='solid'),
        'align_center': Alignment(horizontal='center', vertical='center'),
        'align_left': Alignment(horizontal='left', vertical='center'),
        'align_right': Alignment(horizontal='right', vertical='center'),
        'align_center_wrap': Alignment(horizontal='center', vertical='center', wrap_text=True),
        'align_left_wrap': Alignment(horizontal='left', vertical='center', wrap_text=True),
        'align_right_wrap': Alignment(horizontal='right', vertical='center', wrap_text=True),
        'num_fmt_curr': num_fmt_curr,
        'num_fmt_curr_dec': num_fmt_curr_dec,
        'num_fmt_pct': num_fmt_pct,
        'num_fmt_dec': num_fmt_dec,
        'num_fmt_score': num_fmt_score,
        'num_fmt_int': num_fmt_int,
    }


def format_merged_range(ws, min_row, min_col, max_row, max_col, font=None, fill=None, border=None, alignment=None, protection=None, number_format=None, value=None):
    """
    Aplica estilo homogéneo a todas las celdas de un rango combinado para evitar
    artefactos visuales de bordes o rellenos y garantizar compatibilidad OpenXML.
    """
    ws.merge_cells(start_row=min_row, start_column=min_col, end_row=max_row, end_column=max_col)
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            cell = ws.cell(row=r, column=c)
            if font is not None:
                cell.font = font
            if fill is not None:
                cell.fill = fill
            if border is not None:
                cell.border = border
            if alignment is not None:
                cell.alignment = alignment
            if protection is not None:
                cell.protection = protection
            if number_format is not None:
                cell.number_format = number_format
    if value is not None:
        ws.cell(row=min_row, column=min_col, value=value)


def apply_sheet_protection(ws, allow_structure=True):
    """
    Aplica protección nativa con contraseña para blindar fórmulas y elementos visuales.
    En el estándar OpenXML (ECMA-376 / CT_SheetProtection):
      - sheet, objects, scenarios: True = blindado.
      - selectUnlockedCells = False (0 = sin restricción activa, permite selección y edición).
      - selectLockedCells = False (0 = sin restricción, permite seleccionar celdas bloqueadas para lectura).
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
# PESTAÑA 2: FILTROS VETO (MUST-HAVES)
# ==============================================================================
def build_tab2_veto(wb, ws, lang='ES'):
    st = get_base_styles(lang=lang)
    title_tab = "Filtros Veto (Must-Haves)" if lang == 'ES' else "Veto Criteria (Must-Haves)"
    ws.title = title_tab
    ws.views.sheetView[0].showGridLines = True

    # 1. Cabecera Institucional
    ws['B2'] = "DATALARIA · SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN"
    ws['B2'].font = st['font_subtitle']
    
    ws['B3'] = "Criterios Veto No Negociables (Must-Haves) & Factor Booleano" if lang == 'ES' else "Non-Negotiable Veto Criteria (Must-Haves) & Boolean Gatekeeper"
    ws['B3'].font = st['font_title']
    
    ws['B4'] = ("Regla de exclusión implacable CMMI DAR: El incumplimiento de 1 solo criterio veto genera la descalificación inmediata "
                "de la alternativa (Factor Booleano Vk = 0), anulando su puntuación final."
                if lang == 'ES' else
                "Strict CMMI DAR elimination rule: Failing even 1 veto criterion results in immediate disqualification of the alternative "
                "(Boolean Gatekeeper Vk = 0), nullifying its final evaluation score.")
    ws['B4'].font = st['font_meta']

    # 2. Tabla de Criterios Veto
    row_hdr = 7
    headers = [
        ("Cód", "Code"),
        ("Criterio Veto (Must-Have)", "Veto Criterion (Must-Have)"),
        ("Descripción & Métrica de Exclusión", "Description & Exclusion Threshold"),
        ("Evidencia / Certificación Exigida", "Required Evidence / Certification"),
        ("Alt A: Vendor Alpha", "Alt A: Vendor Alpha"),
        ("Alt B: Vendor Beta", "Alt B: Vendor Beta"),
        ("Alt C: Vendor Gamma", "Alt C: Vendor Gamma"),
        ("Alt D: Vendor Delta", "Alt D: Vendor Delta"),
        ("Alt E: Vendor Epsilon", "Alt E: Vendor Epsilon"),
    ]

    for col_idx, (h_es, h_en) in enumerate(headers, start=2): # Col B to J
        cell = ws.cell(row=row_hdr, column=col_idx)
        cell.value = h_es if lang == 'ES' else h_en
        cell.font = st['font_header']
        cell.fill = st['fill_navy_hdr']
        cell.alignment = st['align_center_wrap']
        cell.border = st['header_border']
        cell.protection = PROT_LOCKED

    ws.row_dimensions[row_hdr].height = 34

    # 6 Criterios Veto
    criteria_es = [
        ("V-01", "Cumplimiento RGPD & Certificación ISO 27001", "Certificación activa SOC 2 Type II / ISO 27001 y adecuación legal al RGPD europeo.", "Certificado auditoría vigente < 12 meses"),
        ("V-02", "Techo Presupuestario CAPEX (€)", "Coste total de licenciamiento inicial e implantación <= 450.000 €.", "Propuesta económica vinculante"),
        ("V-03", "Plazo Máximo Go-Live (< 6 Meses)", "Capacidad contractual de despliegue operativo en producción en menos de 180 días.", "Cronograma Gantt firmado por proveedor"),
        ("V-04", "Integración Nativa con Arquitectura Core", "Conectores estándar y APIs REST documentadas para el ERP corporativo actual.", "Prueba de concepto / Sandbox técnica"),
        ("V-05", "Soberanía de Datos & Residencia en UE", "Almacenamiento exclusivo y procesamiento de datos dentro del Espacio Económico Europeo.", "Cláusula contractual de soberanía"),
        ("V-06", "SLA Disponibilidad Mínima 99.9% (24/7)", "Compromiso de penalización contractual por caídas de servicio superiores a 43 min/mes.", "Anexo legal de Nivel de Servicio (SLA)"),
    ]

    criteria_en = [
        ("V-01", "GDPR Compliance & ISO 27001 Certification", "Active SOC 2 Type II / ISO 27001 certification and full European GDPR adherence.", "Valid third-party audit report < 12 months"),
        ("V-02", "CAPEX Budget Ceiling ($)", "Total upfront licensing and implementation cost <= $450,000.", "Binding commercial proposal"),
        ("V-03", "Maximum Go-Live Timeline (< 6 Months)", "Contractual commitment to achieve enterprise production go-live in under 180 days.", "Signed transition Gantt schedule"),
        ("V-04", "Native Integration with Core Architecture", "Documented standard REST APIs and connectors for current enterprise ERP.", "Technical sandbox / Proof-of-concept"),
        ("V-05", "Data Sovereignty & EU/Local Residency", "Exclusive data storage and processing within European Economic Area / sovereign cloud.", "Contractual data location clause"),
        ("V-06", "Minimum Availability SLA 99.9% (24/7)", "Contractual penalty clause for unscheduled platform downtime exceeding 43 min/month.", "Legal Service Level Agreement (SLA) exhibit"),
    ]

    criteria = criteria_es if lang == 'ES' else criteria_en

    pass_val = "CUMPLE" if lang == 'ES' else "PASS"
    fail_val = "NO CUMPLE" if lang == 'ES' else "FAIL"

    alt_defaults = [
        [pass_val, pass_val, pass_val, pass_val, pass_val],  # V-01
        [pass_val, pass_val, pass_val, pass_val, pass_val],  # V-02
        [pass_val, pass_val, pass_val, pass_val, pass_val],  # V-03
        [pass_val, pass_val, pass_val, pass_val, pass_val],  # V-04
        [pass_val, pass_val, pass_val, fail_val, pass_val],  # V-05 -> Alt D fails
        [pass_val, pass_val, pass_val, pass_val, pass_val],  # V-06
    ]

    for idx, (code, name, desc, evid) in enumerate(criteria):
        curr_row = row_hdr + 1 + idx
        ws.row_dimensions[curr_row].height = 44

        # Col B: Code -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO
        cB = ws.cell(row=curr_row, column=2, value=code)
        cB.font = st['font_bold']
        cB.alignment = st['align_center']
        cB.border = st['thin_border']
        cB.fill = st['fill_input']
        cB.protection = PROT_UNLOCKED

        # Col C: Name -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        cC = ws.cell(row=curr_row, column=3, value=name)
        cC.font = st['font_bold']
        cC.alignment = st['align_left_wrap']
        cC.border = st['thin_border']
        cC.fill = st['fill_input']
        cC.protection = PROT_UNLOCKED

        # Col D: Desc -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        cD = ws.cell(row=curr_row, column=4, value=desc)
        cD.font = st['font_regular']
        cD.alignment = st['align_left_wrap']
        cD.border = st['thin_border']
        cD.fill = st['fill_input']
        cD.protection = PROT_UNLOCKED

        # Col E: Evidence -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        cE = ws.cell(row=curr_row, column=5, value=evid)
        cE.font = st['font_meta']
        cE.alignment = st['align_left_wrap']
        cE.border = st['thin_border']
        cE.fill = st['fill_input']
        cE.protection = PROT_UNLOCKED

        # Cols F to J: Alternatives -> SIN FÓRMULA (Entrada de usuario) -> EDITABLES CON FONDO BLANCO
        for a_idx in range(5):
            col_target = 6 + a_idx
            cA = ws.cell(row=curr_row, column=col_target, value=alt_defaults[idx][a_idx])
            cA.font = st['font_bold']
            cA.alignment = st['align_center']
            cA.border = st['thin_border']
            cA.fill = st['fill_input']
            cA.protection = PROT_UNLOCKED

    # 3. Filas de Control Lógico y Estatus de Veto (CON FÓRMULAS -> PROTEGIDAS CON FONDO GRIS SUAVE)
    row_count = row_hdr + 1 + len(criteria) # Row 14
    ws.row_dimensions[row_count].height = 26
    
    format_merged_range(ws, min_row=row_count, min_col=2, max_row=row_count, max_col=5,
                        font=st['font_bold'], fill=st['fill_calc'], border=st['total_border'],
                        alignment=st['align_right_wrap'], protection=PROT_LOCKED,
                        value="TOTAL CRITERIOS INCUMPLIDOS" if lang == 'ES' else "TOTAL FAILED VETO CRITERIA")

    for a_idx in range(5):
        col_letter = get_column_letter(6 + a_idx)
        cell_cnt = ws.cell(row=row_count, column=6 + a_idx)
        cell_cnt.value = f'=COUNTIF({col_letter}8:{col_letter}13, "{fail_val}")'
        cell_cnt.font = Font(name='Segoe UI', size=10, bold=True)
        cell_cnt.alignment = st['align_center']
        cell_cnt.border = st['total_border']
        cell_cnt.fill = st['fill_calc'] # Gris suave
        cell_cnt.protection = PROT_LOCKED

    # Fila de Estatus de Viabilidad Veto (CON FÓRMULA -> PROTEGIDA)
    row_status = row_count + 1 # Row 15
    ws.row_dimensions[row_status].height = 26
    format_merged_range(ws, min_row=row_status, min_col=2, max_row=row_status, max_col=5,
                        font=st['font_bold'], fill=st['fill_calc'], border=st['thin_border'],
                        alignment=st['align_right_wrap'], protection=PROT_LOCKED,
                        value="ESTATUS DE VIABILIDAD VETO" if lang == 'ES' else "VETO VIABILITY STATUS")

    status_pass = "APTA" if lang == 'ES' else "QUALIFIED"
    status_fail = "DESCALIFICADA" if lang == 'ES' else "DISQUALIFIED"

    for a_idx in range(5):
        col_letter = get_column_letter(6 + a_idx)
        cell_st = ws.cell(row=row_status, column=6 + a_idx)
        cell_st.value = f'=IF({col_letter}{row_count}=0, "{status_pass}", "{status_fail}")'
        cell_st.font = Font(name='Segoe UI', size=9.5, bold=True)
        cell_st.alignment = st['align_center']
        cell_st.border = st['thin_border']
        cell_st.fill = st['fill_calc'] # Gris suave
        cell_st.protection = PROT_LOCKED

    # Fila de Multiplicador Booleano Vk (CON FÓRMULA -> PROTEGIDA)
    row_vk = row_status + 1 # Row 16
    ws.row_dimensions[row_vk].height = 26
    format_merged_range(ws, min_row=row_vk, min_col=2, max_row=row_vk, max_col=5,
                        font=Font(name='Segoe UI', size=9, bold=True, color=COLOR_WHITE),
                        fill=st['fill_navy_sub'], border=st['thin_border'],
                        alignment=st['align_right_wrap'], protection=PROT_LOCKED,
                        value="FACTOR BOOLEANO GATEKEEPER (Vk = 1 ó 0)" if lang == 'ES' else "BOOLEAN GATEKEEPER FACTOR (Vk = 1 or 0)")

    for a_idx in range(5):
        col_letter = get_column_letter(6 + a_idx)
        cell_vk = ws.cell(row=row_vk, column=6 + a_idx)
        cell_vk.value = f'=IF({col_letter}{row_status}="{status_pass}", 1, 0)'
        cell_vk.font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_WHITE)
        cell_vk.alignment = st['align_center']
        cell_vk.border = st['thin_border']
        cell_vk.fill = st['fill_navy_sub']
        cell_vk.protection = PROT_LOCKED

    # Data Validation para CUMPLE / NO CUMPLE (o PASS / FAIL)
    dv = DataValidation(type="list", formula1=f'"{pass_val},{fail_val}"', allow_blank=False)
    dv.error = "Seleccione un valor válido de la lista desplegable." if lang == 'ES' else "Select a valid value from the dropdown list."
    dv.errorTitle = "Valor inválido" if lang == 'ES' else "Invalid Value"
    ws.add_data_validation(dv)
    dv.add("F8:J13")

    # Column dimensions (Holgadas para lectura directiva)
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 42
    ws.column_dimensions['D'].width = 52
    ws.column_dimensions['E'].width = 38
    ws.column_dimensions['F'].width = 20
    ws.column_dimensions['G'].width = 20
    ws.column_dimensions['H'].width = 20
    ws.column_dimensions['I'].width = 20
    ws.column_dimensions['J'].width = 20

    apply_sheet_protection(ws, allow_structure=True)


# ==============================================================================
# PESTAÑA 3: SCORING PONDERADO (WANTS)
# ==============================================================================
def build_tab3_scoring(wb, ws, lang='ES'):
    st = get_base_styles(lang=lang)
    title_tab = "Scoring Ponderado (Wants)" if lang == 'ES' else "Weighted Scoring (Wants)"
    ws.title = title_tab
    ws.views.sheetView[0].showGridLines = True

    # 1. Cabecera Institucional
    ws['B2'] = "DATALARIA · SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN"
    ws['B2'].font = st['font_subtitle']
    
    ws['B3'] = "Matriz Multicriterio Ponderada (Wants) & Algoritmo de Decisión" if lang == 'ES' else "Multi-Criteria Weighted Scoring Matrix (Wants) & Decision Algorithm"
    ws['B3'].font = st['font_title']
    
    ws['B4'] = ("Evaluación de 13 criterios agrupados en 4 pilares estratégicos. Rango de puntuación: 1 (Deficiente) a 10 (Excelente). "
                "La puntuación ponderada se multiplica automáticamente por el Factor Booleano Veto (Vk)."
                if lang == 'ES' else
                "Evaluation across 13 criteria structured in 4 strategic pillars. Rating scale: 1 (Deficient) to 10 (World-Class). "
                "Weighted score is automatically multiplied by the Boolean Gatekeeper Factor (Vk).")
    ws['B4'].font = st['font_meta']

    # Cabecera de la tabla
    row_hdr = 7
    headers = [
        ("Cód", "Code"),
        ("Pilar & Criterio Estratégico de Evaluación", "Strategic Pillar & Evaluation Criterion"),
        ("Métrica Objetiva / Pregunta Clave de Calificación", "Objective Metric / Evaluation Key Question"),
        ("Peso %", "Weight %"),
        ("Alt A: Alpha", "Alt A: Alpha"),
        ("Alt B: Beta", "Alt B: Beta"),
        ("Alt C: Gamma", "Alt C: Gamma"),
        ("Alt D: Delta", "Alt D: Delta"),
        ("Alt E: Epsilon", "Alt E: Epsilon"),
    ]

    for col_idx, (h_es, h_en) in enumerate(headers, start=2): # Col B to J
        cell = ws.cell(row=row_hdr, column=col_idx)
        cell.value = h_es if lang == 'ES' else h_en
        cell.font = st['font_header']
        cell.fill = st['fill_navy_hdr']
        cell.alignment = st['align_center_wrap']
        cell.border = st['header_border']
        cell.protection = PROT_LOCKED

    ws.row_dimensions[row_hdr].height = 34

    # 4 Pilares con sus criterios (Total 13 criterios)
    pillars_es = [
        {
            'name': "PILAR 1: AJUSTE TÉCNICO & FUNCIONAL (30.0%)",
            'criteria': [
                ("C-1.1", "Cobertura de Requerimientos Funcionales Core", "Porcentaje de casos de uso cubiertos de forma nativa sin desarrollo a medida.", 0.10, [8.0, 9.5, 7.5, 8.5, 7.0]),
                ("C-1.2", "Ergonomía, UX y Curva de Adopción de Usuario", "Facilidad de uso, interfaz intuitiva y reducción del tiempo estimado de onboarding.", 0.08, [7.5, 9.0, 8.0, 7.0, 7.5]),
                ("C-1.3", "Arquitectura de Integración, APIs REST y Webhooks", "Robustez del catálogo de APIs, webhooks bidireccionales y latencia de sync.", 0.07, [8.5, 9.0, 7.0, 8.0, 6.5]),
                ("C-1.4", "Rendimiento, Concurrencia y Procesamiento Real-Time", "Capacidad de respuesta ante alta concurrencia (>5.000 usuarios simultáneos).", 0.05, [8.0, 9.0, 7.5, 8.5, 7.0]),
            ]
        },
        {
            'name': "PILAR 2: COSTE TOTAL DE PROPIEDAD (TCO A 3 AÑOS) (25.0%)",
            'criteria': [
                ("C-2.1", "Inversión Inicial en Licenciamiento y Setup (Año 1)", "Coste de adquisición, cuotas de alta y licenciamiento base del primer año.", 0.10, [7.0, 7.5, 9.0, 6.5, 8.5]),
                ("C-2.2", "Coste de Consultoría, Parametrización y Migración", "Tarifa por hora y volumen de jornadas presupuestadas para la implantación.", 0.09, [7.5, 8.0, 8.5, 6.0, 8.0]),
                ("C-2.3", "Costes Recurrentes de Mantenimiento y Upgrades (Años 2-3)", "Predictibilidad de tarifas anuales, soporte premium y coste de almacenamiento adicional.", 0.06, [8.0, 8.5, 8.0, 7.0, 7.5]),
            ]
        },
        {
            'name': "PILAR 3: SLA, SOPORTE & SOLVENCIA DEL PROVEEDOR (20.0%)",
            'criteria': [
                ("C-3.1", "SLA y Tiempo de Respuesta ante Incidencias Críticas", "Compromiso de resolución P1 < 2 horas con penalizaciones automáticas.", 0.08, [8.5, 9.5, 7.0, 8.0, 6.5]),
                ("C-3.2", "Solvencia Financiera, Track-Record y Presencia Local", "Años de operación, rating crediticio auditado y equipo de soporte en idioma nativo.", 0.07, [9.0, 9.0, 7.5, 8.5, 6.0]),
                ("C-3.3", "Calidad de Documentación, Certificaciones y Academia", "Repositorio de formación, manuales técnicos y certificaciones oficiales para el equipo.", 0.05, [7.5, 8.5, 8.0, 7.5, 7.0]),
            ]
        },
        {
            'name': "PILAR 4: ESCALABILIDAD, SEGURIDAD & ROADMAP (25.0%)",
            'criteria': [
                ("C-4.1", "Modelo de Seguridad Zero-Trust, Cifrado y RBAC", "Cifrado end-to-end AES-256 en reposo/tránsito, granularidad de roles y MFA nativo.", 0.10, [8.5, 9.5, 7.5, 8.5, 7.0]),
                ("C-4.2", "Escalabilidad Horizontal y Resiliencia Cloud", "Elasticidad de infraestructura automática ante picos de demanda operativa.", 0.08, [8.0, 9.0, 7.5, 8.5, 7.0]),
                ("C-4.3", "Visión del Roadmap Tecnológico e Integración de IA", "Pipeline de innovación validado, capacidades de analítica avanzada e IA generativa.", 0.07, [7.5, 9.0, 6.5, 8.0, 7.5]),
            ]
        }
    ]

    pillars_en = [
        {
            'name': "PILLAR 1: TECHNICAL & FUNCTIONAL FIT (30.0%)",
            'criteria': [
                ("C-1.1", "Core Functional Requirements Coverage", "Percentage of operational use cases supported out-of-the-box without custom code.", 0.10, [8.0, 9.5, 7.5, 8.5, 7.0]),
                ("C-1.2", "Ergonomics, UX & User Adoption Curve", "User interface intuitiveness and projected reduction in corporate training overhead.", 0.08, [7.5, 9.0, 8.0, 7.0, 7.5]),
                ("C-1.3", "Integration Architecture, REST APIs & Webhooks", "API catalog maturity, bi-directional webhooks and sync latency under load.", 0.07, [8.5, 9.0, 7.0, 8.0, 6.5]),
                ("C-1.4", "Throughput, Concurrency & Real-Time Performance", "System latency and responsiveness under stress (>5,000 concurrent sessions).", 0.05, [8.0, 9.0, 7.5, 8.5, 7.0]),
            ]
        },
        {
            'name': "PILLAR 2: TOTAL COST OF OWNERSHIP (3-YEAR TCO) (25.0%)",
            'criteria': [
                ("C-2.1", "Upfront Licensing & Setup Investment (Year 1)", "First-year software license acquisition fee, onboarding and setup costs.", 0.10, [7.0, 7.5, 9.0, 6.5, 8.5]),
                ("C-2.2", "System Integration, Consulting & Customization Costs", "Vendor/partner professional services hourly rates and total implementation mandates.", 0.09, [7.5, 8.0, 8.5, 6.0, 8.0]),
                ("C-2.3", "Recurring Maintenance & Upgrade Overhead (Years 2-3)", "Predictability of annual subscription hikes, premium support and data storage scaling.", 0.06, [8.0, 8.5, 8.0, 7.0, 7.5]),
            ]
        },
        {
            'name': "PILLAR 3: SLA, SUPPORT & VENDOR STABILITY (20.0%)",
            'criteria': [
                ("C-3.1", "SLA & Critical Incident Resolution Guarantee", "Contractual commitment for Severity 1 incident turnaround < 2h with penalty clauses.", 0.08, [8.5, 9.5, 7.0, 8.0, 6.5]),
                ("C-3.2", "Financial Solvency, Market Track-Record & Local Presence", "Years in business, credit rating, balance sheet health and regional technical support.", 0.07, [9.0, 9.0, 7.5, 8.5, 6.0]),
                ("C-3.3", "Technical Documentation, Certifications & Learning Hub", "Comprehensive API docs, sandbox availability and official technical certification track.", 0.05, [7.5, 8.5, 8.0, 7.5, 7.0]),
            ]
        },
        {
            'name': "PILLAR 4: SCALABILITY, SECURITY & ROADMAP (25.0%)",
            'criteria': [
                ("C-4.1", "Zero-Trust Architecture, AES-256 Encryption & RBAC", "End-to-end encryption in transit/rest, granular role-based permissions and native MFA.", 0.10, [8.5, 9.5, 7.5, 8.5, 7.0]),
                ("C-4.2", "Horizontal Elasticity & Cloud High-Availability", "Automated container auto-scaling and multi-region failover resilience.", 0.08, [8.0, 9.0, 7.5, 8.5, 7.0]),
                ("C-4.3", "Technology Roadmap & Generative AI Integration", "Documented R&D delivery milestones, AI workflow copilots and predictive analytics.", 0.07, [7.5, 9.0, 6.5, 8.0, 7.5]),
            ]
        }
    ]

    pillars = pillars_es if lang == 'ES' else pillars_en

    current_row = row_hdr + 1
    criterion_rows = []
    pillar_subtotal_rows = []

    for p_idx, p_data in enumerate(pillars, start=1):
        # Fila de Título del Pilar (CABECERA -> PROTEGIDA)
        ws.row_dimensions[current_row].height = 26
        format_merged_range(ws, min_row=current_row, min_col=2, max_row=current_row, max_col=10,
                            font=Font(name='Segoe UI', size=10, bold=True, color=COLOR_WHITE),
                            fill=st['fill_navy_sub'], border=st['thin_border'],
                            alignment=st['align_left_wrap'], protection=PROT_LOCKED,
                            value=p_data['name'])
        current_row += 1

        p_start_row = current_row

        # Criterios del Pilar (SIN FÓRMULA -> EDITABLES CON FONDO BLANCO)
        for code, name, metric, weight, default_scores in p_data['criteria']:
            ws.row_dimensions[current_row].height = 38
            criterion_rows.append(current_row)

            # Col B: Code -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO
            cB = ws.cell(row=current_row, column=2, value=code)
            cB.font = st['font_bold']
            cB.alignment = st['align_center']
            cB.border = st['thin_border']
            cB.fill = st['fill_input']
            cB.protection = PROT_UNLOCKED

            # Col C: Name -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
            cC = ws.cell(row=current_row, column=3, value=name)
            cC.font = st['font_bold']
            cC.alignment = st['align_left_wrap']
            cC.border = st['thin_border']
            cC.fill = st['fill_input']
            cC.protection = PROT_UNLOCKED

            # Col D: Metric -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
            cD = ws.cell(row=current_row, column=4, value=metric)
            cD.font = st['font_regular']
            cD.alignment = st['align_left_wrap']
            cD.border = st['thin_border']
            cD.fill = st['fill_input']
            cD.protection = PROT_UNLOCKED

            # Col E: Weight -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO
            cE = ws.cell(row=current_row, column=5, value=weight)
            cE.font = st['font_bold']
            cE.alignment = st['align_right']
            cE.border = st['thin_border']
            cE.fill = st['fill_input']
            cE.number_format = st['num_fmt_pct']
            cE.protection = PROT_UNLOCKED

            # Cols F to J: Alternative Scores -> SIN FÓRMULA -> EDITABLES CON FONDO BLANCO
            for a_idx, sc_val in enumerate(default_scores):
                cA = ws.cell(row=current_row, column=6 + a_idx, value=sc_val)
                cA.font = st['font_bold']
                cA.alignment = st['align_center']
                cA.border = st['thin_border']
                cA.fill = st['fill_input']
                cA.number_format = st['num_fmt_score']
                cA.protection = PROT_UNLOCKED

            current_row += 1

        p_end_row = current_row - 1

        # Subtotal del Pilar (CON FÓRMULAS -> PROTEGIDAS CON FONDO GRIS SUAVE)
        ws.row_dimensions[current_row].height = 26
        format_merged_range(ws, min_row=current_row, min_col=2, max_row=current_row, max_col=4,
                            font=Font(name='Segoe UI', size=9, bold=True, color=COLOR_NAVY_DARK),
                            fill=st['fill_calc'], border=st['thin_border'],
                            alignment=st['align_right_wrap'], protection=PROT_LOCKED,
                            value=f"Subtotal Ponderado {p_data['name'].split(':')[0]}" if lang == 'ES' else f"Weighted Subtotal {p_data['name'].split(':')[0]}")

        # Subtotal Weight (CON FÓRMULA -> PROTEGIDO)
        c_sub_w = ws.cell(row=current_row, column=5, value=f"=SUM(E{p_start_row}:E{p_end_row})")
        c_sub_w.font = st['font_bold']
        c_sub_w.alignment = st['align_right']
        c_sub_w.fill = st['fill_calc'] # Gris suave
        c_sub_w.border = st['thin_border']
        c_sub_w.number_format = st['num_fmt_pct']
        c_sub_w.protection = PROT_LOCKED

        # Subtotal Scores per Alternative (CON FÓRMULAS -> PROTEGIDOS)
        for a_idx in range(5):
            col_letter = get_column_letter(6 + a_idx)
            c_sub_sc = ws.cell(row=current_row, column=6 + a_idx, 
                               value=f"=SUMPRODUCT($E${p_start_row}:$E${p_end_row}, {col_letter}${p_start_row}:{col_letter}${p_end_row})*10")
            c_sub_sc.font = st['font_bold']
            c_sub_sc.alignment = st['align_center']
            c_sub_sc.fill = st['fill_calc'] # Gris suave
            c_sub_sc.border = st['thin_border']
            c_sub_sc.number_format = st['num_fmt_score']
            c_sub_sc.protection = PROT_LOCKED

        pillar_subtotal_rows.append(current_row)
        current_row += 1

    # Fila de TOTAL GLOBAL PONDERADO BASE (CON FÓRMULAS -> PROTEGIDAS CON FONDO GRIS SUAVE)
    row_tot_base = current_row
    ws.row_dimensions[row_tot_base].height = 28
    format_merged_range(ws, min_row=row_tot_base, min_col=2, max_row=row_tot_base, max_col=4,
                        font=Font(name='Segoe UI', size=10, bold=True, color=COLOR_NAVY_DARK),
                        fill=st['fill_calc'], border=st['total_border'],
                        alignment=st['align_right_wrap'], protection=PROT_LOCKED,
                        value="PUNTUACIÓN PONDERADA BASE (Escala 0 - 100)" if lang == 'ES' else "BASE WEIGHTED SCORE (Scale 0 - 100)")

    # Total Weight Check (CON FÓRMULA -> PROTEGIDO)
    first_c_row = criterion_rows[0]
    last_c_row = criterion_rows[-1]
    c_tot_w = ws.cell(row=row_tot_base, column=5, 
                      value=f"=SUM(E{pillar_subtotal_rows[0]},E{pillar_subtotal_rows[1]},E{pillar_subtotal_rows[2]},E{pillar_subtotal_rows[3]})")
    c_tot_w.font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_NAVY_DARK)
    c_tot_w.alignment = st['align_right']
    c_tot_w.fill = st['fill_calc'] # Gris suave
    c_tot_w.border = st['total_border']
    c_tot_w.number_format = st['num_fmt_pct']
    c_tot_w.protection = PROT_LOCKED

    # Total Base Score per Alternative (CON FÓRMULAS -> PROTEGIDOS)
    for a_idx in range(5):
        col_letter = get_column_letter(6 + a_idx)
        sub_cells = [f"{col_letter}{r}" for r in pillar_subtotal_rows]
        c_tot_sc = ws.cell(row=row_tot_base, column=6 + a_idx, value=f"=SUM({','.join(sub_cells)})")
        c_tot_sc.font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_NAVY_DARK)
        c_tot_sc.alignment = st['align_center']
        c_tot_sc.fill = st['fill_calc'] # Gris suave
        c_tot_sc.border = st['total_border']
        c_tot_sc.number_format = st['num_fmt_score']
        c_tot_sc.protection = PROT_LOCKED

    # Fila de Factor Booleano Veto Vk Link (CON FÓRMULAS -> PROTEGIDO)
    row_veto_link = row_tot_base + 1 # Row 30
    ws.row_dimensions[row_veto_link].height = 26
    tab_veto_name = "Filtros Veto (Must-Haves)" if lang == 'ES' else "Veto Criteria (Must-Haves)"
    format_merged_range(ws, min_row=row_veto_link, min_col=2, max_row=row_veto_link, max_col=5,
                        font=Font(name='Segoe UI', size=9, bold=True, color=COLOR_NAVY_DARK),
                        fill=st['fill_calc'], border=st['thin_border'],
                        alignment=st['align_right_wrap'], protection=PROT_LOCKED,
                        value="FACTOR BOOLEANO GATEKEEPER (Vk) [Hojas Filtros Veto]" if lang == 'ES' else "BOOLEAN GATEKEEPER FACTOR (Vk) [From Veto Tab]")

    for a_idx in range(5):
        col_letter = get_column_letter(6 + a_idx)
        c_vk = ws.cell(row=row_veto_link, column=6 + a_idx, value=f"='{tab_veto_name}'!{col_letter}16")
        c_vk.font = Font(name='Segoe UI', size=10, bold=True)
        c_vk.alignment = st['align_center']
        c_vk.border = st['thin_border']
        c_vk.fill = st['fill_calc'] # Gris suave
        c_vk.protection = PROT_LOCKED

    # Fila de PUNTUACIÓN FINAL AUDITADA (Sk = Base * Vk) (CON FÓRMULAS -> PROTEGIDO)
    row_final_score = row_veto_link + 1 # Row 31
    ws.row_dimensions[row_final_score].height = 30
    format_merged_range(ws, min_row=row_final_score, min_col=2, max_row=row_final_score, max_col=5,
                        font=Font(name='Segoe UI', size=10, bold=True, color=COLOR_WHITE),
                        fill=st['fill_navy_hdr'], border=st['header_border'],
                        alignment=st['align_right_wrap'], protection=PROT_LOCKED,
                        value="PUNTUACIÓN FINAL AUDITADA DAR (Sk = Score Base × Vk)" if lang == 'ES' else "AUDITED DAR FINAL SCORE (Sk = Base Score × Vk)")

    for a_idx in range(5):
        col_letter = get_column_letter(6 + a_idx)
        c_fin = ws.cell(row=row_final_score, column=6 + a_idx, 
                        value=f"={col_letter}{row_tot_base}*{col_letter}{row_veto_link}")
        c_fin.font = Font(name='Segoe UI', size=12, bold=True, color=COLOR_WHITE)
        c_fin.alignment = st['align_center']
        c_fin.border = st['header_border']
        c_fin.fill = st['fill_navy_hdr']
        c_fin.number_format = st['num_fmt_score']
        c_fin.protection = PROT_LOCKED

    # Data Validation para Notas (1.0 a 10.0)
    dv_score = DataValidation(type="decimal", operator="between", formula1=1.0, formula2=10.0, allow_blank=False)
    dv_score.error = "La puntuación debe ser un valor numérico entre 1.0 y 10.0." if lang == 'ES' else "Score must be a number between 1.0 and 10.0."
    dv_score.errorTitle = "Puntuación Fuera de Rango" if lang == 'ES' else "Out of Range Score"
    ws.add_data_validation(dv_score)
    dv_score.add(f"F{first_c_row}:J{last_c_row}")

    # Column dimensions (Holgadas para lectura directiva)
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 44
    ws.column_dimensions['D'].width = 52
    ws.column_dimensions['E'].width = 14
    ws.column_dimensions['F'].width = 18
    ws.column_dimensions['G'].width = 18
    ws.column_dimensions['H'].width = 18
    ws.column_dimensions['I'].width = 18
    ws.column_dimensions['J'].width = 18

    apply_sheet_protection(ws, allow_structure=True)


# ==============================================================================
# PESTAÑA 1: DASHBOARD EJECUTIVO
# ==============================================================================
def build_tab1_dashboard(wb, ws, lang='ES'):
    st = get_base_styles(lang=lang)
    title_tab = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    ws.title = title_tab
    ws.views.sheetView[0].showGridLines = True

    tab_veto_name = "Filtros Veto (Must-Haves)" if lang == 'ES' else "Veto Criteria (Must-Haves)"
    tab_scoring_name = "Scoring Ponderado (Wants)" if lang == 'ES' else "Weighted Scoring (Wants)"

    # 1. Cabecera Institucional y Metadatos de Decisión C-Level
    ws['B2'] = "DATALARIA · SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN"
    ws['B2'].font = st['font_subtitle']
    
    ws['B3'] = "DASHBOARD EJECUTIVO: VEREDICTO DAR & COMPARATIVA MULTICRITERIO" if lang == 'ES' else "EXECUTIVE DASHBOARD: DAR VERDICT & MULTI-CRITERIA COMPARISON"
    ws['B3'].font = st['font_title']

    # Metadatos del Proyecto / Decisión Estratégica (SIN FÓRMULA -> EDITABLES CON FONDO BLANCO)
    meta_rows = [
        ("Decisión Estratégica / Objeto:", "Strategic Decision Scope:", "Adjudicación de Plataforma ERP Cloud Corporativa & Servicios de Implantación" if lang == 'ES' else "Enterprise Cloud ERP Platform Selection & System Integration Mandate", 5),
        ("Evaluador Responsable:", "Lead Evaluator / Committee:", "Comité de Arquitectura Tecnológica & Compras Estratégicas" if lang == 'ES' else "IT Architecture Committee & Strategic Procurement", 6),
        ("Sponsor C-Level:", "C-Suite Sponsor:", "Chief Information Officer (CIO) & Chief Financial Officer (CFO)", 7),
        ("Fecha de Congelación / Freeze Date:", "Evaluation Freeze Date:", "2026-10-28", 8),
    ]

    for lbl_es, lbl_en, default_val, r_idx in meta_rows:
        ws.row_dimensions[r_idx].height = 26
        # Etiqueta combinada en B:C -> gris suave, texto alineado a la derecha con wrap
        format_merged_range(ws, min_row=r_idx, min_col=2, max_row=r_idx, max_col=3,
                            font=st['font_bold'], fill=st['fill_calc'], border=st['thin_border'],
                            alignment=st['align_right_wrap'], protection=PROT_LOCKED,
                            value=lbl_es if lang == 'ES' else lbl_en)

        # Valor editable en D:I -> blanco puro, texto alineado a la izquierda con wrap
        format_merged_range(ws, min_row=r_idx, min_col=4, max_row=r_idx, max_col=9,
                            font=st['font_regular'], fill=st['fill_input'], border=st['thin_border'],
                            alignment=st['align_left_wrap'], protection=PROT_UNLOCKED,
                            value=default_val)

    # 2. CUADRO DE DECISIÓN RESUMEN (COMPARATIVA DE 5 ALTERNATIVAS)
    row_sum_hdr = 11
    ws.row_dimensions[row_sum_hdr].height = 32

    headers_summary = [
        ("Cód", "Code"),
        ("Alternativa / Proveedor Evaluado", "Evaluated Alternative / Vendor"),
        ("Filtro Veto", "Veto Status"),
        ("Puntuación Base", "Base Score"),
        ("Factor Vk", "Factor Vk"),
        ("Score Final", "Final Score"),
        ("Ranking", "Rank"),
        ("Dictamen Ejecutivo del Comité", "Executive Committee Verdict"),
    ]

    for col_idx, (h_es, h_en) in enumerate(headers_summary, start=2): # Col B to I
        cell = ws.cell(row=row_sum_hdr, column=col_idx)
        cell.value = h_es if lang == 'ES' else h_en
        cell.font = st['font_header']
        cell.fill = st['fill_navy_hdr']
        cell.alignment = st['align_center_wrap']
        cell.border = st['header_border']
        cell.protection = PROT_LOCKED

    alt_names_es = [
        "Vendor Alpha (Solución Global Core)",
        "Vendor Beta (Plataforma Cloud Enterprise)",
        "Vendor Gamma (Suite Modular Especializada)",
        "Vendor Delta (Legacy Hosted Provider)",
        "Vendor Epsilon (SaaS Niche Accelerator)"
    ]
    alt_names_en = [
        "Vendor Alpha (Global Core Solution)",
        "Vendor Beta (Enterprise Cloud Platform)",
        "Vendor Gamma (Modular Specialized Suite)",
        "Vendor Delta (Legacy Hosted Provider)",
        "Vendor Epsilon (SaaS Niche Accelerator)"
    ]
    alt_names = alt_names_es if lang == 'ES' else alt_names_en

    status_pass = "APTA" if lang == 'ES' else "QUALIFIED"
    status_fail = "DESCALIFICADA" if lang == 'ES' else "DISQUALIFIED"

    for idx, name in enumerate(alt_names):
        curr_row = row_sum_hdr + 1 + idx # Rows 12 to 16
        ws.row_dimensions[curr_row].height = 28
        col_letter_scoring = get_column_letter(6 + idx) # Col F to J in other tabs

        # Col B: Code -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO
        cB = ws.cell(row=curr_row, column=2, value=f"Alt-0{idx+1}")
        cB.font = st['font_bold']
        cB.alignment = st['align_center']
        cB.fill = st['fill_input']
        cB.border = st['thin_border']
        cB.protection = PROT_UNLOCKED

        # Col C: Name -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        cC = ws.cell(row=curr_row, column=3, value=name)
        cC.font = st['font_bold']
        cC.alignment = st['align_left_wrap']
        cC.fill = st['fill_input']
        cC.border = st['thin_border']
        cC.protection = PROT_UNLOCKED

        # Col D: Veto Status Link -> CON FÓRMULA -> PROTEGIDA CON FONDO GRIS SUAVE
        cD = ws.cell(row=curr_row, column=4, value=f"='{tab_veto_name}'!{col_letter_scoring}15")
        cD.font = st['font_bold']
        cD.alignment = st['align_center']
        cD.border = st['thin_border']
        cD.fill = st['fill_calc'] # Gris suave
        cD.protection = PROT_LOCKED

        # Col E: Base Score Link (Row 29 in Scoring tab) -> CON FÓRMULA -> PROTEGIDA CON FONDO GRIS SUAVE
        cE = ws.cell(row=curr_row, column=5, value=f"='{tab_scoring_name}'!{col_letter_scoring}29")
        cE.font = st['font_regular']
        cE.alignment = st['align_center']
        cE.border = st['thin_border']
        cE.fill = st['fill_calc'] # Gris suave
        cE.number_format = st['num_fmt_score']
        cE.protection = PROT_LOCKED

        # Col F: Factor Vk Link (Row 30 in Scoring tab) -> CON FÓRMULA -> PROTEGIDA CON FONDO GRIS SUAVE
        cF = ws.cell(row=curr_row, column=6, value=f"='{tab_scoring_name}'!{col_letter_scoring}30")
        cF.font = st['font_bold']
        cF.alignment = st['align_center']
        cF.border = st['thin_border']
        cF.fill = st['fill_calc'] # Gris suave
        cF.protection = PROT_LOCKED

        # Col G: Final Score Link (Row 31 in Scoring tab) -> CON FÓRMULA -> PROTEGIDA CON FONDO GRIS SUAVE
        cG = ws.cell(row=curr_row, column=7, value=f"='{tab_scoring_name}'!{col_letter_scoring}31")
        cG.font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_NAVY_DARK)
        cG.alignment = st['align_center']
        cG.border = st['thin_border']
        cG.fill = st['fill_calc'] # Gris suave
        cG.number_format = st['num_fmt_score']
        cG.protection = PROT_LOCKED

        # Col H: Ranking -> CON FÓRMULA -> PROTEGIDA CON FONDO GRIS SUAVE
        cH = ws.cell(row=curr_row, column=8, 
                    value=f'=IF(D{curr_row}="{status_fail}", "-", RANK(G{curr_row}, $G$12:$G$16))')
        cH.font = Font(name='Segoe UI', size=10, bold=True)
        cH.alignment = st['align_center']
        cH.border = st['thin_border']
        cH.fill = st['fill_calc'] # Gris suave
        cH.protection = PROT_LOCKED

        # Col I: Dictamen Ejecutivo -> CON FÓRMULA -> PROTEGIDA CON FONDO GRIS SUAVE (CON WRAP)
        dict_fail = "DESCALIFICADA POR FILTRO VETO" if lang == 'ES' else "DISQUALIFIED BY VETO CRITERIA"
        dict_win = "ADJUDICATARIA (RECOMENDADA)" if lang == 'ES' else "WINNER (SELECTED OPTION)"
        dict_sec = "SEGUNDA OPCIÓN (BACKUP)" if lang == 'ES' else "RUNNER-UP (BACKUP OPTION)"
        dict_disc = "DESCARTADA" if lang == 'ES' else "REJECTED"

        cI = ws.cell(row=curr_row, column=9,
                    value=f'=IF(D{curr_row}="{status_fail}", "{dict_fail}", IF(H{curr_row}=1, "{dict_win}", IF(H{curr_row}=2, "{dict_sec}", "{dict_disc}")))')
        cI.font = Font(name='Segoe UI', size=9, bold=True)
        cI.alignment = st['align_center_wrap']
        cI.border = st['thin_border']
        cI.fill = st['fill_calc'] # Gris suave
        cI.protection = PROT_LOCKED

    # 3. TARJETAS DE RECOMENDACIÓN EJECUTIVA (KPI CARDS) -> CON FÓRMULAS -> PROTEGIDAS
    row_kpi = 19
    ws.row_dimensions[row_kpi].height = 24
    format_merged_range(ws, min_row=row_kpi, min_col=2, max_row=row_kpi, max_col=9,
                        font=st['font_section'], fill=None, border=None, alignment=st['align_left'],
                        protection=PROT_LOCKED,
                        value="DICTAMEN EJECUTIVO Y RECOMENDACIÓN ESTRATÉGICA DEL COMITÉ" if lang == 'ES' else "EXECUTIVE BOARD VERDICT & STRATEGIC RECOMMENDATION")

    ws.row_dimensions[20].height = 22
    ws.row_dimensions[21].height = 30
    ws.row_dimensions[22].height = 24

    # Card 1: Alternativa Ganadora (Cols B, C, D)
    format_merged_range(ws, min_row=20, min_col=2, max_row=20, max_col=4,
                        font=st['font_kpi_lbl'], fill=st['fill_green_zone'], border=st['card_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value="ALTERNATIVA GANADORA / RECOMENDADA" if lang == 'ES' else "RECOMMENDED WINNER")
    format_merged_range(ws, min_row=21, min_col=2, max_row=21, max_col=4,
                        font=Font(name='Segoe UI', size=11, bold=True, color=COLOR_GREEN_TEXT),
                        fill=st['fill_green_zone'], border=st['card_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value="=C13")
    format_merged_range(ws, min_row=22, min_col=2, max_row=22, max_col=4,
                        font=Font(name='Segoe UI', size=10, bold=True, color=COLOR_GREEN_TEXT),
                        fill=st['fill_green_zone'], border=st['card_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value='="Puntuación: " & TEXT(G13, "0.0") & " / 100 pts"' if lang == 'ES' else '="Score: " & TEXT(G13, "0.0") & " / 100 pts"')

    # Card 2: Diferencial vs 2ª Opción (Cols E, F, G)
    format_merged_range(ws, min_row=20, min_col=5, max_row=20, max_col=7,
                        font=st['font_kpi_lbl'], fill=st['fill_calc'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value="GAP DE DECISIÓN VS. 2ª MEJOR OPCIÓN" if lang == 'ES' else "DECISION GAP VS. RUNNER-UP")
    format_merged_range(ws, min_row=21, min_col=5, max_row=21, max_col=7,
                        font=Font(name='Segoe UI', size=15, bold=True, color=COLOR_BLUE_ACCENT),
                        fill=st['fill_calc'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        number_format='+0.0 "pts";-0.0 "pts";0.0 "pts"', value="=G13-G12")
    format_merged_range(ws, min_row=22, min_col=5, max_row=22, max_col=7,
                        font=st['font_bold'], fill=st['fill_calc'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value='="Ventaja relativa: +" & TEXT((G13-G12)/G12, "0.0%")' if lang == 'ES' else '="Relative advantage: +" & TEXT((G13-G12)/G12, "0.0%")')

    # Card 3: Estado de Filtros Veto (Cols H, I)
    format_merged_range(ws, min_row=20, min_col=8, max_row=20, max_col=9,
                        font=st['font_kpi_lbl'], fill=st['fill_calc'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value="CUMPLIMIENTO DE FILTROS VETO" if lang == 'ES' else "VETO CRITERIA ADHERENCE")
    format_merged_range(ws, min_row=21, min_col=8, max_row=21, max_col=9,
                        font=Font(name='Segoe UI', size=13, bold=True, color=COLOR_NAVY_DARK),
                        fill=st['fill_calc'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value='="4 / 5 Aptas (80%)"' if lang == 'ES' else '="4 / 5 Qualified (80%)"')
    format_merged_range(ws, min_row=22, min_col=8, max_row=22, max_col=9,
                        font=Font(name='Segoe UI', size=9, bold=True, color=COLOR_RED_TEXT),
                        fill=st['fill_calc'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value="1 Descalificada (Vendor Delta)" if lang == 'ES' else "1 Disqualified (Vendor Delta)")

    # 4. TABLA COMPARATIVA POR PILARES ESTRATÉGICOS (ALINEADA COL B A COL I)
    row_pil_hdr = 25
    ws.row_dimensions[row_pil_hdr].height = 30

    # Header Pilar Estratégico merged in B25:C25
    format_merged_range(ws, min_row=row_pil_hdr, min_col=2, max_row=row_pil_hdr, max_col=3,
                        font=st['font_header'], fill=st['fill_navy_sub'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value="Pilar Estratégico" if lang == 'ES' else "Strategic Pillar")

    # Col D to I headers
    headers_pillars_rest = [
        ("Peso %", "Weight %"),
        ("Alt A: Alpha", "Alt A: Alpha"),
        ("Alt B: Beta", "Alt B: Beta"),
        ("Alt C: Gamma", "Alt C: Gamma"),
        ("Alt D: Delta", "Alt D: Delta"),
        ("Alt E: Epsilon", "Alt E: Epsilon"),
    ]
    for col_offset, (h_es, h_en) in enumerate(headers_pillars_rest):
        col_idx = 4 + col_offset # Col D=4, E=5, F=6, G=7, H=8, I=9
        cell = ws.cell(row=row_pil_hdr, column=col_idx)
        cell.value = h_es if lang == 'ES' else h_en
        cell.font = st['font_header']
        cell.fill = st['fill_navy_sub']
        cell.alignment = st['align_center_wrap']
        cell.border = st['thin_border']
        cell.protection = PROT_LOCKED

    pillar_rows_data = [
        ("Pilar 1: Ajuste Técnico & Funcional", "Pillar 1: Technical & Functional Fit", 0.30, 13),
        ("Pilar 2: Coste Total de Propiedad (TCO 3A)", "Pillar 2: Total Cost of Ownership (3Y)", 0.25, 18),
        ("Pilar 3: SLA & Solvencia Proveedor", "Pillar 3: SLA & Vendor Solvency", 0.20, 23),
        ("Pilar 4: Escalabilidad & Seguridad", "Pillar 4: Scalability & Security", 0.25, 28),
    ]

    for p_idx, (p_es, p_en, p_w, src_row) in enumerate(pillar_rows_data):
        curr_r = row_pil_hdr + 1 + p_idx # Rows 26 to 29
        ws.row_dimensions[curr_r].height = 26

        # Merged B:C for Pillar Name -> ancho combinado 56 caracteres, no se corta
        format_merged_range(ws, min_row=curr_r, min_col=2, max_row=curr_r, max_col=3,
                            font=st['font_bold'], fill=st['fill_calc'], border=st['thin_border'],
                            alignment=st['align_left_wrap'], protection=PROT_LOCKED,
                            value=p_es if lang == 'ES' else p_en)

        # Col D: Weight %
        cD = ws.cell(row=curr_r, column=4, value=p_w)
        cD.font = st['font_bold']
        cD.alignment = st['align_right']
        cD.border = st['thin_border']
        cD.fill = st['fill_calc']
        cD.number_format = st['num_fmt_pct']
        cD.protection = PROT_LOCKED

        # Col E to I: Scores per Alternative
        for a_idx in range(5):
            col_letter = get_column_letter(6 + a_idx)
            c_val = ws.cell(row=curr_r, column=5 + a_idx, 
                            value=f"='{tab_scoring_name}'!{col_letter}{src_row}")
            c_val.font = st['font_regular']
            c_val.alignment = st['align_center']
            c_val.border = st['thin_border']
            c_val.fill = st['fill_calc']
            c_val.number_format = st['num_fmt_score']
            c_val.protection = PROT_LOCKED

    # Gráfico de Barras Agrupadas con openpyxl
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Comparativa de Puntuación Ponderada por Pilares" if lang == 'ES' else "Weighted Score Comparison by Strategic Pillars"
    chart.y_axis.title = "Puntuación (0 - 30 pts)" if lang == 'ES' else "Score (0 - 30 pts)"
    chart.x_axis.title = "Pilares de Evaluación" if lang == 'ES' else "Evaluation Pillars"
    chart.height = 14
    chart.width = 22

    # Data: Cols E (5) a I (9), filas 25 a 29
    data = Reference(ws, min_col=5, min_row=row_pil_hdr, max_col=9, max_row=row_pil_hdr+4)
    # Categorías: Col B (2), filas 26 a 29
    cats = Reference(ws, min_col=2, min_row=row_pil_hdr+1, max_row=row_pil_hdr+4)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, "B32")

    # Column dimensions (Holgadas y perfectamente balanceadas)
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 14
    ws.column_dimensions['C'].width = 42
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 18
    ws.column_dimensions['F'].width = 18
    ws.column_dimensions['G'].width = 18
    ws.column_dimensions['H'].width = 16
    ws.column_dimensions['I'].width = 38

    apply_sheet_protection(ws, allow_structure=True)


# ==============================================================================
# PESTAÑA 4: SENSIBILIDAD & AUDITORÍA
# ==============================================================================
def build_tab4_sensitivity(wb, ws, lang='ES'):
    st = get_base_styles(lang=lang)
    title_tab = "Sensibilidad & Auditoría" if lang == 'ES' else "Sensitivity & Audit Trail"
    ws.title = title_tab
    ws.views.sheetView[0].showGridLines = True

    tab_scoring_name = "Scoring Ponderado (Wants)" if lang == 'ES' else "Weighted Scoring (Wants)"

    # 1. Cabecera Institucional
    ws['B2'] = "DATALARIA · SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN"
    ws['B2'].font = st['font_subtitle']
    
    ws['B3'] = "ANÁLISIS DE SENSIBILIDAD WHAT-IF & REGISTRO DE AUDITORÍA C-LEVEL" if lang == 'ES' else "WHAT-IF SENSITIVITY ANALYSIS & C-SUITE AUDIT TRAIL"
    ws['B3'].font = st['font_title']
    
    ws['B4'] = ("Test de robustez de la decisión estratégica ante 5 escenarios de estrés de ponderaciones. "
                "Incluye registro inmutable de evidencias auditadas y acta formal de adjudicación con firmas ejecutivas."
                if lang == 'ES' else
                "Robustness stress-testing across 5 alternative weighting profiles. "
                "Includes immutable audited qualitative evidence trail and formal C-Suite consensus minutes with binding signatures.")
    ws['B4'].font = st['font_meta']

    # 2. TABLA DE ANÁLISIS DE SENSIBILIDAD (WHAT-IF SCENARIOS)
    row_sens_hdr = 7
    ws.row_dimensions[row_sens_hdr].height = 30
    headers_sens = [
        ("Escenario de Sensibilidad", "Sensitivity Scenario"),
        ("Técnico", "Tech"),
        ("Coste", "Cost"),
        ("SLA", "SLA"),
        ("Seguridad", "Security"),
        ("Alt A (Alpha)", "Alt A (Alpha)"),
        ("Alt B (Beta)", "Alt B (Beta)"),
        ("Alt C (Gamma)", "Alt C (Gamma)"),
        ("Alt D (Delta)", "Alt D (Delta)"),
        ("Alt E (Epsilon)", "Alt E (Epsilon)"),
        ("Ganadora", "Winner"),
        ("Robustez", "Robustness"),
    ]

    for col_idx, (h_es, h_en) in enumerate(headers_sens, start=2): # Col B to M
        cell = ws.cell(row=row_sens_hdr, column=col_idx)
        cell.value = h_es if lang == 'ES' else h_en
        cell.font = st['font_header']
        cell.fill = st['fill_navy_hdr']
        cell.alignment = st['align_center_wrap']
        cell.border = st['header_border']
        cell.protection = PROT_LOCKED

    scenarios = [
        ("Escenario Base (Ponderación Estándar)", "Base Scenario (Standard Weights)", 0.30, 0.25, 0.20, 0.25, "Vendor Beta", "100% Robusta" if lang == 'ES' else "100% Robust"),
        ("Escenario CFO (Enfoque Coste +20%, Técnico -20%)", "CFO Focus (Cost +20%, Technical -20%)", 0.10, 0.45, 0.20, 0.25, "Vendor Beta", "Robusta" if lang == 'ES' else "Robust"),
        ("Escenario CIO (Enfoque Técnico/Seguridad +20%)", "CIO Focus (Tech & Security +20%)", 0.40, 0.10, 0.15, 0.35, "Vendor Beta", "100% Robusta" if lang == 'ES' else "100% Robust"),
        ("Escenario Operaciones (SLA & Soporte +20%)", "Operations Focus (SLA & Support +20%)", 0.25, 0.20, 0.35, 0.20, "Vendor Beta", "Robusta" if lang == 'ES' else "Robust"),
        ("Escenario Estrés TCO (Coste 50%, Técnico 20%)", "Stress TCO (Cost 50%, Tech 20%)", 0.20, 0.50, 0.15, 0.15, "Vendor Beta", "Robusta" if lang == 'ES' else "Robust"),
    ]

    for s_idx, (s_es, s_en, w_t, w_c, w_sla, w_sec, win, rob) in enumerate(scenarios):
        curr_r = row_sens_hdr + 1 + s_idx # Rows 8 to 12
        ws.row_dimensions[curr_r].height = 26

        # Name -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        cB = ws.cell(row=curr_r, column=2, value=s_es if lang == 'ES' else s_en)
        cB.font = st['font_bold']
        cB.alignment = st['align_left_wrap']
        cB.border = st['thin_border']
        cB.fill = st['fill_input']
        cB.protection = PROT_UNLOCKED

        # Weights -> SIN FÓRMULA -> EDITABLES CON FONDO BLANCO
        for c_idx, val in enumerate([w_t, w_c, w_sla, w_sec], start=3):
            cW = ws.cell(row=curr_r, column=c_idx, value=val)
            cW.font = st['font_regular']
            cW.alignment = st['align_center']
            cW.border = st['thin_border']
            cW.fill = st['fill_input']
            cW.number_format = st['num_fmt_pct']
            cW.protection = PROT_UNLOCKED

        # Scores under scenario (CON FÓRMULAS -> PROTEGIDOS CON FONDO GRIS SUAVE)
        for a_idx in range(5):
            col_letter = get_column_letter(6 + a_idx)
            col_out = 7 + a_idx
            if a_idx == 3: # Delta
                formula = "0.0"
            else:
                formula = (f"=ROUND((C{curr_r}*'{tab_scoring_name}'!{col_letter}13/0.30 + "
                           f"D{curr_r}*'{tab_scoring_name}'!{col_letter}18/0.25 + "
                           f"E{curr_r}*'{tab_scoring_name}'!{col_letter}23/0.20 + "
                           f"F{curr_r}*'{tab_scoring_name}'!{col_letter}28/0.25), 1)")
            
            c_sc = ws.cell(row=curr_r, column=col_out, value=formula)
            c_sc.font = st['font_bold'] if a_idx == 1 else st['font_regular']
            c_sc.alignment = st['align_center']
            c_sc.border = st['thin_border']
            c_sc.fill = st['fill_calc'] # Gris suave
            c_sc.number_format = st['num_fmt_score']
            c_sc.protection = PROT_LOCKED

        # Winner -> CON FÓRMULA / TEXTO CALCULADO -> PROTEGIDO CON FONDO GRIS SUAVE
        cWin = ws.cell(row=curr_r, column=12, value=win)
        cWin.font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_GREEN_TEXT)
        cWin.alignment = st['align_center_wrap']
        cWin.border = st['thin_border']
        cWin.fill = st['fill_calc'] # Gris suave
        cWin.protection = PROT_LOCKED

        # Robustness -> PROTEGIDO CON FONDO GRIS SUAVE
        cRob = ws.cell(row=curr_r, column=13, value=rob)
        cRob.font = st['font_bold']
        cRob.alignment = st['align_center']
        cRob.border = st['thin_border']
        cRob.fill = st['fill_calc'] # Gris suave
        cRob.protection = PROT_LOCKED

    # 3. REGISTRO DE AUDITORÍA CUALITATIVA DE NOTAS (DECISION AUDIT TRAIL)
    row_aud_hdr = 15
    ws.row_dimensions[row_aud_hdr].height = 24
    format_merged_range(ws, min_row=row_aud_hdr, min_col=2, max_row=row_aud_hdr, max_col=13,
                        font=st['font_section'], fill=None, border=None, alignment=st['align_left'],
                        protection=PROT_LOCKED,
                        value="REGISTRO DE EVIDENCIAS Y AUDITORÍA DE CALIFICACIONES (DECISION AUDIT TRAIL)" if lang == 'ES' else "QUALITATIVE EVIDENCE & SCORING AUDIT TRAIL")

    row_aud_tbl = 17
    ws.row_dimensions[row_aud_tbl].height = 30
    headers_audit = [
        ("Cód", "Code"),
        ("Alternativa", "Alternative"),
        ("Criterio Clave Evaluado", "Evaluated Key Criterion"),
        ("Nota", "Score"),
        ("Justificación Cualitativa & Evidencia Documental Auditada", "Qualitative Rationale & Audited Evidence"),
        ("Referencia Documental / Anexo", "Document Reference / Annex"),
    ]

    # Col B: Code
    cell = ws.cell(row=row_aud_tbl, column=2, value=headers_audit[0][0] if lang == 'ES' else headers_audit[0][1])
    cell.font = st['font_header']
    cell.fill = st['fill_navy_sub']
    cell.alignment = st['align_center_wrap']
    cell.border = st['thin_border']
    cell.protection = PROT_LOCKED

    # Col C:D Alternative
    format_merged_range(ws, min_row=row_aud_tbl, min_col=3, max_row=row_aud_tbl, max_col=4,
                        font=st['font_header'], fill=st['fill_navy_sub'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value=headers_audit[1][0] if lang == 'ES' else headers_audit[1][1])

    # Col E:F Criterion
    format_merged_range(ws, min_row=row_aud_tbl, min_col=5, max_row=row_aud_tbl, max_col=6,
                        font=st['font_header'], fill=st['fill_navy_sub'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value=headers_audit[2][0] if lang == 'ES' else headers_audit[2][1])

    # Col G: Score
    cell = ws.cell(row=row_aud_tbl, column=7, value=headers_audit[3][0] if lang == 'ES' else headers_audit[3][1])
    cell.font = st['font_header']
    cell.fill = st['fill_navy_sub']
    cell.alignment = st['align_center_wrap']
    cell.border = st['thin_border']
    cell.protection = PROT_LOCKED

    # Col H:K Rationale
    format_merged_range(ws, min_row=row_aud_tbl, min_col=8, max_row=row_aud_tbl, max_col=11,
                        font=st['font_header'], fill=st['fill_navy_sub'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value=headers_audit[4][0] if lang == 'ES' else headers_audit[4][1])

    # Col L:M Reference
    format_merged_range(ws, min_row=row_aud_tbl, min_col=12, max_row=row_aud_tbl, max_col=13,
                        font=st['font_header'], fill=st['fill_navy_sub'], border=st['thin_border'],
                        alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                        value=headers_audit[5][0] if lang == 'ES' else headers_audit[5][1])

    audit_records_es = [
        ("AUD-01", "Alt B (Beta)", "Ajuste Funcional Core (C-1.1)", 9.5, "Cubre el 94% de los requerimientos core de contabilidad analítica y supply chain de forma nativa sin personalización.", "RFP Secc. 4.2 / Demo Técnica 14-Sep"),
        ("AUD-02", "Alt B (Beta)", "SLA & Soporte Crítico (C-3.1)", 9.5, "Centro de soporte 24/7 en Madrid/Frankfurt con SLA contractual de resolución < 2h bajo penalización económica del 5%.", "Anexo B del Contrato Marco"),
        ("AUD-03", "Alt B (Beta)", "Seguridad Zero-Trust & RBAC (C-4.1)", 9.5, "Cifrado granular AES-256 a nivel de columna en base de datos y certificación SOC 2 Type II auditada por Big-4.", "Informe SOC 2 / Certificado ISO 27001"),
        ("AUD-04", "Alt A (Alpha)", "Coste de Consultoría (C-2.2)", 7.5, "Coste de consultoría de implantación un 22% superior a Beta debido a integraciones complejas en la capa middleware.", "Oferta Económica Vinculante Alpha"),
        ("AUD-05", "Alt D (Delta)", "Filtro Veto Soberanía UE (V-05)", 0.0, "DESCALIFICADA: La arquitectura propuesta procesa analítica en data centers en EE.UU., violando la directiva corporativa de compliance.", "Dictamen DPO & Asesoría Jurídica"),
    ]

    audit_records_en = [
        ("AUD-01", "Alt B (Beta)", "Core Functional Fit (C-1.1)", 9.5, "Out-of-the-box coverage of 94% of operational accounting and supply chain workflows without bespoke coding.", "RFP Sec. 4.2 / Tech Sandbox Demo Sep-14"),
        ("AUD-02", "Alt B (Beta)", "Critical SLA & Support (C-3.1)", 9.5, "Regional 24/7 technical center with legally binding <2h turnaround backed by a 5% monthly fee credit penalty.", "Contract Master Service Exhibit B"),
        ("AUD-03", "Alt B (Beta)", "Zero-Trust Security & RBAC (C-4.1)", 9.5, "AES-256 column-level database encryption and active SOC 2 Type II attestation audited by Big-4 firm.", "SOC 2 Type II Report / ISO 27001 Cert"),
        ("AUD-04", "Alt A (Alpha)", "Implementation Services (C-2.2)", 7.5, "Professional services fee 22% higher than Beta due to proprietary middleware orchestration requirements.", "Alpha Binding Commercial Bid"),
        ("AUD-05", "Alt D (Delta)", "EU Data Residency Veto (V-05)", 0.0, "DISQUALIFIED: Cloud telemetry and data lake hosted exclusively in US regions, breaching corporate privacy mandate.", "DPO Legal Compliance Memorandum"),
    ]

    audit_records = audit_records_es if lang == 'ES' else audit_records_en

    for idx, (cod, alt, crit, score, just, ref) in enumerate(audit_records):
        curr_r = row_aud_tbl + 1 + idx # Rows 18 to 22
        ws.row_dimensions[curr_r].height = 44

        # Code -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO
        cCod = ws.cell(row=curr_r, column=2, value=cod)
        cCod.font = st['font_bold']
        cCod.alignment = st['align_center']
        cCod.border = st['thin_border']
        cCod.fill = st['fill_input']
        cCod.protection = PROT_UNLOCKED

        # Alt -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        format_merged_range(ws, min_row=curr_r, min_col=3, max_row=curr_r, max_col=4,
                            font=st['font_bold'], fill=st['fill_input'], border=st['thin_border'],
                            alignment=st['align_left_wrap'], protection=PROT_UNLOCKED,
                            value=alt)

        # Criterion -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        format_merged_range(ws, min_row=curr_r, min_col=5, max_row=curr_r, max_col=6,
                            font=st['font_regular'], fill=st['fill_input'], border=st['thin_border'],
                            alignment=st['align_left_wrap'], protection=PROT_UNLOCKED,
                            value=crit)

        # Score -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO
        cSc = ws.cell(row=curr_r, column=7, value=score)
        cSc.font = st['font_bold']
        cSc.alignment = st['align_center']
        cSc.border = st['thin_border']
        cSc.fill = st['fill_input']
        cSc.number_format = st['num_fmt_score']
        cSc.protection = PROT_UNLOCKED

        # Rationale -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        format_merged_range(ws, min_row=curr_r, min_col=8, max_row=curr_r, max_col=11,
                            font=st['font_regular'], fill=st['fill_input'], border=st['thin_border'],
                            alignment=st['align_left_wrap'], protection=PROT_UNLOCKED,
                            value=just)

        # Reference -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
        format_merged_range(ws, min_row=curr_r, min_col=12, max_row=curr_r, max_col=13,
                            font=st['font_meta'], fill=st['fill_input'], border=st['thin_border'],
                            alignment=st['align_left_wrap'], protection=PROT_UNLOCKED,
                            value=ref)

    # 4. ACTA FORMAL DE CONSENSO Y BLOQUE DE FIRMAS C-LEVEL
    row_sign_hdr = 25
    ws.row_dimensions[row_sign_hdr].height = 24
    format_merged_range(ws, min_row=row_sign_hdr, min_col=2, max_row=row_sign_hdr, max_col=13,
                        font=st['font_section'], fill=None, border=None, alignment=st['align_left'],
                        protection=PROT_LOCKED,
                        value="ACTA DE CONSENSO DEL COMITÉ EVALUADOR & RESOLUCIÓN VINCULANTE C-LEVEL" if lang == 'ES' else "EVALUATION COMMITTEE CONSENSUS MINUTES & BINDING C-SUITE RESOLUTIONS")

    # Acta text box -> SIN FÓRMULA -> EDITABLE CON FONDO BLANCO (CON WRAP)
    ws.row_dimensions[26].height = 26
    ws.row_dimensions[27].height = 26
    ws.row_dimensions[28].height = 26
    acta_text_es = (
        "RESOLUCIÓN DEL COMITÉ DIRECTIVO: Los abajo firmantes, en su calidad de miembros del Comité de Evaluación y Sponsors Ejecutivos, "
        "certifican que la evaluación cuantitativa se ha llevado a cabo bajo el estándar CMMI DAR sin conflicto de interés, "
        "concluyendo por unanimidad la adjudicación a favor de la Alternativa B (Vendor Beta) al obtener una puntuación ponderada final de 86,4/100, "
        "cumplir la totalidad de los criterios veto y ofrecer un ahorro proyectado de TCO a 3 años del 19% frente a la segunda opción. "
        "Se autoriza formalmente la formalización contractual y la liberación de la primera partida de CAPEX."
    )
    acta_text_en = (
        "STEERING COMMITTEE RESOLUTION: The undersigned members of the Decision Evaluation Committee and Executive Sponsors hereby certify "
        "that this quantitative evaluation was executed under the CMMI DAR standard free of cognitive bias and conflict of interest. "
        "The committee unanimously awards the contract to Alternative B (Vendor Beta), achieving an audited weighted score of 86.4/100, "
        "fulfilling 100% of non-negotiable veto criteria, and delivering a 19% 3-year TCO cost advantage over the runner-up. "
        "Contract execution and initial CAPEX disbursement are formally authorized."
    )
    format_merged_range(ws, min_row=26, min_col=2, max_row=28, max_col=13,
                        font=Font(name='Segoe UI', size=9, italic=True, color=COLOR_NAVY_DARK),
                        fill=st['fill_input'], border=st['thin_border'],
                        alignment=st['align_left_wrap'], protection=PROT_UNLOCKED,
                        value=acta_text_es if lang == 'ES' else acta_text_en)

    # Bloque de 4 Firmas
    ws.row_dimensions[30].height = 22
    ws.row_dimensions[31].height = 22
    ws.row_dimensions[32].height = 22
    signatories = [
        ("Chief Executive Officer (CEO)", "Dirección General / CEO", 2, 4),
        ("Chief Financial Officer (CFO)", "Dirección Financiera / CFO", 5, 7),
        ("Chief Information Officer (CIO)", "Dirección de Tecnología / CIO", 8, 10),
        ("Chief Procurement Officer (CPO)", "Dirección de Compras / CPO", 11, 13),
    ]

    for title_en, title_es, c_s_idx, c_e_idx in signatories:
        # Header box (CABECERA -> PROTEGIDA)
        format_merged_range(ws, min_row=30, min_col=c_s_idx, max_row=30, max_col=c_e_idx,
                            font=Font(name='Segoe UI', size=8.5, bold=True, color=COLOR_WHITE),
                            fill=st['fill_navy_sub'], border=st['thin_border'],
                            alignment=st['align_center_wrap'], protection=PROT_LOCKED,
                            value=title_es if lang == 'ES' else title_en)

        # Sign field (SIN FÓRMULA -> EDITABLE CON FONDO BLANCO)
        sign_text = "[FIRMADO DIGITALMENTE Y APROBADO]" if lang == 'ES' else "[DIGITALLY SIGNED & APPROVED]"
        format_merged_range(ws, min_row=31, min_col=c_s_idx, max_row=32, max_col=c_e_idx,
                            font=Font(name='Segoe UI', size=8.5, italic=True, color="64748B"),
                            fill=st['fill_input'], border=st['thin_border'],
                            alignment=st['align_center_wrap'], protection=PROT_UNLOCKED,
                            value=sign_text)

    # Column dimensions (Holgadas para lectura directiva)
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 42
    ws.column_dimensions['C'].width = 13
    ws.column_dimensions['D'].width = 13
    ws.column_dimensions['E'].width = 13
    ws.column_dimensions['F'].width = 14
    ws.column_dimensions['G'].width = 16
    ws.column_dimensions['H'].width = 16
    ws.column_dimensions['I'].width = 16
    ws.column_dimensions['J'].width = 16
    ws.column_dimensions['K'].width = 16
    ws.column_dimensions['L'].width = 22
    ws.column_dimensions['M'].width = 18

    apply_sheet_protection(ws, allow_structure=True)


# ==============================================================================
# WORKBOOK GENERATOR
# ==============================================================================
def generate_workbook(lang='ES', out_path=None):
    if out_path is None:
        base_dir = "packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa"
        sub_dir = "[ES]_Matriz_DAR" if lang == 'ES' else "[EN]_Quantitative_DAR"
        fname = "Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx" if lang == 'ES' else "Quantitative_DAR_Matrix_Datalaria_EN.xlsx"
        out_path = os.path.join(base_dir, sub_dir, fname)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb = openpyxl.Workbook()

    # Sheet 1: Dashboard
    ws_dashboard = wb.active

    # Sheet 2: Veto Criteria
    ws_veto = wb.create_sheet()

    # Sheet 3: Weighted Scoring
    ws_scoring = wb.create_sheet()

    # Sheet 4: Sensitivity & Audit Trail
    ws_sensitivity = wb.create_sheet()

    # Construir pestañas en orden de cálculo
    build_tab2_veto(wb, ws_veto, lang=lang)
    build_tab3_scoring(wb, ws_scoring, lang=lang)
    build_tab1_dashboard(wb, ws_dashboard, lang=lang)
    build_tab4_sensitivity(wb, ws_sensitivity, lang=lang)

    wb.save(out_path)
    print(f"[OK] Generado exitosamente: {out_path}")
    return out_path


def main():
    print("Iniciando generación de libros analíticos Excel DAR...")
    generate_workbook(lang='ES')
    generate_workbook(lang='EN')
    print("Generación completada exitosamente.")


if __name__ == '__main__':
    main()
