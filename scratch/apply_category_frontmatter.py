import os, glob, re, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Category names
CATEGORIES_ES = {
    'biografias': 'Biografías',
    'startups': 'Startups',
    'proyectos': 'Proyectos Tecnológicos',
    'tecnicos': 'Artículos Técnicos'
}

CATEGORIES_EN = {
    'biografias': 'Biographies',
    'startups': 'Startups',
    'proyectos': 'Tech Projects',
    'tecnicos': 'Technical Articles'
}

# Slugs mapping for Biografías
bio_slugs = {
    'abraham_wald', 'ada_lovelace', 'alan_turing', 'claude_shannon',
    'deming', 'florence-nightingale', 'florence_nightingale',
    'john-snow', 'john_snow', 'john_von_neumann',
    'kantorovich', 'oppenheimer', 'thomas_bayes'
}

# Slugs mapping for Startups
startup_slugs = {
    'carto', 'clarity_ai', 'devo', 'flywire', 'freepik', 'graphext',
    'happyrobot', 'multiverse_computing', 'netflix', 'nextail',
    'submer', 'wallapop'
}

# Slugs prefixes / exact names for Proyectos
project_exact_or_prefixes = [
    'app-lifeops', 'app_lifeops',
    'ia_agents', 'ai_agents',
    'obs_parte', 'obs_part',
    'app-openweather', 'app_openweather',
    'sop_ingenieria', 'sop-ingenieria', 'sop_engineering', 'sop-engineering',
    'proj_ops',
    'game_snake', 'app_flashcards', 'app_conversor_unidades', 'app_unit_converter',
    'datalaria-blog', 'datalaria_blog'
]

def determine_category_key(slug):
    s = slug.lower()
    if s in bio_slugs:
        return 'biografias'
    if s in startup_slugs:
        return 'startups'
    for prefix in project_exact_or_prefixes:
        if s.startswith(prefix) or s == prefix:
            return 'proyectos'
    return 'tecnicos'

def update_file(file_path, cat_value, dry_run=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Frontmatter regex
    fm_match = re.match(r'^(---\s*\n)(.*?\n)(---\s*\n)(.*)$', content, re.DOTALL)
    if not fm_match:
        print(f"⚠️ Could not parse frontmatter in: {file_path}")
        return False

    prefix_dashes, fm_body, suffix_dashes, body = fm_match.groups()

    # Check if category: already present
    cat_match = re.search(r'^category:\s*.*$', fm_body, re.MULTILINE)
    new_cat_line = f'category: "{cat_value}"'

    if cat_match:
        new_fm_body = re.sub(r'^category:\s*.*$', new_cat_line, fm_body, flags=re.MULTILINE)
    else:
        # Insert after draft: if present, else after date: or title:
        draft_match = re.search(r'^(draft:\s*(?:true|false)\s*\n)', fm_body, re.MULTILINE)
        if draft_match:
            new_fm_body = fm_body[:draft_match.end()] + f'{new_cat_line}\n' + fm_body[draft_match.end():]
        else:
            date_match = re.search(r'^(date:\s*.*?\n)', fm_body, re.MULTILINE)
            if date_match:
                new_fm_body = fm_body[:date_match.end()] + f'{new_cat_line}\n' + fm_body[date_match.end():]
            else:
                # Top of frontmatter
                new_fm_body = f'{new_cat_line}\n' + fm_body

    new_content = prefix_dashes + new_fm_body + suffix_dashes + body

    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return True

def process_language(lang, dry_run=True):
    base_dir = f'content/{lang}/posts'
    cat_map = CATEGORIES_ES if lang == 'es' else CATEGORIES_EN
    count = 0
    breakdown = {}
    
    for d in sorted(os.listdir(base_dir)):
        dir_path = os.path.join(base_dir, d)
        if not os.path.isdir(dir_path):
            continue
        md_files = glob.glob(os.path.join(dir_path, '*.md'))
        if not md_files:
            continue
        md_file = md_files[0]
        cat_key = determine_category_key(d)
        cat_val = cat_map[cat_key]
        breakdown[cat_val] = breakdown.get(cat_val, 0) + 1
        
        ok = update_file(md_file, cat_val, dry_run=dry_run)
        if ok:
            count += 1

    print(f"\nLanguage: {lang.upper()} (Dry run: {dry_run})")
    print(f"Total processed files: {count}")
    for k, v in breakdown.items():
        print(f"  - {k}: {v} posts")
    return count

if __name__ == '__main__':
    import sys
    dry_run = '--execute' not in sys.argv
    if dry_run:
        print("🔍 RUNNING IN DRY-RUN MODE (No files will be modified)")
    else:
        print("🚀 EXECUTING CHANGES (Modifying frontmatter in content/es and content/en)")
        
    es_count = process_language('es', dry_run=dry_run)
    en_count = process_language('en', dry_run=dry_run)
    
    if dry_run:
        print("\nDry-run completed successfully! Run with --execute to apply changes.")
    else:
        print(f"\n✅ Completed: {es_count} ES posts and {en_count} EN posts updated!")
