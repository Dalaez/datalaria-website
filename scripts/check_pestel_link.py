with open("content/es/posts/matriz-pestel-cuantitativa/index.md", "r", encoding="utf-8") as f:
    text = f.read()

for line in text.splitlines():
    if "estrategia-corporativa-mba-framework-cuantitativo" in line:
        print("Pestel link:", line)
