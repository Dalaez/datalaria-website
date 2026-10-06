import sys
sys.path.append('scripts/executive_pack_pert')
from generate_excel import build_wbs_data

tasks = build_wbs_data('ES')
total_all = 0
crit_mu = 0
crit_var = 0
crit_count = 0
for t in tasks:
    code, phase, name, crit, o, m, p = t
    mu = (o + 4*m + p) / 6.0
    var = ((p - o) / 6.0) ** 2
    total_all += mu
    if crit == 'SÍ':
        crit_count += 1
        crit_mu += mu
        crit_var += var
        print(f"CRIT {code:4} o={o:4.1f} m={m:4.1f} p={p:4.1f} -> mu={mu:4.1f} var={var:5.2f} | {name}")

print(f"\nTotal critical tasks: {crit_count}")
print(f"Total expected critical duration: {crit_mu:.1f}")
print(f"Total critical variance: {crit_var:.2f}")
print(f"Total critical std dev: {crit_var**0.5:.2f}")
