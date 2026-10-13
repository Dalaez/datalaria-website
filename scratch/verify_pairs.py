import os, glob, re, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from apply_category_frontmatter import determine_category_key

# Check all EN posts vs ES posts
en_dirs = [d for d in os.listdir('content/en/posts') if os.path.isdir(f'content/en/posts/{d}')]
es_dirs = [d for d in os.listdir('content/es/posts') if os.path.isdir(f'content/es/posts/{d}')]

print(f"Total ES dirs: {len(es_dirs)}, Total EN dirs: {len(en_dirs)}")

# Check category counts
cat_keys_es = {}
for d in es_dirs:
    k = determine_category_key(d)
    cat_keys_es[k] = cat_keys_es.get(k, 0) + 1

cat_keys_en = {}
for d in en_dirs:
    k = determine_category_key(d)
    cat_keys_en[k] = cat_keys_en.get(k, 0) + 1

print("ES breakdown by key:", cat_keys_es)
print("EN breakdown by key:", cat_keys_en)

assert cat_keys_es == cat_keys_en, "Discrepancy found between ES and EN categories!"
print("🎉 100% Perfect 1-to-1 Match between ES and EN!")
