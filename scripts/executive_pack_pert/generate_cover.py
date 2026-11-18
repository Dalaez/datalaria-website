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


def draw_icon_excel(draw, x, y):
    """Dibuja un icono vectorial de hoja de cálculo Excel."""
    draw.rounded_rectangle([(x, y), (x + 14, y + 14)], radius=2, fill=(16, 185, 129))
    draw.line([(x + 5, y + 2), (x + 5, y + 12)], fill=(15, 23, 42), width=1)
    draw.line([(x + 10, y + 2), (x + 10, y + 12)], fill=(15, 23, 42), width=1)
    draw.line([(x + 2, y + 5), (x + 12, y + 5)], fill=(15, 23, 42), width=1)
    draw.line([(x + 2, y + 9), (x + 12, y + 9)], fill=(15, 23, 42), width=1)


def draw_icon_pptx(draw, x, y):
    """Dibuja un icono vectorial de presentación C-Level 16:9."""
    draw.rounded_rectangle([(x, y + 1), (x + 15, y + 11)], radius=2, fill=(245, 158, 11))
    draw.line([(x + 7, y + 11), (x + 7, y + 14)], fill=(251, 191, 36), width=2)
    draw.line([(x + 4, y + 14), (x + 11, y + 14)], fill=(251, 191, 36), width=1)
    draw.rectangle([(x + 3, y + 4), (x + 6, y + 8)], fill=(15, 23, 42))
    draw.rectangle([(x + 8, y + 5), (x + 12, y + 8)], fill=(15, 23, 42))


def draw_icon_pdf(draw, x, y):
    """Dibuja un icono vectorial de documento guía PDF."""
    draw.polygon([(x + 1, y), (x + 9, y), (x + 13, y + 4), (x + 13, y + 14), (x + 1, y + 14)], fill=(239, 68, 68))
    draw.polygon([(x + 9, y), (x + 9, y + 4), (x + 13, y + 4)], fill=(252, 165, 165))
    draw.line([(x + 3, y + 7), (x + 10, y + 7)], fill=(255, 255, 255), width=1)
    draw.line([(x + 3, y + 10), (x + 10, y + 10)], fill=(255, 255, 255), width=1)


def draw_icon_bolt(draw, x, y):
    """Dibuja un icono vectorial de rayo (descarga instantánea)."""
    pts = [
        (x + 7, y),
        (x + 2, y + 8),
        (x + 6, y + 8),
        (x + 4, y + 14),
        (x + 11, y + 6),
        (x + 7, y + 6),
    ]
    draw.polygon(pts, fill=(52, 211, 153))


def text_width(draw, txt, font):
    bbox = draw.textbbox((0, 0), txt, font=font)
    return bbox[2] - bbox[0]


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
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(56, 189, 248), font=font_bold)
    sub_panel = "μ = (o+4m+p)/6 · σ_proj = √(Σσ²)"
    sub_w = text_width(draw, sub_panel, font_small)
    draw.text((x0 + w - 16 - sub_w, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

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
    draw.line([(cx_mu, base_y), (cx_mu, base_y - peak_h - 14)], fill=(148, 163, 184), width=1)
    mu_lbl = "μ=132.5d"
    mu_w = text_width(draw, mu_lbl, font_mono)
    draw.text((cx_mu - mu_w // 2, base_y + 8), mu_lbl, fill=(148, 163, 184), font=font_mono)

    # Línea vertical de la fecha límite (rojo) — etiqueta posicionada limpiamente a la izquierda
    dead_top = gy0 + 16
    draw.line([(cx_deadline, base_y), (cx_deadline, dead_top)], fill=(239, 68, 68), width=2)
    lbl_dead = "Target: 125d" if lang == 'EN' else "Límite: 125d"
    lbl_prob = "P=34.2% (Risk)" if lang == 'EN' else "P=34.2% (Riesgo)"
    dead_w = max(text_width(draw, lbl_dead, font_bold), text_width(draw, lbl_prob, font_mono))
    pill_x0 = cx_deadline - dead_w - 22
    draw.rounded_rectangle([(pill_x0, dead_top), (cx_deadline - 6, dead_top + 38)], radius=5, fill=(69, 18, 24), outline=(239, 68, 68), width=1)
    draw.text((pill_x0 + 8, dead_top + 5), lbl_dead, fill=(254, 202, 202), font=font_bold)
    draw.text((pill_x0 + 8, dead_top + 21), lbl_prob, fill=(252, 165, 165), font=font_mono)

    # Línea vertical P90 (verde) — etiqueta en zona abierta derecha
    p90_top = gy0 + 26
    draw.line([(cx_p90, base_y), (cx_p90, p90_top)], fill=(16, 185, 129), width=2)
    lbl_p90 = "Board P90: 148d"
    lbl_cert = "90% Certainty" if lang == 'EN' else "Certidumbre 90%"
    p90_w = max(text_width(draw, lbl_p90, font_bold), text_width(draw, lbl_cert, font_mono))
    draw.rounded_rectangle([(cx_p90 + 6, p90_top), (cx_p90 + 22 + p90_w, p90_top + 38)], radius=5, fill=(14, 48, 38), outline=(16, 185, 129), width=1)
    draw.text((cx_p90 + 14, p90_top + 5), lbl_p90, fill=(110, 231, 183), font=font_bold)
    draw.text((cx_p90 + 14, p90_top + 21), lbl_cert, fill=(167, 243, 208), font=font_mono)

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

    # 1. Kicker / Badge (ancho medido dinámicamente para evitar recortes)
    badge_txt = "DATALARIA EXECUTIVE PACK · PMBOK 7th / STOCHASTIC ENGINE"
    f_badge_fit = get_font("segoeuib.ttf", 11)
    badge_w = text_width(draw, badge_txt, f_badge_fit) + 28
    draw.rounded_rectangle([(left_x, 50), (left_x + badge_w, 78)], radius=6, fill=(30, 58, 138), outline=(37, 99, 235), width=1)
    draw.text((left_x + 14, 57), badge_txt, fill=(147, 197, 253), font=f_badge_fit)

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

    # 4. Píldoras de Entregables con iconos vectoriales (cero cajas unicode rotas)
    pills = [
        ("excel", "Excel + Sheets", (30, 41, 59), (56, 189, 248)),
        ("pptx", "PPTX 16:9 C-Level", (30, 41, 59), (56, 189, 248)),
        ("pdf", "Guía PDF" if lang == 'ES' else "PDF Guide", (30, 41, 59), (56, 189, 248)),
    ]
    px = left_x
    py = 285
    for icon_kind, p_txt, p_bg, p_fg in pills:
        tw = text_width(draw, p_txt, f_pill)
        pw = 12 + 15 + 8 + tw + 12
        draw.rounded_rectangle([(px, py), (px + pw, py + 32)], radius=6, fill=p_bg, outline=(71, 85, 105), width=1)
        if icon_kind == "excel":
            draw_icon_excel(draw, px + 11, py + 9)
        elif icon_kind == "pptx":
            draw_icon_pptx(draw, px + 11, py + 9)
        else:
            draw_icon_pdf(draw, px + 11, py + 9)
        draw.text((px + 34, py + 8), p_txt, fill=p_fg, font=f_pill)
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
    by = 342
    for b in b_list:
        draw.text((left_x, by), b, fill=(226, 232, 240), font=get_font("segoeui.ttf", 13))
        by += 24

    # 6. Garantía de Entrega con icono rayo vectorial
    guar_txt = "Descarga directa inmediata (.ZIP con versiones ES y EN)" if lang == 'ES' else "Instant direct download (.ZIP with ES & EN versions)"
    guar_w = max(470, 14 + 14 + 10 + text_width(draw, guar_txt, f_guarantee) + 16)
    draw.rounded_rectangle([(left_x, 462), (left_x + guar_w, 494)], radius=6, fill=(24, 45, 40), outline=(16, 185, 129), width=1)
    draw_icon_bolt(draw, left_x + 14, 471)
    draw.text((left_x + 34, 470), guar_txt, fill=(110, 231, 183), font=f_guarantee)

    # 7. Marca de Agua Inferior
    wm_txt = "DATALARIA.COM · EXECUTIVE DECISION PACKS · CONTROL OPERATIVO" if lang == 'ES' else "DATALARIA.COM · EXECUTIVE DECISION PACKS · OPERATIONS CONTROL"
    draw.text((left_x, 550), wm_txt, fill=(100, 116, 139), font=f_watermark)

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
