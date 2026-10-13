#!/usr/bin/env python3
import os

es_path = "content/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/index.md"
en_path = "content/en/posts/decision-making-prioritization-quantitative-framework/index.md"

for p in [es_path, en_path]:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            text = f.read()
            words = text.split()
            print(f"{p}: {len(words)} words, {len(text)} characters, {len(text.splitlines())} lines")
    else:
        print(f"NOT FOUND: {p}")

es_cover = "content/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/cover.png"
en_cover = "content/en/posts/decision-making-prioritization-quantitative-framework/cover.png"

for c in [es_cover, en_cover]:
    if os.path.exists(c):
        print(f"COVER EXISTS: {c} ({os.path.getsize(c)} bytes)")
    else:
        print(f"COVER MISSING: {c}")
