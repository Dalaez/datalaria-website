import zipfile
import re
import xml.etree.ElementTree as ET

ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def inspect_file(fpath):
    print(f"\n=================== {fpath} ===================")
    with zipfile.ZipFile(fpath, 'r') as z:
        for name in z.namelist():
            if 'sheet' in name and name.endswith('.xml'):
                root = ET.fromstring(z.read(name))
                for c in root.findall('.//s:c', ns):
                    f = c.find('s:f', ns)
                    if f is not None and f.text:
                        txt = f.text
                        # Check single quotes not followed by exclamation mark !
                        # A valid sheet reference is 'Sheet Name'!A1
                        # If there's ' something ' not followed by !
                        tokens = re.findall(r"'[^']+'", txt)
                        for tok in tokens:
                            idx = txt.find(tok)
                            after = txt[idx+len(tok):idx+len(tok)+1]
                            if after != '!':
                                print(f"ERROR in {name} cell {c.attrib.get('r')}: {txt} | Illegal string token: {tok}")

inspect_file('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[ES]_Estimacion_PERT_3_Puntos/Estimacion_PERT_Estocastica_ES.xlsx')
inspect_file('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[EN]_3Point_PERT_Estimation/Stochastic_PERT_Estimation_EN.xlsx')
