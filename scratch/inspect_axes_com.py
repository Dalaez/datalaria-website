import win32com.client as win32
import os

excel = win32.Dispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False
wb_excel = excel.Workbooks.Open(os.path.abspath("scratch/test_tornado_chart_v2.xlsx"))
ws_excel = wb_excel.Sheets(1)
ch = ws_excel.ChartObjects(1).Chart

# In Excel VBA:
# xlCategory = 1, xlValue = 2
# xlPrimary = 1, xlSecondary = 2
ax_cat = ch.Axes(1, 1) # xlCategory, xlPrimary
ax_val = ch.Axes(2, 1) # xlValue, xlPrimary

print("Category Axis:")
print("  HasTitle:", ax_cat.HasTitle)
print("  TickLabelPosition:", ax_cat.TickLabelPosition) # xlTickLabelPositionLow = -4134, High = -4127, NextToAxis = 4, None = -4142
print("  HasMajorGridlines:", ax_cat.HasMajorGridlines)
print("  Visible:", ax_cat.Format.Line.Visible)

print("\nValue Axis:")
print("  HasTitle:", ax_val.HasTitle)
print("  TickLabelPosition:", ax_val.TickLabelPosition)
print("  HasMajorGridlines:", ax_val.HasMajorGridlines)

wb_excel.Close(False)
excel.Quit()
