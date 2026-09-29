---
title: "Submer: La Refrigeración Líquida Nacida en Barcelona que Permite Enfriar los Superordenadores de la AGI"
date: 2026-11-01
draft: false
categories: ["casos_exito", "Ingeniería", "Inteligencia Artificial"]
tags: ["submer", "immersion cooling", "data centers", "supercomputacion", "hardware", "esg", "startups", "sostenibilidad", "agi"]
image: cover.jpg
weight: 10
authorAvatar: datalaria-logo.png
social_text: "¿Cómo una startup de Barcelona se convirtió en la pieza física invisible para enfriar los superordenadores de la AGI? La historia de Submer y la refrigeración líquida por inmersión 🧊🖥️⚡ #Submer #DataCenters #ImmersionCooling #Hardware #AI"
description: "Cómo dos emprendedores en Barcelona revolucionaron la infraestructura física de la computación. Analizamos la tecnología de inmersión líquida de Submer, sus alianzas con Intel y Nvidia, y por qué enfriar servidores con fluidos dieléctricos es el cuello de botella que decide el futuro de la AGI."
summary: "Entrenar y ejecutar modelos frontera de IA genera una densidad térmica que pulveriza los límites de la refrigeración por aire tradicional. Submer, fundada en Barcelona por Daniel Pope y Pol Valls, sumerge servidores en fluidos dieléctricos biodegradables logrando un PUE récord de 1.03. Analizamos su tecnología, rondas de inversión y por qué son la pieza invisible indispensable en la carrera hacia la AGI."
---

Cuando en 2026 la industria tecnológica debate sobre el horizonte de la **Inteligencia Artificial General (AGI)**, la conversación suele gravitar en torno a abstracciones matemáticas: billones de parámetros, funciones de recompensa de razonamiento, modelos como **Gemini 3.8 / 4 Pro**, **Claude Mythos** o **GPT Astra**, y complejos agentes autónomos.

Sin embargo, en el interior de los centros de datos masivos donde esos modelos cobran vida, la realidad es brutalmente física, ruidosa y termodinámica: **vatios, silicio y calor extremo**.

Un solo rack de servidores diseñado para entrenamiento de IA de última generación (con aceleradores de alta densidad gráfica) consume hoy entre **80 y 120 kilovatios (kW)** de potencia eléctrica. Para ponerlo en perspectiva: ese único armario metálico genera la misma energía térmica que cuarenta hornos industriales funcionando a máxima potencia en el espacio de un metro cuadrado.

Intentar enfriar esa monstruosidad empujando corrientes de aire frío con ventiladores tradicionales es, desde el punto de vista de las leyes de la física, como intentar apagar un volcán con un abanico.

Históricamente, **hasta el 40% de toda la factura eléctrica de un centro de datos no se consumía en computar datos, sino en hacer funcionar compresores de aire acondicionado y turbinas gigantescas para evitar que los procesadores se fundieran**.

En 2015, dos ingenieros en Barcelona anticiparon que este modelo colapsaría con la llegada de la supercomputación y decidieron formular una pregunta que sonaba a locura: **¿Y si sumergimos los servidores enteros directamente en líquido?**

Así nació **Submer**.

Tras haber explorado en Datalaria las trayectorias de [Wallapop](/es/posts/wallapop/), [HappyRobot](/es/posts/happyrobot/), [Devo](/es/posts/devo/), [Carto](/es/posts/carto/) y la analítica climática de [Clarity AI](/es/posts/clarity_ai/), este artículo disecciona la ingeniería de Submer: la startup nacida en Cataluña que ha revolucionado la refrigeración por inmersión líquida (*Immersion Cooling*) y se ha convertido en el aliado silencioso de gigantes como **Intel, Nvidia, Dell y Supermicro** para hacer físicamente viable la infraestructura de la AGI.

{{< youtube Fj-yRj84Z7U >}}

### El Origen: Del Ruido Ensordecedor a un Taller en L'Hospitalet

La historia de Submer arranca de la frustración operativa real. **Daniel Pope**, un emprendedor hispano-británico con amplia experiencia en arquitectura de centros de datos y redes de telecomunicaciones, llevaba años gestionando instalaciones tradicionales. Vivía a diario la pesadilla de la refrigeración por aire: salas con un ruido acústico superior a los 90 decibelios, consumos millonarios de agua potable en torres de evaporación y hardware que sufría estrangulamiento térmico (*thermal throttling*) al menor pico de demanda.

Junto a su socio **Pol Valls** (ingeniero de software y especialista en producto), Pope llegó a una conclusión irrevocable: el aire es un conductor térmico pésimo. El líquido tiene una capacidad calorífica volumétrica **más de mil veces superior a la del aire**.

En 2015, en una nave industrial de L'Hospitalet de Llobregat (Barcelona), los fundadores comenzaron a sumergir placas base encendidas en peceras y contenedores caseros llenos de aceites minerales y fluidos no conductores. Los primeros prototipos eran toscos y generaban escepticismo entre los directores de IT tradicionales, aterrorizados ante la idea de verter líquidos sobre microchips de miles de euros.

Pero la física era inapelable. En 2018, Submer presentó en el *Mobile World Congress* su primer producto comercial, el **SmartPod**: un tanque horizontal sellado donde los servidores estándar de rack se introducen verticalmente en un fluido transparente y viscoso. Al encenderlo, las placas funcionaban a temperaturas gélidas sin un solo ventilador ruidoso, en un silencio sepulcral y reduciendo el consumo eléctrico de refrigeración en más de un **95%**.

### La Ciencia de la Inmersión Monofásica: Fluidos Dieléctricos y Termodinámica

A diferencia de la refrigeración líquida directa al chip (*Direct-to-Chip*, donde pequeños tubos de agua tocan únicamente la CPU), Submer apostó por la **refrigeración por inmersión líquida monofásica completa (*Single-Phase Immersion Cooling*)**.

El funcionamiento del sistema se sustenta en tres principios de ingeniería fundamentales:

#### 1. Fluidos Dieléctricos Sintéticos Biodegradables
El corazón de la tecnología no es agua (que provocaría un cortocircuito inmediato), sino fluidos hidrocarburos sintéticos de formulación propietaria (y alianzas con gigantes químicos como Castrol / BP). Son fluidos **dieléctricos** (aislantes eléctricos absolutos), inodoros, no tóxicos, completamente biodegradables y con un punto de evaporación altísimo. Los componentes electrónicos —chips, memorias RAM, pistas de cobre, condensadores y fuentes de alimentación— operan sumergidos permanentemente en el líquido sin la más mínima degradación ni corrosión.

#### 2. Convección Natural y Bombeo de Ultra-Baja Energía
El fluido frío entra por la base del tanque. Al entrar en contacto con las GPUs y procesadores calientes, el líquido absorbe el calor por conducción directa, pierde densidad y asciende por convección hacia la superficie. Una bomba de bajo consumo extrae el fluido caliente y lo envía a un intercambiador de calor de placas exterior (refrigerado por un circuito cerrado de agua externa o circuito seco), devolviendo el fluido frío al tanque en un ciclo continuo y cerrado.

#### 3. El Indicador Maestro: PUE de 1.03
El rendimiento de un centro de datos se mide por el **PUE (*Power Usage Effectiveness*)**:
$$\text{PUE} = \frac{\text{Energía Total del Data Center}}{\text{Energía Consumida por el Hardware IT}}$$
En un centro de datos clásico con aire acondicionado, el PUE ronda **1.50 a 1.60** (por cada vatio que consume un procesador, se gastan otros 0.5 o 0.6 vatios en mover aire y enfriar la sala).

Submer pulverizó esta métrica hasta situarla en **1.03**. Prácticamente el **97% de toda la electricidad que entra en la instalación se destina a computar**, eliminando el desperdicio energético casi por completo.

![Comparativa técnica entre la refrigeración por aire tradicional y la inmersión líquida de Submer](refrigeracion_inmersion_submer.jpg)

### Financiación y Alianzas: La Consagración de un Campeón Industrial

La trayectoria financiera de Submer refleja la maduración de una de las *deep tech* de hardware más ambiciosas de Europa:

* **Rondas Iniciales (2018–2020)**: Apoyo clave de fondos de capital riesgo como **Alma Mundi Ventures**, validando la tecnología en proyectos piloto en telecomunicaciones y supercomputación.
* **Serie B (2022)**: Entrada del fondo europeo de inversión de impacto **Planet First Partners** con una inyección de **34 millones de dólares**, permitiendo a la empresa abrir fábricas y centros de excelencia de I+D en Estados Unidos (Houston) y Taiwán.
* **Serie C y la antesala del Unicornio (2024–2026)**: En octubre de 2024, Submer cerró una ronda Serie C de **55,5 millones de dólares** liderada por el gigante británico **M&G Investments**, con la participación de **Norrsken VC** y Mundi Ventures. Esta operación situó la valoración de la compañía en el entorno de los **500 millones de euros**, preparándola para el asalto a la categoría de unicornio.
* **Evolución a Operador de Infraestructura e InferX (2025–2026)**: La empresa no se ha limitado a vender tanques de inmersión; ha lanzado filiales dedicadas como **InferX** y unidades de negocio para diseñar, construir y operar campus enteros de supercomputación, destacando su macroproyecto de **56 MW en Barcelona** diseñado específicamente para alojar clusters de Inteligencia Artificial como Servicio (*AI-as-a-Service*).

A nivel industrial, la clave de su hegemonía radica en su colaboración con el **Open Compute Project (OCP)** y alianzas directas con fabricantes de chips como **Intel** (con quienes diseñó especificaciones de referencia para procesadores Xeon sumergidos) y el ecosistema de integradores de **Nvidia**, garantizando que los servidores vengan certificados de fábrica para sumergirse sin perder la garantía del fabricante.

---

### La Barrera de la AGI: Por Qué la IA Depende de la Termodinámica

En nuestro análisis de [Alan Turing](/es/posts/alan_turing/) y [Oppenheimer](/es/posts/oppenheimer/) vimos cómo los grandes saltos científicos siempre acaban chocando contra la realidad material del mundo físico.

La carrera hacia la AGI ha topado con un muro insalvable: **la densidad de potencia por metro cuadrado**.

Para entrenar modelos que razonen con cadenas de pensamiento profundo (como analizamos en [Silicon Valley](/es/posts/silicon_valley/)), las GPUs deben colocarse a distancias microscópicas unas de otras para evitar la latencia de interconexión en el bus de red. Colocar ocho chips de 1.000 vatios cada uno en un chasis de servidor de pocas pulgadas crea un punto térmico que el aire no puede disipar sin que el chip reduzca automáticamente su velocidad de reloj por seguridad.

La refrigeración líquida de Submer desactiva este cuello de botella:
1. **Densidad Sin Precedentes**: Permite albergar más de **100 kW por rack** en el mismo espacio donde el aire solo permitía 15 o 20 kW, multiplicando por cinco la potencia computacional por metro cuadrado de suelo.
2. **Cero Consumo de Agua**: Los centros de datos de IA han sido duramente criticados por evaporar millones de litros de agua dulce en épocas de sequía. La inmersión en circuito cerrado de Submer elimina prácticamente la evaporación de agua.
3. **Economía Circular y Calefacción Urbana**: El calor extraído del fluido no se expulsa al exterior; sale a temperaturas de entre 45°C y 55°C, ideales para inyectarse directamente en redes de calefacción urbana (*district heating*) de ciudades o procesos agrícolas industriales, en perfecta consonancia con las auditorías ambientales del [EU AI Act](/es/posts/eu_ai_act/) y [Clarity AI](/es/posts/clarity_ai/).

---

### Cuadro Comparativo: Startups Tecnológicas en Datalaria

Con la entrada de Submer, el cuadro de honor de la innovación tecnológica española analizada en Datalaria abarca desde el software de analítica y visión artificial hasta el hardware más profundo:

| Compañía | Fundación / Sede | Dominio Tecnológico Clave | Modelo de Negocio | Hito Corporativo Destacado |
| :--- | :---: | :--- | :--- | :--- |
| **Devo** | 2011 / Madrid–Boston | Ingesta masiva de logs en tiempo real y ciberseguridad | B2B SaaS Enterprise / SIEM | Unicornio (valoración >1.500M$) |
| **Flywire** | 2011 / Valencia–Boston | Pasarelas de pago transfronterizas complejas con ML | B2B2C Fintech | Salida a bolsa en NASDAQ ($FLYW) |
| **Carto** | 2012 / Madrid–NY | Inteligencia geoespacial (Location Intelligence) y Spatial SQL | B2B Cloud Data Analytics | Líder mundial en analítica espacial |
| **Clarity AI** | 2017 / Madrid–NY | Scoring ESG y analítica de sostenibilidad con IA | B2B SaaS Fintech | Alianzas con BlackRock y BNP Paribas |
| **Nextail** | 2014 / Madrid | Optimización de inventario retail con analítica prescriptiva | B2B SaaS Retail / Supply Chain | Despliegue en retailers de 30+ países |
| **Freepik** | 2010 / Málaga | Banco de recursos creativos y modelos fundacionales GenAI | B2C/B2B Freemium / GenAI | Adquisición por el fondo EQT |
| **Multiverse Computing** | 2019 / San Sebastián | Redes tensoriales cuánticas para compresión de LLMs | B2B Deep Tech Cuántica | Líder europeo en software cuántico |
| **Wallapop** | 2013 / Barcelona | Visión artificial, grafos antifraude y economía circular | C2C/B2C Marketplace | Adquisición mayoritaria por NAVER (>800M€) |
| **HappyRobot** | 2022 / SF–Madrid | Agentes de voz autónomos en tiempo real para logística | B2B SaaS Enterprise / Voice AI | Unicornio (valoración 1.200M$, Serie C) |
| **Submer** | 2015 / Barcelona | **Refrigeración líquida por inmersión para supercomputación e IA** | **B2B Deep Tech Hardware / Data Centers** | **Ronda Serie C (55M$, valoración ~500M€)** |

---

### 5 Lecciones de Ingeniería y Negocio de Submer

La trayectoria de Daniel Pope y Pol Valls ofrece enseñanzas invaluables para constructores de tecnología:

#### 1. Ataca los límites físicos, no solo los algorítmicos
Muchas startups se apresuran a crear capas de software sobre APIs ajenas. El valor más defendible a largo plazo suele residir en los fundamentos físicos de la infraestructura: la termodinámica, los materiales y la eficiencia energética.

#### 2. La sostenibilidad como ventaja económica, no como eslogan
Submer no convenció a los gigantes de la computación apelando a su conciencia ecológica; los convenció demostrando que un PUE de 1.03 ahorra decenas de millones de euros en gasto operativo (*OPEX*) y reduce la inversión en espacio (*CAPEX*). La mejor tecnología verde es la que resulta económicamente imbatible.

#### 3. Comprométete con los estándares abiertos desde el día uno
Crear tecnología propietaria incompatible con los estándares de la industria es una condena al ostracismo. Diseñar sus racks bajo los estándares del *Open Compute Project* permitió a Submer integrarse sin fricción en las cadenas de suministro de los grandes fabricantes de servidores.

#### 4. La fiabilidad del hardware exige paciencia de capital
Construir hardware crítico para centros de datos requiere años de homologaciones químicas, ensayos de toxicidad y pruebas de estrés. Buscar inversores alineados con los ciclos de la *deep tech* (como Planet First o Norrsken) fue decisivo para no morir en el valle de la muerte inicial.

#### 5. El calor residual es un recurso, no un residuo
En la era de la transición energética, disipar calor a la atmósfera es una ineficiencia inaceptable. Diseñar sistemas capaces de transferir calor a redes urbanas convierte a los centros de datos de vecinos indeseados en infraestructuras cívicas útiles.

---

### Conclusión

La carrera hacia la Inteligencia Artificial General no se decidirá únicamente en los despachos de Silicon Valley programando nuevas funciones de pérdida ni en las conferencias académicas de aprendizaje automático. Se decidirá, en gran medida, en la capacidad de la civilización humana para suministrar energía y disipar el calor generado por millones de transistores trabajando al unísono.

Desde una nave industrial en Barcelona, Daniel Pope y Pol Valls comprendieron que el futuro de la inteligencia digital exigía sumergir el silicio en líquido. Hoy, cuando los mayores clusters de IA del planeta comienzan a operar bajo un mar silencioso de fluidos dieléctricos, la visión de Submer ha dejado de ser una excentricidad experimental: se ha convertido en **los cimientos físicos sobre los que se construye el futuro de la computación humana**.

---

#### Fuentes de Interés:
* [**Submer**: Portal Oficial y Catálogo de Tecnología de Inmersión](https://submer.com/)
* [**YouTube**: Immersion Cooling in 10 MIN — Submer Official Guide](https://www.youtube.com/watch?v=Fj-yRj84Z7U)
* [**YouTube**: Interview with Submer CEO, Daniel Pope](https://www.youtube.com/watch?v=k4Sj4n4x89k)
* [**Open Compute Project (OCP)**: Immersion Cooling Requirements & Standards](https://www.opencompute.org/)
* [**Datalaria**: Clarity AI — La Revolución de la Sostenibilidad y las Métricas ESG](/es/posts/clarity_ai/)
* [**Datalaria**: Devo — Ingesta Masiva de Datos e Infraestructura en Tiempo Real](/es/posts/devo/)
* [**Datalaria**: HappyRobot — Cómo los Agentes de Voz Conquistaron la Logística](/es/posts/happyrobot/)
* [**Datalaria**: J. Robert Oppenheimer — De Monte Carlo al Dilema Ético de la AGI](/es/posts/oppenheimer/)
* [**Datalaria**: EU AI Act — Guía Práctica de Gobernanza y Eficiencia de la IA](/es/posts/eu_ai_act/)
* [**Datalaria**: Silicon Valley y el Dilema de PiperNet — La IA Incontrolable](/es/posts/silicon_valley/)
