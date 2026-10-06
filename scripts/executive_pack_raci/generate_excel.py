#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos oficiales de cálculo en Excel (.xlsx) y Google Sheets:
1. packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga/[ES]_Matriz_RACI_Balance_Carga/Matriz_RACI_Balance_Carga_ES.xlsx
2. packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga/[EN]_Quantitative_RACI_Workload/Quantitative_RACI_Workload_EN.xlsx

Arquitectura de 4 Pestañas:
- Pestaña 1: Dashboard Ejecutivo / Executive Dashboard
- Pestaña 2: Matriz RACI & Gobernanza / RACI Matrix & Governance
- Pestaña 3: Balance de Carga (Workload) / Workload Balancing
- Pestaña 4: Plan de Rebalanceo & Acción / Action & Rebalancing Plan

Protección OpenXML ECMA-376 con contraseña "Datalaria2026":
- Celdas de entrada desbloqueadas (locked=False, fondo blanco #FFFFFF).
- Celdas de fórmulas y títulos protegidas (locked=True, fondo #F1F5F9 o decorativo).
- selectUnlockedCells=False y selectLockedCells=False.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.chart.data_source import StrRef, StrData, StrVal, AxDataSource
from openpyxl.utils import get_column_letter

from protection_policy import (
    PASSWORD_PROTECT, FILL_INPUT, FILL_FORMULA, apply_sheet_protection
)

# Paleta Corporativa Datalaria
C_NAVY_DARK = "0F172A"    # Slate 900
C_NAVY_MED = "1E293B"     # Slate 800
C_BLUE_ACCENT = "2563EB"  # Blue 600
C_BLUE_LIGHT = "EFF6FF"   # Blue 50
C_TEAL_ACCENT = "0D9488"  # Teal 600
C_TEAL_LIGHT = "F0FDFA"   # Teal 50
C_PURPLE = "7C3AED"       # Purple 600
C_AMBER_ACCENT = "D97706" # Amber 600
C_AMBER_LIGHT = "FFFBEB"  # Amber 50
C_RED_ACCENT = "E11D48"   # Red 600
C_RED_LIGHT = "FFF1F2"    # Red 50
C_GREEN_ACCENT = "10B981"# Emerald 500
C_GREEN_LIGHT = "D1FAE5" # Emerald 100
C_GREEN_TEXT = "065F46"  # Emerald 800
C_AMBER_TEXT = "92400E"  # Amber 800
C_RED_TEXT = "991B1B"    # Red 800
C_GRAY_BG = "F8FAFC"     # Slate 50
C_BORDER = "CBD5E1"      # Slate 300
C_BORDER_LIGHT = "E2E8F0"# Slate 200
C_WHITE = "FFFFFF"

# Fills y Fuentes comunes
FONT_TITLE = Font(name="Segoe UI", size=14, bold=True, color=C_WHITE)
FONT_SUBTITLE = Font(name="Segoe UI", size=9, italic=True, color="94A3B8")
FONT_SEC_HEADER = Font(name="Segoe UI", size=11, bold=True, color=C_WHITE)
FONT_TH = Font(name="Segoe UI", size=9, bold=True, color=C_WHITE)
FONT_TH_DARK = Font(name="Segoe UI", size=9, bold=True, color=C_NAVY_DARK)
FONT_REGULAR = Font(name="Segoe UI", size=9, color="1E293B")
FONT_BOLD = Font(name="Segoe UI", size=9, bold=True, color="0F172A")
FONT_MUTED = Font(name="Segoe UI", size=8, color="64748B")
FONT_KPI_VAL = Font(name="Segoe UI", size=18, bold=True, color=C_NAVY_DARK)
FONT_KPI_VAL_ACCENT = Font(name="Segoe UI", size=18, bold=True, color=C_BLUE_ACCENT)
FONT_KPI_LBL = Font(name="Segoe UI", size=8, bold=True, color="475569")
FONT_KPI_SUB = Font(name="Segoe UI", size=7, italic=True, color="64748B")

FILL_NAVY = PatternFill("solid", fgColor=C_NAVY_DARK)
FILL_NAVY_MED = PatternFill("solid", fgColor=C_NAVY_MED)
FILL_BLUE = PatternFill("solid", fgColor=C_BLUE_ACCENT)
FILL_BLUE_LIGHT = PatternFill("solid", fgColor=C_BLUE_LIGHT)
FILL_TEAL = PatternFill("solid", fgColor=C_TEAL_ACCENT)
FILL_TEAL_LIGHT = PatternFill("solid", fgColor=C_TEAL_LIGHT)
FILL_PURPLE = PatternFill("solid", fgColor=C_PURPLE)
FILL_AMBER = PatternFill("solid", fgColor=C_AMBER_ACCENT)
FILL_AMBER_LIGHT = PatternFill("solid", fgColor=C_AMBER_LIGHT)
FILL_RED_LIGHT = PatternFill("solid", fgColor=C_RED_LIGHT)
FILL_GREEN_LIGHT = PatternFill("solid", fgColor=C_GREEN_LIGHT)
FILL_GRAY = PatternFill("solid", fgColor=C_GRAY_BG)

THIN_SIDE = Side(border_style="thin", color=C_BORDER)
THIN_LIGHT_SIDE = Side(border_style="thin", color=C_BORDER_LIGHT)
BORDER_ALL_THIN = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)
BORDER_CARD = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")


def build_raci_workbook(lang='ES'):
    wb = openpyxl.Workbook()
    # Sheet names
    if lang == 'ES':
        s1_name = "Dashboard Ejecutivo"
        s2_name = "Matriz RACI & Gobernanza"
        s3_name = "Balance de Carga"
        s4_name = "Plan de Rebalanceo"
    else:
        s1_name = "Executive Dashboard"
        s2_name = "RACI Matrix & Governance"
        s3_name = "Workload Balancing"
        s4_name = "Rebalancing Plan"

    ws1 = wb.active
    ws1.title = s1_name
    ws2 = wb.create_sheet(title=s2_name)
    ws3 = wb.create_sheet(title=s3_name)
    ws4 = wb.create_sheet(title=s4_name)

    num_fmt_pct = "0,0%" if lang == 'ES' else "0.0%"
    num_fmt_num = "#,##0.0" if lang == 'ES' else "#,##0.0"
    num_fmt_int = "#,##0"

    # =========================================================================
    # TABLA DE ENTREGABLES Y ROLES (Para Pestaña 2)
    # =========================================================================
    roles_es = [
        "Sponsor / Comité",
        "Project Manager",
        "Tech Lead / Arq.",
        "Equipo Desarrollo",
        "QA & Testing",
        "Diseñador UX/UI",
        "Operaciones / DevOps",
        "Legal & Compliance",
        "Product Owner"
    ]
    roles_en = [
        "Sponsor / Steering",
        "Project Manager",
        "Tech Lead / Arch.",
        "Engineering Team",
        "QA & Testing",
        "UX/UI Designer",
        "Operations / DevOps",
        "Legal & Compliance",
        "Product Owner"
    ]
    roles = roles_es if lang == 'ES' else roles_en

    # 25 Entregables Corporativos WBS
    deliverables_es = [
        # Fase 1: Inicio y Alcance
        ("1.1", "Fase 1: Inicio & Alcance", "Project Charter & Caso de Negocio", "Alta", ["A", "R", "I", "I", "I", "I", "I", "C", "C"]),
        ("1.2", "Fase 1: Inicio & Alcance", "Matriz de Interesados (Stakeholders)", "Media", ["I", "A", "I", "I", "I", "I", "I", "C", "R"]),
        ("1.3", "Fase 1: Inicio & Alcance", "Definición de Alcance & WBS Inicial", "Alta", ["C", "A", "C", "I", "I", "I", "I", "I", "R"]),
        ("1.4", "Fase 1: Inicio & Alcance", "Presupuesto Inicial & Calendario Maestro", "Alta", ["A", "R", "I", "I", "I", "I", "I", "I", "C"]),
        ("1.5", "Fase 1: Inicio & Alcance", "Plan de Gobernanza & Matriz RACI", "Alta", ["A", "R", "C", "I", "I", "I", "I", "C", "C"]),

        # Fase 2: Diseño y Arquitectura
        ("2.1", "Fase 2: Diseño & Arquitectura", "Documento de Arquitectura de Software (SAD)", "Alta", ["I", "I", "A", "R", "C", "I", "C", "I", "I"]),
        ("2.2", "Fase 2: Diseño & Arquitectura", "Diseño de Base de Datos & Modelo E-R", "Alta", ["I", "I", "A", "R", "I", "I", "C", "I", "I"]),
        ("2.3", "Fase 2: Diseño & Arquitectura", "Diseño de Interfaz UX/UI & Prototipos", "Media", ["I", "I", "C", "I", "I", "R", "I", "I", "A"]),
        ("2.4", "Fase 2: Diseño & Arquitectura", "Especificación de Requisitos de Negocio (BRD)", "Alta", ["I", "C", "C", "I", "I", "C", "I", "I", "A"]), # R falta temporalmente
        ("2.5", "Fase 2: Diseño & Arquitectura", "Evaluación de Seguridad & RGPD / Cumplimiento", "Alta", ["I", "I", "C", "I", "I", "I", "I", "A", "I"]), # Falta R directo

        # Fase 3: Construcción e Integración
        ("3.1", "Fase 3: Construcción & Integración", "Infraestructura Cloud & Pipeline CI/CD", "Alta", ["I", "I", "A", "I", "I", "I", "R", "I", "I"]),
        ("3.2", "Fase 3: Construcción & Integración", "Desarrollo de Microservicios Backend", "Alta", ["I", "I", "A", "R", "C", "I", "I", "I", "I"]),
        ("3.3", "Fase 3: Construcción & Integración", "Desarrollo Frontend & Componentes Web", "Media", ["I", "I", "C", "R", "C", "C", "I", "I", "A"]), # Doble A inducido para auditoría
        ("3.4", "Fase 3: Construcción & Integración", "Integración de Pasarela de Pagos & APIs", "Alta", ["I", "I", "A", "R", "C", "I", "C", "C", "I"]),
        ("3.5", "Fase 3: Construcción & Integración", "Mapeo y Migración de Datos Legados", "Alta", ["I", "I", "A", "R", "C", "I", "C", "I", "C"]),
        ("3.6", "Fase 3: Construcción & Integración", "Pruebas Unitarias & Cobertura de Código", "Media", ["I", "I", "A", "R", "C", "I", "I", "I", "I"]),

        # Fase 4: Pruebas y Certificación
        ("4.1", "Fase 4: Pruebas & QA", "Plan Maestro de Pruebas (Test Plan)", "Alta", ["I", "I", "C", "I", "A", "I", "I", "I", "C"]), # R omitido intencionalmente
        ("4.2", "Fase 4: Pruebas & QA", "Batería de Pruebas de Integración y Regresión", "Alta", ["I", "I", "C", "C", "A", "I", "I", "I", "I"]),
        ("4.3", "Fase 4: Pruebas & QA", "Pruebas de Carga, Rendimiento y Estrés", "Media", ["I", "I", "C", "I", "A", "I", "R", "I", "I"]),
        ("4.4", "Fase 4: Pruebas & QA", "Auditoría de Vulnerabilidades & Pentesting", "Alta", ["I", "I", "C", "I", "A", "I", "C", "C", "I"]),
        ("4.5", "Fase 4: Pruebas & QA", "Pruebas de Aceptación de Usuario (UAT)", "Alta", ["I", "C", "I", "I", "C", "I", "I", "I", "A"]),

        # Fase 5: Despliegue y Go-Live
        ("5.1", "Fase 5: Despliegue & Operación", "Plan de Transición & Cutover Maestro", "Alta", ["C", "A", "C", "I", "I", "I", "R", "I", "C"]),
        ("5.2", "Fase 5: Despliegue & Operación", "Manuales de Operación & Capacitación", "Media", ["I", "A", "I", "I", "I", "C", "I", "I", "R"]),
        ("5.3", "Fase 5: Despliegue & Operación", "Despliegue Productivo & Go-Live Final", "Alta", ["A", "R", "C", "I", "I", "I", "C", "I", "C"]),
        ("5.4", "Fase 5: Despliegue & Operación", "SLA Operativo & Monitorización 24/7", "Alta", ["I", "I", "C", "I", "I", "I", "A", "I", "C"])
    ]

    deliverables_en = [
        # Phase 1: Initiation and Scope
        ("1.1", "Phase 1: Initiation & Scope", "Project Charter & Business Case", "High", ["A", "R", "I", "I", "I", "I", "I", "C", "C"]),
        ("1.2", "Phase 1: Initiation & Scope", "Stakeholder Matrix & Engagement Plan", "Medium", ["I", "A", "I", "I", "I", "I", "I", "C", "R"]),
        ("1.3", "Phase 1: Initiation & Scope", "Scope Baseline & Initial WBS", "High", ["C", "A", "C", "I", "I", "I", "I", "I", "R"]),
        ("1.4", "Phase 1: Initiation & Scope", "Initial Budget & Master Milestone Schedule", "High", ["A", "R", "I", "I", "I", "I", "I", "I", "C"]),
        ("1.5", "Phase 1: Initiation & Scope", "Governance Plan & RACI Matrix Baseline", "High", ["A", "R", "C", "I", "I", "I", "I", "C", "C"]),

        # Phase 2: Design and Architecture
        ("2.1", "Phase 2: Design & Architecture", "Software Architecture Document (SAD)", "High", ["I", "I", "A", "R", "C", "I", "C", "I", "I"]),
        ("2.2", "Phase 2: Design & Architecture", "Database Schema & Entity-Relationship Model", "High", ["I", "I", "A", "R", "I", "I", "C", "I", "I"]),
        ("2.3", "Phase 2: Design & Architecture", "UX/UI Design System & High-Fi Prototypes", "Medium", ["I", "I", "C", "I", "I", "R", "I", "I", "A"]),
        ("2.4", "Phase 2: Design & Architecture", "Business Requirements Specification (BRD)", "High", ["I", "C", "C", "I", "I", "C", "I", "I", "A"]),
        ("2.5", "Phase 2: Design & Architecture", "Security & GDPR / Regulatory Assessment", "High", ["I", "I", "C", "I", "I", "I", "I", "A", "I"]),

        # Phase 3: Construction & Integration
        ("3.1", "Phase 3: Construction & Build", "Cloud Infrastructure & CI/CD Pipelines", "High", ["I", "I", "A", "I", "I", "I", "R", "I", "I"]),
        ("3.2", "Phase 3: Construction & Build", "Backend Microservices Core Development", "High", ["I", "I", "A", "R", "C", "I", "I", "I", "I"]),
        ("3.3", "Phase 3: Construction & Build", "Frontend Web Portal & UI Integration", "Medium", ["I", "I", "C", "R", "C", "C", "I", "I", "A"]),
        ("3.4", "Phase 3: Construction & Build", "Payment Gateway & External API Integrations", "High", ["I", "I", "A", "R", "C", "I", "C", "C", "I"]),
        ("3.5", "Phase 3: Construction & Build", "Data Mapping & Legacy System Migration", "High", ["I", "I", "A", "R", "C", "I", "C", "I", "C"]),
        ("3.6", "Phase 3: Construction & Build", "Unit Testing Suite & Code Coverage Reports", "Medium", ["I", "I", "A", "R", "C", "I", "I", "I", "I"]),

        # Phase 4: Testing & QA
        ("4.1", "Phase 4: Testing & QA", "Master Test Plan & Traceability Matrix", "High", ["I", "I", "C", "I", "A", "I", "I", "I", "C"]),
        ("4.2", "Phase 4: Testing & QA", "System Integration & Automated Regression Suite", "High", ["I", "I", "C", "C", "A", "I", "I", "I", "I"]),
        ("4.3", "Phase 4: Testing & QA", "Load, Performance & Scalability Stress Tests", "Medium", ["I", "I", "C", "I", "A", "I", "R", "I", "I"]),
        ("4.4", "Phase 4: Testing & QA", "Vulnerability Assessment & Penetration Audit", "High", ["I", "I", "C", "I", "A", "I", "C", "C", "I"]),
        ("4.5", "Phase 4: Testing & QA", "User Acceptance Testing (UAT) Sign-Off", "High", ["I", "C", "I", "I", "C", "I", "I", "I", "A"]),

        # Phase 5: Deployment & Operations
        ("5.1", "Phase 5: Deployment & Go-Live", "Cutover & Production Transition Runbook", "High", ["C", "A", "C", "I", "I", "I", "R", "I", "C"]),
        ("5.2", "Phase 5: Deployment & Go-Live", "Operations Runbooks & Staff Training Materials", "Medium", ["I", "A", "I", "I", "I", "C", "I", "I", "R"]),
        ("5.3", "Phase 5: Deployment & Go-Live", "Production Deployment & Go-Live Sign-Off", "High", ["A", "R", "C", "I", "I", "I", "C", "I", "C"]),
        ("5.4", "Phase 5: Deployment & Go-Live", "Operational SLA & 24/7 Monitoring Baseline", "High", ["I", "I", "C", "I", "I", "I", "A", "I", "C"])
    ]

    deliverables = deliverables_es if lang == 'ES' else deliverables_en

    # =========================================================================
    # CONSTRUCCIÓN DE PESTAÑA 2: MATRIZ RACI & GOBERNANZA
    # =========================================================================
    # Banner
    ws2.merge_cells("A1:R2")
    ws2["A1"] = "DATALARIA | " + ("MATRIZ RACI & VERIFICACIÓN DE GOBERNANZA" if lang == 'ES' else "RACI MATRIX & GOVERNANCE AUDIT")
    ws2["A1"].font = FONT_TITLE
    ws2["A1"].fill = FILL_NAVY
    ws2["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # Subtítulo en fila 3
    ws2.merge_cells("A3:R3")
    ws2["A3"] = ("Control de Responsabilidades: Regla áurea de Accountable único (A=1) y Ejecución mínima (R>=1). Celdas blancas editables." if lang == 'ES' else "Role Accountability: Golden rule of single Accountable (A=1) and minimum Responsible (R>=1). White cells are editable.")
    ws2["A3"].font = FONT_SUBTITLE
    ws2["A3"].fill = FILL_NAVY_MED
    ws2["A3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # Encabezados de Tabla en fila 5 y 6
    headers_sec1 = ("WBS", "Fase / Etapa", "Entregable / Hito del Proyecto", "Criticidad") if lang == 'ES' else ("WBS", "Project Phase", "Deliverable / Project Milestone", "Criticality")
    for col_idx, h in enumerate(headers_sec1, start=1):
        cell = ws2.cell(row=5, column=col_idx, value=h)
        cell.font = FONT_TH
        cell.fill = FILL_NAVY
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL_THIN
        ws2.merge_cells(start_row=5, start_column=col_idx, end_row=6, end_column=col_idx)

    # Roles de Col 5 a Col 13 (E a M)
    ws2.merge_cells("E5:M5")
    ws2["E5"] = "ROLES & DEPARTAMENTOS TRANSVERSALES" if lang == 'ES' else "CROSS-FUNCTIONAL ROLES & DEPARTMENTS"
    ws2["E5"].font = FONT_TH
    ws2["E5"].fill = FILL_BLUE
    ws2["E5"].alignment = ALIGN_CENTER
    ws2["E5"].border = BORDER_ALL_THIN

    for idx, r_name in enumerate(roles, start=5):
        cell = ws2.cell(row=6, column=idx, value=r_name)
        cell.font = FONT_TH
        cell.fill = FILL_NAVY_MED
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL_THIN

    # Columnas de Auditoría (N a R)
    ws2.merge_cells("N5:R5")
    ws2["N5"] = "AUDITORÍA AUTOMÁTICA DE GOBERNANZA" if lang == 'ES' else "AUTOMATED GOVERNANCE AUDIT"
    ws2["N5"].font = FONT_TH
    ws2["N5"].fill = FILL_TEAL
    ws2["N5"].alignment = ALIGN_CENTER
    ws2["N5"].border = BORDER_ALL_THIN

    audit_headers = ["A", "R", "C", "I", "Estado de Gobernanza" if lang == 'ES' else "Governance Status"]
    for idx, ah in enumerate(audit_headers, start=14):
        cell = ws2.cell(row=6, column=idx, value=ah)
        cell.font = FONT_TH
        cell.fill = FILL_NAVY_MED
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL_THIN

    # Filas de datos (fila 7 a 31)
    start_row_raci = 7
    for row_offset, d in enumerate(deliverables):
        r_idx = start_row_raci + row_offset
        wbs_code, phase, name, crit, assignments = d

        # Contexto
        c1 = ws2.cell(row=r_idx, column=1, value=wbs_code)
        c2 = ws2.cell(row=r_idx, column=2, value=phase)
        c3 = ws2.cell(row=r_idx, column=3, value=name)
        c4 = ws2.cell(row=r_idx, column=4, value=crit)

        for c in (c1, c2, c3, c4):
            c.font = FONT_REGULAR
            c.border = BORDER_ALL_THIN
            c.fill = FILL_INPUT
            c.protection = Protection(locked=False)
        c1.alignment = ALIGN_CENTER
        c2.alignment = ALIGN_LEFT
        c3.alignment = ALIGN_LEFT
        c4.alignment = ALIGN_CENTER

        # Asignaciones Roles (Col 5 a 13)
        for col_offset, val in enumerate(assignments):
            col_curr = 5 + col_offset
            c = ws2.cell(row=r_idx, column=col_curr, value=val)
            c.font = FONT_BOLD
            c.alignment = ALIGN_CENTER
            c.border = BORDER_ALL_THIN
            c.fill = FILL_INPUT
            c.protection = Protection(locked=False)

        # Fórmulas de Auditoría
        # N: Count A
        f_a = f'=COUNTIF(E{r_idx}:M{r_idx}, "A")'
        # O: Count R
        f_r = f'=COUNTIF(E{r_idx}:M{r_idx}, "R")'
        # P: Count C
        f_c = f'=COUNTIF(E{r_idx}:M{r_idx}, "C")'
        # Q: Count I
        f_i = f'=COUNTIF(E{r_idx}:M{r_idx}, "I")'

        # R: Status
        if lang == 'ES':
            f_stat = f'=IF(AND(N{r_idx}=1, O{r_idx}>=1), "OK", IF(N{r_idx}=0, "CRÍTICO: Sin A", IF(N{r_idx}>1, "ERROR: Múltiple A", "ALERTA: Sin R")))'
        else:
            f_stat = f'=IF(AND(N{r_idx}=1, O{r_idx}>=1), "OK", IF(N{r_idx}=0, "CRITICAL: No A", IF(N{r_idx}>1, "ERROR: Multiple A", "ALERT: No R")))'

        for c_idx, formula in [(14, f_a), (15, f_r), (16, f_c), (17, f_i), (18, f_stat)]:
            c = ws2.cell(row=r_idx, column=c_idx, value=formula)
            c.font = FONT_BOLD
            c.alignment = ALIGN_CENTER
            c.border = BORDER_ALL_THIN
            c.fill = FILL_FORMULA
            c.protection = Protection(locked=True)

    # Formato Condicional en Columna R (Estado de Gobernanza)
    range_status = f"R7:R{start_row_raci + len(deliverables) - 1}"
    green_fill = PatternFill(bgColor=C_GREEN_LIGHT, fill_type="solid")
    green_font = Font(color=C_GREEN_TEXT, bold=True)
    red_fill = PatternFill(bgColor=C_RED_LIGHT, fill_type="solid")
    red_font = Font(color=C_RED_TEXT, bold=True)
    amber_fill = PatternFill(bgColor=C_AMBER_LIGHT, fill_type="solid")
    amber_font = Font(color=C_AMBER_TEXT, bold=True)

    ok_val = '"OK"'
    crit_val = '"CRÍTICO: Sin A"' if lang == 'ES' else '"CRITICAL: No A"'
    err_val = '"ERROR: Múltiple A"' if lang == 'ES' else '"ERROR: Multiple A"'
    alert_val = '"ALERTA: Sin R"' if lang == 'ES' else '"ALERT: No R"'

    ws2.conditional_formatting.add(range_status, CellIsRule(operator='equal', formula=[ok_val], fill=green_fill, font=green_font))
    ws2.conditional_formatting.add(range_status, CellIsRule(operator='equal', formula=[crit_val], fill=red_fill, font=red_font))
    ws2.conditional_formatting.add(range_status, CellIsRule(operator='equal', formula=[err_val], fill=red_fill, font=red_font))
    ws2.conditional_formatting.add(range_status, CellIsRule(operator='equal', formula=[alert_val], fill=amber_fill, font=amber_font))

    # Anchos de columna ws2
    col_widths_ws2 = {
        'A': 8, 'B': 24, 'C': 44, 'D': 14,
        'E': 16, 'F': 16, 'G': 16, 'H': 16, 'I': 16, 'J': 16, 'K': 18, 'L': 18, 'M': 16,
        'N': 6, 'O': 6, 'P': 6, 'Q': 6, 'R': 22
    }
    for col_l, w in col_widths_ws2.items():
        ws2.column_dimensions[col_l].width = w

    # =========================================================================
    # CONSTRUCCIÓN DE PESTAÑA 3: BALANCE DE CARGA (WORKLOAD)
    # =========================================================================
    # Banner
    ws3.merge_cells("A1:K2")
    ws3["A1"] = "DATALARIA | " + ("BALANCE CUANTITATIVO DE CARGA OPERATIVA & FTE" if lang == 'ES' else "QUANTITATIVE OPERATIONAL WORKLOAD & FTE BALANCING")
    ws3["A1"].font = FONT_TITLE
    ws3["A1"].fill = FILL_NAVY
    ws3["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws3.merge_cells("A3:K3")
    ws3["A3"] = ("Modelo Matemático de Capacidad: Ponderación de esfuerzo por tipo de implicación RACI vs. Capacidad Nominal." if lang == 'ES' else "Mathematical Capacity Engine: Weighted effort calibration per RACI involvement vs. Nominal Capacity.")
    ws3["A3"].font = FONT_SUBTITLE
    ws3["A3"].fill = FILL_NAVY_MED
    ws3["A3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # Sección 1: Ponderación de Esfuerzo (Horas base por asignación)
    ws3.merge_cells("B5:E5")
    ws3["B5"] = "BAREMOS DE PONDERACIÓN POR TIPO DE ASIGNACIÓN (HORAS BASE)" if lang == 'ES' else "EFFORT WEIGHTING STANDARDS PER ASSIGNMENT TYPE (BASE HOURS)"
    ws3["B5"].font = FONT_TH
    ws3["B5"].fill = FILL_BLUE
    ws3["B5"].alignment = ALIGN_CENTER
    ws3["B5"].border = BORDER_ALL_THIN

    weight_headers = ["Tipo RACI", "Descripción Operativa", "Ponderación (Horas)", "Factor FTE (%)"] if lang == 'ES' else ["RACI Type", "Operational Description", "Weight (Hours)", "FTE Factor (%)"]
    for idx, wh in enumerate(weight_headers, start=2):
        c = ws3.cell(row=6, column=idx, value=wh)
        c.font = FONT_TH
        c.fill = FILL_NAVY_MED
        c.alignment = ALIGN_CENTER
        c.border = BORDER_ALL_THIN

    weight_data_es = [
        ("A - Accountable", "Supervisión, toma de decisiones y sign-off ejecutivo", 12.0, "=D7/40"),
        ("R - Responsible", "Construcción activa, análisis y entrega de la tarea", 26.0, "=D8/40"),
        ("C - Consulted", "Reunión de asesoramiento técnico y revisión bilateral", 5.0, "=D9/40"),
        ("I - Informed", "Lectura de actas, minutas y alineación pasiva", 1.5, "=D10/40")
    ]
    weight_data_en = [
        ("A - Accountable", "Oversight, executive sign-off & strategic decision", 12.0, "=D7/40"),
        ("R - Responsible", "Hands-on execution, analysis & deliverable build", 26.0, "=D8/40"),
        ("C - Consulted", "Technical advisory session & bilateral review", 5.0, "=D9/40"),
        ("I - Informed", "Status report reading & passive communication", 1.5, "=D10/40")
    ]
    w_data = weight_data_es if lang == 'ES' else weight_data_en
    for offset, row_info in enumerate(w_data):
        r_idx = 7 + offset
        c_code = ws3.cell(row=r_idx, column=2, value=row_info[0])
        c_desc = ws3.cell(row=r_idx, column=3, value=row_info[1])
        c_hours = ws3.cell(row=r_idx, column=4, value=row_info[2])
        c_factor = ws3.cell(row=r_idx, column=5, value=row_info[3])

        c_code.font = FONT_BOLD
        c_desc.font = FONT_REGULAR
        c_hours.font = FONT_BOLD
        c_factor.font = FONT_REGULAR

        for c in (c_code, c_desc, c_hours):
            c.border = BORDER_ALL_THIN
            c.fill = FILL_INPUT
            c.protection = Protection(locked=False) # Editable por usuario

        c_factor.border = BORDER_ALL_THIN
        c_factor.fill = FILL_FORMULA
        c_factor.protection = Protection(locked=True)
        c_factor.number_format = num_fmt_pct

        c_code.alignment = ALIGN_LEFT
        c_desc.alignment = ALIGN_LEFT
        c_hours.alignment = ALIGN_RIGHT
        c_factor.alignment = ALIGN_RIGHT
        c_hours.number_format = num_fmt_num

    # Sección 2: Tabla de Capacidad y Balance por Rol
    ws3.merge_cells("A13:K13")
    ws3["A13"] = "MATRIZ DE CAPACIDAD ASIGNADA, SATURACIÓN & SEMÁFORO DE RIESGO" if lang == 'ES' else "ASSIGNED WORKLOAD, CAPACITY SATURATION & RISK HEATMAP"
    ws3["A13"].font = FONT_TH
    ws3["A13"].fill = FILL_NAVY
    ws3["A13"].alignment = ALIGN_CENTER
    ws3["A13"].border = BORDER_ALL_THIN

    cap_headers_es = [
        "Código", "Rol / Departamento", "Hitos como A", "Hitos como R", "Hitos como C", "Hitos como I",
        "Carga Total (h)", "Capacidad (h)", "Saturación (%)", "Semáforo Operativo", "Veredicto"
    ]
    cap_headers_en = [
        "Code", "Role / Department", "Tasks as A", "Tasks as R", "Tasks as C", "Tasks as I",
        "Total Load (h)", "Capacity (h)", "Saturation (%)", "Operational Alert", "Verdict"
    ]
    cap_headers = cap_headers_es if lang == 'ES' else cap_headers_en
    for idx, ch in enumerate(cap_headers, start=1):
        c = ws3.cell(row=14, column=idx, value=ch)
        c.font = FONT_TH
        c.fill = FILL_NAVY_MED
        c.alignment = ALIGN_CENTER
        c.border = BORDER_ALL_THIN

    # Capacidades nominales base (horas mes o periodo de referencia de 160h)
    nominal_caps = [80.0, 160.0, 160.0, 320.0, 160.0, 160.0, 160.0, 80.0, 160.0]

    start_row_cap = 15
    for offset, r_name in enumerate(roles):
        r_idx = start_row_cap + offset
        role_code = f"ROL-{offset+1:02d}"
        col_letter_ws2 = get_column_letter(5 + offset) # E, F, G...

        c1 = ws3.cell(row=r_idx, column=1, value=role_code)
        c2 = ws3.cell(row=r_idx, column=2, value=r_name)

        c1.font = FONT_BOLD
        c1.alignment = ALIGN_CENTER
        c1.border = BORDER_ALL_THIN
        c1.fill = FILL_FORMULA
        c1.protection = Protection(locked=True)

        c2.font = FONT_BOLD
        c2.alignment = ALIGN_LEFT
        c2.border = BORDER_ALL_THIN
        c2.fill = FILL_INPUT
        c2.protection = Protection(locked=False) # Nombre editable

        # Fórmulas de recuento vinculadas a Pestaña 2
        f_cnt_a = f'=COUNTIF(\'{s2_name}\'!${col_letter_ws2}$7:${col_letter_ws2}$31, "A")'
        f_cnt_r = f'=COUNTIF(\'{s2_name}\'!${col_letter_ws2}$7:${col_letter_ws2}$31, "R")'
        f_cnt_c = f'=COUNTIF(\'{s2_name}\'!${col_letter_ws2}$7:${col_letter_ws2}$31, "C")'
        f_cnt_i = f'=COUNTIF(\'{s2_name}\'!${col_letter_ws2}$7:${col_letter_ws2}$31, "I")'

        for c_idx, formula in [(3, f_cnt_a), (4, f_cnt_r), (5, f_cnt_c), (6, f_cnt_i)]:
            c = ws3.cell(row=r_idx, column=c_idx, value=formula)
            c.font = FONT_REGULAR
            c.alignment = ALIGN_CENTER
            c.border = BORDER_ALL_THIN
            c.fill = FILL_FORMULA
            c.protection = Protection(locked=True)
            c.number_format = num_fmt_int

        # Carga Total (h) = C*w_A + D*w_R + E*w_C + F*w_I
        f_load = f'=(C{r_idx}*$D$7)+(D{r_idx}*$D$8)+(E{r_idx}*$D$9)+(F{r_idx}*$D$10)'
        c_load = ws3.cell(row=r_idx, column=7, value=f_load)
        c_load.font = FONT_BOLD
        c_load.alignment = ALIGN_RIGHT
        c_load.border = BORDER_ALL_THIN
        c_load.fill = FILL_FORMULA
        c_load.protection = Protection(locked=True)
        c_load.number_format = num_fmt_num

        # Capacidad Nominal (h) - Celda de entrada editable
        c_cap = ws3.cell(row=r_idx, column=8, value=nominal_caps[offset])
        c_cap.font = FONT_BOLD
        c_cap.alignment = ALIGN_RIGHT
        c_cap.border = BORDER_ALL_THIN
        c_cap.fill = FILL_INPUT
        c_cap.protection = Protection(locked=False)
        c_cap.number_format = num_fmt_num

        # Ratio de Saturación = Carga / Capacidad
        f_sat = f'=G{r_idx}/H{r_idx}'
        c_sat = ws3.cell(row=r_idx, column=9, value=f_sat)
        c_sat.font = FONT_BOLD
        c_sat.alignment = ALIGN_RIGHT
        c_sat.border = BORDER_ALL_THIN
        c_sat.fill = FILL_FORMULA
        c_sat.protection = Protection(locked=True)
        c_sat.number_format = num_fmt_pct

        # Semáforo de Riesgo
        if lang == 'ES':
            f_sem = f'=IF(I{r_idx}>1.0, "ROJO: Sobrecarga Crítica", IF(I{r_idx}>=0.8, "ÁMBAR: Alerta Límite", "VERDE: Carga Saludable"))'
            f_verd = f'=IF(I{r_idx}>1.0, "CUELLO DE BOTELLA", IF(I{r_idx}>=0.8, "RIESGO MEDIO", "SOSTENIBLE"))'
        else:
            f_sem = f'=IF(I{r_idx}>1.0, "RED: Critical Overload", IF(I{r_idx}>=0.8, "AMBER: High Risk", "GREEN: Healthy Load"))'
            f_verd = f'=IF(I{r_idx}>1.0, "BOTTLENECK", IF(I{r_idx}>=0.8, "MODERATE RISK", "SUSTAINABLE"))'

        c_sem = ws3.cell(row=r_idx, column=10, value=f_sem)
        c_sem.font = FONT_BOLD
        c_sem.alignment = ALIGN_CENTER
        c_sem.border = BORDER_ALL_THIN
        c_sem.fill = FILL_FORMULA
        c_sem.protection = Protection(locked=True)

        c_verd = ws3.cell(row=r_idx, column=11, value=f_verd)
        c_verd.font = FONT_REGULAR
        c_verd.alignment = ALIGN_CENTER
        c_verd.border = BORDER_ALL_THIN
        c_verd.fill = FILL_FORMULA
        c_verd.protection = Protection(locked=True)

    # Fila de Totales en fila 24
    tot_row = start_row_cap + len(roles)
    ws3.cell(row=tot_row, column=1, value="")
    ws3.cell(row=tot_row, column=2, value="TOTALES & PROMEDIOS" if lang == 'ES' else "TOTALS & AVERAGES")
    ws3.cell(row=tot_row, column=2).font = FONT_TH
    ws3.cell(row=tot_row, column=2).fill = FILL_NAVY
    ws3.cell(row=tot_row, column=2).alignment = ALIGN_LEFT

    for c_idx in range(3, 7):
        c = ws3.cell(row=tot_row, column=c_idx, value=f'=SUM({get_column_letter(c_idx)}15:{get_column_letter(c_idx)}23)')
        c.font = FONT_TH
        c.fill = FILL_NAVY_MED
        c.alignment = ALIGN_CENTER
        c.border = BORDER_ALL_THIN
        c.protection = Protection(locked=True)

    # Total Carga
    c_tot_load = ws3.cell(row=tot_row, column=7, value=f'=SUM(G15:G23)')
    c_tot_load.font = FONT_TH
    c_tot_load.fill = FILL_NAVY_MED
    c_tot_load.alignment = ALIGN_RIGHT
    c_tot_load.border = BORDER_ALL_THIN
    c_tot_load.number_format = num_fmt_num
    c_tot_load.protection = Protection(locked=True)

    # Total Capacidad
    c_tot_cap = ws3.cell(row=tot_row, column=8, value=f'=SUM(H15:H23)')
    c_tot_cap.font = FONT_TH
    c_tot_cap.fill = FILL_NAVY_MED
    c_tot_cap.alignment = ALIGN_RIGHT
    c_tot_cap.border = BORDER_ALL_THIN
    c_tot_cap.number_format = num_fmt_num
    c_tot_cap.protection = Protection(locked=True)

    # Ratio Global
    c_tot_sat = ws3.cell(row=tot_row, column=9, value=f'=G{tot_row}/H{tot_row}')
    c_tot_sat.font = FONT_TH
    c_tot_sat.fill = FILL_NAVY_MED
    c_tot_sat.alignment = ALIGN_RIGHT
    c_tot_sat.border = BORDER_ALL_THIN
    c_tot_sat.number_format = num_fmt_pct
    c_tot_sat.protection = Protection(locked=True)

    ws3.merge_cells(f"J{tot_row}:K{tot_row}")
    c_tot_lbl = ws3.cell(row=tot_row, column=10, value="CAPACIDAD TOTAL DEL EQUIPO" if lang == 'ES' else "OVERALL TEAM CAPACITY")
    c_tot_lbl.font = FONT_TH
    c_tot_lbl.fill = FILL_NAVY_MED
    c_tot_lbl.alignment = ALIGN_CENTER
    c_tot_lbl.border = BORDER_ALL_THIN

    # Formato condicional de Saturación en Columna I y Columna J
    range_sat = f"I15:I23"
    range_sem = f"J15:J23"
    ws3.conditional_formatting.add(range_sat, CellIsRule(operator='greaterThan', formula=['1.0'], fill=red_fill, font=red_font))
    ws3.conditional_formatting.add(range_sat, CellIsRule(operator='between', formula=['0.8', '1.0'], fill=amber_fill, font=amber_font))
    ws3.conditional_formatting.add(range_sat, CellIsRule(operator='lessThan', formula=['0.8'], fill=green_fill, font=green_font))

    sem_red = '"ROJO: Sobrecarga Crítica"' if lang == 'ES' else '"RED: Critical Overload"'
    sem_amb = '"ÁMBAR: Alerta Límite"' if lang == 'ES' else '"AMBER: High Risk"'
    sem_grn = '"VERDE: Carga Saludable"' if lang == 'ES' else '"GREEN: Healthy Load"'
    ws3.conditional_formatting.add(range_sem, CellIsRule(operator='equal', formula=[sem_red], fill=red_fill, font=red_font))
    ws3.conditional_formatting.add(range_sem, CellIsRule(operator='equal', formula=[sem_amb], fill=amber_fill, font=amber_font))
    ws3.conditional_formatting.add(range_sem, CellIsRule(operator='equal', formula=[sem_grn], fill=green_fill, font=green_font))

    # Anchos de columna ws3
    col_widths_ws3 = {
        'A': 10, 'B': 24, 'C': 14, 'D': 14, 'E': 14, 'F': 14,
        'G': 18, 'H': 16, 'I': 16, 'J': 26, 'K': 20
    }
    for col_l, w in col_widths_ws3.items():
        ws3.column_dimensions[col_l].width = w

    # =========================================================================
    # CONSTRUCCIÓN DE PESTAÑA 4: PLAN DE REBALANCEO & ACCIÓN
    # =========================================================================
    # Banner
    ws4.merge_cells("A1:J2")
    ws4["A1"] = "DATALARIA | " + ("PLAN EJECUTIVO DE REBALANCEO & MITIGACIÓN DE CUELLOS DE BOTELLA" if lang == 'ES' else "EXECUTIVE REBALANCING & BOTTLENECK MITIGATION PLAN")
    ws4["A1"].font = FONT_TITLE
    ws4["A1"].fill = FILL_NAVY
    ws4["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws4.merge_cells("A3:J3")
    ws4["A3"] = ("Registro de Decisiones Operativas: Reasignación de 'R', delegación de 'A' y racionalización de 'C' a 'I'." if lang == 'ES' else "Operational Action Registry: Reassignment of 'R', delegation of 'A', and streamlining 'C' to 'I'.")
    ws4["A3"].font = FONT_SUBTITLE
    ws4["A3"].fill = FILL_NAVY_MED
    ws4["A3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    headers_act_es = [
        "ID Acción", "Rol Afectado (Saturado)", "Entregable en Conflicto", "Implicación",
        "Acción de Gobernanza Propuesta", "Rol Receptor / Delegado", "Horas Liberadas",
        "Aprobador C-Level", "Fecha Límite", "Estado"
    ]
    headers_act_en = [
        "Action ID", "Saturated Role", "Conflicted Deliverable", "Involvement",
        "Governance Mitigation Action", "Receiving Role", "Freed Hours",
        "C-Level Approver", "Target Date", "Status"
    ]
    headers_act = headers_act_es if lang == 'ES' else headers_act_en

    for idx, ah in enumerate(headers_act, start=1):
        c = ws4.cell(row=5, column=idx, value=ah)
        c.font = FONT_TH
        c.fill = FILL_NAVY
        c.alignment = ALIGN_CENTER
        c.border = BORDER_ALL_THIN

    # Acciones precargadas de ejemplo realista
    actions_data_es = [
        ("ACT-01", "Tech Lead / Arq.", "WBS 3.1 - Cloud & Pipeline CI/CD", "R", "Delegar ejecución directa 'R' en DevOps y retener 'A' de supervisión", "Operaciones / DevOps", 26.0, "COO / Director PMO", "15/10/2026", "Aprobado"),
        ("ACT-02", "Tech Lead / Arq.", "WBS 3.3 - Desarrollo Frontend & Web", "C", "Degradar implicación 'C' a 'I' (Informed) para evitar parálisis de revisión", "Diseñador UX/UI", 5.0, "PMO Lead", "20/10/2026", "Aprobado"),
        ("ACT-03", "Project Manager", "WBS 1.2 - Matriz de Interesados", "A", "Transferir 'A' a Product Owner para concentrar PMO en control de hitos", "Product Owner", 12.0, "Comité Directivo", "25/10/2026", "En Proceso"),
        ("ACT-04", "Tech Lead / Arq.", "WBS 3.5 - Mapeo y Migración de Datos", "R", "Asignar desarrollo 'R' a Senior Backend Engineer con soporte externo", "Equipo Desarrollo", 26.0, "CTO / PMO", "30/10/2026", "Aprobado"),
        ("ACT-05", "QA & Testing", "WBS 4.1 - Plan Maestro de Pruebas", "R", "Designar formalmente ejecutor 'R' en el equipo de control de calidad", "QA & Testing", 26.0, "QA Lead", "05/11/2026", "Pendiente"),
        ("ACT-06", "", "", "", "", "", "", "", "", ""),
        ("ACT-07", "", "", "", "", "", "", "", "", ""),
        ("ACT-08", "", "", "", "", "", "", "", "", ""),
        ("ACT-09", "", "", "", "", "", "", "", "", ""),
        ("ACT-10", "", "", "", "", "", "", "", "", "")
    ]
    actions_data_en = [
        ("ACT-01", "Tech Lead / Arch.", "WBS 3.1 - Cloud & CI/CD Pipelines", "R", "Delegate direct execution 'R' to DevOps team while retaining 'A'", "Operations / DevOps", 26.0, "COO / PMO Director", "15/10/2026", "Approved"),
        ("ACT-02", "Tech Lead / Arch.", "WBS 3.3 - Frontend Portal & Web UI", "C", "Downgrade 'C' to 'I' (Informed) to prevent code review bottleneck", "UX/UI Designer", 5.0, "PMO Lead", "20/10/2026", "Approved"),
        ("ACT-03", "Project Manager", "WBS 1.2 - Stakeholder Matrix", "A", "Transfer 'A' to Product Owner to streamline PMO master tracking", "Product Owner", 12.0, "Steering Committee", "25/10/2026", "In Progress"),
        ("ACT-04", "Tech Lead / Arch.", "WBS 3.5 - Legacy Data Migration", "R", "Reassign 'R' to Senior Backend Engineer supported by external specialist", "Engineering Team", 26.0, "CTO / PMO", "30/10/2026", "Approved"),
        ("ACT-05", "QA & Testing", "WBS 4.1 - Master Test Plan", "R", "Formally assign 'R' to senior QA engineer to resolve orphan task", "QA & Testing", 26.0, "QA Lead", "05/11/2026", "Pending"),
        ("ACT-06", "", "", "", "", "", "", "", "", ""),
        ("ACT-07", "", "", "", "", "", "", "", "", ""),
        ("ACT-08", "", "", "", "", "", "", "", "", ""),
        ("ACT-09", "", "", "", "", "", "", "", "", ""),
        ("ACT-10", "", "", "", "", "", "", "", "", "")
    ]
    act_data = actions_data_es if lang == 'ES' else actions_data_en

    for offset, row_info in enumerate(act_data):
        r_idx = 6 + offset
        c1 = ws4.cell(row=r_idx, column=1, value=row_info[0]) # ID
        c1.font = FONT_BOLD
        c1.alignment = ALIGN_CENTER
        c1.border = BORDER_ALL_THIN
        c1.fill = FILL_FORMULA
        c1.protection = Protection(locked=True)

        for col_idx in range(2, 11):
            val = row_info[col_idx-1]
            c = ws4.cell(row=r_idx, column=col_idx, value=val)
            c.font = FONT_REGULAR
            c.border = BORDER_ALL_THIN
            c.fill = FILL_INPUT
            c.protection = Protection(locked=False) # Totalmente editable
            if col_idx in (4, 10):
                c.alignment = ALIGN_CENTER
            elif col_idx == 7:
                c.alignment = ALIGN_RIGHT
                c.number_format = num_fmt_num
            else:
                c.alignment = ALIGN_LEFT

    # Fila de Total de Horas Liberadas
    r_tot_act = 16
    ws4.merge_cells(f"A{r_tot_act}:F{r_tot_act}")
    ws4.cell(row=r_tot_act, column=1, value="TOTAL HORAS REBALANCEADAS" if lang == 'ES' else "TOTAL REBALANCED HOURS")
    ws4.cell(row=r_tot_act, column=1).font = FONT_TH
    ws4.cell(row=r_tot_act, column=1).fill = FILL_NAVY
    ws4.cell(row=r_tot_act, column=1).alignment = ALIGN_RIGHT

    c_sum_freed = ws4.cell(row=r_tot_act, column=7, value=f'=SUM(G6:G15)')
    c_sum_freed.font = FONT_TH
    c_sum_freed.fill = FILL_NAVY_MED
    c_sum_freed.alignment = ALIGN_RIGHT
    c_sum_freed.border = BORDER_ALL_THIN
    c_sum_freed.number_format = num_fmt_num
    c_sum_freed.protection = Protection(locked=True)

    ws4.merge_cells(f"H{r_tot_act}:J{r_tot_act}")
    ws4.cell(row=r_tot_act, column=8, value="IMPACTO ESTIMADO: +22% EFICIENCIA" if lang == 'ES' else "ESTIMATED IMPACT: +22% EFFICIENCY")
    ws4.cell(row=r_tot_act, column=8).font = FONT_TH
    ws4.cell(row=r_tot_act, column=8).fill = FILL_NAVY_MED
    ws4.cell(row=r_tot_act, column=8).alignment = ALIGN_CENTER
    ws4.cell(row=r_tot_act, column=8).border = BORDER_ALL_THIN

    col_widths_ws4 = {
        'A': 12, 'B': 22, 'C': 32, 'D': 12, 'E': 42,
        'F': 22, 'G': 16, 'H': 22, 'I': 14, 'J': 14
    }
    for col_l, w in col_widths_ws4.items():
        ws4.column_dimensions[col_l].width = w

    # =========================================================================
    # CONSTRUCCIÓN DE PESTAÑA 1: DASHBOARD EJECUTIVO
    # =========================================================================
    # Header Banner
    ws1.merge_cells("A1:M2")
    ws1["A1"] = "DATALARIA | " + ("DASHBOARD EJECUTIVO: GOBERNANZA RACI & CAPACIDAD OPERATIVA" if lang == 'ES' else "EXECUTIVE DASHBOARD: RACI GOVERNANCE & OPERATIONAL CAPACITY")
    ws1["A1"].font = FONT_TITLE
    ws1["A1"].fill = FILL_NAVY
    ws1["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws1.merge_cells("A3:M3")
    ws1["A3"] = ("Visión de Alto Nivel para CEOs, COOs y PMOs: Auditoría de rendición de cuentas y equilibrio de saturación." if lang == 'ES' else "High-Level Board Overview for CEOs, COOs & PMOs: Accountability audit & workload balance.")
    ws1["A3"].font = FONT_SUBTITLE
    ws1["A3"].fill = FILL_NAVY_MED
    ws1["A3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # TARJETAS KPI (Filas 5 a 7)
    kpis = [
        # (ColStart, ColEnd, Title, Formula, Format, Subtitle)
        (1, 3, "TOTAL ENTREGABLES WBS" if lang == 'ES' else "TOTAL WBS DELIVERABLES",
         f'=COUNTA(\'{s2_name}\'!C7:C31)', num_fmt_int, "Hitos en alcance activo" if lang == 'ES' else "Active scope milestones"),
        (4, 6, "SALUD DE GOBERNANZA" if lang == 'ES' else "GOVERNANCE HEALTH INDEX",
         f'=COUNTIF(\'{s2_name}\'!R7:R31, "OK")/COUNTA(\'{s2_name}\'!C7:C31)', num_fmt_pct, "Regla: 1 A y >= 1 R" if lang == 'ES' else "Rule: 1 A and >= 1 R"),
        (7, 9, "ROL MÁS SATURADO" if lang == 'ES' else "MAX SATURATED ROLE",
         f'=INDEX(\'{s3_name}\'!B15:B23, MATCH(MAX(\'{s3_name}\'!I15:I23), \'{s3_name}\'!I15:I23, 0))', "@", "Cuello de botella crítico" if lang == 'ES' else "Critical bottleneck"),
        (10, 12, "SATURACIÓN MÁXIMA" if lang == 'ES' else "PEAK SATURATION RATIO",
         f'=MAX(\'{s3_name}\'!I15:I23)', num_fmt_pct, "Umbral de riesgo > 100%" if lang == 'ES' else "Risk threshold > 100%")
    ]

    for c_start, c_end, title, f_val, fmt, sub in kpis:
        # Title box (row 5)
        ws1.merge_cells(start_row=5, start_column=c_start, end_row=5, end_column=c_end)
        c_t = ws1.cell(row=5, column=c_start, value=title)
        c_t.font = FONT_KPI_LBL
        c_t.fill = FILL_GRAY
        c_t.alignment = ALIGN_CENTER
        c_t.border = Border(top=THIN_SIDE, left=THIN_SIDE, right=THIN_SIDE)

        # Value box (row 6)
        ws1.merge_cells(start_row=6, start_column=c_start, end_row=6, end_column=c_end)
        c_v = ws1.cell(row=6, column=c_start, value=f_val)
        c_v.font = FONT_KPI_VAL_ACCENT if fmt != "@" else FONT_BOLD
        c_v.fill = FILL_INPUT
        c_v.alignment = ALIGN_CENTER
        c_v.number_format = fmt
        c_v.border = Border(left=THIN_SIDE, right=THIN_SIDE)
        c_v.protection = Protection(locked=True)

        # Subtitle box (row 7)
        ws1.merge_cells(start_row=7, start_column=c_start, end_row=7, end_column=c_end)
        c_s = ws1.cell(row=7, column=c_start, value=sub)
        c_s.font = FONT_KPI_SUB
        c_s.fill = FILL_GRAY
        c_s.alignment = ALIGN_CENTER
        c_s.border = Border(bottom=THIN_SIDE, left=THIN_SIDE, right=THIN_SIDE)

    # PANEL DE ALERTAS DE GOBERNANZA (A9 a E17)
    ws1.merge_cells("A9:E9")
    ws1["A9"] = "PANEL DE AUDITORÍA & ALERTAS DE GOBERNANZA" if lang == 'ES' else "GOVERNANCE AUDIT & ALERT PANEL"
    ws1["A9"].font = FONT_TH
    ws1["A9"].fill = FILL_NAVY
    ws1["A9"].alignment = ALIGN_CENTER
    ws1["A9"].border = BORDER_ALL_THIN

    audit_rows_es = [
        ("Entregables Huérfanos sin Accountable (A = 0)", f'=COUNTIF(\'{s2_name}\'!N7:N31, 0)', "Rojo / Crítico"),
        ("Entregables con Accountable Múltiple (A > 1)", f'=COUNTIF(\'{s2_name}\'!N7:N31, ">1")', "Rojo / Crítico"),
        ("Entregables Huérfanos sin Responsible (R = 0)", f'=COUNTIF(\'{s2_name}\'!O7:O31, 0)', "Ámbar / Alerta"),
        ("Entregables con Exceso de Consultados (C >= 4)", f'=COUNTIF(\'{s2_name}\'!P7:P31, ">=4")', "Ámbar / Sobrecarga"),
        ("Entregables 100% Conformes con Regla Áurea", f'=COUNTIF(\'{s2_name}\'!R7:R31, "OK")', "Verde / Conforme"),
        ("TOTAL ANOMALÍAS DETECTADAS", f'=B10+B11+B12', "Acción Requerida")
    ]
    audit_rows_en = [
        ("Orphan Tasks without Accountable (A = 0)", f'=COUNTIF(\'{s2_name}\'!N7:N31, 0)', "Red / Critical"),
        ("Tasks with Multiple Diluted Accountables (A > 1)", f'=COUNTIF(\'{s2_name}\'!N7:N31, ">1")', "Red / Critical"),
        ("Tasks without Responsible Executor (R = 0)", f'=COUNTIF(\'{s2_name}\'!O7:O31, 0)', "Amber / Warning"),
        ("Tasks with Excessive Consultation (C >= 4)", f'=COUNTIF(\'{s2_name}\'!P7:P31, ">=4")', "Amber / Overload"),
        ("Deliverables 100% Fully Compliant with Golden Rule", f'=COUNTIF(\'{s2_name}\'!R7:R31, "OK")', "Green / Compliant"),
        ("TOTAL GOVERNANCE ANOMALIES DETECTED", f'=B10+B11+B12', "Action Required")
    ]
    a_rows = audit_rows_es if lang == 'ES' else audit_rows_en

    for idx, (label, form, alert_level) in enumerate(a_rows, start=10):
        ws1.merge_cells(f"A{idx}:C{idx}")
        c_lbl = ws1.cell(row=idx, column=1, value=label)
        c_lbl.font = FONT_BOLD if idx == 15 else FONT_REGULAR
        c_lbl.fill = FILL_GRAY if idx != 15 else FILL_NAVY_MED
        c_lbl.alignment = ALIGN_LEFT
        c_lbl.border = BORDER_ALL_THIN
        if idx == 15:
            c_lbl.font = FONT_TH

        c_val = ws1.cell(row=idx, column=4, value=form)
        c_val.font = FONT_BOLD
        c_val.fill = FILL_INPUT if idx != 15 else FILL_NAVY_MED
        c_val.alignment = ALIGN_CENTER
        c_val.border = BORDER_ALL_THIN
        c_val.number_format = num_fmt_int
        c_val.protection = Protection(locked=True)
        if idx == 15:
            c_val.font = FONT_TH

        c_stat = ws1.cell(row=idx, column=5, value=alert_level)
        c_stat.font = FONT_MUTED
        c_stat.fill = FILL_GRAY if idx != 15 else FILL_NAVY_MED
        c_stat.alignment = ALIGN_CENTER
        c_stat.border = BORDER_ALL_THIN
        if idx == 15:
            c_stat.font = FONT_TH

    # TABLA RESUMEN DE SATURACIÓN POR ROL (G9 a L19)
    ws1.merge_cells("G9:L9")
    ws1["G9"] = "EQUILIBRIO DE CARGA POR ROL / DEPARTAMENTO" if lang == 'ES' else "WORKLOAD BALANCE PER ROLE / DEPARTMENT"
    ws1["G9"].font = FONT_TH
    ws1["G9"].fill = FILL_BLUE
    ws1["G9"].alignment = ALIGN_CENTER
    ws1["G9"].border = BORDER_ALL_THIN

    dash_th = ["Rol / Departamento", "Carga (h)", "Capacidad (h)", "Saturación", "Semáforo", "Estado"] if lang == 'ES' else ["Role / Department", "Load (h)", "Capacity (h)", "Saturation", "Alert", "Status"]
    for idx, th in enumerate(dash_th, start=7):
        c = ws1.cell(row=10, column=idx, value=th)
        c.font = FONT_TH
        c.fill = FILL_NAVY_MED
        c.alignment = ALIGN_CENTER
        c.border = BORDER_ALL_THIN

    for idx, r_name in enumerate(roles, start=11):
        cap_row = 15 + (idx - 11)
        c1 = ws1.cell(row=idx, column=7, value=f'=\'{s3_name}\'!B{cap_row}')
        c2 = ws1.cell(row=idx, column=8, value=f'=\'{s3_name}\'!G{cap_row}')
        c3 = ws1.cell(row=idx, column=9, value=f'=\'{s3_name}\'!H{cap_row}')
        c4 = ws1.cell(row=idx, column=10, value=f'=\'{s3_name}\'!I{cap_row}')
        c5 = ws1.cell(row=idx, column=11, value=f'=\'{s3_name}\'!J{cap_row}')
        c6 = ws1.cell(row=idx, column=12, value=f'=\'{s3_name}\'!K{cap_row}')

        c1.font = FONT_REGULAR
        c1.alignment = ALIGN_LEFT
        c2.font = FONT_REGULAR
        c2.alignment = ALIGN_RIGHT
        c2.number_format = num_fmt_num
        c3.font = FONT_REGULAR
        c3.alignment = ALIGN_RIGHT
        c3.number_format = num_fmt_num
        c4.font = FONT_BOLD
        c4.alignment = ALIGN_RIGHT
        c4.number_format = num_fmt_pct
        c5.font = FONT_BOLD
        c5.alignment = ALIGN_CENTER
        c6.font = FONT_MUTED
        c6.alignment = ALIGN_CENTER

        for c in (c1, c2, c3, c4, c5, c6):
            c.border = BORDER_ALL_THIN
            c.fill = FILL_FORMULA
            c.protection = Protection(locked=True)

    # Formato condicional de saturación en Dashboard (J11:J19)
    ws1.conditional_formatting.add("J11:J19", CellIsRule(operator='greaterThan', formula=['1.0'], fill=red_fill, font=red_font))
    ws1.conditional_formatting.add("J11:J19", CellIsRule(operator='between', formula=['0.8', '1.0'], fill=amber_fill, font=amber_font))
    ws1.conditional_formatting.add("J11:J19", CellIsRule(operator='lessThan', formula=['0.8'], fill=green_fill, font=green_font))

    # GRÁFICO NATIVO DE EXCEL DE BARRAS (Carga vs Capacidad)
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Carga de Trabajo Asignada vs. Capacidad Nominal (Horas)" if lang == 'ES' else "Assigned Workload vs. Nominal Capacity (Hours)"
    chart.y_axis.title = "Horas" if lang == 'ES' else "Hours"
    chart.x_axis.title = "Roles Operativos" if lang == 'ES' else "Operational Roles"
    chart.height = 14
    chart.width = 23

    # Datos desde la Pestaña 3: Balance de Carga
    # Col G es Carga (col 7), Col H es Capacidad (col 8)
    data = Reference(ws3, min_col=7, min_row=14, max_col=8, max_row=23)
    chart.add_data(data, titles_from_data=True)

    # Configuración explícita de categorías como StrRef con StrData cacheado
    cat_formula = f"'{s3_name}'!$B$15:$B$23"
    sdata = StrData(ptCount=len(roles), pt=[StrVal(idx=i, v=r_name) for i, r_name in enumerate(roles)])
    sref = StrRef(f=cat_formula, strCache=sdata)
    for s in chart.series:
        s.cat = AxDataSource(strRef=sref)

    # Configuración estricta de ejes: posición inferior y etiquetas visibles
    chart.x_axis.axPos = "b"       # Posición inferior (bottom)
    chart.x_axis.tickLblPos = "nextTo" # Etiquetas de categoría junto al eje (visibles)
    chart.x_axis.delete = False    # Asegurar que el eje no se suprima
    chart.y_axis.axPos = "l"       # Posición izquierda (left)
    chart.y_axis.tickLblPos = "nextTo"
    chart.y_axis.delete = False
    chart.legend.legendPos = "r"

    # Ubicación del gráfico en Dashboard
    ws1.add_chart(chart, "A19")

    # Anchos de columnas en Dashboard
    col_widths_ws1 = {
        'A': 12, 'B': 14, 'C': 14, 'D': 14, 'E': 14, 'F': 14,
        'G': 24, 'H': 14, 'I': 14, 'J': 14, 'K': 24, 'L': 18, 'M': 10
    }
    for col_l, w in col_widths_ws1.items():
        ws1.column_dimensions[col_l].width = w

    # =========================================================================
    # APLICACIÓN DE PROTECCIÓN ESTRICTA OPENXML ECMA-376
    # =========================================================================
    for ws in [ws1, ws2, ws3, ws4]:
        apply_sheet_protection(ws)

    return wb


def main():
    base_dir = "packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga"
    dir_es = os.path.join(base_dir, "[ES]_Matriz_RACI_Balance_Carga")
    dir_en = os.path.join(base_dir, "[EN]_Quantitative_RACI_Workload")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    file_es = os.path.join(dir_es, "Matriz_RACI_Balance_Carga_ES.xlsx")
    file_en = os.path.join(dir_en, "Quantitative_RACI_Workload_EN.xlsx")

    print("[1/2] Generando modelo Excel en Español...")
    wb_es = build_raci_workbook(lang='ES')
    wb_es.save(file_es)
    print(f"  -> Guardado exitosamente: {file_es}")

    print("[2/2] Generando modelo Excel en Inglés...")
    wb_en = build_raci_workbook(lang='EN')
    wb_en.save(file_en)
    print(f"  -> Guardado exitosamente: {file_en}")


if __name__ == "__main__":
    main()
