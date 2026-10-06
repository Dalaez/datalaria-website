import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[ES]_Estimacion_PERT_3_Puntos/Estimacion_PERT_Estocastica_ES.xlsx', 'r') as z:
    for name in z.namelist():
        if 'chart' in name:
            print("Found chart:", name)
            xml_content = z.read(name).decode('utf-8')
            print(xml_content[:2000])
