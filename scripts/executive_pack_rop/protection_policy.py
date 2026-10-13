#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protection_policy.py
====================
Módulo de política de protección de celdas y seguridad OpenXML ECMA-376
para el Executive Decision Pack Calculadora de Stock de Seguridad & ROP (Datalaria.com).

Reglas de protección:
- Celdas de entrada (usuario): locked=False, fondo blanco #FFFFFF.
- Celdas con fórmulas: locked=True, fondo #F1F5F9.
- Celdas decorativas/encabezados: locked=True, fondo corporativo preservado.
- Contraseña oficial interna: "Datalaria2026"
- ECMA-376: selectUnlockedCells=False, selectLockedCells=False
  (En el estándar XML de Excel, estos atributos representan restricciones: False = sin restricción/bloqueo activo,
  permitiendo seleccionar, hacer doble clic y editar con fluidez las celdas desbloqueadas).
"""

from openpyxl.styles import Protection, PatternFill
from openpyxl.cell.cell import MergedCell
from openpyxl.worksheet.formula import ArrayFormula

PASSWORD_PROTECT = "Datalaria2026"
FILL_INPUT = PatternFill(fill_type="solid", fgColor="FFFFFF")
FILL_FORMULA = PatternFill(fill_type="solid", fgColor="F1F5F9")


def is_formula(cell):
    """Verifica si una celda contiene una fórmula de Excel."""
    v = cell.value
    return isinstance(v, ArrayFormula) or (isinstance(v, str) and str(v).startswith("="))


def apply_sheet_protection(ws):
    """
    Aplica protección de hoja según el estándar ECMA-376 OpenXML.
    selectUnlockedCells = False (permite seleccionar y editar celdas desbloqueadas con total normalidad)
    selectLockedCells = False (permite seleccionar celdas bloqueadas para lectura transparente de fórmulas)
    objects = False (permite renderizado e interactividad fluida con gráficos)
    """
    ws.protection.set_password(PASSWORD_PROTECT)
    ws.protection.sheet = True
    ws.protection.objects = False
    ws.protection.scenarios = True
    ws.protection.selectUnlockedCells = False
    ws.protection.selectLockedCells = False
    ws.protection.insertRows = False
    ws.protection.deleteRows = False
    ws.protection.formatCells = False
    ws.protection.formatColumns = False
    ws.protection.formatRows = False
    ws.protection.sort = False
    ws.protection.autoFilter = False


def finalize_protection(ws, input_ranges=None, formula_ranges=None, decorative_cells=None):
    """
    Asegura que:
    1. Celdas de entrada (usuario) tengan locked=False y fondo blanco puro #FFFFFF.
    2. Celdas de fórmula o datos protegidos tengan locked=True y fondo gris claro #F1F5F9.
    3. Celdas de cabecera/decorativas mantengan su estilo y locked=True.
    4. NINGUNA celda bloqueada quede con fondo blanco (erradicando confusión visual).
    5. Se active la protección con la contraseña oficial 'Datalaria2026'.
    """
    dec_set = set(decorative_cells) if decorative_cells else set()
    input_set = set()
    if input_ranges:
        for r in input_ranges:
            if isinstance(r, (list, set, tuple)):
                input_set.update(r)
            else:
                input_set.add(r)

    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell, MergedCell):
                continue
            coord = cell.coordinate

            # 1. Celdas de entrada explícitas: DESBLOQUEADAS y FONDO BLANCO PURO
            if coord in input_set:
                cell.protection = Protection(locked=False, hidden=False)
                cell.fill = FILL_INPUT
            # 2. Cabeceras y celdas decorativas: BLOQUEADAS, preservar su color corporativo
            elif coord in dec_set or cell.row in (1, 2, 3, 4):
                cell.protection = Protection(locked=True, hidden=False)
            # 3. Fórmulas: BLOQUEADAS y FONDO GRIS SUAVE
            elif is_formula(cell):
                cell.protection = Protection(locked=True, hidden=False)
                cell.fill = FILL_FORMULA
            # 4. Cualquier otra celda que no sea input: BLOQUEADA
            else:
                cell.protection = Protection(locked=True, hidden=False)
                # Si no tiene fondo corporativo, asignar gris suave para no confundir con celdas blancas editables
                if not cell.fill or cell.fill.fill_type is None or cell.fill.fgColor.rgb in ("00000000", "FFFFFFFF", None):
                    cell.fill = FILL_FORMULA

    apply_sheet_protection(ws)
