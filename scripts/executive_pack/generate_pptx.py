#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) para:
1. Presentacion_CLevel_DAFO_CAME_ES.pptx (Versión en Español)
2. Executive_CLevel_Deck_SWOT_TOWS_EN.pptx (Versión en Inglés)

Estructura de diapositivas basada en la Pirámide de Minto (SCQA) con Action Titles.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --- PALETA CORPORATIVA DATALARIA ---
COLOR_NAVY_DARK = RGBColor(15, 23, 42)     # #0F172A Slate 900
COLOR_NAVY_MED = RGBColor(30, 41, 59)      # #1E293B Slate 800
COLOR_BLUE_ACCENT = RGBColor(37, 99, 235)  # #2563EB Blue 600
COLOR_BLUE_LIGHT = RGBColor(239, 246, 255) # #EFF6FF Blue 50
COLOR_TEAL_ACCENT = RGBColor(13, 148, 136) # #0D9488 Teal 600
COLOR_AMBER = RGBColor(217, 119, 6)        # #D97706 Amber 600
COLOR_AMBER_LIGHT = RGBColor(254, 243, 199)# #FEF3C7 Amber 100
COLOR_RED_ACCENT = RGBColor(225, 29, 72)   # #E11D48 Rose 600
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_TEXT_MAIN = RGBColor(30, 41, 59)     # #1E293B
COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
COLOR_CARD_BG = RGBColor(248, 250, 252)    # #F8FAFC
COLOR_BORDER = RGBColor(203, 213, 225)     # #CBD5E1

FONT_TITLE = "Segoe UI"
FONT_BODY = "Segoe UI"


def create_deck(lang='ES'):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    texts = {
        'ES': {
            'out_path': "static/downloads/dafo-came-es/Presentacion_CLevel_DAFO_CAME_ES.pptx",
            'header_kicker': "COMITÉ DE DIRECCIÓN • REVISIÓN ESTRATÉGICA & DECISIÓN DE ASIGNACIÓN DE CAPITAL",
            'footer_left': "Datalaria.com | Executive Decision Pack • Uso Estrictamente Confidencial para Consejo",
            'footer_right': "Página {cur} de 3",
            
            # Slide 1
            's1_action_title': "Postura Ofensiva Validada: La robustez en margen (+18%) y retención NRR (118%) financia la captura del nuevo mercado digital en Q3.",
            's1_sub': "Diagnóstico de situación según modelo DAFO Cuantitativo normalizado. Se identifican ventajas competitivas defendibles y focos prioritarios.",
            's1_card1_tag': "DIAGNÓSTICO CUANTITATIVO",
            's1_card1_title': "Vector (+2.10, +1.85)",
            's1_card1_desc': "Postura dominante OFENSIVA (Maxi-Maxi). Magnitud de impulso de 2.80 pts. La solidez interna supera con holgura los cuellos de botella.",
            's1_card2_tag': "VENTAJA DEFENDIBLE (MOAT)",
            's1_card2_title': "Propiedad Intelectual + Margen",
            's1_card2_desc': "3 patentes europeas registradas y margen EBITDA del 24.2% permiten absorber inversiones de crecimiento sin acudir a deuda bancaria.",
            's1_card3_tag': "VULNERABILIDAD CRÍTICA",
            's1_card3_title': "Concentración Top-2 (42%)",
            's1_card3_desc': "Elevada dependencia de 2 clientes clave y ciclo comercial enterprise prolongado (8.5 meses) exigen diversificación comercial urgente.",
            's1_card4_tag': "RETORNO DE INVERSIÓN (ROI)",
            's1_card4_title': "245k € Presupuesto → +1.2M €",
            's1_card4_desc': "Plan CAME estructurado en 4 líneas. Retorno estimado de 1.2M € en nuevo ARR dentro de los primeros 12 meses de despliegue operativo.",
            's1_bottom_bar': "Gobernanza de Comité: Sesión formal de decisión de asignación de capital y aprobación de partida presupuestaria para el ejercicio 2026-2027.",

            # Slide 2
            's2_action_title': "El Cruce Cuantitativo Concentra el 68% del Potencial en Sinergias Ofensivas (F-O), Mandatando Blindaje Inmediato en Concentración (D-A).",
            's2_sub': "Matriz de Cruce de Impacto y Cuadrante Cartesiano. Traducción de interdependencias estratégicas en prioridades de ejecución.",
            's2_quad_title': "Matriz de Cuadrantes Estratégicos (Posición Cartesiana)",
            's2_heat_title': "Resumen de Intensidad de Cruce (TOWS Forces)",
            's2_box_so_title': "Sinergias Ofensivas F-O (38 pts)",
            's2_box_so_desc': "Aceleración en captura de fondos NextGen EU apoyados en patentes propias y alianzas con integradores globales (Accenture/Indra).",
            's2_box_st_title': "Estrategias Defensivas F-A (26 pts)",
            's2_box_st_desc': "Blindaje de contratos plurianuales de clientes enterprise para neutralizar la entrada de proveedores low-cost y anticipar NIS2.",
            's2_box_wo_title': "Iniciativas de Reorientación D-O (18 pts)",
            's2_box_wo_desc': "Despliegue de red de distribución en LatAm y refactorización del motor de facturación multi-divisa para reducir lead time a 5 meses.",
            's2_box_wt_title': "Vulnerabilidades de Supervivencia D-A (29 pts)",
            's2_box_wt_desc': "Punto crítico: la dependencia de 2 clientes frente a la presión de precios de competidores exige diversificación inmediata de cartera.",

            # Slide 3
            's3_action_title': "Despliegue CAME 2026: 4 Iniciativas Priorizadas con 245.000 € de Presupuesto para Asegurar 1.2M € de Nuevo Margen.",
            's3_sub': "Hoja de ruta operativa por trimestres con responsable C-Level asignado, presupuesto detallado y caja de decisión requerida.",
            's3_q1_title': "Q1: Ciberseguridad & Blindaje",
            's3_q1_text': "• CAME-A01: Contratos plurianuales top accounts (CEO)\n• CAME-A02: Auditoría NIS2 / DORA (CISO)\nPresupuesto: 45.000 €",
            's3_q2_title': "Q2: Expansión & Canal LatAm",
            's3_q2_text': "• CAME-C01: Red comercial LatAm (CCO)\n• CAME-C02: Acuerdo integradores (VP Sales)\nPresupuesto: 80.000 €",
            's3_q3_title': "Q3: Despliegue Industrial SaaS",
            's3_q3_text': "• CAME-E01: 40 factorías NextGen (COO)\n• CAME-C03: Refactorización billing (CTO)\nPresupuesto: 90.000 €",
            's3_q4_title': "Q4: Consolidación & IP Moat",
            's3_q4_text': "• CAME-M01: Ampliación patentes Asia (Legal)\n• CAME-M02: LTIP retención I+D (CPO)\nPresupuesto: 30.000 €",
            's3_dec_header': "DECISIÓN REQUERIDA DEL COMITÉ DE DIRECCIÓN (BOARD DECISION GATEWAY)",
            's3_dec_1': "1. APROBACIÓN PRESUPUESTARIA: Autorizar partida de 245.000 € (140k € CAPEX / 105k € OPEX) con cargo al fondo de inversión estratégica.",
            's3_dec_2': "2. PATROCINIO EJECUTIVO: Ratificar al COO como Sponsor de CAME-E01 y al CCO como Sponsor del Programa de Diversificación LatAm.",
            's3_dec_3': "3. GOBERNANZA Y REPORTE: Establecer reuniones mensuales de seguimiento y presentación de KPIs de avance en cada Consejo trimestral.",
        },
        'EN': {
            'out_path': "static/downloads/swot-tows-en/Executive_CLevel_Deck_SWOT_TOWS_EN.pptx",
            'header_kicker': "BOARD OF DIRECTORS • STRATEGIC REVIEW & CAPITAL ALLOCATION GATEWAY",
            'footer_left': "Datalaria.com | Executive Decision Pack • Strictly Confidential for Board Use",
            'footer_right': "Slide {cur} of 3",
            
            # Slide 1
            's1_action_title': "Offensive Posture Validated: Operating Margin (+18%) and NRR (118%) Secure Capital to Scale Industrial AI Expansion by Q3.",
            's1_sub': "Quantitative SWOT assessment baseline. Clear defensible moats identified alongside urgent single-client concentration risks.",
            's1_card1_tag': "QUANTITATIVE BASELINE",
            's1_card1_title': "Vector (+2.10, +1.85)",
            's1_card1_desc': "Dominant OFFENSIVE posture (Maxi-Maxi). Momentum vector magnitude at 2.80 pts. Internal strengths comfortably exceed operational weaknesses.",
            's1_card2_tag': "DEFENSIBLE MOAT",
            's1_card2_title': "Proprietary IP + Cash Margin",
            's1_card2_desc': "3 registered patents and 24.2% EBITDA margin finance growth initiatives organically without debt dilution.",
            's1_card3_tag': "CRITICAL VULNERABILITY",
            's1_card3_title': "Top-2 Concentration (42%)",
            's1_card3_desc': "High revenue concentration in 2 key accounts combined with long enterprise sales cycles (8.5 months) demands immediate diversification.",
            's1_card4_tag': "CAPITAL & ROI",
            's1_card4_title': "€245k Budget → +€1.2M ARR",
            's1_card4_desc': "Structured 4-pillar TOWS action plan. Expected incremental ARR of €1.2M within 12 months of operational rollout.",
            's1_bottom_bar': "Board Gateway: Formal decision meeting for capital allocation authorization and initiative sponsor ratification for FY2026-2027.",

            # Slide 2
            's2_action_title': "Factor Cross-Impact Concentrates 68% of Synergies in Offensive Space (S-O), Mandating Strategic Moat Against Customer Concentration (W-T).",
            's2_sub': "TOWS Cross-Impact Matrix and Cartesian quadrant positioning. Translating analytical interdependencies into board execution priorities.",
            's2_quad_title': "Cartesian Strategic Matrix (Vector Positioning)",
            's2_heat_title': "TOWS Cross-Impact Forces Summary",
            's2_box_so_title': "Offensive Synergies S-O (38 pts)",
            's2_box_so_desc': "Accelerate rollout across smart factory subsidies using proprietary IP and joint go-to-market with Tier-1 system integrators.",
            's2_box_st_title': "Defensive Strategies S-T (26 pts)",
            's2_box_st_desc': "Secure multi-year enterprise lock-ins to defeat low-cost Asian market entrants and pre-empt NIS2/DORA compliance mandates.",
            's2_box_wo_title': "Turnaround Initiatives W-O (18 pts)",
            's2_box_wo_desc': "Build LatAm distribution network and refactor multi-currency billing engine to compress sales cycle down to 5 months.",
            's2_box_wt_title': "Survival Vulnerabilities W-T (29 pts)",
            's2_box_wt_desc': "Critical stress point: top client concentration exposed to price erosion requires rapid account diversification.",

            # Slide 3
            's3_action_title': "2026 TOWS Deployment: 4 Prioritized Initiatives with €245k Capital Allocation to Capture €1.2M Incremental ARR.",
            's3_sub': "Quarterly operational roadmap with assigned C-Level executive ownership, financial budget, and Board Decision Gateway.",
            's3_q1_title': "Q1: Cyber Moat & Account Lock-in",
            's3_q1_text': "• TOWS-T01: Multi-year key account lock-in (CEO)\n• TOWS-T02: NIS2 / DORA compliance readiness (CISO)\nAllocated: €45,000",
            's3_q2_title': "Q2: Channel & Geo Expansion",
            's3_q2_text': "• TOWS-W01: LatAm distribution channel (CCO)\n• TOWS-W02: SI co-selling framework (VP Sales)\nAllocated: €80,000",
            's3_q3_title': "Q3: Industrial SaaS Scaling",
            's3_q3_text': "• TOWS-O01: 40 manufacturing sites rollout (COO)\n• TOWS-W03: Billing microservice refactor (CTO)\nAllocated: €90,000",
            's3_q4_title': "Q4: Talent Moat & Patent Defense",
            's3_q4_text': "• TOWS-S01: Supplemental patent filing (Legal)\n• TOWS-S02: Senior R&D retention LTIP (CPO)\nAllocated: €30,000",
            's3_dec_header': "BOARD DECISION GATEWAY (REQUIRED ACTION)",
            's3_dec_1': "1. CAPITAL ALLOCATION: Approve strategic appropriation of €245,000 (€140k CAPEX / €105k OPEX) from corporate reserves.",
            's3_dec_2': "2. EXECUTIVE SPONSORSHIP: Formally assign COO as Sponsor for TOWS-O01 and CCO for the Commercial Diversification Program.",
            's3_dec_3': "3. GOVERNANCE & REPORTING: Establish monthly PMO steering committee and quarterly Board milestone verification reviews.",
        }
    }[lang]

    # Helper para cabecera común
    def add_slide_header(slide, action_title, sub_text, cur_slide):
        # Kicker
        kicker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
        tf_k = kicker_box.text_frame
        tf_k.word_wrap = True
        p_k = tf_k.paragraphs[0]
        p_k.text = texts['header_kicker']
        p_k.font.name = FONT_TITLE
        p_k.font.size = Pt(9)
        p_k.font.bold = True
        p_k.font.color.rgb = COLOR_BLUE_ACCENT

        # Action Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.75))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = action_title
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(17)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY_DARK

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.35))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = sub_text
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = COLOR_TEXT_MUTED

        # Footer divider line
        divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
        divider.fill.solid()
        divider.fill.fore_color.rgb = COLOR_BORDER
        divider.line.fill.background()

        # Footer text
        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8.0), Inches(0.3))
        tf_f = f_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = texts['footer_left']
        p_f.font.name = FONT_BODY
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = COLOR_TEXT_MUTED

        p_box = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.0), Inches(0.3))
        tf_p = p_box.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.RIGHT
        p_p.text = texts['footer_right'].format(cur=cur_slide)
        p_p.font.name = FONT_BODY
        p_p.font.size = Pt(8.5)
        p_p.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================================================
    # SLIDE 1: SÍNTESIS EJECUTIVA (EXECUTIVE SYNTHESIS)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_header(s1, texts['s1_action_title'], texts['s1_sub'], 1)

    # 4 Tarjetas de Impacto
    cards = [
        (texts['s1_card1_tag'], texts['s1_card1_title'], texts['s1_card1_desc'], COLOR_BLUE_ACCENT, COLOR_BLUE_LIGHT),
        (texts['s1_card2_tag'], texts['s1_card2_title'], texts['s1_card2_desc'], COLOR_TEAL_ACCENT, RGBColor(236, 253, 245)),
        (texts['s1_card3_tag'], texts['s1_card3_title'], texts['s1_card3_desc'], COLOR_AMBER, COLOR_AMBER_LIGHT),
        (texts['s1_card4_tag'], texts['s1_card4_title'], texts['s1_card4_desc'], COLOR_NAVY_DARK, RGBColor(241, 245, 249)),
    ]

    card_width = Inches(2.78)
    card_gap = Inches(0.20)
    card_start_x = Inches(0.8)
    card_y = Inches(1.85)
    card_h = Inches(4.3)

    for idx, (tag, title, desc, accent_color, bg_color) in enumerate(cards):
        cx = card_start_x + idx * (card_width + card_gap)

        # Fondo Tarjeta
        shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_width, card_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = COLOR_BORDER
        shape.line.width = Pt(1)

        # Barra superior decorativa
        bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, card_y, card_width, Inches(0.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_color
        bar.line.fill.background()

        # Texto interior
        tb = s1.shapes.add_textbox(cx + Inches(0.2), card_y + Inches(0.25), card_width - Inches(0.4), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = tag
        p0.font.name = FONT_TITLE
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = accent_color

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p1.space_before = Pt(8)
        p1.space_after = Pt(12)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # Barra Inferior de Resumen
    b_bar = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.55))
    b_bar.fill.solid()
    b_bar.fill.fore_color.rgb = COLOR_NAVY_MED
    b_bar.line.fill.background()

    b_tb = s1.shapes.add_textbox(Inches(0.9), Inches(6.32), Inches(11.5), Inches(0.5))
    b_tf = b_tb.text_frame
    b_p = b_tf.paragraphs[0]
    b_p.text = texts['s1_bottom_bar']
    b_p.font.name = FONT_BODY
    b_p.font.size = Pt(9.5)
    b_p.font.bold = True
    b_p.font.color.rgb = COLOR_WHITE
    b_p.alignment = PP_ALIGN.CENTER

    # ==========================================================================
    # SLIDE 2: MATRIZ CUANTITATIVA & MAPA DE CUADRANTES
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, texts['s2_action_title'], texts['s2_sub'], 2)

    # Contenedor Izquierdo: Cuadrantes Cartesiano
    left_x = Inches(0.8)
    left_y = Inches(1.85)
    left_w = Inches(5.6)
    left_h = Inches(4.9)

    left_bg = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, left_y, left_w, left_h)
    left_bg.fill.solid()
    left_bg.fill.fore_color.rgb = COLOR_CARD_BG
    left_bg.line.color.rgb = COLOR_BORDER
    left_bg.line.width = Pt(1)

    l_tb = s2.shapes.add_textbox(left_x + Inches(0.2), left_y + Inches(0.15), left_w - Inches(0.4), Inches(0.4))
    l_tf = l_tb.text_frame
    l_p = l_tf.paragraphs[0]
    l_p.text = texts['s2_quad_title']
    l_p.font.name = FONT_TITLE
    l_p.font.size = Pt(11)
    l_p.font.bold = True
    l_p.font.color.rgb = COLOR_NAVY_DARK

    # Dibujo de los 4 cuadrantes dentro del contenedor
    sub_w = Inches(2.4)
    sub_h = Inches(1.7)
    qx1 = left_x + Inches(0.3)
    qx2 = left_x + Inches(2.9)
    qy1 = left_y + Inches(0.65)
    qy2 = left_y + Inches(2.55)

    # Cuadrante Reorientación (-X, +Y)
    q_re = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, qx1, qy1, sub_w, sub_h)
    q_re.fill.solid()
    q_re.fill.fore_color.rgb = RGBColor(254, 243, 199)
    q_re.line.color.rgb = RGBColor(245, 158, 11)
    q_re_tb = s2.shapes.add_textbox(qx1 + Inches(0.1), qy1 + Inches(0.1), sub_w - Inches(0.2), sub_h - Inches(0.2))
    q_re_p = q_re_tb.text_frame.paragraphs[0]
    q_re_p.text = "REORIENTACIÓN\n(Mini-Maxi • WO)\n\nX < 0 (Debilidades)\nY ≥ 0 (Oportunidades)" if lang=='ES' else "REORIENTATION\n(Mini-Maxi • WO)\n\nX < 0 (Weaknesses)\nY ≥ 0 (Opportunities)"
    q_re_p.font.size = Pt(9)
    q_re_p.font.bold = True
    q_re_p.font.color.rgb = RGBColor(146, 64, 14)
    q_re_p.alignment = PP_ALIGN.CENTER

    # Cuadrante Ofensivo (+X, +Y) -> RESALTADO ACTIVO
    q_of = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, qx2, qy1, sub_w, sub_h)
    q_of.fill.solid()
    q_of.fill.fore_color.rgb = RGBColor(209, 250, 229)
    q_of.line.color.rgb = RGBColor(16, 185, 129)
    q_of.line.width = Pt(2)
    q_of_tb = s2.shapes.add_textbox(qx2 + Inches(0.1), qy1 + Inches(0.1), sub_w - Inches(0.2), sub_h - Inches(0.2))
    q_of_p = q_of_tb.text_frame.paragraphs[0]
    q_of_p.text = "★ OFENSIVO (ACTIVO)\n(Maxi-Maxi • SO)\n\nX ≥ 0 (Fortalezas: +2.10)\nY ≥ 0 (Oportunidades: +1.85)" if lang=='ES' else "★ OFFENSIVE (ACTIVE)\n(Maxi-Maxi • SO)\n\nX ≥ 0 (Strengths: +2.10)\nY ≥ 0 (Opportunities: +1.85)"
    q_of_p.font.size = Pt(9)
    q_of_p.font.bold = True
    q_of_p.font.color.rgb = RGBColor(6, 95, 70)
    q_of_p.alignment = PP_ALIGN.CENTER

    # Cuadrante Supervivencia (-X, -Y)
    q_su = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, qx1, qy2, sub_w, sub_h)
    q_su.fill.solid()
    q_su.fill.fore_color.rgb = RGBColor(254, 226, 226)
    q_su.line.color.rgb = RGBColor(239, 68, 68)
    q_su_tb = s2.shapes.add_textbox(qx1 + Inches(0.1), qy2 + Inches(0.1), sub_w - Inches(0.2), sub_h - Inches(0.2))
    q_su_p = q_su_tb.text_frame.paragraphs[0]
    q_su_p.text = "SUPERVIVENCIA\n(Mini-Mini • WT)\n\nX < 0 (Debilidades)\nY < 0 (Amenazas)" if lang=='ES' else "SURVIVAL\n(Mini-Mini • WT)\n\nX < 0 (Weaknesses)\nY < 0 (Threats)"
    q_su_p.font.size = Pt(9)
    q_su_p.font.bold = True
    q_su_p.font.color.rgb = RGBColor(153, 27, 27)
    q_su_p.alignment = PP_ALIGN.CENTER

    # Cuadrante Defensivo (+X, -Y)
    q_de = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, qx2, qy2, sub_w, sub_h)
    q_de.fill.solid()
    q_de.fill.fore_color.rgb = RGBColor(219, 234, 254)
    q_de.line.color.rgb = RGBColor(59, 130, 246)
    q_de_tb = s2.shapes.add_textbox(qx2 + Inches(0.1), qy2 + Inches(0.1), sub_w - Inches(0.2), sub_h - Inches(0.2))
    q_de_p = q_de_tb.text_frame.paragraphs[0]
    q_de_p.text = "DEFENSIVO\n(Maxi-Mini • ST)\n\nX ≥ 0 (Fortalezas)\nY < 0 (Amenazas)" if lang=='ES' else "DEFENSIVE\n(Maxi-Mini • ST)\n\nX ≥ 0 (Strengths)\nY < 0 (Threats)"
    q_de_p.font.size = Pt(9)
    q_de_p.font.bold = True
    q_de_p.font.color.rgb = RGBColor(30, 64, 175)
    q_de_p.alignment = PP_ALIGN.CENTER

    # Indicador de Coordenadas bajo los cuadrantes
    coord_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x + Inches(0.3), left_y + Inches(4.35), left_w - Inches(0.6), Inches(0.42))
    coord_box.fill.solid()
    coord_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    coord_box.line.fill.background()
    c_tb = s2.shapes.add_textbox(left_x + Inches(0.3), left_y + Inches(4.35), left_w - Inches(0.6), Inches(0.42))
    c_p = c_tb.text_frame.paragraphs[0]
    c_p.text = "Coordenadas del Vector: (+2.10, +1.85) | Módulo ||V|| = 2.80 pts" if lang=='ES' else "Strategic Vector: (+2.10, +1.85) | Magnitude ||V|| = 2.80 pts"
    c_p.font.size = Pt(9)
    c_p.font.bold = True
    c_p.font.color.rgb = COLOR_WHITE
    c_p.alignment = PP_ALIGN.CENTER

    # Contenedor Derecho: Resumen de Fuerzas de Cruce
    right_x = Inches(6.6)
    right_y = Inches(1.85)
    right_w = Inches(5.933)
    right_h = Inches(4.9)

    r_blocks = [
        (texts['s2_box_so_title'], texts['s2_box_so_desc'], RGBColor(16, 185, 129), RGBColor(236, 253, 245), RGBColor(6, 95, 70)),
        (texts['s2_box_st_title'], texts['s2_box_st_desc'], RGBColor(59, 130, 246), RGBColor(239, 246, 255), RGBColor(30, 64, 175)),
        (texts['s2_box_wo_title'], texts['s2_box_wo_desc'], RGBColor(245, 158, 11), RGBColor(254, 243, 199), RGBColor(146, 64, 14)),
        (texts['s2_box_wt_title'], texts['s2_box_wt_desc'], RGBColor(239, 68, 68), RGBColor(254, 226, 226), RGBColor(153, 27, 27)),
    ]

    block_h = Inches(1.1)
    block_gap = Inches(0.15)

    for b_idx, (b_title, b_desc, b_border, b_bg, b_txt_col) in enumerate(r_blocks):
        by = right_y + b_idx * (block_h + block_gap)
        b_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, by, right_w, block_h)
        b_box.fill.solid()
        b_box.fill.fore_color.rgb = b_bg
        b_box.line.color.rgb = b_border
        b_box.line.width = Pt(1)

        b_tbox = s2.shapes.add_textbox(right_x + Inches(0.2), by + Inches(0.1), right_w - Inches(0.4), block_h - Inches(0.2))
        b_tf = b_tbox.text_frame
        b_tf.word_wrap = True

        bp0 = b_tf.paragraphs[0]
        bp0.text = b_title
        bp0.font.name = FONT_TITLE
        bp0.font.size = Pt(10.5)
        bp0.font.bold = True
        bp0.font.color.rgb = b_txt_col

        bp1 = b_tf.add_paragraph()
        bp1.text = b_desc
        bp1.font.name = FONT_BODY
        bp1.font.size = Pt(9.5)
        bp1.font.color.rgb = COLOR_TEXT_MAIN
        bp1.space_before = Pt(3)

    # ==========================================================================
    # SLIDE 3: PLAN DE ACCIÓN CAME & DECISIÓN REQUERIDA
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, texts['s3_action_title'], texts['s3_sub'], 3)

    # 4 Bloques Trimestrales (Roadmap)
    quarters = [
        (texts['s3_q1_title'], texts['s3_q1_text'], COLOR_BLUE_ACCENT),
        (texts['s3_q2_title'], texts['s3_q2_text'], COLOR_TEAL_ACCENT),
        (texts['s3_q3_title'], texts['s3_q3_text'], COLOR_AMBER),
        (texts['s3_q4_title'], texts['s3_q4_text'], COLOR_NAVY_DARK),
    ]

    q_w = Inches(2.78)
    q_gap = Inches(0.20)
    q_x = Inches(0.8)
    q_y = Inches(1.85)
    q_h = Inches(2.3)

    for q_idx, (q_t, q_body, q_col) in enumerate(quarters):
        qx = q_x + q_idx * (q_w + q_gap)

        q_shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx, q_y, q_w, q_h)
        q_shape.fill.solid()
        q_shape.fill.fore_color.rgb = COLOR_CARD_BG
        q_shape.line.color.rgb = COLOR_BORDER

        q_bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, qx, q_y, q_w, Inches(0.08))
        q_bar.fill.solid()
        q_bar.fill.fore_color.rgb = q_col
        q_bar.line.fill.background()

        q_tb = s3.shapes.add_textbox(qx + Inches(0.15), q_y + Inches(0.15), q_w - Inches(0.3), q_h - Inches(0.3))
        q_tf = q_tb.text_frame
        q_tf.word_wrap = True

        qp0 = q_tf.paragraphs[0]
        qp0.text = q_t
        qp0.font.name = FONT_TITLE
        qp0.font.size = Pt(10.5)
        qp0.font.bold = True
        qp0.font.color.rgb = q_col

        qp1 = q_tf.add_paragraph()
        qp1.text = q_body
        qp1.font.name = FONT_BODY
        qp1.font.size = Pt(9)
        qp1.font.color.rgb = COLOR_TEXT_MAIN
        qp1.space_before = Pt(6)

    # CAJA DESTACADA: DECISIÓN REQUERIDA DEL COMITÉ (BOARD DECISION GATEWAY)
    dec_y = Inches(4.35)
    dec_h = Inches(2.45)
    dec_w = Inches(11.733)

    dec_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), dec_y, dec_w, dec_h)
    dec_box.fill.solid()
    dec_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    dec_box.line.color.rgb = COLOR_AMBER
    dec_box.line.width = Pt(2)

    # Título Caja Decisión
    dec_tb = s3.shapes.add_textbox(Inches(1.0), dec_y + Inches(0.15), dec_w - Inches(0.4), dec_h - Inches(0.3))
    dec_tf = dec_tb.text_frame
    dec_tf.word_wrap = True

    dp0 = dec_tf.paragraphs[0]
    dp0.text = texts['s3_dec_header']
    dp0.font.name = FONT_TITLE
    dp0.font.size = Pt(11)
    dp0.font.bold = True
    dp0.font.color.rgb = RGBColor(254, 240, 138) # Gold accent

    items = [texts['s3_dec_1'], texts['s3_dec_2'], texts['s3_dec_3']]
    for it in items:
        dp = dec_tf.add_paragraph()
        dp.text = it
        dp.font.name = FONT_BODY
        dp.font.size = Pt(9.5)
        dp.font.color.rgb = COLOR_WHITE
        dp.space_before = Pt(7)

    os.makedirs(os.path.dirname(texts['out_path']), exist_ok=True)
    prs.save(texts['out_path'])
    print(f"[OK {lang}] Presentación guardada en: {texts['out_path']} ({os.path.getsize(texts['out_path'])} bytes)")


def main():
    create_deck('ES')
    create_deck('EN')


if __name__ == '__main__':
    main()
