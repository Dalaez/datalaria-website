#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_excel.py
=================
Genera los modelos oficiales de cálculo en Excel (.xlsx) y Google Sheets:
1. packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE/[ES]_Matriz_RACI_AMFE/Matriz_Riesgos_AMFE_Datalaria_ES.xlsx
2. packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE/[EN]_FMEA_Risk_Matrix/Quantitative_Risk_Matrix_FMEA_EN.xlsx

Arquitectura de 4 Pestañas Funcionales:
- Pestaña 1: Dashboard Ejecutivo / Executive Dashboard
- Pestaña 2: Matriz de Riesgos 5x5 (ISO 31000) / 5x5 Risk Matrix (ISO 31000)
- Pestaña 3: AMFE Operativo (FMEA AIAG-VDA) / Operational FMEA (AIAG-VDA)
- Pestaña 4: Plan de Mitigación & CAPEX / Mitigation Plan & CAPEX

Protección OpenXML ECMA-376 con contraseña "Datalaria2026":
- Celdas de entrada desbloqueadas (locked=False, fondo blanco #FFFFFF).
- Celdas de fórmulas y títulos protegidas (locked=True, fondo #F1F5F9 o corporativo).
- selectUnlockedCells=False y selectLockedCells=False (permite editar celdas desbloqueadas y leer fórmulas).
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.utils import get_column_letter

from protection_policy import (
    PASSWORD_PROTECT, FILL_INPUT, FILL_FORMULA, apply_sheet_protection
)

# Paleta Corporativa Datalaria
C_NAVY_DARK = "0F172A"     # Slate 900
C_NAVY_MED = "1E293B"      # Slate 800
C_BLUE_ACCENT = "2563EB"   # Blue 600
C_BLUE_LIGHT = "EFF6FF"    # Blue 50
C_TEAL_ACCENT = "0D9488"   # Teal 600
C_TEAL_LIGHT = "F0FDFA"    # Teal 50
C_AMBER_ACCENT = "D97706"  # Amber 600
C_AMBER_LIGHT = "FFFBEB"   # Amber 50
C_RED_ACCENT = "DC2626"    # Red 600
C_RED_LIGHT = "FEF2F2"     # Red 50
C_GREEN_ACCENT = "10B981"  # Emerald 500
C_GREEN_LIGHT = "D1FAE5"   # Emerald 100
C_GREEN_TEXT = "065F46"    # Emerald 800
C_AMBER_TEXT = "92400E"    # Amber 800
C_RED_TEXT = "991B1B"      # Red 800
C_GRAY_BG = "F8FAFC"      # Slate 50
C_BORDER = "CBD5E1"       # Slate 300
C_BORDER_LIGHT = "E2E8F0" # Slate 200
C_WHITE = "FFFFFF"

# Fills y Fuentes comunes
FONT_TITLE = Font(name="Segoe UI", size=14, bold=True, color=C_WHITE)
FONT_SUBTITLE = Font(name="Segoe UI", size=9, italic=True, color="94A3B8")
FONT_SEC_HEADER = Font(name="Segoe UI", size=11, bold=True, color=C_WHITE)
FONT_TH = Font(name="Segoe UI", size=9, bold=True, color=C_WHITE)
FONT_TH_DARK = Font(name="Segoe UI", size=9, bold=True, color=C_NAVY_DARK)
FONT_REGULAR = Font(name="Segoe UI", size=9, color="1E293B")
FONT_BOLD = Font(name="Segoe UI", size=9, bold=True, color="0F172A")
FONT_MUTED = Font(name="Segoe UI", size=8, color="64748B")
FONT_KPI_VAL = Font(name="Segoe UI", size=18, bold=True, color=C_NAVY_DARK)
FONT_KPI_VAL_ACCENT = Font(name="Segoe UI", size=18, bold=True, color=C_BLUE_ACCENT)
FONT_KPI_LBL = Font(name="Segoe UI", size=8, bold=True, color="475569")
FONT_KPI_SUB = Font(name="Segoe UI", size=7, italic=True, color="64748B")

FILL_NAVY = PatternFill("solid", fgColor=C_NAVY_DARK)
FILL_NAVY_MED = PatternFill("solid", fgColor=C_NAVY_MED)
FILL_BLUE = PatternFill("solid", fgColor=C_BLUE_ACCENT)
FILL_BLUE_LIGHT = PatternFill("solid", fgColor=C_BLUE_LIGHT)
FILL_TEAL = PatternFill("solid", fgColor=C_TEAL_ACCENT)
FILL_TEAL_LIGHT = PatternFill("solid", fgColor=C_TEAL_LIGHT)
FILL_AMBER = PatternFill("solid", fgColor=C_AMBER_ACCENT)
FILL_AMBER_LIGHT = PatternFill("solid", fgColor=C_AMBER_LIGHT)
FILL_RED_LIGHT = PatternFill("solid", fgColor=C_RED_LIGHT)
FILL_GREEN_LIGHT = PatternFill("solid", fgColor=C_GREEN_LIGHT)
FILL_GRAY = PatternFill("solid", fgColor=C_GRAY_BG)

THIN_SIDE = Side(border_style="thin", color=C_BORDER)
THIN_LIGHT_SIDE = Side(border_style="thin", color=C_BORDER_LIGHT)
BORDER_ALL_THIN = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)
BORDER_CARD = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")


def build_amfe_workbook(lang='ES'):
    wb = openpyxl.Workbook()
    # Sheet names
    if lang == 'ES':
        s1_name = "Dashboard Ejecutivo"
        s2_name = "Matriz de Riesgos 5x5"
        s3_name = "AMFE Operativo"
        s4_name = "Plan Mitigacion & CAPEX"
    else:
        s1_name = "Executive Dashboard"
        s2_name = "5x5 Risk Matrix"
        s3_name = "Operational FMEA"
        s4_name = "Mitigation Plan & CAPEX"

    ws1 = wb.active
    ws1.title = s1_name
    ws2 = wb.create_sheet(title=s2_name)
    ws3 = wb.create_sheet(title=s3_name)
    ws4 = wb.create_sheet(title=s4_name)

    num_fmt_pct = "0,0%" if lang == 'ES' else "0.0%"
    num_fmt_curr = "#,##0.00 €" if lang == 'ES' else "$#,##0.00"
    num_fmt_roi = "0,0x" if lang == 'ES' else "0.0x"
    num_fmt_int = "#,##0"

    # =========================================================================
    # DATOS MAESTROS DE RIESGOS 5x5 (ISO 31000) - PESTAÑA 2
    # =========================================================================
    risks_data_es = [
        ("RIE-01", "Ciberseguridad", "Ataque de ransomware paraliza base de datos transaccional core", 5, 4, "Mitigar", "Copias inmutables, microsegmentación y SOC 24/7", 2, 2, "CISO"),
        ("RIE-02", "Operativo", "Caída prolongada de clúster Cloud principal por fallo de zona", 4, 3, "Mitigar", "Arquitectura multi-región activa-activa en AWS", 2, 2, "Cloud Lead"),
        ("RIE-03", "Cadena Suministro", "Rotura de stock de microcontroladores críticos por tensión geopolítica", 4, 4, "Mitigar", "Dual-sourcing con fabricante europeo y stock buffer", 2, 2, "Dir. Compras"),
        ("RIE-04", "Legal / Compliance", "Sanción de la AEPD / GDPR por brecha de fuga de datos de clientes", 5, 2, "Mitigar", "Cifrado KMS de extremo a extremo y auditoría anual", 2, 1, "DPO / Legal"),
        ("RIE-05", "Financiero", "Fluctuación adversa del tipo de cambio USD/EUR (>12%)", 3, 4, "Transferir", "Contratos de cobertura forward y opciones FX", 1, 3, "CFO"),
        ("RIE-06", "Estratégico", "Entrada de competidor low-cost con subsidio exterior en segmento core", 4, 3, "Aceptar", "Fidelización, aceleración de roadmap de producto y moat", 3, 2, "CEO / Estrategia"),
        ("RIE-07", "Talento", "Fuga masiva de perfiles clave de arquitectura de software y DevOps", 4, 4, "Mitigar", "Plan de retención equity (RSUs), bandas salariales P75", 2, 2, "Chief People"),
        ("RIE-08", "Operativo", "Fallo catastrófico en migración de base de datos relacional a Cloud", 5, 3, "Mitigar", "Despliegues canary, shadow traffic y rollback < 5 min", 2, 1, "Tech Lead"),
        ("RIE-09", "Ciberseguridad", "Robo de credenciales de administrador mediante spear-phishing", 4, 4, "Mitigar", "Autenticación FIDO2 hardware (YubiKey) y Zero Trust", 1, 2, "SecOps Lead"),
        ("RIE-10", "Legal / Compliance", "Cambio regulatorio en directiva de IA (AI Act) que invalida algoritmos", 4, 3, "Mitigar", "Auditoría de explicabilidad de modelos y comités éticos", 2, 2, "Head of AI"),
        ("RIE-11", "Financiero", "Impago de cliente corporativo que representa el 22% del ARR", 4, 2, "Transferir", "Póliza de seguro de crédito y límites de exposición", 2, 1, "Credit Manager"),
        ("RIE-12", "Operativo", "Corrupción silenciosa de datos analíticos en pipeline de ETL", 3, 3, "Mitigar", "Tests de integridad automatizados Great Expectations", 1, 2, "Data Lead"),
        ("RIE-13", "Estratégico", "Retraso superior a 6 meses en lanzamiento de producto insignia", 4, 3, "Mitigar", "Corte de alcance scope-boxing y sprints quincenales", 2, 2, "CPO"),
        ("RIE-14", "Cadena Suministro", "Quiebra imprevista de proveedor logístico exclusivo de última milla", 3, 3, "Mitigar", "Acuerdos marco de respaldo con dos operadores locales", 1, 2, "COO"),
        ("RIE-15", "Ciberseguridad", "Vulnerabilidad Zero-Day en librería Open Source ampliamente usada", 4, 4, "Mitigar", "Escaneo automatizado SBOM y Dependabot diario", 2, 2, "AppSec Lead"),
        ("RIE-16", "Financiero", "Sobrecoste superior al 30% en consumo de infraestructura cloud", 3, 4, "Mitigar", "FinOps, alertas automáticas de gasto y reservas anuales", 1, 2, "FinOps Lead"),
        ("RIE-17", "Operativo", "Interrupción del servicio de pasarela de pagos durante Black Friday", 5, 3, "Mitigar", "Enrutamiento dinámico smart-routing multiaquirente", 2, 1, "Head of Payments"),
        ("RIE-18", "Legal / Compliance", "Litigio por infracción involuntaria de patente de software", 3, 2, "Evitar", "Auditoría de propiedad intelectual previa a releases", 2, 1, "Asesor Jurídico"),
        ("RIE-19", "Talento", "Burnout y absentismo elevado en equipo de soporte técnico L1/L2", 3, 4, "Mitigar", "Implantación de bots de IA para triage y turnos rotativos", 2, 2, "Head of Support"),
        ("RIE-20", "Estratégico", "Rechazo de usuarios a nuevo rediseño de interfaz en aplicación core", 3, 3, "Mitigar", "Test A/B progresivos y programa beta cerrado", 1, 2, "UX Lead"),
    ]

    risks_data_en = [
        ("RSK-01", "Cybersecurity", "Ransomware infection paralyzes core transactional database", 5, 4, "Mitigate", "Immutable backups, microsegmentation and 24/7 MDR SOC", 2, 2, "CISO"),
        ("RSK-02", "Operational", "Prolonged primary cloud cluster outage due to zone failure", 4, 3, "Mitigate", "Active-active multi-region AWS resilient architecture", 2, 2, "Cloud Lead"),
        ("RSK-03", "Supply Chain", "Critical microcontroller supply shortage due to geopolitical friction", 4, 4, "Mitigate", "Dual-sourcing with European fabricator & safety buffer", 2, 2, "Procurement Head"),
        ("RSK-04", "Legal / Compliance", "GDPR data breach enforcement penalty from supervisory authority", 5, 2, "Mitigate", "End-to-end KMS envelope encryption & annual audit", 2, 1, "DPO / General Counsel"),
        ("RSK-05", "Financial", "Adverse USD/EUR foreign exchange rate volatility (>12%)", 3, 4, "Transfer", "FX forward hedging contracts & currency options", 1, 3, "CFO"),
        ("RSK-06", "Strategic", "Aggressive subsidized entry of low-cost international competitor", 4, 3, "Accept", "Customer retention programs & proprietary moat build", 3, 2, "CEO / Strategy"),
        ("RSK-07", "People / Talent", "Key personnel attrition across Core Architecture & DevOps", 4, 4, "Mitigate", "Equity retention pools (RSUs) & P75 compensation band", 2, 2, "Chief People Officer"),
        ("RSK-08", "Operational", "Catastrophic database corruption during cloud migration cutover", 5, 3, "Mitigate", "Canary deployment, shadow traffic & <5min automated rollback", 2, 1, "Tech Lead"),
        ("RSK-09", "Cybersecurity", "Privileged administrative credential theft via targeted spear-phishing", 4, 4, "Mitigate", "Hardware FIDO2 keys (YubiKey) & Zero Trust architecture", 1, 2, "SecOps Lead"),
        ("RSK-10", "Legal / Compliance", "EU AI Act regulatory compliance breach forcing model deprecation", 4, 3, "Mitigate", "Algorithmic explainability audit & AI governance board", 2, 2, "Head of AI"),
        ("RSK-11", "Financial", "Default of enterprise tier-1 client accounting for 22% of ARR", 4, 2, "Transfer", "Credit risk insurance policy & strict credit exposure caps", 2, 1, "Credit Manager"),
        ("RSK-12", "Operational", "Silent analytical data drift and ETL pipeline corruption", 3, 3, "Mitigate", "Automated data contracts & Great Expectations unit tests", 1, 2, "Data Lead"),
        ("RSK-13", "Strategic", "Over 6-month launch schedule slip for core enterprise flagship product", 4, 3, "Mitigate", "Scope-boxing discipline & bi-weekly agile release cadences", 2, 2, "CPO"),
        ("RSK-14", "Supply Chain", "Sudden insolvency of single-source last-mile logistics provider", 3, 3, "Mitigate", "Standby master services agreements with secondary carriers", 1, 2, "COO"),
        ("RSK-15", "Cybersecurity", "Critical zero-day vulnerability discovered in core open-source dependency", 4, 4, "Mitigate", "Automated daily SBOM scanning & Dependabot pipeline gating", 2, 2, "AppSec Lead"),
        ("RSK-16", "Financial", "Uncontrolled cloud infrastructure cost overrun exceeding 30%", 3, 4, "Mitigate", "FinOps practice, automated budget alerts & compute savings plans", 1, 2, "FinOps Lead"),
        ("RSK-17", "Operational", "Payment gateway outage during peak Black Friday sales window", 5, 3, "Mitigate", "Dynamic multi-acquirer smart routing failover engine", 2, 1, "Head of Payments"),
        ("RSK-18", "Legal / Compliance", "Inadvertent third-party software patent infringement litigation", 3, 2, "Avoid", "Comprehensive IP clearance audit prior to GA release", 2, 1, "Legal Counsel"),
        ("RSK-19", "People / Talent", "Severe support engineer burnout leading to acute attrition in L1/L2", 3, 4, "Mitigate", "AI-assisted automated triage bots & shift rotation balance", 2, 2, "Head of Support"),
        ("RSK-20", "Strategic", "User pushback and churn spike following core UI/UX redesign", 3, 3, "Mitigate", "Phased cohort A/B rollout & closed enterprise beta program", 1, 2, "UX Lead"),
    ]

    risks_data = risks_data_es if lang == 'ES' else risks_data_en

    # =========================================================================
    # DATOS MAESTROS DE AMFE / FMEA (AIAG-VDA) - PESTAÑA 3
    # =========================================================================
    fmea_data_es = [
        ("FMEA-01", "Pasarela de Pagos", "Fallo de comunicación con adquirente bancario", "Rechazo de transacciones y pérdida de ventas", "Timeout de red en endpoint externo", "Reintentos automáticos simples", "Monitor de salud con ping cada 5 min", 8, 6, 7, "Implementar fallback automático a adquirente secundario", "Lead Payments", "Q1", 8, 2, 3),
        ("FMEA-02", "Almacenamiento Cloud", "Pérdida o corrupción de datos transaccionales", "Incapacidad de operar, daño reputacional severo", "Error humano en script de base de datos", "Revisión manual de scripts", "Alertas tras fallos de queries", 9, 5, 8, "Backups inmutables WORM y pipeline CI/CD con validación", "Database Admin", "Q1", 9, 2, 2),
        ("FMEA-03", "Control de Accesos", "Autenticación indebida de terceros maliciosos", "Fuga masiva de datos y secuestro de cuentas", "Ataque de fuerza bruta y credential stuffing", "Límite de 5 intentos por IP", "Logs analizados al final del día", 9, 7, 7, "MFA obligatorio, captcha adaptativo y WAF con rate-limiting", "CISO", "Q2", 9, 2, 2),
        ("FMEA-04", "Balanceador Carga", "Saturación de memoria por pico de tráfico", "Denegación de servicio (503 Service Unavailable)", "Fuga de memoria en proxy inverso", "Monitor de CPU básico", "Notificación cuando uso de RAM > 95%", 8, 6, 6, "Auto-scaling horizontal con reinicios preventivos canary", "DevOps Lead", "Q2", 8, 2, 3),
        ("FMEA-05", "Pipeline CI/CD", "Despliegue a producción con bug bloqueante", "Regresión crítica que inutiliza el checkout", "Tests unitarios incompletos en release", "Suite de tests locales sin obligatoriedad", "Test manual por QA antes del merge", 8, 6, 6, "Cobertura mínima 85% obligatoria en GitHub Actions y staging", "QA Lead", "Q1", 8, 2, 3),
        ("FMEA-06", "Cola Mensajería", "Acumulación descontrolada de eventos (lag)", "Retrasos de horas en procesamiento de pedidos", "Consumidores bloqueados por fallo de red", "Dead-letter queue básica", "Revisión diaria de colas por operadores", 7, 6, 7, "Escalado dinámico de pods consumidores y alertas PagerDuty", "Backend Lead", "Q2", 7, 2, 3),
        ("FMEA-07", "Línea Ensamblaje", "Desalineación de cabezal robótico en soldadura", "Piezas defectuosas con resistencia estructural baja", "Desgaste mecánico prematuro de servo", "Mantenimiento correctivo periódico", "Inspección visual humana al final de línea", 9, 5, 8, "Mantenimiento predictivo IoT con vibración y visión artificial", "Ingeniero Planta", "Q2", 9, 2, 2),
        ("FMEA-08", "Control Térmico", "Sobrecalentamiento en hornos de polimerizado", "Deformación del polímero y lote inservible", "Fallo de termopar o relé de estado sólido", "Sensor redundante simple", "Alarma sonora local en planta", 8, 5, 7, "Controlador PID digital doble con corte automático y telemetría", "Mantenimiento Lead", "Q3", 8, 2, 3),
        ("FMEA-09", "Servicio DNS", "Resolución fallida de nombres de dominio core", "Sitio web totalmente inaccesible a nivel global", "Ataque DDoS sobre servidores autoritativos", "Anycast básico de proveedor único", "Monitor externo ping cada 10 min", 8, 5, 7, "Arquitectura Dual-DNS con dos proveedores independientes", "NetOps Lead", "Q1", 8, 1, 2),
        ("FMEA-10", "Almacén Logístico", "Error de picking y envío de referencia errónea", "Devoluciones, sobrecoste de transporte y quejas", "Código de barras dañado o lectura manual", "Escaneo óptico de pistola básico", "Comprobación visual de albarán", 6, 7, 6, "Validación por pesaje automatizado en báscula de báscula dinámica", "Jefe Logística", "Q3", 6, 2, 2),
        ("FMEA-11", "Certificados SSL", "Expiración inadvertida de certificado HTTPS", "Bloqueo por navegadores y pánico de clientes", "Falta de renovación automática en servidor", "Calendario compartido de expiración", "Aviso por correo 15 días antes", 8, 5, 6, "Automatización con Let's Encrypt / Certbot y monitor cert-checker", "SecOps Lead", "Q1", 8, 1, 1),
        ("FMEA-12", "Motor de Búsqueda", "Desincronización de índices con catálogo", "Resultados vacíos de productos disponibles", "Fallo silencioso en webhooks de actualización", "Reindexado manual nocturno", "Detección cuando clientes reportan incidencias", 7, 6, 8, "Validación de recuentos de inventario con reconciliación por hora", "Search Engineer", "Q2", 7, 2, 3),
        ("FMEA-13", "Inyección Plástico", "Burbujas y porosidad en carcasa inyectada", "Fractura prematura de la pieza ante impactos", "Humedad residual en granza plástica", "Secado por tiempo estándar", "Muestreo destructivo 1 cada 500 piezas", 7, 6, 7, "Sensor de punto de rocío en tolva y control de deshumidificación", "Ingeniero Calidad", "Q2", 7, 2, 2),
        ("FMEA-14", "Gestión de Sesión", "Fuga de token JWT en local storage de cliente", "Suplantación de identidad de sesión activa", "XSS en entrada de comentarios no saneada", "Sanitización básica HTML", "Análisis SAST trimestral", 8, 5, 7, "Cookies HttpOnly / SameSite=Strict y CSP estricto", "AppSec Lead", "Q1", 8, 2, 2),
        ("FMEA-15", "Refrigeración Server", "Fuga de líquido refrigerante en rack de alta densidad", "Cortocircuito y parada de emergencia de servidores", "Fatiga en racores de acoplamiento rápido", "Inspección visual quincenal", "Sensor de humedad en falso suelo", 9, 4, 8, "Cables sensores de fuga de líquido por conductividad en cada rack", "Data Center Mgr", "Q3", 9, 1, 2),
    ]

    fmea_data_en = [
        ("FMEA-01", "Payment Gateway", "Communication failure with bank acquirer", "Transaction rejection and direct revenue loss", "Network timeout on third-party endpoint", "Basic synchronous retry logic", "Healthcheck ping polling every 5 min", 8, 6, 7, "Deploy multi-acquirer smart routing automated failover", "Lead Payments", "Q1", 8, 2, 3),
        ("FMEA-02", "Cloud Storage", "Transactional database corruption or data loss", "Service outage, severe brand & regulatory damage", "Human operational error in migration scripts", "Manual peer review of migration scripts", "Post-failure alert when SQL query errors trigger", 9, 5, 8, "WORM immutable backups & automated CI/CD schema sandbox testing", "Database Admin", "Q1", 9, 2, 2),
        ("FMEA-03", "Access Control", "Unauthorized privileged login by threat actor", "Mass customer data exfiltration & account takeover", "Credential stuffing & distributed brute force", "5-attempt IP rate limiting", "Batch log audit analyzed at end of business day", 9, 7, 7, "Mandatory MFA hardware tokens, adaptive CAPTCHA & WAF defense", "CISO", "Q2", 9, 2, 2),
        ("FMEA-04", "Load Balancer", "Memory exhaustion under sudden traffic surge", "Denial of service (503 Service Unavailable HTTP)", "Memory leak in reverse proxy ingress process", "Standard host CPU monitoring", "Notification triggered when RAM exceeds 95%", 8, 6, 6, "Horizontal autoscaling with automated canary health restarts", "DevOps Lead", "Q2", 8, 2, 3),
        ("FMEA-05", "CI/CD Pipeline", "Production deployment containing critical blocker", "Catastrophic regression breaking customer checkout", "Incomplete unit and integration test coverage", "Optional local test suite execution", "Manual sanity QA pass prior to branch merge", 8, 6, 6, "Mandatory 85% coverage gate enforced in GitHub Actions & staging", "QA Lead", "Q1", 8, 2, 3),
        ("FMEA-06", "Message Broker", "Uncontrolled message queue backlog and consumer lag", "Multi-hour delays processing customer orders", "Consumer threads deadlocked on network I/O", "Default dead-letter queue", "Daily manual inspection of queue depths by ops", 7, 6, 7, "Dynamic consumer pod autoscaling & PagerDuty latency alerts", "Backend Lead", "Q2", 7, 2, 3),
        ("FMEA-07", "Assembly Line", "Robotic weld head mechanical misalignment", "Defective structural joints with low shear tolerance", "Premature mechanical wear on drive servo motor", "Periodic corrective maintenance intervals", "Human visual inspection at end of production line", 9, 5, 8, "IoT predictive vibration monitoring & automated computer vision", "Plant Engineer", "Q2", 9, 2, 2),
        ("FMEA-08", "Thermal Control", "Overtemperature spike in industrial curing ovens", "Polymer warping and complete batch scrap", "Thermocouple drift or solid-state relay failure", "Single standard sensor loop", "Local plant audible alarm bell", 8, 5, 7, "Dual digital PID controller with auto-cutoff & cloud telemetry", "Maintenance Lead", "Q3", 8, 2, 3),
        ("FMEA-09", "DNS Resolution", "Resolution outage for core authoritative apex domains", "Global web application completely unreachable", "Targeted distributed denial-of-service (DDoS)", "Single Anycast provider footprint", "External HTTP synthetic ping every 10 min", 8, 5, 7, "Dual-DNS architecture deployed across two independent carriers", "NetOps Lead", "Q1", 8, 1, 2),
        ("FMEA-10", "Warehouse Ops", "Incorrect SKU picked and dispatched to customer", "High return logistics costs and buyer churn", "Damaged barcode or manual handheld input error", "Standard handheld optical scanner", "Visual packing slip verification", 6, 7, 6, "Automated conveyor inline checkweigher validation before ship", "Logistics Head", "Q3", 6, 2, 2),
        ("FMEA-11", "SSL Certificates", "Inadvertent expiration of TLS/HTTPS certificate", "Browser security warning blocking all web traffic", "Omission in manual renewal calendar tracking", "Shared calendar reminder", "Email notification sent 15 days before expiry", 8, 5, 6, "Automated ACME / Let's Encrypt renewal with multi-region cert-check", "SecOps Lead", "Q1", 8, 1, 1),
        ("FMEA-12", "Search Engine", "Search index drift and catalog desynchronization", "Empty search results for high-demand inventory items", "Silent failure in inventory ingestion webhooks", "Nightly scheduled batch reindexing", "Reactive detection when customer support receives calls", 7, 6, 8, "Real-time inventory contract validation & hourly reconciliation", "Search Engineer", "Q2", 7, 2, 3),
        ("FMEA-13", "Plastic Injection", "Trapped moisture causing cosmetic bubbles and voids", "Premature part brittle failure under load impact", "Residual moisture in raw polymer resin pellets", "Fixed-time standard drying cycle", "Destructive QA testing 1 per 500 unit batch", 7, 6, 7, "Real-time dew-point monitoring sensors in drying hoppers", "Quality Engineer", "Q2", 7, 2, 2),
        ("FMEA-14", "Session Mgmt", "JWT authorization token leak via client local storage", "Active user session hijacking and fraud", "Stored cross-site scripting (XSS) vulnerability", "Basic input sanitation library", "Quarterly static code analysis (SAST)", 8, 5, 7, "HttpOnly / SameSite=Strict cookies with strict CSP headers", "AppSec Lead", "Q1", 8, 2, 2),
        ("FMEA-15", "Data Center Cooling", "Liquid coolant leak inside high-density compute rack", "Electrical short-circuit and emergency shutdown", "Mechanical fatigue on quick-disconnect couplings", "Bi-weekly visual inspection", "Standard subfloor moisture detector", 9, 4, 8, "Per-rack conductive rope leak sensing with automatic valve isolation", "Data Center Mgr", "Q3", 9, 1, 2),
    ]

    fmea_data = fmea_data_es if lang == 'ES' else fmea_data_en

    # =========================================================================
    # DATOS MAESTROS DE PLAN DE MITIGACIÓN & CAPEX - PESTAÑA 4
    # =========================================================================
    capex_data_es = [
        ("MIT-01", "RIE-01 / FMEA-03", "Despliegue de Arquitectura Zero Trust y Llaves FIDO2", "CISO", 38000, 240000, 36000, "Q1", "En Curso"),
        ("MIT-02", "RIE-02 / FMEA-04", "Infraestructura Multi-Región Activa-Activa en AWS", "Cloud Lead", 65000, 320000, 48000, "Q1-Q2", "En Curso"),
        ("MIT-03", "RIE-03", "Estrategia Dual-Sourcing y Stock de Seguridad Estratégico", "Dir. Compras", 45000, 180000, 30000, "Q2", "Planificado"),
        ("MIT-04", "RIE-04 / FMEA-14", "Cifrado Envelope KMS, Blindaje GDPR y CSP Estricto", "DPO / Legal", 25000, 200000, 20000, "Q1", "Completado"),
        ("MIT-05", "RIE-05", "Programa de Coberturas Financieras FX Forward (Hedging)", "CFO", 18000, 110000, 15000, "Q1", "Completado"),
        ("MIT-06", "RIE-08 / FMEA-02", "Plataforma de Backups Inmutables WORM y CI/CD Canary", "Tech Lead", 42000, 280000, 35000, "Q1-Q2", "En Curso"),
        ("MIT-07", "RIE-17 / FMEA-01", "Enrutamiento Dinámico Smart-Routing Multiaquirente", "Head Payments", 28000, 190000, 25000, "Q1", "Completado"),
        ("MIT-08", "FMEA-07", "Sistema de Visión Artificial y Mantenimiento Predictivo IoT", "Ing. Planta", 52000, 260000, 38000, "Q2-Q3", "Planificado"),
        ("MIT-09", "FMEA-09", "Despliegue de Redundancia Dual-DNS Global Independiente", "NetOps Lead", 15000, 140000, 12000, "Q1", "Completado"),
        ("MIT-10", "FMEA-15", "Detección Inteligente de Fugas de Refrigerante por Rack", "Data Center Mgr", 32000, 210000, 28000, "Q3", "Planificado"),
    ]

    capex_data_en = [
        ("MIT-01", "RSK-01 / FMEA-03", "Deploy Zero Trust Architecture & FIDO2 Hardware Keys", "CISO", 38000, 240000, 36000, "Q1", "In Progress"),
        ("MIT-02", "RSK-02 / FMEA-04", "Active-Active Multi-Region AWS Resilient Cloud Footprint", "Cloud Lead", 65000, 320000, 48000, "Q1-Q2", "In Progress"),
        ("MIT-03", "RSK-03", "Dual-Sourcing Supply Contracts & Strategic Safety Buffer", "Procurement Head", 45000, 180000, 30000, "Q2", "Planned"),
        ("MIT-04", "RSK-04 / FMEA-14", "KMS Envelope Encryption, GDPR Hardening & Strict CSP", "DPO / Legal", 25000, 200000, 20000, "Q1", "Completed"),
        ("MIT-05", "RSK-05", "FX Forward Hedging Framework & Currency Risk Treasury", "CFO", 18000, 110000, 15000, "Q1", "Completed"),
        ("MIT-06", "RSK-08 / FMEA-02", "WORM Immutable Storage Engine & Canary CI/CD Gating", "Tech Lead", 42000, 280000, 35000, "Q1-Q2", "In Progress"),
        ("MIT-07", "RSK-17 / FMEA-01", "Multi-Acquirer Dynamic Smart Routing Engine", "Head Payments", 28000, 190000, 25000, "Q1", "Completed"),
        ("MIT-08", "FMEA-07", "Computer Vision Quality Inspection & IoT Predictive Maintenance", "Plant Engineer", 52000, 260000, 38000, "Q2-Q3", "Planned"),
        ("MIT-09", "FMEA-09", "Independent Dual-DNS Global Resiliency Deployment", "NetOps Lead", 15000, 140000, 12000, "Q1", "Completed"),
        ("MIT-10", "FMEA-15", "Conductive Per-Rack Coolant Leak Sensing & Isolation", "Data Center Mgr", 32000, 210000, 28000, "Q3", "Planned"),
    ]

    capex_data = capex_data_es if lang == 'ES' else capex_data_en

    # =========================================================================
    # CONSTRUCCIÓN PESTAÑA 2: MATRIZ DE RIESGOS 5x5 (ISO 31000)
    # =========================================================================
    ws2.views.sheetView[0].showGridLines = True
    # Header Banner
    ws2.merge_cells("B2:N2")
    ws2["B2"] = ("DATALARIA | MATRIZ DE RIESGOS 5x5 (ESTÁNDAR ISO 31000 / COSO ERM)"
                 if lang == 'ES' else
                 "DATALARIA | 5x5 QUANTITATIVE RISK MATRIX (ISO 31000 / COSO ERM STANDARD)")
    ws2["B2"].font = FONT_TITLE
    ws2["B2"].fill = FILL_NAVY
    ws2["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws2.row_dimensions[2].height = 28

    ws2.merge_cells("B3:N3")
    ws2["B3"] = ("Registro estructurado de riesgos corporativos con evaluación de impacto inherente y residual post-mitigación"
                 if lang == 'ES' else
                 "Corporate risk registry with inherent and residual risk scoring post-mitigation strategy")
    ws2["B3"].font = FONT_SUBTITLE
    ws2["B3"].fill = FILL_NAVY
    ws2["B3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws2.row_dimensions[3].height = 18

    # Table Headers
    headers_ws2_es = [
        ("B5", "ID", 10),
        ("C5", "Categoría", 18),
        ("D5", "Descripción del Riesgo Corporativo", 38),
        ("E5", "Impacto (I)\n[1-5]", 12),
        ("F5", "Probabilidad (P)\n[1-5]", 14),
        ("G5", "Puntuación\nInherente", 12),
        ("H5", "Nivel\nInherente", 12),
        ("I5", "Estrategia de\nRespuesta", 14),
        ("J5", "Medidas de Mitigación / Plan de Contingencia", 42),
        ("K5", "Impacto (I)\nResidual", 12),
        ("L5", "Probabilidad (P)\nResidual", 14),
        ("M5", "Puntuación\nResidual", 12),
        ("N5", "Dueño del Riesgo\n(Risk Owner)", 18),
    ]

    headers_ws2_en = [
        ("B5", "ID", 10),
        ("C5", "Category", 18),
        ("D5", "Corporate Risk Description", 38),
        ("E5", "Impact (I)\n[1-5]", 12),
        ("F5", "Probability (P)\n[1-5]", 14),
        ("G5", "Inherent\nScore", 12),
        ("H5", "Inherent\nLevel", 12),
        ("I5", "Response\nStrategy", 14),
        ("J5", "Mitigation Actions / Contingency Plan", 42),
        ("K5", "Residual (I)\nImpact", 12),
        ("L5", "Residual (P)\nProbability", 14),
        ("M5", "Residual\nScore", 12),
        ("N5", "Risk Owner", 18),
    ]

    headers_ws2 = headers_ws2_es if lang == 'ES' else headers_ws2_en
    ws2.row_dimensions[5].height = 28

    for cell_ref, text, width in headers_ws2:
        cell = ws2[cell_ref]
        cell.value = text
        cell.font = FONT_TH
        cell.fill = FILL_NAVY_MED
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL_THIN
        col_letter = cell_ref[0]
        ws2.column_dimensions[col_letter].width = width

    input_cells_ws2 = []
    formula_cells_ws2 = []

    start_row_ws2 = 6
    for idx, r in enumerate(risks_data):
        row = start_row_ws2 + idx
        ws2.row_dimensions[row].height = 22

        # ID
        c_id = ws2[f"B{row}"]
        c_id.value = r[0]
        c_id.font = FONT_BOLD
        c_id.alignment = ALIGN_CENTER
        c_id.border = BORDER_ALL_THIN
        c_id.fill = FILL_GRAY

        # Categoría
        c_cat = ws2[f"C{row}"]
        c_cat.value = r[1]
        c_cat.font = FONT_REGULAR
        c_cat.alignment = ALIGN_CENTER
        c_cat.border = BORDER_ALL_THIN
        input_cells_ws2.append(f"C{row}")

        # Descripción
        c_desc = ws2[f"D{row}"]
        c_desc.value = r[2]
        c_desc.font = FONT_REGULAR
        c_desc.alignment = ALIGN_LEFT
        c_desc.border = BORDER_ALL_THIN
        input_cells_ws2.append(f"D{row}")

        # Impacto Inherente (1-5)
        c_i = ws2[f"E{row}"]
        c_i.value = r[3]
        c_i.font = FONT_BOLD
        c_i.alignment = ALIGN_CENTER
        c_i.border = BORDER_ALL_THIN
        c_i.number_format = num_fmt_int
        input_cells_ws2.append(f"E{row}")

        # Probabilidad Inherente (1-5)
        c_p = ws2[f"F{row}"]
        c_p.value = r[4]
        c_p.font = FONT_BOLD
        c_p.alignment = ALIGN_CENTER
        c_p.border = BORDER_ALL_THIN
        c_p.number_format = num_fmt_int
        input_cells_ws2.append(f"F{row}")

        # Puntuación Inherente: =E * F
        c_sc = ws2[f"G{row}"]
        c_sc.value = f"=E{row}*F{row}"
        c_sc.font = FONT_BOLD
        c_sc.alignment = ALIGN_CENTER
        c_sc.border = BORDER_ALL_THIN
        c_sc.fill = FILL_FORMULA
        c_sc.number_format = num_fmt_int
        formula_cells_ws2.append(f"G{row}")

        # Nivel Inherente
        c_niv = ws2[f"H{row}"]
        if lang == 'ES':
            c_niv.value = f'=IF(G{row}>=15,"Crítico",IF(G{row}>=8,"Medio","Bajo"))'
        else:
            c_niv.value = f'=IF(G{row}>=15,"Critical",IF(G{row}>=8,"Medium","Low"))'
        c_niv.font = FONT_BOLD
        c_niv.alignment = ALIGN_CENTER
        c_niv.border = BORDER_ALL_THIN
        c_niv.fill = FILL_FORMULA
        formula_cells_ws2.append(f"H{row}")

        # Estrategia
        c_strat = ws2[f"I{row}"]
        c_strat.value = r[5]
        c_strat.font = FONT_REGULAR
        c_strat.alignment = ALIGN_CENTER
        c_strat.border = BORDER_ALL_THIN
        input_cells_ws2.append(f"I{row}")

        # Medidas
        c_med = ws2[f"J{row}"]
        c_med.value = r[6]
        c_med.font = FONT_REGULAR
        c_med.alignment = ALIGN_LEFT
        c_med.border = BORDER_ALL_THIN
        input_cells_ws2.append(f"J{row}")

        # Impacto Residual
        c_ir = ws2[f"K{row}"]
        c_ir.value = r[7]
        c_ir.font = FONT_BOLD
        c_ir.alignment = ALIGN_CENTER
        c_ir.border = BORDER_ALL_THIN
        c_ir.number_format = num_fmt_int
        input_cells_ws2.append(f"K{row}")

        # Probabilidad Residual
        c_pr = ws2[f"L{row}"]
        c_pr.value = r[8]
        c_pr.font = FONT_BOLD
        c_pr.alignment = ALIGN_CENTER
        c_pr.border = BORDER_ALL_THIN
        c_pr.number_format = num_fmt_int
        input_cells_ws2.append(f"L{row}")

        # Puntuación Residual: =K * L
        c_scr = ws2[f"M{row}"]
        c_scr.value = f"=K{row}*L{row}"
        c_scr.font = FONT_BOLD
        c_scr.alignment = ALIGN_CENTER
        c_scr.border = BORDER_ALL_THIN
        c_scr.fill = FILL_FORMULA
        c_scr.number_format = num_fmt_int
        formula_cells_ws2.append(f"M{row}")

        # Risk Owner
        c_own = ws2[f"N{row}"]
        c_own.value = r[9]
        c_own.font = FONT_REGULAR
        c_own.alignment = ALIGN_CENTER
        c_own.border = BORDER_ALL_THIN
        input_cells_ws2.append(f"N{row}")

    end_row_ws2 = start_row_ws2 + len(risks_data) - 1

    # Formato condicional para Nivel Inherente en Pestaña 2
    red_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    red_font = Font(name="Segoe UI", size=9, bold=True, color="991B1B")
    amber_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    amber_font = Font(name="Segoe UI", size=9, bold=True, color="92400E")
    green_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    green_font = Font(name="Segoe UI", size=9, bold=True, color="065F46")

    crit_val = '"Crítico"' if lang == 'ES' else '"Critical"'
    med_val = '"Medio"' if lang == 'ES' else '"Medium"'
    low_val = '"Bajo"' if lang == 'ES' else '"Low"'

    ws2.conditional_formatting.add(f"H6:H{end_row_ws2}", CellIsRule(operator="equal", formula=[crit_val], fill=red_fill, font=red_font))
    ws2.conditional_formatting.add(f"H6:H{end_row_ws2}", CellIsRule(operator="equal", formula=[med_val], fill=amber_fill, font=amber_font))
    ws2.conditional_formatting.add(f"H6:H{end_row_ws2}", CellIsRule(operator="equal", formula=[low_val], fill=green_fill, font=green_font))

    # =========================================================================
    # CONSTRUCCIÓN PESTAÑA 3: AMFE OPERATIVO (AIAG-VDA)
    # =========================================================================
    ws3.views.sheetView[0].showGridLines = True
    ws3.merge_cells("B2:U2")
    ws3["B2"] = ("DATALARIA | ANÁLISIS DE MODOS DE FALLO Y EFECTOS (AMFE / FMEA AIAG-VDA)"
                 if lang == 'ES' else
                 "DATALARIA | FAILURE MODE AND EFFECTS ANALYSIS (OPERATIONAL FMEA AIAG-VDA)")
    ws3["B2"].font = FONT_TITLE
    ws3["B2"].fill = FILL_NAVY
    ws3["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws3.row_dimensions[2].height = 28

    ws3.merge_cells("B3:U3")
    ws3["B3"] = ("Cuantificación tridimensional de fallos de proceso: Severidad (S) x Ocurrencia (O) x Detección (D) = NPR (1-1000)"
                 if lang == 'ES' else
                 "Three-dimensional process failure quantification: Severity (S) x Occurrence (O) x Detection (D) = RPN (1-1000)")
    ws3["B3"].font = FONT_SUBTITLE
    ws3["B3"].fill = FILL_NAVY
    ws3["B3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws3.row_dimensions[3].height = 18

    headers_ws3_es = [
        ("B5", "ID", 10),
        ("C5", "Proceso /\nComponente", 18),
        ("D5", "Modo Potencial de Fallo", 30),
        ("E5", "Efecto Potencial del Fallo", 32),
        ("F5", "Causa Raíz Potencial", 30),
        ("G5", "Controles Actuales\n(Prevención)", 24),
        ("H5", "Controles Actuales\n(Detección)", 24),
        ("I5", "Sev (S)\n[1-10]", 9),
        ("J5", "Ocu (O)\n[1-10]", 9),
        ("K5", "Det (D)\n[1-10]", 9),
        ("L5", "NPR\nInherente", 11),
        ("M5", "Prioridad\nAcción (AP)", 12),
        ("N5", "Plan de Acción Recomendado", 36),
        ("O5", "Responsable", 16),
        ("P5", "Plazo", 10),
        ("Q5", "Sev (S)\nResidual", 9),
        ("R5", "Ocu (O)\nResidual", 9),
        ("S5", "Det (D)\nResidual", 9),
        ("T5", "NPR\nResidual", 11),
        ("U5", "% Reducción\nde Riesgo", 13),
    ]

    headers_ws3_en = [
        ("B5", "ID", 10),
        ("C5", "Process /\nComponent", 18),
        ("D5", "Potential Failure Mode", 30),
        ("E5", "Potential Effect of Failure", 32),
        ("F5", "Potential Root Cause", 30),
        ("G5", "Current Controls\n(Prevention)", 24),
        ("H5", "Current Controls\n(Detection)", 24),
        ("I5", "Sev (S)\n[1-10]", 9),
        ("J5", "Occ (O)\n[1-10]", 9),
        ("K5", "Det (D)\n[1-10]", 9),
        ("L5", "Inherent\nRPN", 11),
        ("M5", "Action\nPriority (AP)", 12),
        ("N5", "Recommended Action Plan", 36),
        ("O5", "Owner", 16),
        ("P5", "Target Date", 10),
        ("Q5", "Sev (S)\nResidual", 9),
        ("R5", "Occ (O)\nResidual", 9),
        ("S5", "Det (D)\nResidual", 9),
        ("T5", "Residual\nRPN", 11),
        ("U5", "Risk Reduction\nPercentage", 13),
    ]

    headers_ws3 = headers_ws3_es if lang == 'ES' else headers_ws3_en
    ws3.row_dimensions[5].height = 28

    for cell_ref, text, width in headers_ws3:
        cell = ws3[cell_ref]
        cell.value = text
        cell.font = FONT_TH
        cell.fill = FILL_NAVY_MED
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL_THIN
        # Extract column letters from cell_ref
        col_letter = "".join([c for c in cell_ref if c.isalpha()])
        ws3.column_dimensions[col_letter].width = width

    input_cells_ws3 = []
    formula_cells_ws3 = []

    start_row_ws3 = 6
    for idx, f in enumerate(fmea_data):
        row = start_row_ws3 + idx
        ws3.row_dimensions[row].height = 22

        # ID
        ws3[f"B{row}"] = f[0]
        ws3[f"B{row}"].font = FONT_BOLD
        ws3[f"B{row}"].alignment = ALIGN_CENTER
        ws3[f"B{row}"].border = BORDER_ALL_THIN
        ws3[f"B{row}"].fill = FILL_GRAY

        # Componente
        ws3[f"C{row}"] = f[1]
        ws3[f"C{row}"].font = FONT_REGULAR
        ws3[f"C{row}"].alignment = ALIGN_CENTER
        ws3[f"C{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"C{row}")

        # Modo de fallo
        ws3[f"D{row}"] = f[2]
        ws3[f"D{row}"].font = FONT_REGULAR
        ws3[f"D{row}"].alignment = ALIGN_LEFT
        ws3[f"D{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"D{row}")

        # Efecto
        ws3[f"E{row}"] = f[3]
        ws3[f"E{row}"].font = FONT_REGULAR
        ws3[f"E{row}"].alignment = ALIGN_LEFT
        ws3[f"E{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"E{row}")

        # Causa
        ws3[f"F{row}"] = f[4]
        ws3[f"F{row}"].font = FONT_REGULAR
        ws3[f"F{row}"].alignment = ALIGN_LEFT
        ws3[f"F{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"F{row}")

        # Control Prevención
        ws3[f"G{row}"] = f[5]
        ws3[f"G{row}"].font = FONT_REGULAR
        ws3[f"G{row}"].alignment = ALIGN_LEFT
        ws3[f"G{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"G{row}")

        # Control Detección
        ws3[f"H{row}"] = f[6]
        ws3[f"H{row}"].font = FONT_REGULAR
        ws3[f"H{row}"].alignment = ALIGN_LEFT
        ws3[f"H{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"H{row}")

        # S (1-10)
        ws3[f"I{row}"] = f[7]
        ws3[f"I{row}"].font = FONT_BOLD
        ws3[f"I{row}"].alignment = ALIGN_CENTER
        ws3[f"I{row}"].border = BORDER_ALL_THIN
        ws3[f"I{row}"].number_format = num_fmt_int
        input_cells_ws3.append(f"I{row}")

        # O (1-10)
        ws3[f"J{row}"] = f[8]
        ws3[f"J{row}"].font = FONT_BOLD
        ws3[f"J{row}"].alignment = ALIGN_CENTER
        ws3[f"J{row}"].border = BORDER_ALL_THIN
        ws3[f"J{row}"].number_format = num_fmt_int
        input_cells_ws3.append(f"J{row}")

        # D (1-10)
        ws3[f"K{row}"] = f[9]
        ws3[f"K{row}"].font = FONT_BOLD
        ws3[f"K{row}"].alignment = ALIGN_CENTER
        ws3[f"K{row}"].border = BORDER_ALL_THIN
        ws3[f"K{row}"].number_format = num_fmt_int
        input_cells_ws3.append(f"K{row}")

        # NPR Inherente: =I * J * K
        ws3[f"L{row}"] = f"=I{row}*J{row}*K{row}"
        ws3[f"L{row}"].font = FONT_BOLD
        ws3[f"L{row}"].alignment = ALIGN_CENTER
        ws3[f"L{row}"].border = BORDER_ALL_THIN
        ws3[f"L{row}"].fill = FILL_FORMULA
        ws3[f"L{row}"].number_format = num_fmt_int
        formula_cells_ws3.append(f"L{row}")

        # Prioridad Acción (AP)
        if lang == 'ES':
            ws3[f"M{row}"] = f'=IF(OR(L{row}>=120,I{row}>=9),"Alta",IF(L{row}>=60,"Media","Baja"))'
        else:
            ws3[f"M{row}"] = f'=IF(OR(L{row}>=120,I{row}>=9),"High",IF(L{row}>=60,"Medium","Low"))'
        ws3[f"M{row}"].font = FONT_BOLD
        ws3[f"M{row}"].alignment = ALIGN_CENTER
        ws3[f"M{row}"].border = BORDER_ALL_THIN
        ws3[f"M{row}"].fill = FILL_FORMULA
        formula_cells_ws3.append(f"M{row}")

        # Plan de acción
        ws3[f"N{row}"] = f[10]
        ws3[f"N{row}"].font = FONT_REGULAR
        ws3[f"N{row}"].alignment = ALIGN_LEFT
        ws3[f"N{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"N{row}")

        # Responsable
        ws3[f"O{row}"] = f[11]
        ws3[f"O{row}"].font = FONT_REGULAR
        ws3[f"O{row}"].alignment = ALIGN_CENTER
        ws3[f"O{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"O{row}")

        # Plazo
        ws3[f"P{row}"] = f[12]
        ws3[f"P{row}"].font = FONT_REGULAR
        ws3[f"P{row}"].alignment = ALIGN_CENTER
        ws3[f"P{row}"].border = BORDER_ALL_THIN
        input_cells_ws3.append(f"P{row}")

        # S Residual
        ws3[f"Q{row}"] = f[13]
        ws3[f"Q{row}"].font = FONT_BOLD
        ws3[f"Q{row}"].alignment = ALIGN_CENTER
        ws3[f"Q{row}"].border = BORDER_ALL_THIN
        ws3[f"Q{row}"].number_format = num_fmt_int
        input_cells_ws3.append(f"Q{row}")

        # O Residual
        ws3[f"R{row}"] = f[14]
        ws3[f"R{row}"].font = FONT_BOLD
        ws3[f"R{row}"].alignment = ALIGN_CENTER
        ws3[f"R{row}"].border = BORDER_ALL_THIN
        ws3[f"R{row}"].number_format = num_fmt_int
        input_cells_ws3.append(f"R{row}")

        # D Residual
        ws3[f"S{row}"] = f[15]
        ws3[f"S{row}"].font = FONT_BOLD
        ws3[f"S{row}"].alignment = ALIGN_CENTER
        ws3[f"S{row}"].border = BORDER_ALL_THIN
        ws3[f"S{row}"].number_format = num_fmt_int
        input_cells_ws3.append(f"S{row}")

        # NPR Residual: =Q * R * S
        ws3[f"T{row}"] = f"=Q{row}*R{row}*S{row}"
        ws3[f"T{row}"].font = FONT_BOLD
        ws3[f"T{row}"].alignment = ALIGN_CENTER
        ws3[f"T{row}"].border = BORDER_ALL_THIN
        ws3[f"T{row}"].fill = FILL_FORMULA
        ws3[f"T{row}"].number_format = num_fmt_int
        formula_cells_ws3.append(f"T{row}")

        # % Reducción: =(L - T) / L
        ws3[f"U{row}"] = f"=(L{row}-T{row})/L{row}"
        ws3[f"U{row}"].font = FONT_BOLD
        ws3[f"U{row}"].alignment = ALIGN_CENTER
        ws3[f"U{row}"].border = BORDER_ALL_THIN
        ws3[f"U{row}"].fill = FILL_FORMULA
        ws3[f"U{row}"].number_format = num_fmt_pct
        formula_cells_ws3.append(f"U{row}")

    end_row_ws3 = start_row_ws3 + len(fmea_data) - 1

    # Formato condicional para Prioridad de Acción en Pestaña 3
    ap_alta = '"Alta"' if lang == 'ES' else '"High"'
    ap_media = '"Media"' if lang == 'ES' else '"Medium"'
    ap_baja = '"Baja"' if lang == 'ES' else '"Low"'
    ws3.conditional_formatting.add(f"M6:M{end_row_ws3}", CellIsRule(operator="equal", formula=[ap_alta], fill=red_fill, font=red_font))
    ws3.conditional_formatting.add(f"M6:M{end_row_ws3}", CellIsRule(operator="equal", formula=[ap_media], fill=amber_fill, font=amber_font))
    ws3.conditional_formatting.add(f"M6:M{end_row_ws3}", CellIsRule(operator="equal", formula=[ap_baja], fill=green_fill, font=green_font))

    # =========================================================================
    # CONSTRUCCIÓN PESTAÑA 4: PLAN DE MITIGACIÓN & CAPEX
    # =========================================================================
    ws4.views.sheetView[0].showGridLines = True
    ws4.merge_cells("B2:L2")
    ws4["B2"] = ("DATALARIA | PLAN DE MITIGACIÓN, PRESUPUESTO CAPEX & ROI DEL CONTROL"
                 if lang == 'ES' else
                 "DATALARIA | MITIGATION PLAN, CAPEX BUDGET & CONTROL ROI")
    ws4["B2"].font = FONT_TITLE
    ws4["B2"].fill = FILL_NAVY
    ws4["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[2].height = 28

    ws4.merge_cells("B3:L3")
    ws4["B3"] = ("Asignación presupuestaria, análisis coste-beneficio de controles y reducción de pérdida esperada ΔE(L)"
                 if lang == 'ES' else
                 "Budget allocation, control cost-effectiveness ratio and expected loss reduction ΔE(L)")
    ws4["B3"].font = FONT_SUBTITLE
    ws4["B3"].fill = FILL_NAVY
    ws4["B3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[3].height = 18

    headers_ws4_es = [
        ("B5", "ID Control", 12),
        ("C5", "Riesgo / Fallo Asociado", 22),
        ("D5", "Acción de Mitigación / Inversión de Control", 44),
        ("E5", "Responsable", 18),
        ("F5", "Coste de Mitigación\n(CAPEX/OPEX)", 18),
        ("G5", "Pérdida Esperada\nPre-Control E(L)", 18),
        ("H5", "Pérdida Esperada\nPost-Control E(L)", 18),
        ("I5", "Reducción de\nPérdida ΔE(L)", 18),
        ("J5", "Ratio ROI Control\n(CER)", 15),
        ("K5", "Cronograma", 12),
        ("L5", "Estado", 14),
    ]

    headers_ws4_en = [
        ("B5", "Control ID", 12),
        ("C5", "Associated Risk / Failure", 22),
        ("D5", "Mitigation Action / Control Investment", 44),
        ("E5", "Owner", 18),
        ("F5", "Mitigation Cost\n(CAPEX/OPEX)", 18),
        ("G5", "Expected Loss\nPre-Control E(L)", 18),
        ("H5", "Expected Loss\nPost-Control E(L)", 18),
        ("I5", "Loss Reduction\nΔE(L)", 18),
        ("J5", "Control ROI\nRatio (CER)", 15),
        ("K5", "Schedule", 12),
        ("L5", "Status", 14),
    ]

    headers_ws4 = headers_ws4_es if lang == 'ES' else headers_ws4_en
    ws4.row_dimensions[5].height = 28

    for cell_ref, text, width in headers_ws4:
        cell = ws4[cell_ref]
        cell.value = text
        cell.font = FONT_TH
        cell.fill = FILL_NAVY_MED
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL_THIN
        col_letter = "".join([c for c in cell_ref if c.isalpha()])
        ws4.column_dimensions[col_letter].width = width

    input_cells_ws4 = []
    formula_cells_ws4 = []

    start_row_ws4 = 6
    for idx, c in enumerate(capex_data):
        row = start_row_ws4 + idx
        ws4.row_dimensions[row].height = 22

        # ID
        ws4[f"B{row}"] = c[0]
        ws4[f"B{row}"].font = FONT_BOLD
        ws4[f"B{row}"].alignment = ALIGN_CENTER
        ws4[f"B{row}"].border = BORDER_ALL_THIN
        ws4[f"B{row}"].fill = FILL_GRAY

        # Asociado
        ws4[f"C{row}"] = c[1]
        ws4[f"C{row}"].font = FONT_REGULAR
        ws4[f"C{row}"].alignment = ALIGN_CENTER
        ws4[f"C{row}"].border = BORDER_ALL_THIN
        input_cells_ws4.append(f"C{row}")

        # Acción
        ws4[f"D{row}"] = c[2]
        ws4[f"D{row}"].font = FONT_REGULAR
        ws4[f"D{row}"].alignment = ALIGN_LEFT
        ws4[f"D{row}"].border = BORDER_ALL_THIN
        input_cells_ws4.append(f"D{row}")

        # Responsable
        ws4[f"E{row}"] = c[3]
        ws4[f"E{row}"].font = FONT_REGULAR
        ws4[f"E{row}"].alignment = ALIGN_CENTER
        ws4[f"E{row}"].border = BORDER_ALL_THIN
        input_cells_ws4.append(f"E{row}")

        # Coste
        ws4[f"F{row}"] = c[4]
        ws4[f"F{row}"].font = FONT_BOLD
        ws4[f"F{row}"].alignment = ALIGN_RIGHT
        ws4[f"F{row}"].border = BORDER_ALL_THIN
        ws4[f"F{row}"].number_format = num_fmt_curr
        input_cells_ws4.append(f"F{row}")

        # Pérdida Pre
        ws4[f"G{row}"] = c[5]
        ws4[f"G{row}"].font = FONT_REGULAR
        ws4[f"G{row}"].alignment = ALIGN_RIGHT
        ws4[f"G{row}"].border = BORDER_ALL_THIN
        ws4[f"G{row}"].number_format = num_fmt_curr
        input_cells_ws4.append(f"G{row}")

        # Pérdida Post
        ws4[f"H{row}"] = c[6]
        ws4[f"H{row}"].font = FONT_REGULAR
        ws4[f"H{row}"].alignment = ALIGN_RIGHT
        ws4[f"H{row}"].border = BORDER_ALL_THIN
        ws4[f"H{row}"].number_format = num_fmt_curr
        input_cells_ws4.append(f"H{row}")

        # Reducción ΔE(L) = G - H
        ws4[f"I{row}"] = f"=G{row}-H{row}"
        ws4[f"I{row}"].font = FONT_BOLD
        ws4[f"I{row}"].alignment = ALIGN_RIGHT
        ws4[f"I{row}"].border = BORDER_ALL_THIN
        ws4[f"I{row}"].fill = FILL_FORMULA
        ws4[f"I{row}"].number_format = num_fmt_curr
        formula_cells_ws4.append(f"I{row}")

        # ROI / CER = I / F
        ws4[f"J{row}"] = f"=I{row}/F{row}"
        ws4[f"J{row}"].font = FONT_BOLD
        ws4[f"J{row}"].alignment = ALIGN_CENTER
        ws4[f"J{row}"].border = BORDER_ALL_THIN
        ws4[f"J{row}"].fill = FILL_FORMULA
        ws4[f"J{row}"].number_format = num_fmt_roi
        formula_cells_ws4.append(f"J{row}")

        # Cronograma
        ws4[f"K{row}"] = c[7]
        ws4[f"K{row}"].font = FONT_REGULAR
        ws4[f"K{row}"].alignment = ALIGN_CENTER
        ws4[f"K{row}"].border = BORDER_ALL_THIN
        input_cells_ws4.append(f"K{row}")

        # Estado
        ws4[f"L{row}"] = c[8]
        ws4[f"L{row}"].font = FONT_REGULAR
        ws4[f"L{row}"].alignment = ALIGN_CENTER
        ws4[f"L{row}"].border = BORDER_ALL_THIN
        input_cells_ws4.append(f"L{row}")

    end_row_ws4 = start_row_ws4 + len(capex_data) - 1

    # Totals Row
    tot_row = end_row_ws4 + 1
    ws4.row_dimensions[tot_row].height = 24
    ws4.merge_cells(f"B{tot_row}:E{tot_row}")
    ws4[f"B{tot_row}"] = "TOTAL CONSOLIDADO / CONSOLIDATED TOTAL" if lang == 'EN' else "TOTAL CONSOLIDADO"
    ws4[f"B{tot_row}"].font = FONT_TH_DARK
    ws4[f"B{tot_row}"].fill = FILL_GRAY
    ws4[f"B{tot_row}"].alignment = Alignment(horizontal="right", vertical="center")
    ws4[f"B{tot_row}"].border = BORDER_ALL_THIN

    # F sum
    ws4[f"F{tot_row}"] = f"=SUM(F6:F{end_row_ws4})"
    ws4[f"F{tot_row}"].font = FONT_BOLD
    ws4[f"F{tot_row}"].fill = FILL_FORMULA
    ws4[f"F{tot_row}"].alignment = ALIGN_RIGHT
    ws4[f"F{tot_row}"].border = BORDER_ALL_THIN
    ws4[f"F{tot_row}"].number_format = num_fmt_curr
    formula_cells_ws4.append(f"F{tot_row}")

    # G sum
    ws4[f"G{tot_row}"] = f"=SUM(G6:G{end_row_ws4})"
    ws4[f"G{tot_row}"].font = FONT_BOLD
    ws4[f"G{tot_row}"].fill = FILL_FORMULA
    ws4[f"G{tot_row}"].alignment = ALIGN_RIGHT
    ws4[f"G{tot_row}"].border = BORDER_ALL_THIN
    ws4[f"G{tot_row}"].number_format = num_fmt_curr
    formula_cells_ws4.append(f"G{tot_row}")

    # H sum
    ws4[f"H{tot_row}"] = f"=SUM(H6:H{end_row_ws4})"
    ws4[f"H{tot_row}"].font = FONT_BOLD
    ws4[f"H{tot_row}"].fill = FILL_FORMULA
    ws4[f"H{tot_row}"].alignment = ALIGN_RIGHT
    ws4[f"H{tot_row}"].border = BORDER_ALL_THIN
    ws4[f"H{tot_row}"].number_format = num_fmt_curr
    formula_cells_ws4.append(f"H{tot_row}")

    # I sum
    ws4[f"I{tot_row}"] = f"=SUM(I6:I{end_row_ws4})"
    ws4[f"I{tot_row}"].font = FONT_BOLD
    ws4[f"I{tot_row}"].fill = FILL_FORMULA
    ws4[f"I{tot_row}"].alignment = ALIGN_RIGHT
    ws4[f"I{tot_row}"].border = BORDER_ALL_THIN
    ws4[f"I{tot_row}"].number_format = num_fmt_curr
    formula_cells_ws4.append(f"I{tot_row}")

    # J weighted ROI
    ws4[f"J{tot_row}"] = f"=I{tot_row}/F{tot_row}"
    ws4[f"J{tot_row}"].font = FONT_BOLD
    ws4[f"J{tot_row}"].fill = FILL_FORMULA
    ws4[f"J{tot_row}"].alignment = ALIGN_CENTER
    ws4[f"J{tot_row}"].border = BORDER_ALL_THIN
    ws4[f"J{tot_row}"].number_format = num_fmt_roi
    formula_cells_ws4.append(f"J{tot_row}")

    ws4[f"K{tot_row}"].border = BORDER_ALL_THIN
    ws4[f"K{tot_row}"].fill = FILL_GRAY
    ws4[f"L{tot_row}"].border = BORDER_ALL_THIN
    ws4[f"L{tot_row}"].fill = FILL_GRAY

    # =========================================================================
    # CONSTRUCCIÓN PESTAÑA 1: DASHBOARD EJECUTIVO
    # =========================================================================
    ws1.views.sheetView[0].showGridLines = True
    ws1.merge_cells("B2:M2")
    ws1["B2"] = ("DATALARIA | EXECUTIVE DECISION DASHBOARD: MATRIZ DE RIESGOS & AMFE"
                 if lang == 'ES' else
                 "DATALARIA | EXECUTIVE DECISION DASHBOARD: RISK MATRIX & FMEA")
    ws1["B2"].font = FONT_TITLE
    ws1["B2"].fill = FILL_NAVY
    ws1["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[2].height = 28

    ws1.merge_cells("B3:M3")
    ws1["B3"] = ("Visión C-Level: Concentración de riesgos, mapa de calor 5x5 dinámico y ranking Pareto de criticidad"
                 if lang == 'ES' else
                 "C-Level View: Risk concentration, dynamic 5x5 heatmap and Pareto criticality ranking")
    ws1["B3"].font = FONT_SUBTITLE
    ws1["B3"].fill = FILL_NAVY
    ws1["B3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[3].height = 18

    # Col dimensions for Tab 1
    col_widths_ws1 = {
        'B': 10, 'C': 14, 'D': 14, 'E': 14, 'F': 14, 'G': 14,
        'H': 14, 'I': 16, 'J': 18, 'K': 16, 'L': 16, 'M': 16
    }
    for col_l, w in col_widths_ws1.items():
        ws1.column_dimensions[col_l].width = w

    # -------------------------------------------------------------------------
    # 4 TARJETAS KPI C-LEVEL (Filas 5 a 7)
    # -------------------------------------------------------------------------
    ws1.row_dimensions[5].height = 16
    ws1.row_dimensions[6].height = 28
    ws1.row_dimensions[7].height = 16

    # KPI 1: Total Eventos Auditados
    ws1.merge_cells("B5:D5")
    ws1["B5"] = "TOTAL EVENTOS EVALUADOS" if lang == 'ES' else "TOTAL EVENTS EVALUATED"
    ws1["B5"].font = FONT_KPI_LBL
    ws1["B5"].alignment = ALIGN_CENTER

    ws1.merge_cells("B6:D6")
    ws1["B6"] = f"=COUNTA('{s2_name}'!B6:B{end_row_ws2}) + COUNTA('{s3_name}'!B6:B{end_row_ws3})"
    ws1["B6"].font = FONT_KPI_VAL_ACCENT
    ws1["B6"].alignment = ALIGN_CENTER
    ws1["B6"].number_format = num_fmt_int

    ws1.merge_cells("B7:D7")
    ws1["B7"] = "20 Riesgos Corp. + 15 Modos AMFE" if lang == 'ES' else "20 Corp. Risks + 15 FMEA Modes"
    ws1["B7"].font = FONT_KPI_SUB
    ws1["B7"].alignment = ALIGN_CENTER

    for r_idx in range(5, 8):
        for c_idx in ["B", "C", "D"]:
            cell = ws1[f"{c_idx}{r_idx}"]
            cell.fill = FILL_BLUE_LIGHT
            cell.border = BORDER_CARD

    # KPI 2: NPR Máximo Detectado
    ws1.merge_cells("E5:G5")
    ws1["E5"] = "NPR MÁXIMO DETECTADO" if lang == 'ES' else "MAX DETECTED RPN"
    ws1["E5"].font = FONT_KPI_LBL
    ws1["E5"].alignment = ALIGN_CENTER

    ws1.merge_cells("E6:G6")
    ws1["E6"] = f"=MAX('{s3_name}'!L6:L{end_row_ws3})"
    ws1["E6"].font = FONT_KPI_VAL
    ws1["E6"].alignment = ALIGN_CENTER
    ws1["E6"].number_format = num_fmt_int

    ws1.merge_cells("E7:G7")
    ws1["E7"] = "Crítico: Requiere acción inmediata" if lang == 'ES' else "Critical: Immediate action required"
    ws1["E7"].font = FONT_KPI_SUB
    ws1["E7"].alignment = ALIGN_CENTER

    for r_idx in range(5, 8):
        for c_idx in ["E", "F", "G"]:
            cell = ws1[f"{c_idx}{r_idx}"]
            cell.fill = FILL_RED_LIGHT
            cell.border = BORDER_CARD

    # KPI 3: % Fallos de Alta Prioridad (AP Alta)
    ws1.merge_cells("H5:J5")
    ws1["H5"] = "% PRIORIDAD ALTA (AP ALTA)" if lang == 'ES' else "% HIGH ACTION PRIORITY"
    ws1["H5"].font = FONT_KPI_LBL
    ws1["H5"].alignment = ALIGN_CENTER

    ws1.merge_cells("H6:J6")
    target_ap = '"Alta"' if lang == 'ES' else '"High"'
    ws1["H6"] = f"=COUNTIF('{s3_name}'!M6:M{end_row_ws3},{target_ap})/COUNTA('{s3_name}'!M6:M{end_row_ws3})"
    ws1["H6"].font = FONT_KPI_VAL
    ws1["H6"].alignment = ALIGN_CENTER
    ws1["H6"].number_format = num_fmt_pct

    ws1.merge_cells("H7:J7")
    ws1["H7"] = "Umbral Board: < 20% objetivo" if lang == 'ES' else "Board Threshold: < 20% target"
    ws1["H7"].font = FONT_KPI_SUB
    ws1["H7"].alignment = ALIGN_CENTER

    for r_idx in range(5, 8):
        for c_idx in ["H", "I", "J"]:
            cell = ws1[f"{c_idx}{r_idx}"]
            cell.fill = FILL_AMBER_LIGHT
            cell.border = BORDER_CARD

    # KPI 4: Reducción Media de Riesgo Residual
    ws1.merge_cells("K5:M5")
    ws1["K5"] = "REDUCCIÓN RIESGO RESIDUAL" if lang == 'ES' else "RESIDUAL RISK REDUCTION"
    ws1["K5"].font = FONT_KPI_LBL
    ws1["K5"].alignment = ALIGN_CENTER

    ws1.merge_cells("K6:M6")
    ws1["K6"] = f"=AVERAGE('{s3_name}'!U6:U{end_row_ws3})"
    ws1["K6"].font = FONT_KPI_VAL
    ws1["K6"].alignment = ALIGN_CENTER
    ws1["K6"].number_format = num_fmt_pct

    ws1.merge_cells("K7:M7")
    ws1["K7"] = "Eficacia proyectada post-CAPEX" if lang == 'ES' else "Projected efficacy post-CAPEX"
    ws1["K7"].font = FONT_KPI_SUB
    ws1["K7"].alignment = ALIGN_CENTER

    for r_idx in range(5, 8):
        for c_idx in ["K", "L", "M"]:
            cell = ws1[f"{c_idx}{r_idx}"]
            cell.fill = FILL_GREEN_LIGHT
            cell.border = BORDER_CARD

    # -------------------------------------------------------------------------
    # MATRIZ DE CALOR 5x5 DINÁMICA (Lado Izquierdo: Columnas B a G, Filas 10 a 18)
    # -------------------------------------------------------------------------
    ws1.merge_cells("B9:G9")
    ws1["B9"] = ("1. MATRIZ DE CALOR 5x5: PROBABILIDAD VS. IMPACTO (ISO 31000)"
                 if lang == 'ES' else
                 "1. 5x5 DYNAMIC HEAT MAP: PROBABILITY VS. IMPACT (ISO 31000)")
    ws1["B9"].font = FONT_SEC_HEADER
    ws1["B9"].fill = FILL_NAVY_MED
    ws1["B9"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[9].height = 22

    # Column Subheaders (Impacto 1 a 5)
    impact_labels_es = ["P \\ I", "1: Muy Bajo", "2: Bajo", "3: Medio", "4: Alto", "5: Crítico"]
    impact_labels_en = ["P \\ I", "1: Very Low", "2: Low", "3: Medium", "4: High", "5: Critical"]
    impact_labels = impact_labels_es if lang == 'ES' else impact_labels_en

    cols_heat = ["B", "C", "D", "E", "F", "G"]
    ws1.row_dimensions[10].height = 20
    for idx_c, col_name in enumerate(cols_heat):
        cell = ws1[f"{col_name}10"]
        cell.value = impact_labels[idx_c]
        cell.font = FONT_TH
        cell.fill = FILL_NAVY
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL_THIN

    # Filas: Probabilidad de 5 (arriba) a 1 (abajo)
    prob_rows = [
        (11, 5, "5: Muy Alta" if lang == 'ES' else "5: Very High"),
        (12, 4, "4: Alta" if lang == 'ES' else "4: High"),
        (13, 3, "3: Media" if lang == 'ES' else "3: Medium"),
        (14, 2, "2: Baja" if lang == 'ES' else "2: Low"),
        (15, 1, "1: Muy Baja" if lang == 'ES' else "1: Very Low"),
    ]

    # Paletas de color por celda según Score = P * I
    fill_crit = PatternFill("solid", fgColor="FEE2E2") # Rojo
    font_crit = Font(name="Segoe UI", size=10, bold=True, color="991B1B")
    fill_med = PatternFill("solid", fgColor="FEF3C7")  # Amarillo
    font_med = Font(name="Segoe UI", size=10, bold=True, color="92400E")
    fill_low = PatternFill("solid", fgColor="D1FAE5")  # Verde
    font_low = Font(name="Segoe UI", size=10, bold=True, color="065F46")

    formula_cells_ws1 = []

    for r_num, p_val, p_lbl in prob_rows:
        ws1.row_dimensions[r_num].height = 22
        # Header de la fila (Probabilidad)
        cell_p = ws1[f"B{r_num}"]
        cell_p.value = p_lbl
        cell_p.font = FONT_TH_DARK
        cell_p.fill = FILL_GRAY
        cell_p.alignment = ALIGN_CENTER
        cell_p.border = BORDER_ALL_THIN

        for i_val in range(1, 6):
            col_letter = cols_heat[i_val]
            cell_heat = ws1[f"{col_letter}{r_num}"]
            # COUNTIFS fórmula dinámica: cuenta riesgos donde Impacto=i_val y Probabilidad=p_val
            cell_heat.value = f"=COUNTIFS('{s2_name}'!$E$6:$E${end_row_ws2},{i_val},'{s2_name}'!$F$6:$F${end_row_ws2},{p_val})"
            cell_heat.alignment = ALIGN_CENTER
            cell_heat.border = BORDER_ALL_THIN
            formula_cells_ws1.append(f"{col_letter}{r_num}")

            # Color estático según puntuación P * I
            score = p_val * i_val
            if score >= 15:
                cell_heat.fill = fill_crit
                cell_heat.font = font_crit
            elif score >= 8:
                cell_heat.fill = fill_med
                cell_heat.font = font_med
            else:
                cell_heat.fill = fill_low
                cell_heat.font = font_low

    # Resumen de Cuadrantes debajo del Heat Map
    ws1.merge_cells("B16:C16")
    ws1["B16"] = "ZONA CRÍTICA (Score 15-25):" if lang == 'ES' else "CRITICAL ZONE (Score 15-25):"
    ws1["B16"].font = font_crit
    ws1["B16"].fill = fill_crit
    ws1["B16"].alignment = ALIGN_LEFT
    ws1["B16"].border = BORDER_ALL_THIN

    ws1["D16"] = f"=COUNTIF('{s2_name}'!H6:H{end_row_ws2},{crit_val})"
    ws1["D16"].font = font_crit
    ws1["D16"].fill = fill_crit
    ws1["D16"].alignment = ALIGN_CENTER
    ws1["D16"].border = BORDER_ALL_THIN
    formula_cells_ws1.append("D16")

    ws1.merge_cells("E16:F16")
    ws1["E16"] = "ZONA MEDIA (Score 8-12):" if lang == 'ES' else "MEDIUM ZONE (Score 8-12):"
    ws1["E16"].font = font_med
    ws1["E16"].fill = fill_med
    ws1["E16"].alignment = ALIGN_LEFT
    ws1["E16"].border = BORDER_ALL_THIN

    ws1["G16"] = f"=COUNTIF('{s2_name}'!H6:H{end_row_ws2},{med_val})"
    ws1["G16"].font = font_med
    ws1["G16"].fill = fill_med
    ws1["G16"].alignment = ALIGN_CENTER
    ws1["G16"].border = BORDER_ALL_THIN
    formula_cells_ws1.append("G16")

    # -------------------------------------------------------------------------
    # TABLA PARETO C-LEVEL TOP MODOS DE FALLO (Lado Derecho: H a M, Filas 9 a 17)
    # -------------------------------------------------------------------------
    ws1.merge_cells("I9:M9")
    ws1["I9"] = ("2. TOP MODOS DE FALLO CRÍTICOS (AIAG-VDA NPR)"
                 if lang == 'ES' else
                 "2. TOP CRITICAL FAILURE MODES (AIAG-VDA RPN)")
    ws1["I9"].font = FONT_SEC_HEADER
    ws1["I9"].fill = FILL_NAVY_MED
    ws1["I9"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    headers_pareto_es = [("I10", "Modo de Fallo", 20), ("J10", "Componente", 16), ("K10", "Sev", 8), ("L10", "NPR", 10), ("M10", "AP", 10)]
    headers_pareto_en = [("I10", "Failure Mode", 20), ("J10", "Component", 16), ("K10", "Sev", 8), ("L10", "RPN", 10), ("M10", "AP", 10)]
    headers_pareto = headers_pareto_es if lang == 'ES' else headers_pareto_en

    for cell_ref, text, w in headers_pareto:
        cell = ws1[cell_ref]
        cell.value = text
        cell.font = FONT_TH
        cell.fill = FILL_NAVY
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL_THIN

    # Top 6 Modos de fallo vinculados directamente a la Pestaña 3
    # Los primeros 6 modos ordenados por criticidad
    pareto_source_rows = [6, 7, 8, 9, 10, 11]  # filas en Tab 3
    for idx_p, src_row in enumerate(pareto_source_rows):
        r_dest = 11 + idx_p
        ws1.row_dimensions[r_dest].height = 20

        # Modo de fallo
        c_mode = ws1[f"I{r_dest}"]
        c_mode.value = f"='{s3_name}'!D{src_row}"
        c_mode.font = FONT_REGULAR
        c_mode.alignment = ALIGN_LEFT
        c_mode.border = BORDER_ALL_THIN
        formula_cells_ws1.append(f"I{r_dest}")

        # Componente
        c_comp = ws1[f"J{r_dest}"]
        c_comp.value = f"='{s3_name}'!C{src_row}"
        c_comp.font = FONT_REGULAR
        c_comp.alignment = ALIGN_CENTER
        c_comp.border = BORDER_ALL_THIN
        formula_cells_ws1.append(f"J{r_dest}")

        # Sev
        c_s = ws1[f"K{r_dest}"]
        c_s.value = f"='{s3_name}'!I{src_row}"
        c_s.font = FONT_BOLD
        c_s.alignment = ALIGN_CENTER
        c_s.border = BORDER_ALL_THIN
        formula_cells_ws1.append(f"K{r_dest}")

        # NPR
        c_npr = ws1[f"L{r_dest}"]
        c_npr.value = f"='{s3_name}'!L{src_row}"
        c_npr.font = FONT_BOLD
        c_npr.alignment = ALIGN_CENTER
        c_npr.border = BORDER_ALL_THIN
        formula_cells_ws1.append(f"L{r_dest}")

        # AP
        c_ap = ws1[f"M{r_dest}"]
        c_ap.value = f"='{s3_name}'!M{src_row}"
        c_ap.font = FONT_BOLD
        c_ap.alignment = ALIGN_CENTER
        c_ap.border = BORDER_ALL_THIN
        formula_cells_ws1.append(f"M{r_dest}")

    # Formato condicional para AP en Pareto
    ws1.conditional_formatting.add("M11:M16", CellIsRule(operator="equal", formula=[ap_alta], fill=red_fill, font=red_font))
    ws1.conditional_formatting.add("M11:M16", CellIsRule(operator="equal", formula=[ap_media], fill=amber_fill, font=amber_font))
    ws1.conditional_formatting.add("M11:M16", CellIsRule(operator="equal", formula=[ap_baja], fill=green_fill, font=green_font))

    # -------------------------------------------------------------------------
    # RESUMEN EJECUTIVO DE CAPEX & ROI (Filas 18 a 22)
    # -------------------------------------------------------------------------
    ws1.merge_cells("B18:M18")
    ws1["B18"] = ("3. BALANCE FINANCIERO DE MITIGACIÓN & ASIGNACIÓN DE CAPEX"
                  if lang == 'ES' else
                  "3. FINANCIAL MITIGATION BALANCE & CAPEX ALLOCATION")
    ws1["B18"].font = FONT_SEC_HEADER
    ws1["B18"].fill = FILL_NAVY_MED
    ws1["B18"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[18].height = 22

    capex_summary_items_es = [
        ("B20:D20", "B21:D21", "Presupuesto CAPEX / OPEX Requerido", f"='{s4_name}'!F{tot_row}", num_fmt_curr, FILL_BLUE_LIGHT, C_BLUE_ACCENT),
        ("E20:G20", "E21:G21", "Reducción de Pérdida Esperada ΔE(L)", f"='{s4_name}'!I{tot_row}", num_fmt_curr, FILL_GREEN_LIGHT, C_GREEN_TEXT),
        ("H20:J20", "H21:J21", "ROI del Control (Cost-Effectiveness Ratio)", f"='{s4_name}'!J{tot_row}", num_fmt_roi, FILL_AMBER_LIGHT, C_AMBER_TEXT),
        ("K20:M20", "K21:M21", "Controles Aprobados / Planificados", f"=COUNTA('{s4_name}'!B6:B{end_row_ws4})", num_fmt_int, FILL_GRAY, C_NAVY_DARK),
    ]

    capex_summary_items_en = [
        ("B20:D20", "B21:D21", "Required CAPEX / OPEX Budget", f"='{s4_name}'!F{tot_row}", num_fmt_curr, FILL_BLUE_LIGHT, C_BLUE_ACCENT),
        ("E20:G20", "E21:G21", "Expected Loss Reduction ΔE(L)", f"='{s4_name}'!I{tot_row}", num_fmt_curr, FILL_GREEN_LIGHT, C_GREEN_TEXT),
        ("H20:J20", "H21:J21", "Control ROI (Cost-Effectiveness Ratio)", f"='{s4_name}'!J{tot_row}", num_fmt_roi, FILL_AMBER_LIGHT, C_AMBER_TEXT),
        ("K20:M20", "K21:M21", "Approved / Planned Controls Count", f"=COUNTA('{s4_name}'!B6:B{end_row_ws4})", num_fmt_int, FILL_GRAY, C_NAVY_DARK),
    ]

    capex_items = capex_summary_items_es if lang == 'ES' else capex_summary_items_en

    for lbl_rng, val_rng, lbl_text, formula_val, n_fmt, bg_fill, txt_color in capex_items:
        ws1.merge_cells(lbl_rng)
        top_cell = ws1[lbl_rng.split(":")[0]]
        top_cell.value = lbl_text.upper()
        top_cell.font = FONT_KPI_LBL
        top_cell.alignment = ALIGN_CENTER

        ws1.merge_cells(val_rng)
        val_cell = ws1[val_rng.split(":")[0]]
        val_cell.value = formula_val
        val_cell.font = Font(name="Segoe UI", size=15, bold=True, color=txt_color)
        val_cell.alignment = ALIGN_CENTER
        val_cell.number_format = n_fmt
        formula_cells_ws1.append(val_rng.split(":")[0])

        col_start = lbl_rng.split(":")[0][0]
        col_end = lbl_rng.split(":")[1][0]
        cols_span = [chr(c) for c in range(ord(col_start), ord(col_end) + 1)]
        r1 = int("".join([c for c in lbl_rng.split(":")[0] if c.isdigit()]))
        r2 = int("".join([c for c in val_rng.split(":")[1] if c.isdigit()]))
        for r_x in range(r1, r2 + 1):
            for c_x in cols_span:
                cell_box = ws1[f"{c_x}{r_x}"]
                if not isinstance(cell_box, openpyxl.cell.cell.MergedCell):
                    cell_box.fill = bg_fill
                    cell_box.border = BORDER_CARD

    # -------------------------------------------------------------------------
    # APLICAR POLÍTICA DE PROTECCIÓN RIGUROSA (ECMA-376)
    # -------------------------------------------------------------------------
    # Pestaña 1: Sólo visualización / Dashboard C-Level
    for row in ws1.iter_rows():
        for cell in row:
            if not isinstance(cell, openpyxl.cell.cell.MergedCell):
                cell.protection = Protection(locked=True)
    apply_sheet_protection(ws1)

    # Pestaña 2: Matriz 5x5
    for row in ws2.iter_rows():
        for cell in row:
            if not isinstance(cell, openpyxl.cell.cell.MergedCell):
                coord = cell.coordinate
                if coord in input_cells_ws2:
                    cell.protection = Protection(locked=False)
                    cell.fill = FILL_INPUT
                else:
                    cell.protection = Protection(locked=True)
    apply_sheet_protection(ws2)

    # Pestaña 3: AMFE FMEA
    for row in ws3.iter_rows():
        for cell in row:
            if not isinstance(cell, openpyxl.cell.cell.MergedCell):
                coord = cell.coordinate
                if coord in input_cells_ws3:
                    cell.protection = Protection(locked=False)
                    cell.fill = FILL_INPUT
                else:
                    cell.protection = Protection(locked=True)
    apply_sheet_protection(ws3)

    # Pestaña 4: Plan Mitigación & CAPEX
    for row in ws4.iter_rows():
        for cell in row:
            if not isinstance(cell, openpyxl.cell.cell.MergedCell):
                coord = cell.coordinate
                if coord in input_cells_ws4:
                    cell.protection = Protection(locked=False)
                    cell.fill = FILL_INPUT
                else:
                    cell.protection = Protection(locked=True)
    apply_sheet_protection(ws4)

    return wb


def main():
    base_pack_dir = "packages/Suite_03_Control_Operativo/02_Matriz_Riesgos_AMFE"
    dir_es = os.path.join(base_pack_dir, "[ES]_Matriz_Riesgos_AMFE")
    dir_en = os.path.join(base_pack_dir, "[EN]_FMEA_Risk_Matrix")

    os.makedirs(dir_es, exist_ok=True)
    os.makedirs(dir_en, exist_ok=True)

    path_es = os.path.join(dir_es, "Matriz_Riesgos_AMFE_Datalaria_ES.xlsx")
    path_en = os.path.join(dir_en, "Quantitative_Risk_Matrix_FMEA_EN.xlsx")

    print("[1/2] Generando modelo Excel en Español...")
    wb_es = build_amfe_workbook(lang='ES')
    wb_es.save(path_es)
    print(f"  -> Guardado: {path_es}")

    print("[2/2] Generando modelo Excel en Inglés...")
    wb_en = build_amfe_workbook(lang='EN')
    wb_en.save(path_en)
    print(f"  -> Guardado: {path_en}")

    print("\n✓ Generación de motores Excel completada con éxito.")


if __name__ == "__main__":
    main()
