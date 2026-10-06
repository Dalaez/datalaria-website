import openpyxl

wb = openpyxl.load_workbook('packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[ES]_Business_Case_VAN_TIR/Business_Case_VAN_TIR_Datalaria_ES.xlsx')
ws = wb['Sensibilidad & Tornado']
ch = ws._charts[0]
print("Chart type:", ch.type)
print("Grouping:", ch.grouping)
print("Overlap:", ch.overlap)
print("Number of series:", len(ch.series))
for i, s in enumerate(ch.series):
    print(f"Series {i}: title={s.title}, val={s.val}, cat={s.cat}")
    print(f"  solidFill: {getattr(s.graphicalProperties, 'solidFill', None)}")
