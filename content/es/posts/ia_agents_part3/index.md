---
title: "Autopilot - Los Creativos: Cómo programé a una IA para que fuera cínica en Twitter y corporativa en LinkedIn"
date: 2026-01-03
draft: false
category: "Proyectos Tecnológicos"
categories: ["IA Generativa", "Prompt Engineering", "Python"]
tags: ["CrewAI", "Personalidad IA", "Automatización", "Marketing", "Storytelling"]
image: "cover.png"
description: "Tercer capítulo de Proyecto Autopilot. Transformamos datos fríos en historias virales creando dos agentes con personalidades opuestas: un influencer cínico y un líder corporativo."
summary: "Tener los datos no es suficiente; nadie da like a un JSON. En este post, diseñamos la personalidad de nuestros Agentes Redactores, enseñamos a Gemini a escribir 'Broetry' para LinkedIn y 'Shitposting' para Twitter, y escalamos la arquitectura para publicar en español e inglés simultáneamente."
---

En el [Post 2: El Cerebro]({{< ref "ia_agents_part2" >}}), logramos algo técnicamente importante: un script de Python capaz de leer mis artículos técnicos y extraer su esencia en un JSON estructurado.

Pero tengo un problema. **Si publico un JSON en Twitter, nadie lo va a leer.**

Los datos son fríos. Las redes sociales son emocionales. Para que este sistema de "Autopilot" funcione, no necesito más analistas; necesito **creativos**. Necesito redactores que entiendan la psicología de cada plataforma.

Hoy, vamos a darle **alma** a la máquina. Vamos a crear a **"Los Creativos"**.

![Imagen conceptual del proyecto - Los Creativos](autopilot_creative.png)

## La Teoría del Rol (El Método Stanislavski para IA)

Los Grandes Modelos de Lenguaje (LLMs) como Gemini son, en esencia, actores de método. Si les pides "escribe un tweet", te darán un tweet genérico, aburrido y lleno de hashtags como #Tecnología #Innovación.

Pero si les das un **rol**, una historia de fondo (*backstory*) y una motivación, su comportamiento cambia radicalmente. En ingeniería de prompts, esto es la diferencia entre un chatbot y un agente.

Para Datalaria, no quiero una voz genérica. Quiero cubrir dos extremos del espectro:
1.  **El Caos (Twitter/X):** Breve, directo, un poco cínico y alérgico a lo corporativo.
2.  **El Orden (LinkedIn):** Profesional, inspirador, enfocado en el valor de negocio.

## Diseñando las Personalidades (El Código)

Usando **CrewAI**, definir estas personalidades es tan sencillo (y complejo) como escribir una biografía. Aquí está el código real de `src/agents.py` que define a mis dos nuevos empleados digitales.

### 1. El Influencer Tech (Twitter)
Le he pedido explícitamente que odie la jerga corporativa y use minúsculas por estética.

```python
def twitter_writer_agent(self):
    return Agent(
        role="Tech Twitter Influencer",
        goal="Convert structured insights into a viral Twitter thread",
        backstory="""You are a tech influencer who hates corporate jargon. 
        You write in a punchy, provocative style. 
        You use lowercase often for aesthetic. 
        You focus on the 'Marketing Hooks' from the input. 
        You NEVER use hashtags like #Technology, only niche ones.""",
        llm=self.llm
    )
```

### 2. El Líder de Pensamiento (LinkedIn)
Aquí buscamos el estilo "Broetry" (frases cortas con mucho espacio en blanco) que funciona en LinkedIn.

```python
def linkedin_writer_agent(self):
    return Agent(
        role="LinkedIn Thought Leader",
        goal="Write a high-engagement LinkedIn post",
        backstory="""You are a respected Voice in the Tech industry. 
        You write with empathy and professionalism. 
        You use the 'Broetry' style (short paragraphs, lots of whitespace). 
        You focus on the 'Key Takeaways' and business value. 
        You start with a strong hook.""",
        llm=self.llm
    )
```

## Refactorización: El Desafío Multilingüe

Datalaria es un blog global, así que me enfrenté a un reto: **¿Necesito crear 4 agentes distintos para escribir en Español e Inglés?**

La respuesta de ingeniería es **NO**. Un agente es una entidad con una personalidad; el idioma es solo una herramienta.

En lugar de duplicar agentes, dupliqué las **Tareas (`Tasks`)**. En `src/tasks.py`, ahora defino explícitamente el idioma de salida:

```python
def twitter_task_es(self, agent, context):
    return Task(
        description="Escribe un hilo viral en ESPAÑOL basado en el análisis...",
        agent=agent,
        expected_output="Un hilo de Twitter en Español..."
    )

def twitter_task_en(self, agent, context):
    return Task(
        description="Write a viral Twitter thread in ENGLISH based on the analysis...",
        agent=agent,
        expected_output="A Twitter thread in English..."
    )
```

Esto hace que mi pipeline sea escalable. Si mañana quiero publicar en francés, solo añado una tarea, no contrato a un nuevo agente.

## La Batalla de los Agentes: Resultados Reales

Para probar esto, usé mi artículo sobre **"Procesos S&OP con IA y BPMN"**. Es un tema denso y aburrido si no se vende bien.

Veamos qué hicieron los agentes con el mismo input.

### El Resultado en Twitter (El Cínico)
*Nota del autor: Este resultado me dolió un poco, es más directo que yo.*

> Deja de ahogarte en muros de texto.
> Convertir manualmente narrativas industriales en diagramas es una tortura, es desperdiciar cerebro.
> Estamos usando genai para convertir docs de S&OP sucios en diagramas BPMN precisos en segundos.
> Así es como dejas de ser un traductor humano. 🧵
> ---
> La mayoría del "análisis de negocio" es solo fricción costosa y tediosa.
> La ia identifica dependencias ocultas que los humanos pasan por alto.
> No es solo dibujar; es descubrir la lógica enterrada bajo el relleno corporativo.
> #IngenieríaDeProcesos #Industry40

### El Resultado en LinkedIn (El Corporativo)

> Deja de ahogarte en "muros de texto" y cementerios de PDFs. 🧱
>
> Los procesos industriales son el corazón de tu empresa.
>
> Pero a menudo están enterrados en densas narrativas de S&OP que nadie lee.
>
> Esto crea una brecha masiva entre lo que el negocio necesita y lo que ingeniería construye.
>
> He pasado años viendo a Líderes Técnicos y Gerentes de Operaciones luchar con esta "capa de traducción".
>
> ¿La buena noticia? La IA Generativa está cambiando el juego.
>
> Al usar IA como un Analista de Negocio virtual, puedes transformar narrativas complejas en diagramas BPMN precisos en segundos.
>
> No se trata solo de velocidad. Se trata de claridad.
>
> 👇 ¿Cómo está tu equipo cerrando la brecha entre negocio y tecnología? Hablemos en los comentarios.

## Conclusión

La diferencia es abismal. El mismo modelo (Gemini 3.0 Flash), leyendo el mismo artículo, ha generado dos piezas de contenido completamente distintas, adaptadas al canal y al idioma.

Ya tengo:
1.  El **Cerebro** que entiende el código.
2.  Los **Creativos** que escriben el copy.
3.  Los archivos generados en mi disco duro.

Pero todavía hay un "humano" en el bucle. Sigo teniendo que ejecutar `python main.py` manualmente y copiar-pegar estos textos en las redes sociales.

En el próximo post, entramos en territorio hostil. Vamos a intentar conectar a estos agentes con el mundo exterior.

**Próximamente Post 4: La Pesadilla de las APIs.** Intentaré conectar mis agentes a Twitter y LinkedIn y (probablemente) casi perderé la cabeza en el proceso.

👉 **Código Fuente:** El código actualizado con los nuevos agentes y soporte multilingüe está disponible en la carpeta `/autopilot` del [repo de GitHub](https://github.com/Dalaez/datalaria-website).