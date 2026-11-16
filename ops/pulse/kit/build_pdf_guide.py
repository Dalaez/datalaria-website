"""
ops/pulse/kit/build_pdf_guide.py
--------------------------------
Generador programático de la Guía Ejecutiva de Datalaria Pulse en formato PDF A4 (5 páginas)
disponible en edición dual Español (ES) e Inglés (EN) utilizando PyMuPDF (fitz) con
fuentes TrueType UTF-8 y cajas con ajuste automático de línea y guardas anti-desbordamiento.

Especificación: Hitos 6.3, P-LAUNCH-3B y P-LAUNCH-3C (specs/apps/pulse/spec.md).
Produce:
  - packages/pulse/GUIA_EJECUTIVA_PULSE_ES.pdf (y alias GUIA_EJECUTIVA_PULSE.pdf)
  - packages/pulse/PULSE_EXECUTIVE_GUIDE_EN.pdf
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import fitz  # PyMuPDF

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
OUTPUT_PDF_ES = ROOT_DIR / "packages" / "pulse" / "GUIA_EJECUTIVA_PULSE_ES.pdf"
OUTPUT_PDF_EN = ROOT_DIR / "packages" / "pulse" / "PULSE_EXECUTIVE_GUIDE_EN.pdf"
OUTPUT_PDF_LEGACY = ROOT_DIR / "packages" / "pulse" / "GUIA_EJECUTIVA_PULSE.pdf"

# Geometría estricta A4 (595 x 842 pt) con márgenes de seguridad
PAGE_W = 595.0
PAGE_H = 842.0
MARGIN_X0 = 40.0
MARGIN_X1 = 555.0  # Cumple x1 <= 555 en todo el documento (ancho útil 515 pt)

# Paleta corporativa Datalaria
DARK_BG = (0.043, 0.059, 0.090)       # #0b0f17
DARK_CARD = (0.075, 0.106, 0.169)     # #131b2b
DARK_BORDER = (0.145, 0.200, 0.298)   # #25334c
EMERALD = (0.063, 0.725, 0.506)       # #10b981
EMERALD_DARK = (0.016, 0.471, 0.341)  # #047857
CYAN = (0.024, 0.714, 0.831)          # #06b6d4
VIOLET = (0.545, 0.361, 0.965)        # #8b5cf6
AMBER = (0.961, 0.620, 0.043)         # #f59e0b
ROSE = (0.937, 0.267, 0.267)          # #ef4444
TEXT_LIGHT = (0.976, 0.980, 0.984)    # #f8fafc
TEXT_MUTED_DARK = (0.796, 0.835, 0.882)  # #cbd5e1
SLATE_900 = (0.059, 0.090, 0.165)     # #0f172a
SLATE_700 = (0.200, 0.255, 0.333)     # #334155
SLATE_500 = (0.392, 0.455, 0.545)     # #64748b
CARD_LIGHT = (0.969, 0.980, 0.988)    # #f7fafc
BORDER_LIGHT = (0.859, 0.898, 0.941)  # #dbe5f0
EMERALD_BG = (0.925, 0.992, 0.961)    # #ecfdf5
CYAN_BG = (0.925, 0.996, 1.000)       # #ecfeff
AMBER_BG = (1.000, 0.984, 0.922)      # #fffbeb


@dataclass(frozen=True)
class FontBundle:
    regular: str
    bold: str
    mono: str
    has_ttf: bool


def _resolve_ttf_candidates() -> Tuple[Optional[Path], Optional[Path], Optional[Path]]:
    """Localiza fuentes TrueType UTF-8 en Windows o Linux para renderizar €, acentos y guiones."""
    reg_candidates = [
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    ]
    bold_candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    ]
    mono_candidates = [
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
    ]
    reg = next((p for p in reg_candidates if p.exists()), None)
    bold = next((p for p in bold_candidates if p.exists()), reg)
    mono = next((p for p in mono_candidates if p.exists()), reg)
    return reg, bold, mono


def register_page_fonts(page: fitz.Page) -> FontBundle:
    """Registra fuentes UTF-8 en la página actual y devuelve sus alias."""
    reg, bold, mono = _resolve_ttf_candidates()
    if reg and bold and mono:
        page.insert_font(fontname="pulse_reg", fontfile=str(reg))
        page.insert_font(fontname="pulse_bold", fontfile=str(bold))
        page.insert_font(fontname="pulse_mono", fontfile=str(mono))
        return FontBundle(regular="pulse_reg", bold="pulse_bold", mono="pulse_mono", has_ttf=True)
    return FontBundle(regular="helv", bold="hebo", mono="cour", has_ttf=False)


def draw_textbox(
    page: fitz.Page,
    rect: fitz.Rect,
    text: str,
    *,
    fontname: str,
    fontsize: float,
    color: Tuple[float, float, float],
    align: int = fitz.TEXT_ALIGN_LEFT,
    lineheight: float = 1.25,
) -> float:
    """
    Inserta texto con word-wrap estricto dentro de `rect` y verifica que no exista recorte.
    Si el texto desborda la caja (`rc < 0`), lanza ValueError de inmediato para impedir cortes.
    """
    if rect.x0 < MARGIN_X0 - 0.5 or rect.x1 > MARGIN_X1 + 0.5:
        raise ValueError(f"Caja fuera de márgenes A4 permitidos ({MARGIN_X0}..{MARGIN_X1}): {rect}")

    clean_text = text.replace("\u00b7", "|")
    rc = page.insert_textbox(
        rect,
        clean_text,
        fontsize=fontsize,
        fontname=fontname,
        color=color,
        align=align,
        lineheight=lineheight,
    )
    if rc < 0:
        raise ValueError(
            f"Texto desbordado en PDF (rc={rc:.2f}) dentro de rect={rect} con fontsize={fontsize}: {clean_text[:90]}"
        )
    return rc


def draw_header_footer(page: fitz.Page, fonts: FontBundle, page_num: int, total_pages: int = 5, is_es: bool = True) -> None:
    """Inserta cabecera y pie homogéneos con cajas acotadas en todas las páginas interiores."""
    if page_num == 1:
        return

    top_title = "DATALARIA PULSE | CONTENT OPS AS CODE & NOTION MIGRATION KIT"
    top_badge = "MANUAL EJECUTIVO v1.0.0" if is_es else "EXECUTIVE MANUAL v1.0.0"

    draw_textbox(
        page,
        fitz.Rect(MARGIN_X0, 22, 415, 38),
        top_title,
        fontname=fonts.bold,
        fontsize=7.8,
        color=SLATE_500,
    )
    draw_textbox(
        page,
        fitz.Rect(420, 22, MARGIN_X1, 38),
        top_badge,
        fontname=fonts.bold,
        fontsize=7.8,
        color=EMERALD_DARK,
        align=fitz.TEXT_ALIGN_RIGHT,
    )
    page.draw_rect(fitz.Rect(MARGIN_X0, 41, MARGIN_X1, 42.5), color=EMERALD, fill=EMERALD)

    page.draw_rect(fitz.Rect(MARGIN_X0, 804, MARGIN_X1, 805), color=BORDER_LIGHT, fill=BORDER_LIGHT)
    footer_text = (
        "© 2026 Datalaria.com | Licencia Comercial Perpetua | Gobernanza SDD"
        if is_es
        else "© 2026 Datalaria.com | Perpetual Commercial License | SDD Governance"
    )
    page_text = f"Página {page_num} / {total_pages}" if is_es else f"Page {page_num} / {total_pages}"

    draw_textbox(
        page,
        fitz.Rect(MARGIN_X0, 811, 465, 828),
        footer_text,
        fontname=fonts.regular,
        fontsize=7.8,
        color=SLATE_500,
    )
    draw_textbox(
        page,
        fitz.Rect(470, 811, MARGIN_X1, 828),
        page_text,
        fontname=fonts.bold,
        fontsize=8.0,
        color=SLATE_700,
        align=fitz.TEXT_ALIGN_RIGHT,
    )


def draw_page_title(page: fitz.Page, fonts: FontBundle, title: str, subtitle: str) -> None:
    """Dibuja título de sección y subtítulo explicativo en páginas interiores."""
    draw_textbox(
        page,
        fitz.Rect(MARGIN_X0, 50, MARGIN_X1, 80),
        title,
        fontname=fonts.bold,
        fontsize=15.5,
        color=SLATE_900,
        lineheight=1.15,
    )
    draw_textbox(
        page,
        fitz.Rect(MARGIN_X0, 77, MARGIN_X1, 102),
        subtitle,
        fontname=fonts.regular,
        fontsize=9.3,
        color=SLATE_500,
        lineheight=1.2,
    )


def build_executive_pdf_guide(output_path: Optional[Path] = None, lang: str = "es") -> Path:
    """Genera el documento PDF A4 ejecutivo de 5 páginas en el idioma especificado ('es' o 'en')."""
    lang = lang.lower()
    is_es = lang == "es"

    if output_path is None:
        output_path = OUTPUT_PDF_ES if is_es else OUTPUT_PDF_EN

    doc = fitz.open()
    total_pages = 5

    # =========================================================================
    # PÁGINA 1: PORTADA EJECUTIVA, MAPA DEL KIT Y RUTAS RÁPIDAS
    # =========================================================================
    p1 = doc.new_page(width=PAGE_W, height=PAGE_H)
    f1 = register_page_fonts(p1)

    p1.draw_rect(fitz.Rect(0, 0, PAGE_W, PAGE_H), color=DARK_BG, fill=DARK_BG)
    p1.draw_rect(fitz.Rect(MARGIN_X0, 42, MARGIN_X1, 46), color=EMERALD, fill=EMERALD)

    tag_p1 = (
        "DATALARIA ENGINEERING  |  OPERATIONS & APPLIED AI  |  EDICIÓN COMERCIAL DUAL v1.0.0"
        if is_es
        else "DATALARIA ENGINEERING  |  OPERATIONS & APPLIED AI  |  DUAL COMMERCIAL EDITION v1.0.0"
    )
    title_p1 = "Datalaria Pulse"
    sub1_p1 = "Content Ops as Code & Notion Migration Kit"
    sub2_p1 = (
        "Manual Maestro de Implementación, Caso de Uso Paso a Paso y Retorno Orgánico (SEO + B2B)"
        if is_es
        else "Master Implementation Manual, Step-by-Step Use Cases & Organic Content ROI (SEO + B2B)"
    )

    draw_textbox(p1, fitz.Rect(MARGIN_X0, 58, MARGIN_X1, 76), tag_p1, fontname=f1.bold, fontsize=8.5, color=EMERALD)
    draw_textbox(p1, fitz.Rect(MARGIN_X0, 82, MARGIN_X1, 126), title_p1, fontname=f1.bold, fontsize=32, color=TEXT_LIGHT, lineheight=1.1)
    draw_textbox(p1, fitz.Rect(MARGIN_X0, 126, MARGIN_X1, 154), sub1_p1, fontname=f1.regular, fontsize=16.5, color=TEXT_MUTED_DARK)
    draw_textbox(p1, fitz.Rect(MARGIN_X0, 156, MARGIN_X1, 180), sub2_p1, fontname=f1.regular, fontsize=10.5, color=CYAN)

    # Caja 1: Arquitectura completa del paquete (Raíz + 2 Carpetas de Idioma)
    p1.draw_rect(fitz.Rect(MARGIN_X0, 194, MARGIN_X1, 448), color=DARK_CARD, fill=DARK_CARD)
    p1.draw_rect(fitz.Rect(MARGIN_X0, 194, MARGIN_X0 + 4, 448), color=EMERALD, fill=EMERALD)

    box1_title = (
        "ESTRUCTURA DEL ENTREGABLE BILINGÜE DUAL (RAÍZ + CARPETAS ES / EN):"
        if is_es
        else "DUAL BILINGUAL DELIVERABLE STRUCTURE (ROOT + ES / EN FOLDERS):"
    )
    draw_textbox(p1, fitz.Rect(56, 206, 540, 226), box1_title, fontname=f1.bold, fontsize=10.5, color=TEXT_LIGHT)

    if is_es:
        deliverable_rows = [
            ("Raíz del ZIP:", "00_EMPIEZA_AQUI_ES.md, 00_START_HERE_EN.md, LICENSE_ES.txt y LICENSE_EN.txt."),
            ("Carpeta ES/:", "Plantilla Excel automatizada (ES), 2 conectores Power Query M (ES), scripts CLI y Guía PDF."),
            ("Carpeta EN/:", "Master Excel Template (EN), 2 Power Query M connectors (EN), scripts CLI and English PDF Guide."),
            ("Automatización Excel:", "Cero doble escritura: Kanban dinámico sin macros, Métricas autocompletadas y Dashboard ejecutivo."),
            ("Licencia Comercial:", "Pago único perpetuo de 19 € con soberanía total, cero cuotas SaaS y privacidad INV-PULSE-1..8."),
        ]
    else:
        deliverable_rows = [
            ("ZIP Root:", "00_EMPIEZA_AQUI_ES.md, 00_START_HERE_EN.md, LICENSE_ES.txt and LICENSE_EN.txt."),
            ("ES/ Folder:", "Automated Excel template (ES), 2 Power Query connectors (ES), CLI scripts and Spanish PDF Guide."),
            ("EN/ Folder:", "Automated Master Excel (EN), 2 Power Query M connectors (EN), CLI scripts and English PDF Guide."),
            ("Excel Automation:", "Zero duplicate manual entry: dynamic live Kanban, auto-lookup Metrics and Executive Dashboard."),
            ("Commercial License:", "Perpetual single payment of 19 € with full data sovereignty, zero SaaS fees and INV-PULSE-1..8."),
        ]

    y_row = 234.0
    for label, desc in deliverable_rows:
        draw_textbox(p1, fitz.Rect(56, y_row, 196, y_row + 38), label, fontname=f1.bold, fontsize=9.2, color=EMERALD, lineheight=1.2)
        draw_textbox(p1, fitz.Rect(200, y_row, 542, y_row + 40), desc, fontname=f1.regular, fontsize=8.8, color=TEXT_MUTED_DARK, lineheight=1.22)
        y_row += 42.0

    # Cajas comparativas centrales (TCO + Compatibilidad)
    p1.draw_rect(fitz.Rect(MARGIN_X0, 466, 290, 616), color=DARK_CARD, fill=DARK_CARD)
    p1.draw_rect(fitz.Rect(305, 466, MARGIN_X1, 616), color=DARK_CARD, fill=DARK_CARD)

    tco_title = "COMPARATIVA TCO A 3 AÑOS" if is_es else "3-YEAR TCO BENCHMARK"
    tco_text = (
        "- Notion / Airtable SaaS: 1.800 € - 3.600 € recurrentes.\n"
        "- Datalaria Pulse Kit: 19 € pago único perpetuo.\n"
        "- Amortización directa desde el Día 1.\n"
        "- Soberanía total: datos en tu máquina y tu Git."
        if is_es
        else
        "- Notion / Airtable SaaS: 1,800 € - 3,600 € recurring.\n"
        "- Datalaria Pulse Kit: 19 € single perpetual payment.\n"
        "- Instant ROI payback from Day 1.\n"
        "- Full data sovereignty: files on your machine & Git."
    )
    draw_textbox(p1, fitz.Rect(54, 478, 278, 498), tco_title, fontname=f1.bold, fontsize=9.8, color=TEXT_LIGHT)
    draw_textbox(p1, fitz.Rect(54, 502, 278, 608), tco_text, fontname=f1.regular, fontsize=8.6, color=TEXT_MUTED_DARK, lineheight=1.35)

    comp_title = "COMPATIBILIDAD Y ESTÁNDARES" if is_es else "COMPATIBILITY & STANDARDS"
    comp_text = (
        "- Excel 2016, 2019, 2021, Office 365 y Google Sheets.\n"
        "- Hugo, Astro, Next.js, Docusaurus y Jekyll.\n"
        "- Python 3.8+ (0 dependencias externas en scanner).\n"
        "- Compatible con Windows, macOS y Linux CI/CD."
        if is_es
        else
        "- Excel 2016, 2019, 2021, Office 365 & Google Sheets.\n"
        "- Hugo, Astro, Next.js, Docusaurus & Jekyll.\n"
        "- Python 3.8+ (0 external dependencies in scanner).\n"
        "- Fully verified on Windows, macOS & Linux CI/CD."
    )
    draw_textbox(p1, fitz.Rect(319, 478, 542, 498), comp_title, fontname=f1.bold, fontsize=9.8, color=TEXT_LIGHT)
    draw_textbox(p1, fitz.Rect(319, 502, 542, 608), comp_text, fontname=f1.regular, fontsize=8.6, color=TEXT_MUTED_DARK, lineheight=1.35)

    # Caja inferior: Elige tu ruta en 60 segundos
    p1.draw_rect(fitz.Rect(MARGIN_X0, 634, MARGIN_X1, 766), color=DARK_CARD, fill=DARK_CARD)
    p1.draw_rect(fitz.Rect(MARGIN_X0, 634, MARGIN_X1, 637), color=CYAN, fill=CYAN)

    quick_title = "ELIGE TU RUTA DE ARRANQUE EN 60 SEGUNDOS:" if is_es else "CHOOSE YOUR STARTING TRACK IN 60 SECONDS:"
    quick_text = (
        "1. Ruta A (No-Code Excel): Abre la plantilla en tu idioma (ES/ o EN/) y revisa los 10 activos de muestra.\n"
        "2. Ruta B (Salir de Notion): Ejecuta notion_power_query_*.m en Excel o migrate_notion.py sobre sample_notion_export_*.csv.\n"
        "3. Ruta C (Repo Git/Markdown): Lanza pulse_repo_scanner.py (--lang es|en) sobre tu carpeta content/ para auditar SEO y paridad."
        if is_es
        else
        "1. Track A (No-Code Excel): Open the localized template in ES/ or EN/ and explore the 10 curated sample assets.\n"
        "2. Track B (Exit Notion): Run notion_power_query_*.m in Excel or execute migrate_notion.py on sample_notion_export_*.csv.\n"
        "3. Track C (Git/Markdown Repo): Run pulse_repo_scanner.py (--lang es|en) on your content/ folder to audit SEO and parity."
    )
    draw_textbox(p1, fitz.Rect(56, 646, 542, 666), quick_title, fontname=f1.bold, fontsize=9.8, color=CYAN)
    draw_textbox(p1, fitz.Rect(56, 668, 542, 756), quick_text, fontname=f1.regular, fontsize=8.7, color=TEXT_LIGHT, lineheight=1.36)

    footer_p1 = (
        "Datalaria Engineering  |  https://datalaria.com/es/apps/pulse/  |  Soporte: contacto@datalaria.com\n"
        "Desarrollado y verificado bajo el framework Spec-Driven Development (SDD) e Invariantes INV-PULSE-1..8"
        if is_es
        else
        "Datalaria Engineering  |  https://datalaria.com/en/apps/pulse/  |  Support: contacto@datalaria.com\n"
        "Engineered and verified under Spec-Driven Development (SDD) framework & Invariants INV-PULSE-1..8"
    )
    draw_textbox(p1, fitz.Rect(MARGIN_X0, 782, MARGIN_X1, 822), footer_p1, fontname=f1.regular, fontsize=8.3, color=TEXT_MUTED_DARK, lineheight=1.3)

    # =========================================================================
    # PÁGINA 2: RADIOGRAFÍA DE LAS 6 HOJAS DEL EXCEL + CONEXIÓN GA4/GSC
    # =========================================================================
    p2 = doc.new_page(width=PAGE_W, height=PAGE_H)
    f2 = register_page_fonts(p2)
    draw_header_footer(p2, f2, 2, total_pages, is_es=is_es)

    p2_title = "1. Radiografía del Master Tracker Excel (6 Hojas)" if is_es else "1. Anatomy of the Master Excel Tracker (6 Sheets)"
    p2_sub = (
        "Estructura profesional con tablas nativas, paneles congelados, color de pestañas y fórmulas sin macros VBA."
        if is_es
        else "Professional architecture with native Tables, freeze panes, colored tabs and zero-macro dynamic formulas."
    )
    draw_page_title(p2, f2, p2_title, p2_sub)

    if is_es:
        sheets_info = [
            ("Hoja 1: Instrucciones (Pestaña Azul)", "Resumen visual y Flujo de Trabajo en 3 Pasos. Explica cómo ingestar Notion/Git, aplicar el ritual semanal y consolidar KPIs.", 48.0),
            ("Hoja 2: Taxonomía (Pestaña Azul)", "Catálogo maestro que alimenta desplegables anti-error: Tipos (POST/APP/KIT), Estados (Idea..Published), Visibilidad, Paridad, Frescura, las 5 Categorías Canónicas y Tipo Release SemVer.", 60.0),
            ("Hoja 3: Activos (Pestaña Esmeralda)", "Tabla nativa estructurada (23 columnas) con filtros y ordenación. Consolida títulos ES/EN, fechas, paridad, tiempo de lectura calculado y visitas/usuarios leídos automáticamente desde Métricas.", 56.0),
            ("Hoja 4: Kanban Visual (Pestaña Esmeralda)", "Tablero 100% dinámico en 5 columnas con contadores en vivo. Mover el estado de un activo en 'Activos' actualiza al instante su columna sin macros VBA.", 50.0),
            ("Hoja 5: Métricas (Pestaña Esmeralda)", "Consolidación de GA4 y Search Console. Al seleccionar el ID del activo, su Tipo y Título se autocompletan inmediatamente para evitar transcripciones manuales.", 50.0),
            ("Hoja 6: Dashboard Ejecutivo (Pestaña Ámbar)", "Cuadro de mando C-Level en tiempo real: KPIs base, distribución por tipo de activo, salud por las 5 categorías canónicas y radar de accionables (fórmulas universales Excel/Sheets).", 52.0),
        ]
    else:
        sheets_info = [
            ("Sheet 1: Instructions (Blue Tab)", "Visual overview and Recommended 3-Step Workflow. Explains how to ingest from Notion/Git, execute weekly governance, and consolidate executive KPIs.", 48.0),
            ("Sheet 2: Taxonomy (Blue Tab)", "Master catalog powering error-free dropdowns: Asset Types (POST/APP/KIT), Statuses (Idea..Published), Visibility, Parity, Freshness, 5 Canonical Categories, and SemVer Releases.", 60.0),
            ("Sheet 3: Assets (Emerald Tab)", "Structured native Table (23 columns) with column filters and sorting. Features auto-calculated read time and dynamic views/users lookup from Metrics with zero duplication.", 56.0),
            ("Sheet 4: Live Dynamic Kanban (Emerald Tab)", "Real-time 5-column visual board with live header counters. Changing status in 'Assets' instantly updates cards here without VBA macros.", 50.0),
            ("Sheet 5: Metrics (Emerald Tab)", "Quantitative consolidation for GA4 and Search Console. Selecting the Asset ID automatically populates Asset Type and Title to eliminate manual data entry.", 50.0),
            ("Sheet 6: Executive Dashboard (Amber Tab)", "C-Level real-time scorecards: core KPIs, breakdown by asset type, category health across 5 pillars, and actionable alerts radar (universal Excel/Sheets formulas).", 52.0),
        ]

    y_cur = 106.0
    for s_title, s_desc, box_h in sheets_info:
        p2.draw_rect(fitz.Rect(MARGIN_X0, y_cur, MARGIN_X1, y_cur + box_h), color=CARD_LIGHT, fill=CARD_LIGHT)
        p2.draw_rect(fitz.Rect(MARGIN_X0, y_cur, MARGIN_X0 + 4, y_cur + box_h), color=EMERALD, fill=EMERALD)
        draw_textbox(p2, fitz.Rect(54, y_cur + 5, 542, y_cur + 21), s_title, fontname=f2.bold, fontsize=9.6, color=SLATE_900)
        draw_textbox(p2, fitz.Rect(54, y_cur + 20, 542, y_cur + box_h - 2), s_desc, fontname=f2.regular, fontsize=8.3, color=SLATE_700, lineheight=1.20)
        y_cur += box_h + 6.0

    # Bloque inferior Pagina 2: Conexión GA4 + GSC y Privacidad INV-PULSE-2
    ga_title = "2. Cómo Conectar Google Analytics 4 y Search Console sin Riesgos" if is_es else "2. How to Connect Google Analytics 4 & Search Console Safely"
    draw_textbox(p2, fitz.Rect(MARGIN_X0, 488, MARGIN_X1, 512), ga_title, fontname=f2.bold, fontsize=12.5, color=SLATE_900)
    p2.draw_rect(fitz.Rect(MARGIN_X0, 514, MARGIN_X1, 646), color=CARD_LIGHT, fill=CARD_LIGHT)

    ga_text = (
        "Paso 1 (Google Cloud): Crea un proyecto, habilita 'Google Analytics Data API' y 'Google Search Console API', genera una Cuenta de Servicio (ej. pulse-reporter) y descarga tu archivo local JSON de credenciales (nunca lo subas a Git).\n"
        "Paso 2 (Permisos de solo lectura): En GA4 (Administrar > Gestión de accesos) y en Search Console (Ajustes > Usuarios), añade el email de la Cuenta de Servicio con rol estrictamente de 'Lector'.\n"
        "Paso 3 (Actualización de Métricas): Vuelca el export mensual en la hoja 'Métricas' (o usa el script sync_metrics.py en tu entorno CI/CD privado) para alimentar los cruces de ROI editorial en Excel."
        if is_es
        else
        "Step 1 (Google Cloud): Create a project, enable 'Google Analytics Data API' and 'Search Console API', generate a Service Account (e.g. pulse-reporter), and download credentials JSON locally (never commit to Git).\n"
        "Step 2 (Read-Only Access): In GA4 (Admin > Access Management) and Search Console (Settings > Users), add the Service Account email with strict 'Viewer' role.\n"
        "Step 3 (Metrics Ingestion): Paste monthly numbers into 'Metrics' (or run sync_metrics.py in private CI/CD) to feed automated cross-sheet ROI calculations in Excel."
    )
    draw_textbox(p2, fitz.Rect(54, 522, 542, 640), ga_text, fontname=f2.regular, fontsize=8.6, color=SLATE_700, lineheight=1.32)

    p2.draw_rect(fitz.Rect(MARGIN_X0, 662, MARGIN_X1, 774), color=EMERALD_BG, fill=EMERALD_BG)
    p2.draw_rect(fitz.Rect(MARGIN_X0, 662, MARGIN_X0 + 4, 774), color=EMERALD_DARK, fill=EMERALD_DARK)
    inv_title = "INVARIANTE DE PRIVACIDAD POR DISEÑO (INV-PULSE-1 e INV-PULSE-2):" if is_es else "PRIVACY BY DESIGN INVARIANTS (INV-PULSE-1 & INV-PULSE-2):"
    inv_desc = (
        "Tu libro Excel privado local y tus credenciales permanecen 100% bajo tu control. Si publicas una Web App pública o compartes public.json, las métricas absolutas de facturación o visitas nunca se exponen: se transforman determinísticamente a Índice Base 100 sobre la mediana (index_100) y Percentil de tráfico (rank_pct), excluyendo cualquier fila con visibility='private'."
        if is_es
        else
        "Your private Excel workbook and cloud credentials stay 100% under your control. When publishing a web app or public.json, absolute revenue and traffic figures are never exposed: they are deterministically converted into Base-100 index (index_100) and traffic percentile (rank_pct), strictly excluding visibility='private' rows."
    )
    draw_textbox(p2, fitz.Rect(54, 672, 542, 692), inv_title, fontname=f2.bold, fontsize=9.8, color=EMERALD_DARK)
    draw_textbox(p2, fitz.Rect(54, 694, 542, 766), inv_desc, fontname=f2.regular, fontsize=8.7, color=SLATE_700, lineheight=1.3)

    # =========================================================================
    # PÁGINA 3: CONECTORES POWER QUERY M, SCRIPTS PYTHON Y DATASET DE 10 MUESTRAS
    # =========================================================================
    p3 = doc.new_page(width=PAGE_W, height=PAGE_H)
    f3 = register_page_fonts(p3)
    draw_header_footer(p3, f3, 3, total_pages, is_es=is_es)

    p3_title = "3. Conectores Power Query M y Scripts CLI Python" if is_es else "3. Power Query M Connectors and Python CLI Scripts"
    p3_sub = (
        "Cuatro mecanismos complementarios para migrar desde Notion o auditar repositorios Markdown sin fricción."
        if is_es
        else "Four complementary mechanisms to migrate from Notion or audit Markdown repositories with zero friction."
    )
    draw_page_title(p3, f3, p3_title, p3_sub)

    # Conector A: notion_power_query
    p3.draw_rect(fitz.Rect(MARGIN_X0, 114, MARGIN_X1, 248), color=CARD_LIGHT, fill=CARD_LIGHT)
    p3.draw_rect(fitz.Rect(MARGIN_X0, 114, MARGIN_X0 + 4, 248), color=EMERALD, fill=EMERALD)
    pq1_title = (
        "Vía 1 (Sin Código) | Conector Power Query para Notion (notion_power_query_*.m)"
        if is_es
        else "Method 1 (No-Code) | Notion Power Query Connector (notion_power_query_*.m)"
    )
    pq1_desc = (
        "1. En tu base de datos de Notion: menú '...' > Export > Formato Markdown & CSV > incluye subpáginas.\n"
        "2. En Excel: Datos > Obtener datos > De otras fuentes > Consulta en blanco > abre el 'Editor avanzado'.\n"
        "3. Pega el código de notion_power_query_*.m y sustituye la variable RutaArchivoCSV por tu ruta local.\n"
        "4. Pulsa 'Listo' y 'Cerrar y cargar': normaliza automáticamente títulos, estados canónicos (Idea..Published), fechas ISO y columnas exactas de la hoja 'Activos'."
        if is_es
        else
        "1. In your Notion database: menu '...' > Export > Markdown & CSV format > include subpages.\n"
        "2. In Excel: Data > Get Data > From Other Sources > Blank Query > open Advanced Editor.\n"
        "3. Paste the code of notion_power_query_*.m and replace RutaArchivoCSV with your local file path.\n"
        "4. Click 'Done' and 'Close & Load': automatically normalizes titles, canonical statuses (Idea..Published), ISO dates, and exact 'Assets' columns."
    )
    draw_textbox(p3, fitz.Rect(54, 122, 542, 142), pq1_title, fontname=f3.bold, fontsize=10.0, color=SLATE_900)
    draw_textbox(p3, fitz.Rect(54, 144, 542, 242), pq1_desc, fontname=f3.regular, fontsize=8.6, color=SLATE_700, lineheight=1.3)

    # Conector B: git_public_json_power_query
    p3.draw_rect(fitz.Rect(MARGIN_X0, 260, MARGIN_X1, 382), color=CARD_LIGHT, fill=CARD_LIGHT)
    p3.draw_rect(fitz.Rect(MARGIN_X0, 260, MARGIN_X0 + 4, 382), color=CYAN, fill=CYAN)
    pq2_title = (
        "Vía 2 (Sin Código) | Conector Power Query para Git public.json (git_public_json_power_query_*.m)"
        if is_es
        else "Method 2 (No-Code) | Git public.json Power Query Connector (git_public_json_power_query_*.m)"
    )
    pq2_desc = (
        "1. Abre 'Consulta en blanco' > 'Editor avanzado' y pega el código de git_public_json_power_query_*.m.\n"
        "2. Configura RutaPublicJson apuntando a tu archivo local static/apps/pulse/data/public.json.\n"
        "3. Pulsa 'Cerrar y cargar': expande cada ContentAsset, su Score SEO (0-100) y sus métricas relativas Base 100. Cada vez que hagas commit en Git, basta pulsar 'Datos > Actualizar todo'."
        if is_es
        else
        "1. Open 'Blank Query' > 'Advanced Editor' and paste the code from git_public_json_power_query_*.m.\n"
        "2. Set RutaPublicJson pointing to your local static/apps/pulse/data/public.json file.\n"
        "3. Click 'Close & Load': expands each ContentAsset, its SEO Score (0-100), and Base-100 relative metrics. Refresh anytime with 'Data > Refresh All'."
    )
    draw_textbox(p3, fitz.Rect(54, 268, 542, 288), pq2_title, fontname=f3.bold, fontsize=10.0, color=SLATE_900)
    draw_textbox(p3, fitz.Rect(54, 290, 542, 376), pq2_desc, fontname=f3.regular, fontsize=8.6, color=SLATE_700, lineheight=1.3)

    # Caja CLI oscura: migrate_notion.py & pulse_repo_scanner.py
    p3.draw_rect(fitz.Rect(MARGIN_X0, 396, MARGIN_X1, 610), color=DARK_BG, fill=DARK_BG)
    p3.draw_rect(fitz.Rect(MARGIN_X0, 396, MARGIN_X1, 400), color=EMERALD, fill=EMERALD)
    cli_title = (
        "Vías 3 y 4 (Línea de Comandos) | Conversor migrate_notion.py y Escáner pulse_repo_scanner.py"
        if is_es
        else "Methods 3 & 4 (Command Line) | Converter migrate_notion.py and Scanner pulse_repo_scanner.py"
    )
    cli_desc = (
        "Convierte cualquier exportación CSV de Notion en un libro Excel completo de 6 hojas (.xlsx) o en un backlog YAML/JSON listo para Git, o audita cualquier carpeta Markdown (Hugo, Astro, Jekyll, Next.js) sin instalar paquetes con pip:"
        if is_es
        else "Convert any Notion CSV export into a 6-sheet Excel workbook (.xlsx) or a Git-versioned YAML/JSON backlog, or audit any Markdown repository (Hugo, Astro, Jekyll, Next.js) with zero pip dependencies:"
    )
    draw_textbox(p3, fitz.Rect(54, 410, 542, 430), cli_title, fontname=f3.bold, fontsize=10.2, color=TEXT_LIGHT)
    draw_textbox(p3, fitz.Rect(54, 434, 542, 464), cli_desc, fontname=f3.regular, fontsize=8.5, color=TEXT_MUTED_DARK, lineheight=1.25)

    cmd_a = (
        "# A) Convertir CSV de Notion a libro Excel profesional (soporta --lang es|en):\n"
        f"python 02_Migration_Scripts/migrate_notion.py -i 02_Migration_Scripts/sample_notion_export_{lang}.csv -o Tracker.xlsx -f xlsx --lang {lang}"
    )
    cmd_b = (
        "# B) Exportar a YAML estructurado para usar como backlog versionado en Git:\n"
        f"python 02_Migration_Scripts/migrate_notion.py -i 02_Migration_Scripts/sample_notion_export_{lang}.csv -o backlog.yaml -f yaml"
    )
    cmd_c = (
        "# C) Escanear repositorio Markdown real (0 dependencias externas, devuelve CSV listo para pegar):\n"
        f"python 02_Migration_Scripts/pulse_repo_scanner.py --content-dir ./content --output auditoria_git.csv --lang {lang}"
    )
    draw_textbox(p3, fitz.Rect(54, 472, 542, 504), cmd_a, fontname=f3.mono, fontsize=7.6, color=EMERALD, lineheight=1.28)
    draw_textbox(p3, fitz.Rect(54, 514, 542, 546), cmd_b, fontname=f3.mono, fontsize=7.6, color=CYAN, lineheight=1.28)
    draw_textbox(p3, fitz.Rect(54, 556, 542, 594), cmd_c, fontname=f3.mono, fontsize=7.6, color=AMBER, lineheight=1.28)

    # Caja dataset de 10 muestras
    p3.draw_rect(fitz.Rect(MARGIN_X0, 626, MARGIN_X1, 774), color=AMBER_BG, fill=AMBER_BG)
    p3.draw_rect(fitz.Rect(MARGIN_X0, 626, MARGIN_X0 + 4, 774), color=AMBER, fill=AMBER)
    sample_title = (
        "DATASET DE MUESTRA INCLUIDO: EXACTAMENTE 10 ACTIVOS REPRESENTATIVOS"
        if is_es
        else "INCLUDED SAMPLE DATASET: EXACTLY 10 REPRESENTATIVE ASSETS"
    )
    sample_desc = (
        "Tanto la plantilla Excel como sample_notion_export_*.csv han sido curados con 10 activos representativos (8 artículos post, 1 Web App y 1 Kit B2B) en lugar de un volcado masivo difícil de leer.\n"
        "- Cubre las 5 categorías canónicas: IA/Ingeniería, Estrategia y Operaciones, Startups, Pioneros y Cultura Tech.\n"
        "- Cubre los 5 estados del flujo editorial: Published, Scheduled, Review, Draft e Idea.\n"
        "- Incluye anomalías reales intencionadas (paridad outdated_en, Quick Win SEO pos 9,4 y huérfano sin Kit) para que ejecutes el Caso de Uso de la página siguiente."
        if is_es
        else
        "Both the Master Excel Template and sample_notion_export_*.csv include 10 curated representative assets (8 posts, 1 Web App, 1 B2B Kit) rather than an unreadable bulk dump.\n"
        "- Covers all 5 canonical categories: AI/Engineering, Strategy & Operations, Startups, Pioneers, Tech Culture.\n"
        "- Covers all 5 lifecycle statuses: Published, Scheduled, Review, Draft, and Idea.\n"
        "- Includes real intentional anomalies (outdated_en parity, SEO Quick Win at pos 9.4, and orphan without kit) for hands-on practice in the following Use Case."
    )
    draw_textbox(p3, fitz.Rect(54, 636, 542, 656), sample_title, fontname=f3.bold, fontsize=10.0, color=SLATE_900)
    draw_textbox(p3, fitz.Rect(54, 658, 542, 766), sample_desc, fontname=f3.regular, fontsize=8.6, color=SLATE_700, lineheight=1.3)

    # =========================================================================
    # PÁGINA 4: CASO DE USO PRÁCTICO COMPLETO (EL MÉTODO DATALARIA SCRIBA)
    # =========================================================================
    p4 = doc.new_page(width=PAGE_W, height=PAGE_H)
    f4 = register_page_fonts(p4)
    draw_header_footer(p4, f4, 4, total_pages, is_es=is_es)

    p4_title = "4. Caso de Uso Práctico: El Ritual Editorial Datalaria Scriba" if is_es else "4. Practical Use Case: The Datalaria Scriba Editorial Ritual"
    p4_sub = (
        "Cómo auditar los 10 activos de muestra paso a paso para duplicar tu retorno orgánico sin redactar desde cero."
        if is_es
        else "Step-by-step audit of the 10 sample assets to maximize organic traffic and conversions without rewriting from scratch."
    )
    draw_page_title(p4, f4, p4_title, p4_sub)

    # Escenario 1: Paridad Bilingue
    p4.draw_rect(fitz.Rect(MARGIN_X0, 114, MARGIN_X1, 250), color=CARD_LIGHT, fill=CARD_LIGHT)
    p4.draw_rect(fitz.Rect(MARGIN_X0, 114, MARGIN_X0 + 4, 250), color=CYAN, fill=CYAN)
    sc1_title = (
        "Escenario 1 | Auditoría de Paridad Bilingüe (ES <-> EN) en la hoja 'Activos'"
        if is_es
        else "Scenario 1 | Bilingual Parity Audit (ES <-> EN) in the 'Assets' Sheet"
    )
    sc1_desc = (
        "1. Abre la hoja 'Activos' y aplica un filtro en la columna J ('Paridad') desmarcando 'complete'.\n"
        "2. Detecta la alerta 'outdated_en': El activo 'framework-porter-estrategia-c-level' muestra última modificación ES en 2026-11-10 y EN en 2026-09-15 (desfase > 7 días). Acción: actualizar la traducción EN para no perder tráfico internacional.\n"
        "3. Detecta la alerta 'missing_en': El borrador 'agentes-ia-automatizacion-sops' (v0.4.0) está en Draft sin versión EN. Bloquea su paso a Scheduled hasta completar la paridad bilingüe."
        if is_es
        else
        "1. Open 'Assets' and apply a column filter on J ('Parity'), unchecking 'complete'.\n"
        "2. Spot the 'outdated_en' alert: 'framework-porter-estrategia-c-level' shows last modified ES on 2026-11-10 and EN on 2026-09-15 (lag > 7 days). Action: update English translation to retain international readership.\n"
        "3. Spot the 'missing_en' alert: 'agentes-ia-automatizacion-sops' (v0.4.0) is in Draft with missing EN. Block progression to Scheduled until parity is completed."
    )
    draw_textbox(p4, fitz.Rect(54, 122, 542, 142), sc1_title, fontname=f4.bold, fontsize=10.2, color=SLATE_900)
    draw_textbox(p4, fitz.Rect(54, 144, 542, 242), sc1_desc, fontname=f4.regular, fontsize=8.6, color=SLATE_700, lineheight=1.3)

    # Escenario 2: Quick Wins SEO
    p4.draw_rect(fitz.Rect(MARGIN_X0, 264, MARGIN_X1, 514), color=CARD_LIGHT, fill=CARD_LIGHT)
    p4.draw_rect(fitz.Rect(MARGIN_X0, 264, MARGIN_X0 + 4, 514), color=EMERALD, fill=EMERALD)
    sc2_title = (
        "Escenario 2 | Caza de Quick Wins SEO con las 5 Reglas de 20 Puntos (Score 0-100)"
        if is_es
        else "Scenario 2 | SEO Quick Wins Hunting with 5 Rules of 20 Points (Score 0-100)"
    )
    sc2_desc = (
        "1. Filtra los activos con Estado='Published' y 'Score SEO' < 80, y crúzalos con la hoja 'Métricas'.\n"
        "2. Observa el activo de muestra 'matriz-riesgos-amfe-fmea': tiene 6.200 impresiones mensuales en Google, posición media 9,4 (final de Página 1 en Google), pero un CTR bajo de 1,90 % y Score SEO = 65.\n"
        "3. Qué significa y qué corregir hoy: Con solo optimizar su meta-descripción y título más atractivo para subir el CTR del 1,9 % al 4,5 %, capturas +160 clics mensuales inmediatos sin escribir un artículo nuevo."
        if is_es
        else
        "1. Filter assets with Status='Published' and 'SEO Score' < 80, cross-referencing with 'Metrics'.\n"
        "2. Inspect sample asset 'matriz-riesgos-amfe-fmea': it has 6,200 monthly Google impressions, average position 9.4 (bottom of Page 1), but a low CTR of 1.90 % and SEO Score = 65.\n"
        "3. Actionable fix: optimizing title and meta-description raises CTR from 1.9 % to 4.5 %, capturing +160 immediate monthly clicks without drafting a new article."
    )
    draw_textbox(p4, fitz.Rect(54, 272, 542, 292), sc2_title, fontname=f4.bold, fontsize=10.2, color=SLATE_900)
    draw_textbox(p4, fitz.Rect(54, 294, 542, 390), sc2_desc, fontname=f4.regular, fontsize=8.6, color=SLATE_700, lineheight=1.28)

    p4.draw_rect(fitz.Rect(54, 396, 542, 504), color=(1.0, 1.0, 1.0), fill=(1.0, 1.0, 1.0))
    rules_title = (
        "DESGLOSE DETERMINISTA DEL SCORE SEO (5 CHECKS x 20 PUNTOS = 100):"
        if is_es
        else "DETERMINISTIC SEO SCORE BREAKDOWN (5 CHECKS x 20 POINTS = 100):"
    )
    rules_desc = (
        "- title_ok (+20 pts): Longitud del título entre 30 y 80 caracteres (óptimo para evitar recortes en SERPs).\n"
        "- description_ok (+20 pts): Resumen o meta-descripción presente entre 70 y 220 caracteres.\n"
        "- parity_ok (+20 pts): Estado de paridad lingüística igual a 'complete' (ES y EN sincronizados).\n"
        "- taxonomy_ok (+20 pts): Al menos 1 categoría canónica válida y >= 2 etiquetas (tags) asignadas.\n"
        "- internal_links_ok (+20 pts): Al menos 1 enlace interno a otro post/app o imagen/shortcode en el cuerpo."
        if is_es
        else
        "- title_ok (+20 pts): Title length between 30 and 80 characters (prevents SERP truncations).\n"
        "- description_ok (+20 pts): Summary or meta-description present between 70 and 220 characters.\n"
        "- parity_ok (+20 pts): Language parity status equals 'complete' (ES and EN synchronized).\n"
        "- taxonomy_ok (+20 pts): At least 1 canonical category and >= 2 tags assigned.\n"
        "- internal_links_ok (+20 pts): At least 1 internal link to another post/app or image/shortcode in body."
    )
    draw_textbox(p4, fitz.Rect(64, 402, 532, 418), rules_title, fontname=f4.bold, fontsize=8.5, color=EMERALD_DARK)
    draw_textbox(p4, fitz.Rect(64, 420, 532, 498), rules_desc, fontname=f4.regular, fontsize=8.1, color=SLATE_700, lineheight=1.26)

    # Escenario 3: Huerfanos de Monetizacion y Gobernanza SemVer
    p4.draw_rect(fitz.Rect(MARGIN_X0, 528, MARGIN_X1, 774), color=CARD_LIGHT, fill=CARD_LIGHT)
    p4.draw_rect(fitz.Rect(MARGIN_X0, 528, MARGIN_X0 + 4, 774), color=VIOLET, fill=VIOLET)
    sc3_title = (
        "Escenario 3 | Huérfanos de Monetización y Gobernanza SemVer (v1.0.0 / v0.9.0 / v0.4.0)"
        if is_es
        else "Scenario 3 | Monetization Orphans & SemVer Release Governance (v1.0.0 / v0.9.0 / v0.4.0)"
    )
    sc3_desc = (
        "1. Detección de Huérfanos de Monetización: Ordena la hoja 'Activos' por la columna T ('Visitas 30d') de mayor a menor. Verás que 'ada-lovelace-pioneros-computacion' es el post más visitado (2.450 visitas/mes y 690 clics), pero sus columnas 'App Asociada' y 'Kit Asociado' están VACÍAS. Todo artículo tractor sin llamada a la acción comercial pierde leads recurrentes.\n"
        "2. Control de Releases SemVer (Columnas V y W): Filtra por 'Tipo' = APP o KIT y revisa 'Versión' y 'Tipo Release'. Los activos consolidados marcan v1.0.0 (major/minor), el artículo en revisión marca v0.9.0 (minor) y los borradores/ideas tempranas v0.4.0 (minor/patch).\n"
        "3. Regla Cero Silent Releases (INV-PULSE-8): Ninguna release v1.0.0 de una App o Kit debe quedarse sin su artículo técnico vinculado. En el ejemplo, tanto 'datalaria-pulse-web-app' como 'pack-pulse-content-ops-kit' enlazan al post de lanzamiento 'pulse-adios-notion-content-ops'."
        if is_es
        else
        "1. Detecting Monetization Orphans: Sort 'Assets' by column T ('Views 30d') descending. You will see that 'ada-lovelace-pioneros-computacion' is the most visited post (2,450 views/month and 690 clicks), but its 'Related App' and 'Related Kit' columns are EMPTY. Any tractor article lacking a conversion CTA leaks high-intent leads.\n"
        "2. SemVer Release Tracking (Columns V and W): Filter by 'Type' = APP or KIT. Consolidated products mark v1.0.0 (major/minor), in-review assets mark v0.9.0 (minor), and early drafts mark v0.4.0 (minor/patch).\n"
        "3. Zero Silent Releases Rule (INV-PULSE-8): No v1.0.0 release of an App or Kit may ship without a linked technical article. In the sample, both 'pulse' app and 'pack-pulse' kit link to launch post 'pulse-adios-notion-content-ops'."
    )
    draw_textbox(p4, fitz.Rect(54, 536, 542, 556), sc3_title, fontname=f4.bold, fontsize=10.2, color=SLATE_900)
    draw_textbox(p4, fitz.Rect(54, 558, 542, 766), sc3_desc, fontname=f4.regular, fontsize=8.6, color=SLATE_700, lineheight=1.32)

    # =========================================================================
    # PÁGINA 5: ESQUEMA TÉCNICO CONTENTASSET, CATEGORÍAS, INVARIANTES Y SOPORTE
    # =========================================================================
    p5 = doc.new_page(width=PAGE_W, height=PAGE_H)
    f5 = register_page_fonts(p5)
    draw_header_footer(p5, f5, 5, total_pages, is_es=is_es)

    p5_title = "5. Esquema ContentAsset, Taxonomía e Invariantes INV-PULSE-1..8" if is_es else "5. ContentAsset Schema, Taxonomy and Invariants INV-PULSE-1..8"
    p5_sub = (
        "Referencia técnica definitiva para integrar Datalaria Pulse con tus pipelines Git, CI/CD y comités."
        if is_es
        else "Definitive technical reference to integrate Datalaria Pulse with Git pipelines, CI/CD, and executive committees."
    )
    draw_page_title(p5, f5, p5_title, p5_sub)

    # Bloque 1: Esquema resumido ContentAsset
    p5.draw_rect(fitz.Rect(MARGIN_X0, 112, MARGIN_X1, 304), color=CARD_LIGHT, fill=CARD_LIGHT)
    sch_title = (
        "A) ATRIBUTOS CANÓNICOS PRINCIPALES DEL MODELO ContentAsset (Pydantic v2 / Excel):"
        if is_es
        else "A) CORE CANONICAL ATTRIBUTES OF THE ContentAsset MODEL (Pydantic v2 / Excel):"
    )
    draw_textbox(p5, fitz.Rect(54, 120, 542, 138), sch_title, fontname=f5.bold, fontsize=9.6, color=SLATE_900)

    sch_left = (
        "- id (str): Identificador kebab-case inmutable.\n"
        "- asset_type: POST | APP | KIT.\n"
        "- status: idea | draft | review | scheduled | published.\n"
        "- visibility: public | private (nunca en public.json).\n"
        "- language_parity: complete | missing_es/en | outdated_*.\n"
        "- category / tags / series: Clasificación editorial.\n"
        "- word_count_es/en y reading_time_min: Conteo neto."
        if is_es
        else
        "- id (str): Immutable kebab-case identifier.\n"
        "- asset_type: POST | APP | KIT.\n"
        "- status: idea | draft | review | scheduled | published.\n"
        "- visibility: public | private (never in public.json).\n"
        "- language_parity: complete | missing_es/en | outdated_*.\n"
        "- category / tags / series: Editorial classification.\n"
        "- word_count_es/en and reading_time_min: Net counts."
    )
    sch_right = (
        "- seo_audit.score_0_100: Score determinista 0 a 100.\n"
        "- freshness_status: fresh | review_needed | stale.\n"
        "- related_app / related_kit / price: Conversión PLG.\n"
        "- version (v1.0.0) y release_type (major/minor/patch).\n"
        "- parent_asset_id y editorial_post_slug: Trazabilidad.\n"
        "- metrics_relative: index_100, rank_pct, trend_30d_pct.\n"
        "- metrics_absolute: Solo uso privado local/Excel."
        if is_es
        else
        "- seo_audit.score_0_100: Deterministic score 0 to 100.\n"
        "- freshness_status: fresh | review_needed | stale.\n"
        "- related_app / related_kit / price: PLG conversion.\n"
        "- version (v1.0.0) and release_type (major/minor/patch).\n"
        "- parent_asset_id and editorial_post_slug: Audit trail.\n"
        "- metrics_relative: index_100, rank_pct, trend_30d_pct.\n"
        "- metrics_absolute: Private local/Excel use only."
    )
    draw_textbox(p5, fitz.Rect(54, 140, 292, 298), sch_left, fontname=f5.regular, fontsize=8.2, color=SLATE_700, lineheight=1.34)
    draw_textbox(p5, fitz.Rect(300, 140, 542, 298), sch_right, fontname=f5.regular, fontsize=8.2, color=SLATE_700, lineheight=1.34)

    # Bloque 2: Las 5 Categorias Canonicas
    p5.draw_rect(fitz.Rect(MARGIN_X0, 316, MARGIN_X1, 412), color=CYAN_BG, fill=CYAN_BG)
    p5.draw_rect(fitz.Rect(MARGIN_X0, 316, MARGIN_X0 + 4, 412), color=CYAN, fill=CYAN)
    cat_title = (
        "B) LAS 5 CATEGORÍAS CANÓNICAS DE DATALARIA (TAXONOMÍA OFICIAL):"
        if is_es
        else "B) THE 5 CANONICAL CATEGORIES OF DATALARIA (OFFICIAL TAXONOMY):"
    )
    cat_desc = (
        "1. IA, Ingeniería y Proyectos (agentes, software, arquitectura SDD)  |  2. Estrategia y Operaciones (modelos cuantitativos, Porter, AMFE, PMBOK)  |  3. Startups (unit economics, PLG, escalado)  |  4. Pioneros y Referentes (biografías técnicas fundacionales)  |  5. Cultura Tech y Media (ensayos, análisis sectorial y productividad)."
        if is_es
        else
        "1. AI, Engineering & Projects (agents, software, SDD architecture)  |  2. Strategy & Operations (quantitative models, Porter, FMEA, PMBOK)  |  3. Startups (unit economics, PLG, scaling)  |  4. Pioneers & Mentors (foundational technical biographies)  |  5. Tech Culture & Media (essays, industry analysis & productivity)."
    )
    draw_textbox(p5, fitz.Rect(54, 324, 542, 342), cat_title, fontname=f5.bold, fontsize=9.6, color=SLATE_900)
    draw_textbox(p5, fitz.Rect(54, 344, 542, 406), cat_desc, fontname=f5.regular, fontsize=8.4, color=SLATE_700, lineheight=1.32)

    # Bloque 3: Las 8 Invariantes INV-PULSE-1..8
    p5.draw_rect(fitz.Rect(MARGIN_X0, 424, MARGIN_X1, 634), color=CARD_LIGHT, fill=CARD_LIGHT)
    p5.draw_rect(fitz.Rect(MARGIN_X0, 424, MARGIN_X0 + 4, 634), color=EMERALD, fill=EMERALD)
    invs_title = (
        "C) LAS 8 INVARIANTES DE GOBERNANZA EDITORIAL (INV-PULSE-1 a INV-PULSE-8):"
        if is_es
        else "C) THE 8 EDITORIAL GOVERNANCE INVARIANTS (INV-PULSE-1 to INV-PULSE-8):"
    )
    invs_desc = (
        "- INV-PULSE-1 (Aislamiento de Privacidad): Los registros visibility='private' jamás se exportan a public.json.\n"
        "- INV-PULSE-2 (Relativización Base 100): public.json solo publica index_100 y rank_pct; nunca visitas ni ingresos brutos.\n"
        "- INV-PULSE-3 (Paridad Bilingüe Determinista): Alerta automática si falta ES/EN o si un idioma supera 7 días de desfase.\n"
        "- INV-PULSE-4 (Inmutabilidad de IDs): El identificador kebab-case es estable y sirve de clave de enlace entre idiomas.\n"
        "- INV-PULSE-5 (Compatibilidad Excel Universal): Fórmulas estándar (COUNTA, COUNTIF, SUM) compatibles con Excel 2016+ y Sheets.\n"
        "- INV-PULSE-6 (ROI Editorial Cuantitativo): Cruce determinista entre Score SEO, tráfico relativo y monetización activa.\n"
        "- INV-PULSE-7 (Aislamiento sin Dependencias): Escaneo CLI en Python puro aplicable en cualquier máquina o CI/CD.\n"
        "- INV-PULSE-8 (Sincronización Release-Editorial): Toda nueva versión major/minor se vincula con su post editorial."
        if is_es
        else
        "- INV-PULSE-1 (Privacy Isolation): visibility='private' records are never exported to public.json.\n"
        "- INV-PULSE-2 (Base-100 Relative Index): public.json only exposes index_100 and rank_pct; never raw visits or revenue.\n"
        "- INV-PULSE-3 (Deterministic Bilingual Parity): Automatic alert if ES/EN is missing or if either language exceeds 7-day drift.\n"
        "- INV-PULSE-4 (ID Immutability): Stable kebab-case slug serves as the universal key linking language editions.\n"
        "- INV-PULSE-5 (Universal Excel Compatibility): Standard formulas (COUNTA, COUNTIF, SUM) compatible with Excel 2016+ & Sheets.\n"
        "- INV-PULSE-6 (Quantitative Editorial ROI): Deterministic cross-analysis between SEO Score, relative traffic, and active CTAs.\n"
        "- INV-PULSE-7 (Zero-Dependency Isolation): Pure Python CLI scanner executable on any environment or CI/CD pipeline.\n"
        "- INV-PULSE-8 (Release-Editorial Synchronization): Every major/minor app release must link to a published editorial post."
    )
    draw_textbox(p5, fitz.Rect(54, 432, 542, 450), invs_title, fontname=f5.bold, fontsize=9.6, color=SLATE_900)
    draw_textbox(p5, fitz.Rect(54, 452, 542, 626), invs_desc, fontname=f5.regular, fontsize=8.3, color=SLATE_700, lineheight=1.34)

    # Bloque 4: Siguiente nivel Helix y Soporte Oficial
    p5.draw_rect(fitz.Rect(MARGIN_X0, 648, MARGIN_X1, 782), color=DARK_BG, fill=DARK_BG)
    p5.draw_rect(fitz.Rect(MARGIN_X0, 648, MARGIN_X1, 651), color=VIOLET, fill=VIOLET)
    sup_title = (
        "SOPORTE OFICIAL, CONSULTORÍA B2B Y EVOLUCIÓN HACIA DATALARIA HELIX"
        if is_es
        else "OFFICIAL SUPPORT, B2B CONSULTING & UPGRADE TO DATALARIA HELIX"
    )
    sup_desc = (
        "Datalaria Pulse es la base operativa del sistema de 12 agentes de ingeniería (Helix) y 8 agentes editoriales (Scriba).\n"
        "Si necesitas automatizar flujos con PostgreSQL/Supabase, webhooks CI/CD o auditorías editoriales a medida:\n"
        "- Web y App Sandbox: https://datalaria.com/es/apps/pulse/\n"
        "- Catálogo de Kits y Recursos B2B: https://datalaria.com/es/recursos/#pack-pulse\n"
        "- Email Directo de Ingeniería y Soporte: contacto@datalaria.com"
        if is_es
        else
        "Datalaria Pulse is the operational foundation of the 12-agent engineering squad (Helix) and 8-agent editorial squad (Scriba).\n"
        "If you need to automate workflows with PostgreSQL/Supabase, CI/CD webhooks, or custom editorial audits:\n"
        "- Web & App Sandbox: https://datalaria.com/en/apps/pulse/\n"
        "- B2B Kits & Resources Catalog: https://datalaria.com/en/resources/#pack-pulse\n"
        "- Direct Engineering & Support Email: contacto@datalaria.com"
    )
    draw_textbox(p5, fitz.Rect(54, 660, 542, 680), sup_title, fontname=f5.bold, fontsize=9.8, color=TEXT_LIGHT)
    draw_textbox(p5, fitz.Rect(54, 682, 542, 774), sup_desc, fontname=f5.regular, fontsize=8.6, color=TEXT_MUTED_DARK, lineheight=1.34)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.subset_fonts()
    doc.save(str(output_path), garbage=4, deflate=True)
    doc.close()

    # Si es español y el destino no es el legacy, sincronizar copia legacy
    if is_es and output_path != OUTPUT_PDF_LEGACY:
        shutil.copy2(output_path, OUTPUT_PDF_LEGACY)

    print(f"[PDF GUIDE] Generado exitosamente ({lang.upper()}): {output_path.resolve()} ({output_path.stat().st_size // 1024} KB)")
    return output_path


def build_pulse_pdf_guide(output_path: Optional[Path] = None, lang: str = "es") -> Path:
    """Función de compatibilidad con código existente."""
    return build_executive_pdf_guide(output_path=output_path, lang=lang)


if __name__ == "__main__":
    # Generar ambas guías ejecutivas
    build_executive_pdf_guide(lang="es")
    build_executive_pdf_guide(lang="en")
