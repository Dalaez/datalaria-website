import os
from PIL import Image

p = "content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/preview-pack.png"
if os.path.exists(p):
    im = Image.open(p)
    print("Suite 1 preview-pack.png:", im.size, im.format, os.path.getsize(p))

for root, dirs, files in os.walk("content"):
    for f in files:
        if "preview" in f.lower() or "captura" in f.lower():
            fp = os.path.join(root, f)
            print("Found image:", fp, os.path.getsize(fp))

for root, dirs, files in os.walk("static"):
    for f in files:
        if "preview" in f.lower() or "suite" in f.lower():
            fp = os.path.join(root, f)
            print("Found static image:", fp, os.path.getsize(fp))
