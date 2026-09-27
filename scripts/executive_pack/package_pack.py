#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los archivos del Executive Decision Pack en el archivo ZIP oficial
listo para distribución comercial en Lemon Squeezy:
- Executive_Decision_Pack_DAFO_SWOT_Dual.zip
"""

import os
import zipfile
import shutil

DIR_STATIC = "static/downloads"
DIR_ES = os.path.join(DIR_STATIC, "01_Espanol_DAFO_CAME")
DIR_EN = os.path.join(DIR_STATIC, "02_English_SWOT_TOWS")

LEEME_ES_CONTENT = """================================================================================
DATALARIA | EXECUTIVE DECISION PACK
DAFO Cuantitativo & Matriz CAME (Edición Oficial 2026)
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este paquete contiene herramientas de consultoría estratégica de grado Tier-1 
diseñadas para Comités de Dirección (C-Level) y Consejos de Administración.

--------------------------------------------------------------------------------
1. CONTENIDO DEL PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• DAFO_Cuantitativo_CAME_Datalaria_ES.xlsx
  Libro de trabajo en Excel con 4 pestañas interconectadas:
  - Pestaña 1: Dashboard Ejecutivo (KPIs, Vector cartesiano, Scatter Plot)
  - Pestaña 2: Evaluación FODA (10 factores dinámicos, tolerante a filas vacías)
  - Pestaña 3: Matriz de Cruce CAME (Cruce 0-3 y cálculo de fuerzas)
  - Pestaña 4: Plan CAME (Iniciativas con Owner C-Level, plazos, CAPEX/OPEX y P&L)

• Presentacion_CLevel_DAFO_CAME_ES.pptx
  Presentación en PowerPoint panorámica (16:9) estructurada bajo el principio de 
  la Pirámide de Minto (Action Titles, mapas de calor y caja de Decisión Requerida).

• Guia_Metodologica_DAFO_CAME_ES.pdf
  Guía editorial de 5 páginas con fundamentación matemática, demostración vectorial, 
  caso práctico industrial resuelto y protocolo de defensa ante preguntas difíciles.

--------------------------------------------------------------------------------
2. INSTRUCCIONES DE USO EN GOOGLE SHEETS
--------------------------------------------------------------------------------
La plantilla Excel ha sido optimizada para garantizar compatibilidad nativa al 100% 
con Google Sheets sin macros complejas:
1. Abre tu navegador web e ingresa a Google Drive (drive.google.com).
2. Haz clic en "Nuevo" > "Subir archivo" y selecciona DAFO_Cuantitativo_CAME_Datalaria_ES.xlsx.
3. Haz doble clic sobre el archivo subido y selecciona "Abrir con Hojas de cálculo de Google".
4. Todas las fórmulas matriciales, gráficos y vínculos entre hojas operarán automáticamente.

--------------------------------------------------------------------------------
3. PROTECCIÓN DE FÓRMULAS Y CONTRASEÑA
--------------------------------------------------------------------------------
Para evitar rotura accidental de fórmulas durante sesiones ejecutivas, las celdas de 
cálculo están protegidas. Todas las celdas de entrada de datos (inputs en blanco o azul 
suave) están desbloqueadas para su edición libre.

Si deseas desproteger las hojas para realizar modificaciones estructurales avanzadas, 
la contraseña oficial es:
  Datalaria2026

--------------------------------------------------------------------------------
4. SOPORTE Y CONTACTO CORPORATIVO
--------------------------------------------------------------------------------
¿Necesitas adaptaciones personalizadas, modelos multi-divisa o workshops ejecutivos 
de facilitación estratégica para tu Comité de Dirección?
• Web: https://datalaria.com
• Soporte y Consultoría: datalaria@gmail.com
• LinkedIn: https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/

© 2026 Datalaria. Todos los derechos reservados.
"""

README_EN_CONTENT = """================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Quantitative SWOT & TOWS Matrix (Official 2026 Edition)
================================================================================

Thank you for purchasing Datalaria's official Executive Decision Pack.
This suite provides Tier-1 management consulting decision-support tools tailored 
for C-Suite committees, Boards of Directors, and strategic advisory engagements.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Quantitative_SWOT_TOWS_Datalaria_EN.xlsx
  Comprehensive 4-tab strategic workbook:
  - Tab 1: Executive Dashboard (Key Metrics, Cartesian Vector, Scatter Chart)
  - Tab 2: SWOT Weighted Assessment (Dynamic 10 factors, blank-row tolerance)
  - Tab 3: TOWS Cross-Impact Matrix (0-3 cross-scoring & strategic force sums)
  - Tab 4: Action Plan (Initiatives with C-Level Owners, CAPEX/OPEX, and P&L KPIs)

• Executive_CLevel_Deck_SWOT_TOWS_EN.pptx
  16:9 widescreen boardroom presentation engineered under the Minto Pyramid 
  Principle (Action Titles, force heatmaps, and Board Decision Gateway).

• Methodology_Guide_SWOT_TOWS_EN.pdf
  5-page executive guide featuring mathematical proofs, vector mechanics, 
  full industrial case study, and tough boardroom defense Q&A protocols.

--------------------------------------------------------------------------------
2. GOOGLE SHEETS COMPATIBILITY INSTRUCTIONS
--------------------------------------------------------------------------------
The Excel model is engineered for 100% native compatibility with Google Sheets:
1. Open Google Drive (drive.google.com) in your web browser.
2. Click "New" > "File upload" and select Quantitative_SWOT_TOWS_Datalaria_EN.xlsx.
3. Double click the uploaded file and click "Open with Google Sheets".
4. All matrix formulas, calculations, and sheet interconnections will function natively.

--------------------------------------------------------------------------------
3. WORKSHEET PROTECTION & MASTER PASSWORD
--------------------------------------------------------------------------------
To protect critical matrix algorithms from accidental disruption during boardroom 
meetings, calculation cells are locked. All input cells (white and light background) 
are unlocked for free data entry.

To unprotect sheets for custom architectural modifications, use the master password:
  Datalaria2026

--------------------------------------------------------------------------------
4. CORPORATE ADVISORY & SUPPORT
--------------------------------------------------------------------------------
For enterprise licensing, bespoke financial modeling, or C-Suite strategic facilitation:
• Web: https://datalaria.com
• Advisory Services: datalaria@gmail.com
• LinkedIn: https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/

© 2026 Datalaria. All rights reserved.
"""


def build_packages():
    os.makedirs(DIR_STATIC, exist_ok=True)
    os.makedirs(DIR_ES, exist_ok=True)
    os.makedirs(DIR_EN, exist_ok=True)

    # 1. Guardar archivos LEEME / README en disco dentro de sus carpetas
    leeme_es_path = os.path.join(DIR_ES, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
    with open(leeme_es_path, "w", encoding="utf-8") as f:
        f.write(LEEME_ES_CONTENT)

    readme_en_path = os.path.join(DIR_EN, "README_GOOGLE_SHEETS_ACCESS.txt")
    with open(readme_en_path, "w", encoding="utf-8") as f:
        f.write(README_EN_CONTENT)

    files_es = [
        ("DAFO_Cuantitativo_CAME_Datalaria_ES.xlsx", os.path.join(DIR_ES, "DAFO_Cuantitativo_CAME_Datalaria_ES.xlsx")),
        ("Presentacion_CLevel_DAFO_CAME_ES.pptx", os.path.join(DIR_ES, "Presentacion_CLevel_DAFO_CAME_ES.pptx")),
        ("Guia_Metodologica_DAFO_CAME_ES.pdf", os.path.join(DIR_ES, "Guia_Metodologica_DAFO_CAME_ES.pdf")),
        ("LEEME_ACCESO_GOOGLE_SHEETS.txt", leeme_es_path),
    ]

    files_en = [
        ("Quantitative_SWOT_TOWS_Datalaria_EN.xlsx", os.path.join(DIR_EN, "Quantitative_SWOT_TOWS_Datalaria_EN.xlsx")),
        ("Executive_CLevel_Deck_SWOT_TOWS_EN.pptx", os.path.join(DIR_EN, "Executive_CLevel_Deck_SWOT_TOWS_EN.pptx")),
        ("Methodology_Guide_SWOT_TOWS_EN.pdf", os.path.join(DIR_EN, "Methodology_Guide_SWOT_TOWS_EN.pdf")),
        ("README_GOOGLE_SHEETS_ACCESS.txt", readme_en_path),
    ]

    # 2. Empaquetar ÚNICAMENTE el ZIP Dual oficial: Executive_Decision_Pack_DAFO_SWOT_Dual.zip
    zip_dual_path = os.path.join(DIR_STATIC, "Executive_Decision_Pack_DAFO_SWOT_Dual.zip")
    with zipfile.ZipFile(zip_dual_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # Carpeta 01_Espanol_DAFO_CAME
        for arcname, fpath in files_es:
            z.write(fpath, arcname=f"01_Espanol_DAFO_CAME/{arcname}")
        # Carpeta 02_English_SWOT_TOWS
        for arcname, fpath in files_en:
            z.write(fpath, arcname=f"02_English_SWOT_TOWS/{arcname}")
        # En la raíz del ZIP Dual
        z.write(leeme_es_path, arcname="LEEME_ACCESO_GOOGLE_SHEETS.txt")
        z.write(readme_en_path, arcname="README_GOOGLE_SHEETS_ACCESS.txt")
    print(f"[OK DUAL] ZIP creado: {zip_dual_path} ({os.path.getsize(zip_dual_path)} bytes)")

    # 3. Limpieza de carpetas intermedias y archivos obsoletos/duplicados en static y public
    DIR_PUBLIC = "public/downloads"
    obsolete_paths = [
        os.path.join(DIR_STATIC, "dafo-came-es"),
        os.path.join(DIR_STATIC, "swot-tows-en"),
        os.path.join(DIR_STATIC, "Executive_Decision_Pack_DAFO_SWOT_Dual"),
        os.path.join(DIR_STATIC, "DAFO_CAME_Executive_Decision_Pack_ES.zip"),
        os.path.join(DIR_STATIC, "SWOT_TOWS_Executive_Decision_Pack_EN.zip"),
        os.path.join(DIR_STATIC, "LEEME_ACCESO_GOOGLE_SHEETS.txt"),
        os.path.join(DIR_STATIC, "README_GOOGLE_SHEETS_ACCESS.txt"),
        os.path.join(DIR_PUBLIC, "dafo-came-es"),
        os.path.join(DIR_PUBLIC, "swot-tows-en"),
        os.path.join(DIR_PUBLIC, "Executive_Decision_Pack_DAFO_SWOT_Dual"),
        os.path.join(DIR_PUBLIC, "DAFO_CAME_Executive_Decision_Pack_ES.zip"),
        os.path.join(DIR_PUBLIC, "SWOT_TOWS_Executive_Decision_Pack_EN.zip"),
        os.path.join(DIR_PUBLIC, "LEEME_ACCESO_GOOGLE_SHEETS.txt"),
        os.path.join(DIR_PUBLIC, "README_GOOGLE_SHEETS_ACCESS.txt"),
    ]
    for p in obsolete_paths:
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
            print(f"[CLEANUP] Directorio eliminado: {p}")
        elif os.path.isfile(p):
            os.remove(p)
            print(f"[CLEANUP] Archivo eliminado: {p}")

    # Sincronizar ZIP y carpetas a public/downloads si existe el directorio public
    if os.path.isdir("public"):
        os.makedirs(DIR_PUBLIC, exist_ok=True)
        shutil.copy2(zip_dual_path, os.path.join(DIR_PUBLIC, "Executive_Decision_Pack_DAFO_SWOT_Dual.zip"))
        print(f"[SYNC] Sincronizado a public/downloads/Executive_Decision_Pack_DAFO_SWOT_Dual.zip")
        # Sincronizar carpetas 01_Espanol y 02_English
        for folder_name in ["01_Espanol_DAFO_CAME", "02_English_SWOT_TOWS"]:
            src_f = os.path.join(DIR_STATIC, folder_name)
            dst_f = os.path.join(DIR_PUBLIC, folder_name)
            shutil.copytree(src_f, dst_f, dirs_exist_ok=True)
            print(f"[SYNC] Sincronizado directorio a public: {dst_f}")


if __name__ == '__main__':
    build_packages()
