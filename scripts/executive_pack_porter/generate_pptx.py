#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. static/downloads/[ES]_5_Fuerzas_Porter/Presentacion_Porter_CLevel_ES.pptx
2. static/downloads/[EN]_Porter_5_Forces/Deck_Porter_CLevel_EN.pptx

Características de diseño Tier-1 (McKinsey / BCG):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Pirámide de Minto y Action Titles contundentes.
- Gráfico Radar pentagonal generado en alta resolución e integrado en Slide 2.
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
    """Genera un gráfico radar pentagonal de alta resolución para la slide 2."""
    if lang == 'ES':
        categories = ['Rivalidad\nCompetitiva', 'Poder de\nProveedores', 'Poder de\nClientes', 'Nuevos\nEntrantes', 'Productos\nSustitutos']
    else:
        categories = ['Competitive\nRivalry', 'Supplier\nPower', 'Buyer\nPower', 'New\nEntrants', 'Substitute\nProducts']

    N = len(categories)
    # Valores cuantitativos de la evaluación canónica
    values = [3.45, 3.25, 4.00, 2.20, 3.85]
    values += values[:1]

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.8, 5.2), subplot_kw=dict(polar=True), dpi=220)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories, color='#0F172A', size=9.5, weight='bold', fontfamily='sans-serif')
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ['1.0', '2.0', '3.0', '4.0', '5.0'], color='#64748B', size=8, fontfamily='sans-serif')
    plt.ylim(0, 5.2)

    # Cuadrícula y polígono de datos
    ax.grid(color='#CBD5E1', linestyle='--', linewidth=0.8)
    ax.spines['polar'].set_color('#94A3B8')

    ax.plot(angles, values, color='#2563EB', linewidth=2.8, linestyle='solid', label='Perfil 5 Fuerzas' if lang == 'ES' else '5 Forces Profile')
    ax.fill(angles, values, color='#2563EB', alpha=0.22)
    ax.scatter(angles[:-1], values[:-1], color='#0F172A', s=55, zorder=5, edgecolors='#FFFFFF', linewidths=1.5)

    # Etiqueta central de índice medio
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', transparent=False, facecolor='#FFFFFF')
    plt.close()
    return out_path


def add_header_banner(slide, kicker_text, badge_text, action_title, sub_text, badge_color=COLOR_BLUE_ACCENT):
    """Genera la cabecera corporativa estándar Minto de Datalaria."""
    # Kicker / Categoría superior izquierda
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

    # Badge / Píldora de estado superior derecha
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

    # Action Title (Minto Pyramid Principle)
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

    # Subtítulo explicativo
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
    # Línea divisoria
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BORDER
    line.line.color.rgb = COLOR_BORDER

    # Texto confidencial
    conf_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(8.5), Inches(0.3))
    tf_c = conf_box.text_frame
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = "Datalaria.com | Executive Decision Pack • Documento Confidencial para Consejo de Administración" if lang == 'ES' else "Datalaria.com | Executive Decision Pack • Confidential Board of Directors Document"
    p_c.font.name = FONT_BODY
    p_c.font.size = Pt(8.5)
    p_c.font.color.rgb = COLOR_TEXT_MUTED

    # Numeración
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
    badge = "DIAGNÓSTICO ESTRATÉGICO C-LEVEL" if lang == 'ES' else "C-SUITE STRATEGIC DIAGNOSIS"
    title = ("La presión de sustitutos y concentración de compradores erosionará nuestro margen EBITDA en un 4.5% si no consolidamos barreras antes de Q4"
             if lang == 'ES' else
             "Emerging substitutes and buyer concentration will erode EBITDA margins by 4.5% unless defensive switching costs are built by Q4")
    sub = ("Diagnóstico cuantitativo del sector, evaluación del foso defensivo (Moat) y retorno de las iniciativas de blindaje."
           if lang == 'ES' else
           "Quantitative industry assessment, defendable economic moat diagnosis, and capital allocation return metrics.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_NAVY_DARK)

    # 4 Tarjetas de Impacto perfectamente alineadas
    cards_data = [
        {
            'tag': "ATRACTIVO DE INDUSTRIA" if lang == 'ES' else "INDUSTRY ATTRACTIVENESS",
            'metric': "1.58 / 4.0",
            'submetric': "Hostilidad Moderada-Alta" if lang == 'ES' else "Moderate-High Hostility",
            'bullets': [
                "Crecimiento desacelerado (+1.8% anual)" if lang == 'ES' else "Decelerated industry growth (+1.8% YoY)",
                "Guerra de precios activa en cuentas clave" if lang == 'ES' else "Active price war across key corporate accounts",
                "Oligopolio: 3 rivales concentran 68%" if lang == 'ES' else "Oligopoly: top 3 players hold 68% share"
            ],
            'pill': "SECTOR EXIGENTE" if lang == 'ES' else "HOSTILE ENVIRONMENT",
            'color_theme': COLOR_BLUE_ACCENT,
            'bg_color': COLOR_BLUE_BG,
            'border_color': COLOR_BLUE_BORDER,
            'text_color': COLOR_BLUE_TEXT
        },
        {
            'tag': "FUERZAS CRÍTICAS (PEAK)" if lang == 'ES' else "CRITICAL PEAK FORCES",
            'metric': "F3 & F5: 4.0",
            'submetric': "Clientes y Sustitutos" if lang == 'ES' else "Buyers & Substitutes",
            'bullets': [
                "Top 5 clientes generan 52% del ARR" if lang == 'ES' else "Top 5 clients generate 52% of total ARR",
                "Sustitutos IA ofrecen 40% ahorro coste" if lang == 'ES' else "AI substitutes offer 40% lower cost",
                "Presión a la baja en cada renovación" if lang == 'ES' else "Continuous downward pricing pressure"
            ],
            'pill': "FOCO DE MITIGACIÓN" if lang == 'ES' else "MITIGATION PRIORITY",
            'color_theme': COLOR_ROSE_ACCENT,
            'bg_color': COLOR_ROSE_BG,
            'border_color': COLOR_ROSE_BORDER,
            'text_color': COLOR_ROSE_TEXT
        },
        {
            'tag': "FOSO DEFENDIBLE (MOAT)" if lang == 'ES' else "DEFENDABLE ECONOMIC MOAT",
            'metric': "3.80 / 5.0",
            'submetric': "Margen +18.4% vs Sector" if lang == 'ES' else "Gross Margin +18.4% vs Peers",
            'bullets': [
                "Conectores ERP integrados en clientes" if lang == 'ES' else "Deep ERP workflow integrations",
                "2 patentes activas y algoritmos core" if lang == 'ES' else "2 active patents & proprietary algorithms",
                "Retención neta NRR histórica en 112%" if lang == 'ES' else "Historical Net Retention Rate (NRR) at 112%"
            ],
            'pill': "VENTAJA DEFENDIBLE" if lang == 'ES' else "STRONG ECONOMIC MOAT",
            'color_theme': COLOR_EMERALD_ACCENT,
            'bg_color': COLOR_EMERALD_BG,
            'border_color': COLOR_EMERALD_BORDER,
            'text_color': COLOR_EMERALD_TEXT
        },
        {
            'tag': "ASIGNACIÓN DE CAPITAL" if lang == 'ES' else "CAPITAL ALLOCATION",
            'metric': "+4.8% EBITDA",
            'submetric': "CAPEX 675k€ | OPEX 240k€" if lang == 'ES' else "CAPEX $675k | OPEX $240k",
            'bullets': [
                "8 iniciativas de blindaje asignadas" if lang == 'ES' else "8 prioritized moat initiatives",
                "Retorno esperado de inversión ROIC > 26%" if lang == 'ES' else "Expected investment return ROIC > 26%",
                "Preserva 3.2M€ en flujo libre (FCF)" if lang == 'ES' else "Preserves $3.2M cumulative free cash flow"
            ],
            'pill': "PAYBACK < 14 MESES" if lang == 'ES' else "PAYBACK < 14 MONTHS",
            'color_theme': COLOR_AMBER_ACCENT,
            'bg_color': COLOR_AMBER_BG,
            'border_color': COLOR_AMBER_BORDER,
            'text_color': COLOR_AMBER_TEXT
        }
    ]

    card_w = Inches(2.78)
    card_h = Inches(5.15)
    start_x = Inches(0.8)
    gap_x = Inches(0.2)
    start_y = Inches(1.65)

    for i, card in enumerate(cards_data):
        curr_x = start_x + i * (card_w + gap_x)

        # Contenedor de fondo de la tarjeta
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, start_y, card_w, card_h)
        box.fill.solid()
        box.fill.fore_color.rgb = card['bg_color']
        box.line.color.rgb = card['border_color']
        box.line.width = Pt(1.5)

        # Header Pill de categoría
        p_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x + Inches(0.18), start_y + Inches(0.2), card_w - Inches(0.36), Inches(0.36))
        p_shape.fill.solid()
        p_shape.fill.fore_color.rgb = card['color_theme']
        p_shape.line.fill.background()
        tf_p = p_shape.text_frame
        tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        p = tf_p.paragraphs[0]
        p.text = card['tag']
        p.font.name = FONT_HEADING
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        # Métrica Principal (26pt bold)
        m_box = slide.shapes.add_textbox(curr_x + Inches(0.15), start_y + Inches(0.68), card_w - Inches(0.3), Inches(0.55))
        tf_m = m_box.text_frame
        tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
        p_m = tf_m.paragraphs[0]
        p_m.text = card['metric']
        p_m.font.name = FONT_HEADING
        p_m.font.size = Pt(25)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_NAVY_DARK
        p_m.alignment = PP_ALIGN.CENTER

        # Submétrica explicativa
        s_box = slide.shapes.add_textbox(curr_x + Inches(0.15), start_y + Inches(1.28), card_w - Inches(0.3), Inches(0.35))
        tf_sub = s_box.text_frame
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
        p_s = tf_sub.paragraphs[0]
        p_s.text = card['submetric']
        p_s.font.name = FONT_HEADING
        p_s.font.size = Pt(10)
        p_s.font.bold = True
        p_s.font.color.rgb = card['text_color']
        p_s.alignment = PP_ALIGN.CENTER

        # Línea divisoria
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, curr_x + Inches(0.2), start_y + Inches(1.72), card_w - Inches(0.4), Inches(0.015))
        div.fill.solid()
        div.fill.fore_color.rgb = card['border_color']
        div.line.fill.background()

        # Viñetas de soporte ejecutivo
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

        # Píldora inferior de veredicto
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
# SLIDE 2: EVIDENCIA CUANTITATIVA & PERFIL RADAR PENTAGONAL
# ==============================================================================
def build_slide2(prs, lang='ES'):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    kicker = "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD"
    badge = "EVIDENCIA CUANTITATIVA & RADAR" if lang == 'ES' else "QUANTITATIVE EVIDENCE & RADAR"
    title = ("El perfil pentagonal revela asimetría: las barreras nos protegen, pero clientes y sustitutos exigen blindaje urgente"
             if lang == 'ES' else
             "Pentagonal profile reveals critical asymmetry: entry barriers protect core, but buyers and substitutes demand moat")
    sub = ("Desglose analítico de las 5 fuerzas canónicas de Porter y ponderación estocástica de intensidad competitiva."
           if lang == 'ES' else
           "Analytical breakdown of Porter's 5 canonical forces and normalized stochastic competitive intensity weighting.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_BLUE_ACCENT)

    # CONTENEDOR IZQUIERDO: GRÁFICO RADAR (X: 0.8", W: 5.7", H: 5.15")
    left_x = Inches(0.8)
    cont_y = Inches(1.65)
    left_w = Inches(5.7)
    cont_h = Inches(5.15)

    left_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, cont_y, left_w, cont_h)
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = COLOR_CARD_BG
    left_box.line.color.rgb = COLOR_BORDER
    left_box.line.width = Pt(1.5)

    # Título del contenedor izquierdo
    t_left = slide.shapes.add_textbox(left_x + Inches(0.2), cont_y + Inches(0.15), left_w - Inches(0.4), Inches(0.35))
    tf_tl = t_left.text_frame
    tf_tl.margin_left = tf_tl.margin_right = tf_tl.margin_top = tf_tl.margin_bottom = 0
    p_tl = tf_tl.paragraphs[0]
    p_tl.text = "PERFIL PENTAGONAL DE LAS 5 FUERZAS DE PORTER" if lang == 'ES' else "PORTER'S 5 FORCES PENTAGONAL PROFILE"
    p_tl.font.name = FONT_HEADING
    p_tl.font.size = Pt(10.5)
    p_tl.font.bold = True
    p_tl.font.color.rgb = COLOR_NAVY_DARK
    p_tl.alignment = PP_ALIGN.CENTER

    # Generar e insertar imagen Radar
    img_radar_path = create_radar_image(lang=lang, out_path=f"temp_radar_{lang}.png")
    slide.shapes.add_picture(img_radar_path, left_x + Inches(0.45), cont_y + Inches(0.55), width=Inches(4.8))

    # Caption inferior del radar
    cap_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x + Inches(0.3), cont_y + cont_h - Inches(0.65), left_w - Inches(0.6), Inches(0.48))
    cap_box.fill.solid()
    cap_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    cap_box.line.fill.background()
    tf_cap = cap_box.text_frame
    tf_cap.margin_left = tf_cap.margin_right = tf_cap.margin_top = tf_cap.margin_bottom = 0
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = ("Índice de Intensidad I_comp = 3.42 / 5.00  •  Atractivo Estructural A_ind = 1.58 / 4.00"
                  if lang == 'ES' else
                  "Competitive Intensity Index I_comp = 3.42 / 5.00  •  Industry Attractiveness A_ind = 1.58 / 4.00")
    p_cap.font.name = FONT_HEADING
    p_cap.font.size = Pt(8.5)
    p_cap.font.bold = True
    p_cap.font.color.rgb = COLOR_WHITE
    p_cap.alignment = PP_ALIGN.CENTER

    # CONTENEDOR DERECHO: 3 TARJETAS ESTRUCTURADAS DE SEVERIDAD (X: 6.75", W: 5.78", H: 5.15")
    right_x = Inches(6.75)
    right_w = Inches(5.78)

    severity_blocks = [
        {
            'badge': "SEVERIDAD CRÍTICA (4.0 / 5.0)" if lang == 'ES' else "CRITICAL SEVERITY (4.0 / 5.0)",
            'title': "F3 (Clientes) & F5 (Sustitutos Tecnológicos)" if lang == 'ES' else "F3 (Buyers) & F5 (Tech Substitutes)",
            'bullets': [
                "Top 5 compradores concentran 52% de compras y presionan con licitaciones" if lang == 'ES' else "Top 5 buyers account for 52% volume and demand annual price tenders",
                "Herramientas IA emergentes reducen tiempos operativos un 40% a menor coste" if lang == 'ES' else "Emerging AI tools deliver 40% faster workflow at a lower cost base",
                "Riesgo directo: erosión anual de márgenes brutos de 2.0 a 3.5 puntos" if lang == 'ES' else "Direct threat: 2.0 to 3.5 percentage point gross margin erosion"
            ],
            'color': COLOR_ROSE_ACCENT,
            'bg': COLOR_ROSE_BG,
            'border': COLOR_ROSE_BORDER,
            'h': Inches(1.58)
        },
        {
            'badge': "SEVERIDAD MODERADA (3.3 / 5.0)" if lang == 'ES' else "MODERATE SEVERITY (3.3 / 5.0)",
            'title': "F1 (Rivalidad Competitiva) & F2 (Proveedores)" if lang == 'ES' else "F1 (Competitive Rivalry) & F2 (Suppliers)",
            'bullets': [
                "Oligopolio asimétrico: batalla intensa por nuevos logos pero estabilidad en base" if lang == 'ES' else "Asymmetric rivalry: aggressive fight for new logos but stable existing base",
                "Proveedores de chips e infraestructura especializada con costes al alza" if lang == 'ES' else "Specialized infrastructure and component vendors passing cost increases",
                "Mitigación: homologación de compras dual sourcing y contratos marco" if lang == 'ES' else "Mitigation: dual-sourcing supplier qualification and long-term contracts"
            ],
            'color': COLOR_AMBER_ACCENT,
            'bg': COLOR_AMBER_BG,
            'border': COLOR_AMBER_BORDER,
            'h': Inches(1.58)
        },
        {
            'badge': "SEVERIDAD BAJA / PROTEGIDA (2.2 / 5.0)" if lang == 'ES' else "LOW SEVERITY / PROTECTED (2.2 / 5.0)",
            'title': "F4 (Amenaza de Nuevos Entrantes)" if lang == 'ES' else "F4 (Threat of New Entrants)",
            'bullets': [
                "Barreras de capital elevadas (3M€+ de inversión requerida y homologación ISO)" if lang == 'ES' else "High capital barriers ($3M+ upfront investment and ISO security compliance)",
                "Curva de experiencia acumulada de 8 años en optimización de algoritmos" if lang == 'ES' else "8-year accumulated dataset learning curve and proprietary domain logic",
                "Ventaja defendible mientras mantengamos el ritmo inversor en I+D" if lang == 'ES' else "Sustainable moat provided internal R&D cadence is aggressively maintained"
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

        # Header Pill
        hp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x + Inches(0.18), curr_sy + Inches(0.12), Inches(2.6), Inches(0.26))
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

        # Título del bloque
        tb = slide.shapes.add_textbox(right_x + Inches(2.9), curr_sy + Inches(0.1), right_w - Inches(3.05), Inches(0.3))
        tf_tb = tb.text_frame
        tf_tb.margin_left = tf_tb.margin_right = tf_tb.margin_top = tf_tb.margin_bottom = 0
        p_tb = tf_tb.paragraphs[0]
        p_tb.text = block['title']
        p_tb.font.name = FONT_HEADING
        p_tb.font.size = Pt(10.5)
        p_tb.font.bold = True
        p_tb.font.color.rgb = COLOR_NAVY_DARK

        # Viñetas
        vb = slide.shapes.add_textbox(right_x + Inches(0.18), curr_sy + Inches(0.42), right_w - Inches(0.36), block['h'] - Inches(0.45))
        tf_vb = vb.text_frame
        tf_vb.word_wrap = True
        tf_vb.margin_left = Inches(0.04)
        tf_vb.margin_right = Inches(0.04)
        tf_vb.margin_top = Inches(0.04)
        tf_vb.margin_bottom = Inches(0.04)

        for b_idx, bullet in enumerate(block['bullets']):
            p_v = tf_vb.paragraphs[0] if b_idx == 0 else tf_vb.add_paragraph()
            p_v.text = f"•  {bullet}"
            p_v.font.name = FONT_BODY
            p_v.font.size = Pt(8.8)
            p_v.font.color.rgb = COLOR_TEXT_MAIN
            p_v.space_after = Pt(2.5)

        curr_sy += block['h'] + Inches(0.2)

    # Limpieza imagen temporal
    if os.path.exists(img_radar_path):
        try:
            os.remove(img_radar_path)
        except Exception:
            pass

    add_footer(slide, 2, 3, lang=lang)


# ==============================================================================
# SLIDE 3: ROADMAP DE BLINDAJE & GATEWAY DE DECISIÓN DEL CONSEJO
# ==============================================================================
def build_slide3(prs, lang='ES'):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    kicker = "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD"
    badge = "ROADMAP & GATEWAY DE DECISIÓN" if lang == 'ES' else "ROADMAP & BOARD DECISION GATEWAY"
    title = ("Plan de Blindaje Q1-Q4: Despliegue de 8 iniciativas clave y Gateway de Decisión para el Consejo"
             if lang == 'ES' else
             "Moat Roadmap Q1-Q4: Execution of 8 Strategic Initiatives and Formal Board Decision Gateway")
    sub = ("Cronograma de ejecución de costes de cambio y resolución de asignación de capital CAPEX/OPEX."
           if lang == 'ES' else
           "Execution timeline for switching costs moat building and formal board capital approval gateway.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_AMBER_ACCENT)

    # MITAD SUPERIOR: ROADMAP POR CUATRIMESTRES (Q1-Q4) (Y: 1.65", H: 2.35")
    quarters = [
        {
            'q': "Q1-2026",
            'focus': "BARRERAS TÉCNICAS" if lang == 'ES' else "TECH BARRIERS",
            'inits': [
                ("Conectores ERP Propietarios", "CTO", "140k€") if lang == 'ES' else ("Proprietary ERP Connectors", "CTO", "$140k"),
                ("Auditoría ISO 27001 Enterprise", "CFO", "45k€") if lang == 'ES' else ("Enterprise ISO 27001 Audit", "CFO", "$45k")
            ],
            'color': COLOR_BLUE_ACCENT,
            'bg': COLOR_BLUE_BG,
            'border': COLOR_BLUE_BORDER
        },
        {
            'q': "Q2-2026",
            'focus': "DIFERENCIACIÓN & COMPRAS" if lang == 'ES' else "DIFFERENTIATION & SOURCING",
            'inits': [
                ("Soluciones Verticales Nicho", "CMO", "95k€") if lang == 'ES' else ("Vertical Industry Suites", "CMO", "$95k"),
                ("Dual Sourcing Materias Primas", "COO", "60k€") if lang == 'ES' else ("Strategic Dual Sourcing", "COO", "$60k")
            ],
            'color': COLOR_EMERALD_ACCENT,
            'bg': COLOR_EMERALD_BG,
            'border': COLOR_EMERALD_BORDER
        },
        {
            'q': "Q3-2026",
            'focus': "INNOVACIÓN ANTE SUSTITUTOS" if lang == 'ES' else "INNOVATION VS SUBSTITUTES",
            'inits': [
                ("Módulo IA Embebida Nativo", "VP Prod", "185k€") if lang == 'ES' else ("Native Embedded AI Module", "VP Prod", "$185k"),
                ("Alianzas Integradores SI", "VP Sales", "75k€") if lang == 'ES' else ("System Integrator Ecosystem", "VP Sales", "$75k")
            ],
            'color': COLOR_AMBER_ACCENT,
            'bg': COLOR_AMBER_BG,
            'border': COLOR_AMBER_BORDER
        },
        {
            'q': "Q4-2026",
            'focus': "ESCALA & FIDELIZACIÓN" if lang == 'ES' else "SCALE & RETENTION",
            'inits': [
                ("Contratos Plurianuales Marco", "CEO", "30k€") if lang == 'ES' else ("Multi-Year Enterprise MSAs", "CEO", "$30k"),
                ("Automatización Self-Service", "COO", "110k€") if lang == 'ES' else ("Self-Service Automation", "COO", "$110k")
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

        # Header de Cuatrimestre
        qh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_qx + Inches(0.15), start_qy + Inches(0.12), q_w - Inches(0.3), Inches(0.32))
        qh.fill.solid()
        qh.fill.fore_color.rgb = q_data['color']
        qh.line.fill.background()
        tf_qh = qh.text_frame
        tf_qh.margin_left = tf_qh.margin_right = tf_qh.margin_top = tf_qh.margin_bottom = 0
        p_qh = tf_qh.paragraphs[0]
        p_qh.text = f"{q_data['q']} • {q_data['focus']}"
        p_qh.font.name = FONT_HEADING
        p_qh.font.size = Pt(8.5)
        p_qh.font.bold = True
        p_qh.font.color.rgb = COLOR_WHITE
        p_qh.alignment = PP_ALIGN.CENTER

        # Iniciativas
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
            p_sub.text = f"    Owner: {init_owner}  |  CAPEX: {init_capex}"
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

    # Título del Gateway
    gt_box = slide.shapes.add_textbox(gate_x + Inches(0.3), gate_y + Inches(0.12), gate_w - Inches(4.5), Inches(0.35))
    tf_gt = gt_box.text_frame
    tf_gt.margin_left = tf_gt.margin_right = tf_gt.margin_top = tf_gt.margin_bottom = 0
    p_gt = tf_gt.paragraphs[0]
    p_gt.text = ("DECISIÓN REQUERIDA DEL COMITÉ DE DIRECCIÓN (BOARD DECISION GATEWAY)"
                 if lang == 'ES' else
                 "BOARD OF DIRECTORS FORMAL DECISION GATEWAY")
    p_gt.font.name = FONT_HEADING
    p_gt.font.size = Pt(11)
    p_gt.font.bold = True
    p_gt.font.color.rgb = COLOR_WHITE

    # Badge de resoluciones
    res_badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gate_x + gate_w - Inches(3.8), gate_y + Inches(0.12), Inches(3.5), Inches(0.32))
    res_badge.fill.solid()
    res_badge.fill.fore_color.rgb = COLOR_GOLD
    res_badge.line.fill.background()
    tf_rb = res_badge.text_frame
    tf_rb.margin_left = tf_rb.margin_right = tf_rb.margin_top = tf_rb.margin_bottom = 0
    p_rb = tf_rb.paragraphs[0]
    p_rb.text = "3 RESOLUCIONES FORMALES SOMETIDAS A VOTACIÓN" if lang == 'ES' else "3 FORMAL RESOLUTIONS SUBMITTED FOR VOTE"
    p_rb.font.name = FONT_HEADING
    p_rb.font.size = Pt(8)
    p_rb.font.bold = True
    p_rb.font.color.rgb = COLOR_NAVY_DARK
    p_rb.alignment = PP_ALIGN.CENTER

    # 3 Columnas de Resoluciones Internas
    res_cards = [
        {
            'num': "RESOLUCIÓN 1" if lang == 'ES' else "RESOLUTION 1",
            'title': "Aprobación de Asignación de Capital" if lang == 'ES' else "Capital Allocation Approval",
            'desc': ("Aprobación formal de 675.000 € en CAPEX y 240.000 € en OPEX anual consignados al presupuesto 2026 para blindaje de costes de cambio."
                     if lang == 'ES' else
                     "Formal sign-off of $675,000 CAPEX and $240,000 annual OPEX earmarked in the 2026 budget to build defendable switching costs."),
            'metric': "Payback: 13.8 meses | ROIC > 26%" if lang == 'ES' else "Payback: 13.8 months | ROIC > 26%"
        },
        {
            'num': "RESOLUCIÓN 2" if lang == 'ES' else "RESOLUTION 2",
            'title': "Ratificación de Sponsors C-Level" if lang == 'ES' else "C-Level Executive Sponsors",
            'desc': ("Designación formal del CTO (barreras técnicas ERP e IA) y CMO (diferenciación de catálogo) como ejecutivos responsables ante Consejo."
                     if lang == 'ES' else
                     "Official appointment of CTO (ERP & AI barriers) and CMO (differentiation) as accountable executive sponsors before the Board."),
            'metric': "Incentivos vinculados a Churn < 2.5%" if lang == 'ES' else "Incentives tied to Churn < 2.5%"
        },
        {
            'num': "RESOLUCIÓN 3" if lang == 'ES' else "RESOLUTION 3",
            'title': "Calendario de Auditoría y Control" if lang == 'ES' else "Governance & Tracking Cadence",
            'desc': ("Establecimiento de una revisión trimestral formal en Comité de Dirección para auditar KPIs de margen EBITDA, NRR y adopción de features."
                     if lang == 'ES' else
                     "Establishment of a formal quarterly Board review to audit EBITDA margin milestones, NRR benchmarks, and feature adoption rates."),
            'metric': "1ª Auditoría Formal: Q2-2026" if lang == 'ES' else "1st Formal Board Audit: Q2-2026"
        }
    ]

    r_w = Inches(3.64)
    r_h = Inches(1.98)
    r_start_x = gate_x + Inches(0.25)
    r_gap = Inches(0.25)
    r_y = gate_y + Inches(0.58)

    for i, res in enumerate(res_cards):
        curr_rx = r_start_x + i * (r_w + r_gap)

        rc_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_rx, r_y, r_w, r_h)
        rc_box.fill.solid()
        rc_box.fill.fore_color.rgb = COLOR_NAVY_MED
        rc_box.line.color.rgb = COLOR_TEXT_MUTED
        rc_box.line.width = Pt(1.0)

        # Header de la resolución
        rh_box = slide.shapes.add_textbox(curr_rx + Inches(0.15), r_y + Inches(0.1), r_w - Inches(0.3), Inches(0.4))
        tf_rh = rh_box.text_frame
        tf_rh.word_wrap = True
        tf_rh.margin_left = tf_rh.margin_right = tf_rh.margin_top = tf_rh.margin_bottom = 0
        p_rh1 = tf_rh.paragraphs[0]
        p_rh1.text = res['num']
        p_rh1.font.name = FONT_HEADING
        p_rh1.font.size = Pt(8)
        p_rh1.font.bold = True
        p_rh1.font.color.rgb = COLOR_GOLD

        p_rh2 = tf_rh.add_paragraph()
        p_rh2.text = res['title']
        p_rh2.font.name = FONT_HEADING
        p_rh2.font.size = Pt(10)
        p_rh2.font.bold = True
        p_rh2.font.color.rgb = COLOR_WHITE

        # Descripción
        rd_box = slide.shapes.add_textbox(curr_rx + Inches(0.15), r_y + Inches(0.58), r_w - Inches(0.3), Inches(0.9))
        tf_rd = rd_box.text_frame
        tf_rd.word_wrap = True
        tf_rd.margin_left = tf_rd.margin_right = tf_rd.margin_top = tf_rd.margin_bottom = 0
        p_rd = tf_rd.paragraphs[0]
        p_rd.text = res['desc']
        p_rd.font.name = FONT_BODY
        p_rd.font.size = Pt(8.5)
        p_rd.font.color.rgb = RGBColor(226, 232, 240)

        # Píldora de métrica de control
        rm_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_rx + Inches(0.15), r_y + r_h - Inches(0.42), r_w - Inches(0.3), Inches(0.3))
        rm_pill.fill.solid()
        rm_pill.fill.fore_color.rgb = COLOR_NAVY_DARK
        rm_pill.line.color.rgb = COLOR_GOLD
        rm_pill.line.width = Pt(1.0)
        tf_rm = rm_pill.text_frame
        tf_rm.margin_left = tf_rm.margin_right = tf_rm.margin_top = tf_rm.margin_bottom = 0
        p_rm = tf_rm.paragraphs[0]
        p_rm.text = res['metric']
        p_rm.font.name = FONT_HEADING
        p_rm.font.size = Pt(8.5)
        p_rm.font.bold = True
        p_rm.font.color.rgb = COLOR_GOLD
        p_rm.alignment = PP_ALIGN.CENTER

    add_footer(slide, 3, 3, lang=lang)


def generate_deck(lang='ES', out_dir='.'):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    os.makedirs(out_dir, exist_ok=True)
    filename = "Presentacion_Porter_CLevel_ES.pptx" if lang == 'ES' else "Deck_Porter_CLevel_EN.pptx"
    out_path = os.path.join(out_dir, filename)

    print(f"[{lang}] Generando presentación C-Level 16:9: {out_path}...")

    # Construir las 3 diapositivas canónicas
    build_slide1(prs, lang=lang)
    build_slide2(prs, lang=lang)
    build_slide3(prs, lang=lang)

    prs.save(out_path)
    print(f"[{lang}] OK: Presentación guardada con éxito ({os.path.getsize(out_path)} bytes).")
    return out_path


def main():
    base_dir_es = "packages/[ES]_5_Fuerzas_Porter"
    base_dir_en = "packages/[EN]_Porter_5_Forces"
    os.makedirs(base_dir_es, exist_ok=True)
    os.makedirs(base_dir_en, exist_ok=True)

    generate_deck(lang='ES', out_dir=base_dir_es)
    generate_deck(lang='EN', out_dir=base_dir_en)


if __name__ == '__main__':
    main()
