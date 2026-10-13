#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) para el Post Pilar Maestro de la Suite 03:
- content/es/posts/control-operativo-pmbok-framework-cuantitativo/cover.png
- content/en/posts/operational-control-pmbok-quantitative-framework/cover.png

Composición visual de estándar McKinsey / PMO Corporativa / C-Level:
- Fondo Dark Slate (#0B1120 a #0F172A y #1E293B) con degradado suave y malla técnica.
- Trazados de ingeniería operativa: Curva S sigmoidal sutil y patrón Diente de Sierra.
- Las 5 tarjetas analíticas interconectadas (RACI, AMFE, PERT, EVM, Stock ROP).
- Título dispuesto en 2 líneas de alto contraste para evitar solapamiento horizontal.
- Badge superior: DATALARIA EXECUTIVE FRAMEWORK • SUITE 03 MEGA BUNDLE
- Subtítulo ejecutivo y viñetas estratégicas estructuradas en la columna izquierda.
- Píldoras de entregables: [📊 10 Modelos Excel/Sheets] [📑 10 Decks PPTX 16:9] [📄 5 Guías PDF].
- Bloque de oferta y garantía: 22€ (Ahorro 35% • Original 34€).
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
            blend = (ratio_x * 0.35 + ratio_y * 0.65)
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


def draw_engineering_curves(draw, center_x, center_y):
    """Dibuja trazados sutiles de Curva S y Diente de Sierra en el fondo derecho."""
    s_points = []
    start_x = center_x - 210
    end_x = center_x + 230
    base_y = center_y + 130
    top_y = center_y - 200

    for px in range(start_x, end_x, 4):
        t = (px - start_x) / (end_x - start_x)
        sig = 1 / (1 + math.exp(-7 * (t - 0.5)))
        py = int(base_y - sig * (base_y - top_y))
        s_points.append((px, py))

    for i in range(len(s_points) - 1):
        draw.line([s_points[i], s_points[i + 1]], fill=(30, 58, 110), width=3)

    saw_y_base = center_y + 245
    saw_y_top = center_y + 190
    saw_x_start = center_x - 170
    saw_x_end = center_x + 210
    saw_cycle = 75

    cx = saw_x_start
    while cx < saw_x_end:
        next_drop = min(cx + saw_cycle, saw_x_end)
        draw.line([(cx, saw_y_top), (next_drop, saw_y_base)], fill=(76, 29, 149), width=2)
        if next_drop < saw_x_end:
            draw.line([(next_drop, saw_y_base), (next_drop, saw_y_top)], fill=(88, 28, 135), width=2)
        cx = next_drop


def draw_5_pillars(draw, center_x, center_y, font_bold, font_small, font_tiny, lang='ES'):
    """Dibuja las 5 tarjetas de los pilares del framework de forma compacta y ejecutiva."""
    card_w = 360
    card_h = 66
    spacing = 26  # Espacio entre tarjetas

    # 5 tarjetas calculadas verticalmente desde center_y
    # Altura total: 5 * 66 + 4 * 26 = 330 + 104 = 434 px
    start_y = center_y - (434 // 2)

    pillars = [
        {
            "num": "P1",
            "name": "RACI MATRIX" if lang == 'EN' else "MATRIZ RACI",
            "role": "Governance & Workload" if lang == 'EN' else "Gobernanza & Carga",
            "metric": "A = 1  |  W_k = Σ w_x · X_ik",
            "col_border": (16, 185, 129),   # Emerald
            "col_bg": (15, 23, 42),
            "col_badge": (52, 211, 153),
            "y": start_y
        },
        {
            "num": "P2",
            "name": "FMEA / AMFE" if lang == 'EN' else "AMFE / FMEA",
            "role": "Reliability & NPR" if lang == 'EN' else "Prevención & NPR",
            "metric": "RPN = S × O × D  (ISO 31000)" if lang == 'EN' else "NPR = S × O × D  (ISO 31000)",
            "col_border": (244, 63, 94),    # Rose/Red
            "col_bg": (15, 23, 42),
            "col_badge": (251, 113, 133),
            "y": start_y + (card_h + spacing) * 1
        },
        {
            "num": "P3",
            "name": "3-POINT PERT" if lang == 'EN' else "PERT 3 PUNTOS",
            "role": "Beta Timeline & Buffers" if lang == 'EN' else "Cronograma Beta & Buffers",
            "metric": "μ = (o + 4m + p)/6  |  Z-Score",
            "col_border": (59, 130, 246),   # Blue
            "col_bg": (15, 23, 42),
            "col_badge": (96, 165, 250),
            "y": start_y + (card_h + spacing) * 2
        },
        {
            "num": "P4",
            "name": "EVM S-CURVE" if lang == 'EN' else "EVM CURVA S",
            "role": "Earned Value & EAC" if lang == 'EN' else "Valor Ganado & EAC",
            "metric": "CPI = EV/AC  |  EAC = BAC/CPI",
            "col_border": (245, 158, 11),   # Amber
            "col_bg": (15, 23, 42),
            "col_badge": (251, 191, 36),
            "y": start_y + (card_h + spacing) * 3
        },
        {
            "num": "P5",
            "name": "SAFETY STOCK & ROP" if lang == 'EN' else "STOCK ROP",
            "role": "Working Capital & Buffer" if lang == 'EN' else "Circulante & Nivel Servicio",
            "metric": "SS = Z · √(L σ_d² + d² σ_L²)",
            "col_border": (168, 85, 247),  # Purple
            "col_bg": (15, 23, 42),
            "col_badge": (192, 132, 252),
            "y": start_y + (card_h + spacing) * 4
        }
    ]

    # Conectores verticales entre tarjetas
    for i in range(len(pillars) - 1):
        y1 = pillars[i]["y"] + card_h
        y2 = pillars[i + 1]["y"]
        draw.line([(center_x, y1), (center_x, y2)], fill=(56, 189, 248), width=2)
        # Flecha indicadora pequeña
        draw.polygon([
            (center_x, y2),
            (center_x - 4, y2 - 6),
            (center_x + 4, y2 - 6)
        ], fill=(56, 189, 248))

    # Dibujar las 5 tarjetas
    for p in pillars:
        w = card_w
        h = card_h
        x1 = center_x - w // 2
        y1 = p["y"]
        x2 = center_x + w // 2
        y2 = y1 + h

        # Sombra sutil
        draw.rounded_rectangle([(x1 + 4, y1 + 4), (x2 + 4, y2 + 4)], radius=8, fill=(10, 15, 28))

        # Tarjeta principal
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=8, fill=p["col_bg"], outline=p["col_border"], width=2)

        # Badge lateral (P1, P2, ...)
        badge_w = 44
        draw.rounded_rectangle([(x1 + 10, y1 + 10), (x1 + 10 + badge_w, y1 + 31)], radius=4, fill=(30, 41, 59), outline=p["col_border"], width=1)
        b_txt = p["num"]
        bbox_b = font_small.getbbox(b_txt)
        bw_txt = bbox_b[2] - bbox_b[0]
        draw.text((x1 + 10 + (badge_w - bw_txt) // 2, y1 + 13), b_txt, fill=p["col_badge"], font=font_small)

        # Título de la herramienta
        t_name = p["name"]
        draw.text((x1 + 64, y1 + 10), t_name, fill=(255, 255, 255), font=font_bold)

        # Subtítulo de función
        draw.text((x1 + 64, y1 + 27), p["role"], fill=(148, 163, 184), font=font_small)

        # Barra inferior con fórmula / métrica algorítmica
        formula_box_y1 = y1 + 44
        draw.rounded_rectangle([(x1 + 10, formula_box_y1), (x2 - 10, formula_box_y1 + 16)], radius=3, fill=(18, 28, 48))
        f_txt = p["metric"]
        draw.text((x1 + 18, formula_box_y1 + 1), f_txt, fill=(56, 189, 248), font=font_tiny)

    # Indicador de flujo a la derecha de las tarjetas
    status_x = center_x + card_w // 2 + 18
    if status_x < WIDTH - 30:
        labels = [
            ("1. GOVERNANCE", "Balance de Roles") if lang == 'ES' else ("1. GOVERNANCE", "Role Balancing"),
            ("2. RELIABILITY", "Mitigación AMFE") if lang == 'ES' else ("2. RELIABILITY", "FMEA Mitigation"),
            ("3. SCHEDULE", "Línea Base PERT") if lang == 'ES' else ("3. SCHEDULE", "PERT Baseline"),
            ("4. FINANCIALS", "Control Curva S") if lang == 'ES' else ("4. FINANCIALS", "S-Curve Tracking"),
            ("5. INVENTORY", "Stock Seguridad") if lang == 'ES' else ("5. INVENTORY", "Safety Buffer")
        ]
        for i, (l_top, l_bot) in enumerate(labels):
            ly = pillars[i]["y"] + 11
            draw.text((status_x, ly), l_top, fill=(245, 158, 11), font=font_tiny)
            draw.text((status_x, ly + 13), l_bot, fill=(203, 213, 225), font=font_tiny)


def create_cover(lang='ES', out_path='cover.png'):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado Slate Dark
    draw_linear_gradient(draw, WIDTH, HEIGHT, (11, 17, 32), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # 3. Trazados de ingeniería en el fondo derecho
    draw_engineering_curves(draw, 875, 315)

    # 4. Fuentes
    font_badge = get_font("segoeuib.ttf", 11)
    font_title_large = get_font("segoeuib.ttf", 34)
    font_subtitle = get_font("segoeui.ttf", 13)
    font_bullet_title = get_font("segoeuib.ttf", 13)
    font_bullet_desc = get_font("segoeui.ttf", 11)
    font_pill = get_font("segoeuib.ttf", 11)
    font_tier_bold = get_font("segoeuib.ttf", 12)
    font_tier_small = get_font("segoeuib.ttf", 10)
    font_tier_tiny = get_font("segoeui.ttf", 9)
    font_price_main = get_font("segoeuib.ttf", 22)
    font_price_strike = get_font("segoeui.ttf", 13)

    # 5. Badge Superior Corporativo
    badge_text = "DATALARIA EXECUTIVE FRAMEWORK • SUITE 03 MEGA BUNDLE"
    b_x, b_y = 60, 32
    b_w, b_h = 475, 26
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text((b_x + 14, b_y + 5), badge_text, fill=(56, 189, 248), font=font_badge)

    # 6. Título Principal en 2 Líneas (Sin solapamiento con la columna derecha)
    # Columna izquierda: x=60 a ~520 px. Tarjetas derechas: x=695 a 1055 px.
    t_y1 = 72
    t_y2 = 114

    if lang == 'ES':
        title_line1 = "CONTROL OPERATIVO &"
        title_line2 = "MÉTRICAS PMBOK"
    else:
        title_line1 = "OPERATIONAL CONTROL &"
        title_line2 = "PMBOK METRICS"

    # Línea 1 en blanco de alto impacto
    draw.text((60, t_y1), title_line1, fill=(255, 255, 255), font=font_title_large)
    # Línea 2 en ámbar corporativo
    draw.text((60, t_y2), title_line2, fill=(245, 158, 11), font=font_title_large)

    # 7. Subtítulo Ejecutivo
    sub_y = 164
    subtitle = (
        "El Framework Cuantitativo de 5 Pilares: RACI, AMFE, PERT, EVM & Stock ROP"
        if lang == 'ES' else
        "The 5-Pillar Quantitative Framework: RACI, FMEA, PERT, EVM & Safety Stock"
    )
    draw.text((60, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle)

    # Línea decorativa horizontal
    draw.line([(60, 194), (550, 194)], fill=(37, 99, 235), width=2)

    # 8. Balas de valor estratégico
    bullets = [
        (
            "Pilares 1 & 2: Gobernanza RACI & Prevención AMFE",
            "Principio de Accountable único, balance de FTEs y priorización por NPR objetivo"
        ) if lang == 'ES' else (
            "Pillars 1 & 2: RACI Governance & FMEA Prevention",
            "Single accountability enforcement, role saturation, and objective RPN risk ranking"
        ),
        (
            "Pilares 3 & 4: Plazos PERT & Finanzas de Proyecto EVM",
            "Distribución Beta estocástica, buffers de ruta crítica y Curva S con proyección EAC"
        ) if lang == 'ES' else (
            "Pillars 3 & 4: PERT Schedule & EVM Project Financials",
            "Stochastic Beta distribution, critical path buffers, and S-Curve EAC cost forecasting"
        ),
        (
            "Pilar 5: Cadena de Suministro & Working Capital (ROP)",
            "Convolución estocástica de demanda/plazo y calibración EOQ para proteger circulante"
        ) if lang == 'ES' else (
            "Pillar 5: Supply Chain & Working Capital (ROP/EOQ)",
            "Stochastic convolution of lead time/demand and Wilson lot sizing to free cash"
        )
    ]

    bullet_start_y = 210
    spacing_y = 64
    for i, (btitle, bdesc) in enumerate(bullets):
        by = bullet_start_y + i * spacing_y

        col_accent = [(16, 185, 129), (59, 130, 246), (168, 85, 247)][i]
        draw.rounded_rectangle([(60, by + 2), (72, by + 14)], radius=2, fill=col_accent)

        draw.text((82, by), btitle, fill=(255, 255, 255), font=font_bullet_title)
        draw.text((82, by + 18), bdesc, fill=(148, 163, 184), font=font_bullet_desc)

    # 9. Píldoras de Entregables
    pills_y = 412
    pills = [
        ("10 Modelos Excel/Sheets" if lang == 'ES' else "10 Excel/Sheets Models", (30, 41, 59), (56, 189, 248), (56, 189, 248)),
        ("10 Decks PPTX 16:9" if lang == 'ES' else "10 PPTX 16:9 Decks", (30, 41, 59), (167, 139, 250), (167, 139, 250)),
        ("5 Guías PDF" if lang == 'ES' else "5 PDF Guides", (30, 41, 59), (52, 211, 153), (52, 211, 153))
    ]

    curr_px = 60
    for ptext, bgcol, bordercol, dotcol in pills:
        bbox_p = font_pill.getbbox(ptext)
        pw = bbox_p[2] - bbox_p[0] + 36
        ph = 28
        draw.rounded_rectangle([(curr_px, pills_y), (curr_px + pw, pills_y + ph)], radius=6, fill=bgcol, outline=bordercol, width=1)
        # Dot indicador de color
        dot_x = curr_px + 12
        dot_y = pills_y + 14
        draw.ellipse([(dot_x - 3, dot_y - 3), (dot_x + 3, dot_y + 3)], fill=dotcol)
        draw.text((curr_px + 22, pills_y + 6), ptext, fill=(255, 255, 255), font=font_pill)
        curr_px += pw + 12

    # 10. Bloque de Precio y Garantía
    cta_box_y = 458
    cta_w, cta_h = 500, 84
    draw.rounded_rectangle([(60, cta_box_y), (60 + cta_w, cta_box_y + cta_h)], radius=10, fill=(15, 23, 42), outline=(37, 99, 235), width=2)

    # Precio
    draw.text((80, cta_box_y + 14), "22€", fill=(245, 158, 11), font=font_price_main)

    # Precio tachado y ahorro
    strike_txt = "Valor individual: 34€" if lang == 'ES' else "Individual value: 34€"
    draw.text((140, cta_box_y + 16), strike_txt, fill=(148, 163, 184), font=font_price_strike)
    bbox_st = font_price_strike.getbbox(strike_txt)
    st_w = bbox_st[2] - bbox_st[0]
    draw.line([(140, cta_box_y + 24), (140 + st_w, cta_box_y + 24)], fill=(239, 68, 68), width=1)

    # Badge de ahorro
    savings_badge = "Ahorro 35%" if lang == 'ES' else "35% Savings"
    draw.rounded_rectangle([(140 + st_w + 12, cta_box_y + 14), (140 + st_w + 12 + 82, cta_box_y + 32)], radius=4, fill=(16, 185, 129))
    draw.text((140 + st_w + 20, cta_box_y + 16), savings_badge, fill=(255, 255, 255), font=font_tier_small)

    # Subtexto de garantía
    trust_txt = "Descarga directa inmediata (.ZIP) • 100% desbloqueado para Comités" if lang == 'ES' else "Instant direct download (.ZIP) • 100% unlocked for Boardroom review"
    draw.text((80, cta_box_y + 48), trust_txt, fill=(203, 213, 225), font=font_tier_small)

    # 11. Dibujar los 5 Pilares Cuantitativos a la derecha
    # Centrado en x=875, y=315 (distancia holgada respecto a la columna izquierda)
    pillar_center_x = 875
    pillar_center_y = 315
    draw_5_pillars(draw, pillar_center_x, pillar_center_y, font_tier_bold, font_tier_small, font_tier_tiny, lang=lang)

    # Guardar imagen optimizada
    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Portada generada con éxito: {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    es_path = os.path.join(base_dir, "content", "es", "posts", "control-operativo-pmbok-framework-cuantitativo", "cover.png")
    en_path = os.path.join(base_dir, "content", "en", "posts", "operational-control-pmbok-quantitative-framework", "cover.png")

    create_cover(lang='ES', out_path=es_path)
    create_cover(lang='EN', out_path=en_path)
