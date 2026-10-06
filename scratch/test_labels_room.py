import win32com.client as win32
import os

excel = win32.Dispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False
wb_excel = excel.Workbooks.Open(os.path.abspath("scratch/test_tornado_chart_v2.xlsx"))
ws_excel = wb_excel.Worksheets("TornadoTest")
ch = ws_excel.ChartObjects(1).Chart

# Check TickLabels count and text
ax_cat = ch.Axes(1, 1)
print("TickLabels count:", ax_cat.TickLabels.Count)
for i in range(1, ax_cat.TickLabels.Count + 1):
    print(f"  Label {i}: '{ax_cat.TickLabels(i).Text}'")

# Check PlotArea size
pa = ch.PlotArea
print(f"PlotArea: Left={pa.Left}, Top={pa.Top}, Width={pa.Width}, Height={pa.Height}")
print(f"ChartArea: Width={ch.ChartArea.Width}, Height={ch.ChartArea.Height}")

# Let's adjust PlotArea.Left and PlotArea.Width to give room for labels
pa.Left = 140
pa.Width = ch.ChartArea.Width - 160
ch.Export(os.path.abspath("scratch/test_tornado_with_room.png"))
print("Exported with room to test_tornado_with_room.png")

wb_excel.Close(False)
excel.Quit()
