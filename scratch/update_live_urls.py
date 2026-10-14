import os

REPLACEMENTS = {
    # Mega Bundle Suite 03 Control Operativo & PMBOK (22€)
    "https://datalaria.lemonsqueezy.com/checkout/buy/e5b89ce3-f635-4839-9cd3-97a17f56da44": "https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a",
    "e5b89ce3-f635-4839-9cd3-97a17f56da44": "ee578b8e-29d6-4361-ba19-4b0b5abfd89a",
}

FILES = [
    r"content\es\posts\control-operativo-pmbok-framework-cuantitativo\index.md",
    r"content\en\posts\operational-control-pmbok-quantitative-framework\index.md",
    r"content\es\recursos\_index.md",
    r"content\en\resources\_index.md",
    r"layouts\partials\recursos_catalog.html",
    r"scripts\generate_recursos_pages.py",
    r"mockup_recursos_v1.html",
    r"mockup_recursos_v2.html",
]

base_dir = r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria"

for rel_path in FILES:
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    for old_val, new_val in REPLACEMENTS.items():
        if old_val in content:
            content = content.replace(old_val, new_val)
            modified = True
            
    if modified:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {rel_path}")
    else:
        print(f"No changes needed: {rel_path}")
