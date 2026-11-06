# apps/flashcards/build_icons.py
# Generador determinista de iconos rasterizados PWA para Flashcards AI
# Datalaria Helix — Strict Offline Resilience (INV-FLASH-8)

import math
from pathlib import Path
from PIL import Image, ImageDraw

APP_DIR = Path(__file__).resolve().parent

def draw_flashcards_icon(size: int, maskable: bool = False) -> Image.Image:
    # Lienzo RGBA
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado de violeta (#8b5cf6 -> 139, 92, 246) a azul (#3b82f6 -> 59, 130, 246)
    # Creamos un gradiente diagonal
    grad = Image.new("RGBA", (size, size))
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            r = int(139 * (1 - t) + 59 * t)
            g = int(92 * (1 - t) + 130 * t)
            b = int(246 * (1 - t) + 246 * t)
            grad.putpixel((x, y), (r, g, b, 255))

    # Máscara de esquinas redondeadas si no es maskable
    if not maskable:
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        corner_r = int(size * 0.22)
        mask_draw.rounded_rectangle([0, 0, size, size], radius=corner_r, fill=255)
        img.paste(grad, (0, 0), mask)
    else:
        # Maskable: fondo completo de 100% para safe-zone
        img.paste(grad, (0, 0))

    # 2. Dibujar las cartas 3D
    # Si es maskable, escalamos al 78% para cumplir con la zona segura de Android (80% safe zone)
    scale = (size / 512.0) * (0.80 if maskable else 0.95)
    cx, cy = size / 2, size / 2

    # Capa para los elementos centrales
    fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    fg_draw = ImageDraw.Draw(fg)

    # Carta Trasera (Verde Esmeralda - inclinada ~ -12 grados)
    # Creamos una tarjeta individual y la rotamos
    card_w = int(240 * scale)
    card_h = int(300 * scale)
    card_radius = int(22 * scale)

    # Sombra suave
    back_card = Image.new("RGBA", (card_w + 20, card_h + 20), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(back_card)
    b_draw.rounded_rectangle([4, 4, card_w + 4, card_h + 4], radius=card_radius, fill=(16, 185, 129, 255), outline=(52, 211, 153, 255), width=int(3 * scale))
    # Detalle en carta trasera: círculo y check blanco
    check_r = int(36 * scale)
    b_draw.ellipse([card_w//2 - check_r + 4, card_h//2 - check_r + 4, card_w//2 + check_r + 4, card_h//2 + check_r + 4], fill=(255, 255, 255, 60))
    
    # Rotar carta trasera -14 grados
    back_rot = back_card.rotate(14, resample=Image.Resampling.BICUBIC, expand=True)
    fg.paste(back_rot, (int(cx - back_rot.width / 2 - 15 * scale), int(cy - back_rot.height / 2 + 5 * scale)), back_rot)

    # Carta Frontal (Blanca - inclinada +6 grados)
    front_card = Image.new("RGBA", (card_w + 20, card_h + 20), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(front_card)
    f_draw.rounded_rectangle([4, 4, card_w + 4, card_h + 4], radius=card_radius, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=int(3 * scale))

    # Franjas de contenido en carta frontal
    f_draw.rounded_rectangle([int(35 * scale), int(50 * scale), int(card_w - 35 * scale), int(75 * scale)], radius=int(6 * scale), fill=(139, 92, 246, 255))
    f_draw.rounded_rectangle([int(50 * scale), int(90 * scale), int(card_w - 50 * scale), int(105 * scale)], radius=int(4 * scale), fill=(203, 213, 225, 255))
    f_draw.rounded_rectangle([int(35 * scale), int(140 * scale), int(card_w - 35 * scale), int(148 * scale)], radius=int(3 * scale), fill=(226, 232, 240, 255))
    f_draw.rounded_rectangle([int(35 * scale), int(160 * scale), int(card_w - 55 * scale), int(168 * scale)], radius=int(3 * scale), fill=(226, 232, 240, 255))
    f_draw.rounded_rectangle([int(35 * scale), int(180 * scale), int(card_w - 75 * scale), int(188 * scale)], radius=int(3 * scale), fill=(226, 232, 240, 255))

    # Icono de altavoz fonético en la base de la carta
    speaker_cx = card_w // 2 + 4
    speaker_cy = int(240 * scale)
    f_draw.ellipse([speaker_cx - int(24 * scale), speaker_cy - int(24 * scale), speaker_cx + int(24 * scale), speaker_cy + int(24 * scale)], fill=(238, 242, 255, 255))
    f_draw.polygon([
        (speaker_cx - int(10 * scale), speaker_cy - int(6 * scale)),
        (speaker_cx - int(3 * scale), speaker_cy - int(6 * scale)),
        (speaker_cx + int(6 * scale), speaker_cy - int(12 * scale)),
        (speaker_cx + int(6 * scale), speaker_cy + int(12 * scale)),
        (speaker_cx - int(3 * scale), speaker_cy + int(6 * scale)),
        (speaker_cx - int(10 * scale), speaker_cy + int(6 * scale))
    ], fill=(139, 92, 246, 255))

    # Rotar carta frontal -6 grados
    front_rot = front_card.rotate(-6, resample=Image.Resampling.BICUBIC, expand=True)
    fg.paste(front_rot, (int(cx - front_rot.width / 2 + 10 * scale), int(cy - front_rot.height / 2 - 10 * scale)), front_rot)

    # Destello de estrella mágica (dorada #fbbf24)
    star_x = int(cx + 120 * scale)
    star_y = int(cy - 120 * scale)
    star_size = int(28 * scale)
    fg_draw.polygon([
        (star_x, star_y - star_size),
        (star_x + star_size // 4, star_y - star_size // 4),
        (star_x + star_size, star_y),
        (star_x + star_size // 4, star_y + star_size // 4),
        (star_x, star_y + star_size),
        (star_x - star_size // 4, star_y + star_size // 4),
        (star_x - star_size, star_y),
        (star_x - star_size // 4, star_y - star_size // 4)
    ], fill=(251, 191, 36, 255))

    img.paste(fg, (0, 0), fg)
    return img

def main():
    print("[build_icons.py] Generando suite completa de iconos PWA para Flashcards AI...")
    
    # 1. icon-512.png (512x512 estándar)
    icon_512 = draw_flashcards_icon(512, maskable=False)
    icon_512.save(APP_DIR / "icon-512.png", "PNG", optimize=True)
    print("  -> Generado icon-512.png")

    # 2. icon-192.png (192x192 estándar)
    icon_192 = draw_flashcards_icon(192, maskable=False)
    icon_192.save(APP_DIR / "icon-192.png", "PNG", optimize=True)
    print("  -> Generado icon-192.png")

    # 3. icon-maskable-512.png (512x512 maskable)
    mask_512 = draw_flashcards_icon(512, maskable=True)
    mask_512.save(APP_DIR / "icon-maskable-512.png", "PNG", optimize=True)
    print("  -> Generado icon-maskable-512.png")

    # 4. icon-maskable-192.png (192x192 maskable)
    mask_192 = draw_flashcards_icon(192, maskable=True)
    mask_192.save(APP_DIR / "icon-maskable-192.png", "PNG", optimize=True)
    print("  -> Generado icon-maskable-192.png")

    # 5. apple-touch-icon.png (180x180 para iOS)
    apple_icon = draw_flashcards_icon(180, maskable=False)
    apple_icon.save(APP_DIR / "apple-touch-icon.png", "PNG", optimize=True)
    print("  -> Generado apple-touch-icon.png")

    print("[build_icons.py] 5 iconos PWA generados con éxito.")

if __name__ == "__main__":
    main()
