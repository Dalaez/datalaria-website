with open("layouts/partials/index_profile.html", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "suite-02" in line or "decisiones" in line.lower():
            print(f"Line {idx+1}: {line.strip()[:100]}")
