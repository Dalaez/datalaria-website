#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py
=================
Genera las imágenes de portada cover.png de alta resolución (1200 x 630 px, proporción 1.91:1) para:
- content/es/posts/calculadora-stock-seguridad-rop/cover.png
- content/en/posts/safety-stock-reorder-point-calculator/cover.png

Composición visual de estándar APICS / ASCM / MIT CTL / McKinsey:
- Fondo: Degradado Dark Slate (#0F172A a #1E293B) con malla técnica sutil.
- Badge superior: "DATALARIA EXECUTIVE DECISION PACK • SUPPLY CHAIN / APICS STANDARD".
- Título principal: "CALCULADORA DE STOCK DE SEGURIDAD & ROP" / "SAFETY STOCK & REORDER POINT (ROP)".
- Subtítulo: "Optimización de Inventario, Nivel de Servicio & Working Capital C-Level".
- Panel analítico derecho: Gráfico cartesiano del ciclo Diente de Sierra (Sawtooth) con líneas de ROP y SS.
- Píldoras de entregables: [📊 Excel + Sheets] [📑 PPTX 16:9 C-Level] [📄 Guía PDF].
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def get_font(name, size):
    """Carga fuente TrueType del sistema Windows o fallback predeterminado."""
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
    """Pinta un degradado diagonal suave en el fondo."""
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
    """Dibuja una cuadrícula y cruces de alineación técnica sutiles."""
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(20, 30, 48), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(20, 30, 48), width=1)

    for x in range(60, width, 120):
        for y in range(60, height, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=(51, 65, 85), width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=(51, 65, 85), width=1)


def draw_sawtooth_panel(draw, x0, y0, w, h, font_small, font_bold, font_mono, lang='ES'):
    """
    Dibuja el panel analítico ejecutivo del motor de inventario Diente de Sierra (Sawtooth).
    """
    is_es = (lang == 'ES')
    # Marco exterior
    draw.rounded_rectangle([(x0, y0), (x0 + w, y0 + h)], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # 1. Cabecera del Panel Gráfico
    draw.rounded_rectangle([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 38)], radius=10, fill=(30, 41, 59))
    title_panel = "MOTOR ESTOCÁSTICO SCM (APICS / MIT CTL)" if lang == 'ES' else "STOCHASTIC SCM ENGINE (APICS / MIT CTL)"
    draw.text((x0 + 16, y0 + 12), title_panel, fill=(2, 132, 199), font=font_bold)
    sub_panel = "SS = Z · √(L·σd² + d²·σL²)  |  ROP = d·L + SS"
    draw.text((x0 + w - 275, y0 + 13), sub_panel, fill=(148, 163, 184), font=font_small)

    # 2. Área del Gráfico Cartesiano Diente de Sierra
    gx0 = x0 + 20
    gy0 = y0 + 50
    gw = w - 40
    gh = 240

    draw.rounded_rectangle([(gx0, gy0), (gx0 + gw, gy0 + gh)], radius=8, fill=(24, 33, 50), outline=(51, 65, 85), width=1)

    # Ejes cartesianos
    base_y = gy0 + gh - 35
    top_y = gy0 + 25
    draw.line([(gx0 + 35, base_y), (gx0 + gw - 25, base_y)], fill=(71, 85, 105), width=1)
    draw.line([(gx0 + 35, base_y), (gx0 + 35, top_y)], fill=(71, 85, 105), width=1)

    # Zona de Colchón de Seguridad (SS Buffer) sombreada
    ss_y = base_y - 45
    draw.rectangle([(gx0 + 36, ss_y), (gx0 + gw - 25, base_y - 1)], fill=(16, 185, 129, 40), outline=None)
    draw.line([(gx0 + 35, ss_y), (gx0 + gw - 25, ss_y)], fill=(16, 185, 129), width=2)
    draw.text((gx0 + gw - 130, ss_y - 14), "SS Colchón Basal" if lang == 'ES' else "SS Safety Buffer", fill=(16, 185, 129), font=font_small)

    # Línea horizontal de Punto de Pedido (ROP)
    rop_y = base_y - 110
    # Línea discontinua simulada para ROP
    for dash_x in range(gx0 + 35, gx0 + gw - 25, 10):
        draw.line([(dash_x, rop_y), (dash_x + 5, rop_y)], fill=(245, 158, 11), width=2)
    draw.text((gx0 + gw - 130, rop_y - 14), "ROP Punto Pedido" if lang == 'ES' else "ROP Reorder Point", fill=(245, 158, 11), font=font_small)

    # Trazado de dos ciclos de Diente de Sierra
    # Ciclo 1: de x=45 a x=245. Empieza en top_inv_y (base_y - 170), baja a ss_y, y salta a top_inv_y
    top_inv_y = base_y - 175

    # Puntos Ciclo 1
    p1_start = (gx0 + 40, top_inv_y)
    p1_rop_trigger = (gx0 + 130, rop_y)
    p1_bottom = (gx0 + 230, ss_y)
    p1_replenish = (gx0 + 230, top_inv_y)

    # Puntos Ciclo 2
    p2_rop_trigger = (gx0 + 320, rop_y)
    p2_bottom = (gx0 + 420, ss_y)
    p2_replenish = (gx0 + 420, top_inv_y)

    # Dibujar líneas del diente de sierra (Azul Datalaria brillante)
    draw.line([p1_start, p1_bottom], fill=(37, 99, 235), width=3)
    draw.line([p1_bottom, p1_replenish], fill=(37, 99, 235), width=3)
    draw.line([p1_replenish, p2_bottom], fill=(37, 99, 235), width=3)
    draw.line([p2_bottom, p2_replenish], fill=(37, 99, 235), width=3)

    # Marcadores de disparo de pedido (ROP)
    draw.ellipse([(p1_rop_trigger[0] - 5, p1_rop_trigger[1] - 5), (p1_rop_trigger[0] + 5, p1_rop_trigger[1] + 5)], fill=(245, 158, 11), outline=(255, 255, 255), width=1)
    draw.ellipse([(p2_rop_trigger[0] - 5, p2_rop_trigger[1] - 5), (p2_rop_trigger[0] + 5, p2_rop_trigger[1] + 5)], fill=(245, 158, 11), outline=(255, 255, 255), width=1)

    # Marcadores de llegada de lote (+EOQ)
    draw.ellipse([(p1_bottom[0] - 5, p1_bottom[1] - 5), (p1_bottom[0] + 5, p1_bottom[1] + 5)], fill=(16, 185, 129), outline=(255, 255, 255), width=1)

    # Callout: Ventana Lead Time
    draw.line([(p1_rop_trigger[0], rop_y + 15), (p1_bottom[0], rop_y + 15)], fill=(203, 213, 225), width=1)
    draw.text((p1_rop_trigger[0] + 15, rop_y + 18), "Lead Time (L)" if lang == 'ES' else "Lead Time (L)", fill=(148, 163, 184), font=font_small)

    # Callout: Lote EOQ
    draw.text((p1_bottom[0] + 10, top_inv_y + 35), "+EOQ Lote Wilson" if lang == 'ES' else "+EOQ Wilson Batch", fill=(2, 132, 199), font=font_small)

    # Eje horizontal labels (Días)
    draw.text((gx0 + 40, base_y + 6), "Día 0" if lang == 'ES' else "Day 0", fill=(100, 116, 139), font=font_small)
    draw.text((p1_bottom[0] - 15, base_y + 6), "Día 15" if lang == 'ES' else "Day 15", fill=(100, 116, 139), font=font_small)
    draw.text((p2_bottom[0] - 15, base_y + 6), "Día 30" if lang == 'ES' else "Day 30", fill=(100, 116, 139), font=font_small)

    # 3. Tres Tarjetas KPI Inferiores
    ky = gy0 + gh + 14
    kw = (gw - 20) // 3
    kh = 74

    kpis_data_es = [
        ("NIVEL DE SERVICIO", "98,0% (Z=2,05)", "Clase A Blindada", (16, 185, 129)),
        ("CAPITAL LIBERADO", "240.000 €", "Retorno Working Capital", (37, 99, 235)),
        ("ROTURAS CLASE A", "< 2,0%", "-65% Riesgo Quiebre", (245, 158, 11))
    ]
    kpis_data_en = [
        ("SERVICE LEVEL", "98.0% (Z=2.05)", "Protected Class A", (16, 185, 129)),
        ("CASH RELEASED", "$240,000", "Working Capital Freed", (37, 99, 235)),
        ("CLASS A SHORTAGE", "< 2.0%", "-65% Stockout Risk", (245, 158, 11))
    ]
    kpis_data = kpis_data_es if is_es else kpis_data_en

    for idx, (kt, kv, ks, kc) in enumerate(kpis_data):
        kx = gx0 + idx * (kw + 10)
        draw.rounded_rectangle([(kx, ky), (kx + kw, ky + kh)], radius=6, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text((kx + 10, ky + 8), kt, fill=(148, 163, 184), font=font_small)
        draw.text((kx + 10, ky + 25), kv, fill=kc, font=font_bold)
        draw.text((kx + 10, ky + 52), ks, fill=(100, 116, 139), font=font_small)

    # 4. Barra de Diagnóstico Inferior
    by = ky + kh + 10
    draw.rounded_rectangle([(gx0, by), (gx0 + gw, by + 26)], radius=6, fill=(16, 185, 129, 30), outline=(16, 185, 129), width=1)
    status_text = (
        "ESTADO: MODELO ESTOCÁSTICO VALIDADO • GRADO CONSEJO DE ADMINISTRACIÓN"
        if lang == 'ES' else
        "STATUS: STOCHASTIC ENGINE VALIDATED • BOARDROOM DECISION-GRADE"
    )
    draw.text((gx0 + 20, by + 6), status_text, fill=(16, 185, 129), font=font_bold)


def create_cover(output_path, lang='ES'):
    """Genera la imagen completa de portada (1200 x 630 px)."""
    width = 1200
    height = 630

    img = Image.new('RGB', (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Fondo con degradado y malla
    draw_linear_gradient(draw, width, height, (15, 23, 42), (30, 41, 59))
    draw_technical_grid(draw, width, height)

    # Fuentes del sistema
    font_badge = get_font("segoeuib.ttf", 13)
    font_title = get_font("segoeuib.ttf", 36)
    font_sub = get_font("segoeui.ttf", 16)
    font_bold = get_font("segoeuib.ttf", 14)
    font_body = get_font("segoeui.ttf", 13)
    font_small = get_font("segoeui.ttf", 10)
    font_mono = get_font("consola.ttf", 11)

    # 2. Panel Izquierdo: Textos y Propuesta de Valor
    lx = 65

    # Badge Superior
    draw.rounded_rectangle([(lx, 55), (lx + 430, 85)], radius=6, fill=(37, 99, 235), outline=None)
    badge_text = "DATALARIA EXECUTIVE PACK • APICS / ASCM STANDARD"
    draw.text((lx + 14, 62), badge_text, fill=(255, 255, 255), font=font_badge)

    # Título Principal
    if lang == 'ES':
        draw.text((lx, 110), "STOCK DE SEGURIDAD", fill=(255, 255, 255), font=font_title)
        draw.text((lx, 155), "& REORDER POINT (ROP)", fill=(37, 99, 235), font=font_title)
        sub_text1 = "Optimización de Inventario, Nivel de Servicio"
        sub_text2 = "& Working Capital para el Consejo de Administración"
    else:
        draw.text((lx, 110), "SAFETY STOCK &", fill=(255, 255, 255), font=font_title)
        draw.text((lx, 155), "REORDER POINT (ROP)", fill=(37, 99, 235), font=font_title)
        sub_text1 = "Inventory Optimization, Service Level &"
        sub_text2 = "C-Level Working Capital Management"

    # Subtítulo en 2 líneas
    draw.text((lx, 218), sub_text1, fill=(203, 213, 225), font=font_sub)
    draw.text((lx, 242), sub_text2, fill=(148, 163, 184), font=font_sub)

    # Separador decorativo
    draw.line([(lx, 280), (lx + 480, 280)], fill=(51, 65, 85), width=2)

    # Bullets de Valor Diferencial
    bullets_es = [
        "Modelado estocástico completo: SS = Z·√(L·σd² + d²·σL²)",
        "Sincronización del ciclo Diente de Sierra y lote Wilson EOQ",
        "Matriz estratégica ABC y liberación neta de Working Capital"
    ]
    bullets_en = [
        "Complete stochastic convolution: SS = Z·√(L·σd² + d²·σL²)",
        "Continuous Sawtooth cycle dynamics & Wilson EOQ lot sizing",
        "Strategic ABC stratification & releasable working capital"
    ]
    bullets = bullets_es if lang == 'ES' else bullets_en

    by = 300
    for b in bullets:
        draw.ellipse([(lx + 2, by + 4), (lx + 10, by + 12)], fill=(2, 132, 199))
        draw.text((lx + 20, by), b, fill=(226, 232, 240), font=font_body)
        by += 32

    # Píldoras de Entregables Oficiales
    py = 430
    pills = [
        ("📊 Excel + Sheets", (37, 99, 235)),
        ("📑 PPTX 16:9 C-Level", (16, 185, 129)),
        ("📄 Guía PDF", (217, 119, 6))
    ]
    cur_px = lx
    for p_name, p_col in pills:
        pill_w = 150 if "PPTX" in p_name else 130
        draw.rounded_rectangle([(cur_px, py), (cur_px + pill_w, py + 34)], radius=8, fill=(30, 41, 59), outline=p_col, width=1)
        draw.text((cur_px + 14, py + 8), p_name, fill=(255, 255, 255), font=font_bold)
        cur_px += pill_w + 14

    # Footer Institucional
    draw.text((lx, 555), "Datalaria.com • Standard APICS / MIT Center for Transportation & Logistics", fill=(100, 116, 139), font=font_small)

    # 3. Panel Derecho: Panel Analítico Diente de Sierra
    rx = 575
    ry = 55
    rw = 560
    rh = 520
    draw_sawtooth_panel(draw, rx, ry, rw, rh, font_small, font_bold, font_mono, lang=lang)

    # Guardar imagen
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=95)


def main():
    """Genera las portadas en las carpetas de contenido de los posts."""
    path_es = "content/es/posts/calculadora-stock-seguridad-rop/cover.png"
    path_en = "content/en/posts/safety-stock-reorder-point-calculator/cover.png"

    print("[1/2] Generando portada en Español (content/es/posts/.../cover.png)...")
    create_cover(path_es, lang='ES')
    print(f"      -> Guardado: {path_es}")

    print("[2/2] Generating cover image in English (content/en/posts/.../cover.png)...")
    create_cover(path_en, lang='EN')
    print(f"      -> Saved: {path_en}")

    print("Portadas de alta resolución cover.png generadas con total éxito.")


if __name__ == "__main__":
    main()
