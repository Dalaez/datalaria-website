#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_post3_collage_v2.py
============================
Genera el collage balanceado y proporcional de las 3 vistas de la App:
- Arriba (Ancho completo): Tabla Ejecutiva (con búsqueda, filtros y filas)
- Abajo Izquierda: Tablero Kanban (5 columnas de ciclo de vida)
- Abajo Derecha: Calendario Editorial (planificación cronológica)

Respeta el aspect ratio natural de cada captura (cero distorsión vertical).
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

def create_window_box(width: int, height: int, title: str, crop_img: Image.Image, accent_color=(56, 189, 248)) -> Image.Image:
    panel = Image.new("RGBA", (width, height), (11, 17, 32, 255))
    draw = ImageDraw.Draw(panel)
    bar_h = 24

    # Borde exterior
    draw.rounded_rectangle([0, 0, width, height], radius=9, fill=(11, 17, 32, 255), outline=(accent_color[0], accent_color[1], accent_color[2], 170), width=1)
    draw.rectangle([0, bar_h, width, height], fill=(13, 20, 36, 255))

    # Dots Mac
    draw.ellipse([11, 6, 19, 14], fill=(239, 68, 68, 240))
    draw.ellipse([24, 6, 32, 14], fill=(234, 179, 8, 240))
    draw.ellipse([37, 6, 45, 14], fill=(34, 197, 94, 240))

    # Título
    font_title = get_font(11, bold=True)
    draw.text((54, 5), title, font=font_title, fill=(226, 232, 240, 240))

    # Encajar la captura manteniendo proporción (cover / fill centrado)
    inner_w = width - 2
    inner_h = height - bar_h - 2

    # Aspect ratios
    src_w, src_h = crop_img.size
    target_ratio = inner_w / inner_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # La fuente es más ancha: recortar laterales
        crop_w = int(src_h * target_ratio)
        x_off = (src_w - crop_w) // 2
        fitted = crop_img.crop((x_off, 0, x_off + crop_w, src_h))
    else:
        # La fuente es más alta: recortar arriba/abajo
        crop_h = int(src_w / target_ratio)
        y_off = (src_h - crop_h) // 2
        fitted = crop_img.crop((0, y_off, src_w, y_off + crop_h))

    fitted_resized = fitted.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    panel.paste(fitted_resized, (1, bar_h + 1))

    return panel

def generate_collage(out_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    # 1. Canvas Base
    img = Image.new("RGBA", (WIDTH, HEIGHT), (7, 12, 22, 255))
    draw = ImageDraw.Draw(img)

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(7 + (14 - 7) * ratio)
        g = int(12 + (22 - 12) * ratio)
        b = int(22 + (38 - 22) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # 2. Resplandores ambientales
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([WIDTH // 2 - 300, 40, WIDTH // 2 + 300, 320], fill=(6, 182, 212, 22))   # Cian arriba
    g_draw.ellipse([50, 280, 550, 620], fill=(168, 85, 247, 24))                             # Púrpura abajo-izq
    g_draw.ellipse([650, 280, 1150, 620], fill=(16, 185, 129, 24))                           # Esmeralda abajo-der
    g_draw.ellipse([20, -20, 350, 160], fill=(56, 189, 248, 25))                             # Azul badge
    glow = glow.filter(ImageFilter.GaussianBlur(65))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 3. Malla blueprint técnica sutil
    grid_color = (18, 28, 48, 255)
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color)

    # 4. Header Bar con Badge de Serie (3/5)
    bx = 42
    by = 20
    bw = 78
    bh = 38
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=9, fill=(10, 18, 32, 220), outline=(56, 189, 248, 180), width=1)
    draw_pulse_waveform(draw, bx + 7, by + 7, 30, 24, color=(56, 189, 248, 90), stroke_width=4)
    draw_pulse_waveform(draw, bx + 7, by + 7, 30, 24, color=(56, 189, 248, 255), stroke_width=2)
    draw.line([(bx + 42, by + 9), (bx + 42, by + bh - 9)], fill=(71, 85, 105, 180), width=1)
    font_badge = get_font(13, bold=True)
    draw.text((bx + 48, by + 10), "3/5", font=font_badge, fill=(244, 114, 182, 240))

    font_stack = get_font(11, bold=True)
    draw.rounded_rectangle([bx + bw + 14, by + 6, bx + bw + 260, by + bh - 6], radius=5, fill=(15, 23, 42, 210), outline=(51, 65, 85, 170), width=1)
    draw.text((bx + bw + 24, by + 9), "COLLAGE: TABLA • KANBAN • CALENDARIO", font=font_stack, fill=(56, 189, 248, 255))

    font_mono = get_font(11, bold=False)
    draw.text((WIDTH - 280, by + 10), "datalaria.com  |  Pulse Cockpit", font=font_mono, fill=(100, 116, 139, 220))

    # 5. Cargar las 3 capturas reales tomadas directamente de la App en vivo
    p_table = r"C:\Users\dalae\.gemini\antigravity\brain\9cc3e8ea-e324-41b5-80e8-6114503cfb4d\live_table_board.png"
    p_kanban = r"C:\Users\dalae\.gemini\antigravity\brain\9cc3e8ea-e324-41b5-80e8-6114503cfb4d\live_kanban_board.png"
    p_cal = r"C:\Users\dalae\.gemini\antigravity\brain\9cc3e8ea-e324-41b5-80e8-6114503cfb4d\live_calendar_board.png"

    raw_table = Image.open(p_table).convert("RGBA")
    raw_kanban = Image.open(p_kanban).convert("RGBA")
    raw_cal = Image.open(p_cal).convert("RGBA")

    # Recortes proporcionales de cada vista auténtica:
    # 1. Tabla Ejecutiva: buscador, filtros y primeras filas de datos
    crop_table = raw_table.crop((0, 30, 1340, 340))

    # 2. Tablero Kanban: las 5 columnas activas con tarjetas distribuidas
    crop_kanban = raw_kanban.crop((0, 0, 1340, 620))

    # 3. Calendario Mensual: navegación Noviembre 2026 y cuadrícula de días con artículos
    crop_cal = raw_cal.crop((0, 0, 1340, 620))

    # Posiciones de las 3 ventanas:
    # Ventana 1: Tabla Ejecutiva (Arriba, ancho completo)
    w1_x, w1_y = 42, 70
    w1_w, w1_h = 1116, 240
    win_table = create_window_box(w1_w, w1_h, "1. Tabla Ejecutiva — Búsqueda, Filtros Taxonómicos, Paginación y Métricas", crop_table, accent_color=(6, 182, 212))

    # Ventana 2: Tablero Kanban (Abajo Izquierda)
    w2_x, w2_y = 42, 325
    w2_w, w2_h = 548, 285
    win_kanban = create_window_box(w2_w, w2_h, "2. Tablero Kanban — 5 Fases del Ciclo de Vida Editorial", crop_kanban, accent_color=(168, 85, 247))

    # Ventana 3: Calendario Editorial (Abajo Derecha)
    w3_x, w3_y = 610, 325
    w3_w, w3_h = 548, 285
    win_cal = create_window_box(w3_w, w3_h, "3. Calendario Mensual — Planificación Cronológica de Lanzamientos", crop_cal, accent_color=(16, 185, 129))

    # Sombras elevadas
    shadows = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadows)

    for px, py, pw, ph in [(w1_x, w1_y, w1_w, w1_h), (w2_x, w2_y, w2_w, w2_h), (w3_x, w3_y, w3_w, w3_h)]:
        s_draw.rounded_rectangle([px - 6, py - 4, px + pw + 6, py + ph + 8], radius=13, fill=(0, 0, 0, 190))

    shadows = shadows.filter(ImageFilter.GaussianBlur(16))
    img = Image.alpha_composite(img, shadows)

    # Pegar ventanas
    img.paste(win_table, (w1_x, w1_y), win_table)
    img.paste(win_kanban, (w2_x, w2_y), win_kanban)
    img.paste(win_cal, (w3_x, w3_y), win_cal)

    final_rgb = img.convert("RGB")
    final_rgb.save(out_path, format="PNG", quality=95)
    print(f"[OK] Guardado Collage v2: {out_path} ({WIDTH}x{HEIGHT})")

if __name__ == "__main__":
    out_es = "content/es/posts/pulse-parte3-tablero-react-tabla-kanban-calendario/cover.png"
    out_en = "content/en/posts/pulse-part3-react-dashboard-table-kanban-calendar/cover.png"
    generate_collage(out_es)
    generate_collage(out_en)
