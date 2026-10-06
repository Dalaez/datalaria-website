#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[ES]_Estimacion_PERT_3_Puntos/Presentacion_PERT_CLevel_ES.pptx
2. packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[EN]_3Point_PERT_Estimation/Deck_PERT_CLevel_EN.pptx

Características de diseño Tier-1 (PMBOK 7th / TOC / McKinsey Minto Pyramid):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Action Titles contundentes.
- Diapositiva 1: Diagnóstico Ejecutivo & Riesgo de Cronograma (4 KPI Cards y diagnóstico cualitativo vs estocástico).
- Diapositiva 2: Curva de Densidad de Probabilidad (Gaussiana) & Gráfico Tornado de Sensibilidad (Top 5 varianzas).
- Diapositiva 3: Estrategia de Buffers, Crashing & Board Decision Gateway (4 resoluciones y firmas).
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


def apply_gradient_fill(shape, color1_hex, color2_hex, angle_deg=90):
    """Aplica degradado lineal nativo DrawingML a una forma."""
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


def add_header(slide, action_title, slide_num, total_slides=3, lang='ES'):
    """Cabecera institucional de alto impacto con Action Title de Minto."""
    tb_badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_b = tb_badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = "DATALARIA EXECUTIVE PACK  ·  PMBOK 7th / STOCHASTIC MANAGEMENT" if lang == 'ES' else "DATALARIA EXECUTIVE PACK  ·  PMBOK 7th / STOCHASTIC MANAGEMENT"
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


def generate_bell_curve_image(output_path, lang='ES'):
    """Genera el gráfico de la curva de Gauss con bandas de probabilidad."""
    mu = 132.5
    sigma = 11.8
    td = 125.0

    x = np.linspace(mu - 3.8 * sigma, mu + 3.8 * sigma, 400)
    y = (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    # Línea de la curva
    ax.plot(x, y, color='#2563EB', linewidth=2.5, label='Densidad Normal PERT (CLT)')

    # Sombrear área hasta fecha comprometida (34% probabilidad)
    x_risk = x[x <= td]
    y_risk = y[x <= td]
    ax.fill_between(x_risk, y_risk, color='#FEE2E2', alpha=0.8, label=f'P(T ≤ {td:.0f}d) = 34.2% (Riesgo Crítico)' if lang == 'ES' else f'P(T ≤ {td:.0f}d) = 34.2% (High Risk)')

    # Sombrear área segura hasta 90%
    x_90 = np.linspace(td, mu + 1.282 * sigma, 200)
    y_90 = (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_90 - mu) / sigma) ** 2)
    ax.fill_between(x_90, y_90, color='#EFF6FF', alpha=0.6, label='Buffer P90 (+15.1d)' if lang == 'ES' else 'P90 Buffer (+15.1d)')

    # Líneas verticales
    ax.axvline(mu, color='#0F172A', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.text(mu, max(y)*0.95, f'μ = {mu:.1f}d', color='#0F172A', fontsize=8.5, fontweight='bold', ha='center')

    ax.axvline(td, color='#DC2626', linestyle='-', linewidth=2.0)
    ax.text(td, max(y)*0.75, f'Compromiso: {td:.0f}d\n(Solo 34% éxito)' if lang == 'ES' else f'Target: {td:.0f}d\n(34% success)',
            color='#DC2626', fontsize=8, fontweight='bold', ha='right')

    p90_val = mu + 1.282 * sigma
    ax.axvline(p90_val, color='#10B981', linestyle='-.', linewidth=1.8)
    ax.text(p90_val, max(y)*0.85, f'P90: {p90_val:.1f}d\n(Objetivo Board)' if lang == 'ES' else f'P90: {p90_val:.1f}d\n(Board Target)',
            color='#065F46', fontsize=8, fontweight='bold', ha='left')

    ax.set_title("Curva de Densidad de Probabilidad del Cronograma" if lang == 'ES' else "Schedule Probability Density Curve (CLT)",
                 fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel("Duración Total en Días Hábiles" if lang == 'ES' else "Total Duration in Business Days",
                  fontsize=8.5, color='#334155', fontweight='bold')
    ax.set_ylabel("Densidad f(x)" if lang == 'ES' else "Density f(x)",
                  fontsize=8.5, color='#334155')

    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper right', fontsize=7.5, framealpha=0.9)
    plt.tight_layout()

    fig.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close(fig)


def generate_tornado_chart_image(output_path, lang='ES'):
    """Genera el gráfico Tornado con las 5 tareas de mayor varianza."""
    if lang == 'ES':
        tasks = [
            "2.1 Motor Conciliación Transaccional",
            "3.1 Conector Bidireccional ERP SAP",
            "2.3 Módulo de Procesamiento Pagos",
            "3.2 Pasarelas Bancarias Core",
            "4.4 Pruebas UAT de Negocio"
        ]
    else:
        tasks = [
            "2.1 Transactional Reconciliation",
            "3.1 Bidirectional SAP ERP Connector",
            "2.3 Payment Processing Module",
            "3.2 Core Banking Gateways",
            "4.4 Business UAT Acceptance"
        ]
    tasks = tasks[::-1]
    # Varianzas σ²
    variances = [7.1, 9.0, 9.0, 11.1, 11.1][::-1]
    percentages = [12.8, 16.2, 16.2, 20.0, 20.0][::-1]

    fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    bars = ax.barh(tasks, variances, color='#2563EB', edgecolor='#1D4ED8', height=0.55, alpha=0.9)
    bars[-1].set_color('#DC2626')  # Destacar la mayor varianza
    bars[-1].set_edgecolor('#B91C1C')
    bars[-2].set_color('#DC2626')
    bars[-2].set_edgecolor('#B91C1C')

    for bar, pct, val in zip(bars, percentages, variances):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                f"σ² = {val:.1f} ({pct:.1f}%)",
                va='center', ha='left', fontsize=8, color='#0F172A', fontweight='bold')

    ax.set_xlim(0, 14.5)
    ax.set_title("Top 5 Tareas con Mayor Varianza (75.2% de la Incertidumbre)" if lang == 'ES' else "Top 5 High-Variance Tasks (75.2% of Total Uncertainty)",
                 fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel("Varianza Individual σ² (días²)" if lang == 'ES' else "Individual Variance σ² (days²)",
                  fontsize=8.5, color='#334155', fontweight='bold')

    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1', axis='x')
    plt.tight_layout()

    fig.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close(fig)


def build_presentation(prs, lang='ES'):
    """Construye las 3 diapositivas ejecutivas oficiales."""
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    tmp_dir = "scripts/executive_pack_pert/tmp_charts"
    os.makedirs(tmp_dir, exist_ok=True)
    bell_path = os.path.join(tmp_dir, f"bell_curve_{lang}.png")
    tornado_path = os.path.join(tmp_dir, f"tornado_{lang}.png")

    generate_bell_curve_image(bell_path, lang)
    generate_tornado_chart_image(tornado_path, lang)

    # =========================================================================
    # SLIDE 1: DIAGNÓSTICO EJECUTIVO & RIESGO DE CRONOGRAMA
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)

    title_s1 = (
        "La fecha de entrega comprometida para el Go-Live tiene únicamente un 34% de probabilidad de éxito: se requiere formalizar un buffer de 16 días hábiles para garantizar un 90% de certidumbre ante el Board."
        if lang == 'ES' else
        "The committed Go-Live delivery date has only a 34% probability of success: formalizing a 16 business-day buffer is required to guarantee 90% certainty before the Board."
    )
    add_header(slide1, title_s1, 1, 3, lang)

    # 4 Tarjetas KPI superiores
    add_kpi_card(slide1, Inches(0.8), Inches(1.8), Inches(2.75), Inches(1.5),
                 "Duración Esperada μ" if lang == 'ES' else "Expected Duration μ",
                 "132.5 Días" if lang == 'ES' else "132.5 Days",
                 "Media estocástica camino crítico" if lang == 'ES' else "Stochastic critical path mean",
                 status='accent')

    add_kpi_card(slide1, Inches(3.78), Inches(1.8), Inches(2.75), Inches(1.5),
                 "Desviación Global σ" if lang == 'ES' else "Global Std Deviation σ",
                 "± 11.8 Días" if lang == 'ES' else "± 11.8 Days",
                 "Dispersión cuadrática CLT (±2σ = 47d)" if lang == 'ES' else "CLT dispersion (±2σ = 47d)",
                 status='neutral')

    add_kpi_card(slide1, Inches(6.76), Inches(1.8), Inches(2.75), Inches(1.5),
                 "Probabilidad en Fecha Actual" if lang == 'ES' else "Target Date Probability",
                 "34.2% Éxito" if lang == 'ES' else "34.2% Success",
                 "Objetivo 125d: INVIABLE sin colchón" if lang == 'ES' else "Target 125d: UNFEASIBLE w/o buffer",
                 status='danger')

    add_kpi_card(slide1, Inches(9.74), Inches(1.8), Inches(2.75), Inches(1.5),
                 "Buffer Requerido P90" if lang == 'ES' else "Required P90 Buffer",
                 "+15.1 Días" if lang == 'ES' else "+15.1 Days",
                 "Fecha blindada Board: 147.6 días" if lang == 'ES' else "Board target date: 147.6 days",
                 status='success')

    # Contenedores analíticos inferiores
    # Contenedor Izquierdo: Patologías del Modelo Determinista
    sh_left = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.55), Inches(5.75), Inches(3.35))
    sh_left.fill.solid()
    sh_left.fill.fore_color.rgb = COLOR_CARD_BG
    sh_left.line.color.rgb = COLOR_BORDER
    sh_left.line.width = Pt(1.2)
    tf_l = sh_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.25)
    tf_l.margin_top = tf_l.margin_bottom = Inches(0.2)

    p_lh = tf_l.paragraphs[0]
    p_lh.text = "DIAGNÓSTICO: LA TRAMPA DE LA ESTIMACIÓN A UN SOLO PUNTO" if lang == 'ES' else "DIAGNOSIS: THE SINGLE-POINT ESTIMATION TRAP"
    p_lh.font.name = FONT_HEADING
    p_lh.font.size = Pt(11)
    p_lh.font.bold = True
    p_lh.font.color.rgb = COLOR_NAVY_DARK
    p_lh.space_after = Pt(8)

    points_l_es = [
        ("La Falacia del Escenario 'Más Probable' (m):", "Fijar el compromiso en 125 días asume implícitamente un 100% de éxito en cada tarea sin fricción, lo que estadísticamente arroja solo un 34% de probabilidad de cumplimiento."),
        ("Ley de Parkinson & Síndrome del Estudiante:", "Las estimaciones individuales contienen colchones ocultos informales que se consumen por postergación, perdiéndose la oportunidad de acelerar el cronograma."),
        ("Asimetría Positiva del Riesgo Técnico:", "En integración de software e infraestructura cloud, las desviaciones pesimistas (p) son hasta 3 veces mayores que los ahorros optimistas (o).")
    ]
    points_l_en = [
        ("The 'Most Likely' (m) Fallacy:", "Committing to 125 days assumes zero friction across all tasks, which mathematically yields only a 34% probability of on-time delivery."),
        ("Parkinson's Law & Student Syndrome:", "Hidden individual safety buffers are wasted due to procrastination, preventing any potential schedule gains from accumulating."),
        ("Positive Skew of Engineering Risks:", "In software integration and cloud infrastructure, pessimistic delays (p) are up to 3 times larger than optimistic gains (o).")
    ]
    p_list_l = points_l_es if lang == 'ES' else points_l_en
    for b_title, b_desc in p_list_l:
        p_item = tf_l.add_paragraph()
        p_item.text = f"• {b_title} "
        p_item.font.name = FONT_BODY
        p_item.font.size = Pt(9)
        p_item.font.bold = True
        p_item.font.color.rgb = COLOR_NAVY_MED
        p_item.space_after = Pt(2)

        run_desc = p_item.add_run()
        run_desc.text = b_desc
        run_desc.font.name = FONT_BODY
        run_desc.font.size = Pt(8.5)
        run_desc.font.bold = False
        run_desc.font.color.rgb = COLOR_TEXT_MAIN

    # Contenedor Derecho: Solución Estocástica Datalaria
    sh_right = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(3.55), Inches(5.75), Inches(3.35))
    sh_right.fill.solid()
    sh_right.fill.fore_color.rgb = COLOR_BLUE_LIGHT
    sh_right.line.color.rgb = COLOR_BLUE_ACCENT
    sh_right.line.width = Pt(1.5)
    tf_r = sh_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.25)
    tf_r.margin_top = tf_r.margin_bottom = Inches(0.2)

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "SOLUCIÓN: GOBERNANZA ESTOCÁSTICA PERT (PMBOK / TOC)" if lang == 'ES' else "SOLUTION: STOCHASTIC PERT GOVERNANCE (PMBOK / TOC)"
    p_rh.font.name = FONT_HEADING
    p_rh.font.size = Pt(11)
    p_rh.font.bold = True
    p_rh.font.color.rgb = COLOR_BLUE_ACCENT
    p_rh.space_after = Pt(8)

    points_r_es = [
        ("Distribución Beta de 3 Puntos:", "Calibración matemática de Optimista (o), Más Probable (m) y Pesimista (p) ponderando la media μ = (o + 4m + p)/6 y dispersión σ = (p - o)/6."),
        ("Teorema del Límite Central (CLT):", "Las varianzas independientes del camino crítico se suman cuadráticamente (Σ σ²), permitiendo modelar el proyecto global mediante una distribución normal rigurosa."),
        ("Gobernanza de Colchones C-Level (P90):", "Extracción de la protección oculta de las tareas para concentrarla en un único 'Project Buffer' visible y gestionado formalmente por el Comité de Dirección.")
    ]
    points_r_en = [
        ("3-Point Beta Distribution:", "Mathematical calibration of Optimistic (o), Most Likely (m), and Pessimistic (p) weighting mean μ = (o + 4m + p)/6 and dispersion σ = (p - o)/6."),
        ("Central Limit Theorem (CLT):", "Critical path independent variances aggregate quadratically (Σ σ²), enabling exact normal distribution modeling of the total project schedule."),
        ("C-Level Buffer Governance (P90):", "Extracting safety padding from individual tasks and consolidating it into a transparent 'Project Buffer' governed directly by the Board.")
    ]
    p_list_r = points_r_es if lang == 'ES' else points_r_en
    for b_title, b_desc in p_list_r:
        p_item = tf_r.add_paragraph()
        p_item.text = f"• {b_title} "
        p_item.font.name = FONT_BODY
        p_item.font.size = Pt(9)
        p_item.font.bold = True
        p_item.font.color.rgb = COLOR_NAVY_MED
        p_item.space_after = Pt(2)

        run_desc = p_item.add_run()
        run_desc.text = b_desc
        run_desc.font.name = FONT_BODY
        run_desc.font.size = Pt(8.5)
        run_desc.font.bold = False
        run_desc.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 2: CURVA DE PROBABILIDAD & SENSIBILIDAD TORNADO
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)

    title_s2 = (
        "El análisis estocástico revela que 5 tareas concentran el 75% de la varianza del proyecto: la adopción del percentil P90 blinda la fecha en 148 días con un 90% de certidumbre."
        if lang == 'ES' else
        "Stochastic analysis reveals that 5 tasks drive 75% of schedule variance: adopting the P90 percentile secures delivery at 148 days with 90% certainty."
    )
    add_header(slide2, title_s2, 2, 3, lang)

    # Contenedor Izquierdo: Curva de Probabilidad
    sh_c1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    sh_c1.fill.solid()
    sh_c1.fill.fore_color.rgb = COLOR_WHITE
    sh_c1.line.color.rgb = COLOR_BORDER
    sh_c1.line.width = Pt(1.2)

    slide2.shapes.add_picture(bell_path, Inches(0.95), Inches(1.95), width=Inches(5.45))

    # Contenedor Derecho: Gráfico Tornado de Sensibilidad
    sh_c2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    sh_c2.fill.solid()
    sh_c2.fill.fore_color.rgb = COLOR_WHITE
    sh_c2.line.color.rgb = COLOR_BORDER
    sh_c2.line.width = Pt(1.2)

    slide2.shapes.add_picture(tornado_path, Inches(6.9), Inches(1.95), width=Inches(5.45))

    # =========================================================================
    # SLIDE 3: ESTRATEGIA DE BUFFERS & BOARD DECISION GATEWAY
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)

    title_s3 = (
        "Estrategia de aceleración y aprobación del Board Decision Gateway: adopción formal de la fecha P90, gobernanza del buffer de 16 días y plan de crashing selectivo."
        if lang == 'ES' else
        "Acceleration strategy and Board Decision Gateway approval: formal P90 date adoption, 16-day project buffer governance, and targeted crashing plan."
    )
    add_header(slide3, title_s3, 3, 3, lang)

    # Mitad Superior: 3 Pilares de Aceleración y Control de Buffer
    col_w = Inches(3.75)
    gap = Inches(0.24)

    pillars_es = [
        ("1. DIMENSIONAMIENTO DE BUFFER", "Buffer P90 Recomendado: +15.1 Días", "A diferencia del corte arbitrario del 50%, el método RSS y el cálculo Z-Score P90 dimensionan el colchón en 15.1 días hábiles, protegiendo al proyecto de variaciones en el camino crítico sin encarecerlo artificialmente."),
        ("2. PROTOCOLO DE CRASHING", "Coste Marginal Óptimo: 750 € a 1.200 €/día", "Identificación de tareas críticas con mayor ratio de retorno temporal por euro invertido: Pruebas UAT, Integración Bancaria y Motor de Conciliación permiten reducir hasta 11 días con un CAPEX controlado de 38.000 €."),
        ("3. SEGUIMIENTO DE BURN RATE", "Monitoreo Quincenal del Consumo de Buffer", "Semáforo de consumo de colchón: Zona Verde (<33% consumido), Zona Ámbar (33%-66% consumido: congelar scope), Zona Roja (>66% consumido: activación inmediata de recursos de crashing pre-aprobados).")
    ]
    pillars_en = [
        ("1. BUFFER SIZING METHODOLOGY", "Recommended P90 Buffer: +15.1 Days", "Unlike arbitrary 50% cuts, the RSS method and P90 Z-Score calculation size the contingency buffer at 15.1 business days, shielding the project from critical path shocks without inflating budgets."),
        ("2. TARGETED CRASHING PROTOCOL", "Optimal Marginal Cost: $750 to $1,200/day", "Pinpointing critical tasks with highest time-reduction yield per dollar: UAT Testing, Banking Gateway, and Core Reconciliation allow recovering up to 11 days with a controlled CAPEX of $38,000."),
        ("3. BUFFER BURN RATE GOVERNANCE", "Bi-Weekly Buffer Consumption Tracking", "Buffer penetration monitoring: Green Zone (<33% consumed), Amber Zone (33%-66%: scope lock), Red Zone (>66%: automatic trigger of pre-approved crashing resources).")
    ]
    p_data = pillars_es if lang == 'ES' else pillars_en

    for idx, (p_h, p_sub, p_txt) in enumerate(p_data):
        c_left = Inches(0.8) + idx * (col_w + gap)
        sh_p = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), col_w, Inches(2.2))
        sh_p.fill.solid()
        sh_p.fill.fore_color.rgb = COLOR_CARD_BG
        sh_p.line.color.rgb = COLOR_BORDER
        sh_p.line.width = Pt(1.2)

        tf_p = sh_p.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_right = Inches(0.18)
        tf_p.margin_top = tf_p.margin_bottom = Inches(0.15)

        p0 = tf_p.paragraphs[0]
        p0.text = p_h
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_BLUE_ACCENT
        p0.space_after = Pt(2)

        p1 = tf_p.add_paragraph()
        p1.text = p_sub
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p1.space_after = Pt(4)

        p2 = tf_p.add_paragraph()
        p2.text = p_txt
        p2.font.name = FONT_BODY
        p2.font.size = Pt(7.8)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # Mitad Inferior: Board Decision Gateway (Acuerdos Vinculantes y Firmas)
    sh_gw = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(11.7), Inches(2.7))
    sh_gw.fill.solid()
    sh_gw.fill.fore_color.rgb = COLOR_WHITE
    sh_gw.line.color.rgb = COLOR_BLUE_ACCENT
    sh_gw.line.width = Pt(1.8)

    tf_gw = sh_gw.text_frame
    tf_gw.word_wrap = True
    tf_gw.margin_left = tf_gw.margin_right = Inches(0.25)
    tf_gw.margin_top = tf_gw.margin_bottom = Inches(0.15)

    p_gwh = tf_gw.paragraphs[0]
    p_gwh.text = "BOARD DECISION GATEWAY · RESOLUCIONES VINCULANTES DEL COMITÉ DE DIRECCIÓN" if lang == 'ES' else "BOARD DECISION GATEWAY · BINDING EXECUTIVE COMMITTEE RESOLUTIONS"
    p_gwh.font.name = FONT_HEADING
    p_gwh.font.size = Pt(11)
    p_gwh.font.bold = True
    p_gwh.font.color.rgb = COLOR_NAVY_DARK
    p_gwh.space_after = Pt(6)

    resolutions_es = [
        "1. Fijación del Compromiso Oficial en Percentil P90 (148 días hábiles) con fecha objetivo formal de Go-Live ante stakeholders.",
        "2. Aprobación y blindaje de la Reserva de Contingencia (Project Buffer de 16 días) bajo gobernanza exclusiva del Project Manager y PMO.",
        "3. Dotación presupuestaria pre-aprobada de 38.000 € para ejecución de Crashing en tareas críticas si el buffer supera la Zona Ámbar (66%).",
        "4. Convocatoria quincenal de revisión de consumo de buffer en el Comité de Operaciones y veto expreso a la adición de alcance sin ampliación de buffer."
    ]
    resolutions_en = [
        "1. Official Delivery Date locked at P90 Percentile (148 business days) for all stakeholder and external contractual commitments.",
        "2. Formal approval and protection of the 16-day Project Buffer under exclusive governance of the PMO and Project Lead.",
        "3. Pre-allocated emergency Crashing budget of $38,000 ready for immediate deployment if buffer penetration exceeds Amber threshold (66%).",
        "4. Bi-weekly Boardroom Buffer Burn Rate review and strict governance veto against scope additions without proportional buffer extension."
    ]
    res_list = resolutions_es if lang == 'ES' else resolutions_en

    for r_txt in res_list:
        p_res = tf_gw.add_paragraph()
        p_res.text = r_txt
        p_res.font.name = FONT_BODY
        p_res.font.size = Pt(8.2)
        p_res.font.color.rgb = COLOR_NAVY_MED
        p_res.space_after = Pt(2)

    # Bloque de Firmas / Aprobaciones
    p_sig = tf_gw.add_paragraph()
    p_sig.text = "Firmas de Conformidad: [  ] Chief Executive Officer (CEO)    [  ] Chief Operating Officer (COO)    [  ] Chief Financial Officer (CFO)    [  ] Project Sponsor" if lang == 'ES' else "Approval Signatures: [  ] Chief Executive Officer (CEO)    [  ] Chief Operating Officer (COO)    [  ] Chief Financial Officer (CFO)    [  ] Project Sponsor"
    p_sig.font.name = FONT_HEADING
    p_sig.font.size = Pt(8)
    p_sig.font.bold = True
    p_sig.font.color.rgb = COLOR_TEXT_MUTED
    p_sig.space_before = Pt(6)


def main():
    base_dir = "packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos"
    dir_es = os.path.join(base_dir, "[ES]_Estimacion_PERT_3_Puntos")
    dir_en = os.path.join(base_dir, "[EN]_3Point_PERT_Estimation")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    file_es = os.path.join(dir_es, "Presentacion_PERT_CLevel_ES.pptx")
    file_en = os.path.join(dir_en, "Deck_PERT_CLevel_EN.pptx")

    print("[1/2] Generando presentación PowerPoint C-Level en Español...")
    prs_es = Presentation()
    build_presentation(prs_es, lang='ES')
    prs_es.save(file_es)
    print(f" -> Guardado exitosamente: {file_es}")

    print("[2/2] Generando presentación PowerPoint C-Level en Inglés...")
    prs_en = Presentation()
    build_presentation(prs_en, lang='EN')
    prs_en.save(file_en)
    print(f" -> Guardado exitosamente: {file_en}")

    # Limpieza temporal
    tmp_dir = "scripts/executive_pack_pert/tmp_charts"
    if os.path.exists(tmp_dir):
        for f in os.listdir(tmp_dir):
            os.remove(os.path.join(tmp_dir, f))
        os.rmdir(tmp_dir)

    print("Proceso PPTX completado con éxito.")


if __name__ == "__main__":
    main()
