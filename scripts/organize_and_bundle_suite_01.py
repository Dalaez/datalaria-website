#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organize_and_bundle_suite_01.py
===============================
Script de arquitectura y organización de entregables de Datalaria:
1. Limpia los archivos sueltos redundantes de la raíz de packages/.
2. Clasifica los 5 packs de la Suite 01 en carpetas individuales dedicadas dentro de:
   packages/Suite_01_Estrategia_MBA/
3. Prepara la estructura de directorios para los siguientes 2 conjuntos de packs:
   - packages/Suite_02_Toma_Decisiones/
   - packages/Suite_03_Control_Operativo/
4. Genera el archivo ZIP del MEGA BUNDLE oficial de la Suite 01:
   Executive_Decision_Bundle_Suite_01_Estrategia_MBA_Dual.zip
   con organización bilingüe impecable (01_VERSION_ESPANOL / 02_ENGLISH_VERSION).
5. Crea el hub centralizado packages/00_DISTRIBUCION_LEMONSQUEEZY/ con todos los .zip listos
   y su catálogo de configuración para carga inmediata en Lemon Squeezy.
"""

import os
import shutil
import zipfile

BASE_DIR = os.path.abspath("packages")

DIR_SUITE_01 = os.path.join(BASE_DIR, "Suite_01_Estrategia_MBA")
DIR_SUITE_02 = os.path.join(BASE_DIR, "Suite_02_Toma_Decisiones")
DIR_SUITE_03 = os.path.join(BASE_DIR, "Suite_03_Control_Operativo")
DIR_DISTRIB = os.path.join(BASE_DIR, "00_DISTRIBUCION_LEMONSQUEEZY")

LEEME_SUITE_01_ES = """================================================================================
DATALARIA | MEGA BUNDLE EJECUTIVO: SUITE 01 · ESTRATEGIA CORPORATIVA & MBA
Colección Oficial Completa de Herramientas Cuantitativas de Decisión (Edición 2026)
================================================================================

Muchas gracias por adquirir el Mega Bundle de la Suite 01: Estrategia Corporativa & MBA
de Datalaria.com.

Este ecosistema directivo reúne los 5 Executive Decision Packs oficiales diseñados 
para transformar análisis cualitativos subjetivos en motores cuantitativos defendibles 
con rigor matemático ante Comités de Dirección (C-Level), Consejos de Administración 
y Comités de Inversión de M&A y Private Equity.

--------------------------------------------------------------------------------
1. ESTRUCTURA Y CONTENIDO DE ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
Este archivo comprimido contiene las ediciones oficiales completas tanto en Español 
como en Inglés, organizadas en carpetas independientes para máxima comodidad directiva:

📁 01_VERSION_ESPANOL/
   ├── 📁 01_DAFO_Cuantitativo_CAME/
   │   ├── DAFO_Cuantitativo_CAME_Datalaria_ES.xlsx (Motor 4 pestañas con vector cartesiano)
   │   ├── Presentacion_CLevel_DAFO_CAME_ES.pptx (Deck 16:9 Pirámide de Minto)
   │   ├── Guia_Metodologica_DAFO_CAME_ES.pdf (Guía editorial con rigor matemático)
   │   └── LEEME_INSTRUCCIONES.txt (Instrucciones detalladas y contraseñas)
   │
   ├── 📁 02_5_Fuerzas_Porter/
   │   ├── Porter_5_Fuerzas_Datalaria_ES.xlsx (Scoring 0-10 con Radar dinámico)
   │   ├── Presentacion_Porter_CLevel_ES.pptx (Deck 16:9 con Action Titles)
   │   ├── Guia_Metodologica_Porter_ES.pdf (Guía de análisis de poder de mercado)
   │   └── LEEME_INSTRUCCIONES.txt
   │
   ├── 📁 03_PESTEL_Cuantitativo/
   │   ├── PESTEL_Cuantitativo_Datalaria_ES.xlsx (Motor de Severidad & Volatilidad)
   │   ├── Presentacion_PESTEL_CLevel_ES.pptx (Deck 16:9 con mapa térmico de riesgos)
   │   ├── Guia_Metodologica_PESTEL_ES.pdf (Guía de anticipación y resiliencia macro)
   │   └── LEEME_INSTRUCCIONES.txt
   │
   ├── 📁 04_BCG_Dinamica/
   │   ├── BCG_Dinamica_Datalaria_ES.xlsx (Gráfico de burbujas y flujo de caja proyectado)
   │   ├── Presentacion_BCG_CLevel_ES.pptx (Deck 16:9 con matriz de asignación de capital)
   │   ├── Guia_Metodologica_BCG_ES.pdf (Guía estratégica de ciclo de vida de producto)
   │   └── LEEME_INSTRUCCIONES.txt
   │
   └── 📁 05_Matriz_McKinsey_GE/
       ├── ES_Matriz_McKinsey_GE_Datalaria.xlsx (Motor multifactorial 3x3 de 9 cajas)
       ├── ES_Matriz_McKinsey_GE_Presentacion.pptx (Deck 16:9 con Board Decision Gateway)
       ├── ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf (Guía de gobernanza de capital)
       └── LEEME_INSTRUCCIONES.txt

📁 02_ENGLISH_VERSION/
   ├── 📁 01_Quantitative_SWOT_TOWS/
   ├── 📁 02_Porter_5_Forces/
   ├── 📁 03_Quantitative_PESTEL/
   ├── 📁 04_Dynamic_BCG/
   └── 📁 05_McKinsey_GE_Matrix/
   (Estructura simétrica con los 5 toolkits íntegramente en inglés para juntas directivas
   internacionales o comités globales).

--------------------------------------------------------------------------------
2. PROTOCOLO DE DESBLOQUEO Y EDICIÓN EN EXCEL Y GOOGLE SHEETS
--------------------------------------------------------------------------------
• Todas las celdas de entrada y datos (inputs) vienen desbloqueadas por defecto 
  (con fondo suave marfil/gris diferenciado) para permitir edición inmediata, doble clic y 
  escenarios personalizados sin necesidad de contraseñas.
• Las celdas de fórmulas, ponderaciones matriciales, totales consolidados y 
  cabeceras ejecutivas se encuentran protegidas para evitar corrupciones accidentales.
• En caso de requerir personalizaciones estructurales avanzadas en Excel o Google Sheets, 
  la contraseña unificada de desprotección es: Datalaria2026

--------------------------------------------------------------------------------
3. SOPORTE CORPORATIVO & ACTUALIZACIONES
--------------------------------------------------------------------------------
Para cualquier duda metodológica, asistencia con modelos o facturación corporativa:
• Web oficial: https://datalaria.com
• Soporte directo: datalaria@gmail.com
• Recursos y actualizaciones: https://datalaria.com/recursos/
================================================================================
"""

README_SUITE_01_EN = """================================================================================
DATALARIA | EXECUTIVE MEGA BUNDLE: SUITE 01 · CORPORATE STRATEGY & MBA
Complete Official Quantitative Decision Toolkits (2026 Edition)
================================================================================

Thank you for purchasing the official Suite 01: Corporate Strategy & MBA Mega Bundle 
from Datalaria.com.

This executive ecosystem brings together all 5 official Executive Decision Packs designed 
to turn subjective qualitative analyses into quantitative engines defendable with mathematical 
rigor before Executive Committees (C-Level), Boards of Directors, and M&A / Private Equity 
Investment Committees.

--------------------------------------------------------------------------------
1. STRUCTURE & CONTENT OF THIS BUNDLE (.ZIP)
--------------------------------------------------------------------------------
This archive contains the complete official editions in both Spanish and English, 
organized into separate folders for executive convenience:

📁 01_VERSION_ESPANOL/
   (Contains all 5 complete packs in Spanish)

📁 02_ENGLISH_VERSION/
   ├── 📁 01_Quantitative_SWOT_TOWS/
   │   ├── Quantitative_SWOT_TOWS_Datalaria_EN.xlsx (4-tab model with Cartesian vector)
   │   ├── Executive_CLevel_Deck_SWOT_TOWS_EN.pptx (16:9 Minto Pyramid deck)
   │   ├── Methodology_Guide_SWOT_TOWS_EN.pdf (Executive guide with mathematical rigor)
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 02_Porter_5_Forces/
   │   ├── Porter_5_Forces_Datalaria_EN.xlsx (0-10 scoring engine with dynamic Radar)
   │   ├── Deck_Porter_CLevel_EN.pptx (16:9 deck with Action Titles)
   │   ├── Methodology_Guide_Porter_EN.pdf (Market power analysis guide)
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 03_Quantitative_PESTEL/
   │   ├── Quantitative_PESTEL_Datalaria_EN.xlsx (Severity & Volatility dual scoring)
   │   ├── Deck_PESTEL_CLevel_EN.pptx (16:9 deck with macro risk heatmap)
   │   ├── Methodology_Guide_PESTEL_EN.pdf (Strategic anticipation & resilience guide)
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 04_Dynamic_BCG/
   │   ├── Dynamic_BCG_Datalaria_EN.xlsx (Bubble chart matrix & cash flow projection)
   │   ├── Deck_BCG_CLevel_EN.pptx (16:9 deck with capital allocation matrix)
   │   ├── Methodology_Guide_BCG_EN.pdf (Product lifecycle strategy guide)
   │   └── README_INSTRUCTIONS.txt
   │
   └── 📁 05_McKinsey_GE_Matrix/
       ├── EN_McKinsey_GE_Matrix_Datalaria.xlsx (3x3 9-box multi-factor assessment engine)
       ├── EN_McKinsey_GE_Matrix_Presentation.pptx (16:9 deck with Board Decision Gateway)
       ├── EN_McKinsey_GE_Matrix_Methodology_Guide.pdf (Capital governance framework)
       └── README_INSTRUCTIONS.txt

--------------------------------------------------------------------------------
2. PROTOCOL FOR EXCEL & GOOGLE SHEETS EDITING
--------------------------------------------------------------------------------
• All data input cells are unlocked by default (styled with soft ivory/gray background) 
  to allow immediate editing, double-clicking, and custom scenarios without passwords.
• Formula cells, matrix weights, consolidated totals, and executive headers are locked 
  to prevent accidental corruption.
• If advanced sheet customization is required in Excel or Google Sheets, the unified 
  unprotection password is: Datalaria2026

--------------------------------------------------------------------------------
3. CORPORATE SUPPORT & UPDATES
--------------------------------------------------------------------------------
For methodological questions, model assistance, or corporate billing:
• Official Website: https://datalaria.com
• Direct Support: datalaria@gmail.com
• Resource Hub: https://datalaria.com/resources/
================================================================================
"""

CATALOGO_LEMONSQUEEZY_TXT = """================================================================================
DATALARIA | CATÁLOGO DE PRODUCTOS EJECUTIVOS PARA LEMONSQUEEZY
================================================================================

Este catálogo detalla la configuración lista para registrar y subir cada producto digital 
en la consola de administración de Lemon Squeezy (https://app.lemonsqueezy.com/products):

--------------------------------------------------------------------------------
PRODUCTO 1: DAFO Cuantitativo & Matriz CAME Dual (ES/EN)
--------------------------------------------------------------------------------
- Nombre: DAFO Cuantitativo & Matriz CAME Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_DAFO_SWOT_Dual.zip
- Precio de venta: 5.00 € (Precio ancla: 19.00 €)
- Slug recomendado: dafo-cuantitativo-came
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/dafo-cuantitativo-came
- Entregables incluidos:
  • Excel (.xlsx) con vector cartesiano y ponderaciones numéricas
  • Presentación PowerPoint 16:9 C-Level con Pirámide de Minto
  • Guía Metodológica PDF (5 págs) con demostración matemática y defensa ante Board
  • Versiones completas en Español e Inglés + Acceso a Google Sheets

--------------------------------------------------------------------------------
PRODUCTO 2: 5 Fuerzas de Porter Ponderadas & Atractivo Industrial Dual (ES/EN)
--------------------------------------------------------------------------------
- Nombre: 5 Fuerzas de Porter Ponderadas & Atractivo Industrial Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_Porter_5_Forces_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: 5-fuerzas-porter
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/5-fuerzas-porter
- Entregables incluidos:
  • Excel (.xlsx) con scoring 0-10 y Gráfico Radar dinámico
  • Presentación PowerPoint 16:9 C-Level con Action Titles y plan de blindaje (Moat)
  • Guía Metodológica PDF con protocolo de poder de mercado
  • Versiones completas en Español e Inglés + Acceso a Google Sheets

--------------------------------------------------------------------------------
PRODUCTO 3: Matriz PESTEL Cuantitativa: Severidad, Volatilidad & Riesgo Macro Dual (ES/EN)
--------------------------------------------------------------------------------
- Nombre: Matriz PESTEL Cuantitativa: Severidad, Volatilidad & Riesgo Macro Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_PESTEL_Dual.zip
- Precio de venta: 5.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-pestel-cuantitativa
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-pestel-cuantitativa
- Entregables incluidos:
  • Excel (.xlsx) bidimensional con Severidad vs. Volatilidad y Mapa Térmico
  • Presentación PowerPoint 16:9 C-Level con matriz de incertidumbre y plan de resiliencia
  • Guía Metodológica PDF con framework de anticipación macro
  • Versiones completas en Español e Inglés + Acceso a Google Sheets

--------------------------------------------------------------------------------
PRODUCTO 4: Matriz BCG Dinámica de Cartera & Asignación de Capital Dual (ES/EN)
--------------------------------------------------------------------------------
- Nombre: Matriz BCG Dinámica de Cartera & Asignación de Capital Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_BCG_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-bcg-dinamica
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-bcg-dinamica
- Entregables incluidos:
  • Excel (.xlsx) con cálculo automático de CMR y Gráfico de Burbujas proporcional a facturación
  • Presentación PowerPoint 16:9 C-Level con balance Estrellas/Vacas/Interrogantes/Perros
  • Guía Metodológica PDF con reglas de asignación y preservación de flujo de caja
  • Versiones completas en Español e Inglés + Acceso a Google Sheets

--------------------------------------------------------------------------------
PRODUCTO 5: Matriz McKinsey / GE 3x3 & Asignación de Capital Dual (ES/EN)
--------------------------------------------------------------------------------
- Nombre: Matriz McKinsey / GE 3x3 & Asignación de Capital Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_McKinsey_GE_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-mckinsey-ge
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-mckinsey-ge
- Entregables incluidos:
  • Excel (.xlsx) multifactorial de 9 cuadrantes con semáforo por Zonas de Capital
  • Presentación PowerPoint 16:9 C-Level con Board Decision Gateway y mandatos de CAPEX
  • Guía Metodológica PDF con protocolo de gobernanza Minto y FAQ para directores
  • Versiones completas en Español e Inglés + Acceso a Google Sheets

================================================================================
MEGA BUNDLE: SUITE 01 · ESTRATEGIA CORPORATIVA & MBA (COLECCIÓN COMPLETA)
================================================================================
- Nombre: Mega Bundle: Suite 01 · Estrategia Corporativa & MBA Dual (ES/EN)
- Archivo descargable: Executive_Decision_Bundle_Suite_01_Estrategia_MBA_Dual.zip
- Precio de venta: 19.00 € (Precio ancla: 28.00 € | Ahorro: 32%)
- Slug recomendado: suite-01-estrategia-mba
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/suite-01-estrategia-mba
- Contenido:
  • Los 5 Executive Decision Packs íntegros (DAFO + Porter + PESTEL + BCG + McKinsey)
  • 10 Motores de Cálculo en Excel (.xlsx)
  • 10 Presentaciones Ejecutivas 16:9 en PowerPoint (.pptx)
  • 10 Guías Metodológicas Editoriales en PDF (.pdf)
  • Acceso completo a Google Sheets en ambos idiomas
================================================================================
"""

def main():
    print("Iniciando organizacion y empaquetado de packages/...")

    # 1. Eliminar archivos sueltos redundantes de la raiz de packages/
    loose_redundant = [
        "EN_McKinsey_GE_Matrix_Datalaria.xlsx",
        "EN_McKinsey_GE_Matrix_Methodology_Guide.pdf",
        "EN_McKinsey_GE_Matrix_Presentation.pptx",
        "ES_Guia_Metodologica_Matriz_McKinsey_GE.pdf",
        "ES_Matriz_McKinsey_GE_Datalaria.xlsx",
        "ES_Matriz_McKinsey_GE_Presentacion.pptx",
    ]
    for fname in loose_redundant:
        p = os.path.join(BASE_DIR, fname)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"  [LIMPIEZA] Eliminado archivo suelto redundante: {fname}")
            except Exception as e:
                print(f"  [AVISO] No se pudo eliminar {fname} (posiblemente abierto en Excel): {e}")

    # 2. Crear carpetas de Suites
    os.makedirs(DIR_SUITE_01, exist_ok=True)
    os.makedirs(DIR_SUITE_02, exist_ok=True)
    os.makedirs(DIR_SUITE_03, exist_ok=True)
    os.makedirs(DIR_DISTRIB, exist_ok=True)

    # 3. Mapear y clasificar los 5 packs de la Suite 01
    suite_01_packs = [
        {
            "id": "01_DAFO_Cuantitativo_CAME",
            "dir_es_src": os.path.join(BASE_DIR, "01_Espanol_DAFO_CAME"),
            "dir_es_target": "[ES]_DAFO_CAME",
            "dir_en_src": os.path.join(BASE_DIR, "02_English_SWOT_TOWS"),
            "dir_en_target": "[EN]_SWOT_TOWS",
            "zip_name": "Executive_Decision_Pack_DAFO_SWOT_Dual.zip",
        },
        {
            "id": "02_5_Fuerzas_Porter",
            "dir_es_src": os.path.join(BASE_DIR, "[ES]_5_Fuerzas_Porter"),
            "dir_es_target": "[ES]_5_Fuerzas_Porter",
            "dir_en_src": os.path.join(BASE_DIR, "[EN]_Porter_5_Forces"),
            "dir_en_target": "[EN]_Porter_5_Forces",
            "zip_name": "Executive_Decision_Pack_Porter_5_Forces_Dual.zip",
        },
        {
            "id": "03_PESTEL_Cuantitativo",
            "dir_es_src": os.path.join(BASE_DIR, "[ES]_PESTEL_Cuantitativo"),
            "dir_es_target": "[ES]_PESTEL_Cuantitativo",
            "dir_en_src": os.path.join(BASE_DIR, "[EN]_Quantitative_PESTEL"),
            "dir_en_target": "[EN]_Quantitative_PESTEL",
            "zip_name": "Executive_Decision_Pack_PESTEL_Dual.zip",
        },
        {
            "id": "04_BCG_Dinamica",
            "dir_es_src": os.path.join(BASE_DIR, "[ES]_BCG_Dinamica"),
            "dir_es_target": "[ES]_BCG_Dinamica",
            "dir_en_src": os.path.join(BASE_DIR, "[EN]_Dynamic_BCG"),
            "dir_en_target": "[EN]_Dynamic_BCG",
            "zip_name": "Executive_Decision_Pack_BCG_Dual.zip",
        },
        {
            "id": "05_Matriz_McKinsey_GE",
            "dir_es_src": os.path.join(BASE_DIR, "[ES]_Matriz_McKinsey_GE"),
            "dir_es_target": "[ES]_Matriz_McKinsey_GE",
            "dir_en_src": os.path.join(BASE_DIR, "[EN]_McKinsey_GE_Matrix"),
            "dir_en_target": "[EN]_McKinsey_GE_Matrix",
            "zip_name": "Executive_Decision_Pack_McKinsey_GE_Dual.zip",
        }
    ]

    for pinfo in suite_01_packs:
        pack_dir = os.path.join(DIR_SUITE_01, pinfo["id"])
        os.makedirs(pack_dir, exist_ok=True)

        target_es = os.path.join(pack_dir, pinfo["dir_es_target"])
        if os.path.exists(pinfo["dir_es_src"]) and not os.path.exists(target_es):
            shutil.move(pinfo["dir_es_src"], target_es)
            print(f"  [MOVIDO] {os.path.basename(pinfo['dir_es_src'])} -> {pinfo['id']}/{pinfo['dir_es_target']}")
        elif os.path.exists(target_es):
            print(f"  [OK] Carpeta ES ya presente: {pinfo['id']}/{pinfo['dir_es_target']}")

        target_en = os.path.join(pack_dir, pinfo["dir_en_target"])
        if os.path.exists(pinfo["dir_en_src"]) and not os.path.exists(target_en):
            shutil.move(pinfo["dir_en_src"], target_en)
            print(f"  [MOVIDO] {os.path.basename(pinfo['dir_en_src'])} -> {pinfo['id']}/{pinfo['dir_en_target']}")
        elif os.path.exists(target_en):
            print(f"  [OK] Carpeta EN ya presente: {pinfo['id']}/{pinfo['dir_en_target']}")

        # Mover o copiar el ZIP del pack al directorio del pack y al de distribucion
        src_zip = os.path.join(BASE_DIR, pinfo["zip_name"])
        pack_zip = os.path.join(pack_dir, pinfo["zip_name"])
        distrib_zip = os.path.join(DIR_DISTRIB, pinfo["zip_name"])

        if os.path.exists(src_zip):
            shutil.copy2(src_zip, pack_zip)
            shutil.copy2(src_zip, distrib_zip)
            try:
                os.remove(src_zip) # Limpiar de la raiz
            except Exception as e:
                print(f"  [AVISO] No se pudo eliminar zip raiz {src_zip}: {e}")
            print(f"  [ZIP] Centralizado {pinfo['zip_name']} en pack y en distribucion")
        elif os.path.exists(pack_zip):
            if not os.path.exists(distrib_zip):
                shutil.copy2(pack_zip, distrib_zip)
            print(f"  [ZIP] Confirmado {pinfo['zip_name']} en {pinfo['id']}")

    # 4. Crear subdirectorios de preparacion para Suite 02 y Suite 03
    suite_02_packs = [
        ("01_Matriz_DAR_Cuantitativa", "Matriz DAR (Decision Analysis & Resolution) con Criterios Veto"),
        ("02_Matriz_RICE_ICE_Agil", "Matriz RICE & ICE de Priorización Ágil"),
        ("03_Business_Case_VAN_TIR", "Business Case Financiero (VAN, TIR, Payback)"),
    ]
    for sname, sdesc in suite_02_packs:
        sp = os.path.join(DIR_SUITE_02, sname)
        os.makedirs(sp, exist_ok=True)
        readme_path = os.path.join(sp, "README_PLANIFICACION.txt")
        if not os.path.exists(readme_path):
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"Datalaria | Executive Decision Pack\n{sname}\n{sdesc}\nEstado: En preparación para Lote 2.\n")

    suite_03_packs = [
        ("01_Matriz_RACI_Balance_Carga", "Matriz RACI con Balance de Carga & Cuellos de Botella"),
        ("02_Matriz_Riesgos_AMFE", "Matriz de Riesgos & AMFE / FMEA Cuantitativo"),
        ("03_Estimacion_PERT_3_Puntos", "Estimación PERT de 3 Puntos Estocástica"),
        ("04_Cuadro_EVM_Valor_Ganado", "Cuadro de Mando EVM / Valor Ganado (Curva S)"),
        ("05_Stock_Seguridad_ROP", "Calculadora de Stock de Seguridad & ROP"),
    ]
    for sname, sdesc in suite_03_packs:
        sp = os.path.join(DIR_SUITE_03, sname)
        os.makedirs(sp, exist_ok=True)
        readme_path = os.path.join(sp, "README_PLANIFICACION.txt")
        if not os.path.exists(readme_path):
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"Datalaria | Executive Decision Pack\n{sname}\n{sdesc}\nEstado: En preparación para Lote 3.\n")

    # 5. Generar archivos informativos de la Suite 01
    leeme_suite_path = os.path.join(DIR_SUITE_01, "LEEME_SUITE_01_ESTRATEGIA_MBA.txt")
    with open(leeme_suite_path, "w", encoding="utf-8") as f:
        f.write(LEEME_SUITE_01_ES)

    readme_suite_path = os.path.join(DIR_SUITE_01, "README_SUITE_01_CORPORATE_STRATEGY.txt")
    with open(readme_suite_path, "w", encoding="utf-8") as f:
        f.write(README_SUITE_01_EN)

    # 6. Generar el MEGA BUNDLE ZIP oficial de la Suite 01
    bundle_zip_name = "Executive_Decision_Bundle_Suite_01_Estrategia_MBA_Dual.zip"
    bundle_zip_path_s01 = os.path.join(DIR_SUITE_01, bundle_zip_name)
    bundle_zip_path_distrib = os.path.join(DIR_DISTRIB, bundle_zip_name)

    print(f"\nGenerando MEGA BUNDLE ZIP: {bundle_zip_name}...")
    with zipfile.ZipFile(bundle_zip_path_s01, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Añadir archivos de cabecera a la raíz del ZIP
        zipf.write(leeme_suite_path, arcname="LEEME_SUITE_01_ESTRATEGIA_MBA.txt")
        zipf.write(readme_suite_path, arcname="README_SUITE_01_CORPORATE_STRATEGY.txt")

        leeme_gs = os.path.join(BASE_DIR, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
        if os.path.exists(leeme_gs):
            zipf.write(leeme_gs, arcname="LEEME_ACCESO_GOOGLE_SHEETS.txt")
        readme_gs = os.path.join(BASE_DIR, "README_GOOGLE_SHEETS_ACCESS.txt")
        if os.path.exists(readme_gs):
            zipf.write(readme_gs, arcname="README_GOOGLE_SHEETS_ACCESS.txt")

        # Añadir los 5 packs estructurados por idioma
        # Mapeo de carpetas de destino en el bundle:
        # 01_VERSION_ESPANOL/
        #   01_DAFO_Cuantitativo_CAME/
        #   02_5_Fuerzas_Porter/
        #   03_PESTEL_Cuantitativo/
        #   04_BCG_Dinamica/
        #   05_Matriz_McKinsey_GE/
        # 02_ENGLISH_VERSION/
        #   01_Quantitative_SWOT_TOWS/
        #   02_Porter_5_Forces/
        #   03_Quantitative_PESTEL/
        #   04_Dynamic_BCG/
        #   05_McKinsey_GE_Matrix/
        bundle_map = [
            ("01_DAFO_Cuantitativo_CAME", "[ES]_DAFO_CAME", "01_VERSION_ESPANOL/01_DAFO_Cuantitativo_CAME",
             "[EN]_SWOT_TOWS", "02_ENGLISH_VERSION/01_Quantitative_SWOT_TOWS"),
            ("02_5_Fuerzas_Porter", "[ES]_5_Fuerzas_Porter", "01_VERSION_ESPANOL/02_5_Fuerzas_Porter",
             "[EN]_Porter_5_Forces", "02_ENGLISH_VERSION/02_Porter_5_Forces"),
            ("03_PESTEL_Cuantitativo", "[ES]_PESTEL_Cuantitativo", "01_VERSION_ESPANOL/03_PESTEL_Cuantitativo",
             "[EN]_Quantitative_PESTEL", "02_ENGLISH_VERSION/03_Quantitative_PESTEL"),
            ("04_BCG_Dinamica", "[ES]_BCG_Dinamica", "01_VERSION_ESPANOL/04_BCG_Dinamica",
             "[EN]_Dynamic_BCG", "02_ENGLISH_VERSION/04_Dynamic_BCG"),
            ("05_Matriz_McKinsey_GE", "[ES]_Matriz_McKinsey_GE", "01_VERSION_ESPANOL/05_Matriz_McKinsey_GE",
             "[EN]_McKinsey_GE_Matrix", "02_ENGLISH_VERSION/05_McKinsey_GE_Matrix"),
        ]

        total_files_packed = 0
        for pid, es_sub, es_arc, en_sub, en_arc in bundle_map:
            pack_dir = os.path.join(DIR_SUITE_01, pid)
            es_path = os.path.join(pack_dir, es_sub)
            en_path = os.path.join(pack_dir, en_sub)

            # Archivos ES
            if os.path.exists(es_path):
                for f in sorted(os.listdir(es_path)):
                    fpath = os.path.join(es_path, f)
                    if os.path.isfile(fpath) and not f.startswith("~$"):
                        arc = f"{es_arc}/{f}"
                        zipf.write(fpath, arcname=arc)
                        total_files_packed += 1
                        print(f"  + [BUNDLE ES] {arc}")

            # Archivos EN
            if os.path.exists(en_path):
                for f in sorted(os.listdir(en_path)):
                    fpath = os.path.join(en_path, f)
                    if os.path.isfile(fpath) and not f.startswith("~$"):
                        arc = f"{en_arc}/{f}"
                        zipf.write(fpath, arcname=arc)
                        total_files_packed += 1
                        print(f"  + [BUNDLE EN] {arc}")

    # Copiar el bundle al hub de distribucion
    shutil.copy2(bundle_zip_path_s01, bundle_zip_path_distrib)

    # 7. Crear catálogo para Lemon Squeezy en 00_DISTRIBUCION_LEMONSQUEEZY/
    cat_path = os.path.join(DIR_DISTRIB, "CATALOGO_PRODUCTOS_LEMONSQUEEZY.txt")
    with open(cat_path, "w", encoding="utf-8") as f:
        f.write(CATALOGO_LEMONSQUEEZY_TXT)

    bundle_size_mb = os.path.getsize(bundle_zip_path_s01) / (1024 * 1024)
    print(f"\n[EXITO] Mega Bundle creado con exito: {bundle_zip_name} ({bundle_size_mb:.2f} MB, {total_files_packed} archivos)")
    print(f"[EXITO] Hub de distribucion listo en: packages/00_DISTRIBUCION_LEMONSQUEEZY/")
    print(f"[EXITO] Clasificacion de suites completada.")

if __name__ == "__main__":
    main()
