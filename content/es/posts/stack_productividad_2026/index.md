---
title: "El Stack de Productividad de un Ingeniero en 2026: Las Herramientas que Uso Cada Día"
date: 2026-08-01
draft: false
categories: ["Ingeniería"]
tags: ["productividad", "herramientas", "stack", "ingeniero", "workflow", "python", "supabase", "github actions", "crewai", "hugo"]
description: "El stack real de herramientas de un ingeniero de datos en 2026: desde Gemini Deep Research hasta GitHub Actions, pasando por Python, Supabase, CrewAI y Hugo. Sin patrocinios, sin afiliados, sin filtros. Cada herramienta explicada con el post donde la uso."
summary: "Después de más de 60 artículos, 9 series técnicas y 4 aplicaciones en producción, este es el stack real que uso todos los días. Sin patrocinios, sin afiliados, sin filtros. 10 herramientas organizadas por fase del workflow, lo que probé y descarté, y el coste total: menos de 5€ al mes."
social_text: "Después de +60 artículos, 9 series técnicas y 4 apps en producción, este es mi stack REAL de productividad como ingeniero en 2026. Sin patrocinios, sin filtros. Coste total: <5€/mes ⚡🛠️🧠 #Productividad #Ingeniería #Stack #Herramientas"
image: cover.jpg
weight: 10
authorAvatar: datalaria-logo.png
---

Después de más de 60 artículos, 9 series técnicas, 4 aplicaciones en producción y un blog bilingüe que genera contenido semanal, me hacen la misma pregunta una y otra vez: **«¿Qué herramientas usas?»**. No qué herramientas recomiendo, no qué herramientas están de moda, sino cuáles uso yo realmente, todos los días, para construir lo que ves en Datalaria.

Este artículo es la respuesta. Sin patrocinios, sin enlaces de afiliados, sin filtros. Cada herramienta que aparece aquí la he testeado en producción, he pagado (o no) por ella con mi propio dinero, y he documentado su uso en al menos un post de este blog. Si no la he usado en un proyecto real, no está en esta lista.

### El Workflow: 10 Fases, 10 Herramientas

La clave de mi productividad no está en las herramientas individuales sino en cómo encajan unas con otras. Cada fase del workflow alimenta a la siguiente, y la salida de una herramienta es la entrada de otra. No hay silos; hay un pipeline.

![El workflow completo: de la idea al despliegue](workflow.jpg)

| Fase | Herramienta | Por qué esta y no otra |
| :--- | :--- | :--- |
| 🧠 **Pensar** | Gemini Deep Research | Investigación exhaustiva en minutos |
| ✍️ **Escribir** | Hugo + VS Code + Markdown | Control total, Git-native, velocidad |
| 💻 **Codificar** | Python + Pandas + FastAPI | El tridente de la ingeniería de datos |
| 🗄️ **Almacenar** | Supabase (PostgreSQL) | BaaS gratuito, RLS, APIs REST automáticas |
| 🤖 **Orquestar IA** | CrewAI + Gemini 2.5 | Agentes autónomos con Tool Calling |
| ⚙️ **Automatizar** | GitHub Actions | CI/CD gratuito, evento-driven |
| 🚀 **Desplegar** | Netlify | Deploy from Git en segundos |
| 📧 **Comunicar** | Brevo (Newsletter) | Email marketing gratuito, API, segmentación |
| 📊 **Visualizar** | Chart.js + Vanilla JS | Ligero, sin frameworks pesados, interactivo |
| 📚 **Aprender** | NotebookLM | Transforma cualquier fuente en recursos de estudio |

### 🧠 Pensar: Gemini Deep Research

Antes de escribir una sola línea, investigo. Y aquí es donde la IA generativa ha cambiado radicalmente mi workflow. **Gemini Deep Research** (dentro de Gemini Advanced) es la herramienta que uso para hacer investigación exhaustiva antes de cada artículo y cada proyecto técnico.

Cuando estaba preparando el artículo sobre [Thomas Bayes](/es/posts/thomas_bayes/), necesitaba verificar fechas, publicaciones, contexto histórico de la Royal Society, y la conexión matemática precisa entre el teorema de Bayes y Facebook Prophet. Lo que antes habría requerido horas de navegación por Wikipedia, Stanford Encyclopedia of Philosophy y papers académicos, Gemini Deep Research lo compiló en un informe estructurado en **menos de 10 minutos**, con citas y fuentes verificables.

La clave: **no lo uso para escribir; lo uso para investigar**. El texto final siempre es mío. Gemini me da la materia prima; yo construyo la narrativa. Documenté este enfoque en detalle en [IA en Educación con Deep Research](/es/posts/ia-educacion-deep_research/).

### ✍️ Escribir: Hugo + VS Code + Markdown

Todo lo que ves en Datalaria está escrito en **Markdown puro**, editado en **VS Code**, compilado con **Hugo** y versionado en **Git**. Cero WordPress, cero CMS visual, cero drag-and-drop.

¿Por qué esta decisión aparentemente masoquista? Porque un blog en Hugo es **código**. Puedo hacer `git diff` para ver qué cambié en un artículo. Puedo hacer `git blame` para saber cuándo lo cambié. Puedo hacer un fork, crear una rama, experimentar con una estructura nueva, y hacer merge solo si funciona. Y puedo automatizar el despliegue con un `git push`. Documenté todas estas decisiones arquitectónicas en [Construyendo Datalaria](/es/posts/datalaria-blog/).

Hugo compila las más de 700 páginas de este blog (español + inglés) en **menos de 4 minutos**. Un CMS tradicional tardaría varios segundos solo en renderizar una página individual. Cuando iteras rápido, la velocidad de compilación no es un lujo; es una necesidad.

### 💻 Codificar: Python + Pandas + FastAPI

El tridente que uso para absolutamente todo lo que implique datos:

* **Python** como lenguaje base. Sin discusión. El ecosistema de librerías para ingeniería de datos, ML y automatización no tiene rival.
* **Pandas** para manipulación, limpieza y transformación de datos. Cada pipeline de la [serie S&OP](/es/posts/sop-ingenieria-parte2-prediccion/) — desde la ingesta de datos de venta hasta la generación de forecasts con Prophet — pasa por Pandas.
* **FastAPI** cuando necesito exponer un servicio como API REST. Lo usamos en la [Parte 6 de la serie de Observabilidad](/es/posts/obs_parte6_fastapi/) para construir el backend del radar de obsolescencia, y en la [app de OpenWeather](/es/posts/app-openweather_part1_backend/) como backend de predicción meteorológica.

### 🗄️ Almacenar: Supabase (PostgreSQL)

**Supabase** es PostgreSQL gestionado con superpoderes: autenticación, Row Level Security (RLS), APIs REST automáticas generadas a partir del esquema de la base de datos, y un tier gratuito que cubre el 95% de mis necesidades de desarrollo y prototipado.

Lo uso como backend de datos en la [serie de Observabilidad](/es/posts/obs_parte4_ingesta/) (almacenando el catálogo de componentes, alertas de obsolescencia y grafos BOM), en los pipelines de [S&OP](/es/posts/sop-ingenieria-parte3-optimizacion/) (datos de demanda, forecasts, planes de producción), y en el [juego Snake con leaderboard global](/es/posts/game_snake/).

¿Por qué Supabase y no Firebase? Porque Supabase es **PostgreSQL real**. Puedo escribir SQL nativo, crear vistas materializadas, usar JOINs complejos y migrar a cualquier otro PostgreSQL gestionado (RDS, Cloud SQL) sin cambiar una línea de código. Firebase te atrapa en su ecosistema propietario; Supabase te da la puerta de salida incluida.

### 🤖 Orquestar IA: CrewAI + Gemini 2.5

Cuando necesito que la IA no solo responda preguntas sino que **ejecute tareas complejas de múltiples pasos**, uso **CrewAI** como framework de orquestación de agentes. Cada agente tiene un rol, un objetivo, herramientas Python específicas (decoradas con `@tool`), y la capacidad de coordinarse con otros agentes.

Gemini 2.5 Pro/Flash es el LLM que alimenta a los agentes. La combinación CrewAI + Gemini + Tool Calling es la arquitectura que documenta toda la [serie Autopilot de 9 partes](/es/posts/ia_agents_part1/), desde el generador automático de contenido hasta el Ops Copilot.

Como analizamos en el [artículo de RAG vs. Tool Calling](/es/posts/rag_antipatrones/), la clave está en separar el «cerebro semántico» (el LLM entiende el contexto) del «músculo determinista» (las herramientas Python ejecutan las operaciones de precisión). El LLM piensa; las herramientas hacen.

### ⚙️ Automatizar: GitHub Actions

Cada pipeline de CI/CD de Datalaria corre en **GitHub Actions**. Es gratuito para repositorios públicos, evento-driven (se dispara con un push, un cron, un webhook), y lo suficientemente flexible para orquestar desde la compilación de Hugo hasta la ejecución de pipelines de CrewAI.

En la [Parte 5 del Autopilot](/es/posts/ia_agents_part5/), documentamos cómo configurar un workflow de GitHub Actions que ejecuta el pipeline agéntico completo cada semana: genera contenido con CrewAI, crea los archivos Markdown, hace commit, push, y despliega automáticamente en Netlify. Todo sin intervención humana.

### 🚀 Desplegar: Netlify

**Netlify** despliega Datalaria directamente desde el repositorio de GitHub. Cada `git push` a la rama `main` dispara un build de Hugo y publica el sitio en segundos. Funcionalidades como Netlify Functions (serverless), redirects, y headers personalizados cubren todo lo que necesito sin gestionar servidores.

Lo documentamos en la [Parte 2 de la app OpenWeather](/es/posts/app_openweather_part2_frontend/) como plataforma de despliegue para aplicaciones frontend con backend serverless.

### 📧 Comunicar: Brevo (Newsletter)

La newsletter de Datalaria usa **Brevo** (antes Sendinblue). Tier gratuito generoso (300 emails/día), API REST para automatización, segmentación de audiencia, y editor de templates.

En la [Parte 6 del Autopilot](/es/posts/ia_agents_part6/), documentamos cómo el pipeline de CrewAI genera el contenido del email, construye el HTML, y lo envía automáticamente vía la API de Brevo — cerrando el ciclo completo de generación → publicación → distribución sin intervención manual.

### 📊 Visualizar: Chart.js + Vanilla JS

Cuando necesito gráficos interactivos en las apps web, uso **Chart.js** con **JavaScript vanilla**. Sin React, sin Vue, sin frameworks pesados. La filosofía es intencional: cada librería que añades es una dependencia que mantener, una superficie de ataque que proteger, y un bundle que inflar.

La [Parte 4 de la app OpenWeather](/es/posts/app_openweather_part4_extras_ux/) y las [Visualizaciones Básicas](/es/posts/Visualizaciones-basicas/) demuestran que Chart.js + CSS puro produce dashboards interactivos de calidad profesional sin necesidad de un framework de 200KB.

### 📚 Aprender: NotebookLM

**NotebookLM** de Google es mi herramienta de aprendizaje acelerado. Subo documentación técnica, papers académicos o transcripciones de conferencias, y NotebookLM genera resúmenes, preguntas de estudio, y — lo más transformador — **podcasts de audio** donde dos hosts discuten el material como si fuera una conversación natural.

Lo documenté en profundidad en [NotebookLM + SQL](/es/posts/notebooklm-sql/), mostrando cómo transformar la documentación de PostgreSQL en recursos de estudio interactivos.

### Lo que Probé y Descarté

No todo lo que pruebas sobrevive al contacto con la producción. Estas son las herramientas que evalué y descarté, con las razones:

* **WordPress**: Lo usé durante años. Lo abandoné por la lentitud, los plugins, las actualizaciones de seguridad constantes, y la imposibilidad de versionar el contenido con Git. Hugo es 100x más rápido y todo es código.
* **LangChain**: Framework de orquestación de LLMs que probé antes de CrewAI. Demasiada abstracción, cadenas de herencia profundas y difíciles de depurar, y una API que cambiaba con cada versión minor. CrewAI es más simple, más explícito, y más estable.
* **Streamlit**: Excelente para prototipos rápidos de dashboards de datos. Pero cuando necesitas control sobre el frontend (CSS, animaciones, UX), Streamlit se convierte en una camisa de fuerza. Para producción, prefiero FastAPI + HTML/CSS/JS, donde tengo control total.
* **MongoDB**: Lo probé como alternativa a PostgreSQL para datos semi-estructurados. Pero la falta de JOINs y la imposibilidad de hacer queries relacionales complejas lo descartaron rápidamente para mis casos de uso industriales (grafos BOM, cruce de tablas de demanda).

### El Coste Total del Stack: La Economía Real

Aquí es donde la [Economía Oculta de la IA](/es/posts/economia_oculta_ia/) cobra relevancia directa. ¿Cuánto cuesta operar todo este stack?

| Herramienta | Coste mensual | Notas |
| :--- | :--- | :--- |
| Gemini Advanced | ~€22/mes | Incluye Deep Research, 2.5 Pro, etc. |
| Hugo | €0 | Open source |
| VS Code | €0 | Open source |
| Python + librerías | €0 | Open source |
| Supabase | €0 | Tier gratuito |
| CrewAI | €0 | Open source |
| GitHub Actions | €0 | Gratuito para repos públicos |
| Netlify | €0 | Tier gratuito |
| Brevo | €0 | Tier gratuito (300 emails/día) |
| Chart.js | €0 | Open source |
| NotebookLM | €0 | Incluido en Gemini Advanced |
| **TOTAL** | **~€22/mes** | |

Prácticamente todo el stack es gratuito o open source. El único coste recurrente es la suscripción a Gemini Advanced, que cubre tanto Deep Research como los modelos que alimentan los agentes de CrewAI. Incluso si contamos los costes de API de Gemini para las ejecuciones del pipeline Autopilot, el total rara vez supera los **€5 adicionales al mes**.

Compara esto con el coste de un stack «enterprise»: un CMS con licencia (€50-500/mes), una herramienta de email marketing premium (€30-200/mes), un servicio de hosting gestionado (€20-100/mes), y una plataforma de BI (€50-300/mes). El stack open source no es solo más barato; es **más potente**, porque cada herramienta es una caja que puedes abrir, inspeccionar, modificar y aprender de ella.

### La Filosofía: Aprendizaje > Comodidad

Si hay un hilo conductor en todas las decisiones de este stack, es este: **priorizo aprender sobre comodidad**. Hugo es más difícil que WordPress, pero aprendí generación de sitios estáticos, Go templates y CI/CD. FastAPI es más trabajo que Streamlit, pero aprendí diseño de APIs REST, async/await y OpenAPI. Supabase con SQL nativo es más verboso que Firebase, pero aprendí PostgreSQL real, RLS y migraciones.

Cada herramienta del stack no es solo una herramienta; es un **curso**. Y los 60+ artículos de este blog son los apuntes de esos cursos, compartidos en abierto para que cualquiera pueda recorrer el mismo camino.

Como diría [Deming](/es/posts/deming/): *«El aprendizaje no es obligatorio. Tampoco lo es la supervivencia»*. En un mundo donde la IA redefine las reglas del juego cada trimestre, el stack que uses importa menos que **tu capacidad de aprender el siguiente stack**. Y esa capacidad se construye eligiendo herramientas que te obliguen a entender qué hay debajo del capó.

---

#### Fuentes de Interés:
* [**Hugo**: Generador de Sitios Estáticos — Documentación Oficial](https://gohugo.io/)
* [**Supabase**: Backend as a Service Open Source](https://supabase.com/)
* [**CrewAI**: Framework de Agentes de IA](https://www.crewai.com/)
* [**FastAPI**: Framework Web Moderno para Python](https://fastapi.tiangolo.com/)
* [**Chart.js**: Visualizaciones JavaScript Open Source](https://www.chartjs.org/)
* [**Brevo**: Plataforma de Email Marketing](https://www.brevo.com/)
* [**Datalaria**: Construyendo el Blog — Decisiones de Arquitectura](/es/posts/datalaria-blog/)
* [**Datalaria**: La Economía Oculta de la IA — El Coste Real del Stack](/es/posts/economia_oculta_ia/)
* [**Datalaria**: Serie Autopilot — 9 Partes de Ingeniería Agéntica](/es/posts/ia_agents_part1/)
