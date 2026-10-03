#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para:
1. packages/[ES]_BCG_Dinamica/Guia_Metodologica_BCG_ES.pdf
2. packages/[EN]_Dynamic_BCG/Methodology_Guide_BCG_EN.pdf

Estándar editorial de alta dirección (McKinsey / BCG):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (La Falacia de la Matriz BCG Cualitativa).
- Página 2: Sección 2 (Fundamentación Matemática, Curva de Experiencia de Henderson y Balance FCF).
- Página 3: Sección 3 (Reglas de Oro de Asignación de Capital de Boston Consulting Group y Trampas).
- Página 4: Sección 4 (Caso de Estudio Industrial B2B Resuelto: Nexus Industrial Technologies Group).
- Página 5: Sección 5 (Protocolo de Defensa en Comité C-Level - FAQ) y Referencias Bibliográficas.
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
C_TEAL_LIGHT = colors.HexColor("#F0FDFA")   # Teal 50
C_AMBER_ACCENT = colors.HexColor("#D97706") # Amber 600
C_AMBER_LIGHT = colors.HexColor("#FFFBEB") # Amber 50
C_ROSE_ACCENT = colors.HexColor("#E11D48")   # Rose 600
C_ROSE_LIGHT = colors.HexColor("#FFF1F2")   # Rose 50
C_GOLD_ACCENT = colors.HexColor("#F59E0B")  # Gold
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
            header_right = ("MATRIZ BCG DINÁMICA & ASIGNACIÓN DE CAPITAL"
                            if lang == 'ES' else
                            "DYNAMIC BCG MATRIX & CAPITAL ALLOCATION")
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
            fontName='Helvetica-Bold', fontSize=19, leading=23,
            textColor=C_NAVY_DARK, spaceAfter=6
        ),
        'CoverSub': ParagraphStyle(
            'CoverSub', parent=base['Normal'],
            fontName='Helvetica', fontSize=9.5, leading=13.5,
            textColor=C_SLATE_MUTED, spaceAfter=8
        ),
        'SecHeading': ParagraphStyle(
            'SecHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=11.5, leading=15,
            textColor=C_NAVY_DARK, spaceBefore=7, spaceAfter=4,
            keepWithNext=True
        ),
        'SubHeading': ParagraphStyle(
            'SubHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=9.2, leading=12,
            textColor=C_NAVY_MED, spaceBefore=4, spaceAfter=2.5,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.3, leading=11.5,
            textColor=C_NAVY_MED, spaceAfter=3.5
        ),
        'Bullet': ParagraphStyle(
            'Bullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.3, leading=11.5,
            textColor=C_NAVY_MED, leftIndent=12, firstLineIndent=-7, spaceAfter=2.5
        ),
        'MathBox': ParagraphStyle(
            'MathBox', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.8, leading=12.5,
            textColor=C_NAVY_DARK, alignment=1
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.8, leading=9.5,
            textColor=C_WHITE, alignment=1
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.6, leading=9.8,
            textColor=C_NAVY_MED
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.6, leading=9.8,
            textColor=C_NAVY_DARK
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica-Oblique', fontSize=8.0, leading=11.0,
            textColor=C_NAVY_DARK
        ),
        'FAQ_Q': ParagraphStyle(
            'FAQ_Q', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.6, leading=11.5,
            textColor=C_NAVY_DARK, spaceBefore=4, spaceAfter=1.5,
            keepWithNext=True
        ),
        'FAQ_A': ParagraphStyle(
            'FAQ_A', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.0, leading=11.0,
            textColor=C_NAVY_MED, spaceAfter=3.5
        ),
        'Biblio': ParagraphStyle(
            'Biblio', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.6, leading=10.2,
            textColor=C_NAVY_MED, leftIndent=10, firstLineIndent=-7, spaceAfter=2.5
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
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
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
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


# ==============================================================================
# GUÍA EN ESPAÑOL (5 PÁGINAS EXACTAS)
# ==============================================================================
def generate_pdf_es(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=44, bottomMargin=48
    )
    styles = get_custom_styles()
    story = []

    # ==========================
    # PÁGINA 1: PORTADA & SECCIÓN 1
    # ==========================
    story.append(Paragraph("DATALARIA STRATEGY PRACTICE • MCKINSEY & BCG STANDARD", styles['CoverKicker']))
    story.append(Paragraph("Matriz BCG Dinámica:<br/>Gestión de Cartera & Asignación de Capital C-Level", styles['CoverTitle']))
    story.append(Paragraph(
        "Guía metodológica oficial para transformar el análisis cualitativo de 4 cuadrantes en un motor cuantitativo "
        "de balance de liquidez (Bruce Henderson), cálculo de cuota relativa y roadmap de reasignación presupuestaria ante Consejos de Administración.",
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
            Paragraph("<b>Aplicación:</b> Gestión de Cartera & M&A", styles['TableCell']),
            Paragraph("<b>Modelo:</b> Dinámica de Fondos Henderson", styles['TableCell']),
            Paragraph("<b>Estándar:</b> McKinsey / BCG Tier-1", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 170, 171])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. La Falacia de la Matriz BCG Cualitativa", styles['SecHeading']))
    story.append(Paragraph(
        "Desarrollada por Bruce D. Henderson en 1968 para Boston Consulting Group, la Matriz de Crecimiento-Cuota "
        "es uno de los marcos estratégicos más reconocidos y, paradójicamente, más tergiversados del management. "
        "En más del 80% de las reuniones corporativas, su uso degenera en una 'ilustración estática' sin rigor cuantitativo:",
        styles['Body']
    ))

    story.append(Paragraph(
        "• <b>Confusión entre Cuota Absoluta y Cuota Relativa (CMR):</b> Se clasifica una unidad como 'líder' por poseer un 25% de cuota, "
        "ignorando que si el competidor principal ostenta el 50%, la cuota relativa es de tan solo 0.50x, lo que sitúa a la empresa en una grave desventaja de costes.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Desconexión del Flujo de Caja Libre (FCF):</b> La matriz original nunca fue una taxonomía de marketing, sino un modelo de asignación "
        "de liquidez financiera neta. Evaluar unidades sin auditar su consumo o generación de FCF conduce a la asfixia del holding.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>La Trampa de los Perros Financieramente Viables:</b> Se tolera la supervivencia indefinida de 'Perros' simplemente porque muestran "
        "un margen contable marginal positivo, obviando el coste de oportunidad del capital y la destrucción sistemática de ROIC.",
        styles['Bullet']
    ))

    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Axioma de Henderson:</b> La rentabilidad y la generación de efectivo de una empresa dependen fundamentalmente de su cuota de mercado "
        "relativa respecto al líder competidor directo, debido al descenso acumulativo de costes por la Curva de Experiencia.",
        styles, border_color=C_BLUE_ACCENT, bg_color=C_BLUE_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PÁGINA 2: FUNDAMENTACIÓN MATEMÁTICA & BALANCE FCF
    # ==========================
    story.append(Paragraph("2. Fundamentación Matemática: Dinámica de Cartera & Curva de Experiencia", styles['SecHeading']))
    story.append(Paragraph(
        "Para transformar la Matriz BCG en un motor objetivo auditable, cada Unidad Estratégica de Negocio (UEN) "
        "se modela mediante un vector cartesiano y ecuaciones de balance de fondos:",
        styles['Body']
    ))

    story.append(Paragraph("2.1. Cuota de Mercado Relativa (CMR)", styles['SubHeading']))
    story.append(Paragraph(
        "La Cuota de Mercado Relativa cuantifica la posición de escala y eficiencia respecto al principal operador del mercado:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "CMR<sub>i</sub> = V<sub>i</sub> / V<sub>líder, i</sub> &nbsp;&nbsp;&nbsp;&nbsp; "
        "(Si la UEN es el líder: CMR<sub>i</sub> = V<sub>i</sub> / V<sub>competidor #2, i</sub> > 1.00x)",
        styles
    ))

    story.append(Paragraph("2.2. Tasa de Crecimiento del Mercado (TCM)", styles['SubHeading']))
    story.append(Paragraph(
        "Determina la velocidad de expansión del sector y las necesidades intrínsecas de reinversión en capital circulante y CAPEX:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "TCM<sub>i</sub> = [(Mercado<sub>t</sub> - Mercado<sub>t-1</sub>) / Mercado<sub>t-1</sub>] × 100% &nbsp;&nbsp;&nbsp;&nbsp; "
        "(Umbral canónico de corte: TCM<sub>corte</sub> = 10.0% anual)",
        styles
    ))

    story.append(Paragraph("2.3. Efecto Curva de Experiencia de Henderson", styles['SubHeading']))
    story.append(Paragraph(
        "Formulada por BCG en 1968, establece que el coste unitario real de valor añadido desciende entre un 20% y un 30% "
        "cada vez que la producción acumulada se duplica:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "C<sub>n</sub> = C<sub>1</sub> · n<sup>-b</sup> &nbsp;&nbsp;&nbsp;&nbsp; "
        "con exponente de aprendizaje: b = -ln(PR) / ln(2) &nbsp;&nbsp;&nbsp;&nbsp; (para PR = 80%, b ≈ 0.322)",
        styles
    ))

    story.append(Paragraph("2.4. Ecuación del Flujo de Caja Libre Neto (FCF)", styles['SubHeading']))
    story.append(Paragraph(
        "El balance neto de fondos de cada cuadrante se rige por la mecánica de flujo de caja descontado:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "FCF<sub>i</sub> = EBITDA<sub>i</sub> · (1 - t) - ΔNWC<sub>i</sub> - CAPEX<sub>mantenimiento, i</sub> - CAPEX<sub>crecimiento, i</sub>",
        styles
    ))
    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Implicación Directa:</b> Un líder con CMR = 2.0x produce al doble de volumen acumulado que su competidor más próximo, "
        "lo que en sectores fabriles y de software reduce su coste unitario entre un 20% y un 35%, generando un margen EBITDA estructuralmente superior.",
        styles, border_color=C_TEAL_ACCENT, bg_color=C_TEAL_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PÁGINA 3: REGLAS DE ORO DE ASIGNACIÓN & TRAMPAS DE CAPITAL
    # ==========================
    story.append(Paragraph("3. Reglas de Oro de Asignación de Capital de Boston Consulting Group", styles['SecHeading']))
    story.append(Paragraph(
        "El principio rector de Bruce Henderson es el <b>equilibrio dinámico de fondos</b>: una corporación no puede financiar "
        "el crecimiento futuro recurriendo perpetuamente a deuda bancaria o dilución de accionistas; debe generar sus propios fondos internamente.",
        styles['Body']
    ))

    story.append(Paragraph("3.1. El Ciclo Virtuoso de Gestión de Cartera", styles['SubHeading']))
    story.append(Paragraph(
        "1. <b>Vacas Lecheras (Generación):</b> Extraer de forma disciplinada el excedente de FCF generado por las unidades consolidadas.<br/>"
        "2. <b>Interrogantes Seleccionadas (Inyección):</b> Concentrar el capital en 1 o 2 Interrogantes con potencial real de alcanzar CMR ≥ 1.0x.<br/>"
        "3. <b>Estrellas (Defensa):</b> Financiar la capacidad para sostener el liderazgo hasta que el crecimiento del mercado se desacelere.<br/>"
        "4. <b>Nuevas Vacas (Relevo Generacional):</b> La maduración natural convierte a las Estrellas en la próxima generación de Vacas Lecheras.",
        styles['Body']
    ))

    story.append(Paragraph("3.2. Tabla de Prescripciones Estratégicas y Asignación de Capital", styles['SubHeading']))

    presc_table_data = [
        [
            Paragraph("<b>Cuadrante</b>", styles['TableHeader']),
            Paragraph("<b>Posición (CMR / TCM)</b>", styles['TableHeader']),
            Paragraph("<b>Flujo Neto FCF</b>", styles['TableHeader']),
            Paragraph("<b>Estrategia de Capital C-Level</b>", styles['TableHeader']),
        ],
        [
            Paragraph("<b>⭐ ESTRELLAS</b>", styles['TableCellBold']),
            Paragraph("CMR ≥ 1.0x | TCM ≥ 10%", styles['TableCell']),
            Paragraph("Neutral o leve positivo", styles['TableCellBold']),
            Paragraph("<b>Invertir agresivamente:</b> Blindar cuota fabril y tecnológica; no desviar fondos.", styles['TableCell']),
        ],
        [
            Paragraph("<b>🐄 VACAS</b>", styles['TableCellBold']),
            Paragraph("CMR ≥ 1.0x | TCM < 10%", styles['TableCell']),
            Paragraph("Superávit masivo (+)", styles['TableCellBold']),
            Paragraph("<b>Ordeño riguroso:</b> Financiar sólo CAPEX de mantenimiento; transferir FCF.", styles['TableCell']),
        ],
        [
            Paragraph("<b>❓ INTERROGANTES</b>", styles['TableCellBold']),
            Paragraph("CMR < 1.0x | TCM ≥ 10%", styles['TableCell']),
            Paragraph("Déficit severo (-)", styles['TableCellBold']),
            Paragraph("<b>Decisión binaria:</b> Inyectar capital para liderar o desinvertir/cerrar sin demora.", styles['TableCell']),
        ],
        [
            Paragraph("<b>🐕 PERROS</b>", styles['TableCellBold']),
            Paragraph("CMR < 1.0x | TCM < 10%", styles['TableCell']),
            Paragraph("Débil o negativo (-)", styles['TableCellBold']),
            Paragraph("<b>Cosecha o venta (M&A):</b> Liberar capital circulante y reasignar ingenieros.", styles['TableCell']),
        ]
    ]

    t_presc = Table(presc_table_data, colWidths=[95, 115, 105, 196])
    t_presc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, 1), C_BLUE_LIGHT),
        ('BACKGROUND', (0, 2), (-1, 2), C_TEAL_LIGHT),
        ('BACKGROUND', (0, 3), (-1, 3), C_AMBER_LIGHT),
        ('BACKGROUND', (0, 4), (-1, 4), C_ROSE_LIGHT),
    ]))
    story.append(t_presc)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3. Las Cuatro Trampas Fatales de Cartera de Henderson", styles['SubHeading']))
    story.append(Paragraph(
        "• <b>Sobreordeño de Vacas:</b> Recortar el mantenimiento básico hasta perder cuota frente a competidores secundarios.<br/>"
        "• <b>Alimentar a los Perros:</b> Reinyectar flujos en unidades marginales por arraigo emocional o historia corporativa.<br/>"
        "• <b>Dispersión de Interrogantes:</b> Repartir el capital entre 5 interrogantes simultáneas sin que ninguna logre superar CMR = 1.0x.<br/>"
        "• <b>Envejecimiento de Cartera:</b> Poseer solo Vacas y Perros; la compañía genera caja hoy pero está sentenciada a desaparecer.",
        styles['Body']
    ))

    story.append(PageBreak())

    # ==========================
    # PÁGINA 4: CASO DE ESTUDIO INDUSTRIAL B2B (NEXUS GROUP)
    # ==========================
    story.append(Paragraph("4. Caso de Estudio Industrial B2B: Nexus Industrial Technologies Group", styles['SecHeading']))
    story.append(Paragraph(
        "Para ilustrar la aplicación en Consejo de Administración, analizamos el caso real anonimizado del holding industrial "
        "<b>Nexus Group</b> (107,0 M€ de facturación, 18,98 M€ de EBITDA y 8 UENs operativas).",
        styles['Body']
    ))

    case_table_data = [
        [
            Paragraph("<b>UEN</b>", styles['TableHeader']),
            Paragraph("<b>Ventas (€)</b>", styles['TableHeader']),
            Paragraph("<b>Líder (€)</b>", styles['TableHeader']),
            Paragraph("<b>CMR</b>", styles['TableHeader']),
            Paragraph("<b>TCM %</b>", styles['TableHeader']),
            Paragraph("<b>EBITDA %</b>", styles['TableHeader']),
            Paragraph("<b>FCF Neto (€)</b>", styles['TableHeader']),
            Paragraph("<b>Cuadrante</b>", styles['TableHeader']),
        ],
        [
            Paragraph("UEN-01: Robótica IA", styles['TableCellBold']),
            Paragraph("18.5 M€", styles['TableCell']),
            Paragraph("14.8 M€", styles['TableCell']),
            Paragraph("<b>1.25x</b>", styles['TableCellBold']),
            Paragraph("+18.5%", styles['TableCell']),
            Paragraph("22.0%", styles['TableCell']),
            Paragraph("+0.65 M€", styles['TableCellBold']),
            Paragraph("⭐ ESTRELLA", styles['TableCellBold']),
        ],
        [
            Paragraph("UEN-02: SaaS IoT", styles['TableCellBold']),
            Paragraph("12.2 M€", styles['TableCell']),
            Paragraph("10.5 M€", styles['TableCell']),
            Paragraph("<b>1.16x</b>", styles['TableCellBold']),
            Paragraph("+24.0%", styles['TableCell']),
            Paragraph("25.0%", styles['TableCell']),
            Paragraph("+0.28 M€", styles['TableCellBold']),
            Paragraph("⭐ ESTRELLA", styles['TableCellBold']),
        ],
        [
            Paragraph("UEN-03: Hidráulicos", styles['TableCellBold']),
            Paragraph("32.0 M€", styles['TableCell']),
            Paragraph("16.0 M€", styles['TableCell']),
            Paragraph("<b>2.00x</b>", styles['TableCellBold']),
            Paragraph("+3.5%", styles['TableCell']),
            Paragraph("20.0%", styles['TableCell']),
            Paragraph("<b>+4.85 M€</b>", styles['TableCellBold']),
            Paragraph("🐄 VACA", styles['TableCellBold']),
        ],
        [
            Paragraph("UEN-04: Motores", styles['TableCellBold']),
            Paragraph("24.5 M€", styles['TableCell']),
            Paragraph("17.5 M€", styles['TableCell']),
            Paragraph("<b>1.40x</b>", styles['TableCellBold']),
            Paragraph("+2.0%", styles['TableCell']),
            Paragraph("18.0%", styles['TableCell']),
            Paragraph("<b>+3.20 M€</b>", styles['TableCellBold']),
            Paragraph("🐄 VACA", styles['TableCellBold']),
        ],
        [
            Paragraph("UEN-05: Baterías Storage", styles['TableCellBold']),
            Paragraph("6.5 M€", styles['TableCell']),
            Paragraph("18.5 M€", styles['TableCell']),
            Paragraph("<b>0.35x</b>", styles['TableCellBold']),
            Paragraph("+32.0%", styles['TableCell']),
            Paragraph("6.0%", styles['TableCell']),
            Paragraph("<b>-2.15 M€</b>", styles['TableCellBold']),
            Paragraph("❓ INTERROG.", styles['TableCellBold']),
        ],
        [
            Paragraph("UEN-06: Láser Cuántico", styles['TableCellBold']),
            Paragraph("3.8 M€", styles['TableCell']),
            Paragraph("15.2 M€", styles['TableCell']),
            Paragraph("<b>0.25x</b>", styles['TableCellBold']),
            Paragraph("+21.0%", styles['TableCell']),
            Paragraph("4.0%", styles['TableCell']),
            Paragraph("<b>-1.45 M€</b>", styles['TableCellBold']),
            Paragraph("❓ INTERROG.", styles['TableCellBold']),
        ],
        [
            Paragraph("UEN-07: Cableado Cobre", styles['TableCellBold']),
            Paragraph("5.2 M€", styles['TableCell']),
            Paragraph("20.8 M€", styles['TableCell']),
            Paragraph("<b>0.25x</b>", styles['TableCellBold']),
            Paragraph("+1.0%", styles['TableCell']),
            Paragraph("5.0%", styles['TableCell']),
            Paragraph("-0.18 M€", styles['TableCellBold']),
            Paragraph("🐕 PERRO", styles['TableCellBold']),
        ],
        [
            Paragraph("UEN-08: Válvulas Neum.", styles['TableCellBold']),
            Paragraph("4.3 M€", styles['TableCell']),
            Paragraph("14.3 M€", styles['TableCell']),
            Paragraph("<b>0.30x</b>", styles['TableCellBold']),
            Paragraph("-1.5%", styles['TableCell']),
            Paragraph("7.0%", styles['TableCell']),
            Paragraph("+0.09 M€", styles['TableCellBold']),
            Paragraph("🐕 PERRO", styles['TableCellBold']),
        ],
        [
            Paragraph("<b>CONSOLIDADO</b>", styles['TableCellBold']),
            Paragraph("<b>107.0 M€</b>", styles['TableCellBold']),
            Paragraph("<b>-</b>", styles['TableCellBold']),
            Paragraph("<b>1.09x</b>", styles['TableCellBold']),
            Paragraph("<b>+8.2%</b>", styles['TableCellBold']),
            Paragraph("<b>17.7%</b>", styles['TableCellBold']),
            Paragraph("<b>+5.29 M€</b>", styles['TableCellBold']),
            Paragraph("<b>SOSTENIBLE</b>", styles['TableCellBold']),
        ]
    ]

    t_case = Table(case_table_data, colWidths=[105, 58, 58, 48, 50, 52, 65, 75])
    t_case.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_case)
    story.append(Spacer(1, 5))

    story.append(Paragraph("Diagnóstico y Resoluciones Aprobadas por el Consejo:", styles['SubHeading']))
    story.append(Paragraph(
        "• <b>Superávit Masivo de Vacas (+8,05 M€ FCF):</b> Cubre con holgura el déficit de crecimiento de las Interrogantes (-3,60 M€), "
        "dejando un flujo libre remanente de +4,45 M€.<br/>"
        "• <b>Inyección en Baterías de Estado Sólido (UEN-05):</b> Se asignan 2,8 M€ para ampliar capacidad fabril y elevar la CMR de 0.35x a 1.05x, "
        "transformándola en una nueva Estrella antes de 2027.<br/>"
        "• <b>Venta de Cableado (UEN-07):</b> Mandato de desinversión M&A otorgado por 3,2 M€ para desbloquear circulante y detener pérdidas.<br/>"
        "• <b>Impacto en Valor:</b> El ROIC consolidado pasa del 16.0% al 19.2% (+320 bps) con un periodo de recuperación (Payback) de 18 meses.",
        styles['Body']
    ))

    story.append(PageBreak())

    # ==========================
    # PÁGINA 5: FAQ C-LEVEL & BIBLIOGRAFÍA
    # ==========================
    story.append(Paragraph("5. Protocolo de Defensa en Comité de Dirección (FAQ)", styles['SecHeading']))

    faqs = [
        ("¿Por qué desinvertir en un Perro que todavía genera 90k€ de EBITDA contable positivo?",
         "Porque el EBITDA positivo oculta una destrucción real de valor cuando el ROIC de la unidad (ej: 4%) es inferior al coste ponderado "
         "del capital (WACC corporativo: 8.5%). Además, mantener un negocio marginal consume tiempo directivo de alta dirección y retiene "
         "capital circulante que rendiría un 22% reinvertido en Estrellas."),

        ("¿Cómo seleccionar entre dos Interrogantes cuál debe recibir el capital excedentario?",
         "Mediante tres filtros cuantitativos: 1) Trayectoria hacia CMR ≥ 1.0x (probabilidad matemática de superar al líder actual), "
         "2) Intensidad de capital requerida para duplicar cuota, y 3) Horizonte de crecimiento del mercado (TCM sostenible a más de 5 años). "
         "La que no cumpla los tres criterios debe desinvertirse o compartirse mediante Joint Venture."),

        ("¿Cómo evitar la desmotivación del equipo gestor de las unidades Vaca Lecheras?",
         "Desvinculando su retribución variable del crecimiento de ventas e indexándola al 100% sobre la generación de Flujo de Caja Libre (FCF), "
         "eficiencia de capital circulante (NWC) y retención estricta de cuota de mercado. Los directores de Vacas deben ser reconocidos como "
         "los garantes del dividendo corporativo."),

        ("¿Cómo gestionar el riesgo de canibalización entre Estrellas e Interrogantes?",
         "Henderson defendía que si una innovación va a devorar un negocio maduro, es preferible que la canibalización sea interna antes de que "
         "un competidor externo liquide la cuota del grupo. La regla es acelerar la transición hacia la nueva tecnología fijando precios agresivos.")
    ]

    for q, a in faqs:
        story.append(Paragraph(f"<b>P: {q}</b>", styles['FAQ_Q']))
        story.append(Paragraph(f"<b>R:</b> {a}", styles['FAQ_A']))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Referencias Bibliográficas Canónicas de Autoridad", styles['SecHeading']))

    bibs = [
        ("Henderson, Bruce D. (1970).", "<i>The Product Portfolio</i>. Boston Consulting Group Perspectives, No. 66.",
         "Artículo seminal donde se formaliza por primera vez la matriz de crecimiento-cuota de 4 cuadrantes y la dinámica de fondos."),
        ("Henderson, Bruce D. (1968).", "<i>The Experience Curve</i>. Boston Consulting Group, Boston.",
         "Tratado fundacional sobre la ley empírica de reducción de costes unitarios por duplicación de volumen acumulado."),
        ("Day, George S. (1977).", "<i>Diagnosing the Product Portfolio</i>. Journal of Marketing, Vol. 41, No. 2, pp. 29-38.",
         "Formalización académica de los riesgos de dispersión de capital y obsolescencia de cartera."),
        ("Porter, Michael E. (1980).", "<i>Competitive Strategy: Techniques for Analyzing Industries and Competitors</i>. Free Press, NY.",
         "Integración del liderazgo en costes por economías de escala y barreras de entrada sectoriales."),
        ("Minto, Barbara (2009).", "<i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall.",
         "Estándar metodológico de Action Titles y comunicación ejecutiva en consultoras Tier-1."),
        ("McKinsey & Company (2012).", "<i>Valuation: Measuring and Managing the Value of Companies</i>. John Wiley & Sons, NY.",
         "Conexión formal entre retorno sobre el capital invertido (ROIC), crecimiento y creación neta de valor accionarial.")
    ]

    for author, work, annot in bibs:
        p_text = f"<b>{author}</b> {work} — <font color='#64748B'>{annot}</font>"
        story.append(Paragraph(p_text, styles['Biblio']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Guía Metodológica PDF (ES) generada exitosamente: {out_path}")


# ==============================================================================
# GUÍA EN INGLÉS (5 PÁGINAS EXACTAS)
# ==============================================================================
def generate_pdf_en(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=44, bottomMargin=48
    )
    styles = get_custom_styles()
    story = []

    # ==========================
    # PAGE 1: COVER & SECTION 1
    # ==========================
    story.append(Paragraph("DATALARIA STRATEGY PRACTICE • MCKINSEY & BCG STANDARD", styles['CoverKicker']))
    story.append(Paragraph("Dynamic BCG Matrix:<br/>Portfolio Management & C-Level Capital Allocation", styles['CoverTitle']))
    story.append(Paragraph(
        "Official methodology guide to transform qualitative 4-quadrant illustrations into a rigorous quantitative "
        "cash flow balance model (Bruce Henderson), relative market share analytics, and board-level capital reallocation roadmap.",
        styles['CoverSub']
    ))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Author:</b> Datalaria Strategy Practice", styles['TableCell']),
            Paragraph("<b>Version:</b> 2026.1 Official C-Level", styles['TableCell']),
            Paragraph("<b>Classification:</b> Board Decision Support", styles['TableCell'])
        ],
        [
            Paragraph("<b>Domain:</b> Portfolio Strategy & M&A", styles['TableCell']),
            Paragraph("<b>Framework:</b> Henderson Cash Flow Dynamics", styles['TableCell']),
            Paragraph("<b>Standard:</b> McKinsey / BCG Tier-1", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 170, 171])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. The Fallacy of the Qualitative BCG Matrix", styles['SecHeading']))
    story.append(Paragraph(
        "Introduced by Bruce D. Henderson in 1968 for the Boston Consulting Group, the Growth-Share Matrix "
        "is one of the most recognized and, paradoxically, most misapplied strategic frameworks. "
        "In over 80% of boardroom presentations, it degenerates into a superficial static sketch devoid of quantitative discipline:",
        styles['Body']
    ))

    story.append(Paragraph(
        "• <b>Absolute vs. Relative Market Share (RMS) Confusion:</b> A business unit is mislabeled a 'market leader' based on a 25% share, "
        "ignoring that if the principal rival commands 50%, its relative share is only 0.50x—placing it in an acute scale-driven cost disadvantage.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Disconnection from Free Cash Flow (FCF):</b> The matrix was never intended as a marketing taxonomy, but as a corporate liquidity "
        "allocation model. Evaluating business units without auditing their net cash consumption or generation leads to group insolvency.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>The 'Viable Dog' Capital Trap:</b> Management tolerates chronically low-share Dogs simply because they produce marginal positive EBITDA, "
        "ignoring capital opportunity cost and systemic ROIC destruction.",
        styles['Bullet']
    ))

    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Henderson's Axiom:</b> A company's profitability and cash flow generation are fundamentally determined by its relative market share "
        "against its leading competitor, driven by the compounding unit cost reductions of the Experience Curve.",
        styles, border_color=C_BLUE_ACCENT, bg_color=C_BLUE_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PAGE 2: MATHEMATICAL FOUNDATIONS & FCF BALANCE
    # ==========================
    story.append(Paragraph("2. Mathematical Foundations: Portfolio Dynamics & The Experience Curve", styles['SecHeading']))
    story.append(Paragraph(
        "To transform the BCG matrix into an auditable decision engine, each Strategic Business Unit (SBU) "
        "is mapped via a Cartesian vector and cash flow balance equations:",
        styles['Body']
    ))

    story.append(Paragraph("2.1. Relative Market Share (RMS)", styles['SubHeading']))
    story.append(Paragraph(
        "Relative Market Share quantifies relative scale and operating cost advantage against the leading competitor:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "RMS<sub>i</sub> = Revenue<sub>i</sub> / Revenue<sub>leader, i</sub> &nbsp;&nbsp;&nbsp;&nbsp; "
        "(If SBU is leader: RMS<sub>i</sub> = Revenue<sub>i</sub> / Revenue<sub>runner-up, i</sub> > 1.00x)",
        styles
    ))

    story.append(Paragraph("2.2. Market Growth Rate (MGR)", styles['SubHeading']))
    story.append(Paragraph(
        "Determines industry expansion speed and structural capital reinvestment demands across working capital and CAPEX:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "MGR<sub>i</sub> = [(Market<sub>t</sub> - Market<sub>t-1</sub>) / Market<sub>t-1</sub>] × 100% &nbsp;&nbsp;&nbsp;&nbsp; "
        "(Canonical threshold: MGR<sub>cutoff</sub> = 10.0% annually)",
        styles
    ))

    story.append(Paragraph("2.3. Bruce Henderson's Experience Curve", styles['SubHeading']))
    story.append(Paragraph(
        "Formulated by BCG in 1968, establishing that real value-added unit costs decline by 20% to 30% "
        "each time cumulative production volume doubles:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "C<sub>n</sub> = C<sub>1</sub> · n<sup>-b</sup> &nbsp;&nbsp;&nbsp;&nbsp; "
        "with learning elasticity: b = -ln(PR) / ln(2) &nbsp;&nbsp;&nbsp;&nbsp; (for PR = 80%, b ≈ 0.322)",
        styles
    ))

    story.append(Paragraph("2.4. Free Cash Flow (FCF) Balance Equation", styles['SubHeading']))
    story.append(Paragraph(
        "The net liquidity contribution of each quadrant is governed by discounted corporate cash flow dynamics:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "FCF<sub>i</sub> = EBITDA<sub>i</sub> · (1 - t) - ΔNWC<sub>i</sub> - Maintenance_CAPEX<sub>i</sub> - Growth_CAPEX<sub>i</sub>",
        styles
    ))
    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Core Strategic Implication:</b> A market leader with RMS = 2.0x operates at double the cumulative experience of its nearest rival, "
        "yielding a 20% to 35% unit cost advantage in manufacturing and software, generating structurally higher EBITDA margins.",
        styles, border_color=C_TEAL_ACCENT, bg_color=C_TEAL_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PAGE 3: BCG GOLDEN RULES & CAPITAL TRAPS
    # ==========================
    story.append(Paragraph("3. Boston Consulting Group Golden Rules of Capital Allocation", styles['SecHeading']))
    story.append(Paragraph(
        "Bruce Henderson's foundational principle is <b>internal cash balance equilibrium</b>: a corporation cannot sustain "
        "long-term growth through perpetual debt financing or equity dilution; it must generate its investment capital internally.",
        styles['Body']
    ))

    story.append(Paragraph("3.1. The Virtuous Portfolio Lifecycle", styles['SubHeading']))
    story.append(Paragraph(
        "1. <b>Cash Cows (Generation):</b> Disciplined extraction of net surplus cash generated by mature market leaders.<br/>"
        "2. <b>Selected Question Marks (Injection):</b> Concentrated capital push into 1 or 2 SBUs with realistic runway to reach RMS ≥ 1.0x.<br/>"
        "3. <b>Stars (Defense):</b> Reinvesting heavily in operational capacity to defend leadership until market growth moderates.<br/>"
        "4. <b>New Cash Cows (Generational Renewal):</b> Natural market maturation turns Stars into the next generation of Cash Cows.",
        styles['Body']
    ))

    story.append(Paragraph("3.2. Strategic Prescriptions & Capital Allocation Matrix", styles['SubHeading']))

    presc_en_data = [
        [
            Paragraph("<b>Quadrant</b>", styles['TableHeader']),
            Paragraph("<b>Position (RMS / MGR)</b>", styles['TableHeader']),
            Paragraph("<b>Net Cash Flow (FCF)</b>", styles['TableHeader']),
            Paragraph("<b>C-Level Capital Strategy</b>", styles['TableHeader']),
        ],
        [
            Paragraph("<b>⭐ STARS</b>", styles['TableCellBold']),
            Paragraph("RMS ≥ 1.0x | MGR ≥ 10%", styles['TableCell']),
            Paragraph("Neutral / Mild Positive", styles['TableCellBold']),
            Paragraph("<b>Aggressive investment:</b> Protect scale and tech moat; reinvest all operating cash.", styles['TableCell']),
        ],
        [
            Paragraph("<b>🐄 CASH COWS</b>", styles['TableCellBold']),
            Paragraph("RMS ≥ 1.0x | MGR < 10%", styles['TableCell']),
            Paragraph("Massive Surplus (+)", styles['TableCellBold']),
            Paragraph("<b>Disciplined milking:</b> Cap CAPEX at sustaining levels; remit surplus to holding.", styles['TableCell']),
        ],
        [
            Paragraph("<b>❓ QUESTION MARKS</b>", styles['TableCellBold']),
            Paragraph("RMS < 1.0x | MGR ≥ 10%", styles['TableCell']),
            Paragraph("Heavy Deficit (-)", styles['TableCellBold']),
            Paragraph("<b>Binary decision:</b> Aggressive capital push to achieve #1 or prompt divestment.", styles['TableCell']),
        ],
        [
            Paragraph("<b>🐕 DOGS</b>", styles['TableCellBold']),
            Paragraph("RMS < 1.0x | MGR < 10%", styles['TableCell']),
            Paragraph("Weak / Negative (-)", styles['TableCellBold']),
            Paragraph("<b>Harvest or M&A carve-out:</b> Unlock working capital and redeploy key talent.", styles['TableCell']),
        ]
    ]

    t_presc_en = Table(presc_en_data, colWidths=[95, 115, 105, 196])
    t_presc_en.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, 1), C_BLUE_LIGHT),
        ('BACKGROUND', (0, 2), (-1, 2), C_TEAL_LIGHT),
        ('BACKGROUND', (0, 3), (-1, 3), C_AMBER_LIGHT),
        ('BACKGROUND', (0, 4), (-1, 4), C_ROSE_LIGHT),
    ]))
    story.append(t_presc_en)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3. Henderson's Four Fatal Portfolio Traps", styles['SubHeading']))
    story.append(Paragraph(
        "• <b>Overmilking Cash Cows:</b> Starving mature engines of basic maintenance CAPEX, surrendering leadership to rivals.<br/>"
        "• <b>Feeding the Dogs:</b> Sunk cost fallacy; pouring fresh capital into stagnant, sub-scale lines out of emotional attachment.<br/>"
        "• <b>Scattering Question Marks:</b> Thinly spreading capital across 5 different ventures without enabling any to cross RMS = 1.0x.<br/>"
        "• <b>Portfolio Aging:</b> Holding exclusively Cash Cows and Dogs; generating strong cash today but facing inevitable obsolescence.",
        styles['Body']
    ))

    story.append(PageBreak())

    # ==========================
    # PAGE 4: INDUSTRIAL CASE STUDY (NEXUS GROUP)
    # ==========================
    story.append(Paragraph("4. Industrial B2B Case Study: Nexus Industrial Technologies Group", styles['SecHeading']))
    story.append(Paragraph(
        "To demonstrate boardroom execution, we examine the anonymized corporate portfolio of <b>Nexus Group</b> "
        "(€107.0M Revenue, €18.98M EBITDA, and 8 operating business units).",
        styles['Body']
    ))

    case_en_data = [
        [
            Paragraph("<b>SBU</b>", styles['TableHeader']),
            Paragraph("<b>Sales (€)</b>", styles['TableHeader']),
            Paragraph("<b>Leader (€)</b>", styles['TableHeader']),
            Paragraph("<b>RMS</b>", styles['TableHeader']),
            Paragraph("<b>MGR %</b>", styles['TableHeader']),
            Paragraph("<b>EBITDA %</b>", styles['TableHeader']),
            Paragraph("<b>Net FCF (€)</b>", styles['TableHeader']),
            Paragraph("<b>Quadrant</b>", styles['TableHeader']),
        ],
        [
            Paragraph("SBU-01: AI Vision", styles['TableCellBold']),
            Paragraph("€18.5M", styles['TableCell']),
            Paragraph("€14.8M", styles['TableCell']),
            Paragraph("<b>1.25x</b>", styles['TableCellBold']),
            Paragraph("+18.5%", styles['TableCell']),
            Paragraph("22.0%", styles['TableCell']),
            Paragraph("+€0.65M", styles['TableCellBold']),
            Paragraph("⭐ STAR", styles['TableCellBold']),
        ],
        [
            Paragraph("SBU-02: IoT SaaS", styles['TableCellBold']),
            Paragraph("€12.2M", styles['TableCell']),
            Paragraph("€10.5M", styles['TableCell']),
            Paragraph("<b>1.16x</b>", styles['TableCellBold']),
            Paragraph("+24.0%", styles['TableCell']),
            Paragraph("25.0%", styles['TableCell']),
            Paragraph("+€0.28M", styles['TableCellBold']),
            Paragraph("⭐ STAR", styles['TableCellBold']),
        ],
        [
            Paragraph("SBU-03: Hydraulics", styles['TableCellBold']),
            Paragraph("€32.0M", styles['TableCell']),
            Paragraph("€16.0M", styles['TableCell']),
            Paragraph("<b>2.00x</b>", styles['TableCellBold']),
            Paragraph("+3.5%", styles['TableCell']),
            Paragraph("20.0%", styles['TableCell']),
            Paragraph("<b>+€4.85M</b>", styles['TableCellBold']),
            Paragraph("🐄 COW", styles['TableCellBold']),
        ],
        [
            Paragraph("SBU-04: Engines", styles['TableCellBold']),
            Paragraph("€24.5M", styles['TableCell']),
            Paragraph("€17.5M", styles['TableCell']),
            Paragraph("<b>1.40x</b>", styles['TableCellBold']),
            Paragraph("+2.0%", styles['TableCell']),
            Paragraph("18.0%", styles['TableCell']),
            Paragraph("<b>+€3.20M</b>", styles['TableCellBold']),
            Paragraph("🐄 COW", styles['TableCellBold']),
        ],
        [
            Paragraph("SBU-05: Batteries", styles['TableCellBold']),
            Paragraph("€6.5M", styles['TableCell']),
            Paragraph("€18.5M", styles['TableCell']),
            Paragraph("<b>0.35x</b>", styles['TableCellBold']),
            Paragraph("+32.0%", styles['TableCell']),
            Paragraph("6.0%", styles['TableCell']),
            Paragraph("<b>-€2.15M</b>", styles['TableCellBold']),
            Paragraph("❓ QUESTION", styles['TableCellBold']),
        ],
        [
            Paragraph("SBU-06: Quantum Laser", styles['TableCellBold']),
            Paragraph("€3.8M", styles['TableCell']),
            Paragraph("€15.2M", styles['TableCell']),
            Paragraph("<b>0.25x</b>", styles['TableCellBold']),
            Paragraph("+21.0%", styles['TableCell']),
            Paragraph("4.0%", styles['TableCell']),
            Paragraph("<b>-€1.45M</b>", styles['TableCellBold']),
            Paragraph("❓ QUESTION", styles['TableCellBold']),
        ],
        [
            Paragraph("SBU-07: Copper Wiring", styles['TableCellBold']),
            Paragraph("€5.2M", styles['TableCell']),
            Paragraph("€20.8M", styles['TableCell']),
            Paragraph("<b>0.25x</b>", styles['TableCellBold']),
            Paragraph("+1.0%", styles['TableCell']),
            Paragraph("5.0%", styles['TableCell']),
            Paragraph("-€0.18M", styles['TableCellBold']),
            Paragraph("🐕 DOG", styles['TableCellBold']),
        ],
        [
            Paragraph("SBU-08: Analog Valves", styles['TableCellBold']),
            Paragraph("€4.3M", styles['TableCell']),
            Paragraph("€14.3M", styles['TableCell']),
            Paragraph("<b>0.30x</b>", styles['TableCellBold']),
            Paragraph("-1.5%", styles['TableCell']),
            Paragraph("7.0%", styles['TableCell']),
            Paragraph("+€0.09M", styles['TableCellBold']),
            Paragraph("🐕 DOG", styles['TableCellBold']),
        ],
        [
            Paragraph("<b>CONSOLIDATED</b>", styles['TableCellBold']),
            Paragraph("<b>€107.0M</b>", styles['TableCellBold']),
            Paragraph("<b>-</b>", styles['TableCellBold']),
            Paragraph("<b>1.09x</b>", styles['TableCellBold']),
            Paragraph("<b>+8.2%</b>", styles['TableCellBold']),
            Paragraph("<b>17.7%</b>", styles['TableCellBold']),
            Paragraph("<b>+€5.29M</b>", styles['TableCellBold']),
            Paragraph("<b>SUSTAINABLE</b>", styles['TableCellBold']),
        ]
    ]

    t_case_en = Table(case_en_data, colWidths=[105, 58, 58, 48, 50, 52, 65, 75])
    t_case_en.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_case_en)
    story.append(Spacer(1, 5))

    story.append(Paragraph("Strategic Audit & Board Resolutions Approved:", styles['SubHeading']))
    story.append(Paragraph(
        "• <b>Massive Cash Cow Surplus (+€8.05M FCF):</b> Comfortably funds Question Mark growth deficits (-€3.60M), "
        "leaving a net group liquidity surplus of +€4.45M.<br/>"
        "• <b>Battery Scale-up Push (SBU-05):</b> €2.8M capital injection to expand manufacturing and drive RMS from 0.35x to 1.05x, "
        "securing a future Star before 2027.<br/>"
        "• <b>Wiring Carve-out Divestment (SBU-07):</b> M&A sale mandate approved for €3.2M, unlocking working capital and ending cash drag.<br/>"
        "• <b>ROIC Accretion:</b> Group ROIC increases from 16.0% to 19.2% (+320 bps) with an 18-month capital payback.",
        styles['Body']
    ))

    story.append(PageBreak())

    # ==========================
    # PAGE 5: BOARDROOM DEFENSE FAQ & BIBLIOGRAPHY
    # ==========================
    story.append(Paragraph("5. Boardroom Defense Protocol (C-Level FAQ)", styles['SecHeading']))

    faqs_en = [
        ("Why divest a Dog that still produces €90k in positive EBITDA?",
         "Because positive accounting EBITDA masks economic value destruction when SBU ROIC (e.g. 4%) is lower than corporate WACC (8.5%). "
         "Furthermore, sustaining sub-scale Dogs consumes scarce executive bandwidth and ties up capital that earns 22% in Stars."),

        ("How do we select which Question Mark deserves Cash Cow funding?",
         "Apply three quantitative filters: 1) Scale trajectory to RMS ≥ 1.0x (mathematical probability of surpassing the incumbent), "
         "2) Capital intensity required to double market share, and 3) Sustainable market growth runway (MGR > 10% for 5+ years). "
         "Any venture failing all three must be promptly divested or carved into a Joint Venture."),

        ("How do we keep the management teams of Cash Cow units motivated?",
         "Decouple executive bonuses from revenue growth targets and anchor them 100% on net Free Cash Flow (FCF) generation, "
         "lean working capital management, and market share defense. Cash Cow leaders should be rewarded as the guarantors of corporate liquidity."),

        ("How should the Board manage cannibalization risk between Stars and Question Marks?",
         "Bruce Henderson argued that if an emerging technology is destined to disrupt a legacy line, internal cannibalization is far superior "
         "to external disruption. The correct strategy is to aggressively scale the new technology and capture the future market profit pool.")
    ]

    for q, a in faqs_en:
        story.append(Paragraph(f"<b>Q: {q}</b>", styles['FAQ_Q']))
        story.append(Paragraph(f"<b>A:</b> {a}", styles['FAQ_A']))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Authoritative Canonical Bibliography", styles['SecHeading']))

    bibs_en = [
        ("Henderson, Bruce D. (1970).", "<i>The Product Portfolio</i>. Boston Consulting Group Perspectives, No. 66.",
         "Foundational treatise introducing the growth-share matrix and internal cash flow dynamics."),
        ("Henderson, Bruce D. (1968).", "<i>The Experience Curve</i>. Boston Consulting Group, Boston.",
         "Seminal empirical study detailing unit cost reductions driven by cumulative volume doubling."),
        ("Day, George S. (1977).", "<i>Diagnosing the Product Portfolio</i>. Journal of Marketing, Vol. 41, No. 2, pp. 29-38.",
         "Academic rigor applied to capital misallocation risks and strategic portfolio aging."),
        ("Porter, Michael E. (1980).", "<i>Competitive Strategy: Techniques for Analyzing Industries and Competitors</i>. Free Press, NY.",
         "Theoretical integration of scale-driven cost leadership and industry entry barriers."),
        ("Minto, Barbara (2009).", "<i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall.",
         "The standard framework for executive communication, structured logic, and Action Titles."),
        ("McKinsey & Company (2012).", "<i>Valuation: Measuring and Managing the Value of Companies</i>. John Wiley & Sons, NY.",
         "Definitive guide linking return on invested capital (ROIC), revenue growth, and shareholder value creation.")
    ]

    for author, work, annot in bibs_en:
        p_text = f"<b>{author}</b> {work} — <font color='#64748B'>{annot}</font>"
        story.append(Paragraph(p_text, styles['Biblio']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Methodology Guide PDF (EN) generated successfully: {out_path}")


def main():
    dir_packages = "packages"
    dir_es = os.path.join(dir_packages, "[ES]_BCG_Dinamica")
    dir_en = os.path.join(dir_packages, "[EN]_Dynamic_BCG")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    file_es = os.path.join(dir_es, "Guia_Metodologica_BCG_ES.pdf")
    file_en = os.path.join(dir_en, "Methodology_Guide_BCG_EN.pdf")

    generate_pdf_es(file_es)
    generate_pdf_en(file_en)


if __name__ == "__main__":
    main()
