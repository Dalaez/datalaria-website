# -*- coding: utf-8 -*-
"""ops/obs_kit/visuals_builder.py — Generador determinista de previews 1600x980 y portadas 1200x750/1200x630/1080x1080.

Cumple b2b-kit-factory SKILL:
- Previews compuestas reales 1600x980 en static/images/recursos/obs-preview-{es,en}.png
  combinando captura real del Executive Risk Cockpit v2.0 + páginas reales renderizadas del PDF de 5 págs.
- Portadas de tienda 1200x750 (16:10 Safe Zone [145, 1055]), 1200x630 y 1080x1080 en
  packages/00_DISTRIBUCION_LEMONSQUEEZY/Images/ e Images_Square/.
- Cero glifos rotos (□): iconografía 100% vectorial Pillow.
"""

from __future__ import annotations

import io
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

BG_DARK = (11, 15, 23)        # #0b0f17
CARD_DARK = (17, 24, 39)      # #111827
BORDER_DARK = (37, 51, 76)    # #25334c
CYAN = (14, 165, 233)         # #0ea5e9
VIOLET = (139, 92, 246)       # #8b5cf6
EMERALD = (16, 185, 129)      # #10b981
AMBER = (245, 158, 11)        # #f59e0b
WHITE = (248, 250, 252)       # #f8fafc
MUTED = (180, 194, 212)


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"]
        if bold
        else ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"]
    )
    for name in names:
        for candidate in (Path(r"C:\Windows\Fonts") / name, Path("/usr/share/fonts/truetype/dejavu") / name, Path(name)):
            try:
                return ImageFont.truetype(str(candidate), int(size))
            except OSError:
                continue
    return ImageFont.load_default()


def _render_pdf_page(pdf_path: Path, page_idx: int, target_w: int) -> Image.Image:
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_idx)
    scale = target_w / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    doc.close()
    return img


def _draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, bg: tuple, fg: tuple, font) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 14, 7
    draw.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y], radius=8, fill=bg)
    draw.text((x + pad_x, y + pad_y - 2), text, fill=fg, font=font)
    return x + tw + 2 * pad_x + 12


def _draw_radar_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CARD_DARK, outline=CYAN, width=3)
    draw.ellipse([cx - int(r * 0.65), cy - int(r * 0.65), cx + int(r * 0.65), cy + int(r * 0.65)], outline=BORDER_DARK, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=BORDER_DARK, width=1)
    draw.line([cx, cy - r, cx, cy + r], fill=BORDER_DARK, width=1)
    draw.line([cx, cy, cx + int(r * 0.72), cy - int(r * 0.64)], fill=WHITE, width=3)
    draw.ellipse([cx + int(r * 0.42) - 5, cy - int(r * 0.22) - 5, cx + int(r * 0.42) + 5, cy - int(r * 0.22) + 5], fill=AMBER)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=CYAN)


def build_composite_preview_1600x980(
    lang: str, pdf_path: Path, cockpit_cover_path: Path, output_path: Path
) -> Path:
    """Genera previsualización compuesta 1600x980 px para el catálogo /recursos/."""
    w, h = 1600, 980
    canvas = Image.new("RGB", (w, h), BG_DARK)
    draw = ImageDraw.Draw(canvas)

    # Top accent bar & header band
    draw.rectangle([0, 0, w, 8], fill=CYAN)
    draw.rectangle([0, 8, w, 152], fill=CARD_DARK)
    draw.line([0, 152, w, 152], fill=BORDER_DARK, width=2)

    _draw_radar_icon(draw, 72, 80, 32)
    f_title = _get_font(34, bold=True)
    f_sub = _get_font(19, bold=False)
    f_badge = _get_font(16, bold=True)
    f_card_t = _get_font(18, bold=True)
    f_card_b = _get_font(15, bold=False)

    if lang == "es":
        title = "IEC 62402 Obsolescencia, Riesgo BOM & LTB Decision Kit"
        sub = "Motor Excel Dual 5 Hojas (0 VBA) · Playbook PDF 5 Págs · Starter Blueprint PostgreSQL RLS & Python"
        b1, b2, b3 = "LANZAMIENTO 09 DIC · 19 €", "EDICIÓN DUAL ES / EN", "COMPLEMENTO DE PACK-STOCK"
        lbl_left = "1. EXECUTIVE RISK COCKPIT v2.0 + PLANTILLA CSV LOCAL"
        lbl_right = "2. PLAYBOOK EJECUTIVO PDF (5 PÁGS.) + EXCEL 5 HOJAS"
        footer_bullets = [
            "01_BOM_AML_EXPLORER + 02_IEC62402_CRITICALITY (0-100)",
            "03_LTB_VS_FFF_SIMULATOR (WACC + SS_LTB tras congelar ROP)",
            "03_STARTER_BLUEPRINT: obs_radar RLS SQL + bom_engine.py",
        ]
    else:
        title = "IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit"
        sub = "5-Sheet Dual Excel Engine (0 VBA) · 5-Page Executive PDF Playbook · PostgreSQL RLS & Python Blueprint"
        b1, b2, b3 = "LAUNCH DEC 09 · EUR 19", "DUAL EDITION ES / EN", "PAIRS WITH PACK-STOCK"
        lbl_left = "1. EXECUTIVE RISK COCKPIT v2.0 + LOCAL CSV TEMPLATE"
        lbl_right = "2. EXECUTIVE PDF PLAYBOOK (5 PAGES) + 5-SHEET EXCEL"
        footer_bullets = [
            "01_BOM_AML_EXPLORER + 02_IEC62402_CRITICALITY (0-100)",
            "03_LTB_VS_FFF_SIMULATOR (WACC + SS_LTB after freezing ROP)",
            "03_STARTER_BLUEPRINT: obs_radar RLS SQL + bom_engine.py",
        ]

    draw.text((124, 28), title, fill=WHITE, font=f_title)
    draw.text((124, 74), sub, fill=MUTED, font=f_sub)
    nx = _draw_badge(draw, 124, 106, b1, CYAN, BG_DARK, f_badge)
    nx = _draw_badge(draw, nx, 106, b2, VIOLET, WHITE, f_badge)
    _draw_badge(draw, nx, 106, b3, EMERALD, BG_DARK, f_badge)

    # Left panel: Real Cockpit v2.0 screenshot
    draw.text((48, 174), lbl_left, fill=CYAN, font=f_card_t)
    draw.rounded_rectangle([44, 206, 868, 740], radius=14, fill=CARD_DARK, outline=CYAN, width=2)
    if cockpit_cover_path.exists():
        shot = Image.open(cockpit_cover_path).convert("RGB").resize((804, 502), Image.Resampling.LANCZOS)
        canvas.paste(shot, (54, 222))

    # Right panel: Real PDF Page 1 & Page 4 side by side
    draw.text((902, 174), lbl_right, fill=VIOLET, font=f_card_t)
    draw.rounded_rectangle([898, 206, 1556, 740], radius=14, fill=CARD_DARK, outline=VIOLET, width=2)
    p1_img = _render_pdf_page(pdf_path, 0, 304)
    p4_img = _render_pdf_page(pdf_path, 3, 304)
    p1_img = p1_img.resize((304, 430), Image.Resampling.LANCZOS)
    p4_img = p4_img.resize((304, 430), Image.Resampling.LANCZOS)
    canvas.paste(p1_img, (916, 232))
    canvas.paste(p4_img, (1236, 232))
    draw.text((916, 678), "Pág. 1 · Portada & Arquitectura" if lang == "es" else "Page 1 · Cover & Architecture", fill=MUTED, font=f_card_b)
    draw.text((1236, 678), "Pág. 4 · Sinergia ROP vs. LTB" if lang == "es" else "Page 4 · ROP vs. LTB Synergy", fill=MUTED, font=f_card_b)

    # Bottom deliverables strip (3 cards)
    card_w = 488
    for idx, btxt in enumerate(footer_bullets):
        bx = 44 + idx * (card_w + 24)
        draw.rounded_rectangle([bx, 768, bx + card_w, 932], radius=12, fill=CARD_DARK, outline=BORDER_DARK, width=2)
        dot_color = CYAN if idx == 0 else (VIOLET if idx == 1 else EMERALD)
        draw.ellipse([bx + 20, 796, bx + 38, 814], fill=dot_color)
        draw.text((bx + 50, 792), f"ENTREGABLE 0{idx + 1}" if lang == "es" else f"DELIVERABLE 0{idx + 1}", fill=dot_color, font=f_badge)
        draw.text((bx + 20, 834), btxt, fill=WHITE, font=f_card_b)
        extra = (
            "100% formulas nativas auditadas · 0 VBA" if idx == 0 else (
                "Cero solapamiento con pack-stock (7 EUR)" if idx == 1 else "Listo para importar en Agentic Radar v2.0"
            )
        ) if lang == "es" else (
            "100% audited native formulas · 0 VBA" if idx == 0 else (
                "Zero overlap with pack-stock (EUR 7)" if idx == 1 else "Ready to import in Agentic Radar v2.0"
            )
        )
        draw.text((bx + 20, 868), extra, fill=MUTED, font=f_card_b)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)
    return output_path


def build_store_cover(
    lang: str, width: int, height: int, pdf_path: Path, cockpit_cover_path: Path, output_path: Path
) -> Path:
    """Genera portada comercial 1200x750 (Safe Zone [145, 1055]), 1200x630 o 1080x1080."""
    canvas = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, width, 10], fill=CYAN)

    # Safe Zone boundaries for 1200x750: x in [145, 1055]
    safe_x0 = 152 if width == 1200 else 64
    safe_x1 = width - safe_x0

    f_kicker = _get_font(17 if width == 1200 else 20, bold=True)
    f_title = _get_font(38 if width == 1200 else 44, bold=True)
    f_sub = _get_font(18 if width == 1200 else 22, bold=False)
    f_badge = _get_font(15 if width == 1200 else 18, bold=True)

    _draw_radar_icon(draw, safe_x0 + 26, 74, 24)
    kicker = "DATALARIA B2B KIT · NORMA IEC 62402" if lang == "es" else "DATALARIA B2B KIT · IEC 62402 STANDARD"
    draw.text((safe_x0 + 66, 62), kicker, fill=CYAN, font=f_kicker)

    title_lines = (
        ["Obsolescencia, Riesgo BOM", "& Decisión Last Time Buy (LTB)"]
        if lang == "es"
        else ["Obsolescence, BOM Risk", "& Last Time Buy (LTB) Kit"]
    )
    ty = 114
    for line in title_lines:
        draw.text((safe_x0, ty), line, fill=WHITE, font=f_title)
        ty += 48 if width == 1200 else 56

    sub_txt = (
        "Excel Dual 5 Hojas + Playbook PDF 5 Págs. + Blueprint PostgreSQL RLS"
        if lang == "es"
        else "5-Sheet Dual Excel + 5-Page PDF Playbook + PostgreSQL RLS Blueprint"
    )
    draw.text((safe_x0, ty + 6), sub_txt, fill=MUTED, font=f_sub)

    bx = _draw_badge(draw, safe_x0, ty + 42, "19 € EARLY-BIRD" if lang == "es" else "€19 EARLY-BIRD", CYAN, BG_DARK, f_badge)
    bx = _draw_badge(draw, bx, ty + 42, "DUAL ES / EN", VIOLET, WHITE, f_badge)
    _draw_badge(draw, bx, ty + 42, "0 MACROS VBA", EMERALD, BG_DARK, f_badge)

    # Embedded real visual cards inside Safe Zone
    vis_y = ty + 98
    avail_h = height - vis_y - 36
    avail_w = safe_x1 - safe_x0
    left_w = int(avail_w * 0.62)
    right_w = avail_w - left_w - 22

    draw.rounded_rectangle([safe_x0, vis_y, safe_x0 + left_w, vis_y + avail_h], radius=12, fill=CARD_DARK, outline=CYAN, width=2)
    if cockpit_cover_path.exists():
        shot = Image.open(cockpit_cover_path).convert("RGB").resize((left_w - 16, avail_h - 16), Image.Resampling.LANCZOS)
        canvas.paste(shot, (safe_x0 + 8, vis_y + 8))

    pdf_x = safe_x0 + left_w + 22
    draw.rounded_rectangle([pdf_x, vis_y, pdf_x + right_w, vis_y + avail_h], radius=12, fill=CARD_DARK, outline=VIOLET, width=2)
    p1_img = _render_pdf_page(pdf_path, 0, right_w - 16).resize((right_w - 16, avail_h - 16), Image.Resampling.LANCZOS)
    canvas.paste(p1_img, (pdf_x + 8, vis_y + 8))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)
    return output_path
