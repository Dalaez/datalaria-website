#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pulse_cover.py
=======================
Genera programáticamente las portadas oficiales de Datalaria Pulse:
1. Portada Ilustrada Conceptual del Post 1 (1200 x 630 px) para ES y EN.
   - Ilustración arquitectónica conceptual: De los silos de Notion al Git SSOT y Cockpit de Pulse.
   - Esquina superior izquierda: Icono del pulso azul (ECG waveform) identificando la serie editorial.
   - Sin capturas de pantalla de la interfaz, 100% gráfico e ilustrado.
   - Tipografía corporativa con acentos nativos y balance visual Tier-1.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1200
HEIGHT = 630


def get_font(name: str, size: int):
    """Carga fuente TrueType del sistema con fallback seguro."""
    candidates = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
        "C:/Windows/Fonts/segoeuib.ttf" if "b" in name.lower() else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if "b" in name.lower() else "C:/Windows/Fonts/arial.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_pulse_waveform(draw, x: float, y: float, w: float, h: float, color=(56, 189, 248), stroke_width=2):
    """
    Dibuja la onda de pulso exacta de Datalaria Pulse:
    M22 12h-4l-3 9L9 3l-3 9H2
    Puntos normalizados (0 a 24):
    (2, 12) -> (6, 12) -> (9, 3) -> (15, 21) -> (18, 12) -> (22, 12)
    """
    pts = [
        (2.0, 12.0),
        (6.0, 12.0),
        (9.0, 3.0),
        (15.0, 21.0),
        (18.0, 12.0),
        (22.0, 12.0)
    ]
    scaled_pts = []
    for px, py in pts:
        sx = x + (px / 24.0) * w
        sy = y + (py / 24.0) * h
        scaled_pts.append((sx, sy))

    for i in range(len(scaled_pts) - 1):
        p1 = scaled_pts[i]
        p2 = scaled_pts[i + 1]
        draw.line([p1, p2], fill=color, width=stroke_width)


def create_post1_cover(lang: str = "es") -> Image.Image:
    """Crea la portada conceptual ilustrada para el Artículo 1 de Datalaria Pulse."""
    # 1. Lienzo Base
    img = Image.new("RGBA", (WIDTH, HEIGHT), (11, 17, 32, 255))
    draw = ImageDraw.Draw(img)

    # Gradiente vertical oscuro de alta fidelidad
    c_top = (7, 12, 22)
    c_bot = (15, 23, 42)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # 2. Resplandores ambientales de fondo (Atmospheric glow)
    glow_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    # Glow sutil ambar en la columna Notion
    glow_draw.ellipse([-80, 160, 340, 560], fill=(239, 68, 68, 16))
    # Glow cian en el Git engine central
    glow_draw.ellipse([420, 120, 840, 520], fill=(6, 182, 212, 24))
    # Glow esmeralda en el cockpit de Pulse
    glow_draw.ellipse([840, 140, 1260, 540], fill=(16, 185, 129, 20))
    # Glow cian superior izquierdo para el badge de serie
    glow_draw.ellipse([20, 10, 380, 150], fill=(56, 189, 248, 22))

    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img, glow_overlay)
    draw = ImageDraw.Draw(img)

    # 3. Malla técnica blueprint sutil y oscura
    grid_color = (18, 28, 48, 255)
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color)

    # Micro-cruces en intersecciones
    cross_color = (30, 41, 59, 255)
    for x in range(80, WIDTH, 160):
        for y in range(80, HEIGHT, 160):
            draw.line([(x - 3, y), (x + 3, y)], fill=cross_color)
            draw.line([(x, y - 3), (x, y + 3)], fill=cross_color)

    # 4. Fuentes del sistema
    font_brand = get_font("segoeuib.ttf", 13)
    font_series = get_font("segoeuib.ttf", 12)
    font_mono_small = get_font("consola.ttf", 11)
    font_mono_bold = get_font("consolab.ttf", 12)
    font_title = get_font("segoeuib.ttf", 27)
    font_subtitle = get_font("segoeui.ttf", 14)
    font_card_header = get_font("segoeuib.ttf", 13)
    font_card_sub = get_font("segoeui.ttf", 11)
    font_card_body_bold = get_font("segoeuib.ttf", 11)
    font_badge = get_font("segoeuib.ttf", 10)
    font_kpi_val = get_font("segoeuib.ttf", 20)
    font_kpi_lbl = get_font("segoeui.ttf", 10)

    # =========================================================================
    # 5. HEADER Y BADGE DE SERIE CON EL FAVICON DE PULSE (ESQUINA SUP. IZQ.)
    # =========================================================================
    icon_box_x = 45
    icon_box_y = 24
    icon_size = 32

    # Contenedor del favicon con borde cian
    draw.rounded_rectangle(
        [icon_box_x, icon_box_y, icon_box_x + icon_size, icon_box_y + icon_size],
        radius=7,
        fill=(15, 23, 42, 255),
        outline=(56, 189, 248, 220),
        width=1
    )
    # Resplandor sutil del icono
    draw_pulse_waveform(draw, icon_box_x + 3, icon_box_y + 3, icon_size - 6, icon_size - 6, color=(56, 189, 248, 80), stroke_width=4)
    # Trazo nítido del icono de pulso en azul cian (#38bdf8)
    draw_pulse_waveform(draw, icon_box_x + 3, icon_box_y + 3, icon_size - 6, icon_size - 6, color=(56, 189, 248, 255), stroke_width=2)

    # Textos de identificación de la serie
    series_txt_x = icon_box_x + icon_size + 12
    draw.text((series_txt_x, icon_box_y + 6), "DATALARIA PULSE", font=font_brand, fill=(56, 189, 248, 255))
    draw.text((series_txt_x + 130, icon_box_y + 6), "-", font=font_series, fill=(100, 116, 139, 255))
    
    series_badge_text = "SERIE EDITORIAL (1/5)" if lang == "es" else "EDITORIAL SERIES (1/5)"
    draw.text((series_txt_x + 144, icon_box_y + 6), series_badge_text, font=font_series, fill=(244, 114, 182, 255))
    
    sub_tag = "CONTENT OPS AS CODE"
    tag_x = series_txt_x + 310
    draw.rounded_rectangle(
        [tag_x, icon_box_y + 3, tag_x + 145, icon_box_y + 24],
        radius=4,
        fill=(6, 182, 212, 35),
        outline=(6, 182, 212, 140),
        width=1
    )
    draw.text((tag_x + 10, icon_box_y + 6), sub_tag, font=font_badge, fill=(34, 211, 238, 255))

    watermark_text = "datalaria.com  |  Engineering Intelligence"
    draw.text((WIDTH - 290, icon_box_y + 8), watermark_text, font=font_mono_small, fill=(100, 116, 139, 220))

    # =========================================================================
    # 6. TÍTULO Y SUBTÍTULO DEL ARTÍCULO 1
    # =========================================================================
    title_y = 68
    if lang == "es":
        title_text = "Adiós Notion: Datalaria Pulse y Content Ops as Code"
        subtitle_text = "De la desincronización de bases de datos a la gestión editorial determinista que se escribe sola desde Git"
    else:
        title_text = "Goodbye Notion: Datalaria Pulse and Content Ops as Code"
        subtitle_text = "From external database drift to deterministic editorial operations written directly from Git"

    draw.text((45, title_y), title_text, font=font_title, fill=(248, 250, 252, 255))
    draw.text((45, title_y + 34), subtitle_text, font=font_subtitle, fill=(148, 163, 184, 255))

    # =========================================================================
    # 7. ILUSTRACIÓN CONCEPTUAL: EL PIPELINE DE TRANSFORMACIÓN (3 COLUMNAS)
    # =========================================================================
    col_y1 = 142
    col_y2 = 562
    col_h = col_y2 - col_y1

    c1_x1, c1_x2 = 45, 360
    c2_x1, c2_x2 = 430, 785
    c3_x1, c3_x2 = 855, 1155

    # -------------------------------------------------------------------------
    # CONECTORES DE FLUJO ENTRE ETAPAS
    # -------------------------------------------------------------------------
    # Conector 1: Notion -> Git
    arrow1_cy = col_y1 + col_h // 2
    draw.line([(c1_x2 + 4, arrow1_cy), (c2_x1 - 4, arrow1_cy)], fill=(244, 63, 94, 200), width=2)
    draw.polygon([(c2_x1 - 4, arrow1_cy), (c2_x1 - 12, arrow1_cy - 5), (c2_x1 - 12, arrow1_cy + 5)], fill=(244, 63, 94, 255))
    
    badge1_txt = "MIGRAR ->" if lang == "es" else "MIGRATE ->"
    b1_w = 64
    b1_x = (c1_x2 + c2_x1 - b1_w) // 2
    draw.rounded_rectangle([b1_x, arrow1_cy - 12, b1_x + b1_w, arrow1_cy + 12], radius=4, fill=(15, 23, 42, 255), outline=(244, 63, 94, 180), width=1)
    draw.text((b1_x + 6, arrow1_cy - 6), badge1_txt, font=font_mono_small, fill=(251, 113, 133, 255))

    # Conector 2: Git -> Pulse
    arrow2_cy = col_y1 + col_h // 2
    draw.line([(c2_x2 + 4, arrow2_cy), (c3_x1 - 4, arrow2_cy)], fill=(16, 185, 129, 200), width=2)
    draw.polygon([(c3_x1 - 4, arrow2_cy), (c3_x1 - 12, arrow2_cy - 5), (c3_x1 - 12, arrow2_cy + 5)], fill=(16, 185, 129, 255))

    badge2_txt = "0ms TOIL"
    b2_w = 60
    b2_x = (c2_x2 + c3_x1 - b2_w) // 2
    draw.rounded_rectangle([b2_x, arrow2_cy - 12, b2_x + b2_w, arrow2_cy + 12], radius=4, fill=(15, 23, 42, 255), outline=(16, 185, 129, 180), width=1)
    draw.text((b2_x + 6, arrow2_cy - 6), badge2_txt, font=font_mono_small, fill=(52, 211, 153, 255))

    # -------------------------------------------------------------------------
    # COLUMNA 1: NOTION & SILOS EXTERNOS (EL PASADO: DRIFT Y CAOS)
    # -------------------------------------------------------------------------
    draw.rounded_rectangle([c1_x1, col_y1, c1_x2, col_y2], radius=10, fill=(15, 23, 42, 250), outline=(239, 68, 68, 110), width=1)
    draw.rounded_rectangle([c1_x1, col_y1, c1_x2, col_y1 + 34], radius=10, fill=(30, 41, 59, 230))
    draw.rectangle([c1_x1, col_y1 + 24, c1_x2, col_y1 + 34], fill=(30, 41, 59, 230))
    draw.text((c1_x1 + 14, col_y1 + 8), "[ALERTA] SILOS NOTION & CAOS" if lang == "es" else "[ALERT] NOTION SILOS & DRIFT", font=font_card_header, fill=(248, 113, 113, 255))

    # Tarjeta 1
    card1_y = col_y1 + 44
    draw.rounded_rectangle([c1_x1 + 12, card1_y, c1_x2 - 12, card1_y + 74], radius=6, fill=(11, 17, 32, 255), outline=(51, 65, 85, 200), width=1)
    draw.text((c1_x1 + 20, card1_y + 8), "Notion: Plan Editorial 2026" if lang == "es" else "Notion: Editorial Plan 2026", font=font_card_body_bold, fill=(226, 232, 240, 255))
    draw.text((c1_x1 + 20, card1_y + 26), "Estado: 'Publicado' (falta en web)" if lang == "es" else "Status: 'Published' (missing on web)", font=font_card_sub, fill=(148, 163, 184, 255))
    draw.rounded_rectangle([c1_x1 + 20, card1_y + 46, c1_x1 + 155, card1_y + 64], radius=3, fill=(239, 68, 68, 30), outline=(239, 68, 68, 140), width=1)
    draw.text((c1_x1 + 26, card1_y + 49), "[!] SCHEMA DRIFT 409", font=font_mono_small, fill=(248, 113, 113, 255))

    # Tarjeta 2
    card2_y = card1_y + 82
    draw.rounded_rectangle([c1_x1 + 12, card2_y, c1_x2 - 12, card2_y + 74], radius=6, fill=(11, 17, 32, 255), outline=(51, 65, 85, 200), width=1)
    draw.text((c1_x1 + 20, card2_y + 8), "plan_editorial_v2_final.xlsx", font=font_card_body_bold, fill=(226, 232, 240, 255))
    draw.text((c1_x1 + 20, card2_y + 26), "Metadatos sin contratos de tipado" if lang == "es" else "Metadata without strict schemas", font=font_card_sub, fill=(148, 163, 184, 255))
    draw.rounded_rectangle([c1_x1 + 20, card2_y + 46, c1_x1 + 165, card2_y + 64], radius=3, fill=(245, 158, 11, 30), outline=(245, 158, 11, 140), width=1)
    draw.text((c1_x1 + 26, card2_y + 49), "[!] ESQUEMA MANUAL" if lang == "es" else "[!] MANUAL SCHEMA", font=font_mono_small, fill=(251, 191, 36, 255))

    # Tarjeta 3
    card3_y = card2_y + 82
    draw.rounded_rectangle([c1_x1 + 12, card3_y, c1_x2 - 12, card3_y + 74], radius=6, fill=(11, 17, 32, 255), outline=(51, 65, 85, 200), width=1)
    draw.text((c1_x1 + 20, card3_y + 8), "Slugs & Enlaces Huérfanos" if lang == "es" else "Orphaned Slugs & Dead Links", font=font_card_body_bold, fill=(226, 232, 240, 255))
    draw.text((c1_x1 + 20, card3_y + 26), "Traducción EN desfasada de ES" if lang == "es" else "EN translation lagging behind ES", font=font_card_sub, fill=(148, 163, 184, 255))
    draw.rounded_rectangle([c1_x1 + 20, card3_y + 46, c1_x1 + 175, card3_y + 64], radius=3, fill=(239, 68, 68, 30), outline=(239, 68, 68, 140), width=1)
    draw.text((c1_x1 + 26, card3_y + 49), "[X] ENLACES ROTOS" if lang == "es" else "[X] BROKEN LINKS", font=font_mono_small, fill=(248, 113, 113, 255))

    # Lista de fricciones
    fn1_y = card3_y + 86
    bullets = [
        "Sin control de versiones atómico",
        "Pérdida de contexto editorial",
        "Toil manual y rotura silenciosa"
    ] if lang == "es" else [
        "No atomic version control",
        "Loss of editorial context",
        "Manual toil & silent link breaks"
    ]
    for b_idx, b_txt in enumerate(bullets):
        by = fn1_y + (b_idx * 20)
        draw.ellipse([c1_x1 + 18, by + 4, c1_x1 + 24, by + 10], fill=(239, 68, 68, 240))
        draw.text((c1_x1 + 32, by), b_txt, font=font_card_sub, fill=(148, 163, 184, 220))

    # -------------------------------------------------------------------------
    # COLUMNA 2: GIT REPOSITORY & PIPELINE PYDANTIC (EL CORAZÓN SDD)
    # -------------------------------------------------------------------------
    draw.rounded_rectangle([c2_x1, col_y1, c2_x2, col_y2], radius=10, fill=(12, 20, 36, 250), outline=(6, 182, 212, 160), width=1)
    draw.rounded_rectangle([c2_x1, col_y1, c2_x2, col_y1 + 34], radius=10, fill=(15, 32, 53, 230))
    draw.rectangle([c2_x1, col_y1 + 24, c2_x2, col_y1 + 34], fill=(15, 32, 53, 230))
    draw.text((c2_x1 + 14, col_y1 + 8), "[CORE] GIT SSOT & PIPELINE", font=font_card_header, fill=(34, 211, 238, 255))

    # Componente A: Árbol de Commits de Git
    git_tree_y = col_y1 + 44
    draw.rounded_rectangle([c2_x1 + 12, git_tree_y, c2_x2 - 12, git_tree_y + 94], radius=6, fill=(8, 13, 26, 255), outline=(30, 58, 138, 180), width=1)
    draw.text((c2_x1 + 20, git_tree_y + 8), "Árbol Atómico de Commits (Git main)" if lang == "es" else "Atomic Git Commit Tree (Git main)", font=font_mono_bold, fill=(147, 197, 253, 255))
    
    draw.line([(c2_x1 + 30, git_tree_y + 34), (c2_x1 + 30, git_tree_y + 78)], fill=(6, 182, 212, 220), width=2)
    commits = [
        (git_tree_y + 34, "c018a4d", "feat(pulse): pydantic content schema"),
        (git_tree_y + 56, "7bf29e1", "test: 100% bilingual pairing parity"),
        (git_tree_y + 78, "40c3d82", "release: v0.1.0 pulse standalone kit")
    ]
    for cy, c_hash, c_msg in commits:
        draw.ellipse([c2_x1 + 26, cy - 4, c2_x1 + 34, cy + 4], fill=(34, 211, 238, 255), outline=(255, 255, 255, 220), width=1)
        draw.text((c2_x1 + 42, cy - 6), c_hash, font=font_mono_small, fill=(56, 189, 248, 255))
        draw.text((c2_x1 + 96, cy - 6), c_msg, font=font_card_sub, fill=(203, 213, 225, 240))

    # Componente B: Escáner y Válvula Pydantic v2 (El Filtro Fail-Closed)
    pyd_y = git_tree_y + 104
    draw.rounded_rectangle([c2_x1 + 12, pyd_y, c2_x2 - 12, pyd_y + 124], radius=6, fill=(8, 13, 26, 255), outline=(16, 185, 129, 160), width=1)
    draw.text((c2_x1 + 20, pyd_y + 8), "[VALIDACIÓN] Válvula Pydantic v2" if lang == "es" else "[VALIDATION] Pydantic v2 Gate", font=font_card_body_bold, fill=(52, 211, 153, 255))
    
    checks = [
        ("Front Matter & Tipado Estricto", "Validado"),
        ("Invariante 1: Paridad ES <-> EN", "137 / 137 OK"),
        ("Invariante 2: Apps <-> Posts", "0 roturas"),
        ("Auditoría SEO & Conteo Léxico", "Score >= 80")
    ] if lang == "es" else [
        ("Front Matter & Strict Types", "Validated"),
        ("Invariant 1: Bilingual ES <-> EN", "137 / 137 OK"),
        ("Invariant 2: Apps <-> Posts", "0 broken"),
        ("SEO Audit & Lexical Count", "Score >= 80")
    ]
    cy = pyd_y + 30
    for chk_txt, chk_sub in checks:
        draw.ellipse([c2_x1 + 22, cy + 4, c2_x1 + 28, cy + 10], fill=(16, 185, 129, 255))
        draw.text((c2_x1 + 36, cy), chk_txt, font=font_card_sub, fill=(226, 232, 240, 240))
        draw.text((c2_x2 - 120, cy), chk_sub, font=font_mono_small, fill=(16, 185, 129, 240))
        cy += 22

    # Componente C: Automatización CI/CD GitHub Actions
    ci_y = pyd_y + 134
    draw.rounded_rectangle([c2_x1 + 12, ci_y, c2_x2 - 12, ci_y + 70], radius=6, fill=(15, 23, 42, 255), outline=(168, 85, 247, 160), width=1)
    draw.text((c2_x1 + 20, ci_y + 8), "[CI/CD] GitHub Actions Automation", font=font_card_body_bold, fill=(192, 132, 252, 255))
    draw.text((c2_x1 + 20, ci_y + 28), "$ python -m ops.pulse.build_index\n$ pytest ops/pulse/tests/  -->  18 passed (100%)", font=font_mono_small, fill=(148, 163, 184, 240))

    # -------------------------------------------------------------------------
    # COLUMNA 3: DATALARIA PULSE EXECUTIVE COCKPIT (EL RESULTADO DETERMINISTA)
    # -------------------------------------------------------------------------
    draw.rounded_rectangle([c3_x1, col_y1, c3_x2, col_y2], radius=10, fill=(10, 22, 33, 250), outline=(16, 185, 129, 160), width=1)
    draw.rounded_rectangle([c3_x1, col_y1, c3_x2, col_y1 + 34], radius=10, fill=(13, 40, 42, 230))
    draw.rectangle([c3_x1, col_y1 + 24, c3_x2, col_y1 + 34], fill=(13, 40, 42, 230))
    draw.text((c3_x1 + 14, col_y1 + 8), "[LIVE] COCKPIT EJECUTIVO PULSE" if lang == "es" else "[LIVE] PULSE EXECUTIVE COCKPIT", font=font_card_header, fill=(52, 211, 153, 255))

    # Monitor de Pulso Cardiaco
    scope_y = col_y1 + 44
    scope_w = c3_x2 - c3_x1 - 24
    scope_h = 70
    draw.rounded_rectangle([c3_x1 + 12, scope_y, c3_x2 - 12, scope_y + scope_h], radius=6, fill=(6, 16, 24, 255), outline=(16, 185, 129, 120), width=1)
    
    for gx in range(c3_x1 + 20, c3_x2 - 12, 20):
        draw.line([(gx, scope_y + 4), (gx, scope_y + scope_h - 4)], fill=(16, 185, 129, 25))
    for gy in range(scope_y + 10, scope_y + scope_h, 15):
        draw.line([(c3_x1 + 16, gy), (c3_x2 - 16, gy)], fill=(16, 185, 129, 25))
    
    wave_w = scope_w // 2 - 10
    draw_pulse_waveform(draw, c3_x1 + 16, scope_y + 12, wave_w, 46, color=(16, 185, 129, 90), stroke_width=4)
    draw_pulse_waveform(draw, c3_x1 + 16, scope_y + 12, wave_w, 46, color=(52, 211, 153, 255), stroke_width=2)
    draw_pulse_waveform(draw, c3_x1 + 16 + wave_w, scope_y + 12, wave_w, 46, color=(56, 189, 248, 90), stroke_width=4)
    draw_pulse_waveform(draw, c3_x1 + 16 + wave_w, scope_y + 12, wave_w, 46, color=(56, 189, 248, 255), stroke_width=2)

    # 4 Mini-KPIs en Grid 2x2
    kpi_grid_y = scope_y + scope_h + 10
    kpis = [
        ("137", "Total Activos" if lang == "es" else "Total Assets", (56, 189, 248)),
        ("100%", "Paridad ES <-> EN" if lang == "es" else "Bilingual Parity", (168, 85, 247)),
        ("$21k", "Patrimonio Est." if lang == "es" else "Asset Equity", (16, 185, 129)),
        ("0 ms", "Toil Editorial" if lang == "es" else "Editorial Toil", (251, 191, 36))
    ]

    kw = (scope_w - 8) // 2
    kh = 58
    for idx, (val, lbl, col) in enumerate(kpis):
        kx = c3_x1 + 12 + (idx % 2) * (kw + 8)
        ky = kpi_grid_y + (idx // 2) * (kh + 8)
        draw.rounded_rectangle([kx, ky, kx + kw, ky + kh], radius=6, fill=(11, 17, 32, 255), outline=(col[0], col[1], col[2], 120), width=1)
        draw.text((kx + 10, ky + 6), val, font=font_kpi_val, fill=(col[0], col[1], col[2], 255))
        draw.text((kx + 10, ky + 34), lbl, font=font_kpi_lbl, fill=(148, 163, 184, 255))

    # Estado y Stack Pro
    cap_y = kpi_grid_y + (kh * 2) + 24
    draw.rounded_rectangle([c3_x1 + 12, cap_y, c3_x2 - 12, cap_y + 64], radius=6, fill=(8, 13, 26, 255), outline=(51, 65, 85, 180), width=1)
    draw.ellipse([c3_x1 + 20, cap_y + 11, c3_x1 + 26, cap_y + 17], fill=(52, 211, 153, 255))
    draw.text((c3_x1 + 32, cap_y + 7), "Estado: Operativo & Sincronizado" if lang == "es" else "Status: Fully Synchronized", font=font_mono_bold, fill=(52, 211, 153, 255))
    draw.text((c3_x1 + 20, cap_y + 26), "React 19 Executive UI - Dark Mode\nSupabase Cloud Pro + Row Level Security", font=font_card_sub, fill=(148, 163, 184, 240))

    # =========================================================================
    # 8. CINTA INFERIOR DE BADGES TECNOLÓGICOS (FOOTER RIBBON)
    # =========================================================================
    ribbon_y = 578
    bottom_badges = [
        ("Git as Single Source of Truth", (16, 185, 129)),
        ("Pydantic v2 Fail-Closed", (6, 182, 212)),
        ("100% Paridad Bilingüe", (168, 85, 247)),
        ("CI/CD GitHub Actions", (56, 189, 248)),
        ("React 19 Executive Cockpit", (245, 158, 11)),
    ] if lang == "es" else [
        ("Git as Single Source of Truth", (16, 185, 129)),
        ("Pydantic v2 Fail-Closed", (6, 182, 212)),
        ("100% Bilingual Parity", (168, 85, 247)),
        ("CI/CD GitHub Actions", (56, 189, 248)),
        ("React 19 Executive Cockpit", (245, 158, 11)),
    ]

    rx = 45
    for b_text, color in bottom_badges:
        b_w = len(b_text) * 7 + 22
        draw.rounded_rectangle(
            [rx, ribbon_y, rx + b_w, ribbon_y + 26],
            radius=4,
            fill=(15, 23, 42, 255),
            outline=(color[0], color[1], color[2], 140),
            width=1
        )
        draw.ellipse([rx + 8, ribbon_y + 10, rx + 14, ribbon_y + 16], fill=(color[0], color[1], color[2], 255))
        draw.text((rx + 19, ribbon_y + 5), b_text, font=font_series, fill=(226, 232, 240, 255))
        rx += b_w + 14

    return img.convert("RGB")


def main():
    print("[*] Generando portadas conceptuales ilustradas de Datalaria Pulse...")
    
    # 1. Portada Ilustrada del Post 1 (1200 x 630 px) para ES y EN
    p1_es_path = "content/es/posts/pulse-parte1-adios-notion-content-ops/cover.png"
    post_cover_es = create_post1_cover(lang="es")
    post_cover_es.save(p1_es_path, format="PNG", quality=95)
    print(f"  [OK] Post 1 ES: {p1_es_path} (1200x630)")

    p1_en_path = "content/en/posts/pulse-part1-goodbye-notion-content-ops/cover.png"
    post_cover_en = create_post1_cover(lang="en")
    post_cover_en.save(p1_en_path, format="PNG", quality=95)
    print(f"  [OK] Post 1 EN: {p1_en_path} (1200x630)")

    print("[DONE] Portadas ilustradas generadas con éxito.")

if __name__ == "__main__":
    main()
