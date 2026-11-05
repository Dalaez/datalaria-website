#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Executive Decision Pack de la Matriz RICE & ICE Ágil en español e inglés:
- static/images/recursos/rice-ice-preview-es.png
- static/images/recursos/rice-ice-preview-en.png
- content/es/posts/matriz-rice-ice-priorizacion/preview-pack.png
- content/en/posts/rice-ice-prioritization-matrix/preview-pack.png

Cumple con el estándar visual de la Suite 02 (DAR, BCG, McKinsey/GE):
- Lienzo 1600 x 980 px Dark-Slate Tier-1.
- Header con badge, título y chips de entregables.
- Ventana izquierda: Excel .xlsx con Dashboard Ejecutivo, KPIs, Top 10 y dictamen.
- Ventana superior derecha: Guía Metodológica en PDF (páginas 1 y 2 reales vía pypdfium2).
- Ventana inferior derecha: Presentación Ejecutiva en PowerPoint .pptx (Slide 3 real vía PowerPoint COM).
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


def export_pptx_slide3(pptx_path):
    """Exporta la Diapositiva 3 de la presentación vía PowerPoint COM."""
    if not os.path.exists(pptx_path):
        return None
    import win32com.client
    temp_png = os.path.abspath("temp_slide3_export.png")
    app = win32com.client.Dispatch("PowerPoint.Application")
    try:
        pres = app.Presentations.Open(pptx_path, WithWindow=False)
        slide = pres.Slides(3)
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
    draw.rounded_rectangle([40, 26, 440, 48], radius=6, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw_sparkle(draw, 55, 37, 6, (56, 189, 248))
    badge_text = "EXECUTIVE DECISION PACK • PRIORIZACIÓN ÁGIL" if is_es else "EXECUTIVE DECISION PACK • AGILE PRIORITIZATION"
    draw.text((68, 30), badge_text, font=f_badge, fill=(56, 189, 248))

    # Título Principal
    title_text = "MATRIZ RICE & ICE DE PRIORIZACIÓN ÁGIL" if is_es else "AGILE RICE & ICE PRIORITIZATION MATRIX"
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    # Subtítulo
    sub_text = (
        "BACKLOG CUANTITATIVO, MATRIZ IMPACTO/ESFUERZO, LÍNEA DE CORTE & ROADMAP C-LEVEL"
        if is_es else
        "QUANTITATIVE BACKLOG, IMPACT/EFFORT MATRIX, CAPACITY CUT-LINE & C-LEVEL ROADMAP"
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
    title_win_es = "Excel .xlsx — Motor Cuantitativo & Dashboard de Decisión RICE [Protegido]"
    title_win_en = "Excel .xlsx — Quantitative Engine & RICE Decision Dashboard [Protected]"
    draw_window_header(draw, wx, wy, ww, 34, title_win_es if is_es else title_win_en, (16, 124, 65), f_win_title)

    # Formula Bar
    draw.rectangle([wx, wy + 34, wx + ww, wy + 62], fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    fx_text_es = 'fx: =SI(O(F8=""; I8=""; I8<=0); ""; (E8*J8*K8)/H8)'
    fx_text_en = 'fx: =IF(OR(F8="", I8="", I8<=0), "", (E8*J8*K8)/H8)'
    draw.text((wx + 15, wy + 41), fx_text_es if is_es else fx_text_en, font=f_formula, fill=(71, 85, 105))

    # Inner Content Area
    # Banner Directivo
    bx, by, bw, bh = wx + 12, wy + 68, ww - 24, 28
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=4, fill=(15, 23, 42))
    b_text_es = "CUADRO DE MANDO EJECUTIVO: PRIORIZACIÓN ÁGIL RICE & ROADMAP C-LEVEL"
    b_text_en = "EXECUTIVE DASHBOARD: AGILE RICE PRIORITIZATION & C-SUITE ROADMAP"
    bbox_b = f_th.getbbox(b_text_es if is_es else b_text_en)
    draw.text((bx + (bw - (bbox_b[2] - bbox_b[0])) // 2, by + 7), b_text_es if is_es else b_text_en, font=f_th, fill=(255, 255, 255))

    # Metadata Row
    my = by + bh + 4
    draw.rectangle([bx, my, bx + bw, my + 20], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    m_info_es = "Portfolio: Plataforma Cloud & SaaS   •   Horizonte: Q1-Q4 Plan Estratégico   •   Fecha: 2026-11-05   •   Sponsor: CPO & Board"
    m_info_en = "Portfolio: Enterprise Cloud & SaaS   •   Horizon: Q1-Q4 Strategic Roadmap   •   Updated: 2026-11-05   •   Sponsor: CPO & Board"
    draw.text((bx + 12, my + 4), m_info_es if is_es else m_info_en, font=f_kpi_sub, fill=(71, 85, 105))

    # 5 KPI Cards
    ky = my + 26
    kw = (bw - 20) // 5
    kh = 52
    kpis_es = [
        ("INICIATIVAS EVALUADAS", "20", "Backlog estructurado", (37, 99, 235)),
        ("% VALOR TOP 20%", "54.2%", "Concentración en Top 4", (16, 185, 129)),
        ("UTILIZACIÓN CAPACIDAD", "84.5%", "Esfuerzo / Capacidad neta", (217, 119, 6)),
        ("FUERA DE CAPACIDAD", "5", "Iniciativas diferidas", (239, 68, 68)),
        ("QUICK WINS IDENTIFICADOS", "5", "Alto impacto & bajo esfuerzo", (16, 185, 129)),
    ]
    kpis_en = [
        ("EVALUATED INITIATIVES", "20", "Structured backlog items", (37, 99, 235)),
        ("TOP 20% VALUE SHARE", "54.2%", "Concentrated in Top 4", (16, 185, 129)),
        ("CAPACITY UTILIZATION", "84.5%", "Effort vs Net Capacity", (217, 119, 6)),
        ("CUT-LINE EXCLUSIONS", "5", "Deferred / Frozen backlog", (239, 68, 68)),
        ("QUICK WINS IDENTIFIED", "5", "High impact & low effort", (16, 185, 129)),
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

    # Top 10 Dynamic Ranking Section Title
    sy = ky + kh + 10
    draw.rounded_rectangle([bx, sy, bx + bw, sy + 22], radius=4, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    s_title = "RANKING TOP 10 RICE (MOTOR DINÁMICO LARGE + INDEX/MATCH)" if is_es else "TOP 10 DYNAMIC RICE RANKING (LARGE + INDEX/MATCH RESOLUTION)"
    draw.text((bx + 10, sy + 4), s_title, font=f_th, fill=(37, 99, 235))

    # Table Header
    ty = sy + 26
    draw.rectangle([bx, ty, bx + bw, ty + 24], fill=(30, 41, 59))
    headers_es = [("Pos", 32), ("ID", 50), ("Iniciativa / Funcionalidad Priorizada", 310), ("Score RICE", 78), ("Norm.", 55), ("Valor (RxIxC)", 85), ("Cuadrante", 100), ("Trim.", 50), ("Línea de Corte", 120)]
    headers_en = [("Pos", 32), ("ID", 50), ("Prioritized Initiative / Feature", 310), ("RICE Score", 78), ("Norm.", 55), ("Value (RxIxC)", 85), ("Quadrant", 100), ("Qtr.", 50), ("Capacity Cut-Line", 120)]
    headers = headers_es if is_es else headers_en

    hx = bx
    for h_txt, h_w in headers:
        draw.text((hx + 6, ty + 5), h_txt, font=f_th, fill=(255, 255, 255))
        hx += h_w

    # Table Rows
    rows_es = [
        ("1", "INIT-18", "2FA Obligatorio SMS / TOTP", "33.333,3", "100.0", "20.000", "⭐ Quick Win", "Q1", "✅ Dentro capacidad", (16, 185, 129)),
        ("2", "INIT-15", "Autenticación SSO Google / SAML 2.0", "12.000,0", "36.0", "18.000", "⭐ Quick Win", "Q1", "✅ Dentro capacidad", (16, 185, 129)),
        ("3", "INIT-03", "Exportación Masiva Informes CSV / XLSX", "10.000,0", "30.0", "10.000", "⭐ Quick Win", "Q1", "✅ Dentro capacidad", (16, 185, 129)),
        ("4", "INIT-05", "Webhooks Salientes en Tiempo Real", "8.888,9", "26.7", "16.000", "⭐ Quick Win", "Q1", "✅ Dentro capacidad", (16, 185, 129)),
        ("5", "INIT-01", "Onboarding Interactivo Self-Serve PWA", "8.000,0", "24.0", "24.000", "⭐ Quick Win", "Q1", "✅ Dentro capacidad", (16, 185, 129)),
        ("6", "INIT-08", "Motor de Recomendación Basado en IA", "6.400,0", "19.2", "32.000", "🚀 Gran Apuesta", "Q2", "✅ Dentro capacidad", (37, 99, 235)),
        ("7", "INIT-12", "Facturación Recurrente Stripe Billing", "4.800,0", "14.4", "12.000", "🚀 Gran Apuesta", "Q2", "✅ Dentro capacidad", (37, 99, 235)),
        ("8", "INIT-04", "Modo Oscuro & Accesibilidad WCAG 2.1", "4.000,0", "12.0", "2.000", "📦 Relleno", "Q3", "✅ Dentro capacidad", (100, 116, 139)),
        ("9", "INIT-14", "API Gateway GraphQL Unificada", "1.142,9", "3.4", "8.000", "🛑 Pozo sin Fondo", "Desc.", "⛔ Fuera de corte", (239, 68, 68)),
        ("10", "INIT-19", "Reescritura de Microservicios en Rust", "285,7", "0.9", "4.000", "🛑 Pozo sin Fondo", "Desc.", "⛔ Fuera de corte", (239, 68, 68)),
    ]
    rows_en = [
        ("1", "INIT-18", "Mandatory SMS / TOTP 2FA", "33,333.3", "100.0", "20,000", "⭐ Quick Win", "Q1", "✅ Within Capacity", (16, 185, 129)),
        ("2", "INIT-15", "SSO Google / SAML 2.0 Auth", "12,000.0", "36.0", "18,000", "⭐ Quick Win", "Q1", "✅ Within Capacity", (16, 185, 129)),
        ("3", "INIT-03", "Bulk CSV / XLSX Export Engine", "10,000.0", "30.0", "10,000", "⭐ Quick Win", "Q1", "✅ Within Capacity", (16, 185, 129)),
        ("4", "INIT-05", "Real-Time Outbound Webhooks", "8,888.9", "26.7", "16,000", "⭐ Quick Win", "Q1", "✅ Within Capacity", (16, 185, 129)),
        ("5", "INIT-01", "Self-Serve PWA User Onboarding", "8,000.0", "24.0", "24,000", "⭐ Quick Win", "Q1", "✅ Within Capacity", (16, 185, 129)),
        ("6", "INIT-08", "AI Recommendation Engine", "6,400.0", "19.2", "32,000", "🚀 Big Bet", "Q2", "✅ Within Capacity", (37, 99, 235)),
        ("7", "INIT-12", "Automated Stripe Billing Engine", "4,800.0", "14.4", "12,000", "🚀 Big Bet", "Q2", "✅ Within Capacity", (37, 99, 235)),
        ("8", "INIT-04", "Dark Mode & WCAG Accessibility", "4,000.0", "12.0", "2,000", "📦 Fill-in", "Q3", "✅ Within Capacity", (100, 116, 139)),
        ("9", "INIT-14", "Unified GraphQL API Gateway", "1,142.9", "3.4", "8,000", "🛑 Money Pit", "Def.", "⛔ Exceeds Cut-Line", (239, 68, 68)),
        ("10", "INIT-19", "Backend Rewrite in Rust", "285.7", "0.9", "4,000", "🛑 Money Pit", "Def.", "⛔ Exceeds Cut-Line", (239, 68, 68)),
    ]
    rows = rows_es if is_es else rows_en

    row_h = 24
    for r_i, r_data in enumerate(rows):
        ry = ty + 24 + r_i * row_h
        bg_col = (255, 255, 255) if (r_i % 2 == 0) else (248, 250, 252)
        if "⛔" in r_data[8]:
            bg_col = (254, 242, 242)  # Soft red for cut-line exclusions
        elif "⭐" in r_data[6]:
            bg_col = (240, 253, 244)  # Soft green for Quick Wins

        draw.rectangle([bx, ry, bx + bw, ry + row_h], fill=bg_col, outline=(241, 245, 249), width=1)

        rx = bx
        for col_idx, (val, (h_txt, h_w)) in enumerate(zip(r_data[:9], headers)):
            f_use = f_td_b if col_idx in [0, 1, 3, 6, 8] else f_td
            c_fill = (15, 23, 42)
            if col_idx == 3:
                c_fill = (37, 99, 235)  # Blue for score
            elif col_idx == 6 or col_idx == 8:
                c_fill = r_data[9]      # Status color

            draw.text((rx + 6, ry + 4), str(val), font=f_use, fill=c_fill)
            rx += h_w

    # Dictamen y Recomendaciones Ejecutivas (Bottom of Excel)
    dy = ty + 24 + len(rows) * row_h + 8
    draw.rounded_rectangle([bx, dy, bx + bw, dy + 70], radius=5, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    d_title = "DICTAMEN ESTRATÉGICO & RECOMENDACIONES VINCULANTES DEL COMITÉ (C-LEVEL)" if is_es else "C-SUITE STRATEGIC VERDICT & EXECUTIVE RECOMMENDATIONS"
    draw.text((bx + 10, dy + 6), d_title, font=f_th, fill=(30, 41, 59))

    d_b1 = (
        "• Prioridad #1: INIT-18 (2FA Obligatorio, Score 33.333,3) concentra la mayor densidad de valor por persona-mes.\n"
        "• 5 Quick Wins capturan el 54% del valor con solo 7.5 PM de esfuerzo (Q1). Congelar de inmediato INIT-19 e INIT-14 (21 PM)."
        if is_es else
        "• #1 Priority: INIT-18 (Mandatory 2FA, Score 33,333.3) delivers the highest verified value density per person-month.\n"
        "• 5 Quick Wins capture 54% of portfolio value with only 7.5 PM effort (Q1). Freeze INIT-19 & INIT-14 (21 PM reclaimed)."
    )
    draw.text((bx + 10, dy + 24), d_b1, font=f_td, fill=(71, 85, 105))

    # Pestañas inferiores de la hoja de cálculo
    tab_y = wy + wh - 30
    draw.rectangle([wx, tab_y, wx + ww, wy + wh], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    tabs = [
        ("Dashboard Ejecutivo" if is_es else "Executive Dashboard", (16, 124, 65), True),
        ("Backlog RICE" if is_es else "RICE Backlog", (100, 116, 139), False),
        ("Experimentos ICE" if is_es else "ICE Experiments", (100, 116, 139), False),
        ("Capacidad & Roadmap" if is_es else "Capacity & Roadmap", (100, 116, 139), False),
        ("Escalas & Calibración" if is_es else "Scales & Calibration", (100, 116, 139), False),
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
    folder = "[ES]_Matriz_RICE_ICE" if is_es else "[EN]_RICE_ICE_Matrix"
    fname_pdf = "Guia_Metodologica_RICE_ICE_ES.pdf" if is_es else "Methodology_Guide_RICE_ICE_EN.pdf"
    pdf_path = os.path.join(BASE_DIR, "packages", "Suite_02_Toma_Decisiones", "02_Matriz_RICE_ICE_Agil", folder, fname_pdf)

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

        lbl_p1 = "Pág. 1: Encuadre & Algoritmo RICE" if is_es else "Page 1: Scope & RICE Algorithm"
        lbl_p2 = "Pág. 2: Descuento Bayesiano & Capacidad" if is_es else "Page 2: Bayesian Discount & Capacity"
        draw.text((start_x + 6, start_y + pdf_target_h + 6), lbl_p1, font=f_page_lbl, fill=(148, 163, 184))
        draw.text((start_x + pdf_target_w + gap + 6, start_y + pdf_target_h + 6), lbl_p2, font=f_page_lbl, fill=(148, 163, 184))

    # =========================================================================
    # 4. BOTTOM-RIGHT WINDOW: CAPTURA REAL SLIDE 3 PPTX (x=985, y=505, w=575, h=375)
    # =========================================================================
    sx, sy, sw, sh = 985, 505, 575, 375
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pptx_title_es = "Presentación Grado Consejo (.pptx 16:9 Widescreen)"
    pptx_title_en = "Boardroom Presentation (.pptx 16:9 Widescreen)"
    draw_window_header(draw, sx, sy, sw, 34, pptx_title_es if is_es else pptx_title_en, (194, 65, 12), f_win_title)

    fname_ppt = "Presentacion_RICE_ICE_CLevel_ES.pptx" if is_es else "Deck_RICE_ICE_CLevel_EN.pptx"
    pptx_path = os.path.join(BASE_DIR, "packages", "Suite_02_Toma_Decisiones", "02_Matriz_RICE_ICE_Agil", folder, fname_ppt)
    ppt_slide = export_pptx_slide3(pptx_path)

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
        "Estándar Intercom RICE & Growth Hacking ICE • C-Level Audit Ready"
        if is_es else
        "Intercom RICE & Growth Hacking ICE Standards • C-Level Audit Ready"
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
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + 32], radius=6, fill=(15, 36, 58), outline=(56, 189, 248), width=1)
    draw_download_icon(draw, btn_x + 18, btn_y + 15, 5, (56, 189, 248))
    dl_badge = "Descarga Inmediata (.ZIP)" if is_es else "Instant Download (.ZIP)"
    draw.text((btn_x + 30, btn_y + 8), dl_badge, font=f_footer_b, fill=(56, 189, 248))

    return im


def main():
    os.makedirs(os.path.join(BASE_DIR, "static", "images", "recursos"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "es", "posts", "matriz-rice-ice-priorizacion"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "en", "posts", "rice-ice-prioritization-matrix"), exist_ok=True)

    # 1. Vista previa en Español
    print("Generando vista previa en Español (ES)...")
    im_es = generate_preview_pack(lang="es")
    p_static_es = os.path.join(BASE_DIR, "static", "images", "recursos", "rice-ice-preview-es.png")
    p_post_es = os.path.join(BASE_DIR, "content", "es", "posts", "matriz-rice-ice-priorizacion", "preview-pack.png")
    im_es.save(p_static_es, "PNG", optimize=True)
    im_es.save(p_post_es, "PNG", optimize=True)
    print(f"  [OK] Generado ES: {p_static_es} y {p_post_es} ({im_es.size})")

    # 2. Vista previa en Inglés
    print("Generando vista previa en Inglés (EN)...")
    im_en = generate_preview_pack(lang="en")
    p_static_en = os.path.join(BASE_DIR, "static", "images", "recursos", "rice-ice-preview-en.png")
    p_post_en = os.path.join(BASE_DIR, "content", "en", "posts", "rice-ice-prioritization-matrix", "preview-pack.png")
    im_en.save(p_static_en, "PNG", optimize=True)
    im_en.save(p_post_en, "PNG", optimize=True)
    print(f"  [OK] Generado EN: {p_static_en} y {p_post_en} ({im_en.size})")

    print("\nGeneración de vistas previas completada con éxito.")


if __name__ == "__main__":
    main()
