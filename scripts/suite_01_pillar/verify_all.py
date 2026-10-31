import sys

# 1. Check pillar posts
for path in ['content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/index.md', 'content/en/posts/corporate-strategy-mba-quantitative-framework/index.md']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    assert 'product-card' in c, f"Missing product-card in {path}"
    assert 'preview-pack.png' in c, f"Missing preview-pack.png in {path}"
    assert '### 🌐 ' in c or '### 🌐 Tool 1' in c, f"Missing formatted H3 tool headers in {path}"
    assert 'flowchart TD' in c, f"Missing flowchart TD in {path}"
    assert chr(96)*3 not in c, f"Found unexpected code blocks (```) in {path}"
    print(f"Pillar post OK: {path}")

# 2. Check catalog
with open('layouts/partials/recursos_catalog.html', 'r', encoding='utf-8') as f:
    cat = f.read()
assert "openModal('suite-01')" in cat, "Missing openModal('suite-01')"
assert '/es/posts/estrategia-corporativa-mba-framework-cuantitativo/' in cat, "Missing ES pillar URL in catalog"
assert '/en/posts/corporate-strategy-mba-quantitative-framework/' in cat, "Missing EN pillar URL in catalog"
assert 'suite-01-preview-es.png' in cat, "Missing ES preview img in catalog"
assert 'suite-01-preview-en.png' in cat, "Missing EN preview img in catalog"
print("Recursos catalog HTML OK!")

# 3. Check kits.yaml
with open('data/pulse/kits.yaml', 'r', encoding='utf-8') as f:
    y = f.read()
assert '/es/posts/estrategia-corporativa-mba-framework-cuantitativo/' in y, "Missing ES pillar in kits.yaml"
assert '/en/posts/corporate-strategy-mba-quantitative-framework/' in y, "Missing EN pillar in kits.yaml"
print("kits.yaml OK!")

# 4. Check index_profile.html
with open('layouts/partials/index_profile.html', 'r', encoding='utf-8') as f:
    idx_p = f.read()
assert 'suite-01' in idx_p, "Missing suite-01 in index_profile.html"
assert 'estrategia-corporativa-mba-framework-cuantitativo' in idx_p, "Missing ES pillar in index_profile.html"
assert 'corporate-strategy-mba-quantitative-framework' in idx_p, "Missing EN pillar in index_profile.html"
assert 'dlh-res-links-row' in idx_p, "Missing dlh-res-links-row in index_profile.html"
print("index_profile.html OK!")

print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
