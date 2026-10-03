#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para el Executive Decision Pack DAR:
1. packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa/[ES]_Matriz_DAR/Guia_Metodologica_DAR_ES.pdf (Versión en Español)
2. packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa/[EN]_Quantitative_DAR/Methodology_Guide_DAR_EN.pdf (Versión en Inglés)

Estándar editorial de alta dirección (McKinsey / BCG / CMMI):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (El Coste Oculto de la Intuición Directiva).
- Página 2: Sección 2 (Marco Teórico & Fundamentación Matemática: Filtro Veto Booleano, Scoring Normalizado y Sensibilidad).
- Página 3: Sección 3 (Protocolo de Calibración de Criterios & Pesos: Must-Haves vs. Wants, Comparación por Pares y Rúbricas).
- Página 4: Sección 4 (Caso Práctico Corporativo Resuelto: Selección de Plataforma ERP Cloud en Horizon Global Logistics).
- Página 5: Sección 5 (Board Defense Protocol: 5 Preguntas Clave del CFO y Comité de Auditoría) y Referencias Bibliográficas Canónicas.
- Paginación dinámica con NumberedCanvas ("Página X de Y" / "Page X of Y").
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

# Acentos y Estados
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
            header_right = ("MATRIZ DAR CUANTITATIVA: ANÁLISIS DE DECISIONES & CRITERIOS VETO"
                            if lang == 'ES' else
                            "QUANTITATIVE DAR MATRIX: DECISION ANALYSIS & VETO CRITERIA")
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
        footer_left = ("Datalaria.com • Documento Confidencial para Consejo de Administración"
                       if lang == 'ES' else
                       "Datalaria.com • Confidential Board of Directors Document")
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
        'SubHeading': ParagraphStyle(
            'SubHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=11,
            textColor=C_NAVY_MED, spaceBefore=4, spaceAfter=2,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.8, leading=10.8,
            textColor=C_NAVY_MED, spaceAfter=2.8
        ),
        'Bullet': ParagraphStyle(
            'Bullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.8, leading=10.6,
            textColor=C_NAVY_MED, leftIndent=11, firstLineIndent=-7, spaceAfter=1.8
        ),
        'MathBox': ParagraphStyle(
            'MathBox', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=11.5,
            textColor=C_NAVY_DARK, alignment=1
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.2, leading=9.0,
            textColor=C_WHITE, alignment=1
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.0, leading=9.0,
            textColor=C_NAVY_MED
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.0, leading=9.0,
            textColor=C_NAVY_DARK
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica-Oblique', fontSize=7.6, leading=10.2,
            textColor=C_NAVY_DARK
        ),
        'FAQ_Q': ParagraphStyle(
            'FAQ_Q', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.0, leading=10.5,
            textColor=C_NAVY_DARK, spaceBefore=3.0, spaceAfter=1.5,
            keepWithNext=True
        ),
        'FAQ_A': ParagraphStyle(
            'FAQ_A', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.5, leading=10.2,
            textColor=C_NAVY_MED, spaceAfter=3.5
        ),
        'BiblioTitle': ParagraphStyle(
            'BiblioTitle', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.0, leading=10.5,
            textColor=C_NAVY_DARK, spaceBefore=4.0, spaceAfter=1.0,
            keepWithNext=True
        ),
        'BiblioBody': ParagraphStyle(
            'BiblioBody', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.2, leading=9.4,
            textColor=C_SLATE_MUTED, spaceAfter=2.5
        )
    }
    return styles


def build_meta_card(styles, lang='ES'):
    data = [
        [
            Paragraph("<b>Autor:</b> Equipo de Estrategia Corporativa & Finanzas Datalaria" if lang == 'ES' else "<b>Author:</b> Datalaria Corporate Strategy & Finance Team", styles['TableCell']),
            Paragraph("<b>Estándar:</b> CMMI DAR (Process Area) & Kepner-Tregoe" if lang == 'ES' else "<b>Standard:</b> CMMI DAR (Process Area) & Kepner-Tregoe", styles['TableCell'])
        ],
        [
            Paragraph("<b>Destinatarios:</b> CEOs, CFOs, CIOs y Comités de Inversión" if lang == 'ES' else "<b>Audience:</b> CEOs, CFOs, CIOs & Board Investment Committees", styles['TableCell']),
            Paragraph("<b>Gobernanza:</b> ECMA-376 / Fórmulas Auditadas / ISO 27001" if lang == 'ES' else "<b>Governance:</b> ECMA-376 / Audited Formulas / ISO 27001", styles['TableCell'])
        ]
    ]
    t = Table(data, colWidths=[255, 255])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


def build_formula_box(math_text, desc_text, styles, width=510):
    content = [
        [Paragraph(math_text, styles['MathBox'])],
        [Paragraph(desc_text, styles['CalloutText'])]
    ]
    t = Table(content, colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BLUE_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BLUE_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


def build_pdf(lang='ES', out_path=None):
    if out_path is None:
        base_dir = "packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa"
        sub_dir = "[ES]_Matriz_DAR" if lang == 'ES' else "[EN]_Quantitative_DAR"
        fname = "Guia_Metodologica_DAR_ES.pdf" if lang == 'ES' else "Methodology_Guide_DAR_EN.pdf"
        out_path = os.path.join(base_dir, sub_dir, fname)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=42, rightMargin=42,
        topMargin=54, bottomMargin=50
    )

    styles = get_custom_styles()
    story = []

    # ==========================================================================
    # PÁGINA 1: PORTADA & SECCIÓN 1 (EL COSTE OCULTO DE LA INTUICIÓN DIRECTIVA)
    # ==========================================================================
    kicker = ("SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN | ESTÁNDAR CMMI DAR & KEPNER-TREGOE"
              if lang == 'ES' else
              "SUITE 02 · DECISION ANALYSIS & RESOLUTION | CMMI DAR & KEPNER-TREGOE STANDARD")
    title = ("MATRIZ DAR CUANTITATIVA: ANÁLISIS DE DECISIONES, FILTROS VETO Y SCORING MULTICRITERIO"
             if lang == 'ES' else
             "QUANTITATIVE DAR MATRIX: DECISION ANALYSIS & RESOLUTION, VETO CRITERIA & MULTI-CRITERIA SCORING")
    subtitle = ("Protocolo formal de evaluación cuantitativa para blindar adjudicaciones tecnológicas, contrataciones críticas, dilemas Make vs. Buy y decisiones estratégicas ante Consejos de Administración."
                if lang == 'ES' else
                "A formal quantitative evaluation protocol to safeguard technology procurement, critical hires, Make vs. Buy dilemmas, and strategic mandates before corporate Boards of Directors.")

    story.append(Paragraph(kicker, styles['CoverKicker']))
    story.append(Paragraph(title, styles['CoverTitle']))
    story.append(Paragraph(subtitle, styles['CoverSub']))
    story.append(build_meta_card(styles, lang=lang))
    story.append(Spacer(1, 8))

    # Sección 1
    sec1_title = ("1. El Coste Oculto de la Intuición Directiva en Decisiones de Alto Impacto"
                  if lang == 'ES' else
                  "1. The Hidden Cost of Executive Intuition in High-Stakes Decisions")
    story.append(Paragraph(sec1_title, styles['SecHeading']))

    sec1_body_es = [
        "En corporaciones medianas y grandes, las decisiones estratégicas de alta incertidumbre —tales como la selección de una plataforma ERP/Cloud corporativa, fusiones y adquisiciones (M&A), o la externalización de infraestructura crítica (*Make vs. Buy*)— conllevan compromisos de capital que superan con frecuencia decenas de millones de euros. Sin embargo, en más del 70% de las ocasiones, estas deliberaciones se resuelven mediante procesos informales dominados por la intuición ejecutiva, el carisma comercial de los proveedores y la política de pasillo.",
        "La psicología organizacional y la teoría de la decisión contemporánea han tipificado las cuatro patologías cognitivas que sabotean sistemáticamente las deliberaciones del Comité de Dirección:",
        "<b>1. Sesgo de Confirmación & Efecto Halo:</b> Un directivo senior con afinidad hacia un determinado proveedor interpreta selectivamente las especificaciones técnicas para ratificar su preferencia preconcebida, ignorando deficiencias estructurales flagrantes en seguridad o costes ocultos.",
        "<b>2. La Falacia del 'Coste Hundido' y el Anclaje:</b> Persistir en arquitecturas obsoletas o favorecer a suministradores incumbentes con el pretexto de rentabilizar inversiones históricas amortizadas, a expensas de la competitividad futura.",
        "<b>3. El Compromiso Diplomático Egalitario:</b> Asignar ponderaciones arbitrarias idénticas a todos los criterios para evitar fricciones interdepartamentales, equiparando exigencias críticas (ej. soberanía del dato o cumplimiento legal) con aspectos cosméticos.",
        "<b>4. La Ausencia de Filtros Veto (Must-Haves):</b> Evaluar ofertas en matrices sumatorias donde una calificación extraordinaria en funcionalidades accesorias compensa indebidamente el incumplimiento de requisitos obligatorios no negociables."
    ]

    sec1_body_en = [
        "In mid-to-large enterprises, strategic decisions characterized by high uncertainty—such as selecting an enterprise Cloud/ERP platform, executing M&A carve-outs, or navigating complex Make vs. Buy dilemmas—routinely commit millions in multi-year capital expenditure. Yet in over 70% of corporate settings, these decisions are resolved through informal deliberations dominated by executive gut-feeling, vendor sales charisma, and internal hallway politics.",
        "Organizational psychology and modern decision theory have formalized the four systemic cognitive pathologies that routinely sabotage C-Suite deliberations:",
        "<b>1. Confirmation Bias & Halo Effect:</b> Senior executives with pre-existing affinity toward a specific brand selectively emphasize technical features to validate their preconception, discounting structural cybersecurity risks or hidden licensing overhead.",
        "<b>2. Sunk-Cost Fallacy & Incumbent Anchoring:</b> Clinging to legacy systems or favoring incumbent suppliers to justify historical expenditures, directly jeopardizing enterprise agility and unit economics.",
        "<b>3. Egalitarian Diplomatic Compromise:</b> Assigning uniform weights to disparate criteria to avoid inter-departmental friction, improperly equating mandatory regulatory compliance with cosmetic UI preferences.",
        "<b>4. Absence of Binary Veto Filters (Must-Haves):</b> Utilizing compensatory linear scoring matrices where high marks in secondary features mask the violation of non-negotiable legal or architectural requirements."
    ]

    sec1_body = sec1_body_es if lang == 'ES' else sec1_body_en
    for p in sec1_body:
        story.append(Paragraph(p, styles['Body']))

    story.append(Spacer(1, 4))
    callout_p1_es = "<b>Regla de Oro CMMI DAR:</b> Una decisión estratégica no es auditable por la brillantez retórica de su defensa, sino por la trazabilidad matemática de sus exclusiones y la objetividad reproducible de su scoring ponderado."
    callout_p1_en = "<b>CMMI DAR Golden Rule:</b> A strategic decision is not auditable by the eloquence of its executive defense, but by the mathematical traceability of its exclusions and the reproducible objectivity of its weighted scoring."
    story.append(build_formula_box(
        "CMMI DAR Standard: Traceability = Governance",
        callout_p1_es if lang == 'ES' else callout_p1_en,
        styles
    ))

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 2: MARCO TEÓRICO & FUNDAMENTACIÓN MATEMÁTICA
    # ==========================================================================
    sec2_title = ("2. Marco Teórico & Fundamentación Matemática del Modelo DAR"
                  if lang == 'ES' else
                  "2. Theoretical Framework & Mathematical Foundation of the DAR Model")
    story.append(Paragraph(sec2_title, styles['SecHeading']))

    sec2_sub1 = ("2.1. El Filtro Veto Booleano (Non-Negotiable Gatekeeper)"
                 if lang == 'ES' else
                 "2.1. The Boolean Veto Filter (Non-Negotiable Gatekeeper)")
    story.append(Paragraph(sec2_sub1, styles['SubHeading']))

    p_v_es = (r"El estándar CMMI DAR y la metodología Kepner-Tregoe imponen una separación matemática tajante entre criterios no negociables (*Must-Haves*) "
              r"y criterios deseables ponderados (*Wants*). Sea una alternativa $k \in \{1, \dots, K\}$ y un conjunto de $m$ filtros veto binarios. "
              r"Cada filtro se evalúa como una variable de Bernoulli $v_{ki} \in \{0, 1\}$, donde $v_{ki} = 1$ denota cumplimiento estricto y $v_{ki} = 0$ incumplimiento:")
    p_v_en = (r"The CMMI DAR standard and the Kepner-Tregoe methodology enforce an absolute mathematical partition between non-negotiable criteria (*Must-Haves*) "
              r"and weighted desirable attributes (*Wants*). For any alternative $k \in \{1, \dots, K\}$ evaluated across $m$ binary veto criteria, "
              r"each condition is modeled as a Bernoulli variable $v_{ki} \in \{0, 1\}$, where $v_{ki} = 1$ denotes compliance and $v_{ki} = 0$ denotes failure:")
    story.append(Paragraph(p_v_es if lang == 'ES' else p_v_en, styles['Body']))

    story.append(build_formula_box(
        "Factor Booleano Veto:   V_k = \\prod_{i=1}^m v_{ki} \\in \\{0, 1\\}",
        "Si existe al menos un criterio i tal que v_{ki} = 0, entonces V_k = 0 (Descalificación Fulminante e Implacable)."
        if lang == 'ES' else
        "If there exists at least one criterion i where v_{ki} = 0, then V_k = 0 (Immediate & Irreversible Disqualification).",
        styles
    ))
    story.append(Spacer(1, 4))

    sec2_sub2 = ("2.2. Algoritmo de Scoring Ponderado Normalizado"
                 if lang == 'ES' else
                 "2.2. Normalized Multi-Criteria Weighted Scoring Algorithm")
    story.append(Paragraph(sec2_sub2, styles['SubHeading']))

    p_sc_es = ("Para las alternativas que superan los filtros veto ($V_k = 1$), la puntuación estratégica global $S_k$ se calcula mediante "
               "la combinación lineal de $n$ criterios ponderados agrupados en pilares homogéneos, normalizada en una escala continua de 0 a 100 puntos:")
    p_sc_en = ("For alternatives that pass all veto hurdles ($V_k = 1$), the composite strategic score $S_k$ is calculated via "
               "a linear combination of $n$ weighted criteria grouped into distinct pillars, normalized on a continuous scale of 0 to 100 points:")
    story.append(Paragraph(p_sc_es if lang == 'ES' else p_sc_en, styles['Body']))

    story.append(build_formula_box(
        "Puntuación Final Efectiva:   S_k = V_k \\cdot \\left[ 10 \\cdot \\sum_{j=1}^n w_j \\cdot s_{kj} \\right] \\quad \\text{con} \\quad \\sum_{j=1}^n w_j = 1.00",
        "Donde w_j es la ponderación porcentual del criterio j, y s_{kj} \\in [1.0, 10.0] es la calificación objetiva auditada."
        if lang == 'ES' else
        "Where w_j is the percentage weight of criterion j, and s_{kj} \\in [1.0, 10.0] is the audited objective rating.",
        styles
    ))
    story.append(Spacer(1, 4))

    sec2_sub3 = ("2.3. Sensibilidad Marginal y Robustez de la Decisión"
                 if lang == 'ES' else
                 "2.3. Marginal Sensitivity & Decision Robustness")
    story.append(Paragraph(sec2_sub3, styles['SubHeading']))

    p_sens_es = ("Para blindar el veredicto ante impugnaciones del Comité de Auditoría, se calcula la sensibilidad marginal respecto al peso del criterio $j$: "
                 "$\\frac{\\partial S_k}{\\partial w_j} = 10 \\cdot V_k \\cdot s_{kj}$. Una decisión se declara <b>estructuralmente robusta</b> cuando el ranking de la alternativa "
                 "ganadora se preserva inalterado ante variaciones de $\\pm 20\\%$ en las ponderaciones de cualquiera de los cuatro pilares clave.")
    p_sens_en = ("To defend the selection against Audit Committee scrutiny, the marginal sensitivity with respect to weight $w_j$ is evaluated: "
                 "$\\frac{\\partial S_k}{\\partial w_j} = 10 \\cdot V_k \\cdot s_{kj}$. A decision is deemed <b>structurally robust</b> when the winning alternative's rank "
                 "remains strictly invariant under a $\\pm 20\\%$ weight swing across any of the core strategic pillars.")
    story.append(Paragraph(p_sens_es if lang == 'ES' else p_sens_en, styles['Body']))

    # Cuadro comparativo: Métodos Tradicionales vs Matriz DAR
    story.append(Spacer(1, 3))
    comp_headers = [
        ("Dimensión de Gobierno", "Governance Dimension"),
        ("Toma de Decisiones Convencional", "Conventional Decision-Making"),
        ("Matriz DAR Cuantitativa Datalaria", "Datalaria Quantitative DAR Matrix")
    ]
    comp_data_es = [
        ["Tratamiento de Requisitos", "Compensatorio: defectos graves se tapan con extras", "Booleano Estricto: 1 fallo descalifica automáticamente"],
        ["Asignación de Ponderaciones", "Arbitraria o reactiva a la oferta favorita", "Comparación por pares pre-establecida y congelada"],
        ["Escala de Calificación", "Subjetiva (1 a 5 con definiciones difusas)", "Rúbrica objetiva (1 a 10 anclada a evidencias auditables)"],
        ["TCO y Costes Ocultos", "Foco miope en precio inicial de compra", "TCO consolidado a 3 años (licencias, setup, OPEX y SLA)"],
        ["Auditoría y Trazabilidad", "Actas de reunión cualitativas sin justificación", "Registro formal de evidencias, matriz what-if y firmas C-Level"]
    ]
    comp_data_en = [
        ["Requirement Handling", "Compensatory: severe defects offset by perks", "Strict Boolean: 1 single breach triggers immediate disqualification"],
        ["Weight Assignment", "Arbitrary or reverse-engineered for preferred vendor", "Pairwise comparison frozen prior to evaluating commercial bids"],
        ["Scoring Scale", "Subjective (1 to 5 with ambiguous labels)", "Objective rubric (1 to 10 anchored to audited documentation)"],
        ["TCO & Hidden Costs", "Myopic focus on upfront sticker price", "3-Year consolidated TCO (licensing, setup, OPEX and SLA credits)"],
        ["Audit & Traceability", "Informal meeting minutes without quantitative trail", "Formal evidence trail, sensitivity matrix, and C-Suite sign-offs"]
    ]
    comp_rows = comp_data_es if lang == 'ES' else comp_data_en
    tbl_comp_data = [[
        Paragraph(comp_headers[0][0] if lang == 'ES' else comp_headers[0][1], styles['TableHeader']),
        Paragraph(comp_headers[1][0] if lang == 'ES' else comp_headers[1][1], styles['TableHeader']),
        Paragraph(comp_headers[2][0] if lang == 'ES' else comp_headers[2][1], styles['TableHeader']),
    ]]
    for r in comp_rows:
        tbl_comp_data.append([
            Paragraph(r[0], styles['TableCellBold']),
            Paragraph(r[1], styles['TableCell']),
            Paragraph(r[2], styles['TableCellBold']),
        ])
    t_comp = Table(tbl_comp_data, colWidths=[110, 200, 200])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (2,1), (2,-1), C_GREEN_LIGHT),
    ]))
    story.append(t_comp)

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 3: PROTOCOLO DE CALIBRACIÓN DE CRITERIOS & PESOS
    # ==========================================================================
    sec3_title = ("3. Protocolo de Calibración de Criterios & Ponderaciones sin Manipulación Política"
                  if lang == 'ES' else
                  "3. Criteria & Weight Calibration Protocol Free from Political Bias")
    story.append(Paragraph(sec3_title, styles['SecHeading']))

    sec3_sub1 = ("3.1. Diferenciación Taxonómica: Must-Haves (Veto) vs. Wants (Deseables)"
                 if lang == 'ES' else
                 "3.1. Taxonomic Distinction: Must-Haves (Veto) vs. Wants (Desirables)")
    story.append(Paragraph(sec3_sub1, styles['SubHeading']))

    p_tax_es = ("El error directivo más destructivo consiste en convertir deseos deseables en criterios veto (provocando descalificación de todos los postores) "
                "o, inversamente, degradar requisitos obligatorios a criterios ponderados. Un criterio sólo califica como <b>Filtro Veto (Must-Have)</b> si cumple "
                "tres condiciones sine qua non: (1) Es medible de forma binaria (CUMPLE / NO CUMPLE sin grises), (2) Su incumplimiento expone a la empresa a riesgo legal "
                "inaceptable o quiebra operativa, y (3) Es no negociable bajo ninguna circunstancia económica.")
    p_tax_en = ("The most damaging executive mistake is classifying aspirational preferences as veto filters (paralyzing the process by disqualifying every candidate) "
                "or, conversely, treating non-negotiable mandates as tradable weighted scores. A criterion strictly qualifies as a <b>Veto Gatekeeper (Must-Have)</b> "
                "only if it satisfies three tests: (1) Binary measurability (PASS / FAIL with zero ambiguity), (2) Non-compliance creates unacceptable legal exposure "
                "or operational failure, and (3) It is strictly non-negotiable regardless of price concessions.")
    story.append(Paragraph(p_tax_es if lang == 'ES' else p_tax_en, styles['Body']))

    sec3_sub2 = ("3.2. Calibración de Ponderaciones mediante Comparación por Pares (AHP)"
                 if lang == 'ES' else
                 "3.2. Weight Calibration via Pairwise Comparison (AHP)")
    story.append(Paragraph(sec3_sub2, styles['SubHeading']))

    p_ahp_es = ("Para evitar que los pesos se ajusten 'a medida' tras conocer las ofertas, las ponderaciones deben congelarse antes de recibir las propuestas técnicas. "
                "El comité evaluador pondera los 4 pilares estratégicos mediante matrices de jerarquía analítica (AHP / Kepner-Tregoe):")
    p_ahp_en = ("To prevent stakeholders from reverse-engineering weights once commercial proposals are unsealed, weight distribution must be formally frozen "
                "prior to receiving bids. The committee calibrates the 4 strategic pillars through Analytic Hierarchy Process (AHP / Kepner-Tregoe) matrices:")
    story.append(Paragraph(p_ahp_es if lang == 'ES' else p_ahp_en, styles['Body']))

    pillars_detail_es = [
        "<b>• Pilar 1: Ajuste Técnico & Funcional (30.0%):</b> Cobertura de procesos core sin desarrollo a medida (10%), ergonomía y UX (8%), APIs y webhooks (7%), rendimiento (5%).",
        "<b>• Pilar 2: Coste Total de Propiedad - TCO 3 Años (25.0%):</b> Inversión inicial en setup y licencias (10%), consultoría de implantación (9%), costes recurrentes y upgrades (6%).",
        "<b>• Pilar 3: SLA, Soporte & Solvencia Proveedor (20.0%):</b> SLA de resolución crítica < 2h con penalizaciones (8%), solvencia crediticia y presencia local (7%), academia y docs (5%).",
        "<b>• Pilar 4: Escalabilidad, Seguridad & Roadmap (25.0%):</b> Seguridad Zero-Trust y cifrado AES-256 (10%), elasticidad cloud (8%), visión e IA generativa (7%)."
    ]
    pillars_detail_en = [
        "<b>• Pillar 1: Technical & Functional Fit (30.0%):</b> Out-of-the-box core workflow coverage (10%), UX ergonomics (8%), REST APIs & webhooks (7%), throughput latency (5%).",
        "<b>• Pillar 2: Total Cost of Ownership - 3Y TCO (25.0%):</b> Initial licensing & setup (10%), systems integration & consulting (9%), recurring maintenance & upgrades (6%).",
        "<b>• Pillar 3: SLA, Support & Vendor Solvency (20.0%):</b> Critical incident SLA < 2h with fee credits (8%), credit rating & local support (7%), documentation & training (5%).",
        "<b>• Pillar 4: Scalability, Security & Roadmap (25.0%):</b> Zero-Trust architecture & AES-256 encryption (10%), cloud auto-scaling (8%), R&D delivery roadmap & AI (7%)."
    ]
    for b in (pillars_detail_es if lang == 'ES' else pillars_detail_en):
        story.append(Paragraph(b, styles['Bullet']))

    story.append(Spacer(1, 3))
    sec3_sub3 = ("3.3. Rúbrica de Puntuación Objetiva (1 a 10) y Evidencias Exigidas"
                 if lang == 'ES' else
                 "3.3. Objective Scoring Rubric (1 to 10) & Audited Evidence Standards")
    story.append(Paragraph(sec3_sub3, styles['SubHeading']))

    # Tabla de Rúbricas
    rub_headers = [
        ("Banda de Calificación", "Score Band"),
        ("Definición Cualitativa Rigurosa", "Rigorous Qualitative Definition"),
        ("Estándar Probatorio Documental Requerido", "Required Evidentiary Documentation")
    ]
    rub_data_es = [
        ["9.0 - 10.0 (Excelente)", "Supera el estado del arte. Cobertura nativa > 90% con referencias demostrables.", "Demo técnica grabada en sandbox, informe SOC 2 auditado y clientes cotizados."],
        ["7.0 - 8.9 (Apto Sólido)", "Cumple plenamente los requerimientos con desviaciones menores absorbibles.", "Documentación técnica oficial, manuales de API y compromisos de SLA contractual."],
        ["5.0 - 6.9 (Aceptable)", "Cumple los requerimientos pero exige desarrollos ad-hoc o consultoría adicional.", "Oferta de servicios profesionales y hoja de ruta de desarrollo en plazo."],
        ["3.0 - 4.9 (Deficiente)", "Brechas funcionales sustanciales; rendimiento inferior a la media de la industria.", "Resultados de pruebas de carga insuficientes o SLA sin penalizaciones económicas."],
        ["1.0 - 2.9 (Inadmisible)", "Incapacidad técnica probada o negativa del proveedor a garantizar el servicio.", "Falta de respuesta formal a la RFP o rechazo explícito a cláusulas estándar."]
    ]
    rub_data_en = [
        ["9.0 - 10.0 (World-Class)", "Exceeds market benchmark. Native coverage > 90% with verifiable enterprise scale.", "Recorded technical sandbox demo, third-party SOC 2 audit, Fortune 500 references."],
        ["7.0 - 8.9 (Solid Fit)", "Fully satisfies specifications with minor, easily manageable workarounds.", "Official developer documentation, verified API specs, and contractual SLA terms."],
        ["5.0 - 6.9 (Acceptable)", "Meets baseline criteria but requires custom bespoke development or extra fees.", "Statement of Work with explicit development hours and firm completion milestones."],
        ["3.0 - 4.9 (Deficient)", "Substantial feature gaps; throughput or security posture below industry average.", "Sub-par load test results, or reluctance to agree to binding penalty terms."],
        ["1.0 - 2.9 (Unacceptable)", "Demonstrated technical incompetence or vendor refusal to commit to warranties.", "RFP non-responsiveness or outright rejection of mandatory corporate clauses."]
    ]
    rub_rows = rub_data_es if lang == 'ES' else rub_data_en
    tbl_rub_data = [[
        Paragraph(rub_headers[0][0] if lang == 'ES' else rub_headers[0][1], styles['TableHeader']),
        Paragraph(rub_headers[1][0] if lang == 'ES' else rub_headers[1][1], styles['TableHeader']),
        Paragraph(rub_headers[2][0] if lang == 'ES' else rub_headers[2][1], styles['TableHeader']),
    ]]
    for r in rub_rows:
        tbl_rub_data.append([
            Paragraph(r[0], styles['TableCellBold']),
            Paragraph(r[1], styles['TableCell']),
            Paragraph(r[2], styles['TableCell']),
        ])
    t_rub = Table(tbl_rub_data, colWidths=[95, 205, 210])
    t_rub.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,1), (-1,1), C_GREEN_LIGHT),
        ('BACKGROUND', (0,5), (-1,5), C_RED_LIGHT),
    ]))
    story.append(t_rub)

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 4: CASO PRÁCTICO CORPORATIVO RESUELTO
    # ==========================================================================
    sec4_title = ("4. Caso Práctico Empresarial Resuelto: Horizon Global Logistics"
                  if lang == 'ES' else
                  "4. End-to-End Enterprise Case Study: Horizon Global Logistics")
    story.append(Paragraph(sec4_title, styles['SecHeading']))

    p_cs_es = ("<b>Contexto Operativo:</b> Horizon Global Logistics, operador logístico multinacional con 1.400 empleados, 12 delegaciones en Europa y "
               "una facturación anual de 185 M€, convocó un proceso de licitación estratégica para renovar su plataforma ERP Core en la nube. "
               "El Comité de Inversión estableció un techo de CAPEX de 450.000 € y un requerimiento estricto de despliegue en menos de 6 meses "
               "para evitar disrupciones en el pico estacional de Q4. Se evaluaron cinco proveedores internacionales líderes:")
    p_cs_en = ("<b>Operational Context:</b> Horizon Global Logistics, a pan-European supply chain operator with 1,400 employees, 12 regional hubs, "
               "and €185M in annual turnover, initiated a strategic RFP to replace its legacy on-premise ERP with a modern Cloud ERP platform. "
               "The Investment Committee enforced a strict CAPEX ceiling of €450,000 and a 6-month go-live deadline to avoid peak seasonal disruption. "
               "Five enterprise vendors were evaluated under the Datalaria DAR protocol:")
    story.append(Paragraph(p_cs_es if lang == 'ES' else p_cs_en, styles['Body']))

    # Tabla Resumen del Caso de Estudio
    cs_headers = [
        ("Proveedor / Alternativa", "Vendor / Alternative"),
        ("Veto (Must)", "Veto Gate"),
        ("Técnico (30%)", "Tech (30%)"),
        ("TCO 3A (25%)", "3Y TCO (25%)"),
        ("SLA (20%)", "SLA (20%)"),
        ("Seguridad (25%)", "Security (25%)"),
        ("Score Base", "Base Score"),
        ("Final (Vk)", "Final (Vk)"),
        ("Dictamen Directivo", "Executive Verdict")
    ]
    cs_data_es = [
        ["Vendor Alpha (Global Core)", "APTA", "23.6", "19.3", "16.9", "18.8", "78.6", "78.6", "Segunda Opción (Backup)"],
        ["Vendor Beta (Cloud Enterprise)", "APTA", "27.6", "20.0", "18.4", "20.4", "86.4", "86.4", "ADJUDICATARIA (Ganador)"],
        ["Vendor Gamma (Suite Modular)", "APTA", "22.7", "21.4", "15.0", "17.5", "76.6", "76.6", "Descartada (Bajo SLA)"],
        ["Vendor Delta (Legacy Hosted)", "DESCALIFICADA", "24.8", "16.3", "16.3", "18.9", "76.3", "0.0", "DESCALIFICADA (V-05)"],
        ["Vendor Epsilon (SaaS Niche)", "APTA", "21.1", "20.1", "13.0", "17.6", "71.8", "71.8", "Descartada (Sub-escala)"]
    ]
    cs_data_en = [
        ["Vendor Alpha (Global Core)", "PASS", "23.6", "19.3", "16.9", "18.8", "78.6", "78.6", "Designated Runner-Up"],
        ["Vendor Beta (Cloud Enterprise)", "PASS", "27.6", "20.0", "18.4", "20.4", "86.4", "86.4", "CONTRACT AWARD (Winner)"],
        ["Vendor Gamma (Suite Modular)", "PASS", "22.7", "21.4", "15.0", "17.5", "76.6", "76.6", "Rejected (Weak SLA)"],
        ["Vendor Delta (Legacy Hosted)", "DISQUALIFIED", "24.8", "16.3", "16.3", "18.9", "76.3", "0.0", "DISQUALIFIED (V-05)"],
        ["Vendor Epsilon (SaaS Niche)", "PASS", "21.1", "20.1", "13.0", "17.6", "71.8", "71.8", "Rejected (Sub-scale)"]
    ]
    cs_rows = cs_data_es if lang == 'ES' else cs_data_en
    tbl_cs_data = [[
        Paragraph(cs_headers[0][0] if lang == 'ES' else cs_headers[0][1], styles['TableHeader']),
        Paragraph(cs_headers[1][0] if lang == 'ES' else cs_headers[1][1], styles['TableHeader']),
        Paragraph(cs_headers[2][0] if lang == 'ES' else cs_headers[2][1], styles['TableHeader']),
        Paragraph(cs_headers[3][0] if lang == 'ES' else cs_headers[3][1], styles['TableHeader']),
        Paragraph(cs_headers[4][0] if lang == 'ES' else cs_headers[4][1], styles['TableHeader']),
        Paragraph(cs_headers[5][0] if lang == 'ES' else cs_headers[5][1], styles['TableHeader']),
        Paragraph(cs_headers[6][0] if lang == 'ES' else cs_headers[6][1], styles['TableHeader']),
        Paragraph(cs_headers[7][0] if lang == 'ES' else cs_headers[7][1], styles['TableHeader']),
        Paragraph(cs_headers[8][0] if lang == 'ES' else cs_headers[8][1], styles['TableHeader']),
    ]]
    for r in cs_rows:
        tbl_cs_data.append([
            Paragraph(r[0], styles['TableCellBold']),
            Paragraph(r[1], styles['TableCellBold']),
            Paragraph(r[2], styles['TableCell']),
            Paragraph(r[3], styles['TableCell']),
            Paragraph(r[4], styles['TableCell']),
            Paragraph(r[5], styles['TableCell']),
            Paragraph(r[6], styles['TableCell']),
            Paragraph(r[7], styles['TableCellBold']),
            Paragraph(r[8], styles['TableCellBold']),
        ])
    t_cs = Table(tbl_cs_data, colWidths=[105, 55, 42, 42, 38, 45, 42, 42, 99])
    t_cs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (1,1), (-2,-1), 'CENTER'),
        ('BACKGROUND', (0,2), (-1,2), C_GREEN_LIGHT), # Vendor Beta
        ('BACKGROUND', (0,4), (-1,4), C_RED_LIGHT),   # Vendor Delta
    ]))
    story.append(t_cs)
    story.append(Spacer(1, 6))

    sec4_findings_es = [
        "<b>1. Descalificación Inapelable de Vendor Delta (Criterio V-05):</b> A pesar de contar con un score técnico base de 76.3 y ofrecer un precio agresivo, su solución procesaba telemetría y réplicas analíticas en servidores ubicados en EE.UU., violando la directiva de compliance de datos en la UE. El multiplicador $V_{\\text{Delta}} = 0$ anuló de inmediato su puntuación efectiva a 0.0.",
        "<b>2. Victoria Estructural de Vendor Beta (86.4 pts vs. 78.6 pts):</b> Vendor Beta superó a Vendor Alpha por un diferencial de +7.8 puntos (+9.9% relativo). Su cobertura funcional nativa (94%) ahorra más de 140 jornadas de desarrollo a medida, reduciendo el riesgo de retrasos en el go-live.",
        "<b>3. Impacto Financiero en TCO a 3 Años:</b> Aunque el coste de suscripción inicial de Beta fue 15.000 € superior al de Gamma, sus costes de mantenimiento y consultoría generaron un ahorro acumulado de 380.000 € frente a Alpha y una reducción del 19% frente al TCO medio de la industria.",
        "<b>4. Blindaje de la Decisión ante el Comité de Auditoría:</b> La matriz de sensibilidad demostró que incluso duplicando la ponderación de precio (Escenario CFO: 50% TCO), Vendor Beta mantenía el liderazgo gracias a sus bajos costes operativos recurrentes."
    ]
    sec4_findings_en = [
        "<b>1. Unconditional Elimination of Vendor Delta (V-05 Veto Gate):</b> Despite commanding a 76.3 base score and aggressive upfront discount, the vendor processed analytics telemetry through US servers, violating EU GDPR mandates. Multiplier $V_{\\text{Delta}} = 0$ wiped out its effective score to 0.0.",
        "<b>2. Structural Supremacy of Vendor Beta (86.4 vs. 78.6 pts):</b> Vendor Beta achieved an undisputed victory with a +7.8 point decision gap (+9.9% relative margin) over Vendor Alpha. Native process coverage (94%) eliminated 140 days of bespoke coding risk.",
        "<b>3. Financial Impact across 3-Year TCO:</b> Although initial Year 1 licensing was €15k higher than Gamma, automated zero-code upgrades and lower support tickets delivered €380,000 in net multi-year savings compared to Alpha, beating industry average TCO by 19%.",
        "<b>4. Audit Committee Proofing:</b> The 'What-If' sensitivity analysis confirmed that even under an extreme CFO scenario (50% Cost weight), Vendor Beta remained the winning choice due to predictable recurring subscriptions."
    ]
    for b in (sec4_findings_es if lang == 'ES' else sec4_findings_en):
        story.append(Paragraph(b, styles['Bullet']))

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 5: BOARD DEFENSE PROTOCOL & REFERENCIAS CANÓNICAS
    # ==========================================================================
    sec5_title = ("5. Protocolo de Defensa ante el Consejo (Boardroom Defense FAQ)"
                  if lang == 'ES' else
                  "5. Boardroom Defense Protocol (C-Suite & Audit FAQ)")
    story.append(Paragraph(sec5_title, styles['SecHeading']))

    faq_es = [
        ("¿Por qué no adjudicamos la licitación al proveedor más barato en coste inicial (Vendor Gamma)?",
         "Porque confunde precio de compra con Coste Total de Propiedad (TCO). Gamma exigía 180.000 € en consultoría adicional para adaptar sus módulos y su SLA carecía de penalizaciones por caídas de servicio. A 36 meses, Vendor Beta es 210.000 € más económico en términos de flujo de caja neto."),
        ("¿Cómo demostramos que las ponderaciones no se manipularon a posteriori para favorecer a Beta?",
         "Mediante el protocolo de 'Congelación Previa' auditado por la PMO: la matriz de pesos se firmó y registró en la plataforma de compras antes de abrir los sobres técnicos de las ofertas, impidiendo cualquier ajuste retroactivo."),
        ("¿Qué grado de estabilidad ofrece la decisión si cambian las condiciones de mercado en 12 meses?",
         "El análisis de sensibilidad 'What-If' sometió el modelo a 5 escenarios de estrés (+/- 20% en costes y tecnología). En el 100% de los casos simulados, Vendor Beta mantuvo la primera posición debido a su ventaja estructural en cobertura nativa."),
        ("¿Por qué descalificar fulminantemente a Vendor Delta si es un suministrador líder del mercado?",
         "El cumplimiento normativo no es negociable. Aceptar data centers fuera de la UE exponía a la corporación a sanciones del RGPD de hasta el 4% de la facturación global. Un beneficio económico puntual jamás justifica un riesgo regulatorio catastrófico."),
        ("¿Cómo garantizamos el cumplimiento de plazos tras la firma del contrato?",
         "El pliego contractual vincula el 30% de los honorarios de implantación a la superación de las pruebas de aceptación de usuario (UAT) y fija penalizaciones automáticas del 1% semanal ante retrasos injustificados en el hito de Go-Live.")
    ]

    faq_en = [
        ("Why didn't we award the contract to the cheapest upfront bidder (Vendor Gamma)?",
         "Because sticker price must never be confused with Total Cost of Ownership (TCO). Gamma required €180,000 in custom development to support core workflows, and offered no uptime penalties. Over 36 months, Vendor Beta is €210,000 cheaper in net cash outflow."),
        ("How do we prove to internal auditors that weights were not reverse-engineered for Beta?",
         "Through the 'Pre-Freeze Governance Gate': the weight distribution matrix was formally signed off and timestamped in the procurement portal before technical bids were unsealed, rendering ex-post manipulation impossible."),
        ("How resilient is the selection if vendor pricing or market conditions shift within 12 months?",
         "The 'What-If' sensitivity analysis tested 5 extreme stress scenarios (+/- 20% cost and tech swings). Vendor Beta retained the top rank in 100% of simulations due to its structural superiority in native feature depth."),
        ("Why permanently disqualify a reputable incumbent like Vendor Delta over one technical point?",
         "Regulatory compliance is strictly non-negotiable. Storing analytics data in US regions exposed the firm to GDPR fines of up to 4% of global turnover. Tactical cost savings never justify catastrophic existential regulatory liability."),
        ("How do we enforce milestone compliance during implementation roll-out?",
         "The Master Services Agreement binds 30% of professional fees to successful UAT sign-off and enforces a contractual 1% weekly penalty on software subscription for unexcused go-live delays.")
    ]

    faqs = faq_es if lang == 'ES' else faq_en
    for q, a in faqs:
        story.append(Paragraph(f"<b>P: {q}</b>" if lang == 'ES' else f"<b>Q: {q}</b>", styles['FAQ_Q']))
        story.append(Paragraph(f"<b>R:</b> {a}" if lang == 'ES' else f"<b>A:</b> {a}", styles['FAQ_A']))

    story.append(Spacer(1, 4))
    sec6_title = ("6. Referencias Bibliográficas Canónicas de Autoridad"
                  if lang == 'ES' else
                  "6. Authoritative Canonical Bibliography")
    story.append(Paragraph(sec6_title, styles['SecHeading']))

    biblio_es = [
        ("CMMI Institute (2018).", "CMMI for Development (CMMI-DEV, V2.0): Decision Analysis and Resolution (DAR) Process Area.", "Estándar formal de evaluación de alternativas, criterios veto y trazabilidad de decisiones en ingeniería de sistemas complejos y adquisición corporativa."),
        ("Kepner, Charles H. & Tregoe, Benjamin B. (1965).", "The Rational Manager: A Systematic Approach to Decision Making and Problem Solving.", "McGraw-Hill, New York. Obra fundacional del método KT para separación de objetivos Must vs. Want y análisis cuantitativo de riesgos."),
        ("Keeney, Ralph L. & Raiffa, Howard (1976).", "Decisions with Multiple Objectives: Preferences and Value Trade-Offs.", "John Wiley & Sons, New York. Tratado seminal sobre teoría de utilidad multiatributo (MAUT) y estructuración de trade-offs corporativos."),
        ("Raiffa, Howard (1968).", "Decision Analysis: Introductory Lectures on Choices Under Uncertainty.", "Addison-Wesley. Formalización de árboles de decisión, análisis de sensibilidad y neutralización de aversión al riesgo en alta dirección."),
        ("Minto, Barbara (2009).", "The Pyramid Principle: Logic in Writing and Thinking.", "Financial Times / Prentice Hall (3ª Edición). Estándar de oro de estructuración deductiva y Action Titles para comunicación ejecutiva ante Consejos.")
    ]

    biblio_en = [
        ("CMMI Institute (2018).", "CMMI for Development (CMMI-DEV, V2.0): Decision Analysis and Resolution (DAR) Process Area.", "Canonical standard for formal structured alternatives appraisal, mandatory veto gates, and decision traceability in enterprise procurement."),
        ("Kepner, Charles H. & Tregoe, Benjamin B. (1965).", "The Rational Manager: A Systematic Approach to Decision Making and Problem Solving.", "McGraw-Hill, New York. Foundational treatise introducing the Must vs. Want framework and quantitative decision matrices."),
        ("Keeney, Ralph L. & Raiffa, Howard (1976).", "Decisions with Multiple Objectives: Preferences and Value Trade-Offs.", "John Wiley & Sons, New York. Seminal reference on Multi-Attribute Utility Theory (MAUT) and mathematical value trade-off modeling."),
        ("Raiffa, Howard (1968).", "Decision Analysis: Introductory Lectures on Choices Under Uncertainty.", "Addison-Wesley. Rigorous mathematical foundation for decision trees, marginal sensitivity indices, and corporate risk governance."),
        ("Minto, Barbara (2009).", "The Pyramid Principle: Logic in Writing and Thinking.", "Financial Times / Prentice Hall (3rd Edition). The global benchmark for deductive structuring, executive synthesis, and boardroom Action Titles.")
    ]

    biblios = biblio_es if lang == 'ES' else biblio_en
    for auth, book, desc in biblios:
        story.append(Paragraph(f"<b>{auth}</b> <i>{book}</i>", styles['BiblioTitle']))
        story.append(Paragraph(desc, styles['BiblioBody']))

    # Construir documento asignando _lang a la clase canvas
    def make_canvas(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c._lang = lang
        return c

    doc.build(story, canvasmaker=make_canvas)
    print(f"[OK] Guía Metodológica PDF generada ({lang}): {out_path}")
    return out_path


def main():
    print("Iniciando generación de Guías Metodológicas DAR en PDF (5 páginas exactas)...")
    es_path = build_pdf(lang='ES')
    en_path = build_pdf(lang='EN')
    print("Guías Metodológicas generadas exitosamente.")


if __name__ == "__main__":
    main()
