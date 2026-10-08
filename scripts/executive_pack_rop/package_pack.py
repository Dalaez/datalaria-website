#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los activos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial privada en Lemon Squeezy:
- packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/Executive_Decision_Pack_Stock_ROP_Dual.zip
- Copia directa en packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_Stock_ROP_Dual.zip

Estructura del archivo ZIP:
- [ES]_Stock_Seguridad_ROP/
  - Calculadora_Stock_Seguridad_ROP_ES.xlsx
  - Presentacion_Stock_ROP_CLevel_ES.pptx
  - Guia_Metodologica_Stock_ROP_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- [EN]_Safety_Stock_ROP/
  - Safety_Stock_ROP_Calculator_EN.xlsx
  - Deck_Safety_Stock_ROP_CLevel_EN.pptx
  - Methodology_Guide_Safety_Stock_ROP_EN.pdf
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

DIR_PACK = "packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP"
DIR_ES = os.path.join(DIR_PACK, "[ES]_Stock_Seguridad_ROP")
DIR_EN = os.path.join(DIR_PACK, "[EN]_Safety_Stock_ROP")
DIR_LEMON = "packages/00_DISTRIBUCION_LEMONSQUEEZY"

ZIP_NAME = "Executive_Decision_Pack_Stock_ROP_Dual.zip"
ZIP_PATH_LOCAL = os.path.join(DIR_PACK, ZIP_NAME)
ZIP_PATH_LEMON = os.path.join(DIR_LEMON, ZIP_NAME)

PASSWORD_OFFICIAL = "Datalaria2026"
SUPPORT_EMAIL = "datalaria@gmail.com"

LEEME_INSTRUCCIONES_ES = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Calculadora de Stock de Seguridad & ROP: Optimización de Inventario & Nivel de Servicio
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas analíticas de grado directivo y consultoría Tier-1
(estándar APICS / ASCM / MIT Center for Transportation & Logistics) está diseñado
específicamente para Directores Generales (CEO), Directores Financieros (CFO),
Directores de Operaciones (COO), Directores de Cadena de Suministro (Supply Chain)
y Comités de Dirección.

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Calculadora_Stock_Seguridad_ROP_ES.xlsx
  Libro de trabajo analítico en Excel con 4 pestañas funcionales estructuradas:
  - Pestaña 1: Dashboard Ejecutivo (Tarjetas KPI C-Level: Inversión en SS, CSL Medio,
               Probabilidad de Rotura, Capital Liberable, SKUs en Riesgo; Gráfico
               dinámico Diente de Sierra / Sawtooth y Matriz de Distribución ABC).
  - Pestaña 2: Matriz SKU & Datos Operativos (Catálogo parametrizable de 35 referencias,
               entradas de usuario desbloqueadas para demanda d, dispersión σd,
               plazo proveedor L, impuntualidad σL, CSL objetivo, coste C, tasa h y coste S).
  - Pestaña 3: Motor Matemático SS & ROP (Modelos estocásticos 1, 2 y 3 integral,
               factor Z dinámico, Punto de Pedido ROP, lote económico EOQ de Wilson,
               benchmark contra reglas empíricas de 3 semanas y diagnóstico de riesgo).
  - Pestaña 4: Trade-offs de Working Capital (Curva asintótica de sensibilidad del 85%
               al 99.9%, demostración de rendimientos decrecientes y simulador de impacto
               de negociación de Lead Time y SLAs con proveedores).

• Presentacion_Stock_ROP_CLevel_ES.pptx
  Deck ejecutivo en formato panorámico 16:9 widescreen (3 diapositivas de alta dirección):
  - Diapositiva 1: Diagnóstico Ejecutivo de Inventario & Working Capital (4 KPI cards y
                   comparativa de choque: Regla Empírica vs. Modelo Estocástico).
  - Diapositiva 2: Dinámica Diente de Sierra & Curva Asintótica de Nivel de Servicio
                   (Gráfico Sawtooth con líneas de ROP y SS, y curva exponencial con matriz ABC).
  - Diapositiva 3: Plan de Compresión de Lead Time & Board Decision Gateway (3 Pilares
                   estratégicos de negociación, 4 resoluciones de Consejo y Cajas de Firma).

• Guia_Metodologica_Stock_ROP_ES.pdf
  Guía editorial de referencia ejecutiva de 5 páginas completas con fundamentación
  matemática estocástica, derivación de fórmulas, segmentación ABC, caso de estudio real
  con 220.000 € de caja liberada, protocolo de defensa en comité y bibliografía canónica.

• LEEME_INSTRUCCIONES.txt
  Este documento con las directrices operativas y la clave de protección.

--------------------------------------------------------------------------------
2. POLÍTICA DE PROTECCIÓN DE CELDAS & CONTRASEÑA OFICIAL
--------------------------------------------------------------------------------
Para garantizar la integridad matemática del modelo y evitar sobreescrituras accidentales
en fórmulas estocásticas y financieras, las hojas del libro de Excel se entregan
protegidas bajo el estándar OpenXML ECMA-376:

• CELDAS DE ENTRADA (Fondo Blanco #FFFFFF):
  Completamente desbloqueadas. Puede introducir sus propios SKUs, demandas medias,
  desviaciones estándar, plazos de entrega y costes unitarios con total libertad.

• CELDAS DE FÓRMULAS (Fondo Gris Claro #F1F5F9):
  Bloqueadas para lectura y cálculo automático transparente.

• CONTRASEÑA OFICIAL PARA DESPROTEGER HOJAS:
  Si su equipo directivo desea auditar, adaptar o ampliar la arquitectura del modelo:
  
  CONTRASEÑA: {PASSWORD_OFFICIAL}

  (Para desproteger en Excel: Pestaña 'Revisar' -> 'Desproteger hoja' -> Introducir contraseña).

--------------------------------------------------------------------------------
3. SOPORTE DIRECTIVO Y CONTACTO
--------------------------------------------------------------------------------
Para consultas metodológicas, soporte técnico o solicitudes de adaptación corporativa:
Correo Oficial: {SUPPORT_EMAIL}
Portal Ejecutivo: https://datalaria.com
"""

README_INSTRUCTIONS_EN = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Safety Stock & Reorder Point (ROP) Calculator: Inventory & Service Level Optimization
================================================================================

Thank you for purchasing the official Datalaria.com Executive Decision Pack.
This Tier-1 management consulting and analytical toolkit (APICS / ASCM / MIT Center
for Transportation & Logistics standards) is specifically designed for Chief
Executive Officers (CEOs), Chief Financial Officers (CFOs), Chief Operating Officers
(COOs), Supply Chain Directors, and Executive Investment Committees.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Safety_Stock_ROP_Calculator_EN.xlsx
  Comprehensive financial and operational Excel workbook featuring 4 functional tabs:
  - Tab 1: Executive Dashboard (C-Level KPI Cards: Total SS Capital, Weighted CSL,
           Stockout Probability, Releasable Working Capital, Critical SKUs at Risk;
           Dynamic Sawtooth Cycle Chart and Portfolio ABC Distribution Matrix).
  - Tab 2: SKU Matrix & Operational Inputs (Parametric catalog of 35 references,
           unlocked inputs for mean demand d, demand std dev σd, mean lead time L,
           supplier tardiness σL, target CSL, unit cost C, holding rate h, and order cost S).
  - Tab 3: Safety Stock & ROP Models (Stochastic Models 1, 2, and 3 full convolution,
           dynamic Z-Factor, Reorder Point ROP, Wilson EOQ lot sizing, benchmark
           against naive 3-week heuristic rules, and operational shortage diagnoses).
  - Tab 4: Working Capital Optimization (Asymptotic sensitivity curve from 85% to 99.9%,
           mathematical proof of diminishing returns, and supplier negotiation impact simulator).

• Deck_Safety_Stock_ROP_CLevel_EN.pptx
  Executive 16:9 widescreen presentation deck (3 high-impact boardroom slides):
  - Slide 1: Executive Inventory & Working Capital Diagnosis (4 KPI cards and
             side-by-side comparison: Empirical Guesswork vs. Stochastic Rigor).
  - Slide 2: Sawtooth Dynamics & Asymptotic Service Curve (Continuous replenishment
             Sawtooth chart with ROP/SS triggers and exponential capital curve).
  - Slide 3: Lead Time Compression Roadmap & Board Decision Gateway (3 Strategic
             negotiation pillars, 4 formal board resolutions, and Executive Sign-off boxes).

• Methodology_Guide_Safety_Stock_ROP_EN.pdf
  5-page executive reference guide covering mathematical stochastic proofs,
  ABC stratification protocols, real-world case study ($220k cash released, -45% stockouts),
  executive boardroom defense FAQ, and authoritative canonical references.

• README_INSTRUCTIONS.txt
  This operational instruction manual and official model unlock password.

--------------------------------------------------------------------------------
2. CELL PROTECTION POLICY & OFFICIAL PASSWORD
--------------------------------------------------------------------------------
To guarantee mathematical formula integrity and prevent accidental alterations to
complex stochastic convolution formulas, the Excel sheets are protected under the
OpenXML ECMA-376 standard:

• USER INPUT CELLS (Pure White Fill #FFFFFF):
  Completely unlocked. Enter your catalog SKUs, demands, lead times, standard deviations,
  and costs with total operational flexibility.

• FORMULA CELLS (Light Slate Fill #F1F5F9):
  Protected and locked for automated, transparent calculation.

• OFFICIAL WORKBOOK UNPROTECT PASSWORD:
  If your analytics team wishes to audit or customize internal equations:
  
  PASSWORD: {PASSWORD_OFFICIAL}

  (To unprotect in Excel: 'Review' tab -> 'Unprotect Sheet' -> Enter password).

--------------------------------------------------------------------------------
3. EXECUTIVE SUPPORT & INQUIRIES
--------------------------------------------------------------------------------
For methodological advisory, corporate customization, or technical support:
Official Support Email: {SUPPORT_EMAIL}
Executive Portal: https://datalaria.com
"""

LEEME_GOOGLE_SHEETS_ES = """================================================================================
DATALARIA | ACCESO Y COMPATIBILIDAD CON GOOGLE SHEETS
================================================================================

El libro analítico 'Calculadora_Stock_Seguridad_ROP_ES.xlsx' es 100% compatible
con Google Sheets y Microsoft 365 en la nube.

INSTRUCCIONES DE IMPORTACIÓN DIRECTA:
1. Abra Google Drive (https://drive.google.com).
2. Haga clic en '+ Nuevo' -> 'Subir archivo'.
3. Seleccione el archivo 'Calculadora_Stock_Seguridad_ROP_ES.xlsx'.
4. Haga doble clic sobre el archivo subido en Google Drive para abrirlo en Google Sheets.
5. Seleccione 'Archivo' -> 'Guardar como hoja de cálculo de Google'.

Todas las fórmulas estocásticas (NORM.S.INV, SQRT, SUM, AVERAGE, COUNTIF, etc.),
los vínculos entre hojas y el formato condicional se ejecutan de forma nativa e inmediata.
================================================================================
"""

README_GOOGLE_SHEETS_EN = """================================================================================
DATALARIA | GOOGLE SHEETS ACCESS & COMPATIBILITY
================================================================================

The analytical model 'Safety_Stock_ROP_Calculator_EN.xlsx' is 100% compatible
with Google Sheets and Microsoft 365 Cloud.

STEP-BY-STEP IMPORT INSTRUCTIONS:
1. Open Google Drive (https://drive.google.com).
2. Click '+ New' -> 'File upload'.
3. Select 'Safety_Stock_ROP_Calculator_EN.xlsx'.
4. Double-click the uploaded file in Google Drive to open it in Google Sheets.
5. Click 'File' -> 'Save as Google Sheets'.

All stochastic formulas (NORM.S.INV, SQRT, SUM, AVERAGE, COUNTIF, etc.), inter-sheet
links, and conditional formatting run natively and instantly in Google Workspace.
================================================================================
"""


def create_instruction_files():
    """Genera los archivos de instrucciones de texto en sus carpetas respectivas."""
    # Archivos dentro de [ES]
    path_leeme_es = os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt")
    with open(path_leeme_es, "w", encoding="utf-8") as f:
        f.write(LEEME_INSTRUCCIONES_ES)
    print(f" -> Creado: {path_leeme_es}")

    # Archivos dentro de [EN]
    path_readme_en = os.path.join(DIR_EN, "README_INSTRUCTIONS.txt")
    with open(path_readme_en, "w", encoding="utf-8") as f:
        f.write(README_INSTRUCTIONS_EN)
    print(f" -> Created: {path_readme_en}")

    # Archivos de raíz
    path_sheets_es = os.path.join(DIR_PACK, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
    with open(path_sheets_es, "w", encoding="utf-8") as f:
        f.write(LEEME_GOOGLE_SHEETS_ES)
    print(f" -> Creado: {path_sheets_es}")

    path_sheets_en = os.path.join(DIR_PACK, "README_GOOGLE_SHEETS_ACCESS.txt")
    with open(path_sheets_en, "w", encoding="utf-8") as f:
        f.write(README_GOOGLE_SHEETS_EN)
    print(f" -> Created: {path_sheets_en}")


def build_master_zip():
    """Construye el archivo ZIP maestro con la estructura oficial requerida."""
    os.makedirs(DIR_LEMON, exist_ok=True)

    print(f"\nGenerando archivo ZIP maestro: {ZIP_PATH_LOCAL}...")
    with zipfile.ZipFile(ZIP_PATH_LOCAL, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 1. Archivos en raíz del ZIP
        sheets_es = os.path.join(DIR_PACK, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
        sheets_en = os.path.join(DIR_PACK, "README_GOOGLE_SHEETS_ACCESS.txt")
        zipf.write(sheets_es, arcname="LEEME_ACCESO_GOOGLE_SHEETS.txt")
        zipf.write(sheets_en, arcname="README_GOOGLE_SHEETS_ACCESS.txt")

        # 2. Carpeta [ES]_Stock_Seguridad_ROP
        es_files = [
            "Calculadora_Stock_Seguridad_ROP_ES.xlsx",
            "Presentacion_Stock_ROP_CLevel_ES.pptx",
            "Guia_Metodologica_Stock_ROP_ES.pdf",
            "LEEME_INSTRUCCIONES.txt"
        ]
        for f in es_files:
            p = os.path.join(DIR_ES, f)
            if os.path.exists(p):
                zipf.write(p, arcname=f"[ES]_Stock_Seguridad_ROP/{f}")
                print(f"    + [ES] {f}")
            else:
                print(f"    ! ERROR: Falta archivo {p}")

        # 3. Carpeta [EN]_Safety_Stock_ROP
        en_files = [
            "Safety_Stock_ROP_Calculator_EN.xlsx",
            "Deck_Safety_Stock_ROP_CLevel_EN.pptx",
            "Methodology_Guide_Safety_Stock_ROP_EN.pdf",
            "README_INSTRUCTIONS.txt"
        ]
        for f in en_files:
            p = os.path.join(DIR_EN, f)
            if os.path.exists(p):
                zipf.write(p, arcname=f"[EN]_Safety_Stock_ROP/{f}")
                print(f"    + [EN] {f}")
            else:
                print(f"    ! ERROR: Missing file {p}")

    print(f" -> Archivo ZIP maestro creado con éxito: {ZIP_PATH_LOCAL}")

    # Copiar a 00_DISTRIBUCION_LEMONSQUEEZY
    shutil.copy2(ZIP_PATH_LOCAL, ZIP_PATH_LEMON)
    print(f" -> Copia sincronizada en Lemon Squeezy: {ZIP_PATH_LEMON}")


def main():
    print("Iniciando empaquetado del Executive Decision Pack Stock & ROP...")
    create_instruction_files()
    build_master_zip()
    print("\nProceso de empaquetado finalizado con total éxito.")


if __name__ == "__main__":
    main()
