# -*- coding: utf-8 -*-
"""build_icons.py - Generador de iconos PWA Gold (any, maskable, Apple Touch) para Weather Intelligence."""

import math
from pathlib import Path
from PIL import Image, ImageDraw

BASE_DIR = Path(__file__).resolve().parent

WIDTH_512 = 512
WIDTH_192 = 192
APPLE_TOUCH_180 = 180

# Colores PWA
BG_COLOR = (11, 15, 23)        # #0b0f17
SURFACE_COLOR = (17, 24, 39)   # #111827
ACCENT_CYAN = (14, 165, 233)    # #0ea5e9
ACCENT_PURPLE = (139, 92, 246)  # #8b5cf6
ACCENT_AMBER = (245, 158, 11)   # #f59e0b


def _draw_weather_emblem(draw: ImageDraw.ImageDraw, size: int, scale: float = 1.0) -> None:
    """Dibuja el emblema solar + nube + onda armónica escalado respecto al centro."""
    cx = size / 2.0
    cy = size / 2.0

    def px(norm_x: float) -> float:
        return cx + (norm_x - 0.5) * size * scale

    def py(norm_y: float) -> float:
        return cy + (norm_y - 0.5) * size * scale

    def s(norm_len: float) -> float:
        return norm_len * size * scale

    # Sol dorado
    sun_x, sun_y, sun_r = px(0.62), py(0.37), s(0.155)
    draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=ACCENT_AMBER)

    # Halo / lóbulos cian de la nube
    c_y = py(0.57)
    c_x1, c_x2, c_x3 = px(0.33), px(0.51), px(0.68)
    r1, r2, r3 = s(0.135), s(0.185), s(0.125)

    draw.ellipse([c_x1 - r1, c_y - r1, c_x1 + r1, c_y + r1], fill=ACCENT_CYAN)
    draw.ellipse([c_x3 - r3, c_y - r3, c_x3 + r3, c_y + r3], fill=ACCENT_CYAN)
    draw.rounded_rectangle(
        [c_x1 - r1 * 0.45, c_y - r1 * 0.2, c_x3 + r3 * 0.45, c_y + r1],
        radius=max(2, int(r1 * 0.65)),
        fill=ACCENT_CYAN,
    )
    draw.ellipse([c_x2 - r2, c_y - r2 * 1.25, c_x2 + r2, c_y + r2 * 0.72], fill=(240, 249, 255))
    draw.rounded_rectangle(
        [c_x1 - r1 * 0.35, c_y - r1 * 0.1, c_x3 + r3 * 0.35, c_y + r1 * 0.92],
        radius=max(2, int(r1 * 0.6)),
        fill=(224, 242, 254),
    )

    # Curva sinusoidal de Fourier al pie
    w_start = px(0.24)
    w_end = px(0.76)
    w_base = py(0.79)
    amp = s(0.036)
    steps = max(24, int(w_end - w_start))
    wave_pts = []
    for i in range(steps + 1):
        frac = i / steps
        x = w_start + frac * (w_end - w_start)
        y = w_base + math.sin(frac * 2.0 * math.pi) * amp
        wave_pts.append((x, y))
    draw.line(wave_pts, fill=ACCENT_PURPLE, width=max(3, int(s(0.03))))


def create_icon(size: int) -> Image.Image:
    """Icono estándar con marco redondeado ('any')."""
    img = Image.new("RGBA", (size, size), (*BG_COLOR, 255))
    draw = ImageDraw.Draw(img)
    pad = int(size * 0.08)
    draw.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=int(size * 0.22),
        fill=(*SURFACE_COLOR, 255),
        outline=ACCENT_CYAN,
        width=max(2, int(size * 0.02)),
    )
    _draw_weather_emblem(draw, size, scale=0.88)
    return img


def create_maskable_icon(size: int) -> Image.Image:
    """Icono maskable PWA sin recorte en zona segura del 80% central y fondo sólido."""
    img = Image.new("RGBA", (size, size), (*BG_COLOR, 255))
    draw = ImageDraw.Draw(img)
    pad = int(size * 0.06)
    draw.rectangle([0, 0, size, size], fill=(*SURFACE_COLOR, 255))
    draw.ellipse([pad, pad, size - pad, size - pad], fill=(*BG_COLOR, 255))
    _draw_weather_emblem(draw, size, scale=0.68)
    return img


def create_apple_touch_icon(size: int = APPLE_TOUCH_180) -> Image.Image:
    """Icono opaco 180x180 para iOS Safari (sin alfa transparente)."""
    img = Image.new("RGB", (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)
    _draw_weather_emblem(draw, size, scale=0.84)
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
    img512 = create_icon(WIDTH_512)
    img192 = create_icon(WIDTH_192)
    mask512 = create_maskable_icon(WIDTH_512)
    mask192 = create_maskable_icon(WIDTH_192)
    apple180 = create_apple_touch_icon(APPLE_TOUCH_180)

    svg_content = create_svg_icon()

    destinations = [
        BASE_DIR,
        BASE_DIR.parent.parent / "static" / "apps" / "weather"
    ]

    for d in destinations:
        d.mkdir(parents=True, exist_ok=True)
        img512.save(d / "icon-512.png", format="PNG")
        img192.save(d / "icon-192.png", format="PNG")
        mask512.save(d / "icon-maskable-512.png", format="PNG")
        mask192.save(d / "icon-maskable-192.png", format="PNG")
        apple180.save(d / "apple-touch-icon.png", format="PNG")
        with open(d / "icon.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Iconos PWA generados en {d}")


if __name__ == "__main__":
    main()
