#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/matriz-mckinsey-ge/cover.png
- content/en/posts/mckinsey-ge-matrix/cover.png

Composición visual de estándar McKinsey / BCG:
- Fondo degradado ejecutivo: Azul Marino #0F172A a Azul Medianoche #1E293B.
- Malla técnica vectorial con puntos de precisión.
- Badge superior izquierdo: "SUITE 01 · ESTRATEGIA MBA" en dorado y azul.
- Título principal de gran contraste y legibilidad en #F8FAFC y ámbar (#F59E0B).
- Subtítulo descriptivo de los ejes y zonas de capital.
- Gráfico abstracto geométrico a la derecha representando la cuadrícula 3x3 con acentos
  en Verde (#10B981), Ámbar (#F59E0B) y Azul (#2563EB) con burbujas de UENs.
- Píldoras de entregables: [📊 Excel + Google Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF Minto].
- Marca de agua / Logo inferior derecho: "DATALARIA.COM · EXECUTIVE DECISION PACKS".
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
    """Dibuja una malla técnica con cuadrículas y puntos sutiles."""
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(22, 34, 54), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(22, 34, 54), width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_mckinsey_grid_graphic(draw, x0, y0, w, h, font_small, font_bold, lang='ES'):
    """
    Dibuja la cuadrícula 3x3 de McKinsey / GE con acentos geométricos,
    zonas de color y burbujas de UENs.
    """
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    cell_w = (w - 20) / 3
    cell_h = (h - 20) / 3

    # Colores de las 3 zonas:
    # Verde (Invertir): (16, 185, 129)
    # Ámbar (Selectividad): (245, 158, 11)
    # Rojo (Cosechar): (239, 68, 68)
    grid_zones = [
        # Fila 0 (Alto Atractivo): [Verde, Verde, Ámbar]
        [(16, 185, 129, 45), (16, 185, 129, 45), (245, 158, 11, 45)],
        # Fila 1 (Medio Atractivo): [Verde, Ámbar, Rojo]
        [(16, 185, 129, 45), (245, 158, 11, 45), (239, 68, 68, 45)],
        # Fila 2 (Bajo Atractivo): [Ámbar, Rojo, Rojo]
        [(245, 158, 11, 45), (239, 68, 68, 45), (239, 68, 68, 45)],
    ]

    border_colors = [
        [(16, 185, 129), (16, 185, 129), (245, 158, 11)],
        [(16, 185, 129), (245, 158, 11), (239, 68, 68)],
        [(245, 158, 11), (239, 68, 68), (239, 68, 68)],
    ]

    fill_tones = [
        [(20, 48, 42), (20, 48, 42), (48, 40, 24)],
        [(20, 48, 42), (48, 40, 24), (48, 24, 28)],
        [(48, 40, 24), (48, 24, 28), (48, 24, 28)],
    ]

    for r in range(3):
        for c in range(3):
            cx0 = x0 + 10 + c * cell_w
            cy0 = y0 + 10 + r * cell_h
            cx1 = cx0 + cell_w - 4
            cy1 = cy0 + cell_h - 4

            # Celda
            b_col = border_colors[r][c]
            f_col = fill_tones[r][c]
            draw.rounded_rectangle([(cx0, cy0), (cx1, cy1)], radius=6, fill=f_col, outline=b_col, width=1)

    # Burbujas destacadas en la cuadrícula
    # UEN-01 (Cloud IA): Celda [0, 0] (Alto, Fuerte)
    b1_x = x0 + 10 + 0.5 * cell_w
    b1_y = y0 + 10 + 0.45 * cell_h
    draw.ellipse([(b1_x - 30, b1_y - 30), (b1_x + 30, b1_y + 30)], fill=(16, 185, 129), outline=(209, 250, 229), width=2)
    draw.text((b1_x - 22, b1_y - 7), "UEN-01", fill=(15, 23, 42), font=font_bold)

    # UEN-02 (Robótica): Celda [0, 1] (Alto, Media)
    b2_x = x0 + 10 + 1.45 * cell_w
    b2_y = y0 + 10 + 0.55 * cell_h
    draw.ellipse([(b2_x - 25, b2_y - 25), (b2_x + 25, b2_y + 25)], fill=(16, 185, 129), outline=(209, 250, 229), width=2)
    draw.text((b2_x - 20, b2_y - 7), "UEN-02", fill=(15, 23, 42), font=font_bold)

    # UEN-04 (Sensores): Celda [1, 1] (Medio, Media)
    b4_x = x0 + 10 + 1.5 * cell_w
    b4_y = y0 + 10 + 1.5 * cell_h
    draw.ellipse([(b4_x - 24, b4_y - 24), (b4_x + 24, b4_y + 24)], fill=(245, 158, 11), outline=(254, 243, 199), width=2)
    draw.text((b4_x - 20, b4_y - 7), "UEN-04", fill=(15, 23, 42), font=font_bold)

    # UEN-06 (HVAC): Celda [2, 0] (Bajo, Fuerte)
    b6_x = x0 + 10 + 0.45 * cell_w
    b6_y = y0 + 10 + 2.45 * cell_h
    draw.ellipse([(b6_x - 22, b6_y - 22), (b6_x + 22, b6_y + 22)], fill=(245, 158, 11), outline=(254, 243, 199), width=2)
    draw.text((b6_x - 18, b6_y - 6), "UEN-06", fill=(15, 23, 42), font=font_small)

    # UEN-10 (Medidores / Salida): Celda [2, 2] (Bajo, Débil)
    b10_x = x0 + 10 + 2.5 * cell_w
    b10_y = y0 + 10 + 2.5 * cell_h
    draw.ellipse([(b10_x - 18, b10_y - 18), (b10_x + 18, b10_y + 18)], fill=(239, 68, 68), outline=(254, 226, 226), width=2)
    draw.text((b10_x - 15, b10_y - 6), "EXIT", fill=(255, 255, 255), font=font_small)

    # Ejes anotados
    # Eje Y vertical a la izquierda
    lbl_y = "ATRACTIVO INDUSTRIA (Y)" if lang == 'ES' else "INDUSTRY ATTRACTIVENESS (Y)"
    draw.text((x0 + 12, y0 - 18), lbl_y, fill=(148, 163, 184), font=font_small)

    # Eje X horizontal abajo
    lbl_x = "FORTALEZA COMPETITIVA UEN (X)" if lang == 'ES' else "BUSINESS UNIT STRENGTH (X)"
    draw.text((x0 + w - 210, y0 + h + 6), lbl_x, fill=(148, 163, 184), font=font_small)

    # Badge Central de Retorno / ROIC Accretion
    badge_w, badge_h = 280, 36
    bx1 = x0 + (w - badge_w) // 2
    by1 = y0 + h - 46
    draw.rounded_rectangle([(bx1, by1), (bx1 + badge_w, by1 + badge_h)], radius=18, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    lbl_bal = "ROIC PROYECTADO: +380 bps" if lang == 'ES' else "PROJECTED ROIC: +380 bps"
    draw.text((bx1 + 28, by1 + 10), lbl_bal, fill=(209, 250, 229), font=font_bold)


def create_cover(lang='ES', out_path='cover.png'):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado ejecutivo Slate 900 -> Slate 800
    draw_linear_gradient(draw, WIDTH, HEIGHT, (15, 23, 42), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes
    font_badge = get_font("segoeuib.ttf", 11)
    font_title_large = get_font("segoeuib.ttf", 41)
    font_subtitle = get_font("segoeui.ttf", 16)
    font_body = get_font("segoeui.ttf", 12)
    font_bold = get_font("segoeuib.ttf", 12.5)
    font_small = get_font("segoeui.ttf", 9.5)
    font_pill = get_font("segoeuib.ttf", 12.5)
    font_footer = get_font("segoeuib.ttf", 10.5)

    # 3. Badge Superior Izquierdo: SUITE 01 · ESTRATEGIA MBA en dorado/azul
    b_x, b_y = 65, 46
    b_w, b_h = 250, 28
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=6, fill=(15, 23, 42), outline=(245, 158, 11), width=1)
    draw.text((b_x + 14, b_y + 7), "SUITE 01 · ESTRATEGIA MBA", fill=(245, 158, 11), font=font_badge)

    # 4. Título Principal de Alto Contraste
    t_y = 92
    if lang == 'ES':
        title_p1 = "MATRIZ MCKINSEY / GE "
        title_p2 = "3x3"
    else:
        title_p1 = "MCKINSEY / GE "
        title_p2 = "3x3 MATRIX"

    draw.text((65, t_y), title_p1, fill=(248, 250, 252), font=font_title_large)
    bbox_p1 = font_title_large.getbbox(title_p1)
    p1_width = bbox_p1[2] - bbox_p1[0]
    draw.text((65 + p1_width, t_y), title_p2, fill=(245, 158, 11), font=font_title_large)

    # 5. Subtítulo Descriptivo de los Ejes y Zonas
    sub_y = 154
    subtitle = (
        "Atractivo de la Industria vs. Fortaleza Competitiva · Asignación de Capital C-Level"
        if lang == 'ES' else
        "Industry Attractiveness vs. Business Unit Strength · C-Level Capital Allocation"
    )
    draw.text((65, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle)

    # Línea divisoria en azul Datalaria
    draw.line([(65, 190), (580, 190)], fill=(37, 99, 235), width=2)

    # 6. Balas de Valor Estratégico
    bullets_es = [
        ("Motor Multifactorial Ponderado", "Evaluación objetiva de 5 factores de mercado y 5 capacidades competitivas."),
        ("Asignación de Capital en 3 Zonas", "Mandato claro: Invertir (Verde), Seleccionar (Ámbar) y Cosechar (Rojo)."),
        ("Gobernanza C-Level & Desbloqueo de ROIC", "Presupuesto a 36 meses, Hurdle Rates (TIR) y plan de carve-out para el Consejo.")
    ]
    bullets_en = [
        ("Weighted Multifactor Scoring Engine", "Rigorous audit of 5 market attractiveness and 5 business strength criteria."),
        ("3-Zone Capital Allocation Mandates", "Actionable governance: Invest (Green), Selectivity (Amber), Harvest (Red)."),
        ("C-Level Governance & ROIC Expansion", "36-month CAPEX roadmap, Hurdle Rates (IRR), and Board carve-out mandates.")
    ]
    bullets = bullets_es if lang == 'ES' else bullets_en

    bullet_y = 212
    for b_title, b_desc in bullets:
        # Puntero cuadrado azul
        draw.rounded_rectangle([(65, bullet_y + 3), (73, bullet_y + 11)], radius=2, fill=(37, 99, 235))
        draw.text((85, bullet_y), b_title, fill=(255, 255, 255), font=font_bold)
        draw.text((85, bullet_y + 20), b_desc, fill=(148, 163, 184), font=font_body)
        bullet_y += 56

    # 7. Píldoras de Entregables (Inferior Izquierda)
    pills = [
        ("📊 Excel + Google Sheets", (37, 99, 235), (239, 246, 255), (29, 78, 216)),
        ("📑 PPTX 16:9 C-Level", (245, 158, 11), (254, 243, 199), (146, 64, 14)),
        ("📄 Guía PDF Minto (5 págs)" if lang == 'ES' else "📄 Minto PDF Guide (5 pgs)", (16, 185, 129), (209, 250, 229), (6, 95, 70))
    ]

    pill_x = 65
    pill_y = 440
    for p_txt, p_border, p_bg, p_fg in pills:
        bbox = font_pill.getbbox(p_txt)
        pw = (bbox[2] - bbox[0]) + 26
        ph = 34
        draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pw, pill_y + ph)], radius=17, fill=(15, 23, 42), outline=p_border, width=2)
        draw.text((pill_x + 13, pill_y + 8), p_txt, fill=(248, 250, 252), font=font_pill)
        pill_x += pw + 12

    # 8. Gráfico Abstracto Geométrico a la Derecha (McKinsey 3x3 Grid)
    grid_x0 = 660
    grid_y0 = 92
    grid_w = 475
    grid_h = 445
    draw_mckinsey_grid_graphic(draw, grid_x0, grid_y0, grid_w, grid_h, font_small, font_bold, lang=lang)

    # 9. Marca de Agua / Logo Inferior Derecho
    footer_text = "DATALARIA.COM · EXECUTIVE DECISION PACKS"
    bbox_f = font_footer.getbbox(footer_text)
    f_w = bbox_f[2] - bbox_f[0]
    draw.text((WIDTH - f_w - 65, HEIGHT - 46), footer_text, fill=(100, 116, 139), font=font_footer)

    # Línea inferior decorativa
    draw.line([(65, HEIGHT - 58), (WIDTH - 65, HEIGHT - 58)], fill=(30, 41, 59), width=1)

    img.save(out_path, format='PNG', quality=95)
    print(f"[OK] Portada generada ({lang}): {out_path}")
    return out_path


def main():
    print("Iniciando generación de portadas cover.png (1200x630 px)...")

    es_cover = os.path.join("content", "es", "posts", "matriz-mckinsey-ge", "cover.png")
    en_cover = os.path.join("content", "en", "posts", "mckinsey-ge-matrix", "cover.png")

    create_cover(lang='ES', out_path=es_cover)
    create_cover(lang='EN', out_path=en_cover)

    print("Portadas generadas exitosamente.")


if __name__ == "__main__":
    main()
