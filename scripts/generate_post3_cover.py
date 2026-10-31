#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_post3_cover.py
=======================
Genera la portada del Post 3 de Datalaria Pulse como un mix de la UI real
del dashboard en React 19 y el entorno de diseño corporativo Dark Slate.
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

def create_ui_mix_cover(screenshot_path: str, out_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    # 1. Canvas Base con gradiente
    img = Image.new("RGBA", (WIDTH, HEIGHT), (7, 12, 22, 255))
    draw = ImageDraw.Draw(img)

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(7 + (15 - 7) * ratio)
        g = int(12 + (23 - 12) * ratio)
        b = int(22 + (42 - 22) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # 2. Resplandores ambientales
    glow_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_overlay)
    g_draw.ellipse([50, -50, 450, 250], fill=(6, 182, 212, 28))
    g_draw.ellipse([WIDTH - 500, HEIGHT - 350, WIDTH + 100, HEIGHT + 100], fill=(16, 185, 129, 25))
    g_draw.ellipse([WIDTH // 2 - 250, HEIGHT // 2 - 150, WIDTH // 2 + 250, HEIGHT // 2 + 200], fill=(56, 189, 248, 16))
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(65))
    img = Image.alpha_composite(img, glow_overlay)
    draw = ImageDraw.Draw(img)

    # 3. Malla blueprint sutil
    grid_color = (18, 28, 48, 255)
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color)

    # 4. Badge Superior Izquierda (Serie 3/5 con icono de pulso)
    bx = 42
    by = 24
    bw = 78
    bh = 38
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=9, fill=(10, 18, 32, 220), outline=(56, 189, 248, 180), width=1)
    
    # Onda de pulso
    draw_pulse_waveform(draw, bx + 7, by + 7, 30, 24, color=(56, 189, 248, 90), stroke_width=4)
    draw_pulse_waveform(draw, bx + 7, by + 7, 30, 24, color=(56, 189, 248, 255), stroke_width=2)
    # Separador
    draw.line([(bx + 42, by + 9), (bx + 42, by + bh - 9)], fill=(71, 85, 105, 180), width=1)
    # 3/5
    font_badge = get_font(13, bold=True)
    draw.text((bx + 48, by + 10), "3/5", font=font_badge, fill=(244, 114, 182, 240))

    # Tag descriptivo del stack al lado
    font_stack = get_font(11, bold=True)
    draw.rounded_rectangle([bx + bw + 14, by + 6, bx + bw + 225, by + bh - 6], radius=5, fill=(15, 23, 42, 200), outline=(51, 65, 85, 160), width=1)
    draw.text((bx + bw + 24, by + 9), "REACT 19 • TABLA & KANBAN", font=font_stack, fill=(56, 189, 248, 240))

    # Watermark corporativo a la derecha
    font_mono = get_font(11, bold=False)
    draw.text((WIDTH - 280, by + 10), "datalaria.com  |  Pulse Cockpit", font=font_mono, fill=(100, 116, 139, 220))

    # 5. Ventana Flotante del Dashboard de la App (Hero Element)
    win_x = 50
    win_y = 76
    win_w = WIDTH - 100
    win_h = HEIGHT - win_y - 24

    bar_h = 28

    # Sombra profunda elevada
    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([win_x - 8, win_y - 6, win_x + win_w + 8, win_y + win_h + 12], radius=16, fill=(0, 0, 0, 220))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, shadow)

    # Contenedor de la ventana
    window_img = Image.new("RGBA", (win_w, win_h), (11, 17, 32, 255))
    w_draw = ImageDraw.Draw(window_img)

    # Borde y barra superior
    w_draw.rounded_rectangle([0, 0, win_w, win_h], radius=12, fill=(11, 17, 32, 255), outline=(56, 189, 248, 140), width=1)
    w_draw.rectangle([0, bar_h, win_w, win_h], fill=(13, 20, 36, 255))

    # Dots tipo Mac
    w_draw.ellipse([14, 8, 24, 18], fill=(239, 68, 68, 240))
    w_draw.ellipse([30, 8, 40, 18], fill=(234, 179, 8, 240))
    w_draw.ellipse([46, 8, 56, 18], fill=(34, 197, 94, 240))

    # Título de ventana / URL
    font_url = get_font(11, bold=True)
    w_draw.text((70, 7), "datalaria.com/apps/pulse  —  Content Ops as Code Cockpit (Zero-Latency SPA)", font=font_url, fill=(148, 163, 184, 220))

    # Pegar screenshot de la UI
    if os.path.exists(screenshot_path):
        raw_ss = Image.open(screenshot_path).convert("RGBA")
        inner_w = win_w - 2
        inner_h = win_h - bar_h - 2
        # Escalar manteniendo proporción y encajando
        ss_resized = raw_ss.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
        window_img.paste(ss_resized, (1, bar_h + 1))

    # Pegar ventana en el lienzo
    img.paste(window_img, (win_x, win_y), window_img)

    final_rgb = img.convert("RGB")
    final_rgb.save(out_path, format="PNG", quality=95)
    print(f"[OK] Guardado Cover UI Mix: {out_path} ({WIDTH}x{HEIGHT})")

if __name__ == "__main__":
    ss = r"C:\Users\dalae\.gemini\antigravity\brain\9cc3e8ea-e324-41b5-80e8-6114503cfb4d\.user_uploaded\media_1793284012362_f265b19a.png"
    out_es = "content/es/posts/pulse-parte3-tablero-react-tabla-kanban-calendario/cover.png"
    out_en = "content/en/posts/pulse-part3-react-dashboard-table-kanban-calendar/cover.png"
    create_ui_mix_cover(ss, out_es)
    create_ui_mix_cover(ss, out_en)
