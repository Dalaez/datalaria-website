import os

for root, dirs, files in os.walk("scripts"):
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as file:
                content = file.read()
                if "preview" in content.lower() or "suite-01" in content or "composite" in content:
                    print(f"Match in {p}")
