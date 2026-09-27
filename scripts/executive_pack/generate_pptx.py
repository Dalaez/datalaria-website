#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx.py
================
Genera las presentaciones ejecutivas C-Level (16:9 widescreen) de alta dirección:
1. static/downloads/01_Espanol_DAFO_CAME/Presentacion_CLevel_DAFO_CAME_ES.pptx
2. static/downloads/02_English_SWOT_TOWS/Executive_CLevel_Deck_SWOT_TOWS_EN.pptx

Características de diseño:
- Sistema de color unificado por postura estratégica (Ofensiva = Azul, Defensiva = Teal, Reorientación = Ámbar, Supervivencia = Carmesí).
- Insignia de objetivo clara en cada diapositiva para identificar de inmediato su propósito ante el Consejo.
- Síntesis visual: métricas numéricas destacadas, píldoras de estado y viñetas ejecutivas concisas (sin bloques densos de texto).
- Caja de Decisión Requerida (Board Decision Gateway) estructurada en 3 resoluciones formales.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# SISTEMA DE COLOR ESTRATÉGICO UNIFICADO (TIER-1 CONSULTING PALETTE)
# ==============================================================================
# 1. OFENSIVA / SO / EXPLOTAR (Azul Corporativo)
COLOR_OFENSIVA_BLUE = RGBColor(37, 99, 235)      # #2563EB Blue 600
COLOR_OFENSIVA_BG = RGBColor(239, 246, 255)       # #EFF6FF Blue 50
COLOR_OFENSIVA_BORDER = RGBColor(147, 197, 253)   # #93C5FD Blue 300
COLOR_OFENSIVA_TEXT = RGBColor(29, 78, 216)       # #1D4ED8 Blue 700

# 2. DEFENSIVA / ST / MANTENER (Teal / Moat)
COLOR_DEFENSIVA_TEAL = RGBColor(13, 148, 136)     # #0D9488 Teal 600
COLOR_DEFENSIVA_BG = RGBColor(240, 253, 250)      # #F0FDFA Teal 50
COLOR_DEFENSIVA_BORDER = RGBColor(153, 246, 228)  # #99F6E4 Teal 200
COLOR_DEFENSIVA_TEXT = RGBColor(15, 118, 110)     # #0F766E Teal 700

# 3. REORIENTACIÓN / WO / CORREGIR (Ámbar Cálido)
COLOR_REORIENT_AMBER = RGBColor(217, 119, 6)      # #D97706 Amber 600
COLOR_REORIENT_BG = RGBColor(255, 251, 235)       # #FFFBEB Amber 50
COLOR_REORIENT_BORDER = RGBColor(253, 230, 138)   # #FDE68A Amber 200
COLOR_REORIENT_TEXT = RGBColor(146, 64, 14)       # #92400E Amber 800

# 4. SUPERVIVENCIA / WT / AFRONTAR (Carmesí / Riesgo)
COLOR_SURVIVAL_RED = RGBColor(225, 29, 72)        # #E11D48 Rose 600
COLOR_SURVIVAL_BG = RGBColor(255, 241, 242)       # #FFF1F2 Rose 50
COLOR_SURVIVAL_BORDER = RGBColor(254, 205, 211)   # #FECDD3 Rose 200
COLOR_SURVIVAL_TEXT = RGBColor(159, 18, 57)       # #9F1239 Rose 800

# Neutros Corporativos
COLOR_NAVY_DARK = RGBColor(15, 23, 42)            # #0F172A Slate 900
COLOR_NAVY_MED = RGBColor(30, 41, 59)             # #1E293B Slate 800
COLOR_TEXT_MAIN = RGBColor(51, 65, 85)            # #334155 Slate 700
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)        # #64748B Slate 500
COLOR_CARD_BG = RGBColor(248, 250, 252)           # #F8FAFC Slate 50
COLOR_BORDER = RGBColor(226, 232, 240)            # #E2E8F0 Slate 200
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_GOLD = RGBColor(245, 158, 11)               # #F59E0B Gold / Amber
COLOR_GOLD_LIGHT = RGBColor(254, 240, 138)        # #FEF08A Gold 100

FONT_TITLE = "Segoe UI"
FONT_BODY = "Segoe UI"


def create_deck(lang='ES'):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    texts = {
        'ES': {
            'out_path': "packages/01_Espanol_DAFO_CAME/Presentacion_CLevel_DAFO_CAME_ES.pptx",
            'header_standard': "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD",
            'footer_left': "Datalaria.com | Executive Decision Pack • Confidencial Consejo de Administración",
            'footer_right': "Página {cur} de 3",

            # ------------------------------------------------------------------
            # SLIDE 1: DIAGNÓSTICO ESTRATÉGICO & SÍNTESIS
            # ------------------------------------------------------------------
            's1_badge': "Diagnóstico Estratégico y Síntesis",
            's1_action_title': "Postura Ofensiva Validada: Margen (+18%) y Retención NRR (118%) Financian la Expansión",
            's1_sub': "Diagnóstico DAFO normalizado, ventajas competitivas clave y foco prioritario de mitigación.",
            
            # Card 1 (Ofensiva - Azul)
            's1_c1_tag': "OFENSIVA (DOMINANTE)",
            's1_c1_metric': "+2.10, +1.85",
            's1_c1_submetric': "Vector ||V|| = 2.80 pts (Impulso Alto)",
            's1_c1_bullets': [
                "Cuadrante I (Maxi-Maxi) dominante",
                "Solidez interna supera cuellos de botella",
                "Entorno macro con vientos de cola"
            ],
            's1_c1_pill': "POSTURA ACTIVA Q1",

            # Card 2 (Defensiva / Moat - Teal)
            's1_c2_tag': "VENTAJA DEFENDIBLE (MOAT)",
            's1_c2_metric': "24.2% EBITDA",
            's1_c2_submetric': "Margen Bruto +18.4% vs Sector",
            's1_c2_bullets': [
                "3 patentes europeas registradas",
                "Retención neta de ingresos (NRR) 118%",
                "Financiación orgánica de I+D sin deuda"
            ],
            's1_c2_pill': "FORTALEZA DE IP",

            # Card 3 (Riesgo / Vulnerabilidad - Ámbar)
            's1_c3_tag': "PUNTO DE ESTRÉS CRÍTICO",
            's1_c3_metric': "42% TOP-2",
            's1_c3_submetric': "Ciclo Enterprise: 8.5 Meses",
            's1_c3_bullets': [
                "Alta concentración en 2 clientes clave",
                "Presión de precios de competidores (-35%)",
                "Exige diversificación comercial en LatAm"
            ],
            's1_c3_pill': "MITIGACIÓN INMEDIATA",

            # Card 4 (Financiero / Retorno - Navy)
            's1_c4_tag': "ASIGNACIÓN DE CAPITAL",
            's1_c4_metric': "245k € → +1.2M €",
            's1_c4_submetric': "Payback: 11 Meses • VAN Positivo",
            's1_c4_bullets': [
                "Partida: 140k € CAPEX / 105k € OPEX",
                "Captura de 1.2M € de subvenciones y ARR",
                "Dilución de riesgo top-2 a < 25% ARR"
            ],
            's1_c4_pill': "DECISIÓN REQUERIDA",

            's1_takeaway_badge': "MANDATO DEL CONSEJO",
            's1_takeaway_text': "Autorizar 245.000 € para desplegar las 4 iniciativas CAME, capturando 1.2M € de ARR y blindando la concentración de clientes.",

            # ------------------------------------------------------------------
            # SLIDE 2: POSICIONAMIENTO CARTESIANO & FUERZAS DE CRUCE
            # ------------------------------------------------------------------
            's2_badge': "Posicionamiento y Fuerzas Estratégicas",
            's2_action_title': "68% del Potencial en Sinergias Ofensivas y Blindaje Inmediato ante Concentración de Clientes",
            's2_sub': "Espacio vectorial de cuadrantes y balance de fuerzas de cruce CAME.",
            's2_left_header': "ESPACIO VECTORIAL CARTESIANO",
            
            # Cuadrantes
            's2_q_re_title': "REORIENTACIÓN (WO)",
            's2_q_re_coord': "X < 0, Y ≥ 0",
            's2_q_re_desc': "Corregir debilidades internas para capturar oportunidades.",

            's2_q_of_title': "★ OFENSIVA (SO) • ACTIVO",
            's2_q_of_coord': "X = +2.10, Y = +1.85",
            's2_q_of_desc': "Máxima aceleración de capital sobre ventajas clave.",

            's2_q_su_title': "SUPERVIVENCIA (WT)",
            's2_q_su_coord': "X < 0, Y < 0",
            's2_q_su_desc': "Contención estricta y preservación de liquidez.",

            's2_q_de_title': "DEFENSIVA (ST)",
            's2_q_de_coord': "X ≥ 0, Y < 0",
            's2_q_de_desc': "Blindar margen y clientes con moats de patentes.",

            's2_vector_pill': "VECTOR ESTRATÉGICO: (+2.10, +1.85) | IMPULSO ||V|| = 2.80 PTS | ORIENTACIÓN θ = 41.3º",

            # Bloques derecha
            's2_b_so_title': "Sinergias Ofensivas (F-O / SO) • 38 pts",
            's2_b_so_pill': "68% POTENCIAL • FOCO 1",
            's2_b_so_bullets': [
                "Captura de subvenciones NextGen EU en 40 plantas industriales",
                "Alianzas de co-selling con integradores Tier-1 (Accenture/Indra)"
            ],

            's2_b_st_title': "Estrategias Defensivas (F-A / ST) • 26 pts",
            's2_b_st_pill': "BLINDAJE DE MOAT",
            's2_b_st_bullets': [
                "Blindaje de contratos plurianuales (3 años) con clientes clave",
                "Adecuación anticipada a normativas de ciberseguridad NIS2/DORA"
            ],

            's2_b_wo_title': "Iniciativas Reorientación (D-O / WO) • 18 pts",
            's2_b_wo_pill': "TURNAROUND OPERATIVO",
            's2_b_wo_bullets': [
                "Despliegue de red de distribución comercial en México y Colombia",
                "Refactorización del billing multi-divisa (lead time reducido a 5 meses)"
            ],

            's2_b_wt_title': "Vulnerabilidades Supervivencia (D-A / WT) • 29 pts",
            's2_b_wt_pill': "RIESGO CRÍTICO",
            's2_b_wt_bullets': [
                "Riesgo de concentración de clientes (42%) frente a guerras de precios",
                "Mandato de diversificación antes de concluir el ejercicio Q3"
            ],

            # ------------------------------------------------------------------
            # SLIDE 3: PLAN DE ACCIÓN CAME & DECISIÓN REQUERIDA
            # ------------------------------------------------------------------
            's3_badge': "Plan de Acción CAME y Decisión del Consejo",
            's3_action_title': "Despliegue CAME 2026: 245.000 € de Presupuesto para Capturar 1.2M € de Nuevo ARR",
            's3_sub': "Hoja de ruta trimestral, responsables C-Level y resoluciones vinculantes del Consejo.",
            
            # 4 Trimestres
            's3_q1_title': "Q1 • BLINDAJE & NIS2",
            's3_q1_pillar': "DEFENSIVA (ST)",
            's3_q1_bullets': [
                "CAME-A01: Contratos enterprise [CEO]",
                "CAME-A02: Auditoría NIS2 / DORA [CISO]"
            ],
            's3_q1_budget': "45.000 €",

            's3_q2_title': "Q2 • CANAL LATAM & ALIANZAS",
            's3_q2_pillar': "REORIENTACIÓN (WO)",
            's3_q2_bullets': [
                "CAME-C01: Red comercial LatAm [CCO]",
                "CAME-C02: Acuerdo integradores [VP Sales]"
            ],
            's3_q2_budget': "80.000 €",

            's3_q3_title': "Q3 • ESCALA SAAS INDUSTRIAL",
            's3_q3_pillar': "OFENSIVA (SO)",
            's3_q3_bullets': [
                "CAME-E01: Módulo SaaS 40 factorías [COO]",
                "CAME-C03: Refactorización billing [CTO]"
            ],
            's3_q3_budget': "90.000 €",

            's3_q4_title': "Q4 • RETENCIÓN I+D & MOAT",
            's3_q4_pillar': "PRESERVACIÓN DE MOAT",
            's3_q4_bullets': [
                "CAME-M01: Ampliación patentes Asia [Legal]",
                "CAME-M02: LTIP phantom shares IA [CPO]"
            ],
            's3_q4_budget': "30.000 €",

            # Gateway
            's3_gw_header': "DECISIÓN REQUERIDA DEL CONSEJO (BOARD GATEWAY)",
            's3_gw_sub': "Tres acuerdos vinculantes para la ejecución del plan estratégico y liberación de fondos:",
            
            's3_gw_d1_title': "1. APROBACIÓN DE CAPITAL",
            's3_gw_d1_val': "245.000 €",
            's3_gw_d1_desc': "Autorizar 140k € CAPEX / 105k € OPEX con cargo al fondo de inversión estratégica.",

            's3_gw_d2_title': "2. SPONSORSHIP C-LEVEL",
            's3_gw_d2_val': "COO & CCO",
            's3_gw_d2_desc': "Ratificar al COO como Sponsor de CAME-E01 y al CCO para la Diversificación LatAm.",

            's3_gw_d3_title': "3. GOBERNANZA & REPORTING",
            's3_gw_d3_val': "Revisión Trimestral",
            's3_gw_d3_desc': "Comité mensual de seguimiento y auditoría de KPIs de ARR en cada Consejo ordinario.",
        },
        'EN': {
            'out_path': "packages/02_English_SWOT_TOWS/Executive_CLevel_Deck_SWOT_TOWS_EN.pptx",
            'header_standard': "DATALARIA STRATEGY PRACTICE • MCKINSEY/BCG STANDARD",
            'footer_left': "Datalaria.com | Executive Decision Pack • Strictly Confidential for Board of Directors",
            'footer_right': "Slide {cur} of 3",

            # ------------------------------------------------------------------
            # SLIDE 1: STRATEGIC DIAGNOSIS & EXECUTIVE SYNTHESIS
            # ------------------------------------------------------------------
            's1_badge': "Strategic Diagnosis & Synthesis",
            's1_action_title': "Offensive Posture Validated: Margin (+18%) and NRR (118%) Fund Market Scaling",
            's1_sub': "Normalized SWOT diagnosis, key defensible moats, and critical mitigation priorities.",
            
            # Card 1 (Offensive - Blue)
            's1_c1_tag': "OFFENSIVE (DOMINANT)",
            's1_c1_metric': "+2.10, +1.85",
            's1_c1_submetric': "Momentum Vector ||V|| = 2.80 pts (High)",
            's1_c1_bullets': [
                "Dominant Quadrant I (Maxi-Maxi)",
                "Internal moat exceeds operational debt",
                "Strong macroeconomic expansion tailwinds"
            ],
            's1_c1_pill': "ACTIVE POSTURE Q1",

            # Card 2 (Defensive / Moat - Teal)
            's1_c2_tag': "DEFENSIBLE MOAT (ST)",
            's1_c2_metric': "24.2% EBITDA",
            's1_c2_submetric': "Gross Margin +18.4% vs Peers",
            's1_c2_bullets': [
                "3 granted European patents",
                "Net Revenue Retention (NRR) at 118%",
                "Self-funded R&D scaling without debt"
            ],
            's1_c2_pill': "IP ASSET MOAT",

            # Card 3 (Risk / Vulnerability - Amber)
            's1_c3_tag': "CRITICAL STRESS POINT",
            's1_c3_metric': "42% TOP-2",
            's1_c3_submetric': "Sales Deal Cycle: 8.5 Months",
            's1_c3_bullets': [
                "Severe revenue concentration in 2 logos",
                "Asian competitor price discounting (-35%)",
                "Demands immediate LatAm channel hedge"
            ],
            's1_c3_pill': "URGENT MITIGATION",

            # Card 4 (Financial / ROI - Navy)
            's1_c4_tag': "CAPITAL & ROI",
            's1_c4_metric': "€245k → +€1.2M",
            's1_c4_submetric': "Payback: 11 Months • Positive NPV",
            's1_c4_bullets': [
                "Allocation: €140k CAPEX / €105k OPEX",
                "Capture of €1.2M NextGen ARR",
                "Dilute Top-2 exposure down to < 25% ARR"
            ],
            's1_c4_pill': "BOARD GATEWAY",

            's1_takeaway_badge': "BOARDROOM MANDATE",
            's1_takeaway_text': "Authorize €245,000 to deploy the 4 TOWS initiatives, securing €1.2M ARR while neutralizing client concentration.",

            # ------------------------------------------------------------------
            # SLIDE 2: CARTESIAN POSITIONING & CROSS-IMPACT FORCES
            # ------------------------------------------------------------------
            's2_badge': "Strategic Positioning & Cross-Forces",
            's2_action_title': "68% of Synergies in Offensive Space with Urgent Customer Concentration Hedging",
            's2_sub': "Cartesian quadrant matrix and TOWS cross-impact force intensity map.",
            's2_left_header': "CARTESIAN STRATEGIC SPACE",
            
            # Quadrants
            's2_q_re_title': "REORIENTATION (WO)",
            's2_q_re_coord': "X < 0, Y ≥ 0",
            's2_q_re_desc': "Turn around internal bottlenecks to capture market tailwinds.",

            's2_q_of_title': "★ OFFENSIVE (SO) • ACTIVE",
            's2_q_of_coord': "X = +2.10, Y = +1.85",
            's2_q_of_desc': "Direct aggressive capital to exploit proprietary moats.",

            's2_q_su_title': "SURVIVAL (WT)",
            's2_q_su_coord': "X < 0, Y < 0",
            's2_q_su_desc': "Enforce strict cash preservation and defensive hedging.",

            's2_q_de_title': "DEFENSIVE (ST)",
            's2_q_de_coord': "X ≥ 0, Y < 0",
            's2_q_de_desc': "Hedge external risks leveraging margins and IP.",

            's2_vector_pill': "STRATEGIC VECTOR: (+2.10, +1.85) | MOMENTUM ||V|| = 2.80 PTS | ANGLE θ = 41.3º",

            # Bloques derecha
            's2_b_so_title': "Offensive Synergies (S-O) • 38 pts",
            's2_b_so_pill': "68% POTENTIAL • PRIORITY 1",
            's2_b_so_bullets': [
                "Accelerated smart factory SaaS rollout across 40 plants",
                "Tier-1 system integrator co-selling agreements (Accenture/Indra)"
            ],

            's2_b_st_title': "Defensive Moats (S-T) • 26 pts",
            's2_b_st_pill': "MOAT PRESERVATION",
            's2_b_st_bullets': [
                "3-year multi-year master service agreement lock-ins with enterprise logos",
                "Proactive regulatory compliance certification for NIS2 and DORA"
            ],

            's2_b_wo_title': "Turnaround Initiatives (W-O) • 18 pts",
            's2_b_wo_pill': "OPERATIONAL TURNAROUND",
            's2_b_wo_bullets': [
                "Establish LatAm master distributor partnerships in Mexico and Colombia",
                "Refactor multi-currency billing engine to compress deal cycle to 5 months"
            ],

            's2_b_wt_title': "Survival Vulnerabilities (W-T) • 29 pts",
            's2_b_wt_pill': "CRITICAL RISK",
            's2_b_wt_bullets': [
                "Top-2 logo concentration risk (42%) exposed to Asian discount pricing",
                "Mandatory account diversification milestone enforced before end of Q3"
            ],

            # ------------------------------------------------------------------
            # SLIDE 3: TOWS CAPITAL ROADMAP & BOARD DECISION GATEWAY
            # ------------------------------------------------------------------
            's3_badge': "TOWS Action Plan & Board Decision",
            's3_action_title': "2026 TOWS Deployment: €245k Capital Allocation to Capture €1.2M New ARR",
            's3_sub': "Quarterly execution roadmap, C-Level owners, and binding Boardroom resolutions.",
            
            # 4 Quarters
            's3_q1_title': "Q1 • CYBER MOAT & LOCK-IN",
            's3_q1_pillar': "DEFENSIVE (ST)",
            's3_q1_bullets': [
                "TOWS-T01: Enterprise logo lock-in [CEO]",
                "TOWS-T02: NIS2 / DORA compliance [CISO]"
            ],
            's3_q1_budget': "€45,000",

            's3_q2_title': "Q2 • LATAM CHANNEL & PARTNERS",
            's3_q2_pillar': "REORIENTATION (WO)",
            's3_q2_bullets': [
                "TOWS-W01: LatAm master distributor [CCO]",
                "TOWS-W02: SI co-selling framework [VP Sales]"
            ],
            's3_q2_budget': "€80,000",

            's3_q3_title': "Q3 • INDUSTRIAL SAAS SCALING",
            's3_q3_pillar': "OFFENSIVE (SO)",
            's3_q3_bullets': [
                "TOWS-O01: 40 smart factories rollout [COO]",
                "TOWS-C03: Billing microservice refactor [CTO]"
            ],
            's3_q3_budget': "€90,000",

            's3_q4_title': "Q4 • R&D TALENT & PATENTS",
            's3_q4_pillar': "MOAT PRESERVATION",
            's3_q4_bullets': [
                "TOWS-M01: Supplemental patent filing [Legal]",
                "TOWS-M02: Senior AI engineer LTIP [CPO]"
            ],
            's3_q4_budget': "€30,000",

            # Gateway
            's3_gw_header': "BOARD DECISION GATEWAY (REQUIRED RESOLUTIONS)",
            's3_gw_sub': "Three binding resolutions submitted for formal Board adoption:",
            
            's3_gw_d1_title': "1. CAPITAL APPROPRIATION",
            's3_gw_d1_val': "€245,000",
            's3_gw_d1_desc': "Authorize €140k CAPEX / €105k OPEX allocation from strategic corporate investment reserve.",

            's3_gw_d2_title': "2. C-LEVEL SPONSORSHIP",
            's3_gw_d2_val': "COO & CCO",
            's3_gw_d2_desc': "Ratify COO as Executive Sponsor for TOWS-O01 and CCO for Commercial LatAm Expansion.",

            's3_gw_d3_title': "3. GOVERNANCE & AUDIT",
            's3_gw_d3_val': "Quarterly Review",
            's3_gw_d3_desc': "Enforce monthly steering reviews and quarterly Board milestone audits on ARR impact."
        }
    }[lang]

    # ==========================================================================
    # HELPER DE CABECERA Y FOOTER
    # ==========================================================================
    def add_slide_header(slide, badge_text, action_title, sub_text, cur_slide):
        # 1. Slide Objective Badge (Píldora destacada de propósito)
        badge_w = min(Inches(4.5), max(Inches(3.2), Inches(len(badge_text) * 0.085 + 0.4)))
        badge_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), badge_w, Inches(0.28))
        badge_box.adjustments[0] = 0.25
        badge_box.fill.solid()
        badge_box.fill.fore_color.rgb = COLOR_NAVY_DARK
        badge_box.line.fill.background()
        
        b_tf = badge_box.text_frame
        b_tf.word_wrap = False
        b_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        b_tf.margin_left = Inches(0.12)
        b_tf.margin_right = Inches(0.12)
        b_tf.margin_top = Inches(0.01)
        b_tf.margin_bottom = Inches(0.01)
        bp = b_tf.paragraphs[0]
        bp.text = badge_text
        bp.font.name = FONT_TITLE
        bp.font.size = Pt(8.5)
        bp.font.bold = True
        bp.font.color.rgb = COLOR_GOLD_LIGHT
        bp.alignment = PP_ALIGN.CENTER

        # 2. Standard Kicker (Derecha)
        meta_box = slide.shapes.add_textbox(Inches(6.5), Inches(0.34), Inches(6.033), Inches(0.28))
        m_tf = meta_box.text_frame
        mp = m_tf.paragraphs[0]
        mp.alignment = PP_ALIGN.RIGHT
        mp.text = texts['header_standard']
        mp.font.name = FONT_TITLE
        mp.font.size = Pt(8)
        mp.font.bold = True
        mp.font.color.rgb = COLOR_TEXT_MUTED

        # 3. Action Title (Título ejecutivo de Minto)
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = action_title
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(16.5)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY_DARK

        # 4. Subtitle / Contexto
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.30))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = sub_text
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(9.5)
        p_s.font.color.rgb = COLOR_TEXT_MUTED

        # 5. Footer divider & text
        divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.98), Inches(11.733), Inches(0.015))
        divider.fill.solid()
        divider.fill.fore_color.rgb = COLOR_BORDER
        divider.line.fill.background()

        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.04), Inches(8.5), Inches(0.3))
        p_f = f_box.text_frame.paragraphs[0]
        p_f.text = texts['footer_left']
        p_f.font.name = FONT_BODY
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = COLOR_TEXT_MUTED

        p_box = slide.shapes.add_textbox(Inches(10.5), Inches(7.04), Inches(2.033), Inches(0.3))
        p_p = p_box.text_frame.paragraphs[0]
        p_p.alignment = PP_ALIGN.RIGHT
        p_p.text = texts['footer_right'].format(cur=cur_slide)
        p_p.font.name = FONT_BODY
        p_p.font.size = Pt(8.5)
        p_p.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================================================
    # SLIDE 1: DIAGNÓSTICO ESTRATÉGICO & SÍNTESIS EJECUTIVA
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_header(s1, texts['s1_badge'], texts['s1_action_title'], texts['s1_sub'], 1)

    # 4 Tarjetas de Diagnóstico Numérico (Colores Estratégicos Alineados)
    cards_data = [
        (
            texts['s1_c1_tag'], texts['s1_c1_metric'], texts['s1_c1_submetric'],
            texts['s1_c1_bullets'], texts['s1_c1_pill'],
            COLOR_OFENSIVA_BLUE, COLOR_OFENSIVA_BG, COLOR_OFENSIVA_BORDER, COLOR_OFENSIVA_TEXT
        ),
        (
            texts['s1_c2_tag'], texts['s1_c2_metric'], texts['s1_c2_submetric'],
            texts['s1_c2_bullets'], texts['s1_c2_pill'],
            COLOR_DEFENSIVA_TEAL, COLOR_DEFENSIVA_BG, COLOR_DEFENSIVA_BORDER, COLOR_DEFENSIVA_TEXT
        ),
        (
            texts['s1_c3_tag'], texts['s1_c3_metric'], texts['s1_c3_submetric'],
            texts['s1_c3_bullets'], texts['s1_c3_pill'],
            COLOR_REORIENT_AMBER, COLOR_REORIENT_BG, COLOR_REORIENT_BORDER, COLOR_REORIENT_TEXT
        ),
        (
            texts['s1_c4_tag'], texts['s1_c4_metric'], texts['s1_c4_submetric'],
            texts['s1_c4_bullets'], texts['s1_c4_pill'],
            COLOR_NAVY_DARK, RGBColor(241, 245, 249), COLOR_BORDER, COLOR_NAVY_DARK
        ),
    ]

    card_w = Inches(2.78)
    card_gap = Inches(0.20)
    card_x = Inches(0.8)
    card_y = Inches(1.80)
    card_h = Inches(4.25)

    for idx, (tag, metric, submetric, bullets, pill, color_accent, color_bg, color_border, color_text) in enumerate(cards_data):
        cx = card_x + idx * (card_w + card_gap)

        # Contenedor Tarjeta con esquinas sutiles ejecutivas y contorno cromático temático
        shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        shape.adjustments[0] = 0.05
        shape.fill.solid()
        shape.fill.fore_color.rgb = color_bg
        shape.line.color.rgb = color_accent
        shape.line.width = Pt(1.5)

        # Marco de texto superior: Tag, Métrica, Submétrica
        tb_head = s1.shapes.add_textbox(cx + Inches(0.18), card_y + Inches(0.14), card_w - Inches(0.36), Inches(1.22))
        tf_h = tb_head.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = tf_h.margin_bottom = 0

        # Tag de Categoría
        p_tag = tf_h.paragraphs[0]
        p_tag.text = tag
        p_tag.font.name = FONT_TITLE
        p_tag.font.size = Pt(8)
        p_tag.font.bold = True
        p_tag.font.color.rgb = color_accent

        # Métrica Principal (Impacto visual alto, tamaño calibrado para no partir en 2 líneas)
        p_met = tf_h.add_paragraph()
        p_met.text = metric
        p_met.font.name = FONT_TITLE
        p_met.font.size = Pt(16.5) if len(metric) > 12 else Pt(19)
        p_met.font.bold = True
        p_met.font.color.rgb = COLOR_NAVY_DARK
        p_met.space_before = Pt(3)
        p_met.space_after = Pt(2)

        # Submétrica explicativa
        p_sub = tf_h.add_paragraph()
        p_sub.text = submetric
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(8.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = color_text

        # Separador interno sutil (físicamente separado entre cabecera y viñetas sin solapar texto)
        line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx + Inches(0.18), card_y + Inches(1.42), card_w - Inches(0.36), Inches(0.012))
        line.fill.solid()
        line.fill.fore_color.rgb = color_border
        line.line.fill.background()

        # Marco de texto de viñetas (empieza estrictamente debajo del separador, 0% riesgo de colisión)
        tb_bullets = s1.shapes.add_textbox(cx + Inches(0.18), card_y + Inches(1.50), card_w - Inches(0.36), Inches(2.15))
        tf_b = tb_bullets.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for b_idx, b_text in enumerate(bullets):
            pb = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            pb.text = f"•  {b_text}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(8.5)
            pb.font.color.rgb = COLOR_TEXT_MAIN
            if b_idx > 0:
                pb.space_before = Pt(4)

        # Píldora inferior de estado
        pill_y = card_y + card_h - Inches(0.48)
        p_shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.18), pill_y, card_w - Inches(0.36), Inches(0.30))
        p_shape.adjustments[0] = 0.25
        p_shape.fill.solid()
        p_shape.fill.fore_color.rgb = color_accent
        p_shape.line.fill.background()

        ptb = s1.shapes.add_textbox(cx + Inches(0.18), pill_y, card_w - Inches(0.36), Inches(0.30))
        ptb_tf = ptb.text_frame
        ptb_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        ptb_tf.margin_left = ptb_tf.margin_right = ptb_tf.margin_top = ptb_tf.margin_bottom = 0
        pp = ptb_tf.paragraphs[0]
        pp.text = pill
        pp.font.name = FONT_TITLE
        pp.font.size = Pt(8)
        pp.font.bold = True
        pp.font.color.rgb = COLOR_WHITE
        pp.alignment = PP_ALIGN.CENTER

    # Barra Inferior: Conclusión Vinculante para Consejo
    bot_y = Inches(6.20)
    bot_w = Inches(11.733)
    bot_h = Inches(0.55)

    bot_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), bot_y, bot_w, bot_h)
    bot_box.adjustments[0] = 0.10
    bot_box.fill.solid()
    bot_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    bot_box.line.color.rgb = COLOR_OFENSIVA_BLUE
    bot_box.line.width = Pt(1.5)

    # Insignia de mandato en la barra inferior
    m_pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), bot_y + Inches(0.11), Inches(1.8), Inches(0.33))
    m_pill.adjustments[0] = 0.25
    m_pill.fill.solid()
    m_pill.fill.fore_color.rgb = COLOR_OFENSIVA_BLUE
    m_pill.line.fill.background()
    mp_tb = s1.shapes.add_textbox(Inches(0.95), bot_y + Inches(0.11), Inches(1.8), Inches(0.33))
    mp_tf = mp_tb.text_frame
    mp_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    mp_tf.margin_left = mp_tf.margin_right = mp_tf.margin_top = mp_tf.margin_bottom = 0
    mpp = mp_tf.paragraphs[0]
    mpp.text = texts['s1_takeaway_badge']
    mpp.font.name = FONT_TITLE
    mpp.font.size = Pt(8)
    mpp.font.bold = True
    mpp.font.color.rgb = COLOR_WHITE
    mpp.alignment = PP_ALIGN.CENTER

    # Texto de conclusión del Consejo
    bt_box = s1.shapes.add_textbox(Inches(2.88), bot_y + Inches(0.10), Inches(9.5), Inches(0.35))
    bt_tf = bt_box.text_frame
    bt_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    bt_tf.margin_left = bt_tf.margin_right = bt_tf.margin_top = bt_tf.margin_bottom = 0
    bp = bt_tf.paragraphs[0]
    bp.text = texts['s1_takeaway_text']
    bp.font.name = FONT_BODY
    bp.font.size = Pt(9)
    bp.font.bold = True
    bp.font.color.rgb = COLOR_WHITE

    # ==========================================================================
    # SLIDE 2: POSICIONAMIENTO CARTESIANO & MAPA DE FUERZAS DE CRUCE
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, texts['s2_badge'], texts['s2_action_title'], texts['s2_sub'], 2)

    # CONTENEDOR IZQUIERDO: MATRIZ CARTESIANA (4 Cuadrantes con Colores Alineados)
    left_x = Inches(0.8)
    left_y = Inches(1.80)
    left_w = Inches(5.60)
    left_h = Inches(4.00)

    l_bg = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, left_y, left_w, left_h)
    l_bg.adjustments[0] = 0.035
    l_bg.fill.solid()
    l_bg.fill.fore_color.rgb = COLOR_CARD_BG
    l_bg.line.color.rgb = COLOR_BORDER
    l_bg.line.width = Pt(1)

    # Cabecera contenedor izquierdo
    l_head = s2.shapes.add_textbox(left_x + Inches(0.24), left_y + Inches(0.12), left_w - Inches(0.48), Inches(0.30))
    lhp = l_head.text_frame.paragraphs[0]
    lhp.text = texts['s2_left_header']
    lhp.font.name = FONT_TITLE
    lhp.font.size = Pt(9.5)
    lhp.font.bold = True
    lhp.font.color.rgb = COLOR_NAVY_DARK

    sub_w = Inches(2.46)
    sub_h = Inches(1.58)
    qx1 = left_x + Inches(0.24)
    qx2 = left_x + Inches(2.90)
    qy1 = left_y + Inches(0.48)
    qy2 = left_y + Inches(2.20)

    # 1. Cuadrante Reorientación (-X, +Y) -> ÁMBAR
    q_re = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx1, qy1, sub_w, sub_h)
    q_re.adjustments[0] = 0.05
    q_re.fill.solid()
    q_re.fill.fore_color.rgb = COLOR_REORIENT_BG
    q_re.line.color.rgb = COLOR_REORIENT_BORDER
    q_re.line.width = Pt(1.5)
    
    q_re_tb = s2.shapes.add_textbox(qx1 + Inches(0.12), qy1 + Inches(0.12), sub_w - Inches(0.24), sub_h - Inches(0.24))
    tf_re = q_re_tb.text_frame
    tf_re.word_wrap = True
    tf_re.margin_left = tf_re.margin_right = tf_re.margin_top = tf_re.margin_bottom = 0
    p0 = tf_re.paragraphs[0]
    p0.text = texts['s2_q_re_title']
    p0.font.name = FONT_TITLE
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_REORIENT_TEXT
    p0.alignment = PP_ALIGN.CENTER
    p1 = tf_re.add_paragraph()
    p1.text = texts['s2_q_re_coord']
    p1.font.name = FONT_BODY
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MUTED
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(3)
    p2 = tf_re.add_paragraph()
    p2.text = texts['s2_q_re_desc']
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8)
    p2.font.color.rgb = COLOR_TEXT_MAIN
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(5)

    # 2. Cuadrante Ofensivo (+X, +Y) -> AZUL (POSICIÓN ACTIVA DESTACADA)
    q_of = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx2, qy1, sub_w, sub_h)
    q_of.adjustments[0] = 0.05
    q_of.fill.solid()
    q_of.fill.fore_color.rgb = COLOR_OFENSIVA_BG
    q_of.line.color.rgb = COLOR_OFENSIVA_BLUE
    q_of.line.width = Pt(2.5)

    q_of_tb = s2.shapes.add_textbox(qx2 + Inches(0.12), qy1 + Inches(0.12), sub_w - Inches(0.24), sub_h - Inches(0.24))
    tf_of = q_of_tb.text_frame
    tf_of.word_wrap = True
    tf_of.margin_left = tf_of.margin_right = tf_of.margin_top = tf_of.margin_bottom = 0
    p0 = tf_of.paragraphs[0]
    p0.text = texts['s2_q_of_title']
    p0.font.name = FONT_TITLE
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_OFENSIVA_TEXT
    p0.alignment = PP_ALIGN.CENTER
    p1 = tf_of.add_paragraph()
    p1.text = texts['s2_q_of_coord']
    p1.font.name = FONT_BODY
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_OFENSIVA_BLUE
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(3)
    p2 = tf_of.add_paragraph()
    p2.text = texts['s2_q_of_desc']
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8)
    p2.font.color.rgb = COLOR_TEXT_MAIN
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(5)

    # 3. Cuadrante Supervivencia (-X, -Y) -> CARMESÍ / ROJO
    q_su = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx1, qy2, sub_w, sub_h)
    q_su.adjustments[0] = 0.05
    q_su.fill.solid()
    q_su.fill.fore_color.rgb = COLOR_SURVIVAL_BG
    q_su.line.color.rgb = COLOR_SURVIVAL_BORDER
    q_su.line.width = Pt(1.5)

    q_su_tb = s2.shapes.add_textbox(qx1 + Inches(0.12), qy2 + Inches(0.12), sub_w - Inches(0.24), sub_h - Inches(0.24))
    tf_su = q_su_tb.text_frame
    tf_su.word_wrap = True
    tf_su.margin_left = tf_su.margin_right = tf_su.margin_top = tf_su.margin_bottom = 0
    p0 = tf_su.paragraphs[0]
    p0.text = texts['s2_q_su_title']
    p0.font.name = FONT_TITLE
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_SURVIVAL_TEXT
    p0.alignment = PP_ALIGN.CENTER
    p1 = tf_su.add_paragraph()
    p1.text = texts['s2_q_su_coord']
    p1.font.name = FONT_BODY
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MUTED
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(3)
    p2 = tf_su.add_paragraph()
    p2.text = texts['s2_q_su_desc']
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8)
    p2.font.color.rgb = COLOR_TEXT_MAIN
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(5)

    # 4. Cuadrante Defensivo (+X, -Y) -> TEAL
    q_de = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx2, qy2, sub_w, sub_h)
    q_de.adjustments[0] = 0.05
    q_de.fill.solid()
    q_de.fill.fore_color.rgb = COLOR_DEFENSIVA_BG
    q_de.line.color.rgb = COLOR_DEFENSIVA_BORDER
    q_de.line.width = Pt(1.5)

    q_de_tb = s2.shapes.add_textbox(qx2 + Inches(0.12), qy2 + Inches(0.12), sub_w - Inches(0.24), sub_h - Inches(0.24))
    tf_de = q_de_tb.text_frame
    tf_de.word_wrap = True
    tf_de.margin_left = tf_de.margin_right = tf_de.margin_top = tf_de.margin_bottom = 0
    p0 = tf_de.paragraphs[0]
    p0.text = texts['s2_q_de_title']
    p0.font.name = FONT_TITLE
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_DEFENSIVA_TEXT
    p0.alignment = PP_ALIGN.CENTER
    p1 = tf_de.add_paragraph()
    p1.text = texts['s2_q_de_coord']
    p1.font.name = FONT_BODY
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MUTED
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(3)
    p2 = tf_de.add_paragraph()
    p2.text = texts['s2_q_de_desc']
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8)
    p2.font.color.rgb = COLOR_TEXT_MAIN
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(5)

    # Píldora / Banner de Vector de Posicionamiento (Ubicado de forma independiente debajo del contenedor)
    v_y = left_y + Inches(4.14)
    v_h = Inches(0.56)
    v_w = left_w
    v_x = left_x
    v_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, v_x, v_y, v_w, v_h)
    v_box.adjustments[0] = 0.08
    v_box.fill.solid()
    v_box.fill.fore_color.rgb = COLOR_NAVY_DARK
    v_box.line.color.rgb = COLOR_OFENSIVA_BLUE
    v_box.line.width = Pt(1.5)

    v_tb = s2.shapes.add_textbox(v_x, v_y, v_w, v_h)
    v_tf = v_tb.text_frame
    v_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    v_tf.margin_left = v_tf.margin_right = v_tf.margin_top = v_tf.margin_bottom = 0
    vp = v_tf.paragraphs[0]
    vp.text = texts['s2_vector_pill']
    vp.font.name = FONT_TITLE
    vp.font.size = Pt(8.5)
    vp.font.bold = True
    vp.font.color.rgb = COLOR_GOLD_LIGHT
    vp.alignment = PP_ALIGN.CENTER

    # CONTENEDOR DERECHO: MAPA DE FUERZAS DE CRUCE (Alineación cromática estricta)
    right_x = Inches(6.63)
    right_y = Inches(1.80)
    right_w = Inches(5.90)
    right_h = Inches(4.70)

    r_cards = [
        # 1. Ofensiva (F-O / SO) -> AZUL
        (
            texts['s2_b_so_title'], texts['s2_b_so_pill'], texts['s2_b_so_bullets'],
            COLOR_OFENSIVA_BLUE, COLOR_OFENSIVA_BG, COLOR_OFENSIVA_BORDER, COLOR_OFENSIVA_TEXT
        ),
        # 2. Defensiva (F-A / ST) -> TEAL
        (
            texts['s2_b_st_title'], texts['s2_b_st_pill'], texts['s2_b_st_bullets'],
            COLOR_DEFENSIVA_TEAL, COLOR_DEFENSIVA_BG, COLOR_DEFENSIVA_BORDER, COLOR_DEFENSIVA_TEXT
        ),
        # 3. Reorientación (D-O / WO) -> ÁMBAR
        (
            texts['s2_b_wo_title'], texts['s2_b_wo_pill'], texts['s2_b_wo_bullets'],
            COLOR_REORIENT_AMBER, COLOR_REORIENT_BG, COLOR_REORIENT_BORDER, COLOR_REORIENT_TEXT
        ),
        # 4. Supervivencia (D-A / WT) -> CARMESÍ
        (
            texts['s2_b_wt_title'], texts['s2_b_wt_pill'], texts['s2_b_wt_bullets'],
            COLOR_SURVIVAL_RED, COLOR_SURVIVAL_BG, COLOR_SURVIVAL_BORDER, COLOR_SURVIVAL_TEXT
        ),
    ]

    b_h = Inches(1.10)
    b_gap = Inches(0.10)

    for b_i, (b_title, b_pill, b_bullets, b_acc, b_bg, b_bord, b_txt) in enumerate(r_cards):
        by = right_y + b_i * (b_h + b_gap)

        # Caja
        b_shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, by, right_w, b_h)
        b_shape.adjustments[0] = 0.05
        b_shape.fill.solid()
        b_shape.fill.fore_color.rgb = b_bg
        b_shape.line.color.rgb = b_acc
        b_shape.line.width = Pt(1.5)

        # Texto interior
        b_tb = s2.shapes.add_textbox(right_x + Inches(0.20), by + Inches(0.08), right_w - Inches(0.40), b_h - Inches(0.16))
        btf = b_tb.text_frame
        btf.word_wrap = True
        btf.margin_left = btf.margin_right = btf.margin_top = btf.margin_bottom = 0

        # Fila 1: Título y Píldora
        bp0 = btf.paragraphs[0]
        bp0.text = f"{b_title}   [{b_pill}]"
        bp0.font.name = FONT_TITLE
        bp0.font.size = Pt(9.5)
        bp0.font.bold = True
        bp0.font.color.rgb = b_txt

        # Viñetas concisas
        for bullet in b_bullets:
            bp_b = btf.add_paragraph()
            bp_b.text = f"•  {bullet}"
            bp_b.font.name = FONT_BODY
            bp_b.font.size = Pt(8.5)
            bp_b.font.color.rgb = COLOR_TEXT_MAIN
            bp_b.space_before = Pt(2.5)

    # ==========================================================================
    # SLIDE 3: PLAN DE ACCIÓN CAME & DECISIÓN REQUERIDA
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, texts['s3_badge'], texts['s3_action_title'], texts['s3_sub'], 3)

    # 4 TRIMESTRES CAME (Colores Alineados por Tipo Estratégico)
    quarters_data = [
        # Q1: Defensiva (ST) -> TEAL
        (
            texts['s3_q1_title'], texts['s3_q1_pillar'], texts['s3_q1_bullets'], texts['s3_q1_budget'],
            COLOR_DEFENSIVA_TEAL, COLOR_DEFENSIVA_BG, COLOR_DEFENSIVA_BORDER, COLOR_DEFENSIVA_TEXT
        ),
        # Q2: Reorientación (WO) -> ÁMBAR
        (
            texts['s3_q2_title'], texts['s3_q2_pillar'], texts['s3_q2_bullets'], texts['s3_q2_budget'],
            COLOR_REORIENT_AMBER, COLOR_REORIENT_BG, COLOR_REORIENT_BORDER, COLOR_REORIENT_TEXT
        ),
        # Q3: Ofensiva (SO) -> AZUL
        (
            texts['s3_q3_title'], texts['s3_q3_pillar'], texts['s3_q3_bullets'], texts['s3_q3_budget'],
            COLOR_OFENSIVA_BLUE, COLOR_OFENSIVA_BG, COLOR_OFENSIVA_BORDER, COLOR_OFENSIVA_TEXT
        ),
        # Q4: Preservación Moat -> SLATE / NAVY
        (
            texts['s3_q4_title'], texts['s3_q4_pillar'], texts['s3_q4_bullets'], texts['s3_q4_budget'],
            COLOR_NAVY_DARK, RGBColor(241, 245, 249), COLOR_BORDER, COLOR_NAVY_MED
        ),
    ]

    q_w = Inches(2.78)
    q_gap = Inches(0.20)
    q_x = Inches(0.8)
    q_y = Inches(1.80)
    q_h = Inches(2.25)

    for q_idx, (q_title, q_pillar, q_bullets, q_budget, q_acc, q_bg, q_bord, q_txt) in enumerate(quarters_data):
        qx = q_x + q_idx * (q_w + q_gap)

        # Caja Trimestre
        q_shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx, q_y, q_w, q_h)
        q_shape.adjustments[0] = 0.05
        q_shape.fill.solid()
        q_shape.fill.fore_color.rgb = q_bg
        q_shape.line.color.rgb = q_acc
        q_shape.line.width = Pt(1.5)

        # Cabecera Trimestre
        q_head_tb = s3.shapes.add_textbox(qx + Inches(0.15), q_y + Inches(0.14), q_w - Inches(0.30), Inches(0.52))
        qtf_h = q_head_tb.text_frame
        qtf_h.word_wrap = True
        qtf_h.margin_left = qtf_h.margin_right = qtf_h.margin_top = qtf_h.margin_bottom = 0

        qp0 = qtf_h.paragraphs[0]
        qp0.text = q_title
        qp0.font.name = FONT_TITLE
        qp0.font.size = Pt(9)
        qp0.font.bold = True
        qp0.font.color.rgb = q_acc

        qp_pil = qtf_h.add_paragraph()
        pillar_prefix = "Pilar: " if lang == 'ES' else "Pillar: "
        qp_pil.text = f"{pillar_prefix}{q_pillar}"
        qp_pil.font.name = FONT_BODY
        qp_pil.font.size = Pt(8)
        qp_pil.font.bold = True
        qp_pil.font.color.rgb = q_txt
        qp_pil.space_before = Pt(2)

        # Viñetas de Iniciativas CAME (en caja de texto dedicada separada)
        q_bullets_tb = s3.shapes.add_textbox(qx + Inches(0.15), q_y + Inches(0.68), q_w - Inches(0.30), Inches(1.00))
        qtf_b = q_bullets_tb.text_frame
        qtf_b.word_wrap = True
        qtf_b.margin_left = qtf_b.margin_right = qtf_b.margin_top = qtf_b.margin_bottom = 0

        for b_i, b_str in enumerate(q_bullets):
            qpb = qtf_b.paragraphs[0] if b_i == 0 else qtf_b.add_paragraph()
            qpb.text = f"• {b_str}"
            qpb.font.name = FONT_BODY
            qpb.font.size = Pt(8.5)
            qpb.font.color.rgb = COLOR_TEXT_MAIN
            if b_i > 0:
                qpb.space_before = Pt(3)

        # Píldora de Presupuesto
        pb_y = q_y + q_h - Inches(0.38)
        pb_shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx + Inches(0.15), pb_y, q_w - Inches(0.30), Inches(0.28))
        pb_shape.adjustments[0] = 0.25
        pb_shape.fill.solid()
        pb_shape.fill.fore_color.rgb = q_acc
        pb_shape.line.fill.background()

        pbtb = s3.shapes.add_textbox(qx + Inches(0.15), pb_y, q_w - Inches(0.30), Inches(0.28))
        pbtb_tf = pbtb.text_frame
        pbtb_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        pbtb_tf.margin_left = pbtb_tf.margin_right = pbtb_tf.margin_top = pbtb_tf.margin_bottom = 0
        pb_p = pbtb_tf.paragraphs[0]
        prefix = "Partida: " if lang == 'ES' else "Budget: "
        pb_p.text = f"{prefix}{q_budget}"
        pb_p.font.name = FONT_TITLE
        pb_p.font.size = Pt(8)
        pb_p.font.bold = True
        pb_p.font.color.rgb = COLOR_WHITE
        pb_p.alignment = PP_ALIGN.CENTER

    # ==========================================================================
    # CAJA DESTACADA: DECISIÓN REQUERIDA DEL CONSEJO (BOARD DECISION GATEWAY)
    # ==========================================================================
    gw_x = Inches(0.8)
    gw_y = Inches(4.25)
    gw_w = Inches(11.733)
    gw_h = Inches(2.55)

    # Contenedor Fondo Oscuro Ejecutivo
    gw_bg = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gw_x, gw_y, gw_w, gw_h)
    gw_bg.adjustments[0] = 0.035
    gw_bg.fill.solid()
    gw_bg.fill.fore_color.rgb = COLOR_NAVY_DARK
    gw_bg.line.color.rgb = COLOR_GOLD
    gw_bg.line.width = Pt(1.5)

    # Encabezado Gateway
    gw_head_tb = s3.shapes.add_textbox(gw_x + Inches(0.35), gw_y + Inches(0.14), gw_w - Inches(0.70), Inches(0.48))
    gtf = gw_head_tb.text_frame
    gtf.word_wrap = True
    gtf.margin_left = gtf.margin_right = gtf.margin_top = gtf.margin_bottom = 0
    
    gp0 = gtf.paragraphs[0]
    gp0.text = texts['s3_gw_header']
    gp0.font.name = FONT_TITLE
    gp0.font.size = Pt(11)
    gp0.font.bold = True
    gp0.font.color.rgb = COLOR_GOLD_LIGHT

    gp1 = gtf.add_paragraph()
    gp1.text = texts['s3_gw_sub']
    gp1.font.name = FONT_BODY
    gp1.font.size = Pt(8.5)
    gp1.font.color.rgb = COLOR_BORDER
    gp1.space_before = Pt(2)

    # 3 Tarjetas de Resoluciones C-Level lado a lado (Alineación perfecta y simétrica sin desbordamiento)
    dec_cards = [
        (texts['s3_gw_d1_title'], texts['s3_gw_d1_val'], texts['s3_gw_d1_desc'], COLOR_OFENSIVA_BLUE),
        (texts['s3_gw_d2_title'], texts['s3_gw_d2_val'], texts['s3_gw_d2_desc'], COLOR_REORIENT_AMBER),
        (texts['s3_gw_d3_title'], texts['s3_gw_d3_val'], texts['s3_gw_d3_desc'], COLOR_DEFENSIVA_TEAL),
    ]

    dw_w = Inches(3.51)
    dw_gap = Inches(0.25)
    dw_y = gw_y + Inches(0.68)
    dw_h = Inches(1.70)
    gw_pad_x = Inches(0.35)

    for d_idx, (d_title, d_val, d_desc, d_color) in enumerate(dec_cards):
        dx = gw_x + gw_pad_x + d_idx * (dw_w + dw_gap)

        d_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, dw_y, dw_w, dw_h)
        d_card.adjustments[0] = 0.05
        d_card.fill.solid()
        d_card.fill.fore_color.rgb = COLOR_NAVY_MED
        d_card.line.color.rgb = d_color
        d_card.line.width = Pt(1.5)

        dtb = s3.shapes.add_textbox(dx + Inches(0.18), dw_y + Inches(0.14), dw_w - Inches(0.36), dw_h - Inches(0.24))
        dtf = dtb.text_frame
        dtf.word_wrap = True
        dtf.margin_left = dtf.margin_right = dtf.margin_top = dtf.margin_bottom = 0

        dp0 = dtf.paragraphs[0]
        dp0.text = d_title
        dp0.font.name = FONT_TITLE
        dp0.font.size = Pt(8.5)
        dp0.font.bold = True
        dp0.font.color.rgb = d_color

        dp_val = dtf.add_paragraph()
        dp_val.text = d_val
        dp_val.font.name = FONT_TITLE
        dp_val.font.size = Pt(15)
        dp_val.font.bold = True
        dp_val.font.color.rgb = COLOR_WHITE
        dp_val.space_before = Pt(3)
        dp_val.space_after = Pt(3)

        dp_desc = dtf.add_paragraph()
        dp_desc.text = d_desc
        dp_desc.font.name = FONT_BODY
        dp_desc.font.size = Pt(8.5)
        dp_desc.font.color.rgb = RGBColor(203, 213, 225) # Slate 300

    os.makedirs(os.path.dirname(texts['out_path']), exist_ok=True)
    prs.save(texts['out_path'])
    print(f"[OK {lang}] Presentación guardada en: {texts['out_path']} ({os.path.getsize(texts['out_path'])} bytes)")


def main():
    create_deck('ES')
    create_deck('EN')


if __name__ == '__main__':
    main()
