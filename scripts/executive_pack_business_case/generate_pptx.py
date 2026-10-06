#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 Panorámico: 13.333" x 7.5")
para el Executive Decision Pack Business Case de Datalaria:
1. packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[ES]_Business_Case_VAN_TIR/Presentacion_Business_Case_CLevel_ES.pptx
2. packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[EN]_Financial_Business_Case/Deck_Business_Case_CLevel_EN.pptx

Estructura de 3 Diapositivas bajo la Pirámide de Minto:
- Diapositiva 1: Síntesis Ejecutiva & Recomendación de Inversión (Action Title, 4 KPI cards, dictamen APROBAR, tesis de inversión).
- Diapositiva 2: Evidencia de Riesgo: Gráfico Tornado Nativo & Escenarios (Gráfico horizontal BAR_CLUSTERED nativo con overlap 100, tarjetas pesimista/base/optimista, VAN esperado y puntos de equilibrio).
- Diapositiva 3: Plan de Financiación por Tramos & Board Decision Gateway (Cronograma de CAPEX por tramos, stage gates de OEE, 3 kill criteria y contenedor con 4 acuerdos vinculantes y 4 firmas C-Level).
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor

import model_core

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Paleta Corporativa Datalaria
COLOR_NAVY_DARK = RGBColor(0x0F, 0x17, 0x2A)    # Slate 900
COLOR_NAVY_MED = RGBColor(0x1E, 0x29, 0x3B)     # Slate 800
COLOR_NAVY_LIGHT = RGBColor(0x33, 0x41, 0x55)   # Slate 700
COLOR_BLUE_ACCENT = RGBColor(0x25, 0x63, 0xEB)  # Blue 600
COLOR_BLUE_LIGHT = RGBColor(0xEF, 0xF6, 0xFF)   # Blue 50

COLOR_GREEN_BG = RGBColor(0xD1, 0xFA, 0xE5)     # Green 100
COLOR_GREEN_TEXT = RGBColor(0x06, 0x5F, 0x46)   # Green 800
COLOR_GREEN_ACCENT = RGBColor(0x10, 0xB9, 0x81) # Green 500

COLOR_AMBER_BG = RGBColor(0xFE, 0xF3, 0xC7)     # Amber 100
COLOR_AMBER_TEXT = RGBColor(0x92, 0x40, 0x0E)   # Amber 800
COLOR_AMBER_ACCENT = RGBColor(0xF5, 0x9E, 0x0B) # Amber 500

COLOR_RED_BG = RGBColor(0xFE, 0xE2, 0xE2)       # Red 100
COLOR_RED_TEXT = RGBColor(0x99, 0x1B, 0x1B)     # Red 800
COLOR_RED_ACCENT = RGBColor(0xEF, 0x44, 0x44)   # Red 500

COLOR_BG_CARD = RGBColor(0xF8, 0xFA, 0xFC)      # Slate 50
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_BORDER_LIGHT = RGBColor(0xCB, 0xD5, 0xE1) # Slate 300
COLOR_BORDER_MED = RGBColor(0x94, 0xA3, 0xB8)   # Slate 400
COLOR_MUTED_TEXT = RGBColor(0x64, 0x74, 0x8B)   # Slate 500

FONT_NAME = "Segoe UI"


def create_header(slide, title_text, category_badge, lang='ES'):
    """Crea la cabecera ejecutiva con Action Title y badge de contexto corporativo."""
    # Badge superior de categoría
    badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
    tf_b = badge_box.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = Inches(0)
    tf_b.margin_top = Inches(0)
    tf_b.margin_bottom = Inches(0)
    p_b = tf_b.paragraphs[0]
    p_b.text = category_badge.upper()
    p_b.font.name = FONT_NAME
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_BLUE_ACCENT

    # Action Title (Pirámide de Minto)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.85))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = Inches(0)
    tf_t.margin_top = Inches(0)
    tf_t.margin_bottom = Inches(0)
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_NAME
    p_t.font.size = Pt(15.0)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK


def add_kpi_card(slide, left, top, width, height, title, value_str, subtitle, bg_color=COLOR_BG_CARD, val_color=COLOR_NAVY_DARK):
    """Crea una tarjeta KPI estilizada con bordes y tipografía ejecutiva."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = COLOR_BORDER_LIGHT
    shape.line.width = Pt(1)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.1)
    tf.margin_bottom = Inches(0.1)

    p0 = tf.paragraphs[0]
    p0.text = title.upper()
    p0.font.name = FONT_NAME
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_MUTED_TEXT

    p1 = tf.add_paragraph()
    p1.text = value_str
    p1.font.name = FONT_NAME
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = val_color

    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.name = FONT_NAME
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = COLOR_NAVY_LIGHT


def build_slide1_executive_summary(prs, lang='ES'):
    """Diapositiva 1: Síntesis Ejecutiva & Recomendación de Inversión."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    badge = (
        "SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN | CORPORATE FINANCE STANDARD"
        if lang == 'ES' else
        "SUITE 02 · DECISION ANALYSIS & PRIORITIZATION | CORPORATE FINANCE STANDARD"
    )
    title = (
        "La automatización de la línea genera un VAN de 693 k€ y una TIR del 28,9% frente a un WACC del 9,5%, "
        "recuperando la inversión en 3,35 años: se solicita aprobar 1,2 M€ de CAPEX en dos tramos condicionados."
        if lang == 'ES' else
        "Production line automation yields $693k NPV and 28.9% IRR against a 9.5% WACC, recovering capital in 3.35 years: "
        "request approval for $1.2M CAPEX across two conditional milestone tranches."
    )
    create_header(slide, title, badge, lang)

    # 4 Tarjetas KPI Alineadas (Filas de arriba: top = 1.65", height = 1.35")
    card_w = Inches(2.78)
    card_h = Inches(1.35)
    gap = Inches(0.2)
    start_x = Inches(0.8)

    kpis = [
        ("VAN a 5 Años (NPV)" if lang == 'ES' else "5-Year Net Present Value (NPV)", "+693 k€" if lang == 'ES' else "+$693k", "Tasa de descuento WACC = 9,50%" if lang == 'ES' else "Discount hurdle WACC = 9.50%", COLOR_BG_CARD, COLOR_BLUE_ACCENT),
        ("TIR vs. WACC (Spread)" if lang == 'ES' else "IRR vs. WACC Spread", "28,9%" if lang == 'ES' else "28.9%", "+19,4 pp sobre WACC (mín. exigido: +3 pp)" if lang == 'ES' else "+19.4 pp above WACC (hurdle: +3 pp)", COLOR_BG_CARD, COLOR_GREEN_TEXT),
        ("Payback Descontado" if lang == 'ES' else "Discounted Payback", "3,35 años" if lang == 'ES' else "3.35 yrs", "Umbral máx. política: < 4,0 años" if lang == 'ES' else "Corporate policy limit: < 4.0 yrs", COLOR_BG_CARD, COLOR_NAVY_DARK),
        ("Peak Funding (Máx. Caja)" if lang == 'ES' else "Peak Funding Exposure", "-995 k€" if lang == 'ES' else "-$995k", "Exposición pico en Q4 Año 1" if lang == 'ES' else "Maximum cash trough in Q4 Year 1", COLOR_BG_CARD, COLOR_RED_TEXT),
    ]

    for i, (k_title, k_val, k_sub, bg, val_col) in enumerate(kpis):
        x = start_x + i * (card_w + gap)
        add_kpi_card(slide, x, Inches(1.65), card_w, card_h, k_title, k_val, k_sub, bg, val_col)

    # Sello de Dictamen Prominente (Columna Izquierda: x=0.8", y=3.2", w=3.6", h=3.8")
    seal_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(3.6), Inches(3.8))
    seal_box.fill.solid()
    seal_box.fill.fore_color.rgb = COLOR_GREEN_BG
    seal_box.line.color.rgb = COLOR_GREEN_ACCENT
    seal_box.line.width = Pt(2)

    tf_seal = seal_box.text_frame
    tf_seal.word_wrap = True
    tf_seal.margin_left = Inches(0.2)
    tf_seal.margin_right = Inches(0.2)
    tf_seal.margin_top = Inches(0.2)
    tf_seal.margin_bottom = Inches(0.2)

    p_s0 = tf_seal.paragraphs[0]
    p_s0.text = "DICTAMEN DEL COMITÉ" if lang == 'ES' else "COMMITTEE VERDICT"
    p_s0.font.name = FONT_NAME
    p_s0.font.size = Pt(10)
    p_s0.font.bold = True
    p_s0.font.color.rgb = COLOR_GREEN_TEXT

    p_s1 = tf_seal.add_paragraph()
    p_s1.text = "✅ APROBAR" if lang == 'ES' else "✅ APPROVE"
    p_s1.font.name = FONT_NAME
    p_s1.font.size = Pt(22)
    p_s1.font.bold = True
    p_s1.font.color.rgb = COLOR_GREEN_TEXT

    p_s2 = tf_seal.add_paragraph()
    p_s2.text = (
        "El proyecto cumple simultáneamente todos los criterios de la política interna de inversión:\n\n"
        "• VAN positivo (+693 k€) con creación neta de valor.\n"
        "• TIR del 28,9%, superando en +19,4 pp el WACC del 9,5% (muy por encima del margen exigido de +3 pp).\n"
        "• Payback descontado de 3,35 años, inferior al límite de 4,0 años de política corporativa.\n"
        "• Financiación en 2 tramos con stage gates para blindar la tesorería de la compañía."
        if lang == 'ES' else
        "The project simultaneously clears all internal corporate hurdle policy criteria:\n\n"
        "• Positive NPV (+$693k) generating net shareholder value.\n"
        "• IRR of 28.9%, clearing 9.5% WACC by +19.4 pp (well above the required +3.0 pp spread).\n"
        "• Discounted payback of 3.35 years, comfortably within the 4.0-year policy limit.\n"
        "• 2-tranche staged financing structure protecting corporate cash flow."
    )
    p_s2.font.name = FONT_NAME
    p_s2.font.size = Pt(9.5)
    p_s2.font.color.rgb = COLOR_NAVY_DARK

    # Contenedor de Síntesis Estratégica (Columna Derecha: x=4.65", y=3.2", w=7.88", h=3.8")
    synth_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.65), Inches(3.2), Inches(7.88), Inches(3.8))
    synth_box.fill.solid()
    synth_box.fill.fore_color.rgb = COLOR_BG_CARD
    synth_box.line.color.rgb = COLOR_BORDER_LIGHT
    synth_box.line.width = Pt(1)

    tf_syn = synth_box.text_frame
    tf_syn.word_wrap = True
    tf_syn.margin_left = Inches(0.25)
    tf_syn.margin_right = Inches(0.25)
    tf_syn.margin_top = Inches(0.2)
    tf_syn.margin_bottom = Inches(0.2)

    p_sy0 = tf_syn.paragraphs[0]
    p_sy0.text = "SÍNTESIS ESTRATÉGICA & TESIS DE INVERSIÓN (BOARDROOM BRIEF)" if lang == 'ES' else "STRATEGIC RATIONALE & INVESTMENT THESIS (BOARDROOM BRIEF)"
    p_sy0.font.name = FONT_NAME
    p_sy0.font.size = Pt(11)
    p_sy0.font.bold = True
    p_sy0.font.color.rgb = COLOR_BLUE_ACCENT

    p_sy1 = tf_syn.add_paragraph()
    p_sy1.text = (
        "1. Desafío Operativo & Oportunidad de Mercado:\n"
        "La línea actual opera al 92% de saturación con costes de mantenimiento crecientes (+14% interanual) y mermas del 4,2%. La automatización robótica y el software MES reducirán el coste variable del 65% al 60% sobre ventas y elevarán la capacidad efectiva en un 35%.\n\n"
        "2. Estructura de Capital & Financiación por Tramos:\n"
        "Inversión total de 1.200.000 € dividida en Tramo 1 (850 k€ en Q1 Año 0 para maquinaria e ingeniería) y Tramo 2 (350 k€ en Q4 Año 1 para software y robótica). La liberación del Tramo 2 queda contractualmente supeditada a superar las pruebas FAT y alcanzar un OEE preliminar ≥ 75%.\n\n"
        "3. Solidez Financiera ante Incertidumbre Macro:\n"
        "Incluso bajo el escenario pesimista (caída del volumen del 8% y encarecimiento del OPEX), el VAN se sitúa en equilibrio (-30 k€, TIR 8,6%). El análisis Tornado confirma que el proyecto soporta caídas de ventas de hasta el 23,2% antes de comprometer el capital de la firma."
        if lang == 'ES' else
        "1. Operational Challenge & Market Opportunity:\n"
        "Current production line operates at 92% saturation with escalating maintenance costs (+14% YoY) and 4.2% scrap rate. Robotic automation and MES software will reduce variable cost from 65% to 60% of sales and increase effective throughput by 35%.\n\n"
        "2. Phased Capital Structure & Stage Gates:\n"
        "Total capital expenditure of $1,200,000 split into Tranche 1 ($850k in Q1 Year 0 for robotics procurement and facility prep) and Tranche 2 ($350k in Q4 Year 1 for integration). Tranche 2 release is contractually contingent upon passing FAT testing and achieving preliminary OEE ≥ 75%.\n\n"
        "3. Financial Resilience Under Macro Stress:\n"
        "Even under the downside scenario (-8% sales volume and cost inflation), the project hovers at break-even (-$30k NPV, 8.6% IRR). Tornado analysis proves the investment withstands up to -23.2% commercial sales contraction before destroying capital."
    )
    p_sy1.font.name = FONT_NAME
    p_sy1.font.size = Pt(9.5)
    p_sy1.font.color.rgb = COLOR_NAVY_DARK


def build_slide2_risk_tornado(prs, lang='ES'):
    """Diapositiva 2: Evidencia de Riesgo: Gráfico Tornado & Escenarios."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    badge = (
        "SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN | ANÁLISIS DE RIESGO CUANTITATIVO"
        if lang == 'ES' else
        "SUITE 02 · DECISION ANALYSIS & PRIORITIZATION | QUANTITATIVE RISK ANALYSIS"
    )
    title = (
        "El análisis Tornado revela que Precio y Volumen dominan el 70% de la volatilidad del VAN, con márgenes "
        "de seguridad holgados: resiste caídas de demanda de hasta el 23,2% antes de destruir valor."
        if lang == 'ES' else
        "Tornado analysis demonstrates Price and Volume drive 70% of NPV volatility with robust safety margins: "
        "the project withstands up to -23.2% demand contraction before destroying net value."
    )
    create_header(slide, title, badge, lang)

    # 1. Contenedor Izquierdo: Gráfico Tornado Nativo (~60% ancho: x=0.8", y=1.65", w=7.4", h=5.45")
    chart_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(7.4), Inches(5.45))
    chart_bg.fill.solid()
    chart_bg.fill.fore_color.rgb = COLOR_WHITE
    chart_bg.line.color.rgb = COLOR_BORDER_LIGHT
    chart_bg.line.width = Pt(1)

    # Título y Subtítulo/Leyenda en la cabecera del contenedor
    t_box = slide.shapes.add_textbox(Inches(0.95), Inches(1.72), Inches(7.1), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_top = Inches(0)
    tf_t.margin_bottom = Inches(0)
    p_tb = tf_t.paragraphs[0]
    p_tb.text = (
        "GRÁFICO TORNADO: SENSIBILIDAD DEL VAN POR DRIVER (Δ k€ vs. CASO BASE 693 k€)"
        if lang == 'ES' else
        "TORNADO SENSITIVITY CHART: NPV IMPACT BY DRIVER (Δ $k vs. BASE CASE $693k)"
    )
    p_tb.font.name = FONT_NAME
    p_tb.font.size = Pt(10)
    p_tb.font.bold = True
    p_tb.font.color.rgb = COLOR_NAVY_DARK

    p_sub = tf_t.add_paragraph()
    p_sub.text = (
        "■ Rojo: Impacto Desfavorable (Downside)    |    ■ Verde: Impacto Favorable (Upside)"
        if lang == 'ES' else
        "■ Red: Downside Impact (Unfavorable)    |    ■ Green: Upside Impact (Favorable)"
    )
    p_sub.font.name = FONT_NAME
    p_sub.font.size = Pt(8.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_MUTED_TEXT

    # Construir datos para gráfico nativo BAR_CLUSTERED
    # Para que el driver de mayor amplitud quede arriba en PowerPoint horizontal,
    # pasamos las categorías desde menor amplitud (abajo) hasta mayor amplitud (arriba).
    tornado_rows_reversed = list(reversed(model_core.TORNADO_RESULTS))
    cats = [
        r["name_es"].split("(")[0].strip() if lang == 'ES' else r["name_en"].split("(")[0].strip()
        for r in tornado_rows_reversed
    ]
    deltas_neg = [round(r["delta_pessimistic"] / 1000.0, 1) for r in tornado_rows_reversed]
    deltas_pos = [round(r["delta_optimistic"] / 1000.0, 1) for r in tornado_rows_reversed]

    chart_data = CategoryChartData()
    chart_data.categories = cats
    chart_data.add_series("Δ Impacto Negativo" if lang == 'ES' else "Δ Downside Impact", deltas_neg)
    chart_data.add_series("Δ Impacto Positivo" if lang == 'ES' else "Δ Upside Impact", deltas_pos)

    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(0.95), Inches(2.25), Inches(7.05), Inches(4.55),
        chart_data
    )
    chart = chart_shape.chart
    chart.has_legend = False
    chart.plots[0].gap_width = 50
    chart.plots[0].overlap = 100

    # Categorías alineadas a la izquierda (fuera de las barras)
    chart.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    chart.category_axis.tick_labels.font.name = FONT_NAME
    chart.category_axis.tick_labels.font.size = Pt(8.5)

    # Valores numéricos en la base inferior
    chart.value_axis.tick_labels.font.name = FONT_NAME
    chart.value_axis.tick_labels.font.size = Pt(8.5)

    # Formatear series: Rojo sólido para negativo, Verde sólido para positivo, sin inversión a blanco
    if len(chart.series) >= 2:
        chart.series[0].format.fill.solid()
        chart.series[0].format.fill.fore_color.rgb = COLOR_RED_ACCENT
        chart.series[0].invert_if_negative = False

        chart.series[1].format.fill.solid()
        chart.series[1].format.fill.fore_color.rgb = COLOR_GREEN_ACCENT
        chart.series[1].invert_if_negative = False

    # 2. Contenedor Derecho: Escenarios y Break-Even (x=8.3", y=1.65", w=4.233", h=5.45")
    # Tarjeta de Escenarios (Mitad superior derecha: y=1.65", h=2.95")
    scen_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.65), Inches(4.233), Inches(2.95))
    scen_box.fill.solid()
    scen_box.fill.fore_color.rgb = COLOR_BG_CARD
    scen_box.line.color.rgb = COLOR_BORDER_LIGHT
    scen_box.line.width = Pt(1)

    tf_sc = scen_box.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = Inches(0.18)
    tf_sc.margin_right = Inches(0.18)
    tf_sc.margin_top = Inches(0.14)
    tf_sc.margin_bottom = Inches(0.14)

    p_sc0 = tf_sc.paragraphs[0]
    p_sc0.text = "MATRIZ DE ESCENARIOS Y VAN ESPERADO" if lang == 'ES' else "SCENARIO MATRIX & EXPECTED NPV"
    p_sc0.font.name = FONT_NAME
    p_sc0.font.size = Pt(10.5)
    p_sc0.font.bold = True
    p_sc0.font.color.rgb = COLOR_BLUE_ACCENT

    p_sc1 = tf_sc.add_paragraph()
    p_sc1.text = (
        "• Escenario Pesimista (p = 25%):\n"
        "  VAN = -30 k€ | TIR = 8,61% | Payback > 5 años\n"
        "  (Volumen: 92.000 u. | Precio: 24,00 € | CAPEX: 1,25 M€)\n\n"
        "• Escenario Base (p = 50%):\n"
        "  VAN = +693 k€ | TIR = 28,89% | Payback = 3,35 años\n"
        "  (Volumen: 100.000 u. | Precio: 25,00 € | CAPEX: 1,20 M€)\n\n"
        "• Escenario Optimista (p = 25%):\n"
        "  VAN = +1.609 k€ | TIR = 52,39% | Payback = 2,36 años\n"
        "  (Volumen: 110.000 u. | Precio: 26,00 € | CAPEX: 1,15 M€)\n\n"
        "➜ VALOR ACTUAL NETO ESPERADO: E[VAN] = +741 k€"
        if lang == 'ES' else
        "• Downside Scenario (p = 25%):\n"
        "  NPV = -$30k | IRR = 8.61% | Payback > 5 yrs\n"
        "  (Volume: 92,000 u. | Price: $24.00 | CAPEX: $1.25M)\n\n"
        "• Base Central Case (p = 50%):\n"
        "  NPV = +$693k | IRR = 28.89% | Payback = 3.35 yrs\n"
        "  (Volume: 100,000 u. | Price: $25.00 | CAPEX: $1.20M)\n\n"
        "• Upside Scenario (p = 25%):\n"
        "  NPV = +$1,609k | IRR = 52.39% | Payback = 2.36 yrs\n"
        "  (Volume: 110,000 u. | Price: $26.00 | CAPEX: $1.15M)\n\n"
        "➜ EXPECTED NET PRESENT VALUE: E[NPV] = +$741k"
    )
    p_sc1.font.name = FONT_NAME
    p_sc1.font.size = Pt(8.5)
    p_sc1.font.color.rgb = COLOR_NAVY_DARK

    # Tarjeta de Puntos de Equilibrio (Mitad inferior derecha: y=4.75", h=2.35")
    be_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(4.75), Inches(4.233), Inches(2.35))
    be_box.fill.solid()
    be_box.fill.fore_color.rgb = COLOR_AMBER_BG
    be_box.line.color.rgb = COLOR_AMBER_ACCENT
    be_box.line.width = Pt(1.5)

    tf_be = be_box.text_frame
    tf_be.word_wrap = True
    tf_be.margin_left = Inches(0.18)
    tf_be.margin_right = Inches(0.18)
    tf_be.margin_top = Inches(0.14)
    tf_be.margin_bottom = Inches(0.14)

    p_be0 = tf_be.paragraphs[0]
    p_be0.text = "PUNTOS DE EQUILIBRIO (BREAK-EVEN: VAN = 0)" if lang == 'ES' else "BREAK-EVEN POINTS (NPV = 0 THRESHOLDS)"
    p_be0.font.name = FONT_NAME
    p_be0.font.size = Pt(9.5)
    p_be0.font.bold = True
    p_be0.font.color.rgb = COLOR_AMBER_TEXT

    p_be1 = tf_be.add_paragraph()
    p_be1.text = (
        "• Precio de Equilibrio: 19,21 €/u (Caída máxima admisible: -23,2%)\n"
        "• Volumen de Equilibrio: 76.840 u. (Caída máxima admisible: -23,2%)\n"
        "• Sobrecoste Máximo CAPEX: 2.070.561 € (Sobrecoste admisible: +72,5%)\n\n"
        "Conclusión de Riesgo: Se requeriría una contracción comercial superior al 23% "
        "para que el proyecto destruya valor económico."
        if lang == 'ES' else
        "• Break-Even Unit Price: $19.21/u (Tolerates max decline: -23.2%)\n"
        "• Break-Even Sales Volume: 76,840 units (Tolerates max decline: -23.2%)\n"
        "• Max Tolerable CAPEX: $2,070,561 (Tolerates overrun up to: +72.5%)\n\n"
        "Risk Conclusion: It would require a severe sales contraction exceeding 23% "
        "to wipe out the investment's net economic value."
    )
    p_be1.font.name = FONT_NAME
    p_be1.font.size = Pt(8.5)
    p_be1.font.color.rgb = COLOR_NAVY_DARK


def build_slide3_governance(prs, lang='ES'):
    """Diapositiva 3: Plan de Financiación por Tramos & Board Decision Gateway."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    badge = (
        "SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN | GOBERNANZA & PLAN DE EJECUCIÓN"
        if lang == 'ES' else
        "SUITE 02 · DECISION ANALYSIS & PRIORITIZATION | GOVERNANCE & EXECUTION ROADMAP"
    )
    title = (
        "Desembolso por tramos condicionados (850 k€ en Q1 y 350 k€ en Q4) con stage gates de OEE "
        "y criterios vinculantes de cancelación protege la tesorería de la compañía."
        if lang == 'ES' else
        "Phased capital tranches ($850k in Q1 and $350k in Q4) with OEE stage gates and binding "
        "stop-loss kill criteria safeguard corporate liquidity."
    )
    create_header(slide, title, badge, lang)

    # Mitad Superior: Cronograma de Financiación & Kill Criteria (y=1.65", h=2.25")
    # Caja Izquierda: Cronograma por Tramos (x=0.8", w=5.7", h=2.25")
    sched_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.7), Inches(2.25))
    sched_box.fill.solid()
    sched_box.fill.fore_color.rgb = COLOR_BG_CARD
    sched_box.line.color.rgb = COLOR_BORDER_LIGHT
    sched_box.line.width = Pt(1)

    tf_sc = sched_box.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = Inches(0.18)
    tf_sc.margin_right = Inches(0.18)
    tf_sc.margin_top = Inches(0.12)
    tf_sc.margin_bottom = Inches(0.12)

    p_sc0 = tf_sc.paragraphs[0]
    p_sc0.text = "CRONOGRAMA DE FINANCIACIÓN POR TRAMOS (CAPEX STAGING)" if lang == 'ES' else "PHASED FINANCING ROADMAP (CAPEX STAGING)"
    p_sc0.font.name = FONT_NAME
    p_sc0.font.size = Pt(9.5)
    p_sc0.font.bold = True
    p_sc0.font.color.rgb = COLOR_BLUE_ACCENT

    p_sc1 = tf_sc.add_paragraph()
    p_sc1.text = (
        "• Tramo 1 (Q1 Año 0) | 850.000 €:\n"
        "  Ingeniería de detalle, obra civil y maquinaria principal.\n"
        "  Stage Gate 1: Pruebas FAT en fábrica superadas al 100% sin incidencias.\n\n"
        "• Tramo 2 (Q4 Año 1) | 350.000 €:\n"
        "  Software MES, robótica en planta y puesta en marcha.\n"
        "  Stage Gate 2: Pruebas SAT superadas y OEE preliminar ≥ 75%.\n\n"
        "➜ Total Inversión Comprometida: 1.200.000 € (Peak Funding: -995.000 €)"
        if lang == 'ES' else
        "• Tranche 1 (Q1 Year 0) | $850,000:\n"
        "  Detailed engineering, facility preparation and primary robotics.\n"
        "  Stage Gate 1: 100% FAT sign-off with zero critical non-conformities.\n\n"
        "• Tranche 2 (Q4 Year 1) | $350,000:\n"
        "  MES software, cell robotics integration and commissioning.\n"
        "  Stage Gate 2: Site SAT acceptance and preliminary OEE ≥ 75%.\n\n"
        "➜ Total Committed Capital: $1,200,000 (Peak Funding: -$995,000)"
    )
    p_sc1.font.name = FONT_NAME
    p_sc1.font.size = Pt(8.2)
    p_sc1.font.color.rgb = COLOR_NAVY_DARK

    # Caja Derecha: Criterios de Cancelación Vinculantes (x=6.7", w=5.833", h=2.25")
    kill_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(1.65), Inches(5.833), Inches(2.25))
    kill_box.fill.solid()
    kill_box.fill.fore_color.rgb = COLOR_RED_BG
    kill_box.line.color.rgb = COLOR_RED_ACCENT
    kill_box.line.width = Pt(1.5)

    tf_k = kill_box.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = Inches(0.18)
    tf_k.margin_right = Inches(0.18)
    tf_k.margin_top = Inches(0.12)
    tf_k.margin_bottom = Inches(0.12)

    p_k0 = tf_k.paragraphs[0]
    p_k0.text = "CRITERIOS DE CANCELACIÓN VINCULANTES (KILL CRITERIA / STOP-LOSS)" if lang == 'ES' else "BINDING PROJECT ABORT RULES (KILL CRITERIA / STOP-LOSS POLICY)"
    p_k0.font.name = FONT_NAME
    p_k0.font.size = Pt(9.5)
    p_k0.font.bold = True
    p_k0.font.color.rgb = COLOR_RED_TEXT

    p_k1 = tf_k.add_paragraph()
    p_k1.text = (
        "1. Sobrecoste Técnico (> 15% Tramo 1):\n"
        "   Si el sobrecoste supera 127.500 € en Q3, congelar automáticamente Tramo 2.\n\n"
        "2. Demanda Comercial Inadecuada (< 75% Plan):\n"
        "   Si a 9 meses los contratos no alcanzan 69.000 u., suspender automatización.\n\n"
        "3. Deterioro de Rentabilidad (TIR < WACC):\n"
        "   Si el DCF revisado arroja una TIR < 9,50%, ejecutar plan formal de salida."
        if lang == 'ES' else
        "1. Engineering Overrun (> 15% Tranche 1):\n"
        "   If engineering costs exceed +$127.5k by Q3, immediately freeze Tranche 2.\n\n"
        "2. Demand Shortfall (< 75% Plan Target):\n"
        "   If confirmed sales backlog at 9 months fails to reach 69,000 units, halt robotics.\n\n"
        "3. Hurdle Impairment (Revised IRR < WACC):\n"
        "   If annual DCF re-underwriting yields revised IRR < 9.50%, execute formal exit."
    )
    p_k1.font.name = FONT_NAME
    p_k1.font.size = Pt(8.2)
    p_k1.font.color.rgb = COLOR_NAVY_DARK

    # Mitad Inferior: Board Decision Gateway Container (x=0.8", y=4.05", w=11.733", h=3.15")
    gate_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.05), Inches(11.733), Inches(3.15))
    gate_box.fill.solid()
    gate_box.fill.fore_color.rgb = COLOR_WHITE
    gate_box.line.color.rgb = COLOR_BLUE_ACCENT
    gate_box.line.width = Pt(1.5)

    # Texto de Acuerdos Vinculantes (Cuadro dedicado)
    ag_box = slide.shapes.add_textbox(Inches(1.05), Inches(4.15), Inches(11.2), Inches(1.30))
    tf_ag = ag_box.text_frame
    tf_ag.word_wrap = True
    tf_ag.margin_left = Inches(0)
    tf_ag.margin_right = Inches(0)
    tf_ag.margin_top = Inches(0)
    tf_ag.margin_bottom = Inches(0)

    p_g0 = tf_ag.paragraphs[0]
    p_g0.text = "DECISIÓN REQUERIDA DEL COMITÉ DE INVERSIONES (BOARD DECISION GATEWAY)" if lang == 'ES' else "DECISION REQUIRED FROM THE INVESTMENT COMMITTEE (BOARD DECISION GATEWAY)"
    p_g0.font.name = FONT_NAME
    p_g0.font.size = Pt(10.5)
    p_g0.font.bold = True
    p_g0.font.color.rgb = COLOR_BLUE_ACCENT

    p_hdr = tf_ag.add_paragraph()
    p_hdr.text = "ACUERDOS VINCULANTES SOMETIDOS A VOTACIÓN FORMAL:" if lang == 'ES' else "BINDING RESOLUTIONS SUBMITTED FOR FORMAL APPROVAL:"
    p_hdr.font.name = FONT_NAME
    p_hdr.font.size = Pt(8.5)
    p_hdr.font.bold = True
    p_hdr.font.color.rgb = COLOR_NAVY_DARK

    agreements = [
        (
            "1. Aprobación del CAPEX total (1.200.000 €) y desembolso inmediato de 850.000 € para el Tramo 1 (Q1 Año 0).",
            "1. Approval of total $1,200,000 CAPEX with immediate release of $850,000 for Tranche 1 (Q1 Year 0)."
        ),
        (
            "2. Supeditar la liberación del Tramo 2 (350.000 € en Q4) a la superación formal de Stage Gates de OEE (≥ 75%).",
            "2. Conditional release of Tranche 2 ($350,000 in Q4) subject to formal sign-off of OEE Stage Gates (≥ 75%)."
        ),
        (
            "3. Mandato vinculante de activar Stop-Loss Kill Criteria ante desviaciones de ingeniería o demanda > 15%.",
            "3. Binding mandate to enforce Stop-Loss Kill Criteria if project deviations exceed 15%."
        ),
        (
            "4. Designación del COO como sponsor de ejecución y fijación de Revisión Post-Inversión (PIR) formal a 12 meses.",
            "4. Appointment of COO as executive sponsor and scheduling of formal 12-month Post-Investment Review (PIR)."
        )
    ]
    for ag_es, ag_en in agreements:
        p_item = tf_ag.add_paragraph()
        p_item.text = ag_es if lang == 'ES' else ag_en
        p_item.font.name = FONT_NAME
        p_item.font.size = Pt(8.2)
        p_item.font.color.rgb = COLOR_NAVY_DARK

    # 4 Tarjetas de Firma individuales (Fondo gris suave, borde fino)
    sig_w = Inches(2.65)
    sig_h = Inches(1.25)
    sig_gap = Inches(0.20)
    sig_y = Inches(5.75)

    sigs = [
        (
            "Consejero Delegado (CEO)" if lang == 'ES' else "Chief Executive Officer (CEO)",
            "Aprobación Estratégica Global" if lang == 'ES' else "Strategic Sign-Off"
        ),
        (
            "Director Financiero (CFO)" if lang == 'ES' else "Chief Financial Officer (CFO)",
            "Validación WACC, VAN & Financiación" if lang == 'ES' else "WACC, NPV & Financing Sign-Off"
        ),
        (
            "Presidente Comité Inversiones" if lang == 'ES' else "Investment Committee Chair",
            "Dictamen Hurdle Policy & Stage Gates" if lang == 'ES' else "Hurdle Policy Verdict"
        ),
        (
            "Director de Operaciones (COO)" if lang == 'ES' else "Chief Operating Officer (COO)",
            "Compromiso CAPEX, OEE y Plazos" if lang == 'ES' else "CAPEX, OEE & Schedule Commitment"
        ),
    ]

    for i, (role_txt, man_txt) in enumerate(sigs):
        x = Inches(1.05) + i * (sig_w + sig_gap)
        s_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, sig_y, sig_w, sig_h)
        s_card.fill.solid()
        s_card.fill.fore_color.rgb = COLOR_BG_CARD
        s_card.line.color.rgb = COLOR_BORDER_LIGHT
        s_card.line.width = Pt(1)

        tf_s = s_card.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = Inches(0.15)
        tf_s.margin_right = Inches(0.15)
        tf_s.margin_top = Inches(0.12)
        tf_s.margin_bottom = Inches(0.08)

        p0 = tf_s.paragraphs[0]
        p0.text = role_txt
        p0.font.name = FONT_NAME
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_DARK

        p1 = tf_s.add_paragraph()
        p1.text = man_txt
        p1.font.name = FONT_NAME
        p1.font.size = Pt(7.5)
        p1.font.color.rgb = COLOR_MUTED_TEXT

        p2 = tf_s.add_paragraph()
        p2.text = "Firma: ________________________" if lang == 'ES' else "Signature: ____________________"
        p2.font.name = FONT_NAME
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = COLOR_NAVY_MED


def generate_deck(lang='ES', out_path=None):
    """Genera la presentación ejecutiva completa de 3 diapositivas."""
    print(f"\n[GENERANDO PPTX {lang}] -> {out_path}...")
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide1_executive_summary(prs, lang)
    build_slide2_risk_tornado(prs, lang)
    build_slide3_governance(prs, lang)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    prs.save(out_path)
    print(f"[OK] Presentación generada exitosamente: {out_path}")


def main():
    path_es = os.path.join(
        "packages", "Suite_02_Toma_Decisiones", "03_Business_Case_VAN_TIR",
        "[ES]_Business_Case_VAN_TIR", "Presentacion_Business_Case_CLevel_ES.pptx"
    )
    path_en = os.path.join(
        "packages", "Suite_02_Toma_Decisiones", "03_Business_Case_VAN_TIR",
        "[EN]_Financial_Business_Case", "Deck_Business_Case_CLevel_EN.pptx"
    )

    generate_deck(lang='ES', out_path=path_es)
    generate_deck(lang='EN', out_path=path_en)
    print("\n[ÉXITO] Generación de presentaciones PowerPoint C-Level completada.")


if __name__ == "__main__":
    main()
