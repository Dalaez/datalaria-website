import json

with open('scratch/categorized_posts.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

# Let's inspect samples
print("Biografías:", len(cat['biografias']))
print("Startups:", len(cat['startups']))
print("Proyectos:", len(cat['proyectos']))
print("Técnicos:", len(cat['tecnicos']))

all_posts = []
for c_name, posts in cat.items():
    for p in posts:
        all_posts.append({
            'dir': p['dir'],
            'title': p['title'],
            'date': p['date'][:10] if p['date'] else '',
            'category': c_name,
            'desc': p.get('desc', ''),
            'url': f"/es/posts/{p['dir']}/"
        })

with open('scratch/posts_for_mockup.json', 'w', encoding='utf-8') as f:
    json.dump(all_posts, f, ensure_ascii=False, indent=2)

print(f"Total posts ready for mockup: {len(all_posts)}")
