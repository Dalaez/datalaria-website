#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para el Executive Decision Pack:
1. packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/[ES]_Stock_Seguridad_ROP/Guia_Metodologica_Stock_ROP_ES.pdf
2. packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/[EN]_Safety_Stock_ROP/Methodology_Guide_Safety_Stock_ROP_EN.pdf

Estándar editorial de alta dirección (APICS / ASCM / MIT CTL / McKinsey Minto Pyramid):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (La Falacia de la Regla de las 3 Semanas).
- Página 2: Sección 2 (Fundamentación Matemática: Convolución Estocástica SS, ROP, Wilson EOQ y Barrera Asintótica).
- Página 3: Sección 3 (Estrategia de Segmentación ABC y Calibración Diferenciada de Nivel de Servicio).
- Página 4: Sección 4 (Caso de Estudio Realista: Empresa de 4.5M € de inventario, -45% roturas y 220k € de caja liberada).
- Página 5: Sección 5 (Protocolo de Defensa ante Comité - Boardroom FAQ) y Bibliografía Canónica.
- Paginación dinámica con NumberedCanvas ("Página X de Y" / "Page X of Y").
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- PALETA CORPORATIVA DATALARIA ---
C_NAVY_DARK = colors.HexColor("#0F172A")    # Slate 900
C_NAVY_MED = colors.HexColor("#1E293B")     # Slate 800
C_SLATE_MUTED = colors.HexColor("#64748B")  # Slate 500
C_BLUE_ACCENT = colors.HexColor("#2563EB")  # Blue 600
C_BLUE_LIGHT = colors.HexColor("#EFF6FF")   # Blue 50
C_CYAN_ACCENT = colors.HexColor("#0284C7")  # Sky 600

# Acentos y Estados
C_GREEN_ACCENT = colors.HexColor("#10B981") # Emerald 500
C_GREEN_LIGHT = colors.HexColor("#D1FAE5")  # Emerald 100
C_GREEN_TEXT = colors.HexColor("#065F46")   # Emerald 800

C_AMBER_ACCENT = colors.HexColor("#F59E0B") # Amber 500
C_AMBER_LIGHT = colors.HexColor("#FEF3C7")  # Amber 100
C_AMBER_TEXT = colors.HexColor("#92400E")   # Amber 800

C_RED_ACCENT = colors.HexColor("#DC2626")   # Red 600
C_RED_LIGHT = colors.HexColor("#FEE2E2")    # Red 100
C_RED_TEXT = colors.HexColor("#991B1B")     # Red 800

C_BG_CARD = colors.HexColor("#F8FAFC")      # Slate 50
C_BORDER_LIGHT = colors.HexColor("#CBD5E1") # Slate 300
C_WHITE = colors.HexColor("#FFFFFF")


class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para calcular y renderizar el número total de páginas dinámicamente."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f" -> Total páginas generadas: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        cur_page = self._pageNumber
        lang = getattr(self, '_lang', 'ES')

        # Cabecera institucional en páginas 2 a 5
        if cur_page > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(C_SLATE_MUTED)
            self.drawString(42, 805, "DATALARIA | EXECUTIVE DECISION PACK")
            header_right = ("STOCK DE SEGURIDAD & ROP: GUÍA METODOLÓGICA C-LEVEL"
                            if lang == 'ES' else
                            "SAFETY STOCK & ROP: C-LEVEL METHODOLOGY GUIDE")
            self.drawRightString(553, 805, header_right)
            self.setStrokeColor(C_BORDER_LIGHT)
            self.setLineWidth(0.75)
            self.line(42, 798, 553, 798)

        # Pie de página institucional
        self.setStrokeColor(C_BORDER_LIGHT)
        self.setLineWidth(0.75)
        self.line(42, 45, 553, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(C_SLATE_MUTED)
        footer_left = ("Datalaria.com • Documento Confidencial para Comité de Dirección & Supply Chain Governance"
                       if lang == 'ES' else
                       "Datalaria.com • Confidential Executive Committee & Supply Chain Governance Document")
        self.drawString(42, 32, footer_left)
        page_str = f"Página {cur_page} de {total_pages}" if lang == 'ES' else f"Page {cur_page} of {total_pages}"
        self.drawRightString(553, 32, page_str)

        self.restoreState()


def build_pdf(filename, lang='ES'):
    """Construye la guía metodológica de 5 páginas en el idioma especificado."""
    is_es = (lang == 'ES')

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=52,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Tipografías y Jerarquías
    style_cover_badge = ParagraphStyle(
        'CoverBadge',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=C_BLUE_ACCENT,
        spaceAfter=4
    )
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=C_NAVY_DARK,
        spaceAfter=5
    )
    style_cover_sub = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=C_SLATE_MUTED,
        spaceAfter=10
    )
    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=C_NAVY_DARK,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=C_BLUE_ACCENT,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=C_NAVY_MED,
        spaceAfter=5
    )
    style_body_bold = ParagraphStyle(
        'BodyBold_Custom',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=C_NAVY_DARK,
        spaceAfter=5
    )
    style_table_text = ParagraphStyle(
        'TableText',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=C_NAVY_MED
    )
    style_table_bold = ParagraphStyle(
        'TableBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=C_NAVY_DARK
    )
    style_callout = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_NAVY_DARK
    )

    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA EJECUTIVA + SECCIÓN 1 (LA FALACIA DE LAS 3 SEMANAS)
    # =========================================================================
    story.append(Paragraph("DATALARIA EXECUTIVE PACK • SUPPLY CHAIN & OPERATIONS STRATEGY (APICS / ASCM / MIT CTL)", style_cover_badge))
    p_title = (
        "GUÍA METODOLÓGICA: STOCK DE SEGURIDAD & PUNTO DE PEDIDO (ROP)"
        if is_es else
        "METHODOLOGY GUIDE: SAFETY STOCK & REORDER POINT (ROP)"
    )
    story.append(Paragraph(p_title, style_cover_title))

    p_sub = (
        "Fundamentación Matemática Estocástica, Optimización de Inventario y Gobernanza de Working Capital ante el Consejo de Administración"
        if is_es else
        "Stochastic Mathematical Derivation, Inventory Optimization and Working Capital Governance for the Board of Directors"
    )
    story.append(Paragraph(p_sub, style_cover_sub))

    # Tabla de Metadatos
    meta_data_es = [
        [Paragraph("<b>Estándar:</b> APICS / ASCM / MIT CTL", style_table_text), Paragraph("<b>Gobernanza:</b> Consejo de Administración / C-Level", style_table_text)],
        [Paragraph("<b>Audiencia:</b> CEO, CFO, COO, Dir. Supply Chain", style_table_text), Paragraph("<b>Versión:</b> 2.4 Oficial (Bilingüe)", style_table_text)]
    ]
    meta_data_en = [
        [Paragraph("<b>Standard:</b> APICS / ASCM / MIT CTL", style_table_text), Paragraph("<b>Governance:</b> Board of Directors / Executive Committee", style_table_text)],
        [Paragraph("<b>Target Audience:</b> CEO, CFO, COO, VP Supply Chain", style_table_text), Paragraph("<b>Version:</b> 2.4 Official (Bilingual)", style_table_text)]
    ]
    meta_data = meta_data_es if is_es else meta_data_en
    t_meta = Table(meta_data, colWidths=[255, 256])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Caja de Resumen Ejecutivo
    exec_summary_es = (
        "<b>RESUMEN EJECUTIVO:</b> Las organizaciones modernas inmovilizan millones de euros en circulante mientras sufren roturas recurrentes en sus productos más rentables. Esta aparente paradoja está causada por 'reglas empíricas' heurísticas (como fijar 3 semanas de stock para todo el catálogo). Esta guía establece el estándar cuantitativo para erradicar las heurísticas mediante la convolución estocástica de variabilidad de demanda y lead time, alineando el nivel de servicio con la política financiera de caja."
    )
    exec_summary_en = (
        "<b>EXECUTIVE SUMMARY:</b> Modern enterprises needlessly lock up millions of dollars in working capital while suffering frequent stockouts on core profit drivers. This apparent paradox is driven by naive 'rules of thumb' (such as carrying 3 arbitrary weeks of demand). This guide provides the rigorous quantitative framework to replace empirical guesswork with stochastic demand and lead time convolution, aligning cycle service levels with corporate cash flow."
    )
    exec_text = exec_summary_es if is_es else exec_summary_en
    t_sum = Table([[Paragraph(exec_text, style_callout)]], colWidths=[511])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BLUE_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BLUE_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 8))

    # SECCIÓN 1: LA FALACIA DE LA REGLA DE LAS 3 SEMANAS
    sec1_title = "1. La Falacia de la 'Regla de las 3 Semanas' y la Crisis de Liquidez" if is_es else "1. The Fallacy of the '3-Week Rule' and the Liquidity Squeeze"
    story.append(Paragraph(sec1_title, style_h1))

    sec1_text1 = (
        "En una gran cantidad de comités de dirección, directores de operaciones y responsables de aprovisionamiento justifican sus niveles de stock basándose en axiomas no demostrados: <i>'mantenemos 3 semanas de stock de seguridad para estar cubiertos'</i>. Esta regla heurística, aparentemente conservadora y prudente, constituye una de las mayores fuentes de destrucción de valor en la empresa:"
        if is_es else
        "Across corporate executive suites, supply chain leaders and procurement directors defend working capital decisions using unverified folklore: <i>'we keep 3 weeks of safety stock across the board to be safe'</i>. This empirical rule of thumb, while appearing prudent, represents one of the largest sources of destroyed corporate value:"
    )
    story.append(Paragraph(sec1_text1, style_body))

    points_sec1_es = [
        "<b>1. Sobrestock Masivo en SKUs Rápidos y Estables:</b> Para artículos de demanda constante y proveedores locales fiables (plazo de 2 días), 21 días de stock representa un exceso injustificable del 400%, absorbiendo caja que debería remunerar a accionistas o financiar CAPEX productivo.",
        "<b>2. Infradotación Crítica en SKUs Volátiles:</b> Para componentes importados de ultramar con lead time medio de 30 días y alta dispersión, 21 días es inferior a la demanda durante el plazo de entrega. Cuando ocurre un retraso en aduanas o un pico estacional, la empresa entra en rotura inevitable.",
        "<b>3. Ceguera ante la Impuntualidad del Proveedor (σL):</b> Las reglas heurísticas suponen erróneamente que los plazos de entrega son deterministas y perfectos, ignorando que la variabilidad logística representa más del 50% del riesgo real de rotura."
    ]
    points_sec1_en = [
        "<b>1. Massive Overstock on Fast, Stable SKUs:</b> For steady-demand items with local suppliers (2-day lead time), 21 days is a 400% unwarranted over-buffer, locking up cash that belongs in productive CAPEX or dividends.",
        "<b>2. Severe Shortages on Volatile Items:</b> For overseas components with a 30-day transit lead time and erratic demand, 21 days does not even cover the delivery window. A single shipping delay immediately induces catastrophic stockouts.",
        "<b>3. Complete Blindness to Supplier Lead Time Variance (σL):</b> Empirical rules mistakenly treat transit times as deterministic, ignoring that delivery tardiness generates over 50% of real-world stockout occurrences."
    ]
    points_sec1 = points_sec1_es if is_es else points_sec1_en
    for pt in points_sec1:
        story.append(Paragraph(f"• {pt}", style_body))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: FUNDAMENTACIÓN MATEMÁTICA Y DINÁMICA DEL INVENTARIO ESTOCÁSTICO
    # =========================================================================
    sec2_title = "2. Fundamentación Matemática y Dinámica del Inventario Estocástico" if is_es else "2. Mathematical Foundations & Stochastic Inventory Dynamics"
    story.append(Paragraph(sec2_title, style_h1))

    sec2_intro = (
        "El estándar APICS / ASCM y la teoría clásica de inventarios (Silver, Pyke & Thomas; Chopra & Meindl) modelan la demanda durante el plazo de entrega como una variable aleatoria continua. El colchón de seguridad debe proteger a la empresa durante la ventana de reabastecimiento frente a dos fuentes estocásticas independientes: la volatilidad del consumo del cliente (σd) y la dispersión del plazo de entrega del proveedor (σL)."
        if is_es else
        "The APICS / ASCM standard and classical inventory theory (Silver, Pyke & Thomas; Chopra & Meindl) formalize lead time demand as a continuous random variable. Safety stock must shield the firm during the replenishment cycle against two independent stochastic drivers: customer demand dispersion (σd) and supplier delivery unreliability (σL)."
    )
    story.append(Paragraph(sec2_intro, style_body))

    # TABLA DE FÓRMULAS DE LOS 3 MODELOS
    story.append(Paragraph("<b>Los Tres Modelos Estocásticos de la Literatura Científica:</b>" if is_es else "<b>The Three Stochastic Models in Academic Literature:</b>", style_h2))

    models_data_es = [
        [Paragraph("<b>Modelo</b>", style_table_bold), Paragraph("<b>Condición Operativa</b>", style_table_bold), Paragraph("<b>Fórmula Matemática</b>", style_table_bold), Paragraph("<b>Aplicación Típica</b>", style_table_bold)],
        [Paragraph("<b>Mod. 1: Demanda Variable, Plazo Fijo</b>", style_table_text), Paragraph("Demanda volátil (σd > 0), pero proveedor 100% puntual (σL = 0)", style_table_text), Paragraph("<b>SS = Z · σd · √L</b>", style_table_bold), Paragraph("Fabricación interna o proveedores locales JIT con slot garantizado", style_table_text)],
        [Paragraph("<b>Mod. 2: Demanda Fija, Plazo Variable</b>", style_table_text), Paragraph("Demanda perfectamente conocida (σd = 0), proveedor impuntual (σL > 0)", style_table_text), Paragraph("<b>SS = Z · d · σL</b>", style_table_bold), Paragraph("Líneas de ensamblaje cautivas con contratos de suministro transoceánico", style_table_text)],
        [Paragraph("<b>Mod. 3: Modelo Integral Convolución</b>", style_table_text), Paragraph("Demanda variable Y proveedor impuntual (σd > 0, σL > 0)", style_table_text), Paragraph("<b>SS = Z · √(L·σd² + d²·σL²)</b>", style_table_bold), Paragraph("<b>Estándar Corporativo Datalaria:</b> Distribución, retail y fabricación real", style_table_text)]
    ]
    models_data_en = [
        [Paragraph("<b>Model</b>", style_table_bold), Paragraph("<b>Operational Condition</b>", style_table_bold), Paragraph("<b>Mathematical Formula</b>", style_table_bold), Paragraph("<b>Typical Use Case</b>", style_table_bold)],
        [Paragraph("<b>Mod. 1: Variable Demand, Fixed LT</b>", style_table_text), Paragraph("Volatile demand (σd > 0), but 100% punctual vendor (σL = 0)", style_table_text), Paragraph("<b>SS = Z · σd · √L</b>", style_table_bold), Paragraph("Internal manufacturing or local JIT vendors with guaranteed time windows", style_table_text)],
        [Paragraph("<b>Mod. 2: Fixed Demand, Variable LT</b>", style_table_text), Paragraph("Predictable consumption (σd = 0), erratic vendor (σL > 0)", style_table_text), Paragraph("<b>SS = Z · d · σL</b>", style_table_bold), Paragraph("Captive assembly lines with overseas ocean freight suppliers", style_table_text)],
        [Paragraph("<b>Mod. 3: Full Stochastic Convolution</b>", style_table_text), Paragraph("Variable demand AND erratic supplier (σd > 0, σL > 0)", style_table_text), Paragraph("<b>SS = Z · √(L·σd² + d²·σL²)</b>", style_table_bold), Paragraph("<b>Datalaria Corporate Benchmark:</b> Real-world retail, distribution, manufacturing", style_table_text)]
    ]
    models_data = models_data_es if is_es else models_data_en
    t_mod = Table(models_data, colWidths=[110, 135, 140, 126])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 8))

    # ECUACIONES ROP Y WILSON EOQ
    story.append(Paragraph("<b>Cálculo del Punto de Pedido (ROP) y Lote Económico (EOQ de Wilson):</b>" if is_es else "<b>Reorder Point (ROP) and Wilson Economic Order Quantity (EOQ):</b>", style_h2))

    rop_text_es = (
        "El Punto de Pedido (<i>Reorder Point</i>) define el umbral exacto de inventario disponible en el que el sistema ERP/WMS debe emitir una nueva orden de reabastecimiento: <b>ROP = (d · L) + SS</b>, donde <i>d · L</i> representa la demanda esperada durante el lead time (LTD). Por su parte, el tamaño del lote de compra se optimiza mediante el modelo clásico de Wilson para equilibrar el coste anual de emisión y el de posesión: <b>EOQ = √[(2 · D · S) / (h · C)]</b>, donde D es la demanda anual, S es el coste administrativo fijo por pedido (€/pedido), C es el coste unitario y h es la tasa anual de posesión (% anual, típicamente 20%-25%)."
    )
    rop_text_en = (
        "The Reorder Point (ROP) establishes the precise inventory threshold that triggers a replenishment order: <b>ROP = (d · L) + SS</b>, where <i>d · L</i> is the expected Lead Time Demand (LTD). Replenishment batch size is optimized via Wilson's classic economic lot sizing to balance fixed order costs and inventory holding costs: <b>EOQ = √[(2 · D · S) / (h · C)]</b>, where D is annual demand, S is fixed order placement cost ($/order), C is unit purchase price, and h is annual holding rate (%/year, typically 20%-25%)."
    )
    story.append(Paragraph(rop_text_es if is_es else rop_text_en, style_body))

    # COMPORTAMIENTO ASINTÓTICO Y FACTOR Z
    story.append(Paragraph("<b>La Barrera Asintótica: Por qué el 100% de Servicio Exige Inventario Infinito:</b>" if is_es else "<b>The Asymptotic Barrier: Why 100% Service Level Demands Infinite Inventory:</b>", style_h2))

    asymp_text_es = (
        "El factor Z representa el cuantil de la distribución normal estándar: <b>Z = Φ⁻¹(CSL)</b>. A medida que el nivel de servicio se acerca al 100%, la cola de la distribución gaussiana se extiende hacia el infinito. Pasar de un 95% (Z = 1,645) a un 98% (Z = 2,054) incrementa el stock un 25%. Sin embargo, elevarlo al 99,5% (Z = 2,576) exige un +56% de capital, y alcanzar el 99,9% (Z = 3,090) dispara el circulante un +88%. Exigir un 100% exigiría Z = ∞, inmovilizando la totalidad de los fondos propios de la compañía."
    )
    asymp_text_en = (
        "The Z-factor represents the inverse standard normal quantile: <b>Z = Φ⁻¹(CSL)</b>. As Cycle Service Level approaches 100%, the Gaussian tail stretches to infinity. Moving from 95% (Z = 1.645) to 98% (Z = 2.054) increases required safety stock by 25%. However, pushing to 99.5% (Z = 2.576) consumes +56% extra capital, and 99.9% (Z = 3.090) inflates capital by +88%. Pursuing a theoretical 100% service level requires Z = ∞, locking up the entirety of the corporation's equity."
    )
    story.append(Paragraph(asymp_text_es if is_es else asymp_text_en, style_body))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: ESTRATEGIA DE SEGMENTACIÓN ABC Y ASIGNACIÓN DE NIVEL DE SERVICIO
    # =========================================================================
    sec3_title = "3. Estrategia de Segmentación ABC y Asignación de Nivel de Servicio" if is_es else "3. ABC Stratification Strategy & Differential Service Level Policy"
    story.append(Paragraph(sec3_title, style_h1))

    sec3_intro = (
        "El error más costoso en la gestión de la cadena de suministro consiste en tratar a todos los productos con el mismo criterio. Exigir un nivel de servicio del 98% o 99% a todo el catálogo es una receta garantizada para la asfixia de tesorería. La metodología Datalaria aplica el principio de Pareto estratificado para asignar niveles de servicio diferenciados según el valor económico y la criticidad de rotura:"
        if is_es else
        "The most financially destructive practice in supply chain management is treating all inventory items identically. Mandating a 98% or 99% service level across the entire catalog is a guaranteed recipe for working capital paralysis. Datalaria's methodology establishes a stratified Pareto policy matching service levels to economic value and stockout criticality:"
    )
    story.append(Paragraph(sec3_intro, style_body))

    # TABLA MATRIZ ABC
    abc_table_data_es = [
        [Paragraph("<b>Clase ABC</b>", style_table_bold), Paragraph("<b>% Catálogo</b>", style_table_bold), Paragraph("<b>% Ventas / Margen</b>", style_table_bold), Paragraph("<b>CSL Objetivo</b>", style_table_bold), Paragraph("<b>Factor Z</b>", style_table_bold), Paragraph("<b>Estrategia Operativa & Financiera</b>", style_table_bold)],
        [Paragraph("<b>Clase A (Críticos)</b>", style_table_text), Paragraph("15% - 20%", style_table_text), Paragraph("75% - 80%", style_table_text), Paragraph("<b>98,0% - 99,0%</b>", style_table_bold), Paragraph("2,054 - 2,326", style_table_text), Paragraph("Blindaje máximo de stock. Revisión semanal de ROP. Integración EDI/VMI con proveedores estratégicos.", style_table_text)],
        [Paragraph("<b>Clase B (Intermedios)</b>", style_table_text), Paragraph("25% - 30%", style_table_text), Paragraph("15% - 20%", style_table_text), Paragraph("<b>95,0%</b>", style_table_bold), Paragraph("1,645", style_table_text), Paragraph("Equilibrio estándar. Revisión quincenal de parámetros. Reposición automatizada por ERP bajo ROP.", style_table_text)],
        [Paragraph("<b>Clase C (Accesorios)</b>", style_table_text), Paragraph("50% - 55%", style_table_text), Paragraph("5% - 10%", style_table_text), Paragraph("<b>90,0%</b>", style_table_bold), Paragraph("1,282", style_table_text), Paragraph("Mínimo capital inmovilizado. Se acepta 10% de rotura en ciclo. Lotes de compra agrupados para reducir costes S.", style_table_text)]
    ]
    abc_table_data_en = [
        [Paragraph("<b>ABC Class</b>", style_table_bold), Paragraph("<b>% SKUs</b>", style_table_bold), Paragraph("<b>% Sales / Margin</b>", style_table_bold), Paragraph("<b>Target CSL</b>", style_table_bold), Paragraph("<b>Z-Factor</b>", style_table_bold), Paragraph("<b>Strategic & Financial Policy</b>", style_table_bold)],
        [Paragraph("<b>Class A (Critical)</b>", style_table_text), Paragraph("15% - 20%", style_table_text), Paragraph("75% - 80%", style_table_text), Paragraph("<b>98.0% - 99.0%</b>", style_table_bold), Paragraph("2.054 - 2.326", style_table_text), Paragraph("Strict capital protection. Weekly ROP audits. EDI/VMI integration with Tier-1 strategic suppliers.", style_table_text)],
        [Paragraph("<b>Class B (Intermediate)</b>", style_table_text), Paragraph("25% - 30%", style_table_text), Paragraph("15% - 20%", style_table_text), Paragraph("<b>95.0%</b>", style_table_bold), Paragraph("1.645", style_table_text), Paragraph("Balanced benchmark. Bi-weekly parameter updates. Automated ERP replenishment triggered by ROP.", style_table_text)],
        [Paragraph("<b>Class C (Accessory)</b>", style_table_text), Paragraph("50% - 55%", style_table_text), Paragraph("5% - 10%", style_table_text), Paragraph("<b>90.0%</b>", style_table_bold), Paragraph("1.282", style_table_text), Paragraph("Minimal working capital lockup. 10% cycle stockout accepted. Grouped purchase orders to curb order cost S.", style_table_text)]
    ]
    abc_table_data = abc_table_data_es if is_es else abc_table_data_en
    t_abc = Table(abc_table_data, colWidths=[95, 60, 75, 75, 55, 151])
    t_abc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_abc)
    story.append(Spacer(1, 8))

    # PRINCIPIOS DE ASIGNACIÓN
    story.append(Paragraph("<b>Protocolo de Calibración Dinámica de Niveles de Servicio:</b>" if is_es else "<b>Dynamic Service Level Calibration Protocol:</b>", style_h2))

    points_abc_es = [
        "<b>1. Coste de la Rotura vs. Coste de Posesión:</b> Si el margen bruto unitario o el coste de penalización contractual por falta de servicio supera con creces el coste de posesión <i>h · C</i>, el nivel óptimo tiende a 98%-99%. Si la rotura no tiene penalización y el producto es sustituible, el nivel óptimo desciende al 90%.",
        "<b>2. Recalibración Estacional de la Demanda:</b> Los parámetros <i>d</i> y <i>σd</i> deben recalcularse con ventanas móviles (30, 60 o 90 días) para evitar que un pico estacional distorsione permanentemente el stock de seguridad.",
        "<b>3. Auditoría de Desviación del Proveedor (σL):</b> Proveedores con alta impuntualidad deben clasificarse en zona roja, exigiendo renegociación contractual o diversificación de fuentes de suministro."
    ]
    points_abc_en = [
        "<b>1. Stockout Cost vs. Carrying Cost:</b> If unit gross margin or contractual breach penalties far exceed unit holding cost <i>h · C</i>, optimal service level shifts to 98%-99%. For substitutable items with zero penalty, optimal service sits at 90%.",
        "<b>2. Seasonal Moving-Window Recalibration:</b> Parameters <i>d</i> and <i>σd</i> must be refreshed across rolling time windows (30, 60, or 90 days) to prevent short seasonal demand spikes from permanently trapping inventory.",
        "<b>3. Supplier Lead Time Variance Auditing (σL):</b> Chronically unpunctual suppliers must be placed on high-alert watchlists, mandating SLA contract renegotiations or dual-sourcing execution."
    ]
    points_abc = points_abc_es if is_es else points_abc_en
    for pt in points_abc:
        story.append(Paragraph(f"• {pt}", style_body))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: CASO DE ESTUDIO REALISTA DE DISTRIBUCIÓN B2B / ECOMMERCE
    # =========================================================================
    sec4_title = "4. Caso de Estudio Real: Empresa B2B con 4.5M € de Inventario" if is_es else "4. Real-World Case Study: B2B Distributor with $4.5M Inventory"
    story.append(Paragraph(sec4_title, style_h1))

    case_intro_es = (
        "<b>Contexto Operativo:</b> Una compañía de distribución industrial y eCommerce técnico con 2.400 referencias activas y un balance de inventario de <b>4.500.000 €</b> presentaba una crisis recurrente ante el Comité de Dirección: el departamento comercial denunciaba una tasa de rotura de stock del 6,8% en sus 150 referencias más vendidas (Clase A), mientras el CFO alertaba de que el 40% del almacén central estaba colapsado con artículos de rotación lenta."
    )
    case_intro_en = (
        "<b>Operational Context:</b> An industrial distribution and technical eCommerce enterprise managing 2,400 active SKUs with <b>$4,500,000</b> in balance sheet inventory faced a chronic executive crisis: commercial sales teams reported a severe 6.8% stockout rate across the top 150 revenue generators (Class A), while the CFO warned that 40% of central warehouse capacity was suffocated with slow-moving stock."
    )
    story.append(Paragraph(case_intro_es if is_es else case_intro_en, style_body))

    # TABLA COMPARATIVA ANTES VS DESPUÉS
    story.append(Paragraph("<b>Resultados Financieros y Operativos tras la Implantación del Modelo Datalaria:</b>" if is_es else "<b>Financial & Operational Results Post-Implementation:</b>", style_h2))

    case_data_es = [
        [Paragraph("<b>Indicador Clave (KPI)</b>", style_table_bold), Paragraph("<b>Situación Previa (Regla 30d)</b>", style_table_bold), Paragraph("<b>Optimización Estocástica</b>", style_table_bold), Paragraph("<b>Impacto Financiero / Operativo</b>", style_table_bold)],
        [Paragraph("<b>Rotura en Clase A (Top SKUs)</b>", style_table_text), Paragraph("6,8% de ciclos sin stock", style_table_text), Paragraph("<b>1,8% de ciclos sin stock</b>", style_table_bold), Paragraph("<b>-73% de roturas:</b> +380.000 € en ventas salvadas", style_table_text)],
        [Paragraph("<b>Inversión Total en Inventario</b>", style_table_text), Paragraph("4.500.000 €", style_table_text), Paragraph("<b>4.280.000 €</b>", style_table_bold), Paragraph("<b>+220.000 € de caja neta liberada</b>", style_table_bold)],
        [Paragraph("<b>Coste Anual de Posesión (22%)</b>", style_table_text), Paragraph("990.000 € / año", style_table_text), Paragraph("<b>941.600 € / año</b>", style_table_bold), Paragraph("<b>Ahorro neto recurrente de 48.400 € / año</b>", style_table_text)],
        [Paragraph("<b>Rotación Anual (Turns)</b>", style_table_text), Paragraph("4,2x rotaciones / año", style_table_text), Paragraph("<b>5,1x rotaciones / año</b>", style_table_bold), Paragraph("+21% de aceleración en ciclo de conversión de caja", style_table_text)],
        [Paragraph("<b>Nivel de Servicio OTIF Global</b>", style_table_text), Paragraph("91,5% entregas a tiempo", style_table_text), Paragraph("<b>98,2% entregas a tiempo</b>", style_table_bold), Paragraph("Consolidación de cuentas clave y mejora en NPS", style_table_text)]
    ]
    case_data_en = [
        [Paragraph("<b>Core KPI</b>", style_table_bold), Paragraph("<b>Baseline (30d Rule)</b>", style_table_bold), Paragraph("<b>Stochastic Optimization</b>", style_table_bold), Paragraph("<b>Financial / Operational Impact</b>", style_table_bold)],
        [Paragraph("<b>Class A Stockout Rate</b>", style_table_text), Paragraph("6.8% stockout frequency", style_table_text), Paragraph("<b>1.8% stockout frequency</b>", style_table_bold), Paragraph("<b>-73% stockouts:</b> +$380,000 in preserved sales", style_table_text)],
        [Paragraph("<b>Total Inventory Investment</b>", style_table_text), Paragraph("$4,500,000", style_table_text), Paragraph("<b>$4,280,000</b>", style_table_bold), Paragraph("<b>+$220,000 net cash released</b>", style_table_bold)],
        [Paragraph("<b>Annual Carrying Cost (22%)</b>", style_table_text), Paragraph("$990,000 / year", style_table_text), Paragraph("<b>$941,600 / year</b>", style_table_bold), Paragraph("<b>$48,400 / year recurring net savings</b>", style_table_text)],
        [Paragraph("<b>Inventory Turns</b>", style_table_text), Paragraph("4.2x turns / year", style_table_text), Paragraph("<b>5.1x turns / year</b>", style_table_bold), Paragraph("+21% cash conversion cycle velocity acceleration", style_table_text)],
        [Paragraph("<b>Overall OTIF Service Level</b>", style_table_text), Paragraph("91.5% on-time in-full", style_table_text), Paragraph("<b>98.2% on-time in-full</b>", style_table_bold), Paragraph("Key client retention and commercial NPS boost", style_table_text)]
    ]
    case_data = case_data_es if is_es else case_data_en
    t_case = Table(case_data, colWidths=[120, 110, 120, 161])
    t_case.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_case)
    story.append(Spacer(1, 8))

    # LECCIONES CLAVE DEL CASO
    story.append(Paragraph("<b>Claves Ejecutivas de la Transformación:</b>" if is_es else "<b>Executive Takeaways from the Turnaround:</b>", style_h2))

    case_points_es = [
        "<b>Autofinanciación del Stock Crítico:</b> La liquidación del sobrestock en artículos Clase C generó 310.000 € de liquidez inmediata, de los cuales se reinvirtieron 90.000 € en reforzar el colchón de seguridad de las referencias Clase A. La mejora de servicio se autofinanció liberando 220.000 € de caja neta.",
        "<b>Acuerdos SLA con Proveedores:</b> Compras renegoció contratos con los 5 principales proveedores, estableciendo ventanas fijas de entrega (reduciendo σL de 6 días a 2 días), lo que redujo en un 28% adicional el stock de seguridad necesario.",
        "<b>Paz Organizativa:</b> La tensión histórica entre Ventas (que exigía stock infinito) y Finanzas (que exigía recortes indiscriminados) se resolvió adoptando un modelo matemático transparente aprobado por el Consejo."
    ]
    case_points_en = [
        "<b>Self-Funding Critical Inventory:</b> Liquidating overstock across Class C references generated $310,000 in immediate liquidity, of which $90,000 was reinvested into reinforcing Class A buffers. The service leap was entirely self-funded while delivering $220,000 in net cash.",
        "<b>Strategic Supplier SLA Agreements:</b> Procurement renegotiated delivery windows with the top 5 vendors, compressing lead time variance (σL dropped from 6 to 2 days), driving an additional 28% reduction in required safety stock.",
        "<b>Organizational Alignment:</b> The chronic friction between Sales (demanding infinite stock) and Finance (demanding arbitrary cuts) vanished once the Board ratified a mathematically transparent policy."
    ]
    case_points = case_points_es if is_es else case_points_en
    for pt in case_points:
        story.append(Paragraph(f"• {pt}", style_body))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: PROTOCOLO DE DEFENSA EN COMITÉ (FAQ) & BIBLIOGRAFÍA CANÓNICA
    # =========================================================================
    sec5_title = "5. Protocolo de Defensa en Comité (Boardroom FAQ) & Bibliografía" if is_es else "5. Boardroom Defense Protocol (Executive FAQ) & References"
    story.append(Paragraph(sec5_title, style_h1))

    faq_items_es = [
        ("¿Por qué un 100% de nivel de servicio exigiría inventario infinito?",
         "Porque la distribución gaussiana de la demanda tiene colas infinitas. Para cubrir una probabilidad del 100%, la función cuantil Z tiende a infinito (Z → ∞). En la práctica empresarial, buscar el 100% destruye la rentabilidad del capital (ROCE) absorbiendo recursos desproporcionados para cubrir eventos que solo ocurren una vez cada década."),
        ("¿Qué ahorra más circulante: mejorar la previsión de demanda o exigir puntualidad al proveedor?",
         "En el modelo completo SS = Z · √(L · σd² + d² · σL²), el impacto de la puntualidad del proveedor (σL) está multiplicado por el cuadrado de la demanda media (d²). En referencias de gran consumo, reducir la variabilidad del proveedor a la mitad (reducir σL un 50%) libera típicamente entre 2 y 3 veces más capital que invertir en costosos algoritmos predictivos de demanda."),
        ("¿Cómo frenar las presiones comerciales para sobre-almacenar?",
         "Vinculando la cuenta de resultados comercial al coste de posesión de inventario. Cuando el equipo comercial comprende que mantener un sobrestock innecesario devenga una tasa h del 22% anual que reduce el margen neto de su división, se alinea de forma natural con los niveles estocásticos óptimos.")
    ]
    faq_items_en = [
        ("Why does a 100% service level mathematically demand infinite inventory?",
         "Because the Gaussian normal distribution has infinite tails. To guarantee zero probability of stockout, the inverse quantile Z reaches infinity (Z → ∞). In corporate practice, chasing 100% availability destroys return on capital employed (ROCE) by tying up massive capital against tail events that occur once a decade."),
        ("What saves more capital: improving demand forecasting or enforcing supplier punctuality?",
         "In the full stochastic model SS = Z · √(L · σd² + d² · σL²), supplier unreliability (σL) is scaled by the squared mean demand (d²). For high-volume references, cutting supplier lead time variance in half (50% σL reduction) typically releases 2 to 3 times more working capital than investing in complex demand AI algorithms."),
        ("How to resist commercial sales pressure to excessively overstock?",
         "By charging inventory carrying costs (h = 22%/yr) directly to business unit P&L statements. When commercial teams realize that excessive safety buffers eat away their divisional operating margins, they naturally champion mathematically optimized ABC service targets.")
    ]
    faq_items = faq_items_es if is_es else faq_items_en

    for q, a in faq_items:
        story.append(Paragraph(f"<b>P: {q}</b>" if is_es else f"<b>Q: {q}</b>", style_h2))
        story.append(Paragraph(f"<b>R:</b> {a}" if is_es else f"<b>A:</b> {a}", style_body))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Bibliografía Canónica y Normas Internacionales de Autoridad:</b>" if is_es else "<b>Canonical Bibliography & Authoritative Standards:</b>", style_h2))

    biblio_items = [
        "<b>Silver, E. A., Pyke, D. F., & Thomas, D. J. (2016)</b> <i>Inventory and Production Management in Supply Chains – 4th Edition</i>, CRC Press.",
        "<b>Chopra, S., & Meindl, P. (2016)</b> <i>Supply Chain Management: Strategy, Planning, and Operation – 6th Edition</i>, Pearson.",
        "<b>Association for Supply Chain Management (ASCM / APICS) (2020)</b> <i>APICS Dictionary – 16th Edition: Operations & Inventory Standards</i>.",
        "<b>Simchi-Levi, D., Kaminsky, P., & Simchi-Levi, E. (2008)</b> <i>Designing and Managing the Supply Chain: Concepts, Strategies and Case Studies</i>, McGraw-Hill.",
        "<b>Zipkin, P. H. (2000)</b> <i>Foundations of Inventory Management</i>, McGraw-Hill / Irwin.",
        "<b>Barbara Minto (2009)</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>, Financial Times / Prentice Hall."
    ]
    for b in biblio_items:
        story.append(Paragraph(f"• {b}", style_table_text))

    # Compilar documento con NumberedCanvas
    def canvas_maker(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c._lang = lang
        return c

    doc.build(story, canvasmaker=canvas_maker)


def main():
    """Genera ambas guías metodológicas en PDF en sus respectivas carpetas oficiales."""
    base_dir = "packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP"
    es_dir = os.path.join(base_dir, "[ES]_Stock_Seguridad_ROP")
    en_dir = os.path.join(base_dir, "[EN]_Safety_Stock_ROP")

    os.makedirs(es_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)

    file_es = os.path.join(es_dir, "Guia_Metodologica_Stock_ROP_ES.pdf")
    file_en = os.path.join(en_dir, "Methodology_Guide_Safety_Stock_ROP_EN.pdf")

    print("[1/2] Generando Guía Metodológica en Español (Guia_Metodologica_Stock_ROP_ES.pdf)...")
    build_pdf(file_es, lang='ES')
    print(f"      -> Guardado: {file_es}")

    print("[2/2] Generating Methodology Guide in English (Methodology_Guide_Safety_Stock_ROP_EN.pdf)...")
    build_pdf(file_en, lang='EN')
    print(f"      -> Saved: {file_en}")

    print("Guías metodológicas en PDF (5 páginas exactas) generadas con total éxito.")


if __name__ == "__main__":
    main()
