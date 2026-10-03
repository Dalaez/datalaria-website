#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/matriz-dar-cuantitativa/cover.png
- content/en/posts/quantitative-dar-matrix/cover.png

Composición visual de estándar McKinsey / BCG / CMMI:
- Fondo: Degradado Dark Navy (#0F172A a #1E293B) con malla técnica sutil.
- Badge superior: "SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN • CMMI & KEPNER-TREGOE STANDARD"
- Título principal: "MATRIZ DAR CUANTITATIVA" / "QUANTITATIVE DAR MATRIX"
- Subtítulo: "Decision Analysis & Resolution, Criterios Veto & Ponderación Multicriterio C-Level"
- Gráfico abstracto lateral: Embudo de decisión con filtros veto (rojo/verde) y barras de scoring ponderado.
- Píldoras de entregables: [📊 Excel + Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF].
- Marca de agua / Logo inferior derecho: "DATALARIA.COM · EXECUTIVE DECISION PACKS".
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


def draw_dar_decision_graphic(draw, x0, y0, w, h, font_small, font_bold, lang='ES'):
    """
    Dibuja el motor gráfico DAR:
    - Embudo superior: Filtros Veto (Must-Haves) con nodos verdes y un nodo rojo descalificado.
    - Bloque intermedio: Scoring Ponderado (Barras de puntuación).
    - Bloque inferior: Alternativa Adjudicataria destacada en verde esmeralda.
    """
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR DE DECISIÓN CMMI DAR" if lang == 'ES' else "CMMI DAR DECISION ENGINE"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(245, 158, 11), font=font_bold)
    sub_panel = "Vk (VETO) × ∑(wj · sj)" if lang == 'ES' else "Vk (GATE) × ∑(wj · sj)"
    draw.text((x0 + w - 170, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. SECCIÓN A: FILTRO VETO GATEKEEPER
    y_veto = y0 + 52
    lbl_veto = "1. FILTROS VETO (MUST-HAVES)" if lang == 'ES' else "1. VETO CRITERIA (MUST-HAVES)"
    draw.text((x0 + 16, y_veto), lbl_veto, fill=(56, 189, 248), font=font_bold)

    # 5 Nodos de alternativas
    alt_nodes = [
        ("Alt A", True, (16, 185, 129)),
        ("Alt B", True, (16, 185, 129)),
        ("Alt C", True, (16, 185, 129)),
        ("Alt D", False, (239, 68, 68)), # VETO!
        ("Alt E", True, (16, 185, 129)),
    ]

    node_w = 78
    node_h = 36
    node_spacing = 14
    start_nx = x0 + 16

    for i, (name, passes, col) in enumerate(alt_nodes):
        nx = start_nx + i * (node_w + node_spacing)
        ny = y_veto + 22
        bg_col = (16, 40, 32) if passes else (48, 20, 24)
        border_col = col
        draw.rounded_rectangle([(nx, ny), (nx + node_w, ny + node_h)], radius=6, fill=bg_col, outline=border_col, width=2)
        
        draw.text((nx + 10, ny + 6), name, fill=(241, 245, 249), font=font_bold)
        status_txt = "✓ APTA" if (passes and lang == 'ES') else ("✓ PASS" if passes else ("✕ VETO" if lang == 'ES' else "✕ FAIL"))
        draw.text((nx + 10, ny + 20), status_txt, fill=col, font=font_small)

    # Línea divisoria
    draw.line([(x0 + 16, y_veto + 72), (x0 + w - 16, y_veto + 72)], fill=(51, 65, 85), width=1)

    # 3. SECCIÓN B: SCORING MULTICRITERIO PONDERADO (BARRAS)
    y_sc = y_veto + 82
    lbl_sc = "2. SCORING PONDERADO (WANTS) [0 - 100 PTS]" if lang == 'ES' else "2. WEIGHTED SCORING (WANTS) [0 - 100 PTS]"
    draw.text((x0 + 16, y_sc), lbl_sc, fill=(56, 189, 248), font=font_bold)

    bars_data = [
        ("Vendor Beta", 86.4, (16, 185, 129), True),
        ("Vendor Alpha", 78.6, (59, 130, 246), False),
        ("Vendor Gamma", 76.6, (148, 163, 184), False),
        ("Vendor Epsilon", 71.8, (100, 116, 139), False),
        ("Vendor Delta", 0.0, (239, 68, 68), False), # Disqualified
    ]

    bar_start_y = y_sc + 22
    max_bar_w = 260

    for i, (b_name, b_val, b_col, is_win) in enumerate(bars_data):
        by = bar_start_y + i * 34
        # Label
        draw.text((x0 + 16, by + 4), b_name, fill=(255, 255, 255) if is_win else (203, 213, 225), font=font_bold if is_win else font_small)
        
        # Bar track
        bx0 = x0 + 130
        bx_end = bx0 + max_bar_w
        draw.rounded_rectangle([(bx0, by + 4), (bx_end, by + 20)], radius=4, fill=(30, 41, 59))

        # Filled bar
        filled_w = int((b_val / 100.0) * max_bar_w) if b_val > 0 else 6
        if b_val > 0:
            draw.rounded_rectangle([(bx0, by + 4), (bx0 + filled_w, by + 20)], radius=4, fill=b_col)
            draw.text((bx0 + filled_w + 10, by + 4), f"{b_val:.1f} pts", fill=b_col, font=font_bold)
        else:
            draw.rounded_rectangle([(bx0, by + 4), (bx0 + filled_w, by + 20)], radius=4, fill=b_col)
            draw.text((bx0 + filled_w + 10, by + 4), "0.0 (VETO)" if lang == 'ES' else "0.0 (VETO)", fill=b_col, font=font_bold)

    # Línea divisoria
    draw.line([(x0 + 16, bar_start_y + 176), (x0 + w - 16, bar_start_y + 176)], fill=(51, 65, 85), width=1)

    # 4. SECCIÓN C: VEREDICTO C-LEVEL ADJUDICACIÓN
    y_win = bar_start_y + 188
    draw.rounded_rectangle([(x0 + 16, y_win), (x0 + w - 16, y_win + 54)], radius=8, fill=(16, 46, 36), outline=(16, 185, 129), width=2)
    
    win_title = "🏆 ADJUDICATARIA: VENDOR BETA (86,4 / 100)" if lang == 'ES' else "🏆 AWARD RECIPIENT: VENDOR BETA (86.4 / 100)"
    draw.text((x0 + 30, y_win + 10), win_title, fill=(209, 250, 229), font=font_bold)
    
    win_sub = "Ahorro TCO: -19% acumulado a 3 años | SLA < 2h | Pleno Compliance UE" if lang == 'ES' else "TCO Advantage: -19% across 36M | SLA < 2h | 100% EU GDPR Adherence"
    draw.text((x0 + 30, y_win + 30), win_sub, fill=(110, 231, 183), font=font_small)


def generate_cover_image(lang='ES', out_path=None):
    if out_path is None:
        if lang == 'ES':
            out_path = "content/es/posts/matriz-dar-cuantitativa/cover.png"
        else:
            out_path = "content/en/posts/quantitative-dar-matrix/cover.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo Degradado y Malla Técnica
    draw_linear_gradient(draw, WIDTH, HEIGHT, (11, 17, 32), (30, 41, 59))
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes
    font_badge = get_font("segoeuib.ttf", 15)
    font_title = get_font("segoeuib.ttf", 46)
    font_sub = get_font("segoeuib.ttf", 20)
    font_desc = get_font("segoeui.ttf", 15)
    font_pill = get_font("segoeuib.ttf", 14)
    font_meta = get_font("segoeui.ttf", 13)
    font_bold_sm = get_font("segoeuib.ttf", 13)
    font_sm = get_font("segoeui.ttf", 12)

    # 2. Badge Superior Izquierdo
    badge_x = 70
    badge_y = 65
    badge_text = ("SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN • CMMI & KEPNER-TREGOE"
                  if lang == 'ES' else
                  "SUITE 02 · DECISION ANALYSIS & RESOLUTION • CMMI & KEPNER-TREGOE")
    
    badge_w = 540 if lang == 'ES' else 525
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + 32)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235), width=2)
    draw.text((badge_x + 14, badge_y + 7), badge_text, fill=(245, 158, 11), font=font_badge)

    # 3. Título Principal
    title_y = 115
    if lang == 'ES':
        draw.text((70, title_y), "MATRIZ DAR", fill=(255, 255, 255), font=font_title)
        draw.text((70, title_y + 54), "CUANTITATIVA", fill=(56, 189, 248), font=font_title)
    else:
        draw.text((70, title_y), "QUANTITATIVE", fill=(255, 255, 255), font=font_title)
        draw.text((70, title_y + 54), "DAR MATRIX", fill=(56, 189, 248), font=font_title)

    # 4. Subtítulo y Descripción
    sub_y = title_y + 120
    sub_text = ("Decision Analysis & Resolution, Criterios Veto" if lang == 'ES' else "Decision Analysis & Resolution, Veto Criteria")
    sub_text2 = ("& Ponderación Multicriterio C-Level" if lang == 'ES' else "& Multi-Criteria Scoring for Corporate Boards")
    draw.text((70, sub_y), sub_text, fill=(245, 158, 11), font=font_sub)
    draw.text((70, sub_y + 26), sub_text2, fill=(245, 158, 11), font=font_sub)

    desc_y = sub_y + 64
    bullets_es = [
        "• Filtro Veto Booleano (Must-Haves): Descalificación fulminante",
        "• Matriz de 13 Criterios Ponderados en 4 Pilares de Decisión",
        "• Análisis de Sensibilidad Marginal What-If (+/- 20% Coste/Técnico)",
        "• Presentación 16:9 con Board Decision Gateway y Firmas C-Level"
    ]
    bullets_en = [
        "• Non-Negotiable Boolean Veto Filter (Must-Haves Gatekeeper)",
        "• 13 Weighted Criteria Matrix Structured in 4 Strategic Pillars",
        "• Marginal What-If Sensitivity Test (+/- 20% Cost/Technical Fit)",
        "• 16:9 Boardroom Deck with Governance Gateway & C-Suite Sign-off"
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

    # 6. Marca de Agua / Footer Izquierdo
    draw.text((70, 580), "DATALARIA.COM · EXECUTIVE DECISION PACKS · STANDARD TIER-1", fill=(100, 116, 139), font=font_meta)

    # 7. GRÁFICO ABSTRACTO LATERAL (DERECHA)
    gx = 670
    gy = 75
    gw = 470
    gh = 475
    draw_dar_decision_graphic(draw, gx, gy, gw, gh, font_sm, font_bold_sm, lang=lang)

    # Guardar imagen PNG de alta fidelidad
    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Portada generada ({lang}): {out_path}")
    return out_path


def main():
    print("Iniciando generación de portadas visuales cover.png...")
    es_path = generate_cover_image(lang='ES')
    en_path = generate_cover_image(lang='EN')
    print("Portadas generadas exitosamente.")


if __name__ == "__main__":
    main()
