import os

for root, dirs, files in os.walk("assets"):
    for f in files:
        if f.endswith(".css"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as file:
                content = file.read()
                if "modal-preview" in content:
                    print(f"Found in {p}")
