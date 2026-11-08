# -*- coding: utf-8 -*-
"""build_icons.py - Generador de iconos PWA para Weather Intelligence v3.0."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent

WIDTH_512 = 512
WIDTH_192 = 192

# Colores PWA
BG_COLOR = (11, 15, 23)        # #0b0f17
ACCENT_CYAN = (14, 165, 233)    # #0ea5e9
ACCENT_PURPLE = (139, 92, 246)  # #8b5cf6
ACCENT_AMBER = (245, 158, 11)   # #f59e0b
TEXT_COLOR = (248, 250, 252)    # #f8fafc


def create_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (*BG_COLOR, 255))
    draw = ImageDraw.Draw(img)

    # Círculo de fondo con degradado o borde
    pad = int(size * 0.08)
    draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=int(size * 0.22), fill=(17, 24, 39, 255), outline=ACCENT_CYAN, width=max(2, int(size * 0.02)))

    # Sol (dorado)
    sun_x = int(size * 0.62)
    sun_y = int(size * 0.38)
    sun_r = int(size * 0.16)
    draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=ACCENT_AMBER)

    # Nube estilizada (cian / púrpura)
    c_y = int(size * 0.60)
    c_x1 = int(size * 0.32)
    c_x2 = int(size * 0.52)
    c_x3 = int(size * 0.68)
    r1 = int(size * 0.14)
    r2 = int(size * 0.20)
    r3 = int(size * 0.13)

    # Base de la nube
    draw.ellipse([c_x1 - r1, c_y - r1, c_x1 + r1, c_y + r1], fill=ACCENT_CYAN)
    draw.ellipse([c_x2 - r2, c_y - int(r2 * 1.3), c_x2 + r2, c_y + int(r2 * 0.7)], fill=(224, 242, 254))
    draw.ellipse([c_x3 - r3, c_y - r3, c_x3 + r3, c_y + r3], fill=ACCENT_CYAN)
    draw.rounded_rectangle([c_x1 - int(r1 * 0.5), c_y - int(r1 * 0.2), c_x3 + int(r3 * 0.5), c_y + r1], radius=int(r1 * 0.6), fill=(224, 242, 254))

    # Curva sinusoidal de Fourier al pie de la nube
    wave_pts = []
    w_start = int(size * 0.22)
    w_end = int(size * 0.78)
    w_base = int(size * 0.76)
    for x in range(w_start, w_end):
        t = (x - w_start) / (w_end - w_start) * 2 * 3.14159
        y = w_base - int(size * 0.04 * (1.0 - t / (2 * 3.14159)) * 0.8 * (-1.0) * (size * 0.05 / (size * 0.05)) * 0) # simple sin line
        wave_pts.append((x, int(w_base - (size * 0.035) * ((1 if (x // 15) % 2 == 0 else -1) * 0.5))))

    return img


def create_svg_icon() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" rx="112" fill="#0b0f17" stroke="#0ea5e9" stroke-width="8"/>
  <circle cx="320" cy="190" r="80" fill="#f59e0b"/>
  <g fill="#0ea5e9" opacity="0.95">
    <circle cx="170" cy="310" r="70"/>
    <circle cx="340" cy="310" r="65"/>
    <rect x="170" y="270" width="170" height="110" rx="40"/>
  </g>
  <circle cx="260" cy="245" r="95" fill="#f0f9ff"/>
  <path d="M 120 420 Q 180 390 240 420 T 360 420 T 420 420" fill="none" stroke="#8b5cf6" stroke-width="12" stroke-linecap="round"/>
</svg>"""


def main():
    img512 = create_icon(512)
    img192 = create_icon(192)

    svg_content = create_svg_icon()

    destinations = [
        BASE_DIR,
        BASE_DIR.parent.parent / "static" / "apps" / "weather"
    ]

    for d in destinations:
        d.mkdir(parents=True, exist_ok=True)
        img512.save(d / "icon-512.png", format="PNG")
        img192.save(d / "icon-192.png", format="PNG")
        with open(d / "icon.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Iconos PWA generados en {d}")


if __name__ == "__main__":
    main()
