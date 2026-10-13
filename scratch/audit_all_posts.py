import os, glob, re, json

def audit(lang):
    base_dir = f'content/{lang}/posts'
    posts = []
    for d in sorted(os.listdir(base_dir)):
        full_d = os.path.join(base_dir, d)
        if not os.path.isdir(full_d):
            continue
        md_files = glob.glob(os.path.join(full_d, '*.md'))
        if not md_files:
            continue
        md_file = md_files[0]
        with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # parse title
        t_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
        title = t_match.group(1).strip('"\'') if t_match else d
        
        # parse draft
        d_match = re.search(r'^draft:\s*(true|false)', content, re.MULTILINE)
        draft = d_match.group(1) if d_match else 'false'
        
        # parse category (singular)
        cat_sing = re.search(r'^category:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
        category_singular = cat_sing.group(1).strip('"\'') if cat_sing else None
        
        # parse categories (plural)
        cat_plur = re.search(r'^categories:\s*\[(.*?)\]', content, re.MULTILINE)
        categories_plural = [c.strip().strip('"\'') for c in cat_plur.group(1).split(',')] if cat_plur else None
        
        posts.append({
            'dir': d,
            'file': md_file,
            'title': title,
            'draft': draft,
            'category_singular': category_singular,
            'categories_plural': categories_plural
        })
    return posts

es_posts = audit('es')
en_posts = audit('en')

print(f"ES total: {len(es_posts)}")
print(f"EN total: {len(en_posts)}")

drafts_es = [p for p in es_posts if p['draft'] == 'true']
print(f"ES drafts count: {len(drafts_es)}")
for p in drafts_es:
    print(f"  [DRAFT ES] {p['dir']} - {p['title']}")

drafts_en = [p for p in en_posts if p['draft'] == 'true']
print(f"EN drafts count: {len(drafts_en)}")
for p in drafts_en:
    print(f"  [DRAFT EN] {p['dir']} - {p['title']}")

# Save full audit
with open('scratch/full_audit.json', 'w', encoding='utf-8') as f:
    json.dump({'es': es_posts, 'en': en_posts}, f, ensure_ascii=False, indent=2)
