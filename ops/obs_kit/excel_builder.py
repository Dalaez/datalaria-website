# -*- coding: utf-8 -*-
"""ops/obs_kit/excel_builder.py — Generador determinista de libros Excel Dual ES/EN (.xlsx sin VBA).

Cumple b2b-kit-factory SKILL e INV-PULSE-5:
- 5 hojas exactas:
  1. 01_BOM_AML_EXPLORER
  2. 02_IEC62402_CRITICALITY
  3. 03_LTB_VS_FFF_SIMULATOR
  4. 04_MITIGATION_ROADMAP
  5. 05_EXECUTIVE_DASHBOARD
- Fórmulas estándar en inglés (IF, OR, SUM, SUMIF, COUNTIF, AVERAGE, ROUND, ROUNDUP, ABS, MIN, SQRT)
  para auto-traducción automática en Excel ES/EN y Google Sheets.
- Tablas nativas Excel, DataValidation, formato condicional, celdas de entrada desbloqueadas y fórmulas bloqueadas.
- Gráfico de barras nativo (BarChart) y tabla comparativa explícita pack-stock vs. pack-obs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo


# Paleta Executive Data-Dense (Datalaria)
NAVY_HEX = "0F172A"
DARK_SLATE_HEX = "1E293B"
CYAN_HEX = "0EA5E9"
CYAN_LIGHT_HEX = "E0F2FE"
VIOLET_HEX = "7C3AED"
VIOLET_LIGHT_HEX = "EDE9FE"
ZEBRA_HEX = "F8FAFC"
INPUT_HEX = "EFF6FF"
BORDER_HEX = "CBD5E1"
DANGER_BG_HEX = "FEE2E2"
DANGER_FG_HEX = "991B1B"
WARN_BG_HEX = "FEF3C7"
WARN_FG_HEX = "92400E"
OK_BG_HEX = "D1FAE5"
OK_FG_HEX = "065F46"

THIN_SIDE = Side(style="thin", color=BORDER_HEX)
MED_NAVY = Side(style="medium", color=NAVY_HEX)
CELL_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

FONT_TITLE = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
FONT_SUB = Font(name="Calibri", size=10, italic=True, color="CBD5E1")
FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
FONT_SECTION = Font(name="Calibri", size=11, bold=True, color=NAVY_HEX)
FONT_DATA = Font(name="Calibri", size=10, color="0F172A")
FONT_DATA_BOLD = Font(name="Calibri", size=10, bold=True, color="0F172A")
FONT_INPUT = Font(name="Calibri", size=10, bold=True, color="1D4ED8")
FONT_KPI_LABEL = Font(name="Calibri", size=9, bold=True, color="475569")
FONT_KPI_VAL = Font(name="Calibri", size=16, bold=True, color=NAVY_HEX)

FILL_NAVY = PatternFill("solid", fgColor=NAVY_HEX)
FILL_SLATE = PatternFill("solid", fgColor=DARK_SLATE_HEX)
FILL_CYAN = PatternFill("solid", fgColor=CYAN_HEX)
FILL_CYAN_LIGHT = PatternFill("solid", fgColor=CYAN_LIGHT_HEX)
FILL_VIOLET_LIGHT = PatternFill("solid", fgColor=VIOLET_LIGHT_HEX)
FILL_ZEBRA = PatternFill("solid", fgColor=ZEBRA_HEX)
FILL_WHITE = PatternFill("solid", fgColor="FFFFFF")
FILL_INPUT = PatternFill("solid", fgColor=INPUT_HEX)
FILL_DANGER = PatternFill("solid", fgColor=DANGER_BG_HEX)
FILL_WARN = PatternFill("solid", fgColor=WARN_BG_HEX)
FILL_OK = PatternFill("solid", fgColor=OK_BG_HEX)

LOCKED = Protection(locked=True)
UNLOCKED = Protection(locked=False)

# Dataset industrial sintético limpio (12 líneas BOM realistas, 0 datos privados de Datalaria)
BOM_SAMPLE_ROWS: list[dict[str, Any]] = [
    {
        "id": "BOM-001", "mpn": "TI-CAP-10U-50", "mfg": "Texas Instruments", "ipn": "INT-CAP-10UF",
        "alts": 0, "sub": "PWR-REG-BOARD", "sku": "DRONE-X1-PRO", "qty": 4, "demand": 1200,
        "margin": 145.0, "status": "EOL", "lt_w": 26,
        "ltb_mo": 24, "mo_dem": 400, "sd_mo": 65, "ltb_px": 1.85, "nre": 28000, "recert": 9500, "red_mo": 7, "brk_px": 4.90,
        "owner": "Component Eng.", "cutoff": "2027-01-31", "action_es": "Congelar ROP y ejecutar compra LTB 24m",
        "action_en": "Freeze ROP and execute 24m LTB bridge", "capex_app": 20000, "capex_sp": 18200, "state": "In Progress",
    },
    {
        "id": "BOM-002", "mpn": "MK20DX256VLH7", "mfg": "NXP Semiconductors", "ipn": "INT-MCU-K20",
        "alts": 0, "sub": "FLIGHT-CTRL-V3", "sku": "DRONE-X1-PRO", "qty": 1, "demand": 1200,
        "margin": 145.0, "status": "Obsolete", "lt_w": 32,
        "ltb_mo": 30, "mo_dem": 110, "sd_mo": 18, "ltb_px": 11.40, "nre": 42000, "recert": 18000, "red_mo": 9, "brk_px": 29.00,
        "owner": "Hardware Lead", "cutoff": "2027-01-15", "action_es": "Puente LTB 12m + Rediseño FFF a STM32H7",
        "action_en": "12m LTB bridge + FFF Redesign to STM32H7", "capex_app": 60000, "capex_sp": 22500, "state": "Approved",
    },
    {
        "id": "BOM-003", "mpn": "CC1206KKX7R9BB106", "mfg": "Yageo", "ipn": "INT-CAP-HV12",
        "alts": 1, "sub": "INVERTER-STAGE", "sku": "EDGE-PLC-400", "qty": 6, "demand": 850,
        "margin": 210.0, "status": "EOL", "lt_w": 18,
        "ltb_mo": 18, "mo_dem": 425, "sd_mo": 55, "ltb_px": 0.95, "nre": 14000, "recert": 6000, "red_mo": 4, "brk_px": 2.40,
        "owner": "Procurement", "cutoff": "2027-02-28", "action_es": "Cualificar 2a fuente Murata en AML",
        "action_en": "Qualify Murata 2nd source in AML", "capex_app": 12000, "capex_sp": 8900, "state": "Open",
    },
    {
        "id": "BOM-004", "mpn": "ADUM1401ARWZ", "mfg": "Analog Devices", "ipn": "INT-ISO-4CH",
        "alts": 0, "sub": "ISOLATION-BUS", "sku": "MED-PUMP-S9", "qty": 2, "demand": 600,
        "margin": 390.0, "status": "PDN", "lt_w": 28,
        "ltb_mo": 36, "mo_dem": 100, "sd_mo": 15, "ltb_px": 6.20, "nre": 55000, "recert": 38000, "red_mo": 12, "brk_px": 16.50,
        "owner": "Regulatory QA", "cutoff": "2027-03-15", "action_es": "LTB 36m obligatorio (alta recertificación médica)",
        "action_en": "Mandatory 36m LTB (high medical recert cost)", "capex_app": 28000, "capex_sp": 25400, "state": "Approved",
    },
    {
        "id": "BOM-005", "mpn": "STM32F405RGT6", "mfg": "STMicroelectronics", "ipn": "INT-MCU-F4",
        "alts": 1, "sub": "MAIN-LOGIC-PCB", "sku": "EDGE-PLC-400", "qty": 1, "demand": 850,
        "margin": 210.0, "status": "NRND", "lt_w": 20,
        "ltb_mo": 24, "mo_dem": 75, "sd_mo": 12, "ltb_px": 9.80, "nre": 26000, "recert": 8000, "red_mo": 6, "brk_px": 21.00,
        "owner": "Firmware Lead", "cutoff": "2027-06-30", "action_es": "Planificar migración pin-to-pin antes de PDN",
        "action_en": "Schedule pin-to-pin migration ahead of PDN", "capex_app": 34000, "capex_sp": 6000, "state": "Open",
    },
    {
        "id": "BOM-006", "mpn": "LM2596S-5.0/NOPB", "mfg": "Texas Instruments", "ipn": "INT-REG-5V",
        "alts": 0, "sub": "LIDAR-PSU-MOD", "sku": "LIDAR-SCAN-V2", "qty": 2, "demand": 500,
        "margin": 320.0, "status": "PDN", "lt_w": 22,
        "ltb_mo": 24, "mo_dem": 85, "sd_mo": 16, "ltb_px": 3.40, "nre": 15000, "recert": 5500, "red_mo": 5, "brk_px": 9.20,
        "owner": "Power Eng.", "cutoff": "2027-02-15", "action_es": "Ejecutar LTB 24m (bajo desembolso CAPEX)",
        "action_en": "Execute 24m LTB (low CAPEX outlay)", "capex_app": 9500, "capex_sp": 7800, "state": "In Progress",
    },
    {
        "id": "BOM-007", "mpn": "LAN8720A-CP-TR", "mfg": "Microchip", "ipn": "INT-PHY-ETH",
        "alts": 0, "sub": "COMMS-ETH-CARD", "sku": "EDGE-PLC-400", "qty": 1, "demand": 850,
        "margin": 210.0, "status": "EOL", "lt_w": 24,
        "ltb_mo": 36, "mo_dem": 72, "sd_mo": 14, "ltb_px": 4.10, "nre": 19000, "recert": 6500, "red_mo": 5, "brk_px": 11.80,
        "owner": "Hardware Lead", "cutoff": "2027-01-25", "action_es": "Evaluar LTB 36m vs. rediseño DP83848",
        "action_en": "Evaluate 36m LTB vs. DP83848 redesign", "capex_app": 14000, "capex_sp": 11900, "state": "In Progress",
    },
    {
        "id": "BOM-008", "mpn": "OPA2188AIDR", "mfg": "Texas Instruments", "ipn": "INT-OPAMP-PREC",
        "alts": 1, "sub": "SENSOR-AFE-V2", "sku": "MED-PUMP-S9", "qty": 3, "demand": 600,
        "margin": 390.0, "status": "NRND", "lt_w": 16,
        "ltb_mo": 24, "mo_dem": 150, "sd_mo": 22, "ltb_px": 4.60, "nre": 18000, "recert": 24000, "red_mo": 8, "brk_px": 12.50,
        "owner": "Analog Eng.", "cutoff": "2027-08-30", "action_es": "Revisar stock puente y validar 2a fuente ADI",
        "action_en": "Review bridge buffer and validate ADI 2nd source", "capex_app": 20000, "capex_sp": 4000, "state": "Open",
    },
    {
        "id": "BOM-009", "mpn": "W25Q128JVSIQ", "mfg": "Winbond", "ipn": "INT-NOR-128M",
        "alts": 2, "sub": "MAIN-LOGIC-PCB", "sku": "DRONE-X1-PRO", "qty": 1, "demand": 1200,
        "margin": 145.0, "status": "Active", "lt_w": 8,
        "ltb_mo": 0, "mo_dem": 0, "sd_mo": 0, "ltb_px": 0, "nre": 0, "recert": 0, "red_mo": 0, "brk_px": 0,
        "owner": "S&OP Planner", "cutoff": "2028-12-31", "action_es": "Mantener reposición APICS ROP (pack-stock)",
        "action_en": "Keep APICS ROP replenishment (pack-stock)", "capex_app": 0, "capex_sp": 0, "state": "Closed",
    },
    {
        "id": "BOM-010", "mpn": "DRV8301DCAR", "mfg": "Texas Instruments", "ipn": "INT-DRV-3PH",
        "alts": 2, "sub": "MOTOR-ESC-V4", "sku": "DRONE-X1-PRO", "qty": 4, "demand": 1200,
        "margin": 145.0, "status": "Active", "lt_w": 10,
        "ltb_mo": 0, "mo_dem": 0, "sd_mo": 0, "ltb_px": 0, "nre": 0, "recert": 0, "red_mo": 0, "brk_px": 0,
        "owner": "S&OP Planner", "cutoff": "2028-12-31", "action_es": "Mantener reposición APICS ROP (pack-stock)",
        "action_en": "Keep APICS ROP replenishment (pack-stock)", "capex_app": 0, "capex_sp": 0, "state": "Closed",
    },
    {
        "id": "BOM-011", "mpn": "TPS62130RGTR", "mfg": "Texas Instruments", "ipn": "INT-BUCK-3A",
        "alts": 2, "sub": "LIDAR-PSU-MOD", "sku": "LIDAR-SCAN-V2", "qty": 2, "demand": 500,
        "margin": 320.0, "status": "Active", "lt_w": 9,
        "ltb_mo": 0, "mo_dem": 0, "sd_mo": 0, "ltb_px": 0, "nre": 0, "recert": 0, "red_mo": 0, "brk_px": 0,
        "owner": "S&OP Planner", "cutoff": "2028-12-31", "action_es": "Mantener reposición APICS ROP (pack-stock)",
        "action_en": "Keep APICS ROP replenishment (pack-stock)", "capex_app": 0, "capex_sp": 0, "state": "Closed",
    },
    {
        "id": "BOM-012", "mpn": "MAX485ESA+", "mfg": "Analog Devices", "ipn": "INT-RS485-TX",
        "alts": 3, "sub": "COMMS-ETH-CARD", "sku": "EDGE-PLC-400", "qty": 2, "demand": 850,
        "margin": 210.0, "status": "Active", "lt_w": 6,
        "ltb_mo": 0, "mo_dem": 0, "sd_mo": 0, "ltb_px": 0, "nre": 0, "recert": 0, "red_mo": 0, "brk_px": 0,
        "owner": "S&OP Planner", "cutoff": "2028-12-31", "action_es": "Mantener reposición APICS ROP (pack-stock)",
        "action_en": "Keep APICS ROP replenishment (pack-stock)", "capex_app": 0, "capex_sp": 0, "state": "Closed",
    },
]

COPY: dict[str, dict[str, Any]] = {
    "es": {
        "s1_title": "01 · EXPLORADOR MULTINIVEL BOM & AML (NORMA IEC 62402)",
        "s1_sub": "Mapeo determinista MPN -> Parte Interna -> Alternativos AML -> Subensamblaje -> SKU Final y Margen P&L en Riesgo (Celdas azules editables).",
        "s1_headers": [
            "ID_BOM", "MPN_Fabricante", "Fabricante", "Ref_Interna", "Fuentes_Alt_AML",
            "Subensamblaje", "SKU_Final", "Cant_x_SKU", "Demanda_Anual_SKU", "Margen_Unit_EUR",
            "Estado_Ciclo_Vida", "Lead_Time_Sem", "Margen_Anual_Riesgo_EUR",
        ],
        "s2_title": "02 · MATRIZ CUANTITATIVA DE CRITICIDAD IEC 62402",
        "s2_sub": "Cálculo automático 0–100 ponderando Fuente Única AML (40), Urgencia de Ciclo de Vida (35), Lead Time (15) y Exposición P&L (10).",
        "s2_headers": [
            "ID_BOM", "MPN_Fabricante", "Estado_Ciclo_Vida", "Riesgo_AML_40", "Urgencia_EOL_35",
            "Exposicion_LT_15", "Impacto_PnL_10", "Score_IEC62402", "Nivel_Accion_IEC", "Regla_ROP_vs_LTB",
        ],
        "s3_title": "03 · SIMULADOR FINANCIERO LAST TIME BUY (LTB) VS. REDISEÑO FFF",
        "s3_sub": "Decisión CAPEX/Working Capital tras congelar el Punto de Pedido recurrente (ROP) ante alertas PCN/PDN/EOL.",
        "s3_params_title": "PARÁMETROS FINANCIEROS GLOBALES (EDITABLES)",
        "s3_p1": "Tasa WACC / Coste de Capital Anual",
        "s3_p2": "Tasa Anual de Almacenaje, Seguro y Merma",
        "s3_p3": "Factor Z Nivel de Servicio Puente (SS_LTB)",
        "s3_note_title": "SINERGIA CON PACK-STOCK (7 €): CONGELACIÓN DE ROP -> COMPRA PUENTE LTB",
        "s3_note_body": (
            "Mientras un componente está Active (Fase Madurez), usa pack-stock (Calculadora Stock de Seguridad & ROP · APICS) "
            "para pedidos recurrentes (EOQ/ROP). En el instante en que llega un aviso PDN/EOL, CONGELA el ROP automático y calcula "
            "aquí el colchón puente único SS_LTB y si conviene ejecutar Last Time Buy (LTB) o financiar un Rediseño FFF (NRE)."
        ),
        "s3_headers": [
            "ID_BOM", "MPN_Fabricante", "Horizonte_Meses", "Demanda_Mensual", "Desv_Std_Mensual",
            "Precio_LTB_EUR", "NRE_Rediseño_EUR", "Recertificacion_EUR", "Meses_Rediseño", "Precio_Broker_EUR",
            "SS_LTB_Puente_Uds", "Uds_Totales_LTB", "Capex_LTB_EUR", "Coste_WACC_Merma_EUR",
            "Coste_Total_LTB_EUR", "Coste_Total_FFF_EUR", "Ahorro_Optimo_EUR", "Equilibrio_T_Meses", "Veredicto_Ejecutivo",
        ],
        "s4_title": "04 · HOJA DE RUTA DE MITIGACIÓN Y GOBERNANZA CAPEX",
        "s4_sub": "Seguimiento de fechas límite LTB (Cutoff), cualificación de alternativas AML y control de desvío presupuestario CAPEX.",
        "s4_headers": [
            "ID_BOM", "MPN_Fabricante", "Score_IEC62402", "Nivel_Accion_IEC", "Responsable",
            "Fecha_Limite_LTB", "Accion_Mitigacion", "Estado_Plan", "CAPEX_Aprobado_EUR",
            "CAPEX_Ejecutado_EUR", "Desvio_CAPEX_EUR",
        ],
        "s5_title": "05 · CUADRO DE MANDO EJECUTIVO C-LEVEL (COO / CFO)",
        "s5_sub": "Resumen consolidado de exposición financiera IEC 62402, necesidad de Working Capital LTB y matriz de uso pack-stock vs. pack-obs.",
        "kpi_labels": [
            "MARGEN ANUAL P&L EN RIESGO",
            "COMPONENTES CRÍTICOS (LTB)",
            "CAPITAL LTB TOTAL REQUERIDO",
            "INVERSIÓN NRE REDISEÑO FFF",
            "AHORRO NETO DECISIÓN ÓPTIMA",
            "SCORE MEDIO IEC 62402",
        ],
        "sum_title": "DESGLOSE DE EXPOSICIÓN POR ESTADO DE CICLO DE VIDA",
        "sum_headers": ["Estado Ciclo de Vida", "Nº Componentes", "Margen P&L en Riesgo (€)", "% Exposición Total"],
        "cmp_title": "MATRIZ EJECUTIVA ANTI-CONFUSIÓN: ¿CUÁNDO USAR PACK-STOCK (7 €) VS. PACK-OBS (19 €)?",
        "cmp_headers": ["Dimensión Operativa", "pack-stock (Stock Seguridad & ROP · 7 €)", "pack-obs (IEC 62402 Obsolescencia & LTB · 19 €)"],
        "cmp_rows": [
            ("Fase del Ciclo de Vida", "Madurez (Proveedor activo, compras recurrentes)", "Fin de Vida (PCN / PDN / EOL: la línea cierra)"),
            ("Estándar Normativo", "APICS / ASCM & MIT CTL (Revisión continua s,Q)", "IEC 62402 & JEDEC J-STD-048 (Gestión de Obsolescencia)"),
            ("Motor Matemático", "Convolución SS3, Punto de Pedido (ROP) y Wilson EOQ", "Explosión DAG BOM Multinivel, Criticidad IEC y LTB vs. FFF"),
            ("Decisión que Resuelve", "¿Cuánto stock mantener cada mes sin roturas ni exceso?", "¿Qué SKUs se paran y conviene comprar LTB 3 años o rediseñar?"),
            ("Relación entre Ambos", "Gobierna el catálogo sano; al llegar EOL se congela ROP", "Toma el relevo en crisis EOL y calcula el colchón puente SS_LTB"),
        ],
        "chart_title": "Margen P&L en Riesgo (€) por Estado de Ciclo de Vida",
    },
    "en": {
        "s1_title": "01 · MULTILEVEL BOM & AML EXPLORER (IEC 62402 STANDARD)",
        "s1_sub": "Deterministic MPN -> Internal Part -> AML Alternates -> Sub-Assembly -> End SKU & Annual P&L Margin at Risk (Blue cells editable).",
        "s1_headers": [
            "BOM_ID", "MPN_Part_Number", "Manufacturer", "Internal_PN", "AML_Alt_Sources",
            "Sub_Assembly", "Final_SKU", "Qty_Per_SKU", "Annual_SKU_Demand", "Unit_Margin_EUR",
            "Lifecycle_Status", "Lead_Time_Wks", "Annual_Margin_At_Risk_EUR",
        ],
        "s2_title": "02 · IEC 62402 QUANTITATIVE CRITICALITY MATRIX",
        "s2_sub": "Automated 0–100 scoring weighting Single-Source AML Risk (40), Lifecycle Urgency (35), Lead Time (15), and P&L Exposure (10).",
        "s2_headers": [
            "BOM_ID", "MPN_Part_Number", "Lifecycle_Status", "AML_Risk_40", "EOL_Urgency_35",
            "LeadTime_Exp_15", "PnL_Impact_10", "IEC62402_Score", "IEC_Action_Tier", "ROP_vs_LTB_Trigger",
        ],
        "s3_title": "03 · LAST TIME BUY (LTB) VS. FFF REDESIGN FINANCIAL SIMULATOR",
        "s3_sub": "CAPEX / Working Capital decision model after freezing recurring Reorder Point (ROP) upon PCN/PDN/EOL notices.",
        "s3_params_title": "GLOBAL FINANCIAL ASSUMPTIONS (EDITABLE)",
        "s3_p1": "Annual WACC / Cost of Capital Rate",
        "s3_p2": "Annual Holding, Insurance & Decay Rate",
        "s3_p3": "Service Level Z-Factor for Bridge Buffer (SS_LTB)",
        "s3_note_title": "SYNERGY WITH PACK-STOCK (€7): FREEZING ROP -> ONE-SHOT LTB BRIDGE",
        "s3_note_body": (
            "While a component is Active (Maturity phase), use pack-stock (Safety Stock & ROP Calculator · APICS) "
            "for recurring replenishment (EOQ/ROP). The moment a PDN/EOL notice arrives, FREEZE recurring ROP and compute "
            "the one-shot bridge buffer SS_LTB and LTB vs. FFF Redesign (NRE) financial frontier here."
        ),
        "s3_headers": [
            "BOM_ID", "MPN_Part_Number", "Horizon_Months", "Monthly_Demand", "Monthly_StdDev",
            "LTB_Unit_EUR", "Redesign_NRE_EUR", "Recert_Cost_EUR", "Redesign_Months", "Broker_Unit_EUR",
            "SS_LTB_Bridge_Units", "Total_LTB_Units", "LTB_Capex_EUR", "WACC_Holding_EUR",
            "Total_LTB_Cost_EUR", "Total_FFF_Cost_EUR", "Optimal_Savings_EUR", "BreakEven_T_Mo", "Executive_Verdict",
        ],
        "s4_title": "04 · MITIGATION ROADMAP & CAPEX GOVERNANCE",
        "s4_sub": "Tracking LTB cutoff deadlines, AML second-source qualification milestones, and CAPEX budget variance.",
        "s4_headers": [
            "BOM_ID", "MPN_Part_Number", "IEC62402_Score", "IEC_Action_Tier", "Owner",
            "LTB_Cutoff_Date", "Mitigation_Action", "Plan_Status", "Approved_CAPEX_EUR",
            "Actual_CAPEX_EUR", "CAPEX_Variance_EUR",
        ],
        "s5_title": "05 · C-LEVEL EXECUTIVE DASHBOARD (COO / CFO)",
        "s5_sub": "Consolidated IEC 62402 financial risk exposure, LTB working capital demand, and pack-stock vs. pack-obs decision matrix.",
        "kpi_labels": [
            "ANNUAL P&L MARGIN AT RISK",
            "CRITICAL LTB COMPONENTS",
            "TOTAL LTB WORKING CAPITAL",
            "TOTAL FFF REDESIGN NRE",
            "NET SAVINGS (BEST OPTION)",
            "AVG IEC 62402 SCORE",
        ],
        "sum_title": "FINANCIAL EXPOSURE BREAKDOWN BY LIFECYCLE STATUS",
        "sum_headers": ["Lifecycle Status", "Component Count", "P&L Margin at Risk (€)", "% of Total Exposure"],
        "cmp_title": "ANTI-CONFUSION EXECUTIVE MATRIX: WHEN TO USE PACK-STOCK (€7) VS. PACK-OBS (€19)",
        "cmp_headers": ["Operational Axis", "pack-stock (Safety Stock & ROP · €7)", "pack-obs (IEC 62402 Obsolescence & LTB · €19)"],
        "cmp_rows": [
            ("Lifecycle Stage", "Maturity (Active vendor, recurring monthly orders)", "End-of-Life (PCN / PDN / EOL: production line shuts down)"),
            ("Global Standard", "APICS / ASCM & MIT CTL (Continuous review s,Q)", "IEC 62402 & JEDEC J-STD-048 (Obsolescence Management)"),
            ("Core Math Engine", "SS3 convolution, Reorder Point (ROP) & Wilson EOQ", "Multilevel BOM DAG traversal, IEC Criticality & LTB vs. FFF"),
            ("Boardroom Question", "How much monthly buffer ensures 98% fill rate?", "Which end SKUs halt & should we buy 3yr LTB or redesign?"),
            ("Mutual Synergy", "Governs healthy SKUs; freeze ROP once EOL hits", "Takes over at EOL crisis & sizes the SS_LTB bridge buffer"),
        ],
        "chart_title": "Annual P&L Margin at Risk (€) by Lifecycle Status",
    },
}


def _configure_sheet_base(ws, title: str, subtitle: str, max_col: int, freeze_cell: str = "A5") -> None:
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = freeze_cell
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0

    end_col_letter = get_column_letter(max_col)
    ws.merge_cells(f"A1:{end_col_letter}1")
    ws.merge_cells(f"A2:{end_col_letter}2")
    ws["A1"] = title
    ws["A1"].font = FONT_TITLE
    ws["A1"].fill = FILL_NAVY
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 28

    ws["A2"] = subtitle
    ws["A2"].font = FONT_SUB
    ws["A2"].fill = FILL_SLATE
    ws["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 20
    ws.row_dimensions[3].height = 8


def _style_table_header(ws, row_idx: int, headers: list[str]) -> None:
    ws.row_dimensions[row_idx].height = 26
    for c_idx, text in enumerate(headers, start=1):
        cell = ws.cell(row=row_idx, column=c_idx, value=text)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY
        cell.border = CELL_BORDER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.protection = LOCKED


def _add_native_table(ws, display_name: str, ref: str) -> None:
    tbl = Table(displayName=display_name, ref=ref)
    tbl.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    ws.add_table(tbl)


def _autosize_columns(ws, widths: dict[int, float]) -> None:
    for col_idx, width in widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width


def build_excel_workbook(lang: str, output_path: Path) -> Path:
    """Genera el libro Excel Dual (.xlsx sin VBA) con las 5 hojas exactas."""
    assert lang in ("es", "en")
    c = COPY[lang]
    wb = Workbook()

    # ------------------------------------------------------------------
    # HOJA 1: 01_BOM_AML_EXPLORER
    # ------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "01_BOM_AML_EXPLORER"
    _configure_sheet_base(ws1, c["s1_title"], c["s1_sub"], max_col=13, freeze_cell="A5")
    _style_table_header(ws1, 4, c["s1_headers"])

    for idx, row in enumerate(BOM_SAMPLE_ROWS, start=5):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        vals = [
            row["id"], row["mpn"], row["mfg"], row["ipn"], row["alts"],
            row["sub"], row["sku"], row["qty"], row["demand"], row["margin"],
            row["status"], row["lt_w"],
            f'=IF(OR(K{idx}="EOL",K{idx}="Obsolete",K{idx}="PDN"),I{idx}*J{idx},IF(K{idx}="NRND",I{idx}*J{idx}*0.35,0))',
        ]
        ws1.row_dimensions[idx].height = 20
        for col_i, val in enumerate(vals, start=1):
            cell = ws1.cell(row=idx, column=col_i, value=val)
            cell.border = CELL_BORDER
            is_formula = isinstance(val, str) and val.startswith("=")
            if col_i in (5, 8, 9, 10, 11, 12):
                cell.fill = FILL_INPUT
                cell.font = FONT_INPUT
                cell.protection = UNLOCKED
            else:
                cell.fill = fill
                cell.font = FONT_DATA_BOLD if is_formula or col_i == 2 else FONT_DATA
                cell.protection = LOCKED

            if col_i in (5, 8, 9, 12):
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i in (10, 13):
                cell.number_format = "#,##0.00 €"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i in (1, 11):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    last_s1 = 4 + len(BOM_SAMPLE_ROWS)
    _add_native_table(ws1, f"TblBOM_{lang.upper()}", f"A4:M{last_s1}")

    # Validación de datos para Estado de Ciclo de Vida
    dv_status = DataValidation(type="list", formula1='"Active,NRND,PDN,EOL,Obsolete"', allow_blank=False)
    ws1.add_data_validation(dv_status)
    dv_status.add(f"K5:K{last_s1}")

    # Fila de Totales fuera de la tabla para máxima claridad
    tot_r = last_s1 + 2
    ws1.cell(row=tot_r, column=1, value="TOTAL").font = FONT_DATA_BOLD
    ws1.cell(row=tot_r, column=9, value=f"=SUM(I5:I{last_s1})").number_format = "#,##0"
    ws1.cell(row=tot_r, column=13, value=f"=SUM(M5:M{last_s1})").number_format = "#,##0.00 €"
    for ci in (1, 9, 13):
        ws1.cell(row=tot_r, column=ci).font = FONT_DATA_BOLD
        ws1.cell(row=tot_r, column=ci).fill = FILL_CYAN_LIGHT
        ws1.cell(row=tot_r, column=ci).border = CELL_BORDER

    _autosize_columns(ws1, {1: 11, 2: 21, 3: 19, 4: 16, 5: 14, 6: 18, 7: 16, 8: 11, 9: 16, 10: 15, 11: 15, 12: 13, 13: 22})

    # ------------------------------------------------------------------
    # HOJA 2: 02_IEC62402_CRITICALITY
    # ------------------------------------------------------------------
    ws2 = wb.create_sheet("02_IEC62402_CRITICALITY")
    _configure_sheet_base(ws2, c["s2_title"], c["s2_sub"], max_col=10, freeze_cell="A5")
    _style_table_header(ws2, 4, c["s2_headers"])

    for idx in range(5, last_s1 + 1):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        ws2.row_dimensions[idx].height = 20
        formulas = [
            f"='01_BOM_AML_EXPLORER'!A{idx}",
            f"='01_BOM_AML_EXPLORER'!B{idx}",
            f"='01_BOM_AML_EXPLORER'!K{idx}",
            f"=IF('01_BOM_AML_EXPLORER'!E{idx}=0,40,IF('01_BOM_AML_EXPLORER'!E{idx}=1,20,5))",
            f'=IF(C{idx}="Obsolete",35,IF(C{idx}="EOL",30,IF(C{idx}="PDN",22,IF(C{idx}="NRND",12,0))))',
            f"=IF('01_BOM_AML_EXPLORER'!L{idx}>=24,15,IF('01_BOM_AML_EXPLORER'!L{idx}>=12,10,4))",
            f"=IF('01_BOM_AML_EXPLORER'!M{idx}>=150000,10,IF('01_BOM_AML_EXPLORER'!M{idx}>=50000,6,2))",
            f"=MIN(100,SUM(D{idx}:G{idx}))",
            f'=IF(H{idx}>=70,"CRITICAL LTB REQUIRED",IF(H{idx}>=40,"DUAL-SOURCE / QUALIFY","MONITOR"))',
            f'=IF(H{idx}>=70,"FREEZE ROP -> LTB",IF(H{idx}>=40,"REVIEW SAFETY STOCK","KEEP ROP (pack-stock)"))',
        ]
        for col_i, f_val in enumerate(formulas, start=1):
            cell = ws2.cell(row=idx, column=col_i, value=f_val)
            cell.fill = fill
            cell.font = FONT_DATA_BOLD if col_i in (2, 8, 9) else FONT_DATA
            cell.border = CELL_BORDER
            cell.protection = LOCKED
            if col_i in (4, 5, 6, 7, 8):
                cell.number_format = "0"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i in (1, 3, 9, 10):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    _add_native_table(ws2, f"TblIEC_{lang.upper()}", f"A4:J{last_s1}")
    ws2.conditional_formatting.add(
        f"H5:H{last_s1}",
        CellIsRule(operator="greaterThanOrEqual", formula=["70"], fill=FILL_DANGER, font=Font(bold=True, color=DANGER_FG_HEX)),
    )
    ws2.conditional_formatting.add(
        f"H5:H{last_s1}",
        CellIsRule(operator="between", formula=["40", "69"], fill=FILL_WARN, font=Font(bold=True, color=WARN_FG_HEX)),
    )
    ws2.conditional_formatting.add(
        f"H5:H{last_s1}",
        CellIsRule(operator="lessThan", formula=["40"], fill=FILL_OK, font=Font(bold=True, color=OK_FG_HEX)),
    )
    _autosize_columns(ws2, {1: 11, 2: 21, 3: 15, 4: 14, 5: 15, 6: 15, 7: 14, 8: 15, 9: 24, 10: 24})

    # ------------------------------------------------------------------
    # HOJA 3: 03_LTB_VS_FFF_SIMULATOR
    # ------------------------------------------------------------------
    ws3 = wb.create_sheet("03_LTB_VS_FFF_SIMULATOR")
    _configure_sheet_base(ws3, c["s3_title"], c["s3_sub"], max_col=19, freeze_cell="A12")

    # Bloque de parámetros globales (Filas 4-7)
    ws3.merge_cells("A4:C4")
    ws3["A4"] = c["s3_params_title"]
    ws3["A4"].font = FONT_HEADER
    ws3["A4"].fill = FILL_NAVY
    ws3["A4"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    params = [(5, c["s3_p1"], 0.10, "0.0%"), (6, c["s3_p2"], 0.08, "0.0%"), (7, c["s3_p3"], 1.96, "0.00")]
    for pr, label, val, fmt in params:
        ws3.merge_cells(f"A{pr}:B{pr}")
        ws3[f"A{pr}"] = label
        ws3[f"A{pr}"].font = FONT_DATA_BOLD
        ws3[f"A{pr}"].fill = FILL_ZEBRA
        ws3[f"A{pr}"].border = CELL_BORDER
        ws3[f"B{pr}"].border = CELL_BORDER
        p_cell = ws3[f"C{pr}"]
        p_cell.value = val
        p_cell.number_format = fmt
        p_cell.font = FONT_INPUT
        p_cell.fill = FILL_INPUT
        p_cell.border = CELL_BORDER
        p_cell.protection = UNLOCKED
        p_cell.alignment = Alignment(horizontal="right", vertical="center")

    # Caja metodológica de sinergia con pack-stock (Columnas E-S, filas 4-7)
    ws3.merge_cells("E4:S4")
    ws3["E4"] = c["s3_note_title"]
    ws3["E4"].font = FONT_HEADER
    ws3["E4"].fill = FILL_CYAN
    ws3["E4"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws3.merge_cells("E5:S7")
    ws3["E5"] = c["s3_note_body"]
    ws3["E5"].font = FONT_DATA
    ws3["E5"].fill = FILL_CYAN_LIGHT
    ws3["E5"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
    for rr in range(5, 8):
        for cc in range(5, 20):
            ws3.cell(row=rr, column=cc).border = CELL_BORDER

    ws3.row_dimensions[9].height = 8
    _style_table_header(ws3, 11, c["s3_headers"])

    # 8 componentes en riesgo (NRND/PDN/EOL/Obsolete)
    risk_rows = [r for r in BOM_SAMPLE_ROWS if r["status"] != "Active"]
    for idx_offset, row in enumerate(risk_rows):
        r_idx = 12 + idx_offset
        src_r = 5 + idx_offset
        fill = FILL_ZEBRA if r_idx % 2 == 1 else FILL_WHITE
        ws3.row_dimensions[r_idx].height = 20

        vals = [
            f"='01_BOM_AML_EXPLORER'!A{src_r}",
            f"='01_BOM_AML_EXPLORER'!B{src_r}",
            row["ltb_mo"],
            row["mo_dem"],
            row["sd_mo"],
            row["ltb_px"],
            row["nre"],
            row["recert"],
            row["red_mo"],
            row["brk_px"],
            # K: Colchón puente SS_LTB tras congelar ROP recurrente
            f"=ROUNDUP($C$7*E{r_idx}*SQRT(C{r_idx}),0)",
            # L: Unidades totales LTB (Demanda horizonte + SS_LTB)
            f"=ROUNDUP(C{r_idx}*D{r_idx}+K{r_idx},0)",
            # M: Capex Cash Out LTB
            f"=L{r_idx}*F{r_idx}",
            # N: Coste financiero WACC + almacenaje/merma (inventario medio 50% durante horizonte)
            f"=M{r_idx}*($C$5+$C$6)*(C{r_idx}/24)",
            # O: Coste Total LTB
            f"=M{r_idx}+N{r_idx}",
            # P: Coste Total Rediseño FFF (NRE + Recertificación + riesgo de retraso/expediting)
            f"=G{r_idx}+H{r_idx}+(I{r_idx}*0.15*D{r_idx}*F{r_idx})",
            # Q: Ahorro neto eligiendo opción óptima
            f"=ABS(O{r_idx}-P{r_idx})",
            # R: Punto de equilibrio en meses T*
            f"=IF((D{r_idx}*F{r_idx}*(1+($C$5+$C$6)*0.5))>0,ROUND((G{r_idx}+H{r_idx})/(D{r_idx}*F{r_idx}*(1+($C$5+$C$6)*0.5)),1),0)",
            # S: Veredicto Ejecutivo
            f'=IF(O{r_idx}<=P{r_idx}*0.92,"EXECUTE LTB",IF(P{r_idx}<=O{r_idx}*0.92,"REDESIGN FFF","HYBRID BRIDGE"))',
        ]
        for col_i, val in enumerate(vals, start=1):
            cell = ws3.cell(row=r_idx, column=col_i, value=val)
            cell.border = CELL_BORDER
            if 3 <= col_i <= 10:
                cell.fill = FILL_INPUT
                cell.font = FONT_INPUT
                cell.protection = UNLOCKED
            else:
                cell.fill = fill
                cell.font = FONT_DATA_BOLD if col_i in (2, 15, 16, 19) else FONT_DATA
                cell.protection = LOCKED

            if col_i in (3, 4, 5, 9, 11, 12):
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i in (6, 7, 8, 10, 13, 14, 15, 16, 17):
                cell.number_format = "#,##0.00 €"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i == 18:
                cell.number_format = "0.0"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i in (1, 19):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    last_s3 = 11 + len(risk_rows)
    _add_native_table(ws3, f"TblLTB_{lang.upper()}", f"A11:S{last_s3}")
    _autosize_columns(ws3, {
        1: 11, 2: 20, 3: 14, 4: 14, 5: 14, 6: 13, 7: 15, 8: 15, 9: 13, 10: 14,
        11: 16, 12: 15, 13: 16, 14: 17, 15: 18, 16: 18, 17: 17, 18: 14, 19: 18,
    })

    # ------------------------------------------------------------------
    # HOJA 4: 04_MITIGATION_ROADMAP
    # ------------------------------------------------------------------
    ws4 = wb.create_sheet("04_MITIGATION_ROADMAP")
    _configure_sheet_base(ws4, c["s4_title"], c["s4_sub"], max_col=11, freeze_cell="A5")
    _style_table_header(ws4, 4, c["s4_headers"])

    for idx_offset, row in enumerate(BOM_SAMPLE_ROWS):
        r_idx = 5 + idx_offset
        fill = FILL_ZEBRA if r_idx % 2 == 1 else FILL_WHITE
        ws4.row_dimensions[r_idx].height = 22
        action_txt = row["action_es"] if lang == "es" else row["action_en"]
        vals = [
            f"='01_BOM_AML_EXPLORER'!A{r_idx}",
            f"='01_BOM_AML_EXPLORER'!B{r_idx}",
            f"='02_IEC62402_CRITICALITY'!H{r_idx}",
            f"='02_IEC62402_CRITICALITY'!I{r_idx}",
            row["owner"],
            row["cutoff"],
            action_txt,
            row["state"],
            row["capex_app"],
            row["capex_sp"],
            f"=J{r_idx}-I{r_idx}",
        ]
        for col_i, val in enumerate(vals, start=1):
            cell = ws4.cell(row=r_idx, column=col_i, value=val)
            cell.border = CELL_BORDER
            if col_i in (5, 6, 7, 8, 9, 10):
                cell.fill = FILL_INPUT
                cell.font = FONT_INPUT
                cell.protection = UNLOCKED
            else:
                cell.fill = fill
                cell.font = FONT_DATA_BOLD if col_i in (2, 3, 11) else FONT_DATA
                cell.protection = LOCKED

            if col_i == 3:
                cell.number_format = "0"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i in (9, 10, 11):
                cell.number_format = "#,##0.00 €"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i in (1, 4, 6, 8):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    _add_native_table(ws4, f"TblRoad_{lang.upper()}", f"A4:K{last_s1}")
    dv_plan = DataValidation(type="list", formula1='"Open,In Progress,Approved,Closed"', allow_blank=False)
    ws4.add_data_validation(dv_plan)
    dv_plan.add(f"H5:H{last_s1}")
    _autosize_columns(ws4, {1: 11, 2: 20, 3: 14, 4: 23, 5: 17, 6: 15, 7: 42, 8: 14, 9: 18, 10: 18, 11: 18})

    # ------------------------------------------------------------------
    # HOJA 5: 05_EXECUTIVE_DASHBOARD
    # ------------------------------------------------------------------
    ws5 = wb.create_sheet("05_EXECUTIVE_DASHBOARD")
    _configure_sheet_base(ws5, c["s5_title"], c["s5_sub"], max_col=9, freeze_cell="A4")

    kpi_specs = [
        (1, 3, c["kpi_labels"][0], f"=SUM('01_BOM_AML_EXPLORER'!M5:M{last_s1})", "#,##0 €", FILL_DANGER),
        (4, 6, c["kpi_labels"][1], f'=COUNTIF(\'02_IEC62402_CRITICALITY\'!I5:I{last_s1},"CRITICAL LTB REQUIRED")', "0", FILL_WARN),
        (7, 9, c["kpi_labels"][2], f"=SUM('03_LTB_VS_FFF_SIMULATOR'!O12:O{last_s3})", "#,##0 €", FILL_CYAN_LIGHT),
    ]
    kpi_specs_row2 = [
        (1, 3, c["kpi_labels"][3], f"=SUM('03_LTB_VS_FFF_SIMULATOR'!P12:P{last_s3})", "#,##0 €", FILL_VIOLET_LIGHT),
        (4, 6, c["kpi_labels"][4], f"=SUM('03_LTB_VS_FFF_SIMULATOR'!Q12:Q{last_s3})", "#,##0 €", FILL_OK),
        (7, 9, c["kpi_labels"][5], f"=AVERAGE('02_IEC62402_CRITICALITY'!H5:H{last_s1})", "0.0", FILL_ZEBRA),
    ]

    for block_start, specs in [(4, kpi_specs), (8, kpi_specs_row2)]:
        ws5.row_dimensions[block_start].height = 18
        ws5.row_dimensions[block_start + 1].height = 28
        for c1, c2, lbl, form, fmt, bg in specs:
            ws5.merge_cells(start_row=block_start, start_column=c1, end_row=block_start, end_column=c2)
            ws5.merge_cells(start_row=block_start + 1, start_column=c1, end_row=block_start + 1, end_column=c2)
            lc = ws5.cell(row=block_start, column=c1, value=lbl)
            lc.font = FONT_KPI_LABEL
            lc.fill = bg
            lc.alignment = Alignment(horizontal="center", vertical="center")
            vc = ws5.cell(row=block_start + 1, column=c1, value=form)
            vc.font = FONT_KPI_VAL
            vc.fill = bg
            vc.number_format = fmt
            vc.alignment = Alignment(horizontal="center", vertical="center")
            vc.protection = LOCKED
            for rr in (block_start, block_start + 1):
                for cc in range(c1, c2 + 1):
                    ws5.cell(row=rr, column=cc).border = CELL_BORDER

    # Tabla resumen por Estado de Ciclo de Vida (Filas 12-18)
    ws5.merge_cells("A12:D12")
    ws5["A12"] = c["sum_title"]
    ws5["A12"].font = FONT_SECTION
    ws5.row_dimensions[12].height = 22
    _style_table_header(ws5, 13, c["sum_headers"])

    statuses = ["Obsolete", "EOL", "PDN", "NRND", "Active"]
    for idx_s, st in enumerate(statuses, start=14):
        ws5.row_dimensions[idx_s].height = 20
        ws5.cell(row=idx_s, column=1, value=st).alignment = Alignment(horizontal="center", vertical="center")
        ws5.cell(row=idx_s, column=2, value=f'=COUNTIF(\'01_BOM_AML_EXPLORER\'!$K$5:$K${last_s1},A{idx_s})').number_format = "0"
        ws5.cell(row=idx_s, column=3, value=f'=SUMIF(\'01_BOM_AML_EXPLORER\'!$K$5:$K${last_s1},A{idx_s},\'01_BOM_AML_EXPLORER\'!$M$5:$M${last_s1})').number_format = "#,##0 €"
        ws5.cell(row=idx_s, column=4, value=f"=IF($C$19>0,C{idx_s}/$C$19,0)").number_format = "0.0%"
        for ci in range(1, 5):
            cell = ws5.cell(row=idx_s, column=ci)
            cell.font = FONT_DATA_BOLD if ci == 1 else FONT_DATA
            cell.fill = FILL_ZEBRA if idx_s % 2 == 0 else FILL_WHITE
            cell.border = CELL_BORDER
            cell.protection = LOCKED

    ws5.cell(row=19, column=1, value="TOTAL").font = FONT_DATA_BOLD
    ws5.cell(row=19, column=2, value="=SUM(B14:B18)").number_format = "0"
    ws5.cell(row=19, column=3, value="=SUM(C14:C18)").number_format = "#,##0 €"
    ws5.cell(row=19, column=4, value="=SUM(D14:D18)").number_format = "0.0%"
    for ci in range(1, 5):
        ws5.cell(row=19, column=ci).font = FONT_DATA_BOLD
        ws5.cell(row=19, column=ci).fill = FILL_CYAN_LIGHT
        ws5.cell(row=19, column=ci).border = CELL_BORDER

    # Gráfico de barras nativo (E12:I19)
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = c["chart_title"]
    chart.y_axis.title = "EUR"
    chart.legend = None
    data_ref = Reference(ws5, min_col=3, min_row=13, max_row=18)
    cats_ref = Reference(ws5, min_col=1, min_row=14, max_row=18)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.width = 16
    chart.height = 8
    ws5.add_chart(chart, "E12")

    # Tabla Comparativa Anti-Confusión: pack-stock (7 €) vs. pack-obs (19 €) (Filas 22-28)
    ws5.merge_cells("A22:I22")
    ws5["A22"] = c["cmp_title"]
    ws5["A22"].font = FONT_HEADER
    ws5["A22"].fill = FILL_NAVY
    ws5["A22"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[22].height = 24

    # Sub-headers combinados: A-B, C-E, F-I
    ws5.merge_cells("A23:B23")
    ws5.merge_cells("C23:E23")
    ws5.merge_cells("F23:I23")
    for col_start, title_h, bg_h in [(1, c["cmp_headers"][0], FILL_SLATE), (3, c["cmp_headers"][1], FILL_CYAN), (6, c["cmp_headers"][2], FILL_NAVY)]:
        cell = ws5.cell(row=23, column=col_start, value=title_h)
        cell.font = FONT_HEADER
        cell.fill = bg_h
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws5.row_dimensions[23].height = 22
    for cc in range(1, 10):
        ws5.cell(row=23, column=cc).border = CELL_BORDER

    for offset_c, (dim, v_stock, v_obs) in enumerate(c["cmp_rows"]):
        rr = 24 + offset_c
        ws5.row_dimensions[rr].height = 24
        ws5.merge_cells(f"A{rr}:B{rr}")
        ws5.merge_cells(f"C{rr}:E{rr}")
        ws5.merge_cells(f"F{rr}:I{rr}")
        ws5[f"A{rr}"] = dim
        ws5[f"A{rr}"].font = FONT_DATA_BOLD
        ws5[f"A{rr}"].fill = FILL_ZEBRA
        ws5[f"C{rr}"] = v_stock
        ws5[f"C{rr}"].font = FONT_DATA
        ws5[f"C{rr}"].fill = FILL_CYAN_LIGHT if offset_c % 2 == 0 else FILL_WHITE
        ws5[f"F{rr}"] = v_obs
        ws5[f"F{rr}"].font = FONT_DATA_BOLD if offset_c == 4 else FONT_DATA
        ws5[f"F{rr}"].fill = FILL_VIOLET_LIGHT if offset_c % 2 == 0 else FILL_WHITE
        for col_s in (1, 3, 6):
            ws5.cell(row=rr, column=col_s).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
        for cc in range(1, 10):
            ws5.cell(row=rr, column=cc).border = CELL_BORDER

    _autosize_columns(ws5, {1: 20, 2: 16, 3: 22, 4: 18, 5: 16, 6: 18, 7: 18, 8: 18, 9: 18})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    return output_path
