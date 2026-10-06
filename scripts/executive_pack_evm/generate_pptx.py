#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/[ES]_Cuadro_EVM_Valor_Ganado/Presentacion_EVM_CLevel_ES.pptx
2. packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/[EN]_Earned_Value_Management_EVM/Deck_EVM_CLevel_EN.pptx

Características de diseño Tier-1 (ANSI/EIA-748 / PMBOK / McKinsey Minto Pyramid):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Action Titles contundentes.
- Diapositiva 1: Diagnóstico Ejecutivo de Salud Financiera & Plazos (4 KPI Cards y la trampa contable vs EVM).
- Diapositiva 2: Curva S Ejecutiva & Análisis de Varianzas por Entregable (Gráfico Curva S y Top 3 entregables en sobrecoste).
- Diapositiva 3: Plan de Recuperación, Opciones de Descope & Board Decision Gateway (3 Pilares, 4 Resoluciones y Cajas de Firma).
- Sin solapes de texto, márgenes protegidos y acabados visuales de calidad Consejo de Administración.
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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
COLOR_NAVY_DARK = RGBColor(15, 23, 42)       # #0F172A Slate 900
COLOR_NAVY_MED = RGBColor(30, 41, 59)        # #1E293B Slate 800
COLOR_BLUE_ACCENT = RGBColor(37, 99, 235)    # #2563EB Blue 600
COLOR_BLUE_LIGHT = RGBColor(239, 246, 255)   # #EFF6FF Blue 50
COLOR_CYAN_ACCENT = RGBColor(2, 132, 199)    # #0284C7 Sky 600
COLOR_PURPLE_ACCENT = RGBColor(124, 58, 237) # #7C3AED Purple 600

# Estados y Acentos
COLOR_GREEN_BG = RGBColor(209, 250, 229)     # #D1FAE5 Verde suave
COLOR_GREEN_BORDER = RGBColor(16, 185, 129)  # #10B981 Verde acento
COLOR_GREEN_TEXT = RGBColor(6, 95, 70)       # #065F46 Verde texto

COLOR_AMBER_BG = RGBColor(254, 243, 199)     # #FEF3C7 Ámbar suave
COLOR_AMBER_BORDER = RGBColor(245, 158, 11)  # #F59E0B Ámbar acento
COLOR_AMBER_TEXT = RGBColor(146, 64, 14)     # #92400E Ámbar texto

COLOR_RED_BG = RGBColor(254, 226, 226)       # #FEE2E2 Rojo suave
COLOR_RED_BORDER = RGBColor(220, 38, 38)     # #DC2626 Rojo acento
COLOR_RED_TEXT = RGBColor(153, 27, 27)       # #991B1B Rojo texto

COLOR_TEXT_MAIN = RGBColor(51, 65, 85)       # #334155 Slate 700
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B Slate 500
COLOR_CARD_BG = RGBColor(248, 250, 252)      # #F8FAFC Slate 50
COLOR_BORDER = RGBColor(203, 213, 225)       # #CBD5E1 Slate 300
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"


def add_header(slide, action_title, slide_num, total_slides=3, lang='ES'):
    """Cabecera institucional de alto impacto con Action Title de Minto."""
    tb_badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_b = tb_badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = "DATALARIA EXECUTIVE PACK  ·  ANSI/EIA-748 & PMBOK EARNED VALUE MANAGEMENT" if lang == 'ES' else "DATALARIA EXECUTIVE PACK  ·  ANSI/EIA-748 & PMBOK EARNED VALUE MANAGEMENT"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_BLUE_ACCENT

    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.85))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(17)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    tb_num = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.0), Inches(0.3))
    tf_n = tb_num.text_frame
    tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
    p_n = tf_n.paragraphs[0]
    p_n.text = f"{slide_num:02d} / {total_slides:02d}"
    p_n.alignment = PP_ALIGN.RIGHT
    p_n.font.name = FONT_HEADING
    p_n.font.size = Pt(9)
    p_n.font.bold = True
    p_n.font.color.rgb = COLOR_TEXT_MUTED


def add_kpi_card(slide, left, top, width, height, title, value, subtitle, status='neutral'):
    """Crea una tarjeta KPI estilizada con borde y color contextual."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.shadow.inherit = False

    if status == 'danger':
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_RED_BG
        shape.line.color.rgb = COLOR_RED_BORDER
        val_color = COLOR_RED_TEXT
    elif status == 'success':
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_GREEN_BG
        shape.line.color.rgb = COLOR_GREEN_BORDER
        val_color = COLOR_GREEN_TEXT
    elif status == 'accent':
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_BLUE_LIGHT
        shape.line.color.rgb = COLOR_BLUE_ACCENT
        val_color = COLOR_BLUE_ACCENT
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_BORDER
        val_color = COLOR_NAVY_DARK

    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.14)
    tf.margin_bottom = Inches(0.14)

    p0 = tf.paragraphs[0]
    p0.text = title.upper()
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(8.5)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_TEXT_MUTED
    p0.space_after = Pt(4)

    p1 = tf.add_paragraph()
    p1.text = value
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = val_color
    p1.space_after = Pt(3)

    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8)
    p2.font.color.rgb = COLOR_TEXT_MUTED


def generate_scurve_chart_image(output_path, lang='ES'):
    """Genera la imagen en alta resolución de la Curva S ejecutiva con proyección EAC."""
    months = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    # PV acumulado planeado
    pv_cum = np.array([60, 140, 240, 350, 470, 600, 730, 850, 960, 1060, 1140, 1200])  # miles €

    # EV acumulado (solo hasta mes 6)
    ev_cum = np.array([58, 133, 225, 320, 418, 516])
    m_ev = np.array([1, 2, 3, 4, 5, 6])

    # AC acumulado (solo hasta mes 6)
    ac_cum = np.array([62, 146, 254, 368, 484, 600])
    m_ac = np.array([1, 2, 3, 4, 5, 6])

    # Proyección EAC desde mes 6 (600k€) hasta mes 12 (1.395k€)
    m_eac = np.array([6, 7, 8, 9, 10, 11, 12])
    eac_cum = np.array([600, 732, 865, 998, 1130, 1262, 1395])

    fig, ax = plt.subplots(figsize=(6.4, 4.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    # Líneas de curvas
    ax.plot(months, pv_cum, color='#2563EB', linewidth=2.5, linestyle='-', marker='o', markersize=4, label='PV Planificado (Baseline)')
    ax.plot(m_ev, ev_cum, color='#10B981', linewidth=2.8, linestyle='-', marker='s', markersize=5, label='EV Valor Ganado (Trabajo Real)')
    ax.plot(m_ac, ac_cum, color='#DC2626', linewidth=2.8, linestyle='-', marker='^', markersize=5, label='AC Coste Real Incurrido')
    ax.plot(m_eac, eac_cum, color='#7C3AED', linewidth=2.2, linestyle='--', marker='d', markersize=4, label='EAC 1 Proyección Final (1.395 k€)')

    # Sombrear brecha entre AC y EV en mes 6
    ax.fill_between([6, 6.05], [516, 516], [600, 600], color='#FEE2E2', alpha=0.9)

    # Línea vertical de corte en Mes 6
    ax.axvline(6, color='#0F172A', linestyle=':', linewidth=1.5, alpha=0.8)
    ax.text(6.1, 150, "Corte Mes 6" if lang == 'ES' else "Cutoff Month 6",
            color='#0F172A', fontsize=8.5, fontweight='bold')

    # Marcadores de varianza en mes 6
    ax.annotate("CV = -84 k€\n(Sobrecoste)" if lang == 'ES' else "CV = -$84k\n(Overrun)",
                xy=(6, 600), xytext=(4.3, 720),
                arrowprops=dict(facecolor='#DC2626', shrink=0.05, width=1, headwidth=4),
                fontsize=7.5, fontweight='bold', color='#991B1B',
                bbox=dict(boxstyle="round,pad=0.3", fc="#FEE2E2", ec="#DC2626", lw=1))

    ax.annotate("SV = -84 k€\n(Retraso)" if lang == 'ES' else "SV = -$84k\n(Delay)",
                xy=(6, 516), xytext=(6.5, 420),
                arrowprops=dict(facecolor='#D97706', shrink=0.05, width=1, headwidth=4),
                fontsize=7.5, fontweight='bold', color='#92400E',
                bbox=dict(boxstyle="round,pad=0.3", fc="#FEF3C7", ec="#F59E0B", lw=1))

    # Títulos y ejes
    ax.set_title("Curva S Acumulada: PV vs EV vs AC & Proyección EAC" if lang == 'ES' else "Cumulative S-Curve: PV vs EV vs AC & EAC Forecast",
                 fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel("Mes de Ejecución" if lang == 'ES' else "Execution Month",
                  fontsize=8.5, color='#334155', fontweight='bold')
    ax.set_ylabel("Importe Acumulado (Miles € / $)" if lang == 'ES' else "Cumulative Amount (k$ / k€)",
                  fontsize=8.5, color='#334155')

    ax.set_xticks(months)
    ax.set_xticklabels([f"M{m:02d}" for m in months], fontsize=8)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper left', fontsize=7.5, framealpha=0.95)
    plt.tight_layout()

    fig.savefig(output_path, dpi=220, bbox_inches='tight')
    plt.close(fig)


def build_slide1(prs, lang='ES'):
    """Diapositiva 1: Diagnóstico Ejecutivo de Salud Financiera & Plazos."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    action_title = (
        "El proyecto presenta un sobrecoste del 16% (CPI = 0.86) y 3 semanas de retraso (SPI = 0.86): "
        "la proyección estadística EAC anticipa una desviación final de 195.000 € que exige renegociar el alcance antes de Q4"
        if lang == 'ES' else
        "The project exhibits a 16% cost overrun (CPI = 0.86) and 3-week schedule delay (SPI = 0.86): "
        "statistical EAC forecasting anticipates a $195,000 budget deficit requiring scope re-baselining before Q4"
    )
    add_header(slide, action_title, slide_num=1, total_slides=3, lang=lang)

    # 4 KPI Cards (Top: 1.85", Height: 1.35", Width: 2.75", Gap: 0.2")
    top_kpi = Inches(1.85)
    h_kpi = Inches(1.35)
    w_kpi = Inches(2.75)
    gap = Inches(0.24)
    l0 = Inches(0.8)

    cards = [
        ("Índice de Coste (CPI)" if lang == 'ES' else "Cost Perf. Index (CPI)",
         "0.86x",
         "Por cada 1€ gastado se generan 0.86€ de valor" if lang == 'ES' else "Only $0.86 earned value per $1 spent",
         "danger"),

        ("Índice de Plazo (SPI)" if lang == 'ES' else "Schedule Perf. (SPI)",
         "0.86x",
         "3 semanas de retraso frente a la línea base" if lang == 'ES' else "3 weeks behind approved baseline schedule",
         "danger"),

        ("Desviación al Cierre (VAC)" if lang == 'ES' else "Variance at Close (VAC)",
         "-195.349 €" if lang == 'ES' else "-$195,349",
         "Déficit proyectado a la conclusión (BAC - EAC)" if lang == 'ES' else "Projected deficit at completion (BAC - EAC)",
         "danger"),

        ("Rendimiento Requerido (TCPI)" if lang == 'ES' else "To-Complete Index (TCPI)",
         "1.14x",
         "Inviable según PMBOK (>1.10 requiere re-baseline)" if lang == 'ES' else "Unviable per PMBOK (>1.10 requires re-baseline)",
         "danger"),
    ]

    for idx, (title, val, sub, stat) in enumerate(cards):
        left_pos = l0 + idx * (w_kpi + gap)
        add_kpi_card(slide, left_pos, top_kpi, w_kpi, h_kpi, title, val, sub, stat)

    # 2 Contenedores Inferiores:
    # Izquierda: La Falacia de la Contabilidad Tradicional vs EVM
    # Derecha: Implicaciones Estratégicas para el Consejo
    top_box = Inches(3.45)
    h_box = Inches(3.45)
    w_box = Inches(5.72)

    # Caja Izquierda
    box_l = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_box, w_box, h_box)
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = COLOR_CARD_BG
    box_l.line.color.rgb = COLOR_BORDER
    box_l.line.width = Pt(1.5)
    box_l.shadow.inherit = False

    tf_l = box_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.25)
    tf_l.margin_top = tf_l.margin_bottom = Inches(0.2)

    p = tf_l.paragraphs[0]
    p.text = "LA TRAMPA DE LA CONTABILIDAD TRADICIONAL VS DIAGNÓSTICO EVM" if lang == 'ES' else "THE TRADITIONAL ACCOUNTING TRAP VS EVM DIAGNOSTICS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(8)

    bullets_l = [
        ("La Ilusión del Presupuesto 50% Gastado:",
         "La contabilidad financiera tradicional reporta que habiendo transcurrido 6 meses (50% del plazo) y habiéndose gastado 600.000 € (50% del presupuesto de 1.2M €), el proyecto aparenta estar 'en orden y en costes'."
         if lang == 'ES' else
         "Traditional finance reporting states that with 6 months elapsed (50% of timeline) and $600,000 spent (50% of the $1.2M budget), the initiative appears deceptively 'on budget and under control'."),

        ("La Revelación Quirúrgica del Valor Ganado (EV):",
         "El estándar EVM mide el trabajo físico realmente completado: solo se han producido 516.000 € de avance real. Existe un déficit oculto de 84.000 € de sobrecoste y otros 84.000 € de retraso funcional."
         if lang == 'ES' else
         "EVM quantifies physical deliverables actually completed: only $516,000 of earned value exists. A hidden deficit of $84,000 in pure overrun and $84,000 in functional delay has been uncovered."),

        ("Pérdida de Poder Adquisitivo del Proyecto:",
         "El equipo de desarrollo e integración está destruyendo 0,14 € por cada euro invertido debido a refactorizaciones imprevistas, bloqueos de dependencias en APIs externas y rotación de especialistas."
         if lang == 'ES' else
         "The engineering and integration squads are losing $0.14 per dollar invested due to unexpected architectural refactoring, external API dependency blockers, and specialized team turnover."),
    ]

    for b_title, b_desc in bullets_l:
        p_b = tf_l.add_paragraph()
        p_b.text = f"• {b_title} "
        p_b.font.name = FONT_HEADING
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_BLUE_ACCENT
        p_b.space_after = Pt(2)

        run = p_b.add_run()
        run.text = b_desc
        run.font.name = FONT_BODY
        run.font.size = Pt(9)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MAIN

    # Caja Derecha
    box_r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), top_box, w_box, h_box)
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = COLOR_BLUE_LIGHT
    box_r.line.color.rgb = COLOR_BLUE_ACCENT
    box_r.line.width = Pt(1.5)
    box_r.shadow.inherit = False

    tf_r = box_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.25)
    tf_r.margin_top = tf_r.margin_bottom = Inches(0.2)

    p = tf_r.paragraphs[0]
    p.text = "IMPLICACIONES ESTRATÉGICAS PARA EL CONSEJO DE ADMINISTRACIÓN" if lang == 'ES' else "STRATEGIC IMPLICATIONS FOR THE EXECUTIVE BOARD"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(8)

    bullets_r = [
        ("Agotamiento Inminente de Reservas de Gestión:",
         "La reserva de contingencia contractual (10% = 120.000 €) ya ha sido consumida en un 70% por los sobrecostes acumulados de las Fases 1 y 2, dejando el proyecto desprotegido ante la Fase 4 de migración."
         if lang == 'ES' else
         "The contractual contingency reserve (10% = $120,000) has already been 70% absorbed by accumulated Phase 1 & 2 overruns, leaving Phase 4 data migration vulnerable to downstream shocks."),

        ("Imposibilidad Estadística de Recuperar el Presupuesto Inicial:",
         "Un TCPI de 1.14x significa que los equipos deberían acelerar su productividad un 32% sobre su histórico. Exigir cumplir el BAC sin inyectar capital ni recortar alcance es empujar al equipo al colapso técnico."
         if lang == 'ES' else
         "A TCPI of 1.14x requires teams to boost delivery efficiency by 32% above historical baselines. Forcing the original BAC without capital injection or descope risks structural delivery failure."),

        ("Ventana de Intervención Ejecutiva Limitada (Q3):",
         "Si el Consejo interviene hoy mediante fast-tracking y descope acordado, la desviación final se acota en +50k€. Si se espera a Q4, el efecto compuesto (EAC 3) disparará el desvío por encima de los 1.9M €."
         if lang == 'ES' else
         "Decisive Q3 board action (fast-tracking and negotiated descope) caps final variance at +$50k. Waiting until Q4 compounds delay and cost (EAC 3), risking an overrun exceeding $1.9M."),
    ]

    for b_title, b_desc in bullets_r:
        p_b = tf_r.add_paragraph()
        p_b.text = f"• {b_title} "
        p_b.font.name = FONT_HEADING
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_NAVY_DARK
        p_b.space_after = Pt(2)

        run = p_b.add_run()
        run.text = b_desc
        run.font.name = FONT_BODY
        run.font.size = Pt(9)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MAIN


def build_slide2(prs, chart_img_path, lang='ES'):
    """Diapositiva 2: Curva S Ejecutiva & Análisis de Varianzas por Entregable."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    action_title = (
        "La Curva S revela una brecha de varianza de 84.000 € a mitad de plazo: "
        "3 paquetes de trabajo de integración concentran el 75% del sobrecoste acumulado"
        if lang == 'ES' else
        "The S-Curve reveals an $84,000 variance gap at mid-point: "
        "3 integration work packages account for 75% of the cumulative cost overrun"
    )
    add_header(slide, action_title, slide_num=2, total_slides=3, lang=lang)

    # Contenedor Izquierdo: Imagen de la Curva S
    # Left: 0.8", Top: 1.85", Width: 6.2", Height: 5.0"
    slide.shapes.add_picture(chart_img_path, Inches(0.8), Inches(1.85), width=Inches(6.2), height=Inches(5.0))

    # Contenedor Derecho: Desglose de varianzas y cuadrantes de salud
    top_r = Inches(1.85)
    w_r = Inches(5.3)

    # 1. Caja de Semáforo de Salud Operativa
    box_quad = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), top_r, w_r, Inches(1.6))
    box_quad.fill.solid()
    box_quad.fill.fore_color.rgb = COLOR_RED_BG
    box_quad.line.color.rgb = COLOR_RED_BORDER
    box_quad.line.width = Pt(1.5)
    box_quad.shadow.inherit = False

    tf_q = box_quad.text_frame
    tf_q.word_wrap = True
    tf_q.margin_left = tf_q.margin_right = Inches(0.2)
    tf_q.margin_top = tf_q.margin_bottom = Inches(0.12)

    pq = tf_q.paragraphs[0]
    pq.text = "DIAGNÓSTICO EN MATRIZ DE SALUD: CUADRANTE 4 (CRISIS ACTIVA)" if lang == 'ES' else "HEALTH MATRIX DIAGNOSTIC: QUADRANT 4 (ACTIVE CRISIS)"
    pq.font.name = FONT_HEADING
    pq.font.size = Pt(10.5)
    pq.font.bold = True
    pq.font.color.rgb = COLOR_RED_TEXT
    pq.space_after = Pt(4)

    pq_desc = tf_q.add_paragraph()
    pq_desc.text = (
        "Posición del Proyecto: CPI = 0.86 (< 1.0) y SPI = 0.86 (< 1.0).\n"
        "El proyecto se ubica en la zona de mayor vulnerabilidad operativa: sobrecoste financiero simultáneo con retraso de cronograma. Exige intervención correctiva antes de comprometer la Fase 4 de migración."
        if lang == 'ES' else
        "Project Coordinates: CPI = 0.86 (< 1.0) and SPI = 0.86 (< 1.0).\n"
        "The project is locked in the highest risk quadrant: simultaneous budget overrun and schedule delay. Immediate executive intervention is mandatory prior to committing Phase 4 data migration."
    )
    pq_desc.font.name = FONT_BODY
    pq_desc.font.size = Pt(8.5)
    pq_desc.font.color.rgb = COLOR_RED_TEXT

    # 2. Caja de Ranking de los 3 Entregables Críticos (Top 75% Sobrecoste)
    box_top3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(3.6), w_r, Inches(3.25))
    box_top3.fill.solid()
    box_top3.fill.fore_color.rgb = COLOR_CARD_BG
    box_top3.line.color.rgb = COLOR_BORDER
    box_top3.line.width = Pt(1.5)
    box_top3.shadow.inherit = False

    tf_3 = box_top3.text_frame
    tf_3.word_wrap = True
    tf_3.margin_left = tf_3.margin_right = Inches(0.2)
    tf_3.margin_top = tf_3.margin_bottom = Inches(0.15)

    p3 = tf_3.paragraphs[0]
    p3.text = "RANKING DE ENTREGABLES RESPONSABLES DEL SOBRECOSTE (PARETO 75%)" if lang == 'ES' else "TOP OVERRUN CONTRIBUTORS (PARETO 75% ROOT CAUSES)"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(10.5)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_NAVY_DARK
    p3.space_after = Pt(6)

    top_tasks = [
        ("1. WBS 2.1 Motor Transaccional de Conciliación",
         "CV: -20.000 € | CPI: 0.83x | SPI: 0.85x" if lang == 'ES' else "CV: -$20,000 | CPI: 0.83x | SPI: 0.85x",
         "Causa: Complejidad algorítmica imprevista en consistencia eventual distribuida. Consumió 115k€ frente a 95k€ previstos."
         if lang == 'ES' else
         "Root Cause: Unexpected algorithmic complexity in distributed eventual consistency. Consumed $115k vs $95k planned."),

        ("2. WBS 2.3 Módulo de Procesamiento de Pagos",
         "CV: -13.000 € | CPI: 0.87x | SPI: 0.82x" if lang == 'ES' else "CV: -$13,000 | CPI: 0.87x | SPI: 0.82x",
         "Causa: Fricciones y demoras de homologación con sandbox bancario externo. Retraso de 2,5 semanas en validación."
         if lang == 'ES' else
         "Root Cause: Certification latency and integration friction with partner bank sandbox. 2.5-week validation delay."),

        ("3. WBS 3.1 Conector Bidireccional ERP Core SAP",
         "CV: -13.000 € | CPI: 0.81x | SPI: 0.62x" if lang == 'ES' else "CV: -$13,000 | CPI: 0.81x | SPI: 0.62x",
         "Causa: Desviación de alcance en mapeo de tablas legacy e inflación de tarifas de consultores externos Time & Materials."
         if lang == 'ES' else
         "Root Cause: Scope creep in legacy table schema mapping combined with contractor Time & Materials rate inflation."),
    ]

    for t_name, t_metrics, t_cause in top_tasks:
        pt = tf_3.add_paragraph()
        pt.text = t_name
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(9.5)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_BLUE_ACCENT
        pt.space_after = Pt(1)

        pm = tf_3.add_paragraph()
        pm.text = f"  [{t_metrics}]"
        pm.font.name = FONT_HEADING
        pm.font.size = Pt(8.5)
        pm.font.bold = True
        pm.font.color.rgb = COLOR_RED_TEXT
        pm.space_after = Pt(1)

        pc = tf_3.add_paragraph()
        pc.text = f"  {t_cause}"
        pc.font.name = FONT_BODY
        pc.font.size = Pt(8)
        pc.font.color.rgb = COLOR_TEXT_MAIN
        pc.space_after = Pt(4)


def build_slide3(prs, lang='ES'):
    """Diapositiva 3: Plan de Recuperación, Opciones de Descope & Board Decision Gateway."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    action_title = (
        "Plan de estabilización operativa: inyección de 195.000 € de reservas de gestión, "
        "fast-tracking en pasarelas y descope diferido de módulos no críticos"
        if lang == 'ES' else
        "Operational stabilization plan: $195,000 management reserve allocation, "
        "payment gateway fast-tracking, and deferred non-critical scope"
    )
    add_header(slide, action_title, slide_num=3, total_slides=3, lang=lang)

    # MITAD SUPERIOR: 3 PILARES DEL PLAN DE RECUPERACIÓN (Top: 1.85", Height: 2.2", Width: 3.75", Gap: 0.2")
    top_p = Inches(1.85)
    h_p = Inches(2.2)
    w_p = Inches(3.72)
    gap_p = Inches(0.24)
    l0_p = Inches(0.8)

    pillars = [
        ("PILAR 1: FAST-TRACKING & PARALELIZACIÓN" if lang == 'ES' else "PILLAR 1: FAST-TRACKING & OVERLAPPING",
         "Recuperación de Cronograma (Δ SPI = +0.06)" if lang == 'ES' else "Schedule Acceleration (Δ SPI = +0.06)",
         "• Paralelización de pruebas de homologación sandbox bancaria con auditorías de seguridad.\n"
         "• Solapamiento de la preparación de scripts de migración (WBS 4.1) sin esperar a finalizar el conector CRM.\n"
         "• Ganancia estimada: 2,5 semanas recuperadas en el camino crítico."
         if lang == 'ES' else
         "• Execute bank sandbox certification in parallel with cybersecurity audits.\n"
         "• Overlap data migration scripting (WBS 4.1) prior to completing secondary CRM integrations.\n"
         "• Estimated recovery: 2.5 weeks regained on critical path."),

        ("PILAR 2: CRASHING SELECTIVO CON TALENTO SENIOR" if lang == 'ES' else "PILLAR 2: SELECTIVE CRASHING WITH EXPERTS",
         "Blindaje del Motor Core (Δ SPI = +0.05 | Δ CPI = +0.04)" if lang == 'ES' else "Core Engine Stabilization (Δ SPI = +0.05 | Δ CPI = +0.04)",
         "• Inyección de 2 arquitectos senior especializados en concurrencia distribuida durante 6 semanas.\n"
         "• Reasignación de recursos internos liberados de la Fase 1 para resolver el cuello de botella del motor.\n"
         "• Coste marginal: 24.000 € financiado con reservas de contingencia."
         if lang == 'ES' else
         "• Deploy 2 senior distributed systems architects for a targeted 6-week sprint.\n"
         "• Reassign freed internal Phase 1 infrastructure leads to clear transaction engine bottlenecks.\n"
         "• Marginal investment: $24,000 funded via approved contingency reserve."),

        ("PILAR 3: DESCOPE NEGOCIADO & PRECIO CERRADO" if lang == 'ES' else "PILLAR 3: NEGOTIATED DESCOPE & FIXED FEES",
         "Contención Presupuestaria (Δ CPI = +0.08)" if lang == 'ES' else "Budget Containment (Δ CPI = +0.08)",
         "• Diferir la sincronización secundaria del CRM Salesforce (WBS 3.3) para Q1 post Go-Live.\n"
         "• Migración obligatoria de contratos de consultoría SAP a precio cerrado por hito (fin de T&M).\n"
         "• Ahorro directo inmediato de 35.000 € de gasto evitado en Fase 3."
         if lang == 'ES' else
         "• Defer secondary CRM Salesforce contact sync (WBS 3.3) to Q1 post-launch release.\n"
         "• Enforce fixed-fee cap milestones with SAP implementation vendors (terminate T&M).\n"
         "• Immediate net savings: $35,000 in avoided Phase 3 expenditures."),
    ]

    for idx, (p_title, p_sub, p_body) in enumerate(pillars):
        left_pos = l0_p + idx * (w_p + gap_p)
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_p, w_p, h_p)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_BLUE_ACCENT if idx == 0 else COLOR_BORDER
        shape.line.width = Pt(1.5)
        shape.shadow.inherit = False

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = tf.margin_bottom = Inches(0.12)

        p0 = tf.paragraphs[0]
        p0.text = p_title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_BLUE_ACCENT
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = p_sub
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_GREEN_TEXT
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = p_body
        p2.font.name = FONT_BODY
        p2.font.size = Pt(7.8)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # MITAD INFERIOR: BOARD DECISION GATEWAY (Top: 4.2", Height: 2.7", Width: 11.73")
    top_gate = Inches(4.2)
    h_gate = Inches(2.7)
    w_gate = Inches(11.73)

    gate_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_gate, w_gate, h_gate)
    gate_box.fill.solid()
    gate_box.fill.fore_color.rgb = COLOR_BLUE_LIGHT
    gate_box.line.color.rgb = COLOR_BLUE_ACCENT
    gate_box.line.width = Pt(2.0)
    gate_box.shadow.inherit = False

    tf_g = gate_box.text_frame
    tf_g.word_wrap = True
    tf_g.margin_left = tf_g.margin_right = Inches(0.25)
    tf_g.margin_top = tf_g.margin_bottom = Inches(0.14)

    pg = tf_g.paragraphs[0]
    pg.text = "BOARD DECISION GATEWAY · RESOLUCIONES VINCULANTES DEL COMITÉ DE DIRECCIÓN" if lang == 'ES' else "BOARD DECISION GATEWAY · BINDING EXECUTIVE BOARD RESOLUTIONS"
    pg.font.name = FONT_HEADING
    pg.font.size = Pt(11)
    pg.font.bold = True
    pg.font.color.rgb = COLOR_NAVY_DARK
    pg.space_after = Pt(5)

    resolutions = [
        ("Resolución 1 (Aprobación de Techo EAC):",
         "Se aprueba el re-baselining formal del proyecto autorizando un nuevo techo presupuestario EAC de 1.395.349 € con liberación de 195.349 € de reservas de gestión corporativa."
         if lang == 'ES' else
         "Formal project re-baselining is ratified, approving an updated EAC budget ceiling of $1,395,349 with a $195,349 release from corporate management reserves."),

        ("Resolución 2 (Ratificación de Descope):",
         "Se ratifica diferir la fase 2 de sincronización CRM Salesforce a la release de Q1 post Go-Live para proteger la fecha inamovible de corte regulatorio."
         if lang == 'ES' else
         "Approval of Phase 2 CRM Salesforce synchronization deferral to post-launch Q1 release to secure regulatory compliance deadlines."),

        ("Resolución 3 (Mandato de Contratación Cerrada):",
         "Se instruye a Compras fijar contratos cerrados 'Fixed-Price' para las consultorías de SAP e integraciones restantes, cancelando esquemas Time & Materials."
         if lang == 'ES' else
         "Procurement is mandated to transition all remaining SAP and integration vendor contracts to Fixed-Price deliverables, ending T&M billing."),

        ("Resolución 4 (Gobernanza Quincenal EVM):",
         "Se establece un comité de control de valor ganado quincenal obligatorio presidido por el CFO y el COO para auditar el cumplimiento del nuevo TCPI = 0.86x."
         if lang == 'ES' else
         "Establishment of a mandatory bi-weekly EVM audit cadence led by the CFO and COO to track adherence to the revised TCPI = 0.86x target."),
    ]

    for r_title, r_desc in resolutions:
        pr = tf_g.add_paragraph()
        pr.text = f"• {r_title} "
        pr.font.name = FONT_HEADING
        pr.font.size = Pt(8.5)
        pr.font.bold = True
        pr.font.color.rgb = COLOR_BLUE_ACCENT
        pr.space_after = Pt(2)

        run = pr.add_run()
        run.text = r_desc
        run.font.name = FONT_BODY
        run.font.size = Pt(8)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MAIN

    # Cajas de firma de aprobación ejecutiva (4 firmas)
    top_sign = Inches(6.15)
    h_sign = Inches(0.65)
    w_sign = Inches(2.65)
    gap_s = Inches(0.25)
    l0_s = Inches(1.1)

    signatures = [
        ("CEO / Sponsor Ejecutivo" if lang == 'ES' else "CEO / Executive Sponsor", "[APROBADO / FIRMA]"),
        ("Chief Financial Officer (CFO)", "[APROBADO / FIRMA]"),
        ("Chief Operating Officer (COO)", "[APROBADO / FIRMA]"),
        ("Director PMO Corporativo", "[APROBADO / FIRMA]"),
    ]

    for idx, (role, status) in enumerate(signatures):
        left_s = l0_s + idx * (w_sign + gap_s)
        s_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_s, top_sign, w_sign, h_sign)
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = COLOR_WHITE
        s_box.line.color.rgb = COLOR_BORDER
        s_box.line.width = Pt(1.0)
        s_box.shadow.inherit = False

        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = Inches(0.1)
        tf_s.margin_top = tf_s.margin_bottom = Inches(0.05)

        ps0 = tf_s.paragraphs[0]
        ps0.text = role
        ps0.alignment = PP_ALIGN.CENTER
        ps0.font.name = FONT_HEADING
        ps0.font.size = Pt(7.5)
        ps0.font.bold = True
        ps0.font.color.rgb = COLOR_NAVY_DARK

        ps1 = tf_s.add_paragraph()
        ps1.text = status
        ps1.alignment = PP_ALIGN.CENTER
        ps1.font.name = FONT_BODY
        ps1.font.size = Pt(7)
        ps1.font.color.rgb = COLOR_TEXT_MUTED


def generate_presentation(lang='ES'):
    """Genera la presentación completa de 3 slides para el idioma especificado."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    dir_base = "packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado"
    if lang == 'ES':
        out_dir = os.path.join(dir_base, "[ES]_Cuadro_EVM_Valor_Ganado")
        out_file = os.path.join(out_dir, "Presentacion_EVM_CLevel_ES.pptx")
    else:
        out_dir = os.path.join(dir_base, "[EN]_Earned_Value_Management_EVM")
        out_file = os.path.join(out_dir, "Deck_EVM_CLevel_EN.pptx")

    os.makedirs(out_dir, exist_ok=True)

    # Generar gráfico temporal para la slide 2
    chart_tmp = os.path.join(out_dir, f"temp_scurve_{lang}.png")
    generate_scurve_chart_image(chart_tmp, lang=lang)

    print(f"[{lang}] Creando Diapositiva 1: Diagnóstico Ejecutivo...")
    build_slide1(prs, lang=lang)

    print(f"[{lang}] Creando Diapositiva 2: Curva S & Varianzas Pareto...")
    build_slide2(prs, chart_tmp, lang=lang)

    print(f"[{lang}] Creando Diapositiva 3: Plan de Recuperación & Board Gateway...")
    build_slide3(prs, lang=lang)

    prs.save(out_file)
    print(f"-> Presentación guardada exitosamente: {out_file}")

    # Limpiar archivo temporal
    if os.path.exists(chart_tmp):
        os.remove(chart_tmp)


def generate_all_pptx():
    """Genera las presentaciones en ambos idiomas."""
    generate_presentation(lang='ES')
    generate_presentation(lang='EN')
    print("\nGeneración de presentaciones PPTX completada con éxito.")


if __name__ == "__main__":
    generate_all_pptx()
