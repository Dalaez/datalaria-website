#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/matriz-rice-ice-priorizacion/cover.png
- content/en/posts/rice-ice-prioritization-matrix/cover.png

Composición visual de estándar McKinsey / BCG / Intercom:
- Fondo: Degradado Dark Navy (#0F172A a #1E293B) con malla técnica sutil.
- Badge superior: "SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN • INTERCOM RICE & GROWTH ICE STANDARD"
- Título principal: "MATRIZ RICE & ICE" / "RICE & ICE MATRIX"
- Subtítulo: "Priorización Ágil de Backlog, Matriz Impacto/Esfuerzo & Línea de Corte de Capacidad"
- Gráfico abstracto lateral: Cuadrícula 2x2 Impacto/Esfuerzo con cuadrantes (Quick Wins, Big Bets, Fill-ins, Money Pits),
  línea de corte de capacidad y tarjeta de iniciativa líder.
- Píldoras de entregables: [📊 Excel + Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF Minto].
- Marca de agua: "DATALARIA.COM · EXECUTIVE DECISION PACKS · STANDARD TIER-1".
"""

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 630


def get_font(name, size):
    """Carga fuente TrueType del sistema o fallback predeterminado."""
    font_paths = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
        f"C:/Windows/Fonts/{name.replace('b', '')}",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_linear_gradient(draw, width, height, start_color, end_color):
    """Pinta un degradado diagonal suave en la imagen."""
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    for y in range(height):
        ratio_y = y / height
        for x in range(0, width, 2):
            ratio_x = x / width
            blend = (ratio_x * 0.4 + ratio_y * 0.6)
            r = int(r1 + (r2 - r1) * blend)
            g = int(g1 + (g2 - g1) * blend)
            b = int(b1 + (b2 - b1) * blend)
            draw.line([(x, y), (x + 1, y)], fill=(r, g, b))


def draw_technical_grid(draw, width, height):
    """Dibuja una malla técnica con cuadrículas y puntos sutiles."""
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48), width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_rice_matrix_graphic(draw, x0, y0, w, h, font_small, font_bold, lang='ES'):
    """
    Dibuja el motor analítico RICE & ICE en el panel lateral derecho:
    - Cabecera del panel.
    - Cuadrantes 2x2 Impacto vs Esfuerzo (Quick Wins verde, Big Bets azul, Fill-ins gris, Money Pits rojo).
    - Línea discontinua ámbar de corte de capacidad.
    - Veredicto de iniciativa #1 y capacidad liberada.
    """
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR DE PRIORIZACIÓN RICE & ICE" if lang == 'ES' else "RICE & ICE PRIORITIZATION ENGINE"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(245, 158, 11), font=font_bold)
    sub_panel = "(R·I·C)/E  &  I·C·E"
    draw.text((x0 + w - 140, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. MATRIZ 2x2 IMPACTO VS ESFUERZO
    y_mat = y0 + 50
    mat_w = w - 32
    mat_h = 240
    mx0 = x0 + 16
    my0 = y_mat

    # Cuadrantes
    half_w = mat_w // 2
    half_h = mat_h // 2

    # Q2: Quick Wins (Top-Left) -> Verde
    draw.rounded_rectangle([(mx0, my0), (mx0 + half_w - 4, my0 + half_h - 4)], radius=6, fill=(16, 42, 32), outline=(16, 185, 129), width=1)
    lbl_qw = "QUICK WINS (54% VALOR)" if lang == 'ES' else "QUICK WINS (54% VALUE)"
    draw.text((mx0 + 10, my0 + 8), lbl_qw, fill=(209, 250, 229), font=font_bold)
    draw.text((mx0 + 10, my0 + 26), "• INIT-18: 2FA Auth (33.3k)", fill=(110, 231, 183), font=font_small)
    draw.text((mx0 + 10, my0 + 44), "• INIT-15: NPS Pulse (25.0k)", fill=(110, 231, 183), font=font_small)
    draw.text((mx0 + 10, my0 + 62), "• INIT-03: Exporter (22.0k)", fill=(110, 231, 183), font=font_small)
    draw.text((mx0 + 10, my0 + 80), "• INIT-05: Onboarding (20.0k)", fill=(110, 231, 183), font=font_small)

    # Q1: Grandes Apuestas (Top-Right) -> Azul
    draw.rounded_rectangle([(mx0 + half_w + 4, my0), (mx0 + mat_w, my0 + half_h - 4)], radius=6, fill=(20, 35, 60), outline=(37, 99, 235), width=1)
    lbl_bb = "GRANDES APUESTAS" if lang == 'ES' else "STRATEGIC BIG BETS"
    draw.text((mx0 + half_w + 14, my0 + 8), lbl_bb, fill=(224, 238, 255), font=font_bold)
    draw.text((mx0 + half_w + 14, my0 + 26), "• INIT-02: AI Copilot (7.2k)", fill=(147, 197, 253), font=font_small)
    draw.text((mx0 + half_w + 14, my0 + 44), "• INIT-04: Custom BI (3.5k)", fill=(147, 197, 253), font=font_small)
    draw.text((mx0 + half_w + 14, my0 + 62), "• INIT-11: RBAC Teams (3.7k)", fill=(147, 197, 253), font=font_small)
    draw.text((mx0 + half_w + 14, my0 + 80), "Horizonte Q2-Q3 Planned", fill=(147, 197, 253), font=font_small)

    # Q3: Rellenos / Fill-ins (Bottom-Left) -> Gris
    draw.rounded_rectangle([(mx0, my0 + half_h + 4), (mx0 + half_w - 4, my0 + mat_h)], radius=6, fill=(24, 32, 47), outline=(100, 116, 139), width=1)
    lbl_fi = "RELLENOS (FILL-INS)" if lang == 'ES' else "FILL-INS (LOW IMPACT)"
    draw.text((mx0 + 10, my0 + half_h + 10), lbl_fi, fill=(203, 213, 225), font=font_bold)
    draw.text((mx0 + 10, my0 + half_h + 28), "• INIT-10: Dark Mode", fill=(148, 163, 184), font=font_small)
    draw.text((mx0 + 10, my0 + half_h + 46), "• INIT-17: Email Reports", fill=(148, 163, 184), font=font_small)
    draw.text((mx0 + 10, my0 + half_h + 64), "Ejecutar solo con holgura", fill=(148, 163, 184), font=font_small)

    # Q4: Pozos sin Fondo / Money Pits (Bottom-Right) -> Rojo
    draw.rounded_rectangle([(mx0 + half_w + 4, my0 + half_h + 4), (mx0 + mat_w, my0 + mat_h)], radius=6, fill=(45, 18, 22), outline=(239, 68, 68), width=1)
    lbl_mp = "POZOS SIN FONDO" if lang == 'ES' else "MONEY PITS (FREEZE)"
    draw.text((mx0 + half_w + 14, my0 + half_h + 10), lbl_mp, fill=(254, 202, 202), font=font_bold)
    draw.text((mx0 + half_w + 14, my0 + half_h + 28), "• INIT-19: Rust Rewrite (89)", fill=(248, 113, 113), font=font_small)
    draw.text((mx0 + half_w + 14, my0 + half_h + 46), "• INIT-14: GraphQL API (214)", fill=(248, 113, 113), font=font_small)
    draw.text((mx0 + half_w + 14, my0 + half_h + 64), "CONGELAR: Ahorro 21 PM", fill=(248, 113, 113), font=font_small)

    # 3. LÍNEA DE CORTE DE CAPACIDAD (Dashed Amber Badge)
    y_cut = my0 + mat_h + 12
    draw.rounded_rectangle([(mx0, y_cut), (mx0 + mat_w, y_cut + 40)], radius=6, fill=(38, 28, 14), outline=(245, 158, 11), width=1)
    cut_title = "LÍNEA DE CORTE DE CAPACIDAD: 120 PERSONA-MES (Q1-Q4)" if lang == 'ES' else "CAPACITY CUT-LINE CEILING: 120 PERSON-MONTHS (Q1-Q4)"
    draw.text((mx0 + 12, y_cut + 6), cut_title, fill=(253, 230, 138), font=font_bold)
    cut_sub = "Aprobado por Board | Buffer Deuda Técnica 16.7% intocable" if lang == 'ES' else "Approved by Board | 16.7% Technical Debt Buffer Ring-Fenced"
    draw.text((mx0 + 12, y_cut + 22), cut_sub, fill=(245, 158, 11), font=font_small)

    # 4. TARJETA DE VEREDICTO C-LEVEL
    y_win = y_cut + 52
    draw.rounded_rectangle([(mx0, y_win), (mx0 + mat_w, y_win + 58)], radius=8, fill=(16, 46, 36), outline=(16, 185, 129), width=2)
    win_title = "INICIATIVA #1: INIT-18 (SCORE RICE: 33.333,3)" if lang == 'ES' else "PRIORITY #1: INIT-18 (RICE SCORE: 33,333.3)"
    draw.text((mx0 + 14, y_win + 10), win_title, fill=(209, 250, 229), font=font_bold)
    win_sub = "Máxima densidad de valor | 2FA Obligatorio | Esfuerzo: 1.5 PM" if lang == 'ES' else "Highest value density | Mandatory 2FA Security | Effort: 1.5 PM"
    draw.text((mx0 + 14, y_win + 32), win_sub, fill=(110, 231, 183), font=font_small)


def generate_cover_image(lang='ES', out_path=None):
    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/matriz-rice-ice-priorizacion/cover.png"
        else:
            out_path = "content/en/posts/rice-ice-prioritization-matrix/cover.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo Degradado y Malla Técnica
    draw_linear_gradient(draw, WIDTH, HEIGHT, (11, 17, 32), (30, 41, 59))
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes
    font_badge = get_font("segoeuib.ttf", 14)
    font_title = get_font("segoeuib.ttf", 46)
    font_sub = get_font("segoeuib.ttf", 19)
    font_desc = get_font("segoeui.ttf", 14)
    font_pill = get_font("segoeuib.ttf", 14)
    font_meta = get_font("segoeui.ttf", 13)
    font_bold_sm = get_font("segoeuib.ttf", 12)
    font_sm = get_font("segoeui.ttf", 11)

    # 2. Badge Superior Izquierdo
    badge_x = 70
    badge_y = 65
    badge_text = (
        "SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN • INTERCOM RICE & GROWTH ICE"
        if lang == 'ES' else
        "SUITE 02 · DECISION ANALYSIS & PRIORITIZATION • INTERCOM RICE & GROWTH ICE"
    )
    badge_w = 560 if lang == 'ES' else 550
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + 32)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235), width=2)
    draw.text((badge_x + 14, badge_y + 7), badge_text, fill=(245, 158, 11), font=font_badge)

    # 3. Título Principal
    title_y = 115
    if lang == 'ES':
        draw.text((70, title_y), "MATRIZ RICE & ICE", fill=(255, 255, 255), font=font_title)
        draw.text((70, title_y + 54), "PRIORIZACIÓN ÁGIL", fill=(56, 189, 248), font=font_title)
    else:
        draw.text((70, title_y), "RICE & ICE MATRIX", fill=(255, 255, 255), font=font_title)
        draw.text((70, title_y + 54), "AGILE PRIORITIZATION", fill=(56, 189, 248), font=font_title)

    # 4. Subtítulo y Bullets
    sub_y = title_y + 120
    sub_text = (
        "Backlog Cuantitativo, Matriz Impacto vs. Esfuerzo"
        if lang == 'ES' else
        "Quantitative Backlog, Impact vs. Effort Matrix"
    )
    sub_text2 = (
        "& Línea de Corte de Capacidad del Equipo"
        if lang == 'ES' else
        "& Real Team Capacity Cut-Line Framework"
    )
    draw.text((70, sub_y), sub_text, fill=(245, 158, 11), font=font_sub)
    draw.text((70, sub_y + 25), sub_text2, fill=(245, 158, 11), font=font_sub)

    desc_y = sub_y + 64
    bullets_es = [
        "• Motor Cuantitativo RICE: (Reach × Impact × Confidence) / Effort",
        "• Framework ICE Complementario para Experimentos Ágiles de Growth",
        "• Detección Automática de Cuadrantes (Quick Wins vs. Pozos sin Fondo)",
        "• Deck 16:9 con Asignación Now/Next/Later y Firmas del Product Council"
    ]
    bullets_en = [
        "• Quantitative RICE Engine: (Reach × Impact × Confidence) / Effort",
        "• Complementary ICE Framework for Rapid Agile Growth Experiments",
        "• Automated Strategic Quadrants (Quick Wins vs. Costly Money Pits)",
        "• 16:9 Executive Deck with Now/Next/Later Allocation & C-Level Sign-off"
    ]
    bullets = bullets_es if lang == 'ES' else bullets_en

    for idx, b in enumerate(bullets):
        draw.text((70, desc_y + idx * 24), b, fill=(203, 213, 225), font=font_desc)

    # 5. Píldoras de Entregables (Inferior Izquierda)
    pill_y = 515
    pills = [
        ("📊 Excel + Sheets", 150),
        ("📑 PPTX 16:9 C-Level", 175),
        ("📄 Guía PDF Minto", 160)
    ]
    px = 70
    for p_text, p_w in pills:
        draw.rounded_rectangle([(px, pill_y), (px + p_w, pill_y + 36)], radius=18, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
        draw.text((px + 14, pill_y + 9), p_text, fill=(241, 245, 249), font=font_pill)
        px += p_w + 14

    # 6. Footer Izquierdo
    draw.text((70, 580), "DATALARIA.COM · EXECUTIVE DECISION PACKS · STANDARD TIER-1", fill=(100, 116, 139), font=font_meta)

    # 7. GRÁFICO ABSTRACTO LATERAL (DERECHA)
    gx = 670
    gy = 75
    gw = 470
    gh = 475
    draw_rice_matrix_graphic(draw, gx, gy, gw, gh, font_sm, font_bold_sm, lang=lang)

    # Guardar imagen PNG de alta fidelidad
    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Portada generada ({lang}): {out_path}")
    return out_path


def main():
    print("Iniciando generación de portadas visuales cover.png...")
    es_path = generate_cover_image(lang='ES')
    en_path = generate_cover_image(lang='EN')
    print("Portadas generadas exitosamente en ambos idiomas.")


if __name__ == "__main__":
    main()
