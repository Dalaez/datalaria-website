---
title: "Matriz DAR Cuantitativa: Criterios Veto, Ponderación Multicriterio y Análisis de Decisiones C-Level"
date: 2026-10-28
draft: false
categories: ["Toma de Decisiones", "Estrategia Corporativa", "Plantillas Ejecutivas"]
tags: ["Matriz DAR", "CMMI", "Kepner-Tregoe", "Toma de Decisiones", "Criterios Veto", "Scoring Multicriterio", "ERP", "Make vs Buy", "C-Level"]
description: "Guía metodológica y cuantitativa para implementar la matriz CMMI DAR (Decision Analysis and Resolution) y Kepner-Tregoe: filtros veto booleanos, scoring multicriterio ponderado, análisis de sensibilidad What-If y gobierno corporativo ante Consejos de Administración."
summary: "Transforma decisiones estratégicas de alta incertidumbre (selección de ERP/Cloud, M&A, contrataciones directivas o dilemas Make vs. Buy) en un proceso cuantitativo blindado, reproducible y libre de sesgos cognitivos. Este marco de estándar Tier-1 (McKinsey / CMMI DAR) combina filtros veto de exclusión implacable, matrices ponderadas de 4 pilares, pruebas de sensibilidad What-If y un Board Decision Gateway para Comités de Dirección."
---

En casi cualquier comité de inversiones, sesión extraordinaria de Consejo de Administración o comité de dirección tecnológica (CIO/CFO), surge inevitablemente el problema que en la consultoría estratégica de alta dirección denominamos **"la trampa de la última milla ejecutiva"**: 

Una corporación invierte cientos de horas de trabajo técnico, solicita complejas peticiones de oferta (RFP) a proveedores internacionales o analiza exhaustivamente objetivos de adquisición (*M&A* / *Make vs. Buy*). Sin embargo, al alcanzar la mesa del Consejo o del Comité Ejecutivo, **el proceso formal se desintegra**. La deliberación final degenera en un debate retórico dominado por la intuición visceral, el carisma comercial de un postor, el sesgo de confirmación de directores departamentales o compromisos políticos de compromiso mutuo.

Las consecuencias de este vacío metodológico son multimillonarias:
1. **El Síndrome de la Opción Barata:** Adjudicar un contrato crítico al proveedor con la menor cuota inicial de entrada (*sticker price*), ignorando que sus costes ocultos de parametrización, personalizaciones obligatorias y falta de soporte triplican el Coste Total de Propiedad (**TCO**) a 36 meses.
2. **La Compensación Ilícita de Deficiencias Graves:** Utilizar matrices sumatorias informales donde una puntuación sobresaliente en aspectos cosméticos o complementarios (ej. una interfaz de usuario atractiva o módulos adicionales gratuitos) "compensa" y oculta vulnerabilidades críticas inadmisibles (como la falta de certificación ISO 27001, latencias intolerables o la ausencia de soberanía de datos dentro de la Unión Europea).
3. **La Manipulación Ex-Post de Ponderaciones:** Alterar retroactivamente los pesos porcentuales de los criterios una vez abiertas las plicas económicas para forzar artificialmente la victoria del proveedor predilecto de un miembro del equipo gestor.

Para erradicar estas patologías y blindar la toma de decisiones estratégicas ante comités de auditoría, agencias reguladoras y consejos de administración, la ingeniería de sistemas complejos y la alta dirección corporativa desarrollaron dos metodologías canónicas complementarias: el área de proceso **CMMI DAR (Decision Analysis and Resolution)** y el método **Kepner-Tregoe (KT)**.

En esta guía metodológica oficial, formalizamos el motor matemático del modelo DAR, el protocolo de exclusión binaria mediante **Filtros Veto (*Must-Haves*)**, la calibración de **Ponderaciones Multicriterio (*Wants*)**, el test de sensibilidad marginal *What-If*, y la presentación ejecutiva estructurada bajo el principio de la **Pirámide de Minto**.

---

## 1. El Embudo de Decisión Metodológico CMMI DAR

El marco DAR no es un formulario burocrático de homologación de compras; es un **algoritmo de decisión secuencial y vinculante** diseñado para transformar la incertidumbre cualitativa en una recomendación cuantitativa auditable:

{{< mermaid >}}
flowchart TD
    A["<b>1. Encuadre Estratégico & Alternativas</b><br/><small>Identificación de la decisión crítica (ERP, M&A, Make vs. Buy)<br/>Definición formal de hasta 5 alternativas viables</small>"]
    
    B{"<b>2. Puerta de Filtros Veto (Must-Haves)</b><br/><small>Evaluación booleana de requisitos no negociables<br/>RGPD, Techo CAPEX, Plazo Go-Live, ISO 27001</small>"}
    
    C["<b>DESCALIFICACIÓN INAPELABLE</b><br/><small>Factor Booleano Vk = 0<br/>Exclusión automática del ranking (Score = 0)</small>"]
    
    D["<b>3. Scoring Multicriterio Ponderado (Wants)</b><br/><small>Evaluación de 13 criterios en 4 pilares estratégicos:<br/>Ajuste Técnico (30%) • TCO 3A (25%) • SLA (20%) • Seguridad (25%)</small>"]
    
    E["<b>4. Test de Sensibilidad What-If</b><br/><small>Simulación de estrés: +/- 20% Coste vs. Calidad Técnica<br/>Validación de robustez e invarianza del ranking ganador</small>"]
    
    F["<b>5. Board Decision Gateway (C-Level)</b><br/><small>Presentación ejecutiva 16:9 widescreen (Minto Pyramid)<br/>4 resoluciones vinculantes y firmas (CEO, CFO, CIO, CPO)</small>"]

    A --> B
    B -->|"Incumple 1 criterio (vi = 0)"| C
    B -->|"Cumple 100% criterios (Vk = 1)"| D
    D --> E
    E --> F

    style A fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px,color:#0F172A
    style B fill:#0F172A,stroke:#2563EB,stroke-width:2px,color:#FFFFFF
    style C fill:#FEE2E2,stroke:#EF4444,stroke-width:2px,color:#991B1B
    style D fill:#EFF6FF,stroke:#3B82F6,stroke-width:1.5px,color:#1E3A8A
    style E fill:#FEF3C7,stroke:#F59E0B,stroke-width:1.5px,color:#92400E
    style F fill:#D1FAE5,stroke:#10B981,stroke-width:2px,color:#065F46
{{< /mermaid >}}

---

## 2. Fundamentación Matemática del Modelo DAR

Para garantizar que el dictamen final resista el escrutinio de un Comité de Auditoría o un tribunal en disputas corporativas, la evaluación se apoya en un formalismo matemático riguroso compuesto por tres operadores: el **Filtro Booleano Veto**, la **Suma Ponderada Normalizada** y la **Derivada de Sensibilidad Marginal**.

### 2.1. El Filtro Booleano Veto (Gatekeeper No Negociable)

Sea un conjunto de $K$ alternativas analizadas, indexadas por $k \in \{1, \dots, K\}$, y un conjunto de $m$ criterios veto no negociables (*Must-Haves*).

Cada criterio veto se evalúa de manera estrictamente binaria como una variable de Bernoulli:

$$v_{ki} = \begin{cases} 1 & \text{si la alternativa } k \text{ cumple plenamente el requisito } i \\ 0 & \text{si la alternativa } k \text{ incumple el requisito } i \end{cases}$$

El **Factor de Viabilidad Veto ($V_k$)** de la alternativa $k$ es el producto booleano de todos sus filtros de exclusión:

$$V_k = \prod_{i=1}^m v_{ki} \in \{0, 1\}$$

$$\text{Propiedad de Exclusión Implacable: } \exists \, i \text{ tal que } v_{ki} = 0 \implies V_k = 0$$

Si una alternativa no supera aunque sea **un solo filtro veto**, su factor multiplicador es idénticamente cero ($V_k = 0$). Ninguna excelencia técnica, descuento comercial o prestigio de marca puede compensar un cero regulatorio u operativo.

### 2.2. Algoritmo de Scoring Multicriterio Normalizado (Wants)

Para las alternativas declaradas aptas en la fase veto ($V_k = 1$), el modelo evalúa $n$ criterios cuantitativos y cualitativos ponderados (*Wants*), estructurados en cuatro pilares estratégicos homogéneos.

Cada criterio $j \in \{1, \dots, n\}$ cuenta con:
* Un peso porcentual normalizado $w_j \in (0, 1)$ tal que:
$$\sum_{j=1}^n w_j = 1.00 \quad (100.0\%)$$
* Una calificación objetiva auditada $s_{kj} \in [1.0, 10.0]$ asignada a la alternativa $k$.

La **Puntuación Ponderada Base ($B_k$)** en escala de 0 a 100 puntos se define como:

$$B_k = 10 \cdot \sum_{j=1}^n w_j \cdot s_{kj}$$

La **Puntuación Final Efectiva ($S_k$)** de la alternativa $k$ resulta de la multiplicación escalar entre la viabilidad veto y la puntuación base:

$$S_k = V_k \cdot B_k = V_k \cdot \left[ 10 \cdot \sum_{j=1}^n w_j \cdot s_{kj} \right]$$

Si $V_k = 0$, entonces $S_k = 0.0$ automáticamente, excluyendo a la alternativa de la asignación de ranking.

### 2.3. Sensibilidad Marginal y Test de Robustez "What-If"

Para neutralizar acusaciones de arbitrariedad en la fijación de ponderaciones, el modelo calcula la **sensibilidad marginal** del score respecto al peso del criterio $j$:

$$\frac{\partial S_k}{\partial w_j} = 10 \cdot V_k \cdot s_{kj}$$

El **Gap de Decisión ($\Delta_{1,2}$)** entre la alternativa ganadora ($k^*$) y la segunda mejor opción ($k'$) viene dado por:

$$\Delta_{1,2} = S_{k^*} - S_{k'} = 10 \sum_{j=1}^n w_j (s_{k^*j} - s_{k'j}) > 0$$

Una decisión se considera **estructuralmente blindada y robusta** cuando:

$$\Delta_{1,2}(\mathbf{w} + \Delta \mathbf{w}) > 0 \quad \forall \, \Delta \mathbf{w} \text{ tal que } \|\Delta \mathbf{w}\|_\infty \le 0.20$$

Esto significa que ante cualquier variación de hasta $\pm 20\%$ en los pesos de los pilares (por ejemplo, aumentando drásticamente la prioridad del Coste frente al Ajuste Técnico), el orden jerárquico no sufre inversión (*rank reversal*).

---

## 3. Protocolo de Calibración de Criterios: Must-Haves vs. Wants

El talón de Aquiles de la toma de decisiones en comités es la confusión semántica entre lo que la empresa **necesita obligatoriamente para sobrevivir** (*Must-Haves*) y lo que **desearía tener para optimizar** (*Wants*).

### 3.1. Reglas Canónicas de Clasificación

Para evitar sesgos políticos en la definición de las bases de evaluación, la Oficina de Dirección Estratégica (PMO / FP&A) aplica tres pruebas de fuego:

| Atributo | Filtro Veto (Must-Have) | Criterio Ponderado (Want) |
| :--- | :--- | :--- |
| **Naturaleza de la Métrica** | Binaria estricta (CUMPLE / NO CUMPLE) | Escalar continua (1.0 a 10.0 puntos) |
| **Consecuencia del Incumplimiento** | Descalificación fulminante e irreversible | Penalización gradual en el score final |
| **Capacidad de Trade-Off** | Innegociable; no intercambiable por precio | Negociable; compensable con otros pilares |
| **Ejemplo Típico** | Certificación ISO 27001, Techo de CAPEX | Facilidad de uso (UX), latencia de APIs |

### 3.2. Estructura de los 4 Pilares Estratégicos (13 Criterios)

En el estándar corporativo de Datalaria, los 13 criterios ponderables se distribuyen en 4 pilares equilibrados:

1. **Pilar 1: Ajuste Técnico & Funcional (Ponderación 30.0%)**
   * $C_{1.1}$: Cobertura nativa de requerimientos core sin desarrollo a medida ($w = 0.10$).
   * $C_{1.2}$: Ergonomía de interfaz, UX y curva de adopción de usuarios ($w = 0.08$).
   * $C_{1.3}$: Arquitectura de integración, catálogo de APIs REST y webhooks ($w = 0.07$).
   * $C_{1.4}$: Concurrencia, latencia y rendimiento en tiempo real ($w = 0.05$).

2. **Pilar 2: Coste Total de Propiedad - TCO a 3 Años (Ponderación 25.0%)**
   * $C_{2.1}$: Inversión inicial en licenciamiento y setup Año 1 ($w = 0.10$).
   * $C_{2.2}$: Coste de consultoría, parametrización y migración de datos ($w = 0.09$).
   * $C_{2.3}$: Costes recurrentes de mantenimiento, soporte y upgrades Años 2-3 ($w = 0.06$).

3. **Pilar 3: SLA, Soporte & Solvencia del Proveedor (Ponderación 20.0%)**
   * $C_{3.1}$: SLA contractual de resolución de incidencias críticas < 2h con penalizaciones ($w = 0.08$).
   * $C_{3.2}$: Solvencia financiera, años en el mercado y soporte técnico local ($w = 0.07$).
   * $C_{3.3}$: Calidad de la documentación, repositorio técnico y certificación ($w = 0.05$).

4. **Pilar 4: Escalabilidad, Seguridad & Roadmap (Ponderación 25.0%)**
   * $C_{4.1}$: Modelo de seguridad Zero-Trust, cifrado AES-256 y control de accesos RBAC ($w = 0.10$).
   * $C_{4.2}$: Escalabilidad elástica y resiliencia de infraestructura cloud ($w = 0.08$).
   * $C_{4.3}$: Visión de producto, roadmap tecnológico e integración de IA generativa ($w = 0.07$).

---

## 4. Caso Práctico Empresarial Resuelto: Horizon Global Logistics

Para ilustrar la mecánica del modelo en una decisión corporativa de máxima exposición, analizamos el caso real modelizado de **Horizon Global Logistics**, operador de transporte con 1.400 empleados, 12 delegaciones logísticas y una facturación consolidada de 185 M€.

### 4.1. La Encrucijada Estratégica
La compañía requería sustituir su sistema ERP legacy por una solución Cloud Enterprise de última generación. El Comité de Dirección fijó un techo de inversión inicial (**CAPEX máximo de 450.000 €**) y un plazo improrrogable de puesta en producción de **menos de 6 meses** para no colisionar con la campaña estacional de transporte.

Se presentaron cinco competidores internacionales:
* **Vendor Alpha:** Proveedor global con solución madura y amplia reputación de mercado.
* **Vendor Beta:** Plataforma Cloud Enterprise especializada en logística y finanzas.
* **Vendor Gamma:** Suite modular de bajo coste con fuerte presencia en pymes.
* **Vendor Delta:** Proveedor tradicional de software alojado (*legacy hosted*).
* **Vendor Epsilon:** Plataforma emergente SaaS orientada a nichos.

### 4.2. Matriz de Evaluación y Veredicto DAR

La ejecución rigurosa del modelo arrojó los siguientes resultados cuantitativos:

| Cód | Alternativa Evaluada | Filtros Veto (Must) | P1: Técnico (30%) | P2: TCO 3A (25%) | P3: SLA (20%) | P4: Segur. (25%) | Score Base | Factor $V_k$ | Score Final | Ranking | Dictamen del Comité |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Alt-01** | Vendor Alpha (Global Core) | **APTA** | 23.6 | 19.3 | 16.9 | 18.8 | 78.6 | 1.0 | **78.6** | **2º** | Segunda Opción (Backup) |
| **Alt-02** | **Vendor Beta (Cloud Enterprise)** | **APTA** | **27.6** | **20.0** | **18.4** | **20.4** | **86.4** | **1.0** | **86.4** | **1º** | **ADJUDICATARIA (Recomendada)** |
| **Alt-03** | Vendor Gamma (Suite Modular) | **APTA** | 22.7 | 21.4 | 15.0 | 17.5 | 76.6 | 1.0 | **76.6** | **3º** | Descartada por Brecha SLA |
| **Alt-04** | Vendor Delta (Legacy Hosted) | **DESCALIFICADA** | 24.8 | 16.3 | 16.3 | 18.9 | 76.3 | **0.0** | **0.0** | **-** | **DESCALIFICADA (Criterio V-05)** |
| **Alt-05** | Vendor Epsilon (SaaS Niche) | **APTA** | 21.1 | 20.1 | 13.0 | 17.6 | 71.8 | 1.0 | **71.8** | **4º** | Descartada por Sub-escala |

### 4.3. Análisis de las Decisiones Críticas

1. **La Descalificación Fulminante de Vendor Delta:** A pesar de haber obtenido una sólida nota técnica base de 76.3 puntos y ofrecer un descuento comercial atractivo, la auditoría de compliance descubrió que su telemetría y réplicas secundarias de datos se procesaban en centros de datos ubicados en EE.UU., violando el criterio veto **V-05 (Soberanía y Residencia de Datos en la UE / RGPD)**. El multiplicador booleano actuó sin contemplaciones: $V_{\text{Delta}} = 0 \implies S_{\text{Delta}} = 0.0$. La alternativa quedó excluida del análisis económico.
2. **La Victoria Estructural de Vendor Beta:** Vendor Beta se impuso con **86.4 puntos**, superando a Vendor Alpha por un diferencial concluyente de **+7.8 puntos (+9.9% de ventaja relativa)**. Su liderazgo se fundamenta en su extraordinaria cobertura nativa de procesos logísticos (94%), que ahorra 140 jornadas de desarrollo a medida y elimina el riesgo de retrasos en el calendario.
3. **El Trade-Off Financiero Real del TCO a 3 Años:** Aunque la cuota de suscripción del primer año de Vendor Beta fue 15.000 € superior a la de Vendor Gamma, sus herramientas de migración automatizada y su modelo de soporte premium reducen el coste operativo acumulado a 3 años en **380.000 € frente a Vendor Alpha**, resultando un 19% más económica en términos de flujo de caja neto descontado.

---

## 5. Protocolo de Defensa ante el Consejo (Boardroom Defense FAQ)

Cuando el equipo evaluador comparece ante el CFO, el Comité de Auditoría y los consejeros independientes, surgen invariablemente las cinco preguntas más complejas de la gobernanza corporativa:

### 1. ¿Por qué no adjudicamos el contrato a la alternativa más barata (Vendor Gamma)?
Confundir el precio inicial con el coste total del ciclo de vida es la causa primaria de los fracasos en transformación digital. Vendor Gamma requería 180.000 € en desarrollos externos adicionales para adaptar sus módulos a nuestra operativa y su contrato carecía de penalizaciones financieras por caída de servicio. A 36 meses vista, Vendor Beta representa un ahorro neto de 210.000 € y garantiza contractualmente un uptime del 99.9%.

### 2. ¿Cómo demostramos que las ponderaciones no fueron manipuladas para favorecer a Vendor Beta?
Mediante el **Protocolo de Congelación Previa** auditado por la PMO: la matriz de pesos del 100% se firmó formalmente, se selló con hash criptográfico y se registró ante la Dirección de Cumplimiento antes de proceder a la apertura de las ofertas técnicas y económicas de los licitadores, impidiendo cualquier ajuste retroactivo a conveniencia.

### 3. ¿Por qué descalificar de forma tan categórica a un postor consolidado como Vendor Delta?
El cumplimiento normativo y la ciberseguridad corporativa no son variables de regateo comercial. Incumplir la normativa de soberanía de datos del RGPD expone al grupo a sanciones regulatorias de hasta el 4% de la facturación global anual y a una quiebra reputacional irreparable. Un ahorro marginal en licencias jamás puede justificar un riesgo existencial para los accionistas.

### 4. ¿Qué solidez mantiene la decisión si las condiciones de precios cambian un 20% en 12 meses?
El análisis de sensibilidad matricial *What-If* demostró que incluso en un escenario de estrés extremo en el que el CFO duplicase la ponderación del Coste hasta el 50% del total, Vendor Beta conservaría la primera posición del ranking. Su ventaja competitiva es estructural y reside en la eficiencia operativa, no en un ajuste puntual de tarifas.

### 5. ¿Cómo aseguramos contractualmente la rendición de cuentas tras la firma del contrato?
El modelo DAR vincula el veredicto con el **Board Decision Gateway**: el 30% de la facturación de servicios profesionales queda retenido hasta la superación formal de las pruebas de aceptación de usuario (UAT) y se establecen penalizaciones del 1% semanal sobre la suscripción ante retrasos imputables al proveedor en el hito de Go-Live.

---

## 6. Executive Decision Pack Oficial: Matriz DAR Cuantitativa Dual

Para directores generales (CEO), directores financieros (CFO), directores de tecnología (CIO/CTO) y responsables de compras estratégicas que requieran implementar este modelo con calidad de producción inmediata y grado Consejo de Administración, hemos empaquetado todos los activos programáticos oficiales:

{{< product-card
  title="Matriz DAR Cuantitativa: Criterios Veto & Ponderación Multicriterio"
  category="Toma de Decisiones"
  price="6€"
  original_price="24€"
  badge="⚖️ Decisión Objetiva CMMI"
  icon="⚖️"
  deliverables="Excel .xlsx + Sheets|PowerPoint .pptx 16:9 C-Level|Guía Metodológica PDF"
  features="Algoritmo de scoring ponderado con Criterios Veto (Non-Negotiable)|Comparativa cuantitativa de hasta 5 alternativas o proveedores|Slide PPTX con tabla ejecutiva de trade-offs y recomendación final|Guía metodológica con protocolo de auditoría de decisiones|Descarga directa inmediata (.ZIP con versiones ES y EN)"
  checkout_url="https://datalaria.lemonsqueezy.com/buy/matriz-dar"
  button_text="Descargar Pack Completo (.ZIP) • 6€"
>}}
El archivo comprimido incluye los libros oficiales en **Excel (.xlsx)** con protección estándar ECMA-376 (fórmulas bloqueadas bajo contraseña proporcionada en las instrucciones y celdas de entrada 100% editables), las presentaciones ejecutivas en **PowerPoint (.pptx 16:9 widescreen)** estructuradas bajo la Pirámide de Minto con el gráfico analítico en alta resolución y el Board Decision Gateway, las **Guías Metodológicas en PDF** de 5 páginas con la demostración matemática completa, y las instrucciones de importación fluida a Google Sheets.
{{< /product-card >}}

---

## 7. Referencias Bibliográficas Canónicas de Autoridad

1. **CMMI Institute (2018).** *CMMI for Development (CMMI-DEV, V2.0): Decision Analysis and Resolution (DAR) Process Area*. Information Science Institute / Carnegie Mellon University.  
   *Estándar internacional canónico que formaliza el proceso de evaluación estructurada de alternativas, el establecimiento de criterios veto y la trazabilidad de decisiones críticas en proyectos tecnológicos y organizacionales de gran envergadura.* [Ver estándar oficial en cmmiinstitute.com](https://cmmiinstitute.com)

2. **Kepner, Charles H. & Tregoe, Benjamin B. (1965).** *The Rational Manager: A Systematic Approach to Decision Making and Problem Solving*. McGraw-Hill, New York.  
   *La obra fundacional de la consultoría de decisiones operativas y estratégicas donde se introduce por primera vez la distinción axiomática entre objetivos no negociables (Musts) y deseables ponderables (Wants).* ISBN: `978-0070341753`

3. **Keeney, Ralph L. & Raiffa, Howard (1976).** *Decisions with Multiple Objectives: Preferences and Value Trade-Offs*. John Wiley & Sons, New York.  
   *Tratado seminal de la teoría de la decisión que establece las bases matemáticas de la Teoría de Utilidad Multiatributo (MAUT), la independencia de preferencias y la estructuración cuantitativa de trade-offs corporativos.* ISBN: `978-0521441858`

4. **Raiffa, Howard (1968).** *Decision Analysis: Introductory Lectures on Choices Under Uncertainty*. Addison-Wesley, Reading, MA.  
   *Monografía clásica de Harvard Business School sobre la modelización de árboles de decisión, análisis de sensibilidad marginal bayesiana y neutralización de la aversión al riesgo en la alta dirección.* ISBN: `978-0075548546`

5. **Minto, Barbara (2009).** *The Pyramid Principle: Logic in Writing and Thinking*. Financial Times / Prentice Hall (3ª Edición).  
   *El estándar universal de estructuración lógica de diapositivas ejecutivas, síntesis deductiva y Action Titles adoptado por McKinsey, BCG y Bain para la comunicación directiva ante Consejos de Administración.* ISBN: `978-0273710516`
