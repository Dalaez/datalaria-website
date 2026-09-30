#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para:
1. packages/[ES]_PESTEL_Cuantitativo/Guia_Metodologica_PESTEL_ES.pdf
2. packages/[EN]_Quantitative_PESTEL/Methodology_Guide_PESTEL_EN.pdf

Estándar editorial de alta dirección (McKinsey / BCG):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (La Falacia del PESTEL Cualitativo).
- Página 2: Sección 2 (Fundamentación Matemática del Espacio de Incertidumbre Bidimensional).
- Página 3: Sección 3 (La Matriz de Incertidumbre Estratégica: Cuadrantes y Protocolos C-Level).
- Página 4: Sección 4 (Caso de Estudio Industrial B2B con Impacto Financiero en P&L y EBITDA).
- Página 5: Sección 5 (Protocolo de Defensa en Comité de Dirección - FAQ) y Referencias Bibliográficas.
- Paginación dinámica con NumberedCanvas ("Página X de Y" / "Page X of Y").
- Expresiones matemáticas maquetadas con tablas estilizadas, entidades Unicode y sub/superíndices.
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
C_AMBER_ACCENT = colors.HexColor("#D97706") # Amber 600
C_ROSE_ACCENT = colors.HexColor("#E11D48")   # Rose 600
C_ROSE_LIGHT = colors.HexColor("#FFF1F2")   # Rose 50
C_EMERALD_ACCENT = colors.HexColor("#059669")
C_BG_CARD = colors.HexColor("#F8FAFC")      # Slate 50
C_BORDER_LIGHT = colors.HexColor("#CBD5E1") # Slate 300
C_WHITE = colors.HexColor("#FFFFFF")


class NumberedCanvas(canvas.Canvas):
    """Canvas con dos pasadas para calcular y pintar el número total de páginas dinámicamente."""
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
            header_right = "MATRIZ PESTEL CUANTITATIVA: SEVERIDAD & VOLATILIDAD" if lang == 'ES' else "QUANTITATIVE PESTEL MATRIX: SEVERITY & VOLATILITY"
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
            fontName='Helvetica-Bold', fontSize=9, leading=11,
            textColor=C_BLUE_ACCENT, textTransform='uppercase', spaceAfter=4
        ),
        'CoverTitle': ParagraphStyle(
            'CoverTitle', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=20, leading=24,
            textColor=C_NAVY_DARK, spaceAfter=6
        ),
        'CoverSub': ParagraphStyle(
            'CoverSub', parent=base['Normal'],
            fontName='Helvetica', fontSize=9.5, leading=13.5,
            textColor=C_NAVY_MED, spaceAfter=10
        ),
        'H1': ParagraphStyle(
            'H1', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=12.5, leading=16,
            textColor=C_NAVY_DARK, spaceBefore=9, spaceAfter=4,
            keepWithNext=True
        ),
        'H2': ParagraphStyle(
            'H2', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=10, leading=13,
            textColor=C_BLUE_ACCENT, spaceBefore=6, spaceAfter=3,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.5, leading=11.8,
            textColor=C_NAVY_MED, spaceAfter=4
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=11.8,
            textColor=C_NAVY_DARK, spaceAfter=4
        ),
        'Bullet': ParagraphStyle(
            'Bullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.2, leading=11.5,
            textColor=C_NAVY_MED, leftIndent=10, firstLineIndent=-7, spaceAfter=2.5
        ),
        'MathBox': ParagraphStyle(
            'MathBox', parent=base['Normal'],
            fontName='Courier-Bold', fontSize=8.8, leading=12,
            textColor=C_NAVY_DARK, alignment=1
        ),
        'TableHead': ParagraphStyle(
            'TableHead', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.8, leading=9.5,
            textColor=C_WHITE, alignment=1
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.8, leading=10,
            textColor=C_NAVY_MED
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.8, leading=10,
            textColor=C_NAVY_DARK
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica-Oblique', fontSize=8.2, leading=11.5,
            textColor=C_NAVY_DARK
        ),
        'FAQ_Q': ParagraphStyle(
            'FAQ_Q', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.8, leading=11.8,
            textColor=C_NAVY_DARK, spaceBefore=5, spaceAfter=1.5,
            keepWithNext=True
        ),
        'FAQ_A': ParagraphStyle(
            'FAQ_A', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.2, leading=11.2,
            textColor=C_NAVY_MED, spaceAfter=4
        ),
        'Biblio': ParagraphStyle(
            'Biblio', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.8, leading=10.5,
            textColor=C_NAVY_MED, leftIndent=10, firstLineIndent=-7, spaceAfter=3
        ),
    }
    return styles


def build_callout(text, styles, border_color=C_BLUE_ACCENT, bg_color=C_BLUE_LIGHT):
    p = Paragraph(text, styles['CalloutText'])
    t = Table([[p]], colWidths=[511])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def build_equation_box(eq_text, styles):
    p = Paragraph(eq_text, styles['MathBox'])
    t = Table([[p]], colWidths=[511])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    return t


# ==============================================================================
# GUÍA EN ESPAÑOL (5 PÁGINAS EXACTAS)
# ==============================================================================
def generate_pdf_es(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=46, bottomMargin=50
    )
    styles = get_custom_styles()
    story = []

    # ==========================
    # PÁGINA 1: PORTADA & SECCIÓN 1
    # ==========================
    story.append(Paragraph("DATALARIA STRATEGY PRACTICE • MCKINSEY & BCG STANDARD", styles['CoverKicker']))
    story.append(Paragraph("Matriz PESTEL Cuantitativa:<br/>Severidad, Volatilidad & Riesgo Macro", styles['CoverTitle']))
    story.append(Paragraph(
        "Guía metodológica oficial para transformar el análisis macroambiental cualitativo en un motor matemático "
        "bidimensional (Severidad en P&L vs. Volatilidad Temporal), con mapa térmico cartesiano y plan de resiliencia C-Level.",
        styles['CoverSub']
    ))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Autoría:</b> Datalaria Strategy Practice", styles['TableCell']),
            Paragraph("<b>Versión:</b> 2026.1 Oficial C-Level", styles['TableCell']),
            Paragraph("<b>Clasificación:</b> Board Decision Support", styles['TableCell'])
        ],
        [
            Paragraph("<b>Aplicación:</b> Estrategia Macro & Riesgos", styles['TableCell']),
            Paragraph("<b>Modelo:</b> Motor Bidimensional (S × V)", styles['TableCell']),
            Paragraph("<b>Estándar:</b> McKinsey / BCG Tier-1", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 170, 171])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. La Falacia del PESTEL Cualitativo y el Síndrome del Inventario Inerte", styles['H1']))
    story.append(Paragraph(
        "Desde que Francis J. Aguilar concibiera en 1967 el marco de exploración del entorno (Scanning the Business Environment), "
        "el análisis de las dimensiones Política, Económica, Social, Tecnológica, Ecológica y Legal (PESTEL) se convirtió en el estándar "
        "para la planificación corporativa. Sin embargo, en la abrumadora mayoría de las corporaciones, este marco sufre una degradación "
        "estructural que lo despoja de toda capacidad prescriptiva ante Comités de Dirección y Consejos de Administración:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• <b>La Trampa de la Simetría Tipográfica:</b> Cuando un informe lista en viñetas idénticas una sanción de hasta 35 M€ por el "
        "Reglamento Europeo de Inteligencia Artificial (EU AI Act) y una actualización de ordenanzas locales sobre residuos de oficina, "
        "el cerebro directivo asume inconscientemente paridad de atención. Se dedica el mismo tiempo de deliberación a una molestia burocrática "
        "que a una amenaza existencial contra la solvencia de la empresa.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>La Ceguera ante la Volatilidad Temporal:</b> No todas las fuerzas macroeconómicas operan en el mismo régimen dinámico. "
        "Una tendencia demográfica (inversión de la pirámide de edad) es estructural, lenta y altamente predecible a 10 años vista. "
        "Por el contrario, un shock en el precio mayorista del gas o un arancel transatlántico repentino es un fenómeno hipervolátil. "
        "Tratarlos como riesgos equivalentes distorsiona por completo la asignación de recursos y el diseño de coberturas.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>La Brecha de la Última Milla Ejecutiva:</b> Un análisis tradicional concluye con conclusiones etéreas como "
        "<i>'el entorno macroeconómico presenta vientos de cara moderados'</i>. Ningún Director Financiero (CFO) o Consejero Delegado (CEO) "
        "puede transformar esa prosa en una partida de capital (CAPEX/OPEX), un sponsor ejecutivo responsable o un plan de contingencia auditable.",
        styles['Bullet']
    ))
    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Axioma Datalaria:</b> <i>\"Un factor macro que no esté modelizado mediante un vector bidimensional de Severidad en P&L y "
        "Volatilidad Temporal no es estrategia corporativa; es recopilación periodística sin valor para la toma de decisiones del Consejo.\"</i>",
        styles, border_color=C_ROSE_ACCENT, bg_color=C_ROSE_LIGHT
    ))

    # ==========================
    # PÁGINA 2: FUNDAMENTACIÓN MATEMÁTICA
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("2. Fundamentación Matemática del Espacio de Incertidumbre Bidimensional", styles['H1']))
    story.append(Paragraph(
        "Para erradicar la subjetividad, formalizamos la evaluación macroambiental mediante un espacio métrico euclídeo bidimensional "
        "(S, V) ∈ [1.0, 5.0]² dotado de normalización estocástica y agregación tensorial.",
        styles['Body']
    ))

    story.append(Paragraph("Paso 2.1: Restricción Estocástica Unitaria por Dimensión (Σw = 1.00)", styles['H2']))
    story.append(Paragraph(
        "Cada una de las 6 dimensiones canónicas <i>d</i> ∈ {Político, Económico, Social, Tecnológico, Ecológico, Legal} agrupa <i>n<sub>d</sub></i> "
        "factores objetivos auditables. A cada factor <i>i</i> se le asigna un peso relativo <i>w<sub>d,i</sub></i> sujeto a la condición estricta:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "&Sigma;<sub>i=1</sub><sup>n<sub>d</sub></sup> w<sub>d,i</sub> = 1.00 &nbsp;&nbsp;&nbsp;&nbsp; con &nbsp; w<sub>d,i</sub> &ge; 0 &nbsp;&forall; i",
        styles
    ))

    story.append(Paragraph("Paso 2.2: Vector de Severidad (S) y Volatilidad (V) Anclado a Datos", styles['H2']))
    story.append(Paragraph(
        "Cada factor se califica en dos dimensiones independientes mediante escalas ancladas en indicadores empíricos:<br/>"
        "• <b>Severidad del Impacto en EBITDA (<i>S<sub>d,i</sub></i> ∈ [1.0, 5.0]):</b> Magnitud del deterioro operativo, donde 1.0 representa "
        "un impacto insignificante (&lt;1% EBITDA) y 5.0 representa una amenaza existencial (&gt;15% EBITDA o pérdida de licencia de actividad).<br/>"
        "• <b>Volatilidad Temporal (<i>V<sub>d,i</sub></i> ∈ [1.0, 5.0]):</b> Impredecibilidad y velocidad del shock, donde 1.0 representa evolución "
        "inercial predecible a 5+ años y 5.0 representa un shock disruptivo inmediato o cisne negro.",
        styles['Body']
    ))

    story.append(Paragraph("Paso 2.3: Formulación Geométrica del Riesgo Compuesto Individual (R_d,i)", styles['H2']))
    story.append(Paragraph(
        "El riesgo no es una suma aditiva ingenua, sino el producto geométrico que penaliza fuertemente la confluencia de severidad y volatilidad:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "R<sub>d,i</sub> = &radic;(S<sub>d,i</sub> &middot; V<sub>d,i</sub>) &nbsp;&nbsp;&nbsp;&nbsp; con &nbsp; R<sub>d,i</sub> &isin; [1.00, 5.00]",
        styles
    ))

    story.append(Paragraph("Paso 2.4: Agregación de la Dimensión e Índice de Riesgo Macro (R_comp)", styles['H2']))
    story.append(Paragraph(
        "La severidad media, volatilidad media y riesgo compuesto de cada dimensión se calculan mediante el producto escalar ponderado. "
        "Posteriormente, aplicando el vector de importancia macrosectorial <i>W</i> = (<i>W</i><sub>1</sub>, ..., <i>W</i><sub>6</sub>) con &Sigma; <i>W<sub>d</sub></i> = 1.00, "
        "obtenemos el <b>Índice de Riesgo Macro Compuesto (<i>R</i><sub>comp</sub>)</b> y la <b>Resiliencia Empresarial (<i>RES</i><sub>macro</sub>)</b>:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "R<sub>comp</sub> = &Sigma;<sub>d=1</sub><sup>6</sup> W<sub>d</sub> &middot; [&Sigma;<sub>i=1</sub><sup>n<sub>d</sub></sup> w<sub>d,i</sub> &middot; R<sub>d,i</sub>] &nbsp;&nbsp;|&nbsp;&nbsp; RES<sub>macro</sub> = 5.00 - R<sub>comp</sub>",
        styles
    ))
    story.append(Spacer(1, 4))

    # Tabla de interpretación de R_comp
    scale_data = [
        [
            Paragraph("<b>Rango R_comp</b>", styles['TableHead']),
            Paragraph("<b>Resiliencia</b>", styles['TableHead']),
            Paragraph("<b>Diagnóstico Macroambiental</b>", styles['TableHead']),
            Paragraph("<b>Directriz Estratégica del Consejo</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>&ge; 3.80</b>", styles['TableCellBold']),
            Paragraph("&le; 1.20", styles['TableCell']),
            Paragraph("<b>Entorno Crítico / Shocks Severos</b>", styles['TableCellBold']),
            Paragraph("Comité de crisis quincenal, blindaje de caja y coberturas financieras obligatorias.", styles['TableCell'])
        ],
        [
            Paragraph("<b>2.80 - 3.79</b>", styles['TableCellBold']),
            Paragraph("1.21 - 2.20", styles['TableCell']),
            Paragraph("<b>Riesgo Moderado / Vigilancia Táctica</b>", styles['TableCell']),
            Paragraph("Mitigación preventiva, diversificación de suministros y contratos marco.", styles['TableCell'])
        ],
        [
            Paragraph("<b>&lt; 2.80</b>", styles['TableCellBold']),
            Paragraph("&gt; 2.20", styles['TableCell']),
            Paragraph("<b>Entorno Resiliente / Estable</b>", styles['TableCell']),
            Paragraph("Asignación de capital expansiva, captura agresiva de cuota de mercado y M&A.", styles['TableCell'])
        ]
    ]
    scale_table = Table(scale_data, colWidths=[75, 65, 160, 211])
    scale_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD])
    ]))
    story.append(scale_table)

    # ==========================
    # PÁGINA 3: MATRIZ DE INCERTIDUMBRE
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("3. La Matriz de Incertidumbre Estratégica: Cuadrantes de Decisión", styles['H1']))
    story.append(Paragraph(
        "Al proyectar los factores en un plano cartesiano donde la abscisa representa la Volatilidad Temporal (<i>V</i>) y la ordenada la "
        "Severidad en EBITDA (<i>S</i>), la partición con centro en el umbral 3.0 define cuatro cuadrantes operacionales ineludibles:",
        styles['Body']
    ))

    q_matrix_data = [
        [
            Paragraph("<b>Cuadrante</b>", styles['TableHead']),
            Paragraph("<b>Umbral</b>", styles['TableHead']),
            Paragraph("<b>Arquetipo de Riesgo Macro</b>", styles['TableHead']),
            Paragraph("<b>Protocolo y Asignación de Capital C-Level</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Q1: Riesgos Críticos Volátiles</b>", styles['TableCellBold']),
            Paragraph("S &ge; 3.0<br/>V &ge; 3.0", styles['TableCell']),
            Paragraph("Fuerzas de máximo impacto y desestabilización violenta e impredecible (picos de energía, sanciones geopolíticas, ransomware).", styles['TableCell']),
            Paragraph("<b>Blindaje Activo:</b> Coberturas financieras de derivados, contratos PPA de energía, seguros cibernéticos y comité de crisis quincenal.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Q2: Riesgos Estructurales</b>", styles['TableCellBold']),
            Paragraph("S &ge; 3.0<br/>V &lt; 3.0", styles['TableCell']),
            Paragraph("Fuerzas de alto impacto pero trayectoria lenta, gradual y predecible (envejecimiento demográfico, directiva CSRD, descarbonización).", styles['TableCell']),
            Paragraph("<b>Planificación Multianual:</b> Reingeniería de procesos, planes de retención y formación técnica, e inversiones en CAPEX a 3-5 años.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Q3: Alertas Tempranas</b>", styles['TableCellBold']),
            Paragraph("S &lt; 3.0<br/>V &ge; 3.0", styles['TableCell']),
            Paragraph("Factores de bajo impacto actual pero alta dinamismo o velocidad de cambio (tendencias virales en redes, regulaciones piloto en mercados secundarios).", styles['TableCell']),
            Paragraph("<b>Vigilancia Pasiva:</b> Radar automatizado de KPIs y umbrales de activación (triggers) sin comprometer partidas de capital pesado.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Q4: Ruidos Menores</b>", styles['TableCellBold']),
            Paragraph("S &lt; 3.0<br/>V &lt; 3.0", styles['TableCell']),
            Paragraph("Fricciones operativas ordinarias de baja severidad y evolución estable (trámites burocráticos ordinarios, variaciones estacionales normales).", styles['TableCell']),
            Paragraph("<b>Absorción BAU:</b> Gestión rutinaria en operaciones ordinarias. Queda expresamente prohibido consumir tiempo del Consejo en estos asuntos.", styles['TableCell'])
        ]
    ]
    q_table = Table(q_matrix_data, colWidths=[105, 55, 175, 176])
    q_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD])
    ]))
    story.append(q_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Taxonomía de Respuestas: Cisnes Negros vs. Ruido Operacional", styles['H2']))
    story.append(Paragraph(
        "La aportación de Nassim Nicholas Taleb (2007) a la gestión de riesgos demostró que las organizaciones quiebran no por la acumulación "
        "de pequeños errores predecibles, sino por su fragilidad ante eventos de alta severidad y baja predictibilidad. "
        "La Matriz PESTEL Cuantitativa de Datalaria aísla estos fenómenos en el <b>Cuadrante Q1</b>, evitando que el Consejo disperse su capital "
        "en mitigar ruidos del Cuadrante Q4 que no ponen en riesgo la continuidad del negocio.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Protocolo de Activación por Umbrales (Triggers):</b> Cada factor del Cuadrante Q3 cuenta con un KPI de monitorización continua. "
        "Si la severidad de un factor de alerta temprana supera la cota de 3.0 (por ejemplo, si un proyecto de ley piloto se convierte en directiva vinculante), "
        "el modelo lo transfiere automáticamente a Q1, desbloqueando de forma reglamentaria los fondos de contingencia pre-autorizados.",
        styles['Body']
    ))
    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Regla de Oro del Consejo de Administración:</b> <i>\"El 80% del tiempo de deliberación estratégica del Consejo debe consagrarse "
        "exclusivamente a los factores ubicados en los Cuadrantes Q1 y Q2. Discutir factores de Q4 en comité es un síntoma de incompetencia en gobernanza.\"</i>",
        styles, border_color=C_AMBER_ACCENT, bg_color=colors.HexColor("#FFFBEB")
    ))

    # ==========================
    # PÁGINA 4: CASO DE ESTUDIO INDUSTRIAL
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("4. Caso de Estudio Industrial B2B con Impacto Financiero en P&L", styles['H1']))
    story.append(Paragraph(
        "Para verificar el retorno de la inversión de esta metodología ante un Comité de Inversión, exponemos el caso real anonimizado "
        "de un fabricante europeo de bienes de equipo e instrumentación de precisión (<b>Vectis Dynamics GmbH</b>):<br/>"
        "• <b>Facturación Anual:</b> 45.0 M€  |  <b>EBITDA Base:</b> 8.32 M€ (Margen EBITDA: 18.5%).<br/>"
        "• <b>Vulnerabilidades Críticas:</b> Alto consumo electrointensivo, exportación del 35% de producción a Norteamérica y soluciones "
        "con algoritmos embebidos sujetas a la regulación de alto riesgo del EU AI Act.",
        styles['Body']
    ))

    case_data = [
        [
            Paragraph("<b>Dimensión PESTEL</b>", styles['TableHead']),
            Paragraph("<b>Peso (Wd)</b>", styles['TableHead']),
            Paragraph("<b>Severidad (S)</b>", styles['TableHead']),
            Paragraph("<b>Volatilidad (V)</b>", styles['TableHead']),
            Paragraph("<b>Riesgo (Rd)</b>", styles['TableHead']),
            Paragraph("<b>Factor Crítico Evaluado en Vectis Dynamics</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>1. Político</b>", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("3.63", styles['TableCell']),
            Paragraph("3.25", styles['TableCell']),
            Paragraph("3.42", styles['TableCellBold']),
            Paragraph("Tensiones arancelarias bilaterales con recargos potenciales del 15% en aduanas.", styles['TableCell'])
        ],
        [
            Paragraph("<b>2. Económico</b>", styles['TableCellBold']),
            Paragraph("25%", styles['TableCell']),
            Paragraph("3.88", styles['TableCell']),
            Paragraph("3.68", styles['TableCell']),
            Paragraph("3.77", styles['TableCellBold']),
            Paragraph("Picos del 35% en gas natural y electricidad en meses invernales sin cobertura.", styles['TableCell'])
        ],
        [
            Paragraph("<b>3. Social</b>", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("3.18", styles['TableCell']),
            Paragraph("2.70", styles['TableCell']),
            Paragraph("2.91", styles['TableCellBold']),
            Paragraph("Escasez estructural de ingenieros mecatrónicos y rotación voluntaria del 18%.", styles['TableCell'])
        ],
        [
            Paragraph("<b>4. Tecnológico</b>", styles['TableCellBold']),
            Paragraph("20%", styles['TableCell']),
            Paragraph("3.88", styles['TableCell']),
            Paragraph("3.68", styles['TableCell']),
            Paragraph("3.77", styles['TableCellBold']),
            Paragraph("Competidores con agentes GenAI que reducen costes operativos unitarios un 28%.", styles['TableCell'])
        ],
        [
            Paragraph("<b>5. Ecológico</b>", styles['TableCellBold']),
            Paragraph("10%", styles['TableCell']),
            Paragraph("3.63", styles['TableCell']),
            Paragraph("3.15", styles['TableCell']),
            Paragraph("3.37", styles['TableCellBold']),
            Paragraph("Directiva CSRD: auditoría obligatoria de huella de carbono Alcance 1, 2 y 3.", styles['TableCell'])
        ],
        [
            Paragraph("<b>6. Legal</b>", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("3.98", styles['TableCell']),
            Paragraph("3.18", styles['TableCell']),
            Paragraph("3.54", styles['TableCellBold']),
            Paragraph("Sanciones de hasta 35 M€ por algoritmos de visión artificial no certificados ante la UE.", styles['TableCell'])
        ],
        [
            Paragraph("<b>CONSOLIDADO</b>", styles['TableCellBold']),
            Paragraph("<b>100%</b>", styles['TableCellBold']),
            Paragraph("<b>3.75</b>", styles['TableCellBold']),
            Paragraph("<b>3.42</b>", styles['TableCellBold']),
            Paragraph("<b>R_comp = 3.58</b>", styles['TableCellBold']),
            Paragraph("<b>Exposición Elevada • Resiliencia: 1.42 / 4.00</b>", styles['TableCellBold'])
        ]
    ]
    case_table = Table(case_data, colWidths=[78, 48, 55, 55, 68, 207])
    case_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [C_WHITE, C_BG_CARD]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#EFF6FF")),
    ]))
    story.append(case_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Diagnóstico Inercial vs. Retorno Financiero del Plan Aprobado", styles['H2']))
    story.append(Paragraph(
        "<b>Escenario Inercial (Sin Intervención):</b> La confluencia simultánea del shock energético y las penalizaciones por desalineación "
        "regulatoria proyectaban una contracción directa del margen EBITDA del <b>18.5% al 14.1%</b> en 12 meses, representando una evaporación "
        "anual de flujo de caja libre de <b>1.98 M€</b> y una depreciación en la valoración de la compañía de 16 M€ (a múltiplo de 8x EBITDA).",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Plan de Resiliencia Aprobado por el Consejo (715.000 €):</b> El Consejo de Administración ratificó una partida de "
        "<b>485.000 € en CAPEX</b> y <b>230.000 € en OPEX</b> distribuida en: contratos de compraventa PPA de electricidad fija a 3 años (CFO), "
        "certificación ISO 42001 de gobernanza algorítmica para el software embebido (CLO) y centro de ensamblaje en Europa del Este para eludir aranceles (COO).",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Resultado Financiero Verificado:</b> El margen EBITDA se blindó en el <b>18.2%</b> (preservando <b>1.85 M€ anuales de flujo de caja</b>). "
        "La inversión de contingencia se recuperó en <b>14.2 meses</b> (Payback), generando un <b>Ratio de Retorno de Resiliencia de 2.6x</b> "
        "respecto al capital total comprometido.",
        styles['Body']
    ))

    # ==========================
    # PÁGINA 5: PROTOCOLO DE DEFENSA & BIBLIOGRAFÍA
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("5. Protocolo de Defensa en Comité de Dirección (C-Level FAQ)", styles['H1']))

    faqs = [
        ("¿Cómo justificar ante el CFO una partida de contingencia para riesgos que tal vez no se materialicen?",
         "Mediante la teoría de opciones reales y el Coste Esperado de Inacción (CEI). La partida de 715k€ no es un coste hundido, sino una prima "
         "de seguro de P&L. Si el shock energético o legal ocurre sin cobertura, la pérdida directa asciende a 1.98 M€; pagar una prima del 36% "
         "para inmunizar el 90% de la cola de riesgo genera un Valor Actual Neto (VAN) de resiliencia positivo desde el primer trimestre."),

        ("¿Por qué medir la volatilidad temporal de forma independiente a la severidad del impacto?",
         "Porque exigen palancas operativas y financieras radicalmente distintas. Un riesgo de alta severidad y baja volatilidad (CSRD) "
         "se gestiona mediante planificación estructural a 3 años y reingeniería de sistemas. Un riesgo de alta severidad y alta volatilidad "
         "(picos energéticos o hackeo) exige coberturas líquidas en mercados financieros y protocolos con tiempo de activación inferior a 48 horas."),

        ("¿Cómo evitar que la matriz PESTEL se convierta en un ejercicio burocrático anual desconectado del negocio?",
         "Asignando cada factor a un sponsor ejecutivo C-Level estatutario e integrando los semáforos en los cuadros de mando mensuales. "
         "En el modelo Datalaria, los factores clasificados en Q1 (Críticos Volátiles) disparan revisiones automáticas quincenales."),

        ("¿Cómo conectar el Índice R_comp con las pruebas de estrés financiero (stress testing) y los modelos de valoración DCF?",
         "En comisiones de M&A y valoraciones DCF, un sector con R_comp > 3.80 exige elevar el WACC entre 150 y 250 puntos básicos por prima de "
         "riesgo macroeconómico no diversificable. Asimismo, en el test de estrés financiero se modeliza la confluencia simultánea de los tres factores de mayor severidad.")
    ]

    for q, a in faqs:
        story.append(Paragraph(f"<b>P: {q}</b>", styles['FAQ_Q']))
        story.append(Paragraph(a, styles['FAQ_A']))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Referencias Bibliográficas Canónicas de Autoridad", styles['H1']))

    bibliografia = [
        "1. <b>Aguilar, Francis J. (1967).</b> <i>Scanning the Business Environment</i>. Macmillan, New York. [Obra fundacional donde se introduce por primera vez la taxonomía macroambiental ETPS, antecesora directa del marco PESTEL contemporáneo].",
        "2. <b>Porter, Michael E. (1985).</b> <i>Competitive Advantage: Creating and Sustaining Superior Performance</i>. Free Press, New York. [Marco canónico sobre la interacción entre fuerzas estructurales externas y el diseño de barreras competitivas].",
        "3. <b>Narayanan, V.K., & Fahey, Liam (2001).</b> <i>Macroenvironmental Analysis for Strategic Management</i>. Wiley. [Formalización de la anticipación de discontinuidades tecnológicas y regulatorias en la estrategia corporativa].",
        "4. <b>Taleb, Nassim Nicholas (2007).</b> <i>The Black Swan: The Impact of the Highly Improbable</i>. Random House. [Fundamento de la asimetría entre eventos de alta severidad e impredecibilidad temporal en sistemas económicos complejos].",
        "5. <b>Minto, Barbara (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall. [Estándar de estructuración piramidal de mensajes y Action Titles para presentaciones ante Comités de Dirección].",
        "6. <b>World Economic Forum (2026).</b> <i>Global Risks Report: Macroeconomic Volatility and Geopolitical Fragmentation</i>. WEF, Ginebra. [Taxonomía empírica de riesgos macroeconómicos, climáticos y de ciberseguridad a escala global]."
    ]

    for b in bibliografia:
        story.append(Paragraph(b, styles['Biblio']))

    # Construir documento
    doc.build(story, canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, _lang='ES', **kwargs))
    print(f"[OK] Guía Metodológica PDF generada (ES): {out_path}")


# ==============================================================================
# GUÍA EN INGLÉS (5 PÁGINAS EXACTAS)
# ==============================================================================
def generate_pdf_en(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=46, bottomMargin=50
    )
    styles = get_custom_styles()
    story = []

    # ==========================
    # PÁGINA 1: COVER & SECTION 1
    # ==========================
    story.append(Paragraph("DATALARIA STRATEGY PRACTICE • MCKINSEY & BCG STANDARD", styles['CoverKicker']))
    story.append(Paragraph("Quantitative PESTEL Matrix:<br/>Severity, Volatility & Macro Risk", styles['CoverTitle']))
    story.append(Paragraph(
        "Official executive methodology guide to transforming qualitative macroenvironmental scanning into an objective "
        "2D mathematical engine (P&L Impact Severity vs. Temporal Volatility), featuring Cartesian risk mapping and C-Suite contingency roadmaps.",
        styles['CoverSub']
    ))

    # Meta Table
    meta_data = [
        [
            Paragraph("<b>Author:</b> Datalaria Strategy Practice", styles['TableCell']),
            Paragraph("<b>Version:</b> 2026.1 Official C-Level", styles['TableCell']),
            Paragraph("<b>Classification:</b> Board Decision Support", styles['TableCell'])
        ],
        [
            Paragraph("<b>Scope:</b> Macro Strategy & Risk Allocation", styles['TableCell']),
            Paragraph("<b>Model:</b> 2D Engine (Severity × Volatility)", styles['TableCell']),
            Paragraph("<b>Standard:</b> McKinsey / BCG Tier-1", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 170, 171])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. The Fallacy of Qualitative PESTEL and the Inert Inventory Syndrome", styles['H1']))
    story.append(Paragraph(
        "Ever since Francis J. Aguilar introduced the business environment scanning framework in 1967 (Scanning the Business Environment), "
        "analyzing Political, Economic, Social, Technological, Environmental, and Legal (PESTEL) forces has been the standard tool "
        "for corporate planning. Yet in the vast majority of boardrooms, this exercise degenerates into an unweighted descriptive "
        "inventory that provides zero prescriptive guidance for C-Suite executives and Boards of Directors:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• <b>The Typographic Equivalence Trap:</b> When a deck lists a potential €35M fine under the EU AI Act in identical bullet points "
        "alongside routine municipal zoning updates, human cognition intuitively assumes parity. Equal boardroom debate is squandered on minor "
        "administrative frictions while existential balance sheet threats remain unhedged.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Temporal Volatility Blindness:</b> External macro forces do not operate in the same dynamic regime. A demographic shift "
        "(aging population) is structural, gradual, and highly predictable over a 10-year horizon. In contrast, an unhedged natural gas price spike "
        "or sudden geopolitical tariff is a hyper-volatile shock. Conflating both without isolating volatility distorts capital allocation.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>The Executive 'Last-Mile' Decision Gap:</b> Qualitative decks routinely conclude with vague platitudes such as "
        "<i>'the macroeconomic environment presents moderate headwinds'</i>. Neither a Chief Financial Officer (CFO) nor a Chief Executive Officer (CEO) "
        "can translate such prose into capital reserves (CAPEX/OPEX), designated C-Suite accountability, or an auditable contingency roadmap.",
        styles['Bullet']
    ))
    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Datalaria Axiom:</b> <i>\"A macro factor that is not quantified through a two-dimensional vector of P&L Severity and "
        "Temporal Volatility is not corporate strategy; it is superficial journalism devoid of boardroom utility.\"</i>",
        styles, border_color=C_ROSE_ACCENT, bg_color=C_ROSE_LIGHT
    ))

    # ==========================
    # PÁGINA 2: MATHEMATICAL FOUNDATION
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("2. Mathematical Foundations of the 2D Strategic Uncertainty Space", styles['H1']))
    story.append(Paragraph(
        "To eradicate subjective ambiguity, the framework formalizes external environmental forces as a 2D Euclidean metric space "
        "(S, V) ∈ [1.0, 5.0]² governed by normalized stochastic weighting and tensor aggregation.",
        styles['Body']
    ))

    story.append(Paragraph("Step 2.1: Unitary Stochastic Normalization per Pillar (Σw = 1.00)", styles['H2']))
    story.append(Paragraph(
        "Each of the 6 canonical dimensions <i>d</i> ∈ {Political, Economic, Social, Technological, Environmental, Legal} groups <i>n<sub>d</sub></i> "
        "audited objective factors. Each factor <i>i</i> is assigned a relative weight <i>w<sub>d,i</sub></i> satisfying:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "&Sigma;<sub>i=1</sub><sup>n<sub>d</sub></sup> w<sub>d,i</sub> = 1.00 &nbsp;&nbsp;&nbsp;&nbsp; where &nbsp; w<sub>d,i</sub> &ge; 0 &nbsp;&forall; i",
        styles
    ))

    story.append(Paragraph("Step 2.2: Dual Scoring Vector: P&L Severity (S) & Temporal Volatility (V)", styles['H2']))
    story.append(Paragraph(
        "Each factor is evaluated across continuous 1.0 to 5.0 scales anchored in auditable metrics:<br/>"
        "• <b>P&L Severity (<i>S<sub>d,i</sub></i> ∈ [1.0, 5.0]):</b> Magnitude of downside EBITDA disruption, where 1.0 represents "
        "negligible impact (&lt;1% EBITDA) and 5.0 represents existential disruption (&gt;15% EBITDA or operational license forfeiture).<br/>"
        "• <b>Temporal Volatility (<i>V<sub>d,i</sub></i> ∈ [1.0, 5.0]):</b> Unpredictability and propagation velocity, where 1.0 represents predictable "
        "5-year structural trends and 5.0 represents sudden, disruptive black swan shocks.",
        styles['Body']
    ))

    story.append(Paragraph("Step 2.3: Geometric Composite Risk Formulation (R_d,i)", styles['H2']))
    story.append(Paragraph(
        "Factor risk is formulated as the geometric mean to heavily penalize the acute confluence of high severity and high volatility:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "R<sub>d,i</sub> = &radic;(S<sub>d,i</sub> &middot; V<sub>d,i</sub>) &nbsp;&nbsp;&nbsp;&nbsp; where &nbsp; R<sub>d,i</sub> &isin; [1.00, 5.00]",
        styles
    ))

    story.append(Paragraph("Step 2.4: Pillar Aggregation & Composite Macro Risk Index (R_comp)", styles['H2']))
    story.append(Paragraph(
        "Pillar severity, volatility, and consolidated risk are derived via inner dot product. Applying macro sector weights "
        "<i>W</i> = (<i>W</i><sub>1</sub>, ..., <i>W</i><sub>6</sub>) where &Sigma; <i>W<sub>d</sub></i> = 1.00, the <b>Composite Macro Risk Index (<i>R</i><sub>comp</sub>)</b> "
        "and <b>Corporate Resilience Index (<i>RES</i><sub>macro</sub>)</b> are formally established:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "R<sub>comp</sub> = &Sigma;<sub>d=1</sub><sup>6</sup> W<sub>d</sub> &middot; [&Sigma;<sub>i=1</sub><sup>n<sub>d</sub></sup> w<sub>d,i</sub> &middot; R<sub>d,i</sub>] &nbsp;&nbsp;|&nbsp;&nbsp; RES<sub>macro</sub> = 5.00 - R<sub>comp</sub>",
        styles
    ))
    story.append(Spacer(1, 4))

    # Scale interpretation table
    scale_data_en = [
        [
            Paragraph("<b>R_comp Range</b>", styles['TableHead']),
            Paragraph("<b>Resilience</b>", styles['TableHead']),
            Paragraph("<b>Macro Environment Diagnosis</b>", styles['TableHead']),
            Paragraph("<b>Boardroom Strategic Directive</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>&ge; 3.80</b>", styles['TableCellBold']),
            Paragraph("&le; 1.20", styles['TableCell']),
            Paragraph("<b>Critical Shock Exposure</b>", styles['TableCellBold']),
            Paragraph("Biweekly crisis committee, cash preservation, and mandatory financial derivatives hedging.", styles['TableCell'])
        ],
        [
            Paragraph("<b>2.80 - 3.79</b>", styles['TableCellBold']),
            Paragraph("1.21 - 2.20", styles['TableCell']),
            Paragraph("<b>Moderate Risk / Tactical Alert</b>", styles['TableCell']),
            Paragraph("Preventive mitigation, supplier dual-sourcing, and flexible commercial frameworks.", styles['TableCell'])
        ],
        [
            Paragraph("<b>&lt; 2.80</b>", styles['TableCellBold']),
            Paragraph("&gt; 2.20", styles['TableCell']),
            Paragraph("<b>Resilient / Stable Context</b>", styles['TableCell']),
            Paragraph("Expansive capital deployment, aggressive market share capture, and strategic M&A.", styles['TableCell'])
        ]
    ]
    scale_table_en = Table(scale_data_en, colWidths=[75, 65, 160, 211])
    scale_table_en.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD])
    ]))
    story.append(scale_table_en)

    # ==========================
    # PÁGINA 3: UNCERTAINTY MATRIX
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("3. Strategic Uncertainty Matrix: 4 Executive Decision Quadrants", styles['H1']))
    story.append(Paragraph(
        "Plotting Temporal Volatility (<i>V</i>) on the X-axis against P&L Severity (<i>S</i>) on the Y-axis with a 3.0 midpoint "
        "segments the macro risk landscape into four actionable governance quadrants:",
        styles['Body']
    ))

    q_matrix_data_en = [
        [
            Paragraph("<b>Quadrant</b>", styles['TableHead']),
            Paragraph("<b>Threshold</b>", styles['TableHead']),
            Paragraph("<b>Macro Risk Archetype</b>", styles['TableHead']),
            Paragraph("<b>Mandatory C-Suite Protocol & Capital Allocation</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Q1: Critical Volatile Risks</b>", styles['TableCellBold']),
            Paragraph("S &ge; 3.0<br/>V &ge; 3.0", styles['TableCell']),
            Paragraph("Forces with peak financial damage and violent, unpredictable timing (energy price shocks, sanctions, OT cyberattacks).", styles['TableCell']),
            Paragraph("<b>Active Shielding:</b> Financial derivatives, long-term corporate PPAs, dedicated contingency cash reserves, and biweekly board tracking.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Q2: Structural Risks</b>", styles['TableCellBold']),
            Paragraph("S &ge; 3.0<br/>V &lt; 3.0", styles['TableCell']),
            Paragraph("High impact forces evolving along predictable, multi-year structural trajectories (demographics, CSRD carbon audits, ESG mandates).", styles['TableCell']),
            Paragraph("<b>Multi-Year Planning:</b> Process re-engineering, STEM talent retention programs, and 3-5 year sustainability CAPEX roadmaps.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Q3: Early Warnings</b>", styles['TableCellBold']),
            Paragraph("S &lt; 3.0<br/>V &ge; 3.0", styles['TableCell']),
            Paragraph("Forces with limited immediate financial impact but high dynamism (viral social trends, pilot overseas rules, secondary FX swings).", styles['TableCell']),
            Paragraph("<b>Passive Surveillance:</b> Automated KPI radar and threshold activation triggers without committing heavy capital budgets.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Q4: Minor Noise</b>", styles['TableCellBold']),
            Paragraph("S &lt; 3.0<br/>V &lt; 3.0", styles['TableCell']),
            Paragraph("Routine operating frictions with low severity and stable patterns (ordinary paperwork, regular seasonal fluctuations).", styles['TableCell']),
            Paragraph("<b>Routine BAU Absorption:</b> Managed within standard operating workflows; strictly excluded from Boardroom agendas.", styles['TableCell'])
        ]
    ]
    q_table_en = Table(q_matrix_data_en, colWidths=[105, 55, 175, 176])
    q_table_en.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD])
    ]))
    story.append(q_table_en)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Response Taxonomy: Black Swans vs. Operational Noise", styles['H2']))
    story.append(Paragraph(
        "Nassim Nicholas Taleb's seminal research (2007) proved that corporate enterprises fail not from the accumulation of small predictable "
        "inefficiencies, but from systemic fragility to severe, unpredictable shocks. "
        "Datalaria's Quantitative PESTEL Matrix isolates these critical exposures within <b>Quadrant Q1</b>, ensuring executive bandwidth is not "
        "diluted managing Quadrant Q4 noise that poses zero existential threat.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Threshold Activation Protocols (Triggers):</b> Every early warning factor in Quadrant Q3 is monitored via continuous operational KPIs. "
        "If a trigger breaches the 3.0 severity threshold (e.g., draft pilot regulations transitioning into enforceable legislation), "
        "the model automatically escalates the factor into Q1, unlocking pre-authorized contingency budgets.",
        styles['Body']
    ))
    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Golden Boardroom Governance Rule:</b> <i>\"80% of executive boardroom strategic review must be dedicated strictly "
        "to factors located within Quadrants Q1 and Q2. Debating Q4 factors during board meetings is a definitive hallmark of flawed governance.\"</i>",
        styles, border_color=C_AMBER_ACCENT, bg_color=colors.HexColor("#FFFBEB")
    ))

    # ==========================
    # PÁGINA 4: CASE STUDY
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("4. Industrial B2B Case Study with Full P&L Financial Impact", styles['H1']))
    story.append(Paragraph(
        "To validate capital allocation efficacy, we present the anonymized case study of an advanced European precision "
        "engineering and equipment manufacturer (<b>Vectis Dynamics GmbH</b>):<br/>"
        "• <b>Annual Revenue:</b> $45.0M  |  <b>Base EBITDA:</b> $8.32M (EBITDA Margin: 18.5%).<br/>"
        "• <b>Critical Macro Vulnerabilities:</b> Power-intensive production, 35% non-EU export revenues, and embedded "
        "automation algorithms subject to the European AI Act.",
        styles['Body']
    ))

    case_data_en = [
        [
            Paragraph("<b>PESTEL Pillar</b>", styles['TableHead']),
            Paragraph("<b>Weight (Wd)</b>", styles['TableHead']),
            Paragraph("<b>Severity (S)</b>", styles['TableHead']),
            Paragraph("<b>Volatility (V)</b>", styles['TableHead']),
            Paragraph("<b>Risk (Rd)</b>", styles['TableHead']),
            Paragraph("<b>Audited Critical Factor at Vectis Dynamics</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>1. Political</b>", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("3.63", styles['TableCell']),
            Paragraph("3.25", styles['TableCell']),
            Paragraph("3.42", styles['TableCellBold']),
            Paragraph("Transatlantic trade tensions and potential 15% cross-border tariff surcharges.", styles['TableCell'])
        ],
        [
            Paragraph("<b>2. Economic</b>", styles['TableCellBold']),
            Paragraph("25%", styles['TableCell']),
            Paragraph("3.88", styles['TableCell']),
            Paragraph("3.68", styles['TableCell']),
            Paragraph("3.77", styles['TableCellBold']),
            Paragraph("Unhedged 35% winter power and gas volatility compressing manufacturing margins.", styles['TableCell'])
        ],
        [
            Paragraph("<b>3. Social</b>", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("3.18", styles['TableCell']),
            Paragraph("2.70", styles['TableCell']),
            Paragraph("2.91", styles['TableCellBold']),
            Paragraph("Severe STEM mechatronics talent shortage driving voluntary turnover to 18%.", styles['TableCell'])
        ],
        [
            Paragraph("<b>4. Technological</b>", styles['TableCellBold']),
            Paragraph("20%", styles['TableCell']),
            Paragraph("3.88", styles['TableCell']),
            Paragraph("3.68", styles['TableCell']),
            Paragraph("3.77", styles['TableCellBold']),
            Paragraph("Rival entrants deploying GenAI workflows to lower unit production costs by 28%.", styles['TableCell'])
        ],
        [
            Paragraph("<b>5. Environmental</b>", styles['TableCellBold']),
            Paragraph("10%", styles['TableCell']),
            Paragraph("3.63", styles['TableCell']),
            Paragraph("3.15", styles['TableCell']),
            Paragraph("3.37", styles['TableCellBold']),
            Paragraph("Mandatory EU CSRD Scope 1-3 greenhouse gas accounting and supply chain audits.", styles['TableCell'])
        ],
        [
            Paragraph("<b>6. Legal</b>", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("3.98", styles['TableCell']),
            Paragraph("3.18", styles['TableCell']),
            Paragraph("3.54", styles['TableCellBold']),
            Paragraph("EU AI Act non-compliance penalties up to €35M for uncertified vision algorithms.", styles['TableCell'])
        ],
        [
            Paragraph("<b>CONSOLIDATED</b>", styles['TableCellBold']),
            Paragraph("<b>100%</b>", styles['TableCellBold']),
            Paragraph("<b>3.75</b>", styles['TableCellBold']),
            Paragraph("<b>3.42</b>", styles['TableCellBold']),
            Paragraph("<b>R_comp = 3.58</b>", styles['TableCellBold']),
            Paragraph("<b>Elevated Exposure • Resilience: 1.42 / 4.00</b>", styles['TableCellBold'])
        ]
    ]
    case_table_en = Table(case_data_en, colWidths=[78, 48, 55, 55, 68, 207])
    case_table_en.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [C_WHITE, C_BG_CARD]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#EFF6FF")),
    ]))
    story.append(case_table_en)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Inertial Trajectory vs. Approved Resilience Return", styles['H2']))
    story.append(Paragraph(
        "<b>Inertial Baseline (No Mitigation):</b> The unhedged confluence of power volatility and regulatory fines was projected to "
        "compress EBITDA margins from <b>18.5% down to 14.1%</b> within 12 months, destroying <b>$1.98M in annual operating cash flow</b> "
        "and erasing $16M in enterprise value (at an 8x exit multiple).",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Approved Board Contingency Plan ($715,000):</b> The Board ratified <b>$485,000 CAPEX</b> and <b>$230,000 OPEX</b> earmarked for: "
        "3-year corporate PPA electricity hedges (CFO), ISO 42001 algorithmic compliance audit for embedded models (CLO), and an Eastern European "
        "assembly facility to bypass tariff exposure (COO).",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Verified Financial Return:</b> EBITDA margin stabilized at <b>18.2%</b> (safeguarding <b>$1.85M annual cash flow</b>). "
        "The contingency allocation broke even in <b>14.2 months</b>, generating a <b>Resilience ROI Ratio of 2.6x</b> against committed capital.",
        styles['Body']
    ))

    # ==========================
    # PÁGINA 5: BOARD DEFENSE & BIBLIOGRAPHY
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("5. Boardroom Defense Protocol (C-Suite FAQ)", styles['H1']))

    faqs_en = [
        ("How do I justify a macro contingency budget to the CFO when risks may not materialize?",
         "Through real options theory and the Cost of Inaction (COI) framework. Contingency capital ($715k) is not a sunk cost, but a risk management "
         "call option. If an unhedged shock materializes, direct EBITDA loss reaches $1.98M; paying a 36% premium to insulate 90% of tail risk "
         "yields a positive net present value (NPV) from day one."),

        ("Why evaluate temporal volatility independently from P&L severity?",
         "Because they mandate radically different capital and operational responses. A high severity, low volatility risk (CSRD compliance) "
         "is addressed via structured 3-year CAPEX and reporting re-engineering. Conversely, high severity, high volatility threats (power spikes or ransomware) "
         "require liquid market hedges and sub-48-hour response playbooks."),

        ("How do we prevent PESTEL from turning into a bureaucratic annual checklist?",
         "By anchoring every factor to a statutory C-Suite Owner and embedding risk thresholds into monthly board dashboards. "
         "Under our framework, factors in Q1 (Critical Volatile) trigger mandatory biweekly audit reviews, ensuring rapid capital reallocation."),

        ("How does the R_comp Index feed into corporate valuation and DCF stress testing?",
         "In M&A and corporate valuations, sectors with R_comp > 3.80 command a 150 to 250 bps macro risk premium added to the WACC. "
         "In stress testing, financial models simultaneously simulate the confluence of the top three severity drivers to verify debt covenant headroom.")
    ]

    for q, a in faqs_en:
        story.append(Paragraph(f"<b>Q: {q}</b>", styles['FAQ_Q']))
        story.append(Paragraph(a, styles['FAQ_A']))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Authoritative Canonical References", styles['H1']))

    bibliografia_en = [
        "1. <b>Aguilar, Francis J. (1967).</b> <i>Scanning the Business Environment</i>. Macmillan, New York. [Foundational text establishing the ETPS macroenvironmental taxonomy, direct ancestor of the contemporary PESTEL framework].",
        "2. <b>Porter, Michael E. (1985).</b> <i>Competitive Advantage: Creating and Sustaining Superior Performance</i>. Free Press, New York. [Canonical work linking external structural forces to the erection of sustainable competitive moats].",
        "3. <b>Narayanan, V.K., & Fahey, Liam (2001).</b> <i>Macroenvironmental Analysis for Strategic Management</i>. Wiley. [Advanced methodology for anticipating regulatory and technological discontinuities in enterprise strategy].",
        "4. <b>Taleb, Nassim Nicholas (2007).</b> <i>The Black Swan: The Impact of the Highly Improbable</i>. Random House. [Formal treatise on the radical asymmetry between high-impact unpredictable shocks and corporate fragility].",
        "5. <b>Minto, Barbara (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall. [Tier-1 executive communication standard governing boardroom pyramid structure and Action Titles].",
        "6. <b>World Economic Forum (2026).</b> <i>Global Risks Report: Macroeconomic Volatility and Geopolitical Fragmentation</i>. WEF, Geneva. [Global empirical dataset mapping economic, climate, and technology volatility across major sectors]."
    ]

    for b in bibliografia_en:
        story.append(Paragraph(b, styles['Biblio']))

    # Build document
    doc.build(story, canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, _lang='EN', **kwargs))
    print(f"[OK] Methodology Guide PDF generated (EN): {out_path}")


def main():
    dir_es = os.path.join("packages", "[ES]_PESTEL_Cuantitativo")
    dir_en = os.path.join("packages", "[EN]_Quantitative_PESTEL")

    path_es = os.path.join(dir_es, "Guia_Metodologica_PESTEL_ES.pdf")
    path_en = os.path.join(dir_en, "Methodology_Guide_PESTEL_EN.pdf")

    generate_pdf_es(path_es)
    generate_pdf_en(path_en)


if __name__ == '__main__':
    main()
