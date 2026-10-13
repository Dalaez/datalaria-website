import json

with open('scratch/full_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

es_dirs = set(p['dir'] for p in data['es'])
en_dirs = set(p['dir'] for p in data['en'])

print("Directories only in ES:", len(es_dirs - en_dirs))
for d in sorted(es_dirs - en_dirs):
    print("  ES only:", d)

print("\nDirectories only in EN:", len(en_dirs - es_dirs))
for d in sorted(en_dirs - es_dirs):
    print("  EN only:", d)
