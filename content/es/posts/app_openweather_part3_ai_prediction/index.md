---
title: "Proyecto Weather Service (Parte 3): Prediciendo el Futuro con IA y OpenWeatherMap"
date: 2025-11-15
draft: False
categories: ["Proyectos", "IA", "Herramientas"]
tags: ["machine-learning", "regresion", "openweathermpa", "python", "pandas", "scikit-learn", "javascript", "frontend", "prediccion-datos", "pronostico-tiempo", "serverless"]
image: weather_forecast_dashboard.png
description: "La entrega final de nuestro proyecto Weather Service. Nos adentramos en la adición de capacidades predictivas, combinando pronósticos oficiales de OpenWeatherMap con nuestro modelo de IA (Regresión Lineal) personalizado para predecir el tiempo de mañana y visualizar su precisión."
summary: "De la recolección de datos a los dashboards dinámicos, ¡ahora es el momento de predecir! Este post explora la integración del pronóstico a 5 días de OpenWeatherMap y la construcción de nuestro propio modelo de predicción de IA a 1 día utilizando datos históricos, todo visualizado en nuestro frontend interactivo."
---

En la [primera parte de esta serie](/blog/weather-service-part-1-backend), establecimos la columna vertebral de nuestro servicio meteorológico global, recolectando datos brutos utilizando Python y GitHub Actions. Luego, en la [Parte 2](/blog/weather-service-part-2-frontend), transformamos esos datos en un hermoso dashboard interactivo, aprovechando GitHub Pages/Netlify, JavaScript, PapaParse.js y Chart.js.

Ahora, es el momento del gran final: añadir capacidad predictiva a nuestro Weather Service. Exploraremos cómo aumentar nuestra visualización de datos históricos con pronósticos reales. Esta entrega se centra en un enfoque dual: integrar un pronóstico oficial y fiable de un servicio profesional (OpenWeatherMap) y, lo que es más emocionante, construir y entrenar nuestro propio modelo de IA simple (Regresión Lineal) para predecir el tiempo de mañana basándonos en los datos históricos que hemos recolectado meticulosamente. Finalmente, visualizaremos ambos pronósticos en nuestro dashboard, permitiendo una comparación directa y una prueba real de la precisión de nuestra IA.

¡Convirtamos nuestros datos en una bola de cristal! 🔮

![Conceptual image of Weather Service Predictions](AI_App_Weather_Image_Predictions.png)

---

### El Núcleo Predictivo: OpenWeatherMap y Nuestra IA Personalizada

El objetivo de esta funcionalidad predictiva era doble:

1.  **Pronóstico Oficial**: Obtener un pronóstico fiable y a varios días de un servicio meteorológico profesional (OpenWeatherMap - OWM).
2.  **Predicción de IA Personalizada**: Crear nuestro propio modelo de IA simple (Regresión Lineal) entrenado con los datos históricos que hemos recolectado, para predecir el tiempo del día siguiente.
3.  **Visualización y Comparación**: Mostrar y comparar ambos pronósticos para medir la precisión y el rendimiento de nuestro modelo de IA personalizado.

---

### 1. ⚙️ Lógica Backend: `read_weather.py` se Vuelve más Inteligente

Nuestro script `read_weather.py`, anteriormente responsable de la recolección de datos, ahora amplía su función para recopilar datos tanto de OWM como de nuestros archivos históricos, consolidando todo en un único fichero `predicciones.json`.

#### Paso 1: Obtener el Pronóstico a 5 Días de OpenWeatherMap

Decidimos que, además de la predicción de IA a 1 día, un pronóstico a 5 días de OWM proporcionaría un contexto valioso.

* **API Endpoint**: Optamos por la API gratuita `data/2.5/forecast` (ya que OneCall 3.0 requería un método de pago).
* **Procesamiento de Datos**: Esta API devuelve datos en bloques de 3 horas. Tuvimos que añadir lógica en Python para:
    * Iterar sobre la lista de ~40 pronósticos.
    * Agruparlos por día (ignorando el día actual).
    * Para cada uno de los 5 días siguientes, calcular la temperatura máxima, mínima y media de todos los bloques de 3 horas dentro de ese día.
* **Resultado**: Una lista de 5 objetos (uno por día) que contienen las predicciones de temperatura máxima, mínima y media de OWM.

#### Paso 2: Implementar Nuestro Modelo de IA (Predicción a 1 Día)

Esta es la parte central de nuestra "IA casera". Para cada ciudad:

* **Carga de Datos**: Utilizamos `pandas` para leer el fichero CSV histórico de la ciudad (ej. `datos/Madrid.csv`).
* **Ingeniería de Características (Feature Engineering)**: Como teníamos múltiples lecturas por día, el paso más crucial fue transformar estos datos:
    * **Remuestreo**: Usamos `df.resample('D')` de `pandas` para agrupar los datos por día, calculando los agregados diarios reales (ej., `temp_max`, `temp_min`, `temp_media`, `hum_media`).
    * **Creación de Características (X)**: Creamos nuevas columnas "desplazadas" (`.shift(1)`) para que cada fila (representando un día) contuviera los datos del día anterior (ej., `temp_max_lag1`, `hum_media_lag1`). También añadimos `dia_del_anio` para capturar la estacionalidad.
    * **Creación de Objetivos (y)**: Definimos qué queríamos predecir (ej., la `temp_max` real del día actual).
* **Entrenamiento de 3 Modelos**: En lugar de uno, entrenamos tres modelos de Regresión Lineal (`scikit-learn`) independientes:
    * `model_max`: Entrenado con `y = df_clean['temp_max']`.
    * `model_min`: Entrenado con `y = df_clean['temp_min']`.
    * `model_media`: Entrenado con `y = df_clean['temp_media']`.
* **Predicción**:
    * Tomamos la última fila de datos agregados (representando los datos de "hoy").
    * Alimentamos estos datos a los 3 modelos para predecir los valores de "mañana".
    * Incluimos una salvaguarda (`MIN_RECORDS_FOR_IA = 10`) para que el modelo solo intente predecir si tiene suficientes datos históricos (ej., 10 días limpios).

#### Paso 3: Consolidar y Guardar

El script combina los resultados de los Pasos 1 y 2 en una estructura JSON y la guarda en `predicciones.json`:

```json
{
  "Madrid": {
    "pred_owm_5day": [ 
      { "date": "...", "max": 15.0, "min": 10.0, "avg": 12.5 }, 
      ... (5 días) ...
    ],
    "pred_ia": {
      "max": 14.8,
      "min": 7.5,
      "media": 11.2,
      "records": 120
    }
  },
  "A Coruña": {
     ...
     "pred_ia": { "max": null, "min": null, "avg": null, "records": 9 } // Ejemplo de datos insuficientes
  }
}
```

---

### 2. 🎨 Lógica Frontend: `index.html` Visualiza el Futuro

El frontend es responsable de cargar este fichero `predicciones.json` y presentarlo de forma visualmente atractiva e informativa.

#### Paso 1: Carga de Datos

  * `loadPredictions()`: Creamos una nueva función `async` que se ejecuta una vez durante la inicialización (antes de `updateDashboard`).
  * `allPredictionsCache`: Esta función carga `predicciones.json` y lo guarda en esta nueva variable global para que todas las funciones de visualización tengan acceso a él.

#### Paso 2: Visualización en las "Super-Cards" (KPIs)

Queríamos una comparación directa y clara.

  * **Pronóstico OWM a 5 Días**:
      * Creamos una función auxiliar `buildForecastHTML()`.
      * Esta función toma la lista `pred_owm_5day` y genera un bloque de HTML con una lista de los 5 días y sus temperaturas máximas/mínimas (ej. "Sáb, 9 nov: 15.1°C / 10.0°C").
  * **Pronóstico IA a 1 Día (Comparativa)**:
      * Creamos una segunda función auxiliar `buildIAForecastHTML()`.
      * Esta función toma el objeto `pred_ia` y el primer día del pronóstico de OWM (`pred_owm_5day[0]`).
      * **Lógica de Comparación**: Para las temperaturas máxima, mínima y media, muestra el valor de la IA y luego, a su lado, la diferencia con OWM.
      * **Impacto Visual**: La diferencia se colorea de rojo (si nuestra IA predice más calor) o azul (si predice más frío), dándonos una señal visual inmediata de la desviación de nuestro modelo.
      * También gestiona el caso de "Datos insuficientes" (`${ia_preds.records}/${MIN_RECORDS_FOR_IA}`).
  * `updateKPIs()`: La plantilla de la tarjeta fue modificada para llamar a estas dos nuevas funciones, mostrando ambos bloques de pronóstico.

#### Paso 3: Visualización en los Gráficos

Queríamos que los pronósticos se integraran directamente en los gráficos existentes.

  * **Gráfico de Evolución (Línea de Puntos)**:
      * En `updateChart()`, añadimos un nuevo dataset por cada ciudad.
      * Este dataset utiliza la media de la predicción de OWM (`pred_owm_5day`).
      * Le aplicamos el estilo `borderDash: [5, 5]` para que se dibuje como una línea de puntos.
      * "Cosemos" el inicio de esta línea al último punto de datos reales para que parezca una continuación fluida.
  * **Gráfico de Variación (Barras Rayadas)**:
      * En `updateVariationChart()`, añadimos otro dataset por cada ciudad.
      * Los datos `y` de este conjunto son `day.max - day.min` (la variación) del pronóstico de OWM.
      * Para el estilo, creamos una función auxiliar `createStripedPattern()` que dibuja un patrón de rayas en un canvas.
      * Utilizamos este patrón como `backgroundColor` para las barras de pronóstico, diferenciándolas de las barras de datos reales, que son sólidas.

---

### Conclusión (Parte 3)

¡Con esta entrega final, nuestro proyecto Weather Service está completo! Hemos integrado con éxito tanto pronósticos profesionales a 5 días de OpenWeatherMap como un modelo de predicción de IA personalizado a 1 día, todo ello impulsado por nuestros datos históricos recopilados. El frontend ahora proporciona una experiencia rica e interactiva que no solo visualiza el clima pasado, sino que también ofrece un vistazo al futuro, con un análisis comparativo del rendimiento de nuestra IA.

Este viaje ha cubierto desde la recolección de datos en el backend, la automatización con GitHub Actions, el alojamiento de sitios estáticos con Netlify, hasta el desarrollo de frontend dinámico con JavaScript "vainilla", el análisis avanzado de datos con PapaParse.js, la creación de gráficos interactivos con Chart.js, y finalmente, adentrarnos en el Machine Learning para el análisis predictivo.

Hemos construido una aplicación robusta, sin servidor y perspicaz, enteramente con servicios gratuitos. Las posibilidades de expansión (ej., modelos de ML más complejos, diferentes fuentes de datos, cuentas de usuario) son infinitas, pero por ahora, ¡tenemos un oráculo meteorológico completamente funcional!

---

### Referencias y Enlaces de Interés:

  * **Servicio Web Completo**: Puedes ver el resultado final de este proyecto en acción aquí: [https://datalaria.com/apps/weather/](https://datalaria.com/apps/weather/)
  * **Repositorio GitHub del Proyecto**: Explora el código fuente y la estructura del proyecto en mi repositorio: [https://github.com/Dalaez/app_weather](https://github.com/Dalaez/app_weather)
  * **OpenWeatherMap API**: [https://openweathermap.org/api](https://openweathermap.org/api)
  * **Pandas**: Librería de análisis de datos de Python: [https://pandas.pydata.org/](https://pandas.pydata.org/)
  * **Scikit-learn**: Machine Learning en Python: [https://scikit-learn.org/](https://scikit-learn.org/)
  * **PapaParse.js**: Parser de CSV rápido en el navegador para JavaScript: [https://www.papaparse.com/](https://www.papaparse.com/)
  * **Chart.js**: Gráficos JavaScript simples pero flexibles para diseñadores y desarrolladores: [https://www.chartjs.org/](https://www.chartjs.org/)