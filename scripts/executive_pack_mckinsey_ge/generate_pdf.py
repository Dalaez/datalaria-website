#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas ejecutivas oficiales en PDF (5 páginas exactas) para:
1. packages/ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf (Versión en Español)
2. packages/EN_McKinsey_GE_Matrix_Methodology_Guide.pdf (Versión en Inglés)

Estándar editorial de alta dirección (McKinsey / BCG):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (Superando la Miopía de la Matriz BCG 2x2: La Génesis del Modelo McKinsey / GE).
- Página 2: Sección 2 (Fundamentación Matemática: Índices Ponderados IA/FC, Espacio Cartesiano 3x3 y Cuadro Comparativo BCG vs GE).
- Página 3: Sección 3 (Protocolo Cuantitativo de Evaluación, Neutralización del Sesgo del Management y Tabla de Conversión 1-5).
- Página 4: Sección 4 (Caso de Estudio Corporativo Resuelto: Vanguard Industrial & Tech Group con impacto en ROIC).
- Página 5: Sección 5 (Protocolo de Defensa ante el Consejo - Board Defense FAQ con 5 preguntas difíciles) y Referencias Bibliográficas.
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

# Zonas Estratégicas
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

DIR_PACKAGES = "packages"


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
            header_right = ("MATRIZ MCKINSEY / GE 3x3 & ASIGNACIÓN DE CAPITAL"
                            if lang == 'ES' else
                            "MCKINSEY / GE 3x3 MATRIX & CAPITAL ALLOCATION")
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
            fontName='Helvetica', fontSize=9.2, leading=13.0,
            textColor=C_SLATE_MUTED, spaceAfter=8
        ),
        'SecHeading': ParagraphStyle(
            'SecHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=11, leading=14.5,
            textColor=C_NAVY_DARK, spaceBefore=6, spaceAfter=3.5,
            keepWithNext=True
        ),
        'SubHeading': ParagraphStyle(
            'SubHeading', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.8, leading=11.5,
            textColor=C_NAVY_MED, spaceBefore=4, spaceAfter=2,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.0, leading=11.0,
            textColor=C_NAVY_MED, spaceAfter=3.0
        ),
        'Bullet': ParagraphStyle(
            'Bullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=8.0, leading=11.0,
            textColor=C_NAVY_MED, leftIndent=11, firstLineIndent=-7, spaceAfter=2.0
        ),
        'MathBox': ParagraphStyle(
            'MathBox', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.5, leading=11.5,
            textColor=C_NAVY_DARK, alignment=1
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.5, leading=9.2,
            textColor=C_WHITE, alignment=1
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.3, leading=9.4,
            textColor=C_NAVY_MED
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=7.3, leading=9.4,
            textColor=C_NAVY_DARK
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText', parent=base['Normal'],
            fontName='Helvetica-Oblique', fontSize=7.8, leading=10.6,
            textColor=C_NAVY_DARK
        ),
        'FAQ_Q': ParagraphStyle(
            'FAQ_Q', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=8.2, leading=11.0,
            textColor=C_NAVY_DARK, spaceBefore=3.5, spaceAfter=1.5,
            keepWithNext=True
        ),
        'FAQ_A': ParagraphStyle(
            'FAQ_A', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.7, leading=10.4,
            textColor=C_NAVY_MED, spaceAfter=2.5
        ),
        'Biblio': ParagraphStyle(
            'Biblio', parent=base['Normal'],
            fontName='Helvetica', fontSize=7.3, leading=9.8,
            textColor=C_NAVY_MED, leftIndent=9, firstLineIndent=-6, spaceAfter=2.0
        ),
    }
    return styles


def build_callout(text, styles, border_color=C_BLUE_ACCENT, bg_color=C_BLUE_LIGHT):
    p = Paragraph(text, styles['CalloutText'])
    t = Table([[p]], colWidths=[511])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('LINEBEFORE', (0, 0), (0, -1), 3.0, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 3.0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.0),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t


def build_equation_box(eq_text, styles):
    p = Paragraph(eq_text, styles['MathBox'])
    t = Table([[p]], colWidths=[511])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
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
    story.append(Paragraph("Matriz McKinsey / GE 3x3:<br/>Diagnóstico Multifactorial de Cartera & Asignación de Capital C-Level", styles['CoverTitle']))
    story.append(Paragraph(
        "Guía metodológica oficial para superar las limitaciones unifactoriales de la matriz BCG tradicional mediante la evaluación "
        "ponderada de Atractivo de la Industria vs. Fortaleza Competitiva y gobernanza de capital ante Consejos de Administración.",
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
            Paragraph("<b>Aplicación:</b> Gestión de Cartera & Asignación de Capital", styles['TableCell']),
            Paragraph("<b>Modelo:</b> Matriz McKinsey / General Electric 3x3", styles['TableCell']),
            Paragraph("<b>Estándar:</b> McKinsey Tier-1 / MBA Harvard", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 170, 171])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.0),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Superando la Miopía de la Matriz BCG 2x2: La Génesis del Modelo McKinsey / GE", styles['SecHeading']))
    story.append(Paragraph(
        "A principios de la década de 1970, General Electric (GE) operaba más de 170 divisiones de negocio dispersas en industrias tan dispares "
        "como turbinas nucleares, electrodomésticos y servicios financieros. El CEO de GE, Fred Borch, descubrió que la clásica matriz 2x2 de Boston Consulting Group "
        "(crecimiento vs. cuota de mercado relativa) resultaba peligrosamente insuficiente para gobernar una cartera compleja. "
        "McKinsey & Company fue comisionada para diseñar un marco de asignación de capital multifactorial más sofisticado: la Matriz McKinsey / GE de 9 cajas.",
        styles['Body']
    ))
    story.append(Paragraph(
        "La consultoría estratégica de alta dirección reconoce tres defectos estructurales insalvables en la matriz BCG tradicional:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• <b>La Falacia del Crecimiento como Sinónimo de Atractivo:</b> Un sector puede registrar un crecimiento anual del 30%, pero si carece "
        "de barreras de entrada y sufre una feroz competencia en precios (comoditización acelerada), la rentabilidad del capital invertido será desastrosa. "
        "El atractivo sectorial no depende únicamente de la expansión del PIB o del mercado, sino de los márgenes medios, el poder de los clientes y la estabilidad regulatoria.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>La Insuficiencia de la Cuota de Mercado como Única Ventaja Competitiva:</b> En sectores intensivos en I+D, software, marcas de lujo o servicios especializados, "
        "una empresa con apenas un 10% de cuota puede disfrutar de márgenes EBITDA del 40% gracias a patentes exclusivas, patentes de software o relaciones cerradas con clientes clave. "
        "La cuota relativa de mercado (CMR) de Henderson no explica por sí sola la ventaja competitiva sostenible.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>La Rigidez Reduccionista de los 4 Cuadrantes:</b> Forzar la toma de decisiones corporativas en cuatro cajas blanco o negro "
        "(Estrella, Vaca, Interrogante o Perro) empuja al management a clasificaciones arbitrarias en las zonas limítrofes, destruyendo la sutileza requerida para priorizar el CAPEX.",
        styles['Bullet']
    ))

    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Axioma de McKinsey:</b> El destino del capital corporativo no debe regirse por dos métricas aisladas. El atractivo de una industria "
        "debe medirse por su capacidad intrínseca de generar beneficios económicos a largo plazo, y la fortaleza de una UEN por la solidez de sus ventajas competitivas defendibles.",
        styles, border_color=C_BLUE_ACCENT, bg_color=C_BLUE_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PÁGINA 2: FUNDAMENTACIÓN MATEMÁTICA
    # ==========================
    story.append(Paragraph("2. Fundamentación Matemática: Índices Ponderados & Espacio Cartesiano 3x3", styles['SecHeading']))
    story.append(Paragraph(
        "A diferencia del enfoque cualitativo tradicional, el modelo de Datalaria formaliza la Matriz McKinsey / GE como un espacio vectorial continuo "
        "donde cada Unidad Estratégica de Negocio (UEN) se proyecta mediante un par de coordenadas normalizadas (FC, IA) en el intervalo [1.00, 5.00]:",
        styles['Body']
    ))

    story.append(Paragraph("2.1. Ecuación del Índice Ponderado de Atractivo de la Industria (IA)", styles['SubHeading']))
    story.append(Paragraph(
        "El Atractivo de la Industria (Eje Y) sintetiza la calidad estructural y el potencial de rentabilidad del sector en el que opera la UEN:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "I<sub>A</sub> = &sum;<sub>i=1</sub><sup>n</sup> w<sub>i</sub> &middot; A<sub>i</sub> &nbsp;&nbsp;&nbsp;&nbsp; "
        "sujeto a: &sum;<sub>i=1</sub><sup>n</sup> w<sub>i</sub> = 1.00 (100%), &nbsp; A<sub>i</sub> &isin; [1.00, 5.00]",
        styles
    ))
    story.append(Paragraph(
        "Donde <i>w<sub>i</sub></i> representa la ponderación estratégica asignada por el Comité de Dirección a cada uno de los 5 factores estándar: "
        "Crecimiento del Mercado (25%), Margen Operativo Sectorial (20%), Barreras de Entrada (20%), Estabilidad Regulatoria (15%) y Resiliencia Macroeconómica (20%).",
        styles['Body']
    ))

    story.append(Paragraph("2.2. Ecuación del Índice Ponderado de Fortaleza Competitiva de la UEN (FC)", styles['SubHeading']))
    story.append(Paragraph(
        "La Fortaleza Competitiva (Eje X) cuantifica la capacidad de la UEN para batir a sus competidores directos y capturar rentas económicas:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "F<sub>C</sub> = &sum;<sub>j=1</sub><sup>m</sup> v<sub>j</sub> &middot; C<sub>j</sub> &nbsp;&nbsp;&nbsp;&nbsp; "
        "sujeto a: &sum;<sub>j=1</sub><sup>m</sup> v<sub>j</sub> = 1.00 (100%), &nbsp; C<sub>j</sub> &isin; [1.00, 5.00]",
        styles
    ))
    story.append(Paragraph(
        "Donde <i>v<sub>j</sub></i> representa el peso de los factores internos: Cuota de Mercado Relativa (25%), Ventaja Tecnológica y Patentes (20%), "
        "Diferencial de Margen Bruto (20%), Fuerza de Marca y Canales (15%) y Capacidad Financiera y Operativa (20%).",
        styles['Body']
    ))

    story.append(Paragraph("2.3. Partición del Espacio Cartesiano en 9 Cuadrantes y 3 Zonas de Capital", styles['SubHeading']))
    story.append(Paragraph(
        "El espacio bidimensional continuo [1.00, 5.00] &times; [1.00, 5.00] se divide en tres intervalos canónicos de frontera: "
        "Rango Alto / Fuerte [3.67, 5.00], Rango Medio [2.33, 3.66] y Rango Bajo / Débil [1.00, 2.32]. Esta partición genera 9 cuadrantes agrupados en 3 zonas estratégicas:",
        styles['Body']
    ))

    # Cuadro comparativo BCG vs GE
    comp_headers = [
        Paragraph("<b>Dimensión Analítica</b>", styles['TableHeader']),
        Paragraph("<b>Matriz BCG 2x2 (Henderson 1968)</b>", styles['TableHeader']),
        Paragraph("<b>Matriz McKinsey / GE 3x3 (1971 / 2026)</b>", styles['TableHeader']),
    ]
    comp_rows = [
        comp_headers,
        [
            Paragraph("<b>Eje Vertical (Mercado)</b>", styles['TableCellBold']),
            Paragraph("Tasa de Crecimiento del Mercado (%) única", styles['TableCell']),
            Paragraph("Atractivo Multifactorial (Crecimiento, Margen, Barreras, ESG)", styles['TableCell']),
        ],
        [
            Paragraph("<b>Eje Horizontal (Empresa)</b>", styles['TableCellBold']),
            Paragraph("Cuota de Mercado Relativa (CMR) unifactorial", styles['TableCell']),
            Paragraph("Fortaleza Multifactorial (CMR, Tecnología, Patentes, Marca)", styles['TableCell']),
        ],
        [
            Paragraph("<b>Resolución / Granularidad</b>", styles['TableCellBold']),
            Paragraph("4 cuadrantes dicotómicos rígidos", styles['TableCell']),
            Paragraph("9 cajas con 3 zonas estratégicas de asignación de capital", styles['TableCell']),
        ],
        [
            Paragraph("<b>Zona de Ambigüedad</b>", styles['TableCellBold']),
            Paragraph("Interrogantes (trampa crónica de capital)", styles['TableCell']),
            Paragraph("Diagonal de Selectividad con mandatos de autofinanciación", styles['TableCell']),
        ],
        [
            Paragraph("<b>Impacto en Gobierno</b>", styles['TableCellBold']),
            Paragraph("Clasificación descriptiva de marcas", styles['TableCell']),
            Paragraph("Mandato vinculante de CAPEX, Hurdle Rates (TIR) y Carve-outs", styles['TableCell']),
        ],
    ]
    comp_table = Table(comp_rows, colWidths=[120, 195, 196])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(comp_table)

    story.append(PageBreak())

    # ==========================
    # PÁGINA 3: PROTOCOLO CUANTITATIVO Y NEUTRALIZACIÓN DE SESGOS
    # ==========================
    story.append(Paragraph("3. Protocolo Cuantitativo de Evaluación y Neutralización de Sesgos", styles['SecHeading']))
    story.append(Paragraph(
        "El principal riesgo en la aplicación práctica de la Matriz McKinsey / GE es el <b>Sesgo de Autoindulgencia del Management</b>: "
        "los directores de división tienden a sobrestimar la fortaleza de sus negocios (calificándose sistemáticamente con notas de 4.5 o 5.0) "
        "y a exagerar el atractivo de sus mercados para asegurar asignaciones presupuestarias más elevadas.",
        styles['Body']
    ))

    story.append(Paragraph("3.1. Los Cuatro Filtros de Auditoría de la Oficina de Estrategia (PMO / FP&A)", styles['SubHeading']))
    story.append(Paragraph(
        "Para garantizar que las calificaciones reflejen la realidad económica y no la retórica del management, Datalaria prescribe un protocolo de 4 filtros obligatorios:",
        styles['Body']
    ))
    story.append(Paragraph(
        "1. <b>Filtro de Evidencia Numérica:</b> Ninguna nota superior a 3.0 puede asignarse sin una métrica cuantitativa verificable (ej: auditoría de cuota, "
        "margen bruto auditado frente a competidores directos o número de patentes activas registradas en los últimos 24 meses).",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "2. <b>Filtro de Benchmark Externo:</b> Las estimaciones de crecimiento del mercado y márgenes sectoriales deben validarse contra fuentes independientes "
        "(informes de analistas de banca de inversión, Gartner, IDC, consultoras especializadas o asociaciones sectoriales reguladas).",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "3. <b>Filtro de Auditoría Cruzada Inter-divisional:</b> En la sesión de calibración del Comité de Dirección, cada director de UEN debe defender "
        "sus notas ante el escrutinio de los líderes de las restantes divisiones y del Director Financiero (CFO).",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "4. <b>Filtro de Backtesting Histórico:</b> Si una división se autocalifica con 'Fortaleza Tecnológica 5.0', se audita si esa presunta ventaja "
        "se ha traducido efectivamente en una prima de precio (pricing power) y margen bruto superior al del líder en los últimos 3 ejercicios.",
        styles['Bullet']
    ))

    story.append(Paragraph("3.2. Matriz de Conversión Cuantitativa Estándar (Escala Objetiva 1.0 a 5.0)", styles['SubHeading']))
    story.append(Paragraph(
        "Para eliminar la ambigüedad semántica, cada factor se califica utilizando baremos empíricos contrastables:",
        styles['Body']
    ))

    # Tabla de Baremos
    scale_headers = [
        Paragraph("<b>Nivel / Calificación</b>", styles['TableHeader']),
        Paragraph("<b>Crecimiento Mercado (CAGR)</b>", styles['TableHeader']),
        Paragraph("<b>Margen EBITDA Sector</b>", styles['TableHeader']),
        Paragraph("<b>Cuota Relativa (CMR)</b>", styles['TableHeader']),
        Paragraph("<b>Ventaja Tecnológica / IP</b>", styles['TableHeader']),
    ]
    scale_rows = [
        scale_headers,
        [
            Paragraph("<b>5.0 (Excepcional / Líder)</b>", styles['TableCellBold']),
            Paragraph("> 15.0% anual compuesto", styles['TableCell']),
            Paragraph("> 25.0% sobre ventas", styles['TableCell']),
            Paragraph("&ge; 2.0x (Líder indiscutido)", styles['TableCell']),
            Paragraph("Patentes exclusivas / Monopolio IP", styles['TableCell']),
        ],
        [
            Paragraph("<b>4.0 (Fuerte / Favorable)</b>", styles['TableCellBold']),
            Paragraph("10.0% - 15.0% anual", styles['TableCell']),
            Paragraph("18.0% - 25.0%", styles['TableCell']),
            Paragraph("1.2x - 1.9x (Liderazgo disputado)", styles['TableCell']),
            Paragraph("Tecnología puntera / Pipeline sólido", styles['TableCell']),
        ],
        [
            Paragraph("<b>3.0 (Medio / Neutral)</b>", styles['TableCellBold']),
            Paragraph("5.0% - 9.9% (en línea PIB)", styles['TableCell']),
            Paragraph("12.0% - 17.9%", styles['TableCell']),
            Paragraph("0.8x - 1.1x (Paridad de mercado)", styles['TableCell']),
            Paragraph("En línea con competidores estándar", styles['TableCell']),
        ],
        [
            Paragraph("<b>2.0 (Débil / Desfavorable)</b>", styles['TableCellBold']),
            Paragraph("1.0% - 4.9% (madurez)", styles['TableCell']),
            Paragraph("7.0% - 11.9%", styles['TableCell']),
            Paragraph("0.4x - 0.7x (Seguidor secundario)", styles['TableCell']),
            Paragraph("Dependencia de licencias de terceros", styles['TableCell']),
        ],
        [
            Paragraph("<b>1.0 (Muy Bajo / Crítico)</b>", styles['TableCellBold']),
            Paragraph("&le; 0.0% (contracción)", styles['TableCell']),
            Paragraph("< 7.0% (comoditizado)", styles['TableCell']),
            Paragraph("< 0.4x (Marginal / Enano)", styles['TableCell']),
            Paragraph("Obsolescencia tecnológica severa", styles['TableCell']),
        ],
    ]
    scale_table = Table(scale_rows, colWidths=[105, 105, 100, 101, 100])
    scale_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(scale_table)

    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Regla de Oro de Gobernanza:</b> Si el valor consolidado de Atractivo o Fortaleza se ubica en la frontera exacta (ej: 3.65 a 3.69), "
        "el Comité debe realizar un análisis de sensibilidad estresando las ponderaciones &plusmn;5% antes de ratificar el cuadrante asignado.",
        styles, border_color=C_AMBER_ACCENT, bg_color=C_AMBER_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PÁGINA 4: CASO DE ESTUDIO CORPORATIVO
    # ==========================
    story.append(Paragraph("4. Caso de Estudio Corporativo Resuelto: Vanguard Industrial & Tech Group", styles['SecHeading']))
    story.append(Paragraph(
        "Vanguard Industrial & Tech Group es un conglomerado industrial cotizado con 10 Unidades Estratégicas de Negocio, una facturación anual "
        "de 485.0M€ y un presupuesto trianual de CAPEX de 75.0M€. Históricamente, el grupo distribuía su capital de manera 'democrática' (+5% lineal a cada división), "
        "lo que resultó en una erosión progresiva del ROIC corporativo (11.2% frente a un WACC del 8.8%) y la pérdida de tracción en sus negocios más innovadores.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Tras implementar el modelo analítico de Datalaria, la cartera completa fue mapeada objetivamente en la Matriz McKinsey / GE 3x3:",
        styles['Body']
    ))

    # Tabla de Resultados Vanguard Group
    vg_headers = [
        Paragraph("<b>Cód</b>", styles['TableHeader']),
        Paragraph("<b>Unidad de Negocio (UEN)</b>", styles['TableHeader']),
        Paragraph("<b>Ventas (€M)</b>", styles['TableHeader']),
        Paragraph("<b>EBITDA %</b>", styles['TableHeader']),
        Paragraph("<b>IA</b>", styles['TableHeader']),
        Paragraph("<b>FC</b>", styles['TableHeader']),
        Paragraph("<b>Zona Estratégica</b>", styles['TableHeader']),
        Paragraph("<b>CAPEX 3A</b>", styles['TableHeader']),
        Paragraph("<b>TIR Mín</b>", styles['TableHeader']),
    ]
    vg_rows = [
        vg_headers,
        [Paragraph("UEN-01", styles['TableCellBold']), Paragraph("Plataformas Cloud e IA Industrial", styles['TableCell']), Paragraph("95.0", styles['TableCellBold']), Paragraph("28.5%", styles['TableCell']), Paragraph("4.64", styles['TableCell']), Paragraph("4.63", styles['TableCell']), Paragraph("Invertir / Crecer", styles['TableCellBold']), Paragraph("24.0 M€", styles['TableCellBold']), Paragraph("18.0%", styles['TableCell'])],
        [Paragraph("UEN-02", styles['TableCellBold']), Paragraph("Robótica Médica y Quirúrgica", styles['TableCell']), Paragraph("72.0", styles['TableCellBold']), Paragraph("24.0%", styles['TableCell']), Paragraph("4.61", styles['TableCell']), Paragraph("3.81", styles['TableCell']), Paragraph("Invertir / Crecer", styles['TableCellBold']), Paragraph("18.5 M€", styles['TableCellBold']), Paragraph("18.0%", styles['TableCell'])],
        [Paragraph("UEN-03", styles['TableCellBold']), Paragraph("Electrónica de Potencia e Inversores", styles['TableCell']), Paragraph("110.0", styles['TableCellBold']), Paragraph("18.2%", styles['TableCell']), Paragraph("3.72", styles['TableCell']), Paragraph("4.20", styles['TableCell']), Paragraph("Invertir / Crecer", styles['TableCellBold']), Paragraph("16.0 M€", styles['TableCellBold']), Paragraph("18.0%", styles['TableCell'])],
        [Paragraph("UEN-04", styles['TableCellBold']), Paragraph("Automatización y Sensores Industriales", styles['TableCell']), Paragraph("68.0", styles['TableCell']), Paragraph("16.5%", styles['TableCell']), Paragraph("3.29", styles['TableCell']), Paragraph("3.49", styles['TableCell']), Paragraph("Seleccionar / Proteger", styles['TableCell']), Paragraph("7.5 M€", styles['TableCell']), Paragraph("14.0%", styles['TableCell'])],
        [Paragraph("UEN-05", styles['TableCellBold']), Paragraph("Telemática y Conectividad de Flotas", styles['TableCell']), Paragraph("35.0", styles['TableCell']), Paragraph("14.0%", styles['TableCell']), Paragraph("3.57", styles['TableCell']), Paragraph("2.72", styles['TableCell']), Paragraph("Seleccionar / Proteger", styles['TableCell']), Paragraph("5.3 M€", styles['TableCell']), Paragraph("14.0%", styles['TableCell'])],
        [Paragraph("UEN-06", styles['TableCellBold']), Paragraph("Climatización HVAC y Sistemas Térmicos", styles['TableCell']), Paragraph("42.0", styles['TableCell']), Paragraph("15.0%", styles['TableCell']), Paragraph("2.25", styles['TableCell']), Paragraph("4.09", styles['TableCell']), Paragraph("Seleccionar / Proteger", styles['TableCell']), Paragraph("4.5 M€", styles['TableCell']), Paragraph("14.0%", styles['TableCell'])],
        [Paragraph("UEN-07", styles['TableCellBold']), Paragraph("Mecanizado y Aleaciones de Precisión", styles['TableCell']), Paragraph("25.0", styles['TableCell']), Paragraph("11.0%", styles['TableCell']), Paragraph("3.91", styles['TableCell']), Paragraph("1.98", styles['TableCell']), Paragraph("Seleccionar / Proteger", styles['TableCell']), Paragraph("4.7 M€", styles['TableCell']), Paragraph("14.0%", styles['TableCell'])],
        [Paragraph("UEN-08", styles['TableCellBold']), Paragraph("Válvulas Hidráulicas Maquinaria Pesada", styles['TableCell']), Paragraph("18.0", styles['TableCell']), Paragraph("8.5%", styles['TableCell']), Paragraph("2.64", styles['TableCell']), Paragraph("1.95", styles['TableCell']), Paragraph("Cosechar / Desinvertir", styles['TableCellBold']), Paragraph("1.2 M€", styles['TableCell']), Paragraph("10.0%", styles['TableCell'])],
        [Paragraph("UEN-09", styles['TableCellBold']), Paragraph("Cableado y Conectores Estándar", styles['TableCell']), Paragraph("12.0", styles['TableCell']), Paragraph("6.0%", styles['TableCell']), Paragraph("1.90", styles['TableCell']), Paragraph("2.52", styles['TableCell']), Paragraph("Cosechar / Desinvertir", styles['TableCellBold']), Paragraph("0.8 M€", styles['TableCell']), Paragraph("10.0%", styles['TableCell'])],
        [Paragraph("UEN-10", styles['TableCellBold']), Paragraph("Cuadros Eléctricos y Medidores Analógicos", styles['TableCell']), Paragraph("8.0", styles['TableCell']), Paragraph("3.2%", styles['TableCell']), Paragraph("1.57", styles['TableCell']), Paragraph("1.60", styles['TableCell']), Paragraph("Cosechar / Desinvertir", styles['TableCellBold']), Paragraph("0.2 M€", styles['TableCell']), Paragraph("10.0%", styles['TableCell'])],
    ]
    vg_table = Table(vg_rows, colWidths=[38, 145, 52, 45, 34, 34, 88, 45, 30])
    vg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.0),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(vg_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.1. Impacto Financiero del Plan de Reasignación de Capital de Datalaria", styles['SubHeading']))
    story.append(Paragraph(
        "• <b>Concentración en Ganadores (68% del CAPEX):</b> Se asignaron 51.0M€ a las UENs 01, 02 y 03, financiando nuevas líneas de producción y compras M&A bolt-on.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Autofinanciación en Selectividad (27% del CAPEX):</b> Las UENs 04, 05, 06 y 07 recibieron 20.2M€ exclusivamente bajo la condición de autofinanciarse vía EBITDA.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Desinversión en Cosecha (Salida de Capital):</b> Se congeló el CAPEX en UENs 08, 09 y 10 (apenas 2.2M€ regulatorios), iniciando un proceso de carve-out que liberará 24.0M€ en efectivo antes de Q4 2026. "
        "El ROIC corporativo proyectado pasa del 11.2% al 15.0% (+380 bps) a 36 meses.",
        styles['Bullet']
    ))

    story.append(Spacer(1, 3))
    story.append(build_callout(
        "<b>Resultado para el Accionista:</b> La eliminación del arrastre negativo de las 3 unidades en zona roja expande el múltiplo EV/EBITDA "
        "corporativo en +2.1x, generando un incremento de valor patrimonial neto estimado en 92M€.",
        styles, border_color=C_GREEN_ACCENT, bg_color=C_GREEN_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PÁGINA 5: PROTOCOLO DE DEFENSA & FAQ C-LEVEL
    # ==========================
    story.append(Paragraph("5. Protocolo de Defensa ante el Consejo de Administración (Board Defense FAQ)", styles['SecHeading']))
    story.append(Paragraph(
        "En reuniones de Consejo de Administración, directores independientes y comisiones de auditoría plantearán preguntas incisivas "
        "sobre las conclusiones del modelo. A continuación se presentan 5 respuestas modelo basadas estrictamente en fundamentos económico-financieros:",
        styles['Body']
    ))

    faqs_es = [
        ("P1: ¿Por qué debemos reemplazar la Matriz BCG por la Matriz McKinsey / GE si la BCG es más sencilla de entender?",
         "<b>Respuesta C-Level:</b> La matriz BCG simplifica en exceso la realidad competitiva al asumir que el crecimiento del mercado equivale a rentabilidad. "
         "En la economía moderna, sectores con alto crecimiento pueden tener márgenes nulos si las barreras de entrada son bajas. La Matriz McKinsey / GE "
         "incorpora cinco factores estructurales de atractivo y cinco de fortaleza competitiva, evitando errores multimillonarios de sobreinversión en mercados trampa."),

        ("P2: ¿Cómo justificamos desinvertir o congelar el CAPEX en una UEN (zona roja) que todavía arroja beneficio contable positivo?",
         "<b>Respuesta C-Level:</b> El beneficio contable marginal oculta una destrucción real de valor patrimonial. Si una UEN genera un ROIC del 6.0% "
         "mientras el WACC corporativo es del 8.8%, cada euro reinvertido en sus activos destruye 28 céntimos de valor para el accionista. Vender o cosechar "
         "esa unidad permite reinvertir ese capital liberado en UENs de la Zona Verde con retornos del 24% al 31%."),

        ("P3: ¿Cómo resolvemos el dilema estratégico en la diagonal de Selectividad (¿invertir selectivamente o preparar para venta?)?",
         "<b>Respuesta C-Level:</b> La diagonal de Selectividad exige una prueba de fuego cuantitativa: si la UEN tiene una vía clara y verificable para alcanzar "
         "una posición de liderazgo en un nicho de alto margen autofinanciándose, se autoriza el plan. Si requiere inyecciones constantes de capital corporativo "
         "sin mejorar su cuota relativa en 18 meses, se reclasifica automáticamente para desinversión."),

        ("P4: ¿Cómo respondemos si un director de división acusa al modelo de subjetividad en las ponderaciones de los criterios?",
         "<b>Respuesta C-Level:</b> El modelo no es subjetivo porque aplica los 4 filtros de auditoría corporativa y obliga a vincular cada nota a fuentes externas "
         "(Gartner, estados contables auditados de competidores). Además, realizamos pruebas de estrés variando las ponderaciones &plusmn;20%: si el cuadrante "
         "asignado es robusto ante estas variaciones, la conclusión estratégica es matemáticamente incontrovertible."),

        ("P5: ¿Cuál es el impacto en el coste ponderado de capital (WACC) tras desinvertir las divisiones de la zona roja?",
         "<b>Respuesta C-Level:</b> Desinvertir unidades maduras o en declive reduce la deuda financiera neta corporativa, mejora la ratio de cobertura de intereses "
         "(ICR) y disminuye la beta desapalancada del grupo, lo que comprime el WACC entre 40 y 60 bps y eleva automáticamente la valoración del holding."),
    ]

    for q, a in faqs_es:
        story.append(Paragraph(q, styles['FAQ_Q']))
        story.append(Paragraph(a, styles['FAQ_A']))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Referencias Bibliográficas y Fuentes Canónicas", styles['SubHeading']))
    bibs_es = [
        "• McKinsey & Company (1971): <i>Strategic Business Planning: The Multifactor Portfolio Matrix</i>, McKinsey Staff Paper Series, New York.",
        "• Day, George S. (1977): <i>Diagnosing the Product Portfolio</i>, Journal of Marketing, Vol. 41, No. 2, pp. 29-38.",
        "• Haspeslagh, Philippe (1982): <i>Portfolio Planning: Uses and Limits</i>, Harvard Business Review, Vol. 60, No. 1, pp. 58-73.",
        "• Henderson, Bruce D. (1979): <i>Henderson on Corporate Strategy</i>, Boston Consulting Group / Abt Books, Cambridge, MA.",
    ]
    for b in bibs_es:
        story.append(Paragraph(b, styles['Biblio']))

    # Construcción del documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Guía PDF en Español generada: {out_path}")
    return out_path


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
    story.append(Paragraph("McKinsey / GE 3x3 Matrix:<br/>Multifactor Portfolio Diagnostics & C-Level Capital Allocation", styles['CoverTitle']))
    story.append(Paragraph(
        "Official executive methodology guide to overcoming the unidimensional limits of the legacy BCG matrix through rigorous "
        "multifactor scoring of Industry Attractiveness vs. Business Unit Strength and boardroom capital allocation governance.",
        styles['CoverSub']
    ))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Authorship:</b> Datalaria Strategy Practice", styles['TableCell']),
            Paragraph("<b>Version:</b> 2026.1 Official C-Level", styles['TableCell']),
            Paragraph("<b>Classification:</b> Board Decision Support", styles['TableCell'])
        ],
        [
            Paragraph("<b>Application:</b> Portfolio Strategy & Capital Allocation", styles['TableCell']),
            Paragraph("<b>Framework:</b> McKinsey / General Electric 3x3 Matrix", styles['TableCell']),
            Paragraph("<b>Standard:</b> McKinsey Tier-1 / Harvard MBA", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 170, 171])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.0),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Overcoming the Myopia of the BCG 2x2: The Genesis of the McKinsey / GE Model", styles['SecHeading']))
    story.append(Paragraph(
        "In the early 1970s, General Electric (GE) operated more than 170 diverse strategic business units spanning aircraft engines, "
        "appliances, industrial plastics, and financial services. GE's CEO, Fred Borch, realized that Boston Consulting Group's classic 2x2 matrix "
        "(market growth rate vs. relative market share) was critically inadequate to govern such complex capital allocation. "
        "McKinsey & Company was retained to engineer a multifactor portfolio framework: the McKinsey / GE 9-Box Matrix.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Tier-1 corporate strategy recognizes three insurmountable structural flaws in the legacy BCG 2x2 matrix:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• <b>The Fallacy of Growth as a Proxy for Attractiveness:</b> An industry may enjoy 30% annual top-line growth, but if entry barriers "
        "are non-existent and commoditization triggers brutal price wars, return on invested capital will collapse. "
        "Structural attractiveness depends on industry margins, supplier/buyer power, and regulatory moats—not simply addressable market expansion.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Market Share as an Insufficient Competitive Proxy:</b> In high-tech, software, IP-heavy, or specialized B2B segments, "
        "a company with only a 10% market share can generate 40% EBITDA margins due to proprietary patents, algorithmic defensibility, or captive client channels. "
        "Henderson's Relative Market Share (RMS) fails to account for differentiated micro-moats.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>The Oversimplification of 4 Binary Quadrants:</b> Forcing corporate allocation into four crude categories "
        "(Star, Cash Cow, Question Mark, Dog) pushes leadership into distorted frontier calls, lacking the granularity needed to govern capital.",
        styles['Bullet']
    ))

    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>The McKinsey Axiom:</b> Corporate capital allocation must never rely on two isolated proxies. Industry attractiveness must be measured "
        "by structural economic profit potential, and business strength by the defensibility of distinct competitive advantages.",
        styles, border_color=C_BLUE_ACCENT, bg_color=C_BLUE_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PAGE 2: MATHEMATICAL FOUNDATIONS
    # ==========================
    story.append(Paragraph("2. Mathematical Foundations: Weighted Indices & 3x3 Vector Space", styles['SecHeading']))
    story.append(Paragraph(
        "Unlike subjective qualitative diagrams, Datalaria's model formalizes the McKinsey / GE Matrix as a continuous vector space "
        "where each Strategic Business Unit (SBU) is projected via normalized coordinates (FC, IA) across the [1.00, 5.00] scale:",
        styles['Body']
    ))

    story.append(Paragraph("2.1. Industry Attractiveness Weighted Index Equation (IA)", styles['SubHeading']))
    story.append(Paragraph(
        "Industry Attractiveness (Y-Axis) synthesizes structural industry profitability and economic expansion potential:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "I<sub>A</sub> = &sum;<sub>i=1</sub><sup>n</sup> w<sub>i</sub> &middot; A<sub>i</sub> &nbsp;&nbsp;&nbsp;&nbsp; "
        "subject to: &sum;<sub>i=1</sub><sup>n</sup> w<sub>i</sub> = 1.00 (100%), &nbsp; A<sub>i</sub> &isin; [1.00, 5.00]",
        styles
    ))
    story.append(Paragraph(
        "Where <i>w<sub>i</sub></i> denotes the strategic weights calibrated by the Board across 5 standard criteria: "
        "Market Growth Rate (25%), Industry Operating Margin (20%), Entry Barriers & Rivalry (20%), Regulatory Stability (15%), and Macroeconomic Resilience (20%).",
        styles['Body']
    ))

    story.append(Paragraph("2.2. Business Unit Competitive Strength Weighted Index Equation (FC)", styles['SubHeading']))
    story.append(Paragraph(
        "Business Unit Strength (X-Axis) quantifies internal competitive moat depth and economic rent extraction ability:",
        styles['Body']
    ))
    story.append(build_equation_box(
        "F<sub>C</sub> = &sum;<sub>j=1</sub><sup>m</sup> v<sub>j</sub> &middot; C<sub>j</sub> &nbsp;&nbsp;&nbsp;&nbsp; "
        "subject to: &sum;<sub>j=1</sub><sup>m</sup> v<sub>j</sub> = 1.00 (100%), &nbsp; C<sub>j</sub> &isin; [1.00, 5.00]",
        styles
    ))
    story.append(Paragraph(
        "Where <i>v<sub>j</sub></i> represents internal weights: Relative Market Share (25%), Tech Advantage & Patents (20%), "
        "Relative Gross Margin (20%), Brand Equity & Channel Reach (15%), and Financial/Operational Agility (20%).",
        styles['Body']
    ))

    story.append(Paragraph("2.3. Vector Space Partition: 9 Quadrants and 3 Strategic Capital Zones", styles['SubHeading']))
    story.append(Paragraph(
        "The [1.00, 5.00] &times; [1.00, 5.00] space is partitioned into three canonical boundary tiers: "
        "Upper Tier [3.67, 5.00], Middle Tier [2.33, 3.66], and Lower Tier [1.00, 2.32]. This yields 9 distinct boxes consolidated into 3 strategic capital zones:",
        styles['Body']
    ))

    # Analytical Comparison Table
    comp_headers = [
        Paragraph("<b>Strategic Dimension</b>", styles['TableHeader']),
        Paragraph("<b>Legacy BCG 2x2 (Henderson 1968)</b>", styles['TableHeader']),
        Paragraph("<b>McKinsey / GE 3x3 Matrix (1971 / 2026)</b>", styles['TableHeader']),
    ]
    comp_rows = [
        comp_headers,
        [
            Paragraph("<b>Vertical Axis (Market)</b>", styles['TableCellBold']),
            Paragraph("Single Market Growth Rate (%)", styles['TableCell']),
            Paragraph("Multifactor Attractiveness (Growth, Margins, Barriers, ESG)", styles['TableCell']),
        ],
        [
            Paragraph("<b>Horizontal Axis (Company)</b>", styles['TableCellBold']),
            Paragraph("Single Relative Market Share (RMS)", styles['TableCell']),
            Paragraph("Multifactor Strength (RMS, Tech Edge, Patents, Brand)", styles['TableCell']),
        ],
        [
            Paragraph("<b>Resolution & Granularity</b>", styles['TableCellBold']),
            Paragraph("4 rigid, dichotomous quadrants", styles['TableCell']),
            Paragraph("9 boxes consolidated into 3 actionable capital allocation zones", styles['TableCell']),
        ],
        [
            Paragraph("<b>Ambiguity Handling</b>", styles['TableCellBold']),
            Paragraph("Question Marks (chronic capital drain trap)", styles['TableCell']),
            Paragraph("Selectivity Diagonal with strict self-funding mandates", styles['TableCell']),
        ],
        [
            Paragraph("<b>Boardroom Mandate</b>", styles['TableCellBold']),
            Paragraph("Descriptive brand taxonomy", styles['TableCell']),
            Paragraph("Binding CAPEX hurdles, IRR benchmarks, and carve-out triggers", styles['TableCell']),
        ],
    ]
    comp_table = Table(comp_rows, colWidths=[120, 195, 196])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(comp_table)

    story.append(PageBreak())

    # ==========================
    # PAGE 3: QUANTITATIVE PROTOCOL & BIAS ELIMINATION
    # ==========================
    story.append(Paragraph("3. Quantitative Evaluation Protocol & Management Bias Elimination", styles['SecHeading']))
    story.append(Paragraph(
        "The primary threat to the integrity of the McKinsey / GE Matrix in corporate practice is <b>Management Self-Serving Bias</b>: "
        "divisional executives routinely inflate their unit's competitive edge (awarding themselves 4.5 or 5.0 ratings) "
        "while exaggerating market growth to secure corporate capital appropriations.",
        styles['Body']
    ))

    story.append(Paragraph("3.1. The Four-Filter Audit Protocol for Corporate Strategy & FP&A", styles['SubHeading']))
    story.append(Paragraph(
        "To enforce empirical rigor and neutralize optimism bias, Datalaria mandates a four-filter audit protocol:",
        styles['Body']
    ))
    story.append(Paragraph(
        "1. <b>Hard Metric Verification:</b> No rating above 3.0 may be awarded without audited quantitative proof (e.g., third-party market share audits, "
        "gross margin differentials vs. direct peers, or active patent filings over the trailing 24 months).",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "2. <b>External Benchmark Validation:</b> Addressable market CAGR and industry margin baselines must be substantiated by external research "
        "(independent investment banking research, Gartner, IDC, or regulated industry trade data).",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "3. <b>Cross-Divisional Peer Scrutiny:</b> During executive calibration sessions, each SBU head must defend their ratings "
        "under rigorous challenge from peer business leaders and the Chief Financial Officer (CFO).",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "4. <b>Historical Backtesting:</b> If an SBU claims a '5.0 Technological Moat', corporate FP&A audits whether that alleged advantage "
        "has translated into superior pricing power and above-industry gross margins over the preceding three fiscal years.",
        styles['Bullet']
    ))

    story.append(Paragraph("3.2. Standard Quantitative Scoring Scale (Objective 1.0 to 5.0 Calibration)", styles['SubHeading']))
    story.append(Paragraph(
        "To eliminate subjective ambiguity, all criteria are mapped against verifiable quantitative metrics:",
        styles['Body']
    ))

    # Benchmark scale table
    scale_headers = [
        Paragraph("<b>Rating / Tier</b>", styles['TableHeader']),
        Paragraph("<b>Market Growth (CAGR)</b>", styles['TableHeader']),
        Paragraph("<b>Industry EBITDA Margin</b>", styles['TableHeader']),
        Paragraph("<b>Relative Share (RMS)</b>", styles['TableHeader']),
        Paragraph("<b>Tech Advantage & IP</b>", styles['TableHeader']),
    ]
    scale_rows = [
        scale_headers,
        [
            Paragraph("<b>5.0 (Exceptional Leader)</b>", styles['TableCellBold']),
            Paragraph("> 15.0% CAGR", styles['TableCell']),
            Paragraph("> 25.0% on revenue", styles['TableCell']),
            Paragraph("&ge; 2.0x (Undisputed leader)", styles['TableCell']),
            Paragraph("Proprietary patent monopoly", styles['TableCell']),
        ],
        [
            Paragraph("<b>4.0 (Strong Moat)</b>", styles['TableCellBold']),
            Paragraph("10.0% - 15.0%", styles['TableCell']),
            Paragraph("18.0% - 25.0%", styles['TableCell']),
            Paragraph("1.2x - 1.9x (Challenger/Co-leader)", styles['TableCell']),
            Paragraph("Defensible IP & active pipeline", styles['TableCell']),
        ],
        [
            Paragraph("<b>3.0 (Average / Parity)</b>", styles['TableCellBold']),
            Paragraph("5.0% - 9.9% (in line with GDP)", styles['TableCell']),
            Paragraph("12.0% - 17.9%", styles['TableCell']),
            Paragraph("0.8x - 1.1x (Market parity)", styles['TableCell']),
            Paragraph("Standard industry parity", styles['TableCell']),
        ],
        [
            Paragraph("<b>2.0 (Weak / Lagging)</b>", styles['TableCellBold']),
            Paragraph("1.0% - 4.9% (mature/slow)", styles['TableCell']),
            Paragraph("7.0% - 11.9%", styles['TableCell']),
            Paragraph("0.4x - 0.7x (Secondary follower)", styles['TableCell']),
            Paragraph("Third-party license dependence", styles['TableCell']),
        ],
        [
            Paragraph("<b>1.0 (Critical / Deficit)</b>", styles['TableCellBold']),
            Paragraph("&le; 0.0% (contracting)", styles['TableCell']),
            Paragraph("< 7.0% (commoditized)", styles['TableCell']),
            Paragraph("< 0.4x (Marginal dwarf)", styles['TableCell']),
            Paragraph("Severe technological obsolescence", styles['TableCell']),
        ],
    ]
    scale_table = Table(scale_rows, colWidths=[105, 105, 100, 101, 100])
    scale_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(scale_table)

    story.append(Spacer(1, 4))
    story.append(build_callout(
        "<b>Board Governance Rule:</b> Any consolidated Attractiveness or Strength score landing precisely on boundary thresholds "
        "(e.g., 3.65 to 3.69) requires sensitivity stress testing (&plusmn;5% on factor weights) before the Board formalizes quadrant assignment.",
        styles, border_color=C_AMBER_ACCENT, bg_color=C_AMBER_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PAGE 4: CORPORATE CASE STUDY
    # ==========================
    story.append(Paragraph("4. Industrial Corporate Case Study: Vanguard Industrial & Tech Group", styles['SecHeading']))
    story.append(Paragraph(
        "Vanguard Industrial & Tech Group is a diversified publicly traded conglomerate with 10 Strategic Business Units, $485.0M in annual revenue, "
        "and a $75.0M 3-year corporate CAPEX pool. Historically, capital was allocated homogeneously (+5% annually across all divisions), "
        "causing chronic corporate ROIC degradation (11.2% vs. 8.8% WACC) and underfunding breakthrough growth platforms.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Deploying Datalaria's analytical engine mapped the entire portfolio into the McKinsey / GE 9-Box Matrix:",
        styles['Body']
    ))

    # Master Table Vanguard
    vg_headers = [
        Paragraph("<b>Code</b>", styles['TableHeader']),
        Paragraph("<b>Strategic Business Unit (SBU)</b>", styles['TableHeader']),
        Paragraph("<b>Sales ($M)</b>", styles['TableHeader']),
        Paragraph("<b>EBITDA %</b>", styles['TableHeader']),
        Paragraph("<b>IA</b>", styles['TableHeader']),
        Paragraph("<b>FC</b>", styles['TableHeader']),
        Paragraph("<b>Strategic Zone</b>", styles['TableHeader']),
        Paragraph("<b>3Y CAPEX</b>", styles['TableHeader']),
        Paragraph("<b>Hurdle</b>", styles['TableHeader']),
    ]
    vg_rows = [
        vg_headers,
        [Paragraph("UEN-01", styles['TableCellBold']), Paragraph("Industrial AI & Cloud Platforms", styles['TableCell']), Paragraph("95.0", styles['TableCellBold']), Paragraph("28.5%", styles['TableCell']), Paragraph("4.64", styles['TableCell']), Paragraph("4.63", styles['TableCell']), Paragraph("Invest / Grow", styles['TableCellBold']), Paragraph("$24.0M", styles['TableCellBold']), Paragraph("18.0%", styles['TableCell'])],
        [Paragraph("UEN-02", styles['TableCellBold']), Paragraph("Surgical & Medical Robotics", styles['TableCell']), Paragraph("72.0", styles['TableCellBold']), Paragraph("24.0%", styles['TableCell']), Paragraph("4.61", styles['TableCell']), Paragraph("3.81", styles['TableCell']), Paragraph("Invest / Grow", styles['TableCellBold']), Paragraph("$18.5M", styles['TableCellBold']), Paragraph("18.0%", styles['TableCell'])],
        [Paragraph("UEN-03", styles['TableCellBold']), Paragraph("Power Electronics & Inverters", styles['TableCell']), Paragraph("110.0", styles['TableCellBold']), Paragraph("18.2%", styles['TableCell']), Paragraph("3.72", styles['TableCell']), Paragraph("4.20", styles['TableCell']), Paragraph("Invest / Grow", styles['TableCellBold']), Paragraph("$16.0M", styles['TableCellBold']), Paragraph("18.0%", styles['TableCell'])],
        [Paragraph("UEN-04", styles['TableCellBold']), Paragraph("Smart Factory Automation & Sensors", styles['TableCell']), Paragraph("68.0", styles['TableCell']), Paragraph("16.5%", styles['TableCell']), Paragraph("3.29", styles['TableCell']), Paragraph("3.49", styles['TableCell']), Paragraph("Selectivity / Hold", styles['TableCell']), Paragraph("$7.5M", styles['TableCell']), Paragraph("14.0%", styles['TableCell'])],
        [Paragraph("UEN-05", styles['TableCellBold']), Paragraph("Fleet Telematics & IoT Solutions", styles['TableCell']), Paragraph("35.0", styles['TableCell']), Paragraph("14.0%", styles['TableCell']), Paragraph("3.57", styles['TableCell']), Paragraph("2.72", styles['TableCell']), Paragraph("Selectivity / Hold", styles['TableCell']), Paragraph("$5.3M", styles['TableCell']), Paragraph("14.0%", styles['TableCell'])],
        [Paragraph("UEN-06", styles['TableCellBold']), Paragraph("HVAC & Thermal Systems", styles['TableCell']), Paragraph("42.0", styles['TableCell']), Paragraph("15.0%", styles['TableCell']), Paragraph("2.25", styles['TableCell']), Paragraph("4.09", styles['TableCell']), Paragraph("Selectivity / Hold", styles['TableCell']), Paragraph("$4.5M", styles['TableCell']), Paragraph("14.0%", styles['TableCell'])],
        [Paragraph("UEN-07", styles['TableCellBold']), Paragraph("Precision Machining & Aerospace Alloys", styles['TableCell']), Paragraph("25.0", styles['TableCell']), Paragraph("11.0%", styles['TableCell']), Paragraph("3.91", styles['TableCell']), Paragraph("1.98", styles['TableCell']), Paragraph("Selectivity / Hold", styles['TableCell']), Paragraph("$4.7M", styles['TableCell']), Paragraph("14.0%", styles['TableCell'])],
        [Paragraph("UEN-08", styles['TableCellBold']), Paragraph("Heavy Machinery Hydraulic Valves", styles['TableCell']), Paragraph("18.0", styles['TableCell']), Paragraph("8.5%", styles['TableCell']), Paragraph("2.64", styles['TableCell']), Paragraph("1.95", styles['TableCell']), Paragraph("Harvest / Divest", styles['TableCellBold']), Paragraph("$1.2M", styles['TableCell']), Paragraph("10.0%", styles['TableCell'])],
        [Paragraph("UEN-09", styles['TableCellBold']), Paragraph("Commodity Wiring & Industrial Cabling", styles['TableCell']), Paragraph("12.0", styles['TableCell']), Paragraph("6.0%", styles['TableCell']), Paragraph("1.90", styles['TableCell']), Paragraph("2.52", styles['TableCell']), Paragraph("Harvest / Divest", styles['TableCellBold']), Paragraph("$0.8M", styles['TableCell']), Paragraph("10.0%", styles['TableCell'])],
        [Paragraph("UEN-10", styles['TableCellBold']), Paragraph("Analog Switchboards & Legacy Meters", styles['TableCell']), Paragraph("8.0", styles['TableCell']), Paragraph("3.2%", styles['TableCell']), Paragraph("1.57", styles['TableCell']), Paragraph("1.60", styles['TableCell']), Paragraph("Harvest / Divest", styles['TableCellBold']), Paragraph("$0.2M", styles['TableCell']), Paragraph("10.0%", styles['TableCell'])],
    ]
    vg_table = Table(vg_rows, colWidths=[38, 145, 52, 45, 34, 34, 88, 45, 30])
    vg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY_DARK),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.0),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(vg_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.1. Financial Execution Impact of Datalaria's Rebalancing Plan", styles['SubHeading']))
    story.append(Paragraph(
        "• <b>Concentration in Winners (68% of Corporate CAPEX):</b> $51.0M allocated to SBUs 01, 02, and 03 to scale automated manufacturing and execute bolt-on M&A.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Discipline in Selectivity (27% of Corporate CAPEX):</b> SBUs 04, 05, 06, and 07 received $20.2M strictly conditioned on divisional EBITDA self-funding.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "• <b>Harvest & Divestment Exit:</b> Freezing non-regulatory CAPEX in SBUs 08, 09, and 10 ($2.2M total) initiates an M&A carve-out auction, unlocking $24M in cash by Q4 2026. "
        "Corporate ROIC expands from 11.2% to 15.0% (+380 bps) within 36 months.",
        styles['Bullet']
    ))

    story.append(Spacer(1, 3))
    story.append(build_callout(
        "<b>Shareholder Value Creation:</b> Eliminating the negative dragging effect of the 3 Red Zone units expands the corporate EV/EBITDA multiple "
        "by +2.1x, generating an estimated $92M in net equity value accretion.",
        styles, border_color=C_GREEN_ACCENT, bg_color=C_GREEN_LIGHT
    ))

    story.append(PageBreak())

    # ==========================
    # PAGE 5: BOARD DEFENSE PROTOCOL & FAQ
    # ==========================
    story.append(Paragraph("5. Boardroom Defense Protocol (C-Level FAQ)", styles['SecHeading']))
    story.append(Paragraph(
        "During Board meetings and investment committees, independent directors and institutional shareholders will raise tough questions. "
        "Below are five model responses grounded strictly in financial economics and corporate strategy:",
        styles['Body']
    ))

    faqs_en = [
        ("Q1: Why should the Board transition from the classic BCG matrix to the McKinsey / GE matrix if BCG is simpler?",
         "<b>C-Level Response:</b> The BCG matrix oversimplifies competitive reality by assuming high growth automatically equates to high profitability. "
         "In modern markets, high-growth sectors can generate zero economic profits if entry barriers are low. The McKinsey / GE matrix "
         "incorporates five structural market attractiveness factors and five competitive strength moats, preventing catastrophic capital misallocation into commodity traps."),

        ("Q2: How do we justify freezing CAPEX and divesting an SBU (Red Zone) that is still reporting positive accounting profits?",
         "<b>C-Level Response:</b> Accounting net income conceals active economic value destruction. If an SBU yields an ROIC of 6.0% "
         "while our corporate WACC is 8.8%, every dollar reinvested into its assets destroys 28 cents of shareholder wealth. Divesting or harvesting "
         "that unit releases trapped cash that can be redeployed into Green Zone platforms generating 24% to 31% ROIC."),

        ("Q3: How do we resolve the capital allocation dilemma along the Selectivity diagonal (double down vs. prepare for sale)?",
         "<b>C-Level Response:</b> The Selectivity diagonal requires a strict quantitative hurdle: if the unit has a verified, self-funding roadmap to capture "
         "leadership in a high-margin niche via its own EBITDA, investment is approved. If it requires continuous corporate subsidies without expanding "
         "its relative market share within 18 months, it is automatically reclassified for divestiture."),

        ("Q4: How do we defend against divisional managers claiming criterion weighting is subjective?",
         "<b>C-Level Response:</b> The model eliminates subjectivity by enforcing our 4-filter audit protocol, linking all ratings to audited third-party sources "
         "(Gartner, competitor financial filings). Furthermore, stress testing weights by &plusmn;20% proves that quadrant assignments remain stable, "
         "rendering strategic conclusions mathematically robust."),

        ("Q5: What is the measurable impact on corporate WACC and valuation multiple following Red Zone divestitures?",
         "<b>C-Level Response:</b> Divesting low-margin, mature divisions reduces net leverage, expands interest coverage ratios (ICR), "
         "and compresses the group's asset beta, lowering our corporate WACC by 40-60 bps while unlocking a 2.1x expansion in corporate EV/EBITDA multiples."),
    ]

    for q, a in faqs_en:
        story.append(Paragraph(q, styles['FAQ_Q']))
        story.append(Paragraph(a, styles['FAQ_A']))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Canonical References & Academic Literature", styles['SubHeading']))
    bibs_en = [
        "• McKinsey & Company (1971): <i>Strategic Business Planning: The Multifactor Portfolio Matrix</i>, McKinsey Staff Paper Series, New York.",
        "• Day, George S. (1977): <i>Diagnosing the Product Portfolio</i>, Journal of Marketing, Vol. 41, No. 2, pp. 29-38.",
        "• Haspeslagh, Philippe (1982): <i>Portfolio Planning: Uses and Limits</i>, Harvard Business Review, Vol. 60, No. 1, pp. 58-73.",
        "• Henderson, Bruce D. (1979): <i>Henderson on Corporate Strategy</i>, Boston Consulting Group / Abt Books, Cambridge, MA.",
    ]
    for b in bibs_en:
        story.append(Paragraph(b, styles['Biblio']))

    # Document compilation
    canvas_obj = NumberedCanvas
    # Set language attribute on canvas
    class LangCanvas(NumberedCanvas):
        _lang = 'EN'

    doc.build(story, canvasmaker=LangCanvas)
    print(f"[OK] English PDF Guide generated: {out_path}")
    return out_path


def main():
    print("Iniciando construcción de guías metodológicas en PDF (ReportLab)...")
    es_path = os.path.join(DIR_PACKAGES, "ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf")
    en_path = os.path.join(DIR_PACKAGES, "EN_McKinsey_GE_Matrix_Methodology_Guide.pdf")

    generate_pdf_es(es_path)
    generate_pdf_en(en_path)

    # Copias en carpetas específicas
    dir_es = os.path.join(DIR_PACKAGES, "[ES]_Matriz_McKinsey_GE")
    dir_en = os.path.join(DIR_PACKAGES, "[EN]_McKinsey_GE_Matrix")
    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    generate_pdf_es(os.path.join(dir_es, "ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf"))
    generate_pdf_en(os.path.join(dir_en, "EN_McKinsey_GE_Matrix_Methodology_Guide.pdf"))

    print("Guías metodológicas PDF completadas exitosamente.")


if __name__ == "__main__":
    main()
