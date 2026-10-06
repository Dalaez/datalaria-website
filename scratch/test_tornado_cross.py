import openpyxl
from openpyxl.chart import BarChart, Reference
import os
import subprocess

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "TornadoTest"

ws.append(["Rank", "Driver", "Swing", "Impacto Negativo (Rojo)", "Impacto Positivo (Verde)"])
drivers = [
    (1, "Precio Unitario (€/u)", 957499, -478749, 478749),
    (2, "Volumen Año 1 (u)", 897655, -448827, 448827),
    (3, "Coste Variable (%)", 819448, -409724, 409724),
    (4, "OPEX Fijo Anual (€)", 418120, -209060, 209060),
    (5, "Crecimiento Volumen (%)", 312203, -152011, 160192),
    (6, "CAPEX Total (€)", 286570, -143285, 143285),
    (7, "Tasa Descuento (WACC)", 209781, -100176, 109605),
    (8, "Capital Circulante (%)", 171364, -85682, 85682),
]

for d in drivers:
    ws.append(list(d))

chart = BarChart()
chart.type = "bar"
chart.grouping = "clustered"
chart.overlap = 100
chart.title = "ANÁLISIS DE SENSIBILIDAD TORNADO: IMPACTO EN VAN (€)"
chart.width = 20
chart.height = 12

chart.x_axis.scaling.orientation = "maxMin"
chart.x_axis.crosses = "min"
chart.x_axis.tickLblPos = "nextTo"

chart.y_axis.scaling.orientation = "minMax"
chart.legend.position = "b"

data = Reference(ws, min_col=4, min_row=1, max_col=5, max_row=9)
cats = Reference(ws, min_col=2, min_row=2, max_row=9)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

for s in chart.series:
    s.invertIfNegative = False

chart.series[0].graphicalProperties.solidFill = "EF4444"
chart.series[1].graphicalProperties.solidFill = "10B981"

ws.add_chart(chart, "G2")

test_path = os.path.abspath("scratch/test_tornado_cross_min.xlsx")
wb.save(test_path)
print("Saved:", test_path)
