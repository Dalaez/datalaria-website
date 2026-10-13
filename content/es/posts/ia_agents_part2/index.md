---
title: "Autopilot - El Cerebro: Configurando Gemini y CrewAI para leer mi blog"
date: 2025-12-31
draft: false
category: "Proyectos Tecnológicos"
categories: ["Ingeniería de Software", "IA Generativa", "Python"]
tags: ["CrewAI", "Gemini API", "Backend", "Clean Code", "Automatización"]
image: "cover.png"
description: "Segundo capítulo de Proyecto Autopilot. Abrimos el IDE para conectar Python con Gemini Flash y crear nuestro primer Agente Analista capaz de entender código Markdown."
summary: "Un script que lee archivos es fácil. Un script que 'entiende' la tecnología es otra historia. En este post configuramos el entorno Python, solucionamos los errores de integración de CrewAI y logramos que Gemini Flash extraiga 'oro puro' de nuestros posts en Markdown."
---

En el [Post 1: La Estrategia]({{< ref "ia_agents_part1" >}}), prometí que no usaría herramientas de terceros para gestionar mis redes sociales. Prometí construir un "ejército de agentes".

Hoy, dejamos el PowerPoint y abrimos el IDE. Vamos a construir el **Cerebro** del sistema.

El objetivo de hoy es técnico y concreto: crear un script en Python que sea capaz de leer un archivo `.md` de mi repositorio local, "leerlo" como lo haría un ingeniero senior, y devolverme un análisis estructurado en JSON.

![Imagen conceptual del proyecto - El cerebro](autopilot_brain.png)

## El Stack Tecnológico: Velocidad sobre Potencia Bruta

Para esta tarea, he tomado dos decisiones de arquitectura:

1.  **El Orquestador: CrewAI.** Necesito algo que maneje "Agentes" y "Tareas", no solo cadenas de texto. CrewAI me permite definir *roles* (quién eres) y *goals* (qué quieres), lo cual es vital para los siguientes pasos.
2.  **El Modelo: Google Gemini Flash.** Al principio intenté usar el modelo más potente (Pro), pero me di cuenta de un error de principiante: para tareas de lectura masiva y extracción de datos, no necesitas al filósofo, necesitas al bibliotecario rápido. Flash es mucho más rápido, barato (gratis en el tier actual) y tiene una ventana de contexto gigantesca.

## Paso 1: Higiene del Repositorio (Clean Monorepo)

Antes de escribir código, hay que organizar la casa. Mi blog está hecho en Hugo, y no quiero ensuciar la carpeta del sitio web con scripts de Python.

He optado por una estructura de "Monorepo Limpio". He creado una carpeta `autopilot` en la raíz del proyecto que actúa como un módulo independiente.

```text
datalaria/
├── content/           <-- Mis posts en Markdown (Hugo)
├── themes/
├── autopilot/         <-- EL NUEVO CEREBRO 🧠
│   ├── .env           <-- ¡OJO! Aquí van las claves (Ignorado por Git)
│   ├── main.py        <-- El punto de entrada
│   └── src/           <-- Lógica de Agentes y Tareas
└── .gitignore         <-- Configurado para proteger mis secretos
```

> **Lección aprendida:** Configura tu `.gitignore` antes de hacer el primer commit. Si subes tu API Key a GitHub por error, los bots tardarán segundos en encontrarla o peor aún, puede que te encuentres con costes indeseados de otros usuarios que hayan encontrado tu API Key.

## Paso 2: El Código (Manos a la obra)

El corazón de este sistema no es `main.py`, sino cómo definimos al agente. Usando la librería `crewai` y `langchain_google_genai`, definí a mi primer empleado digital: **"El Analista"**.

### El Problema de la "Obsesión con OpenAI"

Aquí me topé con el primer muro. CrewAI está diseñado por defecto para buscar una API Key de OpenAI (GPT-4). Aunque yo configuré Gemini, el script fallaba con el error:

`ValueError: OPENAI_API_KEY is required`

La solución fue forzar explícitamente el LLM (Large Language Model) dentro de la definición del agente. Así se ve el código en `src/agents.py`:

```python
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

class BlogAgents:
    def __init__(self):
        # Configuramos Gemini Flash explícitamente
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            verbose=True,
            temperature=0.2, # Baja temperatura = Más analítico, menos creativo
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def analyst_agent(self):
        return Agent(
            role='Senior Tech Editor & Data Analyst',
            goal='Analyze raw content to extract structured insights',
            backstory='You are a veteran tech editor...',
            allow_delegation=False,
            llm=self.llm  # <--- ESTA LÍNEA ES CRÍTICA. Si la quitas, buscará OpenAI.
        )
```

## Paso 3: El Prompt de Ingeniería (JSON Mode)

Para que esto sea útil, el agente no puede simplemente "charlar" sobre el artículo. Necesito datos que pueda procesar computacionalmente después.

En `src/tasks.py`, definí la tarea con instrucciones estrictas de salida. No usé el "JSON Mode" nativo de la API (que a veces es complejo de configurar), sino que confié en la capacidad de instrucción del modelo:

> "OUTPUT FORMAT: Return ONLY a valid JSON object with keys: summary, target_audience, tech_stack, key_takeaways, marketing_hooks."

## El Resultado: ¡Funciona!

Ejecuté el script contra uno de mis artículos técnicos más densos (sobre procesos S&OP). Tenía miedo de que el modelo alucinara o se perdiera en el texto.

El resultado en la terminal fue este JSON limpio:

```json
{
  "summary": "This post demonstrates how Generative AI bridges the gap between complex business narratives and technical execution...",
  "target_audience": "Business Analysts, Industrial Engineers, Operations Managers...",
  "tech_stack": [
    "Generative AI (LLMs)",
    "BPMN 2.0",
    "Mermaid.js",
    "Gemini API"
  ],
  "marketing_hooks": [
    "Stop drowning in dense business requirements! 🚀 Learn how to use AI to turn messy narratives into professional BPMN diagrams...",
    "Documentation as Code is here. 💻 See how LLMs can generate Mermaid.js diagrams..."
  ]
}
```

Es impresionante. El modelo no solo resumió el texto, sino que entendió el **contexto profundo**: identificó que el artículo hablaba de "Mermaid.js" y "BPMN" y generó ganchos de marketing ("marketing_hooks") que realmente suenan a algo que yo escribiría en Twitter.

## ¿Qué sigue?

Ya tenemos el **Cerebro** (`autopilot`) capaz de leer y entender lo que escribo en `content`. Los datos están estructurados y listos.

Pero un JSON no consigue likes.

En el próximo post, vamos a construir a **Los Creativos**. Usaremos estos datos para alimentar a dos nuevos agentes con personalidades opuestas: un experto en viralidad para Twitter y un estratega corporativo para LinkedIn. Y veremos cómo el *Prompt Engineering* puede cambiar drásticamente el tono de una IA.

👉 **Código Fuente:** Puedes ver el código de este módulo en la carpeta `/autopilot` del [repositorio de Datalaria en GitHub](https://github.com/Dalaez/datalaria-website).