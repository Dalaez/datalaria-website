#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/matriz-pestel-cuantitativa/cover.png
- content/en/posts/quantitative-pestel-matrix/cover.png

Composición visual de estándar McKinsey / BCG:
- Fondo: Degradado Dark Slate / Navy (#0B1120 a #0F172A y #1E293B) con malla técnica y cuadrantes.
- Badge superior corporativo Datalaria con borde azul consultoría (#2563EB).
- Título principal de alto contraste en blanco y oro ámbar (#F59E0B).
- Subtítulo ejecutivo y balas de valor estratégico.
- Elemento gráfico central: Radar hexagonal PESTEL con nodos (P, E, S, T, E, L) y polígono cuantitativo.
- Píldoras de entregables: [📊 Excel + Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF].
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
        for x in range(0, width, 2):  # optimización por pasos
            ratio_x = x / width
            blend = (ratio_x * 0.4 + ratio_y * 0.6)
            r = int(r1 + (r2 - r1) * blend)
            g = int(g1 + (g2 - g1) * blend)
            b = int(b1 + (b2 - b1) * blend)
            draw.line([(x, y), (x + 1, y)], fill=(r, g, b))


def draw_technical_grid(draw, width, height):
    """Dibuja una malla técnica con cuadrículas y puntos sutiles."""
    grid_color = (30, 41, 59, 120)  # Slate 800 sutil
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48), width=1)

    # Cruces sutiles en intersecciones cada 120px
    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_hexagon_radar(draw, center_x, center_y, max_radius, font_small, font_bold, lang='ES'):
    """Dibuja el radar hexagonal de las 6 dimensiones PESTEL."""
    labels = [
        ("P", "Político" if lang == 'ES' else "Political", 3.82, (244, 63, 94)),     # Rose
        ("E", "Económico" if lang == 'ES' else "Economic", 4.10, (245, 158, 11)),   # Amber
        ("S", "Social" if lang == 'ES' else "Social", 3.12, (34, 197, 94)),        # Green
        ("T", "Tecnológico" if lang == 'ES' else "Tech", 4.41, (168, 85, 247)),     # Purple
        ("E", "Ecológico" if lang == 'ES' else "Environ.", 3.52, (20, 184, 166)),   # Teal
        ("L", "Legal" if lang == 'ES' else "Legal", 4.15, (99, 102, 241))          # Indigo
    ]

    num_axes = 6
    angles = [i * (2 * math.pi / num_axes) - math.pi / 2 for i in range(num_axes)]

    # 1. Cuadrícula concéntrica hexagonal (5 niveles de 1 a 5)
    for level in range(1, 6):
        r = max_radius * (level / 5.0)
        points = []
        for a in angles:
            px = center_x + r * math.cos(a)
            py = center_y + r * math.sin(a)
            points.append((px, py))
        points.append(points[0])
        # Dibujar líneas del nivel
        for p_idx in range(len(points) - 1):
            draw.line([points[p_idx], points[p_idx + 1]], fill=(51, 65, 85), width=1)

    # 2. Ejes radiales
    for a in angles:
        ex = center_x + max_radius * math.cos(a)
        ey = center_y + max_radius * math.sin(a)
        draw.line([(center_x, center_y), (ex, ey)], fill=(71, 85, 105), width=1)

    # 3. Polígono de datos cuantitativo
    data_points = []
    for (code, name, score, col), a in zip(labels, angles):
        r_val = max_radius * (score / 5.0)
        px = center_x + r_val * math.cos(a)
        py = center_y + r_val * math.sin(a)
        data_points.append((px, py))

    # Relleno translúcido simulado mediante líneas concéntricas
    for step_ratio in [0.2, 0.4, 0.6, 0.8, 1.0]:
        inner_pts = []
        for px, py in data_points:
            ix = center_x + (px - center_x) * step_ratio
            iy = center_y + (py - center_y) * step_ratio
            inner_pts.append((ix, iy))
        inner_pts.append(inner_pts[0])
        for p_idx in range(len(inner_pts) - 1):
            draw.line([inner_pts[p_idx], inner_pts[p_idx + 1]], fill=(37, 99, 235), width=2)

    # Contorno exterior del polígono
    data_pts_closed = data_points + [data_points[0]]
    for p_idx in range(len(data_pts_closed) - 1):
        draw.line([data_pts_closed[p_idx], data_pts_closed[p_idx + 1]], fill=(56, 189, 248), width=3)

    # 4. Nodos de datos en cada vértice
    for px, py in data_points:
        draw.ellipse([(px - 5, py - 5), (px + 5, py + 5)], fill=(255, 255, 255), outline=(37, 99, 235), width=2)

    # 5. Etiquetas de los 6 pilares en los extremos
    for (code, name, score, col), a in zip(labels, angles):
        label_r = max_radius + 36
        lx = center_x + label_r * math.cos(a)
        ly = center_y + label_r * math.sin(a)

        # Círculo insignia del pilar
        node_r = 18
        draw.ellipse([(lx - node_r, ly - node_r), (lx + node_r, ly + node_r)], fill=(15, 23, 42), outline=col, width=2)
        # Letra pilar (P, E, S, T, E, L)
        draw.text((lx - 5, ly - 8), code, fill=(255, 255, 255), font=font_bold)

        # Texto y Score debajo/al lado
        score_txt = f"{score:.1f}"
        if math.cos(a) > 0.3:
            draw.text((lx + 24, ly - 10), name, fill=(241, 245, 249), font=font_bold)
            draw.text((lx + 24, ly + 4), f"R: {score_txt}/5", fill=col, font=font_small)
        elif math.cos(a) < -0.3:
            draw.text((lx - 75, ly - 10), name, fill=(241, 245, 249), font=font_bold)
            draw.text((lx - 75, ly + 4), f"R: {score_txt}/5", fill=col, font=font_small)
        elif math.sin(a) < 0:
            draw.text((lx - 25, ly - 36), f"{name} ({score_txt})", fill=(241, 245, 249), font=font_bold)
        else:
            draw.text((lx - 25, ly + 22), f"{name} ({score_txt})", fill=(241, 245, 249), font=font_bold)

    # Badge central del índice consolidado
    badge_w, badge_h = 130, 44
    bx1 = center_x - badge_w // 2
    by1 = center_y - badge_h // 2
    draw.rounded_rectangle([(bx1, by1), (bx1 + badge_w, by1 + badge_h)], radius=8, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    lbl_r = "R_comp = 3.82"
    draw.text((bx1 + 14, by1 + 6), lbl_r, fill=(255, 255, 255), font=font_bold)
    sub_r = "RIESGO ELEVADO" if lang == 'ES' else "HIGH MACRO RISK"
    draw.text((bx1 + 18, by1 + 24), sub_r, fill=(245, 158, 11), font=font_small)


def create_cover(lang='ES', out_path='cover.png'):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado Slate Dark
    draw_linear_gradient(draw, WIDTH, HEIGHT, (11, 17, 32), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes
    font_kicker = get_font("segoeuib.ttf", 12)
    font_title_large = get_font("segoeuib.ttf", 44)
    font_subtitle = get_font("segoeui.ttf", 17)
    font_body = get_font("segoeui.ttf", 13)
    font_bold = get_font("segoeuib.ttf", 13)
    font_small = get_font("segoeui.ttf", 10)
    font_pill = get_font("segoeuib.ttf", 13)

    # 3. Badge Superior Corporativo
    badge_text = "DATALARIA EXECUTIVE DECISION PACK • MCKINSEY & BCG STANDARD"
    b_x, b_y = 65, 52
    b_w, b_h = 490, 30
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text((b_x + 16, b_y + 8), badge_text, fill=(56, 189, 248), font=font_kicker)

    # 4. Título Principal
    t_y = 104
    title_p1 = "MATRIZ PESTEL " if lang == 'ES' else "QUANTITATIVE "
    title_p2 = "CUANTITATIVA" if lang == 'ES' else "PESTEL MATRIX"

    draw.text((65, t_y), title_p1, fill=(255, 255, 255), font=font_title_large)
    bbox_p1 = font_title_large.getbbox(title_p1)
    p1_width = bbox_p1[2] - bbox_p1[0]
    draw.text((65 + p1_width, t_y), title_p2, fill=(245, 158, 11), font=font_title_large)

    # 5. Subtítulo
    sub_y = 168
    subtitle = (
        "Severidad del Impacto, Volatilidad & Resiliencia Macro para Comités de Dirección"
        if lang == 'ES' else
        "Severity, Volatility & Macro Resilience for Executive Board Decisions"
    )
    draw.text((65, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle)

    # Línea decorativa horizontal
    draw.line([(65, 206), (560, 206)], fill=(37, 99, 235), width=2)

    # 6. Balas de valor estratégico
    bullets = [
        ("Motor Cuantitativo Bidimensional", "Severidad en P&L vs. Volatilidad Temporal en escala 1-5") if lang == 'ES' else
        ("2D Quantitative Macro Engine", "Audited P&L Severity vs. Temporal Volatility on 1-5 scale"),

        ("Matriz Cartesiana de Incertidumbre", "4 cuadrantes: Críticos Volátiles, Estructurales, Alertas y Ruido") if lang == 'ES' else
        ("Cartesian Uncertainty Mapping", "4 quadrants: Critical Volatile, Structural, Early Warning & Noise"),

        ("Roadmap de Contingencia & Resoluciones", "8 iniciativas con Owner C-Level y 3 resoluciones de Consejo") if lang == 'ES' else
        ("Contingency Roadmap & Board Gateway", "8 C-Suite initiatives and 3 binding Board resolutions")
    ]

    bullet_y = 230
    for b_title, b_desc in bullets:
        # Marcador de viñeta
        draw.rounded_rectangle([(65, bullet_y + 4), (73, bullet_y + 12)], radius=2, fill=(37, 99, 235))
        draw.text((85, bullet_y), b_title, fill=(255, 255, 255), font=font_bold)
        draw.text((85, bullet_y + 20), b_desc, fill=(148, 163, 184), font=font_body)
        bullet_y += 54

    # 7. Píldoras de Entregables (Bottom Left)
    pills = [
        ("📊 Excel + Sheets", (37, 99, 235), (239, 246, 255), (29, 78, 216)),
        ("📑 PPTX 16:9 C-Level", (217, 119, 6), (255, 251, 235), (146, 64, 14)),
        ("📄 Guía PDF (5 págs)" if lang == 'ES' else "📄 PDF Guide (5 pgs)", (13, 148, 136), (240, 253, 250), (15, 118, 110))
    ]

    pill_x = 65
    pill_y = 445
    for p_txt, p_border, p_bg, p_fg in pills:
        bbox = font_pill.getbbox(p_txt)
        pw = (bbox[2] - bbox[0]) + 30
        ph = 36
        draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pw, pill_y + ph)], radius=18, fill=(15, 23, 42), outline=p_border, width=2)
        draw.text((pill_x + 15, pill_y + 9), p_txt, fill=(255, 255, 255), font=font_pill)
        pill_x += pw + 14

    # 8. Barra inferior de pie
    draw.line([(65, 545), (1135, 545)], fill=(51, 65, 85), width=1)
    foot_left = "Datalaria.com • Official Executive Decision Pack 2026 • Confidential & Licensed"
    foot_right = "Descarga Directa Inmediata (.ZIP)" if lang == 'ES' else "Instant Direct Download (.ZIP)"
    draw.text((65, 560), foot_left, fill=(100, 116, 139), font=font_small)
    bbox_fr = font_small.getbbox(foot_right)
    draw.text((1135 - (bbox_fr[2] - bbox_fr[0]), 560), foot_right, fill=(56, 189, 248), font=font_small)

    # 9. Elemento Gráfico Central: Radar Hexagonal PESTEL
    radar_center_x = 880
    radar_center_y = 285
    radar_radius = 165
    draw_hexagon_radar(draw, radar_center_x, radar_center_y, radar_radius, font_small, font_bold, lang=lang)

    # Guardar imagen en disco
    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Portada generada ({lang}): {out_path} ({os.path.getsize(out_path)} bytes)")


def main():
    path_es = os.path.join("content", "es", "posts", "matriz-pestel-cuantitativa", "cover.png")
    path_en = os.path.join("content", "en", "posts", "quantitative-pestel-matrix", "cover.png")

    create_cover(lang='ES', out_path=path_es)
    create_cover(lang='EN', out_path=path_en)


if __name__ == '__main__':
    main()
