#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_mega_bundle_cover.py
=============================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) para el Post Marco del Mega Bundle:
- content/es/posts/executive-decision-packs-framework-cuantitativo/cover.png
- content/en/posts/executive-decision-packs-quantitative-framework/cover.png
- static/images/lemon_squeezy_mega_bundle_cover.png

Composición visual de estándar directivo Tier-1:
- Fondo Dark Slate (#0B1120 a #1E293B) con degradado y malla técnica.
- Diagrama tri-nodal de arquitectura conectando las 3 Suites (Estrategia, Decisiones, Operaciones).
- Badges de entregables, Pirámide de Minto y sello de calidad Datalaria.
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
            blend = (ratio_x * 0.45 + ratio_y * 0.55)
            r = int(r1 + (r2 - r1) * blend)
            g = int(g1 + (g2 - g1) * blend)
            b = int(b1 + (b2 - b1) * blend)
            draw.line([(x, y), (x + 1, y)], fill=(r, g, b))


def draw_technical_grid(draw, width, height):
    """Dibuja una malla técnica sutil con cuadrículas."""
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(18, 28, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(18, 28, 48), width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def get_box_edge_point(box_cx, box_cy, box_w, box_h, target_x, target_y):
    """Calcula el punto exacto de intersección de un rayo desde el centro de la caja hacia el objetivo."""
    dx = target_x - box_cx
    dy = target_y - box_cy
    if dx == 0 and dy == 0:
        return (box_cx, box_cy)
    hw = box_w / 2.0
    hh = box_h / 2.0
    scale_x = hw / abs(dx) if dx != 0 else float('inf')
    scale_y = hh / abs(dy) if dy != 0 else float('inf')
    scale = min(scale_x, scale_y)
    return (int(round(box_cx + dx * scale)), int(round(box_cy + dy * scale)))


def draw_architecture_diagram(draw, cx, cy, font_bold, font_mid, font_tiny, lang='ES'):
    """Dibuja el diagrama de arquitectura tri-nodal de las 3 Suites conectadas al Hub Central sin superposición de líneas."""
    hub_w, hub_h = 240, 84
    hx = cx - hub_w // 2
    hy = cy - hub_h // 2

    # 3 Nodos de Suites alrededor del Hub
    # Ángulos: Arriba (-90°), Abajo-Derecha (30°), Abajo-Izquierda (150°)
    suites = [
        {
            "angle": -math.pi / 2, # Arriba
            "dist": 165,
            "title": "SUITE 01: ESTRATEGIA MBA" if lang == 'ES' else "SUITE 01: MBA STRATEGY",
            "tools": "DAFO · Porter · PESTEL · BCG · McKinsey",
            "color": (239, 68, 68),
            "accent": (254, 226, 226)
        },
        {
            "angle": math.pi / 6, # Abajo Derecha
            "dist": 175,
            "title": "SUITE 02: DECISIONES" if lang == 'ES' else "SUITE 02: DECISIONS",
            "tools": "DAR Veto · RICE Ágil · VAN / TIR",
            "color": (245, 158, 11),
            "accent": (254, 243, 199)
        },
        {
            "angle": 5 * math.pi / 6, # Abajo Izquierda
            "dist": 175,
            "title": "SUITE 03: CONTROL OPERATIVO" if lang == 'ES' else "SUITE 03: OPERATIONS",
            "tools": "RACI · AMFE · PERT · EVM · Stock ROP",
            "color": (16, 185, 129),
            "accent": (209, 250, 229)
        }
    ]

    nw, nh = 216, 60

    # 1. Trazar líneas de conexión en el fondo ANTES de pintar cualquier caja o texto
    for s in suites:
        sx = cx + int(round(s["dist"] * math.cos(s["angle"])))
        sy = cy + int(round(s["dist"] * math.sin(s["angle"])))
        s["sx"] = sx
        s["sy"] = sy

        # Puntos limpios en el perímetro exterior de las cajas (no cruzan el interior)
        p_hub = get_box_edge_point(cx, cy, hub_w + 4, hub_h + 4, sx, sy)
        p_suite = get_box_edge_point(sx, sy, nw + 4, nh + 4, cx, cy)

        # Línea de conexión (resplandor de fondo + trazo frontal)
        draw.line([p_hub, p_suite], fill=(30, 58, 138), width=3)
        draw.line([p_hub, p_suite], fill=s["color"], width=1)

        # Conectores sutiles en los bordes
        for p in (p_hub, p_suite):
            draw.ellipse([(p[0] - 2, p[1] - 2), (p[0] + 2, p[1] + 2)], fill=s["color"])

    # 2. Dibujar Caja del Hub Central con fondo opaco (15, 23, 42)
    draw.rounded_rectangle([(hx - 3, hy - 3), (hx + hub_w + 3, hy + hub_h + 3)], radius=14, fill=None, outline=(56, 189, 248), width=2)
    draw.rounded_rectangle([(hx, hy), (hx + hub_w, hy + hub_h)], radius=12, fill=(15, 23, 42), outline=(14, 165, 233), width=2)

    title_hub = "EXECUTIVE SUITE"
    sub_hub = "13 Quantitative Models" if lang == 'EN' else "13 Modelos Cuantitativos"
    sub2_hub = "Boardroom Decision Standard" if lang == 'EN' else "Estándar Comité de Dirección"

    bb = font_bold.getbbox(title_hub)
    draw.text((cx - (bb[2] - bb[0]) // 2, hy + 13), title_hub, fill=(255, 255, 255), font=font_bold)
    bb2 = font_tiny.getbbox(sub_hub)
    draw.text((cx - (bb2[2] - bb2[0]) // 2, hy + 39), sub_hub, fill=(56, 189, 248), font=font_tiny)
    bb3 = font_tiny.getbbox(sub2_hub)
    draw.text((cx - (bb3[2] - bb3[0]) // 2, hy + 55), sub2_hub, fill=(148, 163, 184), font=font_tiny)

    # 3. Dibujar Cajas de las Suites con fondo opaco y textos perfectamente legibles
    for s in suites:
        sx, sy = s["sx"], s["sy"]
        nx1 = sx - nw // 2
        ny1 = sy - nh // 2
        draw.rounded_rectangle([(nx1, ny1), (nx1 + nw, ny1 + nh)], radius=8, fill=(15, 23, 42), outline=s["color"], width=2)

        bb_st = font_mid.getbbox(s["title"])
        draw.text((sx - (bb_st[2] - bb_st[0]) // 2, ny1 + 10), s["title"], fill=(255, 255, 255), font=font_mid)
        bb_tl = font_tiny.getbbox(s["tools"])
        draw.text((sx - (bb_tl[2] - bb_tl[0]) // 2, ny1 + 32), s["tools"], fill=s["color"], font=font_tiny)


def create_cover(lang='ES', out_path='cover.png'):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado
    draw_linear_gradient(draw, WIDTH, HEIGHT, (11, 17, 32), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # 3. Fuentes
    font_badge = get_font("SegoeUIB", 13)
    font_title = get_font("SegoeUIB", 36)
    font_subtitle = get_font("SegoeUI", 18)
    font_bold = get_font("SegoeUIB", 15)
    font_mid = get_font("SegoeUIB", 12)
    font_text = get_font("SegoeUI", 13)
    font_tiny = get_font("SegoeUI", 11)
    font_price = get_font("SegoeUIB", 20)

    # 4. Badge Superior Izquierdo
    badge_text = "DATALARIA EXECUTIVE SUITE • MEGA BUNDLE"
    bx, by = 60, 48
    bb_b = font_badge.getbbox(badge_text)
    bw = (bb_b[2] - bb_b[0]) + 24
    draw.rounded_rectangle([(bx, by), (bx + bw, by + 28)], radius=6, fill=(2, 132, 199, 40), outline=(56, 189, 248), width=1)
    draw.text((bx + 12, by + 5), badge_text, fill=(56, 189, 248), font=font_badge)

    # 5. Título Principal
    tx, ty = 60, 92
    title_main = "EXECUTIVE DECISION PACKS"
    draw.text((tx, ty), title_main, fill=(255, 255, 255), font=font_title)

    # 6. Subtítulo Ejecutivo
    sy = ty + 50
    subtitle_main = (
        "Del cálculo cuantitativo a la aprobación del Comité de Dirección"
        if lang == 'ES'
        else "From quantitative modeling to Board of Directors approval"
    )
    draw.text((tx, sy), subtitle_main, fill=(148, 163, 184), font=font_subtitle)

    # Separador
    draw.line([(tx, sy + 32), (tx + 480, sy + 32)], fill=(51, 65, 85), width=1)

    # 7. Los 3 Pilares del Ecosistema (Viñetas de Valor)
    bullets = [
        (
            "1. Motor Cuantitativo (Excel & Google Sheets):",
            "Fórmulas matriciales dinámicas y celdas protegidas sin macros."
            if lang == 'ES'
            else "Dynamic array formulas and protected inputs without risky macros."
        ),
        (
            "2. Deck C-Level 16:9 (Pirámide de Minto):",
            "Action Titles y caja de decisión requerida para votación ejecutiva."
            if lang == 'ES'
            else "Action Titles and required decision gateway for Board approval."
        ),
        (
            "3. Guía Metodológica & Protocolo de Defensa:",
            "Justificación axiomática y respuestas a preguntas críticas del CFO."
            if lang == 'ES'
            else "Axiomatic defense guide and answers to critical CFO scrutiny."
        )
    ]

    by_start = sy + 46
    for i, (b_title, b_desc) in enumerate(bullets):
        cy_item = by_start + i * 50
        # Dot
        draw.ellipse([(tx, cy_item + 3), (tx + 8, cy_item + 11)], fill=(56, 189, 248))
        draw.text((tx + 18, cy_item), b_title, fill=(248, 250, 252), font=font_bold)
        draw.text((tx + 18, cy_item + 19), b_desc, fill=(148, 163, 184), font=font_text)

    # 8. Entregables y Badges (Pills con dot vectorial)
    py_chips = by_start + 160
    pills = [
        ("13 Modelos Excel", (16, 185, 129)),
        ("13 Decks PPTX 16:9", (59, 130, 246)),
        ("13 Guías PDF", (168, 85, 247))
    ] if lang == 'ES' else [
        ("13 Excel Models", (16, 185, 129)),
        ("13 PPTX 16:9 Decks", (59, 130, 246)),
        ("13 PDF Guides", (168, 85, 247))
    ]

    curr_x = tx
    for label, col in pills:
        b_p = font_tiny.getbbox(label)
        pw = (b_p[2] - b_p[0]) + 30
        draw.rounded_rectangle([(curr_x, py_chips), (curr_x + pw, py_chips + 24)], radius=5, fill=(15, 23, 42), outline=col, width=1)
        # Dot indicador de color
        draw.ellipse([(curr_x + 8, py_chips + 9), (curr_x + 14, py_chips + 15)], fill=col)
        draw.text((curr_x + 20, py_chips + 4), label, fill=(255, 255, 255), font=font_tiny)
        curr_x += pw + 10

    # 9. Badge de Precio / Descuento Lemon Squeezy
    py_price = py_chips + 36
    draw.rounded_rectangle([(tx, py_price), (tx + 290, py_price + 36)], radius=6, fill=(15, 23, 42), outline=(245, 158, 11), width=2)
    draw.text((tx + 12, py_price + 7), "39€", fill=(245, 158, 11), font=font_price)
    strike_txt = "Valor 82€ • Ahorro >52%" if lang == 'ES' else "Value 82€ • 52% Off"
    draw.text((tx + 65, py_price + 11), strike_txt, fill=(148, 163, 184), font=font_mid)

    # 10. Diagrama de Arquitectura en el Lado Derecho
    right_cx = 920
    right_cy = 320
    draw_architecture_diagram(draw, right_cx, right_cy, font_bold, font_mid, font_tiny, lang=lang)

    # Guardar
    img.save(out_path, format="PNG", quality=95)
    print(f"Cover guardada con éxito en: {out_path}")


def main():
    base_dir = os.path.abspath(".")
    
    # 1. Post en Español
    es_cover = os.path.join(base_dir, "content", "es", "posts", "executive-decision-packs-framework-cuantitativo", "cover.png")
    create_cover(lang='ES', out_path=es_cover)

    # 2. Post en Inglés
    en_cover = os.path.join(base_dir, "content", "en", "posts", "executive-decision-packs-quantitative-framework", "cover.png")
    create_cover(lang='EN', out_path=en_cover)

    # 3. Lemon Squeezy Product Pack Cover
    ls_cover = os.path.join(base_dir, "static", "images", "lemon_squeezy_mega_bundle_cover.png")
    create_cover(lang='ES', out_path=ls_cover)


if __name__ == "__main__":
    main()
