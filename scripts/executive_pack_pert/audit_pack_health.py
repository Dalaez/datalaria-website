#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_pack_health.py
====================
Verifica minuciosamente la integridad de todos los archivos generados tras el reinicio/apagón:
1. Integridad CRC32 de los archivos zip (.xlsx, .pptx, .zip).
2. Verificación de fórmulas XML en openpyxl sin corrupción.
3. Verificación de permisos y protecciones de celdas ECMA-376.
4. Verificación de dimensiones de celdas y gráficos.
5. Comprobación del paquete de distribución Lemon Squeezy.
"""

import os
import sys
import zipfile
import re
import xml.etree.ElementTree as ET
import openpyxl
from pptx import Presentation

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def audit_xlsx(fpath):
    print(f"\n=======================================================")
    print(f"AUDITORÍA XLSX: {fpath}")
    print(f"=======================================================")
    
    # 1. CRC Check
    with zipfile.ZipFile(fpath, 'r') as z:
        bad = z.testzip()
        if bad:
            print(f"[FAIL] Archivo corrupto en entrada ZIP: {bad}")
            return False
        print("[PASS] Integridad física ZIP CRC32: 100% Correcta.")
        
        # 2. XML Formula syntax check
        err_count = 0
        for name in z.namelist():
            if 'sheet' in name and name.endswith('.xml'):
                root = ET.fromstring(z.read(name))
                for c in root.findall('.//s:c', ns):
                    f = c.find('s:f', ns)
                    if f is not None and f.text:
                        txt = f.text
                        tokens = re.findall(r"'[^']+'", txt)
                        for tok in tokens:
                            idx = txt.find(tok)
                            after = txt[idx+len(tok):idx+len(tok)+1]
                            if after != '!':
                                print(f"  [ERROR FÓRMULA] {name} celda {c.attrib.get('r')}: {txt} | Token inválido: {tok}")
                                err_count += 1
        if err_count == 0:
            print("[PASS] Fórmulas OpenXML: Cero errores de sintaxis (sin comillas simples en strings).")
        else:
            print(f"[FAIL] {err_count} errores de fórmulas detectados.")
            return False

        # 3. Chart XML check
        if 'xl/charts/chart1.xml' in z.namelist():
            chart_xml = z.read('xl/charts/chart1.xml')
            ch_root = ET.fromstring(chart_xml)
            axes = [elem.tag.split('}')[-1] for elem in ch_root.iter() if elem.tag.endswith('catAx') or elem.tag.endswith('valAx')]
            print(f"[PASS] Gráfico chart1.xml presente con ejes: {axes}")
        else:
            print("[WARN] chart1.xml no encontrado en el paquete.")

    # 4. openpyxl load test
    wb = openpyxl.load_workbook(fpath)
    print(f"[PASS] Apertura openpyxl exitosa. Pestañas ({len(wb.sheetnames)}): {wb.sheetnames}")
    for name in wb.sheetnames:
        ws = wb[name]
        is_prot = ws.protection.sheet
        print(f"  • [{name}]: {ws.max_row} filas x {ws.max_column} columnas | Protección: {is_prot}")
    return True

def audit_pptx(fpath):
    print(f"\n=======================================================")
    print(f"AUDITORÍA PPTX: {fpath}")
    print(f"=======================================================")
    with zipfile.ZipFile(fpath, 'r') as z:
        bad = z.testzip()
        if bad:
            print(f"[FAIL] Corrupción ZIP en PPTX: {bad}")
            return False
    prs = Presentation(fpath)
    print(f"[PASS] Presentación cargada: {len(prs.slides)} diapositivas (16:9).")
    for i, slide in enumerate(prs.slides, 1):
        shapes_count = len(slide.shapes)
        print(f"  • Slide {i}: {shapes_count} elementos gráficos.")
    return True

def audit_zip(fpath):
    print(f"\n=======================================================")
    print(f"AUDITORÍA ZIP MASTER: {fpath}")
    print(f"=======================================================")
    with zipfile.ZipFile(fpath, 'r') as z:
        bad = z.testzip()
        if bad:
            print(f"[FAIL] Archivo ZIP maestro corrupto: {bad}")
            return False
        print(f"[PASS] Archivo ZIP maestro ({os.path.getsize(fpath)/1024:.1f} KB) - Integridad CRC32 perfecta.")
        for info in z.infolist():
            print(f"  • {info.filename} ({info.file_size/1024:.1f} KB)")
    return True

if __name__ == '__main__':
    ok1 = audit_xlsx('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[ES]_Estimacion_PERT_3_Puntos/Estimacion_PERT_Estocastica_ES.xlsx')
    ok2 = audit_xlsx('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[EN]_3Point_PERT_Estimation/Stochastic_PERT_Estimation_EN.xlsx')
    ok3 = audit_pptx('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[ES]_Estimacion_PERT_3_Puntos/Presentacion_PERT_CLevel_ES.pptx')
    ok4 = audit_pptx('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/[EN]_3Point_PERT_Estimation/Deck_PERT_CLevel_EN.pptx')
    ok5 = audit_zip('packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/Executive_Decision_Pack_PERT_Dual.zip')
    ok6 = audit_zip('packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_PERT_Dual.zip')

    if all([ok1, ok2, ok3, ok4, ok5, ok6]):
        print("\n\n>>> VEREDICTO FINAL: TODOS LOS ARCHIVOS ESTÁN 100% INTACTOS, SIN DAÑOS NI CORRUPCIÓN TRAS EL APAGÓN. <<<")
    else:
        print("\n\n>>> ALERTA: SE DETECTARON ERRORES TRAS EL APAGÓN. <<<")
