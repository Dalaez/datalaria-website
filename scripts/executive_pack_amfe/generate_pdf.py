#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para el Executive Decision Pack AMFE / Riesgos:
1. packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE/[ES]_Matriz_Riesgos_AMFE/Guia_Metodologica_AMFE_Riesgos_ES.pdf
2. packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE/[EN]_FMEA_Risk_Matrix/Methodology_Guide_FMEA_Risk_EN.pdf

Estándar editorial de alta dirección (ISO 31000 / AIAG-VDA / McKinsey Risk Practice):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (La Falacia de la Gestión Cualitativa de Riesgos).
- Página 2: Sección 2 (Fundamentación Matemática: E(L), NPR = S x O x D, Prioridad de Acción AIAG-VDA y CER).
- Página 3: Sección 3 (Baremos de Calibración Objetiva 1-10 para Severidad, Ocurrencia y Detección).
- Página 4: Sección 4 (Caso de Estudio Realista: Resiliencia en Pasarela Transaccional Cloud & Reducción 91.8%).
- Página 5: Sección 5 (Protocolo de Defensa ante Comité - Boardroom FAQ) y Referencias Canónicas.
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
C_TEAL_ACCENT = colors.HexColor("#0D9488")  # Teal 600
C_TEAL_LIGHT = colors.HexColor("#F0FDFA")   # Teal 50

# Acentos y Estados
C_GREEN_ACCENT = colors.HexColor("#10B981") # Emerald 500
C_GREEN_LIGHT = colors.HexColor("#D1FAE5")  # Emerald 100
C_GREEN_TEXT = colors.HexColor("#065F46")   # Emerald 800

C_AMBER_ACCENT = colors.HexColor("#F59E0B") # Amber 500
C_AMBER_BORDER = colors.HexColor("#F59E0B") # Amber 500
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
            header_right = ("MATRIZ DE RIESGOS CUANTITATIVA & AMFE OPERATIVO"
                            if lang == 'ES' else
                            "QUANTITATIVE RISK MATRIX & OPERATIONAL FMEA")
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
        footer_left = ("Datalaria.com • Documento Confidencial para Comité de Dirección & Auditoría de Riesgos"
                       if lang == 'ES' else
                       "Datalaria.com • Confidential Executive Committee & Risk Audit Document")
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
            textColor=C_NAVY_MED, spaceAfter=2.5
        ),
        'Biblio': ParagraphStyle(
            'Biblio', parent=base['Normal'],
            fontName='Helvetica', fontSize=6.8, leading=8.8,
            textColor=C_NAVY_MED, leftIndent=10, firstLineIndent=-10, spaceAfter=1.8
        )
    }
    return styles


def build_guide_pdf(lang='ES', out_path=None):
    if out_path is None:
        base_dir = "packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE"
        sub_dir = "[ES]_Matriz_Riesgos_AMFE" if lang == 'ES' else "[EN]_FMEA_Risk_Matrix"
        fname = "Guia_Metodologica_AMFE_Riesgos_ES.pdf" if lang == 'ES' else "Methodology_Guide_FMEA_Risk_EN.pdf"
        out_path = os.path.join(base_dir, sub_dir, fname)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=45,
        bottomMargin=45
    )

    styles = get_custom_styles()
    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA & SECCIÓN 1 (LA FALACIA DE LA GESTIÓN CUALITATIVA)
    # =========================================================================
    kicker = ("DATALARIA EXECUTIVE DECISION PACK · ESTÁNDAR ISO 31000 / AIAG-VDA"
              if lang == 'ES' else
              "DATALARIA EXECUTIVE DECISION PACK · ISO 31000 / AIAG-VDA STANDARD")
    title = ("GUÍA METODOLÓGICA: MATRIZ DE RIESGOS CUANTITATIVA & AMFE OPERATIVO"
             if lang == 'ES' else
             "METHODOLOGY GUIDE: QUANTITATIVE RISK MATRIX & OPERATIONAL FMEA")
    subtitle = ("Cuantificación Tridimensional de Fallos (Severidad x Ocurrencia x Detección), Dinámica del NPR y Rentabilidad del Control (CER)"
                if lang == 'ES' else
                "Three-Dimensional Failure Quantification (Severity x Occurrence x Detection), RPN Dynamics & Control Cost-Effectiveness Ratio")

    story.append(Paragraph(kicker, styles['CoverKicker']))
    story.append(Paragraph(title, styles['CoverTitle']))
    story.append(Paragraph(subtitle, styles['CoverSub']))

    # Metadata Box
    meta_data_es = [
        [Paragraph("<b>Marco de Referencia:</b> ISO 31000:2018 / AIAG-VDA 1st Ed.", styles['TableCell']),
         Paragraph("<b>Perfil Directivo:</b> CEO, COO, CFO, CISO & Audit Committee", styles['TableCell'])],
        [Paragraph("<b>Versión del Modelo:</b> 2.0 (Dual Metric: 5x5 + FMEA)", styles['TableCell']),
         Paragraph("<b>Clasificación:</b> Confidencial · Gobernanza & Control Operativo", styles['TableCell'])]
    ]
    meta_data_en = [
        [Paragraph("<b>Core Framework:</b> ISO 31000:2018 / AIAG-VDA 1st Ed.", styles['TableCell']),
         Paragraph("<b>Executive Audience:</b> CEO, COO, CFO, CISO & Audit Committee", styles['TableCell'])],
        [Paragraph("<b>Engine Version:</b> 2.0 (Dual Metric: 5x5 + FMEA)", styles['TableCell']),
         Paragraph("<b>Classification:</b> Confidential · Corporate Governance & Ops", styles['TableCell'])]
    ]
    meta_table = Table(meta_data_es if lang == 'ES' else meta_data_en, colWidths=[255, 255])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Sección 1
    s1_title = ("1. La Falacia de la Gestión Cualitativa de Riesgos"
                if lang == 'ES' else
                "1. The Last-Mile Execution Fallacy: Qualitative Risk Pitfalls")
    story.append(Paragraph(s1_title, styles['SecHeading']))

    s1_text_es = [
        "En auditorías de riesgos, comités de dirección y reuniones de seguimiento de operaciones, la gestión de riesgos se aborda frecuentemente mediante matrices cualitativas de colores (rojo, amarillo, verde) construidas sobre percepciones subjetivas. En consultoría estratégica de operaciones, este fenómeno se conoce como <b>la falacia de la última milla cualitativa</b>.",
        "Cuando un riesgo crítico se clasifica simplemente como 'Alto' o 'Medio' sin anclaje numérico objetivo, se desencadenan cuatro patologías que destruyen el rigor directivo:",
        "<b>1. Compresión de Escalas e Ilusión de Equivalencia:</b> Asignar color rojo a un fallo que cuesta 50.000 € y al mismo tiempo a una brecha de ciberseguridad que cuesta 5.000.000 € desorienta al CFO e imposibilita priorizar racionalmente el presupuesto de CAPEX.",
        "<b>2. El Sesgo de Optimismo en la Detección:</b> Las matrices tradicionales 5x5 evalúan Probabilidad e Impacto, pero ignoran por completo la capacidad de detección. Un fallo de gravedad extrema que cuenta con telemetría automática instantánea requiere una respuesta radicalmente distinta de un fallo indetectable hasta la catástrofe.",
        "<b>3. La Trampa del Centrado Blando:</b> Ante la incertidumbre, los evaluadores tienden a calificar sistemáticamente en valores intermedios (3 sobre 5), generando una masa indiferenciada de eventos en 'zona amarilla' que paraliza la toma de decisiones.",
        "<b>4. La Falta de Justificación del Retorno de Inversión (ROI):</b> Los Comités de Auditoría y CFOs rechazan sistemáticamente partidas de mitigación cuando los gestores de operaciones no pueden demostrar el ratio de coste-eficacia actuarial (Cost-Effectiveness Ratio)."
    ]
    s1_text_en = [
        "In boardrooms, audit committees, and operational reviews, risk management is routinely conducted using subjective color-coded matrices (red, amber, green) built on qualitative gut feelings. In management consulting, this failure mode is termed <b>the last-mile qualitative fallacy</b>.",
        "When critical enterprise risks are labeled merely as 'High' or 'Medium' without rigorous mathematical scoring, four predictable pathologies undermine corporate governance:",
        "<b>1. Scale Compression & False Equivalence:</b> Labeling a €50,000 operational hiccup and a €5,000,000 regulatory data breach with the identical 'Red' badge blinds the CFO, making capital budgeting impossible.",
        "<b>2. Detection Optimism Blindspot:</b> Conventional 5x5 matrices evaluate Probability and Impact but completely omit Detection capability. A catastrophic event equipped with automated telemetry demands a completely different defense from an event undetectable until total failure.",
        "<b>3. Central Tendency Inertia:</b> Evaluators confronted with ambiguity instinctively rate events as 'Medium' (3 out of 5), creating a massive wall of amber risks that paralyzes executive decision-making.",
        "<b>4. Absence of Actuarial ROI Justification:</b> CFOs and Audit Committees reject mitigation proposals when operational leaders fail to demonstrate the formal Cost-Effectiveness Ratio (CER) of controls."
    ]
    for p in (s1_text_es if lang == 'ES' else s1_text_en):
        story.append(Paragraph(p, styles['Body']))

    # Callout Box Pág 1
    c1_es = "<b>Principio de Gobernanza Datalaria:</b> La gestión de riesgos de clase mundial (ISO 31000 / AIAG-VDA) exige sustituir adjetivos subjetivos por baremos objetivos 1-10 y cuantificación actuarial del valor esperado de la pérdida E(L)."
    c1_en = "<b>Datalaria Governance Principle:</b> World-class enterprise risk management (ISO 31000 / AIAG-VDA) requires replacing qualitative adjectives with audited 1-10 quantitative scales and actuarial expected loss calculations E(L)."
    callout1 = Table([[Paragraph(c1_es if lang == 'ES' else c1_en, styles['CalloutText'])]], colWidths=[510])
    callout1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_TEAL_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_TEAL_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout1)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: SECCIÓN 2 (FUNDAMENTACIÓN MATEMÁTICA Y DINÁMICA DEL RIESGO)
    # =========================================================================
    s2_title = ("2. Fundamentación Matemática y Dinámica Cuantitativa"
                if lang == 'ES' else
                "2. Mathematical Foundations & Quantitative Risk Dynamics")
    story.append(Paragraph(s2_title, styles['SecHeading']))

    s2_intro_es = "Para que la gestión de riesgos sea computable y defendible ante el Consejo de Administración, el modelo articula cuatro formulaciones matemáticas interconectadas:"
    s2_intro_en = "To ensure enterprise risk models are mathematically auditable and Board-defensible, the framework integrates four formal analytical formulations:"
    story.append(Paragraph(s2_intro_es if lang == 'ES' else s2_intro_en, styles['Body']))

    # 2.1 E(L)
    sub21 = ("2.1 Valor Esperado de la Pérdida Financiera (Expected Loss)"
             if lang == 'ES' else
             "2.1 Actuarial Expected Loss Model E(L)")
    story.append(Paragraph(sub21, styles['SubHeading']))
    m1_es = "E(L) = P × I × Exposición Monetaria Total (€)"
    m1_en = "E(L) = P × I × Total Monetary Asset Exposure (€)"
    m1_box = Table([[Paragraph(m1_es if lang == 'ES' else m1_en, styles['MathBox'])]], colWidths=[510])
    m1_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BLUE_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BLUE_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(m1_box)
    story.append(Spacer(1, 3))
    t21_es = "Donde <i>P</i> representa la probabilidad de ocurrencia anualizada (0 a 1) e <i>I</i> el porcentaje de degradación o destrucción patrimonial. Permite fijar con precisión el capital en riesgo antes y después de aplicar controles."
    t21_en = "Where <i>P</i> denotes the annualized probability (0 to 1) and <i>I</i> represents the percentage loss severity. This establishes the exact capital at risk pre- and post-control."
    story.append(Paragraph(t21_es if lang == 'ES' else t21_en, styles['Body']))

    # 2.2 NPR
    sub22 = ("2.2 Ecuación del Número de Prioridad de Riesgo (NPR / RPN)"
             if lang == 'ES' else
             "2.2 Risk Priority Number Equation (RPN)")
    story.append(Paragraph(sub22, styles['SubHeading']))
    m2_text = "NPR = S × O × D    (Escala Continua: 1 a 1.000)" if lang == 'ES' else "RPN = S × O × D    (Continuous Scale: 1 to 1,000)"
    m2_box = Table([[Paragraph(m2_text, styles['MathBox'])]], colWidths=[510])
    m2_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_RED_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_RED_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(m2_box)
    story.append(Spacer(1, 3))
    t22_es = "<b>Severidad (S):</b> Magnitud del impacto en seguridad, finanzas o continuidad de negocio (1-10).<br/><b>Ocurrencia (O):</b> Frecuencia estadística de aparición de la causa raíz (1-10).<br/><b>Detección (D):</b> Capacidad de los controles actuales de detectar el fallo antes de que alcance al cliente o afecte a la operativa (1-10, donde 10 es detección nula y 1 es detección inmediata)."
    t22_en = "<b>Severity (S):</b> Magnitude of impact on safety, financial assets, or business continuity (1-10).<br/><b>Occurrence (O):</b> Statistical frequency of the underlying root cause triggering (1-10).<br/><b>Detection (D):</b> Efficacy of current monitoring controls to intercept the defect before client impact (1-10, where 10 is zero detection and 1 is fail-safe automated detection)."
    story.append(Paragraph(t22_es if lang == 'ES' else t22_en, styles['Body']))

    # 2.3 AIAG-VDA
    sub23 = ("2.3 La Evolución AIAG-VDA: Prioridad de Acción (AP)"
             if lang == 'ES' else
             "2.3 The AIAG-VDA Evolution: Action Priority (AP)")
    story.append(Paragraph(sub23, styles['SubHeading']))
    t23_es = "El estándar unificado AIAG-VDA (2019) corrigió la principal limitación del NPR clásico: un fallo con S=9, O=2, D=3 tiene NPR=54 (aparentemente bajo), pero su severidad es catastrófica. La Prioridad de Acción categoriza de forma jerárquica: <b>Alta (AP High)</b> si S ≥ 9 independientemente del NPR, o si NPR ≥ 120; <b>Media (AP Med)</b> si 60 ≤ NPR < 120; y <b>Baja (AP Low)</b> si NPR < 60."
    t23_en = "The AIAG-VDA (2019) standard resolved the fundamental flaw of legacy RPN: an event with S=9, O=2, D=3 yields RPN=54 (seemingly harmless), yet its severity is catastrophic. Action Priority establishes hierarchical triage: <b>High (AP High)</b> if S ≥ 9 regardless of RPN, or if RPN ≥ 120; <b>Medium (AP Med)</b> if 60 ≤ RPN < 120; and <b>Low (AP Low)</b> if RPN < 60."
    story.append(Paragraph(t23_es if lang == 'ES' else t23_en, styles['Body']))

    # 2.4 CER
    sub24 = ("2.4 Modelo de Eficacia del Control (Cost-Effectiveness Ratio)"
             if lang == 'ES' else
             "2.4 Control Cost-Effectiveness Ratio (CER)")
    story.append(Paragraph(sub24, styles['SubHeading']))
    m3_text = "CER = ΔE(L) / Coste del Control = [ E(L)_pre - E(L)_post ] / [ CAPEX + OPEX ]" if lang == 'ES' else "CER = ΔE(L) / Control Cost = [ E(L)_pre - E(L)_post ] / [ CAPEX + OPEX ]"
    m3_box = Table([[Paragraph(m3_text, styles['MathBox'])]], colWidths=[510])
    m3_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_GREEN_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_GREEN_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(m3_box)
    story.append(Spacer(1, 3))
    t24_es = "Un CER > 1.0x certifica que la inversión en el control ahorra más de lo que cuesta. En nuestro modelo corporativo, el umbral mínimo de aprobación por el Comité de Inversiones es CER ≥ 2.5x."
    t24_en = "A CER > 1.0x proves that control investment yields greater savings than its cost. Under our corporate model, the mandatory threshold for Board CAPEX approval is CER ≥ 2.5x."
    story.append(Paragraph(t24_es if lang == 'ES' else t24_en, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: SECCIÓN 3 (BAREMOS DE CALIBRACIÓN OBJETIVA 1-10)
    # =========================================================================
    s3_title = ("3. Baremos de Calibración Objetiva 1-10 (AIAG-VDA)"
                if lang == 'ES' else
                "3. Objective Calibration Criteria 1-10 (AIAG-VDA)")
    story.append(Paragraph(s3_title, styles['SecHeading']))

    s3_desc_es = "Para erradicar la arbitrariedad, la asignación de puntuaciones de Severidad, Ocurrencia y Detección debe seguir estrictamente los baremos calibrados:"
    s3_desc_en = "To eliminate subjective scoring variance, ratings across Severity, Occurrence, and Detection must strictly adhere to calibrated operational benchmarks:"
    story.append(Paragraph(s3_desc_es if lang == 'ES' else s3_desc_en, styles['Body']))

    table_data_es = [
        [Paragraph("Punt.", styles['TableHeader']), Paragraph("Severidad (S) - Impacto", styles['TableHeader']), Paragraph("Ocurrencia (O) - Frecuencia", styles['TableHeader']), Paragraph("Detección (D) - Capacidad", styles['TableHeader'])],
        [Paragraph("<b>9 - 10</b>", styles['TableCellBold']), Paragraph("<b>Catastrófico:</b> Pérdida de vidas, quiebra, brecha de seguridad masiva o sanción regulatoria crítica sin aviso.", styles['TableCell']), Paragraph("<b>Muy Alta:</b> Fallo casi inevitable. Tasa de fallo > 10% (> 100 por 1.000 eventos). Frecuencia semanal.", styles['TableCell']), Paragraph("<b>Nula / Casi Imposible:</b> Cero controles. El fallo solo se detecta cuando el cliente lo reporta tras horas.", styles['TableCell'])],
        [Paragraph("<b>7 - 8</b>", styles['TableCellBold']), Paragraph("<b>Crítico:</b> Interrupción total de operaciones > 4 horas, daño reputacional severo en prensa o coste > 200.000 €.", styles['TableCell']), Paragraph("<b>Alta:</b> Fallos repetidos en procesos similares. Tasa entre 2% y 5% (20 a 50 por 1.000). Frecuencia mensual.", styles['TableCell']), Paragraph("<b>Baja:</b> Detección manual o auditoría retardada al final del día. Alta probabilidad de fuga al cliente.", styles['TableCell'])],
        [Paragraph("<b>5 - 6</b>", styles['TableCellBold']), Paragraph("<b>Moderado:</b> Degradación de servicio con quejas de clientes, parada operativa de 1 a 4 horas o coste entre 50k y 200k €.", styles['TableCell']), Paragraph("<b>Moderada:</b> Fallos ocasionales documentados. Tasa entre 0.5% y 1% (5 a 10 por 1.000). Ocurre trimestralmente.", styles['TableCell']), Paragraph("<b>Moderada:</b> Controles por muestreo o monitoreo asíncrono con alertas cada 15-30 minutos.", styles['TableCell'])],
        [Paragraph("<b>3 - 4</b>", styles['TableCellBold']), Paragraph("<b>Menor:</b> Molestia menor para usuarios, retrabajo operativo interno sin parada de servicio o coste < 50.000 €.", styles['TableCell']), Paragraph("<b>Baja:</b> Fallos aislados poco frecuentes. Tasa entre 0.05% y 0.1% (0.5 a 1 por 1.000). Anual.", styles['TableCell']), Paragraph("<b>Alta:</b> Telemetría en tiempo real con alertas automáticas inmediatas (PagerDuty / Datadog).", styles['TableCell'])],
        [Paragraph("<b>1 - 2</b>", styles['TableCellBold']), Paragraph("<b>Inapreciable:</b> Efecto nulo en la operativa del cliente. Variación estética o imperceptible.", styles['TableCell']), Paragraph("<b>Muy Baja / Remota:</b> Prácticamente imposible. Tasa < 0.01 por 1.000 eventos.", styles['TableCell']), Paragraph("<b>Casi Segura / Preventiva:</b> Fallback automático instantáneo (Poka-Yoke) que intercepta el fallo en < 1 segundo.", styles['TableCell'])],
    ]

    table_data_en = [
        [Paragraph("Score", styles['TableHeader']), Paragraph("Severity (S) - Impact", styles['TableHeader']), Paragraph("Occurrence (O) - Frequency", styles['TableHeader']), Paragraph("Detection (D) - Capability", styles['TableHeader'])],
        [Paragraph("<b>9 - 10</b>", styles['TableCellBold']), Paragraph("<b>Catastrophic:</b> Safety hazard, corporate insolvency, massive breach, or critical regulatory sanction without warning.", styles['TableCell']), Paragraph("<b>Very High:</b> Inevitable failure. Rate > 10% (> 100 per 1,000 events). Weekly recurrence cadence.", styles['TableCell']), Paragraph("<b>None / Almost Impossible:</b> Zero controls. Defect detected only when angry clients report after hours.", styles['TableCell'])],
        [Paragraph("<b>7 - 8</b>", styles['TableCellBold']), Paragraph("<b>Critical:</b> Total outage > 4 hours, severe press damage, or financial loss > €200,000.", styles['TableCell']), Paragraph("<b>High:</b> Repeated failure in similar pipelines. Rate 2% to 5% (20 to 50 per 1,000). Monthly frequency.", styles['TableCell']), Paragraph("<b>Low:</b> Manual inspection or batch end-of-day audit. High probability of escaping into production.", styles['TableCell'])],
        [Paragraph("<b>5 - 6</b>", styles['TableCellBold']), Paragraph("<b>Moderate:</b> Service degradation, customer churn complaints, 1-4 hour outage, or cost €50k-€200k.", styles['TableCell']), Paragraph("<b>Moderate:</b> Occasional documented defect. Rate 0.5% to 1% (5 to 10 per 1,000). Quarterly frequency.", styles['TableCell']), Paragraph("<b>Moderate:</b> Sample testing or asynchronous monitoring with 15-30 minute alert latencies.", styles['TableCell'])],
        [Paragraph("<b>3 - 4</b>", styles['TableCellBold']), Paragraph("<b>Minor:</b> Minor end-user inconvenience, internal rework without downtime, or cost < €50,000.", styles['TableCell']), Paragraph("<b>Low:</b> Rare isolated failures. Rate 0.05% to 0.1% (0.5 to 1 per 1,000). Annual recurrence.", styles['TableCell']), Paragraph("<b>High:</b> Real-time telemetry with automated instant alerting (PagerDuty / Datadog).", styles['TableCell'])],
        [Paragraph("<b>1 - 2</b>", styles['TableCellBold']), Paragraph("<b>Negligible:</b> Zero perceptible effect on client operations. Cosmetic or invisible variance.", styles['TableCell']), Paragraph("<b>Very Low / Remote:</b> Virtually impossible. Failure rate < 0.01 per 1,000 transactions.", styles['TableCell']), Paragraph("<b>Almost Certain / Fail-Safe:</b> Automated inline Poka-Yoke prevention intercepting failure in < 1 sec.", styles['TableCell'])],
    ]

    calib_table = Table(table_data_es if lang == 'ES' else table_data_en, colWidths=[38, 157, 157, 158])
    calib_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('BACKGROUND', (0,1), (0,-1), C_BG_CARD),
        ('ROWBACKGROUNDS', (1,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(calib_table)
    story.append(Spacer(1, 7))

    rule_box_es = "<b>Regla de Oro AIAG-VDA:</b> Para reducir el NPR de un proceso, la ingeniería no puede alterar la Severidad intrínseca (S) salvo rediseñando el sistema por completo. La intervención de controles eficaces se focaliza en <b>reducir la Ocurrencia (O) mediante prevención</b> y <b>reducir la Detección (D) mediante telemetría automática</b>."
    rule_box_en = "<b>AIAG-VDA Golden Rule:</b> To slash process RPN, engineering cannot modify inherent Severity (S) without a fundamental architectural redesign. High-ROI mitigation focuses on <b>reducing Occurrence (O) via preventive controls</b> and <b>reducing Detection (D) via real-time telemetry</b>."
    callout_rule = Table([[Paragraph(rule_box_es if lang == 'ES' else rule_box_en, styles['CalloutText'])]], colWidths=[510])
    callout_rule.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_AMBER_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_AMBER_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_rule)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: SECCIÓN 4 (CASO DE ESTUDIO REALISTA)
    # =========================================================================
    s4_title = ("4. Caso de Estudio Realista: Resiliencia en Pasarela Cloud"
                if lang == 'ES' else
                "4. Real-World Case Study: Cloud Transactional Resiliency")
    story.append(Paragraph(s4_title, styles['SecHeading']))

    c_intro_es = "<b>Compañía:</b> Nexus Global Payments (Plataforma Fintech transaccional con 45 M€ de volumen procesado mensual).<br/><b>Contexto Operativo:</b> Caída del 18% en tasas de conversión durante campañas de alta demanda (Black Friday / Cyber Monday) debido a timeouts de red con el adquirente bancario principal y saturación de proxies inversos."
    c_intro_en = "<b>Enterprise:</b> Nexus Global Payments (High-throughput Fintech platform processing €45M monthly volume).<br/><b>Operational Context:</b> An 18% conversion rate collapse during peak shopping events (Black Friday / Cyber Monday) caused by upstream network timeouts with the primary acquiring bank and reverse-proxy saturation."
    story.append(Paragraph(c_intro_es if lang == 'ES' else c_intro_en, styles['Body']))
    story.append(Spacer(1, 4))

    # Tabla Antes vs Después
    cs_table_data_es = [
        [Paragraph("Métrica de Riesgo", styles['TableHeader']), Paragraph("Situación Pre-Control (Inherente)", styles['TableHeader']), Paragraph("Situación Post-Control (Residual)", styles['TableHeader']), Paragraph("Impacto Directo", styles['TableHeader'])],
        [Paragraph("<b>Severidad (S)</b>", styles['TableCellBold']), Paragraph("<b>8 / 10</b> (Parada de checkout)", styles['TableCell']), Paragraph("<b>8 / 10</b> (Severidad intrínseca)", styles['TableCell']), Paragraph("Invariable (impacto de negocio idéntico)", styles['TableCell'])],
        [Paragraph("<b>Ocurrencia (O)</b>", styles['TableCellBold']), Paragraph("<b>6 / 10</b> (Incidencia quincenal)", styles['TableCell']), Paragraph("<b>2 / 10</b> (Remota: dual-routing)", styles['TableCell']), Paragraph("Reducción del 67% en fallos", styles['TableCell'])],
        [Paragraph("<b>Detección (D)</b>", styles['TableCellBold']), Paragraph("<b>7 / 10</b> (Detección por tickets de usuarios)", styles['TableCell']), Paragraph("<b>2 / 10</b> (Fallback automático < 1s)", styles['TableCell']), Paragraph("Detección e intercepción en tiempo real", styles['TableCell'])],
        [Paragraph("<b>NPR / RPN</b>", styles['TableCellBold']), Paragraph("<b>336 NPR</b> (Prioridad Acción: ALTA)", styles['TableCell']), Paragraph("<b>32 NPR</b> (Prioridad Acción: BAJA)", styles['TableCell']), Paragraph("<b>-90,5% de Riesgo Residual</b>", styles['TableCellBold'])],
        [Paragraph("<b>Pérdida Esperada E(L)</b>", styles['TableCellBold']), Paragraph("190.000 € / año", styles['TableCell']), Paragraph("25.000 € / año", styles['TableCell']), Paragraph("<b>165.000 € anuales evitados</b>", styles['TableCellBold'])],
        [Paragraph("<b>Coste de Mitigación</b>", styles['TableCellBold']), Paragraph("0 € (Inacción operativa)", styles['TableCell']), Paragraph("28.000 € (Smart-routing multiaquirente)", styles['TableCell']), Paragraph("<b>ROI del Control (CER): 5,89x</b>", styles['TableCellBold'])],
    ]

    cs_table_data_en = [
        [Paragraph("Risk Metric", styles['TableHeader']), Paragraph("Pre-Control Baseline (Inherent)", styles['TableHeader']), Paragraph("Post-Control State (Residual)", styles['TableHeader']), Paragraph("Operational Impact", styles['TableHeader'])],
        [Paragraph("<b>Severity (S)</b>", styles['TableCellBold']), Paragraph("<b>8 / 10</b> (Checkout outage)", styles['TableCell']), Paragraph("<b>8 / 10</b> (Intrinsic impact)", styles['TableCell']), Paragraph("Invariable (identical business impact)", styles['TableCell'])],
        [Paragraph("<b>Occurrence (O)</b>", styles['TableCellBold']), Paragraph("<b>6 / 10</b> (Bi-weekly incident)", styles['TableCell']), Paragraph("<b>2 / 10</b> (Remote: dual-routing)", styles['TableCell']), Paragraph("67% reduction in root cause events", styles['TableCell'])],
        [Paragraph("<b>Detection (D)</b>", styles['TableCellBold']), Paragraph("<b>7 / 10</b> (User tickets detection)", styles['TableCell']), Paragraph("<b>2 / 10</b> (Automated failover < 1s)", styles['TableCell']), Paragraph("Real-time telemetry interception", styles['TableCell'])],
        [Paragraph("<b>RPN Score</b>", styles['TableCellBold']), Paragraph("<b>336 RPN</b> (Action Priority: HIGH)", styles['TableCell']), Paragraph("<b>32 RPN</b> (Action Priority: LOW)", styles['TableCell']), Paragraph("<b>-90.5% Residual Risk Drop</b>", styles['TableCellBold'])],
        [Paragraph("<b>Expected Loss E(L)</b>", styles['TableCellBold']), Paragraph("€190,000 / year", styles['TableCell']), Paragraph("€25,000 / year", styles['TableCell']), Paragraph("<b>€165,000 annualized savings</b>", styles['TableCellBold'])],
        [Paragraph("<b>Mitigation Cost</b>", styles['TableCellBold']), Paragraph("€0 (Cost of inaction)", styles['TableCell']), Paragraph("€28,000 (Multi-acquirer smart-routing)", styles['TableCell']), Paragraph("<b>Control ROI (CER): 5.89x</b>", styles['TableCellBold'])],
    ]

    cs_table = Table(cs_table_data_es if lang == 'ES' else cs_table_data_en, colWidths=[95, 138, 142, 135])
    cs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (1,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(cs_table)
    story.append(Spacer(1, 6))

    cs_concl_es = "<b>Resolución del Comité:</b> La dirección técnica defendió la inversión ante el CFO y el CEO demostrando que cada euro invertido en smart-routing protegía 5,89 € de ingresos netos. El riesgo residual resultante (NPR=32) cumplió holgadamente el umbral corporativo (NPR < 80)."
    cs_concl_en = "<b>Board Resolution:</b> Engineering leadership successfully defended the CAPEX allocation before the CFO and CEO by proving that every euro invested in smart routing secured €5.89 in net revenue. The resulting residual risk (RPN=32) comfortably met corporate risk appetite (RPN < 80)."
    story.append(Paragraph(cs_concl_es if lang == 'ES' else cs_concl_en, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: SECCIÓN 5 (BOARDROOM FAQ) & BIBLIOGRAFÍA
    # =========================================================================
    s5_title = ("5. Protocolo de Defensa en Comité (Boardroom FAQ)"
                if lang == 'ES' else
                "5. Boardroom Defense Protocol (C-Level FAQ)")
    story.append(Paragraph(s5_title, styles['SecHeading']))

    faqs_es = [
        ("P1: ¿Por qué debemos invertir presupuesto en mitigar un riesgo que puede no materializarse nunca?",
         "<b>Respuesta Directiva:</b> La no materialización pasada es una ilusión de seguridad estadística, no una garantía. El modelo calcula el Valor Esperado de la Pérdida E(L). Invertir 28.000 € en un control que previene una pérdida probabilística de 190.000 € es equivalente a adquirir una póliza con retorno garantizado. El coste de la inacción suele multiplicar por 7 el coste de la prevención."),
        ("P2: ¿Cómo calibramos objetivamente la Detección (D) si nuestro sistema actual carece de telemetría?",
         "<b>Respuesta Directiva:</b> Bajo el principio de prudencia contable e ISO 31000, la ausencia de telemetría documentada exige calificar la Detección automáticamente en D ≥ 8 ('Detección reactiva por clientes'). Esta penalización eleva el NPR e impone al equipo de ingeniería la urgencia de instalar observabilidad en tiempo real."),
        ("P3: ¿Cómo debe fijar el Consejo de Administración el umbral de corte de NPR?",
         "<b>Respuesta Directiva:</b> El Consejo nunca debe fijar un umbral arbitrario único. Recomendamos la regla dual AIAG-VDA: tolerancia cero (veto absoluto) para cualquier fallo con Severidad S ≥ 9 o NPR ≥ 120 (Prioridad Alta); y aprobación condicionada a plan de contingencia para eventos en Prioridad Media (60 a 119).")
    ]

    faqs_en = [
        ("Q1: Why authorize capital expenditure to mitigate an operational risk that might never occur?",
         "<b>Executive Defense:</b> Past absence of failure is statistical luck, not operational competence. The framework computes actuarial Expected Loss E(L). Allocating €28,000 to prevent an annualized probabilistic loss of €190,000 delivers an actuarial ROI of 5.89x. Inaction costs on average 7 times more than proactive prevention."),
        ("Q2: How do we objectively calibrate Detection (D) when infrastructure lacks real-time telemetry?",
         "<b>Executive Defense:</b> Under ISO 31000 prudence principles, missing telemetry mandates an immediate default rating of D ≥ 8 ('Reactive customer-reported detection'). This penalty inflates RPN, compelling engineering to prioritize automated observability."),
        ("Q3: How should the Board establish the official corporate RPN cutoff threshold?",
         "<b>Executive Defense:</b> The Board should never rely on an arbitrary single cutoff. We recommend the dual AIAG-VDA governance gate: zero tolerance (automatic veto) for any process exhibiting Severity S ≥ 9 or RPN ≥ 120 (High Priority); with mandatory mitigation roadmaps for Medium Priority events (60 to 119).")
    ]

    for q, a in (faqs_es if lang == 'ES' else faqs_en):
        story.append(Paragraph(q, styles['FAQ_Q']))
        story.append(Paragraph(a, styles['FAQ_A']))

    story.append(Spacer(1, 4))

    # Bibliografía
    s_bib = "Referencias Canónicas de Autoridad" if lang == 'ES' else "Canonical Authority References"
    story.append(Paragraph(s_bib, styles['SecHeading']))

    bib_items_es = [
        "1. <b>International Organization for Standardization (2018).</b> <i>ISO 31000:2018 - Risk management: Guidelines</i>. Geneva: ISO.",
        "2. <b>AIAG & VDA (2019).</b> <i>Failure Mode and Effects Analysis (FMEA Handbook) – 1st Edition</i>. Southfield: AIAG.",
        "3. <b>Kaplan, R. S. & Mikes, A. (2012).</b> <i>Managing Risks: A New Framework</i>. Harvard Business Review, 90(6), 48-60.",
        "4. <b>Hubbard, D. W. (2020).</b> <i>The Failure of Risk Management: Why It's Broken and How to Fix It</i>. Hoboken: John Wiley & Sons.",
        "5. <b>Project Management Institute (2021).</b> <i>A Guide to the PMBOK Guide – 7th Edition: Risk Management Domain</i>. Newtown Square: PMI.",
        "6. <b>Minto, Barbara (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. London: Financial Times Prentice Hall."
    ]

    bib_items_en = [
        "1. <b>International Organization for Standardization (2018).</b> <i>ISO 31000:2018 - Risk management: Guidelines</i>. Geneva: ISO.",
        "2. <b>AIAG & VDA (2019).</b> <i>Failure Mode and Effects Analysis (FMEA Handbook) – 1st Edition</i>. Southfield: AIAG.",
        "3. <b>Kaplan, R. S. & Mikes, A. (2012).</b> <i>Managing Risks: A New Framework</i>. Harvard Business Review, 90(6), 48-60.",
        "4. <b>Hubbard, D. W. (2020).</b> <i>The Failure of Risk Management: Why It's Broken and How to Fix It</i>. Hoboken: John Wiley & Sons.",
        "5. <b>Project Management Institute (2021).</b> <i>A Guide to the PMBOK Guide – 7th Edition: Risk Management Domain</i>. Newtown Square: PMI.",
        "6. <b>Minto, Barbara (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. London: Financial Times Prentice Hall."
    ]

    for b in (bib_items_es if lang == 'ES' else bib_items_en):
        story.append(Paragraph(b, styles['Biblio']))

    # Construir PDF
    def canvas_maker(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c._lang = lang
        return c

    doc.build(story, canvasmaker=canvas_maker)
    print(f"  -> Guía PDF generada: {out_path}")


def main():
    print("[1/2] Generando Guía Metodológica PDF en Español...")
    build_guide_pdf(lang='ES')

    print("[2/2] Generando Guía Metodológica PDF en Inglés...")
    build_guide_pdf(lang='EN')

    print("\n✓ Generación de guías metodológicas PDF completada con éxito.")


if __name__ == "__main__":
    main()
