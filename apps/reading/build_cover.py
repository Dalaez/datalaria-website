# -*- coding: utf-8 -*-
"""apps/reading/build_cover.py
Generador determinista de portadas oficiales cover.png para Lector Arcade / Reader Arcade (ES y EN).

Dimensiones: 1200 x 750 px (16:10)
Safe Zone Horizontal: [145px, 1055px]
Garantiza cero glifos tofu (□) y alta legibilidad para PaperMod y showcase /apps/.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 750

# Safe Zone canónica para PaperMod
SAFE_LEFT = 145
SAFE_RIGHT = 1055

# Paleta Arcade Datalaria (Cosmic Night & Daylight Playful)
BG_CANVAS = (12, 16, 29)          # #0c101d
BG_SURFACE = (18, 25, 44)         # #12192c
BG_CARD = (26, 36, 62)            # #1a243e
BG_CARD_INNER = (34, 47, 80)      # #222f50
BORDER_COLOR = (53, 71, 115)      # #354773
BORDER_ACCENT = (14, 165, 233)    # Cyan
TEXT_PRIMARY = (248, 250, 252)    # #f8fafc
TEXT_MUTED = (148, 163, 184)      # #94a3b8
TEXT_DIM = (100, 116, 139)        # #64748b

# Acentos arcade
COLOR_CYAN = (14, 165, 233)       # #0ea5e9
COLOR_EMERALD = (16, 185, 129)    # #10b981
COLOR_AMBER = (245, 158, 11)      # #f59e0b
COLOR_PURPLE = (168, 85, 247)     # #a855f7
COLOR_ROSE = (244, 63, 94)        # #f43f5e
COLOR_INDIGO = (99, 102, 241)     # #6366f1


def get_font(size: int, bold: bool = False):
    """Carga fuentes TrueType del sistema con fallback seguro determinista."""
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "/System/Library/Fonts/SFProText-Bold.ttf" if bold else "/System/Library/Fonts/SFProText-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for fn in font_names:
        p = Path(fn)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_rounded_rect(draw: ImageDraw.Draw, xy, radius: int, fill=None, outline=None, width=1):
    """Dibuja un rectángulo con esquinas redondeadas."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def create_cover(lang: str = "es") -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    # 1. Fondo con gradiente vertical sutil
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(12 * (1 - ratio) + 18 * ratio)
        g = int(16 * (1 - ratio) + 24 * ratio)
        b = int(29 * (1 - ratio) + 42 * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Rejilla sutil geométrica
    grid_gap = 48
    for x in range(0, WIDTH, grid_gap):
        for y in range(0, HEIGHT, grid_gap):
            draw.point((x, y), fill=(35, 48, 80))

    # 2. Barra de gradiente superior arcade
    gradient_stops = [COLOR_EMERALD, COLOR_CYAN, COLOR_INDIGO, COLOR_PURPLE, COLOR_AMBER, COLOR_ROSE]
    num_stops = len(gradient_stops) - 1
    for i in range(WIDTH):
        pos = (i / WIDTH) * num_stops
        idx = min(int(pos), num_stops - 1)
        t = pos - idx
        c1 = gradient_stops[idx]
        c2 = gradient_stops[idx + 1]
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(i, 0), (i, 4)], fill=(r, g, b))

    # 3. Lado Izquierdo: Branding, Título y Descripción
    font_badge = get_font(13, bold=True)
    font_title = get_font(40, bold=True)
    font_subtitle = get_font(16, bold=False)
    font_body = get_font(14, bold=False)
    font_chip = get_font(12, bold=True)
    font_lg_bold = get_font(22, bold=True)
    font_md_bold = get_font(16, bold=True)

    # Brand Pill
    brand_text = "DATALARIA LAB • CONSUMER PLAYFUL • PWA OFFLINE"
    badge_w = 410
    draw_rounded_rect(draw, [SAFE_LEFT, 68, SAFE_LEFT + badge_w, 96], radius=14, fill=BG_CARD_INNER, outline=BORDER_COLOR)
    draw.text((SAFE_LEFT + 16, 74), brand_text, fill=COLOR_CYAN, font=font_badge)

    # Título Principal
    title_text = "Lector Arcade v1.1" if lang == "es" else "Reader Arcade v1.1"
    draw.text((SAFE_LEFT, 114), title_text, fill=TEXT_PRIMARY, font=font_title)

    # Subtítulo y Tagline
    sub_text = (
        "Alfabetización Lúdica · Conciencia Fonológica · Fluidez Lectora PPM"
        if lang == "es" else
        "Playful Literacy · Phonics & Syllables · Split Reading Stopwatch"
    )
    draw.text((SAFE_LEFT, 172), sub_text, fill=COLOR_AMBER, font=font_subtitle)

    desc_line1 = (
        "Entrenamiento adaptativo en 6 niveles con audio dual 1.0x/0.5x,"
        if lang == "es" else
        "Adaptive 6-level reading training featuring dual 1.0x/0.5x audio,"
    )
    desc_line2 = (
        "karaoke silábico, SVGs nativos, modo 'Mis Palabras' y láminas A4."
        if lang == "es" else
        "syllable karaoke, native SVGs, 'My Words' mode, and printable A4 sheets."
    )
    draw.text((SAFE_LEFT, 206), desc_line1, fill=TEXT_MUTED, font=font_body)
    draw.text((SAFE_LEFT, 230), desc_line2, fill=TEXT_MUTED, font=font_body)

    # Píldoras de Features (Columna izquierda inferior)
    pills = [
        ("🌱 6 Niveles Curriculares" if lang == "es" else "🌱 6 Curricular Levels", COLOR_EMERALD),
        ("⏱️ Cronómetro Split PPM" if lang == "es" else "⏱️ Split WPM Stopwatch", COLOR_CYAN),
        ("🔊 Audio Dual · 🐢 0.5x" if lang == "es" else "🔊 Dual Audio · 🐢 0.5x", COLOR_AMBER),
        ("🎨 Ilustraciones SVG" if lang == "es" else "🎨 Native SVG Icons", COLOR_PURPLE),
        ("✏️ Modo Mis Palabras" if lang == "es" else "✏️ Custom Words Mode", COLOR_ROSE),
        ("🖨️ Lámina A4 & Diploma" if lang == "es" else "🖨️ A4 Sheet & Diploma", COLOR_CYAN),
    ]

    pill_y = 280
    for i, (text, col) in enumerate(pills):
        col_idx = i % 2
        row_idx = i // 2
        px = SAFE_LEFT + col_idx * 210
        py = pill_y + row_idx * 38
        draw_rounded_rect(draw, [px, py, px + 200, py + 30], radius=8, fill=BG_SURFACE, outline=BORDER_COLOR)
        draw.text((px + 10, py + 7), text, fill=TEXT_PRIMARY, font=font_chip)

    # Módulo de Perfiles Familiares en la base izquierda
    prof_y = 412
    draw_rounded_rect(draw, [SAFE_LEFT, prof_y, SAFE_LEFT + 420, prof_y + 80], radius=12, fill=BG_CARD, outline=BORDER_COLOR)
    prof_label = "Perfiles Familiares Aislados:" if lang == "es" else "Isolated Family Profiles:"
    draw.text((SAFE_LEFT + 16, prof_y + 12), prof_label, fill=TEXT_MUTED, font=font_chip)

    profiles = [
        ("🦁 Jugador 1" if lang == "es" else "🦁 Player 1", "Récord: 145 PPM", COLOR_EMERALD),
        ("🦊 Jugador 2" if lang == "es" else "🦊 Player 2", "Racha: 12", COLOR_CYAN),
        ("🦉 Adulto" if lang == "es" else "🦉 Adult", "6 Medallas", COLOR_PURPLE),
    ]
    for idx, (pname, pstat, pcol) in enumerate(profiles):
        bx = SAFE_LEFT + 16 + idx * 132
        by = prof_y + 36
        draw_rounded_rect(draw, [bx, by, bx + 122, by + 34], radius=6, fill=BG_CARD_INNER, outline=pcol)
        draw.text((bx + 8, by + 4), pname, fill=TEXT_PRIMARY, font=font_chip)
        draw.text((bx + 8, by + 18), pstat, fill=pcol, font=get_font(10, bold=False))

    # Indicador de privacidad en la esquina inferior izquierda
    priv_y = 512
    priv_text = "🛡️ Privacidad Infantil Garantizada · 100% Client-Side · Cero Micrófonos Remotos" if lang == "es" else "🛡️ Child Privacy Enforced · 100% Client-Side · Zero Remote Microphones"
    draw.text((SAFE_LEFT, priv_y), priv_text, fill=COLOR_EMERALD, font=font_chip)

    # 4. Lado Derecho: Maqueta Interactiva de la Tarjeta Arcade de Juego
    CARD_X = 610
    CARD_Y = 110
    CARD_W = 430
    CARD_H = 430

    # Sombra de tarjeta
    draw_rounded_rect(draw, [CARD_X + 6, CARD_Y + 6, CARD_X + CARD_W + 6, CARD_Y + CARD_H + 6], radius=18, fill=(8, 11, 20))
    # Tarjeta Principal Arcade
    draw_rounded_rect(draw, [CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + CARD_H], radius=18, fill=BG_CARD, outline=COLOR_CYAN, width=2)

    # Cabecera de la Tarjeta Arcade
    draw_rounded_rect(draw, [CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + 48], radius=18, fill=BG_CARD_INNER)
    draw.line([(CARD_X, CARD_Y + 48), (CARD_X + CARD_W, CARD_Y + 48)], fill=BORDER_COLOR, width=1)

    level_header = "NIVEL 2: PALABRA CON IMAGEN · ⭐⭐⭐" if lang == "es" else "LEVEL 2: WORD WITH IMAGE · ⭐⭐⭐"
    draw.text((CARD_X + 18, CARD_Y + 16), level_header, fill=COLOR_CYAN, font=font_badge)

    # Indicador de modo Contrarreloj (derecha de la cabecera)
    stopwatch_header = "⏱️ CONTRARRELOJ" if lang == "es" else "⏱️ TIME ATTACK"
    draw.text((CARD_X + CARD_W - 145, CARD_Y + 16), stopwatch_header, fill=COLOR_AMBER, font=font_badge)

    # Cuerpo del Reto Lector
    # Visual Box
    box_x = CARD_X + 24
    box_y = CARD_Y + 66
    box_w = CARD_W - 48
    box_h = 138
    draw_rounded_rect(draw, [box_x, box_y, box_x + box_w, box_y + box_h], radius=12, fill=BG_SURFACE, outline=BORDER_COLOR)

    # Icono central representativo
    icon_text = "🦁"
    draw.text((box_x + box_w // 2 - 24, box_y + 8), icon_text, fill=COLOR_AMBER, font=get_font(38))

    # Sílabas coloreadas debajo del icono
    syl_label = "[ LE ]   [ ÓN ]" if lang == "es" else "[ LI ]   [ ON ]"
    draw.text((box_x + box_w // 2 - 46, box_y + 62), syl_label, fill=COLOR_CYAN, font=font_lg_bold)

    # Botones Duales de Audio con Karaoke
    audio_btn_y = box_y + 98
    draw_rounded_rect(draw, [box_x + 36, audio_btn_y, box_x + 166, audio_btn_y + 28], radius=6, fill=BG_CARD_INNER, outline=COLOR_CYAN)
    draw.text((box_x + 46, audio_btn_y + 6), "🔊 1.0x Normal", fill=TEXT_PRIMARY, font=get_font(10, bold=True))
    draw_rounded_rect(draw, [box_x + 180, audio_btn_y, box_x + 310, audio_btn_y + 28], radius=6, fill=BG_CARD_INNER, outline=COLOR_AMBER)
    draw.text((box_x + 190, audio_btn_y + 6), "🐢 0.5x Tortuga", fill=COLOR_AMBER, font=get_font(10, bold=True))

    # Barra del Cronómetro Split congelado
    timer_box_y = box_y + box_h + 12
    draw_rounded_rect(draw, [box_x, timer_box_y, box_x + box_w, timer_box_y + 42], radius=8, fill=BG_CARD_INNER, outline=COLOR_AMBER)
    timer_display = "⏱️ Tiempo: 01.8s   |   Fluidez: 120 PPM" if lang == "es" else "⏱️ Time: 01.8s   |   Fluency: 120 WPM"
    draw.text((box_x + 18, timer_box_y + 11), timer_display, fill=COLOR_AMBER, font=font_md_bold)

    # Botón Principal Verde Arcade: "¡Leído!"
    btn_y = timer_box_y + 54
    draw_rounded_rect(draw, [box_x, btn_y, box_x + box_w, btn_y + 50], radius=12, fill=COLOR_EMERALD, outline=(255, 255, 255), width=2)
    btn_text = "✅  ¡LEÍDO! (Detener Cronómetro)" if lang == "es" else "✅  READ DONE! (Freeze Timer)"
    draw.text((box_x + 28, btn_y + 14), btn_text, fill=(255, 255, 255), font=font_md_bold)

    # Micro-check de comprensión (simulado en la parte inferior de la tarjeta)
    check_y = btn_y + 60
    check_q = "¿Qué animal has leído?  [ 🦁 León ]  [ 🐻 Oso ]  [ 🦊 Zorro ]" if lang == "es" else "Which animal did you read?  [ 🦁 Lion ]  [ 🐻 Bear ]  [ 🦊 Fox ]"
    draw_rounded_rect(draw, [box_x, check_y, box_x + box_w, check_y + 32], radius=6, fill=BG_SURFACE, outline=BORDER_COLOR)
    draw.text((box_x + 12, check_y + 8), check_q, fill=TEXT_MUTED, font=get_font(11, bold=False))

    # Medalla coleccionable flotante decorativa
    medal_x = CARD_X + CARD_W - 65
    medal_y = CARD_Y - 18
    draw_rounded_rect(draw, [medal_x, medal_y, medal_x + 56, medal_y + 56], radius=28, fill=COLOR_AMBER, outline=(255, 255, 255), width=2)
    draw.text((medal_x + 14, medal_y + 12), "🏅", fill=(255, 255, 255), font=get_font(24))

    # Guardar imagen con compresión óptima
    return img


def main():
    root = Path(__file__).resolve().parent.parent.parent

    # Destinos canónicos
    out_es = root / "content" / "es" / "apps" / "reading" / "cover.png"
    out_en = root / "content" / "en" / "apps" / "reading" / "cover.png"

    out_es.parent.mkdir(parents=True, exist_ok=True)
    out_en.parent.mkdir(parents=True, exist_ok=True)

    print("Generando portada ES (1200x750)...")
    img_es = create_cover("es")
    img_es.save(str(out_es), format="PNG", optimize=True)
    print(f" -> Guardado: {out_es} ({out_es.stat().st_size} bytes)")

    print("Generando portada EN (1200x750)...")
    img_en = create_cover("en")
    img_en.save(str(out_en), format="PNG", optimize=True)
    print(f" -> Guardado: {out_en} ({out_en.stat().st_size} bytes)")

    # Copia de seguridad en apps/reading/cover.png y static/apps/reading/cover.png
    local_cover = root / "apps" / "reading" / "cover.png"
    static_cover = root / "static" / "apps" / "reading" / "cover.png"
    img_es.save(str(local_cover), format="PNG", optimize=True)
    img_es.save(str(static_cover), format="PNG", optimize=True)
    print(f" -> Copias locales actualizadas en apps/reading/ y static/apps/reading/")


if __name__ == "__main__":
    main()
