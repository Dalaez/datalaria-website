import os

target = "Artículo próximamente"
for root, dirs, files in os.walk("."):
    if ".git" in root or "node_modules" in root or "public" in root or ".gemini" in root:
        continue
    for f in files:
        if f.endswith((".md", ".html", ".yaml", ".yml", ".json", ".toml", ".js", ".ts")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8") as file:
                    content = file.read()
                    if target in content or "próximamente" in content.lower():
                        print(f"Found in {p}")
            except Exception:
                pass
