#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Executive Decision Pack del Business Case Financiero (VAN, TIR, Payback & Tornado)
en español e inglés:
- static/images/recursos/business-case-preview-es.png
- static/images/recursos/business-case-preview-en.png
- content/es/posts/business-case-financiero-van-tir/preview-pack.png
- content/en/posts/financial-business-case-npv-irr/preview-pack.png

Cumple con el estándar visual de la Suite 02 (DAR, RICE/ICE, BCG, McKinsey/GE):
- Lienzo 1600 x 980 px Dark-Slate Tier-1 (#0B1120).
- Header con badge, título y chips de entregables.
- Ventana izquierda: Excel .xlsx con Dashboard Ejecutivo DCF, KPIs, Semáforo Hurdle Policy y Proyección 5 Años.
- Ventana superior derecha: Guía Metodológica en PDF (páginas 1 y 2 reales vía pypdfium2).
- Ventana inferior derecha: Presentación Ejecutiva en PowerPoint .pptx (Slide 2 real Tornado & Escenarios vía PowerPoint COM).
- Footer con marcas de auditoría, compatibilidad y descarga inmediata (.ZIP).
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import pypdfium2

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
    draw.rounded_rectangle([x, y, x + w, y + h + 10], radius=8, fill=bg_color)
    draw.rectangle([x, y + h - 5, x + w, y + h], fill=bg_color)
    r = 5
    cy = y + h // 2
    draw.ellipse([x + 14 - r, cy - r, x + 14 + r, cy + r], fill=(255, 95, 86))   # Red
    draw.ellipse([x + 30 - r, cy - r, x + 30 + r, cy + r], fill=(255, 189, 46))  # Yellow
    draw.ellipse([x + 46 - r, cy - r, x + 46 + r, cy + r], fill=(39, 201, 63))   # Green
    bbox = font.getbbox(title)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (w - tw) // 2, cy - th // 2 - 2), title, font=font, fill=(255, 255, 255))


def draw_sparkle(draw, cx, cy, r, fill):
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
    draw.rectangle([cx - 2, cy - r, cx + 2, cy + 2], fill=fill)
    draw.polygon([(cx - int(r * 0.8), cy + 1), (cx + int(r * 0.8), cy + 1), (cx, cy + r + 1)], fill=fill)
    draw.line([(cx - r, cy + r + 3), (cx + r, cy + r + 3)], fill=fill, width=2)


def render_pdf_pages(pdf_path):
    if not os.path.exists(pdf_path):
        return None, None
    doc = pypdfium2.PdfDocument(pdf_path)
    p1 = doc[0].render(scale=2.5).to_pil()
    p2 = doc[1].render(scale=2.5).to_pil()
    return p1, p2


def export_pptx_slide(pptx_path, slide_idx=2):
    """Exporta la diapositiva especificada (por defecto Slide 2: Tornado & Escenarios) vía PowerPoint COM."""
    if not os.path.exists(pptx_path):
        return None
    try:
        import win32com.client
        temp_png = os.path.abspath(f"temp_slide_{slide_idx}_export.png")
        app = win32com.client.Dispatch("PowerPoint.Application")
        try:
            pres = app.Presentations.Open(pptx_path, WithWindow=False)
            slide = pres.Slides(slide_idx)
            slide.Export(temp_png, "PNG", 1920, 1080)
            pres.Close()
        finally:
            app.Quit()

        if os.path.exists(temp_png):
            img = Image.open(temp_png).copy()
            os.remove(temp_png)
            return img
    except Exception as e:
        print(f"Warning COM export: {e}")
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
    draw.rounded_rectangle([40, 26, 470, 48], radius=6, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw_sparkle(draw, 55, 37, 6, (56, 189, 248))
    badge_text = "EXECUTIVE DECISION PACK • FINANZAS CORPORATIVAS" if is_es else "EXECUTIVE DECISION PACK • CORPORATE FINANCE"
    draw.text((68, 30), badge_text, font=f_badge, fill=(56, 189, 248))

    # Título Principal
    title_text = "BUSINESS CASE FINANCIERO: VAN, TIR & SENSIBILIDAD TORNADO" if is_es else "FINANCIAL BUSINESS CASE: NPV, IRR & TORNADO SENSITIVITY"
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    # Subtítulo
    sub_text = (
        "MODELO DCF INSTITUCIONAL, WACC (CAPM), PAYBACK DESCONTADO, ESCENARIOS & STAGE GATES"
        if is_es else
        "INSTITUTIONAL DCF MODEL, WACC (CAPM), DISCOUNTED PAYBACK, SCENARIOS & STAGE GATES"
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
    title_win_es = "Excel .xlsx — Modelo Financiero DCF & Dashboard C-Level [Fórmulas Protegidas]"
    title_win_en = "Excel .xlsx — DCF Financial Model & C-Level Dashboard [Formulas Protected]"
    draw_window_header(draw, wx, wy, ww, 34, title_win_es if is_es else title_win_en, (16, 124, 65), f_win_title)

    # Formula Bar
    draw.rectangle([wx, wy + 34, wx + ww, wy + 62], fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    fx_text_es = 'fx: =SI(Y(\'Proyección DCF\'!$C$33>0; \'Proyección DCF\'!$C$34>=\'Supuestos & Drivers\'!$C$28+3%; ...); "✅ APROBAR"; "REVISAR")'
    fx_text_en = 'fx: =IF(AND(\'DCF Projection\'!$C$33>0, \'DCF Projection\'!$C$34>=\'Assumptions & Drivers\'!$C$28+3%, ...), "✅ APPROVE", "REVIEW")'
    draw.text((wx + 15, wy + 41), fx_text_es if is_es else fx_text_en, font=f_formula, fill=(71, 85, 105))

    # Inner Content Area
    # Banner Directivo
    bx, by, bw, bh = wx + 12, wy + 68, ww - 24, 28
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=4, fill=(15, 23, 42))
    b_text_es = "CUADRO DE MANDO EJECUTIVO: EVALUACIÓN FINANCIERA INSTITUCIONAL DCF"
    b_text_en = "EXECUTIVE DASHBOARD: INSTITUTIONAL DCF CAPITAL ALLOCATION APPRAISAL"
    bbox_b = f_th.getbbox(b_text_es if is_es else b_text_en)
    draw.text((bx + (bw - (bbox_b[2] - bbox_b[0])) // 2, by + 7), b_text_es if is_es else b_text_en, font=f_th, fill=(255, 255, 255))

    # Metadata Row
    my = by + bh + 4
    draw.rectangle([bx, my, bx + bw, my + 20], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    m_info_es = "Proyecto: Automatización Planta Industrial   •   CAPEX: 1.200.000 €   •   WACC: 9,50% (CAPM)   •   Dictamen: ✅ APROBAR"
    m_info_en = "Project: Manufacturing Line Automation   •   CAPEX: $1,200,000   •   WACC: 9.50% (CAPM)   •   Verdict: ✅ APPROVE"
    draw.text((bx + 12, my + 4), m_info_es if is_es else m_info_en, font=f_kpi_sub, fill=(71, 85, 105))

    # 5 KPI Cards
    ky = my + 26
    kw = (bw - 20) // 5
    kh = 52
    kpis_es = [
        ("VAN A 5 AÑOS (NPV)", "+693 k€", "Valor neto creado", (16, 185, 129)),
        ("TIR VS. WACC SPREAD", "28,89%", "+19,4 pp s/ WACC (9,5%)", (37, 99, 235)),
        ("PAYBACK DESCONTADO", "3,35 años", "Límite política: < 4,0 a.", (16, 185, 129)),
        ("PEAK FUNDING", "-995 k€", "Exposición máx. Año 1", (239, 68, 68)),
        ("VAN ESPERADO E[VAN]", "+741 k€", "Ponderado 3 escenarios", (217, 119, 6)),
    ]
    kpis_en = [
        ("5-YEAR NPV", "+$693k", "Net economic value", (16, 185, 129)),
        ("IRR VS WACC SPREAD", "28.89%", "+19.4 pp vs WACC (9.5%)", (37, 99, 235)),
        ("DISCOUNTED PAYBACK", "3.35 yrs", "Policy limit: < 4.0 yrs", (16, 185, 129)),
        ("PEAK FUNDING", "-$995k", "Max trough Year 1", (239, 68, 68)),
        ("EXPECTED NPV E[NPV]", "+$741k", "Probability-weighted", (217, 119, 6)),
    ]
    kpis = kpis_es if is_es else kpis_en
    for i, (k_lbl, k_val, k_sub, k_col) in enumerate(kpis):
        kx = bx + i * (kw + 5)
        draw.rounded_rectangle([kx, ky, kx + kw, ky + kh], radius=5, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([kx, ky, kx + kw, ky + 16], radius=4, fill=(30, 41, 59))
        draw.rectangle([kx, ky + 10, kx + kw, ky + 16], fill=(30, 41, 59))
        draw.text((kx + 6, ky + 2), k_lbl, font=f_kpi_lbl, fill=(255, 255, 255))
        draw.text((kx + 8, ky + 18), k_val, font=f_kpi_val, fill=k_col)
        draw.text((kx + 8, ky + 36), k_sub, font=f_kpi_sub, fill=(100, 116, 139))

    # Semáforo de Dictamen Ejecutivo
    dy = ky + kh + 8
    draw.rounded_rectangle([bx, dy, bx + bw, dy + 28], radius=5, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    dictamen_lbl = "DICTAMEN AUTOMÁTICO DE POLÍTICA: ✅ APROBAR INVERSIÓN" if is_es else "AUTOMATED HURDLE VERDICT: ✅ APPROVE CAPITAL EXPENDITURE"
    dictamen_sub = "Cumple holgadamente todos los criterios de la Hurdle Policy: VAN > 0, TIR ≥ WACC + 3 pp y Payback ≤ 4 años." if is_es else "Exceeds all corporate hurdle policy criteria: NPV > 0, IRR ≥ WACC + 3 pp, and Discounted Payback ≤ 4 yrs."
    draw.text((bx + 12, dy + 3), dictamen_lbl, font=f_th, fill=(22, 101, 52))
    draw.text((bx + 12, dy + 16), dictamen_sub, font=f_td, fill=(21, 128, 61))

    # Proyección DCF Consolidada Section Title
    sy = dy + 34
    draw.rounded_rectangle([bx, sy, bx + bw, sy + 22], radius=4, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    s_title = "ESTADO DE FLUJOS DE CAJA LIBRE DESCONTADOS (DCF) — AÑOS 0 A 5" if is_es else "DISCOUNTED FREE CASH FLOW (DCF) STATEMENT — YEARS 0 TO 5"
    draw.text((bx + 10, sy + 4), s_title, font=f_th, fill=(37, 99, 235))

    # Table Header
    ty = sy + 26
    draw.rectangle([bx, ty, bx + bw, ty + 24], fill=(30, 41, 59))
    headers_es = [("Línea de Proyección (k€)", 250), ("Año 0", 100), ("Año 1", 100), ("Año 2", 100), ("Año 3", 100), ("Año 4", 110), ("Año 5", 110)]
    headers_en = [("Projection Line Item ($k)", 250), ("Year 0", 100), ("Year 1", 100), ("Year 2", 100), ("Year 3", 100), ("Year 4", 110), ("Year 5", 110)]
    headers = headers_es if is_es else headers_en

    hx = bx
    for h_txt, h_w in headers:
        draw.text((hx + 6, ty + 5), h_txt, font=f_th, fill=(255, 255, 255))
        hx += h_w

    # DCF Rows
    rows_es = [
        ("Ingresos por Ventas (P x Q)", "-", "2.500,0", "2.677,5", "2.867,6", "3.071,2", "3.289,3"),
        ("Costes Variables (60% Ventas)", "-", "-1.500,0", "-1.606,5", "-1.720,6", "-1.842,7", "-1.973,6"),
        ("OPEX Fijo Anual", "-", "-250,0", "-257,5", "-265,2", "-273,2", "-281,4"),
        ("EBITDA Operativo", "-", "+750,0", "+813,5", "+881,8", "+955,3", "+1.034,3"),
        ("(-) Amortización Lineal (D&A)", "-", "-170,0", "-240,0", "-240,0", "-240,0", "-240,0"),
        ("EBIT (Resultado de Explotación)", "-", "+580,0", "+573,5", "+641,8", "+715,3", "+794,3"),
        ("(-) Impuestos Sociedades (t = 25%)", "-", "-145,0", "-143,4", "-160,5", "-178,8", "-198,6"),
        ("NOPAT (EBIT x (1 - t))", "-", "+435,0", "+430,1", "+481,4", "+536,5", "+595,7"),
        ("(+) Amortización Revertida", "-", "+170,0", "+240,0", "+240,0", "+240,0", "+240,0"),
        ("(-) Inversión CAPEX por Tramos", "-850,0", "-350,0", "0,0", "0,0", "0,0", "0,0"),
        ("(-) Variación Capital Circulante (ΔNWC)", "-", "-250,0", "-17,8", "-19,0", "-20,4", "-21,8"),
        ("FLUJO DE CAJA LIBRE (FCF)", "-850,0", "-145,0", "+501,3", "+550,1", "+602,8", "+659,7"),
        ("Factor Descuento WACC (9,50%)", "1,0000", "0,9132", "0,8340", "0,7617", "0,6956", "0,6352"),
        ("VALOR PRESENTE DEL FCF (VP)", "-850,0", "-132,4", "+418,1", "+419,0", "+419,3", "+419,1"),
        ("VP ACUMULADO (CURVA J)", "-850,0", "-982,4", "-564,4", "-145,4", "+274,0", "+693,0"),
    ]
    rows_en = [
        ("Gross Sales Revenue (P x Q)", "-", "2,500.0", "2,677.5", "2,867.6", "3,071.2", "3,289.3"),
        ("Variable Costs (60% Revenue)", "-", "-1,500.0", "-1,606.5", "-1,720.6", "-1,842.7", "-1,973.6"),
        ("Fixed Operating OPEX", "-", "-250.0", "-257.5", "-265.2", "-273.2", "-281.4"),
        ("Operating EBITDA", "-", "+750.0", "+813.5", "+881.8", "+955.3", "+1,034.3"),
        ("(-) Depreciation & Amortization", "-", "-170.0", "-240.0", "-240.0", "-240.0", "-240.0"),
        ("EBIT (Operating Income)", "-", "+580.0", "+573.5", "+641.8", "+715.3", "+794.3"),
        ("(-) Corporate Tax (t = 25%)", "-", "-145.0", "-143.4", "-160.5", "-178.8", "-198.6"),
        ("NOPAT (EBIT x (1 - t))", "-", "+435.0", "+430.1", "+481.4", "+536.5", "+595.7"),
        ("(+) Depreciation Add-back", "-", "+170.0", "+240.0", "+240.0", "+240.0", "+240.0"),
        ("(-) Phased CAPEX Disbursements", "-850.0", "-350.0", "0.0", "0.0", "0.0", "0.0"),
        ("(-) Working Capital Change (ΔNWC)", "-", "-250.0", "-17.8", "-19.0", "-20.4", "-21.8"),
        ("FREE CASH FLOW TO FIRM (FCF)", "-850.0", "-145.0", "+501.3", "+550.1", "+602.8", "+659.7"),
        ("Discount Factor (WACC = 9.50%)", "1.0000", "0.9132", "0.8340", "0.7617", "0.6956", "0.6352"),
        ("PRESENT VALUE OF FCF (PV)", "-850.0", "-132.4", "+418.1", "+419.0", "+419.3", "+419.1"),
        ("CUMULATIVE PV (J-CURVE)", "-850.0", "-982.4", "-564.4", "-145.4", "+274.0", "+693.0"),
    ]
    rows = rows_es if is_es else rows_en

    row_h = 22
    for r_i, r_data in enumerate(rows):
        ry = ty + 24 + r_i * row_h
        bg_col = (255, 255, 255) if (r_i % 2 == 0) else (248, 250, 252)
        if "FLUJO DE CAJA LIBRE" in r_data[0] or "FREE CASH FLOW" in r_data[0]:
            bg_col = (240, 253, 244)  # Highlight green
        elif "VP ACUMULADO" in r_data[0] or "CUMULATIVE PV" in r_data[0]:
            bg_col = (239, 246, 255)  # Highlight blue

        draw.rectangle([bx, ry, bx + bw, ry + row_h], fill=bg_col, outline=(241, 245, 249), width=1)

        rx = bx
        is_bold_row = r_i in [3, 5, 7, 11, 13, 14]
        for col_idx, (val, (h_txt, h_w)) in enumerate(zip(r_data, headers)):
            f_use = f_td_b if (is_bold_row or col_idx == 0) else f_td
            c_fill = (15, 23, 42)
            if col_idx > 0 and val.startswith("-"):
                c_fill = (220, 38, 38)
            elif col_idx > 0 and val.startswith("+"):
                c_fill = (16, 124, 65)
            elif r_i == 14 and col_idx == 6:
                c_fill = (37, 99, 235)  # Final NPV

            draw.text((rx + 6, ry + 4), val, font=f_use, fill=c_fill)
            rx += h_w

    # Bottom Sheet Tabs
    tab_y = wy + wh - 30
    draw.rectangle([wx, tab_y, wx + ww, wy + wh], fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    tabs_es = ["📊 Dashboard Ejecutivo", "⚙️ Supuestos & Drivers", "📈 Proyección DCF", "🌪️ Sensibilidad & Tornado", "📋 Plan Inversión & Gobernanza", "📖 Guía de Uso"]
    tabs_en = ["📊 Executive Dashboard", "⚙️ Assumptions & Drivers", "📈 DCF Projection", "🌪️ Sensitivity & Tornado", "📋 Investment Plan & Governance", "📖 User Guide"]
    tabs = tabs_es if is_es else tabs_en

    tx = wx + 15
    for t_idx, t_name in enumerate(tabs):
        bbox_t = f_tab.getbbox(t_name)
        tw = bbox_t[2] - bbox_t[0] + 16
        is_active = (t_idx == 0)
        t_bg = (255, 255, 255) if is_active else (226, 232, 240)
        t_fg = (16, 124, 65) if is_active else (100, 116, 139)
        draw.rounded_rectangle([tx, tab_y + 3, tx + tw, tab_y + 24], radius=3, fill=t_bg, outline=(203, 213, 225), width=1)
        draw.text((tx + 8, tab_y + 6), t_name, font=f_tab, fill=t_fg)
        tx += (tw + 6)

    # =========================================================================
    # 3. TOP-RIGHT WINDOW: GUÍA METODOLÓGICA EN PDF (x=985, y=115, w=575, h=370)
    # =========================================================================
    px_win, py_win, pw_win, ph_win = 985, 115, 575, 370
    draw.rounded_rectangle([px_win, py_win, px_win + pw_win, py_win + ph_win], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pdf_title_es = "Guía Metodológica Oficial (.pdf) — 5 Páginas C-Level"
    pdf_title_en = "Official Methodology Guide (.pdf) — 5 C-Level Pages"
    draw_window_header(draw, px_win, py_win, pw_win, 34, pdf_title_es if is_es else pdf_title_en, (30, 58, 138), f_win_title)

    # Cargar e incrustar Página 1 y Página 2 del PDF real
    folder = "[ES]_Business_Case_VAN_TIR" if is_es else "[EN]_Financial_Business_Case"
    fname_pdf = "Guia_Metodologica_Business_Case_ES.pdf" if is_es else "Methodology_Guide_Business_Case_EN.pdf"
    pdf_path = os.path.join(BASE_DIR, "packages", "Suite_02_Toma_Decisiones", "03_Business_Case_VAN_TIR", folder, fname_pdf)

    p1_img, p2_img = render_pdf_pages(pdf_path)
    if p1_img and p2_img:
        pdf_target_h = 300
        pdf_target_w = int(pdf_target_h * (p1_img.width / p1_img.height))

        p1_scaled = p1_img.resize((pdf_target_w, pdf_target_h), Image.Resampling.LANCZOS)
        p2_scaled = p2_img.resize((pdf_target_w, pdf_target_h), Image.Resampling.LANCZOS)

        gap = 25
        total_w = pdf_target_w * 2 + gap
        start_x = px_win + (pw_win - total_w) // 2
        start_y = py_win + 42

        draw.rounded_rectangle([start_x - 3, start_y - 3, start_x + pdf_target_w + 3, start_y + pdf_target_h + 3], radius=4, fill=(30, 41, 59))
        draw.rounded_rectangle([start_x + pdf_target_w + gap - 3, start_y - 3, start_x + total_w + 3, start_y + pdf_target_h + 3], radius=4, fill=(30, 41, 59))

        im.paste(p1_scaled, (start_x, start_y))
        im.paste(p2_scaled, (start_x + pdf_target_w + gap, start_y))

        lbl_p1 = "Pág. 1: Encuadre, FCF & WACC (CAPM)" if is_es else "Page 1: Scope, FCFF & WACC (CAPM)"
        lbl_p2 = "Pág. 2: Formulación Matemática & Métricas" if is_es else "Page 2: Mathematical Proofs & Metrics"
        draw.text((start_x + 6, start_y + pdf_target_h + 6), lbl_p1, font=f_page_lbl, fill=(148, 163, 184))
        draw.text((start_x + pdf_target_w + gap + 6, start_y + pdf_target_h + 6), lbl_p2, font=f_page_lbl, fill=(148, 163, 184))

    # =========================================================================
    # 4. BOTTOM-RIGHT WINDOW: CAPTURA REAL SLIDE PPTX (x=985, y=505, w=575, h=375)
    # =========================================================================
    sx, sy, sw, sh = 985, 505, 575, 375
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pptx_title_es = "Presentación Grado Consejo (.pptx 16:9 Widescreen) — Gráfico Tornado"
    pptx_title_en = "Boardroom Presentation (.pptx 16:9 Widescreen) — Tornado Chart"
    draw_window_header(draw, sx, sy, sw, 34, pptx_title_es if is_es else pptx_title_en, (194, 65, 12), f_win_title)

    fname_ppt = "Presentacion_Business_Case_CLevel_ES.pptx" if is_es else "Deck_Business_Case_CLevel_EN.pptx"
    pptx_path = os.path.join(BASE_DIR, "packages", "Suite_02_Toma_Decisiones", "03_Business_Case_VAN_TIR", folder, fname_ppt)
    ppt_slide = export_pptx_slide(pptx_path, slide_idx=2)

    # Fallback si COM no está disponible a los PNGs pre-exportados de scratch
    if not ppt_slide:
        scratch_fallback = os.path.join(r"C:\Users\dalae\.gemini\antigravity\brain\3efcc652-87a4-47bc-8430-182e85797896\scratch", f"{'es' if is_es else 'en'}_slide_2.png")
        if os.path.exists(scratch_fallback):
            ppt_slide = Image.open(scratch_fallback).copy()

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
        "Estándar McKinsey Corporate Finance & BCG Strategy • C-Level Audit Ready"
        if is_es else
        "McKinsey Corporate Finance & BCG Strategy Standards • C-Level Audit Ready"
    )
    draw.text((45, 935), sub_foot, font=f_footer_sub, fill=(71, 85, 105))

    center_text = (
        "Fórmulas 100% Auditables • Celdas Desbloqueadas • Compatibilidad MS Excel & Google Sheets"
        if is_es else
        "100% Auditable Formulas • Unlocked Input Cells • MS Excel & Google Sheets Compatibility"
    )
    draw.text((430, 925), center_text, font=f_footer, fill=(203, 213, 225))

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
    os.makedirs(os.path.join(BASE_DIR, "content", "es", "posts", "business-case-financiero-van-tir"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "en", "posts", "financial-business-case-npv-irr"), exist_ok=True)

    # 1. Vista previa en Español
    print("Generando vista previa en Español (ES)...")
    im_es = generate_preview_pack(lang="es")
    p_static_es = os.path.join(BASE_DIR, "static", "images", "recursos", "business-case-preview-es.png")
    p_post_es = os.path.join(BASE_DIR, "content", "es", "posts", "business-case-financiero-van-tir", "preview-pack.png")
    im_es.save(p_static_es, "PNG", optimize=True)
    im_es.save(p_post_es, "PNG", optimize=True)
    print(f"  [OK] Generado ES: {p_static_es} y {p_post_es} ({im_es.size})")

    # 2. Vista previa en Inglés
    print("Generando vista previa en Inglés (EN)...")
    im_en = generate_preview_pack(lang="en")
    p_static_en = os.path.join(BASE_DIR, "static", "images", "recursos", "business-case-preview-en.png")
    p_post_en = os.path.join(BASE_DIR, "content", "en", "posts", "financial-business-case-npv-irr", "preview-pack.png")
    im_en.save(p_static_en, "PNG", optimize=True)
    im_en.save(p_post_en, "PNG", optimize=True)
    print(f"  [OK] Generado EN: {p_static_en} y {p_post_en} ({im_en.size})")

    print("\nGeneración de vistas previas completada con éxito.")


if __name__ == "__main__":
    main()
