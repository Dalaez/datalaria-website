#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_pulse_badge.py
====================
Compone sutilmente el icono de Pulse (onda ECG azul) en la esquina superior izquierda
de las ilustraciones 3D oficiales de la serie editorial Datalaria Pulse (1/5 a 5/5).
"""

import os
from PIL import Image, ImageDraw, ImageFont

def draw_pulse_waveform(draw, x: float, y: float, w: float, h: float, color=(56, 189, 248), stroke_width=2):
    """Dibuja la onda exacta de Datalaria Pulse."""
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
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def process_cover(source_img_path: str, out_path: str, part_num: int = 1, target_size=(1200, 630)):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    im = Image.open(source_img_path).convert("RGBA")
    
    # 1. Recorte y ajuste al aspect ratio 1200x630 (1.91:1) manteniendo el centro
    src_w, src_h = im.size
    target_w, target_h = target_size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        x_offset = (src_w - new_w) // 2
        im = im.crop((x_offset, 0, x_offset + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        y_offset = (src_h - new_h) // 2
        im = im.crop((0, y_offset, src_w, y_offset + new_h))

    im = im.resize(target_size, Image.Resampling.LANCZOS)

    # 2. Capa de badge superior izquierda
    overlay = Image.new("RGBA", target_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    bx = 42
    by = 38
    bw = 78
    bh = 38

    # Fondo frosted glass oscuro con borde cian
    draw.rounded_rectangle(
        [bx, by, bx + bw, by + bh],
        radius=9,
        fill=(10, 18, 32, 215),
        outline=(56, 189, 248, 170),
        width=1
    )

    # Dibujar la onda de pulso en azul cian con brillo
    icon_w = 30
    icon_h = 24
    ix = bx + 7
    iy = by + (bh - icon_h) // 2
    # Glow sutil
    draw_pulse_waveform(draw, ix, iy, icon_w, icon_h, color=(56, 189, 248, 90), stroke_width=4)
    # Línea nítida
    draw_pulse_waveform(draw, ix, iy, icon_w, icon_h, color=(56, 189, 248, 255), stroke_width=2)

    # Separador vertical fino
    draw.line([(bx + 42, by + 9), (bx + 42, by + bh - 9)], fill=(71, 85, 105, 180), width=1)

    # Indicador de serie (ej: 1/5, 2/5...)
    font_num = get_font(13, bold=True)
    draw.text((bx + 48, by + 10), f"{part_num}/5", font=font_num, fill=(244, 114, 182, 240))

    final_img = Image.alpha_composite(im, overlay).convert("RGB")
    final_img.save(out_path, format="PNG", quality=95)
    print(f"[OK] Guardado: {out_path} ({target_w}x{target_h}) [Part {part_num}/5]")

if __name__ == "__main__":
    # Post 1
    src1 = "C:/Users/dalae/.gemini/antigravity/brain/9cc3e8ea-e324-41b5-80e8-6114503cfb4d/datalaria_pulse_migration_cover_v2_1793348082394.jpg"
    process_cover(src1, "content/es/posts/pulse-parte1-adios-notion-content-ops/cover.png", part_num=1)
    process_cover(src1, "content/en/posts/pulse-part1-goodbye-notion-content-ops/cover.png", part_num=1)

    # Post 2
    src2 = "C:/Users/dalae/.gemini/antigravity/brain/9cc3e8ea-e324-41b5-80e8-6114503cfb4d/pydantic_bilingual_cicd_cover_1793356756214.jpg"
    process_cover(src2, "content/es/posts/pulse-parte2-indexador-pydantic-paridad-ci/cover.png", part_num=2)
    process_cover(src2, "content/en/posts/pulse-part2-pydantic-indexer-bilingual-parity-ci/cover.png", part_num=2)
