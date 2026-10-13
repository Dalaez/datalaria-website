#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) para el Post Pilar Maestro de la Suite 02:
- content/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/cover.png
- content/en/posts/decision-making-prioritization-quantitative-framework/cover.png

Composición visual de estándar McKinsey / C-Suite / Corporate Board:
- Fondo Dark Slate (#0B1120 a #0F172A y #1E293B) con degradado suave y malla técnica de decisión.
- Embudo gráfico de 3 Niveles interconectados:
  * Nivel 1: Matriz DAR (Filtros Veto & Ponderación Multicriterio)
  * Nivel 2: Matriz RICE & ICE (Densidad de Valor & Línea de Corte)
  * Nivel 3: Business Case DCF (VAN, TIR, WACC & Gráfico Tornado)
- Badge superior corporativo: DATALARIA EXECUTIVE FRAMEWORK • SUITE 02 MEGA BUNDLE
- Título de alto contraste y subtítulo ejecutivo.
- Balas de valor estratégico con viñetas destacadas.
- Píldoras de entregables: [📊 6 Modelos Excel/Sheets] [📑 6 Decks PPTX 16:9] [📄 3 Guías PDF].
- Badge de precio y acceso: 15€ (Ahorro 25% • Original 20€).
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 630


def get_font(name, size):
    """Carga fuente TrueType del sistema o fallback predeterminado."""
    font_paths = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
        f"C:/Windows/Fonts/{name.replace('b', '')}",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_linear_gradient(draw, width, height, start_color, end_color):
    """Pinta un degradado diagonal suave en la imagen."""
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    for y in range(height):
        ratio_y = y / height
        for x in range(0, width, 2):
            ratio_x = x / width
            blend = (ratio_x * 0.4 + ratio_y * 0.6)
            r = int(r1 + (r2 - r1) * blend)
            g = int(g1 + (g2 - g1) * blend)
            b = int(b1 + (b2 - b1) * blend)
            draw.line([(x, y), (x + 1, y)], fill=(r, g, b))


def draw_technical_grid(draw, width, height):
    """Dibuja una malla técnica con cuadrículas y cruces de alineación sutiles."""
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(18, 28, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(18, 28, 48), width=1)

    # Intersecciones sutiles cada 120px
    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_decision_funnel(draw, center_x, center_y, font_bold, font_small, font_tiny, lang='ES'):
    """Dibuja el embudo visual jerárquico de 3 niveles con conectores y métricas."""
    
    tiers = [
        {
            "num": "TIER 1",
            "name": "MATRIZ DAR",
            "role": "Veto Gates & Multi-Criteria" if lang == 'EN' else "Filtros Veto & Ponderación",
            "metric": "V_k = 1  |  S_j = Σ w_i · s_ij",
            "col_border": (16, 185, 129),   # Emerald
            "col_bg": (15, 23, 42),
            "col_badge": (52, 211, 153),
            "width": 380,
            "y": center_y - 145
        },
        {
            "num": "TIER 2",
            "name": "RICE & ICE",
            "role": "Value Density & Cut-Line" if lang == 'EN' else "Densidad Valor & Corte",
            "metric": "RICE = (R · I · C) / E",
            "col_border": (59, 130, 246),   # Blue
            "col_bg": (15, 23, 42),
            "col_badge": (96, 165, 250),
            "width": 330,
            "y": center_y
        },
        {
            "num": "TIER 3",
            "name": "BUSINESS CASE",
            "role": "DCF Capex & Tornado Risk" if lang == 'EN' else "VAN, TIR & Gráfico Tornado",
            "metric": "NPV = -I_0 + Σ FCF_t/(1+WACC)^t" if lang == 'EN' else "VAN = -I_0 + Σ CF_t/(1+WACC)^t",
            "col_border": (245, 158, 11),   # Amber
            "col_bg": (15, 23, 42),
            "col_badge": (251, 191, 36),
            "width": 280,
            "y": center_y + 145
        }
    ]

    card_h = 76

    # Líneas y formas de embudo de fondo
    t1 = tiers[0]
    t2 = tiers[1]
    t3 = tiers[2]

    # Embudo trapezoidal translúcido / guías de flujo
    p1_l = (center_x - t1["width"] // 2 - 15, t1["y"] + card_h // 2)
    p1_r = (center_x + t1["width"] // 2 + 15, t1["y"] + card_h // 2)
    p3_l = (center_x - t3["width"] // 2 - 15, t3["y"] + card_h // 2)
    p3_r = (center_x + t3["width"] // 2 + 15, t3["y"] + card_h // 2)

    draw.line([p1_l, p3_l], fill=(30, 58, 138), width=2)
    draw.line([p1_r, p3_r], fill=(30, 58, 138), width=2)

    # Conectores de flujo verticales con flechas estilizadas
    for i in range(2):
        from_y = tiers[i]["y"] + card_h
        to_y = tiers[i + 1]["y"]
        mid_y = (from_y + to_y) // 2

        # Líneas verticales
        draw.line([(center_x, from_y), (center_x, to_y)], fill=(56, 189, 248), width=2)

        # Rombo de decisión intermedio
        rw = 12
        draw.polygon([
            (center_x, mid_y - rw),
            (center_x + rw, mid_y),
            (center_x, mid_y + rw),
            (center_x - rw, mid_y)
        ], fill=(30, 41, 59), outline=(56, 189, 248))

    # Dibujar las 3 tarjetas de nivel
    for tier in tiers:
        w = tier["width"]
        h = card_h
        x1 = center_x - w // 2
        y1 = tier["y"]
        x2 = center_x + w // 2
        y2 = y1 + h

        # Sombra sutil
        draw.rounded_rectangle([(x1 + 4, y1 + 4), (x2 + 4, y2 + 4)], radius=8, fill=(10, 15, 28))

        # Tarjeta principal
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=8, fill=tier["col_bg"], outline=tier["col_border"], width=2)

        # Badge lateral (TIER X)
        badge_w = 64
        draw.rounded_rectangle([(x1 + 10, y1 + 12), (x1 + 10 + badge_w, y1 + 34)], radius=4, fill=(30, 41, 59), outline=tier["col_border"], width=1)
        b_txt = tier["num"]
        bbox_b = font_small.getbbox(b_txt)
        bw_txt = bbox_b[2] - bbox_b[0]
        draw.text((x1 + 10 + (badge_w - bw_txt) // 2, y1 + 16), b_txt, fill=tier["col_badge"], font=font_small)

        # Título de la herramienta
        t_name = tier["name"]
        draw.text((x1 + 86, y1 + 14), t_name, fill=(255, 255, 255), font=font_bold)

        # Subtítulo de función
        draw.text((x1 + 86, y1 + 33), tier["role"], fill=(148, 163, 184), font=font_small)

        # Barra inferior con fórmula / métrica algorítmica
        formula_box_y1 = y1 + 50
        draw.rounded_rectangle([(x1 + 10, formula_box_y1), (x2 - 10, formula_box_y1 + 18)], radius=3, fill=(18, 28, 48))
        f_txt = tier["metric"]
        draw.text((x1 + 18, formula_box_y1 + 2), f_txt, fill=(56, 189, 248), font=font_tiny)

    # Indicador de flujo a la derecha de las tarjetas
    status_x = center_x + t1["width"] // 2 + 35
    if status_x < WIDTH - 40:
        labels = [
            ("1. SELECT", "Filtro Arquitectura") if lang == 'ES' else ("1. SELECT", "Architecture Filter"),
            ("2. PRIORITIZE", "Línea de Corte") if lang == 'ES' else ("2. PRIORITIZE", "Backlog Cut-Line"),
            ("3. JUSTIFY", "Aprobación CFO") if lang == 'ES' else ("3. JUSTIFY", "CFO Board Sign-Off")
        ]
        for i, (l_top, l_bot) in enumerate(labels):
            ly = tiers[i]["y"] + 15
            draw.text((status_x, ly), l_top, fill=(245, 158, 11), font=font_tiny)
            draw.text((status_x, ly + 14), l_bot, fill=(203, 213, 225), font=font_tiny)


def create_cover(lang='ES', out_path='cover.png'):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado Slate Dark
    draw_linear_gradient(draw, WIDTH, HEIGHT, (11, 17, 32), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # 3. Fuentes
    font_badge = get_font("segoeuib.ttf", 11)
    font_title_large = get_font("segoeuib.ttf", 36)
    font_subtitle = get_font("segoeui.ttf", 15)
    font_bullet_title = get_font("segoeuib.ttf", 13)
    font_bullet_desc = get_font("segoeui.ttf", 12)
    font_pill = get_font("segoeuib.ttf", 11)
    font_tier_bold = get_font("segoeuib.ttf", 13)
    font_tier_small = get_font("segoeuib.ttf", 10)
    font_tier_tiny = get_font("segoeui.ttf", 9)
    font_price_main = get_font("segoeuib.ttf", 22)
    font_price_strike = get_font("segoeui.ttf", 13)

    # 4. Badge Superior Corporativo
    badge_text = "DATALARIA EXECUTIVE FRAMEWORK • SUITE 02 MEGA BUNDLE"
    b_x, b_y = 60, 42
    b_w, b_h = 475, 28
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text((b_x + 14, b_y + 6), badge_text, fill=(56, 189, 248), font=font_badge)

    # 5. Título Principal
    t_y = 88
    if lang == 'ES':
        title_p1 = "TOMA DE DECISIONES & "
        title_p2 = "PRIORIZACIÓN"
    else:
        title_p1 = "DECISION-MAKING & "
        title_p2 = "PRIORITIZATION"

    draw.text((60, t_y), title_p1, fill=(255, 255, 255), font=font_title_large)
    bbox_p1 = font_title_large.getbbox(title_p1)
    p1_width = bbox_p1[2] - bbox_p1[0]
    draw.text((60 + p1_width, t_y), title_p2, fill=(245, 158, 11), font=font_title_large)

    # 6. Subtítulo
    sub_y = 144
    subtitle = (
        "El Framework Cuantitativo de 3 Niveles: Matriz DAR, RICE/ICE & Business Case"
        if lang == 'ES' else
        "The 3-Tier Quantitative Framework: DAR Matrix, RICE/ICE & Business Case"
    )
    draw.text((60, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle)

    # Línea decorativa horizontal
    draw.line([(60, 178), (590, 178)], fill=(37, 99, 235), width=2)

    # 7. Balas de valor estratégico
    bullets = [
        (
            "Nivel 1: Filtros Veto & CMMI DAR (Must-Haves)",
            "Exclusión booleana implacable y scoring multicriterio para arquitecturas y RFPs"
        ) if lang == 'ES' else (
            "Tier 1: Boolean Veto Gates & CMMI DAR (Must-Haves)",
            "Uncompromising binary hurdles and multi-criteria scoring for vendors & tech fit"
        ),
        (
            "Nivel 2: Backlog RICE & Capacidad Neta de Squads",
            "Maximiza el valor por unidad de esfuerzo con línea de corte automática (Knapsack)"
        ) if lang == 'ES' else (
            "Tier 2: RICE Backlog & Net Squad Capacity Cut-Line",
            "Maximizes value density per unit of effort with automated greedy knapsack cut-off"
        ),
        (
            "Nivel 3: Business Case Financiero DCF ante el CFO",
            "Defiende el CAPEX con VAN, TIR, Payback descontado y análisis de riesgo Tornado"
        ) if lang == 'ES' else (
            "Tier 3: Institutional DCF Business Case for the CFO",
            "Secures capital approval with NPV, IRR, discounted payback, and Tornado sensitivity"
        )
    ]

    bullet_start_y = 196
    spacing_y = 66
    for i, (btitle, bdesc) in enumerate(bullets):
        by = bullet_start_y + i * spacing_y

        # Viñeta cuadrada con gradiente/color
        col_accent = [(16, 185, 129), (59, 130, 246), (245, 158, 11)][i]
        draw.rounded_rectangle([(60, by + 2), (72, by + 14)], radius=2, fill=col_accent)

        draw.text((82, by), btitle, fill=(255, 255, 255), font=font_bullet_title)
        draw.text((82, by + 19), bdesc, fill=(148, 163, 184), font=font_bullet_desc)

    # 8. Píldoras de Entregables
    pills_y = 415
    pills = [
        ("📊 6 Modelos Excel/Sheets" if lang == 'ES' else "📊 6 Excel/Sheets Models", (30, 41, 59), (56, 189, 248)),
        ("📑 6 Decks PPTX 16:9" if lang == 'ES' else "📑 6 PPTX 16:9 Decks", (30, 41, 59), (167, 139, 250)),
        ("📄 3 Guías PDF" if lang == 'ES' else "📄 3 PDF Guides", (30, 41, 59), (52, 211, 153))
    ]

    curr_px = 60
    for ptext, bgcol, bordercol in pills:
        bbox_p = font_pill.getbbox(ptext)
        pw = bbox_p[2] - bbox_p[0] + 24
        ph = 30
        draw.rounded_rectangle([(curr_px, pills_y), (curr_px + pw, pills_y + ph)], radius=6, fill=bgcol, outline=bordercol, width=1)
        draw.text((curr_px + 12, pills_y + 7), ptext, fill=(255, 255, 255), font=font_pill)
        curr_px += pw + 12

    # 9. Bloque de Precio y Garantía
    cta_box_y = 470
    cta_w, cta_h = 510, 84
    draw.rounded_rectangle([(60, cta_box_y), (60 + cta_w, cta_box_y + cta_h)], radius=10, fill=(15, 23, 42), outline=(37, 99, 235), width=2)

    # Precio
    draw.text((80, cta_box_y + 14), "15€", fill=(245, 158, 11), font=font_price_main)

    # Precio tachado y ahorro
    strike_txt = "Valor individual: 20€" if lang == 'ES' else "Individual value: 20€"
    draw.text((140, cta_box_y + 16), strike_txt, fill=(148, 163, 184), font=font_price_strike)
    bbox_st = font_price_strike.getbbox(strike_txt)
    st_w = bbox_st[2] - bbox_st[0]
    draw.line([(140, cta_box_y + 24), (140 + st_w, cta_box_y + 24)], fill=(239, 68, 68), width=1)

    # Badge de ahorro
    savings_badge = "Ahorro 25%" if lang == 'ES' else "25% Savings"
    draw.rounded_rectangle([(140 + st_w + 12, cta_box_y + 14), (140 + st_w + 12 + 82, cta_box_y + 32)], radius=4, fill=(16, 185, 129))
    draw.text((140 + st_w + 20, cta_box_y + 16), savings_badge, fill=(255, 255, 255), font=font_tier_small)

    # Subtexto de garantía
    trust_txt = "Descarga directa inmediata (.ZIP) • Modelos 100% desbloqueados y listos para Comité" if lang == 'ES' else "Instant direct download (.ZIP) • 100% unlocked models ready for Boardroom review"
    draw.text((80, cta_box_y + 48), trust_txt, fill=(203, 213, 225), font=font_tier_small)

    # 10. Dibujar el Embudo Cuantitativo a la derecha
    funnel_center_x = 880
    funnel_center_y = 315
    draw_decision_funnel(draw, funnel_center_x, funnel_center_y, font_tier_bold, font_tier_small, font_tier_tiny, lang=lang)

    # Guardar imagen optimizada
    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Portada generada con éxito: {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    es_path = os.path.join(base_dir, "content", "es", "posts", "toma-decisiones-priorizacion-framework-cuantitativo", "cover.png")
    en_path = os.path.join(base_dir, "content", "en", "posts", "decision-making-prioritization-quantitative-framework", "cover.png")

    create_cover(lang='ES', out_path=es_path)
    create_cover(lang='EN', out_path=en_path)
