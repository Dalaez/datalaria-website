with open("layouts/partials/recursos_catalog.html", "r", encoding="utf-8") as f:
    text = f.read()

for idx, line in enumerate(text.splitlines()):
    if "renderModalPreview" in line:
        print(f"Line {idx+1}: {line}")
