---
title: "Devo: Cómo un Químico Autodidacta Construyó desde Madrid el Motor de Datos que Defiende a la Fuerza Aérea de EE.UU."
date: 2026-06-07
draft: false
categories: ["casos_exito", "IA"]
tags: ["devo", "ciberseguridad", "pedro castillo", "siem", "big data", "cloud-native", "startup", "unicornio", "streaming analytics"]
description: "La historia de Devo, la startup española fundada por Pedro Castillo que revolucionó el análisis de datos de seguridad con latencia cero, conquistó un contrato con la Fuerza Aérea de EE.UU. y alcanzó una valoración de 1.900 millones de dólares."
summary: "Cuando un ataque de phishing paralizó uno de los bancos más innovadores de España, un químico reconvertido en ingeniero de seguridad identificó el fallo que la industria entera ignoraba. Esta es la historia de Devo: de las trincheras de la ciberseguridad bancaria en Madrid al motor de datos que defiende las redes militares más críticas del planeta."
social_text: "Un químico autodidacta de Madrid construyó el motor de datos que defiende la Fuerza Aérea de EE.UU. La historia de Devo: de startup a unicornio de $1.900M revolucionando la ciberseguridad con latencia cero 🛡️🚀📊 #Devo #Ciberseguridad #Startup #Unicornio"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

En el campo de batalla del ciberespacio, donde un atacante patrocinado por un estado puede comprometer credenciales y moverse lateralmente a través de una red militar en apenas **18 minutos y 49 segundos**, cada segundo de retraso en la detección puede significar la diferencia entre defender una infraestructura crítica o perderla. Sin embargo, durante años, la industria de la ciberseguridad aceptó como normal que sus herramientas de análisis tardaran hasta 15 minutos en procesar un simple registro de seguridad.

Esta es la historia de **Devo**, la crónica de cómo un químico madrileño autodidacta identificó esa brecha absurda en las trincheras de un banco español, fundó una startup que los inversores intentaron arrebatarle, y terminó construyendo el motor de datos en tiempo real que hoy protege las redes de la **Fuerza Aérea de los Estados Unidos**. Un viaje desde la asfixia operativa del sector financiero hasta el estatus de *unicornio* valorado en **1.900 millones de dólares**.

![Imagen conceptual de Devo](devo_imagen_conceptual.png)

### El Origen: Un Ataque de Phishing y una Obsesión por la Velocidad

La semilla de Devo no germinó en un garaje de Silicon Valley, sino en la sala de crisis de **Bankinter** en 2003. **Pedro Castillo** no responde al arquetipo del emprendedor tecnológico convencional. Licenciado en Ciencias Químicas por la Universidad Complutense de Madrid, descubrió su verdadera vocación de forma fortuita al encontrar un ordenador Silicon Graphics en su facultad, lo que despertó una fascinación que le llevó a aprender a programar de manera completamente autodidacta.

A mediados de los años noventa, cuando Internet era aún territorio exclusivo de universidades y organismos gubernamentales, Castillo ya prestaba servicios informáticos avanzados a corporaciones como **El Corte Inglés**. Esa experiencia temprana culminó con la fundación de **Webline** en 1996, su primera empresa de ciberseguridad, que le abrió las puertas del sector financiero español. Bankinter, una de las entidades más innovadoras del país, lo reclutó hasta convertirlo en Director de Seguridad Tecnológica.

Fue precisamente en esas trincheras bancarias donde todo cambió. En 2003, un sofisticado ataque de *phishing* golpeó a Bankinter. Castillo y su equipo se encontraron con un obstáculo paralizante: las herramientas de la época eran **incapaces de ingerir y correlacionar los volúmenes masivos de datos** generados por servidores, cortafuegos y tráfico de red a la velocidad necesaria para detener el ataque antes de que se consumara el fraude. Las soluciones existentes imponían una elección imposible: pagar costes exorbitantes para almacenarlo todo, o filtrar los datos y crear «puntos ciegos» que los atacantes explotarían inevitablemente.

Obsesionado con liberar el valor del dato en bruto, Castillo abandonó su cómoda posición ejecutiva y fundó **Logtrust** en Madrid en 2011. Su filosofía fue radical: mientras otras *startups* corrían a las conferencias y a la prensa, él y su equipo se atrincheraron en el desarrollo de software, construyendo un motor de base de datos desde cero. Un producto, en sus propias palabras, *«absolutamente diferencial»*.

{{< youtube bq-9Zf0aQm8 >}}

### La Revolución Tecnológica: HyperStream y la Latencia Cero

¿Por qué Devo logró desbancar a gigantes como Splunk en múltiples licitaciones? La respuesta reside en una reingeniería radical del procesamiento de datos de seguridad.

El estándar de la industria, dominado por Splunk, dependía de la **indexación durante la ingesta** (*index-on-ingest*): los datos debían ser analizados, normalizados y estructurados en un índice masivo *antes* de almacenarse. Este diseño creaba tres debilidades críticas:

1. **Retraso letal**: En entornos de alto volumen, los eventos tardaban más de 15 minutos en estar disponibles para el analista.
2. **Contención de recursos**: La lectura y escritura del índice compartían CPU, degradando el rendimiento justo cuando más urgía la velocidad.
3. **Costes prohibitivos**: Mantener índices de petabytes obligaba a los directivos a crear «puntos ciegos», dejando de monitorizar hasta un tercio de sus sistemas.

Devo descartó por completo la indexación tradicional y construyó **HyperStream**, una tecnología propietaria de análisis en *streaming* basada en principios opuestos:

* **Ingesta sin normalización**: Los datos se almacenan en su formato original. La plataforma aplica el esquema en el momento de la consulta (*schema-on-read*), no al guardar el dato.
* **Micro-índices inmutables**: En lugar de un índice global, HyperStream crea un micro-índice diario por fuente de datos que, una vez generado, nunca se reescribe. Resultado: **compresión 10:1** y paralelización masiva.
* **Latencia cero**: La telemetría está disponible para alertas y búsquedas en el milisegundo exacto en que toca el disco.

La convergencia de estas innovaciones permitió un logro sin precedentes: mantener **400 días de datos «siempre calientes»**, consultables en sub-segundos. Mientras los competidores archivaban los datos antiguos en almacenamiento frío e inconsultable, un analista forense con Devo podía investigar una intrusión de hace un año con la misma velocidad que si hubiera ocurrido hace cinco minutos.

### La Prueba de Fuego: Defender las Redes de la Fuerza Aérea de EE.UU.

La validación definitiva de HyperStream llegó en julio de 2020, cuando Devo se adjudicó un contrato de **9,5 millones de dólares con la Fuerza Aérea de los Estados Unidos** para desplegar su tecnología como SIEM central del programa de Ciberdefensa Empresarial.

La situación era crítica: los escuadrones cibernéticos operaban con un SIEM de 1999 que aglomeraba hasta **70 aplicaciones inconexas**, generando más de **8 millones de alertas diarias** sin capacidad de correlación automatizada. La iniciativa militar «12N12» exigía consolidar ese caos en 12 herramientas funcionales en 12 meses.

Los resultados del despliegue de Devo fueron transformadores:

* Un **panel de control unificado** que eliminó la fragmentación operativa.
* Más de **20.000 horas humanas** ahorradas en triaje manual de amenazas.
* Reorientación de los analistas cibernéticos de tareas repetitivas hacia la **caza proactiva de amenazas** contra actores estatales.

### El Crisol del Capital Riesgo: De la Batalla en la Junta al Estatus de Unicornio

El camino financiero de Devo fue tan intenso como su ingeniería. A principios de 2017, la primera ronda de 11 millones de dólares trajo consigo lo que Castillo describió como una *«situación terrible»*: los inversores intentaron forzar su destitución como CEO para imponer un perfil corporativo externo. La intervención de **Insight Partners**, que lideró una Serie B de 35 millones de dólares, estabilizó la gobernanza y respaldó la visión técnica del fundador.

En 2018, coincidiendo con la Serie C, Logtrust se rebautizó como **Devo** (contracción de *«Data Evolution»*) y trasladó su sede a Boston, manteniendo la ingeniería en Madrid. El hipercrecimiento que siguió fue explosivo: **80% de crecimiento interanual** en ingresos y **136% en clientes** hacia 2021.

| Ronda | Fecha | Capital | Inversores Principales | Hito |
| :--- | :--- | :--- | :--- | :--- |
| **Venture Round** | Ene 2017 | $11M | Kibo Ventures, Atlantic Bridge | Expansión inicial |
| **Serie B** | Sep 2017 | $35M | Insight Partners | Estabilización del liderazgo |
| **Serie C** | Jun 2018 | $25M | Insight Partners, Kibo Ventures | Rebranding a Devo; sede a Boston |
| **Serie D** | Sep 2020 | $60M | Georgian, Bessemer Venture | Marc van Zadelhoff, nuevo CEO |
| **Serie E** | Oct 2021 | $250M | TCV, General Atlantic, Eurazeo | **Unicornio: $1.500M** |
| **Serie F** | Jun 2022 | $100M | TCV, Insight, Bessemer | **Valoración: $1.900M** |

{{< youtube qNvsiA-JQ5s >}}

### El Futuro: IA Agentística y Strike48

Pero la ingesta masiva no es suficiente si la organización no puede responder a los hallazgos con igual celeridad. El Centro de Operaciones de Seguridad (SOC) contemporáneo padece un mal sistémico: la **fatiga de alertas**. Un SOC corporativo promedio recibe más de **4.400 alertas diarias** procedentes de más de 28 herramientas de seguridad diferentes, y el **53% de esas alertas son falsos positivos** que consumen un tiempo irrecuperable. Con una escasez global estimada en **4,8 millones de profesionales** de ciberseguridad, la automatización dejó de ser un lujo para convertirse en una necesidad existencial.

En 2026, Devo dio el salto hacia la **Inteligencia Artificial Agentística** con el lanzamiento de **Strike48**. En lugar de *copilotos* que asisten pasivamente al analista, Strike48 despliega un escuadrón de **micro-agentes autónomos** que ejecutan investigaciones complejas: correlacionan alertas, identifican al *«paciente cero»*, recopilan evidencia forense y construyen árboles de evidencia visuales, deteniéndose únicamente para la aprobación humana de acciones irreversibles.

La arquitectura resuelve además un problema devastador: las empresas monitorizan apenas un **66% de sus sistemas** por restricciones presupuestarias de los SIEM legados. Los conectores de Strike48 interrogan los datos directamente donde residen —buckets de AWS, lagos de datos, instalaciones de Splunk— sin duplicar almacenamiento, otorgando a los agentes de IA la **visión omnisciente** necesaria para detectar lo que antes quedaba en la sombra. En las implementaciones de prueba tempranas, este modelo redujo el Tiempo Medio de Detección (MTTD) a menos de **ocho minutos**, descubriendo campañas sigilosas que las herramientas legadas habían pasado completamente por alto.

Como nota final de esta trayectoria: habiendo consolidado a Devo como un titán indiscutible, Pedro Castillo demostró su condición de emprendedor en serie fundando **Onum** en 2023, una plataforma para reducir el ruido de los *pipelines* de datos en un 80%. La validación fue fulminante: en agosto de 2025, fue adquirida por **CrowdStrike**.

### Conclusión: Ingeniería Contra Dogma

La historia de Devo es la demostración de que los cambios transformacionales no nacen de estrategias comerciales audaces, sino de la terquedad ingenieril de cuestionar los dogmas aceptados. Mientras la industria entera construía índices cada vez más grandes, un químico autodidacta de Madrid se preguntó: *«¿Y si el índice es el problema?»*.

Esa pregunta, respondida con una década de ingeniería obsesiva y con la resiliencia de sobrevivir a las maniobras del capital riesgo, generó un motor capaz de proteger desde un banco español hasta el ciberespacio militar más exigente del planeta. El trayecto de Pedro Castillo —desde un laboratorio de química en la Complutense hasta los centros de innovación de Massachusetts, pasando por las trincheras bancarias de Madrid— es un recordatorio potente de que, en la era del Big Data, las batallas no se ganan con más munición, sino con armas más rápidas. Y en ese terreno, la velocidad de máquina que Devo ha logrado dominar es, quizás, la única defensa fiable contra las amenazas que operan a esa misma velocidad.

---

#### Fuentes de Interés:
* [**Devo**: Sitio Oficial — Plataforma de Datos de Seguridad](https://www.devo.com/)
* [**The Objective**: Pedro Castillo, fundador de un 'unicornio' de 1.300 millones: «Yo siempre he sido autodidacta»](https://theobjective.com/podcasts/asi-empece/pedro-castillo-devo/)
* [**YouTube**: Pedro Castillo — Mis aventuras y desventuras con los inversionistas de Silicon Valley](https://www.youtube.com/watch?v=bq-9Zf0aQm8)
* [**YouTube**: How Devo built Strike48 to kill the SOC alert](https://www.youtube.com/watch?v=qNvsiA-JQ5s)
* [**GlobeNewsWire**: Devo se adjudica contrato de $9,5M con la Fuerza Aérea de EE.UU.](https://www.globenewswire.com/news-release/2020/07/14/2061860/0/en/Devo-Awarded-9-5M-U-S-Air-Force-Contract-for-Next-Generation-SIEM-Technology.html)
* [**Emprendedores**: Logtrust, la tecnología española que ha captado 71 millones de dólares](https://emprendedores.es/ideas-de-negocio/mejores-startups-empresas-exito-emprendedores-logtrust/)
* [**Strike48**: Plataforma de Inteligencia Agentística de Registros](https://www.strike48.com/)
* [**CRN**: CrowdStrike To Acquire Onum For Next-Gen SIEM Expansion](https://www.crn.com/news/security/2025/crowdstrike-to-acquire-onum-for-next-gen-siem-expansion)
* [**Insight Partners**: How Devo built agentic Strike48](https://www.insightpartners.com/ideas/devo-leadership-story/)
