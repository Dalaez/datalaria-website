"""
ops/pulse/kit/build_preview_images.py
-------------------------------------
Generador determinista de miniaturas comerciales estilo Executive Decision Pack
(1200x630 px y 1080x1080 px) y previsualizaciones del catálogo (1600x980 px)
para Datalaria Pulse Content Ops Kit Dual (ES/EN).

Genera:
  - packages/pulse/Pulse_Kit_Thumbnail_ES.png (1200x630 px — Miniatura ES)
  - packages/pulse/Pulse_Kit_Thumbnail_EN.png (1200x630 px — Miniatura EN para Lemon Squeezy)
  - packages/00_DISTRIBUCION_LEMONSQUEEZY/Images/Pulse.png (1200x630 px)
  - packages/00_DISTRIBUCION_LEMONSQUEEZY/Images_Square/Pulse.png (1080x1080 px)
  - static/images/recursos/pulse-preview-es.png (1600x980 px con PDF real de 5 págs)
  - static/images/recursos/pulse-preview-en.png (1600x980 px con PDF real de 5 págs)
  - Copias sincronizadas en content/{es,en}/posts/pulse-parte1.. y pulse-parte5..

Cero glifos rotos (□): toda la iconografía usa primitivos vectoriales Pillow.
"""

import io
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PACKAGES_PULSE_DIR = ROOT_DIR / "packages" / "pulse"
PDF_ES_PATH = PACKAGES_PULSE_DIR / "GUIA_EJECUTIVA_PULSE_ES.pdf"
PDF_EN_PATH = PACKAGES_PULSE_DIR / "PULSE_EXECUTIVE_GUIDE_EN.pdf"
LEMON_IMAGES_DIR = ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY" / "Images"
LEMON_SQUARE_DIR = ROOT_DIR / "packages" / "00_DISTRIBUCION_LEMONSQUEEZY" / "Images_Square"
RECURSOS_IMAGES_DIR = ROOT_DIR / "static" / "images" / "recursos"

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def get_font(size: int, bold: bool = False):
    """Carga fuente TrueType verificada en Windows/Linux con fallback seguro."""
    candidates = (
        ["segoeuib.ttf", "seguisb.ttf", "arialbd.ttf", "calibrib.ttf"]
        if bold
        else ["segoeui.ttf", "arial.ttf", "calibri.ttf"]
    )
    for name in candidates:
        win_path = Path(r"C:\Windows\Fonts") / name
        for target in (str(win_path), name):
            try:
                return ImageFont.truetype(target, int(size))
            except OSError:
                continue
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Primitivos vectoriales Pillow (evitan glifos □ / tofu de fuentes sin emoji)
# ---------------------------------------------------------------------------

def draw_icon_excel(draw: ImageDraw.ImageDraw, x: int, y: int, color):
    draw.rounded_rectangle([(x, y), (x + 16, y + 16)], radius=3, fill=color)
    draw.line([(x + 5, y + 3), (x + 5, y + 13)], fill=(255, 255, 255), width=1)
    draw.line([(x + 10, y + 3), (x + 10, y + 13)], fill=(255, 255, 255), width=1)
    draw.line([(x + 3, y + 8), (x + 13, y + 8)], fill=(255, 255, 255), width=1)


def draw_icon_cli(draw: ImageDraw.ImageDraw, x: int, y: int, color):
    draw.rounded_rectangle([(x, y), (x + 16, y + 16)], radius=3, fill=color)
    draw.line([(x + 4, y + 5), (x + 7, y + 8), (x + 4, y + 11)], fill=(255, 255, 255), width=2)
    draw.line([(x + 9, y + 11), (x + 13, y + 11)], fill=(255, 255, 255), width=2)


def draw_icon_pdf(draw: ImageDraw.ImageDraw, x: int, y: int, color):
    draw.rounded_rectangle([(x + 1, y), (x + 15, y + 16)], radius=2, fill=color)
    draw.line([(x + 4, y + 5), (x + 12, y + 5)], fill=(255, 255, 255), width=2)
    draw.line([(x + 4, y + 9), (x + 12, y + 9)], fill=(255, 255, 255), width=1)
    draw.line([(x + 4, y + 12), (x + 9, y + 12)], fill=(255, 255, 255), width=1)


def draw_icon_bolt(draw: ImageDraw.ImageDraw, x: int, y: int, color):
    pts = [(x + 8, y), (x + 2, y + 9), (x + 7, y + 9), (x + 5, y + 16), (x + 13, y + 7), (x + 8, y + 7)]
    draw.polygon(pts, fill=color)


def draw_icon_check(draw: ImageDraw.ImageDraw, x: int, y: int, circle_color, tick_color=(15, 23, 42)):
    draw.ellipse([(x, y), (x + 16, y + 16)], fill=circle_color)
    draw.line([(x + 4, y + 8), (x + 7, y + 11), (x + 12, y + 5)], fill=tick_color, width=2)


def draw_linear_gradient(draw: ImageDraw.ImageDraw, width: int, height: int, start_color, end_color):
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    for y in range(height):
        ratio_y = y / height
        for x in range(0, width, 2):
            ratio_x = x / width
            blend = ratio_x * 0.4 + ratio_y * 0.6
            r = int(r1 + (r2 - r1) * blend)
            g = int(g1 + (g2 - g1) * blend)
            b = int(b1 + (b2 - b1) * blend)
            draw.line([(x, y), (x + 1, y)], fill=(r, g, b))


def draw_technical_grid(draw: ImageDraw.ImageDraw, width: int, height: int):
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48), width=1)
    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


# ---------------------------------------------------------------------------
# 1. Miniatura de Producto B2B estilo PERT/AMFE (1200 x 630 px + Cuadrada)
# ---------------------------------------------------------------------------

def draw_pulse_architecture_panel(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    w: int,
    h: int,
    font_small,
    font_bold,
    font_mono,
    lang: str = "es",
):
    """Panel analítico derecho mostrando el flujo 6 hojas, Kanban vivo y SEO por categoría."""
    is_es = (lang == "es")
    draw.rounded_rectangle(
        [(x0, y0), (x0 + w, y0 + h)],
        radius=14,
        fill=(15, 23, 42),
        outline=(51, 65, 85),
        width=2,
    )

    # Cabecera del panel
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR PULSE · 6 PESTAÑAS ENLAZADAS" if is_es else "PULSE ENGINE · 6 LINKED WORKSHEETS"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(45, 212, 191), font=font_bold)
    sub_panel = "INV-PULSE-1..8 · Excel 2016+" if is_es else "INV-PULSE-1..8 · Excel 2016+"
    sub_bbox = font_small.getbbox(sub_panel)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text((x0 + w - sub_w - 16, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # Sección 1: Pestañas codificadas + Kanban Vivo
    y_sec1 = y0 + 50
    lbl_sec1 = (
        "1. TABLERO KANBAN DINÁMICO Y PESTAÑAS TEMÁTICAS"
        if is_es else
        "1. LIVE AUTO-KANBAN & COLOR-CODED WORKSHEET TABS"
    )
    draw.text((x0 + 16, y_sec1), lbl_sec1, fill=(56, 189, 248), font=font_bold)

    # Píldoras de colores de pestaña (Azul, Esmeralda, Ámbar)
    tabs_y = y_sec1 + 24
    tab_pills = (
        [
            ("Instrucciones", (2, 132, 199)),
            ("Taxonomía", (2, 132, 199)),
            ("Activos", (5, 150, 105)),
            ("Kanban", (5, 150, 105)),
            ("Métricas", (5, 150, 105)),
            ("Dashboard", (217, 119, 6)),
        ]
        if is_es else
        [
            ("Instructions", (2, 132, 199)),
            ("Taxonomy", (2, 132, 199)),
            ("Assets", (5, 150, 105)),
            ("Kanban", (5, 150, 105)),
            ("Metrics", (5, 150, 105)),
            ("Dashboard", (217, 119, 6)),
        ]
    )
    tx = x0 + 16
    for t_name, t_col in tab_pills:
        tb = font_small.getbbox(t_name)
        tw = (tb[2] - tb[0]) + 16
        draw.rounded_rectangle([(tx, tabs_y), (tx + tw, tabs_y + 24)], radius=4, fill=(22, 33, 52), outline=t_col, width=1)
        draw.rectangle([(tx + 3, tabs_y + 20), (tx + tw - 3, tabs_y + 22)], fill=t_col)
        draw.text((tx + 8, tabs_y + 4), t_name, fill=(241, 245, 249), font=font_small)
        tx += tw + 6

    # Mini columnas Kanban dinámicas
    kanban_y = tabs_y + 34
    stages = (
        [
            ("IDEA (1)", (100, 116, 139), ["Flujo Caja"]),
            ("DRAFT (1)", (245, 158, 11), ["Agentes IA"]),
            ("REVIEW (1)", (139, 92, 246), ["Prophet ML"]),
            ("SCHED (2)", (56, 189, 248), ["Pulse v1.0", "Helix Kit"]),
            ("LIVE (5)", (16, 185, 129), ["AMFE Riesgo", "Ada Lovelace"]),
        ]
        if is_es else
        [
            ("IDEA (1)", (100, 116, 139), ["SME Cash"]),
            ("DRAFT (1)", (245, 158, 11), ["AI Agents"]),
            ("REVIEW (1)", (139, 92, 246), ["Prophet ML"]),
            ("SCHED (2)", (56, 189, 248), ["Pulse v1.0", "Helix Kit"]),
            ("LIVE (5)", (16, 185, 129), ["FMEA Risk", "Ada Lovelace"]),
        ]
    )
    col_w = 100
    col_gap = 7
    for idx, (st_lbl, st_col, cards) in enumerate(stages):
        kx = x0 + 16 + idx * (col_w + col_gap)
        draw.rounded_rectangle([(kx, kanban_y), (kx + col_w, kanban_y + 106)], radius=6, fill=(20, 29, 47), outline=(41, 53, 72), width=1)
        draw.rounded_rectangle([(kx + 2, kanban_y + 2), (kx + col_w - 2, kanban_y + 22)], radius=4, fill=st_col)
        draw.text((kx + 8, kanban_y + 5), st_lbl, fill=(15, 23, 42) if st_col != (100, 116, 139) else (255, 255, 255), font=font_bold)
        cy = kanban_y + 29
        for card_txt in cards:
            draw.rounded_rectangle([(kx + 5, cy), (kx + col_w - 5, cy + 32)], radius=4, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
            draw.text((kx + 9, cy + 8), card_txt, fill=(226, 232, 240), font=font_small)
            cy += 37

    # Divider
    div_y = kanban_y + 120
    draw.line([(x0 + 16, div_y), (x0 + w - 16, div_y)], fill=(51, 65, 85), width=1)

    # Sección 2: Salud SEO & Paridad por Categoría Canónica
    y_sec2 = div_y + 12
    lbl_sec2 = (
        "2. SALUD SEO MEDIA & PARIDAD POR CATEGORÍA (MUESTRA 10 ACTIVOS)"
        if is_es else
        "2. CATEGORY SEO HEALTH & PARITY MATRIX (10 CURATED ASSETS)"
    )
    draw.text((x0 + 16, y_sec2), lbl_sec2, fill=(56, 189, 248), font=font_bold)

    cat_bars = (
        [
            ("IA, Ingeniería y Proyectos", 94, (16, 185, 129), "SEO 94 · Dual ES/EN"),
            ("Estrategia y Operaciones", 82, (56, 189, 248), "SEO 82 · Quick Win"),
            ("Startups & Growth", 91, (16, 185, 129), "SEO 91 · Live Parity"),
            ("Pioneros y Referentes", 88, (245, 158, 11), "SEO 88 · CTA Orphan"),
            ("Cultura Tech y Media", 85, (56, 189, 248), "SEO 85 · Complete"),
        ]
        if is_es else
        [
            ("AI, Engineering & Projects", 94, (16, 185, 129), "SEO 94 · Dual ES/EN"),
            ("Strategy & Operations", 82, (56, 189, 248), "SEO 82 · Quick Win"),
            ("Startups & Growth", 91, (16, 185, 129), "SEO 91 · Live Parity"),
            ("Pioneers & Icons", 88, (245, 158, 11), "SEO 88 · CTA Orphan"),
            ("Tech Culture & Media", 85, (56, 189, 248), "SEO 85 · Complete"),
        ]
    )
    bar_start_y = y_sec2 + 24
    max_bar_w = 185
    bx0 = x0 + 188
    bx_end = bx0 + max_bar_w

    for i, (cname, score, col, tag) in enumerate(cat_bars):
        by = bar_start_y + i * 28
        draw.text((x0 + 16, by + 2), cname, fill=(241, 245, 249), font=font_small)
        draw.rounded_rectangle([(bx0, by + 4), (bx_end, by + 16)], radius=3, fill=(30, 41, 59))
        fill_w = int((score / 100.0) * max_bar_w)
        draw.rounded_rectangle([(bx0, by + 4), (bx0 + fill_w, by + 16)], radius=3, fill=col)
        draw.text((bx_end + 12, by + 2), tag, fill=col, font=font_bold)

    # Divider
    div2_y = bar_start_y + 148
    draw.line([(x0 + 16, div2_y), (x0 + w - 16, div2_y)], fill=(51, 65, 85), width=1)

    # Sección 3: Veredicto Ejecutivo
    y_win = div2_y + 10
    draw.rounded_rectangle([(x0 + 16, y_win), (x0 + w - 16, y_win + 54)], radius=8, fill=(16, 46, 36), outline=(16, 185, 129), width=2)
    draw_icon_check(draw, x0 + 28, y_win + 10, (16, 185, 129))
    win_title = (
        "CERO DUPLICACIÓN MANUAL: ÍNDICE INDEX/MATCH EN VIVO"
        if is_es else
        "ZERO MANUAL DUPLICATION: LIVE INDEX/MATCH AUTOMATION"
    )
    draw.text((x0 + 52, y_win + 10), win_title, fill=(209, 250, 229), font=font_bold)
    win_sub = (
        "Pago único 19€ · Ahorra 1.800–3.600 € frente a Notion (TCO 3 años)"
        if is_es else
        "One-time 19€ license · Saves €1,800–€3,600 vs Notion (3-yr TCO)"
    )
    draw.text((x0 + 52, y_win + 30), win_sub, fill=(110, 231, 183), font=font_small)


def build_product_thumbnail(lang: str = "es", out_path: Path | None = None) -> Path:
    """Genera miniatura B2B 1200x630 px estilo PERT/AMFE en packages/pulse/."""
    is_es = (lang == "es")
    W, H = 1200, 630
    if out_path is None:
        fname = "Pulse_Kit_Thumbnail_ES.png" if is_es else "Pulse_Kit_Thumbnail_EN.png"
        out_path = PACKAGES_PULSE_DIR / fname
    out_path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_linear_gradient(draw, W, H, (15, 23, 42), (30, 41, 59))
    draw_technical_grid(draw, W, H)

    font_kicker = get_font(12, bold=True)
    font_title = get_font(31, bold=True)
    font_sub = get_font(16, bold=False)
    font_pill = get_font(13.5, bold=True)
    font_watermark = get_font(11.5, bold=True)
    font_bold = get_font(11.5, bold=True)
    font_small = get_font(10.5, bold=False)
    font_mono = get_font(10.5, bold=False)

    # Badge superior izquierda
    badge_text = (
        "DATALARIA CONTENT OPS KIT · EDICIÓN DUAL (ES/EN)"
        if is_es else
        "DATALARIA CONTENT OPS KIT · DUAL EDITION (ES/EN)"
    )
    b_box = font_kicker.getbbox(badge_text)
    badge_w = (b_box[2] - b_box[0]) + 28
    draw.rounded_rectangle([(56, 48), (56 + badge_w, 78)], radius=6, fill=(13, 148, 136), outline=(20, 184, 166), width=1)
    draw.text((70, 55), badge_text, fill=(255, 255, 255), font=font_kicker)

    # Título principal
    line1 = "DATALARIA PULSE"
    line2 = "CONTENT OPS & NOTION KIT" if is_es else "& NOTION MIGRATION KIT"
    sub1 = (
        "Excel Automatizado (6 Hojas), Conectores Power Query M"
        if is_es else
        "Automated 6-Sheet Excel, Dual Power Query M Connectors"
    )
    sub2 = (
        "y Escáner Git en Python (Sin Suscripciones)"
        if is_es else
        "& Zero-Dependency Python Scanner (Zero Subscriptions)"
    )

    draw.text((56, 102), line1, fill=(255, 255, 255), font=font_title)
    draw.text((56, 144), line2, fill=(56, 189, 248), font=font_title)
    draw.text((56, 202), sub1, fill=(203, 213, 225), font=font_sub)
    draw.text((56, 228), sub2, fill=(148, 163, 184), font=font_sub)

    # Píldoras de entregables con iconos vectoriales
    pills = (
        [
            ("Excel (.xlsx) + Sheets · Dual ES/EN", (37, 99, 235), draw_icon_excel),
            ("Power Query M + Scripts Python CLI", (13, 148, 136), draw_icon_cli),
            ("Guía Ejecutiva PDF (5 Páginas A4)", (220, 38, 38), draw_icon_pdf),
        ]
        if is_es else
        [
            ("Excel (.xlsx) + Sheets · Dual ES/EN", (37, 99, 235), draw_icon_excel),
            ("Power Query M + Python CLI Tools", (13, 148, 136), draw_icon_cli),
            ("Executive PDF Guide (5 Pages A4)", (220, 38, 38), draw_icon_pdf),
        ]
    )
    py = 286
    for text, col, icon_fn in pills:
        draw.rounded_rectangle([(56, py), (420, py + 38)], radius=6, fill=(15, 23, 42), outline=col, width=2)
        icon_fn(draw, 70, py + 11, col)
        draw.text((96, py + 9), text, fill=(241, 245, 249), font=font_pill)
        py += 50

    # Tarjeta de descarga instantánea
    draw.rounded_rectangle([(56, 456), (554, 514)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw_icon_bolt(draw, 70, 476, (245, 158, 11))
    tag_txt = (
        "Descarga inmediata (.ZIP) | Tablas Nativas y Filtros | Sin Macros VBA"
        if is_es else
        "Instant .ZIP Download | Native Tables & AutoFilters | Zero VBA"
    )
    draw.text((92, 477), tag_txt, fill=(226, 232, 240), font=font_small)

    # Watermark inferior
    draw.text((56, 558), "DATALARIA.COM · CONTENT OPS AS CODE · DUAL EDITION (ES/EN)", fill=(100, 116, 139), font=font_watermark)

    # Panel derecho
    draw_pulse_architecture_panel(
        draw, x0=584, y0=48, w=560, h=534,
        font_small=font_small, font_bold=font_bold, font_mono=font_mono, lang=lang
    )

    img.save(out_path, format="PNG", optimize=True)
    size_kb = round(out_path.stat().st_size / 1024, 1)
    print(f"[THUMBNAIL] Generada miniatura ({lang.upper()}): {out_path.name} ({W}x{H} px, {size_kb} KB)")
    return out_path


def build_lemon_checkout_4x3(out_path: Path) -> Path:
    """
    Genera imagen nativa 4:3 (1200x900 px) optimizada para el modal de Checkout
    de Lemon Squeezy (sin recortes laterales ni solapamiento del logo circular inferior).
    """
    W, H = 1200, 900
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_linear_gradient(draw, W, H, (11, 17, 32), (17, 24, 39))
    draw_technical_grid(draw, W, H)

    # Franja superior emerald -> cyan
    draw.rectangle([(0, 0), (W, 6)], fill=(16, 185, 129))

    font_kicker = get_font(16, bold=True)
    font_title = get_font(46, bold=True)
    font_sub = get_font(20, bold=False)
    font_pill = get_font(17, bold=True)
    font_small = get_font(14, bold=False)
    font_bold = get_font(15, bold=True)
    font_mono = get_font(13, bold=False)

    # Cabecera centrada / segura en ancho completo [x=64..1136, y=42..290]
    badge_text = "DATALARIA CONTENT OPS KIT  |  DUAL EDITION (ES / EN)"
    b_box = font_kicker.getbbox(badge_text)
    badge_w = (b_box[2] - b_box[0]) + 36
    draw.rounded_rectangle([(64, 42), (64 + badge_w, 78)], radius=8, fill=(13, 148, 136), outline=(52, 211, 153), width=1)
    draw.text((82, 51), badge_text, fill=(255, 255, 255), font=font_kicker)

    # Sello precio derecha en cabecera
    price_txt = "EARLY-BIRD 19€  |  ONE-TIME"
    p_box = font_kicker.getbbox(price_txt)
    p_w = (p_box[2] - p_box[0]) + 32
    draw.rounded_rectangle([(W - 64 - p_w, 42), (W - 64, 78)], radius=8, fill=(6, 78, 59), outline=(16, 185, 129), width=1)
    draw.text((W - 64 - p_w + 16, 51), price_txt, fill=(167, 243, 208), font=font_kicker)

    draw.text((64, 102), "DATALARIA PULSE", fill=(255, 255, 255), font=font_title)
    draw.text((64, 156), "& NOTION MIGRATION KIT", fill=(56, 189, 248), font=font_title)
    draw.text((64, 218), "Automated 6-Sheet Excel (ES/EN), Power Query M Connectors & Zero-Dep CLI", fill=(203, 213, 225), font=font_sub)

    # Bloque izquierdo: Entregables con iconos vectoriales [x=64..536, y=278..738]
    pills = [
        ("Excel Workbooks (6 Sheets ES/EN)", (37, 99, 235), draw_icon_excel),
        ("Power Query M + Python CLI Tools", (13, 148, 136), draw_icon_cli),
        ("Executive PDF Guide (5 Pages A4)", (220, 38, 38), draw_icon_pdf),
    ]
    py = 282
    for text, col, icon_fn in pills:
        draw.rounded_rectangle([(64, py), (532, py + 62)], radius=10, fill=(15, 23, 42), outline=col, width=2)
        icon_fn(draw, 84, py + 23, col)
        draw.text((116, py + 20), text, fill=(241, 245, 249), font=font_pill)
        py += 80

    # Tarjeta resumen abajo izquierda [y=534..658] + banda métricas [y=674..776]
    draw.rounded_rectangle([(64, 534), (532, 658)], radius=10, fill=(17, 24, 39), outline=(51, 65, 85), width=1)
    draw_icon_bolt(draw, 82, 554, (245, 158, 11))
    draw.text((108, 552), "Instant .ZIP Download · Zero VBA", fill=(248, 250, 252), font=font_bold)
    draw.text((82, 584), "Excel 2016/365 & Google Sheets ready.", fill=(148, 163, 184), font=font_small)
    draw.text((82, 610), "Includes 10-asset Notion sample + RLS docs.", fill=(148, 163, 184), font=font_small)

    kpis_left = [("6 Sheets", "Linked Formulas"), ("Dual ES/EN", "Full Packs"), ("3.6k€ ROI", "vs SaaS")]
    for idx_k, (k_val, k_lbl) in enumerate(kpis_left):
        kx = 64 + idx_k * 160
        draw.rounded_rectangle([(kx, 676), (kx + 148, 776)], radius=10, fill=(15, 23, 42), outline=(16, 185, 129), width=1)
        draw.text((kx + 16, 696), k_val, fill=(52, 211, 153), font=font_pill)
        draw.text((kx + 16, 732), k_lbl, fill=(148, 163, 184), font=font_small)

    # Panel derecho: Arquitectura Pulse compacta [x=560..1136, y=282..776]
    draw_pulse_architecture_panel(
        draw, x0=560, y0=282, w=576, h=494,
        font_small=font_small, font_bold=font_bold, font_mono=font_mono, lang="en"
    )

    # Zona inferior [y=748..900] despejada en el centro para el logo circular de Lemon Squeezy
    draw.text((64, 836), "DATALARIA.COM", fill=(100, 116, 139), font=font_small)
    r_txt = "CONTENT OPS AS CODE"
    rb = font_small.getbbox(r_txt)
    draw.text((W - 64 - (rb[2] - rb[0]), 836), r_txt, fill=(16, 185, 129), font=font_small)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    size_kb = round(out_path.stat().st_size / 1024, 1)
    print(f"[THUMBNAIL 4:3] Generada miniatura checkout 4:3: {out_path.name} ({W}x{H} px, {size_kb} KB)")
    return out_path


def build_square_thumbnail(checkout_4x3_path: Path, out_path: Path) -> Path:
    """Genera variante cuadrada 1200x1200 px centrando la composición 4:3 con margen seguro."""
    S = 1200
    sq = Image.new("RGB", (S, S), (11, 17, 32))
    draw = ImageDraw.Draw(sq)
    draw_technical_grid(draw, S, S)

    src = Image.open(checkout_4x3_path).convert("RGB")
    target_w = 1120
    target_h = int(src.height * (target_w / src.width))  # 840 px
    resized = src.resize((target_w, target_h), Image.Resampling.LANCZOS)

    x_off = (S - target_w) // 2
    y_off = (S - target_h) // 2
    draw.rounded_rectangle(
        [(x_off - 3, y_off - 3), (x_off + target_w + 3, y_off + target_h + 3)],
        radius=12,
        outline=(16, 185, 129),
        width=2,
    )
    sq.paste(resized, (x_off, y_off))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sq.save(out_path, format="PNG", optimize=True)
    size_kb = round(out_path.stat().st_size / 1024, 1)
    print(f"[THUMBNAIL SQ] Generada miniatura cuadrada: {out_path.name} ({S}x{S} px, {size_kb} KB)")
    return out_path


# ---------------------------------------------------------------------------
# 2. Previews 1600x980 px del Catálogo / Recursos y Posts (PDF real 5 págs)
# ---------------------------------------------------------------------------

def render_pdf_page(doc, page_num: int, target_height: int) -> Image.Image:
    page = doc[page_num]
    zoom = (target_height / page.rect.height) * 1.5
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    aspect = img.width / img.height
    target_width = int(target_height * aspect)
    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)


def add_drop_shadow(base_img: Image.Image, element: Image.Image, x: int, y: int, shadow_offset: int = 14, border_color=(16, 185, 129)):
    shadow_box = Image.new("RGBA", (element.width + shadow_offset * 2, element.height + shadow_offset * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_box)
    sdraw.rectangle([shadow_offset, shadow_offset, shadow_box.width - 2, shadow_box.height - 2], fill=(0, 0, 0, 160))
    base_img.paste(shadow_box, (x - shadow_offset // 2, y - shadow_offset // 2), mask=shadow_box)

    elem_with_border = element.copy().convert("RGBA")
    edraw = ImageDraw.Draw(elem_with_border)
    edraw.rectangle([0, 0, elem_with_border.width - 1, elem_with_border.height - 1], outline=border_color, width=2)
    base_img.paste(elem_with_border, (x, y))


def build_preview(lang: str = "es") -> Path:
    """Genera la imagen de previsualización 1600x980 px para el catálogo web y artículos."""
    is_es = (lang == "es")
    WIDTH, HEIGHT = 1600, 980
    RECURSOS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RECURSOS_IMAGES_DIR / f"pulse-preview-{lang}.png"

    img = Image.new("RGB", (WIDTH, HEIGHT), color="#0b0f17")
    draw = ImageDraw.Draw(img)

    for r in range(500, 0, -10):
        alpha = int(18 * (1 - r / 500))
        draw.ellipse([800 - r, 490 - r, 800 + r, 490 + r], fill=(16, int(24 + alpha * 0.8), int(39 + alpha)))

    for y in range(0, HEIGHT, 70):
        draw.line([(0, y), (WIDTH, y)], fill=(17, 24, 39), width=1)
    for x in range(0, WIDTH, 100):
        draw.line([(x, 0), (x, HEIGHT)], fill=(17, 24, 39), width=1)

    draw.rectangle([16, 16, WIDTH - 17, HEIGHT - 17], outline=(30, 41, 59), width=2)
    draw.rectangle([20, 20, WIDTH - 21, HEIGHT - 21], outline=(16, 185, 129), width=1)

    f_badge = get_font(17, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(21, bold=False)
    f_item_title = get_font(20, bold=True)
    f_item_desc = get_font(15, bold=False)
    f_kpi_num = get_font(25, bold=True)
    f_kpi_lbl = get_font(13, bold=False)
    f_price_badge = get_font(22, bold=True)

    if is_es:
        badge_text = "KIT COMERCIAL B2B · EDICIÓN DUAL ES/EN · 19€"
        title_text = "Datalaria Pulse Content Ops Kit"
        sub_text = "Excel Automatizado (6 Hojas), Power Query M Dual y Scripts CLI"
        features = [
            ("01. Plantillas Excel Duales (.xlsx)", "Tablas nativas con filtros, colores temáticos, Kanban vivo e INDEX/MATCH"),
            ("02. Conectores Power Query M (ES/EN)", "Sincronización en 1 clic desde Notion CSV y public.json de Git"),
            ("03. Migrador y Escáner CLI en Python", "0 dependencias externas, soporte --lang es/en y 10 activos de muestra"),
            ("04. Guías Ejecutivas PDF (5 Páginas)", "Manuales maquetados ES y EN con Caso de Uso completo e INV-PULSE-1..8"),
        ]
        kpi_items = [
            ("19€", "Licencia Única Perpetua"),
            ("Dual ES/EN", "Dos Árboles Completos"),
            ("6 Hojas", "Excel Sin Duplicación"),
            ("100%", "Soberanía Git Local"),
        ]
        price_txt = "19€  ·  LANZAMIENTO EARLY-BIRD (PVP: 39€)"
        pdf_badge = "GUIA_EJECUTIVA_PULSE_ES.pdf (5 Páginas A4)"
        footer_left = "datalaria.com/es/recursos/#pack-pulse · Compatible Excel 2016+/365 & Sheets"
        footer_right = "Compra Única Perpetua · Cero Suscripciones"
        pdf_source = PDF_ES_PATH
    else:
        badge_text = "B2B COMMERCIAL KIT · DUAL EDITION ES/EN · 19€"
        title_text = "Datalaria Pulse Content Ops Kit"
        sub_text = "Automated 6-Sheet Excel, Dual Power Query M & Python CLI Tools"
        features = [
            ("01. Dual Excel Workbooks (.xlsx)", "Native AutoFilter tables, colored tabs, live Kanban & INDEX/MATCH"),
            ("02. Dual Power Query M Connectors", "1-click sync from Notion CSV exports and Git public.json manifests"),
            ("03. Python CLI Migration & Scanner", "Zero external dependencies, --lang es/en flags & 10 curated sample assets"),
            ("04. Executive PDF Guides (5 Pages A4)", "Formatted ES & EN handbooks with full Scriba Use Case & INV-PULSE-1..8"),
        ]
        kpi_items = [
            ("19€", "One-Time Perpetual"),
            ("Dual ES/EN", "Full Isolated Trees"),
            ("6 Sheets", "Zero Duplication"),
            ("100%", "Local Data Ownership"),
        ]
        price_txt = "19€  ·  EARLY-BIRD LAUNCH (Reg: 39€)"
        pdf_badge = "PULSE_EXECUTIVE_GUIDE_EN.pdf (5 Pages A4)"
        footer_left = "datalaria.com/en/resources/#pack-pulse · Excel 2016+/365 & Google Sheets"
        footer_right = "Buy Once, Own Forever · Zero Recurring Fees"
        pdf_source = PDF_EN_PATH

    # Badge superior ajustado al texto
    b_box = f_badge.getbbox(badge_text)
    draw.rounded_rectangle([70, 56, 70 + (b_box[2] - b_box[0]) + 36, 94], radius=8, fill=(16, 185, 129), outline=(5, 150, 105), width=1)
    draw.text((88, 64), badge_text, fill=(11, 15, 23), font=f_badge)

    draw.text((70, 114), title_text, fill=(249, 250, 251), font=f_title)
    draw.text((70, 174), sub_text, fill=(156, 163, 175), font=f_sub)

    y_start = 240
    for i, (feat_title, feat_desc) in enumerate(features):
        box_y = y_start + i * 92
        draw.rounded_rectangle([70, box_y, 790, box_y + 78], radius=8, fill=(17, 24, 39), outline=(51, 65, 85), width=1)
        draw_icon_check(draw, 88, box_y + 21, (16, 185, 129), tick_color=(255, 255, 255))
        draw.text((120, box_y + 14), feat_title, fill=(249, 250, 251), font=f_item_title)
        draw.text((120, box_y + 44), feat_desc, fill=(156, 163, 175), font=f_item_desc)

    kpi_y = 636
    for k_idx, (num, lbl) in enumerate(kpi_items):
        kx = 70 + k_idx * 184
        draw.rounded_rectangle([kx, kpi_y, kx + 174, kpi_y + 88], radius=8, fill=(15, 23, 42), outline=(16, 185, 129), width=1)
        draw.text((kx + 14, kpi_y + 12), num, fill=(16, 185, 129), font=f_kpi_num)
        draw.text((kx + 14, kpi_y + 54), lbl, fill=(148, 163, 184), font=f_kpi_lbl)

    # Sello precio ajustado dinámicamente al texto (sin desbordamiento)
    p_box = f_price_badge.getbbox(price_txt)
    pw = (p_box[2] - p_box[0]) + 64
    draw.rounded_rectangle([70, 752, 70 + pw, 812], radius=10, fill=(16, 185, 129), outline=(5, 150, 105), width=2)
    draw_icon_bolt(draw, 88, 774, (11, 15, 23))
    draw.text((112, 769), price_txt, fill=(11, 15, 23), font=f_price_badge)

    if fitz and pdf_source.exists():
        try:
            doc = fitz.open(pdf_source)
            p1_img = render_pdf_page(doc, 0, target_height=630)
            p2_img = render_pdf_page(doc, 1, target_height=540) if len(doc) > 1 else None
            if p2_img:
                add_drop_shadow(img, p2_img, x=1110, y=145, shadow_offset=18, border_color=(6, 182, 212))
            add_drop_shadow(img, p1_img, x=845, y=110, shadow_offset=22, border_color=(16, 185, 129))

            pb_box = f_badge.getbbox(pdf_badge)
            pb_w = (pb_box[2] - pb_box[0]) + 54
            pb_x = 845
            draw.rounded_rectangle([pb_x, 776, pb_x + pb_w, 822], radius=8, fill=(17, 24, 39), outline=(16, 185, 129), width=1)
            draw_icon_pdf(draw, pb_x + 14, 791, (220, 38, 38))
            draw.text((pb_x + 38, 789), pdf_badge, fill=(249, 250, 251), font=f_badge)
            doc.close()
        except Exception as e:
            print(f"[WARN] Error renderizando PDF {pdf_source}: {e}")

    f_footer = get_font(15, bold=False)
    draw.line([(70, 890), (WIDTH - 70, 890)], fill=(51, 65, 85), width=1)
    draw.text((70, 915), footer_left, fill=(148, 163, 184), font=f_footer)
    fr_box = f_footer.getbbox(footer_right)
    draw.text((WIDTH - 70 - (fr_box[2] - fr_box[0]), 915), footer_right, fill=(16, 185, 129), font=f_footer)

    img.save(out_path, format="PNG", optimize=True)
    size_kb = round(out_path.stat().st_size / 1024, 1)
    print(f"[PREVIEW] Generada imagen {out_path.name} ({WIDTH}x{HEIGHT} px, {size_kb} KB)")
    return out_path


def main():
    print("[PREVIEW BUILDER] Generando miniaturas Lemon Squeezy y vistas previas 1600x980 para Datalaria Pulse Kit...")
    thumb_es = build_product_thumbnail("es", PACKAGES_PULSE_DIR / "Pulse_Kit_Thumbnail_ES.png")
    thumb_en = build_product_thumbnail("en", PACKAGES_PULSE_DIR / "Pulse_Kit_Thumbnail_EN.png")

    LEMON_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(thumb_en, LEMON_IMAGES_DIR / "Pulse.png")
    checkout_4x3 = build_lemon_checkout_4x3(PACKAGES_PULSE_DIR / "Pulse_Kit_LemonSqueezy_Checkout.png")
    shutil.copy2(checkout_4x3, LEMON_IMAGES_DIR / "Pulse_Checkout_4x3.png")
    build_square_thumbnail(checkout_4x3, LEMON_SQUARE_DIR / "Pulse.png")

    prev_es = build_preview("es")
    prev_en = build_preview("en")

    # Sincronizar copias en Parte 1 y Parte 5
    sync_targets = [
        (prev_es, ROOT_DIR / "content" / "es" / "posts" / "pulse-parte1-adios-notion-content-ops" / "pulse-preview-es.png"),
        (prev_es, ROOT_DIR / "content" / "es" / "posts" / "pulse-parte5-kit-excel-migracion-notion-equipos" / "pulse-preview-es.png"),
        (prev_en, ROOT_DIR / "content" / "en" / "posts" / "pulse-part1-goodbye-notion-content-ops" / "pulse-preview-en.png"),
        (prev_en, ROOT_DIR / "content" / "en" / "posts" / "pulse-part5-excel-kit-notion-migration-teams" / "pulse-preview-en.png"),
    ]
    for src, dst in sync_targets:
        if dst.parent.exists():
            shutil.copy2(src, dst)
            print(f"[SYNC] Copiado a {dst.relative_to(ROOT_DIR)}")

    print("\n[OK] Todas las miniaturas y previews generadas con éxito.")


if __name__ == "__main__":
    main()
