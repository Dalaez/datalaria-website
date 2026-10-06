#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga/[ES]_Matriz_RACI_Balance_Carga/Presentacion_RACI_CLevel_ES.pptx
2. packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga/[EN]_Quantitative_RACI_Workload/Deck_RACI_CLevel_EN.pptx

Características de diseño Tier-1 (McKinsey / BCG / Bain / PMBOK / Prince2):
- Formato 16:9 Widescreen (13.333" x 7.5").
- Regla estricta de 3 diapositivas con Pirámide de Minto y Action Titles contundentes.
- Diapositiva 1: Diagnóstico de Gobernanza & Salud Operativa (4 KPI Cards y hallazgos clave).
- Diapositiva 2: Organigrama Funcional Matricial & Mapa de Sobrecarga (Estructura y gráfico de saturación con patologías).
- Diapositiva 3: Roadmap de Rebalanceo & Board Decision Gateway (4 fases de estabilización, 4 resoluciones y firmas).
- Sin solapes de texto, márgenes protegidos y acabados visuales pulidos.
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
COLOR_RED_BORDER = RGBColor(225, 29, 72)     # #E11D48 Rojo acento
COLOR_RED_TEXT = RGBColor(159, 18, 57)       # #9F1239 Rojo texto

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
    p_b.text = ("DATALARIA EXECUTIVE DECISION PACK · CONTROL OPERATIVO & GOBERNANZA · PMBOK / PRINCE2"
                if lang == 'ES' else
                "DATALARIA EXECUTIVE DECISION PACK · OPERATIONAL CONTROL & GOVERNANCE · PMBOK / PRINCE2")
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
    p_t.font.size = Pt(14)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK
    p_t.font.name = FONT_HEADING

    # Pie institucional
    tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.7), Inches(0.25))
    tf_f = tb_foot.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = (f"Datalaria.com · Documento Confidencial para Comité de Dirección & PMO | Diapositiva {slide_num} de {total_slides}"
                if lang == 'ES' else
                f"Datalaria.com · Confidential Executive Committee & PMO Document | Slide {slide_num} of {total_slides}")
    p_f.font.size = Pt(8)
    p_f.font.color.rgb = COLOR_TEXT_MUTED
    p_f.font.name = FONT_BODY


def create_workload_chart(lang='ES', out_path='temp_workload_chart.png'):
    """Genera gráfico de barras de alta resolución para la diapositiva 2."""
    fig, ax = plt.subplots(figsize=(6.2, 3.4), dpi=220)

    roles_es = ['Sponsor', 'PMO Lead', 'Tech Lead', 'Equipo Dev', 'QA Lead', 'UX/UI Des.', 'DevOps', 'Legal', 'Product Owner']
    roles_en = ['Sponsor', 'PMO Lead', 'Tech Lead', 'Eng. Team', 'QA Lead', 'UX/UI Des.', 'DevOps', 'Legal', 'Product Owner']
    roles = roles_es if lang == 'ES' else roles_en

    # Porcentajes de saturación modelados
    saturation = [52.5, 96.3, 142.5, 87.8, 86.9, 44.4, 69.4, 38.8, 81.3]

    y_pos = np.arange(len(roles))
    colors_list = []
    for s in saturation:
        if s > 100.0:
            colors_list.append('#E11D48') # Rojo cuello de botella
        elif s >= 80.0:
            colors_list.append('#F59E0B') # Ámbar límite
        else:
            colors_list.append('#10B981') # Verde saludable

    bars = ax.barh(y_pos, saturation, align='center', color=colors_list, height=0.62)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(roles, fontsize=8, fontweight='bold', color='#1E293B')
    ax.invert_yaxis()

    ax.axvline(100, color='#E11D48', linestyle='--', linewidth=1.2, label='100% Límite' if lang == 'ES' else '100% Capacity')
    ax.axvline(80, color='#F59E0B', linestyle=':', linewidth=1.0, label='80% Alerta' if lang == 'ES' else '80% Warning')

    ax.set_xlabel('Ratio de Saturación (% Capacidad Asignada)' if lang == 'ES' else 'Saturation Ratio (% Allocated Capacity)', fontsize=8, color='#475569')
    ax.set_xlim(0, 160)

    for bar, val in zip(bars, saturation):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, f"{val:.1f}%",
                va='center', ha='left', fontsize=7.5, fontweight='bold',
                color='#E11D48' if val > 100 else '#1E293B')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.tick_params(colors='#475569', labelsize=8)
    ax.grid(axis='x', linestyle='--', alpha=0.3, color='#94A3B8')
    ax.legend(loc='lower right', fontsize=7.5, frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0')

    plt.tight_layout()
    fig.savefig(out_path, dpi=220, bbox_inches='tight')
    plt.close(fig)
    return out_path


def create_deck(lang='ES', out_path=None):
    if out_path is None:
        base_dir = "packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga"
        sub_dir = "[ES]_Matriz_RACI_Balance_Carga" if lang == 'ES' else "[EN]_Quantitative_RACI_Workload"
        fname = "Presentacion_RACI_CLevel_ES.pptx" if lang == 'ES' else "Deck_RACI_CLevel_EN.pptx"
        out_path = os.path.join(base_dir, sub_dir, fname)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================================================
    # SLIDE 1: DIAGNÓSTICO DE GOBERNANZA & SALUD OPERATIVA
    # ==========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    title_s1 = (
        "El 38% de los hitos críticos diluye su responsabilidad entre múltiples Accountables y el Tech Lead acumula un 140% de saturación: se requiere rebalancear 8 entregables antes de Q3"
        if lang == 'ES' else
        "38% of critical milestones dilute accountability across multiple roles while the Tech Lead reaches 140% workload saturation: urgent rebalancing of 8 deliverables required before Q3"
    )
    add_header(slide1, title_s1, 1, 3, lang=lang)

    # 4 Tarjetas KPI
    card_w = Inches(2.78)
    card_h = Inches(1.35)
    card_y = Inches(1.60)

    cards_data_es = [
        ("INTEGRIDAD RACI (A=1, R≥1)", "84,0%", "21 de 25 entregables conformes", "F8FAFC", "EFF6FF", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT, COLOR_GREEN_TEXT),
        ("CUELLO DE BOTELLA CLAVE", "Tech Lead (142%)", "Sobrecarga crítica > 100%", "FFF1F2", "FEE2E2", COLOR_RED_BORDER, COLOR_RED_TEXT, COLOR_RED_TEXT),
        ("ENTREGABLES EN RIESGO", "4 Hitos", "2 con A múltiple · 2 huérfanos sin R", "FFFBEB", "FEF3C7", COLOR_AMBER_BORDER, COLOR_AMBER_TEXT, COLOR_AMBER_TEXT),
        ("CAPACIDAD REBALANCEABLE", "95,0 Horas", "Dedicación liberable de inmediato", "F0FDFA", "CCFBF1", COLOR_TEAL_ACCENT, COLOR_TEAL_ACCENT, COLOR_TEXT_MAIN),
    ]
    cards_data_en = [
        ("RACI INTEGRITY (A=1, R≥1)", "84.0%", "21 of 25 deliverables compliant", "F8FAFC", "EFF6FF", COLOR_BLUE_ACCENT, COLOR_BLUE_ACCENT, COLOR_GREEN_TEXT),
        ("PRIMARY BOTTLENECK", "Tech Lead (142%)", "Critical overload > 100%", "FFF1F2", "FEE2E2", COLOR_RED_BORDER, COLOR_RED_TEXT, COLOR_RED_TEXT),
        ("DELIVERABLES AT RISK", "4 Milestones", "2 with multiple A · 2 orphan without R", "FFFBEB", "FEF3C7", COLOR_AMBER_BORDER, COLOR_AMBER_TEXT, COLOR_AMBER_TEXT),
        ("REBALANCEABLE CAPACITY", "95.0 Hours", "Immediate transferable workload", "F0FDFA", "CCFBF1", COLOR_TEAL_ACCENT, COLOR_TEAL_ACCENT, COLOR_TEXT_MAIN),
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
        p1.font.size = Pt(15.5)
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

    # Panel 1: Hallazgos de Auditoría PMO
    p1_shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), panel_y, panel_w, panel_h)
    p1_shape.fill.solid()
    p1_shape.fill.fore_color.rgb = COLOR_CARD_BG
    p1_shape.line.color.rgb = COLOR_BORDER
    p1_shape.line.width = Pt(1)

    tb_p1 = slide1.shapes.add_textbox(Inches(0.95), panel_y + Inches(0.15), panel_w - Inches(0.3), panel_h - Inches(0.3))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True
    tf_p1.margin_left = tf_p1.margin_top = tf_p1.margin_right = tf_p1.margin_bottom = 0

    h_p1 = tf_p1.paragraphs[0]
    h_p1.text = "HALLAZGOS DE AUDITORÍA PMO & GOBERNANZA" if lang == 'ES' else "PMO AUDIT & GOVERNANCE FINDINGS"
    h_p1.font.size = Pt(11)
    h_p1.font.bold = True
    h_p1.font.color.rgb = COLOR_NAVY_DARK

    bullets_es_1 = [
        ("Accountability Diluida (WBS 3.3): ", "El desarrollo frontend tiene asignado 'A' dual (Tech Lead y Product Owner). Al fallar la integración nadie asume la pérdida económica."),
        ("Vacío de Ejecución Directa (WBS 4.1): ", "El Plan Maestro de Pruebas tiene Accountable formal en QA pero carece de ejecutor 'R', generando un cuello de botella silencioso."),
        ("Saturación Asimétrica del Tech Lead: ", "Acumula 7 entregables con 'A' y 5 con 'R', alcanzando 228 horas de dedicación frente a una capacidad nominal de 160 horas (142.5%)."),
        ("Parálisis por Consenso en Comités: ", "6 entregables técnicos involucran más de 4 áreas en rol 'Consulted' (C), ralentizando las decisiones técnicas un 45%."),
        ("Capacidad Ociosa en Soporte: ", "DevOps (69%) y UX/UI (44%) disponen de más de 80 horas liberables para absorber tareas delegadas sin coste incremental.")
    ]
    bullets_en_1 = [
        ("Diluted Accountability (WBS 3.3): ", "Frontend development has dual 'A' (Tech Lead and Product Owner). When delivery fails, no single executive assumes ownership."),
        ("Orphan Execution Gap (WBS 4.1): ", "Master Test Plan has formal QA Accountable but zero Responsible 'R' assigned, creating an invisible project roadblock."),
        ("Asymmetric Tech Lead Overload: ", "Concentrates 7 deliverables as 'A' and 5 as 'R', totaling 228 hours vs. 160h nominal capacity (142.5% saturation)."),
        ("Consensus Paralysis in Reviews: ", "6 technical tasks involve over 4 departments in Consulted (C) roles, inducing a 45% cycle-time delay in critical reviews."),
        ("Available Absorption Capacity: ", "DevOps (69%) and UX/UI (44%) possess over 80 idle hours ready to absorb delegated tasks with zero added cost.")
    ]
    b1_list = bullets_es_1 if lang == 'ES' else bullets_en_1
    for bold_txt, norm_txt in b1_list:
        p = tf_p1.add_paragraph()
        p.space_before = Pt(6)
        r_b = p.add_run()
        r_b.text = "• " + bold_txt
        r_b.font.bold = True
        r_b.font.size = Pt(9)
        r_b.font.color.rgb = COLOR_NAVY_DARK
        r_n = p.add_run()
        r_n.text = norm_txt
        r_n.font.size = Pt(8.5)
        r_n.font.color.rgb = COLOR_TEXT_MAIN

    # Panel 2: Impacto en el Negocio & Riesgos
    p2_shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), panel_y, panel_w, panel_h)
    p2_shape.fill.solid()
    p2_shape.fill.fore_color.rgb = COLOR_CARD_BG
    p2_shape.line.color.rgb = COLOR_BORDER
    p2_shape.line.width = Pt(1)

    tb_p2 = slide1.shapes.add_textbox(Inches(6.95), panel_y + Inches(0.15), panel_w - Inches(0.3), panel_h - Inches(0.3))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True
    tf_p2.margin_left = tf_p2.margin_top = tf_p2.margin_right = tf_p2.margin_bottom = 0

    h_p2 = tf_p2.paragraphs[0]
    h_p2.text = "IMPACTO EN NEGOCIO & COSTE DE NO INTERVENCIÓN" if lang == 'ES' else "BUSINESS IMPACT & COST OF INACTION"
    h_p2.font.size = Pt(11)
    h_p2.font.bold = True
    h_p2.font.color.rgb = COLOR_NAVY_DARK

    bullets_es_2 = [
        ("Retraso Proyectado en Go-Live: ", "La acumulación de tareas críticas en el Tech Lead introduce un desvío estimado de +6 semanas sobre el calendario maestro."),
        ("Riesgo Existencial de Burnout / Fuga: ", "Una saturación sostenida superior al 140% triplica la probabilidad de abandono voluntario de personal técnico clave."),
        ("Dilución de Responsabilidad Legal: ", "En caso de brecha en evaluación de seguridad (RGPD), la falta de un Accountable único expone al Consejo a sanciones regulatorias."),
        ("Sobrecoste Operativo Directo: ", "El retrabajo derivado de aprobaciones ambiguas y reuniones de consenso redundantes consume ~35.000 € mensuales de gasto indirecto."),
        ("Ventana de Intervención: ", "El rebalanceo antes del cierre de Fase 2 estabiliza los ratios en menos de 10 días laborables con coste cero de plantilla externa.")
    ]
    bullets_en_2 = [
        ("Projected Go-Live Delay: ", "Workload bottlenecks on the Tech Lead induce an estimated +6 weeks slippage on the master project schedule."),
        ("Key Talent Burnout & Turnover: ", "Sustained overload above 140% triples the probability of voluntary turnover in critical senior technical positions."),
        ("Regulatory & Compliance Exposure: ", "Without a single Accountable for security deliverables, regulatory penalties (GDPR) directly expose the Executive Board."),
        ("Direct Operational Inefficiency: ", "Rework from ambiguous approvals and redundant consensus meetings consumes ~€35,000 monthly in overhead friction."),
        ("Action Window: ", "Executing rebalancing prior to Phase 2 sign-off restores healthy workload within 10 business days without external hiring.")
    ]
    b2_list = bullets_es_2 if lang == 'ES' else bullets_en_2
    for bold_txt, norm_txt in b2_list:
        p = tf_p2.add_paragraph()
        p.space_before = Pt(6)
        r_b = p.add_run()
        r_b.text = "• " + bold_txt
        r_b.font.bold = True
        r_b.font.size = Pt(9)
        r_b.font.color.rgb = COLOR_NAVY_DARK
        r_n = p.add_run()
        r_n.text = norm_txt
        r_n.font.size = Pt(8.5)
        r_n.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================================================
    # SLIDE 2: ORGANIGRAMA FUNCIONAL MATRICIAL & MAPA DE SOBRECARGA
    # ==========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    title_s2 = (
        "El organigrama matricial revela sobrecarga crítica en roles técnicos y parálisis por consenso en tareas de negocio: el Tech Lead concentra 142% de capacidad y 5 roles operan como cuellos de botella"
        if lang == 'ES' else
        "Matrix org structure reveals critical workload saturation in technical leads and consensus paralysis in business tasks: Tech Lead operates at 142% capacity with 5 bottleneck risks"
    )
    add_header(slide2, title_s2, 2, 3, lang=lang)

    col_w = Inches(5.72)
    col_h = Inches(5.25)
    col_y = Inches(1.60)

    # Contenedor Izquierdo: Organigrama Funcional Matricial
    s_org = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), col_y, col_w, col_h)
    s_org.fill.solid()
    s_org.fill.fore_color.rgb = COLOR_CARD_BG
    s_org.line.color.rgb = COLOR_BORDER
    s_org.line.width = Pt(1)

    tb_org = slide2.shapes.add_textbox(Inches(0.95), col_y + Inches(0.12), col_w - Inches(0.3), Inches(0.4))
    tf_org = tb_org.text_frame
    tf_org.margin_left = tf_org.margin_top = tf_org.margin_right = tf_org.margin_bottom = 0
    p_org_h = tf_org.paragraphs[0]
    p_org_h.text = "ORGANIGRAMA FUNCIONAL MATRICIAL & DISTRIBUCIÓN DE ROLES" if lang == 'ES' else "CROSS-FUNCTIONAL MATRIX ORG CHART & ROLE ALLOCATION"
    p_org_h.font.size = Pt(11)
    p_org_h.font.bold = True
    p_org_h.font.color.rgb = COLOR_NAVY_DARK

    # 4 Bloques Jerárquicos en el Organigrama Matricial
    blocks_es = [
        ("1. DIRECCIÓN & SPONSORSHIP (Comité Directivo)", "3 Accountables · 2 Responsibles · Saturación: 52.5% (Saludable)",
         "Foco: Aprobación de presupuestos, charter de proyecto y go-live final.", COLOR_BLUE_ACCENT, "EFF6FF"),
        ("2. GESTIÓN & ORQUESTACIÓN (PMO & Product Owner)", "7 Accountables · 6 Responsibles · Saturación: 88.8% (Alerta)",
         "Foco: Control de hitos, alcance, BRD y pruebas de aceptación UAT.", COLOR_TEAL_ACCENT, "F0FDFA"),
        ("3. INGENIERÍA & ARQUITECTURA (Tech Lead & Dev)", "9 Accountables · 11 Responsibles · Saturación: 115.1% (CRÍTICO)",
         "Foco: Arquitectura SAD, backend, frontend y pipelines CI/CD.", COLOR_RED_BORDER, "FFF1F2"),
        ("4. CONTROL, CALIDAD & OPERACIONES (QA, DevOps, Legal)", "6 Accountables · 6 Responsibles · Saturación: 65.0% (Capacidad Disponible)",
         "Foco: Pruebas unitarias, seguridad RGPD, cutover e infraestructura.", COLOR_NAVY_MED, "F8FAFC")
    ]
    blocks_en = [
        ("1. EXECUTIVE STEERING & SPONSORSHIP", "3 Accountables · 2 Responsibles · Saturation: 52.5% (Healthy)",
         "Focus: Budget approval, project charter authorization, and final go-live sign-off.", COLOR_BLUE_ACCENT, "EFF6FF"),
        ("2. PMO MANAGEMENT & PRODUCT OWNERSHIP", "7 Accountables · 6 Responsibles · Saturation: 88.8% (Warning)",
         "Focus: Milestone tracking, WBS baseline, BRD specs, and UAT sign-off.", COLOR_TEAL_ACCENT, "F0FDFA"),
        ("3. ENGINEERING & ARCHITECTURE CORE", "9 Accountables · 11 Responsibles · Saturation: 115.1% (CRITICAL)",
         "Focus: SAD architecture, microservices backend, frontend web, and CI/CD.", COLOR_RED_BORDER, "FFF1F2"),
        ("4. QA, DEVOPS & COMPLIANCE OPERATIONS", "6 Accountables · 6 Responsibles · Saturation: 65.0% (Available Capacity)",
         "Focus: Automated testing, GDPR compliance, production cutover, and Cloud infra.", COLOR_NAVY_MED, "F8FAFC")
    ]
    blocks = blocks_es if lang == 'ES' else blocks_en

    for b_idx, (b_title, b_metrics, b_desc, border_c, bg_c) in enumerate(blocks):
        by = col_y + Inches(0.55 + b_idx * 1.14)
        bw = col_w - Inches(0.3)
        bh = Inches(1.02)
        b_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), by, bw, bh)
        b_box.fill.solid()
        b_box.fill.fore_color.rgb = RGBColor.from_string(bg_c)
        b_box.line.color.rgb = border_c
        b_box.line.width = Pt(1.5)

        tb_b = slide2.shapes.add_textbox(Inches(1.05), by + Inches(0.08), bw - Inches(0.2), bh - Inches(0.16))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

        p0 = tf_b.paragraphs[0]
        p0.text = b_title
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_DARK

        p1 = tf_b.add_paragraph()
        p1.text = b_metrics
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = border_c

        p2 = tf_b.add_paragraph()
        p2.text = b_desc
        p2.font.size = Pt(7.8)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # Contenedor Derecho: Gráfico de Barras de Saturación & Patologías
    s_chart = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), col_y, col_w, col_h)
    s_chart.fill.solid()
    s_chart.fill.fore_color.rgb = COLOR_CARD_BG
    s_chart.line.color.rgb = COLOR_BORDER
    s_chart.line.width = Pt(1)

    chart_img = create_workload_chart(lang=lang, out_path=f"temp_chart_{lang}.png")
    slide2.shapes.add_picture(chart_img, Inches(6.9), col_y + Inches(0.15), width=Inches(5.52))

    # Caja de Patologías en la base del contenedor derecho
    pat_y = col_y + Inches(3.45)
    pat_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95), pat_y, Inches(5.42), Inches(1.65))
    pat_box.fill.solid()
    pat_box.fill.fore_color.rgb = COLOR_WHITE
    pat_box.line.color.rgb = COLOR_BORDER
    pat_box.line.width = Pt(1)

    tb_pat = slide2.shapes.add_textbox(Inches(7.05), pat_y + Inches(0.08), Inches(5.22), Inches(1.5))
    tf_pat = tb_pat.text_frame
    tf_pat.word_wrap = True
    tf_pat.margin_left = tf_pat.margin_top = tf_pat.margin_right = tf_pat.margin_bottom = 0

    p_ph = tf_pat.paragraphs[0]
    p_ph.text = "DIAGNÓSTICO DE PATOLOGÍAS ORGANIZATIVAS" if lang == 'ES' else "ORGANIZATIONAL PATHOLOGY DIAGNOSIS"
    p_ph.font.size = Pt(9.5)
    p_ph.font.bold = True
    p_ph.font.color.rgb = COLOR_NAVY_DARK

    pats_es = [
        ("• Dilución de Rendición de Cuentas: ", "Múltiples 'A' provocan 'la tragedia de los comunes': nadie rinde cuentas."),
        ("• Sobrecarga de Cuello de Botella: ", "Tech Lead (142%) centraliza decisiones y tareas operativas de bajo valor."),
        ("• Parálisis por Consenso: ", "Comités sobredimensionados de 'C' bloquean el ritmo de entregas semanales."),
        ("• Tareas Huérfanas de Ejecución: ", "Hitos con A directivo pero sin R técnico provocan bloqueos imprevistos.")
    ]
    pats_en = [
        ("• Diluted Accountability: ", "Multiple 'A' causes 'tragedy of the commons': when all own it, nobody is accountable."),
        ("• Bottleneck Overload: ", "Tech Lead (142%) centralizes high-level architectural calls and routine dev tasks."),
        ("• Consensus Paralysis: ", "Oversized 'Consulted' forums delay decision-making by over 45%."),
        ("• Orphan Deliverables: ", "Tasks with executive 'A' but zero technical 'R' lead to unexpected blockers.")
    ]
    pats = pats_es if lang == 'ES' else pats_en
    for b_lbl, b_txt in pats:
        p = tf_pat.add_paragraph()
        r1 = p.add_run()
        r1.text = b_lbl
        r1.font.bold = True
        r1.font.size = Pt(8)
        r1.font.color.rgb = COLOR_RED_TEXT if "Dilución" in b_lbl or "Diluted" in b_lbl or "Botella" in b_lbl or "Bottleneck" in b_lbl else COLOR_NAVY_DARK
        r2 = p.add_run()
        r2.text = b_txt
        r2.font.size = Pt(7.8)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================================================
    # SLIDE 3: ROADMAP DE REBALANCEO & BOARD DECISION GATEWAY
    # ==========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    title_s3 = (
        "Roadmap de rebalanceo en 4 fases para estabilizar la carga operativa y Gateway de Decisión del Comité para blindar la gobernanza única e indelegable"
        if lang == 'ES' else
        "Four-phase workload rebalancing roadmap to restore operational health alongside Board Decision Gateway enforcing strict single accountability"
    )
    add_header(slide3, title_s3, 3, 3, lang=lang)

    # MITAD SUPERIOR: ROADMAP DE 4 FASES (Y = 1.60 a 3.80)
    tb_rm_h = slide3.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.7), Inches(0.3))
    tf_rm_h = tb_rm_h.text_frame
    tf_rm_h.margin_left = tf_rm_h.margin_top = tf_rm_h.margin_right = tf_rm_h.margin_bottom = 0
    p_rm = tf_rm_h.paragraphs[0]
    p_rm.text = "HOJA DE RUTA DE ESTABILIZACIÓN OPERATIVA EN 4 FASES" if lang == 'ES' else "4-PHASE OPERATIONAL STABILIZATION ROADMAP"
    p_rm.font.size = Pt(10.5)
    p_rm.font.bold = True
    p_rm.font.color.rgb = COLOR_NAVY_DARK

    phases_es = [
        ("FASE 1: ALINEACIÓN DIRECTIVA", "Semanas 1 - 2", "Aprobación formal de A=1", "Congelación del principio de Accountable único e intransferible. Resolución de los 2 hitos con A múltiple en WBS 3.3 y WBS 1.2."),
        ("FASE 2: DESCARGA TÉCNICA", "Semanas 3 - 4", "Transferencia de 68h de R", "Delegación de tareas directas 'R' del Tech Lead (CI/CD a DevOps, migración a Senior Backend). Reducción de saturación al 88%."),
        ("FASE 3: RACIONALIZACIÓN 'C' A 'I'", "Semanas 5 - 6", "Reducción de Comités", "Degradación sistemática de 'Consulted' a 'Informed' en entregables sin dependencia técnica estricta. Erradicación del consenso pasivo."),
        ("FASE 4: SLAs & AUDITORÍA PMO", "Semanas 7 - 8", "Control Continuo", "Establecimiento de cadencia de revisión bimestral en PMO. Integración de alertas de saturación (>80%) en el cuadro de mando directivo.")
    ]
    phases_en = [
        ("PHASE 1: C-LEVEL ALIGNMENT", "Weeks 1 - 2", "Strict A=1 Enforcement", "Formal ratification of single non-delegable Accountable rule. Elimination of dual-A conflicts on WBS 3.3 and WBS 1.2."),
        ("PHASE 2: TECHNICAL UNBURDENING", "Weeks 3 - 4", "Reassignment of 68h R", "Delegation of direct execution 'R' from Tech Lead (CI/CD to DevOps, migration to Senior Eng). Tech Lead saturation cut to 88%."),
        ("PHASE 3: STREAMLINING 'C' TO 'I'", "Weeks 5 - 6", "Eliminating Review Drag", "Systematic downgrade of 'Consulted' to 'Informed' on non-dependent tasks. Eradication of passive committee sign-offs."),
        ("PHASE 4: SLAS & PMO AUDIT", "Weeks 7 - 8", "Continuous Monitoring", "Implementation of bimonthly PMO capacity audit rhythm. Automatic escalation for roles exceeding 80% saturation threshold.")
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
        box.line.color.rgb = COLOR_BLUE_ACCENT if idx == 0 else (COLOR_TEAL_ACCENT if idx == 1 else COLOR_BORDER)
        box.line.width = Pt(1.5) if idx < 2 else Pt(1)

        tb = slide3.shapes.add_textbox(px + Inches(0.12), ph_y + Inches(0.1), ph_w - Inches(0.24), ph_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = p_title
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_BLUE_ACCENT if idx == 0 else COLOR_NAVY_DARK

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

    # MITAD INFERIOR: BOARD DECISION GATEWAY (Y = 3.90 a 6.95)
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
        ("1. Principio de Rendición de Cuentas Única: ", "Se ratifica que todo entregable tendrá exactamente un Accountable (A=1). Queda prohibida la asignación compartida bajo apercibimiento de invalidez."),
        ("2. Mandato de Delegación Técnica: ", "Se aprueba la transferencia inmediata de 68 horas de ejecución 'R' desde el Tech Lead hacia DevOps e Ingeniería Senior."),
        ("3. Racionalización de Consultas (C): ", "Se establece un límite máximo de dos áreas en rol 'Consulted' para tareas no regulatorias, agilizando el ciclo de desarrollo."),
        ("4. Auditoría Bimestral PMO: ", "La PMO reportará al Comité de Operaciones cualquier rol con saturación proyectada superior al 85% para balanceo preventivo.")
    ]
    res_en = [
        ("1. Single Accountability Mandate: ", "Ratification that every milestone must have exactly one Accountable (A=1). Shared accountability is strictly voided across all teams."),
        ("2. Technical Delegation Authorization: ", "Immediate transfer of 68 execution hours 'R' from Tech Lead to DevOps and Senior Engineering team."),
        ("3. Consultation Streamlining: ", "Maximum cap of two departments in Consulted 'C' capacity on non-regulatory deliverables to accelerate execution cycles."),
        ("4. Bimonthly PMO Workload Audit: ", "PMO shall formally report any role exceeding 85% projected capacity to Executive Committee for preventive rebalancing.")
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
        run_b = p.add_run()
        run_b.text = r_bold
        run_b.font.bold = True
        run_b.font.size = Pt(8.5)
        run_b.font.color.rgb = COLOR_NAVY_DARK
        run_t = p.add_run()
        run_t.text = r_text
        run_t.font.size = Pt(8)
        run_t.font.color.rgb = COLOR_TEXT_MAIN

    # Bloque de 4 Firmas Directivas en la parte inferior del Gateway
    sig_y = gw_y + Inches(2.05)
    sig_w = Inches(2.65)
    sig_h = Inches(0.75)

    sigs_es = [
        ("CEO / Director General", "Aprobación Ejecutiva"),
        ("COO / Director de Operaciones", "Gobierno Operativo"),
        ("PMO Director / Gestión", "Auditoría de Hitos"),
        ("CTO / Tech Director", "Capacidad Técnica")
    ]
    sigs_en = [
        ("Chief Executive Officer (CEO)", "Executive Authorization"),
        ("Chief Operating Officer (COO)", "Operational Governance"),
        ("PMO Director / VP Delivery", "Milestone Audit"),
        ("Chief Technology Officer (CTO)", "Technical Capacity")
    ]
    sigs = sigs_es if lang == 'ES' else sigs_en

    for s_idx, (role_name, purpose) in enumerate(sigs):
        sx = Inches(1.0 + s_idx * 2.88)
        # Línea de firma
        l_shape = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, sx, sig_y + Inches(0.35), sig_w, Inches(0.02))
        l_shape.fill.solid()
        l_shape.fill.fore_color.rgb = COLOR_BORDER
        l_shape.line.color.rgb = COLOR_BORDER

        tb_s = slide3.shapes.add_textbox(sx, sig_y + Inches(0.38), sig_w, Inches(0.35))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0

        p_rn = tf_s.paragraphs[0]
        p_rn.text = role_name
        p_rn.font.bold = True
        p_rn.font.size = Pt(8)
        p_rn.font.color.rgb = COLOR_NAVY_DARK

        p_purp = tf_s.add_paragraph()
        p_purp.text = purpose
        p_purp.font.size = Pt(7)
        p_purp.font.color.rgb = COLOR_TEXT_MUTED

    # Guardar presentación
    prs.save(out_path)
    print(f"  -> Guardada presentación PPTX: {out_path}")

    # Limpiar archivo temporal si existe
    if os.path.exists(f"temp_chart_{lang}.png"):
        os.remove(f"temp_chart_{lang}.png")


def main():
    base_dir = "packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga"
    dir_es = os.path.join(base_dir, "[ES]_Matriz_RACI_Balance_Carga")
    dir_en = os.path.join(base_dir, "[EN]_Quantitative_RACI_Workload")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    file_es = os.path.join(dir_es, "Presentacion_RACI_CLevel_ES.pptx")
    file_en = os.path.join(dir_en, "Deck_RACI_CLevel_EN.pptx")

    print("[1/2] Generando presentación ejecutiva en Español...")
    create_deck(lang='ES', out_path=file_es)

    print("[2/2] Generando presentación ejecutiva en Inglés...")
    create_deck(lang='EN', out_path=file_en)


if __name__ == "__main__":
    main()
