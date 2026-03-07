---
title: "Ingeniería S&OP II: Demand Planning, de la Adivinación a la Probabilidad"
date: 2026-03-07
draft: false
categories: ["Ingeniería de S&OP", "Data Engineering", "Machine Learning"]
tags: ["Supply Chain", "Forecasting", "Prophet", "Python", "MLOps"]
author: "Datalaria"
description: "Una predicción determinista en Excel es un riesgo financiero. En el Capítulo 2, evolucionamos nuestro pipeline S&OP con Facebook Prophet para calcular la probabilidad de la demanda, intervalos de incertidumbre y Safety Stock matemáticamente."
image: "cover.png"
---

Tu Excel dice "venderemos 100 unidades". Es un número redondo, bonito, determinista. ¿Y si vendes 120? Rotura de stock, cliente insatisfecho, penalización contractual. ¿Y si vendes 50? 50 unidades ocupando almacén, inmovilizando capital que podría estar generando rendimiento.

El problema no es la predicción en sí. Es la **arrogancia del número único**.

En el [Capítulo 1](/es/posts/sop_ingenieria-higiene-datos/) construimos una "Válvula de Calidad" que elimina el ruido de los datos del ERP. Ahora que tenemos una señal pura, vamos a hacer algo que Excel no puede: **medir la incertidumbre**.

> **Resumen Ejecutivo:** Un forecast probabilístico no te dice "venderás 100". Te dice "con un 95% de probabilidad, venderás entre 35 y 157". Esa banda de incertidumbre es la base matemática para calcular tu Safety Stock sin recurrir a reglas de dedo.

## La Arquitectura: MLOps, no Scripts

No hemos escrito un script de usar y tirar. Hemos conectado nuestro cerebro matemático (Python/Prophet) directamente a nuestra Single Source of Truth (Supabase/PostgreSQL).

El diseño clave es la tabla `demand_forecasts`. Observa una columna que la diferencia de un tutorial básico:

```sql
CREATE TABLE demand_forecasts (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_date  DATE NOT NULL,     -- ← Cuándo corrimos el modelo
    ds              DATE NOT NULL,     -- Fecha futura predicha
    yhat            NUMERIC NOT NULL,  -- Predicción central
    yhat_lower      NUMERIC NOT NULL,  -- Límite inferior (Safety Stock)
    yhat_upper      NUMERIC NOT NULL,  -- Límite superior (Riesgo)
    model_version   TEXT NOT NULL,     -- Trazabilidad
    UNIQUE(execution_date, ds)         -- Un forecast por ejecución y fecha
);
```

**¿Por qué `execution_date`?** Porque dentro de 6 meses, cuando quieras auditar si tu modelo era preciso, necesitas saber *cuándo* hiciste la predicción frente a *qué ocurrió realmente*. Esto es lo que en MLOps se llama **Snapshotting**: registrar el contexto de cada ejecución para poder evaluar el drift del modelo a lo largo del tiempo.

Sin esta columna, tienes un modelo. Con ella, tienes un **sistema auditable**.

## La Ingeniería: Por qué Prophet (y no un ARIMA de manual)

Prophet es un motor de series temporales desarrollado por Meta que fue diseñado para datos de negocio irregulares: gaps, festivos, cambios de tendencia. Exactamente lo que tiene una cadena de suministro real.

Aquí está el fragmento central de nuestra clase `ProphetPredictor`:

```python
def train_model(self, country_code='ES'):
    """
    Entrena Prophet con dos configuraciones clave para S&OP:
    - interval_width: Ancho del intervalo de confianza
    - country_holidays: Contexto operativo del país
    """
    self.model = Prophet(
        interval_width=0.95,     # ← Intervalo de confianza del 95%
        weekly_seasonality=True,
        yearly_seasonality=True
    )
    # Festivos que alteran patrones de carga/descarga
    self.model.add_country_holidays(country_name=country_code)
    self.model.fit(self.ts_df)
```

Dos decisiones de ingeniería que nos separan de un tutorial de YouTube:

**`interval_width=0.95`**: No es un parámetro decorativo. El límite superior (`yhat_upper`) representa la demanda máxima probable con un 95% de confianza. Esto es literalmente tu base de cálculo para el **Safety Stock**: `Safety Stock = yhat_upper - yhat`. Sin este intervalo, tu stock de seguridad es una corazonada; con él, es matemática.

**`add_country_holidays('ES')`**: En S&OP, los festivos no son "días libres". Son anomalías operativas: la fábrica cierra, el almacén no despacha, el transporte para. Si el modelo no sabe que el 15 de agosto España está de vacaciones, interpretará la caída de pedidos como una tendencia a la baja. Esto corrompe la predicción de septiembre.

## Traduciendo Matemáticas a Decisiones de Negocio

La teoría es bonita. Pero un Director General no aprueba presupuestos basándose en código Python. Necesita ver evidencia visual.

### El Forecast Probabilístico

![Forecast probabilístico de demanda con intervalos de confianza al 95%](prophet_forecast_plot.png)
*Los puntos negros son tu demanda histórica real. La línea azul central es la predicción (yhat). La banda sombreada es el intervalo de confianza al 95%. A mayor volatilidad histórica, más ancha es la banda → más Safety Stock necesitas → más caja inmovilizas. Esta banda es la conversación que deberías tener con tu CFO.*

### Explicabilidad: Separar Tendencia de Ruido Estacional

![Descomposición de componentes del modelo: tendencia, estacionalidad semanal y anual](prophet_components_plot.png)
*Esto es XAI (Explainable AI) aplicado al negocio. El modelo separa la Tendencia (¿el negocio crece o decrece?) de la Estacionalidad (¿hay picos por época del año?) y del efecto de los festivos. Esto es lo que el Director General necesita ver para aprobar el plan de operaciones: saber si el crecimiento es real o si es solo un efecto del calendario.*

## Open Kitchen: Pruébalo tú mismo

Desconfío de las teorías que no se pueden poner en práctica. Por eso, he preparado un entorno aislado donde puedes entrenar el modelo sobre un snapshot anonimizado de los datos que acabamos de limpiar en el Capítulo 1.

No necesitas instalar Python, ni Prophet, ni configurar Supabase. Solo necesitas un navegador:

📎 **[Abrir el Notebook interactivo en Google Colab](https://colab.research.google.com/drive/1q_iZ3rPmcoXXJ3qXQzSrlxMYCSstyP12?usp=sharing)**

Dale a "Play" en las celdas y observa cómo se genera un forecast probabilístico con bandas de incertidumbre. Modifica el horizonte, el país, el intervalo de confianza. Haz ingeniería, no fe.

## Siguiente Paso: De la Predicción a la Decisión

Ahora sabemos la probabilidad de lo que vamos a vender. La pregunta deja de ser *"¿cuánto venderemos?"* y pasa a ser **"¿qué debemos fabricar o comprar para maximizar margen y minimizar riesgo?"**.

En el Capítulo 3, introduciremos **Optimización Matemática** (PuLP) y **Teoría de Restricciones** para transformar las predicciones en decisiones de suministro: cuánto comprar, cuándo producir y cómo distribuir recursos finitos minimizando costes.

> La diferencia entre un Director de Operaciones que reacciona y uno que decide es un modelo matemático entre los datos y la acción.
