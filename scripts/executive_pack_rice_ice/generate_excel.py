#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos cuantitativos analíticos oficiales de Priorización Ágil RICE & ICE de Datalaria:
1. packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[ES]_Matriz_RICE_ICE/Matriz_RICE_ICE_Datalaria_ES.xlsx
2. packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[EN]_RICE_ICE_Matrix/RICE_ICE_Matrix_Datalaria_EN.xlsx

Arquitectura de 5 pestañas interconectadas:
- Pestaña 1: "Dashboard Ejecutivo" / "Executive Dashboard"
- Pestaña 2: "Backlog RICE" / "RICE Backlog" (hasta 30 iniciativas, 20 precargadas + 10 configuradas)
- Pestaña 3: "Experimentos ICE" / "ICE Experiments" (hasta 20 experimentos, 12 precargados + 8 configurados)
- Pestaña 4: "Capacidad & Roadmap" / "Capacity & Roadmap" (Now/Next/Later, semáforos de utilización)
- Pestaña 5: "Escalas & Calibración" / "Scales & Calibration" (Tablas maestras de Impacto y Confianza)

POLÍTICA DE PROTECCIÓN Y COMPATIBILIDAD (ECMA-376 / OpenXML):
- Celda sin fórmula: fondo #FFFFFF, locked=False (editable).
- Celda con fórmula: fondo #F1F5F9, locked=True (protegida).
- Cabeceras, títulos y tarjetas decorativas: registradas en decorative_cells.
- Fórmulas en inglés con comas: TODAY, IF, SUMIFS, SUMIF, INDEX, MATCH, LARGE, RANK, MEDIAN, ROUND, COUNTA, COUNTIF, MAX, AVERAGE.
- Compatibilidad garantizada con Microsoft Excel y Google Sheets.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import ScatterChart, Reference, Series, BarChart

from protection_policy import finalize_sheet

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = "0F172A"       # Slate 900
COLOR_NAVY_MED = "1E293B"        # Slate 800
COLOR_NAVY_LIGHT = "334155"      # Slate 700
COLOR_BLUE_ACCENT = "2563EB"     # Blue 600 (Consultoría)
COLOR_BLUE_LIGHT = "EFF6FF"      # Blue 50

COLOR_GREEN_BG = "D1FAE5"        # Quick Wins / Holgura
COLOR_GREEN_TEXT = "065F46"
COLOR_GREEN_BORDER = "10B981"

COLOR_AMBER_BG = "FEF3C7"        # Capacidad Plena / Big Bets
COLOR_AMBER_TEXT = "92400E"
COLOR_AMBER_BORDER = "F59E0B"

COLOR_RED_BG = "FEE2E2"          # Pozos sin Fondo / Fuera de Corte
COLOR_RED_TEXT = "991B1B"
COLOR_RED_BORDER = "EF4444"

COLOR_BG_CARD = "F8FAFC"         # Slate 50
COLOR_WHITE = "FFFFFF"
COLOR_BORDER_LIGHT = "CBD5E1"    # Slate 300
COLOR_BORDER_MED = "94A3B8"      # Slate 400

FONT_NAME = "Segoe UI"


def create_borders():
    thin = Side(style='thin', color=COLOR_BORDER_LIGHT)
    med = Side(style='medium', color=COLOR_NAVY_MED)
    double = Side(style='double', color=COLOR_NAVY_DARK)

    return {
        'thin': Border(left=thin, right=thin, top=thin, bottom=thin),
        'header': Border(left=thin, right=thin, top=med, bottom=med),
        'total': Border(left=thin, right=thin, top=thin, bottom=double),
        'card': Border(left=med, right=thin, top=thin, bottom=thin),
    }


def build_tab5_scales(wb, lang='ES'):
    """Construye la Pestaña 5: Escalas & Calibración / Scales & Calibration."""
    sheet_title = "Escalas & Calibración" if lang == 'ES' else "Scales & Calibration"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    # 1. Cabecera Principal
    ws.merge_cells("B2:E3")
    top_cell = ws["B2"]
    top_cell.value = (
        "CALIBRACIÓN METODOLÓGICA: ESCALAS CANÓNICAS RICE & ICE"
        if lang == 'ES' else
        "METHODOLOGICAL CALIBRATION: CANONICAL RICE & ICE SCALES"
    )
    top_cell.font = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
    top_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)
    top_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 20

    for r in range(2, 4):
        for c in range(2, 6):
            coord = f"{get_column_letter(c)}{r}"
            decorative.add(coord)
            ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)

    # 2. SECCIÓN A: Escala de Impacto
    sec1_title = "1. ESCALA DE IMPACTO RICE (ESTÁNDAR INTERCOM)" if lang == 'ES' else "1. RICE IMPACT SCALE (INTERCOM STANDARD)"
    ws["B5"].value = sec1_title
    ws["B5"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["B5"].alignment = Alignment(vertical="center")
    decorative.add("B5")

    h_labels = ["Etiqueta Desplegable", "Multiplicador Numérico", "Definición Operativa & Evidencia Requerida"] if lang == 'ES' else [
        "Dropdown Label", "Numeric Multiplier", "Operational Definition & Evidentiary Standard"
    ]
    for i, h in enumerate(h_labels, start=2):
        col_let = get_column_letter(i)
        coord = f"{col_let}6"
        ws[coord].value = h
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if i != 4 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)
    ws.row_dimensions[6].height = 24

    impact_data_es = [
        ("Masivo (3.0)", 3.0, "Multiplica el valor del producto x3 o impacta a >80% de usuarios core"),
        ("Alto (2.0)", 2.0, "Mejora sustancial en conversión, retención o ARR en segmento prioritario"),
        ("Medio (1.0)", 1.0, "Impacto notable pero acotado a un flujo secundario o squad específico"),
        ("Bajo (0.5)", 0.5, "Mejora incremental menor en satisfacción o eficiencia operativa"),
        ("Mínimo (0.25)", 0.25, "Ajuste cosmético o corrección puntual de muy baja tracción"),
    ]
    impact_data_en = [
        ("Massive (3.0)", 3.0, "Triples core product value or impacts >80% of active enterprise user base"),
        ("High (2.0)", 2.0, "Substantial uplift in conversion, retention, or ARR expansion"),
        ("Medium (1.0)", 1.0, "Noticeable improvement across secondary workflow or dedicated squad"),
        ("Low (0.5)", 0.5, "Minor incremental improvement in user satisfaction or ticket resolution"),
        ("Minimal (0.25)", 0.25, "Cosmetic adjustment or edge-case fix with negligible adoption impact"),
    ]
    impact_data = impact_data_es if lang == 'ES' else impact_data_en

    for idx, (label, val, desc) in enumerate(impact_data, start=7):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"B{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = val
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"C{idx}"].number_format = "0.00"
        ws[f"C{idx}"].border = borders['thin']

        ws[f"D{idx}"].value = desc
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"D{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"D{idx}"].border = borders['thin']
        ws.row_dimensions[idx].height = 26

    # 3. SECCIÓN B: Escala de Confianza (Confidence Meter)
    sec2_title = "2. ESCALA DE CONFIANZA RICE (CONFIDENCE METER - ITAMAR GILAD)" if lang == 'ES' else "2. RICE CONFIDENCE METER (ITAMAR GILAD STANDARD)"
    ws["B14"].value = sec2_title
    ws["B14"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["B14"].alignment = Alignment(vertical="center")
    decorative.add("B14")

    h2_labels = ["Nivel de Confianza", "Factor Probabilidad", "Evidencia Exigida / Grado de Validación Experimental"] if lang == 'ES' else [
        "Confidence Tier", "Probability Factor", "Required Evidentiary Standard & Validation Rigor"
    ]
    for i, h in enumerate(h2_labels, start=2):
        col_let = get_column_letter(i)
        coord = f"{col_let}15"
        ws[coord].value = h
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if i != 4 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)
    ws.row_dimensions[15].height = 24

    conf_data_es = [
        ("Alta (100%)", 1.0, "Test A/B con significación estadística >95%, telemetría masiva o prototipo validado"),
        ("Media (80%)", 0.8, "Encuesta cuantitativa a 50+ clientes, datos analíticos o benchmarking de mercado"),
        ("Baja (50%)", 0.5, "Opinión de producto, intuición preliminar, petición aislada de ventas o hipótesis no probada"),
    ]
    conf_data_en = [
        ("High (100%)", 1.0, "Statistically significant A/B test (>95% conf.), live telemetry, or prototype testing"),
        ("Medium (80%)", 0.8, "Quantitative customer survey (50+ accounts), analytics event tracking, or peer benchmark"),
        ("Low (50%)", 0.5, "Product hunch, unvalidated customer feedback, anecdotal sales request, or unverified hypothesis"),
    ]
    conf_data = conf_data_es if lang == 'ES' else conf_data_en

    for idx, (label, val, desc) in enumerate(conf_data, start=16):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"B{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = val
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"C{idx}"].number_format = "0.0%"
        ws[f"C{idx}"].border = borders['thin']

        ws[f"D{idx}"].value = desc
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"D{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"D{idx}"].border = borders['thin']
        ws.row_dimensions[idx].height = 28

    # 4. SECCIÓN C: Guía de Estimación de Reach y Effort
    sec3_title = "3. GUÍA DE ESTIMACIÓN CANÓNICA DE REACH (ALCANCE) Y EFFORT (ESFUERZO)" if lang == 'ES' else "3. CANONICAL ESTIMATION GUIDELINES: REACH & EFFORT"
    ws["B21"].value = sec3_title
    ws["B21"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["B21"].alignment = Alignment(vertical="center")
    decorative.add("B21")

    h3_labels = ["Parámetro", "Unidad Canónica", "Regla de Estimación & Buenas Prácticas"] if lang == 'ES' else [
        "Parameter", "Canonical Unit", "Estimation Protocol & Industry Best Practice"
    ]
    for i, h in enumerate(h3_labels, start=2):
        col_let = get_column_letter(i)
        coord = f"{col_let}22"
        ws[coord].value = h
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if i != 4 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)
    ws.row_dimensions[22].height = 24

    guide_data_es = [
        ("Reach (Alcance)", "Usuarios o Eventos / Trimestre", "Número absoluto de usuarios, transacciones o cuentas alcanzadas durante el trimestre de lanzamiento. Usar métricas de analítica (ej. 15.000 DAU)."),
        ("Effort (Esfuerzo)", "Persona-Mes (PM)", "Trabajo total combinado de ingeniería, producto y diseño (1 PM = 1 profesional a dedicación completa durante 1 mes = aprox. 160h). Mínimo 0.5 PM."),
        ("ICE: Impact (1-10)", "Escala 1 a 10", "Magnitud del impacto sobre la métrica North Star del experimento (1 = imperceptible; 10 = crecimiento x2)."),
        ("ICE: Ease (1-10)", "Escala 1 a 10", "Facilidad de ejecución y despliegue rápido del test (10 = < 1 día de setup sin código; 1 = semanas de desarrollo complejo)."),
    ]
    guide_data_en = [
        ("Reach", "Users or Events / Quarter", "Absolute number of unique users, accounts, or events impacted in the target quarter. Must be rooted in telemetry (e.g. 15,000 active users)."),
        ("Effort", "Person-Months (PM)", "Combined cross-functional engineering, UX, and QA effort (1 PM = 1 full-time person for 1 month = ~160 hours). Minimum 0.5 PM."),
        ("ICE: Impact (1-10)", "Scale 1 to 10", "Magnitude of anticipated lift on North Star metric (1 = negligible; 10 = doubles conversion rate or volume)."),
        ("ICE: Ease (1-10)", "Scale 1 to 10", "Simplicity and deployment velocity of the experiment (10 = <1 day no-code test; 1 = complex multi-week engineering refactor)."),
    ]
    guide_data = guide_data_es if lang == 'ES' else guide_data_en

    for idx, (param, unit, desc) in enumerate(guide_data, start=23):
        ws[f"B{idx}"].value = param
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"B{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = unit
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_MED)
        ws[f"C{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"C{idx}"].border = borders['thin']

        ws[f"D{idx}"].value = desc
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"D{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"D{idx}"].border = borders['thin']
        ws.row_dimensions[idx].height = 32

    # Anchos de columna
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 24
    ws.column_dimensions["D"].width = 80
    ws.column_dimensions["E"].width = 6

    finalize_sheet(ws, decorative_cells=frozenset(decorative))
    print(f"  [OK] Pestaña '{sheet_title}' creada con éxito.")
    return sheet_title


def build_tab4_capacity(wb, lang='ES'):
    """Construye la Pestaña 4: Capacidad & Roadmap / Capacity & Roadmap."""
    sheet_title = "Capacidad & Roadmap" if lang == 'ES' else "Capacity & Roadmap"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    # 1. Título
    ws.merge_cells("B2:H3")
    top_cell = ws["B2"]
    top_cell.value = (
        "MODELO DE CAPACIDAD TRIMESTRAL & ASIGNACIÓN DE ROADMAP"
        if lang == 'ES' else
        "QUARTERLY TEAM CAPACITY MODEL & ROADMAP ALLOCATION"
    )
    top_cell.font = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
    top_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)
    top_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 20

    for r in range(2, 4):
        for c in range(2, 9):
            coord = f"{get_column_letter(c)}{r}"
            decorative.add(coord)
            ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)

    # 2. SECCIÓN A: Parámetros de Capacidad de Ingeniería
    sec1_title = "1. PARÁMETROS DE CAPACIDAD DEL EQUIPO (SQUADS & BUFFERS)" if lang == 'ES' else "1. TEAM CAPACITY CONFIGURATION (SQUADS & BUFFERS)"
    ws["B5"].value = sec1_title
    ws["B5"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["B5"].alignment = Alignment(vertical="center")
    decorative.add("B5")

    params_labels_es = [
        ("B6", "Número de Squads de Producto Dedicados:", "D6", 3, "Squads independientes"),
        ("B7", "Capacidad Bruta por Squad (Persona-Mes / Trimestre):", "D7", 12.0, "PM / Squad / Trimestre"),
        ("B8", "Capacidad Bruta Total del Equipo (Persona-Mes / Q):", "D8", "=D6*D7", "PM Brutos / Trimestre"),
        ("B9", "Buffer Reservado a Deuda Técnica, Incidencias & On-Call (%):", "D9", 0.167, "% de holgura operativa"),
        ("B10", "Buffer Trimestral Reservado (Persona-Mes):", "D10", "=ROUND(D8*D9,1)", "PM reservados para mantenimiento"),
        ("B11", "Capacidad Neta Trimestral Disponible para Roadmap (K):", "D11", "=D8-D10", "PM Netos disponibles por Trimestre"),
    ]
    params_labels_en = [
        ("B6", "Number of Dedicated Product Squads:", "D6", 3, "Cross-functional squads"),
        ("B7", "Gross Capacity per Squad (Person-Months / Quarter):", "D7", 12.0, "PM / Squad / Quarter"),
        ("B8", "Total Gross Team Capacity (Person-Months / Q):", "D8", "=D6*D7", "Gross PM / Quarter"),
        ("B9", "Technical Debt, Bugs & Maintenance Buffer (%):", "D9", 0.167, "% allocated to debt/bugs"),
        ("B10", "Reserved Quarterly Maintenance Buffer (Person-Months):", "D10", "=ROUND(D8*D9,1)", "PM reserved for KTLO/debt"),
        ("B11", "Net Quarterly Available Roadmap Capacity (K):", "D11", "=D8-D10", "Net PM available per Quarter"),
    ]
    params_data = params_labels_es if lang == 'ES' else params_labels_en

    for b_coord, lbl, d_coord, val, note in params_data:
        ws.merge_cells(f"{b_coord}:C{b_coord[1:]}")
        ws[b_coord].value = lbl
        ws[b_coord].font = Font(name=FONT_NAME, size=10, bold=(b_coord in ["B8", "B11"]), color=COLOR_NAVY_DARK)
        ws[b_coord].alignment = Alignment(horizontal="left", vertical="center")
        ws[b_coord].border = borders['thin']
        ws[f"C{b_coord[1:]}"].border = borders['thin']

        ws[d_coord].value = val
        ws[d_coord].font = Font(name=FONT_NAME, size=10, bold=(b_coord in ["B8", "B11"]), color=COLOR_NAVY_DARK if b_coord != "B11" else COLOR_BLUE_ACCENT)
        ws[d_coord].alignment = Alignment(horizontal="right", vertical="center")
        ws[d_coord].border = borders['thin']
        if b_coord == "B9":
            ws[d_coord].number_format = "0.0%"
        elif b_coord in ["B7", "B8", "B10", "B11"]:
            ws[d_coord].number_format = "0.0"
        else:
            ws[d_coord].number_format = "0"

        ws.merge_cells(f"E{b_coord[1:]}:G{b_coord[1:]}")
        ws[f"E{b_coord[1:]}"].value = note
        ws[f"E{b_coord[1:]}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"E{b_coord[1:]}"].alignment = Alignment(horizontal="left", vertical="center")
        for col_l in ["E", "F", "G"]:
            ws[f"{col_l}{b_coord[1:]}"].border = borders['thin']

        ws.row_dimensions[int(b_coord[1:])].height = 22

    # 3. SECCIÓN B: Utilización y Línea de Corte Trimestral (Q1-Q4)
    sec2_title = "2. CUADRO DE CAPACIDAD TRIMESTRAL, ESFUERZO COMPROMETIDO & LÍNEA DE CORTE" if lang == 'ES' else "2. QUARTERLY UTILIZATION, COMMITTED EFFORT & CAPACITY CUT-LINE"
    ws["B13"].value = sec2_title
    ws["B13"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["B13"].alignment = Alignment(vertical="center")
    decorative.add("B13")

    h2_cols_es = ["Trimestre", "Capacidad Neta (PM)", "Capacidad Acumulada", "Esfuerzo Asignado (PM)", "Holgura / Saldo (PM)", "% Utilización", "Semáforo de Capacidad"]
    h2_cols_en = ["Quarter", "Net Capacity (PM)", "Cumulative Net Cap.", "Committed Effort (PM)", "Slack / Balance (PM)", "% Utilization", "Capacity Status"]
    h2_cols = h2_cols_es if lang == 'ES' else h2_cols_en

    for idx, h in enumerate(h2_cols, start=2):
        col_let = get_column_letter(idx)
        coord = f"{col_let}14"
        ws[coord].value = h
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws[coord].border = borders['header']
        decorative.add(coord)
    ws.row_dimensions[14].height = 26

    quarters = [
        ("Q1 (Now)", 15, "=$D$11", "=C15", "Q1"),
        ("Q2 (Next)", 16, "=$D$11", "=D15+C16", "Q2"),
        ("Q3 (Next)", 17, "=$D$11", "=D16+C17", "Q3"),
        ("Q4 (Later)", 18, "=$D$11", "=D17+C18", "Q4"),
    ]
    backlog_tab = "'Backlog RICE'" if lang == 'ES' else "'RICE Backlog'"

    for q_label, r_idx, net_f, cum_f, q_code in quarters:
        ws[f"B{r_idx}"].value = q_label
        ws[f"B{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"B{r_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"B{r_idx}"].border = borders['thin']

        ws[f"C{r_idx}"].value = net_f
        ws[f"C{r_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_DARK)
        ws[f"C{r_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"C{r_idx}"].number_format = "0.0"
        ws[f"C{r_idx}"].border = borders['thin']

        ws[f"D{r_idx}"].value = cum_f
        ws[f"D{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"D{r_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"D{r_idx}"].number_format = "0.0"
        ws[f"D{r_idx}"].border = borders['thin']

        ws[f"E{r_idx}"].value = f"=SUMIF({backlog_tab}!$T$8:$T$37,\"{q_code}\",{backlog_tab}!$H$8:$H$37)"
        ws[f"E{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"E{r_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"E{r_idx}"].number_format = "0.0"
        ws[f"E{r_idx}"].border = borders['thin']

        ws[f"F{r_idx}"].value = f"=C{r_idx}-E{r_idx}"
        ws[f"F{r_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_DARK)
        ws[f"F{r_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"F{r_idx}"].number_format = "0.0"
        ws[f"F{r_idx}"].border = borders['thin']

        ws[f"G{r_idx}"].value = f"=IF(C{r_idx}>0,E{r_idx}/C{r_idx},0)"
        ws[f"G{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"G{r_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"G{r_idx}"].number_format = "0.0%"
        ws[f"G{r_idx}"].border = borders['thin']

        # Semáforo
        status_f = (
            f'=IF(G{r_idx}<=0.85,"🟢 Holgura Óptima",IF(G{r_idx}<=1.0,"🟡 Capacidad Plena","🔴 Sobreasignado"))'
            if lang == 'ES' else
            f'=IF(G{r_idx}<=0.85,"🟢 Optimal Slack",IF(G{r_idx}<=1.0,"🟡 Full Capacity","🔴 Overallocated"))'
        )
        ws[f"H{r_idx}"].value = status_f
        ws[f"H{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"H{r_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"H{r_idx}"].border = borders['thin']
        ws.row_dimensions[r_idx].height = 22

    # Fila de Totales Anuales (Row 19)
    ws["B19"].value = "TOTAL ANUAL (Q1-Q4)" if lang == 'ES' else "FULL YEAR TOTAL (Q1-Q4)"
    ws["B19"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["B19"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B19"].border = borders['total']

    ws["C19"].value = "=SUM(C15:C18)"
    ws["C19"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["C19"].alignment = Alignment(horizontal="right", vertical="center")
    ws["C19"].number_format = "0.0"
    ws["C19"].border = borders['total']

    ws["D19"].value = "=D18"
    ws["D19"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
    ws["D19"].alignment = Alignment(horizontal="right", vertical="center")
    ws["D19"].number_format = "0.0"
    ws["D19"].border = borders['total']

    ws["E19"].value = "=SUM(E15:E18)"
    ws["E19"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["E19"].alignment = Alignment(horizontal="right", vertical="center")
    ws["E19"].number_format = "0.0"
    ws["E19"].border = borders['total']

    ws["F19"].value = "=C19-E19"
    ws["F19"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["F19"].alignment = Alignment(horizontal="right", vertical="center")
    ws["F19"].number_format = "0.0"
    ws["F19"].border = borders['total']

    ws["G19"].value = "=IF(C19>0,E19/C19,0)"
    ws["G19"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["G19"].alignment = Alignment(horizontal="right", vertical="center")
    ws["G19"].number_format = "0.0%"
    ws["G19"].border = borders['total']

    tot_status_f = (
        '=IF(G19<=0.85,"🟢 Holgura Óptima",IF(G19<=1.0,"🟡 Capacidad Plena","🔴 Sobreasignado"))'
        if lang == 'ES' else
        '=IF(G19<=0.85,"🟢 Optimal Slack",IF(G19<=1.0,"🟡 Full Capacity","🔴 Overallocated"))'
    )
    ws["H19"].value = tot_status_f
    ws["H19"].font = Font(name=FONT_NAME, size=10, bold=True)
    ws["H19"].alignment = Alignment(horizontal="center", vertical="center")
    ws["H19"].border = borders['total']
    ws.row_dimensions[19].height = 24

    # 4. SECCIÓN C: Cuadro de Mando Now / Next / Later
    sec3_title = "3. DISTRIBUCIÓN ESTRATÉGICA DEL ROADMAP (HORIZONTES NOW / NEXT / LATER)" if lang == 'ES' else "3. STRATEGIC ROADMAP HORIZONS: NOW / NEXT / LATER"
    ws["B22"].value = sec3_title
    ws["B22"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["B22"].alignment = Alignment(vertical="center")
    decorative.add("B22")

    h3_cols_es = ["Horizonte", "Trimestres", "Criterio de Inclusión", "Objetivo Estratégico & Acciones del Comité"]
    h3_cols_en = ["Horizon", "Quarters", "Inclusion Threshold", "Strategic Mandate & Council Actions"]
    h3_cols = h3_cols_es if lang == 'ES' else h3_cols_en

    for idx, h in enumerate(h3_cols, start=2):
        col_let = get_column_letter(idx)
        coord = f"{col_let}23"
        ws[coord].value = h
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if idx != 5 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)
    ws.row_dimensions[23].height = 24

    nnl_data_es = [
        ("NOW (Inmediato)", "Q1", "Top RICE acumulado <= 30 PM (Quick Wins prioritarios)", "Compromiso de entrega vinculante; sprints cerrados; recursos asignados al 100%"),
        ("NEXT (En Maduración)", "Q2 - Q3", "RICE alto acumulado entre 31 PM y 90 PM (Grandes Apuestas)", "Discovery avanzado, prototipado y refinamiento de arquitectura técnica previa a Q2"),
        ("LATER (Exploratorio)", "Q4 / Futuro", "Iniciativas entre 91 y 120 PM o dependientes de validación previa", "Reevaluación en cadencia trimestral; validar mediante experimentos ICE"),
        ("DESCARTE (Fuera de Capacidad)", "Backlog", "Esfuerzo acumulado > 120 PM o Pozos sin Fondo", "Congelación formal; evitar malgastar tiempo de ingeniería; liberar capacidad"),
    ]
    nnl_data_en = [
        ("NOW (Committed)", "Q1", "Top RICE items <= 30 PM (Priority Quick Wins)", "Binding execution commitment; locked sprints; engineering fully staffed"),
        ("NEXT (Planned)", "Q2 - Q3", "High RICE items between 31 PM and 90 PM (Strategic Big Bets)", "Active discovery, UX prototyping, and technical spike resolution prior to Q2"),
        ("LATER (Exploratory)", "Q4 / Future", "Initiatives between 91 PM and 120 PM requiring telemetry gates", "Quarterly review cadence; test viability through agile ICE growth experiments"),
        ("EXCLUDED (Cut-Off)", "Backlog", "Cumulative effort > 120 PM or Money Pit classification", "Formal cancellation/freeze; protects engineering focus; prevents feature factory"),
    ]
    nnl_data = nnl_data_es if lang == 'ES' else nnl_data_en

    for idx, (horiz, qtrs, crit, mandate) in enumerate(nnl_data, start=24):
        ws[f"B{idx}"].value = horiz
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"B{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = qtrs
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"C{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"C{idx}"].border = borders['thin']

        ws[f"D{idx}"].value = crit
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"D{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"D{idx}"].border = borders['thin']

        ws.merge_cells(f"E{idx}:H{idx}")
        ws[f"E{idx}"].value = mandate
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_MED)
        ws[f"E{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        for col_l in ["E", "F", "G", "H"]:
            ws[f"{col_l}{idx}"].border = borders['thin']

        ws.row_dimensions[idx].height = 34

    # Anchos de columnas
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 30
    ws.column_dimensions["E"].width = 24
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 18
    ws.column_dimensions["H"].width = 24

    finalize_sheet(ws, decorative_cells=frozenset(decorative))
    print(f"  [OK] Pestaña '{sheet_title}' creada con éxito.")
    return sheet_title


def build_tab3_ice(wb, lang='ES'):
    """Construye la Pestaña 3: Experimentos ICE / ICE Experiments."""
    sheet_title = "Experimentos ICE" if lang == 'ES' else "ICE Experiments"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    # 1. Cabecera Principal
    ws.merge_cells("A2:N3")
    top_cell = ws["A2"]
    top_cell.value = (
        "FRAMEWORK ICE DE EXPERIMENTACIÓN ÁGIL: GROWTH, ACTIVACIÓN & OPTIMIZACIÓN"
        if lang == 'ES' else
        "ICE AGILE GROWTH EXPERIMENTATION FRAMEWORK: TESTING & ACTIVATION"
    )
    top_cell.font = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
    top_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)
    top_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 20

    for r in range(2, 4):
        for c in range(1, 15):
            coord = f"{get_column_letter(c)}{r}"
            decorative.add(coord)
            ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)

    # 2. Cabecera de Columnas (Row 6)
    headers_es = [
        "ID", "Hipótesis del Experimento", "Métrica North Star Impactada",
        "Impacto (1-10)", "Confianza (1-10)", "Facilidad (1-10)", "Squad / Lead",
        "Fecha Test", "Resultado Observado / Aprendizaje",
        "Score ICE (I×C×E)", "Score ICE (Media)", "Desempate", "Ranking ICE", "Semáforo Prioridad"
    ]
    headers_en = [
        "ID", "Experiment Hypothesis", "Target North Star Metric",
        "Impact (1-10)", "Confidence (1-10)", "Ease (1-10)", "Squad / Lead",
        "Launch Date", "Observed Outcome / Learning",
        "ICE Score (I×C×E)", "ICE Score (Mean)", "Tiebreaker", "ICE Rank", "Priority Semaphore"
    ]
    headers = headers_es if lang == 'ES' else headers_en

    for idx, h in enumerate(headers, start=1):
        col_let = get_column_letter(idx)
        coord = f"{col_let}6"
        ws[coord].value = h
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws[coord].border = borders['header']
        decorative.add(coord)
    ws.row_dimensions[6].height = 34

    # 3. Datos Precargados (12 experimentos de crecimiento realistas)
    ice_experiments_es = [
        ("EXP-01", "Registro con 1 Clic con Google en el Hero de la Portada", "Tasa de Registro / Signup Conversion", 8, 9, 9, "Growth Squad", "2026-01-15", "Aumento del +24% en conversiones de registro sin fricción"),
        ("EXP-02", "Banner de Descuento del 20% en Suscripción Anual en el Checkout", "ARR Cobrado por Adelantado / Cashflow", 9, 8, 8, "Monetization Squad", "2026-01-22", "Incremento del +31% en adopción de planes anuales"),
        ("EXP-03", "Lista de Verificación de Onboarding Gamificada con Barra de Progreso", "Activación en Día 1 (D1 Activation)", 8, 8, 8, "Product-Led Squad", "2026-02-05", "Reducción del tiempo hasta el primer evento core de 4d a 1d"),
        ("EXP-04", "Prueba Gratuita de 14 Días sin Requerir Tarjeta de Crédito", "Volumen de Cuentas Nuevas Activas", 8, 7, 9, "Growth Squad", "2026-02-12", "Duplicó el volumen de pruebas; conversión a pago se mantuvo estable"),
        ("EXP-05", "Widget de Invitación a Compañeros de Equipo con Enlaces Mágicos", "Coeficiente Viral / K-Factor", 7, 7, 7, "Core Team Squad", "2026-02-20", "En preparación para fase beta"),
        ("EXP-06", "Encuesta de Cancelación Ofreciendo Pausa de Cuenta de 1 Mes", "Tasa de Churn Voluntario", 7, 6, 8, "Retention Squad", "2026-03-01", "Retuvo al 18% de usuarios que iban a darse de baja definitiva"),
        ("EXP-07", "Rediseño Ejecutivo del Correo Semanal de Resumen de Actividad", "Retención Semanal de Usuarios (WAU)", 6, 7, 7, "Marketing Ops", "2026-03-10", "Tasa de apertura aumentó del 21% al 38%"),
        ("EXP-08", "Tooltips Contextuales Guiados para Descubrir Nuevos Módulos", "Adopción de Funcionalidades Secundarias", 5, 6, 8, "Product-Led Squad", "2026-03-18", "Test en curso en cohorte del 10%"),
        ("EXP-09", "Notificaciones Push en Navegador para Actualizaciones de Soporte", "Resolución de Tickets en Primer Contacto", 6, 5, 6, "Support Ops", "2026-03-25", "Baja tasa de opt-in (12%); impacto marginal"),
        ("EXP-10", "Chatbot de IA para Responder Dudas en la Página de Tarifas", "Leads Cualificados de Ventas (MQL)", 6, 5, 5, "Sales Ops Squad", "2026-04-02", "Generó ruido y quejas de spam; se desaconseja escalar"),
        ("EXP-11", "Insignias de Confianza SOC2 y Reseñas de Clientes en el Pago", "Reducción de Carritos Abandonados", 4, 6, 9, "Growth Squad", "2026-04-10", "Aumento estadísticamente no significativo (+1.2%)"),
        ("EXP-12", "Sistema de Puntos y Recompensas por Uso Diario Continuado", "Tiempo Medio de Sesión Diario", 3, 3, 4, "Product-Led Squad", "2026-04-20", "Sobrecarga de complejidad de producto con nulo retorno"),
    ]
    ice_experiments_en = [
        ("EXP-01", "One-Click Google OAuth Signup Flow on Homepage Hero", "Visitor-to-Signup Conversion Rate", 8, 9, 9, "Growth Squad", "2026-01-15", "+24% lift in new free account signups across all cohorts"),
        ("EXP-02", "20% Annual Subscription Discount Callout in Checkout Funnel", "Upfront Annual Contract Cashflow", 9, 8, 8, "Monetization Squad", "2026-01-22", "+31% shift from monthly to annual enterprise renewals"),
        ("EXP-03", "Gamified Interactive Onboarding Checklist with Progress Bar", "Day 1 Core Feature Activation Rate", 8, 8, 8, "Product-Led Squad", "2026-02-05", "Decreased median time to first valuable action from 4d to 1d"),
        ("EXP-04", "14-Day Frictionless Free Trial without Credit Card Requirement", "Total Weekly Active Workspaces", 8, 7, 9, "Growth Squad", "2026-02-12", "Doubled workspace creation; paid conversion remained at 4.2%"),
        ("EXP-05", "One-Click Instant Team Member Invitation via Magic Links", "Viral Expansion K-Factor", 7, 7, 7, "Core Team Squad", "2026-02-20", "In pre-launch staging environment"),
        ("EXP-06", "Cancellation Flow Micro-Survey Offering 30-Day Billing Pause", "Monthly Voluntary Churn Rate", 7, 6, 8, "Retention Squad", "2026-03-01", "Saved 18% of canceling users into paused retention state"),
        ("EXP-07", "Executive Summary Redesign for Weekly Activity Digest Email", "Weekly Active User Retention (WAU)", 6, 7, 7, "Marketing Ops", "2026-03-10", "Open rate jumped from 21% to 38% with higher re-engagement"),
        ("EXP-08", "Contextual In-App Guidance Tooltips for Secondary Modules", "Secondary Feature Adoption Breadth", 5, 6, 8, "Product-Led Squad", "2026-03-18", "Ongoing 10% canary cohort deployment"),
        ("EXP-09", "Browser Web Push Notifications for Support Ticket Updates", "First-Contact Support Resolution Time", 6, 5, 6, "Support Ops", "2026-03-25", "Low user opt-in rate (12%); marginal overall engagement impact"),
        ("EXP-10", "AI Chatbot Assistant Triggered on Pricing Page Hesitation", "Marketing Qualified Inbound Leads (MQL)", 6, 5, 5, "Sales Ops Squad", "2026-04-02", "Created user annoyance; failed to convert enterprise leads"),
        ("EXP-11", "SOC2 Type II Trust Badges & Verified Testimonials on Checkout", "Checkout Abandonment Drop-off", 4, 6, 9, "Growth Squad", "2026-04-10", "Statistically insignificant conversion uplift (+1.2%)"),
        ("EXP-12", "Usage Streaks and Daily Engagement Gamification Badges", "Average Daily Active Session Duration", 3, 3, 4, "Product-Led Squad", "2026-04-20", "High engineering complexity; near-zero ARR expansion impact"),
    ]
    ice_data = ice_experiments_es if lang == 'ES' else ice_experiments_en

    # Validación de datos: enteros 1-10 en columnas D, E, F
    dv_ice = DataValidation(type="whole", operator="between", formula1=1, formula2=10, allow_blank=True)
    dv_ice.errorTitle = "Calificación Inválida" if lang == 'ES' else "Invalid Rating"
    dv_ice.errorMessage = "Debes ingresar un número entero del 1 al 10." if lang == 'ES' else "Enter an integer between 1 and 10."
    ws.add_data_validation(dv_ice)
    dv_ice.add("D7:F26")

    # Filas 7 a 26 (20 filas: 12 precargadas + 8 vacías listas para el usuario)
    for row_idx in range(7, 27):
        is_prefilled = (row_idx - 7) < len(ice_data)
        if is_prefilled:
            exp_id, hyp, metric, imp, conf, ease, squad, ldate, result = ice_data[row_idx - 7]
        else:
            exp_id = f"EXP-{row_idx - 6:02d}"
            hyp, metric, imp, conf, ease, squad, ldate, result = "", "", "", "", "", "", "", ""

        ws[f"A{row_idx}"].value = exp_id
        ws[f"A{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"A{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"A{row_idx}"].border = borders['thin']

        ws[f"B{row_idx}"].value = hyp
        ws[f"B{row_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_DARK)
        ws[f"B{row_idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"B{row_idx}"].border = borders['thin']

        ws[f"C{row_idx}"].value = metric
        ws[f"C{row_idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_MED)
        ws[f"C{row_idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"C{row_idx}"].border = borders['thin']

        # Inputs numéricos D, E, F
        for c_let, val in [("D", imp), ("E", conf), ("F", ease)]:
            ws[f"{c_let}{row_idx}"].value = val
            ws[f"{c_let}{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
            ws[f"{c_let}{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
            ws[f"{c_let}{row_idx}"].border = borders['thin']
            ws[f"{c_let}{row_idx}"].number_format = "0"

        ws[f"G{row_idx}"].value = squad
        ws[f"G{row_idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"G{row_idx}"].alignment = Alignment(horizontal="left", vertical="center")
        ws[f"G{row_idx}"].border = borders['thin']

        ws[f"H{row_idx}"].value = ldate
        ws[f"H{row_idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"H{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"H{row_idx}"].border = borders['thin']

        ws[f"I{row_idx}"].value = result
        ws[f"I{row_idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"I{row_idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"I{row_idx}"].border = borders['thin']

        # FÓRMULAS CALCULADAS:
        # Col J: Score ICE Multiplicativo (I×C×E)
        ws[f"J{row_idx}"].value = f'=IF(OR(D{row_idx}="",E{row_idx}="",F{row_idx}=""),"",D{row_idx}*E{row_idx}*F{row_idx})'
        ws[f"J{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"J{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"J{row_idx}"].number_format = "#,##0"
        ws[f"J{row_idx}"].border = borders['thin']

        # Col K: Score ICE Promedio (I+C+E)/3
        ws[f"K{row_idx}"].value = f'=IF(OR(D{row_idx}="",E{row_idx}="",F{row_idx}=""),"",ROUND((D{row_idx}+E{row_idx}+F{row_idx})/3,1))'
        ws[f"K{row_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_MED)
        ws[f"K{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"K{row_idx}"].number_format = "0.0"
        ws[f"K{row_idx}"].border = borders['thin']

        # Col L: Columna auxiliar de desempate
        ws[f"L{row_idx}"].value = f'=IF(J{row_idx}="","",J{row_idx}+ROW()/1000000000)'
        ws[f"L{row_idx}"].font = Font(name=FONT_NAME, size=8, color=COLOR_BORDER_LIGHT)
        ws[f"L{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"L{row_idx}"].number_format = "0.000000000"
        ws[f"L{row_idx}"].border = borders['thin']

        # Col M: Ranking ICE
        ws[f"M{row_idx}"].value = f'=IF(L{row_idx}="","",RANK(L{row_idx},$L$7:$L$26))'
        ws[f"M{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"M{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"M{row_idx}"].border = borders['thin']
        ws[f"M{row_idx}"].number_format = "0"

        # Col N: Semáforo de Prioridad
        sem_f = (
            f'=IF(J{row_idx}="","",IF(J{row_idx}>=500,"🟢 Lanzar ya",IF(J{row_idx}>=200,"🟡 Backlog experimentos","🔴 Descartar")))'
            if lang == 'ES' else
            f'=IF(J{row_idx}="","",IF(J{row_idx}>=500,"🟢 Launch Now",IF(J{row_idx}>=200,"🟡 Growth Backlog","🔴 Deprioritize")))'
        )
        ws[f"N{row_idx}"].value = sem_f
        ws[f"N{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"N{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"N{row_idx}"].border = borders['thin']

        ws.row_dimensions[row_idx].height = 28

    # Fila de Resumen / Promedio ICE (Row 27)
    ws["B27"].value = "PROMEDIO / TOTAL EVALUADO" if lang == 'ES' else "EVALUATION SUMMARY / AVERAGE"
    ws["B27"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["B27"].alignment = Alignment(horizontal="left", vertical="center")
    ws["B27"].border = borders['total']

    for c_let in ["A", "C", "G", "H", "I", "L", "M", "N"]:
        ws[f"{c_let}27"].border = borders['total']

    ws["D27"].value = "=AVERAGE(D7:D26)"
    ws["D27"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["D27"].alignment = Alignment(horizontal="right", vertical="center")
    ws["D27"].number_format = "0.0"
    ws["D27"].border = borders['total']

    ws["E27"].value = "=AVERAGE(E7:E26)"
    ws["E27"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["E27"].alignment = Alignment(horizontal="right", vertical="center")
    ws["E27"].number_format = "0.0"
    ws["E27"].border = borders['total']

    ws["F27"].value = "=AVERAGE(F7:F26)"
    ws["F27"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["F27"].alignment = Alignment(horizontal="right", vertical="center")
    ws["F27"].number_format = "0.0"
    ws["F27"].border = borders['total']

    ws["J27"].value = "=AVERAGE(J7:J26)"
    ws["J27"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
    ws["J27"].alignment = Alignment(horizontal="right", vertical="center")
    ws["J27"].number_format = "#,##0"
    ws["J27"].border = borders['total']

    ws["K27"].value = "=AVERAGE(K7:K26)"
    ws["K27"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["K27"].alignment = Alignment(horizontal="right", vertical="center")
    ws["K27"].number_format = "0.0"
    ws["K27"].border = borders['total']

    ws.row_dimensions[27].height = 26

    # Anchos de columna
    col_widths = {
        "A": 12, "B": 56, "C": 36, "D": 15, "E": 16, "F": 15, "G": 22,
        "H": 14, "I": 56, "J": 18, "K": 18, "L": 14, "M": 14, "N": 24
    }
    for c_let, w in col_widths.items():
        ws.column_dimensions[c_let].width = w

    finalize_sheet(ws, decorative_cells=frozenset(decorative))
    print(f"  [OK] Pestaña '{sheet_title}' creada con éxito.")
    return sheet_title


def build_tab2_rice_backlog(wb, lang='ES'):
    """Construye la Pestaña 2: Backlog RICE / RICE Backlog (30 filas: 20 precargadas + 10 configuradas)."""
    sheet_title = "Backlog RICE" if lang == 'ES' else "RICE Backlog"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    # 1. Cabecera Principal
    ws.merge_cells("A2:T3")
    top_cell = ws["A2"]
    top_cell.value = (
        "BACKLOG CUANTITATIVO RICE: PRIORIZACIÓN, CUADRANTES & LÍNEA DE CORTE DE CAPACIDAD"
        if lang == 'ES' else
        "QUANTITATIVE RICE BACKLOG: VALUE SCORING, QUADRANTS & CAPACITY CUT-LINE"
    )
    top_cell.font = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
    top_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)
    top_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 20

    for r in range(2, 4):
        for c in range(1, 21):
            coord = f"{get_column_letter(c)}{r}"
            decorative.add(coord)
            ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)

    # 2. Subcabeceras de Columnas (Row 6)
    headers_es = [
        "ID", "Iniciativa / Funcionalidad", "Objetivo / OKR Vinculado", "Squad Responsable",
        "Reach (Q)", "Impacto (Etiqueta)", "Confianza (Etiqueta)", "Esfuerzo (PM)", "Evidencia & Justificación",
        "Impacto (Num)", "Confianza (%)", "Valor Esperado (R×I×C)", "Score RICE",
        "Desempate", "Score Norm. (0-100)", "Ranking RICE", "Cuadrante Estratégico",
        "Esfuerzo Acumulado (PM)", "Línea de Corte", "Trimestre Asignado"
    ]
    headers_en = [
        "ID", "Initiative / Feature", "Linked OKR / Goal", "Squad / Team",
        "Reach (Q)", "Impact (Label)", "Confidence (Label)", "Effort (PM)", "Evidence & Rationale",
        "Impact (Num)", "Confidence (%)", "Expected Value (R×I×C)", "RICE Score",
        "Tiebreaker", "Norm. Score (0-100)", "RICE Rank", "Strategic Quadrant",
        "Cumulative Effort (PM)", "Capacity Cut-Line", "Assigned Quarter"
    ]
    headers = headers_es if lang == 'ES' else headers_en

    for idx, h in enumerate(headers, start=1):
        col_let = get_column_letter(idx)
        coord = f"{col_let}6"
        ws[coord].value = h
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws[coord].border = borders['header']
        decorative.add(coord)
    ws.row_dimensions[6].height = 36

    # 3. Datos Precargados (20 iniciativas enterprise B2B SaaS de alto rigor)
    backlog_initiatives_es = [
        ("INIT-01", "Autenticación SSO SAML 2.0 / Okta Enterprise", "Crecimiento Enterprise & Seguridad", "Enterprise Core", 8500, "Alto (2.0)", "Alta (100%)", 2.0, "Validado con 12 clientes Tier-1 en RFP; requisito de cierre"),
        ("INIT-02", "Copilot de IA en Flujo de Trabajo para Generación de Informes", "Adopción de Producto & Retención NRR", "AI Innovation", 18000, "Masivo (3.0)", "Media (80%)", 6.0, "Beta interna con 85% de satisfacción y ahorro operativo"),
        ("INIT-03", "Exportador Rápido de Informes a Excel, CSV y PDF Vectorial", "Productividad del Usuario & NPS", "Core Experience", 22000, "Medio (1.0)", "Alta (100%)", 1.0, "Petición #1 en portal de feedback con 450 votos de clientes"),
        ("INIT-04", "Constructor Visual de Dashboards Drag & Drop Personalizados", "Diferenciación Competitiva & Upsell", "Analytics & BI", 12000, "Alto (2.0)", "Media (80%)", 5.5, "Análisis de churn revela pérdida de 8 cuentas por falta de BI ad-hoc"),
        ("INIT-05", "Flujo de Onboarding Autoservicio Guiado e Interactivo", "Activación de Cuentas (Time to Value)", "Growth Squad", 15000, "Alto (2.0)", "Alta (100%)", 1.5, "Pruebas de usabilidad muestran caída del 42% en primer setup"),
        ("INIT-06", "Catálogo de Webhooks de Eventos y API Pública REST v2", "Ecosistema & Integraciones ISV", "Platform Squad", 6000, "Alto (2.0)", "Alta (100%)", 3.5, "Requisito contractual en 5 acuerdos con partners tecnológicos"),
        ("INIT-07", "Notificaciones Push Móviles y Alertas Inteligentes", "Engagement Diario (DAU/MAU)", "Mobile Squad", 14000, "Medio (1.0)", "Media (80%)", 2.0, "Encuesta a 300 usuarios activos solicita aprobaciones en movilidad"),
        ("INIT-08", "Migración de Pasarela a Stripe Billing & Motor Multi-Divisa", "Expansión Internacional & Cobros", "Billing Squad", 9000, "Alto (2.0)", "Alta (100%)", 3.0, "Habilita pagos locales en USD, GBP y JPY; reduce fallos un 18%"),
        ("INIT-09", "Pistas de Auditoría Inmutables y Cumplimiento SOC2 Type II", "Seguridad & Compliance Bancario", "Enterprise Core", 4000, "Alto (2.0)", "Alta (100%)", 2.5, "Exigido por comités de seguridad de 7 clientes en renovación"),
        ("INIT-10", "Soporte Completo de Modo Oscuro (Native Dark Mode)", "Ergonomía de Interfaz & Accesibilidad", "Core Experience", 20000, "Bajo (0.5)", "Alta (100%)", 2.0, "Petición cosmética recurrente sin impacto cuantificable en retención"),
        ("INIT-11", "Espacios de Trabajo Multi-Equipo y Permisos RBAC Granulares", "Penetración en Grandes Cuentas", "Enterprise Core", 7500, "Alto (2.0)", "Alta (100%)", 4.0, "Imprescindible para cerrar 4 contratos >100k€ ARR"),
        ("INIT-12", "Marca Blanca Completa y Personalización de Dominio", "Canal de Agencias & Revendedores", "Growth Squad", 1500, "Alto (2.0)", "Media (80%)", 5.0, "Solicitado por 3 agencias; segmento de mercado total reducido"),
        ("INIT-13", "Edición Masiva y Etiquetado Múltiple de Registros", "Eficiencia Operativa del Usuario", "Core Experience", 16000, "Medio (1.0)", "Alta (100%)", 1.5, "Ahorra un promedio estimado de 45 minutos semanales por operador"),
        ("INIT-14", "Capa de Integración GraphQL para Consultas Complejas", "Arquitectura Técnica & Rendimiento", "Platform Squad", 3000, "Medio (1.0)", "Baja (50%)", 7.0, "Iniciativa interna de ingeniería; falta validación externa"),
        ("INIT-15", "Medición Automatizada de NPS In-App y Micro-Feedback", "Voz del Cliente & Detección de Fricción", "Growth Squad", 25000, "Medio (1.0)", "Alta (100%)", 1.0, "Captura sentimiento en tiempo real en momentos clave de valor"),
        ("INIT-16", "Integración Bidireccional con Slack y Microsoft Teams", "Colaboración en Equipo & Retención", "Platform Squad", 11000, "Alto (2.0)", "Media (80%)", 3.0, "Permite aprobaciones directas desde el chat corporativo"),
        ("INIT-17", "Programador de Envíos Automatizados de Reportes por Correo", "Hábito de Uso & Retención Ejecutiva", "Analytics & BI", 8000, "Medio (1.0)", "Alta (100%)", 1.5, "Informa periódicamente al C-Level sin obligar al login"),
        ("INIT-18", "Autenticación de Doble Factor Obligatoria vía SMS y TOTP", "Seguridad de Cuentas & Anti-Fraude", "Enterprise Core", 25000, "Alto (2.0)", "Alta (100%)", 1.5, "Reduce incidentes de compromiso de credenciales a casi cero"),
        ("INIT-19", "Refactorización Integral de Base de Datos y Reescribe a Rust", "Rendimiento Teórico de Infraestructura", "Core Platform", 5000, "Bajo (0.5)", "Baja (50%)", 14.0, "Iniciativa técnica sin cuellos de botella reales demostrados"),
        ("INIT-20", "Módulo de Facturación Electrónica B2B FacturaE y VeriFactu", "Cumplimiento Legal Regulatorio", "Billing Squad", 7000, "Alto (2.0)", "Alta (100%)", 2.5, "Mandato estatutario obligatorio para operar en el próximo ejercicio"),
    ]
    backlog_initiatives_en = [
        ("INIT-01", "Enterprise SAML 2.0 / Okta Single Sign-On (SSO)", "Enterprise Expansion & Security", "Enterprise Core", 8500, "High (2.0)", "High (100%)", 2.0, "Validated across 12 Tier-1 RFPs; essential closing gate"),
        ("INIT-02", "In-Workflow Generative AI Copilot for Report Summaries", "Product Adoption & NRR Expansion", "AI Innovation", 18000, "Massive (3.0)", "Medium (80%)", 6.0, "Internal beta achieved 85% CSAT and significant time saving"),
        ("INIT-03", "Instant Data Exporter to Excel, CSV, and Vector PDF", "User Daily Productivity & NPS", "Core Experience", 22000, "Medium (1.0)", "High (100%)", 1.0, "#1 upvoted customer feature request on feedback portal (450 votes)"),
        ("INIT-04", "Custom Drag-and-Drop Executive Dashboard Builder", "Competitive Moat & ARR Expansion", "Analytics & BI", 12000, "High (2.0)", "Medium (80%)", 5.5, "Churn analysis shows 8 lost enterprise renewals due to rigid BI"),
        ("INIT-05", "Interactive Self-Service Guided Product Onboarding Tour", "Account Activation & Time to Value", "Growth Squad", 15000, "High (2.0)", "High (100%)", 1.5, "Usability audits revealed a 42% setup abandonment rate on Day 1"),
        ("INIT-06", "Public REST API v2 & Real-Time Event Webhooks Catalog", "Developer Platform & ISV Ecosystem", "Platform Squad", 6000, "High (2.0)", "High (100%)", 3.5, "Contractual commitment across 5 technology partner integrations"),
        ("INIT-07", "Intelligent Mobile Push Alerts & Activity Digest", "Daily Engagement (DAU/MAU)", "Mobile Squad", 14000, "Medium (1.0)", "Medium (80%)", 2.0, "Survey of 300 active users requested mobile approval alerts"),
        ("INIT-08", "Stripe Billing Migration & Multi-Currency Engine", "International Expansion & Ops", "Billing Squad", 9000, "High (2.0)", "High (100%)", 3.0, "Enables domestic clearing in USD, GBP, JPY; slashes declines by 18%"),
        ("INIT-09", "Immutable Audit Logging & SOC2 Type II Certification", "Enterprise Trust & Governance", "Enterprise Core", 4000, "High (2.0)", "High (100%)", 2.5, "Required by InfoSec committees of 7 enterprise customers"),
        ("INIT-10", "System-Wide Native Dark Mode Interface Theme", "UI Ergonomics & Accessibility", "Core Experience", 20000, "Low (0.5)", "High (100%)", 2.0, "Popular cosmetic feedback with near-zero measurable ARR impact"),
        ("INIT-11", "Multi-Team Workspaces & Granular RBAC Permissions", "Large Account Corporate Rollout", "Enterprise Core", 7500, "High (2.0)", "High (100%)", 4.0, "Key requirement to unlock 4 major expansion deals >100k€ ARR"),
        ("INIT-12", "Full White-Labeling & Custom Domain Branding", "Reseller & Agency Partner Channel", "Growth Squad", 1500, "High (2.0)", "Medium (80%)", 5.0, "Expressed by 3 agency partners; small total addressable segment"),
        ("INIT-13", "Bulk Record Editing & Multi-Tagging Utilities", "Operational Back-Office Speed", "Core Experience", 16000, "Medium (1.0)", "High (100%)", 1.5, "Saves an estimated 45 mins/week per administrative user"),
        ("INIT-14", "GraphQL API Micro-Services Layer for Deep Queries", "Technical Architecture Modernization", "Platform Squad", 3000, "Medium (1.0)", "Low (50%)", 7.0, "Internal engineering proposal; weak external customer validation"),
        ("INIT-15", "Automated In-App Micro-Surveys & NPS Sentiment Pulse", "Voice of Customer & Retention Signals", "Growth Squad", 25000, "Medium (1.0)", "High (100%)", 1.0, "Triggers lightweight satisfaction checks at moments of value"),
        ("INIT-16", "Bi-Directional Slack & Microsoft Teams Bot Integration", "Team Collaboration & Sticky Loops", "Platform Squad", 11000, "High (2.0)", "Medium (80%)", 3.0, "Enables task approvals directly from corporate chat channels"),
        ("INIT-17", "Automated Scheduled PDF/Excel Report Email Dispatcher", "Executive Habit Loops & Usage", "Analytics & BI", 8000, "Medium (1.0)", "High (100%)", 1.5, "Keeps executive sponsors engaged without forcing direct web login"),
        ("INIT-18", "Mandatory Two-Factor Authentication via SMS & TOTP", "Account Security & Fraud Defense", "Enterprise Core", 25000, "High (2.0)", "High (100%)", 1.5, "Cuts credential-stuffing takeover incidents by >99%"),
        ("INIT-19", "Full Database Rewrite & Microservices Migration to Rust", "Theoretical Performance Latency", "Core Platform", 5000, "Low (0.5)", "Low (50%)", 14.0, "Executive pet project; zero measured production bottlenecks"),
        ("INIT-20", "Automated B2B E-Invoicing & Statutory Tax Connector", "Regulatory & Statutory Compliance", "Billing Squad", 7000, "High (2.0)", "High (100%)", 2.5, "Statutory requirement effective next fiscal cycle for EU operations"),
    ]
    backlog_data = backlog_initiatives_es if lang == 'ES' else backlog_initiatives_en

    # Validación de datos por listas desplegables referenciando la Pestaña 5
    scales_tab = "'Escalas & Calibración'" if lang == 'ES' else "'Scales & Calibration'"
    cap_tab = "'Capacidad & Roadmap'" if lang == 'ES' else "'Capacity & Roadmap'"

    dv_impact = DataValidation(type="list", formula1=f"{scales_tab}!$B$7:$B$11", allow_blank=True)
    dv_impact.errorTitle = "Impacto no válido" if lang == 'ES' else "Invalid Impact"
    dv_impact.errorMessage = "Selecciona una opción de la lista de impacto." if lang == 'ES' else "Select an option from the impact scale."
    ws.add_data_validation(dv_impact)
    dv_impact.add("F7:F36")

    dv_conf = DataValidation(type="list", formula1=f"{scales_tab}!$B$16:$B$18", allow_blank=True)
    dv_conf.errorTitle = "Confianza no válida" if lang == 'ES' else "Invalid Confidence"
    dv_conf.errorMessage = "Selecciona una opción de la lista de confianza." if lang == 'ES' else "Select an option from the confidence scale."
    ws.add_data_validation(dv_conf)
    dv_conf.add("G7:G36")

    # Filas 7 a 36 (30 filas: 20 precargadas + 10 vacías)
    for row_idx in range(7, 37):
        is_prefilled = (row_idx - 7) < len(backlog_data)
        if is_prefilled:
            i_id, i_name, i_okr, i_squad, r_val, imp_lbl, conf_lbl, eff_val, notes = backlog_data[row_idx - 7]
        else:
            i_id = f"INIT-{row_idx - 6:02d}"
            i_name, i_okr, i_squad, r_val, imp_lbl, conf_lbl, eff_val, notes = "", "", "", "", "", "", "", ""

        # Col A: ID
        ws[f"A{row_idx}"].value = i_id
        ws[f"A{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"A{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"A{row_idx}"].border = borders['thin']

        # Col B: Iniciativa
        ws[f"B{row_idx}"].value = i_name
        ws[f"B{row_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_DARK)
        ws[f"B{row_idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"B{row_idx}"].border = borders['thin']

        # Col C: OKR
        ws[f"C{row_idx}"].value = i_okr
        ws[f"C{row_idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"C{row_idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"C{row_idx}"].border = borders['thin']

        # Col D: Squad
        ws[f"D{row_idx}"].value = i_squad
        ws[f"D{row_idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"D{row_idx}"].alignment = Alignment(horizontal="left", vertical="center")
        ws[f"D{row_idx}"].border = borders['thin']

        # Col E: Reach
        ws[f"E{row_idx}"].value = r_val
        ws[f"E{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"E{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"E{row_idx}"].number_format = "#,##0"
        ws[f"E{row_idx}"].border = borders['thin']

        # Col F: Impacto (Etiqueta)
        ws[f"F{row_idx}"].value = imp_lbl
        ws[f"F{row_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_DARK)
        ws[f"F{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"F{row_idx}"].border = borders['thin']

        # Col G: Confianza (Etiqueta)
        ws[f"G{row_idx}"].value = conf_lbl
        ws[f"G{row_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_DARK)
        ws[f"G{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"G{row_idx}"].border = borders['thin']

        # Col H: Esfuerzo (PM)
        ws[f"H{row_idx}"].value = eff_val
        ws[f"H{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"H{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"H{row_idx}"].number_format = "0.0"
        ws[f"H{row_idx}"].border = borders['thin']

        # Col I: Evidencia
        ws[f"I{row_idx}"].value = notes
        ws[f"I{row_idx}"].font = Font(name=FONT_NAME, size=9, color=COLOR_NAVY_LIGHT)
        ws[f"I{row_idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"I{row_idx}"].border = borders['thin']

        # FÓRMULAS CALCULADAS:
        # Col J: Impacto Numérico vía INDEX/MATCH contra Escalas
        ws[f"J{row_idx}"].value = f'=IF(F{row_idx}="","",INDEX({scales_tab}!$C$7:$C$11,MATCH(F{row_idx},{scales_tab}!$B$7:$B$11,0)))'
        ws[f"J{row_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_MED)
        ws[f"J{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"J{row_idx}"].number_format = "0.00"
        ws[f"J{row_idx}"].border = borders['thin']

        # Col K: Confianza % vía INDEX/MATCH contra Escalas
        ws[f"K{row_idx}"].value = f'=IF(G{row_idx}="","",INDEX({scales_tab}!$C$16:$C$18,MATCH(G{row_idx},{scales_tab}!$B$16:$B$18,0)))'
        ws[f"K{row_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_MED)
        ws[f"K{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"K{row_idx}"].number_format = "0.0%"
        ws[f"K{row_idx}"].border = borders['thin']

        # Col L: Valor Esperado (R × I × C)
        ws[f"L{row_idx}"].value = f'=IF(OR(E{row_idx}="",J{row_idx}="",K{row_idx}=""),"",E{row_idx}*J{row_idx}*K{row_idx})'
        ws[f"L{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"L{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"L{row_idx}"].number_format = "#,##0"
        ws[f"L{row_idx}"].border = borders['thin']

        # Col M: Score RICE = (R × I × C) / Effort (protegido contra división por cero)
        ws[f"M{row_idx}"].value = f'=IF(OR(E{row_idx}="",H{row_idx}="",H{row_idx}<=0,J{row_idx}="",K{row_idx}=""),"",ROUND((E{row_idx}*J{row_idx}*K{row_idx})/H{row_idx},1))'
        ws[f"M{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"M{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"M{row_idx}"].number_format = "#,##0.0"
        ws[f"M{row_idx}"].border = borders['thin']

        # Col N: Columna auxiliar de desempate = Score + ROW()/10^9
        ws[f"N{row_idx}"].value = f'=IF(M{row_idx}="","",M{row_idx}+ROW()/1000000000)'
        ws[f"N{row_idx}"].font = Font(name=FONT_NAME, size=8, color=COLOR_BORDER_LIGHT)
        ws[f"N{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"N{row_idx}"].number_format = "0.000000000"
        ws[f"N{row_idx}"].border = borders['thin']

        # Col O: Score Normalizado 0-100 = 100 * Score / MAX(Scores)
        ws[f"O{row_idx}"].value = f'=IF(M{row_idx}="","",ROUND(100*M{row_idx}/MAX($M$7:$M$36),1))'
        ws[f"O{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"O{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"O{row_idx}"].number_format = "0.0"
        ws[f"O{row_idx}"].border = borders['thin']

        # Col P: Ranking RICE = RANK sobre columna de desempate
        ws[f"P{row_idx}"].value = f'=IF(N{row_idx}="","",RANK(N{row_idx},$N$7:$N$36))'
        ws[f"P{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"P{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"P{row_idx}"].border = borders['thin']
        ws[f"P{row_idx}"].number_format = "0"

        # Col Q: Cuadrante Estratégico (Quick Win, Gran Apuesta, Relleno, Pozo sin Fondo)
        quad_f = (
            f'=IF(M{row_idx}="","",IF(AND(L{row_idx}>=MEDIAN($L$7:$L$36),H{row_idx}<=MEDIAN($H$7:$H$36)),"Quick Win",IF(AND(L{row_idx}>=MEDIAN($L$7:$L$36),H{row_idx}>MEDIAN($H$7:$H$36)),"Gran Apuesta",IF(AND(L{row_idx}<MEDIAN($L$7:$L$36),H{row_idx}<=MEDIAN($H$7:$H$36)),"Relleno","Pozo sin Fondo"))))'
            if lang == 'ES' else
            f'=IF(M{row_idx}="","",IF(AND(L{row_idx}>=MEDIAN($L$7:$L$36),H{row_idx}<=MEDIAN($H$7:$H$36)),"Quick Win",IF(AND(L{row_idx}>=MEDIAN($L$7:$L$36),H{row_idx}>MEDIAN($H$7:$H$36)),"Big Bet",IF(AND(L{row_idx}<MEDIAN($L$7:$L$36),H{row_idx}<=MEDIAN($H$7:$H$36)),"Fill-in","Money Pit"))))'
        )
        ws[f"Q{row_idx}"].value = quad_f
        ws[f"Q{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"Q{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"Q{row_idx}"].border = borders['thin']

        # Col R: Esfuerzo Acumulado por Ranking = SUMIFS(Effort, Rank, "<="&Rank_i)
        ws[f"R{row_idx}"].value = f'=IF(P{row_idx}="","",SUMIFS($H$7:$H$36,$P$7:$P$36,"<="&P{row_idx}))'
        ws[f"R{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"R{row_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"R{row_idx}"].number_format = "0.0"
        ws[f"R{row_idx}"].border = borders['thin']

        # Col S: Estado de Línea de Corte
        cut_f = (
            f'=IF(R{row_idx}="","",IF(R{row_idx}<={cap_tab}!$D$19,"✅ Dentro de capacidad","⛔ Fuera de capacidad"))'
            if lang == 'ES' else
            f'=IF(R{row_idx}="","",IF(R{row_idx}<={cap_tab}!$D$19,"✅ Within Capacity","⛔ Exceeds Capacity"))'
        )
        ws[f"S{row_idx}"].value = cut_f
        ws[f"S{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"S{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"S{row_idx}"].border = borders['thin']

        # Col T: Trimestre Asignado (Q1, Q2, Q3, Q4, o Backlog Descartado)
        q_assign_f = (
            f'=IF(R{row_idx}="","",IF(R{row_idx}<={cap_tab}!$D$15,"Q1",IF(R{row_idx}<={cap_tab}!$D$16,"Q2",IF(R{row_idx}<={cap_tab}!$D$17,"Q3",IF(R{row_idx}<={cap_tab}!$D$18,"Q4","Backlog Descartado")))))'
            if lang == 'ES' else
            f'=IF(R{row_idx}="","",IF(R{row_idx}<={cap_tab}!$D$15,"Q1",IF(R{row_idx}<={cap_tab}!$D$16,"Q2",IF(R{row_idx}<={cap_tab}!$D$17,"Q3",IF(R{row_idx}<={cap_tab}!$D$18,"Q4","Deferred Backlog")))))'
        )
        ws[f"T{row_idx}"].value = q_assign_f
        ws[f"T{row_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"T{row_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"T{row_idx}"].border = borders['thin']

        ws.row_dimensions[row_idx].height = 28

    # Fila de Resumen / Totales (Row 37)
    ws["B37"].value = "TOTALES / PROMEDIOS DE CARTERA" if lang == 'ES' else "PORTFOLIO TOTALS & AVERAGES"
    ws["B37"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["B37"].alignment = Alignment(horizontal="left", vertical="center")
    ws["B37"].border = borders['total']

    for c_let in ["A", "C", "D", "F", "G", "I", "J", "K", "N", "O", "P", "Q", "R", "S", "T"]:
        ws[f"{c_let}37"].border = borders['total']

    ws["E37"].value = "=SUM(E7:E36)"
    ws["E37"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["E37"].alignment = Alignment(horizontal="right", vertical="center")
    ws["E37"].number_format = "#,##0"
    ws["E37"].border = borders['total']

    ws["H37"].value = "=SUM(H7:H36)"
    ws["H37"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["H37"].alignment = Alignment(horizontal="right", vertical="center")
    ws["H37"].number_format = "0.0"
    ws["H37"].border = borders['total']

    ws["L37"].value = "=SUM(L7:L36)"
    ws["L37"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["L37"].alignment = Alignment(horizontal="right", vertical="center")
    ws["L37"].number_format = "#,##0"
    ws["L37"].border = borders['total']

    ws["M37"].value = "=AVERAGE(M7:M36)"
    ws["M37"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
    ws["M37"].alignment = Alignment(horizontal="right", vertical="center")
    ws["M37"].number_format = "#,##0.0"
    ws["M37"].border = borders['total']

    ws.row_dimensions[37].height = 26

    # Anchos de columna
    col_widths = {
        "A": 12, "B": 52, "C": 36, "D": 22, "E": 14, "F": 18, "G": 18, "H": 14,
        "I": 65, "J": 14, "K": 14, "L": 22, "M": 16, "N": 14, "O": 16, "P": 14,
        "Q": 22, "R": 22, "S": 24, "T": 18
    }
    for c_let, w in col_widths.items():
        ws.column_dimensions[c_let].width = w

    finalize_sheet(ws, decorative_cells=frozenset(decorative))
    print(f"  [OK] Pestaña '{sheet_title}' creada con éxito.")
    return sheet_title


def build_tab1_dashboard(wb, lang='ES'):
    """Construye la Pestaña 1: Dashboard Ejecutivo / Executive Dashboard."""
    sheet_title = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    # 1. Título y Banner Directivo
    ws.merge_cells("B2:J3")
    top_cell = ws["B2"]
    top_cell.value = (
        "CUADRO DE MANDO EJECUTIVO: PRIORIZACIÓN ÁGIL RICE & ROADMAP C-LEVEL"
        if lang == 'ES' else
        "EXECUTIVE DASHBOARD: AGILE RICE PRIORITIZATION & C-SUITE ROADMAP"
    )
    top_cell.font = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
    top_cell.fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)
    top_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 20

    for r in range(2, 4):
        for c in range(2, 11):
            coord = f"{get_column_letter(c)}{r}"
            decorative.add(coord)
            ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)

    # Metadatos del Comité (Row 4)
    ws.merge_cells("B4:D4")
    ws["B4"].value = "Portfolio: Plataforma Cloud & SaaS Enterprise" if lang == 'ES' else "Portfolio: Enterprise Cloud & SaaS Platform"
    ws["B4"].font = Font(name=FONT_NAME, size=9, bold=True, color=COLOR_NAVY_LIGHT)
    ws["B4"].alignment = Alignment(horizontal="left", vertical="center")

    ws.merge_cells("E4:F4")
    ws["E4"].value = "Horizonte: Q1-Q4 Plan Estratégico" if lang == 'ES' else "Horizon: Q1-Q4 Strategic Roadmap"
    ws["E4"].font = Font(name=FONT_NAME, size=9, bold=True, color=COLOR_NAVY_LIGHT)
    ws["E4"].alignment = Alignment(horizontal="center", vertical="center")

    ws["G4"].value = "Actualizado:" if lang == 'ES' else "Updated:"
    ws["G4"].font = Font(name=FONT_NAME, size=9, bold=True, color=COLOR_NAVY_LIGHT)
    ws["G4"].alignment = Alignment(horizontal="right", vertical="center")

    ws["H4"].value = "=TODAY()"
    ws["H4"].font = Font(name=FONT_NAME, size=9, bold=True, color=COLOR_NAVY_LIGHT)
    ws["H4"].alignment = Alignment(horizontal="center", vertical="center")
    ws["H4"].number_format = "yyyy-mm-dd"

    ws.merge_cells("I4:J4")
    ws["I4"].value = "Sponsor / PMO: CPO & Board" if lang == 'ES' else "Executive Sponsor: CPO & Board"
    ws["I4"].font = Font(name=FONT_NAME, size=9, bold=True, color=COLOR_NAVY_LIGHT)
    ws["I4"].alignment = Alignment(horizontal="center", vertical="center")

    ws.row_dimensions[4].height = 24
    for c in range(2, 11):
        coord = f"{get_column_letter(c)}4"
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_BG_CARD)
        ws[coord].border = borders['thin']
        decorative.add(coord)

    # 2. TARJETAS DE MÉTRICAS KPI (Rows 6 a 8)
    backlog_tab = "'Backlog RICE'" if lang == 'ES' else "'RICE Backlog'"
    cap_tab = "'Capacidad & Roadmap'" if lang == 'ES' else "'Capacity & Roadmap'"

    cards_def_es = [
        ("B6:C6", "B7:C7", "B8:C8", "INICIATIVAS EVALUADAS", f"=COUNTIF({backlog_tab}!$B$7:$B$36,\"?*\")", "0", "Total en backlog estructurado"),
        ("D6", "D7", "D8", "% VALOR TOP 20%", f"=SUM(G14:G17)/{backlog_tab}!$L$37", "0.0%", "Concentración en Top 4"),
        ("E6:F6", "E7:F7", "E8:F8", "UTILIZACIÓN CAPACIDAD", f"=SUMIFS({backlog_tab}!$H$7:$H$36,{backlog_tab}!$S$7:$S$36,\"✅ Dentro de capacidad\")/{cap_tab}!$D$19", "0.0%", "Esfuerzo / Capacidad neta"),
        ("G6:H6", "G7:H7", "G8:H8", "FUERA DE CAPACIDAD", f"=COUNTIF({backlog_tab}!$S$7:$S$36,\"⛔ Fuera de capacidad\")", "0", "Iniciativas diferidas / congeladas"),
        ("I6:J6", "I7:J7", "I8:J8", "QUICK WINS IDENTIFICADOS", f"=COUNTIF({backlog_tab}!$Q$7:$Q$36,\"Quick Win\")", "0", "Alto impacto con bajo esfuerzo"),
    ]
    cards_def_en = [
        ("B6:C6", "B7:C7", "B8:C8", "EVALUATED INITIATIVES", f"=COUNTIF({backlog_tab}!$B$7:$B$36,\"?*\")", "0", "Structured backlog inventory"),
        ("D6", "D7", "D8", "TOP 20% VALUE SHARE", f"=SUM(G14:G17)/{backlog_tab}!$L$37", "0.0%", "Value captured in top 4 items"),
        ("E6:F6", "E7:F7", "E8:F8", "CAPACITY UTILIZATION", f"=SUMIFS({backlog_tab}!$H$7:$H$36,{backlog_tab}!$S$7:$S$36,\"✅ Within Capacity\")/{cap_tab}!$D$19", "0.0%", "Committed effort vs capacity"),
        ("G6:H6", "G7:H7", "G8:H8", "CUT-LINE EXCLUSIONS", f"=COUNTIF({backlog_tab}!$S$7:$S$36,\"⛔ Exceeds Capacity\")", "0", "Deferred / Frozen backlog items"),
        ("I6:J6", "I7:J7", "I8:J8", "QUICK WINS IDENTIFIED", f"=COUNTIF({backlog_tab}!$Q$7:$Q$36,\"Quick Win\")", "0", "High impact & low effort"),
    ]
    cards_def = cards_def_es if lang == 'ES' else cards_def_en

    ws.row_dimensions[6].height = 22
    ws.row_dimensions[7].height = 26
    ws.row_dimensions[8].height = 18

    for h_rng, v_rng, s_rng, h_text, val_form, num_fmt, sub_text in cards_def:
        # Cabecera de tarjeta
        if ":" in h_rng:
            ws.merge_cells(h_rng)
            h_c = h_rng.split(":")[0]
            h_cols = [h_rng.split(":")[0][0], h_rng.split(":")[1][0]]
        else:
            h_c = h_rng
            h_cols = [h_rng[0]]

        ws[h_c].value = h_text
        ws[h_c].font = Font(name=FONT_NAME, size=9, bold=True, color="FFFFFF")
        ws[h_c].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[h_c].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Valor de tarjeta
        if ":" in v_rng:
            ws.merge_cells(v_rng)
            v_c = v_rng.split(":")[0]
        else:
            v_c = v_rng

        ws[v_c].value = val_form
        ws[v_c].font = Font(name=FONT_NAME, size=16, bold=True, color=COLOR_BLUE_ACCENT)
        ws[v_c].alignment = Alignment(horizontal="center", vertical="center")
        ws[v_c].number_format = num_fmt

        # Subtítulo de tarjeta
        if ":" in s_rng:
            ws.merge_cells(s_rng)
            s_c = s_rng.split(":")[0]
        else:
            s_c = s_rng

        ws[s_c].value = sub_text
        ws[s_c].font = Font(name=FONT_NAME, size=8, color=COLOR_NAVY_LIGHT)
        ws[s_c].fill = PatternFill(fill_type="solid", fgColor=COLOR_BG_CARD)
        ws[s_c].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Borde y decorative para toda la tarjeta (filas 6, 7, 8)
        start_c = ord(h_cols[0]) - ord('A') + 1
        end_c = ord(h_cols[-1]) - ord('A') + 1
        for col_i in range(start_c, end_c + 1):
            col_l = get_column_letter(col_i)
            for r_n in range(6, 9):
                cell_id = f"{col_l}{r_n}"
                ws[cell_id].border = borders['thin']
                decorative.add(cell_id)

    # 3. SECCIÓN B: Ranking Dinámico Top 10 RICE (Rows 12 a 23)
    ws.merge_cells("B11:J11")
    ws["B11"].value = "RANKING TOP 10 RICE (MOTOR DINÁMICO LARGE + INDEX/MATCH)" if lang == 'ES' else "TOP 10 DYNAMIC RICE RANKING (LARGE + INDEX/MATCH RESOLUTION)"
    ws["B11"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["B11"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[11].height = 24
    for c in range(2, 11):
        decorative.add(f"{get_column_letter(c)}11")

    ws.row_dimensions[12].height = 10

    h_rank_es = ["Pos", "ID", "Iniciativa / Funcionalidad Priorizada", "Score RICE", "Score Norm.", "Valor (R×I×C)", "Cuadrante", "Trimestre", "Línea de Corte"]
    h_rank_en = ["Pos", "ID", "Prioritized Initiative / Feature", "RICE Score", "Norm. Score", "Value (R×I×C)", "Quadrant", "Quarter", "Capacity Status"]
    h_rank = h_rank_es if lang == 'ES' else h_rank_en

    for idx, h in enumerate(h_rank, start=2):
        col_let = get_column_letter(idx)
        coord = f"{col_let}13"
        ws[coord].value = h
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws[coord].border = borders['header']
        decorative.add(coord)
    ws.row_dimensions[13].height = 26

    for pos in range(1, 11):
        r_idx = 13 + pos
        # Col B: Posición
        ws[f"B{r_idx}"].value = pos
        ws[f"B{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"B{r_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"B{r_idx}"].border = borders['thin']

        # Col C: ID
        ws[f"C{r_idx}"].value = f'=INDEX({backlog_tab}!$A$7:$A$36,MATCH(LARGE({backlog_tab}!$N$7:$N$36,B{r_idx}),{backlog_tab}!$N$7:$N$36,0))'
        ws[f"C{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"C{r_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"C{r_idx}"].border = borders['thin']

        # Col D: Iniciativa
        ws[f"D{r_idx}"].value = f'=INDEX({backlog_tab}!$B$7:$B$36,MATCH(LARGE({backlog_tab}!$N$7:$N$36,B{r_idx}),{backlog_tab}!$N$7:$N$36,0))'
        ws[f"D{r_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_DARK)
        ws[f"D{r_idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"D{r_idx}"].border = borders['thin']

        # Col E: Score RICE
        ws[f"E{r_idx}"].value = f'=INDEX({backlog_tab}!$M$7:$M$36,MATCH(LARGE({backlog_tab}!$N$7:$N$36,B{r_idx}),{backlog_tab}!$N$7:$N$36,0))'
        ws[f"E{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"E{r_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"E{r_idx}"].number_format = "#,##0.0"
        ws[f"E{r_idx}"].border = borders['thin']

        # Col F: Score Normalizado
        ws[f"F{r_idx}"].value = f'=INDEX({backlog_tab}!$O$7:$O$36,MATCH(LARGE({backlog_tab}!$N$7:$N$36,B{r_idx}),{backlog_tab}!$N$7:$N$36,0))'
        ws[f"F{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"F{r_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"F{r_idx}"].number_format = "0.0"
        ws[f"F{r_idx}"].border = borders['thin']

        # Col G: Valor (R×I×C)
        ws[f"G{r_idx}"].value = f'=INDEX({backlog_tab}!$L$7:$L$36,MATCH(LARGE({backlog_tab}!$N$7:$N$36,B{r_idx}),{backlog_tab}!$N$7:$N$36,0))'
        ws[f"G{r_idx}"].font = Font(name=FONT_NAME, size=10, color=COLOR_NAVY_DARK)
        ws[f"G{r_idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"G{r_idx}"].number_format = "#,##0"
        ws[f"G{r_idx}"].border = borders['thin']

        # Col H: Cuadrante
        ws[f"H{r_idx}"].value = f'=INDEX({backlog_tab}!$Q$7:$Q$36,MATCH(LARGE({backlog_tab}!$N$7:$N$36,B{r_idx}),{backlog_tab}!$N$7:$N$36,0))'
        ws[f"H{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"H{r_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"H{r_idx}"].border = borders['thin']

        # Col I: Trimestre
        ws[f"I{r_idx}"].value = f'=INDEX({backlog_tab}!$T$7:$T$36,MATCH(LARGE({backlog_tab}!$N$7:$N$36,B{r_idx}),{backlog_tab}!$N$7:$N$36,0))'
        ws[f"I{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"I{r_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"I{r_idx}"].border = borders['thin']

        # Col J: Línea de Corte
        ws[f"J{r_idx}"].value = f'=INDEX({backlog_tab}!$S$7:$S$36,MATCH(LARGE({backlog_tab}!$N$7:$N$36,B{r_idx}),{backlog_tab}!$N$7:$N$36,0))'
        ws[f"J{r_idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"J{r_idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"J{r_idx}"].border = borders['thin']

        ws.row_dimensions[r_idx].height = 28

    ws.row_dimensions[24].height = 10

    # 4. TARJETA DE RECOMENDACIÓN EJECUTIVA C-LEVEL (Rows 26 a 29)
    rec_title = "DICTAMEN ESTRATÉGICO & RECOMENDACIONES VINCULANTES DEL COMITÉ (C-LEVEL)" if lang == 'ES' else "C-SUITE STRATEGIC VERDICT & EXECUTIVE RECOMMENDATIONS"
    ws.merge_cells("B25:J25")
    ws["B25"].value = rec_title
    ws["B25"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["B25"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[25].height = 24
    for c in range(2, 11):
        decorative.add(f"{get_column_letter(c)}25")

    rec_cards_es = [
        ("B26:E27", "🏆 INICIATIVA #1 (MÁXIMA DENSIDAD)", "INIT-18: 2FA Obligatorio SMS/TOTP (Score 33.333,3) concentra la mayor densidad de valor por persona-mes invertido."),
        ("F26:J27", "⚡ QUICK WINS A EJECUTAR DE INMEDIATO (Q1)", "5 Quick Wins identificados (INIT-18, INIT-15, INIT-03, INIT-05, INIT-01) capturan el 54% del valor con solo 7.5 PM de esfuerzo."),
        ("B28:E29", "🛑 PROYECTOS A CONGELAR / DESCARTAR", "INIT-19 (Reescribe a Rust) e INIT-14 (GraphQL) consumen 21 PM de ingeniería con bajísima certeza: congelar de inmediato."),
        ("F28:J29", "💡 CAPACIDAD LIBERADA & GOBERNANZA", "La aplicación estricta de la línea de corte libera 28 PM de ingeniería, evitando el síndrome HiPPO y garantizando el foco en OKRs."),
    ]
    rec_cards_en = [
        ("B26:E27", "🏆 #1 PRIORITY INITIATIVE (VALUE DENSITY)", "INIT-18: Mandatory 2FA (RICE Score 33,333.3) delivers the highest verified value density per engineering person-month."),
        ("F26:J27", "⚡ IMMEDIATE Q1 QUICK WINS EXECUTION", "5 identified Quick Wins (INIT-18, INIT-15, INIT-03, INIT-05, INIT-01) capture 54% of total value using only 7.5 PM of capacity."),
        ("B28:E29", "🛑 INITIATIVES TO FORMALLY FREEZE", "INIT-19 (Rust rewrite) & INIT-14 (GraphQL) consume 21 PM with low confidence: freeze immediately to protect roadmap focus."),
        ("F28:J29", "💡 FREED CAPACITY & GOVERNANCE GAIN", "Strict capacity cut-line enforcement reclaims 28 person-months, eliminating HiPPO syndrome and securing quarterly OKRs."),
    ]
    rec_cards = rec_cards_es if lang == 'ES' else rec_cards_en

    for rng, h_txt, body_txt in rec_cards:
        ws.merge_cells(rng)
        r_start = rng.split(":")[0]
        ws[r_start].value = f"{h_txt}\n{body_txt}"
        ws[r_start].font = Font(name=FONT_NAME, size=9.5, color=COLOR_NAVY_DARK)
        ws[r_start].fill = PatternFill(fill_type="solid", fgColor=COLOR_BG_CARD)
        ws[r_start].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

        c_start_let = rng.split(":")[0][0]
        c_end_let = rng.split(":")[1][0]
        r1_n = int(rng.split(":")[0][1:])
        r2_n = int(rng.split(":")[1][1:])
        for col_idx in range(ord(c_start_let) - ord('A') + 1, ord(c_end_let) - ord('A') + 2):
            for row_n in range(r1_n, r2_n + 1):
                cell_c = f"{get_column_letter(col_idx)}{row_n}"
                ws[cell_c].border = borders['thin']
                decorative.add(cell_c)

    ws.row_dimensions[26].height = 32
    ws.row_dimensions[27].height = 32
    ws.row_dimensions[28].height = 32
    ws.row_dimensions[29].height = 32

    # 5. GRÁFICOS ANALÍTICOS (Dispersión y Barras Horizontales)
    # Gráfico 1: Dispersión Impacto vs Esfuerzo (colocado en L6)
    ws_backlog = wb["Backlog RICE" if lang == 'ES' else "RICE Backlog"]
    chart_scatter = ScatterChart()
    chart_scatter.title = "Matriz Valor Esperado vs. Esfuerzo (R×I×C vs. PM)" if lang == 'ES' else "Expected Value vs. Effort Matrix (R×I×C vs. PM)"
    chart_scatter.style = 13
    chart_scatter.x_axis.title = "Esfuerzo / Effort (Persona-Mes)" if lang == 'ES' else "Effort (Person-Months)"
    chart_scatter.y_axis.title = "Valor Esperado / Expected Value" if lang == 'ES' else "Expected Value (R×I×C)"
    chart_scatter.width = 17
    chart_scatter.height = 10

    xvalues = Reference(ws_backlog, min_col=8, min_row=7, max_row=26)   # Esfuerzo (Col H)
    yvalues = Reference(ws_backlog, min_col=12, min_row=7, max_row=26)  # Valor Esperado (Col L)
    series_sc = Series(yvalues, xvalues, title_from_data=False)
    series_sc.marker.symbol = "circle"
    series_sc.marker.size = 7
    series_sc.graphicalProperties.line.noFill = True
    chart_scatter.series.append(series_sc)
    ws.add_chart(chart_scatter, "L6")

    # Gráfico 2: Barras Horizontales Top 10 por Score RICE (colocado en L21)
    chart_bar = BarChart()
    chart_bar.type = "bar"  # horizontal
    chart_bar.style = 10
    chart_bar.title = "Top 10 Iniciativas por Score RICE" if lang == 'ES' else "Top 10 Initiatives by RICE Score"
    chart_bar.y_axis.title = "Iniciativa" if lang == 'ES' else "Initiative"
    chart_bar.x_axis.title = "Score RICE"
    chart_bar.width = 17
    chart_bar.height = 10

    data_bar = Reference(ws, min_col=5, min_row=13, max_row=23)  # Col E: Score RICE
    cats_bar = Reference(ws, min_col=4, min_row=14, max_row=23)  # Col D: Iniciativa
    chart_bar.add_data(data_bar, titles_from_data=True)
    chart_bar.set_categories(cats_bar)
    chart_bar.legend = None
    ws.add_chart(chart_bar, "L21")

    # Anchos de columna
    col_widths = {
        "A": 4, "B": 8, "C": 16, "D": 50, "E": 15, "F": 15,
        "G": 18, "H": 20, "I": 15, "J": 24, "K": 4, "L": 18
    }
    for c_let, w in col_widths.items():
        ws.column_dimensions[c_let].width = w

    finalize_sheet(ws, decorative_cells=frozenset(decorative))
    print(f"  [OK] Pestaña '{sheet_title}' creada con éxito.")
    return sheet_title


def generate_rice_ice_workbook(lang='ES', out_path=None):
    if out_path is None:
        if lang == 'ES':
            out_path = "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[ES]_Matriz_RICE_ICE/Matriz_RICE_ICE_Datalaria_ES.xlsx"
        else:
            out_path = "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[EN]_RICE_ICE_Matrix/RICE_ICE_Matrix_Datalaria_EN.xlsx"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print(f"\nIniciando construcción del libro Excel ({lang}): {out_path}...")

    wb = openpyxl.Workbook()
    # Eliminar hoja por defecto al inicio
    default_sheet = wb.active

    # Construir pestañas en orden de dependencia metodológica
    # 1. Pestaña 5: Escalas & Calibración (la Pestaña 2 la referencia)
    build_tab5_scales(wb, lang=lang)
    # 2. Pestaña 4: Capacidad & Roadmap (la Pestaña 2 la referencia para la línea de corte)
    build_tab4_capacity(wb, lang=lang)
    # 3. Pestaña 3: Experimentos ICE
    build_tab3_ice(wb, lang=lang)
    # 4. Pestaña 2: Backlog RICE
    build_tab2_rice_backlog(wb, lang=lang)
    # 5. Pestaña 1: Dashboard Ejecutivo (referencia Backlog RICE y Capacidad)
    build_tab1_dashboard(wb, lang=lang)

    # Eliminar hoja por defecto
    wb.remove(default_sheet)

    # Reordenar las hojas para que aparezcan en el orden ejecutivo:
    # 1. Dashboard, 2. Backlog RICE, 3. Experimentos ICE, 4. Capacidad & Roadmap, 5. Escalas
    sheet_order_es = [
        "Dashboard Ejecutivo", "Backlog RICE", "Experimentos ICE",
        "Capacidad & Roadmap", "Escalas & Calibración"
    ]
    sheet_order_en = [
        "Executive Dashboard", "RICE Backlog", "ICE Experiments",
        "Capacity & Roadmap", "Scales & Calibration"
    ]
    target_order = sheet_order_es if lang == 'ES' else sheet_order_en
    wb._sheets = [wb[sname] for sname in target_order]
    wb.active = wb[target_order[0]]

    wb.save(out_path)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"[OK] Libro Excel guardado con éxito: {out_path} ({size_kb:.1f} KB)")
    return out_path


def main():
    print("================================================================================")
    print("DATALARIA | GENERADOR EXCEL RICE & ICE PRIORITIZATION ENGINE")
    print("================================================================================")
    es_path = generate_rice_ice_workbook(lang='ES')
    en_path = generate_rice_ice_workbook(lang='EN')
    print("\nGeneración completada para ambas ediciones (ES y EN).")


if __name__ == "__main__":
    main()
