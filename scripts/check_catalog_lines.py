with open("layouts/partials/recursos_catalog.html", "r", encoding="utf-8") as f:
    text = f.read()

print("ES Quick Grid lines:")
for idx, line in enumerate(text.splitlines()[:150]):
    if "suite-02" in line or "Artículo próximamente" in line:
        print(f"Line {idx+1}: {line}")

print("\nEN Quick Grid lines:")
for idx, line in enumerate(text.splitlines()[2070:2130]):
    if "suite-02" in line or "Article coming soon" in line:
        print(f"Line {idx+2071}: {line}")
