#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/[ES]_PESTEL_Cuantitativo/Presentacion_PESTEL_CLevel_ES.pptx
2. packages/[EN]_Quantitative_PESTEL/Deck_PESTEL_CLevel_EN.pptx

Características de diseño Tier-1 (McKinsey / BCG):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Pirámide de Minto y Action Titles contundentes.
- Gráfico Radar hexagonal generado en alta resolución e integrado en Slide 2.
- Gateway de Decisión del Comité de Dirección destacado en Slide 3.
- Márgenes interiores estrictos, jerarquía tipográfica sin desbordes.
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
COLOR_BLUE_BG = RGBColor(239, 246, 255)      # #EFF6FF Blue 50
COLOR_BLUE_BORDER = RGBColor(147, 197, 253)  # #93C5FD Blue 300
COLOR_BLUE_TEXT = RGBColor(29, 78, 216)      # #1D4ED8 Blue 700

COLOR_TEAL_ACCENT = RGBColor(13, 148, 136)   # #0D9488 Teal 600
COLOR_TEAL_BG = RGBColor(240, 253, 250)      # #F0FDFA Teal 50
COLOR_TEAL_BORDER = RGBColor(153, 246, 228)  # #99F6E4 Teal 200
COLOR_TEAL_TEXT = RGBColor(15, 118, 110)     # #0F766E Teal 700

COLOR_AMBER_ACCENT = RGBColor(217, 119, 6)   # #D97706 Amber 600
COLOR_AMBER_BG = RGBColor(255, 251, 235)     # #FFFBEB Amber 50
COLOR_AMBER_BORDER = RGBColor(253, 230, 138) # #FDE68A Amber 200
COLOR_AMBER_TEXT = RGBColor(146, 64, 14)     # #92400E Amber 800

COLOR_ROSE_ACCENT = RGBColor(225, 29, 72)    # #E11D48 Rose 600
COLOR_ROSE_BG = RGBColor(255, 241, 242)      # #FFF1F2 Rose 50
COLOR_ROSE_BORDER = RGBColor(254, 205, 211)  # #FECDD3 Rose 200
COLOR_ROSE_TEXT = RGBColor(159, 18, 57)      # #9F1239 Rose 800

COLOR_EMERALD_ACCENT = RGBColor(5, 150, 105) # #059669 Emerald 600
COLOR_EMERALD_BG = RGBColor(236, 253, 245)   # #ECFDF5 Emerald 50
COLOR_EMERALD_BORDER = RGBColor(167, 243, 208)
COLOR_EMERALD_TEXT = RGBColor(6, 95, 70)

COLOR_GOLD = RGBColor(245, 158, 11)          # #F59E0B Gold
COLOR_TEXT_MAIN = RGBColor(51, 65, 85)       # #334155 Slate 700
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B Slate 500
COLOR_CARD_BG = RGBColor(248, 250, 252)      # #F8FAFC Slate 50
COLOR_BORDER = RGBColor(226, 232, 240)       # #E2E8F0 Slate 200
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"


def create_radar_image(lang='ES', out_path='temp_radar.png'):
    """Genera un gráfico radar hexagonal de alta resolución para la slide 2."""
    if lang == 'ES':
        categories = ['1. Político', '2. Económico', '3. Social', '4. Tecnológico', '5. Ecológico', '6. Legal']
    else:
        categories = ['1. Political', '2. Economic', '3. Social', '4. Technological', '5. Environmental', '6. Legal']

    N = len(categories)
    # Valores cuantitativos de la evaluación canónica PESTEL
    values = [3.82, 4.10, 3.12, 4.41, 3.52, 4.15]
    values += values[:1]

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.6, 5.0), subplot_kw=dict(polar=True), dpi=220)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories, color='#0F172A', size=9.5, weight='bold', fontfamily='sans-serif')
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ['1.0', '2.0', '3.0', '4.0', '5.0'], color='#64748B', size=8, fontfamily='sans-serif')
    plt.ylim(0, 5.2)

    # Cuadrícula y polígono de datos
    ax.grid(color='#CBD5E1', linestyle='--', linewidth=0.8)
    ax.spines['polar'].set_color('#94A3B8')

    ax.plot(angles, values, color='#2563EB', linewidth=2.8, linestyle='solid', label='Perfil PESTEL' if lang == 'ES' else 'PESTEL Profile')
    ax.fill(angles, values, color='#2563EB', alpha=0.22)
    ax.scatter(angles[:-1], values[:-1], color='#0F172A', s=55, zorder=5, edgecolors='#FFFFFF', linewidths=1.5)

    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', transparent=False, facecolor='#FFFFFF')
    plt.close()
    return out_path


def add_header_banner(slide, kicker_text, badge_text, action_title, sub_text, badge_color=COLOR_BLUE_ACCENT):
    """Genera la cabecera corporativa estándar Minto de Datalaria."""
    kicker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8.5), Inches(0.3))
    tf_k = kicker_box.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = kicker_text
    p_k.font.name = FONT_HEADING
    p_k.font.size = Pt(8.5)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_TEXT_MUTED

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.6), Inches(0.35), Inches(2.933), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = badge_color
    badge.line.color.rgb = badge_color
    tf_b = badge.text_frame
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = badge_text
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_WHITE
    p_b.alignment = PP_ALIGN.CENTER

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(19)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.3))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = sub_text
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(10)
    p_s.font.color.rgb = COLOR_TEXT_MUTED


def add_footer(slide, cur_page, total_pages=3, lang='ES'):
    """Genera el pie de página formal confidencial."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BORDER
    line.line.color.rgb = COLOR_BORDER

    conf_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(8.5), Inches(0.3))
    tf_c = conf_box.text_frame
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = "Datalaria.com | Executive Decision Pack • Documento Confidencial para Consejo de Administración" if lang == 'ES' else "Datalaria.com | Executive Decision Pack • Confidential Board of Directors Document"
    p_c.font.name = FONT_BODY
    p_c.font.size = Pt(8.5)
    p_c.font.color.rgb = COLOR_TEXT_MUTED

    num_box = slide.shapes.add_textbox(Inches(9.533), Inches(7.12), Inches(3.0), Inches(0.3))
    tf_n = num_box.text_frame
    tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
    p_n = tf_n.paragraphs[0]
    p_n.text = f"Página {cur_page} de {total_pages}" if lang == 'ES' else f"Page {cur_page} of {total_pages}"
    p_n.font.name = FONT_BODY
    p_n.font.size = Pt(8.5)
    p_n.font.color.rgb = COLOR_TEXT_MUTED
    p_n.alignment = PP_ALIGN.RIGHT


# ==============================================================================
# SLIDE 1: SÍNTESIS EJECUTIVA & 4 TARJETAS DE IMPACTO
# ==============================================================================
def build_slide1(prs, lang='ES'):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    kicker = "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD"
    badge = "DIAGNÓSTICO MACRO C-LEVEL" if lang == 'ES' else "C-SUITE MACRO DIAGNOSIS"
    title = ("La confluencia de volatilidad regulatoria (AI Act) e inflación energética exige un plan de contingencia de 715.000 € para blindar el EBITDA en 2026"
             if lang == 'ES' else
             "The confluence of regulatory volatility (EU AI Act) and energy cost spikes demands a $715,000 contingency plan to shield 2026 EBITDA")
    sub = ("Diagnóstico cuantitativo bidimensional (Severidad vs. Volatilidad), dimensiones críticas y plan de resiliencia ejecutiva."
           if lang == 'ES' else
           "2D quantitative macro diagnosis (Severity vs. Volatility), peak critical dimensions, and executive resilience roadmap.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_NAVY_DARK)

    # 4 Tarjetas de Impacto alineadas
    cards_data = [
        {
            'tag': "RIESGO MACRO COMPUESTO" if lang == 'ES' else "COMPOSITE MACRO RISK",
            'metric': "3.82 / 5.0",
            'submetric': "Exposición Crítica a Shocks" if lang == 'ES' else "Critical Shock Exposure",
            'bullets': [
                "24 factores macro auditados en 6 áreas" if lang == 'ES' else "24 macro factors audited across 6 pillars",
                "Índice ponderado en zona de alta hostilidad" if lang == 'ES' else "Weighted index in elevated risk territory",
                "Resiliencia interna de absorción: 1.18 / 4.0" if lang == 'ES' else "Internal shock absorption: 1.18 / 4.0"
            ],
            'pill': "ALERTA DIRECTIVA" if lang == 'ES' else "BOARD ALERT",
            'color_theme': COLOR_ROSE_ACCENT,
            'bg_color': COLOR_ROSE_BG,
            'border_color': COLOR_ROSE_BORDER,
            'text_color': COLOR_ROSE_TEXT
        },
        {
            'tag': "DIMENSIÓN DESESTABILIZADORA" if lang == 'ES' else "PEAK CRITICAL DIMENSION",
            'metric': "Tecnología (4.41)" if lang == 'ES' else "Tech (4.41)",
            'submetric': "Disrupción IA & Ciberriesgo" if lang == 'ES' else "AI Disruption & Cyber Risk",
            'bullets': [
                "IA Generativa con severidad máxima 4.6" if lang == 'ES' else "Generative AI at maximum severity 4.6",
                "Ciberamenazas OT con volatilidad 4.2" if lang == 'ES' else "OT cyberattacks with volatility 4.2",
                "Dimensión Legal en paridad crítica (4.15)" if lang == 'ES' else "Legal dimension in critical parity (4.15)"
            ],
            'pill': "FOCO INMEDIATO" if lang == 'ES' else "IMMEDIATE FOCUS",
            'color_theme': COLOR_AMBER_ACCENT,
            'bg_color': COLOR_AMBER_BG,
            'border_color': COLOR_AMBER_BORDER,
            'text_color': COLOR_AMBER_TEXT
        },
        {
            'tag': "ESTRATEGIA DE BLINDAJE" if lang == 'ES' else "RESILIENCE STRATEGY",
            'metric': "8 Iniciativas" if lang == 'ES' else "8 Initiatives",
            'submetric': "Hedging, IA Act & Nearshoring" if lang == 'ES' else "Hedging, AI Act & Nearshore",
            'bullets': [
                "Contratos PPA de energía al 70% fijo" if lang == 'ES' else "Corporate PPA contracts hedging 70% power",
                "Gobernanza AI Act (ISO 42001) certificada" if lang == 'ES' else "ISO 42001 AI Act compliance certification",
                "Planta en Europa del Este para aranceles" if lang == 'ES' else "Nearshoring assembly hub in Eastern Europe"
            ],
            'pill': "COBERTURA ACTIVA" if lang == 'ES' else "ACTIVE HEDGING",
            'color_theme': COLOR_BLUE_ACCENT,
            'bg_color': COLOR_BLUE_BG,
            'border_color': COLOR_BLUE_BORDER,
            'text_color': COLOR_BLUE_TEXT
        },
        {
            'tag': "PRESUPUESTO & RETORNO" if lang == 'ES' else "BUDGET & RETURN",
            'metric': "715.000 €" if lang == 'ES' else "$715,000",
            'submetric': "CAPEX 485k€ | OPEX 230k€" if lang == 'ES' else "CAPEX $485k | OPEX $230k",
            'bullets': [
                "Preserva 1.85 M€ de EBITDA en 2026" if lang == 'ES' else "Preserves $1.85M EBITDA in 2026",
                "Ratio Retorno de Resiliencia: 2.6x" if lang == 'ES' else "Resilience Return Ratio: 2.6x",
                "Payback de contingencia < 15 meses" if lang == 'ES' else "Contingency payback < 15 months"
            ],
            'pill': "ROI ACREDITADO" if lang == 'ES' else "PROVEN ROI",
            'color_theme': COLOR_EMERALD_ACCENT,
            'bg_color': COLOR_EMERALD_BG,
            'border_color': COLOR_EMERALD_BORDER,
            'text_color': COLOR_EMERALD_TEXT
        }
    ]

    card_w = Inches(2.78)
    card_h = Inches(5.15)
    start_x = Inches(0.8)
    gap_x = Inches(0.2)
    start_y = Inches(1.65)

    for i, card in enumerate(cards_data):
        curr_x = start_x + i * (card_w + gap_x)

        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, start_y, card_w, card_h)
        box.fill.solid()
        box.fill.fore_color.rgb = card['bg_color']
        box.line.color.rgb = card['border_color']
        box.line.width = Pt(1.5)

        # Header Pill
        p_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x + Inches(0.18), start_y + Inches(0.2), card_w - Inches(0.36), Inches(0.36))
        p_shape.fill.solid()
        p_shape.fill.fore_color.rgb = card['color_theme']
        p_shape.line.fill.background()
        tf_p = p_shape.text_frame
        tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        p = tf_p.paragraphs[0]
        p.text = card['tag']
        p.font.name = FONT_HEADING
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        # Métrica Principal
        m_box = slide.shapes.add_textbox(curr_x + Inches(0.15), start_y + Inches(0.68), card_w - Inches(0.3), Inches(0.55))
        tf_m = m_box.text_frame
        tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
        p_m = tf_m.paragraphs[0]
        p_m.text = card['metric']
        p_m.font.name = FONT_HEADING
        p_m.font.size = Pt(23)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_NAVY_DARK
        p_m.alignment = PP_ALIGN.CENTER

        # Submétrica
        s_box = slide.shapes.add_textbox(curr_x + Inches(0.15), start_y + Inches(1.28), card_w - Inches(0.3), Inches(0.35))
        tf_sub = s_box.text_frame
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
        p_s = tf_sub.paragraphs[0]
        p_s.text = card['submetric']
        p_s.font.name = FONT_HEADING
        p_s.font.size = Pt(9.5)
        p_s.font.bold = True
        p_s.font.color.rgb = card['text_color']
        p_s.alignment = PP_ALIGN.CENTER

        # Línea divisoria
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, curr_x + Inches(0.2), start_y + Inches(1.72), card_w - Inches(0.4), Inches(0.015))
        div.fill.solid()
        div.fill.fore_color.rgb = card['border_color']
        div.line.fill.background()

        # Viñetas
        b_box = slide.shapes.add_textbox(curr_x + Inches(0.18), start_y + Inches(1.85), card_w - Inches(0.36), Inches(2.5))
        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = Inches(0.05)
        tf_b.margin_right = Inches(0.05)
        tf_b.margin_top = Inches(0.05)
        tf_b.margin_bottom = Inches(0.05)

        for b_idx, bullet in enumerate(card['bullets']):
            p_bullet = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p_bullet.text = f"•  {bullet}"
            p_bullet.font.name = FONT_BODY
            p_bullet.font.size = Pt(9.5)
            p_bullet.font.color.rgb = COLOR_TEXT_MAIN
            p_bullet.space_after = Pt(10)

        # Píldora inferior
        bot_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x + Inches(0.25), start_y + card_h - Inches(0.55), card_w - Inches(0.5), Inches(0.35))
        bot_pill.fill.solid()
        bot_pill.fill.fore_color.rgb = COLOR_WHITE
        bot_pill.line.color.rgb = card['color_theme']
        bot_pill.line.width = Pt(1.2)
        tf_bp = bot_pill.text_frame
        tf_bp.margin_left = tf_bp.margin_right = tf_bp.margin_top = tf_bp.margin_bottom = 0
        p_bp = tf_bp.paragraphs[0]
        p_bp.text = card['pill']
        p_bp.font.name = FONT_HEADING
        p_bp.font.size = Pt(8.5)
        p_bp.font.bold = True
        p_bp.font.color.rgb = card['text_color']
        p_bp.alignment = PP_ALIGN.CENTER

    add_footer(slide, 1, 3, lang=lang)


# ==============================================================================
# SLIDE 2: EVIDENCIA CUANTITATIVA & RADAR 6 DIMENSIONES
# ==============================================================================
def build_slide2(prs, lang='ES'):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    kicker = "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD"
    badge = "EVIDENCIA CUANTITATIVA & RADAR" if lang == 'ES' else "QUANTITATIVE EVIDENCE & RADAR"
    title = ("La evaluación de 24 factores macro revela una asimetría crítica: el 42% del riesgo se concentra en shocks tecnológicos y regulatorios"
             if lang == 'ES' else
             "The assessment of 24 macro factors reveals a critical asymmetry: 42% of risk is concentrated in tech and regulatory shocks")
    sub = ("Desglose analítico de las 6 dimensiones PESTEL, perfil de severidad vs. volatilidad y horizonte temporal de impacto."
           if lang == 'ES' else
           "Analytical breakdown of the 6 PESTEL dimensions, severity vs. volatility profile, and risk horizon mapping.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_BLUE_ACCENT)

    # CONTENEDOR IZQUIERDO: RADAR (X: 0.8", W: 5.7", H: 5.15")
    left_x = Inches(0.8)
    cont_y = Inches(1.65)
    left_w = Inches(5.7)
    cont_h = Inches(5.15)

    left_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, cont_y, left_w, cont_h)
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = COLOR_CARD_BG
    left_box.line.color.rgb = COLOR_BORDER
    left_box.line.width = Pt(1.5)

    t_left = slide.shapes.add_textbox(left_x + Inches(0.2), cont_y + Inches(0.15), left_w - Inches(0.4), Inches(0.35))
    tf_tl = t_left.text_frame
    tf_tl.margin_left = tf_tl.margin_right = tf_tl.margin_top = tf_tl.margin_bottom = 0
    p_tl = tf_tl.paragraphs[0]
    p_tl.text = "PERFIL HEXAGONAL DE LAS 6 DIMENSIONES PESTEL" if lang == 'ES' else "PESTEL 6 DIMENSIONS HEXAGONAL PROFILE"
    p_tl.font.name = FONT_HEADING
    p_tl.font.size = Pt(10.5)
    p_tl.font.bold = True
    p_tl.font.color.rgb = COLOR_NAVY_DARK
    p_tl.alignment = PP_ALIGN.CENTER

    img_radar_path = create_radar_image(lang=lang, out_path=f"temp_pestel_radar_{lang}.png")
    slide.shapes.add_picture(img_radar_path, left_x + Inches(0.45), cont_y + Inches(0.55), width=Inches(4.8))

    cap_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x + Inches(0.3), cont_y + cont_h - Inches(0.65), left_w - Inches(0.6), Inches(0.48))
    cap_box.fill.solid()
    cap_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    cap_box.line.fill.background()
    tf_cap = cap_box.text_frame
    tf_cap.margin_left = tf_cap.margin_right = tf_cap.margin_top = tf_cap.margin_bottom = 0
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = ("Índice Riesgo Compuesto R_comp = 3.82 / 5.00  •  Resiliencia Macro = 1.18 / 4.00"
                  if lang == 'ES' else
                  "Composite Macro Risk Index R_comp = 3.82 / 5.00  •  Macro Resilience = 1.18 / 4.00")
    p_cap.font.name = FONT_HEADING
    p_cap.font.size = Pt(8.5)
    p_cap.font.bold = True
    p_cap.font.color.rgb = COLOR_WHITE
    p_cap.alignment = PP_ALIGN.CENTER

    # CONTENEDOR DERECHO: 3 TARJETAS ESTRUCTURADAS DE SEVERIDAD & HORIZONTE
    right_x = Inches(6.75)
    right_w = Inches(5.78)

    severity_blocks = [
        {
            'badge': "SEVERIDAD MÁXIMA EN P&L (S ≥ 4.5)" if lang == 'ES' else "PEAK P&L SEVERITY (S ≥ 4.5)",
            'title': "Disrupción IA Generativa, Picos Energéticos y Sanciones AI Act" if lang == 'ES' else "Generative AI Disruption, Power Spikes & AI Act Penalties",
            'bullets': [
                "IA Generativa (4.6) amenaza con abaratar un 40% el coste de nuevos competidores" if lang == 'ES' else "Generative AI (4.6) threatens a 40% unit cost reduction for new entrants",
                "Volatilidad energética (4.5) impacta directamente en margen bruto de producción" if lang == 'ES' else "Energy price swings (4.5) directly compress manufacturing gross margins",
                "Sanciones de hasta 35M€ ante el Reglamento de IA sin gobernanza algorítmica" if lang == 'ES' else "Fines up to 35M€ under EU AI Act in absence of formal algorithmic compliance"
            ],
            'color': COLOR_ROSE_ACCENT,
            'bg': COLOR_ROSE_BG,
            'border': COLOR_ROSE_BORDER,
            'h': Inches(1.58)
        },
        {
            'badge': "ALTA VOLATILIDAD TEMPORAL (V ≥ 4.0)" if lang == 'ES' else "HIGH TEMPORAL VOLATILITY (V ≥ 4.0)",
            'title': "Tensiones Arancelarias, Ciberamenazas y Tipos de Cambio" if lang == 'ES' else "Tariff Tensions, Cyber Attacks & FX Fluctuations",
            'bullets': [
                "Fragmentación comercial global: aranceles y barreras con oscilación trimestral" if lang == 'ES' else "Global trade fragmentation: tariffs and barriers shifting on quarterly cycles",
                "Ataques avanzados de ransomware dirigidos a infraestructuras críticas y ERP" if lang == 'ES' else "Advanced persistent ransomware attacks targeting industrial SCADA and ERP",
                "Fluctuaciones EUR/USD sin cobertura que desestabilizan ingresos internacionales" if lang == 'ES' else "Unhedged EUR/USD currency volatility eroding overseas export earnings"
            ],
            'color': COLOR_AMBER_ACCENT,
            'bg': COLOR_AMBER_BG,
            'border': COLOR_AMBER_BORDER,
            'h': Inches(1.58)
        },
        {
            'badge': "HORIZONTE TEMPORAL & ESTRUCTURAL" if lang == 'ES' else "STRUCTURAL HORIZON & RESILIENCE",
            'title': "Envejecimiento Demográfico y Directiva CSRD (Alcance 1-3)" if lang == 'ES' else "Demographic Aging & EU CSRD Directives (Scope 1-3)",
            'bullets': [
                "Horizonte 0-6 meses: blindaje urgente de contratos de energía y auditoría legal" if lang == 'ES' else "0-6 month horizon: immediate energy contract hedges & AI Act legal audit",
                "Horizonte 12-24 meses: adaptación técnica CSRD y programa de retención de talento" if lang == 'ES' else "12-24 month horizon: CSRD reporting infrastructure & STEM talent retention",
                "El 78% del impacto macro es evitable mediante ejecución disciplinada del plan" if lang == 'ES' else "78% of macro financial risk is preventable through disciplined plan execution"
            ],
            'color': COLOR_TEAL_ACCENT,
            'bg': COLOR_TEAL_BG,
            'border': COLOR_TEAL_BORDER,
            'h': Inches(1.58)
        }
    ]

    curr_sy = cont_y
    for block in severity_blocks:
        b_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, curr_sy, right_w, block['h'])
        b_shape.fill.solid()
        b_shape.fill.fore_color.rgb = block['bg']
        b_shape.line.color.rgb = block['border']
        b_shape.line.width = Pt(1.5)

        hp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x + Inches(0.18), curr_sy + Inches(0.12), Inches(2.8), Inches(0.26))
        hp.fill.solid()
        hp.fill.fore_color.rgb = block['color']
        hp.line.fill.background()
        tf_hp = hp.text_frame
        tf_hp.margin_left = tf_hp.margin_right = tf_hp.margin_top = tf_hp.margin_bottom = 0
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = block['badge']
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(8)
        p_hp.font.bold = True
        p_hp.font.color.rgb = COLOR_WHITE
        p_hp.alignment = PP_ALIGN.CENTER

        t_box = slide.shapes.add_textbox(right_x + Inches(0.18), curr_sy + Inches(0.38), right_w - Inches(0.36), Inches(0.32))
        tf_tb = t_box.text_frame
        tf_tb.margin_left = tf_tb.margin_right = tf_tb.margin_top = tf_tb.margin_bottom = 0
        p_t = tf_tb.paragraphs[0]
        p_t.text = block['title']
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY_DARK

        b_box = slide.shapes.add_textbox(right_x + Inches(0.18), curr_sy + Inches(0.70), right_w - Inches(0.36), block['h'] - Inches(0.75))
        tf_bb = b_box.text_frame
        tf_bb.word_wrap = True
        tf_bb.margin_left = tf_bb.margin_right = tf_bb.margin_top = tf_bb.margin_bottom = 0

        for b_idx, bullet in enumerate(block['bullets']):
            p_b = tf_bb.paragraphs[0] if b_idx == 0 else tf_bb.add_paragraph()
            p_b.text = f"• {bullet}"
            p_b.font.name = FONT_BODY
            p_b.font.size = Pt(8.5)
            p_b.font.color.rgb = COLOR_TEXT_MAIN
            p_b.space_after = Pt(2)

        curr_sy += block['h'] + Inches(0.20)

    add_footer(slide, 2, 3, lang=lang)


# ==============================================================================
# SLIDE 3: ROADMAP DE RESILIENCIA & GATEWAY DE DECISIÓN
# ==============================================================================
def build_slide3(prs, lang='ES'):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    kicker = "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD"
    badge = "ROADMAP & GATEWAY DE DECISIÓN" if lang == 'ES' else "ROADMAP & BOARD DECISION GATEWAY"
    title = ("El plan de contingencia 2026 despliega 8 iniciativas con responsables C-Level y somete a votación 3 resoluciones vinculantes"
             if lang == 'ES' else
             "The 2026 contingency roadmap deploys 8 C-Suite initiatives and submits 3 binding board resolutions for formal approval")
    sub = ("Cronograma trimestral de blindaje macroeconómico, presupuesto asignado y aprobaciones requeridas del Consejo."
           if lang == 'ES' else
           "Quarterly macroeconomic resilience schedule, allocated budget, and required Board authorizations.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_AMBER_ACCENT)

    # MITAD SUPERIOR: ROADMAP Q1-Q4 (Y: 1.65", H: 2.35")
    quarters = [
        {
            'q': "Q1-2026",
            'focus': "COBERTURAS & BLINDAJE FINANCIERO" if lang == 'ES' else "FINANCIAL HEDGES & DEFENSE",
            'inits': [
                ("Contratos PPA & Cobertura Gas", "CFO", "80k€") if lang == 'ES' else ("PPA & Natural Gas Hedges", "CFO", "$80k"),
                ("Pólizas Forward USD/GBP", "CFO", "15k€") if lang == 'ES' else ("FX Forward Contracts", "CFO", "$15k")
            ],
            'color': COLOR_BLUE_ACCENT,
            'bg': COLOR_BLUE_BG,
            'border': COLOR_BLUE_BORDER
        },
        {
            'q': "Q2-2026",
            'focus': "COMPLIANCE & ADOPCIÓN IA" if lang == 'ES' else "COMPLIANCE & AI ADOPTION",
            'inits': [
                ("Agentes GenAI en Operaciones", "CTO", "150k€") if lang == 'ES' else ("GenAI Agents in Operations", "CTO", "$150k"),
                ("Auditoría Legal EU AI Act", "CLO", "65k€") if lang == 'ES' else ("EU AI Act Legal Audit", "CLO", "$65k")
            ],
            'color': COLOR_EMERALD_ACCENT,
            'bg': COLOR_EMERALD_BG,
            'border': COLOR_EMERALD_BORDER
        },
        {
            'q': "Q3-2026",
            'focus': "CADENA SUMINISTRO & ESG" if lang == 'ES' else "SUPPLY CHAIN & ESG",
            'inits': [
                ("Nearshoring Ensamblaje Europa", "COO", "170k€") if lang == 'ES' else ("Nearshoring Assembly Hub", "COO", "$170k"),
                ("Software Contabilidad CSRD", "CSO", "70k€") if lang == 'ES' else ("CSRD Carbon Software", "CSO", "$70k")
            ],
            'color': COLOR_AMBER_ACCENT,
            'bg': COLOR_AMBER_BG,
            'border': COLOR_AMBER_BORDER
        },
        {
            'q': "Q4-2026",
            'focus': "CIBERSEGURIDAD & TALENTO" if lang == 'ES' else "CYBERSECURITY & TALENT",
            'inits': [
                ("Arquitectura Zero-Trust SOC", "CISO", "100k€") if lang == 'ES' else ("Zero-Trust SOC Rollout", "CISO", "$100k"),
                ("Academia Retención Talento", "CHRO", "65k€") if lang == 'ES' else ("STEM Academy & Retention", "CHRO", "$65k")
            ],
            'color': COLOR_ROSE_ACCENT,
            'bg': COLOR_ROSE_BG,
            'border': COLOR_ROSE_BORDER
        }
    ]

    q_w = Inches(2.78)
    q_h = Inches(2.3)
    start_qx = Inches(0.8)
    gap_qx = Inches(0.2)
    start_qy = Inches(1.65)

    for i, q_data in enumerate(quarters):
        curr_qx = start_qx + i * (q_w + gap_qx)

        q_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_qx, start_qy, q_w, q_h)
        q_box.fill.solid()
        q_box.fill.fore_color.rgb = q_data['bg']
        q_box.line.color.rgb = q_data['border']
        q_box.line.width = Pt(1.5)

        qh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_qx + Inches(0.15), start_qy + Inches(0.12), q_w - Inches(0.3), Inches(0.32))
        qh.fill.solid()
        qh.fill.fore_color.rgb = q_data['color']
        qh.line.fill.background()
        tf_qh = qh.text_frame
        tf_qh.margin_left = tf_qh.margin_right = tf_qh.margin_top = tf_qh.margin_bottom = 0
        p_qh = tf_qh.paragraphs[0]
        p_qh.text = f"{q_data['q']} • {q_data['focus']}"
        p_qh.font.name = FONT_HEADING
        p_qh.font.size = Pt(7.8)
        p_qh.font.bold = True
        p_qh.font.color.rgb = COLOR_WHITE
        p_qh.alignment = PP_ALIGN.CENTER

        in_box = slide.shapes.add_textbox(curr_qx + Inches(0.12), start_qy + Inches(0.52), q_w - Inches(0.24), q_h - Inches(0.6))
        tf_in = in_box.text_frame
        tf_in.word_wrap = True
        tf_in.margin_left = tf_in.margin_right = tf_in.margin_top = tf_in.margin_bottom = 0

        for in_idx, (init_name, init_owner, init_capex) in enumerate(q_data['inits']):
            p_n = tf_in.paragraphs[0] if in_idx == 0 else tf_in.add_paragraph()
            p_n.text = f"▶ {init_name}"
            p_n.font.name = FONT_HEADING
            p_n.font.size = Pt(9.5)
            p_n.font.bold = True
            p_n.font.color.rgb = COLOR_NAVY_DARK

            p_sub = tf_in.add_paragraph()
            p_sub.text = f"    Owner: {init_owner}  |  Presupuesto: {init_capex}" if lang == 'ES' else f"    Owner: {init_owner}  |  Budget: {init_capex}"
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(8.5)
            p_sub.font.color.rgb = COLOR_TEXT_MUTED
            p_sub.space_after = Pt(8)

    # MITAD INFERIOR: BOARD DECISION GATEWAY (Y: 4.15", H: 2.75")
    gate_x = Inches(0.8)
    gate_y = Inches(4.15)
    gate_w = Inches(11.733)
    gate_h = Inches(2.75)

    gate_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gate_x, gate_y, gate_w, gate_h)
    gate_box.fill.solid()
    gate_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    gate_box.line.color.rgb = COLOR_GOLD
    gate_box.line.width = Pt(2.0)

    gt_box = slide.shapes.add_textbox(gate_x + Inches(0.3), gate_y + Inches(0.12), gate_w - Inches(4.5), Inches(0.35))
    tf_gt = gt_box.text_frame
    tf_gt.margin_left = tf_gt.margin_right = tf_gt.margin_top = tf_gt.margin_bottom = 0
    p_gt = tf_gt.paragraphs[0]
    p_gt.text = ("DECISIÓN REQUERIDA DEL CONSEJO DE ADMINISTRACIÓN (BOARD DECISION GATEWAY)"
                 if lang == 'ES' else
                 "BOARD OF DIRECTORS FORMAL DECISION GATEWAY")
    p_gt.font.name = FONT_HEADING
    p_gt.font.size = Pt(11)
    p_gt.font.bold = True
    p_gt.font.color.rgb = COLOR_WHITE

    gpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gate_x + gate_w - Inches(4.0), gate_y + Inches(0.12), Inches(3.7), Inches(0.32))
    gpill.fill.solid()
    gpill.fill.fore_color.rgb = COLOR_GOLD
    gpill.line.fill.background()
    tf_gp = gpill.text_frame
    tf_gp.margin_left = tf_gp.margin_right = tf_gp.margin_top = tf_gp.margin_bottom = 0
    p_gp = tf_gp.paragraphs[0]
    p_gp.text = "SOMETER A VOTACIÓN FORMAL" if lang == 'ES' else "SUBMITTED FOR FORMAL VOTE"
    p_gp.font.name = FONT_HEADING
    p_gp.font.size = Pt(8.5)
    p_gp.font.bold = True
    p_gp.font.color.rgb = COLOR_NAVY_DARK
    p_gp.alignment = PP_ALIGN.CENTER

    resolutions = [
        {
            'num': "RESOLUCIÓN 1" if lang == 'ES' else "RESOLUTION 1",
            'title': "Aprobación del Fondo de Contingencia Macro (715.000 €)" if lang == 'ES' else "Authorization of Macro Contingency Reserve ($715,000)",
            'desc': ("Aprobación formal de una partida de 485.000 € en CAPEX y 230.000 € en OPEX anual consignada específicamente para coberturas energéticas, auditoría del AI Act y diversificación de proveedores."
                     if lang == 'ES' else
                     "Formal approval of $485,000 CAPEX and $230,000 OPEX earmarked for energy derivative hedges, EU AI Act compliance, and supply chain nearshoring."),
            'status': "RECOMENDADA: APROBAR" if lang == 'ES' else "RECOMMENDED: APPROVE"
        },
        {
            'num': "RESOLUCIÓN 2" if lang == 'ES' else "RESOLUTION 2",
            'title': "Ratificación de Mandatos y Responsables C-Level" if lang == 'ES' else "Ratification of C-Suite Accountability Mandates",
            'desc': ("Designación estatutaria del CFO como responsable de coberturas de derivados, del CTO como garante de gobernanza de IA y del COO para la seguridad de la cadena de suministro."
                     if lang == 'ES' else
                     "Statutory assignment of the CFO as head of financial hedging, the CTO for algorithmic compliance, and the COO for supply chain resilience."),
            'status': "RECOMENDADA: APROBAR" if lang == 'ES' else "RECOMMENDED: APPROVE"
        },
        {
            'num': "RESOLUCIÓN 3" if lang == 'ES' else "RESOLUTION 3",
            'title': "Calendario de Auditoría y Supervisión Trimestral" if lang == 'ES' else "Quarterly Board Audit & Surveillance Schedule",
            'desc': ("Instauración de una revisión obligatoria en cada reunión ordinaria del Consejo sobre la evolución de la matriz de volatilidad y la ejecución del presupuesto de contingencia."
                     if lang == 'ES' else
                     "Establishment of a mandatory standing agenda item at each regular Board session to review macro volatility shifts and contingency milestones."),
            'status': "RECOMENDADA: APROBAR" if lang == 'ES' else "RECOMMENDED: APPROVE"
        }
    ]

    r_w = Inches(3.64)
    r_h = Inches(1.95)
    r_y = gate_y + Inches(0.58)
    r_gap = Inches(0.25)

    for r_idx, res in enumerate(resolutions):
        rx = gate_x + Inches(0.3) + r_idx * (r_w + r_gap)

        r_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, r_y, r_w, r_h)
        r_card.fill.solid()
        r_card.fill.fore_color.rgb = COLOR_NAVY_MED
        r_card.line.color.rgb = RGBColor(71, 85, 105)
        r_card.line.width = Pt(1.2)

        # Tag
        rtag = slide.shapes.add_textbox(rx + Inches(0.15), r_y + Inches(0.08), r_w - Inches(0.3), Inches(0.22))
        tf_rtag = rtag.text_frame
        tf_rtag.margin_left = tf_rtag.margin_right = tf_rtag.margin_top = tf_rtag.margin_bottom = 0
        p_rt = tf_rtag.paragraphs[0]
        p_rt.text = res['num']
        p_rt.font.name = FONT_HEADING
        p_rt.font.size = Pt(8.5)
        p_rt.font.bold = True
        p_rt.font.color.rgb = COLOR_GOLD

        # Title
        rtitle = slide.shapes.add_textbox(rx + Inches(0.15), r_y + Inches(0.28), r_w - Inches(0.3), Inches(0.42))
        tf_rtitle = rtitle.text_frame
        tf_rtitle.word_wrap = True
        tf_rtitle.margin_left = tf_rtitle.margin_right = tf_rtitle.margin_top = tf_rtitle.margin_bottom = 0
        p_rti = tf_rtitle.paragraphs[0]
        p_rti.text = res['title']
        p_rti.font.name = FONT_HEADING
        p_rti.font.size = Pt(9.5)
        p_rti.font.bold = True
        p_rti.font.color.rgb = COLOR_WHITE

        # Desc
        rdesc = slide.shapes.add_textbox(rx + Inches(0.15), r_y + Inches(0.72), r_w - Inches(0.3), Inches(0.82))
        tf_rdesc = rdesc.text_frame
        tf_rdesc.word_wrap = True
        tf_rdesc.margin_left = tf_rdesc.margin_right = tf_rdesc.margin_top = tf_rdesc.margin_bottom = 0
        p_rd = tf_rdesc.paragraphs[0]
        p_rd.text = res['desc']
        p_rd.font.name = FONT_BODY
        p_rd.font.size = Pt(8.2)
        p_rd.font.color.rgb = RGBColor(203, 213, 225)

        # Status Pill
        rspill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx + Inches(0.15), r_y + r_h - Inches(0.36), r_w - Inches(0.3), Inches(0.26))
        rspill.fill.solid()
        rspill.fill.fore_color.rgb = COLOR_EMERALD_ACCENT
        rspill.line.fill.background()
        tf_rsp = rspill.text_frame
        tf_rsp.margin_left = tf_rsp.margin_right = tf_rsp.margin_top = tf_rsp.margin_bottom = 0
        p_rsp = tf_rsp.paragraphs[0]
        p_rsp.text = res['status']
        p_rsp.font.name = FONT_HEADING
        p_rsp.font.size = Pt(8)
        p_rsp.font.bold = True
        p_rsp.font.color.rgb = COLOR_WHITE
        p_rsp.alignment = PP_ALIGN.CENTER

    add_footer(slide, 3, 3, lang=lang)


def generate_deck(lang='ES', out_path='Presentacion_PESTEL_CLevel_ES.pptx'):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide1(prs, lang=lang)
    build_slide2(prs, lang=lang)
    build_slide3(prs, lang=lang)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    prs.save(out_path)
    print(f"[OK] Presentación PowerPoint generada ({lang}): {out_path}")

    # Limpiar radar temporal
    radar_tmp = f"temp_pestel_radar_{lang}.png"
    if os.path.exists(radar_tmp):
        os.remove(radar_tmp)


def main():
    dir_es = os.path.join("packages", "[ES]_PESTEL_Cuantitativo")
    dir_en = os.path.join("packages", "[EN]_Quantitative_PESTEL")

    path_es = os.path.join(dir_es, "Presentacion_PESTEL_CLevel_ES.pptx")
    path_en = os.path.join(dir_en, "Deck_PESTEL_CLevel_EN.pptx")

    generate_deck(lang='ES', out_path=path_es)
    generate_deck(lang='EN', out_path=path_en)


if __name__ == '__main__':
    main()
