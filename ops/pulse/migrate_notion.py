"""
ops/pulse/migrate_notion.py
---------------------------
Conversor determinista y universal de exportaciones CSV de Notion a
los esquemas editoriales canónicos de Datalaria Pulse.

Especificación: Hito 5.6 (specs/apps/pulse/spec.md).

Permite transformar en segundos cualquier base de datos editorial de Notion
en un archivo YAML compatible con data/editorial/backlog.yaml o JSON.
"""

import sys
import csv
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None


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
    
    # Extraer primera fecha si viene en rango tipo "2026-10-15 -> 2026-10-20"
    if "->" in val:
        val = val.split("->")[0].strip()

    # Formatos típicos
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%B %d, %Y",
        "%b %d, %Y"
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(val, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Regex para extraer patrón de 4 dígitos año
    match = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", val)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    return None


def generate_slug_from_title(title: str) -> str:
    """Genera un slug limpio y descriptivo a partir del título."""
    if not title:
        return "asset-untitled"
    # Reemplazar acentos
    trans = str.maketrans("áéíóúÁÉÍÓÚñÑüÜ", "aeiouAEIOUnNuU")
    slug = title.translate(trans).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug[:60] if slug else "asset-untitled"


def find_column_value(row: Dict[str, str], candidates: List[str]) -> Optional[str]:
    """Busca el valor de una columna entre varios alias posibles (case-insensitive)."""
    norm_row = {k.strip().lower(): v for k, v in row.items()}
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

    # Detectar codificación y delimitador
    content = csv_path.read_bytes()
    encoding = "utf-8-sig" if content.startswith(b"\xef\xbb\xbf") else "utf-8"
    
    text = content.decode(encoding, errors="replace")
    delimiter = ";" if text.count(";") > text.count(",") else ","

    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    assets = []

    for row in reader:
        # 1. Título
        title = find_column_value(row, [
            "Name", "Title", "Nombre", "Título", "Titulo", "Post", "Article", "Page"
        ])
        if not title:
            continue # Fila vacía de Notion

        # 2. Estado
        raw_status = find_column_value(row, ["Status", "Estado", "State", "Fase"])
        status = normalize_status(raw_status)

        # 3. Fecha
        raw_date = find_column_value(row, [
            "Date", "Fecha", "Publish Date", "Fecha de Publicación",
            "Fecha Publicación", "Publication Date", "Target Date"
        ])
        publish_date = parse_date_str(raw_date)

        # 4. Categoría
        category = find_column_value(row, [
            "Category", "Categoría", "Categoria", "Área", "Area", "Pilar", "Tipo de Contenido"
        ]) or "General"

        # 5. Tipo de activo
        raw_type = find_column_value(row, ["Asset Type", "Type", "Tipo", "Kind"]) or "post"
        asset_type = raw_type.lower()
        if "app" in asset_type:
            asset_type = "app"
        elif "kit" in asset_type or "pack" in asset_type:
            asset_type = "kit"
        else:
            asset_type = "post"

        # 6. Tags
        raw_tags = find_column_value(row, ["Tags", "Etiquetas", "Keywords"]) or ""
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

        # 7. Resumen / Notas
        summary = find_column_value(row, [
            "Summary", "Notes", "Notas", "Briefing", "Descripción", "Description"
        ])

        # 8. Slug / ID
        slug = find_column_value(row, ["Slug", "ID", "Identificador"])
        if not slug:
            slug = generate_slug_from_title(title)

        asset = {
            "id": slug,
            "asset_type": asset_type,
            "status": status,
            "visibility": "public" if status != "idea" else "private",
            "title_es": title,
            "title_en": "",
            "publish_date": publish_date,
            "category": category,
            "tags": tags,
            "notes": summary or "",
            "source": "notion_migration"
        }
        assets.append(asset)

    return assets


def migrate_notion(csv_path: Path, output_path: Optional[Path] = None, out_format: str = "yaml") -> List[Dict[str, Any]]:
    """Función de alto nivel para importar CSV y guardarlo en formato YAML o JSON."""
    assets = parse_notion_csv(csv_path)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if out_format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(assets, f, indent=2, ensure_ascii=False)
        else:
            # YAML por defecto
            if yaml:
                with open(output_path, "w", encoding="utf-8") as f:
                    yaml.dump(assets, f, sort_keys=False, allow_unicode=True)
            else:
                # Fallback sin pyyaml
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(assets, f, indent=2, ensure_ascii=False)

    return assets


def main():
    parser = argparse.ArgumentParser(description="Migrador de base de datos de Notion a Datalaria Pulse")
    parser.add_argument("csv_path", type=Path, help="Ruta al CSV exportado de Notion")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Ruta de destino (.yaml o .json)")
    parser.add_argument("-f", "--format", choices=["yaml", "json"], default="yaml", help="Formato de salida")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar desglose detallado de importación")

    args = parser.parse_args()

    try:
        assets = migrate_notion(args.csv_path, args.output, args.format)
        
        # Resumen estadístico
        counts = {}
        for a in assets:
            counts[a["status"]] = counts.get(a["status"], 0) + 1

        print(f"\n[OK] Importados con éxito {len(assets)} activos desde '{args.csv_path}':")
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
