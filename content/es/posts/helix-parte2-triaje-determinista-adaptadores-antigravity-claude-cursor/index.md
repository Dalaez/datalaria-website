---
title: "Triaje Determinista XS–XL y Adaptadores Multi-Herramienta: Cómo Reducir un 87 % el Gasto de Tokens en Antigravity, Claude Code, Cursor y Codex"
date: 2027-01-26
draft: false
cover:
  image: "cover.png"
  alt: "Datalaria Helix: Triaje Determinista XS-XL y Adaptadores Multi-Herramienta"
  caption: "Datalaria Helix (2/5) — Triaje Determinista XS–XL, Ahorro del 87 % de Contexto y Compilador Multi-Herramienta"
  relative: true
image: "cover.png"
category: "IA, Ingeniería y Proyectos"
categories: ["Ingeniería de Software", "Spec-Driven Development", "Agentes IA", "IA, Ingeniería y Proyectos"]
tags: ["Datalaria Helix", "Spec-Driven Development", "SDD", "Triaje Agéntico", "Token Optimization", "Google Antigravity", "Claude Code", "Cursor Rules", "DevOps"]
description: "Por qué cargar decenas de reglas agénticas satura el contexto de los LLMs y cómo el algoritmo matemático de triaje de Helix y su compilador determinista reducen un 87 % el consumo de tokens manteniendo cero fricción en Antigravity, Claude y Cursor."
summary: "El error más costoso al trabajar con agentes de IA es arrojar cientos de instrucciones al prompt de arranque esperando que el modelo las recuerde todas. En esta segunda entrega de Datalaria Helix revelamos nuestro motor de triaje determinista (tallas XS a XL), los disparadores automáticos innegociables (TRG-SEC, TRG-UX, TRG-I18N), las invariantes de higiene anti-bloat y el compilador que genera 26 adaptadores multiplataforma desde una única fuente canónica."
translationKey: "helix-part2"
---

Uno de los errores más extendidos y costosos en los equipos que intentan profesionalizar el desarrollo con inteligencia artificial consiste en tratar la ventana de contexto del modelo de lenguaje como si fuera un contenedor infinito.

La tentación inicial es comprensible: creas una carpeta con quince manuales de estilo, guías de arquitectura de microservicios, reglas de TypeScript, políticas de seguridad corporativas y fichas descriptivas de agentes. A continuación, inyectas todos esos documentos en el archivo de instrucciones globales del editor (como un gigantesco `.cursorrules`, un `CLAUDE.md` de 2.000 líneas o un mega-prompt del sistema).

El resultado práctico es desolador:
- El modelo consume entre 80.000 y 140.000 tokens de entrada en cada turno de conversación solo para leer sus propias instrucciones.
- La atención matemática del transformador se fragmenta entre cientos de directrices secundarias, ignorando reglas fundamentales de seguridad y cometiendo fallos elementales en tareas triviales (*Prompt Bloat*).
- Las facturas de API se disparan exponencialmente sin que la calidad del código producido aumente un solo punto porcentual.

En **Datalaria Helix**, abordamos este desafío mediante dos pilares de ingeniería formal: la **Invariante de Carga Bajo Demanda (`INV-HELIX-2`)** gobernada por una matriz de **Triaje Determinista (`XS` a `XL`)**, y un **Compilador Automático de Adaptadores (`ops/helix/build_adapters.py`)** que sincroniza 26 artefactos nativos para Google Antigravity, Claude Code, Cursor IDE y OpenAI Codex a partir de una única especificación canónica.

El resultado es una reducción empírica del **~87 % en el consumo de tokens** (de ~140.000 tokens en flujos no controlados a solo ~18.500 tokens por sesión acotada), eliminando cualquier pérdida de foco en el modelo.

---

### 🗺️ Hoja de Ruta de la Serie Datalaria Helix

1. ⚪ **Parte 1:** [La Especificación es el ADN de tu App: Por Qué el Vibe Coding Colapsa a las 48 Horas y Cómo los 12 Agentes de Helix Gobiernan el Desarrollo con IA](/es/posts/helix-parte1-especificacion-adn-escuadron-12-agentes/).
2. 🟢 **Parte 2 (Este artículo):** *Triaje Determinista XS–XL y Adaptadores Multi-Herramienta: Cómo Reducir un 87 % el Gasto de Tokens en Antigravity, Claude Code, Cursor y Codex.*
3. ⚪ **Parte 3:** [El Músculo Determinista: CLI helix.py en Python Puro, Evaluación SpecQualityScore (0..100) y Rollback Automático al Segundo Fallo](/es/posts/helix-parte3-cli-python-cero-dependencias-spec-score-rollback/).
4. ⚪ **Parte 4:** [Helix Spec Builder en React 19 + TypeScript: Modo A con Empaquetado PKZIP Client-Side y Modo B con Exportador de Mega-Prompt](/es/posts/helix-parte4-sandbox-react-spec-builder-zip-client-side/).
5. ⚪ **Parte 5:** [Evidencia Empírica de Veto en Acción: La Auditoría de Datalaria Pulse ("Operación Crisol"), el Caso MarginGuard B2B y los Kits Comerciales](/es/posts/helix-parte5-casos-reales-operacion-crisol-pulse-marginguard-kits/).

---

## 1. La Patología del Prompt Bloat: Por Qué Más Reglas Producen Menor Calidad

En los modelos generativos contemporáneos, el coste cognitivo de procesar instrucciones irrelevantes para la tarea inmediata no es lineal: es hiperbólico.

Si un desarrollador necesita corregir una errata tipográfica en un botón de la interfaz o modificar el color de fondo de una tarjeta, cargar en contexto las directrices de migración de esquemas SQL en Supabase, las políticas de webhook de Lemon Squeezy y el manual de optimización de PyMuPDF no aporta valor alguno. Al contrario: introduce vectores de distracción donde el modelo intenta "demostrar que conoce todo el contexto", refactorizando clases adyacentes que nadie le pidió modificar.

```
COMPARATIVA DE CONSUMO DE CONTEXTO POR SESIÓN:
Vibe Coding / Mega-Prompts: [========== 140.000 tokens ==========] (Ruido cognitivo)
Datalaria Helix SDD:       [== 18.500 ==] (-87 % Ahorro directo y foco láser)
```

Por esta razón, la Constitución de Datalaria Helix establece una prohibición categórica:

> **Invariante INV-HELIX-2 (Carga Bajo Demanda):** Queda terminantemente prohibido cargar en el contexto de una sesión las 12 fichas de agentes simultáneamente para tareas de talla `XS`, `S` o `M`. Todo agente debe ejecutar el triaje determinista y leer exclusivamente las fichas de los roles expresamente convocados.

---

## 2. El Algoritmo Matemático de Triaje: Tallas XS a XL

¿Cómo decide el sistema qué agentes activar sin caer en la improvisación humana? Mediante un algoritmo determinista parametrizado sobre tres variables objetivas:

1. El número estimado de archivos modificados ($F \in \mathbb{N}$).
2. El conjunto de superficies técnicas afectadas ($S \subseteq \{\text{docs}, \text{ui}, \text{frontend}, \text{backend}, \text{data\_sql}, \text{apis}, \text{media\_i18n}, \text{monetization}, \text{auth\_security}\}$).
3. Banderas booleanas de cambio de especificación ($\Delta_{\text{spec}} \in \{0, 1\}$) o creación de nueva aplicación ($\Delta_{\text{app}} \in \{0, 1\}$).

```
Matriz de Asignación de Talla Base:
- Si Delta_app = 1                   ==> Talla XL (Se descompone en N hitos <= L)
- Si Delta_spec = 1 o |S| >= 3       ==> Talla L  (Convocatoria ampliada)
- Si |S| = 2 o F > 3                 ==> Talla M  (Arquitectura + Constructores + Release)
- Si 1 < F <= 3 y |S| = 1            ==> Talla S  (Constructor directo + QA)
- Si F = 1 y |S| = 1 y Delta_spec = 0 ==> Talla XS (Constructor puntual + QA)
```

### Tabla Canónica de Dimensionamiento por Talla:

| Talla | Criterio Objetivo Determinista | Roles Convocados | Fichas en Contexto | Ejemplo Real en Datalaria |
| :-: | :--- | :--- | :-: | :--- |
| **`XS`** | $F = 1$ archivo · $1$ superficie no sensible · $\Delta_{\text{spec}} = 0$ | `01` + $1$ Constructor + `11-qa` | **2–3** | Corregir una errata tipográfica o ajustar un margen de espaciado CSS. |
| **`S`** | $1 \le F \le 3$ archivos · $1$ superficie técnica · Sin cambio de arquitectura | `01` + $1\text{–}2$ Constructores + `11-qa` | **3–4** | Añadir un filtro por fecha en una tabla React o una nueva prueba en `pytest`. |
| **`M`** | $F > 3$ archivos **o** $2$ superficies combinadas **o** ajuste menor de contrato | `01` + `03-architect` + $2\text{–}3$ Constructores + `11-qa` + `12-release` | **4–6** | Integrar el formulario de Waitlist con Brevo en posts y catálogo (Hito 6.0). |
| **`L`** | Funcionalidad completa que crea/modifica una `spec.md` o el modelo de negocio | `01` + `02` + `03` + `04` + Constructores + `10` + `11-qa` + `12-release` | **6–9** | Auditoría integral y robustecimiento de Datalaria Pulse y Kit ZIP (Hito 6.3). |
| **`XL`** | Aplicación nueva desde cero o épica multi-módulo | **Prohibido ejecutar de golpe.** División en $N$ hitos atómicos de talla $\le \mathbf{L}$. | Secuencial | Desarrollo completo del producto Datalaria Helix (Hitos 6.0 a 6.9). |

### La Tarjeta de Triaje Canónica de 6 Líneas:

Antes de escribir una sola línea de código o abrir un archivo de producción, el Orquestador (`01-orchestrator`) emite en el chat un bloque estructurado e inmutable:

```text
TRIAGE HELIX · Hito 6.2 · Talla: M
Superficies afectadas: backend, docs, auth_security
Roles activados (5 de 12): 🎯 01-orchestrator, 🏛️ 03-architect, 🗄️ 06-backend-data, 🛡️ 10-security-privacy, ✅ 11-qa-verifier (VETO)
Roles en banquillo: 02, 04, 05, 07, 08, 09, 12
Verification Gate: pytest ops/helix/tests -v ; python -m ops.helix.build_adapters --check ; hugo --renderToMemory
Presupuesto y Gobernanza: Máx. 2 intentos por gate · Checkpoint sdd-checkpoint-pre-6.2 · Aprobación humana previa: SÍ
```

Cualquier agente que no figure entre los **Roles activados** permanece en el banquillo y **jamás se carga en la memoria de la sesión**.

---

## 3. Disparadores Automáticos Innegociables (`INV-HELIX-3`)

Una vulnerabilidad común de los sistemas de triaje ingenuos es que un desarrollador o agente intente clasificar como `XS` una tarea pequeña en número de líneas pero crítica en repercusiones de seguridad (por ejemplo, alterar una línea en un archivo `.env` o relajar una política de Row Level Security).

Para blindar el sistema ante esta trampa, Helix establece la **Invariante INV-HELIX-3**:

> **Invariante INV-HELIX-3 (Disparadores Automáticos Innegociables):** Ninguna tarea, sin importar que toque un único archivo o una sola línea, puede catalogarse como `XS` o `S` sin convocar al especialista correspondiente si se detecta alguno de los 5 disparadores obligatorios:

1. **`TRG-SEC` (Seguridad y Privacidad):** Si se tocan variables de entorno, autenticación, Supabase RLS, funciones serverless, cobros o la carpeta `/static/` $\implies$ Activa obligatoriamente a [`10-security-privacy`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/10-security-privacy.md) con derecho a veto.
2. **`TRG-UX` (Diseño y Experiencia):** Si se crea o modifica cualquier elemento de interfaz visible (`.tsx`, `.html`, `.css`, modales, paletas) $\implies$ Activa obligatoriamente a [`04-ux-ui`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/04-ux-ui.md) para auditar contra `design.md` y WCAG 2.2 AA.
3. **`TRG-I18N` (Contenidos y Paridad Lingüística):** Si se tocan artículos en `content/`, metadatos en `data/apps/*.yaml` o diccionarios `i18n` $\implies$ Activa a [`08-media-i18n`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/08-media-i18n.md) para asegurar paridad estricta `ES ⇔ EN` y regenerar el índice de Pulse.
4. **`TRG-MON` (Monetización y Precios):** Si se tocan precios, URLs de Lemon Squeezy, `/recursos/` o eventos analíticos $\implies$ Activa a [`09-monetization`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/09-monetization.md).
5. **`TRG-QA` (Garantía de Calidad Universal):** Aplica en **el 100 % de las tareas** $\implies$ Activa a [`11-qa-verifier`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/11-qa-verifier.md) con derecho a veto inapelable.

---

## 4. Higiene de Contexto y Control Anti-Bloat (`INV-HELIX-8`)

Con el paso de las semanas, los sistemas agénticos tienden a sufrir una forma perniciosa de esclerosis: los desarrolladores añaden reglas, excepciones y parches acumulativos hasta que los prompts de sistema superan los miles de líneas de longitud.

Datalaria Helix combate este fenómeno mediante la **Invariante INV-HELIX-8**:

```
REGLAS INMUTABLES DE HIGIENE ANTI-BLOAT (INV-HELIX-8):
1. Tope Duro por Ficha: <= 85 líneas totales por archivo canónico specs/squad/*.md
2. Límite de Fricción:  Máximo 6 reglas en la Sección 6 ([USER-FIX] / [ENV-FIX])
3. Criterio de Entrada: Prohibida teoría general; solo correcciones empíricas reales
4. Memoria Templada:   TECH_RADAR.yaml y OPPORTUNITY_BACKLOG.md nunca se cargan de inicio
```

### Criterio Exclusivo de Entrada: Lecciones de Fricción Real

En la Sección `## 6` de cada agente **solo se permite registrar reglas nacidas de fricción empírica documentada**:
- **`[USER-FIX]`:** Correcciones explícitas realizadas por el usuario humano ante una desviación del modelo en una sesión previa (por ejemplo, *«prohibido usar el carácter & dentro de diagramas Mermaid en Hugo»*).
- **`[ENV-FIX]`:** Errores específicos del entorno de ejecución (por ejemplo, *«en consolas Windows PowerShell, invocar npm.cmd en lugar de npm para evitar bloqueos de ejecución de scripts»*).

Cuando un agente acumula 6 reglas y surge una séptima lección aprendida, el Orquestador aplica poda **FIFO** (elimina la regla más antigua ya interiorizada por el modelo) o ejecuta una fusión sintética, manteniendo el archivo invariablemente por debajo de las 85 líneas.

---

## 5. El Compilador Multi-Herramienta: De una Fuente Canónica a 26 Adaptadores

Uno de los mayores triunfos de ingeniería en Datalaria Helix es su **total agnosticismo respecto al entorno de desarrollo**. Helix no te ata a una herramienta propietaria ni exige una suscripción exclusiva: funciona de forma idéntica en **Google Antigravity**, **Claude Code**, **Cursor IDE** y **OpenAI Codex / GitHub Copilot**.

¿Cómo logramos esta universalidad sin mantener 4 versiones desincronizadas de cada agente? Mediante nuestro compilador determinista: **`ops/helix/build_adapters.py`**:

{{< mermaid >}}
flowchart LR
    SRC["12 Fichas Canónicas Markdown\n(specs/squad/*.md)"] --> COMP["Compilador Python\n(ops/helix/build_adapters.py)"]
    COMP --> AGY[".agents/squad/\n12 Adaptadores Antigravity\n+ manifest.json"]
    COMP --> CLD[".claude/agents/\n12 Subagentes Claude Code\n+ CLAUDE.md"]
    COMP --> CUR[".cursor/rules/\nhelix-squad.mdc\n(Cursor IDE Rule)"]
    COMP --> CDX["AGENTS.md\n(OpenAI Codex / Copilot\nUniversal Entrypoint)"]
{{< /mermaid >}}

### Ejecución Determinista e Idempotente:

El script se ejecuta como parte obligatoria del ciclo de integración continua:

```bash
# Compilar y propagar adaptadores
python -m ops.helix.build_adapters

# Verificar sincronización en CI/CD (retorna código 1 si hay deriva)
python -m ops.helix.build_adapters --check
```

A partir de las 12 fichas maestras en `specs/squad/`, el compilador genera:
1. **Para Google Antigravity:** 12 archivos Markdown optimizados para modelos Gemini en `.agents/squad/<id>.md` y el catálogo estructurado `.agents/squad/manifest.json`.
2. **Para Anthropic Claude Code:** 12 subagentes con metadatos YAML de invocación nativa en `.claude/agents/<id>.md`.
3. **Para Cursor IDE:** La regla global unificada con directrices de triaje en `.cursor/rules/helix-squad.mdc`.
4. **Para OpenAI Codex / Copilot:** El mapa de gobernanza y arranque de tres pasos en `AGENTS.md`.

Los adaptadores son artefactos de compilación estricta (`INV-HELIX-4`). Está **terminantemente prohibido editarlos a mano**: cualquier mejora o ajuste se realiza en la ficha canónica de `specs/squad/` y se propaga en un solo segundo mediante el compilador.

---

## 6. Adopta la Gobernanza Agéntica en tu Propio Repositorio

La disciplina de triaje determinista y compilación de adaptadores que gobierna Datalaria Helix está diseñada para ser transferida a cualquier proyecto de software en cuestión de minutos.

{{< app-ref slug="helix" >}}

### Comienza Hoy Mismo con Datalaria Helix:

1. **Prueba el Algoritmo de Triaje en el Sandbox ([/apps/helix/](/apps/helix/)):**  
   Introduce las características de tu proyecto en el configurador interactivo. Observa en tiempo real cómo el motor dimensiona tu desarrollo, identifica los disparadores de riesgo y selecciona exactamente los agentes requeridos para tu arquitectura.  
   👉 [**Probar Triaje en Vivo en el Sandbox →**](/apps/helix/)

2. **Consigue el Core Kit con Todos los Adaptadores Pre-Compilados:**  
   En nuestra sección de recursos puedes descargar el **Datalaria Helix Core Kit** a precio de lanzamiento Early-Bird (**19 €** en lugar de **39 €**). Incluye las 12 fichas maestras, el compilador `build_adapters.py`, los 26 adaptadores listos para copiar a tu repositorio, el CLI `helix.py` y los 3 blueprints de producción.  
   🚀 [**Descargar Datalaria Helix Core Kit en Recursos →**](/es/recursos/#pack-sdd)

En la próxima entrega (*Parte 3/5*), nos sumergiremos en el **músculo determinista** del sistema: el CLI `helix.py` en Python estándar sin dependencias externas, el cálculo matemático del **SpecQualityScore (0..100)** y el protocolo de **Rollback Automático al segundo fallo consecutivo**.
