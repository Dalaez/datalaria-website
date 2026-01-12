---
title: "Proyecto Weather Service (Parte 2): Construyendo el Frontend Interactivo con GitHub Pages o Netlify y JavaScript"
date: 2025-11-08
draft: False
categories: ["Proyectos", "Herramientas"]
tags: ["javascript", "frontend", "github pages", "html", "css", "papaparse", "chartjs", "serverless", "visualizacion-datos", "netlify"]
image: cover.png
description: "Segunda entrega del proyecto Weather Service. Nos adentramos en el frontend: sirviendo un dashboard dinámico con GitHub Pages o Netlify, leyendo datos CSV con PapaParse.js y creando gráficos interactivos con Chart.js."
summary: "Después de construir el recolector de datos, ¡es hora de visualizarlos! Este post te guía a través de la creación de un dashboard meteorológico interactivo usando GitHub Pages o Netlify, JavaScript, PapaParse.js y Chart.js. ¡Dale vida a tus datos!"
---

En la [primera parte de esta serie](/blog/weather-service-part-1-backend), sentamos las bases de nuestro servicio meteorológico global. Construimos un script de Python para obtener datos del clima de OpenWeatherMap, los almacenamos eficientemente en ficheros CSV separados por ciudad y automatizamos todo el proceso de recolección utilizando GitHub Actions. Nuestro "robot" está diligentemente recopilando datos 24/7.

Pero, ¿de qué sirven los datos si no puedes verlos? Hoy, cambiamos nuestro enfoque al **frontend**: la construcción de un dashboard interactivo y fácil de usar que permita a cualquiera explorar los datos meteorológicos que hemos recopilado. Aprovecharemos el poder del alojamiento de sitios estáticos con **GitHub Pages o Netlify**, utilizaremos **JavaScript** "vainilla" para darle vida y nos apoyaremos en algunas excelentes librerías para el manejo y la visualización de datos. ¡Hagamos que nuestros datos brillen!

![Conceptual image of Weather Service Frontend](AI_App_Weather_Image_Frontend.png)

---

### Alojamiento Web Gratuito: GitHub Pages vs. Netlify

El primer obstáculo para cualquier proyecto web es el alojamiento. Los servidores tradicionales pueden ser costosos y complejos de gestionar. Siguiendo nuestra filosofía "serverless y gratis", tanto **GitHub Pages** como **Netlify** son soluciones perfectas para alojar sitios web estáticos directamente desde tu repositorio de GitHub.

#### Opción 1: GitHub Pages

Permite alojar sitios web estáticos directamente desde tu repositorio de GitHub.

**La activación es trivial:**
1.  Ve a `Settings > Pages` en tu repositorio.
2.  Selecciona tu rama `main` (o la rama que contenga tu contenido web) como fuente.
3.  Elige la carpeta `/root` (o una carpeta `/docs` si lo prefieres) como la ubicación de tus archivos web.
4.  Haz clic en `Save`.

Y así, tu archivo `index.html` (y cualquier recurso vinculado) se vuelve accesible públicamente en una URL como `https://tu-usuario.github.io/tu-nombre-de-repositorio/`. ¡Sencillo, efectivo y gratuito\! 🚀

#### Opción 2: Netlify (¡la elección final para este proyecto!)

Para este proyecto, finalmente he optado por **Netlify** por su flexibilidad, la facilidad para gestionar dominios personalizados y su integración con el despliegue continuo. Además, me permite alojar el proyecto directamente bajo mi dominio de Datalaria (`https://datalaria.com/apps/weather/`).

**Pasos para desplegar en Netlify:**

1.  **Conectar tu Repositorio**: Inicia sesión en Netlify. Haz clic en "Add new site" y luego en "Import an existing project". Conecta tu cuenta de GitHub y selecciona el repositorio de tu proyecto Weather Service.
2.  **Configuración de Despliegue**:
    * **Owner**: Tu cuenta de GitHub.
    * **Branch to deploy**: `main` (o la rama donde tengas tu código frontend).
    * **Base directory**: Deja esto vacío si tu `index.html` y assets están en la raíz del repositorio, o especifica una subcarpeta si es el caso (ej., `/frontend`).
    * **Build command**: Déjalo vacío, ya que nuestro frontend es puramente estático sin necesidad de un paso de build (sin frameworks como React/Vue).
    * **Publish directory**: `.` (o la subcarpeta que contenga tus archivos estáticos, ej., `/frontend`).
3.  **Desplegar Sitio**: Haz clic en "Deploy site". Netlify tomará tu repositorio, lo desplegará y te proporcionará una URL aleatoria.
4.  **Dominio Personalizado (Opcional pero recomendado)**: Para usar un dominio como `datalaria.com/apps/weather/`:
    * Ve a `Site settings > Domain management > Domains > Add a custom domain`.
    * Sigue los pasos para añadir tu dominio y configurarlo con los DNS de tu proveedor (añadiendo registros `CNAME` o `A`).
    * Para la ruta específica (`/apps/weather/`), necesitarás configurar una "subcarpeta" o "base URL" en tu aplicación si no está directamente en la raíz del dominio. En este caso, nuestro `index.html` está diseñado para ser servido desde una subruta. Netlify gestiona esto de forma transparente una vez que el sitio está desplegado y tu dominio configurado.
    
¡Así de sencillo! Cada `git push` a tu rama configurada activará un nuevo despliegue en Netlify, manteniendo tu dashboard siempre actualizado.

---

### La Pila Tecnológica del Frontend: HTML, CSS y JavaScript (con una pequeña ayuda)

Para este dashboard, opté por un enfoque ligero: HTML puro para la estructura, un poco de CSS para los estilos y **JavaScript "vainilla"** (sin frameworks complejos) para la interactividad. Para manejar tareas específicas, incorporé dos librerías fantásticas:

1.  [**PapaParse.js**](https://www.papaparse.com/): El mejor parser de CSV del lado del cliente para el navegador. Es el puente entre nuestros archivos CSV en bruto y las estructuras de datos de JavaScript que necesitamos para la visualización.
2.  [**Chart.js**](https://www.chartjs.org/): Una potente y flexible librería de gráficos JavaScript que facilita enormemente la creación de gráficos bonitos, responsivos e interactivos.

---

### La Lógica del Dashboard: Dando Vida a los Datos en `index.html`

Nuestro `index.html` actúa como el lienzo principal, orquestando la obtención, el parseo y la representación de los datos meteorológicos.

#### 1. Carga Dinámica de Ciudades

En lugar de codificar una lista de ciudades, queremos que nuestro dashboard se actualice automáticamente si añadimos nuevas ciudades en el backend. Lo logramos obteniendo un simple archivo `ciudades.txt` (que contiene un nombre de ciudad por línea) y poblando dinámicamente un elemento desplegable `<select>` utilizando la API `fetch` de JavaScript.

```javascript
const citySelector = document.getElementById('citySelector');
let myChart = null; // Variable global para almacenar la instancia de Chart.js

async function cargarListaCiudades() {
    try {
        const response = await fetch('ciudades.txt');
        const text = await response.text();
        // Filtramos las líneas vacías del archivo de texto
        const ciudades = text.split('\n').filter(line => line.trim() !== '');

        ciudades.forEach(ciudad => {
            const option = document.createElement('option');
            option.value = ciudad;
            option.textContent = ciudad;
            citySelector.appendChild(option);
        });

        // Cargamos la primera ciudad por defecto al inicio de la página
        if (ciudades.length > 0) {
            cargarYDibujarDatos(ciudades[0]);
        }
    } catch (error) {
        console.error('Error cargando la lista de ciudades:', error);
        // Opcional: Mostrar un mensaje de error amigable al usuario
    }
}

// Disparamos la carga de ciudades cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', cargarListaCiudades);
```

#### 2. Reacción a la Selección del Usuario

Cuando un usuario selecciona una ciudad del desplegable, necesitamos responder de inmediato. Un `addEventListener` en el elemento `<select>` detecta el evento `change` y llama a nuestra función principal para obtener y dibujar los datos de la ciudad recién seleccionada.

```javascript
citySelector.addEventListener('change', (event) => {
    const ciudadSeleccionada = event.target.value;
    cargarYDibujarDatos(ciudadSeleccionada);
});
```

#### 3. Obtención, Parseo y Dibujado de Datos

Esta es la función central donde todo cobra vida. Es responsable de:

  * Construir la URL para el archivo CSV específico de la ciudad (ej., `datos/León.csv`).
  * Utilizar `Papa.parse` para descargar y procesar el contenido del CSV directamente en el navegador. PapaParse maneja la obtención y el parseo asíncronos, lo que lo hace increíblemente fácil.
  * Extraer las `etiquetas` (fechas) y los `datos` (temperaturas) relevantes del CSV parseado para Chart.js.
  * **¡Crucial\!**: Antes de dibujar un nuevo gráfico, debemos **destruir la instancia anterior de Chart.js** (`if (myChart) { myChart.destroy(); }`). ¡Olvidar este paso lleva a gráficos superpuestos y problemas de rendimiento! 💥
  * Crear una nueva instancia de `Chart()` con los datos actualizados.
  * Adicionalmente, llama a una función para cargar y mostrar la predicción de IA para esa ciudad, integrándola sin problemas en el dashboard.

```javascript
function cargarYDibujarDatos(ciudad) {
    const csvUrl = `datos/${ciudad}.csv`; // Nota la carpeta 'datos/' de la Parte 1
    const ctx = document.getElementById('weatherChart').getContext('2d');

    Papa.parse(csvUrl, {
        download: true, // Indica a PapaParse que descargue el archivo
        header: true,   // Trata la primera fila como encabezados
        skipEmptyLines: true,
        complete: function(results) {
            const datosClimaticos = results.data;

            // Extraer etiquetas (fechas) y datos (temperaturas)
            const etiquetas = datosClimaticos.map(fila => fila.fecha_hora.split(' ')[0]); // Extraer solo la fecha
            const tempMax = datosClimaticos.map(fila => parseFloat(fila.temp_max_c));
            const tempMin = datosClimaticos.map(fila => parseFloat(fila.temp_min_c));

            // Destruir la instancia de gráfico anterior si existe para evitar superposiciones
            if (myChart) {
                myChart.destroy();
            }

            // Crear una nueva instancia de Chart.js
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: etiquetas,
                    datasets: [{
                        label: `Temp Máx (°C) - ${ciudad}`,
                        data: tempMax,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }, {
                        label: `Temp Mín (°C) - ${ciudad}`,
                        data: tempMin,
                        borderColor: 'rgb(54, 162, 235)',
                        tension: 0.1
                    }]
                },
                options: { // Opciones del gráfico para responsividad, título, etc.
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: false } },
                    plugins: { legend: { position: 'top' }, title: { display: true, text: `Datos Históricos del Clima para ${ciudad}` } }
                }
            });

            // Cargar y mostrar la predicción de IA
            cargarPrediccion(ciudad);
        },
        error: function(err, file) {
            console.error("Error al parsear el CSV:", err, file);
            // Opcional: mostrar un mensaje de error amigable en el dashboard
            if (myChart) { myChart.destroy(); } // Limpiar gráfico si falla la carga
        }
    });
}
```

#### 4. Mostrar Predicciones de IA

La integración de las predicciones de IA (en las que profundizaremos en la Parte 3) también se gestiona desde el frontend. El backend genera un archivo `predicciones.json`, y nuestro JavaScript simplemente obtiene este JSON, encuentra la predicción para la ciudad seleccionada y la muestra.

```javascript
async function cargarPrediccion(ciudad) {
    const predictionElement = document.getElementById('prediction');
    try {
        const response = await fetch('predicciones.json');
        const predicciones = await response.json();
        if (predicciones && predicciones[ciudad]) {
             predictionElement.textContent = `Predicción de Temp. Máx. para mañana: ${predicciones[ciudad].toFixed(1)}°C`;
        } else {
             predictionElement.textContent = 'Predicción no disponible.';
        }
    } catch (error) {
         console.error('Error cargando predicciones:', error);
         predictionElement.textContent = 'Error al cargar la predicción.';
    }
}
```

---

### Conclusión (Parte 2)

¡Hemos transformado los datos en bruto en una experiencia atractiva e interactiva! Al combinar el alojamiento estático de GitHub Pages o Netlify, JavaScript "vainilla" para la lógica, PapaParse.js para el manejo de CSV y Chart.js para visualizaciones hermosas, hemos construido un frontend potente que es a la vez gratuito y muy efectivo.

El dashboard ahora proporciona información inmediata sobre los patrones climáticos históricos de cualquier ciudad seleccionada. Pero, ¿qué pasa con el futuro? En la **tercera y última parte de esta serie**, nos adentraremos en el emocionante mundo del **Machine Learning** para añadir una capa predictiva a nuestro servicio. Exploraremos cómo usar datos históricos para pronosticar el tiempo de mañana, convirtiendo nuestro servicio en un verdadero "oráculo" meteorológico. ¡No te lo pierdas!

---

### Referencias y Enlaces de Interés:

  * **Servicio Web Completo**: Puedes ver el resultado final de este proyecto en acción aquí: [https://datalaria.com/apps/weather/](https://datalaria.com/apps/weather/)
  * **Repositorio GitHub del Proyecto**: Explora el código fuente y la estructura del proyecto en mi repositorio: [https://github.com/Dalaez/app_weather](https://github.com/Dalaez/app_weather)
  * **PapaParse.js**: Parser de CSV rápido en el navegador para JavaScript: [https://www.papaparse.com/](https://www.papaparse.com/)
  * **Chart.js**: Gráficos JavaScript simples pero flexibles para diseñadores y desarrolladores: [https://www.chartjs.org/](https://www.chartjs.org/)
  * **GitHub Pages**: Documentación oficial sobre cómo alojar tus sitios: [https://docs.github.com/es/pages](https://docs.github.com/es/pages)
  * **Netlify**: Página oficial de Netlify: [https://www.netlify.com/](https://www.netlify.com/)