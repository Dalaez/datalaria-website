#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py
===============
Genera las guías metodológicas oficiales en PDF (5 páginas exactas) para el Executive Decision Pack PERT:
1. packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[ES]_Estimacion_PERT_3_Puntos/Guia_Metodologica_PERT_ES.pdf
2. packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[EN]_3Point_PERT_Estimation/Methodology_Guide_PERT_EN.pdf

Estándar editorial de alta dirección (PMBOK 7th / TOC / Operations Research / McKinsey Minto Pyramid):
- Página 1: Portada ejecutiva, metadatos y Sección 1 (La Falacia de la Estimación Determinista).
- Página 2: Sección 2 (Fundamentación Matemática: Distribución Beta, CLT, Z-Score y Ecuaciones Canónicas).
- Página 3: Sección 3 (Protocolo de Entrevista para Calibrar los 3 Puntos: Eliminación de Sesgos de Anclaje).
- Página 4: Sección 4 (Caso de Estudio Realista: Transformación Digital Core, Z-Score 34% a 90% y Crashing).
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
            header_right = ("ESTIMACIÓN PERT DE 3 PUNTOS & RIESGO DE CRONOGRAMA"
                            if lang == 'ES' else
                            "3-POINT PERT ESTIMATION & SCHEDULE RISK PROBABILITY")
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
        footer_left = ("Datalaria.com • Documento Confidencial para Comité de Dirección & Auditoría de Proyectos"
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
        base_dir = "packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos"
        sub_dir = "[ES]_Estimacion_PERT_3_Puntos" if lang == 'ES' else "[EN]_3Point_PERT_Estimation"
        fname = "Guia_Metodologica_PERT_ES.pdf" if lang == 'ES' else "Methodology_Guide_PERT_EN.pdf"
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
    # PÁGINA 1: PORTADA & SECCIÓN 1 (LA FALACIA DETERMINISTA)
    # =========================================================================
    kicker_txt = "DATALARIA EXECUTIVE DECISION PACK · PMBOK 7th / OPERATIONS RESEARCH" if lang == 'ES' else "DATALARIA EXECUTIVE DECISION PACK · PMBOK 7th / OPERATIONS RESEARCH"
    story.append(Paragraph(kicker_txt, styles['CoverKicker']))

    title_txt = "Estimación PERT de 3 Puntos Estocástica & Probabilidad de Cronograma" if lang == 'ES' else "Stochastic 3-Point PERT Estimation & Schedule Risk Probability"
    story.append(Paragraph(title_txt, styles['CoverTitle']))

    sub_txt = "De la ilusión determinista a la certeza matemática: Distribución Beta, Teorema del Límite Central, curvas S de probabilidad y dimensionamiento científico de buffers ante el Consejo de Administración." if lang == 'ES' else "Overcoming deterministic schedule illusion with mathematical rigor: Beta Distribution, Central Limit Theorem, S-Curve probabilities, and scientific buffer sizing for Executive Boards."
    story.append(Paragraph(sub_txt, styles['CoverSub']))

    # Metadata Card
    meta_data = [
        [
            Paragraph("<b>Área:</b> Control Operativo & PMO" if lang == 'ES' else "<b>Domain:</b> Operations & PMO Governance", styles['TableCell']),
            Paragraph("<b>Estándar:</b> PMBOK 7th / TOC / CLT" if lang == 'ES' else "<b>Standard:</b> PMBOK 7th / TOC / CLT", styles['TableCell']),
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
    sec1_title = "1. La Falacia de la Estimación Determinista a un Solo Punto" if lang == 'ES' else "1. The Fallacy of Deterministic Single-Point Estimation"
    story.append(Paragraph(sec1_title, styles['SecHeading']))

    p1_1 = (
        "En los comités de dirección ejecutiva y consejos de administración, la gran mayoría de proyectos estratégicos de ingeniería, software o infraestructura incurren en retrasos y sobrecostes sistemáticos. Este fenómeno patológico no obedece principalmente a la incompetencia técnica, sino a una debilidad estructural en el método de planificación: <b>la falacia de la estimación determinista a un solo punto</b>. Al solicitar a un equipo técnico que comprometa 'una fecha exacta', la organización ignora las leyes fundamentales de la teoría de colas y la varianza estocástica."
        if lang == 'ES' else
        "In executive boardrooms and steering committees, the overwhelming majority of strategic engineering, software, and capital projects experience systematic schedule slippages and cost overruns. This breakdown does not stem from technical incompetence, but from a fatal methodology flaw: <b>the fallacy of deterministic single-point estimation</b>. By forcing engineering leads to commit to a single static deadline, organizations ignore the fundamental mathematics of queuing theory and stochastic variance."
    )
    story.append(Paragraph(p1_1, styles['Body']))

    p1_2 = (
        "La gestión determinista colapsa ante tres trampas operacionales ampliamente documentadas en la literatura de investigación operativa (Goldratt, 1997; Meredith & Mantel, 2011):"
        if lang == 'ES' else
        "Deterministic project scheduling collapses under three behavioral and structural traps thoroughly proven in operations research (Goldratt, 1997; Meredith & Mantel, 2011):"
    )
    story.append(Paragraph(p1_2, styles['Body']))

    b1_items_es = [
        "<b>La Ley de Parkinson:</b> El trabajo se expande automáticamente hasta llenar el tiempo total disponible para su realización. Cuando un desarrollador o contratista finaliza antes de lo previsto, rara vez entrega anticipadamente; consume el colchón informal por perfeccionismo secundario.",
        "<b>El Síndrome del Estudiante:</b> Las personas postergan el esfuerzo concentrado hasta el último momento posible antes de la fecha límite. Cualquier contingencia imprevista en la fase final impacta de inmediato en la fecha de entrega sin margen de absorción.",
        "<b>Asimetría Estructural de las Rutas Críticas:</b> En un cronograma interconectado, las holguras ganadas rara vez se transfieren hacia adelante, pero los retrasos en el camino crítico se acumulan con una probabilidad del 100%. Trabajar con el valor más probable (<i>m</i>) deja al proyecto con solo un 50% (o inferior) de probabilidad de éxito antes de empezar."
    ]
    b1_items_en = [
        "<b>Parkinson's Law:</b> Work expands to fill the entire time allocated for its completion. When an engineer or vendor finishes ahead of schedule, they rarely report early handover; the invisible buffer is absorbed by secondary polish.",
        "<b>Student Syndrome:</b> Teams delay focused execution until the final possible moment before the milestone. Any unexpected shock occurring near delivery immediately causes a hard delay with zero absorption capacity.",
        "<b>Structural Asymmetry of Critical Paths:</b> In complex dependency graphs, early gains are rarely passed forward, whereas delays on the critical path accumulate with 100% transmission. Relying on the 'most likely' estimate (<i>m</i>) yields at best a 50% coin-toss probability of success before work even begins."
    ]
    b1_items = b1_items_es if lang == 'ES' else b1_items_en
    for bi in b1_items:
        story.append(Paragraph(f"• {bi}", styles['Bullet']))

    story.append(Spacer(1, 4))
    callout_p1 = [
        [Paragraph(
            "<b>Mandato Directivo:</b> Un Director General o Sponsor que exige 'una fecha fija sin rangos' no está exigiendo rigor; está forzando a sus ingenieros a ocultar la incertidumbre bajo capas informales de colchón o a asumir un riesgo no asegurado que destruirá la credibilidad del comité."
            if lang == 'ES' else
            "<b>Executive Mandate:</b> A CEO or Sponsor demanding a 'single static date without ranges' is not enforcing accountability; they are compelling teams to hide variance behind informal padding or assume unhedged delivery risks that destroy executive credibility.",
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
    # PÁGINA 2: SECCIÓN 2 (FUNDAMENTACIÓN MATEMÁTICA Y CLT)
    # =========================================================================
    sec2_title = "2. Fundamentación Matemática y Estadística del Modelo PERT" if lang == 'ES' else "2. Mathematical and Statistical Foundations of the PERT Model"
    story.append(Paragraph(sec2_title, styles['SecHeading']))

    p2_1 = (
        "Desarrollada originalmente por la Oficina de Proyectos Especiales de la Armada de EE.UU. y Booz Allen Hamilton (Malcolm et al., 1959) para el programa de misiles Polaris, la técnica PERT sustituye el punto único por una función de densidad continua modelada mediante la <b>Distribución Beta</b>, parametrizada a través de tres puntos:"
        if lang == 'ES' else
        "Originally engineered by the US Navy Special Projects Office and Booz Allen Hamilton (Malcolm et al., 1959) for the Polaris submarine missile program, PERT replaces single-point dates with a continuous probability density function parameterized via the <b>Beta Distribution</b> using three points:"
    )
    story.append(Paragraph(p2_1, styles['Body']))

    story.append(Paragraph(
        "<b>1. Estimación Optimista (<i>o</i>):</b> Duración mínima si absolutamente todas las condiciones operativas resultan excepcionalmente favorables (percentil 5%).<br/>"
        "<b>2. Estimación Más Probable (<i>m</i>):</b> Moda de la distribución; la duración más frecuente bajo condiciones estándar de trabajo.<br/>"
        "<b>3. Estimación Pesimista (<i>p</i>):</b> Duración máxima en el peor escenario operativo previsible, excluyendo eventos de fuerza mayor catastróficos (percentil 95%)."
        if lang == 'ES' else
        "<b>1. Optimistic Estimate (<i>o</i>):</b> Minimum duration if all operational conditions unfold exceptionally well (5th percentile).<br/>"
        "<b>2. Most Likely Estimate (<i>m</i>):</b> Mode of the distribution; the most frequent duration under normal operating conditions.<br/>"
        "<b>3. Pessimistic Estimate (<i>p</i>):</b> Maximum duration in worst-case scenario, excluding extreme force majeure catastrophes (95th percentile).",
        styles['Body']
    ))

    # Tabla de Fórmulas Canónicas
    formula_data = [
        [Paragraph("<b>PARÁMETRO</b>", styles['TableHeader']), Paragraph("<b>ECUACIÓN CANÓNICA PERT</b>", styles['TableHeader']), Paragraph("<b>INTERPRETACIÓN DIRECTIVA</b>", styles['TableHeader'])],
        [Paragraph("Duración Esperada (μ_i)", styles['TableCellBold']), Paragraph("<b>μ_i = (o + 4m + p) / 6</b>", styles['MathBox']), Paragraph("Media ponderada que asigna un peso de 66.7% al valor más probable y 16.7% a cada extremo.", styles['TableCell'])],
        [Paragraph("Desviación Estándar (σ_i)", styles['TableCellBold']), Paragraph("<b>σ_i = (p - o) / 6</b>", styles['MathBox']), Paragraph("Medida de dispersión individual. Asume que el rango [o, p] abarca 6 desviaciones estándar.", styles['TableCell'])],
        [Paragraph("Varianza Individual (σ_i²)", styles['TableCellBold']), Paragraph("<b>σ_i² = [ (p - o) / 6 ]²</b>", styles['MathBox']), Paragraph("Grado de incertidumbre cuadrática acumulable en el camino crítico del cronograma.", styles['TableCell'])],
        [Paragraph("Duración Agregada (CLT)", styles['TableCellBold']), Paragraph("<b>μ_total = Σ μ_crit</b>", styles['MathBox']), Paragraph("Suma lineal de las duraciones esperadas de las tareas pertenecientes al camino crítico.", styles['TableCell'])],
        [Paragraph("Varianza Agregada (CLT)", styles['TableCellBold']), Paragraph("<b>σ²_total = Σ σ²_crit</b>", styles['MathBox']), Paragraph("Teorema del Límite Central: Las varianzas de tareas independientes se suman cuadráticamente.", styles['TableCell'])],
        [Paragraph("Desviación Global (σ_total)", styles['TableCellBold']), Paragraph("<b>σ_total = √( Σ σ²_crit )</b>", styles['MathBox']), Paragraph("Dispersión global del proyecto. Raíz cuadrada de la varianza combinada.", styles['TableCell'])],
        [Paragraph("Puntuación Z (Z-Score)", styles['TableCellBold']), Paragraph("<b>Z = (T_d - μ_total) / σ_total</b>", styles['MathBox']), Paragraph("Número de desviaciones estándar entre la fecha directiva objetivo (T_d) y la media del proyecto.", styles['TableCell'])],
        [Paragraph("Probabilidad de Éxito", styles['TableCellBold']), Paragraph("<b>P(T ≤ T_d) = Φ( Z )</b>", styles['MathBox']), Paragraph("Función de distribución normal acumulada evaluada en el valor Z obtenido.", styles['TableCell'])],
    ]
    t_form = Table(formula_data, colWidths=[110, 165, 236])
    t_form.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_form)
    story.append(Spacer(1, 6))

    p2_2 = (
        "<b>El Teorema del Límite Central (CLT) y la Curva de Campana:</b> Aunque las tareas individuales sigan distribuciones Beta marcadamente asimétricas, el CLT demuestra que la distribución de la suma de variables aleatorias independientes converge rápidamente hacia una <b>Distribución Normal Gaussiana</b>. Esto habilita el cálculo exacto de fechas para cualquier nivel de certidumbre directiva requerido (por ejemplo, P90 o P95)."
        if lang == 'ES' else
        "<b>The Central Limit Theorem (CLT) and Bell-Shaped Convergence:</b> Even when individual tasks follow heavily skewed Beta distributions, the CLT guarantees that the sum of independent random variables converges toward a <b>Gaussian Normal Distribution</b>. This allows exact calculation of completion dates for any target confidence threshold (such as P90 or P95)."
    )
    story.append(Paragraph(p2_2, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: SECCIÓN 3 (PROTOCOLO DE ENTREVISTA 3 PUNTOS)
    # =========================================================================
    sec3_title = "3. Protocolo de Entrevista para Calibrar los 3 Puntos sin Sesgos" if lang == 'ES' else "3. Interview Protocol for Bias-Free 3-Point Calibration"
    story.append(Paragraph(sec3_title, styles['SecHeading']))

    p3_1 = (
        "La precisión de un modelo PERT depende críticamente de la pureza de las entradas <i>(o, m, p)</i>. Si el project manager interroga a sus ingenieros con preguntas convencionales como '¿cuánto vas a tardar?', se activan dos sesgos cognitivos devastadores: <b>el sesgo de anclaje</b> (fijarse en la primera cifra mencionada) y <b>el sesgo de deseabilidad social</b> (complacer al superior jerárquico). Para neutralizarlos, se debe aplicar el siguiente protocolo de interrogatorio estructurado:"
        if lang == 'ES' else
        "The mathematical power of PERT relies entirely on the integrity of inputs <i>(o, m, p)</i>. Inquiring with casual questions such as 'how long will this take?' instantly triggers two cognitive traps: <b>anchoring bias</b> (fixating on the first uttered number) and <b>social desirability bias</b> (aiming to appease senior leadership). To neutralize these traps, the PMO must follow a structured elicitation protocol:"
    )
    story.append(Paragraph(p3_1, styles['Body']))

    steps_es = [
        ("Paso 1: Interrogar el Escenario Más Probable (m)", "Definir la línea de base operativa: 'Asumiendo que no surjan incidencias extraordinarias y el equipo trabaje a ritmo nominal, ¿cuál es el plazo típico de ejecución?'. Registrar este valor como ancla modal provisoria."),
        ("Paso 2: Aislamiento del Escenario Pesimista (p) [Técnica Pre-Mortem]", "Romper el optimismo ingenuo obligando a la mente a situarse en el futuro fallido: 'Imagina que el proyecto ha descarrilado por completo en este módulo: la API externa falló, el proveedor cambió de interlocutor y la migración corrompió datos. Sin invocar catástrofes irreales como guerras o incendios, ¿cuánto tardaría en resolverse bajo fricción operativa real?'. Asignar p al percentil 95% (solo 1 de cada 20 veces se superaría)."),
        ("Paso 3: Aislamiento del Escenario Optimista (o)", "Determinar la frontera de velocidad máxima: 'Si los contratos se firman en 24 horas, no hay deuda técnica y las dependencias responden al instante, ¿cuál es el mínimo absoluto físicamente posible?'. Asignar o al percentil 5%."),
        ("Paso 4: Auditoría del Ratio de Asimetría (Skewness)", "Verificar si (p - m) > (m - o). En el 90% de proyectos tecnológicos y de construcción, el sesgo a la derecha es pronunciado: la distancia al peor escenario multiplica por 2 o 3 la distancia al mejor escenario. Si un estimador presenta un rango simétrico artificial (ej. o=8, m=10, p=12), se debe auditar exhaustivamente por probable complacencia superficial.")
    ]
    steps_en = [
        ("Step 1: Eliciting the Most Likely Scenario (m)", "Establish the operating baseline: 'Assuming standard staffing, ordinary cadence, and no major shocks, what is the most frequent duration?'. Record this as the preliminary modal baseline."),
        ("Step 2: Isolating the Pessimistic Scenario (p) [Pre-Mortem Technique]", "Disrupt naive optimism by conducting a micro pre-mortem: 'Imagine this deliverable has suffered severe friction: vendor turnover, breaking API changes, and data migration errors. Excluding unrealistic acts of God, what is the realistic worst-case duration?'. Set p at the 95th percentile (exceeded only 1 in 20 times)."),
        ("Step 3: Isolating the Optimistic Scenario (o)", "Establish the absolute speed ceiling: 'If procurement clears in 24 hours, zero tech debt is encountered, and dependencies deliver flawlessly, what is the absolute physical minimum duration?'. Set o at the 5th percentile."),
        ("Step 4: Skewness Ratio Audit", "Evaluate whether (p - m) > (m - o). In over 90% of engineering and capital projects, risk is heavily right-skewed: the distance to the worst case is 2 to 3 times greater than the gain to the best case. If an engineer provides a perfectly symmetric range (e.g. o=8, m=10, p=12), challenge it for superficial complacency.")
    ]
    st_data = steps_es if lang == 'ES' else steps_en
    for s_title, s_desc in st_data:
        story.append(Paragraph(f"<b>{s_title}:</b> {s_desc}", styles['Body']))
        story.append(Spacer(1, 2))

    # Comparativa Beta vs Triangular
    p3_comp = (
        "<b>Beta PERT frente a Distribución Triangular:</b> Mientras la distribución triangular calcula la media simple μ_tri = (o + m + p)/3, el modelo Beta PERT pondera el valor más probable por cuatro, suavizando los extremos exagerados. Cuando la asimetría es extrema, la media Beta protege el cronograma contra la sobre-reacción a escenarios remotos sin ignorar el riesgo de cola."
        if lang == 'ES' else
        "<b>Beta PERT versus Triangular Distribution:</b> While triangular distributions calculate an unweighted average μ_tri = (o + m + p)/3, Beta PERT assigns a weight of 4 to the modal value, softening unrealistic tails. In high-uncertainty initiatives, Beta PERT protects the schedule from over-reacting to extreme remote cases while capturing critical tail risk."
    )
    story.append(Paragraph(p3_comp, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: SECCIÓN 4 (CASO DE ESTUDIO REALISTA)
    # =========================================================================
    sec4_title = "4. Caso de Estudio: Plataforma Transaccional Core & Reducción de Riesgo" if lang == 'ES' else "4. Enterprise Case Study: Core Transactional Platform & Risk Mitigation"
    story.append(Paragraph(sec4_title, styles['SecHeading']))

    p4_1 = (
        "<b>El Contexto del Proyecto:</b> Una entidad financiera corporativa inicia la modernización de su motor transaccional de pagos y conector ERP (25 paquetes de trabajo WBS, 15 en el camino crítico). El Sponsor de Negocio exigió inicialmente un plazo de entrega cerrado de <b>125 días hábiles (6 meses calendario)</b> bajo la creencia determinista de que la suma de estimaciones estándar cumplía el hito."
        if lang == 'ES' else
        "<b>Project Context:</b> A financial institution launches a major overhaul of its core transactional clearing engine and ERP integration (25 WBS work packages, 15 on the critical path). The Business Sponsor initially demanded a fixed deadline of <b>125 business days (6 calendar months)</b> based on naive addition of standard estimates."
    )
    story.append(Paragraph(p4_1, styles['Body']))

    p4_2 = (
        "<b>El Diagnóstico Estocástico Datalaria:</b> Al aplicar el modelo PERT de 3 puntos y agregar las varianzas en el camino crítico mediante CLT, el modelo arrojó los siguientes parámetros reales:"
        if lang == 'ES' else
        "<b>The Datalaria Stochastic Audit:</b> Applying 3-point PERT estimation and aggregating critical path variances via CLT revealed the underlying statistical reality:"
    )
    story.append(Paragraph(p4_2, styles['Body']))

    case_kpis = [
        [Paragraph("<b>PARÁMETRO AUDITADO</b>", styles['TableHeader']), Paragraph("<b>VALOR DETERMINISTA</b>", styles['TableHeader']), Paragraph("<b>VALOR ESTOCÁSTICO REAL</b>", styles['TableHeader']), Paragraph("<b>DIAGNÓSTICO DIRECTIVO</b>", styles['TableHeader'])],
        [Paragraph("Duración Esperada (μ)", styles['TableCellBold']), Paragraph("125.0 días", styles['TableCell']), Paragraph("<b>132.5 días</b>", styles['TableCellBold']), Paragraph("Déficit base de 7.5 días respecto a la media real.", styles['TableCell'])],
        [Paragraph("Desviación Estándar (σ)", styles['TableCellBold']), Paragraph("0.0 días (ignorado)", styles['TableCell']), Paragraph("<b>11.8 días</b>", styles['TableCellBold']), Paragraph("Rango ±2σ entre 108.9 y 156.1 días.", styles['TableCell'])],
        [Paragraph("Z-Score en Fecha 125d", styles['TableCellBold']), Paragraph("N/A", styles['TableCell']), Paragraph("<b>Z = -0.41</b>", styles['TableCellBold']), Paragraph("La fecha exigida se sitúa a la izquierda de la media.", styles['TableCell'])],
        [Paragraph("Probabilidad de Éxito", styles['TableCellBold']), Paragraph("100% (falsa certidumbre)", styles['TableCell']), Paragraph("<b>34.2% ÉXITO</b>", styles['TableCellBold']), Paragraph("🔴 65.8% de probabilidad de fracaso público.", styles['TableCell'])],
        [Paragraph("Fecha P90 (Board Goal)", styles['TableCellBold']), Paragraph("N/A", styles['TableCell']), Paragraph("<b>147.6 días</b>", styles['TableCellBold']), Paragraph("Fecha recomendada con 90% de certidumbre formal.", styles['TableCell'])],
    ]
    t_case = Table(case_kpis, colWidths=[120, 100, 110, 181])
    t_case.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY_DARK),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG_CARD]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_case)
    story.append(Spacer(1, 6))

    p4_3 = (
        "<b>La Solución Implementada:</b> En lugar de ocultar el riesgo o prometer plazos imposibles, el equipo presentó la Curva de Campana ante el Comité de Dirección y ejecutó dos palancas complementarias:<br/>"
        "<b>1. Formalización de Project Buffer P90:</b> Se acordó una fecha objetivo contractual en 148 días, dotando un colchón visible de 15.1 días gobernado por la PMO.<br/>"
        "<b>2. Plan de Crashing Selectivo:</b> Se pre-autorizó una partida de 38.000 € en las 3 tareas con menor coste marginal de reducción (Pruebas UAT, Pasarelas Bancarias y Motor de Conciliación), permitiendo recuperar hasta 11 días en caso de que el buffer penetre en Zona Ámbar.<br/>"
        "<b>Resultado:</b> El proyecto se entregó en 141 días hábiles, absorbiendo dos bloqueos regulatorios graves y finalizando 7 días antes del compromiso P90 sin sobrecostes de emergencia."
        if lang == 'ES' else
        "<b>The Implemented Solution:</b> Instead of concealing uncertainty, the team presented the Bell Curve to the Steering Committee and activated two strategic levers:<br/>"
        "<b>1. Formal P90 Project Buffer Adoption:</b> Delivery commitment was formally set at 148 days, establishing a transparent 15.1-day buffer governed by the PMO.<br/>"
        "<b>2. Targeted Crashing Contingency:</b> Pre-approved $38,000 budget deployed on the top 3 high-yield critical tasks (UAT Testing, Banking Gateway, Core Engine), unlocking up to 11 recovery days if buffer penetration reached Amber.<br/>"
        "<b>Result:</b> The project went live in 141 business days, successfully absorbing two unexpected banking regulatory delays and finishing 7 days ahead of the P90 commitment with zero crisis budget spikes."
    )
    story.append(Paragraph(p4_3, styles['Body']))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: SECCIÓN 5 (BOARDROOM FAQ) & BIBLIOGRAFÍA CANÓNICA
    # =========================================================================
    sec5_title = "5. Protocolo de Defensa en Comité (Boardroom FAQ) & Bibliografía" if lang == 'ES' else "5. Boardroom Defense Protocol (Executive FAQ) & References"
    story.append(Paragraph(sec5_title, styles['SecHeading']))

    faq_data_es = [
        ("FAQ 1: '¿Por qué no podemos trabajar directamente con la fecha más probable (m)?'",
         "<b>Argumentación C-Level:</b> Trabajar con el valor más probable asume una distribución simétrica perfecta donde nada falla. Debido a la asimetría positiva de los riesgos técnicos, el valor modal (m) suele coincidir con un percentil inferior al 40-50%. Comprometerse con 'm' equivale a aceptar voluntariamente una probabilidad de fracaso superior al 50% ante clientes y accionistas."),
        ("FAQ 2: '¿Cómo explicar al CEO que sumar los peores escenarios (p) es absurdo?'",
         "<b>Argumentación C-Level:</b> Sumar aritméticamente todas las estimaciones pesimistas asume que absolutamente todos los riesgos independientes ocurrirán de forma simultánea. La probabilidad conjunta de que 15 tareas independientes alcancen su percentil 95% es (0.05)^15 ≈ 3 × 10^-20 (virtualmente cero). El Teorema del Límite Central demuestra que la incertidumbre agregada crece con la raíz de las varianzas (√Σσ²), no con la suma lineal de desvíos."),
        ("FAQ 3: '¿Qué nivel de certidumbre (80%, 90% o 95%) debe exigir el Consejo?'",
         "<b>Argumentación C-Level:</b> Proyectos internos ágiles toleran P75-P80. Para proyectos de escala corporativa con compromisos contractuales y dependencias comerciales cruzadas, el estándar internacional Tier-1 exige el percentil <b>P90 (1.282σ)</b>. Umbrales superiores (P95-P99) solo se justifican en misiones críticas o bajo penalizaciones contractuales exorbitantes.")
    ]
    faq_data_en = [
        ("FAQ 1: 'Why can't we simply commit to the Most Likely (m) date?'",
         "<b>Executive Defense:</b> Committing to 'm' implicitly assumes a perfectly symmetrical world where zero shocks occur. Due to positive technical risk skewness, the mode typically corresponds to a percentile below 40-50%. Promising 'm' is mathematically equivalent to accepting an unhedged >50% failure rate before stakeholders."),
        ("FAQ 2: 'How to explain to the CEO that summing worst-case scenarios (p) is absurd?'",
         "<b>Executive Defense:</b> Linearly adding all pessimistic estimates assumes that every independent risk materializes simultaneously. The joint probability of 15 independent tasks hitting their 95th percentile is (0.05)^15 ≈ 3 × 10^-20 (virtually zero). Central Limit Theorem proves that aggregate uncertainty grows with the square root of variances (√Σσ²), not line-item addition."),
        ("FAQ 3: 'What certainty threshold (80%, 90%, or 95%) should the Board require?'",
         "<b>Executive Defense:</b> Internal agile iterations can tolerate P75-P80. For enterprise-scale transformation projects with contractual milestones and commercial commitments, Tier-1 corporate governance demands <b>P90 (1.282σ)</b>. Extreme thresholds (P95-P99) are reserved for life-critical or catastrophic penalty environments.")
    ]
    f_data = faq_data_es if lang == 'ES' else faq_data_en

    for q, a in f_data:
        story.append(Paragraph(q, styles['FAQ_Q']))
        story.append(Paragraph(a, styles['FAQ_A']))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Referencias Bibliográficas Canónicas de Autoridad" if lang == 'ES' else "Canonical References & Authoritative Bibliography", styles['SubHeading']))

    bib_items = [
        "1. <b>Project Management Institute (PMI) (2021).</b> <i>A Guide to the Project Management Body of Knowledge (PMBOK Guide) – 7th Edition: Schedule & Measurement Performance Domains</i>. PMI, Newtown Square, PA.",
        "2. <b>Malcolm, D. G., Roseboom, J. H., Clark, C. E., & Fazar, W. (1959).</b> <i>Application of a Technique for Research and Development Program Evaluation (PERT)</i>. Operations Research, Vol. 7, No. 5, pp. 646–669.",
        "3. <b>Goldratt, Eliyahu M. (1997).</b> <i>Critical Chain</i>. The North River Press, Great Barrington, MA.",
        "4. <b>Meredith, Jack R., & Mantel, Samuel J. (2011).</b> <i>Project Management: A Managerial Approach (8th Edition)</i>. John Wiley & Sons, Hoboken, NJ.",
        "5. <b>Kerzner, Harold (2017).</b> <i>Project Management: A Systems Approach to Planning, Scheduling, and Controlling (12th Edition)</i>. John Wiley & Sons.",
        "6. <b>Minto, Barbara (2009).</b> <i>The Pyramid Principle: Logic in Writing and Thinking</i>. Financial Times / Prentice Hall, London."
    ]
    for b in bib_items:
        story.append(Paragraph(b, styles['Biblio']))

    # Construir documento
    doc.build(story, canvasmaker=NumberedCanvas)
    return out_path


def main():
    base_dir = "packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos"
    dir_es = os.path.join(base_dir, "[ES]_Estimacion_PERT_3_Puntos")
    dir_en = os.path.join(base_dir, "[EN]_3Point_PERT_Estimation")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    pdf_es = os.path.join(dir_es, "Guia_Metodologica_PERT_ES.pdf")
    pdf_en = os.path.join(dir_en, "Methodology_Guide_PERT_EN.pdf")

    print("[1/2] Generando Guía Metodológica en PDF (Español)...")
    build_guide_pdf(lang='ES', out_path=pdf_es)
    print(f" -> Guardado exitosamente: {pdf_es}")

    print("[2/2] Generando Guía Metodológica en PDF (Inglés)...")
    build_guide_pdf(lang='EN', out_path=pdf_en)
    print(f" -> Guardado exitosamente: {pdf_en}")

    print("Proceso PDF completado con éxito.")


if __name__ == "__main__":
    main()
