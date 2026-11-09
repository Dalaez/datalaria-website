import os

individual_posts = [
    ("ES DAR", "content/es/posts/matriz-dar-cuantitativa/index.md"),
    ("ES RICE", "content/es/posts/matriz-rice-ice-priorizacion/index.md"),
    ("ES BC", "content/es/posts/business-case-financiero-van-tir/index.md"),
    ("EN DAR", "content/en/posts/quantitative-dar-matrix/index.md"),
    ("EN RICE", "content/en/posts/rice-ice-prioritization-matrix/index.md"),
    ("EN BC", "content/en/posts/financial-business-case-npv-irr/index.md")
]

for label, p in individual_posts:
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()
        has_es_link = "toma-decisiones-priorizacion" in text
        has_en_link = "decision-making-prioritization" in text
        print(f"{label}: has_es_link={has_es_link}, has_en_link={has_en_link}")
