import os
import pathlib

es_frontmatter = """---
title: "Executive Decision Packs"
description: "Modelos cuantitativos en Excel, presentaciones PowerPoint 16:9 C-Level y guías metodológicas para defender decisiones estratégicas en comités de dirección."
draft: false
hidemeta: true
translationKey: resources
---
"""

en_frontmatter = """---
title: "Executive Decision Packs"
description: "Quantitative Excel models, 16:9 C-Level PowerPoint presentations and methodological guides to defend strategic decisions in executive committees."
draft: false
hidemeta: true
translationKey: resources
---
"""

def get_bodies():
    cat_path = pathlib.Path("layouts/partials/recursos_catalog.html")
    cat_text = cat_path.read_text(encoding="utf-8")
    parts = cat_text.split("{{- else -}}")
    assert len(parts) == 2, "recursos_catalog.html must contain {{- else -}}"
    
    es_part = parts[0]
    en_part = parts[1].split("{{- end -}}")[0]
    
    es_lines = [l for l in es_part.splitlines() if not l.startswith("{{-")]
    en_lines = [l for l in en_part.splitlines() if not l.startswith("{{-")]
    
    return "\n".join(es_lines).strip() + "\n", "\n".join(en_lines).strip() + "\n"

def main():
    es_body, en_body = get_bodies()
    es_file = os.path.join("content", "es", "recursos", "_index.md")
    en_file = os.path.join("content", "en", "resources", "_index.md")

    with open(es_file, "w", encoding="utf-8") as f:
        f.write(es_frontmatter + "\n" + es_body)
    print(f"Written: {es_file}")

    with open(en_file, "w", encoding="utf-8") as f:
        f.write(en_frontmatter + "\n" + en_body)
    print(f"Written: {en_file}")

if __name__ == "__main__":
    main()
