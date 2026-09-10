#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas ejecutivas en PDF (4-5 páginas) para:
1. Guia_Metodologica_DAFO_CAME_ES.pdf (Versión en Español)
2. Methodology_Guide_SWOT_TOWS_EN.pdf (Versión en Inglés)

Maquetación editorial de alta dirección con ReportLab y NumberedCanvas.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- PALETA DE COLOR EJECUTIVA ---
C_NAVY_DARK = colors.HexColor("#0F172A")    # Slate 900
C_NAVY_MED = colors.HexColor("#1E293B")     # Slate 800
C_SLATE_MUTED = colors.HexColor("#64748B")  # Slate 500
C_BLUE_ACCENT = colors.HexColor("#2563EB")  # Blue 600
C_BLUE_LIGHT = colors.HexColor("#EFF6FF")   # Blue 50
C_TEAL_ACCENT = colors.HexColor("#0D9488")  # Teal 600
C_AMBER_ACCENT = colors.HexColor("#D97706") # Amber 600
C_AMBER_LIGHT = colors.HexColor("#FEF3C7")  # Amber 100
C_RED_ACCENT = colors.HexColor("#E11D48")   # Rose 600
C_BG_CARD = colors.HexColor("#F8FAFC")      # Slate 50
C_BORDER_LIGHT = colors.HexColor("#CBD5E1") # Slate 300
C_WHITE = colors.HexColor("#FFFFFF")


class NumberedCanvas(canvas.Canvas):
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

        # Cabecera en páginas 2 en adelante
        if cur_page > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(C_SLATE_MUTED)
            self.drawString(42, 805, "DATALARIA | EXECUTIVE DECISION PACK")
            self.drawRightString(553, 805, "METODOLOGÍA ESTRATÉGICA C-LEVEL")
            self.setStrokeColor(C_BORDER_LIGHT)
            self.setLineWidth(0.75)
            self.line(42, 798, 553, 798)

        # Pie de página en todas las páginas
        self.setStrokeColor(C_BORDER_LIGHT)
        self.setLineWidth(0.75)
        self.line(42, 45, 553, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(C_SLATE_MUTED)
        self.drawString(42, 32, "Datalaria.com • Documento Confidencial para Consejo de Administración")
        page_str = f"Página {cur_page} de {total_pages}"
        self.drawRightString(553, 32, page_str)

        self.restoreState()


def get_custom_styles():
    base = getSampleStyleSheet()

    styles = {
        'CoverKicker': ParagraphStyle(
            'CoverKicker', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=10, leading=13,
            textColor=C_BLUE_ACCENT, textTransform='uppercase', spaceAfter=6
        ),
        'CoverTitle': ParagraphStyle(
            'CoverTitle', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=24, leading=29,
            textColor=C_NAVY_DARK, spaceAfter=10
        ),
        'CoverSub': ParagraphStyle(
            'CoverSub', parent=base['Normal'],
            fontName='Helvetica', fontSize=12, leading=16,
            textColor=C_NAVY_MED, spaceAfter=20
        ),
        'H1': ParagraphStyle(
            'H1', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=15, leading=19,
            textColor=C_NAVY_DARK, spaceBefore=14, spaceAfter=8,
            keepWithNext=True
        ),
        'H2': ParagraphStyle(
            'H2', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=11.5, leading=15,
            textColor=C_BLUE_ACCENT, spaceBefore=10, spaceAfter=4,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=9.5, leading=13.5,
            textColor=C_NAVY_MED, spaceAfter=6
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=9.5, leading=13.5,
            textColor=C_NAVY_DARK, spaceAfter=6
        ),
        'Bullet': ParagraphStyle(
            'Bullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=9, leading=13,
            textColor=C_NAVY_MED, leftIndent=14, firstLineIndent=-10, spaceAfter=4
        ),
        'MathBox': ParagraphStyle(
            'MathBox', parent=base['Normal'],
            fontName='Courier-Bold', fontSize=9.5, leading=14,
            textColor=C_NAVY_DARK, alignment=1
        ),
        'TableHead': ParagraphStyle(
            'TableHead', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=11,
            textColor=C_WHITE, alignment=1
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['Normal'],
            fontName='Helvetica', fontSize=8, leading=11,
            textColor=C_NAVY_MED
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8, leading=11,
            textColor=C_NAVY_DARK
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica-Oblique', fontSize=9, leading=13,
            textColor=C_NAVY_DARK
        ),
        'FAQ_Q': ParagraphStyle(
            'FAQ_Q', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=10, leading=13.5,
            textColor=C_NAVY_DARK, spaceBefore=8, spaceAfter=3,
            keepWithNext=True
        ),
        'FAQ_A': ParagraphStyle(
            'FAQ_A', parent=base['Normal'],
            fontName='Helvetica', fontSize=9, leading=13,
            textColor=C_NAVY_MED, spaceAfter=8
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
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return t


def build_equation_box(eq_text, styles):
    p = Paragraph(eq_text, styles['MathBox'])
    t = Table([[p]], colWidths=[511])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


# ==============================================================================
# CONSTRUCCIÓN GUÍA EN ESPAÑOL
# ==============================================================================
def generate_pdf_es(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=48, bottomMargin=52
    )
    styles = get_custom_styles()
    story = []

    # --------------------------------------------------------------------------
    # PÁGINA 1: PORTADA EJECUTIVA Y RESUMEN METODOLÓGICO
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("EXECUTIVE DECISION PACK • SERIE ESTRATEGIA CORPORATIVA", styles['CoverKicker']))
    story.append(Paragraph("DAFO Cuantitativo & Matriz CAME", styles['CoverTitle']))
    story.append(Paragraph("Protocolo Matemático de Diagnóstico Estratégico y Traducción Operativa para Comités de Dirección (C-Level)", styles['CoverSub']))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Autoría:</b> Datalaria Strategy Practice", styles['TableCell']),
            Paragraph("<b>Versión:</b> 2026.1 Oficial", styles['TableCell']),
            Paragraph("<b>Clasificación:</b> Board Decision Support", styles['TableCell'])
        ],
        [
            Paragraph("<b>Aplicación:</b> Planificación Estratégica & M&A", styles['TableCell']),
            Paragraph("<b>Modelo:</b> Cuantitativo Vectorial", styles['TableCell']),
            Paragraph("<b>Estándar:</b> McKinsey / BCG Tier-1", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 170, 171])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Resumen Ejecutivo y Propósito de la Guía", styles['H2']))
    story.append(Paragraph(
        "En más del 85% de las organizaciones corporativas, el análisis DAFO tradicional se reduce a un ejercicio de pizarra "
        "subjetivo que no sobrevive a la primera ronda de preguntas en un Comité de Dirección. Los factores se listan sin ponderación, "
        "las opiniones del directivo con mayor rango jerárquico sesgan las conclusiones y el documento final termina archivado "
        "sin vinculación alguna con los presupuestos de capital (CAPEX/OPEX).",
        styles['Body']
    ))
    story.append(Paragraph(
        "Esta guía metodológica formaliza el paso del DAFO cualitativo hacia un <b>modelo matemático vectorial</b>, eliminando la ambigüedad "
        "mediante la asignación de pesos relativos normalizados (\u2211w\u1d62 = 1.0) y calificaciones objetivas de impacto (1 a 5). "
        "Posteriormente, establece las reglas algorítmicas de la <b>Matriz CAME</b> para convertir los cuadrantes de fuerza en iniciativas "
        "de inversión accionables con responsable C-Level, calendario trimestral y métricas de retorno auditables.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    story.append(build_callout(
        "<b>Regla de Oro de Datalaria:</b> Un análisis estratégico solo es válido para un Comité de Dirección si "
        "resuelve tres condiciones: (1) matemáticamente riguroso y reproducible, (2) traducido en asignación de capital "
        "concreto, y (3) defendible en 5 minutos bajo el estándar de la Pirámide de Minto.",
        styles, border_color=C_NAVY_DARK, bg_color=C_BG_CARD
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Estructura del Executive Decision Pack Incluido", styles['H2']))
    story.append(Paragraph("• <b>Plantilla Excel Avanzada (.xlsx):</b> Motor matricial con 4 pestañas interconectadas, protección de fórmulas críticas, 10 factores dinámicos por cuadrante y gráfico cartesiano.", styles['Bullet']))
    story.append(Paragraph("• <b>Presentación C-Level (.pptx 16:9):</b> Diapositivas panorámicas con Action Titles ejecutivos, mapas térmicos de cruce y caja destacada de 'Decisión Requerida del Comité'.", styles['Bullet']))
    story.append(Paragraph("• <b>Guía Metodológica Oficial (.pdf):</b> Fundamentación matemática, caso práctico industrial resuelto y protocolo de defensa ante preguntas escépticas del Board.", styles['Bullet']))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PÁGINA 2: LA FALACIA DEL DAFO CUALITATIVO Y FUNDAMENTACIÓN MATEMÁTICA
    # --------------------------------------------------------------------------
    story.append(Paragraph("1. La Falacia del DAFO Cualitativo en el Boardroom", styles['H1']))
    story.append(Paragraph(
        "El análisis DAFO clásico adolece de tres sesgos fatales que destruyen su credibilidad ante Directores Generales (CEO) "
        "y Directores Financieros (CFO):", styles['Body']
    ))
    story.append(Paragraph("<b>1. Paradoja de Equivalencia Tipográfica:</b> Una fortaleza menor ('buen ambiente laboral') ocupa el mismo tamaño visual que una fortaleza decisiva ('margen bruto 18% superior al sector'), induciendo a error en la asignación de recursos.", styles['Bullet']))
    story.append(Paragraph("<b>2. Sesgo de Elocuencia y Rango (HIPPO):</b> La discusión se resuelve a favor del ejecutivo que mejor oratoria posee o mayor rango jerárquico ostenta, no de los datos operativos.", styles['Bullet']))
    story.append(Paragraph("<b>3. Desconexión Absoluta del P&L:</b> El análisis no produce cifras de inversión requerida ni retorno proyectado, convirtiéndose en un mero ejercicio retórico sin consecuencias.", styles['Bullet']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Formalización Matemática del Espacio Estratégico", styles['H1']))
    story.append(Paragraph(
        "Para superar la subjetividad, representamos cada cuadrante k \u2208 {F, D, O, A} como un vector de pesos w\u2096 y un vector de impacto c\u2096 en un espacio \u211d\u207f:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "w_k = [w_{k,1}, w_{k,2}, ..., w_{k,n}]^T, \u2200 w_{k,i} \u2208 [0, 1] \u2227 \u2211_{i=1}^n w_{k,i} = 1.00<br/>"
        "c_k = [c_{k,1}, c_{k,2}, ..., c_{k,n}]^T, \u2200 c_{k,i} \u2208 {1, 2, 3, 4, 5}<br/>"
        "S_k = w_k \u00b7 c_k = \u2211_{i=1}^n (w_{k,i} \u00b7 c_{k,i})",
        styles
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Donde <b>S_k</b> representa la puntuación ponderada agregada del cuadrante. A partir de estos valores escalares, "
        "definimos el <b>Vector de Postura Estratégica V</b> en el plano cartesiano:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "X = S_F - S_D \u2208 [-4.0, +4.0]  (Posición Interna Neta)<br/>"
        "Y = S_O - S_A \u2208 [-4.0, +4.0]  (Presión Externa Neta)<br/>"
        "\u2192 V = (X, Y) = (S_F - S_D) \u00ee + (S_O - S_A) \u0135<br/>"
        "||V|| = \u221a(X\u00b2 + Y\u00b2)  (Magnitud de Impulso Estratégico)",
        styles
    ))
    story.append(Spacer(1, 8))

    # Tabla de Cuadrantes
    q_table_data = [
        [Paragraph("<b>Cuadrante</b>", styles['TableHead']), Paragraph("<b>Condición</b>", styles['TableHead']), Paragraph("<b>Postura Dominante</b>", styles['TableHead']), Paragraph("<b>Mandato Ejecutivo del Consejo</b>", styles['TableHead'])],
        [Paragraph("<b>I (Superior Der.)</b>", styles['TableCellBold']), Paragraph("X \u2265 0, Y \u2265 0", styles['TableCell']), Paragraph("<b>OFENSIVA (Maxi-Maxi)</b>", styles['TableCellBold']), Paragraph("Máxima asignación de capital a captura de cuota, innovación y expansión.", styles['TableCell'])],
        [Paragraph("<b>II (Superior Izq.)</b>", styles['TableCellBold']), Paragraph("X < 0, Y \u2265 0", styles['TableCell']), Paragraph("<b>REORIENTACIÓN (Mini-Maxi)</b>", styles['TableCellBold']), Paragraph("Eliminar cuellos de botella internos para capitalizar vientos de cola.", styles['TableCell'])],
        [Paragraph("<b>III (Inferior Izq.)</b>", styles['TableCellBold']), Paragraph("X < 0, Y < 0", styles['TableCell']), Paragraph("<b>SUPERVIVENCIA (Mini-Mini)</b>", styles['TableCellBold']), Paragraph("Contención estricta de costes, desinversión selectiva y salvaguarda.", styles['TableCell'])],
        [Paragraph("<b>IV (Inferior Der.)</b>", styles['TableCellBold']), Paragraph("X \u2265 0, Y < 0", styles['TableCell']), Paragraph("<b>DEFENSIVA (Maxi-Mini)</b>", styles['TableCellBold']), Paragraph("Blindar contratos clave, proteger márgenes y construir moats de IP.", styles['TableCell'])],
    ]
    t_q = Table(q_table_data, colWidths=[90, 85, 130, 206])
    t_q.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_q)

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PÁGINA 3: EL ALGORITMO CAME Y LA MATRIZ DE CRUCE
    # --------------------------------------------------------------------------
    story.append(Paragraph("3. El Algoritmo CAME: Del Diagnóstico a la Inversión", styles['H1']))
    story.append(Paragraph(
        "El DAFO cuantitativo sitúa la posición de la compañía, pero es la <b>Matriz CAME (Corregir, Afrontar, Mantener, Explotar)</b> "
        "la que dicta la intervención en el P&L. Mediante el cruce sistemático de factores internos y externos, se construye una matriz de impacto M:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "M_{cruce} \u2208 {0, 1, 2, 3}^{m \u00d7 n}<br/>"
        "0 = Sin correlación | 1 = Impacto Débil | 2 = Impacto Moderado | 3 = Impacto Crítico / Sinérgico",
        styles
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Reglas de Transición Sistemática CAME", styles['H2']))
    story.append(Paragraph("<b>1. Corregir Debilidades (Estrategias WO):</b> Intersección de debilidades internas prioritarias con oportunidades externas. "
                           "¿Qué transformación o adquisición de capacidad elimina el bloqueo que impide capturar la oportunidad de mercado?", styles['Body']))
    story.append(Paragraph("<b>2. Afrontar Amenazas (Estrategias ST):</b> Intersección de fortalezas internas con amenazas del entorno. "
                           "¿Cómo se movilizan los activos nucleares (IP, caja, contratos) para levantar barreras que neutralicen competidores low-cost o regulaciones?", styles['Body']))
    story.append(Paragraph("<b>3. Mantener Fortalezas (Defensa de Moat):</b> Preservación activa de las ventajas competitivas que generan el margen operativo. "
                           "Inversión continua en retención de talento clave y protección jurídica de propiedad intelectual.", styles['Body']))
    story.append(Paragraph("<b>4. Explotar Oportunidades (Estrategias SO):</b> Máxima aceleración sobre las tendencias de mercado donde la organización "
                           "posee ventajas demostrables. Despliegue agresivo de capital comercial y alianzas estratégicas.", styles['Body']))
    story.append(Spacer(1, 6))

    # Tabla CAME de Gobernanza
    came_table_data = [
        [Paragraph("<b>Dimensión CAME</b>", styles['TableHead']), Paragraph("<b>Tipo Estrategia</b>", styles['TableHead']), Paragraph("<b>Criterio de Aprobación en Comité</b>", styles['TableHead']), Paragraph("<b>KPI Típico en P&L</b>", styles['TableHead'])],
        [Paragraph("<b>Corregir (C)</b>", styles['TableCellBold']), Paragraph("Reorientación (WO)", styles['TableCell']), Paragraph("Eliminación de cuellos de botella con ROI < 18 meses.", styles['TableCell']), Paragraph("Reducción de lead time, menor rotación.", styles['TableCell'])],
        [Paragraph("<b>Afrontar (A)</b>", styles['TableCellBold']), Paragraph("Defensiva (ST)", styles['TableCell']), Paragraph("Contingencia ante riesgos con impacto > 10% EBITDA.", styles['TableCell']), Paragraph("Retención de margen bruto, churn < 2%.", styles['TableCell'])],
        [Paragraph("<b>Mantener (M)</b>", styles['TableCellBold']), Paragraph("Preservación", styles['TableCell']), Paragraph("Mantenimiento de ventajas con ratio coste/beneficio óptimo.", styles['TableCell']), Paragraph("Patentes activas, satisfacción del equipo.", styles['TableCell'])],
        [Paragraph("<b>Explotar (E)</b>", styles['TableCellBold']), Paragraph("Ofensiva (SO)", styles['TableCell']), Paragraph("Proyectos con VAN positivo y captura rápida de cuota.", styles['TableCell']), Paragraph("Crecimiento de ARR, nuevos contratos Tier-1.", styles['TableCell'])],
    ]
    t_came = Table(came_table_data, colWidths=[95, 95, 180, 141])
    t_came.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_MED),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_came)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Protocolo de Asignación Financiera de Iniciativas", styles['H2']))
    story.append(Paragraph(
        "Toda iniciativa CAME admitida en la presentación al Consejo debe contar con: (1) un único <b>Owner C-Level</b> responsable de la ejecución, "
        "(2) un horizonte temporal definido por trimestres (Q1 a Q4), (3) una dotación presupuestaria dividida en <b>CAPEX y OPEX</b>, "
        "y (4) una métrica de control directamente vinculada al estado de resultados.",
        styles['Body']
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PÁGINA 4: CASO PRÁCTICO INDUSTRIAL COMPLETO
    # --------------------------------------------------------------------------
    story.append(Paragraph("4. Caso Práctico: InnoTech Industrial Components S.L.", styles['H1']))
    story.append(Paragraph(
        "<b>Contexto Empresarial:</b> Fabricante de componentes industriales de precisión con 48M € de facturación anual y 210 empleados. "
        "Enfrenta la transición hacia sensores IoT inteligentes, presión de competidores asiáticos y la necesidad de optar a ayudas públicas NextGen EU.",
        styles['Body']
    ))

    # Tabla del Caso
    case_summary_data = [
        [Paragraph("<b>Cuadrante</b>", styles['TableHead']), Paragraph("<b>Factores Clave Evaluados</b>", styles['TableHead']), Paragraph("<b>Peso w</b>", styles['TableHead']), Paragraph("<b>Imp. c</b>", styles['TableHead']), Paragraph("<b>Score S</b>", styles['TableHead'])],
        [Paragraph("<b>Fortalezas (F)</b>", styles['TableCellBold']), Paragraph("Margen bruto superior (+18.4%), 3 patentes europeas, retención NRR 118%, ISO 27001.", styles['TableCell']), Paragraph("100%", styles['TableCell']), Paragraph("4.6 / 5", styles['TableCell']), Paragraph("<b>4.35</b>", styles['TableCellBold'])],
        [Paragraph("<b>Debilidades (D)</b>", styles['TableCellBold']), Paragraph("Concentración de clientes (42% en top 2), lead time de 8.5 meses, dependencia hardware.", styles['TableCell']), Paragraph("100%", styles['TableCell']), Paragraph("3.4 / 5", styles['TableCell']), Paragraph("<b>2.25</b>", styles['TableCellBold'])],
        [Paragraph("<b>Oportunidades (O)</b>", styles['TableCellBold']), Paragraph("Subvenciones NextGen digitalización, directiva EU AI Act, expansión distribuidores LatAm.", styles['TableCell']), Paragraph("100%", styles['TableCell']), Paragraph("4.5 / 5", styles['TableCell']), Paragraph("<b>4.20</b>", styles['TableCellBold'])],
        [Paragraph("<b>Amenazas (A)</b>", styles['TableCellBold']), Paragraph("Presión de precios asiáticos (-35%), inflación ingenieros de IA, aranceles exteriores.", styles['TableCell']), Paragraph("100%", styles['TableCell']), Paragraph("3.2 / 5", styles['TableCell']), Paragraph("<b>2.35</b>", styles['TableCellBold'])],
    ]
    t_case = Table(case_summary_data, colWidths=[90, 241, 55, 60, 65])
    t_case.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_case)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Diagnóstico Cuantitativo del Caso", styles['H2']))
    story.append(Paragraph(
        "• <b>Posición Interna Neta:</b> X = S_F - S_D = 4.35 - 2.25 = <b>+2.10</b> (Las fortalezas dominan sobre las debilidades).<br/>"
        "• <b>Presión Externa Neta:</b> Y = S_O - S_A = 4.20 - 2.35 = <b>+1.85</b> (Las oportunidades superan los riesgos del mercado).<br/>"
        "• <b>Vector de Postura:</b> V = (+2.10, +1.85) \u2192 <b>Postura OFENSIVA / CRECIMIENTO (Maxi-Maxi)</b> con impulso ||V|| = 2.80 pts.",
        styles['Body']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Plan de Acción CAME Aprobado por el Comité", styles['H2']))
    came_actions_table = [
        [Paragraph("<b>ID</b>", styles['TableHead']), Paragraph("<b>Iniciativa Estratégica</b>", styles['TableHead']), Paragraph("<b>Owner</b>", styles['TableHead']), Paragraph("<b>Plazo</b>", styles['TableHead']), Paragraph("<b>Presupuesto</b>", styles['TableHead']), Paragraph("<b>KPI Objetivo</b>", styles['TableHead'])],
        [Paragraph("<b>CAME-E01</b>", styles['TableCellBold']), Paragraph("Despliegue módulo SaaS subvencionado en 40 factorías", styles['TableCell']), Paragraph("COO", styles['TableCell']), Paragraph("Q1-Q3", styles['TableCell']), Paragraph("105.000 €", styles['TableCell']), Paragraph("+1.2M € ARR", styles['TableCell'])],
        [Paragraph("<b>CAME-C01</b>", styles['TableCellBold']), Paragraph("Programa comercial en LatAm para diversificar clientes", styles['TableCell']), Paragraph("CCO", styles['TableCell']), Paragraph("Q2-Q4", styles['TableCell']), Paragraph("105.000 €", styles['TableCell']), Paragraph("Top-2 < 25% ARR", styles['TableCell'])],
        [Paragraph("<b>CAME-A01</b>", styles['TableCellBold']), Paragraph("Blindaje contractual plurianual con clientes enterprise", styles['TableCell']), Paragraph("CEO", styles['TableCell']), Paragraph("Q1-Q2", styles['TableCell']), Paragraph("30.000 €", styles['TableCell']), Paragraph("Churn < 1.5%", styles['TableCell'])],
        [Paragraph("<b>CAME-M02</b>", styles['TableCellBold']), Paragraph("Plan de incentivos y retención de talento clave de I+D", styles['TableCell']), Paragraph("CPO", styles['TableCell']), Paragraph("Q1-Q4", styles['TableCell']), Paragraph("45.000 €", styles['TableCell']), Paragraph("Rotación < 3%", styles['TableCell'])],
    ]
    t_act = Table(came_actions_table, colWidths=[55, 176, 50, 45, 75, 110])
    t_act.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_MED),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_act)
    story.append(Spacer(1, 8))

    story.append(build_callout(
        "<b>Resultado de Consejo:</b> Con una asignación total de 245.000 € (140k € CAPEX / 105k € OPEX), "
        "el Comité aprobó unánimemente el plan tras verificar que el riesgo de concentración de clientes "
        "quedaba blindado en paralelo a la captura de los 1.2M € de subvenciones y nuevo ARR.",
        styles, border_color=C_TEAL_ACCENT, bg_color=colors.HexColor("#ECFDF5")
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PÁGINA 5: PROTOCOLO DE DEFENSA ANTE EL CONSEJO (C-LEVEL FAQ)
    # --------------------------------------------------------------------------
    story.append(Paragraph("5. Protocolo de Defensa ante el Comité de Dirección (FAQ)", styles['H1']))
    story.append(Paragraph(
        "Respuestas metodológicas preparadas para neutralizar las preguntas más incisivas y escépticas en comités ejecutivos:",
        styles['Body']
    ))

    story.append(Paragraph("¿Cómo garantizamos que los pesos asignados no son arbitrarios? (Pregunta del CFO)", styles['FAQ_Q']))
    story.append(Paragraph(
        "<b>Respuesta:</b> Los pesos relativos (w\u1d62) no se asignan por intuición, sino mediante un protocolo de calibración "
        "en dos fases: primero, un panel Delphi ciego entre los miembros de la mesa directiva; segundo, la ponderación "
        "se valida contra estados financieros históricos (por ejemplo, el peso del margen operativo se ancla al EBITDA auditado). "
        "Asimismo, la plantilla de Excel incluye un análisis de sensibilidad que demuestra que una variación de \u00b115% en los pesos "
        "no altera el cuadrante estratégico dominante.",
        styles['FAQ_A']
    ))

    story.append(Paragraph("¿Qué ocurre si la dirección insiste en una estrategia ofensiva pero los números arrojan supervivencia? (Pregunta del CEO)", styles['FAQ_Q']))
    story.append(Paragraph(
        "<b>Respuesta:</b> El modelo matemático introduce el principio de <i>falsación objetiva</i>. Si el vector resultante V "
        "se sitúa en el cuadrante de Supervivencia (X < 0, Y < 0), forzar inversiones de crecimiento agresivo incrementa el riesgo "
        "de tensión de liquidez o quiebra. La metodología establece que antes de liberar CAPEX ofensivo, es preceptivo ejecutar "
        "las iniciativas CAME de Contención para desplazar la coordenada interna neta (X) por encima de cero.",
        styles['FAQ_A']
    ))

    story.append(Paragraph("¿Cómo evitamos que cada director de área sobrecalifique a su departamento? (Pregunta del COO)", styles['FAQ_Q']))
    story.append(Paragraph(
        "<b>Respuesta:</b> La regla fundamental del DAFO Cuantitativo exige que ninguna calificación c\u1d62 \u2265 4 sea admitida "
        "sin un respaldo documental auditable en la columna 'Métrica Base'. Si un departamento comercial afirma poseer 'excelente relación "
        "con clientes', debe aportar un Net Retention Rate (NRR) > 110% o un NPS auditado. De lo contrario, la calificación máxima admisible es 3.",
        styles['FAQ_A']
    ))

    story.append(Paragraph("¿Con qué periodicidad debe actualizarse la matriz cuantitativa? (Pregunta del CRO)", styles['FAQ_Q']))
    story.append(Paragraph(
        "<b>Respuesta:</b> Se recomienda una gobernanza en dos niveles: (1) <b>Revisión Trimestral Ligera</b> de los avances "
        "de las iniciativas CAME y reevaluación del vector de postura; y (2) <b>Recálculo Anual Integral</b> durante el ciclo "
        "presupuestario de planificación estratégica en Q3-Q4.",
        styles['FAQ_A']
    ))
    story.append(Spacer(1, 10))

    # Cuadro Final de Cierre
    story.append(build_callout(
        "<b>Garantía Oficial Datalaria:</b> Este Executive Decision Pack ha sido diseñado bajo los estándares de las principales "
        "firmas globales de consultoría estratégica. Para soporte metodológico, adaptaciones corporativas o workshops de facilitación, "
        "contacte con <b>consultoria@datalaria.com</b>.",
        styles, border_color=C_NAVY_DARK, bg_color=C_BG_CARD
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK ES] PDF generado: {out_path} ({os.path.getsize(out_path)} bytes)")


# ==============================================================================
# CONSTRUCCIÓN GUÍA EN INGLÉS
# ==============================================================================
def generate_pdf_en(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=48, bottomMargin=52
    )
    styles = get_custom_styles()
    story = []

    # --------------------------------------------------------------------------
    # PAGE 1: EXECUTIVE COVER & METHODOLOGY OVERVIEW
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("EXECUTIVE DECISION PACK • CORPORATE STRATEGY PRACTICE", styles['CoverKicker']))
    story.append(Paragraph("Quantitative SWOT & TOWS Matrix", styles['CoverTitle']))
    story.append(Paragraph("Mathematical Framework for Strategic Diagnosis and Boardroom Capital Allocation Protocols", styles['CoverSub']))

    meta_data = [
        [
            Paragraph("<b>Author:</b> Datalaria Strategy & Architecture", styles['TableCell']),
            Paragraph("<b>Version:</b> 2026.1 Official Release", styles['TableCell']),
            Paragraph("<b>Classification:</b> Board Decision Support", styles['TableCell'])
        ],
        [
            Paragraph("<b>Focus:</b> Corporate Strategy & Capital Allocation", styles['TableCell']),
            Paragraph("<b>Model:</b> Vector Quantitative Engine", styles['TableCell']),
            Paragraph("<b>Standard:</b> Tier-1 Strategy Consulting", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 170, 171])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Executive Summary & Methodological Purpose", styles['H2']))
    story.append(Paragraph(
        "In over 85% of corporate boardrooms, traditional SWOT analyses fail the first rigorous cross-examination from the Board. "
        "Items are listed qualitatively without weighting, loudest-voice bias skews strategic priorities, and the final slide is "
        "promptly archived without connecting to capital expenditure (CAPEX/OPEX) or P&L targets.",
        styles['Body']
    ))
    story.append(Paragraph(
        "This methodology guide formalizes the transition from qualitative brainstorming to an <b>objective vector-based mathematical engine</b>. "
        "By enforcing normalized relative weights (\u2211w\u1d62 = 1.0) and standardized impact ratings (1 to 5), it establishes a reproducible "
        "baseline. It then operationalizes the <b>TOWS Matrix</b> to convert strategic quadrant forces into budgeted corporate initiatives "
        "with designated C-Level sponsors, quarterly delivery schedules, and auditable financial KPIs.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    story.append(build_callout(
        "<b>Datalaria's Boardroom Rule:</b> A corporate strategy analysis is only boardroom-ready if it meets three criteria: "
        "(1) mathematically rigorous and reproducible, (2) directly translated into capital allocation, and (3) defensible in 5 minutes "
        "under the Minto Pyramid Principle.",
        styles, border_color=C_NAVY_DARK, bg_color=C_BG_CARD
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Included Deliverables in this Executive Pack", styles['H2']))
    story.append(Paragraph("• <b>Advanced Excel Engine (.xlsx):</b> 4 interconnected worksheets with protected formulas, dynamic 10-factor quadrants, and native scatter quadrant charting.", styles['Bullet']))
    story.append(Paragraph("• <b>C-Level Slide Deck (.pptx 16:9):</b> Widescreen board-ready presentation with Minto Action Titles, cross-impact heat maps, and a dedicated 'Board Decision Gateway' box.", styles['Bullet']))
    story.append(Paragraph("• <b>Official Methodology Guide (.pdf):</b> Mathematical proofs, full industrial case study, and tough Q&A protocol for C-Suite committee defense.", styles['Bullet']))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 2: THE QUALITATIVE SWOT FALLACY & MATHEMATICAL RIGOR
    # --------------------------------------------------------------------------
    story.append(Paragraph("1. The Qualitative SWOT Fallacy in the Boardroom", styles['H1']))
    story.append(Paragraph(
        "Standard whiteboard SWOT matrices suffer from three systemic failure modes that destroy executive credibility:",
        styles['Body']
    ))
    story.append(Paragraph("<b>1. Typographical Equivalence Paradox:</b> A minor operational strength ('friendly team culture') occupies identical slide real estate as a decisive moat ('18% superior gross margin'), corrupting resource allocation.", styles['Bullet']))
    story.append(Paragraph("<b>2. Rhetoric & HiPPO Bias:</b> Debates are won by the most articulate executive or the Highest Paid Person's Opinion (HiPPO), rather than empirical operational evidence.", styles['Bullet']))
    story.append(Paragraph("<b>3. Zero P&L Connectivity:</b> The matrix produces no capital requirements or expected returns, rendering it an academic exercise with zero accountability.", styles['Bullet']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Mathematical Formulation of the Strategic Vector Space", styles['H1']))
    story.append(Paragraph(
        "To eliminate subjective distortion, we model each quadrant k \u2208 {S, W, O, T} as a weight vector w\u2096 and an impact vector c\u2096 in \u211d\u207f:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "w_k = [w_{k,1}, w_{k,2}, ..., w_{k,n}]^T, \u2200 w_{k,i} \u2208 [0, 1] \u2227 \u2211_{i=1}^n w_{k,i} = 1.00<br/>"
        "c_k = [c_{k,1}, c_{k,2}, ..., c_{k,n}]^T, \u2200 c_{k,i} \u2208 {1, 2, 3, 4, 5}<br/>"
        "S_k = w_k \u00b7 c_k = \u2211_{i=1}^n (w_{k,i} \u00b7 c_{k,i})",
        styles
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Where <b>S_k</b> represents the composite weighted quadrant score. We then define the <b>Cartesian Strategic Vector V</b> in \u211d\u00b2:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "X = S_S - S_W \u2208 [-4.0, +4.0]  (Net Internal Position)<br/>"
        "Y = S_O - S_T \u2208 [-4.0, +4.0]  (Net External Pressure)<br/>"
        "\u2192 V = (X, Y) = (S_S - S_W) \u00ee + (S_O - S_T) \u0135<br/>"
        "||V|| = \u221a(X\u00b2 + Y\u00b2)  (Strategic Momentum Magnitude)",
        styles
    ))
    story.append(Spacer(1, 8))

    # English Quadrant Table
    q_en_table = [
        [Paragraph("<b>Quadrant</b>", styles['TableHead']), Paragraph("<b>Coordinates</b>", styles['TableHead']), Paragraph("<b>Dominant Posture</b>", styles['TableHead']), Paragraph("<b>Executive Boardroom Mandate</b>", styles['TableHead'])],
        [Paragraph("<b>I (Top Right)</b>", styles['TableCellBold']), Paragraph("X \u2265 0, Y \u2265 0", styles['TableCell']), Paragraph("<b>OFFENSIVE (Maxi-Maxi)</b>", styles['TableCellBold']), Paragraph("Direct maximum capital to market capture, R&D scaling, and aggressive expansion.", styles['TableCell'])],
        [Paragraph("<b>II (Top Left)</b>", styles['TableCellBold']), Paragraph("X < 0, Y \u2265 0", styles['TableCell']), Paragraph("<b>REORIENTATION (Mini-Maxi)</b>", styles['TableCellBold']), Paragraph("Eliminate internal operational bottlenecks to unlock market tailwinds.", styles['TableCell'])],
        [Paragraph("<b>III (Bottom Left)</b>", styles['TableCellBold']), Paragraph("X < 0, Y < 0", styles['TableCell']), Paragraph("<b>SURVIVAL (Mini-Mini)</b>", styles['TableCellBold']), Paragraph("Enforce cost containment, divest non-core assets, and preserve liquidity.", styles['TableCell'])],
        [Paragraph("<b>IV (Bottom Right)</b>", styles['TableCellBold']), Paragraph("X \u2265 0, Y < 0", styles['TableCell']), Paragraph("<b>DEFENSIVE (Maxi-Mini)</b>", styles['TableCellBold']), Paragraph("Leverage internal IP and margin fortress to hedge external market risks.", styles['TableCell'])],
    ]
    t_q_en = Table(q_en_table, colWidths=[85, 85, 135, 206])
    t_q_en.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_q_en)

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 3: THE TOWS CROSS-IMPACT ALGORITHM
    # --------------------------------------------------------------------------
    story.append(Paragraph("3. The TOWS Cross-Impact Algorithm", styles['H1']))
    story.append(Paragraph(
        "Quantitative SWOT locates the company's position, but the <b>TOWS Cross-Impact Matrix</b> translates that position into capital allocation. "
        "By systematically evaluating intersections between internal strengths/weaknesses and external opportunities/threats, we construct an impact matrix M:",
        styles['Body']
    ))

    story.append(build_equation_box(
        "M_{cross} \u2208 {0, 1, 2, 3}^{m \u00d7 n}<br/>"
        "0 = No relationship | 1 = Low Impact | 2 = Moderate Synergy | 3 = Critical Catalyst / Acute Threat",
        styles
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("The Four Operational Strategic Tracks", styles['H2']))
    story.append(Paragraph("<b>1. Maxi-Maxi (SO - Offensive Scaling):</b> How do internal capabilities aggressively exploit emerging market spaces? "
                           "Prioritizes high-NPV capital deployment and strategic channel partnerships.", styles['Body']))
    story.append(Paragraph("<b>2. Maxi-Mini (ST - Defensive Moats):</b> How do core strengths protect enterprise value from external market threats? "
                           "Focuses on multi-year contract lock-ins, patent litigation defense, and regulatory compliance moats.", styles['Body']))
    story.append(Paragraph("<b>3. Mini-Maxi (WO - Operational Turnaround):</b> How do external tailwinds finance the removal of internal operational bottlenecks? "
                           "Targets technical debt refactoring, ERP modernizations, and sales velocity improvements.", styles['Body']))
    story.append(Paragraph("<b>4. Mini-Mini (WT - Survival & Risk Hedging):</b> How does the enterprise de-risk acute internal vulnerabilities exposed to lethal external threats? "
                           "Mandates supplier diversification and debt restructuring.", styles['Body']))
    story.append(Spacer(1, 6))

    # TOWS Governance Table
    tows_gov_data = [
        [Paragraph("<b>TOWS Track</b>", styles['TableHead']), Paragraph("<b>Focus Area</b>", styles['TableHead']), Paragraph("<b>Board Approval Gateway</b>", styles['TableHead']), Paragraph("<b>Primary P&L Target</b>", styles['TableHead'])],
        [Paragraph("<b>SO (Maxi-Maxi)</b>", styles['TableCellBold']), Paragraph("Aggressive Scaling", styles['TableCell']), Paragraph("Positive NPV, ARR acceleration, payback < 14 months.", styles['TableCell']), Paragraph("Net New ARR, Enterprise Logo Growth.", styles['TableCell'])],
        [Paragraph("<b>ST (Maxi-Mini)</b>", styles['TableCellBold']), Paragraph("Moat Preservation", styles['TableCell']), Paragraph("Risk reduction on assets generating > 15% EBITDA.", styles['TableCell']), Paragraph("Gross Margin Protection, Churn < 1.5%.", styles['TableCell'])],
        [Paragraph("<b>WO (Mini-Maxi)</b>", styles['TableCellBold']), Paragraph("Turnaround", styles['TableCell']), Paragraph("Bottleneck removal with verified operational ROI.", styles['TableCell']), Paragraph("Sales Cycle Compression, Dev Velocity.", styles['TableCell'])],
        [Paragraph("<b>WT (Mini-Mini)</b>", styles['TableCellBold']), Paragraph("Solvency Defense", styles['TableCell']), Paragraph("Loss mitigation on existential business dependencies.", styles['TableCell']), Paragraph("Single-Client Risk < 25%, OPEX Cut.", styles['TableCell'])],
    ]
    t_tows_gov = Table(tows_gov_data, colWidths=[95, 95, 180, 141])
    t_tows_gov.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_MED),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_tows_gov)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Initiative Governance Protocol", styles['H2']))
    story.append(Paragraph(
        "Every TOWS initiative submitted to the Board requires four mandatory governance attributes: "
        "(1) a single <b>Accountable C-Level Owner</b>, (2) an explicit quarterly execution window (Q1-Q4), "
        "(3) formal capital partitioning into <b>CAPEX and OPEX</b>, and (4) an auditable target P&L metric.",
        styles['Body']
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 4: FULL INTERNATIONAL INDUSTRIAL CASE STUDY
    # --------------------------------------------------------------------------
    story.append(Paragraph("4. Industrial Case Study: Apex Precision Engineering Inc.", styles['H1']))
    story.append(Paragraph(
        "<b>Company Profile:</b> B2B specialized industrial software and components manufacturer with $52M annual turnover and 220 employees. "
        "Facing AI-driven automation disruptions, Asian price erosion, and capital grant opportunities for smart manufacturing.",
        styles['Body']
    ))

    # Case Data Table
    case_en_data = [
        [Paragraph("<b>Quadrant</b>", styles['TableHead']), Paragraph("<b>Evaluated Strategic Baseline Factors</b>", styles['TableHead']), Paragraph("<b>Weight w</b>", styles['TableHead']), Paragraph("<b>Rating c</b>", styles['TableHead']), Paragraph("<b>Score S</b>", styles['TableHead'])],
        [Paragraph("<b>Strengths (S)</b>", styles['TableCellBold']), Paragraph("Gross margin fortress (+18.4%), 3 granted patents, NRR 118%, ISO/SOC2.", styles['TableCell']), Paragraph("100%", styles['TableCell']), Paragraph("4.6 / 5", styles['TableCell']), Paragraph("<b>4.35</b>", styles['TableCellBold'])],
        [Paragraph("<b>Weaknesses (W)</b>", styles['TableCellBold']), Paragraph("High concentration (42% in 2 logos), 8.5-month deal cycle, hardware debt.", styles['TableCell']), Paragraph("100%", styles['TableCell']), Paragraph("3.4 / 5", styles['TableCell']), Paragraph("<b>2.25</b>", styles['TableCellBold'])],
        [Paragraph("<b>Opportunities (O)</b>", styles['TableCellBold']), Paragraph("Smart factory subsidies, EU AI Act compliance demand, LatAm channel.", styles['TableCell']), Paragraph("100%", styles['TableCell']), Paragraph("4.5 / 5", styles['TableCell']), Paragraph("<b>4.20</b>", styles['TableCellBold'])],
        [Paragraph("<b>Threats (T)</b>", styles['TableCellBold']), Paragraph("Asian price discounting (-35%), AI engineer wage inflation, tariff risks.", styles['TableCell']), Paragraph("100%", styles['TableCell']), Paragraph("3.2 / 5", styles['TableCell']), Paragraph("<b>2.35</b>", styles['TableCellBold'])],
    ]
    t_case_en = Table(case_en_data, colWidths=[90, 241, 55, 60, 65])
    t_case_en.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_case_en)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Mathematical Resolution & Vector Orientation", styles['H2']))
    story.append(Paragraph(
        "• <b>Net Internal Position:</b> X = S_S - S_W = 4.35 - 2.25 = <b>+2.10</b> (Internal moats comfortably surpass operational debt).<br/>"
        "• <b>Net External Pressure:</b> Y = S_O - S_T = 4.20 - 2.35 = <b>+1.85</b> (Macro tailwinds significantly outweigh headwinds).<br/>"
        "• <b>Strategic Vector:</b> V = (+2.10, +1.85) \u2192 <b>Dominant OFFENSIVE / EXPANSION Posture (Maxi-Maxi)</b> with magnitude ||V|| = 2.80 pts.",
        styles['Body']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Boardroom Capital Allocation Roadmap", styles['H2']))
    act_en_data = [
        [Paragraph("<b>ID</b>", styles['TableHead']), Paragraph("<b>Strategic Initiative & Scope</b>", styles['TableHead']), Paragraph("<b>Owner</b>", styles['TableHead']), Paragraph("<b>Target</b>", styles['TableHead']), Paragraph("<b>Budget</b>", styles['TableHead']), Paragraph("<b>Target KPI</b>", styles['TableHead'])],
        [Paragraph("<b>TOWS-O01</b>", styles['TableCellBold']), Paragraph("Subsidized Industrial SaaS module across 40 plants", styles['TableCell']), Paragraph("COO", styles['TableCell']), Paragraph("Q1-Q3", styles['TableCell']), Paragraph("€105,000", styles['TableCell']), Paragraph("+€1.2M ARR", styles['TableCell'])],
        [Paragraph("<b>TOWS-W01</b>", styles['TableCellBold']), Paragraph("LatAm distributor channel to de-risk client concentration", styles['TableCell']), Paragraph("CCO", styles['TableCell']), Paragraph("Q2-Q4", styles['TableCell']), Paragraph("€105,000", styles['TableCell']), Paragraph("Top-2 < 25% ARR", styles['TableCell'])],
        [Paragraph("<b>TOWS-T01</b>", styles['TableCellBold']), Paragraph("Multi-year enterprise contract lock-ins with top accounts", styles['TableCell']), Paragraph("CEO", styles['TableCell']), Paragraph("Q1-Q2", styles['TableCell']), Paragraph("€30,000", styles['TableCell']), Paragraph("Logo Churn < 1.5%", styles['TableCell'])],
        [Paragraph("<b>TOWS-S02</b>", styles['TableCellBold']), Paragraph("Senior AI engineering phantom equity & retention plan", styles['TableCell']), Paragraph("CPO", styles['TableCell']), Paragraph("Q1-Q4", styles['TableCell']), Paragraph("€45,000", styles['TableCell']), Paragraph("R&D Churn < 3%", styles['TableCell'])],
    ]
    t_act_en = Table(act_en_data, colWidths=[55, 176, 50, 45, 75, 110])
    t_act_en.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_MED),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_act_en)
    story.append(Spacer(1, 8))

    story.append(build_callout(
        "<b>Boardroom Resolution:</b> The Board authorized the full €245,000 allocation (€140k CAPEX / €105k OPEX) "
        "after verifying that the single-client vulnerability was actively neutralized while capturing €1.2M in high-margin SaaS ARR.",
        styles, border_color=C_TEAL_ACCENT, bg_color=colors.HexColor("#ECFDF5")
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 5: BOARDROOM DEFENSE PROTOCOL (C-LEVEL FAQ)
    # --------------------------------------------------------------------------
    story.append(Paragraph("5. Boardroom Defense Protocol (C-Level FAQ)", styles['H1']))
    story.append(Paragraph(
        "Prescribed methodological responses for handling tough executive committee inquiries:",
        styles['Body']
    ))

    story.append(Paragraph("How do we prove relative weight assignments are not subjective? (Chief Financial Officer)", styles['FAQ_Q']))
    story.append(Paragraph(
        "<b>Defense:</b> Relative weights (w\u1d62) are anchored to empirical financial audits rather than subjective perception. "
        "For example, the operational margin factor weight is linked directly to EBITDA performance. Furthermore, our Excel model "
        "includes a Monte Carlo sensitivity stress-test demonstrating that a \u00b115% shift across factor weights does not alter "
        "the dominant offensive strategic posture.",
        styles['FAQ_A']
    ))

    story.append(Paragraph("What if the Board insists on an Offensive posture when data dictates Survival? (Chief Executive Officer)", styles['FAQ_Q']))
    story.append(Paragraph(
        "<b>Defense:</b> The mathematical model enforces objective reality testing. If vector V lies in the Survival quadrant "
        "(X < 0, Y < 0), aggressive capital expansion dramatically elevates enterprise insolvency risk. Methodological governance "
        "dictates that turnaround initiatives must first lift net internal position (X) into positive territory before offensive growth capital can be unlocked.",
        styles['FAQ_A']
    ))

    story.append(Paragraph("How do we prevent departmental heads from inflating their ratings? (Chief Operating Officer)", styles['FAQ_Q']))
    story.append(Paragraph(
        "<b>Defense:</b> Quantitative SWOT enforces a strict evidentiary standard: no impact rating c\u1d62 \u2265 4 may be submitted "
        "without auditable empirical documentation in the 'Baseline Metric' column. Claims of customer loyalty require auditable NRR > 110% "
        "or churn < 2.5%; unverified qualitative claims are capped at a maximum rating of 3.",
        styles['FAQ_A']
    ))

    story.append(Paragraph("How frequently should this matrix be recalculated? (Chief Risk Officer)", styles['FAQ_Q']))
    story.append(Paragraph(
        "<b>Defense:</b> A dual-cadence governance model is standard: (1) <b>Quarterly Light Reviews</b> to audit TOWS initiative "
        "milestones and re-plot the vector against macro shifts; and (2) <b>Full Annual Recalculation</b> during formal capital allocation "
        "and budgeting in Q3-Q4.",
        styles['FAQ_A']
    ))
    story.append(Spacer(1, 10))

    story.append(build_callout(
        "<b>Datalaria Official Certification:</b> This Executive Decision Pack conforms to Tier-1 management consulting standards. "
        "For corporate advisory, custom model adaptation, or executive workshop facilitation, contact <b>advisory@datalaria.com</b>.",
        styles, border_color=C_NAVY_DARK, bg_color=C_BG_CARD
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK EN] PDF generated: {out_path} ({os.path.getsize(out_path)} bytes)")


def main():
    generate_pdf_es("static/downloads/dafo-came-es/Guia_Metodologica_DAFO_CAME_ES.pdf")
    generate_pdf_en("static/downloads/swot-tows-en/Methodology_Guide_SWOT_TOWS_EN.pdf")


if __name__ == '__main__':
    main()
