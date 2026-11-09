posts = [
    "content/es/posts/matriz-dar-cuantitativa/index.md",
    "content/es/posts/matriz-rice-ice-priorizacion/index.md",
    "content/es/posts/business-case-financiero-van-tir/index.md",
    "content/en/posts/quantitative-dar-matrix/index.md",
    "content/en/posts/rice-ice-prioritization-matrix/index.md",
    "content/en/posts/financial-business-case-npv-irr/index.md"
]

for p in posts:
    with open(p, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for idx, l in enumerate(lines[:35]):
            if l.startswith("## "):
                print(f"{p}: Section 1 at line {idx+1}: {l.strip()}")
