import json

with open('scratch/full_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

es_posts = data['es']
en_posts = data['en']

# Slugs mapping for Biografías
bio_slugs = {
    'abraham_wald', 'ada_lovelace', 'alan_turing', 'claude_shannon',
    'deming', 'florence-nightingale', 'john-snow', 'john_von_neumann',
    'kantorovich', 'oppenheimer', 'thomas_bayes',
    # English equivalents if any
    'florence_nightingale', 'john_snow'
}

# Slugs mapping for Startups
startup_slugs = {
    'carto', 'clarity_ai', 'devo', 'flywire', 'freepik', 'graphext',
    'happyrobot', 'multiverse_computing', 'netflix', 'nextail',
    'submer', 'wallapop'
}

# Slugs mapping for Proyectos Tecnológicos
project_slugs_prefixes = [
    'app-lifeops', 'app_lifeops', 'app-openweather', 'app_openweather',
    'ia_agents', 'ai_agents', 'obs_parte', 'obs_part',
    'sop-ingenieria', 'sop_engineering', 'sop_ingenieria',
    'proj_ops',
    'game_snake', 'app_flashcards', 'app_conversor_unidades',
    'app_unit_converter', 'datalaria-blog', 'datalaria_blog'
]

def classify_slug(slug):
    s = slug.lower()
    if s in bio_slugs:
        return 'biografias'
    if s in startup_slugs:
        return 'startups'
    for prefix in project_slugs_prefixes:
        if s.startswith(prefix):
            return 'proyectos'
    return 'tecnicos'

results_es = {}
for p in es_posts:
    cat = classify_slug(p['dir'])
    results_es.setdefault(cat, []).append(p['dir'])

results_en = {}
for p in en_posts:
    cat = classify_slug(p['dir'])
    results_en.setdefault(cat, []).append(p['dir'])

print("=== ES CLASSIFICATION ===")
for cat, slugs in results_es.items():
    print(f"{cat}: {len(slugs)} posts")

print("\n=== EN CLASSIFICATION ===")
for cat, slugs in results_en.items():
    print(f"{cat}: {len(slugs)} posts")

# Let's check any differences between ES and EN
print("\nES tecnicos count:", len(results_es.get('tecnicos', [])))
print("EN tecnicos count:", len(results_en.get('tecnicos', [])))
