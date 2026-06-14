---
title: "La Economía Oculta de la IA: Cuánto Cuesta Realmente Usar LLMs en Producción (Con Datos Reales)"
date: 2026-06-14
draft: false
categories: ["Inteligencia Artificial", "Ingeniería", "Productividad"]
tags: ["costes ia", "api pricing", "llm", "gemini", "openai", "claude", "producción", "tokens", "crewai", "github actions"]
description: "Análisis real de los costes de usar modelos de lenguaje (LLMs) en producción. Comparativa de APIs de Gemini, GPT-4o y Claude con datos propios de los proyectos Autopilot y Obsolescencia de Datalaria. Desglose del iceberg de costes ocultos."
summary: "Todo el mundo habla de lo que la IA puede hacer. Casi nadie habla de lo que la IA cuesta hacer. Después de más de 6 meses operando agentes autónomos en producción con Gemini, CrewAI y GitHub Actions, abro las cuentas y desgrano cada euro invertido — y cada sorpresa que encontré por el camino."
social_text: "Todo el mundo habla de lo que la IA puede hacer. Casi nadie habla de lo que CUESTA. Abro mis cuentas reales después de 6 meses operando agentes IA en producción 🧾💸🤖 #IA #LLM #Costes #Producción #Gemini"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

Hay una verdad incómoda que la industria de la inteligencia artificial prefiere susurrar en lugar de proclamar: **el coste real de poner un LLM en producción casi nunca coincide con la factura de la API**. Es como comprar un coche y descubrir que el precio del concesionario no incluía ni las ruedas, ni el seguro, ni la gasolina. La etiqueta dice "0,15$ por millón de tokens de entrada". Lo que no dice es cuántos millones de tokens quemará tu agente en un bucle de delegación que se descontrola a las 3 de la madrugada.

Lo sé porque me ha pasado. Durante los últimos seis meses he operado sistemas de agentes autónomos en producción real: el [Proyecto Autopilot](/es/posts/ia_agents_part1/) (9 entregas) para automatizar la distribución de contenido en redes sociales, y la serie de [Ingeniería de la Obsolescencia](/es/posts/obs_parte1_intro/) (7 entregas) con un radar agéntico 24/7 para monitorear riesgos en la cadena de suministro. Este artículo no es un ejercicio teórico: es una radiografía de mis facturas reales, mis errores y mis lecciones aprendidas.

![El iceberg de los costes ocultos de la IA](iceberg_costes_ocultos.png)

### El Iceberg: Lo que la Factura de la API No te Cuenta

El error más peligroso al presupuestar un proyecto de IA generativa es **confundir el coste de la API con el coste total del sistema**. Es como medir el coste de un restaurante solo por el precio de los ingredientes. En mi experiencia operando estos sistemas, la API representa aproximadamente un **15-25% del coste real**. El resto es el iceberg sumergido:

| Capa de Coste | Qué Incluye | % Típico |
| :--- | :--- | :---: |
| **API del LLM** | Tokens de entrada/salida, caché de contexto | 15-25% |
| **Infraestructura** | GitHub Actions (minutes), Netlify Functions, Supabase | 25-35% |
| **Tiempo de Ingeniero** | Debugging de agentes, prompt tuning, programación defensiva | 30-40% |
| **Costes Silenciosos** | Reintentos por fallos, bucles infinitos, sobre-consumo de tokens | 10-15% |

El tercer bloque —el tiempo de ingeniero— es donde la mayoría de los proyectos mueren. Como documenté en el [post-mortem del Autopilot](/es/posts/ia_agents_part9/), los modelos son estocásticos: ejecutas el mismo pipeline diez veces y obtienes diez resultados diferentes. Eso significa que **no puedes testear un agente IA como testeas un microservicio convencional**. Necesitas programación defensiva, validación de output con JSON Schemas, y reintentos con backoff exponencial. Cada hora invertida en esa ingeniería tiene un coste.

### La Comparativa que Nadie Hace: Gemini vs GPT-4o vs Claude en Producción Real

Las comparativas de LLMs que abundan online suelen medir benchmarks académicos: MMLU, HumanEval, razonamiento lógico. Eso está bien para papers de investigación, pero en producción lo que importa es la **ecuación coste-calidad-fiabilidad por tarea concreta**. Aquí va mi experiencia operativa con los tres modelos principales:

| Criterio | Gemini 2.5 Flash | GPT-4o | Claude Sonnet 4 |
| :--- | :--- | :--- | :--- |
| **Coste Input** (por 1M tokens) | $0,15 | $2,50 | $3,00 |
| **Coste Output** (por 1M tokens) | $0,60 | $10,00 | $15,00 |
| **Latencia media** (respuesta completa) | ~2,1s | ~3,8s | ~4,5s |
| **Fiabilidad JSON** (structured output) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Respeto de instrucciones de sistema** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Creatividad / "personalidad"** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

La diferencia de precio entre Gemini Flash y sus competidores no es un porcentaje: es un **orden de magnitud**. Para tareas de alto volumen y baja creatividad —clasificación, extracción de datos estructurados, parsing de emails— Gemini Flash es imbatible. Es exactamente por eso que lo elegí como motor del [radar agéntico de obsolescencia](/es/posts/obs_parte5_radar/): necesitaba ejecutar cientos de análisis al mes sin que la factura se disparara.

Sin embargo, cuando la tarea exige matiz, personalidad o razonamiento complejo, la diferencia de calidad justifica el precio. En el Proyecto Autopilot, el agente que escribía posts para LinkedIn con tono "corporativo" y el que escribía tweets con tono "cínico" ([Parte 3](/es/posts/ia_agents_part3/)) rendían significativamente mejor con modelos de gama alta. **La lección: no existe el "mejor modelo", existe el modelo correcto para cada tarea de tu pipeline.**

### Anatomía de una Factura Real: El Proyecto Autopilot

Desglosemos los costes reales de operar el Proyecto Autopilot durante un mes típico. Este sistema analiza cada nuevo post del blog, genera contenido optimizado para Twitter y LinkedIn en dos idiomas (ES/EN), pasa por una auditoría de calidad, y publica automáticamente con aprobación humana.

| Concepto | Coste Mensual | Notas |
| :--- | :--- | :--- |
| **Gemini API** (Flash + Pro) | ~1,20 € | ~4 ejecuciones/mes, ~50K tokens por ejecución |
| **GitHub Actions** (CI/CD minutes) | 0,00 € | Free tier: 2.000 min/mes (sobra para esto) |
| **Brevo** (Newsletter) | 0,00 € | Free tier: 300 emails/día |
| **Netlify** (Functions + Hosting) | 0,00 € | Free tier: 125K invocaciones/mes |
| **Supabase** (PostgreSQL) | 0,00 € | Free tier: 500MB, 2 proyectos |
| **Dominio** (datalaria.com) | ~1,50 € | Prorrateado mensual |
| **Tiempo de ingeniero** | ¿? | El verdadero coste oculto |
| **Total infraestructura** | **~2,70 €/mes** | |

Sí, has leído bien: **menos de 3 euros al mes** para operar un sistema completo de agentes IA con publicación automatizada en redes sociales, newsletter y CI/CD. La clave está en tres decisiones arquitectónicas deliberadas:

1. **Gemini Flash como motor principal**: A $0,15/M tokens de entrada, el coste por ejecución es de céntimos, no de euros.
2. **Free tiers agresivos**: GitHub Actions, Netlify, Supabase y Brevo ofrecen generosos planes gratuitos que cubren sobradamente un proyecto individual o una startup temprana.
3. **Ejecución bajo demanda**: El pipeline no corre 24/7, solo se activa con cada nuevo post (evento), evitando el coste de servidores siempre encendidos.

### La Trampa de los Bucles: Cuando tu Agente Quema Dinero Solo

Pero la factura no siempre es tan amable. En el post-mortem del Autopilot documenté un fallo crítico que todo ingeniero debería conocer: los **bucles de delegación infinita** de CrewAI. Cuando un agente no encuentra la respuesta esperada, puede re-delegarse la tarea a sí mismo en un bucle que consume tokens exponencialmente hasta que GitHub Actions mata el proceso por timeout (**SIGTERM** a los 60 minutos).

En una sola ejecución fallida, ese bucle puede consumir **más tokens que un mes entero de operación normal**. Es el equivalente digital de dejar un grifo abierto toda la noche. La solución es brutalmente simple pero nadie la implementa de serie:

* **`max_iter`** y **`max_execution_time`** en cada agente CrewAI
* **Validación de output** con Pydantic antes de pasar al siguiente agente
* **Alertas de coste** configuradas en la consola de Google Cloud
* **Circuit breakers** que matan la ejecución si el consumo supera un umbral

{{< youtube 7zbuEULTHIs >}}

### La Regla del 10x: Cuándo Merece la Pena Pagar Más

Después de seis meses operando estos sistemas, he destilado una regla pragmática que llamo la **Regla del 10x**: un modelo más caro solo se justifica si produce un resultado al menos **10 veces mejor** en la métrica que importa para tu caso de uso. ¿Qué significa "10 veces mejor"?

* **En clasificación**: 10x menos errores de clasificación
* **En generación de contenido**: 10x menos iteraciones humanas de corrección
* **En extracción de datos**: 10x menos alucinaciones verificables
* **En latencia**: 10x más rápido en la ruta crítica del usuario

Si la mejora es de un 20-30%, quédate con el modelo barato. Si es de un 2x-3x, evalúa. Si es de un 10x, no lo pienses. Esta regla me llevó a usar Gemini Flash para el 90% de las tareas y reservar modelos premium solo para la generación creativa de contenido.

### Mirando al Futuro: La Deflación de la Inteligencia

Hay una tendencia macro que todo ingeniero debe tener en el radar: **el coste por token está cayendo a un ritmo brutal**. Gemini Flash en junio de 2025 costaba $0,35/M tokens de entrada. Un año después, cuesta $0,15 — una caída del **57% en 12 meses**. Si esta tendencia se mantiene (y todo indica que se acelerará con la competencia de modelos open-source como Llama y Mistral), en dos años estaremos hablando de costes de API que serán **esencialmente gratuitos** para la mayoría de los casos de uso.

Eso no significa que la IA será gratis. Significa que **el coste se desplazará definitivamente de la API al ingeniero**: la capacidad de diseñar sistemas robustos, implementar programación defensiva, y orquestar pipelines complejos será el verdadero diferencial competitivo. El modelo será un commodity; la arquitectura será el moat.

Como bien decía W. Edwards Deming —al que dediqué un [artículo completo](/es/posts/deming/)— : *"No basta con hacer lo mejor que puedas; primero debes saber qué hacer"*. En la economía oculta de la IA, saber qué modelo usar, cuándo usarlo y cuándo **no** usarlo es la habilidad más valiosa que puedes desarrollar.

---

#### Fuentes de Interés:
* [**Google AI**: Gemini API Pricing — Modelos y Precios Actualizados](https://ai.google.dev/pricing)
* [**OpenAI**: API Pricing — Modelos GPT-4o, GPT-4o mini](https://openai.com/api/pricing/)
* [**Anthropic**: Claude API Pricing — Modelos Claude 4 y Sonnet](https://www.anthropic.com/pricing)
* [**Datalaria**: Post-Mortem del Proyecto Autopilot — Lecciones Aprendidas](/es/posts/ia_agents_part9/)
* [**Datalaria**: El Radar Agéntico — Tool Calling vs RAG en Producción](/es/posts/obs_parte5_radar/)
* [**Andreessen Horowitz**: The Cost of AI — Who Pays and How Much? (Informe Andreessen Horowitz)](https://a16z.com/navigating-the-high-cost-of-ai-compute/)
* [**GitHub**: GitHub Actions Billing — Free Tier y Precios](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
