#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Executive Decision Pack de la Matriz BCG Dinámica en español e inglés:
- static/images/recursos/bcg-preview-es.png
- static/images/recursos/bcg-preview-en.png
- content/es/posts/matriz-bcg-dinamica/preview-pack.png
- content/en/posts/dynamic-bcg-matrix/preview-pack.png

Cumple con el estándar visual exacto de DAFO, 5 Fuerzas de Porter y PESTEL:
- Lienzo 1600 x 980 px
- Header con badge, título y chips de entregables
- Ventana izquierda: Excel .xlsx con Dashboard y Gráfico de Burbujas dinámico
- Ventana superior derecha: Guía Metodológica en PDF (5 páginas C-Level)
- Ventana inferior derecha: Presentación Ejecutiva en PowerPoint .pptx 16:9
- Footer con marcas de auditoría, compatibilidad y descarga inmediata (.ZIP)
"""

import os
from PIL import Image, ImageDraw, ImageFont

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

def generate_preview_pack(lang="es"):
    is_es = (lang == "es")
    W, H = 1600, 980
    im = Image.new("RGB", (W, H), (11, 17, 32))  # Deep Slate Navy #0B1120
    draw = ImageDraw.Draw(im)

    # Subtle grid lines / border
    draw.rounded_rectangle([15, 15, W - 15, H - 15], radius=16, outline=(30, 41, 59), width=2)

    # Fonts
    f_badge = get_font(12, bold=True)
    f_title = get_font(26, bold=True)
    f_subtitle = get_font(13, bold=False)
    f_pill = get_font(12, bold=True)
    f_win_title = get_font(13, bold=True)
    f_kpi_label = get_font(10, bold=True)
    f_kpi_val = get_font(18, bold=True)
    f_kpi_sub = get_font(9, bold=False)
    f_body = get_font(11, bold=False)
    f_body_b = get_font(11, bold=True)
    f_chart_label = get_font(11, bold=True)
    f_chart_sub = get_font(9, bold=False)
    f_table = get_font(10, bold=False)
    f_table_b = get_font(10, bold=True)
    f_footer = get_font(11, bold=False)
    f_footer_b = get_font(11, bold=True)

    # =========================================================================
    # 1. HEADER (y = 25 .. 105)
    # =========================================================================
    # Badge
    badge_text = "★ EXECUTIVE DECISION PACK • ESTRATEGIA MBA" if is_es else "★ EXECUTIVE DECISION PACK • MBA STRATEGY"
    draw.rounded_rectangle([40, 26, 340, 48], radius=6, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw.text((48, 30), badge_text, font=f_badge, fill=(56, 189, 248))

    # Main Title
    title_text = "MATRIZ BCG DINÁMICA DE CARTERA" if is_es else "DYNAMIC BCG PORTFOLIO MATRIX"
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    # Subtitle
    sub_text = "ASIGNACIÓN OBJETIVA DE CAPITAL, BALANCE DE FCF & GRÁFICO DE BURBUJAS INTERACTIVO" if is_es else "OBJECTIVE CAPITAL ALLOCATION, FCF BALANCE & INTERACTIVE BUBBLE CHART"
    draw.text((42, 85), sub_text, font=f_subtitle, fill=(148, 163, 184))

    # Deliverables Pills on Right
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
    # 2. LEFT PANEL: EXCEL MOCKUP (x=40, y=115, w=925, h=765)
    # =========================================================================
    wx, wy, ww, wh = 40, 115, 925, 765
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(255, 255, 255), outline=(51, 65, 85), width=2)
    
    # Titlebar (Excel Green #107C41)
    title_win_es = "Excel .xlsx — Motor Cuantitativo & Dashboard Ejecutivo BCG"
    title_win_en = "Excel .xlsx — Quantitative Engine & BCG Executive Dashboard"
    draw_window_header(draw, wx, wy, ww, 34, title_win_es if is_es else title_win_en, (16, 124, 65), f_win_title)

    # Formula / Toolbar Bar
    draw.rectangle([wx, wy + 34, wx + ww, wy + 62], fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    draw.text((wx + 15, wy + 41), "fx: =SI(Y(CMR>=1; TCM>=10%); \"Estrella\"; SI(Y(CMR>=1; TCM<10%); \"Vaca\"; \"Interrogante\"))" if is_es else "fx: =IF(AND(RMS>=1, MGR>=10%), \"Star\", IF(AND(RMS>=1, MGR<10%), \"Cash Cow\", \"Question Mark\"))", font=f_table, fill=(71, 85, 105))

    # Top KPI Row (4 Cards)
    kpis = [
        ("INGRESOS CARTERA" if is_es else "PORTFOLIO SALES", "52.40 M€", "+8.5% YoY", (16, 185, 129)),
        ("SUPERÁVIT VACAS" if is_es else "COWS CASH SURPLUS", "+4.85 M€", "Reinversión: 65%" if is_es else "Reinvest: 65%", (217, 119, 6)),
        ("DÉFICIT ESTRELLAS" if is_es else "STARS CAPEX NEED", "-3.10 M€", "Financiado" if is_es else "Funded 100%", (37, 99, 235)),
        ("SALDO NETO FCF" if is_es else "NET LIQUIDITY", "+1.75 M€", "🟢 Sostenible" if is_es else "🟢 Sustainable", (5, 150, 105)),
    ]
    kw = (ww - 50) // 4
    for i, (k_label, k_val, k_sub, k_col) in enumerate(kpis):
        kx = wx + 15 + i * (kw + 7)
        ky = wy + 72
        draw.rounded_rectangle([kx, ky, kx + kw, ky + 58], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((kx + 10, ky + 8), k_label, font=f_kpi_label, fill=(100, 116, 139))
        draw.text((kx + 10, ky + 22), k_val, font=f_kpi_val, fill=k_col)
        draw.text((kx + 10, ky + 43), k_sub, font=f_kpi_sub, fill=(100, 116, 139))

    # Main Split inside Excel:
    # Left: Bubble Chart (w=535), Right: Table (w=345)
    cx, cy, cw, ch = wx + 15, wy + 140, 535, 580
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    # Chart Header
    draw.rectangle([cx, cy, cx + cw, cy + 30], fill=(248, 250, 252))
    draw.text((cx + 12, cy + 8), "MATRIZ BCG: CUOTA RELATIVA (CMR) vs. CRECIMIENTO MERCADO (TCM)" if is_es else "BCG MATRIX: RELATIVE MARKET SHARE (RMS) vs. MARKET GROWTH (MGR)", font=f_chart_label, fill=(15, 23, 42))

    # Quadrant Backgrounds inside Chart
    # Crosshair coordinates:
    qx = cx + 265  # CMR = 1.0 boundary
    qy = cy + 30 + (ch - 60) // 2  # TCM = 10% boundary
    
    # Top-Left: Interrogantes / Question Marks (CMR < 1, TCM >= 10)
    draw.rectangle([cx + 40, cy + 32, qx, qy], fill=(239, 246, 255))
    draw.text((cx + 50, cy + 40), "❓ INTERROGANTES (Question Marks)" if is_es else "❓ QUESTION MARKS", font=f_chart_label, fill=(37, 99, 235))
    draw.text((cx + 50, cy + 56), "Apostar o Desinvertir • FCF Negativo" if is_es else "Selective Investment • Negative FCF", font=f_chart_sub, fill=(59, 130, 246))

    # Top-Right: Estrellas / Stars (CMR >= 1, TCM >= 10)
    draw.rectangle([qx, cy + 32, cx + cw - 10, qy], fill=(240, 253, 250))
    draw.text((qx + 15, cy + 40), "⭐ ESTRELLAS (Stars)" if is_es else "⭐ STARS", font=f_chart_label, fill=(13, 148, 136))
    draw.text((qx + 15, cy + 56), "Mantener Liderazgo • FCF Neutro" if is_es else "Maintain Leadership • Neutral FCF", font=f_chart_sub, fill=(20, 184, 166))

    # Bottom-Left: Perros / Dogs (CMR < 1, TCM < 10)
    draw.rectangle([cx + 40, qy, qx, cy + ch - 30], fill=(255, 241, 242))
    draw.text((cx + 50, qy + 12), "🐕 PERROS (Dogs)" if is_es else "🐕 DOGS", font=f_chart_label, fill=(225, 29, 72))
    draw.text((cx + 50, qy + 28), "Desinvertir / Reestructurar" if is_es else "Divest or Restructure • Low ROIC", font=f_chart_sub, fill=(244, 63, 94))

    # Bottom-Right: Vacas Lecheras / Cash Cows (CMR >= 1, TCM < 10)
    draw.rectangle([qx, qy, cx + cw - 10, cy + ch - 30], fill=(255, 251, 235))
    draw.text((qx + 15, qy + 12), "🐄 VACAS LECHERAS (Cash Cows)" if is_es else "🐄 CASH COWS", font=f_chart_label, fill=(217, 119, 6))
    draw.text((qx + 15, qy + 28), "Ordeñar Liquidez • FCF Positivo Alto" if is_es else "Harvest Cash Flow • High Positive FCF", font=f_chart_sub, fill=(245, 158, 11))

    # Crosshair Lines
    for y_dash in range(cy + 32, cy + ch - 30, 8):
        draw.line([qx, y_dash, qx, y_dash + 4], fill=(148, 163, 184), width=2)
    for x_dash in range(cx + 40, cx + cw - 10, 8):
        draw.line([x_dash, qy, x_dash + 4, qy], fill=(148, 163, 184), width=2)

    # Bubbles (with glow and revenue-proportional radii)
    bubbles = [
        # (name, x_pos, y_pos, radius, fill_color, border_color, rev_text)
        ("Cloud Enterprise", qx + 130, cy + 150, 48, (13, 148, 136), (15, 118, 110), "16.5 M€ (31%)"),
        ("Legacy ERP Suite", qx + 150, qy + 140, 56, (217, 119, 6), (180, 83, 9), "22.0 M€ (42%)"),
        ("AI Analytics Suite", cx + 150, cy + 130, 32, (37, 99, 235), (29, 78, 216), "5.5 M€ (11%)"),
        ("Hardware POS", cx + 160, qy + 160, 38, (225, 29, 72), (190, 18, 60), "8.4 M€ (16%)"),
    ]
    for b_name, bx, by, br, b_fill, b_border, b_rev in bubbles:
        # Subtle shadow
        draw.ellipse([bx - br + 3, by - br + 3, bx + br + 3, by + br + 3], fill=(203, 213, 225))
        # Bubble body
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=b_fill, outline=b_border, width=2)
        # Inner gloss
        draw.ellipse([bx - br + 8, by - br + 6, bx + br - 8, by - br + 20], fill=(255, 255, 255, 80))
        # Label
        bbox = f_chart_label.getbbox(b_name)
        bw = bbox[2] - bbox[0]
        draw.text((bx - bw // 2, by - 10), b_name, font=f_chart_label, fill=(255, 255, 255))
        bbox_r = f_chart_sub.getbbox(b_rev)
        brw = bbox_r[2] - bbox_r[0]
        draw.text((bx - brw // 2, by + 5), b_rev, font=f_chart_sub, fill=(255, 255, 255))

    # Axis notations
    draw.text((cx + 42, cy + ch - 22), "← 0.1x (Baja Cuota)     Eje X: Cuota de Mercado Relativa (CMR)     10x (Líder) →" if is_es else "← 0.1x (Low Share)     X-Axis: Relative Market Share (RMS)     10x (Leader) →", font=f_table, fill=(100, 116, 139))

    # Right: Data Table inside Excel (x=565, y=wy+140, w=345, h=580)
    tx, ty, tw, th = wx + 560, wy + 140, 350, 580
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    # Table Header
    draw.rectangle([tx, ty, tx + tw, ty + 30], fill=(15, 23, 42))
    draw.text((tx + 10, ty + 8), "EVALUACIÓN DE CARTERA (12 UENs)" if is_es else "PORTFOLIO ASSESSMENT (12 SBUs)", font=f_table_b, fill=(255, 255, 255))

    # Table Columns Header
    draw.rectangle([tx, ty + 30, tx + tw, ty + 56], fill=(241, 245, 249))
    draw.text((tx + 8, ty + 38), "UEN / División" if is_es else "SBU / Division", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 120, ty + 38), "Ventas" if is_es else "Sales", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 180, ty + 38), "CMR", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 225, ty + 38), "TCM", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 270, ty + 38), "Cuadrante" if is_es else "Quadrant", font=f_table_b, fill=(71, 85, 105))

    # Rows
    rows = [
        ("Cloud Enterprise", "16.5 M€", "1.8x", "18.0%", "⭐ Estrella" if is_es else "⭐ Star", (20, 184, 166)),
        ("Legacy ERP Suite", "22.0 M€", "2.4x", "4.0%", "🐄 Vaca" if is_es else "🐄 Cow", (245, 158, 11)),
        ("AI Analytics Suite", "5.5 M€", "0.4x", "22.5%", "❓ Interrog." if is_es else "❓ Question", (59, 130, 246)),
        ("Hardware POS", "8.4 M€", "0.3x", "2.0%", "🐕 Perro" if is_es else "🐕 Dog", (244, 63, 94)),
        ("Cybersecurity Ops", "4.2 M€", "1.2x", "14.5%", "⭐ Estrella" if is_es else "⭐ Star", (20, 184, 166)),
        ("Telecom Legacy", "6.8 M€", "1.9x", "3.2%", "🐄 Vaca" if is_es else "🐄 Cow", (245, 158, 11)),
        ("IoT Platforms", "2.8 M€", "0.5x", "19.0%", "❓ Interrog." if is_es else "❓ Question", (59, 130, 246)),
        ("Retail Software", "3.1 M€", "0.4x", "1.5%", "🐕 Perro" if is_es else "🐕 Dog", (244, 63, 94)),
    ]
    for r_i, (r_name, r_rev, r_cmr, r_tcm, r_quad, r_col) in enumerate(rows):
        ry = ty + 56 + r_i * 32
        row_bg = (248, 250, 252) if (r_i % 2 == 0) else (255, 255, 255)
        draw.rectangle([tx, ry, tx + tw, ry + 32], fill=row_bg)
        draw.text((tx + 8, ry + 8), r_name, font=f_table, fill=(30, 41, 59))
        draw.text((tx + 120, ry + 8), r_rev, font=f_table_b, fill=(15, 23, 42))
        draw.text((tx + 180, ry + 8), r_cmr, font=f_table, fill=(100, 116, 139))
        draw.text((tx + 225, ry + 8), r_tcm, font=f_table, fill=(100, 116, 139))
        draw.rounded_rectangle([tx + 265, ry + 4, tx + tw - 8, ry + 26], radius=4, fill=r_col)
        draw.text((tx + 272, ry + 7), r_quad, font=f_table_b, fill=(255, 255, 255))

    # Net Fund Flow Highlight Box in Table
    ff_y = ty + 320
    draw.rounded_rectangle([tx + 10, ff_y, tx + tw - 10, ff_y + 115], radius=6, fill=(240, 253, 250), outline=(20, 184, 166), width=1)
    draw.text((tx + 18, ff_y + 8), "BALANCE DE FONDOS (Bruce Henderson)" if is_es else "FUND FLOW BALANCE (Bruce Henderson)", font=f_table_b, fill=(13, 148, 136))
    draw.text((tx + 18, ff_y + 26), "• Generación FCF Vacas: +4.85 M€\n• Requerimiento CAPEX Estrellas: -3.10 M€\n• Superávit Neto Liquidez: +1.75 M€ (Autofinanciado)" if is_es else "• Cows FCF Harvested: +4.85 M€\n• Stars CAPEX Demands: -3.10 M€\n• Net Free Cash Flow: +1.75 M€ (Self-Funded)", font=f_table, fill=(15, 118, 110))

    # Henderson Equation
    draw.rounded_rectangle([tx + 10, ff_y + 125, tx + tw - 10, ty + th - 15], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((tx + 18, ff_y + 133), "REGLA DE ORO DE ASIGNACIÓN:" if is_es else "GOLDEN ALLOCATION RULE:", font=f_kpi_label, fill=(100, 116, 139))
    draw.text((tx + 18, ff_y + 150), "ΔFCF = Σ FCF(Vacas) - Σ CAPEX(Estrellas/Incógnitas)\nEl superávit financia la innovación sin deuda externa." if is_es else "ΔFCF = Σ FCF(Cows) - Σ CAPEX(Stars/Questions)\nSurplus funds high-growth bets without external debt.", font=f_table, fill=(71, 85, 105))

    # Bottom Sheet Tabs
    tab_y = wy + wh - 30
    draw.rectangle([wx, tab_y, wx + ww, wy + wh], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    tabs = [
        ("Dashboard Ejecutivo" if is_es else "Executive Dashboard", (16, 124, 65), True),
        ("Evaluación Cartera" if is_es else "Portfolio Assessment", (100, 116, 139), False),
        ("Matriz & Flujo Fondos" if is_es else "BCG & Fund Flow", (100, 116, 139), False),
        ("Plan Asignación Capital" if is_es else "Capital Allocation Plan", (100, 116, 139), False),
    ]
    tbx = wx + 15
    for tab_name, tab_col, is_active in tabs:
        bbox = f_table_b.getbbox(tab_name)
        tbw = bbox[2] - bbox[0] + 18
        if is_active:
            draw.rounded_rectangle([tbx, tab_y - 2, tbx + tbw, wy + wh], radius=4, fill=(16, 124, 65))
            draw.text((tbx + 9, tab_y + 4), tab_name, font=f_table_b, fill=(255, 255, 255))
        else:
            draw.text((tbx + 9, tab_y + 4), tab_name, font=f_table, fill=tab_col)
        tbx += (tbw + 10)

    # =========================================================================
    # 3. RIGHT TOP: PDF GUIDE MOCKUP (x=985, y=115, w=575, h=370)
    # =========================================================================
    px, py, pw, ph = 985, 115, 575, 370
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=8, fill=(255, 255, 255), outline=(51, 65, 85), width=2)
    
    # Titlebar (PDF / Blue #1E3A8A)
    pdf_title_es = "Guía Metodológica Oficial (.pdf) — 5 Páginas C-Level"
    pdf_title_en = "Official Methodology Guide (.pdf) — 5 C-Level Pages"
    draw_window_header(draw, px, py, pw, 34, pdf_title_es if is_es else pdf_title_en, (30, 58, 138), f_win_title)

    # Inner PDF Page Header
    draw.rectangle([px + 15, py + 45, px + pw - 15, py + 75], fill=(248, 250, 252))
    draw.text((px + 25, py + 52), "DATALARIA EXECUTIVE FRAMEWORKS • ASIGNACIÓN DE CAPITAL BCG" if is_es else "DATALARIA EXECUTIVE FRAMEWORKS • BCG CAPITAL ALLOCATION", font=f_kpi_label, fill=(30, 58, 138))

    # PDF Formula Box
    draw.rounded_rectangle([px + 15, py + 85, px + pw - 15, py + 165], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((px + 25, py + 92), "DEMOSTRACIONES MATEMÁTICAS & FORMULACIÓN OFICIAL" if is_es else "MATHEMATICAL PROOFS & OFFICIAL FORMULATION", font=f_kpi_label, fill=(15, 23, 42))
    draw.text((px + 25, py + 110), "• Cuota Relativa (CMR) = Ventas UEN / Ventas Líder Competidor\n• Curva Experiencia Henderson: Cn = C1 · n^(-b)  (Reducción coste 20-30%)\n• Equilibrio Cartera: ΔFCF = Σ FCF(Vacas) - Σ CAPEX(Estrellas/Incógnitas)" if is_es else "• Relative Market Share (RMS) = SBU Revenue / Leader Revenue\n• Henderson Experience Curve: Cn = C1 · n^(-b)  (20-30% unit cost reduction)\n• Portfolio Balance: ΔFCF = Σ FCF(Cows) - Σ CAPEX(Stars/Questions)", font=f_table_b, fill=(30, 41, 59))

    # 4 Quadrant Decision Matrix Cards
    quad_cards = [
        ("⭐ ESTRELLAS" if is_es else "⭐ STARS", "Inversión agresiva; blindar cuota" if is_es else "Aggressive CAPEX; defend share", (20, 184, 166)),
        ("🐄 VACAS" if is_es else "🐄 CASH COWS", "Ordeñar FCF; CAPEX solo mantenimiento" if is_es else "Harvest FCF; maintenance CAPEX", (245, 158, 11)),
        ("❓ INTERROGANTES" if is_es else "❓ QUESTIONS", "Apuesta selectiva a Estrella o venta" if is_es else "Selectively bet or divest early", (59, 130, 246)),
        ("🐕 PERROS" if is_es else "🐕 DOGS", "Desinversión / cosecha final rápida" if is_es else "Divestment or rapid liquidation", (244, 63, 94)),
    ]
    for q_i, (q_t, q_d, q_c) in enumerate(quad_cards):
        qx = px + 15 + (q_i % 2) * ((pw - 40) // 2 + 10)
        qy = py + 175 + (q_i // 2) * 75
        qw = (pw - 40) // 2
        draw.rounded_rectangle([qx, qy, qx + qw, qy + 68], radius=6, fill=(248, 250, 252), outline=q_c, width=1)
        draw.text((qx + 10, qy + 8), q_t, font=f_table_b, fill=q_c)
        draw.text((qx + 10, qy + 28), q_d, font=f_table, fill=(71, 85, 105))

    # PDF Page Footer
    draw.text((px + 20, py + ph - 22), "Página 1 de 5 • Grado Consejo de Administración" if is_es else "Page 1 of 5 • Boardroom Standard & C-Level Audit", font=f_kpi_sub, fill=(148, 163, 184))

    # =========================================================================
    # 4. RIGHT BOTTOM: POWERPOINT 16:9 DECK (x=985, y=505, w=575, h=375)
    # =========================================================================
    sx, sy, sw, sh = 985, 505, 575, 375
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    
    # Titlebar (PowerPoint / Orange #C2410C)
    pptx_title_es = "Presentación Grado Consejo (.pptx 16:9 Widescreen)"
    pptx_title_en = "Boardroom Presentation (.pptx 16:9 Widescreen)"
    draw_window_header(draw, sx, sy, sw, 34, pptx_title_es if is_es else pptx_title_en, (194, 65, 12), f_win_title)

    # Slide Master Header / Action Title (Minto Pyramid)
    draw.rectangle([sx + 15, sy + 44, sx + sw - 15, sy + 100], fill=(24, 32, 47), outline=(30, 41, 59), width=1)
    draw.text((sx + 24, sy + 50), "SÍNTESIS EJECUTIVA (PIRÁMIDE DE MINTO):" if is_es else "EXECUTIVE SYNTHESIS (MINTO PYRAMID):", font=f_kpi_label, fill=(245, 158, 11))
    draw.text((sx + 24, sy + 66), "\"El 68% del flujo de caja depende de dos Vacas Lecheras en madurez:\nse requiere reasignar 450k€ a dos Interrogantes de alto crecimiento\"" if is_es else "\"68% of corporate cash flow relies on two mature Cash Cows:\nreallocating 450k€ to two Question Marks is required before Q4\"", font=f_table_b, fill=(248, 250, 252))

    # 4 Slide Content Cards
    slide_cards = [
        ("DIAGNÓSTICO CARTERA" if is_es else "PORTFOLIO HEALTH", "Concentración del 73% de ventas en negocios maduros." if is_es else "73% of sales concentrated in mature divisions.", (56, 189, 248)),
        ("FLUJO NETO LIQUIDEZ" if is_es else "NET CASH FLOW", "Superávit neto de 1.75 M€ para financiar innovación." if is_es else "1.75 M€ net surplus funding high-growth bets.", (52, 211, 153)),
        ("TRAMPAS DE CAPITAL" if is_es else "CAPITAL TRAPS", "2 Perros consumen 450k€ de CAPEX con ROIC < WACC." if is_es else "2 Dogs consume 450k€ CAPEX with ROIC < WACC.", (251, 113, 133)),
        ("RETORNO PROYECTADO" if is_es else "PROJECTED RETURN", "ROIC corporativo aumenta del 16.0% al 19.2% (+320 bps)." if is_es else "Corporate ROIC grows from 16.0% to 19.2% (+320 bps).", (251, 191, 36)),
    ]
    for s_i, (s_t, s_d, s_c) in enumerate(slide_cards):
        scx = sx + 15 + (s_i % 2) * ((sw - 40) // 2 + 10)
        scy = sy + 110 + (s_i // 2) * 85
        scw = (sw - 40) // 2
        draw.rounded_rectangle([scx, scy, scx + scw, scy + 78], radius=6, fill=(24, 32, 47), outline=(51, 65, 85), width=1)
        draw.text((scx + 10, scy + 8), s_t, font=f_kpi_label, fill=s_c)
        draw.text((scx + 10, scy + 26), s_d, font=f_table, fill=(226, 232, 240))

    # Board Decision Gateway Banner (Crucial Minto element)
    gw_y = sy + 290
    draw.rounded_rectangle([sx + 15, gw_y, sx + sw - 15, sy + sh - 15], radius=6, fill=(30, 58, 138), outline=(59, 130, 246), width=1)
    draw.text((sx + 25, gw_y + 10), "⚡ BOARD DECISION GATEWAY (DECISIÓN REQUERIDA):" if is_es else "⚡ BOARD DECISION GATEWAY (REQUIRED ACTION):", font=f_kpi_label, fill=(251, 191, 36))
    draw.text((sx + 25, gw_y + 30), "1. Aprobar reasignación de 450k€ de CAPEX a UENs Estrella e Interrogantes.\n2. Iniciar proceso de carve-out/venta de división Hardware POS antes de Q4." if is_es else "1. Approve 450k€ CAPEX reallocation to Star & Question Mark divisions.\n2. Initiate carve-out / trade sale of POS Hardware division prior to Q4.", font=f_table_b, fill=(255, 255, 255))

    # =========================================================================
    # 5. FOOTER (y = 900 .. 965)
    # =========================================================================
    # Left: Watermark
    draw.text((45, 915), "DATALARIA.COM • EXECUTIVE DECISION SUPPORT", font=f_footer_b, fill=(100, 116, 139))
    draw.text((45, 935), "Estándar Consultoría Tier-1 (McKinsey / BCG)" if is_es else "Tier-1 Consulting Standards (McKinsey / BCG)", font=f_kpi_sub, fill=(71, 85, 105))

    # Center: Guarantees
    center_text = "Fórmulas 100% Auditables • Celdas Desbloqueadas • Compatibilidad MS Excel & Google Sheets" if is_es else "100% Auditable Formulas • Unlocked Input Cells • MS Excel & Google Sheets Compatibility"
    draw.text((440, 925), center_text, font=f_footer, fill=(203, 213, 225))

    # Right: Instant Download Badge
    dl_badge = "⚡ Descarga Inmediata (.ZIP)" if is_es else "⚡ Instant Download (.ZIP)"
    draw.rounded_rectangle([W - 250, 915, W - 40, 947], radius=6, fill=(15, 36, 58), outline=(56, 189, 248), width=1)
    draw.text((W - 232, 923), dl_badge, font=f_footer_b, fill=(56, 189, 248))

    return im

def main():
    os.makedirs("static/images/recursos", exist_ok=True)
    os.makedirs("content/es/posts/matriz-bcg-dinamica", exist_ok=True)
    os.makedirs("content/en/posts/dynamic-bcg-matrix", exist_ok=True)

    # 1. Spanish preview
    im_es = generate_preview_pack(lang="es")
    p_static_es = "static/images/recursos/bcg-preview-es.png"
    p_post_es = "content/es/posts/matriz-bcg-dinamica/preview-pack.png"
    im_es.save(p_static_es, "PNG", optimize=True)
    im_es.save(p_post_es, "PNG", optimize=True)
    print(f"[OK] Generated {p_static_es} and {p_post_es} ({im_es.size})")

    # 2. English preview
    im_en = generate_preview_pack(lang="en")
    p_static_en = "static/images/recursos/bcg-preview-en.png"
    p_post_en = "content/en/posts/dynamic-bcg-matrix/preview-pack.png"
    im_en.save(p_static_en, "PNG", optimize=True)
    im_en.save(p_post_en, "PNG", optimize=True)
    print(f"[OK] Generated {p_static_en} and {p_post_en} ({im_en.size})")

if __name__ == "__main__":
    main()
