import yaml
import glob
import re

# 1. Check data/apps/pulse.yaml
with open("data/apps/pulse.yaml", "r", encoding="utf-8") as f:
    pulse_app = yaml.safe_load(f)
assert pulse_app["status"] == "incubating", f"FAIL: Expected incubating, got {pulse_app['status']}"
print("[PASS] pulse.yaml status is incubating")

# 2. Check draft: true in apps/pulse/index.md
for lang in ["es", "en"]:
    with open(f"content/{lang}/apps/pulse/index.md", "r", encoding="utf-8") as f:
        c = f.read()
    assert "draft: true" in c, f"FAIL: draft: true missing in {lang}/apps/pulse"
    print(f"[PASS] {lang}/apps/pulse/index.md has draft: true")

# 3. Check Post 5 taxonomy
with open("content/es/posts/pulse-parte5-kit-excel-migracion-notion-equipos/index.md", "r", encoding="utf-8") as f:
    es5 = f.read()
assert 'category: "IA, Ingeniería y Proyectos"' in es5, "FAIL: ES Post 5 category incorrect"
print("[PASS] ES Post 5 taxonomy correct")

with open("content/en/posts/pulse-part5-excel-kit-notion-migration-teams/index.md", "r", encoding="utf-8") as f:
    en5 = f.read()
assert 'category: "AI, Engineering & Projects"' in en5, "FAIL: EN Post 5 category incorrect"
print("[PASS] EN Post 5 taxonomy correct")

# 4. Check prices in Post 5
for txt, name in [(es5, "ES"), (en5, "EN")]:
    assert "19 €" in txt, f"FAIL: 19 € missing in {name} Post 5"
    assert "29 €" not in txt and "29€" not in txt, f"FAIL: 29€ found in {name} Post 5"
    assert "49 €" not in txt and "49€" not in txt, f"FAIL: 49€ found in {name} Post 5"
    assert "USD" not in txt and "$" not in txt, f"FAIL: USD or $ found in {name} Post 5"
    print(f"[PASS] {name} Post 5 prices unified in 19 € (zero USD/29€/49€)")

# 5. Check app-ref in all 10 posts
for p in sorted(glob.glob("content/**/pulse-*/index.md", recursive=True)):
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    assert '{{< app-ref slug="pulse" >}}' in c, f"FAIL: app-ref missing in {p}"
    assert "cover:" in c and "alt:" in c and "caption:" in c, f"FAIL: cover block missing in {p}"
print("[PASS] All 10 pulse posts have {{< app-ref slug=\"pulse\" >}} and structured cover block")

# 6. Check Post 3 ASCII tables
for lang in ["es", "en"]:
    slug = "pulse-parte3-tablero-react-tabla-kanban-calendario" if lang == "es" else "pulse-part3-react-dashboard-table-kanban-calendar"
    with open(f"content/{lang}/posts/{slug}/index.md", "r", encoding="utf-8") as f:
        c = f.read()
    assert "┌" not in c and "└" not in c, f"FAIL: ASCII table found in {lang} Post 3"
print("[PASS] Post 3 has clean Markdown tables (zero ASCII art)")

# 7. Check Helix bridge and contact in Post 5
for txt, name in [(es5, "ES"), (en5, "EN")]:
    assert "Datalaria Helix" in txt, f"FAIL: Helix bridge missing in {name} Post 5"
    assert "contacto@datalaria.com" in txt, f"FAIL: contact email missing in {name} Post 5"
    assert "/recursos/#software" in txt or "/resources/#software" in txt, f"FAIL: Helix waitlist link missing in {name} Post 5"
    assert "/recursos/#pack-pulse" in txt or "/resources/#pack-pulse" in txt, f"FAIL: pack-pulse CTA missing in {name} Post 5"
print("[PASS] Post 5 has Helix bridge, B2B contact CTA, and pack-pulse CTA")

# 8. Check canonical kit filenames in Post 5
for txt, name in [(es5, "ES"), (en5, "EN")]:
    assert "Pulse_Content_Ops_Template.xlsx" in txt, f"FAIL: template name in {name}"
    assert "migrate_notion.py" in txt, f"FAIL: migrator name in {name}"
    assert "notion_power_query.m" in txt, f"FAIL: connector name in {name}"
    assert "pulse_repo_scanner.py" in txt, f"FAIL: scanner name in {name}"
    assert "GUIA_PULSE_KIT.md" in txt, f"FAIL: guide name in {name}"
print("[PASS] Post 5 has canonical kit filenames")

print("\n>>> ALL VERIFICATION CHECKS PASSED PERFECTLY! <<<")
