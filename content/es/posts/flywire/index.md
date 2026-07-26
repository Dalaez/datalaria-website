---
title: "Flywire: Cómo un Español Construyó desde Boston el Cerebro de los Pagos Internacionales"
date: 2026-07-25
draft: false
categories: ["casos_exito"]
tags: ["flywire", "fintech", "pagos internacionales", "nasdaq", "startup española", "machine learning", "cross-border", "iker marcaide"]
description: "La historia de Flywire (FLYW), el unicornio español cotizado en el Nasdaq que procesa miles de millones en pagos internacionales para educación, sanidad y viajes. Cómo Iker Marcaide convirtió un dolor de estudiante en MIT en una plataforma global que usa ML para optimizar cada transacción."
summary: "Cuando un estudiante coreano intenta pagar la matrícula de una universidad en Madrid, se enfrenta a un laberinto de comisiones bancarias, tipos de cambio opacos y transferencias que tardan 5 días. Un ingeniero español en MIT decidió que eso era inaceptable. Hoy, su empresa Flywire cotiza en el Nasdaq, factura más de 600 millones de dólares y procesa pagos en 140 divisas usando machine learning para optimizar cada transacción."
social_text: "Un estudiante español en MIT se harta de los pagos universitarios internacionales. Funda peerTransfer en 2009. Hoy, se llama Flywire, cotiza en el Nasdaq ($FLYW), factura $600M+ y procesa pagos en 140 divisas con ML 🇪🇸💸🌍 #Flywire #Fintech #StartupEspañola"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

Cuando un estudiante coreano intenta pagar la matrícula de una universidad en Madrid, se enfrenta a un laberinto kafkiano: comisiones bancarias opacas que devoran entre un 3% y un 5% de la transacción, tipos de cambio desfavorables impuestos unilateralmente por el banco intermediario, transferencias SWIFT que tardan entre 3 y 5 días hábiles en liquidarse, y un sistema de referencia de pago que, si el estudiante se equivoca en un solo dígito, provoca que la universidad no pueda reconciliar el ingreso con su matrícula. El resultado: el estudiante paga de más, la universidad recibe de menos, y ambos pierden tiempo en correos electrónicos y llamadas intentando cuadrar las cuentas.

**Iker Marcaide**, un ingeniero español cursando su MBA en el **MIT Sloan School of Management** en Boston, vivió este dolor en primera persona. Pero a diferencia del 99% de las personas que se quejan del sistema bancario internacional y siguen adelante, Marcaide hizo lo que hacen los fundadores: **se preguntó por qué tenía que ser así y construyó la alternativa**.

En 2009, fundó **peerTransfer** — una plataforma que permitía a los estudiantes internacionales pagar su matrícula en su moneda local, con tipos de cambio transparentes, comisiones mínimas y liquidación garantizada en la cuenta de la universidad. En 2016, la empresa se rebautizó como **Flywire** para reflejar su expansión más allá de la educación. En mayo de 2021, salió a cotizar en el **Nasdaq** bajo el ticker **$FLYW**. En el año fiscal 2025, facturó más de **603 millones de dólares**, con un crecimiento interanual del 27%. En el primer trimestre de 2026, los ingresos alcanzaron **188 millones de dólares**, un 41% más que el mismo trimestre del año anterior.

Es, junto a [Carto](/es/posts/carto/), [Devo](/es/posts/devo/), [Clarity AI](/es/posts/clarity_ai/), [Nextail](/es/posts/nextail/) y [Freepik](/es/posts/freepik/), una de las startups españolas que han alcanzado escala global. Pero Flywire tiene un rasgo que la distingue de todas las demás: **cotiza en la bolsa americana**. No en el MAB, no en una ronda privada, no en el BME Growth — en el Nasdaq, junto a Apple, Google y Tesla.

{{< youtube 0eGSRmq1dPc >}}


### La Tecnología: El Cerebro Inteligente de los Pagos

Flywire no es un procesador de pagos convencional como Stripe o PayPal. La diferencia fundamental está en que Flywire ha construido una plataforma diseñada específicamente para **pagos complejos, de alto valor y cross-border**, donde la fricción no está en el último clic del usuario (eso ya lo resolvió Stripe), sino en toda la cadena que ocurre detrás: el routing entre bancos, la conversión de divisas, la reconciliación con el sistema del receptor, y el cumplimiento regulatorio de múltiples jurisdicciones.

La plataforma opera en tres capas tecnológicas que se refuerzan mutuamente:

**1. Red Global de Pagos Propietaria**: Flywire ha construido una red de conexiones bancarias directas en más de **240 países y territorios**, soportando pagos en más de **140 divisas**. Esta red propia les permite seleccionar la ruta óptima para cada transacción — no la ruta por defecto del sistema SWIFT, que puede pasar por 3-4 bancos intermediarios, cada uno cobrando su comisión, sino la ruta más directa, rápida y económica para ese corredor de divisas específico.

**2. Machine Learning para Optimización de Transacciones**: Aquí es donde la ingeniería de datos marca la diferencia competitiva. Flywire utiliza algoritmos de ML para tres funciones críticas:

* **Routing inteligente**: Para cada transacción, el sistema evalúa múltiples rutas bancarias y selecciona la combinación óptima de tipo de cambio, velocidad de liquidación y coste total. No es una tabla estática de rutas; es un modelo que aprende continuamente de las transacciones históricas para optimizar cada corredor de divisas.
* **Reconciliación automática con deep learning**: La pesadilla de las oficinas de tesorería de universidades y hospitales es reconciliar los pagos recibidos con las facturas pendientes. Cuando un estudiante paga desde Corea del Sur, el nombre del pagador puede aparecer transliterado de tres formas diferentes, la referencia de pago puede estar truncada, y el importe recibido difiere del facturado por las comisiones intermedias. Flywire usa **redes neuronales profundas y aprendizaje por refuerzo** para emparejar automáticamente pagos con facturas, incluso cuando los datos no coinciden exactamente.
* **Detección de fraude**: Modelos de ML que analizan patrones de transacciones para identificar anomalías y prevenir fraude antes de que la transacción se complete.

**3. Software Vertical Especializado**: Para cada industria, Flywire no solo procesa pagos sino que se integra directamente en los sistemas core del cliente — **Student Information Systems (SIS)** en educación, **Electronic Health Records (EHR)** en sanidad, **ERPs** en B2B. Esta integración profunda convierte a Flywire en infraestructura, no en un proveedor intercambiable.

### La Expansión Vertical: El Patrón "Land and Expand"

La historia de crecimiento de Flywire sigue un patrón que hemos visto repetirse en cada unicornio español que hemos analizado en este blog: **encuentra un dolor específico en una vertical, resuélvelo con ingeniería obsesiva, y expándete horizontalmente**.

![La expansión vertical de Flywire: de educación a sanidad y viajes](expansion_vertical.png)

**Educación (2009-2016)**: El punto de partida. peerTransfer resolvió el dolor de los pagos de matrícula internacional, empezando por universidades en Estados Unidos y expandiéndose a Europa, Australia y Asia. La propuesta de valor era clara: el estudiante paga en su moneda local con total transparencia, la universidad recibe exactamente el importe facturado sin comisiones ocultas, y la reconciliación es automática. Hoy, Flywire procesa pagos para más de **3.800 instituciones educativas** a nivel global.

**Sanidad / Healthcare (2016-2019)**: El salto a sanidad fue natural. Los hospitales americanos enfrentan el mismo problema de pagos complejos: pacientes internacionales, seguros fragmentados, planes de pago a plazos, y una reconciliación administrativa que consume recursos enormes. Flywire adaptó su plataforma para integrarse con los sistemas de gestión hospitalaria y ofrecer opciones de pago flexibles (planes de financiación, pagos parciales) que mejoran la tasa de cobro del hospital y la experiencia del paciente.

**Viajes / Travel (2019-presente)**: La tercera vertical. Los operadores turísticos, agencias de viajes y hoteles de lujo manejan reservas de alto valor con clientes internacionales que quieren pagar en su moneda local. Los márgenes son estrechos, y perder un 3-5% en comisiones de tipo de cambio puede destruir la rentabilidad de una reserva. Flywire ofrece la misma transparencia y routing inteligente, adaptada al flujo de trabajo específico de la industria del viaje.

**B2B (2021-presente)**: La cuarta frontera. Pagos entre empresas a nivel internacional — facturas, liquidaciones de proveedores, pagos de royalties. El patrón se repite: complejidad regulatoria, múltiples divisas, reconciliación manual ineficiente. Flywire automatiza el flujo completo de *invoice-to-cash*.

### Las Cifras: Un Unicornio Español en el Nasdaq

| Métrica | Dato |
| :--- | :--- |
| **Fundación** | 2009 (como peerTransfer) |
| **Rebrand a Flywire** | 2016 |
| **IPO Nasdaq** | Mayo 2021 (ticker: $FLYW) |
| **Revenue FY2025** | ~$603 millones (+27% YoY) |
| **Revenue Q1 2026** | $188 millones (+41% YoY) |
| **Divisas soportadas** | 140+ |
| **Países** | 240+ |
| **Clientes educación** | 3.800+ instituciones |
| **Sede** | Boston, MA (EE.UU.) |
| **Fundador** | Iker Marcaide (España) |

Para poner las cifras en contexto dentro del ecosistema de unicornios españoles: Flywire factura más que [Devo](/es/posts/devo/) (adquirida por LogRhythm en 2023 tras alcanzar valoración de unicornio) y más que [Nextail](/es/posts/nextail/) (que opera en un nicho más estrecho de retail). La comparación más directa es con [Clarity AI](/es/posts/clarity_ai/) — ambas son fintech, ambas operan desde el ecosistema regulatorio europeo pero con mercado global, y ambas enfrentan las exigencias del [EU AI Act](/es/posts/eu_ai_act/) por operar en categorías sensibles (servicios financieros esenciales, Anexo III del reglamento).

### Lecciones para Ingenieros

La historia de Flywire destila tres lecciones que aplican a cualquier ingeniero que construya productos tecnológicos:

**Lección 1: El "Efecto Plataforma" — Empieza por un dolor, expándete por la infraestructura**

Flywire no empezó diciendo «vamos a construir una plataforma global de pagos». Empezó diciendo «vamos a resolver los pagos de matrícula internacional para universidades americanas». Un dolor específico, un cliente específico, un mercado específico. Una vez que la plataforma estaba construida y probada en educación, la expansión a sanidad y viajes fue una extensión natural del mismo motor tecnológico aplicado a un flujo de trabajo diferente.

Es el mismo patrón que vimos en [Carto](/es/posts/carto/) (empezó como herramienta de visualización geoespacial, se expandió a Location Intelligence empresarial), en [Devo](/es/posts/devo/) (empezó como SIEM de siguiente generación, se expandió a observabilidad completa para defensa y ciberseguridad), y en [Nextail](/es/posts/nextail/) (empezó optimizando el inventario de tienda, se expandió a IA prescriptiva para toda la cadena de suministro del retail).

**Lección 2: Build vs. Buy — Por qué Flywire construyó su propio motor de pagos**

La pregunta obvia es: ¿por qué no usar Stripe? Stripe es extraordinario para pagos online estándar (e-commerce, SaaS). Pero los pagos cross-border de alto valor tienen tres requisitos que Stripe no resolvía en 2009 (y que sigue sin resolver completamente para este nicho): routing inteligente por corredor de divisas, reconciliación automática con sistemas verticales (SIS, EHR), y cumplimiento regulatorio multi-jurisdicción para pagos que cruzan fronteras. Flywire necesitaba controlar la cadena completa para optimizar cada eslabón. La decisión build vs. buy se resume en una pregunta: ¿el pago **es** tu producto, o es una funcionalidad auxiliar de tu producto? Si el pago es tu producto (como en Flywire), construyes. Si es auxiliar (como en un e-commerce), compras.

**Lección 3: La regulación como ventaja competitiva, no como freno**

Flywire opera en uno de los sectores más regulados del planeta: pagos financieros transfronterizos. Cumple con regulaciones de anti-lavado de dinero (AML), know-your-customer (KYC), PCI DSS para seguridad de datos de tarjetas, y las regulaciones financieras de cada país donde opera. Como discutimos en el [artículo sobre el EU AI Act](/es/posts/eu_ai_act/), los sistemas de IA que determinan el acceso a servicios financieros esenciales caen en la categoría de «alto riesgo» del reglamento europeo.

Pero Flywire ha convertido esta complejidad regulatoria en una **barrera de entrada para competidores**. Cualquier startup que quiera competir con Flywire en pagos universitarios cross-border necesita no solo construir una plataforma tecnológica comparable, sino también obtener las licencias regulatorias en docenas de jurisdicciones — un proceso que puede tardar años y costar millones. La regulación que ahoga a los competidores potenciales protege a los incumbentes bien posicionados.

### El Patrón Español: Dolor Local, Escala Global

Si miras la serie completa de startups españolas que hemos analizado en este blog, el patrón se repite con una consistencia casi algorítmica:

| Startup | Dolor inicial | Expansión | Resultado |
| :--- | :--- | :--- | :--- |
| **Flywire** | Pagos de matrícula internacional | Educación → Sanidad → Viajes → B2B | Nasdaq ($FLYW), $603M revenue |
| [**Devo**](/es/posts/devo/) | Logging de seguridad | SIEM → Observabilidad → Defensa | Unicornio, adquisición LogRhythm |
| [**Carto**](/es/posts/carto/) | Mapas web | Visualización → Location Intelligence | Plataforma cloud empresarial |
| [**Nextail**](/es/posts/nextail/) | Inventario de tienda | Retail → IA prescriptiva → Supply chain | ESPR 2026, expansión global |
| [**Clarity AI**](/es/posts/clarity_ai/) | Scoring ESG | Sostenibilidad → Fintech → Regulación | Plataforma de impacto, BlackRock |
| [**Freepik**](/es/posts/freepik/) | Banco de imágenes | Stock → IA generativa → Diseño | Rentable desde día 1 |

El denominador común es siempre el mismo: un fundador español con formación internacional, un dolor concreto y verificable, una solución técnicamente obsesiva, y una expansión horizontal una vez que la plataforma base demuestra tracción. Ni la falta de ecosistema VC en España, ni la distancia a Silicon Valley, ni la barrera del idioma han impedido que estas empresas alcancen escala global. Lo que las ha impulsado es exactamente lo que [Deming](/es/posts/deming/) predicaba hace décadas: **calidad obsesiva en la ejecución y mejora continua basada en evidencia**.

Iker Marcaide no inventó los pagos internacionales. Pero hizo lo que hacen los grandes ingenieros: miró un proceso roto, entendió cada eslabón de la cadena, y construyó una solución que era 10 veces mejor que el *status quo*. Hoy, esa solución procesa miles de millones de dólares y cotiza en el Nasdaq. Y empezó con un estudiante español en MIT que se negó a pagar comisiones abusivas por su matrícula.

---

#### Fuentes de Interés:
* [**Flywire**: Sitio Oficial — Plataforma de Pagos Globales](https://www.flywire.com/)
* [**Nasdaq**: Flywire Corporation ($FLYW) — Perfil de Cotización](https://www.nasdaq.com/market-activity/stocks/flyw)
* [**Flywire Investor Relations**: Resultados Financieros Q1 2026](https://ir.flywire.com/)
* [**Xataka**: Iker Marcaide y la Historia de Flywire](https://www.xataka.com/)
* [**YouTube**: Flywire — Simplifying Complex Payments](https://www.youtube.com/watch?v=0eGSRmq1dPc)
* [**Datalaria**: Devo — El SIEM Español que Escaló al Pentágono](/es/posts/devo/)
* [**Datalaria**: Clarity AI — La Fintech que Puntúa al Planeta](/es/posts/clarity_ai/)
* [**Datalaria**: Carto — De Mapas Web a Location Intelligence Empresarial](/es/posts/carto/)
* [**Datalaria**: EU AI Act — Regulación y Fintech como Categoría de Alto Riesgo](/es/posts/eu_ai_act/)
