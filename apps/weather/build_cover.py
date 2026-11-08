# -*- coding: utf-8 -*-
"""Generador determinista de portadas cover.png para Weather Service v2.0.

Diseñado con Safe Zone estricta (márgenes laterales de 140px y despeje superior derecho de 280px)
para evitar recortes en tarjetas de Hugo (/apps/, home portal, y posts) independientemente
del aspect-ratio o de los badges absolutos de estado ([En Producción] [v2.0.0]).
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 750

# Paleta Dark Cockpit Datalaria
BG_CANVAS = (11, 15, 23)        # #0b0f17
BG_SURFACE = (17, 24, 39)       # #111827
BG_ELEVATED = (30, 41, 59)      # #1e293b
BORDER_COLOR = (51, 65, 85)     # #334155
TEXT_PRIMARY = (248, 250, 252)  # #f8fafc
TEXT_MUTED = (148, 163, 184)    # #94a3b8
ACCENT_CYAN = (14, 165, 233)    # #0ea5e9
ACCENT_PURPLE = (139, 92, 246)  # #8b5cf6
ACCENT_GREEN = (16, 185, 129)   # #10b981
ACCENT_AMBER = (245, 158, 11)   # #f59e0b
ACCENT_ROSE = (244, 63, 94)     # #f43f5e


def get_font(size: int, bold: bool = False):
    """Carga fuentes del sistema Windows con fallback determinista a default."""
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for fn in font_names:
        p = Path(fn)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_cover() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    # 1. Background Grid sutil
    grid_spacing = 40
    for x in range(0, WIDTH, grid_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=(17, 24, 39), width=1)
    for y in range(0, HEIGHT, grid_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=(17, 24, 39), width=1)

    # Línea superior de gradiente decorativo Cyan -> Purple
    for i in range(WIDTH):
        ratio = i / WIDTH
        r = int(ACCENT_CYAN[0] * (1 - ratio) + ACCENT_PURPLE[0] * ratio)
        g = int(ACCENT_CYAN[1] * (1 - ratio) + ACCENT_PURPLE[1] * ratio)
        b = int(ACCENT_CYAN[2] * (1 - ratio) + ACCENT_PURPLE[2] * ratio)
        draw.line([(i, 0), (i, 4)], fill=(r, g, b))

    # Safe Zone Horizontal: X in [140, 1060] (margen de seguridad de 140px a cada lado)
    SAFE_LEFT = 140
    SAFE_RIGHT = 1060

    # 2. Header Zone (alineado a SAFE_LEFT, dejando despejado X > 880 en Y < 90 para badges Hugo)
    font_brand = get_font(13, bold=True)
    draw.text((SAFE_LEFT, 68), "DATALARIA ENGINEERING • FLAGSHIP WEATHER v2.0", fill=ACCENT_CYAN, font=font_brand)

    font_title = get_font(38, bold=True)
    draw.text((SAFE_LEFT, 94), "Weather Intelligence v2.0", fill=TEXT_PRIMARY, font=font_title)

    font_subtitle = get_font(15, bold=False)
    draw.text((SAFE_LEFT, 146), "Observatorio Climático · Laboratorio ML Fourier · Atlas Global 168 Estaciones", fill=TEXT_MUTED, font=font_subtitle)

    # 3. Badges Row
    badges = [
        ("RELEASE v2.0.0", ACCENT_CYAN),
        ("168 ESTACIONES", ACCENT_GREEN),
        ("FOURIER HARMONIC ML", ACCENT_PURPLE),
        ("BIO-CONFORT 0..100", ACCENT_AMBER),
        ("0.00 €/mes SERVERLESS", ACCENT_GREEN),
    ]
    font_badge = get_font(11, bold=True)
    bx = SAFE_LEFT
    by = 180
    for text, color in badges:
        bbox = font_badge.getbbox(text)
        bw = (bbox[2] - bbox[0]) + 16
        bh = 24
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=BG_SURFACE, outline=color, width=1)
        draw.text((bx + 8, by + 4), text, fill=color, font=font_badge)
        bx += bw + 10

    # 4. Tres Tarjetas de las Vistas del Cockpit
    # Ancho disponible = 1060 - 140 = 920px. 3 tarjetas de 290px + 2 huecos de 25px = 920px.
    card_y = 226
    card_h = 444
    card_w = 290
    card_gap = 25

    # ----------------------------------------------------
    # Card 1: Observatorio Climático
    # ----------------------------------------------------
    c1_x = SAFE_LEFT
    draw.rounded_rectangle([c1_x, card_y, c1_x + card_w, card_y + card_h], radius=12, fill=BG_SURFACE, outline=BORDER_COLOR, width=1)
    draw.rounded_rectangle([c1_x, card_y, c1_x + card_w, card_y + 42], radius=12, fill=BG_ELEVATED)
    draw.rectangle([c1_x, card_y + 32, c1_x + card_w, card_y + 42], fill=BG_ELEVATED)
    draw.line([(c1_x, card_y + 42), (c1_x + card_w, card_y + 42)], fill=BORDER_COLOR, width=1)

    font_card_head = get_font(14, bold=True)
    draw.text((c1_x + 14, card_y + 11), "🌍 Vista 1: Observatorio", fill=TEXT_PRIMARY, font=font_card_head)

    font_metric_big = get_font(28, bold=True)
    font_small = get_font(12, bold=False)
    font_bold_small = get_font(12, bold=True)

    draw.text((c1_x + 16, card_y + 58), "Madrid, ES", fill=ACCENT_CYAN, font=font_bold_small)
    draw.text((c1_x + 16, card_y + 80), "21.4°C", fill=TEXT_PRIMARY, font=font_metric_big)
    draw.text((c1_x + 125, card_y + 90), "+2.4°C Δ30d", fill=ACCENT_ROSE, font=font_bold_small)

    # Confort pill
    draw.rounded_rectangle([c1_x + 16, card_y + 130, c1_x + card_w - 16, card_y + 162], radius=16, fill=(16, 185, 129, 35), outline=ACCENT_GREEN, width=1)
    draw.text((c1_x + 28, card_y + 138), "🏃 Confort: 88/100 Óptimo", fill=ACCENT_GREEN, font=font_bold_small)

    # Leaflet box
    map_box_y = card_y + 180
    draw.rounded_rectangle([c1_x + 16, map_box_y, c1_x + card_w - 16, map_box_y + 115], radius=8, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)
    draw.text((c1_x + 24, map_box_y + 10), "Leaflet Multi-Capa (5 Capas):", fill=TEXT_MUTED, font=font_small)

    dots = [
        (c1_x + 50, map_box_y + 50, ACCENT_GREEN),
        (c1_x + 95, map_box_y + 70, ACCENT_AMBER),
        (c1_x + 155, map_box_y + 42, ACCENT_CYAN),
        (c1_x + 215, map_box_y + 78, ACCENT_ROSE),
    ]
    for dx, dy, col in dots:
        draw.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=col, outline=TEXT_PRIMARY, width=1)

    draw.text((c1_x + 16, card_y + 320), "• Selector 7 Métricas (Sensación)", fill=TEXT_MUTED, font=font_small)
    draw.text((c1_x + 16, card_y + 348), "• Barra 5 Presets en 1 Clic", fill=TEXT_MUTED, font=font_small)
    draw.text((c1_x + 16, card_y + 376), "• Matriz Estacional 12 Meses", fill=TEXT_MUTED, font=font_small)
    draw.text((c1_x + 16, card_y + 404), "• Deep-Linking & Export CSV/JSON", fill=TEXT_MUTED, font=font_small)

    # ----------------------------------------------------
    # Card 2: Laboratorio ML Fourier
    # ----------------------------------------------------
    c2_x = c1_x + card_w + card_gap
    draw.rounded_rectangle([c2_x, card_y, c2_x + card_w, card_y + card_h], radius=12, fill=BG_SURFACE, outline=BORDER_COLOR, width=1)
    draw.rounded_rectangle([c2_x, card_y, c2_x + card_w, card_y + 42], radius=12, fill=BG_ELEVATED)
    draw.rectangle([c2_x, card_y + 32, c2_x + card_w, card_y + 42], fill=BG_ELEVATED)
    draw.line([(c2_x, card_y + 42), (c2_x + card_w, card_y + 42)], fill=BORDER_COLOR, width=1)

    draw.text((c2_x + 14, card_y + 11), "🤖 Vista 2: Laboratorio ML", fill=TEXT_PRIMARY, font=font_card_head)

    draw.text((c2_x + 16, card_y + 58), "Armónicos Cíclicos de Fourier:", fill=ACCENT_PURPLE, font=font_bold_small)

    # Sine/Cosine Wave Box
    wave_box_y = card_y + 82
    draw.rounded_rectangle([c2_x + 16, wave_box_y, c2_x + card_w - 16, wave_box_y + 105], radius=8, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)

    curve_pts = []
    for step in range(c2_x + 24, c2_x + card_w - 24):
        t = (step - (c2_x + 24)) / (card_w - 48) * 2 * math.pi
        y_val = wave_box_y + 52 - int(math.sin(t) * 32)
        curve_pts.append((step, y_val))
    if len(curve_pts) > 1:
        draw.line(curve_pts, fill=ACCENT_PURPLE, width=3)
    draw.text((c2_x + 24, wave_box_y + 10), "sin(2π·doy/365.25) + cos(...)", fill=TEXT_MUTED, font=font_small)

    # Scorecard Box
    sc_y = card_y + 208
    draw.text((c2_x + 16, sc_y), "Duelo Walk-Forward IA vs OWM:", fill=TEXT_PRIMARY, font=font_bold_small)

    sc_items = [
        ("R² Global Medio", "0.852", ACCENT_GREEN),
        ("MAE 30d Medio", "1.42 °C", ACCENT_CYAN),
        ("Bias 30d Medio", "-0.04 °C", TEXT_MUTED),
        ("IA Win-Rate 5D", "54.6 %", ACCENT_PURPLE),
    ]
    for idx, (label, val, val_col) in enumerate(sc_items):
        item_y = sc_y + 24 + idx * 28
        draw.text((c2_x + 20, item_y), label, fill=TEXT_MUTED, font=font_small)
        draw.text((c2_x + card_w - 85, item_y), val, fill=val_col, font=font_bold_small)

    draw.text((c2_x + 16, card_y + 376), "• Coherencia física min <= med <= max", fill=TEXT_MUTED, font=font_small)
    draw.text((c2_x + 16, card_y + 404), "• Feature weights normalizados", fill=TEXT_MUTED, font=font_small)

    # ----------------------------------------------------
    # Card 3: Atlas Global 168 Ciudades
    # ----------------------------------------------------
    c3_x = c2_x + card_w + card_gap
    draw.rounded_rectangle([c3_x, card_y, c3_x + card_w, card_y + card_h], radius=12, fill=BG_SURFACE, outline=BORDER_COLOR, width=1)
    draw.rounded_rectangle([c3_x, card_y, c3_x + card_w, card_y + 42], radius=12, fill=BG_ELEVATED)
    draw.rectangle([c3_x, card_y + 32, c3_x + card_w, card_y + 42], fill=BG_ELEVATED)
    draw.line([(c3_x, card_y + 42), (c3_x + card_w, card_y + 42)], fill=BORDER_COLOR, width=1)

    draw.text((c3_x + 14, card_y + 11), "🏆 Vista 3: Atlas 168", fill=TEXT_PRIMARY, font=font_card_head)

    draw.text((c3_x + 16, card_y + 58), "Cobertura en 6 Regiones:", fill=ACCENT_AMBER, font=font_bold_small)

    regions = [
        ("🇪🇸 España", "56 est."),
        ("🇪🇺 Europa", "47 est."),
        ("🌏 Asia", "25 est."),
        ("🌎 América", "23 est."),
        ("🌍 África", "13 est."),
        ("🇦🇺 Oceanía", "4 est."),
    ]
    for idx, (reg, count) in enumerate(regions):
        ry = card_y + 82 + idx * 24
        draw.text((c3_x + 20, ry), reg, fill=TEXT_PRIMARY, font=font_small)
        draw.text((c3_x + card_w - 75, ry), count, fill=ACCENT_CYAN, font=font_bold_small)

    # Mini Table
    tbl_y = card_y + 242
    draw.rounded_rectangle([c3_x + 16, tbl_y, c3_x + card_w - 16, tbl_y + 90], radius=8, fill=BG_CANVAS, outline=BORDER_COLOR, width=1)
    draw.text((c3_x + 24, tbl_y + 10), "#1 Palma • 21.2° • Confort 100", fill=ACCENT_GREEN, font=font_bold_small)
    draw.text((c3_x + 24, tbl_y + 36), "#2 Tenerife • 23.0° • Confort 94", fill=ACCENT_GREEN, font=font_small)
    draw.text((c3_x + 24, tbl_y + 62), "#168 Ulán Bator • -23° • Confort 12", fill=ACCENT_ROSE, font=font_small)

    draw.text((c3_x + 16, card_y + 376), "• Buscador por texto y 6 regiones", fill=TEXT_MUTED, font=font_small)
    draw.text((c3_x + 16, card_y + 404), "• Botón +Comparar a Observatorio", fill=TEXT_MUTED, font=font_small)

    # 5. Bottom Status Strip (dentro del Safe Zone)
    draw.line([(SAFE_LEFT, 686), (SAFE_RIGHT, 686)], fill=BORDER_COLOR, width=1)
    font_footer = get_font(11, bold=False)
    draw.text((SAFE_LEFT, 702), "DATALARIA SDD • SPEC-DRIVEN DEVELOPMENT • ARCHITECTURE ADR-021 • 192.000+ EMPIRICAL DATA", fill=TEXT_MUTED, font=font_footer)
    draw.text((SAFE_RIGHT - 180, 702), "datalaria.com/apps/weather", fill=ACCENT_CYAN, font=font_footer)

    return img


def main():
    img = create_cover()

    dest_paths = [
        Path("content/es/apps/weather/cover.png"),
        Path("content/en/apps/weather/cover.png"),
        Path("static/apps/weather/cover.png"),
    ]

    for p in dest_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        img.save(p, format="PNG", optimize=True)
        print(f"Generated: {p} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
