#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los activos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga/Executive_Decision_Pack_RACI_Dual.zip
- Copia directa en packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_RACI_Dual.zip

Estructura del archivo ZIP:
- [ES]_Matriz_RACI_Balance_Carga/
  - Matriz_RACI_Balance_Carga_ES.xlsx
  - Presentacion_RACI_CLevel_ES.pptx
  - Guia_Metodologica_RACI_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- [EN]_Quantitative_RACI_Workload/
  - Quantitative_RACI_Workload_EN.xlsx
  - Deck_RACI_CLevel_EN.pptx
  - Methodology_Guide_RACI_EN.pdf
  - README_INSTRUCTIONS.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- LEEME_ACCESO_GOOGLE_SHEETS.txt (en la raíz del ZIP)
- README_GOOGLE_SHEETS_ACCESS.txt (en la raíz del ZIP)

SEGURIDAD ESTRICTA:
Queda terminantemente prohibido almacenar o sincronizar archivos a static/downloads/
o public/downloads/. Todos los activos quedan alojados exclusivamente en packages/.
"""

import os
import sys
import zipfile
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DIR_PACK = "packages/Suite_03_Control_Operativo/01_Matriz_RACI_Balance_Carga"
DIR_ES = os.path.join(DIR_PACK, "[ES]_Matriz_RACI_Balance_Carga")
DIR_EN = os.path.join(DIR_PACK, "[EN]_Quantitative_RACI_Workload")
DIR_LEMON = "packages/00_DISTRIBUCION_LEMONSQUEEZY"

ZIP_NAME = "Executive_Decision_Pack_RACI_Dual.zip"
ZIP_PATH_LOCAL = os.path.join(DIR_PACK, ZIP_NAME)
ZIP_PATH_LEMON = os.path.join(DIR_LEMON, ZIP_NAME)

PASSWORD_OFFICIAL = "Datalaria2026"
SUPPORT_EMAIL = "datalaria@gmail.com"

LEEME_INSTRUCCIONES_ES = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Matriz RACI Cuantitativa & Balance de Carga Operativa
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas de consultoría estratégica y dirección de PMO
de estándar Tier-1 (PMBOK 7ª Edición / PRINCE2 / McKinsey Operations Practice)
está diseñado específicamente para Directores de Operaciones (COO), Directores
de PMO, Project Managers, Tech Leads y Comités de Dirección (Executive Committee).

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Matriz_RACI_Balance_Carga_ES.xlsx
  Libro de trabajo analítico en Excel con 4 pestañas estructuradas e interconectadas:
  - Pestaña 1: Dashboard Ejecutivo (Cabecera directiva, 4 KPI Cards de Gobernanza,
               Panel de Alertas de Auditoría, Tabla Resumen de Saturación y Gráfico
               dinámico de barras Carga Asignada vs. Capacidad Nominal).
  - Pestaña 2: Matriz RACI & Gobernanza (25 entregables estructurados en 5 fases WBS,
               9 roles transversales configurables, recuentos automáticos de R/A/C/I,
               columna de Estado de Gobernanza con fórmulas de verificación estricta
               y formato condicional multicromático).
  - Pestaña 3: Balance de Carga (Tabla de parametrización de horas base por tipo de
               implicación A/R/C/I, matriz de cálculo de carga ponderada, capacidades
               nominales por rol, ratio de saturación % y semáforo de riesgo operativo).
  - Pestaña 4: Plan de Rebalanceo (Registro formal de mitigación de sobrecargas:
               delegación de 'R', reasignación de 'A', degradación de 'C' a 'I',
               horas liberadas, aprobador directivo y seguimiento de estado).

• Presentacion_RACI_CLevel_ES.pptx
  Presentación ejecutiva panorámica (16:9 widescreen) bajo la Pirámide de Minto (3 diapositivas):
  - Diapositiva 1: Diagnóstico de Gobernanza & Salud Operativa (4 KPI Cards y diagnóstico de PMO).
  - Diapositiva 2: Organigrama Funcional Matricial & Mapa de Sobrecarga (Estructura y gráfico de saturación).
  - Diapositiva 3: Roadmap de Rebalanceo en 4 Fases & Board Decision Gateway (4 resoluciones formales y firmas).

• Guia_Metodologica_RACI_ES.pdf
  Guía metodológica oficial de 5 páginas con la fundamentación matemática del modelo
  cuantitativo, principios de unicidad de Accountable y ejecución mínima, modelo de carga
  compuesta, índice de Gini organizacional, catálogo de patologías y protocolo de defensa en comité.

--------------------------------------------------------------------------------
2. POLÍTICA DE PROTECCIÓN DE CELDAS & CONTRASEÑA OFICIAL
--------------------------------------------------------------------------------
Para garantizar la integridad matemática del modelo y evitar sobreescrituras accidentales
en fórmulas de auditoría, las hojas del libro de Excel se entregan protegidas bajo el
estándar OpenXML ECMA-376:

• CELDAS DE ENTRADA (Fondo Blanco #FFFFFF):
  Completamente desbloqueadas. Puede editar nombres de tareas, fases, asignaciones RACI,
  roles, capacidades nominales, baremos de horas y registros del plan de acción.

• CELDAS DE FÓRMULAS & CABECERAS (Fondo Gris #F1F5F9 o Corporativo):
  Protegidas contra modificaciones involuntarias.

• CONTRASEÑA OFICIAL DE DESPROTECCIÓN:
  {PASSWORD_OFFICIAL}

  Para desproteger cualquier hoja en Microsoft Excel:
  Pestaña "Revisar" -> "Desproteger hoja" -> Introducir: {PASSWORD_OFFICIAL}

--------------------------------------------------------------------------------
3. SOPORTE TÉCNICO & CONSULTAS
--------------------------------------------------------------------------------
Si tiene alguna duda sobre la parametrización de sus proyectos o requiere soporte:
• Email de soporte: {SUPPORT_EMAIL}
• Web oficial: https://datalaria.com
"""

README_INSTRUCTIONS_EN = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Quantitative RACI Matrix & Operational Workload Balancing
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This corporate strategy and PMO leadership toolkit meets Tier-1 standards
(PMBOK 7th Edition / PRINCE2 / McKinsey Operations Practice) and is specifically
tailored for Chief Operating Officers (COO), PMO Directors, Project Managers,
Tech Leads, and Corporate Executive Committees.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Quantitative_RACI_Workload_EN.xlsx
  Analytical Excel workbook featuring 4 structured and interconnected worksheets:
  - Sheet 1: Executive Dashboard (C-Level header, 4 Governance KPI Cards, Audit
             Alert Panel, Role Saturation Summary Table, and dynamic Bar Chart
             comparing Allocated Workload vs. Nominal Capacity).
  - Sheet 2: RACI Matrix & Governance (25 deliverables across 5 WBS phases, 9
             customizable cross-functional roles, automated R/A/C/I counters,
             Governance Status verification formulas, and conditional formatting).
  - Sheet 3: Workload Balancing (Effort weighting calibration table for A/R/C/I,
             composite workload engine, nominal capacity per role, saturation
             ratios %, and operational risk heatmap).
  - Sheet 4: Rebalancing Plan (Formal operational mitigation log: 'R' delegation,
             'A' reallocation, streamlining 'C' to 'I', freed capacity hours,
             C-Level approver, and milestone tracking).

• Deck_RACI_CLevel_EN.pptx
  Executive 16:9 widescreen presentation structured under the Minto Pyramid (3 slides):
  - Slide 1: Governance Diagnosis & Operational Health (4 KPI Cards and PMO audit findings).
  - Slide 2: Cross-Functional Matrix Org Chart & Workload Heatmap (Structure and chart).
  - Slide 3: 4-Phase Rebalancing Roadmap & Board Decision Gateway (4 binding resolutions and signatures).

• Methodology_Guide_RACI_EN.pdf
  Official 5-page editorial methodology guide detailing mathematical foundations,
  single accountability invariance, active execution mandate, composite workload
  formula, organizational Gini coefficient, pathology catalog, and boardroom defense FAQ.

--------------------------------------------------------------------------------
2. CELL PROTECTION POLICY & OFFICIAL PASSWORD
--------------------------------------------------------------------------------
To safeguard mathematical integrity and prevent accidental formula corruption,
worksheets are protected according to ECMA-376 OpenXML standards:

• INPUT CELLS (White Fill #FFFFFF):
  Fully unlocked. You can freely edit task names, phases, RACI assignments, role titles,
  nominal capacities, effort weights, and action plan fields.

• FORMULA & HEADER CELLS (Gray Fill #F1F5F9 or Corporate Navy):
  Protected against inadvertent modifications.

• OFFICIAL UNPROTECT PASSWORD:
  {PASSWORD_OFFICIAL}

  To unprotect any worksheet in Microsoft Excel:
  "Review" Tab -> "Unprotect Sheet" -> Enter: {PASSWORD_OFFICIAL}

--------------------------------------------------------------------------------
3. TECHNICAL SUPPORT & INQUIRIES
--------------------------------------------------------------------------------
For customization questions or enterprise assistance:
• Support Email: {SUPPORT_EMAIL}
• Official Website: https://datalaria.com
"""

LEEME_GOOGLE_SHEETS_ES = """================================================================================
DATALARIA | INSTRUCCIONES DE IMPORTACIÓN A GOOGLE SHEETS
================================================================================

El libro de trabajo oficial en Excel (.xlsx) ha sido auditado para ofrecer
compatibilidad nativa al 100% con Google Sheets sin requerir plugins ni macros:

PASOS PARA ABRIR EN GOOGLE SHEETS:
1. Abra Google Drive (drive.google.com).
2. Haga clic en "+ Nuevo" -> "Subir archivo".
3. Seleccione el archivo "Matriz_RACI_Balance_Carga_ES.xlsx" (o la versión en inglés).
4. Haga doble clic en el archivo subido en Google Drive.
5. Haga clic en el botón superior "Abrir con Hojas de cálculo de Google".
6. ¡Listo! Todas las fórmulas (COUNTIF, INDEX, MATCH, IF, AND) y el formato
   condicional funcionarán de forma fluida y en tiempo real.

Soporte: datalaria@gmail.com
"""

README_GOOGLE_SHEETS_EN = """================================================================================
DATALARIA | GOOGLE SHEETS IMPORT INSTRUCTIONS
================================================================================

The official Excel workbook (.xlsx) has been verified for 100% native compatibility
with Google Sheets without requiring third-party plugins or VBA macros:

STEPS TO OPEN IN GOOGLE SHEETS:
1. Open Google Drive (drive.google.com).
2. Click "+ New" -> "File upload".
3. Select "Quantitative_RACI_Workload_EN.xlsx" (or the Spanish version).
4. Double-click the uploaded file in Google Drive.
5. Click the top button "Open with Google Sheets".
6. Completed! All formulas (COUNTIF, INDEX, MATCH, IF, AND) and conditional
   formatting rules will recalculate seamlessly in real time.

Support: datalaria@gmail.com
"""


def create_instruction_files():
    """Genera los archivos de texto de soporte e instrucciones."""
    # En [ES]
    path_es = os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt")
    with open(path_es, "w", encoding="utf-8") as f:
        f.write(LEEME_INSTRUCCIONES_ES)
    print(f"  -> Creado: {path_es}")

    # En [EN]
    path_en = os.path.join(DIR_EN, "README_INSTRUCTIONS.txt")
    with open(path_en, "w", encoding="utf-8") as f:
        f.write(README_INSTRUCTIONS_EN)
    print(f"  -> Creado: {path_en}")

    # En la raíz del paquete
    path_gs_es = os.path.join(DIR_PACK, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
    with open(path_gs_es, "w", encoding="utf-8") as f:
        f.write(LEEME_GOOGLE_SHEETS_ES)
    print(f"  -> Creado: {path_gs_es}")

    path_gs_en = os.path.join(DIR_PACK, "README_GOOGLE_SHEETS_ACCESS.txt")
    with open(path_gs_en, "w", encoding="utf-8") as f:
        f.write(README_GOOGLE_SHEETS_EN)
    print(f"  -> Creado: {path_gs_en}")


def build_master_zip():
    """Construye el archivo ZIP maestro y lo copia al directorio de Lemon Squeezy."""
    print("\n[1/3] Generando archivos de documentación de texto...")
    create_instruction_files()

    print("\n[2/3] Empaquetando Executive_Decision_Pack_RACI_Dual.zip...")
    os.makedirs(DIR_LEMON, exist_ok=True)

    files_to_pack = [
        # Subcarpeta ES
        (os.path.join(DIR_ES, "Matriz_RACI_Balance_Carga_ES.xlsx"), "[ES]_Matriz_RACI_Balance_Carga/Matriz_RACI_Balance_Carga_ES.xlsx"),
        (os.path.join(DIR_ES, "Presentacion_RACI_CLevel_ES.pptx"), "[ES]_Matriz_RACI_Balance_Carga/Presentacion_RACI_CLevel_ES.pptx"),
        (os.path.join(DIR_ES, "Guia_Metodologica_RACI_ES.pdf"), "[ES]_Matriz_RACI_Balance_Carga/Guia_Metodologica_RACI_ES.pdf"),
        (os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt"), "[ES]_Matriz_RACI_Balance_Carga/LEEME_INSTRUCCIONES.txt"),
        
        # Subcarpeta EN
        (os.path.join(DIR_EN, "Quantitative_RACI_Workload_EN.xlsx"), "[EN]_Quantitative_RACI_Workload/Quantitative_RACI_Workload_EN.xlsx"),
        (os.path.join(DIR_EN, "Deck_RACI_CLevel_EN.pptx"), "[EN]_Quantitative_RACI_Workload/Deck_RACI_CLevel_EN.pptx"),
        (os.path.join(DIR_EN, "Methodology_Guide_RACI_EN.pdf"), "[EN]_Quantitative_RACI_Workload/Methodology_Guide_RACI_EN.pdf"),
        (os.path.join(DIR_EN, "README_INSTRUCTIONS.txt"), "[EN]_Quantitative_RACI_Workload/README_INSTRUCTIONS.txt"),

        # Raíz
        (os.path.join(DIR_PACK, "LEEME_ACCESO_GOOGLE_SHEETS.txt"), "LEEME_ACCESO_GOOGLE_SHEETS.txt"),
        (os.path.join(DIR_PACK, "README_GOOGLE_SHEETS_ACCESS.txt"), "README_GOOGLE_SHEETS_ACCESS.txt")
    ]

    with zipfile.ZipFile(ZIP_PATH_LOCAL, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for src, arcname in files_to_pack:
            if not os.path.exists(src):
                raise FileNotFoundError(f"Archivo requerido no encontrado: {src}")
            zf.write(src, arcname)
            print(f"  + Añadido al ZIP: {arcname}")

    print(f"\n  -> ZIP Maestro creado con éxito: {ZIP_PATH_LOCAL}")

    print("\n[3/3] Copiando ZIP a packages/00_DISTRIBUCION_LEMONSQUEEZY/...")
    shutil.copy2(ZIP_PATH_LOCAL, ZIP_PATH_LEMON)
    print(f"  -> Copia de distribución completada: {ZIP_PATH_LEMON}")

    # Verificación de contenido del ZIP
    print("\n--- VERIFICACIÓN DEL CONTENIDO DEL ARCHIVO ZIP ---")
    with zipfile.ZipFile(ZIP_PATH_LOCAL, 'r') as zf:
        for info in zf.infolist():
            print(f"  - {info.filename} ({info.file_size:,} bytes)")


if __name__ == "__main__":
    build_master_zip()
