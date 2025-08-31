---
title: "De una Idea a una App Funcional en Minutos: Creando un Conversor de Ficheros con Gemini y GitHub Pages"
date: 2025-08-29
draft: False
categories: ["Proyectos", "Herramientas"]
tags: ["gemini", "ia", "desarrollo web", "github pages", "javascript", "html", "css", "low-code"]
image: gemini_code_canvas.png
description: "Crónica de un experimento práctico: cómo utilicé la Pizarra de Código de Gemini 1.5 Pro para generar, depurar y desplegar una aplicación web funcional en GitHub Pages."
summary: "Tenía una idea para una app, pero en lugar de abrir un editor de código, abrí una conversación con Gemini. Te cuento el proceso paso a paso de cómo la IA generó una aplicación de conversión de formatos y cómo la publiqué gratis para que cualquiera pueda usarla."
---

Todos hemos tenido esa idea fugaz: "Ojalá existiera una pequeña herramienta que hiciera X". En mi caso, era un conversor de formatos de archivo sencillo, online y que no requiriera subir mis ficheros a un servidor desconocido. Tradicionalmente, incluso una idea "sencilla" como esta implicaba abrir un editor de código, crear ficheros HTML, CSS, JavaScript, depurar, y finalmente, buscar un hosting.

Hoy, ese proceso ha cambiado radicalmente. En este post, voy a contaros el viaje de cómo esa idea se convirtió en una **aplicación web funcional y pública en cuestión de minutos**, utilizando únicamente dos herramientas: la asombrosa capacidad de generación de código de **Gemini 1.5 Pro** y la simplicidad de **GitHub Pages**.

El resultado final, antes de empezar, lo podéis probar aquí: **[Enlace a tu App en GitHub Pages]**

### El Desafío: Un Conversor de Ficheros Universal en el Navegador

El objetivo era claro: crear una aplicación web de una sola página que permitiera a un usuario arrastrar un fichero (una imagen, un documento) y convertirlo a otro formato (por ejemplo, de PNG a JPG, o de DOCX a PDF) directamente en su navegador. La clave era que todo el procesamiento debía ocurrir en el lado del cliente, garantizando la **privacidad y la velocidad**.

Este es un caso de uso perfecto para poner a prueba a una IA, ya que requiere la creación coordinada de tres componentes:
1.  **HTML**: Para la estructura y los elementos de la interfaz (caja para subir archivos, menús, botones).
2.  **CSS**: Para darle un aspecto limpio y usable.
3.  **JavaScript**: El cerebro de la operación, encargado de la lógica de conversión.

### La Conversación con Gemini: Desarrollo Asistido en la "Pizarra"

En lugar de escribir código, empecé a escribir un prompt. La funcionalidad de "Pizarra" o *Code Canvas* de Gemini no es un simple chat que te devuelve texto; es un entorno interactivo que te presenta el código organizado y una vista previa en tiempo real.

**1. El Prompt Inicial:**
Mi primera petición fue directa y clara, definiendo todos los requisitos:

> "Genera el código HTML, CSS y JavaScript para una aplicación web de una sola página que funcione como un conversor de formatos de archivo. La interfaz debe tener un área para arrastrar y soltar archivos, un menú desplegable para seleccionar el formato de salida y un botón de descarga. Todo el procesamiento debe hacerse en el lado del cliente para asegurar la privacidad."

**2. La Pizarra en Acción:**
En menos de un minuto, Gemini no solo generó el código, sino que lo presentó en una interfaz organizada con pestañas para HTML, CSS y JS, y una ventana de previsualización que mostraba la aplicación funcionando. Es como tener a un desarrollador senior a tu lado, materializando tus ideas al instante.

![Screenshot de la interfaz de código de Gemini (Pizarra / Code Canvas)](gemini_app_preview.png)

**3. Refinamiento Iterativo:**
El primer resultado era funcional, pero visualmente muy básico. Aquí es donde la naturaleza conversacional brilla. En lugar de editar el CSS a mano, simplemente le pedí:

> "Excelente. Ahora, aplica un estilo más moderno y limpio. Usa un tema oscuro, centra los elementos verticalmente y haz que el botón de 'Convertir' tenga una animación sutil al pasar el ratón por encima."

Tras un par de ajustes más, tenía un producto pulido y listo. Todo el proceso, desde el prompt inicial hasta el código final, quedó registrado en esta conversación pública de Gemini que podéis consultar: **[Enlace a tu conversación compartida de Gemini]**

### Del Código a la Realidad: Despliegue Mágico con GitHub Pages

Tener el código es solo la mitad del camino. La otra mitad es publicarlo para que el mundo pueda usarlo. Aquí es donde entra GitHub Pages, un servicio gratuito que convierte un repositorio de código en un sitio web en vivo.

El proceso es increíblemente sencillo:

1.  **Crear un Repositorio en GitHub**: Creé un nuevo repositorio público llamado, por ejemplo, `file-converter-app`.
2.  **Subir los Ficheros**: Añadí tres ficheros al repositorio: `index.html`, `style.css` y `script.js`, y pegué en cada uno el código que Gemini había generado.
3.  **Activar GitHub Pages**: Este es el paso "mágico". En la configuración del repositorio, fui a la sección "Pages", seleccioné la rama `main` como fuente y guardé. En menos de un minuto, GitHub me proporcionó una URL pública donde mi aplicación ya estaba funcionando.

![Screenshot de la configuración de GitHub Pages](github_pages_settings.png)

### Conclusión: La Nueva Era del Desarrollo Asistido por IA

Este experimento, que duró menos de una hora, es una ventana al futuro (y presente) del desarrollo de software. No se trata de que la IA vaya a reemplazar a los desarrolladores, sino de que va a **potenciar a los creadores**. Ha reducido drásticamente la barrera de entrada para construir herramientas útiles.

Herramientas como la Pizarra de Código de Gemini son un acelerador sin precedentes para:
* **Prototipar ideas** a una velocidad impensable.
* **Aprender a programar**, viendo en tiempo real cómo un experto (la IA) estructura el código.
* **Construir utilidades personales y proyectos pequeños** sin necesidad de un equipo o un presupuesto.

Te animo a que pienses en esa pequeña herramienta que siempre has querido y se lo pidas a Gemini. El poder de crear ya no está solo en saber escribir código, sino en saber formular las preguntas correctas.

---

#### Fuentes y Recursos:
* **Prueba la App**: [Conversor de Ficheros (desplegado en GitHub Pages)](https://tu-usuario-github.github.io/file-converter-app/)
* **Conversación con Gemini**: [Consulta aquí el proceso de creación de la App](https://g.co/gemini/share/e7ea383f7c14)
* **GitHub Pages**: [Documentación oficial para empezar](https://pages.github.com/)
* **Gemini de Google**: [Página oficial](https://gemini.google.com/)