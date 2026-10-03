#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los archivos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa/Executive_Decision_Pack_DAR_Dual.zip
- Copia directa en packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_DAR_Dual.zip

Estructura del archivo ZIP:
- [ES]_Matriz_DAR/
  - Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx
  - Presentacion_DAR_CLevel_ES.pptx
  - Guia_Metodologica_DAR_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- [EN]_Quantitative_DAR/
  - Quantitative_DAR_Matrix_Datalaria_EN.xlsx
  - Deck_DAR_CLevel_EN.pptx
  - Methodology_Guide_DAR_EN.pdf
  - README_INSTRUCTIONS.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- LEEME_ACCESO_GOOGLE_SHEETS.txt (en la raíz del ZIP)
- README_GOOGLE_SHEETS_ACCESS.txt (en la raíz del ZIP)

SEGURIDAD ESTRICTA:
Queda terminantemente prohibido almacenar o sincronizar archivos a static/downloads/
o public/downloads/. Todos los activos quedan alojados exclusivamente en packages/.
"""

import os
import zipfile
import shutil

DIR_PACK = "packages/Suite_02_Toma_Decisiones/01_Matriz_DAR_Cuantitativa"
DIR_ES = os.path.join(DIR_PACK, "[ES]_Matriz_DAR")
DIR_EN = os.path.join(DIR_PACK, "[EN]_Quantitative_DAR")
DIR_LEMON = "packages/00_DISTRIBUCION_LEMONSQUEEZY"

ZIP_NAME = "Executive_Decision_Pack_DAR_Dual.zip"
ZIP_PATH_LOCAL = os.path.join(DIR_PACK, ZIP_NAME)
ZIP_PATH_LEMON = os.path.join(DIR_LEMON, ZIP_NAME)

PASSWORD_OFFICIAL = "Datalaria2026"
SUPPORT_EMAIL = "datalaria@gmail.com"

LEEME_INSTRUCCIONES_ES = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Matriz DAR Cuantitativa: Análisis de Decisiones, Criterios Veto & Scoring Multicriterio
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas de consultoría estratégica de estándar Tier-1 (McKinsey / BCG)
está diseñado específicamente para Comités de Dirección (C-Level), Consejos de Administración
y Comités de Adquisición/Inversión corporativos.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx
  Libro de trabajo analítico en Excel con 4 pestañas estructuradas e interconectadas:
  - Pestaña 1: Dashboard Ejecutivo (Cabecera directiva, comparativa de 5 alternativas, 
               estado de veto, score ponderado 0-100, ranking dinámico, dictamen del comité,
               gráfico comparativo por pilares y tarjetas de recomendación ejecutiva).
  - Pestaña 2: Filtros Veto (Must-Haves) (Tabla de 6 criterios no negociables de exclusión 
               binaria CUMPLE/NO CUMPLE, control automático de incumplimientos y multiplicador 
               booleano de viabilidad Vk).
  - Pestaña 3: Scoring Ponderado (Wants) (Matriz de 13 criterios ponderados agrupados en 4 pilares: 
               Ajuste Técnico 30%, TCO 3 Años 25%, SLA & Solvencia 20%, y Seguridad/Roadmap 25%, 
               con validación de notas 1-10 y control estricto de suma 100%).
  - Pestaña 4: Sensibilidad & Auditoría (Simulador What-If con 5 escenarios de estrés de pesos, 
               registro de auditoría cualitativa de notas, acta de consenso y bloque de firmas C-Level).

• Presentacion_DAR_CLevel_ES.pptx
  Presentación ejecutiva panorámica (16:9 widescreen) bajo la Pirámide de Minto (3 diapositivas):
  - Diapositiva 1: Síntesis Ejecutiva & Veredicto DAR (4 KPI Cards y fundamentos de adjudicación).
  - Diapositiva 2: Matriz de Trade-Offs & Evidencia Comparativa (Tabla analítica, gráfico comparativo y trade-offs).
  - Diapositiva 3: Roadmap de Transición & Board Decision Gateway (Cronograma Q1-Q4, 4 acuerdos vinculantes y firmas).

• Guia_Metodologica_DAR_ES.pdf
  Guía metodológica oficial de 5 páginas con fundamentación matemática formal del factor booleano Vk 
  y la suma ponderada normalizada Sk, protocolo para neutralizar el sesgo de autoindulgencia, 
  caso de estudio resuelto (Horizon Global Logistics con impacto en TCO) y FAQ de defensa ante el Consejo.

--------------------------------------------------------------------------------
2. CONTRASEÑA OFICIAL Y PROTECCIÓN DE CELDAS
--------------------------------------------------------------------------------
Para garantizar la integridad del modelo durante deliberaciones ejecutivas y evitar la 
alteración accidental de fórmulas y rankings, las celdas de cálculo y cabeceras están protegidas.

Todas las celdas de entrada de datos (nombres de alternativas, selectores CUMPLE/NO CUMPLE, 
ponderaciones porcentuales %, calificaciones del 1 al 10, notas de auditoría y nombres) 
están 100% DESBLOQUEADAS para su libre edición e interacción directa.

Si necesitas desproteger las hojas para realizar ampliaciones estructurales en Excel, 
la contraseña oficial del modelo es:
  {PASSWORD_OFFICIAL}

--------------------------------------------------------------------------------
3. COMPATIBILIDAD CON GOOGLE SHEETS
--------------------------------------------------------------------------------
El archivo Excel utiliza exclusivamente funciones nativas compatibles al 100% con Google Drive 
y Google Sheets (ver archivo adjunto LEEME_ACCESO_GOOGLE_SHEETS.txt en la raíz del paquete).

--------------------------------------------------------------------------------
4. CONTACTO Y ASESORÍA ESTRATÉGICA
--------------------------------------------------------------------------------
Para workshops de facilitación con Comités de Dirección o modelización ad-hoc:
• Web: https://datalaria.com
• Email Corporativo de Soporte: {SUPPORT_EMAIL}
• LinkedIn: https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/

© 2026 Datalaria. Todos los derechos reservados.
"""

README_INSTRUCTIONS_EN = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Quantitative DAR Matrix: Decision Analysis & Resolution, Veto Criteria & Multi-Criteria Scoring
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite provides Tier-1 management consulting decision-support tools tailored 
for C-Suite committees, Boards of Directors, and Corporate Investment / Procurement Committees.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Quantitative_DAR_Matrix_Datalaria_EN.xlsx
  Comprehensive 4-tab strategic workbook:
  - Tab 1: Executive Dashboard (C-Suite metadata header, 5-alternative comparative table, 
           veto viability status, 0-100 weighted score, dynamic ranking, committee verdict, 
           visual pillar comparison chart, and executive recommendation cards).
  - Tab 2: Veto Criteria (Must-Haves) (6 non-negotiable binary gatekeeper criteria with PASS/FAIL 
           dropdown validation, automated breach count, and Boolean gatekeeper factor Vk).
  - Tab 3: Weighted Scoring (Wants) (13 weighted criteria grouped into 4 strategic pillars: 
           Technical Fit 30%, 3-Year TCO 25%, SLA & Stability 20%, and Security/Roadmap 25%, 
           with 1-10 scoring validation and 100% sum check).
  - Tab 4: Sensitivity & Audit Trail (What-If stress test across 5 weighting scenarios, 
           qualitative evidence audit trail, consensus minutes, and formal C-Suite sign-off block).

• Deck_DAR_CLevel_EN.pptx
  Executive widescreen presentation (16:9 widescreen) structured under Minto Pyramid Principle (3 slides):
  - Slide 1: Executive Synthesis & DAR Verdict (4 KPI cards and award rationale).
  - Slide 2: Trade-Off Matrix & Comparative Evidence (Executive table, high-res chart, and trade-off dynamics).
  - Slide 3: Transition Roadmap & Board Decision Gateway (Q1-Q4 transition timeline, 4 binding resolutions, and signatures).

• Methodology_Guide_DAR_EN.pdf
  Official 5-page executive methodology guide with formal mathematical proof of the Boolean gatekeeper Vk 
  and normalized score Sk, weight calibration protocol (Kepner-Tregoe AHP), solved enterprise case study 
  (Horizon Global Logistics TCO optimization), and Boardroom Defense FAQ.

--------------------------------------------------------------------------------
2. MASTER PASSWORD & CELL PROTECTION
--------------------------------------------------------------------------------
To safeguard model integrity during executive presentations and prevent accidental formula corruption, 
calculation cells and headers are protected.

All user input cells (alternative names, PASS/FAIL dropdowns, percentage weights %, 
1 to 10 ratings, qualitative audit evidence, and signatory names) are 100% UNLOCKED 
for free editing and data entry.

If you need to unprotect the worksheets for structural expansions in Microsoft Excel, 
the official model password is:
  {PASSWORD_OFFICIAL}

--------------------------------------------------------------------------------
3. GOOGLE SHEETS COMPATIBILITY
--------------------------------------------------------------------------------
The Excel workbook uses standard native formulas fully compatible with Google Drive 
and Google Sheets (see README_GOOGLE_SHEETS_ACCESS.txt at the root of this archive).

--------------------------------------------------------------------------------
4. CORPORATE CONTACT & EXECUTIVE ADVISORY
--------------------------------------------------------------------------------
For steering committee facilitation workshops or custom decision modeling:
• Web: https://datalaria.com
• Corporate Support Email: {SUPPORT_EMAIL}
• LinkedIn: https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/

© 2026 Datalaria. All rights reserved.
"""

LEEME_GOOGLE_SHEETS = """================================================================================
DATALARIA | GUÍA DE IMPORTACIÓN Y USO EN GOOGLE SHEETS
================================================================================

La plantilla Excel (.xlsx) del Executive Decision Pack ha sido diseñada bajo estrictos 
estándares de compatibilidad para funcionar con total fluidez tanto en Microsoft Excel 
como en Google Sheets:

1. Abre tu navegador web y accede a Google Drive (https://drive.google.com).
2. Haz clic en el botón "+ Nuevo" en la esquina superior izquierda y selecciona "Subir archivo".
3. Selecciona el archivo:
   - "Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx" (o la versión en inglés).
4. Una vez completada la subida, haz doble clic sobre el archivo en tu unidad de Drive.
5. Haz clic en "Abrir con Hojas de cálculo de Google" en la barra superior.
6. ¡Listo! Todas las fórmulas matriciales, ponderaciones SUMAPRODUCTO, semáforos lógicos 
   y vínculos entre pestañas operarán de manera completamente nativa.

Nota: Si deseas desproteger las hojas dentro de Google Sheets para personalizar filas 
o columnas, accede a Datos > Hojas y rangos protegidos e introduce la contraseña oficial 
documentada en LEEME_INSTRUCCIONES.txt (Datalaria2026).
"""

README_GOOGLE_SHEETS = """================================================================================
DATALARIA | GOOGLE SHEETS IMPORT & ACCESS GUIDE
================================================================================

The Executive Decision Pack Excel workbook (.xlsx) is engineered for 100% native 
compatibility with Google Drive and Google Sheets without any proprietary macros:

1. Open your web browser and navigate to Google Drive (https://drive.google.com).
2. Click "+ New" in the top-left corner and select "File upload".
3. Select the workbook:
   - "Quantitative_DAR_Matrix_Datalaria_EN.xlsx" (or the Spanish edition).
4. Once uploaded, double-click the file in your Google Drive list.
5. Click "Open with Google Sheets" at the top center.
6. All matrix formulas, SUMPRODUCT calculations, logic checks, and cross-tab linkages will function natively.

Note: To unprotect sheets within Google Sheets for structural customizations, navigate to 
Data > Protected sheets and ranges and enter the master password documented in 
README_INSTRUCTIONS.txt (Datalaria2026).
"""


def write_text_files():
    # Escribir archivos de texto en sus carpetas respectivas
    path_txt_es = os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt")
    with open(path_txt_es, "w", encoding="utf-8") as f:
        f.write(LEEME_INSTRUCCIONES_ES)
    print(f"[OK] Generado: {path_txt_es}")

    path_txt_en = os.path.join(DIR_EN, "README_INSTRUCTIONS.txt")
    with open(path_txt_en, "w", encoding="utf-8") as f:
        f.write(README_INSTRUCTIONS_EN)
    print(f"[OK] Generado: {path_txt_en}")

    path_gs_es = os.path.join(DIR_PACK, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
    with open(path_gs_es, "w", encoding="utf-8") as f:
        f.write(LEEME_GOOGLE_SHEETS)
    print(f"[OK] Generado: {path_gs_es}")

    path_gs_en = os.path.join(DIR_PACK, "README_GOOGLE_SHEETS_ACCESS.txt")
    with open(path_gs_en, "w", encoding="utf-8") as f:
        f.write(README_GOOGLE_SHEETS)
    print(f"[OK] Generado: {path_gs_en}")


def build_zip_package():
    os.makedirs(DIR_LEMON, exist_ok=True)
    os.makedirs(DIR_PACK, exist_ok=True)

    print(f"Construyendo paquete ZIP maestro: {ZIP_PATH_LOCAL}...")

    # Archivos a incluir con su ruta interna en el ZIP
    files_to_pack = [
        # Carpeta ES
        (os.path.join(DIR_ES, "Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx"), "[ES]_Matriz_DAR/Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx"),
        (os.path.join(DIR_ES, "Presentacion_DAR_CLevel_ES.pptx"), "[ES]_Matriz_DAR/Presentacion_DAR_CLevel_ES.pptx"),
        (os.path.join(DIR_ES, "Guia_Metodologica_DAR_ES.pdf"), "[ES]_Matriz_DAR/Guia_Metodologica_DAR_ES.pdf"),
        (os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt"), "[ES]_Matriz_DAR/LEEME_INSTRUCCIONES.txt"),
        # Carpeta EN
        (os.path.join(DIR_EN, "Quantitative_DAR_Matrix_Datalaria_EN.xlsx"), "[EN]_Quantitative_DAR/Quantitative_DAR_Matrix_Datalaria_EN.xlsx"),
        (os.path.join(DIR_EN, "Deck_DAR_CLevel_EN.pptx"), "[EN]_Quantitative_DAR/Deck_DAR_CLevel_EN.pptx"),
        (os.path.join(DIR_EN, "Methodology_Guide_DAR_EN.pdf"), "[EN]_Quantitative_DAR/Methodology_Guide_DAR_EN.pdf"),
        (os.path.join(DIR_EN, "README_INSTRUCTIONS.txt"), "[EN]_Quantitative_DAR/README_INSTRUCTIONS.txt"),
        # Raíz del ZIP
        (os.path.join(DIR_PACK, "LEEME_ACCESO_GOOGLE_SHEETS.txt"), "LEEME_ACCESO_GOOGLE_SHEETS.txt"),
        (os.path.join(DIR_PACK, "README_GOOGLE_SHEETS_ACCESS.txt"), "README_GOOGLE_SHEETS_ACCESS.txt"),
    ]

    # Verificar existencia de archivos
    for src, arc in files_to_pack:
        if not os.path.exists(src):
            raise FileNotFoundError(f"Archivo requerido no encontrado: {src}")

    # Crear ZIP
    with zipfile.ZipFile(ZIP_PATH_LOCAL, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for src, arc in files_to_pack:
            zf.write(src, arcname=arc)
            print(f"  + Añadido a ZIP: {arc}")

    size_kb = os.path.getsize(ZIP_PATH_LOCAL) / 1024
    print(f"[OK] Archivo ZIP local creado con éxito: {ZIP_PATH_LOCAL} ({size_kb:.1f} KB)")

    # Copiar al hub de Lemon Squeezy
    shutil.copy2(ZIP_PATH_LOCAL, ZIP_PATH_LEMON)
    print(f"[OK] Copia sincronizada en el hub Lemon Squeezy: {ZIP_PATH_LEMON}")

    # SEGURIDAD: Verificar que NO existe ningún zip en static/downloads o public/downloads
    for unsafe_dir in ["static/downloads", "public/downloads"]:
        if os.path.exists(unsafe_dir):
            for fname in os.listdir(unsafe_dir):
                if "DAR" in fname or fname.endswith(".zip"):
                    bad_file = os.path.join(unsafe_dir, fname)
                    os.remove(bad_file)
                    print(f"[ALERTA DE SEGURIDAD ELIMINADA] Archivo eliminado de ruta pública: {bad_file}")


def main():
    print("Iniciando proceso de empaquetado oficial DAR...")
    write_text_files()
    build_zip_package()
    print("Empaquetado completado exitosamente.")


if __name__ == "__main__":
    main()
