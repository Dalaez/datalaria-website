---
title: "Fine-Tuning vs Prompt Engineering vs RAG: Cuándo Usar Cada Uno (y la Cuarta Opción que Nadie Menciona)"
date: 2026-08-09
draft: false
categories: ["Inteligencia Artificial", "Ingeniería"]
tags: ["fine-tuning", "prompt engineering", "rag", "tool calling", "llm", "arquitectura ia", "lora", "qlora", "mcp"]
description: "Guía definitiva para elegir entre Prompt Engineering, RAG, Fine-Tuning y Tool Calling. Con árbol de decisión, matriz comparativa de costes y precisión, y los casos reales del Ops Copilot y el Radar de Obsolescencia de Datalaria."
summary: "Tu modelo de IA alucina con los datos de tu empresa. ¿La solución es RAG, fine-tuning, o un prompt mejor? La respuesta correcta depende de una sola pregunta que casi nadie se hace. Después de implementar las cuatro técnicas en producción, he destilado el árbol de decisión que ojalá hubiera tenido al empezar."
social_text: "Tu IA alucina con los datos de tu empresa. ¿La solución es RAG, fine-tuning, o un prompt mejor? Después de implementar las 4 técnicas en producción, he destilado el árbol de decisión definitivo 🧠🌳🔧 #IA #RAG #FineTuning #PromptEngineering #LLM"
image: cover.jpg
weight: 10
authorAvatar: datalaria-logo.png
---

Tienes un modelo de IA que alucina con los datos de tu empresa. Abre un ticket de soporte y le pides al chatbot que responda sobre tu política de devoluciones. El chatbot, alimentado por GPT-4 o Gemini 2.5, responde con una política inventada que suena perfectamente plausible pero no tiene nada que ver con la realidad de tu empresa. Tu jefe te mira. Tu cliente se queja. Tú abres Google y buscas **"cómo conectar LLM a mis datos"**.

Los primeros 10 resultados te ofrecen tres respuestas contradictorias: «usa RAG», «haz fine-tuning», «mejora tu prompt». Los tres tienen razón. Los tres están equivocados. Porque la respuesta correcta no es ninguna de las tres en abstracto — es **la que encaja con tu caso de uso específico**. Y hay una cuarta opción que casi nadie menciona y que, en mi experiencia, es la correcta en más casos de los que la industria admite.

Este artículo es el árbol de decisión que ojalá hubiera tenido cuando empecé a construir los sistemas de IA de este blog. Lo he destilado después de implementar las cuatro técnicas en producción real: Prompt Engineering en toda la [serie Autopilot](/es/posts/ia_agents_part1/), RAG en el [Ops Copilot](/es/posts/ia_agents_part8/) con Algolia, Tool Calling puro en el [Radar de Obsolescencia](/es/posts/obs_parte5_radar/), y fine-tuning experimental en pipelines de clasificación industrial. Cierra la trilogía que empezó con [RAG: 7 Antipatrones](/es/posts/rag_antipatrones/) y continuó con [MCP Protocol](/es/posts/mcp_protocol/).

### La Pregunta que Nadie Se Hace

Antes de elegir una técnica, hazte esta pregunta: **¿El conocimiento que necesita tu LLM cambia o es estático?**

Si la respuesta es «cambia frecuentemente» (documentación de producto, inventario, precios, regulaciones), necesitas una técnica que acceda a datos **en tiempo real** sin reentrenar el modelo. Si la respuesta es «es estático o cambia muy lento» (tono de marca, reglas de formato, nomenclatura de dominio), puedes considerar técnicas que **incorporen ese conocimiento al modelo**.

Esta distinción es el primer nodo del árbol de decisión. Parece obvia escrita así. Sin embargo, la mayoría de los equipos que he visto saltan directamente a la técnica que está de moda (RAG en 2024, fine-tuning en 2023, prompt engineering siempre) sin hacerse esta pregunta fundamental.

![Árbol de decisión: cómo elegir entre las 4 técnicas](arbol_decision.jpg)

### Opción 1: Prompt Engineering — El 80% de los Casos

La verdad incómoda que la industria del tooling de IA no quiere que sepas: **para el 80% de los casos de uso, un prompt bien diseñado es suficiente**. No necesitas RAG. No necesitas fine-tuning. Necesitas un system prompt que defina claramente el rol, el contexto, las restricciones y el formato de salida esperado.

**Cuándo es suficiente**:
- El conocimiento necesario cabe en la ventana de contexto del modelo (Gemini 2.5 maneja hasta 1 millón de tokens; Claude hasta 200K).
- La tarea es genérica pero necesita estructura (redactar emails, resumir documentos, clasificar textos, generar código).
- No necesitas datos propietarios actualizados — el conocimiento general del modelo basta.

**Técnicas avanzadas que marcan la diferencia**:
- **System Prompts estructurados**: Define el rol («Eres un ingeniero de supply chain senior»), las restricciones («Responde siempre en español técnico»), y el formato de salida («Devuelve un JSON con los campos: análisis, recomendación, confianza»).
- **Few-shot prompting**: Incluye 3-5 ejemplos de entrada-salida correctos en el prompt. En la [serie Autopilot](/es/posts/ia_agents_part3/), los agentes de CrewAI usan few-shot para mantener la consistencia de estilo entre artículos generados.
- **Chain-of-thought (CoT)**: Instruye al modelo a «pensar paso a paso» antes de dar la respuesta final. Mejora drásticamente la precisión en tareas de razonamiento, cálculo y análisis multi-paso.
- **Prompt chaining**: Divide tareas complejas en subtareas secuenciales, cada una con su propio prompt optimizado. Es exactamente lo que hace CrewAI con la arquitectura de agentes: cada agente tiene un prompt especializado para su rol.

**Coste**: Prácticamente cero (solo el coste de tokens de la API). Un prompt bien diseñado puede llevar horas de iteración, pero el coste operativo es mínimo.

**Limitación fatal**: La ventana de contexto tiene un límite. Si necesitas que el modelo «sepa» sobre 10.000 documentos de tu base de conocimiento, no puedes inyectarlos todos en el prompt. Aquí es donde entra RAG.

### Opción 2: RAG — Conocimiento Propietario Actualizable

**RAG (Retrieval-Augmented Generation)** es la respuesta correcta cuando necesitas que el LLM responda sobre **tu conocimiento propietario** y ese conocimiento **se actualiza frecuentemente**.

**Cuándo es necesario**:
- Documentación de producto, manuales técnicos, bases de conocimiento internas que se actualizan semanalmente o mensualmente.
- El usuario puede hacer preguntas impredecibles sobre un corpus amplio de documentos (no sabes de antemano qué fragmento necesitará el LLM).
- Necesitas **citabilidad**: que la respuesta incluya las fuentes de donde proviene la información (crítico para compliance, como documentamos en el [EU AI Act](/es/posts/eu_ai_act/), Artículo 13 sobre transparencia).

**Cuándo NO usarlo**: Cuando los datos son estructurados (tablas SQL, APIs con esquemas definidos) o cuando necesitas precisión numérica. Como documenté extensamente en el [Antipatrón 7 del artículo de RAG](/es/posts/rag_antipatrones/), RAG sobre datos estructurados genera alucinaciones narrativas donde necesitas cifras exactas.

**Arquitectura correcta (resumida)**:
1. **Chunking semántico** (no por longitud fija — Antipatrón 1)
2. **Embeddings evaluados** con benchmark de tu dominio (Antipatrón 2)
3. **Reranking** entre el retriever y el LLM (Antipatrón 3)
4. **Contexto generoso** (top-10/15, no top-3 — Antipatrón 4)
5. **Evaluación con RAGAS/DeepEval** antes de producción (Antipatrón 6)

**Coste real**: Moderado. El vector store (Pinecone, Weaviate, Algolia) tiene un coste mensual (€0-100 según volumen), más el coste de embeddings (bajo) y el coste de generación (tokens de API). En el [Ops Copilot](/es/posts/ia_agents_part8/), el coste total de RAG con Algolia fue inferior a **€3/mes** para los ~70 posts del blog.

**Caso real en Datalaria**: El Ops Engineering Copilot ([Autopilot Part 8](/es/posts/ia_agents_part8/)) usa RAG con Algolia Agent Studio para responder preguntas sobre el contenido del blog. Los posts se indexan como records semánticos (un record por sección), y el copilot recupera los fragmentos relevantes antes de generar la respuesta. Funciona bien para búsqueda semántica sobre texto libre.

### Opción 3: Fine-Tuning — El Bisturí, No el Martillo

**Fine-tuning** es la técnica más potente y la más mal utilizada. Consiste en **reentrenar parcialmente** un modelo base (Gemini, Llama, Mistral) con tus propios datos para que el modelo internalice conocimiento, estilo o comportamiento específico.

**Cuándo es imprescindible**:
- Necesitas que el modelo adopte un **tono o estilo muy específico** de forma consistente (una marca con un voice & tone estricto, un dominio con jerga técnica muy particular).
- La tarea es **altamente especializada** y los modelos generalistas no la resuelven bien ni con prompting avanzado (clasificación de defectos industriales, extracción de entidades de nomenclatura propietaria, diagnóstico médico especializado).
- Necesitas **reducir latencia y coste** en producción: un modelo fine-tuneado más pequeño (7B-13B parámetros) puede igualar la calidad de un modelo grande (70B+) en tu tarea específica, a una fracción del coste y la latencia.

**Cuándo NO usarlo** (el mito más extendido):
- **No uses fine-tuning para "enseñarle datos" al modelo**. Fine-tuning no es una base de datos. Si necesitas que el modelo conozca tu catálogo de productos, usa RAG. Fine-tuning «graba» patrones de comportamiento, no hechos actualizables.
- **No uses fine-tuning si tu conocimiento cambia frecuentemente**. Cada actualización requiere reentrenar, lo que puede costar horas y cientos de euros. RAG es instantáneo: actualiza el documento y el retriever lo encuentra inmediatamente.

**Herramientas modernas**:
- **LoRA (Low-Rank Adaptation)**: La técnica estándar. En lugar de reentrenar los miles de millones de parámetros del modelo completo, LoRA entrena solo unas matrices de bajo rango «acopladas» a las capas del modelo. Reduce el coste de entrenamiento en un 90%+ y el almacenamiento del modelo fine-tuneado a unos pocos MB de «adaptadores».
- **QLoRA**: LoRA aplicado sobre un modelo cuantizado a 4 bits. Permite fine-tunear modelos de 70B parámetros en una sola GPU de consumo (24GB VRAM). Democratizó el fine-tuning para startups y equipos sin clusters de GPUs.
- **Vertex AI Tuning / OpenAI Fine-Tuning API**: Servicios gestionados donde subes tu dataset de entrenamiento (pares instrucción-respuesta) y la plataforma ejecuta el fine-tuning sin que gestiones infraestructura GPU.

**Coste real**: Variable. Fine-tuning con LoRA en un modelo de 7B parámetros con 10.000 ejemplos cuesta entre **€5-20** en cloud (Google Cloud, AWS). Un modelo de 70B puede costar **€50-200** por sesión de entrenamiento. Más el coste de preparar el dataset (horas de trabajo humano). Como analizamos en la [Economía Oculta de la IA](/es/posts/economia_oculta_ia/), el coste oculto del fine-tuning no es el compute — es la **curación del dataset de entrenamiento**.

### Opción 4: Tool Calling / MCP — La que Nadie Menciona

Esta es la opción que descubrí por eliminación después de que RAG fallara estrepitosamente en el [Radar de Obsolescencia](/es/posts/obs_parte5_radar/). **Tool Calling** significa que el LLM no intenta «saber» la respuesta; en su lugar, sabe **a quién preguntarle** — es decir, qué herramienta ejecutar para obtener la información con precisión determinista.

**Cuándo es la opción correcta**:
- Los datos son **estructurados** (bases de datos SQL, APIs REST, hojas de cálculo con esquemas).
- Necesitas **precisión numérica absoluta** (cálculos financieros, métricas de inventario, datos de sensores).
- La operación requiere **acciones**, no solo respuestas (crear un ticket, enviar un email, ejecutar un query, llamar a una API externa).
- Quieres **estandarizar las conexiones** entre el LLM y las herramientas para no quedar atado a un proveedor — exactamente el problema que resuelve [MCP (Model Context Protocol)](/es/posts/mcp_protocol/).

**Arquitectura**: El LLM (Gemini 2.5, Claude) actúa como **orquestador semántico**: entiende la intención del usuario en lenguaje natural, decide qué herramienta(s) ejecutar, construye los parámetros, ejecuta la(s) herramienta(s), e interpreta los resultados para el usuario. Las herramientas son funciones Python deterministas (decoradas con `@tool` en CrewAI) que ejecutan operaciones de precisión: queries SQL a Supabase, llamadas a APIs de proveedores, cálculos de programación lineal con PuLP.

**Coste**: El más bajo de las cuatro opciones. Solo pagas los tokens del LLM (típicamente pocos, porque el prompt es corto) y la ejecución de las herramientas (queries SQL, llamadas API). En el Radar de Obsolescencia, el coste por ejecución completa (analizar un componente, cruzar el grafo BOM, calcular impacto financiero, generar reporte ejecutivo) fue inferior a **€0.02 por consulta**.

**Caso real en Datalaria**: El [Radar Agéntico de Obsolescencia](/es/posts/obs_parte5_radar/) usa exclusivamente Tool Calling. El LLM (Gemini 2.5 vía CrewAI) entiende la alerta de obsolescencia en lenguaje natural, pero todas las operaciones de datos — consulta SQL al catálogo de componentes, cruce del grafo BOM, cálculo del P&L, generación del PDF — las ejecutan herramientas Python deterministas. Resultado: reportes ejecutivos en 4 segundos con **0% de alucinación numérica**.

### La Matriz de Decisión

| Criterio | Prompt Engineering | RAG | Fine-Tuning | Tool Calling |
| :--- | :---: | :---: | :---: | :---: |
| **Coste inicial** | ⭐ Mínimo | ⭐⭐ Bajo-medio | ⭐⭐⭐ Alto | ⭐⭐ Bajo |
| **Coste operativo** | ⭐ Bajo | ⭐⭐ Medio | ⭐ Bajo (modelo pequeño) | ⭐ Mínimo |
| **Precisión (texto libre)** | ⭐⭐ Media | ⭐⭐⭐ Alta | ⭐⭐⭐ Muy alta | ⭐ N/A |
| **Precisión (datos estruct.)** | ⭐ Baja | ⭐ Baja | ⭐ Baja | ⭐⭐⭐ Exacta |
| **Actualización de datos** | ⭐⭐⭐ Instantánea | ⭐⭐⭐ Instantánea | ⭐ Requiere reentrenar | ⭐⭐⭐ Tiempo real |
| **Esfuerzo de implementación** | ⭐ Horas | ⭐⭐ Días-semanas | ⭐⭐⭐ Semanas-meses | ⭐⭐ Días |
| **Mantenimiento** | ⭐ Mínimo | ⭐⭐ Medio | ⭐⭐⭐ Alto (data drift) | ⭐⭐ Medio |
| **Trazabilidad (EU AI Act)** | ⭐ Difícil | ⭐⭐⭐ Alta (fuentes citables) | ⭐ Opaca (caja negra) | ⭐⭐⭐ Total (determinista) |
| **Caso de uso ideal** | Tareas genéricas con instrucciones claras | Conocimiento propietario textual, actualizable | Estilo/tono específico, tareas ultra-especializadas | Datos estructurados, precisión numérica, acciones |

### El Framework de 3 Preguntas

Si la matriz te parece densa, he destilado un framework de 3 preguntas que resuelve el 90% de las decisiones:

**Pregunta 1: ¿Los datos que necesita el LLM caben en el prompt?**
- Sí → **Prompt Engineering**. Inyecta el contexto directamente. Es más simple, más barato, más rápido.
- No → Siguiente pregunta.

**Pregunta 2: ¿Los datos son texto libre o estructurados?**
- Texto libre (documentación, manuales, posts) → **RAG**. El retrieval semántico es superior para buscar en texto no estructurado.
- Estructurados (SQL, APIs, tablas, cálculos) → **Tool Calling**. Herramientas deterministas que ejecutan queries exactos.
- Ambos → **Arquitectura híbrida** (RAG para el contexto textual + Tool Calling para los datos estructurados, como propusimos en el [artículo de RAG](/es/posts/rag_antipatrones/)).

**Pregunta 3: ¿Necesitas un comportamiento o estilo que el modelo base no reproduce ni con el mejor prompt?**
- Sí (tono de marca único, jerga de dominio ultra-específica, tarea que los modelos generalistas fallan consistentemente) → **Fine-Tuning** sobre un modelo base.
- No → Vuelve a Prompt Engineering y afina tu prompt antes de considerar técnicas más complejas.

### Lo que Aprendí Implementando las Cuatro

La lección más valiosa que me dejó la experiencia de operar estas cuatro técnicas en producción se resume en una frase: **empieza siempre por la técnica más simple que podría funcionar**.

La tentación es ir directamente a RAG o fine-tuning porque son más «sofisticados». Pero la sofisticación no correlaciona con la efectividad. En el [Autopilot](/es/posts/ia_agents_part1/), la mayor parte de la calidad del output proviene del Prompt Engineering — system prompts cuidadosamente diseñados, few-shot examples, y Chain-of-thought. RAG añadió valor marginal en el Ops Copilot para búsqueda en el blog. Fine-tuning no fue necesario en ningún caso. Y Tool Calling fue la técnica transformadora en el Radar de Obsolescencia, donde RAG había fracasado.

El orden de evaluación debería ser siempre:
1. **Prompt Engineering** (horas, ~€0)
2. **Tool Calling** si los datos son estructurados (días, ~€0)
3. **RAG** si necesitas acceso a texto propietario (días-semanas, ~€3-50/mes)
4. **Fine-Tuning** solo si las tres anteriores fallan consistentemente (semanas, €50-500+)

Y en la era del [EU AI Act](/es/posts/eu_ai_act/), hay una quinta consideración que no es técnica sino legal: la **trazabilidad**. El Artículo 10 del reglamento exige que los datos de entrenamiento de sistemas de alto riesgo sean «pertinentes, representativos, y en la medida de lo posible, exentos de errores y completos». Esto aplica directamente al fine-tuning: si fine-tuneas un modelo con datos sesgados o incorrectos, y ese modelo toma decisiones en un ámbito regulado, estás expuesto a sanciones. RAG y Tool Calling, al ser transparentes en sus fuentes, ofrecen una trazabilidad que fine-tuning no puede igualar.

Como escribimos en la [Economía Oculta de la IA](/es/posts/economia_oculta_ia/), la Regla del 10x aplica: si una técnica más compleja no te da un resultado **10 veces mejor** que la anterior, probablemente no justifica su coste y complejidad adicional. Empieza simple. Mide. Escala solo cuando los datos lo exijan.

---

#### Fuentes de Interés:
* [**Google Cloud**: Tuning & Fine-tuning with Vertex AI](https://cloud.google.com/vertex-ai/docs/generative-ai/models/tune-models)
* [**Hugging Face**: LoRA — Low-Rank Adaptation of Large Language Models](https://huggingface.co/docs/peft/conceptual_guides/lora)
* [**Pinecone**: RAG vs Fine-Tuning — How to Choose](https://www.pinecone.io/learn/rag-vs-fine-tuning/)
* [**Anthropic**: Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
* [**Datalaria**: RAG en Producción — 7 Antipatrones que Destruyen la Precisión](/es/posts/rag_antipatrones/)
* [**Datalaria**: MCP Protocol — El USB de la IA (Tool Calling Estandarizado)](/es/posts/mcp_protocol/)
* [**Datalaria**: El Radar Agéntico — Tool Calling en Producción](/es/posts/obs_parte5_radar/)
* [**Datalaria**: La Economía Oculta de la IA — Costes Reales de Cada Técnica](/es/posts/economia_oculta_ia/)
* [**Datalaria**: EU AI Act — Artículo 10 y Datos de Entrenamiento](/es/posts/eu_ai_act/)
