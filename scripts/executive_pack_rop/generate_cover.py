#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera las imágenes de portada cover.png de alta resolución (1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/calculadora-stock-seguridad-rop/cover.png
- content/en/posts/safety-stock-reorder-point-calculator/cover.png
Y actualiza la miniatura cuadrada del catálogo en:
- static/images/recursos/Stock.png

Composición visual de estándar APICS / ASCM / MIT CTL / McKinsey:
- Fondo: Degradado Dark Slate (#0F172A a #1E293B) con malla técnica sutil.
- Badge superior medido dinámicamente: "DATALARIA EXECUTIVE PACK • APICS / ASCM STANDARD".
- Título principal + subtítulo bilingüe.
- Píldoras de entregables con iconos vectoriales Pillow (cero glifos Unicode rotos).
- Caja de garantía encuadrada: "Descarga directa inmediata (.ZIP con versiones ES y EN)".
- Panel analítico derecho sin solapes: Gráfico cartesiano Diente de Sierra (Sawtooth) con banda de leyenda superior,
  umbrales ROP/SS en zona libre de trazado, 3 KPI Cards y barra de diagnóstico encuadrada.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

WIDTH = 1200
HEIGHT = 630


def get_font(name, size):
    """Carga fuente TrueType del sistema Windows o fallback predeterminado."""
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


def text_width(draw, txt, font):
    bbox = draw.textbbox((0, 0), txt, font=font)
    return bbox[2] - bbox[0]


def draw_linear_gradient(draw, width, height, start_color, end_color):
    """Pinta un degradado diagonal suave en el fondo."""
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
    """Dibuja una cuadrícula y cruces de alineación técnica sutiles."""
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48), width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_icon_excel(draw, x, y):
    """Icono vectorial de hoja de cálculo Excel."""
    draw.rounded_rectangle([(x, y), (x + 14, y + 14)], radius=2, fill=(16, 185, 129))
    draw.line([(x + 5, y + 2), (x + 5, y + 12)], fill=(15, 23, 42), width=1)
    draw.line([(x + 10, y + 2), (x + 10, y + 12)], fill=(15, 23, 42), width=1)
    draw.line([(x + 2, y + 5), (x + 12, y + 5)], fill=(15, 23, 42), width=1)
    draw.line([(x + 2, y + 9), (x + 12, y + 9)], fill=(15, 23, 42), width=1)


def draw_icon_pptx(draw, x, y):
    """Icono vectorial de presentación C-Level 16:9."""
    draw.rounded_rectangle([(x, y + 1), (x + 15, y + 11)], radius=2, fill=(245, 158, 11))
    draw.line([(x + 7, y + 11), (x + 7, y + 14)], fill=(251, 191, 36), width=2)
    draw.line([(x + 4, y + 14), (x + 11, y + 14)], fill=(251, 191, 36), width=1)
    draw.rectangle([(x + 3, y + 4), (x + 6, y + 8)], fill=(15, 23, 42))
    draw.rectangle([(x + 8, y + 5), (x + 12, y + 8)], fill=(15, 23, 42))


def draw_icon_pdf(draw, x, y):
    """Icono vectorial de documento guía PDF."""
    draw.polygon([(x + 1, y), (x + 9, y), (x + 13, y + 4), (x + 13, y + 14), (x + 1, y + 14)], fill=(239, 68, 68))
    draw.polygon([(x + 9, y), (x + 9, y + 4), (x + 13, y + 4)], fill=(252, 165, 165))
    draw.line([(x + 3, y + 7), (x + 10, y + 7)], fill=(255, 255, 255), width=1)
    draw.line([(x + 3, y + 10), (x + 10, y + 10)], fill=(255, 255, 255), width=1)


def draw_icon_bolt(draw, x, y):
    """Icono vectorial de rayo (descarga instantánea)."""
    pts = [
        (x + 7, y),
        (x + 2, y + 8),
        (x + 6, y + 8),
        (x + 4, y + 14),
        (x + 11, y + 6),
        (x + 7, y + 6),
    ]
    draw.polygon(pts, fill=(52, 211, 153))


def draw_sawtooth_panel(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang='ES'):
    """
    Dibuja el panel analítico ejecutivo del motor de inventario Diente de Sierra (Sawtooth)
    con separación dinámica entre cabeceras, banda superior de leyenda aislada y barra inferior legible.
    """
    is_es = (lang == 'ES')
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico (medida dinámicamente sin solape)
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR ESTOCÁSTICO SCM (APICS)" if is_es else "STOCHASTIC SCM ENGINE (APICS)"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(56, 189, 248), font=font_bold)

    sub_panel = "SS = Z·√(L·σd² + d²·σL²) | ROP = d·L + SS"
    sub_w = text_width(draw, sub_panel, font_small)
    draw.text((x0 + w - 16 - sub_w, y0 + 14), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. Área del Gráfico Cartesiano Diente de Sierra
    gx0 = x0 + 18
    gy0 = y0 + 48
    gw = w - 36
    gh = 248

    draw.rounded_rectangle([(gx0, gy0), (gx0 + gw, gy0 + gh)], radius=8, fill=(24, 33, 50), outline=(51, 65, 85), width=1)

    # Banda superior de leyenda aislada del área de trazado
    leg_y = gy0 + 10
    legend_items = (
        [
            ("Inventario Físico (EOQ)", (56, 189, 248)),
            ("Umbral ROP", (245, 158, 11)),
            ("Colchón SS", (16, 185, 129)),
        ]
        if is_es
        else [
            ("Physical Stock (EOQ)", (56, 189, 248)),
            ("ROP Threshold", (245, 158, 11)),
            ("SS Buffer", (16, 185, 129)),
        ]
    )
    lx = gx0 + 20
    for l_txt, l_col in legend_items:
        draw.ellipse([(lx, leg_y + 3), (lx + 7, leg_y + 10)], fill=l_col)
        draw.text((lx + 11, leg_y), l_txt, fill=l_col, font=font_small)
        lx += 11 + text_width(draw, l_txt, font_small) + 22

    # Ejes cartesianos estrictamente por debajo de la leyenda
    base_y = gy0 + gh - 30
    top_y = gy0 + 36
    ax_x0 = gx0 + 32
    ax_x1 = gx0 + gw - 18
    draw.line([(ax_x0, base_y), (ax_x1, base_y)], fill=(71, 85, 105), width=1)
    draw.line([(ax_x0, base_y), (ax_x0, top_y)], fill=(71, 85, 105), width=1)

    # Zona de Colchón de Seguridad (SS Buffer) en tono oscuro esmeralda + línea superior
    ss_y = base_y - 42
    draw.rectangle([(ax_x0 + 1, ss_y), (ax_x1, base_y - 1)], fill=(14, 58, 52), outline=None)
    draw.line([(ax_x0, ss_y), (ax_x1, ss_y)], fill=(16, 185, 129), width=2)

    # Línea horizontal discontinua de Punto de Pedido (ROP)
    rop_y = base_y - 102
    for dash_x in range(ax_x0, ax_x1 - 4, 10):
        draw.line([(dash_x, rop_y), (min(dash_x + 5, ax_x1), rop_y)], fill=(245, 158, 11), width=2)

    # Coordenadas del Diente de Sierra (2 ciclos terminando en x=ax_x0 + 340 para dejar libre la zona derecha)
    top_inv_y = top_y + 14
    cycle_w = 160
    x_c1_start = ax_x0 + 12
    x_c1_end = x_c1_start + cycle_w
    x_c2_end = x_c1_end + cycle_w

    # Interpolación exacta del punto donde el diente de sierra cruza ROP
    t_rop = (rop_y - top_inv_y) / (ss_y - top_inv_y)
    x_c1_rop = int(x_c1_start + t_rop * cycle_w)
    x_c2_rop = int(x_c1_end + t_rop * cycle_w)

    # Trazado azul brillante del ciclo de inventario
    draw.line([(x_c1_start, top_inv_y), (x_c1_end, ss_y)], fill=(56, 189, 248), width=3)
    draw.line([(x_c1_end, ss_y), (x_c1_end, top_inv_y)], fill=(56, 189, 248), width=3)
    draw.line([(x_c1_end, top_inv_y), (x_c2_end, ss_y)], fill=(56, 189, 248), width=3)
    draw.line([(x_c2_end, ss_y), (x_c2_end, top_inv_y)], fill=(56, 189, 248), width=3)

    # Puntos críticos (Disparos ROP y Llegada EOQ)
    draw.ellipse([(x_c1_rop - 5, rop_y - 5), (x_c1_rop + 5, rop_y + 5)], fill=(245, 158, 11), outline=(255, 255, 255), width=1)
    draw.ellipse([(x_c2_rop - 5, rop_y - 5), (x_c2_rop + 5, rop_y + 5)], fill=(245, 158, 11), outline=(255, 255, 255), width=1)
    draw.ellipse([(x_c1_end - 5, ss_y - 5), (x_c1_end + 5, ss_y + 5)], fill=(16, 185, 129), outline=(255, 255, 255), width=1)

    # Etiquetas en zona derecha despejada (sin cruces con líneas azules)
    rop_lbl = "ROP = d·L + SS"
    ss_lbl = "SS Colchón Basal" if is_es else "SS Safety Buffer"
    draw.text((x_c2_end + 12, rop_y - 16), rop_lbl, fill=(245, 158, 11), font=font_small)
    draw.text((x_c2_end + 12, ss_y - 16), ss_lbl, fill=(52, 211, 153), font=font_small)

    # Callout +EOQ Lote Wilson en zona superior despejada sobre el segundo salto
    eoq_lbl = "+EOQ Wilson"
    draw.text((x_c2_end + 12, top_inv_y + 4), eoq_lbl, fill=(56, 189, 248), font=font_small)

    # Callout Lead Time en el cuadrante superior libre sobre el tramo descendente entre ROP y Day 15
    lt_y = rop_y - 16
    draw.line([(x_c1_rop, lt_y), (x_c1_end - 3, lt_y)], fill=(148, 163, 184), width=1)
    draw.line([(x_c1_rop, lt_y - 4), (x_c1_rop, lt_y + 4)], fill=(148, 163, 184), width=1)
    draw.line([(x_c1_end - 3, lt_y - 4), (x_c1_end - 3, lt_y + 4)], fill=(148, 163, 184), width=1)
    lt_txt = "L"
    lt_w = text_width(draw, lt_txt, font_small)
    draw.text(((x_c1_rop + x_c1_end - 3 - lt_w) // 2, lt_y - 14), lt_txt, fill=(203, 213, 225), font=font_small)

    # Etiquetas eje horizontal
    draw.text((x_c1_start - 10, base_y + 7), "Día 0" if is_es else "Day 0", fill=(100, 116, 139), font=font_small)
    draw.text((x_c1_end - 14, base_y + 7), "Día 15" if is_es else "Day 15", fill=(100, 116, 139), font=font_small)
    draw.text((x_c2_end - 14, base_y + 7), "Día 30" if is_es else "Day 30", fill=(100, 116, 139), font=font_small)

    # 3. Tres Tarjetas KPI Inferiores
    ky = gy0 + gh + 12
    kw = (gw - 20) // 3
    kh = 72

    kpis_data = (
        [
            ("NIVEL DE SERVICIO", "98,0% (Z=2,05)", "Clase A Blindada", (16, 185, 129)),
            ("CAPITAL LIBERADO", "220.000 €", "Working Capital Neto", (56, 189, 248)),
            ("ROTURAS CLASE A", "< 2,0%", "-73% Riesgo Quiebre", (245, 158, 11))
        ]
        if is_es
        else [
            ("SERVICE LEVEL", "98.0% (Z=2.05)", "Protected Class A", (16, 185, 129)),
            ("CASH RELEASED", "$220,000", "Net Working Capital", (56, 189, 248)),
            ("CLASS A SHORTAGE", "< 2.0%", "-73% Stockout Risk", (245, 158, 11))
        ]
    )

    for idx, (kt, kv, ks, kc) in enumerate(kpis_data):
        kx = gx0 + idx * (kw + 10)
        draw.rounded_rectangle([(kx, ky), (kx + kw, ky + kh)], radius=6, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text((kx + 10, ky + 8), kt, fill=(148, 163, 184), font=font_small)
        draw.text((kx + 10, ky + 25), kv, fill=kc, font=font_bold)
        draw.text((kx + 10, ky + 50), ks, fill=(148, 163, 184), font=font_small)

    # 4. Barra de Diagnóstico Inferior (fondo oscuro sólido legible y texto 100% encuadrado)
    by = ky + kh + 10
    draw.rounded_rectangle([(gx0, by), (gx0 + gw, by + 34)], radius=6, fill=(24, 45, 40), outline=(16, 185, 129), width=1)
    status_text = (
        "DIAGNÓSTICO: Modelo Estocástico Validado · Grado Consejo C-Level"
        if is_es
        else "DIAGNOSTIC: Stochastic Engine Validated · Boardroom Decision-Grade"
    )
    draw.text((gx0 + 16, by + 9), status_text, fill=(110, 231, 183), font=font_bold)


def create_cover(output_path, lang='ES'):
    """Genera la imagen completa de portada (1200 x 630 px)."""
    is_es = (lang == 'ES')
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo con degradado y malla
    draw_linear_gradient(draw, WIDTH, HEIGHT, (15, 23, 42), (30, 41, 59))
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes del sistema
    f_badge = get_font("segoeuib.ttf", 11)
    f_title = get_font("segoeuib.ttf", 36)
    f_sub = get_font("segoeui.ttf", 16)
    f_pill = get_font("segoeuib.ttf", 12)
    f_bullet = get_font("segoeui.ttf", 13)
    f_guarantee = get_font("segoeui.ttf", 12)
    f_watermark = get_font("segoeuib.ttf", 10)

    f_p_small = get_font("segoeui.ttf", 10)
    f_p_bold = get_font("segoeuib.ttf", 12)
    f_p_mono = get_font("consola.ttf", 10)

    # 2. Panel Izquierdo: Textos y Propuesta de Valor
    lx = 55

    # Badge Superior medido dinámicamente
    badge_text = "DATALARIA EXECUTIVE PACK • APICS / ASCM STANDARD"
    badge_w = text_width(draw, badge_text, f_badge) + 28
    draw.rounded_rectangle([(lx, 50), (lx + badge_w, 78)], radius=6, fill=(30, 58, 138), outline=(37, 99, 235), width=1)
    draw.text((lx + 14, 57), badge_text, fill=(147, 197, 253), font=f_badge)

    # Título Principal
    if is_es:
        draw.text((lx, 100), "STOCK DE SEGURIDAD", fill=(255, 255, 255), font=f_title)
        draw.text((lx, 146), "& REORDER POINT (ROP)", fill=(56, 189, 248), font=f_title)
        sub_text1 = "Optimización de Inventario, Nivel de Servicio"
        sub_text2 = "& Working Capital para el Consejo de Administración"
    else:
        draw.text((lx, 100), "SAFETY STOCK &", fill=(255, 255, 255), font=f_title)
        draw.text((lx, 146), "REORDER POINT (ROP)", fill=(56, 189, 248), font=f_title)
        sub_text1 = "Inventory Optimization, Service Level &"
        sub_text2 = "C-Level Working Capital Management"

    # Subtítulo en 2 líneas
    draw.text((lx, 210), sub_text1, fill=(203, 213, 225), font=f_sub)
    draw.text((lx, 235), sub_text2, fill=(148, 163, 184), font=f_sub)

    # Píldoras de Entregables con iconos vectoriales Pillow (encuadre dinámico sin glifos rotos)
    pills = [
        ("excel", "Excel + Sheets", (30, 41, 59), (56, 189, 248)),
        ("pptx", "PPTX 16:9 C-Level", (30, 41, 59), (56, 189, 248)),
        ("pdf", "Guía PDF" if is_es else "PDF Guide", (30, 41, 59), (56, 189, 248)),
    ]
    cur_px = lx
    py = 285
    for icon_kind, p_txt, p_bg, p_fg in pills:
        tw = text_width(draw, p_txt, f_pill)
        pw = 12 + 15 + 8 + tw + 12
        draw.rounded_rectangle([(cur_px, py), (cur_px + pw, py + 32)], radius=6, fill=p_bg, outline=(71, 85, 105), width=1)
        if icon_kind == "excel":
            draw_icon_excel(draw, cur_px + 11, py + 9)
        elif icon_kind == "pptx":
            draw_icon_pptx(draw, cur_px + 11, py + 9)
        else:
            draw_icon_pdf(draw, cur_px + 11, py + 9)
        draw.text((cur_px + 34, py + 8), p_txt, fill=p_fg, font=f_pill)
        cur_px += pw + 12

    # Bullets de Valor Diferencial
    bullets = (
        [
            "• Convolución estocástica completa: SS = Z·√(L·σd² + d²·σL²)",
            "• Sincronización Diente de Sierra, Punto de Pedido (ROP) y EOQ",
            "• Control de ciclo de vida IEC 62402 (PCN, PDN, LTB, EOL)",
            "• Matriz estratégica ABC y liberación neta de Working Capital"
        ]
        if is_es
        else [
            "• Full stochastic convolution: SS = Z·√(L·σd² + d²·σL²)",
            "• Continuous Sawtooth cycle, Reorder Point (ROP) & Wilson EOQ",
            "• IEC 62402 component lifecycle alignment (PCN, PDN, LTB, EOL)",
            "• Strategic ABC stratification & releasable working capital"
        ]
    )

    by = 342
    for b in bullets:
        draw.text((lx, by), b, fill=(226, 232, 240), font=f_bullet)
        by += 24

    # Caja encuadrada de garantía con icono vectorial de rayo
    guar_txt = (
        "Descarga directa inmediata (.ZIP con versiones ES y EN)"
        if is_es
        else "Instant direct download (.ZIP with ES & EN editions)"
    )
    guar_w = max(470, 14 + 14 + 10 + text_width(draw, guar_txt, f_guarantee) + 16)
    draw.rounded_rectangle([(lx, 462), (lx + guar_w, 494)], radius=6, fill=(24, 45, 40), outline=(16, 185, 129), width=1)
    draw_icon_bolt(draw, lx + 14, 471)
    draw.text((lx + 34, 470), guar_txt, fill=(110, 231, 183), font=f_guarantee)

    # Footer Institucional
    draw.text(
        (lx, 548),
        "DATALARIA.COM • STANDARD APICS / ASCM & MIT CTL",
        fill=(100, 116, 139),
        font=f_watermark,
    )

    # 3. Panel Derecho: Panel Analítico Diente de Sierra
    rx = 585
    ry = 50
    rw = 565
    rh = 515
    draw_sawtooth_panel(draw, rx, ry, rw, rh, f_p_small, f_p_bold, f_p_mono, lang=lang)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", optimize=True)


def update_catalog_square_thumb(src_cover: Path, dst_square: Path):
    """Genera la miniatura cuadrada 1200x1200 para el catálogo /recursos/ y Lemon Squeezy."""
    canvas_w, canvas_h = 1200, 1200
    bg_color = (11, 17, 32)
    grid_line = (18, 27, 44)
    grid_cross = (35, 48, 68)
    border_col = (56, 189, 248)

    canvas = Image.new("RGB", (canvas_w, canvas_h), bg_color)
    d = ImageDraw.Draw(canvas)
    for x in range(0, canvas_w, 40):
        d.line([(x, 0), (x, canvas_h)], fill=grid_line, width=1)
    for y in range(0, canvas_h, 40):
        d.line([(0, y), (canvas_w, y)], fill=grid_line, width=1)
    for x in range(60, canvas_w, 120):
        for y in range(60, canvas_h, 120):
            d.line([(x - 3, y), (x + 3, y)], fill=grid_cross, width=1)
            d.line([(x, y - 3), (x, y + 3)], fill=grid_cross, width=1)

    im = Image.open(src_cover).convert("RGB")
    scale = 1080 / im.width
    new_w = int(im.width * scale)
    new_h = int(im.height * scale)
    im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

    paste_x = (canvas_w - new_w) // 2
    paste_y = 575 - (new_h // 2)
    canvas.paste(im_resized, (paste_x, paste_y))
    d.rectangle([(paste_x - 1, paste_y - 1), (paste_x + new_w, paste_y + new_h)], outline=border_col, width=1)

    dst_square.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst_square, "PNG", quality=95)
    print(f"      -> Square thumb updated: {dst_square}")


def main():
    """Genera las portadas en las carpetas de contenido y la miniatura cuadrada del catálogo."""
    path_es = "content/es/posts/calculadora-stock-seguridad-rop/cover.png"
    path_en = "content/en/posts/safety-stock-reorder-point-calculator/cover.png"

    print("[1/3] Generando portada en Español (content/es/posts/.../cover.png)...")
    create_cover(path_es, lang='ES')
    print(f"      -> Guardado: {path_es}")

    print("[2/3] Generating cover image in English (content/en/posts/.../cover.png)...")
    create_cover(path_en, lang='EN')
    print(f"      -> Saved: {path_en}")

    print("[3/3] Actualizando miniatura cuadrada en static/images/recursos/Stock.png...")
    update_catalog_square_thumb(Path(path_en), Path("static/images/recursos/Stock.png"))

    lemon_img = Path("packages/00_DISTRIBUCION_LEMONSQUEEZY/Images/Stock.png")
    lemon_sq = Path("packages/00_DISTRIBUCION_LEMONSQUEEZY/Images_Square/Stock.png")
    if lemon_img.parent.exists():
        Image.open(path_en).save(lemon_img, "PNG", optimize=True)
        update_catalog_square_thumb(Path(path_en), lemon_sq)

    print("Portadas de alta resolución cover.png generadas con total éxito.")


if __name__ == "__main__":
    main()
