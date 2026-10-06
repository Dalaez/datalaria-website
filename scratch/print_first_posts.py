import json

with open('scratch/posts_summary.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

posts.sort(key=lambda x: x['date'], reverse=True)

print("--- POSTS 1 to 10 ---")
for i, p in enumerate(posts[:10]):
    print(f"{i+1:02d}. [{p['date'][:10]}] ({p['dir']}) {p['title']}")
