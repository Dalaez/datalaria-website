#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Mega Bundle Suite 01: Estrategia Corporativa & MBA en español e inglés:
- static/images/recursos/suite-01-preview-es.png
- static/images/recursos/suite-01-preview-en.png
- content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/preview-pack.png
- content/en/posts/corporate-strategy-mba-quantitative-framework/preview-pack.png

Integra capturas reales de alta resolución de los 5 Executive Decision Packs
individuales (PESTEL, 5 Fuerzas de Porter, DAFO-CAME, BCG Dinámica y McKinsey/GE 3x3)
en el estándar visual Dark-Slate Tier-1 (1600x980 px).
"""

import os
from PIL import Image, ImageDraw, ImageFont


def get_font(size, bold=False):
    font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
    alt_name = "arialbd.ttf" if bold else "arial.ttf"
    path = os.path.join(r"C:\Windows\Fonts", font_name)
    if os.path.exists(path):
        return ImageFont.truetype(path, int(size))
    alt_path = os.path.join(r"C:\Windows\Fonts", alt_name)
    if os.path.exists(alt_path):
        return ImageFont.truetype(alt_path, int(size))
    return ImageFont.load_default()


def draw_window_header(draw, x, y, w, h, title, bg_color, font, price_badge=None, f_badge=None):
    draw.rounded_rectangle([x, y, x + w, y + h + 8], radius=8, fill=bg_color)
    draw.rectangle([x, y + h - 4, x + w, y + h], fill=bg_color)
    # macOS traffic lights
    r = 4
    cy = y + h // 2
    draw.ellipse([x + 12 - r, cy - r, x + 12 + r, cy + r], fill=(255, 95, 86))
    draw.ellipse([x + 26 - r, cy - r, x + 26 + r, cy + r], fill=(255, 189, 46))
    draw.ellipse([x + 40 - r, cy - r, x + 40 + r, cy + r], fill=(39, 201, 63))
    # Title
    bbox = font.getbbox(title)
    th = bbox[3] - bbox[1]
    draw.text((x + 54, cy - th // 2 - 2), title, font=font, fill=(255, 255, 255))
    # Optional price pill on right of header
    if price_badge and f_badge:
        pb_box = f_badge.getbbox(price_badge)
        pw = pb_box[2] - pb_box[0] + 14
        draw.rounded_rectangle([x + w - pw - 8, y + 5, x + w - 8, y + h - 5], radius=4, fill=(15, 23, 42))
        draw.text((x + w - pw - 1, y + 7), price_badge, font=f_badge, fill=(52, 211, 153))


def generate_preview_suite01(lang="es"):
    is_es = (lang == "es")
    W, H = 1600, 980
    im = Image.new("RGB", (W, H), (11, 17, 32))  # Deep Slate Navy #0B1120
    draw = ImageDraw.Draw(im)

    # Outer frame border
    draw.rounded_rectangle([15, 15, W - 15, H - 15], radius=16, outline=(30, 41, 59), width=2)

    # Fonts
    f_badge = get_font(12, bold=True)
    f_title = get_font(26, bold=True)
    f_subtitle = get_font(13, bold=False)
    f_pill = get_font(12, bold=True)
    f_win_title = get_font(12, bold=True)
    f_win_badge = get_font(10, bold=True)
    f_card_h = get_font(13, bold=True)
    f_card_b = get_font(11, bold=True)
    f_card_r = get_font(10, bold=False)
    f_price_big = get_font(24, bold=True)
    f_footer = get_font(11, bold=False)
    f_footer_b = get_font(11, bold=True)
    f_kpi_sub = get_font(9, bold=False)

    # =========================================================================
    # 1. HEADER (y = 25 .. 105)
    # =========================================================================
    badge_text = (
        "SUITE 01 MEGA BUNDLE • COLECCIÓN COMPLETA C-LEVEL (5 PACKS)"
        if is_es else
        "SUITE 01 MEGA BUNDLE • COMPLETE C-LEVEL COLLECTION (5 PACKS)"
    )
    draw.rounded_rectangle([40, 26, 475, 48], radius=6, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw.text((50, 30), badge_text, font=f_badge, fill=(56, 189, 248))

    title_text = (
        "SUITE 01: ESTRATEGIA CORPORATIVA & MBA (5 EN 1)"
        if is_es else
        "SUITE 01: CORPORATE STRATEGY & MBA MEGA BUNDLE (5-IN-1)"
    )
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    sub_text = (
        "PESTEL CUANTITATIVO  •  5 FUERZAS DE PORTER  •  DAFO & CAME  •  MATRIZ BCG DINÁMICA  •  MCKINSEY / GE 3x3"
        if is_es else
        "QUANTITATIVE PESTEL  •  PORTER'S 5 FORCES  •  SWOT & TOWS  •  DYNAMIC BCG MATRIX  •  MCKINSEY / GE 3x3"
    )
    draw.text((42, 85), sub_text, font=f_subtitle, fill=(148, 163, 184))

    # Deliverables Pills on Right
    pills = [
        ("10 Excel .xlsx + Sheets", (16, 124, 65), (236, 253, 245), (16, 185, 129)),
        ("10 PowerPoint 16:9 C-Level", (194, 65, 12), (255, 251, 235), (245, 158, 11)),
        ("5 Guías Metodológicas PDF" if is_es else "5 PDF Methodology Guides", (30, 58, 138), (239, 246, 255), (59, 130, 246)),
    ]
    px = W - 40
    for label, bg, fg, border in reversed(pills):
        bbox = f_pill.getbbox(label)
        pw = bbox[2] - bbox[0] + 24
        draw.rounded_rectangle([px - pw, 50, px, 78], radius=6, fill=bg, outline=border, width=1)
        draw.text((px - pw + 12, 56), label, font=f_pill, fill=(255, 255, 255))
        px -= (pw + 12)

    # =========================================================================
    # 2. 3x2 MOSAIC OF REAL CAPTURES FROM THE 5 TOOLS + SUITE SUMMARY CARD
    # =========================================================================
    tools_meta = [
        {
            "path": (
                "content/es/posts/matriz-pestel-cuantitativa/preview-pack.png"
                if is_es else
                "content/en/posts/quantitative-pestel-matrix/preview-pack.png"
            ),
            "title": (
                "01 · Matriz PESTEL Cuantitativa (Excel + PPTX)"
                if is_es else
                "01 · Quantitative PESTEL Matrix (Excel + PPTX)"
            ),
            "badge": "Incluido (Val. 5€)" if is_es else "Included (Val. 5€)",
            "header_col": (16, 124, 65),
        },
        {
            "path": (
                "content/es/posts/5-fuerzas-porter-cuantitativas/preview-pack.png"
                if is_es else
                "content/en/posts/quantitative-porter-5-forces/preview-pack.png"
            ),
            "title": (
                "02 · 5 Fuerzas de Porter Ponderadas (Excel + PPTX)"
                if is_es else
                "02 · Weighted Porter's 5 Forces (Excel + PPTX)"
            ),
            "badge": "Incluido (Val. 6€)" if is_es else "Included (Val. 6€)",
            "header_col": (15, 118, 110),
        },
        {
            "path": (
                "content/es/posts/dafo-cuantitativo-matriz-came/preview-pack.png"
                if is_es else
                "content/en/posts/quantitative-swot-tows-matrix/preview-pack.png"
            ),
            "title": (
                "03 · DAFO Cuantitativo & Matriz CAME (Excel + PPTX)"
                if is_es else
                "03 · Quantitative SWOT & TOWS Matrix (Excel + PPTX)"
            ),
            "badge": "Incluido (Val. 5€)" if is_es else "Included (Val. 5€)",
            "header_col": (30, 58, 138),
        },
        {
            "path": (
                "content/es/posts/matriz-bcg-dinamica/preview-pack.png"
                if is_es else
                "content/en/posts/dynamic-bcg-matrix/preview-pack.png"
            ),
            "title": (
                "04 · Matriz BCG Dinámica & Cash Flow (Excel + PPTX)"
                if is_es else
                "04 · Dynamic BCG Matrix & Cash Flow (Excel + PPTX)"
            ),
            "badge": "Incluido (Val. 6€)" if is_es else "Included (Val. 6€)",
            "header_col": (194, 65, 12),
        },
        {
            "path": (
                "content/es/posts/matriz-mckinsey-ge/preview-pack.png"
                if is_es else
                "content/en/posts/mckinsey-ge-matrix/preview-pack.png"
            ),
            "title": (
                "05 · Matriz McKinsey / GE 3x3 (Excel + PPTX)"
                if is_es else
                "05 · McKinsey / GE 3x3 Matrix (Excel + PPTX)"
            ),
            "badge": "Incluido (Val. 6€)" if is_es else "Included (Val. 6€)",
            "header_col": (109, 40, 217),
        },
    ]

    grid_x0 = 40
    grid_y0 = 115
    col_gap = 22
    row_gap = 20
    cell_w = (W - 80 - 2 * col_gap) // 3  # 492 px
    cell_h = (770 - row_gap) // 2         # 375 px
    header_h = 30

    for idx, tinfo in enumerate(tools_meta):
        r = idx // 3
        c = idx % 3
        cx = grid_x0 + c * (cell_w + col_gap)
        cy = grid_y0 + r * (cell_h + row_gap)

        # Window frame
        draw.rounded_rectangle(
            [cx, cy, cx + cell_w, cy + cell_h],
            radius=8,
            fill=(15, 23, 42),
            outline=(51, 65, 85),
            width=2,
        )
        draw_window_header(
            draw,
            cx,
            cy,
            cell_w,
            header_h,
            tinfo["title"],
            tinfo["header_col"],
            f_win_title,
            price_badge=tinfo["badge"],
            f_badge=f_win_badge,
        )

        # Load real preview-pack.png and crop the main workspace (y=115..880, x=35..1565)
        if os.path.exists(tinfo["path"]):
            src_img = Image.open(tinfo["path"]).convert("RGB")
            # Crop the 3-window composite region from the individual preview-pack
            cropped = src_img.crop((35, 112, 1565, 885))
            target_w = cell_w - 8
            target_h = cell_h - header_h - 6
            resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
            im.paste(resized, (cx + 4, cy + header_h + 2))

        # Re-draw crisp border around window
        draw.rounded_rectangle(
            [cx, cy, cx + cell_w, cy + cell_h],
            radius=8,
            outline=(71, 85, 105),
            width=2,
        )

    # =========================================================================
    # 3. 6th PANEL (BOTTOM RIGHT): SUITE 01 ARCHITECTURE & BUNDLE VALUE SUMMARY
    # =========================================================================
    c6_x = grid_x0 + 2 * (cell_w + col_gap)
    c6_y = grid_y0 + 1 * (cell_h + row_gap)

    draw.rounded_rectangle(
        [c6_x, c6_y, c6_x + cell_w, c6_y + cell_h],
        radius=8,
        fill=(15, 23, 42),
        outline=(56, 189, 248),
        width=2,
    )
    suite_win_title = (
        "Suite 01 · El Sistema de Decisión Integrado C-Level"
        if is_es else
        "Suite 01 · The Integrated C-Level Decision Engine"
    )
    draw_window_header(
        draw,
        c6_x,
        c6_y,
        cell_w,
        header_h,
        suite_win_title,
        (30, 58, 138),
        f_win_title,
        price_badge="AHORRO 32%" if is_es else "SAVE 32%",
        f_badge=f_win_badge,
    )

    # Inside 6th Panel: 5-Step Flow Pipeline
    iy = c6_y + header_h + 10
    ix = c6_x + 14
    iw = cell_w - 28

    draw.text(
        (ix, iy),
        " FLUJO SECUENCIAL DE CAPITAL (OUTSIDE-IN):" if is_es else " SEQUENTIAL CAPITAL PIPELINE (OUTSIDE-IN):",
        font=f_win_badge,
        fill=(56, 189, 248),
    )
    iy += 18

    steps = [
        ("1. PESTEL", "Resiliencia Macro (RES) & EBITDA at Risk" if is_es else "Macro Resilience (RES) & EBITDA at Risk", (16, 185, 129)),
        ("2. PORTER", "Atractivo Industrial (A_ind) vs. Moat (M)" if is_es else "Industry Attractiveness (A_ind) vs. Moat", (56, 189, 248)),
        ("3. DAFO-CAME", "Vector Cartesiano V(X,Y) & Cruces 40×40" if is_es else "Cartesian Vector V(X,Y) & 40×40 TOWS", (99, 102, 241)),
        ("4. BCG", "Curva Experiencia & Equilibrio FCF (BNF)" if is_es else "Experience Curve & Net FCF Balance", (245, 158, 11)),
        ("5. MCKINSEY", "9 Cajas (T1=2.33, T2=3.67) & Hurdle TIR" if is_es else "9-Box Grid (T1=2.33, T2=3.67) & IRR Hurdle", (168, 85, 247)),
    ]

    for s_tag, s_desc, s_col in steps:
        draw.rounded_rectangle([ix, iy, ix + iw, iy + 34], radius=5, fill=(24, 34, 53), outline=(51, 65, 85), width=1)
        draw.rounded_rectangle([ix + 4, iy + 5, ix + 108, iy + 29], radius=4, fill=(15, 23, 42), outline=s_col, width=1)
        draw.text((ix + 10, iy + 9), s_tag, font=f_win_badge, fill=s_col)
        draw.text((ix + 118, iy + 9), s_desc, font=f_card_r, fill=(226, 232, 240))
        iy += 38

    # Bottom Offer Box inside 6th Panel
    iy += 4
    draw.rounded_rectangle(
        [ix, iy, ix + iw, c6_y + cell_h - 12],
        radius=8,
        fill=(16, 38, 56),
        outline=(16, 185, 129),
        width=2,
    )
    offer_title = (
        "PACK COMPLETO (25 ARCHIVOS EJECUTIVOS)"
        if is_es else
        "COMPLETE MEGA BUNDLE (25 EXECUTIVE FILES)"
    )
    draw.text((ix + 14, iy + 10), offer_title, font=f_card_b, fill=(52, 211, 153))
    offer_sub = (
        "• 10 Modelos Excel/Sheets (ES+EN) 100% desbloqueados\n• 10 Presentaciones PPTX 16:9 + 5 Guías PDF C-Level"
        if is_es else
        "• 10 Unlocked Excel/Sheets Models (ES+EN)\n• 10 Widescreen PPTX 16:9 Decks + 5 C-Level PDF Guides"
    )
    draw.text((ix + 14, iy + 30), offer_sub, font=f_card_r, fill=(203, 213, 225))

    # Price Badge on Right of Offer Box
    draw.rounded_rectangle(
        [ix + iw - 122, iy + 12, ix + iw - 12, c6_y + cell_h - 22],
        radius=6,
        fill=(15, 23, 42),
        outline=(245, 158, 11),
        width=1,
    )
    draw.text((ix + iw - 108, iy + 16), "19 €", font=f_price_big, fill=(245, 158, 11))
    draw.text((ix + iw - 54, iy + 24), "28€", font=f_card_b, fill=(148, 163, 184))
    draw.line([ix + iw - 56, iy + 32, ix + iw - 24, iy + 32], fill=(239, 68, 68), width=2)
    draw.text(
        (ix + iw - 108, iy + 48),
        "Ahorro 32% (.ZIP)" if is_es else "Save 32% (.ZIP)",
        font=f_kpi_sub,
        fill=(52, 211, 153),
    )

    # =========================================================================
    # 4. FOOTER (y = 900 .. 965)
    # =========================================================================
    draw.text((45, 915), "DATALARIA.COM • EXECUTIVE DECISION SUPPORT", font=f_footer_b, fill=(100, 116, 139))
    draw.text(
        (45, 935),
        "Estándar Consultoría Tier-1 (McKinsey / BCG / Bain)" if is_es else "Tier-1 Consulting Standards (McKinsey / BCG / Bain)",
        font=f_kpi_sub,
        fill=(71, 85, 105),
    )

    center_text = (
        "Fórmulas 100% Auditables • Celdas Desbloqueadas • Compatibilidad MS Excel & Google Sheets"
        if is_es else
        "100% Auditable Formulas • Unlocked Input Cells • MS Excel & Google Sheets Compatibility"
    )
    draw.text((440, 925), center_text, font=f_footer, fill=(203, 213, 225))

    dl_badge = "Descarga Inmediata (.ZIP)" if is_es else "Instant Download (.ZIP)"
    draw.rounded_rectangle([W - 240, 915, W - 40, 947], radius=6, fill=(15, 36, 58), outline=(56, 189, 248), width=1)
    draw.text((W - 222, 923), dl_badge, font=f_footer_b, fill=(56, 189, 248))

    return im


def main():
    os.makedirs("static/images/recursos", exist_ok=True)
    os.makedirs("content/es/posts/estrategia-corporativa-mba-framework-cuantitativo", exist_ok=True)
    os.makedirs("content/en/posts/corporate-strategy-mba-quantitative-framework", exist_ok=True)

    im_es = generate_preview_suite01(lang="es")
    p_static_es = "static/images/recursos/suite-01-preview-es.png"
    p_post_es = "content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/preview-pack.png"
    im_es.save(p_static_es, "PNG", optimize=True)
    im_es.save(p_post_es, "PNG", optimize=True)
    print(f"[OK] Generated {p_static_es} and {p_post_es} ({im_es.size})")

    im_en = generate_preview_suite01(lang="en")
    p_static_en = "static/images/recursos/suite-01-preview-en.png"
    p_post_en = "content/en/posts/corporate-strategy-mba-quantitative-framework/preview-pack.png"
    im_en.save(p_static_en, "PNG", optimize=True)
    im_en.save(p_post_en, "PNG", optimize=True)
    print(f"[OK] Generated {p_static_en} and {p_post_en} ({im_en.size})")


if __name__ == "__main__":
    main()
