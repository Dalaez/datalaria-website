import os

for root, dirs, files in os.walk("layouts"):
    for f in files:
        p = os.path.join(root, f)
        with open(p, "r", encoding="utf-8") as file:
            c = file.read()
            if "suite-02" in c or "decisiones" in c and "próximamente" in c.lower():
                print(f"Match in {p}")
