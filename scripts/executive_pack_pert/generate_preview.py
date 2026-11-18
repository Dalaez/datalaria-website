#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes compuestas `preview-pack.png` (1600 x 980 px) a partir de los
activos reales generados en `packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/`:
- Excel Dashboard: métricas reales de `Estimacion_PERT_Estocastica_ES.xlsx` / `Stochastic_PERT_Estimation_EN.xlsx`
  (μ=192.5d, σ=10.14d, Td=188.0d, Z=-0.44, P=32.9%, Buffer P90=+13.0d y tabla Crashing).
- Guía PDF: renderizado real de páginas 1 y 2 vía `pypdfium2`.
- Deck PPTX 16:9: exportación real de Slide 2 vía PowerPoint COM (con fallback seguro).

Salidas:
- static/images/recursos/pert-preview-es.png
- content/es/posts/estimacion-pert-3-puntos/preview-pack.png
- static/images/recursos/pert-preview-en.png
- content/en/posts/stochastic-3-point-pert-estimation/preview-pack.png
"""

import math
import os
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PKG_DIR = ROOT_DIR / "packages" / "Suite_03_Control_Operativo" / "03_Estimacion_PERT_3_Puntos"

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
    # Body background
    d.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=12, fill=body_bg + (255,), outline=(51, 65, 85, 255), width=2)
    # Top title bar
    d.rounded_rectangle([(0, 0), (width - 1, 38)], radius=12, fill=(15, 23, 42, 255))
    d.rectangle([(0, 22), (width - 1, 38)], fill=(15, 23, 42, 255))
    d.line([(0, 38), (width - 1, 38)], fill=(51, 65, 85, 255), width=1)
    # Traffic lights
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


def render_pdf_pages(pdf_path: Path, page_indices=(0, 1), target_h=415) -> list[Image.Image]:
    doc = pdfium.PdfDocument(str(pdf_path))
    imgs = []
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
        "Estimacion_PERT_Estocastica_ES.xlsx — Excel 365 & Google Sheets"
        if lang == "ES"
        else "Stochastic_PERT_Estimation_EN.xlsx — Excel 365 & Google Sheets"
    )
    badge = "MODELO PROTEGIDO · 4 PESTAÑAS" if lang == "ES" else "PROTECTED ENGINE · 4 TABS"
    win = make_window_chrome(win_w, win_h, title, badge, badge_bg=(5, 150, 105), body_bg=(248, 250, 252))
    d = ImageDraw.Draw(win)

    f_h1 = get_font("segoeuib.ttf", 16)
    f_sub = get_font("segoeui.ttf", 11)
    f_b12 = get_font("segoeuib.ttf", 12)
    f_b11 = get_font("segoeuib.ttf", 11)
    f_r11 = get_font("segoeui.ttf", 11)
    f_r10 = get_font("segoeui.ttf", 10)
    f_kpi = get_font("segoeuib.ttf", 22)
    f_mono = get_font("consola.ttf", 11)
    f_monob = get_font("consolab.ttf", 11)

    # Sheet header banner
    d.rounded_rectangle([(14, 48), (win_w - 14, 104)], radius=8, fill=(15, 23, 42))
    h_txt = (
        "DASHBOARD EJECUTIVO: ESTIMACIÓN PERT & RIESGO DE CRONOGRAMA"
        if lang == "ES"
        else "EXECUTIVE DASHBOARD: PERT ESTIMATION & SCHEDULE RISK"
    )
    s_txt = (
        "Motor Estocástico Beta + Camino Crítico (CLT) · 25 Paquetes WBS (16 Críticos)"
        if lang == "ES"
        else "Stochastic Beta Engine + Critical Path (CLT) · 25 WBS Packages (16 Critical)"
    )
    d.text((28, 56), h_txt, fill=(255, 255, 255), font=f_h1)
    d.text((28, 80), s_txt, fill=(148, 163, 184), font=f_sub)

    # 4 Top KPI Cards
    kpis_es = [
        ("DURACIÓN ESPERADA (μ)", "192.5 días", "Suma crítica CLT", (239, 246, 255), (37, 99, 235), (30, 58, 138)),
        ("DESVIACIÓN GLOBAL (σ)", "10.14 días", "σ² = 102.81 días²", (248, 250, 252), (100, 116, 139), (15, 23, 42)),
        ("INTERVALO 95% (μ±1.96σ)", "172.6 – 212.4", "Ventana estadística", (248, 250, 252), (2, 132, 199), (15, 23, 42)),
        ("COLCHÓN P90 CONSEJO", "+13.0 días", "P90 = 205.5 días", (240, 253, 244), (5, 150, 105), (5, 150, 105)),
    ]
    kpis_en = [
        ("EXPECTED DURATION (μ)", "192.5 days", "CLT Critical Sum", (239, 246, 255), (37, 99, 235), (30, 58, 138)),
        ("GLOBAL STD DEV (σ)", "10.14 days", "σ² = 102.81 days²", (248, 250, 252), (100, 116, 139), (15, 23, 42)),
        ("95% CONFIDENCE (μ±1.96σ)", "172.6 – 212.4", "Statistical Window", (248, 250, 252), (2, 132, 199), (15, 23, 42)),
        ("BOARD P90 BUFFER", "+13.0 days", "P90 = 205.5 days", (240, 253, 244), (5, 150, 105), (5, 150, 105)),
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

    # Middle Left: Target Date Calculator + P50-P99 Table
    mx, my, mw, mh = 14, 210, 392, 392
    d.rounded_rectangle([(mx, my), (mx + mw, my + mh)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(mx, my), (mx + mw, my + 30)], radius=8, fill=(30, 41, 59))
    d.rectangle([(mx, my + 16), (mx + mw, my + 30)], fill=(30, 41, 59))
    calc_t = "CALCULADORA DE FECHA COMPROMISO" if lang == "ES" else "TARGET DEADLINE CALCULATOR"
    d.text((mx + 12, my + 8), calc_t, fill=(255, 255, 255), font=f_b11)

    rows_calc = (
        [
            ("Fecha Límite (Td):", "188.0 d", (239, 246, 255), (37, 99, 235)),
            ("Z-Score [(Td-μ)/σ]:", "-0.44 σ", (248, 250, 252), (15, 23, 42)),
            ("Probabilidad P(T≤Td):", "32.9%", (254, 242, 242), (220, 38, 38)),
            ("Diagnóstico:", "INVIABLE SIN BUFFER", (254, 242, 242), (185, 28, 28)),
            ("Días extra para P90:", "+17.5 días", (240, 253, 244), (5, 150, 105)),
        ]
        if lang == "ES"
        else [
            ("Target Deadline (Td):", "188.0 d", (239, 246, 255), (37, 99, 235)),
            ("Z-Score [(Td-μ)/σ]:", "-0.44 σ", (248, 250, 252), (15, 23, 42)),
            ("Success Prob P(T≤Td):", "32.9%", (254, 242, 242), (220, 38, 38)),
            ("Verdict:", "UNFEASIBLE NO BUFFER", (254, 242, 242), (185, 28, 28)),
            ("Extra Days for P90:", "+17.5 days", (240, 253, 244), (5, 150, 105)),
        ]
    )
    ry = my + 38
    for lbl, val, rbg, vcol in rows_calc:
        d.rectangle([(mx + 10, ry), (mx + mw - 10, ry + 26)], fill=rbg, outline=(226, 232, 240))
        d.text((mx + 16, ry + 6), lbl, fill=(51, 65, 85), font=f_r11)
        vw = text_w(d, val, f_monob)
        d.text((mx + mw - 18 - vw, ry + 6), val, fill=vcol, font=f_monob)
        ry += 28

    # Percentile Confidence Table inside middle left
    py0 = ry + 10
    p_hdr = "ESCENARIOS DE CERTIDUMBRE (NORMINV)" if lang == "ES" else "CONFIDENCE SCENARIOS (NORMINV)"
    d.rectangle([(mx + 10, py0), (mx + mw - 10, py0 + 24)], fill=(15, 23, 42))
    d.text((mx + 16, py0 + 5), p_hdr, fill=(255, 255, 255), font=get_font("segoeuib.ttf", 10))
    py0 += 26
    pct_rows = [
        ("P50", "0.00", "192.5 d", "+0.0 d"),
        ("P70", "+0.52", "197.8 d", "+5.3 d"),
        ("P80", "+0.84", "201.0 d", "+8.5 d"),
        ("P90", "+1.28", "205.5 d", "+13.0 d"),
        ("P95", "+1.64", "209.2 d", "+16.7 d"),
        ("P99", "+2.33", "216.1 d", "+23.6 d"),
    ]
    for idx, (pc, zv, dv, bv) in enumerate(pct_rows):
        is_p90 = pc == "P90"
        bg_r = (220, 252, 231) if is_p90 else ((248, 250, 252) if idx % 2 == 0 else (255, 255, 255))
        tc = (5, 150, 105) if is_p90 else (30, 41, 59)
        f_use = f_monob if is_p90 else f_mono
        d.rectangle([(mx + 10, py0), (mx + mw - 10, py0 + 22)], fill=bg_r, outline=(226, 232, 240))
        d.text((mx + 18, py0 + 4), pc, fill=tc, font=f_use)
        d.text((mx + 92, py0 + 4), f"Z={zv}", fill=(100, 116, 139), font=f_use)
        d.text((mx + 205, py0 + 4), dv, fill=tc, font=f_use)
        d.text((mx + 305, py0 + 4), f"Buf {bv}", fill=tc, font=f_use)
        py0 += 23

    # Middle Right: Bell Curve Plot N(192.5, 10.14)
    gx, gy, gw, gh = 418, 210, win_w - 14 - 418, 392
    d.rounded_rectangle([(gx, gy), (gx + gw, gy + gh)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(gx, gy), (gx + gw, gy + 30)], radius=8, fill=(30, 41, 59))
    d.rectangle([(gx, gy + 16), (gx + gw, gy + 30)], fill=(30, 41, 59))
    g_title = "DISTRIBUCIÓN NORMAL DEL PROYECTO N(192.5, 10.14²)" if lang == "ES" else "PROJECT GAUSSIAN DISTRIBUTION N(192.5, 10.14²)"
    d.text((gx + 14, gy + 8), g_title, fill=(255, 255, 255), font=f_b11)

    ax_x0, ax_x1 = gx + 48, gx + gw - 24
    ax_y0, ax_y1 = gy + 55, gy + gh - 56
    # Gridlines
    for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
        yy = int(ax_y1 - (ax_y1 - ax_y0) * frac)
        d.line([(ax_x0, yy), (ax_x1, yy)], fill=(226, 232, 240), width=1)
        lbl_y = f"{0.04 * frac:.3f}"
        d.text((gx + 8, yy - 6), lbl_y, fill=(100, 116, 139), font=get_font("consola.ttf", 9))

    mu, sigma = 192.5, 10.14
    x_min, x_max = 157.0, 228.0

    def map_x(val):
        return ax_x0 + (val - x_min) / (x_max - x_min) * (ax_x1 - ax_x0)

    def pdf(val):
        return math.exp(-0.5 * ((val - mu) / sigma) ** 2)

    pts = []
    for s in range(140):
        xv = x_min + (x_max - x_min) * (s / 139)
        px = map_x(xv)
        py = ax_y1 - pdf(xv) * (ax_y1 - ax_y0 - 12)
        pts.append((px, py))

    px_td = map_x(188.0)
    px_mu = map_x(192.5)
    px_p90 = map_x(205.5)

    # Shaded regions
    poly_td = [(ax_x0, ax_y1)] + [p for p in pts if p[0] <= px_td] + [(px_td, ax_y1)]
    d.polygon(poly_td, fill=(254, 202, 202))
    poly_mid = [(px_td, ax_y1)] + [p for p in pts if px_td <= p[0] <= px_p90] + [(px_p90, ax_y1)]
    d.polygon(poly_mid, fill=(191, 219, 254))
    poly_tail = [(px_p90, ax_y1)] + [p for p in pts if p[0] >= px_p90] + [(ax_x1, ax_y1)]
    d.polygon(poly_tail, fill=(209, 250, 229))

    # Main Curve line
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(37, 99, 235), width=3)

    # Axes & ticks
    d.line([(ax_x0, ax_y1), (ax_x1, ax_y1)], fill=(71, 85, 105), width=2)
    d.line([(ax_x0, ax_y0), (ax_x0, ax_y1)], fill=(71, 85, 105), width=2)
    for xv in [160, 170, 180, 190, 200, 210, 220]:
        tx = int(map_x(xv))
        d.line([(tx, ax_y1), (tx, ax_y1 + 5)], fill=(71, 85, 105), width=1)
        d.text((tx - 12, ax_y1 + 9), f"{xv}d", fill=(71, 85, 105), font=get_font("consola.ttf", 10))
    ax_lbl = "Duración Total del Proyecto (Días Hábiles)" if lang == "ES" else "Total Project Duration (Working Days)"
    ax_lw = text_w(d, ax_lbl, f_r10)
    d.text((ax_x0 + (ax_x1 - ax_x0 - ax_lw) // 2, ax_y1 + 26), ax_lbl, fill=(51, 65, 85), font=f_r10)

    # Threshold vertical lines & non-overlapping pills
    d.line([(px_td, ax_y0 + 18), (px_td, ax_y1)], fill=(220, 38, 38), width=2)
    td_lbl = "Td=188d (32.9%)"
    td_lw = text_w(d, td_lbl, get_font("segoeuib.ttf", 10))
    d.rounded_rectangle([(px_td - td_lw - 18, ax_y0 + 18), (px_td - 4, ax_y0 + 38)], radius=4, fill=(254, 226, 226), outline=(220, 38, 38))
    d.text((px_td - td_lw - 11, ax_y0 + 21), td_lbl, fill=(185, 28, 28), font=get_font("segoeuib.ttf", 10))

    d.line([(px_mu, ax_y0), (px_mu, ax_y1)], fill=(100, 116, 139), width=1)
    d.text((px_mu - 24, ax_y0 - 15), "μ=192.5d", fill=(51, 65, 85), font=f_monob)

    d.line([(px_p90, ax_y0 + 30), (px_p90, ax_y1)], fill=(5, 150, 105), width=2)
    p90_lbl = "P90=205.5d"
    p90_lw = text_w(d, p90_lbl, get_font("segoeuib.ttf", 10))
    d.rounded_rectangle([(px_p90 + 5, ax_y0 + 30), (px_p90 + p90_lw + 18, ax_y0 + 50)], radius=4, fill=(209, 250, 229), outline=(5, 150, 105))
    d.text((px_p90 + 11, ax_y0 + 33), p90_lbl, fill=(4, 120, 87), font=get_font("segoeuib.ttf", 10))

    # Bottom Section: Tab 4 Crashing Matrix Preview
    cx, cy, cw_tbl, ch_tbl = 14, 614, win_w - 28, 256
    d.rounded_rectangle([(cx, cy), (cx + cw_tbl, cy + ch_tbl)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(cx, cy), (cx + cw_tbl, cy + 30)], radius=8, fill=(15, 23, 42))
    d.rectangle([(cx, cy + 16), (cx + cw_tbl, cy + 30)], fill=(15, 23, 42))
    crash_t = (
        "PESTAÑA 4 · MATRIZ DE ACELERACIÓN (CRASHING) & COSTE MARGINAL"
        if lang == "ES"
        else "TAB 4 · SCHEDULE CRASHING MATRIX & MARGINAL COST RANKING"
    )
    d.text((cx + 14, cy + 8), crash_t, fill=(255, 255, 255), font=f_b11)

    cols = (
        ["WBS", "Tarea Crítica", "Normal", "Crash", "Reducción", "Sobrecolchón", "Coste / Día", "Decisión Comité"]
        if lang == "ES"
        else ["WBS", "Critical Task", "Normal", "Crash", "Max Red.", "Delta Cost", "Cost / Day", "Board Decision"]
    )
    col_x = [cx + 14, cx + 68, cx + 330, cx + 405, cx + 478, cx + 560, cx + 662, cx + 755]
    hy = cy + 36
    d.rectangle([(cx + 8, hy), (cx + cw_tbl - 8, hy + 26)], fill=(226, 232, 240))
    for i, cname in enumerate(cols):
        d.text((col_x[i], hy + 6), cname, fill=(15, 23, 42), font=get_font("segoeuib.ttf", 10))

    crash_rows = (
        [
            ("1.1", "Arquitectura Cloud & Microservicios", "11.0 d", "7.0 d", "-4.0 d", "6.000 €", "1.500 €/d", "Aprobado (Fase 1)", True),
            ("1.3", "Especificación de APIs OpenAPI", "9.0 d", "6.0 d", "-3.0 d", "4.500 €", "1.500 €/d", "Aprobado (Fase 1)", True),
            ("4.2", "Pruebas de Carga & Estrés", "11.0 d", "7.0 d", "-4.0 d", "7.000 €", "1.750 €/d", "Aprobado (Fase 4)", True),
            ("2.4", "Motor de Reglas de Negocio", "14.7 d", "10.0 d", "-4.7 d", "9.500 €", "2.021 €/d", "En Reserva (Fase 2)", False),
            ("3.2", "Integración Pasarelas Bancarias", "15.0 d", "10.0 d", "-5.0 d", "12.500 €", "2.500 €/d", "Aprobado (Fase 3)", True),
            ("2.1", "Motor Transaccional Conciliación", "19.3 d", "13.0 d", "-6.3 d", "17.000 €", "2.698 €/d", "Aprobado (Fase 2)", True),
        ]
        if lang == "ES"
        else [
            ("1.1", "Cloud Microservices Architecture", "11.0 d", "7.0 d", "-4.0 d", "$6,000", "$1,500/d", "Approved (Phase 1)", True),
            ("1.3", "OpenAPI API Specification", "9.0 d", "6.0 d", "-3.0 d", "$4,500", "$1,500/d", "Approved (Phase 1)", True),
            ("4.2", "Stress & Load Testing (10k TPS)", "11.0 d", "7.0 d", "-4.0 d", "$7,000", "$1,750/d", "Approved (Phase 4)", True),
            ("2.4", "Business Rules Engine", "14.7 d", "10.0 d", "-4.7 d", "$9,500", "$2,021/d", "On Hold (Phase 2)", False),
            ("3.2", "Acquiring Banking Gateways", "15.0 d", "10.0 d", "-5.0 d", "$12,500", "$2,500/d", "Approved (Phase 3)", True),
            ("2.1", "Core Reconciliation Engine", "19.3 d", "13.0 d", "-6.3 d", "$17,000", "$2,698/d", "Approved (Phase 2)", True),
        ]
    )
    ry_c = hy + 28
    for idx, (wbs, tname, dn, dc, red, dcst, cpd, dec, ok) in enumerate(crash_rows):
        bg_c = (248, 250, 252) if idx % 2 == 0 else (255, 255, 255)
        d.rectangle([(cx + 8, ry_c), (cx + cw_tbl - 8, ry_c + 29)], fill=bg_c, outline=(241, 245, 249))
        vals = [wbs, tname, dn, dc, red, dcst, cpd]
        for i, v in enumerate(vals):
            d.text((col_x[i], ry_c + 7), v, fill=(30, 41, 59), font=f_mono if i != 1 else f_r11)
        pill_bg = (220, 252, 231) if ok else (254, 243, 199)
        pill_fg = (5, 150, 105) if ok else (180, 83, 9)
        d.rounded_rectangle([(col_x[7] - 4, ry_c + 4), (cx + cw_tbl - 14, ry_c + 25)], radius=4, fill=pill_bg)
        d.text((col_x[7] + 2, ry_c + 7), dec, fill=pill_fg, font=get_font("segoeuib.ttf", 10))
        ry_c += 30

    # Excel Bottom Worksheet Tabs
    tabs = (
        ["Dashboard Ejecutivo", "Estimación WBS 3 Puntos", "Camino Crítico & Análisis Z", "Buffers & Plan de Aceleración"]
        if lang == "ES"
        else ["Executive Dashboard", "WBS 3-Point Estimation", "Critical Path & Z-Score", "Schedule Buffers & Crashing"]
    )
    ty = win_h - 40
    d.rectangle([(1, ty - 4), (win_w - 2, win_h - 2)], fill=(226, 232, 240))
    tx = 16
    for i, tb in enumerate(tabs):
        active = i == 0
        tw = text_w(d, tb, f_b11) + 26
        bg_t = (255, 255, 255) if active else (241, 245, 249)
        fg_t = (5, 150, 105) if active else (71, 85, 105)
        d.rounded_rectangle([(tx, ty), (tx + tw, ty + 28)], radius=5, fill=bg_t, outline=(148, 163, 184))
        if active:
            d.rectangle([(tx + 4, ty + 24), (tx + tw - 4, ty + 27)], fill=(5, 150, 105))
        d.text((tx + 13, ty + 6), tb, fill=fg_t, font=f_b11 if active else f_r11)
        tx += tw + 8

    return win


def draw_pdf_window(lang: str) -> Image.Image:
    win_w, win_h = 630, 494
    pdf_file = (
        PKG_DIR / "[ES]_Estimacion_PERT_3_Puntos" / "Guia_Metodologica_PERT_ES.pdf"
        if lang == "ES"
        else PKG_DIR / "[EN]_3Point_PERT_Estimation" / "Methodology_Guide_PERT_EN.pdf"
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
        PKG_DIR / "[ES]_Estimacion_PERT_3_Puntos" / "Presentacion_PERT_CLevel_ES.pptx"
        if lang == "ES"
        else PKG_DIR / "[EN]_3Point_PERT_Estimation" / "Deck_PERT_CLevel_EN.pptx"
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
    # Subtle gradient/grid backdrop
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
            ROOT_DIR / "static" / "images" / "recursos" / "pert-preview-es.png",
            ROOT_DIR / "content" / "es" / "posts" / "estimacion-pert-3-puntos" / "preview-pack.png",
        ]
    else:
        outs = [
            ROOT_DIR / "static" / "images" / "recursos" / "pert-preview-en.png",
            ROOT_DIR / "content" / "en" / "posts" / "stochastic-3-point-pert-estimation" / "preview-pack.png",
        ]
    for o in outs:
        o.parent.mkdir(parents=True, exist_ok=True)
        final_img.save(o, format="PNG", optimize=True)
        print(f" -> Preview guardada: {o}")


def main():
    print("[1/2] Generando preview compuesta en Español...")
    build_preview("ES")
    print("[2/2] Generando preview compuesta en Inglés...")
    build_preview("EN")
    print("Previews generadas correctamente.")


if __name__ == "__main__":
    main()
