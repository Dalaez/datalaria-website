#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_post4_cover.py
=======================
Genera la portada oficial para el Post 4 de Datalaria Pulse:
- Título: Google Analytics 4 y Search Console Automatizados: Cómo Medir el ROI Orgánico
- Dimensiones: 1200 x 630 px (proporción 16:9 / OpenGraph)
- Badge oficial: Onda de pulso azul cyan (#38bdf8) + "4/5" + pill identificadora
- Composición: Ventana ejecutiva flotante con captura real del panel de Salud & ROI
  (Patrimonio Editorial $21.480 USD + Matriz de 4 Cuadrantes: Joyas SEO, Motores de Tráfico,
   Candidatos a Refresh y Brecha de Monetización) y chips de telemetría GA4/GSC.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1200
HEIGHT = 630

def draw_pulse_waveform(draw, x: float, y: float, w: float, h: float, color=(56, 189, 248), stroke_width=2):
    pts = [
        (2.0, 12.0),
        (6.0, 12.0),
        (9.0, 3.0),
        (15.0, 21.0),
        (18.0, 12.0),
        (22.0, 12.0)
    ]
    scaled_pts = []
    for px, py in pts:
        sx = x + (px / 24.0) * w
        sy = y + (py / 24.0) * h
        scaled_pts.append((sx, sy))

    for i in range(len(scaled_pts) - 1):
        p1 = scaled_pts[i]
        p2 = scaled_pts[i + 1]
        draw.line([p1, p2], fill=color, width=stroke_width)

def get_font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def create_window_box(width: int, height: int, title: str, crop_img: Image.Image, accent_color=(16, 185, 129)) -> Image.Image:
    panel = Image.new("RGBA", (width, height), (11, 17, 32, 255))
    draw = ImageDraw.Draw(panel)
    bar_h = 28

    # Borde exterior con glow suave
    draw.rounded_rectangle([0, 0, width, height], radius=10, fill=(11, 17, 32, 255), outline=(accent_color[0], accent_color[1], accent_color[2], 180), width=1)
    draw.rectangle([0, bar_h, width, height], fill=(13, 20, 36, 255))

    # Dots Mac
    draw.ellipse([14, 8, 22, 16], fill=(239, 68, 68, 240))
    draw.ellipse([27, 8, 35, 16], fill=(234, 179, 8, 240))
    draw.ellipse([40, 8, 48, 16], fill=(34, 197, 94, 240))

    # Título de ventana
    font_title = get_font(12, bold=True)
    draw.text((60, 6), title, font=font_title, fill=(241, 245, 249, 240))

    # Badges en la barra de ventana
    font_mini = get_font(10, bold=True)
    badge_x = width - 260
    draw.rounded_rectangle([badge_x, 5, badge_x + 115, bar_h - 5], radius=4, fill=(16, 185, 129, 30), outline=(16, 185, 129, 120), width=1)
    draw.text((badge_x + 8, 7), "INV-PULSE-2 COMPLIANT", font=font_mini, fill=(52, 211, 153, 240))

    badge2_x = width - 135
    draw.rounded_rectangle([badge2_x, 5, badge2_x + 120, bar_h - 5], radius=4, fill=(6, 182, 212, 30), outline=(6, 182, 212, 120), width=1)
    draw.text((badge2_x + 8, 7), "GA4 + GSC EN VIVO", font=font_mini, fill=(56, 189, 248, 240))

    # Encajar la captura manteniendo proporción exacta
    inner_w = width - 2
    inner_h = height - bar_h - 2

    src_w, src_h = crop_img.size
    target_ratio = inner_w / inner_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        crop_w = int(src_h * target_ratio)
        x_off = (src_w - crop_w) // 2
        fitted = crop_img.crop((x_off, 0, x_off + crop_w, src_h))
    else:
        crop_h = int(src_w / target_ratio)
        y_off = (src_h - crop_h) // 2
        fitted = crop_img.crop((0, y_off, src_w, y_off + crop_h))

    fitted_resized = fitted.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    panel.paste(fitted_resized, (1, bar_h + 1))

    return panel

def generate_post4_cover(out_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    # 1. Canvas Base con gradiente profundo
    img = Image.new("RGBA", (WIDTH, HEIGHT), (7, 12, 22, 255))
    draw = ImageDraw.Draw(img)

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(6 + (12 - 6) * ratio)
        g = int(10 + (22 - 10) * ratio)
        b = int(20 + (38 - 20) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # 2. Resplandores ambientales técnicos (Verde ROI + Azul GA4 + Púrpura)
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([WIDTH // 2 - 350, 60, WIDTH // 2 + 350, 420], fill=(16, 185, 129, 28))   # Esmeralda ROI central
    g_draw.ellipse([50, 180, 500, 580], fill=(6, 182, 212, 26))                               # Cian GA4 izquierda
    g_draw.ellipse([700, 200, 1180, 600], fill=(168, 85, 247, 24))                             # Púrpura derecha
    g_draw.ellipse([20, -20, 350, 160], fill=(56, 189, 248, 25))                               # Azul badge
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 3. Malla técnica sutil (grid blueprint)
    grid_color = (18, 28, 48, 255)
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color)

    # 4. Header Bar con Badge de Serie Oficial (4/5)
    bx = 42
    by = 18
    bw = 78
    bh = 38
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=9, fill=(10, 18, 32, 220), outline=(56, 189, 248, 180), width=1)
    draw_pulse_waveform(draw, bx + 7, by + 7, 30, 24, color=(56, 189, 248, 90), stroke_width=4)
    draw_pulse_waveform(draw, bx + 7, by + 7, 30, 24, color=(56, 189, 248, 255), stroke_width=2)
    draw.line([(bx + 42, by + 9), (bx + 42, by + bh - 9)], fill=(71, 85, 105, 180), width=1)
    font_badge = get_font(13, bold=True)
    draw.text((bx + 48, by + 10), "4/5", font=font_badge, fill=(244, 114, 182, 240))

    # Píldora de temática
    font_stack = get_font(11, bold=True)
    draw.rounded_rectangle([bx + bw + 14, by + 6, bx + bw + 340, by + bh - 6], radius=5, fill=(15, 23, 42, 210), outline=(51, 65, 85, 170), width=1)
    draw.text((bx + bw + 24, by + 9), "TELEMETRÍA ORGÁNICA: GA4 • GSC • SALUD & ROI", font=font_stack, fill=(52, 211, 153, 255))

    font_mono = get_font(11, bold=False)
    draw.text((WIDTH - 280, by + 10), "datalaria.com  |  Pulse Cockpit", font=font_mono, fill=(100, 116, 139, 220))

    # 5. Cargar la captura real del panel de Salud & ROI
    p_health = r"C:\Users\dalae\.gemini\antigravity\brain\9cc3e8ea-e324-41b5-80e8-6114503cfb4d\health_matrix_crop.png"
    if not os.path.exists(p_health):
        raise FileNotFoundError(f"No se encontró {p_health}")

    raw_health = Image.open(p_health).convert("RGBA")

    # Ventana Principal: Panel Ejecutivo de Salud y Matriz de 4 Cuadrantes
    w_x, w_y = 42, 72
    w_w, w_h = 1116, 460
    win_health = create_window_box(
        w_w, w_h,
        "Datalaria Pulse — Panel de Salud Editorial, Patrimonio Estimado y Matriz de 4 Cuadrantes",
        raw_health,
        accent_color=(16, 185, 129)
    )

    # 6. Barra Inferior de Métricas y Fórmulas
    foot_y = 546
    foot_h = 66
    draw.rounded_rectangle([w_x, foot_y, w_x + w_w, foot_y + foot_h], radius=8, fill=(10, 18, 30, 230), outline=(30, 41, 59, 200), width=1)

    # 3 Pills informativas en el footer
    font_kpi_lbl = get_font(9, bold=True)
    font_kpi_val = get_font(12, bold=True)
    font_formula = get_font(10, bold=False)

    # KPI 1: Patrimonio Editorial
    kpi1_x = w_x + 20
    draw.text((kpi1_x, foot_y + 12), "PATRIMONIO EDITORIAL ESTIMADO", font=font_kpi_lbl, fill=(100, 116, 139, 240))
    draw.text((kpi1_x, foot_y + 30), "$21.480 USD", font=font_kpi_val, fill=(52, 211, 153, 255))
    draw.text((kpi1_x + 115, foot_y + 32), "(214.800 palabras @ $0.10/palabra)", font=font_formula, fill=(148, 163, 184, 200))

    # Divisor 1
    draw.line([(w_x + 400, foot_y + 12), (w_x + 400, foot_y + foot_h - 12)], fill=(51, 65, 85, 150), width=1)

    # KPI 2: Principio de Relativización (Base 100)
    kpi2_x = w_x + 420
    draw.text((kpi2_x, foot_y + 12), "NORMALIZACIÓN DETERMINISTA (INV-PULSE-2)", font=font_kpi_lbl, fill=(100, 116, 139, 240))
    draw.text((kpi2_x, foot_y + 30), "I₁₀₀ = (Vᵢ / Ṽ) × 100", font=font_kpi_val, fill=(56, 189, 248, 255))
    draw.text((kpi2_x + 165, foot_y + 32), "|  Centrado en Mediana + Percentil Rank", font=font_formula, fill=(148, 163, 184, 200))

    # Divisor 2
    draw.line([(w_x + 780, foot_y + 12), (w_x + 780, foot_y + foot_h - 12)], fill=(51, 65, 85, 150), width=1)

    # KPI 3: Ingesta Automática
    kpi3_x = w_x + 800
    draw.text((kpi3_x, foot_y + 12), "FUENTES DE TELEMETRÍA (READ-ONLY)", font=font_kpi_lbl, fill=(100, 116, 139, 240))
    draw.text((kpi3_x, foot_y + 30), "Google Cloud Service Account", font=font_kpi_val, fill=(192, 132, 252, 255))
    draw.text((kpi3_x + 205, foot_y + 32), "|  GA4 Data API + GSC v1", font=font_formula, fill=(148, 163, 184, 200))

    # Sombra elevada para la ventana
    shadows = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadows)
    s_draw.rounded_rectangle([w_x - 6, w_y - 4, w_x + w_w + 6, w_y + w_h + 8], radius=14, fill=(0, 0, 0, 200))
    shadows = shadows.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img, shadows)

    # Pegar ventana
    img.paste(win_health, (w_x, w_y), win_health)

    # Guardar
    final_rgb = img.convert("RGB")
    final_rgb.save(out_path, format="PNG", quality=95)
    print(f"[OK] Portada Post 4 guardada en: {out_path} ({WIDTH}x{HEIGHT})")

if __name__ == "__main__":
    out_es = "content/es/posts/pulse-parte4-ga4-search-console-automatico/cover.png"
    out_en = "content/en/posts/pulse-part4-ga4-search-console-automated/cover.png"
    generate_post4_cover(out_es)
    generate_post4_cover(out_en)
