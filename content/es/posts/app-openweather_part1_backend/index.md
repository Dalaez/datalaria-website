---
title: "Proyecto Weather Service (Parte 1): Construyendo el Recolector de Datos con Python y GitHub Actions o Netlify"
date: 2025-10-31
category: "Proyectos Tecnológicos"
draft: False
categories: ["Proyectos", "Herramientas"]
tags: ["python", "api", "github actions", "automatizacion", "serverless", "datos", "backend", "netlify"]
image: cover.png
description: "Primera entrega de la serie sobre cómo construir un servicio meteorológico. Nos centramos en el backend: conectar a la API de OpenWeatherMap, almacenar datos en CSV y automatizar todo 24/7 gratis con GitHub Actions o Netlify."
summary: "Empezamos nuestro proyecto meteorológico creando el motor: un script de Python que habla con una API, guarda datos históricos y se ejecuta solo cada día gracias a GitHub Actions. ¡Te cuento los trucos y los problemas!"
---

Como comenté en un post anterior, uno de mis objetivos con Datalaria es "ensuciarme las manos" con proyectos que me permitan aprender y conectar diferentes tecnologías del mundo de los datos. Hoy empezamos una serie dedicada a uno de esos proyectos: la creación de un **servicio meteorológico global completo**, desde la recolección de datos hasta su visualización y predicción, todo ello sin servidores y con herramientas gratuitas.

En esta primera entrega, nos centraremos en el **corazón del sistema: el backend recolector de datos**. Veremos cómo construir un "robot" que trabaje por nosotros 24/7, conectándose a una API externa, guardando la información de forma estructurada y haciendo todo esto de manera automática y gratuita. ¡Vamos allá!

![Conceptual image of Weather Service](Imagen_App_Weather_IA.png)

---

### El Primer Paso: Hablar con la API de OpenWeatherMap

Todo servicio meteorológico necesita una fuente de datos. Elegí [OpenWeatherMap](https://openweathermap.org/) por su popularidad y su generoso plan gratuito. El proceso inicial es sencillo:

1.  **Registrarse**: Crear una cuenta en su web.
2.  **Obtener la API Key**: Generar una clave única que nos identificará en cada llamada. Es como nuestra "llave" para acceder a sus datos.
3.  **Guardar la Clave**: ¡**Nunca** directamente en el código! Hablaremos de esto más adelante.

Con la clave en mano (¡o casi!), escribí un primer script `test_clima.py` para probar la conexión usando la maravillosa librería `requests` de Python:

```python
import requests

API_KEY = "TU_API_KEY_AQUI" # ¡Temporalmente! Luego usaremos Secretos
CIUDAD = "Madrid"
URL = f"[https://api.openweathermap.org/data/2.5/weather?q=](https://api.openweathermap.org/data/2.5/weather?q=){CIUDAD}&appid={API_KEY}&units=metric&lang=es"

try:
    respuesta = requests.get(URL)
    respuesta.raise_for_status() # Lanza un error si la respuesta no es 200 OK
    datos = respuesta.json()
    print(f"Temperatura en {CIUDAD}: {datos['main']['temp']}°C")
except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API: {e}")
except KeyError as e:
    print(f"Respuesta inesperada de la API, falta la clave: {e}")
```

**Primer Obstáculo Superado (con Paciencia):** Al ejecutarlo por primera vez, ¡error 401: No Autorizado\! 😱 Resulta que las API Keys de OpenWeatherMap pueden tardar unas horas en activarse después de generarlas. La lección: a veces, la solución es simplemente esperar. ⏳

-----

### La "Base de Datos": ¿Por Qué CSV y No SQL?

Con los datos fluyendo, necesitaba almacenarlos. Podría haber montado una base de datos SQL (PostgreSQL, MySQL...), pero eso implicaba complejidad, un servidor (coste) y, para este proyecto, era matar moscas a cañonazos.

Opté por la simplicidad radical: **ficheros CSV (Comma Separated Values)**.

  * **Ventajas**: Fáciles de leer y escribir con Python, perfectamente versionables con Git (podemos ver el historial de cambios), y suficientes para el volumen de datos que manejaríamos inicialmente.
  * **Lógica Clave**: Necesitaba añadir una nueva fila cada día a cada fichero de ciudad, pero escribiendo la cabecera (`fecha_hora`, `ciudad`, `temperatura_c`, etc.) solo la primera vez. La librería `csv` nativa de Python y `os.path.exists` lo hacen trivial:

```python
import csv
import os
from datetime import datetime

# ... (código para obtener datos de la API para una ciudad) ...

ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
fila_datos = [ahora, ciudad, temperatura, ...] # Lista con los datos
cabecera = ['fecha_hora', 'ciudad', 'temperatura_c', ...] # Lista con los nombres de columna
nombre_fichero = f"datos/{ciudad}.csv" # Creamos una carpeta 'datos'

# Asegurarse de que la carpeta 'datos' existe
os.makedirs(os.path.dirname(nombre_fichero), exist_ok=True)

es_archivo_nuevo = not os.path.exists(nombre_fichero)

try:
    with open(nombre_fichero, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if es_archivo_nuevo:
            writer.writerow(cabecera) # Escribir cabecera SOLO si es nuevo
        writer.writerow(fila_datos) # Añadir la nueva fila de datos
    print(f"Datos guardados para {ciudad}")
except IOError as e:
    print(f"Error al escribir en {nombre_fichero}: {e}")
```

-----

### El Robot de Automatización: GitHub Actions al Rescate 🤖

Aquí viene la magia: ¿cómo hacer que este script se ejecute solo todos los días sin tener un servidor encendido? La respuesta es **GitHub Actions**, el motor de automatización integrado en GitHub. Es como tener un pequeño robot que trabaja gratis para nosotros.

**La Seguridad Primero: ¡Nunca Subas tu API Key\!**
El error más grave sería subir `registrar_clima.py` con la `API_KEY` escrita directamente. Cualquiera podría verla en GitHub.

  * **Solución**: Usar los **Secretos de Repositorio** de GitHub.
    1.  Ve a `Settings > Secrets and variables > Actions` en tu repositorio de GitHub.
    2.  Crea un nuevo secreto llamado `OPENWEATHER_API_KEY` y pega ahí tu clave.
    3.  En el script Python, lee la clave de forma segura usando `os.environ.get("OPENWEATHER_API_KEY")`.

**El Cerebro del Robot: El Fichero `.github/workflows/actualizar-clima.yml`**
Este fichero YAML le dice a GitHub Actions qué hacer y cuándo:

```yaml
name: Actualizar Datos Climáticos Diarios

on:
  workflow_dispatch: # Permite lanzarlo manualmente desde GitHub
  push:
    branches: [ main ] # Se lanza si subimos cambios a la rama main
  schedule:
    - cron: '0 6 * * *' # La clave: se lanza cada día a las 6:00 UTC

jobs:
  actualizar_datos:
    runs-on: ubuntu-latest # Usamos una máquina virtual Linux gratuita
    steps:
      - name: Checkout del código del repositorio
        uses: actions/checkout@v4 # Descarga nuestro código

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10' # O la versión que prefieras

      - name: Instalar dependencias necesarias
        run: pip install -r requirements.txt # Lee requirements.txt e instala requests, etc.

      - name: Ejecutar el script de recolección de datos
        run: python registrar_clima.py # ¡La acción principal!
        env:
          OPENWEATHER_API_KEY: ${{ secrets.OPENWEATHER_API_KEY }} # Inyectamos el secreto de forma segura

      - name: Guardar los nuevos datos en el repositorio (Commit & Push)
        run: |
          git config user.name 'github-actions[bot]' # Identifica al 'bot'
          git config user.email 'github-actions[bot]@users.noreply.github.com'
          git add datos/*.csv # Añade SOLO los ficheros CSV modificados en la carpeta 'datos'
          # Comprueba si hay cambios antes de hacer commit para evitar commits vacíos
          git diff --staged --quiet || git commit -m "Actualización automática de datos climáticos 🤖"
          git push # Sube los cambios al repositorio
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Token automático para permitir el push
```

**¡Este último paso es crucial\!** La propia Action actúa como un usuario, haciendo `git add`, `git commit` y `git push` de los ficheros CSV que el script Python acaba de modificar. Así, los datos actualizados quedan guardados en nuestro repositorio cada día.

---

### La Alternativa Serverless: Despliegue y Automatización con Netlify 🚀

Aunque GitHub Actions es una herramienta fantástica para la automatización, para este proyecto he decidido explorar una alternativa aún más integrada con el concepto de "serverless": **Netlify**. Netlify no solo nos permite desplegar nuestro frontend estático (como GitHub Pages), sino que también ofrece funciones serverless y, lo que es clave para nuestro backend, **funciones de ejecución programadas (Scheduled Functions o Cron Jobs)**.

#### Desplegando el Frontend Estático con Netlify

1.  **Conectar tu Repositorio**: El proceso es increíblemente sencillo. Inicia sesión en Netlify, haz clic en "Add new site" y selecciona "Import an existing project". Conecta con tu cuenta de GitHub y elige el repositorio de tu proyecto Weather Service.
2.  **Configuración Básica**: Netlify detectará automáticamente tu proyecto. Asegúrate de que la "Build command" esté vacía (ya que es un sitio estático sin proceso de build) y que el "Publish directory" sea la raíz de tu repositorio (`./`).
3.  **Despliegue Continuo**: Netlify configurará automáticamente el despliegue continuo. Cada vez que hagas un `git push` a la rama `main` (o la que hayas configurado), Netlify reconstruirá y desplegará tu sitio.

#### Automatizando el Backend con Netlify Functions (y Cron Jobs)

Aquí es donde Netlify Serverless Functions brillan para nuestro recolector de datos. En lugar de un flujo de GitHub Actions, podemos usar una función de Netlify para ejecutar nuestro script Python de forma programada:

1.  **Estructura del Proyecto**: Crea una carpeta `netlify/functions/` en la raíz de tu proyecto. Dentro, puedes tener un archivo Python como `collect_weather.py`.
2.  **Manejo de Dependencias**: Necesitarás un `requirements.txt` en la raíz de tu proyecto para que Netlify instale las dependencias Python (`requests`, `pandas`, `scikit-learn`).
3.  **Configuración de `netlify.toml`**: Este archivo en la raíz de tu proyecto es crucial para definir tus funciones y sus programaciones:

    ```toml
    [build]
      publish = "." # Directorio donde está tu index.html
      command = "" # No necesitamos un comando de build para un sitio estático

    [functions]
      directory = "netlify/functions" # Donde están tus funciones
      node_bundler = "esbuild" # Para funciones JS/TS. Netlify detectará Python.

    [[edge_functions]] # Para programar una función (requiere Netlify Edge Functions)
      function = "collect_weather" # El nombre de tu función (sin la extensión .py)
      path = "/.netlify/functions/collect_weather" # La ruta de la función (puede ser diferente)
      schedule = "@daily" # O usa un cron string como "0 6 * * *"
    ```

4.  **La Función Python (`netlify/functions/collect_weather.py`)**: Esta función encapsulará la lógica de tu `registrar_clima.py`. Netlify la ejecutará en un entorno Python.

    ```python
    # netlify/functions/collect_weather.py
    import json
    import requests
    import os
    import time
    from datetime import datetime
    import csv

    # ... (todo el código de tu script registrar_clima.py va aquí) ...
    # Asegúrate de que las API_KEYs se leen de os.environ
    # y que los datos se escriben directamente en el repositorio usando GitPython
    # o de alguna manera que Netlify pueda persistir los cambios.
    # **Importante**: Netlify Functions son efímeras.
    # Para persistir cambios en el repo, necesitarías una integración con Git
    # similar a lo que haría GitHub Actions (usando un Personal Access Token).
    # Sin embargo, para un frontend estático, lo más simple es que esta función
    # solo genere un JSON de predicciones y lo suba a un storage como S3,
    # o que el script Python de recolección siga ejecutándose en GitHub Actions
    # y Netlify solo sirva el frontend.
    # Si la idea es que Netlify TAMBIÉN haga el commit, esto es más complejo
    # y requeriría una API de Git o un token PAT desde Netlify.

    def handler(event, context):
        # Aquí iría la llamada principal a tu lógica de recolección de datos
        # Esto es un ejemplo simplificado
        try:
            # Tu lógica para obtener y guardar datos, generar CSVs/JSONs
            # Si quieres que esto haga commit a GitHub, necesitarías:
            # 1. Un token PAT de GitHub guardado como variable de entorno en Netlify.
            # 2. Una librería como GitPython para interactuar con Git.
            # Es más común que las funciones serverless persistan datos en bases de datos
            # o servicios de almacenamiento de objetos (ej. S3), no en el propio repo Git.
            
            # Para este proyecto, el enfoque con GitHub Actions para el backend
            # que hace el commit directamente al repo sigue siendo más sencillo
            # para el almacenamiento en CSV. Netlify sería ideal para el frontend
            # y funciones para APIs en tiempo real o predicciones ligeras.

            print("Función de Netlify para recolección de clima ejecutada.")
            # Si la función genera algún output JSON para el frontend, lo devolvería aquí:
            # return {
            #     "statusCode": 200,
            #     "body": json.dumps({"message": "Data collection complete"}),
            # }
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "La lógica de backend se ejecutaría aquí. Para persistir datos en GitHub, GitHub Actions es más directo."}),
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)}),
            }
    ```

5.  **Variables de Entorno en Netlify**: Para la `OPENWEATHER_API_KEY`, ve a `Site settings > Build & deploy > Environment variables` y añade tu clave allí.

**Consideración Importante**: Para que la función de Netlify persista los cambios directamente en tu repositorio de GitHub (como el commit de los CSV), necesitarías una configuración más avanzada (como usar un Personal Access Token de GitHub dentro de la función de Netlify para hacer `git push`), lo cual es más complejo. Para mantener la simplicidad y el almacenamiento directo en el repositorio Git con commits automáticos de los CSVs, la solución de **GitHub Actions sigue siendo la más directa y eficiente para el backend recolector de datos en este caso específico**. Netlify es excelente para el despliegue del frontend y para funciones que interactúan con servicios externos o bases de datos sin hacer `commit` al propio repositorio de la aplicación principal.

En este proyecto, usamos GitHub Actions para el backend (recolección y commit de CSVs) y Netlify para el despliegue del frontend y, potencialmente, funciones más ligeras o en tiempo real que no necesiten modificar el repo Git.

---

**¡Este último paso es crucial\!** La propia Action actúa como un usuario, haciendo `git add`, `git commit` y `git push` de los ficheros CSV que el script Python acaba de modificar. Así, los datos actualizados quedan guardados en nuestro repositorio cada día.

-----

### El Problema de Escalar (y el Pivote de Arquitectura Necesario)

Mi idea inicial era monitorizar unas 1000 ciudades y guardar todo en un único fichero `datos_climaticos.csv`. Hice un cálculo rápido: 1000 ciudades \* \~200 bytes/día \* 365 días \* 3 años... ¡más de 200 MB\! 😱

**¿Por qué es un problema?** Porque el frontend (nuestro dashboard, que veremos en el próximo post) se ejecuta en el navegador del usuario. Tendría que descargar esos 200 MB *completos* solo para mostrar el gráfico de *una* ciudad. Totalmente inaceptable en términos de rendimiento. 🐢

**La Solución Arquitectónica:** Cambiar a una estrategia de **"un fichero por entidad"**.

  * Creamos una carpeta `datos/`.
  * El script `registrar_clima.py` ahora genera (o añade datos a) un fichero CSV por cada ciudad: `datos/Madrid.csv`, `datos/León.csv`, `datos/Tokio.csv`, etc.

Así, cuando el usuario quiera ver el tiempo de León, el frontend solo descargará el fichero `datos/León.csv`, que pesará unos pocos kilobytes. ¡La carga es instantánea\! ✨

**Segundo Obstáculo de Escalado (Límites de API):** OpenWeatherMap, en su plan gratuito, permite unas 60 llamadas por minuto. Mi bucle para obtener datos de 155 ciudades (mi lista actual) las haría demasiado rápido.

  * **Solución Vital:** Añadir `import time` al inicio del script Python y `time.sleep(1.1)` al final del bucle `for ciudad in ciudades:`. Esto introduce una pausa de poco más de 1 segundo entre cada llamada a la API, asegurando que nos mantenemos por debajo del límite y evitamos que nos bloqueen. 🚦

-----

### Conclusión (Parte 1)

¡Ya tenemos la base\! Hemos construido un sistema robusto y automático que:

  * Se conecta a una API externa de forma segura.
  * Procesa y almacena datos históricos de múltiples entidades (ciudades).
  * Se ejecuta solo cada día, sin coste alguno, gracias a GitHub Actions.
  * Está diseñado para escalar de forma eficiente.

En el próximo post, nos pondremos el sombrero de desarrollador frontend y construiremos el dashboard interactivo que permitirá a cualquier usuario explorar estos datos con gráficos dinámicos. ¡No te lo pierdas\!

---

### Referencias y Enlaces de Interés:

* **Servicio Web Completo**: Puedes ver el resultado final de este proyecto en acción aquí: [https://datalaria.com/apps/weather/](https://datalaria.com/apps/weather/)
* **Repositorio GitHub del Proyecto**: Explora el código fuente y la estructura del proyecto en mi repositorio: [https://github.com/Dalaez/app_weather](https://github.com/Dalaez/app_weather)
* **OpenWeatherMap**: Documentación de la API de clima: [https://openweathermap.org/api](https://openweathermap.org/api)
* **Python Requests**: Documentación de la librería para hacer peticiones HTTP: [https://requests.readthedocs.io/en/master/](https://requests.readthedocs.io/en/master/)
* **GitHub Actions**: Guía oficial de GitHub Actions: [https://docs.github.com/es/actions](https://docs.github.com/es/actions)
* **Netlify**: Página oficial de Netlify: [https://www.netlify.com/](https://www.netlify.com/)