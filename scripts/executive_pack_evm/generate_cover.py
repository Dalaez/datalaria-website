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
- Badge superior: "DATALARIA EXECUTIVE DECISION PACK • ANSI/EIA-748 / PMBOK STANDARD"
- Título principal: "CUADRO DE MANDO EVM / VALOR GANADO" / "EARNED VALUE MANAGEMENT (EVM)"
- Subtítulo: "Curva S, Control de Costes y Plazos & Proyecciones EAC C-Level"
- Panel analítico derecho: Gráfico cartesiano de Curva S (PV azul, EV verde, AC rojo, EAC púrpura) con fecha de corte y brecha de varianza.
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


def draw_evm_scurve_panel(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang='ES'):
    """
    Dibuja el panel analítico ejecutivo del motor EVM:
    - Cabecera: Ecuaciones canónicas ANSI/EIA-748 (CPI, SPI, EAC).
    - Gráfico Curva S cartesiano: PV (azul), EV (verde), AC (rojo) y Proyección EAC (púrpura).
    - Línea vertical de corte en Mes 6 y brecha de varianza CV/SV.
    - 3 KPI Cards inferiores (CPI, SPI, EAC).
    - Barra de diagnóstico inferior.
    """
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR ANALÍTICO EVM (ANSI/EIA-748)" if lang == 'ES' else "EVM ANALYTICAL ENGINE (ANSI/EIA-748)"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(2, 132, 199), font=font_bold)
    sub_panel = "CPI = EV/AC · SPI = EV/PV · EAC = BAC/CPI"
    draw.text((x0 + w - 240, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. Área del Gráfico de la Curva S
    gx0 = x0 + 20
    gy0 = y0 + 50
    gw = w - 40
    gh = 240

    draw.rounded_rectangle([(gx0, gy0), (gx0 + gw, gy0 + gh)], radius=8, fill=(24, 33, 50), outline=(51, 65, 85), width=1)

    # Eje horizontal y vertical
    base_y = gy0 + gh - 35
    top_y = gy0 + 25
    draw.line([(gx0 + 35, base_y), (gx0 + gw - 25, base_y)], fill=(71, 85, 105), width=1)
    draw.line([(gx0 + 35, base_y), (gx0 + 35, top_y)], fill=(71, 85, 105), width=1)

    # Eje X: 12 meses
    plot_w = gw - 65
    step_x = plot_w / 11.0

    # Puntos de la Curva S (Normalizados de 0 a 1):
    # PV (12 meses): sigmoide clásica
    pv_vals = [0.05, 0.12, 0.20, 0.30, 0.40, 0.50, 0.62, 0.72, 0.82, 0.90, 0.96, 1.00]
    # EV (hasta mes 6): retraso respecto a PV (43% en mes 6)
    ev_vals = [0.048, 0.11, 0.187, 0.266, 0.348, 0.43]
    # AC (hasta mes 6): sobrecoste respecto a EV (50% en mes 6)
    ac_vals = [0.052, 0.122, 0.212, 0.307, 0.403, 0.50]
    # EAC Proyección (meses 6 a 12): sube hasta 1.163 (1.395M / 1.2M)
    eac_vals = [0.50, 0.61, 0.72, 0.83, 0.94, 1.05, 1.163]

    # Convertir a coordenadas de pixel
    def to_coords(m_idx, val):
        px = gx0 + 35 + m_idx * step_x
        # Escala: 0 en base_y, 1.2 en top_y
        ratio = val / 1.25
        py = base_y - ratio * (base_y - top_y)
        return (px, py)

    pv_pts = [to_coords(i, v) for i, v in enumerate(pv_vals)]
    ev_pts = [to_coords(i, v) for i, v in enumerate(ev_vals)]
    ac_pts = [to_coords(i, v) for i, v in enumerate(ac_vals)]
    eac_pts = [to_coords(5 + i, v) for i, v in enumerate(eac_vals)]

    # Dibujar líneas de cuadrícula horizontal
    for tick in [0.25, 0.50, 0.75, 1.00]:
        _, ty = to_coords(0, tick)
        draw.line([(gx0 + 35, ty), (gx0 + gw - 25, ty)], fill=(35, 48, 70), width=1)

    # 1. Trazar PV (Azul)
    for i in range(len(pv_pts) - 1):
        draw.line([pv_pts[i], pv_pts[i+1]], fill=(37, 99, 235), width=2)
    for pt in pv_pts:
        draw.ellipse([(pt[0]-2, pt[1]-2), (pt[0]+2, pt[1]+2)], fill=(37, 99, 235))

    # 2. Trazar EAC Proyección (Púrpura discontinua)
    for i in range(len(eac_pts) - 1):
        draw.line([eac_pts[i], eac_pts[i+1]], fill=(124, 58, 237), width=2)
    for pt in eac_pts:
        draw.ellipse([(pt[0]-2, pt[1]-2), (pt[0]+2, pt[1]+2)], fill=(124, 58, 237))

    # 3. Trazar AC (Rojo)
    for i in range(len(ac_pts) - 1):
        draw.line([ac_pts[i], ac_pts[i+1]], fill=(220, 38, 38), width=3)
    for pt in ac_pts:
        draw.ellipse([(pt[0]-3, pt[1]-3), (pt[0]+3, pt[1]+3)], fill=(220, 38, 38))

    # 4. Trazar EV (Verde)
    for i in range(len(ev_pts) - 1):
        draw.line([ev_pts[i], ev_pts[i+1]], fill=(16, 185, 129), width=3)
    for pt in ev_pts:
        draw.ellipse([(pt[0]-3, pt[1]-3), (pt[0]+3, pt[1]+3)], fill=(16, 185, 129))

    # Línea vertical de corte en Mes 6
    cut_x, _ = to_coords(5, 0)
    draw.line([(cut_x, base_y), (cut_x, top_y - 10)], fill=(148, 163, 184), width=1)
    lbl_cut = "Corte M06" if lang == 'ES' else "Cutoff M06"
    draw.text((cut_x - 24, base_y + 8), lbl_cut, fill=(148, 163, 184), font=font_mono)

    # Etiquetas de curvas en el gráfico
    draw.text((gx0 + 45, top_y - 8), "PV: Baseline", fill=(37, 99, 235), font=font_small)
    draw.text((gx0 + 130, top_y - 8), "EV: Real", fill=(16, 185, 129), font=font_small)
    draw.text((gx0 + 195, top_y - 8), "AC: Gasto", fill=(220, 38, 38), font=font_small)
    draw.text((gx0 + 265, top_y - 8), "EAC Proyección", fill=(124, 58, 237), font=font_small)

    # Indicador de brecha CV y SV en mes 6
    ac_pt6 = ac_pts[-1]
    ev_pt6 = ev_pts[-1]
    # Corchete o flecha entre AC y EV
    draw.line([(ac_pt6[0] + 8, ac_pt6[1]), (ac_pt6[0] + 8, ev_pt6[1])], fill=(239, 68, 68), width=2)
    draw.text((ac_pt6[0] + 12, (ac_pt6[1] + ev_pt6[1]) // 2 - 6), "CV = -84k€" if lang == 'ES' else "CV = -$84k", fill=(252, 165, 165), font=font_mono)

    # 3. Mini KPI Cards inferiores
    ky0 = y0 + 302
    kw = (w - 56) // 3
    kh = 70

    # Card 1: CPI
    draw.rounded_rectangle([(x0 + 16, ky0), (x0 + 16 + kw, ky0 + kh)], radius=6, fill=(45, 20, 25), outline=(220, 38, 38), width=1)
    draw.text((x0 + 26, ky0 + 8), "ÍNDICE COSTE (CPI)" if lang == 'ES' else "COST INDEX (CPI)", fill=(252, 165, 165), font=font_small)
    draw.text((x0 + 26, ky0 + 26), "0.86x", fill=(239, 68, 68), font=font_bold)
    draw.text((x0 + 26, ky0 + 48), "Sobrecoste +16.3%" if lang == 'ES' else "+16.3% Cost Overrun", fill=(252, 165, 165), font=font_small)

    # Card 2: SPI
    draw.rounded_rectangle([(x0 + 28 + kw, ky0), (x0 + 28 + 2 * kw, ky0 + kh)], radius=6, fill=(45, 30, 15), outline=(245, 158, 11), width=1)
    draw.text((x0 + 38 + kw, ky0 + 8), "ÍNDICE PLAZO (SPI)" if lang == 'ES' else "SCHED. INDEX (SPI)", fill=(253, 230, 138), font=font_small)
    draw.text((x0 + 38 + kw, ky0 + 26), "0.86x", fill=(245, 158, 11), font=font_bold)
    draw.text((x0 + 38 + kw, ky0 + 48), "Retraso 3 semanas" if lang == 'ES' else "3-Week Delay", fill=(253, 230, 138), font=font_small)

    # Card 3: EAC
    draw.rounded_rectangle([(x0 + 40 + 2 * kw, ky0), (x0 + 40 + 3 * kw, ky0 + kh)], radius=6, fill=(30, 20, 48), outline=(124, 58, 237), width=1)
    draw.text((x0 + 50 + 2 * kw, ky0 + 8), "PREVISIÓN EAC 1" if lang == 'ES' else "EAC 1 FORECAST", fill=(216, 180, 254), font=font_small)
    draw.text((x0 + 50 + 2 * kw, ky0 + 26), "1.395.349 €" if lang == 'ES' else "$1,395,349", fill=(168, 85, 247), font=font_bold)
    draw.text((x0 + 50 + 2 * kw, ky0 + 48), "Déficit VAC: -195k" if lang == 'ES' else "VAC Deficit: -$195k", fill=(216, 180, 254), font=font_small)

    # 4. Barra de Diagnóstico de Riesgo Inferior
    by0 = ky0 + kh + 10
    draw.rounded_rectangle([(x0 + 16, by0), (x0 + w - 16, by0 + 36)], radius=6, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    diag_txt = (
        "DIAGNÓSTICO: Cuadrante 4 (Crisis de Coste y Plazo) -> Requiere Plan de Recuperación & Re-baselining EAC."
        if lang == 'ES' else
        "DIAGNOSTIC: Quadrant 4 (Cost & Schedule Crisis) -> Requires Recovery Plan & EAC Re-baselining."
    )
    draw.text((x0 + 26, by0 + 10), diag_txt, fill=(251, 191, 36), font=font_small)


def generate_cover_image(lang='ES', out_path=None):
    """Genera la imagen de portada completa."""
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
    f_badge = get_font("segoeuib.ttf", 12)
    f_title = get_font("segoeuib.ttf", 34)
    f_sub = get_font("segoeui.ttf", 15)
    f_pill = get_font("segoeuib.ttf", 12)
    f_guarantee = get_font("segoeui.ttf", 12)
    f_watermark = get_font("segoeuib.ttf", 11)

    f_p_small = get_font("segoeui.ttf", 10)
    f_p_bold = get_font("segoeuib.ttf", 11)
    f_p_mono = get_font("consola.ttf", 10)

    # LADO IZQUIERDO: TEXTOS CORPORATIVOS
    left_x = 55

    # 1. Badge superior
    badge_txt = "DATALARIA EXECUTIVE DECISION PACK · ANSI/EIA-748 / PMBOK STANDARD"
    draw.rounded_rectangle([(left_x, 48), (left_x + 530, 78)], radius=6, fill=(30, 58, 138), outline=(37, 99, 235), width=1)
    draw.text((left_x + 14, 55), badge_txt, fill=(147, 197, 253), font=f_badge)

    # 2. Título Principal
    t1 = "CUADRO DE MANDO EVM" if lang == 'ES' else "EARNED VALUE"
    t2 = "VALOR GANADO & CURVA S" if lang == 'ES' else "MANAGEMENT (EVM)"
    draw.text((left_x, 100), t1, fill=(255, 255, 255), font=f_title)
    draw.text((left_x, 144), t2, fill=(56, 189, 248), font=f_title)

    # 3. Subtítulo
    sub_t = (
        "Curva S, Control de Costes y Plazos,\nVarianzas CV/SV & Proyecciones EAC C-Level"
        if lang == 'ES' else
        "S-Curve, Cost & Schedule Control,\nCV/SV Variances & C-Level EAC Forecasting"
    )
    draw.text((left_x, 206), sub_t, fill=(203, 213, 225), font=f_sub)

    # 4. Píldoras de Entregables
    pills = [
        ("📊 Excel + Sheets", (30, 41, 59), (51, 65, 85), (255, 255, 255)),
        ("📑 PPTX 16:9 C-Level", (30, 41, 59), (51, 65, 85), (255, 255, 255)),
        ("📄 Guía PDF (5 págs)", (30, 41, 59), (51, 65, 85), (255, 255, 255))
        if lang == 'ES' else
        ("📄 PDF Guide (5 pgs)", (30, 41, 59), (51, 65, 85), (255, 255, 255)),
    ]
    px = left_x
    py = 295
    for p_txt, p_bg, p_border, p_col in pills:
        pw = int(len(p_txt) * 9.2) + 18
        draw.rounded_rectangle([(px, py), (px + pw, py + 32)], radius=6, fill=p_bg, outline=p_border, width=1)
        draw.text((px + 10, py + 7), p_txt, fill=p_col, font=f_pill)
        px += pw + 12

    # 5. Mensaje de Garantía
    guar_txt = "Descarga directa inmediata (.ZIP)" if lang == 'ES' else "Instant direct download (.ZIP)"
    draw.text((left_x, 348), f"✓ {guar_txt}", fill=(16, 185, 129), font=f_guarantee)

    # 6. Bullets de Valor Ejecutivo
    b_y = 390
    bullets = [
        "• Cálculo en tiempo real: PV, EV, AC, varianzas CV/SV e índices CPI/SPI",
        "• Modelos comparativos EAC: Típico (BAC/CPI), Atípico y Compuesto",
        "• Semáforo de salud operativa 2x2 y viabilidad estadística TCPI",
        "• Plantilla PPTX 16:9 Minto lista para defender ante el Comité / Board"
    ] if lang == 'ES' else [
        "• Real-time EVM tracking: PV, EV, AC, CV/SV variances & CPI/SPI indices",
        "• Comparative EAC models: Typical (BAC/CPI), Atypical & Combined",
        "• 2x2 Operational health matrix & statistical TCPI feasibility testing",
        "• Minto 16:9 executive deck ready for C-Level & Board defense"
    ]
    for b in bullets:
        draw.text((left_x, b_y), b, fill=(148, 163, 184), font=f_p_small)
        b_y += 24

    # 7. Marca de Agua Inferior
    wm_txt = "DATALARIA.COM · EXECUTIVE DECISION PACKS · CONTROL OPERATIVO"
    draw.text((left_x, 565), wm_txt, fill=(71, 85, 105), font=f_watermark)

    # LADO DERECHO: PANEL ANALÍTICO DE LA CURVA S EVM
    draw_evm_scurve_panel(draw, 620, 50, 525, 525, f_p_small, f_p_bold, f_p_mono, lang=lang)

    img.save(out_path, format="PNG", optimize=True)
    print(f"[{lang}] Portada generada exitosamente en: {out_path}")


def generate_all_covers():
    """Genera las portadas en español e inglés."""
    generate_cover_image(lang='ES')
    generate_cover_image(lang='EN')
    print("\nGeneración de portadas cover.png completada con éxito.")


if __name__ == "__main__":
    generate_all_covers()
