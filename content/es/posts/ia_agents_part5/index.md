---
title: "Autopilot - Final: De Localhost a la Nube con GitHub Actions y CI/CD"
date: 2026-01-10
draft: false
category: "Proyectos Tecnológicos"
categories: ["DevOps", "GitHub Actions", "Python"]
tags: ["CI/CD", "Automation", "Pipeline", "GitOps", "Workflow"]
image: "cover.png"
description: "Capítulo final de Proyecto Autopilot. Ya no ejecuto scripts en mi ordenador. Ahora, un simple 'git push' despierta a mis agentes de IA, genera el contenido y lo publica en redes sociales tras mi aprobación."
summary: "En este último capítulo, abandonamos la ejecución manual. Construimos un pipeline de CI/CD en GitHub Actions que detecta nuevos artículos, orquesta a los agentes de IA y gestiona la publicación en Twitter y LinkedIn bajo supervisión humana. Bienvenidos a la automatización total."
---

Hemos recorrido un largo camino. Empezamos diseñando un **Cerebro** capaz de leer ([Post 2]({{< ref "posts/ia_agents_part2" >}})), le dimos personalidad con **Agentes Creativos** ([Post 3]({{< ref "posts/ia_agents_part3" >}})) y luchamos contra la burocracia para conseguir unas **Manos** (APIs) que pudieran publicar legalmente ([Post 4]({{< ref "posts/ia_agents_part4" >}})).

Pero nos quedaba un último gran paso para no **ser un esclavo de mi terminal** y es que ahora mismo, para publicar, tenía que estar en mi ordenador, abrir la consola y ejecutar `python main.py`. Eso no es "Piloto Automático". Eso es "Conducción Asistida".

Hoy, en el capítulo final, cortamos los cables. Nos vamos a la nube y automatizamos todo el proceso con mis agentes IA.

![Imagen conceptual del proyecto - Final](autopilot_final.png)

## La Arquitectura del Flujo (Pipeline)

El objetivo es el **GitOps**: que mi única interacción con el sistema sea subir cambios a Git. Todo lo demás debe ocurrir por magia (o mejor dicho, por **GitHub Actions**).

He diseñado un flujo de trabajo en dos fases:

1.  **Fase de Detección y Previsualización (Automática):**
    * GitHub detecta un nuevo archivo `.md` (o cambios en uno existente).
    * Se activa el **Orquestador**.
    * El sistema detecta el idioma del post (Español/Inglés) y calcula la URL correcta.
    * La IA (o el sistema de plantillas) propone un tweet y un post de LinkedIn.
    * El sistema me muestra una "Vista Previa" en los logs de ejecución, pero **no publica nada**.

2.  **Fase de Publicación (Manual):**
    * El proceso se **pausa** automáticamente gracias a los *Environments* de GitHub.
    * Me llega una alerta para revisar el despliegue.
    * Si le doy al botón verde (**Approve**), el sistema ejecuta la llamada real a las APIs.

{{< mermaid >}}
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f4f8', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#e6e6e6'}}}%%
graph TD
    %% Nodo Inicial
    START([GitHub detecta cambio en .md]) --> ORC

    %% --- FASE 1: AUTOMÁTICA ---
    subgraph Phase1 ["🔹 Fase 1: Detección y Previsualización (Automática)"]
        direction TB
        ORC[Se activa el Orquestador]
        
        %% Tareas en paralelo
        ORC --> TASK1[Detectar Idioma y Calcular URL]
        ORC --> TASK2[IA propone Tweet y LinkedIn]
        
        %% Convergencia
        TASK1 --> LOGS
        TASK2 --> LOGS
        
        LOGS[Mostrar 'Vista Previa' en Logs de Ejecución]
        LOGS --> NOPUB[🚫 NO SE PUBLICA NADA AÚN]
    end

    NOPUB --> PAUSE

    %% --- FASE 2: MANUAL ---
    subgraph Phase2 ["🔸 Fase 2: Publicación (Manual)"]
        direction TB
        PAUSE((⏸️ PAUSA AUTOMÁTICA<br/>GitHub Environments))
        
        PAUSE --> ALERT[🔔 Llega alerta para revisar despliegue]
        ALERT --> DECISION{¿Aprobar Despliegue?}
        
        %% Camino de Aprobación
        DECISION -- "Botón Verde (Approve) ✅" --> EXEC[🚀 Ejecutar llamada real a APIs]
        
        %% Camino de Rechazo (Implícito)
        DECISION -- "Rechazar / Cancelar ❌" --> STOP([Fin del flujo sin publicar])
    end

    %% Estilos para resaltar los pasos finales
    style EXEC fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724
    style STOP fill:#f8d7da,stroke:#dc3545,stroke-width:2px,color:#721c24
    style PAUSE fill:#fff3cd,stroke:#ffc107,stroke-width:3px
{{< /mermaid >}}

## El Director de Orquesta (`orchestrator.py`)

Necesitaba un script que uniera todas las piezas. Para ello, comencé desarrollando un orquestador en Python el cual actúa como puente entre el archivo Markdown y mis módulos de redes sociales.

Este script es el encargado de la lógica "fina" que a veces olvidamos:
* ¿Es un post en inglés (`/en/`) o en español (`/es/`)?
* ¿Tiene imagen destacada para generar la tarjeta de Twitter/X o LinkedIn?
* ¿Quiero que lo escriba la IA o quiero escribirlo yo?

### La Funcionalidad Estrella: "Director's Cut"

A veces, la IA no acierta con el tono exacto, o simplemente quiero escribir yo mismo el copy para un anuncio especial. Para no perder la automatización pero mantener el control, implementé una lógica de "Sobreescritura Manual" usando el *Frontmatter* de Hugo.

Si mi script detecta esto en la cabecera del artículo:

```yaml
---
title: "Mi Gran Post"
social_text: "Hoy no quiero que la IA escriba por mí. Este post es tan especial que lo he redactado a mano. 👇"
---
```

El sistema **ignora la generación automática** y usa mis palabras exactas. Es el equilibrio perfecto: automatización por defecto, control manual cuando es necesario.

## Seguridad y CI/CD: Dormir Tranquilo

El archivo `.github/workflows/autopilot.yml` es donde ocurre la magia. Aquí definimos los "Secretos" (mis claves de API de Twitter y LinkedIn) y las reglas del juego.

Lo más interesante es la protección del entorno:

```yaml
jobs:
  publish:
    environment: production  # <--- La clave de la seguridad
    needs: check_changes
    steps:
      - run: python orchestrator.py
```

Al definir el entorno como `production`, GitHub me obliga a revisar y aprobar el despliegue. Esto evita que un error en el código o una "alucinación" de la IA publique contenido no deseado.

Además, hemos configurado el sistema para que **Twitter/X** genere las *Cards* con imagen automáticamente y **LinkedIn** trate el contenido como un "Artículo", asegurando que en ambas redes la imagen destacada del blog se vea grande y atractiva.

## El Resultado Final

Ahora, mi proceso de publicación es este:

1.  Escribo mi artículo en Markdown tranquilamente.
2.  Hago `git push`.
3.  Me tomo un café. ☕
4.  Entro a GitHub desde el móvil, veo la "Preview" del tweet generado (en el idioma correcto).
5.  Sonrío y pulso **Approve**.

En segundos, el contenido aparece en Twitter y LinkedIn. Sin abrir la terminal. Sin tocar Python. Desde cualquier lugar.

**Publicación en Twitter/X**

![Post publicado automáticamente en twitter](datalaria_twitter_primera_automatizacion.png)

**Publicación en Linkedin**

![Post publicado automáticamente en linkedin](datalaria_linkedin_primera_automatizacion.png)

## Conclusión del Proyecto Autopilot

Lo que empezó como un experimento para probar como funcionan los agentes de IA y como me puede ayudar en mi día a día, se ha convertido en un sistema de publicación profesional. Hemos tocado:
* **Prompt Engineering** para definir personalidades.
* **APIs OAuth 2.0** complejas y manejo de tokens.
* **Python** backend robusto.
* **DevOps** y CI/CD con GitHub Actions.

Este blog ya no es solo una colección de textos; es una aplicación viva que trabaja por mí. Y ahora que tengo tiempo libre... ¿qué será lo próximo que automaticemos?

**Gracias por acompañarme en esta serie.**

👉 **Código Fuente Final:** Todo el proyecto está disponible (y documentado) en [GitHub](https://github.com/Dalaez/datalaria-website).