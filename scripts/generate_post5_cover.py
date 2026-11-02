#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_post5_cover.py
=======================
Genera la portada oficial para el Post 5 (Cierre de la Serie) de Datalaria Pulse:
- Título: Gestión Editorial para Equipos de Documentación, SEO y Marketing: de Notion a Excel en 5 minutos
  + Capítulo Especial Pro Supabase Cloud & Fábrica Autónoma con IA.
- Dimensiones: 1200 x 630 px (proporción 16:9 / OpenGraph)
- Badge oficial: Onda de pulso azul cyan (#38bdf8) + "5/5" + pill identificadora
- Composición: Arquitectura Dual-Mode y Fábrica de IA (3 columnas con tarjetas ejecutivas estilo Mac:
  1. Kit Excel Standalone & Migrador Notion,
  2. Supabase Cloud PostgreSQL 15 & RLS Multi-Tenant,
  3. Fábrica Editorial Autónoma con Agentes de IA).
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1200
HEIGHT = 630

def draw_pulse_waveform(draw, x: float, y: float, w: float, h: float, color=(56, 189, 248), stroke_width=2):
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

def get_font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_mac_header(draw, x, y, w, title, font_sm, accent_color=(56, 189, 248)):
    # Header bar
    draw.rectangle([x, y, x + w, y + 30], fill=(15, 23, 42, 255))
    draw.line([x, y + 30, x + w, y + 30], fill=(30, 41, 59, 255), width=1)
    # Mac buttons
    draw.ellipse([x + 12, y + 10, x + 20, y + 18], fill=(239, 68, 68))
    draw.ellipse([x + 26, y + 10, x + 34, y + 18], fill=(234, 179, 8))
    draw.ellipse([x + 40, y + 10, x + 48, y + 18], fill=(34, 197, 94))
    # Title
    draw.text((x + 58, y + 7), title, fill=(241, 245, 249), font=font_sm)

def build_post5_cover():
    # 1. Base Canvas Dark Slate
    img = Image.new("RGBA", (WIDTH, HEIGHT), (9, 13, 22, 255))
    draw = ImageDraw.Draw(img)

    # Ambient Glows
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    # Cyan glow top-left
    glow_draw.ellipse([-100, -100, 450, 350], fill=(6, 182, 212, 35))
    # Emerald glow bottom-left
    glow_draw.ellipse([-50, 350, 400, 650], fill=(16, 185, 129, 30))
    # Indigo/Violet glow center-right
    glow_draw.ellipse([700, -50, 1300, 500], fill=(99, 102, 241, 35))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img.paste(glow, (0, 0), glow)
    draw = ImageDraw.Draw(img)

    # Subtle Tech Grid
    for gx in range(0, WIDTH, 40):
        draw.line([(gx, 0), (gx, HEIGHT)], fill=(255, 255, 255, 5), width=1)
    for gy in range(0, HEIGHT, 40):
        draw.line([(0, gy), (WIDTH, gy)], fill=(255, 255, 255, 5), width=1)

    # Fonts
    font_badge_sm = get_font(11, bold=True)
    font_badge_md = get_font(13, bold=True)
    font_title = get_font(13, bold=True)
    font_card_sub = get_font(11, bold=False)
    font_mono_xs = get_font(10, bold=False)
    font_mono_bold = get_font(10, bold=True)
    font_stat_val = get_font(18, bold=True)
    font_stat_lbl = get_font(10, bold=False)

    # -------------------------------------------------------------
    # TOP BADGE & IDENTIFIER (5/5)
    # -------------------------------------------------------------
    badge_x, badge_y = 40, 28
    badge_w, badge_h = 440, 42
    # Frosted pill
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=21,
        fill=(15, 23, 42, 230),
        outline=(56, 189, 248, 180),
        width=1
    )
    # Waveform
    draw_pulse_waveform(draw, badge_x + 14, badge_y + 9, 26, 24, color=(56, 189, 248), stroke_width=2)
    # 5/5 counter badge
    cnt_x = badge_x + 50
    draw.rounded_rectangle([cnt_x, badge_y + 9, cnt_x + 36, badge_y + 33], radius=6, fill=(56, 189, 248, 40), outline=(56, 189, 248, 120), width=1)
    draw.text((cnt_x + 7, badge_y + 13), "5/5", fill=(56, 189, 248), font=font_badge_md)
    # Text Pill
    draw.text((cnt_x + 46, badge_y + 14), "KIT EXCEL • SUPABASE PRO • FÁBRICA IA", fill=(241, 245, 249), font=font_badge_sm)

    # Top Right Badge: Serie Completa
    tr_w, tr_h = 320, 36
    tr_x = WIDTH - 40 - tr_w
    tr_y = 31
    draw.rounded_rectangle([tr_x, tr_y, tr_x + tr_w, tr_y + tr_h], radius=18, fill=(16, 185, 129, 25), outline=(16, 185, 129, 140), width=1)
    draw.ellipse([tr_x + 14, tr_y + 13, tr_x + 24, tr_y + 23], fill=(34, 197, 94))
    draw.text((tr_x + 32, tr_y + 10), "SERIE COMPLETA · LISTO PARA PRODUCCIÓN", fill=(110, 231, 183), font=font_badge_sm)

    # -------------------------------------------------------------
    # 3 MAIN PILLARS (CARDS)
    # -------------------------------------------------------------
    card_w = 352
    card_h = 420
    card_y = 92

    # CARD 1: KIT EXCEL & NOTION (X: 40)
    c1_x = 40
    # Shadow & Card Box
    draw.rounded_rectangle([c1_x, card_y, c1_x + card_w, card_y + card_h], radius=12, fill=(11, 17, 32, 245), outline=(16, 185, 129, 90), width=1)
    draw_mac_header(draw, c1_x, card_y, card_w, "1. Kit Excel Standalone & Notion", font_title, accent_color=(16, 185, 129))

    # Inner Content Card 1
    # Excel Mockup Table
    tbl_x = c1_x + 14
    tbl_y = card_y + 44
    tbl_w = card_w - 28
    draw.rounded_rectangle([tbl_x, tbl_y, tbl_x + tbl_w, tbl_y + 160], radius=8, fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=1)
    
    # Table header
    draw.rectangle([tbl_x, tbl_y, tbl_x + tbl_w, tbl_y + 24], fill=(16, 185, 129, 35))
    draw.line([tbl_x, tbl_y + 24, tbl_x + tbl_w, tbl_y + 24], fill=(16, 185, 129, 80), width=1)
    draw.text((tbl_x + 8, tbl_y + 6), "ID", fill=(110, 231, 183), font=font_mono_bold)
    draw.text((tbl_x + 50, tbl_y + 6), "TÍTULO DEL ARTÍCULO", fill=(110, 231, 183), font=font_mono_bold)
    draw.text((tbl_x + 220, tbl_y + 6), "ESTADO", fill=(110, 231, 183), font=font_mono_bold)
    draw.text((tbl_x + 285, tbl_y + 6), "SEO", fill=(110, 231, 183), font=font_mono_bold)

    # 4 sample rows
    rows_data = [
        ("ART-01", "Adiós Notion: Datalaria...", "Publicado", (34, 197, 94), "100"),
        ("ART-02", "Del Front Matter al...", "Publicado", (34, 197, 94), "100"),
        ("ART-03", "Tabla & Kanban React...", "Publicado", (34, 197, 94), "100"),
        ("ART-04", "GA4 & GSC Automat...", "Publicado", (34, 197, 94), "100"),
        ("ART-05", "Docs & Fábrica IA...", "Revisión", (56, 189, 248), "100"),
    ]
    ry = tbl_y + 28
    for rid, rtitle, rstatus, rcolor, rseo in rows_data:
        draw.text((tbl_x + 8, ry + 2), rid, fill=(148, 163, 184), font=font_mono_xs)
        draw.text((tbl_x + 50, ry + 2), rtitle, fill=(241, 245, 249), font=font_mono_xs)
        # pill status
        draw.rounded_rectangle([tbl_x + 216, ry, tbl_x + 274, ry + 16], radius=4, fill=(rcolor[0], rcolor[1], rcolor[2], 30), outline=(rcolor[0], rcolor[1], rcolor[2], 100), width=1)
        draw.text((tbl_x + 222, ry + 2), rstatus, fill=rcolor, font=font_mono_xs)
        draw.text((tbl_x + 290, ry + 2), rseo, fill=(56, 189, 248), font=font_mono_bold)
        draw.line([tbl_x, ry + 22, tbl_x + tbl_w, ry + 22], fill=(25, 33, 50), width=1)
        ry += 24

    # Card 1 Features Box
    f1_y = tbl_y + 172
    draw.rounded_rectangle([tbl_x, f1_y, tbl_x + tbl_w, f1_y + 170], radius=8, fill=(15, 23, 42, 180), outline=(30, 41, 59, 200), width=1)
    
    features_c1 = [
        ("📊 Plantilla Maestra Excel 2016/365", "Validación celdas, listas y KPIs automáticos"),
        ("⚡ Conector Power Query M", "Ingesta directa de public.json con 1-clic"),
        ("🔄 Migrador Notion en 5 Minutos", "Conversión de export CSV a estándar Pulse"),
        ("💻 Escáner CLI pulse_repo_scanner.py", "Universal, zero-dependencies (Hugo, Next, Astro)")
    ]
    fy = f1_y + 10
    for f_title, f_sub in features_c1:
        draw.text((tbl_x + 10, fy), f_title, fill=(248, 250, 252), font=font_card_sub)
        draw.text((tbl_x + 10, fy + 16), f_sub, fill=(100, 116, 139), font=font_mono_xs)
        fy += 38

    # Bottom Pill Card 1
    draw.rounded_rectangle([tbl_x, card_y + card_h - 28, tbl_x + tbl_w, card_y + card_h - 10], radius=6, fill=(16, 185, 129, 20), outline=(16, 185, 129, 90), width=1)
    draw.text((tbl_x + 36, card_y + card_h - 26), "STANDALONE · LICENCIA PERPETUA · 0 DEPENDENCIAS", fill=(110, 231, 183), font=font_mono_bold)

    # -------------------------------------------------------------
    # CARD 2: SUPABASE CLOUD & RLS (X: 424)
    # -------------------------------------------------------------
    c2_x = 424
    draw.rounded_rectangle([c2_x, card_y, c2_x + card_w, card_y + card_h], radius=12, fill=(11, 17, 32, 245), outline=(56, 189, 248, 90), width=1)
    draw_mac_header(draw, c2_x, card_y, card_w, "2. Supabase Cloud & RLS Multi-Tenant", font_title, accent_color=(56, 189, 248))

    # Inner Content Card 2
    tb2_x = c2_x + 14
    tb2_y = card_y + 44
    tb2_w = card_w - 28

    # PostgreSQL Schema Box
    draw.rounded_rectangle([tb2_x, tb2_y, tb2_x + tb2_w, tb2_y + 100], radius=8, fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=1)
    draw.text((tb2_x + 12, tb2_y + 10), "POSTGRESQL 15 (SUPABASE)", fill=(56, 189, 248), font=font_mono_bold)
    draw.text((tb2_x + tb2_w - 75, tb2_y + 10), "v0.2.0 PRO", fill=(34, 197, 94), font=font_mono_bold)
    
    schema_lines = [
        "schema: pulse | tables: assets, ideas, metrics",
        "RLS POLICY: auth.uid() = user_id (STRICT)",
        "SYNC: Web Client <--> Supabase Realtime (0 ms)"
    ]
    s_y = tb2_y + 32
    for sl in schema_lines:
        draw.text((tb2_x + 12, s_y), "• " + sl, fill=(148, 163, 184), font=font_mono_xs)
        s_y += 20

    # Multi-tenant Isolation Box
    draw.rounded_rectangle([tb2_x, tb2_y + 112, tb2_x + tb2_w, tb2_y + 248], radius=8, fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=1)
    draw.text((tb2_x + 12, tb2_y + 122), "AISLAMIENTO MULTI-TENANT & ROLES", fill=(248, 250, 252), font=font_mono_bold)

    roles = [
        ("👤 Invitados / Demo Mode", "10 activos sintéticos, sandbox sin credenciales", (234, 179, 8)),
        ("🔑 Nuevos Usuarios Auth", "Espacio privado aislado desde cero (RLS)", (56, 189, 248)),
        ("⚡ Master Admins Datalaria", "Sincronización bidireccional con Git repo", (16, 185, 129)),
    ]
    ry2 = tb2_y + 144
    for r_title, r_desc, r_col in roles:
        draw.text((tb2_x + 12, ry2), r_title, fill=r_col, font=font_card_sub)
        draw.text((tb2_x + 12, ry2 + 15), r_desc, fill=(100, 116, 139), font=font_mono_xs)
        ry2 += 34

    # Bottom Pill Card 2
    draw.rounded_rectangle([tb2_x, card_y + card_h - 28, tb2_x + tb2_w, card_y + card_h - 10], radius=6, fill=(56, 189, 248, 20), outline=(56, 189, 248, 90), width=1)
    draw.text((tb2_x + 44, card_y + card_h - 26), "CLOUD COLABORATIVO · AUTH · ROW-LEVEL SECURITY", fill=(125, 211, 252), font=font_mono_bold)

    # -------------------------------------------------------------
    # CARD 3: FÁBRICA EDITORIAL CON IA (X: 808)
    # -------------------------------------------------------------
    c3_x = 808
    draw.rounded_rectangle([c3_x, card_y, c3_x + card_w, card_y + card_h], radius=12, fill=(11, 17, 32, 245), outline=(139, 92, 246, 90), width=1)
    draw_mac_header(draw, c3_x, card_y, card_w, "3. Fábrica Editorial con Agentes IA", font_title, accent_color=(139, 92, 246))

    # Inner Content Card 3 (AI Pipeline)
    tb3_x = c3_x + 14
    tb3_y = card_y + 44
    tb3_w = card_w - 28

    ai_steps = [
        ("1. Idea & Benchmarking", "Agentes investigan brechas SEO y tendencias", (168, 85, 247), "Claude / Argon"),
        ("2. Redacción Guiada por Spec", "Generación Markdown respetando Front Matter", (139, 92, 246), "Pydantic v2"),
        ("3. Verificación Determinista", "CI/CD: Paridad bilingüe ES/EN, linters, links", (59, 130, 246), "Code Exit 0"),
        ("4. Publicación & Telemetría", "Hugo genera 2.750+ páginas y GA4 audita ROI", (16, 185, 129), "GitHub Actions")
    ]

    p_y = tb3_y
    for s_num, s_desc, s_color, s_tag in ai_steps:
        draw.rounded_rectangle([tb3_x, p_y, tb3_x + tb3_w, p_y + 60], radius=6, fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=1)
        # Left color bar
        draw.rectangle([tb3_x, p_y, tb3_x + 4, p_y + 60], fill=s_color)
        draw.text((tb3_x + 12, p_y + 8), s_num, fill=(248, 250, 252), font=font_title)
        draw.text((tb3_x + tb3_w - 90, p_y + 8), s_tag, fill=s_color, font=font_mono_bold)
        draw.text((tb3_x + 12, p_y + 28), s_desc, fill=(148, 163, 184), font=font_mono_xs)
        # Arrow down connecting steps (except last)
        if s_num != ai_steps[-1][0]:
            draw.text((tb3_x + tb3_w // 2 - 4, p_y + 61), "↓", fill=(100, 116, 139), font=font_mono_bold)
        p_y += 74

    # Bottom Pill Card 3
    draw.rounded_rectangle([tb3_x, card_y + card_h - 28, tb3_x + tb3_w, card_y + card_h - 10], radius=6, fill=(139, 92, 246, 20), outline=(139, 92, 246, 90), width=1)
    draw.text((tb3_x + 36, card_y + card_h - 26), "CICLO CONTINUO · SPEC-DRIVEN DEVELOPMENT", fill=(196, 181, 253), font=font_mono_bold)

    # -------------------------------------------------------------
    # BOTTOM EXECUTIVE METRICS BAR
    # -------------------------------------------------------------
    bar_y = 530
    bar_h = 74
    draw.rounded_rectangle([40, bar_y, WIDTH - 40, bar_y + bar_h], radius=10, fill=(11, 17, 32, 250), outline=(56, 189, 248, 90), width=1)

    kpis = [
        ("ARQUITECTURA DUAL-MODE", "Excel Standalone + Supabase Pro", (56, 189, 248)),
        ("INVENTARIO CONSOLIDADO", "140 Activos (113 Posts + 8 Apps)", (16, 185, 129)),
        ("PARIDAD BILINGÜE", "100% Cobertura ES ⇔ EN", (168, 85, 247)),
        ("GOBERNANZA EDITORIAL", "Content Ops as Code en Git", (245, 158, 11)),
    ]

    col_w = (WIDTH - 80) // 4
    for idx, (lbl, val, col) in enumerate(kpis):
        cx = 40 + idx * col_w
        if idx > 0:
            draw.line([cx, bar_y + 12, cx, bar_y + bar_h - 12], fill=(30, 41, 59, 255), width=1)
        draw.text((cx + 20, bar_y + 14), lbl, fill=(148, 163, 184), font=font_stat_lbl)
        draw.text((cx + 20, bar_y + 36), val, fill=col, font=font_title)

    # Save outputs
    es_path = "content/es/posts/pulse-parte5-kit-excel-migracion-notion-equipos/cover.png"
    en_path = "content/en/posts/pulse-part5-excel-kit-notion-migration-teams/cover.png"
    artifact_path = "C:/Users/dalae/.gemini/antigravity/brain/9cc3e8ea-e324-41b5-80e8-6114503cfb4d/cover_post5.png"

    os.makedirs(os.path.dirname(es_path), exist_ok=True)
    os.makedirs(os.path.dirname(en_path), exist_ok=True)

    img.save(es_path, format="PNG", optimize=True)
    shutil.copyfile(es_path, en_path)
    shutil.copyfile(es_path, artifact_path)
    print(f"[OK] Portada Post 5 guardada exitosamente en:")
    print(f"     - {es_path}")
    print(f"     - {en_path}")
    print(f"     - {artifact_path}")

if __name__ == "__main__":
    build_post5_cover()
