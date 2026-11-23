#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes compuestas `preview-pack.png` (1600 x 980 px) a partir de los
activos reales generados en `packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/`:
- Excel Dashboard: métricas reales de `Cuadro_Mando_EVM_Datalaria_ES.xlsx` / `EVM_Dashboard_Datalaria_EN.xlsx`
  (BAC=1.200.000€, PV=600.000€, EV=516.000€, AC=600.000€, CPI=0.86x, SPI=0.86x, EAC1=1.395.349€,
  Curva S M01-M12 y Plan de Recuperación WBS).
- Guía PDF: renderizado real de páginas 1 y 2 vía `pypdfium2` / `fitz`.
- Deck PPTX 16:9: exportación real de Slide 2 vía PowerPoint COM (con fallback Pillow seguro).

Salidas:
- static/images/recursos/evm-preview-es.png
- content/es/posts/cuadro-mando-evm-valor-ganado/preview-pack.png
- static/images/recursos/evm-preview-en.png
- content/en/posts/earned-value-management-evm-dashboard/preview-pack.png
"""

import os
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PKG_DIR = ROOT_DIR / "packages" / "Suite_03_Control_Operativo" / "04_Cuadro_EVM_Valor_Ganado"

W, H = 1600, 980


def get_font(name: str, size: int):
    paths = [
        rf"C:\Windows\Fonts\{name}",
        rf"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def text_w(draw: ImageDraw.ImageDraw, txt: str, font) -> int:
    b = draw.textbbox((0, 0), txt, font=font)
    return b[2] - b[0]


def paste_with_shadow(canvas: Image.Image, panel: Image.Image, xy: tuple[int, int]):
    x, y = xy
    pad = 18
    sh = Image.new("RGBA", (panel.width + pad * 2, panel.height + pad * 2), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.rounded_rectangle(
        [(pad, pad + 6), (pad + panel.width, pad + panel.height + 6)],
        radius=12,
        fill=(2, 6, 23, 145),
    )
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    canvas.alpha_composite(sh, (x - pad, y - pad))
    canvas.alpha_composite(panel.convert("RGBA"), (x, y))


def make_window_chrome(width: int, height: int, title: str, badge_txt: str, badge_bg=(37, 99, 235), body_bg=(248, 250, 252)) -> Image.Image:
    win = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(win)
    d.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=12, fill=body_bg + (255,), outline=(51, 65, 85, 255), width=2)
    d.rounded_rectangle([(0, 0), (width - 1, 38)], radius=12, fill=(15, 23, 42, 255))
    d.rectangle([(0, 22), (width - 1, 38)], fill=(15, 23, 42, 255))
    d.line([(0, 38), (width - 1, 38)], fill=(51, 65, 85, 255), width=1)
    for idx, col in enumerate([(239, 68, 68), (245, 158, 11), (16, 185, 129)]):
        cx = 20 + idx * 18
        d.ellipse([(cx - 5, 14), (cx + 5, 24)], fill=col)
    f_title = get_font("segoeuib.ttf", 13)
    f_badge = get_font("segoeuib.ttf", 11)
    d.text((78, 11), title, fill=(226, 232, 240), font=f_title)
    bw = text_w(d, badge_txt, f_badge) + 20
    d.rounded_rectangle([(width - bw - 14, 9), (width - 14, 29)], radius=5, fill=badge_bg)
    d.text((width - bw - 4, 12), badge_txt, fill=(255, 255, 255), font=f_badge)
    return win


def render_pdf_pages(pdf_path: Path, page_indices=(0, 1), target_h=416) -> list[Image.Image]:
    imgs = []
    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(str(pdf_path))
        for idx in page_indices:
            if idx >= len(doc):
                continue
            page = doc[idx]
            pil_img = page.render(scale=2.0).to_pil().convert("RGBA")
            scale = target_h / pil_img.height
            new_w = int(pil_img.width * scale)
            imgs.append(pil_img.resize((new_w, target_h), Image.Resampling.LANCZOS))
        doc.close()
        return imgs
    except Exception:
        pass

    import fitz
    doc = fitz.open(str(pdf_path))
    for idx in page_indices:
        if idx >= len(doc):
            continue
        page = doc[idx]
        pix = page.get_pixmap(dpi=150)
        pil_img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples if pix.alpha else pix.tobytes("png")) if False else None
        from io import BytesIO
        pil_img = Image.open(BytesIO(pix.tobytes("png"))).convert("RGBA")
        scale = target_h / pil_img.height
        new_w = int(pil_img.width * scale)
        imgs.append(pil_img.resize((new_w, target_h), Image.Resampling.LANCZOS))
    doc.close()
    return imgs


def export_pptx_slide_com(pptx_path: Path, slide_num=2) -> Image.Image | None:
    try:
        import pythoncom
        import win32com.client

        pythoncom.CoInitialize()
        app = None
        pres = None
        with tempfile.TemporaryDirectory() as tmpdir:
            out_img = Path(tmpdir) / "slide.png"
            try:
                app = win32com.client.DispatchEx("PowerPoint.Application")
                pres = app.Presentations.Open(str(pptx_path.resolve()), ReadOnly=True, Untitled=False, WithWindow=False)
                if len(pres.Slides) >= slide_num:
                    pres.Slides[slide_num - 1].Export(str(out_img), "PNG", 1280, 720)
                if out_img.exists():
                    return Image.open(out_img).convert("RGBA").copy()
            finally:
                if pres is not None:
                    try:
                        pres.Close()
                    except Exception:
                        pass
                if app is not None:
                    try:
                        app.Quit()
                    except Exception:
                        pass
                pythoncom.CoUninitialize()
    except Exception as e:
        print(f"   [WARN] PowerPoint COM fallback triggered ({e})")
    return None


def draw_excel_dashboard_window(lang: str) -> Image.Image:
    win_w, win_h = 900, 924
    title = (
        "Cuadro_Mando_EVM_Datalaria_ES.xlsx — Excel 365 & Google Sheets"
        if lang == "ES"
        else "EVM_Dashboard_Datalaria_EN.xlsx — Excel 365 & Google Sheets"
    )
    badge = "MODELO PROTEGIDO · 4 PESTAÑAS" if lang == "ES" else "PROTECTED ENGINE · 4 TABS"
    win = make_window_chrome(win_w, win_h, title, badge, badge_bg=(5, 150, 105), body_bg=(248, 250, 252))
    d = ImageDraw.Draw(win)

    f_h1 = get_font("segoeuib.ttf", 16)
    f_sub = get_font("segoeui.ttf", 11)
    f_b11 = get_font("segoeuib.ttf", 11)
    f_r11 = get_font("segoeui.ttf", 11)
    f_r10 = get_font("segoeui.ttf", 10)
    f_kpi = get_font("segoeuib.ttf", 21)
    f_mono = get_font("consola.ttf", 11)
    f_monob = get_font("consolab.ttf", 11)

    # Sheet header banner
    d.rounded_rectangle([(14, 48), (win_w - 14, 104)], radius=8, fill=(15, 23, 42))
    h_txt = (
        "CUADRO DE MANDO EJECUTIVO EVM (EARNED VALUE MANAGEMENT)"
        if lang == "ES"
        else "EXECUTIVE EVM DASHBOARD (EARNED VALUE MANAGEMENT)"
    )
    s_txt = (
        "Estándar ANSI/EIA-748 & PMBOK · Proyecto: Transformación Core · Corte: Mes 6 (50%)"
        if lang == "ES"
        else "ANSI/EIA-748 & PMBOK Standard · Project: Core Transformation · Cutoff: Month 6 (50%)"
    )
    d.text((28, 56), h_txt, fill=(255, 255, 255), font=f_h1)
    d.text((28, 80), s_txt, fill=(148, 163, 184), font=f_sub)

    # 4 Top KPI Cards
    kpis_es = [
        ("PRESUPUESTO TOTAL (BAC)", "1.200.000 €", "PV Corte: 600.000 €", (239, 246, 255), (37, 99, 235), (30, 58, 138)),
        ("ÍNDICE COSTE (CPI)", "0.86x", "EV 516k · AC 600k · CV -84k€", (254, 242, 242), (220, 38, 38), (185, 28, 28)),
        ("ÍNDICE PLAZO (SPI)", "0.86x", "Retraso: -84.000 € (-3 sem.)", (255, 251, 235), (217, 119, 6), (180, 83, 9)),
        ("PREVISIÓN CIERRE (EAC₁)", "1.395.349 €", "VAC -195k€ · TCPI 1.14x", (245, 243, 255), (124, 58, 237), (109, 40, 217)),
    ]
    kpis_en = [
        ("TOTAL BUDGET (BAC)", "$1,200,000", "Cutoff PV: $600,000", (239, 246, 255), (37, 99, 235), (30, 58, 138)),
        ("COST INDEX (CPI)", "0.86x", "EV $516k · AC $600k · CV -$84k", (254, 242, 242), (220, 38, 38), (185, 28, 28)),
        ("SCHEDULE INDEX (SPI)", "0.86x", "Variance SV: -$84,000 (-3 wks)", (255, 251, 235), (217, 119, 6), (180, 83, 9)),
        ("FORECAST AT END (EAC₁)", "$1,395,349", "VAC -$195k · TCPI 1.14x", (245, 243, 255), (124, 58, 237), (109, 40, 217)),
    ]
    kpis = kpis_es if lang == "ES" else kpis_en
    cw = (win_w - 28 - 36) // 4
    ky = 116
    for i, (lbl, val, sub, bg, bdr, col) in enumerate(kpis):
        kx = 14 + i * (cw + 12)
        d.rounded_rectangle([(kx, ky), (kx + cw, ky + 82)], radius=8, fill=bg, outline=bdr, width=1)
        d.text((kx + 12, ky + 9), lbl, fill=(71, 85, 105), font=get_font("segoeuib.ttf", 9))
        d.text((kx + 12, ky + 28), val, fill=col, font=f_kpi)
        d.text((kx + 12, ky + 60), sub, fill=(100, 116, 139), font=f_r10)

    # Middle Left: EAC Models & TCPI Reality Test + Quadrant Matrix
    mx, my, mw, mh = 14, 210, 392, 392
    d.rounded_rectangle([(mx, my), (mx + mw, my + mh)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(mx, my), (mx + mw, my + 30)], radius=8, fill=(30, 41, 59))
    d.rectangle([(mx, my + 16), (mx + mw, my + 30)], fill=(30, 41, 59))
    calc_t = "MODELOS PREDICTIVOS EAC & TEST TCPI" if lang == "ES" else "EAC FORECASTING MODELS & TCPI TEST"
    d.text((mx + 12, my + 8), calc_t, fill=(255, 255, 255), font=f_b11)

    rows_calc = (
        [
            ("EAC₁ Típico (BAC/CPI):", "1.395.349 €", (245, 243, 255), (109, 40, 217)),
            ("EAC₂ Atípico (AC+Rem):", "1.284.000 €", (248, 250, 252), (15, 23, 42)),
            ("EAC₃ Compuesto (CPI×SPI):", "1.524.824 €", (254, 242, 242), (185, 28, 28)),
            ("TCPI (BAC Original):", "1.14x INVIABLE", (254, 242, 242), (220, 38, 38)),
            ("TCPI (Techo EAC₁):", "0.86x VIABLE", (240, 253, 244), (5, 150, 105)),
        ]
        if lang == "ES"
        else [
            ("EAC₁ Typical (BAC/CPI):", "$1,395,349", (245, 243, 255), (109, 40, 217)),
            ("EAC₂ Atypical (AC+Rem):", "$1,284,000", (248, 250, 252), (15, 23, 42)),
            ("EAC₃ Combined (CPI×SPI):", "$1,524,824", (254, 242, 242), (185, 28, 28)),
            ("TCPI (Original BAC):", "1.14x UNVIABLE", (254, 242, 242), (220, 38, 38)),
            ("TCPI (Revised EAC₁):", "0.86x VIABLE", (240, 253, 244), (5, 150, 105)),
        ]
    )
    ry = my + 38
    for lbl, val, rbg, vcol in rows_calc:
        d.rectangle([(mx + 10, ry), (mx + mw - 10, ry + 26)], fill=rbg, outline=(226, 232, 240))
        d.text((mx + 16, ry + 6), lbl, fill=(51, 65, 85), font=f_r11)
        vw = text_w(d, val, f_monob)
        d.text((mx + mw - 18 - vw, ry + 6), val, fill=vcol, font=f_monob)
        ry += 28

    # 2x2 Quadrant Status Grid inside Middle Left
    qy0 = ry + 10
    q_hdr = "MATRIZ DE SALUD OPERATIVA (CPI vs SPI)" if lang == "ES" else "OPERATIONAL HEALTH MATRIX (CPI vs SPI)"
    d.rectangle([(mx + 10, qy0), (mx + mw - 10, qy0 + 24)], fill=(15, 23, 42))
    d.text((mx + 16, qy0 + 5), q_hdr, fill=(255, 255, 255), font=get_font("segoeuib.ttf", 10))
    qy0 += 28
    qw_box = (mw - 28) // 2
    qh_box = 78
    quads = (
        [
            (0, 0, "C1: SALUDABLE", "CPI ≥ 1.0 | SPI ≥ 1.0", "En plazo y presupuesto", (240, 253, 244), (16, 185, 129), (6, 95, 70), False),
            (1, 0, "C2: ALERTA PLAZO", "CPI ≥ 1.0 | SPI < 1.0", "En coste, con retraso", (255, 251, 235), (245, 158, 11), (146, 64, 14), False),
            (0, 1, "C3: ALERTA COSTE", "CPI < 1.0 | SPI ≥ 1.0", "En plazo, con sobrecoste", (255, 251, 235), (245, 158, 11), (146, 64, 14), False),
            (1, 1, "C4: CRISIS [ACTIVA]", "CPI 0.86 | SPI 0.86", "Sobrecoste + Retraso", (254, 226, 226), (220, 38, 38), (153, 27, 27), True),
        ]
        if lang == "ES"
        else [
            (0, 0, "Q1: HEALTHY ZONE", "CPI ≥ 1.0 | SPI ≥ 1.0", "On time & on budget", (240, 253, 244), (16, 185, 129), (6, 95, 70), False),
            (1, 0, "Q2: SCHEDULE ALERT", "CPI ≥ 1.0 | SPI < 1.0", "Under budget, delayed", (255, 251, 235), (245, 158, 11), (146, 64, 14), False),
            (0, 1, "Q3: COST ALERT", "CPI < 1.0 | SPI ≥ 1.0", "On schedule, overrun", (255, 251, 235), (245, 158, 11), (146, 64, 14), False),
            (1, 1, "Q4: CRISIS [ACTIVE]", "CPI 0.86 | SPI 0.86", "Overrun + Delay", (254, 226, 226), (220, 38, 38), (153, 27, 27), True),
        ]
    )
    for col_i, row_i, qt, qr, qd, qbg, qbdr, qfg, active_q in quads:
        bx = mx + 10 + col_i * (qw_box + 8)
        by = qy0 + row_i * (qh_box + 8)
        d.rounded_rectangle([(bx, by), (bx + qw_box, by + qh_box)], radius=6, fill=qbg, outline=qbdr, width=2 if active_q else 1)
        d.text((bx + 10, by + 10), qt, fill=qfg, font=get_font("segoeuib.ttf", 10))
        d.text((bx + 10, by + 30), qr, fill=qfg, font=f_monob)
        d.text((bx + 10, by + 50), qd, fill=(71, 85, 105), font=f_r10)

    # Middle Right: Native Excel S-Curve Chart (M01..M12)
    gx, gy, gw, gh = 418, 210, win_w - 14 - 418, 392
    d.rounded_rectangle([(gx, gy), (gx + gw, gy + gh)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(gx, gy), (gx + gw, gy + 30)], radius=8, fill=(30, 41, 59))
    d.rectangle([(gx, gy + 16), (gx + gw, gy + 30)], fill=(30, 41, 59))
    g_title = "CURVA S EJECUTIVA: PV vs EV vs AC & PROYECCIÓN EAC" if lang == "ES" else "EXECUTIVE S-CURVE: PV vs EV vs AC & EAC FORECAST"
    d.text((gx + 14, gy + 8), g_title, fill=(255, 255, 255), font=f_b11)

    # Legend strip inside chart box
    leg_y = gy + 42
    legs = (
        [("Σ PV Plan", (37, 99, 235)), ("Σ EV Ganado", (16, 185, 129)), ("Σ AC Coste", (220, 38, 38)), ("EAC Proy.", (124, 58, 237))]
        if lang == "ES"
        else [("Σ PV Planned", (37, 99, 235)), ("Σ EV Earned", (16, 185, 129)), ("Σ AC Actual", (220, 38, 38)), ("EAC Forecast", (124, 58, 237))]
    )
    lx = gx + 60
    for l_t, l_c in legs:
        d.rectangle([(lx, leg_y + 3), (lx + 12, leg_y + 7)], fill=l_c)
        d.text((lx + 16, leg_y), l_t, fill=(51, 65, 85), font=f_r10)
        lx += 16 + text_w(d, l_t, f_r10) + 18

    ax_x0, ax_x1 = gx + 64, gx + gw - 22
    ax_y0, ax_y1 = gy + 70, gy + gh - 50
    y_max = 1500.0

    def map_x(idx):
        return ax_x0 + (idx / 11.0) * (ax_x1 - ax_x0)

    def map_y(val_k):
        return ax_y1 - (val_k / y_max) * (ax_y1 - ax_y0)

    for tick_k in [0, 300, 600, 900, 1200, 1500]:
        yy = int(map_y(tick_k))
        d.line([(ax_x0, yy), (ax_x1, yy)], fill=(226, 232, 240), width=1)
        lbl_y = f"{tick_k:,}k€".replace(",", ".") if lang == "ES" else f"${tick_k:,}k"
        if tick_k == 0:
            lbl_y = "0 €" if lang == "ES" else "$0"
        d.text((gx + 10, yy - 6), lbl_y, fill=(100, 116, 139), font=get_font("consola.ttf", 9))

    d.line([(ax_x0, ax_y1), (ax_x1, ax_y1)], fill=(71, 85, 105), width=2)
    d.line([(ax_x0, ax_y0), (ax_x0, ax_y1)], fill=(71, 85, 105), width=2)

    months = [f"M{m:02d}" for m in range(1, 13)]
    for i, mlbl in enumerate(months):
        tx = int(map_x(i))
        d.line([(tx, ax_y1), (tx, ax_y1 + 4)], fill=(100, 116, 139), width=1)
        d.text((tx - 9, ax_y1 + 7), mlbl, fill=(71, 85, 105), font=get_font("consola.ttf", 9))
    ax_lbl = "Evolución Mensual del Proyecto (M01 – M12)" if lang == "ES" else "Monthly Project Timeline (M01 – M12)"
    d.text((ax_x0 + (ax_x1 - ax_x0 - text_w(d, ax_lbl, f_r10)) // 2, ax_y1 + 23), ax_lbl, fill=(51, 65, 85), font=f_r10)

    pv_k = [60, 140, 240, 350, 470, 600, 730, 850, 960, 1060, 1140, 1200]
    ev_k = [58, 133, 225, 320, 418, 516]
    ac_k = [62, 146, 254, 368, 484, 600]
    eac_k = [600, 733, 865, 998, 1130, 1263, 1395.3]

    pv_pts = [(map_x(i), map_y(v)) for i, v in enumerate(pv_k)]
    ev_pts = [(map_x(i), map_y(v)) for i, v in enumerate(ev_k)]
    ac_pts = [(map_x(i), map_y(v)) for i, v in enumerate(ac_k)]
    eac_pts = [(map_x(5 + i), map_y(v)) for i, v in enumerate(eac_k)]

    # Cutoff line M06
    cx6 = map_x(5)
    d.line([(cx6, ax_y0), (cx6, ax_y1)], fill=(148, 163, 184), width=1)

    for pts_arr, col, w_line in [(pv_pts, (37, 99, 235), 2), (eac_pts, (124, 58, 237), 2), (ac_pts, (220, 38, 38), 3), (ev_pts, (16, 185, 129), 3)]:
        for i in range(len(pts_arr) - 1):
            d.line([pts_arr[i], pts_arr[i + 1]], fill=col, width=w_line)
        for px, py in pts_arr:
            d.ellipse([(px - 3, py - 3), (px + 3, py + 3)], fill=col)

    # Annotations inside chart
    d.rounded_rectangle([(ax_x1 - 118, int(map_y(1440)) - 22), (ax_x1 - 4, int(map_y(1440)))], radius=4, fill=(245, 243, 255), outline=(124, 58, 237))
    eac_lbl = "EAC₁: 1.395k€" if lang == "ES" else "EAC₁: $1,395k"
    d.text((ax_x1 - 111, int(map_y(1440)) - 18), eac_lbl, fill=(109, 40, 217), font=get_font("segoeuib.ttf", 10))

    d.rounded_rectangle([(int(cx6) + 8, int(map_y(490))), (int(cx6) + 106, int(map_y(490)) + 20)], radius=4, fill=(254, 226, 226), outline=(220, 38, 38))
    d.text((int(cx6) + 14, int(map_y(490)) + 3), "CV: -84k€" if lang == "ES" else "CV: -$84k", fill=(185, 28, 28), font=get_font("segoeuib.ttf", 10))

    # Bottom Section: Tab 2 & 4 WBS & Recovery Plan Preview
    cx, cy, cw_tbl, ch_tbl = 14, 614, win_w - 28, 256
    d.rounded_rectangle([(cx, cy), (cx + cw_tbl, cy + ch_tbl)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(cx, cy), (cx + cw_tbl, cy + 30)], radius=8, fill=(15, 23, 42))
    d.rectangle([(cx, cy + 16), (cx + cw_tbl, cy + 30)], fill=(15, 23, 42))
    tbl_t = (
        "PESTAÑAS 2 & 4 · CONTROL WBS CON DESVIACIÓN CRÍTICA & PLAN DE RECUPERACIÓN"
        if lang == "ES"
        else "TABS 2 & 4 · CRITICAL WBS DELIVERABLES & BOARD RECOVERY PLAN"
    )
    d.text((cx + 14, cy + 8), tbl_t, fill=(255, 255, 255), font=f_b11)

    cols = (
        ["WBS", "Paquete de Trabajo Crítico", "BAC", "EV", "AC", "CPI", "Palanca C-Level"]
        if lang == "ES"
        else ["WBS", "Critical WBS Deliverable", "BAC", "EV", "AC", "CPI", "C-Level Lever"]
    )
    col_x = [cx + 14, cx + 68, cx + 360, cx + 448, cx + 536, cx + 622, cx + 700]
    hy = cy + 36
    d.rectangle([(cx + 8, hy), (cx + cw_tbl - 8, hy + 26)], fill=(226, 232, 240))
    for i, cname in enumerate(cols):
        d.text((col_x[i], hy + 6), cname, fill=(15, 23, 42), font=get_font("segoeuib.ttf", 10))

    wbs_rows = (
        [
            ("2.1", "Motor Transaccional Conciliación", "85.000 €", "72.250 €", "98.000 €", "0.74", "Crashing (+0.04 CPI)", False),
            ("2.3", "Módulo Pagos & Pasarelas", "75.000 €", "52.500 €", "82.000 €", "0.64", "Fast-Tracking (+0.06 SPI)", False),
            ("3.1", "Conector Bidireccional ERP SAP", "80.000 €", "32.000 €", "28.000 €", "1.14", "Precio Cerrado (+0.05 CPI)", True),
            ("3.2", "Integración Pasarelas SWIFT", "60.000 €", "24.000 €", "20.000 €", "1.20", "Escalado Ejecutivo (+0.04 SPI)", True),
            ("3.3", "Conector CRM Salesforce", "40.000 €", "10.000 €", "10.000 €", "1.00", "Descope Q1 (+0.03 CPI)", True),
            ("1.1", "Arquitectura Cloud & IaC", "40.000 €", "40.000 €", "41.000 €", "0.98", "Completado 100% (OK)", True),
        ]
        if lang == "ES"
        else [
            ("2.1", "Core Reconciliation Engine", "$85,000", "$72,250", "$98,000", "0.74", "Crashing (+0.04 CPI)", False),
            ("2.3", "Payment Processing Module", "$75,000", "$52,500", "$82,000", "0.64", "Fast-Tracking (+0.06 SPI)", False),
            ("3.1", "Core ERP Connector (SAP)", "$80,000", "$32,000", "$28,000", "1.14", "Fixed-Fee Cap (+0.05 CPI)", True),
            ("3.2", "Banking SWIFT Gateways", "$60,000", "$24,000", "$20,000", "1.20", "Board Escalation (+0.04 SPI)", True),
            ("3.3", "CRM Salesforce Sync", "$40,000", "$10,000", "$10,000", "1.00", "Deferred Descope (+0.03 CPI)", True),
            ("1.1", "Cloud Architecture & IaC", "$40,000", "$40,000", "$41,000", "0.98", "Completed 100% (OK)", True),
        ]
    )
    ry_c = hy + 28
    for idx, (wbs, tname, bac, ev, ac, cpi, dec, ok) in enumerate(wbs_rows):
        bg_c = (248, 250, 252) if idx % 2 == 0 else (255, 255, 255)
        d.rectangle([(cx + 8, ry_c), (cx + cw_tbl - 8, ry_c + 29)], fill=bg_c, outline=(241, 245, 249))
        vals = [wbs, tname, bac, ev, ac, cpi]
        for i, v in enumerate(vals):
            d.text((col_x[i], ry_c + 7), v, fill=(30, 41, 59), font=f_mono if i != 1 else f_r11)
        pill_bg = (220, 252, 231) if ok else (254, 226, 226)
        pill_fg = (5, 150, 105) if ok else (185, 28, 28)
        d.rounded_rectangle([(col_x[6] - 4, ry_c + 4), (cx + cw_tbl - 14, ry_c + 25)], radius=4, fill=pill_bg)
        d.text((col_x[6] + 2, ry_c + 7), dec, fill=pill_fg, font=get_font("segoeuib.ttf", 10))
        ry_c += 30

    # Excel Bottom Worksheet Tabs
    tabs = (
        ["Dashboard Ejecutivo EVM", "Control WBS & Entregables", "Serie Temporal & Proyecciones", "Plan de Acción & Recuperación"]
        if lang == "ES"
        else ["Executive EVM Dashboard", "WBS & Deliverables Tracking", "Time Series & EAC Forecasting", "Action & Recovery Plan"]
    )
    ty = win_h - 40
    d.rectangle([(1, ty - 4), (win_w - 2, win_h - 2)], fill=(226, 232, 240))
    tx = 16
    for i, tb in enumerate(tabs):
        active = i == 0
        tw = text_w(d, tb, f_b11) + 22
        bg_t = (255, 255, 255) if active else (241, 245, 249)
        fg_t = (5, 150, 105) if active else (71, 85, 105)
        d.rounded_rectangle([(tx, ty), (tx + tw, ty + 28)], radius=5, fill=bg_t, outline=(148, 163, 184))
        if active:
            d.rectangle([(tx + 4, ty + 24), (tx + tw - 4, ty + 27)], fill=(5, 150, 105))
        d.text((tx + 11, ty + 6), tb, fill=fg_t, font=f_b11 if active else f_r11)
        tx += tw + 8

    return win


def draw_pdf_window(lang: str) -> Image.Image:
    win_w, win_h = 630, 494
    pdf_file = (
        PKG_DIR / "[ES]_Cuadro_EVM_Valor_Ganado" / "Guia_Metodologica_EVM_ES.pdf"
        if lang == "ES"
        else PKG_DIR / "[EN]_Earned_Value_Management_EVM" / "Methodology_Guide_EVM_EN.pdf"
    )
    title = f"{pdf_file.name}"
    badge = "GUÍA METODOLÓGICA · 5 PÁGINAS" if lang == "ES" else "METHODOLOGY GUIDE · 5 PAGES"
    win = make_window_chrome(win_w, win_h, title, badge, badge_bg=(220, 38, 38), body_bg=(30, 41, 59))

    pages = render_pdf_pages(pdf_file, page_indices=(0, 1), target_h=416)
    px = 24
    for p_img in pages:
        paste_with_shadow(win, p_img, (px, 56))
        px += p_img.width + 20
    return win


def draw_pptx_window(lang: str) -> Image.Image:
    win_w, win_h = 630, 410
    pptx_file = (
        PKG_DIR / "[ES]_Cuadro_EVM_Valor_Ganado" / "Presentacion_EVM_CLevel_ES.pptx"
        if lang == "ES"
        else PKG_DIR / "[EN]_Earned_Value_Management_EVM" / "Deck_EVM_CLevel_EN.pptx"
    )
    badge = "DECK EJECUTIVO 16:9 · SLIDE 2" if lang == "ES" else "C-LEVEL 16:9 DECK · SLIDE 2"
    win = make_window_chrome(win_w, win_h, pptx_file.name, badge, badge_bg=(217, 119, 6), body_bg=(15, 23, 42))

    slide_img = export_pptx_slide_com(pptx_file, slide_num=2)
    if slide_img is not None:
        target_w = win_w - 28
        target_h = int(slide_img.height * (target_w / slide_img.width))
        if target_h > win_h - 56:
            target_h = win_h - 56
            target_w = int(slide_img.width * (target_h / slide_img.height))
        slide_img = slide_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        sx = (win_w - target_w) // 2
        sy = 46 + ((win_h - 54 - target_h) // 2)
        paste_with_shadow(win, slide_img, (sx, sy))
    else:
        d = ImageDraw.Draw(win)
        d.text((40, 180), f"{pptx_file.name} (16:9 Slide Deck)", fill=(226, 232, 240), font=get_font("segoeuib.ttf", 18))
    return win


def build_preview(lang: str):
    canvas = Image.new("RGBA", (W, H), (15, 23, 42, 255))
    d = ImageDraw.Draw(canvas)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=(23, 35, 58, 255), width=1)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=(23, 35, 58, 255), width=1)

    win_excel = draw_excel_dashboard_window(lang)
    win_pdf = draw_pdf_window(lang)
    win_pptx = draw_pptx_window(lang)

    paste_with_shadow(canvas, win_excel, (26, 28))
    paste_with_shadow(canvas, win_pdf, (944, 28))
    paste_with_shadow(canvas, win_pptx, (944, 542))

    final_img = canvas.convert("RGB")
    if lang == "ES":
        outs = [
            ROOT_DIR / "static" / "images" / "recursos" / "evm-preview-es.png",
            ROOT_DIR / "content" / "es" / "posts" / "cuadro-mando-evm-valor-ganado" / "preview-pack.png",
        ]
    else:
        outs = [
            ROOT_DIR / "static" / "images" / "recursos" / "evm-preview-en.png",
            ROOT_DIR / "content" / "en" / "posts" / "earned-value-management-evm-dashboard" / "preview-pack.png",
        ]
    for o in outs:
        o.parent.mkdir(parents=True, exist_ok=True)
        final_img.save(o, format="PNG", optimize=True)
        print(f" -> Preview guardada: {o}")


def main():
    print("[1/2] Generando preview compuesta EVM en Español...")
    build_preview("ES")
    print("[2/2] Generando preview compuesta EVM en Inglés...")
    build_preview("EN")
    print("Previews EVM generadas correctamente.")


if __name__ == "__main__":
    main()
