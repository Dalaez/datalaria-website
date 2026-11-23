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

def _post_is_live(post_rel: str) -> bool:
    import datetime, re
    p = pathlib.Path(post_rel)
    if not p.exists():
        return False
    txt = p.read_text(encoding="utf-8")
    draft_m = re.search(r"^draft:\s*(true|false)", txt, re.M)
    if draft_m and draft_m.group(1) == "true":
        return False
    date_m = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", txt, re.M)
    if not date_m:
        return True
    pub = datetime.date.fromisoformat(date_m.group(1))
    return pub <= datetime.date.today()


def _resolve_post_conditionals(text: str, lang: str, var_name: str, es_tuple: tuple[str, str], en_tuple: tuple[str, str]) -> str:
    import re
    rel, url = es_tuple if lang == "es" else en_tuple
    live = _post_is_live(rel)

    def _repl(m):
        branch = m.group(1) if live else m.group(2)
        return branch.replace(f"{{{{ ${var_name}.RelPermalink }}}}", url)

    return re.sub(
        rf"\{{\{{\s*if \${var_name}\s*\}}\}}(.*?)\{{\{{\s*else\s*\}}\}}(.*?)\{{\{{\s*end\s*\}}\}}",
        _repl,
        text,
    )


def get_bodies():
    cat_path = pathlib.Path("layouts/partials/recursos_catalog.html")
    cat_text = cat_path.read_text(encoding="utf-8")
    parts = cat_text.split("{{- else -}}")
    assert len(parts) == 2, "recursos_catalog.html must contain {{- else -}}"
    
    es_part = _resolve_post_conditionals(
        parts[0],
        "es",
        "pertPost",
        ("content/es/posts/estimacion-pert-3-puntos/index.md", "/es/posts/estimacion-pert-3-puntos/"),
        ("content/en/posts/stochastic-3-point-pert-estimation/index.md", "/en/posts/stochastic-3-point-pert-estimation/"),
    )
    es_part = _resolve_post_conditionals(
        es_part,
        "es",
        "evmPost",
        ("content/es/posts/cuadro-mando-evm-valor-ganado/index.md", "/es/posts/cuadro-mando-evm-valor-ganado/"),
        ("content/en/posts/earned-value-management-evm-dashboard/index.md", "/en/posts/earned-value-management-evm-dashboard/"),
    )
    es_part = _resolve_post_conditionals(
        es_part,
        "es",
        "stockPost",
        ("content/es/posts/calculadora-stock-seguridad-rop/index.md", "/es/posts/calculadora-stock-seguridad-rop/"),
        ("content/en/posts/safety-stock-reorder-point-calculator/index.md", "/en/posts/safety-stock-reorder-point-calculator/"),
    )

    en_part = _resolve_post_conditionals(
        parts[1].rsplit("{{- end -}}", 1)[0],
        "en",
        "pertPost",
        ("content/es/posts/estimacion-pert-3-puntos/index.md", "/es/posts/estimacion-pert-3-puntos/"),
        ("content/en/posts/stochastic-3-point-pert-estimation/index.md", "/en/posts/stochastic-3-point-pert-estimation/"),
    )
    en_part = _resolve_post_conditionals(
        en_part,
        "en",
        "evmPost",
        ("content/es/posts/cuadro-mando-evm-valor-ganado/index.md", "/es/posts/cuadro-mando-evm-valor-ganado/"),
        ("content/en/posts/earned-value-management-evm-dashboard/index.md", "/en/posts/earned-value-management-evm-dashboard/"),
    )
    en_part = _resolve_post_conditionals(
        en_part,
        "en",
        "stockPost",
        ("content/es/posts/calculadora-stock-seguridad-rop/index.md", "/es/posts/calculadora-stock-seguridad-rop/"),
        ("content/en/posts/safety-stock-reorder-point-calculator/index.md", "/en/posts/safety-stock-reorder-point-calculator/"),
    )
    
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
