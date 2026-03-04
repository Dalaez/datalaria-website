---
title: "Autopilot - Post-Mortem Técnico: Cómo Construí un Ejército de IA con Gemini"
date: 2026-03-04
draft: false
categories: ["Ingeniería", "IA", "DevOps"]
tags: ["devchallenge", "geminireflections", "gemini", "ai", "crewai", "python"]
image: "cover.png"
description: "Un post-mortem técnico sincero sobre el Proyecto Autopilot: cómo utilicé Google Gemini y CrewAI dentro de GitHub Actions para automatizar la distribución de contenido y la ingeniería necesaria para que los LLMs sean deterministas."
summary: "Los ingenieros construyen sistemas complejos pero odian el marketing. Construí un ejército de agentes autónomos con Gemini para distribuir mi contenido. Aquí está el desglose técnico de lo que funcionó, la fricción que encontré y cómo moldea mi hoja de ruta."
---

## 1. El Génesis: La Paradoja del Constructor

En el mundo de los blogs técnicos y la ingeniería, a menudo nos enfrentamos a la "Paradoja del Constructor": podemos pasar 40 horas perfeccionando una arquitectura compleja, definiendo un pipeline de datos S&OP o depurando microservicios, pero parece que no podemos encontrar 15 minutos para empaquetar y promocionar ese trabajo de manera efectiva en las redes sociales.

{{< mermaid >}}
graph TD
    %% Estilos
    classDef human fill:#ff9f43,stroke:#333,stroke-width:2px,color:white;
    classDef code fill:#5f27cd,stroke:#333,stroke-width:2px,color:white;
    classDef ai fill:#0abde3,stroke:#333,stroke-width:2px,color:white;
    classDef social fill:#ee5253,stroke:#333,stroke-width:2px,color:white;

    User("👱‍♂️ Yo / Autor"):::human -->|git push| Git["📂 Repositorio GitHub"]:::code
    Git -->|Trigger| Action["⚙️ GitHub Actions CI/CD"]:::code
    Action -->|Webhooks| Orchestrator{"🧠 Orquestador CrewAI"}:::ai

    Orchestrator -->|Markdown Crudo| Analyst["🕵️ Agente Analista (Gemini Pro)"]:::ai
    Analyst -->|Metadatos JSON| Orchestrator

    Orchestrator -->|Contexto + Ganchos| WriterX["🐦 Redactor Twitter (Gemini Flash)"]:::ai
    Orchestrator -->|Contexto + Claves| WriterLI["💼 Redactor LinkedIn (Gemini Flash)"]:::ai

    WriterX --> X["Twitter API"]:::social
    WriterLI --> LI["LinkedIn API"]:::social
{{< /mermaid >}}

Llegué a ese punto de quiebre con Datalaria. El contenido estaba ahí, la profundidad técnica era sólida, pero la distribución sufría debido a un cuello de botella masivo: yo mismo. Odiaba la carga del marketing.

Así que tomé una decisión estratégica: me despedí del rol de Community Manager. En mi lugar, construí el **Proyecto Autopilot**: un orquestador autónomo impulsado por eventos que se ejecuta completamente dentro de GitHub Actions. Cada vez que hago push de un nuevo archivo Markdown (Hugo) al repositorio, el sistema se despierta, extrae el contexto usando Google Gemini y emplea CrewAI para generar hilos estructurados de Twitter y posts de LinkedIn.

El diagrama conceptual inicial era simple: Entra texto, la IA hace magia, salen posts. La realidad de construir un pipeline determinista con LLMs estocásticos resultó ser un desafío de ingeniería mucho más profundo.

![Conceptual image of the project](cover.png)

## 2. Bajo el Capó: El Motor Gemini

Para construir un pipeline CI/CD que redacte contenido basado en artículos profundamente técnicos (abarcando Ciencia de Datos, Operaciones y procesos S&OP), un simple script de Python analizando strings no iba a ser suficiente. Necesitábamos gran capacidad de razonamiento y una enorme memoria.

Aquí es donde los modelos Gemini de Google se convirtieron en el motor crítico de la arquitectura.

### Ingesta Masiva de Contexto con Gemini Pro
Los posts técnicos, especialmente los que detallan Sales & Operations Planning (S&OP) o higiene de datos con Python, son largos y densos. Contienen lógica de negocio, fragmentos de código y diagramas. Elegí **Gemini Pro** para el *Agente Analista* inicial debido a su enorme ventana de contexto y alta retención. Puede ingerir un tutorial de 3.000 palabras sin "olvidar" la premisa central establecida en el primer párrafo.

### Extracción de Datos Estructurados con Gemini Flash
Mientras que Gemini Pro se encargaba de la comprensión pesada, necesitaba un modelo increíblemente rápido para tareas repetitivas de formateo y extracción de metadatos. **Gemini Flash** se convirtió en la opción predeterminada para estas tareas de disparo rápido.

Sin embargo, los pipelines CI/CD requieren de un determinismo estricto. Un LLM chateando en lenguaje natural rompe la automatización. Tuve que forzar a Gemini a actuar como un estricto procesador de datos para conectar directamente su salida con el siguiente paso de GitHub Action. Aquí hay un fragmento real de cómo obligamos a la API de Gemini a que devolviese un formato JSON estricto:

```python
import google.generativeai as genai
import os
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def extract_metadata(markdown_content):
    # Confiamos en Gemini Flash por su velocidad y formato JSON estricto
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.1,
            "response_mime_type": "application/json",
        }
    )
    
    prompt = f"""
    Analiza el siguiente post técnico en Markdown.
    Devuelve SOLAMENTE un objeto JSON válido que coincida con este esquema:
    {{
        "summary": "string",
        "key_takeaways": ["string", "string"],
        "target_audience": "string",
        "suggested_hashtags": ["string"]
    }}
    
    CONTENT:
    {markdown_content}
    """
    
    response = model.generate_content(prompt)
    return json.loads(response.text)
```

Al configurar `response_mime_type="application/json"`, eliminamos los errores de parseo que plagan tantos flujos de trabajo basados en agentes, permitiendo que el orquestador pase metadatos de manera elegante a los *Agentes Copywriter* especializados de CrewAI.

## 3. La Fricción: Lo Bueno, Lo Malo y Lo Feo

Integrar Inteligencia Artificial generativa en un flujo de trabajo CI/CD rígido rara vez es tan ágil como afirman en los tutoriales y documentación rápida. Aquí tienes la cruda realidad de construir con agentes en producción.

### Lo Bueno: La Velocidad como Característica
En un entorno CI/CD, la latencia se traduce directamente en costes de ejecución ("runner costs"). La velocidad de inferencia de **Gemini 1.5 Flash** es asombrosa. Al derivar las tareas sencillas de formateo y extracción de metadatos a Flash, y reservando **Gemini 1.5 Pro** estrictamente para el razonamiento profundo dentro del rol del Analista de CrewAI, optimizamos tanto la velocidad como los costes. LangChain proporcionó el pegamento, pero Gemini nos dió los caballos de fuerza. Su capacidad nativa y lista para usar para analizar estructuras complejas en Markdown (incluyendo diagramas de Mermaid incrustados y bloques de código) me ahorró días de escribir analizadores frágiles con expresiones regulares.

### Lo Malo: Modelos Estocásticos vs. Pipelines Deterministas
La verdadera fricción en el desarrollo provino de un desajuste de impedancia (Impedance Mismatch). GitHub Actions espera una ejecución determinista paso a paso. Los Modelos de Lenguaje (LLMs) son inherentemente estocásticos.

Incluso con la temperatura establecida en 0.1, un agente de CrewAI podía de vez en cuando alucinar con una etiqueta Markdown estándar inexistente o corromper sutilmente la estructura de los párrafos que requería el post de LinkedIn. Aprendí rápidamente que la Ingeniería de Prompts (Prompt Engineering) no es suficiente; necesitas **Programación Defensiva**. Tuve que envolver diferentes cadenas de ejecución en bloques `Try/Catch` muy estrictos e implementar esquemas Pydantic para poder validar todos y cada uno de los elementos de salida. No confiarse a ciegas a un LLM para llamar a la API de una red social. Era imperativo limitarlo con fuerza, validarlo y sanear el contenido devuelto antes de ejecutar cualquier petición POST del API. En esencia, tuvimos que crear una "puerta de calidad" determinista alrededor de un cerebro no determinista.

### Lo Feo: Bucles de Delegación Infinitos y Runner Timeouts
Los peores momentos -los realmente incómodos- ocurrieron dentro de los ejecutores de GitHub Actions. CrewAI integra un mecanismo de delegación autónoma en el que los agentes pueden transferirse tareas entre sí. En teoría, esto es brillante y de gran ayuda. En la práctica, si no se establecen límites estrictos, es un completo desastre.

Ocasionalmente, el Agente Analista y el Agente Escritor se atascaban en un "bucle de reflexión" infinito y muy educado para debatir qué enfoque era más apropiado para resumir un párrafo técnico. 

Puesto que GitHub Actions cobra por minutos consumidos, estos bucles silenciosos devoraban todo el tiempo del "runner" hasta que el propio sistema detenía el pipeline a la fuerza, mostrando un frustrante `Error 143 (SIGTERM)`. Solucionar este desafío exigió realizar una intervención profunda: desactivar la delegación en caso de que no fuera estrictamente necesaria en la configuración de CrewAI, aplicar tiempos de espera límite (`max_execution_time`) más acotados y por agente, y diseñar sistemas de seguridad estrictos (fail-safes) con los que el pipeline se anulara limpiamente en lugar de mantenerse inmovilizado y prolongar dicho estado de manera indefinida.

## 4. La Lección: Ingeniería de Operaciones

Este proyecto cambió fundamentalmente mi mentalidad. Integrar IA en flujos de trabajo no es un problema de Prompt Engineering; **es un problema de Ingeniería de Sistemas y CI/CD.**

A través de este experimento extremo de "dogfooding", aprendí a tratar las tuberías de contenido y datos con el mismo rigor exacto que aplico a una Cadena de Suministro física. Un Agente IA es básicamente un nodo altamente capaz pero ocasionalmente impredecible en una red de operaciones. Tienes que construir tolerancia a fallos, contratos claros (esquemas JSON) y controles de calidad a su alrededor.

## 5. Mirando al Futuro: El Pivote S&OP

El Proyecto Autopilot resolvió mi problema de distribución. Pero automatizar las redes sociales era simplemente el campo de pruebas.

Ahora que Gemini y CrewAI han demostrado que pueden ingerir de manera fiable texto complejo y no estructurado, extraer el significado y orquestar acciones, el siguiente paso en la hoja de ruta de Datalaria es mucho más ambicioso. Voy a tomar esta misma arquitectura multi-agente y a pivotarla hacia las operaciones empresariales.

En lugar de leer Markdown para escribir tweets, la próxima iteración de estos agentes impulsados por Gemini ingerirá datos fragmentados de ERPs, correos electrónicos y volcados de Excel para automatizar la higiene de datos y resumir riesgos de negocio para las reuniones de **S&OP (Sales & Operations Planning)**. Estamos pasando de resolver la Paradoja del Constructor a optimizar cadenas de suministro en el mundo real.

El ejército de IA está construido. Ahora es el momento de ponerlo a trabajar de verdad.
