import os

with open("layouts/partials/recursos_catalog.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "suite-02" in line or "suite 2" in line.lower() or "decisiones" in line.lower() and "ctx" in line.lower():
        print(f"Line {idx+1}: {line.strip()[:100]}")
