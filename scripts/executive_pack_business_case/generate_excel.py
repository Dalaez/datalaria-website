#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Generador maestro de los libros de cálculo en Excel para el Executive Decision Pack:
1. packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[ES]_Business_Case_VAN_TIR/Business_Case_VAN_TIR_Datalaria_ES.xlsx
2. packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[EN]_Financial_Business_Case/Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx

Arquitectura de 6 pestañas interconectadas:
- Pestaña 1: "Dashboard Ejecutivo" / "Executive Dashboard"
- Pestaña 2: "Supuestos & Drivers" / "Assumptions & Drivers"
- Pestaña 3: "Proyección DCF" / "DCF Projection"
- Pestaña 4: "Sensibilidad & Tornado" / "Sensitivity & Tornado"
- Pestaña 5: "Plan de Inversión & Gobernanza" / "Investment Plan & Governance"
- Pestaña 6: "Guía de Uso" / "User Guide"

Estándar de Seguridad y Compatibilidad:
- ECMA-376 / OpenXML compliant.
- Celdas sin fórmula = editables (#FFFFFF, locked=False).
- Celdas con fórmula = protegidas (#F1F5F9, locked=True).
- Contraseña oficial: "Datalaria2026".
- Fórmulas en inglés sin prefijos dinámicos _xlfn.
- Formatos numéricos en sintaxis invariante (localizados por Excel).
- Gráficos nativos: Curva J acumulada, Gráfico Tornado y Escenarios.
- Nombres de rango canónicos: VAN_Base, TIR_Base, WACC, Payback_Desc, VAN_Esperado.
"""

import os
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, LineChart, Reference, Series
from openpyxl.chart.data_source import AxDataSource, StrRef, StrData, StrVal
from openpyxl.workbook.defined_name import DefinedName

from protection_policy import finalize_sheet
import model_core

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Paleta Corporativa Datalaria
COLOR_NAVY_DARK = "0F172A"       # Slate 900
COLOR_NAVY_MED = "1E293B"        # Slate 800
COLOR_NAVY_LIGHT = "334155"      # Slate 700
COLOR_BLUE_ACCENT = "2563EB"     # Blue 600
COLOR_BLUE_LIGHT = "EFF6FF"      # Blue 50

COLOR_GREEN_BG = "D1FAE5"        # Green 100
COLOR_GREEN_TEXT = "065F46"      # Green 800
COLOR_GREEN_BORDER = "10B981"    # Green 500

COLOR_AMBER_BG = "FEF3C7"        # Amber 100
COLOR_AMBER_TEXT = "92400E"      # Amber 800
COLOR_AMBER_BORDER = "F59E0B"    # Amber 500

COLOR_RED_BG = "FEE2E2"          # Red 100
COLOR_RED_TEXT = "991B1B"        # Red 800
COLOR_RED_BORDER = "EF4444"      # Red 500

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
        'highlight': Border(left=med, right=med, top=med, bottom=med),
    }


def style_merged_header(ws, range_str, title_text, decorative_set, bg_color=COLOR_NAVY_DARK, fg_color="FFFFFF", font_size=13):
    ws.merge_cells(range_str)
    first_coord = range_str.split(":")[0]
    cell = ws[first_coord]
    cell.value = title_text
    cell.font = Font(name=FONT_NAME, size=font_size, bold=True, color=fg_color)
    cell.fill = PatternFill(fill_type="solid", fgColor=bg_color)
    cell.alignment = Alignment(horizontal="center", vertical="center")

    start_col, start_row, end_col, end_row = openpyxl.utils.range_boundaries(range_str)
    for r in range(start_row, end_row + 1):
        for c in range(start_col, end_col + 1):
            coord = f"{get_column_letter(c)}{r}"
            decorative_set.add(coord)
            ws[coord].fill = PatternFill(fill_type="solid", fgColor=bg_color)


def build_tab2_assumptions(wb, lang='ES'):
    """Construye la Pestaña 2: Supuestos & Drivers / Assumptions & Drivers."""
    sheet_title = "Supuestos & Drivers" if lang == 'ES' else "Assumptions & Drivers"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    # Formatos de número invariantes OpenXML
    fmt_curr = '#,##0 "€";[Red]-#,##0 "€"' if lang == 'ES' else '"$"#,##0;[Red]("$"#,##0)'
    fmt_pct = '0.0%'
    fmt_yrs = '0.0 "años"' if lang == 'ES' else '0.0 "yrs"'

    # 1. Cabecera Principal
    h_title = (
        "SUPUESTOS MACROECONÓMICOS, POLÍTICA DE INVERSIÓN Y DRIVERS OPERATIVOS"
        if lang == 'ES' else
        "MACROECONOMIC ASSUMPTIONS, HURDLE POLICY & OPERATING DRIVERS"
    )
    style_merged_header(ws, "B2:G3", h_title, decorative, COLOR_NAVY_DARK, "FFFFFF", 12)
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 20

    # 2. SECCIÓN 1: Política de Inversión (Hurdle Policy)
    s1_title = "1. POLÍTICA DE INVERSIÓN & UMBRALES DE APROBACIÓN (HURDLE POLICY)" if lang == 'ES' else "1. INVESTMENT POLICY & APPROVAL THRESHOLDS (HURDLE POLICY)"
    ws["B5"].value = s1_title
    ws["B5"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B5")

    h_cols = ["Concepto / Parámetro", "Valor", "Unidad", "Definición / Criterio del Comité de Inversiones"] if lang == 'ES' else [
        "Concept / Parameter", "Value", "Unit", "Definition / Investment Committee Benchmark"
    ]
    for c_idx, h_text in enumerate(h_cols, start=2):
        coord = f"{get_column_letter(c_idx)}6"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx in [3, 4] else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    ws.merge_cells("E6:G6")
    ws["F6"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["G6"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["F6"].border = borders['header']
    ws["G6"].border = borders['header']
    decorative.add("F6")
    decorative.add("G6")

    hurdle_rows = [
        ("Prima de riesgo exigida sobre WACC (Hurdle Margin)" if lang == 'ES' else "Required Risk Spread over WACC (Hurdle Margin)", 0.030, fmt_pct, "pp", "Margen mínimo exigido a la TIR sobre el WACC (+3,0 pp)" if lang == 'ES' else "Minimum required spread for IRR above WACC (+3.0 pp)"),
        ("Payback descontado máximo admisible" if lang == 'ES' else "Maximum Allowable Discounted Payback", 4.0, '0.0', "años" if lang == 'ES' else "yrs", "Límite superior de recuperación de capital según política interna" if lang == 'ES' else "Internal corporate threshold for capital recovery"),
        ("Tasa de reinversión para MIRR" if lang == 'ES' else "Reinvestment Rate for MIRR", 0.095, fmt_pct, "%", "Tasa para reinversión de flujos positivos (coste de oportunidad)" if lang == 'ES' else "Reinvestment rate for positive cash inflows (opportunity cost)"),
        ("Vida útil para amortización lineal" if lang == 'ES' else "Useful Life for Straight-Line Depreciation", 5, '0', "años" if lang == 'ES' else "yrs", "Horizonte fiscal y técnico para amortización del activo industrial" if lang == 'ES' else "Fiscal and technical depreciation horizon for industrial asset"),
        ("Tipo impositivo efectivo sobre sociedades (t)" if lang == 'ES' else "Corporate Income Tax Rate (t)", 0.250, fmt_pct, "%", "Tipo impositivo nominal para cálculo de NOPAT y escudo fiscal" if lang == 'ES' else "Nominal tax rate for NOPAT and interest tax shield calculation"),
        ("Crecimiento nominal a perpetuidad (g - Gordon)" if lang == 'ES' else "Perpetual Growth Rate (g - Gordon Terminal)", 0.015, fmt_pct, "%", "Tasa de crecimiento a largo plazo para valor terminal residual" if lang == 'ES' else "Long-term perpetual growth rate for terminal residual value"),
    ]

    for idx, (label, val, fmt, unit, desc) in enumerate(hurdle_rows, start=7):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10)
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = val
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"C{idx}"].number_format = fmt
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"C{idx}"].border = borders['thin']

        ws[f"D{idx}"].value = unit
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9, color="64748B")
        ws[f"D{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"D{idx}"].border = borders['thin']

        ws.merge_cells(f"E{idx}:G{idx}")
        ws[f"E{idx}"].value = desc
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=9, color="334155")
        ws[f"E{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        for c in range(5, 8):
            coord = f"{get_column_letter(c)}{idx}"
            ws[coord].border = borders['thin']
            decorative.add(coord)
        ws.row_dimensions[idx].height = 24

    # 3. SECCIÓN 2: Calculadora de WACC (CAPM)
    s2_title = "2. CALCULADORA DE COSTE DE CAPITAL PROMEDIO PONDERADO (WACC - CAPM)" if lang == 'ES' else "2. WEIGHTED AVERAGE COST OF CAPITAL CALCULATOR (WACC - CAPM)"
    ws["B14"].value = s2_title
    ws["B14"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B14")

    h_cols_wacc = ["Variable Financiera (CAPM)", "Valor", "Unidad", "Fundamento Metodológico / Fuente de Mercado"] if lang == 'ES' else [
        "Financial Variable (CAPM)", "Value", "Unit", "Methodological Basis / Market Benchmark"
    ]
    for c_idx, h_text in enumerate(h_cols_wacc, start=2):
        coord = f"{get_column_letter(c_idx)}15"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx in [3, 4] else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    ws.merge_cells("E15:G15")
    ws["F15"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["G15"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["F15"].border = borders['header']
    ws["G15"].border = borders['header']
    decorative.add("F15")
    decorative.add("G15")

    wacc_params = [
        ("Tasa libre de riesgo (Rf)" if lang == 'ES' else "Risk-Free Rate (Rf)", 0.035, fmt_pct, "%", "Bono soberano a 10 años (referencia libre de riesgo)" if lang == 'ES' else "10-year sovereign government bond benchmark", False),
        ("Beta apalancada de la industria (β)" if lang == 'ES' else "Levered Industry Beta (β)", 1.200, '0.00"x"', "x", "Riesgo sistemático de la industria manufacturera (Damodaran)" if lang == 'ES' else "Systematic risk for industrial machinery sector (Damodaran)", False),
        ("Prima de riesgo de mercado (ERP)" if lang == 'ES' else "Equity Risk Premium (ERP)", 0.055, fmt_pct, "%", "Rentabilidad adicional exigida a la renta variable sobre deuda soberana" if lang == 'ES' else "Historical equity market risk premium over sovereign debt", False),
        ("Prima de riesgo específica / tamaño" if lang == 'ES' else "Size / Project Specific Risk Premium", 0.014, fmt_pct, "%", "Ajuste por iliquidez, tamaño pyme y ejecución de ingeniería" if lang == 'ES' else "Spread for illiquidity, mid-cap size and execution risk", False),
        ("Coste del capital propio (Ke = Rf + β·ERP + Primas)" if lang == 'ES' else "Cost of Equity (Ke = Rf + β·ERP + Premiums)", "=$C$16 + $C$17*$C$18 + $C$19", fmt_pct, "%", "Rentabilidad mínima exigida por los accionistas (CAPM institucional)" if lang == 'ES' else "Expected return required by equity holders (institutional CAPM)", True),
        ("Coste de la deuda antes de impuestos (Kd)" if lang == 'ES' else "Pre-Tax Cost of Debt (Kd)", 0.0466666667, fmt_pct, "%", "Tipo de interés medio ponderado de la financiación bancaria" if lang == 'ES' else "Weighted average borrowing rate for senior corporate debt", False),
        ("Coste de la deuda neto de escudo fiscal (Kd·(1-t))" if lang == 'ES' else "After-Tax Cost of Debt (Kd·(1-t))", "=$C$21 * (1 - $C$11)", fmt_pct, "%", "Efecto protector fiscal de los gastos financieros deducibles" if lang == 'ES' else "Tax shield benefit of deductible corporate interest expenses", True),
        ("Peso de la deuda financiera (D / (D + E))" if lang == 'ES' else "Weight of Debt (D / (D + E))", 0.250, fmt_pct, "%", "Estructura financiera objetivo de endeudamiento" if lang == 'ES' else "Target financial leverage structure (debt ratio)", False),
        ("Peso de los fondos propios (E / (D + E))" if lang == 'ES' else "Weight of Equity (E / (D + E))", "=1 - $C$23", fmt_pct, "%", "Estructura financiera objetivo de capital propio" if lang == 'ES' else "Target financial capital structure (equity ratio)", True),
        ("WACC Calculado por Modelo" if lang == 'ES' else "Model Calculated WACC", "=$C$24*$C$20 + $C$23*$C$22", fmt_pct, "%", "WACC = (E/V)·Ke + (D/V)·Kd·(1-t)" if lang == 'ES' else "WACC = (E/V)·Ke + (D/V)·Kd·(1-t)", True),
        ("Modo de selección de WACC" if lang == 'ES' else "WACC Selection Mode", "Calculado" if lang == 'ES' else "Calculated", "@", "modo" if lang == 'ES' else "mode", "Desplegable: 'Calculado' o 'Manual' ('Calculated' / 'Manual')" if lang == 'ES' else "Dropdown: 'Calculated' or 'Manual'", False),
        ("WACC Manual (Override del usuario)" if lang == 'ES' else "Manual WACC (User Override)", 0.095, fmt_pct, "%", "Tasa de descuento corporativa fijada directamente por el CFO" if lang == 'ES' else "Corporate hurdle discount rate set directly by the CFO", False),
        ("WACC EFECTIVO APLICADO AL DCF" if lang == 'ES' else "EFFECTIVE WACC APPLIED TO DCF", f'=IF($C$26="{"Manual" if lang == "ES" else "Manual"}", $C$27, $C$25)', fmt_pct, "%", "Tasa de descuento vinculante que alimenta las proyecciones y el VAN" if lang == 'ES' else "Binding discount rate feeding all DCF projections and NPV", True),
    ]

    for idx, (label, val, fmt, unit, desc, is_calc) in enumerate(wacc_params, start=16):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=is_calc)
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = val
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT if idx == 28 else "000000")
        ws[f"C{idx}"].number_format = fmt
        ws[f"C{idx}"].alignment = Alignment(horizontal="right" if idx != 26 else "center", vertical="center")
        ws[f"C{idx}"].border = borders['highlight'] if idx == 28 else borders['thin']

        ws[f"D{idx}"].value = unit
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9, color="64748B")
        ws[f"D{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"D{idx}"].border = borders['thin']

        ws.merge_cells(f"E{idx}:G{idx}")
        ws[f"E{idx}"].value = desc
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=9, color="334155")
        ws[f"E{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        for c in range(5, 8):
            coord = f"{get_column_letter(c)}{idx}"
            ws[coord].border = borders['thin']
            decorative.add(coord)
        ws.row_dimensions[idx].height = 22

    # 4. SECCIÓN 3: Tabla de Escenarios y Selector Activo
    s3_title = "3. TABLA DE ESCENARIOS Y SELECTOR DE ESCENARIO ACTIVO" if lang == 'ES' else "3. SCENARIO TABLE AND ACTIVE SCENARIO SELECTOR"
    ws["B30"].value = s3_title
    ws["B30"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B30")

    h_cols_scen = [
        "Driver Operativo / Parámetro",
        "Pesimista" if lang == 'ES' else "Pessimistic",
        "Base",
        "Optimista" if lang == 'ES' else "Optimistic",
        "Unidad",
        "Escenario Activo" if lang == 'ES' else "Active Scenario",
    ]
    for c_idx, h_text in enumerate(h_cols_scen, start=2):
        coord = f"{get_column_letter(c_idx)}31"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx >= 3 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    # Selector de Escenario en G32
    ws["B32"].value = "SELECTOR DE ESCENARIO ACTIVO" if lang == 'ES' else "ACTIVE SCENARIO SELECTOR"
    ws["B32"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
    ws["B32"].border = borders['thin']
    ws["C32"].value = "Pesimista" if lang == 'ES' else "Pessimistic"
    ws["C32"].font = Font(name=FONT_NAME, size=9, italic=True)
    ws["C32"].alignment = Alignment(horizontal="center")
    ws["C32"].border = borders['thin']
    ws["D32"].value = "Base"
    ws["D32"].font = Font(name=FONT_NAME, size=9, italic=True)
    ws["D32"].alignment = Alignment(horizontal="center")
    ws["D32"].border = borders['thin']
    ws["E32"].value = "Optimista" if lang == 'ES' else "Optimistic"
    ws["E32"].font = Font(name=FONT_NAME, size=9, italic=True)
    ws["E32"].alignment = Alignment(horizontal="center")
    ws["E32"].border = borders['thin']
    ws["F32"].value = "selector"
    ws["F32"].alignment = Alignment(horizontal="center")
    ws["F32"].border = borders['thin']

    ws["G32"].value = "Base"
    ws["G32"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["G32"].alignment = Alignment(horizontal="center", vertical="center")
    ws["G32"].border = borders['highlight']

    # Fila 33: Probabilidad por Escenario
    ws["B33"].value = "Probabilidad asignada por escenario" if lang == 'ES' else "Assigned Probability by Scenario"
    ws["B33"].font = Font(name=FONT_NAME, size=10, bold=True)
    ws["B33"].border = borders['thin']
    ws["C33"].value = 0.25
    ws["C33"].number_format = fmt_pct
    ws["C33"].alignment = Alignment(horizontal="right")
    ws["C33"].border = borders['thin']
    ws["D33"].value = 0.50
    ws["D33"].number_format = fmt_pct
    ws["D33"].alignment = Alignment(horizontal="right")
    ws["D33"].border = borders['thin']
    ws["E33"].value = 0.25
    ws["E33"].number_format = fmt_pct
    ws["E33"].alignment = Alignment(horizontal="right")
    ws["E33"].border = borders['thin']
    ws["F33"].value = "%"
    ws["F33"].alignment = Alignment(horizontal="center")
    ws["F33"].border = borders['thin']
    ws["G33"].value = '=IF(ABS(SUM(C33:E33)-1)<0.001, "✅ Σ = 100%", "⚠️ Error Σ ≠ 100%")'
    ws["G33"].alignment = Alignment(horizontal="center", vertical="center")
    ws["G33"].border = borders['thin']

    scenario_drivers = [
        ("Volumen comercializado Año 1" if lang == 'ES' else "Commercialized Volume Year 1", 92000, 100000, 110000, '#,##0', "unidades" if lang == 'ES' else "units"),
        ("Crecimiento anual del volumen (%)" if lang == 'ES' else "Annual Volume Growth Rate (%)", 0.030, 0.050, 0.070, fmt_pct, "%"),
        ("Precio de venta unitario Año 1" if lang == 'ES' else "Unit Selling Price Year 1", 24.00, 25.00, 26.00, fmt_curr, "€/u" if lang == 'ES' else "$/u"),
        ("Escalado anual del precio de venta (%)" if lang == 'ES' else "Annual Price Escalation Rate (%)", 0.015, 0.020, 0.025, fmt_pct, "%"),
        ("Coste variable sobre ventas (%)" if lang == 'ES' else "Variable Cost of Sales (%)", 0.620, 0.600, 0.580, fmt_pct, "%"),
        ("OPEX fijo anual Año 1" if lang == 'ES' else "Annual Fixed OPEX Year 1", 470000, 450000, 430000, fmt_curr, "€" if lang == 'ES' else "$"),
        ("Inflación anual del OPEX fijo (%)" if lang == 'ES' else "Annual Fixed OPEX Inflation (%)", 0.020, 0.020, 0.020, fmt_pct, "%"),
        ("CAPEX Tramo 1 (Año 0)" if lang == 'ES' else "CAPEX Tranche 1 (Year 0)", 880000, 850000, 820000, fmt_curr, "€" if lang == 'ES' else "$"),
        ("CAPEX Tramo 2 (Año 1)" if lang == 'ES' else "CAPEX Tranche 2 (Year 1)", 370000, 350000, 330000, fmt_curr, "€" if lang == 'ES' else "$"),
        ("Capital circulante sobre ventas (NWC %)" if lang == 'ES' else "Working Capital to Sales (NWC %)", 0.110, 0.100, 0.090, fmt_pct, "%"),
        ("Crecimiento a perpetuidad (g residual)" if lang == 'ES' else "Terminal Growth Rate (g residual)", 0.010, 0.015, 0.020, fmt_pct, "%"),
    ]

    for idx, (label, v_pes, v_base, v_opt, fmt, unit) in enumerate(scenario_drivers, start=34):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10)
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = v_pes
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10)
        ws[f"C{idx}"].number_format = fmt
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"C{idx}"].border = borders['thin']

        ws[f"D{idx}"].value = v_base
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=10)
        ws[f"D{idx}"].number_format = fmt
        ws[f"D{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"D{idx}"].border = borders['thin']

        ws[f"E{idx}"].value = v_opt
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=10)
        ws[f"E{idx}"].number_format = fmt
        ws[f"E{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"E{idx}"].border = borders['thin']

        ws[f"F{idx}"].value = unit
        ws[f"F{idx}"].font = Font(name=FONT_NAME, size=9, color="64748B")
        ws[f"F{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"F{idx}"].border = borders['thin']

        # Celda G con fórmula INDEX/MATCH
        ws[f"G{idx}"].value = f"=INDEX(C{idx}:E{idx}, 1, MATCH($G$32, $C$31:$E$31, 0))"
        ws[f"G{idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"G{idx}"].number_format = fmt
        ws[f"G{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"G{idx}"].border = borders['thin']

    # Fila 45: Interruptor "Incluir Valor Residual"
    ws["B45"].value = "Interruptor de Valor Residual (Gordon Shapiro)" if lang == 'ES' else "Terminal Value Switch (Gordon Shapiro)"
    ws["B45"].font = Font(name=FONT_NAME, size=10, bold=True)
    ws["B45"].border = borders['thin']
    ws["C45"].value = "No"
    ws["C45"].alignment = Alignment(horizontal="center")
    ws["C45"].border = borders['thin']
    ws["D45"].value = "No"
    ws["D45"].alignment = Alignment(horizontal="center")
    ws["D45"].border = borders['thin']
    ws["E45"].value = "Sí" if lang == 'ES' else "Yes"
    ws["E45"].alignment = Alignment(horizontal="center")
    ws["E45"].border = borders['thin']
    ws["F45"].value = "on/off"
    ws["F45"].alignment = Alignment(horizontal="center")
    ws["F45"].border = borders['thin']
    ws["G45"].value = "No"
    ws["G45"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_AMBER_TEXT)
    ws["G45"].alignment = Alignment(horizontal="center", vertical="center")
    ws["G45"].border = borders['highlight']

    # 5. SECCIÓN 4: Rangos de Sensibilidad Tornado
    s4_title = "4. RANGOS DE SENSIBILIDAD PARA ANÁLISIS TORNADO (PERTURBACIONES SOBRE BASE)" if lang == 'ES' else "4. SENSITIVITY RANGES FOR TORNADO ANALYSIS (PERTURBATIONS OVER BASE)"
    ws["B48"].value = s4_title
    ws["B48"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B48")

    h_cols_torn = [
        "Driver de Sensibilidad Evaluado",
        "Valor Base",
        "Valor Bajo (Sensibilidad)",
        "Valor Alto (Sensibilidad)",
        "Unidad",
        "Rango de Perturbación",
    ] if lang == 'ES' else [
        "Evaluated Sensitivity Driver",
        "Base Value",
        "Low Value (Sensitivity)",
        "High Value (Sensitivity)",
        "Unit",
        "Perturbation Range",
    ]
    for c_idx, h_text in enumerate(h_cols_torn, start=2):
        coord = f"{get_column_letter(c_idx)}49"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx >= 3 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    tornado_inputs = [
        ("Precio Unitario (€/u)" if lang == 'ES' else "Unit Price ($/unit)", "=D36", 21.00, 29.00, fmt_curr, "€/u" if lang == 'ES' else "$/u", "±16.0%"),
        ("Volumen Comercializado Año 1" if lang == 'ES' else "Year 1 Sales Volume", "=D34", 85000, 115000, '#,##0', "unidades" if lang == 'ES' else "units", "±15.0%"),
        ("Coste Variable sobre ventas (%)" if lang == 'ES' else "Variable Cost of Sales (%)", "=D38", 0.550, 0.650, fmt_pct, "%", "±5.0 pp"),
        ("CAPEX Total (Tramo 1 + Tramo 2)" if lang == 'ES' else "Total CAPEX (Tranche 1 + 2)", "=D41+D42", 1020000, 1380000, fmt_curr, "€" if lang == 'ES' else "$", "±15.0%"),
        ("OPEX Fijo Anual (€)" if lang == 'ES' else "Annual Fixed OPEX ($)", "=D39", 380000, 520000, fmt_curr, "€" if lang == 'ES' else "$", "±70 k€" if lang == 'ES' else "±$70k"),
        ("Crecimiento Anual del Volumen (%)" if lang == 'ES' else "Volume Growth Rate (%)", "=D35", 0.020, 0.080, fmt_pct, "%", "±3.0 pp"),
        ("Tasa de Descuento (WACC %)" if lang == 'ES' else "Discount Rate (WACC %)", "=$C$28", 0.075, 0.115, fmt_pct, "%", "±2.0 pp"),
        ("Capital Circulante sobre ventas (%)" if lang == 'ES' else "Working Capital to Sales (%)", "=D43", 0.070, 0.130, fmt_pct, "%", "±3.0 pp"),
    ]

    for idx, (label, f_base, v_low, v_high, fmt, unit, r_txt) in enumerate(tornado_inputs, start=50):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10)
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = f_base
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"C{idx}"].number_format = fmt
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"C{idx}"].border = borders['thin']

        ws[f"D{idx}"].value = v_low
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=10)
        ws[f"D{idx}"].number_format = fmt
        ws[f"D{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"D{idx}"].border = borders['thin']

        ws[f"E{idx}"].value = v_high
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=10)
        ws[f"E{idx}"].number_format = fmt
        ws[f"E{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"E{idx}"].border = borders['thin']

        ws[f"F{idx}"].value = unit
        ws[f"F{idx}"].font = Font(name=FONT_NAME, size=9, color="64748B")
        ws[f"F{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"F{idx}"].border = borders['thin']

        ws[f"G{idx}"].value = r_txt
        ws[f"G{idx}"].font = Font(name=FONT_NAME, size=9, italic=True)
        ws[f"G{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"G{idx}"].border = borders['thin']

    # Validaciones de Datos
    dv_scen = DataValidation(type="list", formula1='"Pesimista,Base,Optimista"' if lang == 'ES' else '"Pessimistic,Base,Optimistic"', allow_blank=False)
    ws.add_data_validation(dv_scen)
    dv_scen.add("G32")

    dv_wacc_mode = DataValidation(type="list", formula1='"Calculado,Manual"' if lang == 'ES' else '"Calculated,Manual"', allow_blank=False)
    ws.add_data_validation(dv_wacc_mode)
    dv_wacc_mode.add("C26")

    dv_switch_vr = DataValidation(type="list", formula1='"Sí,No"' if lang == 'ES' else '"Yes,No"', allow_blank=False)
    ws.add_data_validation(dv_switch_vr)
    dv_switch_vr.add("G45")

    # Anchos de columna
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 48
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 18
    ws.column_dimensions["F"].width = 14
    ws.column_dimensions["G"].width = 24

    finalize_sheet(ws, decorative_cells=frozenset(decorative))


def build_tab3_dcf(wb, lang='ES'):
    """Construye la Pestaña 3: Proyección DCF / DCF Projection."""
    sheet_title = "Proyección DCF" if lang == 'ES' else "DCF Projection"
    assumptions_sheet = "Supuestos & Drivers" if lang == 'ES' else "Assumptions & Drivers"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    fmt_curr = '#,##0 "€";[Red]-#,##0 "€"' if lang == 'ES' else '"$"#,##0;[Red]("$"#,##0)'
    fmt_pct = '0.0%'
    fmt_factor = '0.0000'

    # 1. Cabecera Principal
    h_title = (
        "PROYECCIÓN DE FLUJO DE CAJA LIBRE DESCONTADO (DCF INSTITUCIONAL: AÑOS 0 A 5)"
        if lang == 'ES' else
        "DISCOUNTED FREE CASH FLOW PROJECTION (INSTITUTIONAL DCF: YEARS 0 TO 5)"
    )
    style_merged_header(ws, "B2:I3", h_title, decorative, COLOR_NAVY_DARK, "FFFFFF", 12)
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 20

    # 2. Cabeceras de Columnas (Fila 5)
    cols_h = [
        "Línea de Proyección Financiera" if lang == 'ES' else "Financial Projection Line",
        "Unidad" if lang == 'ES' else "Unit",
        "Año 0 (Inversión)" if lang == 'ES' else "Year 0 (Capex)",
        "Año 1" if lang == 'ES' else "Year 1",
        "Año 2" if lang == 'ES' else "Year 2",
        "Año 3" if lang == 'ES' else "Year 3",
        "Año 4" if lang == 'ES' else "Year 4",
        "Año 5" if lang == 'ES' else "Year 5",
    ]
    for c_idx, h_text in enumerate(cols_h, start=2):
        coord = f"{get_column_letter(c_idx)}5"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx >= 3 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    # 3. Filas Operativas del DCF (Filas 6 a 28)
    # Volumen
    ws["B6"].value = "Volumen comercializado (unidades)" if lang == 'ES' else "Commercialized Volume (units)"
    ws["C6"].value = "unidades" if lang == 'ES' else "units"
    ws["D6"].value = 0
    ws["E6"].value = f"='{assumptions_sheet}'!$G$34"
    ws["F6"].value = f"=E6*(1+'{assumptions_sheet}'!$G$35)"
    ws["G6"].value = f"=F6*(1+'{assumptions_sheet}'!$G$35)"
    ws["H6"].value = f"=G6*(1+'{assumptions_sheet}'!$G$35)"
    ws["I6"].value = f"=H6*(1+'{assumptions_sheet}'!$G$35)"

    # Precio Unitario
    ws["B7"].value = "Precio de venta unitario (€/u)" if lang == 'ES' else "Unit Selling Price ($/u)"
    ws["C7"].value = "€/u" if lang == 'ES' else "$/u"
    ws["D7"].value = 0.0
    ws["E7"].value = f"='{assumptions_sheet}'!$G$36"
    ws["F7"].value = f"=E7*(1+'{assumptions_sheet}'!$G$37)"
    ws["G7"].value = f"=F7*(1+'{assumptions_sheet}'!$G$37)"
    ws["H7"].value = f"=G7*(1+'{assumptions_sheet}'!$G$37)"
    ws["I7"].value = f"=H7*(1+'{assumptions_sheet}'!$G$37)"

    # Ingresos Brutos
    ws["B8"].value = "Ingresos por ventas" if lang == 'ES' else "Revenue from Sales"
    ws["C8"].value = "€" if lang == 'ES' else "$"
    ws["D8"].value = 0.0
    ws["E8"].value = "=E6*E7"
    ws["F8"].value = "=F6*F7"
    ws["G8"].value = "=G6*G7"
    ws["H8"].value = "=H6*H7"
    ws["I8"].value = "=I6*I7"

    # Costes Variables
    ws["B9"].value = "(-) Costes variables operativos" if lang == 'ES' else "(-) Variable Operating Costs"
    ws["C9"].value = "€" if lang == 'ES' else "$"
    ws["D9"].value = 0.0
    ws["E9"].value = f"=E8*'{assumptions_sheet}'!$G$38"
    ws["F9"].value = f"=F8*'{assumptions_sheet}'!$G$38"
    ws["G9"].value = f"=G8*'{assumptions_sheet}'!$G$38"
    ws["H9"].value = f"=H8*'{assumptions_sheet}'!$G$38"
    ws["I9"].value = f"=I8*'{assumptions_sheet}'!$G$38"

    # Margen Bruto
    ws["B10"].value = "MARGEN BRUTO" if lang == 'ES' else "GROSS PROFIT"
    ws["C10"].value = "€" if lang == 'ES' else "$"
    ws["D10"].value = 0.0
    ws["E10"].value = "=E8-E9"
    ws["F10"].value = "=F8-F9"
    ws["G10"].value = "=G8-G9"
    ws["H10"].value = "=H8-H9"
    ws["I10"].value = "=I8-I9"

    # OPEX Fijo
    ws["B11"].value = "(-) OPEX fijo anual de explotación" if lang == 'ES' else "(-) Annual Fixed Operating OPEX"
    ws["C11"].value = "€" if lang == 'ES' else "$"
    ws["D11"].value = 0.0
    ws["E11"].value = f"='{assumptions_sheet}'!$G$39"
    ws["F11"].value = f"=E11*(1+'{assumptions_sheet}'!$G$40)"
    ws["G11"].value = f"=F11*(1+'{assumptions_sheet}'!$G$40)"
    ws["H11"].value = f"=G11*(1+'{assumptions_sheet}'!$G$40)"
    ws["I11"].value = f"=H11*(1+'{assumptions_sheet}'!$G$40)"

    # EBITDA
    ws["B12"].value = "EBITDA (Resultado Bruto de Explotación)" if lang == 'ES' else "EBITDA (Operating Cash Flow)"
    ws["C12"].value = "€" if lang == 'ES' else "$"
    ws["D12"].value = 0.0
    ws["E12"].value = "=E10-E11"
    ws["F12"].value = "=F10-F11"
    ws["G12"].value = "=G10-G11"
    ws["H12"].value = "=H10-H11"
    ws["I12"].value = "=I10-I11"

    # Margen EBITDA %
    ws["B13"].value = "Margen EBITDA (%)" if lang == 'ES' else "EBITDA Margin (%)"
    ws["C13"].value = "%"
    ws["D13"].value = 0.0
    ws["E13"].value = "=IF(E8>0, E12/E8, 0)"
    ws["F13"].value = "=IF(F8>0, F12/F8, 0)"
    ws["G13"].value = "=IF(G8>0, G12/G8, 0)"
    ws["H13"].value = "=IF(H8>0, H12/H8, 0)"
    ws["I13"].value = "=IF(I8>0, I12/I8, 0)"

    # Amortización (D&A)
    ws["B14"].value = "(-) Amortización lineal del inmovilizado (D&A)" if lang == 'ES' else "(-) Straight-Line Depreciation (D&A)"
    ws["C14"].value = "€" if lang == 'ES' else "$"
    ws["D14"].value = 0.0
    ws["E14"].value = f"='{assumptions_sheet}'!$G$41/'{assumptions_sheet}'!$C$10"
    ws["F14"].value = f"=('{assumptions_sheet}'!$G$41+'{assumptions_sheet}'!$G$42)/'{assumptions_sheet}'!$C$10"
    ws["G14"].value = "=F14"
    ws["H14"].value = "=F14"
    ws["I14"].value = "=F14"

    # EBIT
    ws["B15"].value = "EBIT (Resultado Operativo Neto)" if lang == 'ES' else "EBIT (Operating Income)"
    ws["C15"].value = "€" if lang == 'ES' else "$"
    ws["D15"].value = 0.0
    ws["E15"].value = "=E12-E14"
    ws["F15"].value = "=F12-F14"
    ws["G15"].value = "=G12-G14"
    ws["H15"].value = "=H12-H14"
    ws["I15"].value = "=I12-I14"

    # Impuestos sobre EBIT
    ws["B16"].value = "(-) Impuestos teóricos sobre EBIT (EBIT·t)" if lang == 'ES' else "(-) Operating Taxes on EBIT (EBIT·t)"
    ws["C16"].value = "€" if lang == 'ES' else "$"
    ws["D16"].value = 0.0
    ws["E16"].value = f"=MAX(0, E15*'{assumptions_sheet}'!$C$11)"
    ws["F16"].value = f"=MAX(0, F15*'{assumptions_sheet}'!$C$11)"
    ws["G16"].value = f"=MAX(0, G15*'{assumptions_sheet}'!$C$11)"
    ws["H16"].value = f"=MAX(0, H15*'{assumptions_sheet}'!$C$11)"
    ws["I16"].value = f"=MAX(0, I15*'{assumptions_sheet}'!$C$11)"

    # NOPAT
    ws["B17"].value = "NOPAT (Beneficio Operativo después de Impuestos)" if lang == 'ES' else "NOPAT (Net Operating Profit After Tax)"
    ws["C17"].value = "€" if lang == 'ES' else "$"
    ws["D17"].value = 0.0
    ws["E17"].value = "=E15-E16"
    ws["F17"].value = "=F15-F16"
    ws["G17"].value = "=G15-G16"
    ws["H17"].value = "=H15-H16"
    ws["I17"].value = "=I15-I16"

    # (+) Amortización
    ws["B18"].value = "(+) Amortización lineal (gasto no monetario)" if lang == 'ES' else "(+) Depreciation (non-cash add-back)"
    ws["C18"].value = "€" if lang == 'ES' else "$"
    ws["D18"].value = 0.0
    ws["E18"].value = "=E14"
    ws["F18"].value = "=F14"
    ws["G18"].value = "=G14"
    ws["H18"].value = "=H14"
    ws["I18"].value = "=I14"

    # (-) CAPEX
    ws["B19"].value = "(-) Inversión en Inmovilizado (CAPEX)" if lang == 'ES' else "(-) Capital Expenditure (CAPEX)"
    ws["C19"].value = "€" if lang == 'ES' else "$"
    ws["D19"].value = f"='{assumptions_sheet}'!$G$41"
    ws["E19"].value = f"='{assumptions_sheet}'!$G$42"
    ws["F19"].value = 0.0
    ws["G19"].value = 0.0
    ws["H19"].value = 0.0
    ws["I19"].value = 0.0

    # NWC Saldo
    ws["B20"].value = "Capital Circulante Operativo (NWC = Ventas·%NWC)" if lang == 'ES' else "Operating Working Capital (NWC = Sales·%NWC)"
    ws["C20"].value = "€" if lang == 'ES' else "$"
    ws["D20"].value = 0.0
    ws["E20"].value = f"=E8*'{assumptions_sheet}'!$G$43"
    ws["F20"].value = f"=F8*'{assumptions_sheet}'!$G$43"
    ws["G20"].value = f"=G8*'{assumptions_sheet}'!$G$43"
    ws["H20"].value = f"=H8*'{assumptions_sheet}'!$G$43"
    ws["I20"].value = f"=I8*'{assumptions_sheet}'!$G$43"

    # (-) Variación NWC
    ws["B21"].value = "(-) Variación de Capital Circulante (ΔNWC)" if lang == 'ES' else "(-) Change in Working Capital (ΔNWC)"
    ws["C21"].value = "€" if lang == 'ES' else "$"
    ws["D21"].value = 0.0
    ws["E21"].value = "=E20-D20"
    ws["F21"].value = "=F20-E20"
    ws["G21"].value = "=G20-F20"
    ws["H21"].value = "=H20-G20"
    ws["I21"].value = "=I20-H20"

    # FLUJO DE CAJA LIBRE (FCF)
    ws["B22"].value = "FLUJO DE CAJA LIBRE (FCF = NOPAT+D&A-CAPEX-ΔNWC)" if lang == 'ES' else "FREE CASH FLOW (FCF = NOPAT+D&A-CAPEX-ΔNWC)"
    ws["C22"].value = "€" if lang == 'ES' else "$"
    ws["D22"].value = "=-D19"
    ws["E22"].value = "=E17+E18-E19-E21"
    ws["F22"].value = "=F17+F18-F19-F21"
    ws["G22"].value = "=G17+G18-G19-G21"
    ws["H22"].value = "=H17+H18-H19-H21"
    ws["I22"].value = "=I17+I18-I19-I21"

    # Factor de Descuento
    ws["B23"].value = f"Factor de Descuento (1 / (1 + WACC)^t)" if lang == 'ES' else "Discount Factor (1 / (1 + WACC)^t)"
    ws["C23"].value = "factor"
    ws["D23"].value = 1.0
    ws["E23"].value = f"=1/((1+'{assumptions_sheet}'!$C$28)^1)"
    ws["F23"].value = f"=1/((1+'{assumptions_sheet}'!$C$28)^2)"
    ws["G23"].value = f"=1/((1+'{assumptions_sheet}'!$C$28)^3)"
    ws["H23"].value = f"=1/((1+'{assumptions_sheet}'!$C$28)^4)"
    ws["I23"].value = f"=1/((1+'{assumptions_sheet}'!$C$28)^5)"

    # Valor Presente FCF
    ws["B24"].value = "Valor Presente del Flujo (VP del FCF)" if lang == 'ES' else "Present Value of Cash Flow (PV of FCF)"
    ws["C24"].value = "€" if lang == 'ES' else "$"
    ws["D24"].value = "=D22*D23"
    ws["E24"].value = "=E22*E23"
    ws["F24"].value = "=F22*F23"
    ws["G24"].value = "=G22*G23"
    ws["H24"].value = "=H22*H23"
    ws["I24"].value = "=I22*I23"

    # Flujo Acumulado Nominal
    ws["B25"].value = "Flujo de Caja Libre Acumulado (Curva J Nominal)" if lang == 'ES' else "Cumulative Free Cash Flow (Nominal J-Curve)"
    ws["C25"].value = "€" if lang == 'ES' else "$"
    ws["D25"].value = "=D22"
    ws["E25"].value = "=D25+E22"
    ws["F25"].value = "=E25+F22"
    ws["G25"].value = "=F25+G22"
    ws["H25"].value = "=G25+H22"
    ws["I25"].value = "=H25+I22"

    # Flujo Acumulado Descontado
    ws["B26"].value = "Valor Presente Acumulado (Curva J Descontada)" if lang == 'ES' else "Cumulative Present Value (Discounted J-Curve)"
    ws["C26"].value = "€" if lang == 'ES' else "$"
    ws["D26"].value = "=D24"
    ws["E26"].value = "=D26+E24"
    ws["F26"].value = "=E26+F24"
    ws["G26"].value = "=F26+G24"
    ws["H26"].value = "=G26+H24"
    ws["I26"].value = "=H26+I24"

    # Filas de Cruce para Interpolación de Payback
    ws["B27"].value = "Fila Auxiliar: Cruce Payback Simple" if lang == 'ES' else "Auxiliary Row: Simple Payback Cross"
    ws["C27"].value = "años" if lang == 'ES' else "yrs"
    ws["D27"].value = '""'
    ws["E27"].value = '=IF(AND(D25<0, E25>=0), 0 + (-D25/E22), "")'
    ws["F27"].value = '=IF(AND(E25<0, F25>=0), 1 + (-E25/F22), "")'
    ws["G27"].value = '=IF(AND(F25<0, G25>=0), 2 + (-F25/G22), "")'
    ws["H27"].value = '=IF(AND(G25<0, H25>=0), 3 + (-G25/H22), "")'
    ws["I27"].value = '=IF(AND(H25<0, I25>=0), 4 + (-H25/I22), "")'

    ws["B28"].value = "Fila Auxiliar: Cruce Payback Descontado" if lang == 'ES' else "Auxiliary Row: Discounted Payback Cross"
    ws["C28"].value = "años" if lang == 'ES' else "yrs"
    ws["D28"].value = '""'
    ws["E28"].value = '=IF(AND(D26<0, E26>=0), 0 + (-D26/E24), "")'
    ws["F28"].value = '=IF(AND(E26<0, F26>=0), 1 + (-E26/F24), "")'
    ws["G28"].value = '=IF(AND(F26<0, G26>=0), 2 + (-F26/G24), "")'
    ws["H28"].value = '=IF(AND(G26<0, H26>=0), 3 + (-G26/H24), "")'
    ws["I28"].value = '=IF(AND(H26<0, I26>=0), 4 + (-H26/I24), "")'

    # Valor Residual Gordon (Fila 29)
    ws["B29"].value = "Valor Residual a Perpetuidad (Gordon Shapiro)" if lang == 'ES' else "Terminal Value at Perpetuity (Gordon Shapiro)"
    ws["C29"].value = "€" if lang == 'ES' else "$"
    for col_c in ["D", "E", "F", "G", "H"]:
        ws[f"{col_c}29"].value = 0.0
    sw_yes = "Sí" if lang == 'ES' else "Yes"
    ws["I29"].value = f'=IF(\'{assumptions_sheet}\'!$G$45="{sw_yes}", IF(\'{assumptions_sheet}\'!$C$28>\'{assumptions_sheet}\'!$G$44, I22*(1+\'{assumptions_sheet}\'!$G$44)/(\'{assumptions_sheet}\'!$C$28-\'{assumptions_sheet}\'!$G$44), 0), 0)'

    # VP Valor Residual (Fila 30)
    ws["B30"].value = "VP del Valor Residual Descontado" if lang == 'ES' else "PV of Discounted Terminal Value"
    ws["C30"].value = "€" if lang == 'ES' else "$"
    for col_c in ["D", "E", "F", "G", "H"]:
        ws[f"{col_c}30"].value = 0.0
    ws["I30"].value = f'=I29/((1+\'{assumptions_sheet}\'!$C$28)^5)'

    # Formatos de celdas para filas 6 a 30
    for r in range(6, 31):
        ws[f"B{r}"].font = Font(name=FONT_NAME, size=10, bold=(r in [10, 12, 15, 17, 22, 25, 26]))
        ws[f"B{r}"].border = borders['thin']
        ws[f"C{r}"].font = Font(name=FONT_NAME, size=9, color="64748B")
        ws[f"C{r}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"C{r}"].border = borders['thin']

        for c_idx in range(4, 10):
            coord = f"{get_column_letter(c_idx)}{r}"
            cell = ws[coord]
            cell.border = borders['thin']
            cell.alignment = Alignment(horizontal="right", vertical="center")

            if r == 6:
                cell.number_format = '#,##0'
            elif r in [7]:
                cell.number_format = fmt_curr
            elif r in [13]:
                cell.number_format = fmt_pct
            elif r in [23]:
                cell.number_format = fmt_factor
            elif r in [27, 28]:
                cell.number_format = '0.00'
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.number_format = fmt_curr

            if r == 22:
                cell.font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
                cell.border = borders['highlight']
            elif r in [10, 12, 17, 26]:
                cell.font = Font(name=FONT_NAME, size=10, bold=True)

    # 4. Sección Resumen de Métricas Financieras (Filas 32 a 42)
    s_metrics_title = "RESUMEN DE RENTABILIDAD, LIQUIDEZ Y DECISIÓN DE INVERSIÓN (C-LEVEL)" if lang == 'ES' else "SUMMARY OF PROFITABILITY, LIQUIDITY & INVESTMENT METRICS (C-LEVEL)"
    ws["B32"].value = s_metrics_title
    ws["B32"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B32")

    metrics_rows = [
        ("VALOR ACTUAL NETO (VAN a 5 Años)" if lang == 'ES' else "NET PRESENT VALUE (NPV 5-Year)", f"=D22 + NPV('{assumptions_sheet}'!$C$28, E22:I22) + I30", fmt_curr, "€" if lang == 'ES' else "$", "VAN > 0 indica creación neta de valor económico para el accionista" if lang == 'ES' else "NPV > 0 indicates net economic shareholder value creation"),
        ("VALOR ACTUAL NETO A 3 AÑOS (NPV 3Y)" if lang == 'ES' else "NET PRESENT VALUE AT 3 YEARS (NPV 3Y)", f"=D22 + NPV('{assumptions_sheet}'!$C$28, E22:G22)", fmt_curr, "€" if lang == 'ES' else "$", "Rentabilidad acumulada en horizonte conservador a 3 años" if lang == 'ES' else "Cumulative profitability on conservative 3-year horizon"),
        ("TASA INTERNA DE RETORNO (TIR / IRR)" if lang == 'ES' else "INTERNAL RATE OF RETURN (IRR)", "=IFERROR(IRR(D22:I22), \"n/d\")", fmt_pct, "%", "Tasa de descuento de equilibrio donde VAN = 0 (exigida TIR ≥ WACC+3pp)" if lang == 'ES' else "Break-even discount rate where NPV = 0 (required IRR ≥ WACC+3pp)"),
        ("TIR MODIFICADA (MIRR / TIRM)" if lang == 'ES' else "MODIFIED INTERNAL RATE OF RETURN (MIRR)", f"=IFERROR(MIRR(D22:I22, '{assumptions_sheet}'!$C$28, '{assumptions_sheet}'!$C$9), \"n/d\")", fmt_pct, "%", "Corrige la hipótesis irrealista de reinversión a la propia TIR" if lang == 'ES' else "Eliminates unrealistic reinvestment assumption of standard IRR"),
        ("PAYBACK SIMPLE (Plazo de Recuperación Nominal)" if lang == 'ES' else "SIMPLE PAYBACK (Nominal Recovery Period)", "=IFERROR(MIN(E27:I27), \"> 5 años\")" if lang == 'ES' else "=IFERROR(MIN(E27:I27), \"> 5 yrs\")", '0.00 "años"' if lang == 'ES' else '0.00 "yrs"', "años" if lang == 'ES' else "yrs", "Tiempo requerido para recuperar el desembolso nominal invertido" if lang == 'ES' else "Time required to recover initial cash outlay without time value"),
        ("PAYBACK DESCONTADO (Con Coste de Capital)" if lang == 'ES' else "DISCOUNTED PAYBACK (With Cost of Capital)", "=IFERROR(MIN(E28:I28), \"> 5 años\")" if lang == 'ES' else "=IFERROR(MIN(E28:I28), \"> 5 yrs\")", '0.00 "años"' if lang == 'ES' else '0.00 "yrs"', "años" if lang == 'ES' else "yrs", "Tiempo requerido para recuperar la inversión considerando el WACC" if lang == 'ES' else "Time required to recover capital taking WACC opportunity cost into account"),
        ("ÍNDICE DE RENTABILIDAD (PI / Profitability Index)" if lang == 'ES' else "PROFITABILITY INDEX (PI / Benefit-Cost Ratio)", "=SUMIF(E24:I24, \">0\") / ABS(D24 + SUMIF(E24:I24, \"<0\"))", '0.00"x"', "x", "Relación de valor creado por cada euro de inversión descontada" if lang == 'ES' else "Present value generated per dollar of discounted capital invested"),
        ("NECESIDAD MÁXIMA DE FINANCIACIÓN (Peak Funding)" if lang == 'ES' else "MAXIMUM FINANCING REQUIREMENT (Peak Funding)", "=MIN(D25:I25)", fmt_curr, "€" if lang == 'ES' else "$", "Punto de máxima exposición de tesorería y necesidad crediticia" if lang == 'ES' else "Maximum cash flow trough and peak working treasury commitment"),
        ("COSTE DE CAPITAL MEDIO PONDERADO (WACC)" if lang == 'ES' else "WEIGHTED AVERAGE COST OF CAPITAL (WACC)", f"='{assumptions_sheet}'!$C$28", fmt_pct, "%", "Tasa de descuento de corte institucional aplicada al flujo de fondos" if lang == 'ES' else "Institutional discount hurdle rate applied to projected cash flows"),
    ]

    for idx, (label, formula_val, fmt, unit, desc) in enumerate(metrics_rows, start=33):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=(idx in [33, 35, 38]))
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = formula_val
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT if idx == 33 else "000000")
        ws[f"C{idx}"].number_format = fmt
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"C{idx}"].border = borders['highlight'] if idx == 33 else borders['thin']

        ws[f"D{idx}"].value = unit
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9, color="64748B")
        ws[f"D{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"D{idx}"].border = borders['thin']

        ws[f"E{idx}"].value = desc
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=9, color="334155")
        ws[f"E{idx}"].border = borders['thin']

    # Fila 42: Control de Cuadre
    ws["B42"].value = "CONTROL DE CUADRE MATEMÁTICO (NPV vs. Σ VP)" if lang == 'ES' else "MATHEMATICAL BALANCING CHECK (NPV vs. Σ PV)"
    ws["B42"].font = Font(name=FONT_NAME, size=10, bold=True)
    ws["B42"].border = borders['thin']
    ws["C42"].value = '=IF(ABS(C33 - (SUM(D24:I24)+I30)) < 1, "✅ Modelo cuadrado", "⚠️ Revisar cálculo")' if lang == 'ES' else '=IF(ABS(C33 - (SUM(D24:I24)+I30)) < 1, "✅ Model Balanced", "⚠️ Check Calculation")'
    ws["C42"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_GREEN_TEXT)
    ws["C42"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C42"].border = borders['highlight']
    ws["D42"].value = "control"
    ws["D42"].alignment = Alignment(horizontal="center")
    ws["D42"].border = borders['thin']
    ws["E42"].value = "Verificación estricta: función NPV de Excel coincide exactamente con la suma discreta de valores presentes" if lang == 'ES' else "Strict verification: Excel NPV function matches discrete discounted sum"
    ws["E42"].font = Font(name=FONT_NAME, size=9, italic=True)
    ws["E42"].border = borders['thin']

    # Anchos de columna
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 48
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 16
    ws.column_dimensions["F"].width = 16
    ws.column_dimensions["G"].width = 16
    ws.column_dimensions["H"].width = 16
    ws.column_dimensions["I"].width = 18

    finalize_sheet(ws, decorative_cells=frozenset(decorative))


def build_tab4_sensitivity(wb, lang='ES'):
    """Construye la Pestaña 4: Sensibilidad & Tornado / Sensitivity & Tornado."""
    sheet_title = "Sensibilidad & Tornado" if lang == 'ES' else "Sensitivity & Tornado"
    dcf_sheet = "Proyección DCF" if lang == 'ES' else "DCF Projection"
    assumptions_sheet = "Supuestos & Drivers" if lang == 'ES' else "Assumptions & Drivers"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    fmt_curr = '#,##0 "€";[Red]-#,##0 "€"' if lang == 'ES' else '"$"#,##0;[Red]("$"#,##0)'
    fmt_pct = '0.0%'

    # 1. Cabecera Principal
    h_title = (
        "ANÁLISIS DE SENSIBILIDAD UNIVARIABLE, GRÁFICO TORNADO & ESCENARIOS PROBABILÍSTICOS"
        if lang == 'ES' else
        "UNIVARIATE SENSITIVITY ANALYSIS, TORNADO CHART & PROBABILISTIC SCENARIOS"
    )
    style_merged_header(ws, "B2:N3", h_title, decorative, COLOR_NAVY_DARK, "FFFFFF", 12)
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 20

    # 2. MOTOR DE SENSIBILIDAD: Bloque de Filas de Recálculo Explícito (Filas 5 a 23)
    s1_title = "1. MOTOR DE RECÁLCULO DCF PARA SENSIBILIDAD (SIN TABLAS DE DATOS - COMPATIBLE GOOGLE SHEETS)" if lang == 'ES' else "1. DCF SENSITIVITY RECALCULATION ENGINE (WITHOUT DATA TABLES - SHEETS COMPATIBLE)"
    ws["B5"].value = s1_title
    ws["B5"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B5")

    h_motor = [
        "Caso Evaluado",
        "Driver / Variable",
        "Valor Evaluado",
        "FCF Año 0",
        "FCF Año 1",
        "FCF Año 2",
        "FCF Año 3",
        "FCF Año 4",
        "FCF Año 5",
        "WACC Fila",
        "VAN 5 Años",
        "Δ vs. Base",
        "Estado Motor",
    ] if lang == 'ES' else [
        "Evaluated Case",
        "Driver / Variable",
        "Tested Value",
        "FCF Year 0",
        "FCF Year 1",
        "FCF Year 2",
        "FCF Year 3",
        "FCF Year 4",
        "FCF Year 5",
        "Row WACC",
        "NPV 5-Year",
        "Δ vs. Base",
        "Engine Status",
    ]
    for c_idx, h_text in enumerate(h_motor, start=2):
        coord = f"{get_column_letter(c_idx)}6"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx >= 4 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    # Fila 7: Caso Base
    ws["B7"].value = "Escenario Base (Referencia)" if lang == 'ES' else "Base Scenario (Benchmark)"
    ws["C7"].value = "Base Central" if lang == 'ES' else "Central Base"
    ws["D7"].value = "-"
    ws["E7"].value = f"='{dcf_sheet}'!$D$22"
    ws["F7"].value = f"='{dcf_sheet}'!$E$22"
    ws["G7"].value = f"='{dcf_sheet}'!$F$22"
    ws["H7"].value = f"='{dcf_sheet}'!$G$22"
    ws["I7"].value = f"='{dcf_sheet}'!$H$22"
    ws["J7"].value = f"='{dcf_sheet}'!$I$22"
    ws["K7"].value = f"='{assumptions_sheet}'!$C$28"
    ws["L7"].value = "=E7 + NPV(K7, F7:J7)"
    ws["M7"].value = "=L7 - $L$7"
    ws["N7"].value = f'=IF(ABS(L7 - \'{dcf_sheet}\'!$C$33) < 1, "{"✅ Motor cuadrado" if lang == "ES" else "✅ Engine Balanced"}", "{"⚠️ Revisar motor" if lang == "ES" else "⚠️ Check Engine"}")'

    # 16 Filas de Recálculo: 8 Drivers x 2 casos (Bajo y Alto)
    # Lista de drivers con sus referencias de Supuestos
    recalc_cases = [
        # (ID, Label, Driver_name, Val_coord, Is_High_or_Low, Param_row)
        ("p_low", "Precio Unitario - Bajo" if lang == 'ES' else "Unit Price - Low", "Precio Unitario", f"='{assumptions_sheet}'!$D$50", "low", 50),
        ("p_high", "Precio Unitario - Alto" if lang == 'ES' else "Unit Price - High", "Precio Unitario", f"='{assumptions_sheet}'!$E$50", "high", 50),
        ("v_low", "Volumen Año 1 - Bajo" if lang == 'ES' else "Volume Year 1 - Low", "Volumen Año 1", f"='{assumptions_sheet}'!$D$51", "low", 51),
        ("v_high", "Volumen Año 1 - Alto" if lang == 'ES' else "Volume Year 1 - High", "Volumen Año 1", f"='{assumptions_sheet}'!$E$51", "high", 51),
        ("vc_low", "Coste Variable % - Bajo (Favorable)" if lang == 'ES' else "Variable Cost % - Low (Favorable)", "Coste Variable %", f"='{assumptions_sheet}'!$D$52", "low", 52),
        ("vc_high", "Coste Variable % - Alto (Desfavorable)" if lang == 'ES' else "Variable Cost % - High (Unfavorable)", "Coste Variable %", f"='{assumptions_sheet}'!$E$52", "high", 52),
        ("c_low", "CAPEX Total - Bajo (-15%)" if lang == 'ES' else "Total CAPEX - Low (-15%)", "CAPEX Total", f"='{assumptions_sheet}'!$D$53", "low", 53),
        ("c_high", "CAPEX Total - Alto (+15%)" if lang == 'ES' else "Total CAPEX - High (+15%)", "CAPEX Total", f"='{assumptions_sheet}'!$E$53", "high", 53),
        ("op_low", "OPEX Fijo Anual - Bajo (-70k€)" if lang == 'ES' else "Fixed OPEX - Low (-$70k)", "OPEX Fijo", f"='{assumptions_sheet}'!$D$54", "low", 54),
        ("op_high", "OPEX Fijo Anual - Alto (+70k€)" if lang == 'ES' else "Fixed OPEX - High (+$70k)", "OPEX Fijo", f"='{assumptions_sheet}'!$E$54", "high", 54),
        ("gv_low", "Crecimiento Volumen - Bajo (2%)" if lang == 'ES' else "Volume Growth - Low (2%)", "Crecimiento Volumen", f"='{assumptions_sheet}'!$D$55", "low", 55),
        ("gv_high", "Crecimiento Volumen - Alto (8%)" if lang == 'ES' else "Volume Growth - High (8%)", "Crecimiento Volumen", f"='{assumptions_sheet}'!$E$55", "high", 55),
        ("w_low", "WACC % - Bajo (7,5%)" if lang == 'ES' else "WACC % - Low (7.5%)", "WACC %", f"='{assumptions_sheet}'!$D$56", "low", 56),
        ("w_high", "WACC % - Alto (11,5%)" if lang == 'ES' else "WACC % - High (11.5%)", "WACC %", f"='{assumptions_sheet}'!$E$56", "high", 56),
        ("nwc_low", "Capital Circulante % - Bajo (7%)" if lang == 'ES' else "Working Capital % - Low (7%)", "Capital Circulante %", f"='{assumptions_sheet}'!$D$57", "low", 57),
        ("nwc_high", "Capital Circulante % - Alto (13%)" if lang == 'ES' else "Working Capital % - High (13%)", "Capital Circulante %", f"='{assumptions_sheet}'!$E$57", "high", 57),
    ]

    for idx, (cid, label, dname, val_ref, mode, prow) in enumerate(recalc_cases, start=8):
        ws[f"B{idx}"].value = label
        ws[f"C{idx}"].value = dname
        ws[f"D{idx}"].value = val_ref

        dtype = (
            "var_cost" if cid.startswith("vc_") else
            "price" if cid.startswith("p_") else
            "volume" if cid.startswith("v_") else
            "capex" if cid.startswith("c_") else
            "opex" if cid.startswith("op_") else
            "g_vol" if cid.startswith("gv_") else
            "wacc" if cid.startswith("w_") else
            "nwc" if cid.startswith("nwc_") else
            ""
        )

        # Fórmulas de FCF parametrizadas para cada caso:
        # FCF0 (Columna E)
        if dtype == "capex":
            ws[f"E{idx}"].value = f"=-(D{idx} * (850000/1200000))"
        else:
            ws[f"E{idx}"].value = f"='{assumptions_sheet}'!$D$41 * -1"

        # FCF1 (Columna F)
        f_vol1 = f"D{idx}" if dtype == "volume" else f"'{assumptions_sheet}'!$D$34"
        f_p1 = f"D{idx}" if dtype == "price" else f"'{assumptions_sheet}'!$D$36"
        f_vc1 = f"D{idx}" if dtype == "var_cost" else f"'{assumptions_sheet}'!$D$38"
        f_op1 = f"D{idx}" if dtype == "opex" else f"'{assumptions_sheet}'!$D$39"
        f_c1_y0 = f"D{idx} * (850000/1200000)" if dtype == "capex" else f"'{assumptions_sheet}'!$D$41"
        f_c1_y1 = f"D{idx} * (350000/1200000)" if dtype == "capex" else f"'{assumptions_sheet}'!$D$42"
        f_nwc1 = f"D{idx}" if dtype == "nwc" else f"'{assumptions_sheet}'!$D$43"

        # FCF1 fórmula compacta exacta:
        # NOPAT1 = (Rev1*(1-vc) - op1 - c1_y0/5) * 0.75
        # FCF1 = NOPAT1 + c1_y0/5 - c1_y1 - Rev1*nwc
        ws[f"F{idx}"].value = (
            f"=(({f_vol1}*{f_p1})*(1-{f_vc1}) - {f_op1} - ({f_c1_y0})/5) * (1-'{assumptions_sheet}'!$C$11) "
            f"+ ({f_c1_y0})/5 - ({f_c1_y1}) - ({f_vol1}*{f_p1})*{f_nwc1}"
        )

        # FCF2 a 5 (Columnas G, H, I, J)
        f_gvol = f"D{idx}" if dtype == "g_vol" else f"'{assumptions_sheet}'!$D$35"
        f_ctot = f"D{idx}" if dtype == "capex" else f"('{assumptions_sheet}'!$D$41+'{assumptions_sheet}'!$D$42)"

        for t_idx, col_l in enumerate(["G", "H", "I", "J"], start=2):
            pow_t_prev = t_idx - 2
            pow_t = t_idx - 1
            rev_prev_expr = f"({f_vol1}*(1+{f_gvol})^{pow_t_prev}) * ({f_p1}*(1+'{assumptions_sheet}'!$D$37)^{pow_t_prev})" if pow_t_prev > 0 else f"({f_vol1}*{f_p1})"
            rev_t_expr = f"({f_vol1}*(1+{f_gvol})^{pow_t}) * ({f_p1}*(1+'{assumptions_sheet}'!$D$37)^{pow_t})"
            op_t_expr = f"{f_op1}*(1+'{assumptions_sheet}'!$D$40)^{pow_t}"

            ws[f"{col_l}{idx}"].value = (
                f"=(({rev_t_expr})*(1-{f_vc1}) - {op_t_expr} - ({f_ctot})/5) * (1-'{assumptions_sheet}'!$C$11) "
                f"+ ({f_ctot})/5 - ({rev_t_expr} - {rev_prev_expr})*{f_nwc1}"
            )

        # WACC Fila (Columna K)
        if dtype == "wacc":
            ws[f"K{idx}"].value = f"=D{idx}"
        else:
            ws[f"K{idx}"].value = f"='{assumptions_sheet}'!$C$28"

        # VAN 5 Años (Columna L)
        ws[f"L{idx}"].value = f"=E{idx} + NPV(K{idx}, F{idx}:J{idx})"

        # Δ vs. Base (Columna M)
        ws[f"M{idx}"].value = f"=L{idx} - $L$7"

        # Estado (Columna N)
        ws[f"N{idx}"].value = f'=IF(L{idx}>0, "{"✅ Rentable" if lang == "ES" else "✅ Profitable"}", "{"⛔ Destruye valor" if lang == "ES" else "⛔ Destroys value"}")'

    # Estilos del bloque de recálculo (Filas 7 a 23)
    for r in range(7, 24):
        ws[f"B{r}"].font = Font(name=FONT_NAME, size=9, bold=(r == 7))
        ws[f"B{r}"].border = borders['thin']
        ws[f"C{r}"].font = Font(name=FONT_NAME, size=9)
        ws[f"C{r}"].border = borders['thin']
        ws[f"D{r}"].font = Font(name=FONT_NAME, size=9, bold=True)
        ws[f"D{r}"].border = borders['thin']
        ws[f"D{r}"].alignment = Alignment(horizontal="right", vertical="center")

        for c_idx in range(5, 11):
            coord = f"{get_column_letter(c_idx)}{r}"
            cell = ws[coord]
            cell.font = Font(name=FONT_NAME, size=9)
            cell.border = borders['thin']
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = fmt_curr

        # WACC K
        ws[f"K{r}"].font = Font(name=FONT_NAME, size=9)
        ws[f"K{r}"].number_format = fmt_pct
        ws[f"K{r}"].border = borders['thin']
        ws[f"K{r}"].alignment = Alignment(horizontal="right", vertical="center")

        # VAN L
        ws[f"L{r}"].font = Font(name=FONT_NAME, size=9, bold=True, color=COLOR_BLUE_ACCENT if r == 7 else "000000")
        ws[f"L{r}"].number_format = fmt_curr
        ws[f"L{r}"].border = borders['highlight'] if r == 7 else borders['thin']
        ws[f"L{r}"].alignment = Alignment(horizontal="right", vertical="center")

        # Delta M
        ws[f"M{r}"].font = Font(name=FONT_NAME, size=9, bold=True)
        ws[f"M{r}"].number_format = fmt_curr
        ws[f"M{r}"].border = borders['thin']
        ws[f"M{r}"].alignment = Alignment(horizontal="right", vertical="center")

        # Estado N
        ws[f"N{r}"].font = Font(name=FONT_NAME, size=9)
        ws[f"N{r}"].border = borders['thin']
        ws[f"N{r}"].alignment = Alignment(horizontal="center", vertical="center")

    # 3. TABLA TORNADO ESTRUCTURADA (Filas 26 a 34)
    s2_title = "2. TABLA RESUMEN DE SENSIBILIDAD POR DRIVER (AMPLITUD / SWING)" if lang == 'ES' else "2. SENSITIVITY SUMMARY TABLE BY DRIVER (SWING ANALYSIS)"
    ws["B25"].value = s2_title
    ws["B25"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B25")

    h_torn_tab = [
        "Driver de Sensibilidad",
        "Valor Bajo",
        "Valor Alto",
        "VAN Caso Bajo",
        "VAN Caso Alto",
        "Δ Caso Bajo",
        "Δ Caso Alto",
        "Amplitud (Swing)",
        "Ranking Amplitud",
    ] if lang == 'ES' else [
        "Sensitivity Driver",
        "Low Value",
        "High Value",
        "NPV Low Case",
        "NPV High Case",
        "Δ Low Case",
        "Δ High Case",
        "Swing (|High - Low|)",
        "Swing Ranking",
    ]
    for c_idx, h_text in enumerate(h_torn_tab, start=2):
        coord = f"{get_column_letter(c_idx)}26"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx >= 3 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    # 8 Drivers mapeados a las filas del motor
    tornado_summary_mapping = [
        # (Label, Low_Row, High_Row, Param_row)
        ("Precio Unitario (€/u)" if lang == 'ES' else "Unit Price ($/unit)", 8, 9, 50),
        ("Volumen Comercializado Año 1" if lang == 'ES' else "Year 1 Sales Volume", 10, 11, 51),
        ("Coste Variable sobre ventas (%)" if lang == 'ES' else "Variable Cost of Sales (%)", 12, 13, 52),
        ("CAPEX Total (Tramo 1+2)" if lang == 'ES' else "Total CAPEX (Tranche 1+2)", 14, 15, 53),
        ("OPEX Fijo Anual (€)" if lang == 'ES' else "Annual Fixed OPEX ($)", 16, 17, 54),
        ("Crecimiento Anual del Volumen (%)" if lang == 'ES' else "Volume Growth Rate (%)", 18, 19, 55),
        ("Tasa de Descuento (WACC %)" if lang == 'ES' else "Discount Rate (WACC %)", 20, 21, 56),
        ("Capital Circulante sobre ventas (%)" if lang == 'ES' else "Working Capital to Sales (%)", 22, 23, 57),
    ]

    for idx, (label, r_low, r_high, p_row) in enumerate(tornado_summary_mapping, start=27):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = f"='{assumptions_sheet}'!$D${p_row}"
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"C{idx}"].border = borders['thin']
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"D{idx}"].value = f"='{assumptions_sheet}'!$E${p_row}"
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"D{idx}"].border = borders['thin']
        ws[f"D{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"E{idx}"].value = f"=L{r_low}"
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"E{idx}"].number_format = fmt_curr
        ws[f"E{idx}"].border = borders['thin']
        ws[f"E{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"F{idx}"].value = f"=L{r_high}"
        ws[f"F{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"F{idx}"].number_format = fmt_curr
        ws[f"F{idx}"].border = borders['thin']
        ws[f"F{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"G{idx}"].value = f"=E{idx} - $L$7"
        ws[f"G{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"G{idx}"].number_format = fmt_curr
        ws[f"G{idx}"].border = borders['thin']
        ws[f"G{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"H{idx}"].value = f"=F{idx} - $L$7"
        ws[f"H{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"H{idx}"].number_format = fmt_curr
        ws[f"H{idx}"].border = borders['thin']
        ws[f"H{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"I{idx}"].value = f"=ABS(F{idx} - E{idx})"
        ws[f"I{idx}"].font = Font(name=FONT_NAME, size=9, bold=True)
        ws[f"I{idx}"].number_format = fmt_curr
        ws[f"I{idx}"].border = borders['thin']
        ws[f"I{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        # Ranking con desempate determinista ROW()/10^9
        ws[f"J{idx}"].value = f"=RANK(I{idx}, $I$27:$I$34) + ROW()/1000000000"
        ws[f"J{idx}"].font = Font(name=FONT_NAME, size=8, color="64748B")
        ws[f"J{idx}"].number_format = '0.0000'
        ws[f"J{idx}"].border = borders['thin']
        ws[f"J{idx}"].alignment = Alignment(horizontal="center", vertical="center")

    # 4. TABLA TORNADO ORDENADA (Para alimentación del Gráfico) (Filas 37 a 45)
    s3_title = "3. TABLA ORDENADA DE MAYOR A MENOR SENSIBILIDAD (ALIMENTA GRÁFICO TORNADO)" if lang == 'ES' else "3. RANKED SENSITIVITY TABLE (POWERS NATIVE TORNADO CHART)"
    ws["B36"].value = s3_title
    ws["B36"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B36")

    h_ord_tab = [
        "Ranking",
        "Driver Ordenado por Amplitud",
        "Amplitud (Swing)",
        "Impacto Negativo (Rojo)",
        "Impacto Positivo (Verde)",
    ] if lang == 'ES' else [
        "Rank",
        "Ranked Driver by Swing",
        "Swing (|High - Low|)",
        "Negative Impact (Red)",
        "Positive Impact (Green)",
    ]
    for c_idx, h_text in enumerate(h_ord_tab, start=2):
        coord = f"{get_column_letter(c_idx)}37"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx != 3 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    for rank_k in range(1, 9):
        r_ord = 37 + rank_k
        ws[f"B{r_ord}"].value = rank_k
        ws[f"B{r_ord}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"B{r_ord}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"B{r_ord}"].border = borders['thin']

        # Driver name vía INDEX/MATCH sobre LARGE
        ws[f"C{r_ord}"].value = f"=INDEX($B$27:$B$34, MATCH(SMALL($J$27:$J$34, B{r_ord}), $J$27:$J$34, 0))"
        ws[f"C{r_ord}"].font = Font(name=FONT_NAME, size=9, bold=True)
        ws[f"C{r_ord}"].border = borders['thin']

        # Swing vía LARGE
        ws[f"D{r_ord}"].value = f"=INDEX($I$27:$I$34, MATCH(SMALL($J$27:$J$34, B{r_ord}), $J$27:$J$34, 0))"
        ws[f"D{r_ord}"].font = Font(name=FONT_NAME, size=9, bold=True)
        ws[f"D{r_ord}"].number_format = fmt_curr
        ws[f"D{r_ord}"].border = borders['thin']
        ws[f"D{r_ord}"].alignment = Alignment(horizontal="right", vertical="center")

        # Impacto Negativo (mínimo de las dos deltas)
        ws[f"E{r_ord}"].value = f"=MIN(INDEX($G$27:$G$34, MATCH(SMALL($J$27:$J$34, B{r_ord}), $J$27:$J$34, 0)), INDEX($H$27:$H$34, MATCH(SMALL($J$27:$J$34, B{r_ord}), $J$27:$J$34, 0)))"
        ws[f"E{r_ord}"].font = Font(name=FONT_NAME, size=9, color=COLOR_RED_TEXT)
        ws[f"E{r_ord}"].number_format = fmt_curr
        ws[f"E{r_ord}"].border = borders['thin']
        ws[f"E{r_ord}"].alignment = Alignment(horizontal="right", vertical="center")

        # Impacto Positivo (máximo de las dos deltas)
        ws[f"F{r_ord}"].value = f"=MAX(INDEX($G$27:$G$34, MATCH(SMALL($J$27:$J$34, B{r_ord}), $J$27:$J$34, 0)), INDEX($H$27:$H$34, MATCH(SMALL($J$27:$J$34, B{r_ord}), $J$27:$J$34, 0)))"
        ws[f"F{r_ord}"].font = Font(name=FONT_NAME, size=9, color=COLOR_GREEN_TEXT)
        ws[f"F{r_ord}"].number_format = fmt_curr
        ws[f"F{r_ord}"].border = borders['thin']
        ws[f"F{r_ord}"].alignment = Alignment(horizontal="right", vertical="center")

    # Gráfico Tornado Nativo en Pestaña 4
    chart_tornado = BarChart()
    chart_tornado.type = "bar"
    chart_tornado.grouping = "clustered"
    chart_tornado.overlap = 100
    chart_tornado.title = "ANÁLISIS DE SENSIBILIDAD TORNADO: IMPACTO EN VAN (€)" if lang == 'ES' else "TORNADO SENSITIVITY ANALYSIS: IMPACT ON NPV ($)"
    chart_tornado.style = 10
    chart_tornado.width = 24
    chart_tornado.height = 14

    data_tornado = Reference(ws, min_col=5, min_row=37, max_col=6, max_row=45)
    cats_tornado = Reference(ws, min_col=3, min_row=38, max_row=45)
    chart_tornado.add_data(data_tornado, titles_from_data=True)

    # Inyección de categorías con caché explícito para renderizado universal en Excel
    sorted_driver_names = [r["name_es"] if lang == 'ES' else r["name_en"] for r in model_core.TORNADO_RESULTS]
    str_cache = StrData(pt=[StrVal(idx=i, v=d) for i, d in enumerate(sorted_driver_names)])
    str_ref = StrRef(f=str(cats_tornado), strCache=str_cache)
    for s in chart_tornado.series:
        s.cat = AxDataSource(strRef=str_ref)
        s.invertIfNegative = False

    if len(chart_tornado.series) >= 2:
        chart_tornado.series[0].graphicalProperties.solidFill = COLOR_RED_BORDER    # Impacto negativo
        chart_tornado.series[1].graphicalProperties.solidFill = COLOR_GREEN_BORDER  # Impacto positivo

    # Configuración de ejes para garantizar visualización perfecta de etiquetas y números
    chart_tornado.x_axis.delete = False
    chart_tornado.x_axis.scaling.orientation = "maxMin"   # Mayor swing en la parte superior
    chart_tornado.x_axis.axPos = "l"
    chart_tornado.x_axis.tickLblPos = "low"                # Etiquetas de drivers legibles a la izquierda
    chart_tornado.x_axis.crosses = "autoZero"              # Cruce simétrico en cero

    chart_tornado.y_axis.delete = False
    chart_tornado.y_axis.scaling.orientation = "minMax"
    chart_tornado.y_axis.axPos = "b"
    chart_tornado.y_axis.tickLblPos = "high"               # Escala numérica situada en la base del gráfico
    chart_tornado.y_axis.crosses = "autoZero"
    chart_tornado.y_axis.number_format = '#,##0 €' if lang == 'ES' else '$#,##0'
    chart_tornado.legend.position = "r"                    # Leyenda en el lateral derecho para evitar colisiones

    ws.add_chart(chart_tornado, "H36")

    # 5. BLOQUE DE ESCENARIOS Y VAN ESPERADO (Filas 48 a 54)
    s4_title = "4. ESCENARIOS PROBABILÍSTICOS Y VALOR ACTUAL NETO ESPERADO (E[VAN])" if lang == 'ES' else "4. PROBABILISTIC SCENARIOS AND EXPECTED NET PRESENT VALUE (E[NPV])"
    ws["B48"].value = s4_title
    ws["B48"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B48")

    h_scen_res = [
        "Escenario",
        "Probabilidad (p)",
        "VAN a 5 Años",
        "Ponderación (p·VAN)",
        "TIR Proyectada",
        "Payback Descontado",
    ] if lang == 'ES' else [
        "Scenario",
        "Probability (p)",
        "NPV 5-Year",
        "Weighted Term (p·NPV)",
        "Projected IRR",
        "Discounted Payback",
    ]
    for c_idx, h_text in enumerate(h_scen_res, start=2):
        coord = f"{get_column_letter(c_idx)}49"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx >= 3 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    # Pesimista
    ws["B50"].value = "Pesimista (Downside)" if lang == 'ES' else "Pessimistic (Downside)"
    ws["C50"].value = f"='{assumptions_sheet}'!$C$33"
    ws["C50"].number_format = fmt_pct
    ws["D50"].value = round(model_core.PROJ_PES["npv_5y"], 2)
    ws["D50"].number_format = fmt_curr
    ws["E50"].value = "=C50*D50"
    ws["E50"].number_format = fmt_curr
    ws["F50"].value = round(model_core.PROJ_PES["irr"], 4) if model_core.PROJ_PES["irr"] else 0.0
    ws["F50"].number_format = fmt_pct
    ws["G50"].value = "> 5 años" if lang == 'ES' else "> 5 yrs"

    # Base
    ws["B51"].value = "Base (Caso Central)" if lang == 'ES' else "Base (Central Case)"
    ws["C51"].value = f"='{assumptions_sheet}'!$D$33"
    ws["C51"].number_format = fmt_pct
    ws["D51"].value = "=$L$7"
    ws["D51"].number_format = fmt_curr
    ws["E51"].value = "=C51*D51"
    ws["E51"].number_format = fmt_curr
    ws["F51"].value = f"='{dcf_sheet}'!$C$35"
    ws["F51"].number_format = fmt_pct
    ws["G51"].value = f"='{dcf_sheet}'!$C$38"

    # Optimista
    ws["B52"].value = "Optimista (Upside)" if lang == 'ES' else "Optimistic (Upside)"
    ws["C52"].value = f"='{assumptions_sheet}'!$E$33"
    ws["C52"].number_format = fmt_pct
    ws["D52"].value = round(model_core.PROJ_OPT["npv_5y"], 2)
    ws["D52"].number_format = fmt_curr
    ws["E52"].value = "=C52*D52"
    ws["E52"].number_format = fmt_curr
    ws["F52"].value = round(model_core.PROJ_OPT["irr"], 4) if model_core.PROJ_OPT["irr"] else 0.0
    ws["F52"].number_format = fmt_pct
    ws["G52"].value = f"{model_core.PROJ_OPT['payback_discounted']:.2f} años" if lang == 'ES' else f"{model_core.PROJ_OPT['payback_discounted']:.2f} yrs"

    for r in [50, 51, 52]:
        for c in range(2, 8):
            coord = f"{get_column_letter(c)}{r}"
            ws[coord].font = Font(name=FONT_NAME, size=9)
            ws[coord].border = borders['thin']
            if c >= 3:
                ws[coord].alignment = Alignment(horizontal="right", vertical="center")

    # Fila 53: VAN Esperado Ponderado
    ws["B53"].value = "VALOR ACTUAL NETO ESPERADO (E[VAN] PONDERADO)" if lang == 'ES' else "EXPECTED NET PRESENT VALUE (WEIGHTED E[NPV])"
    ws["B53"].font = Font(name=FONT_NAME, size=10, bold=True)
    ws["B53"].border = borders['total']
    ws["C53"].value = "=SUM(C50:C52)"
    ws["C53"].font = Font(name=FONT_NAME, size=10, bold=True)
    ws["C53"].number_format = fmt_pct
    ws["C53"].alignment = Alignment(horizontal="right", vertical="center")
    ws["C53"].border = borders['total']
    ws["D53"].value = "=SUM(E50:E52)"
    ws["D53"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["D53"].number_format = fmt_curr
    ws["D53"].alignment = Alignment(horizontal="right", vertical="center")
    ws["D53"].border = borders['highlight']
    ws["E53"].value = "=D53"
    ws["E53"].font = Font(name=FONT_NAME, size=10, bold=True)
    ws["E53"].number_format = fmt_curr
    ws["E53"].alignment = Alignment(horizontal="right", vertical="center")
    ws["E53"].border = borders['total']
    ws["F53"].value = "-"
    ws["F53"].alignment = Alignment(horizontal="center")
    ws["F53"].border = borders['total']
    ws["G53"].value = "-"
    ws["G53"].alignment = Alignment(horizontal="center")
    ws["G53"].border = borders['total']

    # 6. PUNTOS DE EQUILIBRIO (BREAK-EVEN POINTS: VAN = 0) (Filas 56 a 61)
    s5_title = "5. PUNTOS DE EQUILIBRIO LINEALES (BREAK-EVEN POINTS: UMBRALES DE VAN = 0)" if lang == 'ES' else "5. LINEAR BREAK-EVEN POINTS (THRESHOLDS WHERE NPV = 0)"
    ws["B56"].value = s5_title
    ws["B56"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B56")

    h_be = [
        "Variable Clave Evaluada",
        "Valor Base",
        "Punto de Equilibrio (VAN = 0)",
        "Variación Máxima Admisible",
        "Margen de Seguridad / Diagnóstico",
    ] if lang == 'ES' else [
        "Key Variable Evaluated",
        "Base Value",
        "Break-Even Point (NPV = 0)",
        "Maximum Allowable Variance",
        "Safety Margin / Diagnostic",
    ]
    for c_idx, h_text in enumerate(h_be, start=2):
        coord = f"{get_column_letter(c_idx)}57"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx >= 3 else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    be_data = [
        ("Precio Unitario (€/u)" if lang == 'ES' else "Unit Price ($/unit)", f"='{assumptions_sheet}'!$D$36", model_core.SUMMARY['break_even']['price']['value'], fmt_curr, f"{model_core.SUMMARY['break_even']['price']['drop_pct']*100:.1f}%", "Soporta una caída del precio del 23,2% antes de destruir valor" if lang == 'ES' else "Can tolerate up to -23.2% price decline before destroying value"),
        ("Volumen Comercializado Año 1" if lang == 'ES' else "Year 1 Sales Volume", f"='{assumptions_sheet}'!$D$34", model_core.SUMMARY['break_even']['volume']['value'], '#,##0', f"{model_core.SUMMARY['break_even']['volume']['drop_pct']*100:.1f}%", "Soporta una pérdida de demanda del 23,2% sobre el plan comercial" if lang == 'ES' else "Can absorb up to -23.2% sales volume loss versus target"),
        ("CAPEX Total Inicial (€)" if lang == 'ES' else "Total Initial CAPEX ($)", f"='{assumptions_sheet}'!$D$41+'{assumptions_sheet}'!$D$42", model_core.SUMMARY['break_even']['capex']['value'], fmt_curr, f"+{model_core.SUMMARY['break_even']['capex']['increase_pct']*100:.1f}%", "Soporta un sobrecoste de ingeniería de hasta +72,5% (hasta 2,07 M€)" if lang == 'ES' else "Can withstand engineering overruns up to +72.5% (up to $2.07M)"),
    ]

    for idx, (label, f_base, be_val, fmt, var_str, diag_txt) in enumerate(be_data, start=58):
        ws[f"B{idx}"].value = label
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=9, bold=True)
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = f_base
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"C{idx}"].number_format = fmt
        ws[f"C{idx}"].border = borders['thin']
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"D{idx}"].value = be_val
        ws[f"D{idx}"].font = Font(name=FONT_NAME, size=9, bold=True, color=COLOR_BLUE_ACCENT)
        ws[f"D{idx}"].number_format = fmt
        ws[f"D{idx}"].border = borders['thin']
        ws[f"D{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"E{idx}"].value = var_str
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=9, bold=True, color=COLOR_AMBER_TEXT)
        ws[f"E{idx}"].border = borders['thin']
        ws[f"E{idx}"].alignment = Alignment(horizontal="center", vertical="center")

        ws[f"F{idx}"].value = diag_txt
        ws[f"F{idx}"].font = Font(name=FONT_NAME, size=9, italic=True)
        ws[f"F{idx}"].border = borders['thin']

    # Anchos de columna
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 38
    ws.column_dimensions["C"].width = 36
    ws.column_dimensions["D"].width = 22
    ws.column_dimensions["E"].width = 26
    ws.column_dimensions["F"].width = 26
    ws.column_dimensions["G"].width = 18
    ws.column_dimensions["H"].width = 18
    ws.column_dimensions["I"].width = 18
    ws.column_dimensions["J"].width = 16
    ws.column_dimensions["K"].width = 14
    ws.column_dimensions["L"].width = 18
    ws.column_dimensions["M"].width = 16
    ws.column_dimensions["N"].width = 20

    finalize_sheet(ws, decorative_cells=frozenset(decorative))


def build_tab1_dashboard(wb, lang='ES'):
    """Construye la Pestaña 1: Dashboard Ejecutivo / Executive Dashboard."""
    sheet_title = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    dcf_sheet = "Proyección DCF" if lang == 'ES' else "DCF Projection"
    assumptions_sheet = "Supuestos & Drivers" if lang == 'ES' else "Assumptions & Drivers"
    sens_sheet = "Sensibilidad & Tornado" if lang == 'ES' else "Sensitivity & Tornado"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    fmt_curr = '#,##0 "€";[Red]-#,##0 "€"' if lang == 'ES' else '"$"#,##0;[Red]("$"#,##0)'
    fmt_pct = '0.0%'

    # 1. Cabecera Principal
    h_title = (
        "DASHBOARD EJECUTIVO: BUSINESS CASE FINANCIERO & DICTAMEN DE INVERSIÓN (C-LEVEL)"
        if lang == 'ES' else
        "EXECUTIVE DASHBOARD: FINANCIAL BUSINESS CASE & INVESTMENT VERDICT (C-LEVEL)"
    )
    style_merged_header(ws, "B2:M3", h_title, decorative, COLOR_NAVY_DARK, "FFFFFF", 13)
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 20

    # Metadatos del Proyecto (Filas 4 y 5)
    meta_items = [
        ("B4", "Proyecto:" if lang == 'ES' else "Project:", "C4:E4", "Automatización y Digitalización de Línea de Producción" if lang == 'ES' else "Production Line Automation & Digitalization"),
        ("F4", "Sponsor C-Level:", "G4:H4", "COO & VP Industrial Operations"),
        ("I4", "Fecha:" if lang == 'ES' else "Date:", "J4:K4", "=TODAY()"),
        ("B5", "Unidad de Negocio:" if lang == 'ES' else "Business Unit:", "C5:E5", "División Industrial Manufactura" if lang == 'ES' else "Industrial Manufacturing Division"),
        ("F5", "Escenario Activo:" if lang == 'ES' else "Active Scenario:", "G5:H5", f"='{assumptions_sheet}'!$G$32"),
        ("I5", "WACC Descuento:" if lang == 'ES' else "Discount WACC:", "J5:K5", f"='{assumptions_sheet}'!$C$28"),
    ]

    for lbl_c, lbl_t, rng, val in meta_items:
        ws[lbl_c].value = lbl_t
        ws[lbl_c].font = Font(name=FONT_NAME, size=9, bold=True, color="64748B")
        decorative.add(lbl_c)

        if ":" in rng:
            ws.merge_cells(rng)
            c_first = rng.split(":")[0]
            ws[c_first].value = val
            ws[c_first].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
            if lbl_c == "I4":
                ws[c_first].number_format = 'yyyy-mm-dd'
            elif lbl_c == "I5":
                ws[c_first].number_format = fmt_pct
            start_col, start_row, end_col, end_row = openpyxl.utils.range_boundaries(rng)
            for r in range(start_row, end_row + 1):
                for c in range(start_col, end_col + 1):
                    decorative.add(f"{get_column_letter(c)}{r}")

    # 2. BANNER DE DICTAMEN DE INVERSIÓN (Filas 7 a 9)
    ws.merge_cells("B7:M7")
    ws["B7"].value = "DICTAMEN VINCULANTE DEL COMITÉ DE INVERSIONES (HURDLE POLICY GATEWAY)" if lang == 'ES' else "BINDING INVESTMENT COMMITTEE VERDICT (HURDLE POLICY GATEWAY)"
    ws["B7"].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    ws["B7"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["B7"].alignment = Alignment(horizontal="center", vertical="center")
    decorative.add("B7")
    for c in range(2, 14):
        decorative.add(f"{get_column_letter(c)}7")

    # Fórmula del Semáforo en B8:D9
    ws.merge_cells("B8:D9")
    app_word = "✅ APROBAR" if lang == 'ES' else "✅ APPROVE"
    rev_word = "🟠 REVISAR" if lang == 'ES' else "🟠 REVIEW"
    rej_word = "⛔ RECHAZAR" if lang == 'ES' else "⛔ REJECT"
    ws["B8"].value = (
        f'=IF(AND(\'{dcf_sheet}\'!$C$33>0, \'{dcf_sheet}\'!$C$35>=\'{assumptions_sheet}\'!$C$28+\'{assumptions_sheet}\'!$C$7, '
        f'\'{dcf_sheet}\'!$C$38<=\'{assumptions_sheet}\'!$C$8), "{app_word}", '
        f'IF(\'{dcf_sheet}\'!$C$33>0, "{rev_word}", "{rej_word}"))'
    )
    ws["B8"].font = Font(name=FONT_NAME, size=16, bold=True, color=COLOR_NAVY_DARK)
    ws["B8"].alignment = Alignment(horizontal="center", vertical="center")
    ws["B8"].border = borders['highlight']
    for r in range(8, 10):
        for c in range(2, 5):
            decorative.add(f"{get_column_letter(c)}{r}")

    # Texto Explicativo en E8:M9
    ws.merge_cells("E8:M9")
    diag_app = (
        "El proyecto supera el WACC exigido (+3 pp de margen), genera VAN positivo (+693 k€), recupera la inversión en 3,35 años (< 4 años máximo) y resiste caídas de demanda de hasta el 23,2%."
        if lang == 'ES' else
        "The project exceeds required hurdle rate (+3 pp spread), yields positive NPV (+$693k), achieves discounted payback in 3.35 yrs (< 4.0 yrs limit) and tolerates up to -23.2% demand drop."
    )
    diag_rev = (
        "El proyecto genera VAN positivo pero incumple el umbral de rentabilidad exigido a la TIR o supera el periodo máximo admisible de payback descontado. Requiere optimización previa de CAPEX."
        if lang == 'ES' else
        "The project yields positive NPV but breaches hurdle rate requirements or exceeds maximum discounted payback limit. Requires CAPEX scope optimization."
    )
    diag_rej = (
        "El proyecto destruye valor económico neto (VAN <= 0) bajo las condiciones proyectadas. Dictamen vinculante: RECHAZAR la asignación de capital."
        if lang == 'ES' else
        "The project destroys net shareholder value (NPV <= 0) under projected parameters. Binding verdict: REJECT capital allocation request."
    )
    ws["E8"].value = f'=IF(B8="{app_word}", "{diag_app}", IF(B8="{rev_word}", "{diag_rev}", "{diag_rej}"))'
    ws["E8"].font = Font(name=FONT_NAME, size=10, bold=False, color="334155")
    ws["E8"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws["E8"].border = borders['card']
    for r in range(8, 10):
        for c in range(5, 14):
            decorative.add(f"{get_column_letter(c)}{r}")

    # 3. DIEZ TARJETAS KPI EJECUTIVAS (Filas 11 a 15)
    # Fila 1: 5 Tarjetas (Filas 11-12)
    # Fila 2: 5 Tarjetas (Filas 14-15)
    kpis_config = [
        # (Row, Col_range, Label, Formula, Format, Color)
        (11, "B11:C12", "VAN (5 Años)" if lang == 'ES' else "NPV (5-Year)", f"='{dcf_sheet}'!$C$33", fmt_curr, COLOR_BLUE_ACCENT),
        (11, "D11:E12", "TIR vs. WACC" if lang == 'ES' else "IRR vs. WACC", f"='{dcf_sheet}'!$C$35", fmt_pct, COLOR_GREEN_TEXT),
        (11, "F11:G12", "Payback Descontado" if lang == 'ES' else "Discounted Payback", f"='{dcf_sheet}'!$C$38", '0.00 "a"' if lang == 'ES' else '0.00 "y"', COLOR_NAVY_DARK),
        (11, "H11:I12", "Índice Rentabilidad (PI)" if lang == 'ES' else "Profitability Index (PI)", f"='{dcf_sheet}'!$C$39", '0.00"x"', COLOR_NAVY_DARK),
        (11, "J11:M12", "Peak Funding (Máx. Caja)" if lang == 'ES' else "Peak Funding Exposure", f"='{dcf_sheet}'!$C$40", fmt_curr, COLOR_RED_TEXT),
        
        (14, "B14:C15", "VAN (3 Años)" if lang == 'ES' else "NPV (3-Year)", f"='{dcf_sheet}'!$C$34", fmt_curr, COLOR_NAVY_MED),
        (14, "D14:E15", "TIR Modificada (MIRR)" if lang == 'ES' else "Modified IRR (MIRR)", f"='{dcf_sheet}'!$C$36", fmt_pct, COLOR_NAVY_DARK),
        (14, "F14:G15", "Payback Simple" if lang == 'ES' else "Simple Payback", f"='{dcf_sheet}'!$C$37", '0.00 "a"' if lang == 'ES' else '0.00 "y"', COLOR_NAVY_MED),
        (14, "H14:I15", "Tasa de Descuento (WACC)" if lang == 'ES' else "Discount Rate (WACC)", f"='{assumptions_sheet}'!$C$28", fmt_pct, COLOR_NAVY_DARK),
        (14, "J14:M15", "VAN Esperado (Ponderado)" if lang == 'ES' else "Expected NPV (Weighted)", f"='{sens_sheet}'!$D$53", fmt_curr, COLOR_BLUE_ACCENT),
    ]

    for r_top, rng, label, formula_val, fmt, color_txt in kpis_config:
        ws.merge_cells(rng)
        first_coord = rng.split(":")[0]
        ws[first_coord].value = formula_val
        ws[first_coord].font = Font(name=FONT_NAME, size=15, bold=True, color=color_txt)
        ws[first_coord].number_format = fmt
        ws[first_coord].alignment = Alignment(horizontal="center", vertical="center")
        ws[first_coord].border = borders['card']

        # Fila de etiqueta encima o contextual
        lbl_coord = f"{first_coord[0]}{int(first_coord[1:]) - 1}"
        # Ponemos la etiqueta como comentario o en la celda
        start_col, start_row, end_col, end_row = openpyxl.utils.range_boundaries(rng)
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                decorative.add(f"{get_column_letter(c)}{r}")

    # Etiquetas de KPI encima de las tarjetas (centradas sobre las tarjetas fusionadas)
    labels_row1 = [
        ("B10:C10", "VAN (5 AÑOS)" if lang == 'ES' else "NPV (5-YEAR)"),
        ("D10:E10", "TIR vs. WACC" if lang == 'ES' else "IRR vs. WACC"),
        ("F10:G10", "PAYBACK DESC." if lang == 'ES' else "DISC. PAYBACK"),
        ("H10:I10", "ÍNDICE PI" if lang == 'ES' else "PI RATIO"),
        ("J10:M10", "PEAK FUNDING"),
    ]
    for rng_c, txt in labels_row1:
        ws.merge_cells(rng_c)
        coord = rng_c.split(":")[0]
        ws[coord].value = txt
        ws[coord].font = Font(name=FONT_NAME, size=8, bold=True, color="64748B")
        ws[coord].alignment = Alignment(horizontal="center", vertical="center")
        start_col, start_row, end_col, end_row = openpyxl.utils.range_boundaries(rng_c)
        for c in range(start_col, end_col + 1):
            decorative.add(f"{get_column_letter(c)}{start_row}")

    labels_row2 = [
        ("B13:C13", "VAN (3 AÑOS)" if lang == 'ES' else "NPV (3-YEAR)"),
        ("D13:E13", "MIRR / TIRM"),
        ("F13:G13", "PAYBACK SIMPLE"),
        ("H13:I13", "WACC"),
        ("J13:M13", "VAN ESPERADO E[VAN]" if lang == 'ES' else "EXPECTED E[NPV]"),
    ]
    for rng_c, txt in labels_row2:
        ws.merge_cells(rng_c)
        coord = rng_c.split(":")[0]
        ws[coord].value = txt
        ws[coord].font = Font(name=FONT_NAME, size=8, bold=True, color="64748B")
        ws[coord].alignment = Alignment(horizontal="center", vertical="center")
        start_col, start_row, end_col, end_row = openpyxl.utils.range_boundaries(rng_c)
        for c in range(start_col, end_col + 1):
            decorative.add(f"{get_column_letter(c)}{start_row}")

    # 4. GRÁFICOS NATIVOS EN PESTAÑA 1
    # Gráfico A: Curva J Acumulada (Nominal vs. Descontado)
    chart_j = LineChart()
    chart_j.title = "CURVA J: FLUJO DE CAJA ACUMULADO NOMINAL VS. DESCONTADO (€)" if lang == 'ES' else "J-CURVE: CUMULATIVE NOMINAL VS. DISCOUNTED CASH FLOW ($)"
    chart_j.style = 13
    chart_j.width = 16
    chart_j.height = 10
    chart_j.y_axis.title = "Flujo Acumulado (€)" if lang == 'ES' else "Cumulative Flow ($)"
    chart_j.x_axis.title = "Horizonte Temporal" if lang == 'ES' else "Time Horizon"

    # min_col=2 (columna B con títulos "Flujo acumulado nominal", etc.), min_row=25, max_col=9 (Año 5), max_row=26
    data_j = Reference(ws.parent[dcf_sheet], min_col=2, min_row=25, max_col=9, max_row=26)
    cats_j = Reference(ws.parent[dcf_sheet], min_col=4, min_row=5, max_col=9, max_row=5)
    chart_j.add_data(data_j, titles_from_data=True, from_rows=True)
    chart_j.set_categories(cats_j)

    if len(chart_j.series) >= 2:
        chart_j.series[0].graphicalProperties.line.solidFill = COLOR_BLUE_ACCENT
        chart_j.series[1].graphicalProperties.line.solidFill = COLOR_NAVY_DARK

    ws.add_chart(chart_j, "B17")

    # Gráfico B: VAN por Escenario (Columnas)
    chart_scen = BarChart()
    chart_scen.type = "col"
    chart_scen.title = "VALOR ACTUAL NETO POR ESCENARIO (€)" if lang == 'ES' else "NET PRESENT VALUE BY SCENARIO ($)"
    chart_scen.style = 10
    chart_scen.width = 14
    chart_scen.height = 10
    chart_scen.legend = None

    data_scen = Reference(ws.parent[sens_sheet], min_col=4, min_row=49, max_col=4, max_row=52)
    cats_scen = Reference(ws.parent[sens_sheet], min_col=2, min_row=50, max_col=2, max_row=52)
    chart_scen.add_data(data_scen, titles_from_data=True)
    chart_scen.set_categories(cats_scen)

    if len(chart_scen.series) >= 1:
        chart_scen.series[0].graphicalProperties.solidFill = COLOR_BLUE_ACCENT

    ws.add_chart(chart_scen, "H17")

    # Anchos de columna
    ws.column_dimensions["A"].width = 4
    for c_let in ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
        ws.column_dimensions[c_let].width = 16

    finalize_sheet(ws, decorative_cells=frozenset(decorative))


def build_tab5_governance(wb, lang='ES'):
    """Construye la Pestaña 5: Plan de Inversión & Gobernanza / Investment Plan & Governance."""
    sheet_title = "Plan de Inversión & Gobernanza" if lang == 'ES' else "Investment Plan & Governance"
    assumptions_sheet = "Supuestos & Drivers" if lang == 'ES' else "Assumptions & Drivers"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    fmt_curr = '#,##0 "€";[Red]-#,##0 "€"' if lang == 'ES' else '"$"#,##0;[Red]("$"#,##0)'

    # 1. Cabecera Principal
    h_title = (
        "PLAN DE FINANCIACIÓN POR TRAMOS, STAGE GATES, CRITERIOS DE CANCELACIÓN Y GOBERNANZA"
        if lang == 'ES' else
        "PHASED FINANCING PLAN, STAGE GATES, KILL CRITERIA AND BOARDROOM GOVERNANCE"
    )
    style_merged_header(ws, "B2:H3", h_title, decorative, COLOR_NAVY_DARK, "FFFFFF", 12)
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 20

    # 2. SECCIÓN 1: Calendario de Financiación por Tramos y Stage Gates
    s1_title = "1. CALENDARIO DE FINANCIACIÓN POR TRAMOS & HITOS DE LIBERACIÓN (STAGE GATES)" if lang == 'ES' else "1. PHASED FINANCING SCHEDULE & STAGE GATE RELEASE MILESTONES"
    ws["B5"].value = s1_title
    ws["B5"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B5")

    h_gates = [
        "Tramo de Financiación",
        "Importe Comprometido",
        "Trimestre / Plazo",
        "Alcance Técnico de la Fase",
        "KPI de Aceptación para Liberar Siguiente Tramo",
        "Umbral Mínimo Requerido",
        "Responsable de Validación",
    ] if lang == 'ES' else [
        "Financing Tranche",
        "Committed Capital",
        "Quarter / Timeline",
        "Technical Phase Scope",
        "Acceptance KPI to Release Next Tranche",
        "Minimum Required Threshold",
        "Validation Owner",
    ]
    for c_idx, h_text in enumerate(h_gates, start=2):
        coord = f"{get_column_letter(c_idx)}6"
        ws[coord].value = h_text
        ws[coord].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        ws[coord].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
        ws[coord].alignment = Alignment(horizontal="center" if c_idx in [3, 4, 7] else "left", vertical="center")
        ws[coord].border = borders['header']
        decorative.add(coord)

    tranches = [
        ("Tramo 1 (Desembolso Inicial)" if lang == 'ES' else "Tranche 1 (Initial Outlay)", f"='{assumptions_sheet}'!$D$41", "Q1 Año 0" if lang == 'ES' else "Q1 Year 0", "Ingeniería de detalle, obra civil y pedido maquinaria principal" if lang == 'ES' else "Detailed engineering, civil works & main robotics procurement", "Recepción y pruebas FAT (Factory Acceptance Test) en origen" if lang == 'ES' else "FAT (Factory Acceptance Test) passed at vendor facility", "Certificación técnica 100% sin no-conformidades críticas" if lang == 'ES' else "100% technical sign-off with zero critical non-conformities", "COO & Director Industrial" if lang == 'ES' else "COO & Industrial Director"),
        ("Tramo 2 (Automatización & MES)" if lang == 'ES' else "Tranche 2 (Automation & MES)", f"='{assumptions_sheet}'!$D$42", "Q4 Año 1" if lang == 'ES' else "Q4 Year 1", "Integración robótica en planta, software MES y puesta en marcha" if lang == 'ES' else "On-site robotic integration, MES software and plant commissioning", "Pruebas SAT en planta y Eficiencia Global de Equipos (OEE)" if lang == 'ES' else "Site SAT acceptance and Overall Equipment Effectiveness (OEE)", "OEE preliminar ≥ 75% y cadencia de línea validada" if lang == 'ES' else "Preliminary OEE ≥ 75% and line throughput validated", "VP Operaciones & Plant Manager" if lang == 'ES' else "VP Operations & Plant Manager"),
        ("Tramo 3 (Opcional - Expansión Fase 2)" if lang == 'ES' else "Tranche 3 (Optional - Phase 2 Expansion)", 0, "Q2 Año 3" if lang == 'ES' else "Q2 Year 3", "Módulo secundario de paletizado y visión artificial para control de calidad" if lang == 'ES' else "Secondary palletizing cell & computer vision QC inspection", "Crecimiento de ventas y saturación de capacidad > 85%" if lang == 'ES' else "Sales demand growth & line capacity utilization > 85%", "TIR marginal recalculada ≥ 15,0% sobre el Tramo 3" if lang == 'ES' else "Recalculated marginal IRR ≥ 15.0% for Tranche 3", "Comité de Dirección (C-Level)" if lang == 'ES' else "Executive Committee (C-Level)"),
    ]

    ws.row_dimensions[6].height = 24
    for idx, (t_name, imp, term, scope, kpi, thresh, owner) in enumerate(tranches, start=7):
        ws[f"B{idx}"].value = t_name
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"B{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = imp
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"C{idx}"].number_format = fmt_curr
        ws[f"C{idx}"].border = borders['thin']
        ws[f"C{idx}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"D{idx}"].value = term
        ws[f"D{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"D{idx}"].border = borders['thin']

        ws[f"E{idx}"].value = scope
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"E{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"E{idx}"].border = borders['thin']

        ws[f"F{idx}"].value = kpi
        ws[f"F{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"F{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"F{idx}"].border = borders['thin']

        ws[f"G{idx}"].value = thresh
        ws[f"G{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"G{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"G{idx}"].border = borders['thin']

        ws[f"H{idx}"].value = owner
        ws[f"H{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"H{idx}"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws[f"H{idx}"].border = borders['thin']
        ws.row_dimensions[idx].height = 28

    # Fila Total CAPEX
    ws["B10"].value = "TOTAL CAPEX COMPROMETIDO (TRAMOS 1 + 2)" if lang == 'ES' else "TOTAL COMMITTED CAPEX (TRANCHES 1 + 2)"
    ws["B10"].font = Font(name=FONT_NAME, size=10, bold=True)
    ws["B10"].alignment = Alignment(horizontal="left", vertical="center")
    ws["B10"].border = borders['total']
    ws["C10"].value = "=SUM(C7:C8)"
    ws["C10"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws["C10"].number_format = fmt_curr
    ws["C10"].alignment = Alignment(horizontal="right", vertical="center")
    ws["C10"].border = borders['total']
    for c in range(4, 9):
        ws[f"{get_column_letter(c)}10"].border = borders['total']
    ws.row_dimensions[10].height = 22

    # 3. SECCIÓN 2: Criterios de Cancelación Vinculantes (Kill Criteria)
    s2_title = "2. CRITERIOS DE CANCELACIÓN VINCULANTES (KILL CRITERIA / STOP-LOSS RULES)" if lang == 'ES' else "2. BINDING PROJECT ABORT RULES (KILL CRITERIA / STOP-LOSS POLICY)"
    ws["B12"].value = s2_title
    ws["B12"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_RED_TEXT)
    decorative.add("B12")
    ws.row_dimensions[12].height = 22

    kill_rules = [
        ("KILL CRITERIA 1 (Sobrecoste Técnico):" if lang == 'ES' else "KILL CRITERIA 1 (Engineering Overrun):", "Si el sobrecoste acumulado en la fase de ingeniería supera el 15% del Tramo 1 (> 127.500 €), congelar de inmediato el Tramo 2 y someter auditoría técnica al Consejo." if lang == 'ES' else "If cumulative engineering cost overruns exceed 15% of Tranche 1 (>$127.5k), freeze Tranche 2 immediately and submit technical audit to the Board."),
        ("KILL CRITERIA 2 (Fallo de Tracción Comercial):" if lang == 'ES' else "KILL CRITERIA 2 (Commercial Demand Failure):", "Si los pedidos contractuales o compromisos en firme a 9 meses de proyecto no alcanzan el 75% del volumen objetivo (69.000 u.), suspender integración del Tramo 2." if lang == 'ES' else "If binding commercial purchase commitments at 9 months fail to reach 75% of Year 1 volume (69,000 units), suspend Tranche 2 deployment."),
        ("KILL CRITERIA 3 (Deterioro de Rentabilidad WACC):" if lang == 'ES' else "KILL CRITERIA 3 (Hurdle Rate Deterioration):", "Si el recálculo semestral del DCF con datos reales arroja una TIR revisada inferior al WACC vigente (9,50%), activar protocolo de cancelación y desinversión del activo." if lang == 'ES' else "If semi-annual DCF recalculation with actual operating data yields revised IRR below current WACC (9.50%), trigger formal project termination protocol."),
    ]

    for idx, (k_lbl, k_txt) in enumerate(kill_rules, start=13):
        ws[f"B{idx}"].value = k_lbl
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_RED_TEXT)
        ws[f"B{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"B{idx}"].border = borders['thin']

        ws.merge_cells(f"C{idx}:H{idx}")
        ws[f"C{idx}"].value = k_txt
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"C{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        for c in range(3, 9):
            ws[f"{get_column_letter(c)}{idx}"].border = borders['thin']
        ws.row_dimensions[idx].height = 32

    # 4. SECCIÓN 3: Top 5 Riesgos y Plan de Mitigación
    s3_title = "3. REGISTRO DE RIESGOS CRÍTICOS & PLAN DE CONTINGENCIA" if lang == 'ES' else "3. CRITICAL RISK REGISTER & CONTINGENCY MITIGATION PLAN"
    ws["B17"].value = s3_title
    ws["B17"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B17")
    ws.row_dimensions[17].height = 22

    ws["B18"].value = "Riesgo Identificado" if lang == 'ES' else "Identified Risk"
    ws["B18"].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    ws["B18"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["B18"].alignment = Alignment(horizontal="left", vertical="center")
    ws["B18"].border = borders['header']
    decorative.add("B18")

    ws["C18"].value = "Probabilidad (1-5)" if lang == 'ES' else "Probability (1-5)"
    ws["C18"].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    ws["C18"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["C18"].alignment = Alignment(horizontal="center", vertical="center")
    ws["C18"].border = borders['header']
    decorative.add("C18")

    ws["D18"].value = "Impacto (1-5)" if lang == 'ES' else "Impact (1-5)"
    ws["D18"].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    ws["D18"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["D18"].alignment = Alignment(horizontal="center", vertical="center")
    ws["D18"].border = borders['header']
    decorative.add("D18")

    ws["E18"].value = "Severidad (P x I)" if lang == 'ES' else "Severity (P x I)"
    ws["E18"].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    ws["E18"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["E18"].alignment = Alignment(horizontal="center", vertical="center")
    ws["E18"].border = borders['header']
    decorative.add("E18")

    ws.merge_cells("F18:G18")
    ws["F18"].value = "Plan de Mitigación / Contingencia" if lang == 'ES' else "Mitigation & Contingency Action"
    ws["F18"].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    ws["F18"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["F18"].alignment = Alignment(horizontal="left", vertical="center")
    ws["F18"].border = borders['header']
    ws["G18"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["G18"].border = borders['header']
    decorative.add("F18")
    decorative.add("G18")

    ws["H18"].value = "Propietario del Riesgo" if lang == 'ES' else "Risk Owner"
    ws["H18"].font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    ws["H18"].fill = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
    ws["H18"].alignment = Alignment(horizontal="center", vertical="center")
    ws["H18"].border = borders['header']
    decorative.add("H18")
    ws.row_dimensions[18].height = 24

    risks = [
        ("Retraso en entrega de robótica principal" if lang == 'ES' else "Delay in main robotics delivery", 2, 4, "=C19*D19", "Contrato EPC con penalizaciones diarias por retraso del 0,5% y stock de seguridad" if lang == 'ES' else "Turnkey contract with 0.5%/day liquidated delay damages and safety inventory buffer", "Director de Compras" if lang == 'ES' else "Procurement Director"),
        ("Curva de aprendizaje de operarios lenta" if lang == 'ES' else "Slow operator digital learning curve", 3, 3, "=C20*D20", "Plan de formación intensiva previo con gemelo digital en simulación 3D" if lang == 'ES' else "Intensive pre-commissioning digital twin training in 3D plant simulation", "Director de RRHH" if lang == 'ES' else "HR & Training Director"),
        ("Presión de precios por entrada de competidor" if lang == 'ES' else "Pricing pressure from low-cost entrant", 3, 4, "=C21*D21", "Enfoque en contratos marco anuales con penalización por ruptura y mayor calidad OEE" if lang == 'ES' else "Focus on multi-year master supply agreements with volume rebates and superior OEE quality", "Director Comercial" if lang == 'ES' else "Commercial Director"),
        ("Incremento del coste energético en planta" if lang == 'ES' else "Industrial energy cost volatility", 2, 3, "=C22*D22", "PPA solar fotovoltaico cerrado para cubrir el 40% del consumo de la nueva línea" if lang == 'ES' else "Long-term solar PPA hedging covering 40% of new line power consumption", "Director de Planta" if lang == 'ES' else "Plant Energy Manager"),
        ("Desviación en integración de software MES" if lang == 'ES' else "MES software integration overrun", 2, 3, "=C23*D23", "Desarrollo modular bajo sprints ágiles con entregables quincenales vinculantes" if lang == 'ES' else "Modular agile sprints with bi-weekly deliverable validation gateways", "CIO / Director TI" if lang == 'ES' else "CIO / IT Director"),
    ]

    for idx, (r_name, prob, imp, sev_f, mit, owner) in enumerate(risks, start=19):
        ws[f"B{idx}"].value = r_name
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"B{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"B{idx}"].border = borders['thin']

        ws[f"C{idx}"].value = prob
        ws[f"C{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"C{idx}"].border = borders['thin']

        ws[f"D{idx}"].value = imp
        ws[f"D{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"D{idx}"].border = borders['thin']

        ws[f"E{idx}"].value = sev_f
        ws[f"E{idx}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_AMBER_TEXT)
        ws[f"E{idx}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"E{idx}"].border = borders['thin']

        ws.merge_cells(f"F{idx}:G{idx}")
        ws[f"F{idx}"].value = mit
        ws[f"F{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"F{idx}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws[f"F{idx}"].border = borders['thin']
        ws[f"G{idx}"].border = borders['thin']

        ws[f"H{idx}"].value = owner
        ws[f"H{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"H{idx}"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws[f"H{idx}"].border = borders['thin']

        ws.row_dimensions[idx].height = 30

    # 5. SECCIÓN 4: Bloque de Firmas y Decision Gateway (Filas 25 a 30)
    s4_title = "4. RESOLUCIÓN FORMAL DEL CONSEJO DE ADMINISTRACIÓN (BOARD DECISION GATEWAY)" if lang == 'ES' else "4. FORMAL BOARD OF DIRECTORS RESOLUTION (BOARD DECISION GATEWAY)"
    ws["B25"].value = s4_title
    ws["B25"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B25")
    ws.row_dimensions[25].height = 22

    signatures = [
        ("Consejero Delegado (CEO)" if lang == 'ES' else "Chief Executive Officer (CEO)", "Aprobación Estratégica Global" if lang == 'ES' else "Strategic Business Approval", "Firma: ________________________", "B", "B"),
        ("Director Financiero (CFO)" if lang == 'ES' else "Chief Financial Officer (CFO)", "Validación de WACC, VAN y Financiación" if lang == 'ES' else "WACC, DCF & Liquidity Sign-Off", "Firma: ________________________", "C", "D"),
        ("Presidente Comité Inversiones" if lang == 'ES' else "Investment Committee Chair", "Dictamen Hurdle Policy & Stage Gates" if lang == 'ES' else "Hurdle Policy & Stage Gate Verdict", "Firma: ________________________", "E", "F"),
        ("Director de Operaciones (COO)" if lang == 'ES' else "Chief Operating Officer (COO)", "Compromiso de CAPEX, OEE y Plazos" if lang == 'ES' else "CAPEX, OEE & Execution Commitment", "Firma: ________________________", "G", "H"),
    ]

    for role, mandate, sig_line, c_start, c_end in signatures:
        if c_start != c_end:
            ws.merge_cells(f"{c_start}27:{c_end}27")
            ws.merge_cells(f"{c_start}28:{c_end}28")
            ws.merge_cells(f"{c_start}29:{c_end}29")

        ws[f"{c_start}27"].value = role
        ws[f"{c_start}27"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_NAVY_DARK)
        ws[f"{c_start}27"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        ws[f"{c_start}28"].value = mandate
        ws[f"{c_start}28"].font = Font(name=FONT_NAME, size=8, italic=True, color="64748B")
        ws[f"{c_start}28"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        ws[f"{c_start}29"].value = sig_line
        ws[f"{c_start}29"].font = Font(name=FONT_NAME, size=9)
        ws[f"{c_start}29"].alignment = Alignment(horizontal="center", vertical="center")

        start_col = openpyxl.utils.column_index_from_string(c_start)
        end_col = openpyxl.utils.column_index_from_string(c_end)
        for r in range(27, 30):
            for c in range(start_col, end_col + 1):
                coord = f"{get_column_letter(c)}{r}"
                ws[coord].border = borders['thin']
                decorative.add(coord)

    ws.row_dimensions[27].height = 20
    ws.row_dimensions[28].height = 20
    ws.row_dimensions[29].height = 24

    # Anchos de columna
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 46
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 18
    ws.column_dimensions["E"].width = 36
    ws.column_dimensions["F"].width = 38
    ws.column_dimensions["G"].width = 28
    ws.column_dimensions["H"].width = 26

    finalize_sheet(ws, decorative_cells=frozenset(decorative))


def build_tab6_user_guide(wb, lang='ES'):
    """Construye la Pestaña 6: Guía de Uso / User Guide."""
    sheet_title = "Guía de Uso" if lang == 'ES' else "User Guide"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    borders = create_borders()
    decorative = set()

    # 1. Cabecera Principal
    h_title = (
        "GUÍA DE USO METODOLÓGICA, CONVENCIÓN VISUAL Y GLOSARIO FINANCIERO"
        if lang == 'ES' else
        "METHODOLOGICAL USER GUIDE, VISUAL CONVENTION AND FINANCIAL GLOSSARY"
    )
    style_merged_header(ws, "B2:G3", h_title, decorative, COLOR_NAVY_DARK, "FFFFFF", 12)
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 20

    # 2. SECCIÓN 1: Flujo de Trabajo
    ws["B5"].value = "1. PROTOCOLO DE TRABAJO EN 5 PASOS" if lang == 'ES' else "1. 5-STEP EXECUTIVE WORKFLOW"
    ws["B5"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B5")

    steps = [
        ("Paso 1: Calibrar Hurdle Policy y WACC", "En la Pestaña 2 ('Supuestos & Drivers'), revisa los parámetros macro (Rf, Beta, ERP) o introduce el WACC manual de la compañía.", "Step 1: Calibrate Hurdle Policy & WACC", "In Tab 2 ('Assumptions & Drivers'), review CAPM parameters or enter the company's manual WACC."),
        ("Paso 2: Ajustar Drivers Operativos y Escenarios", "Introduce el volumen previsto, precio, costes variables, OPEX y CAPEX en las columnas Pesimista, Base y Optimista.", "Step 2: Adjust Operating Drivers & Scenarios", "Input expected volume, pricing, variable costs, OPEX and CAPEX across Pessimistic, Base and Optimistic columns."),
        ("Paso 3: Auditar la Proyección DCF", "En la Pestaña 3 ('Proyección DCF'), verifica que la fila 42 muestre '✅ Modelo cuadrado' y comprueba los flujos FCF de los Años 0 a 5.", "Step 3: Audit DCF Projections", "In Tab 3 ('DCF Projection'), ensure row 42 confirms '✅ Model Balanced' and review discrete FCF lines for Years 0 to 5."),
        ("Paso 4: Analizar la Sensibilidad Tornado", "En la Pestaña 4 ('Sensibilidad & Tornado'), identifica qué variables dominan el riesgo y revisa los puntos de equilibrio lineales.", "Step 4: Analyze Tornado Sensitivity", "In Tab 4 ('Sensitivity & Tornado'), identify primary risk drivers and evaluate break-even points where NPV = 0."),
        ("Paso 5: Someter al Comité de Inversiones", "En la Pestaña 1 ('Dashboard Ejecutivo'), comprueba el semáforo de dictamen automático y formaliza la gobernanza en la Pestaña 5.", "Step 5: Present to Investment Committee", "In Tab 1 ('Executive Dashboard'), review automatic verdict seal and formalize Stage Gate governance in Tab 5."),
    ]

    for idx, (s_title_es, s_desc_es, s_title_en, s_desc_en) in enumerate(steps, start=6):
        title = s_title_es if lang == 'ES' else s_title_en
        desc = s_desc_es if lang == 'ES' else s_desc_en

        ws[f"B{idx}"].value = title
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=10, bold=True)
        ws[f"B{idx}"].border = borders['thin']
        ws[f"B{idx}"].alignment = Alignment(vertical="center", wrap_text=True)

        ws.merge_cells(f"C{idx}:G{idx}")
        ws[f"C{idx}"].value = desc
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"C{idx}"].border = borders['thin']
        ws[f"C{idx}"].alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[idx].height = 28
        for c in range(3, 8):
            ws[f"{get_column_letter(c)}{idx}"].border = borders['thin']

    # 3. SECCIÓN 2: Convención Visual de Celdas
    ws["B12"].value = "2. CONVENCIÓN VISUAL Y POLÍTICA DE PROTECCIÓN DE CELDAS" if lang == 'ES' else "2. VISUAL CONVENTION AND CELL PROTECTION POLICY"
    ws["B12"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B12")

    visual_rules = [
        ("Celdas en BLANCO (#FFFFFF):", "Celdas de ENTRADA 100% editables. Puedes modificar libremente precios, volúmenes, costes y supuestos sin restricciones." if lang == 'ES' else "100% editable INPUT cells. Freely enter volumes, prices, cost rates and investment parameters."),
        ("Celdas en GRIS SUAVE (#F1F5F9):", "Celdas de FÓRMULA PROTEGIDAS. Salvaguardan la integridad del motor DCF, rankings y semáforos ante auditorías." if lang == 'ES' else "PROTECTED FORMULA cells. Safeguard financial DCF integrity and rankings during committee reviews."),
        ("Contraseña de Protección Oficial:", "Bajo contraseña proporcionada en las instrucciones dentro del archivo .ZIP (LEEME_INSTRUCCIONES.txt)." if lang == 'ES' else "Protected under password provided in instructions within the .ZIP package (README_INSTRUCTIONS.txt)."),
        ("Soporte Corporativo Datalaria:", "Para dudas metodológicas, adaptaciones a ERP o soporte técnico: datalaria@gmail.com" if lang == 'ES' else "For methodological inquiries, ERP adaptations or technical support: datalaria@gmail.com"),
    ]

    for idx, (v_title, v_desc) in enumerate(visual_rules, start=13):
        ws[f"B{idx}"].value = v_title
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=9, bold=True)
        ws[f"B{idx}"].border = borders['thin']
        ws[f"B{idx}"].alignment = Alignment(vertical="center", wrap_text=True)

        ws.merge_cells(f"C{idx}:G{idx}")
        ws[f"C{idx}"].value = v_desc
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"C{idx}"].border = borders['thin']
        ws[f"C{idx}"].alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[idx].height = 28
        for c in range(3, 8):
            ws[f"{get_column_letter(c)}{idx}"].border = borders['thin']

    # 4. SECCIÓN 3: Glosario Ejecutivo
    ws["B18"].value = "3. GLOSARIO DE CONCEPTOS FINANCIEROS CLAVE" if lang == 'ES' else "3. GLOSSARY OF KEY FINANCIAL CONCEPTS"
    ws["B18"].font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_BLUE_ACCENT)
    decorative.add("B18")

    glossary = [
        ("Flujo de Caja Libre (FCF):", "Caja neta generada por la explotación disponible para acreedores y accionistas tras reinvertir en CAPEX y circulante." if lang == 'ES' else "Net cash generated by operations available to debt & equity holders after CAPEX and working capital."),
        ("WACC (Coste de Capital):", "Coste promedio ponderado de los recursos financieros (capital propio + deuda neta de impuestos) según CAPM." if lang == 'ES' else "Weighted average cost of capital blending cost of equity (CAPM) and after-tax borrowing cost."),
        ("Valor Actual Neto (VAN / NPV):", "Valor económico neto creado por la inversión hoy tras descontar todos los flujos futuros al WACC." if lang == 'ES' else "Net economic value added by project today after discounting future cash flows at WACC."),
        ("Tasa Interna de Retorno (TIR / IRR):", "Tasa de rendimiento intrínseca del proyecto que anula el VAN. Seductora pero vulnerable al supuesto de reinversión." if lang == 'ES' else "Discount rate setting project NPV to zero. Intuitive metric but subject to unrealistic reinvestment assumption."),
        ("TIR Modificada (MIRR):", "Tasa de rendimiento que asume explícitamente que los flujos positivos se reinvierten al WACC de la empresa." if lang == 'ES' else "Rate of return explicitly assuming positive interim cash flows are reinvested at firm's WACC."),
        ("Payback Descontado:", "Número de años necesarios para recuperar la inversión inicial considerando el coste de oportunidad del capital." if lang == 'ES' else "Number of years needed to recover invested capital taking opportunity cost of money into account."),
        ("Índice de Rentabilidad (PI):", "Cociente entre el valor presente de los flujos positivos y el desembolso inicial descontado (eficiencia del capital)." if lang == 'ES' else "Ratio of present value of future cash inflows to initial discounted capital outlay."),
        ("Peak Funding:", "Importe máximo de tesorería comprometido acumulado; representa la necesidad crediticia pico del proyecto." if lang == 'ES' else "Maximum cumulative negative cash trough; represents peak liquidity requirement."),
        ("Gráfico Tornado:", "Representación gráfica de barras que clasifica los drivers según el rango de impacto univariable generado en el VAN." if lang == 'ES' else "Bar chart ranking sensitivity variables from largest to smallest swing impact on NPV."),
    ]

    for idx, (g_term, g_def) in enumerate(glossary, start=19):
        ws[f"B{idx}"].value = g_term
        ws[f"B{idx}"].font = Font(name=FONT_NAME, size=9, bold=True)
        ws[f"B{idx}"].border = borders['thin']
        ws[f"B{idx}"].alignment = Alignment(vertical="center", wrap_text=True)

        ws.merge_cells(f"C{idx}:G{idx}")
        ws[f"C{idx}"].value = g_def
        ws[f"C{idx}"].font = Font(name=FONT_NAME, size=9)
        ws[f"C{idx}"].border = borders['thin']
        ws[f"C{idx}"].alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[idx].height = 26
        for c in range(3, 8):
            ws[f"{get_column_letter(c)}{idx}"].border = borders['thin']

    # Anchos de columna
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 38
    ws.column_dimensions["C"].width = 24
    ws.column_dimensions["D"].width = 24
    ws.column_dimensions["E"].width = 24
    ws.column_dimensions["F"].width = 24
    ws.column_dimensions["G"].width = 24

    finalize_sheet(ws, decorative_cells=frozenset(decorative))


def register_defined_names(wb, lang='ES'):
    """Registra los nombres de rango canónicos para salidas clave."""
    sheet_dcf = "Proyección DCF" if lang == 'ES' else "DCF Projection"
    sheet_assumptions = "Supuestos & Drivers" if lang == 'ES' else "Assumptions & Drivers"
    sheet_sens = "Sensibilidad & Tornado" if lang == 'ES' else "Sensitivity & Tornado"

    # Definir nombres según openpyxl 3.1
    wb.defined_names['VAN_Base'] = DefinedName('VAN_Base', attr_text=f"'{sheet_dcf}'!$C$33")
    wb.defined_names['TIR_Base'] = DefinedName('TIR_Base', attr_text=f"'{sheet_dcf}'!$C$35")
    wb.defined_names['WACC'] = DefinedName('WACC', attr_text=f"'{sheet_assumptions}'!$C$28")
    wb.defined_names['Payback_Desc'] = DefinedName('Payback_Desc', attr_text=f"'{sheet_dcf}'!$C$38")
    wb.defined_names['VAN_Esperado'] = DefinedName('VAN_Esperado', attr_text=f"'{sheet_sens}'!$D$53")


def generate_workbook(lang='ES', out_path=None):
    """Genera el libro completo para el idioma especificado ('ES' o 'EN')."""
    print(f"\n[GENERANDO EXCEL {lang}] -> {out_path}...")
    wb = openpyxl.Workbook()
    # Eliminar hoja por defecto
    wb.remove(wb.active)

    # Orden de construcción por dependencias:
    # Tab 2 (Supuestos), Tab 3 (DCF), Tab 4 (Sensibilidad), Tab 5 (Gobernanza), Tab 6 (Guía), Tab 1 (Dashboard)
    build_tab2_assumptions(wb, lang)
    build_tab3_dcf(wb, lang)
    build_tab4_sensitivity(wb, lang)
    build_tab5_governance(wb, lang)
    build_tab6_user_guide(wb, lang)
    build_tab1_dashboard(wb, lang)

    # Reordenar hojas para que el Dashboard Ejecutivo sea la primera pestaña
    sheet_names = wb.sheetnames
    # El dashboard es la última hoja creada; moverla a la primera posición
    dash_name = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    ordered_sheets = [wb[dash_name]] + [wb[s] for s in sheet_names if s != dash_name]
    wb._sheets = ordered_sheets

    # Registrar nombres de rango canónicos
    register_defined_names(wb, lang)

    # Establecer la primera pestaña como activa
    wb.active = 0

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb.save(out_path)
    print(f"[OK] Archivo generado exitosamente: {out_path}")


def main():
    path_es = os.path.join(
        "packages", "Suite_02_Toma_Decisiones", "03_Business_Case_VAN_TIR",
        "[ES]_Business_Case_VAN_TIR", "Business_Case_VAN_TIR_Datalaria_ES.xlsx"
    )
    path_en = os.path.join(
        "packages", "Suite_02_Toma_Decisiones", "03_Business_Case_VAN_TIR",
        "[EN]_Financial_Business_Case", "Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx"
    )

    generate_workbook(lang='ES', out_path=path_es)
    generate_workbook(lang='EN', out_path=path_en)
    print("\n[ÉXITO] Generación de libros Excel completada.")


if __name__ == "__main__":
    main()
