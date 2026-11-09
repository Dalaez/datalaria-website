#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Mega Bundle Suite 02: Toma de Decisiones & Priorización en español e inglés:
- static/images/recursos/suite-02-preview-es.png
- static/images/recursos/suite-02-preview-en.png
- content/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/preview-pack.png
- content/en/posts/decision-making-prioritization-quantitative-framework/preview-pack.png

Integra capturas reales de alta resolución de los 3 Executive Decision Packs
individuales (Matriz DAR CMMI, Matriz RICE & ICE Ágil y Business Case Financiero DCF)
junto con una tarjeta de arquitectura y valor C-Level en el estándar visual Dark-Slate Tier-1.
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
        pw = pb_box[2] - pb_box[0] + 16
        draw.rounded_rectangle([x + w - pw - 10, y + 5, x + w - 10, y + h - 5], radius=4, fill=(15, 23, 42))
        draw.text((x + w - pw - 2, y + 7), price_badge, font=f_badge, fill=(52, 211, 153))


def generate_preview_suite02(lang="es"):
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
    f_win_title = get_font(13, bold=True)
    f_win_badge = get_font(11, bold=True)
    f_card_h = get_font(15, bold=True)
    f_card_b = get_font(12, bold=True)
    f_card_r = get_font(11, bold=False)
    f_price_big = get_font(28, bold=True)
    f_price_old = get_font(14, bold=False)
    f_footer = get_font(11, bold=False)
    f_footer_b = get_font(11, bold=True)
    f_kpi_sub = get_font(10, bold=False)

    # =========================================================================
    # 1. HEADER (y = 25 .. 105)
    # =========================================================================
    badge_text = (
        "SUITE 02 MEGA BUNDLE • COLECCIÓN COMPLETA DE DECISIÓN C-LEVEL (3 PACKS)"
        if is_es else
        "SUITE 02 MEGA BUNDLE • COMPLETE C-LEVEL DECISION COLLECTION (3 PACKS)"
    )
    b_len = 540 if is_es else 575
    draw.rounded_rectangle([40, 26, 40 + b_len, 48], radius=6, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw.text((50, 30), badge_text, font=f_badge, fill=(56, 189, 248))

    title_text = (
        "SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN CUANTITATIVA (3 EN 1)"
        if is_es else
        "SUITE 02: QUANTITATIVE DECISION-MAKING & PRIORITIZATION (3-IN-1)"
    )
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    sub_text = (
        "MATRIZ DAR CMMI (FILTROS VETO)  •  MATRIZ RICE & ICE ÁGIL (CAPACIDAD SQUADS)  •  BUSINESS CASE FINANCIERO DCF (VAN/TIR/TORNADO)"
        if is_es else
        "CMMI DAR MATRIX (VETO GATES)  •  AGILE RICE & ICE MATRIX (SQUAD CAPACITY)  •  FINANCIAL DCF BUSINESS CASE (NPV/IRR/TORNADO)"
    )
    draw.text((40, 88), sub_text, font=f_subtitle, fill=(148, 163, 184))

    # Right pills in header
    pills = [
        ("📊 6 Excel/Sheets", (30, 41, 59), (56, 189, 248)),
        ("📑 6 Decks PPTX 16:9", (30, 41, 59), (167, 139, 250)),
        ("📄 3 Guías PDF" if is_es else "📄 3 PDF Guides", (30, 41, 59), (52, 211, 153)),
        ("👑 Ahorro 25%" if is_es else "👑 25% Savings", (15, 36, 58), (245, 158, 11)),
    ]
    px = W - 40
    for ptext, bg, fg in reversed(pills):
        p_bbox = f_pill.getbbox(ptext)
        pw = p_bbox[2] - p_bbox[0] + 20
        px -= pw
        draw.rounded_rectangle([px, 46, px + pw, 76], radius=6, fill=bg, outline=fg, width=1)
        draw.text((px + 10, 53), ptext, font=f_pill, fill=fg)
        px -= 10

    # =========================================================================
    # 2. 2x2 GRID (y = 115 .. 885)
    # =========================================================================
    tools_meta = [
        {
            "path": (
                "content/es/posts/matriz-dar-cuantitativa/preview-pack.png"
                if is_es else
                "content/en/posts/quantitative-dar-matrix/preview-pack.png"
            ),
            "title": (
                "01 · Matriz DAR Cuantitativa: Filtros Veto & Ponderación Multicriterio (Excel + PPTX)"
                if is_es else
                "01 · Quantitative DAR Matrix: Veto Hurdles & Multi-Criteria Scoring (Excel + PPTX)"
            ),
            "badge": "Incluido (Val. 6€)" if is_es else "Included (Val. 6€)",
            "header_col": (16, 185, 129),  # Emerald #10B981
        },
        {
            "path": (
                "content/es/posts/matriz-rice-ice-priorizacion/preview-pack.png"
                if is_es else
                "content/en/posts/rice-ice-prioritization-matrix/preview-pack.png"
            ),
            "title": (
                "02 · Matriz RICE & ICE de Priorización Ágil & Capacidad de Squads (Excel + PPTX)"
                if is_es else
                "02 · Agile RICE & ICE Prioritization Matrix & Squad Capacity (Excel + PPTX)"
            ),
            "badge": "Incluido (Val. 6€)" if is_es else "Included (Val. 6€)",
            "header_col": (37, 99, 235),  # Blue #2563EB
        },
        {
            "path": (
                "content/es/posts/business-case-financiero-van-tir/preview-pack.png"
                if is_es else
                "content/en/posts/financial-business-case-npv-irr/preview-pack.png"
            ),
            "title": (
                "03 · Business Case Financiero Completo: VAN, TIR, Payback & Tornado (Excel + PPTX)"
                if is_es else
                "03 · Full Financial DCF Business Case: NPV, IRR, Payback & Tornado (Excel + PPTX)"
            ),
            "badge": "Incluido (Val. 8€)" if is_es else "Included (Val. 8€)",
            "header_col": (217, 119, 6),  # Amber #D97706
        },
    ]

    grid_x0 = 40
    grid_y0 = 115
    col_gap = 24
    row_gap = 20
    cell_w = (W - 80 - col_gap) // 2  # 748 px
    cell_h = (770 - row_gap) // 2      # 375 px
    header_h = 32

    for idx, tinfo in enumerate(tools_meta):
        r = idx // 2
        c = idx % 2
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

        # Load real preview-pack.png and crop the main workspace
        if os.path.exists(tinfo["path"]):
            src_img = Image.open(tinfo["path"]).convert("RGB")
            # Crop the inner workspace region from the individual preview-pack
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
    # 3. 4th PANEL (BOTTOM RIGHT): SUITE 02 ARCHITECTURE & VALUE SUMMARY CARD
    # =========================================================================
    c4_x = grid_x0 + 1 * (cell_w + col_gap)
    c4_y = grid_y0 + 1 * (cell_h + row_gap)

    draw.rounded_rectangle(
        [c4_x, c4_y, c4_x + cell_w, c4_y + cell_h],
        radius=8,
        fill=(15, 23, 42),
        outline=(56, 189, 248),
        width=2,
    )
    draw_window_header(
        draw,
        c4_x,
        c4_y,
        cell_w,
        header_h,
        "SUITE 02 · EL PIPELINE CUANTITATIVO DE DECISIÓN EN 3 NIVELES"
        if is_es else
        "SUITE 02 · THE 3-TIER QUANTITATIVE DECISION PIPELINE",
        (30, 41, 59),
        f_win_title,
        price_badge="AHORRO 25%" if is_es else "25% SAVINGS",
        f_badge=f_win_badge,
    )

    pad_x = c4_x + 20
    cur_y = c4_y + header_h + 16

    # 3 Connected Tiers Section
    sub_title = (
        "ARQUITECTURA DE DECISIÓN INTEGRADA (CMMI + RICE + DCF):"
        if is_es else
        "INTEGRATED DECISION ARCHITECTURE (CMMI + RICE + DCF):"
    )
    draw.text((pad_x, cur_y), sub_title, font=f_card_b, fill=(56, 189, 248))
    cur_y += 24

    tiers_desc = [
        (
            "NIVEL 1 · SELECCIÓN ARQUITECTURA (DAR):"
            if is_es else
            "TIER 1 · ARCHITECTURE SELECTION (DAR):",
            "Filtros veto booleanos (Vk=0 descalifica) y scoring ponderado (TCO, SLA, Tech)."
            if is_es else
            "Boolean veto hurdles (Vk=0 disqualifies) and 4-pillar weighted scoring."
        ),
        (
            "NIVEL 2 · PRIORIZACIÓN ROADMAP (RICE/ICE):"
            if is_es else
            "TIER 2 · ROADMAP PRIORITIZATION (RICE/ICE):",
            "Densidad de valor por esfuerzo con corte automático por capacidad de squads."
            if is_es else
            "Value density per unit of effort with automated squad capacity cut-off."
        ),
        (
            "NIVEL 3 · JUSTIFICACIÓN CAPITAL (BUSINESS CASE):"
            if is_es else
            "TIER 3 · CAPITAL JUSTIFICATION (BUSINESS CASE):",
            "Flujo de caja libre a 3-5 años, WACC, VAN, TIR, Payback y Gráfico Tornado."
            if is_es else
            "Discounted FCF (3-5Y), CAPM WACC, NPV, IRR, Payback, and Tornado Chart."
        ),
    ]

    for t_head, t_body in tiers_desc:
        draw.text((pad_x, cur_y), t_head, font=f_card_b, fill=(245, 158, 11))
        tb_box = f_card_b.getbbox(t_head)
        tb_w = tb_box[2] - tb_box[0] + 8
        draw.text((pad_x + tb_w, cur_y + 1), t_body, font=f_card_r, fill=(226, 232, 240))
        cur_y += 24

    cur_y += 8
    # Divider line
    draw.line([(pad_x, cur_y), (c4_x + cell_w - 20, cur_y)], fill=(30, 41, 59), width=1)
    cur_y += 14

    # Deliverables & Value Box
    draw.rounded_rectangle(
        [pad_x, cur_y, c4_x + cell_w - 20, cur_y + 86],
        radius=6,
        fill=(11, 17, 32),
        outline=(30, 58, 138),
        width=1,
    )

    # Deliverables bullet list
    deliv_lines = [
        "✔ 6 Modelos en Excel (.xlsx) y Google Sheets con celdas 100% desbloqueadas y fórmulas nativas"
        if is_es else
        "✔ 6 Unlocked Excel (.xlsx) and Google Sheets models with native dynamic formulas",
        "✔ 6 Presentaciones ejecutivas en PowerPoint (.pptx 16:9) estructuradas bajo la Pirámide de Minto"
        if is_es else
        "✔ 6 Executive PowerPoint decks (.pptx 16:9) structured under the Minto Pyramid Principle",
        "✔ 3 Guías metodológicas en PDF con derivaciones matemáticas, rúbricas y casos resueltos"
        if is_es else
        "✔ 3 Methodology PDF guides with mathematical proofs, scoring rubrics, and solved cases",
    ]
    dy = cur_y + 10
    for d_line in deliv_lines:
        draw.text((pad_x + 14, dy), d_line, font=f_card_r, fill=(203, 213, 225))
        dy += 22

    cur_y += 98

    # Bottom CTA Box with Price & Lemon Squeezy trust
    p_box_h = 60
    draw.rounded_rectangle(
        [pad_x, cur_y, c4_x + cell_w - 20, cur_y + p_box_h],
        radius=6,
        fill=(15, 36, 58),
        outline=(16, 185, 129),
        width=1,
    )

    # Price on left
    draw.text((pad_x + 16, cur_y + 12), "15€", font=f_price_big, fill=(245, 158, 11))
    p_bbox = f_price_big.getbbox("15€")
    p_w = p_bbox[2] - p_bbox[0] + 12

    strike_txt = "20€ por separado" if is_es else "20€ separate value"
    draw.text((pad_x + 16 + p_w, cur_y + 16), strike_txt, font=f_price_old, fill=(148, 163, 184))
    st_bbox = f_price_old.getbbox(strike_txt)
    draw.line(
        [(pad_x + 16 + p_w, cur_y + 24), (pad_x + 16 + p_w + st_bbox[2] - st_bbox[0], cur_y + 24)],
        fill=(239, 68, 68),
        width=1,
    )

    save_pill = "AHORRO 25%" if is_es else "SAVE 25%"
    draw.rounded_rectangle(
        [pad_x + 22 + p_w + st_bbox[2] - st_bbox[0], cur_y + 15, pad_x + 115 + p_w + st_bbox[2] - st_bbox[0], cur_y + 33],
        radius=4,
        fill=(16, 185, 129),
    )
    draw.text(
        (pad_x + 28 + p_w + st_bbox[2] - st_bbox[0], cur_y + 17),
        save_pill,
        font=f_win_badge,
        fill=(255, 255, 255),
    )

    trust_sub = (
        "⚡ Descarga directa (.ZIP) • Factura B2B deducible • Pasarela segura Lemon Squeezy"
        if is_es else
        "⚡ Instant download (.ZIP) • B2B tax-deductible invoice • Secure Lemon Squeezy checkout"
    )
    draw.text((pad_x + 16, cur_y + 40), trust_sub, font=f_kpi_sub, fill=(148, 163, 184))

    # =========================================================================
    # 4. FOOTER (y = 905 .. 955)
    # =========================================================================
    draw.line([(40, 905), (W - 40, 905)], fill=(30, 41, 59), width=1)

    f_left = (
        "DATALARIA.COM  •  SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN  •  ESTÁNDAR CMMI DAR & CORPORATE FINANCE"
        if is_es else
        "DATALARIA.COM  •  SUITE 02: QUANTITATIVE DECISION-MAKING & PRIORITIZATION  •  CMMI DAR & CORPORATE FINANCE STANDARD"
    )
    draw.text((40, 920), f_left, font=f_footer, fill=(100, 116, 139))

    f_right = (
        "6 MODELOS EXCEL + 6 DECK PPTX 16:9 + 3 GUÍAS PDF  •  15€  •  AHORRO 25%"
        if is_es else
        "6 EXCEL MODELS + 6 PPTX 16:9 DECKS + 3 PDF GUIDES  •  15€  •  25% SAVINGS"
    )
    fr_box = f_footer_b.getbbox(f_right)
    draw.text((W - 40 - (fr_box[2] - fr_box[0]), 920), f_right, font=f_footer_b, fill=(56, 189, 248))

    return im


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Targets
    es_targets = [
        os.path.join(base_dir, "static", "images", "recursos", "suite-02-preview-es.png"),
        os.path.join(base_dir, "content", "es", "posts", "toma-decisiones-priorizacion-framework-cuantitativo", "preview-pack.png"),
    ]
    en_targets = [
        os.path.join(base_dir, "static", "images", "recursos", "suite-02-preview-en.png"),
        os.path.join(base_dir, "content", "en", "posts", "decision-making-prioritization-quantitative-framework", "preview-pack.png"),
    ]

    print("[*] Generando vista previa Suite 02 en Español...")
    im_es = generate_preview_suite02("es")
    for t in es_targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        im_es.save(t, format="PNG", optimize=True)
        print(f"    -> Guardado: {t} ({os.path.getsize(t)} bytes)")

    print("[*] Generando vista previa Suite 02 en Inglés...")
    im_en = generate_preview_suite02("en")
    for t in en_targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        im_en.save(t, format="PNG", optimize=True)
        print(f"    -> Guardado: {t} ({os.path.getsize(t)} bytes)")

    print("[OK] Generación de vistas previas Suite 02 completada.")


if __name__ == "__main__":
    main()
