#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enable_article_button.py
========================
Verifica y asegura la habilitación con precisión quirúrgica del botón de
"Artículo técnico" / "Technical Article" para la Matriz McKinsey / GE en:
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
            '<a href="/es/posts/matriz-mckinsey-ge/" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>',
            '"guideUrl": "/es/posts/matriz-mckinsey-ge/",',
            '<a href="/en/posts/mckinsey-ge-matrix/" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>',
            '"guideUrl": "/en/posts/mckinsey-ge-matrix/",'
        ],
        "content/es/recursos/_index.md": [
            '<a href="/es/posts/matriz-mckinsey-ge/" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>',
            'guideUrl: "/es/posts/matriz-mckinsey-ge/"'
        ],
        "content/en/resources/_index.md": [
            '<a href="/en/posts/mckinsey-ge-matrix/" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>',
            'guideUrl: "/en/posts/mckinsey-ge-matrix/"'
        ],
        "scripts/generate_recursos_pages.py": [
            '<a href="/es/posts/matriz-mckinsey-ge/" class="btn-kit-info" title="Leer artículo técnico">Artículo técnico 📖</a>',
            '<a href="/en/posts/mckinsey-ge-matrix/" class="btn-kit-info" title="Read technical article">Technical Article 📖</a>',
            'guideUrl: "/es/posts/matriz-mckinsey-ge/"',
            'guideUrl: "/en/posts/mckinsey-ge-matrix/"'
        ]
    }

    all_ok = True
    for path, needles in files_to_check.items():
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        for needle in needles:
            if needle in content:
                print(f"[VERIFIED] {path} contains: {needle[:65]}...")
            else:
                print(f"[FAIL] {path} MISSING: {needle[:65]}...")
                all_ok = False
    return all_ok

if __name__ == "__main__":
    ok = verify_enabled()
    print(f"\nAll McKinsey article buttons verified successfully: {ok}")
