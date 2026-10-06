#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para el Executive Decision Pack RICE & ICE:
1. packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[ES]_Matriz_RICE_ICE/Guia_Metodologica_RICE_ICE_ES.pdf (Versión en Español)
2. packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[EN]_RICE_ICE_Matrix/Methodology_Guide_RICE_ICE_EN.pdf (Versión en Inglés)

Estándar editorial de alta dirección (McKinsey / BCG / Intercom):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (El Coste Oculto de la Priorización por Opinión y el Síndrome HiPPO).
- Página 2: Sección 2 (Fundamentación Matemática: Score RICE, Confianza Bayesiana, ICE de Growth, Normalización y Problema de la Mochila).
- Página 3: Sección 3 (Protocolo de Calibración de Métricas: Reach Telemetría, Impacto Intercom, Confidence Meter de Gilad y Matriz RICE vs ICE).
- Página 4: Sección 4 (Caso Práctico Resuelto: Scale-Up SaaS Enterprise con 3 Squads, Quick Wins y Congelación de Pozos sin Fondo).
- Página 5: Sección 5 (Board Defense Protocol: 5 Preguntas Difíciles del Comité de Dirección) y Referencias Bibliográficas Canónicas.
- Paginación dinámica con NumberedCanvas ("Página X de Y" / "Page X of Y") y soporte datalaria@gmail.com.
"""

import os
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

C_GREEN_ACCENT = colors.HexColor("#10B981") # Emerald 500
C_GREEN_LIGHT = colors.HexColor("#D1FAE5")  # Emerald 100
C_GREEN_TEXT = colors.HexColor("#065F46")   # Emerald 800

C_AMBER_ACCENT = colors.HexColor("#F59E0B") # Amber 500
C_AMBER_LIGHT = colors.HexColor("#FEF3C7")  # Amber 100
C_AMBER_TEXT = colors.HexColor("#92400E")   # Amber 800

C_RED_ACCENT = colors.HexColor("#EF4444")   # Red 500
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
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        cur_page = self._pageNumber
        lang = getattr(self, '_lang', 'ES')

        # Cabecera en páginas 2 en adelante
        if cur_page > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(C_SLATE_MUTED)
            self.drawString(42, 805, "DATALARIA | EXECUTIVE DECISION PACK")
            header_right = (
                "MATRIZ RICE & ICE: PRIORIZACIÓN ÁGIL & LÍNEA DE CORTE DE CAPACIDAD"
                if lang == 'ES' else
                "RICE & ICE MATRIX: AGILE PRIORITIZATION & CAPACITY CUT-LINE"
            )
            self.drawRightString(553, 805, header_right)
            self.setStrokeColor(C_BORDER_LIGHT)
            self.setLineWidth(0.75)
            self.line(42, 798, 553, 798)

        # Pie de página en todas las páginas
        self.setStrokeColor(C_BORDER_LIGHT)
        self.setLineWidth(0.75)
        self.line(42, 45, 553, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(C_SLATE_MUTED)
        footer_left = (
            "Datalaria.com • Soporte: datalaria@gmail.com • Confidencial C-Level"
            if lang == 'ES' else
            "Datalaria.com • Support: datalaria@gmail.com • Confidential C-Level"
        )
        self.drawString(42, 32, footer_left)
        page_str = f"Página {cur_page} de {total_pages}" if lang == 'ES' else f"Page {cur_page} of {total_pages}"
        self.drawRightString(553, 32, page_str)

        self.restoreState()


def get_custom_styles():
    base = getSampleStyleSheet()

    styles = {
        'CoverKicker': ParagraphStyle(
            'CoverKicker', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=11,
            textColor=C_BLUE_ACCENT, spaceAfter=4, textTransform='uppercase'
        ),
        'CoverTitle': ParagraphStyle(
            'CoverTitle', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=18, leading=22,
            textColor=C_NAVY_DARK, spaceAfter=6
        ),
        'CoverSub': ParagraphStyle(
            'CoverSub', parent=base['Normal'],
            fontName='Helvetica', fontSize=9.0, leading=12.5,
            textColor=C_SLATE_MUTED, spaceAfter=8
        ),
        'SecHeading': ParagraphStyle(
            'SecHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=10.5, leading=13.5,
            textColor=C_NAVY_DARK, spaceBefore=5, spaceAfter=3,
            keepWithNext=True
        ),
        'SubSecHeading': ParagraphStyle(
            'SubSecHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=9.0, leading=11.5,
            textColor=C_BLUE_ACCENT, spaceBefore=4, spaceAfter=2,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.2, leading=11.2,
            textColor=C_NAVY_MED, spaceAfter=4
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.2, leading=11.2,
            textColor=C_NAVY_DARK, spaceAfter=4
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.0, leading=11.0,
            textColor=C_NAVY_DARK
        ),
        'FormulaText': ParagraphStyle(
            'FormulaText', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=9.0, leading=12.0,
            textColor=C_NAVY_DARK, alignment=1
        ),
        'TableText': ParagraphStyle(
            'TableText', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.5, leading=9.5,
            textColor=C_NAVY_DARK
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.5, leading=9.5,
            textColor=C_WHITE, alignment=1
        ),
        'BibItem': ParagraphStyle(
            'BibItem', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.2, leading=9.2,
            textColor=C_SLATE_MUTED, spaceAfter=3
        ),
    }
    return styles


def make_callout(text, styles, bg_color=C_BLUE_LIGHT, border_color=C_BLUE_ACCENT, width=511):
    p = Paragraph(text, styles['CalloutText'])
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 1.0, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


def make_formula_box(formula_html, styles, width=511):
    p = Paragraph(formula_html, styles['FormulaText'])
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BLUE_LIGHT),
        ('BOX', (0,0), (-1,-1), 1.2, C_BLUE_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t


def build_pdf_story(lang='ES'):
    styles = get_custom_styles()
    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA & SECCIÓN 1 (EL COSTE OCULTO DE LA PRIORIZACIÓN POR OPINIÓN)
    # =========================================================================
    kicker = "SUITE 02: TOMA DE DECISIONES & PRIORIZACIÓN • ESTÁNDAR INTERCOM & GROWTH ICE" if lang == 'ES' else "SUITE 02: DECISION ANALYSIS & PRIORITIZATION • INTERCOM & GROWTH ICE STANDARD"
    story.append(Paragraph(kicker, styles['CoverKicker']))

    title = "MATRIZ RICE & ICE DE PRIORIZACIÓN ÁGIL" if lang == 'ES' else "AGILE RICE & ICE PRIORITIZATION MATRIX"
    story.append(Paragraph(title, styles['CoverTitle']))

    sub = (
        "Backlog Cuantitativo, Matriz Impacto vs. Esfuerzo & Línea de Corte de Capacidad: "
        "Fundamentación Matemática, Protocolo de Calibración de Confianza y Gobierno del Product Council."
        if lang == 'ES' else
        "Quantitative Backlog, Impact vs. Effort Matrix & Capacity Cut-Line: "
        "Mathematical Foundations, Confidence Calibration Protocol, and C-Suite Product Council Governance."
    )
    story.append(Paragraph(sub, styles['CoverSub']))

    # Metadata Card
    meta_text = (
        "<b>Ámbito:</b> Portfolio B2B SaaS Enterprise & Scale-ups &nbsp;|&nbsp; "
        "<b>Versión:</b> 2026.1 &nbsp;|&nbsp; "
        "<b>Autor:</b> Datalaria Strategic Advisory &nbsp;|&nbsp; "
        "<b>Contacto:</b> datalaria@gmail.com"
        if lang == 'ES' else
        "<b>Scope:</b> Enterprise B2B SaaS & Tech Scale-ups &nbsp;|&nbsp; "
        "<b>Edition:</b> 2026.1 &nbsp;|&nbsp; "
        "<b>Author:</b> Datalaria Strategic Advisory &nbsp;|&nbsp; "
        "<b>Support:</b> datalaria@gmail.com"
    )
    story.append(make_callout(meta_text, styles, bg_color=C_BG_CARD, border_color=C_BORDER_LIGHT))
    story.append(Spacer(1, 8))

    # SECCIÓN 1
    s1_title = "1. El Coste Oculto de la Priorización por Opinión y la Fábrica de Funcionalidades" if lang == 'ES' else "1. The Hidden Cost of Opinion-Based Prioritization & The Feature Factory"
    story.append(Paragraph(s1_title, styles['SecHeading']))

    s1_p1 = (
        "En la gestión moderna de producto y tecnología, las organizaciones se enfrentan de manera crónica a la "
        "denominada <b>'trampa de la última milla de priorización'</b>: a pesar de contar con metodologías ágiles "
        "(Scrum, Kanban) para la entrega de software, el proceso que decide <i>qué</i> se construye sigue dominado "
        "por la intuición no fundamentada, compromisos comerciales improvisados y la opinión del directivo mejor remunerado "
        "(síndrome <b>HiPPO</b>, <i>Highest Paid Person's Opinion</i>). Las consecuencias económicas son devastadoras:"
        if lang == 'ES' else
        "In modern product engineering and technical leadership, organizations chronically fall into the "
        "<b>'prioritization last-mile trap'</b>: while agile delivery frameworks (Scrum, Kanban) optimize velocity, "
        "the decision of <i>what</i> gets built remains captive to unvalidated intuition, anecdotal sales promises, "
        "and the <b>HiPPO syndrome</b> (<i>Highest Paid Person's Opinion</i>). The corporate toll is severe:"
    )
    story.append(Paragraph(s1_p1, styles['Body']))

    s1_bullets_es = (
        "• <b>La Fábrica de Funcionalidades (Feature Factory):</b> Equipos de desarrollo medidos por volumen de código "
        "desplegado en lugar de valor económico capturado, acumulando deuda técnica y funcionalidades zombi.<br/>"
        "• <b>El Sesgo de lo Reciente y la Anécdota Comercial:</b> Una conversación aislada con un cliente corporativo "
        "o la última objeción de ventas altera abruptamente el roadmap, canibalizando iniciativas estructurales.<br/>"
        "• <b>El Coste de Oportunidad de la Capacidad Mal Asignada:</b> Cada persona-mes invertido en un proyecto de bajo "
        "retorno es un persona-mes sustraído a las palancas críticas de conversión, retención neta (NRR) y defensibilidad."
    )
    s1_bullets_en = (
        "• <b>The Feature Factory Pathology:</b> Engineering measured on deployment throughput rather than verified business "
        "outcomes, generating product bloat, maintenance overhead, and unadopted zombie features.<br/>"
        "• <b>Recency Bias & The Squeaky-Wheel Trap:</b> An isolated enterprise RFP negotiation or direct executive demand "
        "hijacks quarterly sprints, derailing cross-cutting strategic initiatives without validation.<br/>"
        "• <b>The Opportunity Cost of Misallocated Engineering:</b> Every person-month spent on a marginal pet project "
        "is a person-month stripped from core conversion, net revenue retention (NRR), and competitive moats."
    )
    story.append(Paragraph(s1_bullets_es if lang == 'ES' else s1_bullets_en, styles['Body']))
    story.append(Spacer(1, 4))

    callout_p1 = (
        "<b>Mandato Metodológico del Product Council:</b> Sustituir el debate retórico por un motor analítico dual: "
        "la puntuación <b>RICE</b> (Reach × Impact × Confidence / Effort) para la asignación del roadmap estructural "
        "de ingeniería y la puntuación <b>ICE</b> (Impact × Confidence × Ease) para la experimentación ágil de crecimiento."
        if lang == 'ES' else
        "<b>Product Council Governance Mandate:</b> Replace rhetorical debates with a dual quantitative engine: "
        "<b>RICE</b> (Reach × Impact × Confidence / Effort) for structural engineering roadmap allocation, and "
        "<b>ICE</b> (Impact × Confidence × Ease) for fast-cycle growth experimentation and hypothesis de-risking."
    )
    story.append(make_callout(callout_p1, styles, bg_color=C_GREEN_LIGHT, border_color=C_GREEN_ACCENT))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: SECCIÓN 2 (FUNDAMENTACIÓN MATEMÁTICA DEL MODELO RICE & ICE)
    # =========================================================================
    s2_title = "2. Fundamentación Matemática: Densidad de Valor, Riesgo Bayesiano & Mochila" if lang == 'ES' else "2. Mathematical Foundations: Value Density, Bayesian Risk & The Knapsack Cut"
    story.append(Paragraph(s2_title, styles['SecHeading']))

    s2_p1 = (
        "El modelo cuantitativo de Datalaria formaliza la priorización como un problema formal de <b>densidad de valor "
        "esperado</b> bajo restricciones lineales de capacidad técnica finita."
        if lang == 'ES' else
        "The Datalaria quantitative framework models portfolio prioritization as an optimization of <b>expected "
        "value density</b> subject to finite engineering capacity constraints."
    )
    story.append(Paragraph(s2_p1, styles['Body']))

    # Fórmula RICE
    f_rice_html = (
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Puntuación RICE Canónica:</b>&nbsp;&nbsp;&nbsp;&nbsp;"
        "RICE = ( R · I · C ) / E"
    )
    story.append(make_formula_box(f_rice_html, styles))
    story.append(Spacer(1, 4))

    s2_expl_es = (
        "• <b>Reach (R):</b> Alcance medido en número absoluto de usuarios, cuentas o eventos impactados por trimestre.<br/>"
        "• <b>Impact (I):</b> Multiplicador de impacto en la métrica core: Masivo (3.0), Alto (2.0), Medio (1.0), Bajo (0.5), Mínimo (0.25).<br/>"
        "• <b>Confidence (C):</b> Factor de descuento de riesgo probatorio: <i>C ∈ [0.5, 1.0]</i> (Alta = 100%, Media = 80%, Baja = 50%).<br/>"
        "• <b>Effort (E):</b> Inversión combinada de producto, UX e ingeniería en <b>Persona-Mes (PM)</b> dedicados."
    )
    s2_expl_en = (
        "• <b>Reach (R):</b> Volume of unique users, accounts, or core events affected over the quarterly execution window.<br/>"
        "• <b>Impact (I):</b> Standard multiplier on target metric: Massive (3.0), High (2.0), Medium (1.0), Low (0.5), Minimal (0.25).<br/>"
        "• <b>Confidence (C):</b> Bayesian risk discount factor: <i>C ∈ [0.5, 1.0]</i> (High = 100%, Medium = 80%, Low = 50%).<br/>"
        "• <b>Effort (E):</b> Cross-functional product, design, and engineering delivery investment in <b>Person-Months (PM)</b>."
    )
    story.append(Paragraph(s2_expl_es if lang == 'ES' else s2_expl_en, styles['Body']))
    story.append(Spacer(1, 4))

    # Subsección Confianza y ICE
    s2_sub1 = "2.1. La Confianza como Descuento Bayesiano de Incertidumbre" if lang == 'ES' else "2.1. Confidence as a Bayesian Uncertainty Deflator"
    story.append(Paragraph(s2_sub1, styles['SubSecHeading']))
    s2_conf_txt = (
        "El producto <i>V = R · I</i> representa el valor nominal hipotético. En la práctica ejecutiva, las estimaciones "
        "de impacto suelen estar infladas por optimismo cognitivo. El parámetro <i>C</i> actúa como una <b>probabilidad subjetiva "
        "de éxito respaldada por evidencia</b>. El valor esperado real es <i>E[V] = C · (R · I)</i>. Por tanto, una iniciativa con "
        "confianza baja del 50% sufre un castigo automático del 50% en su score final, neutralizando hipótesis especulativas."
        if lang == 'ES' else
        "The product <i>V = R · I</i> represents nominal hypothetical value. In executive practice, impact projections "
        "are systematically inflated by confirmation bias. Parameter <i>C</i> operates as an <b>evidence-backed subjective "
        "probability of realization</b>: <i>E[V] = C · (R · I)</i>. An unvalidated initiative with 50% confidence incurs an "
        "immediate 50% haircut on its prioritization score, protecting capital from speculative engineering bets."
    )
    story.append(Paragraph(s2_conf_txt, styles['Body']))

    # Subsección ICE y Normalización
    s2_sub2 = "2.2. Score ICE & Normalización Cuantitativa (0 - 100)" if lang == 'ES' else "2.2. ICE Growth Score & 0 - 100 Normalization"
    story.append(Paragraph(s2_sub2, styles['SubSecHeading']))
    f_ice_html = (
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Score ICE Multiplicativo:</b> ICE = I · C · E &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; "
        "<b>Normalización RICE:</b> RICE<sub>n</sub> = 100 · ( RICE<sub>i</sub> / max(RICE) )"
    )
    story.append(make_formula_box(f_ice_html, styles))
    story.append(Spacer(1, 4))

    # Subsección Línea de Corte y Problema de la Mochila
    s2_sub3 = "2.3. Línea de Corte de Capacidad: Aproximación Greedy a la Mochila" if lang == 'ES' else "2.3. Capacity Cut-Line: Greedy Knapsack Approximation"
    story.append(Paragraph(s2_sub3, styles['SubSecHeading']))
    s2_knap_txt = (
        "Asignar capacidad trimestral finita <i>K</i> entre <i>N</i> iniciativas candidatas equivale al <b>Problema de la "
        "Mochila Entero (0-1 Knapsack)</b>: maximizar ∑ V<sub>i</sub> sujeto a ∑ E<sub>i</sub> ≤ K. "
        "Dado que el problema es NP-Hard, ordenar de forma descendente por la densidad de valor RICE<sub>i</sub> = V<sub>i</sub> / E<sub>i</sub> "
        "constituye el <b>algoritmo greedy óptimo</b> con garantía de aproximación estricta. La línea de corte se establece "
        "en el punto donde el esfuerzo acumulado agota la capacidad neta disponible: ∑<sub>i=1</sub><sup>m</sup> E<sub>i</sub> ≤ K."
        if lang == 'ES' else
        "Allocating finite quarterly capacity <i>K</i> across <i>N</i> competing initiatives is mathematically isomorphic to the "
        "<b>0-1 Knapsack Problem</b>: maximize ∑ V<sub>i</sub> subject to ∑ E<sub>i</sub> ≤ K. "
        "Since the integer knapsack is NP-hard, ranking initiatives in descending order of value density RICE<sub>i</sub> = V<sub>i</sub> / E<sub>i</sub> "
        "provides the <b>canonical greedy approximation</b> with proven performance bounds. The capacity cut-line is strictly "
        "drawn where cumulative effort exhausts available net capacity: ∑<sub>i=1</sub><sup>m</sup> E<sub>i</sub> ≤ K."
    )
    story.append(Paragraph(s2_knap_txt, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: SECCIÓN 3 (PROTOCOLO DE CALIBRACIÓN DE MÉTRICAS & RÚBRICAS)
    # =========================================================================
    s3_title = "3. Protocolo de Calibración: Escalas Objetivas, Confidence Meter & RICE vs. ICE" if lang == 'ES' else "3. Calibration Protocol: Objective Scales, The Confidence Meter & RICE vs. ICE"
    story.append(Paragraph(s3_title, styles['SecHeading']))

    s3_p1 = (
        "La integridad de un motor cuantitativo depende de la objetividad de sus datos de entrada. "
        "Datalaria establece anclas rigurosas para erradicar la ambigüedad en los comités de producto:"
        if lang == 'ES' else
        "A quantitative decision engine is only as robust as its calibration governance. "
        "Datalaria establishes strict evidentiary anchors to eliminate subjectivity across product squads:"
    )
    story.append(Paragraph(s3_p1, styles['Body']))

    # Tabla de Escalas
    tbl_scales_data_es = [
        ["Factor", "Nivel / Etiqueta", "Valor", "Criterio de Evidencia & Estándar Requerido"],
        ["Impacto (I)", "Masivo / Massive", "3.0", "Multiplica x3 la métrica core o afecta a >80% de usuarios activos"],
        ["Impacto (I)", "Alto / High", "2.0", "Impacto sustancial en conversión, retención NRR o ingresos clave"],
        ["Impacto (I)", "Medio / Medium", "1.0", "Mejora perceptible pero acotada a un módulo secundario"],
        ["Impacto (I)", "Bajo / Low", "0.5", "Impacto marginal o cosmético con escasa tracción demostrada"],
        ["Impacto (I)", "Mínimo / Minimal", "0.25", "Ajuste puntual de bajísima tracción; evitar salvo bug crítico"],
        ["Confianza (C)", "Alta (100%)", "1.0", "Test A/B con p < 0.05, telemetría a escala o prototipo validado"],
        ["Confianza (C)", "Media (80%)", "0.8", "Encuesta a 50+ clientes B2B, datos de analítica o benchmark sólido"],
        ["Confianza (C)", "Baja (50%)", "0.5", "Intuición de producto, petición aislada de ventas o hipótesis no probada"],
    ]
    tbl_scales_data_en = [
        ["Factor", "Tier / Label", "Value", "Evidentiary Threshold & Required Validation"],
        ["Impact (I)", "Massive (3.0)", "3.0", "Triples core North Star metric or benefits >80% of active accounts"],
        ["Impact (I)", "High (2.0)", "2.0", "Substantial uplift in conversion, expansion ARR, or retention"],
        ["Impact (I)", "Medium (1.0)", "1.0", "Noticeable improvement across secondary workflow or single squad"],
        ["Impact (I)", "Low (0.5)", "0.5", "Marginal improvement in CSAT or non-blocking operational steps"],
        ["Impact (I)", "Minimal (0.25)", "0.25", "Minor cosmetic change; deprioritize unless critical statutory bug"],
        ["Confidence (C)", "High (100%)", "1.0", "Statistically significant A/B test (p < 0.05), telemetry, or UX test"],
        ["Confidence (C)", "Medium (80%)", "0.8", "50+ customer qualitative interviews, product analytics event logs"],
        ["Confidence (C)", "Low (50%)", "0.5", "Product intuition, unverified sales feedback, or anecdotal opinion"],
    ]
    tbl_scales_data = tbl_scales_data_es if lang == 'ES' else tbl_scales_data_en

    t_scales = Table(
        [[Paragraph(c, styles['TableHeader'] if r == 0 else styles['TableText']) for c in row] for r, row in enumerate(tbl_scales_data)],
        colWidths=[70, 75, 40, 326]
    )
    t_scales.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
    ]))
    story.append(t_scales)
    story.append(Spacer(1, 6))

    # Matriz Comparativa RICE vs. ICE
    s3_sub = "3.1. Matriz de Decisión: Cuándo Utilizar RICE vs. ICE" if lang == 'ES' else "3.1. Decision Matrix: When to Deploy RICE vs. ICE"
    story.append(Paragraph(s3_sub, styles['SubSecHeading']))

    tbl_comp_data_es = [
        ["Dimensión Metodológica", "Framework RICE (Intercom)", "Framework ICE (Sean Ellis / Growth)"],
        ["Horizonte Temporal", "Trimestral / Anual (Roadmap Estructural)", "Semanal / Quincenal (Sprints de Growth)"],
        ["Tipo de Iniciativas", "Épicas, grandes funcionalidades y arquitectura", "Experimentos rápidos, copys, A/B tests y flows"],
        ["Granularidad del Esfuerzo", "Persona-Mes (PM) de ingeniería y diseño", "Facilidad relativa (Ease) en escala 1 a 10"],
        ["Exigencia de Evidencia", "Telemetría formal y datos de analítica (C)", "Estimación ágil por el equipo de Growth"],
        ["Gobernanza Directiva", "Aprobación vinculante en Product Council", "Autonomía del squad de experimentación"],
    ]
    tbl_comp_data_en = [
        ["Methodological Dimension", "RICE Framework (Intercom)", "ICE Framework (Growth Hacking)"],
        ["Planning Horizon", "Quarterly / Annual (Structural Roadmap)", "Weekly / Bi-Weekly (Growth Test Sprints)"],
        ["Initiative Scope", "Major epics, cross-cutting features, platform", "Rapid micro-tests, copy variants, onboarding tweaks"],
        ["Effort Granularity", "Person-Months (PM) of cross-functional team", "Relative Ease score on a 1-to-10 scale"],
        ["Evidentiary Standard", "Formal telemetry logs and customer data (C)", "Agile consensus within the growth pod"],
        ["Governance Forum", "Binding C-Suite Product Council Gateway", "Autonomous squad-level continuous deployment"],
    ]
    tbl_comp_data = tbl_comp_data_es if lang == 'ES' else tbl_comp_data_en

    t_comp = Table(
        [[Paragraph(c, styles['TableHeader'] if r == 0 else styles['TableText']) for c in row] for r, row in enumerate(tbl_comp_data)],
        colWidths=[130, 190, 191]
    )
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_MED),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
    ]))
    story.append(t_comp)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: SECCIÓN 4 (CASO PRÁCTICO EMPRESARIAL RESUELTO)
    # =========================================================================
    s4_title = "4. Caso Práctico Resuelto: Scale-Up SaaS Enterprise (3 Squads, 30 PM Netos/Q)" if lang == 'ES' else "4. Enterprise Case Study: B2B SaaS Scale-Up (3 Squads, 30 Net PM/Q)"
    story.append(Paragraph(s4_title, styles['SecHeading']))

    s4_p1 = (
        "Para evidenciar el impacto operativo del modelo, analizamos el caso modelizado de <b>CloudScale Technologies</b>, "
        "plataforma SaaS B2B con 3 squads dedicados (Core, Growth y Enterprise), una capacidad bruta de 36 PM/trimestre "
        "y un backlog inicial de 20 iniciativas que totalizaban 83 PM, superando con creces la capacidad disponible."
        if lang == 'ES' else
        "To illustrate the executive power of the model, we examine the deployment at <b>CloudScale Technologies</b>, "
        "a high-growth B2B SaaS platform with 3 dedicated squads (Core, Growth, Enterprise), gross capacity of 36 PM/quarter, "
        "and an unmanaged 20-initiative backlog demanding 83 PM—far exceeding available delivery velocity."
    )
    story.append(Paragraph(s4_p1, styles['Body']))

    # Tabla Resumen Caso
    tbl_case_data_es = [
        ["ID", "Iniciativa", "Reach", "Imp", "Conf", "PM", "Score RICE", "Cuadrante", "Dictamen del Comité"],
        ["INIT-18", "2FA Obligatorio SMS/TOTP", "25.000", "2.0", "100%", "1.5", "33.333,3", "Quick Win", "Aprobado Q1 (Now)"],
        ["INIT-15", "NPS In-App Automatizado", "25.000", "1.0", "100%", "1.0", "25.000,0", "Quick Win", "Aprobado Q1 (Now)"],
        ["INIT-03", "Exportador Informes Excel/PDF", "22.000", "1.0", "100%", "1.0", "22.000,0", "Quick Win", "Aprobado Q1 (Now)"],
        ["INIT-05", "Onboarding Guiado Interactivo", "15.000", "2.0", "100%", "1.5", "20.000,0", "Quick Win", "Aprobado Q1 (Now)"],
        ["INIT-01", "SSO Okta SAML Enterprise", "8.500", "2.0", "100%", "2.0", "8.500,0", "Quick Win", "Aprobado Q1 (Now)"],
        ["INIT-02", "Copilot IA en Flujo de Trabajo", "18.000", "3.0", "80%", "6.0", "7.200,0", "Gran Apuesta", "Aprobado Q2 (Next)"],
        ["INIT-14", "Capa GraphQL Microservicios", "3.000", "1.0", "50%", "7.0", "214,3", "Pozo sin Fondo", "CONGELADO"],
        ["INIT-19", "Reescribe Integral DB a Rust", "5.000", "0.5", "50%", "14.0", "89,3", "Pozo sin Fondo", "CONGELADO"],
    ]
    tbl_case_data_en = [
        ["ID", "Initiative", "Reach", "Imp", "Conf", "PM", "RICE Score", "Quadrant", "Product Council Verdict"],
        ["INIT-18", "Mandatory Two-Factor 2FA", "25,000", "2.0", "100%", "1.5", "33,333.3", "Quick Win", "Committed Q1 (Now)"],
        ["INIT-15", "Automated In-App NPS Pulse", "25,000", "1.0", "100%", "1.0", "25,000.0", "Quick Win", "Committed Q1 (Now)"],
        ["INIT-03", "Instant Data Exporter Excel/PDF", "22,000", "1.0", "100%", "1.0", "22,000.0", "Quick Win", "Committed Q1 (Now)"],
        ["INIT-05", "Guided Self-Serve Onboarding", "15,000", "2.0", "100%", "1.5", "20,000.0", "Quick Win", "Committed Q1 (Now)"],
        ["INIT-01", "Enterprise Okta SAML SSO", "8,500", "2.0", "100%", "2.0", "8,500.0", "Quick Win", "Committed Q1 (Now)"],
        ["INIT-02", "In-Workflow Generative AI Copilot", "18,000", "3.0", "80%", "6.0", "7,200.0", "Big Bet", "Planned Q2 (Next)"],
        ["INIT-14", "GraphQL Microservices Layer", "3,000", "1.0", "50%", "7.0", "214.3", "Money Pit", "FROZEN"],
        ["INIT-19", "Total Database Rewrite to Rust", "5,000", "0.5", "50%", "14.0", "89.3", "Money Pit", "FROZEN"],
    ]
    tbl_case_data = tbl_case_data_es if lang == 'ES' else tbl_case_data_en

    t_case = Table(
        [[Paragraph(c, styles['TableHeader'] if r == 0 else styles['TableText']) for c in row] for r, row in enumerate(tbl_case_data)],
        colWidths=[42, 130, 42, 30, 32, 28, 55, 68, 84]
    )
    t_case.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('ALIGN', (2,1), (6,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
    ]))
    story.append(t_case)
    story.append(Spacer(1, 6))

    # Diagnóstico del Comité
    s4_dec_title = "4.1. Resoluciones Clave del Comité de Dirección" if lang == 'ES' else "4.1. Core Strategic Council Resolutions"
    story.append(Paragraph(s4_dec_title, styles['SubSecHeading']))

    case_resolutions_es = (
        "<b>1. Captura Inmediata de Quick Wins en Q1:</b> Los 5 Quick Wins identificados concentran el <b>54,2% del valor "
        "total</b> con solo 7,0 PM de esfuerzo (23,3% de la capacidad neta de Q1), generando tracción comercial inmediata.<br/>"
        "<b>2. Congelación Vinculante de Pozos sin Fondo:</b> La reescritura a Rust (INIT-19) y GraphQL (INIT-14) eran proyectos "
        "patrocinados por líderes técnicos que habrían absorbido 21 PM con nula justificación de negocio. Su congelación "
        "liberó capacidad equivalente a 1,5 squads durante un trimestre entero.<br/>"
        "<b>3. Blindaje del Buffer de Deuda Técnica (16,7%):</b> Se reservaron 6 PM trimestrales intocables para refactorización, "
        "evitando la degradación de la plataforma mientras se ejecutaba el Copilot de IA en Q2."
    )
    case_resolutions_en = (
        "<b>1. Immediate Q1 Quick Wins Capture:</b> The 5 priority Quick Wins capture <b>54.2% of total value</b> "
        "using just 7.0 person-months (23.3% of Q1 net capacity), creating rapid commercial momentum.<br/>"
        "<b>2. Binding Freeze on Engineering Money Pits:</b> The database rewrite to Rust (INIT-19) and GraphQL (INIT-14) "
        "were executive pet projects demanding 21 PM with minimal customer demand. Freezing them reclaimed the equivalent "
        "of 1.5 full squads for an entire quarter.<br/>"
        "<b>3. Technical Debt Buffer Ring-Fencing (16.7%):</b> Safeguarded 6 PM/quarter strictly for infrastructure resilience, "
        "preventing production incidents while greenlighting the AI Copilot for Q2 execution."
    )
    story.append(Paragraph(case_resolutions_es if lang == 'ES' else case_resolutions_en, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: SECCIÓN 5 (BOARD DEFENSE FAQ) & BIBLIOGRAFÍA
    # =========================================================================
    s5_title = "5. Board Defense Protocol & Referencias Bibliográficas Canónicas" if lang == 'ES' else "5. Board Defense Protocol & Canonical References"
    story.append(Paragraph(s5_title, styles['SecHeading']))

    faq_data_es = [
        ("1. ¿Por qué el proyecto patrocinado por el CEO no está en Q1?",
         "El modelo evalúa densidad de valor, no jerarquía política. Si una iniciativa exige alto esfuerzo con baja evidencia empírica, consumirá recursos críticos de Quick Wins probados. Puede recalibrarse en Q2 aportando tests A/B o pre-contratos."),
        ("2. ¿Cómo evitamos que los equipos inflen artificialmente la Confianza?",
         "Mediante la rúbrica del Confidence Meter: una puntuación del 100% exige obligatoriamente un test A/B con p < 0.05 o telemetría activa. Sin datos empíricos auditados, el modelo impone automáticamente un techo de Confianza del 50%."),
        ("3. ¿Dónde y cómo se gestiona la deuda técnica y el mantenimiento?",
         "No compitiendo en el ranking RICE, sino mediante un buffer fijo previo del 16,7% (6 PM/Q). La deuda técnica se gestiona como coste de operación estructural, garantizando fiabilidad sin canibalizar el roadmap de valor."),
        ("4. ¿RICE o WSJF (Weighted Shortest Job First / Cost of Delay)?",
         "RICE es superior para roadmaps de producto y crecimiento por su modelización explícita del Reach y el descuento de Confianza. WSJF es complementario en entornos SAFe/Lean donde el Coste del Retraso financiero está estrictamente cuantificado."),
        ("5. ¿Con qué cadencia temporal debe repriorizarse el backlog?",
         "Cada 90 días en la sesión ordinaria del Product Council. Las iniciativas del horizonte 'Now' (Q1) quedan bloqueadas para garantizar foco, mientras que 'Next' y 'Later' se repriorizan con los datos empíricos de los experimentos ICE."),
    ]
    faq_data_en = [
        ("1. Why isn't the CEO's requested feature included in Q1?",
         "The framework prioritizes value density over corporate hierarchy. Committing high-effort, low-confidence pet projects starves verified Quick Wins. The initiative can be reconsidered for Q2 if de-risked via prototypes or customer commitments."),
        ("2. How do we prevent teams from inflating the Confidence factor?",
         "Through the strict Confidence Meter rubric: a 100% score mandates statistically significant A/B test data or live telemetry. Without empirical validation, the model enforces an automatic 50% confidence cap."),
        ("3. Where and how is technical debt / maintenance handled?",
         "Not by forcing it into the RICE value competition, but via a ring-fenced 16.7% capacity buffer (6 PM/quarter). Debt is treated as a structural operational cost, preserving platform stability without diluting roadmap focus."),
        ("4. When to choose RICE over WSJF (Cost of Delay)?",
         "RICE is best-in-class for software products and scale-ups due to explicit user Reach modeling and Bayesian confidence haircuts. WSJF excels in mature Lean/SAFe manufacturing environments where financial Cost of Delay is precisely measured."),
        ("5. What is the optimal governance review cadence?",
         "Every 90 days at the formal C-Suite Product Council. The committed 'Now' (Q1) horizon is locked to protect engineering focus, while 'Next' and 'Later' items are re-scored using empirical insights from bi-weekly ICE tests."),
    ]
    faq_data = faq_data_es if lang == 'ES' else faq_data_en

    for q, a in faq_data:
        p_q = Paragraph(f"<b>Q: {q}</b>", styles['SubSecHeading'])
        story.append(p_q)
        p_a = Paragraph(f"<b>R:</b> {a}" if lang == 'ES' else f"<b>A:</b> {a}", styles['Body'])
        story.append(p_a)
        story.append(Spacer(1, 2))

    # Referencias Bibliográficas
    bib_title = "Referencias Bibliográficas de Autoridad" if lang == 'ES' else "Authoritative Bibliographical References"
    story.append(Paragraph(bib_title, styles['SubSecHeading']))

    bib_items_es = [
        "1. <b>McBride, Sean (2016).</b> <i>RICE: Simple prioritization for product managers</i>. Inside Intercom Blog. (Marco canónico RICE).",
        "2. <b>Ellis, Sean & Brown, Morgan (2017).</b> <i>Hacking Growth: How Today's Fastest-Growing Companies Drive Breakout Success</i>. Crown Business. (Marco ICE).",
        "3. <b>Gilad, Itamar (2023).</b> <i>Evidence-Guided: Creating High-Impact Products in the Face of Uncertainty</i>. (The Confidence Meter).",
        "4. <b>Cagan, Marty (2017).</b> <i>Inspired: How to Create Tech Products Customers Love</i>. Wiley (2ª Edición). (Superación de la fábrica de features).",
        "5. <b>Reinertsen, Donald G. (2009).</b> <i>The Principles of Product Development Flow</i>. Celeritas Publishing. (Coste del Retraso y WSJF).",
        "6. <b>Minto, Barbara (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall. (Estructura ejecutiva C-Level).",
    ]
    bib_items_en = [
        "1. <b>McBride, Sean (2016).</b> <i>RICE: Simple prioritization for product managers</i>. Inside Intercom Blog. (Foundational RICE framework).",
        "2. <b>Ellis, Sean & Brown, Morgan (2017).</b> <i>Hacking Growth: How Today's Fastest-Growing Companies Drive Breakout Success</i>. Crown Business. (ICE framework).",
        "3. <b>Gilad, Itamar (2023).</b> <i>Evidence-Guided: Creating High-Impact Products in the Face of Uncertainty</i>. (The Confidence Meter).",
        "4. <b>Cagan, Marty (2017).</b> <i>Inspired: How to Create Tech Products Customers Love</i>. Wiley (2nd Edition). (Overcoming the feature factory).",
        "5. <b>Reinertsen, Donald G. (2009).</b> <i>The Principles of Product Development Flow</i>. Celeritas Publishing. (Cost of Delay and economic flow).",
        "6. <b>Minto, Barbara (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall. (Minto Pyramid communication).",
    ]
    bib_items = bib_items_es if lang == 'ES' else bib_items_en

    for b in bib_items:
        story.append(Paragraph(b, styles['BibItem']))

    return story


def generate_methodology_guide(lang='ES', out_path=None):
    if out_path is None:
        if lang == 'ES':
            out_path = "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[ES]_Matriz_RICE_ICE/Guia_Metodologica_RICE_ICE_ES.pdf"
        else:
            out_path = "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[EN]_RICE_ICE_Matrix/Methodology_Guide_RICE_ICE_EN.pdf"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print(f"\nGenerando guía metodológica PDF ({lang}): {out_path}...")

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=46,
        bottomMargin=46
    )

    story = build_pdf_story(lang=lang)

    # Inyectar idioma en el canvas numerado
    def canvas_maker(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c._lang = lang
        return c

    doc.build(story, canvasmaker=canvas_maker)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"[OK] Guía PDF generada con éxito: {out_path} ({size_kb:.1f} KB)")
    return out_path


def main():
    print("================================================================================")
    print("DATALARIA | GENERADOR DE GUÍAS METODOLÓGICAS PDF RICE & ICE")
    print("================================================================================")
    es_path = generate_methodology_guide(lang='ES')
    en_path = generate_methodology_guide(lang='EN')
    print("\nGuías PDF generadas exitosamente en ambos idiomas.")


if __name__ == "__main__":
    main()
