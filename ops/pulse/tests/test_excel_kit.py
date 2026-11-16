"""
ops/pulse/tests/test_excel_kit.py
---------------------------------
Suite de pruebas automatizadas para los libros Excel de Datalaria Pulse.
Especificación: Hito P-LAUNCH-3C (specs/apps/pulse/spec.md).

Verifica:
1. Tracker privado (Pulse_Private_Tracker.xlsx en data/pulse/private/).
2. Plantilla comercial en Español (Pulse_Content_Ops_Template_ES.xlsx y alias).
3. Plantilla comercial en Inglés (Pulse_Content_Ops_Template_EN.xlsx).
4. Tablas nativas, filtros, ordenación, freeze_panes y colores de pestaña (0284C7, 059669, D97706).
5. Automatismos de cero duplicación: fórmulas en Activos/Assets, Métricas/Metrics, Kanban y Dashboard.
"""

import os
from pathlib import Path
import openpyxl
import pytest

from ops.pulse.kit.build_pulse_kit import build_pulse_excel, ROOT_DIR, OUTPUT_DIR, PRIVATE_OUTPUT_DIR


def test_build_pulse_excel_private_tracker():
    """Verifica que el tracker privado para Datalaria se genera con todas las hojas y datos."""
    dest_path = build_pulse_excel(is_template=False, lang="es")
    assert dest_path.exists()
    assert dest_path.name == "Pulse_Private_Tracker.xlsx"
    assert dest_path.parent == PRIVATE_OUTPUT_DIR

    wb = openpyxl.load_workbook(dest_path, data_only=False)
    expected_sheets = ["Instrucciones", "Taxonomía", "Activos", "Kanban", "Métricas", "Dashboard"]
    for s in expected_sheets:
        assert s in wb.sheetnames

    ws_act = wb["Activos"]
    # Debe contener cabecera + al menos 135 activos catalogados
    assert ws_act.max_row >= 136

    # Comprobar columnas clave
    assert ws_act.cell(row=1, column=1).value == "ID"
    assert ws_act.cell(row=1, column=10).value == "Paridad"
    assert ws_act.cell(row=1, column=15).value == "Score SEO"
    assert ws_act.cell(row=1, column=20).value == "Visitas 30d"

    # Colores de pestaña
    assert wb["Instrucciones"].sheet_properties.tabColor.rgb == "000284C7"
    assert wb["Activos"].sheet_properties.tabColor.rgb == "00059669"
    assert wb["Dashboard"].sheet_properties.tabColor.rgb == "00D97706"


def test_build_pulse_excel_template_es():
    """Verifica que la plantilla del Kit comercial en español se genera con tablas, colores y fórmulas."""
    dest_path = build_pulse_excel(is_template=True, lang="es")
    assert dest_path.exists()
    assert dest_path.name == "Pulse_Content_Ops_Template_ES.xlsx"
    alias_path = OUTPUT_DIR / "Pulse_Content_Ops_Template.xlsx"
    assert alias_path.exists()

    wb = openpyxl.load_workbook(dest_path, data_only=False)
    expected_sheets = ["Instrucciones", "Taxonomía", "Activos", "Kanban", "Métricas", "Dashboard"]
    for s in expected_sheets:
        assert s in wb.sheetnames

    # 1. Colores de pestaña
    assert wb["Instrucciones"].sheet_properties.tabColor.rgb == "000284C7"
    assert wb["Taxonomía"].sheet_properties.tabColor.rgb == "000284C7"
    assert wb["Activos"].sheet_properties.tabColor.rgb == "00059669"
    assert wb["Kanban"].sheet_properties.tabColor.rgb == "00059669"
    assert wb["Métricas"].sheet_properties.tabColor.rgb == "00059669"
    assert wb["Dashboard"].sheet_properties.tabColor.rgb == "00D97706"

    # 2. Hoja Activos: Tablas nativas, freeze_panes y 10 activos de muestra
    ws_act = wb["Activos"]
    assert len(ws_act.tables) == 1
    assert "ActivosTable" in ws_act.tables
    assert ws_act.freeze_panes == "B2"
    # 10 activos de muestra con ID + fórmulas pre-configuradas hasta fila 50
    asset_rows = [r for r in range(2, ws_act.max_row + 1) if ws_act.cell(row=r, column=1).value]
    assert len(asset_rows) == 10
    assert ws_act.max_row == 50

    # Fórmulas en Activos: Lectura (Col 14), Visitas (Col 20), Usuarios (Col 21)
    reading_formula = str(ws_act.cell(row=2, column=14).value)
    assert "ROUND" in reading_formula and "/200" in reading_formula
    views_formula = str(ws_act.cell(row=2, column=20).value)
    assert "INDEX" in views_formula and "Métricas" in views_formula

    # 3. Hoja Métricas: Auto-rellenado de Tipo (Col B) y Título (Col H)
    ws_met = wb["Métricas"]
    assert len(ws_met.tables) == 1
    assert "MetricasTable" in ws_met.tables
    assert ws_met.freeze_panes == "B2"
    type_formula = str(ws_met.cell(row=2, column=2).value)
    assert "INDEX('Activos'!$B$2:$B$500" in type_formula
    title_formula = str(ws_met.cell(row=2, column=8).value)
    assert "INDEX('Activos'!$E$2:$E$500" in title_formula

    # 4. Hoja Kanban: Fórmulas dinámicas y contadores en cabecera
    ws_kan = wb["Kanban"]
    c2_counter = str(ws_kan.cell(row=2, column=2).value)
    assert "COUNTIF('Activos'!$C$2:$C$500" in c2_counter
    k_card = str(ws_kan.cell(row=4, column=2).value)
    assert "INDEX('Activos'!$E$2:$E$500" in k_card

    # 5. Hoja Dashboard: Scorecard ejecutivo
    ws_dash = wb["Dashboard"]
    d_total = str(ws_dash.cell(row=4, column=4).value)
    assert "COUNTA('Activos'!A2:A11)" in d_total
    d_pub = str(ws_dash.cell(row=5, column=4).value)
    assert 'COUNTIF(\'Activos\'!C2:C11, "Published")' in d_pub


def test_build_pulse_excel_template_en():
    """Verifica que la plantilla comercial en inglés se genera con hojas EN y fórmulas adaptadas."""
    dest_path = build_pulse_excel(is_template=True, lang="en")
    assert dest_path.exists()
    assert dest_path.name == "Pulse_Content_Ops_Template_EN.xlsx"

    wb = openpyxl.load_workbook(dest_path, data_only=False)
    expected_sheets = ["Instructions", "Taxonomy", "Assets", "Kanban", "Metrics", "Dashboard"]
    for s in expected_sheets:
        assert s in wb.sheetnames

    # 1. Colores de pestaña
    assert wb["Instructions"].sheet_properties.tabColor.rgb == "000284C7"
    assert wb["Taxonomy"].sheet_properties.tabColor.rgb == "000284C7"
    assert wb["Assets"].sheet_properties.tabColor.rgb == "00059669"
    assert wb["Kanban"].sheet_properties.tabColor.rgb == "00059669"
    assert wb["Metrics"].sheet_properties.tabColor.rgb == "00059669"
    assert wb["Dashboard"].sheet_properties.tabColor.rgb == "00D97706"

    # 2. Hoja Assets: Tablas nativas, freeze_panes y 10 activos
    ws_ast = wb["Assets"]
    assert len(ws_ast.tables) == 1
    assert "AssetsTable" in ws_ast.tables
    assert ws_ast.freeze_panes == "B2"
    asset_rows = [r for r in range(2, ws_ast.max_row + 1) if ws_ast.cell(row=r, column=1).value]
    assert len(asset_rows) == 10
    assert ws_ast.max_row == 50
    assert ws_ast.cell(row=1, column=1).value == "ID"
    assert ws_ast.cell(row=1, column=2).value == "Type"
    assert ws_ast.cell(row=1, column=10).value == "Parity"

    # Fórmulas en Assets vinculando a Metrics
    views_formula = str(ws_ast.cell(row=2, column=20).value)
    assert "INDEX" in views_formula and "Metrics" in views_formula

    # 3. Hoja Metrics
    ws_met = wb["Metrics"]
    assert len(ws_met.tables) == 1
    assert "MetricsTable" in ws_met.tables
    assert ws_met.freeze_panes == "B2"
    type_formula = str(ws_met.cell(row=2, column=2).value)
    assert "INDEX('Assets'!$B$2:$B$500" in type_formula

    # 4. Hoja Kanban
    ws_kan = wb["Kanban"]
    c2_counter = str(ws_kan.cell(row=2, column=2).value)
    assert "COUNTIF('Assets'!$C$2:$C$500" in c2_counter

    # 5. Hoja Dashboard
    ws_dash = wb["Dashboard"]
    d_total = str(ws_dash.cell(row=4, column=4).value)
    assert "COUNTA('Assets'!A2:A11)" in d_total
