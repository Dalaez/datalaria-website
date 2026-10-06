#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[ES]_Matriz_RICE_ICE/Presentacion_RICE_ICE_CLevel_ES.pptx
2. packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[EN]_RICE_ICE_Matrix/Deck_RICE_ICE_CLevel_EN.pptx

Características de diseño Tier-1 (McKinsey / BCG / Intercom):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Pirámide de Minto y Action Titles contundentes.
- Diapositiva 1: Síntesis Ejecutiva & Veredicto de Priorización (4 KPI Cards y fundamentos de concentración de valor).
- Diapositiva 2: Evidencia Cuantitativa (Matriz 2x2 Impacto/Esfuerzo en alta resolución, Tabla Top RICE y Experimentos ICE).
- Diapositiva 3: Roadmap Now/Next/Later & Product Council Decision Gateway (4 acuerdos vinculantes y bloque de 4 firmas C-Level).
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
from pptx.oxml import parse_xml

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = RGBColor(15, 23, 42)       # Slate 900
COLOR_NAVY_MED = RGBColor(30, 41, 59)        # Slate 800
COLOR_BLUE_ACCENT = RGBColor(37, 99, 235)    # Blue 600
COLOR_BLUE_LIGHT = RGBColor(239, 246, 255)   # Blue 50

# Estados y Acentos
COLOR_GREEN_BG = RGBColor(209, 250, 229)     # Verde suave
COLOR_GREEN_BORDER = RGBColor(16, 185, 129)  # Verde acento
COLOR_GREEN_TEXT = RGBColor(6, 95, 70)       # Verde texto

COLOR_AMBER_BG = RGBColor(254, 243, 199)     # Ámbar suave
COLOR_AMBER_BORDER = RGBColor(245, 158, 11)  # Ámbar acento
COLOR_AMBER_TEXT = RGBColor(146, 64, 14)     # Ámbar texto

COLOR_RED_BG = RGBColor(254, 226, 226)       # Rojo suave
COLOR_RED_BORDER = RGBColor(239, 68, 68)     # Rojo acento
COLOR_RED_TEXT = RGBColor(153, 27, 27)       # Rojo texto

COLOR_TEXT_MAIN = RGBColor(51, 65, 85)       # Slate 700
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # Slate 500
COLOR_CARD_BG = RGBColor(248, 250, 252)      # Slate 50
COLOR_BORDER = RGBColor(226, 232, 240)       # Slate 200
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"


def apply_gradient_fill(shape, color1_hex, color2_hex, angle_deg=90):
    """Aplica un degradado lineal nativo DrawingML a una forma de python-pptx."""
    spPr = shape._element.spPr
    for child in list(spPr):
        if child.tag.endswith('solidFill') or child.tag.endswith('gradFill'):
            spPr.remove(child)
    ang_val = int(angle_deg * 60000)
    grad_xml = (
        f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" flip="none" rotWithShape="1">'
        f'  <a:gsLst>'
        f'    <a:gs pos="0"><a:srgbClr val="{color1_hex}"/></a:gs>'
        f'    <a:gs pos="100000"><a:srgbClr val="{color2_hex}"/></a:gs>'
        f'  </a:gsLst>'
        f'  <a:lin ang="{ang_val}" scaled="1"/>'
        f'</a:gradFill>'
    )
    spPr.append(parse_xml(grad_xml))


def create_impact_effort_chart(lang='ES', out_path='temp_rice_matrix.png'):
    """Genera la Matriz 2x2 Impacto vs. Esfuerzo en alta resolución."""
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=220)

    # Coordenadas: Esfuerzo (X) vs Valor Esperado (Y)
    # Medianas de referencia: Esfuerzo mediana = 2.5 PM, Valor mediana = 15,000
    x_med = 2.5
    y_med = 15000

    # Cuadrantes de fondo
    ax.axvspan(0, x_med, ymin=y_med/50000, ymax=1.0, color='#F0FDF4', alpha=0.7)  # Quick Wins (top-left)
    ax.axvspan(x_med, 15, ymin=y_med/50000, ymax=1.0, color='#EFF6FF', alpha=0.7) # Big Bets (top-right)
    ax.axvspan(0, x_med, ymin=0, ymax=y_med/50000, color='#F8FAFC', alpha=0.7)     # Fill-ins (bottom-left)
    ax.axvspan(x_med, 15, ymin=0, ymax=y_med/50000, color='#FEF2F2', alpha=0.7)    # Money Pits (bottom-right)

    # Líneas de corte
    ax.axvline(x=x_med, color='#94A3B8', linestyle='--', linewidth=1.2)
    ax.axhline(y=y_med, color='#94A3B8', linestyle='--', linewidth=1.2)

    # Títulos de cuadrantes
    lbl_qw = "QUICK WINS\n(Alto Valor, Bajo Esfuerzo)" if lang == 'ES' else "QUICK WINS\n(High Value, Low Effort)"
    lbl_bb = "GRANDES APUESTAS\n(Alto Valor, Alto Esfuerzo)" if lang == 'ES' else "BIG BETS\n(High Value, High Effort)"
    lbl_fi = "RELLENOS\n(Bajo Valor, Bajo Esfuerzo)" if lang == 'ES' else "FILL-INS\n(Low Value, Low Effort)"
    lbl_mp = "POZOS SIN FONDO\n(Bajo Valor, Alto Esfuerzo)" if lang == 'ES' else "MONEY PITS\n(Low Value, High Effort)"

    ax.text(0.3, 44000, lbl_qw, fontsize=8.5, fontweight='bold', color='#166534')
    ax.text(7.5, 44000, lbl_bb, fontsize=8.5, fontweight='bold', color='#1E40AF')
    ax.text(0.3, 3000, lbl_fi, fontsize=8.5, fontweight='bold', color='#475569')
    ax.text(7.5, 3000, lbl_mp, fontsize=8.5, fontweight='bold', color='#991B1B')

    # Puntos de iniciativas
    initiatives = [
        # (Nombre, Esfuerzo, Valor, Color, Cuadrante)
        ("INIT-18 (2FA Auth)", 1.5, 50000, '#10B981', 'QW'),
        ("INIT-15 (NPS Pulse)", 1.0, 25000, '#10B981', 'QW'),
        ("INIT-03 (Exporter)", 1.0, 22000, '#10B981', 'QW'),
        ("INIT-05 (Onboarding)", 1.5, 30000, '#10B981', 'QW'),
        ("INIT-01 (SSO SAML)", 2.0, 17000, '#10B981', 'QW'),
        ("INIT-02 (AI Copilot)", 6.0, 43200, '#2563EB', 'BB'),
        ("INIT-04 (BI Builder)", 5.5, 19200, '#2563EB', 'BB'),
        ("INIT-11 (RBAC Teams)", 4.0, 15000, '#2563EB', 'BB'),
        ("INIT-17 (Email Reports)", 1.5, 8000, '#64748B', 'FI'),
        ("INIT-10 (Dark Mode)", 2.0, 10000, '#64748B', 'FI'),
        ("INIT-14 (GraphQL)", 7.0, 1500, '#EF4444', 'MP'),
        ("INIT-19 (Rust Rewrite)", 14.0, 1250, '#EF4444', 'MP'),
    ]

    for name, eff, val, col, q_type in initiatives:
        ax.scatter(eff, val, color=col, s=85, edgecolors='#0F172A', linewidth=0.9, zorder=5)
        offset_y = 1200 if val < 40000 else -1800
        offset_x = 0.2 if eff < 10 else -1.8
        ax.text(eff + offset_x, val + offset_y, name, fontsize=7.2, fontweight='bold', color='#0F172A', zorder=6)

    ax.set_xlim(0, 15.5)
    ax.set_ylim(0, 52000)
    ax.set_xlabel("Esfuerzo Técnico / Effort (Persona-Mes)" if lang == 'ES' else "Technical Effort (Person-Months)", fontsize=8.5, fontweight='bold', color='#334155')
    ax.set_ylabel("Valor Esperado / Expected Value (R×I×C)" if lang == 'ES' else "Expected Value (R×I×C)", fontsize=8.5, fontweight='bold', color='#334155')
    ax.set_title("Matriz Estratégica 2x2: Valor Esperado vs. Esfuerzo" if lang == 'ES' else "Strategic 2x2 Matrix: Expected Value vs. Effort", fontsize=10.0, fontweight='bold', color='#0F172A', pad=10)
    ax.grid(True, linestyle=':', alpha=0.35, color='#94A3B8')

    plt.tight_layout()
    fig.savefig(out_path, dpi=220, facecolor='#FFFFFF')
    plt.close(fig)
    return out_path


def add_header(slide, action_title, slide_num, total_slides=3, lang='ES'):
    """Añade la cabecera estándar Tier-1 con metadatos y Action Title de Minto."""
    # Badge superior
    tb_badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.0), Inches(0.28))
    tf_b = tb_badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = (
        "DATALARIA · SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN | ESTÁNDAR INTERCOM RICE & GROWTH ICE"
        if lang == 'ES' else
        "DATALARIA · SUITE 02: DECISION ANALYSIS & PRIORITIZATION | INTERCOM RICE & GROWTH ICE STANDARD"
    )
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_BLUE_ACCENT
    p_b.font.name = FONT_HEADING

    # Action Title (Pirámide de Minto)
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.65))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.size = Pt(17.5)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK
    p_t.font.name = FONT_HEADING

    # Número de diapositiva
    tb_num = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.0), Inches(0.28))
    tf_n = tb_num.text_frame
    tf_n.word_wrap = False
    tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
    p_n = tf_n.paragraphs[0]
    p_n.alignment = PP_ALIGN.RIGHT
    p_n.text = f"{slide_num:02d} / {total_slides:02d}"
    p_n.font.size = Pt(8.5)
    p_n.font.bold = True
    p_n.font.color.rgb = COLOR_TEXT_MUTED
    p_n.font.name = FONT_BODY


def add_kpi_card(slide, left, top, width, height, title, value, subtitle, border_color=COLOR_BORDER, value_color=COLOR_BLUE_ACCENT):
    """Crea una tarjeta métrica ejecutiva estilizada con tipografía de alta legibilidad."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_CARD_BG
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.08)
    tf.margin_bottom = Inches(0.06)

    # Título
    p0 = tf.paragraphs[0]
    p0.text = title.upper()
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_TEXT_MUTED
    p0.font.name = FONT_HEADING
    p0.space_after = Pt(2)

    # Valor
    p1 = tf.add_paragraph()
    p1.text = str(value)
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = value_color
    p1.font.name = FONT_HEADING
    p1.space_after = Pt(2)

    # Subtítulo
    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = COLOR_TEXT_MAIN
    p2.font.name = FONT_BODY


def build_slide1(prs, lang='ES'):
    """Diapositiva 1: Síntesis Ejecutiva & Veredicto de Priorización."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    action_title = (
        "De 20 iniciativas evaluadas, 5 Quick Wins concentran el 54% del valor RICE con solo el 19% del esfuerzo: "
        "se propone congelar 2 Pozos sin Fondo y liberar 21 persona-mes para Q1"
        if lang == 'ES' else
        "Across 20 backlog initiatives, 5 Quick Wins capture 54% of RICE value using only 19% of effort: "
        "freezing 2 Money Pits releases 21 person-months for Q1 execution"
    )
    add_header(slide, action_title, 1, 3, lang=lang)

    # 4 KPI Cards superiores
    kpi_defs_es = [
        ("Iniciativa Líder RICE", "INIT-18", "Score 33.333 | 2FA Obligatorio", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT),
        ("Concentración Top 20%", "54,2%", "4 iniciativas capturan más del 50% de valor", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT),
        ("Utilización Capacidad", "76,7%", "Holgura óptima para absorber imprevistos", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT),
        ("Esfuerzo Descartado", "21,0 PM", "Ahorro al congelar 2 Pozos sin Fondo", COLOR_RED_BORDER, COLOR_RED_TEXT),
    ]
    kpi_defs_en = [
        ("#1 Priority Initiative", "INIT-18", "RICE Score 33,333 | Mandatory 2FA", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT),
        ("Top 20% Value Share", "54.2%", "Top 4 items capture over 50% of value", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT),
        ("Capacity Utilization", "76.7%", "Optimal slack to absorb delivery risks", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT),
        ("Freed Engineering", "21.0 PM", "Reclaimed by freezing 2 Money Pits", COLOR_RED_BORDER, COLOR_RED_TEXT),
    ]
    kpis = kpi_defs_es if lang == 'ES' else kpi_defs_en

    card_w = Inches(2.78)
    card_h = Inches(1.22)
    start_x = Inches(0.8)
    gap = Inches(0.19)
    y_kpi = Inches(1.42)

    for i, (t, v, s, bcol, vcol) in enumerate(kpis):
        cx = start_x + i * (card_w + gap)
        add_kpi_card(slide, cx, y_kpi, card_w, card_h, t, v, s, bcol, vcol)

    # Bloques Inferiores: Izquierda (Diagnóstico Cuantitativo) y Derecha (Veredicto C-Level)
    y_bottom = Inches(2.76)
    w_block = Inches(5.75)
    h_block = Inches(4.34)

    # Bloque Izquierdo
    sh_l = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, y_bottom, w_block, h_block)
    sh_l.fill.solid()
    sh_l.fill.fore_color.rgb = COLOR_CARD_BG
    sh_l.line.color.rgb = COLOR_BORDER
    sh_l.line.width = Pt(1.2)

    tf_l = sh_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.2)
    tf_l.margin_top = Inches(0.18)

    p_lh = tf_l.paragraphs[0]
    p_lh.text = "DIAGNÓSTICO ESTRATÉGICO: DENSIDAD DE VALOR & SESGO HiPPO" if lang == 'ES' else "STRATEGIC DIAGNOSTIC: VALUE DENSITY & HiPPO BIAS"
    p_lh.font.size = Pt(12.5)
    p_lh.font.bold = True
    p_lh.font.color.rgb = COLOR_NAVY_DARK
    p_lh.font.name = FONT_HEADING
    p_lh.space_after = Pt(10)

    bullets_l_es = [
        ("Patología de la Fábrica de Funcionalidades:", " El backlog histórico contenía iniciativas solicitadas por intuición directiva (HiPPO) que consumían el 45% del ancho de banda técnico sin evidencia empírica."),
        ("Ley de Potencia en el Retorno (Pareto RICE):", " El 20% superior de iniciativas evaluadas captura el 54,2% del impacto esperado total (R×I×C). Concentrar el esfuerzo en este quintil triplica el ROI de ingeniería."),
        ("El Peligro Oculto de los 'Pozos sin Fondo':", " Proyectos como la reescritura a Rust (INIT-19) y la capa GraphQL (INIT-14) exigían 21 persona-mes con confianza baja (50%), destruyendo la productividad del equipo."),
        ("Gobernanza del Buffer de Deuda Técnica:", " Se reserva un 16,7% estricto de capacidad (6 PM/Q) para refactorización continua y estabilidad, blindando el roadmap frente a incidencias críticas."),
    ]
    bullets_l_en = [
        ("Feature Factory Pathology:", " The legacy backlog was cluttered with executive pet projects (HiPPO bias) consuming 45% of engineering bandwidth without verified market demand."),
        ("Power-Law Value Distribution:", " The top 20% of prioritized initiatives captures 54.2% of total expected RICE value. Focusing capacity here triples engineering return on investment."),
        ("The 'Money Pit' Hazard:", " Initiatives such as the total Rust database rewrite (INIT-19) and GraphQL layer (INIT-14) demand 21 person-months with low confidence (50%), eroding delivery velocity."),
        ("Technical Debt Buffer Governance:", " A mandatory 16.7% buffer (6 PM/quarter) is safeguarded for KTLO, maintenance, and refactoring, insulating sprints from firefighting disruptions."),
    ]
    bullets_l = bullets_l_es if lang == 'ES' else bullets_l_en

    for b_title, b_desc in bullets_l:
        p = tf_l.add_paragraph()
        p.space_after = Pt(6)
        run1 = p.add_run()
        run1.text = f"• {b_title}"
        run1.font.size = Pt(10.0)
        run1.font.bold = True
        run1.font.color.rgb = COLOR_BLUE_ACCENT
        run1.font.name = FONT_HEADING

        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = COLOR_TEXT_MAIN
        run2.font.name = FONT_BODY

    # Bloque Derecho: Veredicto Ejecutivo & Directrices
    x_r = start_x + w_block + gap
    sh_r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_r, y_bottom, w_block, h_block)
    sh_r.fill.solid()
    sh_r.fill.fore_color.rgb = COLOR_CARD_BG
    sh_r.line.color.rgb = COLOR_GREEN_BORDER
    sh_r.line.width = Pt(1.5)

    tf_r = sh_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.2)
    tf_r.margin_top = Inches(0.18)

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "VEREDICTO DEL PRODUCT COUNCIL & ACCIONES DIRECTIVAS" if lang == 'ES' else "PRODUCT COUNCIL VERDICT & EXECUTIVE ACTIONS"
    p_rh.font.size = Pt(12.5)
    p_rh.font.bold = True
    p_rh.font.color.rgb = COLOR_GREEN_TEXT
    p_rh.font.name = FONT_HEADING
    p_rh.space_after = Pt(10)

    bullets_r_es = [
        ("1. Ejecución Inmediata de Quick Wins (Q1):", " Desplegar los 5 Quick Wins prioritarios (2FA, Onboarding Guiado, Exportador Rápido, NPS In-App y SSO Okta) con un compromiso cerrado de 7,5 PM."),
        ("2. Congelación Formal de Pozos sin Fondo:", " Cancelar de inmediato la asignación a INIT-19 e INIT-14. Reasignar los 21 PM liberados a acelerar el Copilot de IA (INIT-02) y la expansión Enterprise."),
        ("3. Aprobación de la Línea de Corte Anual:", " Fijar el techo de capacidad anual en 120 PM netos distribuidos en 3 squads. Toda iniciativa con esfuerzo acumulado > 120 PM queda formalmente diferida."),
        ("4. Cadencia de Experimentación Ágil ICE:", " Implementar un canal rápido de validación para hipótesis de crecimiento (sprint de tests < 2 semanas) antes de comprometer épicas mayores en RICE."),
    ]
    bullets_r_en = [
        ("1. Immediate Q1 Quick Wins Execution:", " Deploy the top 5 high-density Quick Wins (2FA, Guided Onboarding, Fast Exporter, NPS Pulse, Okta SSO) with a hard commitment of 7.5 person-months."),
        ("2. Formal Freeze of Out-of-Capacity Money Pits:", " Immediately halt engineering allocations to INIT-19 and INIT-14. Redirect the 21 reclaimed PM to accelerate the AI Copilot (INIT-02)."),
        ("3. Annual Capacity Cut-Line Ratification:", " Establish a net annual ceiling of 120 PM across 3 dedicated squads. Any initiative exceeding the 120 PM cumulative cut-line is formally deferred."),
        ("4. Agile ICE Experimentation Cadence:", " Institute a bi-weekly growth test track to de-risk high-uncertainty hypotheses via rapid prototypes prior to structural RICE commitment."),
    ]
    bullets_r = bullets_r_es if lang == 'ES' else bullets_r_en

    for b_title, b_desc in bullets_r:
        p = tf_r.add_paragraph()
        p.space_after = Pt(6)
        run1 = p.add_run()
        run1.text = f"• {b_title}"
        run1.font.size = Pt(10.0)
        run1.font.bold = True
        run1.font.color.rgb = COLOR_GREEN_TEXT
        run1.font.name = FONT_HEADING

        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = COLOR_TEXT_MAIN
        run2.font.name = FONT_BODY


def build_slide2(prs, lang='ES'):
    """Diapositiva 2: Evidencia Cuantitativa: Matriz Impacto/Esfuerzo & Ranking Top RICE."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    action_title = (
        "Matriz Impacto vs. Esfuerzo & Top RICE: La concentración en Quick Wins y Grandes Apuestas "
        "maximiza el ROI técnico eliminando proyectos no rentables"
        if lang == 'ES' else
        "Impact vs. Effort Matrix & Top RICE: Focusing on Quick Wins and Strategic Big Bets "
        "maximizes engineering ROI while cutting Money Pits"
    )
    add_header(slide, action_title, 2, 3, lang=lang)

    # 1. Contenedor Izquierdo: Matriz Gráfica 2x2
    chart_img_path = f"temp_rice_chart_{lang}.png"
    create_impact_effort_chart(lang=lang, out_path=chart_img_path)

    x_l = Inches(0.8)
    y_top = Inches(1.42)
    w_l = Inches(5.75)

    slide.shapes.add_picture(chart_img_path, x_l, y_top, width=w_l, height=Inches(4.05))
    if os.path.exists(chart_img_path):
        os.remove(chart_img_path)

    # Caja de notas metodológicas bajo la matriz
    sh_note = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_l, Inches(5.56), w_l, Inches(1.54))
    sh_note.fill.solid()
    sh_note.fill.fore_color.rgb = COLOR_CARD_BG
    sh_note.line.color.rgb = COLOR_BORDER
    sh_note.line.width = Pt(1.0)

    tf_n = sh_note.text_frame
    tf_n.word_wrap = True
    tf_n.margin_left = tf_n.margin_right = Inches(0.16)
    tf_n.margin_top = Inches(0.10)

    p_nh = tf_n.paragraphs[0]
    p_nh.text = "NOTAS DE CALIBRACIÓN DE CUADRANTES:" if lang == 'ES' else "QUADRANT CALIBRATION NOTES:"
    p_nh.font.size = Pt(9.5)
    p_nh.font.bold = True
    p_nh.font.color.rgb = COLOR_NAVY_DARK
    p_nh.space_after = Pt(3)

    p_nb = tf_n.add_paragraph()
    p_nb.text = (
        "• Umbrales de corte fijados por las medianas muestrales: Esfuerzo = 2,5 PM, Valor Esperado = 15.000 pts.\n"
        "• La confianza actúa como factor de descuento de riesgo: C ∈ {0.5, 0.8, 1.0} según evidencia empírica.\n"
        "• Las iniciativas en el cuadrante rojo (Pozos sin Fondo) quedan excluidas de forma inapelable."
        if lang == 'ES' else
        "• Partition thresholds anchored on sample medians: Effort = 2.5 PM, Expected Value = 15,000 pts.\n"
        "• Confidence discounts risk: C ∈ {0.5, 0.8, 1.0} derived from empirical telemetry & user tests.\n"
        "• Red quadrant initiatives (Money Pits) are strictly disqualified from the committed roadmap."
    )
    p_nb.font.size = Pt(8.5)
    p_nb.font.color.rgb = COLOR_TEXT_MAIN

    # 2. Contenedor Derecho: Tabla Top RICE + Bloque Experimentos ICE
    x_r = Inches(6.75)
    w_r = Inches(5.75)

    # Tabla Top 6 RICE
    table_shape = slide.shapes.add_table(7, 6, x_r, y_top, w_r, Inches(2.65))
    tbl = table_shape.table

    # Anchos de columnas
    tbl.columns[0].width = Inches(0.85) # ID
    tbl.columns[1].width = Inches(2.30) # Iniciativa
    tbl.columns[2].width = Inches(0.65) # Reach
    tbl.columns[3].width = Inches(0.60) # Esfuerzo
    tbl.columns[4].width = Inches(0.70) # Score
    tbl.columns[5].width = Inches(0.65) # Cuadrante

    headers_table_es = ["ID", "Iniciativa Priorizada", "Reach", "PM", "Score", "Cuadrante"]
    headers_table_en = ["ID", "Prioritized Initiative", "Reach", "PM", "Score", "Quadrant"]
    h_tbl = headers_table_es if lang == 'ES' else headers_table_en

    for c_idx, h_text in enumerate(h_tbl):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_MED
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER if c_idx != 1 else PP_ALIGN.LEFT

    top_rows_es = [
        ("INIT-18", "2FA Obligatorio SMS/TOTP", "25k", "1.5", "33.333", "Quick Win"),
        ("INIT-15", "NPS In-App Automatizado", "25k", "1.0", "25.000", "Quick Win"),
        ("INIT-03", "Exportador Informes Excel/PDF", "22k", "1.0", "22.000", "Quick Win"),
        ("INIT-05", "Onboarding Guiado Interactivo", "15k", "1.5", "20.000", "Quick Win"),
        ("INIT-01", "SSO Okta SAML Enterprise", "8.5k", "2.0", "8.500", "Quick Win"),
        ("INIT-02", "Copilot de IA en Flujo de Trabajo", "18k", "6.0", "7.200", "Gran Apuesta"),
    ]
    top_rows_en = [
        ("INIT-18", "Mandatory Two-Factor 2FA", "25k", "1.5", "33,333", "Quick Win"),
        ("INIT-15", "Automated In-App NPS Pulse", "25k", "1.0", "25,000", "Quick Win"),
        ("INIT-03", "Instant Data Exporter Excel/PDF", "22k", "1.0", "22,000", "Quick Win"),
        ("INIT-05", "Guided Self-Serve Onboarding", "15k", "1.5", "20,000", "Quick Win"),
        ("INIT-01", "Enterprise Okta SAML SSO", "8.5k", "2.0", "8,500", "Quick Win"),
        ("INIT-02", "In-Workflow Generative AI Copilot", "18k", "6.0", "7,200", "Big Bet"),
    ]
    top_rows = top_rows_es if lang == 'ES' else top_rows_en

    for r_idx, row_vals in enumerate(top_rows, start=1):
        for c_idx, val in enumerate(row_vals):
            cell = tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.name = FONT_BODY
            p.alignment = PP_ALIGN.CENTER if c_idx in [0, 2, 3, 5] else (PP_ALIGN.RIGHT if c_idx == 4 else PP_ALIGN.LEFT)
            if c_idx == 4:
                p.font.bold = True
                p.font.color.rgb = COLOR_BLUE_ACCENT
            elif c_idx == 5:
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN_TEXT if "Quick" in val else COLOR_BLUE_ACCENT

    # Bloque Experimentos ICE (Growth Fast-Track)
    y_ice = Inches(4.18)
    h_ice = Inches(2.92)
    sh_ice = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_r, y_ice, w_r, h_ice)
    sh_ice.fill.solid()
    sh_ice.fill.fore_color.rgb = COLOR_CARD_BG
    sh_ice.line.color.rgb = COLOR_AMBER_BORDER
    sh_ice.line.width = Pt(1.5)

    tf_ice = sh_ice.text_frame
    tf_ice.word_wrap = True
    tf_ice.margin_left = tf_ice.margin_right = Inches(0.18)
    tf_ice.margin_top = Inches(0.12)

    p_ih = tf_ice.paragraphs[0]
    p_ih.text = "⚡ EXPERIMENTACIÓN ÁGIL ICE: TESTS PRIORITARIOS DE GROWTH (Q1)" if lang == 'ES' else "⚡ AGILE ICE EXPERIMENTATION: PRIORITY GROWTH TESTS (Q1)"
    p_ih.font.size = Pt(10.5)
    p_ih.font.bold = True
    p_ih.font.color.rgb = COLOR_AMBER_TEXT
    p_ih.font.name = FONT_HEADING
    p_ih.space_after = Pt(4)

    ice_highlights_es = [
        ("EXP-01: Registro con Google en 1 Clic (Score ICE: 648)", "Impacto: 8 | Conf: 9 | Facilidad: 9 -> Validación demostrada (+24% conversión). Despliegue en Q1."),
        ("EXP-02: Banner 20% Descuento Anual Checkout (Score ICE: 576)", "Impacto: 9 | Conf: 8 | Facilidad: 8 -> Acelera cobros por adelantado en +31%. Squad Monetización."),
        ("EXP-03: Onboarding Gamificado con Progreso (Score ICE: 512)", "Impacto: 8 | Conf: 8 | Facilidad: 8 -> Reduce Time-to-Value de 4 a 1 día. Squad Product-Led."),
    ]
    ice_highlights_en = [
        ("EXP-01: One-Click Google OAuth Signup (ICE Score: 648)", "Impact: 8 | Conf: 9 | Ease: 9 -> Proven +24% signup lift in canary test. Target Q1 deployment."),
        ("EXP-02: 20% Annual Plan Checkout Callout (ICE Score: 576)", "Impact: 9 | Conf: 8 | Ease: 8 -> Drives +31% shift to annual upfront billing. Monetization Squad."),
        ("EXP-03: Gamified Interactive Progress Checklist (ICE Score: 512)", "Impact: 8 | Conf: 8 | Ease: 8 -> Shrinks Time-to-Value from 4d to 1d. Product-Led Squad."),
    ]
    ice_highlights = ice_highlights_es if lang == 'ES' else ice_highlights_en

    for exp_title, exp_desc in ice_highlights:
        p = tf_ice.add_paragraph()
        p.space_after = Pt(4)
        run1 = p.add_run()
        run1.text = f"• {exp_title}\n  "
        run1.font.size = Pt(9.5)
        run1.font.bold = True
        run1.font.color.rgb = COLOR_NAVY_DARK
        run1.font.name = FONT_HEADING

        run2 = p.add_run()
        run2.text = exp_desc
        run2.font.size = Pt(8.5)
        run2.font.color.rgb = COLOR_TEXT_MAIN
        run2.font.name = FONT_BODY


def build_slide3(prs, lang='ES'):
    """Diapositiva 3: Roadmap Now/Next/Later & Product Council Decision Gateway."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    action_title = (
        "Roadmap Now/Next/Later & Gateway de Decisión: Aprobación formal de la capacidad Q1-Q4 (120 PM) "
        "y congelación vinculante de iniciativas fuera de corte"
        if lang == 'ES' else
        "Now/Next/Later Roadmap & Governance Gateway: Binding Q1-Q4 capacity allocation (120 PM) "
        "and formal freeze of out-of-capacity initiatives"
    )
    add_header(slide, action_title, 3, 3, lang=lang)

    # Mitad Superior: 3 Horizontes Now / Next / Later
    y_top = Inches(1.42)
    h_horiz = Inches(2.10)
    w_horiz = Inches(3.78)
    gap = Inches(0.18)
    start_x = Inches(0.8)

    horizons_es = [
        ("NOW (Compromiso Q1)", "30 PM Netos (Utilización 76,7%)", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT, [
            "• INIT-18: 2FA Obligatorio SMS/TOTP (1.5 PM)",
            "• INIT-15: NPS In-App Automatizado (1.0 PM)",
            "• INIT-03: Exportador Rápido de Informes (1.0 PM)",
            "• INIT-05: Onboarding Guiado Interactivo (1.5 PM)",
            "• INIT-01: Autenticación SSO Okta SAML (2.0 PM)",
            "• INIT-08: Facturación Stripe Multi-Divisa (3.0 PM)",
        ]),
        ("NEXT (Planificado Q2 - Q3)", "60 PM Netos (Capacidad en Maduración)", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT, [
            "• INIT-02: Copilot de IA en Flujo de Trabajo (6.0 PM)",
            "• INIT-04: Constructor Visual Dashboards (5.5 PM)",
            "• INIT-06: Catálogo Webhooks & API REST v2 (3.5 PM)",
            "• INIT-11: Workspaces Multi-Equipo RBAC (4.0 PM)",
            "• INIT-16: Integración Bot Slack/Teams (3.0 PM)",
            "• Spikes de Arquitectura Técnica y Discovery previo",
        ]),
        ("LATER / FUERA DE CORTE", "Excluido del Plan Anual (>120 PM)", COLOR_RED_BORDER, COLOR_RED_TEXT, [
            "• INIT-19: Reescribe DB a Rust (14.0 PM) - CONGELADO",
            "• INIT-14: Capa GraphQL (7.0 PM) - CONGELADO",
            "• INIT-12: Marca Blanca Completa (5.0 PM) - DIFERIDO",
            "• Ahorro total de 26,0 PM de esfuerzo no productivo",
            "• Reevaluación condicionada a nuevos datos de analítica",
            "• Protección absoluta contra la fábrica de features",
        ]),
    ]
    horizons_en = [
        ("NOW (Committed Q1)", "30 Net PM (76.7% Utilization)", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT, [
            "• INIT-18: Mandatory Two-Factor 2FA (1.5 PM)",
            "• INIT-15: Automated In-App NPS Pulse (1.0 PM)",
            "• INIT-03: Instant Data Exporter Excel/PDF (1.0 PM)",
            "• INIT-05: Guided Self-Serve Onboarding (1.5 PM)",
            "• INIT-01: Enterprise Okta SAML SSO (2.0 PM)",
            "• INIT-08: Stripe Multi-Currency Billing (3.0 PM)",
        ]),
        ("NEXT (Planned Q2 - Q3)", "60 Net PM (Target Discovery & Spikes)", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT, [
            "• INIT-02: In-Workflow Generative AI Copilot (6.0 PM)",
            "• INIT-04: Custom Executive Dashboard BI (5.5 PM)",
            "• INIT-06: REST API v2 & Event Webhooks (3.5 PM)",
            "• INIT-11: Multi-Team Workspaces RBAC (4.0 PM)",
            "• INIT-16: Slack / MS Teams Collaboration Bot (3.0 PM)",
            "• Active UX discovery & technical de-risking spikes",
        ]),
        ("LATER / CUT-LINE EXCLUSION", "Excluded from Annual Budget (>120 PM)", COLOR_RED_BORDER, COLOR_RED_TEXT, [
            "• INIT-19: Total DB Rewrite to Rust (14.0 PM) - FROZEN",
            "• INIT-14: GraphQL API Layer (7.0 PM) - FROZEN",
            "• INIT-12: Full White-Labeling (5.0 PM) - DEFERRED",
            "• Reclaims 26.0 person-months of low-ROI technical effort",
            "• Re-evaluation gated on customer demand telemetry",
            "• Eliminates feature factory creep and preserves focus",
        ]),
    ]
    horizons = horizons_es if lang == 'ES' else horizons_en

    for i, (h_title, h_sub, bcol, tcol, bullet_list) in enumerate(horizons):
        hx = start_x + i * (w_horiz + gap)
        sh_h = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, hx, y_top, w_horiz, h_horiz)
        sh_h.fill.solid()
        sh_h.fill.fore_color.rgb = COLOR_CARD_BG
        sh_h.line.color.rgb = bcol
        sh_h.line.width = Pt(1.5)

        tf_h = sh_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_right = Inches(0.14)
        tf_h.margin_top = Inches(0.08)

        p_ht = tf_h.paragraphs[0]
        p_ht.text = h_title
        p_ht.font.size = Pt(10.5)
        p_ht.font.bold = True
        p_ht.font.color.rgb = tcol
        p_ht.font.name = FONT_HEADING

        p_hs = tf_h.add_paragraph()
        p_hs.text = h_sub
        p_hs.font.size = Pt(8.5)
        p_hs.font.color.rgb = COLOR_TEXT_MUTED
        p_hs.space_after = Pt(3)

        for b_text in bullet_list:
            p_b = tf_h.add_paragraph()
            p_b.text = b_text
            p_b.font.size = Pt(8.5)
            p_b.font.color.rgb = COLOR_TEXT_MAIN
            p_b.font.name = FONT_BODY

    # Mitad Inferior: Product Council Decision Gateway (Board Resolutions & Sign-Offs)
    # Contenedor Marco Externo (sin texto dentro para evitar solapamientos)
    y_gate = Inches(3.66)
    w_gate = Inches(11.7)
    h_gate = Inches(3.48)

    sh_gate = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, y_gate, w_gate, h_gate)
    sh_gate.fill.solid()
    sh_gate.fill.fore_color.rgb = COLOR_CARD_BG
    sh_gate.line.color.rgb = COLOR_NAVY_MED
    sh_gate.line.width = Pt(1.5)

    # Cuadro de texto exclusivo para Acuerdos Vinculantes (Termina estrictamente antes de las firmas)
    tb_gate = slide.shapes.add_textbox(Inches(1.05), Inches(3.76), Inches(11.2), Inches(1.72))
    tf_g = tb_gate.text_frame
    tf_g.word_wrap = True
    tf_g.margin_left = tf_g.margin_right = tf_g.margin_top = tf_g.margin_bottom = 0

    p_gh = tf_g.paragraphs[0]
    p_gh.text = "ACUERDOS VINCULANTES DEL COMITÉ DE DIRECCIÓN / BOARD DECISION GATEWAY" if lang == 'ES' else "C-SUITE BINDING GOVERNANCE RESOLUTIONS / BOARD DECISION GATEWAY"
    p_gh.font.size = Pt(11.5)
    p_gh.font.bold = True
    p_gh.font.color.rgb = COLOR_NAVY_DARK
    p_gh.font.name = FONT_HEADING
    p_gh.space_after = Pt(5)

    resolutions_es = [
        "1. Aprobación del Roadmap Priorizado (Horizonte Now): Ratificar el compromiso de entrega de los 5 Quick Wins en Q1.",
        "2. Congelación Vinculante de Pozos sin Fondo: Bloquear formalmente la asignación presupuestaria y técnica a INIT-19 e INIT-14.",
        "3. Blindaje del Buffer de Deuda Técnica: Salvaguardar contractualmente el 16,7% (6 PM/Q) para refactor y fiabilidad operativa.",
        "4. Cadencia de Revisión Trimestral: Repriorizar el backlog cada 90 días integrando aprendizajes de los experimentos ICE.",
    ]
    resolutions_en = [
        "1. Committed Roadmap Ratification (Now Horizon): Formally lock delivery milestones for the 5 priority Quick Wins in Q1.",
        "2. Binding Freeze on Money Pits: Legally and operationally halt all budget and engineering allocations to INIT-19 and INIT-14.",
        "3. Technical Debt Buffer Ring-Fencing: Enforce a strict 16.7% capacity buffer (6 PM/quarter) dedicated to platform reliability.",
        "4. Quarterly Backlog Review Cadence: Re-evaluate and re-score the portfolio every 90 days feeding back empirical ICE test results.",
    ]
    res_list = resolutions_es if lang == 'ES' else resolutions_en

    for r_txt in res_list:
        p_r = tf_g.add_paragraph()
        p_r.text = r_txt
        p_r.font.size = Pt(9.5)
        p_r.font.color.rgb = COLOR_TEXT_MAIN
        p_r.font.name = FONT_BODY
        p_r.space_after = Pt(2.5)

    # 4 Bloques de Firmas C-Level (Ubicados limpiamente bajo los acuerdos sin solapamiento)
    y_sign = Inches(5.64)
    w_sign = Inches(2.65)
    h_sign = Inches(1.30)
    sign_gap = Inches(0.23)
    start_sign_x = Inches(1.05)

    signatures_es = [
        ("Chief Executive Officer (CEO)", "Dirección General & Estrategia", "Aprobado [Firma Digital]"),
        ("Chief Product Officer (CPO)", "Definición de Backlog & RICE", "Aprobado [Firma Digital]"),
        ("Chief Technology Officer (CTO)", "Capacidad de Ingeniería & Factibilidad", "Aprobado [Firma Digital]"),
        ("Chief Financial Officer (CFO)", "Asignación Presupuestaria & TCO", "Aprobado [Firma Digital]"),
    ]
    signatures_en = [
        ("Chief Executive Officer (CEO)", "Corporate Strategy & Mandate", "Approved [Digital Signature]"),
        ("Chief Product Officer (CPO)", "Backlog Prioritization & RICE", "Approved [Digital Signature]"),
        ("Chief Technology Officer (CTO)", "Engineering Capacity & Velocity", "Approved [Digital Signature]"),
        ("Chief Financial Officer (CFO)", "Budget Allocation & ARR Moat", "Approved [Digital Signature]"),
    ]
    sigs = signatures_es if lang == 'ES' else signatures_en

    for i, (role, area, status) in enumerate(sigs):
        sx = start_sign_x + i * (w_sign + sign_gap)
        sh_s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, y_sign, w_sign, h_sign)
        sh_s.fill.solid()
        sh_s.fill.fore_color.rgb = COLOR_WHITE
        sh_s.line.color.rgb = COLOR_BORDER
        sh_s.line.width = Pt(1.2)

        tf_s = sh_s.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = Inches(0.12)
        tf_s.margin_top = Inches(0.10)

        p_s0 = tf_s.paragraphs[0]
        p_s0.text = role
        p_s0.font.size = Pt(10.0)
        p_s0.font.bold = True
        p_s0.font.color.rgb = COLOR_NAVY_DARK

        p_s1 = tf_s.add_paragraph()
        p_s1.text = area
        p_s1.font.size = Pt(8.5)
        p_s1.font.color.rgb = COLOR_TEXT_MUTED
        p_s1.space_after = Pt(5)

        p_s2 = tf_s.add_paragraph()
        p_s2.text = f"✓ {status}"
        p_s2.font.size = Pt(9.5)
        p_s2.font.bold = True
        p_s2.font.color.rgb = COLOR_GREEN_TEXT


def generate_deck(lang='ES', out_path=None):
    if out_path is None:
        if lang == 'ES':
            out_path = "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[ES]_Matriz_RICE_ICE/Presentacion_RICE_ICE_CLevel_ES.pptx"
        else:
            out_path = "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[EN]_RICE_ICE_Matrix/Deck_RICE_ICE_CLevel_EN.pptx"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print(f"\nGenerando presentación ejecutiva ({lang}): {out_path}...")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide1(prs, lang=lang)
    build_slide2(prs, lang=lang)
    build_slide3(prs, lang=lang)

    prs.save(out_path)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"[OK] Presentación PowerPoint creada con éxito: {out_path} ({size_kb:.1f} KB)")
    return out_path


def main():
    print("================================================================================")
    print("DATALARIA | GENERADOR DE PRESENTACIONES C-LEVEL RICE & ICE (.PPTX)")
    print("================================================================================")
    es_path = generate_deck(lang='ES')
    en_path = generate_deck(lang='EN')
    print("\nPresentaciones generadas exitosamente en ambos idiomas.")


if __name__ == "__main__":
    main()
