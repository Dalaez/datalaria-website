#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los activos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE/Executive_Decision_Pack_AMFE_Riesgos_Dual.zip
- Copia directa en packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_AMFE_Riesgos_Dual.zip

Estructura del archivo ZIP:
- [ES]_Matriz_Riesgos_AMFE/
  - Matriz_Riesgos_AMFE_Datalaria_ES.xlsx
  - Presentacion_AMFE_Riesgos_CLevel_ES.pptx
  - Guia_Metodologica_AMFE_Riesgos_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- [EN]_FMEA_Risk_Matrix/
  - Quantitative_Risk_Matrix_FMEA_EN.xlsx
  - Deck_FMEA_Risk_CLevel_EN.pptx
  - Methodology_Guide_FMEA_Risk_EN.pdf
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

DIR_PACK = "packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE"
DIR_ES = os.path.join(DIR_PACK, "[ES]_Matriz_Riesgos_AMFE")
DIR_EN = os.path.join(DIR_PACK, "[EN]_FMEA_Risk_Matrix")
DIR_LEMON = "packages/00_DISTRIBUCION_LEMONSQUEEZY"

ZIP_NAME = "Executive_Decision_Pack_AMFE_Riesgos_Dual.zip"
ZIP_PATH_LOCAL = os.path.join(DIR_PACK, ZIP_NAME)
ZIP_PATH_LEMON = os.path.join(DIR_LEMON, ZIP_NAME)

PASSWORD_OFFICIAL = "Datalaria2026"
SUPPORT_EMAIL = "datalaria@gmail.com"

LEEME_INSTRUCCIONES_ES = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Matriz de Riesgos Cuantitativa & AMFE / FMEA Operativo
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas analíticas de grado directivo y de consultoría Tier-1
(estándar ISO 31000:2018 / AIAG-VDA 2019 / IATF 16949 / COSO ERM) está diseñado
específicamente para Directores de Operaciones (COO), Directores de Riesgos (CRO),
Chief Information Security Officers (CISO), CFOs y Comités de Auditoría.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Matriz_Riesgos_AMFE_Datalaria_ES.xlsx
  Libro de trabajo analítico en Excel con 4 pestañas funcionales estructuradas:
  - Pestaña 1: Dashboard Ejecutivo (4 KPI Cards C-Level, Matriz de Calor 5x5 dinámica
               con conteo automático por cuadrante y resumen Pareto de fallos críticos).
  - Pestaña 2: Matriz de Riesgos 5x5 (Registro corporativo de 20 eventos categorizados
               con puntuación de impacto y probabilidad inherente y residual post-mitigación).
  - Pestaña 3: AMFE Operativo (Análisis tridimensional de Modos de Fallo y Efectos:
               Severidad S x Ocurrencia O x Detección D = NPR 1 a 1000, clasificación
               de Prioridad de Acción AIAG-VDA, plan de controles y % reducción residual).
  - Pestaña 4: Plan de Mitigación & CAPEX (Asignación presupuestaria por control, cálculo
               de pérdida esperada evitada ΔE(L), ROI actuarial del control CER y estado).

• Presentacion_AMFE_Riesgos_CLevel_ES.pptx
  Presentación panorámica (16:9 widescreen) estructurada bajo la Pirámide de Minto (3 slides):
  - Diapositiva 1: Diagnóstico Ejecutivo & Exposición al Riesgo (4 KPI Cards y análisis actuarial).
  - Diapositiva 2: Matriz de Calor 5x5 Térmica & Curva Pareto de Modos de Fallo AIAG-VDA.
  - Diapositiva 3: Cronograma de Controles Q1-Q4 & Board Decision Gateway con 4 resoluciones y firmas.

• Guia_Metodologica_AMFE_Riesgos_ES.pdf
  Guía metodológica oficial de 5 páginas con la fundamentación matemática del modelo
  cuantitativo, demostración de E(L), dinámica del NPR, baremos objetivos 1-10, caso de estudio
  de alta resiliencia cloud y protocolo de defensa ante el Comité de Dirección.

--------------------------------------------------------------------------------
2. POLÍTICA DE PROTECCIÓN DE CELDAS & CONTRASEÑA OFICIAL
--------------------------------------------------------------------------------
Para garantizar la integridad matemática del modelo y evitar sobreescrituras accidentales
en fórmulas matriciales y de NPR, las hojas del libro de Excel se entregan protegidas
bajo el estándar OpenXML ECMA-376:

• CELDAS DE ENTRADA (Fondo Blanco #FFFFFF):
  Completamente desbloqueadas. Puede editar libremente nombres de riesgos, procesos,
  descripciones, causas raíz, controles, puntuaciones (P, I, S, O, D), responsables y costes.

• CELDAS DE FÓRMULAS & CABECERAS (Fondo Gris #F1F5F9 o Corporativo):
  Protegidas contra modificaciones involuntarias.

• CONTRASEÑA OFICIAL DE DESPROTECCIÓN:
  {PASSWORD_OFFICIAL}

  Para desproteger cualquier hoja en Microsoft Excel:
  Pestaña "Revisar" -> "Desproteger hoja" -> Introducir: {PASSWORD_OFFICIAL}

--------------------------------------------------------------------------------
3. SOPORTE TÉCNICO & CONSULTAS
--------------------------------------------------------------------------------
Si tiene alguna duda sobre la parametrización de sus modelos de riesgo o requiere soporte:
• Email de soporte: {SUPPORT_EMAIL}
• Web oficial: https://datalaria.com
"""

README_INSTRUCTIONS_EN = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Quantitative Risk Matrix & Operational FMEA
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This corporate risk analytics and operational quality toolkit meets Tier-1 standards
(ISO 31000:2018 / AIAG-VDA 2019 / IATF 16949 / COSO ERM) and is specifically
engineered for Chief Operating Officers (COO), Chief Risk Officers (CRO),
CISOs, CFOs, and Board Audit Committees.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Quantitative_Risk_Matrix_FMEA_EN.xlsx
  Analytical Excel workbook featuring 4 structured worksheets:
  - Sheet 1: Executive Dashboard (4 C-Level KPI Cards, dynamic 5x5 Heat Map with
             automated quadrant counts, and Pareto failure mode criticality ranking).
  - Sheet 2: 5x5 Risk Matrix (Audited 20-risk enterprise registry with inherent and
             residual scoring post-mitigation strategy).
  - Sheet 3: Operational FMEA (Three-dimensional Failure Mode and Effects Analysis:
             Severity S x Occurrence O x Detection D = RPN 1 to 1000, AIAG-VDA Action
             Priority triage, mitigation roadmaps, and residual risk reduction %).
  - Sheet 4: Mitigation Plan & CAPEX (Control budget allocation, expected financial
             loss reduction ΔE(L), actuarial control ROI ratio CER, and Q1-Q4 schedules).

• Deck_FMEA_Risk_CLevel_EN.pptx
  Executive 16:9 widescreen presentation structured under the Minto Pyramid (3 slides):
  - Slide 1: Executive Diagnosis & Risk Exposure (4 KPI Cards and actuarial findings).
  - Slide 2: 5x5 Thermal Heatmap & AIAG-VDA Failure Modes Pareto Curve.
  - Slide 3: Q1-Q4 Preventive Controls Roadmap & Board Decision Gateway (4 binding resolutions).

• Methodology_Guide_FMEA_Risk_EN.pdf
  Official 5-page editorial methodology guide detailing mathematical foundations,
  actuarial E(L) equations, RPN continuous dynamics, 1-10 objective scoring tables,
  mission-critical cloud resiliency case study, and boardroom defense FAQ.

--------------------------------------------------------------------------------
2. CELL PROTECTION POLICY & OFFICIAL PASSWORD
--------------------------------------------------------------------------------
To safeguard mathematical integrity and prevent accidental formula corruption,
worksheets are protected according to ECMA-376 OpenXML standards:

• INPUT CELLS (White Fill #FFFFFF):
  Fully unlocked. You can freely edit risk names, processes, failure modes, root causes,
  controls, scoring ratings (P, I, S, O, D), owners, and CAPEX budgets.

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
3. Seleccione el archivo "Matriz_Riesgos_AMFE_Datalaria_ES.xlsx" (o la versión en inglés).
4. Haga doble clic en el archivo subido en Google Drive.
5. Haga clic en el botón superior "Abrir con Hojas de cálculo de Google".
6. ¡Listo! Todas las fórmulas (COUNTIFS, COUNTIF, SUM, AVERAGE, MAX, IF, OR) y el formato
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
3. Select "Quantitative_Risk_Matrix_FMEA_EN.xlsx" (or the Spanish version).
4. Double-click the uploaded file in Google Drive.
5. Click the top button "Open with Google Sheets".
6. Completed! All formulas (COUNTIFS, COUNTIF, SUM, AVERAGE, MAX, IF, OR) and conditional
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

    print("\n[2/3] Empaquetando Executive_Decision_Pack_AMFE_Riesgos_Dual.zip...")
    os.makedirs(DIR_LEMON, exist_ok=True)

    files_to_pack = [
        # Subcarpeta ES
        (os.path.join(DIR_ES, "Matriz_Riesgos_AMFE_Datalaria_ES.xlsx"), "[ES]_Matriz_Riesgos_AMFE/Matriz_Riesgos_AMFE_Datalaria_ES.xlsx"),
        (os.path.join(DIR_ES, "Presentacion_AMFE_Riesgos_CLevel_ES.pptx"), "[ES]_Matriz_Riesgos_AMFE/Presentacion_AMFE_Riesgos_CLevel_ES.pptx"),
        (os.path.join(DIR_ES, "Guia_Metodologica_AMFE_Riesgos_ES.pdf"), "[ES]_Matriz_Riesgos_AMFE/Guia_Metodologica_AMFE_Riesgos_ES.pdf"),
        (os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt"), "[ES]_Matriz_Riesgos_AMFE/LEEME_INSTRUCCIONES.txt"),
        
        # Subcarpeta EN
        (os.path.join(DIR_EN, "Quantitative_Risk_Matrix_FMEA_EN.xlsx"), "[EN]_FMEA_Risk_Matrix/Quantitative_Risk_Matrix_FMEA_EN.xlsx"),
        (os.path.join(DIR_EN, "Deck_FMEA_Risk_CLevel_EN.pptx"), "[EN]_FMEA_Risk_Matrix/Deck_FMEA_Risk_CLevel_EN.pptx"),
        (os.path.join(DIR_EN, "Methodology_Guide_FMEA_Risk_EN.pdf"), "[EN]_FMEA_Risk_Matrix/Methodology_Guide_FMEA_Risk_EN.pdf"),
        (os.path.join(DIR_EN, "README_INSTRUCTIONS.txt"), "[EN]_FMEA_Risk_Matrix/README_INSTRUCTIONS.txt"),

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
