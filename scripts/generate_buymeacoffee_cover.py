#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_buymeacoffee_cover.py
==============================
Genera la imagen de portada para el producto "Buy Me a Coffee / Support Datalaria"
en Lemon Squeezy:
1. Formato panorámico (1200x630): packages/00_DISTRIBUCION_LEMONSQUEEZY/Images/BuyMeACoffee.png
2. Formato cuadrado optimizado para Lemon Squeezy (1200x1200 con safe zones):
   packages/00_DISTRIBUCION_LEMONSQUEEZY/Images_Square/BuyMeACoffee.png
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

SLIDE_W = 1200
SLIDE_H = 630

SQUARE_W = 1200
SQUARE_H = 1200


def get_font(name, size):
    font_paths = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
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


def draw_technical_grid(draw, width, height, bg_line=(18, 28, 48), cross_col=(51, 65, 85)):
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=bg_line, width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=bg_line, width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=cross_col, width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=cross_col, width=1)


def get_box_edge_point(box_cx, box_cy, box_w, box_h, target_x, target_y):
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


def draw_coffee_icon(draw, cx, cy, scale=1.0):
    """Dibuja un icono vectorial limpio de taza de café con vapor en tonos ámbar/dorado."""
    amber = (245, 158, 11)
    amber_light = (251, 191, 36)
    dark_bg = (15, 23, 42)

    # Halo circular
    r_outer = int(42 * scale)
    draw.ellipse([(cx - r_outer, cy - r_outer), (cx + r_outer, cy + r_outer)],
                 fill=(30, 27, 22), outline=amber, width=2)

    # Asa de la taza (derecha)
    hx1 = cx + int(10 * scale)
    hy1 = cy - int(8 * scale)
    hx2 = cx + int(24 * scale)
    hy2 = cy + int(10 * scale)
    draw.rounded_rectangle([(hx1, hy1), (hx2, hy2)], radius=int(7 * scale), fill=None, outline=amber_light, width=3)

    # Cuerpo de la taza
    cup_w = int(32 * scale)
    cup_h = int(26 * scale)
    cx1 = cx - cup_w // 2 - int(2 * scale)
    cy1 = cy - int(10 * scale)
    cx2 = cx1 + cup_w
    cy2 = cy1 + cup_h
    draw.rounded_rectangle([(cx1, cy1), (cx2, cy2)], radius=int(7 * scale), fill=amber, outline=amber_light, width=2)

    # Detalle interior oscuro en la parte superior de la taza
    draw.line([(cx1 + 4, cy1 + 4), (cx2 - 4, cy1 + 4)], fill=dark_bg, width=2)

    # Plato inferior
    px1 = cx - int(22 * scale)
    px2 = cx + int(18 * scale)
    py = cy2 + int(6 * scale)
    draw.line([(px1, py), (px2, py)], fill=amber_light, width=3)

    # Líneas de vapor (3 ondas verticales)
    for dx in (-8, 0, 8):
        sx = cx + int(dx * scale) - int(2 * scale)
        sy_top = cy1 - int(14 * scale)
        sy_bot = cy1 - int(5 * scale)
        draw.line([(sx, sy_bot), (sx + 2, (sy_top + sy_bot) // 2), (sx, sy_top)], fill=amber_light, width=2)


def draw_ecosystem_diagram(draw, cx, cy, font_bold, font_mid, font_tiny):
    """Dibuja el ecosistema abierto de Datalaria impulsado por el apoyo de la comunidad."""
    hub_w, hub_h = 244, 92
    hx = cx - hub_w // 2
    hy = cy - hub_h // 2

    nodes = [
        {
            "angle": -math.pi / 2,
            "dist": 182,
            "title": "100+ TECHNICAL GUIDES",
            "tools": "Data · Applied AI · Ops Engineering",
            "color": (56, 189, 248),
        },
        {
            "angle": math.pi / 6,
            "dist": 192,
            "title": "OPEN CLOUD APPS",
            "tools": "LifeOps · Agentic Radar · Labs",
            "color": (16, 185, 129),
        },
        {
            "angle": 5 * math.pi / 6,
            "dist": 192,
            "title": "R&D & ARCHITECTURE",
            "tools": "Zero-Ads · Independent Research",
            "color": (168, 85, 247),
        }
    ]

    nw, nh = 220, 60

    for n in nodes:
        sx = cx + int(round(n["dist"] * math.cos(n["angle"])))
        sy = cy + int(round(n["dist"] * math.sin(n["angle"])))
        n["sx"] = sx
        n["sy"] = sy

        p_hub = get_box_edge_point(cx, cy, hub_w + 6, hub_h + 6, sx, sy)
        p_node = get_box_edge_point(sx, sy, nw + 4, nh + 4, cx, cy)

        draw.line([p_hub, p_node], fill=(45, 35, 20), width=4)
        draw.line([p_hub, p_node], fill=(245, 158, 11), width=2)

        for p in (p_hub, p_node):
            draw.ellipse([(p[0] - 3, p[1] - 3), (p[0] + 3, p[1] + 3)], fill=(251, 191, 36))

    # Hub central con borde ámbar ejecutivo
    draw.rounded_rectangle([(hx - 3, hy - 3), (hx + hub_w + 3, hy + hub_h + 3)],
                           radius=14, fill=None, outline=(245, 158, 11), width=2)
    draw.rounded_rectangle([(hx, hy), (hx + hub_w, hy + hub_h)],
                           radius=12, fill=(15, 23, 42), outline=(251, 191, 36), width=2)

    # Icono de café arriba del hub
    draw_coffee_icon(draw, cx, hy - 6, scale=0.62)

    title_hub = "BUY ME A COFFEE"
    sub_hub = "Invítame a un Café · ES / EN"
    sub2_hub = "Community & Supporter Hub"

    bb = font_bold.getbbox(title_hub)
    draw.text((cx - (bb[2] - bb[0]) // 2, hy + 26), title_hub, fill=(255, 255, 255), font=font_bold)
    bb2 = font_tiny.getbbox(sub_hub)
    draw.text((cx - (bb2[2] - bb2[0]) // 2, hy + 49), sub_hub, fill=(251, 191, 36), font=font_tiny)
    bb3 = font_tiny.getbbox(sub2_hub)
    draw.text((cx - (bb3[2] - bb3[0]) // 2, hy + 66), sub2_hub, fill=(148, 163, 184), font=font_tiny)

    for n in nodes:
        sx, sy = n["sx"], n["sy"]
        nx1 = sx - nw // 2
        ny1 = sy - nh // 2
        draw.rounded_rectangle([(nx1, ny1), (nx1 + nw, ny1 + nh)],
                               radius=8, fill=(15, 23, 42), outline=n["color"], width=2)

        bb_st = font_mid.getbbox(n["title"])
        draw.text((sx - (bb_st[2] - bb_st[0]) // 2, ny1 + 10), n["title"], fill=(255, 255, 255), font=font_mid)
        bb_tl = font_tiny.getbbox(n["tools"])
        draw.text((sx - (bb_tl[2] - bb_tl[0]) // 2, ny1 + 32), n["tools"], fill=n["color"], font=font_tiny)


def generate_covers():
    img_dir = r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria\packages\00_DISTRIBUCION_LEMONSQUEEZY\Images"
    sq_dir = r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria\packages\00_DISTRIBUCION_LEMONSQUEEZY\Images_Square"
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(sq_dir, exist_ok=True)

    slide = Image.new("RGB", (SLIDE_W, SLIDE_H), color=(11, 17, 32))
    draw = ImageDraw.Draw(slide)

    draw_linear_gradient(draw, SLIDE_W, SLIDE_H, (11, 17, 32), (28, 38, 56))
    draw_technical_grid(draw, SLIDE_W, SLIDE_H)

    font_badge = get_font("segoeuib.ttf", 13)
    font_title = get_font("segoeuib.ttf", 36)
    font_subtitle = get_font("segoeui.ttf", 17)
    font_bold = get_font("segoeuib.ttf", 15)
    font_mid = get_font("segoeuib.ttf", 12)
    font_text = get_font("segoeui.ttf", 13)
    font_tiny = get_font("segoeui.ttf", 11)
    font_price = get_font("segoeuib.ttf", 20)
    font_watermark = get_font("segoeuib.ttf", 11)

    left_x = 60

    # 1. Badge superior
    badge_text = "DATALARIA OPEN ECOSYSTEM • SUPPORTER CONTRIBUTION"
    bx, by = left_x, 48
    bb_b = font_badge.getbbox(badge_text)
    bw = (bb_b[2] - bb_b[0]) + 28
    draw.rounded_rectangle([(bx, by), (bx + bw, by + 30)], radius=6, fill=(45, 32, 15), outline=(245, 158, 11), width=1)
    draw.text((bx + 14, by + 6), badge_text, fill=(251, 191, 36), font=font_badge)

    # 2. Título Principal
    t1 = "BUY ME A COFFEE"
    t2 = "INVÍTAME A UN CAFÉ"
    draw.text((left_x, 98), t1, fill=(255, 255, 255), font=font_title)
    draw.text((left_x, 142), t2, fill=(251, 191, 36), font=font_title)

    # 3. Subtítulo
    sub_t = "Apoya la divulgación técnica y las apps abiertas de Datalaria\nSupport independent engineering articles & zero-cost web apps"
    draw.text((left_x, 198), sub_t, fill=(203, 213, 225), font=font_subtitle)

    # Línea separadora sutil
    draw.line([(left_x, 254), (left_x + 490, 254)], fill=(51, 65, 85), width=1)

    # 4. Bullets de valor
    items = [
        ("1. Divulgación Técnica Abierta (ES / EN):", "Artículos de arquitectura de datos, IA agéntica e ingeniería operativa."),
        ("2. Laboratorio de Apps & Sandboxes:", "Herramientas interactivas en la nube (LifeOps, Radar IA, Weather ML)."),
        ("3. 100% Independiente & Sin Publicidad:", "Tu aportación mantiene los servidores y la investigación abierta.")
    ]
    iy = 272
    for title_i, desc_i in items:
        draw.ellipse([(left_x, iy + 5), (left_x + 7, iy + 12)], fill=(251, 191, 36))
        draw.text((left_x + 16, iy), title_i, fill=(255, 255, 255), font=font_bold)
        draw.text((left_x + 16, iy + 20), desc_i, fill=(148, 163, 184), font=font_text)
        iy += 52

    # 5. Píldoras de pilares (con rombos vectoriales de color, sin glifos emoji rotos)
    pills = [
        ("Micro-Mecenazgo", (245, 158, 11)),
        ("Open Knowledge", (56, 189, 248)),
        ("Cloud Labs", (16, 185, 129)),
    ]
    px = left_x
    py = 440
    for p_txt, p_col in pills:
        bb_p = font_mid.getbbox(p_txt)
        pw = (bb_p[2] - bb_p[0]) + 34
        draw.rounded_rectangle([(px, py), (px + pw, py + 30)], radius=6, fill=(15, 23, 42), outline=p_col, width=1)
        # Rombo vectorial de color a la izquierda del texto
        dx_c = px + 13
        dy_c = py + 15
        draw.polygon([(dx_c, dy_c - 4), (dx_c + 4, dy_c), (dx_c, dy_c + 4), (dx_c - 4, dy_c)], fill=p_col)
        draw.text((px + 22, py + 7), p_txt, fill=(255, 255, 255), font=font_mid)
        px += pw + 10

    # 6. Caja de Precio / Aportación Libre
    p_box_y = 486
    draw.rounded_rectangle([(left_x, p_box_y), (left_x + 365, p_box_y + 46)],
                           radius=8, fill=(30, 25, 18), outline=(245, 158, 11), width=2)
    draw.text((left_x + 16, p_box_y + 9), "Desde 3€", fill=(251, 191, 36), font=font_price)
    draw.text((left_x + 116, p_box_y + 14), "Aportación libre · Pay what you want", fill=(226, 232, 240), font=font_mid)

    # 7. Marca de agua inferior
    draw.text((left_x, 558), "DATALARIA.COM · INDEPENDENT ENGINEERING & APPLIED AI", fill=(100, 116, 139), font=font_watermark)

    # 8. Diagrama derecho
    draw_ecosystem_diagram(draw, 880, 325, font_bold, font_mid, font_tiny)

    slide_path = os.path.join(img_dir, "BuyMeACoffee.png")
    slide.save(slide_path, "PNG", quality=95)
    print(f"Saved panoramic slide: {slide_path}")

    # Ahora generamos la versión cuadrada 1200x1200 con safe zones idéntica a generate_lemonsqueezy_square_covers.py
    sq_canvas = Image.new("RGB", (SQUARE_W, SQUARE_H), (11, 17, 32))
    sq_draw = ImageDraw.Draw(sq_canvas)
    draw_technical_grid(sq_draw, SQUARE_W, SQUARE_H, bg_line=(18, 27, 44), cross_col=(35, 48, 68))

    scale = 1080 / SLIDE_W
    new_w = int(SLIDE_W * scale)
    new_h = int(SLIDE_H * scale)
    slide_resized = slide.resize((new_w, new_h), Image.Resampling.LANCZOS)

    paste_x = (SQUARE_W - new_w) // 2
    paste_y = 575 - (new_h // 2)
    sq_canvas.paste(slide_resized, (paste_x, paste_y))

    # Marco ejecutivo ámbar/cian
    sq_draw.rectangle(
        [(paste_x - 1, paste_y - 1), (paste_x + new_w, paste_y + new_h)],
        outline=(245, 158, 11),
        width=1
    )

    sq_path = os.path.join(sq_dir, "BuyMeACoffee.png")
    sq_canvas.save(sq_path, "PNG", quality=95)
    print(f"Saved square cover: {sq_path}")


if __name__ == "__main__":
    generate_covers()
