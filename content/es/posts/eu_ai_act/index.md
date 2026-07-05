---
title: "EU AI Act: Lo que Todo Ingeniero Español Necesita Saber (Sin Abogados)"
date: 2026-07-05
draft: false
categories: ["Inteligencia Artificial", "Ingeniería", "Regulación"]
tags: ["eu ai act", "regulación ia", "aesia", "compliance", "alto riesgo", "startups", "ingeniería", "europa"]
description: "Guía técnica del Reglamento Europeo de Inteligencia Artificial (EU AI Act) escrita por y para ingenieros. Clasificación de riesgo, obligaciones técnicas, multas, checklist de compliance y conexión con la Ley española de IA y la AESIA."
summary: "El 2 de agosto de 2026 entra en vigor la mayoría de las obligaciones del EU AI Act. La multa máxima: 35 millones de euros o el 7% de tu facturación global. Y la mayoría de artículos que explican esta regulación están escritos por abogados, para abogados. Este no. Este está escrito por un ingeniero que ya opera agentes de IA en producción, y traduce cada artículo del reglamento al lenguaje que de verdad entendemos: arquitecturas, pipelines y código."
social_text: "El 2 de agosto de 2026 entra en vigor el EU AI Act. Multa máxima: €35M. La mayoría de guías están escritas por abogados. Esta no. La he escrito como ingeniero que ya opera agentes IA en producción 🇪🇺🤖⚖️ #EUAIAct #IA #Regulación #Ingeniería"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

Imagina este escenario: tu startup española lanza una herramienta de IA que analiza currículums para filtrar candidatos en procesos de selección. El producto funciona, los clientes están contentos, la facturación crece. Tres meses después, recibes una notificación formal de la **AESIA** (Agencia Española de Supervisión de Inteligencia Artificial). Tu sistema ha sido clasificado como **"alto riesgo"** bajo el Reglamento (UE) 2024/1689, más conocido como el **EU AI Act**. No tienes documentación técnica obligatoria, no has implementado supervisión humana, y tus datos de entrenamiento no cumplen los requisitos de gobernanza. Multa potencial: hasta **35 millones de euros** o el **7% de tu facturación mundial anual**.

¿Imposible? No. Es exactamente lo que la regulación europea vigente estipula desde febrero de 2025 para las prácticas prohibidas, y lo que a partir del **2 de agosto de 2026** se extiende a la mayoría de las obligaciones para sistemas de alto riesgo ([Art. 113, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689)).

Si ya operas agentes de IA en producción —como hemos hecho en este blog con el [Proyecto Autopilot](/es/posts/ia_agents_part1/) o el [radar agéntico de obsolescencia](/es/posts/obs_parte5_radar/)— necesitas saber exactamente dónde está la línea. Y la mayoría de guías sobre el EU AI Act están escritas por abogados, para abogados. Esta no. Esta está escrita por un ingeniero que traduce cada artículo del reglamento al lenguaje que de verdad entendemos: arquitecturas, pipelines y código.

### La Pirámide del Riesgo: Clasifica tu IA en 60 Segundos

El EU AI Act no prohíbe la inteligencia artificial. Lo que hace es clasificar cada sistema de IA en **cuatro niveles de riesgo**, y asignar obligaciones proporcionales a cada nivel. Es un enfoque pragmático que se inspira en marcos regulatorios existentes como REACH para la industria química o la Directiva de Máquinas para la industria manufacturera: a mayor riesgo potencial, mayor exigencia de control.

![Pirámide de clasificación de riesgo del EU AI Act](piramide_riesgo.png)

#### 🔴 Riesgo Inaceptable — PROHIBIDO (Artículo 5)

Estas prácticas están **completamente vetadas en la UE desde el 2 de febrero de 2025** ([Art. 5, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689#d1e2816-1-1)). No hay excepciones comerciales ni sandboxes que las permitan. Son las líneas rojas absolutas de la regulación:

* **Manipulación subliminal o engañosa**: Sistemas de IA diseñados para distorsionar el comportamiento de una persona usando técnicas que operan por debajo de su umbral de consciencia, causando un perjuicio significativo.
* **Explotación de vulnerabilidades**: IA que explota la edad, la discapacidad o la situación socioeconómica de personas vulnerables para alterar su comportamiento de forma perjudicial.
* **Puntuación social (*social scoring*)**: Sistemas utilizados por autoridades públicas para evaluar o clasificar a personas en función de su comportamiento social o sus rasgos personales, resultando en un trato desfavorable injustificado.
* **Policiamiento predictivo**: IA que predice el comportamiento delictivo de una persona basándose exclusivamente en su perfilado o rasgos de personalidad (con excepciones limitadas para investigaciones en curso).
* **Scraping facial masivo**: La creación o expansión de bases de datos de reconocimiento facial mediante la recopilación no dirigida de imágenes faciales de Internet o de cámaras de vigilancia.
* **Reconocimiento emocional en el trabajo y la educación**: Inferir emociones de empleados en el lugar de trabajo o de estudiantes en centros educativos (con excepciones médicas o de seguridad muy limitadas).
* **Categorización biométrica sensible**: Sistemas que infieren datos como creencias políticas o religiosas, orientación sexual o raza a partir de datos biométricos.

Si un sistema de IA de tu organización roza cualquiera de estas categorías, la posición correcta no es «buscar un hueco legal», sino eliminarlo del producto. La multa para estas prácticas alcanza los **35 millones de euros** o el **7% de la facturación anual global**, lo que sea mayor ([Art. 99.3, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689#d1e9487-1-1)).

#### 🟠 Alto Riesgo — REGULACIÓN ESTRICTA (Artículos 6-49 y Anexo III)

Aquí es donde la mayoría de los sistemas empresariales de IA caen, y donde la regulación exige el mayor esfuerzo técnico. Un sistema se clasifica como «alto riesgo» si es un componente de seguridad de un producto regulado por la legislación armonizada de la UE (dispositivos médicos, juguetes, aviación), o si opera en alguna de las áreas sensibles definidas en el **Anexo III** del reglamento:

* **Infraestructura crítica**: Sistemas para la gestión de servicios esenciales (transporte, agua, gas, electricidad, telecomunicaciones).
* **Educación y formación**: IA que determina el acceso a instituciones educativas o que evalúa el rendimiento de estudiantes.
* **Empleo y RRHH**: Herramientas de IA para reclutamiento, filtrado de CVs, asignación de tareas o gestión de trabajadores. Esto es directamente relevante para lo que analizamos en el [artículo sobre Onboarding con IA](/es/posts/onboarding/): usar IDP y GenAI para automatizar la incorporación de empleados cae en la categoría de alto riesgo si el sistema toma o influye en decisiones sobre personas.
* **Servicios esenciales**: Sistemas que determinan el acceso a crédito, servicios públicos esenciales o seguros de vida y salud. Startups como [Clarity AI](/es/posts/clarity_ai/), que calcula scores de sostenibilidad para decisiones de inversión, operan directamente en esta zona.
* **Orden público, justicia y migración**: IA en control fronterizo, asilo, evaluación de riesgos de seguridad o administración de justicia.
* **Biometría**: Ciertos sistemas de identificación biométrica a distancia.

La multa por incumplimiento en sistemas de alto riesgo es de hasta **15 millones de euros** o el **3% de la facturación mundial anual** ([Art. 99.4, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689#d1e9487-1-1)).

> **Nota importante**: La propuesta legislativa conocida como *"Digital Omnibus"* (2025) podría aplazar algunas obligaciones del Anexo III (alto riesgo) de agosto de 2026 a **diciembre de 2027**. Sin embargo, los requisitos técnicos subyacentes no cambian, solo el calendario de enforcement. No esperes.

#### 🟡 Riesgo Limitado — TRANSPARENCIA (Artículos 50-52)

Los sistemas de riesgo limitado tienen una única obligación fundamental: **informar al usuario de que está interactuando con una IA**. Esto aplica a chatbots, sistemas de generación de contenido (deepfakes), y asistentes conversacionales. Nuestro [Ops Engineering Copilot](/es/posts/ia_agents_part8/) (el chatbot basado en Algolia Agent Studio y RAG que responde preguntas sobre el blog) caería en esta categoría: el usuario debe saber que habla con una máquina, no con una persona.

#### 🟢 Riesgo Mínimo — LIBRE (sin obligaciones adicionales)

La mayoría de los sistemas de IA comerciales caen aquí: filtros de spam, sistemas de recomendación, IA generativa para contenido de marketing. El [Proyecto Autopilot](/es/posts/ia_agents_part1/) que genera automáticamente posts para redes sociales no tiene obligaciones específicas bajo el EU AI Act más allá de las buenas prácticas generales. Lo mismo aplica a herramientas como el [conversor de unidades](/es/posts/app_conversor_unidades/) o la [app de flashcards](/es/posts/app_flashcards/).

### Los 5 Mandamientos Técnicos del Alto Riesgo

Si tu sistema cae en la categoría 🟠, necesitas implementar cinco bloques de requisitos técnicos. Lo notable es que, si ya sigues las prácticas de ingeniería que hemos documentado en este blog, estás más cerca del cumplimiento de lo que crees. Veamos:

**1. Gestión de Riesgos — Artículo 9**

El reglamento exige establecer, implementar y mantener un **sistema de gestión de riesgos que opere durante todo el ciclo de vida del sistema de IA** ([Art. 9, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689#d1e3383-1-1)). Esto incluye la identificación de riesgos conocidos y previsibles para la salud, la seguridad y los derechos fundamentales, la estimación de esos riesgos, y la adopción de medidas de mitigación.

*Traducción para ingenieros*: Es un pipeline de CI/CD aplicado al riesgo. Documenta, monitorea, itera. No es un documento estático que se escribe una vez y se archiva; es un proceso vivo. Exactamente la filosofía que [W. Edwards Deming](/es/posts/deming/) sistematizó con el ciclo PDCA (Plan-Do-Check-Act). Si ya implementas PDCA en tus procesos de calidad, la gestión de riesgos del AI Act te será familiar. Si además conoces el *Concept Drift* (la degradación progresiva de un modelo en producción que Deming habría llamado «proceso inestable»), ya tienes la mentalidad correcta.

**2. Gobernanza de Datos — Artículo 10**

Los datos de entrenamiento, validación y test deben cumplir criterios de alta calidad: ser **representativos, relevantes, libres de errores en la medida de lo posible, y con prácticas de gobernanza apropiadas** para prevenir sesgos ([Art. 10, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689#d1e3549-1-1)).

*Traducción*: La [higiene de datos](/es/posts/sop_ingenieria-higiene-datos/) que predicamos en la serie S&OP ya no es una buena práctica opcional; **es ley**. El pipeline de limpieza con Z-Score para detectar outliers, el marcado (no borrado) de anomalías, y la persistencia en Supabase con Row Level Security que construimos en esa serie cumplen directamente con el espíritu de este artículo. Lo que el reglamento añade es la exigencia de que todo esto esté documentado y sea auditable.

**3. Documentación Técnica — Artículo 11 y Anexo IV**

Antes de comercializar o poner en servicio un sistema de alto riesgo, debes preparar un **expediente técnico** que demuestre el cumplimiento del reglamento ([Art. 11, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689#d1e3667-1-1)). El Anexo IV detalla el contenido mínimo: descripción general del sistema, arquitectura detallada y componentes, información sobre los datos de entrenamiento, métricas de rendimiento (exactitud, robustez, ciberseguridad), y el proceso de desarrollo.

*Traducción*: Tu README y tu Confluence no bastan. El reglamento exige un documento vivo que cubra la arquitectura del sistema (como los diagramas Mermaid que usamos en la serie de [Obsolescencia](/es/posts/obs_parte3_arquitectura/)), las métricas de rendimiento del modelo, las pruebas de robustez y las medidas de ciberseguridad. Piensa en ello como un documento de arquitectura de referencia (*Architecture Decision Record*) con esteroides regulatorios.

**4. Registros y Logging — Artículo 12**

Los sistemas de alto riesgo deben diseñarse para **generar logs automáticos** durante su funcionamiento, garantizando la trazabilidad de cada decisión y la capacidad de reconstruir eventos si surge un problema de cumplimiento ([Art. 12, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689#d1e3702-1-1)).

*Traducción*: Si ya usas Supabase + FastAPI con la arquitectura del [radar agéntico](/es/posts/obs_parte6_fastapi/), esto debería sonar familiar. Cada evento de ingesta, cada decisión del agente CrewAI, cada respuesta del LLM queda registrado en la base de datos. Lo que el reglamento formaliza es lo que cualquier ingeniero de backend competente ya debería estar haciendo: logging estructurado, no como una idea tardía, sino como un requisito de diseño desde el día cero.

**5. Supervisión Humana — Artículo 14**

El sistema debe diseñarse con mecanismos de **«human-in-the-loop»** o **«human-on-the-loop»**, garantizando que un operador humano cualificado pueda supervisar, interpretar y, si es necesario, anular las decisiones de la IA ([Art. 14, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689#d1e3789-1-1)).

*Traducción*: Este es el principio que implementamos en el [Autopilot Parte 5](/es/posts/ia_agents_part5/) con los **GitHub Environments de aprobación manual**. El pipeline genera contenido automáticamente con agentes de IA, pero ningún post se publica sin la revisión y aprobación explícita de un humano. No es un concepto nuevo para nosotros; ahora tiene fuerza de ley.

### España y la AESIA: El Sheriff Local

El EU AI Act es un **Reglamento europeo** (no una Directiva), lo que significa que es directamente aplicable en España sin necesidad de transposición legislativa nacional. Sin embargo, España ha dado un paso adicional: en mayo de 2026, el Consejo de Ministros aprobó la **Ley española de Inteligencia Artificial**, que complementa el reglamento europeo y define el rol de la **AESIA (Agencia Española de Supervisión de Inteligencia Artificial)** como autoridad nacional competente.

La AESIA es la entidad que investigará denuncias, realizará auditorías y, en su caso, impondrá las sanciones del AI Act en territorio español. Además, España ha puesto en marcha **sandboxes regulatorios**: entornos controlados donde startups y empresas pueden testear sistemas de IA innovadores bajo la supervisión de la AESIA, sin riesgo sancionador durante el periodo de prueba. Es un mecanismo inspirado en los que ya utilizan la CNMV y el Banco de España para fintech.

Las startups españolas que hemos analizado en este blog no son ajenas a esta regulación. [Clarity AI](/es/posts/clarity_ai/) opera en el scoring financiero ESG, un área que el Anexo III clasifica como alto riesgo. [Nextail](/es/posts/nextail/) toma decisiones de inventario con IA prescriptiva en la cadena de suministro, y ya tuvo que adaptarse al [ESPR 2026](/es/posts/nextail/). [Devo](/es/posts/devo/) protege infraestructura crítica militar, la categoría más sensible del reglamento. Todas ellas deberán demostrar cumplimiento.

### Compliance-as-Code: El Checklist del Ingeniero

Si algo hemos aprendido construyendo pipelines de datos en este blog, es que la documentación que no está automatizada no se mantiene. Aquí va un checklist accionable, diseñado para que un equipo técnico pueda ejecutarlo sprint a sprint:

**Fase 1 — Inventario y Clasificación** *(Sprint 1)*
* Inventariar todos los sistemas de IA de tu organización (incluidos los que no llamas «IA» pero usan ML internamente)
* Clasificar cada sistema en la pirámide de riesgo: Prohibido / Alto / Limitado / Mínimo
* Para cada sistema clasificado como Alto Riesgo, asignar un responsable técnico de cumplimiento

**Fase 2 — Implementación Técnica** *(Sprints 2-4)*
* Implementar logging automático de decisiones del modelo (Art. 12): timestamps, inputs, outputs, scores de confianza
* Crear documentación técnica viva (Art. 11 + Anexo IV): arquitectura, datos, métricas, proceso
* Diseñar mecanismo de supervisión humana (Art. 14): aprobación manual, botón de «kill switch», dashboards de monitoreo
* Auditar datasets de entrenamiento (Art. 10): sesgo, representatividad, trazabilidad, versionado

**Fase 3 — Gestión Continua** *(Ongoing)*
* Establecer pipeline de gestión de riesgos (Art. 9): revisión periódica, monitoreo de Concept Drift, plan de mitigación
* Para sistemas de Riesgo Limitado: verificar que el usuario sabe que interactúa con IA
* Configurar alertas de coste y uso (conectar con la [Economía Oculta de la IA](/es/posts/economia_oculta_ia/): el compliance es un coste oculto adicional)
* Registrar el sistema en la base de datos pública de la UE (cuando aplique para alto riesgo)

### El Reglamento No Es el Enemigo; la Ignorancia Sí

Existe una tentación comprensible de ver el EU AI Act como un freno burocrático a la innovación europea. Y en parte, la crítica tiene fundamento: la definición de «alto riesgo» en el Anexo III es extremadamente amplia, la carga documental del Anexo IV puede resultar desproporcionada para una startup de cinco personas, y la incertidumbre sobre el *Digital Omnibus* genera parálisis en los equipos legales.

Pero si retiras la capa de jerga legal y miras los requisitos técnicos desnudos, lo que el reglamento realmente pide es: **documenta tu sistema, controla tus datos, registra las decisiones de tu IA, gestiona los riesgos de forma continua, y mantén a un humano en el bucle de control**. Es decir, exactamente lo que un buen ingeniero ya debería estar haciendo.

Si has seguido las prácticas que documentamos en este blog —[higiene de datos con Z-Score](/es/posts/sop_ingenieria-higiene-datos/), [logging automático con FastAPI y Supabase](/es/posts/obs_parte6_fastapi/), [human-in-the-loop con GitHub Environments](/es/posts/ia_agents_part5/), [gestión de riesgos con el ciclo PDCA de Deming](/es/posts/deming/)—, **ya estás al 80% del camino hacia el cumplimiento**. El 20% restante es formalización y documentación.

Como decía Deming: *"No basta con hacer lo mejor que puedas; primero debes saber qué hacer"*. Ahora la regulación te dice qué hacer. El cómo hacerlo, ya lo sabes. O al menos, ya tienes un blog donde encontrarlo.

---

#### Fuentes de Interés:
* [**Reglamento (UE) 2024/1689**: Texto completo del EU AI Act en EUR-Lex (ES)](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689)
* [**Comisión Europea**: Página oficial del EU AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
* [**EU AI Act Explorer**: Guía navegable por artículos del reglamento](https://artificialintelligenceact.eu/)
* [**digital.gob.es**: Información sobre la AESIA y la regulación de IA en España](https://portal.mineco.gob.es/es-es/digitalizacion/Paginas/ia.aspx)
* [**Datalaria**: La Economía Oculta de la IA — Costes Reales en Producción](/es/posts/economia_oculta_ia/)
* [**Datalaria**: W. Edwards Deming — El Padre de la Calidad Total que Predijo el Futuro de la IA](/es/posts/deming/)
* [**Datalaria**: S&OP Higiene de Datos — Por qué tu Excel te miente](/es/posts/sop_ingenieria-higiene-datos/)
* [**Datalaria**: Autopilot Part 5 — De Localhost a la Nube con GitHub Actions y CI/CD](/es/posts/ia_agents_part5/)
