#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) optimizada con ZONA SEGURA (Safe Zone [145, 1055])
para visualización perfecta tanto en página completa como en tarjetas de blog
(aspect ratio 16:9 y 3:2, sin recortes en títulos, diagrama ni viñetas):
- content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/cover.png
- content/en/posts/corporate-strategy-mba-quantitative-framework/cover.png

Composición visual de estándar McKinsey / BCG / Bain:
- Fondo Dark Slate (#0B1120 a #0F172A y #1E293B) con degradado suave y malla técnica.
- Safe Zone: Todo el contenido crítico está enmarcado entre X: 145px y 1055px (zona segura central de 910px),
  garantizando que ninguna tarjeta de lista de posts o vista previa social recorte letras ni nodos.
- Diagrama pentagonal geométrico con los 5 vectores estratégicos interconectados:
  PESTEL, Porter, DAFO/CAME, BCG y McKinsey/GE.
- Badge superior corporativo: DATALARIA EXECUTIVE FRAMEWORK • SUITE 01 MEGA BUNDLE
- Título de alto contraste y subtítulo ejecutivo.
- Balas de valor estratégico con viñetas destacadas.
- Píldoras de entregables: [10 Modelos Excel + Sheets] [10 Decks PPTX 16:9] [5 Guías PDF].
- Badge de precio y acceso: 19€ (antes 28€).
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
    """Dibuja una malla técnica con cuadrículas y puntos sutiles."""
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


def draw_strategic_pentagon(draw, center_x, center_y, radius, font_bold, font_small, font_tiny, lang='ES'):
    """Dibuja la red pentagonal geométrica perfectamente encuadrada dentro de la Safe Zone."""
    nodes = [
        ("PESTEL", "Macro Shock" if lang == 'EN' else "Entorno Macro", (239, 68, 68), (254, 226, 226)),      # Red
        ("PORTER", "Industry Moat" if lang == 'EN' else "Atractivo Industria", (245, 158, 11), (254, 243, 199)), # Amber
        ("DAFO/CAME", "Vector Strategy" if lang == 'EN' else "Vector Estrategico", (16, 185, 129), (209, 250, 229)), # Emerald
        ("BCG", "Cash Flow" if lang == 'EN' else "Flujo Fondos", (59, 130, 246), (219, 234, 254)),         # Blue
        ("MCKINSEY", "CAPEX Alloc." if lang == 'EN' else "Asignacion CAPEX", (168, 85, 247), (243, 232, 255)) # Purple
    ]

    num_nodes = len(nodes)
    angles = [i * (2 * math.pi / num_nodes) - math.pi / 2 for i in range(num_nodes)]
    coords = []

    for a in angles:
        px = center_x + radius * math.cos(a)
        py = center_y + radius * math.sin(a)
        coords.append((px, py))

    # Círculos orbitales concéntricos tenues
    for r_orb in [radius * 0.45, radius * 0.75, radius * 1.0]:
        draw.ellipse(
            [(center_x - r_orb, center_y - r_orb), (center_x + r_orb, center_y + r_orb)],
            outline=(30, 48, 75),
            width=1
        )

    # Conexiones internas completas (red estrella / pentagrama completo)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            draw.line([(x1, y1), (x2, y2)], fill=(37, 99, 235), width=2)

    # Nodos circulares
    node_radius = 23
    for i, (name, role, color_main, color_light) in enumerate(nodes):
        x, y = coords[i]

        # Halo brillante exterior
        draw.ellipse([(x - node_radius - 4, y - node_radius - 4), (x + node_radius + 4, y + node_radius + 4)], outline=color_main, width=1)
        # Relleno del nodo
        draw.ellipse([(x - node_radius, y - node_radius), (x + node_radius, y + node_radius)], fill=(15, 23, 42), outline=color_main, width=2)

        # Nombre del nodo dentro del círculo
        bbox_n = font_bold.getbbox(name)
        nw = bbox_n[2] - bbox_n[0]
        nh = bbox_n[3] - bbox_n[1]
        draw.text((x - nw // 2, y - nh // 2 - 1), name, fill=(255, 255, 255), font=font_bold)

        # Etiqueta de función estratégica externa posicionada según ángulo
        bbox_r = font_small.getbbox(role)
        rw = bbox_r[2] - bbox_r[0]
        
        # Ajuste de posición de etiqueta para no desbordar
        if i == 0:  # Top (PESTEL)
            label_x, label_y = x - rw // 2, y - node_radius - 16
        elif i == 1:  # Top-Right (PORTER)
            label_x, label_y = x - rw // 2, y + node_radius + 6
        elif i == 2:  # Bottom-Right (DAFO/CAME)
            label_x, label_y = x - rw // 2, y + node_radius + 6
        elif i == 3:  # Bottom-Left (BCG)
            label_x, label_y = x - rw // 2, y + node_radius + 6
        else:  # Top-Left (MCKINSEY)
            label_x, label_y = x - rw // 2, y + node_radius + 6

        draw.text((label_x, label_y), role, fill=color_main, font=font_small)

    # Hub central: Motor C-Level
    hub_w, hub_h = 130, 42
    hx1 = center_x - hub_w // 2
    hy1 = center_y - hub_h // 2
    draw.rounded_rectangle([(hx1, hy1), (hx1 + hub_w, hy1 + hub_h)], radius=7, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    center_title = "DECISION ENGINE" if lang == 'EN' else "MOTOR C-LEVEL"
    bbox_ct = font_bold.getbbox(center_title)
    ctw = bbox_ct[2] - bbox_ct[0]
    draw.text((center_x - ctw // 2, hy1 + 7), center_title, fill=(255, 255, 255), font=font_bold)

    center_sub = "5 Connected Matrices" if lang == 'EN' else "5 Matrices Conectadas"
    bbox_cs = font_tiny.getbbox(center_sub)
    csw = bbox_cs[2] - bbox_cs[0]
    draw.text((center_x - csw // 2, hy1 + 24), center_sub, fill=(245, 158, 11), font=font_tiny)


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
    font_title_large = get_font("segoeuib.ttf", 32)
    font_subtitle = get_font("segoeui.ttf", 13.5)
    font_bullet_title = get_font("segoeuib.ttf", 12)
    font_bullet_desc = get_font("segoeui.ttf", 11)
    font_pill = get_font("segoeuib.ttf", 11)
    font_node_bold = get_font("segoeuib.ttf", 10.5)
    font_node_small = get_font("segoeuib.ttf", 9.5)
    font_tiny = get_font("segoeui.ttf", 8.5)
    font_price_main = get_font("segoeuib.ttf", 19)
    font_price_strike = get_font("segoeui.ttf", 13)

    # MARGEN SEGURO IZQUIERDO Y DERECHO (Safe Zone [145, 1055])
    safe_left = 145
    safe_right = 1055

    # 4. Badge Superior Corporativo
    badge_text = "DATALARIA EXECUTIVE FRAMEWORK • SUITE 01 MEGA BUNDLE"
    b_x, b_y = safe_left, 48
    b_w, b_h = 445, 26
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=5, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text((b_x + 14, b_y + 5), badge_text, fill=(56, 189, 248), font=font_badge)

    # 5. Título Principal
    t_y = 88
    if lang == 'ES':
        title_p1 = "ESTRATEGIA CORPORATIVA "
        title_p2 = "CUANTITATIVA"
    else:
        title_p1 = "QUANTITATIVE CORPORATE "
        title_p2 = "STRATEGY"

    draw.text((safe_left, t_y), title_p1, fill=(255, 255, 255), font=font_title_large)
    bbox_p1 = font_title_large.getbbox(title_p1)
    p1_width = bbox_p1[2] - bbox_p1[0]
    draw.text((safe_left + p1_width, t_y), title_p2, fill=(245, 158, 11), font=font_title_large)

    # 6. Subtítulo
    sub_y = 138
    subtitle = (
        "Framework de 5 Pasos para Comités: PESTEL, Porter, DAFO, BCG & McKinsey"
        if lang == 'ES' else
        "5-Step Boardroom Framework: PESTEL, Porter, SWOT, BCG & McKinsey"
    )
    draw.text((safe_left, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle)

    # Línea decorativa horizontal
    draw.line([(safe_left, 168), (620, 168)], fill=(37, 99, 235), width=2)

    # 7. Balas de valor estratégico
    bullets = [
        (
            "Enfoque Outside-In: Del Macroentorno a CAPEX",
            "Conexión matemática secuencial entre volatilidad macro y retorno ROIC"
        ) if lang == 'ES' else (
            "Outside-In Architecture: Macro to Capital Allocation",
            "Sequential mathematical linkage from macro volatility to audited ROIC"
        ),
        (
            "Espacios Métricos & Vectores Cartesianos",
            "Elimina el sesgo de autoindulgencia con algoritmos auditables y ponderados"
        ) if lang == 'ES' else (
            "Metric Spaces & Cartesian Strategy Vectors",
            "Eliminates executive bias through auditable stochastic weighting models"
        ),
        (
            "Equilibrio de Fondos & Decision Gateways",
            "Autofinanciación de cartera y gobernanza lista para votación en Consejo"
        ) if lang == 'ES' else (
            "Cash Flow Balancing & Boardroom Gateways",
            "Portfolio self-funding and governance slides ready for binding board vote"
        )
    ]

    bullet_y = 188
    for b_title, b_desc in bullets:
        draw.rounded_rectangle([(safe_left, bullet_y + 3), (safe_left + 7, bullet_y + 10)], radius=2, fill=(245, 158, 11))
        draw.text((safe_left + 18, bullet_y), b_title, fill=(255, 255, 255), font=font_bullet_title)
        draw.text((safe_left + 18, bullet_y + 17), b_desc, fill=(148, 163, 184), font=font_bullet_desc)
        bullet_y += 46

    # 8. Píldoras de entregables
    pill_y = 338
    pills = [
        ("10 Modelos Excel + Sheets", (37, 99, 235)),
        ("10 Decks PPTX 16:9", (245, 158, 11)),
        ("5 Guías Metodológicas PDF", (13, 148, 136))
    ] if lang == 'ES' else [
        ("10 Excel + Sheets Models", (37, 99, 235)),
        ("10 PPTX 16:9 Decks", (245, 158, 11)),
        ("5 PDF Guides", (13, 148, 136))
    ]

    cur_x = safe_left
    for p_text, p_col in pills:
        bbox = font_pill.getbbox(p_text)
        pw = (bbox[2] - bbox[0]) + 18
        ph = 25
        draw.rounded_rectangle([(cur_x, pill_y), (cur_x + pw, pill_y + ph)], radius=12, fill=(15, 23, 42), outline=p_col, width=1)
        draw.text((cur_x + 9, pill_y + 5), p_text, fill=(255, 255, 255), font=font_pill)
        cur_x += pw + 8

    # 9. Bloque Comercial Integrado
    offer_box_x = safe_left
    offer_box_y = 384
    offer_w = 465
    offer_h = 68
    draw.rounded_rectangle(
        [(offer_box_x, offer_box_y), (offer_box_x + offer_w, offer_box_y + offer_h)],
        radius=8,
        fill=(20, 30, 52),
        outline=(56, 189, 248),
        width=1
    )

    # Insignia de descuento dentro del bloque
    badge_save = "AHORRO 32% • PACK COMPLETO" if lang == 'ES' else "SAVE 32% • FULL BUNDLE"
    draw.rounded_rectangle(
        [(offer_box_x + 14, offer_box_y + 11), (offer_box_x + 215, offer_box_y + 30)],
        radius=4,
        fill=(16, 185, 129)
    )
    draw.text((offer_box_x + 20, offer_box_y + 14), badge_save, fill=(255, 255, 255), font=font_node_bold)

    offer_desc = "Suite 01: PESTEL + Porter + DAFO + BCG + McKinsey" if lang == 'ES' else "Suite 01: PESTEL + Porter + SWOT + BCG + McKinsey"
    draw.text((offer_box_x + 14, offer_box_y + 39), offer_desc, fill=(203, 213, 225), font=font_bullet_desc)

    # Precios
    draw.text((offer_box_x + 335, offer_box_y + 14), "19 €", fill=(245, 158, 11), font=font_price_main)
    draw.text((offer_box_x + 394, offer_box_y + 18), "28 €", fill=(148, 163, 184), font=font_price_strike)
    strike_bbox = font_price_strike.getbbox("28 €")
    sw = strike_bbox[2] - strike_bbox[0]
    draw.line([(offer_box_x + 392, offer_box_y + 26), (offer_box_x + 392 + sw + 4, offer_box_y + 26)], fill=(239, 68, 68), width=2)
    draw.text((offer_box_x + 335, offer_box_y + 42), "Acceso Inmediato" if lang == 'ES' else "Instant Access", fill=(148, 163, 184), font=font_tiny)

    # 10. Diagrama Pentagonal Estratégico (Safe Zone Right [670, 1055])
    pentagon_cx = 865
    pentagon_cy = 280
    pentagon_radius = 135
    draw_strategic_pentagon(
        draw,
        pentagon_cx,
        pentagon_cy,
        pentagon_radius,
        font_node_bold,
        font_node_small,
        font_tiny,
        lang=lang
    )

    # Pie de marca inferior (dentro de safe_left)
    footer_text = "DATALARIA.COM • THE QUANTITATIVE MANAGEMENT ENGINE"
    draw.text((safe_left, 568), footer_text, fill=(71, 85, 105), font=font_badge)

    img.save(out_path, format='PNG', optimize=True)
    print(f"Generated {out_path} ({WIDTH}x{HEIGHT})")


if __name__ == '__main__':
    # 1. Versión en Español
    es_path = "content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/cover.png"
    create_cover(lang='ES', out_path=es_path)

    # 2. Versión en Inglés
    en_path = "content/en/posts/corporate-strategy-mba-quantitative-framework/cover.png"
    create_cover(lang='EN', out_path=en_path)
