#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5-6 páginas) para el Executive Decision Pack Business Case:
1. packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[ES]_Business_Case_VAN_TIR/Guia_Metodologica_Business_Case_ES.pdf
2. packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[EN]_Financial_Business_Case/Methodology_Guide_Business_Case_EN.pdf

Estructura Editorial de Grado Consejo de Administración (McKinsey / BCG Corporate Finance Practice):
- Portada ejecutiva, metadatos y Sección 1: Por Qué Fracasan los Business Cases.
- Sección 2: Fundamentación Matemática Formal (FCF, VAN, TIR, MIRR, WACC CAPM, Gordon, Payback interpolado, PI, trampa de Excel).
- Sección 3: Análisis de Riesgo & Sensibilidad (Metodología Tornado, Escenarios y E[VAN], Break-Even, Dominancia del VAN, Stage Gates).
- Sección 4: Caso Práctico Resuelto con Cifras Exactas de model_core.py.
- Sección 5: Board Defense FAQ (6 Preguntas Difíciles del CFO y Comité de Inversiones con Respuestas Modelo).
- Sección 6: Referencias Bibliográficas Canónicas de Autoridad.
- Paginación dinámica con NumberedCanvas ("Página X de Y" / "Page X of Y") y soporte oficial datalaria@gmail.com.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import model_core

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Paleta Corporativa Datalaria
C_NAVY_DARK = colors.HexColor("#0F172A")    # Slate 900
C_NAVY_MED = colors.HexColor("#1E293B")     # Slate 800
C_SLATE_MUTED = colors.HexColor("#64748B")  # Slate 500
C_BLUE_ACCENT = colors.HexColor("#2563EB")  # Blue 600
C_BLUE_LIGHT = colors.HexColor("#EFF6FF")   # Blue 50

C_GREEN_ACCENT = colors.HexColor("#10B981") # Emerald 500
C_GREEN_LIGHT = colors.HexColor("#D1FAE5")  # Emerald 100
C_GREEN_TEXT = colors.HexColor("#065F46")   # Emerald 800

C_AMBER_ACCENT = colors.HexColor("#F59E0B") # Amber 500
C_AMBER_LIGHT = colors.HexColor("#FEF3C7")  # Amber 100
C_AMBER_TEXT = colors.HexColor("#92400E")   # Amber 800

C_RED_ACCENT = colors.HexColor("#EF4444")   # Red 500
C_RED_LIGHT = colors.HexColor("#FEE2E2")    # Red 100
C_RED_TEXT = colors.HexColor("#991B1B")     # Red 800

C_BG_CARD = colors.HexColor("#F8FAFC")      # Slate 50
C_BORDER_LIGHT = colors.HexColor("#CBD5E1") # Slate 300
C_WHITE = colors.HexColor("#FFFFFF")


class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para calcular y renderizar el número total de páginas dinámicamente."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        cur_page = self._pageNumber
        lang = getattr(self, '_lang', 'ES')

        # Cabecera en páginas 2 en adelante
        if cur_page > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(C_SLATE_MUTED)
            self.drawString(42, 805, "DATALARIA | EXECUTIVE DECISION PACK")
            header_right = (
                "BUSINESS CASE FINANCIERO: VAN, TIR, PAYBACK & ANÁLISIS TORNADO"
                if lang == 'ES' else
                "FINANCIAL BUSINESS CASE: NPV, IRR, PAYBACK & TORNADO SENSITIVITY"
            )
            self.drawRightString(553, 805, header_right)
            self.setStrokeColor(C_BORDER_LIGHT)
            self.setLineWidth(0.75)
            self.line(42, 798, 553, 798)

        # Pie de página en todas las páginas
        self.setStrokeColor(C_BORDER_LIGHT)
        self.setLineWidth(0.75)
        self.line(42, 45, 553, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(C_SLATE_MUTED)
        footer_left = (
            "Datalaria.com • Soporte: datalaria@gmail.com • Confidencial C-Level"
            if lang == 'ES' else
            "Datalaria.com • Support: datalaria@gmail.com • Confidential C-Level"
        )
        self.drawString(42, 32, footer_left)
        page_str = f"Página {cur_page} de {total_pages}" if lang == 'ES' else f"Page {cur_page} of {total_pages}"
        self.drawRightString(553, 32, page_str)

        self.restoreState()


def get_custom_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles['DocTitle'] = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=C_NAVY_DARK,
        spaceAfter=4,
    )
    styles['DocSubtitle'] = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=C_BLUE_ACCENT,
        spaceAfter=12,
    )
    styles['MetaBadge'] = ParagraphStyle(
        'MetaBadge',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=C_BLUE_ACCENT,
        spaceAfter=4,
    )
    styles['SectionTitle'] = ParagraphStyle(
        'SectionTitle',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=C_NAVY_DARK,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )
    styles['SubsectionTitle'] = ParagraphStyle(
        'SubsectionTitle',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=C_BLUE_ACCENT,
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True,
    )
    styles['Body'] = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=C_NAVY_MED,
        spaceAfter=6,
    )
    styles['BodyBold'] = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=C_NAVY_DARK,
        spaceAfter=6,
    )
    styles['Callout'] = ParagraphStyle(
        'Callout',
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=C_NAVY_DARK,
    )
    styles['Formula'] = ParagraphStyle(
        'Formula',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.2,
        textColor=C_NAVY_DARK,
    )
    styles['TableHead'] = ParagraphStyle(
        'TableHead',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=C_WHITE,
        alignment=1, # Center
    )
    styles['TableCell'] = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=C_NAVY_MED,
    )
    styles['TableCellBold'] = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=C_NAVY_DARK,
    )
    styles['TableCellRight'] = ParagraphStyle(
        'TableCellRight',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=C_NAVY_MED,
        alignment=2, # Right
    )
    styles['TableCellRightBold'] = ParagraphStyle(
        'TableCellRightBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=C_NAVY_DARK,
        alignment=2, # Right
    )
    styles['FAQQuestion'] = ParagraphStyle(
        'FAQQuestion',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=C_NAVY_DARK,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True,
    )
    styles['FAQAnswer'] = ParagraphStyle(
        'FAQAnswer',
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=C_NAVY_MED,
        spaceAfter=5,
    )

    return styles


def make_box(content_flowable, bg_color=C_BLUE_LIGHT, border_color=C_BLUE_ACCENT, pad=6):
    """Envuelve uno o varios flowables en una caja estilizada de una celda."""
    t = Table([[content_flowable]], colWidths=[511])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), pad),
        ('BOTTOMPADDING', (0, 0), (-1, -1), pad),
        ('LEFTPADDING', (0, 0), (-1, -1), pad + 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), pad + 2),
    ]))
    return t


def build_pdf_story(lang='ES'):
    """Construye la secuencia completa de flowables para el documento PDF."""
    styles = get_custom_styles()
    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA EJECUTIVA Y SECCIÓN 1: POR QUÉ FRACASAN LOS BUSINESS CASES
    # =========================================================================
    badge_txt = (
        "SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN | ESTÁNDAR CORPORATE FINANCE TIER-1"
        if lang == 'ES' else
        "SUITE 02 · DECISION ANALYSIS & PRIORITIZATION | TIER-1 CORPORATE FINANCE STANDARD"
    )
    title_txt = (
        "Business Case Financiero: VAN, TIR, Payback & Análisis de Sensibilidad Tornado"
        if lang == 'ES' else
        "Financial Business Case: NPV, IRR, Payback & Tornado Sensitivity Analysis"
    )
    subtitle_txt = (
        "Guía Metodológica de Valoración DCF, Coste de Capital WACC y Gobernanza de Inversión ante el Consejo"
        if lang == 'ES' else
        "Methodological Guide to DCF Valuation, WACC Hurdle Rates and Boardroom Investment Governance"
    )

    story.append(Paragraph(badge_txt, styles['MetaBadge']))
    story.append(Paragraph(title_txt, styles['DocTitle']))
    story.append(Paragraph(subtitle_txt, styles['DocSubtitle']))

    # Cuadro de Metadatos del Pack
    meta_table_data = [
        [
            Paragraph("<b>Marco Analítico:</b> Descuento Flujos Libres (DCF) + WACC (CAPM)" if lang == 'ES' else "<b>Analytical Framework:</b> Discounted Free Cash Flow (DCF) + CAPM WACC", styles['TableCell']),
            Paragraph("<b>Horizonte:</b> 5 Años Operativos + Valor Residual Opcional" if lang == 'ES' else "<b>Horizon:</b> 5 Operating Years + Optional Terminal Value", styles['TableCell']),
        ],
        [
            Paragraph("<b>Métricas Clave:</b> VAN, TIR, MIRR, Payback Descontado, PI, Peak Funding" if lang == 'ES' else "<b>Core Metrics:</b> NPV, IRR, MIRR, Discounted Payback, PI, Peak Funding", styles['TableCell']),
            Paragraph("<b>Gobernanza:</b> Stage Gates, Kill Criteria y 4 Firmas C-Level" if lang == 'ES' else "<b>Governance:</b> Phased Stage Gates, Kill Criteria & 4 C-Level Sign-Offs", styles['TableCell']),
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[255, 256])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.75, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # SECCIÓN 1
    s1_title = "1. Por Qué Fracasan los Business Cases en la Práctica Corporativa" if lang == 'ES' else "1. Why Business Cases Fail in Corporate Practice"
    story.append(Paragraph(s1_title, styles['SectionTitle']))

    p_s1_1 = (
        "En la inmensa mayoría de las organizaciones, las solicitudes de inversión de capital (CAPEX) presentadas "
        "ante el Director General (CEO), el Director Financiero (CFO) y el Comité de Inversiones sufren de lo que McKinsey "
        "denomina <i>la trampa de la última milla financiera</i>. Proyectos que prometen transformaciones operativas "
        "terminan destruyendo valor económico por carecer de rigor metodológico institucional."
        if lang == 'ES' else
        "Across corporate organizations, capital expenditure (CAPEX) proposals submitted to the CEO, CFO and Investment "
        "Committee routinely suffer from what McKinsey terms <i>the financial last-mile trap</i>. Projects promising dramatic "
        "operational gains frequently destroy shareholder value due to deficient financial underwriting standards."
    )
    story.append(Paragraph(p_s1_1, styles['Body']))

    p_s1_points = (
        "<b>1. Confusión entre Beneficio Contable y Flujo de Caja:</b> Se confunde el margen EBIT o EBITDA con liquidez real, "
        "omitiendo el calendario de pagos de CAPEX y la amortización contable (que es un gasto no monetario).<br/>"
        "<b>2. Omisión del Capital Circulante (NWC) y del Coste de Oportunidad:</b> A mayor crecimiento de ventas, mayor necesidad "
        "de stock y cuentas a cobrar. Ignorar el ΔNWC infravalora la necesidad real de caja.<br/>"
        "<b>3. Sesgo Optimista y Falacia de la Planificación (Kahneman & Lovallo; Flyvbjerg):</b> Los promotores proyectan ingresos "
        "crecientes sin fricción y minimizan retrasos técnicos. Bent Flyvbjerg demostró que el 80% de los proyectos industriales "
        "sufren sobrecostes superiores al 25% si no se calibran con previsión por clase de referencia (<i>reference class forecasting</i>).<br/>"
        "<b>4. La TIR como Métrica Seductora pero Engañosa:</b> La Tasa Interna de Retorno (TIR) es intuitiva pero asume que los "
        "flujos intermedios se reinvierten a la propia TIR (hipótesis irrealista en proyectos rentables) y es insensible a la escala del capital."
        if lang == 'ES' else
        "<b>1. Accounting Profit vs. Free Cash Flow Confusion:</b> Mistaking EBIT or EBITDA for actual cash liquidity, while ignoring "
        "the timing of capital disbursements and non-cash depreciation add-backs.<br/>"
        "<b>2. Omission of Net Working Capital (NWC) and Opportunity Cost:</b> Revenue expansion demands inventory and accounts receivable. "
        "Ignoring ΔNWC severely underestimates cash drain and working capital drag.<br/>"
        "<b>3. Optimism Bias & Planning Fallacy (Kahneman & Lovallo; Flyvbjerg):</b> Project sponsors forecast frictionless growth while "
        "ignoring technical delays. Prof. Bent Flyvbjerg documented that 80% of industrial CAPEX programs suffer >25% cost overruns "
        "unless mitigated via reference class forecasting.<br/>"
        "<b>4. IRR as an Attractive but Misleading Metric:</b> Internal Rate of Return (IRR) assumes interim cash flows are reinvested "
        "at the project's own IRR (unrealistic for high-return initiatives) and fails to account for scale differences."
    )
    story.append(Paragraph(p_s1_points, styles['Body']))

    box_minto = Paragraph(
        "<b>REGLA DE GOBERNANZA MCKINSEY / BCG:</b> Un Business Case C-Level no es una hoja de cálculo estática; es un contrato vinculante "
        "de asignación de capital basado en Flujo de Caja Libre Descontado (DCF), sensibilidad Tornado y tramos condicionados."
        if lang == 'ES' else
        "<b>MCKINSEY / BCG GOVERNANCE RULE:</b> A C-Level Business Case is not a static spreadsheet; it is a binding capital allocation "
        "contract founded upon Discounted Free Cash Flow (DCF), Tornado risk sensitivity, and conditional milestone tranches.",
        styles['Callout']
    )
    story.append(make_box(box_minto, C_BLUE_LIGHT, C_BLUE_ACCENT, 5))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: SECCIÓN 2: FUNDAMENTACIÓN MATEMÁTICA FORMAL DEL MODELO DCF
    # =========================================================================
    s2_title = "2. Fundamentación Matemática Formal del Modelo DCF Institucional" if lang == 'ES' else "2. Formal Mathematical Foundations of Institutional DCF Modeling"
    story.append(Paragraph(s2_title, styles['SectionTitle']))

    # 2.1 Flujo de Caja Libre
    story.append(Paragraph("2.1. Definición Canónica del Flujo de Caja Libre (FCF)" if lang == 'ES' else "2.1. Canonical Free Cash Flow to Firm (FCF) Definition", styles['SubsectionTitle']))
    fcf_formula = Paragraph(
        "<b>FCF<sub>t</sub> = EBIT<sub>t</sub> · (1 - t) + D&amp;A<sub>t</sub> - CAPEX<sub>t</sub> - ΔNWC<sub>t</sub></b><br/>"
        "<font size='7.5' color='#475569'>"
        "<b>NOPAT</b> = EBIT · (1 - t) (beneficio operativo tras impuestos) &nbsp;|&nbsp; "
        "<b>D&amp;A</b> = amortización recuperada (gasto no monetario)<br/>"
        "<b>CAPEX</b> = inversión en inmovilizado &nbsp;|&nbsp; "
        "<b>ΔNWC</b> = NWC<sub>t</sub> - NWC<sub>t-1</sub> (variación de capital circulante operativo = Ventas · %NWC)"
        "</font>"
        if lang == 'ES' else
        "<b>FCF<sub>t</sub> = EBIT<sub>t</sub> · (1 - t) + D&amp;A<sub>t</sub> - CAPEX<sub>t</sub> - ΔNWC<sub>t</sub></b><br/>"
        "<font size='7.5' color='#475569'>"
        "<b>NOPAT</b> = EBIT · (1 - t) (net operating profit after tax) &nbsp;|&nbsp; "
        "<b>D&amp;A</b> = depreciation &amp; amortization add-back<br/>"
        "<b>CAPEX</b> = capital expenditures in fixed assets &nbsp;|&nbsp; "
        "<b>ΔNWC</b> = NWC<sub>t</sub> - NWC<sub>t-1</sub> (operating working capital change = Sales · %NWC)"
        "</font>",
        styles['Formula']
    )
    story.append(make_box(fcf_formula, C_BG_CARD, C_BORDER_LIGHT, 5))
    story.append(Spacer(1, 4))

    # 2.2 VAN, TIR y WACC
    story.append(Paragraph("2.2. Valor Actual Neto (VAN), Tasa Interna de Retorno (TIR) y WACC (CAPM)" if lang == 'ES' else "2.2. Net Present Value (NPV), Internal Rate of Return (IRR) & WACC (CAPM)", styles['SubsectionTitle']))
    van_wacc_formula = Paragraph(
        "<b>Valor Actual Neto:</b> &nbsp; VAN = ∑ [ FCF<sub>t</sub> / (1 + WACC)<sup>t</sup> ] + [ VR<sub>Gordon</sub> / (1 + WACC)<sup>n</sup> ]<br/>"
        "<b>Tasa Interna de Retorno:</b> &nbsp; Tasa r tal que &nbsp; ∑ [ FCF<sub>t</sub> / (1 + TIR)<sup>t</sup> ] = 0<br/>"
        "<b>Coste de Capital (WACC):</b> &nbsp; WACC = (E / V) · K<sub>e</sub> + (D / V) · K<sub>d</sub> · (1 - t)<br/>"
        "<b>Coste de Fondos Propios (CAPM):</b> &nbsp; K<sub>e</sub> = R<sub>f</sub> + β · ERP + Primas (tamaño e iliquidez)"
        if lang == 'ES' else
        "<b>Net Present Value:</b> &nbsp; NPV = ∑ [ FCF<sub>t</sub> / (1 + WACC)<sup>t</sup> ] + [ TV<sub>Gordon</sub> / (1 + WACC)<sup>n</sup> ]<br/>"
        "<b>Internal Rate of Return:</b> &nbsp; Discount rate r such that &nbsp; ∑ [ FCF<sub>t</sub> / (1 + IRR)<sup>t</sup> ] = 0<br/>"
        "<b>Cost of Capital (WACC):</b> &nbsp; WACC = (E / V) · K<sub>e</sub> + (D / V) · K<sub>d</sub> · (1 - t)<br/>"
        "<b>Cost of Equity (CAPM):</b> &nbsp; K<sub>e</sub> = R<sub>f</sub> + β · ERP + Premiums (size &amp; illiquidity)",
        styles['Formula']
    )
    story.append(make_box(van_wacc_formula, C_BG_CARD, C_BORDER_LIGHT, 5))
    story.append(Spacer(1, 4))

    # 2.3 MIRR, Payback Interpolado y Gordon
    story.append(Paragraph("2.3. TIR Modificada (MIRR), Payback con Interpolación e Índice de Rentabilidad (PI)" if lang == 'ES' else "2.3. Modified IRR (MIRR), Interpolated Payback & Profitability Index (PI)", styles['SubsectionTitle']))
    mirr_pb_formula = Paragraph(
        "<b>TIR Modificada (MIRR):</b> &nbsp; MIRR = [ ( ∑ FCF<sub>t</sub><sup>+</sup> · (1 + r)<sup>n-t</sup> ) / | FCF<sub>0</sub> + ∑ FCF<sub>t</sub><sup>-</sup> · (1 + WACC)<sup>-t</sup> | ]<sup>1/n</sup> - 1<br/>"
        "<b>Índice de Rentabilidad (PI):</b> &nbsp; PI = VP(Flujos Futuros) / | Inversión Descontada |<br/>"
        "<b>Payback Descontado:</b> &nbsp; Payback<sub>desc</sub> = (t - 1) + [ | VP Acumulado<sub>t-1</sub> | / VP FCF<sub>t</sub> ]<br/>"
        "<b>Valor Residual (Gordon):</b> &nbsp; VR<sub>Gordon</sub> = [ FCF<sub>n</sub> · (1 + g) ] / ( WACC - g ) &nbsp;&nbsp; (con WACC > g)"
        if lang == 'ES' else
        "<b>Modified IRR (MIRR):</b> &nbsp; MIRR = [ ( ∑ FCF<sub>t</sub><sup>+</sup> · (1 + r)<sup>n-t</sup> ) / | FCF<sub>0</sub> + ∑ FCF<sub>t</sub><sup>-</sup> · (1 + WACC)<sup>-t</sup> | ]<sup>1/n</sup> - 1<br/>"
        "<b>Profitability Index (PI):</b> &nbsp; PI = PV(Future Inflows) / | Discounted Capital Outlay |<br/>"
        "<b>Discounted Payback:</b> &nbsp; Payback<sub>desc</sub> = (t - 1) + [ | Cum PV<sub>t-1</sub> | / PV FCF<sub>t</sub> ]<br/>"
        "<b>Gordon Terminal Value:</b> &nbsp; TV<sub>Gordon</sub> = [ FCF<sub>n</sub> · (1 + g) ] / ( WACC - g ) &nbsp;&nbsp; (subject to WACC > g)",
        styles['Formula']
    )
    story.append(make_box(mirr_pb_formula, C_BG_CARD, C_BORDER_LIGHT, 5))
    story.append(Spacer(1, 4))

    # Caja de Advertencia: La Trampa de NPV en Excel
    npv_trap_txt = Paragraph(
        "<b>ALERTA TÉCNICA CRÍTICA: LA TRAMPA DE LA FUNCIÓN NPV / VNA EN EXCEL:</b><br/>"
        "La función nativa <b>NPV(tasa, rango)</b> (o VNA) de Excel descuenta el primer flujo del rango como si ocurriese al final del periodo 1 "
        "(descuento por (1 + WACC)<sup>1</sup>). Si se incluye el desembolso del Año 0 dentro del rango, Excel infravalora la inversión inicial "
        "y sobrestima artificialmente el VAN. La formulación matemática estricta e institucional es obligatoriamente:<br/>"
        "<b>= FCF<sub>0</sub> + NPV(WACC, FCF<sub>1</sub>:FCF<sub>n</sub>)</b> (incorporando el Año 0 de forma discreta fuera de la función)."
        if lang == 'ES' else
        "<b>CRITICAL TECHNICAL WARNING: THE EXCEL NPV FUNCTION TRAP:</b><br/>"
        "The native Excel function <b>NPV(rate, range)</b> discounts the first flow in the range back by one full period as if it occurred at the end of Year 1 "
        "(discounted by (1 + WACC)<sup>1</sup>). If Year 0 outlay is included inside the range, Excel understates initial capital "
        "and artificially inflates NPV. The mandatory institutional syntax is:<br/>"
        "<b>= FCF<sub>0</sub> + NPV(WACC, FCF<sub>1</sub>:FCF<sub>n</sub>)</b> (adding Year 0 discretely outside the NPV function).",
        styles['Callout']
    )
    story.append(make_box(npv_trap_txt, C_RED_LIGHT, C_RED_ACCENT, 5))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: SECCIÓN 3: RIESGO, SENSIBILIDAD TORNADO Y GOBERNANZA
    # =========================================================================
    s3_title = "3. Análisis de Riesgo: Gráfico Tornado, Escenarios y Opciones Reales" if lang == 'ES' else "3. Risk Engineering: Tornado Charts, Scenarios & Real Options"
    story.append(Paragraph(s3_title, styles['SectionTitle']))

    story.append(Paragraph("3.1. Metodología del Gráfico Tornado y Jerarquía de Sensibilidad" if lang == 'ES' else "3.1. Tornado Chart Methodology & Risk Hierarchy", styles['SubsectionTitle']))
    p_s3_1 = (
        "El análisis de sensibilidad estático tradicional (variar una celda a mano) oculta la interacción de riesgos. "
        "El Gráfico Tornado aplica una perturbación univariable normalizada (±15% en volúmenes y precios, ±5 pp en márgenes, ±2 pp en WACC) "
        "sobre cada variable del caso Base mientras mantiene todas las demás constantes.<br/>"
        "<b>Amplitud (Swing):</b> Swing<sub>i</sub> = | VAN<sub>i</sub><sup>Alto</sup> - VAN<sub>i</sub><sup>Bajo</sup> |. Los drivers se ordenan "
        "de mayor a menor amplitud, situando en la cúspide las variables que concentran el mayor riesgo corporativo. "
        "En proyectos industriales, Precio y Volumen concentran típicamente entre el 65% y el 75% de la volatilidad total del VAN."
        if lang == 'ES' else
        "Traditional static one-off sensitivity checks fail to reveal true risk concentration. "
        "The Tornado Chart applies standardized univariate perturbations (±15% volumes/prices, ±5 pp cost margins, ±2 pp WACC) "
        "to each Base Case parameter while holding all other variables constant.<br/>"
        "<b>Swing Amplitude:</b> Swing<sub>i</sub> = | NPV<sub>i</sub><sup>High</sup> - NPV<sub>i</sub><sup>Low</sup> |. Drivers are ranked "
        "from largest to smallest swing, placing the most critical risk drivers at the top. "
        "In industrial projects, Price and Volume typically account for 65% to 75% of total NPV volatility."
    )
    story.append(Paragraph(p_s3_1, styles['Body']))

    story.append(Paragraph("3.2. Puntos de Equilibrio (Break-Even) y Margen de Seguridad" if lang == 'ES' else "3.2. Break-Even Points & Operational Margin of Safety", styles['SubsectionTitle']))
    p_s3_2 = (
        "El punto de equilibrio lineal determina el valor crítico exacto de un driver que hace <b>VAN = 0</b>. "
        "Define el margen de seguridad operativo antes de que el proyecto comience a destruir riqueza para el accionista:<br/>"
        "• <i>Precio de Equilibrio:</i> Determina la capacidad del proyecto de resistir guerras de precios en el mercado.<br/>"
        "• <i>Volumen de Equilibrio:</i> Cuantifica el umbral mínimo de ocupación de planta y absorción de costes fijos.<br/>"
        "• <i>Sobrecoste Máximo de CAPEX:</i> Fija el tope financiero para desvíos de ingeniería antes de cancelar el proyecto."
        if lang == 'ES' else
        "Linear break-even analysis calculates the exact critical parameter value where <b>NPV = 0</b>. "
        "It defines the operational margin of safety before capital is destroyed:<br/>"
        "• <i>Break-Even Price:</i> Measures resilience against industrial pricing wars and commoditization.<br/>"
        "• <i>Break-Even Volume:</i> Quantifies minimum plant capacity utilization and fixed cost absorption.<br/>"
        "• <i>Maximum Allowable CAPEX:</i> Establishes the absolute engineering overrun ceiling before cancellation."
    )
    story.append(Paragraph(p_s3_2, styles['Body']))

    story.append(Paragraph("3.3. Stage Gates y Kill Criteria como Opciones Reales Simplificadas", styles['SubsectionTitle']))
    p_s3_3 = (
        "Bajo la teoría de opciones reales (Dixit & Pindyck), un proyecto no debe tratarse como un compromiso irreversible "
        "del 100% del capital. Dividir el CAPEX en tramos condicionados (<i>stage gates</i>) otorga a la dirección "
        "la <b>opción de abandonar (abandonment option)</b> o la <b>opción de diferir (deferral option)</b> a un coste mínimo. "
        "Los <i>Kill Criteria</i> actúan como órdenes stop-loss vinculantes que neutralizan la falacia del coste hundido (<i>sunk cost fallacy</i>)."
        if lang == 'ES' else
        "Under Real Options Theory (Dixit & Pindyck), capital allocation should not be an irreversible all-or-nothing commitment. "
        "Staging CAPEX across milestone-gated tranches provides management with a valuable <b>abandonment option</b> "
        "and <b>deferral option</b>. Binding <i>Kill Criteria</i> act as stop-loss rules, eliminating the psychological trap of the sunk cost fallacy."
    )
    story.append(Paragraph(p_s3_3, styles['Body']))

    box_conflict = Paragraph(
        "<b>¿POR QUÉ PREVALECE EL VAN SOBRE LA TIR EN CASO DE CONFLICTO?</b><br/>"
        "1. <b>Supuesto de Reinversión:</b> El VAN asume reinversión al WACC (realista); la TIR asume reinversión a la propia TIR.<br/>"
        "2. <b>Problema de Escala:</b> Un proyecto de 10.000 € con TIR del 100% genera 10.000 € de valor; uno de 1 M€ con TIR del 25% genera 250.000 €.<br/>"
        "3. <b>TIR Múltiples:</b> Si los flujos cambian de signo más de una vez, la regla de los signos de Descartes genera múltiples raíces matemáticas.",
        styles['Callout']
    )
    story.append(make_box(box_conflict, C_AMBER_LIGHT, C_AMBER_ACCENT, 5))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: SECCIÓN 4: CASO PRÁCTICO RESUELTO (CIFRAS EXACTAS model_core.py)
    # =========================================================================
    s4_title = "4. Caso Práctico Resuelto: Automatización de Línea Industrial" if lang == 'ES' else "4. Master Business Case: Industrial Automation & Digitalization"
    story.append(Paragraph(s4_title, styles['SectionTitle']))

    p_s4_intro = (
        "A continuación se detallan las cifras oficiales de referencia generadas por el motor analítico institucional "
        "para el proyecto de automatización y digitalización industrial (CAPEX 1,2 M€; WACC 9,50%):"
        if lang == 'ES' else
        "Below are the verified analytical benchmark figures generated by the institutional DCF engine "
        "for the manufacturing automation investment ($1.2M CAPEX; 9.50% WACC):"
    )
    story.append(Paragraph(p_s4_intro, styles['Body']))

    # Tabla 1: Proyección de Cuenta de Resultados y Flujo de Caja Libre
    t1_head = [
        Paragraph("<b>Línea Financiera (k€)</b>" if lang == 'ES' else "<b>Financial Line ($k)</b>", styles['TableHead']),
        Paragraph("<b>Año 0</b>" if lang == 'ES' else "<b>Year 0</b>", styles['TableHead']),
        Paragraph("<b>Año 1</b>" if lang == 'ES' else "<b>Year 1</b>", styles['TableHead']),
        Paragraph("<b>Año 2</b>" if lang == 'ES' else "<b>Year 2</b>", styles['TableHead']),
        Paragraph("<b>Año 3</b>" if lang == 'ES' else "<b>Year 3</b>", styles['TableHead']),
        Paragraph("<b>Año 4</b>" if lang == 'ES' else "<b>Year 4</b>", styles['TableHead']),
        Paragraph("<b>Año 5</b>" if lang == 'ES' else "<b>Year 5</b>", styles['TableHead']),
    ]

    proj = model_core.PROJ_BASE
    t1_rows = [
        t1_head,
        [Paragraph("Ingresos por ventas" if lang == 'ES' else "Sales revenues", styles['TableCell']), Paragraph("-", styles['TableCellRight']), Paragraph(f"{proj['revenues'][1]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['revenues'][2]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['revenues'][3]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['revenues'][4]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['revenues'][5]/1000:,.1f}", styles['TableCellRight'])],
        [Paragraph("(-) Costes variables (60%)" if lang == 'ES' else "(-) Variable costs (60%)", styles['TableCell']), Paragraph("-", styles['TableCellRight']), Paragraph(f"-{proj['var_costs'][1]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['var_costs'][2]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['var_costs'][3]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['var_costs'][4]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['var_costs'][5]/1000:,.1f}", styles['TableCellRight'])],
        [Paragraph("(-) OPEX fijo anual" if lang == 'ES' else "(-) Fixed annual OPEX", styles['TableCell']), Paragraph("-", styles['TableCellRight']), Paragraph(f"-{proj['opex_fixed'][1]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['opex_fixed'][2]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['opex_fixed'][3]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['opex_fixed'][4]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['opex_fixed'][5]/1000:,.1f}", styles['TableCellRight'])],
        [Paragraph("<b>EBITDA</b>", styles['TableCellBold']), Paragraph("-", styles['TableCellRightBold']), Paragraph(f"<b>{proj['ebitda'][1]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['ebitda'][2]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['ebitda'][3]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['ebitda'][4]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['ebitda'][5]/1000:,.1f}</b>", styles['TableCellRightBold'])],
        [Paragraph("(-) Amortización (D&amp;A)" if lang == 'ES' else "(-) Depreciation (D&amp;A)", styles['TableCell']), Paragraph("-", styles['TableCellRight']), Paragraph(f"-{proj['depreciation'][1]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['depreciation'][2]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['depreciation'][3]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['depreciation'][4]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['depreciation'][5]/1000:,.1f}", styles['TableCellRight'])],
        [Paragraph("NOPAT = EBIT · (1 - t)", styles['TableCell']), Paragraph("-", styles['TableCellRight']), Paragraph(f"{proj['nopat'][1]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['nopat'][2]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['nopat'][3]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['nopat'][4]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['nopat'][5]/1000:,.1f}", styles['TableCellRight'])],
        [Paragraph("(-) CAPEX por tramos" if lang == 'ES' else "(-) Tranched CAPEX", styles['TableCell']), Paragraph(f"-{proj['capex'][0]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['capex'][1]/1000:,.1f}", styles['TableCellRight']), Paragraph("-", styles['TableCellRight']), Paragraph("-", styles['TableCellRight']), Paragraph("-", styles['TableCellRight']), Paragraph("-", styles['TableCellRight'])],
        [Paragraph("(-) Variación NWC" if lang == 'ES' else "(-) Working capital change", styles['TableCell']), Paragraph("-", styles['TableCellRight']), Paragraph(f"-{proj['delta_nwc'][1]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['delta_nwc'][2]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['delta_nwc'][3]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['delta_nwc'][4]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"-{proj['delta_nwc'][5]/1000:,.1f}", styles['TableCellRight'])],
        [Paragraph("<b>FLUJO DE CAJA LIBRE (FCF)</b>" if lang == 'ES' else "<b>FREE CASH FLOW (FCFF)</b>", styles['TableCellBold']), Paragraph(f"<b>{proj['fcf'][0]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['fcf'][1]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['fcf'][2]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['fcf'][3]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['fcf'][4]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['fcf'][5]/1000:,.1f}</b>", styles['TableCellRightBold'])],
        [Paragraph("FCF Acumulado Nominal" if lang == 'ES' else "Cumulative Nominal FCF", styles['TableCell']), Paragraph(f"{proj['cum_fcf'][0]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['cum_fcf'][1]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['cum_fcf'][2]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['cum_fcf'][3]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['cum_fcf'][4]/1000:,.1f}", styles['TableCellRight']), Paragraph(f"{proj['cum_fcf'][5]/1000:,.1f}", styles['TableCellRight'])],
        [Paragraph("<b>VP Acumulado Descontado</b>" if lang == 'ES' else "<b>Cumulative Discounted PV</b>", styles['TableCellBold']), Paragraph(f"<b>{proj['cum_pv_fcf'][0]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['cum_pv_fcf'][1]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['cum_pv_fcf'][2]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['cum_pv_fcf'][3]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['cum_pv_fcf'][4]/1000:,.1f}</b>", styles['TableCellRightBold']), Paragraph(f"<b>{proj['cum_pv_fcf'][5]/1000:,.1f}</b>", styles['TableCellRightBold'])],
    ]

    t1 = Table(t1_rows, colWidths=[151, 60, 60, 60, 60, 60, 60])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BACKGROUND', (0, 4), (-1, 4), C_BG_CARD),
        ('BACKGROUND', (0, 9), (-1, 9), C_BLUE_LIGHT),
        ('BACKGROUND', (0, 11), (-1, 11), C_GREEN_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    # Tabla 2: Resumen Ejecutivo de Métricas y Escenarios
    curr_sym = "€" if lang == 'ES' else "$"
    t2_data = [
        [
            Paragraph("<b>Métrica Clave</b>" if lang == 'ES' else "<b>Core Metric</b>", styles['TableHead']),
            Paragraph("<b>Valor Base</b>" if lang == 'ES' else "<b>Base Value</b>", styles['TableHead']),
            Paragraph("<b>Escenario Pesimista</b>" if lang == 'ES' else "<b>Pessimistic</b>", styles['TableHead']),
            Paragraph("<b>Escenario Optimista</b>" if lang == 'ES' else "<b>Optimistic</b>", styles['TableHead']),
            Paragraph("<b>Criterio Hurdle Policy</b>" if lang == 'ES' else "<b>Hurdle Policy Criteria</b>", styles['TableHead']),
        ],
        [
            Paragraph(f"VAN a 5 Años ({curr_sym})" if lang == 'ES' else f"5-Year NPV ({curr_sym})", styles['TableCell']),
            Paragraph(f"<b>+{model_core.SUMMARY['npv_base']/1000:,.1f} k{curr_sym}</b>", styles['TableCellRightBold']),
            Paragraph(f"{model_core.SUMMARY['npv_pes']/1000:,.1f} k{curr_sym}", styles['TableCellRight']),
            Paragraph(f"+{model_core.SUMMARY['npv_opt']/1000:,.1f} k{curr_sym}", styles['TableCellRight']),
            Paragraph(f"Exigido: VAN > 0 {curr_sym}" if lang == 'ES' else f"Required: NPV > 0 {curr_sym}", styles['TableCell']),
        ],
        [
            Paragraph("TIR / IRR (%)", styles['TableCell']),
            Paragraph(f"<b>{model_core.SUMMARY['irr_base']*100:.2f}%</b>", styles['TableCellRightBold']),
            Paragraph(f"{model_core.SUMMARY['irr_pes']*100:.2f}%", styles['TableCellRight']),
            Paragraph(f"{model_core.SUMMARY['irr_opt']*100:.2f}%", styles['TableCellRight']),
            Paragraph("Exigido: TIR ≥ WACC+3pp (12,5%)" if lang == 'ES' else "Required: IRR ≥ WACC+3pp (12.5%)", styles['TableCell']),
        ],
        [
            Paragraph("Payback Descontado" if lang == 'ES' else "Discounted Payback", styles['TableCell']),
            Paragraph(f"<b>{model_core.SUMMARY['payback_discounted_base']:.2f} años</b>" if lang == 'ES' else f"<b>{model_core.SUMMARY['payback_discounted_base']:.2f} yrs</b>", styles['TableCellRightBold']),
            Paragraph("> 5 años" if lang == 'ES' else "> 5 years", styles['TableCellRight']),
            Paragraph(f"{model_core.SUMMARY['payback_desc_opt']:.2f} años" if lang == 'ES' else f"{model_core.SUMMARY['payback_desc_opt']:.2f} yrs", styles['TableCellRight']),
            Paragraph("Exigido: Payback < 4,0 años" if lang == 'ES' else "Required: Payback < 4.0 yrs", styles['TableCell']),
        ],
        [
            Paragraph(f"Peak Funding ({curr_sym})", styles['TableCell']),
            Paragraph(f"<b>{model_core.SUMMARY['peak_funding_base']/1000:,.1f} k{curr_sym}</b>", styles['TableCellRightBold']),
            Paragraph(f"-1.090 k{curr_sym}", styles['TableCellRight']),
            Paragraph(f"-890 k{curr_sym}", styles['TableCellRight']),
            Paragraph("Límite línea crédito aprobada" if lang == 'ES' else "Approved credit facility ceiling", styles['TableCell']),
        ],
        [
            Paragraph("VAN Esperado E[VAN]" if lang == 'ES' else "Expected NPV E[NPV]", styles['TableCellBold']),
            Paragraph(f"<b>+{model_core.SUMMARY['npv_expected']/1000:,.1f} k{curr_sym}</b>", styles['TableCellRightBold']),
            Paragraph("Ponderación: 20% / 60% / 20%" if lang == 'ES' else "Weighting: 20% / 60% / 20%", styles['TableCell']),
            Paragraph("<b>[OK] Valor Robusto</b>" if lang == 'ES' else "<b>[OK] Robust Value</b>", styles['TableCellBold']),
            Paragraph("<b>DICTAMEN: APROBAR</b>" if lang == 'ES' else "<b>VERDICT: APPROVE</b>", styles['TableCellBold']),
        ],
    ]
    t2 = Table(t2_data, colWidths=[131, 95, 95, 95, 95])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_MED),
        ('BACKGROUND', (0, 5), (-1, 5), C_GREEN_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: SECCIÓN 5: BOARD DEFENSE FAQ (6 PREGUNTAS DIFÍCILES)
    # =========================================================================
    s5_title = "5. Protocolo de Defensa ante el Consejo (Board Defense FAQ)" if lang == 'ES' else "5. Boardroom Defense Protocol: Hard Questions & Model Answers"
    story.append(Paragraph(s5_title, styles['SectionTitle']))

    faqs = [
        (
            "1. ¿De dónde sale exactamente el WACC del 9,50% y por qué no usar el tipo de interés del banco?",
            "El tipo de interés bancario (Kd ≈ 4,67%) refleja únicamente el riesgo asumido por los acreedores de deuda garantizada. "
            "El capital propio (Equity) financia el 75% del proyecto y exige una prima por riesgo operativo (Ke = 11,50% vía CAPM: "
            "Rf 3,50% + Beta 1,20 × ERP 5,50% + prima de tamaño 1,40%). Utilizar el coste bancario en lugar del WACC provocaría "
            "aprobar proyectos destructores de valor para el accionista.",
            "1. Where does the 9.50% WACC come from, and why not use the commercial bank lending rate?",
            "Bank interest (Kd ≈ 4.67%) reflects only the secured debt risk. Equity capital finances 75% of the asset and demands "
            "a risk-adjusted return (Ke = 11.50% via institutional CAPM: Rf 3.50% + Beta 1.20 × ERP 5.50% + 1.40% mid-cap premium). "
            "Discounting at bank borrowing rates instead of WACC systematically approves investments that destroy shareholder wealth."
        ),
        (
            "2. ¿Por qué debemos priorizar el VAN sobre la TIR si la TIR es mucho más intuitiva?",
            "La TIR adolece de dos defectos estructurales graves: primero, asume matemáticamente que los flujos generados cada año "
            "se reinvierten a la propia TIR (28,89%), lo cual es irreal; el VAN asume reinversión al coste de capital WACC (9,50%), "
            "respaldado por la MIRR (21,84%). Segundo, la TIR ignora la escala: preferir un proyecto con TIR del 40% que genera 50 k€ "
            "frente a uno con TIR del 28,9% que genera 693 k€ de VAN destruye 643 k€ de riqueza neta.",
            "2. Why must we rely on NPV over IRR when IRR is far more intuitive to business leaders?",
            "IRR suffers from two fatal flaws: first, it mathematically presumes interim inflows are reinvested at the project's own "
            "IRR (28.89%), which is unrealistic; NPV assumes reinvestment at the actual corporate WACC (9.50%), as confirmed by the MIRR (21.84%). "
            "Second, IRR is scale-blind: favoring a 40% IRR project generating $50k over a 28.9% IRR project generating $693k NPV destroys $643k in wealth."
        ),
        (
            "3. ¿Qué ocurre exactamente si las ventas caen un 20% respecto al plan comercial?",
            "El análisis de sensibilidad Tornado y el cálculo de puntos de equilibrio demuestran que el proyecto soporta una caída de "
            "hasta el -23,2% en volumen (hasta 76.840 unidades) y de hasta el -23,2% en precio (hasta 19,21 €/u) antes de que el VAN caiga a cero. "
            "Una caída del 20% reduce el VAN de 693 k€ a aproximadamente 95 k€, manteniendo el proyecto en zona de creación de valor.",
            "3. What happens if sales drop by 20% relative to the commercial budget?",
            "Tornado sensitivity and linear break-even calculations show the project withstands up to -23.2% in volume (down to 76,840 units) "
            "and -23.2% in price (down to $19.21/u) before NPV drops to zero. A 20% decline compresses NPV from $693k to approximately $95k, "
            "preserving positive value creation."
        ),
        (
            "4. ¿Cuál es la pérdida máxima que puede sufrir la empresa si el proyecto fracasa por completo?",
            "La pérdida máxima queda estrictamente acotada a la necesidad máxima de financiación (Peak Funding: 995.000 €). "
            "Gracias a la estructuración por tramos condicionados y a los Kill Criteria vinculantes, si se detecta un sobrecoste superior al 15% "
            "o un fallo comercial en el mes 9, el Tramo 2 (350.000 €) se congela automáticamente, limitando la exposición a 850.000 €.",
            "4. What is the maximum downside loss if the initiative fails completely?",
            "Maximum downside is capped at Peak Funding ($995,000). Thanks to phased staging and binding Kill Criteria, if a >15% cost overrun "
            "or commercial failure occurs by month 9, Tranche 2 ($350,000) is frozen immediately, limiting total capital exposure to $850,000."
        ),
        (
            "5. ¿Por qué penalizar el flujo de caja con capital circulante si los clientes terminarán pagando?",
            "Porque el capital circulante operativo (NWC = Clientes + Stock − Proveedores) representa liquidez inmovilizada en el balance. "
            "Cada millón adicional de ventas absorbe 100 k€ de caja en inventario y saldos pendientes. Ignorar el ΔNWC sobreestima el flujo disponible "
            "y provocaría tensiones de tesorería imprevistas durante la fase de crecimiento de la línea.",
            "5. Why penalize cash flow with working capital if customers eventually settle their invoices?",
            "Because Operating Working Capital (NWC = Receivables + Inventory − Payables) ties up liquidity on the balance sheet. "
            "Each $1M in sales growth absorbs $100k of cash into operations. Omitting ΔNWC overstates distributable cash and causes severe "
            "working capital cash crunches during ramp-up."
        ),
        (
            "6. ¿Cómo garantizamos que los supuestos del Business Case no han sido manipulados por sesgo optimista?",
            "Mediante tres mecanismos de auditoría: 1) Registro formal de supuestos con evidencia empírica contrastada; 2) Previsión por clase "
            "de referencia (benchmark de proyectos industriales comparables auditados); y 3) Revisión Post-Inversión (PIR) obligatoria a 12 meses "
            "ligada a la evaluación del desempeño y retribución variable del equipo promotor.",
            "6. How do we ensure Business Case assumptions are not inflated by departmental optimism bias?",
            "Through three governance safeguards: 1) Formal assumptions log with verifiable technical evidence; 2) Reference class forecasting "
            "benchmarked against audited peer industrial projects; and 3) Mandatory 12-month Post-Investment Review (PIR) linked to executive "
            "performance evaluation and compensation clawbacks."
        ),
    ]

    for q_es, a_es, q_en, a_en in faqs:
        q = q_es if lang == 'ES' else q_en
        a = a_es if lang == 'ES' else a_en
        story.append(Paragraph(q, styles['FAQQuestion']))
        story.append(Paragraph(a, styles['FAQAnswer']))

    story.append(Spacer(1, 4))

    # =========================================================================
    # SECCIÓN 6: REFERENCIAS BIBLIOGRÁFICAS CANÓNICAS DE AUTORIDAD
    # =========================================================================
    s6_title = "6. Referencias Bibliográficas Canónicas de Autoridad" if lang == 'ES' else "6. Canonical Academic & Practitioner References"
    story.append(Paragraph(s6_title, styles['SectionTitle']))

    refs = [
        "<b>Brealey, R. A., Myers, S. C., & Allen, F. (2020).</b> <i>Principles of Corporate Finance</i> (13ª ed.). McGraw-Hill. "
        "[El texto fundacional de finanzas corporativas que formaliza la superioridad del VAN sobre la TIR y la valoración DCF].",
        "<b>Koller, T., Goedhart, M., & Wessels, D. — McKinsey & Company (2020).</b> <i>Valuation: Measuring and Managing the Value of Companies</i> (7ª ed.). John Wiley & Sons. "
        "[El estándar global de valoración por flujo de caja descontado y cálculo de WACC en consultoría estratégica].",
        "<b>Damodaran, A. (2012).</b> <i>Investment Valuation: Tools and Techniques for Determining the Value of Any Asset</i> (3ª ed.). Wiley. "
        "[Referencia canónica en estimación de Betas, ERP y primas de riesgo por tamaño y sector].",
        "<b>Graham, J. R., & Harvey, C. R. (2001).</b> 'The Theory and Practice of Corporate Finance: Evidence from the Field'. <i>Journal of Financial Economics</i>, 60(2-3), 187-243. "
        "[Estudio empírico seminal sobre cómo el 75% de los CFOs combinan VAN y TIR en comités de inversión].",
        "<b>Lovallo, D., & Kahneman, D. (2003).</b> 'Delusions of Success: How Optimism Undermines Executives' Decisions'. <i>Harvard Business Review</i>, 81(7), 56-63. "
        "[Análisis de la falacia de planificación y sesgo optimista que arruina las previsiones financieras].",
        "<b>Flyvbjerg, B. (2006).</b> 'From Nobel Prize to Project Management: Getting Risks Right'. <i>Project Management Journal</i>, 37(3), 5-15. "
        "[Metodología de previsión por clase de referencia para evitar sobrecostes en grandes inversiones].",
        "<b>Minto, B. (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall. "
        "[Estándar de comunicación ejecutiva y estructuración deductiva de recomendaciones C-Level].",
    ]

    for r_txt in refs:
        story.append(Paragraph(f"• {r_txt}", styles['TableCell']))
        story.append(Spacer(1, 2))

    return story


def generate_pdf(lang='ES', out_path=None):
    """Genera la guía metodológica oficial en formato PDF."""
    print(f"\n[GENERANDO PDF {lang}] -> {out_path}...")
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=45,
        bottomMargin=45
    )

    story = build_pdf_story(lang)

    # Inyectar idioma en el canvas
    def canvas_maker(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c._lang = lang
        return c

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.build(story, canvasmaker=canvas_maker)
    print(f"[OK] Guía PDF generada exitosamente: {out_path}")


def main():
    path_es = os.path.join(
        "packages", "Suite_02_Toma_Decisiones", "03_Business_Case_VAN_TIR",
        "[ES]_Business_Case_VAN_TIR", "Guia_Metodologica_Business_Case_ES.pdf"
    )
    path_en = os.path.join(
        "packages", "Suite_02_Toma_Decisiones", "03_Business_Case_VAN_TIR",
        "[EN]_Financial_Business_Case", "Methodology_Guide_Business_Case_EN.pdf"
    )

    generate_pdf(lang='ES', out_path=path_es)
    generate_pdf(lang='EN', out_path=path_en)
    print("\n[ÉXITO] Generación de guías metodológicas PDF completada.")


if __name__ == "__main__":
    main()
