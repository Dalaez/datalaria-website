---
title: "Ingeniería S&OP V: El Cerebro Autónomo (Agentic AI)"
date: 2026-03-27
draft: false
categories: ["S&OP Engineering", "Artificial Intelligence", "CrewAI"]
tags: ["Supply Chain", "Agentic AI", "LLMs", "Automation", "Python"]
author: "Datalaria"
image: "cover.png"
description: "Las matemáticas no envían emails. En el gran final de nuestra serie, construimos un equipo de Agentes de IA que leen nuestro plan maestro y ejecutan las operaciones de forma autónoma."
---

# 1. El Abismo de la Ejecución

Las empresas invierten millones en software de planificación y ERPs. Pasan meses integrando datos, limpiando registros y afinando previsiones de demanda. Y aun así, al final del día, la ejecución suele depender de un analista frente a un dashboard. Un humano leyendo gráficos para, finalmente, redactar un correo electrónico al director de la fábrica solicitando cambios en la producción.

Ese *delay* humano es ineficiente, propenso a errores y, francamente, innecesario en la era moderna. Las matemáticas puras no tienen valor si no se ejecutan.

La solución no es un simple script de automatización rígido, ni tampoco un chatbot al que hacerle preguntas. La verdadera modernización requiere **Agentic AI**. No estamos hablando de ChatGPT. Hablamos de Agentes Autónomos: piezas de software con un rol específico, un objetivo claro, e integrados con *herramientas* (Tools) que les permiten interactuar con bases de datos y APIs del mundo real.

# 2. La Arquitectura: CrewAI + Supabase

Para este Cerebro Autónomo, hemos implementado una arquitectura multi-agente utilizando **CrewAI**. Nuestro equipo digital ("La Agencia") está compuesto por dos agentes clave:

*   **Senior Supply Chain Analyst**: Su trabajo es puramente analítico. No le damos un PDF para resumir; le hemos equipado con una herramienta de Python (`@tool`) que le permite ejecutar consultas SQL contra nuestra base de datos en Supabase. Extrae el plan de producción óptimo que generó PuLP en el Capítulo 4, identifica los cuellos de botella y señala los meses donde el nivel de estrés productivo es más crítico.
*   **Procurement & Plant Manager**: Actúa como el ejecutor. Basándose estrictamente en las conclusiones matemáticas del Analista, redacta las órdenes ejecutivas definitivas.

Dato crucial: **No alucinan**. Sus decisiones están ancladas en los datos duros recuperados matemáticamente desde la base de datos central.

# 3. El Código: Tools over Prompts

El verdadero poder del Agentic AI radica en proporcionar a los LLMs la capacidad de interactuar con sistemas externos. El C-Level debe entender que no le estamos dando un Excel a un modelo de lenguaje; le estamos dotando de la capacidad de "pensar" y ejecutar acciones utilizando el patrón **ReAct** (Reasoning and Acting).

Este es un fragmento de cómo conectamos nuestro Agente a Supabase:

```python
from crewai.tools import tool
from supabase import create_client

@tool("fetch_latest_supply_plan")
def fetch_latest_supply_plan() -> str:
    """
    Se conecta a la base de datos Supabase, busca la ejecución más 
    reciente del plan de producción optimizado y extrae el plan estratégico 
    de los próximos 3 meses para todos los SKUs.
    """
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # 1. Buscar ejecución más reciente
    latest = supabase.table("supply_plans").select("execution_date").order("execution_date", desc=True).limit(1).execute()
    exec_date = latest.data[0]["execution_date"]
    
    # 2. Extraer el plan óptimo generado por PuLP
    response = supabase.table("supply_plans").select("*").eq("execution_date", exec_date).execute()
    
    # ... Formateo en Markdown estructurado para evitar alucinaciones ...
    return report

# Instanciamos el Agente Analista conectándolo a la herramienta
analyst_agent = Agent(
    role='Senior Supply Chain Analyst',
    goal='Analizar el plan maestro de producción y detectar cuellos de botella y riesgos de inventario.',
    backstory='Eres un analista implacable que busca la eficiencia del capital. Odias el exceso de inventario pero temes las roturas de stock...',
    verbose=True,
    allow_delegation=False,
    tools=[fetch_latest_supply_plan], # <-- Aquí inyectamos el acceso a la Base de Datos
    llm=gemini_llm
)
```

Al compilar a los agentes en un `Process.sequential`, orquestamos un flujo de trabajo donde la salida del Analista alimenta directamente las acciones del Manager de Planta.

# 4. El Resultado Final

Si ejecutamos nuestra *"Crew"*, esto es exactamente lo que el modelo escupe en la terminal después de consultar la base de datos y razonar sobre los 12.000 límites de capacidad mensuales de la fábrica:

> [!NOTE]
> **ASUNTO: URGENTE - Plan de Producción Julio-Septiembre | Alerta de Cuello de Botella**
> 
> Hola Carlos,
> 
> Tras ejecutar el modelo de optimización matemática para el próximo trimestre, te confirmo el Plan Maestro de Producción. Nos enfrentamos a un cuello de botella crítico de capacidad (12.000 unidades/mes) durante el verano que requiere ejecución estricta.
> 
> **Julio (Capacidad 100% - Riesgo Crítico):**
> Toda la capacidad de la planta debe dedicarse exclusivamente al SKU-001 (12.000 unidades). Paralizad las líneas del SKU-002 y SKU-003 este mes. El modelo ha adelantado esta producción para evitar roturas en los meses siguientes.
> 
> **Agosto (Capacidad 100% - Mix de Producción):**
> La fábrica seguirá al límite. La distribución será:
> - SKU-001: 5.000 uds
> - SKU-002: 15 uds
> - SKU-003: 6.985 uds (Prioridad alta para la campaña estacional)
> 
> **Septiembre (Capacidad 83% - Estabilización):**
> La presión bajará. Fabricaremos 8.000 uds del SKU-001, 10 uds del SKU-002 y 2.000 uds del SKU-003, lo que nos permitirá margen para mantenimiento de las líneas.
> 
> Por favor, coordina con compras para asegurar la materia prima del SKU-001 de forma inmediata para la primera semana de Julio. El algoritmo no contempla margen de error en las 12.000 unidades de ese mes.
> 
> Saludos,
> Agentic S&OP Copilot (En nombre de Dirección de Operaciones)

Este correo no es una plantilla genérica. Es una decisión operativa, justificada e imparcial, generada autónomamente a partir de un modelo de programación lineal y enviada en segundos.

# 5. The Sandbox

¿Quieres ver cómo razonan en tiempo real? He preparado un cuaderno interactivo para que pruebes el sistema tú mismo.

👉 [**Abre el Google Colab de Agentic S&OP**](https://colab.research.google.com/drive/1Yh1D6LiIOgPhpkJyHNnJ6rUZxHknC550?usp=sharing)

Por motivos de seguridad, en el entorno público hemos simulado el retorno de la base de datos, pero si insertas tu propia API Key de Gemini (es gratuita), podrás observar en los logs el proceso de razonamiento paso a paso de los agentes antes de emitir la orden final.

# 6. Conclusión de la Serie

Hemos llegado al final de nuestro viaje "S&OP Engineering". A lo largo de cinco capítulos, hemos evolucionado la planificación empresarial desde sus cimientos más sucios hasta la vanguardia tecnológica:

1.  **Fundamentos**: Limpiamos y normalizamos años de datos históricos desestructurados.
2.  **Visión**: Implementamos motores de Inteligencia Artificial iterativos para prever la demanda futura con alta precisión (Prophet).
3.  **Lógica**: Introdujimos Ciencias de la Decisión y Programación Lineal para equilibrar el inventario (PuLP).
4.  **Escalabilidad**: Llevamos el modelo matemático a nivel Enterprise lidiando con restricciones de capacidad y MLOps paralelizado.
5.  **Ejecución**: Le dimos un Cerebro Autónomo al sistema para cerrar la brecha entre el Dashboard y el mundo real.

The CTO Pitch: **Si tu empresa sigue planificando la demanda con promedios móviles en Excel, estás perdiendo dinero**. La eficiencia del capital, la reducción de roturas de stock y la automatización inteligente ya no son el futuro; son el estándar operativo que exigen los márgenes actuales.

Es hora de jubilar los modelos estáticos. Hablemos de cómo modernizar tu Cadena de Suministro desde la raíz hasta la ejecución autónoma.
