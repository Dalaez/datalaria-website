#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para el Executive Decision Pack EVM:
1. packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/[ES]_Cuadro_EVM_Valor_Ganado/Guia_Metodologica_EVM_ES.pdf
2. packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/[EN]_Earned_Value_Management_EVM/Methodology_Guide_EVM_EN.pdf

Estándar editorial de alta dirección (ANSI/EIA-748 / PMBOK / McKinsey Minto Pyramid):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (La Falacia de la Contabilidad Tradicional en Proyectos).
- Página 2: Sección 2 (Fundamentación Matemática: PV, EV, AC, Varianzas, CPI, SPI, EAC1/2/3, VAC, TCPI).
- Página 3: Sección 3 (Reglas Operativas para Imputar el Avance Físico: 0/100, 50/50, Hitos Ponderados).
- Página 4: Sección 4 (Caso de Estudio Realista: Megaproyecto Tecnológico de 1.2M €, Rescate en Mes 6).
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
C_CYAN_ACCENT = colors.HexColor("#0284C7")  # Sky 600
C_PURPLE_ACCENT = colors.HexColor("#7C3AED")# Purple 600

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
            header_right = ("CUADRO DE MANDO EVM: VALOR GANADO, CURVA S & EAC"
                            if lang == 'ES' else
                            "EARNED VALUE MANAGEMENT (EVM) DASHBOARD & FORECASTING")
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
        footer_left = ("Datalaria.com • Documento Confidencial para Comité de Dirección & Project Governance"
                       if lang == 'ES' else
                       "Datalaria.com • Confidential Executive Committee & Project Governance Document")
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
            textColor=C_NAVY_DARK, spaceBefore=3.0, spaceAfter=1.2,
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
        base_dir = "packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado"
        sub_dir = "[ES]_Cuadro_EVM_Valor_Ganado" if lang == 'ES' else "[EN]_Earned_Value_Management_EVM"
        fname = "Guia_Metodologica_EVM_ES.pdf" if lang == 'ES' else "Methodology_Guide_EVM_EN.pdf"
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
    # PÁGINA 1: PORTADA & SECCIÓN 1 (LA FALACIA CONTABLE TRADICIONAL)
    # =========================================================================
    kicker_txt = "DATALARIA EXECUTIVE DECISION PACK · ANSI/EIA-748 & PMBOK STANDARD" if lang == 'ES' else "DATALARIA EXECUTIVE DECISION PACK · ANSI/EIA-748 & PMBOK STANDARD"
    story.append(Paragraph(kicker_txt, styles['CoverKicker']))

    title_txt = "Cuadro de Mando EVM: Valor Ganado, Curva S & Proyecciones EAC" if lang == 'ES' else "Earned Value Management (EVM) Dashboard: S-Curve & EAC Forecasting"
    story.append(Paragraph(title_txt, styles['CoverTitle']))

    sub_txt = (
        "Superando la trampa de la contabilidad tradicional en proyectos: fundamentación matemática rigurosa, "
        "diagnóstico de varianzas (CV, SV), índices de eficiencia (CPI, SPI), curvas S directivas y modelos predictivos a la conclusión (EAC, VAC, TCPI)."
        if lang == 'ES' else
        "Overcoming traditional project accounting traps with mathematical rigor: Earned Value analytics, "
        "variance diagnostics (CV, SV), efficiency indices (CPI, SPI), executive S-Curves, and completion forecasting (EAC, VAC, TCPI)."
    )
    story.append(Paragraph(sub_txt, styles['CoverSub']))

    # Metadata Card
    meta_data = [
        [
            Paragraph("<b>Área:</b> Control Operativo & PMO" if lang == 'ES' else "<b>Domain:</b> Operations & PMO Governance", styles['TableCell']),
            Paragraph("<b>Estándar:</b> ANSI/EIA-748 / PMBOK" if lang == 'ES' else "<b>Standard:</b> ANSI/EIA-748 / PMBOK", styles['TableCell']),
            Paragraph("<b>Nivel:</b> C-Level / Boardroom" if lang == 'ES' else "<b>Audience:</b> C-Level / Boardroom", styles['TableCell']),
            Paragraph("<b>Versión:</b> 2026.1 Oficial" if lang == 'ES' else "<b>Version:</b> 2026.1 Official", styles['TableCell'])
        ]
    ]
    t_meta = Table(meta_data, colWidths=[127, 128, 128, 128])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Sección 1
    sec1_title = "1. La Falacia de la Contabilidad Tradicional en Proyectos" if lang == 'ES' else "1. The Fallacy of Traditional Project Accounting"
    story.append(Paragraph(sec1_title, styles['SecHeading']))

    p1_1 = (
        "En consejos de administración, comités de inversión y reuniones directivas, directores generales (CEOs), directores financieros (CFOs) y directores de operaciones (COOs) "
        "enfrentan de forma recurrente una patología endémica: <b>la trampa de medir proyectos únicamente contrastando 'gasto real incurrido' frente a 'presupuesto planificado'</b>. "
        "Bajo la contabilidad financiera clásica, si un proyecto estratégico de 1.200.000 € lleva transcurrido el 50% de su plazo (6 meses) y ha consumido 600.000 € (el 50% de su presupuesto), "
        "los informes financieros estándar reportan solemnemente que el proyecto 'marcha dentro del presupuesto y en orden'."
        if lang == 'ES' else
        "In boardrooms, steering committees, and executive councils, CEOs, CFOs, and COOs routinely confront a dangerous corporate pathology: "
        "<b>the trap of tracking capital initiatives solely by comparing 'actual expenditure' against 'planned budget'</b>. "
        "Under traditional accounting, if a strategic $1,200,000 project has elapsed 50% of its scheduled timeframe (6 months) and disbursed $600,000 (50% of its total budget), "
        "standard financial reports declare that the project is 'on budget and fully on track'."
    )
    story.append(Paragraph(p1_1, styles['Body']))

    p1_2 = (
        "Esta lectura tradicional es una peligrosa ilusión estadística. La contabilidad tradicional adolece de un punto ciego fatal: <b>ignora por completo cuánto valor físico real se ha producido a cambio de esos 600.000 €</b>. "
        "Se generan así tres trampas operacionales que desembocan en sorpresas catastróficas en las fases finales del proyecto (Fleming & Koppelman, 2010; Kerzner, 2017):"
        if lang == 'ES' else
        "This traditional interpretation is a perilous statistical illusion. Conventional bookkeeping suffers from a fatal blind spot: <b>it completely ignores how much physical scope has actually been delivered in return for that $600,000</b>. "
        "This creates three structural traps that culminate in late-stage catastrophic surprises (Fleming & Koppelman, 2010; Kerzner, 2017):"
    )
    story.append(Paragraph(p1_2, styles['Body']))

    b1_items_es = [
        "<b>La Trampa del Gasto Ciego:</b> Si se han gastado 600.000 € pero el equipo solo ha completado el 43% del alcance físico (valorado en 516.000 €), el proyecto no está 'en presupuesto': arrastra un sobrecoste oculto de 84.000 € y 3 semanas de retraso funcional acumulado.",
        "<b>La Destrucción Tardía de Reservas:</b> Como la contabilidad lineal no detecta la ineficiencia a mitad de plazo, las reservas de contingencia se consumen silenciosamente. El desvío solo estalla en el mes 10 u 11, cuando el presupuesto se agota pero el trabajo físico está inconcluso.",
        "<b>La Pérdida de la Ventana de Intervención:</b> Cuando un proyecto llega al 80% del tiempo con sobrecostes ocultos, el coste de recuperación es exponencial. El estándar EVM permite detectar la pérdida de rendimiento en el primer 15-20% de ejecución, cuando las medidas correctivas son baratas y eficaces."
    ]
    b1_items_en = [
        "<b>The Blind Spending Trap:</b> If $600,000 has been disbursed but engineering squads have only completed 43% of physical deliverables ($516,000 in earned value), the project is not 'on budget': it harbors a hidden $84,000 cost overrun and a 3-week schedule delay.",
        "<b>Late-Stage Reserve Exhaustion:</b> Because linear accounting masks mid-project inefficiencies, management reserves are quietly consumed. The crisis only surfaces at Month 10 or 11, when cash is exhausted while delivered scope remains incomplete.",
        "<b>Loss of Executive Intervention Window:</b> Once an initiative reaches 80% elapsed schedule with hidden variances, recovery costs become exponential. EVM detects efficiency loss within the first 15-20% of project execution, when corrective action is inexpensive and highly viable."
    ]
    b1_items = b1_items_es if lang == 'ES' else b1_items_en
    for bi in b1_items:
        story.append(Paragraph(f"• {bi}", styles['Bullet']))

    story.append(Spacer(1, 4))
    callout_p1 = [
        [Paragraph(
            "<b>Axioma de Gobernanza C-Level:</b> La contabilidad financiera tradicional mide lo que el proyecto ha costado; el Valor Ganado (EVM) mide lo que el proyecto vale físicamente en el mercado. Tomar decisiones de inversión sin Valor Ganado es gestionar un avión volando a ciegas con el indicador de combustible como único instrumento."
            if lang == 'ES' else
            "<b>C-Level Governance Axiom:</b> Traditional financial accounting measures what an initiative has cost; Earned Value Management (EVM) measures what the project is physically worth. Steering strategic capital projects without EVM is flying an aircraft blind using only the fuel gauge.",
            styles['CalloutText']
        )]
    ]
    t_c1 = Table(callout_p1, colWidths=[511])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BLUE_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BLUE_ACCENT),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_c1)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: FUNDAMENTACIÓN MATEMÁTICA DEL ESTÁNDAR EVM
    # =========================================================================
    sec2_title = "2. Fundamentación Matemática del Estándar EVM (ANSI/EIA-748)" if lang == 'ES' else "2. Mathematical Foundations of the EVM Standard (ANSI/EIA-748)"
    story.append(Paragraph(sec2_title, styles['SecHeading']))

    p2_intro = (
        "El estándar **ANSI/EIA-748-D** y la guía **PMBOK** formalizan el modelo Earned Value Management a través de tres variables canónicas fundamentales y un sistema de ecuaciones algebraicas auditables:"
        if lang == 'ES' else
        "The **ANSI/EIA-748-D** standard and the **PMBOK** guide formalize Earned Value Management through three canonical baseline variables and an auditable algebraic equation system:"
    )
    story.append(Paragraph(p2_intro, styles['Body']))

    # Tabla de las 3 variables canónicas
    t3_head = ["VARIABLE CANÓNICA" if lang == 'ES' else "CANONICAL VARIABLE", "SÍMBOLO" if lang == 'ES' else "SYMBOL", "DEFINICIÓN OPERACIONAL RIGUROSA" if lang == 'ES' else "OPERATIONAL DEFINITION"]
    t3_rows = [
        [
            Paragraph("<b>Valor Planificado</b><br/>(Planned Value)", styles['TableCell']),
            Paragraph("<b>PV</b>", styles['TableCellBold']),
            Paragraph("Presupuesto autorizado asignado al trabajo programado para ejecutarse hasta la fecha de corte ($PV = BAC \\times \\% \\text{Plan}$).", styles['TableCell']) if lang == 'ES' else
            Paragraph("Authorized baseline budget assigned to scheduled work up to the cutoff date ($PV = BAC \\times \\% \\text{Plan}$).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Valor Ganado</b><br/>(Earned Value)", styles['TableCell']),
            Paragraph("<b>EV</b>", styles['TableCellBold']),
            Paragraph("Presupuesto autorizado del trabajo físico efectivamente completado ($EV = BAC \\times \\% \\text{Avance Real Físico}$).", styles['TableCell']) if lang == 'ES' else
            Paragraph("Authorized budget for work physically completed at cutoff ($EV = BAC \\times \\% \\text{Actual Physical Progress}$).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Coste Real Incurrido</b><br/>(Actual Cost)", styles['TableCell']),
            Paragraph("<b>AC</b>", styles['TableCellBold']),
            Paragraph("Coste total real registrado por contabilidad en la realización del trabajo ($AC = \\text{Facturas} + \\text{Nóminas} + \\text{CAPEX}$).", styles['TableCell']) if lang == 'ES' else
            Paragraph("Total direct and indirect expenditures incurred in executing work ($AC = \\text{Invoices} + \\text{Labor} + \\text{CAPEX}$).", styles['TableCell'])
        ],
    ]
    t3_tab = Table([[Paragraph(h, styles['TableHeader']) for h in t3_head]] + t3_rows, colWidths=[120, 55, 336])
    t3_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t3_tab)
    story.append(Spacer(1, 5))

    # Subsección Ecuaciones de Varianzas e Índices
    sub2_1 = "2.1 Ecuaciones de Varianzas e Índices de Rendimiento" if lang == 'ES' else "2.1 Variance Equations & Performance Indices"
    story.append(Paragraph(sub2_1, styles['SubHeading']))

    eq_head = ["MÉTRICA DIRECTIVA" if lang == 'ES' else "EXECUTIVE METRIC", "ECUACIÓN" if lang == 'ES' else "EQUATION", "INTERPRETACIÓN & UMBRALES DE GOBERNANZA" if lang == 'ES' else "GOVERNANCE INTERPRETATION & CUTOFFS"]
    eq_rows = [
        [
            Paragraph("<b>Varianza de Coste (CV)</b>", styles['TableCell']),
            Paragraph("<b>CV = EV - AC</b>", styles['TableCellBold']),
            Paragraph("Positivo = Superávit financiero; Negativo = Sobrecoste respecto al avance real logrado.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Positive = Budget surplus; Negative = Financial overrun relative to earned work.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Varianza de Cronograma (SV)</b>", styles['TableCell']),
            Paragraph("<b>SV = EV - PV</b>", styles['TableCellBold']),
            Paragraph("Positivo = Adelantado; Negativo = Retraso temporal expresado en valor monetario de entregables.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Positive = Ahead of schedule; Negative = Project delay expressed in delivered currency.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Índice Rendimiento Coste (CPI)</b>", styles['TableCell']),
            Paragraph("<b>CPI = EV / AC</b>", styles['TableCellBold']),
            Paragraph("<b>CPI ≥ 1.0:</b> Eficiente (genera valor superior al gasto). <b>CPI < 1.0:</b> Pérdida de capital (0.86 = 0.86€ ganados por cada 1€ gastado).", styles['TableCell']) if lang == 'ES' else
            Paragraph("<b>CPI ≥ 1.0:</b> Efficient. <b>CPI < 1.0:</b> Capital destruction ($0.86 means $0.86 earned per $1.00 spent).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Índice Rendimiento Plazo (SPI)</b>", styles['TableCell']),
            Paragraph("<b>SPI = EV / PV</b>", styles['TableCellBold']),
            Paragraph("<b>SPI ≥ 1.0:</b> Velocidad igual o superior al plan. <b>SPI < 1.0:</b> Retraso funcional acumulado.", styles['TableCell']) if lang == 'ES' else
            Paragraph("<b>SPI ≥ 1.0:</b> Progress matching or exceeding plan. <b>SPI < 1.0:</b> Schedule deficit.", styles['TableCell'])
        ],
    ]
    eq_tab = Table([[Paragraph(h, styles['TableHeader']) for h in eq_head]] + eq_rows, colWidths=[130, 95, 286])
    eq_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(eq_tab)
    story.append(Spacer(1, 5))

    # Subsección Modelos Predictivos a la Conclusión (EAC, VAC, TCPI)
    sub2_2 = "2.2 Modelos Estadísticos de Proyección a la Finalización (EAC, VAC & TCPI)" if lang == 'ES' else "2.2 Statistical Forecasting Models (EAC, VAC & TCPI)"
    story.append(Paragraph(sub2_2, styles['SubHeading']))

    eac_head = ["MODELO PREDICTIVO" if lang == 'ES' else "FORECASTING MODEL", "FÓRMULA CANÓNICA" if lang == 'ES' else "CANONICAL FORMULA", "HIPÓTESIS DE NEGOCIO SUBYACENTE" if lang == 'ES' else "UNDERLYING BUSINESS ASSUMPTION"]
    eac_rows = [
        [
            Paragraph("<b>EAC 1: Escenario Típico</b>", styles['TableCell']),
            Paragraph("<b>EAC₁ = BAC / CPI</b>", styles['TableCellBold']),
            Paragraph("Asume que la eficiencia de coste actual se mantendrá hasta el cierre del proyecto (modelo estándar PMBOK).", styles['TableCell']) if lang == 'ES' else
            Paragraph("Assumes current cost efficiency rate will persist across remaining deliverables (PMBOK default).", styles['TableCell'])
        ],
        [
            Paragraph("<b>EAC 2: Escenario Atípico</b>", styles['TableCell']),
            Paragraph("<b>EAC₂ = AC + (BAC - EV)</b>", styles['TableCellBold']),
            Paragraph("Asume que las desviaciones pasadas fueron anomalías aisladas y que el trabajo remanente se ejecutará a presupuesto.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Assumes past variances were one-off shocks and remaining work executes strictly at budget rate.", styles['TableCell'])
        ],
        [
            Paragraph("<b>EAC 3: Compuesto (Coste+Plazo)</b>", styles['TableCell']),
            Paragraph("<b>EAC₃ = AC + (BAC-EV)/(CPI·SPI)</b>", styles['TableCellBold']),
            Paragraph("Escenario de estrés: el retraso cronológico penaliza gravemente los costes futuros (penalizaciones, fijos).", styles['TableCell']) if lang == 'ES' else
            Paragraph("Stress test: schedule delays heavily inflate remaining delivery costs (carrying overhead, penalties).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Varianza al Cierre (VAC)</b>", styles['TableCell']),
            Paragraph("<b>VAC = BAC - EAC</b>", styles['TableCellBold']),
            Paragraph("Déficit presupuestario final proyectado. Si es negativo, indica la inyección de reservas requerida.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Projected bottom-line variance. Negative values indicate additional funding required from reserves.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Índice para Completar (TCPI)</b>", styles['TableCell']),
            Paragraph("<b>TCPI = (BAC-EV) / (BAC-AC)</b>", styles['TableCellBold']),
            Paragraph("Eficiencia exigida para terminar en presupuesto. <b>Si TCPI > 1.10x</b>, el PMBOK lo califica de inalcanzable sin inyectar capital.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Required efficiency on remaining scope to meet budget. <b>If TCPI > 1.10x</b>, PMBOK marks it statistically unachievable.", styles['TableCell'])
        ],
    ]
    eac_tab = Table([[Paragraph(h, styles['TableHeader']) for h in eac_head]] + eac_rows, colWidths=[120, 125, 266])
    eac_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(eac_tab)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: REGLAS OPERATIVAS DE IMPUTACIÓN DEL AVANCE FÍSICO (EV)
    # =========================================================================
    sec3_title = "3. Reglas Operativas para Imputar el Avance Físico (EV)" if lang == 'ES' else "3. Operational Rules for Crediting Physical Earned Value (EV)"
    story.append(Paragraph(sec3_title, styles['SecHeading']))

    p3_1 = (
        "El talón de Aquiles de cualquier sistema EVM radica en la **subjetividad del porcentaje de avance declarado**. "
        "En proyectos de desarrollo tecnológico y consultoría, los líderes de equipo suelen incurrir en la patología psicológica conocida como **el síndrome del 90% completado infinito**: "
        "una tarea avanza rápidamente del 0% al 90% en pocas semanas, pero permanece atrapada en ese 90% durante meses debido a defectos descubiertos, pruebas inconclusas o falta de definición en los criterios de aceptación."
        if lang == 'ES' else
        "The Achilles' heel of any EVM framework is the **subjectivity of reported percent complete**. "
        "In software engineering and complex integration, team leaders routinely succumb to the behavioral pathology known as the **infinite 90% completion syndrome**: "
        "a work package rapidly progresses from 0% to 90% within weeks, only to remain stalled at 90% for months due to unexpected defect resolution, regression failures, or vague acceptance criteria."
    )
    story.append(Paragraph(p3_1, styles['Body']))

    p3_2 = (
        "Para blindar la integridad del modelo ante auditorías de comité, el estándar **ANSI/EIA-748** establece cuatro reglas estrictas y objetivas para imputar el Valor Ganado ($EV$):"
        if lang == 'ES' else
        "To safeguard mathematical integrity against board audits, the **ANSI/EIA-748** standard specifies four rigorous, objective crediting techniques:"
    )
    story.append(Paragraph(p3_2, styles['Body']))

    rules_head = ["MÉTODO DE IMPUTACIÓN" if lang == 'ES' else "CREDITING METHOD", "REGLA DE CÁLCULO" if lang == 'ES' else "CREDITING LOGIC", "CASO DE APLICACIÓN RECOMENDADO" if lang == 'ES' else "APPLICABILITY & GOVERNANCE USE CASE"]
    rules_rows = [
        [
            Paragraph("<b>Regla 0 / 100</b><br/>(Cero o Cien)", styles['TableCell']),
            Paragraph("0% mientras esté abierta.<br/>100% únicamente al cerrar y validar.", styles['TableCellBold']) if lang == 'ES' else Paragraph("0% while in progress.<br/>100% upon verified completion.", styles['TableCellBold']),
            Paragraph("Obligatorio para tareas de corta duración (< 2 semanas o 1 sprint). Elimina radicalmente el optimismo subjetivo.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Mandatory for short-cycle work packages (< 2 weeks or 1 sprint). Completely eradicates subjective optimism.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Regla 50 / 50</b><br/>(Cincuenta / Cincuenta)", styles['TableCell']),
            Paragraph("50% al iniciar formalmente.<br/>50% remanente al certificar la entrega.", styles['TableCellBold']) if lang == 'ES' else Paragraph("50% credited upon formal start.<br/>Remaining 50% upon sign-off.", styles['TableCellBold']),
            Paragraph("Paquetes de trabajo de ciclo medio (2 a 4 semanas). Otorga crédito por el inicio pero retiene el 50% hasta la entrega.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Medium-cycle work packages (2 to 4 weeks). Credits work initiation while retaining 50% hostage until sign-off.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Hitos Ponderados</b><br/>(Weighted Milestones)", styles['TableCell']),
            Paragraph("Porcentajes fijos pre-acordados ligados a entregables intermedios verificables.", styles['TableCellBold']) if lang == 'ES' else Paragraph("Pre-agreed percentage weights tied to auditable interim gates.", styles['TableCellBold']),
            Paragraph("Entregables extensos (> 1 mes). Ejemplo: 20% Arquitectura aprobada, 30% Código integrado, 30% UAT superado, 20% Pase a Prod.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Long-duration work packages (> 1 month). E.g.: 20% Architecture gate, 30% Core dev, 30% UAT sign-off, 20% Deployment.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Unidades Cuantificadas</b><br/>(Earned Standards)", styles['TableCell']),
            Paragraph("<b>% Real = Unidades Validadas / Total Planificado</b>", styles['TableCellBold']) if lang == 'ES' else Paragraph("<b>% Real = Verified Units / Total Scope</b>", styles['TableCellBold']),
            Paragraph("Migración masiva de datos (ej. millones de registros migrados), despliegue de sucursales o story points certificados.", styles['TableCell']) if lang == 'ES' else
            Paragraph("Repetitive high-volume scope: data migration pipelines, store rollouts, or completed story points certified by QA.", styles['TableCell'])
        ],
    ]
    rules_tab = Table([[Paragraph(h, styles['TableHeader']) for h in rules_head]] + rules_rows, colWidths=[110, 140, 261])
    rules_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(rules_tab)
    story.append(Spacer(1, 6))

    sub3_2 = "3.1 Protocolo de Gobernanza para la Estructura de Desglose del Trabajo (WBS)" if lang == 'ES' else "3.1 Work Breakdown Structure (WBS) Governance Protocol"
    story.append(Paragraph(sub3_2, styles['SubHeading']))

    p3_wbs = (
        "El éxito de un modelo EVM descansa sobre la consistencia de su WBS (*Work Breakdown Structure*). Cada paquete de trabajo debe satisfacer tres requisitos no negociables:\n"
        "1. **Unicidad de Presupuesto ($BAC_i$):** La suma de los presupuestos de los entregables debe coincidir exactamente con la línea base contractual aprobada (100%).\n"
        "2. **Asignación de Entradas Independientes:** El Avance Físico Real (%) no debe calcularse a partir del dinero gastado ni de las horas consumidas. Se determina exclusivamente por entregables tangibles completados.\n"
        "3. **Trazabilidad de Control Accounts (CA):** Los paquetes de trabajo deben agruparse bajo cuentas de control con un único responsable ejecutivo (Accountable) conforme al estándar RACI."
        if lang == 'ES' else
        "The operational viability of EVM depends on strict WBS architectural discipline. Every work package must comply with three mandatory governance principles:\n"
        "1. **Budget Completeness ($BAC_i$):** The sum of all deliverable budgets must equal 100% of the approved performance measurement baseline.\n"
        "2. **Independent Progress Sourcing:** Physical Percent Complete must NEVER be inferred from money spent or labor hours logged. It is strictly earned through verified deliverable acceptance.\n"
        "3. **Control Account (CA) Traceability:** Work packages must aggregate into designated Control Accounts assigned to a single accountable C-Level lead per RACI standards."
    )
    story.append(Paragraph(p3_wbs, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: CASO DE ESTUDIO REALISTA DE MEGAPROYECTO TECNOLÓGICO
    # =========================================================================
    sec4_title = "4. Caso de Estudio: Rescate de Megaproyecto Tecnológico (1.2M €)" if lang == 'ES' else "4. Enterprise Case Study: $1.2M Core Transformation Turnaround"
    story.append(Paragraph(sec4_title, styles['SecHeading']))

    p4_1 = (
        "**Contexto Corporativo:** Una entidad financiera multinacional inicia un proyecto estratégico de transformación del motor transaccional de pagos y conciliación. "
        "El proyecto cuenta con un presupuesto aprobado ($BAC$) de **1.200.000 €**, un cronograma de 12 meses estructurado en 25 entregables WBS, y un corte de control formal fijado en el **Mes 6** (50% de plazo transcurrido)."
        if lang == 'ES' else
        "**Corporate Context:** A tier-1 financial services institution launches an enterprise overhaul of its core transaction routing and reconciliation platform. "
        "The initiative holds an approved budget ($BAC$) of **$1,200,000**, a 12-month timeline across 25 WBS deliverables, and a formal mid-point audit gate at **Month 6** (50% elapsed schedule)."
    )
    story.append(Paragraph(p4_1, styles['Body']))

    # Cuadro comparativo Diagnóstico Mes 6
    p4_diag = "4.1 Diagnóstico de la Brecha de Varianza en Mes 6" if lang == 'ES' else "4.1 Mid-Point Diagnostic: Uncovering the Variance Gap"
    story.append(Paragraph(p4_diag, styles['SubHeading']))

    c_head = ["MÉTRICA ANALÍTICA" if lang == 'ES' else "ANALYTICAL METRIC", "VALOR A CORTE (MES 6)" if lang == 'ES' else "CUTOFF VALUE (M06)", "DIAGNÓSTICO DIRECTIVO EVM" if lang == 'ES' else "EXECUTIVE EVM INTERPRETATION"]
    c_rows = [
        [Paragraph("Presupuesto Planificado (PV)", styles['TableCellBold']), Paragraph("600.000 €" if lang == 'ES' else "$600,000", styles['TableCell']), Paragraph("El plan preveía haber completado la mitad del alcance contractual.", styles['TableCell']) if lang == 'ES' else Paragraph("Baseline schedule dictated 50% physical completion.", styles['TableCell'])],
        [Paragraph("Coste Real Incurrido (AC)", styles['TableCellBold']), Paragraph("600.000 €" if lang == 'ES' else "$600,000", styles['TableCell']), Paragraph("El gasto contable coincide al 100% con el presupuesto (falsa sensación de control).", styles['TableCell']) if lang == 'ES' else Paragraph("Actual cash burn matches budget exactly (false illusion of stability).", styles['TableCell'])],
        [Paragraph("Valor Ganado Físico (EV)", styles['TableCellBold']), Paragraph("516.000 €" if lang == 'ES' else "$516,000", styles['TableCell']), Paragraph("<b>Déficit real:</b> Solo se ha producido el 43% de entregables físicos válidos.", styles['TableCell']) if lang == 'ES' else Paragraph("<b>Real deficit:</b> Only 43% of physical deliverables actually delivered.", styles['TableCell'])],
        [Paragraph("Índice de Coste (CPI)", styles['TableCellBold']), Paragraph("<b>0.86x</b>", styles['TableCellBold']), Paragraph("<b>Sobrecoste del 16,3%:</b> Se destruyen 0,14 € por cada euro invertido.", styles['TableCell']) if lang == 'ES' else Paragraph("<b>16.3% Overrun:</b> $0.14 of capital is lost per dollar spent.", styles['TableCell'])],
        [Paragraph("Índice de Plazo (SPI)", styles['TableCellBold']), Paragraph("<b>0.86x</b>", styles['TableCellBold']), Paragraph("<b>Retraso crítico:</b> Déficit cronológico equivalente a casi 1 mes de trabajo.", styles['TableCell']) if lang == 'ES' else Paragraph("<b>Critical delay:</b> Schedule deficit equivalent to nearly 1 full month.", styles['TableCell'])],
        [Paragraph("Proyección EAC 1 Típica", styles['TableCellBold']), Paragraph("<b>1.395.349 €</b>" if lang == 'ES' else "<b>$1,395,349</b>", styles['TableCellBold']), Paragraph("Si no se interviene, el proyecto cerrará con un <b>déficit (VAC) de -195.349 €</b>.", styles['TableCell']) if lang == 'ES' else Paragraph("Without intervention, project closes with a <b>-$195,349 deficit (VAC)</b>.", styles['TableCell'])],
        [Paragraph("Esfuerzo TCPI (BAC)", styles['TableCellBold']), Paragraph("<b>1.14x</b>", styles['TableCellBold']), Paragraph("<b>Inviable:</b> El equipo requeriría acelerar su rendimiento un 32% (inviable según PMBOK).", styles['TableCell']) if lang == 'ES' else Paragraph("<b>Unviable:</b> Requires a 32% productivity leap on remaining scope.", styles['TableCell'])],
    ]
    c_tab = Table([[Paragraph(h, styles['TableHeader']) for h in c_head]] + c_rows, colWidths=[140, 100, 271])
    c_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(c_tab)
    story.append(Spacer(1, 5))

    p4_rescue = "4.2 El Paquete de Rescate Operativo y Resultados al Cierre" if lang == 'ES' else "4.2 Operational Turnaround Package & Final Closure Results"
    story.append(Paragraph(p4_rescue, styles['SubHeading']))

    p4_actions = (
        "Ante la evidencia matemática presentada por el Director de PMO en el *Executive Committee*, el Consejo de Administración activó tres palancas inmediatas:\n"
        "1. **Crashing Técnico Focalizado (WBS 2.1):** Incorporación de 2 arquitectos senior en consistencia distribuida (+24k€ inversión, recuperó +0.05 SPI y +0.04 CPI).\n"
        "2. **Fast-Tracking en Homologación Bancaria (WBS 2.3):** Paralelización de sandboxes con auditorías de ciberseguridad (recuperó 2,5 semanas de camino crítico, +0.06 SPI).\n"
        "3. **Descope Negociado & Precio Cerrado (WBS 3.1 & 3.3):** Aplazamiento de sincronización secundaria de CRM a Q1 post-Go-Live y transición de consultoría SAP a precio cerrado (ahorro directo de 35k€, +0.08 CPI).\n"
        "**Resultado Final al Cierre (Mes 12):** El proyecto completó el 100% de los entregables estratégicos con un coste real final de **1.248.000 €** (absorbiendo apenas un 4% de contingencia en lugar de los 195k€ proyectados) y con un desfase de solo 1 semana respecto a la fecha objetivo."
        if lang == 'ES' else
        "Confronted with the quantitative EVM briefing, the Executive Board immediately ratified three targeted turnaround levers:\n"
        "1. **Focused Technical Crashing (WBS 2.1):** Onboarded 2 senior distributed systems architects ($24k investment, regained +0.05 SPI and +0.04 CPI).\n"
        "2. **Fast-Tracking on Bank Integration (WBS 2.3):** Overlapped partner bank sandbox testing with cybersecurity audits (recovered 2.5 weeks, +0.06 SPI).\n"
        "3. **Negotiated Descope & Fixed Fees (WBS 3.1 & 3.3):** Deferred secondary CRM contact sync to Q1 post-launch and shifted SAP vendor billing to fixed-price milestones ($35k direct savings, +0.08 CPI).\n"
        "**Final Outcome at Closure (Month 12):** The project delivered 100% of core operational scope at a final actual cost of **$1,248,000** (absorbing merely 4% contingency instead of the projected $195k overrun) with only a 1-week final delivery delta."
    )
    story.append(Paragraph(p4_actions, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: PROTOCOLO DE DEFENSA EN COMITÉ & BIBLIOGRAFÍA
    # =========================================================================
    sec5_title = "5. Protocolo de Defensa ante Comité (Boardroom FAQ) & Referencias" if lang == 'ES' else "5. Boardroom Defense Protocol (Executive FAQ) & References"
    story.append(Paragraph(sec5_title, styles['SecHeading']))

    faq_items_es = [
        ("¿Por qué el SPI vuelve asintóticamente a 1.0 al terminar el proyecto aunque lleve meses o años de retraso?",
         "Es una limitación matemática intrínseca del EVM tradicional: cuando un proyecto finaliza con retraso, todo el trabajo planificado se completa finalmente, por lo que $EV = BAC$ y $PV = BAC$, forzando $SPI = BAC / BAC = 1.00$. "
         "Para solucionar esta anomalía en etapas tardías, el PMBOK y Lipke (2003) introducen el concepto de <b>Cronograma Ganado (Earned Schedule - ES)</b>, que mide la varianza en unidades de tiempo ($SV_t = ES - AT$) en lugar de moneda."),

        ("¿Cómo explicar al CFO que un TCPI > 1.15 es una fantasía estadística según el PMBOK?",
         "Estudios empíricos a gran escala en proyectos de defensa y tecnología (Christensen, 1998; Fleming & Koppelman, 2010) demuestran que **el CPI acumulado se estabiliza a partir del 20% de avance y rara vez mejora en más de 0.05 puntos**. "
         "Exigir a un equipo con un $CPI = 0.86$ que alcance un $TCPI = 1.14$ exige un salto de productividad del 32%. A menos que se modifique sustancialmente el alcance o los procesos, es un engaño contable que garantiza el fracaso."),

        ("¿Cuándo está formalmente justificado aprobar un re-baselining presupuestario?",
         "El re-baselining nunca debe utilizarse para 'ocultar' ineficiencias de gestión. Solo está justificado bajo tres supuestos: (a) Cambios sustanciales de alcance aprobados por el cliente o Board, (b) Shocks regulatorios o de mercado externos imprevistos, o (c) Cuando $TCPI_{BAC} > 1.15$ y se ha demostrado que las medidas de recuperación no pueden cerrar la brecha sin destruir los estándares de calidad.")
    ]

    faq_items_en = [
        ("Why does the SPI mathematically return to 1.00 at project end even when months or years late?",
         "This is an inherent algebraic trait of conventional EVM: when a delayed project eventually crosses the finish line, all planned deliverables are completed, meaning $EV = BAC$ and $PV = BAC$, forcing $SPI = BAC / BAC = 1.00$. "
         "To resolve this late-stage anomaly, modern PMBOK standards incorporate <b>Earned Schedule (ES)</b> (Lipke, 2003), measuring schedule variance in true time units ($SV_t = ES - AT$) rather than monetary equivalents."),

        ("How do we demonstrate to the CFO that a TCPI > 1.15 is pure statistical fantasy?",
         "Decades of empirical project research (Christensen, 1998; Fleming & Koppelman, 2010) prove that **cumulative CPI stabilizes past 20% completion and rarely improves by more than 0.05**. "
         "Demanding that a team operating at $CPI = 0.86$ suddenly achieve $TCPI = 1.14$ assumes an unprecedented 32% efficiency spike. Without changing scope or operating models, it is wishful thinking."),

        ("When is formal project budget re-baselining legitimately justified?",
         "Re-baselining must never serve as an accounting cover-up for poor execution. It is legitimately approved only when: (a) Major client or board-approved scope alterations occur, (b) Unforeseen regulatory or macro shocks arise, or (c) $TCPI_{BAC} > 1.15$ demonstrates that recovery plans cannot close the gap without compromising quality.")
    ]

    faq_list = faq_items_es if lang == 'ES' else faq_items_en
    for q_txt, a_txt in faq_list:
        story.append(Paragraph(f"• <b>Pregunta Board:</b> {q_txt}" if lang == 'ES' else f"• <b>Board Question:</b> {q_txt}", styles['FAQ_Q']))
        story.append(Paragraph(a_txt, styles['FAQ_A']))

    story.append(Spacer(1, 4))

    # Referencias Bibliográficas Canónicas
    sec_bib = "Referencias Bibliográficas Canónicas de Autoridad" if lang == 'ES' else "Canonical Authority References"
    story.append(Paragraph(sec_bib, styles['SubHeading']))

    bib_items = [
        "1. <b>Project Management Institute (PMI) (2019).</b> <i>The Standard for Earned Value Management</i>. Project Management Institute, Newtown Square, PA. ISBN: 978-1628256383.",
        "2. <b>Fleming, Q. W., & Koppelman, J. M. (2010).</b> <i>Earned Value Project Management – 4th Edition</i>. Project Management Institute. ISBN: 978-1935589082.",
        "3. <b>National Defense Industrial Association (NDIA) (2019).</b> <i>ANSI/EIA-748-D: Earned Value Management Systems Standard</i>. Arlington, VA.",
        "4. <b>Kerzner, H. (2017).</b> <i>Project Management: A Systems Approach to Planning, Scheduling, and Controlling – 12th Edition</i>. John Wiley & Sons. ISBN: 978-1119165354.",
        "5. <b>Christensen, D. S. (1998).</b> <i>The Costs and Benefits of Implementing an Earned Value Management System</i>. Acquisition Review Quarterly, Vol. 5, No. 4, pp. 373-386.",
        "6. <b>Barbara Minto (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall. ISBN: 978-0273710516."
    ]

    for bi in bib_items:
        story.append(Paragraph(bi, styles['Biblio']))

    # Construir documento pasando _lang al canvas
    def make_canvas(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c._lang = lang
        return c

    doc.build(story, canvasmaker=make_canvas)
    print(f"[{lang}] Guía metodológica generada exitosamente en: {out_path}")


def generate_all_pdf():
    """Genera las guías en español e inglés."""
    build_guide_pdf(lang='ES')
    build_guide_pdf(lang='EN')
    print("\nGeneración de guías metodológicas PDF completada con éxito.")


if __name__ == "__main__":
    generate_all_pdf()
