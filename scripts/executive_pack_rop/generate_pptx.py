#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/[ES]_Stock_Seguridad_ROP/Presentacion_Stock_ROP_CLevel_ES.pptx
2. packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/[EN]_Safety_Stock_ROP/Deck_Safety_Stock_ROP_CLevel_EN.pptx

Características de diseño Tier-1 (APICS / ASCM / MIT CTL / McKinsey Minto Pyramid):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Action Titles contundentes.
- Diapositiva 1: Diagnóstico Ejecutivo de Inventario & Working Capital (4 KPI Cards y Empírico vs Estocástico).
- Diapositiva 2: Gráfico Diente de Sierra (Sawtooth) & Curva Asintótica de Nivel de Servicio (Matriz ABC).
- Diapositiva 3: Plan de Compresión de Lead Time & Board Decision Gateway (3 Pilares, 4 Resoluciones y Cajas de Firma).
- Gráficos de alta definición generados vía matplotlib e insertados sin solapes.
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
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

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


def add_header(slide, action_title, slide_num, total_slides=3, lang='ES'):
    """Cabecera institucional de alto impacto con Action Title de Minto."""
    tb_badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_b = tb_badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = "DATALARIA EXECUTIVE PACK • SUPPLY CHAIN / APICS INVENTORY OPTIMIZATION"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_BLUE_ACCENT

    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.85))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(15.5)
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
    tf.margin_left = Inches(0.16)
    tf.margin_right = Inches(0.16)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.12)

    p0 = tf.paragraphs[0]
    p0.text = title.upper()
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(8)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_TEXT_MUTED
    p0.space_after = Pt(2)

    p1 = tf.add_paragraph()
    p1.text = value
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = val_color
    p1.space_after = Pt(2)

    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.name = FONT_BODY
    p2.font.size = Pt(7.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED


def generate_sawtooth_chart_image(output_path, lang='ES'):
    """Genera la imagen del ciclo Diente de Sierra (Sawtooth) con matplotlib."""
    fig, ax = plt.subplots(figsize=(6.4, 4.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    # Parámetros visuales del ciclo:
    # 2 ciclos completos de 20 días cada uno
    # SS = 300 u, EOQ = 900 u, d = 45 u/día, L = 10 días, LTD = 450 u, ROP = 750 u
    # Nivel inicial: SS + EOQ = 1200 u
    days = np.linspace(0, 40, 400)
    inventory = []
    for d in days:
        t = d % 20
        if t <= 19.5:
            inv = 1200 - 45 * t
        else:
            inv = 300 + 45 * (20 - t) * 20  # Salto rápido de reposición
        inventory.append(inv)
    inventory = np.array(inventory)

    # Trazado de líneas principales
    ax.plot(days, inventory, color='#2563EB', linewidth=2.5, label='Nivel de Inventario Físico' if lang == 'ES' else 'Physical Inventory Level')
    ax.axhline(750, color='#F59E0B', linewidth=1.8, linestyle='--', label='Punto de Pedido (ROP = 750 u)' if lang == 'ES' else 'Reorder Point (ROP = 750 u)')
    ax.axhline(300, color='#10B981', linewidth=1.8, linestyle='-', label='Stock de Seguridad (SS = 300 u)' if lang == 'ES' else 'Safety Stock (SS = 300 u)')

    # Sombrear colchón de seguridad
    ax.axhspan(0, 300, color='#D1FAE5', alpha=0.5, label='Colchón Basal de Protección' if lang == 'ES' else 'Safety Buffer Protection Zone')

    # Anotaciones directas
    # Disparo de orden en día 10 (cuando inventario cruza ROP)
    ax.scatter([10, 30], [750, 750], color='#D97706', s=55, zorder=5)
    ax.annotate("Disparo de Pedido (+EOQ)\nVentana Lead Time (L = 10d)" if lang == 'ES' else "Order Placed (+EOQ)\nLead Time Window (L = 10d)",
                xy=(10, 750), xytext=(12, 920),
                arrowprops=dict(facecolor='#D97706', shrink=0.05, width=1, headwidth=4),
                fontsize=7.5, fontweight='bold', color='#92400E',
                bbox=dict(boxstyle="round,pad=0.3", fc="#FEF3C7", ec="#F59E0B", lw=1))

    # Recepción de lote en día 20
    ax.scatter([20], [300], color='#059669', s=55, zorder=5)
    ax.annotate("Recepción Pedido\nInventario salta a SS+EOQ" if lang == 'ES' else "Order Arrival\nInventory rises to SS+EOQ",
                xy=(20, 300), xytext=(22, 450),
                arrowprops=dict(facecolor='#059669', shrink=0.05, width=1, headwidth=4),
                fontsize=7.5, fontweight='bold', color='#065F46',
                bbox=dict(boxstyle="round,pad=0.3", fc="#D1FAE5", ec="#10B981", lw=1))

    ax.set_title("Ciclo de Reabastecimiento Continuo (Sawtooth Inventory Model)" if lang == 'ES' else "Continuous Replenishment Cycle (Sawtooth Inventory Model)",
                 fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel("Tiempo Transcurrido (Días de Operación)" if lang == 'ES' else "Time Elapsed (Operational Days)",
                  fontsize=8, fontweight='bold', color='#475569')
    ax.set_ylabel("Unidades en Almacén" if lang == 'ES' else "Warehouse Units",
                  fontsize=8, fontweight='bold', color='#475569')
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 1350)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper right', fontsize=7, framealpha=0.9, facecolor='#FFFFFF')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220)
    plt.close()


def generate_service_curve_chart_image(output_path, lang='ES'):
    """Genera la imagen de la curva exponencial de inversión según nivel de servicio."""
    fig, ax = plt.subplots(figsize=(6.4, 4.3), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    csl = np.array([85.0, 90.0, 93.0, 95.0, 97.0, 98.0, 99.0, 99.5, 99.8, 99.9])
    # Z-scores
    from scipy.stats import norm
    # Si scipy no estuviera, calculamos Z analítico o aproximación
    z_scores = np.array([1.036, 1.282, 1.476, 1.645, 1.881, 2.054, 2.326, 2.576, 2.878, 3.090])
    # Capital requerido en miles de € (base 95% = 232 k€)
    capital_k = (z_scores / 1.645) * 232.0

    ax.plot(csl, capital_k, color='#2563EB', linewidth=2.8, marker='o', markersize=5, label='Inversión en Stock de Seguridad' if lang == 'ES' else 'Safety Stock Capital Investment')

    # Zonas ABC destacadas
    ax.scatter([90.0], [capital_k[1]], color='#64748B', s=70, zorder=5)
    ax.annotate("Clase C: 90% (180 k€)\nRotación baja" if lang == 'ES' else "Class C: 90% ($180k)\nLow turnover",
                xy=(90.0, capital_k[1]), xytext=(86.0, 240),
                arrowprops=dict(facecolor='#64748B', shrink=0.05, width=1, headwidth=4),
                fontsize=7.5, fontweight='bold', color='#334155',
                bbox=dict(boxstyle="round,pad=0.2", fc="#F1F5F9", ec="#94A3B8", lw=1))

    ax.scatter([95.0], [capital_k[3]], color='#F59E0B', s=70, zorder=5)
    ax.annotate("Clase B: 95% (232 k€)\nBenchmark estándar" if lang == 'ES' else "Class B: 95% ($232k)\nStandard benchmark",
                xy=(95.0, capital_k[3]), xytext=(91.0, 310),
                arrowprops=dict(facecolor='#F59E0B', shrink=0.05, width=1, headwidth=4),
                fontsize=7.5, fontweight='bold', color='#92400E',
                bbox=dict(boxstyle="round,pad=0.2", fc="#FEF3C7", ec="#F59E0B", lw=1))

    ax.scatter([98.0], [capital_k[5]], color='#10B981', s=80, zorder=5)
    ax.annotate("Clase A: 98% (290 k€)\nÓptimo C-Level" if lang == 'ES' else "Class A: 98% ($290k)\nC-Level Optimal",
                xy=(98.0, capital_k[5]), xytext=(94.5, 380),
                arrowprops=dict(facecolor='#10B981', shrink=0.05, width=1, headwidth=4),
                fontsize=7.5, fontweight='bold', color='#065F46',
                bbox=dict(boxstyle="round,pad=0.2", fc="#D1FAE5", ec="#10B981", lw=1))

    # Zona asintótica crítica (>99%)
    ax.fill_between([99.0, 100.0], [0, 0], [500, 500], color='#FEE2E2', alpha=0.35)
    ax.text(99.1, 400, "Zona de Hiper-Inmovilización\n(Asíntota z -> inf)" if lang == 'ES' else "Hyper-Carrying Lockup Zone\n(Asymptote z -> inf)",
            fontsize=7.5, fontweight='bold', color='#991B1B')

    ax.set_title("Comportamiento Asintótico Exponencial: Capital vs. Nivel de Servicio" if lang == 'ES' else "Exponential Asymptotic Behavior: Capital vs. Service Level",
                 fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel("Nivel de Servicio de Ciclo (CSL %)" if lang == 'ES' else "Cycle Service Level (CSL %)",
                  fontsize=8, fontweight='bold', color='#475569')
    ax.set_ylabel("Capital Inmovilizado en SS (k€ / k$)" if lang == 'ES' else "SS Capital Lockup (k€ / k$)",
                  fontsize=8, fontweight='bold', color='#475569')
    ax.set_xlim(84.5, 100.2)
    ax.set_ylim(120, 460)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper left', fontsize=7.5, framealpha=0.9, facecolor='#FFFFFF')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220)
    plt.close()


def build_presentation(lang="ES"):
    """Construye la presentación de 3 diapositivas en formato 16:9 widescreen."""
    is_es = (lang == "ES")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    tmp_sawtooth = f"temp_sawtooth_{lang}.png"
    tmp_service = f"temp_service_{lang}.png"
    generate_sawtooth_chart_image(tmp_sawtooth, lang=lang)
    generate_service_curve_chart_image(tmp_service, lang=lang)

    # =========================================================================
    # DIAPOSITIVA 1: DIAGNÓSTICO EJECUTIVO DE INVENTARIO & WORKING CAPITAL
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    title_s1 = (
        "El 38% del capital de trabajo está inmovilizado en sobrestock por reglas empíricas mientras las referencias Clase A sufren un 7% de roturas: la optimización estocástica liberará 240.000 € elevando el servicio al 98%"
        if is_es else
        "38% of working capital is trapped in overstock due to empirical rules while Class A references suffer 7% stockouts: stochastic optimization releases $240,000 while elevating service to 98%"
    )
    add_header(s1, title_s1, 1, 3, lang=lang)

    # 4 KPI Cards
    card_w = Inches(2.78)
    card_h = Inches(1.22)
    card_y = Inches(1.70)
    kpis_s1_es = [
        ("INVERSIÓN ACTUAL EN STOCK", "622.400 €", "Reglas empíricas (3 semanas fijas)", "danger"),
        ("NIVEL DE SERVICIO PONDERADO", "93.2% → 97.4%", "Salto cualitativo con foco Clase A", "accent"),
        ("CAPITAL LIBERABLE DE CAJA", "240.000 €", "Liquidez neta transferible al balance", "success"),
        ("REDUCCIÓN DE ROTURAS CLASE A", "-65%", "De 7.2% a <2.0% de probabilidad de quiebre", "success")
    ]
    kpis_s1_en = [
        ("CURRENT WORKING CAPITAL", "$622,400", "Empirical rule (3 fixed weeks)", "danger"),
        ("WEIGHTED SERVICE LEVEL", "93.2% → 97.4%", "Strategic upgrade with Class A focus", "accent"),
        ("RELEASABLE WORKING CAPITAL", "$240,000", "Net liquidity freed for corporate balance", "success"),
        ("CLASS A STOCKOUT REDUCTION", "-65%", "From 7.2% to <2.0% shortage probability", "success")
    ]
    kpis_s1 = kpis_s1_es if is_es else kpis_s1_en

    for idx, (t, v, sub, st) in enumerate(kpis_s1):
        x = Inches(0.8) + idx * (card_w + Inches(0.18))
        add_kpi_card(s1, x, card_y, card_w, card_h, t, v, sub, st)

    # Comparativa ejecutiva inferior (Dos grandes contenedores)
    cont_y = Inches(3.15)
    cont_w = Inches(5.72)
    cont_h = Inches(3.85)

    # Contenedor Izquierdo: La Trampa Empírica
    shape_left = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), cont_y, cont_w, cont_h)
    shape_left.fill.solid(); shape_left.fill.fore_color.rgb = COLOR_RED_BG
    shape_left.line.color.rgb = COLOR_RED_BORDER; shape_left.line.width = Pt(1.5)
    tf_l = shape_left.text_frame; tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.24); tf_l.margin_top = Inches(0.18)

    p = tf_l.paragraphs[0]
    p.text = "PATOLOGÍA OPERATIVA: LA FALACIA DE LA REGLA DE LAS 3 SEMANAS" if is_es else "OPERATIONAL PATHOLOGY: THE FALLACY OF THE 3-WEEK RULE"
    p.font.name = FONT_HEADING; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_RED_TEXT
    p.space_after = Pt(8)

    bullets_l_es = [
        "Inmovilización Masiva en SKUs Estables: Mantener 21 días de stock en productos de demanda predecible y entrega rápida sobre-financia 185.000 € de capital inerte sin retorno.",
        "Desabastecimiento Crítico en SKUs Volátiles: En componentes con proveedores lejanos (L > 25 días) y alta desviación (σd), 3 semanas es un colchón insuficiente, provocando 7.2% de roturas en referencias Clase A.",
        "Ignorancia de la Impuntualidad del Proveedor: La regla empírica asume que el proveedor siempre entrega a tiempo (σL = 0), ignorando que la variabilidad de entrega causa el 55% de las roturas reales.",
        "Falta de Defensa Financiera ante Auditoría: Incapacidad de justificar el working capital inmovilizado ante el CFO, auditoría externa y entidades bancarias de crédito."
    ]
    bullets_l_en = [
        "Massive Overstock in Stable SKUs: Carrying 21 days of stock on predictable items with fast lead times unnecessarily ties up $185,000 of dormant capital without commercial return.",
        "Critical Shortages on Volatile Items: On components with overseas lead times (L > 25 days) and high demand dispersion (σd), 3 weeks fails to cover lead times, triggering 7.2% stockouts on Class A items.",
        "Blindness to Supplier Tardiness: Empirical rules assume 100% on-time delivery (σL = 0), ignoring that supplier delivery variability triggers over 55% of actual warehouse shortages.",
        "Total Lack of Audit Defense: Inability to justify trapped balance sheet working capital to CFOs, external audit committees and credit rating institutions."
    ]
    bullets_l = bullets_l_es if is_es else bullets_l_en
    for b in bullets_l:
        p_b = tf_l.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.name = FONT_BODY; p_b.font.size = Pt(9); p_b.font.color.rgb = COLOR_TEXT_MAIN
        p_b.space_after = Pt(6)

    # Contenedor Derecho: El Estándar Estocástico Datalaria
    shape_right = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), cont_y, cont_w, cont_h)
    shape_right.fill.solid(); shape_right.fill.fore_color.rgb = COLOR_BLUE_LIGHT
    shape_right.line.color.rgb = COLOR_BLUE_ACCENT; shape_right.line.width = Pt(1.5)
    tf_r = shape_right.text_frame; tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.24); tf_r.margin_top = Inches(0.18)

    p = tf_r.paragraphs[0]
    p.text = "SOLUCIÓN C-LEVEL: MODELO ESTOCÁSTICO INTEGRAL (APICS / MIT CTL)" if is_es else "C-LEVEL SOLUTION: INTEGRAL STOCHASTIC MODEL (APICS / MIT CTL)"
    p.font.name = FONT_HEADING; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_BLUE_ACCENT
    p.space_after = Pt(8)

    bullets_r_es = [
        "Convolución Matemática Exacta: Cálculo de Stock de Seguridad mediante SS = Z · √(L · σd² + d² · σL²), modelando tanto el riesgo de demanda como el retraso de entrega.",
        "Calibración Estratégica ABC: Asignación diferenciada de Nivel de Servicio (98% en A, 95% en B, 90% en C) para maximizar la cobertura en los productos que generan el 80% del margen.",
        "Sincronización del Punto de Pedido (ROP): ROP = (d · L) + SS dispara compras en el momento exacto, eliminando pedidos de urgencia y fletes aéreos de sobrecoste.",
        "Liberación Inmediata de 240.000 €: Desinversión ordenada de excesos en referencias no críticas que financia el stock de protección de los productos estrella."
    ]
    bullets_r_en = [
        "Exact Mathematical Convolution: Safety Stock computed via SS = Z · √(L · σd² + d² · σL²), simultaneously capturing demand spikes and supplier transit variance.",
        "Strategic ABC Calibration: Differential Cycle Service Level allocation (98% on A, 95% on B, 90% on C) concentrating capital on items generating 80% of company margin.",
        "Synchronized Reorder Point (ROP): ROP = (d · L) + SS triggers replenishment at the precise mathematical threshold, eliminating costly express freight air shipments.",
        "Immediate $240,000 Cash Release: Orderly phase-out of overstock on slow movers, self-funding the required protection buffer on core revenue-generating SKUs."
    ]
    bullets_r = bullets_r_es if is_es else bullets_r_en
    for b in bullets_r:
        p_b = tf_r.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.name = FONT_BODY; p_b.font.size = Pt(9); p_b.font.color.rgb = COLOR_TEXT_MAIN
        p_b.space_after = Pt(6)

    # =========================================================================
    # DIAPOSITIVA 2: GRÁFICO DIENTE DE SIERRA & CURVA ASINTÓTICA
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    title_s2 = (
        "El Punto de Pedido sincroniza la reposición con el colchón basal de seguridad, evidenciando que exigir 99.9% a todo el catálogo triplica la deuda sin retorno comercial"
        if is_es else
        "The Reorder Point synchronizes replenishment with safety buffers, proving that demanding 99.9% across all SKUs triples debt without commercial return"
    )
    add_header(s2, title_s2, 2, 3, lang=lang)

    # Panel Izquierdo: Diente de Sierra (Imagen + Tarjeta de Explicación)
    s2.shapes.add_picture(tmp_sawtooth, Inches(0.8), Inches(1.65), width=Inches(5.75))

    desc_box_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.85), Inches(5.75), Inches(1.20))
    desc_box_l.fill.solid(); desc_box_l.fill.fore_color.rgb = COLOR_CARD_BG
    desc_box_l.line.color.rgb = COLOR_BORDER; desc_box_l.line.width = Pt(1)
    tf_dl = desc_box_l.text_frame; tf_dl.word_wrap = True
    tf_dl.margin_left = tf_dl.margin_right = Inches(0.18); tf_dl.margin_top = Inches(0.10)
    p = tf_dl.paragraphs[0]
    p.text = "DINÁMICA OPERATIVA DEL MODELO DIENTE DE SIERRA (SAWTOOTH)" if is_es else "SAWTOOTH REPLENISHMENT OPERATIONAL DYNAMICS"
    p.font.name = FONT_HEADING; p.font.size = Pt(9); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(2)
    p2 = tf_dl.add_paragraph()
    p2.text = (
        "• Punto de Pedido (ROP): Cuando el stock físico desciende a 750 u, el sistema dispara automáticamente el pedido por tamaño EOQ (900 u).\n"
        "• Ventana de Tránsito (Lead Time L = 10d): El pedido arriba exactamente cuando el stock toca el colchón de seguridad (SS = 300 u).\n"
        "• Absorción de Picos: Si la demanda se dispara o el proveedor se retrasa 3 días, el SS absorbe la varianza sin colapso de servicio."
        if is_es else
        "• Reorder Point (ROP): When stock dips to 750 u, system automatically triggers purchase order for Wilson EOQ batch (900 u).\n"
        "• In-Transit Lead Time Window (L = 10d): Shipment arrives exactly as stock touches the safety buffer (SS = 300 u).\n"
        "• Variance Shock Absorption: If demand spikes or supplier is 3 days late, the SS buffer absorbs variance with zero stockout."
    )
    p2.font.name = FONT_BODY; p2.font.size = Pt(8); p2.font.color.rgb = COLOR_TEXT_MAIN

    # Panel Derecho: Curva Asintótica (Imagen + Matriz ABC de Calibración)
    s2.shapes.add_picture(tmp_service, Inches(6.8), Inches(1.65), width=Inches(5.75))

    desc_box_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(5.85), Inches(5.75), Inches(1.20))
    desc_box_r.fill.solid(); desc_box_r.fill.fore_color.rgb = COLOR_CARD_BG
    desc_box_r.line.color.rgb = COLOR_BORDER; desc_box_r.line.width = Pt(1)
    tf_dr = desc_box_r.text_frame; tf_dr.word_wrap = True
    tf_dr.margin_left = tf_dr.margin_right = Inches(0.18); tf_dr.margin_top = Inches(0.10)
    p = tf_dr.paragraphs[0]
    p.text = "POLÍTICA DE CALIBRACIÓN ABC Y LEY DE RENDIMIENTOS DECRECIENTES" if is_es else "ABC CALIBRATION POLICY & LAW OF DIMINISHING RETURNS"
    p.font.name = FONT_HEADING; p.font.size = Pt(9); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(2)
    p2 = tf_dr.add_paragraph()
    p2.text = (
        "• Clase A (98% CSL / Z = 2.05): Colchón estricto en el 20% de SKUs que aportan el 80% de ventas (Inversión: 290.000 €).\n"
        "• Clase B (95% CSL / Z = 1.64): Equilibrio óptimo coste-disponibilidad en rotación media (Inversión: 72.000 €).\n"
        "• Clase C (90% CSL / Z = 1.28): Mínima inmovilización en tornillería y consumibles accesorios (Inversión: 20.400 €).\n"
        "• La Trampa del 99.9%: Elevar todo el catálogo al 99.9% requeriría 880.000 € (+130% de capital inmovilizado ineficiente)."
        if is_es else
        "• Class A (98% CSL / Z = 2.05): Strict protection on the 20% of SKUs driving 80% of revenue (Investment: $290,000).\n"
        "• Class B (95% CSL / Z = 1.64): Optimal cost-availability equilibrium on moderate turnover items (Investment: $72,000).\n"
        "• Class C (90% CSL / Z = 1.28): Minimal capital lockup on fasteners and generic consumables (Investment: $20,400).\n"
        "• The 99.9% Trap: Forcing 99.9% across the board would demand $880,000 (+130% of idle capital with zero financial yield)."
    )
    p2.font.name = FONT_BODY; p2.font.size = Pt(8); p2.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # DIAPOSITIVA 3: PLAN DE COMPRESIÓN DE LEAD TIME & BOARD DECISION GATEWAY
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    title_s3 = (
        "La compresión de plazos y la estabilidad del proveedor liberan un 38% adicional de stock basal: resolución formal para aprobar la política ABC y ejecutar la desinversión de 240.000 €"
        if is_es else
        "Lead time compression and supplier SLA stability release an additional 38% of baseline stock: formal board resolution to approve ABC policy and execute $240,000 cash release"
    )
    add_header(s3, title_s3, 3, 3, lang=lang)

    # MITAD SUPERIOR: 3 PILARES ESTRATÉGICOS DE NEGOCIACIÓN DE LEAD TIME (Inches 1.65 a 3.65)
    pillar_w = Inches(3.75)
    pillar_h = Inches(1.95)
    pillar_y = Inches(1.65)

    pillars_es = [
        ("PILAR 1: COMPRESIÓN DE LEAD TIME (-30% L)",
         "Liberación: +61.000 € de Capital",
         "• Negociación de almacenes de proximidad / consignment stock.\n• Acuerdos de reposición express y slots logísticos fijos.\n• Impacto matemático: Reduce el componente L · σd² en la fórmula estocástica, comprimiendo directamente el stock de seguridad necesario."),
        ("PILAR 2: ESTABILIDAD & SLA DE ENTREGA (-50% σL)",
         "Ahorro de Riesgo: -24% Varianza de Tránsito",
         "• Cláusulas contractuales de penalización por entrega tardía.\n• Cumplimiento garantizado OTIF (On-Time In-Full) ≥ 98%.\n• Impacto matemático: Erradica el multiplicador cuadrático d² · σL², que es el causante del 60% del sobrestock defensivo en artículos de gran consumo."),
        ("PILAR 3: INTEGRACIÓN VMI & GOBERNANZA MENSUAL",
         "Control Continuo: Cero Sorpresas en Cierre",
         "• Conexión EDI / VMI para visibilidad mutua del ROP.\n• Recalibración mensual obligatoria de d, σd, L y σL en Comité.\n• Eliminación de distorsiones estacionales y efecto látigo (Bullwhip Effect) en la cadena de distribución extendida.")
    ]
    pillars_en = [
        ("PILLAR 1: LEAD TIME COMPRESSION (-30% L)",
         "Cash Release: +$61,000 Working Capital",
         "• Negotiate regional vendor buffer / consignment stock agreements.\n• Dedicated express logistics slots and cross-docking.\n• Mathematical impact: Compresses the L · σd² component in the stochastic equation, directly lowering required safety buffer."),
        ("PILLAR 2: SUPPLIER SLA STABILITY (-50% σL)",
         "Risk Reduction: -24% In-Transit Variance",
         "• Strict contract penalty clauses for delivery window breaches.\n• Guaranteed OTIF (On-Time In-Full) performance threshold ≥ 98%.\n• Mathematical impact: Eliminates quadratic multiplier d² · σL², the root cause of 60% of defensive buffer stock in high-volume SKUs."),
        ("PILLAR 3: VMI INTEGRATION & GOVERNANCE",
         "Continuous Control: Zero Balance Surprises",
         "• EDI / VMI connection providing supplier real-time ROP visibility.\n• Mandatory monthly recalibration of d, σd, L, and σL in Committee.\n• Eradication of seasonal demand distortion and the Bullwhip Effect across the extended supply network.")
    ]
    pillars = pillars_es if is_es else pillars_en

    for idx, (p_title, p_badge, p_text) in enumerate(pillars):
        x = Inches(0.8) + idx * (pillar_w + Inches(0.24))
        p_shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, pillar_y, pillar_w, pillar_h)
        p_shape.fill.solid(); p_shape.fill.fore_color.rgb = COLOR_CARD_BG
        p_shape.line.color.rgb = COLOR_BLUE_ACCENT; p_shape.line.width = Pt(1.5)
        tf_p = p_shape.text_frame; tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_right = Inches(0.18); tf_p.margin_top = Inches(0.12)

        p = tf_p.paragraphs[0]
        p.text = p_title
        p.font.name = FONT_HEADING; p.font.size = Pt(8.5); p.font.bold = True; p.font.color.rgb = COLOR_NAVY_DARK
        p.space_after = Pt(2)

        p_sub = tf_p.add_paragraph()
        p_sub.text = p_badge
        p_sub.font.name = FONT_HEADING; p_sub.font.size = Pt(8); p_sub.font.bold = True; p_sub.font.color.rgb = COLOR_GREEN_TEXT
        p_sub.space_after = Pt(4)

        p_bod = tf_p.add_paragraph()
        p_bod.text = p_text
        p_bod.font.name = FONT_BODY; p_bod.font.size = Pt(7.5); p_bod.font.color.rgb = COLOR_TEXT_MAIN

    # MITAD INFERIOR: BOARD DECISION GATEWAY (Inches 3.80 a 7.10)
    bg_gate = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.78), Inches(11.73), Inches(3.28))
    bg_gate.fill.solid(); bg_gate.fill.fore_color.rgb = COLOR_NAVY_DARK
    bg_gate.line.color.rgb = COLOR_BLUE_ACCENT; bg_gate.line.width = Pt(2)

    tf_gate = bg_gate.text_frame; tf_gate.word_wrap = True
    tf_gate.margin_left = tf_gate.margin_right = Inches(0.25); tf_gate.margin_top = Inches(0.16)

    p_gh = tf_gate.paragraphs[0]
    p_gh.text = "DECISIÓN REQUERIDA DEL COMITÉ DE DIRECCIÓN / BOARD DECISION GATEWAY" if is_es else "BOARD DECISION GATEWAY: FORMAL EXECUTIVE ACTION MANDATE"
    p_gh.font.name = FONT_HEADING; p_gh.font.size = Pt(11); p_gh.font.bold = True; p_gh.font.color.rgb = COLOR_WHITE
    p_gh.space_after = Pt(4)

    resolutions_es = (
        "1. Aprobación Formal de la Política de Servicio ABC: Adoptar como estándar vinculante los niveles de servicio del 98% (Clase A), 95% (Clase B) y 90% (Clase C), prohibiendo las reglas heurísticas indiscriminadas.\n"
        "2. Autorización del Plan de Desinversión de Sobre-stock: Ejecutar un programa ordenado de reducción de inventario inerte para liberar 240.000 € de circulante en los próximos 90 días.\n"
        "3. Mandato a Compras para Contratos SLA con Proveedores Críticos: Incorporar cláusulas de penalización por desvío de entrega (reduciendo σL a la mitad) en las renovaciones contractuales.\n"
        "4. Institución del Cuadro de Mando Mensual de Roturas: Monitorizar mensualmente en Comité Ejecutivo el Nivel de Servicio Real vs. Objetivo y la inmovilización de Working Capital."
    )
    resolutions_en = (
        "1. Formal Approval of ABC Service Level Policy: Mandate target cycle service levels of 98% (Class A), 95% (Class B), and 90% (Class C), eliminating arbitrary empirical rules across all plants.\n"
        "2. Authorization of Overstock Liquidation Plan: Authorize execution of an orderly 90-day phase-out of idle safety inventory to release $240,000 in liquid working capital.\n"
        "3. Procurement Mandate for Critical Supplier SLAs: Mandate strict contractual lead time variance penalties (targeting 50% σL reduction) in all Class A supplier renewals.\n"
        "4. Institution of Monthly Executive Stockout Dashboard: Implement monthly Board-level reporting on realized Service Levels, stockout occurrences, and Working Capital carrying costs."
    )
    p_res = tf_gate.add_paragraph()
    p_res.text = resolutions_es if is_es else resolutions_en
    p_res.font.name = FONT_BODY; p_res.font.size = Pt(8.5); p_res.font.color.rgb = RGBColor(226, 232, 240)
    p_res.space_after = Pt(8)

    # Cajas de Firma Ejecutiva (CEO, CFO, COO)
    box_w = Inches(3.60)
    box_h = Inches(0.82)
    box_y = Inches(6.08)

    signatures_es = [
        ("CEO / CONSEJERO DELEGADO", "Aprobación Política Estratégica"),
        ("CFO / DIRECTOR FINANCIERO", "Autorización Retorno Working Capital"),
        ("COO / DIR. OPERACIONES & SCM", "Validación Operativa ROP & Niveles ABC")
    ]
    signatures_en = [
        ("CHIEF EXECUTIVE OFFICER (CEO)", "Strategic Policy Ratification"),
        ("CHIEF FINANCIAL OFFICER (CFO)", "Working Capital Release Authorization"),
        ("CHIEF OPERATING OFFICER (COO)", "Operational ROP & ABC Model Validation")
    ]
    signatures = signatures_es if is_es else signatures_en

    for idx, (role_name, role_sub) in enumerate(signatures):
        bx = Inches(1.05) + idx * (box_w + Inches(0.24))
        sign_shape = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, box_y, box_w, box_h)
        sign_shape.fill.solid(); sign_shape.fill.fore_color.rgb = COLOR_NAVY_MED
        sign_shape.line.color.rgb = RGBColor(71, 85, 105); sign_shape.line.width = Pt(1)

        tf_s = sign_shape.text_frame; tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = Inches(0.12); tf_s.margin_top = Inches(0.06)

        p = tf_s.paragraphs[0]
        p.text = role_name
        p.font.name = FONT_HEADING; p.font.size = Pt(7.5); p.font.bold = True; p.font.color.rgb = RGBColor(148, 163, 184)

        p_sub = tf_s.add_paragraph()
        p_sub.text = role_sub
        p_sub.font.name = FONT_BODY; p_sub.font.size = Pt(7); p_sub.font.color.rgb = RGBColor(203, 213, 225)

        p_line = tf_s.add_paragraph()
        p_line.text = "Firma: _____________________  Fecha: __/__/2026" if is_es else "Signature: __________________  Date: __/__/2026"
        p_line.font.name = FONT_BODY; p_line.font.size = Pt(7); p_line.font.color.rgb = RGBColor(100, 116, 139)

    # Limpiar imágenes temporales al finalizar
    if os.path.exists(tmp_sawtooth):
        os.remove(tmp_sawtooth)
    if os.path.exists(tmp_service):
        os.remove(tmp_service)

    return prs


def main():
    """Genera las presentaciones ejecutivas y las almacena en las carpetas oficiales."""
    base_dir = "packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP"
    es_dir = os.path.join(base_dir, "[ES]_Stock_Seguridad_ROP")
    en_dir = os.path.join(base_dir, "[EN]_Safety_Stock_ROP")

    os.makedirs(es_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)

    file_es = os.path.join(es_dir, "Presentacion_Stock_ROP_CLevel_ES.pptx")
    file_en = os.path.join(en_dir, "Deck_Safety_Stock_ROP_CLevel_EN.pptx")

    print("[1/2] Generando Presentación Ejecutiva en Español (Presentacion_Stock_ROP_CLevel_ES.pptx)...")
    prs_es = build_presentation(lang="ES")
    prs_es.save(file_es)
    print(f"      -> Guardado: {file_es}")

    print("[2/2] Generating C-Level Deck in English (Deck_Safety_Stock_ROP_CLevel_EN.pptx)...")
    prs_en = build_presentation(lang="EN")
    prs_en.save(file_en)
    print(f"      -> Saved: {file_en}")

    print("Presentaciones ejecutivas PPTX 16:9 generadas con total éxito.")


if __name__ == "__main__":
    main()
