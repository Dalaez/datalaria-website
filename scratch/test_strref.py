from openpyxl.chart.data_source import AxDataSource, StrRef
import openpyxl
from openpyxl.chart import BarChart, Reference

wb = openpyxl.Workbook()
ws = wb.active
ws.append(["Category", "Value"])
ws.append(["Precio Unitario", 100])
ws.append(["Volumen", 80])

ch = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_row=3)
ch.add_data(data, titles_from_data=True)

# Test setting StrRef directly
ref_str = f"'{ws.title}'!$A$2:$A$3"
for s in ch.series:
    s.cat = AxDataSource(strRef=StrRef(f=ref_str))

ws.add_chart(ch, "D1")
wb.save("scratch/test_strref.xlsx")

import zipfile, xml.dom.minidom
with zipfile.ZipFile("scratch/test_strref.xlsx") as z:
    xml_str = z.read("xl/charts/chart1.xml").decode("utf-8")
    dom = xml.dom.minidom.parseString(xml_str)
    for tag in dom.getElementsByTagName("cat"):
        print("TAG CAT:", tag.toprettyxml())
