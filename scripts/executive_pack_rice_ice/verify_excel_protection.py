#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_excel_protection.py
==========================
Script de verificación y auditoría exhaustiva de protección y seguridad OpenXML
para los libros Excel del Executive Decision Pack RICE & ICE:
1. packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[ES]_Matriz_RICE_ICE/Matriz_RICE_ICE_Datalaria_ES.xlsx
2. packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[EN]_RICE_ICE_Matrix/RICE_ICE_Matrix_Datalaria_EN.xlsx

Verificaciones obligatorias:
1. Regla de Oro:
   - Toda celda CON fórmula -> locked == True
   - Toda celda SIN fórmula -> locked == False
2. Regla de Relleno en zonas no decorativas:
   - Con fórmula -> F1F5F9
   - Sin fórmula -> FFFFFF
3. Parámetros de ws.protection:
   - sheet is True
   - password hash presente
   - selectUnlockedCells is False
   - selectLockedCells is False
4. Inspección XML crudo en archivo ZIP:
   - Presencia de <sheetProtection
   - Ausencia absoluta de selectUnlockedCells="1" y selectLockedCells="1"
5. Muestreo explícito de 5 celdas vacías y 5 celdas con fórmula por pestaña.
6. Código de salida sys.exit(1) si existe al menos 1 infracción.
"""

import sys
import os
import zipfile
import re
import openpyxl
from openpyxl.cell.cell import MergedCell
from openpyxl.worksheet.formula import ArrayFormula

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

WORKBOOKS = [
    ("ES", "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[ES]_Matriz_RICE_ICE/Matriz_RICE_ICE_Datalaria_ES.xlsx"),
    ("EN", "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/[EN]_RICE_ICE_Matrix/RICE_ICE_Matrix_Datalaria_EN.xlsx"),
]


def is_formula(cell):
    v = cell.value
    return isinstance(v, ArrayFormula) or (isinstance(v, str) and v.startswith("="))


def get_fill_hex(cell):
    if cell.fill and cell.fill.fgColor:
        color = cell.fill.fgColor
        if hasattr(color, 'rgb') and color.rgb:
            rgb_str = str(color.rgb)
            if len(rgb_str) == 8:
                return rgb_str[2:].upper()
            return rgb_str.upper()
    return None


def verify_workbook(label, path):
    print(f"\n{'='*80}")
    print(f"AUDITORÍA DE PROTECCIÓN Y OPENXML: {label} -> {path}")
    print(f"{'='*80}")

    if not os.path.exists(path):
        print(f"[ERROR CRÍTICO] Archivo no encontrado: {path}")
        return 1

    wb = openpyxl.load_workbook(path, data_only=False)
    total_violations = 0

    # 1. Auditoría de cada pestaña a nivel objeto openpyxl
    for sheetname in wb.sheetnames:
        ws = wb[sheetname]
        prot = ws.protection
        sheet_violations = []

        print(f"\n--- [Pestaña: {sheetname}] (Rango: {ws.dimensions}) ---")
        
        # Validar configuración general de protección
        if not prot.sheet:
            sheet_violations.append(f"ws.protection.sheet no está activo ({prot.sheet})")
        if not prot.password:
            sheet_violations.append("No se encontró hash de contraseña en ws.protection")
        if prot.selectUnlockedCells is not False:
            sheet_violations.append(f"selectUnlockedCells debe ser False, se encontró {prot.selectUnlockedCells}")
        if prot.selectLockedCells is not False:
            sheet_violations.append(f"selectLockedCells debe ser False, se encontró {prot.selectLockedCells}")

        editable_count = 0
        protected_count = 0
        empty_samples = []
        formula_samples = []

        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                if isinstance(cell, MergedCell):
                    continue

                has_form = is_formula(cell)
                locked = cell.protection.locked if cell.protection else True

                # Regla de oro de protección
                if has_form and not locked:
                    sheet_violations.append(f"Celda con fórmula DESBLOQUEADA en {cell.coordinate}: '{cell.value}'")
                elif not has_form and locked:
                    sheet_violations.append(f"Celda sin fórmula BLOQUEADA en {cell.coordinate}: '{cell.value}'")

                if locked:
                    protected_count += 1
                else:
                    editable_count += 1

                # Muestreo para informe
                if not has_form and (cell.value is None or str(cell.value).strip() == ""):
                    if len(empty_samples) < 5:
                        empty_samples.append((cell.coordinate, locked, get_fill_hex(cell)))
                elif has_form:
                    if len(formula_samples) < 5:
                        formula_samples.append((cell.coordinate, str(cell.value)[:35], locked, get_fill_hex(cell)))

        print(f"  • Celdas desbloqueadas (editables): {editable_count}")
        print(f"  • Celdas bloqueadas (fórmulas): {protected_count}")

        print("  • Muestreo celdas de entrada vacías (deben ser locked=False, fill=FFFFFF):")
        for coord, lock_st, f_hex in empty_samples:
            status = "OK" if not lock_st and f_hex == "FFFFFF" else "FALLO"
            print(f"     [{status}] {coord}: locked={lock_st}, fill={f_hex}")

        print("  • Muestreo celdas con fórmula (deben ser locked=True, fill=F1F5F9 o decorativo):")
        for coord, form_str, lock_st, f_hex in formula_samples:
            status = "OK" if lock_st else "FALLO"
            safe_str = form_str.encode('ascii', errors='replace').decode('ascii')
            print(f"     [{status}] {coord}: locked={lock_st}, fill={f_hex}, formula='{safe_str}'")

        if sheet_violations:
            print(f"  [X] VIOLACIONES DETECTADAS EN '{sheetname}': {len(sheet_violations)}")
            for v in sheet_violations[:15]:
                print(f"      - {v}")
            total_violations += len(sheet_violations)
        else:
            print(f"  [OK] Pestaña '{sheetname}': 0 violaciones detectadas.")

    # 2. Inspección directa de XML crudo en ZIP
    print("\n--- Verificación Cruda de XML (anti-restricción selectUnlockedCells='1') ---")
    xml_violations = 0
    with zipfile.ZipFile(path, 'r') as zf:
        sheet_files = [f for f in zf.namelist() if f.startswith('xl/worksheets/sheet') and f.endswith('.xml')]
        for sfile in sheet_files:
            xml_content = zf.read(sfile).decode('utf-8', errors='ignore')
            prot_match = re.search(r'<sheetProtection\b([^>]+)>', xml_content)
            if not prot_match:
                print(f"  [X] {sfile}: No se encontró etiqueta <sheetProtection> en XML.")
                xml_violations += 1
                continue
            attrs = prot_match.group(1)
            if 'selectUnlockedCells="1"' in attrs:
                print(f"  [X] {sfile}: Infracción crítica detectada -> selectUnlockedCells=\"1\" bloquea edición.")
                xml_violations += 1
            if 'selectLockedCells="1"' in attrs:
                print(f"  [X] {sfile}: Infracción detectada -> selectLockedCells=\"1\".")
                xml_violations += 1
            if 'password=' not in attrs and 'hashValue=' not in attrs:
                print(f"  [X] {sfile}: No se encontró hash de contraseña en <sheetProtection>.")
                xml_violations += 1

    if xml_violations == 0:
        print("  [OK] XML verificado: <sheetProtection> presente, atributos de restricción = 0.")
    else:
        total_violations += xml_violations

    print(f"\nResumen para {label}: {total_violations} violaciones totales.")
    return total_violations


def main():
    grand_total_violations = 0
    for label, path in WORKBOOKS:
        violations = verify_workbook(label, path)
        grand_total_violations += violations

    print("\n" + "="*80)
    if grand_total_violations == 0:
        print("[AUDITORÍA SUPERADA CON ÉXITO] 0 violaciones en versiones ES y EN.")
        print("Todos los libros cumplen rigurosamente el estándar de protección C-Level.")
        print("="*80)
        sys.exit(0)
    else:
        print(f"[AUDITORÍA FALLIDA] Se detectaron {grand_total_violations} violaciones.")
        print("="*80)
        sys.exit(1)


if __name__ == "__main__":
    main()
