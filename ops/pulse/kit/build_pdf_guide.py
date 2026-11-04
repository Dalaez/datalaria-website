"""
ops/pulse/kit/build_pdf_guide.py
--------------------------------
Generador programático de la Guía Ejecutiva de Datalaria Pulse en formato PDF A4
utilizando PyMuPDF (fitz).

Especificación: Hito 6.3 (specs/apps/pulse/spec.md).
Produce: packages/pulse/GUIA_EJECUTIVA_PULSE.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path
import fitz  # PyMuPDF

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
OUTPUT_PDF = ROOT_DIR / "packages" / "pulse" / "GUIA_EJECUTIVA_PULSE.pdf"


def draw_header_footer(page: fitz.Page, page_num: int, total_pages: int = 4) -> None:
    """Inserta cabecera y pie ejecutivos en páginas de contenido."""
    if page_num == 1:
        return  # Portada limpia

    # Línea y título cabecera
    page.draw_rect(fitz.Rect(50, 40, 545, 41), color=(0.06, 0.72, 0.51), fill=(0.06, 0.72, 0.51))
    page.insert_text(
        fitz.Point(50, 35),
        "DATALARIA PULSE — CONTENT OPS AS CODE & NOTION MIGRATION KIT",
        fontsize=8,
        fontname="helv",
        color=(0.58, 0.64, 0.72),
    )
    page.insert_text(
        fitz.Point(450, 35),
        "MANUAL EJECUTIVO v1.1",
        fontsize=8,
        fontname="helv",
        color=(0.06, 0.72, 0.51),
    )

    # Pie de página
    page.draw_rect(fitz.Rect(50, 805, 545, 806), color=(0.88, 0.91, 0.94), fill=(0.88, 0.91, 0.94))
    page.insert_text(
        fitz.Point(50, 818),
        "© 2026 Datalaria.com — Propiedad y Gobernanza Editorial bajo SDD",
        fontsize=8,
        fontname="helv",
        color=(0.58, 0.64, 0.72),
    )
    page.insert_text(
        fitz.Point(510, 818),
        f"{page_num} / {total_pages}",
        fontsize=8,
        fontname="helv",
        color=(0.2, 0.25, 0.33),
    )


def build_pulse_pdf_guide(output_path: Path = OUTPUT_PDF) -> Path:
    """Genera el documento PDF A4 ejecutivo de 4 páginas."""
    doc = fitz.open()

    # =========================================================================
    # PÁGINA 1: PORTADA EJECUTIVA OSCURA (DARK COCKPIT)
    # =========================================================================
    p1 = doc.new_page(width=595, height=842)
    # Fondo #0b0f17
    p1.draw_rect(fitz.Rect(0, 0, 595, 842), color=(0.043, 0.059, 0.09), fill=(0.043, 0.059, 0.09))

    # Acento superior verde esmeralda (#10b981)
    p1.draw_rect(fitz.Rect(50, 60, 545, 64), color=(0.063, 0.725, 0.506), fill=(0.063, 0.725, 0.506))

    p1.insert_text(
        fitz.Point(50, 110),
        "DATALARIA ENGINEERING · OPERATIONS & APPLIED AI",
        fontsize=10,
        fontname="helv",
        color=(0.063, 0.725, 0.506),
    )

    p1.insert_text(
        fitz.Point(50, 155),
        "Datalaria Pulse",
        fontsize=34,
        fontname="helv",
        color=(0.976, 0.98, 0.984),
    )

    p1.insert_text(
        fitz.Point(50, 190),
        "Content Ops as Code & Notion Migration Kit",
        fontsize=18,
        fontname="helv",
        color=(0.612, 0.639, 0.686),
    )

    p1.insert_text(
        fitz.Point(50, 220),
        "Manual Maestro de Implementación, Gobernanza y Retorno Orgánico",
        fontsize=12,
        fontname="helv",
        color=(0.024, 0.714, 0.831),
    )

    # Caja de resumen de valor (Dark Elevated)
    p1.draw_rect(
        fitz.Rect(50, 260, 545, 430),
        color=(0.067, 0.094, 0.153),
        fill=(0.067, 0.094, 0.153),
    )
    p1.draw_rect(
        fitz.Rect(50, 260, 54, 430),
        color=(0.063, 0.725, 0.506),
        fill=(0.063, 0.725, 0.506),
    )

    p1.insert_text(
        fitz.Point(70, 290),
        "ARQUITECTURA DEL ENTREGABLE B2B (EDICIÓN COMERCIAL v1.1):",
        fontsize=11,
        fontname="helv",
        color=(0.976, 0.98, 0.984),
    )

    bullet_y = 320
    bullets = [
        ("📁 01_Excel_Templates:", "Pulse_Content_Ops_Template.xlsx (6 hojas) + Conectores Power Query M duales."),
        ("📁 02_Migration_Scripts:", "migrate_notion.py (exportador .xlsx/.yaml), pulse_repo_scanner.py y dataset de muestra."),
        ("📁 03_Documentation:", "GUIA_EJECUTIVA_PULSE.pdf, manual GUIA_PULSE_KIT.md y ESPECIFICACION_CAMPOS.md."),
        ("🔒 Modelo Dual-Mode:", "Licencia comercial perpetua 19€ sin suscripciones mensuales recurrentes."),
        ("🌐 Paridad y Privacidad:", "Gobernanza estricta ES/EN e invariantes INV-PULSE-1..5 con cero fuga de datos privados."),
    ]
    for b_title, b_desc in bullets:
        p1.insert_text(fitz.Point(70, bullet_y), b_title, fontsize=10, fontname="helv", color=(0.063, 0.725, 0.506))
        p1.insert_text(fitz.Point(235, bullet_y), b_desc, fontsize=9, fontname="helv", color=(0.898, 0.91, 0.922))
        bullet_y += 24

    # Métricas y TCO Box
    p1.draw_rect(fitz.Rect(50, 460, 285, 590), color=(0.067, 0.094, 0.153), fill=(0.067, 0.094, 0.153))
    p1.insert_text(fitz.Point(65, 490), "COMPARATIVA DE COSTES A 3 AÑOS (TCO)", fontsize=9, fontname="helv", color=(0.976, 0.98, 0.984))
    p1.insert_text(fitz.Point(65, 515), "• Notion / Airtable: 1.800€ – 3.600€ recurrentes", fontsize=9, fontname="helv", color=(0.937, 0.267, 0.267))
    p1.insert_text(fitz.Point(65, 535), "• Datalaria Pulse Kit: 19€ pago único perpetuo", fontsize=9, fontname="helv", color=(0.063, 0.725, 0.506))
    p1.insert_text(fitz.Point(65, 555), "• Retorno de la Inversión: Amortizado en el Día 1", fontsize=9, fontname="helv", color=(0.898, 0.91, 0.922))
    p1.insert_text(fitz.Point(65, 575), "• Soberanía: 100% en tu máquina y tu repositorio Git", fontsize=9, fontname="helv", color=(0.024, 0.714, 0.831))

    # Box derecha: Compatibilidad
    p1.draw_rect(fitz.Rect(310, 460, 545, 590), color=(0.067, 0.094, 0.153), fill=(0.067, 0.094, 0.153))
    p1.insert_text(fitz.Point(325, 490), "COMPATIBILIDAD Y ESTÁNDARES", fontsize=9, fontname="helv", color=(0.976, 0.98, 0.984))
    p1.insert_text(fitz.Point(325, 515), "• Excel 2016, 2019, 2021, Office 365 & Sheets", fontsize=9, fontname="helv", color=(0.898, 0.91, 0.922))
    p1.insert_text(fitz.Point(325, 535), "• Hugo, Astro, Next.js, Docusaurus, Jekyll", fontsize=9, fontname="helv", color=(0.898, 0.91, 0.922))
    p1.insert_text(fitz.Point(325, 555), "• Python 3.8+ (0 dependencias externas en scanner)", fontsize=9, fontname="helv", color=(0.898, 0.91, 0.922))
    p1.insert_text(fitz.Point(325, 575), "• Supabase PostgreSQL 15 con Row-Level Security", fontsize=9, fontname="helv", color=(0.898, 0.91, 0.922))

    # Pie portada
    p1.insert_text(fitz.Point(50, 750), "Desarrollado y gobernado bajo el framework Spec-Driven Development (SDD)", fontsize=9, fontname="helv", color=(0.612, 0.639, 0.686))
    p1.insert_text(fitz.Point(50, 768), "Datalaria Engineering — https://datalaria.com/apps/pulse/", fontsize=9, fontname="helv", color=(0.063, 0.725, 0.506))

    # =========================================================================
    # PÁGINA 2: LA PLANTILLA MAESTRA EXCEL Y MODELO DE 6 HOJAS
    # =========================================================================
    p2 = doc.new_page(width=595, height=842)
    draw_header_footer(p2, 2)

    p2.insert_text(fitz.Point(50, 75), "1. La Plantilla Maestra Excel 2016/365", fontsize=18, fontname="helv", color=(0.06, 0.1, 0.16))
    p2.insert_text(
        fitz.Point(50, 95),
        "Estructura, validaciones automáticas y cuadro de mando operativo sin macros sospechosas.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.35, 0.42),
    )

    y_pos = 125
    sheets = [
        ("Hoja 1: Instrucciones", "Guía rápida de flujo editorial, atajos y referencia de uso para el equipo."),
        ("Hoja 2: Taxonomía", "Catálogo maestro de valores válidos: Tipos (POST/APP/KIT), Estados (Idea, Draft, Review, Scheduled, Published), Visibilidad (public/private), Paridad (complete, missing_en, outdated_en) y Frescura (fresh, review_needed, stale). Alimenta todas las listas desplegables."),
        ("Hoja 3: Activos", "La tabla de verdad unificada. Cada fila consolida un activo digital único bilingüe con cálculo automático de lectura, score SEO (0-100), enlaces cruzados a Apps/Kits y métricas relativas."),
        ("Hoja 4: Kanban", "Tablero visual distribuido en 5 columnas horizontales donde los contenidos se agrupan automáticamente según su estado editorial."),
        ("Hoja 5: Métricas", "Consolidación cuantitativa de Google Analytics 4 (visitas, usuarios, duración de sesión) y Google Search Console (clics, impresiones, CTR y posición media)."),
        ("Hoja 6: Dashboard", "Cuadro de mando ejecutivo con fórmulas universales (COUNTA, COUNTIF, SUM) compatibles con cualquier versión de Excel y Google Sheets (INV-PULSE-5)."),
    ]
    for s_title, s_desc in sheets:
        p2.draw_rect(fitz.Rect(50, y_pos, 545, y_pos + 42), color=(0.95, 0.96, 0.98), fill=(0.95, 0.96, 0.98))
        p2.draw_rect(fitz.Rect(50, y_pos, 54, y_pos + 42), color=(0.06, 0.72, 0.51), fill=(0.06, 0.72, 0.51))
        p2.insert_text(fitz.Point(65, y_pos + 16), s_title, fontsize=10, fontname="helv", color=(0.06, 0.1, 0.16))
        p2.insert_text(fitz.Point(65, y_pos + 32), s_desc, fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))
        y_pos += 48

    p2.insert_text(fitz.Point(50, 440), "2. Las 5 Reglas Deterministas de Auditoría SEO (0-100)", fontsize=14, fontname="helv", color=(0.06, 0.1, 0.16))
    seo_rules = [
        ("title_ok (+20 pts):", "Longitud de título comprendida entre 30 y 80 caracteres para evitar recortes en SERPs."),
        ("description_ok (+20 pts):", "Meta-descripción estructurada entre 70 y 220 caracteres."),
        ("parity_ok (+20 pts):", "Paridad bilingüe completa (ambas versiones ES y EN existen y están sincronizadas)."),
        ("taxonomy_ok (+20 pts):", "Asignación obligatoria de al menos 1 categoría y 2 o más etiquetas (tags)."),
        ("internal_links_ok (+20 pts):", "Presencia de al menos 1 enlace interno o shortcode de producto (app-ref / kit)."),
    ]
    y_seo = 465
    for r_title, r_desc in seo_rules:
        p2.insert_text(fitz.Point(65, y_seo), r_title, fontsize=9.5, fontname="helv", color=(0.06, 0.72, 0.51))
        p2.insert_text(fitz.Point(210, y_seo), r_desc, fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))
        y_seo += 20

    # Cuadro destacado
    p2.draw_rect(fitz.Rect(50, 590, 545, 680), color=(0.92, 0.98, 0.95), fill=(0.92, 0.98, 0.95))
    p2.insert_text(fitz.Point(65, 615), "INVARIANTE CONSTITUCIONAL DE PRIVACIDAD (INV-PULSE-2):", fontsize=10, fontname="helv", color=(0.04, 0.45, 0.31))
    p2.insert_text(
        fitz.Point(65, 635),
        "El dataset público 'public.json' jamás contiene cifras absolutas de facturación o visitas directas.",
        fontsize=9,
        fontname="helv",
        color=(0.18, 0.23, 0.28),
    )
    p2.insert_text(
        fitz.Point(65, 650),
        "Todas las métricas se transforman a índice Base 100 sobre la mediana (index_100) y percentil (rank_pct).",
        fontsize=9,
        fontname="helv",
        color=(0.18, 0.23, 0.28),
    )

    # =========================================================================
    # PÁGINA 3: MIGRACIÓN DESDE NOTION Y CONECTORES POWER QUERY M
    # =========================================================================
    p3 = doc.new_page(width=595, height=842)
    draw_header_footer(p3, 3)

    p3.insert_text(fitz.Point(50, 75), "3. Conectores Power Query M y Migración CLI", fontsize=18, fontname="helv", color=(0.06, 0.1, 0.16))
    p3.insert_text(
        fitz.Point(50, 95),
        "Tres rutas sin fricción para conectar tus fuentes de datos con Excel en 5 minutos.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.35, 0.42),
    )

    # Conector A
    p3.draw_rect(fitz.Rect(50, 120, 545, 235), color=(0.98, 0.98, 0.99), fill=(0.98, 0.98, 0.99))
    p3.insert_text(fitz.Point(65, 142), "Ruta A: Conector Power Query para Notion (notion_power_query.m)", fontsize=11, fontname="helv", color=(0.06, 0.1, 0.16))
    p3.insert_text(fitz.Point(65, 160), "1. En Notion: Base de datos editorial > '...' > Export > Formato CSV > Export.", fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))
    p3.insert_text(fitz.Point(65, 175), "2. En Excel: Datos > Obtener datos > De otras fuentes > Consulta en blanco > Editor avanzado.", fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))
    p3.insert_text(fitz.Point(65, 190), "3. Pega el código M de 01_Excel_Templates/notion_power_query.m y define RutaArchivoCSV.", fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))
    p3.insert_text(fitz.Point(65, 205), "4. Pulsa 'Cerrar y cargar': normaliza títulos, estados y fechas automáticamente en la hoja Activos.", fontsize=8.5, fontname="helv", color=(0.06, 0.72, 0.51))

    # Conector B
    p3.draw_rect(fitz.Rect(50, 255, 545, 370), color=(0.98, 0.98, 0.99), fill=(0.98, 0.98, 0.99))
    p3.insert_text(fitz.Point(65, 277), "Ruta B: Conector Power Query para Git public.json (git_public_json_power_query.m)", fontsize=11, fontname="helv", color=(0.06, 0.1, 0.16))
    p3.insert_text(fitz.Point(65, 295), "1. En Excel: Consulta en blanco > Editor avanzado > Pega el código de git_public_json_power_query.m.", fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))
    p3.insert_text(fitz.Point(65, 310), "2. Define RutaPublicJson con la ruta física o URL de tu dataset static/apps/pulse/data/public.json.", fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))
    p3.insert_text(fitz.Point(65, 325), "3. Pulsa 'Cerrar y cargar': cada commit en Git se refleja en Excel pulsando 'Actualizar todo'.", fontsize=8.5, fontname="helv", color=(0.06, 0.72, 0.51))
    p3.insert_text(fitz.Point(65, 340), "4. Extrae métricas relativas Base 100, percentiles y score SEO determinista sin escribir código.", fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))

    # Conector C / CLI
    p3.draw_rect(fitz.Rect(50, 390, 545, 530), color=(0.067, 0.094, 0.153), fill=(0.067, 0.094, 0.153))
    p3.insert_text(fitz.Point(65, 415), "Ruta C: Script CLI Universal (migrate_notion.py)", fontsize=11, fontname="helv", color=(0.976, 0.98, 0.984))
    p3.insert_text(fitz.Point(65, 435), "Para equipos técnicos y desarrolladores que operan en terminal:", fontsize=8.5, fontname="helv", color=(0.612, 0.639, 0.686))
    p3.insert_text(
        fitz.Point(65, 460),
        "python migrate_notion.py --input sample_notion_export.csv --output Pulse_Tracker.xlsx --format xlsx",
        fontsize=8.5,
        fontname="courier",
        color=(0.063, 0.725, 0.506),
    )
    p3.insert_text(
        fitz.Point(65, 485),
        "python migrate_notion.py --input notion_export.csv --output backlog.yaml --format yaml",
        fontsize=8.5,
        fontname="courier",
        color=(0.024, 0.714, 0.831),
    )
    p3.insert_text(
        fitz.Point(65, 510),
        "• Genera en < 2 segundos un libro Excel listo para abrir o un YAML sincronizable con Git.",
        fontsize=8.5,
        fontname="helv",
        color=(0.898, 0.91, 0.922),
    )

    # Dataset de prueba
    p3.draw_rect(fitz.Rect(50, 555, 545, 640), color=(0.95, 0.96, 0.98), fill=(0.95, 0.96, 0.98))
    p3.insert_text(fitz.Point(65, 580), "DATASET DE PRUEBA INCLUIDO (sample_notion_export.csv):", fontsize=10, fontname="helv", color=(0.06, 0.1, 0.16))
    p3.insert_text(
        fitz.Point(65, 600),
        "Prueba el migrador en 60 segundos ejecutando la Ruta C con el archivo de prueba incluido.",
        fontsize=8.5,
        fontname="helv",
        color=(0.28, 0.33, 0.39),
    )
    p3.insert_text(
        fitz.Point(65, 615),
        "Contiene 8 activos con estados heterogéneos, tags múltiples y casos límite ya resueltos.",
        fontsize=8.5,
        fontname="helv",
        color=(0.28, 0.33, 0.39),
    )

    # =========================================================================
    # PÁGINA 4: ESCÁNER UNIVERSAL, CI/CD Y EVOLUCIÓN HELIX
    # =========================================================================
    p4 = doc.new_page(width=595, height=842)
    draw_header_footer(p4, 4)

    p4.insert_text(fitz.Point(50, 75), "4. Escáner de Repositorios y Automatización CI/CD", fontsize=18, fontname="helv", color=(0.06, 0.1, 0.16))
    p4.insert_text(
        fitz.Point(50, 95),
        "Auditoría determinista sin dependencias externas y conexión segura con GA4/GSC.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.35, 0.42),
    )

    p4.insert_text(fitz.Point(50, 130), "Escáner Universal CLI (pulse_repo_scanner.py):", fontsize=12, fontname="helv", color=(0.06, 0.1, 0.16))
    p4.insert_text(
        fitz.Point(50, 150),
        "Escrito en Python puro (librería estándar, cero pip install). Audita cualquier estructura Markdown en < 200 ms:",
        fontsize=8.5,
        fontname="helv",
        color=(0.28, 0.33, 0.39),
    )
    p4.draw_rect(fitz.Rect(50, 165, 545, 215), color=(0.067, 0.094, 0.153), fill=(0.067, 0.094, 0.153))
    p4.insert_text(
        fitz.Point(65, 190),
        "python pulse_repo_scanner.py --content-dir content/ --output auditoria_editorial.csv",
        fontsize=8.5,
        fontname="courier",
        color=(0.063, 0.725, 0.506),
    )

    p4.insert_text(fitz.Point(50, 245), "Conexión a Google Analytics 4 y Search Console:", fontsize=12, fontname="helv", color=(0.06, 0.1, 0.16))
    ga_steps = [
        ("1. Google Cloud Service Account:", "Crear un proyecto, habilitar GA4 Data API y GSC API, y descargar la clave JSON."),
        ("2. Permisos de Lectura:", "Añadir el email de la Service Account con rol 'Lector' en GA4 y Search Console."),
        ("3. Ejecución Automatizada:", "Ejecutar sync_metrics.py; genera métricas privadas y las relativiza a Base 100 de forma segura."),
    ]
    y_ga = 270
    for s_step, s_desc in ga_steps:
        p4.insert_text(fitz.Point(65, y_ga), s_step, fontsize=9.5, fontname="helv", color=(0.06, 0.72, 0.51))
        p4.insert_text(fitz.Point(235, y_ga), s_desc, fontsize=8.5, fontname="helv", color=(0.28, 0.33, 0.39))
        y_ga += 22

    # El futuro: Helix Box
    p4.draw_rect(fitz.Rect(50, 360, 545, 560), color=(0.043, 0.059, 0.09), fill=(0.043, 0.059, 0.09))
    p4.draw_rect(fitz.Rect(50, 360, 545, 364), color=(0.545, 0.361, 0.965), fill=(0.545, 0.361, 0.965))
    p4.insert_text(fitz.Point(65, 390), "EL FUTURO: DATALARIA HELIX (LANZAMIENTO EN ENERO 2027)", fontsize=11, fontname="helv", color=(0.976, 0.98, 0.984))
    p4.insert_text(
        fitz.Point(65, 415),
        "Datalaria Pulse es el Caso de Estudio #1 del sistema operativo de 12 agentes Datalaria Helix.",
        fontsize=8.5,
        fontname="helv",
        color=(0.898, 0.91, 0.922),
    )
    p4.insert_text(
        fitz.Point(65, 435),
        "• Escuadrón coordinado: Orquestador con triaje XS–XL, Arquitecto, UX/UI, QA con veto vinculante.",
        fontsize=8.5,
        fontname="helv",
        color=(0.612, 0.639, 0.686),
    )
    p4.insert_text(
        fitz.Point(65, 455),
        "• Fábrica Editorial Autónoma: detección de keywords, generación asistida de borradores y review CI/CD.",
        fontsize=8.5,
        fontname="helv",
        color=(0.612, 0.639, 0.686),
    )
    p4.insert_text(
        fitz.Point(65, 475),
        "• Reserva tu acceso prioritario en: https://datalaria.com/es/recursos/#software",
        fontsize=9,
        fontname="helv",
        color=(0.024, 0.714, 0.831),
    )

    # Soporte y contacto
    p4.insert_text(fitz.Point(50, 600), "Soporte Técnico y Consultoría B2B Pro:", fontsize=11, fontname="helv", color=(0.06, 0.1, 0.16))
    p4.insert_text(fitz.Point(50, 620), "• Web Oficial: https://datalaria.com", fontsize=9, fontname="helv", color=(0.28, 0.33, 0.39))
    p4.insert_text(fitz.Point(50, 638), "• Ficha Técnica de la App: https://datalaria.com/es/apps/pulse/", fontsize=9, fontname="helv", color=(0.28, 0.33, 0.39))
    p4.insert_text(fitz.Point(50, 656), "• Email de Ingeniería: contacto@datalaria.com / dalaez1@gmail.com", fontsize=9, fontname="helv", color=(0.28, 0.33, 0.39))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    doc.close()
    print(f"[PDF GUIDE] Generado exitosamente: {output_path.resolve()} ({output_path.stat().st_size // 1024} KB)")
    return output_path


if __name__ == "__main__":
    build_pulse_pdf_guide()
