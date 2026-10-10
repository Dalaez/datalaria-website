#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) para el Post Pilar Maestro de la Suite 01:
- content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/cover.png
- content/en/posts/corporate-strategy-mba-quantitative-framework/cover.png

Composición visual de estándar McKinsey / BCG / Bain:
- Fondo Dark Slate (#0B1120 a #0F172A y #1E293B) con degradado suave y malla técnica.
- Diagrama pentagonal geométrico con los 5 vectores estratégicos interconectados:
  PESTEL, Porter, DAFO/CAME, BCG y McKinsey/GE.
- Badge superior corporativo: DATALARIA EXECUTIVE FRAMEWORK • SUITE 01 MEGA BUNDLE
- Título de alto contraste y subtítulo ejecutivo.
- Balas de valor estratégico con viñetas destacadas.
- Píldoras de entregables: [📊 10 Modelos Excel/Sheets] [📑 10 Decks PPTX 16:9] [📄 5 Guías PDF].
- Badge de precio y acceso: 19€ (Valor 28€).
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
    """Dibuja la red pentagonal geométrica que une las 5 herramientas estratégicas."""
    nodes = [
        ("PESTEL", "Macro Shock" if lang == 'EN' else "Entorno Macro", (239, 68, 68), (254, 226, 226)),      # Red / Rose
        ("PORTER", "Industry Moat" if lang == 'EN' else "Atractivo Industria", (245, 158, 11), (254, 243, 199)), # Amber
        ("DAFO/CAME", "Vector Strategy" if lang == 'EN' else "Vector Estratégico", (16, 185, 129), (209, 250, 229)), # Emerald
        ("BCG", "Cash Flow" if lang == 'EN' else "Flujo Fondos", (59, 130, 246), (219, 234, 254)),         # Blue
        ("MCKINSEY", "CAPEX Alloc." if lang == 'EN' else "Asignación CAPEX", (168, 85, 247), (243, 232, 255)) # Purple
    ]

    num_nodes = len(nodes)
    angles = [i * (2 * math.pi / num_nodes) - math.pi / 2 for i in range(num_nodes)]
    coords = []

    for a in angles:
        px = center_x + radius * math.cos(a)
        py = center_y + radius * math.sin(a)
        coords.append((px, py))

    # Círculos orbitales concéntricos tenues
    for r_orb in [radius * 0.4, radius * 0.7, radius * 1.0]:
        bbox = [center_x - r_orb, center_y - r_orb, center_x + r_orb, center_y + r_orb]
        draw.ellipse(bbox, outline=(30, 41, 59), width=1)

    # Líneas de interconexión pentagonal y estrella interna
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            # Si es el anillo exterior, línea más gruesa y luminosa
            if (j == i + 1) or (i == 0 and j == num_nodes - 1):
                draw.line([(x1, y1), (x2, y2)], fill=(56, 189, 248), width=2)
            else:
                # Línea interna de la estrella
                draw.line([(x1, y1), (x2, y2)], fill=(37, 99, 235), width=1)

    # Nodos de las 5 herramientas
    for i, (name, role, col, bg_pill) in enumerate(nodes):
        nx, ny = coords[i]

        # Resplandor exterior
        draw.ellipse([(nx - 36, ny - 36), (nx + 36, ny + 36)], fill=(15, 23, 42), outline=col, width=3)
        # Núcleo
        draw.ellipse([(nx - 28, ny - 28), (nx + 28, ny + 28)], fill=(30, 41, 59))

        # Texto del nodo
        bbox_txt = font_bold.getbbox(name)
        tw = bbox_txt[2] - bbox_txt[0]
        th = bbox_txt[3] - bbox_txt[1]
        draw.text((nx - tw // 2, ny - th // 2 - 2), name, fill=(255, 255, 255), font=font_bold)

        # Etiqueta descriptiva fuera del nodo
        ang = angles[i]
        label_dist = radius + 46
        lx = center_x + label_dist * math.cos(ang)
        ly = center_y + label_dist * math.sin(ang)

        # Ajuste de posición según ángulo
        if math.cos(ang) > 0.3:
            draw.text((lx - 10, ly - 8), role, fill=col, font=font_small)
        elif math.cos(ang) < -0.3:
            b_r = font_small.getbbox(role)
            rw = b_r[2] - b_r[0]
            draw.text((lx - rw + 10, ly - 8), role, fill=col, font=font_small)
        elif math.sin(ang) < 0:
            b_r = font_small.getbbox(role)
            rw = b_r[2] - b_r[0]
            draw.text((lx - rw // 2, ly - 16), role, fill=col, font=font_small)
        else:
            b_r = font_small.getbbox(role)
            rw = b_r[2] - b_r[0]
            draw.text((lx - rw // 2, ly + 4), role, fill=col, font=font_small)

    # Hub Central de Decisión
    hub_w, hub_h = 144, 52
    hx1 = center_x - hub_w // 2
    hy1 = center_y - hub_h // 2
    draw.rounded_rectangle([(hx1, hy1), (hx1 + hub_w, hy1 + hub_h)], radius=10, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    center_title = "DECISION ENGINE" if lang == 'EN' else "MOTOR C-LEVEL"
    bbox_ct = font_bold.getbbox(center_title)
    ctw = bbox_ct[2] - bbox_ct[0]
    draw.text((center_x - ctw // 2, hy1 + 9), center_title, fill=(255, 255, 255), font=font_bold)

    center_sub = "5 Connected Matrices" if lang == 'EN' else "5 Matrices Conectadas"
    bbox_cs = font_tiny.getbbox(center_sub)
    csw = bbox_cs[2] - bbox_cs[0]
    draw.text((center_x - csw // 2, hy1 + 28), center_sub, fill=(245, 158, 11), font=font_tiny)


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
    font_title_large = get_font("segoeuib.ttf", 38)
    font_subtitle = get_font("segoeui.ttf", 16)
    font_bullet_title = get_font("segoeuib.ttf", 13)
    font_bullet_desc = get_font("segoeui.ttf", 12)
    font_pill = get_font("segoeuib.ttf", 12)
    font_node_bold = get_font("segoeuib.ttf", 11)
    font_node_small = get_font("segoeuib.ttf", 10)
    font_tiny = get_font("segoeui.ttf", 9)
    font_price_main = get_font("segoeuib.ttf", 20)
    font_price_strike = get_font("segoeui.ttf", 14)

    # 4. Badge Superior Corporativo
    badge_text = "DATALARIA EXECUTIVE FRAMEWORK • SUITE 01 MEGA BUNDLE"
    b_x, b_y = 65, 45
    b_w, b_h = 475, 28
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text((b_x + 14, b_y + 6), badge_text, fill=(56, 189, 248), font=font_badge)

    # 5. Título Principal
    t_y = 92
    if lang == 'ES':
        title_p1 = "ESTRATEGIA CORPORATIVA "
        title_p2 = "CUANTITATIVA"
    else:
        title_p1 = "QUANTITATIVE CORPORATE "
        title_p2 = "STRATEGY"

    draw.text((65, t_y), title_p1, fill=(255, 255, 255), font=font_title_large)
    bbox_p1 = font_title_large.getbbox(title_p1)
    p1_width = bbox_p1[2] - bbox_p1[0]
    draw.text((65 + p1_width, t_y), title_p2, fill=(245, 158, 11), font=font_title_large)

    # 6. Subtítulo
    sub_y = 152
    subtitle = (
        "El Framework de 5 Pasos para Comités: PESTEL, Porter, DAFO, BCG & McKinsey"
        if lang == 'ES' else
        "The 5-Step Boardroom Framework: PESTEL, Porter, SWOT, BCG & McKinsey"
    )
    draw.text((65, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle)

    # Línea decorativa horizontal
    draw.line([(65, 188), (620, 188)], fill=(37, 99, 235), width=2)

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

    bullet_y = 210
    for b_title, b_desc in bullets:
        # Marcador de viñeta
        draw.rounded_rectangle([(65, bullet_y + 4), (73, bullet_y + 12)], radius=2, fill=(245, 158, 11))
        draw.text((85, bullet_y), b_title, fill=(255, 255, 255), font=font_bullet_title)
        draw.text((85, bullet_y + 18), b_desc, fill=(148, 163, 184), font=font_bullet_desc)
        bullet_y += 50

    # 8. Píldoras de Entregables (Bottom Left)
    pills = [
        ("📊 10 Modelos Excel/Sheets" if lang == 'ES' else "📊 10 Excel/Sheets Models", (37, 99, 235)),
        ("📑 10 Decks PPTX 16:9" if lang == 'ES' else "📑 10 C-Level PPTX Decks", (217, 119, 6)),
        ("📄 5 Guías PDF" if lang == 'ES' else "📄 5 PDF Guides", (13, 148, 136))
    ]

    pill_x = 65
    pill_y = 405
    for p_txt, p_border in pills:
        bbox = font_pill.getbbox(p_txt)
        pw = (bbox[2] - bbox[0]) + 24
        ph = 32
        draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pw, pill_y + ph)], radius=16, fill=(15, 23, 42), outline=p_border, width=2)
        draw.text((pill_x + 12, pill_y + 7), p_txt, fill=(241, 245, 249), font=font_pill)
        pill_x += pw + 12

    # 9. Bloque de Oferta y Ahorro Suite 01 (Bottom Left debajo de las píldoras)
    offer_box_x = 65
    offer_box_y = 460
    offer_w = 480
    offer_h = 70
    draw.rounded_rectangle(
        [(offer_box_x, offer_box_y), (offer_box_x + offer_w, offer_box_y + offer_h)],
        radius=10,
        fill=(20, 30, 52),
        outline=(56, 189, 248),
        width=1
    )

    # Insignia de descuento dentro del bloque
    badge_save = "AHORRO 32% • PACK COMPLETO" if lang == 'ES' else "SAVE 32% • FULL BUNDLE"
    draw.rounded_rectangle(
        [(offer_box_x + 16, offer_box_y + 12), (offer_box_x + 230, offer_box_y + 32)],
        radius=4,
        fill=(16, 185, 129)
    )
    draw.text((offer_box_x + 24, offer_box_y + 15), badge_save, fill=(255, 255, 255), font=font_node_bold)

    offer_desc = "Suite 01: PESTEL + Porter + DAFO + BCG + McKinsey" if lang == 'ES' else "Suite 01: PESTEL + Porter + SWOT + BCG + McKinsey"
    draw.text((offer_box_x + 16, offer_box_y + 40), offer_desc, fill=(203, 213, 225), font=font_bullet_desc)

    # Precios
    draw.text((offer_box_x + 350, offer_box_y + 16), "19 €", fill=(245, 158, 11), font=font_price_main)
    draw.text((offer_box_x + 412, offer_box_y + 20), "28 €", fill=(148, 163, 184), font=font_price_strike)
    # Línea tachada sobre 28 €
    strike_bbox = font_price_strike.getbbox("28 €")
    sw = strike_bbox[2] - strike_bbox[0]
    draw.line([(offer_box_x + 410, offer_box_y + 28), (offer_box_x + 410 + sw + 4, offer_box_y + 28)], fill=(239, 68, 68), width=2)
    draw.text((offer_box_x + 350, offer_box_y + 44), "Acceso Inmediato" if lang == 'ES' else "Instant Access", fill=(148, 163, 184), font=font_tiny)

    # 10. Diagrama Pentagonal Estratégico (Center-Right)
    pentagon_cx = 920
    pentagon_cy = 315
    pentagon_radius = 175
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

    # Pie de marca inferior
    footer_text = "DATALARIA.COM • THE QUANTITATIVE MANAGEMENT ENGINE"
    draw.text((65, 580), footer_text, fill=(71, 85, 105), font=font_badge)

    img.save(out_path, "PNG", optimize=True)
    print(f"Portada generada con éxito en: {out_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    es_path = os.path.join(base_dir, "content", "es", "posts", "estrategia-corporativa-mba-framework-cuantitativo", "cover.png")
    en_path = os.path.join(base_dir, "content", "en", "posts", "corporate-strategy-mba-quantitative-framework", "cover.png")

    create_cover(lang='ES', out_path=es_path)
    create_cover(lang='EN', out_path=en_path)
