#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente las imágenes oficiales para los posts de Datalaria:
1. cover.png (1200 x 630 px, proporción 1.91:1) en:
   - content/es/posts/business-case-financiero-van-tir/cover.png
   - content/en/posts/financial-business-case-npv-irr/cover.png
2. tornado_chart.png (1200 x 700 px) en:
   - content/es/posts/business-case-financiero-van-tir/tornado_chart.png
   - content/en/posts/financial-business-case-npv-irr/tornado_chart.png

Estándar visual Datalaria:
- Paleta Dark Navy (#0F172A), Slate (#1E293B), Azul Consultoría (#2563EB), Ámbar (#F59E0B), Verde (#10B981) y Rojo (#EF4444).
- Gráficos dibujados con Pillow basados estrictamente en las cifras de model_core.py.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

import model_core

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

WIDTH_COVER = 1200
HEIGHT_COVER = 630

WIDTH_TORNADO = 1200
HEIGHT_TORNADO = 700


def get_font(name, size):
    """Carga fuente TrueType del sistema o fallback."""
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
    """Dibuja un degradado diagonal oscuro suave."""
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
    """Dibuja una cuadrícula técnica sutil con cruces en intersecciones."""
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48), width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_cover_graphic_panel(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang='ES'):
    """Dibuja el panel técnico lateral con Curva J acumulada y mini Tornado de barras."""
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # Cabecera del Panel
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR DCF: CURVA J & SENSIBILIDAD" if lang == 'ES' else "DCF ENGINE: J-CURVE & SENSITIVITY"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(245, 158, 11), font=font_bold)
    draw.text((x0 + w - 120, y0 + 13), "WACC 9,5%", fill=(148, 163, 184), font=font_small)

    # 1. Gráfico Superior: Curva J acumulada (y=y0+50, h=160)
    # Eje cero en y = y0 + 125
    y_zero = y0 + 135
    draw.line([(x0 + 20, y_zero), (x0 + w - 20, y_zero)], fill=(71, 85, 105), width=1)
    draw.text((x0 + 24, y_zero - 14), "Eje 0 € (Breakeven)" if lang == 'ES' else "0 $ Axis (Breakeven)", fill=(100, 116, 139), font=font_small)

    # Coordenadas de los 6 puntos (Año 0 a 5) del Flujo Descontado Acumulado
    # Cum PV: Y0: -850k, Y1: -982k, Y2: -564k, Y3: -145k, Y4: +274k, Y5: +693k
    pts_cum = [
        (0, -850), (1, -982), (2, -564), (3, -145), (4, 274), (5, 693)
    ]
    graph_pts = []
    x_step = (w - 70) / 5.0
    for t, val in pts_cum:
        px = x0 + 35 + t * x_step
        # Mapear val [-1000, +800] a [y_zero + 50, y_zero - 60]
        py = y_zero - (val / 1000.0) * 55
        graph_pts.append((px, py))

    # Dibujar líneas de la curva J
    for i in range(len(graph_pts) - 1):
        draw.line([graph_pts[i], graph_pts[i+1]], fill=(37, 99, 235), width=3)

    # Puntos y etiquetas
    for idx, (px, py) in enumerate(graph_pts):
        draw.ellipse([(px - 4, py - 4), (px + 4, py + 4)], fill=(245, 158, 11), outline=(255, 255, 255), width=1)
        draw.text((px - 8, y_zero + 55), f"Y{idx}", fill=(148, 163, 184), font=font_small)

    # Marca del cruce de Payback (Año 3.35)
    pb_x = x0 + 35 + 3.35 * x_step
    draw.line([(pb_x, y_zero - 45), (pb_x, y_zero + 45)], fill=(16, 185, 129), width=2)
    draw.text((pb_x - 30, y_zero + 30), "Payback: 3,35 a" if lang == 'ES' else "Payback: 3.35 y", fill=(52, 211, 153), font=font_bold)

    # 2. Gráfico Inferior: Mini Tornado de Barras (y=y0+225, h=180)
    draw.rounded_rectangle([(x0 + 16, y0 + 225), (x0 + w - 16, y0 + 415)], radius=8, fill=(20, 30, 48), outline=(51, 65, 85))
    draw.text((x0 + 26, y0 + 233), "SENSIBILIDAD TORNADO (TOP 4 DRIVERS)" if lang == 'ES' else "TORNADO SENSITIVITY (TOP 4 DRIVERS)", fill=(241, 245, 249), font=font_bold)

    center_x = x0 + (w // 2)
    draw.line([(center_x, y0 + 255), (center_x, y0 + 405)], fill=(71, 85, 105), width=1)

    top4_drivers = [
        ("Precio Unitario" if lang == 'ES' else "Unit Price", -479, 479),
        ("Volumen Año 1" if lang == 'ES' else "Sales Volume", -449, 449),
        ("Coste Variable %" if lang == 'ES' else "Variable Cost %", -410, 410),
        ("OPEX Fijo Anual" if lang == 'ES' else "Fixed OPEX", -209, 209),
    ]

    for i, (name, d_neg, d_pos) in enumerate(top4_drivers):
        bar_y = y0 + 262 + i * 36
        draw.text((x0 + 26, bar_y - 2), name, fill=(203, 213, 225), font=font_small)

        # Barra negativa (Rojo)
        w_neg = int(abs(d_neg) * 0.22)
        draw.rounded_rectangle([(center_x - w_neg, bar_y + 12), (center_x, bar_y + 22)], radius=3, fill=(239, 68, 68))

        # Barra positiva (Verde)
        w_pos = int(abs(d_pos) * 0.22)
        draw.rounded_rectangle([(center_x, bar_y + 12), (center_x + w_pos, bar_y + 22)], radius=3, fill=(16, 185, 129))

    # 3. Tarjeta Inferior de Métricas Consolidadas
    draw.rounded_rectangle([(x0 + 16, y0 + 425), (x0 + w - 16, y0 + 490)], radius=8, fill=(16, 42, 32), outline=(16, 185, 129))
    draw.text((x0 + 26, y0 + 433), "DICTAMEN: ✅ APROBAR INVERSIÓN (HURDLE CLEARED)" if lang == 'ES' else "VERDICT: ✅ APPROVE INVESTMENT (HURDLE CLEARED)", fill=(110, 231, 183), font=font_bold)
    draw.text((x0 + 26, y0 + 455), "VAN: +693 k€  •  TIR: 28,9%  •  E[VAN]: +741 k€  •  CAPEX: 1,2 M€" if lang == 'ES' else "NPV: +$693k  •  IRR: 28.9%  •  E[NPV]: +$741k  •  CAPEX: $1.2M", fill=(209, 250, 229), font=font_small)


def generate_cover_image(lang='ES', out_path=None):
    """Genera la imagen de portada cover.png (1200 x 630 px)."""
    print(f"\n[GENERANDO PORTADA {lang}] -> {out_path}...")
    img = Image.new("RGB", (WIDTH_COVER, HEIGHT_COVER))
    draw = ImageDraw.Draw(img)

    # 1. Degradado y malla técnica
    draw_linear_gradient(draw, WIDTH_COVER, HEIGHT_COVER, (15, 23, 42), (30, 41, 59))
    draw_technical_grid(draw, WIDTH_COVER, HEIGHT_COVER)

    # Fuentes
    f_badge = get_font("segoeuib.ttf", 13)
    f_title = get_font("segoeuib.ttf", 46)
    f_accent = get_font("segoeuib.ttf", 36)
    f_sub = get_font("segoeui.ttf", 20)
    f_desc = get_font("segoeui.ttf", 15)
    f_pill = get_font("segoeuib.ttf", 13)
    f_watermark = get_font("segoeuib.ttf", 11)
    f_panel_small = get_font("segoeui.ttf", 12)
    f_panel_bold = get_font("segoeuib.ttf", 13)
    f_panel_mono = get_font("consola.ttf", 12)

    # 2. Badge Superior Izquierdo
    badge_txt = (
        "SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN • CORPORATE FINANCE STANDARD"
        if lang == 'ES' else
        "SUITE 02 · DECISION ANALYSIS & PRIORITIZATION • CORPORATE FINANCE STANDARD"
    )
    draw.rounded_rectangle([(60, 45), (630, 77)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235), width=2)
    draw.text((75, 52), badge_txt, fill=(96, 165, 250), font=f_badge)

    # 3. Título Principal
    y_cursor = 100
    t1 = "BUSINESS CASE FINANCIERO" if lang == 'ES' else "FINANCIAL BUSINESS CASE"
    draw.text((60, y_cursor), t1, fill=(255, 255, 255), font=f_title)
    y_cursor += 56

    t2 = "VAN · TIR · PAYBACK & TORNADO" if lang == 'ES' else "NPV · IRR · PAYBACK & TORNADO"
    draw.text((60, y_cursor), t2, fill=(245, 158, 11), font=f_accent)
    y_cursor += 50

    # 4. Subtítulo
    sub_txt = (
        "Flujo de Caja Descontado, Gráfico Tornado & Decisión C-Level"
        if lang == 'ES' else
        "Discounted Cash Flow, Tornado Chart & C-Level Investment Decision"
    )
    draw.text((60, y_cursor), sub_txt, fill=(203, 213, 225), font=f_sub)
    y_cursor += 36

    # 5. Viñetas de Características
    bullets = [
        "• Modelo DCF institucional a 5 años con cálculo de WACC vía CAPM.",
        "• Sensibilidad univariable Tornado con análisis de amplitud y break-even.",
        "• Plan de inversión por tramos condicionados, stage gates y kill criteria.",
    ] if lang == 'ES' else [
        "• Institutional 5-year DCF model with CAPM-underwritten WACC.",
        "• Univariate Tornado sensitivity with swing ranking and break-even thresholds.",
        "• Milestone-gated investment staging with OEE stage gates and kill criteria.",
    ]
    for b in bullets:
        draw.text((60, y_cursor), b, fill=(148, 163, 184), font=f_desc)
        y_cursor += 24

    # 6. Píldoras de Entregables
    y_pills = 465
    pills = [
        ("📊 Excel + Sheets", 185),
        ("📑 PPTX 16:9 C-Level", 215),
        ("📄 Guía PDF Minto", 185),
    ] if lang == 'ES' else [
        ("📊 Excel + Sheets", 185),
        ("📑 C-Level 16:9 Deck", 215),
        ("📄 PDF Minto Guide", 185),
    ]
    px = 60
    for p_txt, p_w in pills:
        draw.rounded_rectangle([(px, y_pills), (px + p_w, y_pills + 38)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
        draw.text((px + 14, y_pills + 9), p_txt, fill=(241, 245, 249), font=f_pill)
        px += p_w + 14

    # 7. Panel Gráfico Lateral (Lado Derecho: x=670, y=45, w=470, h=510)
    draw_cover_graphic_panel(draw, 670, 45, 470, 510, f_panel_small, f_panel_bold, f_panel_mono, lang)

    # 8. Marca de Agua Inferior
    wm = "DATALARIA.COM · EXECUTIVE DECISION PACKS · STANDARD TIER-1"
    draw.text((60, 585), wm, fill=(100, 116, 139), font=f_watermark)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Portada generada exitosamente: {out_path}")


def generate_tornado_chart_image(lang='ES', out_path=None):
    """Genera la imagen ilustrativa del gráfico tornado tornado_chart.png (1200 x 700 px)."""
    print(f"\n[GENERANDO TORNADO CHART {lang}] -> {out_path}...")
    img = Image.new("RGB", (WIDTH_TORNADO, HEIGHT_TORNADO))
    draw = ImageDraw.Draw(img)

    # Fondo degradado
    draw_linear_gradient(draw, WIDTH_TORNADO, HEIGHT_TORNADO, (15, 23, 42), (30, 41, 59))
    draw_technical_grid(draw, WIDTH_TORNADO, HEIGHT_TORNADO)

    f_title = get_font("segoeuib.ttf", 26)
    f_sub = get_font("segoeui.ttf", 15)
    f_driver = get_font("segoeuib.ttf", 14)
    f_val = get_font("segoeui.ttf", 13)
    f_bold = get_font("segoeuib.ttf", 13)
    f_card = get_font("segoeui.ttf", 13)

    # Cabecera
    t_text = (
        "ANÁLISIS DE SENSIBILIDAD TORNADO: IMPACTO EN EL VAN (€)"
        if lang == 'ES' else
        "TORNADO SENSITIVITY ANALYSIS: IMPACT ON NET PRESENT VALUE ($)"
    )
    sub_text = (
        "Perturbaciones univariables sobre el Escenario Base (VAN = +693 k€, WACC = 9,50%) • Clasificación por Amplitud (Swing)"
        if lang == 'ES' else
        "Univariate perturbations over Base Case (NPV = +$693k, WACC = 9.50%) • Ordered by Swing Amplitude"
    )
    draw.text((60, 35), t_text, fill=(255, 255, 255), font=f_title)
    draw.text((60, 72), sub_text, fill=(203, 213, 225), font=f_sub)

    # Área del gráfico
    # Eje central de referencia (VAN Base Δ = 0)
    x_center = 580
    y_start = 135
    row_h = 58

    draw.line([(x_center, y_start - 15), (x_center, y_start + 8 * row_h)], fill=(100, 116, 139), width=2)
    base_lbl = "Caso Base: 0 € (VAN 693 k€)" if lang == 'ES' else "Base Case: $0 (NPV $693k)"
    draw.text((x_center - 80, y_start - 30), base_lbl, fill=(245, 158, 11), font=f_bold)

    # Escala de píxeles por k€: 500 k€ = 230 px -> 0.46 px/k€
    scale = 0.46

    for i, row_data in enumerate(model_core.TORNADO_RESULTS):
        y_row = y_start + i * row_h
        name = row_data["name_es"] if lang == 'ES' else row_data["name_en"]
        d_neg_k = row_data["delta_pessimistic"] / 1000.0
        d_pos_k = row_data["delta_optimistic"] / 1000.0
        swing_k = row_data["swing"] / 1000.0

        # Etiqueta del driver (Columna izquierda)
        draw.text((60, y_row + 8), f"{i+1}. {name}", fill=(241, 245, 249), font=f_driver)

        # Barra negativa (Rojo)
        w_neg = int(abs(d_neg_k) * scale)
        x_left = x_center - w_neg
        draw.rounded_rectangle([(x_left, y_row + 4), (x_center, y_row + 30)], radius=4, fill=(239, 68, 68), outline=(220, 38, 38))
        draw.text((x_left - 85, y_row + 8), f"{d_neg_k:,.0f} k€" if lang == 'ES' else f"{d_neg_k:,.0f} $k", fill=(248, 113, 113), font=f_val)

        # Barra positiva (Verde)
        w_pos = int(abs(d_pos_k) * scale)
        x_right = x_center + w_pos
        draw.rounded_rectangle([(x_center, y_row + 4), (x_right, y_row + 30)], radius=4, fill=(16, 185, 129), outline=(5, 150, 105))
        draw.text((x_right + 12, y_row + 8), f"+{d_pos_k:,.0f} k€" if lang == 'ES' else f"+{d_pos_k:,.0f} $k", fill=(52, 211, 153), font=f_val)

        # Amplitud Swing
        draw.text((1050, y_row + 8), f"Swing: {swing_k:,.0f} k€" if lang == 'ES' else f"Swing: ${swing_k:,.0f}k", fill=(148, 163, 184), font=f_val)

    # Leyenda inferior y tarjeta de Puntos de Equilibrio
    y_foot = y_start + 8 * row_h + 20
    draw.rounded_rectangle([(60, y_foot), (1140, y_foot + 65)], radius=10, fill=(15, 23, 42), outline=(51, 65, 85), width=1)

    be_text = (
        "PUNTOS DE EQUILIBRIO (BREAK-EVEN):  Precio: 19,21 €/u (-23,2%)  •  Volumen: 76.840 u. (-23,2%)  •  CAPEX: 2,07 M€ (+72,5%)\n"
        "Dictamen de Riesgo: Precio y Volumen explican el 68% de la dispersión del VAN; margen de seguridad confortable ante caídas de demanda."
        if lang == 'ES' else
        "BREAK-EVEN THRESHOLDS (NPV = 0):  Price: $19.21/u (-23.2%)  •  Volume: 76,840 units (-23.2%)  •  CAPEX: $2.07M (+72.5%)\n"
        "Risk Diagnostic: Price and Volume drive 68% of NPV variance; robust margin of safety against commercial volume contraction."
    )
    draw.text((80, y_foot + 14), be_text, fill=(203, 213, 225), font=f_card)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Gráfico Tornado generado exitosamente: {out_path}")


def main():
    # Rutas para posts ES y EN
    dir_post_es = os.path.join("content", "es", "posts", "business-case-financiero-van-tir")
    dir_post_en = os.path.join("content", "en", "posts", "financial-business-case-npv-irr")

    # 1. Portadas cover.png
    generate_cover_image(lang='ES', out_path=os.path.join(dir_post_es, "cover.png"))
    generate_cover_image(lang='EN', out_path=os.path.join(dir_post_en, "cover.png"))

    # 2. Ilustración tornado_chart.png
    generate_tornado_chart_image(lang='ES', out_path=os.path.join(dir_post_es, "tornado_chart.png"))
    generate_tornado_chart_image(lang='EN', out_path=os.path.join(dir_post_en, "tornado_chart.png"))

    print("\n[ÉXITO] Generación de imágenes PNG completada.")


if __name__ == "__main__":
    main()
