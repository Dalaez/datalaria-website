# Registro de Decisiones de Arquitectura (ADR Log — Datalaria SDD)

> **Propósito:** Mantener la memoria histórica de **por qué** se tomaron las decisiones clave de arquitectura en Datalaria. Esto evita que en futuras sesiones un humano o un agente de IA proponga revertir patrones ya evaluados y descartados.

---

## ADR-001: Adopción de Spec-Driven Development (SDD) Agnóstico del Modelo
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** La plataforma Datalaria se desarrolla utilizando múltiples asistentes agénticos de vanguardia (principalmente Google Antigravity con Gemini 4 Argon y agentes basados en Claude). El crecimiento orgánico previo generó código heterogéneo sin una fuente única de verdad.
- **Decisión:** Adoptar una arquitectura estricta **Spec-First** centralizada en `/specs/`, con [`AGENTS.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/AGENTS.md) como punto de entrada universal y [`CLAUDE.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/CLAUDE.md) como puntero ligero. Ningún código de producción se modifica sin actualizar antes su `spec.md`.
- **Consecuencias:** Coherencia total entre sesiones y entre distintos modelos de IA; reducción drástica de regresiones y alucinaciones arquitectónicas.

---

## ADR-002: Expulsión del Código Fuente Backend fuera de `/static/`
- **Fecha:** 2026-10-24
- **Estado:** En ejecución (Completado para LifeOps e Hito 2.1 Obs-Management; pendiente cuarentena Fase 3)
- **Contexto:** Durante la auditoría inicial ([`00-ecosystem-audit.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/audit/00-ecosystem-audit.md)) se detectó que proyectos backend en Python (`project-ops`, `sop-pipeline`, `obs-management`), junto con esquemas `.sql` y archivos `.env`, residían dentro de `static/apps/`. Hugo copia todo el contenido de `static/` al directorio público `public/`.
- **Decisión:** Mover todo código fuente de aplicaciones a un directorio raíz `/apps/<app-slug>/`. El directorio `/static/apps/` queda restringido exclusivamente a artefactos frontend compilados (`dist/`) y activos estáticos puros.
- **Consecuencias:** Eliminación del riesgo de filtración de código propietario y credenciales en despliegues de Netlify; separación limpia entre código fuente y artefactos de distribución.

---

## ADR-003: Patrón de Monetización y Ejecución "Dual-Mode" (Executive Sandbox + Live Engine)
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** Algunas aplicaciones B2B (como `obs-management`) apuntaban a `http://localhost:8001` en su HTML estático, mostrando un error `OFFLINE` a los visitantes reales de `datalaria.com`. Además, mantener múltiples servidores backend encendidos 24/7 para tráfico exploratorio es costoso, pero las apps necesitan demostrar valor inmediato para vender los *Executive Decision Packs* de Lemon Squeezy.
- **Decisión:** Todas las aplicaciones B2B implementarán dos modos:
  1. **Modo Sandbox (Por defecto en web pública):** Funciona 100% en el navegador sin requerir backend activo ni login, utilizando datos ejecutivos pre-calculados o motores deterministas ligeros en cliente, e integrando un banner contextual de compra del *Executive Pack* en Lemon Squeezy.
  2. **Modo Live Engine / Pro:** Conecta con el backend FastAPI + Supabase + IA Agéntica cuando el usuario se autentica o conecta su entorno.
- **Consecuencias:** Cero pantallas rotas en producción, latencia cero para visitantes del blog, coste de infraestructura controlado y embudo de conversión directo hacia Lemon Squeezy.

---

## ADR-004: Consolidación de Persistencia en un Único Proyecto Supabase Multi-Esquema
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** Existían referencias a múltiples proyectos de Supabase distintos (`wkbmxekmofrjtcsyytrv` en LifeOps, `wxwnbzmbzztegcdzrxbg` en Neon Snake, e instancias por `.env` en las demás apps).
- **Decisión:** Consolidar todas las aplicaciones en un único cluster Supabase (`datalaria-core`), aislando los dominios mediante esquemas de PostgreSQL (`lifeops`, `pmo_analytics`, `sop_engine`, `obs_radar`, `arcade`) con políticas RLS estrictas.
- **Consecuencias:** SSO unificado para el usuario en todas las apps de Datalaria, administración centralizada de backups/secretos y prevención de pausas por inactividad en planes gratuitos dispersos.

---

## ADR-005: Congelación ("Feature Freeze") de Micro-Apps Legacy
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** Las utilidades iniciales (`conversor`, `maths`, `flashcards`, `snake`) están construidas con HTML duplicado por idioma (`/es/`, `/en/`) y Tailwind por CDN. Su valor de negocio B2B es nulo o marginal frente al esfuerzo de migrarlas a SDD.
- **Decisión:** Clasificarlas como **No Migrables (Frozen Legacy)**. Se mantienen sus rutas estáticas para no romper enlaces entrantes ni SEO histórico, pero se reubican visualmente en una sección secundaria (*"Open Lab & Arcade"*) dentro de `/apps/`, reservando la cabecera del catálogo para las Suites Ejecutivas y Operativas.
- **Consecuencias:** Foco del 100% de la capacidad de ingeniería en activos monetizables B2B y mejora sustancial de la percepción de marca C-Level.

---

## ADR-006: Sincronización Estricta entre Publicación Editorial y Catálogo de Apps (`Post ⇔ App`)
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** Al cruzar las carpetas de `/static/apps/` con los artículos de `/content/*/posts/`, se comprobó que existen exactamente **7 aplicaciones publicadas en la web** (`lifeops`, `obs-management`, `snake`, `weather`, `flashcards`, `conversor`, `maths`), todas respaldadas por artículos con `draft: false`. En cambio, `project-ops` tiene sus artículos en borrador (`draft: true`) y `sop-pipeline` solo enlazaba a un Google Colab externo, pero sus archivos `.py` y `.env` estaban alojados dentro de `static/apps/`.
- **Decisión:**
  1. **Prioridad Exclusiva en las 7 Apps Activas:** Ejecutar todo el ciclo de consolidación SDD primero sobre las 7 aplicaciones que hoy están publicitadas en la web (empezando por `lifeops`, `obs-management` y `weather`, y congelando `snake`, `flashcards`, `conversor` y `maths`).
  2. **Cuarentena de Incubación para Apps Inéditas:** `project-ops` y `sop-pipeline` no se migran ni se publican ahora; únicamente se retiran sus archivos Python/SQL/env de `static/apps/` por higiene de seguridad y pasan a la **Fase 4 (Incubadora de Nuevos Lanzamientos)** para ser revisadas, validadas y estrenadas bajo SDD cuando se publiquen sus posts.
- **Consecuencias:** Cero trabajo prematuro sobre apps aún no validadas funcionalmente por el autor, eliminación inmediata de código inédito expuesto en `/static/` y alineación total entre el blog editorial y el catálogo de aplicaciones.

---

## ADR-007: Fichas de App Data-Driven con Historial Evolutivo (`apps-showcase`)
- **Fecha:** 2026-10-24
- **Estado:** Implementado (Completado en Hitos 1.3, 1.4, 2.1 y 2.2)
- **Contexto:** El listado `/apps/` actual es HTML embebido en `content/*/apps/_index.md` con tarjetas de solo icono y texto, duplicado por idioma. No existe un lugar donde el usuario vea objetivos, diseño, tecnologías ni la evolución de cada App, y los posts enlazan directamente a la App sin contexto.
- **Decisión:**
  1. Una **ficha por App** en `/{lang}/apps/<slug>/` (page bundle Hugo) con layout común `layouts/apps/single.html`.
  2. **Metadatos en `data/apps/<slug>.yaml`** (bilingüe en un único fichero) como fuente única para ficha, tarjeta y shortcode de posts.
  3. **Tarjetas visuales con captura** en el listado, agrupadas por `tier` (flagship / b2b / lab).
  4. **Shortcode `app-ref`** en los posts de referencia para enlazar a la ficha.
  5. **Validación en build** (campos obligatorios, posts existentes, versión coherente).
- **Alternativas descartadas:**
  - *Front matter por idioma en cada `index.md`:* duplicaría el changelog y las tecnologías en ES y EN → desincronización garantizada.
  - *Generar las fichas desde `spec.md`:* acopla documentación de ingeniería (con deuda y riesgos internos) a contenido público.
  - *Página única con todas las Apps en acordeón:* peor SEO y sin URL compartible por App.
- **Consecuencias:** Añadir una App nueva = 1 YAML + 2 `index.md` + 1 captura. El changelog público se mantiene en paralelo a la spec (regla de Constitución Art. 8.3).

---

## ADR-008: Despliegue Híbrido Serverless con Proxy Netlify para Apps de ETL Continuo (`weather`)
- **Fecha:** 2026-10-24
- **Estado:** Aceptado
- **Contexto:** El Dashboard Climático (`weather`) ingesta telemetría 3 veces al día de más de 160 ciudades y reentrena modelos de Machine Learning. Alojar el dataset vivo dentro del repositorio de Datalaria saturaría Git con decenas de miles de commits automáticos de actualización de CSVs.
- **Decisión:**
  1. Mantener la ejecución continua desatendida en el repositorio upstream `https://github.com/Dalaez/app_weather.git` mediante GitHub Actions y despliegue a Netlify (`datalaria-app-weather.netlify.app`).
  2. Servir la aplicación a los usuarios finales transparentemente bajo el dominio de Datalaria mediante la regla de proxy forzado `200!` en `static/_redirects` (`/apps/weather/* https://datalaria-app-weather.netlify.app/:splat 200!`).
  3. Consolidar el código fuente canónico, scripts de recolección y especificación SDD en [`apps/weather/`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/apps/weather) y [`specs/apps/weather/spec.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/apps/weather/spec.md).
- **Consecuencias:** Cero ruido de commits en el blog principal, 100% serverless con coste $0/mes y preservación transparente de la URL pública canónica `https://datalaria.com/apps/weather/`.
