import sys
sys.path.append('scripts/executive_pack_business_case')
import generate_excel

# Run workbook generation
generate_excel.main()

# Now export the chart with Excel COM
import win32com.client as win32
import os

excel = win32.Dispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False

file_path = os.path.abspath('packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[ES]_Business_Case_VAN_TIR/Business_Case_VAN_TIR_Datalaria_ES.xlsx')
wb = excel.Workbooks.Open(file_path)
excel.CalculateFullRebuild()

ws_sens = wb.Sheets('Sensibilidad & Tornado')
print("=== Tabla 2 (Filas 27 a 34) ===")
for r in range(27, 35):
    print(f"Fila {r}: Driver={ws_sens.Cells(r, 2).Text}, Swing={ws_sens.Cells(r, 9).Text}, RankFormula={ws_sens.Cells(r, 10).Value}")

print("\n=== Tabla 3 (Filas 38 a 45) ===")
for r in range(38, 46):
    print(f"Fila {r}: Rank={ws_sens.Cells(r, 2).Text}, Driver={ws_sens.Cells(r, 3).Text}, Swing={ws_sens.Cells(r, 4).Text}, MinDelta={ws_sens.Cells(r, 5).Text}, MaxDelta={ws_sens.Cells(r, 6).Text}")

if ws_sens.ChartObjects().Count > 0:
    ch = ws_sens.ChartObjects(1)
    img_path = os.path.abspath('scratch/tornado_after_calc_fix.png')
    ch.Chart.Export(img_path)
    print("\nExported chart to:", img_path)

wb.Close(False)
excel.Quit()
