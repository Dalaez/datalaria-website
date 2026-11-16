# 🔁 Playbook Oficial de Ciclo de Series y Divulgación Controlada (`SPEC-SQUAD-SCRIBA`)

> **Versión:** `1.1.0` · **Estado:** `ACTIVE`  
> **Propietario:** [`E01-editorial-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E01-editorial-orchestrator.md) (en coordinación con `E02`–`E08`)  
> **Invariantes Vinculadas:** `INV-SCRIBA-1..5`, `INV-SCRIBA-SEO-SAFE`, `INV-SCRIBA-CHRONO`, `INV-AUTO-1..10`

---

## 1. Propósito Operativo
Establecer un **flujo reproducible en 2 Fases (Preparación Controlada → Push & Live tras OK humano)** para cada nuevo artículo perteneciente a una serie o pilar temático de Datalaria (*Proyecto Autopilot*, *Datalaria Pulse*, *Datalaria Helix*, *Estrategia & Operaciones*, *Pioneros y Referentes*, *Cultura Tech y Media*).

El objetivo es garantizar que cada entrega nueva herede **el estilo narrativo, la coherencia visual y los patrones que mejor convierten en GA4/GSC**, evitando publicaciones ciegas sin aprobación humana previa de las entradas de LinkedIn y X/Twitter.

---

## 2. Arquitectura del Ciclo en 2 Fases (`INV-SCRIBA-5`)

```mermaid
flowchart LR
    U1["Prompt 1: Tema / Serie"] --> A1["Fase A1 (E01 + E02)\nSerie previa + IMPACT_REPORT"]
    A1 --> A2["Fase A2 (E03 + E04 + E05)\nPost ES/EN + Cover + CTAs"]
    A2 --> A3["Fase A3 (E06 + E07)\nsocial_pack.yaml + DRY_RUN + Hugo"]
    A3 --> GATE{"Parada Obligatoria\nSugerencias LinkedIn + X + Brevo"}
    GATE -- "Ajustes" --> A3
    GATE -- "OK Humano (Prompt 2)" --> B1["Fase B1 (E08 / 12-DevOps)\ngit push + Netlify HTTP 200"]
    B1 --> B2["Fase B2\nworkflow_dispatch ES/EN + production"]
    B2 --> B3["Fase B3 (E02)\npulse.yml + impact_analyzer"]
```

---

## 3. FASE A — Inteligencia de Serie, Construcción y Propuesta Social (SIN `git push`)

1. **A1. Auditoría de Continuidad e Impacto (`E01` + `E02`):**
   - Leer los últimos 2–4 capítulos de la serie en `content/{es,en}/posts/` para capturar voz, hooks iniciales, formato de código/diagramas y estética de `cover.png`.
   - Consultar [`specs/audit/IMPACT_REPORT.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/audit/IMPACT_REPORT.md) y `data/pulse/private/metrics.json` para identificar qué enfoques y longitudes traccionan mejor dentro de esa serie/categoría y corregir errores históricos (p. ej. títulos `> 95` chars truncados).
2. **A2. Redacción Bilingüe, Portada, Diagramas PNG y Monetización Segura (`E03` + `E04` + `E05`):**
   - Crear `content/es/posts/<slug-es>/index.md` y `content/en/posts/<slug-en>/index.md` con `translationKey` idéntico, `title` en `[35, 95]` chars, `description` en `[75, 245]` chars y taxonomía completa (`INV-TAX-1`).
   - Generar `cover.png` (`1200×630 px`, foco centrado en *safe zone* coherente con la serie) en ambos bundles.
   - Si el artículo incluye diagramas `{{< mermaid >}}`, renderizar cada diagrama a PNG de alta resolución dentro del bundle y declararlo obligatoriamente en el shortcode (`{{< mermaid image="<diagrama>.png" alt="..." >}}`) para evitar código Mermaid sin renderizar en Dev.to y CoderLegion.
   - Insertar puentes `INV-SCRIBA-CHRONO` exclusivamente hacia recursos/apps/posts ya publicados (`draft: false` y `date <= hoy`). Si el artículo abre paso a un lanzamiento próximo bajo embargo, usar *teaser* narrativo sin enlaces rotos `404`.
3. **A3. Paquete Omnicanal y Gate Local (`E06` + `E07`):**
   - Crear `social_pack.yaml` (`es:` y `en:` con secciones `x`, `linkedin`, `newsletter`, `devto`, `coderlegion`) cumpliendo el esquema `SocialPack`.
   - Ejecutar `python -m ops.pulse.build_index`, `python -m ops.pulse.publish_public`, `DRY_RUN=true` con `orchestrator.py` sobre ES y EN (`Quality Gate Autopilot 2.0: PASS`), `pytest` y `hugo --renderToMemory`.
4. **A4. Parada Obligatoria (`Human-in-the-Loop`):**
   - **Prohibido hacer `git commit`, `git push` o disparar APIs Live en Fase A.**
   - Presentar al usuario el resumen SEO (`100/100`), portada verificada y las **sugerencias completas de LinkedIn (ES/EN), X/Twitter (gancho `< 200`, hilo `4–6` tweets y enlaces 1-clic `X Web Intent` coste `0 €`), Brevo 2.0 y Dev.to/CoderLegion**.

---

## 4. FASE B — Publicación Forzada y Cierre Analítico (Solo tras OK en Prompt 2)

1. **B1. Commit, Push y Verificación Pública:**
   - Aplicar eventuales retoques del usuario en `social_pack.yaml` o `index.md`, re-validar `DRY_RUN=true`, realizar commit atómico y ejecutar `git push origin main` para actualizar GitHub y Netlify.
   - Comprobar `HTTP 200` en las URLs públicas `https://datalaria.com/es/posts/...` y `https://datalaria.com/en/posts/...` antes de sindicar (`canonical_url` / `source_url`).
2. **B2. Despacho Controlado en 3 Olas durante 24h (`E08` — Opción C Híbrida):**
   - Nunca lanzar ES, EN, Dev.to y CoderLegion en el mismo minuto: tras el push conjunto en Hugo (`hreflang`), escalonar las olas en `data/editorial/dispatch_queue.yaml` o vía `workflow_dispatch`:
     - **Ola 1 (`T+0h` · `08:30 CET`, `1_es_native`):** LinkedIn ES + X ES + Brevo #3 (ES).
     - **Ola 2 (`T+7h` · `15:30 CET` / `09:30 EST`, `2_en_native`):** LinkedIn EN + X EN + Brevo #4 (EN).
     - **Ola 3A (`T+12h` · `20:30 CET`, `3a_es_syndication`):** Dev.to ES (con `canonical_url` ya indexado).
     - **Ola 3B (`T+22h` · `07:30 CET Día +1`, `3b_en_syndication`):** Dev.to EN + CoderLegion EN (`canonical_url` / `source_url` blindado).
   - Notificar al usuario si `environment: production` requiere aprobación, verificar logs de cada ola y entregar los enlaces finales más los clics directos de `X Web Intent`.
3. **B3. Retroalimentación Post-Publicación (`E02`):**
   - Ejecutar `gh workflow run pulse.yml` / `python -m ops.pulse.impact_analyzer` para actualizar [`specs/audit/IMPACT_REPORT.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/audit/IMPACT_REPORT.md) y nutrir las decisiones de la siguiente entrega.
