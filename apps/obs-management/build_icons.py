# -*- coding: utf-8 -*-
"""apps/obs-management/build_icons.py - Generador determinista de iconos PWA Gold para Agentic Radar.

Genera los iconos PWA exigidos por INV-OBS-1 e INV-OBS-6:
- icon.svg (Vectorial)
- icon-192.png (Any)
- icon-512.png (Any)
- icon-maskable-192.png (Maskable, 80% safe zone)
- icon-maskable-512.png (Maskable, 80% safe zone)
- apple-touch-icon.png (180x180)
"""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw

WEB_DIR = Path(__file__).resolve().parent / "web"
ICONS_DIR = WEB_DIR / "icons"

WIDTH_512 = 512
WIDTH_192 = 192
APPLE_TOUCH_180 = 180

# Paleta Executive Data-Dense (design.md)
BG_COLOR = (11, 15, 23)        # #0b0f17
SURFACE_COLOR = (17, 24, 39)   # #111827
ACCENT_CYAN = (14, 165, 233)    # #0ea5e9
ACCENT_PURPLE = (139, 92, 246)  # #8b5cf6
ACCENT_EMERALD = (16, 185, 129) # #10b981
ACCENT_AMBER = (245, 158, 11)   # #f59e0b
TEXT_WHITE = (248, 250, 252)    # #f8fafc


def draw_radar_emblem(draw: ImageDraw.ImageDraw, size: int, scale: float = 1.0) -> None:
    """Dibuja el emblema de antena/barrido de radar con retícula concéntrica y nodos."""
    cx = size / 2.0
    cy = size / 2.0

    def s(norm_len: float) -> float:
        return norm_len * size * scale

    # 1. Anillos concéntricos de radar
    r_outer = s(0.42)
    r_mid = s(0.28)
    r_inner = s(0.14)

    # Anillo exterior
    draw.ellipse(
        [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer],
        outline=(30, 41, 59),
        width=max(2, int(s(0.018))),
    )
    # Anillo intermedio
    draw.ellipse(
        [cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid],
        outline=(51, 65, 85),
        width=max(1, int(s(0.014))),
    )
    # Anillo interior
    draw.ellipse(
        [cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner],
        outline=ACCENT_CYAN,
        width=max(2, int(s(0.016))),
    )

    # 2. Retícula cartesiana (ejes X e Y sutiles)
    line_w = max(1, int(s(0.01)))
    draw.line([cx - r_outer, cy, cx + r_outer, cy], fill=(30, 41, 59), width=line_w)
    draw.line([cx, cy - r_outer, cx, cy + r_outer], fill=(30, 41, 59), width=line_w)

    # 3. Haz de barrido radial de 45 grados (sector iluminado)
    # Dibujamos líneas angulares para simular el degradado del barrido de radar
    num_rays = 24
    start_angle = -55
    sweep_span = 45
    for i in range(num_rays):
        t = i / num_rays
        angle_deg = start_angle + t * sweep_span
        angle_rad = math.radians(angle_deg)
        rx = cx + math.cos(angle_rad) * r_outer
        ry = cy + math.sin(angle_rad) * r_outer
        alpha_val = int(40 + 180 * t)
        # Mezclamos con cian/violeta según el avance
        beam_color = (
            int(ACCENT_CYAN[0] * (1 - t * 0.4) + ACCENT_PURPLE[0] * (t * 0.4)),
            int(ACCENT_CYAN[1] * (1 - t * 0.4) + ACCENT_PURPLE[1] * (t * 0.4)),
            int(ACCENT_CYAN[2] * (1 - t * 0.4) + ACCENT_PURPLE[2] * (t * 0.4)),
        )
        draw.line([cx, cy, rx, ry], fill=beam_color, width=max(1, int(s(0.012))))

    # 4. Línea de barrido principal brillante
    lead_rad = math.radians(start_angle + sweep_span)
    lead_x = cx + math.cos(lead_rad) * r_outer
    lead_y = cy + math.sin(lead_rad) * r_outer
    draw.line([cx, cy, lead_x, lead_y], fill=TEXT_WHITE, width=max(2, int(s(0.02))))

    # 5. Nodos objetivo detectados (blips de obsolescencia / alerta)
    # Blip 1: Crítico (Ámbar / Naranja) en anillo medio
    b1_rad = math.radians(-30)
    b1_x = cx + math.cos(b1_rad) * (r_mid * 0.95)
    b1_y = cy + math.sin(b1_rad) * (r_mid * 0.95)
    b1_r = s(0.038)
    draw.ellipse([b1_x - b1_r, b1_y - b1_r, b1_x + b1_r, b1_y + b1_r], fill=ACCENT_AMBER)
    draw.ellipse(
        [b1_x - b1_r * 1.8, b1_y - b1_r * 1.8, b1_x + b1_r * 1.8, b1_y + b1_r * 1.8],
        outline=(245, 158, 11),
        width=max(1, int(s(0.008))),
    )

    # Blip 2: Resuelto (Esmeralda) en cuadrante inferior izquierdo
    b2_rad = math.radians(135)
    b2_x = cx + math.cos(b2_rad) * (r_mid * 0.7)
    b2_y = cy + math.sin(b2_rad) * (r_mid * 0.7)
    b2_r = s(0.028)
    draw.ellipse([b2_x - b2_r, b2_y - b2_r, b2_x + b2_r, b2_y + b2_r], fill=ACCENT_EMERALD)

    # 6. Emisor / Transceptor central
    center_r = s(0.045)
    draw.ellipse(
        [cx - center_r, cy - center_r, cx + center_r, cy + center_r],
        fill=ACCENT_CYAN,
    )
    core_r = s(0.02)
    draw.ellipse(
        [cx - core_r, cy - core_r, cx + core_r, cy + core_r],
        fill=TEXT_WHITE,
    )


def generate_png_icons() -> None:
    """Genera los iconos PNG any, maskable y Apple Touch."""
    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Any icons (scale = 0.88, esquinas sutilmente suavizadas sobre fondo oscuro)
    for width, filename in [(WIDTH_512, "icon-512.png"), (WIDTH_192, "icon-192.png")]:
        img = Image.new("RGBA", (width, width), BG_COLOR + (255,))
        draw = ImageDraw.Draw(img)
        # Círculo contenedor sutil
        draw.ellipse([width * 0.04, width * 0.04, width * 0.96, width * 0.96], fill=SURFACE_COLOR)
        draw_radar_emblem(draw, width, scale=0.86)
        img.save(ICONS_DIR / filename, format="PNG", optimize=True)
        print(f"Generado: {ICONS_DIR / filename} ({width}x{width})")

    # 2. Maskable icons (scale = 0.68, safe zone central estricta <= 80%)
    for width, filename in [(WIDTH_512, "icon-maskable-512.png"), (WIDTH_192, "icon-maskable-192.png")]:
        img = Image.new("RGBA", (width, width), BG_COLOR + (255,))
        draw = ImageDraw.Draw(img)
        draw_radar_emblem(draw, width, scale=0.68)
        img.save(ICONS_DIR / filename, format="PNG", optimize=True)
        print(f"Generado (maskable): {ICONS_DIR / filename} ({width}x{width})")

    # 3. Apple Touch Icon (180x180, en web/)
    img_apple = Image.new("RGBA", (APPLE_TOUCH_180, APPLE_TOUCH_180), BG_COLOR + (255,))
    draw_apple = ImageDraw.Draw(img_apple)
    draw_apple.ellipse(
        [APPLE_TOUCH_180 * 0.04, APPLE_TOUCH_180 * 0.04, APPLE_TOUCH_180 * 0.96, APPLE_TOUCH_180 * 0.96],
        fill=SURFACE_COLOR,
    )
    draw_radar_emblem(draw_apple, APPLE_TOUCH_180, scale=0.82)
    img_apple.save(WEB_DIR / "apple-touch-icon.png", format="PNG", optimize=True)
    print(f"Generado: {WEB_DIR / 'apple-touch-icon.png'} (180x180)")


def generate_svg_icon() -> None:
    """Genera icon.svg vectorial para resoluciones infinitas."""
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" rx="96" fill="#0b0f17" />
  <circle cx="256" cy="256" r="236" fill="#111827" />
  
  <!-- Anillos concéntricos -->
  <circle cx="256" cy="256" r="192" fill="none" stroke="#1e293b" stroke-width="6" />
  <circle cx="256" cy="256" r="128" fill="none" stroke="#334155" stroke-width="4" />
  <circle cx="256" cy="256" r="64" fill="none" stroke="#0ea5e9" stroke-width="4" opacity="0.8" />
  
  <!-- Retícula de ejes -->
  <line x1="64" y1="256" x2="448" y2="256" stroke="#1e293b" stroke-width="3" />
  <line x1="256" y1="64" x2="256" y2="448" stroke="#1e293b" stroke-width="3" />
  
  <!-- Haz de barrido degradado -->
  <defs>
    <linearGradient id="sweepGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0ea5e9" stop-opacity="0.1" />
      <stop offset="70%" stop-color="#0ea5e9" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.85" />
    </linearGradient>
  </defs>
  <path d="M 256 256 L 391 120 A 192 192 0 0 0 256 64 Z" fill="url(#sweepGrad)" />
  <line x1="256" y1="256" x2="391" y2="120" stroke="#f8fafc" stroke-width="5" stroke-linecap="round" />
  
  <!-- Blips de objetivos -->
  <!-- Blip 1: Alerta Crítica (Ámbar) -->
  <circle cx="365" cy="190" r="14" fill="#f59e0b" />
  <circle cx="365" cy="190" r="24" fill="none" stroke="#f59e0b" stroke-width="3" opacity="0.75" />
  
  <!-- Blip 2: Resuelto / Seguro (Esmeralda) -->
  <circle cx="165" cy="345" r="10" fill="#10b981" />
  
  <!-- Transceptor central -->
  <circle cx="256" cy="256" r="18" fill="#0ea5e9" />
  <circle cx="256" cy="256" r="8" fill="#ffffff" />
</svg>
"""
    (WEB_DIR / "icon.svg").write_text(svg_content, encoding="utf-8")
    print(f"Generado: {WEB_DIR / 'icon.svg'}")


if __name__ == "__main__":
    generate_png_icons()
    generate_svg_icon()
    print("OK: Generación de iconos PWA completada.")
