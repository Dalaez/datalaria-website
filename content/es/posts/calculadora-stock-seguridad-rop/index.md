---
title: "Calculadora de Stock de Seguridad & ROP: Optimización de Inventario y Working Capital de Grado Consejo de Administración"
date: 2026-11-26
draft: false
translationKey: "safety-stock-reorder-point-calculator"
category: "Estrategia y Operaciones"
categories: ["Control Operativo", "Supply Chain", "Plantillas Ejecutivas", "Estrategia y Operaciones"]
tags: ["Stock de Seguridad", "Punto de Pedido", "ROP", "Safety Stock", "EOQ", "Wilson", "Working Capital", "Cadena de Suministro", "APICS", "ASCM", "Inventario", "C-Level"]
description: "Guía cuantitativa y metodológica de optimización de inventarios (APICS / ASCM / MIT CTL & IEC 62402): erradicación de reglas empíricas de 3 semanas, ciclo de vida de componentes (PCN, PDN, LTB, EOL), convolución estocástica de demanda y Lead Time, dimensionamiento ROP y Wilson EOQ y liberación de capital de trabajo."
summary: "Erradica las destructivas reglas empíricas en la gestión de inventario. Descubre cómo calcular con rigor matemático el Stock de Seguridad (SS), el Punto de Pedido (ROP) y el Lote Económico (EOQ) integrando el ciclo de vida de componentes (PCN, PDN, LTB, EOL) y la variabilidad estocástica, blindando el Nivel de Servicio al 98% y liberando liquidez inmovilizada."
cover:
  image: "cover.png"
  alt: "Calculadora de Stock de Seguridad & Punto de Pedido (ROP): Optimización de Inventario y Working Capital C-Level"
  caption: "Calculadora de Stock de Seguridad & ROP (Estándar APICS / ASCM & MIT CTL): convolución estocástica de demanda y Lead Time, ciclo Diente de Sierra, Lote Wilson EOQ y liberación de Capital de Trabajo."
  relative: true
images:
  - "cover.png"
  - "preview-pack.png"
  - "diagrama-1-ciclo-vida-iec62402.png"
  - "diagrama-2-pipeline-control-stock-clevel.png"
  - "diagrama-3-dinamica-diente-sierra-sawtooth.png"
---

En comités de dirección ejecutiva (*Executive Committee*), consejos de administración y comités de tesorería, directores generales (CEOs), directores financieros (CFOs), directores de operaciones (COOs) y directores de compras presencian con exasperante regularidad uno de los conflictos organizativos y financieros más destructivos del mundo corporativo: **la guerra civil entre el departamento comercial y el departamento financiero en torno a los niveles de inventario**.

Por un lado, el Director Comercial y de Ventas comparece ante el Consejo denunciando que la compañía pierde cuota de mercado, deteriora su reputación y sufre penalizaciones de grandes cuentas porque la tasa de rotura de stock (*stockout rate*) ha alcanzado un insostenible 7% en las referencias más demandadas:

> *"Nuestros clientes no pueden esperar tres semanas por un producto estrella. Si no tenemos disponibilidad inmediata en el almacén, se van a la competencia en un clic. Necesitamos incrementar urgentemente los colchones de seguridad para tener todo disponible al 100%."*

Por otro lado, el Director Financiero (CFO) exhibe el balance de situación con alarma indisimulada: el capital circulante (*working capital*) se encuentra estrangulado, las líneas de crédito bancario están al límite de su capacidad y la cuenta de resultados arrastra un sangrado continuo en costes de posesión, obsolescencia, primas de seguros y deterioro físico:

> *"Tenemos más de 4.500.000 € inmovilizados en existencias. Los almacenes centrales están colapsados y la rentabilidad sobre el capital empleado (ROCE) se ha desplomado tres puntos. La consigna para el próximo trimestre es recortar un 20% el inventario de forma lineal en todas las familias de producto."*

Ante esta encrucijada, surge la pregunta crítica que todo Consejo de Administración debe formular: **¿cómo es posible que una empresa tenga millones de euros atrapados en sobrestock acumulando polvo y, simultáneamente, sufra roturas de stock cotidianas en sus referencias más críticas?**

La respuesta es técnica, rigurosa y demoledora: **la compañía está gestionando su cadena de suministro mediante reglas empíricas arbitrarias (*rules of thumb*) en lugar de aplicar modelos estocásticos probabilísticos**.

Cuando una organización gestiona su inventario aplicando axiomas informales —como la clásica regla de *"mantener 3 semanas de stock de seguridad para todo el catálogo"* o *"pedir un mes de consumo medio"*—, el desastre financiero y operativo es una certeza matemática. Tratar a un microcontrolador importado de Taiwán con 45 días de plazo y alta volatilidad bajo la misma heurística que a una caja de embalaje con entrega garantizada en 48 horas garantiza el peor de los mundos: **sobre-almacenamiento masivo en productos estables e infradotación crítica en referencias volátiles**.

Para erradicar este punto ciego, los estándares globales de **APICS / ASCM (Association for Supply Chain Management)** y los marcos cuantitativos del **MIT Center for Transportation & Logistics** formalizan el modelo estocástico de **Stock de Seguridad ($SS$)**, **Punto de Pedido ($ROP$)** y **Lote Económico de Pedido ($EOQ$)**. 

En esta guía metodológica desglosamos qué es la herramienta y el impacto del ciclo de vida de los componentes (`PCN`, `PDN`, `LTB`, `EOL`), la arquitectura cuantitativa completa, la derivación de los tres modelos de convolución, la dinámica cartesiana del gráfico Diente de Sierra (*Sawtooth*), la frontera de rendimientos decrecientes en el Nivel de Servicio y el protocolo de gobernanza para defender ante el Consejo de Administración un plan de liberación de liquidez inmediata.

{{< product-card
  variant="compact"
  title="Executive Decision Pack: Calculadora de Stock de Seguridad & ROP"
  price="7€"
  original_price="22€"
  badge="📦 Estándar APICS / ASCM & MIT CTL"
  icon="📦"
  checkout_url="https://datalaria.lemonsqueezy.com/checkout/buy/513e5cad-9f9f-4b53-a435-b511a846d79e"
  button_text="Descargar Kit Ahora (.ZIP) • 7€"
>}}
¿Necesitas defender ante el CEO o el CFO cuánto inventario real necesita tu catálogo sin sufrir roturas ni inmovilizar liquidez? Descarga el motor estocástico en Excel (35 SKUs, convolución integral SS₃, ROP, EOQ de Wilson, Diente de Sierra interactivo y simulador de Working Capital), la guía metodológica PDF de 5 páginas y la presentación ejecutiva 16:9.
{{< /product-card >}}

---

## 1. ¿Qué es la Calculadora de Stock de Seguridad & Punto de Pedido (ROP)? Fundamentos, Ciclo de Vida de Componentes y Objetivos

Para cualquier Director de Operaciones (COO), Director Financiero (CFO), Responsable de Compras, Planificador de S&OP o lector que se aproxime por primera vez a la ingeniería cuantitativa de inventarios, la **Calculadora de Stock de Seguridad ($SS$) & Punto de Pedido ($ROP$)** sustituye la intuición subjetiva de almacén por un **sistema de control estocástico y financiero de revisión continua $(s, Q)$**.

Mientras la gestión artesanal responde *"por experiencia, ten 3 semanas de todo"*, este motor responde con precisión matemática auditada a tres preguntas directivas críticas para cada referencia ($SKU$) o componente de la lista de materiales (*Bill of Materials* — BOM):

1. **¿Cuándo debemos emitir un pedido de reposición? (*Reorder Point* — $ROP$):** Umbral exacto de unidades disponibles que dispara automáticamente la orden de compra en el ERP para cubrir el consumo esperado durante el plazo del proveedor más la incertidumbre estocástica.
2. **¿Qué colchón de protección mínimo debemos mantener? (*Safety Stock* — $SS$):** Reserva técnica calculada mediante la función cuantil normal $Z = \Phi^{-1}(CSL)$ para absorber picos inesperados de demanda ($\sigma_d$) y retrasos del proveedor ($\sigma_L$) con una probabilidad de servicio garantizada.
3. **¿Cuál es el tamaño de lote óptimo? (*Economic Order Quantity* — $EOQ$):** Volumen exacto que equilibra el coste administrativo fijo por pedido ($S$) con el coste financiero anual de posesión, almacenamiento y riesgo de obsolescencia ($h \cdot C$).

### 1.1 Conceptos Rectores del Control de Inventario y del Ciclo de Vida de un Componente (APICS & IEC 62402)

Un error habitual en la industria consiste en tratar los modelos matemáticos $(ROP, EOQ)$ como fórmulas estáticas válidas durante toda la vida de un producto. En electrónica, automoción, maquinaria y manufactura avanzada, el modelo cuantitativo de inventarios está intrínsecamente acoplado al **ciclo de vida físico de cada componente** regulado por los estándares internacionales **UNE-EN IEC 62402:2019** y **JEDEC (J-STD-046 / J-STD-048)**:

{{< mermaid image="diagrama-1-ciclo-vida-iec62402.png" alt="Modelo de Ciclo de Vida del Componente y Gobernanza de Obsolescencia (Estándar IEC 62402 / JEDEC)" >}}
flowchart LR
    L1["<b>1. Introducción</b><br/><small>Demanda incipiente<br/>Alta incertidumbre σd</small>"] --> L2["<b>2. Crecimiento</b><br/><small>Escalado exponencial<br/>Revisión semanal ROP</small>"]
    L2 --> L3["<b>3. Madurez</b><br/><small>Fase estacionaria óptima<br/>Modelo completo SS3 + EOQ</small>"]
    L3 --> L4["<b>4. Declive y PCN</b><br/><small>Cambios de diseño o proceso<br/>Alerta temprana de consumo</small>"]
    L4 --> L5["<b>5. PDN, LTB y EOL</b><br/><small>Última Compra Posible<br/>Suspensión del ROP hacia LTB</small>"]
    L5 --> L6["<b>6. Obsoleto</b><br/><small>Fin de fabricación<br/>Evitar Dead Stock o mercado gris</small>"]

    style L1 fill:#EFF6FF,stroke:#3B82F6,color:#1E3A8A
    style L2 fill:#ECFDF5,stroke:#10B981,color:#065F46
    style L3 fill:#0F172A,stroke:#2563EB,color:#FFFFFF
    style L4 fill:#FEF3C7,stroke:#F59E0B,color:#92400E
    style L5 fill:#FEE2E2,stroke:#DC2626,color:#991B1B
    style L6 fill:#1E293B,stroke:#64748B,color:#F8FAFC
{{< /mermaid >}}

Dominar la transición entre la política estadística normal y las alertas técnicas de ciclo de vida exige manejar seis conceptos clave:

* **Ciclo de Vida de un Componente (*Component Lifecycle*):** Curva sigmoidal que atraviesa todo número de parte (*MPN* — *Manufacturer Part Number*), desde su lanzamiento comercial (*Introducción* y *Crecimiento*), pasando por su estabilidad productiva (*Madurez*, donde el modelo $SS_3, ROP, EOQ$ opera a pleno rendimiento), hasta su *Declive*, fase de retirada (*Phase-Out*) y eventual *Obsolescencia*. Un microcontrolador *COTS* de consumo puede completar todo este ciclo en 24 meses, mientras que un componente automotriz *AEC-Q100* o *Mil-Spec* supera los 10 años.
* **PCN (*Product Change Notification* — Estándar JEDEC J-STD-046):** Notificación formal emitida por un fabricante cuando modifica un aspecto técnico, de fabricación, encapsulado, planta de silicio o especificaciones de un componente activo. Aunque no implica discontinuación inmediata, un **PCN** puede alterar el tiempo de homologación y revalidación técnica (*Form, Fit, Function* — FFF), elevando temporalmente el *Lead Time* efectivo ($L$) y exigiendo incrementar el **Stock de Seguridad ($SS$)** como puente de validación en ingeniería.
* **PDN (*Product Discontinuance Notice* — Estándar JEDEC J-STD-048):** Aviso formal e irrevocable de cese próximo de fabricación emitido por el productor. Es el disparador temprano que indica al departamento de Compras e Ingeniería que la referencia abandona la etapa de madurez y entra en cuenta atrás de extinción. Ignorar un **PDN** mientras el ERP sigue calculando el $ROP$ con parámetros estacionarios garantiza una rotura de producción catastrófica.
* **LTB (*Last Time Buy* — Última Compra Posible):** Ventana temporal crítica (típicamente de 30 a 90 días desde el PDN) durante la cual el fabricante acepta la última orden de compra en firme antes de cerrar la línea de fabricación. En el momento en que se activa un **LTB**, la organización debe **suspender el cálculo automático recurrente de $ROP$ y $EOQ$ de Wilson** para sustituirlo por un modelo de **compra estratégica puente (*Bridge Buy* / *All-Time Buy*)**: se adquiere en una única orden consolidada el volumen necesario para cubrir el consumo restante de los ensamblajes en catálogo, contratos *SLA* firmados y stock de posventa/garantías mientras I+D homologa un reemplazo.
* **EOL (*End of Life* — Fin de Vida Útil):** Fecha o estatus formal que marca el final de la disponibilidad comercial regular de un componente y el cese del soporte estándar por parte del fabricante original. A partir del hito **EOL** (con su fecha límite asociada de último envío o *Last Time Ship* — **LTS**), cualquier necesidad imprevista no cubierta por el **LTB** obliga a acudir a *brokers* en el mercado secundario gris con sobrecostes de $5\times$ a $10\times$ y riesgo severo de falsificación.
* **Componente Obsoleto (*Obsolete*) y Gestión de Stock Muerto (*Dead Stock*):** Estatus terminal en el que la referencia ya no se fabrica ni cuenta con existencias oficiales en canales autorizados. El acoplamiento directo entre la ingeniería de obsolescencia (**IEC 62402**) y el control de inventarios cumple una doble función financiera crítica:
  1. Evitar que el ERP emita pedidos automáticos por $ROP$ de piezas obsoletas o desalineadas de producto acabado en declive (generando **Stock Obsoleto / Muerto — *Dead Stock*** cuyo coste contable hay que deteriorar al 100%).
  2. Incorporar explícitamente la prima de riesgo tecnológico y de obsolescencia dentro de la **tasa anual de mantenimiento de inventario ($h\%$)** —por ejemplo, pasando del $18\%$ en tornillería estándar al $25\%\text{–}30\%$ en semiconductores de ciclo corto—, evitando así que el $EOQ$ sugiera lotes gigantescos de referencias expuestas a una discontinuación inminente.

#### Sinergia Operativa: Gobierno Dinámico `(SS, ROP, EOQ)` + Radar Temprano de Obsolescencia

En la práctica industrial, un motor de inventario es tan seguro como los datos de ciclo de vida que lo alimentan. Mientras la **Calculadora Excel de Stock de Seguridad & ROP** gobierna el cálculo cuantitativo del colchón estocástico ($SS_3$), el umbral de reposición ($ROP$) y el lote óptimo ($EOQ$) durante toda la fase de **Madurez**, el **Radar de Obsolescencia (*Agentic Radar*)** actúa como sistema de alerta temprana conectado a los avisos **PCN/PDN** de fabricantes y a tu estructura **BOM** (*Bill of Materials*). En cuanto detecta una discontinuación inminente (`CRITICAL LTB REQUIRED`), cuantifica el margen en riesgo y avisa a Compras para **congelar el parámetro $ROP$ recurrente** y transicionar hacia una compra puente **LTB**, evitando roturas de línea y acumulación de *Dead Stock*:

{{< app-ref slug="obs-management" >}}

### 1.2 Los Cuatro Objetivos Estratégicos ante el Consejo de Administración

Adoptar un motor cuantitativo de Stock de Seguridad & ROP frente a las reglas empíricas de almacén persigue cuatro objetivos ejecutivos verificables:

1. **Erradicar simultáneamente la escasez crítica y el sobrestock inmovilizado:** Sustituir reglas homogéneas de *"3 semanas de cobertura"* por una modelización asimétrica que blinde las referencias volátiles de alto margen y recorte los excesos acumulados en artículos estables.
2. **Alinear el Nivel de Servicio ($CSL$) con el margen Pareto (ABC) y el ciclo de vida:** Invertir capital exclusivamente donde protege la facturación (98%–99% en Clase A) y modular el reabastecimiento cuando existan avisos **PCN**, **PDN** o ventanas **LTB**.
3. **Liberar liquidez neta al balance (*Working Capital Harvesting*):** Cuantificar al euro el capital circulante innecesariamente atrapado en existencias ociosas y acelerar las rotaciones de inventario (*Inventory Turns*) y el *ROCE*.
4. **Convertir las negociaciones con proveedores en retorno financiero directo:** Demostrar ante Compras que reducir la impuntualidad del proveedor ($\sigma_L$) o su plazo medio ($L$) mediante acuerdos SLA libera mucha más caja que exigir descuentos marginales en tarifa unitaria.

### 1.3 Gestión de Inventario Tradicional vs. Motor Estocástico Datalaria (APICS / MIT CTL & IEC 62402)

| Dimensión de Gobierno | Gestión Empírica Tradicional (*Rules of Thumb*) | Motor Estocástico Datalaria (APICS & IEC 62402) | Ventaja Estratégica C-Level |
| :--- | :--- | :--- | :--- |
| **Criterio de cobertura** | Heurística arbitraria uniforme ("tener siempre 3 semanas o 1 mes de venta"). | **Convolución estocástica multivariante ($SS_3$)** por SKU con demanda y plazo variables. | Elimina el sobrestock crónico en Clase C y las roturas en Clase A importadas. |
| **Gestión de fiabilidad logística** | Asume que el proveedor entrega exactamente en el plazo contractual teórico. | **Cuantifica $\sigma_L$ ponderado por $d^2$**: penaliza a proveedores erráticos e impuntuales. | Prioriza acuerdos SLA en compras donde mayor liquidez neta liberan. |
| **Tamaño de lote de compra** | Pedidos intuitivos o por lotes mínimos comerciales sin análisis financiero. | **Lote Económico de Wilson ($EOQ$)** equilibrando coste fijo de emisión ($S$) y posesión ($h \cdot C$). | Minimiza el coste total anual de aprovisionamiento y almacenamiento. |
| **Acoplamiento al ciclo de vida** | El ERP sigue lanzando órdenes por $ROP$ sin distinguir si hay un **PDN / EOL**. | **Integración con eventos PCN, PDN, LTB y EOL** ajustando $h\%$ o activando compra puente. | Previene paradas de línea ante LTB y evita acumulación de **Dead Stock obsoleto**. |
| **Frontera Nivel de Servicio** | Exigencia emocional de *"disponibilidad del 100% en todo el catálogo"*. | **Curva asintótica $CSL$ (85%–99,9%)** y asignación asimétrica **ABC** (98% / 95% / 90%). | Evita duplicar la deuda corporativa persiguiendo el último 0,5% sin retorno. |
| **Entregable para Comité** | Tablas desconectadas imposibles de defender ante Dirección Financiera. | **Pack Completo:** Excel 4 pestañas ECMA-376, Deck 16:9 Minto y Guía PDF de 5 págs. | Defensa inmediata ante CEO, CFO y COO en Comités de Supply Chain y S&OP. |

### 1.4 El Embudo Estratégico-Operativo en Datalaria (Conexión con Artículos Previos)

La gestión cuantitativa del Stock de Seguridad & ROP constituye el **Pilar 5 de la Suite 03 (Control Operativo & PMBOK)** y dialoga directamente con la **Ingeniería de la Obsolescencia (IEC 62402)** dentro de la arquitectura integral de Datalaria:

* **Capa 1 · Estrategia Corporativa y Cartera (Suite 01):** Antes de dimensionar cadenas de suministro o almacenes, la alta dirección selecciona mercados y unidades de negocio mediante la [Matriz PESTEL Cuantitativa](/es/posts/matriz-pestel-cuantitativa/) (riesgos geopolíticos, aranceles y disrupciones logísticas globales), las [5 Fuerzas de Porter Ponderadas](/es/posts/5-fuerzas-porter-cuantitativas/) (poder negociador de proveedores), el [DAFO Cuantitativo y Matriz CAME](/es/posts/dafo-cuantitativo-matriz-came/), la [Matriz BCG Dinámica](/es/posts/matriz-bcg-dinamica/) y la [Matriz McKinsey / GE 3x3](/es/posts/matriz-mckinsey-ge/), integradas en el [Framework Integral de Estrategia Corporativa MBA](/es/posts/estrategia-corporativa-mba-framework-cuantitativo/).
* **Capa 2 · Decisión Racional, Priorización y Viabilidad de Capital (Suite 02):** Las inversiones industriales y expansiones de capacidad superan criterios veto (*Dual-sourcing*, continuidad de suministro) en la [Matriz DAR Cuantitativa](/es/posts/matriz-dar-cuantitativa/), priorizan iniciativas operativas en la [Matriz RICE & ICE de Priorización Ágil](/es/posts/matriz-rice-ice-priorizacion/) y demuestran rentabilidad financiera ajustada por la variación del capital circulante ($\Delta\text{NWC}$) en el [Business Case Financiero (VAN, TIR y Payback)](/es/posts/business-case-financiero-van-tir/), vertebrados en el [Framework de Toma de Decisiones Racional y Priorización](/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/).
* **Capa 3 · Control Operativo PMBOK e Ingeniería de la Obsolescencia (Suite 03 & IEC 62402):** En ejecución, la [Matriz RACI Cuantitativa y Balance de Carga](/es/posts/matriz-raci-balance-carga/) asigna responsables únicos de compras e inventario; la [Matriz de Riesgos Cuantitativa & AMFE / FMEA (NPR)](/es/posts/matriz-riesgos-amfe-fmea/) cuantifica el impacto financiero de los cortes de suministro *single-source*; la [Estimación PERT de 3 Puntos Estocástica](/es/posts/estimacion-pert-3-puntos/) modela la incertidumbre temporal de rutas críticas; y el [Cuadro de Mando EVM (Valor Ganado y Curva S)](/es/posts/cuadro-mando-evm-valor-ganado/) audita en vivo que el coste real ($AC$) no erosione el presupuesto. En paralelo, para anticipar alertas **PCN, PDN, LTB y EOL** de fabricantes en listas de materiales complejas, este modelo enlaza con nuestra serie de [El Ajedrez de la Obsolescencia (IEC 62402)](/es/posts/obs_parte1_intro/), [El Arsenal Táctico de Componentes (COTS, Mil-Spec, PCN/PDN)](/es/posts/obs_parte2_tactica/) y la aplicación en vivo [Radar de Obsolescencia](/es/apps/obs-management/).

---

## 2. El Pipeline de Planificación y Control de Stocks de Grado C-Level

El control de inventario de clase mundial no es un ejercicio reactivo de aprovisionamiento; es un **sistema de ingeniería operativa y tesorería predictiva** que conecta la volatilidad del cliente, la fiabilidad del proveedor y la estructura de capital de la compañía:

{{< mermaid image="diagrama-2-pipeline-control-stock-clevel.png" alt="Pipeline C-Level de Planificación, Valoración y Control de Inventarios (Estándar APICS / ASCM)" >}}
flowchart TD
    A["<b>1. Segmentación Estratégica ABC</b><br/><small>Clasificación de Pareto por valor de consumo y margen<br/>Asignación formal de Nivel de Servicio Objetivo CSL</small>"]
    
    B["<b>2. Captura Estocástica de la Demanda</b><br/><small>Cálculo de la demanda media diaria d<br/>Cálculo de la desviación estándar del consumo σd</small>"]
    
    C["<b>3. Auditoría de Fiabilidad del Proveedor</b><br/><small>Plazo medio de entrega en días L<br/>Desviación estándar de impuntualidad logística σL</small>"]
    
    D["<b>4. Motor de Convolución Estocástica SS</b><br/><small>Cálculo del Factor Z según CSL: Z = Φ⁻¹ de CSL<br/>SS = Z · √ de L·σd² + d²·σL²</small>"]
    
    E["<b>5. Calibración del Punto de Pedido ROP</b><br/><small>Demanda durante el Lead Time: LTD = d · L<br/>ROP = LTD + SS, Umbral de disparo ERP</small>"]
    
    F["<b>6. Dimensionamiento del Lote Óptimo EOQ</b><br/><small>Equilibrio entre coste de pedido S y posesión h·C<br/>EOQ = √ de 2·D·S entre h·C</small>"]
    
    G{"<b>7. Auditoría de Capital de Trabajo</b><br/><small>¿Existe sobrestock frente a la heurística previa?<br/>Cuantificación de liquidez neta liberable en EUR</small>"}
    
    H["<b>PLAN DE DESINVERSIÓN INMEDIATA</b><br/><small>Consumo natural de excedentes no críticos<br/>Liberación de caja para reforzar líneas Clase A</small>"]
    
    I["<b>8. Board Decision Gateway</b><br/><small>Aprobación formal de la política por CEO, CFO y COO<br/>Integración de SLAs con penalizaciones a proveedores</small>"]

    A --> B
    A --> C
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    G -->|"Exceso de Stock"| H
    G -->|"Inventario Optimizado"| I
    H --> I
{{< /mermaid >}}

---

## 3. La Dinámica Operativa del Ciclo Diente de Sierra (*Sawtooth Model*)

El modelo de revisión continua $(s, Q)$ o $(ROP, EOQ)$ se fundamenta en la dinámica del gráfico en **Diente de Sierra (*Sawtooth Chart*)**, que describe con precisión matemática el flujo físico y financiero del almacén a lo largo del tiempo:

{{< mermaid image="diagrama-3-dinamica-diente-sierra-sawtooth.png" alt="Dinámica en Diente de Sierra (Sawtooth Chart) y Flujo del Ciclo de Reposición Continua" >}}
flowchart TD
    S1["<b>Fase 1: Entrada de Lote +EOQ</b><br/><small>Inventario disponible alcanza su pico: Stock Máximo = SS + EOQ<br/>Consumo comercial a tasa diaria promedio d</small>"]
    
    S2["<b>Fase 2: Consumo y Descenso Lineal</b><br/><small>El inventario desciende con pendiente -d<br/>El colchón de seguridad SS permanece intocado en la base</small>"]
    
    S3{"<b>Fase 3: Cruce del Umbral ROP</b><br/><small>¿Inventario disponible ≤ ROP?<br/>ROP = d · L + SS</small>"}
    
    S4["<b>Fase 4: Emisión de la Orden de Compra</b><br/><small>El ERP emite automáticamente un pedido por tamaño EOQ<br/>Se inicia la ventana crítica de Lead Time de L días</small>"]
    
    S5["<b>Fase 5: Tránsito Logístico y Riesgo Estocástico</b><br/><small>Durante los L días se consumen d · L unidades<br/>Si la demanda se dispara o el proveedor se retrasa, el SS absorbe el choque</small>"]
    
    S6["<b>Fase 6: Recepción y Sincronización</b><br/><small>El lote llega cuando el inventario roza el colchón basal SS<br/>El stock salta instantáneamente de nuevo a SS + EOQ</small>"]

    S1 --> S2
    S2 --> S3
    S3 -->|"Sí: Disparo ROP"| S4
    S4 --> S5
    S5 --> S6
    S6 --> S1
{{< /mermaid >}}

En condiciones ideales y promedio, el pedido nuevo llega al almacén en el milisegundo exacto en que el inventario disponible desciende hasta el nivel basal del **Stock de Seguridad ($SS$)**. El stock nunca debería descender por debajo de $SS$ a menos que se materialice un evento estocástico adverso:
1. Que los clientes demanden más unidades de las previstas durante el plazo de entrega ($\text{Demanda Real} > d \cdot L$).
2. Que el transportista o el proveedor sufra una disrupción operativa y tarde más días de los pactados ($\text{Plazo Real} > L$).

El $SS$ actúa como el **amortiguador basal de absorción de varianza**. Quienes carecen de un modelo cuantitativo confunden el inventario de ciclo ($\frac{EOQ}{2}$) con el inventario de seguridad ($SS$), provocando que compras adelante pedidos sin criterio o reduzca pedidos cuando el almacén está lleno, desincronizando por completo el ciclo de reposición.

---

## 4. Fundamentación Matemática y Modelos Estocásticos de Convolución

Para determinar con precisión de grado Consejo el volumen exacto de existencias de seguridad, la literatura científica de operaciones (Silver, Pyke & Thomas; Chopra & Meindl; Simchi-Levi) clasifica el problema en tres modelos según la naturaleza de sus variables aleatorias:

### 4.1. El Factor Z y la Distribución Normal del Nivel de Servicio (CSL)

El **Nivel de Servicio de Ciclo (*Cycle Service Level* - $CSL$)** se define como la probabilidad estadística de que la demanda no supere el inventario disponible durante el plazo de entrega del proveedor:

$$CSL = P(\text{Demanda en Lead Time} \le ROP) = 1 - \alpha$$

Donde $\alpha$ es la probabilidad tolerable de sufrir una rotura de stock en un ciclo determinado. Asumiendo que las desviaciones diarias de demanda siguen una distribución normal centrada en la media, el **Factor de Seguridad $Z$** se obtiene mediante la función cuantil o función inversa de la distribución normal estándar $\Phi(x)$:

$$Z = \Phi^{-1}(CSL) = \Phi^{-1}(1 - \alpha)$$

En entornos corporativos y hojas de cálculo avanzadas, este valor se computa dinámicamente:
- En Microsoft Excel y Google Sheets: `=NORM.S.INV(CSL)` (en versiones de Excel con interfaz en español: `DISTR.NORM.ESTAND.INV(CSL)`).
- Para un $CSL = 90,0\% \implies Z \approx 1,2816$
- Para un $CSL = 95,0\% \implies Z \approx 1,6449$
- Para un $CSL = 98,0\% \implies Z \approx 2,0537$
- Para un $CSL = 99,0\% \implies Z \approx 2,3263$
- Para un $CSL = 99,5\% \implies Z \approx 2,5758$
- Para un $CSL = 99,9\% \implies Z \approx 3,0902$

---

### 4.2. Modelo 1: Demanda Variable y Lead Time Determinista (Constante)

Este modelo es aplicable cuando la demanda del cliente fluctúa de forma aleatoria con desviación estándar diaria $\sigma_d$, pero el proveedor o la planta interna entrega con puntualidad absoluta en un plazo fijo de $L$ días ($\sigma_L = 0$):

Dado que la varianza de la suma de $L$ variables aleatorias normales independientes es $\sigma_{LTD}^2 = L \cdot \sigma_d^2$, la desviación estándar durante el Lead Time es $\sigma_{LTD} = \sigma_d \sqrt{L}$. Por consiguiente:

$$SS_1 = Z \cdot \sigma_d \cdot \sqrt{L}$$

*Caso típico de uso:* Proveedores locales con entrega JIT garantizada bajo contrato de transporte cautivo o fabricación en centros de mecanizado propios con colas controladas.

---

### 4.3. Modelo 2: Demanda Determinista (Fija) y Lead Time Variable

Este modelo asume que el ritmo de consumo es constante y perfectamente predecible ($d$ unidades por día, $\sigma_d = 0$), pero el proveedor presenta una dispersión logística notable en sus entregas, con plazo medio $L$ y desviación estándar $\sigma_L$ días:

La variabilidad total del inventario durante la espera se debe exclusivamente a los días de retraso del proveedor. La desviación estándar acumulada en unidades es $\sigma_{LTD} = d \cdot \sigma_L$. En consecuencia:

$$SS_2 = Z \cdot d \cdot \sigma_L$$

*Caso típico de uso:* Líneas de montaje industrial cautivas con cadencia de producción rígida alimentadas por proveedores transoceánicos con congestión portuaria o trámites aduaneros impredecibles.

---

### 4.4. Modelo 3: Modelo Integral de Convolución Estocástica (Demanda Variable Y Lead Time Variable)

En el mundo real de la distribución comercial, el gran consumo, la industria farmacéutica y el eCommerce, **tanto la demanda de los clientes como la puntualidad del proveedor son variables aleatorias independientes**. 

Para derivar la desviación estándar combinada de la demanda durante el plazo de entrega ($\sigma_{DL}$), se aplica la ley de la varianza total (teorema de convolución de dos variables aleatorias independientes):

$$\sigma_{DL}^2 = E[L] \cdot \operatorname{Var}(d) + (E[d])^2 \cdot \operatorname{Var}(L) = L \cdot \sigma_d^2 + d^2 \cdot \sigma_L^2$$

Extrayendo la raíz cuadrada y aplicando el factor de cobertura $Z$, obtenemos la ecuación canónica oficial de Datalaria y del estándar APICS:

$$SS_3 = Z \cdot \sqrt{L \cdot \sigma_d^2 + d^2 \cdot \sigma_L^2}$$

Esta fórmula es el corazón analítico del control de stocks contemporáneo. Nótese un detalle matemático de enorme trascendencia directiva: **la variabilidad del proveedor ($\sigma_L$) aparece ponderada por el cuadrado de la demanda media ($d^2$)**. En productos de gran volumen de ventas, una pequeña impuntualidad del proveedor desestabiliza el inventario con mucha mayor fuerza que una oscilación moderada en la demanda del cliente.

---

### 4.5. Punto de Pedido Óptimo ($ROP$)

Una vez calculado el $SS$, el Punto de Pedido ($ROP$) se establece sumando la demanda esperada durante el plazo de entrega medio ($LTD = d \cdot L$) al colchón de protección estocástica:

$$ROP = (d \cdot L) + SS_3 = (d \cdot L) + Z \cdot \sqrt{L \cdot \sigma_d^2 + d^2 \cdot \sigma_L^2}$$

Cuando el stock disponible (definido contablemente como $\text{Stock Físico} + \text{Pedidos en Curso} - \text{Órdenes Comprometidas}$) es menor o igual a $ROP$, el sistema ERP debe emitir de inmediato una orden de compra.

---

### 4.6. Lote Económico de Pedido ($EOQ$ de Wilson) y Coste Financiero

El $ROP$ responde a la pregunta directiva de **¿cuándo pedir?**. La pregunta complementaria de **¿cuánto pedir?** la resuelve el modelo clásico del **Lote Económico de Pedido ($EOQ$) de Ford W. Harris / R. H. Wilson**:

$$EOQ = \sqrt{\frac{2 \cdot D \cdot S}{h \cdot C}}$$

Donde:
- $D$: Demanda anual total proyectada en unidades ($D = d \cdot 365$ o días laborables).
- $S$: Coste administrativo fijo por emisión, procesamiento y recepción de cada pedido (€/pedido o $/pedido).
- $C$: Coste unitario de adquisición del producto (€/unidad).
- $h$: Tasa anual de mantenimiento y posesión de stock (% anual sobre el valor de compra). Incluye el coste medio ponderado de capital de la empresa (WACC), seguros, impuestos sobre existencias, alquiler y climatización de almacén, roturas, mermas y riesgo de obsolescencia. En empresas industriales y de distribución, oscila típicamente entre el **18% y el 25% anual**.

El **Coste Financiero Anual Directo de Mantener el Stock de Seguridad** se calcula como:

$$\text{Coste}_{SS} = SS \cdot C \cdot h$$

Cada unidad innecesaria de stock de seguridad devenga un coste financiero directo que drena el beneficio operativo neto (EBITDA) de la compañía sin aportar una sola venta adicional.

---

## 5. La Ley de Rendimientos Decrecientes y la Barrera Asintótica del Working Capital

Uno de los mayores errores conceptuales que cometen los comités de dirección es exigir a sus equipos de operaciones un *"Nivel de Servicio del 100%"*. Matemáticamente, alcanzar un 100% de disponibilidad garantizada frente a una distribución gaussiana de demanda exigiría situar el factor $Z$ en el infinito:

$$\lim_{CSL \to 100\%} \Phi^{-1}(CSL) = +\infty \implies SS \to \infty$$

Exigir un 100% de nivel de servicio requeriría inmovilizar la totalidad del activo de la empresa en existencias, paralizando las inversiones productivas y precipitando la quiebra técnica por insolvencia.

La relación entre el Nivel de Servicio ($CSL$) y el Capital Inmovilizado es una **curva hiperbólica asintótica exponencial**. Consideremos el comportamiento cuantitativo para un portfolio representativo con una base de 232.000 € de stock de seguridad al 95%:

| Nivel de Servicio ($CSL$) | Factor $Z$ Normal | Multiplicador vs. Base 95% | Capital en $SS$ (€) | Incremento Marginal (€) | Coste Posesión Anual (22%) | Diagnóstico Directivo |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **85,0%** | $1,036$ | $0,63\times$ | 146.200 € | — | 32.164 € | Alto riesgo de rotura (15% quiebres) |
| **90,0%** | $1,282$ | $0,78\times$ | 180.800 € | +34.600 € | 39.776 € | Óptimo para Clase C (Accesorios) |
| **95,0%** | $1,645$ | $1,00\times$ | 232.000 € | +51.200 € | 51.040 € | **Línea Base Estándar (Clase B)** |
| **97,0%** | $1,881$ | $1,14\times$ | 265.300 € | +33.300 € | 58.366 € | Zona de alta disponibilidad |
| **98,0%** | $2,054$ | $1,25\times$ | 289.700 € | +24.400 € | 63.734 € | **Estándar Directivo Clase A (Críticos)** |
| **99,0%** | $2,326$ | $1,41\times$ | 328.000 € | +38.300 € | 72.160 € | Frontera de sobre-inmovilización (+41%) |
| **99,5%** | $2,576$ | $1,57\times$ | 363.300 € | +35.300 € | 79.926 € | Duplicación de coste financiero (+56%) |
| **99,9%** | $3,090$ | $1,88\times$ | 435.800 € | +72.500 € | 95.876 € | **Coste asintótico prohibitivo (+88%)** |

> [!WARNING]
> **Evidencia para el Board:** Elevar el nivel de servicio del 95% al 98% incrementa el capital inmovilizado en 57.700 € (+25%), una inversión razonable y rentable para proteger los márgenes de los productos Clase A. Sin embargo, intentar pasar del 98% al 99,9% requiere inmovilizar 146.100 € adicionales (+50% sobre el óptimo), generando un sobrecoste anual de posesión de 32.142 €/año sin que el cliente final perciba una diferencia apreciable en el mercado.

---

## 6. Estrategia de Segmentación ABC y Matriz de Calibración

Para maximizar la liquidez disponible sin comprometer los ingresos, la metodología Datalaria prohíbe la aplicación de políticas homogéneas a todo el catálogo. Se debe implantar una **política de niveles de servicio asimétricos** vinculada a la clasificación ABC de Pareto:

### Clase A: Las Joyas de la Corona (15% - 20% de SKUs, 75% - 80% del Margen)
- **Nivel de Servicio Objetivo:** **98,0%** ($Z = 2,054$) o **99,0%** ($Z = 2,326$).
- **Justificación Estratégica:** Una rotura de stock en una referencia Clase A paraliza la facturación, provoca pérdida de clientes corporativos estratégicos y genera graves penalizaciones comerciales.
- **Protocolo Operativo:** Revisión semanal de parámetros de demanda, pedidos automáticos por $ROP$ y acuerdos marco de suministro con proveedores Tier-1 bajo integración EDI / VMI.

### Clase B: El Motor Intermedio (25% - 30% de SKUs, 15% - 20% del Margen)
- **Nivel de Servicio Objetivo:** **95,0%** ($Z = 1,645$).
- **Justificación Estratégica:** Artículos de rotación equilibrada donde una probabilidad de rotura de 1 ciclo cada 20 reabastecimientos es comercialmente asumible mediante sustitución de producto o entrega aplazada a 48 horas.
- **Protocolo Operativo:** Revisión mensual de parámetros $d, \sigma_d, L, \sigma_L$ y reabastecimiento estándar mediante $EOQ$.

### Clase C: El Catálogo Accesorio y de Tornillería (50% - 55% de SKUs, 5% - 10% del Margen)
- **Nivel de Servicio Objetivo:** **90,0%** ($Z = 1,282$).
- **Justificación Estratégica:** Mantener colchones de seguridad inflados en miles de referencias accesorias de baja rotación condena a la empresa a inmovilizar cientos de miles de euros en existencias zombies que terminarán provisionándose por obsolescencia.
- **Protocolo Operativo:** Revisión trimestral. Agrupación de pedidos para minimizar el coste administrativo de emisión ($S$). Si se produce una rotura temporal, el impacto en la cuenta de pérdidas y ganancias es insignificante.

---

## 7. Caso de Estudio Realista: Rescate Operativo en una Distribuidora B2B

Para ilustrar el impacto cuantitativo de esta metodología ante un Comité de Inversiones, analizamos un caso real de una empresa de distribución industrial de bienes de equipo y recambios técnicos con **4.500.000 €** en inventario activo y 2.400 referencias en catálogo.

### Diagnóstico Inicial
La compañía operaba bajo una regla heurística no revisada desde hacía cinco años: *"Todos los almacenes deben disponer de 30 días de venta prevista para cada producto"*.
- **Consecuencia 1 (Ventas):** En las 180 referencias Clase A, el plazo medio de importación era de 38 días con alta desviación. La regla de 30 días era insuficiente, provocando una **tasa de rotura del 6,8%** en los productos estrella y ventas frustradas estimadas en 380.000 € anuales.
- **Consecuencia 2 (Finanzas):** En las 1.400 referencias Clase C, los proveedores locales entregaban en 3 días. La regla de 30 días obligaba a mantener 27 días de stock inútil, acumulando **1.200.000 € en mercancía inmovilizada** en las naves centrales.

### Intervención Cuantitativa Datalaria
1. Se sustituyó la regla de los 30 días por el **Modelo Estocástico 3 de Convolución**.
2. Se calibraron los niveles de servicio: 98,5% para Clase A, 95% para Clase B y 90% para Clase C.
3. Se dimensionó el Punto de Pedido $ROP$ y el lote Wilson $EOQ$ para cada SKU.
4. Se pactó con los tres mayores fabricantes un acuerdo de ventana logística fija (reduciendo $\sigma_L$ de 5 a 2 días).

### Balance Ejecutivo de Resultados (Antes vs. Después)

| Indicador Estratégico (KPI) | Línea Base (Regla Heurística 30d) | Modelo Estocástico Datalaria | Impacto en Balance y Cuenta de Resultados |
| :--- | :---: | :---: | :--- |
| **Roturas en SKUs Clase A** | 6,8% de ciclos sin stock | **1,8% de ciclos sin stock** | **-73% de roturas:** +380.000 € en ventas salvadas |
| **Capital Total Inmovilizado** | 4.500.000 € | **4.280.000 €** | **+220.000 € de caja neta liberada al balance** |
| **Coste Financiero Posesión (22%)** | 990.000 € / año | **941.600 € / año** | **Ahorro recurrente directo de 48.400 € / año** |
| **Rotación de Inventario (Turns)** | 4,2x vueltas / año | **5,1x vueltas / año** | +21% de aceleración en conversión de efectivo |
| **Nivel de Servicio OTIF Global** | 91,5% entregas perfectas | **98,2% entregas perfectas** | Salto cualitativo en satisfacción y retención |

El programa liberó **220.000 € netos de tesorería inmediata** en 90 días mientras reducía las roturas en un 73%, demostrando que la eficiencia de inventario no es un juego de suma cero: un modelo matemático riguroso permite tener más disponibilidad con menos capital global.

---

## 8. Protocolo de Negociación de Lead Time y SLAs con Proveedores

Cuando un director de operaciones busca reducir el stock de seguridad, el primer instinto suele ser recortar el nivel de servicio exigido o invertir en software de inteligencia artificial para predecir mejor la demanda ($\sigma_d$). Sin embargo, el análisis matemático del modelo $SS_3 = Z \sqrt{L \sigma_d^2 + d^2 \sigma_L^2}$ demuestra que **la mayor palanca de liberación de caja reside en la mesa de negociación de compras**.

La empresa dispone de dos palancas directas con sus proveedores:

### 1. Compresión del Plazo Medio de Entrega ($L$)
Reducir el plazo de entrega medio en un 30% (por ejemplo, pasando de 14 a 10 días mediante acuerdos de inventario en consignación, almacenes avanzados de proveedor o logística prioritaria) contrae el término $L \cdot \sigma_d^2$. En un portfolio típico de 35 referencias industriales, esta medida libera de forma inmediata entre un **12% y un 18% del capital inmovilizado en stock de seguridad**.

### 2. Erradicación de la Impuntualidad del Proveedor ($\sigma_L$)
Dado que $\sigma_L$ está multiplicado por el cuadrado de la demanda ($d^2$), un proveedor con un plazo medio largo pero perfectamente predecible y puntual ($\sigma_L \to 0$) exige muchísimo menos stock de seguridad que un proveedor rápido pero caótico que entrega indistintamente entre 5 y 25 días.

> [!TIP]
> **Palanca de Negociación para Compras:** Negociar con los proveedores cláusulas contractuales de penalización por desvío de entrega (SLA) para reducir $\sigma_L$ a la mitad genera el doble de ahorro financiero que presionar por un descuento del 2% en el precio de compra. Un proveedor puntual autofinancia su coste reduciendo el colchón basal de tesorería del cliente.

---

## 9. Preguntas Frecuentes de Alta Dirección (Boardroom FAQ)

### ¿Por qué no debemos calcular el stock de seguridad en días de venta?
Expresar el stock de seguridad en días de venta es una trampa cognitiva. Diez días de demanda de un producto con plazo de entrega de 2 días y proveedor local representan un sobrestock exorbitante (+400%). Los mismos 10 días para un producto con plazo de 45 días importado de Asia representan una infradotación suicida. El stock de seguridad debe expresarse en unidades absolutas calculadas estocásticamente en función de $Z$, $\sigma_d$, $L$ y $\sigma_L$, y solo traducirse a días de cobertura como indicador divulgativo secundario.

### ¿Qué ocurre si la demanda no sigue una distribución normal estricta?
Para productos de rotación rápida y media (Clase A y B), el teorema del límite central garantiza que la agregación de la demanda durante períodos de varios días o semanas converge rápidamente a una distribución normal, haciendo el modelo $SS_3$ extraordinariamente robusto. En productos de demanda extremadamente errática o esporádica (típicos de repuestos de muy baja rotación Clase C, donde transcurren semanas sin ventas), se recomienda aplicar distribuciones de Poisson o modelos de probabilidad compuesta negativa binomial, o bien aplicar políticas de pedido bajo demanda sin stock preventivo.

### ¿Cómo convencemos al equipo de ventas para aceptar un 90% en referencias Clase C?
Explicando la economía del inventario con transparencia contable. Cuando el departamento comercial comprueba que los artículos Clase C representan menos del 5% del margen de la empresa pero consumen el 40% de la capacidad de almacenamiento y tesorería, comprende que cada euro inmovilizado en un tornillo accesorio es un euro que no está disponible para blindar el stock de los productos estrella Clase A que sostienen el bonus comercial de todo el equipo.

---

## 10. Executive Decision Pack: Tu Motor Cuantitativo Listo para Producción

Para que tu organización no tenga que invertir semanas en programar y auditar estas ecuaciones desde cero, el equipo de analistas de operaciones y finanzas de Datalaria ha consolidado todo este estándar metodológico en un paquete ejecutivo oficial de grado Consejo de Administración:

{{< product-card
  title="Calculadora de Stock de Seguridad & ROP"
  category="Cadena de Suministro"
  price="7€"
  original_price="22€"
  badge="📦 Control Operativo"
  icon="📦"
  preview_image="preview-pack.png"
  preview_caption="Vista previa real de los entregables incluidos: Calculadora de Stock de Seguridad & ROP en Excel (.xlsx) con Gráfico Diente de Sierra dinámico, Matriz de 35 SKUs, Convolución Estocástica (Modelos 1–3) y Simulador de Working Capital, Guía Metodológica Oficial (.pdf de 5 páginas) y Presentación Ejecutiva C-Level (.pptx 16:9 Widescreen)."
  deliverables="Excel .xlsx + Sheets|PowerPoint .pptx 16:9 C-Level|Guía Metodológica PDF"
  features="Modelos estocásticos de demanda y Lead Time variable|Cálculo automático de Stock de Seguridad (SS) y Punto de Pedido (ROP)|Gráfico dinámico de Diente de Sierra y dimensionamiento EOQ|Slide PPTX con análisis de Working Capital y optimización de caja|Descarga directa inmediata (.ZIP con versiones ES y EN)"
  checkout_url="https://datalaria.lemonsqueezy.com/checkout/buy/513e5cad-9f9f-4b53-a435-b511a846d79e"
  button_text="Descargar Pack Completo (.ZIP) • 7€"
>}}
Optimiza los niveles de inventario de tu empresa eliminando las roturas de stock y liberando capital de trabajo inmovilizado mediante modelos matemáticos rigurosos.
{{< /product-card >}}

### ¿Qué incluye el Executive Decision Pack oficial?

1. **Modelo Analítico Excel (.xlsx) y Google Sheets:**
   - **Pestaña 1 (Dashboard Ejecutivo):** Tarjetas KPI directivas, Gráfico dinámico Diente de Sierra (*Sawtooth*) y Matriz de Distribución y Concentración ABC.
   - **Pestaña 2 (Matriz SKU & Datos Operativos):** Catálogo parametrizable de 35 referencias con celdas de usuario desbloqueadas y fondo blanco para introducir demandas, desviaciones, plazos de proveedor y costes.
   - **Pestaña 3 (Motor Matemático SS & ROP):** Modelos estocásticos 1, 2 y 3 convolución integral, cálculo dinámico de factor Z, Punto de Pedido ROP, lote económico EOQ de Wilson, benchmark de brecha contra reglas heurísticas y diagnóstico de riesgo automatizado. Fórmulas protegidas bajo contraseña proporcionada en las instrucciones para evitar manipulaciones accidentales.
   - **Pestaña 4 (Trade-offs de Working Capital):** Curva de sensibilidad asintótica del 85% al 99,9% y simulador de impacto de negociación de Lead Time y SLAs de proveedor.
2. **Presentación Ejecutiva C-Level en PowerPoint (.pptx 16:9 Widescreen):**
   - 3 diapositivas estructuradas bajo la Pirámide de Minto con Action Titles contundentes: Diagnóstico de working capital, dinámica Diente de Sierra con curva asintótica, y Plan de negociación con el *Board Decision Gateway* y cajas de firma formal para CEO, CFO y COO.
3. **Guía Metodológica Editorial en PDF (5 Páginas):**
   - Documento de referencia de alta dirección con derivaciones matemáticas, caso de estudio real, protocolo de segmentación ABC, argumentario de defensa ante el Comité de Inversiones y bibliografía canónica.
4. **Instrucciones de Despliegue Inmediato:**
   - Descarga directa inmediata (.ZIP) con instrucciones paso a paso para Excel y Google Sheets.

---

## 11. Bibliografía Canónica y Normas Internacionales de Autoridad

1. **Silver, E. A., Pyke, D. F., & Thomas, D. J. (2016)** *Inventory and Production Management in Supply Chains – 4th Edition*, CRC Press / Taylor & Francis Group.
2. **Chopra, S., & Meindl, P. (2016)** *Supply Chain Management: Strategy, Planning, and Operation – 6th Edition*, Pearson Education.
3. **Association for Supply Chain Management (ASCM / APICS) (2020)** *APICS Dictionary – 16th Edition: Operations & Inventory Standards*, Chicago, IL.
4. **UNE-EN IEC 62402:2019** *Obsolescence Management – Guidelines for Managing Obsolescence across Component Lifecycles*, International Electrotechnical Commission (IEC) / IIOM.
5. **JEDEC Solid State Technology Association** *J-STD-046 (Customer Notification Standard for Product/Process Changes — PCN) & J-STD-048 (Notification Standard for Product Discontinuance — PDN / LTB)*.
6. **Simchi-Levi, D., Kaminsky, P., & Simchi-Levi, E. (2008)** *Designing and Managing the Supply Chain: Concepts, Strategies and Case Studies*, McGraw-Hill Irwin.
7. **Zipkin, P. H. (2000)** *Foundations of Inventory Management*, McGraw-Hill / Irwin Operations Management Series.
8. **Minto, B. (2009)** *The Pyramid Principle: Logic in Writing and Thinking*, Financial Times / Prentice Hall.
