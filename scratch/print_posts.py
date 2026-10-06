import json

with open('scratch/posts_summary.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Sort by date
posts.sort(key=lambda x: x['date'], reverse=True)

for i, p in enumerate(posts):
    print(f"{i+1:02d}. [{p['date'][:10]}] ({p['dir']}) {p['title']}")
    print(f"    Tags: {p['tags']}")
    print(f"    Draft: {p['draft']}")
