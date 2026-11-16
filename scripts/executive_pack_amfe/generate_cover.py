#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera las imágenes de portada cover.png de alta resolución (1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/matriz-riesgos-amfe-fmea/cover.png
- content/en/posts/quantitative-risk-matrix-fmea/cover.png

Composición visual calibrada para PaperMod Safe-Zone (sin solapes ni cajas Unicode):
- Fondo: Degradado Dark Slate (#0F172A a #1E293B) con malla técnica sutil.
- Badge superior ajustado dinámicamente al texto.
- Título principal encuadrado en la columna izquierda (x: 56..552).
- Panel analítico derecho (x0: 584..1144): Matriz 5x5 ISO 31000 + Top 5 FMEA Pareto descendente + ROI CER 5.1x.
- Iconos vectoriales nativos en Pillow (cero rectángulos tofu de fuentes sin emoji).
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
        "C:/Windows/Fonts/arial.ttf",
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
            blend = ratio_x * 0.4 + ratio_y * 0.6
            r = int(r1 + (r2 - r1) * blend)
            g = int(g1 + (g2 - g1) * blend)
            b = int(b1 + (b2 - b1) * blend)
            draw.line([(x, y), (x + 1, y)], fill=(r, g, b))


def draw_technical_grid(draw, width, height):
    """Dibuja una malla técnica con cuadrículas y marcas de precisión."""
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48), width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_icon_excel(draw, x, y, color):
    """Icono vectorial minimalista de cuadrícula Excel."""
    draw.rounded_rectangle([(x, y), (x + 16, y + 16)], radius=3, fill=color)
    draw.line([(x + 5, y + 3), (x + 5, y + 13)], fill=(255, 255, 255), width=1)
    draw.line([(x + 10, y + 3), (x + 10, y + 13)], fill=(255, 255, 255), width=1)
    draw.line([(x + 3, y + 8), (x + 13, y + 8)], fill=(255, 255, 255), width=1)


def draw_icon_deck(draw, x, y, color):
    """Icono vectorial de presentación 16:9."""
    draw.rounded_rectangle([(x, y + 1), (x + 16, y + 13)], radius=2, fill=color)
    draw.line([(x + 8, y + 13), (x + 8, y + 16)], fill=color, width=2)
    draw.line([(x + 4, y + 16), (x + 12, y + 16)], fill=color, width=2)
    draw.rectangle([(x + 3, y + 5), (x + 6, y + 10)], fill=(255, 255, 255))
    draw.rectangle([(x + 8, y + 3), (x + 11, y + 10)], fill=(255, 255, 255))


def draw_icon_pdf(draw, x, y, color):
    """Icono vectorial de documento PDF."""
    draw.rounded_rectangle([(x + 1, y), (x + 15, y + 16)], radius=2, fill=color)
    draw.line([(x + 4, y + 5), (x + 12, y + 5)], fill=(255, 255, 255), width=2)
    draw.line([(x + 4, y + 9), (x + 12, y + 9)], fill=(255, 255, 255), width=1)
    draw.line([(x + 4, y + 12), (x + 9, y + 12)], fill=(255, 255, 255), width=1)


def draw_icon_bolt(draw, x, y, color):
    """Rayo vectorial de descarga inmediata."""
    pts = [(x + 8, y), (x + 2, y + 9), (x + 7, y + 9), (x + 5, y + 16), (x + 13, y + 7), (x + 8, y + 7)]
    draw.polygon(pts, fill=color)


def draw_icon_check(draw, x, y, color):
    """Checkmark vectorial nítido."""
    draw.ellipse([(x, y), (x + 16, y + 16)], fill=color)
    draw.line([(x + 4, y + 8), (x + 7, y + 11), (x + 12, y + 5)], fill=(15, 23, 42), width=2)


def draw_fmea_graphic(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang="ES"):
    """Panel analítico derecho con Matriz 5x5, Top 5 Pareto AIAG-VDA y veredicto CER."""
    draw.rounded_rectangle(
        [(x0, y0), (x0 + w, y0 + h)],
        radius=14,
        fill=(15, 23, 42),
        outline=(51, 65, 85),
        width=2,
    )

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR ISO 31000 / FMEA" if lang == "ES" else "ISO 31000 & FMEA ENGINE"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(45, 212, 191), font=font_bold)
    sub_panel = "NPR = S x O x D · CER 5,1x" if lang == "ES" else "RPN = S x O x D · CER 5.1x"
    sub_bbox = font_small.getbbox(sub_panel)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text((x0 + w - sub_w - 16, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. MINI MATRIZ DE CALOR 5x5
    y_content = y0 + 50
    lbl_matrix = "1. MATRIZ DE CALOR 5x5 (PROB. VS. IMPACTO)" if lang == "ES" else "1. 5x5 HEAT MAP (PROB. VS. IMPACT)"
    draw.text((x0 + 16, y_content), lbl_matrix, fill=(56, 189, 248), font=font_bold)

    gx0 = x0 + 16
    gy0 = y_content + 24
    cell_size = 28
    gap = 4

    colors_5x5 = [
        [(254, 243, 199), (254, 243, 199), (254, 226, 226), (254, 226, 226), (254, 226, 226)],
        [(209, 250, 229), (254, 243, 199), (254, 243, 199), (254, 226, 226), (254, 226, 226)],
        [(209, 250, 229), (209, 250, 229), (254, 243, 199), (254, 243, 199), (254, 226, 226)],
        [(209, 250, 229), (209, 250, 229), (209, 250, 229), (254, 243, 199), (254, 243, 199)],
        [(209, 250, 229), (209, 250, 229), (209, 250, 229), (209, 250, 229), (254, 243, 199)],
    ]
    outlines_5x5 = [
        [(245, 158, 11), (245, 158, 11), (220, 38, 38), (220, 38, 38), (220, 38, 38)],
        [(16, 185, 129), (245, 158, 11), (245, 158, 11), (220, 38, 38), (220, 38, 38)],
        [(16, 185, 129), (16, 185, 129), (245, 158, 11), (245, 158, 11), (220, 38, 38)],
        [(16, 185, 129), (16, 185, 129), (16, 185, 129), (245, 158, 11), (245, 158, 11)],
        [(16, 185, 129), (16, 185, 129), (16, 185, 129), (16, 185, 129), (245, 158, 11)],
    ]
    counts_5x5 = {
        (0, 3): "1",
        (0, 1): "1",
        (0, 2): "2",
        (1, 2): "2",
        (1, 3): "4",
        (1, 1): "1",
        (2, 3): "3",
        (2, 2): "3",
        (2, 1): "1",
    }

    for r in range(5):
        for c in range(5):
            cx = gx0 + c * (cell_size + gap)
            cy = gy0 + r * (cell_size + gap)
            bg = colors_5x5[r][c]
            ot = outlines_5x5[r][c]
            draw.rounded_rectangle([(cx, cy), (cx + cell_size, cy + cell_size)], radius=4, fill=bg, outline=ot, width=1)
            val_cnt = counts_5x5.get((r, c), "")
            if val_cnt:
                txt_col = (153, 27, 27) if ot == (220, 38, 38) else ((146, 64, 14) if ot == (245, 158, 11) else (6, 95, 70))
                draw.text((cx + 10, cy + 6), val_cnt, fill=txt_col, font=font_bold)

    lx0 = gx0 + 5 * (cell_size + gap) + 18
    ly0 = gy0 + 12
    legend_rows = [
        ((254, 226, 226), (220, 38, 38), "Zona Crítica (15-25): 5 riesgos" if lang == "ES" else "Critical Zone (15-25): 5 risks"),
        ((254, 243, 199), (245, 158, 11), "Zona Media (8-12): 14 riesgos" if lang == "ES" else "Medium Zone (8-12): 14 risks"),
        ((209, 250, 229), (16, 185, 129), "Zona Baja (1-6): 1 riesgo" if lang == "ES" else "Low Zone (1-6): 1 risk"),
    ]
    for bg_l, ot_l, txt_l in legend_rows:
        draw.rounded_rectangle([(lx0, ly0), (lx0 + 14, ly0 + 14)], radius=3, fill=bg_l, outline=ot_l, width=1)
        draw.text((lx0 + 22, ly0 + 1), txt_l, fill=(241, 245, 249), font=font_small)
        ly0 += 28

    # Línea divisoria
    draw.line([(x0 + 16, gy0 + 170), (x0 + w - 16, gy0 + 170)], fill=(51, 65, 85), width=1)

    # 3. BARRAS PARETO DE MODOS DE FALLO (AIAG-VDA en orden descendente exacto del Excel)
    y_pareto = gy0 + 182
    lbl_pareto = "2. TOP MODOS DE FALLO POR NPR (CRITICIDAD AIAG-VDA)" if lang == "ES" else "2. TOP FAILURE MODES BY RPN (AIAG-VDA CRITICALITY)"
    draw.text((x0 + 16, y_pareto), lbl_pareto, fill=(56, 189, 248), font=font_bold)

    fmea_bars_data = [
        ("Acceso Indebido / Ciber", 441, (220, 38, 38), "NPR 441 · AP ALTA"),
        ("Corrupción BBDD Cloud", 360, (220, 38, 38), "NPR 360 · AP ALTA"),
        ("Soldadura Robótica (Planta)", 360, (220, 38, 38), "NPR 360 · AP ALTA"),
        ("Pasarela de Pagos Core", 336, (245, 158, 11), "NPR 336 · AP ALTA"),
        ("Lag Colas Mensajería", 294, (245, 158, 11), "NPR 294 · AP ALTA"),
    ] if lang == "ES" else [
        ("Unauthorized Access", 441, (220, 38, 38), "RPN 441 · HIGH AP"),
        ("Cloud Database Corrupt.", 360, (220, 38, 38), "RPN 360 · HIGH AP"),
        ("Robotic Weld Misalign.", 360, (220, 38, 38), "RPN 360 · HIGH AP"),
        ("Payment Gateway Core", 336, (245, 158, 11), "RPN 336 · HIGH AP"),
        ("Message Broker Lag", 294, (245, 158, 11), "RPN 294 · HIGH AP"),
    ]

    bar_start_y = y_pareto + 24
    max_bar_w = 195
    bx0 = x0 + 178
    bx_end = bx0 + max_bar_w

    for i, (f_name, f_npr, f_col, f_tag) in enumerate(fmea_bars_data):
        by = bar_start_y + i * 28
        draw.text((x0 + 16, by + 2), f_name, fill=(241, 245, 249), font=font_small)
        draw.rounded_rectangle([(bx0, by + 3), (bx_end, by + 16)], radius=3, fill=(30, 41, 59))
        fill_w = int((f_npr / 500.0) * max_bar_w)
        draw.rounded_rectangle([(bx0, by + 3), (bx0 + fill_w, by + 16)], radius=3, fill=f_col)
        draw.text((bx_end + 12, by + 2), f_tag, fill=f_col, font=font_bold)

    draw.line([(x0 + 16, bar_start_y + 148), (x0 + w - 16, bar_start_y + 148)], fill=(51, 65, 85), width=1)

    # 4. VEREDICTO DE MITIGACIÓN & RIESGO RESIDUAL
    y_win = bar_start_y + 158
    draw.rounded_rectangle([(x0 + 16, y_win), (x0 + w - 16, y_win + 52)], radius=8, fill=(16, 46, 36), outline=(16, 185, 129), width=2)
    draw_icon_check(draw, x0 + 28, y_win + 9, (16, 185, 129))

    win_title = "RIESGO RESIDUAL REDUCIDO: -89,0% POST-MITIGACIÓN" if lang == "ES" else "RESIDUAL RISK REDUCED: -89.0% POST-MITIGATION"
    draw.text((x0 + 52, y_win + 9), win_title, fill=(209, 250, 229), font=font_bold)

    win_sub = (
        "360.000 € CAPEX protegen 1.843.000 € de pérdida esperada (CER 5,1x)"
        if lang == "ES" else
        "€360k CAPEX ringfences €1.843M in expected financial loss (CER 5.1x)"
    )
    draw.text((x0 + 52, y_win + 29), win_sub, fill=(110, 231, 183), font=font_small)


def generate_cover_image(lang="ES", out_path=None):
    if out_path is None:
        out_path = (
            "content/es/posts/matriz-riesgos-amfe-fmea/cover.png"
            if lang == "ES"
            else "content/en/posts/quantitative-risk-matrix-fmea/cover.png"
        )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    draw_linear_gradient(draw, WIDTH, HEIGHT, (15, 23, 42), (30, 41, 59))
    draw_technical_grid(draw, WIDTH, HEIGHT)

    font_kicker = get_font("segoeuib.ttf", 13)
    font_title = get_font("segoeuib.ttf", 31)
    font_sub = get_font("segoeui.ttf", 17)
    font_pill = get_font("segoeuib.ttf", 14)
    font_watermark = get_font("segoeuib.ttf", 12)
    font_bold = get_font("segoeuib.ttf", 12)
    font_small = get_font("segoeui.ttf", 11)
    font_mono = get_font("consola.ttf", 11)

    # 3. Textos Principales en Zona Segura Izquierda (x: 56 .. 554)
    badge_text = "DATALARIA EXECUTIVE PACK • ISO 31000 / AIAG-VDA"
    b_box = font_kicker.getbbox(badge_text)
    badge_w = (b_box[2] - b_box[0]) + 28
    draw.rounded_rectangle([(56, 48), (56 + badge_w, 78)], radius=6, fill=(13, 148, 136), outline=(20, 184, 166), width=1)
    draw.text((70, 54), badge_text, fill=(255, 255, 255), font=font_kicker)

    if lang == "ES":
        title_line1 = "MATRIZ DE RIESGOS"
        title_line2 = "& AMFE / FMEA CUANTITATIVO"
        subtitle_line1 = "Cuantificación de Fallos, Matriz de Calor 5x5"
        subtitle_line2 = "y Cálculo de Prioridad de Riesgo (NPR)"
    else:
        title_line1 = "QUANTITATIVE RISK MATRIX"
        title_line2 = "& OPERATIONAL FMEA"
        subtitle_line1 = "Failure Mode Quantification, 5x5 Heat Map"
        subtitle_line2 = "and Risk Priority Number (RPN) Engine"

    draw.text((56, 102), title_line1, fill=(255, 255, 255), font=font_title)
    draw.text((56, 146), title_line2, fill=(56, 189, 248), font=font_title)

    draw.text((56, 206), subtitle_line1, fill=(203, 213, 225), font=font_sub)
    draw.text((56, 234), subtitle_line2, fill=(148, 163, 184), font=font_sub)

    # Píldoras de Entregables con iconos vectoriales (cero cajas tofu)
    pills = [
        ("Excel + Google Sheets", (37, 99, 235), draw_icon_excel),
        ("Deck PPTX 16:9 C-Level", (13, 148, 136), draw_icon_deck),
        ("Guía Metodológica PDF", (220, 38, 38), draw_icon_pdf),
    ] if lang == "ES" else [
        ("Excel + Google Sheets", (37, 99, 235), draw_icon_excel),
        ("16:9 C-Level PPTX Deck", (13, 148, 136), draw_icon_deck),
        ("Methodology Guide PDF", (220, 38, 38), draw_icon_pdf),
    ]

    py = 294
    for text, col, icon_fn in pills:
        draw.rounded_rectangle([(56, py), (370, py + 38)], radius=6, fill=(15, 23, 42), outline=col, width=2)
        icon_fn(draw, 70, py + 11, col)
        draw.text((96, py + 9), text, fill=(241, 245, 249), font=font_pill)
        py += 50

    # Tarjeta de Garantía
    draw.rounded_rectangle([(56, 462), (542, 518)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw_icon_bolt(draw, 70, 482, (245, 158, 11))
    tag_es = "Descarga directa inmediata (.ZIP) | Protección ECMA-376 | Editables"
    tag_en = "Instant direct download (.ZIP) | ECMA-376 Protection | Editable Inputs"
    draw.text((92, 482), tag_es if lang == "ES" else tag_en, fill=(226, 232, 240), font=font_small)

    # Watermark en safe-zone inferior
    draw.text((56, 558), "DATALARIA.COM · EXECUTIVE DECISION PACKS · CONTROL OPERATIVO", fill=(100, 116, 139), font=font_watermark)

    # 4. Panel Gráfico del Lado Derecho (separación limpia de >= 30 px respecto a textos izquierda)
    draw_fmea_graphic(draw, x0=584, y0=48, w=560, h=534, font_small=font_small, font_bold=font_bold, font_mono=font_mono, lang=lang)

    img.save(out_path, "PNG", optimize=True)
    print(f"  -> Portada generada exitosamente: {out_path}")


def main():
    print("[1/2] Generando cover.png en Español...")
    generate_cover_image(lang="ES")
    print("[2/2] Generando cover.png en Inglés...")
    generate_cover_image(lang="EN")
    print("\n✓ Generación de portadas cover.png completada con éxito.")


if __name__ == "__main__":
    main()
