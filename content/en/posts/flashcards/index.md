---
title: "Flashcards"
date: 2025-11-10
draft: False
categories: ["Proyectos", "Herramientas"]
tags: ["gemini", "ia", "desarrollo web", "conversor de unidades", "html", "css", "javascript", "ingeniería"]
image: conversor_universal_pro.png
description: "Un caso práctico de cómo utilicé Gemini Canvas para desarrollar desde cero una aplicación web de conversión de unidades de medida, organizada por categorías y adaptada a mis necesidades profesionales."
summary: "Cansado de tener que desempolvar conocimientos casi olvidados o tener que recurrir a diferentes conversores online genéricos, decidí crear un conversor propio con la ayuda de la IA de Gemini. Te cuento el proceso y te explico la ciencia detrás de cada conversión, desde la energía hasta la radiofrecuencia."
---

En cualquier disciplina técnica o de ingeniería, nuestro día a día está lleno de pequeñas pero constantes tareas de conversión de unidades de medida. Pasamos de Pascales a PSI, de Kilovatios a Caballos de potencia, de Gigabytes a Terabytes o de frecuencias a longitudes de onda.. En mi etapa universitaria disponíamos de las llamadas *chuletas* o *cheatsheets*, las cuales solíamos tener a mano ya sea pegadas a las calculadoras, carpetas, cuadernos... para nuestro día a día (no para los exámenes por supuesto 😄). Una vez ya en el ámbito profesional y con la proliferación de todo tipo de Apps y páginas web, actualmente ya no es necesario tirar de estos recursos dado que tenemos multitud de opciones disponibles que nos permiten rápidamente consultar cualquier conversión o unidad de medida por rara que sea.

No obstante, ante tal maremagnum de opciones y siendo esta una tarea tan recurrente y necesaria, me planteé un reto: ¿podría crear mi propio conversor de unidades? Uno que fuera rápido, limpio, visualmente atractivo y, sobre todo, **un proyecto vivo**, una especie de "navaja suiza digital" que pudiera ampliar con el tiempo según mis necesidades personales y profesionales. La respuesta, como en otros proyectos del blog, la encontré en la IA. Este post es la descripción de mi conversor de unidades propio recogiendo su desarrollo desde cero y apoyado en la funcionalidad **Canvas de Gemini** para crear una aplicación web con múltiples páginas y categorías.

![Imagen conceptual de la aplicación Conversor Universal Pro](navaja_conversor.png)

### El Proceso: De la Idea a la concepción

El objetivo era crear una aplicación web moderna, intuitiva con una navegación clara por categorías, fluida y fácil de usar. En lugar de empezar a escribir código desde cero, inicié una conversación con Gemini, describiendo mi visión:

> "Crea la estructura de una aplicación web de varias páginas HTML. La aplicación será un conversor de formatos y unidades de medida. La página principal debe mostrar tarjetas para las categorías: Dimensión, Energía, Tiempo, Mecánica, Informática y Radiofrecuencia con conversiones básicas. Cada tarjeta debe enlazar a una página de conversión dedicada a la categoría correspondiente desde una página de inicio donde además de las tarjetas de navegación a cada categoría debe haber un conversor de formato de símbolo "." y "," para miles y decimales en números"

La funcionalidad Canvas de Gemini me permitió ver en tiempo real cómo la IA generaba no solo el código, sino la estructura completa del proyecto. A partir del boceto inicial y tras un par de iteraciones adicionales centradas en refinar algo más el diseño y afinar las unidades utilizadas, vio la luz una primera versión operativa de la aplicación: [Mi aplicación de conversión de unidades de medida](https://dalaez.github.io/conversor-app/)

### Un Vistazo a las Categorías y sus Unidades

Lo que hace útil a una herramienta como esta es entender **qué estamos convirtiendo**. Por eso, el "Conversor Universal Pro" no solo calcula, sino que busca ser didáctico. Estas son las categorías iniciales y la ciencia detrás de sus unidades:

![Imagen de la página de inicio del Conversor Universal Pro](conversor-app.png)

#### 1. Dimensión: Midiendo el Espacio que Nos Rodea

![Imagen de la página de conversión de unidades de dimensión](dimension.png)

Esta categoría agrupa las medidas fundamentales del espacio físico.

* **Longitud:**
    * **¿Qué es?** Es la medida de una dimensión, la distancia entre dos puntos.
    * **¿Cómo se calcula?** Todas las conversiones se calculan tomando el **metro (m)** como unidad de referencia. La fórmula convierte el valor inicial a metros y luego a la unidad final.

* **Área:**
    * **¿Qué es?** Es la medida de una superficie bidimensional.
    * **¿Cómo se calcula?** De forma similar, el cálculo se estandariza usando el **metro cuadrado (m²)** como unidad base.

* **Volumen:**
    * **¿Qué es?** Es la medida del espacio que ocupa un objeto en tres dimensiones.
    * **¿Cómo se calcula?** La unidad base para el volumen en la aplicación es el **litro (l)**, facilitando la conversión entre unidades métricas y otras como los galones o las tazas.

#### 2. Energía: La Capacidad de Realizar un Trabajo

![Imagen de la página de conversión de unidades de energía](energia.png)

Aquí agrupamos las unidades que describen cómo se transfiere y se utiliza la energía.

* **Energía:**
    * **¿Qué es?** Es la capacidad de un sistema para realizar un trabajo.
    * **¿Cómo se calcula?** El **Julio (J)** es la unidad base del Sistema Internacional. A partir de él, se realizan las conversiones a calorías, vatios-hora, etc.

* **Potencia:**
    * **¿Qué es?** Es la velocidad a la que se transfiere la energía o se realiza un trabajo. No es lo mismo tener energía que poder usarla rápidamente.
    * **¿Cómo se calcula?** La unidad base es el **Vatio (W)**, que equivale a un Julio por segundo.

* **Temperatura:**
    * **¿Qué es?** Es una medida de la energía térmica o el calor de un cuerpo.
    * **¿Cómo se calcula?** A diferencia de otras, la temperatura no usa un factor de conversión simple. La aplicación utiliza fórmulas específicas, convirtiendo siempre la entrada a **grados Celsius (°C)** como paso intermedio para luego calcular la unidad de salida (Fahrenheit o Kelvin).

#### 3. Informática: El Mundo de los Bits y los Bytes

![Imagen de la página de conversión de unidades útiles en informática](informatica.png)

Las unidades que definen nuestro mundo digital.

* **Almacenamiento de Datos:**
    * **¿Qué es?** Mide la capacidad de guardar información digital.
    * **¿Cómo se calcula?** La unidad fundamental es el **Byte (B)**. Es importante destacar que en informática, los múltiplos no son decimales (x1000), sino binarios (x1024). Así, 1 Kilobyte son 1024 Bytes.

* **Ancho de Banda:**
    * **¿Qué es?** Mide la velocidad de transferencia de datos en una red.
    * **¿Cómo se calcula?** Su unidad base son los **bits por segundo (bps)**. En este caso, los múltiplos sí son decimales (kbps, mbps, gbps), ya que se refieren a la velocidad de transmisión, no al almacenamiento.

#### 4. Tiempo: Nuestra Dimensión Más Preciada

![Imagen de la página de conversión de unidades de tiempo](tiempo.png)

Aunque parece simple, la conversión de tiempo es fundamental en muchísimos cálculos.

* **Tiempo:**
    * **¿Qué es?** Es la magnitud que mide la duración o separación de los acontecimientos.
    * **¿Cómo se calcula?** Todas las unidades se convierten a la unidad base, el **segundo (s)**, para luego calcular el valor final en minutos, horas, días, etc.

#### 5. Mecánica: Las Fuerzas que Mueven el Mundo

![Imagen de la página de conversión de unidades de mecánica](mecanica.png)

Esta categoría es clave en ingeniería y física.

* **Masa:**
    * **¿Qué es?** Es la medida de la cantidad de materia de un cuerpo. No debe confundirse con el peso, que es la fuerza que ejerce la gravedad sobre esa masa.
    * **¿Cómo se calcula?** La unidad base es el **Kilogramo (kg)**.

* **Fuerza:**
    * **¿Qué es?** Es cualquier interacción que, sin oposición, cambia el movimiento de un objeto.
    * **¿Cómo se calcula?** Se utiliza el **Newton (N)** como unidad base, definido como la fuerza necesaria para proporcionar una aceleración de 1 m/s² a un objeto de 1 kg de masa.

* **Presión:**
    * **¿Qué es?** Es la fuerza aplicada perpendicularmente sobre una superficie.
    * **¿Cómo se calcula?** La unidad base es el **Pascal (Pa)**, que es igual a un Newton por metro cuadrado (N/m²).

#### 6. Radiofrecuencia: El Espectro Invisible

![Imagen de la página de conversión de unidades de radiofrecuencia](radiofrecuencia.png)

Fundamental para las telecomunicaciones.

* **Frecuencia:**
    * **¿Qué es?** Es el número de repeticiones de un fenómeno periódico por unidad de tiempo. En ondas, es el número de ciclos por segundo.
    * **¿Cómo se calcula?** Su unidad base es el **Hercio (Hz)**, que equivale a un ciclo por segundo.

* **Frecuencia a Longitud de Onda:**
    * **¿Qué es?** Esta es una conversión especial que relaciona la frecuencia de una onda electromagnética con su longitud de onda (la distancia entre dos crestas de la onda).
    * **¿Cómo se calcula?** No es una conversión directa, sino que utiliza una fórmula física: **λ = c / f**, donde **λ** es la longitud de onda, **f** es la frecuencia y **c** es la constante de la velocidad de la luz (299,792,458 m/s). La aplicación convierte la frecuencia a Hz, calcula la longitud de onda en metros y luego la convierte a la unidad de longitud deseada.

### Conclusión: Más Allá de una Herramienta, un Proyecto Vivo

El "Conversor Universal Pro" es el ejemplo perfecto de cómo gracias a la IA se pueden materializar ideas y recursos de gran utilidad para nuestro día día personal o profesional. El proceso, en este caso guiado por Gemini Canvas, fue increíblemente ágil y el resultado es una aplicación que no solo resuelve mis necesidades diarias, sino que también sirve como una plataforma de aprendizaje.

Mi objetivo es seguir ampliándola con nuevas categorías y unidades según surjan las necesidades. Esta es la nueva era del desarrollo de software personal: ya no dependemos de herramientas genéricas, sino que tenemos el poder de construir nuestras propias soluciones a medida, con un copiloto de IA que traduce nuestras ideas en código funcional.

---

#### Fuentes y Recursos:
* **Gemini**: [Página oficial de Gemini para probar su funcionalidad Canvas](https.gemini.google.com/app)
* **GitHub Page de la App**: [Mi aplicación de conversión de unidades de medida](https://dalaez.github.io/conversor-app/)