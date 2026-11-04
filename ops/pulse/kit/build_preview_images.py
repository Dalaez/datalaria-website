"""
ops/pulse/kit/build_preview_images.py
-------------------------------------
Generador determinista de imágenes preview de alta resolución (1600x980 px)
para el producto comercial Datalaria Pulse Kit en Lemon Squeezy y el catálogo del portal.

Genera:
  - static/images/recursos/pulse-preview-es.png
  - static/images/recursos/pulse-preview-en.png
utilizando Pillow y PyMuPDF (fitz) para renderizar páginas reales del PDF.
"""

import sys
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PDF_PATH = ROOT_DIR / "packages" / "pulse" / "GUIA_EJECUTIVA_PULSE.pdf"
OUTPUT_DIR = ROOT_DIR / "static" / "images" / "recursos"

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

# Dimensiones estándar de previsualizaciones Datalaria
WIDTH = 1600
HEIGHT = 980


def get_font(size: int, bold: bool = False):
    """Obtiene una fuente tipográfica del sistema con fallback a default."""
    font_names = [
        "seguisb.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_pdf_page(doc, page_num: int, target_height: int) -> Image.Image:
    """Renderiza una página del PDF a imagen PIL con target_height."""
    page = doc[page_num]
    # Usar zoom para nitidez óptima
    zoom = (target_height / page.rect.height) * 1.5
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    # Redimensionar al tamaño exacto deseado con antialiasing
    aspect = img.width / img.height
    target_width = int(target_height * aspect)
    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)


def add_drop_shadow(base_img: Image.Image, element: Image.Image, x: int, y: int, shadow_offset: int = 14, border_color=(16, 185, 129)):
    """Pega un elemento con sombra paralela suave y borde elegante."""
    # Sombra
    shadow_box = Image.new("RGBA", (element.width + shadow_offset * 2, element.height + shadow_offset * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_box)
    sdraw.rectangle(
        [shadow_offset, shadow_offset, shadow_box.width - 2, shadow_box.height - 2],
        fill=(0, 0, 0, 160)
    )
    # Pegar sombra
    base_img.paste(shadow_box, (x - shadow_offset // 2, y - shadow_offset // 2), mask=shadow_box)

    # Elemento con borde
    elem_with_border = element.copy().convert("RGBA")
    edraw = ImageDraw.Draw(elem_with_border)
    edraw.rectangle([0, 0, elem_with_border.width - 1, elem_with_border.height - 1], outline=border_color, width=2)
    base_img.paste(elem_with_border, (x, y))


def build_preview(lang: str = "es") -> Path:
    """Genera la imagen de previsualización 1600x980 px para el idioma indicado."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"pulse-preview-{lang}.png"

    # 1. Canvas de Fondo Ejecutivo Oscuro
    img = Image.new("RGB", (WIDTH, HEIGHT), color="#0b0f17")
    draw = ImageDraw.Draw(img)

    # Fondo degradado radial sutil en la zona central/derecha
    for r in range(500, 0, -10):
        alpha = int(18 * (1 - r / 500))
        draw.ellipse([800 - r, 490 - r, 800 + r, 490 + r], fill=(16, int(24 + alpha * 0.8), int(39 + alpha)))

    # Líneas de rejilla estética
    for y in range(0, HEIGHT, 70):
        draw.line([(0, y), (WIDTH, y)], fill=(17, 24, 39), width=1)
    for x in range(0, WIDTH, 100):
        draw.line([(x, 0), (x, HEIGHT)], fill=(17, 24, 39), width=1)

    # Marco exterior
    draw.rectangle([16, 16, WIDTH - 17, HEIGHT - 17], outline=(30, 41, 59), width=2)
    draw.rectangle([20, 20, WIDTH - 21, HEIGHT - 21], outline=(16, 185, 129), width=1)

    # Fuentes
    f_badge = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(22, bold=False)
    f_item_title = get_font(21, bold=True)
    f_item_desc = get_font(16, bold=False)
    f_kpi_num = get_font(32, bold=True)
    f_kpi_lbl = get_font(14, bold=False)
    f_price_badge = get_font(26, bold=True)

    # Textos según idioma
    if lang == "es":
        badge_text = "KIT COMERCIAL B2B · ARQUITECTURA DUAL-MODE · 19€"
        title_text = "Datalaria Pulse Content Ops Kit"
        sub_text = "Plantilla Maestra Excel, Migrador Notion CLI y Conectores Git en 5 min"
        features = [
            ("01. Plantilla Maestra Excel (.xlsx)", "6 hojas estructuradas (Taxonomía, Activos, Kanban, Métricas y Dashboard)"),
            ("02. Doble Conector Power Query M", "Sincronización de un clic con Notion CSV y con public.json de repositorios Git"),
            ("03. Migrador Notion CLI Determinista", "Script python con exportación directa a .xlsx, .yaml o .json y dataset de prueba"),
            ("04. Guía Ejecutiva Maquetada en PDF", "Manual visual de 4 páginas A4 con arquitectura, flujos y roadmap hacia Modo Cloud"),
        ]
        kpi_items = [
            ("19€", "Pago Único Perpetuo (Launch)"),
            ("6 Hojas", "Libro Excel Master"),
            ("< 5 min", "Migración desde Notion"),
            ("100%", "Soberanía de Datos"),
        ]
        footer_left = "datalaria.com/es/recursos/#pack-pulse · Compatible con Excel 2016/365 & Power Query"
        footer_right = "Buy Once, Own Forever · Cero Suscripciones"
    else:
        badge_text = "B2B COMMERCIAL KIT · DUAL-MODE ARCHITECTURE · 19€"
        title_text = "Datalaria Pulse Content Ops Kit"
        sub_text = "Master Excel Template, Notion Migration CLI & Git Connectors in 5 min"
        features = [
            ("01. Master Excel Template (.xlsx)", "6 structured sheets (Taxonomy, Assets, Kanban, Metrics & Executive Dashboard)"),
            ("02. Dual Power Query M Connectors", "One-click synchronization with Notion CSV and Git public.json manifests"),
            ("03. Deterministic Notion Migration CLI", "Python CLI engine exporting directly to .xlsx, .yaml or .json + test dataset"),
            ("04. Executive Formatted PDF Guide", "4-page A4 visual handbook with dual architecture, flows & Pro Cloud roadmap"),
        ]
        kpi_items = [
            ("19€", "One-Time Payment (Launch)"),
            ("6 Sheets", "Master Excel Workbook"),
            ("< 5 min", "Notion Migration"),
            ("100%", "Data Sovereignty"),
        ]
        footer_left = "datalaria.com/en/resources/#pack-pulse · Compatible with Excel 2016/365 & Power Query"
        footer_right = "Buy Once, Own Forever · Zero Recurring Fees"

    # Cabecera / Badge Superior
    draw.rounded_rectangle([70, 60, 680, 96], radius=8, fill=(16, 185, 129, 30), outline=(16, 185, 129), width=1)
    draw.text((88, 68), badge_text, fill=(52, 211, 153), font=f_badge)

    # Título y Subtítulo
    draw.text((70, 118), title_text, fill=(249, 250, 251), font=f_title)
    draw.text((70, 178), sub_text, fill=(156, 163, 175), font=f_sub)

    # Bloque de 4 Features
    y_start = 245
    for i, (feat_title, feat_desc) in enumerate(features):
        box_y = y_start + i * 92
        # Card container
        draw.rounded_rectangle([70, box_y, 790, box_y + 78], radius=8, fill=(17, 24, 39), outline=(51, 65, 85), width=1)
        # Bullet verde
        draw.rounded_rectangle([86, box_y + 14, 114, box_y + 42], radius=6, fill=(16, 185, 129), outline=(5, 150, 105))
        draw.text((94, box_y + 18), "✓", fill=(255, 255, 255), font=f_badge)
        # Textos
        draw.text((130, box_y + 14), feat_title, fill=(249, 250, 251), font=f_item_title)
        draw.text((130, box_y + 44), feat_desc, fill=(156, 163, 175), font=f_item_desc)

    # Bloque de 4 KPIs en la parte inferior izquierda
    kpi_y = 645
    for k_idx, (num, lbl) in enumerate(kpi_items):
        kx = 70 + k_idx * 185
        draw.rounded_rectangle([kx, kpi_y, kx + 172, kpi_y + 86], radius=8, fill=(15, 23, 42), outline=(16, 185, 129), width=1)
        draw.text((kx + 16, kpi_y + 12), num, fill=(16, 185, 129), font=f_kpi_num)
        draw.text((kx + 16, kpi_y + 52), lbl, fill=(148, 163, 184), font=f_kpi_lbl)

    # Sello de Precio Founder
    draw.rounded_rectangle([70, 755, 420, 815], radius=10, fill=(16, 185, 129), outline=(5, 150, 105), width=2)
    draw.text((88, 770), "⚡ 19€  ·  EARLY-BIRD (Reg: 39€)", fill=(11, 15, 23), font=f_price_badge)

    # 2. Renderizado de Páginas Reales del PDF si fitz está disponible
    if fitz and PDF_PATH.exists():
        try:
            doc = fitz.open(PDF_PATH)
            # Renderizar Página 1 (Portada ejecutiva)
            p1_img = render_pdf_page(doc, 0, target_height=650)
            # Renderizar Página 2 (Estructura Excel y 6 hojas)
            p2_img = render_pdf_page(doc, 1, target_height=560) if len(doc) > 1 else None

            # Pegar p2 ligeramente detrás a la derecha
            if p2_img:
                add_drop_shadow(img, p2_img, x=1090, y=140, shadow_offset=18, border_color=(6, 182, 212))

            # Pegar p1 en primer plano solapada
            add_drop_shadow(img, p1_img, x=840, y=110, shadow_offset=22, border_color=(16, 185, 129))

            # Etiqueta de la maqueta
            draw.rounded_rectangle([1080, 780, 1520, 825], radius=8, fill=(17, 24, 39), outline=(16, 185, 129), width=1)
            draw.text((1100, 792), "📄 GUIA_EJECUTIVA_PULSE.pdf (4 Páginas A4)", fill=(249, 250, 251), font=f_badge)
            doc.close()
        except Exception as e:
            print(f"Advertencia renderizando PDF: {e}")

    # Footer
    f_footer = get_font(15, bold=False)
    draw.line([(70, 890), (WIDTH - 70, 890)], fill=(51, 65, 85), width=1)
    draw.text((70, 915), footer_left, fill=(148, 163, 184), font=f_footer)
    draw.text((WIDTH - 420, 915), footer_right, fill=(16, 185, 129), font=f_footer)

    img.save(out_path, format="PNG", optimize=True)
    size_kb = round(out_path.stat().st_size / 1024, 1)
    print(f"[PREVIEW] Generada imagen {out_path.name} ({WIDTH}x{HEIGHT} px, {size_kb} KB)")
    return out_path


def main():
    print("[PREVIEW BUILDER] Generando capturas de alta resolución para Datalaria Pulse Kit...")
    es_path = build_preview("es")
    en_path = build_preview("en")
    print(f"\n[OK] Previews generadas exitosamente:\n  - {es_path}\n  - {en_path}\n")


if __name__ == "__main__":
    main()
