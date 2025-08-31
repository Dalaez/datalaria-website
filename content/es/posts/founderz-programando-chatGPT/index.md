---
title: "Programar sin Saber Programar: Mi Experiencia con el Curso de IA de Founderz y ChatGPT"
date: 2025-09-30
draft: False
categories: ["Herramientas", "Aprendizaje"]
tags: ["ia", "chatgpt", "prompt engineering", "founderz", "desarrollo web", "no-code", "html"]
image: chatgpt_app_creation.png
description: "Crónica de cómo el curso de IA y Prompt Engineering de Founderz me abrió los ojos a la posibilidad de crear aplicaciones web funcionales usando solo lenguaje natural con ChatGPT."
summary: "Siempre pensé que para crear una app se necesitaba ser programador. El curso de IA de Founderz me demostró lo contrario. Te cuento cómo, aplicando lo aprendido, creé un generador de contraseñas con ChatGPT en minutos."
---

Siempre he creído que una de las barreras más grandes entre una buena idea y su ejecución es el conocimiento técnico. En el mundo digital, esto a menudo se traduce en saber programar. ¿Cuántas veces hemos pensado en una pequeña utilidad o aplicación que nos facilitaría el día a día, solo para descartarla por la complejidad de su desarrollo?

Recientemente, esa percepción cambió por completo para mí. El catalizador fue el curso **[Introducción a la IA y Prompt Engineering de Founderz](https://founderz.com/es/programa/introduccion-a-la-ia-y-prompt-engineering)**, una formación que, más allá de la teoría, me proporcionó una revelación práctica: con las instrucciones adecuadas, cualquiera puede "programar" sin escribir una sola línea de código.

En este post quiero compartir esa revelación y mostraros un ejemplo práctico de cómo, aplicando las técnicas del curso, creé una aplicación funcional usando únicamente una conversación con ChatGPT.

### El "¡Ajá!" Moment del Curso de Founderz

El curso de Founderz es tremendamente didáctico, pero para mí, el punto de inflexión fue cuando dejaron de presentar a la IA (en su caso, Copilot y ChatGPT) como un simple asistente de búsqueda y la posicionaron como un **compañero de creación (un copiloto)**.

La idea de que podías dar instrucciones detalladas a un modelo de lenguaje para que generara no solo texto, sino código estructurado y funcional, fue un cambio de paradigma. Específicamente, el módulo que enseñaba a crear aplicaciones web autocontenidas en un solo fichero HTML fue el que me abrió los ojos al potencial real de esta tecnología para la creación rápida de prototipos y herramientas.

### El Desafío: Creando una Herramienta Útil desde Cero con ChatGPT

Para poner a prueba esta nueva habilidad, decidí crear una utilidad clásica que, sin embargo, siempre viene bien: un **generador de contraseñas seguras y personalizables**.

El objetivo era simple: una página web que me permitiera elegir la longitud de la contraseña y qué tipo de caracteres incluir (mayúsculas, minúsculas, números, símbolos), y que con un clic me la generara y me permitiera copiarla.

### La Receta: El Prompt Detallado es la Clave

Aquí es donde entra en juego el *Prompt Engineering*. No se trata de pedirle a ChatGPT "hazme una app", sino de actuar como un jefe de proyecto que le da a su desarrollador (la IA) unas especificaciones claras y detalladas.

Este fue el prompt que utilicé, inspirado en la metodología del curso:

> Actúa como un desarrollador web experto en frontend. Quiero crear una aplicación de una sola página para generar contraseñas seguras. El código debe estar en **un único fichero HTML** que incluya el CSS y el JavaScript internamente, para que sea fácil de guardar y ejecutar.
>
> **La interfaz debe tener:**
> 1. Un título que diga "Generador de Contraseñas Seguras".
> 2. Un campo de texto (solo lectura) donde se mostrará la contraseña generada.
> 3. Un botón para "Copiar" la contraseña al portapapeles.
> 4. Un control deslizante (slider) para seleccionar la longitud de la contraseña (de 8 a 32 caracteres).
> 5. Casillas de verificación (checkboxes) para incluir: Mayúsculas, Minúsculas, Números y Símbolos.
> 6. Un botón principal para "Generar Contraseña".
>
> **Funcionalidad:**
> * Al pulsar "Generar Contraseña", se debe crear una clave aleatoria según las opciones seleccionadas y mostrarla en el campo de texto.
> * El botón "Copiar" debe funcionar y, si es posible, mostrar un mensaje temporal de "¡Copiado!".
>
> **Estilo:**
> * Aplica un diseño limpio y moderno con un tema oscuro. Centra la aplicación en la página.

ChatGPT procesó la petición y, en segundos, me devolvió un único bloque de código que contenía todo lo solicitado.

### La "Magia": Tu App Funcionando en 30 Segundos

Esta es la parte más gratificante para alguien sin experiencia en desarrollo. ¿Cómo se "ejecuta" este código?

1.  **Abre un editor de texto plano** (como el Bloc de Notas en Windows o TextEdit en Mac).
2.  **Pega el código completo** que te ha proporcionado ChatGPT.
3.  **Guarda el fichero** con el nombre que quieras, pero asegurándote de que la extensión sea `.html` (por ejemplo: `generador.html`).
4.  **Haz doble clic en el fichero guardado.**

¡Y ya está! El fichero se abrirá en tu navegador web y tendrás una aplicación completamente funcional, creada por ti (o, mejor dicho, por ti y tu copiloto de IA).

![Mi generador de contraseñas creado con ChatGPT](password_generator_app.png)

### Conclusión y Próximos Pasos

Esta experiencia demuestra la increíble democratización que la IA está trayendo al mundo de la creación digital. Ya no es imprescindible ser un programador experto para construir herramientas sencillas y útiles. Lo que ahora es crucial es la habilidad de **pensar de forma estructurada y dar instrucciones claras**, la esencia del *Prompt Engineering*.

Este método es increíblemente rápido para crear y probar herramientas de uso personal. Pero, ¿cómo podemos llevarlo un paso más allá? ¿Cómo podemos publicar esta aplicación para que cualquiera en el mundo pueda usarla con un simple enlace, de forma gratuita y segura?

De eso hablaremos en el siguiente post, donde exploraremos el proceso de creación con una herramienta aún más potente, **la Pizarra de Código de Gemini**, y su despliegie público usando **GitHub Pages**.

---

#### Fuentes y Recursos:
* **Founderz**: [Curso de Introducción a la IA y Prompt Engineering](https://founderz.com/es/programa/introduccion-a-la-ia-y-prompt-engineering)
* **OpenAI**: [ChatGPT](https://chat.openai.com/)