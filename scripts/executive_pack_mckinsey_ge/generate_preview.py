#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes de vista previa de alta resolución (1600x980 px) del
Executive Decision Pack de la Matriz McKinsey / GE 3x3 en español e inglés:
- static/images/recursos/mckinsey-ge-preview-es.png
- static/images/recursos/mckinsey-ge-preview-en.png
- content/es/posts/matriz-mckinsey-ge/preview-pack.png
- content/en/posts/mckinsey-ge-matrix/preview-pack.png

Cumple con el estándar visual exacto de DAFO, 5 Fuerzas de Porter, PESTEL y BCG:
- Lienzo 1600 x 980 px
- Header con badge, título y chips de entregables
- Ventana izquierda: Excel .xlsx con Dashboard 3x3 de 9 cajas y tabla maestra
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
    f_kpi_val = get_font(17, bold=True)
    f_kpi_sub = get_font(9, bold=False)
    f_body = get_font(11, bold=False)
    f_body_b = get_font(11, bold=True)
    f_chart_label = get_font(10.5, bold=True)
    f_chart_sub = get_font(8.5, bold=False)
    f_table = get_font(9.5, bold=False)
    f_table_b = get_font(9.5, bold=True)
    f_footer = get_font(11, bold=False)
    f_footer_b = get_font(11, bold=True)

    # =========================================================================
    # 1. HEADER (y = 25 .. 105)
    # =========================================================================
    badge_text = "★ EXECUTIVE DECISION PACK • ESTRATEGIA MBA" if is_es else "★ EXECUTIVE DECISION PACK • MBA STRATEGY"
    draw.rounded_rectangle([40, 26, 350, 48], radius=6, fill=(15, 36, 58), outline=(37, 99, 235), width=1)
    draw.text((48, 30), badge_text, font=f_badge, fill=(56, 189, 248))

    # Main Title
    title_text = "MATRIZ MCKINSEY / GE 3x3 DUAL" if is_es else "MCKINSEY / GE 3x3 MATRIX DUAL PACK"
    draw.text((40, 52), title_text, font=f_title, fill=(248, 250, 252))

    # Subtitle
    sub_text = "EVALUACIÓN MULTIFACTORIAL, ASIGNACIÓN DE CAPITAL C-LEVEL & GOBERNANZA 9 CAJAS" if is_es else "MULTIFACTOR EVALUATION, C-LEVEL CAPITAL ALLOCATION & 9-BOX GOVERNANCE"
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
    title_win_es = "Excel .xlsx — Motor Cuantitativo & Dashboard Ejecutivo McKinsey / GE"
    title_win_en = "Excel .xlsx — Quantitative Engine & McKinsey / GE Executive Dashboard"
    draw_window_header(draw, wx, wy, ww, 34, title_win_es if is_es else title_win_en, (16, 124, 65), f_win_title)

    # Formula / Toolbar Bar
    draw.rectangle([wx, wy + 34, wx + ww, wy + 62], fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    fx_text_es = "fx: =SI(F30>=3.67; SI(G30>=3.67; \"Invertir para Liderar\"; SI(G30>=2.33; \"Invertir para Desarrollar\"; \"Selectividad\")); ...)"
    fx_text_en = "fx: =IF(F30>=3.67, IF(G30>=3.67, \"Invest to Lead\", IF(G30>=2.33, \"Invest to Build\", \"Selectivity\")), ...)"
    draw.text((wx + 15, wy + 41), fx_text_es if is_es else fx_text_en, font=f_table, fill=(71, 85, 105))

    # Top KPI Row (5 Cards)
    kpis = [
        ("FACTURACIÓN TOTAL" if is_es else "TOTAL REVENUE", "485.0 M€", "10 UENs Auditadas" if is_es else "10 SBUs Audited", (15, 23, 42)),
        ("EN ZONA INVERTIR" if is_es else "IN INVEST ZONE", "65.8%", "319.0 M€ (Verde)" if is_es else "$319.0M (Green)", (5, 150, 105)),
        ("EN SELECTIVIDAD" if is_es else "IN SELECTIVITY", "26.4%", "128.0 M€ (Ámbar)" if is_es else "$128.0M (Amber)", (217, 119, 6)),
        ("EN COSECHA" if is_es else "IN HARVEST", "7.8%", "38.0 M€ (Carve-out)" if is_es else "$38.0M (Carve-out)", (225, 29, 72)),
        ("CAPEX 3A TOTAL" if is_es else "TOTAL 3Y CAPEX", "82.7 M€", "ROIC: +380 bps" if is_es else "ROIC: +380 bps", (37, 99, 235)),
    ]
    kw = (ww - 50) // 5
    for i, (k_label, k_val, k_sub, k_col) in enumerate(kpis):
        kx = wx + 12 + i * (kw + 6)
        ky = wy + 72
        draw.rounded_rectangle([kx, ky, kx + kw, ky + 58], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((kx + 10, ky + 8), k_label, font=f_kpi_label, fill=(100, 116, 139))
        draw.text((kx + 10, ky + 22), k_val, font=f_kpi_val, fill=k_col)
        draw.text((kx + 10, ky + 43), k_sub, font=f_kpi_sub, fill=(100, 116, 139))

    # Main Split inside Excel:
    # Left: 3x3 Grid (w=470), Right: SBU Master Table (w=420)
    gx, gy, gw, gh = wx + 15, wy + 140, 465, 580
    draw.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)

    # 3x3 Grid Header
    draw.rectangle([gx, gy, gx + gw, gy + 30], fill=(15, 23, 42))
    draw.text((gx + 12, gy + 8), "MATRIZ MCKINSEY / GE (9-BOX GRID)" if is_es else "MCKINSEY / GE MATRIX (9-BOX GRID)", font=f_chart_label, fill=(255, 255, 255))

    # Axis Labels
    col_w = (gw - 40) // 3
    row_h = (gh - 75) // 3
    g_x0 = gx + 35
    g_y0 = gy + 45

    # Column Headers (X Axis: Competitive Strength)
    cols_x = [
        ("FUERTE" if is_es else "STRONG", "[3.67 - 5.00]"),
        ("MEDIA" if is_es else "MEDIUM", "[2.33 - 3.66]"),
        ("DÉBIL" if is_es else "WEAK", "[1.00 - 2.32]")
    ]
    for c_i, (c_main, c_sub) in enumerate(cols_x):
        cx_pos = g_x0 + c_i * col_w
        draw.rectangle([cx_pos, gy + 32, cx_pos + col_w - 4, gy + 44], fill=(241, 245, 249))
        draw.text((cx_pos + 8, gy + 33), f"{c_main} {c_sub}", font=f_chart_sub, fill=(71, 85, 105))

    # 9 Boxes Data: (row, col, zone_name, zone_type, color_bg, color_border, color_txt, uens)
    boxes_9 = [
        # Row 0 (High Industry Attractiveness)
        (0, 0, "INVERTIR P/ LIDERAR" if is_es else "INVEST TO LEAD", "Verde", (209, 250, 229), (16, 185, 129), (6, 95, 70), "UEN-01, UEN-02"),
        (0, 1, "INVERTIR P/ CONSTRUIR" if is_es else "INVEST TO BUILD", "Verde", (209, 250, 229), (16, 185, 129), (6, 95, 70), "UEN-03"),
        (0, 2, "DOBLAR O SALIR" if is_es else "DOUBLE OR QUIT", "Ámbar", (254, 243, 199), (245, 158, 11), (146, 64, 14), "UEN-07"),
        # Row 1 (Medium Industry Attractiveness)
        (1, 0, "CRECER SELECTIVO" if is_es else "SELECTIVE GROWTH", "Verde", (209, 250, 229), (16, 185, 129), (6, 95, 70), "(Foco Liderazgo)"),
        (1, 1, "RENTABILIZAR" if is_es else "MAXIMIZE RETURN", "Ámbar", (254, 243, 199), (245, 158, 11), (146, 64, 14), "UEN-04, UEN-05"),
        (1, 2, "REESTRUCTURAR" if is_es else "RESTRUCTURE", "Rojo", (254, 226, 226), (239, 68, 68), (153, 27, 27), "UEN-08"),
        # Row 2 (Low Industry Attractiveness)
        (2, 0, "PROTEGER MARGEN" if is_es else "PROTECT CASH", "Ámbar", (254, 243, 199), (245, 158, 11), (146, 64, 14), "UEN-06"),
        (2, 1, "COSECHA CONTROLADA" if is_es else "CONTROLLED HARVEST", "Rojo", (254, 226, 226), (239, 68, 68), (153, 27, 27), "UEN-09"),
        (2, 2, "DESINVERTIR / CARVE-OUT" if is_es else "DIVEST / CARVE-OUT", "Rojo", (254, 226, 226), (239, 68, 68), (153, 27, 27), "UEN-10"),
    ]

    for r_i, c_i, b_title, b_ztype, b_bg, b_border, b_txt, b_uens in boxes_9:
        bx = g_x0 + c_i * col_w
        by = g_y0 + r_i * row_h
        draw.rounded_rectangle([bx, by, bx + col_w - 4, by + row_h - 4], radius=6, fill=b_bg, outline=b_border, width=1)
        draw.text((bx + 6, by + 8), b_title, font=f_chart_label, fill=b_txt)
        draw.text((bx + 6, by + 26), f"[{b_ztype}]", font=f_chart_sub, fill=b_border)
        draw.text((bx + 6, by + 46), b_uens, font=f_table_b, fill=(15, 23, 42))

    # Y-Axis Labels (Left)
    y_labels = ["ALTO" if is_es else "HIGH", "MEDIO" if is_es else "MED", "BAJO" if is_es else "LOW"]
    for y_i, y_txt in enumerate(y_labels):
        by = g_y0 + y_i * row_h
        draw.rectangle([gx + 4, by, g_x0 - 4, by + row_h - 4], fill=(30, 41, 59))
        draw.text((gx + 7, by + row_h // 2 - 8), y_txt, font=f_chart_sub, fill=(255, 255, 255))

    # X-Axis Footer
    draw.text((gx + 50, gy + gh - 22), "Eje X: Fortaleza Competitiva (FC)  •  Eje Y: Atractivo de Industria (IA)" if is_es else "X-Axis: BU Strength (FC)  •  Y-Axis: Industry Attractiveness (IA)", font=f_table, fill=(100, 116, 139))

    # Right: Data Table inside Excel (x=wx+490, y=wy+140, w=420, h=580)
    tx, ty, tw, th = wx + 490, wy + 140, 420, 580
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)

    # Table Header
    draw.rectangle([tx, ty, tx + tw, ty + 30], fill=(15, 23, 42))
    draw.text((tx + 10, ty + 8), "CARTERA CONSOLIDADA (10 UENs)" if is_es else "CONSOLIDATED PORTFOLIO (10 SBUs)", font=f_table_b, fill=(255, 255, 255))

    # Table Columns Header
    draw.rectangle([tx, ty + 30, tx + tw, ty + 56], fill=(241, 245, 249))
    draw.text((tx + 8, ty + 38), "UEN" if is_es else "SBU", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 45, ty + 38), "Nombre UEN" if is_es else "Business Unit", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 175, ty + 38), "Ventas" if is_es else "Sales", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 230, ty + 38), "IA", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 265, ty + 38), "FC", font=f_table_b, fill=(71, 85, 105))
    draw.text((tx + 300, ty + 38), "Zona Capital" if is_es else "Capital Zone", font=f_table_b, fill=(71, 85, 105))

    # Table SBU Rows
    rows_sbu = [
        ("UEN-01", "Cloud e IA Industrial" if is_es else "Industrial Cloud AI", "95.0 M€", "4.64", "4.63", "🟢 Invertir" if is_es else "🟢 Invest", (16, 185, 129)),
        ("UEN-02", "Robótica Quirúrgica" if is_es else "Surgical Robotics", "72.0 M€", "4.61", "3.81", "🟢 Invertir" if is_es else "🟢 Invest", (16, 185, 129)),
        ("UEN-03", "Electrónica Potencia" if is_es else "Power Electronics", "110.0 M€", "3.72", "4.20", "🟢 Invertir" if is_es else "🟢 Invest", (16, 185, 129)),
        ("UEN-04", "Sensores Industriales" if is_es else "Smart Sensors", "68.0 M€", "3.29", "3.49", "🟡 Seleccionar" if is_es else "🟡 Select", (245, 158, 11)),
        ("UEN-05", "Telemática Flotas" if is_es else "Fleet Telematics", "35.0 M€", "3.57", "2.72", "🟡 Seleccionar" if is_es else "🟡 Select", (245, 158, 11)),
        ("UEN-06", "Sistemas HVAC" if is_es else "HVAC Systems", "42.0 M€", "2.25", "4.09", "🟡 Seleccionar" if is_es else "🟡 Select", (245, 158, 11)),
        ("UEN-07", "Aleaciones Nicho" if is_es else "Precision Alloys", "25.0 M€", "3.91", "1.98", "🟡 Seleccionar" if is_es else "🟡 Select", (245, 158, 11)),
        ("UEN-08", "Válvulas Pesadas" if is_es else "Hydraulic Valves", "18.0 M€", "2.64", "1.95", "🔴 Cosechar" if is_es else "🔴 Harvest", (239, 68, 68)),
        ("UEN-09", "Cableado Estándar" if is_es else "Standard Wiring", "12.0 M€", "1.90", "2.52", "🔴 Cosechar" if is_es else "🔴 Harvest", (239, 68, 68)),
        ("UEN-10", "Medidores Analógicos" if is_es else "Analog Meters", "8.0 M€", "1.57", "1.60", "🔴 Desinvertir" if is_es else "🔴 Divest", (239, 68, 68)),
    ]

    for r_i, (r_cod, r_name, r_rev, r_ia, r_fc, r_zone, r_col) in enumerate(rows_sbu):
        ry = ty + 56 + r_i * 26
        row_bg = (248, 250, 252) if (r_i % 2 == 0) else (255, 255, 255)
        draw.rectangle([tx, ry, tx + tw, ry + 26], fill=row_bg)
        draw.text((tx + 8, ry + 5), r_cod, font=f_table_b, fill=(15, 23, 42))
        draw.text((tx + 45, ry + 5), r_name, font=f_table, fill=(30, 41, 59))
        draw.text((tx + 175, ry + 5), r_rev, font=f_table_b, fill=(15, 23, 42))
        draw.text((tx + 230, ry + 5), r_ia, font=f_table, fill=(100, 116, 139))
        draw.text((tx + 265, ry + 5), r_fc, font=f_table, fill=(100, 116, 139))
        draw.text((tx + 300, ry + 5), r_zone, font=f_table_b, fill=r_col)

    # Capital Allocation Policy Box in Table Bottom
    cap_y = ty + 322
    draw.rounded_rectangle([tx + 10, cap_y, tx + tw - 10, cap_y + 115], radius=6, fill=(240, 253, 250), outline=(16, 185, 129), width=1)
    draw.text((tx + 18, cap_y + 8), "MANDATO DE ASIGNACIÓN DE CAPITAL C-LEVEL" if is_es else "C-LEVEL CAPITAL ALLOCATION MANDATE", font=f_table_b, fill=(6, 95, 70))
    pol_text_es = (
        "• Zona Verde (Invertir): 65%-75% CAPEX (TIR &ge; 18.0%)\n"
        "• Zona Ámbar (Selectividad): 20%-30% CAPEX (Autofinanciada)\n"
        "• Zona Roja (Cosechar): 0%-5% CAPEX (Mandato Carve-out &lt;12M)"
    )
    pol_text_en = (
        "• Green Zone (Invest): 65%-75% CAPEX (IRR &ge; 18.0%)\n"
        "• Amber Zone (Selectivity): 20%-30% CAPEX (Self-Funded)\n"
        "• Red Zone (Harvest): 0%-5% CAPEX (Mandatory Carve-out &lt;12M)"
    )
    draw.text((tx + 18, cap_y + 28), pol_text_es if is_es else pol_text_en, font=f_table, fill=(15, 118, 110))

    # Governance & ROIC Rule
    gov_y = cap_y + 122
    draw.rounded_rectangle([tx + 10, gov_y, tx + tw - 10, ty + th - 15], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((tx + 18, gov_y + 8), "REGLA DE GOBERNANZA VINCULANTE:" if is_es else "BINDING GOVERNANCE RULE:", font=f_kpi_label, fill=(100, 116, 139))
    gov_body_es = "Reasignación de 51M€ a Zona Verde y desinversión de 3 unidades\neleva el ROIC corporativo del 11.2% al 15.0% (+380 bps en 36M)."
    gov_body_en = "Reallocating 51M€ to Green Zone and divesting 3 harvest units\nexpands corporate ROIC from 11.2% to 15.0% (+380 bps in 36M)."
    draw.text((tx + 18, gov_y + 24), gov_body_es if is_es else gov_body_en, font=f_table, fill=(71, 85, 105))

    # Bottom Sheet Tabs
    tab_y = wy + wh - 30
    draw.rectangle([wx, tab_y, wx + ww, wy + wh], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    tabs = [
        ("01_Dashboard_Ejecutivo" if is_es else "01_Executive_Dashboard", (16, 124, 65), True),
        ("02_Evaluacion_Multifactorial" if is_es else "02_Multifactor_Assessment", (100, 116, 139), False),
        ("03_Plan_Asignacion_Capital" if is_es else "03_Capital_Allocation_Plan", (100, 116, 139), False),
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
    draw.text((px + 25, py + 52), "DATALARIA EXECUTIVE FRAMEWORKS • MATRIZ MCKINSEY / GE 3x3" if is_es else "DATALARIA EXECUTIVE FRAMEWORKS • MCKINSEY / GE 3x3 MATRIX", font=f_kpi_label, fill=(30, 58, 138))

    # PDF Formula Box
    draw.rounded_rectangle([px + 15, py + 85, px + pw - 15, py + 165], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((px + 25, py + 92), "DEMOSTRACIONES MATEMÁTICAS & FORMULACIÓN OFICIAL" if is_es else "MATHEMATICAL PROOFS & OFFICIAL FORMULATION", font=f_kpi_label, fill=(15, 23, 42))
    f_txt_es = (
        "• Atractivo Industria: IA = Σ wi · Ai  (5 criterios macro, sector y ESG)\n"
        "• Fortaleza UEN: FC = Σ vj · Cj  (5 criterios cuota, tecnología y margen)\n"
        "• Umbrales de Frontera Canónicos: T1 = 2.33 (Bajo/Medio) y T2 = 3.67 (Medio/Alto)"
    )
    f_txt_en = (
        "• Industry Attractiveness: IA = Σ wi · Ai  (5 macro, sector & ESG criteria)\n"
        "• SBU Strength: FC = Σ vj · Cj  (5 share, tech & margin criteria)\n"
        "• Canonical Thresholds: T1 = 2.33 (Low/Med) and T2 = 3.67 (Med/High)"
    )
    draw.text((px + 25, py + 110), f_txt_es if is_es else f_txt_en, font=f_table_b, fill=(30, 41, 59))

    # 3 Strategic Zone Decision Matrix Cards
    zone_cards = [
        ("🟢 ZONA VERDE (Invertir)" if is_es else "🟢 GREEN ZONE (Invest)", "Prioridad máxima CAPEX; I+D y M&A; TIR &ge; 18%" if is_es else "Top CAPEX priority; R&D & M&A; IRR &ge; 18%", (16, 185, 129)),
        ("🟡 ZONA ÁMBAR (Selectividad)" if is_es else "🟡 AMBER ZONE (Hold)", "Inversión autofinanciada; foco nichos; TIR &ge; 14%" if is_es else "Self-funded CAPEX; high-value niches; IRR &ge; 14%", (245, 158, 11)),
        ("🔴 ZONA ROJA (Cosechar)" if is_es else "🔴 RED ZONE (Harvest)", "Congelación CAPEX; maximizar FCF; desinvertir &lt;12M" if is_es else "Freeze non-critical CAPEX; harvest FCF; divest &lt;12M", (239, 68, 68)),
    ]
    for q_i, (q_t, q_d, q_c) in enumerate(zone_cards):
        qx = px + 15
        qy = py + 175 + q_i * 56
        qw = pw - 30
        draw.rounded_rectangle([qx, qy, qx + qw, qy + 50], radius=6, fill=(248, 250, 252), outline=q_c, width=1)
        draw.text((qx + 14, qy + 8), q_t, font=f_table_b, fill=q_c)
        draw.text((qx + 14, qy + 26), q_d, font=f_table, fill=(71, 85, 105))

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
    s_title_es = "\"El 66% de ingresos opera en sectores atractivos: se aprueba concentrar\n51M€ en Zona Verde y desinvertir 3 líneas rojas antes de Q4\""
    s_title_en = "\"66% of portfolio revenues operate in high-attractiveness markets: approving\n51M€ Green Zone CAPEX and divesting 3 red units before Q4\""
    draw.text((sx + 24, sy + 66), s_title_es if is_es else s_title_en, font=f_table_b, fill=(248, 250, 252))

    # 4 Slide Content Cards
    slide_cards = [
        ("DIAGNÓSTICO CARTERA" if is_es else "PORTFOLIO HEALTH", "10 UENs mapeadas en matriz continua 3x3." if is_es else "10 SBUs mapped in continuous 3x3 grid.", (56, 189, 248)),
        ("CONCENTRACIÓN CAPEX" if is_es else "CAPEX FOCUS", "68% en Verde, 27% en Ámbar, 5% en Rojo." if is_es else "68% Green, 27% Amber, 5% Red split.", (52, 211, 153)),
        ("DESINVERSIÓN M&A" if is_es else "M&A CARVE-OUT", "Venta de 3 unidades libera 24M€ de caja." if is_es else "Trade sale of 3 units releases 24M€ cash.", (251, 113, 133)),
        ("EXPANSIÓN EN ROIC" if is_es else "ROIC EXPANSION", "ROIC corporativo aumenta del 11.2% al 15.0%." if is_es else "Corporate ROIC grows from 11.2% to 15.0%.", (251, 191, 36)),
    ]
    for s_i, (s_t, s_d, s_c) in enumerate(slide_cards):
        scx = sx + 15 + (s_i % 2) * ((sw - 40) // 2 + 10)
        scy = sy + 110 + (s_i // 2) * 85
        scw = (sw - 40) // 2
        draw.rounded_rectangle([scx, scy, scx + scw, scy + 78], radius=6, fill=(24, 32, 47), outline=(51, 65, 85), width=1)
        draw.text((scx + 10, scy + 8), s_t, font=f_kpi_label, fill=s_c)
        draw.text((scx + 10, scy + 26), s_d, font=f_table, fill=(226, 232, 240))

    # Board Decision Gateway Banner
    gw_y = sy + 290
    draw.rounded_rectangle([sx + 15, gw_y, sx + sw - 15, sy + sh - 15], radius=6, fill=(30, 58, 138), outline=(59, 130, 246), width=1)
    draw.text((sx + 25, gw_y + 10), "⚡ BOARD DECISION GATEWAY (DECISIÓN REQUERIDA):" if is_es else "⚡ BOARD DECISION GATEWAY (REQUIRED ACTION):", font=f_kpi_label, fill=(251, 191, 36))
    gw_txt_es = "1. Aprobar reasignación de 51M€ de CAPEX a UEN-01, UEN-02 y UEN-03.\n2. Iniciar proceso de carve-out para desinvertir UEN-08, UEN-09 y UEN-10 en <12M."
    gw_txt_en = "1. Approve 51M€ CAPEX allocation to SBU-01, SBU-02 and SBU-03.\n2. Mandate carve-out process to divest SBU-08, SBU-09 and SBU-10 within 12M."
    draw.text((sx + 25, gw_y + 30), gw_txt_es if is_es else gw_txt_en, font=f_table_b, fill=(255, 255, 255))

    # =========================================================================
    # 5. FOOTER (y = 900 .. 965)
    # =========================================================================
    draw.text((45, 915), "DATALARIA.COM • EXECUTIVE DECISION SUPPORT", font=f_footer_b, fill=(100, 116, 139))
    draw.text((45, 935), "Estándar Consultoría Tier-1 (McKinsey / BCG)" if is_es else "Tier-1 Consulting Standards (McKinsey / BCG)", font=f_kpi_sub, fill=(71, 85, 105))

    center_text = "Fórmulas 100% Auditables • Celdas Desbloqueadas • Compatibilidad MS Excel & Google Sheets" if is_es else "100% Auditable Formulas • Unlocked Input Cells • MS Excel & Google Sheets Compatibility"
    draw.text((440, 925), center_text, font=f_footer, fill=(203, 213, 225))

    dl_badge = "⚡ Descarga Inmediata (.ZIP)" if is_es else "⚡ Instant Download (.ZIP)"
    draw.rounded_rectangle([W - 250, 915, W - 40, 947], radius=6, fill=(15, 36, 58), outline=(56, 189, 248), width=1)
    draw.text((W - 232, 923), dl_badge, font=f_footer_b, fill=(56, 189, 248))

    return im


def main():
    os.makedirs("static/images/recursos", exist_ok=True)
    os.makedirs("content/es/posts/matriz-mckinsey-ge", exist_ok=True)
    os.makedirs("content/en/posts/mckinsey-ge-matrix", exist_ok=True)

    # 1. Spanish preview
    im_es = generate_preview_pack(lang="es")
    p_static_es = "static/images/recursos/mckinsey-ge-preview-es.png"
    p_post_es = "content/es/posts/matriz-mckinsey-ge/preview-pack.png"
    im_es.save(p_static_es, "PNG", optimize=True)
    im_es.save(p_post_es, "PNG", optimize=True)
    print(f"[OK] Generated {p_static_es} and {p_post_es} ({im_es.size})")

    # 2. English preview
    im_en = generate_preview_pack(lang="en")
    p_static_en = "static/images/recursos/mckinsey-ge-preview-en.png"
    p_post_en = "content/en/posts/mckinsey-ge-matrix/preview-pack.png"
    im_en.save(p_static_en, "PNG", optimize=True)
    im_en.save(p_post_en, "PNG", optimize=True)
    print(f"[OK] Generated {p_static_en} and {p_post_en} ({im_en.size})")


if __name__ == "__main__":
    main()
