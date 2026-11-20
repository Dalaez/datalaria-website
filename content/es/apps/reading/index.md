---
title: "Lector Arcade (Aprendizaje de Lectura)"
description: "Juego educativo interactivo y gamificado para el aprendizaje de la lectura, conciencia fonológica, sílabas y fluidez lectora en 6 niveles adaptativos."
app: "reading"
translationKey: "app-reading"
layout: "single"
date: "2026-12-16"
draft: true
cover:
  image: "cover.png"
  alt: "Lector Arcade v1.1 — Aprendizaje de Lectura Gamificado"
  relative: true
---

## 🌟 Novedades y Pilares de Lector Arcade v1.1 (Operación Lectura Viva)

**Lector Arcade** (*Reader Arcade*) es la aplicación educativa lúdica de Datalaria concebida para la enseñanza y el perfeccionamiento de la lectura comprensiva en niños y niñas de **4 a 11 años**, así como para personas adultas que aprenden español o inglés como segunda lengua.

Heredando la robustez arquitectónica y la filosofía *Consumer Playful* de **Ábaco Arcade** (`/apps/maths/`), Lector Arcade elimina la presión evaluativa tradicional y transforma la práctica lectora en una experiencia interactiva, táctil y motivadora:

- **6 Niveles Curriculares Adaptativos:** Desde el reconocimiento de letras y silabario elemental directo (`l1`), palabras acompañadas de ilustración (`l2`), palabras con letras faltantes y teclado táctil 3D (`l3`), palabras complejas (`l4`), hasta frases de 2 líneas (`l5`) y mini-relatos de 3 líneas (`l6`) con micro-checks de comprensión en un toque.
- **Audio Dual 1.0x y Tortuga 0.5x con Karaoke Silábico:** Botones de escucha interactiva dentro de la partida (`🔊 1.0x` y `🐢 0.5x`) con iluminación cromática secuencial de cada sílaba al ritmo exacto de la locución nativa (Web Speech API), afianzando la correspondencia grafema-fonema sin retrasos de red.
- **Librería Vectorial SVG Inline (`INV-READ-13`):** 15 ilustraciones SVG nativas optimizadas a todo color (`ReadingIllustrations`: Mesa, Nido, Nudo marinero, Iglú, Foca, Ñandú, Rueda, Cometa, Yoyó, Pozo, etc.) erradicando al 100% los emojis rotos (`□`) en cualquier tablet o sistema operativo.
- **Cálculo Universal de Velocidad Lectora (PPM / WPM) y Fluidez Efectiva:** Cronómetro de precisión split que se detiene al instante con `✅ ¡Leído!` en los 6 niveles y calcula tanto las Palabras Por Minuto brutas como las **PPM Efectivas** penalizadas objetivamente por la precisión de comprensión.
- **Modo "✏️ Mis Palabras" con Deep-Links (`?words=...`):** Panel interactivo para familias y docentes que permite cargar entre 2 y 20 palabras personalizadas (ej. el vocabulario semanal escolar) y generar un enlace compartible directo sin requerir base de datos ni registro.
- **Sistema de 3 Estrellas de Dominio (`⭐⭐⭐`):** Insignias visuales en el selector de niveles que reconocen el progreso y la maestría según la puntuación récord alcanzada, motivando la superación continua sin penalizaciones frustrantes.
- **Diploma Arcade PNG con Nombre Personalizado (`1200×800`):** Certificado de honor descargable en 1 clic renderizado en el navegador con Canvas 2D, orla dorada, avatar, récord de fluidez y campo de nombre editable para el niño o niña.
- **Lámina de Repaso Imprimible A4 PNG (`1200×1600`):** Generador instantáneo de fichas de caligrafía y lectura en papel para reforzar analógicamente las palabras practicadas o falladas en la sesión.
- **PWA 100% Offline y Privacidad Infantil Total:** Service Worker con precaché resiliente, cero dependencias de librerías CDN externas y cero transmisión de audio o telemetría a servidores remotos, garantizando máxima seguridad para los menores.

---

## 🚀 Centro de Control y Acceso Directo por Escenarios (1 Clic)

Lector Arcade v1.1 incorpora un sistema completo de **enlaces profundos (*Deep-Linking*)** que permite a educadores y familias abrir directamente la aplicación en la configuración didáctica deseada:

| Escenario Pedagógico | Nivel / Configuración | Objetivo Didáctico | Enlace Directo |
| :--- | :--- | :--- | :--- |
| **🔤 Primeros Fonemas** | Nivel 1 · Modo Normal | Reconocimiento de letras, sonidos iniciales y sílabas directas | [Abrir Nivel 1 ↗](/apps/reading/?level=l1&mode=normal&lang=es) |
| **🎨 Vocabulario con Imagen** | Nivel 2 · Modo Normal | Asociación palabra-imagen con ilustraciones SVG nativas | [Abrir Nivel 2 ↗](/apps/reading/?level=l2&mode=normal&lang=es) |
| **⌨️ Huecos y Teclado 3D** | Nivel 3 · Modo Normal | Identificación de letras faltantes con teclado táctil en pantalla | [Abrir Nivel 3 ↗](/apps/reading/?level=l3&mode=normal&lang=es) |
| **⏱️ Fluidez de Frases** | Nivel 5 · Contrarreloj | Lectura fluida en 2 líneas con parada voluntaria y micro-check | [Abrir Nivel 5 ↗](/apps/reading/?level=l5&mode=stopwatch&lang=es) |
| **📖 Comprensión Lectora** | Nivel 6 · Contrarreloj | Mini-historias de 3 líneas con cálculo de PPM y pregunta clave | [Abrir Nivel 6 ↗](/apps/reading/?level=l6&mode=stopwatch&lang=es) |
| **✏️ Deberes de la Semana** | Modo "Mis Palabras" | Preset con 5 palabras clave de ejemplo (Mesa, Nido, Nudo, Vela, Pera) | [Cargar Deberes de Ejemplo ↗](/apps/reading/?words=MESA,NIDO,NUDO,VELA,PERA&lang=es) |
| **💡 Laboratorio Fonético** | Pestaña Aprender | Mesa de mezclas interactiva para componer y escuchar sílabas | [Abrir Laboratorio Fonético ↗](/apps/reading/?tab=learn&lang=es) |

---

## 🧠 Matriz Curricular Bilingüe: Método Silábico (ES) vs. Synthetic Phonics (EN)

La enseñanza de la lectura en español y en inglés responde a realidades lingüísticas profundamente diferenciadas. Siguiendo la invariante `INV-READ-6`, Lector Arcade implementa **dos currículos nativos independientes** en su motor y catálogo:

| Nivel | Enfoque Español (Método Silábico Progresivo) | Enfoque Inglés (Synthetic Phonics & Word Families) | Dinámica de Juego |
| :---: | :--- | :--- | :--- |
| **L1** | Sonidos vocálicos, consonantes iniciales y sílabas directas simples (`M`, `P`, `L`, `S`). | Alfabeto fonético, sonidos cortos de vocales y rimas CVC básicas (`-at`, `-an`, `-og`). | Selección múltiple 1 de 3 con audio dual |
| **L2** | Palabras bisílabas directas con apoyo visual SVG (`MESA`, `NIDO`, `VELA`, `PATO`). | Palabras CVC y rimas ilustradas con ilustraciones SVG (`CAT`, `DOG`, `NEST`, `SUN`). | Lectura guiada + imagen confirmatoria |
| **L3** | Palabras con letras faltantes y teclado táctil 3D (`C_SA`, `N_DO`, `P_LO`). | Letras faltantes en onset y rime con teclado 3D (`C_T`, `D_G`, `F_X`). | Entrada táctil con teclado alfabético de 52px |
| **L4** | Sílabas inversas (`ÁR-BOL`), trabadas (`PLA-TO`, `BRA-ZO`) y complejas. | Consonant blends (`BL`, `TR`, `ST`), digraphs (`CH`, `SH`, `TH`) y vowel teams. | Decodificación avanzada + micro-check |
| **L5** | Frases contextualizadas de 2 líneas con entonación natural (10–14 palabras). | 2-line sentence phrasing con palabras visuales (*sight words*, 10–14 palabras). | Cronómetro split + freeze con `¡Leído!` |
| **L6** | Mini-relatos estructurados de 3 líneas con micro-check inferencial (18–24 palabras). | 3-line narrative passages con pregunta de comprensión literal/inferencial. | Medición de PPM brutas y PPM efectivas |

### Modos de Juego y Ergonomía Lúdica

| Modo de Juego | Dinámica Pedagógica | Reloj / Presión | Cálculo PPM / WPM |
| :--- | :--- | :--- | :--- |
| **🎮 Normal (Zen)** | Práctica relajada a ritmo propio con opción de pistas visuales, audio normal y tortuga 0.5x. | Sin límite de tiempo | No aplicable |
| **⏱️ Contrarreloj Lector** | Cronómetro split de parada voluntaria al pulsar `✅ ¡Leído!` con micro-check de comprensión. | Cuenta progresiva | Sí (universal en L1–L6) |
| **⚡ Sprint 60s** | Reto de velocidad y concentración: máxima cantidad de retos resueltos en 60 segundos. | Cuenta atrás 60s | Al completar la sesión |
| **📅 Reto Diario** | Reto determinista estilo Wordle generado por semilla de fecha para compartir en familia. | 10 retos del día | Tira de 10 bloques compartible |

---

## 📐 Fundamentos Cuantitativos y Determinismo Algorítmico (KaTeX)

El motor procedimental determinista (`apps/reading/engine.js`) elimina cualquier evaluación subjetiva mediante fórmulas matemáticas transparentes:

### 1. Velocidad Lectora Bruta (PPM / WPM)
Para evitar anomalías estadísticas por pulsaciones instantáneas accidentales, el cálculo incorpora una cláusula de guarda de tiempo mínimo ($t_{\text{min}} = 0.4\text{ s}$) y un techo fisiológico de lectura comprensiva infantil ($350\text{ PPM}$), según la invariante `INV-READ-2`:

$$\text{PPM} = \min\left(350, \text{round}\left(\frac{\text{palabras}}{\max(0.4, \text{segundos})} \times 60\right)\right)$$

### 2. Fluidez Lectora Efectiva ($\text{PPM}_{\text{efectiva}}$)
La verdadera maestría lectora requiere comprensión. La fluidez efectiva pondera la velocidad media de la sesión por el porcentaje de aciertos en los micro-checks:

$$\text{PPM}_{\text{efectiva}} = \text{round}\left(\overline{\text{PPM}} \times \frac{\text{Precisión}}{100}\right)$$

### 3. Puntuación de Ronda y Estrellas de Dominio
Cada reto completado genera una puntuación basada en la velocidad de respuesta, racha de aciertos y penalización por uso de pistas:

$$S_{\text{round}} = \text{round}\left(\max\left(50, 100 \cdot \frac{t_{\text{target}}}{\max(1.0, t_{\text{elapsed}})}\right) \cdot (1 + 0.1 \cdot \min(streak, 10)) \cdot (0.6^{\text{usedHint}})\right)$$

En el selector de niveles, las **Estrellas de Dominio (`⭐⭐⭐`)** se otorgan determinísticamente a partir de la mejor puntuación histórica del perfil:

$$\text{Estrellas} = \begin{cases} 3\bigstar & \text{si } \text{score} \ge 1200 \\ 2\bigstar & \text{si } 800 \le \text{score} < 1200 \\ 1\bigstar & \text{si } 400 \le \text{score} < 800 \\ 0\bigstar & \text{si } \text{score} < 400 \end{cases}$$

### 4. Generador Pseudoaleatorio Determinista (PRNG Mulberry32)
El Reto Diario utiliza el algoritmo de 32 bits **Mulberry32** sembrado con la fecha ISO (`YYYY-MM-DD`), garantizando que todos los alumnos o miembros de la familia jueguen exactamente la misma secuencia de palabras en cualquier dispositivo:

$$a = (a + 0\text{x6D2B79F5}) \pmod{2^{32}}$$
$$t = a \oplus (a \gg 15), \quad t = t \times (1 \mathbin{|} t), \quad t = (t + (t \oplus (t \gg 7)) \times (61 \mathbin{|} t)) \pmod{2^{32}}$$
$$\text{RNG}_{\text{norm}} = \frac{t \oplus (t \gg 14)}{2^{32}}$$

---

## 👨‍👩‍👧 Zona para Familias, Colegios y Docentes (Recursos Imprimibles)

Lector Arcade está diseñado bajo la filosofía **Dual-Mode**: una aplicación interactiva 100% gratuita y sin anuncios, complementada con recursos analógicos de alta calidad para el aula y el hogar.

### Flujo de Deberes Semanales con "Mis Palabras"
Los docentes pueden seleccionar la lista de palabras trabajada en clase (ej. *fonemas de la semana*, vocabulario temático de ciencias o palabras de ortografía dudosa) y compartirla con las familias mediante una URL directa:
```text
https://datalaria.com/apps/reading/?words=MESA,NIDO,NUDO,VELA,PERA&lang=es
```
Al hacer clic, la aplicación carga automáticamente las palabras en el escenario de juego con teclado 3D, silabeo automático y síntesis de voz, sin que los padres deban instalar nada ni crear cuentas.

### Descarga Gratuita de Lámina de Repaso A4 PNG
Al finalizar cualquier partida en Lector Arcade, los alumnos pueden pulsar el botón **"🖨️ Descargar Lámina de Repaso (A4 PNG)"**. El navegador genera al instante un archivo de alta resolución (`1200×1600 px`) con:
- Encabezado con fecha, nivel y nombre del alumno.
- Las palabras practicadas desglosadas por sílabas en cajas pautadas para caligrafía a lápiz.
- Espacio para colorear y autoevaluación guiada.

### Próximo Lanzamiento: Kit Imprimible Lector Arcade (ES/EN)
Como parte del ecosistema de productos educativos descargables en Lemon Squeezy, estamos preparando el **Kit Imprimible Lector Arcade**:
1. **120 Flashcards Recortables en PDF:** Tarjetas a doble cara con ilustración SVG, palabra pautada y descomposición silábica/phonics.
2. **Cuaderno de Lectoescritura A4 (6 Niveles):** 48 páginas estructuradas de actividades progresivas de discriminación auditiva, huecos de letras y comprensión lectora.
3. **Tracker de Fluidez Lectora en Excel:** Plantilla docente para registrar las PPM y porcentaje de comprensión de hasta 30 alumnos a lo largo del curso escolar.

---

## 📐 Especificación y Comunalidad Técnica

Lector Arcade está construido bajo la metodología **Spec-Driven Development (SDD)** gobernada por el Escuadrón Datalaria Helix, cumpliendo estrictamente con las invariantes de calidad `INV-READ-1..14`:

- **Arquitectura:** SPA autónoma en Vanilla JavaScript moderno compilada en un único archivo inline en `/static/apps/reading/index.html`.
- **Diseño Visual:** Design Tokens nativos en CSS3 para temas `Daylight Arcade` (modo claro) y `Cosmic Night` (modo oscuro) con prevención anti-FOUC.
- **Audio Dual:** Síntesis procedural 8-bit con Web Audio API para aciertos y rachas, combinada con Web Speech API para lectura auditiva accesible a 1.0x y 0.5x.
- **Acceso Directo:** [Abrir Lector Arcade ↗](/apps/reading/)
