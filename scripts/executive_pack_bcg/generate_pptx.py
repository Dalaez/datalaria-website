#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/[ES]_BCG_Dinamica/Presentacion_BCG_CLevel_ES.pptx
2. packages/[EN]_Dynamic_BCG/Deck_BCG_CLevel_EN.pptx

Características de diseño Tier-1 (McKinsey / BCG):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Pirámide de Minto y Action Titles contundentes.
- Diapositiva 1: Síntesis Ejecutiva con 4 tarjetas de impacto de alto contraste.
- Diapositiva 2: Evidencia Cuantitativa con Gráfico de Burbujas cartesiano de alta resolución y tarjetas de cuadrante.
- Diapositiva 3: Roadmap de Asignación Q1-Q4 y Board Decision Gateway con 3 resoluciones formales.
- Sin solapes de texto, márgenes interiores estrictos y jerarquía tipográfica rigurosa.
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

COLOR_GOLD = RGBColor(245, 158, 11)          # #F59E0B Gold
COLOR_TEXT_MAIN = RGBColor(51, 65, 85)       # #334155 Slate 700
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B Slate 500
COLOR_CARD_BG = RGBColor(248, 250, 252)      # #F8FAFC Slate 50
COLOR_BORDER = RGBColor(226, 232, 240)       # #E2E8F0 Slate 200
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"


def create_bubble_chart_image(lang='ES', out_path='temp_bcg_bubble.png'):
    """
    Genera un Gráfico de Burbujas Cartesiano BCG de alta resolución para la slide 2.
    Eje X: Cuota de Mercado Relativa (CMR) [0 a 2.2x] con umbral en 1.0x.
    Eje Y: Tasa de Crecimiento del Mercado (TCM %) [-5% a 35%] con umbral en 10%.
    Tamaño de burbuja: Facturación propia de cada UEN.
    """
    fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=220)

    # 1. Fondos sutiles por cuadrante
    # Cuadrante Superior Izquierdo: INTERROGANTES (CMR < 1.0, TCM >= 10%)
    ax.fill_between([0.0, 1.0], 10.0, 35.0, color='#FFFBEB', alpha=0.9, zorder=1)
    # Cuadrante Superior Derecho: ESTRELLAS (CMR >= 1.0, TCM >= 10%)
    ax.fill_between([1.0, 2.2], 10.0, 35.0, color='#EFF6FF', alpha=0.9, zorder=1)
    # Cuadrante Inferior Izquierdo: PERROS (CMR < 1.0, TCM < 10%)
    ax.fill_between([0.0, 1.0], -5.0, 10.0, color='#FFF1F2', alpha=0.9, zorder=1)
    # Cuadrante Inferior Derecho: VACAS (CMR >= 1.0, TCM < 10%)
    ax.fill_between([1.0, 2.2], -5.0, 10.0, color='#F0FDFA', alpha=0.9, zorder=1)

    # 2. Líneas divisoras cartesianas
    ax.axvline(x=1.0, color='#2563EB', linestyle='--', linewidth=1.5, zorder=2, alpha=0.85)
    ax.axhline(y=10.0, color='#2563EB', linestyle='--', linewidth=1.5, zorder=2, alpha=0.85)

    # 3. Etiquetas de cuadrante en marcas de agua elegantes
    lbl_stars = "ESTRELLAS\n(Invertir)" if lang == 'ES' else "STARS\n(Invest)"
    lbl_cows = "VACAS LECHERAS\n(Ordeñar)" if lang == 'ES' else "CASH COWS\n(Milk)"
    lbl_quest = "INTERROGANTES\n(Decidir / Escalar)" if lang == 'ES' else "QUESTION MARKS\n(Decide / Scale)"
    lbl_dogs = "PERROS\n(Desinvertir / Cosechar)" if lang == 'ES' else "DOGS\n(Divest / Harvest)"

    ax.text(1.60, 31.0, lbl_stars, fontsize=9.5, fontweight='bold', color='#1E40AF', ha='center', va='center', zorder=2)
    ax.text(1.60, -2.0, lbl_cows, fontsize=9.5, fontweight='bold', color='#0F766E', ha='center', va='center', zorder=2)
    ax.text(0.48, 31.0, lbl_quest, fontsize=9.5, fontweight='bold', color='#92400E', ha='center', va='center', zorder=2)
    ax.text(0.48, -2.0, lbl_dogs, fontsize=9.5, fontweight='bold', color='#9F1239', ha='center', va='center', zorder=2)

    # 4. Datos de las 8 UENs
    # (Nombre, CMR, TCM%, Ventas M€, Color borde, Color relleno, Texto etiqueta)
    uens = [
        ("Robótica IA", 1.25, 18.5, 18.5, '#1D4ED8', '#3B82F6', 'UEN-01: Robótica IA\n(18.5M€)' if lang == 'ES' else 'SBU-01: AI Robotics\n($18.5M)'),
        ("SaaS IoT", 1.16, 24.0, 12.2, '#1D4ED8', '#60A5FA', 'UEN-02: SaaS IoT\n(12.2M€)' if lang == 'ES' else 'SBU-02: IoT SaaS\n($12.2M)'),
        ("Hidráulicos", 2.00, 3.5, 32.0, '#0F766E', '#14B8A6', 'UEN-03: Hidráulicos\n(32.0M€)' if lang == 'ES' else 'SBU-03: Hydraulics\n($32.0M)'),
        ("Motores", 1.40, 2.0, 24.5, '#0F766E', '#2DD4BF', 'UEN-04: Motores\n(24.5M€)' if lang == 'ES' else 'SBU-04: Engines\n($24.5M)'),
        ("Baterías", 0.35, 32.0, 6.5, '#92400E', '#F59E0B', 'UEN-05: Baterías\n(6.5M€)' if lang == 'ES' else 'SBU-05: Batteries\n($6.5M)'),
        ("Láser Cuántico", 0.25, 21.0, 3.8, '#92400E', '#FBBF24', 'UEN-06: Láser\n(3.8M€)' if lang == 'ES' else 'SBU-06: Laser\n($3.8M)'),
        ("Cableado Cobre", 0.25, 1.0, 5.2, '#9F1239', '#F43F5E', 'UEN-07: Cableado\n(5.2M€)' if lang == 'ES' else 'SBU-07: Wiring\n($5.2M)'),
        ("Válvulas", 0.30, -1.5, 4.3, '#9F1239', '#FB7185', 'UEN-08: Válvulas\n(4.3M€)' if lang == 'ES' else 'SBU-08: Valves\n($4.3M)'),
    ]

    for uname, cmr, tcm, rev, edge_c, fill_c, lbl in uens:
        # Escala de tamaño proporcional a ventas
        size = rev * 32.0
        ax.scatter(cmr, tcm, s=size, color=fill_c, edgecolors=edge_c, linewidths=2.0, alpha=0.82, zorder=4)

        # Ajuste inteligente de etiquetas para evitar solapes
        offset_y = 2.4
        offset_x = 0.0
        if uname in ["Motores"]:
            offset_y = -3.2
        elif uname in ["Válvulas"]:
            offset_y = 2.4
        elif uname in ["Láser Cuántico"]:
            offset_y = -3.0
        elif uname in ["Robótica IA"]:
            offset_x = 0.12
            offset_y = -2.6

        ax.annotate(
            lbl,
            (cmr, tcm),
            xytext=(cmr + offset_x, tcm + offset_y),
            fontsize=7.2,
            fontweight='bold',
            color='#0F172A',
            ha='center',
            va='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#FFFFFF', edgecolor='#CBD5E1', alpha=0.90, linewidth=0.7),
            zorder=5
        )

    # Configuración de ejes
    ax.set_xlim(0.0, 2.2)
    ax.set_ylim(-5.0, 36.0)

    ax.set_xlabel("Cuota de Mercado Relativa (CMR) [Eje X]" if lang == 'ES' else "Relative Market Share (RMS) [X Axis]",
                  fontsize=9.0, fontweight='bold', color='#1E293B', labelpad=6)
    ax.set_ylabel("Tasa de Crecimiento del Mercado (%) [Eje Y]" if lang == 'ES' else "Market Growth Rate (%) [Y Axis]",
                  fontsize=9.0, fontweight='bold', color='#1E293B', labelpad=6)

    ax.tick_params(colors='#475569', labelsize=8)
    ax.grid(color='#E2E8F0', linestyle=':', linewidth=0.8, alpha=0.8, zorder=0)

    # Bordes del gráfico
    for spine in ax.spines.values():
        spine.set_color('#CBD5E1')
        spine.set_linewidth(1.0)

    plt.tight_layout()
    fig.savefig(out_path, dpi=220)
    plt.close(fig)
    return out_path


def add_header_banner(slide, kicker_text, badge_text, action_title, sub_text, badge_color=COLOR_NAVY_DARK):
    """Genera la cabecera ejecutiva formal de estándar McKinsey / BCG."""
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.05))
    banner.fill.solid()
    banner.fill.fore_color.rgb = COLOR_BLUE_ACCENT
    banner.line.fill.background()

    # Kicker
    k_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(8.5), Inches(0.28))
    tf_k = k_box.text_frame
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = kicker_text
    p_k.font.name = FONT_HEADING
    p_k.font.size = Pt(8.5)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_BLUE_ACCENT

    # Badge a la derecha
    b_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.833), Inches(0.44), Inches(2.7), Inches(0.32))
    b_shape.fill.solid()
    b_shape.fill.fore_color.rgb = badge_color
    b_shape.line.fill.background()
    tf_b = b_shape.text_frame
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = badge_text
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(8)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_WHITE
    p_b.alignment = PP_ALIGN.CENTER

    # Action Title (Pirámide de Minto)
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.733), Inches(0.58))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(17.5)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    # Subtítulo ejecutivo
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.36), Inches(11.733), Inches(0.26))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = sub_text
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(9.5)
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
    p_c.text = ("Datalaria.com | Executive Decision Pack • Documento Confidencial para Consejo de Administración"
               if lang == 'ES' else
               "Datalaria.com | Executive Decision Pack • Confidential Board of Directors Document")
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
    badge = "SÍNTESIS ESTRATÉGICA C-LEVEL" if lang == 'ES' else "C-SUITE PORTFOLIO SYNTHESIS"
    title = ("El 75% del flujo de caja del grupo depende de dos Vacas Lecheras en madurez: se requiere reasignar 3,6 M€ a dos Interrogantes y desinvertir en Perros antes de Q4"
             if lang == 'ES' else
             "75% of group cash flow depends on two mature Cash Cows: €3.6M liquidity reallocation to two Question Marks and Dog divestment required before Q4")
    sub = ("Diagnóstico cuantitativo de cartera (CMR vs. TCM), balance de liquidez de Bruce Henderson y roadmap de reasignación de capital."
           if lang == 'ES' else
           "Quantitative portfolio audit (RMS vs. MGR), Bruce Henderson cash flow balance, and board-level capital reallocation roadmap.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_NAVY_DARK)

    # 4 Tarjetas de Impacto alineadas
    cards_data = [
        {
            'tag': "CONCENTRACIÓN DE CARTERA" if lang == 'ES' else "PORTFOLIO CONCENTRATION",
            'metric': "52,8% Ventas" if lang == 'ES' else "52.8% Revenue",
            'submetric': "Alta Dependencia en Vacas" if lang == 'ES' else "High Dependency on Cows",
            'bullets': [
                "56,5 M€ en 2 líneas con crecimiento < 3.5%" if lang == 'ES' else "€56.5M in 2 lines with growth < 3.5%",
                "75% del FCF corporativo concentrado" if lang == 'ES' else "75% of corporate FCF highly concentrated",
                "Riesgo de obsolescencia a 5 años sin relevo" if lang == 'ES' else "5-year obsolescence risk without pipeline"
            ],
            'pill': "RIESGO ESTRUCTURAL" if lang == 'ES' else "STRUCTURAL RISK",
            'color_theme': COLOR_AMBER_ACCENT,
            'bg_color': COLOR_AMBER_BG,
            'border_color': COLOR_AMBER_BORDER,
            'text_color': COLOR_AMBER_TEXT
        },
        {
            'tag': "BALANCE NETO DE LIQUIDEZ" if lang == 'ES' else "NET LIQUIDITY BALANCE",
            'metric': "+5,29 M€ FCF" if lang == 'ES' else "+€5.29M FCF",
            'submetric': "Superávit de Fondos Saludable" if lang == 'ES' else "Healthy Cash Surplus",
            'bullets': [
                "Vacas generan +8,05 M€ de FCF anual" if lang == 'ES' else "Cash Cows generate +€8.05M annual FCF",
                "Interrogantes absorben -3,60 M€ en I+D" if lang == 'ES' else "Question Marks absorb -€3.60M in scaling",
                "Excedente de +4,45 M€ listo para reasignar" if lang == 'ES' else "Net €4.45M surplus ready for allocation"
            ],
            'pill': "FINANCIACIÓN ASEGURADA" if lang == 'ES' else "FUNDING SECURED",
            'color_theme': COLOR_TEAL_ACCENT,
            'bg_color': COLOR_TEAL_BG,
            'border_color': COLOR_TEAL_BORDER,
            'text_color': COLOR_TEAL_TEXT
        },
        {
            'tag': "TRAMPAS DE CAPITAL EN PERROS" if lang == 'ES' else "CAPITAL TRAPS IN DOGS",
            'metric': "9,5 M€ Ventas" if lang == 'ES' else "€9.5M Revenue",
            'submetric': "Activos Atrapados sin Retorno" if lang == 'ES' else "Trapped Low-Return Assets",
            'bullets': [
                "2 UENs (Cableado y Válvulas) con CMR < 0.3x" if lang == 'ES' else "2 SBUs (Wiring & Valves) with RMS < 0.3x",
                "FCF negativo (-90k€) y erosión de margen" if lang == 'ES' else "Negative FCF (-€90k) and margin drag",
                "Distracción directiva con ROIC < WACC" if lang == 'ES' else "Executive distraction with ROIC < WACC"
            ],
            'pill': "DESINVERSIÓN OBLIGADA" if lang == 'ES' else "DIVESTMENT MANDATE",
            'color_theme': COLOR_ROSE_ACCENT,
            'bg_color': COLOR_ROSE_BG,
            'border_color': COLOR_ROSE_BORDER,
            'text_color': COLOR_ROSE_TEXT
        },
        {
            'tag': "RETORNO DE REASIGNACIÓN" if lang == 'ES' else "REALLOCATION ROIC",
            'metric': "+320 bps ROIC" if lang == 'ES' else "+320 bps ROIC",
            'submetric': "+4,45 M€ EBITDA Adicional" if lang == 'ES' else "+€4.45M Additional EBITDA",
            'bullets': [
                "Baterías (UEN-05) escala a Estrella (CMR > 1.05x)" if lang == 'ES' else "Batteries (SBU-05) scales to Star (RMS > 1.05x)",
                "Venta de Cableado libera 3,2 M€ de liquidez" if lang == 'ES' else "Wiring carve-out unlocks €3.2M cash",
                "Payback del programa estimado en 18 meses" if lang == 'ES' else "Program payback achieved in 18 months"
            ],
            'pill': "CREACIÓN DE VALOR" if lang == 'ES' else "VALUE ACCRETION",
            'color_theme': COLOR_BLUE_ACCENT,
            'bg_color': COLOR_BLUE_BG,
            'border_color': COLOR_BLUE_BORDER,
            'text_color': COLOR_BLUE_TEXT
        }
    ]

    card_w = Inches(2.78)
    card_h = Inches(5.15)
    start_x = Inches(0.8)
    start_y = Inches(1.68)
    spacing = Inches(0.20)

    for idx, card in enumerate(cards_data):
        curr_x = start_x + idx * (card_w + spacing)

        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, start_y, card_w, card_h)
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_CARD_BG
        box.line.color.rgb = COLOR_BORDER
        box.line.width = Pt(1.5)

        # Barra superior de acento
        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x + Inches(0.12), start_y + Inches(0.12), card_w - Inches(0.24), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = card['color_theme']
        bar.line.fill.background()

        # Tag
        t_box = slide.shapes.add_textbox(curr_x + Inches(0.15), start_y + Inches(0.28), card_w - Inches(0.3), Inches(0.28))
        tf_tag = t_box.text_frame
        tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = card['tag']
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_TEXT_MUTED
        p_tag.alignment = PP_ALIGN.CENTER

        # Métrica principal
        m_box = slide.shapes.add_textbox(curr_x + Inches(0.10), start_y + Inches(0.60), card_w - Inches(0.2), Inches(0.60))
        tf_m = m_box.text_frame
        tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
        p_m = tf_m.paragraphs[0]
        p_m.text = card['metric']
        p_m.font.name = FONT_HEADING
        p_m.font.size = Pt(21)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_NAVY_DARK
        p_m.alignment = PP_ALIGN.CENTER

        # Submétrica
        s_box = slide.shapes.add_textbox(curr_x + Inches(0.15), start_y + Inches(1.24), card_w - Inches(0.3), Inches(0.35))
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
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, curr_x + Inches(0.2), start_y + Inches(1.68), card_w - Inches(0.4), Inches(0.015))
        div.fill.solid()
        div.fill.fore_color.rgb = card['border_color']
        div.line.fill.background()

        # Viñetas
        b_box = slide.shapes.add_textbox(curr_x + Inches(0.18), start_y + Inches(1.80), card_w - Inches(0.36), Inches(2.6))
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
            p_bullet.space_after = Pt(12)

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
# SLIDE 2: EVIDENCIA CUANTITATIVA & GRÁFICO DE BURBUJAS
# ==============================================================================
def build_slide2(prs, lang='ES'):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    kicker = "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD"
    badge = "EVIDENCIA CUANTITATIVA & BURBUJAS" if lang == 'ES' else "QUANTITATIVE EVIDENCE & BUBBLE CHART"
    title = ("La dispersión de las 8 UENs evidencia polarización: 2 Estrellas en aceleración, 2 Vacas masivas y 2 Interrogantes que exigen resolución binaria"
             if lang == 'ES' else
             "The 8 SBU scatter reveals sharp polarization: 2 accelerating Stars, 2 massive Cash Cows, and 2 Question Marks demanding binary resolution")
    sub = ("Matriz cartesiana de cuota relativa vs. crecimiento del mercado y desglose financiero de los 4 cuadrantes estratégicos."
           if lang == 'ES' else
           "Cartesian matrix of relative share vs. market growth and financial breakdown across the 4 strategic quadrants.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_BLUE_ACCENT)

    # CONTENEDOR IZQUIERDO: GRÁFICO DE BURBUJAS (X: 0.8", W: 5.7", H: 5.15")
    left_x = Inches(0.8)
    cont_y = Inches(1.68)
    left_w = Inches(5.7)
    cont_h = Inches(5.15)

    left_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, cont_y, left_w, cont_h)
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = COLOR_CARD_BG
    left_box.line.color.rgb = COLOR_BORDER
    left_box.line.width = Pt(1.5)

    t_left = slide.shapes.add_textbox(left_x + Inches(0.2), cont_y + Inches(0.12), left_w - Inches(0.4), Inches(0.30))
    tf_tl = t_left.text_frame
    tf_tl.margin_left = tf_tl.margin_right = tf_tl.margin_top = tf_tl.margin_bottom = 0
    p_tl = tf_tl.paragraphs[0]
    p_tl.text = "MATRIZ CARTESIANA BCG (CMR vs. TCM) • ESCALA POR VENTAS" if lang == 'ES' else "CARTESIAN BCG MATRIX (RMS vs. MGR) • SIZED BY REVENUE"
    p_tl.font.name = FONT_HEADING
    p_tl.font.size = Pt(10)
    p_tl.font.bold = True
    p_tl.font.color.rgb = COLOR_NAVY_DARK
    p_tl.alignment = PP_ALIGN.CENTER

    img_chart_path = create_bubble_chart_image(lang=lang, out_path=f"temp_bcg_bubble_{lang}.png")
    slide.shapes.add_picture(img_chart_path, left_x + Inches(0.35), cont_y + Inches(0.46), width=Inches(5.0))

    cap_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x + Inches(0.3), cont_y + cont_h - Inches(0.60), left_w - Inches(0.6), Inches(0.45))
    cap_box.fill.solid()
    cap_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    cap_box.line.fill.background()
    tf_cap = cap_box.text_frame
    tf_cap.margin_left = tf_cap.margin_right = tf_cap.margin_top = tf_cap.margin_bottom = 0
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = ("Total Cartera: 107,0 M€ Facturación • 18,98 M€ EBITDA (17,7%) • +5,29 M€ FCF Neto"
                  if lang == 'ES' else
                  "Portfolio Total: €107.0M Revenue • €18.98M EBITDA (17.7%) • +€5.29M Net FCF")
    p_cap.font.name = FONT_HEADING
    p_cap.font.size = Pt(8.5)
    p_cap.font.bold = True
    p_cap.font.color.rgb = COLOR_WHITE
    p_cap.alignment = PP_ALIGN.CENTER

    # CONTENEDOR DERECHO: 4 TARJETAS DE CUADRANTES ESTRATÉGICOS
    right_x = Inches(6.75)
    right_w = Inches(5.78)

    quadrant_blocks = [
        {
            'badge': "⭐ ESTRELLAS (2 UENs | 30,7 M€ | 28,7% Cartera | +0,93 M€ FCF)" if lang == 'ES' else "⭐ STARS (2 SBUs | €30.7M | 28.7% Portfolio | +€0.93M FCF)",
            'title': "Robótica Visión IA (18.5M€, CMR 1.25x) & SaaS IoT (12.2M€, CMR 1.16x)" if lang == 'ES' else "AI Vision Robotics (€18.5M, RMS 1.25x) & IoT SaaS (€12.2M, RMS 1.16x)",
            'bullets': [
                "Crecimiento medio de mercado superior al 21% anual con EBITDA del 23.2%" if lang == 'ES' else "Average market growth exceeding 21% annually with 23.2% EBITDA margin",
                "Prescripción C-Level: Invertir 2,05 M€ para blindar cuota antes de la fase de madurez" if lang == 'ES' else "C-Level Prescription: Invest €2.05M to defend share ahead of market maturity"
            ],
            'color': COLOR_BLUE_ACCENT,
            'bg': COLOR_BLUE_BG,
            'border': COLOR_BLUE_BORDER,
            'h': Inches(1.15)
        },
        {
            'badge': "🐄 VACAS LECHERAS (2 UENs | 56,5 M€ | 52,8% Cartera | +8,05 M€ FCF)" if lang == 'ES' else "🐄 CASH COWS (2 SBUs | €56.5M | 52.8% Portfolio | +€8.05M FCF)",
            'title': "Sistemas Hidráulicos (32M€, CMR 2.0x) & Motores Combustión (24.5M€, CMR 1.4x)" if lang == 'ES' else "Hydraulics (€32M, RMS 2.0x) & Industrial Engines (€24.5M, RMS 1.4x)",
            'bullets': [
                "Generan el 75% del flujo libre de caja corporativo con economías de escala consolidadas" if lang == 'ES' else "Generate 75% of corporate FCF with deep scale-driven cost leadership",
                "Prescripción C-Level: Ordeño disciplinado; congelar CAPEX expansivo y extraer 5,7 M€" if lang == 'ES' else "C-Level Prescription: Disciplined milking; freeze non-critical CAPEX and extract €5.7M"
            ],
            'color': COLOR_TEAL_ACCENT,
            'bg': COLOR_TEAL_BG,
            'border': COLOR_TEAL_BORDER,
            'h': Inches(1.15)
        },
        {
            'badge': "❓ INTERROGANTES (2 UENs | 10,3 M€ | 9,6% Cartera | -3,60 M€ FCF)" if lang == 'ES' else "❓ QUESTION MARKS (2 SBUs | €10.3M | 9.6% Portfolio | -€3.60M FCF)",
            'title': "Baterías Estado Sólido (6.5M€, CMR 0.35x) & Láser Cuántico (3.8M€, CMR 0.25x)" if lang == 'ES' else "Solid-State Batteries (€6.5M, RMS 0.35x) & Laser Systems (€3.8M, RMS 0.25x)",
            'bullets': [
                "Mercados en hipercrecimiento (+26% TCM) pero alta desventaja de costes frente a líderes" if lang == 'ES' else "Hypergrowth markets (+26% MGR) but substantial cost penalty vs. leaders",
                "Prescripción C-Level: Decisión binaria; concentrar 2,8 M€ en Baterías y desinvertir Láser" if lang == 'ES' else "C-Level Prescription: Binary decision; fund Batteries with €2.8M and carve out Laser"
            ],
            'color': COLOR_AMBER_ACCENT,
            'bg': COLOR_AMBER_BG,
            'border': COLOR_AMBER_BORDER,
            'h': Inches(1.15)
        },
        {
            'badge': "🐕 PERROS (2 UENs | 9,5 M€ | 8,9% Cartera | -0,09 M€ FCF)" if lang == 'ES' else "🐕 DOGS (2 SBUs | €9.5M | 8.9% Portfolio | -€0.09M FCF)",
            'title': "Cableado Convencional (5.2M€, CMR 0.25x) & Válvulas Analógicas (4.3M€, CMR 0.30x)" if lang == 'ES' else "Conventional Wiring (€5.2M, RMS 0.25x) & Analog Valves (€4.3M, RMS 0.30x)",
            'bullets': [
                "Baja cuota en sectores en declive o estancados; drenan 2,8 M€ en capital circulante" if lang == 'ES' else "Low share in stagnant or declining sectors; drain €2.8M in working capital",
                "Prescripción C-Level: Mandato de venta de Cableado por 3,2 M€ y cosecha/cierre de Válvulas" if lang == 'ES' else "C-Level Prescription: M&A mandate to sell Wiring for €3.2M and harvest/sunset Valves"
            ],
            'color': COLOR_ROSE_ACCENT,
            'bg': COLOR_ROSE_BG,
            'border': COLOR_ROSE_BORDER,
            'h': Inches(1.15)
        },
    ]

    curr_y = cont_y
    for qb in quadrant_blocks:
        q_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, curr_y, right_w, qb['h'])
        q_box.fill.solid()
        q_box.fill.fore_color.rgb = qb['bg']
        q_box.line.color.rgb = qb['border']
        q_box.line.width = Pt(1.2)

        # Badge
        b_tag = slide.shapes.add_textbox(right_x + Inches(0.15), curr_y + Inches(0.06), right_w - Inches(0.3), Inches(0.24))
        tf_bt = b_tag.text_frame
        tf_bt.margin_left = tf_bt.margin_right = tf_bt.margin_top = tf_bt.margin_bottom = 0
        p_bt = tf_bt.paragraphs[0]
        p_bt.text = qb['badge']
        p_bt.font.name = FONT_HEADING
        p_bt.font.size = Pt(8.5)
        p_bt.font.bold = True
        p_bt.font.color.rgb = qb['color']

        # Title
        t_tag = slide.shapes.add_textbox(right_x + Inches(0.15), curr_y + Inches(0.28), right_w - Inches(0.3), Inches(0.26))
        tf_tt = t_tag.text_frame
        tf_tt.margin_left = tf_tt.margin_right = tf_tt.margin_top = tf_tt.margin_bottom = 0
        p_tt = tf_tt.paragraphs[0]
        p_tt.text = qb['title']
        p_tt.font.name = FONT_HEADING
        p_tt.font.size = Pt(9.5)
        p_tt.font.bold = True
        p_tt.font.color.rgb = COLOR_NAVY_DARK

        # Bullets
        bl_tag = slide.shapes.add_textbox(right_x + Inches(0.15), curr_y + Inches(0.52), right_w - Inches(0.3), Inches(0.55))
        tf_bl = bl_tag.text_frame
        tf_bl.word_wrap = True
        tf_bl.margin_left = tf_bl.margin_right = tf_bl.margin_top = tf_bl.margin_bottom = 0

        for b_idx, bullet in enumerate(qb['bullets']):
            p_bl = tf_bl.paragraphs[0] if b_idx == 0 else tf_bl.add_paragraph()
            p_bl.text = f"• {bullet}"
            p_bl.font.name = FONT_BODY
            p_bl.font.size = Pt(8.5)
            p_bl.font.color.rgb = COLOR_TEXT_MAIN
            p_bl.space_after = Pt(2)

        curr_y += qb['h'] + Inches(0.16)

    # Limpieza de imagen temporal
    if os.path.exists(img_chart_path):
        try:
            os.remove(img_chart_path)
        except Exception:
            pass

    add_footer(slide, 2, 3, lang=lang)


# ==============================================================================
# SLIDE 3: ROADMAP DE CAPITAL & BOARD DECISION GATEWAY
# ==============================================================================
def build_slide3(prs, lang='ES'):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    kicker = "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD"
    badge = "ROADMAP DE CAPITAL & GOBERNANZA" if lang == 'ES' else "CAPITAL ROADMAP & GOVERNANCE"
    title = ("El plan de capital 2026 reasigna 3,6 M€ de Vacas a Crecimiento y desbloquea 3,8 M€ mediante desinversión de Perros con aprobación del Consejo"
             if lang == 'ES' else
             "The 2026 capital roadmap reallocates €3.6M from Cash Cows to Growth and unlocks €3.8M via Dog divestment subject to Board approval")
    sub = ("Cronograma Q1-Q4 de reasignación presupuestaria y resoluciones vinculantes sometidas a votación del Consejo de Administración."
           if lang == 'ES' else
           "Q1-Q4 capital reallocation timeline and formal binding resolutions submitted for Board of Directors voting.")

    add_header_banner(slide, kicker, badge, title, sub, badge_color=COLOR_AMBER_ACCENT)

    # MITAD SUPERIOR: 4 WORKSTREAMS DE ASIGNACIÓN (Y: 1.68", H: 2.35")
    start_y = Inches(1.68)
    ws_w = Inches(2.78)
    ws_h = Inches(2.35)
    spacing = Inches(0.20)
    start_x = Inches(0.8)

    workstreams = [
        {
            'ws_num': "WS-1: ESTRELLAS (CAPEX)" if lang == 'ES' else "WS-1: STARS (CAPEX)",
            'owner': "COO & CTO • Q1-Q3" if lang == 'ES' else "COO & CTO • Q1-Q3",
            'budget': "+2.050.000 €" if lang == 'ES' else "+€2,050,000",
            'bullets': [
                "Ampliación fabril en Robótica Visión IA" if lang == 'ES' else "Robotics capacity scale-up in AI Vision",
                "Conectores de red en Plataforma IoT SaaS" if lang == 'ES' else "Network connectors in IoT SaaS Platform",
                "Meta: CMR > 1.35x frente al líder competidor" if lang == 'ES' else "Goal: RMS > 1.35x vs. nearest competitor"
            ],
            'color': COLOR_BLUE_ACCENT,
            'bg': COLOR_BLUE_BG,
            'border': COLOR_BLUE_BORDER,
            'text_c': COLOR_BLUE_TEXT
        },
        {
            'ws_num': "WS-2: INTERROGANTES" if lang == 'ES' else "WS-2: QUESTION MARKS",
            'owner': "CEO & CBO • Q1-Q4" if lang == 'ES' else "CEO & CBO • Q1-Q4",
            'budget': "+2.400.000 € Netos" if lang == 'ES' else "+€2,400,000 Net",
            'bullets': [
                "Inyección de 2,8 M€ en Baterías Estado Sólido" if lang == 'ES' else "€2.8M capital push into Solid-State Batteries",
                "Búsqueda de socio JV en Sensorización Láser" if lang == 'ES' else "Target strategic JV partner for Laser Systems",
                "Meta: Cruzar a Estrella (CMR 1.05x) en Q4" if lang == 'ES' else "Goal: Cross to Star (RMS 1.05x) in Q4"
            ],
            'color': COLOR_AMBER_ACCENT,
            'bg': COLOR_AMBER_BG,
            'border': COLOR_AMBER_BORDER,
            'text_c': COLOR_AMBER_TEXT
        },
        {
            'ws_num': "WS-3: VACAS (ORDEÑO)" if lang == 'ES' else "WS-3: CASH COWS (MILK)",
            'owner': "CFO & COO • Q1-Q4" if lang == 'ES' else "CFO & COO • Q1-Q4",
            'budget': "-5.700.000 € Extraídos" if lang == 'ES' else "-€5,700,000 Extracted",
            'bullets': [
                "Extracción disciplinada de 8,05 M€ FCF" if lang == 'ES' else "Disciplined extraction of €8.05M FCF",
                "Congelar CAPEX expansivo en Hidráulicos" if lang == 'ES' else "Freeze non-critical CAPEX in Hydraulics",
                "Optimizar capital circulante en Motores" if lang == 'ES' else "Lean working capital program in Engines"
            ],
            'color': COLOR_TEAL_ACCENT,
            'bg': COLOR_TEAL_BG,
            'border': COLOR_TEAL_BORDER,
            'text_c': COLOR_TEAL_TEXT
        },
        {
            'ws_num': "WS-4: PERROS (VENTA)" if lang == 'ES' else "WS-4: DOGS (DIVEST)",
            'owner': "M&A Lead • Q2-Q3" if lang == 'ES' else "M&A Lead • Q2-Q3",
            'budget': "-3.850.000 € Liberados" if lang == 'ES' else "-€3,850,000 Unlocked",
            'bullets': [
                "Venta de unidad de Cableado por 3,2 M€" if lang == 'ES' else "Carve-out sale of Wiring unit for €3.2M",
                "Cosecha y cierre ordenado de Válvulas" if lang == 'ES' else "Orderly harvest and sunset of Valves unit",
                "Meta: Liberar circulante y eliminar pérdidas" if lang == 'ES' else "Goal: Eliminate cash drag and release cash"
            ],
            'color': COLOR_ROSE_ACCENT,
            'bg': COLOR_ROSE_BG,
            'border': COLOR_ROSE_BORDER,
            'text_c': COLOR_ROSE_TEXT
        }
    ]

    for idx, ws_item in enumerate(workstreams):
        curr_x = start_x + idx * (ws_w + spacing)

        ws_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, start_y, ws_w, ws_h)
        ws_box.fill.solid()
        ws_box.fill.fore_color.rgb = COLOR_CARD_BG
        ws_box.line.color.rgb = COLOR_BORDER
        ws_box.line.width = Pt(1.5)

        # Barra superior
        top_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x + Inches(0.1), start_y + Inches(0.08), ws_w - Inches(0.2), Inches(0.05))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = ws_item['color']
        top_bar.line.fill.background()

        # WS Num
        h_box = slide.shapes.add_textbox(curr_x + Inches(0.12), start_y + Inches(0.16), ws_w - Inches(0.24), Inches(0.26))
        tf_h = h_box.text_frame
        tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        p_h.text = ws_item['ws_num']
        p_h.font.name = FONT_HEADING
        p_h.font.size = Pt(8.5)
        p_h.font.bold = True
        p_h.font.color.rgb = ws_item['text_c']
        p_h.alignment = PP_ALIGN.CENTER

        # Presupuesto
        b_box = slide.shapes.add_textbox(curr_x + Inches(0.10), start_y + Inches(0.42), ws_w - Inches(0.20), Inches(0.38))
        tf_bud = b_box.text_frame
        tf_bud.margin_left = tf_bud.margin_right = tf_bud.margin_top = tf_bud.margin_bottom = 0
        p_bud = tf_bud.paragraphs[0]
        p_bud.text = ws_item['budget']
        p_bud.font.name = FONT_HEADING
        p_bud.font.size = Pt(13)
        p_bud.font.bold = True
        p_bud.font.color.rgb = COLOR_NAVY_DARK
        p_bud.alignment = PP_ALIGN.CENTER

        # Owner & Timeline
        o_box = slide.shapes.add_textbox(curr_x + Inches(0.12), start_y + Inches(0.80), ws_w - Inches(0.24), Inches(0.24))
        tf_o = o_box.text_frame
        tf_o.margin_left = tf_o.margin_right = tf_o.margin_top = tf_o.margin_bottom = 0
        p_o = tf_o.paragraphs[0]
        p_o.text = ws_item['owner']
        p_o.font.name = FONT_HEADING
        p_o.font.size = Pt(8.2)
        p_o.font.bold = True
        p_o.font.color.rgb = COLOR_TEXT_MUTED
        p_o.alignment = PP_ALIGN.CENTER

        # Viñetas
        bl_box = slide.shapes.add_textbox(curr_x + Inches(0.14), start_y + Inches(1.08), ws_w - Inches(0.28), Inches(1.15))
        tf_b = bl_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for b_idx, bullet in enumerate(ws_item['bullets']):
            p_bullet = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p_bullet.text = f"• {bullet}"
            p_bullet.font.name = FONT_BODY
            p_bullet.font.size = Pt(8.5)
            p_bullet.font.color.rgb = COLOR_TEXT_MAIN
            p_bullet.space_after = Pt(4)

    # MITAD INFERIOR: BOARD DECISION GATEWAY (Y: 4.22", H: 2.65")
    gate_y = Inches(4.20)
    gate_h = Inches(2.65)
    gate_w = Inches(11.733)

    gate_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, gate_y, gate_w, gate_h)
    gate_box.fill.solid()
    gate_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    gate_box.line.color.rgb = COLOR_GOLD
    gate_box.line.width = Pt(2.0)

    # Cabecera del Gateway
    gt_box = slide.shapes.add_textbox(start_x + Inches(0.3), gate_y + Inches(0.15), gate_w - Inches(0.6), Inches(0.32))
    tf_gt = gt_box.text_frame
    tf_gt.margin_left = tf_gt.margin_right = tf_gt.margin_top = tf_gt.margin_bottom = 0
    p_gt = tf_gt.paragraphs[0]
    p_gt.text = ("DECISIÓN REQUERIDA DEL CONSEJO DE ADMINISTRACIÓN • BOARD DECISION GATEWAY"
                 if lang == 'ES' else
                 "BOARD OF DIRECTORS FORMAL DECISION GATEWAY • BINDING RESOLUTIONS")
    p_gt.font.name = FONT_HEADING
    p_gt.font.size = Pt(11.5)
    p_gt.font.bold = True
    p_gt.font.color.rgb = COLOR_GOLD
    p_gt.alignment = PP_ALIGN.CENTER

    # 3 Resoluciones Formales
    resolutions = [
        {
            'num': "RESOLUCIÓN 1 (CAPEX INTERROGANTE)" if lang == 'ES' else "RESOLUTION 1 (QUESTION MARK CAPEX)",
            'text': ("Aprobar la inyección extraordinaria de 2.800.000 € de liquidez proveniente del superávit de Sistemas Hidráulicos (Vaca) hacia la escala fabril de Baterías de Estado Sólido (UEN-05) para alcanzar CMR ≥ 1.05x antes de Q4 2026."
                     if lang == 'ES' else
                     "Approve the extraordinary reallocation of €2,800,000 in liquidity generated by Hydraulics (Cash Cow) to scale Solid-State Batteries (SBU-05) manufacturing capacity to reach RMS ≥ 1.05x before Q4 2026.")
        },
        {
            'num': "RESOLUCIÓN 2 (MANDATO M&A PERRO)" if lang == 'ES' else "RESOLUTION 2 (DOG M&A MANDATE)",
            'text': ("Autorizar formalmente al CFO y Director de M&A a otorgar mandato exclusivo de venta para la desinversión de la unidad de Cableado Convencional (UEN-07), estableciendo un precio suelo de reserva de 3.200.000 € en caja limpia."
                     if lang == 'ES' else
                     "Authorize the CFO and M&A Lead to grant an exclusive sale mandate for the carve-out divestment of Conventional Wiring (SBU-07), establishing a firm floor reserve price of €3,200,000 in net cash.")
        },
        {
            'num': "RESOLUCIÓN 3 (AUDITORÍA DE CMR TRIMESTRAL)" if lang == 'ES' else "RESOLUTION 3 (QUARTERLY RMS AUDIT)",
            'text': ("Instaurar un Comité de Supervisión de Cuota de Mercado Relativa (CMR) con reporte ejecutivo obligatorio cada 90 días ante el Consejo, auditando el cumplimiento de la regla dorada de balance de caja de Henderson."
                     if lang == 'ES' else
                     "Establish a Quarterly Relative Market Share (RMS) Governance Committee with mandatory 90-day executive reporting to the Board, auditing strict adherence to Bruce Henderson's cash balance golden rule.")
        }
    ]

    res_w = Inches(3.64)
    res_spacing = Inches(0.20)
    res_y = gate_y + Inches(0.55)

    for r_idx, res in enumerate(resolutions):
        rx = start_x + Inches(0.3) + r_idx * (res_w + res_spacing)

        r_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, res_y, res_w, Inches(1.85))
        r_card.fill.solid()
        r_card.fill.fore_color.rgb = COLOR_NAVY_MED
        r_card.line.color.rgb = COLOR_BORDER
        r_card.line.width = Pt(1.0)

        r_num_box = slide.shapes.add_textbox(rx + Inches(0.12), res_y + Inches(0.10), res_w - Inches(0.24), Inches(0.25))
        tf_rn = r_num_box.text_frame
        tf_rn.margin_left = tf_rn.margin_right = tf_rn.margin_top = tf_rn.margin_bottom = 0
        p_rn = tf_rn.paragraphs[0]
        p_rn.text = res['num']
        p_rn.font.name = FONT_HEADING
        p_rn.font.size = Pt(8.5)
        p_rn.font.bold = True
        p_rn.font.color.rgb = COLOR_GOLD

        r_txt_box = slide.shapes.add_textbox(rx + Inches(0.12), res_y + Inches(0.38), res_w - Inches(0.24), Inches(1.35))
        tf_rt = r_txt_box.text_frame
        tf_rt.word_wrap = True
        tf_rt.margin_left = tf_rt.margin_right = tf_rt.margin_top = tf_rt.margin_bottom = 0
        p_rt = tf_rt.paragraphs[0]
        p_rt.text = res['text']
        p_rt.font.name = FONT_BODY
        p_rt.font.size = Pt(8.5)
        p_rt.font.color.rgb = COLOR_WHITE

    add_footer(slide, 3, 3, lang=lang)


# ==============================================================================
# GENERACIÓN DE PRESENTACIONES DUAL (ES & EN)
# ==============================================================================
def generate_presentation(lang='ES', out_path='Presentacion_BCG_CLevel_ES.pptx'):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide1(prs, lang=lang)
    build_slide2(prs, lang=lang)
    build_slide3(prs, lang=lang)

    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    prs.save(out_path)
    print(f"[OK] Presentación C-Level generada exitosamente: {out_path}")


def main():
    dir_packages = "packages"
    dir_es = os.path.join(dir_packages, "[ES]_BCG_Dinamica")
    dir_en = os.path.join(dir_packages, "[EN]_Dynamic_BCG")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    file_es = os.path.join(dir_es, "Presentacion_BCG_CLevel_ES.pptx")
    file_en = os.path.join(dir_en, "Deck_BCG_CLevel_EN.pptx")

    generate_presentation(lang='ES', out_path=file_es)
    generate_presentation(lang='EN', out_path=file_en)


if __name__ == "__main__":
    main()
