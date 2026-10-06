#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE/[ES]_Matriz_Riesgos_AMFE/Presentacion_AMFE_Riesgos_CLevel_ES.pptx
2. packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE/[EN]_FMEA_Risk_Matrix/Deck_FMEA_Risk_CLevel_EN.pptx

Características de diseño Tier-1 (ISO 31000 / AIAG-VDA / McKinsey Risk Practice):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Pirámide de Minto y Action Titles contundentes.
- Diapositiva 1: Diagnóstico Ejecutivo & Exposición al Riesgo (4 KPI Cards y diagnóstico de riesgo).
- Diapositiva 2: Matriz de Calor 5x5 & Curva Pareto de Modos de Fallo (Matriz ISO 31000 y gráfico Pareto de NPRs).
- Diapositiva 3: Plan de Mitigación Q1-Q4 & Board Decision Gateway (4 resoluciones ejecutivas y firmas).
- Sin solapes de texto, márgenes protegidos y acabados visuales pulidos.
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
COLOR_TEAL_ACCENT = RGBColor(13, 148, 136)   # #0D9488 Teal 600
COLOR_TEAL_LIGHT = RGBColor(240, 253, 250)   # #F0FDFA Teal 50

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
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = ("DATALARIA EXECUTIVE DECISION PACK · GESTIÓN CUANTITATIVA DE RIESGOS · ISO 31000 / AIAG-VDA"
                if lang == 'ES' else
                "DATALARIA EXECUTIVE DECISION PACK · QUANTITATIVE RISK MANAGEMENT · ISO 31000 / AIAG-VDA")
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_TEAL_ACCENT
    p_b.font.name = FONT_HEADING

    tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.85))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.size = Pt(13.5)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK
    p_t.font.name = FONT_HEADING

    # Pie institucional
    tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.7), Inches(0.25))
    tf_f = tb_foot.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = (f"Datalaria.com · Documento Confidencial para Comité de Dirección & Auditoría de Riesgos | Diapositiva {slide_num} de {total_slides}"
                if lang == 'ES' else
                f"Datalaria.com · Confidential Executive Committee & Risk Audit Document | Slide {slide_num} of {total_slides}")
    p_f.font.size = Pt(8)
    p_f.font.color.rgb = COLOR_TEXT_MUTED
    p_f.font.name = FONT_BODY


def create_pareto_chart(lang='ES', out_path='temp_pareto_chart.png'):
    """Genera gráfico Pareto de Modos de Fallo por NPR para la Diapositiva 2."""
    fig, ax1 = plt.subplots(figsize=(6.2, 3.4), dpi=220)

    modes_es = ['Autenticación Indebida', 'Fallo Pasarela Pagos', 'Corrupción BBDD', 'Saturación Proxy', 'Bug Crítico CI/CD', 'Fallo Robótico Soldadura', 'Líquido en Servidores', 'Desfase Colas Eventos']
    modes_en = ['Unauthorized Auth', 'Payment Gateway Fail', 'Database Corruption', 'Proxy Memory Sat.', 'CI/CD Blocker Bug', 'Robotic Weld Drift', 'Rack Coolant Leak', 'Event Broker Lag']
    modes = modes_es if lang == 'ES' else modes_en

    # NPR values (ordenados de mayor a menor)
    rpn = [441, 336, 360, 288, 288, 360, 288, 294]
    # Sorted
    sorted_indices = np.argsort(rpn)[::-1]
    modes_sorted = [modes[i] for i in sorted_indices]
    rpn_sorted = [rpn[i] for i in sorted_indices]

    cum_pct = np.cumsum(rpn_sorted) / np.sum(rpn_sorted) * 100

    x_pos = np.arange(len(modes_sorted))
    colors_bars = ['#DC2626' if v >= 300 else ('#D97706' if v >= 200 else '#2563EB') for v in rpn_sorted]

    bars = ax1.bar(x_pos, rpn_sorted, color=colors_bars, width=0.6, label='NPR Inherente' if lang == 'ES' else 'Inherent RPN')
    ax1.set_ylabel('Número de Prioridad de Riesgo (NPR)' if lang == 'ES' else 'Risk Priority Number (RPN)', fontsize=8, color='#0F172A', fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(modes_sorted, rotation=35, ha='right', fontsize=7.5, color='#1E293B')
    ax1.set_ylim(0, 500)
    ax1.grid(axis='y', linestyle='--', alpha=0.3, color='#94A3B8')

    # Línea 80/20 acumulada
    ax2 = ax1.twinx()
    ax2.plot(x_pos, cum_pct, color='#0D9488', marker='o', linewidth=2, markersize=4, label='% Acumulado' if lang == 'ES' else '% Cumulative')
    ax2.axhline(80, color='#DC2626', linestyle=':', linewidth=1.2, alpha=0.8, label='Línea 80/20' if lang == 'ES' else '80/20 Threshold')
    ax2.set_ylabel('% Acumulado' if lang == 'ES' else '% Cumulative', fontsize=8, color='#0D9488', fontweight='bold')
    ax2.set_ylim(0, 110)

    for bar, val in zip(bars, rpn_sorted):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 10, str(val),
                 va='bottom', ha='center', fontsize=7, fontweight='bold', color='#0F172A')

    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.spines['left'].set_color('#CBD5E1')
    ax1.spines['bottom'].set_color('#CBD5E1')

    plt.title('Curva Pareto de Criticidad AIAG-VDA (Regla 80/20)' if lang == 'ES' else 'AIAG-VDA Criticality Pareto Curve (80/20 Rule)', fontsize=8.5, fontweight='bold', pad=10, color='#0F172A')
    plt.tight_layout()
    fig.savefig(out_path, dpi=220, bbox_inches='tight')
    plt.close(fig)
    return out_path


def create_deck(lang='ES', out_path=None):
    if out_path is None:
        base_dir = "packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE"
        sub_dir = "[ES]_Matriz_Riesgos_AMFE" if lang == 'ES' else "[EN]_FMEA_Risk_Matrix"
        fname = "Presentacion_AMFE_Riesgos_CLevel_ES.pptx" if lang == 'ES' else "Deck_FMEA_Risk_CLevel_EN.pptx"
        out_path = os.path.join(base_dir, sub_dir, fname)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================================================
    # SLIDE 1: DIAGNÓSTICO EJECUTIVO & EXPOSICIÓN AL RIESGO
    # ==========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    title_s1 = (
        "El 64% de la exposición al riesgo operacional se concentra en 3 modos de fallo críticos de infraestructura con NPR > 150: una inversión de 360.000 € reducirá el riesgo residual en un 71% antes de Q4"
        if lang == 'ES' else
        "64% of operational risk exposure concentrates in 3 critical infrastructure failure modes with RPN > 150: a €360,000 investment will cut residual risk by 71% before Q4"
    )
    add_header(slide1, title_s1, 1, 3, lang=lang)

    # 4 Tarjetas KPI
    card_w = Inches(2.78)
    card_h = Inches(1.35)
    card_y = Inches(1.60)

    cards_data_es = [
        ("EXPOSICIÓN AL RIESGO PRE-CONTROL", "1.870.000 €", "Pérdida Financiera Esperada E(L)", "F8FAFC", "EFF6FF", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT, COLOR_TEXT_MUTED),
        ("MODO DE FALLO #1 (NPR MÁXIMO)", "441 NPR", "Autenticación Indebida / Ransomware", "FFF1F2", "FEE2E2", COLOR_RED_BORDER, COLOR_RED_TEXT, COLOR_RED_TEXT),
        ("REDUCCIÓN DE RIESGO RESIDUAL", "71,4%", "Disminución media post-mitigación", "F0FDFA", "CCFBF1", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT, COLOR_GREEN_TEXT),
        ("PRESUPUESTO CAPEX REQUERIDO", "360.000 €", "ROI Global del Control: 4,4x", "FFFBEB", "FEF3C7", COLOR_AMBER_BORDER, COLOR_AMBER_TEXT, COLOR_AMBER_TEXT),
    ]
    cards_data_en = [
        ("PRE-CONTROL RISK EXPOSURE", "€1,870,000", "Total Expected Financial Loss E(L)", "F8FAFC", "EFF6FF", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT, COLOR_TEXT_MUTED),
        ("TOP FAILURE MODE (MAX RPN)", "441 RPN", "Unauthorized Auth / Ransomware", "FFF1F2", "FEE2E2", COLOR_RED_BORDER, COLOR_RED_TEXT, COLOR_RED_TEXT),
        ("RESIDUAL RISK REDUCTION", "71.4%", "Average decrease post-mitigation", "F0FDFA", "CCFBF1", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT, COLOR_GREEN_TEXT),
        ("REQUIRED CAPEX BUDGET", "€360,000", "Overall Control ROI: 4.4x", "FFFBEB", "FEF3C7", COLOR_AMBER_BORDER, COLOR_AMBER_TEXT, COLOR_AMBER_TEXT),
    ]
    cards_data = cards_data_es if lang == 'ES' else cards_data_en

    for idx, (lbl, val, sub, grad_c1, grad_c2, border_col, val_col, sub_col) in enumerate(cards_data):
        cx = Inches(0.8 + idx * 2.97)
        shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        apply_gradient_fill(shape, grad_c1, grad_c2, angle_deg=90)
        shape.line.color.rgb = border_col
        shape.line.width = Pt(1.5)

        tb = slide1.shapes.add_textbox(cx + Inches(0.12), card_y + Inches(0.1), card_w - Inches(0.24), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = lbl
        p0.font.size = Pt(8)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_DARK
        p0.font.name = FONT_HEADING

        p1 = tf.add_paragraph()
        p1.text = val
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = val_col
        p1.font.name = FONT_HEADING

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = sub_col
        p2.font.name = FONT_BODY

    # Dos Paneles Inferiores de Diagnóstico (Izquierdo y Derecho)
    panel_y = Inches(3.15)
    panel_w = Inches(5.72)
    panel_h = Inches(3.70)

    # Panel 1: Hallazgos de Auditoría de Riesgos (ISO 31000 & AIAG-VDA)
    p1_shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), panel_y, panel_w, panel_h)
    p1_shape.fill.solid()
    p1_shape.fill.fore_color.rgb = COLOR_CARD_BG
    p1_shape.line.color.rgb = COLOR_BORDER
    p1_shape.line.width = Pt(1)

    tb_p1 = slide1.shapes.add_textbox(Inches(0.95), panel_y + Inches(0.15), panel_w - Inches(0.3), panel_h - Inches(0.3))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True
    tf_p1.margin_left = tf_p1.margin_top = tf_p1.margin_right = tf_p1.margin_bottom = 0

    p_p1_h = tf_p1.paragraphs[0]
    p_p1_h.text = "DIAGNÓSTICO DE VULNERABILIDAD & MATRIZ DE RIESGOS" if lang == 'ES' else "VULNERABILITY DIAGNOSIS & RISK MATRIX AUDIT"
    p_p1_h.font.size = Pt(10.5)
    p_p1_h.font.bold = True
    p_p1_h.font.color.rgb = COLOR_NAVY_DARK

    findings_es = [
        ("• Concentración de Riesgos Críticos: ", "5 de los 20 riesgos evaluados bajo ISO 31000 se sitúan en Zona Crítica (Score ≥ 15), destacando ciberataques y caídas de infraestructura cloud."),
        ("• Sesgo Cualitativo Eliminado: ", "La cuantificación mediante baremos 1-10 en Severidad, Ocurrencia y Detección revela 6 modos de fallo con Prioridad de Acción Alta (NPR ≥ 120 o S ≥ 9)."),
        ("• Pérdida Esperada Desprotegida: ", "El valor actuarial esperado E(L) sin controles de contingencia asciende a 1.870.000 €, superando el apetito de riesgo corporativo del Board (máximo fijado en 500.000 €)."),
        ("• Detección Tardía como Multiplicador: ", "El 60% de los modos de fallo severos carece de telemetría automática, arrojando puntuaciones de Detección D ≥ 7 (detección reactiva por clientes).")
    ]
    findings_en = [
        ("• Critical Risk Concentration: ", "5 of 20 risks audited under ISO 31000 occupy the Critical Zone (Score ≥ 15), led by targeted ransomware and multi-region cloud outages."),
        ("• Qualitative Bias Eliminated: ", "Strict 1-10 quantitative scoring across Severity, Occurrence, and Detection isolates 6 failure modes with High Action Priority (RPN ≥ 120 or S ≥ 9)."),
        ("• Unmitigated Expected Loss: ", "Pre-control actuarial loss E(L) reaches €1,870,000, severely breaching the corporate risk appetite limit set by the Board (€500,000 ceiling)."),
        ("• Latent Detection as Risk Multiplier: ", "60% of severe failure modes lack automated telemetry, driving Detection ratings D ≥ 7 (reactive detection via angry customer tickets).")
    ]
    findings = findings_es if lang == 'ES' else findings_en

    for b_lbl, b_txt in findings:
        p = tf_p1.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = b_lbl
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = COLOR_NAVY_DARK
        r2 = p.add_run()
        r2.text = b_txt
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # Panel 2: Impacto Financiero y Decisión Operativa
    p2_shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), panel_y, panel_w, panel_h)
    p2_shape.fill.solid()
    p2_shape.fill.fore_color.rgb = COLOR_CARD_BG
    p2_shape.line.color.rgb = COLOR_BORDER
    p2_shape.line.width = Pt(1)

    tb_p2 = slide1.shapes.add_textbox(Inches(6.95), panel_y + Inches(0.15), panel_w - Inches(0.3), panel_h - Inches(0.3))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True
    tf_p2.margin_left = tf_p2.margin_top = tf_p2.margin_right = tf_p2.margin_bottom = 0

    p_p2_h = tf_p2.paragraphs[0]
    p_p2_h.text = "EFICACIA DEL CONTROL & RENTABILIDAD DEL CAPEX (ROI)" if lang == 'ES' else "CONTROL EFFICACY & CAPEX PROFITABILITY (ROI)"
    p_p2_h.font.size = Pt(10.5)
    p_p2_h.font.bold = True
    p_p2_h.font.color.rgb = COLOR_NAVY_DARK

    impacts_es = [
        ("• Retorno Económico de la Mitigación (CER): ", "La inversión de 360.000 € evita pérdidas esperadas netas por 1.588.000 €, generando un Cost-Effectiveness Ratio medio de 4,4x."),
        ("• Despliegue de Resiliencia Multi-Cloud: ", "La arquitectura activa-activa (65.000 €) abate la pérdida esperada de 320.000 € a 48.000 €, garantizando RTO < 5 min."),
        ("• Detección Automática Preventiva: ", "La implementación de llaves FIDO2 hardware y WAF reduce la ocurrencia y detección en credential stuffing, recortando el NPR de 441 a 36."),
        ("• Blindaje Legal y Regulatorio: ", "La auditoría KMS y explicabilidad del algoritmo erradican la exposición a sanciones de hasta 20 M€ bajo GDPR y el reglamento EU AI Act.")
    ]
    impacts_en = [
        ("• Economic Return of Mitigation (CER): ", "A €360,000 investment mitigates €1,588,000 in net expected losses, yielding an average Cost-Effectiveness Ratio of 4.4x."),
        ("• Multi-Cloud Active Resiliency: ", "Active-active deployment (€65,000) drives expected downtime loss from €320,000 down to €48,000, enforcing RTO < 5 min."),
        ("• Automated Preventive Telemetry: ", "Hardware FIDO2 enforcement and WAF drops credential stuffing occurrence and detection, crashing RPN from 441 to 36."),
        ("• Regulatory & Compliance Ringfence: ", "KMS encryption audit and model explainability eliminate sanction exposures up to €20M under GDPR and EU AI Act.")
    ]
    impacts = impacts_es if lang == 'ES' else impacts_en

    for b_lbl, b_txt in impacts:
        p = tf_p2.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = b_lbl
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = COLOR_NAVY_DARK
        r2 = p.add_run()
        r2.text = b_txt
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================================================
    # SLIDE 2: MATRIZ DE CALOR 5x5 & CURVA PARETO DE MODOS DE FALLO
    # ==========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    title_s2 = (
        "Matriz térmica 5x5 de riesgos inherentes y Curva Pareto de Modos de Fallo: 8 fallos técnicos concentran el 82% del Número de Prioridad de Riesgo de la compañía"
        if lang == 'ES' else
        "5x5 Inherent Risk Heatmap and Failure Modes Pareto Curve: 8 technical failure modes account for 82% of total corporate Risk Priority Number"
    )
    add_header(slide2, title_s2, 2, 3, lang=lang)

    col_y = Inches(1.55)
    col_w = Inches(5.72)
    col_h = Inches(5.30)

    # Contenedor Izquierdo: Matriz de Calor 5x5
    s_heat = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), col_y, col_w, col_h)
    s_heat.fill.solid()
    s_heat.fill.fore_color.rgb = COLOR_CARD_BG
    s_heat.line.color.rgb = COLOR_BORDER
    s_heat.line.width = Pt(1)

    tb_heat_h = slide2.shapes.add_textbox(Inches(0.95), col_y + Inches(0.12), col_w - Inches(0.3), Inches(0.35))
    tf_hh = tb_heat_h.text_frame
    tf_hh.margin_left = tf_hh.margin_top = tf_hh.margin_right = tf_hh.margin_bottom = 0
    p_hh = tf_hh.paragraphs[0]
    p_hh.text = "MATRIZ DE CALOR 5x5: PROBABILIDAD VS. IMPACTO" if lang == 'ES' else "5x5 HEAT MAP: PROBABILITY VS. IMPACT"
    p_hh.font.size = Pt(10.5)
    p_hh.font.bold = True
    p_hh.font.color.rgb = COLOR_NAVY_DARK

    # Dibujar la cuadrícula 5x5 de la matriz en slide 2
    grid_x0 = Inches(1.5)
    grid_y0 = col_y + Inches(0.65)
    cell_gw = Inches(0.94)
    cell_gh = Inches(0.64)

    # Coordenadas y número de eventos modelados por celda (P, I)
    matrix_counts = {
        (5, 4): ("RIE-01", "FEE2E2", COLOR_RED_BORDER),
        (4, 3): ("RIE-02\nRIE-06", "FEF3C7", COLOR_AMBER_BORDER),
        (4, 4): ("RIE-03\nRIE-07\nRIE-09\nRIE-15", "FEE2E2", COLOR_RED_BORDER),
        (5, 2): ("RIE-04", "FEF3C7", COLOR_AMBER_BORDER),
        (3, 4): ("RIE-05\nRIE-16\nRIE-19", "FEF3C7", COLOR_AMBER_BORDER),
        (5, 3): ("RIE-08\nRIE-17", "FEE2E2", COLOR_RED_BORDER),
        (4, 2): ("RIE-11", "FEF3C7", COLOR_AMBER_BORDER),
        (3, 3): ("RIE-12\nRIE-14\nRIE-20", "FEF3C7", COLOR_AMBER_BORDER),
        (3, 2): ("RIE-18", "D1FAE5", COLOR_GREEN_BORDER),
    }

    # Labels de Eje Y (Probabilidad 5 a 1)
    p_labels = ["5: Muy Alta", "4: Alta", "3: Media", "2: Baja", "1: Muy Baja"] if lang == 'ES' else ["5: Very High", "4: High", "3: Medium", "2: Low", "1: Very Low"]
    for p_idx, p_txt in enumerate(p_labels):
        py = grid_y0 + Inches(p_idx * 0.68)
        tb_p = slide2.shapes.add_textbox(Inches(0.85), py, Inches(0.62), cell_gh)
        tf_p = tb_p.text_frame
        tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
        p_p = tf_p.paragraphs[0]
        p_p.text = p_txt
        p_p.font.size = Pt(6.8)
        p_p.font.bold = True
        p_p.font.color.rgb = COLOR_TEXT_MUTED

    # Eje X Labels (Impacto 1 a 5)
    i_labels = ["1: M.Bajo", "2: Bajo", "3: Medio", "4: Alto", "5: Crítico"] if lang == 'ES' else ["1: V.Low", "2: Low", "3: Medium", "4: High", "5: Critical"]
    for i_idx, i_txt in enumerate(i_labels):
        px = grid_x0 + Inches(i_idx * 0.96)
        tb_i = slide2.shapes.add_textbox(px, grid_y0 + Inches(3.45), cell_gw, Inches(0.25))
        tf_i = tb_i.text_frame
        tf_i.margin_left = tf_i.margin_top = tf_i.margin_right = tf_i.margin_bottom = 0
        p_i = tf_i.paragraphs[0]
        p_i.text = i_txt
        p_i.font.size = Pt(7)
        p_i.font.bold = True
        p_i.font.color.rgb = COLOR_TEXT_MUTED
        p_i.alignment = PP_ALIGN.CENTER

    for row_p in range(5, 0, -1):
        for col_i in range(1, 6):
            cell_x = grid_x0 + Inches((col_i - 1) * 0.96)
            cell_y = grid_y0 + Inches((5 - row_p) * 0.68)

            score = row_p * col_i
            if score >= 15:
                default_bg = "FEE2E2"
                default_border = COLOR_RED_BORDER
            elif score >= 8:
                default_bg = "FEF3C7"
                default_border = COLOR_AMBER_BORDER
            else:
                default_bg = "D1FAE5"
                default_border = COLOR_GREEN_BORDER

            cell_val, bg_hex, border_c = matrix_counts.get((row_p, col_i), ("", default_bg, default_border))

            c_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cell_x, cell_y, cell_gw, cell_gh)
            c_box.fill.solid()
            c_box.fill.fore_color.rgb = RGBColor.from_string(bg_hex)
            c_box.line.color.rgb = border_c
            c_box.line.width = Pt(1)

            tb_c = slide2.shapes.add_textbox(cell_x + Inches(0.04), cell_y + Inches(0.04), cell_gw - Inches(0.08), cell_gh - Inches(0.08))
            tf_c = tb_c.text_frame
            tf_c.word_wrap = True
            tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

            p_cell = tf_c.paragraphs[0]
            p_cell.text = cell_val if cell_val else f"{score}"
            p_cell.font.size = Pt(6.8) if cell_val else Pt(8)
            p_cell.font.bold = True
            p_cell.font.color.rgb = COLOR_NAVY_DARK if cell_val else COLOR_TEXT_MUTED
            p_cell.alignment = PP_ALIGN.CENTER

    # Caja de Resumen de Cuadrantes en la base del contenedor izquierdo
    box_res_y = col_y + Inches(4.25)
    b_res = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), box_res_y, col_w - Inches(0.3), Inches(0.92))
    b_res.fill.solid()
    b_res.fill.fore_color.rgb = COLOR_WHITE
    b_res.line.color.rgb = COLOR_BORDER
    b_res.line.width = Pt(1)

    tb_bres = slide2.shapes.add_textbox(Inches(1.05), box_res_y + Inches(0.06), col_w - Inches(0.5), Inches(0.8))
    tf_bres = tb_bres.text_frame
    tf_bres.word_wrap = True
    tf_bres.margin_left = tf_bres.margin_top = tf_bres.margin_right = tf_bres.margin_bottom = 0

    p_br0 = tf_bres.paragraphs[0]
    p_br0.text = "BALANCE DE CUADRANTES DE RIESGO INHERENTE" if lang == 'ES' else "INHERENT RISK QUADRANT SUMMARY"
    p_br0.font.size = Pt(8.5)
    p_br0.font.bold = True
    p_br0.font.color.rgb = COLOR_NAVY_DARK

    p_br1 = tf_bres.add_paragraph()
    p_br1.text = ("• Zona Crítica (Score 15-25): 5 eventos (25%) · Requieren mitigación inmediata\n"
                  "• Zona Media (Score 8-12): 14 eventos (70%) · Monitoreo y transferencias preventivas\n"
                  "• Zona Baja (Score 1-6): 1 evento (5%) · Riesgo asumible bajo apetito corporativo"
                  if lang == 'ES' else
                  "• Critical Zone (Score 15-25): 5 events (25%) · Mandatory immediate mitigation\n"
                  "• Medium Zone (Score 8-12): 14 events (70%) · Ongoing controls & hedging\n"
                  "• Low Zone (Score 1-6): 1 event (5%) · Acceptable under Board risk appetite")
    p_br1.font.size = Pt(7.2)
    p_br1.font.color.rgb = COLOR_TEXT_MAIN

    # Contenedor Derecho: Gráfico Pareto de Modos de Fallo
    s_chart = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), col_y, col_w, col_h)
    s_chart.fill.solid()
    s_chart.fill.fore_color.rgb = COLOR_CARD_BG
    s_chart.line.color.rgb = COLOR_BORDER
    s_chart.line.width = Pt(1)

    chart_img = create_pareto_chart(lang=lang, out_path=f"temp_pareto_{lang}.png")
    slide2.shapes.add_picture(chart_img, Inches(6.9), col_y + Inches(0.15), width=Inches(5.52))

    # Caja de Causas Raíz Críticas en la base del contenedor derecho
    pat_y = col_y + Inches(3.70)
    pat_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95), pat_y, Inches(5.42), Inches(1.48))
    pat_box.fill.solid()
    pat_box.fill.fore_color.rgb = COLOR_WHITE
    pat_box.line.color.rgb = COLOR_BORDER
    pat_box.line.width = Pt(1)

    tb_pat = slide2.shapes.add_textbox(Inches(7.05), pat_y + Inches(0.06), Inches(5.22), Inches(1.36))
    tf_pat = tb_pat.text_frame
    tf_pat.word_wrap = True
    tf_pat.margin_left = tf_pat.margin_top = tf_pat.margin_right = tf_pat.margin_bottom = 0

    p_ph = tf_pat.paragraphs[0]
    p_ph.text = "CAUSAS RAÍZ CRÍTICAS DETECTADAS (AIAG-VDA)" if lang == 'ES' else "CRITICAL ROOT CAUSES IDENTIFIED (AIAG-VDA)"
    p_ph.font.size = Pt(8.5)
    p_ph.font.bold = True
    p_ph.font.color.rgb = COLOR_NAVY_DARK

    roots_es = [
        ("• Dependencia de Proveedor Único: ", "Falta de multiaquirente y proveedor DNS redundante."),
        ("• Controles de Entrada Débiles: ", "Ausencia de hardware MFA y rate-limiting frente a credential stuffing."),
        ("• Mantenimiento Reactivo: ", "Inspección humana al final de línea sin sensores IoT de vibración."),
        ("• Telemetría Asíncrona Lenta: ", "Detección de corrupción de bases de datos mediante reportes de clientes.")
    ]
    roots_en = [
        ("• Single-Point-of-Failure Dependencies: ", "Lack of secondary acquirers and independent dual-DNS topology."),
        ("• Weak Perimeter Entry Controls: ", "Missing hardware MFA and adaptive WAF rate-limiting."),
        ("• Reactive Maintenance Deficit: ", "Human visual line QA lacking IoT predictive vibration telemetry."),
        ("• Latent Customer-Driven Detection: ", "Database drift discovered through end-user support escalations.")
    ]
    roots = roots_es if lang == 'ES' else roots_en
    for b_lbl, b_txt in roots:
        p = tf_pat.add_paragraph()
        r1 = p.add_run()
        r1.text = b_lbl
        r1.font.bold = True
        r1.font.size = Pt(7.5)
        r1.font.color.rgb = COLOR_NAVY_DARK
        r2 = p.add_run()
        r2.text = b_txt
        r2.font.size = Pt(7.2)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================================================
    # SLIDE 3: PLAN DE MITIGACIÓN & BOARD DECISION GATEWAY
    # ==========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    title_s3 = (
        "Cronograma Q1-Q4 de implantación de controles preventivos y Board Decision Gateway para ratificar la inversión de 360.000 € y los umbrales de apetito de riesgo"
        if lang == 'ES' else
        "Q1-Q4 preventive control implementation roadmap alongside Board Decision Gateway authorizing the €360,000 CAPEX allocation and corporate risk thresholds"
    )
    add_header(slide3, title_s3, 3, 3, lang=lang)

    # MITAD SUPERIOR: ROADMAP DE 4 FASES (Y = 1.55 a 3.80)
    tb_rm_h = slide3.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.7), Inches(0.3))
    tf_rm_h = tb_rm_h.text_frame
    tf_rm_h.margin_left = tf_rm_h.margin_top = tf_rm_h.margin_right = tf_rm_h.margin_bottom = 0
    p_rm = tf_rm_h.paragraphs[0]
    p_rm.text = "CRONOGRAMA DE IMPLEMENTACIÓN DE CONTROLES (Q1 - Q4)" if lang == 'ES' else "PREVENTIVE CONTROLS IMPLEMENTATION TIMELINE (Q1 - Q4)"
    p_rm.font.size = Pt(10.5)
    p_rm.font.bold = True
    p_rm.font.color.rgb = COLOR_NAVY_DARK

    phases_es = [
        ("Q1: BLINDAJE CRÍTICO", "Presupuesto: 110.000 €", "MFA FIDO2 & Dual-DNS", "Despliegue de llaves físicas Zero Trust para accesos root. Activación de arquitectura Dual-DNS y fallback de pasarela de pagos. Recorte inmediato de NPR > 400."),
        ("Q2: RESILIENCIA & RESIDUALES", "Presupuesto: 145.000 €", "Cloud Multi-Región & IoT", "Despliegue de clúster activo-activo en AWS. Dual-sourcing europeo de microcontroladores y sensores predictivos IoT en planta de ensamblaje."),
        ("Q3: DETECCIÓN AUTOMATIZADA", "Presupuesto: 75.000 €", "Telemetría 24/7 & Cifrado", "Cables sensores de fuga de líquido en racks. Pesaje dinámico en líneas de picking. Cifrado envelope KMS y pipeline de contratos de datos."),
        ("Q4: AUDITORÍA & STRESS TESTING", "Presupuesto: 30.000 €", "Simulación & Sign-Off", "Simulacros de caída catastrófica (Chaos Engineering). Verificación independiente de NPR residual < 80 y recertificación ISO 31000 / IATF 16949.")
    ]
    phases_en = [
        ("Q1: CRITICAL RINGFENCING", "Budget: €110,000", "FIDO2 MFA & Dual-DNS", "Rollout of physical Zero Trust keys for privileged access. Independent Dual-DNS footprint and dynamic payment routing. Immediate abatement of RPN > 400."),
        ("Q2: RESILIENCY & SUPPLY", "Budget: €145,000", "Multi-Region Cloud & IoT", "Active-active multi-region AWS topology. European dual-sourcing contracts for microcontrollers and IoT vibration telemetry in assembly plants."),
        ("Q3: AUTOMATED TELEMETRY", "Budget: €75,000", "24/7 Monitoring & KMS", "Conductive coolant leak cables installed per compute rack. Dynamic automated checkweighers in logistics. KMS envelope encryption rollout."),
        ("Q4: AUDIT & STRESS TESTING", "Budget: €30,000", "Chaos Drills & Sign-Off", "Enterprise Chaos Engineering drills. Independent verification of residual RPN < 80 and formal ISO 31000 / IATF 16949 recertification.")
    ]
    phases = phases_es if lang == 'ES' else phases_en

    ph_w = Inches(2.78)
    ph_h = Inches(1.85)
    ph_y = Inches(1.88)
    for idx, (p_title, p_time, p_milestone, p_desc) in enumerate(phases):
        px = Inches(0.8 + idx * 2.97)
        box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, ph_y, ph_w, ph_h)
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_CARD_BG
        box.line.color.rgb = COLOR_RED_BORDER if idx == 0 else (COLOR_BLUE_ACCENT if idx == 1 else COLOR_TEAL_ACCENT)
        box.line.width = Pt(1.5) if idx < 2 else Pt(1)

        tb = slide3.shapes.add_textbox(px + Inches(0.12), ph_y + Inches(0.1), ph_w - Inches(0.24), ph_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = p_title
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_DARK

        p1 = tf.add_paragraph()
        p1.text = f"{p_time} · {p_milestone}"
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEAL_ACCENT

        p2 = tf.add_paragraph()
        p2.space_before = Pt(4)
        p2.text = p_desc
        p2.font.size = Pt(7.8)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # MITAD INFERIOR: BOARD DECISION GATEWAY (Y = 3.92 a 6.95)
    gw_y = Inches(3.92)
    gw_w = Inches(11.73)
    gw_h = Inches(3.00)

    gw_shape = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), gw_y, gw_w, gw_h)
    gw_shape.fill.solid()
    gw_shape.fill.fore_color.rgb = COLOR_WHITE
    gw_shape.line.color.rgb = COLOR_NAVY_DARK
    gw_shape.line.width = Pt(2)

    tb_gw = slide3.shapes.add_textbox(Inches(1.0), gw_y + Inches(0.15), gw_w - Inches(0.4), Inches(0.35))
    tf_gw = tb_gw.text_frame
    tf_gw.margin_left = tf_gw.margin_top = tf_gw.margin_right = tf_gw.margin_bottom = 0
    p_gw_title = tf_gw.paragraphs[0]
    p_gw_title.text = "BOARD DECISION GATEWAY · RESOLUCIONES VINCULANTES DEL COMITÉ DE DIRECCIÓN" if lang == 'ES' else "BOARD DECISION GATEWAY · BINDING EXECUTIVE COMMITTEE RESOLUTIONS"
    p_gw_title.font.size = Pt(11)
    p_gw_title.font.bold = True
    p_gw_title.font.color.rgb = COLOR_NAVY_DARK

    # 4 Resoluciones en 2 Columnas
    res_es = [
        ("1. Aprobación del Presupuesto CAPEX de Mitigación: ", "Se autoriza formalmente la partida de 360.000 € imputada a los 10 controles prioritarios para evitar 1.588.000 € en pérdidas esperadas."),
        ("2. Ratificación del Umbral de Apetito de Riesgo: ", "Se fija un límite máximo corporativo de NPR ≤ 80 para cualquier proceso en producción y la erradicación total de riesgos en zona roja."),
        ("3. Mandato de Detección Automatizada 24/7: ", "Se aprueba la obligatoriedad de telemetría de monitoreo continuo en tiempo real para todos los sistemas con Severidad S ≥ 8."),
        ("4. Designación Formal de Risk Owners: ", "Se ratifica la responsabilidad personal de cada directivo asignado, con obligación de comparecencia trimestral ante el Comité de Auditoría.")
    ]
    res_en = [
        ("1. Mitigation CAPEX Budget Authorization: ", "Formal allocation of €360,000 assigned across 10 top-priority risk controls to avoid €1,588,000 in expected losses."),
        ("2. Corporate Risk Appetite Threshold Ratification: ", "Enforcement of a strict RPN ≤ 80 ceiling for all production processes and zero tolerance for red-zone corporate risks."),
        ("3. 24/7 Automated Telemetry Mandate: ", "Mandatory real-time monitoring telemetry for any mission-critical process exhibiting Severity S ≥ 8."),
        ("4. Formal Risk Owner Designations: ", "Personal accountability ratified for each designated Risk Owner, requiring quarterly reporting to Board Audit Committee.")
    ]
    res = res_es if lang == 'ES' else res_en

    for r_idx, (r_bold, r_text) in enumerate(res):
        col_pos = r_idx % 2
        row_pos = r_idx // 2
        rx = Inches(1.0 + col_pos * 5.75)
        ry = gw_y + Inches(0.52 + row_pos * 0.72)
        rw = Inches(5.55)

        tb_r = slide3.shapes.add_textbox(rx, ry, rw, Inches(0.65))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

        p = tf_r.paragraphs[0]
        r1 = p.add_run()
        r1.text = r_bold
        r1.font.bold = True
        r1.font.size = Pt(8.2)
        r1.font.color.rgb = COLOR_NAVY_DARK

        r2 = p.add_run()
        r2.text = r_text
        r2.font.size = Pt(7.8)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # Cajas de Firma C-Level (4 Firmas en la base del Gateway)
    sign_y = gw_y + Inches(2.05)
    sign_w = Inches(2.65)
    sign_h = Inches(0.75)

    sign_roles_es = [
        ("Chief Executive Officer (CEO)", "Aprobación Estratégica"),
        ("Chief Operating Officer (COO)", "Validación de Controles"),
        ("Chief Financial Officer (CFO)", "Liberación de CAPEX"),
        ("Chief Information Security Officer (CISO)", "Ratificación de Riesgos")
    ]
    sign_roles_en = [
        ("Chief Executive Officer (CEO)", "Strategic Approval"),
        ("Chief Operating Officer (COO)", "Operational Controls"),
        ("Chief Financial Officer (CFO)", "CAPEX Disbursement"),
        ("Chief Information Security Officer (CISO)", "Risk Sign-Off")
    ]
    sign_roles = sign_roles_es if lang == 'ES' else sign_roles_en

    for s_idx, (s_title, s_action) in enumerate(sign_roles):
        sx = Inches(1.0 + s_idx * 2.88)
        s_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sign_y, sign_w, sign_h)
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = COLOR_CARD_BG
        s_box.line.color.rgb = COLOR_BORDER
        s_box.line.width = Pt(1)

        tb_s = slide3.shapes.add_textbox(sx + Inches(0.08), sign_y + Inches(0.06), sign_w - Inches(0.16), sign_h - Inches(0.12))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0

        p_s0 = tf_s.paragraphs[0]
        p_s0.text = s_title
        p_s0.font.size = Pt(7.5)
        p_s0.font.bold = True
        p_s0.font.color.rgb = COLOR_NAVY_DARK

        p_s1 = tf_s.add_paragraph()
        p_s1.text = f"Firma & Visto Bueno · {s_action}" if lang == 'ES' else f"Signature & Sign-Off · {s_action}"
        p_s1.font.size = Pt(6.8)
        p_s1.font.color.rgb = COLOR_TEAL_ACCENT

        p_s2 = tf_s.add_paragraph()
        p_s2.text = "Fecha: ____ / ____ / 2026   [Vincúlese]" if lang == 'ES' else "Date: ____ / ____ / 2026   [Binding]"
        p_s2.font.size = Pt(6.5)
        p_s2.font.color.rgb = COLOR_TEXT_MUTED

    prs.save(out_path)
    print(f"  -> Presentación PPTX generada: {out_path}")

    # Limpieza de imágenes temporales
    for tmp in [f"temp_pareto_{lang}.png"]:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass


def main():
    print("[1/2] Generando presentación PPTX C-Level en Español...")
    create_deck(lang='ES')

    print("[2/2] Generando presentación PPTX C-Level en Inglés...")
    create_deck(lang='EN')

    print("\n✓ Generación de presentaciones PPTX completada con éxito.")


if __name__ == "__main__":
    main()
