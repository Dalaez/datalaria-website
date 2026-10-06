import openpyxl
from openpyxl.chart import AreaChart, Reference
from openpyxl.chart.data_source import NumRef, NumData, NumVal, StrRef, StrData, StrVal, AxDataSource, NumDataSource
from openpyxl.chart.axis import ChartLines

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Dashboard'
ws.append(['Días', 'Densidad'])

x_vals = ['157.0', '160.0', '162.9', '165.9', '168.8', '171.8', '174.8', '177.7', '180.7', '183.6', '186.6', '189.5', '192.5', '195.5', '198.4', '201.4', '204.3', '207.3', '210.2', '213.2', '216.2', '219.1', '222.1', '225.0', '228.0']
y_vals = [0.0001, 0.0002, 0.0006, 0.0013, 0.0026, 0.0049, 0.0086, 0.0136, 0.0200, 0.0268, 0.0332, 0.0377, 0.0393, 0.0377, 0.0332, 0.0268, 0.0200, 0.0136, 0.0086, 0.0049, 0.0026, 0.0013, 0.0006, 0.0002, 0.0001]

for x, y in zip(x_vals, y_vals):
    ws.append([x, y])

chart = AreaChart()
chart.title = 'Distribución de Probabilidad'
chart.style = 10
chart.width = 19
chart.height = 11.5

data_ref = Reference(ws, min_col=2, min_row=1, max_row=26)
chart.add_data(data_ref, titles_from_data=True)

# Build explicit StrRef and NumRef caches
sdata = StrData(ptCount=len(x_vals), pt=[StrVal(idx=i, v=v) for i, v in enumerate(x_vals)])
sref = StrRef(f="'Dashboard'!$A$2:$A$26", strCache=sdata)

ndata = NumData(ptCount=len(y_vals), pt=[NumVal(idx=i, v=str(v)) for i, v in enumerate(y_vals)])
nref = NumRef(f="'Dashboard'!$B$2:$B$26", numCache=ndata)

for s in chart.series:
    s.cat = AxDataSource(strRef=sref)
    s.val = NumDataSource(numRef=nref)
    s.graphicalProperties.solidFill = '2563EB'

chart.x_axis.title = 'Duración del Proyecto (Días Hábiles)'
chart.x_axis.axPos = 'b'
chart.x_axis.tickLblPos = 'nextTo'
chart.x_axis.delete = False
chart.x_axis.majorTickMark = 'out'
chart.x_axis.majorGridlines = ChartLines()
chart.x_axis.tickLblSkip = 3

chart.y_axis.title = 'Densidad de Probabilidad f(x)'
chart.y_axis.axPos = 'l'
chart.y_axis.tickLblPos = 'nextTo'
chart.y_axis.delete = False
chart.y_axis.majorTickMark = 'out'
chart.y_axis.majorGridlines = ChartLines()
chart.y_axis.number_format = '0.000'

chart.legend = None

ws.add_chart(chart, 'D2')
wb.save('scratch/test_axis_labels.xlsx')

import zipfile
z = zipfile.ZipFile('scratch/test_axis_labels.xlsx')
print(z.read('xl/charts/chart1.xml').decode('utf-8'))
