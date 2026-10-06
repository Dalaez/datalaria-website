#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para el Executive Decision Pack RACI:
1. packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga/[ES]_Matriz_RACI_Balance_Carga/Guia_Metodologica_RACI_ES.pdf
2. packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga/[EN]_Quantitative_RACI_Workload/Methodology_Guide_RACI_EN.pdf

Estándar editorial de alta dirección (McKinsey / BCG / PMBOK 7ª Ed. / PRINCE2):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (La Falacia de la Matriz RACI Cualitativa).
- Página 2: Sección 2 (Fundamentación Matemática & Reglas Áureas de Gobernanza: Unicidad, Ejecución, Carga Compuesta y Gini).
- Página 3: Sección 3 (Catálogo de Patologías Organizativas & Algoritmos de Corrección: Doble A, Sobrecarga, Parálisis y Tareas Huérfanas).
- Página 4: Sección 4 (Caso de Estudio Realista de Transformación Digital: Proyecto Nexus ERP Cloud).
- Página 5: Sección 5 (Protocolo de Defensa ante el Comité de Dirección - Boardroom FAQ) y Referencias Canónicas.
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
C_TEAL_ACCENT = colors.HexColor("#0D9488")  # Teal 600
C_TEAL_LIGHT = colors.HexColor("#F0FDFA")   # Teal 50

# Acentos y Estados
C_GREEN_ACCENT = colors.HexColor("#10B981") # Emerald 500
C_GREEN_LIGHT = colors.HexColor("#D1FAE5")  # Emerald 100
C_GREEN_TEXT = colors.HexColor("#065F46")   # Emerald 800

C_AMBER_ACCENT = colors.HexColor("#F59E0B") # Amber 500
C_AMBER_LIGHT = colors.HexColor("#FEF3C7")  # Amber 100
C_AMBER_TEXT = colors.HexColor("#92400E")   # Amber 800

C_RED_ACCENT = colors.HexColor("#E11D48")   # Red 600
C_RED_LIGHT = colors.HexColor("#FFF1F2")    # Red 50
C_RED_TEXT = colors.HexColor("#9F1239")     # Red 800

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

        # Cabecera institucional en páginas 2 a 5
        if cur_page > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(C_SLATE_MUTED)
            self.drawString(42, 805, "DATALARIA | EXECUTIVE DECISION PACK")
            header_right = ("MATRIZ RACI CUANTITATIVA & BALANCE DE CARGA OPERATIVA"
                            if lang == 'ES' else
                            "QUANTITATIVE RACI MATRIX & OPERATIONAL WORKLOAD BALANCING")
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
        footer_left = ("Datalaria.com • Documento Confidencial para Comité de Dirección & PMO"
                       if lang == 'ES' else
                       "Datalaria.com • Confidential Executive Committee & PMO Document")
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
            textColor=C_TEAL_ACCENT, spaceAfter=4, textTransform='uppercase'
        ),
        'CoverTitle': ParagraphStyle(
            'CoverTitle', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=17, leading=21,
            textColor=C_NAVY_DARK, spaceAfter=5
        ),
        'CoverSub': ParagraphStyle(
            'CoverSub', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.8, leading=12,
            textColor=C_SLATE_MUTED, spaceAfter=7
        ),
        'SecHeading': ParagraphStyle(
            'SecHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=10.5, leading=13.5,
            textColor=C_NAVY_DARK, spaceBefore=4, spaceAfter=3,
            keepWithNext=True
        ),
        'SubHeading': ParagraphStyle(
            'SubHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=11,
            textColor=C_NAVY_MED, spaceBefore=3, spaceAfter=2,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.6, leading=10.4,
            textColor=C_NAVY_MED, spaceAfter=2.6
        ),
        'Bullet': ParagraphStyle(
            'Bullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.6, leading=10.2,
            textColor=C_NAVY_MED, leftIndent=11, firstLineIndent=-7, spaceAfter=1.6
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
            fontName='Helvetica', fontSize=6.8, leading=8.8,
            textColor=C_NAVY_MED
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=6.8, leading=8.8,
            textColor=C_NAVY_DARK
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica-Oblique', fontSize=7.4, leading=9.8,
            textColor=C_NAVY_DARK
        ),
        'FAQ_Q': ParagraphStyle(
            'FAQ_Q', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.8, leading=10.2,
            textColor=C_NAVY_DARK, spaceBefore=2.8, spaceAfter=1.2,
            keepWithNext=True
        ),
        'FAQ_A': ParagraphStyle(
            'FAQ_A', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.4, leading=9.8,
            textColor=C_NAVY_MED, spaceAfter=3.0
        ),
        'BiblioTitle': ParagraphStyle(
            'BiblioTitle', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.6, leading=9.8,
            textColor=C_NAVY_DARK, spaceBefore=3.5, spaceAfter=1.0,
            keepWithNext=True
        ),
        'BiblioBody': ParagraphStyle(
            'BiblioBody', parent=base['Normal'],
            fontName='Helvetica', fontSize=6.9, leading=9.0,
            textColor=C_SLATE_MUTED, spaceAfter=2.0
        )
    }
    return styles


def build_meta_card(styles, lang='ES'):
    data = [
        [
            Paragraph("<b>Autor:</b> Dirección de Estrategia & Control Operativo Datalaria" if lang == 'ES' else "<b>Author:</b> Datalaria Strategy & Operational Control Practice", styles['TableCell']),
            Paragraph("<b>Estándar:</b> PMBOK 7ª Ed. · PRINCE2 · CMMI V2.0" if lang == 'ES' else "<b>Standard:</b> PMBOK 7th Ed. · PRINCE2 · CMMI V2.0", styles['TableCell'])
        ],
        [
            Paragraph("<b>Destinatarios:</b> CEOs, COOs, PMO Directors y Tech Leads" if lang == 'ES' else "<b>Audience:</b> CEOs, COOs, PMO Directors & Tech Leads", styles['TableCell']),
            Paragraph("<b>Gobernanza:</b> ECMA-376 / Balance FTE / Auditoría de Saturación" if lang == 'ES' else "<b>Governance:</b> ECMA-376 / FTE Balancing / Saturation Audit", styles['TableCell'])
        ]
    ]
    t = Table(data, colWidths=[255, 255])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
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
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


def build_pdf(lang='ES', out_path=None):
    if out_path is None:
        base_dir = "packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga"
        sub_dir = "[ES]_Matriz_RACI_Balance_Carga" if lang == 'ES' else "[EN]_Quantitative_RACI_Workload"
        fname = "Guia_Metodologica_RACI_ES.pdf" if lang == 'ES' else "Methodology_Guide_RACI_EN.pdf"
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
    # PÁGINA 1: PORTADA & SECCIÓN 1 (LA FALACIA DE LA MATRIZ RACI CUALITATIVA)
    # ==========================================================================
    kicker = ("SUITE 03 · CONTROL OPERATIVO & GOBERNANZA | ESTÁNDAR PMBOK 7ª ED. & PRINCE2"
              if lang == 'ES' else
              "SUITE 03 · OPERATIONAL CONTROL & GOVERNANCE | PMBOK 7TH ED. & PRINCE2 STANDARD")
    title = ("MATRIZ RACI CUANTITATIVA & BALANCE DE CARGA OPERATIVA"
             if lang == 'ES' else
             "QUANTITATIVE RACI MATRIX & OPERATIONAL WORKLOAD BALANCING")
    subtitle = ("Protocolo formal de rendición de cuentas, unicidad de Accountable, calibración de FTEs por rol y detección de cuellos de botella organizativos para Comités de Dirección."
                if lang == 'ES' else
                "A formal quantitative governance framework for single accountability enforcement, role-based FTE calibration, and organizational bottleneck mitigation before Executive Committees.")

    story.append(Paragraph(kicker, styles['CoverKicker']))
    story.append(Paragraph(title, styles['CoverTitle']))
    story.append(Paragraph(subtitle, styles['CoverSub']))
    story.append(build_meta_card(styles, lang=lang))
    story.append(Spacer(1, 6))

    # Sección 1
    sec1_title = ("1. La Falacia de la Matriz RACI Cualitativa y el Vacío Operativo en la Alta Dirección"
                  if lang == 'ES' else
                  "1. The Fallacy of Qualitative RACI Matrices and the Executive Execution Gap")
    story.append(Paragraph(sec1_title, styles['SecHeading']))

    sec1_body_es = [
        "En más del 80% de las corporaciones y oficinas de gestión de proyectos (PMO), la matriz RACI tradicional se concibe como un mero ejercicio burocrático de inicio de proyecto. Se completa durante la fase de lanzamiento, se inserta en un anexo documental y se archiva indefinidamente en repositorios compartidos sin volver a consultarse jamás.",
        "La causa raíz de este fracaso metodológico sistemático radica en que las matrices RACI convencionales son <b>estrictamente cualitativas y estáticas</b>: tratan cada letra asignada (R, A, C, I) como un indicador binario homogéneo, ignorando por completo la carga temporal asociada, la capacidad instalada de los departamentos y las relaciones de dependencia crítica.",
        "La consultoría estratégica de operaciones identifica cuatro patologías estructurales que destruyen la efectividad de los modelos cualitativos:",
        "<b>1. La Trampa del Accountable Múltiple (Accountability Dilution):</b> Cuando un entregable complejo asigna la letra 'A' a dos o más directores para reflejar una supuesta 'corresponsabilidad colegiada', el resultado empírico es la tragedia de los comunes: ante desviaciones presupuestarias o retrasos críticos, nadie asume la pérdida.",
        "<b>2. La Ceguera de la Capacidad Real (Unweighted Workload Blindness):</b> Diseñar una matriz sin cuantificar el esfuerzo necesario provoca que perfiles técnicos clave (Tech Leads, Arquitectos o Ingenieros Senior) acumulen simultáneamente decenas de 'R' y 'A', operando a más del 140% de su capacidad nominal sin que la PMO lo detecte hasta el colapso.",
        "<b>3. La Parálisis por Consenso Indiscriminado:</b> Otorgar el rol 'Consulted' (C) a 5 o 6 departamentos como cortesía corporativa transforma tareas operativas ágiles en ciclos infinitos de revisión, aprobaciones cruzadas y reuniones improductivas.",
        "<b>4. La Ilusión de Cobertura de las Tareas Huérfanas:</b> La asignación formal de un sponsor o Accountable ejecutivo genera la falsa sensación de seguridad de que la tarea está bajo control, ignorando que ningún equipo tiene asignada la ejecución directa ('R')."
    ]
    sec1_body_en = [
        "In more than 80% of enterprises and project management offices (PMOs), traditional RACI matrices serve as little more than a ceremonial project initiation artifact. Drafted during project kickoff, inserted into onboarding decks, and subsequently forgotten in intranet drives, qualitative RACI charts fail to govern actual day-to-day operations.",
        "The root cause of this systemic governance breakdown is that legacy RACI charts are <b>strictly qualitative and static</b>: they treat each letter (R, A, C, I) as an unweighted nominal tag, completely ignoring effort commitments, nominal team capacity, and operational bottleneck constraints.",
        "Operations and corporate strategy consulting identify four fundamental structural failures in qualitative RACI frameworks:",
        "<b>1. The Diluted Accountability Trap:</b> Assigning the 'A' label to multiple directors under the guise of 'shared strategic ownership' triggers the classic tragedy of the commons: when project milestones slip or budgets overrun, zero individual ownership is retained.",
        "<b>2. Capacity Blindness:</b> Without weighting effort mathematically, senior specialists (Tech Leads, Architects) accumulate countless 'R' and 'A' obligations, operating at >140% capacity while leadership remains blind to burnout until critical paths stall.",
        "<b>3. Consensus Paralysis:</b> Assigning 'Consulted' (C) status to multiple managers as organizational courtesy converts routine technical execution into endless review boards and circular debates.",
        "<b>4. Orphan Deliverable Illusion:</b> Assigning an executive Accountable without a dedicated Responsible executor creates a false sense of security while no actual execution takes place."
    ]
    sec1_body = sec1_body_es if lang == 'ES' else sec1_body_en
    for p_txt in sec1_body:
        story.append(Paragraph(p_txt, styles['Body']))

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 2: SECCIÓN 2 (FUNDAMENTACIÓN MATEMÁTICA Y REGLAS ÁUREAS)
    # ==========================================================================
    sec2_title = ("2. Fundamentación Matemática y Reglas Áureas de Gobernanza Cuantitativa"
                  if lang == 'ES' else
                  "2. Mathematical Foundations & Golden Rules of Quantitative Governance")
    story.append(Paragraph(sec2_title, styles['SecHeading']))

    sec2_intro_es = "Para transformar la matriz RACI en un motor cuantitativo auditable y predictivo, establecemos un modelo algebraico formal regido por cuatro postulados innegociables:"
    sec2_intro_en = "To transform RACI modeling into an audited, predictive capacity engine, we establish a formal mathematical system governed by four non-negotiable principles:"
    story.append(Paragraph(sec2_intro_es if lang == 'ES' else sec2_intro_en, styles['Body']))

    # Regla 1
    r1_title_es = "Principio 1: Regla de Unicidad de Rendición de Cuentas (Single Accountability)"
    r1_title_en = "Principle 1: Single Accountability Invariance Rule"
    story.append(Paragraph(r1_title_es if lang == 'ES' else r1_title_en, styles['SubHeading']))
    f1_math = "&sum;<sub>k=1</sub><sup>m</sup> A<sub>ik</sub> = 1 &nbsp;&nbsp;&forall; i &isin; {1, ..., n}"
    f1_desc_es = "Para cada entregable <i>i</i> del WBS, debe existir exactamente un único rol <i>k</i> como Accountable (A). Si la suma es 0, la tarea es huérfana; si es &ge; 2, la responsabilidad queda judicialmente diluida."
    f1_desc_en = "For every WBS milestone <i>i</i>, exactly one single role <i>k</i> must be designated as Accountable (A). If sum = 0, task is orphan; if &ge; 2, accountability is legally and operationally void."
    story.append(build_formula_box(f1_math, f1_desc_es if lang == 'ES' else f1_desc_en, styles))
    story.append(Spacer(1, 4))

    # Regla 2
    r2_title_es = "Principio 2: Regla de Ejecución Activa Mínima (Active Execution Mandate)"
    r2_title_en = "Principle 2: Minimum Active Execution Mandate"
    story.append(Paragraph(r2_title_es if lang == 'ES' else r2_title_en, styles['SubHeading']))
    f2_math = "&sum;<sub>k=1</sub><sup>m</sup> R<sub>ik</sub> &ge; 1 &nbsp;&nbsp;&forall; i &isin; {1, ..., n}"
    f2_desc_es = "Ningún hito puede existir sin al menos un ejecutor directo (Responsible). Si &sum; R<sub>ik</sub> = 0, el entregable carece de motor productivo y constituye una alerta roja en la auditoría de PMO."
    f2_desc_en = "No project deliverable may exist without at least one direct builder (Responsible). If &sum; R<sub>ik</sub> = 0, deliverable lacks productive execution and triggers an immediate PMO audit block."
    story.append(build_formula_box(f2_math, f2_desc_es if lang == 'ES' else f2_desc_en, styles))
    story.append(Spacer(1, 4))

    # Regla 3
    r3_title_es = "Principio 3: Modelo de Carga de Trabajo Compuesta Ponderada (Composite Workload Model)"
    r3_title_en = "Principle 3: Composite Weighted Workload Allocation Model"
    story.append(Paragraph(r3_title_es if lang == 'ES' else r3_title_en, styles['SubHeading']))
    f3_math = "W<sub>k</sub> = &sum;<sub>i=1</sub><sup>n</sup> [ w<sub>A</sub> &middot; A<sub>ik</sub> + w<sub>R</sub> &middot; R<sub>ik</sub> + w<sub>C</sub> &middot; C<sub>ik</sub> + w<sub>I</sub> &middot; I<sub>ik</sub> ]"
    f3_desc_es = "La carga total asignada al rol <i>k</i> (W<sub>k</sub>) es la suma lineal ponderada de sus implicaciones. Parámetros calibrados: w<sub>R</sub> = 26.0h (ejecución), w<sub>A</sub> = 12.0h (decisión/sign-off), w<sub>C</sub> = 5.0h (asesoría), w<sub>I</sub> = 1.5h (alineación)."
    f3_desc_en = "Total workload allocated to role <i>k</i> (W<sub>k</sub>) is the weighted linear combination of involvement types. Calibrated weights: w<sub>R</sub> = 26.0h (execution), w<sub>A</sub> = 12.0h (decision/sign-off), w<sub>C</sub> = 5.0h (advisory), w<sub>I</sub> = 1.5h (alignment)."
    story.append(build_formula_box(f3_math, f3_desc_es if lang == 'ES' else f3_desc_en, styles))
    story.append(Spacer(1, 4))

    # Regla 4
    r4_title_es = "Principio 4: Ratio de Saturación Operativa y Coeficiente de Gini Organizacional"
    r4_title_en = "Principle 4: Operational Saturation Ratio & Organizational Gini Index"
    story.append(Paragraph(r4_title_es if lang == 'ES' else r4_title_en, styles['SubHeading']))
    f4_math_es = "S<sub>k</sub> = W<sub>k</sub> / C<sub>k</sub> &nbsp;&nbsp;|&nbsp;&nbsp; G = [ &sum;<sub>j=1</sub><sup>m</sup> &sum;<sub>k=1</sub><sup>m</sup> |S<sub>j</sub> - S<sub>k</sub>| ] / [ 2 &middot; m<sup>2</sup> &middot; S<sub>media</sub> ]"
    f4_math_en = "S<sub>k</sub> = W<sub>k</sub> / C<sub>k</sub> &nbsp;&nbsp;|&nbsp;&nbsp; G = [ &sum;<sub>j=1</sub><sup>m</sup> &sum;<sub>k=1</sub><sup>m</sup> |S<sub>j</sub> - S<sub>k</sub>| ] / [ 2 &middot; m<sup>2</sup> &middot; S<sub>mean</sub> ]"
    f4_math = f4_math_es if lang == 'ES' else f4_math_en
    f4_desc_es = "El ratio de saturación S<sub>k</sub> evalúa la carga frente a la capacidad nominal C<sub>k</sub>. Semáforo: Verde (&lt;80%), Ámbar (80-100%), Rojo (&gt;100%). El Coeficiente de Gini (G) mide la desigualdad en el equipo (donde S<sub>media</sub> es la saturación media): un G &gt; 0.35 exige rebalanceo formal."
    f4_desc_en = "Saturation S<sub>k</sub> maps workload W<sub>k</sub> against nominal capacity C<sub>k</sub>. Heatmap: Green (&lt;80%), Amber (80-100%), Red (&gt;100%). Organizational Gini Index (G) quantifies inequality (where S<sub>mean</sub> is average saturation): G &gt; 0.35 mandates immediate Board rebalancing."
    story.append(build_formula_box(f4_math, f4_desc_es if lang == 'ES' else f4_desc_en, styles))

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 3: SECCIÓN 3 (CATÁLOGO DE PATOLOGÍAS Y ALGORITMOS DE CORRECCIÓN)
    # ==========================================================================
    sec3_title = ("3. Catálogo de Patologías Organizativas y Algoritmos de Corrección"
                  if lang == 'ES' else
                  "3. Organizational Pathology Catalog & Rebalancing Algorithms")
    story.append(Paragraph(sec3_title, styles['SecHeading']))

    sec3_intro_es = "La cuantificación del esfuerzo permite a la PMO y al COO diagnosticar de inmediato las cuatro disfunciones organizativas canónicas y aplicar algoritmos de corrección matemáticamente fundados:"
    sec3_intro_en = "Mathematical effort modeling enables PMOs and COOs to diagnose the four canonical organizational pathologies and deploy automated corrective protocols:"
    story.append(Paragraph(sec3_intro_es if lang == 'ES' else sec3_intro_en, styles['Body']))

    # Tabla de patologías
    th_pat_es = ["Patología Organizativa", "Síntoma Cuantitativo", "Riesgo Directivo", "Algoritmo de Corrección Inmediata"]
    th_pat_en = ["Organizational Pathology", "Quantitative Trigger", "Executive Risk Exposure", "Corrective Action Protocol"]
    th_pat = th_pat_es if lang == 'ES' else th_pat_en

    rows_pat_es = [
        [
            Paragraph("<b>Dilución de Responsabilidad</b><br/>(Multiple Accountables)", styles['TableCellBold']),
            Paragraph("COUNTIF(A) &gt; 1 en hito WBS", styles['TableCell']),
            Paragraph("Tragedia de comunes: disputas políticas y parálisis ante errores.", styles['TableCell']),
            Paragraph("<b>Escisión de WBS</b> en sub-entregables o designación de Lead Delegado con veto único.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Cuello de Botella Crítico</b><br/>(Bottleneck Overload)", styles['TableCellBold']),
            Paragraph("Saturación S<sub>k</sub> &gt; 100% (ej. Tech Lead 142%)", styles['TableCell']),
            Paragraph("Burnout severo, retrasos en cascada en ruta crítica, rotación de talento.", styles['TableCell']),
            Paragraph("<b>Delegación de R:</b> Transferir tareas directas 'R' a perfiles soporte y retener sólo 'A'.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Parálisis por Consenso</b><br/>(Review Drag / Over-Consultation)", styles['TableCellBold']),
            Paragraph("COUNTIF(C) &ge; 4 en entregables de desarrollo", styles['TableCell']),
            Paragraph("Reuniones circulares, dilación de plazos (+45%) y fatiga de comités.", styles['TableCell']),
            Paragraph("<b>Racionalización C&rarr;I:</b> Degradar a 'Informed' con ventana asíncrona de 48h.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Entregable Huérfano</b><br/>(Orphan Execution Gap)", styles['TableCellBold']),
            Paragraph("COUNTIF(R) = 0 y COUNTIF(A) = 1", styles['TableCell']),
            Paragraph("Falso confort ejecutivo: la tarea no avanza y se bloquea en silencio.", styles['TableCell']),
            Paragraph("<b>Asignación Mandatoria de R:</b> Vincular responsable técnico antes de abrir el sprint.", styles['TableCell'])
        ]
    ]

    rows_pat_en = [
        [
            Paragraph("<b>Accountability Dilution</b><br/>(Multiple Accountables)", styles['TableCellBold']),
            Paragraph("COUNTIF(A) &gt; 1 on WBS deliverable", styles['TableCell']),
            Paragraph("Tragedy of the commons: political friction and zero ownership.", styles['TableCell']),
            Paragraph("<b>Split WBS</b> into distinct sub-tasks or designate a single Lead with veto rights.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Critical Bottleneck</b><br/>(Bottleneck Overload)", styles['TableCellBold']),
            Paragraph("Saturation S<sub>k</sub> &gt; 100% (e.g., Tech Lead 142%)", styles['TableCell']),
            Paragraph("Burnout risk, cascaded critical path delays, voluntary turnover.", styles['TableCell']),
            Paragraph("<b>Delegate 'R':</b> Reassign execution to engineering teams while retaining supervisory 'A'.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Consensus Paralysis</b><br/>(Review Drag / Over-Consultation)", styles['TableCellBold']),
            Paragraph("COUNTIF(C) &ge; 4 on execution milestones", styles['TableCell']),
            Paragraph("Circular reviews, cycle-time inflation (+45%), meeting fatigue.", styles['TableCell']),
            Paragraph("<b>Streamline C&rarr;I:</b> Downgrade to 'Informed' with 48h asynchronous review window.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Orphan Milestone</b><br/>(Orphan Execution Gap)", styles['TableCellBold']),
            Paragraph("COUNTIF(R) = 0 and COUNTIF(A) = 1", styles['TableCell']),
            Paragraph("False executive assurance: task has oversight but zero execution.", styles['TableCell']),
            Paragraph("<b>Mandatory 'R' Assignment:</b> Bind technical owner prior to phase commencement.", styles['TableCell'])
        ]
    ]

    r_pat = rows_pat_es if lang == 'ES' else rows_pat_en
    table_data = [[Paragraph(h, styles['TableHeader']) for h in th_pat]] + r_pat

    t_pat = Table(table_data, colWidths=[120, 110, 130, 150])
    t_pat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_pat)
    story.append(Spacer(1, 6))

    # Protocolo de Rebalanceo en 3 Pasos
    p3_h_es = "Protocolo de Ejecución del Rebalanceo en Tres Fases:"
    p3_h_en = "Three-Step Rebalancing Execution Protocol:"
    story.append(Paragraph(p3_h_es if lang == 'ES' else p3_h_en, styles['SubHeading']))

    proto_steps_es = [
        "<b>Fase 1 · Auditoría de Integridad (Día 1-2):</b> Ejecutar fórmulas de verificación en Excel/Sheets. Identificar discrepancias de gobernanza (A &ne; 1 o R = 0) y roles con saturación &gt; 100%.",
        "<b>Fase 2 · Desacoplamiento & Delegación (Día 3-5):</b> Para cada rol saturado, reclasificar tareas operativas directas de 'R' hacia perfiles con capacidad disponible (&lt;80%). El rol senior retiene 'A' de supervisión.",
        "<b>Fase 3 · Formalización en Gateway (Día 6-8):</b> Llevar la matriz equilibrada al Comité de Dirección. Obtener firma vinculante del COO, PMO y Tech Director en el Plan de Acción."
    ]
    proto_steps_en = [
        "<b>Step 1 · Integrity Audit (Days 1-2):</b> Run automated formulas in Excel/Sheets. Flag governance violations (A &ne; 1 or R = 0) and roles exceeding 100% capacity.",
        "<b>Step 2 · Decoupling & Delegation (Days 3-5):</b> For each bottleneck role, transfer direct execution 'R' to roles with idle bandwidth (&lt;80%). Retain supervisory 'A' on senior leads.",
        "<b>Step 3 · Board Decision Gateway (Days 6-8):</b> Submit balanced RACI matrix to Executive Committee. Secure binding authorization from COO, PMO Director, and Tech Lead."
    ]
    p_steps = proto_steps_es if lang == 'ES' else proto_steps_en
    for s_txt in p_steps:
        story.append(Paragraph(f"• {s_txt}", styles['Bullet']))

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 4: SECCIÓN 4 (CASO DE ESTUDIO REALISTA - PROJECT NEXUS ERP CLOUD)
    # ==========================================================================
    sec4_title = ("4. Caso Práctico Corporativo Resuelto: Proyecto Nexus ERP Cloud en Global Logistics"
                  if lang == 'ES' else
                  "4. Solved Corporate Case Study: Project Nexus Cloud ERP at Global Logistics")
    story.append(Paragraph(sec4_title, styles['SecHeading']))

    sec4_text_es = [
        "<b>Contexto Corporativo:</b> Global Logistics Corp, operador multimodal con 4.500 empleados y presencia en 12 países, acomete la migración de su sistema central a una plataforma ERP Cloud integrada. El proyecto comprende 25 entregables críticos estructurados en 5 fases WBS e involucra a 9 departamentos clave.",
        "<b>Diagnóstico Inicial de la PMO:</b> La auditoría automatizada reveló una grave distorsión organizativa: el Tech Lead acumulaba 7 hitos como Accountable y 5 como Responsible, totalizando 228 horas de dedicación frente a una capacidad nominal de 160 horas (142.5% de saturación). Simultáneamente, la tarea WBS 3.3 (Desarrollo Frontend) presentaba 'A' dual entre el Tech Lead y el Product Owner, y el Plan Maestro de Pruebas (WBS 4.1) carecía de ejecutor 'R'. El proyecto acumulaba una previsión de desvío de +6 semanas en el Go-Live.",
        "<b>Intervención Cuantitativa de Rebalanceo:</b> La Dirección de Operaciones aplicó el Executive Decision Pack oficial de Datalaria ejecutando cinco acciones correctivas inmediatas:"
    ]
    sec4_text_en = [
        "<b>Enterprise Context:</b> Global Logistics Corp, a freight and supply-chain enterprise with 4,500 employees across 12 countries, initiated a core Cloud ERP transformation. The initiative encompasses 25 critical deliverables across 5 WBS phases involving 9 functional departments.",
        "<b>Initial PMO Governance Audit:</b> Automated model audit detected severe structural friction: the Tech Lead concentrated 7 deliverables as Accountable and 5 as Responsible, totaling 228 hours against 160h capacity (142.5% saturation). Concurrently, WBS 3.3 (Frontend Portal) had dual Accountables, and WBS 4.1 (Test Plan) had zero Responsible executors. Project forecasts projected a +6 weeks critical-path slip.",
        "<b>Quantitative Rebalancing Protocol:</b> Operations leadership deployed the Datalaria Executive Decision Pack, executing five surgical rebalancing actions:"
    ]
    sec4_text = sec4_text_es if lang == 'ES' else sec4_text_en
    for p_txt in sec4_text:
        story.append(Paragraph(p_txt, styles['Body']))

    # Acciones del caso
    case_actions_es = [
        "<b>ACT-01:</b> Delegación de 'R' en Infraestructura CI/CD (WBS 3.1) al equipo de DevOps (-26.0h).",
        "<b>ACT-02:</b> Degradar 'C' a 'I' en revisiones de interfaces frontend (WBS 3.3) (-5.0h).",
        "<b>ACT-03:</b> Transferir 'A' en Matriz de Interesados (WBS 1.2) al Product Owner (-12.0h).",
        "<b>ACT-04:</b> Reasignar 'R' en Migración de Datos (WBS 3.5) a Ingeniero Senior (-26.0h).",
        "<b>ACT-05:</b> Asignar formalmente 'R' en Plan de Pruebas (WBS 4.1) a QA Senior (+26.0h QA)."
    ]
    case_actions_en = [
        "<b>ACT-01:</b> Reassigned execution 'R' on CI/CD pipelines (WBS 3.1) to DevOps lead (-26.0h).",
        "<b>ACT-02:</b> Downgraded 'C' to 'I' on UI review meetings (WBS 3.3) to eliminate review drag (-5.0h).",
        "<b>ACT-03:</b> Reallocated supervisory 'A' on Stakeholder Matrix (WBS 1.2) to Product Owner (-12.0h).",
        "<b>ACT-04:</b> Reassigned 'R' on Data Migration (WBS 3.5) to Senior Backend Engineer (-26.0h).",
        "<b>ACT-05:</b> Formally designated senior QA engineer as Responsible 'R' on Master Test Plan (+26.0h QA)."
    ]
    c_acts = case_actions_es if lang == 'ES' else case_actions_en
    for ca_txt in c_acts:
        story.append(Paragraph(f"• {ca_txt}", styles['Bullet']))
    story.append(Spacer(1, 4))

    # Tabla Comparativa de Resultados
    th_res_es = ["Métrica Operativa", "Estado Inicial (Pre-Auditoría)", "Estado Rebalanceado (Post-Plan)", "Impacto Directivo"]
    th_res_en = ["Operational Metric", "Baseline (Pre-Audit)", "Balanced (Post-Plan)", "Executive Impact"]
    th_res = th_res_es if lang == 'ES' else th_res_en

    rows_res_es = [
        [Paragraph("Saturación Tech Lead", styles['TableCellBold']), Paragraph("142.5% (228.0 h) - Crítico", styles['TableCell']), Paragraph("87.5% (140.0 h) - Equilibrado", styles['TableCellBold']), Paragraph("Eliminación de riesgo de burnout y fuga.", styles['TableCell'])],
        [Paragraph("Salud de Gobernanza RACI", styles['TableCellBold']), Paragraph("84.0% (4 anomalías)", styles['TableCell']), Paragraph("100.0% (25/25 conformes)", styles['TableCellBold']), Paragraph("Unicidad de A blindada ante auditoría.", styles['TableCell'])],
        [Paragraph("Desviación Go-Live Proyectada", styles['TableCellBold']), Paragraph("+6 semanas de retraso", styles['TableCell']), Paragraph("0 semanas (Cumplimiento en fecha)", styles['TableCellBold']), Paragraph("Ahorro de ~180.000 € en sobrecostes.", styles['TableCell'])],
        [Paragraph("Coeficiente Gini de Carga", styles['TableCellBold']), Paragraph("0.41 (Inequidad severa)", styles['TableCell']), Paragraph("0.22 (Distribución balanceada)", styles['TableCellBold']), Paragraph("Alineación y moral de equipo restaurada.", styles['TableCell'])],
    ]
    rows_res_en = [
        [Paragraph("Tech Lead Saturation", styles['TableCellBold']), Paragraph("142.5% (228.0 h) - Critical", styles['TableCell']), Paragraph("87.5% (140.0 h) - Sustainable", styles['TableCellBold']), Paragraph("Burnout risk eradicated, turnover risk neutralized.", styles['TableCell'])],
        [Paragraph("RACI Governance Health", styles['TableCellBold']), Paragraph("84.0% (4 anomalies)", styles['TableCell']), Paragraph("100.0% (25/25 compliant)", styles['TableCellBold']), Paragraph("Single accountability legally auditable.", styles['TableCell'])],
        [Paragraph("Projected Go-Live Slippage", styles['TableCellBold']), Paragraph("+6 weeks delay", styles['TableCell']), Paragraph("0 weeks (On-time milestone delivery)", styles['TableCellBold']), Paragraph("Saved ~€180,000 in operational drag.", styles['TableCell'])],
        [Paragraph("Workload Gini Index", styles['TableCellBold']), Paragraph("0.41 (Severe asymmetry)", styles['TableCell']), Paragraph("0.22 (Healthy distribution)", styles['TableCellBold']), Paragraph("Restored cross-functional team morale.", styles['TableCell'])],
    ]
    r_res = rows_res_es if lang == 'ES' else rows_res_en
    t_res_data = [[Paragraph(h, styles['TableHeader']) for h in th_res]] + r_res

    t_res = Table(t_res_data, colWidths=[120, 125, 125, 140])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_res)

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 5: SECCIÓN 5 (BOARD DEFENSE FAQ & BIBLIOGRAFÍA)
    # ==========================================================================
    sec5_title = ("5. Protocolo de Defensa ante el Comité de Dirección & Referencias Canónicas"
                  if lang == 'ES' else
                  "5. Boardroom Defense Protocol (FAQ) & Canonical References")
    story.append(Paragraph(sec5_title, styles['SecHeading']))

    faq_es = [
        ("1. ¿Por qué no podemos compartir el Accountable entre dos directores para reflejar la corresponsabilidad?",
         "Porque en gobernanza corporativa, la corresponsabilidad compartida equivale a la irresponsabilidad absoluta. Cuando surge una contingencia crítica o sobrecoste, la ambigüedad diluye las consecuencias. La buena práctica consiste en asignar exactamente un Accountable y desglosar el entregable en dos sub-tareas si existen responsabilidades complementarias."),
        ("2. ¿Cómo recortar los roles 'Consultados' sin ofender a mandos intermedios ni generar rechazo al cambio?",
         "Estableciendo contractualmente que el rol 'Informed' (I) no implica exclusión, sino respeto por su tiempo. Los perfiles informados reciben acceso en tiempo real a las actas y entregables finales, pero se les libera de la carga de asistir a reuniones de diseño técnico salvo que soliciten formalmente una sesión bilateral."),
        ("3. ¿Cómo justificar la externalización o nuevas contrataciones ante el CFO con los datos de saturación?",
         "Presentando el semáforo cuantitativo y el ratio S<sub>k</sub>. Cuando un rol clave opera de forma sostenida al 140% de capacidad y se demuestra que todas sus tareas secundarias ya han sido delegadas a roles soporte sin liberar el cuello de botella, la contratación o el refuerzo externo deja de ser una opinión subjetiva y se convierte en un imperativo de protección de activos."),
        ("4. ¿Qué ocurre si un rol asignado como 'Responsible' discrepa técnicamente del 'Accountable'?",
         "El modelo cuantitativo delimita con claridad la autoridad de decisión: el Responsible ejecuta y propone soluciones técnicas, pero el Accountable ostenta la autoridad final de sign-off y asume el riesgo ante el Comité. La discrepancia se documenta en el log de riesgos pero no paraliza la entrega."),
        ("5. ¿Con qué cadencia temporal debe auditarse la matriz RACI y el balance de carga?",
         "Bimestralmente en la PMO o al cierre de cada fase WBS. Los proyectos son dinámicos y la redistribución de tareas debe actualizarse cada vez que se apruebe una orden de cambio de alcance o se incorporen nuevos requerimientos de negocio.")
    ]

    faq_en = [
        ("1. Why can't two directors share the Accountable role to reflect joint partnership?",
         "Because in corporate governance, shared accountability equals zero accountability. When a critical failure occurs, ambiguous ownership paralyses remediation. Best practice dictates assigning a single Accountable and splitting the milestone into sub-deliverables if domains truly diverge."),
        ("2. How do we reduce 'Consulted' assignments without causing political friction with middle management?",
         "By framing the 'Informed' (I) status as executive respect for their time. Informed stakeholders retain complete real-time access to outputs while being freed from circular review meetings, preserving their capacity for primary domain goals."),
        ("3. How do we justify hiring or external consulting to the CFO using quantitative workload data?",
         "By presenting audited saturation ratios S<sub>k</sub>. When a core lead operates at >140% capacity after delegating all non-core tasks, requesting external capacity transitions from a subjective demand into an audited risk-mitigation imperative."),
        ("4. What protocol governs technical disagreements between a Responsible and their Accountable?",
         "Quantitative RACI explicitly separates execution from decision rights: the Responsible builds and proposes technical implementations, but the Accountable retains exclusive veto and sign-off authority, bearing ultimate performance liability."),
        ("5. What is the required governance cadence for auditing RACI workload health?",
         "Bimonthly or upon the closure of each WBS stage gate. Project scope evolves dynamically; capacity ratios must be refreshed whenever formal change requests alter milestone volume.")
    ]

    faq = faq_es if lang == 'ES' else faq_en
    for q_txt, a_txt in faq:
        story.append(Paragraph(f"<b>{q_txt}</b>", styles['FAQ_Q']))
        story.append(Paragraph(a_txt, styles['FAQ_A']))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Referencias Bibliográficas Canónicas de Autoridad:" if lang == 'ES' else "Canonical Professional & Academic References:", styles['SubHeading']))

    biblio_es = [
        ("Project Management Institute (PMI) (2021).", "<i>A Guide to the Project Management Body of Knowledge (PMBOK Guide) – 7th Edition</i>. Project Management Institute, Newtown Square, PA. Estándar canónico global sobre gobernanza de entregables y asignación de responsabilidades."),
        ("Axelos (2017).", "<i>Managing Successful Projects with PRINCE2 (6th Edition)</i>. TSO (The Stationery Office), London. Marco directivo de rendición de cuentas única y delegación estructurada por paquetes de trabajo."),
        ("Cleland, David I. & King, William R. (1983).", "<i>Systems Analysis and Project Management</i>. McGraw-Hill. Obra fundacional que formalizó la matriz de asignación de responsabilidades (RAM) en ingeniería."),
        ("Minto, Barbara (2009).", "<i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall. Estándar de comunicación ejecutiva y estructuración deductiva adoptado por McKinsey, BCG y Bain."),
        ("CMMI Institute (2018).", "<i>CMMI for Development (V2.0): Organizational Governance & Monitoring</i>. Information Science Institute / Carnegie Mellon University. Marco de auditoría de procesos organizacionales.")
    ]

    biblio_en = [
        ("Project Management Institute (PMI) (2021).", "<i>A Guide to the Project Management Body of Knowledge (PMBOK Guide) – 7th Edition</i>. Project Management Institute. Global benchmark for governance baselines and role accountability."),
        ("Axelos (2017).", "<i>Managing Successful Projects with PRINCE2 (6th Edition)</i>. TSO, London. Foundational framework for single executive accountability and work-package delegation."),
        ("Cleland, David I. & King, William R. (1983).", "<i>Systems Analysis and Project Management</i>. McGraw-Hill. Seminal academic foundation for Responsibility Assignment Matrices (RAM)."),
        ("Minto, Barbara (2009).", "<i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall. Definitive executive communication framework utilized by McKinsey, BCG, and Bain."),
        ("CMMI Institute (2018).", "<i>CMMI for Development (V2.0): Organizational Governance & Monitoring</i>. Carnegie Mellon University. Industry standard for process assurance and decision governance.")
    ]

    biblio = biblio_es if lang == 'ES' else biblio_en
    for b_auth, b_desc in biblio:
        story.append(Paragraph(f"• <b>{b_auth}</b> {b_desc}", styles['BiblioBody']))

    # Construir documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"  -> Generada guía metodológica PDF: {out_path}")


def main():
    base_dir = "packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga"
    dir_es = os.path.join(base_dir, "[ES]_Matriz_RACI_Balance_Carga")
    dir_en = os.path.join(base_dir, "[EN]_Quantitative_RACI_Workload")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    file_es = os.path.join(dir_es, "Guia_Metodologica_RACI_ES.pdf")
    file_en = os.path.join(dir_en, "Methodology_Guide_RACI_EN.pdf")

    print("[1/2] Generando guía metodológica en Español...")
    build_pdf(lang='ES', out_path=file_es)

    print("[2/2] Generando guía metodológica en Inglés...")
    build_pdf(lang='EN', out_path=file_en)


if __name__ == "__main__":
    main()
