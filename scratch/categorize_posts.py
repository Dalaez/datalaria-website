import json

with open('scratch/posts_summary.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Defined sets based on directory names
biografias_slugs = {
    'alan_turing', 'ada_lovelace', 'claude_shannon', 'thomas_bayes',
    'deming', 'kantorovich', 'abraham_wald', 'florence-nightingale',
    'john-snow', 'john_von_neumann', 'oppenheimer'
}

startups_slugs = {
    'submer', 'happyrobot', 'wallapop', 'flywire', 'devo', 'clarity_ai',
    'nextail', 'multiverse_computing', 'graphext', 'carto', 'freepik', 'netflix'
}

proyectos_slugs = {
    'app-lifeops_part1_arquitectura_backend', 'app-lifeops_part2_frontend_dashboard',
    'app-lifeops_part3_modulos_kanban', 'app-lifeops_part4_informes_word_excel',
    'app-lifeops_part5_deploy_mobile_pwa',
    'ia_agents_part1', 'ia_agents_part2', 'ia_agents_part3', 'ia_agents_part4',
    'ia_agents_part5', 'ia_agents_part6', 'ia_agents_part7', 'ia_agents_part8',
    'ia_agents_part9',
    'obs_parte1_intro', 'obs_parte2_tactica', 'obs_parte3_arquitectura',
    'obs_parte4_ingesta', 'obs_parte5_radar', 'obs_parte6_fastapi',
    'obs_parte7_dashboard',
    'app-openweather_part1_backend', 'app_openweather_part2_frontend',
    'app_openweather_part3_ai_prediction', 'app_openweather_part4_extras_ux',
    'sop_ingenieria-higiene-datos', 'sop-ingenieria-parte2-prediccion',
    'sop-ingenieria-parte3-optimizacion', 'sop-ingenieria-parte4-enterprise',
    'sop-ingenieria-parte5-agentes_autonomos',
    'game_snake', 'app_flashcards', 'app_conversor_unidades',
    'datalaria-blog'
}

# The rest fall under "Artículos Técnicos & Gestión Estratégica"
# Let's categorize and print counts
cat_bio = []
cat_startups = []
cat_proyectos = []
cat_tecnicos = []

for p in posts:
    s = p['dir']
    if s in biografias_slugs:
        cat_bio.append(p)
    elif s in startups_slugs:
        cat_startups.append(p)
    elif s in proyectos_slugs:
        cat_proyectos.append(p)
    else:
        cat_tecnicos.append(p)

print(f"Biografías: {len(cat_bio)}")
print(f"Startups: {len(cat_startups)}")
print(f"Proyectos Tecnológicos: {len(cat_proyectos)}")
print(f"Artículos Técnicos: {len(cat_tecnicos)}")
print(f"Total: {len(cat_bio) + len(cat_startups) + len(cat_proyectos) + len(cat_tecnicos)}")

# Save categorized to json
categorized = {
    'biografias': cat_bio,
    'startups': cat_startups,
    'proyectos': cat_proyectos,
    'tecnicos': cat_tecnicos
}

with open('scratch/categorized_posts.json', 'w', encoding='utf-8') as f:
    json.dump(categorized, f, ensure_ascii=False, indent=2)

print("\n--- ARTÍCULOS TÉCNICOS SLUGS ---")
for p in cat_tecnicos:
    print(f"- {p['dir']} ({p['title']})")
