# apps/snake/build_icons.py
# Generador determinista de iconos rasterizados PWA para Neon Snake v2.0.0
# Datalaria Helix — Strict Offline Resilience (INV-SNAKE-8)

import math
from pathlib import Path
from PIL import Image, ImageDraw

APP_DIR = Path(__file__).resolve().parent

def draw_snake_icon(size: int, maskable: bool = False) -> Image.Image:
    # 1. Crear lienzo RGBA
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # Gradiente de fondo Cyberpunk (#05070d -> #0b1224 -> #120820)
    grad = Image.new("RGBA", (size, size))
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            r = int(5 * (1 - t) + 18 * t)
            g = int(7 * (1 - t) + 8 * t)
            b = int(13 * (1 - t) + 32 * t)
            grad.putpixel((x, y), (r, g, b, 255))

    # Máscara de esquinas redondeadas si no es maskable
    if not maskable:
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        corner_r = int(size * 0.22)
        mask_draw.rounded_rectangle([0, 0, size, size], radius=corner_r, fill=255)
        img.paste(grad, (0, 0), mask)
    else:
        # Maskable: fondo al 100% para la safe zone de Android
        img.paste(grad, (0, 0))

    # Factor de escala (si es maskable, 80% safe-zone)
    scale = (size / 512.0) * (0.80 if maskable else 0.95)
    cx, cy = size / 2, size / 2

    draw = ImageDraw.Draw(img)

    # Rejilla cibernética sutil
    grid_step = max(16, int(64 * scale))
    grid_color = (0, 240, 255, 30)
    for gx in range(0, size, grid_step):
        draw.line([(gx, 0), (gx, size)], fill=grid_color, width=1)
    for gy in range(0, size, grid_step):
        draw.line([(0, gy), (size, gy)], fill=grid_color, width=1)

    # Borde cuadrante neón
    b_margin = int(24 * scale)
    b_radius = int(85 * scale)
    b_color = (0, 240, 255, 75)
    draw.rounded_rectangle(
        [b_margin, b_margin, size - b_margin, size - b_margin],
        radius=b_radius,
        outline=b_color,
        width=int(2.5 * scale)
    )

    # Puntos de la serpiente (Curva S)
    pts = [
        (int(cx - 130 * scale), int(cy + 120 * scale)),
        (int(cx - 90 * scale), int(cy + 60 * scale)),
        (int(cx - 40 * scale), int(cy + 10 * scale)),
        (int(cx + 10 * scale), int(cy - 40 * scale)),
        (int(cx + 60 * scale), int(cy - 90 * scale)),
        (int(cx + 120 * scale), int(cy - 40 * scale))
    ]

    # Dibujar cuerpo de la serpiente con círculos interpolados
    num_steps = 60
    for i in range(num_steps):
        t = i / (num_steps - 1)
        # Bezier o spline simple
        # Curva de 3 puntos
        p0 = pts[0]
        p1 = (cx, cy)
        p2 = pts[-1]
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * (cy - 60 * scale) + t**2 * p2[1]

        # Color interpolado de magenta (#ff007a) a cian (#00f0ff)
        cr = int(255 * (1 - t) + 0 * t)
        cg = int(0 * (1 - t) + 240 * t)
        cb = int(122 * (1 - t) + 255 * t)
        r = int((16 + 8 * t) * scale)

        draw.ellipse([x - r, y - r, x + r, y + r], fill=(cr, cg, cb, 230))

    # Cabeza de la serpiente
    head_x, head_y = pts[-1]
    head_r = int(28 * scale)
    # Triángulo de la cabeza
    tip = (head_x + int(24 * scale), head_y - int(10 * scale))
    b1 = (head_x - int(18 * scale), head_y - int(24 * scale))
    b2 = (head_x - int(10 * scale), head_y + int(18 * scale))
    draw.polygon([tip, b1, b2], fill=(0, 240, 255, 255), outline=(255, 255, 255, 255))

    # Ojos blancos brillantes
    draw.ellipse([head_x + int(2 * scale), head_y - int(12 * scale), head_x + int(8 * scale), head_y - int(6 * scale)], fill=(255, 255, 255, 255))
    draw.ellipse([head_x + int(6 * scale), head_y - int(2 * scale), head_x + int(12 * scale), head_y + int(4 * scale)], fill=(255, 255, 255, 255))

    # Nodo Dorado Cibernético
    star_x = int(cx + 120 * scale)
    star_y = int(cy + 100 * scale)
    star_r = int(26 * scale)

    # Halo dorado
    draw.ellipse([star_x - star_r - 8, star_y - star_r - 8, star_x + star_r + 8, star_y + star_r + 8], fill=(255, 230, 0, 50))
    # Estrella de 4 puntas dorada
    draw.polygon([
        (star_x, star_y - star_r),
        (star_x + star_r // 3, star_y - star_r // 3),
        (star_x + star_r, star_y),
        (star_x + star_r // 3, star_y + star_r // 3),
        (star_x, star_y + star_r),
        (star_x - star_r // 3, star_y + star_r // 3),
        (star_x - star_r, star_y),
        (star_x - star_r // 3, star_y - star_r // 3)
    ], fill=(255, 230, 0, 255), outline=(255, 255, 255, 255))

    return img

def build_all_icons():
    print("[build_icons.py] Generando suite de iconos PWA para Neon Snake v2.0...")
    configs = [
        ("icon-192.png", 192, False),
        ("icon-512.png", 512, False),
        ("icon-maskable-192.png", 192, True),
        ("icon-maskable-512.png", 512, True),
        ("apple-touch-icon.png", 180, False)
    ]
    for filename, size, maskable in configs:
        out_path = APP_DIR / filename
        icon = draw_snake_icon(size, maskable)
        icon.save(out_path, "PNG", optimize=True)
        print(f"  -> {filename} ({size}x{size}, maskable={maskable}) OK")

if __name__ == "__main__":
    build_all_icons()
