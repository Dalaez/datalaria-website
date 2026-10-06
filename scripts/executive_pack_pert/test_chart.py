import openpyxl
from openpyxl.chart import AreaChart, LineChart, ScatterChart, Reference, Series

wb = openpyxl.load_workbook('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[ES]_Estimacion_PERT_3_Puntos/Estimacion_PERT_Estocastica_ES.xlsx')
ws = wb['Dashboard Ejecutivo']

print("Charts in Dashboard:", len(ws._charts))
if ws._charts:
    ch = ws._charts[0]
    print("Chart type:", type(ch))
    print("X-axis:", ch.x_axis)
    print("X-axis title:", ch.x_axis.title)
    print("X-axis tickLblPos:", ch.x_axis.tickLblPos)
    print("X-axis number_format:", ch.x_axis.number_format)
    print("Y-axis:", ch.y_axis)
