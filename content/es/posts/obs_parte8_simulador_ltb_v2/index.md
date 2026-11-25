---
title: "Radar IEC 62402 (Parte 8): Grafo BOM y Decisión Last Time Buy vs Rediseño"
date: 2026-12-09
draft: false
translationKey: "obs-part8-ltb-simulator-v2"
category: "Estrategia y Operaciones"
categories: ["Control Operativo", "Supply Chain", "IA, Ingeniería y Proyectos", "Estrategia y Operaciones"]
tags: ["IEC 62402", "Gestión de Obsolescencia", "Last Time Buy", "LTB", "Rediseño FFF", "BOM", "PCN", "PDN", "EOL", "Agentic Radar", "PostgreSQL RLS", "FastAPI"]
description: "Cómo operacionalizar la norma IEC 62402 con Agentic Radar v2.0: explosión de grafos BOM sin ciclos, cálculo financiero Last Time Buy (LTB) vs. rediseño FFF y sinergia con Stock de Seguridad."
summary: "Evolución mayor v2.0 de Agentic Radar (Executive Risk Cockpit Zero-CDN): arquitectura determinista de grafos BOM, evaluación financiera CAPEX Last Time Buy frente a Rediseño Form-Fit-Function, privacidad CSV en navegador, esquema PostgreSQL obs_radar con RLS y el relevo exacto frente al punto de pedido ROP."
cover:
  image: "cover.png"
  alt: "Agentic Radar v2.0: Cockpit Ejecutivo IEC 62402, Simulador de Grafo BOM y Decisión LTB vs. Rediseño"
  caption: "Agentic Radar v2.0.0 — Executive Risk Cockpit Zero-CDN (< 34 KB gzip), Simulador PDN/BOM SVG y Kit B2B IEC 62402."
  relative: true
images:
  - "cover.png"
  - "preview-pack.png"
  - "obs_lifecycle_relay.png"
---

En los comités de operaciones de manufactura avanzada, electrónica industrial, equipamiento médico y sistemas aeroespaciales, existe una asimetría financiera capaz de destruir el EBITDA de todo un ejercicio fiscal en cuestión de semanas: **un condensador cerámico multicapa o un microcontrolador de 2,15 € puede paralizar la facturación de líneas completas con cientos de miles de euros en margen bruto P&L comprometido**.

Cuando un fabricante de semiconductores emite una notificación oficial de discontinuación (**PDN** — *Product Discontinuance Notice* o **EOL** — *End of Life*), la sala de juntas se divide casi instantáneamente entre dos prioridades opuestas:

1. **El Director de Operaciones (COO) y el Ingeniero de Componentes**, conscientes de que no existen fuentes alternativas cualificadas en la Lista de Fabricantes Aprobados (**AML**), exigen aprobar de inmediato una compra de emergencia para los próximos 24 o 36 meses antes de la fecha límite de fabricación (*LTB Cutoff Date*), con tal de no detener las líneas de ensamblaje.
2. **El Director Financiero (CFO)** observa con escepticismo una factura CAPEX no presupuestada que inmoviliza cientos de miles de euros en un almacén inmóvil, castiga el coste medio ponderado del capital (**WACC**) y conlleva riesgo de merma si las previsiones comerciales caen.

Lo que agrava esta parálisis ejecutiva es que la mayoría de organizaciones intentan resolver avisos de fin de vida utilizando **hojas de cálculo planas y parámetros de reposición continua**, una trampa metodológica que falla porque asume un mundo donde el proveedor sigue aceptando pedidos recurrentes cada trimestre.

En las siete entregas anteriores de esta serie ([Parte 1: El Ajedrez de la Obsolescencia](/es/posts/obs_parte1_intro/) hasta la [Parte 7: Dashboard Ejecutivo Táctico](/es/posts/obs_parte7_dashboard/)), construimos los cimientos de **Agentic Radar (`obs-management`)**: ingesta orientada a eventos en FastAPI, extracción semántica con agentes CrewAI y modelado relacional de listas de materiales (**BOM**) en PostgreSQL.

Hoy presentamos **Agentic Radar `v2.0.0` (Executive Risk Cockpit Zero-CDN)** junto al nuevo paquete especializado **`pack-obs` (*IEC 62402 Obsolescence, BOM Risk & LTB Decision Kit*)**. En esta octava entrega profundizamos en la matemática determinista de grafos BOM sin ciclos, la frontera financiera entre **Last Time Buy (LTB)** y **Rediseño Form-Fit-Function (FFF)**, el blindaje multi-tenant con **Row-Level Security (`obs_radar`)** y, sobre todo, la regla exacta de convivencia con tu motor de inventario de madurez (**Stock de Seguridad & Punto de Pedido `pack-stock`**).

---

## 1. El Relevo Matemático en el Ciclo de Vida: `pack-stock` (Madurez ROP) vs. `pack-obs` (Crisis IEC 62402 / LTB)

Uno de los errores más costosos que observamos en auditorías de cadena de suministro es confundir **la gestión estadística del inventario en fase de madurez** con **la ingeniería de obsolescencia en fase de discontinuación**. Aunque ambas disciplinas protegen la continuidad física de planta, operan bajo supuestos matemáticos incompatibles.

Mientras un componente está en estado **`Active`** (el proveedor fabrica con normalidad y acepta órdenes mensuales), la variable crítica es absorber la volatilidad conjunta de la demanda ($\sigma_d$) y los retrasos logísticos ($\sigma_L$) mediante la convolución de **Stock de Seguridad ($SS_3$)**, **Punto de Pedido ($ROP$)** y **Lote Económico de Wilson ($EOQ$)** —el territorio exacto que automatiza nuestra [Calculadora de Stock de Seguridad & ROP (`pack-stock`)](/es/posts/calculadora-stock-seguridad-rop/), Pilar 5 de la [Suite 03: Control Operativo](/es/posts/control-operativo-pmbok-framework-cuantitativo/).

Sin embargo, el día que entra en tu bandeja un aviso **PCN** (*Product Change Notification*), **PDN** o **EOL**, **el concepto mismo de Punto de Pedido ($ROP$) queda invalidado**. La línea de silicio va a cerrarse permanentemente. Mantener activo el disparo automático de pedidos recurrentes en el ERP falsea la rotación, genera compras tardías rechazadas por el fabricante o inmoviliza subconjuntos huérfanos en almacén (*Dead Stock*). La regla de oro operativa exige **congelar el $ROP$ recurrente de esa referencia** y entregar el testigo al protocolo **IEC 62402**.

{{< mermaid image="obs_lifecycle_relay.png" alt="Diagrama del Relevo Matemático en el Ciclo de Vida del Componente: Fase 1 Madurez (pack-stock ROP/EOQ) vs. Fase 2 Crisis Fin de Vida (Agentic Radar v2.0 y pack-obs IEC 62402 LTB)" >}}
flowchart LR
    subgraph F1["FASE 1 · MADUREZ Y FLUJO CONTINUO (Proveedor Activo)"]
        A["pack-stock (7 EUR) / Suite 03 (22 EUR)<br/>Estandar APICS / ASCM & MIT CTL<br/>Convolucion Demanda y Plazo (SS3)<br/>Punto de Pedido Recurrente (ROP)<br/>Lote Economico de Wilson (EOQ)"]
    end

    subgraph EV["DISRUPCION DEL CICLO DE VIDA"]
        X["Aviso Fabricante PCN / PDN / EOL<br/>ACCION: Congelar ROP Automatico"]
    end

    subgraph F2["FASE 2 · FIN DE VIDA Y CRISIS BOM (Linea Cierra)"]
        B["Agentic Radar v2.0 + pack-obs (19 EUR)<br/>Estandar Internacional IEC 62402<br/>Explosion DAG BOM (MPN a SKU)<br/>Colchon Puente Unico SS_LTB<br/>Veredicto CAPEX: LTB (WACC) vs. FFF (NRE)"]
    end

    A -->|"Monitoreo continuo de MPNs"| X
    X -->|"Alerta CRITICAL LTB REQUIRED"| B
    B -->|"Componente redisenado (FFF)"| A

    style F1 fill:#0b1720,stroke:#10b981,stroke-width:2px,color:#f8fafc
    style EV fill:#261c0f,stroke:#f59e0b,stroke-width:2px,color:#f8fafc
    style F2 fill:#0b1324,stroke:#0ea5e9,stroke-width:2px,color:#f8fafc
{{< /mermaid >}}

Para que tu equipo de Compras, Ingeniería y Finanzas sepa exactamente qué modelo abrir en cada reunión de comité sin la menor ambigüedad, esta matriz compara ambos activos:

| Dimensión Operativa | 📦 `pack-stock` (*Calculadora Stock de Seguridad & ROP · 7 €*) | 📡 `pack-obs` (*Kit IEC 62402 Obsolescencia, BOM & LTB · 19 €*) |
| :--- | :--- | :--- |
| **Fase del Ciclo de Vida** | **Madurez (`Active`):** Proveedor activo con reposición continua. | **Declive / Crisis (`NRND / PDN / EOL / Obsolete`):** Cierre definitivo de línea. |
| **Ubicación en Catálogo** | Pilar 5 de la **Suite 03: Control Operativo** (22 €). | **Kit Vertical Especializado** acoplado a la app **Agentic Radar v2.0**. |
| **Estándar Internacional** | **APICS / ASCM & MIT CTL** (Revisión continua $(s, Q)$). | **IEC 62402 & JEDEC J-STD-048** (Gestión de obsolescencia y PDNs). |
| **Alcance Estructural** | SKU individual / referencia en almacén central. | **Grafo BOM multinivel** (`MPN → Parte Interna → AML → Subensamblaje → SKU`). |
| **Motor Matemático** | Convolución estocástica $SS_3$, umbral $ROP$ y lote óptimo $EOQ$. | Explosión DAG sin ciclos, Criticidad IEC (0–100), $SS_{\text{LTB}}$ y LTB vs. FFF. |
| **Pregunta de Negocio** | *¿Cuánto stock mínimo mantener cada mes para cubrir un 98 % de servicio?* | *¿Qué productos finales se paran y conviene LTB a 3 años o rediseño NRE?* |
| **Entregables del `.ZIP`** | Excel 35 SKUs + Gráfico Diente de Sierra + PPTX 16:9 + PDF 5 págs. | Excel Dual 5 hojas (ES/EN) + Playbook PDF 5 págs. + Blueprint SQL RLS/Python/CSV. |

---

## 2. El Músculo Determinista: Recorrido DAG de BOM, Criticidad IEC 62402 y Decisión LTB vs. FFF

En **Agentic Radar v2.0** aplicamos un principio inmutable de ingeniería financiera: **los modelos de lenguaje (CrewAI) interpretan avisos de texto libre, pero jamás realizan aritmética financiera ni recorren estructuras de costes**. Todo el cálculo crítico reside en **El Músculo**, implementado con paridad numérica exacta (`< 0,01 €` de desviación) en dos motores gemelos: `apps/obs-management/web/engine.js` (para ejecución instantánea en el navegador) y `apps/obs-management/api/bom_engine.py` (para validación FastAPI en servidor).

### 2.1 Explosión Ascendente de Grafos BOM Multinivel con Guardia Anti-Ciclos

En entornos industriales reales, un mismo `MPN` de fabricante puede mapearse a una referencia interna (`Internal Part`), que a su vez forma parte de múltiples subensamblajes compartidos entre varias familias de productos comerciales (`SKU Final`). Además, las exportaciones ERP sucias contienen en ocasiones referencias circulares heredadas entre subconjuntos.

Para evitar bucles infinitos y doble contabilización del margen comercial, el algoritmo ejecuta una **búsqueda en profundidad ascendente (DFS)** con conjunto de nodos visitados por rama (`visited`) y **deduplicación estricta por `sku`** en la agregación final de P&L:

1. **Resolución de AML (*Approved Manufacturer List*):** A partir del MPN impactado, se comprueba cuántos MPN alternativos permanecen en estado `Active` asociados a la misma `internal_part_id`. Si existen alternativas cualificadas activas, la criticidad cae drásticamente.
2. **Propagación recursiva de ruta:** Desde cada `internal_part` afectada se asciende por `bom_lines` hacia cada `assembly` padre protegiendo cada paso con `if next_part in visited: flag cycle_detected = True; continue`.
3. **Deduplicación de Margen P&L:** Si un SKU final (`DRONE-X1`, con margen anual expuesto de 12.500 €) consume simultáneamente dos componentes obsoletos en placas distintas, el sistema informa ambas rutas críticas en la tabla de trazabilidad pero suma **una única vez** los 12.500 € en el KPI global de Margen P&L en Riesgo.

### 2.2 Índice Cuantitativo de Criticidad IEC 62402 (0–100)

Cada combinación ruta-componente recibe un índice transparente y auditable que el usuario puede verificar tanto en el popover `Fórmula IEC` del Cockpit como en la hoja `02_IEC62402_CRITICALITY` del Excel del Kit:

$$
C_{\text{IEC}} = \min\left(100,\; \text{AML}_{40} + \text{EOL}_{35} + \text{LT}_{15} + \text{PnL}_{10}\right)
$$

Donde:
- **Fuente Única AML ($\text{AML}_{40}$):** `40` puntos si no hay fuentes alternativas activas (`alt_sources = 0`), `20` puntos con 1 fuente alternativa y `5` puntos con $\ge 2$ alternativas cualificadas.
- **Urgencia de Ciclo de Vida ($\text{EOL}_{35}$):** `35` puntos para `Obsolete`, `30` para `EOL`, `22` para `PDN`, `12` para `NRND` y `0` para `Active`.
- **Exposición de Plazo de Entrega ($\text{LT}_{15}$):** `15` puntos si `lead_time >= 24 semanas`, `10` si está entre `12` y `23` semanas, y `4` por debajo.
- **Impacto Financiero P&L ($\text{PnL}_{10}$):** `10` puntos cuando el margen expuesto supera los `150.000 €/año` (o umbral crítico de SKU), `6` en tramo medio y `2` en bajo impacto.

Las referencias con $C_{\text{IEC}} \ge 70$ disparan el estado **`CRITICAL LTB REQUIRED`** y ordenan congelar de inmediato el $ROP$ automático del ERP.

### 2.3 Derivación Financiera: Last Time Buy (LTB) vs. Rediseño Form-Fit-Function (FFF)

Una vez congelado el $ROP$, el CFO necesita comparar el coste financiero completo de comprar de una sola vez todo el horizonte comercial remanente ($H_{\text{meses}}$) frente a invertir en ingeniería para sustituir el componente en placa ($NRE$ + recertificación regulatoria):

1. **Colchón Puente Único ($SS_{\text{LTB}}$) y Volumen Total a Comprar ($Q_{\text{LTB}}$):**
   A diferencia de un stock mensual, en un LTB no habrá segundas oportunidades de pedido; la incertidumbre acumulada de demanda escala con la raíz cuadrada del horizonte total ($H_{\text{meses}}$):

$$
SS_{\text{LTB}} = \left\lceil Z \cdot \sigma_m \cdot \sqrt{H_{\text{meses}}} \right\rceil \quad \Longrightarrow \quad Q_{\text{LTB}} = \left\lceil H_{\text{meses}} \cdot D_m + SS_{\text{LTB}} \right\rceil
$$

2. **Coste Financiero Total del Last Time Buy ($C_{\text{LTB}}$):**
   Incluye el desembolso inicial en factura ($Q_{\text{LTB}} \cdot P_{\text{LTB}}$) más el coste de oportunidad de capital (**WACC**) y las tasas de almacenaje, seguro y merma ($h$) calculados sobre el inventario promedio mantenido durante el horizonte ($H_{\text{meses}} / 24$ años):

$$
C_{\text{LTB}} = \left(Q_{\text{LTB}} \cdot P_{\text{LTB}}\right) \cdot \left[ 1 + \left(\text{WACC} + h\right) \cdot \frac{H_{\text{meses}}}{24} \right]
$$

3. **Coste Total del Rediseño FFF ($C_{\text{FFF}}$) y Punto de Equilibrio Temporal ($T^*$):**
   Incorpora el coste fijo de ingeniería no recurrente ($\text{NRE}$), la recertificación normativa y el riesgo de retraso durante los meses de transición:

$$
C_{\text{FFF}} = \text{NRE} + \text{Recertificación} + \text{Riesgo\_Transición} \quad \Longrightarrow \quad T^* = \frac{\text{NRE} + \text{Recertificación}}{D_m \cdot P_{\text{LTB}} \cdot \left(1 + 0,5 \cdot (\text{WACC} + h)\right)}
$$

El algoritmo emite un veredicto con banda de indiferencia del $\pm 8\%$:
- Si $C_{\text{LTB}} \le 0,92 \cdot C_{\text{FFF}}$: **`EXECUTE LTB`** (típico en dispositivos médicos o aeroespaciales con recertificación costosa).
- Si $C_{\text{FFF}} \le 0,92 \cdot C_{\text{LTB}}$: **`REDESIGN FFF`** (equipos flagship de alto volumen y horizonte $> 36$ meses).
- Si ambos costes difieren menos de un 8%: **`HYBRID BRIDGE`** (LTB táctico de 12 meses mientras ingeniería homologa la placa revisada).

#### Caso Práctico Auditado: Discontinuación de `TI-CAP-10U-50` en `DRONE-X1-PRO`

Supongamos que llega un aviso EOL sobre el condensador crítico `TI-CAP-10U-50` ($D_m = 400\text{ uds/mes}$, $\sigma_m = 65$, precio unitario LTB $P_{\text{LTB}} = 1,85\text{ €}$, horizonte restante $H = 24\text{ meses}$, nivel de servicio puente $Z = 1,96$ al $97,5\%$, $\text{WACC} + h = 18\%$, ingeniería $\text{NRE} = 28.000\text{ €}$ y recertificación $9.500\text{ €}$):

1. **Colchón puente único tras congelar el ROP:** $SS_{\text{LTB}} = \lceil 1,96 \cdot 65 \cdot \sqrt{24} \rceil = 624\text{ uds}$, elevando la orden total a $Q_{\text{LTB}} = 24 \cdot 400 + 624 = 10.224\text{ uds}$.
2. **Desembolso CAPEX e impacto financiero LTB:** La factura inmediata asciende a $18.914,40\text{ €}$ más $3.404,59\text{ €}$ de coste financiero WACC/almacenaje, arrojando un coste económico total $C_{\text{LTB}} = 22.318,99\text{ €}$.
3. **Alternativa Rediseño FFF:** Frente a los $37.500\text{ €}$ fijos de NRE más recertificación (sin contar retrasos en planta), el punto de equilibrio supera los **46 meses**. Veredicto determinista inmediato: **`EXECUTE LTB` con un ahorro neto auditado superior a `15.180 €`**.

---

## 3. Executive Risk Cockpit `v2.0.0`: Arquitectura Zero-CDN (< 34 KB gzip) y Privacidad CSV Local

En la versión anterior (`v1.0`), la interfaz dependía de `cdn.tailwindcss.com` en tiempo de ejecución y presentaba una única vista estática en inglés. Para **Agentic Radar `v2.0.0`** reconstruimos todo el frontend bajo el estándar **Modern Web Guidance** y nuestro preset *Executive Data-Dense*:

- **Cero CDNs Externos & Shell Ultra-Ligero (`33,03 KB` gzipped):** Todo el conjunto de `index.html`, `styles.css`, `i18n.js`, `engine.js`, `app.js`, `manifest.json` y `sw.js` se compila y verifica determinísticamente desde `apps/obs-management/web/` hacia `static/apps/obs-management/`. Sin dependencias de terceros, con tipografía `tabular-nums`, toggle Dark/Light con sincronización automática de `<meta name="color-scheme">` y cumplimiento estricto WCAG 2.2 AA (`<= 60 px` de altura de cabecera).
- **PWA Instalable 100 % Offline:** Incorpora manifiesto con iconos vectoriales `SVG` y PNGs `any`/`maskable` (safe zone del 80 %), además de un Service Worker **Network-First** que garantiza disponibilidad continua en plantas industriales sin cobertura.
- **Bilingüismo Nativo 100 % ES/EN (`?lang=es|en`):** Traduce KPIs, monedas (`33.850,00 €` vs `€33,850.00`), etiquetas SVG, veredictos financieros, rutas de catálogo y tarjetas exportables **PNG `1200×630`** generadas en cliente mediante Canvas API.
- **Importador CSV BOM 100 % Privado en Navegador (`<dialog>`):** Ninguna lista de materiales es un documento público; los fabricantes protegen su estructura de costes como secreto industrial. Por ello, el importador RFC-4180 procesa tu archivo `.csv` **exclusivamente en memoria RAM del navegador**, sin enviar un solo byte a servidores externos, e incluye un botón **`Probar con BOM de ejemplo (1 clic)`** y descarga de plantilla.

---

## 4. Seguridad Multi-Tenant y Defensa Backend: Esquema `obs_radar` con RLS Real

Para organizaciones que desean conectar la interfaz con una base de datos corporativa propia e ingesta automática de correos y webhooks de distribuidores, el backend en `apps/obs-management/api/` ha sido refactorizado bajo tolerancia cero a vulnerabilidades:

```sql
CREATE SCHEMA IF NOT EXISTS obs_radar;

-- Ejemplo de aislamiento estricto por usuario en las 6 tablas relacionales
ALTER TABLE obs_radar.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.internal_parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.bom_lines ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.aml ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.manufacturer_parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.eol_alerts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation_products" ON obs_radar.products
  FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
```

Además, la nueva API unificada FastAPI (`main.py` + `models.py` Pydantic v2) añade cuatro salvaguardas de producción:
1. **Verificación HMAC-SHA256 / Bearer Token (`HTTP 401`):** Ningún webhook externo entra al orquestador sin firma criptográfica válida.
2. **Delimitación anti-Prompt Injection en `obsolescence_agent.py`:** Los correos crudos de fabricantes se encapsulan con etiquetas delimitadoras estrictas y validación Pydantic previa a cualquier consulta SQL.
3. **CORS restringido por `.env` (`ALLOWED_ORIGINS`) y `seeder_guard.py`:** Bloquea cualquier script de siembra sintética sobre cuentas reales de producción.
4. **Paridad matemática verificada en `pytest`:** Nuestra suite automatizada comprueba que `bom_engine.py` en Python y `engine.js` en JavaScript devuelven resultados idénticos por debajo del céntimo de euro ante cualquier escenario o ciclo BOM.

---

## 5. Prueba el Simulador en Vivo y Equipa a tu Comité Directivo

Ya puedes auditar un escenario industrial o cargar tu propia lista de materiales `.csv` de forma 100 % privada en la Web App gratuita **Agentic Radar `v2.0.0`**:

{{< app-ref slug="obs-management" >}}

### El Kit Completo para Comités de Operaciones e Ingeniería (`pack-obs`)

Si quieres desplegar esta metodología directamente en tus hojas corporativas sin macros VBA, defender el CAPEX ante el Consejo con un Playbook normativo IEC 62402 y contar con el Starter Blueprint completo (`obs_radar` SQL RLS + `bom_engine.py` + CSV compatible), el **miércoles 9 de diciembre** abrimos el acceso Early-Bird al nuevo Kit:

{{< product-card
  title="IEC 62402 Obsolescencia, Riesgo BOM & LTB Decision Kit"
  category="Supply Risk & IEC 62402"
  price="19€"
  original_price="39€"
  badge="📡 Lanzamiento 9 Dic • Complemento de pack-stock"
  icon="📡"
  status="coming"
  preview_image="preview-pack.png"
  preview_caption="Vista previa del Kit v2.0: Executive Risk Cockpit + Playbook PDF (5 págs.) + Excel Dual 5 Hojas sin VBA"
  deliverables="Excel Dual 5 Hojas (0 VBA)|Playbook PDF A4 (5 págs.)|Starter Blueprint SQL RLS + Python"
  features="Libro Excel Dual ES/EN sin macros VBA con 5 hojas auditadas (Explorador BOM/AML, Matriz Criticidad IEC 62402, Simulador LTB vs. Rediseño FFF + colchón puente SS_LTB, Hoja de Ruta CAPEX y Dashboard C-Level)|Playbook Ejecutivo PDF vectorial de 5 páginas A4 en Español e Inglés con matriz operativa pack-stock vs. pack-obs|Starter Blueprint Técnico completo: esquema PostgreSQL obs_radar con RLS en 6 tablas, bom_engine.py puro anti-ciclos, modelos Pydantic v2 y plantilla CSV compatible con Agentic Radar v2.0"
  guide_url="/es/apps/obs-management/"
  guide_text="Probar Web App interactiva v2.0"
>}}
Kit B2B diseñado específicamente para resolver **crisis de discontinuación (PCN/PDN/EOL)** tras congelar tu Punto de Pedido recurrente. Incluye el botón de acceso anticipado dentro de la propia Web App (`🚀 Kit IEC 62402 & Modo Pro B2B`).
{{< /product-card >}}

### ¿Buscas Gobernar También el Inventario Recurrente y el Control Operativo?

Recuerda que la resiliencia industrial completa une las dos mitades del ciclo de vida junto a la gestión cuantitativa de riesgos:

* **📦 Para el flujo continuo en Fase de Madurez:** Dimensiona tus colchones estadísticos ($SS_3$), Punto de Pedido ($ROP$) y Lote de Wilson ($EOQ$) con nuestra [Calculadora de Stock de Seguridad & ROP (`pack-stock` · 7 €)](/es/posts/calculadora-stock-seguridad-rop/) o descárgala directamente vía [Checkout Seguro Lemon Squeezy (7 €)](https://datalaria.lemonsqueezy.com/checkout/buy/513e5cad-9f9f-4b53-a435-b511a846d79e?embed=1).
* **🛡️ Para blindar fallos operativos de proveedores *Single-Source*:** Prioriza riesgos por Severidad, Ocurrencia y Detección (NPR) con el [Pack Matriz de Riesgos & AMFE / FMEA (`pack-amfe` · 7 €)](https://datalaria.lemonsqueezy.com/checkout/buy/6eea6aa0-fe9f-440b-8bb9-6f29b303e57a?embed=1).
* **🏛️ Para todo el sistema de Control Operativo (5 Kits, ahorro 35 %):** Accede a RACI, AMFE, PERT, EVM Curva S y Stock de Seguridad/ROP en la [Suite 03: Control Operativo PMBOK (22 €)](https://datalaria.lemonsqueezy.com/checkout/buy/ee578b8e-29d6-4361-ba19-4b0b5abfd89a?embed=1), documentada en el [Framework Integral de 5 Pilares](/es/posts/control-operativo-pmbok-framework-cuantitativo/).
