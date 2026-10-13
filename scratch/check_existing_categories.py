import glob, re

for lang in ['es', 'en']:
    files = glob.glob(f'content/{lang}/posts/*/*.md')
    has_cats = 0
    all_cats = set()
    no_cat_files = []
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
        m = re.search(r'^categories:\s*\[(.*?)\]', c, re.MULTILINE)
        if m:
            has_cats += 1
            for cat in m.group(1).split(','):
                cat_clean = cat.strip().strip('"\'')
                if cat_clean:
                    all_cats.add(cat_clean)
        else:
            no_cat_files.append(f)
    print(f"=== {lang.upper()} ===")
    print(f"Total posts: {len(files)}")
    print(f"Posts with categories: {has_cats}")
    print(f"Posts WITHOUT categories: {len(no_cat_files)}")
    print(f"Unique categories found ({len(all_cats)}): {sorted(list(all_cats))[:15]}")
    if no_cat_files[:5]:
        print(f"Samples without categories: {no_cat_files[:5]}")
