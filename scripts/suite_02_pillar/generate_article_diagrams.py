"""
Script: generate_article_diagrams.py
Genera los 3 diagramas visuales en alta definición (formato PNG) para el Post Pilar
de la Suite 02 (Toma de Decisiones & Priorización Cuantitativa) en Español e Inglés:

1. Diagrama 1: El Ciclo de Decisión Sesgada (HiPPO Effect Loop)
2. Diagrama 2: El Embudo Cuantitativo de Decisión en 3 Niveles (3-Tier Decision Funnel)
3. Diagrama 3: La Cadena de Custodia Decisional (Decision Custody Chain)

Estilo visual: Dark-Slate Tier-1 Datalaria (#0B1120, #0F172A, #1E293B, acentos cian, esmeralda, azul y ámbar).
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False, semibold=False):
    if bold:
        name = "segoeuib.ttf"
    elif semibold:
        name = "segoeuisb.ttf"
    else:
        name = "segoeui.ttf"
    
    path = os.path.join(r"C:\Windows\Fonts", name)
    if os.path.exists(path):
        return ImageFont.truetype(path, int(size))
    
    # Fallback to Arial
    alt = "arialbd.ttf" if bold else "arial.ttf"
    alt_path = os.path.join(r"C:\Windows\Fonts", alt)
    if os.path.exists(alt_path):
        return ImageFont.truetype(alt_path, int(size))
    return ImageFont.load_default()


def draw_arrow(draw, start, end, color=(148, 163, 184), width=2, arrow_size=6):
    """Dibuja una flecha recta entre start=(x1, y1) y end=(x2, y2)."""
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    if x1 == x2: # Vertical arrow
        if y2 > y1: # Downwards
            draw.polygon([(x2 - arrow_size, y2 - arrow_size), (x2 + arrow_size, y2 - arrow_size), (x2, y2 + 2)], fill=color)
        else: # Upwards
            draw.polygon([(x2 - arrow_size, y2 + arrow_size), (x2 + arrow_size, y2 + arrow_size), (x2, y2 - 2)], fill=color)
    elif y1 == y2: # Horizontal arrow
        if x2 > x1: # Rightwards
            draw.polygon([(x2 - arrow_size, y2 - arrow_size), (x2 - arrow_size, y2 + arrow_size), (x2 + 2, y2)], fill=color)
        else: # Leftwards
            draw.polygon([(x2 + arrow_size, y2 - arrow_size), (x2 + arrow_size, y2 + arrow_size), (x2 - 2, y2)], fill=color)


# =============================================================================
# DIAGRAMA 1: EL CICLO DE DECISIÓN SESGADA (HiPPO EFFECT)
# =============================================================================
def generate_diagram_hippo(lang="es"):
    is_es = (lang == "es")
    W, H = 1200, 360
    im = Image.new("RGB", (W, H), (11, 17, 32))  # Deep Slate Navy #0B1120
    draw = ImageDraw.Draw(im)

    # Frame
    draw.rounded_rectangle([12, 12, W - 12, H - 12], radius=14, outline=(30, 41, 59), width=2)

    # Header
    f_badge = get_font(11, bold=True)
    f_title = get_font(20, bold=True)
    f_sub = get_font(12, bold=False)
    f_card_num = get_font(11, bold=True)
    f_card_title = get_font(14, bold=True)
    f_card_sub = get_font(11, bold=True)
    f_card_body = get_font(11, bold=False)
    f_foot = get_font(11, bold=True)

    badge_text = (
        "PATOLOGÍA DE LA DECISIÓN SUBJETIVA  •  EL EFECTO HiPPO"
        if is_es else
        "PATHOLOGY OF SUBJECTIVE DECISION-MAKING  •  THE HiPPO EFFECT"
    )
    draw.rounded_rectangle([32, 24, 32 + (400 if is_es else 430), 44], radius=4, fill=(30, 41, 59))
    draw.text((42, 27), badge_text, font=f_badge, fill=(239, 68, 68))

    title_text = (
        "El Ciclo Vicioso del Sesgo de Confirmación en Comités Corporativos"
        if is_es else
        "The Vicious Cycle of Confirmation Bias in Corporate Committees"
    )
    draw.text((32, 50), title_text, font=f_title, fill=(248, 250, 252))

    sub_text = (
        "Cómo la intuición de la persona con mayor salario (HiPPO) sustituye al análisis cuantitativo estructurado"
        if is_es else
        "How the highest-paid person's opinion (HiPPO) substitutes structured quantitative inquiry"
    )
    draw.text((32, 78), sub_text, font=f_sub, fill=(148, 163, 184))

    # 4 Steps Cards
    steps = [
        {
            "num": "PASO 01" if is_es else "STEP 01",
            "title": "Intuición HiPPO" if is_es else "HiPPO Intuition",
            "badge": "Subjetividad Pura" if is_es else "Pure Gut-Feel",
            "color": (239, 68, 68),  # Red
            "bg": (28, 25, 38),
            "lines": [
                "El líder o directivo fija una" if is_es else "Executive establishes an initial",
                "preferencia personal previa" if is_es else "personal preference without prior",
                "sin filtros de veto ni datos." if is_es else "veto hurdles or quantitative validation."
            ]
        },
        {
            "num": "PASO 02" if is_es else "STEP 02",
            "title": "Búsqueda Sesgada" if is_es else "Selective Sourcing",
            "badge": "Sesgo Confirmación" if is_es else "Confirmation Bias",
            "color": (245, 158, 11), # Amber
            "bg": (32, 28, 28),
            "lines": [
                "Los equipos buscan métricas" if is_es else "Teams mine cherry-picked data",
                "aisladas para complacer y" if is_es else "solely to validate and support",
                "justificar la idea preconcebida." if is_es else "the pre-existing directive."
            ]
        },
        {
            "num": "PASO 03" if is_es else "STEP 03",
            "title": "Deck Persuasivo" if is_es else "Biased Slide Deck",
            "badge": "Elocuencia Verbal" if is_es else "Rhetorical Pitch",
            "color": (168, 85, 247), # Purple
            "bg": (28, 26, 38),
            "lines": [
                "Presentación cualitativa con" if is_es else "Polished qualitative slides with",
                "supuestos optimistas sin modelo" if is_es else "rosy assumptions lacking an",
                "DCF ni matriz de trade-offs." if is_es else "auditable DCF or trade-off matrix."
            ]
        },
        {
            "num": "PASO 04" if is_es else "STEP 04",
            "title": "Asignación Fallida" if is_es else "Capital Value Drain",
            "badge": "Destrucción de Valor" if is_es else "Destructive CAPEX",
            "color": (244, 63, 94),  # Rose
            "bg": (32, 24, 30),
            "lines": [
                "Aprobación de CAPEX y horas" if is_es else "Committees approve budget and squads",
                "en iniciativas inviables con" if is_es else "for fragile, high-risk initiatives",
                "alto coste de oportunidad." if is_es else "with massive opportunity cost."
            ]
        }
    ]

    card_w = 245
    card_h = 170
    gap = 48
    start_x = 32
    start_y = 112

    for i, s in enumerate(steps):
        cx = start_x + i * (card_w + gap)
        cy = start_y

        # Draw Card
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=8, fill=s["bg"], outline=s["color"], width=1)
        
        # Header inside card
        draw.text((cx + 14, cy + 12), s["num"], font=f_card_num, fill=s["color"])
        draw.text((cx + 14, cy + 28), s["title"], font=f_card_title, fill=(248, 250, 252))

        # Pill badge inside card
        pb_box = f_card_sub.getbbox(s["badge"])
        pw = pb_box[2] - pb_box[0] + 14
        draw.rounded_rectangle([cx + 14, cy + 54, cx + 14 + pw, cy + 72], radius=4, fill=(15, 23, 42), outline=s["color"], width=1)
        draw.text((cx + 21, cy + 56), s["badge"], font=f_card_sub, fill=s["color"])

        # Divider line
        draw.line([(cx + 14, cy + 82), (cx + card_w - 14, cy + 82)], fill=(51, 65, 85), width=1)

        # Body text
        ly = cy + 92
        for line in s["lines"]:
            draw.text((cx + 14, ly), line, font=f_card_body, fill=(203, 213, 225))
            ly += 18

        # Draw arrow to next card
        if i < len(steps) - 1:
            ax1 = cx + card_w + 8
            ax2 = cx + card_w + gap - 8
            ay = cy + card_h // 2
            draw_arrow(draw, (ax1, ay), (ax2, ay), color=(100, 116, 139), width=2, arrow_size=6)

    # Bottom takeaway bar
    bot_y = 302
    draw.rounded_rectangle([32, bot_y, W - 32, bot_y + 36], radius=6, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
    bot_text = (
        "🛡️ CÓMO LO RESUELVE DATALARIA SUITE 02: Sustituye la elocuencia por un pipeline matemático de 3 niveles (DAR + RICE + DCF)"
        if is_es else
        "🛡️ HOW DATALARIA SUITE 02 SOLVES THIS: Replaces rhetoric with a 3-tier quantitative pipeline (DAR + RICE + DCF)"
    )
    draw.text((46, bot_y + 9), bot_text, font=f_foot, fill=(56, 189, 248))

    return im


# =============================================================================
# DIAGRAMA 2: EL EMBUDO CUANTITATIVO DE DECISIÓN EN 3 NIVELES (MASTER FUNNEL)
# =============================================================================
def generate_diagram_funnel(lang="es"):
    is_es = (lang == "es")
    W, H = 1400, 1020
    im = Image.new("RGB", (W, H), (11, 17, 32))  # Deep Slate Navy #0B1120
    draw = ImageDraw.Draw(im)

    # Outer frame
    draw.rounded_rectangle([14, 14, W - 14, H - 14], radius=16, outline=(30, 41, 59), width=2)

    # Fonts
    f_top_badge = get_font(11, bold=True)
    f_main_title = get_font(24, bold=True)
    f_main_sub = get_font(13, bold=False)
    f_step_num = get_font(11, bold=True)
    f_tier_title = get_font(16, bold=True)
    f_tier_sub = get_font(12, bold=False)
    f_col_title = get_font(13, bold=True)
    f_col_body = get_font(11, bold=False)
    f_formula = get_font(12, bold=True)
    f_pill = get_font(10, bold=True)
    f_footer = get_font(11, bold=False)
    f_footer_b = get_font(11, bold=True)

    # 1. Header
    badge_txt = (
        "METODOLOGÍA EXECUTIVA DATALARIA  •  CMMI + AGILE + CORPORATE FINANCE"
        if is_es else
        "DATALARIA EXECUTIVE METHODOLOGY  •  CMMI + AGILE + CORPORATE FINANCE"
    )
    draw.rounded_rectangle([40, 26, 40 + (500 if is_es else 480), 48], radius=6, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw.text((50, 30), badge_txt, font=f_top_badge, fill=(56, 189, 248))

    title_txt = (
        "EL EMBUDO CUANTITATIVO DE DECISIÓN EN 3 NIVELES (THE 3-TIER DECISION FUNNEL)"
        if is_es else
        "THE 3-TIER QUANTITATIVE DECISION FUNNEL ARCHITECTURE"
    )
    draw.text((40, 56), title_txt, font=f_main_title, fill=(248, 250, 252))

    sub_txt = (
        "De los trade-offs de arquitectura y proveedores a la asignación de capacidad de squads y la justificación de CAPEX ante el CFO"
        if is_es else
        "From vendor and architecture trade-offs to squad capacity allocation and binding CFO Capex justification"
    )
    draw.text((40, 92), sub_txt, font=f_main_sub, fill=(148, 163, 184))

    # Top Trigger Node
    top_y = 125
    top_box_w = 760
    top_box_x = (W - top_box_w) // 2
    draw.rounded_rectangle([top_box_x, top_y, top_box_x + top_box_w, top_y + 46], radius=6, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    init_txt = (
        "⚡ INICIATIVA ESTRATÉGICA / RETO CORPORATIVO  (Modernización Cloud, Nuevo Producto, ERP o IA)"
        if is_es else
        "⚡ STRATEGIC MANDATE / CORPORATE CHALLENGE  (Cloud Migration, New Digital Product, ERP, or AI)"
    )
    it_bbox = f_col_title.getbbox(init_txt)
    it_w = it_bbox[2] - it_bbox[0]
    draw.text((top_box_x + (top_box_w - it_w) // 2, top_y + 13), init_txt, font=f_col_title, fill=(255, 255, 255))

    # Down arrow to Tier 1
    arrow_x = W // 2
    draw_arrow(draw, (arrow_x, top_y + 46), (arrow_x, top_y + 72), color=(56, 189, 248), width=2, arrow_size=6)

    # 3 Tiers Container definitions
    tier_w = W - 80 # 1320 px
    tier_h = 225
    col_w = (tier_w - 48) // 2 # 636 px
    start_ty = top_y + 72

    tiers_data = [
        {
            "id": "TIER 1",
            "title": "NIVEL 1: SELECCIÓN DE ARQUITECTURA & PROVEEDORES (MATRIZ DAR - CMMI)" if is_es else "TIER 1: ARCHITECTURE & VENDOR SELECTION (CMMI DAR MATRIX)",
            "subtitle": "Objetivo: Descartar opciones inviables y seleccionar la alternativa óptima mediante scoring multicriterio" if is_es else "Objective: Disqualify unviable options and rank viable candidates via multi-criteria scoring",
            "color": (16, 185, 129), # Emerald #10B981
            "bg": (15, 28, 28),
            "left_title": "1.1. Puerta de Filtros Veto (Must-Haves)" if is_es else "1.1. Boolean Veto Gate (Must-Haves)",
            "left_formula": "Condición Booleana: ∏(k=1..m) V_jk = 1  [Vk=0 descalifica]" if is_es else "Boolean Condition: ∏(k=1..m) V_jk = 1  [Vk=0 disqualifies]",
            "left_lines": [
                "• Filtros obligatorios de compliance (RGPD, ISO 27001, SOC2, residencia de datos)." if is_es else "• Mandatory compliance hurdles (GDPR, ISO 27001, SOC2, data residency).",
                "• Si una opción incumple 1 filtro (Vk = 0), queda descartada con puntuación 0.0." if is_es else "• If an option fails 1 hurdle (Vk = 0), it is immediately disqualified with Score 0.0.",
                "• Elimina el gasto de tiempo analizando proveedores técnicamente inviables." if is_es else "• Eliminates wasted time evaluating vendors that cannot operate legally."
            ],
            "right_title": "1.2. Scoring Ponderado (Wants) & Sensibilidad" if is_es else "1.2. Weighted Scoring (Wants) & Sensitivity",
            "right_formula": "Puntuación Final: S_j = ∑(w_i · s_ij)  donde  ∑ w_i = 100%" if is_es else "Final Score: S_j = ∑(w_i · s_ij)  where  ∑ w_i = 100%",
            "right_lines": [
                "• 4 Pilares de ponderación: Ajuste Técnico (30%), TCO 3 Años (25%), SLA (20%), Ciberseguridad (25%)." if is_es else "• 4 Weighted pillars: Technical Fit (30%), 3Y TCO (25%), SLA (20%), Security (25%).",
                "• Normalización en escala 1-5 basada en rúbricas objetivas predefinidas." if is_es else "• Standardized 1-5 scaling based on pre-established objective rubrics.",
                "• Test What-If de robustez para asegurar invarianza del ranking ante variaciones." if is_es else "• What-If stress test proving the winning vendor is immune to weighting shocks."
            ],
            "deliverable": "ENTREGABLE: Matriz DAR de Trade-Offs + Dictamen Formal de Proveedor Ganador" if is_es else "DELIVERABLE: DAR Trade-Off Matrix + Formal Winning Architecture Report"
        },
        {
            "id": "TIER 2",
            "title": "NIVEL 2: PRIORIZACIÓN DE ROADMAP & CAPACIDAD (MATRIZ RICE/ICE ÁGIL)" if is_es else "TIER 2: ROADMAP & CAPACITY PRIORITIZATION (AGILE RICE/ICE)",
            "subtitle": "Objetivo: Maximizar el retorno por sprint aplicando la línea de corte frente a la capacidad real de squads" if is_es else "Objective: Maximize return per sprint by applying greedy knapsack cut-off against squad capacity",
            "color": (59, 130, 246), # Blue #3B82F6
            "bg": (15, 23, 42),
            "left_title": "2.1. Algoritmo de Densidad de Valor RICE" if is_es else "2.1. RICE Value Density Algorithm",
            "left_formula": "RICE Score = (Reach · Impact · Confidence) / Effort  [Valor / Persona-Mes]" if is_es else "RICE Score = (Reach · Impact · Confidence) / Effort  [Value / Person-Month]",
            "left_lines": [
                "• Desglose de la solución ganadora en módulos, épicas e integraciones de backlog." if is_es else "• Granular breakdown of selected solution into epics, modules, and integrations.",
                "• Reach (usuarios/mes) e Impacto (0.25 a 3.0) calibrados por Confidence (50%-100%)." if is_es else "• Reach (events/mo) and Impact (0.25 to 3.0) calibrated by Confidence (50%-100%).",
                "• Esfuerzo en Persona-Mes: penaliza el coste de oportunidad de la ingeniería." if is_es else "• Effort measured in Person-Months: penalizes engineering opportunity cost."
            ],
            "right_title": "2.2. Matriz 2x2 & Línea de Corte de Capacidad" if is_es else "2.2. 2x2 Matrix & Knapsack Capacity Cut-Off",
            "right_formula": "Capacidad Neta = Capacidad Bruta · (1 - 0.167 Buffer Deuda Técnica)" if is_es else "Net Capacity = Gross Capacity · (1 - 0.167 Technical Debt Buffer)",
            "right_lines": [
                "• Matriz Cartesiana 2x2: Quick Wins (Alto Imp/Bajo Esf), Grandes Apuestas, Rellenos, Trampas." if is_es else "• 2x2 Quadrants: Quick Wins (High Imp/Low Eff), Big Bets, Fill-ins, Money Pits.",
                "• Algoritmo Knapsack Greedy: acumula esfuerzo hasta saturar la capacidad neta del trimestre." if is_es else "• Greedy Knapsack Cut-off: orders initiatives by density until net capacity saturates.",
                "• Asignación vinculante: Now (sprint en curso), Next (siguiente ciclo), Later (congelado)." if is_es else "• Governance output: Now (current sprint), Next (next cycle), Later (deferred)."
            ],
            "deliverable": "ENTREGABLE: Roadmap Vinculante de Ingeniería + Línea de Corte de Capacidad" if is_es else "DELIVERABLE: Binding Engineering Roadmap + Squad Capacity Cut-Off Line"
        },
        {
            "id": "TIER 3",
            "title": "NIVEL 3: JUSTIFICACIÓN DE CAPITAL ANTE EL CFO (BUSINESS CASE FINANCIERO DCF)" if is_es else "TIER 3: CAPITAL JUSTIFICATION TO CFO (DCF FINANCIAL BUSINESS CASE)",
            "subtitle": "Objetivo: Evaluar el retorno financiero, calcular el VAN/TIR y someter el riesgo a estrés con Gráfico Tornado" if is_es else "Objective: Compute NPV/IRR, evaluate CAPM cost of capital, and stress-test risk via Tornado Chart",
            "color": (245, 158, 11), # Amber #F59E0B
            "bg": (28, 25, 20),
            "left_title": "3.1. Flujo de Caja Libre Descontado (DCF)" if is_es else "3.1. Discounted Free Cash Flow (DCF)",
            "left_formula": "VAN = -I_0 + ∑(t=1..n) [ FCF_t / (1 + WACC)^t ]  con WACC por CAPM" if is_es else "NPV = -I_0 + ∑(t=1..n) [ FCF_t / (1 + WACC)^t ]  with CAPM WACC",
            "left_lines": [
                "• Activación obligatoria para iniciativas priorizadas en Tier 2 con CAPEX > 50.000 €." if is_es else "• Mandatory hurdle for initiatives cleared in Tier 2 requiring CAPEX > €50,000.",
                "• Proyección a 3-5 años: NOPAT + D&A − CAPEX − ΔNWC con Curva en J de tesorería." if is_es else "• 3-5 year projection: NOPAT + D&A − CAPEX − ΔNWC with cash flow J-Curve.",
                "• WACC calibrado rigurosamente: coste de fondos propios (Ke) y coste de deuda neta (Kd)." if is_es else "• Calibrated WACC: Ke via CAPM (Rf + β·ERP) and after-tax net debt cost (Kd)."
            ],
            "right_title": "3.2. Rentabilidad & Gráfico Tornado de Sensibilidad" if is_es else "3.2. Return Metrics & Sensitivity Tornado Chart",
            "right_formula": "Criterio de Aprobación: VAN > 0 €  •  TIR > WACC  •  Payback < 24m" if is_es else "Approval Gate: NPV > €0  •  IRR > WACC  •  Discounted Payback < 24m",
            "right_lines": [
                "• Gráfico Tornado: estresa los 5 factores críticos (adopción, churn, coste unitario, OPEX, WACC)." if is_es else "• Tornado Chart: ranks swings across 5 key variables (adoption, churn, pricing, OPEX).",
                "• Identifica el punto de equilibrio (Break-Even) y el margen de seguridad de la inversión." if is_es else "• Pinpoints exact break-even thresholds and financial safety margin.",
                "• Board Decision Gateway: paquete listo para aprobación vinculante en Consejo/CFO." if is_es else "• Board Decision Gateway: C-Level investment memorandum for formal capital release."
            ],
            "deliverable": "ENTREGABLE: Business Case Financiero en Excel + Deck PPTX 16:9 para Consejo" if is_es else "DELIVERABLE: Institutional DCF Excel Model + 16:9 C-Level Board Deck"
        }
    ]

    cur_ty = start_ty
    for idx, t in enumerate(tiers_data):
        # Draw Tier Box Frame
        draw.rounded_rectangle([40, cur_ty, 40 + tier_w, cur_ty + tier_h], radius=10, fill=t["bg"], outline=t["color"], width=2)

        # Header bar of tier
        hb_h = 36
        draw.rounded_rectangle([40, cur_ty, 40 + tier_w, cur_ty + hb_h], radius=8, fill=(15, 23, 42))
        draw.rectangle([40, cur_ty + hb_h - 4, 40 + tier_w, cur_ty + hb_h], fill=(15, 23, 42))

        # Badge ID
        draw.rounded_rectangle([52, cur_ty + 6, 120, cur_ty + 30], radius=4, fill=t["color"])
        draw.text((62, cur_ty + 9), t["id"], font=f_step_num, fill=(11, 17, 32))

        # Title
        draw.text((134, cur_ty + 8), t["title"], font=f_tier_title, fill=(255, 255, 255))

        # Subtitle
        draw.text((54, cur_ty + 42), t["subtitle"], font=f_tier_sub, fill=(148, 163, 184))

        # Two inner columns
        inner_y = cur_ty + 64
        col_h = 118
        c1_x = 54
        c2_x = 54 + col_w + 24

        # Col 1 (Left)
        draw.rounded_rectangle([c1_x, inner_y, c1_x + col_w, inner_y + col_h], radius=6, fill=(11, 17, 32), outline=(51, 65, 85), width=1)
        draw.text((c1_x + 12, inner_y + 8), t["left_title"], font=f_col_title, fill=t["color"])
        draw.text((c1_x + 12, inner_y + 26), t["left_formula"], font=f_formula, fill=(226, 232, 240))
        draw.line([(c1_x + 12, inner_y + 44), (c1_x + col_w - 12, inner_y + 44)], fill=(30, 41, 59), width=1)
        cy1 = inner_y + 50
        for l in t["left_lines"]:
            draw.text((c1_x + 12, cy1), l, font=f_col_body, fill=(203, 213, 225))
            cy1 += 18

        # Col 2 (Right)
        draw.rounded_rectangle([c2_x, inner_y, c2_x + col_w, inner_y + col_h], radius=6, fill=(11, 17, 32), outline=(51, 65, 85), width=1)
        draw.text((c2_x + 12, inner_y + 8), t["right_title"], font=f_col_title, fill=t["color"])
        draw.text((c2_x + 12, inner_y + 26), t["right_formula"], font=f_formula, fill=(226, 232, 240))
        draw.line([(c2_x + 12, inner_y + 44), (c2_x + col_w - 12, inner_y + 44)], fill=(30, 41, 59), width=1)
        cy2 = inner_y + 50
        for l in t["right_lines"]:
            draw.text((c2_x + 12, cy2), l, font=f_col_body, fill=(203, 213, 225))
            cy2 += 18

        # Deliverable bar at bottom of tier
        deliv_y = inner_y + col_h + 8
        draw.rounded_rectangle([54, deliv_y, 54 + tier_w - 28, deliv_y + 24], radius=4, fill=(15, 23, 42), outline=t["color"], width=1)
        draw.text((66, deliv_y + 4), t["deliverable"], font=f_pill, fill=t["color"])

        # Arrow down to next tier
        if idx < len(tiers_data) - 1:
            ay1 = cur_ty + tier_h
            ay2 = cur_ty + tier_h + 28
            draw_arrow(draw, (arrow_x, ay1), (arrow_x, ay2), color=t["color"], width=2, arrow_size=6)
            cur_ty += tier_h + 28
        else:
            cur_ty += tier_h

    # Footer line
    draw.line([(40, H - 45), (W - 40, H - 45)], fill=(30, 41, 59), width=1)
    foot_left = (
        "DATALARIA.COM  •  SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN  •  ESTÁNDAR CMMI, AGILE & CORPORATE FINANCE"
        if is_es else
        "DATALARIA.COM  •  SUITE 02: QUANTITATIVE DECISION-MAKING & PRIORITIZATION  •  CMMI, AGILE & CORPORATE FINANCE"
    )
    draw.text((40, H - 32), foot_left, font=f_footer, fill=(100, 116, 139))

    foot_right = (
        "PIPELINE INTEGRADO EN 3 NIVELES  •  15 ENTREGABLES CUANTITATIVOS  •  15€"
        if is_es else
        "INTEGRATED 3-TIER DECISION PIPELINE  •  15 QUANTITATIVE DELIVERABLES  •  15€"
    )
    fr_box = f_footer_b.getbbox(foot_right)
    draw.text((W - 40 - (fr_box[2] - fr_box[0]), H - 32), foot_right, font=f_footer_b, fill=(56, 189, 248))

    return im


# =============================================================================
# DIAGRAMA 3: LA CADENA DE CUSTODIA DECISIONAL (CUSTODY CHAIN PIPELINE)
# =============================================================================
def generate_diagram_custody_chain(lang="es"):
    is_es = (lang == "es")
    W, H = 1200, 680
    im = Image.new("RGB", (W, H), (11, 17, 32))  # Deep Slate Navy #0B1120
    draw = ImageDraw.Draw(im)

    # Frame
    draw.rounded_rectangle([12, 12, W - 12, H - 12], radius=14, outline=(30, 41, 59), width=2)

    f_badge = get_font(11, bold=True)
    f_title = get_font(20, bold=True)
    f_sub = get_font(12, bold=False)
    f_card_num = get_font(11, bold=True)
    f_card_title = get_font(14, bold=True)
    f_card_sub = get_font(11, bold=True)
    f_card_body = get_font(11, bold=False)
    f_pill = get_font(10, bold=True)
    f_foot = get_font(11, bold=False)

    badge_text = (
        "GOBERNANZA DE INVERSIONES  •  CADENA DE CUSTODIA DECISIONAL"
        if is_es else
        "INVESTMENT GOVERNANCE  •  DECISION CUSTODY CHAIN PIPELINE"
    )
    draw.rounded_rectangle([32, 24, 32 + (420 if is_es else 400), 44], radius=4, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw.text((42, 27), badge_text, font=f_badge, fill=(56, 189, 248))

    title_text = (
        "Cómo Navega una Iniciativa el Pipeline: De la Idea a la Ejecución Auditada"
        if is_es else
        "How an Initiative Traverses the Pipeline: From Mandate to Audited Execution"
    )
    draw.text((32, 50), title_text, font=f_title, fill=(248, 250, 252))

    sub_text = (
        "El protocolo paso a paso para evitar proyectos zombi y justificar la asignación de capital con rigor matemático"
        if is_es else
        "The step-by-step protocol to prevent zombie initiatives and defend capital allocation with mathematical rigor"
    )
    draw.text((32, 78), sub_text, font=f_sub, fill=(148, 163, 184))

    # Top Trigger: Reto Estratégico
    top_w = 460
    top_x = (W - top_w) // 2
    top_y = 110
    draw.rounded_rectangle([top_x, top_y, top_x + top_w, top_y + 38], radius=6, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    t_text = "[0] RETO ESTRATÉGICO / NECESIDAD DE NEGOCIO" if is_es else "[0] STRATEGIC MANDATE / BUSINESS OPPORTUNITY"
    tb_box = f_card_title.getbbox(t_text)
    draw.text((top_x + (top_w - (tb_box[2] - tb_box[0])) // 2, top_y + 10), t_text, font=f_card_title, fill=(255, 255, 255))

    mid_x = W // 2
    draw_arrow(draw, (mid_x, top_y + 38), (mid_x, top_y + 60), color=(148, 163, 184), width=2, arrow_size=6)

    # 3 Gateway Cards Stacked Vertically
    gateways = [
        {
            "badge": "GATEWAY 1 · SELECCIÓN ARQUITECTÓNICA",
            "title": "NIVEL 1: MATRIZ DAR (CMMI & KT)",
            "color": (16, 185, 129), # Emerald
            "bg": (15, 28, 28),
            "crit": "¿Qué evalúa?: 3 a 5 arquitecturas o proveedores alternativos ante requisitos no negociables.",
            "rule": "Mecanismo: Filtros Veto (Must-Haves) descalifican opciones no conformes (Vk=0). Ponderación multicriterio de las viables.",
            "out": "Resultado Vinculante: Selección indiscutible de la Solución Técnica Óptima."
        },
        {
            "badge": "GATEWAY 2 · PRIORIZACIÓN & CAPACIDAD",
            "title": "NIVEL 2: MATRIZ RICE & ICE ÁGIL",
            "color": (59, 130, 246), # Blue
            "bg": (15, 23, 42),
            "crit": "¿Qué evalúa?: Desglose de la solución en épicas, módulos e integraciones con scoring de densidad de valor.",
            "rule": "Mecanismo: RICE = (R·I·C)/E. Segmentación en Matriz 2x2 y línea de corte Knapsack según capacidad neta de squads.",
            "out": "Resultado Vinculante: Roadmap ejecutivo Now (Sprint en curso), Next (Siguiente ciclo) y Later (Diferido)."
        },
        {
            "badge": "GATEWAY 3 · JUSTIFICACIÓN FINANCIERA",
            "title": "NIVEL 3: BUSINESS CASE FINANCIERO (DCF)",
            "color": (245, 158, 11), # Amber
            "bg": (28, 25, 20),
            "crit": "¿Qué evalúa?: Iniciativas priorizadas en 'Now' cuyo desembolso supere el umbral de CAPEX > 50.000 €.",
            "rule": "Mecanismo: Proyección DCF 3-5 años, WACC por CAPM, cálculo de VAN, TIR y Payback Descontado con Gráfico Tornado.",
            "out": "Resultado Vinculante: Board Decision Gateway firmado y liberación formal de fondos en Consejo de Administración."
        }
    ]

    if not is_es:
        gateways = [
            {
                "badge": "GATEWAY 1 · ARCHITECTURAL SELECTION",
                "title": "TIER 1: QUANTITATIVE DAR MATRIX (CMMI & KT)",
                "color": (16, 185, 129),
                "bg": (15, 28, 28),
                "crit": "Evaluation Scope: 3 to 5 candidate architectures or vendors benchmarked against non-negotiable constraints.",
                "rule": "Mechanism: Boolean Veto Gates (Must-Haves) disqualify violators (Vk=0). Multi-criteria scoring for surviving candidates.",
                "out": "Binding Output: Undisputable selection of the mathematically optimal technical architecture."
            },
            {
                "badge": "GATEWAY 2 · CAPACITY & BACKLOG ROADMAP",
                "title": "TIER 2: AGILE RICE & ICE PRIORITIZATION",
                "color": (59, 130, 246),
                "bg": (15, 23, 42),
                "crit": "Evaluation Scope: Decomposition of selected solution into epics, modules, and integrations ranked by value density.",
                "rule": "Mechanism: RICE = (R·I·C)/E. 2x2 Matrix segmentation and greedy knapsack cut-off against net squad capacity.",
                "out": "Binding Output: Enforceable Roadmap: Now (active sprint), Next (next cycle), Later (deprioritized backlog)."
            },
            {
                "badge": "GATEWAY 3 · FINANCIAL CAPEX GOVERNANCE",
                "title": "TIER 3: INSTITUTIONAL DCF BUSINESS CASE",
                "color": (245, 158, 11),
                "bg": (28, 25, 20),
                "crit": "Evaluation Scope: High-priority 'Now' initiatives with cumulative CAPEX exceeding €50,000.",
                "rule": "Mechanism: 3-5Y Free Cash Flow DCF model, CAPM WACC, NPV, IRR, and Discounted Payback with Tornado sensitivity.",
                "out": "Binding Output: Executed Board Decision Gateway and formal capital appropriation by the CFO/Board."
            }
        ]

    card_h = 120
    cur_gy = top_y + 60
    card_w = W - 120

    for i, g in enumerate(gateways):
        gx = 60
        draw.rounded_rectangle([gx, cur_gy, gx + card_w, cur_gy + card_h], radius=8, fill=g["bg"], outline=g["color"], width=1)

        # Badge pill
        pb_box = f_card_num.getbbox(g["badge"])
        pw = pb_box[2] - pb_box[0] + 16
        draw.rounded_rectangle([gx + 16, cur_gy + 10, gx + 16 + pw, cur_gy + 28], radius=4, fill=(15, 23, 42), outline=g["color"], width=1)
        draw.text((gx + 24, cur_gy + 12), g["badge"], font=f_card_num, fill=g["color"])

        # Title
        draw.text((gx + 28 + pw, cur_gy + 10), g["title"], font=f_card_title, fill=(255, 255, 255))

        # Divider
        draw.line([(gx + 16, cur_gy + 34), (gx + card_w - 16, cur_gy + 34)], fill=(51, 65, 85), width=1)

        # 3 bullets
        draw.text((gx + 18, cur_gy + 42), "• " + g["crit"], font=f_card_body, fill=(226, 232, 240))
        draw.text((gx + 18, cur_gy + 64), "• " + g["rule"], font=f_card_body, fill=(203, 213, 225))
        draw.text((gx + 18, cur_gy + 86), "✔ " + g["out"], font=f_card_sub, fill=g["color"])

        # Arrow down
        if i < len(gateways) - 1:
            draw_arrow(draw, (mid_x, cur_gy + card_h), (mid_x, cur_gy + card_h + 22), color=g["color"], width=2, arrow_size=6)
            cur_gy += card_h + 22
        else:
            cur_gy += card_h

    # Bottom Terminal Node
    cur_gy += 20
    bot_w = 460
    bot_x = (W - bot_w) // 2
    draw_arrow(draw, (mid_x, cur_gy - 20), (mid_x, cur_gy), color=(16, 185, 129), width=2, arrow_size=6)
    draw.rounded_rectangle([bot_x, cur_gy, bot_x + bot_w, cur_gy + 36], radius=6, fill=(16, 185, 129))
    bot_txt = "🚀 EJECUCIÓN AUDITADA & CREACIÓN NETA DE VALOR" if is_es else "🚀 AUDITED EXECUTION & NET VALUE CREATION"
    bb_box = f_card_title.getbbox(bot_txt)
    draw.text((bot_x + (bot_w - (bb_box[2] - bb_box[0])) // 2, cur_gy + 8), bot_txt, font=f_card_title, fill=(11, 17, 32))

    return im


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    es_post_dir = os.path.join(base_dir, "content", "es", "posts", "toma-decisiones-priorizacion-framework-cuantitativo")
    en_post_dir = os.path.join(base_dir, "content", "en", "posts", "decision-making-prioritization-quantitative-framework")
    static_recursos = os.path.join(base_dir, "static", "images", "recursos")

    os.makedirs(es_post_dir, exist_ok=True)
    os.makedirs(en_post_dir, exist_ok=True)
    os.makedirs(static_recursos, exist_ok=True)

    print("[*] Generando Diagrama 1: El Ciclo de Decisión Sesgada (HiPPO)...")
    d1_es = generate_diagram_hippo("es")
    d1_en = generate_diagram_hippo("en")
    d1_es.save(os.path.join(es_post_dir, "ciclo-sesgo-hippo-decision.png"), format="PNG", optimize=True)
    d1_es.save(os.path.join(static_recursos, "suite-02-diagram-01-hippo-es.png"), format="PNG", optimize=True)
    d1_en.save(os.path.join(en_post_dir, "hippo-bias-decision-loop.png"), format="PNG", optimize=True)
    d1_en.save(os.path.join(static_recursos, "suite-02-diagram-01-hippo-en.png"), format="PNG", optimize=True)

    print("[*] Generando Diagrama 2: El Embudo Cuantitativo de Decisión en 3 Niveles (Master Funnel)...")
    d2_es = generate_diagram_funnel("es")
    d2_en = generate_diagram_funnel("en")
    d2_es.save(os.path.join(es_post_dir, "pipeline-decision-3-niveles-cuantitativo.png"), format="PNG", optimize=True)
    d2_es.save(os.path.join(static_recursos, "suite-02-diagram-02-funnel-es.png"), format="PNG", optimize=True)
    d2_en.save(os.path.join(en_post_dir, "3-tier-quantitative-decision-pipeline.png"), format="PNG", optimize=True)
    d2_en.save(os.path.join(static_recursos, "suite-02-diagram-02-funnel-en.png"), format="PNG", optimize=True)

    print("[*] Generando Diagrama 3: La Cadena de Custodia Decisional (Custody Chain Pipeline)...")
    d3_es = generate_diagram_custody_chain("es")
    d3_en = generate_diagram_custody_chain("en")
    d3_es.save(os.path.join(es_post_dir, "cadena-custodia-decisional-pipeline.png"), format="PNG", optimize=True)
    d3_es.save(os.path.join(static_recursos, "suite-02-diagram-03-custody-chain-es.png"), format="PNG", optimize=True)
    d3_en.save(os.path.join(en_post_dir, "decision-custody-chain-pipeline.png"), format="PNG", optimize=True)
    d3_en.save(os.path.join(static_recursos, "suite-02-diagram-03-custody-chain-en.png"), format="PNG", optimize=True)

    print("[OK] Todos los diagramas generados y guardados con éxito en los posts y en static/images/recursos/.")


if __name__ == "__main__":
    main()
