#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los archivos del Executive Decision Pack en el archivo ZIP oficial
listo para distribución comercial en Lemon Squeezy:
- static/downloads/Executive_Decision_Pack_Porter_5_Forces_Dual.zip

Estructura del archivo ZIP:
- [ES]_5_Fuerzas_Porter/
  - Porter_5_Fuerzas_Datalaria_ES.xlsx
  - Presentacion_Porter_CLevel_ES.pptx
  - Guia_Metodologica_Porter_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña "Datalaria2026")
- [EN]_Porter_5_Forces/
  - Porter_5_Forces_Datalaria_EN.xlsx
  - Deck_Porter_CLevel_EN.pptx
  - Methodology_Guide_Porter_EN.pdf
  - README_INSTRUCTIONS.txt (con contraseña "Datalaria2026")
- LEEME_ACCESO_GOOGLE_SHEETS.txt (en la raíz)
- README_GOOGLE_SHEETS_ACCESS.txt (en la raíz)

Sincroniza automáticamente a static/downloads/ y public/downloads/.
"""

import os
import zipfile
import shutil

DIR_PACKAGES = "packages"
DIR_ES = os.path.join(DIR_PACKAGES, "[ES]_5_Fuerzas_Porter")
DIR_EN = os.path.join(DIR_PACKAGES, "[EN]_Porter_5_Forces")

LEEME_INSTRUCCIONES_ES = """================================================================================
DATALARIA | EXECUTIVE DECISION PACK
5 Fuerzas de Porter Ponderadas & Atractivo de Industria (Edición Oficial 2026)
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas de consultoría estratégica de estándar Tier-1 
(McKinsey / BCG) está diseñado específicamente para Comités de Dirección (C-Level), 
Consejos de Administración y Comités de Inversión de M&A y Private Equity.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Porter_5_Fuerzas_Datalaria_ES.xlsx
  Libro de trabajo estratégico en Excel con 4 pestañas interconectadas:
  - Pestaña 1: Dashboard Ejecutivo (KPIs, Índice I_comp, Atractivo A_ind, 
               Gráfico Radar pentagonal dinámico y postura estratégica recomendada)
  - Pestaña 2: Evaluación 5 Fuerzas (Desglose de las 5 fuerzas canónicas con 4-5 
               subfactores objetivos cada una, ponderación Σw=100% y notas 1-5)
  - Pestaña 3: Matriz Atractivo vs Moat (Evaluación de los 5 pilares de foso 
               defensivo, matriz cartesiana bidimensional y diagnóstico de cuadrante)
  - Pestaña 4: Plan de Blindaje Estratégico (8 iniciativas de mitigación con 
               Owner C-Level, plazos Q1-Q4, presupuestos CAPEX/OPEX y KPIs en EBITDA)

• Presentacion_Porter_CLevel_ES.pptx
  Presentación ejecutiva panorámica (16:9 widescreen) bajo la Pirámide de Minto:
  - Diapositiva 1: Síntesis Ejecutiva con 4 tarjetas de impacto de alto contraste
  - Diapositiva 2: Evidencia Cuantitativa, Gráfico Radar y bloques de severidad
  - Diapositiva 3: Roadmap de Blindaje Q1-Q4 y Gateway de Decisión del Consejo 
                   con 3 resoluciones formales listas para someter a votación

• Guia_Metodologica_Porter_ES.pdf
  Guía metodológica oficial de 5 páginas con fundamentación matemática formal, 
  demostración escalar del atractivo, algoritmo de blindaje del Moat, caso de estudio 
  industrial resuelto con impacto en P&L y protocolo de defensa ante preguntas difíciles.

--------------------------------------------------------------------------------
2. CONTRASEÑA OFICIAL Y PROTECCIÓN DE CELDAS
--------------------------------------------------------------------------------
Para garantizar la integridad del modelo durante reuniones ejecutivas y evitar la 
alteración accidental de fórmulas, las celdas de cálculo y títulos están protegidas.

Todas las celdas de entrada de datos (subfactores, ponderaciones relativas, notas 
de escala 1-5 y campos del plan de acción) están 100% DESBLOQUEADAS para su libre 
edición e inserción de datos.

Si necesitas desproteger las hojas para realizar ampliaciones estructurales, la 
contraseña oficial del modelo es:
  Datalaria2026

--------------------------------------------------------------------------------
3. COMPATIBILIDAD CON GOOGLE SHEETS
--------------------------------------------------------------------------------
El archivo Excel utiliza exclusivamente funciones matriciales y lógicas nativas 
compatibles al 100% con Google Drive y Google Sheets (ver archivo adjunto 
LEEME_ACCESO_GOOGLE_SHEETS.txt en la raíz del paquete).

--------------------------------------------------------------------------------
4. CONTACTO Y ASESORÍA ESTRATÉGICA
--------------------------------------------------------------------------------
Para workshops de facilitación con Comités de Dirección o modelización ad-hoc:
• Web: https://datalaria.com
• Email Corporativo: datalaria@gmail.com
• LinkedIn: https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/

© 2026 Datalaria. Todos los derechos reservados.
"""

README_INSTRUCTIONS_EN = """================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Weighted Porter's 5 Forces & Industry Attractiveness Matrix (Official 2026 Edition)
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite provides Tier-1 management consulting decision-support tools tailored 
for C-Suite committees, Boards of Directors, and M&A / Private Equity Investment Committees.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Porter_5_Forces_Datalaria_EN.xlsx
  Comprehensive 4-tab strategic workbook:
  - Tab 1: Executive Dashboard (Key Metrics, I_comp Index, A_ind Attractiveness, 
           Dynamic Pentagonal Radar Chart, and Capital Allocation Guidance)
  - Tab 2: 5 Forces Assessment (Breakdown of the 5 canonical forces with 4-5 
           empirical subfactors each, Σw=100% normalization and 1-5 scale)
  - Tab 3: Attractiveness & Moat Matrix (Internal economic moat assessment, 
           2D Cartesian matrix, and strategic quadrant diagnosis)
  - Tab 4: Strategic Moat Action Plan (8 mitigation initiatives with C-Level Owners, 
           Q1-Q4 roadmap, CAPEX/OPEX budgets, and EBITDA impact KPIs)

• Deck_Porter_CLevel_EN.pptx
  16:9 widescreen boardroom presentation engineered under the Minto Pyramid Principle:
  - Slide 1: Executive Synthesis with 4 high-contrast impact KPI cards
  - Slide 2: Quantitative Evidence, Radar Chart, and 3 structured severity blocks
  - Slide 3: Execution Roadmap Q1-Q4 and Board Decision Gateway with 3 formal 
             resolutions submitted for approval and vote

• Methodology_Guide_Porter_EN.pdf
  5-page executive methodology guide featuring mathematical proofs, scalar attractiveness 
  derivation, defensive moat mechanics, full industrial case study with P&L impact, 
  and tough executive boardroom defense protocols.

--------------------------------------------------------------------------------
2. MASTER PASSWORD & WORKSHEET PROTECTION
--------------------------------------------------------------------------------
To safeguard critical matrix algorithms during boardroom meetings and prevent accidental 
disruption of formulas, calculation cells and headers are protected.

All user input cells (subfactor descriptions, relative weights, 1-5 ratings, and 
action plan fields) are 100% UNLOCKED for free editing and data entry.

To unprotect sheets for bespoke architectural modifications, use the master password:
  Datalaria2026

--------------------------------------------------------------------------------
3. GOOGLE SHEETS COMPATIBILITY
--------------------------------------------------------------------------------
The Excel model relies exclusively on native matrix formulas compatible with Google 
Drive and Google Sheets (see accompanying README_GOOGLE_SHEETS_ACCESS.txt).

--------------------------------------------------------------------------------
4. CORPORATE ADVISORY & SUPPORT
--------------------------------------------------------------------------------
For enterprise licensing, bespoke financial modeling, or C-Suite strategic facilitation:
• Web: https://datalaria.com
• Advisory Services: datalaria@gmail.com
• LinkedIn: https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/

© 2026 Datalaria. All rights reserved.
"""

LEEME_GOOGLE_SHEETS_ES = """================================================================================
DATALARIA | GUÍA DE IMPORTACIÓN Y USO EN GOOGLE SHEETS
================================================================================

La plantilla Excel (.xlsx) del Executive Decision Pack ha sido diseñada bajo estrictos 
estándares de compatibilidad para funcionar con total fluidez tanto en Microsoft Excel 
como en Google Sheets:

1. Abre tu navegador web y accede a Google Drive (https://drive.google.com).
2. Haz clic en el botón "+ Nuevo" en la esquina superior izquierda y selecciona "Subir archivo".
3. Selecciona el archivo:
   - "Porter_5_Fuerzas_Datalaria_ES.xlsx" (o la versión en inglés).
4. Una vez completada la subida, haz doble clic sobre el archivo en tu unidad de Drive.
5. Haz clic en "Abrir con Hojas de cálculo de Google" en la barra superior.
6. ¡Listo! Todas las fórmulas matriciales, ponderaciones, semáforos lógicos y vínculos 
   entre pestañas operarán de manera completamente nativa.

Nota: Si deseas desproteger las hojas dentro de Google Sheets para personalizar filas 
o columnas, accede a Datos > Hojas y rangos protegidos e introduce la contraseña oficial 
documentada en LEEME_INSTRUCCIONES.txt (Datalaria2026).
"""

README_GOOGLE_SHEETS_EN = """================================================================================
DATALARIA | GOOGLE SHEETS IMPORT & ACCESS GUIDE
================================================================================

The Executive Decision Pack Excel workbook (.xlsx) is engineered for 100% native 
compatibility with Google Drive and Google Sheets without any proprietary macros:

1. Open your web browser and navigate to Google Drive (https://drive.google.com).
2. Click "+ New" in the top-left corner and select "File upload".
3. Select the workbook:
   - "Porter_5_Forces_Datalaria_EN.xlsx" (or the Spanish edition).
4. Once uploaded, double-click the file in your Google Drive list.
5. Click "Open with Google Sheets" at the top center.
6. All matrix formulas, calculations, logic checks, and cross-tab linkages will function natively.

Note: To unprotect sheets within Google Sheets for structural customizations, navigate to 
Data > Protected sheets and ranges and enter the master password documented in 
README_INSTRUCTIONS.txt (Datalaria2026).
"""


def build_package():
    os.makedirs(DIR_STATIC, exist_ok=True)
    os.makedirs(DIR_ES, exist_ok=True)
    os.makedirs(DIR_EN, exist_ok=True)

    # 1. Guardar archivos de instrucciones en disco
    leeme_es_path = os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt")
    with open(leeme_es_path, "w", encoding="utf-8") as f:
        f.write(LEEME_INSTRUCCIONES_ES)

    readme_en_path = os.path.join(DIR_EN, "README_INSTRUCTIONS.txt")
    with open(readme_en_path, "w", encoding="utf-8") as f:
        f.write(README_INSTRUCTIONS_EN)

    leeme_gs_path = os.path.join(DIR_STATIC, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
    with open(leeme_gs_path, "w", encoding="utf-8") as f:
        f.write(LEEME_GOOGLE_SHEETS_ES)

    readme_gs_path = os.path.join(DIR_STATIC, "README_GOOGLE_SHEETS_ACCESS.txt")
    with open(readme_gs_path, "w", encoding="utf-8") as f:
        f.write(README_GOOGLE_SHEETS_EN)

    files_es = [
        ("Porter_5_Fuerzas_Datalaria_ES.xlsx", os.path.join(DIR_ES, "Porter_5_Fuerzas_Datalaria_ES.xlsx")),
        ("Presentacion_Porter_CLevel_ES.pptx", os.path.join(DIR_ES, "Presentacion_Porter_CLevel_ES.pptx")),
        ("Guia_Metodologica_Porter_ES.pdf", os.path.join(DIR_ES, "Guia_Metodologica_Porter_ES.pdf")),
        ("LEEME_INSTRUCCIONES.txt", leeme_es_path),
    ]

    files_en = [
        ("Porter_5_Forces_Datalaria_EN.xlsx", os.path.join(DIR_EN, "Porter_5_Forces_Datalaria_EN.xlsx")),
        ("Deck_Porter_CLevel_EN.pptx", os.path.join(DIR_EN, "Deck_Porter_CLevel_EN.pptx")),
        ("Methodology_Guide_Porter_EN.pdf", os.path.join(DIR_EN, "Methodology_Guide_Porter_EN.pdf")),
        ("README_INSTRUCTIONS.txt", readme_en_path),
    ]

    # 2. Empaquetar el archivo ZIP maestro oficial en packages/
    zip_path = os.path.join(DIR_PACKAGES, "Executive_Decision_Pack_Porter_5_Forces_Dual.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # Carpeta [ES]_5_Fuerzas_Porter
        for arcname, fpath in files_es:
            if os.path.exists(fpath):
                z.write(fpath, arcname=f"[ES]_5_Fuerzas_Porter/{arcname}")
            else:
                print(f"[WARN] Archivo no encontrado: {fpath}")

        # Carpeta [EN]_Porter_5_Forces
        for arcname, fpath in files_en:
            if os.path.exists(fpath):
                z.write(fpath, arcname=f"[EN]_Porter_5_Forces/{arcname}")
            else:
                print(f"[WARN] Archivo no encontrado: {fpath}")

        # En la raíz del ZIP
        z.write(leeme_gs_path, arcname="LEEME_ACCESO_GOOGLE_SHEETS.txt")
        z.write(readme_gs_path, arcname="README_GOOGLE_SHEETS_ACCESS.txt")

    print(f"[OK] ZIP maestro creado en packages/: {zip_path} ({os.path.getsize(zip_path)} bytes)")

    # 3. Limpieza de seguridad de directorios public y static
    for p in ["static/downloads", "public/downloads"]:
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
            print(f"[SECURITY CLEANUP] Directorio público eliminado: {p}")


if __name__ == '__main__':
    build_package()
