import os

for root, dirs, files in os.walk("content/es/posts"):
    for f in files:
        if f.endswith(".md"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as file:
                c = file.read()
                if "estrategia-corporativa-mba-framework-cuantitativo" in c and "estrategia-corporativa-mba-framework-cuantitativo" not in p:
                    print(f"Linked from {p}")
