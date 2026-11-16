"""
ops/pulse/migrate_notion.py
---------------------------
Conversor determinista y universal de exportaciones CSV de Notion a
los esquemas editoriales canónicos de Datalaria Pulse (.yaml, .json o .xlsx).

Especificación: Hitos 5.6 y 6.3 (specs/apps/pulse/spec.md).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None

try:
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    openpyxl = None


STATUS_MAP = {
    # Ideas / Backlog
    "idea": "idea",
    "ideas": "idea",
    "backlog": "idea",
    "propuesta": "idea",
    "en mente": "idea",
    "to do": "idea",
    "todo": "idea",
    "planning": "idea",
    # Borrador
    "draft": "draft",
    "drafts": "draft",
    "borrador": "draft",
    "en redacción": "draft",
    "en redaccion": "draft",
    "writing": "draft",
    "in progress": "draft",
    "wip": "draft",
    # Revisión
    "review": "review",
    "en revisión": "review",
    "en revision": "review",
    "in review": "review",
    "editing": "review",
    "qa": "review",
    # Programado
    "scheduled": "scheduled",
    "programado": "scheduled",
    "ready": "scheduled",
    "listo": "scheduled",
    "calendarizado": "scheduled",
    # Publicado
    "published": "published",
    "publicado": "published",
    "live": "published",
    "done": "published",
    "completado": "published",
    "finished": "published",
}


def normalize_status(raw_status: Optional[str]) -> str:
    """Mapea un estado arbitrario de Notion a los 5 estados canónicos de Pulse."""
    if not raw_status:
        return "idea"
    cleaned = str(raw_status).strip().lower()
    return STATUS_MAP.get(cleaned, "idea")


def parse_date_str(raw_date: Optional[str]) -> Optional[str]:
    """Normaliza diversos formatos de fecha habituales en Notion a YYYY-MM-DD."""
    if not raw_date or not str(raw_date).strip():
        return None
    val = str(raw_date).strip()

    if "->" in val:
        val = val.split("->")[0].strip()

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%B %d, %Y",
        "%b %d, %Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(val, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    match = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", val)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    return None


def generate_slug_from_title(title: str) -> str:
    """Genera un slug limpio y descriptivo a partir del título."""
    if not title:
        return "asset-untitled"
    trans = str.maketrans("áéíóúÁÉÍÓÚñÑüÜ", "aeiouAEIOUnNuU")
    slug = title.translate(trans).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug[:60] if slug else "asset-untitled"


def find_column_value(row: Dict[str, str], candidates: List[str]) -> Optional[str]:
    """Busca el valor de una columna entre varios alias posibles (case-insensitive)."""
    norm_row = {k.strip().lower(): v for k, v in row.items() if k is not None}
    for cand in candidates:
        c_low = cand.lower()
        if c_low in norm_row:
            val = norm_row[c_low]
            if val is not None and str(val).strip():
                return str(val).strip()
    return None


def parse_notion_csv(csv_path: Path) -> List[Dict[str, Any]]:
    """Lee y parsea un CSV de Notion convirtiéndolo a activos estructurados."""
    if not csv_path.exists():
        raise FileNotFoundError(f"El archivo CSV no existe: {csv_path}")

    content = csv_path.read_bytes()
    encoding = "utf-8-sig" if content.startswith(b"\xef\xbb\xbf") else "utf-8"

    text = content.decode(encoding, errors="replace")
    delimiter = ";" if text.count(";") > text.count(",") else ","

    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    assets: List[Dict[str, Any]] = []

    for row in reader:
        title = find_column_value(
            row, ["Name", "Title", "Nombre", "Título", "Titulo", "Post", "Article", "Page"]
        )
        if not title:
            continue

        raw_status = find_column_value(row, ["Status", "Estado", "State", "Fase"])
        status = normalize_status(raw_status)

        raw_date = find_column_value(
            row,
            [
                "Date",
                "Fecha",
                "Publish Date",
                "Fecha de Publicación",
                "Fecha Publicación",
                "Publication Date",
                "Target Date",
            ],
        )
        publish_date = parse_date_str(raw_date)

        category = (
            find_column_value(
                row,
                ["Category", "Categoría", "Categoria", "Área", "Area", "Pilar", "Tipo de Contenido"],
            )
            or "General"
        )

        raw_type = find_column_value(row, ["Asset Type", "Type", "Tipo", "Kind"]) or "post"
        asset_type = raw_type.lower()
        if "app" in asset_type:
            asset_type = "app"
        elif "kit" in asset_type or "pack" in asset_type:
            asset_type = "kit"
        else:
            asset_type = "post"

        raw_tags = find_column_value(row, ["Tags", "Etiquetas", "Keywords"]) or ""
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

        summary = find_column_value(
            row, ["Summary", "Notes", "Notas", "Briefing", "Descripción", "Description"]
        )

        slug = find_column_value(row, ["Slug", "ID", "Identificador"])
        if not slug:
            slug = generate_slug_from_title(title)

        title_en = find_column_value(row, ["Title EN", "Título EN", "English Title"]) or ""
        parity = "complete" if title_en else "missing_en"
        seo_score = 85 if (title_en and summary and len(tags) >= 2) else 70

        asset = {
            "id": slug,
            "asset_type": asset_type,
            "status": status,
            "visibility": "public" if status != "idea" else "private",
            "title_es": title,
            "title_en": title_en,
            "publish_date": publish_date,
            "category": category,
            "tags": tags,
            "notes": summary or "",
            "language_parity": parity,
            "seo_audit": {"score_0_100": seo_score},
            "freshness_status": "fresh",
            "source": "notion_migration",
        }
        assets.append(asset)

    return assets


try:
    from ops.pulse.kit.build_pulse_kit import generate_pulse_workbook
except ImportError:
    generate_pulse_workbook = None


def export_assets_to_xlsx(assets: List[Dict[str, Any]], output_path: Path, lang: str = "es") -> Path:
    """Exporta los activos migrados de Notion a un libro Excel profesional reutilizando el motor centralizado de Pulse."""
    if openpyxl is None:
        raise RuntimeError("Se requiere 'openpyxl' para exportar a formato .xlsx.")

    if generate_pulse_workbook is not None:
        wb = generate_pulse_workbook(assets=assets, metrics={}, is_template=False, lang=lang)
    else:
        # Fallback autónomo si no estuviera disponible el paquete
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Activos" if lang == "es" else "Assets"
        headers = ["ID", "Tipo", "Estado", "Visibilidad", "Título (ES)", "Título (EN)"]
        ws.append(headers)
        for a in assets:
            ws.append([a["id"], a.get("asset_type", "post").upper(), a.get("status", "idea").capitalize(), a.get("visibility", "public"), a.get("title_es", ""), a.get("title_en", "")])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    return output_path


def migrate_notion(
    csv_path: Path, output_path: Optional[Path] = None, out_format: str = "yaml", lang: str = "es"
) -> List[Dict[str, Any]]:
    """Importa un CSV de Notion y lo guarda en formato YAML, JSON o Excel (.xlsx)."""
    assets = parse_notion_csv(csv_path)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        effective_format = out_format.lower()
        if output_path.suffix.lower() == ".xlsx":
            effective_format = "xlsx"
        elif output_path.suffix.lower() == ".json":
            effective_format = "json"

        if effective_format == "xlsx":
            export_assets_to_xlsx(assets, output_path, lang=lang)
        elif effective_format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(assets, f, indent=2, ensure_ascii=False)
        else:
            if yaml:
                with open(output_path, "w", encoding="utf-8") as f:
                    yaml.dump(assets, f, sort_keys=False, allow_unicode=True)
            else:
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(assets, f, indent=2, ensure_ascii=False)

    return assets


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrador determinista de Notion CSV a Datalaria Pulse (.yaml, .json, .xlsx)"
    )
    parser.add_argument("csv_path_pos", nargs="?", type=Path, help="Ruta al CSV exportado de Notion")
    parser.add_argument("-i", "--input", dest="input_csv", type=Path, help="Ruta al CSV exportado de Notion")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Ruta de destino (.yaml, .json o .xlsx)")
    parser.add_argument(
        "-f",
        "--format",
        choices=["yaml", "json", "xlsx"],
        default="yaml",
        help="Formato de salida (se autodetecta si --output termina en .xlsx o .json)",
    )
    parser.add_argument("-l", "--lang", choices=["es", "en"], default="es", help="Idioma de salida en Excel (es o en)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar desglose detallado")

    args = parser.parse_args()
    csv_source = args.input_csv or args.csv_path_pos
    if not csv_source:
        parser.error("Debes indicar la ruta al archivo CSV (posicional o mediante --input).")

    try:
        assets = migrate_notion(csv_source, args.output, args.format, lang=args.lang)
        counts: Dict[str, int] = {}
        for a in assets:
            counts[a["status"]] = counts.get(a["status"], 0) + 1

        print(f"\n[OK] Importados con éxito {len(assets)} activos desde '{csv_source}':")
        print(f"  - Ideas en Backlog: {counts.get('idea', 0)}")
        print(f"  - Borradores (Draft): {counts.get('draft', 0)}")
        print(f"  - En Revisión: {counts.get('review', 0)}")
        print(f"  - Programados: {counts.get('scheduled', 0)}")
        print(f"  - Publicados: {counts.get('published', 0)}")

        if args.output:
            print(f"\nArchivo guardado en: {args.output.resolve()}\n")
    except Exception as e:
        print(f"[ERROR] Error al migrar archivo de Notion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
