import os

for root, dirs, files in os.walk("content"):
    for f in files:
        if f.endswith(".md"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as file:
                content = file.read()
                if "toma-decisiones-priorizacion" in content:
                    print(f"Found toma-decisiones-priorizacion in {p}")
                if "decision-making-prioritization" in content:
                    print(f"Found decision-making-prioritization in {p}")
