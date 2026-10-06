#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera las imágenes de portada cover.png de alta resolución (1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/matriz-riesgos-amfe-fmea/cover.png
- content/en/posts/quantitative-risk-matrix-fmea/cover.png

Composición visual de estándar McKinsey / ISO 31000 / AIAG-VDA:
- Fondo: Degradado Dark Slate (#0F172A a #1E293B) con malla técnica sutil.
- Badge superior: "DATALARIA EXECUTIVE DECISION PACK • ISO 31000 / IATF 16949 STANDARD"
- Título principal: "MATRIZ DE RIESGOS & AMFE / FMEA" / "QUANTITATIVE RISK MATRIX & FMEA"
- Subtítulo: "Cuantificación de Fallos, Matriz de Calor 5x5 & Número de Prioridad de Riesgo (NPR)"
- Panel analítico derecho: Cuadrícula 5x5 semafórica conectada a barras Pareto de criticidad y reducción residual.
- Píldoras de entregables: [📊 Excel + Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF].
- Mensaje de garantía: "Descarga directa inmediata (.ZIP)".
- Marca de agua inferior: "DATALARIA.COM · EXECUTIVE DECISION PACKS · CONTROL OPERATIVO".
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48), width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_fmea_graphic(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang='ES'):
    """
    Dibuja el panel analítico del motor AMFE / FMEA:
    - Cabecera: Ecuación tridimensional (NPR = S x O x D · AP).
    - Matriz de Calor 5x5 ISO 31000 estilizada.
    - Barras Pareto de Modos de Fallo por NPR.
    - Veredicto de reducción residual post-mitigación (-71.4%).
    """
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR CUANTITATIVO ISO 31000 / FMEA" if lang == 'ES' else "QUANTITATIVE RISK & FMEA ENGINE"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(13, 148, 136), font=font_bold)
    sub_panel = "NPR = S × O × D · CER = ΔE(L)/Coste" if lang == 'ES' else "RPN = S × O × D · CER = ΔE(L)/Cost"
    draw.text((x0 + w - 215, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. MINI MATRIZ DE CALOR 5x5 (Lado Izquierdo del contenedor interno)
    y_content = y0 + 50
    lbl_matrix = "1. MATRIZ DE CALOR 5x5 (PROB. VS. IMPACTO)" if lang == 'ES' else "1. 5x5 HEAT MAP (PROB. VS. IMPACT)"
    draw.text((x0 + 16, y_content), lbl_matrix, fill=(56, 189, 248), font=font_bold)

    # 5x5 Grid cells
    gx0 = x0 + 16
    gy0 = y_content + 22
    cell_size = 28
    gap = 4

    # Matriz 5x5 con colores semafóricos de puntuación P * I
    # Filas: P = 5 a 1
    # Columnas: I = 1 a 5
    colors_5x5 = [
        # P=5
        [(254, 243, 199), (254, 243, 199), (254, 226, 226), (254, 226, 226), (254, 226, 226)],
        # P=4
        [(209, 250, 229), (254, 243, 199), (254, 243, 199), (254, 226, 226), (254, 226, 226)],
        # P=3
        [(209, 250, 229), (209, 250, 229), (254, 243, 199), (254, 243, 199), (254, 226, 226)],
        # P=2
        [(209, 250, 229), (209, 250, 229), (209, 250, 229), (254, 243, 199), (254, 243, 199)],
        # P=1
        [(209, 250, 229), (209, 250, 229), (209, 250, 229), (209, 250, 229), (254, 243, 199)],
    ]

    outlines_5x5 = [
        # P=5
        [(245, 158, 11), (245, 158, 11), (220, 38, 38), (220, 38, 38), (220, 38, 38)],
        # P=4
        [(16, 185, 129), (245, 158, 11), (245, 158, 11), (220, 38, 38), (220, 38, 38)],
        # P=3
        [(16, 185, 129), (16, 185, 129), (245, 158, 11), (245, 158, 11), (220, 38, 38)],
        # P=2
        [(16, 185, 129), (16, 185, 129), (16, 185, 129), (245, 158, 11), (245, 158, 11)],
        # P=1
        [(16, 185, 129), (16, 185, 129), (16, 185, 129), (16, 185, 129), (245, 158, 11)],
    ]

    counts_5x5 = {
        (0, 3): "1",  # P=5, I=4
        (0, 1): "1",  # P=5, I=2
        (0, 2): "2",  # P=5, I=3
        (1, 2): "2",  # P=4, I=3
        (1, 3): "4",  # P=4, I=4
        (1, 1): "1",  # P=4, I=2
        (2, 3): "3",  # P=3, I=4
        (2, 2): "3",  # P=3, I=3
        (2, 1): "1",  # P=3, I=2
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

    # Leyenda al lado de la matriz 5x5
    lx0 = gx0 + 5 * (cell_size + gap) + 16
    ly0 = gy0 + 10
    draw.rounded_rectangle([(lx0, ly0), (lx0 + 14, ly0 + 14)], radius=3, fill=(254, 226, 226), outline=(220, 38, 38), width=1)
    lbl_cr = "Zona Crítica (Score 15-25): 5 eventos" if lang == 'ES' else "Critical Zone (Score 15-25): 5 events"
    draw.text((lx0 + 22, ly0 + 1), lbl_cr, fill=(241, 245, 249), font=font_small)

    ly0 += 26
    draw.rounded_rectangle([(lx0, ly0), (lx0 + 14, ly0 + 14)], radius=3, fill=(254, 243, 199), outline=(245, 158, 11), width=1)
    lbl_me = "Zona Media (Score 8-12): 14 eventos" if lang == 'ES' else "Medium Zone (Score 8-12): 14 events"
    draw.text((lx0 + 22, ly0 + 1), lbl_me, fill=(241, 245, 249), font=font_small)

    ly0 += 26
    draw.rounded_rectangle([(lx0, ly0), (lx0 + 14, ly0 + 14)], radius=3, fill=(209, 250, 229), outline=(16, 185, 129), width=1)
    lbl_lo = "Zona Baja (Score 1-6): 1 evento" if lang == 'ES' else "Low Zone (Score 1-6): 1 event"
    draw.text((lx0 + 22, ly0 + 1), lbl_lo, fill=(241, 245, 249), font=font_small)

    # Línea divisoria
    draw.line([(x0 + 16, gy0 + 172), (x0 + w - 16, gy0 + 172)], fill=(51, 65, 85), width=1)

    # 3. BARRAS PARETO DE MODOS DE FALLO (AIAG-VDA)
    y_pareto = gy0 + 184
    lbl_pareto = "2. TOP MODOS DE FALLO POR NPR (CRITICIDAD AIAG-VDA)" if lang == 'ES' else "2. TOP FAILURE MODES BY RPN (AIAG-VDA CRITICALITY)"
    draw.text((x0 + 16, y_pareto), lbl_pareto, fill=(56, 189, 248), font=font_bold)

    fmea_bars_data = [
        ("Acceso Indebido / Ciber", 441, (220, 38, 38), "NPR 441 · AP ALTA"),
        ("Corrupción BBDD Cloud", 360, (220, 38, 38), "NPR 360 · AP ALTA"),
        ("Fallo Pasarela Pagos", 336, (220, 38, 38), "NPR 336 · AP ALTA"),
        ("Bug CI/CD a Producción", 288, (245, 158, 11), "NPR 288 · AP ALTA"),
        ("Lag Colas de Mensajería", 294, (245, 158, 11), "NPR 294 · AP MEDIA"),
    ] if lang == 'ES' else [
        ("Unauthorized Access", 441, (220, 38, 38), "RPN 441 · HIGH AP"),
        ("Cloud Database Corrupt.", 360, (220, 38, 38), "RPN 360 · HIGH AP"),
        ("Payment Gateway Fail", 336, (220, 38, 38), "RPN 336 · HIGH AP"),
        ("CI/CD Prod Regression", 288, (245, 158, 11), "RPN 288 · HIGH AP"),
        ("Message Queue Backlog", 294, (245, 158, 11), "RPN 294 · MED AP"),
    ]

    bar_start_y = y_pareto + 22
    max_bar_w = 210

    for i, (f_name, f_npr, f_col, f_tag) in enumerate(fmea_bars_data):
        by = bar_start_y + i * 28
        draw.text((x0 + 16, by + 2), f_name, fill=(241, 245, 249), font=font_small)

        # Track
        bx0 = x0 + 160
        bx_end = bx0 + max_bar_w
        draw.rounded_rectangle([(bx0, by + 3), (bx_end, by + 16)], radius=3, fill=(30, 41, 59))

        # Fill
        fill_w = int((f_npr / 500.0) * max_bar_w)
        draw.rounded_rectangle([(bx0, by + 3), (bx0 + fill_w, by + 16)], radius=3, fill=f_col)

        # Tag
        draw.text((bx_end + 12, by + 2), f_tag, fill=f_col, font=font_bold)

    # Línea divisoria
    draw.line([(x0 + 16, bar_start_y + 146), (x0 + w - 16, bar_start_y + 146)], fill=(51, 65, 85), width=1)

    # 4. VEREDICTO DE MITIGACIÓN & RIESGO RESIDUAL
    y_win = bar_start_y + 154
    draw.rounded_rectangle([(x0 + 16, y_win), (x0 + w - 16, y_win + 50)], radius=8, fill=(16, 46, 36), outline=(16, 185, 129), width=2)

    win_title = "✓ RIESGO RESIDUAL REDUCIDO: -71,4% POST-MITIGACIÓN" if lang == 'ES' else "✓ RESIDUAL RISK REDUCED: -71.4% POST-MITIGATION"
    draw.text((x0 + 26, y_win + 8), win_title, fill=(209, 250, 229), font=font_bold)

    win_sub = "NPR Máximo mitigado a < 40 · 360.000 € CAPEX protegen 1.588.000 € de pérdida esperada" if lang == 'ES' else "Max RPN mitigated to < 40 · €360k CAPEX ringfences €1.588M in expected loss"
    draw.text((x0 + 26, y_win + 28), win_sub, fill=(110, 231, 183), font=font_small)


def generate_cover_image(lang='ES', out_path=None):
    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/matriz-riesgos-amfe-fmea/cover.png"
        else:
            out_path = "content/en/posts/quantitative-risk-matrix-fmea/cover.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado oscuro
    draw_linear_gradient(draw, WIDTH, HEIGHT, (15, 23, 42), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes
    font_kicker = get_font("segoeuib.ttf", 14)
    font_title = get_font("segoeuib.ttf", 36)
    font_sub = get_font("segoeui.ttf", 17)
    font_pill = get_font("segoeuib.ttf", 14)
    font_watermark = get_font("segoeuib.ttf", 12)
    font_bold = get_font("segoeuib.ttf", 12)
    font_small = get_font("segoeui.ttf", 11)
    font_mono = get_font("consola.ttf", 11)

    # 3. Textos Principales del Lado Izquierdo
    # Badge Kicker
    badge_text = "DATALARIA EXECUTIVE DECISION PACK • ISO 31000 / IATF 16949 STANDARD"
    draw.rounded_rectangle([(60, 48), (560, 78)], radius=6, fill=(13, 148, 136), outline=(13, 148, 136), width=1)
    draw.text((72, 54), badge_text, fill=(255, 255, 255), font=font_kicker)

    # Título Principal (2 Líneas)
    if lang == 'ES':
        title_line1 = "MATRIZ DE RIESGOS"
        title_line2 = "& AMFE / FMEA CUANTITATIVO"
        subtitle_line1 = "Cuantificación de Fallos, Matriz de Calor 5x5"
        subtitle_line2 = "& Cálculo del Número de Prioridad de Riesgo (NPR)"
    else:
        title_line1 = "QUANTITATIVE RISK MATRIX"
        title_line2 = "& OPERATIONAL FMEA"
        subtitle_line1 = "Failure Mode Quantification, 5x5 Heat Map"
        subtitle_line2 = "& Risk Priority Number (RPN) Calculation Engine"

    draw.text((60, 102), title_line1, fill=(255, 255, 255), font=font_title)
    draw.text((60, 150), title_line2, fill=(56, 189, 248), font=font_title)

    # Subtítulo
    draw.text((60, 214), subtitle_line1, fill=(203, 213, 225), font=font_sub)
    draw.text((60, 242), subtitle_line2, fill=(148, 163, 184), font=font_sub)

    # Píldoras de Entregables
    pills = [
        ("📊 Excel + Google Sheets", (37, 99, 235)),
        ("📑 Deck PPTX 16:9 C-Level", (13, 148, 136)),
        ("📄 Guía Metodológica PDF", (220, 38, 38))
    ] if lang == 'ES' else [
        ("📊 Excel + Google Sheets", (37, 99, 235)),
        ("📑 16:9 C-Level PPTX Deck", (13, 148, 136)),
        ("📄 Methodology Guide PDF", (220, 38, 38))
    ]

    py = 300
    for text, col in pills:
        draw.rounded_rectangle([(60, py), (370, py + 36)], radius=6, fill=(15, 23, 42), outline=col, width=2)
        draw.text((76, py + 8), text, fill=(241, 245, 249), font=font_pill)
        py += 48

    # Tarjeta de Garantía
    draw.rounded_rectangle([(60, 460), (540, 520)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    tag_es = "⚡ Descarga directa inmediata (.ZIP) | Protección ECMA-376 | 100% Personalizable"
    tag_en = "⚡ Instant direct download (.ZIP) | ECMA-376 Protection | 100% Customizable"
    draw.text((74, 478), tag_es if lang == 'ES' else tag_en, fill=(226, 232, 240), font=font_small)

    # Watermark
    draw.text((60, 565), "DATALARIA.COM · EXECUTIVE DECISION PACKS · CONTROL OPERATIVO", fill=(100, 116, 139), font=font_watermark)

    # 4. Panel Gráfico del Lado Derecho
    draw_fmea_graphic(draw, x0=580, y0=48, w=560, h=530, font_small=font_small, font_bold=font_bold, font_mono=font_mono, lang=lang)

    # Guardar
    img.save(out_path, "PNG", optimize=True)
    print(f"  -> Portada generada exitosamente: {out_path}")


def main():
    print("[1/2] Generando cover.png en Español...")
    generate_cover_image(lang='ES')

    print("[2/2] Generando cover.png en Inglés...")
    generate_cover_image(lang='EN')

    print("\n✓ Generación de portadas cover.png completada con éxito.")


if __name__ == "__main__":
    main()
