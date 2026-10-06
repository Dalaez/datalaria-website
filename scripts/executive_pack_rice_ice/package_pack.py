#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los activos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil/Executive_Decision_Pack_RICE_ICE_Dual.zip
- Copia directa en packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_RICE_ICE_Dual.zip

Estructura del archivo ZIP:
- [ES]_Matriz_RICE_ICE/
  - Matriz_RICE_ICE_Datalaria_ES.xlsx
  - Presentacion_RICE_ICE_CLevel_ES.pptx
  - Guia_Metodologica_RICE_ICE_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- [EN]_RICE_ICE_Matrix/
  - RICE_ICE_Matrix_Datalaria_EN.xlsx
  - Deck_RICE_ICE_CLevel_EN.pptx
  - Methodology_Guide_RICE_ICE_EN.pdf
  - README_INSTRUCTIONS.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- LEEME_ACCESO_GOOGLE_SHEETS.txt (en la raíz del ZIP)
- README_GOOGLE_SHEETS_ACCESS.txt (en la raíz del ZIP)

SEGURIDAD ESTRICTA:
Queda terminantemente prohibido almacenar o sincronizar archivos a static/downloads/
o public/downloads/. Todos los activos quedan alojados exclusivamente en packages/.
"""

import os
import sys
import subprocess
import zipfile
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DIR_PACK = "packages/Suite_02_Toma_Decisiones/02_Matriz_RICE_ICE_Agil"
DIR_ES = os.path.join(DIR_PACK, "[ES]_Matriz_RICE_ICE")
DIR_EN = os.path.join(DIR_PACK, "[EN]_RICE_ICE_Matrix")
DIR_LEMON = "packages/00_DISTRIBUCION_LEMONSQUEEZY"

ZIP_NAME = "Executive_Decision_Pack_RICE_ICE_Dual.zip"
ZIP_PATH_LOCAL = os.path.join(DIR_PACK, ZIP_NAME)
ZIP_PATH_LEMON = os.path.join(DIR_LEMON, ZIP_NAME)

PASSWORD_OFFICIAL = "Datalaria2026"
SUPPORT_EMAIL = "datalaria@gmail.com"

LEEME_INSTRUCCIONES_ES = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Matriz RICE & ICE de Priorización Ágil: Backlog Cuantitativo & Línea de Corte
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas de consultoría estratégica de estándar Tier-1 (McKinsey / BCG / Intercom)
está diseñado específicamente para Directores de Producto (CPO), Directores de Tecnología (CTO),
Directores Generales (CEO) y Comités de Dirección (Product Council / Board).

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Matriz_RICE_ICE_Datalaria_ES.xlsx
  Libro de trabajo analítico en Excel con 5 pestañas estructuradas e interconectadas:
  - Pestaña 1: Dashboard Ejecutivo (Cabecera directiva, KPI Cards, ranking dinámico Top 10 RICE
               vía LARGE + INDEX/MATCH, gráfico de dispersión Valor vs. Esfuerzo, gráfico de barras
               horizontales y tarjeta de recomendación ejecutiva C-Level).
  - Pestaña 2: Backlog RICE (Matriz de hasta 30 iniciativas con inputs de Reach, Impacto,
               Confianza y Esfuerzo, columnas calculadas de Valor Esperado, Score RICE,
               Score Normalizado 0-100, Cuadrante Estratégico, Esfuerzo Acumulado por ranking,
               Estado de Línea de Corte y Trimestre Asignado Q1-Q4).
  - Pestaña 3: Experimentos ICE (Matriz de hasta 20 experimentos de crecimiento con inputs de
               Hipótesis, Métrica North Star, Impacto 1-10, Confianza 1-10, Facilidad 1-10,
               Score ICE multiplicativo 1-1.000, ranking y semáforo de prioridad de lanzamiento).
  - Pestaña 4: Capacidad & Roadmap (Modelo de capacidad neta de ingeniería por squad y trimestre,
               buffer intocable del 16,7% para deuda técnica/mantenimiento, control de utilización
               y distribución estratégica Now / Next / Later).
  - Pestaña 5: Escalas & Calibración (Rúbricas maestras editables de Impacto y Confianza
               inspiradas en el Confidence Meter de Itamar Gilad y guía de estimación de Reach y Effort).

• Presentacion_RICE_ICE_CLevel_ES.pptx
  Presentación ejecutiva panorámica (16:9 widescreen) bajo la Pirámide de Minto (3 diapositivas):
  - Diapositiva 1: Síntesis Ejecutiva & Veredicto de Priorización (4 KPI Cards y diagnóstico de valor).
  - Diapositiva 2: Evidencia Cuantitativa (Matriz 2x2 Impacto/Esfuerzo en alta resolución, tabla Top RICE y tests ICE).
  - Diapositiva 3: Roadmap Now/Next/Later & Product Council Decision Gateway (4 acuerdos vinculantes y 4 firmas C-Level).

• Guia_Metodologica_RICE_ICE_ES.pdf
  Guía metodológica oficial de 5 páginas con fundamentación matemática formal de la densidad de valor RICE,
  el descuento de riesgo bayesiano, la aproximación greedy al Problema de la Mochila, protocolo de calibración,
  caso práctico resuelto (scale-up B2B SaaS con 3 squads) y FAQ de defensa ante el Consejo.

--------------------------------------------------------------------------------
2. CONTRASEÑA OFICIAL Y CONVENCIÓN VISUAL DE CELDAS
--------------------------------------------------------------------------------
Para garantizar la integridad del modelo durante deliberaciones ejecutivas y evitar la 
alteración accidental de fórmulas, rankings y líneas de corte, las celdas de cálculo están protegidas:

• CELDAS EDITABLES (Entrada de datos): Fondo BLANCO (#FFFFFF) con protección desbloqueada.
  Puedes introducir libremente nombres de iniciativas, OKRs, squads, estimaciones de Reach,
  selectores de Impacto y Confianza, Persona-Mes de esfuerzo y notas de justificación.

• CELDAS PROTEGIDAS (Fórmulas y cálculos automáticos): Fondo GRIS SUAVE (#F1F5F9).
  Contienen el motor analítico del modelo y no deben ser modificadas directamente.

Si necesitas desproteger las hojas para realizar ampliaciones estructurales en Microsoft Excel, 
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
RICE & ICE Agile Prioritization Matrix: Quantitative Backlog & Capacity Cut-Line
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite provides Tier-1 management consulting decision-support tools tailored 
for Chief Product Officers (CPO), Chief Technology Officers (CTO), CEOs, and Executive Boards.

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• RICE_ICE_Matrix_Datalaria_EN.xlsx
  Comprehensive 5-tab strategic workbook:
  - Tab 1: Executive Dashboard (Executive metadata header, KPI summary cards, dynamic Top 10 RICE
           ranking powered by LARGE + INDEX/MATCH, Expected Value vs. Effort scatter chart, horizontal
           bar chart, and C-Suite executive recommendation cards).
  - Tab 2: RICE Backlog (30-row quantitative portfolio matrix with Reach, Impact, Confidence,
           Effort inputs, Expected Value, RICE score, 0-100 normalized score, Strategic Quadrant,
           cumulative effort by rank, Capacity Cut-Line status, and Q1-Q4 Quarter allocation).
  - Tab 3: ICE Experiments (20-row agile growth testing matrix with Hypothesis, North Star Metric,
           Impact 1-10, Confidence 1-10, Ease 1-10 inputs, 1-1,000 ICE score, ranking, and launch status).
  - Tab 4: Capacity & Roadmap (Quarterly net squad engineering capacity model, ring-fenced 16.7%
           technical debt/KTLO buffer, utilization tracking, and strategic Now / Next / Later distribution).
  - Tab 5: Scales & Calibration (Editable master scales for Impact and Confidence aligned with
           Itamar Gilad's Confidence Meter, plus concrete estimation guidance for Reach and Effort).

• Deck_RICE_ICE_CLevel_EN.pptx
  Executive widescreen presentation (16:9 widescreen) structured under Minto Pyramid Principle (3 slides):
  - Slide 1: Executive Synthesis & Prioritization Verdict (4 KPI cards and value density diagnosis).
  - Slide 2: Quantitative Evidence (High-resolution 2x2 Impact vs. Effort matrix, Top RICE table, ICE tests).
  - Slide 3: Now/Next/Later Roadmap & Product Council Decision Gateway (4 binding resolutions and 4 C-Level sign-offs).

• Methodology_Guide_RICE_ICE_EN.pdf
  Official 5-page executive methodology guide with formal mathematical proofs of RICE value density,
  Bayesian confidence deflation, greedy knapsack cut-line approximation, scale calibration protocols,
  solved enterprise B2B SaaS case study (3 squads), and Boardroom Defense FAQ.

--------------------------------------------------------------------------------
2. MASTER PASSWORD & VISUAL CELL CONVENTION
--------------------------------------------------------------------------------
To safeguard model integrity during executive deliberations and prevent accidental formula corruption,
calculation cells are protected:

• EDITABLE INPUT CELLS: Pure WHITE background (#FFFFFF) with unlocked protection.
  You may freely edit initiative names, OKRs, squads, Reach metrics, Impact and Confidence
  dropdowns, Person-Months of effort, and evidence rationale notes.

• PROTECTED FORMULA CELLS: SOFT GRAY background (#F1F5F9).
  These contain the core calculation engine and are locked to preserve analytical integrity.

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

La plantilla Excel (.xlsx) del Executive Decision Pack RICE & ICE ha sido diseñada bajo estrictos 
estándares de compatibilidad para funcionar con total fluidez tanto en Microsoft Excel 
como en Google Sheets:

1. Abre tu navegador web y accede a Google Drive (https://drive.google.com).
2. Haz clic en el botón "+ Nuevo" en la esquina superior izquierda y selecciona "Subir archivo".
3. Selecciona el archivo:
   - "Matriz_RICE_ICE_Datalaria_ES.xlsx" (o la versión en inglés).
4. Una vez completada la subida, haz doble clic sobre el archivo en tu unidad de Drive.
5. Haz clic en "Abrir con Hojas de cálculo de Google" en la barra superior.
6. ¡Listo! Todas las fórmulas RICE, funciones LARGE e INDEX/MATCH, validaciones de datos
   por lista desplegable y vínculos entre pestañas operarán de manera completamente nativa.

Nota: Si deseas desproteger las hojas dentro de Google Sheets para personalizar filas 
o columnas, accede a Datos > Hojas y rangos protegidos e introduce la contraseña oficial 
documentada en LEEME_INSTRUCCIONES.txt (Datalaria2026).
"""

README_GOOGLE_SHEETS = """================================================================================
DATALARIA | GOOGLE SHEETS IMPORT & ACCESS GUIDE
================================================================================

The Executive Decision Pack RICE & ICE Excel workbook (.xlsx) is engineered for 100% native 
compatibility with Google Drive and Google Sheets without any proprietary macros:

1. Open your web browser and navigate to Google Drive (https://drive.google.com).
2. Click "+ New" in the top-left corner and select "File upload".
3. Select the workbook:
   - "RICE_ICE_Matrix_Datalaria_EN.xlsx" (or the Spanish edition).
4. Once uploaded, double-click the file in your Google Drive list.
5. Click "Open with Google Sheets" at the top center.
6. All RICE formulas, LARGE + INDEX/MATCH rankings, dropdown data validations, and cross-tab linkages will function natively.

Note: To unprotect sheets within Google Sheets for structural customizations, navigate to 
Data > Protected sheets and ranges and enter the master password documented in 
README_INSTRUCTIONS.txt (Datalaria2026).
"""


def write_text_files():
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


def run_protection_audit():
    """Ejecuta el script verify_excel_protection.py y aborta si hay violaciones."""
    print("\n--- Ejecutando auditoría obligatoria de protección OpenXML ---")
    script_path = os.path.join("scripts", "executive_pack_rice_ice", "verify_excel_protection.py")
    res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print(f"[ERROR CRÍTICO] La auditoría de protección ha fallado con código {res.returncode}.")
        if res.stderr:
            print(res.stderr)
        sys.exit(1)
    print("[OK] Auditoría de protección superada con 0 violaciones. Procediendo al empaquetado.\n")


def build_zip_package():
    os.makedirs(DIR_LEMON, exist_ok=True)
    os.makedirs(DIR_PACK, exist_ok=True)

    print(f"Construyendo paquete ZIP maestro: {ZIP_PATH_LOCAL}...")

    files_to_pack = [
        # Carpeta ES
        (os.path.join(DIR_ES, "Matriz_RICE_ICE_Datalaria_ES.xlsx"), "[ES]_Matriz_RICE_ICE/Matriz_RICE_ICE_Datalaria_ES.xlsx"),
        (os.path.join(DIR_ES, "Presentacion_RICE_ICE_CLevel_ES.pptx"), "[ES]_Matriz_RICE_ICE/Presentacion_RICE_ICE_CLevel_ES.pptx"),
        (os.path.join(DIR_ES, "Guia_Metodologica_RICE_ICE_ES.pdf"), "[ES]_Matriz_RICE_ICE/Guia_Metodologica_RICE_ICE_ES.pdf"),
        (os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt"), "[ES]_Matriz_RICE_ICE/LEEME_INSTRUCCIONES.txt"),
        # Carpeta EN
        (os.path.join(DIR_EN, "RICE_ICE_Matrix_Datalaria_EN.xlsx"), "[EN]_RICE_ICE_Matrix/RICE_ICE_Matrix_Datalaria_EN.xlsx"),
        (os.path.join(DIR_EN, "Deck_RICE_ICE_CLevel_EN.pptx"), "[EN]_RICE_ICE_Matrix/Deck_RICE_ICE_CLevel_EN.pptx"),
        (os.path.join(DIR_EN, "Methodology_Guide_RICE_ICE_EN.pdf"), "[EN]_RICE_ICE_Matrix/Methodology_Guide_RICE_ICE_EN.pdf"),
        (os.path.join(DIR_EN, "README_INSTRUCTIONS.txt"), "[EN]_RICE_ICE_Matrix/README_INSTRUCTIONS.txt"),
        # Raíz del ZIP
        (os.path.join(DIR_PACK, "LEEME_ACCESO_GOOGLE_SHEETS.txt"), "LEEME_ACCESO_GOOGLE_SHEETS.txt"),
        (os.path.join(DIR_PACK, "README_GOOGLE_SHEETS_ACCESS.txt"), "README_GOOGLE_SHEETS_ACCESS.txt"),
    ]

    for src, arc in files_to_pack:
        if not os.path.exists(src):
            raise FileNotFoundError(f"Archivo requerido no encontrado: {src}")

    with zipfile.ZipFile(ZIP_PATH_LOCAL, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for src, arc in files_to_pack:
            zf.write(src, arcname=arc)
            print(f"  + Añadido a ZIP: {arc}")

    size_kb = os.path.getsize(ZIP_PATH_LOCAL) / 1024
    print(f"[OK] Archivo ZIP local creado con éxito: {ZIP_PATH_LOCAL} ({size_kb:.1f} KB)")

    shutil.copy2(ZIP_PATH_LOCAL, ZIP_PATH_LEMON)
    print(f"[OK] Copia sincronizada en el hub Lemon Squeezy: {ZIP_PATH_LEMON}")

    # SEGURIDAD ANTI-FILTRACIÓN:
    for unsafe_dir in ["static/downloads", "public/downloads"]:
        if os.path.exists(unsafe_dir):
            for fname in os.listdir(unsafe_dir):
                if "RICE" in fname.upper() or fname.endswith(".zip"):
                    bad_file = os.path.join(unsafe_dir, fname)
                    os.remove(bad_file)
                    print(f"[ALERTA DE SEGURIDAD] Archivo eliminado de ruta pública: {bad_file}")


def update_catalog():
    """Actualiza el catálogo de productos de Lemon Squeezy con la ficha oficial de RICE & ICE."""
    cat_path = os.path.join(DIR_LEMON, "CATALOGO_PRODUCTOS_LEMONSQUEEZY.txt")
    if not os.path.exists(cat_path):
        return

    entry_text = """
--------------------------------------------------------------------------------
PRODUCTO 7: Matriz RICE & ICE de Priorización Ágil Dual (ES/EN)
--------------------------------------------------------------------------------
- Nombre: Matriz RICE & ICE de Priorización Ágil Dual (ES/EN)
- Suite: Suite 02 – Toma de Decisiones & Priorización
- Archivo descargable: Executive_Decision_Pack_RICE_ICE_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-rice-ice
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-rice-ice
- Entregables incluidos:
  • Excel (.xlsx) de 5 pestañas con RICE, ICE, capacidad de squads y línea de corte
  • Presentación PowerPoint 16:9 C-Level con matriz 2x2 y Product Council Gateway
  • Guía Metodológica PDF (5 págs) con demostración matemática de mochila y Confidence Meter
  • Versiones completas en Español e Inglés + Acceso a Google Sheets
"""

    with open(cat_path, "r", encoding="utf-8") as f:
        current_content = f.read()

    if "matriz-rice-ice" not in current_content:
        # Insertar antes del MEGA BUNDLE
        if "MEGA BUNDLE:" in current_content:
            parts = current_content.split("================================================================================")
            # Insertar antes del último bloque grande
            new_content = current_content.replace(
                "================================================================================\nMEGA BUNDLE:",
                entry_text + "\n================================================================================\nMEGA BUNDLE:"
            )
        else:
            new_content = current_content + entry_text

        with open(cat_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK] Catálogo actualizado con la ficha oficial de RICE & ICE: {cat_path}")
    else:
        print("[OK] La ficha de RICE & ICE ya figura en el catálogo.")


def main():
    print("================================================================================")
    print("DATALARIA | MAESTRO DE EMPAQUETADO OFICIAL RICE & ICE")
    print("================================================================================")
    run_protection_audit()
    write_text_files()
    build_zip_package()
    update_catalog()
    print("\nProceso de empaquetado completado exitosamente.")


if __name__ == "__main__":
    main()
