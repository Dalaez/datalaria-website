import os

def list_posts(folder):
    posts = []
    p = os.path.join("content", folder, "posts")
    if os.path.exists(p):
        for item in os.listdir(p):
            posts.append(item)
    return posts

print("ES posts:", [p for p in list_posts("es") if any(k in p for k in ["decis", "cuantitativo", "framework", "suite", "pack", "estrategia"])])
print("EN posts:", [p for p in list_posts("en") if any(k in p for k in ["decis", "quant", "framework", "suite", "pack", "strat"])])
