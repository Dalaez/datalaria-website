#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos analíticos oficiales en Excel (.xlsx) de grado Consejo de Administración:
1. packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/[ES]_Stock_Seguridad_ROP/Calculadora_Stock_Seguridad_ROP_ES.xlsx
2. packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/[EN]_Safety_Stock_ROP/Safety_Stock_ROP_Calculator_EN.xlsx

Arquitectura de 4 Pestañas Funcionales:
- Pestaña 1: "Dashboard Ejecutivo" / "Executive Dashboard"
- Pestaña 2: "Matriz SKU & Datos Operativos" / "SKU Matrix & Operational Inputs"
- Pestaña 3: "Motor Matemático SS & ROP" / "Safety Stock & ROP Models"
- Pestaña 4: "Trade-offs de Working Capital" / "Working Capital Optimization"

Estándar de Seguridad y Compatibilidad OpenXML ECMA-376:
- Celdas de entrada (usuario): locked=False, fondo blanco #FFFFFF.
- Celdas con fórmulas: locked=True, fondo #F1F5F9.
- Contraseña oficial interna: "Datalaria2026".
- ECMA-376: selectUnlockedCells = False, selectLockedCells = False.
- Gráfico Diente de Sierra (Sawtooth) nativo de Openpyxl.
- Alturas de fila y anchos de columna generosos para legibilidad ejecutiva sin solapes.
"""

import os
import sys
import math
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.layout import Layout, ManualLayout

# Importar política de protección ECMA-376
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from protection_policy import finalize_protection, apply_sheet_protection

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = "0F172A"       # Slate 900
COLOR_NAVY_MED = "1E293B"        # Slate 800
COLOR_NAVY_LIGHT = "334155"      # Slate 700
COLOR_BLUE_ACCENT = "2563EB"     # Blue 600
COLOR_BLUE_LIGHT = "EFF6FF"      # Blue 50
COLOR_CYAN_ACCENT = "0284C7"     # Sky 600

COLOR_GREEN_BG = "D1FAE5"        # Emerald 100
COLOR_GREEN_TEXT = "065F46"      # Emerald 800
COLOR_GREEN_BORDER = "10B981"    # Emerald 500

COLOR_AMBER_BG = "FEF3C7"        # Amber 100
COLOR_AMBER_TEXT = "92400E"      # Amber 800
COLOR_AMBER_BORDER = "F59E0B"    # Amber 500

COLOR_RED_BG = "FEE2E2"          # Red 100
COLOR_RED_TEXT = "991B1B"        # Red 800
COLOR_RED_BORDER = "DC2626"      # Red 600

COLOR_BG_CARD = "F8FAFC"         # Slate 50
COLOR_BG_INPUT = "FFFFFF"        # Blanco puro para inputs
COLOR_BG_FORMULA = "F1F5F9"      # Slate 100 para fórmulas
COLOR_BORDER_LIGHT = "CBD5E1"    # Slate 300
COLOR_BORDER_DARK = "64748B"     # Slate 500

FONT_NAME = "Segoe UI"

# Estilos reutilizables
font_title = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
font_subtitle = Font(name=FONT_NAME, size=9.5, italic=True, color="94A3B8")
font_section = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_NAVY_DARK)
font_tbl_header = Font(name=FONT_NAME, size=9.5, bold=True, color="FFFFFF")
font_tbl_subheader = Font(name=FONT_NAME, size=9, bold=True, color="FFFFFF")
font_card_title = Font(name=FONT_NAME, size=8.5, bold=True, color="64748B")
font_card_val = Font(name=FONT_NAME, size=15, bold=True, color=COLOR_NAVY_DARK)
font_card_sub = Font(name=FONT_NAME, size=8, italic=True, color="64748B")
font_body = Font(name=FONT_NAME, size=9.5, color="1E293B")
font_body_bold = Font(name=FONT_NAME, size=9.5, bold=True, color="1E293B")
font_input = Font(name=FONT_NAME, size=9.5, bold=True, color=COLOR_BLUE_ACCENT)

fill_dark = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_DARK)
fill_med = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_MED)
fill_blue_accent = PatternFill(fill_type="solid", fgColor=COLOR_BLUE_ACCENT)
fill_blue_card = PatternFill(fill_type="solid", fgColor=COLOR_BLUE_LIGHT)
fill_card = PatternFill(fill_type="solid", fgColor=COLOR_BG_CARD)
fill_formula = PatternFill(fill_type="solid", fgColor=COLOR_BG_FORMULA)
fill_input = PatternFill(fill_type="solid", fgColor=COLOR_BG_INPUT)

fill_green = PatternFill(fill_type="solid", fgColor=COLOR_GREEN_BG)
fill_amber = PatternFill(fill_type="solid", fgColor=COLOR_AMBER_BG)
fill_red = PatternFill(fill_type="solid", fgColor=COLOR_RED_BG)

thin_border_side = Side(style="thin", color=COLOR_BORDER_LIGHT)
border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
border_thick_side = Side(style="medium", color=COLOR_BLUE_ACCENT)
border_card = Border(left=border_thick_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
border_top_total = Border(top=Side(style="thin", color=COLOR_NAVY_DARK), bottom=Side(style="double", color=COLOR_NAVY_DARK))

# Catálogo maestro de 35 SKUs realistas
SKU_CATALOG = [
    # Clase A: Alto valor de consumo / referencias críticas (7 SKUs)
    ("SKU-1001", "Electrónica & Control", "Microcontrolador Industrial 32-bit Cortex M4", "A", 50, 12, 8, 2, 0.98, 48.50, 0.22, 250.0),
    ("SKU-1002", "Electrónica & Control", "Módulo de Potencia IGBT 1200V / 100A", "A", 85, 22, 21, 5, 0.98, 72.00, 0.22, 120.0),
    ("SKU-1003", "Mecánica & Transmisión", "Servomotor Brushless de Alta Precisión 2.5kW", "A", 35, 14, 35, 12, 0.98, 185.00, 0.20, 150.0),
    ("SKU-1004", "Farma & Diagnóstico", "Reactivo Enzimático Ultra-puro BioTech (Vial 50ml)", "A", 65, 18, 10, 2, 0.99, 140.00, 0.25, 90.0),
    ("SKU-1005", "Automoción & Maquinaria", "Bomba Hidráulica de Pistones Axiales", "A", 25, 10, 40, 14, 0.98, 295.00, 0.20, 160.0),
    ("SKU-1006", "Química & Polímeros", "Resina Epoxi Grado Aeroespacial (Tambor 200L)", "A", 15, 6, 35, 12, 0.98, 410.00, 0.24, 180.0),
    ("SKU-1007", "Telecomunicaciones", "Transceptor Óptico 100G QSFP28 Singlemode", "A", 110, 32, 12, 3, 0.98, 65.00, 0.22, 110.0),

    # Clase B: Valor y rotación intermedia (12 SKUs)
    ("SKU-2001", "Electrónica & Control", "Fuente de Alimentación Conmutada 24V 10A", "B", 75, 18, 14, 3, 0.95, 32.00, 0.22, 85.0),
    ("SKU-2002", "Mecánica & Transmisión", "Rodamiento de Rodillos Cónicos SKF Ø60mm", "B", 90, 24, 15, 4, 0.95, 26.50, 0.20, 75.0),
    ("SKU-2003", "Farma & Diagnóstico", "Kit de Filtros de Membrana Estéril 0.22µm", "B", 130, 30, 10, 2, 0.95, 18.00, 0.22, 60.0),
    ("SKU-2004", "Packaging & FMCG", "Envase Biodegradable Termoformado 500ml (x100)", "B", 240, 55, 7, 2, 0.95, 12.50, 0.20, 50.0),
    ("SKU-2005", "Neumática & Válvulas", "Electroválvula Neumática 5/2 Biestable", "B", 80, 20, 12, 3, 0.95, 38.00, 0.20, 80.0),
    ("SKU-2006", "Electrónica & Control", "Sensor Inductivo M18 Alcance Extendido", "B", 95, 22, 14, 3, 0.95, 24.00, 0.20, 70.0),
    ("SKU-2007", "Química & Polímeros", "Aditivo Anti-UV para Extrusión (Saco 25kg)", "B", 60, 14, 18, 4, 0.95, 42.00, 0.22, 90.0),
    ("SKU-2008", "Ferretería Industrial", "Cadena de Rodillos Doble ANSI 50-2 (Metro)", "B", 85, 19, 14, 3, 0.95, 28.00, 0.20, 75.0),
    ("SKU-2009", "Automoción & Maquinaria", "Filtro Hidráulico de Retorno Alta Eficiencia", "B", 110, 25, 11, 2, 0.95, 19.50, 0.20, 65.0),
    ("SKU-2010", "Packaging & FMCG", "Bobina Film Estirable Automático 23µm", "B", 150, 35, 8, 2, 0.95, 15.00, 0.20, 55.0),
    ("SKU-2011", "Telecomunicaciones", "Patch Cord Fibra Óptica LC-LC Dúplex 5m", "B", 200, 45, 9, 2, 0.95, 9.80, 0.20, 50.0),
    ("SKU-2012", "Textil Técnico", "Tejido Poliéster Ignífugo de Alta Tenacidad (m²)", "B", 140, 32, 16, 4, 0.95, 14.20, 0.22, 70.0),

    # Clase C: Bajo valor individual / alta variedad (16 SKUs)
    ("SKU-3001", "Tornillería & Fijación", "Tornillo DIN 912 M8x35 Inox A2 (Caja 100u)", "C", 220, 50, 7, 2, 0.90, 6.20, 0.20, 45.0),
    ("SKU-3002", "Tornillería & Fijación", "Tuerca Autoblocante DIN 985 M8 (Caja 200u)", "C", 310, 70, 6, 2, 0.90, 4.10, 0.20, 40.0),
    ("SKU-3003", "Conectores & Cableado", "Terminal Faston Aislado Hembra 6.3 (Caja 500u)", "C", 400, 90, 8, 2, 0.90, 3.80, 0.20, 40.0),
    ("SKU-3004", "Packaging & FMCG", "Cinta Adhesiva Acrílica Marrón 50mmx66m (x6)", "C", 280, 60, 5, 1, 0.90, 5.50, 0.20, 45.0),
    ("SKU-3005", "Neumática & Válvulas", "Racor Recto Neumático Tubo 8mm - R1/4", "C", 250, 55, 9, 2, 0.90, 3.20, 0.20, 40.0),
    ("SKU-3006", "Electrónica & Control", "Resistencia SMD 1206 10k 1% (Rollo 5000u)", "C", 180, 40, 12, 3, 0.90, 7.50, 0.20, 50.0),
    ("SKU-3007", "Ferretería Industrial", "Arandela de Cobre M14 para Carter (Caja 100)", "C", 190, 45, 6, 1, 0.90, 4.60, 0.20, 40.0),
    ("SKU-3008", "Seguridad Laboral", "Guante Nitrilo Desechable Talla L (Caja 100)", "C", 350, 75, 5, 1, 0.90, 6.80, 0.20, 45.0),
    ("SKU-3009", "Seguridad Laboral", "Mascarilla FFP2 Auto-filtrante (Pack 50u)", "C", 260, 60, 6, 2, 0.90, 8.50, 0.20, 45.0),
    ("SKU-3010", "Packaging & FMCG", "Caja Cartón Canal Doble 400x300x200 (x25)", "C", 210, 48, 7, 2, 0.90, 9.20, 0.20, 50.0),
    ("SKU-3011", "Conectores & Cableado", "Bridas de Nylon Negro 300x4.8mm (Pack 100)", "C", 380, 85, 5, 1, 0.90, 2.90, 0.20, 35.0),
    ("SKU-3012", "Ferretería Industrial", "Junta Tórica NBR 70 Shore Ø25x3mm (Pack 50)", "C", 240, 50, 8, 2, 0.90, 4.30, 0.20, 40.0),
    ("SKU-3013", "Química & Mantenimiento", "Spray Lubricante Multiusos PTFE 400ml", "C", 160, 35, 7, 2, 0.90, 5.80, 0.20, 45.0),
    ("SKU-3014", "Electrónica & Control", "Fusible Cerámico 5x20mm 2A Rápido (Pack 20)", "C", 290, 65, 8, 2, 0.90, 3.40, 0.20, 40.0),
    ("SKU-3015", "Tornillería & Fijación", "Pasador Elástico DIN 1481 Ø5x30 (Caja 100)", "C", 170, 38, 9, 2, 0.90, 4.80, 0.20, 40.0),
    ("SKU-3016", "Textil Técnico", "Cinta de Velcro Autoadhesiva 25mm (Rollo 25m)", "C", 130, 30, 10, 2, 0.90, 8.10, 0.20, 50.0),
]


def create_header(ws, title_text, subtitle_text, max_col=12):
    """Crea la cabecera ejecutiva Datalaria en la fila 1 y 2."""
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max_col)
    cell1 = ws.cell(row=1, column=1)
    cell1.value = f"  DATALARIA  |  {title_text.upper()}"
    cell1.font = font_title
    cell1.fill = fill_dark
    cell1.alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[1].height = 36

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max_col)
    cell2 = ws.cell(row=2, column=1)
    cell2.value = f"  {subtitle_text}"
    cell2.font = font_subtitle
    cell2.fill = fill_med
    cell2.alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[2].height = 22


def build_workbook(lang="ES"):
    """Construye el libro completo en el idioma especificado (ES o EN)."""
    is_es = (lang == "ES")
    wb = openpyxl.Workbook()

    # Formatos de moneda y porcentaje
    curr_fmt = "#,##0.00 €" if is_es else "$#,##0.00"
    pct_fmt = "0.0%"
    int_fmt = "#,##0"
    dec_fmt = "#,##0.00"

    # Nombres de pestañas
    t1_name = "Dashboard Ejecutivo" if is_es else "Executive Dashboard"
    t2_name = "Matriz SKU & Datos Operativos" if is_es else "SKU Matrix & Operational Inputs"
    t3_name = "Motor Matemático SS & ROP" if is_es else "Safety Stock & ROP Models"
    t4_name = "Trade-offs de Working Capital" if is_es else "Working Capital Optimization"

    # =========================================================================
    # PESTAÑA 2: MATRIZ SKU & DATOS OPERATIVOS (Base de datos para fórmulas)
    # =========================================================================
    ws2 = wb.active
    ws2.title = t2_name
    ws2.views.sheetView[0].showGridLines = True

    t2_title = "Matriz SKU & Datos Operativos de Inventario" if is_es else "SKU Matrix & Operational Inventory Inputs"
    t2_sub = "Parámetros de demanda estocástica (d, σd), fiabilidad del proveedor (L, σL), costes y nivel de servicio" if is_es else "Stochastic demand parameters (d, σd), supplier reliability (L, σL), costs and target service levels"
    create_header(ws2, t2_title, t2_sub, max_col=14)

    # Cabeceras de tabla en fila 4
    headers_t2_es = [
        "SKU ID", "Categoría", "Descripción del Producto", "Clase ABC",
        "Demanda Diaria Media (d) [u/día]", "Desv. Est. Demanda (σd) [u/día]",
        "Lead Time Medio (L) [días]", "Desv. Est. Lead Time (σL) [días]",
        "Nivel Servicio Objetivo (CSL) [%]", "Coste Unitario Adq. (C) [€/u]",
        "Tasa Mantenimiento Anual (h) [%/año]", "Coste Emisión Pedido (S) [€/ped]",
        "Demanda Anual (D) [u/año]", "Consumo Anual Valor (€/año)"
    ]
    headers_t2_en = [
        "SKU ID", "Category", "Product Description", "ABC Class",
        "Mean Daily Demand (d) [u/day]", "Demand Std Dev (σd) [u/day]",
        "Mean Lead Time (L) [days]", "Lead Time Std Dev (σL) [days]",
        "Target Service Level (CSL) [%]", "Unit Purchase Cost (C) [$/u]",
        "Annual Holding Cost Rate (h) [%/yr]", "Fixed Order Cost (S) [$/order]",
        "Annual Demand (D) [u/yr]", "Annual Consumption Value ($/yr)"
    ]
    headers_t2 = headers_t2_es if is_es else headers_t2_en

    ws2.row_dimensions[4].height = 30
    for col_idx, h in enumerate(headers_t2, 1):
        c = ws2.cell(row=4, column=col_idx, value=h)
        c.font = font_tbl_header
        c.fill = fill_blue_accent if col_idx <= 12 else fill_med
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border_cell

    t2_input_coords = []
    t2_formula_coords = []

    start_row = 5
    for i, item in enumerate(SKU_CATALOG):
        r = start_row + i
        ws2.row_dimensions[r].height = 20
        sku, cat, desc, abc, d, sig_d, L, sig_L, csl, C, h, S = item

        # Columnas 1 a 4: Identificación y Clasificación SKU (Entradas desbloqueadas, fondo blanco puro #FFFFFF)
        c_sku = ws2.cell(row=r, column=1, value=sku)
        c_sku.font = font_body_bold; c_sku.alignment = Alignment(horizontal="center", vertical="center"); c_sku.border = border_cell
        c_sku.fill = fill_input; c_sku.protection = Protection(locked=False)
        t2_input_coords.append(c_sku.coordinate)

        c_cat = ws2.cell(row=r, column=2, value=cat)
        c_cat.font = font_body; c_cat.alignment = Alignment(horizontal="left", vertical="center"); c_cat.border = border_cell
        c_cat.fill = fill_input; c_cat.protection = Protection(locked=False)
        t2_input_coords.append(c_cat.coordinate)

        c_desc = ws2.cell(row=r, column=3, value=desc)
        c_desc.font = font_body; c_desc.alignment = Alignment(horizontal="left", vertical="center"); c_desc.border = border_cell
        c_desc.fill = fill_input; c_desc.protection = Protection(locked=False)
        t2_input_coords.append(c_desc.coordinate)

        c_abc = ws2.cell(row=r, column=4, value=abc)
        c_abc.font = font_body_bold; c_abc.alignment = Alignment(horizontal="center", vertical="center"); c_abc.border = border_cell
        c_abc.fill = fill_input; c_abc.protection = Protection(locked=False)
        t2_input_coords.append(c_abc.coordinate)

        # Columnas 5 a 12: Parámetros operativos y costes (Entradas desbloqueadas, fondo blanco puro #FFFFFF)
        vals_inputs = [
            (5, d, int_fmt),
            (6, sig_d, dec_fmt),
            (7, L, int_fmt),
            (8, sig_L, dec_fmt),
            (9, csl, pct_fmt),
            (10, C, curr_fmt),
            (11, h, pct_fmt),
            (12, S, curr_fmt),
        ]
        for col_idx, val, fmt in vals_inputs:
            c = ws2.cell(row=r, column=col_idx, value=val)
            c.font = font_input
            c.number_format = fmt
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.border = border_cell
            c.fill = fill_input
            c.protection = Protection(locked=False)
            t2_input_coords.append(c.coordinate)

        # Columnas 13 y 14: Fórmulas calculadas (Bloqueadas, fondo gris claro #F1F5F9)
        # Demanda Anual D = d * 365
        c_D = ws2.cell(row=r, column=13, value=f"=E{r}*365")
        c_D.font = font_body_bold
        c_D.number_format = int_fmt
        c_D.alignment = Alignment(horizontal="right", vertical="center")
        c_D.border = border_cell
        c_D.fill = fill_formula
        c_D.protection = Protection(locked=True)
        t2_formula_coords.append(c_D.coordinate)

        # Consumo Anual Valor = D * C
        c_val = ws2.cell(row=r, column=14, value=f"=M{r}*J{r}")
        c_val.font = font_body_bold
        c_val.number_format = curr_fmt
        c_val.alignment = Alignment(horizontal="right", vertical="center")
        c_val.border = border_cell
        c_val.fill = fill_formula
        c_val.protection = Protection(locked=True)
        t2_formula_coords.append(c_val.coordinate)

    # Fila de Totales y Medias
    tot_row = start_row + len(SKU_CATALOG)
    ws2.row_dimensions[tot_row].height = 24
    c_tot_label = ws2.cell(row=tot_row, column=1, value="TOTALES / MEDIAS PONDERADAS" if is_es else "TOTALS / WEIGHTED AVERAGES")
    c_tot_label.font = font_body_bold
    c_tot_label.alignment = Alignment(horizontal="left", vertical="center")
    c_tot_label.border = border_top_total
    ws2.merge_cells(start_row=tot_row, start_column=1, end_row=tot_row, end_column=4)

    # Fórmulas de medias
    for c_idx in range(5, 13):
        c = ws2.cell(row=tot_row, column=c_idx, value=f"=AVERAGE({get_column_letter(c_idx)}5:{get_column_letter(c_idx)}{tot_row-1})")
        c.font = font_body_bold
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.border = border_top_total
        if c_idx in (5, 7):
            c.number_format = int_fmt
        elif c_idx in (6, 8):
            c.number_format = dec_fmt
        elif c_idx in (9, 11):
            c.number_format = pct_fmt
        else:
            c.number_format = curr_fmt

    # Suma de D y Consumo Valor
    c_sum_D = ws2.cell(row=tot_row, column=13, value=f"=SUM(M5:M{tot_row-1})")
    c_sum_D.font = font_body_bold
    c_sum_D.number_format = int_fmt
    c_sum_D.alignment = Alignment(horizontal="right", vertical="center")
    c_sum_D.border = border_top_total

    c_sum_val = ws2.cell(row=tot_row, column=14, value=f"=SUM(N5:N{tot_row-1})")
    c_sum_val.font = font_body_bold
    c_sum_val.number_format = curr_fmt
    c_sum_val.alignment = Alignment(horizontal="right", vertical="center")
    c_sum_val.border = border_top_total

    # =========================================================================
    # PESTAÑA 3: MOTOR MATEMÁTICO SS & ROP (Cálculos Estocásticos)
    # =========================================================================
    ws3 = wb.create_sheet(title=t3_name)
    ws3.views.sheetView[0].showGridLines = True

    t3_title = "Motor Matemático de Stock de Seguridad & Punto de Pedido (ROP)" if is_es else "Safety Stock & Reorder Point (ROP) Mathematical Engine"
    t3_sub = "Modelado estocástico completo (Modelos 1, 2 y 3 convolución), Factor Z, EOQ Wilson y Benchmark vs. Reglas Heurísticas" if is_es else "Complete stochastic modeling (Models 1, 2 and 3 convolution), Z-Factor, Wilson EOQ and Benchmark vs. Heuristic Rules"
    create_header(ws3, t3_title, t3_sub, max_col=17)

    headers_t3_es = [
        "SKU ID", "Descripción", "Clase",
        "Factor Z (CSL)",
        "SS Mod.1 (Dem. Var) [u]", "SS Mod.2 (Plazo Var) [u]", "SS Mod.3 (Integral) [u]",
        "SS Recomendado [u]", "Demanda en Plazo (LTD) [u]", "Punto Pedido (ROP) [u]",
        "Lote Óptimo (EOQ) [u]", "Inversión en SS (€)", "Coste Posesión SS (€/año)",
        "Stock Regla 3 Semanas [u]", "Inversión Regla 3 Semanas (€)", "Capital Liberable (€)",
        "Diagnóstico Operativo"
    ]
    headers_t3_en = [
        "SKU ID", "Description", "Class",
        "Z-Factor (CSL)",
        "SS Mod.1 (Dem. Var) [u]", "SS Mod.2 (LT Var) [u]", "SS Mod.3 (Integral) [u]",
        "Recommended SS [u]", "Lead Time Demand (LTD) [u]", "Reorder Point (ROP) [u]",
        "Wilson EOQ [u]", "SS Capital Investment ($)", "Annual SS Holding Cost ($/yr)",
        "3-Week Rule Stock [u]", "3-Week Rule Capital ($)", "Releasable Capital ($)",
        "Operational Diagnosis"
    ]
    headers_t3 = headers_t3_es if is_es else headers_t3_en

    ws3.row_dimensions[4].height = 32
    fill_navy_custom = PatternFill(fill_type="solid", fgColor=COLOR_NAVY_LIGHT)
    for col_idx, h in enumerate(headers_t3, 1):
        c = ws3.cell(row=4, column=col_idx, value=h)
        c.font = font_tbl_header
        if col_idx <= 3:
            c.fill = fill_med
        elif col_idx <= 11:
            c.fill = fill_blue_accent
        else:
            c.fill = fill_navy_custom
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border_cell

    t3_formula_coords = []
    for i, item in enumerate(SKU_CATALOG):
        r = start_row + i
        ws3.row_dimensions[r].height = 20
        r_t2 = r

        # Col A: SKU
        c_sku = ws3.cell(row=r, column=1, value=f"='{t2_name}'!A{r_t2}")
        c_sku.font = font_body_bold; c_sku.alignment = Alignment(horizontal="center", vertical="center"); c_sku.border = border_cell
        t3_formula_coords.append(c_sku.coordinate)

        # Col B: Descripción
        c_desc = ws3.cell(row=r, column=2, value=f"='{t2_name}'!C{r_t2}")
        c_desc.font = font_body; c_desc.alignment = Alignment(horizontal="left", vertical="center"); c_desc.border = border_cell
        t3_formula_coords.append(c_desc.coordinate)

        # Col C: Clase ABC
        c_abc = ws3.cell(row=r, column=3, value=f"='{t2_name}'!D{r_t2}")
        c_abc.font = font_body_bold; c_abc.alignment = Alignment(horizontal="center", vertical="center"); c_abc.border = border_cell
        t3_formula_coords.append(c_abc.coordinate)

        # Col D: Factor Z = _xlfn.NORM.S.INV(CSL)
        c_z = ws3.cell(row=r, column=4, value=f"=_xlfn.NORM.S.INV('{t2_name}'!I{r_t2})")
        c_z.font = font_body_bold; c_z.number_format = "0.000"; c_z.alignment = Alignment(horizontal="right", vertical="center"); c_z.border = border_cell
        t3_formula_coords.append(c_z.coordinate)

        # Col E: SS Modelo 1 = Z * sigma_d * SQRT(L)
        c_ss1 = ws3.cell(row=r, column=5, value=f"=ROUNDUP(D{r}*'{t2_name}'!F{r_t2}*SQRT('{t2_name}'!G{r_t2}),0)")
        c_ss1.font = font_body; c_ss1.number_format = int_fmt; c_ss1.alignment = Alignment(horizontal="right", vertical="center"); c_ss1.border = border_cell
        t3_formula_coords.append(c_ss1.coordinate)

        # Col F: SS Modelo 2 = Z * d * sigma_L
        c_ss2 = ws3.cell(row=r, column=6, value=f"=ROUNDUP(D{r}*'{t2_name}'!E{r_t2}*'{t2_name}'!H{r_t2},0)")
        c_ss2.font = font_body; c_ss2.number_format = int_fmt; c_ss2.alignment = Alignment(horizontal="right", vertical="center"); c_ss2.border = border_cell
        t3_formula_coords.append(c_ss2.coordinate)

        # Col G: SS Modelo 3 = Z * SQRT(L * sigma_d^2 + d^2 * sigma_L^2)
        c_ss3 = ws3.cell(row=r, column=7, value=f"=ROUNDUP(D{r}*SQRT('{t2_name}'!G{r_t2}*('{t2_name}'!F{r_t2}^2) + ('{t2_name}'!E{r_t2}^2)*('{t2_name}'!H{r_t2}^2)),0)")
        c_ss3.font = font_body_bold; c_ss3.number_format = int_fmt; c_ss3.alignment = Alignment(horizontal="right", vertical="center"); c_ss3.border = border_cell
        t3_formula_coords.append(c_ss3.coordinate)

        # Col H: SS Recomendado = SS3
        c_ss_rec = ws3.cell(row=r, column=8, value=f"=G{r}")
        c_ss_rec.font = font_body_bold; c_ss_rec.number_format = int_fmt; c_ss_rec.alignment = Alignment(horizontal="right", vertical="center"); c_ss_rec.border = border_cell
        t3_formula_coords.append(c_ss_rec.coordinate)

        # Col I: Demanda en Plazo LTD = d * L
        c_ltd = ws3.cell(row=r, column=9, value=f"=ROUND('{t2_name}'!E{r_t2}*'{t2_name}'!G{r_t2},0)")
        c_ltd.font = font_body; c_ltd.number_format = int_fmt; c_ltd.alignment = Alignment(horizontal="right", vertical="center"); c_ltd.border = border_cell
        t3_formula_coords.append(c_ltd.coordinate)

        # Col J: Punto de Pedido ROP = LTD + SS_rec
        c_rop = ws3.cell(row=r, column=10, value=f"=I{r}+H{r}")
        c_rop.font = font_body_bold; c_rop.number_format = int_fmt; c_rop.alignment = Alignment(horizontal="right", vertical="center"); c_rop.border = border_cell
        t3_formula_coords.append(c_rop.coordinate)

        # Col K: EOQ Wilson = SQRT((2 * D * S) / (h * C))
        c_eoq = ws3.cell(row=r, column=11, value=f"=ROUNDUP(SQRT((2*'{t2_name}'!M{r_t2}*'{t2_name}'!L{r_t2})/('{t2_name}'!K{r_t2}*'{t2_name}'!J{r_t2})),0)")
        c_eoq.font = font_body_bold; c_eoq.number_format = int_fmt; c_eoq.alignment = Alignment(horizontal="right", vertical="center"); c_eoq.border = border_cell
        t3_formula_coords.append(c_eoq.coordinate)

        # Col L: Inversión en SS = SS_rec * C
        c_inv_ss = ws3.cell(row=r, column=12, value=f"=H{r}*'{t2_name}'!J{r_t2}")
        c_inv_ss.font = font_body_bold; c_inv_ss.number_format = curr_fmt; c_inv_ss.alignment = Alignment(horizontal="right", vertical="center"); c_inv_ss.border = border_cell
        t3_formula_coords.append(c_inv_ss.coordinate)

        # Col M: Coste Posesión Anual SS = Inversión * h
        c_cost_ss = ws3.cell(row=r, column=13, value=f"=L{r}*'{t2_name}'!K{r_t2}")
        c_cost_ss.font = font_body; c_cost_ss.number_format = curr_fmt; c_cost_ss.alignment = Alignment(horizontal="right", vertical="center"); c_cost_ss.border = border_cell
        t3_formula_coords.append(c_cost_ss.coordinate)

        # Col N: Regla Empírica 3 Semanas (21 días * d)
        c_heur = ws3.cell(row=r, column=14, value=f"=21*'{t2_name}'!E{r_t2}")
        c_heur.font = font_body; c_heur.number_format = int_fmt; c_heur.alignment = Alignment(horizontal="right", vertical="center"); c_heur.border = border_cell
        t3_formula_coords.append(c_heur.coordinate)

        # Col O: Inversión Regla 3 Semanas = Stock_heur * C
        c_inv_heur = ws3.cell(row=r, column=15, value=f"=N{r}*'{t2_name}'!J{r_t2}")
        c_inv_heur.font = font_body; c_inv_heur.number_format = curr_fmt; c_inv_heur.alignment = Alignment(horizontal="right", vertical="center"); c_inv_heur.border = border_cell
        t3_formula_coords.append(c_inv_heur.coordinate)

        # Col P: Capital Liberable = Inversión Heurística - Inversión SS
        c_lib = ws3.cell(row=r, column=16, value=f"=O{r}-L{r}")
        c_lib.font = font_body_bold; c_lib.number_format = curr_fmt; c_lib.alignment = Alignment(horizontal="right", vertical="center"); c_lib.border = border_cell
        t3_formula_coords.append(c_lib.coordinate)

        # Col Q: Diagnóstico Operativo
        if is_es:
            diag_formula = f'=IF(N{r}<H{r}, "⚠️ RIESGO ROTURA", IF(P{r}>10000, "💰 SOBRESTOCK CRÍTICO", "✅ OPTIMIZADO"))'
        else:
            diag_formula = f'=IF(N{r}<H{r}, "⚠️ STOCKOUT RISK", IF(P{r}>10000, "💰 CRITICAL OVERSTOCK", "✅ OPTIMIZED"))'
        c_diag = ws3.cell(row=r, column=17, value=diag_formula)
        c_diag.font = font_body_bold; c_diag.alignment = Alignment(horizontal="center", vertical="center"); c_diag.border = border_cell
        t3_formula_coords.append(c_diag.coordinate)

    # Fila de Totales Tab 3
    ws3.row_dimensions[tot_row].height = 24
    c_tot_t3 = ws3.cell(row=tot_row, column=1, value="TOTALES" if is_es else "TOTALS")
    c_tot_t3.font = font_body_bold; c_tot_t3.alignment = Alignment(horizontal="left", vertical="center"); c_tot_t3.border = border_top_total
    ws3.merge_cells(start_row=tot_row, start_column=1, end_row=tot_row, end_column=3)

    # Medias de Z
    c_z_avg = ws3.cell(row=tot_row, column=4, value=f"=AVERAGE(D5:D{tot_row-1})")
    c_z_avg.font = font_body_bold; c_z_avg.number_format = "0.000"; c_z_avg.alignment = Alignment(horizontal="right", vertical="center"); c_z_avg.border = border_top_total

    # Sumas de SS, LTD, ROP, EOQ
    for c_idx in range(5, 12):
        c = ws3.cell(row=tot_row, column=c_idx, value=f"=SUM({get_column_letter(c_idx)}5:{get_column_letter(c_idx)}{tot_row-1})")
        c.font = font_body_bold; c.number_format = int_fmt; c.alignment = Alignment(horizontal="right", vertical="center"); c.border = border_top_total

    # Sumas Monetarias (L, M, N, O, P)
    for c_idx in (12, 13, 15, 16):
        c = ws3.cell(row=tot_row, column=c_idx, value=f"=SUM({get_column_letter(c_idx)}5:{get_column_letter(c_idx)}{tot_row-1})")
        c.font = font_body_bold; c.number_format = curr_fmt; c.alignment = Alignment(horizontal="right", vertical="center"); c.border = border_top_total

    c_sum_heur_u = ws3.cell(row=tot_row, column=14, value=f"=SUM(N5:N{tot_row-1})")
    c_sum_heur_u.font = font_body_bold; c_sum_heur_u.number_format = int_fmt; c_sum_heur_u.alignment = Alignment(horizontal="right", vertical="center"); c_sum_heur_u.border = border_top_total

    c_empty_diag = ws3.cell(row=tot_row, column=17, value="")
    c_empty_diag.border = border_top_total

    # =========================================================================
    # PESTAÑA 4: TRADE-OFFS DE WORKING CAPITAL (Sensibilidad & Negociación)
    # =========================================================================
    ws4 = wb.create_sheet(title=t4_name)
    ws4.views.sheetView[0].showGridLines = True

    t4_title = "Trade-offs de Working Capital & Optimización C-Level" if is_es else "Working Capital Trade-offs & C-Level Optimization"
    t4_sub = "Curva de sensibilidad del Nivel de Servicio, demostración asintótica exponencial y simulador de impacto de negociación de Lead Time" if is_es else "Service Level sensitivity curve, exponential asymptotic demonstration and Lead Time negotiation simulator"
    create_header(ws4, t4_title, t4_sub, max_col=10)

    # SECCIÓN 1: CURVA DE SENSIBILIDAD NIVEL DE SERVICIO VS INVERSIÓN
    ws4.cell(row=4, column=1, value="1. CURVA ASINTÓTICA: INVERSIÓN EN STOCK DE SEGURIDAD SEGÚN NIVEL DE SERVICIO" if is_es else "1. ASYMPTOTIC CURVE: SAFETY STOCK INVESTMENT VS. SERVICE LEVEL").font = font_section

    headers_s1_es = [
        "Nivel de Servicio (CSL) [%]", "Factor Z Estándar", "Multiplicador vs. Base 95%",
        "Inversión Proyectada en SS (€)", "Incremento Marginal (€)", "Coste Posesión Anual (€)",
        "Diagnóstico de Comportamiento Asintótico"
    ]
    headers_s1_en = [
        "Service Level (CSL) [%]", "Standard Z-Factor", "Multiplier vs. 95% Base",
        "Projected SS Investment ($)", "Marginal Capital Increment ($)", "Annual Holding Cost ($)",
        "Asymptotic Behavior Diagnosis"
    ]
    headers_s1 = headers_s1_es if is_es else headers_s1_en

    ws4.row_dimensions[5].height = 28
    for col_idx, h in enumerate(headers_s1, 1):
        c = ws4.cell(row=5, column=col_idx, value=h)
        c.font = font_tbl_header
        c.fill = fill_blue_accent
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border_cell

    csl_levels = [0.850, 0.900, 0.950, 0.970, 0.980, 0.990, 0.995, 0.999]
    diag_csl_es = [
        "Mínima inversión, pero alto riesgo de rotura (15% ciclos sin stock)",
        "Colchón moderado para productos no críticos (Clase C)",
        "Estándar corporativo de referencia equilibrado (Clase B)",
        "Zona de alta disponibilidad con incremento de capital contenido",
        "Estándar directivo para referencias críticas (Clase A)",
        "Frontera de inmovilización severa: +41% de capital sobre base 95%",
        "Duplicación de capital inmovilizado (+56%): Ineficiencia financiera",
        "Coste asintótico prohibitivo (+88% capital): Rendimientos decrecientes"
    ]
    diag_csl_en = [
        "Minimum capital, but severe stockout risk (15% cycles with shortage)",
        "Moderate buffer for non-critical references (Class C)",
        "Balanced corporate benchmark standard (Class B)",
        "High availability zone with controlled working capital stretch",
        "Executive standard for critical references (Class A)",
        "Severe capital lockup boundary: +41% extra capital vs. 95% base",
        "Doubled capital lockup (+56%): Severe financial carrying inefficiency",
        "Prohibitive asymptotic cost (+88% capital): Law of diminishing returns"
    ]
    diag_csl = diag_csl_es if is_es else diag_csl_en
    t4_input_coords = []
    for idx, (csl_val, diag_text) in enumerate(zip(csl_levels, diag_csl)):
        r = 6 + idx
        ws4.row_dimensions[r].height = 20

        # CSL (Input desbloqueado para que el directivo pueda simular niveles custom)
        c_csl = ws4.cell(row=r, column=1, value=csl_val)
        c_csl.font = font_input; c_csl.number_format = pct_fmt; c_csl.alignment = Alignment(horizontal="center", vertical="center"); c_csl.border = border_cell
        c_csl.fill = fill_input; c_csl.protection = Protection(locked=False)
        t4_input_coords.append(c_csl.coordinate)

        # Z = _xlfn.NORM.S.INV(CSL)
        c_z = ws4.cell(row=r, column=2, value=f"=_xlfn.NORM.S.INV(A{r})")
        c_z.font = font_body_bold; c_z.number_format = "0.000"; c_z.alignment = Alignment(horizontal="right", vertical="center"); c_z.border = border_cell

        # Multiplicador vs 95% (Fila 8 es 95%)
        c_mult = ws4.cell(row=r, column=3, value=f"=B{r}/B8")
        c_mult.font = font_body; c_mult.number_format = "0.00x"; c_mult.alignment = Alignment(horizontal="right", vertical="center"); c_mult.border = border_cell

        # Inversión Proyectada = Inversión Total Base (Tab3!L_tot) * (Z / Z_avg)
        c_inv = ws4.cell(row=r, column=4, value=f"='{t3_name}'!L{tot_row}*(B{r}/'{t3_name}'!D{tot_row})")
        c_inv.font = font_body_bold; c_inv.number_format = curr_fmt; c_inv.alignment = Alignment(horizontal="right", vertical="center"); c_inv.border = border_cell

        # Incremento Marginal vs fila anterior
        if idx == 0:
            c_inc = ws4.cell(row=r, column=5, value=0)
        else:
            c_inc = ws4.cell(row=r, column=5, value=f"=D{r}-D{r-1}")
        c_inc.font = font_body; c_inc.number_format = curr_fmt; c_inc.alignment = Alignment(horizontal="right", vertical="center"); c_inc.border = border_cell

        # Coste Posesión Anual = Inversión * h_medio (Tab2!K_tot)
        c_hold = ws4.cell(row=r, column=6, value=f"=D{r}*'{t2_name}'!K{tot_row}")
        c_hold.font = font_body; c_hold.number_format = curr_fmt; c_hold.alignment = Alignment(horizontal="right", vertical="center"); c_hold.border = border_cell

        # Diagnóstico
        c_d = ws4.cell(row=r, column=7, value=diag_text)
        c_d.font = font_body; c_d.alignment = Alignment(horizontal="left", vertical="center"); c_d.border = border_cell
        if csl_val >= 0.995:
            c_d.fill = fill_red
        elif csl_val == 0.980 or csl_val == 0.950:
            c_d.fill = fill_green

    # SECCIÓN 2: SIMULADOR DE IMPACTO DE NEGOCIACIÓN DE LEAD TIME & SLA
    sec2_row = 16
    ws4.cell(row=sec2_row, column=1, value="2. SIMULADOR DE IMPACTO DE NEGOCIACIÓN DE PROVEEDORES (COMPRESIÓN DE L Y σL)" if is_es else "2. SUPPLIER NEGOTIATION IMPACT SIMULATOR (LEAD TIME & VARIABILITY REDUCTION)").font = font_section

    headers_s2_es = [
        "Escenario de Negociación", "Lead Time Medio (L)", "Variabilidad Plazo (σL)",
        "Inversión Requerida en SS (€)", "Capital de Trabajo Liberado (€)", "Ahorro Anual de Mantenimiento (€)",
        "Recomendación para Mesa de Negociación"
    ]
    headers_s2_en = [
        "Negotiation Scenario", "Mean Lead Time (L)", "Lead Time Std Dev (σL)",
        "Required SS Investment ($)", "Working Capital Released ($)", "Annual Carrying Cost Savings ($)",
        "Negotiation Table Strategic Action"
    ]
    headers_s2 = headers_s2_es if is_es else headers_s2_en

    ws4.row_dimensions[sec2_row+1].height = 28
    for col_idx, h in enumerate(headers_s2, 1):
        c = ws4.cell(row=sec2_row+1, column=col_idx, value=h)
        c.font = font_tbl_header
        c.fill = fill_med
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border_cell

    scenarios_es = [
        ("Situación Actual (Línea Base)", "100% (Sin cambios)", "100% (Sin cambios)", 1.00, "Referencia operativa actual del catálogo"),
        ("Compresión de Lead Time (-30%)", "70% (-30% de reducción)", "100% (Variabilidad actual)", 0.84, "Negociar almacén avanzado del proveedor o cross-docking"),
        ("Estabilidad / Puntualidad SLA (-50% σL)", "100% (Plazo actual)", "50% (Puntualidad garantizada)", 0.76, "Establecer penalizaciones por incumplimiento de ventana de entrega"),
        ("Alianza Estratégica Integral (-30% L & -50% σL)", "70% (-30% de reducción)", "50% (Puntualidad garantizada)", 0.62, "VMI (Vendor Managed Inventory) o acuerdo marco preferente C-Level")
    ]
    scenarios_en = [
        ("Current Baseline Situation", "100% (No changes)", "100% (No changes)", 1.00, "Current operational catalog benchmark"),
        ("Lead Time Compression (-30%)", "70% (-30% reduction)", "100% (Current variability)", 0.84, "Negotiate supplier buffer stock or regional cross-docking"),
        ("SLA Punctuality Guarantee (-50% σL)", "100% (Current mean)", "50% (Guaranteed delivery window)", 0.76, "Institute SLA penalty clauses for late delivery deviations"),
        ("Comprehensive Strategic Alliance (-30% L & -50% σL)", "70% (-30% reduction)", "50% (Guaranteed delivery window)", 0.62, "Full Vendor Managed Inventory (VMI) or executive strategic contract")
    ]
    scenarios = scenarios_es if is_es else scenarios_en

    for idx, (scen_name, l_desc, sigl_desc, factor, action_desc) in enumerate(scenarios):
        r = sec2_row + 2 + idx
        ws4.row_dimensions[r].height = 22

        c_name = ws4.cell(row=r, column=1, value=scen_name)
        c_name.font = font_body_bold; c_name.alignment = Alignment(horizontal="left", vertical="center"); c_name.border = border_cell

        c_l = ws4.cell(row=r, column=2, value=l_desc)
        c_l.font = font_body; c_l.alignment = Alignment(horizontal="center", vertical="center"); c_l.border = border_cell

        c_sig = ws4.cell(row=r, column=3, value=sigl_desc)
        c_sig.font = font_body; c_sig.alignment = Alignment(horizontal="center", vertical="center"); c_sig.border = border_cell

        # Inversión Requerida = Inversión Base * factor
        c_inv_scen = ws4.cell(row=r, column=4, value=f"='{t3_name}'!L{tot_row}*{factor}")
        c_inv_scen.font = font_body_bold; c_inv_scen.number_format = curr_fmt; c_inv_scen.alignment = Alignment(horizontal="right", vertical="center"); c_inv_scen.border = border_cell

        # Capital Liberado = Inversión Base - Inversión Escenario
        c_lib_scen = ws4.cell(row=r, column=5, value=f"='{t3_name}'!L{tot_row}-D{r}")
        c_lib_scen.font = font_body_bold; c_lib_scen.number_format = curr_fmt; c_lib_scen.alignment = Alignment(horizontal="right", vertical="center"); c_lib_scen.border = border_cell

        # Ahorro Anual = Capital Liberado * h_medio
        c_ahorro = ws4.cell(row=r, column=6, value=f"=E{r}*'{t2_name}'!K{tot_row}")
        c_ahorro.font = font_body_bold; c_ahorro.number_format = curr_fmt; c_ahorro.alignment = Alignment(horizontal="right", vertical="center"); c_ahorro.border = border_cell

        # Recomendación
        c_rec = ws4.cell(row=r, column=7, value=action_desc)
        c_rec.font = font_body; c_rec.alignment = Alignment(horizontal="left", vertical="center"); c_rec.border = border_cell
        if factor < 1.00:
            c_rec.fill = fill_green

    # =========================================================================
    # PESTAÑA 1: DASHBOARD EJECUTIVO (KPIs, Sawtooth Chart & ABC Breakdown)
    # =========================================================================
    ws1 = wb.create_sheet(title=t1_name, index=0)
    ws1.views.sheetView[0].showGridLines = True

    t1_title = "Cuadro de Mando Ejecutivo: Stock de Seguridad & ROP" if is_es else "Executive Dashboard: Safety Stock & Reorder Point (ROP)"
    t1_sub = "Optimización de Inventario, Nivel de Servicio & Working Capital C-Level (Estándar APICS / MIT CTL)" if is_es else "Inventory Optimization, Service Level & C-Level Working Capital (APICS / MIT CTL Standard)"
    create_header(ws1, t1_title, t1_sub, max_col=13)

    # FILA DE 5 KPI CARDS EJECUTIVAS (Filas 4 a 6)
    kpi_configs_es = [
        ("INVERSIÓN STOCK SEGURIDAD", f"='{t3_name}'!L{tot_row}", curr_fmt, "Capital de protección estocástica"),
        ("NIVEL DE SERVICIO PONDERADO", f"='{t2_name}'!I{tot_row}", pct_fmt, "CSL medio objetivo"),
        ("PROBABILIDAD ROTURA (1 - CSL)", f"=1-D5", pct_fmt, "Riesgo de ciclo sin stock"),
        ("CAPITAL LIBERABLE ESTIMADO", f"='{t3_name}'!P{tot_row}", curr_fmt, "Superando reglas empíricas 3 sem"),
        ("SKUs EN RIESGO DE ROTURA", f'=COUNTIF(\'{t3_name}\'!Q5:Q{tot_row-1}, "*RIESGO ROTURA*")', int_fmt, "Infradotados por regla heurística")
    ]
    kpi_configs_en = [
        ("TOTAL SAFETY STOCK CAPITAL", f"='{t3_name}'!L{tot_row}", curr_fmt, "Stochastic protection buffer"),
        ("WEIGHTED SERVICE LEVEL", f"='{t2_name}'!I{tot_row}", pct_fmt, "Target portfolio CSL"),
        ("STOCKOUT PROBABILITY (1-CSL)", f"=1-D5", pct_fmt, "Stockout risk per replenishment cycle"),
        ("RELEASABLE WORKING CAPITAL", f"='{t3_name}'!P{tot_row}", curr_fmt, "Replacing naive 3-week heuristic"),
        ("SKUs AT STOCKOUT RISK", f'=COUNTIF(\'{t3_name}\'!Q5:Q{tot_row-1}, "*STOCKOUT RISK*")', int_fmt, "Under-buffered by empirical rules")
    ]
    kpi_configs = kpi_configs_es if is_es else kpi_configs_en

    # Disposición de las 5 tarjetas ocupando columnas B a K (2 columnas por tarjeta)
    col_starts = [2, 4, 6, 8, 10]
    ws1.row_dimensions[4].height = 16
    ws1.row_dimensions[5].height = 28
    ws1.row_dimensions[6].height = 16

    for (title_kpi, form_kpi, fmt_kpi, sub_kpi), col_s in zip(kpi_configs, col_starts):
        col_e = col_s + 1
        ws1.merge_cells(start_row=4, start_column=col_s, end_row=4, end_column=col_e)
        c_top = ws1.cell(row=4, column=col_s, value=title_kpi)
        c_top.font = font_card_title; c_top.alignment = Alignment(horizontal="center", vertical="center"); c_top.fill = fill_card

        ws1.merge_cells(start_row=5, start_column=col_s, end_row=5, end_column=col_e)
        c_val = ws1.cell(row=5, column=col_s, value=form_kpi)
        c_val.font = font_card_val; c_val.number_format = fmt_kpi; c_val.alignment = Alignment(horizontal="center", vertical="center"); c_val.fill = fill_card

        ws1.merge_cells(start_row=6, start_column=col_s, end_row=6, end_column=col_e)
        c_sub = ws1.cell(row=6, column=col_s, value=sub_kpi)
        c_sub.font = font_card_sub; c_sub.alignment = Alignment(horizontal="center", vertical="center"); c_sub.fill = fill_card

        # Aplicar borde a la tarjeta
        for r_card in range(4, 7):
            for c_card in range(col_s, col_e + 1):
                cell_box = ws1.cell(row=r_card, column=c_card)
                b_left = border_thick_side if c_card == col_s else thin_border_side
                b_right = thin_border_side if c_card == col_e else Side(style=None)
                b_top = thin_border_side if r_card == 4 else Side(style=None)
                b_bottom = thin_border_side if r_card == 6 else Side(style=None)
                cell_box.border = Border(left=b_left, right=b_right, top=b_top, bottom=b_bottom)

    # FILA 8: SEPARADOR Y TÍTULOS DE SECCIÓN
    ws1.cell(row=8, column=2, value="ANÁLISIS DE DISTRIBUCIÓN ABC DEL PORTFOLIO" if is_es else "PORTFOLIO ABC STRATIFICATION ANALYSIS").font = font_section
    ws1.cell(row=8, column=9, value="SIMULACIÓN DINÁMICA DEL CICLO DE REABASTECIMIENTO (SAWTOOTH)" if is_es else "DYNAMIC REPLENISHMENT CYCLE SIMULATION (SAWTOOTH)").font = font_section

    # TABLA RESUMEN ABC (Columnas B a F, Filas 10 a 15)
    headers_abc_es = ["Clase", "Nº SKUs", "% Catálogo", "Consumo Valor Anual (€)", "% Valor Total", "Inversión en SS (€)"]
    headers_abc_en = ["Class", "SKU Count", "% Catalog", "Annual Consumption ($)", "% Total Value", "SS Investment ($)"]
    headers_abc = headers_abc_es if is_es else headers_abc_en

    ws1.row_dimensions[9].height = 24
    for idx_c, h in enumerate(headers_abc, 2):
        c = ws1.cell(row=9, column=idx_c, value=h)
        c.font = font_tbl_header
        c.fill = fill_med
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border_cell

    abc_classes = ["A", "B", "C"]
    for idx_cls, cls_name in enumerate(abc_classes):
        r = 10 + idx_cls
        ws1.row_dimensions[r].height = 20

        # Clase
        c_cl = ws1.cell(row=r, column=2, value=f"Clase {cls_name}" if is_es else f"Class {cls_name}")
        c_cl.font = font_body_bold; c_cl.alignment = Alignment(horizontal="center", vertical="center"); c_cl.border = border_cell
        if cls_name == "A":
            c_cl.fill = fill_green
        elif cls_name == "B":
            c_cl.fill = fill_amber
        else:
            c_cl.fill = fill_card

        # Nº SKUs
        c_n = ws1.cell(row=r, column=3, value=f'=COUNTIF(\'{t2_name}\'!$D$5:$D${tot_row-1}, "{cls_name}")')
        c_n.font = font_body; c_n.number_format = int_fmt; c_n.alignment = Alignment(horizontal="right", vertical="center"); c_n.border = border_cell

        # % Catálogo
        c_pct_cat = ws1.cell(row=r, column=4, value=f"=C{r}/COUNTIF('{t2_name}'!$D$5:$D${tot_row-1}, \"<>\")")
        c_pct_cat.font = font_body; c_pct_cat.number_format = pct_fmt; c_pct_cat.alignment = Alignment(horizontal="right", vertical="center"); c_pct_cat.border = border_cell

        # Consumo Valor Anual
        c_cons = ws1.cell(row=r, column=5, value=f'=SUMIF(\'{t2_name}\'!$D$5:$D${tot_row-1}, "{cls_name}", \'{t2_name}\'!$N$5:$N${tot_row-1})')
        c_cons.font = font_body_bold; c_cons.number_format = curr_fmt; c_cons.alignment = Alignment(horizontal="right", vertical="center"); c_cons.border = border_cell

        # % Valor Total
        c_pct_val = ws1.cell(row=r, column=6, value=f"=E{r}/SUM('{t2_name}'!$N$5:$N${tot_row-1})")
        c_pct_val.font = font_body_bold; c_pct_val.number_format = pct_fmt; c_pct_val.alignment = Alignment(horizontal="right", vertical="center"); c_pct_val.border = border_cell

        # Inversión en SS
        c_ss_val = ws1.cell(row=r, column=7, value=f'=SUMIF(\'{t3_name}\'!$C$5:$C${tot_row-1}, "{cls_name}", \'{t3_name}\'!$L$5:$L${tot_row-1})')
        c_ss_val.font = font_body_bold; c_ss_val.number_format = curr_fmt; c_ss_val.alignment = Alignment(horizontal="right", vertical="center"); c_ss_val.border = border_cell

    # Fila Total ABC (Fila 13)
    r_abc_tot = 13
    ws1.row_dimensions[r_abc_tot].height = 22
    c_tot_lbl = ws1.cell(row=r_abc_tot, column=2, value="TOTAL")
    c_tot_lbl.font = font_body_bold; c_tot_lbl.alignment = Alignment(horizontal="center", vertical="center"); c_tot_lbl.border = border_top_total

    c_tot_skus = ws1.cell(row=r_abc_tot, column=3, value="=SUM(C10:C12)")
    c_tot_skus.font = font_body_bold; c_tot_skus.number_format = int_fmt; c_tot_skus.alignment = Alignment(horizontal="right", vertical="center"); c_tot_skus.border = border_top_total

    c_tot_pct_c = ws1.cell(row=r_abc_tot, column=4, value="=SUM(D10:D12)")
    c_tot_pct_c.font = font_body_bold; c_tot_pct_c.number_format = pct_fmt; c_tot_pct_c.alignment = Alignment(horizontal="right", vertical="center"); c_tot_pct_c.border = border_top_total

    c_tot_cons = ws1.cell(row=r_abc_tot, column=5, value="=SUM(E10:E12)")
    c_tot_cons.font = font_body_bold; c_tot_cons.number_format = curr_fmt; c_tot_cons.alignment = Alignment(horizontal="right", vertical="center"); c_tot_cons.border = border_top_total

    c_tot_pct_v = ws1.cell(row=r_abc_tot, column=6, value="=SUM(F10:F12)")
    c_tot_pct_v.font = font_body_bold; c_tot_pct_v.number_format = pct_fmt; c_tot_pct_v.alignment = Alignment(horizontal="right", vertical="center"); c_tot_pct_v.border = border_top_total

    c_tot_ss = ws1.cell(row=r_abc_tot, column=7, value="=SUM(G10:G12)")
    c_tot_ss.font = font_body_bold; c_tot_ss.number_format = curr_fmt; c_tot_ss.alignment = Alignment(horizontal="right", vertical="center"); c_tot_ss.border = border_top_total

    # =========================================================================
    # PANEL DE CONTROL Y PARÁMETROS DEL SKU MODELADO EN LA SIMULACIÓN (Filas 9 a 14)
    # =========================================================================
    t1_dec_coords = []
    t1_input_coords = []

    # Fila 9: Banner de sección de simulación
    ws1.merge_cells("I9:M9")
    c_panel_hdr = ws1.cell(row=9, column=9)
    c_panel_hdr.value = "CONTROL DEL SKU MODELADO EN LA SIMULACIÓN" if is_es else "BENCHMARK SKU SIMULATION CONTROL"
    c_panel_hdr.font = font_tbl_header
    c_panel_hdr.fill = fill_dark
    c_panel_hdr.alignment = Alignment(horizontal="center", vertical="center")
    t1_dec_coords.append("I9")

    # Fila 10: Selector interactivo de SKU y descripción del producto
    ws1.row_dimensions[10].height = 22

    # Celda I10: Etiqueta SKU
    c_i10 = ws1.cell(row=10, column=9, value="SKU Simulado:" if is_es else "Simulated SKU:")
    c_i10.font = font_body_bold; c_i10.alignment = Alignment(horizontal="right", vertical="center"); c_i10.border = border_cell
    c_i10.fill = PatternFill(fill_type="solid", fgColor="F8FAFC")
    t1_dec_coords.append("I10")

    # Celda J10: Input de SKU (DESBLOQUEADA, fondo blanco puro #FFFFFF)
    c_j10 = ws1.cell(row=10, column=10, value="SKU-1001")
    c_j10.font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_BLUE_ACCENT)
    c_j10.fill = PatternFill(fill_type="solid", fgColor="FFFFFF")
    c_j10.alignment = Alignment(horizontal="center", vertical="center")
    c_j10.border = Border(left=Side(style="medium", color=COLOR_BLUE_ACCENT), right=Side(style="medium", color=COLOR_BLUE_ACCENT),
                          top=Side(style="medium", color=COLOR_BLUE_ACCENT), bottom=Side(style="medium", color=COLOR_BLUE_ACCENT))
    c_j10.protection = Protection(locked=False)
    t1_input_coords.append("J10")

    # Celda K10: Etiqueta Descripción
    c_k10 = ws1.cell(row=10, column=11, value="Descripción:" if is_es else "Description:")
    c_k10.font = font_body_bold; c_k10.alignment = Alignment(horizontal="right", vertical="center"); c_k10.border = border_cell
    c_k10.fill = PatternFill(fill_type="solid", fgColor="F8FAFC")
    t1_dec_coords.append("K10")

    # Celdas L10:M10 fusionadas con VLOOKUP de descripción
    ws1.merge_cells("L10:M10")
    c_l10 = ws1.cell(row=10, column=12, value=f"=VLOOKUP(J10, '{t2_name}'!$A$5:$N$39, 3, FALSE)")
    c_l10.font = font_body; c_l10.alignment = Alignment(horizontal="left", vertical="center"); c_l10.border = border_cell
    c_l10.fill = PatternFill(fill_type="solid", fgColor="F1F5F9")
    t1_dec_coords.extend(["L10", "M10"])

    # Fila 11: Parámetros operativos de entrada (d, L, CSL)
    ws1.row_dimensions[11].height = 20

    c_i11 = ws1.cell(row=11, column=9, value="Demanda Media (d):" if is_es else "Mean Demand (d):")
    c_i11.font = font_body; c_i11.alignment = Alignment(horizontal="right", vertical="center"); c_i11.border = border_cell
    c_i11.fill = PatternFill(fill_type="solid", fgColor="F8FAFC")
    t1_dec_coords.append("I11")

    c_j11 = ws1.cell(row=11, column=10, value=f"=VLOOKUP(J10, '{t2_name}'!$A$5:$N$39, 5, FALSE)")
    c_j11.font = font_body_bold; c_j11.number_format = int_fmt; c_j11.alignment = Alignment(horizontal="center", vertical="center"); c_j11.border = border_cell
    c_j11.fill = PatternFill(fill_type="solid", fgColor="F1F5F9")

    c_k11 = ws1.cell(row=11, column=11, value="Lead Time Medio (L):" if is_es else "Mean Lead Time (L):")
    c_k11.font = font_body; c_k11.alignment = Alignment(horizontal="right", vertical="center"); c_k11.border = border_cell
    c_k11.fill = PatternFill(fill_type="solid", fgColor="F8FAFC")
    t1_dec_coords.append("K11")

    c_l11 = ws1.cell(row=11, column=12, value=f"=VLOOKUP(J10, '{t2_name}'!$A$5:$N$39, 7, FALSE)")
    c_l11.font = font_body_bold; c_l11.number_format = int_fmt; c_l11.alignment = Alignment(horizontal="center", vertical="center"); c_l11.border = border_cell
    c_l11.fill = PatternFill(fill_type="solid", fgColor="F1F5F9")

    c_m11 = ws1.cell(row=11, column=13, value=f"=VLOOKUP(J10, '{t2_name}'!$A$5:$N$39, 9, FALSE)")
    c_m11.font = font_body_bold; c_m11.number_format = pct_fmt; c_m11.alignment = Alignment(horizontal="center", vertical="center"); c_m11.border = border_cell
    c_m11.fill = PatternFill(fill_type="solid", fgColor="F1F5F9")

    # Fila 12: Cabeceras del Cuadro de Mando de Umbrales de Inventario
    ws1.row_dimensions[12].height = 20
    headers_scorecard_es = [
        "Lote de Pedido (EOQ)", "PUNTO DE PEDIDO (ROP)", "STOCK SEGURIDAD (SS)",
        "Nivel Servicio (CSL)", "Demanda en Plazo (LTD)"
    ]
    headers_scorecard_en = [
        "Order Quantity (EOQ)", "REORDER POINT (ROP)", "SAFETY STOCK (SS)",
        "Target Service (CSL)", "Lead Time Demand (LTD)"
    ]
    headers_sc = headers_scorecard_es if is_es else headers_scorecard_en
    fills_sc_hdr = [
        PatternFill(fill_type="solid", fgColor="F1F5F9"),
        PatternFill(fill_type="solid", fgColor=COLOR_AMBER_BG),
        PatternFill(fill_type="solid", fgColor=COLOR_GREEN_BG),
        PatternFill(fill_type="solid", fgColor="F1F5F9"),
        PatternFill(fill_type="solid", fgColor="F1F5F9")
    ]
    fonts_sc_hdr = [
        Font(name=FONT_NAME, size=8.5, bold=True, color="64748B"),
        Font(name=FONT_NAME, size=8.5, bold=True, color=COLOR_AMBER_TEXT),
        Font(name=FONT_NAME, size=8.5, bold=True, color=COLOR_GREEN_TEXT),
        Font(name=FONT_NAME, size=8.5, bold=True, color="64748B"),
        Font(name=FONT_NAME, size=8.5, bold=True, color="64748B")
    ]

    for c_offset, (h_text, f_fill, f_font) in enumerate(zip(headers_sc, fills_sc_hdr, fonts_sc_hdr)):
        col_target = 9 + c_offset
        c = ws1.cell(row=12, column=col_target, value=h_text)
        c.font = f_font; c.fill = f_fill; c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = border_cell
        t1_dec_coords.append(c.coordinate)

    # Fila 13: Valores calculados de los umbrales para el SKU seleccionado
    ws1.row_dimensions[13].height = 24

    # Celda I13: EOQ
    c_i13 = ws1.cell(row=13, column=9, value=f"=VLOOKUP(J10, '{t3_name}'!$A$5:$K$39, 11, FALSE)")
    c_i13.font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_NAVY_DARK); c_i13.number_format = int_fmt
    c_i13.alignment = Alignment(horizontal="center", vertical="center"); c_i13.border = border_cell
    c_i13.fill = PatternFill(fill_type="solid", fgColor="F1F5F9")

    # Celda J13: ROP (Punto de Pedido) -> Referencia para columna K
    c_j13 = ws1.cell(row=13, column=10, value=f"=VLOOKUP(J10, '{t3_name}'!$A$5:$J$39, 10, FALSE)")
    c_j13.font = Font(name=FONT_NAME, size=11, bold=True, color="B45309"); c_j13.number_format = int_fmt
    c_j13.alignment = Alignment(horizontal="center", vertical="center")
    c_j13.border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=Side(style="medium", color=COLOR_AMBER_BORDER))
    c_j13.fill = PatternFill(fill_type="solid", fgColor="FEF3C7")
    t1_dec_coords.append("J13")

    # Celda K13: SS (Stock de Seguridad) -> Referencia para columna L
    c_k13 = ws1.cell(row=13, column=11, value=f"=VLOOKUP(J10, '{t3_name}'!$A$5:$H$39, 8, FALSE)")
    c_k13.font = Font(name=FONT_NAME, size=11, bold=True, color="047857"); c_k13.number_format = int_fmt
    c_k13.alignment = Alignment(horizontal="center", vertical="center")
    c_k13.border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=Side(style="medium", color=COLOR_GREEN_BORDER))
    c_k13.fill = PatternFill(fill_type="solid", fgColor="D1FAE5")
    t1_dec_coords.append("K13")

    # Celda L13: CSL
    c_l13 = ws1.cell(row=13, column=12, value=f"=VLOOKUP(J10, '{t2_name}'!$A$5:$N$39, 9, FALSE)")
    c_l13.font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_NAVY_DARK); c_l13.number_format = pct_fmt
    c_l13.alignment = Alignment(horizontal="center", vertical="center"); c_l13.border = border_cell
    c_l13.fill = PatternFill(fill_type="solid", fgColor="F1F5F9")

    # Celda M13: LTD (Demanda en Plazo)
    c_m13 = ws1.cell(row=13, column=13, value=f"=VLOOKUP(J10, '{t3_name}'!$A$5:$I$39, 9, FALSE)")
    c_m13.font = Font(name=FONT_NAME, size=11, bold=True, color=COLOR_NAVY_DARK); c_m13.number_format = int_fmt
    c_m13.alignment = Alignment(horizontal="center", vertical="center"); c_m13.border = border_cell
    c_m13.fill = PatternFill(fill_type="solid", fgColor="F1F5F9")

    # Fila 14: Nota técnica aclaratoria
    ws1.row_dimensions[14].height = 18
    ws1.merge_cells("I14:M14")
    c_note = ws1.cell(row=14, column=9)
    c_note.value = ("Nota técnica: Las columnas ROP y SS proyectan los umbrales constantes basales del SKU ($J$13 y $K$13) para trazar las líneas horizontales del gráfico. La columna Estado detalla cada fase del ciclo."
                    if is_es else
                    "Technical note: ROP and SS columns project the constant benchmark thresholds of the SKU ($J$13 and $K$13) to plot horizontal reference lines. Operational Event details cycle phases.")
    c_note.font = Font(name=FONT_NAME, size=8, italic=True, color="64748B")
    c_note.fill = PatternFill(fill_type="solid", fgColor="F8FAFC")
    c_note.alignment = Alignment(horizontal="center", vertical="center")
    c_note.border = border_cell
    t1_dec_coords.extend(["I14", "J14", "K14", "L14", "M14"])

    # =========================================================================
    # TABLA DE DATOS PARA EL GRÁFICO DIENTE DE SIERRA (Filas 15 a 46, Cols I a M)
    # =========================================================================
    ws1.row_dimensions[15].height = 30

    # Cabeceras de tabla con alto contraste visual (Slate 900, Azul 600, Ámbar 600, Verde 600, Slate 800)
    headers_sim_es = [
        ("Día del Ciclo [t]", COLOR_NAVY_DARK),
        ("Inventario Físico (u)", COLOR_BLUE_ACCENT),
        ("Punto de Pedido (ROP) [u]", "D97706"),   # Ámbar oscuro nítido
        ("Stock de Seguridad (SS) [u]", "059669"), # Esmeralda oscuro nítido
        ("Estado Operativo del Ciclo", COLOR_NAVY_MED)
    ]
    headers_sim_en = [
        ("Cycle Day [t]", COLOR_NAVY_DARK),
        ("Physical Stock (u)", COLOR_BLUE_ACCENT),
        ("Reorder Point (ROP) [u]", "D97706"),
        ("Safety Stock (SS) [u]", "059669"),
        ("Cycle Operational Event", COLOR_NAVY_MED)
    ]
    headers_sim = headers_sim_es if is_es else headers_sim_en

    for c_offset, (h_title, h_bg) in enumerate(headers_sim):
        col_target = 9 + c_offset
        c = ws1.cell(row=15, column=col_target, value=h_title)
        c.font = font_tbl_header
        c.fill = PatternFill(fill_type="solid", fgColor=h_bg)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border_cell
        t1_dec_coords.append(c.coordinate)

    # 31 Días de Simulación (Días 0 a 30)
    # Col I: Día
    # Col J: Inventario Físico (calculado con SS=$K$13 y EOQ=$I$13)
    # Col K: Punto de Pedido ROP (referencia constante =$J$13 para alimentar línea horizontal del gráfico)
    # Col L: Stock de Seguridad SS (referencia constante =$K$13 para alimentar línea basal del gráfico)
    # Col M: Estado Operativo del Ciclo (dinámico según nivel físico vs ROP y momentos de arriba de pedido)
    for day_i in range(31):
        r_sim = 16 + day_i
        ws1.row_dimensions[r_sim].height = 20

        # Día [t]
        c_day = ws1.cell(row=r_sim, column=9, value=day_i)
        c_day.font = font_body; c_day.alignment = Alignment(horizontal="center", vertical="center"); c_day.border = border_cell

        # Inventario Físico [u]
        inv_formula = f"=IF(I{r_sim}<15, $K$13 + $I$13 - I{r_sim}*($I$13/15), $K$13 + $I$13 - (I{r_sim}-15)*($I$13/15))"
        c_inv_sim = ws1.cell(row=r_sim, column=10, value=inv_formula)
        c_inv_sim.font = font_body_bold; c_inv_sim.number_format = int_fmt; c_inv_sim.alignment = Alignment(horizontal="right", vertical="center"); c_inv_sim.border = border_cell

        # Umbral ROP (Línea de Referencia para el Gráfico Diente de Sierra)
        c_rop_sim = ws1.cell(row=r_sim, column=11, value="=$J$13")
        c_rop_sim.font = font_body; c_rop_sim.number_format = int_fmt; c_rop_sim.alignment = Alignment(horizontal="right", vertical="center"); c_rop_sim.border = border_cell

        # Colchón SS (Línea de Referencia Basal para el Gráfico Diente de Sierra)
        c_ss_sim = ws1.cell(row=r_sim, column=12, value="=$K$13")
        c_ss_sim.font = font_body; c_ss_sim.number_format = int_fmt; c_ss_sim.alignment = Alignment(horizontal="right", vertical="center"); c_ss_sim.border = border_cell

        # Estado Operativo del Ciclo
        if is_es:
            status_formula = f'=IF(I{r_sim}=0, "📦 Stock Máximo Inicial (SS + EOQ)", IF(OR(I{r_sim}=15, I{r_sim}=30), "🟢 Arribo de Pedido (+EOQ)", IF(J{r_sim}<=K{r_sim}, "🔴 Disparo Pedido (Stock ≤ ROP)", "⚪ Consumo Ordinario")))'
        else:
            status_formula = f'=IF(I{r_sim}=0, "📦 Initial Max Stock (SS + EOQ)", IF(OR(I{r_sim}=15, I{r_sim}=30), "🟢 Order Arrival (+EOQ)", IF(J{r_sim}<=K{r_sim}, "🔴 Order Trigger (Stock ≤ ROP)", "⚪ Normal Consumption")))'
        c_status = ws1.cell(row=r_sim, column=13, value=status_formula)
        c_status.font = font_body; c_status.alignment = Alignment(horizontal="left", vertical="center"); c_status.border = border_cell

    # =========================================================================
    # GRÁFICO DIENTE DE SIERRA OPENPYXL
    # =========================================================================
    chart_sawtooth = LineChart()
    chart_sawtooth.title = "Dinámica del Ciclo Diente de Sierra (Sawtooth) • SKU Modelo" if is_es else "Sawtooth Cycle Dynamics • Benchmark SKU"
    chart_sawtooth.style = 2  # Estilo limpio y moderno sin bordes negros ni compresión de ejes
    chart_sawtooth.y_axis.title = "Unidades en Inventario" if is_es else "Inventory Units"
    chart_sawtooth.x_axis.title = "Días del Ciclo de Reabastecimiento" if is_es else "Replenishment Cycle Days"
    chart_sawtooth.width = 19.5
    chart_sawtooth.height = 11.5

    data_sawtooth = Reference(ws1, min_col=10, min_row=15, max_col=12, max_row=46)
    cats_sawtooth = Reference(ws1, min_col=9, min_row=16, max_row=46)
    chart_sawtooth.add_data(data_sawtooth, titles_from_data=True)
    chart_sawtooth.set_categories(cats_sawtooth)

    # VISIBILIDAD DE EJES Y ETIQUETAS NUMÉRICAS SIN SOLAPAMIENTO
    chart_sawtooth.x_axis.delete = False
    chart_sawtooth.y_axis.delete = False
    chart_sawtooth.x_axis.tickLblPos = "low"
    chart_sawtooth.y_axis.tickLblPos = "nextTo"
    chart_sawtooth.x_axis.tickLblSkip = 5
    chart_sawtooth.x_axis.tickMarkSkip = 5
    chart_sawtooth.x_axis.number_format = '0'
    chart_sawtooth.y_axis.number_format = '#,##0'

    # AJUSTE DE DISEÑO DEL ÁREA DE TRAZADO (MANUAL LAYOUT ANTI-SOLAPES)
    chart_sawtooth.layout = Layout(
        manualLayout=ManualLayout(
            x=0.15,  # Margen izquierdo para título del eje Y y cifras
            y=0.12,  # Margen superior para el título principal del gráfico
            w=0.80,  # Ancho del área de trazado
            h=0.70   # Alto del área de trazado, dejando espacio para etiquetas X y su título
        )
    )

    # Estilos de series
    if len(chart_sawtooth.series) >= 3:
        # Serie 1: Inventario Físico (Azul)
        chart_sawtooth.series[0].graphicalProperties.line.solidFill = COLOR_BLUE_ACCENT
        chart_sawtooth.series[0].graphicalProperties.line.width = 25000
        # Serie 2: ROP (Ámbar)
        chart_sawtooth.series[1].graphicalProperties.line.solidFill = COLOR_AMBER_BORDER
        chart_sawtooth.series[1].graphicalProperties.line.width = 20000
        # Serie 3: SS (Verde)
        chart_sawtooth.series[2].graphicalProperties.line.solidFill = COLOR_GREEN_BORDER
        chart_sawtooth.series[2].graphicalProperties.line.width = 20000

    ws1.add_chart(chart_sawtooth, "B15")

    # =========================================================================
    # AUTOAJUSTE DE ANCHOS DE COLUMNA Y PROTECCIÓN ECMA-376
    # =========================================================================
    # Anchos para ws1 (Garantiza que todas las tarjetas KPI, tablas y panel de control tengan holgura total)
    col_widths_ws1 = {
        1: 4,   # Col A: Margen
        2: 15,  # Col B: Clase ABC (Card 1)
        3: 14,  # Col C: Nº SKUs (Card 1) -> Ancho Card 1 = 29
        4: 14,  # Col D: % Catálogo (Card 2)
        5: 22,  # Col E: Consumo Anual Valor (Card 2) -> Ancho Card 2 = 36
        6: 14,  # Col F: % Valor Total (Card 3)
        7: 18,  # Col G: Inversión en SS (Card 3) -> Ancho Card 3 = 32
        8: 6,   # Col H: Separador elegante entre paneles
        9: 14,  # Col I: Día ciclo Sawtooth / Etiquetas Parámetros
        10: 22, # Col J: Inventario Físico / Input SKU & ROP Card
        11: 26, # Col K: Punto de Pedido (ROP) [u] / SS Card (holgura sin truncar)
        12: 26, # Col L: Stock de Seguridad (SS) [u] / CSL Card (holgura sin truncar)
        13: 34  # Col M: Estado Operativo del Ciclo / LTD Card (holgura total)
    }
    for col_i, w in col_widths_ws1.items():
        ws1.column_dimensions[get_column_letter(col_i)].width = w

    # Anchos para ws2
    col_widths_ws2 = {1: 14, 2: 24, 3: 42, 4: 12, 5: 16, 6: 16, 7: 14, 8: 16, 9: 16, 10: 16, 11: 16, 12: 16, 13: 16, 14: 20}
    for col_i, w in col_widths_ws2.items():
        ws2.column_dimensions[get_column_letter(col_i)].width = w

    # Anchos para ws3
    col_widths_ws3 = {1: 14, 2: 36, 3: 10, 4: 14, 5: 16, 6: 16, 7: 16, 8: 16, 9: 16, 10: 16, 11: 16, 12: 18, 13: 18, 14: 16, 15: 18, 16: 18, 17: 22}
    for col_i, w in col_widths_ws3.items():
        ws3.column_dimensions[get_column_letter(col_i)].width = w

    # Anchos para ws4
    col_widths_ws4 = {1: 26, 2: 16, 3: 18, 4: 22, 5: 20, 6: 20, 7: 46, 8: 4, 9: 4, 10: 4}
    for col_i, w in col_widths_ws4.items():
        ws4.column_dimensions[get_column_letter(col_i)].width = w

    # APLICAR PROTECCIÓN OPENXML ECMA-376
    finalize_protection(ws2, input_ranges=[t2_input_coords])
    finalize_protection(ws3)
    finalize_protection(ws4, input_ranges=[t4_input_coords])
    finalize_protection(ws1, input_ranges=[t1_input_coords], decorative_cells=t1_dec_coords)

    return wb


def main():
    """Genera ambos libros de trabajo y los almacena en sus carpetas oficiales."""
    base_dir = "packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP"
    es_dir = os.path.join(base_dir, "[ES]_Stock_Seguridad_ROP")
    en_dir = os.path.join(base_dir, "[EN]_Safety_Stock_ROP")

    os.makedirs(es_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)

    file_es = os.path.join(es_dir, "Calculadora_Stock_Seguridad_ROP_ES.xlsx")
    file_en = os.path.join(en_dir, "Safety_Stock_ROP_Calculator_EN.xlsx")

    print("[1/2] Generando Calculadora de Stock de Seguridad & ROP en Español...")
    wb_es = build_workbook(lang="ES")
    wb_es.save(file_es)
    print(f"      -> Guardado: {file_es}")

    print("[2/2] Generating Safety Stock & ROP Calculator in English...")
    wb_en = build_workbook(lang="EN")
    wb_en.save(file_en)
    print(f"      -> Saved: {file_en}")

    print("Modelos analíticos de Excel generados con total éxito.")


if __name__ == "__main__":
    main()
