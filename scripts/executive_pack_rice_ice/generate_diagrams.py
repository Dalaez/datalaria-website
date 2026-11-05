#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_diagrams.py
====================
Genera de forma programática las 3 imágenes oficiales de alta resolución
para los artículos de la Matriz RICE & ICE de Priorización Ágil (ES y EN):
1. diagrama-1-embudo-decisiones.png / diagram-1-decision-funnel.png
   (Embudo Estratégico Integral: De Suite 01 Estrategia a Suite 02 Decisiones)
2. diagrama-2-flujo-priorizacion-rice.png / diagram-2-rice-prioritization-pipeline.png
   (Pipeline Cuantitativo de Priorización de Producto en 6 Fases)
3. diagrama-3-matriz-impacto-esfuerzo.png / diagram-3-impact-effort-matrix.png
   (Matriz Estratégica 2x2: Valor Esperado vs Esfuerzo & Cuadrantes Cartesianos)

Estándar Visual Tier-1 (McKinsey / BCG / Intercom):
- Fondo limpio (#FFFFFF) con marco técnico redondeado (#CBD5E1 / #94A3B8).
- Tipografía nítida corporativa (Segoe UI / Arial).
- Coherencia cromática con la identidad visual de Datalaria.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# HELPERS DE FUENTES Y DIBUJO
# ==============================================================================

def get_font(name, size):
    """Carga fuente TrueType del sistema o fallback estándar."""
    paths = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_arrow_down(draw, x, y_start, y_end, color=(100, 116, 139), width=2):
    """Dibuja una flecha vertical hacia abajo con punta proporcionada."""
    draw.line([(x, y_start), (x, y_end)], fill=color, width=width)
    draw.polygon([(x - 5, y_end - 6), (x + 5, y_end - 6), (x, y_end)], fill=color)


def draw_arrow_right(draw, x_start, x_end, y, color=(100, 116, 139), width=2):
    """Dibuja una flecha horizontal hacia la derecha."""
    draw.line([(x_start, y), (x_end, y)], fill=color, width=width)
    draw.polygon([(x_end - 6, y - 5), (x_end - 6, y + 5), (x_end, y)], fill=color)


# ==============================================================================
# DIAGRAMA 1: EL EMBUDO ESTRATÉGICO INTEGRAL (DECISION FUNNEL)
# ==============================================================================

def generate_diagram_1(lang='ES', out_path=None):
    width = 1040
    height = 720

    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/matriz-rice-ice-priorizacion/diagrama-1-embudo-decisiones.png"
        else:
            out_path = "content/en/posts/rice-ice-prioritization-matrix/diagram-1-decision-funnel.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Marco exterior
    draw.rounded_rectangle([(10, 10), (width - 10, height - 10)], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

    # Fuentes
    f_title = get_font("segoeuib.ttf", 22)
    f_sub = get_font("segoeui.ttf", 13)
    f_box_title = get_font("segoeuib.ttf", 15)
    f_box_desc = get_font("segoeui.ttf", 12)

    # Cabecera
    title_text = (
        "Embudo de Decisión Estratégica: De Suite 01 Estrategia a Suite 02 Decisiones"
        if lang == 'ES' else
        "Strategic Decision Funnel: From Suite 01 Strategy to Suite 02 Decisions"
    )
    sub_text = (
        "Cadena de Gobernanza Corporativa: Del Diagnóstico Macro a la Priorización de Capacidad"
        if lang == 'ES' else
        "Corporate Governance Chain: From Macro Diagnosis to Net Backlog Capacity Allocation"
    )

    draw.text((width // 2, 38), title_text, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((width // 2, 64), sub_text, fill=(100, 116, 139), font=f_sub, anchor="mm")

    # 6 Niveles
    levels_es = [
        {
            "title": "Nivel 1: Macroentorno Exógeno — Matriz PESTEL Cuantitativa",
            "desc": "Riesgos geopolíticos, regulación de IA (EU AI Act), inflación y factores ESG",
            "fill": (239, 246, 255), "border": (59, 130, 246), "t_color": (30, 58, 138), "d_color": (37, 99, 235)
        },
        {
            "title": "Nivel 2: Dinámica Microeconómica — 5 Fuerzas de Porter Ponderadas",
            "desc": "Poder de compradores, rivalidad SaaS, barreras de entrada y foso defensivo (Economic Moat)",
            "fill": (238, 242, 255), "border": (99, 102, 241), "t_color": (49, 46, 129), "d_color": (67, 56, 202)
        },
        {
            "title": "Nivel 3: Diagnóstico Interno & Cruce — DAFO Cuantitativo & Matriz CAME",
            "desc": "Vincular fortalezas tecnológicas y operativas con oportunidades de mercado",
            "fill": (236, 253, 245), "border": (16, 185, 129), "t_color": (6, 78, 59), "d_color": (4, 120, 87)
        },
        {
            "title": "Nivel 4: Gestión de Cartera y CAPEX — Matriz BCG & Matriz McKinsey / GE 3x3",
            "desc": "Asignación de capital corporativo por UEN (Estrellas, Vacas Lecheras, Inversión selectiva)",
            "fill": (255, 251, 235), "border": (245, 158, 11), "t_color": (146, 64, 14), "d_color": (180, 83, 9)
        },
        {
            "title": "Nivel 5: Adjudicación de Grandes Decisiones — Matriz DAR Cuantitativa (CMMI / KT)",
            "desc": "Filtros Veto, ponderación multicriterio, Make vs. Buy y selección de plataformas críticas",
            "fill": (15, 23, 42), "border": (100, 116, 139), "t_color": (255, 255, 255), "d_color": (203, 213, 225)
        },
        {
            "title": "Nivel 6: Priorización de Roadmap y Capacidad — Matriz RICE & ICE Ágil",
            "desc": "Densidad de valor, ICE growth, cuadrantes 2x2, línea de corte y asignación Now/Next/Later",
            "fill": (15, 23, 42), "border": (37, 99, 235), "t_color": (96, 165, 250), "d_color": (226, 232, 240), "highlight": True
        }
    ]

    levels_en = [
        {
            "title": "Level 1: Exogenous Macro-Environment — Quantitative PESTEL Matrix",
            "desc": "Geopolitical risks, AI regulation (EU AI Act), inflation, sovereign data and ESG factors",
            "fill": (239, 246, 255), "border": (59, 130, 246), "t_color": (30, 58, 138), "d_color": (37, 99, 235)
        },
        {
            "title": "Level 2: Microeconomic Dynamics — Weighted Porter's 5 Forces",
            "desc": "Buyer power, SaaS rivalry, barriers to entry, substitution risks and Economic Moat",
            "fill": (238, 242, 255), "border": (99, 102, 241), "t_color": (49, 46, 129), "d_color": (67, 56, 202)
        },
        {
            "title": "Level 3: Internal Diagnosis & Alignment — Quantitative SWOT & TOWS/CAME Matrix",
            "desc": "Aligning internal engineering & operational strengths with external market opportunities",
            "fill": (236, 253, 245), "border": (16, 185, 129), "t_color": (6, 78, 59), "d_color": (4, 120, 87)
        },
        {
            "title": "Level 4: Portfolio Management & CAPEX — BCG Matrix & McKinsey / GE 3x3",
            "desc": "Corporate capital allocation across SBUs (Stars, Cash Cows, Selective growth bets)",
            "fill": (255, 251, 235), "border": (245, 158, 11), "t_color": (146, 64, 14), "d_color": (180, 83, 9)
        },
        {
            "title": "Level 5: High-Stakes Decision Governance — Quantitative DAR Matrix (CMMI / KT)",
            "desc": "Binary veto knockout filters, multi-criteria weighting, Make vs. Buy and platform selection",
            "fill": (15, 23, 42), "border": (100, 116, 139), "t_color": (255, 255, 255), "d_color": (203, 213, 225)
        },
        {
            "title": "Level 6: Roadmap & Capacity Prioritization — Agile RICE & ICE Matrix",
            "desc": "Value density, ICE growth, 2x2 quadrants, team capacity cut-line & Now/Next/Later",
            "fill": (15, 23, 42), "border": (37, 99, 235), "t_color": (96, 165, 250), "d_color": (226, 232, 240), "highlight": True
        }
    ]

    levels = levels_es if lang == 'ES' else levels_en

    box_w = 920
    box_h = 70
    box_x = (width - box_w) // 2
    cur_y = 92
    arrow_len = 20

    for i, lvl in enumerate(levels):
        b_width = 3 if lvl.get("highlight") else 2
        draw.rounded_rectangle(
            [(box_x, cur_y), (box_x + box_w, cur_y + box_h)],
            radius=8,
            fill=lvl["fill"],
            outline=lvl["border"],
            width=b_width
        )
        draw.text((box_x + box_w // 2, cur_y + 24), lvl["title"], fill=lvl["t_color"], font=f_box_title, anchor="mm")
        draw.text((box_x + box_w // 2, cur_y + 48), lvl["desc"], fill=lvl["d_color"], font=f_box_desc, anchor="mm")

        if i < len(levels) - 1:
            arrow_start_y = cur_y + box_h
            arrow_end_y = arrow_start_y + arrow_len
            draw_arrow_down(draw, width // 2, arrow_start_y, arrow_end_y, color=(100, 116, 139), width=2)
            cur_y += box_h + arrow_len
        else:
            cur_y += box_h

    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Diagrama 1 generado ({lang}): {out_path}")
    return out_path


# ==============================================================================
# DIAGRAMA 2: PIPELINE DE PRIORIZACIÓN CUANTITATIVA (6 FASES)
# ==============================================================================

def generate_diagram_2(lang='ES', out_path=None):
    width = 1060
    height = 760

    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/matriz-rice-ice-priorizacion/diagrama-2-flujo-priorizacion-rice.png"
        else:
            out_path = "content/en/posts/rice-ice-prioritization-matrix/diagram-2-rice-prioritization-pipeline.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Marco exterior
    draw.rounded_rectangle([(10, 10), (width - 10, height - 10)], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

    # Fuentes
    f_title = get_font("segoeuib.ttf", 22)
    f_sub = get_font("segoeui.ttf", 13)
    f_step_title = get_font("segoeuib.ttf", 14)
    f_step_desc = get_font("segoeui.ttf", 12)

    # Cabecera
    title_text = (
        "Pipeline de Priorización Cuantitativa de Producto (6 Fases Secuenciales)"
        if lang == 'ES' else
        "Quantitative Product Prioritization Pipeline (6 Sequential Phases)"
    )
    sub_text = (
        "Protocolo Secuencial: Del Inventario de Demanda a la Asignación de Capacidad y Firma C-Level"
        if lang == 'ES' else
        "Sequential Protocol: From Raw Demand Inventory to Net Squad Capacity & C-Level Sign-Off"
    )

    draw.text((width // 2, 36), title_text, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((width // 2, 60), sub_text, fill=(100, 116, 139), font=f_sub, anchor="mm")

    box_w = 920
    box_x = (width - box_w) // 2
    cur_y = 85
    arrow_len = 15

    # 1. Backlog Bruto
    step1_title = "1. Backlog Bruto de Iniciativas" if lang == 'ES' else "1. Raw Initiative Backlog"
    step1_desc = (
        "Inventario exhaustivo de peticiones de clientes, visión de producto, deuda técnica y arquitectura"
        if lang == 'ES' else
        "Exhaustive inventory of customer requests, product vision, technical debt and architectural epics"
    )
    draw.rounded_rectangle([(box_x, cur_y), (box_x + box_w, cur_y + 52)], radius=7, fill=(248, 250, 252), outline=(100, 116, 139), width=1)
    draw.text((box_x + box_w // 2, cur_y + 17), step1_title, fill=(15, 23, 42), font=f_step_title, anchor="mm")
    draw.text((box_x + box_w // 2, cur_y + 36), step1_desc, fill=(71, 85, 105), font=f_step_desc, anchor="mm")

    # Arrow 1 -> 2
    cur_y += 52
    draw_arrow_down(draw, width // 2, cur_y, cur_y + arrow_len, color=(100, 116, 139), width=2)
    cur_y += arrow_len

    # 2. Calibración de Escalas
    step2_title = "2. Protocolo de Calibración de Escalas" if lang == 'ES' else "2. Scale Calibration Protocol"
    step2_desc = (
        "Normalización objetiva: Reach empírico trimestral • Rúbrica de Impacto (0.25 a 3.0) • Confidence Meter (50%-80%-100%)"
        if lang == 'ES' else
        "Objective normalization: Quarterly Reach • Impact Rubric (0.25 to 3.0) • Confidence Meter (50%-80%-100%)"
    )
    draw.rounded_rectangle([(box_x, cur_y), (box_x + box_w, cur_y + 52)], radius=7, fill=(239, 246, 255), outline=(59, 130, 246), width=1)
    draw.text((box_x + box_w // 2, cur_y + 17), step2_title, fill=(30, 58, 138), font=f_step_title, anchor="mm")
    draw.text((box_x + box_w // 2, cur_y + 36), step2_desc, fill=(37, 99, 235), font=f_step_desc, anchor="mm")

    # Arrow 2 -> Triage
    cur_y += 52
    draw_arrow_down(draw, width // 2, cur_y, cur_y + arrow_len, color=(100, 116, 139), width=2)
    cur_y += arrow_len

    # Triage Decision Box
    triage_title = "¿Horizonte de la Iniciativa?" if lang == 'ES' else "Initiative Horizon Triage?"
    triage_desc = (
        "Bifurcación metodológica según ciclo de entrega y nivel de incertidumbre"
        if lang == 'ES' else
        "Methodological branching based on delivery cycle and uncertainty level"
    )
    triage_w = 460
    triage_x = (width - triage_w) // 2
    draw.rounded_rectangle([(triage_x, cur_y), (triage_x + triage_w, cur_y + 44)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235), width=2)
    draw.text((width // 2, cur_y + 15), triage_title, fill=(255, 255, 255), font=f_step_title, anchor="mm")
    draw.text((width // 2, cur_y + 31), triage_desc, fill=(147, 197, 253), font=get_font("segoeui.ttf", 10), anchor="mm")

    # Branching arrows
    cur_y += 44
    branch_arrow_h = 16
    left_x = box_x + (box_w // 4)
    right_x = box_x + (box_w * 3 // 4)

    split_y = cur_y + branch_arrow_h // 2
    draw.line([(width // 2, cur_y), (width // 2, split_y)], fill=(100, 116, 139), width=2)
    draw.line([(left_x, split_y), (right_x, split_y)], fill=(100, 116, 139), width=2)
    draw_arrow_down(draw, left_x, split_y, cur_y + branch_arrow_h, color=(100, 116, 139), width=2)
    draw_arrow_down(draw, right_x, split_y, cur_y + branch_arrow_h, color=(100, 116, 139), width=2)
    cur_y += branch_arrow_h

    # Two parallel boxes: RICE (Left) & ICE (Right)
    split_box_w = (box_w - 20) // 2
    rice_x = box_x
    ice_x = box_x + split_box_w + 20
    split_h = 58

    # RICE Box
    draw.rounded_rectangle([(rice_x, cur_y), (rice_x + split_box_w, cur_y + split_h)], radius=7, fill=(240, 253, 244), outline=(16, 185, 129), width=2)
    draw.text((rice_x + split_box_w // 2, cur_y + 18), "Scoring RICE (Roadmap Estructural)" if lang == 'ES' else "RICE Scoring (Structural Roadmap)", fill=(6, 95, 70), font=f_step_title, anchor="mm")
    draw.text((rice_x + split_box_w // 2, cur_y + 38), "RICE = (R × I × C) / E • Persona-Mes • Densidad de Valor" if lang == 'ES' else "RICE = (R × I × C) / E • Person-Month • Value Density", fill=(4, 120, 87), font=f_step_desc, anchor="mm")

    # ICE Box
    draw.rounded_rectangle([(ice_x, cur_y), (ice_x + split_box_w, cur_y + split_h)], radius=7, fill=(254, 243, 199), outline=(245, 158, 11), width=2)
    draw.text((ice_x + split_box_w // 2, cur_y + 18), "Scoring ICE (Experimentos Growth)" if lang == 'ES' else "ICE Scoring (Growth Experiments)", fill=(146, 64, 14), font=f_step_title, anchor="mm")
    draw.text((ice_x + split_box_w // 2, cur_y + 38), "ICE = I × C × E (Escala 1-1.000) • Tests Quincenales" if lang == 'ES' else "ICE = I × C × E (Scale 1-1,000) • Bi-Weekly Sprints", fill=(180, 83, 9), font=f_step_desc, anchor="mm")

    # Merge arrows into Box 3
    cur_y += split_h
    merge_y = cur_y + branch_arrow_h // 2
    draw.line([(left_x, cur_y), (left_x, merge_y)], fill=(100, 116, 139), width=2)
    draw.line([(right_x, cur_y), (right_x, merge_y)], fill=(100, 116, 139), width=2)
    draw.line([(left_x, merge_y), (right_x, merge_y)], fill=(100, 116, 139), width=2)
    draw_arrow_down(draw, width // 2, merge_y, cur_y + branch_arrow_h, color=(100, 116, 139), width=2)
    cur_y += branch_arrow_h

    # 3. Matriz 2x2 Impacto vs Esfuerzo
    step3_title = "3. Matriz 2x2 Impacto vs. Esfuerzo" if lang == 'ES' else "3. 2x2 Impact vs. Effort Matrix"
    step3_desc = (
        "Segmentación analítica: Quick Wins (Q1 Now), Grandes Apuestas (Q2-Q3 Next), Rellenos y Pozos sin Fondo"
        if lang == 'ES' else
        "Analytical segmentation: Quick Wins (Q1 Now), Big Bets (Q2-Q3 Next), Fill-ins, and Costly Money Pits"
    )
    draw.rounded_rectangle([(box_x, cur_y), (box_x + box_w, cur_y + 52)], radius=7, fill=(239, 246, 255), outline=(37, 99, 235), width=2)
    draw.text((box_x + box_w // 2, cur_y + 17), step3_title, fill=(30, 64, 175), font=f_step_title, anchor="mm")
    draw.text((box_x + box_w // 2, cur_y + 36), step3_desc, fill=(37, 99, 235), font=f_step_desc, anchor="mm")

    # Arrow 3 -> 4
    cur_y += 52
    draw_arrow_down(draw, width // 2, cur_y, cur_y + arrow_len, color=(100, 116, 139), width=2)
    cur_y += arrow_len

    # 4. Línea de Corte de Capacidad (Cut-Line)
    step4_title = "4. Línea de Corte de Capacidad (Cut-Line)" if lang == 'ES' else "4. Capacity Cut-Line Framework"
    step4_desc = (
        "Capacidad neta de squads en Persona-Mes (buffer 16,7% blindado para deuda técnica y soporte)"
        if lang == 'ES' else
        "Net quarterly squad capacity in Person-Months (16.7% ring-fenced buffer for tech debt & bugs)"
    )
    draw.rounded_rectangle([(box_x, cur_y), (box_x + box_w, cur_y + 52)], radius=7, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
    draw.text((box_x + box_w // 2, cur_y + 17), step4_title, fill=(153, 27, 27), font=f_step_title, anchor="mm")
    draw.text((box_x + box_w // 2, cur_y + 36), step4_desc, fill=(220, 38, 38), font=f_step_desc, anchor="mm")

    # Arrow 4 -> 5
    cur_y += 52
    draw_arrow_down(draw, width // 2, cur_y, cur_y + arrow_len, color=(100, 116, 139), width=2)
    cur_y += arrow_len

    # 5. Asignación Now / Next / Later
    step5_title = "5. Asignación Now / Next / Later" if lang == 'ES' else "5. Now / Next / Later Allocation"
    step5_desc = (
        "Now (Q1 comprometido 30 PM) • Next (Q2-Q3 maduración) • Later / Congeladas (Pozos sin Fondo descartados)"
        if lang == 'ES' else
        "Now (Q1 committed 30 PM) • Next (Q2-Q3 discovery) • Later / Frozen (Disqualified Money Pits)"
    )
    draw.rounded_rectangle([(box_x, cur_y), (box_x + box_w, cur_y + 52)], radius=7, fill=(248, 250, 252), outline=(71, 85, 105), width=1)
    draw.text((box_x + box_w // 2, cur_y + 17), step5_title, fill=(15, 23, 42), font=f_step_title, anchor="mm")
    draw.text((box_x + box_w // 2, cur_y + 36), step5_desc, fill=(51, 65, 85), font=f_step_desc, anchor="mm")

    # Arrow 5 -> 6
    cur_y += 52
    draw_arrow_down(draw, width // 2, cur_y, cur_y + arrow_len, color=(100, 116, 139), width=2)
    cur_y += arrow_len

    # 6. Product Council Decision Gateway
    step6_title = "6. Product Council Decision Gateway" if lang == 'ES' else "6. Product Council Decision Gateway"
    step6_desc = (
        "Aprobación vinculante en Comité de Dirección (C-Level): Firmas formales de CEO, CPO, CTO y CFO"
        if lang == 'ES' else
        "Binding C-Level Executive Governance: Formal Sign-off from CEO, CPO, CTO and CFO"
    )
    draw.rounded_rectangle([(box_x, cur_y), (box_x + box_w, cur_y + 58)], radius=8, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.text((box_x + box_w // 2, cur_y + 19), step6_title, fill=(52, 211, 153), font=f_step_title, anchor="mm")
    draw.text((box_x + box_w // 2, cur_y + 40), step6_desc, fill=(241, 245, 249), font=f_step_desc, anchor="mm")

    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Diagrama 2 generado ({lang}): {out_path}")
    return out_path


# ==============================================================================
# DIAGRAMA 3: MATRIZ 2x2 IMPACTO VS ESFUERZO (CUADRANTES CARTESIANOS)
# ==============================================================================

def generate_diagram_3(lang='ES', out_path=None):
    width = 1120
    height = 760

    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/matriz-rice-ice-priorizacion/diagrama-3-matriz-impacto-esfuerzo.png"
        else:
            out_path = "content/en/posts/rice-ice-prioritization-matrix/diagram-3-impact-effort-matrix.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Marco exterior
    draw.rounded_rectangle([(10, 10), (width - 10, height - 10)], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

    # Fuentes
    f_title = get_font("segoeuib.ttf", 22)
    f_sub = get_font("segoeui.ttf", 13)
    f_axis = get_font("segoeuib.ttf", 12)
    f_badge = get_font("segoeuib.ttf", 13)
    f_item_id = get_font("segoeuib.ttf", 12)
    f_item_desc = get_font("segoeui.ttf", 11)
    f_kpi = get_font("segoeuib.ttf", 11)

    # Cabecera
    title_text = (
        "Matriz Estratégica: Valor Esperado vs. Esfuerzo & Distribución Cartesiana"
        if lang == 'ES' else
        "Strategic Matrix: Expected Value vs. Effort & Cartesian Backlog Distribution"
    )
    sub_text = (
        "Asignación Racional de Capacidad: Quick Wins, Grandes Apuestas, Rellenos y Pozos sin Fondo"
        if lang == 'ES' else
        "Rational Capacity Allocation: Quick Wins, Big Bets, Fill-ins, and Frozen Money Pits"
    )

    draw.text((width // 2, 38), title_text, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((width // 2, 64), sub_text, fill=(100, 116, 139), font=f_sub, anchor="mm")

    # Área de Cuadrantes 2x2
    grid_x0 = 65
    grid_y0 = 92
    grid_w = 990
    grid_h = 600

    quad_w = (grid_w - 20) // 2
    quad_h = (grid_h - 20) // 2

    # Coordenadas de los 4 cuadrantes
    tl_x = grid_x0
    tl_y = grid_y0

    tr_x = grid_x0 + quad_w + 20
    tr_y = grid_y0

    bl_x = grid_x0
    bl_y = grid_y0 + quad_h + 20

    br_x = grid_x0 + quad_w + 20
    br_y = grid_y0 + quad_h + 20

    # ==========================================================================
    # 1. TOP-LEFT: QUICK WINS (Alto Valor, Bajo Esfuerzo)
    # ==========================================================================
    draw.rounded_rectangle([(tl_x, tl_y), (tl_x + quad_w, tl_y + quad_h)], radius=10, fill=(240, 253, 244), outline=(16, 185, 129), width=2)
    badge_qw = "QUICK WINS — EJECUTAR YA (HORIZONTE NOW / Q1)" if lang == 'ES' else "QUICK WINS — EXECUTE NOW (HORIZON NOW / Q1)"
    draw.rounded_rectangle([(tl_x + 12, tl_y + 12), (tl_x + quad_w - 12, tl_y + 38)], radius=6, fill=(16, 185, 129))
    draw.text((tl_x + quad_w // 2, tl_y + 25), badge_qw, fill=(255, 255, 255), font=f_badge, anchor="mm")

    qw_items_es = [
        ("INIT-18: 2FA Obligatorio SMS/TOTP", "Valor: 50.000 | Esf: 1.5 PM | Score: 33.333"),
        ("INIT-15: NPS In-App Automatizado", "Valor: 25.000 | Esf: 1.0 PM | Score: 25.000"),
        ("INIT-03: Exportador Excel/PDF", "Valor: 22.000 | Esf: 1.0 PM | Score: 22.000"),
        ("INIT-05: Onboarding Interactivo", "Valor: 30.000 | Esf: 1.5 PM | Score: 20.000"),
        ("INIT-01: SSO Okta SAML", "Valor: 17.000 | Esf: 2.0 PM | Score: 8.500"),
    ]
    qw_items_en = [
        ("INIT-18: Mandatory SMS/TOTP 2FA", "Value: 50,000 | Effort: 1.5 PM | Score: 33,333"),
        ("INIT-15: Automated In-App NPS", "Value: 25,000 | Effort: 1.0 PM | Score: 25,000"),
        ("INIT-03: Excel/PDF Exporter", "Value: 22,000 | Effort: 1.0 PM | Score: 22,000"),
        ("INIT-05: Interactive Onboarding", "Value: 30,000 | Effort: 1.5 PM | Score: 20,000"),
        ("INIT-01: Enterprise Okta SSO", "Value: 17,000 | Effort: 2.0 PM | Score: 8,500"),
    ]
    qw_items = qw_items_es if lang == 'ES' else qw_items_en

    for idx, (it_title, it_desc) in enumerate(qw_items):
        iy = tl_y + 48 + idx * 39
        draw.ellipse([(tl_x + 18, iy + 4), (tl_x + 28, iy + 14)], fill=(16, 185, 129))
        draw.text((tl_x + 36, iy), it_title, fill=(6, 78, 59), font=f_item_id)
        draw.text((tl_x + 36, iy + 17), it_desc, fill=(4, 120, 87), font=f_item_desc)

    kpi_qw = "Captura el 54,2% del Valor Total del Backlog con solo 23,3% de Esfuerzo Neto" if lang == 'ES' else "Captures 54.2% of Total Backlog Value with only 23.3% Net Capacity"
    draw.rounded_rectangle([(tl_x + 12, tl_y + quad_h - 32), (tl_x + quad_w - 12, tl_y + quad_h - 10)], radius=5, fill=(209, 250, 229))
    draw.text((tl_x + quad_w // 2, tl_y + quad_h - 21), kpi_qw, fill=(6, 95, 70), font=f_kpi, anchor="mm")

    # ==========================================================================
    # 2. TOP-RIGHT: GRANDES APUESTAS (Alto Valor, Alto Esfuerzo)
    # ==========================================================================
    draw.rounded_rectangle([(tr_x, tr_y), (tr_x + quad_w, tr_y + quad_h)], radius=10, fill=(239, 246, 255), outline=(37, 99, 235), width=2)
    badge_bb = "GRANDES APUESTAS — PLANIFICAR (HORIZONTE NEXT / Q2-Q3)" if lang == 'ES' else "BIG BETS — STRATEGIC DISCOVERY (HORIZON NEXT / Q2-Q3)"
    draw.rounded_rectangle([(tr_x + 12, tr_y + 12), (tr_x + quad_w - 12, tr_y + 38)], radius=6, fill=(37, 99, 235))
    draw.text((tr_x + quad_w // 2, tr_y + 25), badge_bb, fill=(255, 255, 255), font=f_badge, anchor="mm")

    bb_items_es = [
        ("INIT-02: Copilot IA de Flujo de Trabajo", "Valor: 43.200 | Esf: 6.0 PM | Score: 7.200"),
        ("INIT-04: Constructor Dashboards BI", "Valor: 19.200 | Esf: 5.5 PM | Score: 3.490"),
        ("INIT-11: RBAC Roles Avanzados Teams", "Valor: 10.500 | Esf: 5.0 PM | Score: 2.100"),
        ("INIT-07: Motor Recomendaciones IA", "Valor: 12.600 | Esf: 4.5 PM | Score: 2.800"),
    ]
    bb_items_en = [
        ("INIT-02: Workflow AI Copilot", "Value: 43,200 | Effort: 6.0 PM | Score: 7,200"),
        ("INIT-04: Custom BI Dashboard Builder", "Value: 19,200 | Effort: 5.5 PM | Score: 3,490"),
        ("INIT-11: Enterprise RBAC Teams", "Value: 10,500 | Effort: 5.0 PM | Score: 2,100"),
        ("INIT-07: AI Recommendation Engine", "Value: 12,600 | Effort: 4.5 PM | Score: 2,800"),
    ]
    bb_items = bb_items_es if lang == 'ES' else bb_items_en

    for idx, (it_title, it_desc) in enumerate(bb_items):
        iy = tr_y + 52 + idx * 43
        draw.ellipse([(tr_x + 18, iy + 4), (tr_x + 28, iy + 14)], fill=(37, 99, 235))
        draw.text((tr_x + 36, iy), it_title, fill=(30, 58, 138), font=f_item_id)
        draw.text((tr_x + 36, iy + 17), it_desc, fill=(37, 99, 235), font=f_item_desc)

    kpi_bb = "Épicas de plataforma que exigen discovery técnico previo" if lang == 'ES' else "Platform epics requiring upfront technical discovery & spikes"
    draw.rounded_rectangle([(tr_x + 12, tr_y + quad_h - 32), (tr_x + quad_w - 12, tr_y + quad_h - 10)], radius=5, fill=(219, 234, 254))
    draw.text((tr_x + quad_w // 2, tr_y + quad_h - 21), kpi_bb, fill=(30, 64, 175), font=f_kpi, anchor="mm")

    # ==========================================================================
    # 3. BOTTOM-LEFT: RELLENOS (Bajo Valor, Bajo Esfuerzo)
    # ==========================================================================
    draw.rounded_rectangle([(bl_x, bl_y), (bl_x + quad_w, bl_y + quad_h)], radius=10, fill=(248, 250, 252), outline=(100, 116, 139), width=2)
    badge_fi = "RELLENOS — ABSORBER HOLGURAS (SLACK)" if lang == 'ES' else "FILL-INS — ABSORB SPRINT SLACK"
    draw.rounded_rectangle([(bl_x + 12, bl_y + 12), (bl_x + quad_w - 12, bl_y + 38)], radius=6, fill=(100, 116, 139))
    draw.text((bl_x + quad_w // 2, bl_y + 25), badge_fi, fill=(255, 255, 255), font=f_badge, anchor="mm")

    fi_items_es = [
        ("INIT-10: Modo Oscuro Completo", "Valor: 10.000 | Esf: 2.0 PM | Score: 5.000"),
        ("INIT-17: Email Programado de Reportes", "Valor: 1.800 | Esf: 1.0 PM | Score: 1.800"),
        ("INIT-16: Selector de Idioma Manual", "Valor: 900 | Esf: 1.0 PM | Score: 900"),
        ("INIT-12: Atajos de Teclado", "Valor: 1.800 | Esf: 1.0 PM | Score: 1.800"),
    ]
    fi_items_en = [
        ("INIT-10: Complete Dark Mode", "Value: 10,000 | Effort: 2.0 PM | Score: 5,000"),
        ("INIT-17: Scheduled Email Reports", "Value: 1,800 | Effort: 1.0 PM | Score: 1,800"),
        ("INIT-16: Manual Language Selector", "Value: 900 | Effort: 1.0 PM | Score: 900"),
        ("INIT-12: Power-User Shortcuts", "Value: 1,800 | Effort: 1.0 PM | Score: 1,800"),
    ]
    fi_items = fi_items_es if lang == 'ES' else fi_items_en

    for idx, (it_title, it_desc) in enumerate(fi_items):
        iy = bl_y + 52 + idx * 43
        draw.ellipse([(bl_x + 18, iy + 4), (bl_x + 28, iy + 14)], fill=(100, 116, 139))
        draw.text((bl_x + 36, iy), it_title, fill=(30, 41, 59), font=f_item_id)
        draw.text((bl_x + 36, iy + 17), it_desc, fill=(71, 85, 105), font=f_item_desc)

    kpi_fi = "Tareas de amortiguador entre sprints para no desviar foco" if lang == 'ES' else "Sprint buffer tasks to absorb slack without derailing roadmap"
    draw.rounded_rectangle([(bl_x + 12, bl_y + quad_h - 32), (bl_x + quad_w - 12, bl_y + quad_h - 10)], radius=5, fill=(226, 232, 240))
    draw.text((bl_x + quad_w // 2, bl_y + quad_h - 21), kpi_fi, fill=(51, 65, 85), font=f_kpi, anchor="mm")

    # ==========================================================================
    # 4. BOTTOM-RIGHT: POZOS SIN FONDO (Bajo Valor, Alto Esfuerzo)
    # ==========================================================================
    draw.rounded_rectangle([(br_x, br_y), (br_x + quad_w, br_y + quad_h)], radius=10, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
    badge_mp = "POZOS SIN FONDO — CONGELAR O DESCARTAR (LATER)" if lang == 'ES' else "MONEY PITS — FREEZE OR REJECT (LATER)"
    draw.rounded_rectangle([(br_x + 12, br_y + 12), (br_x + quad_w - 12, br_y + 38)], radius=6, fill=(239, 68, 68))
    draw.text((br_x + quad_w // 2, br_y + 25), badge_mp, fill=(255, 255, 255), font=f_badge, anchor="mm")

    mp_items_es = [
        ("INIT-14: Capa GraphQL Microservicios", "Valor: 1.500 | Esf: 7.0 PM | Score: 214"),
        ("INIT-19: Reescritura BD a Rust", "Valor: 1.250 | Esf: 14.0 PM | Score: 89"),
        ("INIT-20: Red Social Interna Clientes", "Valor: 960 | Esf: 8.0 PM | Score: 120"),
    ]
    mp_items_en = [
        ("INIT-14: GraphQL Microservices Layer", "Value: 1,500 | Effort: 7.0 PM | Score: 214"),
        ("INIT-19: Full DB Rewrite to Rust", "Value: 1,250 | Effort: 14.0 PM | Score: 89"),
        ("INIT-20: Internal Customer Social Feed", "Value: 960 | Effort: 8.0 PM | Score: 120"),
    ]
    mp_items = mp_items_es if lang == 'ES' else mp_items_en

    for idx, (it_title, it_desc) in enumerate(mp_items):
        iy = br_y + 56 + idx * 46
        draw.ellipse([(br_x + 18, iy + 4), (br_x + 28, iy + 14)], fill=(239, 68, 68))
        draw.text((br_x + 36, iy), it_title, fill=(153, 27, 27), font=f_item_id)
        draw.text((br_x + 36, iy + 17), it_desc, fill=(185, 28, 28), font=f_item_desc)

    kpi_mp = "CONGELAR: Ahorro de 21 Persona-Mes de ingeniería al erradicar purismos" if lang == 'ES' else "FREEZE: 21 Person-Months saved by eliminating low-ROI tech purism"
    draw.rounded_rectangle([(br_x + 12, br_y + quad_h - 32), (br_x + quad_w - 12, br_y + quad_h - 10)], radius=5, fill=(254, 202, 202))
    draw.text((br_x + quad_w // 2, br_y + quad_h - 21), kpi_mp, fill=(153, 27, 27), font=f_kpi, anchor="mm")

    # ==========================================================================
    # EJES CARTESIANOS Y ETIQUETAS (LIMPIOS Y SIN RECORTE)
    # ==========================================================================
    # Eje X inferior
    axis_x_text = "ESFUERZO DE INGENIERÍA (Persona-Mes)" if lang == 'ES' else "ENGINEERING EFFORT (Person-Months)"
    ax_y = height - 34
    draw.text((width // 2 - 20, ax_y), axis_x_text, fill=(71, 85, 105), font=f_axis, anchor="mm")
    draw_arrow_right(draw, width // 2 + 130, width // 2 + 180, ax_y, color=(71, 85, 105), width=2)

    # Eje Y vertical a la izquierda
    y_axis_text = "VALOR ESPERADO (Reach x Impact x Confidence)" if lang == 'ES' else "EXPECTED VALUE (Reach x Impact x Confidence)"
    lbl_w = 420
    lbl_h = 32
    lbl_img = Image.new('RGBA', (lbl_w, lbl_h), (255, 255, 255, 0))
    lbl_draw = ImageDraw.Draw(lbl_img)
    lbl_draw.text((lbl_w // 2 - 15, lbl_h // 2), y_axis_text, fill=(71, 85, 105), font=f_axis, anchor="mm")
    draw_arrow_right(lbl_draw, lbl_w // 2 + 155, lbl_w // 2 + 195, lbl_h // 2, color=(71, 85, 105), width=2)

    rot_img = lbl_img.rotate(90, expand=True)
    paste_x = 18
    paste_y = grid_y0 + (grid_h - rot_img.height) // 2
    img.paste(rot_img, (paste_x, paste_y), rot_img)

    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Diagrama 3 generado ({lang}): {out_path}")
    return out_path


def main():
    print("======================================================================")
    print("GENERANDO DIAGRAMAS DE LA MATRIZ RICE & ICE ÁGIL (ES Y EN)")
    print("======================================================================")

    # Diagrama 1: Embudo
    generate_diagram_1(lang='ES')
    generate_diagram_1(lang='EN')

    # Diagrama 2: Pipeline
    generate_diagram_2(lang='ES')
    generate_diagram_2(lang='EN')

    # Diagrama 3: Cuadrantes
    generate_diagram_3(lang='ES')
    generate_diagram_3(lang='EN')

    print("======================================================================")
    print("¡LOS 3 DIAGRAMAS BILINGÜES HAN SIDO GENERADOS CON ÉXITO!")
    print("======================================================================")


if __name__ == "__main__":
    main()
