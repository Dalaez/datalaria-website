import zipfile
import xml.etree.ElementTree as ET

z = zipfile.ZipFile('packages/ES_Matriz_McKinsey_GE_Datalaria.xlsx')
styles_tree = ET.fromstring(z.read('xl/styles.xml'))
sheet1_tree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))

# Namespace
ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

cellXfs = styles_tree.find('main:cellXfs', ns)
print(f"Total cellXfs: {len(cellXfs)}")
for idx, xf in enumerate(cellXfs):
    prot = xf.find('main:protection', ns)
    applyProt = xf.attrib.get('applyProtection')
    if prot is not None or applyProt is not None:
        locked = prot.attrib.get('locked') if prot is not None else None
        print(f"xf index {idx}: applyProtection={applyProt}, locked={locked}")

# Check cells in sheet1
for row in sheet1_tree.findall('.//main:row', ns):
    for c in row.findall('main:c', ns):
        r = c.attrib.get('r')
        if r in ['C30', 'D30', 'E30', 'F30', 'H30']:
            s_idx = int(c.attrib.get('s', 0))
            xf = cellXfs[s_idx]
            prot = xf.find('main:protection', ns)
            applyProt = xf.attrib.get('applyProtection')
            locked = prot.attrib.get('locked') if prot is not None else 'default(1)'
            print(f"Cell {r}: style_index={s_idx}, applyProtection={applyProt}, locked={locked}")
