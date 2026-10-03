#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los archivos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Executive_Decision_Pack_BCG_Dual.zip

Estructura del archivo ZIP:
- [ES]_BCG_Dinamica/
  - BCG_Dinamica_Datalaria_ES.xlsx
  - Presentacion_BCG_CLevel_ES.pptx
  - Guia_Metodologica_BCG_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026")
- [EN]_Dynamic_BCG/
  - Dynamic_BCG_Datalaria_EN.xlsx
  - Deck_BCG_CLevel_EN.pptx
  - Methodology_Guide_BCG_EN.pdf
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
DIR_ES = os.path.join(DIR_PACKAGES, "[ES]_BCG_Dinamica")
DIR_EN = os.path.join(DIR_PACKAGES, "[EN]_Dynamic_BCG")

LEEME_INSTRUCCIONES_ES = """================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Matriz BCG Dinámica & Asignación de Capital de Cartera (Edición Oficial 2026)
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas de consultoría estratégica de estándar Tier-1 
(McKinsey / BCG) está diseñado específicamente para Comités de Dirección (C-Level), 
Consejos de Administración y Comités de Inversión de M&A y Private Equity.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• BCG_Dinamica_Datalaria_ES.xlsx
  Libro de trabajo estratégico en Excel con 4 pestañas interconectadas:
  - Pestaña 1: Dashboard Ejecutivo (Gráfico de Burbujas cartesiano dinámico CMR vs. TCM 
               con tamaño proporcional a facturación, Balance Neto de Fondos de Bruce Henderson, 
               desglose por cuadrante y semáforo de sostenibilidad estratégica).
  - Pestaña 2: Evaluación Cartera UENs (Registro y auditoría cuantitativa de hasta 12 UENs: 
               facturación propia, líder competidor, CMR calculada, crecimiento del mercado %, 
               margen EBITDA %, FCF neto y clasificación automatizada).
  - Pestaña 3: Matriz & Flujo de Fondos (Balance de superávit de Vacas vs. déficit de 
               Interrogantes, parámetros de Curva de Experiencia de Henderson y vectores 
               de transición estratégica a 3 años).
  - Pestaña 4: Plan de Asignación de Capital (8 iniciativas con Owner C-Level, plazos Q1-Q4, 
               presupuesto reasignado de CAPEX/desinversión y KPI de impacto en ROIC).

• Presentacion_BCG_CLevel_ES.pptx
  Presentación ejecutiva panorámica (16:9 widescreen) bajo la Pirámide de Minto:
  - Diapositiva 1: Síntesis Ejecutiva con 4 tarjetas de impacto de alto contraste.
  - Diapositiva 2: Evidencia Cuantitativa con Gráfico de Burbujas cartesiano y tarjetas de cuadrante.
  - Diapositiva 3: Roadmap de Capital Q1-Q4 y Board Decision Gateway con 3 resoluciones 
                   formales vinculantes listas para someter a votación del Consejo.

• Guia_Metodologica_BCG_ES.pdf
  Guía metodológica oficial de 5 páginas con fundamentación matemática formal de la 
  Cuota de Mercado Relativa (CMR), derivación de la Curva de Experiencia de Henderson, 
  caso de estudio industrial B2B resuelto (Nexus Group) con impacto en ROIC y protocolo de defensa C-Level (FAQ).

--------------------------------------------------------------------------------
2. CONTRASEÑA OFICIAL Y PROTECCIÓN DE CELDAS
--------------------------------------------------------------------------------
Para garantizar la integridad del modelo durante reuniones ejecutivas y evitar la 
alteración accidental de fórmulas, las celdas de cálculo y títulos están protegidas.

Todas las celdas de entrada de datos (nombres de UENs, facturación propia, ventas 
competidor, tasas de crecimiento %, márgenes % e iniciativas de capital) están 
100% DESBLOQUEADAS para su libre edición e inserción de datos.

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
Dynamic BCG Portfolio Matrix & Capital Allocation (Official 2026 Edition)
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite provides Tier-1 management consulting decision-support tools tailored 
for C-Suite committees, Boards of Directors, and M&A / Private Equity Investment Committees.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Dynamic_BCG_Datalaria_EN.xlsx
  Comprehensive 4-tab strategic workbook:
  - Tab 1: Executive Dashboard (Dynamic Cartesian Bubble Chart RMS vs. MGR with bubble size 
           proportional to revenue, Bruce Henderson Cash Flow Balance, quadrant breakdown, 
           and strategic sustainability scorecard).
  - Tab 2: Business Units Assessment (Registry and quantitative audit of up to 12 SBUs: 
           own sales, leading competitor sales, computed RMS ratio, market growth rate %, 
           EBITDA margin %, net FCF generation, and automated quadrant assignment).
  - Tab 3: BCG Matrix & Fund Flow (Cash Cow surplus vs. Question Mark deficit balance, 
           Henderson Experience Curve parameters, and 3-year strategic transition vectors).
  - Tab 4: Capital Allocation Plan (8 initiatives with C-Suite Owners, Q1-Q4 roadmap, 
           reallocated CAPEX/divestment budgets, and ROIC impact KPIs).

• Deck_BCG_CLevel_EN.pptx
  16:9 widescreen boardroom presentation engineered under the Minto Pyramid Principle:
  - Slide 1: Executive Synthesis with 4 high-contrast impact KPI cards.
  - Slide 2: Quantitative Evidence, high-resolution Bubble Chart, and quadrant strategic cards.
  - Slide 3: Capital Roadmap Q1-Q4 and Board Decision Gateway with 3 binding formal 
             resolutions ready for voting.

• Methodology_Guide_BCG_EN.pdf
  5-page executive methodology guide featuring mathematical proofs of Relative Market Share (RMS), 
  Bruce Henderson's Experience Curve power laws, full industrial B2B case study (Nexus Group) 
  with ROIC accretion, and tough boardroom defense protocols (FAQ).

--------------------------------------------------------------------------------
2. MASTER PASSWORD & WORKSHEET PROTECTION
--------------------------------------------------------------------------------
To safeguard critical matrix algorithms during boardroom meetings and prevent accidental 
disruption of formulas, calculation cells and headers are protected.

All user input cells (SBU names, own sales, competitor revenues, growth rates, margins, 
and capital plan fields) are 100% UNLOCKED for free editing and data entry.

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
   - "BCG_Dinamica_Datalaria_ES.xlsx" (o la versión en inglés).
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
   - "Dynamic_BCG_Datalaria_EN.xlsx" (or the Spanish edition).
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
        ("BCG_Dinamica_Datalaria_ES.xlsx", os.path.join(DIR_ES, "BCG_Dinamica_Datalaria_ES.xlsx")),
        ("Presentacion_BCG_CLevel_ES.pptx", os.path.join(DIR_ES, "Presentacion_BCG_CLevel_ES.pptx")),
        ("Guia_Metodologica_BCG_ES.pdf", os.path.join(DIR_ES, "Guia_Metodologica_BCG_ES.pdf")),
        ("LEEME_INSTRUCCIONES.txt", leeme_es_path),
    ]

    files_en = [
        ("Dynamic_BCG_Datalaria_EN.xlsx", os.path.join(DIR_EN, "Dynamic_BCG_Datalaria_EN.xlsx")),
        ("Deck_BCG_CLevel_EN.pptx", os.path.join(DIR_EN, "Deck_BCG_CLevel_EN.pptx")),
        ("Methodology_Guide_BCG_EN.pdf", os.path.join(DIR_EN, "Methodology_Guide_BCG_EN.pdf")),
        ("README_INSTRUCTIONS.txt", readme_en_path),
    ]

    # Verificar existencia de archivos obligatorios
    for fname, fpath in files_es + files_en:
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"[ERROR] Archivo requerido no encontrado: {fpath}")

    # 2. Generar el archivo ZIP maestro dual exclusivamente en packages/
    zip_output_path = os.path.join(DIR_PACKAGES, "Executive_Decision_Pack_BCG_Dual.zip")
    print(f"Empaquetando archivo maestro: {zip_output_path}...")

    with zipfile.ZipFile(zip_output_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Añadir archivos ES bajo carpeta [ES]_BCG_Dinamica/
        for arcname, fpath in files_es:
            zip_arc_path = f"[ES]_BCG_Dinamica/{arcname}"
            zipf.write(fpath, arcname=zip_arc_path)
            print(f"  + Añadido: {zip_arc_path}")

        # Añadir archivos EN bajo carpeta [EN]_Dynamic_BCG/
        for arcname, fpath in files_en:
            zip_arc_path = f"[EN]_Dynamic_BCG/{arcname}"
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
