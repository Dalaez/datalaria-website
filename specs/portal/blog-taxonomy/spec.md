# Especificación Técnica: Taxonomía Editorial en 5 Pilares (`SPEC-PORTAL-TAXONOMY`)

> **Versión:** 1.1.0  
> **Estado:** APROBADA Y VINCULANTE  
> **Módulo:** Portal Home (`layouts/partials/index_profile.html`), Plantillas SEO (`layouts/partials/head.html`, `layouts/_default/sitemap.xml`), Contenidos (`content/{es,en}/posts/`) y Datalaria Pulse (`ops/pulse/`).  
> **Referencia ADR:** [`ADR-016`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/DECISIONS.md#adr-016)

---

## 1. Visión y Objetivos

Evolucionar la arquitectura temática del blog de Datalaria desde el modelo inicial de 4 pestañas hacia un sistema de **5 Pilares Editoriales**. Esta reorganización persigue:
1. **Unificar Software e IA:** Fusionar los deep-dives técnicos y las series de aplicaciones en un único pilar unificado de ingeniería.
2. **Potenciar el Embudo B2B:** Aislar los 20 artículos cuantitativos de negocio, finanzas y operaciones en su propia categoría visible, conectada con los *Executive Decision Packs* de Lemon Squeezy.
3. **Dignificar el Contenido Cultural e Histórico:** Otorgar identidad propia a los ensayos de cine/series/libros y a los perfiles epistemológicos de pioneros sin contaminar la navegación de ingeniería pura.
4. **Blindaje Absoluto del SEO:** Garantizar que ninguna URL canónica, archivo de categoría preexistente o etiqueta de indexación sufra disrupción alguna.

---

## 2. Invariantes Arquitectónicas y de Negocio

### INV-TAX-1: Preservación Estricta de SEO y Taxonomías Existentes (SEO Safe-Guard)
Está **TERMINANTEMENTE PROHIBIDO** eliminar o modificar tags (`tags: [...]`) o categorías secundarias (`categories: [...]`) preexistentes en los archivos markdown de `content/es/posts/` y `content/en/posts/`.
- Las URLs de taxonomías históricas generadas por Hugo (ej. `/categories/ingenieria/`, `/tags/inteligencia-artificial/`) deben seguir existiendo y resolviendo con código `200`.
- El campo singular `category:` define la temática primaria del portal (`index_profile.html`).
- Si es necesario para consistencia en la taxonomía plural de Hugo, la nueva temática primaria se **añade** al array `categories: [...]`, nunca reemplazando destructivamente los términos ya indexados por Google.

### INV-TAX-2: Arquitectura de 5 Pilares Canónicos Bilingües
El campo `category:` de todo post debe pertenecer exactamente a uno de los 5 pares canónicos:

| Clave (`key`) | Icono | `category` en Front Matter (ES) | `category` en Front Matter (EN) | Etiqueta UI Pestaña (`label_es`) | Etiqueta UI Pestaña (`label_en`) |
| :---: | :---: | :--- | :--- | :--- | :--- |
| `tech` | 🛠️ | `IA, Ingeniería y Proyectos` | `AI, Engineering & Projects` | `IA, Ingeniería & Proyectos` | `AI, Engineering & Projects` |
| `strategy` | 📊 | `Estrategia y Operaciones` | `Strategy & Operations` | `Estrategia & Operaciones` | `Strategy & Operations` |
| `startups` | 🚀 | `Startups` | `Startups` | `Startups & Casos` | `Startups & Cases` |
| `pioneers` | 🏛️ | `Pioneros y Referentes` | `Pioneers & Icons` | `Pioneros & Referentes` | `Pioneers & Icons` |
| `culture` | 🎬 | `Cultura Tech y Media` | `Tech Culture & Media` | `Cultura Tech & Media` | `Tech Culture & Media` |

### INV-TAX-3: Paridad Lingüística Estricta (ES ⇔ EN)
Todo artículo en español con su contraparte en inglés debe compartir exactamente la misma categoría canónica correspondiente. Ningún par de posts puede tener categorías asimétricas.

### INV-TAX-4: Cobertura Completa sin Posts Huérfanos
En la home del portal (`layouts/partials/index_profile.html`):
$$\sum_{i=1}^{5} \text{Posts}(\text{Pilar}_i) = \text{Total Posts Publicados}$$
Ningún artículo publicado puede quedar fuera de las 5 pestañas por discrepancias tipográficas o de espacios en el front matter.

### INV-TAX-5: Compatibilidad con Datalaria Pulse
El escáner determinista `ops/pulse/build_index.py` debe leer las nuevas categorías sin errores de validación en Pydantic v2 y generar `static/apps/pulse/data/public.json` y `data/pulse/private/index.json` reflejando fielmente la nueva taxonomía.

### INV-TAX-6: Sección Blog (`/posts/`) y Cero Riesgo SEO (Crawler Safe Filtering)
La página de listado general del blog (`layouts/posts/section.html`) debe ofrecer una fila de filtros tipo *pills* (diseño homologado con la página de `/recursos/`) y buscador en tiempo real, cumpliendo de forma no negociable:
1. **Renderizado Directo en HTML (SEO 100%):** Todos los artículos publicados se renderizan como nodos completos `<div class="post-card">` con etiquetas semánticas de enlace `<a class="entry-link" href="...">` en el HTML estático inicial entregado por Hugo. Los rastreadores de Googlebot y de cualquier motor de búsqueda descubren e indexan todos los artículos sin toparse con muros de paginación o JavaScript obligatorio.
2. **Filtrado Client-Side Accesible:** El filtrado por píldoras temáticas (`data-theme`) y por texto en buscador se gestiona dinámicamente mediante CSS y DOM manipulation pura, preservando la visibilidad nativa cuando no hay JavaScript habilitado.
3. **Deep Linking por Query Parameters:** Admite parámetros URL (`?topic=tech`, `?q=agentes`, `?page=2`, `?size=12`) para enlazar directamente a vistas filtradas y paginadas de forma determinista.
4. **Paginación Dinámica con Selector de Densidad (12 / 24 / Todos):** La búsqueda y los filtros temáticos operan siempre sobre el 100% de los artículos en memoria. La paginación actúa como una lente de visualización reactiva que divide los resultados coincidentes y recalcula las páginas al instante, ofreciendo selector de densidad (`12`, `24`, `Todos`) y barra de paginación accesible al pie de la cuadrícula con scroll suave automático.

### INV-TAX-7: Directiva Robots `noindex, follow` y Exclusión de Sitemap en Archivos `/tags/`
Para erradicar la canibalización orgánica Post-vs-Tag en Google Search Console sin vulnerar `INV-TAX-1`:
1. **Resolución HTTP 200 y Enlaces Rastreables (`follow`):** Todas las páginas de taxonomía `/tags/` (listado raíz `/es/tags/`, `/en/tags/` y páginas de término `/es/tags/<term>/`, `/en/tags/<term>/`) DEBEN seguir compilándose, existiendo con HTTP `200` (`INV-TAX-1`) y manteniendo enlaces internos rastreables (`follow`).
2. **Directiva `noindex, follow` en Producción:** En entorno de producción (`hugo.IsProduction` o `site.Params.env == "production"`), toda página donde `eq .Data.Plural "tags"` DEBE emitir exactamente una etiqueta `<meta name="robots" content="noindex, follow">` (salvo que `.Params.robotsNoIndex` sea `true`, en cuyo caso emite `noindex, nofollow`).
3. **Exclusión de Sitemaps XML:** La plantilla `layouts/_default/sitemap.xml` DEBE filtrar las páginas donde `eq .Data.Plural "tags"` o `eq .Params.robotsNoIndex true`, garantizando que `es/sitemap.xml` y `en/sitemap.xml` únicamente anuncien a los buscadores URLs canónicas indexables.
4. **Preservación de Superficies Indexables:** Los artículos publicados (`/posts/*`), fichas de aplicaciones (`/apps/*`), catálogo (`/recursos/`, `/resources/`), páginas de categorías pilares (`/categories/*`) y portada mantienen `<meta name="robots" content="index, follow">` en producción.

---

## 3. Criterios de Verificación y Testing

1. **Integridad SEO & Taxonomías:** Script de auditoría que verifique que el 100% de los `tags` preexistentes en los 114 pares se mantienen intactos.
2. **Build Hugo:** `hugo --renderToMemory` finaliza con código de salida `0`.
3. **Suite Pytest de Pulse:** `pytest ops/pulse/tests/` pasa al 100% (cero regresiones en modelos).
4. **Validación de la Home:** Inspección del marcado HTML verificando la presencia de las 5 pestañas y la suma exacta de artículos.
5. **Validación de Sección Blog:** Comprobación automatizada de los 92 artículos renderizados en el DOM con enlaces canónicos válidos y distribución 48 + 8 + 13 + 12 + 11 = 92 en ES y EN, presencia de botones de densidad y barra de navegación de páginas.
6. **Validación Anti-Canibalización (`INV-TAX-7`):** Compilación Hugo verificando que `/es/tags/...` y `/en/tags/...` existen con `<meta name="robots" content="noindex, follow">` (etiqueta única) y están excluidos de `es/sitemap.xml` y `en/sitemap.xml`, mientras `/posts/*` mantienen `<meta name="robots" content="index, follow">` e inclusión en sitemap.

---

## 4. Registro de Verificación Ejecutada

- **Versión `1.0.0` (2026-10-31 · Checkpoint `sdd-checkpoint-pre-taxonomy-5cats`):**
  - `oxlint src`: 0 warnings, 0 errors.
  - `npm.cmd run build:portal` (Pulse): Bundle compilado sin advertencias a `static/apps/pulse/`.
  - `python -m ops.pulse.build_index` & `publish_public`: Salida `0`, `public.json` actualizado.
  - `pytest ops/pulse/tests/`: 18 tests pasados (100%).
  - `hugo --renderToMemory`: Salida `0`, 1115 páginas ES / 1100 páginas EN compiladas con éxito.
  - Auditoría de DOM en `/posts/`: 92 artículos renderizados con enlaces estándar `<a class="entry-link">` (100% rastreables), selector de densidad (12/24/Todos) y barra de paginación verificados en ES y EN.
- **Versión `1.1.0` (2026-11-21 · Hito 7.9 · Checkpoint `sdd-checkpoint-pre-7.9`):** `SECURITY_PASS` y `QA_PASS` verificados (`INV-TAX-7`):
  - `python -m ops.pulse.impact_analyzer`: Salida `0`, `1` alerta post-vs-post (`0` alertas `/tags/`).
  - `python -m pytest ops/pulse/tests ops/helix/tests -v`: `115/115 PASSED` (incluyendo compilación temporal `hugo -d <tmp>` certificando `<meta name="robots" content="noindex, follow">` único en `/tags/`, `index, follow` único en `/posts/*` y `/categories/`, y exclusión completa de `/tags/` en `es/sitemap.xml` y `en/sitemap.xml`).
  - `hugo --renderToMemory`: Salida `0`, `1.342` páginas ES / `1.337` páginas EN compiladas en `20.544 ms`.


