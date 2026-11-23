#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera las imágenes de portada cover.png de alta resolución (1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/cuadro-mando-evm-valor-ganado/cover.png
- content/en/posts/earned-value-management-evm-dashboard/cover.png

Composición visual de estándar ANSI/EIA-748 / PMBOK / McKinsey:
- Fondo: Degradado Dark Slate (#0F172A a #1E293B) con malla técnica sutil.
- Badge superior: "DATALARIA EXECUTIVE PACK · ANSI/EIA-748 / PMBOK"
- Título principal: "CUADRO DE MANDO EVM" / "EARNED VALUE MANAGEMENT"
- Subtítulo: "Valor Ganado, Curva S & Proyecciones EAC"
- Píldoras de entregables con iconos vectoriales Pillow (cero glifos Unicode rotos): Excel + Sheets, PPTX 16:9 C-Level, Guía PDF.
- Panel analítico derecho (encuadrado sin solapes): Gráfico cartesiano de Curva S (PV azul, EV verde, AC rojo, EAC púrpura) con corte M06 y 3 KPI Cards.
- Caja de garantía encuadrada: "Descarga directa inmediata (.ZIP con versiones ES y EN)".
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


def text_width(draw, txt, font):
    bbox = draw.textbbox((0, 0), txt, font=font)
    return bbox[2] - bbox[0]


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
    """Dibuja una malla técnica con cuadrículas y cruces sutiles."""
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


def draw_evm_scurve_panel(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang='ES'):
    """
    Dibuja el panel analítico ejecutivo del motor EVM:
    - Cabecera: Ecuaciones canónicas ANSI/EIA-748 (CPI, SPI, EAC).
    - Banda superior dedicada de leyenda (sin colisión con línea de corte M06).
    - Gráfico Curva S sigmoide: PV (azul), EV (verde), AC (rojo) y Proyección EAC (púrpura).
    - 3 KPI Cards inferiores (CPI, SPI, EAC).
    - Barra de diagnóstico inferior perfectamente encuadrada.
    """
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR ANALÍTICO EVM (ANSI/EIA-748)" if lang == 'ES' else "EVM ANALYTICAL ENGINE (ANSI/EIA-748)"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(56, 189, 248), font=font_bold)
    sub_panel = "CPI = EV/AC · SPI = EV/PV · EAC = BAC/CPI"
    sub_w = text_width(draw, sub_panel, font_small)
    draw.text((x0 + w - 16 - sub_w, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. Área del Gráfico de la Curva S
    gx0 = x0 + 18
    gy0 = y0 + 48
    gw = w - 36
    gh = 246

    draw.rounded_rectangle([(gx0, gy0), (gx0 + gw, gy0 + gh)], radius=8, fill=(24, 33, 50), outline=(51, 65, 85), width=1)

    # Banda superior de leyenda aislada del área de trazado
    leg_y = gy0 + 10
    legend_items = (
        [
            ("PV: Plan", (37, 99, 235)),
            ("EV: Valor Ganado", (16, 185, 129)),
            ("AC: Coste Real", (220, 38, 38)),
            ("EAC: Proyección", (168, 85, 247)),
        ]
        if lang == 'ES'
        else [
            ("PV: Planned", (37, 99, 235)),
            ("EV: Earned", (16, 185, 129)),
            ("AC: Actual Cost", (220, 38, 38)),
            ("EAC: Forecast", (168, 85, 247)),
        ]
    )
    lx = gx0 + 22
    for l_txt, l_col in legend_items:
        draw.ellipse([(lx, leg_y + 3), (lx + 7, leg_y + 10)], fill=l_col)
        draw.text((lx + 11, leg_y), l_txt, fill=l_col, font=font_small)
        lx += 11 + text_width(draw, l_txt, font_small) + 18

    # Eje horizontal y vertical (por debajo de la leyenda)
    base_y = gy0 + gh - 34
    top_y = gy0 + 36
    axis_x0 = gx0 + 36
    axis_x1 = gx0 + gw - 24
    draw.line([(axis_x0, base_y), (axis_x1, base_y)], fill=(71, 85, 105), width=1)
    draw.line([(axis_x0, base_y), (axis_x0, top_y)], fill=(71, 85, 105), width=1)

    plot_w = axis_x1 - axis_x0
    step_x = plot_w / 11.0

    # Curvas S realistas (valores del caso 1.2M€ normalizados a 1.45M€ max)
    # PV acumulado M01..M12 (60k, 140k, 240k, 350k, 470k, 600k, 730k, 850k, 960k, 1060k, 1140k, 1200k)
    pv_vals = [0.050, 0.117, 0.200, 0.292, 0.392, 0.500, 0.608, 0.708, 0.800, 0.883, 0.950, 1.000]
    # EV acumulado M01..M06 (58k, 133k, 225k, 320k, 418k, 516k)
    ev_vals = [0.048, 0.111, 0.188, 0.267, 0.348, 0.430]
    # AC acumulado M01..M06 (62k, 146k, 254k, 368k, 484k, 600k)
    ac_vals = [0.052, 0.122, 0.212, 0.307, 0.403, 0.500]
    # EAC proyección M06..M12 (desde AC=600k hasta EAC=1.395M = 1.163)
    eac_vals = [0.500, 0.610, 0.721, 0.831, 0.942, 1.052, 1.163]

    def to_coords(m_idx, val):
        px = axis_x0 + m_idx * step_x
        ratio = val / 1.22
        py = base_y - ratio * (base_y - top_y)
        return (px, py)

    pv_pts = [to_coords(i, v) for i, v in enumerate(pv_vals)]
    ev_pts = [to_coords(i, v) for i, v in enumerate(ev_vals)]
    ac_pts = [to_coords(i, v) for i, v in enumerate(ac_vals)]
    eac_pts = [to_coords(5 + i, v) for i, v in enumerate(eac_vals)]

    # Líneas horizontales de cuadrícula
    for tick in [0.25, 0.50, 0.75, 1.00]:
        _, ty = to_coords(0, tick)
        draw.line([(axis_x0, ty), (axis_x1, ty)], fill=(35, 48, 70), width=1)

    # 1. Trazar PV (Azul)
    for i in range(len(pv_pts) - 1):
        draw.line([pv_pts[i], pv_pts[i + 1]], fill=(37, 99, 235), width=2)
    for pt in pv_pts:
        draw.ellipse([(pt[0] - 2.5, pt[1] - 2.5), (pt[0] + 2.5, pt[1] + 2.5)], fill=(37, 99, 235))

    # 2. Trazar EAC Proyección (Púrpura)
    for i in range(len(eac_pts) - 1):
        draw.line([eac_pts[i], eac_pts[i + 1]], fill=(168, 85, 247), width=2)
    for pt in eac_pts:
        draw.ellipse([(pt[0] - 2.5, pt[1] - 2.5), (pt[0] + 2.5, pt[1] + 2.5)], fill=(168, 85, 247))

    # 3. Trazar AC (Rojo)
    for i in range(len(ac_pts) - 1):
        draw.line([ac_pts[i], ac_pts[i + 1]], fill=(220, 38, 38), width=3)
    for pt in ac_pts:
        draw.ellipse([(pt[0] - 3, pt[1] - 3), (pt[0] + 3, pt[1] + 3)], fill=(220, 38, 38))

    # 4. Trazar EV (Verde)
    for i in range(len(ev_pts) - 1):
        draw.line([ev_pts[i], ev_pts[i + 1]], fill=(16, 185, 129), width=3)
    for pt in ev_pts:
        draw.ellipse([(pt[0] - 3, pt[1] - 3), (pt[0] + 3, pt[1] + 3)], fill=(16, 185, 129))

    # Línea vertical de corte en Mes 6 (estrictamente acotada debajo de la leyenda)
    cut_x, _ = to_coords(5, 0)
    draw.line([(cut_x, base_y), (cut_x, top_y + 4)], fill=(148, 163, 184), width=1)
    lbl_cut = "Corte M06" if lang == 'ES' else "Cutoff M06"
    cut_w = text_width(draw, lbl_cut, font_mono)
    draw.text((cut_x - cut_w // 2, base_y + 8), lbl_cut, fill=(148, 163, 184), font=font_mono)

    # Etiquetas de inicio/fin en eje X
    draw.text((axis_x0 - 8, base_y + 8), "M01", fill=(100, 116, 139), font=font_mono)
    draw.text((axis_x1 - 18, base_y + 8), "M12", fill=(100, 116, 139), font=font_mono)

    # Indicador de brecha CV en mes 6
    ac_pt6 = ac_pts[-1]
    ev_pt6 = ev_pts[-1]
    draw.line([(ac_pt6[0] + 10, ac_pt6[1]), (ac_pt6[0] + 10, ev_pt6[1])], fill=(239, 68, 68), width=2)
    draw.text((ac_pt6[0] + 16, (ac_pt6[1] + ev_pt6[1]) // 2 - 6), "CV = -84k€" if lang == 'ES' else "CV = -$84k", fill=(252, 165, 165), font=font_mono)

    # 3. Mini KPI Cards inferiores
    ky0 = gy0 + gh + 12
    kw = (w - 56) // 3
    kh = 68

    # Card 1: CPI
    draw.rounded_rectangle([(x0 + 16, ky0), (x0 + 16 + kw, ky0 + kh)], radius=6, fill=(45, 20, 25), outline=(220, 38, 38), width=1)
    draw.text((x0 + 26, ky0 + 8), "ÍNDICE COSTE (CPI)" if lang == 'ES' else "COST INDEX (CPI)", fill=(252, 165, 165), font=font_small)
    draw.text((x0 + 26, ky0 + 25), "0.86x", fill=(239, 68, 68), font=font_bold)
    draw.text((x0 + 26, ky0 + 46), "Sobrecoste +16.3%" if lang == 'ES' else "+16.3% Cost Overrun", fill=(252, 165, 165), font=font_small)

    # Card 2: SPI
    draw.rounded_rectangle([(x0 + 28 + kw, ky0), (x0 + 28 + 2 * kw, ky0 + kh)], radius=6, fill=(45, 30, 15), outline=(245, 158, 11), width=1)
    draw.text((x0 + 38 + kw, ky0 + 8), "ÍNDICE PLAZO (SPI)" if lang == 'ES' else "SCHED. INDEX (SPI)", fill=(253, 230, 138), font=font_small)
    draw.text((x0 + 38 + kw, ky0 + 25), "0.86x", fill=(245, 158, 11), font=font_bold)
    draw.text((x0 + 38 + kw, ky0 + 46), "Retraso 3 semanas" if lang == 'ES' else "3-Week Delay", fill=(253, 230, 138), font=font_small)

    # Card 3: EAC
    draw.rounded_rectangle([(x0 + 40 + 2 * kw, ky0), (x0 + 40 + 3 * kw, ky0 + kh)], radius=6, fill=(30, 20, 48), outline=(168, 85, 247), width=1)
    draw.text((x0 + 50 + 2 * kw, ky0 + 8), "PREVISIÓN EAC₁" if lang == 'ES' else "EAC₁ FORECAST", fill=(216, 180, 254), font=font_small)
    draw.text((x0 + 50 + 2 * kw, ky0 + 25), "1.395.349 €" if lang == 'ES' else "$1,395,349", fill=(192, 132, 252), font=font_bold)
    draw.text((x0 + 50 + 2 * kw, ky0 + 46), "Déficit VAC: -195k" if lang == 'ES' else "VAC Deficit: -$195k", fill=(216, 180, 254), font=font_small)

    # 4. Barra de Diagnóstico de Riesgo Inferior (centrada y holgada)
    by0 = ky0 + kh + 10
    draw.rounded_rectangle([(x0 + 16, by0), (x0 + w - 16, by0 + 36)], radius=6, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    diag_txt = (
        "DIAGNÓSTICO: Cuadrante 4 (Crisis) -> Plan de Recuperación & Re-baselining EAC."
        if lang == 'ES'
        else "DIAGNOSTIC: Quadrant 4 (Crisis) -> Recovery Plan & EAC Re-baselining."
    )
    draw.text((x0 + 26, by0 + 10), diag_txt, fill=(251, 191, 36), font=font_small)


def generate_cover_image(lang='ES', out_path=None):
    """Genera la imagen de portada completa sin solapes ni glifos rotos."""
    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/cuadro-mando-evm-valor-ganado/cover.png"
        else:
            out_path = "content/en/posts/earned-value-management-evm-dashboard/cover.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado Slate
    draw_linear_gradient(draw, WIDTH, HEIGHT, (15, 23, 42), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes
    f_badge = get_font("segoeuib.ttf", 11)
    f_title = get_font("segoeuib.ttf", 36)
    f_sub = get_font("segoeui.ttf", 16)
    f_pill = get_font("segoeuib.ttf", 12)
    f_bullet = get_font("segoeui.ttf", 13)
    f_guarantee = get_font("segoeui.ttf", 12)
    f_watermark = get_font("segoeuib.ttf", 11)

    f_p_small = get_font("segoeui.ttf", 10)
    f_p_bold = get_font("segoeuib.ttf", 12)
    f_p_mono = get_font("consola.ttf", 10)

    # LADO IZQUIERDO: TEXTOS CORPORATIVOS
    left_x = 55

    # 1. Badge superior con ancho medido dinámicamente
    badge_txt = "DATALARIA EXECUTIVE PACK · ANSI/EIA-748 & PMBOK"
    badge_w = text_width(draw, badge_txt, f_badge) + 28
    draw.rounded_rectangle([(left_x, 50), (left_x + badge_w, 78)], radius=6, fill=(30, 58, 138), outline=(37, 99, 235), width=1)
    draw.text((left_x + 14, 57), badge_txt, fill=(147, 197, 253), font=f_badge)

    # 2. Título Principal
    t1 = "CUADRO DE MANDO EVM" if lang == 'ES' else "EARNED VALUE"
    t2 = "VALOR GANADO & CURVA S" if lang == 'ES' else "MANAGEMENT (EVM)"
    draw.text((left_x, 100), t1, fill=(255, 255, 255), font=f_title)
    draw.text((left_x, 146), t2, fill=(56, 189, 248), font=f_title)

    # 3. Subtítulo
    sub1 = "Curva S, Control de Costes y Plazos," if lang == 'ES' else "S-Curve, Cost & Schedule Control,"
    sub2 = "Varianzas CV/SV & Proyecciones EAC C-Level" if lang == 'ES' else "CV/SV Variances & C-Level EAC Forecasting"
    draw.text((left_x, 210), sub1, fill=(203, 213, 225), font=f_sub)
    draw.text((left_x, 235), sub2, fill=(203, 213, 225), font=f_sub)

    # 4. Píldoras de Entregables con iconos vectoriales Pillow (encuadre dinámico sin desborde)
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

    # 5. Viñetas de Valor Ejecutivo
    bullets = (
        [
            "• Seguimiento en tiempo real: PV, EV, AC, CV/SV e índices CPI/SPI",
            "• Modelos comparativos EAC: Típico (BAC/CPI), Atípico y Compuesto",
            "• Semáforo operativo 2x2 y test estadístico de viabilidad TCPI",
            "• Estándar EIA-748 (27 directrices) y EVM en proyectos híbridos",
        ]
        if lang == 'ES'
        else [
            "• Real-time EVM tracking: PV, EV, AC, CV/SV & CPI/SPI indices",
            "• Comparative EAC models: Typical (BAC/CPI), Atypical & Combined",
            "• 2x2 operational health matrix & statistical TCPI feasibility test",
            "• EIA-748 (27 guidelines) & Hybrid Agile-EVM per PMBOK 7th Ed.",
        ]
    )
    b_y = 342
    for b in bullets:
        draw.text((left_x, b_y), b, fill=(226, 232, 240), font=f_bullet)
        b_y += 24

    # 6. Caja encuadrada de garantía con icono vectorial de rayo
    guar_txt = (
        "Descarga directa inmediata (.ZIP con versiones ES y EN)"
        if lang == 'ES'
        else "Instant direct download (.ZIP with ES & EN versions)"
    )
    guar_w = max(470, 14 + 14 + 10 + text_width(draw, guar_txt, f_guarantee) + 16)
    draw.rounded_rectangle([(left_x, 462), (left_x + guar_w, 494)], radius=6, fill=(24, 45, 40), outline=(16, 185, 129), width=1)
    draw_icon_bolt(draw, left_x + 14, 471)
    draw.text((left_x + 34, 470), guar_txt, fill=(110, 231, 183), font=f_guarantee)

    # 7. Marca de Agua Inferior
    wm_txt = (
        "DATALARIA.COM · EXECUTIVE DECISION PACKS · CONTROL OPERATIVO"
        if lang == 'ES'
        else "DATALARIA.COM · EXECUTIVE DECISION PACKS · OPERATIONS CONTROL"
    )
    draw.text((left_x, 550), wm_txt, fill=(100, 116, 139), font=f_watermark)

    # LADO DERECHO: PANEL ANALÍTICO DE LA CURVA S EVM
    panel_x = 590
    panel_y = 50
    panel_w = 560
    panel_h = 515
    draw_evm_scurve_panel(draw, panel_x, panel_y, panel_w, panel_h, f_p_small, f_p_bold, f_p_mono, lang=lang)

    img.save(out_path, format="PNG", optimize=True)
    print(f"[{lang}] Portada generada exitosamente en: {out_path}")


def generate_all_covers():
    """Genera las portadas en español e inglés."""
    generate_cover_image(lang='ES')
    generate_cover_image(lang='EN')
    print("\nGeneración de portadas cover.png completada con éxito.")


if __name__ == "__main__":
    generate_all_covers()
