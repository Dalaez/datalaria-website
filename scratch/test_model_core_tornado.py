import sys
sys.path.append('scripts/executive_pack_business_case')
import model_core

res = model_core.calculate_model()
print("Base NPV:", f"{res['dcf']['npv_5y']:,.2f}")
print("\nTornado analysis from model_core:")
for d in res['tornado']:
    print(f"{d['driver']}: Low={d['val_low']} -> NPV={d['npv_low']:,.0f}, High={d['val_high']} -> NPV={d['npv_high']:,.0f}, Swing={d['swing']:,.0f}")
