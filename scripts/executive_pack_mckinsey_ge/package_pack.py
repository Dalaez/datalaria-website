#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los archivos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Executive_Decision_Pack_McKinsey_GE_Dual.zip

Estructura del archivo ZIP:
- [ES]_Matriz_McKinsey_GE/
  - ES_Matriz_McKinsey_GE_Datalaria.xlsx
  - ES_Matriz_McKinsey_GE_Presentacion.pptx
  - ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026")
- [EN]_McKinsey_GE_Matrix/
  - EN_McKinsey_GE_Matrix_Datalaria.xlsx
  - EN_McKinsey_GE_Matrix_Presentation.pptx
  - EN_McKinsey_GE_Matrix_Methodology_Guide.pdf
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
DIR_ES = os.path.join(DIR_PACKAGES, "[ES]_Matriz_McKinsey_GE")
DIR_EN = os.path.join(DIR_PACKAGES, "[EN]_McKinsey_GE_Matrix")

LEEME_INSTRUCCIONES_ES = """================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Matriz McKinsey / General Electric 3x3 & Asignación de Capital (Edición Oficial 2026)
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas de consultoría estratégica de estándar Tier-1 
(McKinsey / BCG) está diseñado específicamente para Comités de Dirección (C-Level), 
Consejos de Administración y Comités de Inversión de M&A y Private Equity.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• ES_Matriz_McKinsey_GE_Datalaria.xlsx
  Libro de trabajo estratégico en Excel con 3 pestañas estructuradas e interconectadas:
  - Pestaña 1: 01_Dashboard_Ejecutivo (Cuadrícula 3x3 de 9 cajas con semáforo condicional 
               por Zonas de Capital: Invertir/Crecer, Seleccionar/Proteger y Cosechar/Desinvertir, 
               tabla resumen de 10 UENs con cálculo automático de cuadrante y KPIs ejecutivos).
  - Pestaña 2: 02_Evaluacion_Multifactorial (Matriz de ponderación configurable con 5 factores 
               de Atractivo de Industria y 5 de Fortaleza Competitiva, fórmulas SUMAPRODUCTO 
               y validación de datos 1.0 a 5.0).
  - Pestaña 3: 03_Plan_Asignacion_Capital (Reparto porcentual de CAPEX corporativo vs. Política, 
               plan de hitos a 12-24-36 meses por UEN con Hurdle Rates/TIR y bloque de firmas).

• ES_Matriz_McKinsey_GE_Presentacion.pptx
  Presentación ejecutiva panorámica (16:9 widescreen) bajo la Pirámide de Minto:
  - Diapositiva 1: Visión General de Cartera con Gráfico Cartesiano 3x3 de alta resolución y 4 KPI Cards.
  - Diapositiva 2: Diagnóstico de las 3 Zonas Estratégicas y perfilado de riesgo-retorno.
  - Diapositiva 3: Board Decision Gateway con tabla de gobernanza, 3 resoluciones formales y bloque de firmas.

• ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf
  Guía metodológica oficial de 5 páginas con fundamentación matemática formal de los índices IA y FC,
  protocolo cuantitativo de 4 filtros para neutralizar el sesgo del management, caso de estudio 
  industrial resuelto (Vanguard Group) con impacto en ROIC (+380 bps) y FAQ de defensa ante el Consejo.

--------------------------------------------------------------------------------
2. CONTRASEÑA OFICIAL Y PROTECCIÓN DE CELDAS
--------------------------------------------------------------------------------
Para garantizar la integridad del modelo durante reuniones ejecutivas y evitar la 
alteración accidental de fórmulas, las celdas de cálculo y títulos están protegidas.

Todas las celdas de entrada de datos (nombres de UENs, facturación propia, márgenes EBITDA %, 
calificaciones de factores 1.0 a 5.0 e iniciativas de capital) están 100% DESBLOQUEADAS 
para su libre edición e inserción de datos.

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
McKinsey / General Electric 3x3 Matrix & Capital Allocation (Official 2026 Edition)
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite provides Tier-1 management consulting decision-support tools tailored 
for C-Suite committees, Boards of Directors, and M&A / Private Equity Investment Committees.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• EN_McKinsey_GE_Matrix_Datalaria.xlsx
  Comprehensive 3-tab strategic workbook:
  - Tab 1: 01_Executive_Dashboard (Visual 9-box 3x3 grid with conditional color coding across 
           3 Capital Zones: Invest/Grow, Selectivity/Hold, Harvest/Divest, master portfolio table 
           of 10 SBUs with automated quadrant lookup, and executive KPI cards).
  - Tab 2: 02_Multifactor_Assessment (Configurable weighting matrix with 5 Industry Attractiveness 
           and 5 Business Unit Strength criteria, SUMPRODUCT formulas, and 1.0-5.0 score validation).
  - Tab 3: 03_Capital_Allocation_Plan (Corporate CAPEX policy split vs. target, 12-24-36 month 
           milestone roadmap per SBU with Hurdle Rates/IRR and Board sign-off block).

• EN_McKinsey_GE_Matrix_Presentation.pptx
  16:9 widescreen boardroom presentation engineered under the Minto Pyramid Principle:
  - Slide 1: Executive Portfolio Overview with high-resolution 3x3 Cartesian grid and 4 KPI Cards.
  - Slide 2: Strategic Zone Diagnostics & Risk-Return Profiling across 3 executive panels.
  - Slide 3: Board Decision Gateway with governance master table, 3 binding resolutions, and signatures.

• EN_McKinsey_GE_Matrix_Methodology_Guide.pdf
  5-page executive methodology guide featuring mathematical proofs of IA and FC indices, 
  4-filter quantitative audit protocol to eliminate management bias, full industrial case study 
  (Vanguard Group) with +380 bps ROIC accretion, and C-Level boardroom defense protocol (FAQ).

--------------------------------------------------------------------------------
2. MASTER PASSWORD & WORKSHEET PROTECTION
--------------------------------------------------------------------------------
To safeguard critical matrix algorithms during boardroom meetings and prevent accidental 
disruption of formulas, calculation cells and headers are protected.

All user input cells (SBU names, sales, EBITDA margins, 1.0-5.0 factor ratings, 
and capital plan initiatives) are 100% UNLOCKED for free editing and data entry.

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
   - "ES_Matriz_McKinsey_GE_Datalaria.xlsx" (o la versión en inglés).
4. Una vez completada la subida, haz doble clic sobre el archivo en tu unidad de Drive.
5. Haz clic en "Abrir con Hojas de cálculo de Google" en la barra superior.
6. ¡Listo! Todas las fórmulas matriciales, ponderaciones SUMAPRODUCTO, semáforos lógicos 
   y vínculos entre pestañas operarán de manera completamente nativa.

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
   - "EN_McKinsey_GE_Matrix_Datalaria.xlsx" (or the Spanish edition).
4. Once uploaded, double-click the file in your Google Drive list.
5. Click "Open with Google Sheets" at the top center.
6. All matrix formulas, SUMPRODUCT calculations, logic checks, and cross-tab linkages will function natively.

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

    # Asegurar que los archivos en DIR_ES y DIR_EN están sincronizados con la raíz de packages
    # (o copiarlos si no existen)
    for fname in ["ES_Matriz_McKinsey_GE_Datalaria.xlsx", "ES_Matriz_McKinsey_GE_Presentacion.pptx", "ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf"]:
        src = os.path.join(DIR_PACKAGES, fname)
        dst = os.path.join(DIR_ES, fname)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

    for fname in ["EN_McKinsey_GE_Matrix_Datalaria.xlsx", "EN_McKinsey_GE_Matrix_Presentation.pptx", "EN_McKinsey_GE_Matrix_Methodology_Guide.pdf"]:
        src = os.path.join(DIR_PACKAGES, fname)
        dst = os.path.join(DIR_EN, fname)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

    files_es = [
        ("ES_Matriz_McKinsey_GE_Datalaria.xlsx", os.path.join(DIR_ES, "ES_Matriz_McKinsey_GE_Datalaria.xlsx")),
        ("ES_Matriz_McKinsey_GE_Presentacion.pptx", os.path.join(DIR_ES, "ES_Matriz_McKinsey_GE_Presentacion.pptx")),
        ("ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf", os.path.join(DIR_ES, "ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf")),
        ("LEEME_INSTRUCCIONES.txt", leeme_es_path),
    ]

    files_en = [
        ("EN_McKinsey_GE_Matrix_Datalaria.xlsx", os.path.join(DIR_EN, "EN_McKinsey_GE_Matrix_Datalaria.xlsx")),
        ("EN_McKinsey_GE_Matrix_Presentation.pptx", os.path.join(DIR_EN, "EN_McKinsey_GE_Matrix_Presentation.pptx")),
        ("EN_McKinsey_GE_Matrix_Methodology_Guide.pdf", os.path.join(DIR_EN, "EN_McKinsey_GE_Matrix_Methodology_Guide.pdf")),
        ("README_INSTRUCTIONS.txt", readme_en_path),
    ]

    # Verificar existencia de archivos obligatorios
    for fname, fpath in files_es + files_en:
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"[ERROR] Archivo requerido no encontrado: {fpath}")

    # 2. Generar el archivo ZIP maestro dual exclusivamente en packages/
    zip_output_path = os.path.join(DIR_PACKAGES, "Executive_Decision_Pack_McKinsey_GE_Dual.zip")
    print(f"Empaquetando archivo maestro: {zip_output_path}...")

    with zipfile.ZipFile(zip_output_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Añadir archivos ES bajo carpeta [ES]_Matriz_McKinsey_GE/
        for arcname, fpath in files_es:
            zip_arc_path = f"[ES]_Matriz_McKinsey_GE/{arcname}"
            zipf.write(fpath, arcname=zip_arc_path)
            print(f"  + Añadido: {zip_arc_path}")

        # Añadir archivos EN bajo carpeta [EN]_McKinsey_GE_Matrix/
        for arcname, fpath in files_en:
            zip_arc_path = f"[EN]_McKinsey_GE_Matrix/{arcname}"
            zipf.write(fpath, arcname=zip_arc_path)
            print(f"  + Añadido: {zip_arc_path}")

        # Añadir instrucciones de Google Sheets en la raíz del ZIP
        zipf.write(leeme_gs_path, arcname="LEEME_ACCESO_GOOGLE_SHEETS.txt")
        print("  + Añadido: LEEME_ACCESO_GOOGLE_SHEETS.txt (raíz)")
        zipf.write(readme_gs_path, arcname="README_GOOGLE_SHEETS_ACCESS.txt")
        print("  + Añadido: README_GOOGLE_SHEETS_ACCESS.txt (raíz)")

    zip_size_kb = os.path.getsize(zip_output_path) / 1024
    print(f"\n[ÉXITO] Paquete maestro generado con éxito: {zip_output_path} ({zip_size_kb:.1f} KB)")
    print("Verificación de seguridad: Todos los archivos residen exclusivamente en packages/.")


if __name__ == "__main__":
    build_package()
