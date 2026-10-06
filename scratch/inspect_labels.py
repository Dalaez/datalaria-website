import win32com.client as win32
import os

excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False
wb = excel.Workbooks.Open(os.path.abspath("scratch/test_tornado_chart_v2.xlsx"))
ws = wb.Worksheets("TornadoTest")
ch = ws.ChartObjects(1).Chart

ax_cat = ch.Axes(1, 1)
print("TickLabels count:", ax_cat.TickLabels.Count)
for i in range(1, ax_cat.TickLabels.Count + 1):
    print(f"  Label {i}: '{ax_cat.TickLabels(i).Text}'")

pa = ch.PlotArea
print(f"PlotArea: Left={pa.Left}, Top={pa.Top}, Width={pa.Width}, Height={pa.Height}")
print(f"ChartArea: Width={ch.ChartArea.Width}, Height={ch.ChartArea.Height}")

wb.Close(False)
excel.Quit()
