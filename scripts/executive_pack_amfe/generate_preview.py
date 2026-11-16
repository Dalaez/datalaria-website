#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Executive Decision Pack Matriz de Riesgos Cuantitativa & AMFE / FMEA (ES y EN):
- static/images/recursos/amfe-preview-es.png
- static/images/recursos/amfe-preview-en.png
- content/es/posts/matriz-riesgos-amfe-fmea/preview-pack.png
- content/en/posts/quantitative-risk-matrix-fmea/preview-pack.png

Cumple con el estándar visual de las Suites de Datalaria (Suite 01, Suite 02, Suite 03):
- Lienzo 1600 x 980 px Dark-Slate Tier-1 (#0B1120).
- Ventana izquierda: Excel .xlsx con Dashboard Ejecutivo (KPIs reales, Matriz 5x5, Top Modos de Fallo AIAG-VDA & Veredicto CER).
- Ventana superior derecha: Guía Metodológica en PDF real (Páginas 1 y 2 vía pypdfium2).
- Ventana inferior derecha: Presentación Ejecutiva PowerPoint .pptx real (Slide 2 vía PowerPoint COM).
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
    draw.ellipse([x + 14 - r, cy - r, x + 14 + r, cy + r], fill=(255, 95, 86))
    draw.ellipse([x + 30 - r, cy - r, x + 30 + r, cy + r], fill=(255, 189, 46))
    draw.ellipse([x + 46 - r, cy - r, x + 46 + r, cy + r], fill=(39, 201, 63))
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
    """Renderiza páginas 1 y 2 reales de la guía metodológica PDF con pypdfium2."""
    if not os.path.exists(pdf_path):
        print(f"[WARN] PDF no encontrado: {pdf_path}")
        return None, None
    doc = pypdfium2.PdfDocument(pdf_path)
    p1 = doc[0].render(scale=2.5).to_pil()
    p2 = doc[1].render(scale=2.5).to_pil()
    return p1, p2


def export_pptx_slide2(pptx_path):
    """Exporta la Diapositiva 2 real del PowerPoint vía PowerPoint COM."""
    if not os.path.exists(pptx_path):
        print(f"[WARN] PPTX no encontrado: {pptx_path}")
        return None
    import win32com.client
    temp_png = os.path.abspath(f"temp_amfe_slide2_{os.getpid()}.png")
    app = win32com.client.Dispatch("PowerPoint.Application")
    try:
        pres = app.Presentations.Open(os.path.abspath(pptx_path), WithWindow=False)
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
    im = Image.new("RGB", (W, H), (11, 17, 32))
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle([15, 15, W - 15, H - 15], radius=16, outline=(30, 41, 59), width=2)

    f_badge = get_font(12, bold=True)
    f_title = get_font(25, bold=True)
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
    badge_text = (
        "EXECUTIVE DECISION PACK • CONTROL OPERATIVO & RIESGOS"
        if is_es else
        "EXECUTIVE DECISION PACK • OPERATIONAL CONTROL & RISK"
    )
    b_box = f_badge.getbbox(badge_text)
    badge_w = (b_box[2] - b_box[0]) + 40
    draw.rounded_rectangle([40, 26, 40 + badge_w, 48], radius=6, fill=(15, 36, 58), outline=(13, 148, 136), width=1)
    draw_sparkle(draw, 55, 37, 6, (45, 212, 191))
    draw.text((68, 30), badge_text, font=f_badge, fill=(45, 212, 191))

    title_text = (
        "MATRIZ DE RIESGOS CUANTITATIVA & AMFE / FMEA"
        if is_es else
        "QUANTITATIVE RISK MATRIX & OPERATIONAL FMEA"
    )
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    sub_text = (
        "MATRIZ DE CALOR 5x5 ISO 31000, CÁLCULO DE NPR (S x O x D), PRIORIDAD DE ACCIÓN AIAG-VDA & ROI CER"
        if is_es else
        "ISO 31000 5x5 HEAT MAP, RPN SCORING (S x O x D), AIAG-VDA ACTION PRIORITY & CAPEX CER ROI"
    )
    draw.text((42, 85), sub_text, font=f_subtitle, fill=(148, 163, 184))

    pills = [
        ("Excel .xlsx + Sheets", (16, 124, 65), (16, 185, 129)),
        ("PowerPoint 16:9 C-Level", (194, 65, 12), (245, 158, 11)),
        ("Guía Metodológica PDF" if is_es else "PDF Methodology Guide", (30, 58, 138), (59, 130, 246)),
    ]
    px = W - 40
    for label, bg, border in reversed(pills):
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

    title_win = (
        "Excel .xlsx — Motor Cuantitativo ISO 31000 & AMFE / FMEA [ECMA-376]"
        if is_es else
        "Excel .xlsx — Quantitative ISO 31000 & FMEA Engine [ECMA-376]"
    )
    draw_window_header(draw, wx, wy, ww, 34, title_win, (16, 124, 65), f_win_title)

    # Formula Bar
    draw.rectangle([wx, wy + 34, wx + ww, wy + 62], fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    fx_text = (
        'fx: =SI(O(L6>=120; I6>=9); "Alta"; SI(L6>=60; "Media"; "Baja"))   |   NPR = Severidad(I6) * Ocurrencia(J6) * Deteccion(K6)'
        if is_es else
        'fx: =IF(OR(L6>=120, I6>=9), "High", IF(L6>=60, "Medium", "Low"))   |   RPN = Severity(I6) * Occurrence(J6) * Detection(K6)'
    )
    draw.text((wx + 15, wy + 41), fx_text, font=f_formula, fill=(71, 85, 105))

    # Inner Banner Directivo
    bx, by, bw, bh = wx + 12, wy + 68, ww - 24, 28
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=4, fill=(15, 23, 42))
    b_text = (
        "DASHBOARD EJECUTIVO C-LEVEL: RIESGOS ISO 31000, AMFE AIAG-VDA & RETORNO DE MITIGACIÓN"
        if is_es else
        "C-LEVEL EXECUTIVE DASHBOARD: ISO 31000 RISKS, AIAG-VDA FMEA & MITIGATION ROI"
    )
    bbox_b = f_th.getbbox(b_text)
    draw.text((bx + (bw - (bbox_b[2] - bbox_b[0])) // 2, by + 7), b_text, font=f_th, fill=(255, 255, 255))

    # Metadata Row
    my = by + bh + 4
    draw.rectangle([bx, my, bx + bw, my + 20], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    m_info = (
        "Alcance: 20 Riesgos Corporativos + 15 Modos de Fallo FMEA   •   CAPEX Mitigación: 360.000 €   •   Estándar: ISO 31000 / AIAG-VDA"
        if is_es else
        "Scope: 20 Enterprise Risks + 15 FMEA Failure Modes   •   Mitigation CAPEX: $360,000   •   Standard: ISO 31000 / AIAG-VDA"
    )
    draw.text((bx + 12, my + 4), m_info, font=f_kpi_sub, fill=(71, 85, 105))

    # 5 KPI Cards (cifras reales del workbook Excel)
    ky = my + 26
    kw = (bw - 20) // 5
    kh = 52
    kpis = [
        ("EVENTOS EVALUADOS", "35", "20 ISO 31000 + 15 FMEA", (37, 99, 235)),
        ("NPR MÁXIMO INHERENTE", "441", "FMEA-03 (S=9, O=7, D=7)", (220, 38, 38)),
        ("REDUCCIÓN MEDIA NPR", "-89,0%", "Post-mitigación residual", (16, 185, 129)),
        ("PÉRDIDA EVITADA ΔE(L)", "1.843 k€", "De 2.130 k€ a 287 k€", (13, 148, 136)),
        ("RATIO ROI CONTROL CER", "5,1x", "Retorno sobre 360 k€", (217, 119, 6)),
    ] if is_es else [
        ("EVENTS EVALUATED", "35", "20 ISO 31000 + 15 FMEA", (37, 99, 235)),
        ("MAX INHERENT RPN", "441", "FMEA-03 (S=9, O=7, D=7)", (220, 38, 38)),
        ("AVG RPN REDUCTION", "-89.0%", "Post-mitigation residual", (16, 185, 129)),
        ("LOSS AVOIDED ΔE(L)", "$1,843k", "Down from $2,130k to $287k", (13, 148, 136)),
        ("CONTROL ROI (CER)", "5.1x", "Return on $360k CAPEX", (217, 119, 6)),
    ]
    for i, (k_lbl, k_val, k_sub, k_col) in enumerate(kpis):
        kx = bx + i * (kw + 5)
        draw.rounded_rectangle([kx, ky, kx + kw, ky + kh], radius=5, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([kx, ky, kx + kw, ky + 16], radius=4, fill=(30, 41, 59))
        draw.rectangle([kx, ky + 10, kx + kw, ky + 16], fill=(30, 41, 59))
        draw.text((kx + 6, ky + 2), k_lbl, font=f_kpi_lbl, fill=(255, 255, 255))
        draw.text((kx + 8, ky + 18), k_val, font=f_kpi_val, fill=k_col)
        draw.text((kx + 8, ky + 36), k_sub, font=f_kpi_sub, fill=(100, 116, 139))

    # Mini Sección Intermedia: Matriz 5x5 + Pareto FMEA Summary Strip (y = ky+kh+8 .. +92)
    my2 = ky + kh + 8
    draw.rounded_rectangle([bx, my2, bx + bw, my2 + 22], radius=4, fill=(240, 253, 250), outline=(153, 246, 228), width=1)
    s_title = (
        "TOP MODOS DE FALLO CRÍTICOS (AMFE AIAG-VDA) & REEVALUACIÓN POST-MITIGACIÓN"
        if is_es else
        "TOP CRITICAL FAILURE MODES (AIAG-VDA FMEA) & POST-MITIGATION RE-SCORING"
    )
    draw.text((bx + 10, my2 + 4), s_title, font=f_th, fill=(13, 148, 136))

    # Table Header
    ty = my2 + 26
    draw.rectangle([bx, ty, bx + bw, ty + 24], fill=(30, 41, 59))
    headers = [
        ("ID", 64),
        ("Proceso / Sistema", 150),
        ("Modo Potencial de Fallo", 252),
        ("S·O·D", 56),
        ("NPR", 50),
        ("Prioridad AP", 96),
        ("NPR Res.", 64),
        ("% Reduc.", 66),
        ("CER ROI", 103),
    ] if is_es else [
        ("ID", 64),
        ("Process / System", 150),
        ("Potential Failure Mode", 252),
        ("S·O·D", 56),
        ("RPN", 50),
        ("Action AP", 96),
        ("Res. RPN", 64),
        ("% Reduc.", 66),
        ("CER ROI", 103),
    ]
    hx = bx
    for h_txt, h_w in headers:
        draw.text((hx + 6, ty + 5), h_txt, font=f_th, fill=(255, 255, 255))
        hx += h_w

    rows = [
        ("FMEA-03", "Control Accesos", "Autenticación indebida terceros", "9·7·7", "441", "ALTA (Crit.)", "36", "-91,8%", "5,4x · Zero Trust", (220, 38, 38)),
        ("FMEA-02", "Almacenam. Cloud", "Corrupción datos transaccionales", "9·5·8", "360", "ALTA (Crit.)", "36", "-90,0%", "5,8x · WORM CI/CD", (220, 38, 38)),
        ("FMEA-07", "Línea Ensamblaje", "Desalineación cabezal robótico", "9·5·8", "360", "ALTA (Crit.)", "36", "-90,0%", "4,3x · IoT Visión", (220, 38, 38)),
        ("FMEA-01", "Pasarela Pagos", "Timeout comunicación adquirente", "8·6·7", "336", "ALTA (Crit.)", "48", "-85,7%", "5,9x · Smart Route", (220, 38, 38)),
        ("FMEA-12", "Motor Búsqueda", "Desincronización índices catálogo", "7·6·8", "336", "ALTA (Crit.)", "42", "-87,5%", "Control Operativo", (217, 119, 6)),
        ("FMEA-06", "Cola Mensajería", "Acumulación lag eventos críticos", "7·6·7", "294", "ALTA (Crit.)", "42", "-85,7%", "Auto-scaling Pods", (217, 119, 6)),
        ("FMEA-04", "Balanceador Carga", "Saturación RAM pico de tráfico", "8·6·6", "288", "ALTA (Crit.)", "48", "-83,3%", "4,2x · Multi-Región", (217, 119, 6)),
        ("FMEA-15", "Data Center Cool.", "Fuga refrigerante rack densidad", "9·4·8", "288", "ALTA (Crit.)", "18", "-93,8%", "5,7x · Sensor Rack", (16, 185, 129)),
    ] if is_es else [
        ("FMEA-03", "Access Control", "Unauthorized threat actor login", "9·7·7", "441", "HIGH AP", "36", "-91.8%", "5.4x · Zero Trust", (220, 38, 38)),
        ("FMEA-02", "Cloud Storage", "Database corruption or data loss", "9·5·8", "360", "HIGH AP", "36", "-90.0%", "5.8x · WORM CI/CD", (220, 38, 38)),
        ("FMEA-07", "Assembly Line", "Robotic weld head misalignment", "9·5·8", "360", "HIGH AP", "36", "-90.0%", "4.3x · IoT Vision", (220, 38, 38)),
        ("FMEA-01", "Payment Gateway", "Acquirer API socket timeout", "8·6·7", "336", "HIGH AP", "48", "-85.7%", "5.9x · Smart Route", (220, 38, 38)),
        ("FMEA-12", "Search Engine", "Catalog search index drift", "7·6·8", "336", "HIGH AP", "42", "-87.5%", "Hourly Reconcil.", (217, 119, 6)),
        ("FMEA-06", "Message Broker", "Uncontrolled consumer lag", "7·6·7", "294", "HIGH AP", "42", "-85.7%", "Pod Autoscaling", (217, 119, 6)),
        ("FMEA-04", "Load Balancer", "Memory exhaustion spike (503)", "8·6·6", "288", "HIGH AP", "48", "-83.3%", "4.2x · Multi-Region", (217, 119, 6)),
        ("FMEA-15", "Server Cooling", "Coolant leak in dense rack", "9·4·8", "288", "HIGH AP", "18", "-93.8%", "5.7x · Per-Rack", (16, 185, 129)),
    ]

    row_h = 24
    for r_i, r_data in enumerate(rows):
        ry = ty + 24 + r_i * row_h
        bg_col = (254, 242, 242) if r_data[9] == (220, 38, 38) else ((255, 251, 235) if r_data[9] == (217, 119, 6) else (240, 253, 244))
        draw.rectangle([bx, ry, bx + bw, ry + row_h], fill=bg_col, outline=(241, 245, 249), width=1)
        rx = bx
        for col_idx, (val, (_, h_w)) in enumerate(zip(r_data[:9], headers)):
            f_use = f_td_b if col_idx in [0, 4, 5, 7] else f_td
            c_fill = (15, 23, 42)
            if col_idx in [4, 5]:
                c_fill = r_data[9]
            elif col_idx == 7:
                c_fill = (6, 95, 70)
            draw.text((rx + 6, ry + 5), str(val), font=f_use, fill=c_fill)
            rx += h_w

    # Bottom Box inside Excel: Matriz 5x5 Mini-Resumen + Dictamen CAPEX
    dy = ty + 24 + len(rows) * row_h + 10
    box_h = (wy + wh - 36) - dy
    draw.rounded_rectangle([bx, dy, bx + bw, dy + box_h], radius=5, fill=(248, 250, 252), outline=(203, 213, 225), width=1)

    # Mini 5x5 Matrix on left of bottom box
    mgx0, mgy0 = bx + 14, dy + 10
    lbl_m = "MATRIZ 5x5 ISO 31000" if is_es else "ISO 31000 5x5 HEAT MAP"
    draw.text((mgx0, mgy0), lbl_m, font=f_th, fill=(15, 23, 42))
    cs = 24
    cg = 3
    m_colors = [
        [(254, 243, 199), (254, 243, 199), (254, 226, 226), (254, 226, 226), (254, 226, 226)],
        [(209, 250, 229), (254, 243, 199), (254, 243, 199), (254, 226, 226), (254, 226, 226)],
        [(209, 250, 229), (209, 250, 229), (254, 243, 199), (254, 243, 199), (254, 226, 226)],
        [(209, 250, 229), (209, 250, 229), (209, 250, 229), (254, 243, 199), (254, 243, 199)],
        [(209, 250, 229), (209, 250, 229), (209, 250, 229), (209, 250, 229), (254, 243, 199)],
    ]
    m_counts = {(0, 3): "1", (0, 2): "2", (0, 1): "1", (1, 3): "4", (1, 2): "2", (1, 1): "1", (2, 3): "3", (2, 2): "3", (2, 1): "1"}
    for r in range(5):
        for c in range(5):
            cx = mgx0 + c * (cs + cg)
            cy = mgy0 + 20 + r * (cs + cg)
            draw.rounded_rectangle([cx, cy, cx + cs, cy + cs], radius=3, fill=m_colors[r][c], outline=(203, 213, 225), width=1)
            cnt = m_counts.get((r, c), "")
            if cnt:
                draw.text((cx + 8, cy + 4), cnt, font=f_td_b, fill=(15, 23, 42))

    # Verdict text on right of bottom box
    vx = mgx0 + 5 * (cs + cg) + 28
    d_title = (
        "DICTAMEN DE INVERSIÓN & COMITÉ DE AUDITORÍA (BOARD DECISION GATEWAY)"
        if is_es else
        "AUDIT COMMITTEE VERDICT & CAPEX MITIGATION APPROVAL (BOARD GATEWAY)"
    )
    draw.text((vx, dy + 12), d_title, font=f_th, fill=(15, 23, 42))
    d_body = (
        "• Zona Crítica ISO 31000: 5 riesgos en cuadrante rojo (Score >= 15) mitigados hacia zona verde (<= 6) en Q1-Q3.\n"
        "• Prioridad de Acción AIAG-VDA: 100% de modos de fallo críticos (NPR >= 120 o S >= 9) reducidos por debajo de NPR 50.\n"
        "• Eficiencia de Capital (CER): 360.000 € de inversión CAPEX/OPEX neutralizan 1.843.000 € en pérdida esperada anual (ROI 5,1x).\n"
        "• Celdas de entrada editables en blanco (#FFFFFF) y fórmulas protegidas ECMA-376 bajo contraseña en instrucciones."
        if is_es else
        "• ISO 31000 Critical Zone: 5 red-quadrant corporate risks (Score >= 15) mitigated down to green tolerance (<= 6) across Q1-Q3.\n"
        "• AIAG-VDA Action Priority: 100% of High-AP failure modes (RPN >= 120 or S >= 9) engineered below residual RPN 50.\n"
        "• Capital Efficiency (CER): $360,000 CAPEX/OPEX deployment eliminates $1,843,000 in expected annualized losses (5.1x ROI).\n"
        "• Unlocked white input cells (#FFFFFF) and ECMA-376 OpenXML formula protection under password provided in instructions."
    )
    draw.text((vx, dy + 34), d_body, font=f_td, fill=(51, 65, 85), spacing=6)

    # Excel Sheet Tabs
    tab_y = wy + wh - 30
    draw.rectangle([wx, tab_y, wx + ww, wy + wh], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    tabs = [
        ("Dashboard Ejecutivo" if is_es else "Executive Dashboard", True),
        ("Matriz de Riesgos 5x5" if is_es else "5x5 Risk Matrix", False),
        ("AMFE Operativo" if is_es else "Operational FMEA", False),
        ("Plan Mitigacion & CAPEX" if is_es else "Mitigation Plan & CAPEX", False),
    ]
    tbx = wx + 15
    for tab_name, is_active in tabs:
        bbox = f_tab.getbbox(tab_name)
        tbw = bbox[2] - bbox[0] + 18
        if is_active:
            draw.rounded_rectangle([tbx, tab_y - 2, tbx + tbw, wy + wh], radius=4, fill=(16, 124, 65))
            draw.text((tbx + 9, tab_y + 4), tab_name, font=f_tab, fill=(255, 255, 255))
        else:
            draw.text((tbx + 9, tab_y + 4), tab_name, font=f_tab, fill=(100, 116, 139))
        tbx += tbw + 8

    # =========================================================================
    # 3. TOP-RIGHT WINDOW: CAPTURAS REALES GUÍA PDF (x=985, y=115, w=575, h=370)
    # =========================================================================
    px, py, pw, ph = 985, 115, 575, 370
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pdf_title = (
        "Guía Metodológica Oficial (.pdf) — 5 Páginas C-Level"
        if is_es else
        "Official Methodology Guide (.pdf) — 5 C-Level Pages"
    )
    draw_window_header(draw, px, py, pw, 34, pdf_title, (30, 58, 138), f_win_title)

    folder = "[ES]_Matriz_Riesgos_AMFE" if is_es else "[EN]_FMEA_Risk_Matrix"
    fname_pdf = "Guia_Metodologica_AMFE_Riesgos_ES.pdf" if is_es else "Methodology_Guide_FMEA_Risk_EN.pdf"
    pdf_path = os.path.join(BASE_DIR, "packages", "Suite_03_Control_Operativo", "02_Matriz_Riesgos_AMFE", folder, fname_pdf)

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

        draw.rounded_rectangle([start_x - 3, start_y - 3, start_x + pdf_target_w + 3, start_y + pdf_target_h + 3], radius=4, fill=(30, 41, 59))
        draw.rounded_rectangle([start_x + pdf_target_w + gap - 3, start_y - 3, start_x + total_w + 3, start_y + pdf_target_h + 3], radius=4, fill=(30, 41, 59))

        im.paste(p1_scaled, (start_x, start_y))
        im.paste(p2_scaled, (start_x + pdf_target_w + gap, start_y))

        lbl_p1 = "Pág. 1: Diagnóstico Cualitativo" if is_es else "Page 1: Qualitative Fallacy"
        lbl_p2 = "Pág. 2: E(L), NPR & ROI CER" if is_es else "Page 2: E(L), RPN & CER Math"
        draw.text((start_x + 6, start_y + pdf_target_h + 6), lbl_p1, font=f_page_lbl, fill=(148, 163, 184))
        draw.text((start_x + pdf_target_w + gap + 6, start_y + pdf_target_h + 6), lbl_p2, font=f_page_lbl, fill=(148, 163, 184))

    # =========================================================================
    # 4. BOTTOM-RIGHT WINDOW: CAPTURA REAL SLIDE 2 PPTX (x=985, y=505, w=575, h=375)
    # =========================================================================
    sx, sy, sw, sh = 985, 505, 575, 375
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    pptx_title = (
        "Presentación Grado Consejo (.pptx 16:9 Widescreen)"
        if is_es else
        "Boardroom Presentation (.pptx 16:9 Widescreen)"
    )
    draw_window_header(draw, sx, sy, sw, 34, pptx_title, (194, 65, 12), f_win_title)

    fname_ppt = "Presentacion_AMFE_Riesgos_CLevel_ES.pptx" if is_es else "Deck_FMEA_Risk_CLevel_EN.pptx"
    pptx_path = os.path.join(BASE_DIR, "packages", "Suite_03_Control_Operativo", "02_Matriz_Riesgos_AMFE", folder, fname_ppt)
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
        "Estándar ISO 31000:2018 & AIAG-VDA 2019 • C-Level Audit Ready"
        if is_es else
        "ISO 31000:2018 & AIAG-VDA 2019 Standards • C-Level Audit Ready"
    )
    draw.text((45, 935), sub_foot, font=f_footer_sub, fill=(71, 85, 105))

    center_text = (
        "Fórmulas 100% Auditables • Celdas Editables • Compatibilidad MS Excel & Google Sheets"
        if is_es else
        "100% Auditable Formulas • Unlocked Input Cells • MS Excel & Google Sheets Compatibility"
    )
    draw.text((430, 925), center_text, font=f_footer, fill=(203, 213, 225))

    btn_w = 225
    btn_x = W - 40 - btn_w
    btn_y = 915
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + 32], radius=6, fill=(15, 36, 58), outline=(45, 212, 191), width=1)
    draw_download_icon(draw, btn_x + 18, btn_y + 15, 5, (45, 212, 191))
    dl_badge = "Descarga Inmediata (.ZIP)" if is_es else "Instant Download (.ZIP)"
    draw.text((btn_x + 30, btn_y + 8), dl_badge, font=f_footer_b, fill=(45, 212, 191))

    return im


def main():
    os.makedirs(os.path.join(BASE_DIR, "static", "images", "recursos"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "es", "posts", "matriz-riesgos-amfe-fmea"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "content", "en", "posts", "quantitative-risk-matrix-fmea"), exist_ok=True)

    print("Generando vista previa AMFE en Español (ES)...")
    im_es = generate_preview_pack(lang="es")
    p_static_es = os.path.join(BASE_DIR, "static", "images", "recursos", "amfe-preview-es.png")
    p_post_es = os.path.join(BASE_DIR, "content", "es", "posts", "matriz-riesgos-amfe-fmea", "preview-pack.png")
    im_es.save(p_static_es, "PNG", optimize=True)
    im_es.save(p_post_es, "PNG", optimize=True)
    print(f"  [OK] Generado ES: {p_static_es} y {p_post_es} ({im_es.size})")

    print("Generando vista previa AMFE en Inglés (EN)...")
    im_en = generate_preview_pack(lang="en")
    p_static_en = os.path.join(BASE_DIR, "static", "images", "recursos", "amfe-preview-en.png")
    p_post_en = os.path.join(BASE_DIR, "content", "en", "posts", "quantitative-risk-matrix-fmea", "preview-pack.png")
    im_en.save(p_static_en, "PNG", optimize=True)
    im_en.save(p_post_en, "PNG", optimize=True)
    print(f"  [OK] Generado EN: {p_static_en} y {p_post_en} ({im_en.size})")


if __name__ == "__main__":
    main()
