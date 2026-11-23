---
title: "Cuadro de Mando EVM: Valor Ganado, Curva S y Proyecciones EAC C-Level"
date: 2026-11-23
draft: false
translationKey: "earned-value-management-evm-dashboard"
category: "Estrategia y Operaciones"
categories: ["Control Operativo", "Project Finance", "Plantillas Ejecutivas", "Estrategia y Operaciones"]
tags: ["Valor Ganado", "EVM", "ANSI/EIA-748", "Curva S", "CPI", "SPI", "EAC", "TCPI", "Control Operativo", "Project Management", "PMBOK", "C-Level"]
description: "Guía metodológica y cuantitativa de Earned Value Management (EVM / EIA-748): superación de la trampa contable, los 10 conceptos rectores, 27 directrices EVMS, EVM híbrido PMBOK, curvas S y proyecciones EAC/TCPI C-Level."
summary: "Erradica las sorpresas presupuestarias y los retrasos ocultos a mitad de proyecto con el estándar internacional de Earned Value Management (EVM / EIA-748, 27 directrices EVMS y enfoque Híbrido PMBOK). Cuantifica el avance técnico real (EV), audita la eficiencia de gasto (CPI) y cronograma (SPI), traza la Curva S ejecutiva y proyecta el coste final (EAC) listo para defender en comité."
cover:
  image: "cover.png"
  alt: "Cuadro de Mando EVM: Valor Ganado, Curva S, Índices CPI/SPI y Proyecciones EAC"
  caption: "Cuadro de Mando EVM (ANSI/EIA-748 & PMBOK): seguimiento de Valor Planificado (PV), Valor Ganado (EV) y Coste Real (AC), Curva S ejecutiva, modelos predictivos EAC, 27 directrices EVMS y aplicación en entornos híbridos."
  relative: true
images:
  - "cover.png"
  - "preview-pack.png"
---

En comités de dirección ejecutiva (*Executive Committee*), consejos de administración y comités de inversiones, directores generales (CEOs), directores financieros (CFOs), directores de operaciones (COOs) y directores de oficina de proyectos (PMOs) presencian de forma recurrente una de las patologías financieras y organizativas más costosas del mundo corporativo: **la trampa de la contabilidad tradicional en la gestión de proyectos estratégicos**.

Imaginemos un megaproyecto de transformación tecnológica, migración cloud o infraestructura crítica con un presupuesto aprobado ($BAC$) de **1.200.000 €** y un cronograma de ejecución de 12 meses. Al cumplirse el **Mes 6** (exactamente la mitad del plazo temporal previsto), el departamento de contabilidad y control de gestión emite su informe financiero oficial:

> *"A fecha de corte, el proyecto ha consumido 600.000 € frente a un presupuesto total de 1.200.000 €. Habiendo transcurrido el 50% del tiempo y habiéndose devengado el 50% de los fondos, el proyecto se encuentra estrictamente dentro del presupuesto y en orden."*

La alta dirección respira aliviada. Sin embargo, cinco meses más tarde, en el mes 11, salta la alarma ejecutiva: el presupuesto inicial de 1,2M € se ha agotado por completo, pero los entregables clave del sistema se encuentran inacabados, las pruebas de integración están bloqueadas y el equipo técnico solicita una inyección urgente de 300.000 € adicionales y una prórroga de cuatro meses para evitar el colapso operativo.

Ante el desconcierto y la irritación del Consejo de Administración, surge la pregunta inevitable: **¿cómo es posible que un proyecto que marchaba 'perfectamente en presupuesto' a mitad de plazo se convierta en una catástrofe financiera semanas antes del cierre?**

La respuesta es demoledora: **el proyecto nunca estuvo bien**. La contabilidad financiera tradicional reportó una ficción matemática. Medir únicamente el dinero gastado ($AC$) frente al calendario transcurrido ignora la única variable que define el éxito de una inversión: **cuánto valor físico real se ha producido a cambio de esos 600.000 €**.

Si a mitad de plazo se han gastado 600.000 € pero el equipo solo ha completado el 43% de los entregables reales (un valor físico de 516.000 €), el proyecto arrastraba ya en el Mes 6 un sobrecoste neto de 84.000 € y casi un mes de retraso no confesado. Por cada euro desembolsado, la organización solo obtenía 0,86 € de avance real.

Para erradicar este punto ciego y dotar a la gobernanza corporativa de un estándar cuantitativo de grado Consejo de Administración, el Departamento de Defensa de los Estados Unidos (DoD), el estándar industrial **ANSI/EIA-748** (modernizado en sus **27 Directrices EVMS**) y el **Project Management Institute (PMI)** en la **7ª Edición del PMBOK** y en *The Standard for Earned Value Management* formalizan la metodología de **Gestión del Valor Ganado (Earned Value Management - EVM)**.

En este artículo maestro desglosamos qué es el EVM y los 10 conceptos que lo rigen, su integración en el embudo estratégico-operativo de Datalaria, la arquitectura matemática completa (Curva S, varianzas $CV/SV$, índices $CPI/SPI$, modelos $EAC_1/EAC_2/EAC_3$ y test de realidad $TCPI$), los **27 criterios de la norma EIA-748**, su aplicación práctica en **proyectos híbridos / ágiles** y el protocolo de defensa ante el CFO y el Consejo de Administración.

{{< product-card
  variant="compact"
  title="Executive Decision Pack: Cuadro de Mando EVM (Valor Ganado & Curva S)"
  price="8€"
  original_price="25€"
  badge="📉 Estándar ANSI/EIA-748 & PMBOK"
  icon="📉"
  checkout_url="https://datalaria.lemonsqueezy.com/checkout/buy/188950c2-0fd9-4331-919f-237880e2c78b"
  button_text="Descargar Kit Ahora (.ZIP) • 8€"
>}}
¿Necesitas defender el presupuesto y el avance real de un proyecto estratégico ante el CEO o el CFO? Descarga el motor analítico en Excel (25 paquetes WBS, Curva S nativa M01–M12, índices CPI/SPI, modelos EAC₁/EAC₂/EAC₃ y test TCPI), la guía metodológica PDF de 5 páginas y la presentación ejecutiva 16:9.
{{< /product-card >}}

---

## 1. ¿Qué es el Cuadro de Mando de Valor Ganado (EVM)? Fundamentos, Conceptos Rectores y Objetivos

Para cualquier director de operaciones, jefe de proyecto, controller financiero o lector que se aproxime por primera vez a esta disciplina, la **Gestión del Valor Ganado (EVM)** es un método de control integrado que mide el desempeño real de un proyecto combinando tres dimensiones que tradicionalmente vivían separadas en silos distintos: **el alcance técnico completado, el cronograma previsto y el coste contable real**.

Mientras la contabilidad financiera solo pregunta *"¿cuánto dinero hemos gastado hasta hoy?"* y el diagrama de Gantt solo pregunta *"¿en qué día del calendario estamos?"*, el Cuadro de Mando EVM responde a la pregunta verdaderamente directiva: **"Por cada euro que ha salido de caja, ¿cuánto valor físico entregable hemos construido realmente, a qué velocidad avanzamos y cuánto acabará costando el proyecto el día que cierre?"**

Para gobernar cualquier iniciativa con rigor EVMS, todo el sistema se rige por **diez conceptos fundamentales**:

1. **Avance Técnico / Físico Real (*Technical / Physical Percent Complete*):** Porcentaje objetivo de finalización real alcanzado por cada entregable de la Estructura de Desglose del Trabajo (WBS). Se mide mediante reglas auditables ($0/100$, $50/50$, hitos ponderados) sobre resultados técnicos verificados, **nunca** por las horas trabajadas ni por el porcentaje de presupuesto gastado.
2. **Presupuesto hasta la Conclusión ($BAC$ - *Budget at Completion*):** Techo presupuestario total autorizado y aprobado contractualmente para ejecutar el 100% del alcance del proyecto (excluyendo reservas de gestión corporativa).
3. **Valor Planificado ($PV$ - *Planned Value*):** Valor monetario del trabajo que la línea base aprobada exigía tener completado hasta la fecha de corte ($PV = BAC \times \% \text{Avance Planificado}$). Su curva acumulada forma la Curva S de referencia.
4. **Valor Ganado ($EV$ - *Earned Value*):** Núcleo conceptual del sistema. Es el valor presupuestado del trabajo técnico que realmente se ha completado y validado a la fecha de corte ($EV = BAC \times \% \text{Avance Técnico Real}$).
5. **Coste Real Incurrido ($AC$ - *Actual Cost*):** Desembolso real total devengado en la contabilidad analítica (nóminas directas, facturas de proveedores, cloud/licencias y CAPEX imputado) para producir ese avance hasta la fecha de corte.
6. **Varianza de Coste ($CV = EV - AC$):** Desviación absoluta en euros entre el valor técnico producido y el coste pagado por él. Si $CV < 0$, el proyecto está sufriendo un sobrecoste neto.
7. **Varianza de Cronograma ($SV = EV - PV$):** Desviación absoluta expresada en moneda entre el trabajo físico entregado y el trabajo que debía estar entregado según el plan. Si $SV < 0$, el proyecto acumula retraso.
8. **Índice de Rendimiento de Coste ($CPI = EV / AC$):** Ratio adimensional de eficiencia financiera. Un $CPI = 0.86$ significa que por cada $1,00\text{ €}$ gastado solo se obtiene $0,86\text{ €}$ de alcance técnico terminado.
9. **Índice de Rendimiento de Cronograma ($SPI = EV / PV$):** Ratio de velocidad de ejecución respecto al cronograma base. Un $SPI = 0.86$ indica que el equipo entrega alcance al $86\%$ de la velocidad prevista.
10. **Estimación a la Finalización ($EAC$), Varianza al Cierre ($VAC$) e Índice para Completar ($TCPI$):** El $EAC$ proyecta matemáticamente el coste final total al cierre ($BAC / CPI$ en escenario típico); el $VAC = BAC - EAC$ cuantifica el déficit presupuestario final previsto; y el $TCPI = (BAC - EV) / (BAC - AC)$ calcula la eficiencia exacta que el equipo necesitaría mantener en el trabajo pendiente para salvar el presupuesto original.

### 1.1 Los Cuatro Objetivos Estratégicos ante el Consejo de Administración

Adoptar un Cuadro de Mando EVM frente al control presupuestario clásico persigue cuatro objetivos directivos concretos:

1. **Unificar alcance técnico, plazo y tesorería en una única métrica auditable:** Eliminar las presentaciones subjetivas tipo *"el código está casi listo"* obligando a traducir el progreso técnico verificado en valor monetario ganado ($EV$).
2. **Detectar desviaciones estructurales en la ventana temprana del 15–20%:** Aprovechar la estabilidad empírica del $CPI$ descubierta por Christensen (1998) para activar acciones correctivas cuando aún queda el 80% del presupuesto por ejecutar.
3. **Sustituir conjeturas de cierre por modelos probabilísticos y estadísticos ($EAC$ y $VAC$):** Dotar al CFO de tres escenarios cuantitativos (típico, atípico y compuesto) para provisionar reservas de liquidez antes de que el proyecto se quede sin fondos.
4. **Aplicar un test de realidad matemática ($TCPI$) a los planes de recuperación:** Impedir que los directores de proyecto prometan recuperaciones milagrosas sin ajuste de alcance o recursos cuando el esfuerzo requerido supera el umbral empírico de $1.10\text{x}$.

### 1.2 Seguimiento Contable Tradicional vs. Cuadro de Mando EVM (ANSI/EIA-748 & PMBOK)

| Dimensión de Gobierno | Control Contable Tradicional (Gasto vs. Calendario) | Cuadro de Mando EVM (Estándar EIA-748 & PMBOK) | Ventaja Estratégica C-Level |
| :--- | :--- | :--- | :--- |
| **Unidad de control** | Comparación bidimensional de dinero gastado ($AC$) frente a presupuesto planificado ($PV$). | **Integración tridimensional:** Alcance técnico físico ($EV$), Cronograma ($PV$) y Coste Real ($AC$). | Elimina el punto ciego donde gastar el 50% a mitad de plazo oculta un retraso del 14%. |
| **Medición del avance** | Subjetiva ("estamos al 90%") o inferida erróneamente desde horas/facturas consumidas. | **Avance Técnico Real** validado mediante reglas $0/100$, $50/50$, hitos ponderados o *DoD*. | Erradica el "síndrome del 90% completado infinito" antes de pasar a UAT o producción. |
| **Diagnóstico de causa raíz** | Indiferenciado: no distingue si el problema es sobrecoste técnico o retraso en entregas. | **Aislamiento quirúrgico:** $CV/CPI$ miden eficiencia financiera y $SV/SPI$ miden velocidad temporal. | Permite elegir entre palancas de coste (tarifas/descope) o de plazo (*Crashing/Fast-Tracking*). |
| **Previsión a la conclusión** | Inexistente o basada en optimismo lineal ("al final recuperaremos el desvío"). | **Tres modelos formales ($EAC_1, EAC_2, EAC_3$)** y **Varianza al Cierre ($VAC$)**. | Anticipa con meses de antelación la necesidad real de reservas o *re-baselining*. |
| **Validación de viabilidad** | Promesas verbales en comité sin contraste histórico de productividad. | **Test estadístico $TCPI$** frente a umbrales empíricos ($\text{alerta si } TCPI > 1.10$). | Protege al Consejo de aprobar planes de rescate matemáticamente imposibles. |
| **Escalabilidad metodológica** | Rígido; inservible cuando cambian prioridades en equipos iterativos. | **Compatible con Cascada, Híbrido y Agile-EVM** (Cuentas de Control + *Story Points*). | Gobierno financiero homogéneo para el CFO en toda la cartera de proyectos. |

### 1.3 El Embudo Estratégico-Operativo en Datalaria

El Cuadro de Mando EVM no opera de forma aislada: constituye la capa de control financiero y de ejecución en vivo que culmina el ciclo completo de **Estrategia Corporativa, Decisión Inversora y Control Operativo** documentado en Datalaria:

* **Capa 1 · Estrategia Corporativa y Selección de Iniciativas (Suite 01):** Antes de aprobar presupuestos de proyecto, la dirección determina en qué mercados y líneas de negocio competir combinando la [Matriz DAFO Cuantitativa y CAME](/es/posts/dafo-cuantitativo-matriz-came/), el entorno macroeconómico en la [Matriz PESTEL Cuantitativa](/es/posts/matriz-pestel-cuantitativa/), el análisis competitivo con las [5 Fuerzas de Porter Ponderadas](/es/posts/5-fuerzas-porter-cuantitativas/), la [Matriz BCG Dinámica](/es/posts/matriz-bcg-dinamica/) y la [Matriz McKinsey / GE 3x3](/es/posts/matriz-mckinsey-ge/), integrados en el [Framework Integral de Estrategia Corporativa MBA](/es/posts/estrategia-corporativa-mba-framework-cuantitativo/).
* **Capa 2 · Decisión Racional, Priorización y Rentabilidad (Suite 02):** Las iniciativas candidatas superan filtros de veto con la [Matriz DAR Cuantitativa](/es/posts/matriz-dar-cuantitativa/), ordenan su roadmap mediante la [Matriz RICE & ICE de Priorización Ágil](/es/posts/matriz-rice-ice-priorizacion/) y demuestran rentabilidad de capital ($VAN$, $TIR$ y *Payback*) en el [Business Case Financiero](/es/posts/business-case-financiero-van-tir/), vertebrados en el [Framework de Toma de Decisiones Racional y Priorización](/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/).
* **Capa 3 · Control Operativo y Ejecución Blindada (Suite 03):** Aprobado el *Business Case*, la organización asigna un único responsable decisor ($A=1$) por Cuenta de Control en la [Matriz RACI Cuantitativa y Balance de Carga](/es/posts/matriz-raci-balance-carga/), cuantifica modos de fallo y reservas de contingencia en la [Matriz de Riesgos Cuantitativa & AMFE / FMEA (NPR)](/es/posts/matriz-riesgos-amfe-fmea/) y fija una línea base de cronograma probabilística $P_{90}$ con la [Estimación PERT de 3 Puntos Estocástica](/es/posts/estimacion-pert-3-puntos/). A partir del Día 1 de ejecución, este **Cuadro de Mando EVM** audita que el VAN proyectado en el *Business Case* no se destruya por sobrecostes ($CPI < 1$) ni retrasos ($SPI < 1$) antes del cierre operativo y el aprovisionamiento de recursos.

---

## 2. El Pipeline de Control Financiero y Operativo EVM

El estándar EVM no es un simple informe de control de gestión retrospectivo; es un **sistema predictivo de alerta temprana y gobierno de inversiones** que conecta el desglose físico del trabajo (WBS) con la tesorería corporativa:

{{< mermaid image="evm_control_pipeline.png" alt="Pipeline de Control Financiero y Operativo EVM: PMB, PV, EV, AC, CPI, SPI, EAC y TCPI" >}}
flowchart TD
    A["<b>1. Línea Base del Desempeño (PMB)</b><br/><small>Estructura WBS descompuesta en entregables tangibles<br/>Presupuesto total autorizado a la finalización (BAC)</small>"]
    
    B["<b>2. Curva de Valor Planificado (PV)</b><br/><small>Distribución temporal del presupuesto por hitos y meses<br/>PV = BAC × % Planificado a la fecha de corte</small>"]
    
    C["<b>3. Medición del Avance Técnico Real</b><br/><small>Imputación objetiva de avance (Reglas 0/100, 50/50, Hitos)<br/>Eliminación del 'síndrome del 90% infinito'</small>"]
    
    D["<b>4. Cálculo del Valor Ganado (EV)</b><br/><small>Presupuesto autorizado del trabajo completado<br/>EV = BAC × % Avance Técnico Real</small>"]
    
    E["<b>5. Registro del Coste Real Incurrido (AC)</b><br/><small>Facturas aprobadas, horas directas, CAPEX devengado<br/>AC = Contabilidad analítica de costes</small>"]
    
    F["<b>6. Motor de Varianzas e Índices</b><br/><small>Varianza Coste: CV = EV - AC  |  CPI = EV / AC<br/>Varianza Cronograma: SV = EV - PV  |  SPI = EV / PV</small>"]
    
    G{"<b>7. Evaluación de Salud Operativa</b><br/><small>Matriz 2x2: ¿CPI ≥ 1.00 y SPI ≥ 1.00?<br/>Diagnóstico de alertas en Cuadrantes 1 a 4</small>"}
    
    H["<b>ZONA DE ALERTA O CRISIS</b><br/><small>Modelos predictivos EAC (Típico, Atípico, Compuesto)<br/>Cálculo de esfuerzo remanente TCPI vs BAC</small>"]
    
    I["<b>8. Plan de Recuperación y Board Gateway</b><br/><small>Fast-Tracking, Crashing, Descope negociado<br/>Re-baselining formal con aprobación del Consejo</small>"]

    A --> B
    B --> C
    C --> D
    D --> F
    E --> F
    F --> G
    G -->|"Desviación Crítica"| H
    H --> I
    G -->|"Saludable"| B

    style A fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px,color:#0F172A
    style B fill:#EFF6FF,stroke:#3B82F6,stroke-width:1.5px,color:#1E3A8A
    style C fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px,color:#0F172A
    style D fill:#D1FAE5,stroke:#10B981,stroke-width:2px,color:#065F46
    style E fill:#FEE2E2,stroke:#DC2626,stroke-width:1.5px,color:#991B1B
    style F fill:#0F172A,stroke:#2563EB,stroke-width:2px,color:#FFFFFF
    style G fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px,color:#92400E
    style H fill:#FEE2E2,stroke:#DC2626,stroke-width:2px,color:#991B1B
    style I fill:#0F172A,stroke:#7C3AED,stroke-width:2px,color:#FFFFFF
{{< /mermaid >}}

Este flujo garantiza que cualquier desviación operativa se detecte cuando el proyecto ha consumido entre el 15% y el 20% de su ciclo de vida, momento en el cual el coste de recuperación es mínimo y la capacidad de maniobra ejecutiva es máxima.

---

## 3. Fundamentación Matemática del Estándar EVM (ANSI/EIA-748)

Para que el control presupuestario y temporal sea auditable y computable sin ambigüedades, el estándar EVM define con rigor axiomático sus variables canónicas, ecuaciones de varianza, índices de eficiencia y modelos de extrapolación estadística.

### 3.1 Las Cuatro Dimensiones Monetarias de Referencia

Todo el edificio analítico de EVM se apoya sobre magnitudes monetarias evaluadas a una misma fecha de corte (*Status Date* o *Data Date*):

#### A. Presupuesto Total a la Finalización ($BAC$)
El **Budget at Completion ($BAC$)** representa el presupuesto total autorizado y aprobado contractualmente para completar el 100% del alcance del proyecto, excluyendo las reservas de gestión corporativa (*Management Reserves*). Constituye el ancla de referencia financiera:
$$BAC = \sum_{i=1}^{n} BAC_i$$
Donde $BAC_i$ es el presupuesto asignado al paquete de trabajo $i$ de la WBS.

#### B. Valor Planificado ($PV$ - Planned Value)
Conocido históricamente como **BCWS** (*Budgeted Cost of Work Scheduled*), el **Planned Value ($PV$)** es el valor monetario del trabajo que, de acuerdo con el cronograma y la línea base aprobada, debería haberse completado a la fecha de corte:
$$PV = BAC \times \% \text{Avance Planificado}$$

El trazado temporal del $PV$ acumulado a lo largo de los periodos del proyecto genera la clásica curva en forma de 'S' (la Curva S de referencia o *Baseline S-Curve*).

#### C. Valor Ganado ($EV$ - Earned Value)
Conocido históricamente como **BCWP** (*Budgeted Cost of Work Performed*), el **Earned Value ($EV$)** es el corazón del estándar. Representa el valor monetario del trabajo físico que ha sido efectivamente completado y validado a la fecha de corte:
$$EV = BAC \times \% \text{Avance Técnico Real}$$

> **Principio de Oro de EVM:** El Valor Ganado se calcula siempre multiplicando el presupuesto original ($BAC$) por el avance físico real completado. **Nunca** se calcula en función de las horas invertidas ni de las facturas pagadas. Si una tarea presupuestada en 100.000 € se encuentra ejecutada al 40%, su $EV$ es exactamente 40.000 €, independientemente de que se hayan gastado 20.000 € o 90.000 €.

#### D. Coste Real Incurrido ($AC$ - Actual Cost)
Conocido históricamente como **ACWP** (*Actual Cost of Work Performed*), el **Actual Cost ($AC$)** es el coste total devengado y registrado por la contabilidad de la empresa para ejecutar el trabajo realizado hasta la fecha de corte:
$$AC = \text{Costes Directos de Personal} + \text{Facturas de Contratistas} + \text{Licencias} + \text{CAPEX Imputado}$$

---

### 3.2 Ecuaciones de Varianzas: Diagnóstico Absoluto en Moneda

El contraste directo entre estas variables permite aislar con precisión de bisturí los dos grandes problemas de cualquier iniciativa: si el proyecto está gastando de más (problema de coste) o si va con retraso (problema de plazo).

#### 1. Varianza de Coste ($CV$ - Cost Variance)
Cuantifica en unidades monetarias el sobrecoste o ahorro respecto al valor físico producido:
$$CV = EV - AC$$

* **$CV > 0$ (Superávit / Eficiencia):** Se ha generado más valor físico del dinero consumido.
* **$CV = 0$ (Neutral):** El coste real coincide exactamente con el valor del trabajo producido.
* **$CV < 0$ (Sobrecoste / Déficit):** Se ha gastado más dinero del valor físico que se puede justificar. En nuestro ejemplo de corte: $CV = 516.000 - 600.000 = -84.000 \text{ €}$ (pérdida neta de 84.000 €).

#### 2. Varianza de Cronograma ($SV$ - Schedule Variance)
Cuantifica en unidades monetarias el adelanto o retraso del proyecto respecto a la línea base temporal:
$$SV = EV - PV$$

* **$SV > 0$ (Adelanto):** El equipo ha completado más trabajo del que estaba programado.
* **$SV = 0$ (A Tiempo):** La velocidad de entrega coincide exactamente con el cronograma.
* **$SV < 0$ (Retraso):** El equipo ha producido menos entregables de los planificados. En nuestro ejemplo: $SV = 516.000 - 600.000 = -84.000 \text{ €}$ (déficit de entregables valorado en 84.000 €).

---

### 3.3 Índices de Rendimiento Operativo: Eficiencia Relativa ($CPI$ y $SPI$)

Las varianzas en euros ($CV, SV$) miden magnitudes absolutas, pero no permiten comparar proyectos de distinta escala ni proyectar tendencias futuras. Para ello, el estándar EVM establece los dos ratios adimensionales de productividad más respetados en la industria de la gestión de proyectos:

#### A. Índice de Rendimiento de Coste ($CPI$ - Cost Performance Index)
Mide la eficiencia del gasto de capital:
$$CPI = \frac{EV}{AC}$$

* **$CPI = 1.00$:** Rendimiento perfecto. Cada euro gastado genera exactamente un euro de valor entregado.
* **$CPI > 1.00$:** Superávit de productividad. Por ejemplo, $CPI = 1.15$ indica que por cada euro gastado se generan 1,15 € de entregables.
* **$CPI < 1.00$:** Destrucción de capital. En nuestro proyecto: $CPI = \frac{516.000}{600.000} = \mathbf{0.86}$. Por cada 1,00 € gastado, la organización solo está materializando 0,86 € de avance físico (un sobrecoste del 16,3%).

> **Regla de Estabilidad Empírica de Christensen (1998):** En más de 400 proyectos gubernamentales y comerciales analizados por David S. Christensen, se demostró un hecho matemático crucial: **el $CPI$ acumulado de un proyecto se estabiliza cuando se alcanza el 20% de avance físico y rara vez mejora en más de 0.05 puntos hasta el final**. Asumir que un equipo con $CPI = 0.86$ "se recuperará espontáneamente" en la segunda mitad es una ilusión estadística desmentida por décadas de datos empíricos.

#### B. Índice de Rendimiento de Cronograma ($SPI$ - Schedule Performance Index)
Mide la velocidad de conversión del cronograma:
$$SPI = \frac{EV}{PV}$$

* **$SPI = 1.00$:** El proyecto avanza a la velocidad exacta programada.
* **$SPI > 1.00$:** El proyecto avanza más rápido que la planificación original.
* **$SPI < 1.00$:** Retraso acumulado. En nuestro ejemplo: $SPI = \frac{516.000}{600.000} = \mathbf{0.86}$ (el proyecto avanza solo al 86% de la velocidad requerida, lo que a mitad de plazo equivale a 3 semanas de retraso en la cadena de entregables).

---

## 4. Matriz de Salud Operativa 2x2: Diagnóstico Cruzado $CPI$ vs $SPI$

Para la alta dirección y los comités de inversión, la combinación de $CPI$ y $SPI$ define cuatro cuadrantes operacionales inequívocos que dictan el nivel de gobernanza requerido:

{{< mermaid image="evm_health_matrix_2x2.png" alt="Matriz de Salud Operativa EVM 2x2: Diagnóstico Cruzado CPI vs SPI" >}}
flowchart TD
    subgraph CUADRANTE_2["<b>CUADRANTE 2: ALERTA PLAZO</b><br/>CPI ≥ 1.00 | SPI < 1.00"]
        Q2["Bajo presupuesto pero con retraso cronológico.<br/><i>Riesgo:</i> Holguras consumidas y penalizaciones contractuales.<br/><i>Acción:</i> Crashing selectivo con el ahorro de costes disponible."]
    end

    subgraph CUADRANTE_1["<b>CUADRANTE 1: ZONA SALUDABLE</b><br/>CPI ≥ 1.00 | SPI ≥ 1.00"]
        Q1["En tiempo y dentro de presupuesto.<br/><i>Estado:</i> Productividad óptima y gobernanza estándar.<br/><i>Acción:</i> Monitorización preventiva y mantenimiento de ritmo."]
    end

    subgraph CUADRANTE_4["<b>CUADRANTE 4: ZONA DE CRISIS</b><br/>CPI < 1.00 | SPI < 1.00"]
        Q4["Sobrecoste activo y retraso severo en entregables.<br/><i>Estado:</i> Máxima vulnerabilidad organizativa.<br/><i>Acción:</i> Plan de rescate urgente, descope y re-baselining."]
    end

    subgraph CUADRANTE_3["<b>CUADRANTE 3: ALERTA COSTE</b><br/>CPI < 1.00 | SPI ≥ 1.00"]
        Q3["En plazo pero con sobrecoste financiero.<br/><i>Riesgo:</i> Aceleración insostenible pagada con horas extra/CAPEX.<br/><i>Acción:</i> Congelar ampliaciones de equipo y auditar proveedores."]
    end

    Q2 --- Q1
    Q4 --- Q3

    style CUADRANTE_1 fill:#D1FAE5,stroke:#10B981,stroke-width:2px,color:#065F46
    style CUADRANTE_2 fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px,color:#92400E
    style CUADRANTE_3 fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px,color:#92400E
    style CUADRANTE_4 fill:#FEE2E2,stroke:#DC2626,stroke-width:2px,color:#991B1B
{{< /mermaid >}}

En el caso analizado, con $CPI = 0.86$ y $SPI = 0.86$, el proyecto se ubica de lleno en el **Cuadrante 4 (Zona de Crisis)**. Ocultar esta realidad o mantener las operaciones sin cambios garantiza que la desviación al cierre sea incontrolable.

---

## 5. Modelos Matemáticos de Proyección a la Finalización: $EAC$, $VAC$ y $TCPI$

Uno de los mayores aportes de EVM ante el Consejo de Administración es su capacidad para responder a la pregunta que todo CFO y CEO formula: **"¿Cuánto nos va a costar realmente terminar este proyecto y cuándo estará terminado?"**

Para responder, EVM no recurre a estimaciones intuitivas; implementa tres modelos matemáticos de **Estimación a la Finalización ($EAC$ - Estimate at Completion)** según las hipótesis operativas asumidas:

### 5.1 Modelo 1: Escenario Típico ($EAC_1$ - Manteniendo la Eficiencia Actual)
Asume que la ineficiencia o sobrecoste observado hasta la fecha es estructural y que el trabajo remanente se ejecutará con el mismo rendimiento de coste ($CPI$) registrado:
$$EAC_1 = \frac{BAC}{CPI}$$

En nuestro proyecto de 1.200.000 €:
$$EAC_1 = \frac{1.200.000}{0,86} = \mathbf{1.395.349 \text{ €}}$$

Este modelo anticipa que el proyecto terminará costando casi **1,4 millones de euros**, lo que supone un sobrecoste de casi 200.000 €.

### 5.2 Modelo 2: Escenario Atípico ($EAC_2$ - Las Desviaciones Pasadas Fueron Puntuales)
Asume que las desviaciones sufridas se debieron a eventos singulares e irrepetibles (un bloqueo puntual de proveedores o un error inicial de arquitectura ya resuelto) y que todo el trabajo restante se completará exactamente al coste planificado original ($1,00$ de eficiencia):
$$EAC_2 = AC + (BAC - EV)$$

En nuestro caso:
$$EAC_2 = 600.000 + (1.200.000 - 516.000) = 600.000 + 684.000 = \mathbf{1.284.000 \text{ €}}$$

Incluso en este escenario optimista, el proyecto requiere **84.000 € más** de lo presupuestado.

### 5.3 Modelo 3: Escenario Crítico o Compuesto ($EAC_3$ - Impacto Combinado de Coste y Retraso)
En megaproyectos tecnológicos y de ingeniería, los retrasos cronológicos casi nunca son gratuitos: conllevan el pago continuado de nóminas, licencias de infraestructura cloud devengadas por mes, alquileres de servidores y posibles penalizaciones contractuales por entrega tardía. El modelo compuesto penaliza el coste futuro dividiendo el trabajo remanente por el producto de $CPI \times SPI$:
$$EAC_3 = AC + \frac{BAC - EV}{CPI \times SPI}$$

En nuestro proyecto:
$$EAC_3 = 600.000 + \frac{684.000}{0,86 \times 0,86} = 600.000 + \frac{684.000}{0,7396} = 600.000 + 924.824 = \mathbf{1.524.824 \text{ €}}$$

Si la organización no corrige de inmediato el retraso y el sobrecoste simultáneos, el coste final puede desbordarse en más de **324.000 € adicionales**.

---

### 5.4 Varianza a la Conclusión ($VAC$ - Variance at Completion)
Representa la diferencia final proyectada entre el presupuesto autorizado ($BAC$) y el coste proyectado ($EAC$):
$$VAC = BAC - EAC$$

Para el escenario típico:
$$VAC_1 = 1.200.000 - 1.395.349 = \mathbf{-195.349 \text{ €}}$$

El signo negativo indica que la empresa enfrentará un **déficit presupuestario de 195.349 €**, cifra exacta que debe reservarse o negociarse en el comité de dirección.

---

### 5.5 El Índice de Rendimiento para Completar ($TCPI$): El Test de Realidad Estadística

Cuando el equipo de proyecto promete al Consejo de Administración que *"recuperará el retraso y terminará dentro del presupuesto original de 1,2M € sin pedir más dinero"*, el estándar EVM somete esa afirmación a una prueba de fuego matemática mediante el **To-Complete Performance Index ($TCPI$)**:

$$TCPI_{BAC} = \frac{\text{Trabajo Remanente}}{\text{Fondos Remanentes}} = \frac{BAC - EV}{BAC - AC}$$

Calculando para nuestro caso:
$$TCPI_{BAC} = \frac{1.200.000 - 516.000}{1.200.000 - 600.000} = \frac{684.000}{600.000} = \mathbf{1.14}$$

> **Interpretación Crítica para el Consejo:**  
> Un $TCPI_{BAC} = 1.14$ significa que, para entregar el trabajo que falta (684.000 €) con el dinero que queda en caja (600.000 €), el equipo debe rendir a una eficiencia del **114%** durante los próximos seis meses.  
> Teniendo en cuenta que el equipo ha venido operando a un rendimiento de **$0.86$**, exigirle un $TCPI$ de $1.14$ requiere un **salto repentino de productividad del 32,5%**.  
> Según la literatura empírica del PMBOK y ANSI/EIA-748, **cualquier $TCPI > 1.10$ se considera estadísticamente inalcanzable** en condiciones operativas normales. Prometer cumplir el $BAC$ con un $TCPI = 1.14$ es una fantasía contable que aboca al proyecto a un nuevo fracaso en el mes 12.

Para fijar un objetivo realista, el PMBOK prescribe calcular el $TCPI$ referenciado al nuevo techo proyectado ($EAC$):
$$TCPI_{EAC} = \frac{BAC - EV}{EAC_1 - AC} = \frac{684.000}{1.395.349 - 600.000} = \frac{684.000}{795.349} = \mathbf{0.86}$$

Si el Consejo de Administración aprueba formalmente el re-baselining presupuestario elevando el techo a 1.395.349 €, el equipo solo necesita mantener la productividad que ya ha demostrado ($0.86$), haciendo el proyecto perfectamente viable y gobernable.

---

## 6. Reglas Operativas para Imputar el Avance Técnico ($EV$) sin Sesgos

La validez de todo el modelo EVM depende de un factor humano crítico: **cómo se mide el % de avance físico**. Para erradicar el optimismo subjetivo de los líderes de desarrollo, el estándar **ANSI/EIA-748** establece cuatro reglas objetivas de imputación:

1. **Regla 0 / 100 (Cero / Cien):**  
   El entregable tiene un avance del 0% mientras esté en curso. Solo se le imputa el 100% una vez completado, probado y aceptado formalmente. Es de aplicación obligatoria para tareas de corta duración (< 2 semanas o 1 sprint ágil).
2. **Regla 50 / 50 (Cincuenta / Cincuenta):**  
   Se imputa un 50% de avance físico en el momento exacto en que la tarea comienza oficialmente, y el 50% restante únicamente cuando el entregable se certifica al 100%. Recomendada para paquetes de trabajo de duración intermedia (2 a 4 semanas).
3. **Hitos Ponderados (Weighted Milestones):**  
   Para paquetes de trabajo de varios meses, se descompone la tarea en hitos intermedios con porcentajes fijos pre-acordados en la línea base:
   * *Hito 1:* Arquitectura y especificación técnica validada: **20%**
   * *Hito 2:* Código desarrollado y pruebas unitarias superadas: **30%**
   * *Hito 3:* Homologación e integración en staging: **30%**
   * *Hito 4:* Pruebas UAT de negocio firmadas: **20%**
4. **Unidades Cuantificadas (Earned Standards):**  
   Aplicable a procesos repetitivos y volumétricos (ej. migración de 10.000 tablas de base de datos o despliegue de 500 sucursales). El porcentaje de avance es simplemente el ratio de unidades completadas y verificadas respecto al total planificado.

---

## 7. El Estándar EIA-748 y los 27 Criterios de un Sistema EVMS acorde al PMBOK

Muchos directivos conocen el término "Valor Ganado" como un conjunto de fórmulas, pero ignoran que la fiabilidad institucional de esos números ante una auditoría depende del cumplimiento de la norma **EIA-748**, el marco internacional de referencia para los Sistemas de Gestión del Valor Ganado (*Earned Value Management Systems - EVMS*).

Históricamente, la norma nació de los 35 criterios C/SCSC del Departamento de Defensa de EE. UU. (1967) y se consolidó durante más de dos décadas en los **32 criterios** de las versiones ANSI/EIA-748-A hasta la EIA-748-D. Sin embargo, tal y como documenta Roland Wanner en su análisis de referencia sobre el estándar ([EIA-748 and 27 Earned Value Management Systems (EVMS) Guidelines](https://rolandwanner.com/eia-748-and-27-earned-value-management-systems-evms-guidelines/)), la revisión moderna **EIA-748-E** consolida y depura el marco en **27 Directrices EVMS esenciales** alineadas directamente con las áreas de desempeño del **PMBOK**.

El objetivo de esta simplificación de 32 a 27 criterios es eliminar redundancias contables burocráticas, reforzar la flexibilidad operativa y centrar el sistema en la **utilidad real para la toma de decisiones ejecutivas**. Las **27 directrices de la EIA-748** se estructuran en **cinco grandes grupos de procesos**:

| Grupo de Procesos EIA-748 | N.º de Criterios | Propósito Rector y Alineación PMBOK / Datalaria |
| :--- | :---: | :--- |
| **1. Organización** | **4** (Criterios 1–4) | Definir el alcance en una WBS, vincularlo a la estructura organizativa (OBS) y asignar un responsable único (*Control Account Manager*) conforme a la regla $A=1$ de la [Matriz RACI Cuantitativa](/es/posts/matriz-raci-balance-carga/). |
| **2. Planificación, Programación y Presupuestación** | **9** (Criterios 5–13) | Integrar cronograma crítico (alineado con [Estimación PERT](/es/posts/estimacion-pert-3-puntos/)), construir la línea base escalonada ($PMB$), definir reglas objetivas de $EV$ y segregar Reservas de Gestión (conectado con riesgos [AMFE / FMEA](/es/posts/matriz-riesgos-amfe-fmea/)). |
| **3. Evaluación del Progreso y Recopilación de Datos** | **3** (Criterios 14–16) | Garantizar la consistencia contable del Coste Real ($AC$), la medición objetiva del Valor Ganado ($EV$) y el devengo real de materiales y subcontratos sin sesgos de caja. |
| **4. Análisis e Informes de Gestión** | **5** (Criterios 17–21) | Calcular periódicamente $CV, SV, CPI, SPI$, documentar causas raíz, vigilar costes indirectos, ejecutar planes de acción y actualizar las proyecciones $EAC$ y $VAC$ ante el Comité. |
| **5. Revisiones y Mantenimiento de Datos** | **6** (Criterios 22–27) | Incorporar cambios aprobados de alcance sin alterar retroactivamente la historia, impedir trasvases opacos entre cuentas, controlar la Reserva de Gestión y gobernar el *re-baselining* formal. |

### Desglose Operativo de los 27 Criterios EIA-748

1. **Grupo 1 · Organización (4 Criterios):**
   * **Criterio 1:** Definir los elementos de trabajo autorizados mediante una Estructura de Desglose del Trabajo (WBS) única orientada a entregables.
   * **Criterio 2:** Identificar la Estructura Organizativa del Proyecto (OBS), incluyendo subcontratistas relevantes, definiendo claramente quién ejecuta cada bloque.
   * **Criterio 3:** Integrar los sistemas corporativos de planificación, programación, presupuestación, autorización del trabajo y acumulación de costes bajo una codificación WBS/OBS coherente.
   * **Criterio 4:** Establecer **Cuentas de Control (*Control Accounts*)** en la intersección WBS $\times$ OBS, asignando un único gestor responsable (*Control Account Manager - CAM*) con autoridad sobre presupuesto y desempeño.
2. **Grupo 2 · Planificación, Programación y Presupuestación (9 Criterios):**
   * **Criterio 5:** Programar todo el trabajo autorizado en un cronograma maestro integrado con dependencias lógicas, hitos clave y camino crítico identificable.
   * **Criterio 6:** Identificar productos físicos, hitos e indicadores técnicos de progreso que permitan verificar el avance objetivo.
   * **Criterio 7:** Establecer y mantener una **Línea Base de Medición del Desempeño ($PMB$)** distribuida en el tiempo (*Time-Phased Budget*) para el total del trabajo autorizado.
   * **Criterio 8:** Establecer presupuestos para cada Cuenta de Control diferenciando explícitamente los elementos de coste (mano de obra directa, materiales, subcontratos y otros costes directos).
   * **Criterio 9:** Descomponer las Cuentas de Control en **Paquetes de Trabajo (*Work Packages*)** detallados para el horizonte cercano y **Paquetes de Planificación (*Planning Packages*)** para fases futuras pendientes de detalle.
   * **Criterio 10:** Definir por adelantado el método objetivo de cálculo de Valor Ganado ($0/100, 50/50$, hitos ponderados o unidades) para cada paquete de trabajo antes de iniciarlo.
   * **Criterio 11:** Limitar estrictamente la categoría de **Esfuerzo de Nivel (*Level of Effort - LOE*)** a actividades de soporte continuo (p. ej. PMO o administración), donde $EV = PV$ por definición, evitando usarla en desarrollo para que no oculte retrasos técnicos.
   * **Criterio 12:** Establecer presupuestos y controles organizativos separados para los costes indirectos (*Overhead*).
   * **Criterio 13:** Identificar y controlar por separado la **Reserva de Gestión (*Management Reserve - MR*)** y el **Presupuesto No Distribuido (*Undistributed Budget - UB*)**, garantizando que la suma de la $PMB$ más $MR$ iguale el presupuesto contractual total del proyecto.
3. **Grupo 3 · Evaluación del Progreso y Recopilación de Datos (3 Criterios):**
   * **Criterio 14:** Registrar todos los costes directos en el libro mayor de forma totalmente consistente y alineada con las mismas Cuentas de Control y periodos en los que se imputa el $EV$.
   * **Criterio 15:** Determinar objetivamente el Valor Ganado ($EV$) en cada fecha de corte aplicando exactamente las reglas fijadas en el Criterio 10 sobre los entregables realmente completados.
   * **Criterio 16:** Contabilizar el coste real de materiales y subcontratos por devengo y consumo real en el proyecto, evitando distorsiones derivadas de anticipos o retrasos administrativos en el pago de facturas.
4. **Grupo 4 · Análisis e Informes de Gestión (5 Criterios):**
   * **Criterio 17:** Generar periódicamente (al menos de forma mensual) a nivel de Cuenta de Control las varianzas de coste ($CV$), cronograma ($SV$) y los índices $CPI$ y $SPI$.
   * **Criterio 18:** Identificar y documentar la causa raíz, el impacto técnico y las implicaciones financieras de toda varianza que supere los umbrales de tolerancia fijados por la PMO.
   * **Criterio 19:** Monitorizar y resumir el desempeño de los costes indirectos frente a su presupuesto asignado.
   * **Criterio 20:** Implementar, asignar responsables y hacer seguimiento de planes de acción correctiva (*Crashing, Fast-Tracking, Descope*) hasta el cierre de la desviación.
   * **Criterio 21:** Revisar periódicamente las estimaciones de trabajo remanente y recalcular las proyecciones a la finalización ($EAC$ y $VAC$) considerando el desempeño histórico ($CPI/SPI$) y los riesgos pendientes, informando con transparencia al Consejo.
5. **Grupo 5 · Revisiones y Mantenimiento de Datos (6 Criterios):**
   * **Criterio 22:** Incorporar de forma disciplinada y oportuna todos los cambios de alcance, plazo o presupuesto debidamente autorizados en la $PMB$.
   * **Criterio 23:** Mantener una conciliación auditable entre los presupuestos actuales de las Cuentas de Control y el presupuesto contractual original.
   * **Criterio 24:** Prohibir cambios retroactivos en datos históricos ($PV$, $EV$ o $AC$ de periodos ya cerrados), salvo correcciones documentadas de errores contables o ajustes contractuales formales.
   * **Criterio 25:** Impedir transferencias arbitrarias de presupuesto o costes entre Cuentas de Control para maquillar ineficiencias de un área con los ahorros de otra.
   * **Criterio 26:** Documentar todo movimiento de entrada o liberación de fondos desde la Reserva de Gestión (*MR*) y el Presupuesto No Distribuido (*UB*).
   * **Criterio 27:** Ejecutar una re-planificación formal por encima de la línea base original (*Over Target Baseline - OTB* u *Over Target Schedule - OTS*) únicamente bajo autorización formal del cliente o Comité Ejecutivo cuando el análisis $TCPI$ demuestra que el plan original ha dejado de ser viable para gobernar el trabajo pendiente.

---

## 8. Aplicación del EVM en Entornos Híbridos (*Agile-EVM* según el PMBOK)

Una de las objeciones más frecuentes que enfrentan los directores de PMO al proponer el estándar EVM en empresas tecnológicas actuales es la aparente contradicción con el desarrollo ágil: *"Nosotros trabajamos con Scrum, Kanban y Sprints de dos semanas donde el backlog evoluciona; ¿no es el EVM una herramienta rígida exclusiva de proyectos en cascada?"*

La **7ª Edición del PMBOK (*Measurement Performance Domain*)** y la *Agile Practice Guide* del PMI refutan rotundamente ese mito, estableciendo el patrón **Agile-EVM (o EVM Híbrido)** como estándar de gobierno en organizaciones modernas.

En un proyecto híbrido real coexisten dos necesidades legítimas:
* **La necesidad del CFO y el Comité de Inversiones (Capa Macro):** Gobernar el presupuesto CAPEX/OPEX autorizado ($BAC$), controlar el ritmo de consumo de caja mensual ($AC$), vigilar los hitos regulatorios o de lanzamiento comercial y proyectar el coste final a la conclusión ($EAC$).
* **La necesidad de los Equipos de Producto e Ingeniería (Capa Micro):** Trabajar en iteraciones cortas (*Sprints* de 2 semanas), mantener un *Product Backlog* vivo y priorizar historias de usuario según el máximo retorno (conectado directamente con la [Matriz RICE & ICE de Priorización Ágil](/es/posts/matriz-rice-ice-priorizacion/)).

### 8.1 Arquitectura de Gobernanza Financiera EVM + Entregas Iterativas

Para acoplar ambos mundos sin generar burocracia innecesaria en los desarrolladores, las métricas EVM **se miden a nivel de Release, Épica de Negocio o Cuenta de Control**, y se alimentan automáticamente al cierre de cada Sprint sin pedir reportes manuales de horas por tarea:

1. **Línea Base de Release ($BAC$ y $SP_{\text{total}}$):** Antes de arrancar una Release o Incremento de Programa (p. ej. 6 Sprints = 12 semanas), se aprueba un presupuesto autorizado ($BAC$, por ejemplo $300.000\text{ €}$) para el conjunto de capacidades del backlog inicial estimado en $SP_{\text{total}}$ puntos de historia (por ejemplo, $300\text{ Story Points}$). De este modo, cada punto de historia adquiere un valor presupuestario estándar:
   $$V_{SP} = \frac{BAC}{SP_{\text{total}}} = \frac{300.000\text{ €}}{300\text{ SP}} = 1.000\text{ € / SP}$$
2. **Valor Planificado al Sprint $t$ ($PV_t$):** Se calcula multiplicando el $BAC$ por el porcentaje de puntos que la velocidad planificada del equipo preveía completar hasta la iteración $t$:
   $$PV_t = BAC \times \frac{\sum_{k=1}^{t} SP_{\text{plan}, k}}{SP_{\text{total}}}$$
3. **Valor Ganado al Sprint $t$ ($EV_t$) bajo Regla 0/100 y *Definition of Done (DoD)*:** Aquí reside la sinergia perfecta entre Scrum y la Directriz 15 de la EIA-748. Una historia de usuario al "80% de desarrollo" que no ha pasado QA ni ha sido aceptada en la *Sprint Review* computa **0 puntos ganados**. Solo los puntos de historias que cumplen al 100% la *Definition of Done* ($SP_{\text{done}, k}$) generan Valor Ganado:
   $$EV_t = BAC \times \frac{\sum_{k=1}^{t} SP_{\text{done}, k}}{SP_{\text{total}}}$$
4. **Coste Real al Sprint $t$ ($AC_t$):** En equipos ágiles estables, el cálculo contable es trivial y ultrarrápido: es la suma del coste fijo del *squad* por Sprint (*Team Burn Rate*, ej. $48.000\text{ €/Sprint}$) más las licencias cloud o APIs imputadas al incremento.

### 8.2 Tabla de Equivalencias: EVM Clásico (Cascada) vs. Agile-EVM Híbrido (PMBOK)

| Elemento de Gobernanza | EVM Tradicional (Cascada / Ingeniería) | Agile-EVM Híbrido (PMBOK 7th Edition) |
| :--- | :--- | :--- |
| **Unidad de Línea Base ($PMB$)** | Paquetes de Trabajo WBS valorados en euros/horas hasta el cierre total. | Presupuesto por **Release / Program Increment (PI)** asociado a un volumen estimado de *Story Points* ($SP_{\text{total}}$). |
| **Frecuencia de Medición ($Status Date$)** | Corte mensual alineado con cierre contable. | Al término de cada **Sprint** (cada 2 semanas) coincidiendo con la *Sprint Review*, consolidado mensualmente para el CFO. |
| **Imputación del Avance ($EV$)** | Reglas $0/100$, $50/50$, Hitos Ponderados por paquete WBS. | **Regla $0/100$ estricta mediante la *Definition of Done (DoD)*:** historia en WIP = 0% $EV$; historia aceptada = 100% $EV$. |
| **Significado del $SPI$** | Velocidad de avance respecto al diagrama de Gantt / Camino Crítico. | $\text{Velocidad Real Acumulada} / \text{Velocidad Planificada}$ (eficiencia de flujo del equipo). |
| **Significado del $CPI$** | Eficiencia de gasto sobre el presupuesto de los entregables construidos. | Coste real por *Story Point* completado frente al coste estándar planificado por punto ($V_{SP}$). |
| **Gestión de Cambios de Alcance** | Solicitud formal de cambio (*Change Request*) aprobada por comité antes de ejecutar. | ***Scope Swapping*:** sustituir una historia no iniciada de $8\text{ SP}$ por otra nueva de $8\text{ SP}$ mantiene intactos $BAC$ y $SP_{\text{total}}$. |

### 8.3 Protocolo ante Cambios de Backlog (*Scope Swapping* vs. *Scope Creep*)

La regla de oro en entornos híbridos para no corromper la matemática del EVM ante el CFO es distinguir entre **intercambio de alcance** y **ampliación de alcance**:
* **Si el Product Owner sustituye alcance equivalente (*Scope Swapping*):** Entra una funcionalidad urgente de 13 puntos y sale otra no iniciada de 13 puntos. El denominador $SP_{\text{total}}$ y el presupuesto $BAC$ permanecen invariables: la medición de $CPI$ y $SPI$ no sufre distorsión alguna.
* **Si el negocio exige añadir nuevas épicas sin retirar alcance (*Scope Creep*):** Aumenta $SP_{\text{total}}$ sin aumentar proporcionalmente el $BAC$ (lo que diluiría el $V_{SP}$ y generaría una caída falsa del $EV$ en el trabajo ya hecho), o bien se autoriza una liberación formal de presupuesto desde la **Reserva de Gestión (*MR*)** hacia la Cuenta de Control de la Release, actualizando la línea base conforme a los criterios 22 y 26 de la EIA-748.

---

## 9. Caso de Estudio: Rescate Operativo de un Megaproyecto de 1,2M €

Para comprobar cómo se traslada esta metodología a la mesa de decisiones directivas, analicemos el caso real de modernización del motor transaccional de pagos implementado en el **Executive Decision Pack**:

### 9.1 Diagnóstico en la Fecha de Corte (Mes 6)
Al revisar los 25 paquetes de trabajo de la WBS en la Pestaña 2 del modelo analítico, el análisis de Pareto revela que **tres entregables concretos concentran el 75% del sobrecoste acumulado**:
* **WBS 2.1 (Motor Transaccional de Conciliación):** $CV = -20.000 \text{ €}$, $CPI = 0.83$. Causa: Complejidad técnica imprevista en la consistencia de microservicios distribuidos.
* **WBS 2.3 (Módulo de Procesamiento de Pagos):** $CV = -13.000 \text{ €}$, $CPI = 0.87$. Causa: Retrasos de homologación externa con las pasarelas bancarias.
* **WBS 3.1 (Conector ERP Core SAP):** $CV = -13.000 \text{ €}$, $CPI = 0.81$. Causa: Desviación de alcance en mapeo de tablas legacy y coste inflado de consultores externos Time & Materials.

### 9.2 El Plan de Acción y Recuperación Aprobado
En lugar de aceptar pasivamente un desvío de casi 200.000 € ($EAC_1$), el comité de dirección activa tres palancas coordinadas:
1. **Crashing Técnico Selectivo (+24.000 € inversión):** Contratación de 2 arquitectos senior especialistas durante 6 semanas para resolver el motor transaccional ($\Delta SPI = +0.05, \Delta CPI = +0.04$).
2. **Fast-Tracking en Homologación:** Paralelización de pruebas sandbox bancarias con las auditorías de ciberseguridad, recortando 2,5 semanas de retraso crítico ($\Delta SPI = +0.06$).
3. **Descope Negociado y Precio Cerrado:** Diferir la sincronización secundaria del CRM Salesforce a una fase posterior post-lanzamiento (ahorro de 35.000 € de CAPEX) y congelar contratos Time & Materials de SAP exigiendo precio cerrado por entregable ($\Delta CPI = +0.08$).

### 9.3 Resultado Final Auditado al Cierre (Mes 12)
Gracias a la intervención basada en EVM, el proyecto se estabilizó: finalizó el 100% de los entregables nucleares con un coste final real de **1.248.000 €** (absorbiendo apenas un 4% de contingencia en lugar de los 195.000 € proyectados) y con solo una semana de desviación temporal frente a la fecha objetivo.

---

## 10. Protocolo de Defensa ante el Comité de Dirección (Boardroom FAQ)

Defender métricas de EVM ante un Consejo de Administración o un CFO exige anticipar tres preguntas clásicas de alta dirección:

### FAQ 1: "¿Por qué el SPI vuelve asintóticamente a 1.00 al terminar el proyecto aunque lleve meses o años de retraso?"
**Respuesta:** Es una peculiaridad matemática del EVM tradicional en moneda: al completarse el proyecto, todo el trabajo planificado se termina finalmente, por lo que $EV = BAC$ y $PV = BAC$, forzando que $SPI = \frac{BAC}{BAC} = 1.00$. Para solventar esta anomalía en fases finales, el PMBOK y Lipke (2003) introducen el **Cronograma Ganado (Earned Schedule - ES)**, que mide el retraso en unidades de tiempo reales ($SV_t = ES - AT$) en lugar de moneda.

### FAQ 2: "¿Cómo explicar al CFO que un TCPI > 1.15 es una fantasía estadística?"
**Respuesta:** La evidencia empírica de miles de proyectos (Fleming & Koppelman, 2010; Christensen, 1998) demuestra que la productividad de un equipo es altamente inelástica una vez superado el primer quinto del proyecto. Exigir a un equipo que opere a un rendimiento superior al 115% cuando ha venido rindiendo a $0.86$ requiere un cambio radical de metodología o alcance; mantener el plan sin cambios garantiza el incumplimiento.

### FAQ 3: "¿Cuándo está formalmente justificado aprobar un re-baselining presupuestario?"
**Respuesta:** El re-baselining nunca debe ser una vía de escape para maquillar ineficiencias de gestión (Criterio 24 EIA-748). Solo está legitimado cuando: (a) Se producen ampliaciones de alcance aprobadas por el cliente o el Consejo, (b) Surgen cambios regulatorios o macroeconómicos imprevistos, o (c) El $TCPI_{BAC} > 1.15$ demuestra que el objetivo original destruirá los estándares de calidad del producto final.

---

## 11. El Executive Decision Pack: Tu Infraestructura EVM Lista para Producción

Para los directores de operaciones, CFOs, PMOs, consultores y ejecutivos que necesitan implementar este estándar analítico de inmediato sin invertir semanas en el desarrollo y validación de fórmulas estadísticas y curvas S, en Datalaria hemos construido el **Executive Decision Pack oficial**:

{{< product-card
  title="Cuadro de Mando EVM / Valor Ganado (Curva S)"
  category="Control de Costes & Plazo"
  price="8€"
  original_price="25€"
  badge="📉 Control Operativo"
  icon="📉"
  preview_image="preview-pack.png"
  preview_caption="Vista previa real de los entregables incluidos: Cuadro de Mando EVM en Excel (.xlsx) con Curva S nativa M01-M12, modelos EAC₁/EAC₂/EAC₃, test TCPI y control de 25 paquetes WBS, Guía Metodológica Oficial (.pdf) y Presentación C-Level (.pptx 16:9 Widescreen)."
  deliverables="Excel .xlsx + Sheets|PowerPoint .pptx 16:9 C-Level|Guía Metodológica PDF"
  features="Seguimiento automatizado: PV (Valor Planificado), EV (Valor Ganado) y AC (Coste Real)|Índices de rendimiento en tiempo real: CPI (Cost Performance Index) y SPI (Schedule)|Generación de la Curva S ejecutiva con proyección EAC (Estimación a la Finalización)|Slide PPTX C-Level con estado de salud financiero del proyecto|Descarga directa inmediata (.ZIP con versiones ES y EN)"
  checkout_url="https://datalaria.lemonsqueezy.com/checkout/buy/188950c2-0fd9-4331-919f-237880e2c78b"
  button_text="Descargar Pack Completo (.ZIP) • 8€"
>}}
El cuadro de mando definitivo para la dirección de proyectos. Muestra con precisión quirúrgica si un proyecto terminará a tiempo y dentro del presupuesto, calculando el coste final proyectado (EAC).
{{< /product-card >}}

El libro analítico en Excel incluye celdas de entrada 100% editables (fondo blanco) y fórmulas financieras protegidas bajo contraseña proporcionada en las instrucciones (estándar OpenXML ECMA-376). Incluye la presentación ejecutiva panorámica 16:9 widescreen en PowerPoint estructurada bajo la Pirámide de Minto y la guía metodológica editorial de 5 páginas en PDF.

El archivo comprimido maestro incluye las versiones completas y auditadas en **Español** e **Inglés**, manuales de importación nativa a **Google Sheets** y documentación técnica para su despliegue inmediato.

---

## 12. Referencias Bibliográficas Canónicas de Autoridad

1. **Project Management Institute (PMI) (2021).** *A Guide to the Project Management Body of Knowledge (PMBOK Guide) – 7th Edition & The Standard for Earned Value Management (2019)*. Project Management Institute, Newtown Square, PA.  
   *El estándar internacional canónico que formaliza el dominio de medición, el EVM híbrido/ágil, las ecuaciones de varianza y los modelos predictivos EAC y TCPI.* ISBN: `978-1628256642` / `978-1628256383`.

2. **Wanner, Roland (2026).** *EIA-748 and 27 Earned Value Management Systems (EVMS) Guidelines*. Roland Wanner Project Control.  
   *Análisis detallado de la modernización de la norma desde los 32 criterios históricos hasta las 27 directrices EVMS vigentes en cinco grupos de procesos.* Enlace: [rolandwanner.com/eia-748-and-27-earned-value-management-systems-evms-guidelines/](https://rolandwanner.com/eia-748-and-27-earned-value-management-systems-evms-guidelines/).

3. **SAE International / National Defense Industrial Association (NDIA) (2026).** *EIA-748-E: Earned Value Management Systems Standard (27 Guidelines)*. Arlington, VA.  
   *La norma de la industria aeroespacial, defensa e ingeniería compleja que consolida los 27 criterios oficiales de auditoría y control de sistemas EVMS.*

4. **Fleming, Q. W., & Koppelman, J. M. (2010).** *Earned Value Project Management – 4th Edition*. Project Management Institute.  
   *La obra de referencia definitiva que consolidó la aplicación práctica de EVM en contratos corporativos, tecnológicos y gubernamentales.* ISBN: `978-1935589082`.

5. **Kerzner, H. (2017).** *Project Management: A Systems Approach to Planning, Scheduling, and Controlling – 12th Edition*. John Wiley & Sons.  
   *Tratado universitario y directivo sobre integración de líneas base de desempeño, control financiero de grandes programas y gobierno PMO.* ISBN: `978-1119165354`.

6. **Christensen, D. S. (1998).** *The Costs and Benefits of Implementing an Earned Value Management System*. Acquisition Review Quarterly, Vol. 5, No. 4, pp. 373-386.  
   *Estudio empírico fundamental que demostró la estabilidad estadística del CPI acumulado a partir del 20% de avance físico del proyecto.*

7. **Barbara Minto (2009).** *The Pyramid Principle: Logic in Writing and Thinking*. Financial Times / Prentice Hall.  
   *La metodología de comunicación ejecutiva y estructuración jerárquica de argumentos aplicada en las firmas de consultoría estratégica Tier-1.* ISBN: `978-0273710516`.
