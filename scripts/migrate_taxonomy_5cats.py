"""
scripts/migrate_taxonomy_5cats.py
---------------------------------
Migración determinista de taxonomías a 5 Pilares Editoriales bajo SPEC-PORTAL-TAXONOMY y ADR-016.
Invariante INV-TAX-1: Cero alteración destructiva de tags o categories existentes (Blindaje SEO).
"""

import os
import re
from typing import Dict, Tuple, Set
import frontmatter

from ops.pulse.build_index import scan_posts, get_git_file_lastmod_map

# Definición canónica de los 5 pilares
CANONICAL_CATS = {
    "tech": {
        "es": "IA, Ingeniería y Proyectos",
        "en": "AI, Engineering & Projects",
        "icon": "🛠️",
        "label_es": "IA, Ingeniería & Proyectos",
        "label_en": "AI, Engineering & Projects"
    },
    "strategy": {
        "es": "Estrategia y Operaciones",
        "en": "Strategy & Operations",
        "icon": "📊",
        "label_es": "Estrategia & Operaciones",
        "label_en": "Strategy & Operations"
    },
    "startups": {
        "es": "Startups",
        "en": "Startups",
        "icon": "🚀",
        "label_es": "Startups & Casos",
        "label_en": "Startups & Cases"
    },
    "pioneers": {
        "es": "Pioneros y Referentes",
        "en": "Pioneers & Icons",
        "icon": "🏛️",
        "label_es": "Pioneros & Referentes",
        "label_en": "Pioneers & Icons"
    },
    "culture": {
        "es": "Cultura Tech y Media",
        "en": "Tech Culture & Media",
        "icon": "🎬",
        "label_es": "Cultura Tech & Media",
        "label_en": "Tech Culture & Media"
    }
}

CULTURE_SLUGS = {
    'her', 'ex_machina', 'devs', 'halt_and_catch_fire', 'silicon_valley',
    'the_thinking_game', 'the-goal', 'founderz-programando-chatGPT',
    'notebooklm-sql', 'ia-educacion-deep_research', 'nanobanana-ingenieria',
    'kilometro-0-por-que-nace-datalaria'
}

STRATEGY_SLUGS = {
    '5-fuerzas-porter-cuantitativas', 'dafo-cuantitativo-matriz-came',
    'matriz-bcg-dinamica', 'matriz-mckinsey-ge', 'matriz-pestel-cuantitativa',
    'estrategia-corporativa-mba-framework-cuantitativo',
    'business-case-financiero-van-tir', 'cuadro-mando-evm-valor-ganado',
    'estimacion-pert-3-puntos', 'matriz-raci-balance-carga',
    'matriz-riesgos-amfe-fmea', 'calculadora-stock-seguridad-rop',
    'control-operativo-pmbok-framework-cuantitativo',
    'matriz-dar-cuantitativa', 'matriz-rice-ice-priorizacion',
    'toma-decisiones-priorizacion-framework-cuantitativo',
    'executive-decision-packs-framework-cuantitativo',
    'BPMN_SOP', 'reuniones_IA', 'onboarding'
}

def get_pillar_for_asset(slug: str, current_cat_es: str) -> str:
    if current_cat_es == "Startups":
        return "startups"
    if current_cat_es in ("Biografías", "Biographies"):
        return "pioneers"
    if slug in CULTURE_SLUGS:
        return "culture"
    if slug in STRATEGY_SLUGS:
        return "strategy"
    return "tech"

def update_file_frontmatter(file_path: str, new_category_val: str, lang: str):
    """
    Actualiza con regex precisa la línea category: y añade la categoría a categories:
    sin reordenar ni tocar tags, description, saltos de línea ni el resto del documento.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Extraer frontmatter
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$", content)
    if not match:
        raise ValueError(f"No se pudo extraer frontmatter de {file_path}")

    fm_text = match.group(1)
    body_text = match.group(2)

    # 2. Reemplazar o insertar category:
    if re.search(r"^category:\s*.*$", fm_text, flags=re.MULTILINE):
        new_fm = re.sub(
            r"^category:\s*.*$",
            f'category: "{new_category_val}"',
            fm_text,
            flags=re.MULTILINE
        )
    else:
        new_fm = fm_text + f'\ncategory: "{new_category_val}"'

    # 3. Preservar y enriquecer categories: (sin borrar ninguna)
    # Parseamos temporalmente para saber si new_category_val ya está
    parsed = frontmatter.loads(content)
    curr_categories = parsed.metadata.get("categories") or []
    if isinstance(curr_categories, str):
        curr_categories = [curr_categories]
    
    # Si la nueva categoría no está presente, la añadimos preservando las existentes
    if new_category_val not in curr_categories:
        updated_cats = list(curr_categories) + [new_category_val]
        cats_formatted = ', '.join([f'"{c}"' for c in updated_cats])
        if re.search(r"^categories:\s*.*$", new_fm, flags=re.MULTILINE):
            new_fm = re.sub(
                r"^categories:\s*.*$",
                f'categories: [{cats_formatted}]',
                new_fm,
                flags=re.MULTILINE
            )
        else:
            new_fm = new_fm + f'\ncategories: [{cats_formatted}]'

    # 4. Reconstruir archivo intacto
    new_content = f"---\n{new_fm}\n---\n{body_text}"
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)

def main():
    git_map = get_git_file_lastmod_map()
    post_assets = scan_posts(git_map)
    print(f"Total post assets emparejados a procesar: {len(post_assets)}")

    # Guardar snapshot de tags para validación estricta de invariante INV-TAX-1
    tags_snapshot: Dict[str, list] = {}
    for p in post_assets:
        tags_snapshot[p.slug] = list(p.tags)

    updated_count = 0
    bucket_counts = {k: 0 for k in CANONICAL_CATS}

    for p in post_assets:
        pillar = get_pillar_for_asset(p.slug, p.category)
        bucket_counts[pillar] += 1
        cat_es = CANONICAL_CATS[pillar]["es"]
        cat_en = CANONICAL_CATS[pillar]["en"]

        # Rutas de archivo
        es_path = os.path.join("content", "es", "posts", p.slug, "index.md")
        # El nombre del directorio EN puede diferir según build_index mapping
        # Buscamos en url_en o en content/en/posts
        en_slug = p.url_en.strip("/").split("/")[-1] if p.url_en else p.slug
        en_path = os.path.join("content", "en", "posts", en_slug, "index.md")

        if os.path.exists(es_path):
            update_file_frontmatter(es_path, cat_es, "es")
            updated_count += 1
        else:
            print(f"[WARN] Archivo ES no encontrado: {es_path}")

        if os.path.exists(en_path):
            update_file_frontmatter(en_path, cat_en, "en")
            updated_count += 1
        else:
            print(f"[WARN] Archivo EN no encontrado: {en_path}")

    print(f"\n[OK] Archivos actualizados: {updated_count}")
    print("\nDistribución final por Pilar:")
    for k, v in bucket_counts.items():
        print(f"  - {CANONICAL_CATS[k]['icon']} {CANONICAL_CATS[k]['es']} ({CANONICAL_CATS[k]['label_es']}): {v} artículos")

    # VALIDACIÓN DE INVARIANTE INV-TAX-1 (Blindaje SEO de Tags)
    print("\n--- Verificando Invariante INV-TAX-1 (Preservación de Tags)... ---")
    verified_assets = scan_posts(git_map)
    for vp in verified_assets:
        orig_tags = tags_snapshot.get(vp.slug, [])
        curr_tags = vp.tags
        for t in orig_tags:
            if t not in curr_tags:
                raise RuntimeError(f"VIOLACIÓN DE INV-TAX-1: Tag '{t}' desaparecido en post {vp.slug}!")
    print("[PASS] 100% de los tags preexistentes se han preservado intactos sin alteración.")

if __name__ == "__main__":
    main()
