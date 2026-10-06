#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa/[ES]_Matriz_DAR/Presentacion_DAR_CLevel_ES.pptx
2. packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa/[EN]_Quantitative_DAR/Deck_DAR_CLevel_EN.pptx

Características de diseño Tier-1 (McKinsey / BCG / Bain):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Pirámide de Minto y Action Titles contundentes.
- Diapositiva 1: Síntesis Ejecutiva & Veredicto DAR (4 KPI Cards y fundamentos estratégicos).
- Diapositiva 2: Matriz de Trade-Offs & Evidencia Comparativa (Tabla analítica y gráfico comparativo).
- Diapositiva 3: Roadmap de Transición & Board Decision Gateway (Cronograma Q1-Q4 con identidad visual por fase,
  resoluciones vinculantes en 2 columnas y bloque de 4 firmas digitales sin solapamiento).
- Visuales de alta gama: degradados nativos DrawingML, acentos cromáticos dinámicos y jerarquía tipográfica calibrada.
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
COLOR_NAVY_DARK = RGBColor(15, 23, 42)       # #0F172A Slate 900
COLOR_NAVY_MED = RGBColor(30, 41, 59)        # #1E293B Slate 800
COLOR_BLUE_ACCENT = RGBColor(37, 99, 235)    # #2563EB Blue 600
COLOR_BLUE_LIGHT = RGBColor(239, 246, 255)   # #EFF6FF Blue 50

# Estados y Acentos
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


def apply_gradient_fill(shape, color1_hex, color2_hex, angle_deg=90):
    """
    Aplica un degradado lineal nativo DrawingML a una forma de python-pptx.
    angle_deg: 90 para vertical (top-to-bottom), 0 para horizontal (left-to-right).
    """
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


def create_chart_image(lang='ES', out_path='temp_dar_chart.png'):
    """
    Genera un gráfico comparativo de barras de alta resolución para la Diapositiva 2.
    Compara las 4 alternativas viables y muestra el score por pilares y el score final.
    """
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=220)

    categories_es = ['P1: Técnico\n(30%)', 'P2: TCO 36M\n(25%)', 'P3: SLA/Soporte\n(20%)', 'P4: Seguridad\n(25%)', 'Score Final\n(100 pts)']
    categories_en = ['P1: Tech Fit\n(30%)', 'P2: 3Y TCO\n(25%)', 'P3: SLA/Support\n(20%)', 'P4: Security\n(25%)', 'Final Score\n(100 pts)']
    categories = categories_es if lang == 'ES' else categories_en

    alpha_sc = [7.9, 7.7, 8.4, 7.5, 7.86]
    beta_sc = [9.2, 8.0, 9.2, 8.2, 8.64]
    gamma_sc = [7.6, 8.6, 7.5, 7.0, 7.66]
    eps_sc = [7.0, 8.0, 6.5, 7.0, 7.18]

    x = np.arange(len(categories))
    width = 0.20

    rects1 = ax.bar(x - 1.5*width, alpha_sc, width, label='Vendor Alpha', color='#94A3B8', alpha=0.9, edgecolor='#64748B', linewidth=0.8)
    rects2 = ax.bar(x - 0.5*width, beta_sc, width, label='Vendor Beta (Ganador)' if lang == 'ES' else 'Vendor Beta (Winner)', color='#10B981', edgecolor='#065F46', linewidth=1.5)
    rects3 = ax.bar(x + 0.5*width, gamma_sc, width, label='Vendor Gamma', color='#0EA5E9', alpha=0.9, edgecolor='#0284C7', linewidth=0.8)
    rects4 = ax.bar(x + 1.5*width, eps_sc, width, label='Vendor Epsilon', color='#CBD5E1', alpha=0.9, edgecolor='#94A3B8', linewidth=0.8)

    ax.set_ylabel('Calificación Media (1 - 10 pts)' if lang == 'ES' else 'Average Rating (1 - 10 pts)', fontsize=8.5, fontweight='bold', color='#334155')
    ax.set_title('Comparativa Multicriterio por Pilares de Decisión' if lang == 'ES' else 'Multi-Criteria Comparison by Decision Pillars', fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=7.5, color='#334155', fontweight='bold')
    ax.set_ylim(0, 11)
    ax.grid(axis='y', linestyle='--', alpha=0.35, color='#94A3B8')
    ax.legend(loc='upper right', fontsize=7.5, framealpha=0.95, edgecolor='#CBD5E1')

    # Destacar al ganador con anotación
    ax.annotate('+7.8 pts' if lang == 'ES' else '+7.8 pts',
                xy=(x[4] - 0.5*width, beta_sc[4]),
                xytext=(x[4] - 0.5*width, beta_sc[4] + 0.9),
                ha='center', fontsize=7.5, fontweight='bold', color='#065F46',
                arrowprops=dict(arrowstyle='->', color='#10B981', lw=1.2))

    plt.tight_layout()
    fig.savefig(out_path, dpi=220, facecolor='#FFFFFF')
    plt.close(fig)
    return out_path


def add_header(slide, action_title, slide_num, total_slides=3, lang='ES'):
    """Añade la cabecera estándar Tier-1 con metadatos y Action Title."""
    # Badge superior
    tb_badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.0), Inches(0.28))
    tf_b = tb_badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = ("DATALARIA · SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN | ESTÁNDAR CMMI DAR & KEPNER-TREGOE"
                if lang == 'ES' else
                "DATALARIA · SUITE 02: DECISION ANALYSIS & RESOLUTION | CMMI DAR & KEPNER-TREGOE STANDARD")
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_BLUE_ACCENT
    p_b.font.name = FONT_HEADING

    # Action Title (Minto Pyramid Principle)
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.75))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.size = Pt(15.5)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK
    p_t.font.name = FONT_HEADING

    # Número de página y confidencialidad en el pie
    tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.7), Inches(0.25))
    tf_f = tb_foot.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = (f"Datalaria.com · Documento Confidencial para Consejo de Administración | Diapositiva {slide_num} de {total_slides}"
                if lang == 'ES' else
                f"Datalaria.com · Confidential Board of Directors Document | Slide {slide_num} of {total_slides}")
    p_f.font.size = Pt(8)
    p_f.font.color.rgb = COLOR_TEXT_MUTED
    p_f.font.name = FONT_BODY


def create_deck(lang='ES', out_path=None):
    if out_path is None:
        base_dir = "packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa"
        sub_dir = "[ES]_Matriz_DAR" if lang == 'ES' else "[EN]_Quantitative_DAR"
        fname = "Presentacion_DAR_CLevel_ES.pptx" if lang == 'ES' else "Deck_DAR_CLevel_EN.pptx"
        out_path = os.path.join(base_dir, sub_dir, fname)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================================================
    # SLIDE 1: SÍNTESIS EJECUTIVA & VEREDICTO DAR
    # ==========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    title_s1 = (
        "Tras evaluar 5 alternativas mediante 13 criterios ponderados y 6 filtros veto, "
        "Vendor Beta resulta adjudicataria con 86,4/100, ofreciendo un ahorro de TCO del 19% y pleno cumplimiento regulatorio"
        if lang == 'ES' else
        "Following evaluation of 5 alternatives across 13 weighted criteria and 6 veto gates, "
        "Vendor Beta is awarded the mandate with 86.4/100, delivering a 19% 3-year TCO advantage and zero compliance risk"
    )
    add_header(slide1, title_s1, 1, 3, lang=lang)

    # 4 KPI Cards alineadas con degradados sutiles y bordes pulidos
    card_w = Inches(2.78)
    card_h = Inches(1.32)
    card_y = Inches(1.58)

    cards_data_es = [
        ("ALTERNATIVA GANADORA", "Vendor Beta ★", "Plataforma Cloud Enterprise", "ECFDF5", "D1FAE5", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT, COLOR_GREEN_TEXT),
        ("PUNTUACIÓN PONDERADA", "86,4 / 100", "▲ +9,9% vs. Segunda Opción", "F8FAFC", "EFF6FF", COLOR_BLUE_ACCENT, COLOR_NAVY_DARK, COLOR_GREEN_TEXT),
        ("DIFERENCIAL VS 2ª OPCIÓN", "+7,8 pts", "Vendor Alpha: 78,6 pts", "EFF6FF", "DBEAFE", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT, COLOR_TEXT_MAIN),
        ("FILTROS VETO SUPERADOS", "100% CUMPLE", "1 Descalificada (Vendor Delta)", "F8FAFC", "F1F5F9", COLOR_BORDER, COLOR_NAVY_DARK, COLOR_RED_TEXT),
    ]
    cards_data_en = [
        ("RECOMMENDED WINNER", "Vendor Beta ★", "Enterprise Cloud Platform", "ECFDF5", "D1FAE5", COLOR_GREEN_BORDER, COLOR_GREEN_TEXT, COLOR_GREEN_TEXT),
        ("AUDITED WEIGHTED SCORE", "86.4 / 100", "▲ +9.9% vs. Runner-Up", "F8FAFC", "EFF6FF", COLOR_BLUE_ACCENT, COLOR_NAVY_DARK, COLOR_GREEN_TEXT),
        ("DECISION GAP VS RUNNER-UP", "+7.8 pts", "Vendor Alpha: 78.6 pts", "EFF6FF", "DBEAFE", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT, COLOR_TEXT_MAIN),
        ("VETO CRITERIA ADHERENCE", "100% PASS", "1 Disqualified (Vendor Delta)", "F8FAFC", "F1F5F9", COLOR_BORDER, COLOR_NAVY_DARK, COLOR_RED_TEXT),
    ]
    cards_data = cards_data_es if lang == 'ES' else cards_data_en

    for idx, (lbl, val, sub, grad_c1, grad_c2, border_col, val_col, sub_col) in enumerate(cards_data):
        cx = Inches(0.8 + idx * 2.97)
        shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        apply_gradient_fill(shape, grad_c1, grad_c2, angle_deg=90)
        shape.line.color.rgb = border_col
        shape.line.width = Pt(1.5 if idx == 0 else 1.0)

        tf = shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = Inches(0.14)
        tf.margin_right = Inches(0.14)
        tf.margin_top = Inches(0.12)
        tf.margin_bottom = Inches(0.08)

        p0 = tf.paragraphs[0]
        p0.text = lbl
        p0.font.size = Pt(8)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_TEXT_MUTED
        p0.font.name = FONT_HEADING

        p1 = tf.add_paragraph()
        p1.text = val
        p1.font.size = Pt(16.5)
        p1.font.bold = True
        p1.font.color.rgb = val_col
        p1.font.name = FONT_HEADING

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(8)
        p2.font.bold = True
        p2.font.color.rgb = sub_col
        p2.font.name = FONT_BODY

    # Dos Contenedores Principales Abajo (Anclados verticalmente arriba para distribución armónica)
    pnl_y = Inches(3.08)
    pnl_h = Inches(3.82)

    # Panel Izquierdo: Fundamentos del Dictamen
    pnl_l_w = Inches(6.8)
    shape_l = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), pnl_y, pnl_l_w, pnl_h)
    apply_gradient_fill(shape_l, "F8FAFC", "EFF6FF", angle_deg=90)
    shape_l.line.color.rgb = COLOR_BORDER
    shape_l.line.width = Pt(1)

    tf_l = shape_l.text_frame
    tf_l.vertical_anchor = MSO_ANCHOR.TOP
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.24)
    tf_l.margin_right = Inches(0.24)
    tf_l.margin_top = Inches(0.20)

    p_lh = tf_l.paragraphs[0]
    p_lh.text = "FUNDAMENTOS ESTRATÉGICOS DEL DICTAMEN DE ADJUDICACIÓN" if lang == 'ES' else "STRATEGIC RATIONALE FOR AWARD MANDATE"
    p_lh.font.size = Pt(10.5)
    p_lh.font.bold = True
    p_lh.font.color.rgb = COLOR_NAVY_DARK
    p_lh.space_after = Pt(6)

    drivers_es = [
        ("1. Cobertura Funcional Nativa Superior (94% vs. 81% Media):",
         "Vendor Beta minimiza el riesgo de retrasos al no requerir código a medida en contabilidad analítica, facturación electrónica y supply chain."),
        ("2. Eficiencia en Coste Total de Propiedad (-19% TCO a 36 Meses):",
         "Aunque el licenciamiento inicial es ligeramente mayor (+6%), el coste de implantación y soporte genera un ahorro neto acumulado de 380.000 €."),
        ("3. Blindaje de SLA y Soporte Crítico (< 2 Horas Contractuales):",
         "Centro de atención técnica 24/7 con penalizaciones contractuales directas del 5% mensual ante caídas de servicio."),
        ("4. Arquitectura de Ciberseguridad Zero-Trust Auditada:",
         "Pleno cumplimiento del RGPD con data centers exclusivos en la UE (Frankfurt/Madrid) y certificación SOC 2 Type II auditada por Big-4.")
    ]
    drivers_en = [
        ("1. Superior Out-of-the-Box Coverage (94% vs. 81% Benchmark):",
         "Vendor Beta minimizes custom development risk by natively supporting operational accounting, e-invoicing, and warehouse logistics."),
        ("2. TCO Cost Advantage (-19% Total Cost of Ownership at 36 Months):",
         "While upfront subscription is slightly higher (+6%), professional services and maintenance deliver a net 3-year cash savings of $380,000."),
        ("3. Contractual SLA & Critical Incident Resolution (< 2h Turnaround):",
         "Enterprise 24/7 support backed by automatic 5% monthly fee credit penalties for service degradation."),
        ("4. Certified Zero-Trust Cloud Security Architecture:",
         "Full GDPR compliance with sovereign EU data centers and active SOC 2 Type II attestation audited by an independent Big-4 firm.")
    ]
    drivers = drivers_es if lang == 'ES' else drivers_en

    for title_d, body_d in drivers:
        p_dt = tf_l.add_paragraph()
        p_dt.text = title_d
        p_dt.font.size = Pt(8.5)
        p_dt.font.bold = True
        p_dt.font.color.rgb = COLOR_BLUE_ACCENT
        p_dt.space_before = Pt(4)

        p_db = tf_l.add_paragraph()
        p_db.text = body_d
        p_db.font.size = Pt(8)
        p_db.font.color.rgb = COLOR_TEXT_MAIN
        p_db.space_after = Pt(2)

    # Panel Derecho: Síntesis de Riesgos y Alternativa Backup
    pnl_r_w = Inches(4.7)
    pnl_r_x = Inches(7.8)
    shape_r = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pnl_r_x, pnl_y, pnl_r_w, pnl_h)
    apply_gradient_fill(shape_r, "F8FAFC", "F1F5F9", angle_deg=90)
    shape_r.line.color.rgb = COLOR_BORDER
    shape_r.line.width = Pt(1)

    tf_r = shape_r.text_frame
    tf_r.vertical_anchor = MSO_ANCHOR.TOP
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.24)
    tf_r.margin_right = Inches(0.24)
    tf_r.margin_top = Inches(0.20)

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "MATRIZ DE RIESGOS MITIGADOS & ESTRATEGIA BACKUP" if lang == 'ES' else "MITIGATED RISKS & CONTINGENCY BACKUP"
    p_rh.font.size = Pt(10.5)
    p_rh.font.bold = True
    p_rh.font.color.rgb = COLOR_NAVY_DARK
    p_rh.space_after = Pt(6)

    risks_es = [
        ("• Descalificación por Filtro Veto (Vendor Delta):",
         "Descartado de inmediato por almacenar telemetría y datos en EE.UU., violando la directiva de compliance y RGPD."),
        ("• Alternativa de Respaldo / Backup (Vendor Alpha):",
         "Con 78,6 pts, queda designado como opción de contingencia si la negociación con Vendor Beta encalla en 30 días."),
        ("• Riesgo de Dependencia Tecnológica (Lock-In):",
         "Exigencia contractual de backups periódicos en SQL y catálogo de APIs abiertas para garantizar reversibilidad."),
        ("• Recomendación de Inversión Vinculante:",
         "Autorizar el desembolso de 420.000 € presupuestados para el Año 1 e iniciar onboarding formal.")
    ]
    risks_en = [
        ("• Non-Negotiable Veto Gatekeeper (Vendor Delta):",
         "Immediately disqualified for hosting analytics telemetry outside the EU, violating corporate data privacy and GDPR."),
        ("• Contingency Runner-Up Mandate (Vendor Alpha):",
         "Scoring 78.6 pts, designated as formal fallback if contract execution with Vendor Beta stalls past 30 days."),
        ("• Vendor Lock-In Mitigation Clause:",
         "Contractually enforces quarterly raw database snapshots (SQL) and open REST APIs to guarantee long-term portability."),
        ("• Board Investment Recommendation:",
         "Authorize initial Year 1 budget of $420,000 and delegate execution authority to CIO and Procurement.")
    ]
    risks = risks_es if lang == 'ES' else risks_en

    for r_title, r_body in risks:
        p_rt = tf_r.add_paragraph()
        p_rt.text = r_title
        p_rt.font.size = Pt(8.5)
        p_rt.font.bold = True
        p_rt.font.color.rgb = COLOR_NAVY_DARK
        p_rt.space_before = Pt(4)

        p_rb = tf_r.add_paragraph()
        p_rb.text = r_body
        p_rb.font.size = Pt(8)
        p_rb.font.color.rgb = COLOR_TEXT_MAIN
        p_rb.space_after = Pt(2)


    # ==========================================================================
    # SLIDE 2: MATRIZ DE TRADE-OFFS & EVIDENCIA COMPARATIVA
    # ==========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    title_s2 = (
        "Vendor Beta lidera en 3 de los 4 pilares estratégicos, compensando una mayor inversión inicial "
        "con el menor OPEX y coste total de propiedad (TCO) a 36 meses"
        if lang == 'ES' else
        "Vendor Beta dominates 3 out of 4 strategic pillars, offsetting slightly higher initial setup "
        "with the lowest recurring OPEX and superior 3-year Total Cost of Ownership"
    )
    add_header(slide2, title_s2, 2, 3, lang=lang)

    # Contenedor Izquierdo: Tabla Comparativa
    tbl_w = Inches(6.4)
    tbl_h = Inches(4.8)
    tbl_x = Inches(0.8)
    tbl_y = Inches(1.65)

    rows_cnt = 6
    cols_cnt = 7
    table_shape = slide2.shapes.add_table(rows_cnt, cols_cnt, tbl_x, tbl_y, tbl_w, tbl_h)
    table = table_shape.table

    table.columns[0].width = Inches(2.0) # Alternativa
    table.columns[1].width = Inches(0.7) # P1 Tech
    table.columns[2].width = Inches(0.7) # P2 TCO
    table.columns[3].width = Inches(0.7) # P3 SLA
    table.columns[4].width = Inches(0.7) # P4 Sec
    table.columns[5].width = Inches(0.8) # Veto
    table.columns[6].width = Inches(0.8) # Score

    tbl_headers_es = ["Alternativa", "P1 (30%)", "P2 (25%)", "P3 (20%)", "P4 (25%)", "Veto", "Final"]
    tbl_headers_en = ["Alternative", "P1 (30%)", "P2 (25%)", "P3 (20%)", "P4 (25%)", "Veto", "Final"]
    tbl_headers = tbl_headers_es if lang == 'ES' else tbl_headers_en

    for c_i, h_t in enumerate(tbl_headers):
        cell = table.cell(0, c_i)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.text = h_t
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER if c_i > 0 else PP_ALIGN.LEFT

    table_rows_es = [
        ("Alt A: Vendor Alpha", "23,6", "19,3", "16,9", "18,8", "APTA", "78,6"),
        ("Alt B: Vendor Beta ★", "27,6", "20,0", "18,4", "20,4", "APTA", "86,4"),
        ("Alt C: Vendor Gamma", "22,7", "21,4", "15,0", "17,5", "APTA", "76,6"),
        ("Alt D: Vendor Delta", "24,8", "16,3", "16,3", "18,9", "VETO", "0,0"),
        ("Alt E: Vendor Epsilon", "21,1", "20,1", "13,0", "17,6", "APTA", "71,8"),
    ]
    table_rows_en = [
        ("Alt A: Vendor Alpha", "23.6", "19.3", "16.9", "18.8", "PASS", "78.6"),
        ("Alt B: Vendor Beta ★", "27.6", "20.0", "18.4", "20.4", "PASS", "86.4"),
        ("Alt C: Vendor Gamma", "22.7", "21.4", "15.0", "17.5", "PASS", "76.6"),
        ("Alt D: Vendor Delta", "24.8", "16.3", "16.3", "18.9", "FAIL", "0.0"),
        ("Alt E: Vendor Epsilon", "21.1", "20.1", "13.0", "17.6", "PASS", "71.8"),
    ]
    table_rows = table_rows_es if lang == 'ES' else table_rows_en

    for r_i, r_data in enumerate(table_rows, start=1):
        is_winner = (r_i == 2)
        is_veto = (r_i == 4)
        for c_i, val in enumerate(r_data):
            cell = table.cell(r_i, c_i)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.text = val
            cell.fill.solid()
            if is_winner:
                cell.fill.fore_color.rgb = COLOR_GREEN_BG
            elif is_veto:
                cell.fill.fore_color.rgb = COLOR_RED_BG if c_i >= 5 else COLOR_CARD_BG
            else:
                cell.fill.fore_color.rgb = COLOR_WHITE if r_i % 2 == 1 else COLOR_CARD_BG

            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5)
            p.font.name = FONT_BODY
            p.alignment = PP_ALIGN.CENTER if c_i > 0 else PP_ALIGN.LEFT
            if is_winner:
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN_TEXT
            elif is_veto and c_i >= 5:
                p.font.bold = True
                p.font.color.rgb = COLOR_RED_TEXT
            else:
                p.font.color.rgb = COLOR_NAVY_DARK

    # Contenedor Derecho: Gráfico comparativo y Trade-Offs
    chart_img_path = create_chart_image(lang=lang, out_path=f"temp_dar_chart_{lang}.png")
    slide2.shapes.add_picture(chart_img_path, Inches(7.4), Inches(1.65), width=Inches(5.1))

    # Caja de Trade-Offs Abajo del Gráfico con degradado sutil
    to_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.4), Inches(4.75), Inches(5.1), Inches(2.05))
    apply_gradient_fill(to_box, "F8FAFC", "EFF6FF", angle_deg=90)
    to_box.line.color.rgb = COLOR_BORDER
    to_box.line.width = Pt(1)

    tf_to = to_box.text_frame
    tf_to.vertical_anchor = MSO_ANCHOR.TOP
    tf_to.word_wrap = True
    tf_to.margin_left = tf_to.margin_right = Inches(0.20)
    tf_to.margin_top = Inches(0.16)

    p_toh = tf_to.paragraphs[0]
    p_toh.text = "ANÁLISIS DE TRADE-OFFS CLAVE (DECISION DYNAMICS)" if lang == 'ES' else "KEY TRADE-OFF DYNAMICS & STRATEGIC RATIONALE"
    p_toh.font.size = Pt(9.5)
    p_toh.font.bold = True
    p_toh.font.color.rgb = COLOR_NAVY_DARK
    p_toh.space_after = Pt(4)

    tradeoffs_es = [
        ("• Inversión Inicial vs. Gasto Operativo:", "Vendor Gamma es 21.000 € más barato en Year 1 pero su coste de soporte a 3 años dispara el TCO total."),
        ("• Personalización vs. Deuda Técnica:", "Vendor Alpha ofrecía código a medida, lo que aumentaba el riesgo de fallos en futuras actualizaciones."),
        ("• Cumplimiento Regulatorio Binario:", "Vendor Delta ofrecía el precio más agresivo, pero su incapacidad de certificar soberanía de datos en la UE motivó su veto.")
    ]
    tradeoffs_en = [
        ("• Upfront Setup vs. Recurring OPEX:", "Vendor Gamma is $21,000 cheaper in Year 1, but sub-par customer support and custom script overhead bloat long-term TCO."),
        ("• Customization vs. Technical Debt:", "Vendor Alpha required extensive bespoke middleware scripting, increasing upgrade friction and regression failure risks."),
        ("• Binary Compliance & Risk Management:", "Vendor Delta presented aggressive pricing, but failed non-negotiable EU data sovereignty mandates, triggering immediate veto.")
    ]
    tradeoffs = tradeoffs_es if lang == 'ES' else tradeoffs_en

    for th, tb in tradeoffs:
        p_t = tf_to.add_paragraph()
        p_t.text = th
        p_t.font.size = Pt(8.5)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_BLUE_ACCENT
        p_t.space_before = Pt(3)

        p_b = tf_to.add_paragraph()
        p_b.text = tb
        p_b.font.size = Pt(8)
        p_b.font.color.rgb = COLOR_TEXT_MAIN
        p_b.space_after = Pt(1)


    # ==========================================================================
    # SLIDE 3: ROADMAP DE TRANSICIÓN & BOARD DECISION GATEWAY (SIN SOLAPAMIENTO)
    # ==========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    title_s3 = (
        "Plan de transición estructurado en 4 fases de despliegue con un Board Decision Gateway "
        "de 4 acuerdos vinculantes de gobernanza corporativa"
        if lang == 'ES' else
        "Execution transition roadmap structured across 4 phases backed by a formal Board Decision Gateway "
        "with 4 binding corporate governance resolutions"
    )
    add_header(slide3, title_s3, 3, 3, lang=lang)

    # Mitad Superior: Cronograma Q1 - Q4 con identidades visuales atractivas por fase
    phase_w = Inches(2.78)
    phase_h = Inches(2.05)
    phase_y = Inches(1.55)

    # Paletas temáticas por fase para romper la monotonía visual:
    # Q1: Azul Real | Q2: Índigo | Q3: Teal/Cian | Q4: Verde Esmeralda Go-Live
    phases_meta = [
        {"grad_c1": "EFF6FF", "grad_c2": "FFFFFF", "border": RGBColor(59, 130, 246), "tag_col": RGBColor(29, 78, 216)},
        {"grad_c1": "F5F3FF", "grad_c2": "FFFFFF", "border": RGBColor(99, 102, 241), "tag_col": RGBColor(79, 70, 229)},
        {"grad_c1": "F0FDFA", "grad_c2": "FFFFFF", "border": RGBColor(20, 184, 166), "tag_col": RGBColor(13, 148, 136)},
        {"grad_c1": "ECFDF5", "grad_c2": "FFFFFF", "border": RGBColor(16, 185, 129), "tag_col": RGBColor(5, 150, 105)},
    ]

    phases_es = [
        ("Q1 · FASE 1", "Formalización & Kick-Off", "M01 - M02", [
            "Firma del contrato marco y anexo SLA.",
            "Constitución del comité PMO de proyecto.",
            "Validación de arquitectura e integración inicial."
        ]),
        ("Q2 · FASE 2", "Configuración & Sandbox", "M03 - M04", [
            "Parametrización de workflows de finanzas.",
            "Migración piloto de datos históricos (N-3).",
            "Pruebas de estrés y conectores de API."
        ]),
        ("Q3 · FASE 3", "Integración & UAT", "M05 - M06", [
            "Pruebas de aceptación de usuario (UAT).",
            "Capacitación de 120 usuarios clave.",
            "Simulación de corte de servicio y rollback."
        ]),
        ("Q4 · FASE 4", "Go-Live & Hipercare", "M07 - M08", [
            "Pase a producción definitivo (Go-Live).",
            "Soporte 24/7 de estabilización hipercare.",
            "Auditoría post-implantación y cierre."
        ])
    ]
    phases_en = [
        ("Q1 · PHASE 1", "Contracting & Kick-Off", "M01 - M02", [
            "Execute Master Services Agreement & SLA exhibit.",
            "Establish joint Steering Committee & PMO.",
            "Validate security endpoints and network access."
        ]),
        ("Q2 · PHASE 2", "Core Setup & Sandbox", "M03 - M04", [
            "Configure financial & supply chain workflows.",
            "Pilot migration of 3-year historical dataset.",
            "Stress testing and enterprise API integration."
        ]),
        ("Q3 · PHASE 3", "UAT & User Training", "M05 - M06", [
            "End-user acceptance testing (UAT sign-off).",
            "Comprehensive training for 120 key operators.",
            "Dry-run cutover and contingency rollback drill."
        ]),
        ("Q4 · PHASE 4", "Go-Live & Hypercare", "M07 - M08", [
            "Enterprise production cutover (Go-Live).",
            "Dedicated 24/7 hypercare support desk.",
            "Post-implementation audit and committee sign-off."
        ])
    ]
    phases = phases_es if lang == 'ES' else phases_en

    for idx, (p_tag, p_name, p_time, bullets) in enumerate(phases):
        px = Inches(0.8 + idx * 2.97)
        shape = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, phase_y, phase_w, phase_h)
        meta = phases_meta[idx]
        apply_gradient_fill(shape, meta["grad_c1"], meta["grad_c2"], angle_deg=90)
        shape.line.color.rgb = meta["border"]
        shape.line.width = Pt(1.2)

        tf = shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.16)
        tf.margin_top = Inches(0.14)

        p0 = tf.paragraphs[0]
        p0.text = f"{p_tag} • {p_time}"
        p0.font.size = Pt(8)
        p0.font.bold = True
        p0.font.color.rgb = meta["tag_col"]

        p1 = tf.add_paragraph()
        p1.text = p_name
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p1.space_after = Pt(4)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(8)
            pb.font.color.rgb = COLOR_TEXT_MAIN
            pb.space_after = Pt(2)

    # Mitad Inferior: Prominente Board Decision Gateway (CON DEGRADADO SLATE OSCURO Y SIN SOLAPAMIENTO)
    gw_y = Inches(3.75)
    gw_w = Inches(11.7)
    gw_h = Inches(3.20)

    gw_shape = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), gw_y, gw_w, gw_h)
    apply_gradient_fill(gw_shape, "0B1120", "1E293B", angle_deg=90)
    gw_shape.line.color.rgb = RGBColor(51, 65, 85) # Slate 700
    gw_shape.line.width = Pt(1.5)

    # Título del Gateway dentro de la caja
    tb_gwh = slide3.shapes.add_textbox(Inches(1.05), Inches(3.85), Inches(11.2), Inches(0.32))
    tf_gwh = tb_gwh.text_frame
    tf_gwh.word_wrap = True
    tf_gwh.margin_left = tf_gwh.margin_top = tf_gwh.margin_right = tf_gwh.margin_bottom = 0
    p_gwh = tf_gwh.paragraphs[0]
    p_gwh.text = "BOARD DECISION GATEWAY · RESOLUCIONES VINCULANTES DEL COMITÉ DE DIRECCIÓN" if lang == 'ES' else "BOARD DECISION GATEWAY · BINDING STEERING COMMITTEE RESOLUTIONS"
    p_gwh.font.size = Pt(10.5)
    p_gwh.font.bold = True
    p_gwh.font.color.rgb = RGBColor(245, 158, 11) # Ámbar dorado brillante

    # Resoluciones en 2 Columnas para eliminar totalmente la colisión vertical con las firmas:
    # Columna 1 (Izq): Resoluciones 1 y 2
    # Columna 2 (Der): Resoluciones 3 y 4
    res_col1_es = [
        ("1. Adjudicación Oficial:", "Aprobar formalmente la adjudicación del contrato a Vendor Beta con una puntuación auditada de 86,4/100."),
        ("2. Autorización Presupuestaria:", "Liberar una partida de 420.000 € (CAPEX/OPEX Año 1) sujeta al cumplimiento de hitos de la Fase 1 y 2.")
    ]
    res_col2_es = [
        ("3. Delegación de Firma:", "Facultar al CIO y al Director de Compras (CPO) para la rúbrica contractual y el anexo legal de SLA."),
        ("4. Congelación de Evaluación:", "Declarar el cierre formal del expediente de evaluación DAR y archivar las actas de auditoría técnica.")
    ]

    res_col1_en = [
        ("1. Contract Award:", "Formally award the enterprise procurement contract to Vendor Beta based on an audited score of 86.4/100."),
        ("2. Capital Authorization:", "Release initial budget disbursement of $420,000 (Year 1 CAPEX/OPEX) tied to Phase 1 & 2 milestones.")
    ]
    res_col2_en = [
        ("3. Delegation of Authority:", "Grant signing authority to the CIO and Chief Procurement Officer (CPO) for contract execution."),
        ("4. Evaluation Freeze:", "Formally declare the DAR evaluation process closed and register audited scores in corporate governance records.")
    ]

    col1_data = res_col1_es if lang == 'ES' else res_col1_en
    col2_data = res_col2_es if lang == 'ES' else res_col2_en

    # TextBox Columna 1 (Izq: x=1.05, y=4.20, w=5.45, h=1.08)
    tb_c1 = slide3.shapes.add_textbox(Inches(1.05), Inches(4.20), Inches(5.45), Inches(1.08))
    tf_c1 = tb_c1.text_frame
    tf_c1.vertical_anchor = MSO_ANCHOR.TOP
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_top = tf_c1.margin_right = tf_c1.margin_bottom = 0
    for idx_r, (r_title, r_desc) in enumerate(col1_data):
        p = tf_c1.paragraphs[0] if idx_r == 0 else tf_c1.add_paragraph()
        run_t = p.add_run()
        run_t.text = r_title + " "
        run_t.font.bold = True
        run_t.font.size = Pt(8)
        run_t.font.color.rgb = RGBColor(245, 158, 11) # Ámbar

        run_d = p.add_run()
        run_d.text = r_desc
        run_d.font.size = Pt(8)
        run_d.font.color.rgb = RGBColor(241, 245, 249)
        if idx_r > 0:
            p.space_before = Pt(4)

    # TextBox Columna 2 (Der: x=6.80, y=4.20, w=5.45, h=1.08)
    tb_c2 = slide3.shapes.add_textbox(Inches(6.80), Inches(4.20), Inches(5.45), Inches(1.08))
    tf_c2 = tb_c2.text_frame
    tf_c2.vertical_anchor = MSO_ANCHOR.TOP
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_top = tf_c2.margin_right = tf_c2.margin_bottom = 0
    for idx_r, (r_title, r_desc) in enumerate(col2_data):
        p = tf_c2.paragraphs[0] if idx_r == 0 else tf_c2.add_paragraph()
        run_t = p.add_run()
        run_t.text = r_title + " "
        run_t.font.bold = True
        run_t.font.size = Pt(8)
        run_t.font.color.rgb = RGBColor(245, 158, 11) # Ámbar

        run_d = p.add_run()
        run_d.text = r_desc
        run_d.font.size = Pt(8)
        run_d.font.color.rgb = RGBColor(241, 245, 249)
        if idx_r > 0:
            p.space_before = Pt(4)

    # 4 Bloques de Firma C-Level ubicados limpiamente abajo (y = 5.50, h = 1.25)
    # Entre y = 4.20 + 1.08 = 5.28 y y = 5.50 hay 0.22 in de margen libre. CERO SOLAPAMIENTO.
    sign_y = Inches(5.50)
    sign_w = Inches(2.65)
    sign_h = Inches(1.25)

    signs_es = [
        ("Chief Executive Officer (CEO)", "Dirección General / Presidencia"),
        ("Chief Financial Officer (CFO)", "Dirección Financiera"),
        ("Chief Information Officer (CIO)", "Dirección de Tecnología"),
        ("Chief Procurement Officer (CPO)", "Dirección de Compras")
    ]
    signs_en = [
        ("Chief Executive Officer (CEO)", "Office of the CEO / President"),
        ("Chief Financial Officer (CFO)", "Finance & Capital Allocation"),
        ("Chief Information Officer (CIO)", "Technology & Architecture"),
        ("Chief Procurement Officer (CPO)", "Strategic Sourcing & Vendor Ops")
    ]
    signs = signs_es if lang == 'ES' else signs_en

    for s_idx, (s_title, s_sub) in enumerate(signs):
        sx = Inches(1.05 + s_idx * 2.85)
        s_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sign_y, sign_w, sign_h)
        apply_gradient_fill(s_box, "1E293B", "0F172A", angle_deg=90)
        s_box.line.color.rgb = RGBColor(71, 85, 105) # Slate 600
        s_box.line.width = Pt(1)

        tf_s = s_box.text_frame
        tf_s.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = Inches(0.10)
        tf_s.margin_top = Inches(0.08)
        tf_s.margin_bottom = Inches(0.08)

        ps0 = tf_s.paragraphs[0]
        ps0.text = s_title
        ps0.font.size = Pt(8)
        ps0.font.bold = True
        ps0.font.color.rgb = RGBColor(245, 158, 11) # Ámbar dorado
        ps0.alignment = PP_ALIGN.CENTER

        ps1 = tf_s.add_paragraph()
        ps1.text = s_sub
        ps1.font.size = Pt(7)
        ps1.font.color.rgb = RGBColor(148, 163, 184) # Slate 400
        ps1.alignment = PP_ALIGN.CENTER

        ps2 = tf_s.add_paragraph()
        ps2.text = "[FIRMADO DIGITALMENTE]" if lang == 'ES' else "[DIGITALLY SIGNED]"
        ps2.font.size = Pt(7.5)
        ps2.font.color.rgb = RGBColor(16, 185, 129) # Verde Esmeralda
        ps2.font.bold = True
        ps2.alignment = PP_ALIGN.CENTER
        ps2.space_before = Pt(6)

    prs.save(out_path)
    print(f"[OK] Presentación PowerPoint generada ({lang}): {out_path}")
    return out_path


def main():
    print("Iniciando generación de presentaciones PowerPoint DAR C-Level actualizadas...")
    es_path = create_deck(lang='ES')
    en_path = create_deck(lang='EN')
    print("Presentaciones PowerPoint generadas con éxito.")


if __name__ == "__main__":
    main()
