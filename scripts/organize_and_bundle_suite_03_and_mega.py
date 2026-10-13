#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organize_and_bundle_suite_03_and_mega.py
========================================
Script maestro de empaquetado y distribución para Lemon Squeezy:
1. Limpia archivos residuales temporales en packages/Suite_03_Control_Operativo.
2. Genera los archivos oficiales de bienvenida de Suite 03:
   - LEEME_SUITE_03_CONTROL_OPERATIVO.txt
   - README_SUITE_03_OPERATIONAL_CONTROL.txt
3. Construye el paquete ZIP de Suite 03:
   Executive_Decision_Bundle_Suite_03_Control_Operativo_Dual.zip
   con arquitectura bilingüe (01_VERSION_ESPANOL / 02_ENGLISH_VERSION).
4. Genera los archivos oficiales de bienvenida del MEGA BUNDLE COMPLETO (3 Suites, 13 Packs):
   - LEEME_MEGA_BUNDLE_3_SUITES.txt
   - README_MEGA_BUNDLE_3_SUITES.txt
5. Construye el archivo ZIP del MEGA BUNDLE COMPLETO:
   Executive_Decision_MEGA_BUNDLE_3_Suites_Complete_Dual.zip
   con estructura bilingüe y jerarquía de 3 suites.
6. Sincroniza ambos ZIPs en packages/00_DISTRIBUCION_LEMONSQUEEZY/.
7. Actualiza CATALOGO_PRODUCTOS_LEMONSQUEEZY.txt con todos los 13 productos y los 4 bundles.
"""

import os
import shutil
import zipfile

BASE_DIR = os.path.abspath("packages")
DIR_SUITE_01 = os.path.join(BASE_DIR, "Suite_01_Estrategia_MBA")
DIR_SUITE_02 = os.path.join(BASE_DIR, "Suite_02_Toma_Decisiones")
DIR_SUITE_03 = os.path.join(BASE_DIR, "Suite_03_Control_Operativo")
DIR_DISTRIB = os.path.join(BASE_DIR, "00_DISTRIBUCION_LEMONSQUEEZY")

# ==============================================================================
# TEXTOS INFORMATIVOS SUITE 03
# ==============================================================================
LEEME_SUITE_03_ES = """================================================================================
DATALARIA | MEGA BUNDLE EJECUTIVO: SUITE 03 · CONTROL OPERATIVO & MÉTRICAS PMBOK
Colección Oficial Completa de Herramientas Cuantitativas de Operaciones (Edición 2026)
================================================================================

Muchas gracias por adquirir el Mega Bundle de la Suite 03: Control Operativo & 
Métricas PMBOK de Datalaria.com.

Este ecosistema directivo reúne los 5 Executive Decision Packs oficiales diseñados 
para transformar la gestión operativa tradicional (a menudo reactiva y basada en conjeturas) 
en un motor cuantitativo y predictivo con rigor matemático ante Comités de Dirección 
(C-Level), COOs, Directores de Operaciones y PMOs:

--------------------------------------------------------------------------------
1. ESTRUCTURA Y CONTENIDO DE ESTE PAQUETE (.ZIP)
--------------------------------------------------------------------------------
Este archivo comprimido contiene las ediciones oficiales completas tanto en Español 
como en Inglés, organizadas en carpetas independientes para máxima comodidad directiva:

📁 01_VERSION_ESPANOL/
   ├── 📁 01_Matriz_RACI_Balance_Carga/
   │   ├── Matriz_RACI_Balance_Carga_ES.xlsx (Gobernanza con Accountable único y FTEs)
   │   ├── Presentacion_RACI_CLevel_ES.pptx (Deck 16:9 con organigrama matricial)
   │   ├── Guia_Metodologica_RACI_ES.pdf (Guía editorial de resolución de patologías)
   │   └── LEEME_INSTRUCCIONES.txt (Instrucciones detalladas y contraseñas)
   │
   ├── 📁 02_Matriz_Riesgos_AMFE/
   │   ├── Matriz_Riesgos_AMFE_Datalaria_ES.xlsx (Matriz 5x5 ISO 31000 y FMEA con NPR)
   │   ├── Presentacion_AMFE_Riesgos_CLevel_ES.pptx (Deck 16:9 con mapa térmico y Pareto)
   │   ├── Guia_Metodologica_AMFE_Riesgos_ES.pdf (Guía metodológica actuarial y AIAG-VDA)
   │   └── LEEME_INSTRUCCIONES.txt
   │
   ├── 📁 03_Estimacion_PERT_3_Puntos/
   │   ├── Estimacion_PERT_Estocastica_ES.xlsx (Distribución Beta, CLT, Z-Score y buffers)
   │   ├── Presentacion_PERT_CLevel_ES.pptx (Deck 16:9 con curva de campana y tornado)
   │   ├── Guia_Metodologica_PERT_ES.pdf (Guía matemática de incertidumbre temporal)
   │   └── LEEME_INSTRUCCIONES.txt
   │
   ├── 📁 04_Cuadro_EVM_Valor_Ganado/
   │   ├── Cuadro_Mando_EVM_Datalaria_ES.xlsx (PV, EV, AC, Curva S nativa, 3 EACs y TCPI)
   │   ├── Presentacion_EVM_CLevel_ES.pptx (Deck 16:9 con salud financiera del proyecto)
   │   ├── Guia_Metodologica_EVM_ES.pdf (Guía metodológica ANSI/EIA-748 y PMBOK)
   │   └── LEEME_INSTRUCCIONES.txt
   │
   └── 📁 05_Stock_Seguridad_ROP/
       ├── Calculadora_Stock_Seguridad_ROP_ES.xlsx (3 modelos estocásticos, EOQ y Diente Sierra)
       ├── Presentacion_Stock_ROP_CLevel_ES.pptx (Deck 16:9 con trade-offs de Working Capital)
       ├── Guia_Metodologica_Stock_ROP_ES.pdf (Guía de optimización de capital circulante)
       └── LEEME_INSTRUCCIONES.txt

📁 02_ENGLISH_VERSION/
   ├── 📁 01_Quantitative_RACI_Workload/
   │   ├── Quantitative_RACI_Workload_EN.xlsx
   │   ├── Deck_RACI_CLevel_EN.pptx
   │   ├── Methodology_Guide_RACI_EN.pdf
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 02_FMEA_Risk_Matrix/
   │   ├── Quantitative_Risk_Matrix_FMEA_EN.xlsx
   │   ├── Deck_FMEA_Risk_CLevel_EN.pptx
   │   ├── Methodology_Guide_FMEA_Risk_EN.pdf
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 03_3Point_PERT_Estimation/
   │   ├── Stochastic_PERT_Estimation_EN.xlsx
   │   ├── Deck_PERT_CLevel_EN.pptx
   │   ├── Methodology_Guide_PERT_EN.pdf
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 04_Earned_Value_Management_EVM/
   │   ├── EVM_Dashboard_Datalaria_EN.xlsx
   │   ├── Deck_EVM_CLevel_EN.pptx
   │   ├── Methodology_Guide_EVM_EN.pdf
   │   └── README_INSTRUCTIONS.txt
   │
   └── 📁 05_Safety_Stock_ROP/
       ├── Safety_Stock_ROP_Calculator_EN.xlsx
       ├── Deck_Safety_Stock_ROP_CLevel_EN.pptx
       ├── Methodology_Guide_Safety_Stock_ROP_EN.pdf
       └── README_INSTRUCTIONS.txt

--------------------------------------------------------------------------------
2. PROTOCOLO DE DESBLOQUEO Y EDICIÓN EN EXCEL Y GOOGLE SHEETS
--------------------------------------------------------------------------------
• Todas las celdas de entrada y datos (inputs) vienen desbloqueadas por defecto 
  (con fondo blanco #FFFFFF) para permitir edición inmediata, doble clic y 
  escenarios personalizados sin necesidad de contraseñas.
• Las celdas de fórmulas, ponderaciones matriciales, totales calculados y 
  cabeceras se encuentran protegidas para evitar corrupciones accidentales.
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

README_SUITE_03_EN = """================================================================================
DATALARIA | EXECUTIVE MEGA BUNDLE: SUITE 03 · OPERATIONAL CONTROL & PMBOK
Complete Official Quantitative Operations Toolkits (2026 Edition)
================================================================================

Thank you for purchasing the official Suite 03: Operational Control & PMBOK 
Mega Bundle from Datalaria.com.

This executive toolkit brings together all 5 official Executive Decision Packs designed 
to turn traditional reactive operations into a predictive quantitative engine with 
mathematical rigor defendable before Executive Committees (C-Level), COOs, and PMOs:

--------------------------------------------------------------------------------
1. STRUCTURE & CONTENT OF THIS BUNDLE (.ZIP)
--------------------------------------------------------------------------------
This archive contains the complete official editions in both Spanish and English, 
organized into separate folders for executive convenience:

📁 01_VERSION_ESPANOL/
   (Contains all 5 complete packs in Spanish)

📁 02_ENGLISH_VERSION/
   ├── 📁 01_Quantitative_RACI_Workload/
   │   ├── Quantitative_RACI_Workload_EN.xlsx (Single Accountable governance & FTEs)
   │   ├── Deck_RACI_CLevel_EN.pptx (16:9 deck with matrix org chart & Board Gateway)
   │   ├── Methodology_Guide_RACI_EN.pdf (Executive guide, workload models & pathologies)
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 02_FMEA_Risk_Matrix/
   │   ├── Quantitative_Risk_Matrix_FMEA_EN.xlsx (5x5 matrix & 3D FMEA with RPN)
   │   ├── Deck_FMEA_Risk_CLevel_EN.pptx (16:9 deck with heat map & Pareto chart)
   │   ├── Methodology_Guide_FMEA_Risk_EN.pdf (Actuarial & AIAG-VDA methodology guide)
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 03_3Point_PERT_Estimation/
   │   ├── Stochastic_PERT_Estimation_EN.xlsx (Beta distribution, CLT, Z-Score & buffers)
   │   ├── Deck_PERT_CLevel_EN.pptx (16:9 deck with bell curve & sensitivity tornado)
   │   ├── Methodology_Guide_PERT_EN.pdf (Mathematical guide on schedule uncertainty)
   │   └── README_INSTRUCTIONS.txt
   │
   ├── 📁 04_Earned_Value_Management_EVM/
   │   ├── EVM_Dashboard_Datalaria_EN.xlsx (PV, EV, AC, native S-Curve, 3 EACs & TCPI)
   │   ├── Deck_EVM_CLevel_EN.pptx (16:9 deck with project financial health & Gateway)
   │   ├── Methodology_Guide_EVM_EN.pdf (ANSI/EIA-748 & PMBOK methodology guide)
   │   └── README_INSTRUCTIONS.txt
   │
   └── 📁 05_Safety_Stock_ROP/
       ├── Safety_Stock_ROP_Calculator_EN.xlsx (3 stochastic models, EOQ & Sawtooth chart)
       ├── Deck_Safety_Stock_ROP_CLevel_EN.pptx (16:9 deck with Working Capital trade-offs)
       ├── Methodology_Guide_Safety_Stock_ROP_EN.pdf (Working capital optimization guide)
       └── README_INSTRUCTIONS.txt

--------------------------------------------------------------------------------
2. PROTOCOL FOR EXCEL & GOOGLE SHEETS EDITING
--------------------------------------------------------------------------------
• All input cells come unlocked by default (white background #FFFFFF) to allow 
  immediate editing, double-clicking, and scenario testing without passwords.
• Formula cells, array calculations, totals, and headers are protected to prevent 
  accidental alterations.
• If advanced structural customizations are required in Excel or Google Sheets, 
  the master unprotect password is: Datalaria2026

--------------------------------------------------------------------------------
3. CORPORATE SUPPORT & UPDATES
--------------------------------------------------------------------------------
For methodology inquiries, spreadsheet assistance, or questions:
• Official Website: https://datalaria.com
• Direct Support: datalaria@gmail.com
• Resources & Updates: https://datalaria.com/en/resources/
================================================================================
"""

# ==============================================================================
# TEXTOS INFORMATIVOS MEGA BUNDLE 3 SUITES (13 PACKS)
# ==============================================================================
LEEME_MEGA_BUNDLE_3_SUITES_ES = """================================================================================
DATALARIA | MEGA BUNDLE COMPLETO: LAS 3 SUITES EJECUTIVAS (13 DECISION PACKS)
Colección Oficial Maestra de Herramientas Cuantitativas de Estrategia & Decisión (2026)
================================================================================

¡Enhorabuena y muchas gracias por adquirir el MEGA BUNDLE DEFINITIVO de Datalaria.com!

Tienes en tus manos el arsenal completo de toma de decisiones estratégicas, operativas 
y directivas. Un compendio de 13 Executive Decision Packs oficiales diseñados según 
los estándares más exigentes de la consultoría de élite (McKinsey, BCG, CMMI, PMBOK, 
APICS e ISO 31000).

Cada pack ha sido construido para resolver la "última milla ejecutiva": transformar 
la intuición y las diapositivas subjetivas en modelos matemáticos contrastables, 
presentaciones ejecutivas 16:9 con Pirámide de Minto y guías metodológicas con las 
fórmulas y argumentos para defender cada iniciativa ante el Consejo de Administración.

--------------------------------------------------------------------------------
1. CONTENIDO TOTAL DEL MEGA BUNDLE
--------------------------------------------------------------------------------
El paquete reúne los siguientes activos:
• 26 Motores de Cálculo en Microsoft Excel (.xlsx) y Google Sheets (13 ES + 13 EN)
• 26 Presentaciones Ejecutivas 16:9 en PowerPoint (.pptx) con Board Gateways (13 ES + 13 EN)
• 26 Guías Metodológicas Editoriales en PDF (.pdf) listas para imprimir o auditar
• Acceso directo a Google Sheets en ambos idiomas
• Soporte prioritario permanente vía datalaria@gmail.com

--------------------------------------------------------------------------------
2. ARQUITECTURA DE CARPETAS EN ESTE ARCHIVO (.ZIP)
--------------------------------------------------------------------------------
El archivo se encuentra estructurado de forma jerárquica y limpia:

📁 01_VERSION_ESPANOL/
   ├── 📁 Suite_01_Estrategia_Corporativa_MBA/
   │   ├── 📁 01_DAFO_Cuantitativo_CAME/
   │   ├── 📁 02_5_Fuerzas_Porter/
   │   ├── 📁 03_PESTEL_Cuantitativo/
   │   ├── 📁 04_BCG_Dinamica/
   │   └── 📁 05_Matriz_McKinsey_GE/
   │
   ├── 📁 Suite_02_Toma_Decisiones_Priorizacion/
   │   ├── 📁 01_Matriz_DAR_Cuantitativa/
   │   ├── 📁 02_Matriz_RICE_ICE_Agil/
   │   └── 📁 03_Business_Case_VAN_TIR/
   │
   └── 📁 Suite_03_Control_Operativo_PMBOK/
       ├── 📁 01_Matriz_RACI_Balance_Carga/
       ├── 📁 02_Matriz_Riesgos_AMFE/
       ├── 📁 03_Estimacion_PERT_3_Puntos/
       ├── 📁 04_Cuadro_EVM_Valor_Ganado/
       └── 📁 05_Stock_Seguridad_ROP/

📁 02_ENGLISH_VERSION/
   ├── 📁 Suite_01_Corporate_Strategy_MBA/
   │   ├── 📁 01_Quantitative_SWOT_TOWS/
   │   ├── 📁 02_Porter_5_Forces/
   │   ├── 📁 03_Quantitative_PESTEL/
   │   ├── 📁 04_Dynamic_BCG/
   │   └── 📁 05_McKinsey_GE_Matrix/
   │
   ├── 📁 Suite_02_Decision_Analysis_Prioritization/
   │   ├── 📁 01_Quantitative_DAR/
   │   ├── 📁 02_RICE_ICE_Matrix/
   │   └── 📁 03_Financial_Business_Case/
   │
   └── 📁 Suite_03_Operational_Control_PMBOK/
       ├── 📁 01_Quantitative_RACI_Workload/
       ├── 📁 02_FMEA_Risk_Matrix/
       ├── 📁 03_3Point_PERT_Estimation/
       ├── 📁 04_Earned_Value_Management_EVM/
       └── 📁 05_Safety_Stock_ROP/

--------------------------------------------------------------------------------
3. PROTOCOLO DE DESBLOQUEO Y EDICIÓN
--------------------------------------------------------------------------------
• Todas las celdas de entrada y datos (inputs) vienen desbloqueadas por defecto 
  (con fondo blanco #FFFFFF) para permitir edición inmediata sin contraseñas.
• Las celdas de fórmulas y cálculos se encuentran protegidas bajo estándar ECMA-376 
  para salvaguardar la integridad de las plantillas.
• La contraseña unificada oficial para desproteger las fórmulas es: Datalaria2026

--------------------------------------------------------------------------------
4. CONTACTO Y SOPORTE EJECUTIVO
--------------------------------------------------------------------------------
Para cualquier consulta técnica, feedback o soporte con los modelos:
• Web: https://datalaria.com
• Email directo: datalaria@gmail.com
================================================================================
"""

README_MEGA_BUNDLE_3_SUITES_EN = """================================================================================
DATALARIA | COMPLETE MEGA BUNDLE: ALL 3 EXECUTIVE SUITES (13 DECISION PACKS)
Official Master Collection of Quantitative Strategy & Decision Toolkits (2026)
================================================================================

Congratulations and thank you for purchasing the DEFINITIVE MEGA BUNDLE from Datalaria.com!

You have acquired the complete C-Level decision-making arsenal. A comprehensive 
collection of 13 official Executive Decision Packs designed according to elite tier-1 
consulting standards (McKinsey, BCG, CMMI, PMBOK, APICS, and ISO 31000).

Every pack solves the "executive last mile": transforming intuition and qualitative 
decks into robust mathematical models, 16:9 C-Level presentations with Minto Pyramid 
action titles, and methodology guides with formulas to defend proposals before the Board.

--------------------------------------------------------------------------------
1. TOTAL CONTENT OF THE MASTER BUNDLE
--------------------------------------------------------------------------------
This bundle includes:
• 26 Quantitative Calculation Engines in Excel (.xlsx) & Google Sheets (13 ES + 13 EN)
• 26 Executive 16:9 Presentations in PowerPoint (.pptx) with Board Gateways (13 ES + 13 EN)
• 26 Editorial Methodology Guides in PDF (.pdf) ready for boardroom defense
• Full Google Sheets access in both languages
• Priority support via datalaria@gmail.com

--------------------------------------------------------------------------------
2. FOLDER ARCHITECTURE IN THIS ARCHIVE (.ZIP)
--------------------------------------------------------------------------------
📁 01_VERSION_ESPANOL/
   (Contains all 3 complete suites with 13 packs in Spanish)

📁 02_ENGLISH_VERSION/
   ├── 📁 Suite_01_Corporate_Strategy_MBA/
   │   ├── 📁 01_Quantitative_SWOT_TOWS/
   │   ├── 📁 02_Porter_5_Forces/
   │   ├── 📁 03_Quantitative_PESTEL/
   │   ├── 📁 04_Dynamic_BCG/
   │   └── 📁 05_McKinsey_GE_Matrix/
   │
   ├── 📁 Suite_02_Decision_Analysis_Prioritization/
   │   ├── 📁 01_Quantitative_DAR/
   │   ├── 📁 02_RICE_ICE_Matrix/
   │   └── 📁 03_Financial_Business_Case/
   │
   └── 📁 Suite_03_Operational_Control_PMBOK/
       ├── 📁 01_Quantitative_RACI_Workload/
       ├── 📁 02_FMEA_Risk_Matrix/
       ├── 📁 03_3Point_PERT_Estimation/
       ├── 📁 04_Earned_Value_Management_EVM/
       └── 📁 05_Safety_Stock_ROP/

--------------------------------------------------------------------------------
3. UNPROTECT & CUSTOMIZATION PROTOCOL
--------------------------------------------------------------------------------
• All user input cells are unlocked by default (white background #FFFFFF).
• Formula cells and totals are protected to preserve model integrity.
• If deep structural customization is needed, the master unprotect password is: Datalaria2026

--------------------------------------------------------------------------------
4. EXECUTIVE SUPPORT
--------------------------------------------------------------------------------
• Website: https://datalaria.com
• Email: datalaria@gmail.com
================================================================================
"""

# ==============================================================================
# DEFINICIONES DE SUITES Y PACKS PARA EL EMPAQUETADO
# ==============================================================================
SUITE_03_PACKS = [
    {
        "id": "01",
        "dir": "01_Matriz_RACI_Balance_Carga",
        "es_src": "[ES]_Matriz_RACI_Balance_Carga",
        "en_src": "[EN]_Quantitative_RACI_Workload",
        "es_dest": "01_Matriz_RACI_Balance_Carga",
        "en_dest": "01_Quantitative_RACI_Workload",
    },
    {
        "id": "02",
        "dir": "02_Matriz_Riesgos_AMFE",
        "es_src": "[ES]_Matriz_Riesgos_AMFE",
        "en_src": "[EN]_FMEA_Risk_Matrix",
        "es_dest": "02_Matriz_Riesgos_AMFE",
        "en_dest": "02_FMEA_Risk_Matrix",
    },
    {
        "id": "03",
        "dir": "03_Estimacion_PERT_3_Puntos",
        "es_src": "[ES]_Estimacion_PERT_3_Puntos",
        "en_src": "[EN]_3Point_PERT_Estimation",
        "es_dest": "03_Estimacion_PERT_3_Puntos",
        "en_dest": "03_3Point_PERT_Estimation",
    },
    {
        "id": "04",
        "dir": "04_Cuadro_EVM_Valor_Ganado",
        "es_src": "[ES]_Cuadro_EVM_Valor_Ganado",
        "en_src": "[EN]_Earned_Value_Management_EVM",
        "es_dest": "04_Cuadro_EVM_Valor_Ganado",
        "en_dest": "04_Earned_Value_Management_EVM",
    },
    {
        "id": "05",
        "dir": "05_Stock_Seguridad_ROP",
        "es_src": "[ES]_Stock_Seguridad_ROP",
        "en_src": "[EN]_Safety_Stock_ROP",
        "es_dest": "05_Stock_Seguridad_ROP",
        "en_dest": "05_Safety_Stock_ROP",
    },
]

SUITE_01_PACKS = [
    {
        "dir": "01_DAFO_Cuantitativo_CAME",
        "es_src": "[ES]_DAFO_CAME",
        "en_src": "[EN]_SWOT_TOWS",
        "es_dest": "01_DAFO_Cuantitativo_CAME",
        "en_dest": "01_Quantitative_SWOT_TOWS",
    },
    {
        "dir": "02_5_Fuerzas_Porter",
        "es_src": "[ES]_5_Fuerzas_Porter",
        "en_src": "[EN]_Porter_5_Forces",
        "es_dest": "02_5_Fuerzas_Porter",
        "en_dest": "02_Porter_5_Forces",
    },
    {
        "dir": "03_PESTEL_Cuantitativo",
        "es_src": "[ES]_PESTEL_Cuantitativo",
        "en_src": "[EN]_Quantitative_PESTEL",
        "es_dest": "03_PESTEL_Cuantitativo",
        "en_dest": "03_Quantitative_PESTEL",
    },
    {
        "dir": "04_BCG_Dinamica",
        "es_src": "[ES]_BCG_Dinamica",
        "en_src": "[EN]_Dynamic_BCG",
        "es_dest": "04_BCG_Dinamica",
        "en_dest": "04_Dynamic_BCG",
    },
    {
        "dir": "05_Matriz_McKinsey_GE",
        "es_src": "[ES]_Matriz_McKinsey_GE",
        "en_src": "[EN]_McKinsey_GE_Matrix",
        "es_dest": "05_Matriz_McKinsey_GE",
        "en_dest": "05_McKinsey_GE_Matrix",
    },
]

SUITE_02_PACKS = [
    {
        "dir": "01_Matriz_DAR_Cuantitativa",
        "es_src": "[ES]_Matriz_DAR",
        "en_src": "[EN]_Quantitative_DAR",
        "es_dest": "01_Matriz_DAR_Cuantitativa",
        "en_dest": "01_Quantitative_DAR",
    },
    {
        "dir": "02_Matriz_RICE_ICE_Agil",
        "es_src": "[ES]_Matriz_RICE_ICE",
        "en_src": "[EN]_RICE_ICE_Matrix",
        "es_dest": "02_Matriz_RICE_ICE_Agil",
        "en_dest": "02_RICE_ICE_Matrix",
    },
    {
        "dir": "03_Business_Case_VAN_TIR",
        "es_src": "[ES]_Business_Case_VAN_TIR",
        "en_src": "[EN]_Financial_Business_Case",
        "es_dest": "03_Business_Case_VAN_TIR",
        "en_dest": "03_Financial_Business_Case",
    },
]


def clean_residual_files(directory):
    """Elimina archivos de planificación residuales o temporales."""
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.startswith("README_PLANIFICACION") or f.startswith("~$") or f.endswith(".tmp"):
                file_path = os.path.join(root, f)
                try:
                    os.remove(file_path)
                    print(f"  [Limpio] Archivo residual eliminado: {f}")
                except Exception as e:
                    print(f"  [Alerta] No se pudo eliminar {f}: {e}")


def build_suite_03_bundle():
    """Construye el ZIP del Mega Bundle de la Suite 03."""
    print("\n" + "=" * 80)
    print("CONSTRUCCIÓN DEL MEGA BUNDLE SUITE 03: CONTROL OPERATIVO & PMBOK")
    print("=" * 80)

    clean_residual_files(DIR_SUITE_03)

    # 1. Escribir textos en raíz de Suite 03
    leeme_es_path = os.path.join(DIR_SUITE_03, "LEEME_SUITE_03_CONTROL_OPERATIVO.txt")
    readme_en_path = os.path.join(DIR_SUITE_03, "README_SUITE_03_OPERATIONAL_CONTROL.txt")
    with open(leeme_es_path, "w", encoding="utf-8") as f:
        f.write(LEEME_SUITE_03_ES)
    with open(readme_en_path, "w", encoding="utf-8") as f:
        f.write(README_SUITE_03_EN)

    zip_filename = "Executive_Decision_Bundle_Suite_03_Control_Operativo_Dual.zip"
    zip_path = os.path.join(DIR_SUITE_03, zip_filename)

    print(f"Generando archivo ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Añadir textos de cabecera en la raíz del ZIP
        zf.write(leeme_es_path, arcname="LEEME_SUITE_03_CONTROL_OPERATIVO.txt")
        zf.write(readme_en_path, arcname="README_SUITE_03_OPERATIONAL_CONTROL.txt")

        # Buscar enlaces a Google Sheets si existen
        sample_pack_dir = os.path.join(DIR_SUITE_03, SUITE_03_PACKS[0]["dir"])
        gs_es = os.path.join(sample_pack_dir, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
        gs_en = os.path.join(sample_pack_dir, "README_GOOGLE_SHEETS_ACCESS.txt")
        if os.path.exists(gs_es):
            zf.write(gs_es, arcname="LEEME_ACCESO_GOOGLE_SHEETS.txt")
        if os.path.exists(gs_en):
            zf.write(gs_en, arcname="README_GOOGLE_SHEETS_ACCESS.txt")

        # Añadir los 5 packs en español e inglés
        for pack in SUITE_03_PACKS:
            pack_base = os.path.join(DIR_SUITE_03, pack["dir"])
            es_folder = os.path.join(pack_base, pack["es_src"])
            en_folder = os.path.join(pack_base, pack["en_src"])

            print(f"  + Empaquetando: {pack['dir']}")

            # Versión Español
            if os.path.exists(es_folder):
                for item in os.listdir(es_folder):
                    src_file = os.path.join(es_folder, item)
                    if os.path.isfile(src_file) and not item.startswith("."):
                        arcname = f"01_VERSION_ESPANOL/{pack['es_dest']}/{item}"
                        zf.write(src_file, arcname=arcname)
            else:
                print(f"  [ERROR] No existe la carpeta {es_folder}")

            # Versión Inglés
            if os.path.exists(en_folder):
                for item in os.listdir(en_folder):
                    src_file = os.path.join(en_folder, item)
                    if os.path.isfile(src_file) and not item.startswith("."):
                        arcname = f"02_ENGLISH_VERSION/{pack['en_dest']}/{item}"
                        zf.write(src_file, arcname=arcname)
            else:
                print(f"  [ERROR] No existe la carpeta {en_folder}")

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"[OK] ZIP Suite 03 generado exitosamente: {size_mb:.2f} MB")

    # Copiar a 00_DISTRIBUCION_LEMONSQUEEZY
    distrib_zip = os.path.join(DIR_DISTRIB, zip_filename)
    shutil.copy2(zip_path, distrib_zip)
    print(f"[OK] Sincronizado en: {distrib_zip}")

    return zip_path


def build_mega_bundle_3_suites():
    """Construye el ZIP del MEGA BUNDLE definitivo con las 3 Suites completas."""
    print("\n" + "=" * 80)
    print("CONSTRUCCION DEL MEGA BUNDLE TOTAL: LAS 3 SUITES (13 DECISION PACKS)")
    print("=" * 80)

    zip_filename = "Executive_Decision_MEGA_BUNDLE_3_Suites_Complete_Dual.zip"
    zip_path = os.path.join(BASE_DIR, zip_filename)

    leeme_mega_es_path = os.path.join(BASE_DIR, "LEEME_MEGA_BUNDLE_3_SUITES.txt")
    readme_mega_en_path = os.path.join(BASE_DIR, "README_MEGA_BUNDLE_3_SUITES.txt")
    with open(leeme_mega_es_path, "w", encoding="utf-8") as f:
        f.write(LEEME_MEGA_BUNDLE_3_SUITES_ES)
    with open(readme_mega_en_path, "w", encoding="utf-8") as f:
        f.write(README_MEGA_BUNDLE_3_SUITES_EN)

    print(f"Generando archivo ZIP Maestro: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Añadir textos de cabecera en la raíz del ZIP
        zf.write(leeme_mega_es_path, arcname="LEEME_MEGA_BUNDLE_3_SUITES.txt")
        zf.write(readme_mega_en_path, arcname="README_MEGA_BUNDLE_3_SUITES.txt")

        # Acceso a Google Sheets
        gs_sample = os.path.join(DIR_SUITE_02, "LEEME_ACCESO_GOOGLE_SHEETS.txt")
        gs_en_sample = os.path.join(DIR_SUITE_02, "README_GOOGLE_SHEETS_ACCESS.txt")
        if os.path.exists(gs_sample):
            zf.write(gs_sample, arcname="LEEME_ACCESO_GOOGLE_SHEETS.txt")
        if os.path.exists(gs_en_sample):
            zf.write(gs_en_sample, arcname="README_GOOGLE_SHEETS_ACCESS.txt")

        # SUITE 01
        print("  + Anadiendo Suite 01: Estrategia Corporativa & MBA (5 packs)...")
        for pack in SUITE_01_PACKS:
            pack_base = os.path.join(DIR_SUITE_01, pack["dir"])
            es_folder = os.path.join(pack_base, pack["es_src"])
            en_folder = os.path.join(pack_base, pack["en_src"])

            if os.path.exists(es_folder):
                for item in os.listdir(es_folder):
                    src_file = os.path.join(es_folder, item)
                    if os.path.isfile(src_file) and not item.startswith("."):
                        arcname = f"01_VERSION_ESPANOL/Suite_01_Estrategia_Corporativa_MBA/{pack['es_dest']}/{item}"
                        zf.write(src_file, arcname=arcname)

            if os.path.exists(en_folder):
                for item in os.listdir(en_folder):
                    src_file = os.path.join(en_folder, item)
                    if os.path.isfile(src_file) and not item.startswith("."):
                        arcname = f"02_ENGLISH_VERSION/Suite_01_Corporate_Strategy_MBA/{pack['en_dest']}/{item}"
                        zf.write(src_file, arcname=arcname)

        # SUITE 02
        print("  + Anadiendo Suite 02: Toma de Decisiones & Priorizacion (3 packs)...")
        for pack in SUITE_02_PACKS:
            pack_base = os.path.join(DIR_SUITE_02, pack["dir"])
            es_folder = os.path.join(pack_base, pack["es_src"])
            en_folder = os.path.join(pack_base, pack["en_src"])

            if os.path.exists(es_folder):
                for item in os.listdir(es_folder):
                    src_file = os.path.join(es_folder, item)
                    if os.path.isfile(src_file) and not item.startswith("."):
                        arcname = f"01_VERSION_ESPANOL/Suite_02_Toma_Decisiones_Priorizacion/{pack['es_dest']}/{item}"
                        zf.write(src_file, arcname=arcname)

            if os.path.exists(en_folder):
                for item in os.listdir(en_folder):
                    src_file = os.path.join(en_folder, item)
                    if os.path.isfile(src_file) and not item.startswith("."):
                        arcname = f"02_ENGLISH_VERSION/Suite_02_Decision_Analysis_Prioritization/{pack['en_dest']}/{item}"
                        zf.write(src_file, arcname=arcname)

        # SUITE 03
        print("  + Anadiendo Suite 03: Control Operativo & PMBOK (5 packs)...")
        for pack in SUITE_03_PACKS:
            pack_base = os.path.join(DIR_SUITE_03, pack["dir"])
            es_folder = os.path.join(pack_base, pack["es_src"])
            en_folder = os.path.join(pack_base, pack["en_src"])

            if os.path.exists(es_folder):
                for item in os.listdir(es_folder):
                    src_file = os.path.join(es_folder, item)
                    if os.path.isfile(src_file) and not item.startswith("."):
                        arcname = f"01_VERSION_ESPANOL/Suite_03_Control_Operativo_PMBOK/{pack['es_dest']}/{item}"
                        zf.write(src_file, arcname=arcname)

            if os.path.exists(en_folder):
                for item in os.listdir(en_folder):
                    src_file = os.path.join(en_folder, item)
                    if os.path.isfile(src_file) and not item.startswith("."):
                        arcname = f"02_ENGLISH_VERSION/Suite_03_Operational_Control_PMBOK/{pack['en_dest']}/{item}"
                        zf.write(src_file, arcname=arcname)

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"[OK] MEGA BUNDLE 3 Suites generado exitosamente: {size_mb:.2f} MB")

    # Copiar a 00_DISTRIBUCION_LEMONSQUEEZY
    distrib_zip = os.path.join(DIR_DISTRIB, zip_filename)
    shutil.copy2(zip_path, distrib_zip)
    print(f"[OK] Sincronizado en: {distrib_zip}")

    return zip_path


def update_catalog():
    """Actualiza CATALOGO_PRODUCTOS_LEMONSQUEEZY.txt con todos los 13 packs y los 4 bundles."""
    catalog_path = os.path.join(DIR_DISTRIB, "CATALOGO_PRODUCTOS_LEMONSQUEEZY.txt")

    catalog_content = """================================================================================
DATALARIA | CATÁLOGO OFICIAL COMPLETO DE PRODUCTOS PARA LEMONSQUEEZY (2026)
================================================================================

Este catálogo detalla la configuración lista para registrar y subir cada producto digital 
en la consola de administración de Lemon Squeezy (https://app.lemonsqueezy.com/products):

--------------------------------------------------------------------------------
SUITE 01 · ESTRATEGIA CORPORATIVA & MBA
--------------------------------------------------------------------------------

PRODUCTO 1: DAFO Cuantitativo & Matriz CAME Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_DAFO_SWOT_Dual.zip
- Precio de venta: 5.00 € (Precio ancla: 19.00 €)
- Slug recomendado: dafo-cuantitativo-came
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/dafo-cuantitativo-came

PRODUCTO 2: 5 Fuerzas de Porter Ponderadas & Atractivo Industrial Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_Porter_5_Forces_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: 5-fuerzas-porter
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/5-fuerzas-porter

PRODUCTO 3: Matriz PESTEL Cuantitativa: Severidad, Volatilidad & Riesgo Macro Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_PESTEL_Dual.zip
- Precio de venta: 5.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-pestel-cuantitativa
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-pestel-cuantitativa

PRODUCTO 4: Matriz BCG Dinámica de Cartera & Asignación de Capital Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_BCG_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-bcg-dinamica
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-bcg-dinamica

PRODUCTO 5: Matriz McKinsey / GE 3x3 & Asignación de Capital Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_McKinsey_GE_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-mckinsey-ge
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-mckinsey-ge

--------------------------------------------------------------------------------
SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN
--------------------------------------------------------------------------------

PRODUCTO 6: Matriz DAR Cuantitativa: Criterios Veto & Ponderación Multicriterio Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_DAR_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 24.00 €)
- Slug recomendado: matriz-dar
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-dar

PRODUCTO 7: Matriz RICE & ICE de Priorización Ágil Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_RICE_ICE_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-rice-ice
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-rice-ice

PRODUCTO 8: Business Case Financiero: VAN, TIR, Payback & Tornado Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_Business_Case_Dual.zip
- Precio de venta: 8.00 € (Precio ancla: 25.00 €)
- Slug recomendado: business-case-financiero
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/business-case-financiero

--------------------------------------------------------------------------------
SUITE 03 · CONTROL OPERATIVO & MÉTRICAS PMBOK
--------------------------------------------------------------------------------

PRODUCTO 9: Matriz RACI Cuantitativa & Balance de Carga Operativa Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_RACI_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: matriz-raci
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-raci

PRODUCTO 10: Matriz de Riesgos & AMFE / FMEA Cuantitativo Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_AMFE_Riesgos_Dual.zip
- Precio de venta: 7.00 € (Precio ancla: 22.00 €)
- Slug recomendado: matriz-riesgos-amfe
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/matriz-riesgos-amfe

PRODUCTO 11: Estimación PERT de 3 Puntos Estocástica Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_PERT_Dual.zip
- Precio de venta: 6.00 € (Precio ancla: 19.00 €)
- Slug recomendado: estimacion-pert
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/estimacion-pert

PRODUCTO 12: Cuadro de Mando EVM: Valor Ganado, Curva S & EAC Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_EVM_Dual.zip
- Precio de venta: 8.00 € (Precio ancla: 25.00 €)
- Slug recomendado: cuadro-mando-evm
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/cuadro-mando-evm

PRODUCTO 13: Calculadora de Stock de Seguridad & ROP (Punto de Pedido) Dual (ES/EN)
- Archivo descargable: Executive_Decision_Pack_Stock_ROP_Dual.zip
- Precio de venta: 7.00 € (Precio ancla: 22.00 €)
- Slug recomendado: stock-seguridad-rop
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/stock-seguridad-rop

================================================================================
COLECCIONES & MEGA BUNDLES (DESCUENTOS POR VOLUMEN)
================================================================================

BUNDLE 01: SUITE 01 · ESTRATEGIA CORPORATIVA & MBA (5 PACKS)
- Nombre: Mega Bundle: Suite 01 · Estrategia Corporativa & MBA Dual (ES/EN)
- Archivo descargable: Executive_Decision_Bundle_Suite_01_Estrategia_MBA_Dual.zip
- Precio de venta: 19.00 € (Precio ancla: 28.00 € | Ahorro: 32%)
- Slug recomendado: suite-01-estrategia-mba
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/suite-01-estrategia-mba
- Contenido: Los 5 packs de estrategia completos (DAFO, Porter, PESTEL, BCG, McKinsey).

BUNDLE 02: SUITE 02 · TOMA DE DECISIONES & PRIORIZACIÓN (3 PACKS)
- Nombre: Mega Bundle: Suite 02 · Toma de Decisiones & Priorización Dual (ES/EN)
- Archivo descargable: Executive_Decision_Bundle_Suite_02_Toma_Decisiones_Dual.zip
- Precio de venta: 15.00 € (Precio ancla: 20.00 € | Ahorro: 25%)
- Slug recomendado: suite-02-toma-decisiones
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/suite-02-toma-decisiones
- Contenido: Los 3 packs de decisión completos (Matriz DAR, RICE/ICE, Business Case).

BUNDLE 03: SUITE 03 · CONTROL OPERATIVO & MÉTRICAS PMBOK (5 PACKS)
- Nombre: Mega Bundle: Suite 03 · Control Operativo & PMBOK Dual (ES/EN)
- Archivo descargable: Executive_Decision_Bundle_Suite_03_Control_Operativo_Dual.zip
- Precio de venta: 22.00 € (Precio ancla: 34.00 € | Ahorro: 35%)
- Slug recomendado: suite-03-control-operativo
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/suite-03-control-operativo
- Contenido: Los 5 packs de operaciones completos (RACI, AMFE, PERT, EVM, Stock ROP).

================================================================================
MEGA BUNDLE COMPLETO: LAS 3 SUITES · 13 EXECUTIVE DECISION PACKS
================================================================================
- Nombre: MEGA BUNDLE: Executive PM & Strategy Suite Dual (13 Packs · ES/EN)
- Archivo descargable: Executive_Decision_MEGA_BUNDLE_3_Suites_Complete_Dual.zip
- Precio de venta: 39.00 € (Precio ancla: 82.00 € | Ahorro: >52%)
- Slug recomendado: mega-bundle-executive-suite
- Checkout URL: https://datalaria.lemonsqueezy.com/buy/mega-bundle-executive-suite
- Contenido Total:
  • Las 3 Suites Completas: Estrategia MBA + Toma de Decisiones + Control Operativo
  • 26 Motores de Cálculo en Excel (.xlsx) y Google Sheets protegidos bajo contraseña
  • 26 Presentaciones Ejecutivas 16:9 en PowerPoint (.pptx) con Board Decision Gateways
  • 26 Guías Metodológicas Editoriales en PDF (.pdf) con demostración matemática y defensa
  • Acceso integral bilingüe en Español e Inglés
================================================================================
"""

    with open(catalog_path, "w", encoding="utf-8") as f:
        f.write(catalog_content)
    print(f"[OK] Catalogo de Lemon Squeezy actualizado en: {catalog_path}")


if __name__ == "__main__":
    print("\nIniciando arquitectura de empaquetado final para Lemon Squeezy...")
    build_suite_03_bundle()
    build_mega_bundle_3_suites()
    update_catalog()
    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO CON EXITO!")
    print("Todos los paquetes (.zip) estan listos en packages/00_DISTRIBUCION_LEMONSQUEEZY/")
    print("=" * 80)
