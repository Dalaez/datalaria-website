#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera las imágenes de portada cover.png de alta resolución (1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/matriz-raci-balance-carga/cover.png
- content/en/posts/quantitative-raci-workload-matrix/cover.png

Composición visual de estándar McKinsey / BCG / PMBOK 7ª Ed. / PRINCE2:
- Fondo: Degradado Dark Navy (#0F172A a #1E293B) con trama técnica sutil.
- Badge superior: "DATALARIA EXECUTIVE DECISION PACK • PMBOK / PRINCE2 STANDARD"
- Título principal: "MATRIZ RACI & BALANCE DE CARGA" / "QUANTITATIVE RACI MATRIX & WORKLOAD"
- Subtítulo: "Gobernanza de Roles, Asignación de Responsabilidades & Detección de Cuellos de Botella"
- Gráfico abstracto lateral: Cuadrícula cartesiana de responsabilidades RACI conectada a barras de saturación.
- Píldoras de entregables: [📊 Excel + Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF].
- Marca de agua inferior: "DATALARIA.COM · EXECUTIVE DECISION PACKS".
"""

import os
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


def draw_raci_graphic(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang='ES'):
    """
    Dibuja el panel analítico del motor RACI:
    - Cabecera: Ecuación de gobernanza (A=1 · R>=1).
    - Cuadrantes RACI (Responsible, Accountable, Consulted, Informed).
    - Barras de balance de saturación por rol.
    - Veredicto de auditoría conforme.
    """
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR DE GOBERNANZA RACI" if lang == 'ES' else "RACI GOVERNANCE ENGINE"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(13, 148, 136), font=font_bold)
    sub_panel = "A=1 · R≥1 · Wk = ∑(w · X)"
    draw.text((x0 + w - 185, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. CUADRANTES RACI (4 Cajas estilizadas)
    y_quad = y0 + 50
    lbl_quad = "1. MATRIZ DE ASIGNACIÓN CUANTITATIVA" if lang == 'ES' else "1. QUANTITATIVE ALLOCATION MATRIX"
    draw.text((x0 + 16, y_quad), lbl_quad, fill=(56, 189, 248), font=font_bold)

    quads = [
        ("A", "ACCOUNTABLE", "Sign-Off Único (12h)", (124, 58, 237), (35, 20, 60)), # Purple
        ("R", "RESPONSIBLE", "Ejecución Activa (26h)", (37, 99, 235), (20, 35, 65)), # Blue
        ("C", "CONSULTED", "Asesoría Técnica (5h)", (217, 119, 6), (50, 35, 15)),  # Amber
        ("I", "INFORMED", "Alineación Pasiva (1.5h)", (100, 116, 139), (25, 33, 45)) # Slate
    ] if lang == 'ES' else [
        ("A", "ACCOUNTABLE", "Single Sign-Off (12h)", (124, 58, 237), (35, 20, 60)),
        ("R", "RESPONSIBLE", "Hands-On Build (26h)", (37, 99, 235), (20, 35, 65)),
        ("C", "CONSULTED", "Tech Advisory (5h)", (217, 119, 6), (50, 35, 15)),
        ("I", "INFORMED", "Passive Tracking (1.5h)", (100, 116, 139), (25, 33, 45))
    ]

    qw = (w - 48) // 4
    qh = 50
    for idx, (letter, role_name, sub_info, border_col, bg_col) in enumerate(quads):
        qx = x0 + 16 + idx * (qw + 5)
        qy = y_quad + 20
        draw.rounded_rectangle([(qx, qy), (qx + qw, qy + qh)], radius=6, fill=bg_col, outline=border_col, width=2)
        draw.text((qx + 8, qy + 6), letter, fill=border_col, font=font_bold)
        draw.text((qx + 24, qy + 8), role_name[:9], fill=(241, 245, 249), font=font_small)
        draw.text((qx + 8, qy + 28), sub_info[:16], fill=(148, 163, 184), font=font_small)

    # Línea divisoria
    draw.line([(x0 + 16, y_quad + 80), (x0 + w - 16, y_quad + 80)], fill=(51, 65, 85), width=1)

    # 3. BALANCE DE SATURACIÓN POR ROL (BARRAS DE CAPACIDAD)
    y_bars = y_quad + 90
    lbl_bars = "2. BALANCE DE CARGA & SATURACIÓN POR ROL" if lang == 'ES' else "2. ROLE WORKLOAD & SATURATION HEATMAP"
    draw.text((x0 + 16, y_bars), lbl_bars, fill=(56, 189, 248), font=font_bold)

    roles_data = [
        ("Tech Lead / Arq.", 142.5, (225, 29, 72), "142% CUELLO BOTELLA"),
        ("PMO Lead", 88.8, (245, 158, 11), "89% ALERTA"),
        ("Equipo Desarrollo", 87.8, (245, 158, 11), "88% EQUILIBRADO"),
        ("QA & Testing", 86.9, (245, 158, 11), "87% EQUILIBRADO"),
        ("DevOps / Cloud", 69.4, (16, 185, 129), "69% DISPONIBLE"),
    ] if lang == 'ES' else [
        ("Tech Lead / Arch.", 142.5, (225, 29, 72), "142% BOTTLENECK"),
        ("PMO Lead", 88.8, (245, 158, 11), "89% WARNING"),
        ("Engineering Team", 87.8, (245, 158, 11), "88% BALANCED"),
        ("QA & Testing", 86.9, (245, 158, 11), "87% BALANCED"),
        ("DevOps / Cloud", 69.4, (16, 185, 129), "69% HEALTHY"),
    ]

    bar_start_y = y_bars + 22
    max_bar_w = 230

    for i, (r_name, r_sat, r_col, r_tag) in enumerate(roles_data):
        by = bar_start_y + i * 32
        draw.text((x0 + 16, by + 2), r_name, fill=(241, 245, 249), font=font_small)

        # Track
        bx0 = x0 + 140
        bx_end = bx0 + max_bar_w
        draw.rounded_rectangle([(bx0, by + 3), (bx_end, by + 18)], radius=4, fill=(30, 41, 59))

        # Filled portion
        fill_w = int(min(1.0, r_sat / 150.0) * max_bar_w)
        draw.rounded_rectangle([(bx0, by + 3), (bx0 + fill_w, by + 18)], radius=4, fill=r_col)

        # Tag
        draw.text((bx_end + 12, by + 2), r_tag, fill=r_col, font=font_bold)

    # Línea divisoria
    draw.line([(x0 + 16, bar_start_y + 168), (x0 + w - 16, bar_start_y + 168)], fill=(51, 65, 85), width=1)

    # 4. VEREDICTO DE GOBERNANZA REBALANCEADA
    y_win = bar_start_y + 178
    draw.rounded_rectangle([(x0 + 16, y_win), (x0 + w - 16, y_win + 52)], radius=8, fill=(16, 46, 36), outline=(16, 185, 129), width=2)

    win_title = "✓ GOBERNANZA REBALANCEADA: 100% AUDITABLE" if lang == 'ES' else "✓ REBALANCED GOVERNANCE: 100% AUDITABLE"
    draw.text((x0 + 26, y_win + 9), win_title, fill=(209, 250, 229), font=font_bold)

    win_sub = "Unicidad de Accountable blindada · Cuello de botella mitigado (-68h)" if lang == 'ES' else "Single Accountable enforced · Tech bottleneck resolved (-68h)"
    draw.text((x0 + 26, y_win + 29), win_sub, fill=(110, 231, 183), font=font_small)


def generate_cover_image(lang='ES', out_path=None):
    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/matriz-raci-balance-carga/cover.png"
        else:
            out_path = "content/en/posts/quantitative-raci-workload-matrix/cover.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado oscuro
    draw_linear_gradient(draw, WIDTH, HEIGHT, (15, 23, 42), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes
    font_kicker = get_font("segoeuib.ttf", 15)
    font_title = get_font("segoeuib.ttf", 36)
    font_sub = get_font("segoeui.ttf", 17)
    font_pill = get_font("segoeuib.ttf", 14)
    font_watermark = get_font("segoeuib.ttf", 12)
    font_bold = get_font("segoeuib.ttf", 12)
    font_small = get_font("segoeui.ttf", 11)
    font_mono = get_font("consola.ttf", 11)

    # 3. Textos Principales del Lado Izquierdo
    # Badge Kicker
    badge_text = "DATALARIA EXECUTIVE DECISION PACK • PMBOK / PRINCE2 STANDARD"
    draw.rounded_rectangle([(60, 48), (560, 78)], radius=6, fill=(13, 148, 136), outline=(13, 148, 136), width=1)
    draw.text((72, 54), badge_text, fill=(255, 255, 255), font=font_kicker)

    # Título Principal (2 Líneas)
    if lang == 'ES':
        title_line1 = "MATRIZ RACI CUANTITATIVA"
        title_line2 = "& BALANCE DE CARGA"
        subtitle_line1 = "Gobernanza de Roles, Unicidad de Accountable"
        subtitle_line2 = "& Detección de Cuellos de Botella Organizativos"
    else:
        title_line1 = "QUANTITATIVE RACI MATRIX"
        title_line2 = "& WORKLOAD BALANCING"
        subtitle_line1 = "Role Governance, Single Accountability Enforcement"
        subtitle_line2 = "& Operational Bottleneck Mitigation"

    draw.text((60, 102), title_line1, fill=(255, 255, 255), font=font_title)
    draw.text((60, 150), title_line2, fill=(56, 189, 248), font=font_title)

    # Subtítulo
    draw.text((60, 214), subtitle_line1, fill=(203, 213, 225), font=font_sub)
    draw.text((60, 242), subtitle_line2, fill=(148, 163, 184), font=font_sub)

    # Píldoras de Entregables
    pills = [
        ("📊 Excel + Google Sheets", (37, 99, 235)),
        ("📑 Deck PPTX 16:9 C-Level", (13, 148, 136)),
        ("📄 Guía Metodológica PDF", (124, 58, 237))
    ] if lang == 'ES' else [
        ("📊 Excel + Google Sheets", (37, 99, 235)),
        ("📑 16:9 C-Level PPTX Deck", (13, 148, 136)),
        ("📄 Methodology Guide PDF", (124, 58, 237))
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
    draw_raci_graphic(draw, x0=580, y0=48, w=560, h=530, font_small=font_small, font_bold=font_bold, font_mono=font_mono, lang=lang)

    # Guardar
    img.save(out_path, "PNG", optimize=True)
    print(f"  -> Portada generada exitosamente: {out_path}")


def main():
    print("[1/2] Generando cover.png en Español...")
    generate_cover_image(lang='ES')

    print("[2/2] Generando cover.png en Inglés...")
    generate_cover_image(lang='EN')


if __name__ == "__main__":
    main()
