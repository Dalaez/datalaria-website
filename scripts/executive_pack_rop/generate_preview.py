#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_preview.py
===================
Genera las imágenes compuestas `preview-pack.png` (1600 x 980 px) a partir de los
activos reales generados en `packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/`:
- Excel Dashboard: métricas reales de `Calculadora_Stock_Seguridad_ROP_ES.xlsx` /
  `Safety_Stock_ROP_Calculator_EN.xlsx` (Inversión SS = 891.496 €, Capital Liberable = 1.095.966 €,
  Panel Control SKU-1001 con EOQ=925 u, ROP=617 u, SS=217 u, Matriz ABC y Gráfico Diente de Sierra).
- Guía PDF: renderizado real de páginas 1 y 2 vía `pypdfium2` / `fitz`.
- Deck PPTX 16:9: exportación real de Slide 2 vía PowerPoint COM (con fallback Pillow seguro).

Salidas:
- static/images/recursos/stock-preview-es.png
- content/es/posts/calculadora-stock-seguridad-rop/preview-pack.png
- static/images/recursos/stock-preview-en.png
- content/en/posts/safety-stock-reorder-point-calculator/preview-pack.png
"""

import os
import sys
import tempfile
from io import BytesIO
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PKG_DIR = ROOT_DIR / "packages" / "Suite_03_Control_Operativo" / "05_Stock_Seguridad_ROP"

W, H = 1600, 980


def get_font(name: str, size: int):
    paths = [
        rf"C:\Windows\Fonts\{name}",
        r"C:\Windows\Fonts\segoeui.ttf",
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
    is_es = (lang == "ES")
    win_w, win_h = 900, 924
    title = (
        "Calculadora_Stock_Seguridad_ROP_ES.xlsx — Excel 365 & Google Sheets"
        if is_es
        else "Safety_Stock_ROP_Calculator_EN.xlsx — Excel 365 & Google Sheets"
    )
    badge = "MODELO PROTEGIDO · 4 PESTAÑAS" if is_es else "PROTECTED ENGINE · 4 TABS"
    win = make_window_chrome(win_w, win_h, title, badge, badge_bg=(5, 150, 105), body_bg=(248, 250, 252))
    d = ImageDraw.Draw(win)

    f_h1 = get_font("segoeuib.ttf", 16)
    f_sub = get_font("segoeui.ttf", 11)
    f_b11 = get_font("segoeuib.ttf", 11)
    f_r11 = get_font("segoeui.ttf", 11)
    f_r10 = get_font("segoeui.ttf", 10)
    f_kpi = get_font("segoeuib.ttf", 20)
    f_mono = get_font("consola.ttf", 11)
    f_monob = get_font("consolab.ttf", 11)

    # Sheet header banner
    d.rounded_rectangle([(14, 48), (win_w - 14, 104)], radius=8, fill=(15, 23, 42))
    h_txt = (
        "CUADRO DE MANDO EJECUTIVO: STOCK DE SEGURIDAD & ROP"
        if is_es
        else "EXECUTIVE DASHBOARD: SAFETY STOCK & REORDER POINT (ROP)"
    )
    s_txt = (
        "Estándar APICS / MIT CTL · Catálogo: 35 SKUs Estocásticos · Control C-Level"
        if is_es
        else "APICS / MIT CTL Standard · Catalog: 35 Stochastic SKUs · C-Level Working Capital"
    )
    d.text((28, 56), h_txt, fill=(255, 255, 255), font=f_h1)
    d.text((28, 80), s_txt, fill=(148, 163, 184), font=f_sub)

    # 4 Top KPI Cards
    kpis = (
        [
            ("INVERSIÓN STOCK SEGURIDAD", "891.496 €", "35 SKUs Convolución SS3", (239, 246, 255), (37, 99, 235), (30, 58, 138)),
            ("NIVEL SERVICIO MEDIO", "93,3%", "Prob. Rotura (1-CSL): 6,7%", (240, 253, 244), (16, 185, 129), (6, 95, 70)),
            ("CAPITAL LIBERABLE", "1.095.966 €", "Vs. Regla Empírica 3 sem.", (245, 243, 255), (124, 58, 237), (109, 40, 217)),
            ("SKUs EN RIESGO CRÍTICO", "3 SKUs", "Infradotados por heurística", (254, 242, 242), (220, 38, 38), (185, 28, 28)),
        ]
        if is_es
        else [
            ("SAFETY STOCK CAPITAL", "$891,496", "35 SKUs SS3 Convolution", (239, 246, 255), (37, 99, 235), (30, 58, 138)),
            ("WEIGHTED SERVICE LEVEL", "93.3%", "Stockout Risk (1-CSL): 6.7%", (240, 253, 244), (16, 185, 129), (6, 95, 70)),
            ("RELEASABLE CAPITAL", "$1,095,966", "Vs. 3-Week Rule of Thumb", (245, 243, 255), (124, 58, 237), (109, 40, 217)),
            ("SKUs AT STOCKOUT RISK", "3 SKUs", "Under-buffered by rule", (254, 242, 242), (220, 38, 38), (185, 28, 28)),
        ]
    )
    cw = (win_w - 28 - 36) // 4
    ky = 116
    for i, (lbl, val, sub, bg, bdr, col) in enumerate(kpis):
        kx = 14 + i * (cw + 12)
        d.rounded_rectangle([(kx, ky), (kx + cw, ky + 82)], radius=8, fill=bg, outline=bdr, width=1)
        d.text((kx + 12, ky + 9), lbl, fill=(71, 85, 105), font=get_font("segoeuib.ttf", 9))
        d.text((kx + 12, ky + 28), val, fill=col, font=f_kpi)
        d.text((kx + 12, ky + 60), sub, fill=(100, 116, 139), font=f_r10)

    # Middle Left: Interactive Benchmark SKU Card + ABC Matrix
    mx, my, mw, mh = 14, 210, 392, 392
    d.rounded_rectangle([(mx, my), (mx + mw, my + mh)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(mx, my), (mx + mw, my + 30)], radius=8, fill=(30, 41, 59))
    d.rectangle([(mx, my + 16), (mx + mw, my + 30)], fill=(30, 41, 59))
    ctrl_t = "CONTROL SKU SIMULADO & ESTRATIFICACIÓN ABC" if is_es else "BENCHMARK SKU CONTROL & ABC STRATIFICATION"
    d.text((mx + 12, my + 8), ctrl_t, fill=(255, 255, 255), font=get_font("segoeuib.ttf", 10))

    # SKU Selector card
    d.rounded_rectangle([(mx + 10, my + 38), (mx + mw - 10, my + 66)], radius=5, fill=(239, 246, 255), outline=(37, 99, 235))
    sku_sel_txt = "SKU Seleccionado: SKU-1001 · Microcontrolador M4" if is_es else "Selected SKU: SKU-1001 · ARM Cortex-M4 MCU"
    d.text((mx + 18, my + 45), sku_sel_txt, fill=(30, 58, 138), font=f_b11)

    # 4 mini parameter pills (EOQ, ROP, SS, CSL)
    pw_s = (mw - 38) // 4
    params_sku = [
        ("EOQ", "925 u", (241, 245, 249), (15, 23, 42)),
        ("ROP", "617 u", (254, 243, 199), (180, 83, 9)),
        ("SS", "217 u", (209, 250, 229), (4, 120, 87)),
        ("CSL", "98.0%", (241, 245, 249), (15, 23, 42)),
    ]
    for idx_p, (plbl, pval, pbg, pfg) in enumerate(params_sku):
        px0 = mx + 10 + idx_p * (pw_s + 6)
        py0 = my + 74
        d.rounded_rectangle([(px0, py0), (px0 + pw_s, py0 + 48)], radius=5, fill=pbg, outline=(203, 213, 225))
        d.text((px0 + 8, py0 + 6), plbl, fill=(100, 116, 139), font=get_font("segoeuib.ttf", 9))
        d.text((px0 + 8, py0 + 22), pval, fill=pfg, font=get_font("segoeuib.ttf", 13))

    # ABC Matrix inside Middle Left
    ay0 = my + 134
    a_hdr = "MATRIZ DE DISTRIBUCIÓN PARETO ABC" if is_es else "PARETO ABC PORTFOLIO STRATIFICATION"
    d.rectangle([(mx + 10, ay0), (mx + mw - 10, ay0 + 24)], fill=(15, 23, 42))
    d.text((mx + 16, ay0 + 5), a_hdr, fill=(255, 255, 255), font=get_font("segoeuib.ttf", 10))

    ay0 += 28
    abc_cols = ["Clase", "SKUs", "% Val.", "Inversión SS"] if is_es else ["Class", "SKUs", "% Val.", "SS Capital"]
    abc_cx = [mx + 14, mx + 92, mx + 166, mx + 246]
    d.rectangle([(mx + 10, ay0), (mx + mw - 10, ay0 + 22)], fill=(226, 232, 240))
    for i_c, cn in enumerate(abc_cols):
        d.text((abc_cx[i_c], ay0 + 4), cn, fill=(15, 23, 42), font=get_font("segoeuib.ttf", 9))

    abc_rows = (
        [
            ("Clase A", "7 (20%)", "47.3%", "701.010 €", (209, 250, 229), (6, 95, 70)),
            ("Clase B", "12 (34%)", "30.3%", "139.344 €", (254, 243, 199), (146, 64, 14)),
            ("Clase C", "16 (46%)", "22.4%", "51.142 €", (241, 245, 249), (51, 65, 85)),
            ("TOTAL", "35 SKUs", "100.0%", "891.496 €", (239, 246, 255), (30, 58, 138)),
        ]
        if is_es
        else [
            ("Class A", "7 (20%)", "47.3%", "$701,010", (209, 250, 229), (6, 95, 70)),
            ("Class B", "12 (34%)", "30.3%", "$139,344", (254, 243, 199), (146, 64, 14)),
            ("Class C", "16 (46%)", "22.4%", "$51,142", (241, 245, 249), (51, 65, 85)),
            ("TOTAL", "35 SKUs", "100.0%", "$891,496", (239, 246, 255), (30, 58, 138)),
        ]
    )
    ry_a = ay0 + 24
    for c_name, c_cnt, c_pv, c_inv, c_bg, c_fg in abc_rows:
        d.rectangle([(mx + 10, ry_a), (mx + mw - 10, ry_a + 44)], fill=(255, 255, 255), outline=(226, 232, 240))
        d.rounded_rectangle([(mx + 14, ry_a + 10), (mx + 82, ry_a + 34)], radius=4, fill=c_bg)
        d.text((mx + 22, ry_a + 15), c_name, fill=c_fg, font=get_font("segoeuib.ttf", 10))
        d.text((abc_cx[1], ry_a + 15), c_cnt, fill=(30, 41, 59), font=f_mono)
        d.text((abc_cx[2], ry_a + 15), c_pv, fill=(30, 41, 59), font=f_mono)
        d.text((abc_cx[3], ry_a + 15), c_inv, fill=c_fg, font=f_monob)
        ry_a += 46

    # Middle Right: Native Sawtooth Cycle Chart (0..30 Days)
    gx, gy, gw, gh = 418, 210, win_w - 14 - 418, 392
    d.rounded_rectangle([(gx, gy), (gx + gw, gy + gh)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(gx, gy), (gx + gw, gy + 30)], radius=8, fill=(30, 41, 59))
    d.rectangle([(gx, gy + 16), (gx + gw, gy + 30)], fill=(30, 41, 59))
    g_title = "CICLO DIENTE DE SIERRA (SAWTOOTH) · SKU-1001" if is_es else "SAWTOOTH REPLENISHMENT CYCLE · SKU-1001"
    d.text((gx + 14, gy + 8), g_title, fill=(255, 255, 255), font=f_b11)

    leg_y = gy + 42
    legs = (
        [("Inventario Físico (u)", (37, 99, 235)), ("ROP (617 u)", (217, 119, 6)), ("SS Colchón (217 u)", (5, 150, 105))]
        if is_es
        else [("Physical Stock (u)", (37, 99, 235)), ("ROP (617 u)", (217, 119, 6)), ("SS Buffer (217 u)", (5, 150, 105))]
    )
    lx = gx + 48
    for l_t, l_c in legs:
        d.rectangle([(lx, leg_y + 3), (lx + 12, leg_y + 7)], fill=l_c)
        d.text((lx + 16, leg_y), l_t, fill=(51, 65, 85), font=f_r10)
        lx += 16 + text_w(d, l_t, f_r10) + 18

    ax_x0, ax_x1 = gx + 62, gx + gw - 22
    ax_y0, ax_y1 = gy + 72, gy + gh - 48
    y_max = 1250.0

    def map_x_day(day_val):
        return ax_x0 + (day_val / 30.0) * (ax_x1 - ax_x0)

    def map_y_u(u_val):
        return ax_y1 - (u_val / y_max) * (ax_y1 - ax_y0)

    for tick_u in [0, 250, 500, 750, 1000, 1250]:
        yy = int(map_y_u(tick_u))
        d.line([(ax_x0, yy), (ax_x1, yy)], fill=(226, 232, 240), width=1)
        d.text((gx + 14, yy - 6), f"{tick_u:,}", fill=(100, 116, 139), font=get_font("consola.ttf", 9))

    d.line([(ax_x0, ax_y1), (ax_x1, ax_y1)], fill=(71, 85, 105), width=2)
    d.line([(ax_x0, ax_y0), (ax_x0, ax_y1)], fill=(71, 85, 105), width=2)

    for d_tick in [0, 5, 10, 15, 20, 25, 30]:
        tx = int(map_x_day(d_tick))
        d.line([(tx, ax_y1), (tx, ax_y1 + 4)], fill=(100, 116, 139), width=1)
        d.text((tx - 6, ax_y1 + 7), f"D{d_tick}", fill=(71, 85, 105), font=get_font("consola.ttf", 9))

    ax_lbl = "Días del Ciclo de Reabastecimiento (0 – 30 días)" if is_es else "Replenishment Cycle Timeline (0 – 30 days)"
    d.text((ax_x0 + (ax_x1 - ax_x0 - text_w(d, ax_lbl, f_r10)) // 2, ax_y1 + 23), ax_lbl, fill=(51, 65, 85), font=f_r10)

    # Plot SS (217), ROP (617), and Sawtooth (1142 -> 217 -> 1142 -> 217)
    yy_ss = int(map_y_u(217))
    yy_rop = int(map_y_u(617))
    yy_peak = int(map_y_u(1142))

    # Light emerald shaded SS band
    d.rectangle([(ax_x0 + 1, yy_ss), (ax_x1, ax_y1 - 1)], fill=(209, 250, 229))
    d.line([(ax_x0, yy_ss), (ax_x1, yy_ss)], fill=(5, 150, 105), width=2)

    # Dashed Amber ROP line
    for dx in range(int(ax_x0), int(ax_x1) - 4, 10):
        d.line([(dx, yy_rop), (min(dx + 5, int(ax_x1)), yy_rop)], fill=(217, 119, 6), width=2)

    x0_d, x15_d, x30_d = map_x_day(0), map_x_day(15), map_x_day(30)
    saw_pts = [(x0_d, yy_peak), (x15_d, yy_ss), (x15_d, yy_peak), (x30_d, yy_ss), (x30_d, yy_peak)]
    for i_s in range(len(saw_pts) - 1):
        d.line([saw_pts[i_s], saw_pts[i_s + 1]], fill=(37, 99, 235), width=3)

    # Triggers on day ~8.5 and ~23.5 where stock hits 617
    x_trig1 = map_x_day(8.51)
    x_trig2 = map_x_day(23.51)
    for tx_m in [x_trig1, x_trig2]:
        d.ellipse([(tx_m - 5, yy_rop - 5), (tx_m + 5, yy_rop + 5)], fill=(217, 119, 6), outline=(255, 255, 255), width=1)
    d.ellipse([(x15_d - 5, yy_ss - 5), (x15_d + 5, yy_ss + 5)], fill=(5, 150, 105), outline=(255, 255, 255), width=1)

    # Annotations cleanly placed
    d.rounded_rectangle([(int(x_trig1) + 12, yy_rop - 28), (int(x_trig1) + 114, yy_rop - 8)], radius=4, fill=(254, 243, 199), outline=(217, 119, 6))
    d.text((int(x_trig1) + 18, yy_rop - 24), "Disparo ROP" if is_es else "ROP Trigger", fill=(180, 83, 9), font=get_font("segoeuib.ttf", 9))

    d.rounded_rectangle([(int(x15_d) + 8, yy_peak - 4), (int(x15_d) + 110, yy_peak + 16)], radius=4, fill=(239, 246, 255), outline=(37, 99, 235))
    d.text((int(x15_d) + 14, yy_peak), "+EOQ: 925 u", fill=(30, 58, 138), font=get_font("segoeuib.ttf", 9))

    # Bottom Section: Tab 3 Stochastic Matrix & Simulation Diagnostics
    cx, cy, cw_tbl, ch_tbl = 14, 614, win_w - 28, 256
    d.rounded_rectangle([(cx, cy), (cx + cw_tbl, cy + ch_tbl)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.rounded_rectangle([(cx, cy), (cx + cw_tbl, cy + 30)], radius=8, fill=(15, 23, 42))
    d.rectangle([(cx, cy + 16), (cx + cw_tbl, cy + 30)], fill=(15, 23, 42))
    tbl_t = (
        "PESTAÑAS 2, 3 & 4 · MOTOR ESTOCÁSTICO CONVOLUCIÓN SS₃, ROP, WILSON EOQ & WORKING CAPITAL"
        if is_es
        else "TABS 2, 3 & 4 · STOCHASTIC CONVOLUTION ENGINE SS₃, ROP, WILSON EOQ & WORKING CAPITAL"
    )
    d.text((cx + 14, cy + 8), tbl_t, fill=(255, 255, 255), font=f_b11)

    cols = (
        ["SKU", "Descripción Crítica", "Factor Z", "SS₃ Óptimo", "ROP", "EOQ", "Diagnóstico Heurística"]
        if is_es
        else ["SKU", "Critical Product", "Z-Factor", "Optimal SS₃", "ROP", "EOQ", "Heuristic Gap"]
    )
    col_x = [cx + 14, cx + 88, cx + 356, cx + 436, cx + 528, cx + 610, cx + 694]
    hy = cy + 36
    d.rectangle([(cx + 8, hy), (cx + cw_tbl - 8, hy + 26)], fill=(226, 232, 240))
    for i, cname in enumerate(cols):
        d.text((col_x[i], hy + 6), cname, fill=(15, 23, 42), font=get_font("segoeuib.ttf", 10))

    sku_rows = (
        [
            ("SKU-1001", "Microcontrolador Industrial Cortex M4", "2.054", "217 u", "617 u", "925 u", "OPTIMIZADO", "ok"),
            ("SKU-1002", "Módulo de Potencia IGBT 1200V/100A", "2.054", "898 u", "2.683 u", "686 u", "SOBRESTOCK (+64k€)", "warn"),
            ("SKU-1003", "Servomotor Brushless Precisión 2.5kW", "2.054", "880 u", "2.105 u", "322 u", "RIESGO ROTURA", "risk"),
            ("SKU-1004", "Reactivo Enzimático BioTech 50ml", "2.326", "331 u", "981 u", "350 u", "SOBRESTOCK (+145k€)", "warn"),
            ("SKU-1005", "Bomba Hidráulica Pistones Axiales", "2.054", "741 u", "1.741 u", "223 u", "RIESGO ROTURA", "risk"),
            ("SKU-2001", "Fuente Conmutada Industrial 24V", "1.645", "384 u", "1.434 u", "812 u", "SOBRESTOCK (+38k€)", "ok"),
        ]
        if is_es
        else [
            ("SKU-1001", "Industrial MCU 32-bit Cortex M4", "2.054", "217 u", "617 u", "925 u", "OPTIMIZED", "ok"),
            ("SKU-1002", "Power IGBT Module 1200V / 100A", "2.054", "898 u", "2,683 u", "686 u", "OVERSTOCK (+$64k)", "warn"),
            ("SKU-1003", "High-Precision Brushless Servo 2.5kW", "2.054", "880 u", "2,105 u", "322 u", "STOCKOUT RISK", "risk"),
            ("SKU-1004", "Ultra-Pure BioTech Reagent 50ml", "2.326", "331 u", "981 u", "350 u", "OVERSTOCK (+$145k)", "warn"),
            ("SKU-1005", "Axial Piston Hydraulic Pump", "2.054", "741 u", "1,741 u", "223 u", "STOCKOUT RISK", "risk"),
            ("SKU-2001", "Switched Industrial Power 24V", "1.645", "384 u", "1,434 u", "812 u", "OVERSTOCK (+$38k)", "ok"),
        ]
    )
    ry_c = hy + 28
    for idx, (sk, nm, zv, ss_v, rop_v, eoq_v, diag_v, state) in enumerate(sku_rows):
        bg_c = (248, 250, 252) if idx % 2 == 0 else (255, 255, 255)
        d.rectangle([(cx + 8, ry_c), (cx + cw_tbl - 8, ry_c + 29)], fill=bg_c, outline=(241, 245, 249))
        vals = [sk, nm, zv, ss_v, rop_v, eoq_v]
        for i, v in enumerate(vals):
            d.text((col_x[i], ry_c + 7), v, fill=(30, 41, 59), font=f_mono if i != 1 else f_r11)
        if state == "ok":
            pill_bg, pill_fg = (220, 252, 231), (5, 150, 105)
        elif state == "warn":
            pill_bg, pill_fg = (254, 243, 199), (146, 64, 14)
        else:
            pill_bg, pill_fg = (254, 226, 226), (185, 28, 28)
        d.rounded_rectangle([(col_x[6] - 4, ry_c + 4), (cx + cw_tbl - 14, ry_c + 25)], radius=4, fill=pill_bg)
        d.text((col_x[6] + 4, ry_c + 7), diag_v, fill=pill_fg, font=get_font("segoeuib.ttf", 10))
        ry_c += 30

    # Excel Bottom Worksheet Tabs
    tabs = (
        ["Dashboard Ejecutivo", "Matriz SKU & Datos Operativos", "Motor Matemático SS & ROP", "Trade-offs Working Capital"]
        if is_es
        else ["Executive Dashboard", "SKU Matrix & Operational Inputs", "Safety Stock & ROP Models", "Working Capital Trade-offs"]
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
    is_es = (lang == "ES")
    win_w, win_h = 630, 494
    pdf_file = (
        PKG_DIR / "[ES]_Stock_Seguridad_ROP" / "Guia_Metodologica_Stock_ROP_ES.pdf"
        if is_es
        else PKG_DIR / "[EN]_Safety_Stock_ROP" / "Methodology_Guide_Safety_Stock_ROP_EN.pdf"
    )
    badge = "GUÍA METODOLÓGICA · 5 PÁGINAS" if is_es else "METHODOLOGY GUIDE · 5 PAGES"
    win = make_window_chrome(win_w, win_h, pdf_file.name, badge, badge_bg=(220, 38, 38), body_bg=(30, 41, 59))

    pages = render_pdf_pages(pdf_file, page_indices=(0, 1), target_h=416)
    px = 24
    for p_img in pages:
        paste_with_shadow(win, p_img, (px, 56))
        px += p_img.width + 20
    return win


def draw_pptx_window(lang: str) -> Image.Image:
    is_es = (lang == "ES")
    win_w, win_h = 630, 410
    pptx_file = (
        PKG_DIR / "[ES]_Stock_Seguridad_ROP" / "Presentacion_Stock_ROP_CLevel_ES.pptx"
        if is_es
        else PKG_DIR / "[EN]_Safety_Stock_ROP" / "Deck_Safety_Stock_ROP_CLevel_EN.pptx"
    )
    badge = "DECK EJECUTIVO 16:9 · SLIDE 2" if is_es else "C-LEVEL 16:9 DECK · SLIDE 2"
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
            ROOT_DIR / "static" / "images" / "recursos" / "stock-preview-es.png",
            ROOT_DIR / "content" / "es" / "posts" / "calculadora-stock-seguridad-rop" / "preview-pack.png",
        ]
    else:
        outs = [
            ROOT_DIR / "static" / "images" / "recursos" / "stock-preview-en.png",
            ROOT_DIR / "content" / "en" / "posts" / "safety-stock-reorder-point-calculator" / "preview-pack.png",
        ]
    for o in outs:
        o.parent.mkdir(parents=True, exist_ok=True)
        final_img.save(o, format="PNG", optimize=True)
        print(f" -> Preview guardada: {o}")


def main():
    print("[1/2] Generando preview compuesta Stock & ROP en Español...")
    build_preview("ES")
    print("[2/2] Generando preview compuesta Stock & ROP en Inglés...")
    build_preview("EN")
    print("Previews Stock & ROP generadas correctamente.")


if __name__ == "__main__":
    main()
