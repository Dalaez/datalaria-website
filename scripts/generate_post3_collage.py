#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_post3_collage.py
=========================
Genera la portada oficial del Post 3 de Datalaria Pulse como un COLLAGE
de las 3 vistas canónicas desarrolladas en la App:
1. Tabla Ejecutiva (Filtros, Paginación, Scoring SEO y Tráfico)
2. Tablero Kanban (5 Columnas de Ciclo de Vida Editorial)
3. Calendario Editorial (Planificación Cronológica y Releases)

Mantiene la identidad de serie:
- Esquina superior izquierda: Badge con icono de pulso azul (ECG wave) y '3/5'.
- Estética Dark Slate ejecutiva con resplandores neón y ventanas macOS elevadas.
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

def create_window_panel(width: int, height: int, title: str, crop_img: Image.Image, accent_color=(56, 189, 248)) -> Image.Image:
    """Crea una ventana macOS estilizada con título, dots y captura interior."""
    panel = Image.new("RGBA", (width, height), (11, 17, 32, 255))
    draw = ImageDraw.Draw(panel)
    bar_h = 26

    # Borde exterior con acento sutil
    draw.rounded_rectangle([0, 0, width, height], radius=10, fill=(11, 17, 32, 255), outline=(accent_color[0], accent_color[1], accent_color[2], 160), width=1)
    # Barra de ventana
    draw.rectangle([0, bar_h, width, height], fill=(13, 20, 36, 255))

    # Dots Mac
    draw.ellipse([12, 7, 21, 16], fill=(239, 68, 68, 240))
    draw.ellipse([27, 7, 36, 16], fill=(234, 179, 8, 240))
    draw.ellipse([42, 7, 51, 16], fill=(34, 197, 94, 240))

    # Título de ventana
    font_title = get_font(11, bold=True)
    draw.text((62, 6), title, font=font_title, fill=(226, 232, 240, 240))

    # Ajustar e insertar captura
    inner_w = width - 2
    inner_h = height - bar_h - 2
    ss_resized = crop_img.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    panel.paste(ss_resized, (1, bar_h + 1))

    return panel

def create_collage_cover(out_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    # 1. Canvas Base con gradiente
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
    g_draw.ellipse([20, 100, 500, 600], fill=(6, 182, 212, 24))     # Cian en la tabla
    g_draw.ellipse([700, 50, 1180, 400], fill=(168, 85, 247, 22))   # Púrpura en Kanban
    g_draw.ellipse([700, 320, 1180, 620], fill=(16, 185, 129, 22))  # Esmeralda en Calendario
    g_draw.ellipse([20, -20, 350, 160], fill=(56, 189, 248, 25))    # Azul en badge
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
    by = 22
    bw = 78
    bh = 38
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=9, fill=(10, 18, 32, 220), outline=(56, 189, 248, 180), width=1)
    draw_pulse_waveform(draw, bx + 7, by + 7, 30, 24, color=(56, 189, 248, 90), stroke_width=4)
    draw_pulse_waveform(draw, bx + 7, by + 7, 30, 24, color=(56, 189, 248, 255), stroke_width=2)
    draw.line([(bx + 42, by + 9), (bx + 42, by + bh - 9)], fill=(71, 85, 105, 180), width=1)
    font_badge = get_font(13, bold=True)
    draw.text((bx + 48, by + 10), "3/5", font=font_badge, fill=(244, 114, 182, 240))

    # Píldora de descripción del collage
    font_stack = get_font(11, bold=True)
    draw.rounded_rectangle([bx + bw + 14, by + 6, bx + bw + 260, by + bh - 6], radius=5, fill=(15, 23, 42, 210), outline=(51, 65, 85, 170), width=1)
    draw.text((bx + bw + 24, by + 9), "COLLAGE: TABLA • KANBAN • CALENDARIO", font=font_stack, fill=(56, 189, 248, 255))

    font_mono = get_font(11, bold=False)
    draw.text((WIDTH - 280, by + 10), "datalaria.com  |  Pulse Cockpit", font=font_mono, fill=(100, 116, 139, 220))

    # 5. Cargar las 3 capturas reales
    p_table = r"C:\Users\dalae\.gemini\antigravity\brain\9cc3e8ea-e324-41b5-80e8-6114503cfb4d\.user_uploaded\media_1793196910899_66def5c2.png"
    p_kanban = r"C:\Users\dalae\.gemini\antigravity\brain\9cc3e8ea-e324-41b5-80e8-6114503cfb4d\.user_uploaded\media_1793197363747_f94d7be2.png"
    p_cal = r"C:\Users\dalae\.gemini\antigravity\brain\9cc3e8ea-e324-41b5-80e8-6114503cfb4d\.user_uploaded\media_1793197478486_39f47fd1.png"

    raw_table = Image.open(p_table).convert("RGBA")
    raw_kanban = Image.open(p_kanban).convert("RGBA")
    raw_cal = Image.open(p_cal).convert("RGBA")

    # Recortes precisos de contenido
    # Tabla: desde barra de búsqueda hasta filas
    crop_table = raw_table.crop((40, 340, 984, 578))

    # Kanban: columnas
    crop_kanban = raw_kanban.crop((30, 75, 994, 520))

    # Calendario: lista de publicaciones cronológicas
    crop_cal = raw_cal.crop((30, 70, 994, 490))

    # Dimensiones y posiciones del Collage
    # Panel 1: Tabla Ejecutiva (Izquierda, altura completa)
    p1_x, p1_y = 42, 74
    p1_w, p1_h = 665, 532
    win_table = create_window_panel(p1_w, p1_h, "Tabla Ejecutiva — Filtros, Paginación & Scoring SEO", crop_table, accent_color=(6, 182, 212))

    # Panel 2: Tablero Kanban (Derecha Superior)
    p2_x, p2_y = 722, 74
    p2_w, p2_h = 436, 256
    win_kanban = create_window_panel(p2_w, p2_h, "Tablero Kanban — 5 Estados del Ciclo Editorial", crop_kanban, accent_color=(168, 85, 247))

    # Panel 3: Calendario Editorial (Derecha Inferior)
    p3_x, p3_y = 722, 350
    p3_w, p3_h = 436, 256
    win_cal = create_window_panel(p3_w, p3_h, "Calendario Editorial — Planificación Cronológica", crop_cal, accent_color=(16, 185, 129))

    # 6. Sombras elevadas para las 3 ventanas
    shadows = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadows)

    for px, py, pw, ph in [(p1_x, p1_y, p1_w, p1_h), (p2_x, p2_y, p2_w, p2_h), (p3_x, p3_y, p3_w, p3_h)]:
        s_draw.rounded_rectangle([px - 6, py - 4, px + pw + 6, py + ph + 8], radius=14, fill=(0, 0, 0, 190))

    shadows = shadows.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img, shadows)

    # 7. Pegar las ventanas en el lienzo
    img.paste(win_table, (p1_x, p1_y), win_table)
    img.paste(win_kanban, (p2_x, p2_y), win_kanban)
    img.paste(win_cal, (p3_x, p3_y), win_cal)

    final_rgb = img.convert("RGB")
    final_rgb.save(out_path, format="PNG", quality=95)
    print(f"[OK] Guardado Collage Cover: {out_path} ({WIDTH}x{HEIGHT})")

if __name__ == "__main__":
    out_es = "content/es/posts/pulse-parte3-tablero-react-tabla-kanban-calendario/cover.png"
    out_en = "content/en/posts/pulse-part3-react-dashboard-table-kanban-calendar/cover.png"
    create_collage_cover(out_es)
    create_collage_cover(out_en)
