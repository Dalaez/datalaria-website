#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera las imágenes de portada cover.png de alta resolución (1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/estimacion-pert-3-puntos/cover.png
- content/en/posts/stochastic-3-point-pert-estimation/cover.png

Composición visual de estándar PMBOK / Operations Research / McKinsey:
- Fondo: Degradado Dark Slate (#0F172A a #1E293B) con malla técnica sutil.
- Badge superior: "DATALARIA EXECUTIVE DECISION PACK • PMBOK / STOCHASTIC MANAGEMENT"
- Título principal: "ESTIMACIÓN PERT DE 3 PUNTOS" / "3-POINT PERT ESTIMATION"
- Subtítulo: "Distribución Beta, Desviación Estándar & Probabilidad de Cumplimiento"
- Panel analítico derecho: Curva de Gauss (Bell Curve) con bandas de probabilidad, deadline crítico (34%) y buffer P90.
- Píldoras de entregables: [📊 Excel + Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF].
- Mensaje de garantía: "Descarga directa inmediata (.ZIP)".
- Marca de agua inferior: "DATALARIA.COM · EXECUTIVE DECISION PACKS · CONTROL OPERATIVO".
"""

import os
import sys
import math

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


def draw_pert_bell_graphic(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang='ES'):
    """
    Dibuja el panel analítico del motor PERT:
    - Cabecera: Ecuaciones canónicas Beta y CLT.
    - Curva de Gauss continua con sombreado de áreas de riesgo y certidumbre.
    - Líneas de corte: Fecha comprometida (34% éxito) vs Fecha P90 (90% certidumbre).
    - 3 KPI Cards inferiores con parámetros del proyecto.
    """
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR ESTOCÁSTICO PERT (BETA & CLT)" if lang == 'ES' else "STOCHASTIC PERT ENGINE (BETA & CLT)"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(2, 132, 199), font=font_bold)
    sub_panel = "μ = (o+4m+p)/6 · σ_proj = √(Σσ²)" if lang == 'ES' else "μ = (o+4m+p)/6 · σ_proj = √(Σσ²)"
    draw.text((x0 + w - 235, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. Área del Gráfico de Gauss
    gx0 = x0 + 20
    gy0 = y0 + 50
    gw = w - 40
    gh = 240

    # Fondo del gráfico
    draw.rounded_rectangle([(gx0, gy0), (gx0 + gw, gy0 + gh)], radius=8, fill=(24, 33, 50), outline=(51, 65, 85), width=1)

    # Eje horizontal base
    base_y = gy0 + gh - 35
    draw.line([(gx0 + 25, base_y), (gx0 + gw - 25, base_y)], fill=(71, 85, 105), width=1)

    # Puntos de la curva de Gauss
    # mu en x = 0.45 de gw
    # sigma = gw * 0.12
    cx_mu = gx0 + 25 + int((gw - 50) * 0.45)
    sigma_px = (gw - 50) * 0.12
    peak_h = gh - 75

    points = []
    x_steps = 150
    start_x = gx0 + 25
    end_x = gx0 + gw - 25

    for i in range(x_steps):
        curr_x = start_x + (end_x - start_x) * (i / (x_steps - 1))
        # gauss = exp(-0.5 * ((x - mu)/sigma)^2)
        dev = (curr_x - cx_mu) / sigma_px
        curr_y = base_y - peak_h * math.exp(-0.5 * dev * dev)
        points.append((curr_x, curr_y))

    # Sombrear área de riesgo (x <= fecha límite 125d, que está a mu - 0.6sigma)
    cx_deadline = cx_mu - int(sigma_px * 0.6)
    cx_p90 = cx_mu + int(sigma_px * 1.282)

    # Sombrear zona de riesgo (rojo suave)
    poly_risk = [(start_x, base_y)]
    for px, py in points:
        if px <= cx_deadline:
            poly_risk.append((px, py))
    poly_risk.append((cx_deadline, base_y))
    if len(poly_risk) > 2:
        draw.polygon(poly_risk, fill=(90, 24, 24))

    # Sombrear zona P90 (azul suave)
    poly_p90 = [(cx_deadline, base_y)]
    for px, py in points:
        if cx_deadline <= px <= cx_p90:
            poly_p90.append((px, py))
    poly_p90.append((cx_p90, base_y))
    if len(poly_p90) > 2:
        draw.polygon(poly_p90, fill=(20, 60, 110))

    # Trazar línea de la curva de campana
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(56, 189, 248), width=3)

    # Línea vertical de la media μ
    draw.line([(cx_mu, base_y), (cx_mu, base_y - peak_h - 10)], fill=(148, 163, 184), width=1)
    draw.text((cx_mu - 18, base_y + 8), "μ=132.5d", fill=(148, 163, 184), font=font_mono)

    # Línea vertical de la fecha límite (rojo)
    draw.line([(cx_deadline, base_y), (cx_deadline, base_y - peak_h * 0.8)], fill=(239, 68, 68), width=2)
    lbl_dead = "Target: 125d" if lang == 'EN' else "Límite: 125d"
    draw.text((cx_deadline - 58, base_y - peak_h * 0.85), lbl_dead, fill=(239, 68, 68), font=font_bold)
    lbl_prob = "P=34.2%"
    draw.text((cx_deadline - 50, base_y - peak_h * 0.72), lbl_prob, fill=(252, 165, 165), font=font_mono)

    # Línea vertical P90 (verde)
    draw.line([(cx_p90, base_y), (cx_p90, base_y - peak_h * 0.9)], fill=(16, 185, 129), width=2)
    lbl_p90 = "Board P90: 148d"
    draw.text((cx_p90 + 6, base_y - peak_h * 0.92), lbl_p90, fill=(16, 185, 129), font=font_bold)
    draw.text((cx_p90 + 6, base_y - peak_h * 0.78), "Certidumbre 90%", fill=(167, 243, 208), font=font_mono)

    # 3. Mini KPI Cards inferiores (Filas y0 + 305 a y0 + 415)
    ky0 = y0 + 302
    kw = (w - 56) // 3
    kh = 70

    # Card 1: Media μ
    draw.rounded_rectangle([(x0 + 16, ky0), (x0 + 16 + kw, ky0 + kh)], radius=6, fill=(24, 33, 50), outline=(51, 65, 85), width=1)
    draw.text((x0 + 26, ky0 + 8), "DURACIÓN ESPERADA" if lang == 'ES' else "EXPECTED DURATION", fill=(148, 163, 184), font=font_small)
    draw.text((x0 + 26, ky0 + 26), "132.5 Días" if lang == 'ES' else "132.5 Days", fill=(56, 189, 248), font=font_bold)
    draw.text((x0 + 26, ky0 + 48), "Media CLT ponderada" if lang == 'ES' else "Weighted CLT Mean", fill=(100, 116, 139), font=font_small)

    # Card 2: Desviación σ
    draw.rounded_rectangle([(x0 + 28 + kw, ky0), (x0 + 28 + 2 * kw, ky0 + kh)], radius=6, fill=(24, 33, 50), outline=(51, 65, 85), width=1)
    draw.text((x0 + 38 + kw, ky0 + 8), "DESVIACIÓN GLOBAL" if lang == 'ES' else "GLOBAL STD DEV", fill=(148, 163, 184), font=font_small)
    draw.text((x0 + 38 + kw, ky0 + 26), "± 11.8 Días" if lang == 'ES' else "± 11.8 Days", fill=(255, 255, 255), font=font_bold)
    draw.text((x0 + 38 + kw, ky0 + 48), "Rango ±2σ = 47.2d" if lang == 'ES' else "±2σ Range = 47.2d", fill=(100, 116, 139), font=font_small)

    # Card 3: Buffer P90
    draw.rounded_rectangle([(x0 + 40 + 2 * kw, ky0), (x0 + 40 + 3 * kw, ky0 + kh)], radius=6, fill=(24, 45, 40), outline=(16, 185, 129), width=1)
    draw.text((x0 + 50 + 2 * kw, ky0 + 8), "COLCHÓN P90 CONSEJO" if lang == 'ES' else "BOARD P90 BUFFER", fill=(167, 243, 208), font=font_small)
    draw.text((x0 + 50 + 2 * kw, ky0 + 26), "+15.1 Días" if lang == 'ES' else "+15.1 Days", fill=(52, 211, 153), font=font_bold)
    draw.text((x0 + 50 + 2 * kw, ky0 + 48), "Gobernanza blindada" if lang == 'ES' else "Board governed", fill=(110, 231, 183), font=font_small)

    # 4. Barra de Diagnóstico de Riesgo Inferior
    by0 = ky0 + kh + 10
    draw.rounded_rectangle([(x0 + 16, by0), (x0 + w - 16, by0 + 36)], radius=6, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    diag_txt = "VEREDICTO: Fecha 125d tiene 65.8% de probabilidad de fracaso -> Buffer formal de 16d garantiza 90% certidumbre." if lang == 'ES' else "VERDICT: 125d commitment has 65.8% failure risk -> Formal 16d buffer secures 90% certainty."
    draw.text((x0 + 26, by0 + 10), diag_txt, fill=(251, 191, 36), font=font_small)


def generate_cover_image(lang='ES', out_path=None):
    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/estimacion-pert-3-puntos/cover.png"
        else:
            out_path = "content/en/posts/stochastic-3-point-pert-estimation/cover.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado Slate
    draw_linear_gradient(draw, WIDTH, HEIGHT, (15, 23, 42), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes
    f_badge = get_font("segoeuib.ttf", 13)
    f_title = get_font("segoeuib.ttf", 36)
    f_sub = get_font("segoeui.ttf", 16)
    f_pill = get_font("segoeuib.ttf", 12)
    f_guarantee = get_font("segoeui.ttf", 12)
    f_watermark = get_font("segoeuib.ttf", 11)

    f_p_small = get_font("segoeui.ttf", 10)
    f_p_bold = get_font("segoeuib.ttf", 11)
    f_p_mono = get_font("consola.ttf", 10)

    # LADO IZQUIERDO: TEXTOS CORPORATIVOS
    left_x = 55

    # 1. Kicker / Badge
    badge_txt = "DATALARIA EXECUTIVE DECISION PACK · PMBOK 7th / STOCHASTIC MANAGEMENT"
    draw.rounded_rectangle([(left_x, 48), (left_x + 520, 78)], radius=6, fill=(30, 58, 138), outline=(37, 99, 235), width=1)
    draw.text((left_x + 14, 55), badge_txt, fill=(147, 197, 253), font=f_badge)

    # 2. Título Principal
    t1 = "ESTIMACIÓN PERT" if lang == 'ES' else "3-POINT PERT"
    t2 = "DE 3 PUNTOS" if lang == 'ES' else "ESTIMATION"
    draw.text((left_x, 100), t1, fill=(255, 255, 255), font=f_title)
    draw.text((left_x, 146), t2, fill=(56, 189, 248), font=f_title)

    # 3. Subtítulo
    sub1 = "Distribución Beta, Desviación Estándar &" if lang == 'ES' else "Beta Distribution, Standard Deviation &"
    sub2 = "Probabilidad de Cumplimiento de Cronograma" if lang == 'ES' else "Schedule Risk Probability Modeling"
    draw.text((left_x, 210), sub1, fill=(203, 213, 225), font=f_sub)
    draw.text((left_x, 235), sub2, fill=(203, 213, 225), font=f_sub)

    # 4. Píldoras de Entregables
    pills = [
        ("📊 Excel + Sheets", (30, 41, 59), (56, 189, 248)),
        ("📑 PPTX 16:9 C-Level", (30, 41, 59), (56, 189, 248)),
        ("📄 Guía PDF", (30, 41, 59), (56, 189, 248))
    ]
    px = left_x
    py = 285
    for p_txt, p_bg, p_fg in pills:
        pw = len(p_txt) * 9 + 20
        draw.rounded_rectangle([(px, py), (px + pw, py + 30)], radius=6, fill=p_bg, outline=(71, 85, 105), width=1)
        draw.text((px + 10, py + 7), p_txt, fill=p_fg, font=f_pill)
        px += pw + 12

    # 5. Viñetas de valor
    bullets_es = [
        "• Cálculo estocástico de μ, σ y σ² en camino crítico",
        "• Curva de campana y cálculo Z-Score para fecha límite",
        "• Dimensionamiento científico de Project Buffers (TOC)",
        "• Matriz de Crashing con coste marginal por día reducido"
    ]
    bullets_en = [
        "• Stochastic calculation of μ, σ, and σ² on critical path",
        "• Bell curve & Z-Score modeling for target deadlines",
        "• Scientific Project Buffer sizing (TOC / PMBOK)",
        "• Crashing matrix with marginal cost per day reduced"
    ]
    b_list = bullets_es if lang == 'ES' else bullets_en
    by = 340
    for b in b_list:
        draw.text((left_x, by), b, fill=(226, 232, 240), font=get_font("segoeui.ttf", 13))
        by += 24

    # 6. Garantía de Entrega
    guar_txt = "⚡ Descarga directa inmediata (.ZIP con versiones ES y EN)" if lang == 'ES' else "⚡ Instant direct download (.ZIP with ES & EN versions)"
    draw.rounded_rectangle([(left_x, 460), (left_x + 480, 492)], radius=6, fill=(24, 45, 40), outline=(16, 185, 129), width=1)
    draw.text((left_x + 14, 467), guar_txt, fill=(110, 231, 183), font=f_guarantee)

    # 7. Marca de Agua Inferior
    wm_txt = "DATALARIA.COM · EXECUTIVE DECISION PACKS · CONTROL OPERATIVO"
    draw.text((left_x, 560), wm_txt, fill=(100, 116, 139), font=f_watermark)

    # LADO DERECHO: PANEL ANALÍTICO ESTOCÁSTICO
    panel_x = 590
    panel_y = 50
    panel_w = 560
    panel_h = 515
    draw_pert_bell_graphic(draw, panel_x, panel_y, panel_w, panel_h, f_p_small, f_p_bold, f_p_mono, lang)

    # Guardar imagen
    img.save(out_path, format="PNG", optimize=True)
    print(f" -> Portada guardada exitosamente: {out_path}")
    return out_path


def main():
    print("[1/2] Generando portada cover.png en Español...")
    generate_cover_image(lang='ES')

    print("[2/2] Generando portada cover.png en Inglés...")
    generate_cover_image(lang='EN')

    print("Portadas de alta resolución generadas con éxito.")


if __name__ == "__main__":
    main()
