#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_pack.py
===============
Empaqueta los activos del Executive Decision Pack oficial de Datalaria en el
archivo ZIP maestro listo para distribución comercial en Lemon Squeezy:
- packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/Executive_Decision_Pack_Business_Case_Dual.zip
- Copia directa en packages/00_DISTRIBUCION_LEMONSQUEEZY/Executive_Decision_Pack_Business_Case_Dual.zip

Estructura del archivo ZIP:
- [ES]_Business_Case_VAN_TIR/
  - Business_Case_VAN_TIR_Datalaria_ES.xlsx
  - Presentacion_Business_Case_CLevel_ES.pptx
  - Guia_Metodologica_Business_Case_ES.pdf
  - LEEME_INSTRUCCIONES.txt (con contraseña oficial "Datalaria2026" y soporte datalaria@gmail.com)
- [EN]_Financial_Business_Case/
  - Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx
  - Deck_Business_Case_CLevel_EN.pptx
  - Methodology_Guide_Business_Case_EN.pdf
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

DIR_PACK = "packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR"
DIR_ES = os.path.join(DIR_PACK, "[ES]_Business_Case_VAN_TIR")
DIR_EN = os.path.join(DIR_PACK, "[EN]_Financial_Business_Case")
DIR_LEMON = "packages/00_DISTRIBUCION_LEMONSQUEEZY"

ZIP_NAME = "Executive_Decision_Pack_Business_Case_Dual.zip"
ZIP_PATH_LOCAL = os.path.join(DIR_PACK, ZIP_NAME)
ZIP_PATH_LEMON = os.path.join(DIR_LEMON, ZIP_NAME)

PASSWORD_OFFICIAL = "Datalaria2026"
SUPPORT_EMAIL = "datalaria@gmail.com"

LEEME_INSTRUCCIONES_ES = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Business Case Financiero: VAN, TIR, Payback & Análisis de Sensibilidad Tornado
================================================================================

Muchas gracias por adquirir el Executive Decision Pack oficial de Datalaria.com.
Este conjunto de herramientas de consultoría estratégica y finanzas corporativas 
de estándar Tier-1 (McKinsey Corporate Finance Practice / BCG Corporate Development)
está diseñado específicamente para Directores Financieros (CFO), Directores Generales (CEO),
responsables de M&A y Desarrollo Corporativo, y Comités de Inversión (Board of Directors).

--------------------------------------------------------------------------------
1. ENTREGABLES INCLUIDOS EN ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
• Business_Case_VAN_TIR_Datalaria_ES.xlsx
  Libro de trabajo analítico en Excel con 6 pestañas estructuradas e interconectadas:
  - Pestaña 1: Dashboard Ejecutivo (Cabecera directiva, KPI Cards con VAN 5a, VAN 3a,
               TIR, MIRR, WACC, Paybacks, PI, Peak Funding y VAN esperado ponderado,
               semáforo de dictamen automático APROBAR/REVISAR/RECHAZAR según política
               de inversión, Curva J de flujo acumulado nominal y descontado con cruce
               del payback, Gráfico Tornado y comparativa de escenarios).
  - Pestaña 2: Supuestos & Drivers (Calculadora de WACC vía CAPM con coste de equity Ke,
               coste de deuda neta de impuestos, ponderación D/E, tabla de 3 escenarios
               Pesimista/Base/Optimista, selector activo vía INDEX/MATCH, probabilidades
               con control al 100%, switch de valor residual y rangos de sensibilidad).
  - Pestaña 3: Proyección DCF (Modelo de Flujo de Caja Libre Descontado a 5 años: P&L
               completo, NOPAT, variación de capital circulante NWC, CAPEX en dos tramos,
               factores de descuento, flujos descontados, valor residual Gordon-Shapiro,
               VAN, TIR, MIRR, Payback simple y descontado por interpolación lineal,
               Índice de Rentabilidad y fila de control de cuadre del modelo).
  - Pestaña 4: Sensibilidad & Tornado (Motor de recálculo univariable sin tablas de
               datos de Excel compatible con Google Sheets, cálculo de swings por driver,
               ranking dinámico y cálculo de puntos de equilibrio break-even).
  - Pestaña 5: Plan de Inversión & Governance (Estructura de inversión en dos tramos,
               stage gates vinculados a OEE y aceptación SAT, criterios de cancelación
               kill criteria stop-loss y matriz de riesgos de mitigación).
  - Pestaña 6: Guía & Control (Instrucciones metodológicas, convención visual de celdas,
               atajos de teclado de finanzas y control de versiones del modelo).

• Presentacion_Business_Case_CLevel_ES.pptx
  Presentación ejecutiva panorámica (16:9 widescreen) bajo la Pirámide de Minto (3 diapositivas):
  - Diapositiva 1: Síntesis Ejecutiva & Veredicto de Asignación de Capital (4 KPI Cards y diagnóstico de valor).
  - Diapositiva 2: Evidencia Cuantitativa & Análisis de Riesgo (Gráfico Tornado nativo de PowerPoint, tabla de 3 escenarios y puntos de equilibrio break-even).
  - Diapositiva 3: Plan de Inversión por Tramos & Board Decision Gateway (Estructura de tramos condicionados, stage gates, kill criteria y resolución formal con 4 firmas C-Level).

• Guia_Metodologica_Business_Case_ES.pdf
  Guía metodológica oficial de 5 páginas con fundamentación matemática formal del FCFF,
  WACC mediante CAPM, VAN, TIR, MIRR, Payback descontado con interpolación lineal, Índice
  de Rentabilidad, explicación de la trampa de la función NPV de Excel en el Año 0, caso
  práctico resuelto de automatización industrial y protocolo de defensa ante el Consejo (FAQ).

--------------------------------------------------------------------------------
2. CONTRASEÑA OFICIAL Y CONVENCIÓN VISUAL DE CELDAS
--------------------------------------------------------------------------------
Para garantizar la integridad del modelo durante deliberaciones ejecutivas y evitar la 
alteración accidental de fórmulas y vinculaciones del DCF, las celdas de cálculo están protegidas:

• CELDAS EDITABLES (Entrada de datos): Fondo BLANCO (#FFFFFF) con protección desbloqueada.
  Puedes modificar libremente supuestos de volumen, precio, costes, CAPEX, parámetros
  del WACC, probabilidades de escenario y rangos de sensibilidad.

• CELDAS PROTEGIDAS (Fórmulas y cálculos automáticos): Fondo GRIS SUAVE (#F1F5F9).
  Contienen el motor analítico del modelo y no deben ser modificadas directamente.

Si necesitas desproteger las hojas para realizar ampliaciones estructurales en Microsoft Excel, 
la contraseña oficial del modelo es:
  {PASSWORD_OFFICIAL}

--------------------------------------------------------------------------------
3. COMPATIBILIDAD CON GOOGLE SHEETS
--------------------------------------------------------------------------------
El archivo Excel utiliza exclusivamente funciones nativas compatibles al 100% con Google Drive 
y Google Sheets sin macros ni Data Tables propietarias (ver archivo adjunto 
LEEME_ACCESO_GOOGLE_SHEETS.txt en la raíz del paquete).

--------------------------------------------------------------------------------
4. CONTACTO Y ASESORÍA FINANCIERA ESTRATÉGICA
--------------------------------------------------------------------------------
Para modelización financiera a medida, valoraciones corporativas o preparación de Comités:
• Web: https://datalaria.com
• Email Corporativo de Soporte: {SUPPORT_EMAIL}
• LinkedIn: https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/

© 2026 Datalaria. Todos los derechos reservados.
"""

README_INSTRUCTIONS_EN = f"""================================================================================
DATALARIA | EXECUTIVE DECISION PACK
Financial Business Case: NPV, IRR, Payback & Tornado Sensitivity Analysis
================================================================================

Thank you for purchasing the official Executive Decision Pack from Datalaria.com.
This suite provides Tier-1 corporate finance and strategy decision-support tools
aligned with McKinsey Corporate Finance Practice and BCG Corporate Development standards,
tailored for Chief Financial Officers (CFO), Chief Executive Officers (CEO), Corporate
Development / M&A executives, and Investment Committees (Board of Directors).

--------------------------------------------------------------------------------
1. DELIVERABLES INCLUDED IN THIS PACKAGE (.ZIP)
--------------------------------------------------------------------------------
• Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx
  Comprehensive 6-tab strategic financial workbook:
  - Tab 1: Executive Dashboard (Executive metadata header, KPI summary cards featuring
           5-Yr NPV, 3-Yr NPV, IRR, MIRR, WACC, simple & discounted Paybacks, PI,
           Peak Funding, and expected probability-weighted NPV, automated APPROVE/REVIEW/REJECT
           verdict card, cumulative nominal and discounted J-Curve cash flow chart,
           Tornado chart, and scenario comparison).
  - Tab 2: Assumptions & Drivers (CAPM-based WACC calculator with Cost of Equity Ke,
           after-tax cost of debt, capital structure weights, 3-state scenario table
           Pessimistic/Base/Optimistic, active scenario selector via INDEX/MATCH,
           probability weighting check, terminal value switch, and sensitivity ranges).
  - Tab 3: DCF Projection (5-year Discounted Free Cash Flow model: comprehensive P&L,
           NOPAT, working capital change NWC, two-tranche CAPEX schedule, discount factors,
           discounted cash flows, Gordon-Shapiro terminal value, NPV, IRR, MIRR,
           linearly interpolated simple and discounted Paybacks, PI, and balance check).
  - Tab 4: Sensitivity & Tornado (One-way recalculation engine free of Excel Data Tables,
           fully compatible with Google Sheets, dynamic driver swing ranking, and linear
           break-even threshold solver).
  - Tab 5: Investment Plan & Governance (Two-tranche investment calendar, stage gates
           tied to OEE and SAT acceptance, binding kill criteria stop-loss rules, and
           risk mitigation matrix).
  - Tab 6: Guide & Control (Methodological instructions, visual color convention,
           financial keyboard shortcuts, and model version audit trail).

• Deck_Business_Case_CLevel_EN.pptx
  Executive widescreen presentation (16:9 widescreen) structured under the Minto Pyramid (3 slides):
  - Slide 1: Executive Synthesis & Capital Allocation Verdict (4 KPI cards and value creation diagnostic).
  - Slide 2: Quantitative Evidence & Risk Analysis (Native editable PowerPoint Tornado chart, 3-scenario table, and break-even thresholds).
  - Slide 3: Tranched Investment Plan & Board Decision Gateway (Phased tranches, stage gates, kill criteria, and formal C-Level resolution with 4 sign-offs).

• Methodology_Guide_Business_Case_EN.pdf
  Official 5-page executive methodology guide with formal mathematical proofs of FCFF,
  WACC via CAPM, NPV, IRR, MIRR, interpolated Discounted Payback, Profitability Index,
  the Year 0 Excel NPV function trap analysis, solved industrial manufacturing case study,
  and Boardroom Defense Protocol (C-Level FAQ).

--------------------------------------------------------------------------------
2. MASTER PASSWORD & VISUAL CELL CONVENTION
--------------------------------------------------------------------------------
To safeguard model integrity during executive deliberations and prevent accidental formula corruption,
calculation cells are protected:

• EDITABLE INPUT CELLS: Pure WHITE background (#FFFFFF) with unlocked protection.
  You may freely edit volume, price, costs, CAPEX, WACC parameters, scenario probabilities,
  and Tornado sensitivity boundaries.

• PROTECTED FORMULA CELLS: SOFT GRAY background (#F1F5F9).
  These contain the core DCF calculation engine and are locked to preserve analytical integrity.

If you need to unprotect the worksheets for structural expansions in Microsoft Excel, 
the official model password is:
  {PASSWORD_OFFICIAL}

--------------------------------------------------------------------------------
3. GOOGLE SHEETS COMPATIBILITY
--------------------------------------------------------------------------------
The Excel workbook uses standard native formulas fully compatible with Google Drive 
and Google Sheets without proprietary macros or Data Tables (see README_GOOGLE_SHEETS_ACCESS.txt
at the root of this archive).

--------------------------------------------------------------------------------
4. CORPORATE CONTACT & EXECUTIVE FINANCIAL ADVISORY
--------------------------------------------------------------------------------
For custom corporate financial modeling, M&A valuations, or Board preparation workshops:
• Web: https://datalaria.com
• Corporate Support Email: {SUPPORT_EMAIL}
• LinkedIn: https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/

© 2026 Datalaria. All rights reserved.
"""

LEEME_GOOGLE_SHEETS = """================================================================================
DATALARIA | GUÍA DE IMPORTACIÓN Y USO EN GOOGLE SHEETS
================================================================================

La plantilla Excel (.xlsx) del Executive Decision Pack Business Case ha sido diseñada bajo estrictos 
estándares de compatibilidad para funcionar con total fluidez tanto en Microsoft Excel 
como en Google Sheets sin necesidad de macros ni complementos adicionales:

1. Abre tu navegador web y accede a Google Drive (https://drive.google.com).
2. Haz clic en el botón "+ Nuevo" en la esquina superior izquierda y selecciona "Subir archivo".
3. Selecciona el archivo:
   - "Business_Case_VAN_TIR_Datalaria_ES.xlsx" (o la versión en inglés).
4. Una vez completada la subida, haz doble clic sobre el archivo en tu unidad de Drive.
5. Haz clic en "Abrir con Hojas de cálculo de Google" en la barra superior.
6. ¡Listo! Todas las fórmulas de DCF, funciones NPV, IRR, MIRR, listas desplegables
   de validación de datos, motor de recálculo Tornado y vínculos entre pestañas
   operarán de manera completamente nativa.

Nota: Si deseas desproteger las hojas dentro de Google Sheets para personalizar filas 
o columnas, accede a Datos > Hojas y rangos protegidos e introduce la contraseña oficial 
documentada en LEEME_INSTRUCCIONES.txt (Datalaria2026).
"""

README_GOOGLE_SHEETS = """================================================================================
DATALARIA | GOOGLE SHEETS IMPORT & ACCESS GUIDE
================================================================================

The Executive Decision Pack Financial Business Case Excel workbook (.xlsx) is engineered 
for 100% native compatibility with Google Drive and Google Sheets without any proprietary 
macros or What-If Data Tables:

1. Open your web browser and navigate to Google Drive (https://drive.google.com).
2. Click "+ New" in the top-left corner and select "File upload".
3. Select the workbook:
   - "Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx" (or the Spanish edition).
4. Once uploaded, double-click the file in your Google Drive list.
5. Click "Open with Google Sheets" at the top center.
6. All DCF formulas, NPV, IRR, MIRR functions, dropdown data validations, Tornado
   recalculation rows, and cross-tab linkages will function natively.

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
    script_path = os.path.join("scripts", "executive_pack_business_case", "verify_excel_protection.py")
    res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res.stdout)
    if res.returncode != 0:
        print(f"[ERROR CRÍTICO] La auditoría de protección ha fallado con código {res.returncode}.")
        if res.stderr:
            print(res.stderr)
        sys.exit(1)
    print("[OK] Auditoría de protección superada con 0 violaciones.\n")


def build_zip_package():
    os.makedirs(DIR_LEMON, exist_ok=True)
    os.makedirs(DIR_PACK, exist_ok=True)

    print(f"Construyendo paquete ZIP maestro: {ZIP_PATH_LOCAL}...")

    files_to_pack = [
        # Carpeta ES
        (os.path.join(DIR_ES, "Business_Case_VAN_TIR_Datalaria_ES.xlsx"), "[ES]_Business_Case_VAN_TIR/Business_Case_VAN_TIR_Datalaria_ES.xlsx"),
        (os.path.join(DIR_ES, "Presentacion_Business_Case_CLevel_ES.pptx"), "[ES]_Business_Case_VAN_TIR/Presentacion_Business_Case_CLevel_ES.pptx"),
        (os.path.join(DIR_ES, "Guia_Metodologica_Business_Case_ES.pdf"), "[ES]_Business_Case_VAN_TIR/Guia_Metodologica_Business_Case_ES.pdf"),
        (os.path.join(DIR_ES, "LEEME_INSTRUCCIONES.txt"), "[ES]_Business_Case_VAN_TIR/LEEME_INSTRUCCIONES.txt"),
        # Carpeta EN
        (os.path.join(DIR_EN, "Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx"), "[EN]_Financial_Business_Case/Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx"),
        (os.path.join(DIR_EN, "Deck_Business_Case_CLevel_EN.pptx"), "[EN]_Financial_Business_Case/Deck_Business_Case_CLevel_EN.pptx"),
        (os.path.join(DIR_EN, "Methodology_Guide_Business_Case_EN.pdf"), "[EN]_Financial_Business_Case/Methodology_Guide_Business_Case_EN.pdf"),
        (os.path.join(DIR_EN, "README_INSTRUCTIONS.txt"), "[EN]_Financial_Business_Case/README_INSTRUCTIONS.txt"),
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
                if "BUSINESS" in fname.upper() or "VAN" in fname.upper() or fname.endswith(".zip"):
                    bad_file = os.path.join(unsafe_dir, fname)
                    os.remove(bad_file)
                    print(f"[ALERTA DE SEGURIDAD] Archivo eliminado de ruta pública: {bad_file}")


def update_catalog():
    """Actualiza el catálogo de productos de Lemon Squeezy con la ficha oficial de Business Case."""
    cat_path = os.path.join(DIR_LEMON, "CATALOGO_PRODUCTOS_LEMONSQUEEZY.txt")
    if not os.path.exists(cat_path):
        return

    entry_text = """
--------------------------------------------------------------------------------
PRODUCTO 8: Business Case Financiero: VAN, TIR, Payback & Tornado Dual (ES/EN)
--------------------------------------------------------------------------------
- Nombre: Business Case Financiero: VAN, TIR, Payback & Tornado Dual (ES/EN)
- Suite: Suite 02 – Toma de Decisiones & Priorización
- Archivo descargable: Executive_Decision_Pack_Business_Case_Dual.zip
- Precio de venta: 8.00 € (Precio ancla: 25.00 €)
- Slug recomendado: business-case-financiero
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/business-case-financiero
- Entregables incluidos:
  • Excel (.xlsx) de 6 pestañas con DCF, WACC (CAPM), 3 escenarios, Tornado dinámico y J-Curve
  • Presentación PowerPoint 16:9 C-Level con Gráfico Tornado nativo y Board Decision Gateway
  • Guía Metodológica PDF (5 págs) con demostración matemática, WACC y Boardroom Defense FAQ
  • Versiones completas en Español e Inglés + Acceso a Google Sheets
"""

    with open(cat_path, "r", encoding="utf-8") as f:
        current_content = f.read()

    if "business-case-financiero" not in current_content:
        # Insertar antes del MEGA BUNDLE
        if "MEGA BUNDLE:" in current_content:
            new_content = current_content.replace(
                "================================================================================\nMEGA BUNDLE:",
                entry_text + "\n================================================================================\nMEGA BUNDLE:"
            )
        else:
            new_content = current_content + entry_text

        with open(cat_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK] Catálogo actualizado con la ficha oficial de Business Case: {cat_path}")
    else:
        print("[OK] La ficha de Business Case ya figura en el catálogo.")


def main():
    print("================================================================================")
    print("DATALARIA | MAESTRO DE EMPAQUETADO OFICIAL BUSINESS CASE VAN & TIR")
    print("================================================================================")
    run_protection_audit()
    write_text_files()
    build_zip_package()
    update_catalog()
    print("\nProceso de empaquetado completado exitosamente.")


if __name__ == "__main__":
    main()
