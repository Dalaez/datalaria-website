with open("content/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/index.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines):
    if line.startswith("## "):
        print(f"Line {idx+1}: {line.strip()}")
