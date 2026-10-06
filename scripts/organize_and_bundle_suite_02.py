#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organize_and_bundle_suite_02.py
===============================
Script de arquitectura, auditoría y empaquetado del MEGA BUNDLE de la Suite 02:
1. Audita la presencia e integridad de los 3 packs de la Suite 02:
   - 01_Matriz_DAR_Cuantitativa
   - 02_Matriz_RICE_ICE_Agil
   - 03_Business_Case_VAN_TIR
2. Limpia archivos residuales temporales (README_PLANIFICACION.txt, ~$*).
3. Genera los archivos informativos de bienvenida y gobernanza de la Suite 02:
   - LEEME_SUITE_02_TOMA_DECISIONES.txt
   - README_SUITE_02_DECISION_ANALYSIS.txt
4. Construye el archivo ZIP oficial del MEGA BUNDLE de la Suite 02:
   Executive_Decision_Bundle_Suite_02_Toma_Decisiones_Dual.zip
   con arquitectura bilingüe de estándar Tier-1 (01_VERSION_ESPANOL / 02_ENGLISH_VERSION).
5. Sincroniza el ZIP en packages/00_DISTRIBUCION_LEMONSQUEEZY/ y actualiza
   el archivo CATALOGO_PRODUCTOS_LEMONSQUEEZY.txt.
"""

import os
import shutil
import zipfile

BASE_DIR = os.path.abspath("packages")
DIR_SUITE_02 = os.path.join(BASE_DIR, "Suite_02_Toma_Decisiones")
DIR_DISTRIB = os.path.join(BASE_DIR, "00_DISTRIBUCION_LEMONSQUEEZY")

LEEME_SUITE_02_ES = """================================================================================
DATALARIA | MEGA BUNDLE EJECUTIVO: SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN
Colección Oficial Completa de Herramientas Cuantitativas de Decisión (Edición 2026)
================================================================================

Muchas gracias por adquirir el Mega Bundle de la Suite 02: Toma de Decisiones & 
Priorización de Datalaria.com.

Este ecosistema directivo reúne los 3 Executive Decision Packs oficiales diseñados 
para sustituir el sesgo intuitivo y la opinión subjetiva (HiPPO) por modelos 
cuantitativos blindados y defendibles ante Comités de Dirección (C-Level), 
Comités de Producto y Comités de Inversiones:

--------------------------------------------------------------------------------
1. ESTRUCTURA Y CONTENIDO DE ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
Este archivo comprimido contiene las ediciones oficiales completas tanto en Español 
como en Inglés, organizadas en carpetas independientes para máxima comodidad directiva:

📁 01_VERSION_ESPANOL/
   ├── 📁 01_Matriz_DAR_Cuantitativa/
   │   ├── Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx (Filtros Veto, scoring 0-100 y What-If)
   │   ├── Presentacion_DAR_CLevel_ES.pptx (Deck 16:9 con tabla de trade-offs y Board Gateway)
   │   ├── Guia_Metodologica_DAR_ES.pdf (Guía editorial estándar CMMI DAR y auditoría)
   │   └── LEEME_INSTRUCCIONES.txt (Instrucciones detalladas y contraseñas)
   │
   ├── 📁 02_Matriz_RICE_ICE_Agil/
   │   ├── Matriz_RICE_ICE_Datalaria_ES.xlsx (RICE, ICE, capacidad de squads y línea de corte)
   │   ├── Presentacion_RICE_ICE_CLevel_ES.pptx (Deck 16:9 con matriz 2x2 y Product Gateway)
   │   ├── Guia_Metodologica_RICE_ICE_ES.pdf (Guía editorial, problema de la mochila y Confidence)
   │   └── LEEME_INSTRUCCIONES.txt
   │
   └── 📁 03_Business_Case_VAN_TIR/
       ├── Business_Case_VAN_TIR_Datalaria_ES.xlsx (DCF 5 años, WACC CAPM, 3 escenarios y Tornado)
       ├── Presentacion_Business_Case_CLevel_ES.pptx (Deck 16:9 con Tornado nativo y Board Gateway)
       ├── Guia_Metodologica_Business_Case_ES.pdf (Guía editorial DCF, WACC y Boardroom Defense)
       └── LEEME_INSTRUCCIONES.txt

📁 02_ENGLISH_VERSION/
   ├── 📁 01_Quantitative_DAR_Matrix/
   │   ├── Quantitative_DAR_Matrix_Datalaria_EN.xlsx
   │   ├── Deck_DAR_CLevel_EN.pptx
   │   ├── Methodology_Guide_DAR_EN.pdf
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 02_RICE_ICE_Agile_Matrix/
   │   ├── RICE_ICE_Matrix_Datalaria_EN.xlsx
   │   ├── Deck_RICE_ICE_CLevel_EN.pptx
   │   ├── Methodology_Guide_RICE_ICE_EN.pdf
   │   └── README_INSTRUCTIONS.txt
   │
   └── 📁 03_Financial_Business_Case/
       ├── Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx
       ├── Deck_Business_Case_CLevel_EN.pptx
       ├── Methodology_Guide_Business_Case_EN.pdf
       └── README_INSTRUCTIONS.txt

--------------------------------------------------------------------------------
2. PROTOCOLO DE DESBLOQUEO Y EDICIÓN EN EXCEL Y GOOGLE SHEETS
--------------------------------------------------------------------------------
• Todas las celdas de entrada y datos (inputs) vienen desbloqueadas por defecto 
  (con fondo blanco #FFFFFF) para permitir edición inmediata, doble clic y 
  escenarios personalizados sin necesidad de contraseñas.
• Las celdas de fórmulas, ponderaciones matriciales, totales calculados y 
  cabeceras se encuentran protegidas (fondo gris suave #F1F5F9 o estilo corporativo) 
  para evitar corrupciones accidentales.
• En caso de requerir personalizaciones estructurales avanzadas en Excel o Google Sheets, 
  la contraseña unificada de desprotección es: Datalaria2026

--------------------------------------------------------------------------------
3. SOPORTE CORPORATIVO & ACTUALIZACIONES
--------------------------------------------------------------------------------
Para cualquier duda metodológica, asistencia con modelos o consultas:
• Web oficial: https://datalaria.com
• Soporte directo: datalaria@gmail.com
• Recursos y actualizaciones: https://datalaria.com/recursos/
================================================================================
"""

README_SUITE_02_EN = """================================================================================
DATALARIA | EXECUTIVE MEGA BUNDLE: SUITE 02 · DECISION ANALYSIS & PRIORITIZATION
Complete Official Quantitative Decision Toolkits (2026 Edition)
================================================================================

Thank you for purchasing the official Suite 02: Decision Analysis & Prioritization 
Mega Bundle from Datalaria.com.

This executive toolkit brings together all 3 official Executive Decision Packs designed 
to replace intuitive guesswork and subjective opinions (HiPPO) with battle-tested quantitative 
engines defendable before Executive Committees (C-Level), Product Councils, and Investment Boards:

--------------------------------------------------------------------------------
1. STRUCTURE & CONTENT OF THIS BUNDLE (.ZIP)
--------------------------------------------------------------------------------
This archive contains the complete official editions in both Spanish and English, 
organized into separate folders for executive convenience:

📁 01_VERSION_ESPANOL/
   (Contains all 3 complete packs in Spanish)

📁 02_ENGLISH_VERSION/
   ├── 📁 01_Quantitative_DAR_Matrix/
   │   ├── Quantitative_DAR_Matrix_Datalaria_EN.xlsx (Veto criteria, 0-100 scoring & What-If)
   │   ├── Deck_DAR_CLevel_EN.pptx (16:9 deck with trade-offs table & Board Gateway)
   │   ├── Methodology_Guide_DAR_EN.pdf (Executive guide, CMMI DAR standard & audit trail)
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 02_RICE_ICE_Agile_Matrix/
   │   ├── RICE_ICE_Matrix_Datalaria_EN.xlsx (RICE, ICE, squad capacity & cut-line)
   │   ├── Deck_RICE_ICE_CLevel_EN.pptx (16:9 deck with 2x2 matrix & Product Gateway)
   │   ├── Methodology_Guide_RICE_ICE_EN.pdf (Executive guide, knapsack problem & Confidence)
   │   └── README_INSTRUCTIONS.txt
   │
   └── 📁 03_Financial_Business_Case/
       ├── Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx (5-year DCF, WACC CAPM, 3 scenarios & Tornado)
       ├── Deck_Business_Case_CLevel_EN.pptx (16:9 deck with native Tornado chart & Board Gateway)
       ├── Methodology_Guide_Business_Case_EN.pdf (Executive guide, DCF, WACC & Boardroom Defense)
       └── README_INSTRUCTIONS.txt

--------------------------------------------------------------------------------
2. PROTOCOL FOR EXCEL & GOOGLE SHEETS EDITING
--------------------------------------------------------------------------------
• All data input cells are unlocked by default (styled with white background #FFFFFF) 
  to allow immediate editing, double-clicking, and custom scenarios without passwords.
• Formula cells, matrix weights, consolidated totals, and headers are locked 
  (styled with soft gray #F1F5F9 or corporate styling) to prevent accidental corruption.
• If advanced sheet customization is required in Excel or Google Sheets, the unified 
  unprotection password is: Datalaria2026

--------------------------------------------------------------------------------
3. CORPORATE SUPPORT & UPDATES
--------------------------------------------------------------------------------
For methodological questions, model assistance, or corporate inquiries:
• Official Website: https://datalaria.com
• Direct Support: datalaria@gmail.com
• Resource Hub: https://datalaria.com/resources/
================================================================================
"""

LEEME_GS_SUITE_02_ES = """================================================================================
DATALARIA | GUÍA DE IMPORTACIÓN Y USO EN GOOGLE SHEETS (SUITE 02)
================================================================================

Las plantillas Excel (.xlsx) de la Suite 02 han sido diseñadas bajo estrictos 
estándares de compatibilidad para funcionar con total fluidez tanto en Microsoft Excel 
como en Google Sheets:

1. Abre tu navegador web y accede a Google Drive (https://drive.google.com).
2. Haz clic en el botón "+ Nuevo" en la esquina superior izquierda y selecciona "Subir archivo".
3. Selecciona el archivo deseado:
   - Matriz DAR: Matriz_DAR_Cuantitativa_Datalaria_ES.xlsx (o versión EN)
   - Matriz RICE & ICE: Matriz_RICE_ICE_Datalaria_ES.xlsx (o versión EN)
   - Business Case: Business_Case_VAN_TIR_Datalaria_ES.xlsx (o versión EN)
4. Una vez completada la subida, haz doble clic sobre el archivo en Drive.
5. Haz clic en "Abrir con Hojas de cálculo de Google" en la barra superior.
6. ¡Listo! Todas las fórmulas matriciales, ponderaciones SUMAPRODUCTO, VNA/TIR, 
   semáforos lógicos y gráficos operarán de manera completamente nativa.

Nota: Si deseas desproteger las hojas dentro de Google Sheets para personalizar filas 
o columnas, accede a Datos > Hojas y rangos protegidos e introduce la contraseña oficial 
documentada en LEEME_INSTRUCCIONES.txt (Datalaria2026).
"""

README_GS_SUITE_02_EN = """================================================================================
DATALARIA | GOOGLE SHEETS IMPORT & USAGE GUIDE (SUITE 02)
================================================================================

The Excel (.xlsx) templates in Suite 02 are engineered under strict compatibility 
standards to run seamlessly in both Microsoft Excel and Google Sheets:

1. Open your web browser and go to Google Drive (https://drive.google.com).
2. Click the "+ New" button in the upper left corner and select "File upload".
3. Select the desired template file:
   - DAR Matrix: Quantitative_DAR_Matrix_Datalaria_EN.xlsx (or ES version)
   - RICE & ICE Matrix: RICE_ICE_Matrix_Datalaria_EN.xlsx (or ES version)
   - Business Case: Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx (or ES version)
4. Once uploaded, double-click the file in Drive.
5. Click "Open with Google Sheets" at the top.
6. All formula calculations, SUMPRODUCT matrices, NPV/IRR functions, conditional 
   formatting, and charts will run natively.

Note: To unprotect sheets within Google Sheets for structural customizations, go to 
Data > Protected sheets and ranges and enter the official password (Datalaria2026).
"""

CATALOGO_ENTRY_SUITE_02 = """
================================================================================
MEGA BUNDLE: SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN (COLECCIÓN COMPLETA)
================================================================================
- Nombre: Mega Bundle: Suite 02 · Toma de Decisiones & Priorización Dual (ES/EN)
- Archivo descargable: Executive_Decision_Bundle_Suite_02_Toma_Decisiones_Dual.zip
- Precio de venta: 15.00 € (Precio ancla: 20.00 € | Ahorro: 25%)
- Slug recomendado: suite-02-toma-decisiones
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/suite-02-toma-decisiones
- Contenido:
  • Los 3 Executive Decision Packs íntegros (Matriz DAR + Matriz RICE/ICE + Business Case VAN/TIR)
  • 6 Motores de Cálculo en Excel (.xlsx) con celdas de entrada editables y fórmulas protegidas
  • 6 Presentaciones Ejecutivas 16:9 en PowerPoint (.pptx) con Board Decision Gateways
  • 6 Guías Metodológicas Editoriales en PDF (.pdf) con rigor matemático y defensa ante comités
  • Acceso completo a Google Sheets en ambos idiomas
================================================================================
"""

def main():
    print("Iniciando auditoría, empaquetado y centralización de la Suite 02...")

    # 1. Limpieza de archivos residuales obsoletos de inicialización
    for pid in ["01_Matriz_DAR_Cuantitativa", "02_Matriz_RICE_ICE_Agil", "03_Business_Case_VAN_TIR"]:
        pdir = os.path.join(DIR_SUITE_02, pid)
        plan_txt = os.path.join(pdir, "README_PLANIFICACION.txt")
        if os.path.exists(plan_txt):
            os.remove(plan_txt)
            print(f"  [LIMPIEZA] Eliminado {pid}/README_PLANIFICACION.txt obsoleto.")

    # 2. Generación de archivos informativos de la Suite 02
    leeme_path = os.path.join(DIR_SUITE_02, "LEEME_SUITE_02_TOMA_DECISIONES.txt")
    with open(leeme_path, "w", encoding="utf-8") as f:
        f.write(LEEME_SUITE_02_ES)

    readme_path = os.path.join(DIR_SUITE_02, "README_SUITE_02_DECISION_ANALYSIS.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(README_SUITE_02_EN)

    leeme_gs_path = os.path.join(DIR_SUITE_02, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
    with open(leeme_gs_path, "w", encoding="utf-8") as f:
        f.write(LEEME_GS_SUITE_02_ES)

    readme_gs_path = os.path.join(DIR_SUITE_02, "README_GOOGLE_SHEETS_ACCESS.txt")
    with open(readme_gs_path, "w", encoding="utf-8") as f:
        f.write(README_GS_SUITE_02_EN)

    print("  [OK] Documentación oficial de la Suite 02 generada.")

    # 3. Definición del mapeo para el Mega Bundle ZIP
    bundle_zip_name = "Executive_Decision_Bundle_Suite_02_Toma_Decisiones_Dual.zip"
    bundle_zip_s02 = os.path.join(DIR_SUITE_02, bundle_zip_name)
    bundle_zip_distrib = os.path.join(DIR_DISTRIB, bundle_zip_name)

    bundle_map = [
        # (pack_id, es_src_subdir, es_zip_dest_dir, en_src_subdir, en_zip_dest_dir)
        (
            "01_Matriz_DAR_Cuantitativa",
            "[ES]_Matriz_DAR",
            "01_VERSION_ESPANOL/01_Matriz_DAR_Cuantitativa",
            "[EN]_Quantitative_DAR",
            "02_ENGLISH_VERSION/01_Quantitative_DAR_Matrix"
        ),
        (
            "02_Matriz_RICE_ICE_Agil",
            "[ES]_Matriz_RICE_ICE",
            "01_VERSION_ESPANOL/02_Matriz_RICE_ICE_Agil",
            "[EN]_RICE_ICE_Matrix",
            "02_ENGLISH_VERSION/02_RICE_ICE_Agile_Matrix"
        ),
        (
            "03_Business_Case_VAN_TIR",
            "[ES]_Business_Case_VAN_TIR",
            "01_VERSION_ESPANOL/03_Business_Case_VAN_TIR",
            "[EN]_Financial_Business_Case",
            "02_ENGLISH_VERSION/03_Financial_Business_Case"
        ),
    ]

    print(f"\nEmpaquetando MEGA BUNDLE ZIP: {bundle_zip_name}...")
    total_files = 0
    with zipfile.ZipFile(bundle_zip_s02, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Añadir archivos de la raíz del bundle
        zipf.write(leeme_path, arcname="LEEME_SUITE_02_TOMA_DECISIONES.txt")
        zipf.write(readme_path, arcname="README_SUITE_02_DECISION_ANALYSIS.txt")
        zipf.write(leeme_gs_path, arcname="LEEME_ACCESO_GOOGLE_SHEETS.txt")
        zipf.write(readme_gs_path, arcname="README_GOOGLE_SHEETS_ACCESS.txt")
        total_files += 4

        for pid, es_src, es_dest, en_src, en_dest in bundle_map:
            pdir = os.path.join(DIR_SUITE_02, pid)
            es_dir = os.path.join(pdir, es_src)
            en_dir = os.path.join(pdir, en_src)

            # Archivos en Español
            if not os.path.exists(es_dir):
                raise FileNotFoundError(f"[ERROR] Carpeta ES no encontrada: {es_dir}")
            for f in sorted(os.listdir(es_dir)):
                fpath = os.path.join(es_dir, f)
                if os.path.isfile(fpath) and not f.startswith("~$"):
                    arc = f"{es_dest}/{f}"
                    zipf.write(fpath, arcname=arc)
                    total_files += 1
                    print(f"  + [ES] {arc}")

            # Archivos en Inglés
            if not os.path.exists(en_dir):
                raise FileNotFoundError(f"[ERROR] Carpeta EN no encontrada: {en_dir}")
            for f in sorted(os.listdir(en_dir)):
                fpath = os.path.join(en_dir, f)
                if os.path.isfile(fpath) and not f.startswith("~$"):
                    arc = f"{en_dest}/{f}"
                    zipf.write(fpath, arcname=arc)
                    total_files += 1
                    print(f"  + [EN] {arc}")

    # 4. Copiar a 00_DISTRIBUCION_LEMONSQUEEZY
    shutil.copy2(bundle_zip_s02, bundle_zip_distrib)
    bundle_size_kb = os.path.getsize(bundle_zip_s02) / 1024

    print(f"\n[ÉXITO] Mega Bundle Suite 02 generado:")
    print(f"  - Ruta local: {bundle_zip_s02}")
    print(f"  - Copia distribución: {bundle_zip_distrib}")
    print(f"  - Tamaño: {bundle_size_kb:.1f} KB ({total_files} archivos)")

    # 5. Actualizar catálogo de Lemon Squeezy
    cat_path = os.path.join(DIR_DISTRIB, "CATALOGO_PRODUCTOS_LEMONSQUEEZY.txt")
    if os.path.exists(cat_path):
        with open(cat_path, "r", encoding="utf-8") as f:
            cat_content = f.read()
        if "MEGA BUNDLE: SUITE 02" not in cat_content:
            with open(cat_path, "a", encoding="utf-8") as f:
                f.write(CATALOGO_ENTRY_SUITE_02)
            print("  [OK] Añadido Mega Bundle Suite 02 al catálogo de Lemon Squeezy.")
        else:
            print("  [OK] Mega Bundle Suite 02 ya figuraba en el catálogo de Lemon Squeezy.")

    print("\n[PROCESO COMPLETADO CON ÉXITO]")

if __name__ == "__main__":
    main()
