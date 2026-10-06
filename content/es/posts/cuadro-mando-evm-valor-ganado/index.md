---
title: "Cuadro de Mando EVM: Valor Ganado, Curva S y Proyecciones EAC de Grado Consejo de Administración"
date: 2026-11-05
draft: false
categories: ["Control Operativo", "Project Finance", "Plantillas Ejecutivas"]
tags: ["Valor Ganado", "EVM", "ANSI/EIA-748", "Curva S", "CPI", "SPI", "EAC", "TCPI", "Control Operativo", "Project Management", "PMBOK", "C-Level"]
description: "Guía metodológica y cuantitativa de Earned Value Management (EVM / ANSI/EIA-748): superación de la trampa contable tradicional, curvas S ejecutivas, varianzas CV/SV, índices CPI/SPI, modelos predictivos de coste final EAC y cálculo del índice de rendimiento para completar TCPI ante el Consejo de Administración."
summary: "Erradica las sorpresas presupuestarias y los retrasos ocultos a mitad de proyecto con el estándar internacional de Earned Value Management (EVM / ANSI/EIA-748). Cuantifica el avance físico real (EV), audita la eficiencia de gasto (CPI) y de cronograma (SPI), traza la Curva S ejecutiva y proyecta el coste final a la conclusión (EAC) listo para defender en comité de dirección."
---

En comités de dirección ejecutiva (*Executive Committee*), consejos de administración y comités de inversiones, directores generales (CEOs), directores financieros (CFOs), directores de operaciones (COOs) y directores de oficina de proyectos (PMOs) presencian de forma recurrente una de las patologías financieras y organizativas más costosas del mundo corporativo: **la trampa de la contabilidad tradicional en la gestión de proyectos estratégicos**.

Imaginemos un megaproyecto de transformación tecnológica, migración cloud o infraestructura crítica con un presupuesto aprobado ($BAC$) de **1.200.000 €** y un cronograma de ejecución de 12 meses. Al cumplirse el **Mes 6** (exactamente la mitad del plazo temporal previsto), el departamento de contabilidad y control de gestión emite su informe financiero oficial:

> *"A fecha de corte, el proyecto ha consumido 600.000 € frente a un presupuesto total de 1.200.000 €. Habiendo transcurrido el 50% del tiempo y habiéndose devengado el 50% de los fondos, el proyecto se encuentra estrictamente dentro del presupuesto y en orden."*

La alta dirección respira aliviada. Sin embargo, cinco meses más tarde, en el mes 11, salta la alarma ejecutiva: el presupuesto inicial de 1,2M € se ha agotado por completo, pero los entregables clave del sistema se encuentran inacabados, las pruebas de integración están bloqueadas y el equipo técnico solicita una inyección urgente de 300.000 € adicionales y una prórroga de cuatro meses para evitar el colapso operativo.

Ante el desconcierto y la irritación del Consejo de Administración, surge la pregunta inevitable: **¿cómo es posible que un proyecto que marchaba 'perfectamente en presupuesto' a mitad de plazo se convierta en una catástrofe financiera semanas antes del cierre?**

La respuesta es demoledora: **el proyecto nunca estuvo bien**. La contabilidad financiera tradicional reportó una ficción matemática. Medir únicamente el dinero gastado ($AC$) frente al calendario transcurrido ignora la única variable que define el éxito de una inversión: **cuánto valor físico real se ha producido a cambio de esos 600.000 €**.

Si a mitad de plazo se han gastado 600.000 € pero el equipo solo ha completado el 43% de los entregables reales (un valor físico de 516.000 €), el proyecto arrastraba ya en el Mes 6 un sobrecoste neto de 84.000 € y casi un mes de retraso no confesado. Por cada euro desembolsado, la organización solo obtenía 0,86 € de avance real.

Para erradicar este punto ciego y dotar a la gobernanza corporativa de un estándar cuantitativo de grado Consejo de Administración, el Departamento de Defensa de los Estados Unidos (DoD), el estándar industrial **ANSI/EIA-748-D** y el **Project Management Institute (PMI)** en el estándar **The Standard for Earned Value Management** formalizan la metodología de **Gestión del Valor Ganado (Earned Value Management - EVM)**.

En este artículo maestro desglosamos la arquitectura matemática completa de EVM, el trazado de la Curva S ejecutiva, el diagnóstico de varianzas e índices de rendimiento ($CPI, SPI$), los tres modelos matemáticos de proyección al cierre ($EAC$), el cálculo del índice de rendimiento para completar ($TCPI$) y el protocolo de defensa ante el CFO y el Consejo de Administración.

---

## 1. El Pipeline de Control Financiero y Operativo EVM

El estándar EVM no es un simple informe de control de gestión retrospectivo; es un **sistema predictivo de alerta temprana y gobierno de inversiones** que conecta el desglose físico del trabajo (WBS) con la tesorería corporativa:

{{< mermaid >}}
flowchart TD
    A["<b>1. Línea Base del Desempeño (PMB)</b><br/><small>Estructura WBS descompuesta en entregables tangibles<br/>Presupuesto total autorizado a la finalización (BAC)</small>"]
    
    B["<b>2. Curva de Valor Planificado (PV)</b><br/><small>Distribución temporal del presupuesto por hitos y meses<br/>PV = BAC × % Planificado a la fecha de corte</small>"]
    
    C["<b>3. Medición del Avance Físico Real</b><br/><small>Imputación objetiva de avance (Reglas 0/100, 50/50, Hitos)<br/>Eliminación del 'síndrome del 90% infinito'</small>"]
    
    D["<b>4. Cálculo del Valor Ganado (EV)</b><br/><small>Presupuesto autorizado del trabajo completado<br/>EV = BAC × % Avance Físico Real</small>"]
    
    E["<b>5. Registro del Coste Real Incurrido (AC)</b><br/><small>Facturas aprobadas, horas/hombre directas, CAPEX devengado<br/>AC = Contabilidad analítica de costes</small>"]
    
    F["<b>6. Motor de Varianzas e Índices</b><br/><small>Varianza Coste: CV = EV - AC  |  CPI = EV / AC<br/>Varianza Cronograma: SV = EV - PV  |  SPI = EV / PV</small>"]
    
    G{"<b>7. Evaluación de Salud Operativa</b><br/><small>Matriz 2x2: ¿CPI ≥ 1.00 y SPI ≥ 1.00?<br/>Diagnóstico de alertas en Cuadrantes 1 a 4</small>"}
    
    H["<b>ZONA DE ALERTA O CRISIS</b><br/><small>Modelos predictivos EAC (Típico, Atípico, Compuesto)<br/>Cálculo de esfuerzo remanente TCPI vs BAC</small>"]
    
    I["<b>8. Plan de Recuperación & Board Gateway</b><br/><small>Fast-Tracking, Crashing, Descope negociado<br/>Re-baselining formal con aprobación del Consejo</small>"]

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

## 2. Fundamentación Matemática del Estándar EVM (ANSI/EIA-748)

Para que el control presupuestario y temporal sea auditable y computable sin ambigüedades, el estándar EVM define con rigor axiomático tres variables canónicas, dos ecuaciones de varianza, dos índices de eficiencia y un conjunto de modelos de extrapolación estadística.

### 2.1 Las Tres Variables Canónicas

Todo el edificio analítico de EVM se apoya sobre tres dimensiones monetarias evaluadas a una misma fecha de corte (*Status Date* o *Data Date*):

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
$$EV = BAC \times \% \text{Avance Físico Real}$$

> **Principio de Oro de EVM:** El Valor Ganado se calcula siempre multiplicando el presupuesto original ($BAC$) por el avance físico real completado. **Nunca** se calcula en función de las horas invertidas ni de las facturas pagadas. Si una tarea presupuestada en 100.000 € se encuentra ejecutada al 40%, su $EV$ es exactamente 40.000 €, independientemente de que se hayan gastado 20.000 € o 90.000 €.

#### D. Coste Real Incurrido ($AC$ - Actual Cost)
Conocido históricamente como **ACWP** (*Actual Cost of Work Performed*), el **Actual Cost ($AC$)** es el coste total devengado y registrado por la contabilidad de la empresa para ejecutar el trabajo realizado hasta la fecha de corte:
$$AC = \text{Costes Directos de Personal} + \text{Facturas de Contratistas} + \text{Licencias} + \text{CAPEX Imputado}$$

---

### 2.2 Ecuaciones de Varianzas: Diagnóstico Absoluto en Moneda

El contraste directo entre estas tres variables permite aislar con precisión de bisturí los dos grandes problemas de cualquier iniciativa: si el proyecto está gastando de más (problema de coste) o si va con retraso (problema de plazo).

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

### 2.3 Índices de Rendimiento Operativo: Eficiencia Relativa ($CPI$ y $SPI$)

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

## 3. Matriz de Salud Operativa 2x2: Diagnóstico Cruzado $CPI$ vs $SPI$

Para la alta dirección y los comités de inversión, la combinación de $CPI$ y $SPI$ define cuatro cuadrantes operacionales inequívocos que dictan el nivel de gobernanza requerido:

{{< mermaid >}}
flowchart TD
    subgraph CUADRANTE_2["<b>CUADRANTE 2: ALERTA PLAZO</b><br/>CPI ≥ 1.00 | SPI < 1.00"]
        Q2["Bajo presupuesto pero con retraso cronológico.<br/><i>Riesgo:</i> Holguras consumidas y penalizaciones contractuales.<br/><i>Acción:</i> Crashing selectivo con el ahorro de costes disponible."]
    end

    subgraph CUADRANTE_1["<b>CUADRANTE 1: ZONA SALUDABLE</b><br/>CPI ≥ 1.00 | SPI ≥ 1.00"]
        Q1["En tiempo y dentro de presupuesto.<br/><i>Estado:</i> Productividad óptima y gobernanza estándar.<br/><i>Acción:</i> Monitorización preventiva y mantenimiento de ritmo."]
    end

    subgraph CUADRANTE_4["<b>CUADRANTE 4: ZONA DE CRISIS ★</b><br/>CPI < 1.00 | SPI < 1.00"]
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

## 4. Modelos Matemáticos de Proyección a la Finalización: $EAC$, $VAC$ y $TCPI$

Uno de los mayores aportes de EVM ante el Consejo de Administración es su capacidad para responder a la pregunta que todo CFO y CEO formula: **"¿Cuánto nos va a costar realmente terminar este proyecto y cuándo estará terminado?"**

Para responder, EVM no recurre a estimaciones intuitivas; implementa tres modelos matemáticos de **Estimación a la Finalización ($EAC$ - Estimate at Completion)** según las hipótesis operativas asumidas:

### 4.1 Modelo 1: Escenario Típico ($EAC_1$ - Manteniendo la Eficiencia Actual)
Asume que la ineficiencia o sobrecoste observado hasta la fecha es estructural y que el trabajo remanente se ejecutará con el mismo rendimiento de coste ($CPI$) registrado:
$$EAC_1 = \frac{BAC}{CPI}$$

En nuestro proyecto de 1.200.000 €:
$$EAC_1 = \frac{1.200.000}{0,86} = \mathbf{1.395.349 \text{ €}}$$

Este modelo anticipa que el proyecto terminará costando casi **1,4 millones de euros**, lo que supone un sobrecoste de casi 200.000 €.

### 4.2 Modelo 2: Escenario Atípico ($EAC_2$ - Las Desviaciones Pasadas Fueron Puntuales)
Asume que las desviaciones sufridas se debieron a eventos singulares e irrepetibles (un bloqueo puntual de proveedores o un error inicial de arquitectura ya resuelto) y que todo el trabajo restante se completará exactamente al coste planificado original ($1,00$ de eficiencia):
$$EAC_2 = AC + (BAC - EV)$$

En nuestro caso:
$$EAC_2 = 600.000 + (1.200.000 - 516.000) = 600.000 + 684.000 = \mathbf{1.284.000 \text{ €}}$$

Incluso en este escenario optimista, el proyecto requiere **84.000 € más** de lo presupuestado.

### 4.3 Modelo 3: Escenario Crítico o Compuesto ($EAC_3$ - Impacto Combinado de Coste y Retraso)
En megaproyectos tecnológicos y de ingeniería, los retrasos cronológicos casi nunca son gratuitos: conllevan el pago continuado de nóminas, licencias de infraestructura cloud devengadas por mes, alquileres de servidores y posibles penalizaciones contractuales por entrega tardía. El modelo compuesto penaliza el coste futuro dividiendo el trabajo remanente por el producto de $CPI \times SPI$:
$$EAC_3 = AC + \frac{BAC - EV}{CPI \times SPI}$$

En nuestro proyecto:
$$EAC_3 = 600.000 + \frac{684.000}{0,86 \times 0,86} = 600.000 + \frac{684.000}{0,7396} = 600.000 + 924.824 = \mathbf{1.524.824 \text{ €}}$$

Si la organización no corrige de inmediato el retraso y el sobrecoste simultáneos, el coste final puede desbordarse en más de **324.000 € adicionales**.

---

### 4.4 Varianza a la Conclusión ($VAC$ - Variance at Completion)
Representa la diferencia final proyectada entre el presupuesto autorizado ($BAC$) y el coste proyectado ($EAC$):
$$VAC = BAC - EAC$$

Para el escenario típico:
$$VAC_1 = 1.200.000 - 1.395.349 = \mathbf{-195.349 \text{ €}}$$

El signo negativo indica que la empresa enfrentará un **déficit presupuestario de 195.349 €**, cifra exacta que debe reservarse o negociarse en el comité de dirección.

---

### 4.5 El Índice de Rendimiento para Completar ($TCPI$): El Test de Realidad Estadística

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

## 5. Reglas Operativas para Imputar el Avance Físico ($EV$) sin Sesgos

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

## 6. Caso de Estudio: Rescate Operativo de un Megaproyecto de 1,2M €

Para comprobar cómo se traslada esta metodología a la mesa de decisiones directivas, analicemos el caso real de modernización del motor transaccional de pagos implementado en el **Executive Decision Pack**:

### 6.1 Diagnóstico en la Fecha de Corte (Mes 6)
Al revisar los 25 paquetes de trabajo de la WBS en la Pestaña 2 del modelo analítico, el análisis de Pareto revela que **tres entregables concretos concentran el 75% del sobrecoste acumulado**:
* **WBS 2.1 (Motor Transaccional de Conciliación):** $CV = -20.000 \text{ €}$, $CPI = 0.83$. Causa: Complejidad técnica imprevista en la consistencia de microservicios distribuidos.
* **WBS 2.3 (Módulo de Procesamiento de Pagos):** $CV = -13.000 \text{ €}$, $CPI = 0.87$. Causa: Retrasos de homologación externa con las pasarelas bancarias.
* **WBS 3.1 (Conector ERP Core SAP):** $CV = -13.000 \text{ €}$, $CPI = 0.81$. Causa: Desviación de alcance en mapeo de tablas legacy y coste inflado de consultores externos Time & Materials.

### 6.2 El Plan de Acción y Recuperación Aprobado
En lugar de aceptar pasivamente un desvío de casi 200.000 € ($EAC_1$), el comité de dirección activa tres palancas coordinadas:
1. **Crashing Técnico Selectivo (+24.000 € inversión):** Contratación de 2 arquitectos senior especialistas durante 6 semanas para resolver el motor transaccional ($\Delta SPI = +0.05, \Delta CPI = +0.04$).
2. **Fast-Tracking en Homologación:** Paralelización de pruebas sandbox bancarias con las auditorías de ciberseguridad, recortando 2,5 semanas de retraso crítico ($\Delta SPI = +0.06$).
3. **Descope Negociado & Precio Cerrado:** Diferir la sincronización secundaria del CRM Salesforce a una fase posterior post-lanzamiento (ahorro de 35.000 € de CAPEX) y congelar contratos Time & Materials de SAP exigiendo precio cerrado por entregable ($\Delta CPI = +0.08$).

### 6.3 Resultado Final Auditado al Cierre (Mes 12)
Gracias a la intervención basada en EVM, el proyecto se estabilizó: finalizó el 100% de los entregables nucleares con un coste final real de **1.248.000 €** (absorbiendo apenas un 4% de contingencia en lugar de los 195.000 € proyectados) y con solo una semana de desviación temporal frente a la fecha objetivo.

---

Para los directores de operaciones, CFOs, PMOs, consultores y ejecutivos que necesitan implementar este estándar analítico de inmediato sin invertir semanas en el desarrollo y validación de fórmulas estadísticas y curvas S, en Datalaria hemos construido el **Executive Decision Pack oficial**:

{{< product-card
  title="Cuadro de Mando EVM / Valor Ganado (Curva S)"
  category="Control de Costes & Plazo"
  price="8€"
  original_price="25€"
  badge="📉 Control Operativo"
  icon="📉"
  deliverables="Excel .xlsx + Sheets|PowerPoint .pptx 16:9 C-Level|Guía Metodológica PDF"
  features="Seguimiento automatizado: PV (Valor Planificado), EV (Valor Ganado) y AC (Coste Real)|Índices de rendimiento en tiempo real: CPI (Cost Performance Index) y SPI (Schedule)|Generación de la Curva S ejecutiva con proyección EAC (Estimación a la Finalización)|Slide PPTX C-Level con estado de salud financiero del proyecto"
  checkout_url="https://datalaria.lemonsqueezy.com/buy/cuadro-mando-evm"
  button_text="Descargar Pack Completo (.ZIP) • 8€"
>}}
El cuadro de mando definitivo para la dirección de proyectos. Muestra con precisión quirúrgica si un proyecto terminará a tiempo y dentro del presupuesto, calculando el coste final proyectado (EAC).
{{< /product-card >}}

El libro analítico en Excel incluye celdas de entrada 100% editables (fondo blanco) y fórmulas financieras protegidas bajo contraseña proporcionada en las instrucciones (estándar OpenXML ECMA-376). Incluye la presentación ejecutiva panorámica 16:9 widescreen en PowerPoint estructurada bajo la Pirámide de Minto y la guía metodológica editorial de 5 páginas en PDF.

El archivo comprimido maestro incluye las versiones completas y auditadas en **Español** e **Inglés**, manuales de importación nativa a **Google Sheets** y documentación técnica para su despliegue inmediato.

---

## 7. Protocolo de Defensa ante el Comité de Dirección (Boardroom FAQ)

Defender métricas de EVM ante un Consejo de Administración o un CFO exige anticipar tres preguntas clásicas de alta dirección:

### FAQ 1: "¿Por qué el SPI vuelve asintóticamente a 1.00 al terminar el proyecto aunque lleve meses o años de retraso?"
**Respuesta:** Es una peculiaridad matemática del EVM tradicional en moneda: al completarse el proyecto, todo el trabajo planificado se termina finalmente, por lo que $EV = BAC$ y $PV = BAC$, forzando que $SPI = \frac{BAC}{BAC} = 1.00$. Para solventar esta anomalía en fases finales, el PMBOK y Lipke (2003) introducen el **Cronograma Ganado (Earned Schedule - ES)**, que mide el retraso en unidades de tiempo reales ($SV_t = ES - AT$) en lugar de moneda.

### FAQ 2: "¿Cómo explicar al CFO que un TCPI > 1.15 es una fantasía estadística?"
**Respuesta:** La evidencia empírica de miles de proyectos (Fleming & Koppelman, 2010; Christensen, 1998) demuestra que la productividad de un equipo es altamente inelástica una vez superado el primer quinto del proyecto. Exigir a un equipo que opere a un rendimiento superior al 115% cuando ha venido rindiendo a $0.86$ requiere un cambio radical de metodología o alcance; mantener el plan sin cambios garantiza el incumplimiento.

### FAQ 3: "¿Cuándo está formalmente justificado aprobar un re-baselining presupuestario?"
**Respuesta:** El re-baselining nunca debe ser una vía de escape para maquillar ineficiencias de gestión. Solo está legitimado cuando: (a) Se producen ampliaciones de alcance aprobadas por el cliente o el Consejo, (b) Surgen cambios regulatorios o macroeconómicos imprevistos, o (c) El $TCPI_{BAC} > 1.15$ demuestra que el objetivo original destruirá los estándares de calidad del producto final.

---

## 8. Referencias Bibliográficas Canónicas de Autoridad

1. **Project Management Institute (PMI) (2019).** *The Standard for Earned Value Management*. Project Management Institute, Newtown Square, PA.  
   *El estándar internacional canónico que formaliza la terminología, las ecuaciones de varianza y los modelos de proyección EAC y TCPI.* ISBN: `978-1628256383`.

2. **Fleming, Q. W., & Koppelman, J. M. (2010).** *Earned Value Project Management – 4th Edition*. Project Management Institute.  
   *La obra de referencia definitiva que consolidó la aplicación práctica de EVM en contratos corporativos y gubernamentales.* ISBN: `978-1935589082`.

3. **National Defense Industrial Association (NDIA) (2019).** *ANSI/EIA-748-D: Earned Value Management Systems Standard*. Arlington, VA.  
   *La norma de la industria aeroespacial y de defensa que establece los 32 criterios oficiales de auditoría y control de sistemas EVMS.*

4. **Kerzner, H. (2017).** *Project Management: A Systems Approach to Planning, Scheduling, and Controlling – 12th Edition*. John Wiley & Sons.  
   *Tratado universitario y directivo sobre integración de líneas base de desempeño y control financiero de grandes programas.* ISBN: `978-1119165354`.

5. **Christensen, D. S. (1998).** *The Costs and Benefits of Implementing an Earned Value Management System*. Acquisition Review Quarterly, Vol. 5, No. 4, pp. 373-386.  
   *Estudio empírico fundamental que demostró la estabilidad estadística del CPI a partir del 20% de avance físico del proyecto.*

6. **Barbara Minto (2009).** *The Pyramid Principle: Logic in Writing and Thinking*. Financial Times / Prentice Hall.  
   *La metodología de comunicación ejecutiva y estructuración jerárquica de argumentos aplicada en las firmas de consultoría estratégica Tier-1.* ISBN: `978-0273710516`.
