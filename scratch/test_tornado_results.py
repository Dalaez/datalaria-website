import sys
sys.path.append('scripts/executive_pack_business_case')
import model_core

print("Base NPV:", f"{model_core.PROJ_BASE['npv_5y']:,.2f}")
print("\nTORNADO_RESULTS from model_core:")
for r in model_core.TORNADO_RESULTS:
    print(f"Rank {r['rank']}: {r['name_es']} (id={r['id']}) | Low={r['low_val']} -> NPV={r['npv_at_low']:,.0f} (delta={r['delta_pessimistic']:,.0f}) | High={r['high_val']} -> NPV={r['npv_at_high']:,.0f} (delta={r['delta_optimistic']:,.0f}) | Swing={r['swing']:,.0f}")
