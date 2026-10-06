import os, glob, re, json

posts_dir = 'content/es/posts'
data = []
for p in glob.glob(f'{posts_dir}/*/*.md'):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
    date_m = re.search(r'^date:\s*(.*?)\s*$', content, re.MULTILINE)
    tags_m = re.search(r'^tags:\s*\[(.*?)\]', content, re.MULTILINE)
    draft_m = re.search(r'^draft:\s*(true|false)', content, re.MULTILINE)
    desc_m = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
    title = title_m.group(1).strip('"\'') if title_m else os.path.basename(os.path.dirname(p))
    date = date_m.group(1).strip() if date_m else ''
    tags = [t.strip().strip('"\'') for t in tags_m.group(1).split(',')] if tags_m else []
    draft = draft_m.group(1) if draft_m else 'false'
    desc = desc_m.group(1).strip('"\'') if desc_m else ''
    data.append({
        'dir': os.path.basename(os.path.dirname(p)),
        'title': title,
        'date': date,
        'tags': tags,
        'draft': draft,
        'desc': desc
    })

print(f"Total posts found: {len(data)}")
with open('scratch/posts_summary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

for item in sorted(data, key=lambda x: x['date'], reverse=True):
    print(f"{item['date'][:10]} | {item['draft']} | {item['dir']} | {item['title'][:45]}")
