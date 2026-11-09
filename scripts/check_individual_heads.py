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
        lines = [f.readline() for _ in range(25)]
        print(f"=== {p} ===")
        for idx, l in enumerate(lines):
            if l.startswith("## ") or "---" in l:
                print(f"  Line {idx+1}: {l.strip()}")
