#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Executive Decision Pack de la Matriz RACI Cuantitativa & Balance de Carga en español e inglés:
- static/images/recursos/raci-preview-es.png
- static/images/recursos/raci-preview-en.png
- content/es/posts/matriz-raci-balance-carga/preview-pack.png
- content/en/posts/quantitative-raci-workload-matrix/preview-pack.png

Cumple con el estándar visual de las Suites de Datalaria (Suite 01, Suite 02, Suite 03):
- Lienzo 1600 x 980 px Dark-Slate Tier-1.
- Header con badge, título y chips de entregables.
- Ventana izquierda: Excel .xlsx con Dashboard Ejecutivo, KPIs, tabla de saturación y dictamen.
- Ventana superior derecha: Guía Metodológica en PDF (páginas 1 y 2 reales vía pypdfium2).
- Ventana inferior derecha: Presentación Ejecutiva en PowerPoint .pptx (Slide 2 real vía PowerPoint COM).
- Footer con marcas de auditoría, compatibilidad y descarga inmediata (.ZIP).
"""

import os
from PIL import Image, ImageDraw, ImageFont
import pypdfium2

# Directorio raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


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
    """Dibuja una estrella estilizada de 4 puntas."""
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
    """Icono vectorial de descarga."""
    draw.rectangle([cx - 2, cy - r, cx + 2, cy + 2], fill=fill)
    draw.polygon([(cx - int(r * 0.8), cy + 1), (cx + int(r * 0.8), cy + 1), (cx, cy + r + 1)], fill=fill)
    draw.line([(cx - r, cy + r + 3), (cx + r, cy + r + 3)], fill=fill, width=2)


def render_pdf_pages(pdf_path):
    """Renderiza páginas 1 y 2 de la guía metodológica PDF con pypdfium2."""
    if not os.path.exists(pdf_path):
        return None, None
    doc = pypdfium2.PdfDocument(pdf_path)
    p1 = doc[0].render(scale=2.5).to_pil()
    p2 = doc[1].render(scale=2.5).to_pil()
    return p1, p2


def export_pptx_slide2(pptx_path):
    """Exporta la Diapositiva 2 de la presentación vía PowerPoint COM."""
    if not os.path.exists(pptx_path):
        return None
    import win32com.client
    temp_png = os.path.abspath("temp_raci_slide2_export.png")
    app = win32com.client.Dispatch("PowerPoint.Application")
    try:
        pres = app.Presentations.Open(pptx_path, WithWindow=False)
        slide = pres.Slides(2)
        slide.Export(temp_png, "PNG", 1920, 1080)
        pres.Close()
    finally:
        app.Quit()

    if os.path.exists(temp_png):
        img = Image.open(temp_png).copy()
        os.remove(temp_png)
        return img
    return None


def generate_preview_pack(lang="es"):
    is_es = (lang == "es")
    W, H = 1600, 980
    im = Image.new("RGB", (W, H), (11, 17, 32))  # Deep Slate Navy #0B1120
    draw = ImageDraw.Draw(im)

    # Borde exterior general
    draw.rounded_rectangle([15, 15, W - 15, H - 15], radius=16, outline=(30, 41, 59), width=2)

    # Fuentes
    f_badge = get_font(12, bold=True)
    f_title = get_font(26, bold=True)
    f_subtitle = get_font(12.5, bold=False)
    f_pill = get_font(12, bold=True)
    f_win_title = get_font(13, bold=True)
    f_formula = get_font(10.5, bold=False)
    f_tab = get_font(10, bold=True)
    f_page_lbl = get_font(9.5, bold=True)
    f_footer = get_font(11, bold=False)
    f_footer_b = get_font(11, bold=True)
    f_footer_sub = get_font(10, bold=False)

    f_kpi_lbl = get_font(8.5, bold=True)
    f_kpi_val = get_font(16, bold=True)
    f_kpi_sub = get_font(8, bold=False)

    f_th = get_font(9, bold=True)
    f_td = get_font(8.5, bold=False)
    f_td_b = get_font(8.5, bold=True)

    # =========================================================================
    # 1. HEADER (y = 25 .. 105)
    # =========================================================================
    draw.rounded_rectangle([40, 26, 470, 48], radius=6, fill=(15, 36, 58), outline=(13, 148, 136), width=1)
    draw_sparkle(draw, 55, 37, 6, (45, 212, 191))
    badge_text = "EXECUTIVE DECISION PACK • CONTROL OPERATIVO & GOBERNANZA" if is_es else "EXECUTIVE DECISION PACK • OPERATIONAL GOVERNANCE & CONTROL"
    draw.text((68, 30), badge_text, font=f_badge, fill=(45, 212, 191))

    # Título Principal
    title_text = "MATRIZ RACI CUANTITATIVA & BALANCE DE CARGA" if is_es else "QUANTITATIVE RACI MATRIX & WORKLOAD BALANCING"
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    # Subtítulo
    sub_text = (
        "AUDITORÍA DETERMINISTA DE ACCOUNTABLE ÚNICO, RATIO DE SATURACIÓN Y PLAN DE REBALANCEO C-LEVEL"
        if is_es else
        "DETERMINISTIC SINGLE ACCOUNTABILITY AUDIT, SATURATION RATIOS & C-SUITE REBALANCING PLAN"
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
    # 2. LEFT WINDOW: EXCEL DASHBOARD (x=40, y=115, w=925, h=765)
    # =========================================================================
    wx, wy, ww, wh = 40, 115, 925, 765
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(255, 255, 255), outline=(51, 65, 85), width=2)

    # Titlebar (Excel Green #107C41)
    title_win_es = "Excel .xlsx — Motor Cuantitativo & Dashboard RACI [Protegido]"
    title_win_en = "Excel .xlsx — Quantitative Engine & RACI Dashboard [Protected]"
    draw_window_header(draw, wx, wy, ww, 34, title_win_es if is_es else title_win_en, (16, 124, 65), f_win_title)

    # Formula Bar
    draw.rectangle([wx, wy + 34, wx + ww, wy + 62], fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    fx_text_es = 'fx: =SI(Y(D14=1; E14>=1); "OK"; SI(D14=0; "CRÍTICO: Sin A"; SI(D14>1; "ERROR: Múltiple A"; "ALERTA: Sin R")))'
    fx_text_en = 'fx: =IF(AND(D14=1, E14>=1), "OK", IF(D14=0, "CRITICAL: No A", IF(D14>1, "ERROR: Multiple A", "ALERT: No R")))'
    draw.text((wx + 15, wy + 41), fx_text_es if is_es else fx_text_en, font=f_formula, fill=(71, 85, 105))

    # Inner Content Area
    # Banner Directivo
    bx, by, bw, bh = wx + 12, wy + 68, ww - 24, 28
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=4, fill=(15, 23, 42))
    b_text_es = "CUADRO DE MANDO EJECUTIVO: GOBERNANZA RACI, BALANCE DE CARGA & PMO C-LEVEL"
    b_text_en = "EXECUTIVE DASHBOARD: RACI GOVERNANCE, WORKLOAD BALANCING & C-SUITE PMO"
    bbox_b = f_th.getbbox(b_text_es if is_es else b_text_en)
    draw.text((bx + (bw - (bbox_b[2] - bbox_b[0])) // 2, by + 7), b_text_es if is_es else b_text_en, font=f_th, fill=(255, 255, 255))

    # Metadata Row
    my = by + bh + 4
    draw.rectangle([bx, my, bx + bw, my + 20], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    m_info_es = "Proyecto: Migración Cloud & ERP Core   •   Alcance: 25 Entregables WBS   •   Fecha: 2026-11-12   •   Sponsor: COO & PMO Director"
    m_info_en = "Project: Cloud Core ERP Migration   •   Scope: 25 WBS Deliverables   •   Updated: 2026-11-12   •   Sponsor: COO & PMO Director"
    draw.text((bx + 12, my + 4), m_info_es if is_es else m_info_en, font=f_kpi_sub, fill=(71, 85, 105))

    # 5 KPI Cards
    ky = my + 26
    kw = (bw - 20) // 5
    kh = 52
    kpis_es = [
        ("ENTREGABLES WBS", "25", "Paquetes evaluados", (37, 99, 235)),
        ("ÍNDICE SALUD RACI", "92.0%", "Conformidad Regla Áurea", (16, 185, 129)),
        ("ROL MÁS SATURADO", "152.0%", "Tech Lead / Arquitecto", (225, 29, 72)),
        ("ÍNDICE GINI CARGA", "0.412", "Desbalance operativo >0.35", (217, 119, 6)),
        ("ANOMALÍAS DETECTADAS", "2", "1 Múltiple A, 1 Sin R", (225, 29, 72)),
    ]
    kpis_en = [
        ("TOTAL WBS ITEMS", "25", "Audited deliverables", (37, 99, 235)),
        ("RACI HEALTH INDEX", "92.0%", "Golden Rule compliance", (16, 185, 129)),
        ("MAX SATURATION ROLE", "152.0%", "Tech Lead / Architect", (225, 29, 72)),
        ("GINI WORKLOAD INDEX", "0.412", "Operational inequality >0.35", (217, 119, 6)),
        ("GOVERNANCE ANOMALIES", "2", "1 Multiple A, 1 Orphan R", (225, 29, 72)),
    ]
    kpis = kpis_es if is_es else kpis_en
    for i, (k_lbl, k_val, k_sub, k_col) in enumerate(kpis):
        kx = bx + i * (kw + 5)
        draw.rounded_rectangle([kx, ky, kx + kw, ky + kh], radius=5, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        # Top banner of KPI
        draw.rounded_rectangle([kx, ky, kx + kw, ky + 16], radius=4, fill=(30, 41, 59))
        draw.rectangle([kx, ky + 10, kx + kw, ky + 16], fill=(30, 41, 59))
        draw.text((kx + 6, ky + 2), k_lbl, font=f_kpi_lbl, fill=(255, 255, 255))
        draw.text((kx + 8, ky + 18), k_val, font=f_kpi_val, fill=k_col)
        draw.text((kx + 8, ky + 36), k_sub, font=f_kpi_sub, fill=(100, 116, 139))

    # Section Title: Balance de Carga por Rol
    sy = ky + kh + 10
    draw.rounded_rectangle([bx, sy, bx + bw, sy + 22], radius=4, fill=(240, 253, 250), outline=(153, 246, 228), width=1)
    s_title = "BALANCE DE CARGA OPERATIVA & DETECCIÓN DE CUELLOS DE BOTELLA POR ROL" if is_es else "OPERATIONAL WORKLOAD BALANCING & BOTTLENECK DETECTION BY ROLE"
    draw.text((bx + 10, sy + 4), s_title, font=f_th, fill=(13, 148, 136))

    # Table Header
    ty = sy + 26
    draw.rectangle([bx, ty, bx + bw, ty + 24], fill=(30, 41, 59))
    headers_es = [("Pos", 32), ("Rol Organizativo / Departamento", 250), ("Capacidad (h)", 95), ("Carga (h)", 85), ("Saturación", 85), ("A", 40), ("R", 40), ("C", 40), ("I", 40), ("Semáforo Riesgo Operativo", 194)]
    headers_en = [("Pos", 32), ("Organizational Role / Department", 250), ("Capacity (h)", 95), ("Load (h)", 85), ("Saturation", 85), ("A", 40), ("R", 40), ("C", 40), ("I", 40), ("Operational Risk Level", 194)]
    headers = headers_es if is_es else headers_en

    hx = bx
    for h_txt, h_w in headers:
        draw.text((hx + 6, ty + 5), h_txt, font=f_th, fill=(255, 255, 255))
        hx += h_w

    # Table Rows (8 Roles)
    rows_es = [
        ("1", "Tech Lead / Arquitecto", "160.0 h", "243.2 h", "152.0%", "8", "12", "3", "2", "⛔ Sobrecarga Crítica (Cuello de Botella)", (225, 29, 72)),
        ("2", "Project Manager / PMO", "160.0 h", "198.4 h", "124.0%", "10", "8", "4", "3", "⛔ Sobrecarga Crítica (Cuello de Botella)", (225, 29, 72)),
        ("3", "Equipo Desarrollo / SW", "320.0 h", "345.6 h", "108.0%", "2", "18", "2", "3", "⚠️ Alerta / Límite de Capacidad", (217, 119, 6)),
        ("4", "Operaciones / DevOps", "160.0 h", "142.5 h", "89.1%", "1", "6", "8", "4", "⚠️ Alerta / Límite de Capacidad", (217, 119, 6)),
        ("5", "Legal & Compliance", "80.0 h", "65.5 h", "81.9%", "1", "2", "5", "3", "⚠️ Alerta / Límite de Capacidad", (217, 119, 6)),
        ("6", "QA & Testing", "160.0 h", "104.0 h", "65.0%", "1", "5", "6", "4", "✅ Carga Saludable (<80%)", (16, 185, 129)),
        ("7", "Sponsor / Comité Directivo", "40.0 h", "24.0 h", "60.0%", "1", "0", "10", "5", "✅ Carga Saludable (<80%)", (16, 185, 129)),
        ("8", "Diseñador UX/UI", "160.0 h", "72.5 h", "45.3%", "1", "3", "4", "2", "✅ Carga Saludable (<80%)", (16, 185, 129)),
    ]
    rows_en = [
        ("1", "Tech Lead / Architect", "160.0 h", "243.2 h", "152.0%", "8", "12", "3", "2", "⛔ Critical Overload (Bottleneck)", (225, 29, 72)),
        ("2", "Project Manager / PMO", "160.0 h", "198.4 h", "124.0%", "10", "8", "4", "3", "⛔ Critical Overload (Bottleneck)", (225, 29, 72)),
        ("3", "Engineering Squad / Dev", "320.0 h", "345.6 h", "108.0%", "2", "18", "2", "3", "⚠️ Warning / Capacity Limit", (217, 119, 6)),
        ("4", "Operations / DevOps", "160.0 h", "142.5 h", "89.1%", "1", "6", "8", "4", "⚠️ Warning / Capacity Limit", (217, 119, 6)),
        ("5", "Legal & Compliance", "80.0 h", "65.5 h", "81.9%", "1", "2", "5", "3", "⚠️ Warning / Capacity Limit", (217, 119, 6)),
        ("6", "QA & Testing", "160.0 h", "104.0 h", "65.0%", "1", "5", "6", "4", "✅ Healthy Workload (<80%)", (16, 185, 129)),
        ("7", "Executive Sponsor / Board", "40.0 h", "24.0 h", "60.0%", "1", "0", "10", "5", "✅ Healthy Workload (<80%)", (16, 185, 129)),
        ("8", "UX/UI Designer", "160.0 h", "72.5 h", "45.3%", "1", "3", "4", "2", "✅ Healthy Workload (<80%)", (16, 185, 129)),
    ]
    rows = rows_es if is_es else rows_en

    row_h = 24
    for r_i, r_data in enumerate(rows):
        ry = ty + 24 + r_i * row_h
        bg_col = (255, 255, 255) if (r_i % 2 == 0) else (248, 250, 252)
        if "⛔" in r_data[9]:
            bg_col = (254, 242, 242)  # Soft red
        elif "⚠️" in r_data[9]:
            bg_col = (255, 251, 235)  # Soft amber

        draw.rectangle([bx, ry, bx + bw, ry + row_h], fill=bg_col, outline=(241, 245, 249), width=1)

        rx = bx
        for col_idx, (val, (h_txt, h_w)) in enumerate(zip(r_data[:10], headers)):
            f_use = f_td_b if col_idx in [0, 1, 4, 9] else f_td
            c_fill = (15, 23, 42)
            if col_idx == 4:
                c_fill = r_data[10]     # Saturation color
            elif col_idx == 9:
                c_fill = r_data[10]     # Status color

            draw.text((rx + 6, ry + 4), str(val), font=f_use, fill=c_fill)
            rx += h_w

    # Dictamen y Recomendaciones Ejecutivas (Bottom of Excel)
    dy = ty + 24 + len(rows) * row_h + 8
    draw.rounded_rectangle([bx, dy, bx + bw, dy + 70], radius=5, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    d_title = "DICTAMEN DE GOBERNANZA & PLAN DE REBALANCEO C-LEVEL (APROBADO)" if is_es else "C-SUITE GOVERNANCE VERDICT & APPROVED REBALANCING PLAN"
    draw.text((bx + 10, dy + 6), d_title, font=f_th, fill=(30, 41, 59))

    d_b1 = (
        "• Auditoría RACI: 2 anomalías resueltas (Unicidad estricta de A en WBS 2.3 y asignación de ejecutor R en WBS 4.1).\n"
        "• Plan de Mitigación: Tech Lead al 152% rebalancea 4 tareas 'R' a Senior Devs y reduce 5 consultas 'C' a 'I' (Saturación final: 84%)."
        if is_es else
        "• RACI Audit: 2 anomalies resolved (Strict single-A enforcement on WBS 2.3 and executor R assigned to WBS 4.1).\n"
        "• Mitigation Plan: Tech Lead at 152% delegates 4 'R' tasks to Senior Devs and trims 5 'C' consults to 'I' (Final Saturation: 84%)."
    )
    draw.text((bx + 10, dy + 24), d_b1, font=f_td, fill=(71, 85, 105))

    # Pestañas inferiores de la hoja de cálculo
    tab_y = wy + wh - 30
    draw.rectangle([wx, tab_y, wx + ww, wy + wh], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    tabs = [
        ("Dashboard Ejecutivo" if is_es else "Executive Dashboard", (16, 124, 65), True),
        ("Matriz RACI & Gobernanza" if is_es else "RACI Matrix & Governance", (100, 116, 139), False),
        ("Balance de Carga (Workload)" if is_es else "Workload Balancing", (100, 116, 139), False),
        ("Plan de Rebalanceo & Acción" if is_es else "Action & Rebalancing Plan", (100, 116, 139), False),
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
        tbx += (tbw + 8)

    # =========================================================================
    # 3. TOP-RIGHT WINDOW: CAPTURAS REALES GUÍA PDF (x=985, y=115, w=575, h=370)
    # =========================================================================
    px, py, pw, ph = 985, 115, 575, 370
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pdf_title_es = "Guía Metodológica Oficial (.pdf) — 5 Páginas C-Level"
    pdf_title_en = "Official Methodology Guide (.pdf) — 5 C-Level Pages"
    draw_window_header(draw, px, py, pw, 34, pdf_title_es if is_es else pdf_title_en, (30, 58, 138), f_win_title)

    # Cargar e incrustar Página 1 y Página 2 del PDF real
    folder = "[ES]_Matriz_RACI_Balance_Carga" if is_es else "[EN]_Quantitative_RACI_Workload"
    fname_pdf = "Guia_Metodologica_RACI_ES.pdf" if is_es else "Methodology_Guide_RACI_EN.pdf"
    pdf_path = os.path.join(BASE_DIR, "packages", "Suite_03_Control_Operativo", "01_Matriz_RACI_Balance_Carga", folder, fname_pdf)

    p1_img, p2_img = render_pdf_pages(pdf_path)
    if p1_img and p2_img:
        pdf_target_h = 300
        pdf_target_w = int(pdf_target_h * (p1_img.width / p1_img.height))

        p1_scaled = p1_img.resize((pdf_target_w, pdf_target_h), Image.Resampling.LANCZOS)
        p2_scaled = p2_img.resize((pdf_target_w, pdf_target_h), Image.Resampling.LANCZOS)

        gap = 25
        total_w = pdf_target_w * 2 + gap
        start_x = px + (pw - total_w) // 2
        start_y = py + 42

        # Marcos sutiles
        draw.rounded_rectangle([start_x - 3, start_y - 3, start_x + pdf_target_w + 3, start_y + pdf_target_h + 3], radius=4, fill=(30, 41, 59))
        draw.rounded_rectangle([start_x + pdf_target_w + gap - 3, start_y - 3, start_x + total_w + 3, start_y + pdf_target_h + 3], radius=4, fill=(30, 41, 59))

        im.paste(p1_scaled, (start_x, start_y))
        im.paste(p2_scaled, (start_x + pdf_target_w + gap, start_y))

        lbl_p1 = "Pág. 1: Gobernanza & Reglas Áureas" if is_es else "Page 1: Governance & Golden Rules"
        lbl_p2 = "Pág. 2: Ponderación FTE & Desbalance Gini" if is_es else "Page 2: FTE Weights & Gini Inequality"
        draw.text((start_x + 6, start_y + pdf_target_h + 6), lbl_p1, font=f_page_lbl, fill=(148, 163, 184))
        draw.text((start_x + pdf_target_w + gap + 6, start_y + pdf_target_h + 6), lbl_p2, font=f_page_lbl, fill=(148, 163, 184))

    # =========================================================================
    # 4. BOTTOM-RIGHT WINDOW: CAPTURA REAL SLIDE 2 PPTX (x=985, y=505, w=575, h=375)
    # =========================================================================
    sx, sy, sw, sh = 985, 505, 575, 375
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pptx_title_es = "Presentación Grado Consejo (.pptx 16:9 Widescreen)"
    pptx_title_en = "Boardroom Presentation (.pptx 16:9 Widescreen)"
    draw_window_header(draw, sx, sy, sw, 34, pptx_title_es if is_es else pptx_title_en, (194, 65, 12), f_win_title)

    fname_ppt = "Presentacion_RACI_CLevel_ES.pptx" if is_es else "Deck_RACI_CLevel_EN.pptx"
    pptx_path = os.path.join(BASE_DIR, "packages", "Suite_03_Control_Operativo", "01_Matriz_RACI_Balance_Carga", folder, fname_ppt)
    ppt_slide = export_pptx_slide2(pptx_path)

    if ppt_slide:
        ppt_target_w = 555
        ppt_target_h = int(ppt_target_w * (ppt_slide.height / ppt_slide.width))
        ppt_scaled = ppt_slide.resize((ppt_target_w, ppt_target_h), Image.Resampling.LANCZOS)

        ppt_x = sx + (sw - ppt_target_w) // 2
        ppt_y = sy + 34 + (sh - 34 - ppt_target_h) // 2

        draw.rounded_rectangle([ppt_x - 2, ppt_y - 2, ppt_x + ppt_target_w + 2, ppt_y + ppt_target_h + 2], radius=4, fill=(30, 41, 59))
        im.paste(ppt_scaled, (ppt_x, ppt_y))

    # =========================================================================
    # 5. FOOTER (y = 905 .. 965)
    # =========================================================================
    draw.text((45, 915), "DATALARIA.COM • EXECUTIVE DECISION SUPPORT", font=f_footer_b, fill=(100, 116, 139))
    sub_foot = (
        "Estándar PMBOK 7ª Edición & PRINCE2 • C-Level Governance Ready"
        if is_es else
        "PMBOK 7th Edition & PRINCE2 Standards • C-Level Governance Ready"
    )
    draw.text((45, 935), sub_foot, font=f_footer_sub, fill=(71, 85, 105))

    center_text = (
        "Fórmulas 100% Auditables • Celdas Desbloqueadas • Compatibilidad MS Excel & Google Sheets"
        if is_es else
        "100% Auditable Formulas • Unlocked Input Cells • MS Excel & Google Sheets Compatibility"
    )
    draw.text((430, 925), center_text, font=f_footer, fill=(203, 213, 225))

    # Botón de Descarga Inmediata con icono vectorial
    btn_w = 215
    btn_x = W - 40 - btn_w
    btn_y = 915
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + 32], radius=6, fill=(15, 36, 58), outline=(45, 212, 191), width=1)
    draw_download_icon(draw, btn_x + 18, btn_y + 15, 5, (45, 212, 191))
    dl_badge = "Descarga Inmediata (.ZIP)" if is_es else "Instant Download (.ZIP)"
    draw.text((btn_x + 30, btn_y + 8), dl_badge, font=f_footer_b, fill=(45, 212, 191))

    return im


def main():
    os.makedirs(os.path.join(BASE_DIR, "static", "images", "recursos"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "es", "posts", "matriz-raci-balance-carga"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "en", "posts", "quantitative-raci-workload-matrix"), exist_ok=True)

    # 1. Vista previa en Español
    print("Generando vista previa en Español (ES)...")
    im_es = generate_preview_pack(lang="es")
    p_static_es = os.path.join(BASE_DIR, "static", "images", "recursos", "raci-preview-es.png")
    p_post_es = os.path.join(BASE_DIR, "content", "es", "posts", "matriz-raci-balance-carga", "preview-pack.png")
    im_es.save(p_static_es, "PNG", optimize=True)
    im_es.save(p_post_es, "PNG", optimize=True)
    print(f"  [OK] Generado ES: {p_static_es} y {p_post_es} ({im_es.size})")

    # 2. Vista previa en Inglés
    print("Generando vista previa en Inglés (EN)...")
    im_en = generate_preview_pack(lang="en")
    p_static_en = os.path.join(BASE_DIR, "static", "images", "recursos", "raci-preview-en.png")
    p_post_en = os.path.join(BASE_DIR, "content", "en", "posts", "quantitative-raci-workload-matrix", "preview-pack.png")
    im_en.save(p_static_en, "PNG", optimize=True)
    im_en.save(p_post_en, "PNG", optimize=True)
    print(f"  [OK] Generado EN: {p_static_en} y {p_post_en} ({im_en.size})")

    print("\nGeneración de vistas previas RACI completada con éxito.")


if __name__ == "__main__":
    main()
