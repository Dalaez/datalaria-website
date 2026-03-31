import zipfile
import xml.etree.ElementTree as ET
import os

def extract_text_from_docx(docx_path):
    document_zip = zipfile.ZipFile(docx_path)
    xml_content = document_zip.read('word/document.xml')
    document_zip.close()
    
    tree = ET.XML(xml_content)
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    TEXT = WORD_NAMESPACE + 't'
    
    paragraphs = []
    for paragraph in tree.iter(WORD_NAMESPACE + 'p'):
        texts = [node.text
                 for node in paragraph.iter(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))
            
    return '\n'.join(paragraphs)

basedir = r'c:\Users\dalae\OneDrive\Emprendiendo\datalaria\content\es\posts\kantorovich'
docx_path = os.path.join(basedir, 'Kantorovich, Programación Lineal y Optimización.docx')
out_path = os.path.join(basedir, 'extracted_text.txt')

try:
    text = extract_text_from_docx(docx_path)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Success. Extracted to", out_path)
except Exception as e:
    print("Error:", e)
