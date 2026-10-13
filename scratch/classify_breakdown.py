import json

with open('scratch/full_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

es_posts = data['es']

# Biografias (11)
bio_slugs = {
    'abraham_wald', 'ada_lovelace', 'alan_turing', 'claude_shannon',
    'deming', 'florence-nightingale', 'john-snow', 'john_von_neumann',
    'kantorovich', 'oppenheimer', 'thomas_bayes'
}

# Startups (12)
startup_slugs = {
    'carto', 'clarity_ai', 'devo', 'flywire', 'freepik', 'graphext',
    'happyrobot', 'multiverse_computing', 'netflix', 'nextail',
    'submer', 'wallapop'
}

# Proyectos (36)
project_slugs = {
    # LifeOps (5)
    'app-lifeops_part1_arquitectura_backend', 'app-lifeops_part2_frontend_dashboard',
    'app-lifeops_part3_modulos_kanban', 'app-lifeops_part4_informes_word_excel',
    'app-lifeops_part5_deploy_mobile_pwa',
    # Autopilot (9)
    'ia_agents_part1', 'ia_agents_part2', 'ia_agents_part3', 'ia_agents_part4',
    'ia_agents_part5', 'ia_agents_part6', 'ia_agents_part7', 'ia_agents_part8',
    'ia_agents_part9',
    # Obsolescence Radar (7)
    'obs_parte1_intro', 'obs_parte2_tactica', 'obs_parte3_arquitectura',
    'obs_parte4_ingesta', 'obs_parte5_radar', 'obs_parte6_fastapi',
    'obs_parte7_dashboard',
    # Weather Service (4)
    'app-openweather_part1_backend', 'app_openweather_part2_frontend',
    'app_openweather_part3_ai_prediction', 'app_openweather_part4_extras_ux',
    # S&OP Engineering (5)
    'sop_ingenieria-higiene-datos', 'sop-ingenieria-parte2-prediccion',
    'sop-ingenieria-parte3-optimizacion', 'sop-ingenieria-parte4-enterprise',
    'sop-ingenieria-parte5-agentes_autonomos',
    # Project Operations Engineering (2)
    'proj_ops_parte1_intro', 'proj_ops_parte2_agentic_pmo',
    # Interactive Apps & Meta (4)
    'game_snake', 'app_flashcards', 'app_conversor_unidades', 'datalaria-blog'
}

# The remaining are Artículos Técnicos (45)
categorized = {
    'biografias': [],
    'startups': [],
    'proyectos': [],
    'tecnicos': []
}

for p in es_posts:
    s = p['dir']
    if s in bio_slugs:
        categorized['biografias'].append(p)
    elif s in startup_slugs:
        categorized['startups'].append(p)
    elif s in project_slugs:
        categorized['proyectos'].append(p)
    else:
        categorized['tecnicos'].append(p)

print(f"Biografías: {len(categorized['biografias'])}")
print(f"Startups: {len(categorized['startups'])}")
print(f"Proyectos Tecnológicos: {len(categorized['proyectos'])}")
print(f"Artículos Técnicos: {len(categorized['tecnicos'])}")
print(f"Total: {sum(len(v) for v in categorized.values())}")

# Let's inspect all 45 Artículos Técnicos
print("\n--- ARTÍCULOS TÉCNICOS (45) ---")
for p in categorized['tecnicos']:
    print(f"  - {p['dir']} ({p['title'][:50]}) [Draft: {p['draft']}]")

with open('scratch/classified_104_posts.json', 'w', encoding='utf-8') as f:
    json.dump(categorized, f, ensure_ascii=False, indent=2)
