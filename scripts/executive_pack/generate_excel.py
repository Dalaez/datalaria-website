#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los libros Excel oficiales de alta dirección para Datalaria:
1. DAFO_Cuantitativo_CAME_Datalaria_ES.xlsx (Versión en Español)
2. Quantitative_SWOT_TOWS_Datalaria_EN.xlsx (Versión en Inglés)

Diseñado con el estándar de consultoría estratégica de primer nivel (McKinsey/BCG).
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.chart import ScatterChart, Reference, Series

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = "0F172A"     # Headers principales / Slate 900
COLOR_NAVY_MED = "1E293B"      # Subheaders / Slate 800
COLOR_BLUE_ACCENT = "2563EB"   # Azul corporativo / Blue 600
COLOR_TEAL_ACCENT = "0D9488"   # Teal / Verde agua 600
COLOR_WHITE = "FFFFFF"
COLOR_BG_LIGHT = "F8FAFC"      # Fondo celdas editables / Slate 50
COLOR_BG_CARD = "F1F5F9"       # Fondo tarjetas / Slate 100
COLOR_BORDER_LIGHT = "CBD5E1"  # Borde sutil / Slate 300
COLOR_BORDER_STRONG = "94A3B8" # Borde divisor / Slate 400

# Colores de Cuadrantes
COLOR_F_BG = "ECFDF5"          # Verde suave (Fortalezas / Strengths)
COLOR_F_BORDER = "10B981"
COLOR_F_TEXT = "065F46"

COLOR_D_BG = "FFFBEB"          # Ámbar suave (Debilidades / Weaknesses)
COLOR_D_BORDER = "F59E0B"
COLOR_D_TEXT = "92400E"

COLOR_O_BG = "EFF6FF"          # Azul suave (Oportunidades / Opportunities)
COLOR_O_BORDER = "3B82F6"
COLOR_O_TEXT = "1E40AF"

COLOR_A_BG = "FEF2F2"          # Rojo suave (Amenazas / Threats)
COLOR_A_BORDER = "EF4444"
COLOR_A_TEXT = "991B1B"

PASSWORD_PROTECT = "Datalaria2026"


def get_styles():
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
        top=Side(style='thin', color=COLOR_BORDER_STRONG),
        bottom=Side(style='double', color=COLOR_NAVY_DARK)
    )

    return {
        'title_font': Font(name='Segoe UI', size=15, bold=True, color=COLOR_WHITE),
        'title_fill': PatternFill(start_color=COLOR_NAVY_DARK, end_color=COLOR_NAVY_DARK, fill_type='solid'),
        'subtitle_font': Font(name='Segoe UI', size=10, italic=True, color="94A3B8"),
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
        'align_left': Alignment(horizontal='left', vertical='center'),
        'align_right': Alignment(horizontal='right', vertical='center'),
        'align_wrap': Alignment(horizontal='left', vertical='center', wrap_text=True),
    }


BENCHMARK_DATA_ES = {
    'F': [
        ("F01", "Margen operativo bruto superior al sector (+18.4%)", "Auditoría Financiera 2025: EBITDA 24.2% vs 17.5% media", 0.30, 5),
        ("F02", "Propiedad Intelectual y patentes de software predictivo", "3 patentes europeas registradas con vigencia > 2035", 0.25, 4),
        ("F03", "Retención neta de clientes enterprise (NRR) del 118%", "Cohorte 2023-2025: rotación de clientes < 2.1% anual", 0.20, 5),
        ("F04", "Infraestructura cloud certificada ISO 27001 y ENS Alto", "Auditoría de ciberseguridad sin no conformidades", 0.15, 4),
        ("F05", "Equipo de I+D interno con baja rotación de talento (<4%)", "Índice eNPS de 74 puntos en encuestas semestrales", 0.10, 4),
        ("F06", "", "", 0.00, None),
        ("F07", "", "", 0.00, None),
        ("F08", "", "", 0.00, None),
        ("F09", "", "", 0.00, None),
        ("F10", "", "", 0.00, None),
    ],
    'D': [
        ("D01", "Concentración de ingresos en 2 clientes clave (42% facturación)", "Riesgo de concentración de cartera auditado", 0.30, 4),
        ("D02", "Lead time de ciclo de ventas enterprise prolongado (8.5 meses)", "CRM Salesforce: promedio de oportunidad a cierre", 0.25, 3),
        ("D03", "Dependencia técnica de canal de hardware internacional", "Tiempos de entrega de sensores IoT > 14 semanas", 0.20, 4),
        ("D04", "Equipo comercial directo infradimensionado en mercados DACH", "Solo 2 ejecutivos para Alemania, Austria y Suiza", 0.15, 3),
        ("D05", "Deuda técnica en módulo legacy de facturación multi-divisa", "Horas de mantenimiento correctivo > 18% del sprint", 0.10, 3),
        ("D06", "", "", 0.00, None),
        ("D07", "", "", 0.00, None),
        ("D08", "", "", 0.00, None),
        ("D09", "", "", 0.00, None),
        ("D10", "", "", 0.00, None),
    ],
    'O': [
        ("O01", "Fondos de digitalización industrial y ayudas NextGen EU", "Subvenciones a fondo perdido para automatización", 0.30, 5),
        ("O02", "Demanda acelerada de IA explicable y observabilidad por compliance", "Regulación europea EU AI Act en vigor obligatorio", 0.25, 5),
        ("O03", "Consolidación de distribuidores B2B en LatAm (México/Colombia)", "Negociación avanzada de acuerdos de distribución", 0.20, 4),
        ("O04", "Obsolescencia de soluciones tradicionales de competidores Tier-2", "Clientes buscando sustitución activa de plataformas", 0.15, 4),
        ("O05", "Alianzas con integradores globales de sistemas (Accenture, Indra)", "Interés en incorporar motor predictivo en catálogo", 0.10, 4),
        ("O06", "", "", 0.00, None),
        ("O07", "", "", 0.00, None),
        ("O08", "", "", 0.00, None),
        ("O09", "", "", 0.00, None),
        ("O10", "", "", 0.00, None),
    ],
    'A': [
        ("A01", "Presión de precios por nuevos entrantes low-cost asiáticos", "Ofertas en licitaciones con descuentos del 35-40%", 0.30, 4),
        ("A02", "Escasez y encarecimiento salarial de ingenieros de IA senior", "Coste medio de contratación creció un 22% interanual", 0.25, 3),
        ("A03", "Incertidumbre arancelaria y fricciones en comercio exterior", "Posibles aranceles a tecnología y microelectrónica", 0.20, 3),
        ("A04", "Fusiones de competidores directos financiados por Private Equity", "Competidor directo adquirió 2 startups especializadas", 0.15, 4),
        ("A05", "Endurecimiento de directivas de ciberseguridad NIS2 para proveedores", "Exigencias de auditoría estricta de terceros", 0.10, 3),
        ("A06", "", "", 0.00, None),
        ("A07", "", "", 0.00, None),
        ("A08", "", "", 0.00, None),
        ("A09", "", "", 0.00, None),
        ("A10", "", "", 0.00, None),
    ],
}

BENCHMARK_DATA_EN = {
    'F': [
        ("S01", "Superior operating gross margin vs sector (+18.4%)", "2025 Financial Audit: EBITDA 24.2% vs 17.5% peer average", 0.30, 5),
        ("S02", "Proprietary IP and predictive software patents", "3 European and US patents granted through 2036", 0.25, 4),
        ("S03", "Enterprise Net Retention Rate (NRR) of 118%", "2023-2025 cohort: annual logo churn < 2.1%", 0.20, 5),
        ("S04", "ISO 27001 and SOC 2 Type II certified cloud infrastructure", "Zero non-conformities in annual security audit", 0.15, 4),
        ("S05", "High-retention internal R&D talent (turnover < 4%)", "eNPS score of 74 points in bi-annual team survey", 0.10, 4),
        ("S06", "", "", 0.00, None),
        ("S07", "", "", 0.00, None),
        ("S08", "", "", 0.00, None),
        ("S09", "", "", 0.00, None),
        ("S10", "", "", 0.00, None),
    ],
    'D': [
        ("W01", "Revenue concentration in 2 key enterprise clients (42% ARR)", "High single-client dependency identified in audit", 0.30, 4),
        ("W02", "Long enterprise sales cycle duration (8.5 months average)", "Salesforce CRM: qualified pipeline to deal close", 0.25, 3),
        ("W03", "Supply chain dependency on international IoT hardware vendors", "Sensor delivery lead times currently > 14 weeks", 0.20, 4),
        ("W04", "Undersized direct commercial sales force in DACH markets", "Only 2 account executives covering Germany/Switzerland", 0.15, 3),
        ("W05", "Technical debt in legacy multi-currency billing engine", "Maintenance hours > 18% of engineering sprint capacity", 0.10, 3),
        ("W06", "", "", 0.00, None),
        ("W07", "", "", 0.00, None),
        ("W08", "", "", 0.00, None),
        ("W09", "", "", 0.00, None),
        ("W10", "", "", 0.00, None),
    ],
    'O': [
        ("O01", "Industrial digital transformation & automation capital subsidies", "Non-repayable public capital programs for smart factories", 0.30, 5),
        ("O02", "Surging compliance demand for explainable AI & observability", "EU AI Act and international governance frameworks", 0.25, 5),
        ("O03", "B2B distributor network consolidation in LatAm & US Sunbelt", "Advanced negotiations for master distribution partnership", 0.20, 4),
        ("O04", "Obsolescence and vendor fatigue among Tier-2 legacy solutions", "Enterprise RFP wave seeking modern cloud alternatives", 0.15, 4),
        ("O05", "Co-sell partnerships with Tier-1 System Integrators", "Interest from leading consultancies to package our IP", 0.10, 4),
        ("O06", "", "", 0.00, None),
        ("O07", "", "", 0.00, None),
        ("O08", "", "", 0.00, None),
        ("O09", "", "", 0.00, None),
        ("O10", "", "", 0.00, None),
    ],
    'A': [
        ("T01", "Aggressive price erosion from low-cost Asian competitors", "Public tenders experiencing 35-40% price discounting", 0.30, 4),
        ("T02", "Acute talent shortage & wage inflation for senior AI engineers", "Average recruiting salary costs up 22% year-on-year", 0.25, 3),
        ("T03", "Tariff volatility & international cross-border friction", "Potential duties on microelectronics & specialized compute", 0.20, 3),
        ("T04", "M&A roll-up of direct niche competitors backed by PE funds", "Nearest competitor recently acquired two vertical startups", 0.15, 4),
        ("T05", "Stringent supply chain cybersecurity directives (NIS2/DORA)", "Stricter third-party compliance requirements", 0.10, 3),
        ("T06", "", "", 0.00, None),
        ("T07", "", "", 0.00, None),
        ("T08", "", "", 0.00, None),
        ("T09", "", "", 0.00, None),
        ("T10", "", "", 0.00, None),
    ],
}


def build_assessment_sheet(ws, lang='ES', styles=None):
    ws.title = "Evaluación FODA" if lang == 'ES' else "SWOT Weighted Assessment"
    ws.views.sheetView[0].showGridLines = True

    texts = {
        'ES': {
            'title': "DATALARIA | EVALUACIÓN CUANTITATIVA FODA",
            'subtitle': "Asignación de pesos relativos (Σ = 100%) y calificación de impacto (1 a 5). Puntuación ponderada calculada dinámicamente. Filas vacías no computan.",
            'q_f': "1. FORTALEZAS (Capacidades y Activos Internos Clave)",
            'q_d': "2. DEBILIDADES (Vulnerabilidades y Cuellos de Botella Internos)",
            'q_o': "3. OPORTUNIDADES (Tendencias y Vientos de Cola Externos)",
            'q_a': "4. AMENAZAS (Riesgos de Mercado y Presiones Competitivas)",
            'col_code': "Código",
            'col_desc': "Factor Estratégico Evaluado (Editable)",
            'col_base': "Métrica Base / Evidencia Cuantitativa",
            'col_weight': "Peso Relativo (wi)",
            'col_rate': "Impacto (1-5)",
            'col_score': "Puntuación Ponderada",
            'lbl_total': "TOTAL PONDERADO DEL CUADRANTE",
            'note_empty': "— Sin datos —",
            'ok_msg': "✓ 100% Correcto",
            'err_msg': "⚠ Suma: ",
            'must_100': " (debe sumar 100%)",
        },
        'EN': {
            'title': "DATALARIA | QUANTITATIVE SWOT ASSESSMENT",
            'subtitle': "Relative weight allocation (Σ = 100%) and impact rating (1 to 5). Weighted scores calculate dynamically. Blank rows safely ignored.",
            'q_f': "1. STRENGTHS (Core Internal Capabilities & Strategic Assets)",
            'q_d': "2. WEAKNESSES (Internal Vulnerabilities & Operational Bottlenecks)",
            'q_o': "3. OPPORTUNITIES (External Tailwinds & Emerging Market Spaces)",
            'q_a': "4. THREATS (Market Risks & External Headwinds)",
            'col_code': "Code",
            'col_desc': "Strategic Factor Evaluated (Editable)",
            'col_base': "Baseline Metric / Quantitative Evidence",
            'col_weight': "Weight (wi)",
            'col_rate': "Impact (1-5)",
            'col_score': "Weighted Score",
            'lbl_total': "TOTAL WEIGHTED SCORE",
            'note_empty': "— No data —",
            'ok_msg': "✓ 100% Valid",
            'err_msg': "⚠ Sum: ",
            'must_100': " (must equal 100%)",
        }
    }[lang]

    ws.merge_cells('A2:F2')
    ws['A2'] = texts['title']
    ws['A2'].font = styles['title_font']
    ws['A2'].fill = styles['title_fill']
    ws['A2'].alignment = styles['align_left']
    ws.row_dimensions[2].height = 36

    ws.merge_cells('A3:F3')
    ws['A3'] = texts['subtitle']
    ws['A3'].font = styles['subtitle_font']
    ws['A3'].alignment = styles['align_left']
    ws.row_dimensions[3].height = 20

    data = BENCHMARK_DATA_ES if lang == 'ES' else BENCHMARK_DATA_EN

    quadrants = [
        ('F', texts['q_f'], COLOR_F_BG, COLOR_F_BORDER, COLOR_F_TEXT),
        ('D', texts['q_d'], COLOR_D_BG, COLOR_D_BORDER, COLOR_D_TEXT),
        ('O', texts['q_o'], COLOR_O_BG, COLOR_O_BORDER, COLOR_O_TEXT),
        ('A', texts['q_a'], COLOR_A_BG, COLOR_A_BORDER, COLOR_A_TEXT),
    ]

    current_row = 5
    summary_rows = {}

    for q_code, q_title, q_bg, q_border, q_text_col in quadrants:
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=6)
        cell_q = ws.cell(row=current_row, column=1, value=q_title)
        cell_q.font = Font(name='Segoe UI', size=11, bold=True, color=q_text_col)
        cell_q.fill = PatternFill(start_color=q_bg, end_color=q_bg, fill_type='solid')
        cell_q.alignment = styles['align_left']
        ws.row_dimensions[current_row].height = 26
        current_row += 1

        headers = [
            (1, texts['col_code'], 10, styles['align_center']),
            (2, texts['col_desc'], 44, styles['align_left']),
            (3, texts['col_base'], 38, styles['align_left']),
            (4, texts['col_weight'], 16, styles['align_right']),
            (5, texts['col_rate'], 14, styles['align_center']),
            (6, texts['col_score'], 18, styles['align_right']),
        ]
        for col_idx, h_text, width, align in headers:
            c = ws.cell(row=current_row, column=col_idx, value=h_text)
            c.font = styles['header_font']
            c.fill = styles['header_fill']
            c.alignment = align
            c.border = styles['header_border']
            c.protection = Protection(locked=True)
            ws.column_dimensions[get_column_letter(col_idx)].width = max(ws.column_dimensions[get_column_letter(col_idx)].width or 0, width)
        ws.row_dimensions[current_row].height = 22
        current_row += 1

        start_factor_row = current_row
        factors = data[q_code]

        for item in factors:
            f_code, f_desc, f_metric, f_w, f_r = item

            c_code = ws.cell(row=current_row, column=1, value=f_code)
            c_code.font = styles['code_font']
            c_code.alignment = styles['align_center']
            c_code.border = styles['thin_border']
            c_code.fill = styles['calc_fill']
            c_code.protection = Protection(locked=True)

            c_desc = ws.cell(row=current_row, column=2, value=f_desc if f_desc else None)
            c_desc.font = styles['cell_font']
            c_desc.alignment = styles['align_left']
            c_desc.border = styles['thin_border']
            c_desc.fill = styles['input_fill']
            c_desc.protection = Protection(locked=False)

            c_met = ws.cell(row=current_row, column=3, value=f_metric if f_metric else None)
            c_met.font = styles['cell_font']
            c_met.alignment = styles['align_left']
            c_met.border = styles['thin_border']
            c_met.fill = styles['input_fill']
            c_met.protection = Protection(locked=False)

            c_w = ws.cell(row=current_row, column=4, value=f_w if f_w > 0 else None)
            c_w.font = styles['cell_font']
            c_w.number_format = '0.0%'
            c_w.alignment = styles['align_right']
            c_w.border = styles['thin_border']
            c_w.fill = styles['input_fill']
            c_w.protection = Protection(locked=False)

            c_r = ws.cell(row=current_row, column=5, value=f_r if f_r is not None else None)
            c_r.font = styles['cell_font']
            c_r.number_format = '0'
            c_r.alignment = styles['align_center']
            c_r.border = styles['thin_border']
            c_r.fill = styles['input_fill']
            c_r.protection = Protection(locked=False)

            formula_score = f'=IF(OR(B{current_row}="", D{current_row}=""), 0, D{current_row}*E{current_row})'
            c_score = ws.cell(row=current_row, column=6, value=formula_score)
            c_score.font = styles['cell_bold']
            c_score.number_format = '0.00'
            c_score.alignment = styles['align_right']
            c_score.border = styles['thin_border']
            c_score.fill = styles['calc_fill']
            c_score.protection = Protection(locked=True)

            ws.row_dimensions[current_row].height = 20
            current_row += 1

        end_factor_row = current_row - 1
        total_row = current_row
        summary_rows[q_code] = total_row

        ws.cell(row=total_row, column=1, value="").border = styles['total_border']
        ws.cell(row=total_row, column=2, value="").border = styles['total_border']

        c_tot_lbl = ws.cell(row=total_row, column=3, value=texts['lbl_total'])
        c_tot_lbl.font = styles['cell_bold']
        c_tot_lbl.alignment = styles['align_right']
        c_tot_lbl.border = styles['total_border']
        c_tot_lbl.fill = styles['total_fill']
        c_tot_lbl.protection = Protection(locked=True)

        formula_sum_w = f'=SUM(D{start_factor_row}:D{end_factor_row})'
        c_tot_w = ws.cell(row=total_row, column=4, value=formula_sum_w)
        c_tot_w.font = Font(name='Segoe UI', size=10, bold=True, color=q_text_col)
        c_tot_w.number_format = '0.0%'
        c_tot_w.alignment = styles['align_right']
        c_tot_w.border = styles['total_border']
        c_tot_w.fill = styles['total_fill']
        c_tot_w.protection = Protection(locked=True)

        formula_val = (
            f'=IF(COUNTBLANK(D{start_factor_row}:D{end_factor_row})=10, "{texts["note_empty"]}", '
            f'IF(ROUND(SUM(D{start_factor_row}:D{end_factor_row}),2)=1, "{texts["ok_msg"]}", '
            f'"{texts["err_msg"]}" & TEXT(SUM(D{start_factor_row}:D{end_factor_row}),"0.0%") & "{texts["must_100"]}"))'
        )
        c_tot_val = ws.cell(row=total_row, column=5, value=formula_val)
        c_tot_val.font = styles['cell_bold']
        c_tot_val.alignment = styles['align_center']
        c_tot_val.border = styles['total_border']
        c_tot_val.fill = styles['total_fill']
        c_tot_val.protection = Protection(locked=True)

        formula_sum_s = f'=SUM(F{start_factor_row}:F{end_factor_row})'
        c_tot_s = ws.cell(row=total_row, column=6, value=formula_sum_s)
        c_tot_s.font = Font(name='Segoe UI', size=11, bold=True, color=q_text_col)
        c_tot_s.number_format = '0.00'
        c_tot_s.alignment = styles['align_right']
        c_tot_s.border = styles['total_border']
        c_tot_s.fill = styles['total_fill']
        c_tot_s.protection = Protection(locked=True)

        ws.row_dimensions[total_row].height = 24
        current_row += 3

    ws.protection.set_password(PASSWORD_PROTECT)
    ws.protection.sheet = True
    ws.protection.enable()
    ws.protection.selectLockedCells = True
    ws.protection.selectUnlockedCells = True
    ws.protection.insertRows = True
    ws.protection.deleteRows = True

    return summary_rows


def build_dashboard_sheet(ws, summary_rows, lang='ES', styles=None):
    ws.title = "Dashboard Ejecutivo" if lang == 'ES' else "Executive Dashboard"
    ws.views.sheetView[0].showGridLines = True
    sheet_ref = "'Evaluación FODA'" if lang == 'ES' else "'SWOT Weighted Assessment'"

    texts = {
        'ES': {
            'title': "DATALARIA | EXECUTIVE DECISION PACK - CUADRO DE MANDO ESTRATÉGICO",
            'subtitle': "Diagnóstico cuantitativo en tiempo real para Comité de Dirección (C-Level). Modelo vectorial de decisión.",
            'sec_kpi': "1. RESUMEN EJECUTIVO DE PUNTUACIONES CUANTITATIVAS",
            'sec_pos': "2. VECTOR DE FUERZA Y POSTURA ESTRATÉGICA DOMINANTE",
            'sec_rec': "3. SÍNTESIS ESTRATÉGICA Y RECOMENDACIÓN PARA EL CONSEJO",
            'lbl_sf': "Puntuación Total Fortalezas (SF)",
            'lbl_sd': "Puntuación Total Debilidades (SD)",
            'lbl_so': "Puntuación Total Oportunidades (SO)",
            'lbl_sa': "Puntuación Total Amenazas (SA)",
            'lbl_x': "Posición Interna Neta (X = SF - SD)",
            'lbl_y': "Presión Externa Neta (Y = SO - SA)",
            'lbl_v': "Magnitud del Vector Estratégico (||V||)",
            'lbl_posture': "POSTURA ESTRATÉGICA DOMINANTE",
            'posture_of': "OFENSIVA / CRECIMIENTO (Maxi-Maxi)",
            'posture_def': "DEFENSIVA / PROTECCIÓN (Maxi-Mini)",
            'posture_re': "REORIENTACIÓN / ADAPTACIÓN (Mini-Maxi)",
            'posture_sup': "SUPERVIVENCIA / CONTENCIÓN (Mini-Mini)",
            'rec_of': "Postura Ofensiva Validada: La organización cuenta con solidez interna superior a sus vulnerabilidades y un entorno externo favorable. Máxima asignación de CAPEX a captura de cuota, innovación agresiva y expansión internacional.",
            'rec_def': "Postura Defensiva: Las capacidades internas son robustas pero el entorno macro y competitivo presenta amenazas críticas. Priorizar blindaje de contratos clave, aseguramiento de márgenes y diversificación de proveedores.",
            'rec_re': "Postura de Reorientación: Existen catalizadores externos extraordinarios que la organización no puede capturar plenamente debido a cuellos de botella internos. Priorizar transformación operativa y reducción de deuda técnica.",
            'rec_sup': "Postura de Supervivencia: Amenazas externas severas combinadas con debilidades críticas internas. Ejecutar plan de contención de costes, desinversión selectiva de activos no core y renegociación de pasivos.",
            'quadrant_title': "DISTRIBUCIÓN EN MATRIZ CARTESIANA",
        },
        'EN': {
            'title': "DATALARIA | EXECUTIVE DECISION PACK - STRATEGIC DASHBOARD",
            'subtitle': "Real-time quantitative C-Level diagnosis for Board meetings. Vector-based decision modeling.",
            'sec_kpi': "1. EXECUTIVE SUMMARY OF QUANTITATIVE SCORES",
            'sec_pos': "2. STRATEGIC FORCE VECTOR & DOMINANT POSTURE",
            'sec_rec': "3. EXECUTIVE BOARD SYNTHESIS & STRATEGIC RECOMMENDATION",
            'lbl_sf': "Total Strengths Score (SS)",
            'lbl_sd': "Total Weaknesses Score (SW)",
            'lbl_so': "Total Opportunities Score (SO)",
            'lbl_sa': "Total Threats Score (ST)",
            'lbl_x': "Net Internal Position (X = SS - SW)",
            'lbl_y': "Net External Pressure (Y = SO - ST)",
            'lbl_v': "Strategic Vector Magnitude (||V||)",
            'lbl_posture': "DOMINANT STRATEGIC POSTURE",
            'posture_of': "OFFENSIVE / EXPANSION (Maxi-Maxi)",
            'posture_def': "DEFENSIVE / FORTRESS (Maxi-Mini)",
            'posture_re': "REORIENTATION / TURNAROUND (Mini-Maxi)",
            'posture_sup': "SURVIVAL / RESTRUCTURING (Mini-Mini)",
            'rec_of': "Offensive Posture Validated: Internal strengths significantly outpace weaknesses within a receptive external environment. Direct maximum capital allocation to market share capture, aggressive R&D, and global scaling.",
            'rec_def': "Defensive Posture: Internal competencies remain strong, but macro headwinds and competitive threats are severe. Prioritize contractual moat building, margin defense, and supplier de-risking.",
            'rec_re': "Reorientation Posture: High external market tailwinds exist, yet internal bottlenecks prevent full value capture. Expedite operational restructuring, talent realignment, and technical debt elimination.",
            'rec_sup': "Survival Posture: Critical external threats compound severe internal vulnerabilities. Enforce strict OPEX containment, divest non-core assets, and restructure liabilities to preserve enterprise solvency.",
            'quadrant_title': "CARTESIAN MATRIX POSITIONING",
        }
    }[lang]

    ws.merge_cells('A2:H2')
    ws['A2'] = texts['title']
    ws['A2'].font = styles['title_font']
    ws['A2'].fill = styles['title_fill']
    ws['A2'].alignment = styles['align_left']
    ws.row_dimensions[2].height = 36

    ws.merge_cells('A3:H3')
    ws['A3'] = texts['subtitle']
    ws['A3'].font = styles['subtitle_font']
    ws['A3'].alignment = styles['align_left']
    ws.row_dimensions[3].height = 20

    ws.merge_cells('A5:C5')
    ws['A5'] = texts['sec_kpi']
    ws['A5'].font = styles['section_font']
    ws['A5'].fill = styles['section_fill']
    ws.row_dimensions[5].height = 24

    kpi_items = [
        (6, texts['lbl_sf'], f"={sheet_ref}!F{summary_rows['F']}", COLOR_F_BG, COLOR_F_TEXT),
        (7, texts['lbl_sd'], f"={sheet_ref}!F{summary_rows['D']}", COLOR_D_BG, COLOR_D_TEXT),
        (8, texts['lbl_so'], f"={sheet_ref}!F{summary_rows['O']}", COLOR_O_BG, COLOR_O_TEXT),
        (9, texts['lbl_sa'], f"={sheet_ref}!F{summary_rows['A']}", COLOR_A_BG, COLOR_A_TEXT),
    ]

    for row_idx, label, formula, bg, text_col in kpi_items:
        ws.cell(row=row_idx, column=1, value="").border = styles['thin_border']
        c_lbl = ws.cell(row=row_idx, column=2, value=label)
        c_lbl.font = styles['cell_font']
        c_lbl.border = styles['thin_border']
        c_lbl.fill = styles['calc_fill']
        c_lbl.protection = Protection(locked=True)

        c_val = ws.cell(row=row_idx, column=3, value=formula)
        c_val.font = Font(name='Segoe UI', size=11, bold=True, color=text_col)
        c_val.number_format = '0.00'
        c_val.alignment = styles['align_right']
        c_val.border = styles['thin_border']
        c_val.fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')
        c_val.protection = Protection(locked=True)
        ws.row_dimensions[row_idx].height = 22

    ws.merge_cells('A11:C11')
    ws['A11'] = texts['sec_pos']
    ws['A11'].font = styles['section_font']
    ws['A11'].fill = styles['section_fill']
    ws.row_dimensions[11].height = 24

    vector_items = [
        (12, texts['lbl_x'], "=C6-C7"),
        (13, texts['lbl_y'], "=C8-C9"),
        (14, texts['lbl_v'], "=SQRT(C12^2+C13^2)"),
    ]

    for row_idx, label, formula in vector_items:
        ws.cell(row=row_idx, column=1, value="").border = styles['thin_border']
        c_lbl = ws.cell(row=row_idx, column=2, value=label)
        c_lbl.font = styles['cell_bold']
        c_lbl.border = styles['thin_border']
        c_lbl.fill = styles['calc_fill']
        c_lbl.protection = Protection(locked=True)

        c_val = ws.cell(row=row_idx, column=3, value=formula)
        c_val.font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
        c_val.number_format = '+0.00;-0.00;0.00' if row_idx in [12, 13] else '0.00'
        c_val.alignment = styles['align_right']
        c_val.border = styles['thin_border']
        c_val.fill = styles['total_fill']
        c_val.protection = Protection(locked=True)
        ws.row_dimensions[row_idx].height = 22

    ws.merge_cells('A16:C16')
    c_post_hdr = ws.cell(row=16, column=1, value=texts['lbl_posture'])
    c_post_hdr.font = styles['header_font']
    c_post_hdr.fill = styles['header_fill']
    c_post_hdr.alignment = styles['align_center']
    ws.row_dimensions[16].height = 24

    formula_posture = (
        f'=IF(AND(C12>=0, C13>=0), "{texts["posture_of"]}", '
        f'IF(AND(C12>=0, C13<0), "{texts["posture_def"]}", '
        f'IF(AND(C12<0, C13>=0), "{texts["posture_re"]}", "{texts["posture_sup"]}")))'
    )
    ws.merge_cells('A17:C17')
    c_post_val = ws.cell(row=17, column=1, value=formula_posture)
    c_post_val.font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_NAVY_DARK)
    c_post_val.fill = PatternFill(start_color="FEF08A", end_color="FEF08A", fill_type='solid')
    c_post_val.alignment = styles['align_center']
    c_post_val.border = Border(
        left=Side(style='medium', color=COLOR_NAVY_DARK),
        right=Side(style='medium', color=COLOR_NAVY_DARK),
        top=Side(style='medium', color=COLOR_NAVY_DARK),
        bottom=Side(style='medium', color=COLOR_NAVY_DARK)
    )
    c_post_val.protection = Protection(locked=True)
    ws.row_dimensions[17].height = 36

    ws.merge_cells('A19:H19')
    ws['A19'] = texts['sec_rec']
    ws['A19'].font = styles['section_font']
    ws['A19'].fill = styles['section_fill']
    ws.row_dimensions[19].height = 24

    formula_rec = (
        f'=IF(AND(C12>=0, C13>=0), "{texts["rec_of"]}", '
        f'IF(AND(C12>=0, C13<0), "{texts["rec_def"]}", '
        f'IF(AND(C12<0, C13>=0), "{texts["rec_re"]}", "{texts["rec_sup"]}")))'
    )
    ws.merge_cells('A20:H21')
    c_rec_box = ws.cell(row=20, column=1, value=formula_rec)
    c_rec_box.font = Font(name='Segoe UI', size=10, italic=False, color=COLOR_NAVY_DARK)
    c_rec_box.fill = PatternFill(start_color=COLOR_BG_LIGHT, end_color=COLOR_BG_LIGHT, fill_type='solid')
    c_rec_box.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    c_rec_box.border = styles['thin_border']
    c_rec_box.protection = Protection(locked=True)
    ws.row_dimensions[20].height = 28
    ws.row_dimensions[21].height = 28

    ws.merge_cells('E5:H5')
    ws['E5'] = texts['quadrant_title']
    ws['E5'].font = styles['section_font']
    ws['E5'].fill = styles['section_fill']
    ws['E5'].alignment = styles['align_center']

    ws.merge_cells('E6:F9')
    c_re = ws.cell(row=6, column=5, value=f"{texts['posture_re']}\n\nX < 0 (Debilidades dominan)\nY ≥ 0 (Oportunidades altas)")
    c_re.font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_D_TEXT)
    c_re.fill = PatternFill(start_color=COLOR_D_BG, end_color=COLOR_D_BG, fill_type='solid')
    c_re.alignment = styles['align_center']
    c_re.border = styles['thin_border']

    ws.merge_cells('G6:H9')
    c_of = ws.cell(row=6, column=7, value=f"{texts['posture_of']}\n\nX ≥ 0 (Fortalezas dominan)\nY ≥ 0 (Oportunidades altas)")
    c_of.font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_F_TEXT)
    c_of.fill = PatternFill(start_color=COLOR_F_BG, end_color=COLOR_F_BG, fill_type='solid')
    c_of.alignment = styles['align_center']
    c_of.border = styles['thin_border']

    ws.merge_cells('E11:F14')
    c_sup = ws.cell(row=11, column=5, value=f"{texts['posture_sup']}\n\nX < 0 (Debilidades dominan)\nY < 0 (Amenazas críticas)")
    c_sup.font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_A_TEXT)
    c_sup.fill = PatternFill(start_color=COLOR_A_BG, end_color=COLOR_A_BG, fill_type='solid')
    c_sup.alignment = styles['align_center']
    c_sup.border = styles['thin_border']

    ws.merge_cells('G11:H14')
    c_def = ws.cell(row=11, column=7, value=f"{texts['posture_def']}\n\nX ≥ 0 (Fortalezas dominan)\nY < 0 (Amenazas críticas)")
    c_def.font = Font(name='Segoe UI', size=9, bold=True, color=COLOR_O_TEXT)
    c_def.fill = PatternFill(start_color=COLOR_O_BG, end_color=COLOR_O_BG, fill_type='solid')
    c_def.alignment = styles['align_center']
    c_def.border = styles['thin_border']

    ws.merge_cells('E10:H10')
    c_axis = ws.cell(row=10, column=5, value="◄── INTERNO: DEBILIDADES (-X)  |  FORTALEZAS (+X) ──►")
    c_axis.font = Font(name='Segoe UI', size=8, bold=True, color="64748B")
    c_axis.alignment = styles['align_center']

    ws.merge_cells('E16:H17')
    c_coord = ws.cell(row=16, column=5, value='="VECTOR ACTUAL: Coordenadas (" & TEXT(C12,"+0.00;-0.00;0.00") & " , " & TEXT(C13,"+0.00;-0.00;0.00") & ")  •  Impulso: " & TEXT(C14,"0.00")')
    c_coord.font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_NAVY_DARK)
    c_coord.fill = styles['calc_fill']
    c_coord.alignment = styles['align_center']
    c_coord.border = styles['thin_border']

    col_widths = {1: 4, 2: 36, 3: 16, 4: 4, 5: 22, 6: 22, 7: 22, 8: 22}
    for c_i, w in col_widths.items():
        ws.column_dimensions[get_column_letter(c_i)].width = w

    chart = ScatterChart()
    chart.title = "Matriz Cartesiana de Posicionamiento Estratégico (X, Y)" if lang == 'ES' else "Cartesian Strategic Positioning Matrix (X, Y)"
    chart.style = 13
    chart.x_axis.title = "Posición Interna Neta (X = F - D)" if lang == 'ES' else "Net Internal Position (X = S - W)"
    chart.y_axis.title = "Presión Externa Neta (Y = O - A)" if lang == 'ES' else "Net External Pressure (Y = O - T)"
    chart.width = 16
    chart.height = 10
    chart.x_axis.scaling.min = -5
    chart.x_axis.scaling.max = 5
    chart.y_axis.scaling.min = -5
    chart.y_axis.scaling.max = 5

    xvalues = Reference(ws, min_col=3, min_row=12, max_row=12)
    yvalues = Reference(ws, min_col=3, min_row=13, max_row=13)
    series = Series(yvalues, xvalues, title_from_data=False)
    series.marker.symbol = 'circle'
    series.marker.size = 14
    series.marker.graphicalProperties.solidFill = COLOR_BLUE_ACCENT
    series.marker.graphicalProperties.line.solidFill = COLOR_NAVY_DARK
    chart.series.append(series)
    chart.legend = None

    ws.add_chart(chart, 'A23')

    ws.protection.set_password(PASSWORD_PROTECT)
    ws.protection.sheet = True
    ws.protection.enable()
    ws.protection.selectLockedCells = True
    ws.protection.selectUnlockedCells = True


def build_cross_sheet(ws, lang='ES', styles=None):
    ws.title = "Matriz de Cruce" if lang == 'ES' else "TOWS Cross-Impact Matrix"
    ws.views.sheetView[0].showGridLines = True
    sheet_ref = "'Evaluación FODA'" if lang == 'ES' else "'SWOT Weighted Assessment'"

    texts = {
        'ES': {
            'title': "DATALARIA | MATRIZ DE CRUCE CUANTITATIVO (CAME / TOWS)",
            'subtitle': "Evaluación de impacto cruzado (0 = Nulo, 1 = Débil, 2 = Moderado, 3 = Crítico / Sinérgico). Identifica factores catalizadores y vulnerabilidades críticas.",
            'lbl_internal': "FACTORES INTERNOS (FILAS)",
            'lbl_external_o': "OPORTUNIDADES (O01 - O10)",
            'lbl_external_a': "AMENAZAS (A01 - A10)",
            'sec_f': "FORTALEZAS",
            'sec_d': "DEBILIDADES",
            'col_tot': "Total Fila",
            'row_tot': "Total Columna",
            'kpi_so': "Sinergia Ofensiva Total (F x O)",
            'kpi_st': "Impacto Defensivo Total (F x A)",
            'kpi_wo': "Cuellos de Botella (D x O)",
            'kpi_wt': "Vulnerabilidad Crítica (D x A)",
        },
        'EN': {
            'title': "DATALARIA | TOWS QUANTITATIVE CROSS-IMPACT MATRIX",
            'subtitle': "Cross-impact scale (0 = None, 1 = Low, 2 = Moderate, 3 = Critical / Synergistic). Identifies primary catalysts and acute operational vulnerabilities.",
            'lbl_internal': "INTERNAL FACTORS (ROWS)",
            'lbl_external_o': "OPPORTUNITIES (O01 - O10)",
            'lbl_external_a': "THREATS (T01 - T10)",
            'sec_f': "STRENGTHS",
            'sec_d': "WEAKNESSES",
            'col_tot': "Row Total",
            'row_tot': "Column Total",
            'kpi_so': "Total Offensive Synergy (S x O)",
            'kpi_st': "Total Defensive Moat (S x T)",
            'kpi_wo': "Turnaround Friction (W x O)",
            'kpi_wt': "Critical Vulnerability (W x T)",
        }
    }[lang]

    ws.merge_cells('A2:W2')
    ws['A2'] = texts['title']
    ws['A2'].font = styles['title_font']
    ws['A2'].fill = styles['title_fill']
    ws['A2'].alignment = styles['align_left']
    ws.row_dimensions[2].height = 36

    ws.merge_cells('A3:W3')
    ws['A3'] = texts['subtitle']
    ws['A3'].font = styles['subtitle_font']
    ws['A3'].alignment = styles['align_left']
    ws.row_dimensions[3].height = 20

    ws.merge_cells('C5:L5')
    ws['C5'] = texts['lbl_external_o']
    ws['C5'].font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_O_TEXT)
    ws['C5'].fill = PatternFill(start_color=COLOR_O_BG, end_color=COLOR_O_BG, fill_type='solid')
    ws['C5'].alignment = styles['align_center']

    ws.merge_cells('M5:V5')
    ws['M5'] = texts['lbl_external_a']
    ws['M5'].font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_A_TEXT)
    ws['M5'].fill = PatternFill(start_color=COLOR_A_BG, end_color=COLOR_A_BG, fill_type='solid')
    ws['M5'].alignment = styles['align_center']

    ws.cell(row=6, column=1, value="ID").font = styles['header_font']
    ws.cell(row=6, column=1).fill = styles['header_fill']
    ws.cell(row=6, column=1).alignment = styles['align_center']
    ws.column_dimensions['A'].width = 8

    ws.cell(row=6, column=2, value=texts['lbl_internal']).font = styles['header_font']
    ws.cell(row=6, column=2).fill = styles['header_fill']
    ws.cell(row=6, column=2).alignment = styles['align_left']
    ws.column_dimensions['B'].width = 34

    o_prefix = "O"
    for i in range(1, 11):
        col_idx = 2 + i
        code = f"{o_prefix}{i:02d}"
        c = ws.cell(row=6, column=col_idx, value=code)
        c.font = Font(name='Consolas', size=9, bold=True, color=COLOR_O_TEXT)
        c.fill = PatternFill(start_color=COLOR_O_BG, end_color=COLOR_O_BG, fill_type='solid')
        c.alignment = styles['align_center']
        c.border = styles['thin_border']
        ws.column_dimensions[get_column_letter(col_idx)].width = 7

    a_prefix = "A" if lang == 'ES' else "T"
    for i in range(1, 11):
        col_idx = 12 + i
        code = f"{a_prefix}{i:02d}"
        c = ws.cell(row=6, column=col_idx, value=code)
        c.font = Font(name='Consolas', size=9, bold=True, color=COLOR_A_TEXT)
        c.fill = PatternFill(start_color=COLOR_A_BG, end_color=COLOR_A_BG, fill_type='solid')
        c.alignment = styles['align_center']
        c.border = styles['thin_border']
        ws.column_dimensions[get_column_letter(col_idx)].width = 7

    c_tot_hdr = ws.cell(row=6, column=23, value=texts['col_tot'])
    c_tot_hdr.font = styles['header_font']
    c_tot_hdr.fill = styles['header_fill']
    c_tot_hdr.alignment = styles['align_center']
    ws.column_dimensions['W'].width = 12
    ws.row_dimensions[6].height = 24

    matrix_F = [
        [3, 3, 2, 3, 2, 0, 0, 0, 0, 0,  2, 1, 1, 3, 2, 0, 0, 0, 0, 0],
        [3, 3, 1, 2, 3, 0, 0, 0, 0, 0,  1, 2, 1, 2, 3, 0, 0, 0, 0, 0],
        [2, 3, 3, 2, 2, 0, 0, 0, 0, 0,  2, 1, 2, 2, 2, 0, 0, 0, 0, 0],
        [2, 3, 2, 3, 3, 0, 0, 0, 0, 0,  2, 1, 1, 1, 3, 0, 0, 0, 0, 0],
        [2, 2, 1, 1, 2, 0, 0, 0, 0, 0,  1, 3, 1, 2, 1, 0, 0, 0, 0, 0],
        [0]*20, [0]*20, [0]*20, [0]*20, [0]*20
    ]

    matrix_D = [
        [1, 1, 3, 2, 1, 0, 0, 0, 0, 0,  3, 1, 3, 3, 2, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 2, 0, 0, 0, 0, 0,  3, 2, 2, 3, 1, 0, 0, 0, 0, 0],
        [1, 1, 2, 1, 1, 0, 0, 0, 0, 0,  3, 2, 3, 2, 2, 0, 0, 0, 0, 0],
        [1, 1, 1, 2, 1, 0, 0, 0, 0, 0,  2, 1, 2, 2, 1, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 0, 0, 0, 0, 0,  1, 2, 1, 1, 3, 0, 0, 0, 0, 0],
        [0]*20, [0]*20, [0]*20, [0]*20, [0]*20
    ]

    current_r = 7
    f_prefix = "F" if lang == 'ES' else "S"
    d_prefix = "D" if lang == 'ES' else "W"

    ws.merge_cells(start_row=current_r, start_column=1, end_row=current_r, end_column=23)
    c_f_sec = ws.cell(row=current_r, column=1, value=f"{texts['sec_f']} (F01 - F10)" if lang=='ES' else f"{texts['sec_f']} (S01 - S10)")
    c_f_sec.font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_F_TEXT)
    c_f_sec.fill = PatternFill(start_color=COLOR_F_BG, end_color=COLOR_F_BG, fill_type='solid')
    ws.row_dimensions[current_r].height = 20
    current_r += 1
    start_f_row = current_r

    for i in range(10):
        code = f"{f_prefix}{i+1:02d}"
        tab2_row = 7 + i

        ws.cell(row=current_r, column=1, value=code).font = styles['code_font']
        ws.cell(row=current_r, column=1).alignment = styles['align_center']
        ws.cell(row=current_r, column=1).border = styles['thin_border']
        ws.cell(row=current_r, column=1).fill = styles['calc_fill']
        ws.cell(row=current_r, column=1).protection = Protection(locked=True)

        formula_name = f'=IF({sheet_ref}!B{tab2_row}<>"", {sheet_ref}!B{tab2_row}, "{code} [Disponible]")'
        c_name = ws.cell(row=current_r, column=2, value=formula_name)
        c_name.font = styles['cell_font']
        c_name.border = styles['thin_border']
        c_name.fill = styles['calc_fill']
        c_name.protection = Protection(locked=True)

        for col_j in range(20):
            val = matrix_F[i][col_j]
            c_score = ws.cell(row=current_r, column=3 + col_j, value=val if val > 0 else 0)
            c_score.font = styles['cell_font']
            c_score.alignment = styles['align_center']
            c_score.border = styles['thin_border']
            c_score.fill = styles['input_fill']
            c_score.protection = Protection(locked=False)

        formula_row_sum = f'=SUM(C{current_r}:V{current_r})'
        c_tot = ws.cell(row=current_r, column=23, value=formula_row_sum)
        c_tot.font = styles['cell_bold']
        c_tot.alignment = styles['align_center']
        c_tot.border = styles['thin_border']
        c_tot.fill = styles['calc_fill']
        c_tot.protection = Protection(locked=True)

        ws.row_dimensions[current_r].height = 19
        current_r += 1
    end_f_row = current_r - 1

    ws.merge_cells(start_row=current_r, start_column=1, end_row=current_r, end_column=23)
    c_d_sec = ws.cell(row=current_r, column=1, value=f"{texts['sec_d']} (D01 - D10)" if lang=='ES' else f"{texts['sec_d']} (W01 - W10)")
    c_d_sec.font = Font(name='Segoe UI', size=10, bold=True, color=COLOR_D_TEXT)
    c_d_sec.fill = PatternFill(start_color=COLOR_D_BG, end_color=COLOR_D_BG, fill_type='solid')
    ws.row_dimensions[current_r].height = 20
    current_r += 1
    start_d_row = current_r

    for i in range(10):
        code = f"{d_prefix}{i+1:02d}"
        tab2_row = 21 + i

        ws.cell(row=current_r, column=1, value=code).font = styles['code_font']
        ws.cell(row=current_r, column=1).alignment = styles['align_center']
        ws.cell(row=current_r, column=1).border = styles['thin_border']
        ws.cell(row=current_r, column=1).fill = styles['calc_fill']
        ws.cell(row=current_r, column=1).protection = Protection(locked=True)

        formula_name = f'=IF({sheet_ref}!B{tab2_row}<>"", {sheet_ref}!B{tab2_row}, "{code} [Disponible]")'
        c_name = ws.cell(row=current_r, column=2, value=formula_name)
        c_name.font = styles['cell_font']
        c_name.border = styles['thin_border']
        c_name.fill = styles['calc_fill']
        c_name.protection = Protection(locked=True)

        for col_j in range(20):
            val = matrix_D[i][col_j]
            c_score = ws.cell(row=current_r, column=3 + col_j, value=val if val > 0 else 0)
            c_score.font = styles['cell_font']
            c_score.alignment = styles['align_center']
            c_score.border = styles['thin_border']
            c_score.fill = styles['input_fill']
            c_score.protection = Protection(locked=False)

        formula_row_sum = f'=SUM(C{current_r}:V{current_r})'
        c_tot = ws.cell(row=current_r, column=23, value=formula_row_sum)
        c_tot.font = styles['cell_bold']
        c_tot.alignment = styles['align_center']
        c_tot.border = styles['thin_border']
        c_tot.fill = styles['calc_fill']
        c_tot.protection = Protection(locked=True)

        ws.row_dimensions[current_r].height = 19
        current_r += 1
    end_d_row = current_r - 1

    tot_col_r = current_r
    ws.cell(row=tot_col_r, column=1, value="").border = styles['total_border']
    c_tot_col_lbl = ws.cell(row=tot_col_r, column=2, value=texts['row_tot'])
    c_tot_col_lbl.font = styles['cell_bold']
    c_tot_col_lbl.alignment = styles['align_right']
    c_tot_col_lbl.border = styles['total_border']
    c_tot_col_lbl.fill = styles['total_fill']

    for col_j in range(20):
        c_letter = get_column_letter(3 + col_j)
        f_sum = f'=SUM({c_letter}{start_f_row}:{c_letter}{end_f_row})+SUM({c_letter}{start_d_row}:{c_letter}{end_d_row})'
        c_sum = ws.cell(row=tot_col_r, column=3 + col_j, value=f_sum)
        c_sum.font = styles['cell_bold']
        c_sum.alignment = styles['align_center']
        c_sum.border = styles['total_border']
        c_sum.fill = styles['total_fill']
        c_sum.protection = Protection(locked=True)

    ws.cell(row=tot_col_r, column=23, value=f'=SUM(W{start_f_row}:W{end_f_row})+SUM(W{start_d_row}:W{end_d_row})').font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_BLUE_ACCENT)
    ws.cell(row=tot_col_r, column=23).border = styles['total_border']
    ws.cell(row=tot_col_r, column=23).fill = styles['total_fill']
    ws.cell(row=tot_col_r, column=23).alignment = styles['align_center']
    ws.row_dimensions[tot_col_r].height = 24

    card_r = tot_col_r + 2
    ws.merge_cells(f'B{card_r}:F{card_r}')
    ws[f'B{card_r}'] = texts['kpi_so']
    ws[f'B{card_r}'].font = styles['header_font']
    ws[f'B{card_r}'].fill = styles['header_fill']

    ws.merge_cells(f'B{card_r+1}:F{card_r+1}')
    c_so = ws[f'B{card_r+1}']
    c_so.value = f'=SUM(C{start_f_row}:L{end_f_row})'
    c_so.font = Font(name='Segoe UI', size=16, bold=True, color=COLOR_F_TEXT)
    c_so.fill = PatternFill(start_color=COLOR_F_BG, end_color=COLOR_F_BG, fill_type='solid')
    c_so.alignment = styles['align_center']
    c_so.border = styles['thin_border']

    ws.merge_cells(f'H{card_r}:L{card_r}')
    ws[f'H{card_r}'] = texts['kpi_st']
    ws[f'H{card_r}'].font = styles['header_font']
    ws[f'H{card_r}'].fill = styles['header_fill']

    ws.merge_cells(f'H{card_r+1}:L{card_r+1}')
    c_st = ws[f'H{card_r+1}']
    c_st.value = f'=SUM(M{start_f_row}:V{end_f_row})'
    c_st.font = Font(name='Segoe UI', size=16, bold=True, color=COLOR_O_TEXT)
    c_st.fill = PatternFill(start_color=COLOR_O_BG, end_color=COLOR_O_BG, fill_type='solid')
    c_st.alignment = styles['align_center']
    c_st.border = styles['thin_border']

    ws.merge_cells(f'N{card_r}:R{card_r}')
    ws[f'N{card_r}'] = texts['kpi_wo']
    ws[f'N{card_r}'].font = styles['header_font']
    ws[f'N{card_r}'].fill = styles['header_fill']

    ws.merge_cells(f'N{card_r+1}:R{card_r+1}')
    c_wo = ws[f'N{card_r+1}']
    c_wo.value = f'=SUM(C{start_d_row}:L{end_d_row})'
    c_wo.font = Font(name='Segoe UI', size=16, bold=True, color=COLOR_D_TEXT)
    c_wo.fill = PatternFill(start_color=COLOR_D_BG, end_color=COLOR_D_BG, fill_type='solid')
    c_wo.alignment = styles['align_center']
    c_wo.border = styles['thin_border']

    ws.merge_cells(f'T{card_r}:W{card_r}')
    ws[f'T{card_r}'] = texts['kpi_wt']
    ws[f'T{card_r}'].font = styles['header_font']
    ws[f'T{card_r}'].fill = styles['header_fill']

    ws.merge_cells(f'T{card_r+1}:W{card_r+1}')
    c_wt = ws[f'T{card_r+1}']
    c_wt.value = f'=SUM(M{start_d_row}:V{end_d_row})'
    c_wt.font = Font(name='Segoe UI', size=16, bold=True, color=COLOR_A_TEXT)
    c_wt.fill = PatternFill(start_color=COLOR_A_BG, end_color=COLOR_A_BG, fill_type='solid')
    c_wt.alignment = styles['align_center']
    c_wt.border = styles['thin_border']

    ws.protection.set_password(PASSWORD_PROTECT)
    ws.protection.sheet = True
    ws.protection.enable()
    ws.protection.selectLockedCells = True
    ws.protection.selectUnlockedCells = True


def build_came_sheet(ws, lang='ES', styles=None):
    ws.title = "Plan CAME" if lang == 'ES' else "Action Plan (SO, WO, ST, WT)"
    ws.views.sheetView[0].showGridLines = True

    texts = {
        'ES': {
            'title': "DATALARIA | PLAN ESTRATÉGICO DE ACCIÓN CAME (C-LEVEL ROADMAP)",
            'subtitle': "Traducción operativa de la matriz de decisión en iniciativas de inversión con responsable C-Level, plazos y dotación financiera P&L.",
            'sec_c': "1. CORREGIR DEBILIDADES (Iniciativas de Reorientación / WO)",
            'sec_a': "2. AFRONTAR AMENAZAS (Iniciativas Defensivas y Salvaguardas / ST)",
            'sec_m': "3. MANTENER FORTALEZAS (Iniciativas de Preservación de Moat / Moat Defense)",
            'sec_e': "4. EXPLOTAR OPORTUNIDADES (Iniciativas Ofensivas de Crecimiento / SO)",
            'col_id': "ID Acción",
            'col_factor': "Factor Clave",
            'col_name': "Iniciativa Estratégica Concreta",
            'col_owner': "Owner (C-Level)",
            'col_time': "Plazo",
            'col_capex': "CAPEX (€)",
            'col_opex': "OPEX (€)",
            'col_kpi': "KPI de Impacto en P&L",
            'col_status': "Estado",
            'lbl_total_sec': "TOTAL INVERSIÓN SECCIÓN",
            'lbl_grand_tot': "PRESUPUESTO TOTAL PLAN CAME (CAPEX + OPEX)",
        },
        'EN': {
            'title': "DATALARIA | C-LEVEL STRATEGIC ACTION ROADMAP (TOWS / CAME)",
            'subtitle': "Operational translation of the strategic decision matrix into capital allocation initiatives with C-Level ownership, timeline, and P&L targets.",
            'sec_c': "1. WEAKNESS MITIGATION / TURNAROUND (WO Strategies)",
            'sec_a': "2. THREAT DEFENSE & RISK HEDGING (ST Strategies)",
            'sec_m': "3. STRENGTH PRESERVATION & MOAT EXPANSION (Competitive Defense)",
            'sec_e': "4. OPPORTUNITY CAPTURE & AGGRESSIVE GROWTH (SO Strategies)",
            'col_id': "Action ID",
            'col_factor': "Key Factor",
            'col_name': "Strategic Initiative & Scope",
            'col_owner': "C-Level Owner",
            'col_time': "Target",
            'col_capex': "CAPEX (€)",
            'col_opex': "OPEX (€)",
            'col_kpi': "P&L Target Metric / KPI",
            'col_status': "Approval",
            'lbl_total_sec': "SECTION TOTAL INVESTMENT",
            'lbl_grand_tot': "TOTAL STRATEGIC BUDGET REQUIRED (CAPEX + OPEX)",
        }
    }[lang]

    ws.merge_cells('A2:I2')
    ws['A2'] = texts['title']
    ws['A2'].font = styles['title_font']
    ws['A2'].fill = styles['title_fill']
    ws['A2'].alignment = styles['align_left']
    ws.row_dimensions[2].height = 36

    ws.merge_cells('A3:I3')
    ws['A3'] = texts['subtitle']
    ws['A3'].font = styles['subtitle_font']
    ws['A3'].alignment = styles['align_left']
    ws.row_dimensions[3].height = 20

    actions_data_es = [
        ("CAME-C01", "D01 + O03", "Plan de Diversificación Comercial: Programa de canal en LatAm para reducir concentración a < 25%", "Chief Commercial Officer", "Q2-Q4", 45000, 60000, "Concentración top-2 < 25% ARR", "Aprobado"),
        ("CAME-C02", "D02 + O05", "Automatización de ciclo comercial con integradores globales para acortar lead time a 5 meses", "VP Sales Enterprise", "Q1-Q3", 25000, 35000, "Lead time ventas ≤ 5.2 meses", "Aprobado"),
        ("CAME-C03", "D05 + O02", "Refactorización del motor de facturación multi-divisa hacia microservicios cloud", "Chief Technology Officer", "Q2-Q3", 40000, 15000, "Deuda técnica sprint < 6%", "En Revisión"),
        ("CAME-A01", "F01 + A01", "Blindaje contractual plurianual con clientes clave con cláusula de fidelización", "Chief Executive Officer", "Q1-Q2", 10000, 20000, "Churn de clientes < 1.5%", "Aprobado"),
        ("CAME-A02", "F04 + A05", "Certificación anticipada en directiva NIS2 y auditoría de resiliencia operativa DORA", "Chief Information Security Officer", "Q2-Q3", 35000, 15000, "100% cumplimiento normativo", "Aprobado"),
        ("CAME-M01", "F02 + O02", "Extensión de patentes de algoritmos a jurisdicciones asiáticas y protección de IP", "Head of Legal & IP", "Q3-Q4", 30000, 10000, "2 nuevas patentes concedidas", "Propuesto"),
        ("CAME-M02", "F05 + A02", "Plan de retención de talento clave de I+D (Phantom Shares y plan de carrera técnica)", "Chief People Officer", "Q1-Q4", 0, 45000, "Rotación voluntaria < 3%", "Aprobado"),
        ("CAME-E01", "F01 + O01", "Aceleración del despliegue del módulo SaaS subvencionado por NextGen en 40 factorías", "Chief Operating Officer", "Q1-Q3", 65000, 40000, "+1.2M € ARR adicional", "Aprobado"),
        ("CAME-E02", "F03 + O05", "Acuerdo de co-selling con consultora global (Tier-1) para inclusión en licitaciones", "Chief Commercial Officer", "Q2-Q4", 20000, 30000, "+8 nuevos clientes Tier-1", "Aprobado"),
    ]

    actions_data_en = [
        ("TOWS-W01", "W01 + O03", "Commercial Diversification Program: Launch LatAm channel to compress top-client concentration below 25%", "Chief Commercial Officer", "Q2-Q4", 45000, 60000, "Top-2 revenue concentration < 25%", "Approved"),
        ("TOWS-W02", "W02 + O05", "Enterprise Sales Cycle Automation: Tier-1 SI co-selling framework to reduce deal velocity to 5 months", "VP Sales Enterprise", "Q1-Q3", 25000, 35000, "Average cycle time ≤ 5.2 months", "Approved"),
        ("TOWS-W03", "W05 + O02", "Legacy Billing Refactor: Modernize multi-currency engine to cloud-native microservices", "Chief Technology Officer", "Q2-Q3", 40000, 15000, "Maintenance debt < 6% capacity", "In Review"),
        ("TOWS-T01", "S01 + T01", "Multi-Year Contract Lock-in: Secure 3-year master agreements with top accounts to defeat Asian discount pricing", "Chief Executive Officer", "Q1-Q2", 10000, 20000, "Net ARR churn < 1.5%", "Approved"),
        ("TOWS-T02", "S04 + T05", "Accelerated NIS2 & DORA Compliance: Execute pre-audit readiness for enterprise supply chain mandates", "Chief Information Security Officer", "Q2-Q3", 35000, 15000, "100% regulatory audit pass", "Approved"),
        ("TOWS-S01", "S02 + O02", "IP Moat Expansion: File supplemental patent claims in US/Asia for core predictive neural architecture", "Head of Legal & IP", "Q3-Q4", 30000, 10000, "2 supplemental patents granted", "Proposed"),
        ("TOWS-S02", "S05 + T02", "Senior R&D Retention Moat: Deploy LTIP / Phantom Equity incentive package to retain top AI engineers", "Chief People Officer", "Q1-Q4", 0, 45000, "Voluntary engineering churn < 3%", "Approved"),
        ("TOWS-O01", "S01 + O01", "Industrial SaaS Scaling: Deploy subsidy-backed smart manufacturing module across 40 manufacturing sites", "Chief Operating Officer", "Q1-Q3", 65000, 40000, "+€1.2M incremental ARR", "Approved"),
        ("TOWS-O02", "S03 + O05", "Tier-1 SI Joint Go-to-Market: Embed proprietary engine into global systems integrator enterprise catalog", "Chief Commercial Officer", "Q2-Q4", 20000, 30000, "+8 new Fortune 500 logos", "Approved"),
    ]

    actions_data = actions_data_es if lang == 'ES' else actions_data_en

    sections = [
        ("C", texts['sec_c'], COLOR_D_BG, COLOR_D_BORDER, COLOR_D_TEXT, actions_data[0:3]),
        ("A", texts['sec_a'], COLOR_A_BG, COLOR_A_BORDER, COLOR_A_TEXT, actions_data[3:5]),
        ("M", texts['sec_m'], COLOR_F_BG, COLOR_F_BORDER, COLOR_F_TEXT, actions_data[5:7]),
        ("E", texts['sec_e'], COLOR_O_BG, COLOR_O_BORDER, COLOR_O_TEXT, actions_data[7:9]),
    ]

    current_r = 5
    headers = [
        (1, texts['col_id'], 12, styles['align_center']),
        (2, texts['col_factor'], 14, styles['align_center']),
        (3, texts['col_name'], 48, styles['align_left']),
        (4, texts['col_owner'], 28, styles['align_left']),
        (5, texts['col_time'], 10, styles['align_center']),
        (6, texts['col_capex'], 15, styles['align_right']),
        (7, texts['col_opex'], 15, styles['align_right']),
        (8, texts['col_kpi'], 30, styles['align_left']),
        (9, texts['col_status'], 14, styles['align_center']),
    ]

    capex_rows = []
    opex_rows = []

    for s_code, s_title, s_bg, s_border, s_text, rows in sections:
        ws.merge_cells(start_row=current_r, start_column=1, end_row=current_r, end_column=9)
        c_sec = ws.cell(row=current_r, column=1, value=s_title)
        c_sec.font = Font(name='Segoe UI', size=11, bold=True, color=s_text)
        c_sec.fill = PatternFill(start_color=s_bg, end_color=s_bg, fill_type='solid')
        ws.row_dimensions[current_r].height = 24
        current_r += 1

        for col_idx, h_text, width, align in headers:
            c = ws.cell(row=current_r, column=col_idx, value=h_text)
            c.font = styles['header_font']
            c.fill = styles['header_fill']
            c.alignment = align
            c.border = styles['header_border']
            ws.column_dimensions[get_column_letter(col_idx)].width = max(ws.column_dimensions[get_column_letter(col_idx)].width or 0, width)
        ws.row_dimensions[current_r].height = 22
        current_r += 1

        start_s_row = current_r
        for act in rows:
            act_id, factor, name, owner, timeline, capex, opex, kpi, status = act

            c_id = ws.cell(row=current_r, column=1, value=act_id)
            c_id.font = styles['code_font']
            c_id.alignment = styles['align_center']
            c_id.border = styles['thin_border']
            c_id.fill = styles['calc_fill']
            c_id.protection = Protection(locked=True)

            c_fac = ws.cell(row=current_r, column=2, value=factor)
            c_fac.font = styles['cell_bold']
            c_fac.alignment = styles['align_center']
            c_fac.border = styles['thin_border']
            c_fac.fill = styles['calc_fill']
            c_fac.protection = Protection(locked=True)

            c_nm = ws.cell(row=current_r, column=3, value=name)
            c_nm.font = styles['cell_font']
            c_nm.alignment = styles['align_left']
            c_nm.border = styles['thin_border']
            c_nm.fill = styles['input_fill']
            c_nm.protection = Protection(locked=False)

            c_own = ws.cell(row=current_r, column=4, value=owner)
            c_own.font = styles['cell_font']
            c_own.alignment = styles['align_left']
            c_own.border = styles['thin_border']
            c_own.fill = styles['input_fill']
            c_own.protection = Protection(locked=False)

            c_tm = ws.cell(row=current_r, column=5, value=timeline)
            c_tm.font = styles['cell_font']
            c_tm.alignment = styles['align_center']
            c_tm.border = styles['thin_border']
            c_tm.fill = styles['input_fill']
            c_tm.protection = Protection(locked=False)

            c_cap = ws.cell(row=current_r, column=6, value=capex)
            c_cap.font = styles['cell_font']
            c_cap.number_format = '#,##0 €'
            c_cap.alignment = styles['align_right']
            c_cap.border = styles['thin_border']
            c_cap.fill = styles['input_fill']
            c_cap.protection = Protection(locked=False)

            c_opx = ws.cell(row=current_r, column=7, value=opex)
            c_opx.font = styles['cell_font']
            c_opx.number_format = '#,##0 €'
            c_opx.alignment = styles['align_right']
            c_opx.border = styles['thin_border']
            c_opx.fill = styles['input_fill']
            c_opx.protection = Protection(locked=False)

            c_kpi = ws.cell(row=current_r, column=8, value=kpi)
            c_kpi.font = styles['cell_font']
            c_kpi.alignment = styles['align_left']
            c_kpi.border = styles['thin_border']
            c_kpi.fill = styles['input_fill']
            c_kpi.protection = Protection(locked=False)

            c_st = ws.cell(row=current_r, column=9, value=status)
            c_st.font = styles['cell_bold']
            c_st.alignment = styles['align_center']
            c_st.border = styles['thin_border']
            c_st.fill = styles['input_fill']
            c_st.protection = Protection(locked=False)

            ws.row_dimensions[current_r].height = 20
            current_r += 1
        end_s_row = current_r - 1

        sub_row = current_r
        ws.merge_cells(f'A{sub_row}:E{sub_row}')
        c_sub_lbl = ws.cell(row=sub_row, column=1, value=f"{texts['lbl_total_sec']} ({s_code})")
        c_sub_lbl.font = styles['cell_bold']
        c_sub_lbl.alignment = styles['align_right']
        c_sub_lbl.border = styles['total_border']
        c_sub_lbl.fill = styles['total_fill']

        c_sub_cap = ws.cell(row=sub_row, column=6, value=f'=SUM(F{start_s_row}:F{end_s_row})')
        c_sub_cap.font = styles['cell_bold']
        c_sub_cap.number_format = '#,##0 €'
        c_sub_cap.alignment = styles['align_right']
        c_sub_cap.border = styles['total_border']
        c_sub_cap.fill = styles['total_fill']
        c_sub_cap.protection = Protection(locked=True)
        capex_rows.append(f"F{sub_row}")

        c_sub_opx = ws.cell(row=sub_row, column=7, value=f'=SUM(G{start_s_row}:G{end_s_row})')
        c_sub_opx.font = styles['cell_bold']
        c_sub_opx.number_format = '#,##0 €'
        c_sub_opx.alignment = styles['align_right']
        c_sub_opx.border = styles['total_border']
        c_sub_opx.fill = styles['total_fill']
        c_sub_opx.protection = Protection(locked=True)
        opex_rows.append(f"G{sub_row}")

        ws.cell(row=sub_row, column=8, value="").border = styles['total_border']
        ws.cell(row=sub_row, column=9, value="").border = styles['total_border']
        ws.row_dimensions[sub_row].height = 22
        current_r += 2

    grand_row = current_r
    ws.merge_cells(f'A{grand_row}:E{grand_row}')
    c_g_lbl = ws.cell(row=grand_row, column=1, value=texts['lbl_grand_tot'])
    c_g_lbl.font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_WHITE)
    c_g_lbl.fill = styles['title_fill']
    c_g_lbl.alignment = styles['align_right']

    c_g_cap = ws.cell(row=grand_row, column=6, value=f'={ "+".join(capex_rows) }')
    c_g_cap.font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_WHITE)
    c_g_cap.fill = styles['title_fill']
    c_g_cap.number_format = '#,##0 €'
    c_g_cap.alignment = styles['align_right']
    c_g_cap.border = styles['total_border']

    c_g_opx = ws.cell(row=grand_row, column=7, value=f'={ "+".join(opex_rows) }')
    c_g_opx.font = Font(name='Segoe UI', size=11, bold=True, color=COLOR_WHITE)
    c_g_opx.fill = styles['title_fill']
    c_g_opx.number_format = '#,##0 €'
    c_g_opx.alignment = styles['align_right']
    c_g_opx.border = styles['total_border']

    ws.merge_cells(f'H{grand_row}:I{grand_row}')
    c_g_sum = ws.cell(row=grand_row, column=8, value=f'=F{grand_row}+G{grand_row}')
    c_g_sum.font = Font(name='Segoe UI', size=12, bold=True, color="FEF08A")
    c_g_sum.fill = styles['title_fill']
    c_g_sum.number_format = '#,##0 €'
    c_g_sum.alignment = styles['align_center']
    c_g_sum.border = styles['total_border']
    ws.row_dimensions[grand_row].height = 28

    ws.protection.set_password(PASSWORD_PROTECT)
    ws.protection.sheet = True
    ws.protection.enable()
    ws.protection.selectLockedCells = True
    ws.protection.selectUnlockedCells = True


def main():
    styles = get_styles()

    # 1. Versión en Español
    out_dir_es = "static/downloads/dafo-came-es"
    os.makedirs(out_dir_es, exist_ok=True)
    file_es = os.path.join(out_dir_es, "DAFO_Cuantitativo_CAME_Datalaria_ES.xlsx")

    wb_es = openpyxl.Workbook()
    ws_assess_es = wb_es.active
    summary_rows_es = build_assessment_sheet(ws_assess_es, lang='ES', styles=styles)

    ws_dash_es = wb_es.create_sheet(title="Dashboard", index=0)
    build_dashboard_sheet(ws_dash_es, summary_rows_es, lang='ES', styles=styles)

    ws_cross_es = wb_es.create_sheet(title="Cruce", index=2)
    build_cross_sheet(ws_cross_es, lang='ES', styles=styles)

    ws_came_es = wb_es.create_sheet(title="Plan CAME", index=3)
    build_came_sheet(ws_came_es, lang='ES', styles=styles)

    wb_es.save(file_es)
    print(f"[OK ES] Guardado: {file_es} ({os.path.getsize(file_es)} bytes)")

    # 2. Versión en Inglés
    out_dir_en = "static/downloads/swot-tows-en"
    os.makedirs(out_dir_en, exist_ok=True)
    file_en = os.path.join(out_dir_en, "Quantitative_SWOT_TOWS_Datalaria_EN.xlsx")

    wb_en = openpyxl.Workbook()
    ws_assess_en = wb_en.active
    summary_rows_en = build_assessment_sheet(ws_assess_en, lang='EN', styles=styles)

    ws_dash_en = wb_en.create_sheet(title="Dashboard", index=0)
    build_dashboard_sheet(ws_dash_en, summary_rows_en, lang='EN', styles=styles)

    ws_cross_en = wb_en.create_sheet(title="TOWS Matrix", index=2)
    build_cross_sheet(ws_cross_en, lang='EN', styles=styles)

    ws_tows_en = wb_en.create_sheet(title="Action Plan", index=3)
    build_came_sheet(ws_tows_en, lang='EN', styles=styles)

    wb_en.save(file_en)
    print(f"[OK EN] Guardado: {file_en} ({os.path.getsize(file_en)} bytes)")


if __name__ == '__main__':
    main()
