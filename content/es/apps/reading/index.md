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
  alt: "Lector Arcade — Aprendizaje de Lectura Gamificado"
  relative: true
---

## 🌟 Novedades y Pilares de Lector Arcade v1.0

**Lector Arcade** (*Reader Arcade*) es la aplicación educativa lúdica de Datalaria concebida para la enseñanza y el perfeccionamiento de la lectura comprensiva en niños y niñas de **4 a 11 años**, así como para personas adultas que aprenden español o inglés como segunda lengua.

Heredando la robustez arquitectónica y la filosofía *Consumer Playful* de **Ábaco Arcade** (`/apps/maths/`), Lector Arcade elimina la presión evaluativa tradicional y transforma la práctica lectora en una experiencia interactiva, táctil y motivadora:

- **6 Niveles Curriculares Adaptativos:** Desde el reconocimiento de letras y silabario elemental directo (`l1`), palabras acompañadas de imagen (`l2`), palabras con letras faltantes y teclado 3D (`l3`), palabras complejas (`l4`), hasta frases de 2 líneas (`l5`) y mini-relatos de 3 líneas (`l6`) con micro-checks de comprensión en un toque.
- **Contrarreloj Split con Cálculo Determinista de PPM:** Cronómetro de alta precisión que se congela voluntariamente al pulsar `✅ ¡Leído!` y calcula la velocidad lectora en **Palabras Por Minuto (PPM / WPM)**, validada mediante una pregunta inmediata de comprensión.
- **Laboratorio Fonético Bilingüe (`💡 Aprender`):** Mesa de mezclas silábica interactiva para componer y escuchar sílabas directas, inversas y trabadas en español, o familias léxicas CVC, *blends* y *digraphs* en inglés, con sintetizador de voz nativo Web Speech API en velocidad normal (`1.0x`) y modo tortuga didáctico (`0.65x`).
- **Teclado Táctil Alfabético 3D:** Botones de gran formato (`>= 52px`) en pantalla para tabletas y móviles infantiles, evitando que el teclado del sistema operativo desplace la interfaz de juego.
- **Perfiles Familiares Multi-Jugador:** Selector de 3 perfiles locales (`🦁 Jugador 1`, `🦊 Jugador 2`, `🦉 Adulto`) que aísla de forma independiente las puntuaciones máximas, rachas de acierto y las 6 medallas coleccionables.
- **Diploma Arcade PNG en 1 Clic (`1200×800`):** Generador de certificados de honor en alta definición renderizado 100% en el cliente mediante Canvas 2D nativo, con orla dorada, avatar de perfil, récord de velocidad y sello oficial de excelencia lectora.
- **PWA 100% Offline y Privacidad Infantil Total:** Service Worker con precaché resiliente, cero librerías CDN externas y cero envío de voz a servidores remotos, garantizando máxima seguridad para los más pequeños.

---

## 🚀 Modos de Juego y Ergonomía Lúdica

| Modo de Juego | Dinámica Pedagógica | Reloj / Presión | Cálculo PPM / WPM |
| :--- | :--- | :--- | :--- |
| **🎮 Normal (Zen)** | Práctica relajada a ritmo propio con opción de pistas visuales y fonéticas. | Sin tiempo límite | No aplicable |
| **⏱️ Contrarreloj Lector** | Cronómetro split que se detiene en seco al pulsar `✅ ¡Leído!`. | Cuenta progresiva | Sí (con micro-check) |
| **⚡ Sprint 60s** | Reto de velocidad y concentración: tantas palabras o frases como puedas leer en 1 minuto. | Cuenta atrás 60s | Al cerrar la ronda |
| **📅 Reto Diario** | Reto estilo Wordle reproducible por semilla determinista para competir en familia. | 10 retos del día | Tira de 10 bloques compartible |

---

## 📐 Especificación y Comunalidad Técnica

Lector Arcade está construido bajo la metodología **Spec-Driven Development (SDD)** gobernada por el Escuadrón Datalaria Helix, cumpliendo estrictamente con las invariantes de calidad `INV-READ-1..12`:

- **Arquitectura:** SPA autónoma en Vanilla JavaScript moderno compilada en un único archivo inline en `/static/apps/reading/index.html`.
- **Diseño Visual:** Design Tokens nativos en CSS3 para temas `Daylight Arcade` (modo claro) y `Cosmic Night` (modo oscuro) con prevención anti-FOUC.
- **Audio Dual:** Síntesis procedural 8-bit con Web Audio API para aciertos y rachas, combinada con Web Speech API para lectura auditiva accesible sin consumir ancho de banda.
- **Acceso Directo:** [Abrir Lector Arcade ↗](/apps/reading/)
