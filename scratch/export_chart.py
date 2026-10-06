import win32com.client as win32
import os

excel = win32.Dispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False

file_path = os.path.abspath('packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[ES]_Business_Case_VAN_TIR/Business_Case_VAN_TIR_Datalaria_ES.xlsx')
wb = excel.Workbooks.Open(file_path)
excel.CalculateFullRebuild()

ws_sens = wb.Sheets('Sensibilidad & Tornado')
print("Charts in Sensibilidad & Tornado:", ws_sens.ChartObjects().Count)
if ws_sens.ChartObjects().Count > 0:
    ch = ws_sens.ChartObjects(1)
    img_path = os.path.abspath('scratch/tornado_current.png')
    ch.Chart.Export(img_path)
    print("Exported chart to:", img_path)

wb.Close(False)
excel.Quit()
