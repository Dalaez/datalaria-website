#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera programáticamente la imagen de portada cover.png de alta resolución
(1200 x 630 px, proporción 1.91:1) optimizada con ZONA SEGURA (Safe Zone)
para visualización perfecta tanto en página completa como en tarjetas de blog
(aspect ratio 16:9 y 3:2, sin recortes en títulos, matriz ni viñetas):
- content/es/posts/matriz-bcg-dinamica/cover.png
- content/en/posts/dynamic-bcg-matrix/cover.png

Composición visual de estándar McKinsey / BCG:
- Fondo: Degradado Dark Slate / Navy (#0B1120 a #0F172A y #1E293B) con malla técnica.
- Safe Zone: Todo el contenido crítico está enmarcado entre X: 145px y 1055px (zona segura central de 910px),
  garantizando que ninguna tarjeta de lista de posts o vista previa social recorte letras ni nodos.
- Badge superior corporativo Datalaria con borde azul consultoría (#2563EB).
- Título principal de alto impacto visual en blanco y oro ámbar (#F59E0B).
- Subtítulo ejecutivo y balas de valor estratégico.
- Elemento gráfico central derecho: Matriz cartesiana BCG de 4 cuadrantes balanceada con burbujas de UENs.
- Píldoras de entregables: [📊 Excel + Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF].
"""

import os
import math
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


def draw_bcg_quadrant_graphic(draw, x0, y0, w, h, font_small, font_bold, lang='ES'):
    """
    Dibuja la matriz cartesiana BCG perfectamente encuadrada dentro de la Zona Segura,
    con los 4 cuadrantes estilizados, burbujas proporcionales y balance de Henderson.
    """
    mid_x = x0 + w // 2
    mid_y = y0 + h // 2

    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=10, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 4 Cuadrantes con fondos temáticos sutiles
    # Q1 (Top-Left): Interrogantes
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (mid_x - 2, mid_y - 2)], radius=7, fill=(35, 30, 20))
    # Q2 (Top-Right): Estrellas
    draw.rounded_rectangle([(mid_x + 2, y0 + 4), (x0 + w - 4, mid_y - 2)], radius=7, fill=(18, 32, 54))
    # Q3 (Bottom-Left): Perros
    draw.rounded_rectangle([(x0 + 4, mid_y + 2), (mid_x - 2, y0 + h - 4)], radius=7, fill=(38, 20, 26))
    # Q4 (Bottom-Right): Vacas Lecheras
    draw.rounded_rectangle([(mid_x + 2, mid_y + 2), (x0 + w - 4, y0 + h - 4)], radius=7, fill=(16, 36, 36))

    # Ejes cartesianos divisorios en azul consultoría
    draw.line([(mid_x, y0 + 6), (mid_x, y0 + h - 6)], fill=(56, 189, 248), width=2)
    draw.line([(x0 + 6, mid_y), (x0 + w - 6, mid_y)], fill=(56, 189, 248), width=2)

    # Etiquetas breves de cuadrante
    lbl_stars = "⭐ ESTRELLAS" if lang == 'ES' else "⭐ STARS"
    lbl_cows = "🐄 VACAS" if lang == 'ES' else "🐄 CASH COWS"
    lbl_quest = "❓ INTERROG." if lang == 'ES' else "❓ QUESTIONS"
    lbl_dogs = "🐕 PERROS" if lang == 'ES' else "🐕 DOGS"

    draw.text((mid_x + 10, y0 + 10), lbl_stars, fill=(147, 197, 253), font=font_bold)
    draw.text((mid_x + 10, y0 + 26), "Invertir" if lang == 'ES' else "Invest", fill=(96, 165, 250), font=font_small)

    draw.text((x0 + 10, y0 + 10), lbl_quest, fill=(253, 230, 138), font=font_bold)
    draw.text((x0 + 10, y0 + 26), "Decidir" if lang == 'ES' else "Decide", fill=(245, 158, 11), font=font_small)

    draw.text((x0 + 10, mid_y + 10), lbl_dogs, fill=(254, 205, 211), font=font_bold)
    draw.text((x0 + 10, mid_y + 26), "Desinvertir" if lang == 'ES' else "Divest", fill=(244, 63, 94), font=font_small)

    draw.text((mid_x + 10, mid_y + 10), lbl_cows, fill=(153, 246, 228), font=font_bold)
    draw.text((mid_x + 10, mid_y + 26), "Ordeñar (FCF)" if lang == 'ES' else "Milk (FCF)", fill=(20, 184, 166), font=font_small)

    # Burbujas de UENs principales encuadradas
    # Estrellas: Robótica IA (18.5M€) y SaaS IoT (12.2M€)
    bx_s1, by_s1, br_s1 = mid_x + 75, mid_y - 65, 28
    draw.ellipse([(bx_s1 - br_s1, by_s1 - br_s1), (bx_s1 + br_s1, by_s1 + br_s1)], fill=(37, 99, 235), outline=(96, 165, 250), width=2)
    draw.text((bx_s1 - 20, by_s1 - 6), "18.5M€" if lang == 'ES' else "$18.5M", fill=(255, 255, 255), font=font_small)

    bx_s2, by_s2, br_s2 = mid_x + 130, mid_y - 105, 20
    draw.ellipse([(bx_s2 - br_s2, by_s2 - br_s2), (bx_s2 + br_s2, by_s2 + br_s2)], fill=(59, 130, 246), outline=(147, 197, 253), width=2)
    draw.text((bx_s2 - 16, by_s2 - 5), "12.2M" if lang == 'ES' else "$12.2M", fill=(255, 255, 255), font=font_small)

    # Vacas: Hidráulicos (32M€) y Motores (24.5M€)
    bx_c1, by_c1, br_c1 = mid_x + 105, mid_y + 80, 38
    draw.ellipse([(bx_c1 - br_c1, by_c1 - br_c1), (bx_c1 + br_c1, by_c1 + br_c1)], fill=(13, 148, 136), outline=(94, 234, 212), width=2)
    draw.text((bx_c1 - 22, by_c1 - 12), "32.0M€" if lang == 'ES' else "$32.0M", fill=(255, 255, 255), font=font_bold)
    draw.text((bx_c1 - 22, by_c1 + 2), "+4.8M FCF", fill=(204, 251, 241), font=font_small)

    bx_c2, by_c2, br_c2 = mid_x + 48, mid_y + 110, 28
    draw.ellipse([(bx_c2 - br_c2, by_c2 - br_c2), (bx_c2 + br_c2, by_c2 + br_c2)], fill=(20, 184, 166), outline=(153, 246, 228), width=2)
    draw.text((bx_c2 - 18, by_c2 - 6), "24.5M" if lang == 'ES' else "$24.5M", fill=(255, 255, 255), font=font_small)

    # Interrogantes: Baterías (6.5M€) y Láser (3.8M€)
    bx_q1, by_q1, br_q1 = mid_x - 70, mid_y - 90, 18
    draw.ellipse([(bx_q1 - br_q1, by_q1 - br_q1), (bx_q1 + br_q1, by_q1 + br_q1)], fill=(217, 119, 6), outline=(253, 230, 138), width=2)
    draw.text((bx_q1 - 15, by_q1 - 5), "6.5M" if lang == 'ES' else "$6.5M", fill=(255, 255, 255), font=font_small)

    bx_q2, by_q2, br_q2 = mid_x - 115, mid_y - 50, 13
    draw.ellipse([(bx_q2 - br_q2, by_q2 - br_q2), (bx_q2 + br_q2, by_q2 + br_q2)], fill=(245, 158, 11), outline=(254, 243, 199), width=2)

    # Perros: Cableado (5.2M€) y Válvulas (4.3M€)
    bx_d1, by_d1, br_d1 = mid_x - 70, mid_y + 70, 15
    draw.ellipse([(bx_d1 - br_d1, by_d1 - br_d1), (bx_d1 + br_d1, by_d1 + br_d1)], fill=(225, 29, 72), outline=(254, 205, 211), width=2)
    draw.text((bx_d1 - 14, by_d1 - 5), "5.2M" if lang == 'ES' else "$5.2M", fill=(255, 255, 255), font=font_small)

    bx_d2, by_d2, br_d2 = mid_x - 118, mid_y + 100, 13
    draw.ellipse([(bx_d2 - br_d2, by_d2 - br_d2), (bx_d2 + br_d2, by_d2 + br_d2)], fill=(190, 18, 60), outline=(254, 205, 211), width=2)

    # Vector Curvado de Flujo de Fondos (Vacas -> Interrogantes)
    draw.arc([(mid_x - 100, mid_y - 120), (mid_x + 100, mid_y + 120)], start=160, end=340, fill=(245, 158, 11), width=2)

    # Badge Central de Balance de Fondos Henderson
    badge_w, badge_h = 210, 32
    bx1 = mid_x - badge_w // 2
    by1 = y0 + h - 38
    draw.rounded_rectangle([(bx1, by1), (bx1 + badge_w, by1 + badge_h)], radius=16, fill=(15, 23, 42), outline=(245, 158, 11), width=1)
    lbl_bal = "BALANCE HENDERSON: +5,29 M€" if lang == 'ES' else "HENDERSON BALANCE: +$5.29M"
    bbox_bal = font_bold.getbbox(lbl_bal)
    w_bal = bbox_bal[2] - bbox_bal[0]
    draw.text((mid_x - w_bal // 2, by1 + 7), lbl_bal, fill=(255, 255, 255), font=font_bold)


def create_cover(lang='ES', out_path='cover.png'):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado Dark Slate
    draw_linear_gradient(draw, WIDTH, HEIGHT, (11, 17, 32), (30, 41, 59))

    # 2. Malla técnica
    draw_technical_grid(draw, WIDTH, HEIGHT)

    # Fuentes ajustadas proporcionalmente
    font_kicker = get_font("segoeuib.ttf", 11)
    font_title_large = get_font("segoeuib.ttf", 35)
    font_subtitle = get_font("segoeui.ttf", 14)
    font_body = get_font("segoeui.ttf", 11)
    font_bold = get_font("segoeuib.ttf", 12)
    font_small = get_font("segoeui.ttf", 9)
    font_pill = get_font("segoeuib.ttf", 11)

    # MARGEN SEGURO IZQUIERDO Y DERECHO (Safe Zone [145, 1055])
    safe_left = 145
    safe_right = 1055

    # 3. Badge Superior Corporativo
    badge_text = "DATALARIA EXECUTIVE DECISION PACK • MCKINSEY & BCG STANDARD"
    b_x, b_y = safe_left, 52
    b_w, b_h = 445, 26
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=5, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text((b_x + 14, b_y + 6), badge_text, fill=(56, 189, 248), font=font_kicker)

    # 4. Título Principal
    t_y = 92
    title_p1 = "MATRIZ BCG " if lang == 'ES' else "DYNAMIC BCG "
    title_p2 = "DINÁMICA" if lang == 'ES' else "MATRIX"

    draw.text((safe_left, t_y), title_p1, fill=(255, 255, 255), font=font_title_large)
    bbox_p1 = font_title_large.getbbox(title_p1)
    p1_width = bbox_p1[2] - bbox_p1[0]
    draw.text((safe_left + p1_width, t_y), title_p2, fill=(245, 158, 11), font=font_title_large)

    # 5. Subtítulo
    sub_y = 146
    subtitle = (
        "Gestión de Cartera, Curva de Experiencia & Asignación de Capital"
        if lang == 'ES' else
        "Portfolio Management, Experience Curve & C-Level Capital Allocation"
    )
    draw.text((safe_left, sub_y), subtitle, fill=(203, 213, 225), font=font_subtitle)

    # Línea decorativa horizontal
    draw.line([(safe_left, 176), (620, 176)], fill=(37, 99, 235), width=2)

    # 6. Balas de valor estratégico
    bullets = [
        ("Cálculo Matemático de Cuota Relativa (CMR)", "Normalización objetiva frente al líder competidor y curva de experiencia") if lang == 'ES' else
        ("Mathematical Relative Share (RMS) Engine", "Objective benchmark vs. nearest rival and scale learning curve"),

        ("Balance de Liquidez de Bruce Henderson", "Modelo dinámico de flujos de fondos: superávit de Vacas financia Interrogantes") if lang == 'ES' else
        ("Bruce Henderson Cash Flow Balance", "Dynamic fund flow model: Cash Cow surplus finances scalable Question Marks"),

        ("Roadmap de Capital & Resoluciones de Consejo", "Reasignación presupuestaria Q1-Q4 con Owner C-Level y retorno en ROIC") if lang == 'ES' else
        ("Capital Roadmap & Board Decision Gateway", "Q1-Q4 reallocation timeline with C-Suite owners and ROIC accretion")
    ]

    bullet_y = 196
    for b_title, b_desc in bullets:
        draw.rounded_rectangle([(safe_left, bullet_y + 3), (safe_left + 7, bullet_y + 10)], radius=2, fill=(37, 99, 235))
        draw.text((safe_left + 16, bullet_y), b_title, fill=(255, 255, 255), font=font_bold)
        draw.text((safe_left + 16, bullet_y + 17), b_desc, fill=(148, 163, 184), font=font_body)
        bullet_y += 48

    # 7. Píldoras de Entregables (Bottom Left)
    pills = [
        ("📊 Excel + Sheets", (37, 99, 235)),
        ("📑 PPTX 16:9 C-Level", (217, 119, 6)),
        ("📄 Guía PDF (5 págs)" if lang == 'ES' else "📄 PDF Guide (5 pgs)", (13, 148, 136))
    ]

    pill_x = safe_left
    pill_y = 358
    for p_txt, p_border in pills:
        bbox = font_pill.getbbox(p_txt)
        pw = (bbox[2] - bbox[0]) + 24
        ph = 30
        draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pw, pill_y + ph)], radius=15, fill=(15, 23, 42), outline=p_border, width=1)
        draw.text((pill_x + 12, pill_y + 7), p_txt, fill=(255, 255, 255), font=font_pill)
        pill_x += pw + 10

    # 8. Barra inferior de pie enmarcada en Safe Zone
    draw.line([(safe_left, 545), (safe_right, 545)], fill=(51, 65, 85), width=1)
    foot_left = "Datalaria.com • Official Executive Decision Pack 2026 • Confidential & Licensed"
    foot_right = "Descarga Directa Inmediata (.ZIP)" if lang == 'ES' else "Instant Direct Download (.ZIP)"
    draw.text((safe_left, 558), foot_left, fill=(100, 116, 139), font=font_small)
    bbox_fr = font_small.getbbox(foot_right)
    draw.text((safe_right - (bbox_fr[2] - bbox_fr[0]), 558), foot_right, fill=(56, 189, 248), font=font_small)

    # 9. Elemento Gráfico Central: Matriz Cartesiana BCG (encuadrada entre X: 645 y 1045)
    chart_x = 645
    chart_y = 75
    chart_w = 405
    chart_h = 425
    draw_bcg_quadrant_graphic(draw, chart_x, chart_y, chart_w, chart_h, font_small, font_bold, lang=lang)

    # Guardar imagen en disco
    img.save(out_path, format="PNG", optimize=True)
    print(f"[OK] Portada generada ({lang}): {out_path} ({os.path.getsize(out_path)} bytes)")


def main():
    path_es = os.path.join("content", "es", "posts", "matriz-bcg-dinamica", "cover.png")
    path_en = os.path.join("content", "en", "posts", "dynamic-bcg-matrix", "cover.png")

    create_cover(lang='ES', out_path=path_es)
    create_cover(lang='EN', out_path=path_en)


if __name__ == "__main__":
    main()
