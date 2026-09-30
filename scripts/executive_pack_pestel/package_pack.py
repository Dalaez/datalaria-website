#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los archivos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Executive_Decision_Pack_PESTEL_Dual.zip

Estructura del archivo ZIP:
- [ES]_PESTEL_Cuantitativo/
  - PESTEL_Cuantitativo_Datalaria_ES.xlsx
  - Presentacion_PESTEL_CLevel_ES.pptx
  - Guia_Metodologica_PESTEL_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026")
- [EN]_Quantitative_PESTEL/
  - Quantitative_PESTEL_Datalaria_EN.xlsx
  - Deck_PESTEL_CLevel_EN.pptx
  - Methodology_Guide_PESTEL_EN.pdf
  - README_INSTRUCTIONS.txt (con contraseña oficial "Datalaria2026")
- LEEME_ACCESO_GOOGLE_SHEETS.txt (en la raíz del ZIP)
- README_GOOGLE_SHEETS_ACCESS.txt (en la raíz del ZIP)

SEGURIDAD ESTRICTA:
Queda terminantemente prohibido almacenar o sincronizar archivos a static/downloads/
o public/downloads/. Todos los activos quedan alojados exclusivamente en packages/.
"""

import os
import zipfile
import shutil

DIR_PACKAGES = "packages"
DIR_ES = os.path.join(DIR_PACKAGES, "[ES]_PESTEL_Cuantitativo")
DIR_EN = os.path.join(DIR_PACKAGES, "[EN]_Quantitative_PESTEL")

LEEME_INSTRUCCIONES_ES = """================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Matriz PESTEL Cuantitativa: Severidad, Volatilidad & Riesgo Macro (Edición 2026)
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas de consultoría estratégica de estándar Tier-1 
(McKinsey / BCG) está diseñado específicamente para Comités de Dirección (C-Level), 
Consejos de Administración y Comités de Inversión de M&A y Private Equity.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• PESTEL_Cuantitativo_Datalaria_ES.xlsx
  Libro de trabajo estratégico en Excel con 4 pestañas interconectadas:
  - Pestaña 1: Dashboard Ejecutivo (Índice R_comp, Nivel de Exposición Global, 
               Gráfico Radar hexagonal dinámico de las 6 dimensiones PESTEL, 
               Semáforo de Resiliencia Empresarial y Recomendaciones de Capital).
  - Pestaña 2: Evaluación 6 Dimensiones (Evaluación exhaustiva de los 6 pilares: 
               1. Político, 2. Económico, 3. Social, 4. Tecnológico, 5. Ecológico, 
               6. Legal. Ponderación Σw=100%, doble calificación de Severidad [1-5] 
               y Volatilidad [1-5], y cálculo del Riesgo Ponderado).
  - Pestaña 3: Matriz Severidad vs Volatilidad (Mapa cartesiano de Incertidumbre 
               Estratégica categorizando factores en 4 cuadrantes: Q1 Riesgos 
               Críticos Volátiles, Q2 Riesgos Estructurales Predecibles, Q3 Alertas 
               Tempranas Emergentes, Q4 Ruidos Menores).
  - Pestaña 4: Plan Resiliencia & Contingencia (8 iniciativas de mitigación con 
               Owner C-Level, plazos Q1-Q4, presupuesto CAPEX/OPEX y KPI de impacto 
               en P&L o preservación de EBITDA).

• Presentacion_PESTEL_CLevel_ES.pptx
  Presentación ejecutiva panorámica (16:9 widescreen) bajo la Pirámide de Minto:
  - Diapositiva 1: Síntesis Ejecutiva con 4 tarjetas de impacto de alto contraste
  - Diapositiva 2: Evidencia Cuantitativa, Gráfico Radar hexagonal y bloques de severidad
  - Diapositiva 3: Roadmap de Resiliencia Q1-Q4 y Gateway de Decisión del Consejo 
                   con 3 resoluciones formales listas para someter a votación

• Guia_Metodologica_PESTEL_ES.pdf
  Guía metodológica oficial de 5 páginas con fundamentación matemática formal, 
  espacio métrico bidimensional, taxonomía de respuestas ante Cisnes Negros, caso 
  de estudio industrial resuelto con impacto en P&L y protocolo de defensa ante preguntas difíciles.

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
Quantitative PESTEL Matrix: Severity, Volatility & Macro Risk (Official 2026 Edition)
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite provides Tier-1 management consulting decision-support tools tailored 
for C-Suite committees, Boards of Directors, and M&A / Private Equity Investment Committees.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Quantitative_PESTEL_Datalaria_EN.xlsx
  Comprehensive 4-tab strategic workbook:
  - Tab 1: Executive Dashboard (Composite Macro Risk R_comp Index, Exposure Level, 
           Dynamic Hexagonal Radar Chart of the 6 PESTEL dimensions, Corporate 
           Resilience Scorecard, and Capital Allocation Guidance).
  - Tab 2: 6 Dimensions Assessment (Empirical assessment of the 6 canonical 
           pillars: 1. Political, 2. Economic, 3. Social, 4. Technological, 
           5. Environmental, 6. Legal. Σw=100% weighting, dual Severity [1-5] 
           and Volatility [1-5] scoring, and weighted risk metrics).
  - Tab 3: Severity vs Volatility Matrix (Strategic Uncertainty 2D Cartesian map 
           categorizing factors into 4 quadrants: Q1 Critical Volatile Risks, 
           Q2 Structural Predictable Risks, Q3 Early Warnings, Q4 Minor Noise).
  - Tab 4: Macro Resilience Action Plan (8 mitigation initiatives with C-Suite 
           Owners, Q1-Q4 roadmap, CAPEX/OPEX budgets, and EBITDA preservation KPIs).

• Deck_PESTEL_CLevel_EN.pptx
  16:9 widescreen boardroom presentation engineered under the Minto Pyramid Principle:
  - Slide 1: Executive Synthesis with 4 high-contrast impact KPI cards
  - Slide 2: Quantitative Evidence, Radar Chart, and 3 structured severity blocks
  - Slide 3: Resilience Execution Roadmap Q1-Q4 and Board Decision Gateway with 3 formal 
             resolutions submitted for approval and vote

• Methodology_Guide_PESTEL_EN.pdf
  5-page executive methodology guide featuring mathematical proofs, 2D uncertainty 
  space mechanics, response taxonomy against Black Swans vs. Noise, full industrial 
  case study with P&L impact, and tough executive boardroom defense protocols.

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
   - "PESTEL_Cuantitativo_Datalaria_ES.xlsx" (o la versión en inglés).
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
   - "Quantitative_PESTEL_Datalaria_EN.xlsx" (or the Spanish edition).
4. Once uploaded, double-click the file in your Google Drive list.
5. Click "Open with Google Sheets" at the top center.
6. All matrix formulas, calculations, logic checks, and cross-tab linkages will function natively.

Note: To unprotect sheets within Google Sheets for structural customizations, navigate to 
Data > Protected sheets and ranges and enter the master password documented in 
README_INSTRUCTIONS.txt (Datalaria2026).
"""


def build_package():
    os.makedirs(DIR_PACKAGES, exist_ok=True)
    os.makedirs(DIR_ES, exist_ok=True)
    os.makedirs(DIR_EN, exist_ok=True)

    # 1. Guardar archivos de instrucciones en disco
    leeme_es_path = os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt")
    with open(leeme_es_path, "w", encoding="utf-8") as f:
        f.write(LEEME_INSTRUCCIONES_ES)

    readme_en_path = os.path.join(DIR_EN, "README_INSTRUCTIONS.txt")
    with open(readme_en_path, "w", encoding="utf-8") as f:
        f.write(README_INSTRUCTIONS_EN)

    leeme_gs_path = os.path.join(DIR_PACKAGES, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
    with open(leeme_gs_path, "w", encoding="utf-8") as f:
        f.write(LEEME_GOOGLE_SHEETS_ES)

    readme_gs_path = os.path.join(DIR_PACKAGES, "README_GOOGLE_SHEETS_ACCESS.txt")
    with open(readme_gs_path, "w", encoding="utf-8") as f:
        f.write(README_GOOGLE_SHEETS_EN)

    files_es = [
        ("PESTEL_Cuantitativo_Datalaria_ES.xlsx", os.path.join(DIR_ES, "PESTEL_Cuantitativo_Datalaria_ES.xlsx")),
        ("Presentacion_PESTEL_CLevel_ES.pptx", os.path.join(DIR_ES, "Presentacion_PESTEL_CLevel_ES.pptx")),
        ("Guia_Metodologica_PESTEL_ES.pdf", os.path.join(DIR_ES, "Guia_Metodologica_PESTEL_ES.pdf")),
        ("LEEME_INSTRUCCIONES.txt", leeme_es_path),
    ]

    files_en = [
        ("Quantitative_PESTEL_Datalaria_EN.xlsx", os.path.join(DIR_EN, "Quantitative_PESTEL_Datalaria_EN.xlsx")),
        ("Deck_PESTEL_CLevel_EN.pptx", os.path.join(DIR_EN, "Deck_PESTEL_CLevel_EN.pptx")),
        ("Methodology_Guide_PESTEL_EN.pdf", os.path.join(DIR_EN, "Methodology_Guide_PESTEL_EN.pdf")),
        ("README_INSTRUCTIONS.txt", readme_en_path),
    ]

    # 2. Empaquetar el archivo ZIP maestro oficial en packages/
    zip_path = os.path.join(DIR_PACKAGES, "Executive_Decision_Pack_PESTEL_Dual.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # Carpeta [ES]_PESTEL_Cuantitativo
        for arcname, fpath in files_es:
            if os.path.exists(fpath):
                z.write(fpath, arcname=f"[ES]_PESTEL_Cuantitativo/{arcname}")
            else:
                print(f"[WARN] Archivo no encontrado: {fpath}")

        # Carpeta [EN]_Quantitative_PESTEL
        for arcname, fpath in files_en:
            if os.path.exists(fpath):
                z.write(fpath, arcname=f"[EN]_Quantitative_PESTEL/{arcname}")
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
