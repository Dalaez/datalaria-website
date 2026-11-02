#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Executive Decision Pack de la Matriz DAR Cuantitativa en español e inglés:
- static/images/recursos/dar-preview-es.png
- static/images/recursos/dar-preview-en.png
- content/es/posts/matriz-dar-cuantitativa/preview-pack.png
- content/en/posts/quantitative-dar-matrix/preview-pack.png

Utiliza capturas REALES de alta fidelidad extraídas directamente de los
entregables oficiales de la Suite 02:
1. Excel .xlsx: Captura real del Dashboard Ejecutivo con tabla master, KPIs y pilares.
2. PDF .pdf: Capturas reales de la Guía Metodológica C-Level (Págs. 1 y 2 con formulación matemática).
3. PowerPoint .pptx: Captura real de la Diapositiva 3 (Roadmap, Board Decision Gateway y 4 firmas digitales).
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Directorio raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_font(size, bold=False):
    font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
    alt_name = "arialbd.ttf" if bold else "arial.ttf"
    path = os.path.join(r"C:\Windows\Fonts", font_name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    alt_path = os.path.join(r"C:\Windows\Fonts", alt_name)
    if os.path.exists(alt_path):
        return ImageFont.truetype(alt_path, size)
    return ImageFont.load_default()


def draw_window_header(draw, x, y, w, h, title, bg_color, font):
    # Header background
    draw.rounded_rectangle([x, y, x + w, y + h + 10], radius=8, fill=bg_color)
    draw.rectangle([x, y + h - 5, x + w, y + h], fill=bg_color)
    # Traffic lights (macOS style)
    r = 5
    cy = y + h // 2
    draw.ellipse([x + 14 - r, cy - r, x + 14 + r, cy + r], fill=(255, 95, 86))   # Red
    draw.ellipse([x + 30 - r, cy - r, x + 30 + r, cy + r], fill=(255, 189, 46))  # Yellow
    draw.ellipse([x + 46 - r, cy - r, x + 46 + r, cy + r], fill=(39, 201, 63))   # Green
    # Title centered
    bbox = font.getbbox(title)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (w - tw) // 2, cy - th // 2 - 2), title, font=font, fill=(255, 255, 255))


def draw_sparkle(draw, cx, cy, r, fill):
    """Dibuja una estrella estilizada de 4 puntas (sparkle ejecutivo)."""
    points = [
        (cx, cy - r),
        (cx + r * 0.35, cy - r * 0.35),
        (cx + r, cy),
        (cx + r * 0.35, cy + r * 0.35),
        (cx, cy + r),
        (cx - r * 0.35, cy + r * 0.35),
        (cx - r, cy),
        (cx - r * 0.35, cy - r * 0.35),
    ]
    draw.polygon(points, fill=fill)


def draw_download_icon(draw, cx, cy, r, fill):
    """Dibuja un icono vectorial de descarga (flecha hacia abajo con bandeja)."""
    # Flecha vertical
    draw.rectangle([cx - 2, cy - r, cx + 2, cy + 2], fill=fill)
    draw.polygon([(cx - int(r * 0.8), cy + 1), (cx + int(r * 0.8), cy + 1), (cx, cy + r + 1)], fill=fill)
    # Bandeja inferior
    draw.line([(cx - r, cy + r + 3), (cx + r, cy + r + 3)], fill=fill, width=2)


def find_capture_path(filename):
    """Busca un archivo de captura en las rutas conocidas."""
    candidates = [
        os.path.join(BASE_DIR, "scripts", "executive_pack_dar", "captures", filename),
        os.path.join(BASE_DIR, "temp_captures", filename),
        os.path.join(os.path.dirname(__file__), "captures", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def generate_preview_pack(lang="es"):
    is_es = (lang == "es")
    W, H = 1600, 980
    im = Image.new("RGB", (W, H), (11, 17, 32))  # Deep Slate Navy #0B1120
    draw = ImageDraw.Draw(im)

    # Border general
    draw.rounded_rectangle([15, 15, W - 15, H - 15], radius=16, outline=(30, 41, 59), width=2)

    # Fuentes
    f_badge = get_font(12, bold=True)
    f_title = get_font(26, bold=True)
    f_subtitle = get_font(13, bold=False)
    f_pill = get_font(12, bold=True)
    f_win_title = get_font(13, bold=True)
    f_formula = get_font(11, bold=False)
    f_tab = get_font(10, bold=True)
    f_page_lbl = get_font(9.5, bold=True)
    f_footer = get_font(11, bold=False)
    f_footer_b = get_font(11, bold=True)
    f_footer_sub = get_font(10, bold=False)

    # =========================================================================
    # 1. HEADER (y = 25 .. 105)
    # =========================================================================
    # Badge superior izquierdo
    draw.rounded_rectangle([40, 26, 385, 48], radius=6, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw_sparkle(draw, 55, 37, 6, (56, 189, 248))
    badge_text = "EXECUTIVE DECISION PACK \u2022 TOMA DE DECISIONES" if is_es else "EXECUTIVE DECISION PACK \u2022 DECISION MAKING"
    draw.text((68, 30), badge_text, font=f_badge, fill=(56, 189, 248))

    # Título Principal
    title_text = "MATRIZ DAR CUANTITATIVA DUAL" if is_es else "QUANTITATIVE DAR MATRIX DUAL PACK"
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    # Subtítulo
    sub_text = (
        "CRITERIOS VETO (MUST-HAVES), SCORING MULTICRITERIO (WANTS) & BOARD DECISION GATEWAY"
        if is_es else
        "VETO CRITERIA (MUST-HAVES), MULTI-CRITERIA SCORING (WANTS) & BOARD DECISION GATEWAY"
    )
    draw.text((42, 85), sub_text, font=f_subtitle, fill=(148, 163, 184))

    # Pills de Entregables a la derecha
    pills = [
        ("Excel .xlsx + Sheets", (16, 124, 65), (236, 253, 245), (16, 185, 129)),
        ("PowerPoint 16:9 C-Level", (194, 65, 12), (255, 251, 235), (245, 158, 11)),
        ("Guía Metodológica PDF" if is_es else "PDF Methodology Guide", (30, 58, 138), (239, 246, 255), (59, 130, 246)),
    ]
    px = W - 40
    for label, bg, fg, border in reversed(pills):
        bbox = f_pill.getbbox(label)
        pw = bbox[2] - bbox[0] + 24
        draw.rounded_rectangle([px - pw, 50, px, 78], radius=6, fill=bg, outline=border, width=1)
        draw.text((px - pw + 12, 56), label, font=f_pill, fill=(255, 255, 255))
        px -= (pw + 12)

    # =========================================================================
    # 2. LEFT WINDOW: CAPTURA REAL EXCEL DASHBOARD (x=40, y=115, w=925, h=765)
    # =========================================================================
    wx, wy, ww, wh = 40, 115, 925, 765
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(255, 255, 255), outline=(51, 65, 85), width=2)

    # Titlebar (Excel Green #107C41)
    title_win_es = "Excel .xlsx \u2014 Motor Cuantitativo & Dashboard de Decisión DAR [Protegido]"
    title_win_en = "Excel .xlsx \u2014 Quantitative Engine & DAR Decision Dashboard [Protected]"
    draw_window_header(draw, wx, wy, ww, 34, title_win_es if is_es else title_win_en, (16, 124, 65), f_win_title)

    # Formula Bar
    draw.rectangle([wx, wy + 34, wx + ww, wy + 62], fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    fx_text_es = 'fx: =SI(D13="DESCALIFICADA"; "-"; JERARQUIA(G13; $G$12:$G$16))'
    fx_text_en = 'fx: =IF(D13="DISQUALIFIED", "-", RANK(G13, $G$12:$G$16))'
    draw.text((wx + 15, wy + 41), fx_text_es if is_es else fx_text_en, font=f_formula, fill=(71, 85, 105))

    # Inner Excel Sheet Area
    inner_x = wx + 10
    inner_y = wy + 66
    inner_w = ww - 20   # 905 px
    inner_h = wh - 100  # 665 px

    # Cargar e incrustar la captura REAL de la hoja de cálculo
    xl_img_path = find_capture_path(f"tight_excel_{lang}.png")
    if xl_img_path and os.path.exists(xl_img_path):
        xl_raw = Image.open(xl_img_path)
        w_raw, h_raw = xl_raw.size
        # Recortar el 72% superior (metadatos, tabla de alternativas, 3 tarjetas KPI y desglose de 4 pilares)
        xl_crop = xl_raw.crop((0, 0, w_raw, int(h_raw * 0.72)))
        xl_scaled = xl_crop.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
        im.paste(xl_scaled, (inner_x, inner_y))

    # Pestañas inferiores de la hoja de cálculo
    tab_y = wy + wh - 30
    draw.rectangle([wx, tab_y, wx + ww, wy + wh], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    tabs = [
        ("01_Dashboard_Ejecutivo" if is_es else "01_Executive_Dashboard", (16, 124, 65), True),
        ("02_Filtros_Veto_MustHaves" if is_es else "02_Veto_Criteria_MustHaves", (100, 116, 139), False),
        ("03_Scoring_Ponderado_Wants" if is_es else "03_Weighted_Scoring_Wants", (100, 116, 139), False),
        ("04_Sensibilidad_Auditoria" if is_es else "04_Sensitivity_AuditTrail", (100, 116, 139), False),
    ]
    tbx = wx + 15
    for tab_name, tab_col, is_active in tabs:
        bbox = f_tab.getbbox(tab_name)
        tbw = bbox[2] - bbox[0] + 18
        if is_active:
            draw.rounded_rectangle([tbx, tab_y - 2, tbx + tbw, wy + wh], radius=4, fill=(16, 124, 65))
            draw.text((tbx + 9, tab_y + 4), tab_name, font=f_tab, fill=(255, 255, 255))
        else:
            draw.text((tbx + 9, tab_y + 4), tab_name, font=f_tab, fill=tab_col)
        tbx += (tbw + 10)

    # =========================================================================
    # 3. TOP-RIGHT WINDOW: CAPTURAS REALES GUÍA PDF (x=985, y=115, w=575, h=370)
    # =========================================================================
    px, py, pw, ph = 985, 115, 575, 370
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pdf_title_es = "Guía Metodológica Oficial (.pdf) \u2014 5 Páginas C-Level"
    pdf_title_en = "Official Methodology Guide (.pdf) \u2014 5 C-Level Pages"
    draw_window_header(draw, px, py, pw, 34, pdf_title_es if is_es else pdf_title_en, (30, 58, 138), f_win_title)

    # Cargar e incrustar Página 1 y Página 2 del PDF real en disposición folleto ejecutivo
    p1_path = find_capture_path(f"pdf_{lang}_page1.png")
    p2_path = find_capture_path(f"pdf_{lang}_page2.png")
    pdf_target_h = 300
    pdf_target_w = int(pdf_target_h * (1654 / 2339))  # ~212 px

    if p1_path and p2_path and os.path.exists(p1_path) and os.path.exists(p2_path):
        p1_img = Image.open(p1_path).resize((pdf_target_w, pdf_target_h), Image.Resampling.LANCZOS)
        p2_img = Image.open(p2_path).resize((pdf_target_w, pdf_target_h), Image.Resampling.LANCZOS)

        # Centrar ambas páginas horizontalmente dentro de la ventana
        gap = 25
        total_w = pdf_target_w * 2 + gap
        start_x = px + (pw - total_w) // 2
        start_y = py + 42

        # Sombra / marco sutil
        draw.rounded_rectangle([start_x - 3, start_y - 3, start_x + pdf_target_w + 3, start_y + pdf_target_h + 3], radius=4, fill=(30, 41, 59))
        draw.rounded_rectangle([start_x + pdf_target_w + gap - 3, start_y - 3, start_x + total_w + 3, start_y + pdf_target_h + 3], radius=4, fill=(30, 41, 59))

        im.paste(p1_img, (start_x, start_y))
        im.paste(p2_img, (start_x + pdf_target_w + gap, start_y))

        # Etiquetas explicativas bajo cada página
        lbl_p1 = "Pág. 1: Encuadre & Requisitos" if is_es else "Page 1: Scope & Framework"
        lbl_p2 = "Pág. 2: Formulación CMMI DAR" if is_es else "Page 2: CMMI DAR Math Proofs"
        draw.text((start_x + 10, start_y + pdf_target_h + 6), lbl_p1, font=f_page_lbl, fill=(148, 163, 184))
        draw.text((start_x + pdf_target_w + gap + 10, start_y + pdf_target_h + 6), lbl_p2, font=f_page_lbl, fill=(148, 163, 184))

    # =========================================================================
    # 4. BOTTOM-RIGHT WINDOW: CAPTURA REAL SLIDE 3 PPTX (x=985, y=505, w=575, h=375)
    # =========================================================================
    sx, sy, sw, sh = 985, 505, 575, 375
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pptx_title_es = "Presentación Grado Consejo (.pptx 16:9 Widescreen)"
    pptx_title_en = "Boardroom Presentation (.pptx 16:9 Widescreen)"
    draw_window_header(draw, sx, sy, sw, 34, pptx_title_es if is_es else pptx_title_en, (194, 65, 12), f_win_title)

    # Cargar e incrustar Diapositiva 3 real (Roadmap, Board Decision Gateway y Firmas)
    ppt_slide_path = find_capture_path(f"ppt_{lang}_slide3.png")
    if ppt_slide_path and os.path.exists(ppt_slide_path):
        ppt_raw = Image.open(ppt_slide_path)
        ppt_target_w = 555
        ppt_target_h = int(ppt_target_w * (1080 / 1920))  # 312 px (16:9 widescreen)
        ppt_scaled = ppt_raw.resize((ppt_target_w, ppt_target_h), Image.Resampling.LANCZOS)

        ppt_x = sx + (sw - ppt_target_w) // 2
        ppt_y = sy + 34 + (sh - 34 - ppt_target_h) // 2

        # Marco exterior sutil
        draw.rounded_rectangle([ppt_x - 2, ppt_y - 2, ppt_x + ppt_target_w + 2, ppt_y + ppt_target_h + 2], radius=4, fill=(30, 41, 59))
        im.paste(ppt_scaled, (ppt_x, ppt_y))

    # =========================================================================
    # 5. FOOTER (y = 905 .. 965)
    # =========================================================================
    draw.text((45, 915), "DATALARIA.COM \u2022 EXECUTIVE DECISION SUPPORT", font=f_footer_b, fill=(100, 116, 139))
    sub_foot = (
        "Estándar CMMI-DEV V2.0 DAR & Kepner-Tregoe Rational Management"
        if is_es else
        "CMMI-DEV V2.0 DAR & Kepner-Tregoe Rational Management Standards"
    )
    draw.text((45, 935), sub_foot, font=f_footer_sub, fill=(71, 85, 105))

    center_text = (
        "Fórmulas 100% Auditables \u2022 Celdas Desbloqueadas \u2022 Compatibilidad MS Excel & Google Sheets"
        if is_es else
        "100% Auditable Formulas \u2022 Unlocked Input Cells \u2022 MS Excel & Google Sheets Compatibility"
    )
    draw.text((430, 925), center_text, font=f_footer, fill=(203, 213, 225))

    # Botón de Descarga Inmediata con icono vectorial
    btn_w = 215
    btn_x = W - 40 - btn_w
    btn_y = 915
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + 32], radius=6, fill=(15, 36, 58), outline=(56, 189, 248), width=1)
    draw_download_icon(draw, btn_x + 18, btn_y + 15, 5, (56, 189, 248))
    dl_badge = "Descarga Inmediata (.ZIP)" if is_es else "Instant Download (.ZIP)"
    draw.text((btn_x + 30, btn_y + 8), dl_badge, font=f_footer_b, fill=(56, 189, 248))

    return im


def main():
    os.makedirs(os.path.join(BASE_DIR, "static", "images", "recursos"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "es", "posts", "matriz-dar-cuantitativa"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "en", "posts", "quantitative-dar-matrix"), exist_ok=True)

    # 1. Vista previa en Español
    im_es = generate_preview_pack(lang="es")
    p_static_es = os.path.join(BASE_DIR, "static", "images", "recursos", "dar-preview-es.png")
    p_post_es = os.path.join(BASE_DIR, "content", "es", "posts", "matriz-dar-cuantitativa", "preview-pack.png")
    im_es.save(p_static_es, "PNG", optimize=True)
    im_es.save(p_post_es, "PNG", optimize=True)
    print(f"[OK] Generated ES: {p_static_es} and {p_post_es} ({im_es.size})")

    # 2. Vista previa en Inglés
    im_en = generate_preview_pack(lang="en")
    p_static_en = os.path.join(BASE_DIR, "static", "images", "recursos", "dar-preview-en.png")
    p_post_en = os.path.join(BASE_DIR, "content", "en", "posts", "quantitative-dar-matrix", "preview-pack.png")
    im_en.save(p_static_en, "PNG", optimize=True)
    im_en.save(p_post_en, "PNG", optimize=True)
    print(f"[OK] Generated EN: {p_static_en} and {p_post_en} ({im_en.size})")


if __name__ == "__main__":
    main()
