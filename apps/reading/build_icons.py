# apps/reading/build_icons.py
# Generador determinista de iconos rasterizados PWA para Lector Arcade / Reader Arcade
# Datalaria Helix — Strict Offline Resilience (INV-READ-8)

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

APP_DIR = Path(__file__).resolve().parent

def draw_reading_icon(size: int, maskable: bool = False) -> Image.Image:
    # 1. Crear lienzo RGBA
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # Gradiente diagonal de Cyan (#0284c7: 2, 132, 199) -> Azul (#2563eb: 37, 99, 235) -> Violeta (#7c3aed: 124, 58, 237)
    grad = Image.new("RGBA", (size, size))
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2.0 * size)
            if t < 0.5:
                sub_t = t * 2.0
                r = int(2 * (1 - sub_t) + 37 * sub_t)
                g = int(132 * (1 - sub_t) + 99 * sub_t)
                b = int(199 * (1 - sub_t) + 235 * sub_t)
            else:
                sub_t = (t - 0.5) * 2.0
                r = int(37 * (1 - sub_t) + 124 * sub_t)
                g = int(99 * (1 - sub_t) + 58 * sub_t)
                b = int(235 * (1 - sub_t) + 237 * sub_t)
            grad.putpixel((x, y), (r, g, b, 255))

    # Máscara de esquinas redondeadas si no es maskable
    if not maskable:
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        corner_r = int(size * 0.22)
        mask_draw.rounded_rectangle([0, 0, size, size], radius=corner_r, fill=255)
        img.paste(grad, (0, 0), mask)
    else:
        # Maskable: fondo completo de 100% para Android safe zone
        img.paste(grad, (0, 0))

    # 2. Dibujar elementos vectoriales en primer plano
    # Android adaptive icons tienen una zona segura del 80% (diámetro 0.8 * size)
    scale = (size / 512.0) * (0.78 if maskable else 0.94)
    cx, cy = size / 2.0, size / 2.0

    fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    fg_draw = ImageDraw.Draw(fg)

    # Anillo sutil decorativo
    ring_r = int(190 * scale)
    fg_draw.ellipse(
        [cx - ring_r, cy - ring_r + int(10 * scale), cx + ring_r, cy + ring_r + int(10 * scale)],
        outline=(255, 255, 255, 35),
        width=max(1, int(2 * scale))
    )

    # 3. Dibujar Libro Abierto 3D
    book_w = int(320 * scale)
    book_h = int(180 * scale)
    book_top = cy - int(45 * scale)

    # Tapa exterior trasera dorada/ámbar
    cover_pad = int(8 * scale)
    cover_left = cx - book_w / 2 - cover_pad
    cover_right = cx + book_w / 2 + cover_pad
    cover_bottom = book_top + book_h + cover_pad
    
    fg_draw.polygon([
        (cover_left, book_top + int(10 * scale)),
        (cx, book_top + int(30 * scale)),
        (cover_right, book_top + int(10 * scale)),
        (cover_right, cover_bottom),
        (cx, cover_bottom + int(18 * scale)),
        (cover_left, cover_bottom)
    ], fill=(217, 119, 6, 255))

    # Página izquierda (blanco perla / marfil)
    page_l_left = cx - book_w / 2
    page_l_right = cx - int(2 * scale)
    fg_draw.polygon([
        (page_l_left, book_top + int(15 * scale)),
        (page_l_right, book_top + int(32 * scale)),
        (page_l_right, cover_bottom - int(2 * scale)),
        (page_l_left, cover_bottom - int(10 * scale))
    ], fill=(248, 250, 252, 255))

    # Página derecha (blanco puro)
    page_r_left = cx + int(2 * scale)
    page_r_right = cx + book_w / 2
    fg_draw.polygon([
        (page_r_left, book_top + int(32 * scale)),
        (page_r_right, book_top + int(15 * scale)),
        (page_r_right, cover_bottom - int(10 * scale)),
        (page_r_left, cover_bottom - int(2 * scale))
    ], fill=(255, 255, 255, 255))

    # Lomo central sombreado
    fg_draw.rectangle(
        [cx - int(3 * scale), book_top + int(30 * scale), cx + int(3 * scale), cover_bottom],
        fill=(148, 163, 184, 180)
    )

    # 4. Líneas de lectura estilizadas
    line_h = max(2, int(6 * scale))
    # Líneas página izquierda
    fg_draw.rounded_rectangle([page_l_left + int(24 * scale), book_top + int(48 * scale), page_l_right - int(24 * scale), book_top + int(48 * scale) + line_h], radius=line_h//2, fill=(14, 165, 233, 220))
    fg_draw.rounded_rectangle([page_l_left + int(24 * scale), book_top + int(70 * scale), page_l_right - int(38 * scale), book_top + int(70 * scale) + line_h], radius=line_h//2, fill=(203, 213, 225, 200))
    fg_draw.rounded_rectangle([page_l_left + int(24 * scale), book_top + int(92 * scale), page_l_right - int(28 * scale), book_top + int(92 * scale) + line_h], radius=line_h//2, fill=(203, 213, 225, 200))
    fg_draw.rounded_rectangle([page_l_left + int(24 * scale), book_top + int(114 * scale), page_l_right - int(48 * scale), book_top + int(114 * scale) + line_h], radius=line_h//2, fill=(203, 213, 225, 200))

    # Líneas página derecha
    fg_draw.rounded_rectangle([page_r_left + int(24 * scale), book_top + int(48 * scale), page_r_right - int(24 * scale), book_top + int(48 * scale) + line_h], radius=line_h//2, fill=(225, 29, 72, 220))
    fg_draw.rounded_rectangle([page_r_left + int(24 * scale), book_top + int(70 * scale), page_r_right - int(34 * scale), book_top + int(70 * scale) + line_h], radius=line_h//2, fill=(203, 213, 225, 200))
    fg_draw.rounded_rectangle([page_r_left + int(24 * scale), book_top + int(92 * scale), page_r_right - int(44 * scale), book_top + int(92 * scale) + line_h], radius=line_h//2, fill=(203, 213, 225, 200))
    fg_draw.rounded_rectangle([page_r_left + int(24 * scale), book_top + int(114 * scale), page_r_right - int(28 * scale), book_top + int(114 * scale) + line_h], radius=line_h//2, fill=(203, 213, 225, 200))

    # 5. Badges silábicos 3D ("A" en página izquierda, "B" en página derecha, punto central)
    badge_r = int(22 * scale)
    badge_l_cx = int(page_l_left + (page_l_right - page_l_left) / 2)
    badge_l_cy = int(book_top + int(144 * scale))
    
    # Sombra del badge
    fg_draw.ellipse([badge_l_cx - badge_r, badge_l_cy - badge_r + int(3 * scale), badge_l_cx + badge_r, badge_l_cy + badge_r + int(3 * scale)], fill=(2, 132, 199, 120))
    # Badge A
    fg_draw.ellipse([badge_l_cx - badge_r, badge_l_cy - badge_r, badge_l_cx + badge_r, badge_l_cy + badge_r], fill=(2, 132, 199, 255), outline=(56, 189, 248, 255), width=max(1, int(2 * scale)))

    badge_r_cx = int(page_r_left + (page_r_right - page_r_left) / 2)
    badge_r_cy = badge_l_cy
    # Sombra del badge B
    fg_draw.ellipse([badge_r_cx - badge_r, badge_r_cy - badge_r + int(3 * scale), badge_r_cx + badge_r, badge_r_cy + badge_r + int(3 * scale)], fill=(225, 29, 72, 120))
    # Badge B
    fg_draw.ellipse([badge_r_cx - badge_r, badge_r_cy - badge_r, badge_r_cx + badge_r, badge_r_cy + badge_r], fill=(225, 29, 72, 255), outline=(251, 113, 133, 255), width=max(1, int(2 * scale)))

    # Letra A poligonal en badge izquierdo
    font_scale = scale * 0.75
    # Dibujamos triángulo y trazo de 'A' estilizado
    fg_draw.polygon([
        (badge_l_cx, badge_l_cy - int(12 * scale)),
        (badge_l_cx - int(9 * scale), badge_l_cy + int(11 * scale)),
        (badge_l_cx - int(4 * scale), badge_l_cy + int(11 * scale)),
        (badge_l_cx - int(2 * scale), badge_l_cy + int(5 * scale)),
        (badge_l_cx + int(2 * scale), badge_l_cy + int(5 * scale)),
        (badge_l_cx + int(4 * scale), badge_l_cy + int(11 * scale)),
        (badge_l_cx + int(9 * scale), badge_l_cy + int(11 * scale))
    ], fill=(255, 255, 255, 255))
    fg_draw.polygon([
        (badge_l_cx, badge_l_cy - int(4 * scale)),
        (badge_l_cx - int(2 * scale), badge_l_cy + int(2 * scale)),
        (badge_l_cx + int(2 * scale), badge_l_cy + int(2 * scale))
    ], fill=(2, 132, 199, 255))

    # Letra B poligonal en badge derecho
    fg_draw.rounded_rectangle([badge_r_cx - int(7 * scale), badge_r_cy - int(11 * scale), badge_r_cx + int(6 * scale), badge_r_cy + int(11 * scale)], radius=int(4 * scale), fill=(255, 255, 255, 255))
    fg_draw.rounded_rectangle([badge_r_cx - int(3 * scale), badge_r_cy - int(8 * scale), badge_r_cx + int(2 * scale), badge_r_cy - int(2 * scale)], radius=int(2 * scale), fill=(225, 29, 72, 255))
    fg_draw.rounded_rectangle([badge_r_cx - int(3 * scale), badge_r_cy + int(1 * scale), badge_r_cx + int(2 * scale), badge_r_cy + int(8 * scale)], radius=int(2 * scale), fill=(225, 29, 72, 255))

    # Punto silábico dorado central
    dot_r = int(7 * scale)
    fg_draw.ellipse([cx - dot_r, badge_l_cy - dot_r, cx + dot_r, badge_l_cy + dot_r], fill=(251, 191, 36, 255))

    # 6. Estrella Arcade Dorada arriba a la derecha
    star_x = int(cx + 125 * scale)
    star_y = int(cy - 125 * scale)
    star_r_out = int(32 * scale)
    star_r_in = int(14 * scale)
    star_pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * (math.pi / 5)
        r = star_r_out if i % 2 == 0 else star_r_in
        star_pts.append((star_x + r * math.cos(angle), star_y + r * math.sin(angle)))
    fg_draw.polygon(star_pts, fill=(251, 191, 36, 255), outline=(254, 240, 138, 255), width=max(1, int(2 * scale)))

    # Pequeño destello estelar en la estrella
    fg_draw.ellipse([star_x - int(5 * scale), star_y - int(5 * scale), star_x + int(5 * scale), star_y + int(5 * scale)], fill=(255, 255, 255, 200))

    img.paste(fg, (0, 0), fg)
    return img

def main():
    print("[build_icons.py] Generando suite completa de iconos PWA para Lector Arcade...")

    # 1. icon-512.png
    icon_512 = draw_reading_icon(512, maskable=False)
    icon_512.save(APP_DIR / "icon-512.png", "PNG", optimize=True)
    print("  -> Generado icon-512.png")

    # 2. icon-192.png
    icon_192 = draw_reading_icon(192, maskable=False)
    icon_192.save(APP_DIR / "icon-192.png", "PNG", optimize=True)
    print("  -> Generado icon-192.png")

    # 3. icon-maskable-512.png
    mask_512 = draw_reading_icon(512, maskable=True)
    mask_512.save(APP_DIR / "icon-maskable-512.png", "PNG", optimize=True)
    print("  -> Generado icon-maskable-512.png")

    # 4. icon-maskable-192.png
    mask_192 = draw_reading_icon(192, maskable=True)
    mask_192.save(APP_DIR / "icon-maskable-192.png", "PNG", optimize=True)
    print("  -> Generado icon-maskable-192.png")

    # 5. apple-touch-icon.png (180x180 para iOS Safari)
    apple_icon = draw_reading_icon(180, maskable=False)
    apple_icon.save(APP_DIR / "apple-touch-icon.png", "PNG", optimize=True)
    print("  -> Generado apple-touch-icon.png")

    print("[build_icons.py] 5 iconos PWA generados con éxito.")

if __name__ == "__main__":
    main()
