import json

with open('scratch/posts_summary.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

posts.sort(key=lambda x: x['date'], reverse=True)

print("--- POSTS 1 to 45 ---")
for i, p in enumerate(posts[:45]):
    print(f"{i+1:02d}. [{p['date'][:10]}] ({p['dir']}) {p['title']}")

print("\n--- POSTS 46 to 65 ---")
for i, p in enumerate(posts[45:65]):
    print(f"{i+46:02d}. [{p['date'][:10]}] ({p['dir']}) {p['title']}")
