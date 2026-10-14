import glob, os, re

scripts = glob.glob('scripts/**/generate_cover.py', recursive=True)
scripts.extend(glob.glob('scripts/*mega*.py'))

for s in sorted(scripts):
    with open(s, encoding='utf-8') as f:
        lines = f.readlines()
    tool = os.path.basename(os.path.dirname(s)) or os.path.basename(s)
    # Search lines around draw.text
    for i, line in enumerate(lines):
        if 'draw.text(' in line and ('MATRIX' in line or 'PACK' in line or 'SUITE' in line or 'CASE' in line or 'BUNDLE' in line or 'title' in line.lower()):
            print(f"{tool:28}: line {i+1}: {line.strip()}")
