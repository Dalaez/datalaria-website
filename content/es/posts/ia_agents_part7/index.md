---
title: "Autopilot - Ctrl: Auditoría de Contenido IA con GitHub Copilot CLI"
date: 2026-02-01
draft: false
categories: ["DevOps", "Python", "AI"]
tags: ["devchallenge", "githubchallenge", "cli", "githubcopilot", "Copilot CLI", "Content Audit", "Automation"]
image: "cover.png"
description: "Construyo autopilot-ctrl, una CLI que usa GitHub Copilot CLI para auditar y mejorar automáticamente el contenido generado por IA antes de publicarlo en redes sociales."
summary: "Cuando la IA genera contenido para redes sociales, ¿cómo sabemos si es bueno? Construí autopilot-ctrl, una herramienta que usa GitHub Copilot CLI para evaluar la calidad del contenido antes de publicar."
---

*This is a submission for the [GitHub Copilot CLI Challenge](https://dev.to/challenges/github-2026-01-21)*

## What I Built

**autopilot-ctrl** es una herramienta de línea de comandos que audita contenido de redes sociales generado por IA antes de publicarlo. Piénsalo como un "quality gate" para tu pipeline de contenido.

### El Problema

Mi blog tiene un sistema de autopilot que genera automáticamente posts para Twitter, LinkedIn y Newsletter cada vez que publico un artículo. Funciona genial... la mayoría del tiempo. Pero a veces la IA produce:

- 🐦 Tweets genéricos sin gancho
- 💼 Posts de LinkedIn sin estructura
- 📧 Newsletters que revelan demasiado (o muy poco)

Necesitaba una forma de **evaluar la calidad ANTES de publicar** y, si algo no pasaba el corte, mejorarlo automáticamente.

### La Solución

**autopilot-ctrl** usa GitHub Copilot CLI para:

1. **Auditar** contenido contra criterios específicos por plataforma
2. Asignar un **score de calidad** (0-10)
3. **Identificar problemas** específicos
4. **Generar versiones mejoradas** del contenido que falla

```
                               📊 Audit Results                                
┌─────────────┬─────────┬───────────┬─────────────────────────────────────────┐
│ Platform    │  Score  │  Status   │ Issues                                  │
├─────────────┼─────────┼───────────┼─────────────────────────────────────────┤
│ Twitter     │ 3.0/10  │ [XX] FAIL │ No hook, missing hashtags               │
│ Linkedin    │ 7.0/10  │ [OK] PASS │ -                                       │
│ Newsletter  │ 8.0/10  │ [OK] PASS │ -                                       │
└─────────────┴─────────┴───────────┴─────────────────────────────────────────┘
```

## Demo

{{< youtube KNjx5IB8jr8 >}}

**Comandos disponibles:**

```bash
# Verificar que Copilot CLI está instalado
python -m ctrl check

# Auditar contenido
python -m ctrl audit content.json

# Arreglar contenido que falla
python -m ctrl fix content.json --apply
```

**Screenshots del flujo:**

![1. Introducción a Autopilot-Ctrl](PS_Autopilot_Intro.png)

![2. Verificación de Copilot CLI](PS_Autopilot_Check.png)

![3. Contenido de ejemplo](PS_Autopilot_SampleContent.png)

![4. Resultados de la auditoría](PS_Autopilot_Audit.png)

![5. Contenido mejorado por Copilot](PS_Autopilot_Fix.png)

**Código fuente:** [github.com/Dalaez/datalaria/autopilot/ctrl](https://github.com/Dalaez/datalaria-website)

## My Experience with GitHub Copilot CLI

### 🚀 Cómo Usé Copilot CLI

La magia de autopilot-ctrl está en cómo integra Copilot CLI en modo no interactivo:

```python
# auditor.py
result = subprocess.run(
    ['copilot', '-s', '--no-ask-user', '-p', prompt],
    capture_output=True,
    text=True,
    timeout=60,
    encoding='utf-8'
)
```

Cada auditoría envía un prompt estructurado a Copilot CLI y parsea la respuesta natural para extraer:
- Score numérico (ej: "Rating: 7/10")
- Lista de issues (ej: "No engagement", "Generic hook")
- Sugerencias de mejora

### 💡 Lo Que Aprendí

1. **El orden de las flags importa**: `-p` DEBE ser el último argumento
2. **Prompts simples funcionan mejor**: Los prompts largos y estructurados en modo no interactivo devuelven respuestas vacías
3. **Copilot responde en lenguaje natural**: Tuve que crear parsers flexibles para extraer datos de respuestas como "**Rating: 7/10**"

### ⚡ El Impacto en Mi Workflow

Antes de autopilot-ctrl, revisaba manualmente cada post generado. Ahora:

1. `git push` → Autopilot genera contenido
2. `python -m ctrl audit generated_content.json` → Copilot evalúa
3. Si algo falla → `python -m ctrl fix` genera mejoras
4. Contenido aprobado → Se publica automáticamente

**Tiempo ahorrado**: ~15 minutos por publicación.

### 🛠️ Stack Técnico

- **Python + Click**: Framework CLI
- **Rich**: UI de terminal con tablas y colores
- **GitHub Copilot CLI**: Motor de evaluación IA
- **YAML configs**: Prompts personalizables por plataforma

---

## Conclusión

autopilot-ctrl demuestra que GitHub Copilot CLI no es solo para generar código. Es una herramienta poderosa para **integrar IA en cualquier pipeline** - en este caso, evaluación de calidad de contenido.

Si tienes un sistema que genera contenido automáticamente, considera añadir un "quality gate" con Copilot CLI. Tu audiencia (y tus métricas de engagement) te lo agradecerán.

**¿Preguntas?** Déjalas en los comentarios 👇

---

*Este post es parte de la serie [Proyecto Autopilot](https://datalaria.com/es/posts/ia_agents_part1/), donde documento cómo automatizo la creación y publicación de contenido usando IA.*
