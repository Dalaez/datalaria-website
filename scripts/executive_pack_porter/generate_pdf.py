#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (4-5 páginas) para:
1. static/downloads/[ES]_5_Fuerzas_Porter/Guia_Metodologica_Porter_ES.pdf
2. static/downloads/[EN]_Porter_5_Forces/Methodology_Guide_Porter_EN.pdf

Estándar editorial de alta dirección (McKinsey / BCG):
- Portada ejecutiva y caja de metadatos.
- Sección 1: La Falacia del Análisis de Porter Cualitativo.
- Sección 2: Fundamentación Matemática del Índice de Atractivo de Industria.
- Sección 3: Algoritmo de Blindaje Estratégico (Economic Moat).
- Sección 4: Caso de Estudio Industrial Realista con Cifras Financieras (P&L, ROIC, EBITDA).
- Sección 5: Protocolo de Defensa en Comité (FAQ con respuestas a preguntas difíciles del CEO y CFO).
- Paginación dinámica con NumberedCanvas ("Página X de Y" / "Page X of Y").
- Expresiones matemáticas maquetadas con tablas estilizadas, entidades Unicode y sub/superíndices.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
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
C_AMBER_ACCENT = colors.HexColor("#D97706") # Amber 600
C_AMBER_LIGHT = colors.HexColor("#FEF3C7")  # Amber 100
C_ROSE_ACCENT = colors.HexColor("#E11D48")   # Rose 600
C_ROSE_LIGHT = colors.HexColor("#FFF1F2")   # Rose 50
C_EMERALD_ACCENT = colors.HexColor("#059669")
C_EMERALD_LIGHT = colors.HexColor("#ECFDF5")
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
            header_right = "5 FUERZAS DE PORTER PONDERADAS" if lang == 'ES' else "WEIGHTED PORTER'S 5 FORCES"
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
            fontName='Helvetica-Bold', fontSize=9.5, leading=12,
            textColor=C_BLUE_ACCENT, textTransform='uppercase', spaceAfter=5
        ),
        'CoverTitle': ParagraphStyle(
            'CoverTitle', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=22, leading=26,
            textColor=C_NAVY_DARK, spaceAfter=8
        ),
        'CoverSub': ParagraphStyle(
            'CoverSub', parent=base['Normal'],
            fontName='Helvetica', fontSize=11, leading=15,
            textColor=C_NAVY_MED, spaceAfter=16
        ),
        'H1': ParagraphStyle(
            'H1', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=14, leading=18,
            textColor=C_NAVY_DARK, spaceBefore=12, spaceAfter=6,
            keepWithNext=True
        ),
        'H2': ParagraphStyle(
            'H2', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=11, leading=14,
            textColor=C_BLUE_ACCENT, spaceBefore=8, spaceAfter=3,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=9, leading=13,
            textColor=C_NAVY_MED, spaceAfter=5
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=9, leading=13,
            textColor=C_NAVY_DARK, spaceAfter=5
        ),
        'Bullet': ParagraphStyle(
            'Bullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.5, leading=12.5,
            textColor=C_NAVY_MED, leftIndent=12, firstLineIndent=-8, spaceAfter=3
        ),
        'MathBox': ParagraphStyle(
            'MathBox', parent=base['Normal'],
            fontName='Courier-Bold', fontSize=9, leading=13,
            textColor=C_NAVY_DARK, alignment=1
        ),
        'TableHead': ParagraphStyle(
            'TableHead', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8, leading=10,
            textColor=C_WHITE, alignment=1
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['Normal'],
            fontName='Helvetica', fontSize=8, leading=10.5,
            textColor=C_NAVY_MED
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8, leading=10.5,
            textColor=C_NAVY_DARK
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica-Oblique', fontSize=8.5, leading=12,
            textColor=C_NAVY_DARK
        ),
        'FAQ_Q': ParagraphStyle(
            'FAQ_Q', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=9.5, leading=13,
            textColor=C_NAVY_DARK, spaceBefore=7, spaceAfter=2,
            keepWithNext=True
        ),
        'FAQ_A': ParagraphStyle(
            'FAQ_A', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.5, leading=12.5,
            textColor=C_NAVY_MED, spaceAfter=7
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
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def build_equation_box(eq_text, styles):
    p = Paragraph(eq_text, styles['MathBox'])
    t = Table([[p]], colWidths=[511])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t


# ==============================================================================
# GUÍA EN ESPAÑOL
# ==============================================================================
def generate_pdf_es(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=48, bottomMargin=52
    )
    styles = get_custom_styles()
    story = []

    # --- PÁGINA 1: PORTADA EJECUTIVA Y SECCIÓN 1 ---
    story.append(Spacer(1, 10))
    story.append(Paragraph("EXECUTIVE DECISION PACK • SERIE ESTRATEGIA CORPORATIVA", styles['CoverKicker']))
    story.append(Paragraph("5 Fuerzas de Porter Ponderadas & Atractivo de Industria", styles['CoverTitle']))
    story.append(Paragraph("Protocolo Matemático de Evaluación Estructural del Sector, Diagnóstico de Foso Defensivo (Moat) y Defensa en Comité de Inversión", styles['CoverSub']))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Autoría:</b> Datalaria Strategy Practice", styles['TableCell']),
            Paragraph("<b>Versión:</b> 2026.1 Oficial C-Level", styles['TableCell']),
            Paragraph("<b>Clasificación:</b> Board Decision Support", styles['TableCell'])
        ],
        [
            Paragraph("<b>Aplicación:</b> Estrategia & Asignación de Capital", styles['TableCell']),
            Paragraph("<b>Modelo:</b> Multivariable Ponderado", styles['TableCell']),
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
    story.append(Spacer(1, 12))

    # SECCIÓN 1: LA FALACIA DEL ANÁLISIS DE PORTER CUALITATIVO
    story.append(Paragraph("1. La Falacia del Análisis de Porter Cualitativo y la Dispersión Estratégica", styles['H1']))
    story.append(Paragraph(
        "Desde la publicación original de Michael E. Porter en <i>Harvard Business Review</i> (1979), el modelo de las cinco fuerzas competitivas ha sido el marco de referencia universal para evaluar la estructura industrial. Sin embargo, en la práctica habitual de los comités de dirección, el marco suele degenerar en un ejercicio descriptivo y subjetivo que carece de rigor analítico y es sistemáticamente rechazado por directores financieros (CFO) y comités de inversión.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Las tres patologías estructurales que invalidan el análisis cualitativo convencional son:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• <b>La Paradoja de la Simetría Ilusoria:</b> En una plantilla cualitativa, un factor crítico como la concentración del 55% de ingresos en tres clientes corporativos comparte el mismo peso visual que un trámite burocrático menor. La mente humana tiende a percibir paridad entre factores con idéntica tipografía, falseando la severidad real del riesgo.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Inexistencia de Elasticidades Cruzadas y Ponderación del Poder Real:</b> No todas las fuerzas impactan con la misma violencia en la cuenta de resultados (P&L). La amenaza de sustitutos puede tener un efecto letal inmediato en los márgenes brutos, mientras que las barreras de entrada pueden actuar como amortiguadores a largo plazo. Sin una ponderación estocástica normalizada, el modelo es incapaz de jerarquizar el peligro.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>La Brecha de la Última Milla Ejecutiva:</b> Concluido el análisis cualitativo, nadie en el comité sabe con exactitud cuánto CAPEX o qué partida de OPEX debe asignarse para defender la posición competitiva ni qué sponsor ejecutivo debe liderar cada iniciativa.",
        styles['Bullet']
    ))

    story.append(build_callout(
        "<b>Axioma de Consultoría Estratégica:</b> <i>\"Un análisis estratégico que no desemboca en un índice numérico auditable, un semáforo de rentabilidad y una partida presupuestaria vinculante en el P&L no es estrategia corporativa; es literatura de gestión.\"</i>",
        styles, border_color=C_ROSE_ACCENT, bg_color=C_ROSE_LIGHT
    ))

    # --- PÁGINA 2: SECCIÓN 2: FUNDAMENTACIÓN MATEMÁTICA ---
    story.append(PageBreak())
    story.append(Paragraph("2. Fundamentación Matemática: El Índice de Atractivo de Industria (A_ind)", styles['H1']))
    story.append(Paragraph(
        "Para erradicar la ambigüedad cualitativa, el modelo formaliza la evaluación del sector mediante un sistema multivariable con normalización estocástica unitaria y derivación escalar de intensidad.",
        styles['Body']
    ))

    story.append(Paragraph("Paso 2.1: Restricción Estocástica Unitaria por Fuerza (Σw = 1.00)", styles['H2']))
    story.append(Paragraph(
        "Cada una de las 5 fuerzas canónicas <i>F<sub>k</sub></i> (donde <i>k</i> ∈ {1: Rivalidad, 2: Proveedores, 3: Clientes, 4: Nuevos Entrantes, 5: Sustitutos}) se desagrega en un conjunto finito de <i>n<sub>k</sub></i> subfactores auditables. A cada subfactor se le asigna un peso relativo <i>w<sub>k,i</sub></i> que satisface estrictamente la restricción de normalización:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "&Sigma;<sub>i=1</sub><sup>n<sub>k</sub></sup> w<sub>k,i</sub> = 1.00 &nbsp;&nbsp;&nbsp;&nbsp; con &nbsp; w<sub>k,i</sub> &ge; 0 &nbsp;&forall; i",
        styles
    ))

    story.append(Paragraph("Paso 2.2: Escala Discreta Anclada a Evidencias y Fuerza Neta (F_k)", styles['H2']))
    story.append(Paragraph(
        "Cada subfactor se califica en una escala estandarizada <i>c<sub>k,i</sub></i> ∈ [1.0, 5.0], donde 1 representa un entorno altamente favorable para los márgenes del sector y 5 representa una hostilidad crítica destructora de rentabilidad. La puntuación neta ponderada de la fuerza <i>F<sub>k</sub></i> se define como:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "F<sub>k</sub> = &Sigma;<sub>i=1</sub><sup>n<sub>k</sub></sup> w<sub>k,i</sub> &middot; c<sub>k,i</sub> &nbsp;&nbsp;&nbsp;&nbsp; con &nbsp; F<sub>k</sub> &isin; [1.00, 5.00]",
        styles
    ))

    story.append(Paragraph("Paso 2.3: Ponderación Macro-Sectorial e Índice de Intensidad Competitiva (I_comp)", styles['H2']))
    story.append(Paragraph(
        "Dado que el peso macro de cada fuerza varía según la tipología del sector (por ejemplo, los bienes de equipo intensivos en capital otorgan mayor peso a proveedores y rivalidad, mientras que el SaaS corporativo es hiper-sensible a clientes y sustitutos), se asigna un vector de pesos sectoriales <i>W</i> = (<i>W</i><sub>1</sub>, ..., <i>W</i><sub>5</sub>) que satisface &Sigma; <i>W<sub>k</sub></i> = 1.00. El Índice Consolidado de Intensidad Competitiva se computa como:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "I<sub>comp</sub> = &Sigma;<sub>k=1</sub><sup>5</sup> W<sub>k</sub> &middot; F<sub>k</sub> &nbsp;&nbsp;&nbsp;&nbsp; con &nbsp; I<sub>comp</sub> &isin; [1.00, 5.00]",
        styles
    ))

    story.append(Paragraph("Paso 2.4: Cálculo Escalar del Atractivo Estructural de Industria (A_ind)", styles['H2']))
    story.append(Paragraph(
        "El Atractivo Estructural de la Industria es la función complementaria de la intensidad competitiva. A menor hostilidad de las fuerzas, mayor es el excedente económico disponible para las empresas operadoras:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "A<sub>ind</sub> = 5.00 - I<sub>comp</sub> = 5.00 - &Sigma;<sub>k=1</sub><sup>5</sup> W<sub>k</sub> &middot; F<sub>k</sub> &nbsp;&nbsp;&nbsp;&nbsp; con &nbsp; A<sub>ind</sub> &isin; [0.00, 4.00]",
        styles
    ))

    # Tabla de interpretación económica
    interp_data = [
        [
            Paragraph("<b>Rango A<sub>ind</sub></b>", styles['TableHead']),
            Paragraph("<b>Intensidad (I<sub>comp</sub>)</b>", styles['TableHead']),
            Paragraph("<b>Entorno Sectorial</b>", styles['TableHead']),
            Paragraph("<b>Diferencial ROIC vs WACC</b>", styles['TableHead']),
            Paragraph("<b>Directriz de Asignación</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>&ge; 2.20</b>", styles['TableCellBold']),
            Paragraph("&le; 2.80", styles['TableCell']),
            Paragraph("Atractivo Superior", styles['TableCell']),
            Paragraph("ROIC - WACC > +6.0%", styles['TableCell']),
            Paragraph("Inversión expansiva y captura de cuota", styles['TableCell'])
        ],
        [
            Paragraph("<b>1.40 - 2.19</b>", styles['TableCellBold']),
            Paragraph("2.81 - 3.60", styles['TableCell']),
            Paragraph("Moderado / Competitivo", styles['TableCell']),
            Paragraph("ROIC &asymp; WACC (+1.0% a +3.0%)", styles['TableCell']),
            Paragraph("Diferenciación activa y foso defensivo", styles['TableCell'])
        ],
        [
            Paragraph("<b>< 1.40</b>", styles['TableCellBold']),
            Paragraph("> 3.60", styles['TableCell']),
            Paragraph("Hostil / Trampa de Valor", styles['TableCell']),
            Paragraph("ROIC < WACC (Destrucción)", styles['TableCell']),
            Paragraph("Cosecha de caja o desinversión de nicho", styles['TableCell'])
        ]
    ]
    interp_table = Table(interp_data, colWidths=[70, 90, 105, 115, 131])
    interp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(interp_table)

    # --- PÁGINA 3: SECCIÓN 3: ALGORITMO DE BLINDAJE ESTRATÉGICO ---
    story.append(PageBreak())
    story.append(Paragraph("3. Algoritmo de Blindaje Estratégico: Economic Moat y Matriz Cartesiana", styles['H1']))
    story.append(Paragraph(
        "Conocer el atractivo de la industria es solo la mitad del diagnóstico. Una empresa puede operar en un sector estructuralmente difícil y, sin embargo, generar retornos extraordinarios si ha construido un <b>foso económico defensivo (Economic Moat)</b> que aísle su rentabilidad del acoso competitivo.",
        styles['Body']
    ))

    story.append(Paragraph("Los Cuatro Pilares Fundamentales del Foso Defensivo:", styles['BodyBold']))
    moat_pillars = [
        ("1. Costes de Cambio de Cliente (Switching Costs):", "Fricción operativa, técnica o procedimental que disuade al cliente de migrar a un rival (ej. integración profunda en flujos ERP, APIs propietarias o contratos marco multianuales)."),
        ("2. Efectos de Red (Network Effects):", "El valor del producto se incrementa exponencialmente con cada usuario adicional, creando un bloqueo competitivo insalvable para nuevos entrantes."),
        ("3. Activos Intangibles (Intangibles & IP):", "Patentes tecnológicas concedidas, marcas de alta reputación o licencias regulatorias exclusivas que imposibilitan la replicación directa."),
        ("4. Ventaja en Estructura de Costes (Cost Advantage & Scale):", "Economías de escala acumuladas en compras y curva de experiencia que permiten operar con costes unitarios significativamente inferiores a la media del sector.")
    ]
    for p_title, p_desc in moat_pillars:
        story.append(Paragraph(f"• <b>{p_title}</b> {p_desc}", styles['Bullet']))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Matriz Cartesiana: Atractivo de Industria (Eje X) vs Fortaleza del Moat (Eje Y)", styles['H2']))

    # Cuadrantes Cartesianos
    quad_data = [
        [
            Paragraph("<b>Cuadrante</b>", styles['TableHead']),
            Paragraph("<b>Condición Vectorial</b>", styles['TableHead']),
            Paragraph("<b>Postura Estratégica</b>", styles['TableHead']),
            Paragraph("<b>Directriz de Asignación de Capital para el CFO</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>I. Líder Estratégico</b>", styles['TableCellBold']),
            Paragraph("A<sub>ind</sub> &ge; 2 & Moat &ge; 3", styles['TableCell']),
            Paragraph("Reinversión Agresiva", styles['TableCellBold']),
            Paragraph("Acelerar CAPEX en capacidad, I+D y adquisición de clientes.", styles['TableCell'])
        ],
        [
            Paragraph("<b>II. Bastión Defensivo</b>", styles['TableCellBold']),
            Paragraph("A<sub>ind</sub> < 2 & Moat &ge; 3", styles['TableCell']),
            Paragraph("Cosecha & Blindaje", styles['TableCellBold']),
            Paragraph("Proteger márgenes vía costes de cambio. Maximizar dividendos y flujo libre.", styles['TableCell'])
        ],
        [
            Paragraph("<b>III. Terreno en Disputa</b>", styles['TableCellBold']),
            Paragraph("A<sub>ind</sub> &ge; 2 & Moat < 3", styles['TableCell']),
            Paragraph("Construcción de Barreras", styles['TableCellBold']),
            Paragraph("Sector rentable pero empresa vulnerable. Asignar fondos urgentemente a patentes.", styles['TableCell'])
        ],
        [
            Paragraph("<b>IV. Trampa de Valor</b>", styles['TableCellBold']),
            Paragraph("A<sub>ind</sub> < 2 & Moat < 3", styles['TableCell']),
            Paragraph("Desinversión / Nicho", styles['TableCellBold']),
            Paragraph("Congelar CAPEX de crecimiento. Reorientar activos hacia un micro-nicho defendible.", styles['TableCell'])
        ]
    ]
    quad_table = Table(quad_data, colWidths=[95, 95, 110, 211])
    quad_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(quad_table)

    story.append(Spacer(1, 6))
    story.append(build_callout(
        "<b>Regla de Oro de Asignación de Capital:</b> <i>\"El Consejo nunca debe aprobar CAPEX de expansión comercial en Cuadrantes III o IV sin haber financiado previamente el blindaje estructural del Moat.\"</i>",
        styles, border_color=C_AMBER_ACCENT, bg_color=C_AMBER_LIGHT
    ))

    # --- PÁGINA 4: SECCIÓN 4: CASO DE ESTUDIO INDUSTRIAL ---
    story.append(PageBreak())
    story.append(Paragraph("4. Caso de Estudio Industrial Realista: Diagnóstico y Blindaje en B2B", styles['H1']))
    story.append(Paragraph(
        "<b>Contexto Empresarial:</b> 'TechMotion Solutions' es un fabricante europeo de software embebido e instrumentación industrial con 45 M€ de facturación anual y un margen EBITDA histórico del 18.5% (8.32 M€). En el último ejercicio, la compañía experimentó una presión agresiva en renovaciones contractuales y la amenaza de sustitutos basados en inteligencia artificial.",
        styles['Body']
    ))

    story.append(Paragraph("Diagnóstico Cuantitativo de las 5 Fuerzas (Modelo Datalaria):", styles['H2']))

    case_scores = [
        [
            Paragraph("<b>Fuerza Competitiva</b>", styles['TableHead']),
            Paragraph("<b>Peso Sectorial (W<sub>k</sub>)</b>", styles['TableHead']),
            Paragraph("<b>Puntuación (F<sub>k</sub>)</b>", styles['TableHead']),
            Paragraph("<b>Severidad</b>", styles['TableHead']),
            Paragraph("<b>Diagnóstico Empírico Clave</b>", styles['TableHead'])
        ],
        [
            Paragraph("F1: Rivalidad Existente", styles['TableCellBold']),
            Paragraph("25%", styles['TableCell']),
            Paragraph("3.45", styles['TableCellBold']),
            Paragraph("Moderada", styles['TableCell']),
            Paragraph("3 actores concentran el 68%; competencia dura en precios", styles['TableCell'])
        ],
        [
            Paragraph("F2: Poder de Proveedores", styles['TableCellBold']),
            Paragraph("20%", styles['TableCell']),
            Paragraph("3.25", styles['TableCellBold']),
            Paragraph("Moderada", styles['TableCell']),
            Paragraph("Escasez de chips especializados y costes al alza (+12%)", styles['TableCell'])
        ],
        [
            Paragraph("F3: Poder de Clientes", styles['TableCellBold']),
            Paragraph("25%", styles['TableCell']),
            Paragraph("4.00", styles['TableCellBold']),
            Paragraph("Crítica", styles['TableCellBold']),
            Paragraph("Top 5 clientes concentran el 52% del ARR y exigen rebajas", styles['TableCell'])
        ],
        [
            Paragraph("F4: Nuevos Entrantes", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("2.20", styles['TableCellBold']),
            Paragraph("Baja", styles['TableCell']),
            Paragraph("Inversión mínima de 3M€ y homologación ISO disuaden", styles['TableCell'])
        ],
        [
            Paragraph("F5: Productos Sustitutos", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("3.85", styles['TableCellBold']),
            Paragraph("Crítica", styles['TableCellBold']),
            Paragraph("SaaS de automatización con IA ofrecen 40% menor coste", styles['TableCell'])
        ],
        [
            Paragraph("<b>TOTAL PONDERADO</b>", styles['TableCellBold']),
            Paragraph("<b>100%</b>", styles['TableCellBold']),
            Paragraph("<b>I<sub>comp</sub> = 3.42</b>", styles['TableCellBold']),
            Paragraph("<b>A<sub>ind</sub> = 1.58</b>", styles['TableCellBold']),
            Paragraph("<b>Sector Hostil • Compresión Proyectada: -4.5% EBITDA</b>", styles['TableCellBold'])
        ]
    ]
    case_table = Table(case_scores, colWidths=[105, 75, 70, 75, 186])
    case_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [C_WHITE, C_BG_CARD]),
        ('BACKGROUND', (0, -1), (-1, -1), C_AMBER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('ALIGN', (1, 0), (3, -1), 'CENTER'),
    ]))
    story.append(case_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Despliegue del Plan de Blindaje y Retorno Económico:", styles['H2']))
    story.append(Paragraph(
        "Ante la amenaza de que el margen EBITDA colapsara al 14.0% en 18 meses, el Comité de Dirección ratificó un plan de choque con <b>675.000 € en CAPEX</b> y <b>240.000 € en OPEX anual</b> centrado en neutralizar F3 y F5:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• <b>Despliegue de Conectores ERP Propietarios (CTO - 140k€ CAPEX):</b> Se integró el software directamente en SAP y Oracle de los 5 grandes clientes, elevando el switching cost a una media de 9 meses de trabajo de ingeniería por cliente. <i>Resultado: Churn reducido del 6.8% al 1.2%.</i>",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Módulo Nativo de IA Embebida (VP Product - 185k€ CAPEX):</b> En lugar de competir contra los sustitutos, se absorbió su ventaja tecnológica ofreciendo automatización predictiva nativa. <i>Resultado: Adopción del 68% en la base instalada.</i>",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Contratos Marco Plurianuales con Volume Tiers (CEO - 30k€ OPEX):</b> Firma de acuerdos a 3 años blindados con penalización por ruptura. <i>Resultado: ARR asegurado subió del 54% al 81%.</i>",
        styles['Bullet']
    ))

    story.append(build_callout(
        "<b>Impacto en P&L Auditable:</b> El margen EBITDA se protegió en el <b>18.8%</b> (+4.8% frente al escenario inercial de erosión), preservando <b>2.16 M€ anuales</b> de caja operativa con un <b>Payback de 13.8 meses</b> y un <b>ROIC incremental del 28.4%</b>.",
        styles, border_color=C_EMERALD_ACCENT, bg_color=C_EMERALD_LIGHT
    ))

    # --- PÁGINA 5: SECCIÓN 5: PROTOCOLO DE DEFENSA EN COMITÉ (FAQ) ---
    story.append(PageBreak())
    story.append(Paragraph("5. Protocolo de Defensa en Comité: Preguntas Difíciles del CEO y CFO", styles['H1']))
    story.append(Paragraph(
        "Para defender este modelo con éxito ante el Consejo de Administración o Comité de Inversiones, el consultor o directivo debe anticipar las objeciones habituales de finanzas y dirección general.",
        styles['Body']
    ))

    faqs = [
        ("P1: ¿Cómo refutar al CFO si afirma que la asignación de pesos a las 5 fuerzas es arbitraria?",
         "La asignación no es discrecional; sigue un protocolo de calibración objetiva en dos pasos. Primero, se ejecuta un panel Delphi ciego entre los miembros de la mesa directiva. Segundo, los pesos se correlacionan con la estructura de costes auditada (ej. el peso de proveedores F2 se ancla al % que representa el COGS directo sobre el ingreso; el peso de clientes F3 se ancla al ratio de concentración de ingresos del Top 10). Además, el modelo incluye un test de sensibilidad que prueba que una variación de ±15% en los pesos no altera el cuadrante estratégico resultante."),

        ("P2: ¿Por qué invertir en costes de cambio si los clientes corporativos exigen APIs abiertas y estándares de mercado?",
         "Los costes de cambio eficientes en el siglo XXI no se crean mediante formatos cerrados ilegales ni cautiverio tecnológico forzado. Se construyen mediante 'fricción de conveniencia': integración profunda de datos históricos, flujos de trabajo personalizados, entrenamiento acumulado del equipo operativo del cliente y acuerdos de nivel de servicio (SLA) críticos. El cliente es libre de marcharse contractualmente, pero el coste operativo y de parada de proceso hace económicamente irracional la migración."),

        ("P3: ¿Cómo justificar ante el CEO el riesgo de canibalización al lanzar módulos propios inspirados en sustitutos (F5)?",
         "La canibalización preventiva es una ley inexorable de la estrategia moderna. Si un sustituto tecnológico ofrece una relación precio-rendimiento superior, la empresa perderá esa cuota tarde o temprano. Es infinitamente preferible canibalizar un producto propio con un margen inferior pero retener el control del cliente y el flujo de caja, que ceder la relación comercial a un competidor emergente que terminará desplazando el catálogo completo."),

        ("P4: ¿Cómo se conecta el Índice de Atractivo (A_ind) con el Descuento de Flujos de Caja (DCF) y el M&A?",
         "En valoraciones de empresas o análisis de adquisiciones (M&A), el índice A_ind impacta directamente en dos variables: la tasa de descuento (WACC) y la tasa de crecimiento terminal (g). Un sector con A_ind < 1.50 exige una prima de riesgo específica por hostilidad sectorial de 150 a 250 puntos básicos, y una tasa de reinversión obligatoria más alta para mantener la paridad de mercado, evitando pagar múltiplos excesivos basados en EBITDA no defendibles.")
    ]

    for q_txt, a_txt in faqs:
        story.append(Paragraph(f"<b>{q_txt}</b>", styles['FAQ_Q']))
        story.append(Paragraph(a_txt, styles['FAQ_A']))

    # Construir documento PDF con NumberedCanvas
    def set_canvas_lang(canvas_obj, doc_obj):
        canvas_obj._lang = 'ES'

    doc.build(story, canvasmaker=NumberedCanvas, onFirstPage=set_canvas_lang, onLaterPages=set_canvas_lang)
    print(f"[ES] OK: Guía PDF generada: {out_path} ({os.path.getsize(out_path)} bytes).")
    return out_path


# ==============================================================================
# GUÍA EN INGLÉS
# ==============================================================================
def generate_pdf_en(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=48, bottomMargin=52
    )
    styles = get_custom_styles()
    story = []

    # --- PÁGINA 1: COVER & SECTION 1 ---
    story.append(Spacer(1, 10))
    story.append(Paragraph("EXECUTIVE DECISION PACK • CORPORATE STRATEGY SERIES", styles['CoverKicker']))
    story.append(Paragraph("Weighted Porter's 5 Forces & Industry Attractiveness Matrix", styles['CoverTitle']))
    story.append(Paragraph("Quantitative Structural Industry Assessment Protocol, Economic Moat Diagnostics, and Investment Committee Defense", styles['CoverSub']))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Author:</b> Datalaria Strategy Practice", styles['TableCell']),
            Paragraph("<b>Version:</b> 2026.1 Official C-Level", styles['TableCell']),
            Paragraph("<b>Classification:</b> Board Decision Support", styles['TableCell'])
        ],
        [
            Paragraph("<b>Application:</b> Strategy & Capital Allocation", styles['TableCell']),
            Paragraph("<b>Model:</b> Multivariate Weighted Matrix", styles['TableCell']),
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
    story.append(Spacer(1, 12))

    # SECTION 1: THE FALLACY OF QUALITATIVE PORTER ANALYSIS
    story.append(Paragraph("1. The Fallacy of Qualitative Porter Analysis and Strategic Dispersion", styles['H1']))
    story.append(Paragraph(
        "Ever since Michael E. Porter published his seminal framework in the <i>Harvard Business Review</i> (1979), the five competitive forces have served as the benchmark for industry structural analysis. However, in contemporary boardroom practice, the framework frequently deteriorates into a static, subjective brainstorming exercise systematically dismissed by CFOs and Investment Committees.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Three structural flaws undermine traditional qualitative assessments in enterprise strategy:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• <b>The Fallacy of Visual Equivalence:</b> On an unweighted template, a life-threatening factor such as 55% revenue concentration in three buyers carries the exact same visual weight as minor compliance friction. Human cognition intuitively assumes parity among bullet points, distorting risk evaluation.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Absence of Cross-Elasticity & True Power Weighting:</b> Not all forces exert equal pressure on the P&L. Substitute products can immediately collapse gross margins, whereas entry barriers operate as multi-year lags. Without normalized stochastic weights, the framework cannot prioritize capital allocation.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>The Last-Mile Decision Gap:</b> When the qualitative meeting concludes, leadership rarely leaves with auditable CAPEX/OPEX allocations or named C-Suite owners responsible for fortifying specific competitive barriers.",
        styles['Bullet']
    ))

    story.append(build_callout(
        "<b>Management Consulting Axiom:</b> <i>\"A strategic diagnosis that fails to culminate in an auditable metric, a sector return traffic light, and a binding budget in the corporate P&L is not corporate strategy; it is executive fiction.\"</i>",
        styles, border_color=C_ROSE_ACCENT, bg_color=C_ROSE_LIGHT
    ))

    # --- PÁGINA 2: SECTION 2: MATHEMATICAL FOUNDATIONS ---
    story.append(PageBreak())
    story.append(Paragraph("2. Mathematical Foundations: The Industry Attractiveness Index (A_ind)", styles['H1']))
    story.append(Paragraph(
        "To eliminate subjective ambiguity, the model converts structural market forces into a multivariate mathematical space governed by stochastic normalization and scalar attractiveness derivation.",
        styles['Body']
    ))

    story.append(Paragraph("Step 2.1: Stochastic Unit Normalization Constraint (&Sigma;w = 1.00)", styles['H2']))
    story.append(Paragraph(
        "Each canonical force <i>F<sub>k</sub></i> (where <i>k</i> ∈ {1: Rivalry, 2: Suppliers, 3: Buyers, 4: New Entrants, 5: Substitutes}) is evaluated across <i>n<sub>k</sub></i> empirical subfactors. Each subfactor carries a relative weight <i>w<sub>k,i</sub></i> satisfying:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "&Sigma;<sub>i=1</sub><sup>n<sub>k</sub></sup> w<sub>k,i</sub> = 1.00 &nbsp;&nbsp;&nbsp;&nbsp; where &nbsp; w<sub>k,i</sub> &ge; 0 &nbsp;&forall; i",
        styles
    ))

    story.append(Paragraph("Step 2.2: Standardized Evidence Scale & Net Force Calculation (F_k)", styles['H2']))
    story.append(Paragraph(
        "Each subfactor is rated on a standardized scale <i>c<sub>k,i</sub></i> ∈ [1.0, 5.0], where 1 reflects an exceptionally favorable profit environment and 5 reflects severe margin destruction. The weighted score of force <i>F<sub>k</sub></i> is:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "F<sub>k</sub> = &Sigma;<sub>i=1</sub><sup>n<sub>k</sub></sup> w<sub>k,i</sub> &middot; c<sub>k,i</sub> &nbsp;&nbsp;&nbsp;&nbsp; where &nbsp; F<sub>k</sub> &isin; [1.00, 5.00]",
        styles
    ))

    story.append(Paragraph("Step 2.3: Macro-Industry Weights & Competitive Intensity Index (I_comp)", styles['H2']))
    story.append(Paragraph(
        "Because force intensity differs structurally across industries (e.g., heavy manufacturing is weighted toward suppliers and rivalry, whereas B2B SaaS is dominated by buyers and substitutes), an industry vector <i>W</i> = (<i>W</i><sub>1</sub>, ..., <i>W</i><sub>5</sub>) is applied with &Sigma; <i>W<sub>k</sub></i> = 1.00:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "I<sub>comp</sub> = &Sigma;<sub>k=1</sub><sup>5</sup> W<sub>k</sub> &middot; F<sub>k</sub> &nbsp;&nbsp;&nbsp;&nbsp; where &nbsp; I<sub>comp</sub> &isin; [1.00, 5.00]",
        styles
    ))

    story.append(Paragraph("Step 2.4: Scalar Derivation of Industry Attractiveness (A_ind)", styles['H2']))
    story.append(Paragraph(
        "Industry Attractiveness is the inverse economic function of competitive hostility. Lower competitive friction expands available economic surplus:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "A<sub>ind</sub> = 5.00 - I<sub>comp</sub> = 5.00 - &Sigma;<sub>k=1</sub><sup>5</sup> W<sub>k</sub> &middot; F<sub>k</sub> &nbsp;&nbsp;&nbsp;&nbsp; where &nbsp; A<sub>ind</sub> &isin; [0.00, 4.00]",
        styles
    ))

    # Economic interpretation table
    interp_data = [
        [
            Paragraph("<b>A<sub>ind</sub> Range</b>", styles['TableHead']),
            Paragraph("<b>Hostility (I<sub>comp</sub>)</b>", styles['TableHead']),
            Paragraph("<b>Industry Environment</b>", styles['TableHead']),
            Paragraph("<b>ROIC vs WACC Spread</b>", styles['TableHead']),
            Paragraph("<b>Capital Allocation Mandate</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>&ge; 2.20</b>", styles['TableCellBold']),
            Paragraph("&le; 2.80", styles['TableCell']),
            Paragraph("Highly Attractive", styles['TableCell']),
            Paragraph("ROIC - WACC > +6.0%", styles['TableCell']),
            Paragraph("Aggressive expansion and market share growth", styles['TableCell'])
        ],
        [
            Paragraph("<b>1.40 - 2.19</b>", styles['TableCellBold']),
            Paragraph("2.81 - 3.60", styles['TableCell']),
            Paragraph("Moderate / Competitive", styles['TableCell']),
            Paragraph("ROIC &asymp; WACC (+1.0% to +3.0%)", styles['TableCell']),
            Paragraph("Active differentiation and moat defense", styles['TableCell'])
        ],
        [
            Paragraph("<b>< 1.40</b>", styles['TableCellBold']),
            Paragraph("> 3.60", styles['TableCell']),
            Paragraph("Hostile / Value Trap", styles['TableCell']),
            Paragraph("ROIC < WACC (Destruction)", styles['TableCell']),
            Paragraph("FCF harvest or hyper-niche refocusing", styles['TableCell'])
        ]
    ]
    interp_table = Table(interp_data, colWidths=[70, 90, 105, 115, 131])
    interp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(interp_table)

    # --- PÁGINA 3: SECTION 3: STRATEGIC MOAT ALGORITHM ---
    story.append(PageBreak())
    story.append(Paragraph("3. Strategic Moat Algorithm: Cartesian Matrix & Margin Preservation", styles['H1']))
    story.append(Paragraph(
        "Measuring industry attractiveness is only half the executive equation. An enterprise can operate within a structurally challenging market yet generate superior ROIC if it establishes a defensible <b>Economic Moat</b> shielding cash flows.",
        styles['Body']
    ))

    story.append(Paragraph("The Four Pillars of Defensible Moats:", styles['BodyBold']))
    moat_pillars = [
        ("1. Customer Switching Costs:", "Operational or procedural friction discouraging buyer migration (e.g., deep ERP workflow embedding, proprietary data integrations, or multi-year enterprise MSAs)."),
        ("2. Network Effects:", "Product value scales dynamically with each new participant, creating an insurmountable competitive wedge."),
        ("3. Intangible Assets & IP:", "Utility patents, regulatory certifications, and brand equity that prevent direct product replication."),
        ("4. Cost Advantage & Critical Scale:", "Procurement scale and cumulative operational learning curve delivering structurally superior unit economics.")
    ]
    for p_title, p_desc in moat_pillars:
        story.append(Paragraph(f"• <b>{p_title}</b> {p_desc}", styles['Bullet']))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Cartesian Decision Matrix: Industry Attractiveness (X) vs Economic Moat (Y)", styles['H2']))

    quad_data = [
        [
            Paragraph("<b>Quadrant</b>", styles['TableHead']),
            Paragraph("<b>Vector Condition</b>", styles['TableHead']),
            Paragraph("<b>Strategic Posture</b>", styles['TableHead']),
            Paragraph("<b>CFO Capital Allocation Directive</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>I. Strategic Leader</b>", styles['TableCellBold']),
            Paragraph("A<sub>ind</sub> &ge; 2 & Moat &ge; 3", styles['TableCell']),
            Paragraph("Aggressive Expansion", styles['TableCellBold']),
            Paragraph("Accelerate growth CAPEX in R&D, capacity, and customer acquisition.", styles['TableCell'])
        ],
        [
            Paragraph("<b>II. Defensive Fortress</b>", styles['TableCellBold']),
            Paragraph("A<sub>ind</sub> < 2 & Moat &ge; 3", styles['TableCell']),
            Paragraph("Moat Shielding & FCF", styles['TableCellBold']),
            Paragraph("Protect margins via switching costs. Maximize FCF and shareholder yield.", styles['TableCell'])
        ],
        [
            Paragraph("<b>III. Contested Ground</b>", styles['TableCellBold']),
            Paragraph("A<sub>ind</sub> &ge; 2 & Moat < 3", styles['TableCell']),
            Paragraph("Urgent Barrier Building", styles['TableCellBold']),
            Paragraph("Attractive market but vulnerable firm. Channel funds into IP and retention.", styles['TableCell'])
        ],
        [
            Paragraph("<b>IV. Value Trap</b>", styles['TableCellBold']),
            Paragraph("A<sub>ind</sub> < 2 & Moat < 3", styles['TableCell']),
            Paragraph("Divest / Hyper-Niche", styles['TableCellBold']),
            Paragraph("Freeze growth capex. Refocus capital on defendable micro-niches.", styles['TableCell'])
        ]
    ]
    quad_table = Table(quad_data, colWidths=[95, 95, 110, 211])
    quad_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(quad_table)

    story.append(Spacer(1, 6))
    story.append(build_callout(
        "<b>Capital Allocation Golden Rule:</b> <i>\"Boards must never approve aggressive commercial expansion capex in Quadrants III or IV without first fully funding defensible moat fortification.\"</i>",
        styles, border_color=C_AMBER_ACCENT, bg_color=C_AMBER_LIGHT
    ))

    # --- PÁGINA 4: SECTION 4: REALISTIC INDUSTRIAL CASE STUDY ---
    story.append(PageBreak())
    story.append(Paragraph("4. Industrial Case Study: Quantitative Diagnosis & Moat Defense", styles['H1']))
    story.append(Paragraph(
        "<b>Enterprise Context:</b> 'TechMotion Solutions' is a European enterprise software and industrial instrumentation vendor generating $45M in annual revenue with an 18.5% historical EBITDA margin ($8.32M). Over the past year, the company faced aggressive tender renegotiations and emerging AI-driven substitute platforms.",
        styles['Body']
    ))

    story.append(Paragraph("Quantitative 5 Forces Diagnosis (Datalaria Model):", styles['H2']))

    case_scores = [
        [
            Paragraph("<b>Competitive Force</b>", styles['TableHead']),
            Paragraph("<b>Weight (W<sub>k</sub>)</b>", styles['TableHead']),
            Paragraph("<b>Score (F<sub>k</sub>)</b>", styles['TableHead']),
            Paragraph("<b>Severity</b>", styles['TableHead']),
            Paragraph("<b>Key Empirical Finding</b>", styles['TableHead'])
        ],
        [
            Paragraph("F1: Competitive Rivalry", styles['TableCellBold']),
            Paragraph("25%", styles['TableCell']),
            Paragraph("3.45", styles['TableCellBold']),
            Paragraph("Moderate", styles['TableCell']),
            Paragraph("Top 3 players hold 68% market share; price competition", styles['TableCell'])
        ],
        [
            Paragraph("F2: Supplier Power", styles['TableCellBold']),
            Paragraph("20%", styles['TableCell']),
            Paragraph("3.25", styles['TableCellBold']),
            Paragraph("Moderate", styles['TableCell']),
            Paragraph("Component concentration and rising input costs (+12%)", styles['TableCell'])
        ],
        [
            Paragraph("F3: Buyer Power", styles['TableCellBold']),
            Paragraph("25%", styles['TableCell']),
            Paragraph("4.00", styles['TableCellBold']),
            Paragraph("Critical", styles['TableCellBold']),
            Paragraph("Top 5 buyers drive 52% ARR and force annual tender discounts", styles['TableCell'])
        ],
        [
            Paragraph("F4: New Entrants", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("2.20", styles['TableCellBold']),
            Paragraph("Low", styles['TableCell']),
            Paragraph("$3M+ upfront capital and ISO audits deter new entrants", styles['TableCell'])
        ],
        [
            Paragraph("F5: Substitute Products", styles['TableCellBold']),
            Paragraph("15%", styles['TableCell']),
            Paragraph("3.85", styles['TableCellBold']),
            Paragraph("Critical", styles['TableCellBold']),
            Paragraph("AI-native automation platforms offer 40% operating savings", styles['TableCell'])
        ],
        [
            Paragraph("<b>WEIGHTED TOTAL</b>", styles['TableCellBold']),
            Paragraph("<b>100%</b>", styles['TableCellBold']),
            Paragraph("<b>I<sub>comp</sub> = 3.42</b>", styles['TableCellBold']),
            Paragraph("<b>A<sub>ind</sub> = 1.58</b>", styles['TableCellBold']),
            Paragraph("<b>Hostile Market • Projected Erosion: -4.5% EBITDA</b>", styles['TableCellBold'])
        ]
    ]
    case_table = Table(case_scores, colWidths=[105, 75, 70, 75, 186])
    case_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [C_WHITE, C_BG_CARD]),
        ('BACKGROUND', (0, -1), (-1, -1), C_AMBER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('ALIGN', (1, 0), (3, -1), 'CENTER'),
    ]))
    story.append(case_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Action Plan Execution & Economic Return:", styles['H2']))
    story.append(Paragraph(
        "Faced with an imminent EBITDA margin decline to 14.0% over 18 months, leadership authorized a targeted moat plan with <b>$675,000 CAPEX</b> and <b>$240,000 annual OPEX</b> neutralizing F3 and F5:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• <b>Proprietary ERP Workflow Integration (CTO - $140k CAPEX):</b> Deep integration into enterprise SAP/Oracle environments created 9 months of procedural switching friction. <i>Result: Account churn fell from 6.8% to 1.2%.</i>",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Native Embedded AI Module (VP Product - $185k CAPEX):</b> Preempted external substitute platforms by embedding automated logic directly into core workflows. <i>Result: 68% adoption across existing client base.</i>",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Multi-Year Enterprise MSAs (CEO - $30k OPEX):</b> Structured 3-year commitments with tiered volume rebates. <i>Result: Locked recurring revenue (ARR) increased from 54% to 81%.</i>",
        styles['Bullet']
    ))

    story.append(build_callout(
        "<b>Audited P&L Return:</b> EBITDA margin was protected at <b>18.8%</b> (+4.8% vs inertia scenario), preserving <b>$2.16M in annual operating cash flow</b> with a <b>Payback of 13.8 months</b> and an incremental <b>ROIC of 28.4%</b>.",
        styles, border_color=C_EMERALD_ACCENT, bg_color=C_EMERALD_LIGHT
    ))

    # --- PÁGINA 5: SECTION 5: BOARD DEFENSE PROTOCOL (FAQ) ---
    story.append(PageBreak())
    story.append(Paragraph("5. Board Defense Protocol: Tough Executive Q&A", styles['H1']))
    story.append(Paragraph(
        "To successfully defend strategic proposals before the Board of Directors or Investment Committee, strategy leaders must prepare structured responses to core financial objections.",
        styles['Body']
    ))

    faqs = [
        ("Q1: How do we respond to the CFO if they claim weight assignments are subjective?",
         "Weights are not arbitrary; they are calibrated through a two-stage audit. First, independent Delphi blind scoring is conducted across executive heads. Second, weights are empirically anchored to financial statements (e.g., supplier weight F2 is tied to direct COGS share of revenue; buyer weight F3 reflects the revenue concentration of the top 10 accounts). Furthermore, the Excel model features sensitivity stress-testing proving that ±15% weight shifts do not alter the strategic quadrant."),

        ("Q2: Why invest in switching costs when enterprise buyers demand open APIs and data portability?",
         "Effective 21st-century switching costs do not rely on anticompetitive vendor lock-in or closed file formats. They are generated through 'convenience friction': deeply embedded operational workflows, accumulated historical datasets, custom integration templates, and enterprise SLAs. The client remains contractually free to leave, but the migration cost and downtime make substitution economically irrational."),

        ("Q3: How do we address the CEO's fear of self-cannibalization when adopting substitute tech (F5)?",
         "Preemptive cannibalization is an absolute strategic imperative. If an emerging technological paradigm offers superior price-performance, the market will adopt it. It is vastly preferable to cannibalize internal offerings at a slightly reduced gross margin while retaining the client and expanding market share, than to lose the customer entirely to an agile competitor."),

        ("Q4: How does Industry Attractiveness (A_ind) integrate into DCF models and M&A multiples?",
         "In discounted cash flow (DCF) valuations and acquisition modeling, A_ind directly influences the discount rate (WACC) and terminal growth rate (g). Sectors with A_ind < 1.50 require a 150 to 250 bps sector risk premium and higher terminal maintenance capex, preventing overpayment on unsupportable EBITDA multiples.")
    ]

    for q_txt, a_txt in faqs:
        story.append(Paragraph(f"<b>{q_txt}</b>", styles['FAQ_Q']))
        story.append(Paragraph(a_txt, styles['FAQ_A']))

    def set_canvas_lang(canvas_obj, doc_obj):
        canvas_obj._lang = 'EN'

    doc.build(story, canvasmaker=NumberedCanvas, onFirstPage=set_canvas_lang, onLaterPages=set_canvas_lang)
    print(f"[EN] OK: PDF Guide generated: {out_path} ({os.path.getsize(out_path)} bytes).")
    return out_path


def main():
    base_dir_es = "packages/[ES]_5_Fuerzas_Porter"
    base_dir_en = "packages/[EN]_Porter_5_Forces"
    os.makedirs(base_dir_es, exist_ok=True)
    os.makedirs(base_dir_en, exist_ok=True)

    generate_pdf_es(os.path.join(base_dir_es, "Guia_Metodologica_Porter_ES.pdf"))
    generate_pdf_en(os.path.join(base_dir_en, "Methodology_Guide_Porter_EN.pdf"))


if __name__ == '__main__':
    main()
