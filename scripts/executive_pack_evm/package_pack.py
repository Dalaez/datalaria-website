#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los activos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial privada en Lemon Squeezy:
- packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado/Executive_Decision_Pack_EVM_Dual.zip
- Copia directa en packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_EVM_Dual.zip

Estructura del archivo ZIP:
- [ES]_Cuadro_EVM_Valor_Ganado/
  - Cuadro_Mando_EVM_Datalaria_ES.xlsx
  - Presentacion_EVM_CLevel_ES.pptx
  - Guia_Metodologica_EVM_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- [EN]_Earned_Value_Management_EVM/
  - EVM_Dashboard_Datalaria_EN.xlsx
  - Deck_EVM_CLevel_EN.pptx
  - Methodology_Guide_EVM_EN.pdf
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

DIR_PACK = "packages/Suite_03_Control_Operativo/04_Cuadro_EVM_Valor_Ganado"
DIR_ES = os.path.join(DIR_PACK, "[ES]_Cuadro_EVM_Valor_Ganado")
DIR_EN = os.path.join(DIR_PACK, "[EN]_Earned_Value_Management_EVM")
DIR_LEMON = "packages/00_DISTRIBUCION_LEMONSQUEEZY"

ZIP_NAME = "Executive_Decision_Pack_EVM_Dual.zip"
ZIP_PATH_LOCAL = os.path.join(DIR_PACK, ZIP_NAME)
ZIP_PATH_LEMON = os.path.join(DIR_LEMON, ZIP_NAME)

PASSWORD_OFFICIAL = "Datalaria2026"
SUPPORT_EMAIL = "datalaria@gmail.com"

LEEME_INSTRUCCIONES_ES = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Cuadro de Mando EVM: Valor Ganado, Curva S & Proyecciones EAC
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas analíticas de grado directivo y de consultoría Tier-1
(estándar ANSI/EIA-748 / PMBOK / Project Finance) está diseñado específicamente
para Directores Generales (CEO), Directores Financieros (CFO), Directores de Operaciones (COO),
Directores de Oficina de Proyectos (PMO) y Comités de Dirección e Inversión.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Cuadro_Mando_EVM_Datalaria_ES.xlsx
  Libro de trabajo analítico en Excel con 4 pestañas funcionales estructuradas:
  - Pestaña 1: Dashboard Ejecutivo EVM (Tarjetas KPI C-Level: BAC, AC, EV, PV, CV, SV,
               CPI, SPI, EAC, VAC, TCPI; matriz de salud operativa 2x2 y gráfico
               nativo de la Curva S con trazado multi-serie y proyección).
  - Pestaña 2: Control WBS & Entregables (Registro de 25 paquetes de trabajo WBS en 5 fases,
               entradas de usuario desbloqueadas para BAC, % Avance Real Físico, PV y AC;
               cálculo automático de EV, varianzas CV/SV e índices CPI/SPI con semáforos).
  - Pestaña 3: Serie Temporal & Proyecciones (Evolución de 12 meses con corte en Mes 6,
               comparativa de los 3 modelos matemáticos EAC: Típico, Atípico y Compuesto;
               análisis de viabilidad del índice para completar TCPI).
  - Pestaña 4: Plan de Acción & Recuperación (Matriz de 8 iniciativas de intervención:
               Crashing, Fast-Tracking, Descope negociado, responsables C-Level e impacto delta).

• Presentacion_EVM_CLevel_ES.pptx
  Presentación panorámica (16:9 widescreen) estructurada bajo la Pirámide de Minto (3 slides):
  - Diapositiva 1: Diagnóstico Ejecutivo de Salud Financiera & Plazos (4 KPI Cards y contraste
                   entre la trampa contable tradicional y el diagnóstico EVM).
  - Diapositiva 2: Curva S Ejecutiva & Análisis de Varianzas por Entregable (Gráfico de alta
                   resolución, fecha de corte Mes 6 y ranking Pareto del 75% del sobrecoste).
  - Diapositiva 3: Plan de Recuperación, Opciones de Descope & Board Decision Gateway con
                   4 resoluciones vinculantes y firmas de aprobación (CEO, CFO, COO, PMO).

• Guia_Metodologica_EVM_ES.pdf
  Guía metodológica oficial de 5 páginas con la fundamentación matemática de ANSI/EIA-748,
  reglas objetivas de imputación de avance físico (0/100, 50/50, hitos), caso de estudio
  corporativo de rescate de 1.2M € y protocolo de defensa en comité (Boardroom FAQ).

--------------------------------------------------------------------------------
2. POLÍTICA DE PROTECCIÓN DE CELDAS & CONTRASEÑA OFICIAL
--------------------------------------------------------------------------------
Para garantizar la integridad matemática del modelo y evitar sobreescrituras accidentales
en fórmulas financieras y de proyección, las hojas del libro de Excel se entregan
protegidas bajo el estándar OpenXML ECMA-376:

• CELDAS DE ENTRADA (Fondo Blanco #FFFFFF):
  Completamente desbloqueadas. Puede editar libremente presupuestos BAC, porcentajes de avance
  físico real, costes incurridos AC, series mensuales y medidas correctivas.

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
Earned Value Management (EVM) Dashboard: S-Curve & EAC Forecasting
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite of Tier-1 executive analytical tools (ANSI/EIA-748 / PMBOK / Project Finance standards)
is purpose-built for Chief Executive Officers (CEO), Chief Financial Officers (CFO),
Chief Operating Officers (COO), PMO Directors, and Executive Investment Boards.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• EVM_Dashboard_Datalaria_EN.xlsx
  Comprehensive Excel workbook with 4 structured functional tabs:
  - Tab 1: Executive EVM Dashboard (C-Level KPI Cards: BAC, AC, EV, PV, CV, SV,
           CPI, SPI, EAC, VAC, TCPI; 2x2 operational health matrix and native S-Curve
           chart with multi-series tracking and forecast lines).
  - Tab 2: WBS & Deliverables Tracking (25 work package register across 5 phases,
           unlocked user inputs for BAC, % Physical Progress, PV and AC;
           automated EV calculation, CV/SV variances, and individual CPI/SPI indices).
  - Tab 3: Time Series & EAC Forecasting (12-month trajectory with Month 6 cutoff,
           mathematical comparison of 3 EAC models: Typical, Atypical & Combined;
           To-Complete Performance Index TCPI feasibility assessment).
  - Tab 4: Action & Recovery Plan (8-initiative corrective matrix: Crashing, Fast-Tracking,
           negotiated descope, C-Level owners, and projected delta CPI/SPI impact).

• Deck_EVM_CLevel_EN.pptx
  Executive 16:9 widescreen presentation following Minto Pyramid structure (3 slides):
  - Slide 1: Executive Financial Health & Schedule Diagnosis (4 KPI Cards and the traditional
             accounting trap vs EVM clarity).
  - Slide 2: Executive S-Curve & Deliverable Variance Analysis (High-res chart, cutoff date,
             and Pareto ranking of the top 3 overrun root causes).
  - Slide 3: Recovery Roadmap, Descope Levers & Board Decision Gateway with 4 binding
             resolutions and formal sign-off boxes (CEO, CFO, COO, PMO).

• Methodology_Guide_EVM_EN.pdf
  Official 5-page editorial methodology guide covering ANSI/EIA-748 mathematical foundations,
  objective physical progress crediting rules (0/100, 50/50, weighted milestones),
  $1.2M enterprise turnaround case study, and boardroom defense FAQ.

--------------------------------------------------------------------------------
2. CELL PROTECTION POLICY & OFFICIAL PASSWORD
--------------------------------------------------------------------------------
To safeguard mathematical integrity and prevent accidental formula corruption,
worksheets are protected according to ECMA-376 OpenXML standards:

• INPUT CELLS (White Fill #FFFFFF):
  Fully unlocked. You can freely edit task BACs, physical percent complete,
  actual costs incurred AC, monthly time series, and recovery actions.

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
3. Seleccione el archivo "Cuadro_Mando_EVM_Datalaria_ES.xlsx" (o la versión en inglés).
4. Haga doble clic en el archivo subido en Google Drive.
5. Haga clic en el botón superior "Abrir con Hojas de cálculo de Google".
6. ¡Listo! Todas las fórmulas analíticas (SUM, IF, AND, TEXT, multiplicaciones y ratios)
   y los gráficos de la Curva S funcionarán de forma fluida y en tiempo real.

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
3. Select "EVM_Dashboard_Datalaria_EN.xlsx" (or the Spanish version).
4. Double-click the uploaded file in Google Drive.
5. Click the top button "Open with Google Sheets".
6. Completed! All analytical formulas (SUM, IF, AND, TEXT, products, ratios)
   and S-Curve charts will recalculate seamlessly in real time.

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

    print("\n[2/3] Empaquetando Executive_Decision_Pack_EVM_Dual.zip...")
    os.makedirs(DIR_LEMON, exist_ok=True)

    with zipfile.ZipFile(ZIP_PATH_LOCAL, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 1. Archivos en raíz del ZIP
        root_files = ["LEEME_ACCESO_GOOGLE_SHEETS.txt", "README_GOOGLE_SHEETS_ACCESS.txt"]
        for rf in root_files:
            rf_path = os.path.join(DIR_PACK, rf)
            if os.path.exists(rf_path):
                zipf.write(rf_path, arcname=rf)
                print(f"  + Raíz: {rf}")

        # 2. Archivos en carpeta ES
        es_files = [
            "Cuadro_Mando_EVM_Datalaria_ES.xlsx",
            "Presentacion_EVM_CLevel_ES.pptx",
            "Guia_Metodologica_EVM_ES.pdf",
            "LEEME_INSTRUCCIONES.txt"
        ]
        for ef in es_files:
            ef_path = os.path.join(DIR_ES, ef)
            if os.path.exists(ef_path):
                arc_name = os.path.join("[ES]_Cuadro_EVM_Valor_Ganado", ef)
                zipf.write(ef_path, arcname=arc_name)
                print(f"  + [ES]: {ef}")
            else:
                print(f"  ! ALERTA: No se encontró {ef_path}")

        # 3. Archivos en carpeta EN
        en_files = [
            "EVM_Dashboard_Datalaria_EN.xlsx",
            "Deck_EVM_CLevel_EN.pptx",
            "Methodology_Guide_EVM_EN.pdf",
            "README_INSTRUCTIONS.txt"
        ]
        for ef in en_files:
            ef_path = os.path.join(DIR_EN, ef)
            if os.path.exists(ef_path):
                arc_name = os.path.join("[EN]_Earned_Value_Management_EVM", ef)
                zipf.write(ef_path, arcname=arc_name)
                print(f"  + [EN]: {ef}")
            else:
                print(f"  ! ALERTA: No se encontró {ef_path}")

    print(f"  -> Archivo ZIP creado exitosamente: {ZIP_PATH_LOCAL}")

    # Copia para distribución en Lemon Squeezy
    print("\n[3/3] Sincronizando copia a directorio privado de Lemon Squeezy...")
    shutil.copy2(ZIP_PATH_LOCAL, ZIP_PATH_LEMON)
    print(f"  -> Copia lista en: {ZIP_PATH_LEMON}")

    # Verificación de seguridad
    forbidden_paths = [
        "static/downloads/Executive_Decision_Pack_EVM_Dual.zip",
        "public/downloads/Executive_Decision_Pack_EVM_Dual.zip"
    ]
    for fb in forbidden_paths:
        if os.path.exists(fb):
            os.remove(fb)
            print(f"  ! Eliminado archivo en ruta pública no permitida: {fb}")

    print("\nEmpaquetado completado con éxito y conformidad de seguridad 100%.")


if __name__ == "__main__":
    build_master_zip()
