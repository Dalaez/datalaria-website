#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/ES_Matriz_McKinsey_GE_Presentacion.pptx (Versión en Español)
2. packages/EN_McKinsey_GE_Matrix_Presentation.pptx (Versión en Inglés)

Características de diseño Tier-1 (McKinsey / BCG):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Pirámide de Minto y Action Titles contundentes.
- Diapositiva 1: Executive Portfolio Overview & 9-Box Grid Layout (con gráfico cartesiano de burbujas en alta resolución y KPI cards).
- Diapositiva 2: Strategic Zone Diagnostics & Risk-Return Profiling (3 paneles ejecutivos: Invertir / Seleccionar / Cosechar).
- Diapositiva 3: Board Decision Gateway & Capital Allocation Mandate (Tabla de gobernanza, 3 resoluciones formales y bloque de firmas).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = RGBColor(15, 23, 42)       # #0F172A Slate 900
COLOR_NAVY_MED = RGBColor(30, 41, 59)        # #1E293B Slate 800
COLOR_BLUE_ACCENT = RGBColor(37, 99, 235)    # #2563EB Blue 600
COLOR_BLUE_LIGHT = RGBColor(239, 246, 255)   # #EFF6FF Blue 50

# Zonas Estratégicas
COLOR_GREEN_BG = RGBColor(209, 250, 229)     # #D1FAE5 Verde suave
COLOR_GREEN_BORDER = RGBColor(16, 185, 129)  # #10B981 Verde acento
COLOR_GREEN_TEXT = RGBColor(6, 95, 70)       # #065F46 Verde texto

COLOR_AMBER_BG = RGBColor(254, 243, 199)     # #FEF3C7 Ámbar suave
COLOR_AMBER_BORDER = RGBColor(245, 158, 11)  # #F59E0B Ámbar acento
COLOR_AMBER_TEXT = RGBColor(146, 64, 14)     # #92400E Ámbar texto

COLOR_RED_BG = RGBColor(254, 226, 226)       # #FEE2E2 Rojo suave
COLOR_RED_BORDER = RGBColor(239, 68, 68)     # #EF4444 Rojo acento
COLOR_RED_TEXT = RGBColor(153, 27, 27)       # #991B1B Rojo texto

COLOR_TEXT_MAIN = RGBColor(51, 65, 85)       # #334155 Slate 700
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B Slate 500
COLOR_CARD_BG = RGBColor(248, 250, 252)      # #F8FAFC Slate 50
COLOR_BORDER = RGBColor(226, 232, 240)       # #E2E8F0 Slate 200
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

DIR_PACKAGES = "packages"


def create_mckinsey_grid_image(lang='ES', out_path='temp_mckinsey_grid.png'):
    """
    Genera un Gráfico Cartesiano McKinsey / GE 3x3 de alta resolución para la diapositiva 1.
    Eje X: Fortaleza Competitiva (FC) [1.0 a 5.0] con umbrales en 2.33 y 3.67.
    Eje Y: Atractivo de la Industria (IA) [1.0 a 5.0] con umbrales en 2.33 y 3.67.
    Tamaño de burbuja: Proporcional a la Facturación Anual.
    """
    fig, ax = plt.subplots(figsize=(6.4, 5.2), dpi=220)

    # 1. Fondos de cuadrantes coloreados por zona estratégica
    # Fila Superior (Y: 3.67 - 5.0)
    # [Alto, Fuerte] X: 3.67 - 5.0 -> VERDE
    ax.fill_between([3.67, 5.0], 3.67, 5.0, color='#D1FAE5', alpha=0.85, zorder=1)
    # [Alto, Media] X: 2.33 - 3.67 -> VERDE
    ax.fill_between([2.33, 3.67], 3.67, 5.0, color='#D1FAE5', alpha=0.85, zorder=1)
    # [Alto, Débil] X: 1.0 - 2.33 -> ÁMBAR
    ax.fill_between([1.0, 2.33], 3.67, 5.0, color='#FEF3C7', alpha=0.85, zorder=1)

    # Fila Media (Y: 2.33 - 3.67)
    # [Medio, Fuerte] X: 3.67 - 5.0 -> VERDE
    ax.fill_between([3.67, 5.0], 2.33, 3.67, color='#D1FAE5', alpha=0.85, zorder=1)
    # [Medio, Media] X: 2.33 - 3.67 -> ÁMBAR
    ax.fill_between([2.33, 3.67], 2.33, 3.67, color='#FEF3C7', alpha=0.85, zorder=1)
    # [Medio, Débil] X: 1.0 - 2.33 -> ROJO
    ax.fill_between([1.0, 2.33], 2.33, 3.67, color='#FEE2E2', alpha=0.85, zorder=1)

    # Fila Inferior (Y: 1.0 - 2.33)
    # [Bajo, Fuerte] X: 3.67 - 5.0 -> ÁMBAR
    ax.fill_between([3.67, 5.0], 1.0, 2.33, color='#FEF3C7', alpha=0.85, zorder=1)
    # [Bajo, Media] X: 2.33 - 3.67 -> ROJO
    ax.fill_between([2.33, 3.67], 1.0, 2.33, color='#FEE2E2', alpha=0.85, zorder=1)
    # [Bajo, Débil] X: 1.0 - 2.33 -> ROJO
    ax.fill_between([1.0, 2.33], 1.0, 2.33, color='#FEE2E2', alpha=0.85, zorder=1)

    # 2. Líneas divisorias de cuadrantes (umbrales 2.33 y 3.67)
    for thresh in [2.33, 3.67]:
        ax.axvline(x=thresh, color='#94A3B8', linestyle='--', linewidth=1.2, zorder=2)
        ax.axhline(y=thresh, color='#94A3B8', linestyle='--', linewidth=1.2, zorder=2)

    # 3. Etiquetas de los 9 cuadrantes en esquinas
    labels_es = [
        (4.33, 4.80, "INVERTIR P/ LIDERAR", "#065F46"),
        (3.00, 4.80, "INVERTIR P/ DESARROLLAR", "#065F46"),
        (1.67, 4.80, "SELECTIVIDAD / DOBLAR O SALIR", "#92400E"),

        (4.33, 3.50, "CRECER SELECTIVAMENTE", "#065F46"),
        (3.00, 3.50, "SELECTIVIDAD / RENTABILIZAR", "#92400E"),
        (1.67, 3.50, "COSECHAR / REESTRUCTURAR", "#991B1B"),

        (4.33, 2.15, "PROTEGER Y COSECHAR", "#92400E"),
        (3.00, 2.15, "COSECHA CONTROLADA", "#991B1B"),
        (1.67, 2.15, "DESINVERTIR / LIQUIDAR", "#991B1B"),
    ]
    labels_en = [
        (4.33, 4.80, "INVEST TO LEAD", "#065F46"),
        (3.00, 4.80, "INVEST TO BUILD", "#065F46"),
        (1.67, 4.80, "SELECTIVITY / DOUBLE OR QUIT", "#92400E"),

        (4.33, 3.50, "SELECTIVITY / REINFORCE", "#065F46"),
        (3.00, 3.50, "SELECTIVITY / MAX RETURN", "#92400E"),
        (1.67, 3.50, "HARVEST / RESTRUCTURE", "#991B1B"),

        (4.33, 2.15, "PROTECT & HARVEST", "#92400E"),
        (3.00, 2.15, "CONTROLLED HARVEST", "#991B1B"),
        (1.67, 2.15, "DIVEST / DIVESTITURE", "#991B1B"),
    ]
    labels = labels_es if lang == 'ES' else labels_en

    for x_pos, y_pos, text, color in labels:
        ax.text(x_pos, y_pos, text, ha='center', va='top',
                fontsize=6.5, fontweight='bold', color=color, alpha=0.75, zorder=2)

    # 4. Datos de las 10 UENs
    # (code, name, x=Strength, y=Attractiveness, sales_M)
    uens = [
        ("UEN-01", "Cloud IA", 4.63, 4.64, 95.0, '#10B981'),
        ("UEN-02", "Robótica", 3.81, 4.61, 72.0, '#10B981'),
        ("UEN-03", "Electrónica", 4.20, 3.72, 110.0, '#10B981'),
        ("UEN-04", "Sensores", 3.49, 3.29, 68.0, '#F59E0B'),
        ("UEN-05", "Telemática", 2.72, 3.57, 35.0, '#F59E0B'),
        ("UEN-06", "HVAC Térmico", 4.09, 2.25, 42.0, '#F59E0B'),
        ("UEN-07", "Mecanizado", 1.98, 3.91, 25.0, '#F59E0B'),
        ("UEN-08", "Válvulas", 1.95, 2.64, 18.0, '#EF4444'),
        ("UEN-09", "Cableado", 2.52, 1.90, 12.0, '#EF4444'),
        ("UEN-10", "Medidores", 1.60, 1.57, 8.0, '#EF4444'),
    ]

    for code, sname, x_val, y_val, sales, b_col in uens:
        # Área de burbuja proporcional a ventas
        size = sales * 14 + 180
        ax.scatter(x_val, y_val, s=size, color=b_col, edgecolors='#0F172A',
                   linewidth=1.2, alpha=0.9, zorder=5)

        # Etiqueta
        ax.annotate(f"{code}\n({sales:.0f}M€)" if lang == 'ES' else f"{code}\n(${sales:.0f}M)",
                    (x_val, y_val), fontsize=7.2, fontweight='bold',
                    color='#0F172A', ha='center', va='center', zorder=6)

    # 5. Configuración de ejes y estética
    ax.set_xlim(1.0, 5.0)
    ax.set_ylim(1.0, 5.0)

    ax.set_xlabel("Fortaleza Competitiva de la UEN (Eje X)" if lang == 'ES' else "Business Unit Competitive Strength (X-Axis)",
                  fontsize=8.5, fontweight='bold', color='#1E293B', labelpad=6)
    ax.set_ylabel("Atractivo de la Industria (Eje Y)" if lang == 'ES' else "Industry Attractiveness (Y-Axis)",
                  fontsize=8.5, fontweight='bold', color='#1E293B', labelpad=6)

    ax.set_xticks([1.0, 2.33, 3.67, 5.0])
    ax.set_xticklabels(["1.0\n(Débil)" if lang == 'ES' else "1.0\n(Weak)",
                        "2.33\n(Medio)" if lang == 'ES' else "2.33\n(Medium)",
                        "3.67\n(Fuerte)" if lang == 'ES' else "3.67\n(Strong)",
                        "5.0\n(Líder)" if lang == 'ES' else "5.0\n(Leader)"],
                       fontsize=7.5, color='#475569')

    ax.set_yticks([1.0, 2.33, 3.67, 5.0])
    ax.set_yticklabels(["1.0 (Bajo)" if lang == 'ES' else "1.0 (Low)",
                        "2.33 (Medio)" if lang == 'ES' else "2.33 (Medium)",
                        "3.67 (Alto)" if lang == 'ES' else "3.67 (High)",
                        "5.0 (Máximo)" if lang == 'ES' else "5.0 (Peak)"],
                       fontsize=7.5, color='#475569')

    ax.grid(True, linestyle=':', alpha=0.4, color='#CBD5E1', zorder=2)
    for spine in ax.spines.values():
        spine.set_color('#94A3B8')
        spine.set_linewidth(1)

    plt.tight_layout()
    plt.savefig(out_path, dpi=220, bbox_inches='tight')
    plt.close()
    return out_path


def add_header_block(slide, category_text, action_title, subtitle):
    """Inserta la cabecera estándar con Pirámide de Minto y Action Title."""
    # Badge categoría
    badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_b = badge_box.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = category_text.upper()
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_BLUE_ACCENT

    # Action Title (Conclusión orientada)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(17)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    # Subtítulo explicativo
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.38), Inches(11.7), Inches(0.35))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(10)
    p_s.font.color.rgb = COLOR_TEXT_MUTED


# ==============================================================================
# SLIDE 1: PORTFOLIO OVERVIEW & 9-BOX GRID
# ==============================================================================
def build_slide1(prs, lang='ES'):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    cat_text = ("DATALARIA | EXECUTIVE DECISION PACK • GESTIÓN DE CARTERA C-LEVEL"
                if lang == 'ES' else
                "DATALARIA | EXECUTIVE DECISION PACK • C-SUITE PORTFOLIO STRATEGY")
    action_title = ("El 57% de las ventas y el 68% del CAPEX se concentran en tres unidades líderes en sectores de alta expansión"
                    if lang == 'ES' else
                    "57% of corporate revenue and 68% of CAPEX concentrate in three market leaders within high-growth sectors")
    subtitle = ("Diagnóstico integral de 10 Unidades Estratégicas de Negocio mediante la Matriz McKinsey / General Electric 3x3 multifactorial"
                if lang == 'ES' else
                "Comprehensive diagnostic of 10 Strategic Business Units via McKinsey / General Electric 3x3 multifactor matrix")

    add_header_block(slide, cat_text, action_title, subtitle)

    # 1. Gráfico McKinsey 3x3 en la mitad izquierda
    chart_path = f"temp_mckinsey_grid_{lang}.png"
    create_mckinsey_grid_image(lang=lang, out_path=chart_path)
    slide.shapes.add_picture(chart_path, Inches(0.8), Inches(1.8), width=Inches(6.2))

    # 2. Panel Derecho: 4 KPI Cards de Alto Impacto
    kpi_cards = [
        ("FACTURACIÓN TOTAL CARTERA" if lang == 'ES' else "TOTAL PORTFOLIO REVENUE",
         "485 M€" if lang == 'ES' else "$485 M",
         "10 UENs auditadas en 3 zonas" if lang == 'ES' else "10 SBUs audited across 3 zones",
         COLOR_NAVY_DARK),
        ("ZONA INVERTIR / CRECER (VERDE)" if lang == 'ES' else "INVEST / GROW ZONE (GREEN)",
         "277 M€ (57.1%)" if lang == 'ES' else "$277 M (57.1%)",
         "3 UENs líderes • 68% del CAPEX total" if lang == 'ES' else "3 market leaders • 68% of total CAPEX",
         COLOR_GREEN_BORDER),
        ("ZONA SELECTIVIDAD / PROTEGER (ÁMBAR)" if lang == 'ES' else "SELECTIVITY / HOLD ZONE (AMBER)",
         "170 M€ (35.1%)" if lang == 'ES' else "$170 M (35.1%)",
         "4 UENs rentables • Autofinanciación" if lang == 'ES' else "4 cash generators • Strict self-funding",
         COLOR_AMBER_BORDER),
        ("ZONA COSECHAR / DESINVERTIR (ROJO)" if lang == 'ES' else "HARVEST / DIVEST ZONE (RED)",
         "38 M€ (7.8%)" if lang == 'ES' else "$38 M (7.8%)",
         "3 UENs • Carve-out libera 24M€ caja" if lang == 'ES' else "3 SBUs • Carve-out unlocks $24M cash",
         COLOR_RED_BORDER),
    ]

    card_left = Inches(7.2)
    card_width = Inches(5.3)
    card_height = Inches(1.05)

    for idx, (title, value, meta, val_color) in enumerate(kpi_cards):
        top_pos = Inches(1.8 + idx * 1.15)
        # Fondo tarjeta
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, card_left, top_pos, card_width, card_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_BORDER
        shape.line.width = Pt(1)

        # Banda izquierda de color
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, card_left, top_pos, Inches(0.12), card_height)
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = val_color
        stripe.line.fill.background()

        # Texto dentro de la tarjeta
        tb = slide.shapes.add_textbox(card_left + Inches(0.25), top_pos + Inches(0.08), card_width - Inches(0.4), card_height - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_TEXT_MUTED

        p1 = tf.add_paragraph()
        p1.text = value
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = meta
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # Tarjeta de Síntesis Estratégica al pie del panel derecho
    syn_top = Inches(6.42)
    syn_height = Inches(0.7)
    syn_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, card_left, syn_top, card_width, syn_height)
    syn_shape.fill.solid()
    syn_shape.fill.fore_color.rgb = COLOR_BLUE_LIGHT
    syn_shape.line.color.rgb = COLOR_BLUE_ACCENT
    syn_shape.line.width = Pt(1)

    tb_syn = slide.shapes.add_textbox(card_left + Inches(0.15), syn_top + Inches(0.06), card_width - Inches(0.3), syn_height - Inches(0.12))
    tf_syn = tb_syn.text_frame
    tf_syn.word_wrap = True
    tf_syn.margin_left = tf_syn.margin_top = tf_syn.margin_right = tf_syn.margin_bottom = 0

    p_syn = tf_syn.paragraphs[0]
    p_syn.text = ("RECOMENDACIÓN MCKINSEY: Reasignar 51.0M€ de CAPEX hacia UEN-01/02/03 y ejecutar carve-out de UEN-08/09/10 para maximizar el ROIC corporativo (+380 bps)."
                  if lang == 'ES' else
                  "MCKINSEY MANDATE: Reallocate $51.0M CAPEX into SBUs 01/02/03 and execute carve-outs for SBUs 08/09/10 to maximize corporate ROIC (+380 bps).")
    p_syn.font.name = FONT_HEADING
    p_syn.font.size = Pt(8.5)
    p_syn.font.bold = True
    p_syn.font.color.rgb = COLOR_BLUE_ACCENT


# ==============================================================================
# SLIDE 2: STRATEGIC ZONE DIAGNOSTICS & RISK-RETURN PROFILING
# ==============================================================================
def build_slide2(prs, lang='ES'):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    cat_text = ("DATALARIA | EXECUTIVE DECISION PACK • DIAGNÓSTICO DE ZONAS ESTRATÉGICAS"
                if lang == 'ES' else
                "DATALARIA | EXECUTIVE DECISION PACK • STRATEGIC ZONE DIAGNOSTICS")
    action_title = ("Tres mandatos diferenciados: Crecimiento agresivo en Verde, autofinanciación en Ámbar y salida ordenada en Rojo"
                    if lang == 'ES' else
                    "Three distinct strategic mandates: Aggressive growth in Green, self-funding in Amber, and disciplined exit in Red")
    subtitle = ("Perfilado de riesgo-retorno, barreras estructurales y planes de maniobra operativa por zona de asignación de capital"
                if lang == 'ES' else
                "Risk-return profiling, structural barriers, and operational playbooks across capital allocation zones")

    add_header_block(slide, cat_text, action_title, subtitle)

    # 3 Paneles Columnas
    panel_width = Inches(3.75)
    panel_height = Inches(5.25)
    col_gap = Inches(0.23)
    start_left = Inches(0.8)
    top_pos = Inches(1.8)

    panels_es = [
        ("ZONA INVERTIR / CRECER",
         "CAPEX: 51.0 M€ (68.0%) • Mandato Expansión",
         COLOR_GREEN_BG, COLOR_GREEN_BORDER, COLOR_GREEN_TEXT,
         [
             ("UENs Posicionadas", "UEN-01 (Cloud IA), UEN-02 (Robótica Médica), UEN-03 (Electrónica de Potencia)."),
             ("Perfil Riesgo / Retorno", "Sectores con CAGR > 14% anual. Margen EBITDA medio 23.6%. Potencial de liderazgo global con escala."),
             ("Diagnóstico & Ventaja", "Barreras de entrada altas por propiedad intelectual, patentes de algoritmos y certificaciones regulatorias."),
             ("Barreras Operativas", "Escasez de talento especializado en IA/robótica y ciclos prolongados de homologación clínica/industrial."),
             ("Plan de Maniobra C-Level", "Aprobación de 51M€ de CAPEX a 36 meses. Búsqueda activa de adquisiciones bolt-on para integrar tecnología."),
         ]),
        ("ZONA SELECTIVIDAD / PROTEGER",
         "CAPEX: 20.2 M€ (26.9%) • Mandato Margen",
         COLOR_AMBER_BG, COLOR_AMBER_BORDER, COLOR_AMBER_TEXT,
         [
             ("UENs Posicionadas", "UEN-04 (Sensores IoT), UEN-05 (Telemática), UEN-06 (HVAC Térmico), UEN-07 (Mecanizado Aleaciones)."),
             ("Perfil Riesgo / Retorno", "Mercados maduros (CAGR 4-8%). Margen EBITDA 14.1%. Generación recurrente y predecible de caja libre."),
             ("Diagnóstico & Ventaja", "Base instalada fiel y alta capilaridad comercial. Riesgo de erosión paulatina por competidores de bajo coste."),
             ("Barreras Operativas", "Presión en precios en componentes estándar e inflación de materias primas (aluminio, cobre)."),
             ("Plan de Maniobra C-Level", "Autofinanciación estricta vía EBITDA propio. Migración hacia capas de software SaaS y aleaciones aeroespaciales."),
         ]),
        ("ZONA COSECHAR / DESINVERTIR",
         "CAPEX: 3.8 M€ (5.1%) • Mandato Salida",
         COLOR_RED_BG, COLOR_RED_BORDER, COLOR_RED_TEXT,
         [
             ("UENs Posicionadas", "UEN-08 (Válvulas Hidráulicas), UEN-09 (Cableado Estándar), UEN-10 (Medidores Analógicos)."),
             ("Perfil Riesgo / Retorno", "Destrucción activa de valor económico (ROIC 6.2% vs WACC 8.8%). Mercados en estancamiento secular o contracción."),
             ("Diagnóstico & Ventaja", "Comoditización extrema. Ausencia de economías de escala frente a fabricantes asiáticos de gran volumen."),
             ("Barreras Operativas", "Complejidad laboral y compromisos de suministro residual con clientes históricos."),
             ("Plan de Maniobra C-Level", "Congelación total de CAPEX no legal. Contratación de banco de inversión para carve-out en Q3-Q4 (libera 24M€)."),
         ]),
    ]

    panels_en = [
        ("INVEST / GROW ZONE",
         "CAPEX: $51.0M (68.0%) • Expansion Mandate",
         COLOR_GREEN_BG, COLOR_GREEN_BORDER, COLOR_GREEN_TEXT,
         [
             ("Positioned SBUs", "UEN-01 (Cloud AI), UEN-02 (Medical Robotics), UEN-03 (Power Electronics)."),
             ("Risk-Return Profile", "Addressable CAGR > 14%. Avg EBITDA margin 23.6%. Global leadership potential backed by scale economies."),
             ("Diagnostic & Edge", "High entry barriers driven by algorithmic IP, proprietary patents, and stringent regulatory moats."),
             ("Execution Hurdles", "Acute shortage of specialized AI engineers and long FDA/CE certification lead times."),
             ("C-Suite Playbook", "Board authorization of $51M 36-month CAPEX pool. Aggressive pursuit of strategic bolt-on acquisitions."),
         ]),
        ("SELECTIVITY / HOLD ZONE",
         "CAPEX: $20.2M (26.9%) • Margin Mandate",
         COLOR_AMBER_BG, COLOR_AMBER_BORDER, COLOR_AMBER_TEXT,
         [
             ("Positioned SBUs", "UEN-04 (Smart Sensors), UEN-05 (Fleet Telematics), UEN-06 (HVAC Thermal), UEN-07 (Precision Alloys)."),
             ("Risk-Return Profile", "Mature sectors (CAGR 4-8%). Avg EBITDA margin 14.1%. Predictable, highly stable free cash flow generators."),
             ("Diagnostic & Edge", "Entrenched customer accounts and deep distribution. Risk of gradual commoditization by low-cost rivals."),
             ("Execution Hurdles", "Price erosion in standard hardware and raw material inflation (copper, specialized resins)."),
             ("C-Suite Playbook", "Strict self-funding through divisional EBITDA. Pivot toward recurring SaaS software and niche aerospace alloys."),
         ]),
        ("HARVEST / DIVEST ZONE",
         "CAPEX: $3.8M (5.1%) • Exit Mandate",
         COLOR_RED_BG, COLOR_RED_BORDER, COLOR_RED_TEXT,
         [
             ("Positioned SBUs", "UEN-08 (Hydraulic Valves), UEN-09 (Commodity Wiring), UEN-10 (Analog Meters)."),
             ("Risk-Return Profile", "Systematic value destruction (Avg ROIC 6.2% vs WACC 8.8%). Stagnant or contracting addressable demand."),
             ("Diagnostic & Edge", "Complete commoditization. Structural scale deficit against low-cost high-volume Asian manufacturers."),
             ("Execution Hurdles", "Labor severance liabilities and residual supply obligations with legacy industrial OEM accounts."),
             ("C-Suite Playbook", "Total freeze on discretionary CAPEX. Retain boutique investment bank for M&A carve-out (unlocks $24M cash)."),
         ]),
    ]

    panels = panels_es if lang == 'ES' else panels_en

    for idx, (p_title, p_badge, bg_col, bdr_col, txt_col, sections) in enumerate(panels):
        left_pos = start_left + idx * (panel_width + col_gap)

        # Marco exterior del panel
        panel_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, panel_width, panel_height)
        panel_box.fill.solid()
        panel_box.fill.fore_color.rgb = COLOR_WHITE
        panel_box.line.color.rgb = bdr_col
        panel_box.line.width = Pt(1.5)

        # Header del panel
        hdr_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, top_pos, panel_width, Inches(0.8))
        hdr_box.fill.solid()
        hdr_box.fill.fore_color.rgb = bg_col
        hdr_box.line.fill.background()

        tb_h = slide.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.1), panel_width - Inches(0.3), Inches(0.65))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0

        p_ht = tf_h.paragraphs[0]
        p_ht.text = p_title
        p_ht.font.name = FONT_HEADING
        p_ht.font.size = Pt(11)
        p_ht.font.bold = True
        p_ht.font.color.rgb = txt_col

        p_hb = tf_h.add_paragraph()
        p_hb.text = p_badge
        p_hb.font.name = FONT_HEADING
        p_hb.font.size = Pt(8.5)
        p_hb.font.bold = True
        p_hb.font.color.rgb = txt_col

        # Cuerpo del panel (5 secciones de análisis)
        content_top = top_pos + Inches(0.9)
        tb_c = slide.shapes.add_textbox(left_pos + Inches(0.2), content_top, panel_width - Inches(0.4), panel_height - Inches(1.05))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

        for s_idx, (sec_title, sec_desc) in enumerate(sections):
            p_st = tf_c.add_paragraph() if s_idx > 0 else tf_c.paragraphs[0]
            p_st.text = sec_title.upper()
            p_st.font.name = FONT_HEADING
            p_st.font.size = Pt(8)
            p_st.font.bold = True
            p_st.font.color.rgb = COLOR_NAVY_DARK
            p_st.space_before = Pt(6) if s_idx > 0 else Pt(0)

            p_sd = tf_c.add_paragraph()
            p_sd.text = sec_desc
            p_sd.font.name = FONT_BODY
            p_sd.font.size = Pt(8.2)
            p_sd.font.color.rgb = COLOR_TEXT_MAIN
            p_sd.space_after = Pt(2)


# ==============================================================================
# SLIDE 3: BOARD DECISION GATEWAY & CAPITAL ALLOCATION MANDATE
# ==============================================================================
def build_slide3(prs, lang='ES'):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    cat_text = ("DATALARIA | EXECUTIVE DECISION PACK • GOBERNANZA & ACUERDOS DEL CONSEJO"
                if lang == 'ES' else
                "DATALARIA | EXECUTIVE DECISION PACK • BOARD GOVERNANCE & CAPITAL MANDATE")
    action_title = ("El Comité de Inversión somete a aprobación del Consejo un plan de CAPEX de 75.0M€ y 3 mandatos de salida"
                    if lang == 'ES' else
                    "The Investment Committee submits a $75.0M CAPEX plan and 3 divestment mandates for Board approval")
    subtitle = ("Resoluciones formales vinculantes, umbrales de TIR exigida y desbloqueo de liquidez patrimonial para el ejercicio 2026-2029"
                if lang == 'ES' else
                "Binding governance resolutions, hurdle rates (IRR), and equity value release roadmap for the 2026-2029 cycle")

    add_header_block(slide, cat_text, action_title, subtitle)

    # 1. Tabla Ejecutiva Superior de Asignación (10 UENs resumidas en 6 filas clave)
    table_left = Inches(0.8)
    table_top = Inches(1.85)
    table_width = Inches(11.7)
    table_height = Inches(2.3)

    table_shape = slide.shapes.add_table(7, 7, table_left, table_top, table_width, table_height)
    table = table_shape.table

    # Anchos de columnas
    table.columns[0].width = Inches(1.1)  # Cód
    table.columns[1].width = Inches(2.7)  # Nombre
    table.columns[2].width = Inches(1.8)  # Zona
    table.columns[3].width = Inches(1.4)  # Ventas
    table.columns[4].width = Inches(1.4)  # CAPEX 3A
    table.columns[5].width = Inches(1.3)  # TIR Mínima
    table.columns[6].width = Inches(2.0)  # Dictamen

    headers = [
        "CÓDIGO" if lang == 'ES' else "CODE",
        "UNIDAD ESTRATÉGICA (UEN)" if lang == 'ES' else "STRATEGIC SBU",
        "ZONA MCKINSEY" if lang == 'ES' else "MCKINSEY ZONE",
        "VENTAS 2026" if lang == 'ES' else "2026 SALES",
        "CAPEX 36M" if lang == 'ES' else "36M CAPEX",
        "TIR MÍNIMA" if lang == 'ES' else "HURDLE RATE",
        "DICTAMEN FORMAL" if lang == 'ES' else "BOARD MANDATE",
    ]
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_HEADING
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    rows_data_es = [
        ("UEN-01/02", "Cloud IA & Robótica Médica", "Invertir / Crecer", "167.0 M€", "38.5 M€", "18.0%", "Aprobado Vinculante"),
        ("UEN-03", "Electrónica de Potencia", "Invertir / Crecer", "110.0 M€", "12.5 M€", "18.0%", "Aprobado Vinculante"),
        ("UEN-04/05", "Sensores IoT & Telemática Flotas", "Seleccionar / Proteger", "103.0 M€", "12.8 M€", "14.0%", "Aprobado Condicionado"),
        ("UEN-06/07", "HVAC Térmico & Aleaciones", "Seleccionar / Proteger", "67.0 M€", "7.4 M€", "14.0%", "Aprobado Condicionado"),
        ("UEN-08/09", "Válvulas Hidráulicas & Cableado", "Cosechar / Desinvertir", "30.0 M€", "2.0 M€", "10.0%", "Carve-Out Q4 / Subasta"),
        ("UEN-10", "Medidores Analógicos", "Cosechar / Desinvertir", "8.0 M€", "0.2 M€", "10.0%", "Liquidación Ordenada"),
    ]
    rows_data_en = [
        ("UEN-01/02", "Industrial AI & Medical Robotics", "Invest / Grow", "$167.0 M", "$38.5 M", "18.0%", "Binding Approval"),
        ("UEN-03", "Power Electronics & Inverters", "Invest / Grow", "$110.0 M", "$12.5 M", "18.0%", "Binding Approval"),
        ("UEN-04/05", "Smart Sensors & Fleet IoT", "Selectivity / Hold", "$103.0 M", "$12.8 M", "14.0%", "Conditional Approval"),
        ("UEN-06/07", "Thermal HVAC & Precision Alloys", "Selectivity / Hold", "$67.0 M", "$7.4 M", "14.0%", "Conditional Approval"),
        ("UEN-08/09", "Hydraulic Valves & Wiring", "Harvest / Divest", "$30.0 M", "$2.0 M", "10.0%", "Carve-Out Q4 / Auction"),
        ("UEN-10", "Analog Legacy Meters", "Harvest / Divest", "$8.0 M", "$0.2 M", "10.0%", "Orderly Liquidation"),
    ]
    rows_data = rows_data_es if lang == 'ES' else rows_data_en

    for r_idx, row_vals in enumerate(rows_data):
        for c_idx, val in enumerate(row_vals):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_NAVY_DARK

            # Colores y alineación
            if c_idx in [0, 2, 5]:
                p.alignment = PP_ALIGN.CENTER
            elif c_idx in [3, 4]:
                p.alignment = PP_ALIGN.RIGHT
                p.font.bold = True
            elif c_idx == 6:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True

            # Sombrado de fondo alternado
            cell.fill.solid()
            if r_idx % 2 == 0:
                cell.fill.fore_color.rgb = COLOR_CARD_BG
            else:
                cell.fill.fore_color.rgb = COLOR_WHITE

    # 2. Panel Inferior Izquierdo: 3 Resoluciones Formales del Consejo
    res_left = Inches(0.8)
    res_top = Inches(4.35)
    res_width = Inches(7.5)
    res_height = Inches(2.7)

    res_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, res_left, res_top, res_width, res_height)
    res_box.fill.solid()
    res_box.fill.fore_color.rgb = COLOR_CARD_BG
    res_box.line.color.rgb = COLOR_BORDER
    res_box.line.width = Pt(1)

    tb_res = slide.shapes.add_textbox(res_left + Inches(0.2), res_top + Inches(0.12), res_width - Inches(0.4), res_height - Inches(0.24))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True
    tf_res.margin_left = tf_res.margin_top = tf_res.margin_right = tf_res.margin_bottom = 0

    p_rt = tf_res.paragraphs[0]
    p_rt.text = ("RESOLUCIONES FORMALES SOMETIDAS A VOTACIÓN DEL CONSEJO"
                 if lang == 'ES' else
                 "FORMAL RESOLUTIONS SUBMITTED FOR BOARD VOTING")
    p_rt.font.name = FONT_HEADING
    p_rt.font.size = Pt(10)
    p_rt.font.bold = True
    p_rt.font.color.rgb = COLOR_NAVY_DARK
    p_rt.space_after = Pt(4)

    resolutions_es = [
        ("RESOLUCIÓN 1 (EXPANSIÓN DE LIDERAZGO):",
         "Aprobar la asignación vinculante e irrevocable de 51.0M€ de CAPEX para UEN-01 (Cloud IA), UEN-02 (Robótica) y UEN-03 (Electrónica), condicionada a una TIR mínima del 18.0%."),
        ("RESOLUCIÓN 2 (DISCIPLINA EN SELECTIVIDAD):",
         "Condicionar los 20.2M€ asignados a la Zona Ámbar a la estricta autofinanciación con EBITDA interno, bloqueando transferencias cruzadas de caja desde las UENs líderes."),
        ("RESOLUCIÓN 3 (MANDATO DE CARVE-OUT Y VENTA):",
         "Otorgar mandato formal a la Dirección Ejecutiva y CFO para retener asesoría M&A y ejecutar el carve-out de UEN-08 y UEN-09 antes de Q4 2026, liberando 24M€ de capital atrapado."),
    ]
    resolutions_en = [
        ("RESOLUTION 1 (LEADERSHIP EXPANSION):",
         "Authorize the binding, irrevocable allocation of $51.0M CAPEX for SBUs 01 (Cloud AI), 02 (Robotics), and 03 (Power Electronics), tied to an 18.0% minimum Hurdle Rate (IRR)."),
        ("RESOLUTION 2 (SELECTIVITY DISCIPLINE):",
         "Condition the $20.2M allocated to the Amber Zone on strict divisional self-funding via internal EBITDA, prohibiting cross-subsidization from core growth leaders."),
        ("RESOLUTION 3 (CARVE-OUT & DIVESTMENT MANDATE):",
         "Authorize the Executive Committee and CFO to engage boutique M&A advisory to complete the carve-out of SBUs 08 and 09 before Q4 2026, unlocking $24M in trapped capital."),
    ]
    resolutions = resolutions_es if lang == 'ES' else resolutions_en

    for r_title, r_desc in resolutions:
        p_t = tf_res.add_paragraph()
        p_t.text = r_title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(8.5)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_BLUE_ACCENT
        p_t.space_before = Pt(4)

        p_d = tf_res.add_paragraph()
        p_d.text = r_desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(8.2)
        p_d.font.color.rgb = COLOR_TEXT_MAIN

    # 3. Panel Inferior Derecho: Bloque de Firmas y Gobernanza
    sign_left = Inches(8.5)
    sign_top = Inches(4.35)
    sign_width = Inches(4.0)
    sign_height = Inches(2.7)

    sign_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, sign_left, sign_top, sign_width, sign_height)
    sign_box.fill.solid()
    sign_box.fill.fore_color.rgb = COLOR_WHITE
    sign_box.line.color.rgb = COLOR_NAVY_DARK
    sign_box.line.width = Pt(1.5)

    tb_sig = slide.shapes.add_textbox(sign_left + Inches(0.2), sign_top + Inches(0.12), sign_width - Inches(0.4), sign_height - Inches(0.24))
    tf_sig = tb_sig.text_frame
    tf_sig.word_wrap = True
    tf_sig.margin_left = tf_sig.margin_top = tf_sig.margin_right = tf_sig.margin_bottom = 0

    p_st = tf_sig.paragraphs[0]
    p_st.text = ("GOBERNANZA & PROTOCOLO DE FIRMA" if lang == 'ES' else "GOVERNANCE & SIGN-OFF PROTOCOL")
    p_st.font.name = FONT_HEADING
    p_st.font.size = Pt(10)
    p_st.font.bold = True
    p_st.font.color.rgb = COLOR_NAVY_DARK
    p_st.alignment = PP_ALIGN.CENTER
    p_st.space_after = Pt(6)

    officers_es = [
        ("Presidente del Consejo de Administración", "[ APROBADO UNÁNIME ]"),
        ("Consejero Delegado (CEO)", "[ CONFORME A MANDATO ]"),
        ("Director Financiero (CFO)", "[ CERTIFICACIÓN FINANCIERA ]"),
        ("Director de Estrategia Corporativa", "[ DICTAMEN MATRIZ MCKINSEY ]"),
    ]
    officers_en = [
        ("Chairman of the Board of Directors", "[ UNANIMOUSLY APPROVED ]"),
        ("Chief Executive Officer (CEO)", "[ STRATEGY COMPLIANT ]"),
        ("Chief Financial Officer (CFO)", "[ FINANCIALLY CERTIFIED ]"),
        ("Chief Strategy Officer (CSO)", "[ MCKINSEY FRAMEWORK AUDITED ]"),
    ]
    officers = officers_es if lang == 'ES' else officers_en

    for role, stamp in officers:
        p_r = tf_sig.add_paragraph()
        p_r.text = f"• {role}:"
        p_r.font.name = FONT_HEADING
        p_r.font.size = Pt(7.8)
        p_r.font.bold = True
        p_r.font.color.rgb = COLOR_NAVY_MED
        p_r.space_before = Pt(3)

        p_s = tf_sig.add_paragraph()
        p_s.text = f"   {stamp} — 2026-10-27"
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(7.5)
        p_s.font.color.rgb = COLOR_TEXT_MUTED


def generate_presentation(lang='ES', out_path=None):
    if out_path is None:
        fname = "ES_Matriz_McKinsey_GE_Presentacion.pptx" if lang == 'ES' else "EN_McKinsey_GE_Matrix_Presentation.pptx"
        out_path = os.path.join(DIR_PACKAGES, fname)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide1(prs, lang=lang)
    build_slide2(prs, lang=lang)
    build_slide3(prs, lang=lang)

    prs.save(out_path)
    print(f"[OK] Presentación PPTX generada con éxito ({lang}): {out_path}")
    return out_path


def main():
    print("Iniciando construcción de presentaciones PPTX 16:9 McKinsey / GE...")
    es_path = generate_presentation(lang='ES')
    en_path = generate_presentation(lang='EN')

    dir_es = os.path.join(DIR_PACKAGES, "[ES]_Matriz_McKinsey_GE")
    dir_en = os.path.join(DIR_PACKAGES, "[EN]_McKinsey_GE_Matrix")
    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    generate_presentation(lang='ES', out_path=os.path.join(dir_es, "ES_Matriz_McKinsey_GE_Presentacion.pptx"))
    generate_presentation(lang='EN', out_path=os.path.join(dir_en, "EN_McKinsey_GE_Matrix_Presentation.pptx"))

    # Limpiar archivos temporales de gráficos
    for f in ["temp_mckinsey_grid_ES.png", "temp_mckinsey_grid_EN.png"]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass

    print("Presentaciones completadas exitosamente.")


if __name__ == "__main__":
    main()
