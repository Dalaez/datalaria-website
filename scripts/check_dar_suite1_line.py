with open("content/es/posts/matriz-dar-cuantitativa/index.md", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "estrategia-corporativa-mba" in line:
            print(f"Line {idx+1}: {line}")
