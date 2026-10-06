#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los activos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos/Executive_Decision_Pack_PERT_Dual.zip
- Copia directa en packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_PERT_Dual.zip

Estructura del archivo ZIP:
- [ES]_Estimacion_PERT_3_Puntos/
  - Estimacion_PERT_Estocastica_ES.xlsx
  - Presentacion_PERT_CLevel_ES.pptx
  - Guia_Metodologica_PERT_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- [EN]_3Point_PERT_Estimation/
  - Stochastic_PERT_Estimation_EN.xlsx
  - Deck_PERT_CLevel_EN.pptx
  - Methodology_Guide_PERT_EN.pdf
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

DIR_PACK = "packages/Suite_03_Control_Operativo/03_Estimacion_PERT_3_Puntos"
DIR_ES = os.path.join(DIR_PACK, "[ES]_Estimacion_PERT_3_Puntos")
DIR_EN = os.path.join(DIR_PACK, "[EN]_3Point_PERT_Estimation")
DIR_LEMON = "packages/00_DISTRIBUCION_LEMONSQUEEZY"

ZIP_NAME = "Executive_Decision_Pack_PERT_Dual.zip"
ZIP_PATH_LOCAL = os.path.join(DIR_PACK, ZIP_NAME)
ZIP_PATH_LEMON = os.path.join(DIR_LEMON, ZIP_NAME)

PASSWORD_OFFICIAL = "Datalaria2026"
SUPPORT_EMAIL = "datalaria@gmail.com"

LEEME_INSTRUCCIONES_ES = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Estimación PERT de 3 Puntos Estocástica & Probabilidad de Cronograma
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas analíticas de grado directivo y de consultoría Tier-1
(estándar PMBOK 7th / Operations Research / Teoría de Restricciones TOC) está diseñado
específicamente para Directores de Operaciones (COO), Directores de Proyecto (PMO),
Chief Information Officers (CIO), sponsors ejecutivos y Comités de Dirección.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Estimacion_PERT_Estocastica_ES.xlsx
  Libro de trabajo analítico en Excel con 4 pestañas funcionales estructuradas:
  - Pestaña 1: Dashboard Ejecutivo (Tarjetas KPI C-Level: μ_total, σ_total, intervalo 95%,
               calculadora interactiva de fecha compromiso con Z-Score y probabilidad,
               semáforo directivo y gráfico dinámico de curva de campana normal).
  - Pestaña 2: Estimación WBS 3 Puntos (Registro de 25 paquetes de trabajo WBS, entradas
               desbloqueadas o, m, p, cálculo automático de media Beta, media triangular,
               desviación estándar, varianza, rango y sesgo de asimetría).
  - Pestaña 3: Camino Crítico & Análisis Z (Agregación estocástica por Teorema del Límite
               Central CLT: Σ μ_crit, Σ σ²_crit, tabla de escenarios de certidumbre al
               50%, 60%, 70%, 75%, 80%, 85%, 90%, 95% y 99% con recomendación de gobernanza).
  - Pestaña 4: Buffers & Plan de Aceleración (Dimensionamiento científico de colchones TOC
               frente al método Goldratt, matriz de Crashing con coste por día reducido,
               priorización económica y resoluciones para el Board).

• Presentacion_PERT_CLevel_ES.pptx
  Presentación panorámica (16:9 widescreen) estructurada bajo la Pirámide de Minto (3 slides):
  - Diapositiva 1: Diagnóstico Ejecutivo & Riesgo de Cronograma (4 KPI Cards y contraste
                   entre la trampa determinista y la gobernanza estocástica).
  - Diapositiva 2: Curva de Densidad de Probabilidad & Gráfico Tornado de Sensibilidad (Top 5
                   tareas críticas que concentran el 75% de la incertidumbre global).
  - Diapositiva 3: Estrategia de Buffers, Protocolo de Crashing & Board Decision Gateway con
                   4 resoluciones vinculantes y firmas de aprobación (CEO, COO, CFO, Sponsor).

• Guia_Metodologica_PERT_ES.pdf
  Guía metodológica oficial de 5 páginas con la demostración matemática de la Distribución
  Beta, agregación cuadrática del CLT, protocolo de entrevista pre-mortem para eliminar el
  sesgo de optimismo, caso de estudio corporativo de modernización core y FAQ directivas.

--------------------------------------------------------------------------------
2. POLÍTICA DE PROTECCIÓN DE CELDAS & CONTRASEÑA OFICIAL
--------------------------------------------------------------------------------
Para garantizar la integridad matemática del modelo y evitar sobreescrituras accidentales
en fórmulas estadísticas y de camino crítico, las hojas del libro de Excel se entregan
protegidas bajo el estándar OpenXML ECMA-376:

• CELDAS DE ENTRADA (Fondo Blanco #FFFFFF):
  Completamente desbloqueadas. Puede editar libremente nombres de paquetes de trabajo,
  pertenencia al camino crítico (SÍ/NO), valores de estimación (o, m, p), fecha compromiso Td,
  costes de crashing y notas de gobernanza.

• CELDAS DE FÓRMULAS & CABECERAS (Fondo Gris #F1F5F9 o Corporativo):
  Protegidas contra modificaciones involuntarias.

• CONTRASEÑA OFICIAL DE DESPROTECCIÓN:
  {PASSWORD_OFFICIAL}

  Para desproteger cualquier hoja en Microsoft Excel:
  Pestaña "Revisar" -> "Desproteger hoja" -> Introducir: {PASSWORD_OFFICIAL}

--------------------------------------------------------------------------------
3. SOPORTE TÉCNICO & CONSULTAS
--------------------------------------------------------------------------------
Si tiene alguna duda sobre la parametrización de sus cronogramas o requiere soporte:
• Email de soporte: {SUPPORT_EMAIL}
• Web oficial: https://datalaria.com
"""

README_INSTRUCTIONS_EN = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Stochastic 3-Point PERT Estimation & Schedule Risk Probability
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite of Tier-1 executive analytical tools (PMBOK 7th Guide / Operations Research /
Theory of Constraints TOC standards) is purpose-built for Chief Operating Officers (COO),
PMO Directors, Chief Information Officers (CIO), project sponsors, and Executive Boards.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Stochastic_PERT_Estimation_EN.xlsx
  Comprehensive Excel workbook with 4 structured functional tabs:
  - Tab 1: Executive Dashboard (C-Level KPI Cards: μ_total, σ_total, 95% interval,
           interactive deadline calculator with Z-Score and success probability,
           traffic light governance diagnosis, and dynamic bell curve chart).
  - Tab 2: WBS 3-Point Estimation (25 work package register, unlocked user inputs for
           o, m, p, automated Beta mean, triangular mean, standard deviation,
           variance, uncertainty range, and skewness ratio).
  - Tab 3: Critical Path & Z-Score (Central Limit Theorem CLT aggregation: Σ μ_crit,
           Σ σ²_crit, confidence scenario table for 50%, 60%, 70%, 75%, 80%, 85%,
           90%, 95%, and 99% certainty with governance recommendations).
  - Tab 4: Schedule Buffers & Crashing (Scientific TOC buffer sizing vs Goldratt 50% cut,
           crashing matrix with marginal cost per day reduced, and economic prioritization).

• Deck_PERT_CLevel_EN.pptx
  Executive 16:9 widescreen presentation following Minto Pyramid structure (3 slides):
  - Slide 1: Executive Diagnosis & Schedule Risk (4 KPI Cards, single-point trap vs
             stochastic governance).
  - Slide 2: Probability Density Bell Curve & Tornado Sensitivity Chart (Top 5 critical
             tasks driving 75% of global schedule variance).
  - Slide 3: Buffer Sizing, Crashing Protocol & Board Decision Gateway with 4 binding
             resolutions and formal sign-off boxes (CEO, COO, CFO, Sponsor).

• Methodology_Guide_PERT_EN.pdf
  Official 5-page editorial methodology guide covering Beta distribution mathematics,
  CLT variance aggregation, structured pre-mortem elicitation protocol to eliminate
  anchoring bias, core platform case study, and boardroom defense FAQ.

--------------------------------------------------------------------------------
2. CELL PROTECTION POLICY & OFFICIAL PASSWORD
--------------------------------------------------------------------------------
To safeguard mathematical integrity and prevent accidental formula corruption,
worksheets are protected according to ECMA-376 OpenXML standards:

• INPUT CELLS (White Fill #FFFFFF):
  Fully unlocked. You can freely edit task names, critical path indicators (YES/NO),
  estimates (o, m, p), target deadline Td, crashing costs, and governance notes.

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
3. Seleccione el archivo "Estimacion_PERT_Estocastica_ES.xlsx" (o la versión en inglés).
4. Haga doble clic en el archivo subido en Google Drive.
5. Haga clic en el botón superior "Abrir con Hojas de cálculo de Google".
6. ¡Listo! Todas las fórmulas estadísticas (NORMDIST, NORMINV, SQRT, SUMIF, ROUND)
   y los gráficos funcionarán de forma fluida y en tiempo real.

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
3. Select "Stochastic_PERT_Estimation_EN.xlsx" (or the Spanish version).
4. Double-click the uploaded file in Google Drive.
5. Click the top button "Open with Google Sheets".
6. Completed! All statistical formulas (NORMDIST, NORMINV, SQRT, SUMIF, ROUND)
   and charts will recalculate seamlessly in real time.

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

    print("\n[2/3] Empaquetando Executive_Decision_Pack_PERT_Dual.zip...")
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
            "Estimacion_PERT_Estocastica_ES.xlsx",
            "Presentacion_PERT_CLevel_ES.pptx",
            "Guia_Metodologica_PERT_ES.pdf",
            "LEEME_INSTRUCCIONES.txt"
        ]
        for ef in es_files:
            ef_path = os.path.join(DIR_ES, ef)
            if os.path.exists(ef_path):
                arc_name = os.path.join("[ES]_Estimacion_PERT_3_Puntos", ef)
                zipf.write(ef_path, arcname=arc_name)
                print(f"  + [ES]: {ef}")
            else:
                print(f"  ! ALERTA: No se encontró {ef_path}")

        # 3. Archivos en carpeta EN
        en_files = [
            "Stochastic_PERT_Estimation_EN.xlsx",
            "Deck_PERT_CLevel_EN.pptx",
            "Methodology_Guide_PERT_EN.pdf",
            "README_INSTRUCTIONS.txt"
        ]
        for ef in en_files:
            ef_path = os.path.join(DIR_EN, ef)
            if os.path.exists(ef_path):
                arc_name = os.path.join("[EN]_3Point_PERT_Estimation", ef)
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
        "static/downloads/Executive_Decision_Pack_PERT_Dual.zip",
        "public/downloads/Executive_Decision_Pack_PERT_Dual.zip"
    ]
    for fb in forbidden_paths:
        if os.path.exists(fb):
            os.remove(fb)
            print(f"  ! Eliminado archivo en ruta pública no permitida: {fb}")

    print("\nEmpaquetado completado con éxito y conformidad de seguridad 100%.")


if __name__ == "__main__":
    build_master_zip()
