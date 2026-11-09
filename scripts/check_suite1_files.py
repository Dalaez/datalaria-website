import os

p1 = "content/es/posts/estrategia-corporativa-mba-framework-cuantitativo"
if os.path.exists(p1):
    print("Files in estrategia-corporativa-mba-framework-cuantitativo:", os.listdir(p1))

p2 = "content/en/posts/corporate-strategy-mba-quantitative-framework"
if os.path.exists(p2):
    print("Files in corporate-strategy-mba-quantitative-framework:", os.listdir(p2))
