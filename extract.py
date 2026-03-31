import zipfile
import xml.etree.ElementTree as ET
try:
    with zipfile.ZipFile(r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria\content\es\posts\clarity_ai\IA, Sostenibilidad y Datos Financieros.docx") as docx:
        tree = ET.fromstring(docx.read('word/document.xml'))
    print('\n'.join(''.join(n.text for n in p.iterfind('.//w:t', {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) if n.text) for p in tree.iterfind('.//w:p', {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})))
except Exception as e:
    print("Error:", e)
