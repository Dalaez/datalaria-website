---
title: "Ingeniería S&OP IV: Escalando a Enterprise (Multi-SKU y Cuellos de Botella)"
date: 2026-03-20
draft: false
categories: ["Ingeniería de S&OP", "Operations Research", "MLOps"]
tags: ["Supply Chain", "Optimization", "PuLP", "Parallel Processing", "Theory of Constraints"]
author: "Datalaria"
description: "El MVP ha muerto, viva el Enterprise. En el Capítulo 4 estresamos nuestro sistema S&OP con múltiples SKUs, enseñando cómo paralelizar modelos de IA y resolver matemáticamente la guerra por la capacidad de producción compartida."
image: "cover.png"
---

Tu MVP funciona. Un producto, un modelo, un plan perfecto. Enhorabuena: acabas de resolver el problema más fácil del universo de Supply Chain.

Ahora mete 3 productos que comparten la misma fábrica. El Producto A necesita 14.000 unidades en julio. El Producto C necesita 13.000 ese mismo mes. Tu fábrica produce 15.000. **¿A quién dejas sin stock?**

Si tu respuesta es "lo vemos en la reunión del jueves", tu empresa tiene un problema de ingeniería, no de gestión.

> **Executive Summary:** En los capítulos [1](/es/posts/sop_ingenieria-higiene-datos/), [2](/es/posts/sop-ingenieria-parte2-prediccion/) y [3](/es/posts/sop-ingenieria-parte3-optimizacion/) construimos un MVP funcional para un solo producto. En este Capítulo 4, lo destruimos. Inyectamos 3 años de histórico con 3 SKUs de perfiles radicalmente distintos, paralelizamos el entrenamiento de modelos Prophet con MLOps, y construimos un modelo unificado de Programación Lineal donde los productos *compiten matemáticamente* por una capacidad de fábrica limitada. Bienvenido a la Theory of Constraints ejecutada en código.

## El Error Fatal: Optimizar en Silos

El mayor pecado en Supply Chain Planning no es usar datos sucios (eso lo resolvimos en el [Capítulo 1](/es/posts/sop_ingenieria-higiene-datos/)). Es **optimizar cada producto como si la fábrica fuera infinita**.

Imagina tres directores de producto, cada uno con su Excel optimizado:

- Director del SKU-001 (Core): "Necesito producir 6.000/mes. Ya está calculado."
- Director del SKU-002 (Spare Part): "Solo necesito 15/mes. Sin problema."
- Director del SKU-003 (Seasonal): "En julio necesito 14.000. No negociable."

Suma: 6.000 + 15 + 14.000 = **20.015 unidades**. Tu fábrica produce 15.000. Cada director tiene razón individualmente. Colectivamente, es un colapso.

Esto es lo que Eli Goldratt describió en *The Goal* como **Theory of Constraints**: el sistema no se optimiza sumando óptimos locales. Se optimiza identificando el cuello de botella y dejando que las matemáticas repartan los recursos.

## Estrés-Test: Los 3 Perfiles que Rompen tu MVP

Para validar la arquitectura Enterprise, generamos un dataset de 3 años (2023-2025) con tres SKUs diseñados para romper cualquier modelo naïve:

| SKU | Perfil | Demanda Media | Trampa |
|-----|--------|---------------|--------|
| **SKU-001** | Core Product | ~200/día | Alta varianza + Black Friday 3x |
| **SKU-002** | Intermittent Spare | ~0.6/día | 70% días con demanda cero |
| **SKU-003** | Seasonal Summer | ~250/día | Picos de 500+ en julio, cero en invierno |

Le inyectamos ruido ERP real: outliers (x50), fechas corruptas, nulos, negativos. Esto no es un tutorial de juguete. Es lo que sale de un SAP en producción un martes cualquiera.

## MLOps: Paralelizando el Forecasting

Con un solo producto, entrenar Prophet toma 2 segundos. Con 50 SKUs en un bucle `for`, esperas 100 segundos. Con 500, te vas a casa.

La solución es la misma que usan los pipelines de producción: **paralelización**. Cada SKU es independiente estadísticamente, así que cada modelo puede entrenarse en su propio thread:

```python
from concurrent.futures import ThreadPoolExecutor

def process_sku(sku, df_sku, months, country_code):
    """Worker: entrena Prophet para un SKU."""
    predictor = ProphetPredictor(df_sku, sku_name=sku)
    predictor.preprocess_daily_aggregation()
    predictor.train_model(country_code=country_code)
    return predictor.generate_forecast(months=months)

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(process_sku, sku, df, 12, "ES"): sku
        for sku, df in sku_dataframes.items()
    }
```

3 modelos Prophet, 3 segundos. No 6. Tres. Si agregas 50 SKUs como tiene cualquier PYME mediana, la diferencia entre secuencial y paralelo es la diferencia entre un pipeline operativo y un script que nadie quiere ejecutar.

### Negative Clipping: La Regla de Negocio que Prophet Ignora

Prophet puede generar predicciones negativas. Matemáticamente tiene sentido (la regresión no sabe que la demanda no puede ser -12 unidades). Operativamente es un desastre.

Nuestro `forecasting_engine_v2.py` aplica un **Negative Clipping** post-predicción:

```python
# Business Rule: La demanda no puede ser negativa
for col in ["yhat", "yhat_lower", "yhat_upper"]:
    self.forecast[col] = self.forecast[col].clip(lower=0)
```

Una línea. Un error en producción menos. Esto es lo que separa MLOps de "Machine Learning en un Jupyter Notebook".

### Fault Tolerance: Un SKU No Mata al Pipeline

¿Qué pasa si el SKU-002 tiene solo 10 registros y Prophet falla? En un script amateur, el pipeline entero muere. En un sistema Enterprise:

```python
sku_name, forecast_df, error = future.result()
if error:
    print(f"[!!] {sku_name}: FAILED - {error}")
    result["skus_failed"] += 1
else:
    forecasts.append(forecast_df)
    result["skus_success"] += 1
```

Los 2 SKUs sanos terminan su trabajo. El que falló queda en el log. Esto es la diferencia entre un script y un **sistema**.

## La Matemática del Bottleneck: PuLP Unificado

Aquí está el núcleo intelectual de todo el capítulo. En el [Capítulo 3](/es/posts/sop-ingenieria-parte3-optimizacion/) optimizamos un producto. Ahora creamos un **único modelo LP** donde todos los SKUs coexisten:

```python
# ── Variables de decisión MULTI-DIMENSIONALES ──
production[sku][t]  # Cuánto fabricar del SKU s en el periodo t
inventory[sku][t]   # Inventario del SKU s al final del periodo t

# ── Función Objetivo: Coste TOTAL del sistema ──
problem += lpSum(
    prod_cost[sku] * production[sku][t]
    + hold_cost[sku] * inventory[sku][t]
    for sku in skus for t in range(T)
), "Total_System_Cost"

# ── LA RESTRICCIÓN CLAVE: Capacidad Compartida ──
for t in range(T):
    problem += (
        lpSum(production[sku][t] for sku in skus) <= SHARED_MAX_CAPACITY,
        f"SharedCapacity_t{t}"
    )
```

Lee esa última restricción. Es una sola línea de código, pero contiene **toda la teoría de restricciones de Goldratt codificada**:

`lpSum(production[sku][t] for sku in skus) <= 15,000`

Le estás diciendo a la máquina: "La fábrica produce máximo 15.000 unidades al mes. Me da igual si es 15.000 de SKU-001 o 7.500 de cada uno. Tú decides el reparto que minimice el coste total del sistema."

Y el solver decide. Sin reuniones. Sin política. Sin "siempre le damos prioridad al cliente grande". Matemáticas.

## El Resultado: Asignación Inteligente de Capacidad

Nuestro solver con datos reales de Supabase:

```
  SKU-001: demand=70,879 | prod=70,579 | avg_inv=5,754 | cost=855,394 EUR
  SKU-002: demand=143   | prod=128   | avg_inv=6     | cost=6,775 EUR
  SKU-003: demand=84,298 | prod=84,098 | avg_inv=115   | cost=1,265,970 EUR

  Coste producción total:     1,973,660 EUR
  Coste almacenamiento total:   154,479 EUR
  ** COSTE TOTAL SISTEMA:     2,128,139 EUR **
```

Observa las decisiones que tomó el algoritmo:

- **SKU-001** (prod_cost=10€, hold_cost=2€): Es barato de almacenar. El solver produce por adelantado en meses baratos y acumula inventario (avg 5.754 uds). Pre-build inteligente.
- **SKU-002** (prod_cost=50€, hold_cost=5€): Pieza cara. Producción just-in-time estricta (avg_inv=6 uds). No stockea ni una pieza de más.
- **SKU-003** (estacional): Inventario mínimo en safety stock. Produce exactamente lo que necesita cada mes siguiendo la ola estacional.

Ningún humano con Excel puede calcular esto con 3 productos y 13 meses. Y definitivamente no puede recalcularlo cada semana cuando cambia el forecast.

## The Ah-Ha Moment: El Cuello de Botella Visual

![Capacidad de producción compartida Multi-SKU: la línea roja marca el límite de fábrica](pulp_multisku_capacity.png)
*Observa los meses de verano. La demanda combinada de los 3 SKUs supera la capacidad de la fábrica (línea roja). ¿Qué hace el algoritmo? En lugar de romper stock, decide adelantar la producción del SKU más barato de almacenar (SKU-001) a primavera, dejando hueco en la fábrica para el producto estacional crítico (SKU-003) en verano. Esto es Theory of Constraints ejecutada por una máquina.*

*Si miras la gráfica, parece que el SKU-002 (repuestos) no existe. Pero está ahí. Representa el 0,1% del volumen de la fábrica, pero en la gestión manual suele consumir el 20% del tiempo mental del planificador por su alta volatilidad. Al delegar esto a un modelo de Programación Lineal, el sistema gestiona los grandes volúmenes y la larga cola simultáneamente sin estrés.*

## Open Kitchen: Rompe el Sistema

Desconfío de las teorías que no se pueden poner en práctica. He preparado un nuevo Google Colab Enterprise donde puedes hacer el experimento más revelador de toda la serie:

**Baja la variable `SHARED_MAX_CAPACITY` a 12.000.** Observa cómo el solver empieza a hacer malabares extremos: sacrifica inventario de SKU-001 para dar prioridad a SKU-003 en julio. Bájala a 10.000 y verás el modelo declarar `INFEASIBLE` — la fábrica literalmente no puede satisfacer la demanda ni con la mejor planificación posible. Ese es tu punto de inflexión para invertir en ampliar capacidad.

📎 **[Abrir el Google Colab Multi-SKU Enterprise](https://colab.research.google.com/drive/1fBun7rDVGWN7XQGeSUbffm9VuhtTN9Bo?usp=sharing)**

Cambia la capacidad máxima de la fábrica, modifica los costes de almacenamiento, añade un cuarto SKU. Haz ingeniería, no fe.

## La Cadena Completa: De MVP a Enterprise

Con este cuarto capítulo, hemos escalado un prototipo de un solo producto a una arquitectura Enterprise Multi-SKU:

{{< mermaid >}}
flowchart LR
    subgraph CAP1["Capitulo 1: Higiene"]
        A["CSV Sucio ERP"]
        B["Datos Limpios"]
    end

    subgraph CAP2["Capitulo 2: Forecast"]
        C["Prophet Probabilistico"]
    end

    subgraph CAP3["Capitulo 3: Optimizacion MVP"]
        D["PuLP 1 SKU"]
    end

    subgraph CAP4["Capitulo 4: Enterprise"]
        E["Parallel Prophet - 3 SKUs"]
        F["PuLP Unificado - Shared Capacity"]
    end

    subgraph DB["Supabase"]
        G[("Single Source of Truth")]
    end

    A --> B --> G
    G --> C --> G
    G --> D --> G
    G --> E --> G
    G --> F --> G

    style A fill:#ff6b6b,stroke:#c0392b,color:#fff
    style B fill:#2ecc71,stroke:#27ae60,color:#fff
    style C fill:#3498db,stroke:#2980b9,color:#fff
    style D fill:#9b59b6,stroke:#8e44ad,color:#fff
    style E fill:#e67e22,stroke:#d35400,color:#fff
    style F fill:#e74c3c,stroke:#c0392b,color:#fff
    style G fill:#f39c12,stroke:#d35400,color:#fff
{{< /mermaid >}}

**Leyenda:**
- 🔴 **Rojo:** Datos crudos / Restricción crítica (Shared Capacity)
- 🟢 **Verde:** Señal limpia
- 🔵 **Azul:** Predicción probabilística
- 🟣 **Púrpura:** Optimización MVP (1 SKU)
- 🟠 **Naranja:** Procesamiento paralelo (Multi-SKU)
- 🟡 **Amarillo:** Base de datos centralizada

## Siguiente Paso: El Cerebro Autónomo

Nuestra base de datos Supabase ya tiene el plan maestro perfecto. Tres productos, trece meses, cada unidad asignada al mes óptimo considerando costes, estacionalidad y capacidad física.

Pero las bases de datos no envían emails a proveedores. No negocian con los directores de planta. No generan las órdenes de compra a las 6am del lunes.

En el **Capítulo 5 (Gran Final)**, conectaremos este plan a **Agentes de Inteligencia Artificial** (CrewAI) para que ejecuten las operaciones de forma autónoma. El algoritmo decide cuánto comprar. El agente ejecuta la compra. El humano... supervisa.

> La diferencia entre una empresa que planifica y una que se optimiza es un modelo matemático entre sus datos y sus decisiones. Y entre sus decisiones y sus acciones, un agente autónomo.
