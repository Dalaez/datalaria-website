#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_diagrams.py
====================
Genera de forma programática las 3 imágenes oficiales de alta resolución
para los artículos de la Calculadora de Stock de Seguridad & ROP (ES y EN):
1. diagrama-1-ciclo-vida-iec62402.png / diagram-1-component-lifecycle-iec62402.png
   (Modelo de Ciclo de Vida del Componente en 6 Fases según IEC 62402 / JEDEC)
2. diagrama-2-pipeline-control-stock-clevel.png / diagram-2-clevel-inventory-pipeline.png
   (Pipeline C-Level de Planificación y Control de Inventarios en 9 Fases)
3. diagrama-3-dinamica-diente-sierra-sawtooth.png / diagram-3-sawtooth-cycle-dynamics.png
   (Dinámica Continua en Diente de Sierra (s, Q) y Equilibrio Estocástico ROP/EOQ)

Estándar Visual Tier-1 (APICS / ASCM & MIT CTL):
- Fondo limpio (#FFFFFF) con marco técnico redondeado (#CBD5E1 / #94A3B8).
- Tipografía nítida corporativa (Segoe UI / Arial).
- Coherencia cromática con la identidad visual de Datalaria.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# HELPERS DE FUENTES Y DIBUJO
# ==============================================================================

def get_font(name, size):
    """Carga fuente TrueType del sistema con fallback seguro."""
    paths = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_arrow_right(draw, x_start, x_end, y, color=(100, 116, 139), width=2):
    """Dibuja una flecha horizontal hacia la derecha."""
    draw.line([(x_start, y), (x_end, y)], fill=color, width=width)
    draw.polygon([(x_end - 6, y - 5), (x_end - 6, y + 5), (x_end, y)], fill=color)


def draw_arrow_down(draw, x, y_start, y_end, color=(100, 116, 139), width=2):
    """Dibuja una flecha vertical hacia abajo."""
    draw.line([(x, y_start), (x, y_end)], fill=color, width=width)
    draw.polygon([(x - 5, y_end - 6), (x + 5, y_end - 6), (x, y_end)], fill=color)


# ==============================================================================
# DIAGRAMA 1: CICLO DE VIDA DEL COMPONENTE (IEC 62402 / JEDEC)
# ==============================================================================

def generate_diagram_1(lang="ES", out_path=None):
    width = 1280
    height = 540

    if out_path is None:
        if lang == "ES":
            out_path = "content/es/posts/calculadora-stock-seguridad-rop/diagrama-1-ciclo-vida-iec62402.png"
        else:
            out_path = "content/en/posts/safety-stock-reorder-point-calculator/diagram-1-component-lifecycle-iec62402.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Marco exterior
    draw.rounded_rectangle(
        [(10, 10), (width - 10, height - 10)],
        radius=14,
        fill=(255, 255, 255),
        outline=(203, 213, 225),
        width=2,
    )

    # Fuentes
    f_badge = get_font("segoeuib.ttf", 11)
    f_title = get_font("segoeuib.ttf", 22)
    f_sub = get_font("segoeui.ttf", 13)
    f_box_num = get_font("segoeuib.ttf", 12)
    f_box_title = get_font("segoeuib.ttf", 15)
    f_box_sub = get_font("segoeui.ttf", 12)
    f_box_detail = get_font("segoeui.ttf", 11)

    # Cabecera
    badge_text = "ESTÁNDAR IEC 62402 · JEDEC JESD48/JESD46" if lang == "ES" else "IEC 62402 STANDARD · JEDEC JESD48/JESD46"
    title_text = (
        "Modelo de Ciclo de Vida del Componente y Gobernanza de Obsolescencia"
        if lang == "ES"
        else "Component Lifecycle Governance & Strategic Obsolescence Model"
    )
    sub_text = (
        "Intersección entre Gestión de Inventario Estocástico (SS/ROP) y Riesgo de Discontinuación Fabril"
        if lang == "ES"
        else "Intersection of Stochastic Inventory Optimization (SS/ROP) with Manufacturing EOL Risk"
    )

    draw.rounded_rectangle([(width // 2 - 190, 22), (width // 2 + 190, 42)], radius=6, fill=(241, 245, 249), outline=(203, 213, 225))
    draw.text((width // 2, 32), badge_text, fill=(71, 85, 105), font=f_badge, anchor="mm")
    draw.text((width // 2, 65), title_text, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((width // 2, 92), sub_text, fill=(100, 116, 139), font=f_sub, anchor="mm")

    # 6 Cajas horizontales
    stages_es = [
        {
            "num": "FASE 1", "title": "Introducción",
            "desc": "Demanda incipiente",
            "detail": "Alta incertidumbre σd\nLotes piloto pequeños",
            "fill": (239, 246, 255), "stroke": (59, 130, 246), "t_color": (30, 58, 138), "d_color": (37, 99, 235)
        },
        {
            "num": "FASE 2", "title": "Crecimiento",
            "desc": "Escalado exponencial",
            "detail": "Revisión semanal ROP\nEstandarización σL",
            "fill": (236, 253, 245), "stroke": (16, 185, 129), "t_color": (6, 95, 70), "d_color": (5, 150, 105)
        },
        {
            "num": "FASE 3", "title": "Madurez",
            "desc": "Régimen óptimo",
            "detail": "Modelo SS3 + EOQ\nMínimo Working Capital",
            "fill": (15, 23, 42), "stroke": (37, 99, 235), "t_color": (255, 255, 255), "d_color": (147, 197, 253)
        },
        {
            "num": "FASE 4", "title": "Declive & PCN",
            "desc": "Alerta de cambio",
            "detail": "PCN de proceso/diseño\nBuffer de homologación",
            "fill": (254, 243, 199), "stroke": (245, 158, 11), "t_color": (146, 64, 14), "d_color": (180, 83, 9)
        },
        {
            "num": "FASE 5", "title": "PDN / LTB / EOL",
            "desc": "Última compra",
            "detail": "Suspensión de ROP\nCálculo All-Time Buy",
            "fill": (254, 226, 226), "stroke": (220, 38, 38), "t_color": (153, 27, 27), "d_color": (185, 28, 28)
        },
        {
            "num": "FASE 6", "title": "Obsoleto",
            "desc": "Fin de fabricación",
            "detail": "Evitar Dead Stock\nCero compras a brokers",
            "fill": (241, 245, 249), "stroke": (100, 116, 139), "t_color": (30, 41, 59), "d_color": (71, 85, 105)
        },
    ]

    stages_en = [
        {
            "num": "STAGE 1", "title": "Introduction",
            "desc": "Nascent demand",
            "detail": "High σd uncertainty\nSmall pilot runs",
            "fill": (239, 246, 255), "stroke": (59, 130, 246), "t_color": (30, 58, 138), "d_color": (37, 99, 235)
        },
        {
            "num": "STAGE 2", "title": "Growth",
            "desc": "Rapid scaling",
            "detail": "Weekly ROP audits\nStandardized σL",
            "fill": (236, 253, 245), "stroke": (16, 185, 129), "t_color": (6, 95, 70), "d_color": (5, 150, 105)
        },
        {
            "num": "STAGE 3", "title": "Maturity",
            "desc": "Steady-state optimal",
            "detail": "Full SS3 + EOQ engine\nMin Working Capital",
            "fill": (15, 23, 42), "stroke": (37, 99, 235), "t_color": (255, 255, 255), "d_color": (147, 197, 253)
        },
        {
            "num": "STAGE 4", "title": "Decline & PCN",
            "desc": "Change notification",
            "detail": "Process or design shift\nQualification buffer",
            "fill": (254, 243, 199), "stroke": (245, 158, 11), "t_color": (146, 64, 14), "d_color": (180, 83, 9)
        },
        {
            "num": "STAGE 5", "title": "PDN / LTB / EOL",
            "desc": "Last Time Buy",
            "detail": "Freeze recurring ROP\nSize All-Time Buy",
            "fill": (254, 226, 226), "stroke": (220, 38, 38), "t_color": (153, 27, 27), "d_color": (185, 28, 28)
        },
        {
            "num": "STAGE 6", "title": "Obsolete",
            "desc": "Zero production",
            "detail": "Avoid Dead Stock\nZero broker risk",
            "fill": (241, 245, 249), "stroke": (100, 116, 139), "t_color": (30, 41, 59), "d_color": (71, 85, 105)
        },
    ]

    stages = stages_es if lang == "ES" else stages_en

    # Posicionamiento de las 6 cajas
    box_w = 175
    box_h = 240
    gap = 26
    start_x = (width - (6 * box_w + 5 * gap)) // 2
    top_y = 140

    for i, st in enumerate(stages):
        bx = start_x + i * (box_w + gap)
        by = top_y

        # Caja
        draw.rounded_rectangle([(bx, by), (bx + box_w, by + box_h)], radius=10, fill=st["fill"], outline=st["stroke"], width=2)

        # Badge número
        draw.text((bx + box_w // 2, by + 26), st["num"], fill=st["d_color"], font=f_box_num, anchor="mm")
        # Título
        draw.text((bx + box_w // 2, by + 56), st["title"], fill=st["t_color"], font=f_box_title, anchor="mm")

        # Línea separadora
        draw.line([(bx + 20, by + 78), (bx + box_w - 20, by + 78)], fill=st["stroke"], width=1)

        # Subtítulo descriptivo
        draw.text((bx + box_w // 2, by + 102), st["desc"], fill=st["t_color"], font=f_box_sub, anchor="mm")

        # Detalles multi-línea
        lines = st["detail"].split("\n")
        curr_y = by + 138
        for line in lines:
            draw.text((bx + box_w // 2, curr_y), line, fill=st["d_color"], font=f_box_detail, anchor="mm")
            curr_y += 20

        # Flecha conectora a la siguiente caja
        if i < 5:
            arr_start_x = bx + box_w + 4
            arr_end_x = arr_start_x + gap - 8
            draw_arrow_right(draw, arr_start_x, arr_end_x, by + box_h // 2, color=(148, 163, 184), width=2)

    # Barra inferior de síntesis ejecutiva
    footer_text = (
        "REGLA DE GOBERNANZA: Cuando el proveedor emite PDN/EOL, el ERP debe bloquear el disparo automático de ROP y activar el protocolo LTB (Last Time Buy)."
        if lang == "ES"
        else "BOARDROOM GOVERNANCE RULE: Upon PDN/EOL notice, the ERP must freeze automated ROP replenishment and trigger Last Time Buy (LTB) sizing."
    )
    draw.rounded_rectangle([(start_x, height - 90), (start_x + 6 * box_w + 5 * gap, height - 35)], radius=8, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text((width // 2, height - 62), footer_text, fill=(248, 250, 252), font=f_box_detail, anchor="mm")

    img.save(out_path, "PNG", dpi=(150, 150))
    print(f"✅ Diagrama 1 guardado: {out_path}")


# ==============================================================================
# DIAGRAMA 2: PIPELINE C-LEVEL DE CONTROL DE INVENTARIOS
# ==============================================================================

def generate_diagram_2(lang="ES", out_path=None):
    width = 1200
    height = 960

    if out_path is None:
        if lang == "ES":
            out_path = "content/es/posts/calculadora-stock-seguridad-rop/diagrama-2-pipeline-control-stock-clevel.png"
        else:
            out_path = "content/en/posts/safety-stock-reorder-point-calculator/diagram-2-clevel-inventory-pipeline.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(10, 10), (width - 10, height - 10)], radius=14, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

    f_badge = get_font("segoeuib.ttf", 11)
    f_title = get_font("segoeuib.ttf", 22)
    f_sub = get_font("segoeui.ttf", 13)
    f_step_num = get_font("segoeuib.ttf", 12)
    f_step_title = get_font("segoeuib.ttf", 14)
    f_step_desc = get_font("segoeui.ttf", 11)

    badge_text = "ESTÁNDAR APICS / ASCM · MIT CTL" if lang == "ES" else "APICS / ASCM STANDARD · MIT CTL"
    title_text = (
        "Pipeline de Planificación y Control de Inventarios para Alta Dirección (C-Level)"
        if lang == "ES"
        else "The C-Level Inventory Planning, Valuation & Control Pipeline"
    )
    sub_text = (
        "Arquitectura End-to-End: De la Estratificación ABC a la Liberación Neta de Working Capital"
        if lang == "ES"
        else "End-to-End Architecture: From ABC Stratification to Balance Sheet Working Capital Harvesting"
    )

    draw.rounded_rectangle([(width // 2 - 160, 20), (width // 2 + 160, 40)], radius=6, fill=(241, 245, 249), outline=(203, 213, 225))
    draw.text((width // 2, 30), badge_text, fill=(71, 85, 105), font=f_badge, anchor="mm")
    draw.text((width // 2, 60), title_text, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((width // 2, 86), sub_text, fill=(100, 116, 139), font=f_sub, anchor="mm")

    steps_es = [
        ("FASE 1", "Segmentación Estratégica ABC", "Clasificación de Pareto por valor de consumo y margen · Asignación formal de Nivel de Servicio Objetivo (CSL: 90%–99%)", (239, 246, 255), (59, 130, 246)),
        ("FASE 2", "Perfilado Estocástico de Demanda", "Cálculo de demanda media diaria (d) y desviación estándar de volatilidad de clientes (σd)", (238, 242, 255), (99, 102, 241)),
        ("FASE 3", "Auditoría de Fiabilidad de Lead Time", "Plazo medio de tránsito de aprovisionamiento (L) y variabilidad de retrasos de proveedores (σL)", (245, 243, 255), (139, 92, 246)),
        ("FASE 4", "Motor de Convolución Estocástica (SS3)", "Cálculo Z-Score según CSL: SS = Z · √(L · σd² + d² · σL²) · Protección ante colapso conjunto", (15, 23, 42), (37, 99, 235)),
        ("FASE 5", "Calibración del Punto de Pedido (ROP)", "Demanda en tiempo de entrega: LTD = d · L · Umbral de disparo automatizado en ERP: ROP = LTD + SS", (236, 253, 245), (16, 185, 129)),
        ("FASE 6", "Lote Óptimo de Compra (Wilson EOQ)", "Compromiso óptimo entre coste de emisión (S) y posesión financiera (h · C): EOQ = √(2·D·S / h·C)", (240, 253, 250), (20, 184, 166)),
        ("FASE 7", "Auditoría de Working Capital & Liquidez", "¿Existe sobrestock inmovilizado frente a heurísticas planas? · Cuantificación de caja neta liberable", (254, 243, 199), (245, 158, 11)),
        ("FASE 8", "Plan de Liberación Inmediata de Caja", "Desinversión ordenada de excedentes no críticos Clase C/B · Reinversión en colchones críticos Clase A", (254, 226, 226), (220, 38, 38)),
        ("FASE 9", "Gobernanza y Ratificación en Consejo", "Aprobación formal por CEO, CFO y COO · SLAs de entrega con penalizaciones económicas por día de retraso", (248, 250, 252), (100, 116, 139)),
    ]

    steps_en = [
        ("STAGE 1", "Strategic ABC Portfolio Stratification", "Pareto classification by consumption revenue and margin · Formal Cycle Service Level (CSL: 90%–99%) targets", (239, 246, 255), (59, 130, 246)),
        ("STAGE 2", "Stochastic Demand Volatility Profiling", "Daily mean consumption rate (d) and customer demand standard deviation (σd)", (238, 242, 255), (99, 102, 241)),
        ("STAGE 3", "Supplier Lead Time Reliability Audit", "Mean replenishment transit lead time (L) and logistical supplier tardiness variance (σL)", (245, 243, 255), (139, 92, 246)),
        ("STAGE 4", "Stochastic Convolution Engine (SS3)", "Z-Factor computation based on CSL: SS = Z · √(L · σd² + d² · σL²) · Dual volatility hedge", (15, 23, 42), (37, 99, 235)),
        ("STAGE 5", "Reorder Point Calibration (ROP)", "Lead Time Demand: LTD = d · L · Automated ERP replenishment trigger threshold: ROP = LTD + SS", (236, 253, 245), (16, 185, 129)),
        ("STAGE 6", "Wilson Lot Sizing Optimization (EOQ)", "Trade-off between fixed ordering cost (S) and carrying cost (h · C): EOQ = √(2·D·S / h·C)", (240, 253, 250), (20, 184, 166)),
        ("STAGE 7", "Working Capital Liquidity Audit", "Does idle overstock exist versus baseline heuristic rules? · Quantifying net releasable balance sheet capital", (254, 243, 199), (245, 158, 11)),
        ("STAGE 8", "Immediate Inventory Harvesting Plan", "Orderly phase-out of idle non-critical buffer stock · Reallocating cash to protect core Class A revenue drivers", (254, 226, 226), (220, 38, 38)),
        ("STAGE 9", "Boardroom Governance Gateway", "Formal executive policy ratification by CEO, CFO, and COO · Incorporating supplier SLAs with tardiness penalties", (248, 250, 252), (100, 116, 139)),
    ]

    steps = steps_es if lang == "ES" else steps_en

    box_w = 1040
    box_h = 64
    start_x = (width - box_w) // 2
    curr_y = 125

    for i, (num, title, desc, bg, border) in enumerate(steps):
        # Dibujar caja
        draw.rounded_rectangle([(start_x, curr_y), (start_x + box_w, curr_y + box_h)], radius=8, fill=bg, outline=border, width=2 if i == 3 else 1)

        # Texto
        is_dark = (bg == (15, 23, 42))
        t_color = (255, 255, 255) if is_dark else (15, 23, 42)
        d_color = (147, 197, 253) if is_dark else (71, 85, 105)

        # Número + Título
        draw.text((start_x + 24, curr_y + 22), num, fill=border if not is_dark else (96, 165, 250), font=f_step_num, anchor="lm")
        draw.text((start_x + 115, curr_y + 22), title, fill=t_color, font=f_step_title, anchor="lm")

        # Descripción
        draw.text((start_x + 115, curr_y + 44), desc, fill=d_color, font=f_step_desc, anchor="lm")

        # Flecha conectora hacia abajo
        if i < len(steps) - 1:
            draw_arrow_down(draw, width // 2, curr_y + box_h, curr_y + box_h + 24, color=(148, 163, 184), width=2)
            curr_y += box_h + 24
        else:
            curr_y += box_h

    img.save(out_path, "PNG", dpi=(150, 150))
    print(f"✅ Diagrama 2 guardado: {out_path}")


# ==============================================================================
# DIAGRAMA 3: DINÁMICA DIENTE DE SIERRA (SAWTOOTH DYNAMICS)
# ==============================================================================

def generate_diagram_3(lang="ES", out_path=None):
    width = 1200
    height = 800

    if out_path is None:
        if lang == "ES":
            out_path = "content/es/posts/calculadora-stock-seguridad-rop/diagrama-3-dinamica-diente-sierra-sawtooth.png"
        else:
            out_path = "content/en/posts/safety-stock-reorder-point-calculator/diagram-3-sawtooth-cycle-dynamics.png"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(10, 10), (width - 10, height - 10)], radius=14, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

    f_badge = get_font("segoeuib.ttf", 11)
    f_title = get_font("segoeuib.ttf", 22)
    f_sub = get_font("segoeui.ttf", 13)
    f_step_num = get_font("segoeuib.ttf", 12)
    f_step_title = get_font("segoeuib.ttf", 14)
    f_step_desc = get_font("segoeui.ttf", 11)

    badge_text = "MODELO DE REVISIÓN CONTINUA (s, Q) · (ROP, EOQ)" if lang == "ES" else "CONTINUOUS REVIEW MODEL (s, Q) · (ROP, EOQ)"
    title_text = (
        "Dinámica en Diente de Sierra (Sawtooth Chart) y Flujo del Ciclo de Reposición"
        if lang == "ES"
        else "Dynamic Sawtooth Inventory Cycle & Replenishment Feedback Loop"
    )
    sub_text = (
        "Mecánica Estocástica de las 6 Etapas: Del Máximo Stock (SS + EOQ) a la Llegada Sincronizada JIT"
        if lang == "ES"
        else "Stochastic Mechanics Across 6 Stages: From Peak Stock (SS + EOQ) to JIT Dock Ingestion"
    )

    draw.rounded_rectangle([(width // 2 - 180, 20), (width // 2 + 180, 40)], radius=6, fill=(241, 245, 249), outline=(203, 213, 225))
    draw.text((width // 2, 30), badge_text, fill=(71, 85, 105), font=f_badge, anchor="mm")
    draw.text((width // 2, 60), title_text, fill=(15, 23, 42), font=f_title, anchor="mm")
    draw.text((width // 2, 86), sub_text, fill=(100, 116, 139), font=f_sub, anchor="mm")

    stages_es = [
        ("FASE 1", "Entrada de Lote +EOQ", "Inventario disponible alcanza su pico: Stock Máximo = SS + EOQ · Consumo comercial a tasa diaria promedio d", (239, 246, 255), (59, 130, 246)),
        ("FASE 2", "Consumo y Descenso Lineal", "El inventario desciende con pendiente -d · El colchón basal de seguridad SS permanece intocado en la base", (248, 250, 252), (148, 163, 184)),
        ("FASE 3", "Cruce del Umbral ROP (Punto de Pedido)", "¿Inventario disponible ≤ ROP? · ROP = d · L + SS · Punto de inflexión crítico de la cadena de suministro", (254, 243, 199), (245, 158, 11)),
        ("FASE 4", "Emisión Automática de la Orden de Compra", "El ERP emite automáticamente un pedido por tamaño EOQ · Se inicia la ventana crítica de Lead Time de L días", (238, 242, 255), (99, 102, 241)),
        ("FASE 5", "Tránsito Logístico y Riesgo Estocástico", "Durante los L días se consumen d · L unidades · Si la demanda sube (σd) o el proveedor se retrasa (σL), el SS absorbe el choque", (254, 226, 226), (220, 38, 38)),
        ("FASE 6", "Recepción y Sincronización Just-in-Time", "El lote llega justo cuando el inventario roza el colchón basal SS · El stock salta instantáneamente de nuevo a SS + EOQ", (236, 253, 245), (16, 185, 129)),
    ]

    stages_en = [
        ("STAGE 1", "Replenishment Batch Arrival +EOQ", "Available inventory peaks: Maximum Stock = SS + EOQ · Commercial demand proceeds at mean daily rate d", (239, 246, 255), (59, 130, 246)),
        ("STAGE 2", "Linear Depletion Phase", "Inventory depletes along negative slope -d · The basal safety cushion SS remains untouched at the foundation", (248, 250, 252), (148, 163, 184)),
        ("STAGE 3", "Reorder Point Breach (ROP Trigger)", "Does available stock breach ROP? · ROP = d · L + SS · Critical inflection gateway across the supply chain", (254, 243, 199), (245, 158, 11)),
        ("STAGE 4", "Automated Purchase Order Emission", "ERP automatically fires replenishment order for Wilson EOQ batch · Replenishment transit window opens for L days", (238, 242, 255), (99, 102, 241)),
        ("STAGE 5", "Lead Time Transit & Stochastic Risk", "Over L days, an expected d · L units are consumed · If demand surges (σd) or supplier delays (σL), SS absorbs the impact", (254, 226, 226), (220, 38, 38)),
        ("STAGE 6", "Synchronized Dock Delivery & Renewal", "Batch docks exactly as stock touches baseline buffer SS · Available inventory leaps instantaneously back to SS + EOQ", (236, 253, 245), (16, 185, 129)),
    ]

    stages = stages_es if lang == "ES" else stages_en

    box_w = 1040
    box_h = 70
    start_x = (width - box_w) // 2
    curr_y = 125

    for i, (num, title, desc, bg, border) in enumerate(stages):
        draw.rounded_rectangle([(start_x, curr_y), (start_x + box_w, curr_y + box_h)], radius=8, fill=bg, outline=border, width=2 if i in (0, 2, 5) else 1)

        draw.text((start_x + 24, curr_y + 24), num, fill=border, font=f_step_num, anchor="lm")
        draw.text((start_x + 115, curr_y + 24), title, fill=(15, 23, 42), font=f_step_title, anchor="lm")
        draw.text((start_x + 115, curr_y + 48), desc, fill=(71, 85, 105), font=f_step_desc, anchor="lm")

        if i < len(stages) - 1:
            draw_arrow_down(draw, width // 2, curr_y + box_h, curr_y + box_h + 24, color=(148, 163, 184), width=2)
            curr_y += box_h + 24
        else:
            curr_y += box_h

    # Flecha de bucle continuo de Fase 6 a Fase 1
    loop_y_end = 125 + box_h // 2
    loop_y_start = curr_y - box_h // 2
    loop_x = start_x + box_w + 30
    draw.line([(start_x + box_w, loop_y_start), (loop_x, loop_y_start), (loop_x, loop_y_end), (start_x + box_w + 6, loop_y_end)], fill=(16, 185, 129), width=2)
    draw.polygon([(start_x + box_w + 6, loop_y_end - 5), (start_x + box_w + 6, loop_y_end + 5), (start_x + box_w, loop_y_end)], fill=(16, 185, 129))
    draw.text((loop_x + 8, (loop_y_start + loop_y_end) // 2), "CICLO CONTINUO (s, Q)" if lang == "ES" else "CONTINUOUS (s, Q) CYCLE", fill=(16, 185, 129), font=f_step_desc, anchor="lm")

    img.save(out_path, "PNG", dpi=(150, 150))
    print(f"✅ Diagrama 3 guardado: {out_path}")


# ==============================================================================
# MAIN RUNNER
# ==============================================================================

if __name__ == "__main__":
    for lang in ["ES", "EN"]:
        print(f"\n--- Generando diagramas [{lang}] ---")
        generate_diagram_1(lang)
        generate_diagram_2(lang)
        generate_diagram_3(lang)
    print("\n🎉 Todos los diagramas generados exitosamente.")
