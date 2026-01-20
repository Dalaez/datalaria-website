---
title: "Proyecto Autopilot: Por qué me despedí como Community Manager para construir un Ejército de agentes de IA"
date: 2025-12-27
draft: false
categories: ["Automatización", "Inteligencia Artificial", "DevOps"]
tags: ["Agentes", "Gemini", "CrewAI", "GitHub Actions", "Python", "Dogfooding"]
image: "cover.png"
description: "Expermentar con la IA y las nuevas tecnologías es mi pasión; la distribución de estos contenidos no tanto. En esta serie, documento cómo estoy construyendo un equipo automatizado de Agentes IA para mis posts y gestionar su divulgación a través de mis redes sociales."
summary: "La 'Meseta de Tráfico Orgánico' es real. Para superarla sin perder el foco en la ingeniería, lanzo un experimento extremo de 'dogfooding': automatizar la distribución de Datalaria usando Gemini, CrewAI y GitHub Actions. Este es el Plan Maestro."
---

En el mundo de los blogs técnicos y la ingeniería, a menudo nos enfrentamos a la "Paradoja del Constructor". Podemos pasar 40 horas perfeccionando un tema concreto, definiendo una arquitectura o depurando pequeños detalles técnicos. Sin embargo, no se encuentran 15 minutos para promocionar el trabajo realizado de manera efectiva en redes sociales.

He llegado a ese punto con **Datalaria**. El contenido está ahí, la arquitectura está optimizada, pero la distribución sufre por culpa del cuello de botella principal... bueno, yo.

Hoy tomo una decisión estratégica. Me estoy "despidiendo" del rol de Community Manager, el cual realmente nunca llegué a ejercer. En mi lugar, no voy a contratar una agencia; voy a construir una y experimentar con los, tan de moda, "agentes IA".

Bienvenido al **Proyecto Autopilot**: una serie de 5 partes donde construiremos, en vivo y en público, un sistema autónomo de Agentes de IA que lee este blog, lo analiza al detalle y, de manera autónoma, preparan el contenido para su promoción y lo distribuyen en las redes sociales mientras por mi parte estoy a otros menesteres.

## La Estrategia: Dogfooding Extremo

El concepto es simple pero técnicamente ambicioso. Vamos a ejecutar una estrategia de "dogfooding" (comer nuestra propia comida). En lugar de usar herramientas de terceros como [Buffer](https://buffer.com/free-trial/programador-de-contenido-de-redes-sociales?utm_campaign=paid&utm_source=adwords&utm_medium=ppc&utm_content=164769329173&utm_term=manejo%20de%20redes%20sociales&gad_source=1&gad_campaignid=21469228239&gclid=CjwKCAiAu67KBhAkEiwAY0jAlZff6fydtLMfrj_lPM2hoWC0GTJPRnjyCp-VQB1A30qNmyirNvdKpBoC1aYQAvD_BwE) o [Hootsuite](https://hootsuite.com/), construiremos un motor de distribución personalizado utilizando las mismas tecnologías sobre las que escribimos: **IA Generativa** y **Pipelines CI/CD**.

El "Gran Objetivo" es transformar el proceso de blogging. Actualmente, "publicar" significa hacer un push de un archivo Markdown a GitHub. En el futuro, ese `git push` desencadenará una reacción en cadena donde agentes inteligentes analizan, crean y distribuyen contenido.

![Imagen conceptual del proyecto](autopilot.png)

## La Arquitectura: Conoce al Equipo

Para resolver esto, un simple script de Python no es suficiente. Necesitamos capacidades de razonamiento. Necesitamos un sistema que entienda contexto, tono y audiencia.

Estamos diseñando una arquitectura orientada a eventos alojada completamente dentro de **GitHub Actions**, utilizando **Google Gemini** como cerebro y **CrewAI** como orquestador.

Aquí está el flujo conceptual del sistema que vamos a construir:

{{< mermaid >}}
graph TD
    %% Estilos
    classDef human fill:#ff9f43,stroke:#333,stroke-width:2px,color:white;
    classDef code fill:#5f27cd,stroke:#333,stroke-width:2px,color:white;
    classDef ai fill:#0abde3,stroke:#333,stroke-width:2px,color:white;
    classDef social fill:#ee5253,stroke:#333,stroke-width:2px,color:white;

    %% Nodos
    User("👱‍♂️ Yo / Autor"):::human
    Git["📂 Repositorio GitHub <br/> Push nuevo archivo .md"]:::code
    Action["⚙️ GitHub Actions <br/> Runner CI/CD"]:::code
    
    %% FIX: Cambiada dirección a LR para evitar solapamiento
    subgraph TeamAI ["🤖 El Equipo (CrewAI + Gemini)<br/><br/>"]
        direction TB        
        Orchestrator{"🧠 Orquestador"}:::ai
        Analyst["🕵️ Agente 1: El Analista <br/> (Extrae Metadata y Ganchos)"]:::ai
        WriterX["🐦 Agente 2: Redactor Twitter <br/> (Contenido Viral/Corto)"]:::ai
        WriterLI["💼 Agente 3: Redactor LinkedIn <br/> (Tono Profesional)"]:::ai
    end

    Review("👀 Revisión Humana <br/> Pull Request / Borrador"):::human
    
    X["Twitter / X API"]:::social
    LI["LinkedIn API"]:::social

    %% Conexiones
    User -->|git push| Git
    Git -->|Trigger| Action
    Action -->|Inicia Proceso| Orchestrator
    
    Orchestrator -->|Texto Crudo| Analyst
    Analyst -->|JSON| Orchestrator
    
    Orchestrator -->|Contexto + Ganchos| WriterX
    Orchestrator -->|Contexto + Claves| WriterLI
    
    WriterX -->|Borrador| Review
    WriterLI -->|Borrador| Review
    
    Review -->|Aprobar| X
    Review -->|Aprobar| LI
{{< /mermaid >}}

### Decisiones de Arquitectura

1.  **El Trigger (GitHub Actions):** ¿Por qué pagar por un servidor? El blog es estático (Hugo), así que la automatización debe ser efímera. Solo se ejecuta cuando publico.
2.  **El Cerebro (Gemini 3 Pro):** Elegimos este modelo por su gran ventana de contexto. Necesita leer tutoriales técnicos completos sin "olvidar" el principio.
3.  **El Orquestador (CrewAI):** Esto nos permite asignar *personas* o roles específicos. No queremos una IA genérica; queremos un "Experto en Twitter Cínico" y un "Estratega Corporativo" trabajando en paralelo.

## Prueba de Concepto: ¿Puede la IA entender mi código?

Antes de escribir una sola línea del pipeline final, necesitaba validar la hipótesis central: *¿Puede Gemini entender realmente la estructura de mis posts en Hugo?*

Ejecuté una prueba usando un prompt de sistema diseñado para actuar como un "Editor Técnico Senior". El objetivo no era escribir texto, sino extraer datos estructurados (JSON) de mis archivos Markdown crudos.

El resultado fue prometedor:

![Prueba de Concepto Análisis Gemini](ia_agents_proof_concept.png)

El modelo identificó correctamente el **Stack Tecnológico**, generó un resumen, y lo más importante, extrajo "Ángulos Provocativos" para marketing. Este JSON estructurado es lo que alimentará a nuestros agentes redactores en la siguiente fase.

## La Hoja de Ruta (Roadmap)

Esta serie es el núcleo de la estrategia de contenido de Datalaria para los próximos meses. Documentaremos el dolor, los bugs y las victorias en tiempo real.

* **Post 1: La Estrategia (Estás aquí).** El Plan Maestro y la Arquitectura.
* **Post 2: El Cerebro.** Configurando Gemini Pro y LangChain/CrewAI para leer y "entender" Markdown.
* **Post 3: Los Creativos.** Ingeniería de Prompts para crear personalidades distintas para LinkedIn vs. Twitter.
* **Post 4: La Pesadilla de las APIs.** Una mirada honesta a los desafíos de conectar con APIs de Redes Sociales.
* **Post 5: El Orquestador Final.** Integración CI/CD con GitHub Actions para un despliegue totalmente automatizado.

## Conclusión: De Contenido a Producto

Mediante este experimento vamos a tratar de "montar" y "probar" mi primer equipo virtual de trabajo. Para ello, vamos a utilizar la distribución de contenido en redes sociales como un producto en sí mismo que sean capaces de entender, explotar y promover estos agentes.

Esta automatización con estos agentes aspira a probar que:

1.  **La consistencia es clave:** Un bot no se cansa ni se olvida de publicar.
2.  **El contexto es el Rey:** Una IA genérica es aburrida; Agentes especializados con roles claros aportan valor.
3.  **El código es apalancamiento:** Estos agentes, una vez montados, funcionarán para siempre.

Si este experimento falla, documentaré el fallo. Si funciona, **Datalaria** pasará a ser un blog promocionado por sí mismo mediante IA mientras su autor está ocupado escribiendo el siguiente post :).

-----

*¿Listo para ver el código? En el próximo post, abriremos nuestro IDE para configurar el "Agente Lector" usando Python y la API de Gemini.*