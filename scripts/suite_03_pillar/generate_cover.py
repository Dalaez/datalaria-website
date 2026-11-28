#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) con Safe Zone estricta [145, 1055] para el
Post Pilar Maestro de la Suite 03:
- content/es/posts/control-operativo-pmbok-framework-cuantitativo/cover.png
- content/en/posts/operational-control-pmbok-quantitative-framework/cover.png

Reglas visuales:
- Toda tipografía, píldora, precio y tarjeta de pilar queda dentro de x=[145, 1055]
  y y=[38, 592] para evitar cualquier recorte en fichas PaperMod y OpenGraph.
- Cero solapamiento entre la columna izquierda (x=145..635) y las 5 tarjetas
  verticales de los pilares (x=665..1055).
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 630
SAFE_LEFT = 145
SAFE_RIGHT = 1055


def get_font(name, size):
    """Carga fuente TrueType del sistema o fallback predeterminado."""
    font_paths = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
        f"C:/Windows/Fonts/{name.replace('b', '')}",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, int(size))
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
            blend = ratio_x * 0.35 + ratio_y * 0.65
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

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_engineering_curves(draw, center_x, center_y):
    """Dibuja trazados sutiles de Curva S y Diente de Sierra en el fondo derecho."""
    s_points = []
    start_x = center_x - 190
    end_x = center_x + 190
    base_y = center_y + 135
    top_y = center_y - 195

    for px in range(start_x, end_x, 4):
        t = (px - start_x) / (end_x - start_x)
        sig = 1 / (1 + math.exp(-7 * (t - 0.5)))
        py = int(base_y - sig * (base_y - top_y))
        s_points.append((px, py))

    for i in range(len(s_points) - 1):
        draw.line([s_points[i], s_points[i + 1]], fill=(30, 58, 110), width=3)

    saw_y_base = center_y + 230
    saw_y_top = center_y + 185
    saw_x_start = center_x - 160
    saw_x_end = center_x + 175
    saw_cycle = 67

    cx = saw_x_start
    while cx < saw_x_end:
        next_drop = min(cx + saw_cycle, saw_x_end)
        draw.line([(cx, saw_y_top), (next_drop, saw_y_base)], fill=(76, 29, 149), width=2)
        if next_drop < saw_x_end:
            draw.line([(next_drop, saw_y_base), (next_drop, saw_y_top)], fill=(88, 28, 135), width=2)
        cx = next_drop


def draw_5_pillars(draw, center_x, center_y, font_bold, font_small, font_tiny, lang="ES"):
    """Dibuja las 5 tarjetas de los pilares estrictamente dentro de x=[665, 1055]."""
    card_w = 376
    card_h = 72
    spacing = 18
    total_h = 5 * card_h + 4 * spacing  # 432 px
    start_y = center_y - (total_h // 2)

    pillars = [
        {
            "num": "P1",
            "tag": "GOVERNANCE",
            "name": "RACI MATRIX" if lang == "EN" else "MATRIZ RACI",
            "role": "Governance & Workload" if lang == "EN" else "Gobernanza & Carga",
            "metric": "A = 1  |  W_k = Sum(w_x · X_ik)",
            "col_border": (16, 185, 129),
            "col_bg": (15, 23, 42),
            "col_badge": (52, 211, 153),
            "y": start_y,
        },
        {
            "num": "P2",
            "tag": "RELIABILITY",
            "name": "FMEA / AMFE" if lang == "EN" else "AMFE / FMEA",
            "role": "Risk & RPN Priority" if lang == "EN" else "Prevención & NPR",
            "metric": "RPN = S x O x D  (ISO 31000)" if lang == "EN" else "NPR = S x O x D  (ISO 31000)",
            "col_border": (244, 63, 94),
            "col_bg": (15, 23, 42),
            "col_badge": (251, 113, 133),
            "y": start_y + (card_h + spacing) * 1,
        },
        {
            "num": "P3",
            "tag": "SCHEDULE",
            "name": "3-POINT PERT" if lang == "EN" else "PERT 3 PUNTOS",
            "role": "Beta Timeline & Buffers" if lang == "EN" else "Cronograma Beta & Buffers",
            "metric": "mu = (o + 4m + p)/6  |  Z-Score",
            "col_border": (59, 130, 246),
            "col_bg": (15, 23, 42),
            "col_badge": (96, 165, 250),
            "y": start_y + (card_h + spacing) * 2,
        },
        {
            "num": "P4",
            "tag": "FINANCIALS",
            "name": "EVM S-CURVE" if lang == "EN" else "EVM CURVA S",
            "role": "Earned Value & EAC" if lang == "EN" else "Valor Ganado & EAC",
            "metric": "CPI = EV/AC  |  EAC = BAC/CPI",
            "col_border": (245, 158, 11),
            "col_bg": (15, 23, 42),
            "col_badge": (251, 191, 36),
            "y": start_y + (card_h + spacing) * 3,
        },
        {
            "num": "P5",
            "tag": "INVENTORY",
            "name": "SAFETY STOCK & ROP" if lang == "EN" else "STOCK SEGURIDAD ROP",
            "role": "Working Capital & SLA" if lang == "EN" else "Circulante & Nivel Servicio",
            "metric": "SS = Z · sqrt(L·sigma_d^2 + d^2·sigma_L^2)",
            "col_border": (168, 85, 247),
            "col_bg": (15, 23, 42),
            "col_badge": (192, 132, 252),
            "y": start_y + (card_h + spacing) * 4,
        },
    ]

    for i in range(len(pillars) - 1):
        y1 = pillars[i]["y"] + card_h
        y2 = pillars[i + 1]["y"]
        draw.line([(center_x, y1), (center_x, y2)], fill=(56, 189, 248), width=2)
        draw.polygon(
            [(center_x, y2), (center_x - 4, y2 - 6), (center_x + 4, y2 - 6)],
            fill=(56, 189, 248),
        )

    for p in pillars:
        x1 = center_x - card_w // 2
        y1 = p["y"]
        x2 = center_x + card_w // 2
        y2 = y1 + card_h
        assert SAFE_LEFT <= x1 and x2 <= SAFE_RIGHT, f"Card out of safe zone: {x1}..{x2}"

        draw.rounded_rectangle([(x1 + 3, y1 + 3), (x2 + 3, y2 + 3)], radius=8, fill=(10, 15, 28))
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=8, fill=p["col_bg"], outline=p["col_border"], width=2)

        badge_w = 38
        draw.rounded_rectangle(
            [(x1 + 10, y1 + 10), (x1 + 10 + badge_w, y1 + 31)],
            radius=4,
            fill=(30, 41, 59),
            outline=p["col_border"],
            width=1,
        )
        b_txt = p["num"]
        bbox_b = font_small.getbbox(b_txt)
        bw_txt = bbox_b[2] - bbox_b[0]
        draw.text((x1 + 10 + (badge_w - bw_txt) // 2, y1 + 13), b_txt, fill=p["col_badge"], font=font_small)

        draw.text((x1 + 58, y1 + 9), p["name"], fill=(255, 255, 255), font=font_bold)
        draw.text((x1 + 58, y1 + 26), p["role"], fill=(148, 163, 184), font=font_small)

        # Compact stage label integrated inside right edge of card (stays inside SAFE_RIGHT)
        tag_box = font_tiny.getbbox(p["tag"])
        tw = tag_box[2] - tag_box[0] + 12
        draw.rounded_rectangle(
            [(x2 - tw - 10, y1 + 10), (x2 - 10, y1 + 25)],
            radius=3,
            fill=(24, 34, 53),
        )
        draw.text((x2 - tw - 4, y1 + 11), p["tag"], fill=(245, 158, 11), font=font_tiny)

        formula_y1 = y1 + 46
        draw.rounded_rectangle([(x1 + 10, formula_y1), (x2 - 10, formula_y1 + 18)], radius=3, fill=(18, 28, 48))
        draw.text((x1 + 18, formula_y1 + 2), p["metric"], fill=(56, 189, 248), font=font_tiny)


def create_cover(lang="ES", out_path="cover.png"):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    draw_linear_gradient(draw, WIDTH, HEIGHT, (11, 17, 32), (30, 41, 59))
    draw_technical_grid(draw, WIDTH, HEIGHT)

    pillar_center_x = 865  # 376px width => x=677..1053 (strictly inside [145, 1055])
    pillar_center_y = 310
    draw_engineering_curves(draw, pillar_center_x, pillar_center_y)

    font_badge = get_font("segoeuib.ttf", 10.5)
    font_title_large = get_font("segoeuib.ttf", 30)
    font_subtitle = get_font("segoeui.ttf", 12)
    font_bullet_title = get_font("segoeuib.ttf", 12)
    font_bullet_desc = get_font("segoeui.ttf", 10.5)
    font_pill = get_font("segoeuib.ttf", 10.5)
    font_tier_bold = get_font("segoeuib.ttf", 11.5)
    font_tier_small = get_font("segoeuib.ttf", 9.5)
    font_tier_tiny = get_font("segoeui.ttf", 8.5)
    font_price_main = get_font("segoeuib.ttf", 21)
    font_price_strike = get_font("segoeui.ttf", 12)

    # 1. Badge Superior Corporativo (x=145..580)
    badge_text = "DATALARIA EXECUTIVE FRAMEWORK • SUITE 03 MEGA BUNDLE"
    b_box = font_badge.getbbox(badge_text)
    b_w = (b_box[2] - b_box[0]) + 24
    b_x, b_y, b_h = SAFE_LEFT, 42, 24
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=5, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text((b_x + 12, b_y + 4), badge_text, fill=(56, 189, 248), font=font_badge)

    # 2. Título Principal en 2 Líneas (x=145..585 — ~90px claro hasta las tarjetas x=677)
    t_y1, t_y2 = 80, 118
    if lang == "ES":
        title_line1 = "CONTROL OPERATIVO &"
        title_line2 = "MÉTRICAS PMBOK"
    else:
        title_line1 = "OPERATIONAL CONTROL &"
        title_line2 = "PMBOK METRICS"

    draw.text((SAFE_LEFT, t_y1), title_line1, fill=(255, 255, 255), font=font_title_large)
    draw.text((SAFE_LEFT, t_y2), title_line2, fill=(245, 158, 11), font=font_title_large)

    # 3. Subtítulo Ejecutivo
    sub_y = 164
    subtitle = (
        "Framework Cuantitativo de 5 Pilares: RACI, AMFE, PERT, EVM & ROP"
        if lang == "ES" else
        "5-Pillar Quantitative Engine: RACI, FMEA, PERT, EVM & Safety Stock"
    )
    draw.text((SAFE_LEFT, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle)

    draw.line([(SAFE_LEFT, 192), (615, 192)], fill=(37, 99, 235), width=2)

    # 4. Balas de valor estratégico (max x <= 635)
    bullets = [
        (
            "Pilares 1 & 2: Gobernanza RACI & Riesgo AMFE",
            "Accountable único, balance FTE y priorización objetiva por NPR",
        )
        if lang == "ES"
        else (
            "Pillars 1 & 2: RACI Governance & FMEA Risk",
            "Single Accountable rule, FTE load & objective RPN ranking",
        ),
        (
            "Pilares 3 & 4: Plazos PERT & Finanzas EVM",
            "Distribución Beta estocástica, buffers y Curva S con EAC",
        )
        if lang == "ES"
        else (
            "Pillars 3 & 4: PERT Schedule & EVM Financials",
            "Stochastic Beta distribution, buffers & S-Curve EAC tracking",
        ),
        (
            "Pilar 5: Cadena de Suministro & Circulante (ROP)",
            "Convolución demanda/plazo y lote EOQ para liberar capital",
        )
        if lang == "ES"
        else (
            "Pillar 5: Supply Chain & Working Capital (ROP)",
            "Demand/lead-time convolution & EOQ sizing to free cash",
        ),
    ]

    bullet_start_y = 210
    spacing_y = 58
    for i, (btitle, bdesc) in enumerate(bullets):
        by = bullet_start_y + i * spacing_y
        col_accent = [(16, 185, 129), (59, 130, 246), (168, 85, 247)][i]
        draw.rounded_rectangle([(SAFE_LEFT, by + 3), (SAFE_LEFT + 10, by + 13)], radius=2, fill=col_accent)
        draw.text((SAFE_LEFT + 20, by), btitle, fill=(255, 255, 255), font=font_bullet_title)
        draw.text((SAFE_LEFT + 20, by + 17), bdesc, fill=(148, 163, 184), font=font_bullet_desc)

    # 5. Píldoras de Entregables (max x <= 635)
    pills_y = 398
    pills = [
        ("10 Excel + Sheets", (30, 41, 59), (56, 189, 248), (56, 189, 248)),
        ("10 Decks PPTX 16:9" if lang == "ES" else "10 PPTX 16:9 Decks", (30, 41, 59), (167, 139, 250), (167, 139, 250)),
        ("5 Guías PDF" if lang == "ES" else "5 PDF Guides", (30, 41, 59), (52, 211, 153), (52, 211, 153)),
    ]

    curr_px = SAFE_LEFT
    for ptext, bgcol, bordercol, dotcol in pills:
        bbox_p = font_pill.getbbox(ptext)
        pw = bbox_p[2] - bbox_p[0] + 30
        ph = 26
        draw.rounded_rectangle([(curr_px, pills_y), (curr_px + pw, pills_y + ph)], radius=6, fill=bgcol, outline=bordercol, width=1)
        dot_x = curr_px + 11
        dot_y = pills_y + 13
        draw.ellipse([(dot_x - 3, dot_y - 3), (dot_x + 3, dot_y + 3)], fill=dotcol)
        draw.text((curr_px + 20, pills_y + 5), ptext, fill=(255, 255, 255), font=font_pill)
        curr_px += pw + 10

    # 6. Bloque Comercial Integrado (x=145..620)
    cta_box_y = 444
    cta_w, cta_h = 475, 80
    draw.rounded_rectangle(
        [(SAFE_LEFT, cta_box_y), (SAFE_LEFT + cta_w, cta_box_y + cta_h)],
        radius=10,
        fill=(15, 23, 42),
        outline=(37, 99, 235),
        width=2,
    )

    draw.text((SAFE_LEFT + 18, cta_box_y + 12), "22€", fill=(245, 158, 11), font=font_price_main)

    strike_txt = "Valor individual: 34€" if lang == "ES" else "Individual value: 34€"
    sx = SAFE_LEFT + 72
    draw.text((sx, cta_box_y + 15), strike_txt, fill=(148, 163, 184), font=font_price_strike)
    bbox_st = font_price_strike.getbbox(strike_txt)
    st_w = bbox_st[2] - bbox_st[0]
    draw.line([(sx, cta_box_y + 23), (sx + st_w, cta_box_y + 23)], fill=(239, 68, 68), width=1)

    savings_badge = "Ahorro 35%" if lang == "ES" else "35% Savings"
    sb_x = sx + st_w + 12
    sb_box = font_tier_small.getbbox(savings_badge)
    sb_w = (sb_box[2] - sb_box[0]) + 16
    draw.rounded_rectangle([(sb_x, cta_box_y + 13), (sb_x + sb_w, cta_box_y + 31)], radius=4, fill=(16, 185, 129))
    draw.text((sb_x + 8, cta_box_y + 15), savings_badge, fill=(255, 255, 255), font=font_tier_small)

    trust_txt = (
        "Descarga directa inmediata (.ZIP) • Modelos 100% editables"
        if lang == "ES"
        else "Instant direct download (.ZIP) • 100% unlocked for Board review"
    )
    draw.text((SAFE_LEFT + 18, cta_box_y + 46), trust_txt, fill=(203, 213, 225), font=font_tier_small)

    # 7. Footer corporativo en Safe Zone inferior
    draw.text((SAFE_LEFT, 560), "DATALARIA.COM • THE QUANTITATIVE MANAGEMENT ENGINE", fill=(71, 85, 105), font=font_badge)

    # 8. 5 Pilares a la derecha dentro de x=[677, 1053]
    draw_5_pillars(draw, pillar_center_x, pillar_center_y, font_tier_bold, font_tier_small, font_tier_tiny, lang=lang)

    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Portada Safe-Zone [145,1055] generada: {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    es_path = os.path.join(base_dir, "content", "es", "posts", "control-operativo-pmbok-framework-cuantitativo", "cover.png")
    en_path = os.path.join(base_dir, "content", "en", "posts", "operational-control-pmbok-quantitative-framework", "cover.png")
    create_cover(lang="ES", out_path=es_path)
    create_cover(lang="EN", out_path=en_path)
