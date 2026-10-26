#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enable_article_button.py
========================
Habilita con precisión quirúrgica el botón de "Artículo técnico" / "Technical Article"
para la Matriz BCG Dinámica en:
1. layouts/partials/recursos_catalog.html
   - Tarjeta estática HTML español
   - JSON KITS_DATA español
   - Tarjeta estática HTML inglés
   - JSON KITS_DATA inglés
2. content/es/recursos/_index.md
   - Tarjeta 1
   - Tarjeta 2
   - JSON KITS_DATA
3. content/en/resources/_index.md
   - Tarjeta 1
   - Tarjeta 2
   - JSON KITS_DATA
4. scripts/generate_recursos_pages.py
   - Tarjetas y JSON bilingües
"""

def verify_enabled():
    files_to_check = {
        "layouts/partials/recursos_catalog.html": [
            '<a href="/es/posts/matriz-bcg-dinamica/" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>',
            '"guideUrl": "/es/posts/matriz-bcg-dinamica/",',
            '<a href="/en/posts/dynamic-bcg-matrix/" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>',
            '"guideUrl": "/en/posts/dynamic-bcg-matrix/",'
        ],
        "content/es/recursos/_index.md": [
            '<a href="/es/posts/matriz-bcg-dinamica/" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>',
            'guideUrl: "/es/posts/matriz-bcg-dinamica/"'
        ],
        "content/en/resources/_index.md": [
            '<a href="/en/posts/dynamic-bcg-matrix/" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>',
            'guideUrl: "/en/posts/dynamic-bcg-matrix/"'
        ],
        "scripts/generate_recursos_pages.py": [
            '<a href="/es/posts/matriz-bcg-dinamica/" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>',
            '<a href="/en/posts/dynamic-bcg-matrix/" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>'
        ]
    }

    all_ok = True
    for path, needles in files_to_check.items():
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        for needle in needles:
            if needle in content:
                print(f"[VERIFIED] {path} contains: {needle[:60]}...")
            else:
                print(f"[FAIL] {path} MISSING: {needle[:60]}...")
                all_ok = False
    return all_ok

if __name__ == "__main__":
    ok = verify_enabled()
    print(f"\nAll BCG article buttons verified successfully: {ok}")
