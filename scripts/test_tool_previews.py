import os
from PIL import Image

paths_es = [
    "content/es/posts/matriz-dar-cuantitativa/preview-pack.png",
    "content/es/posts/matriz-rice-ice-priorizacion/preview-pack.png",
    "content/es/posts/business-case-financiero-van-tir/preview-pack.png"
]

paths_en = [
    "content/en/posts/quantitative-dar-matrix/preview-pack.png",
    "content/en/posts/rice-ice-prioritization-matrix/preview-pack.png",
    "content/en/posts/financial-business-case-npv-irr/preview-pack.png"
]

for p in paths_es + paths_en:
    if os.path.exists(p):
        im = Image.open(p)
        print(f"Exists: {p} ({im.size})")
    else:
        print(f"MISSING: {p}")
