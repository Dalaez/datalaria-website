# _brand.md — Arquitectura de Marca, 3 Verticales y Guía de Voz (`Datalaria OS`)

> **Versión:** 1.0.0 · **Custodio Temporal (Estadio 1):** [`M01-revenue-orchestrator`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-mercator/M01-revenue-orchestrator.md) (traspasable a `M05` en Estadio 2) · **Decisión:** `ADR-034`  
> **Higiene Anti-Bloat:** Máximo `80` líneas. Fuente única del **Guild de Marca & Voz** para `04`, `08`, `E03`, `E04`, `E06` y `M01`–`M04`.

---

## 1. Posicionamiento Maestro (*Branded House*)
**Datalaria** es un laboratorio independiente de **Ingeniería Cuantitativa y Sistemas Agénticos Aplicados**: convertimos rigor matemático, arquitecturas deterministas y flujos de IA auditables en **herramientas ejecutivas, apps Dual-Mode y kits listos para producción**.

- **Promesa Central (EN):** *"Deterministic engineering, quantitative decision models & production-ready AI systems — zero hype, zero bloat."*
- **Promesa Central (ES):** *"Ingeniería determinista, modelos cuantitativos de decisión y sistemas de IA listos para producción — sin humo ni sobre-ingeniería."*

---

## 2. Arquitectura en 3 Verticales Canónicas (`brand_vertical`)
Para proteger la autoridad B2B C-Level y eliminar la dilución de marca entre suites corporativas y proyectos educativos/personales, todo activo de Datalaria pertenece exactamente a una vertical:

| Vertical (`brand_vertical`) | Audiencia Primaria | Activos Asignados (10 Apps + 21 Kits/Suites) | Rol Comercial |
| :--- | :--- | :--- | :--- |
| **1. `executive_b2b`**<br>*(Datalaria Executive B2B)* | Directores de Operaciones (COO), Supply Chain, PMO, CFO, Estrategia y Consultores. | **App:** `obs-management` (*Agentic Radar*).<br>**Kits/Suites:** `suite-01`, `suite-02`, `suite-03`, `mega-bundle`, `pack-dafo..pack-stock` (13 packs) y `pack-obs` (`19 €`, estreno 9 Dic). | **Motor principal de ingresos B2B** (Kits `5–39 €` + Licencias Equipo `99–249 €`). |
| **2. `ai_systems`**<br>*(Datalaria AI Systems)* | Tech Leads, Arquitectos, Product Builders, Equipos de Contenido/SEO y No-Devs con IA. | **Apps:** `pulse` (*Datalaria Pulse*), `helix` (*Datalaria Helix*, estreno 19 Ene 2027).<br>**Kits/Suites:** `pack-pulse` (`19 €`), `pack-sdd` / `suite-sdd` (`19 €`, estreno 19 Ene). | **Motor de diferenciación, autoridad IA y escala SaaS/Pro** (EN-first). |
| **3. `open_lab`**<br>*(Datalaria Open Lab)* | Comunidad técnica general, familias, estudiantes y visitantes orgánicos. | **Apps:** `weather`, `lifeops`, `reading` (16 Dic), `maths`, `flashcards`, `conversor`, `snake`. | **Escaparate de ingeniería, viralidad orgánica y backlinks** (nunca mezclado visualmente encima del catálogo B2B). |

---

## 3. Reglas de Jerarquía Visual y Mensajería
1. **Orden de Prioridad en Escaparates Públicos (Home, `/apps/`, `/recursos/`, LinkedIn):** Siempre **1.° `executive_b2b`** + **2.° `ai_systems`** arriba (above the fold), y **3.° `open_lab`** en bloque secundario claramente etiquetado.
2. **Tono y Voz Bilingüe (`ES ⇔ EN`):**
   - **Directivo y Empírico:** Cifras reales, fórmulas verificables, capturas auténticas (`1600×980 px`) y casos reales (*Caso Crisol*, *MarginGuard*, *IEC 62402*).
   - **Antihumo:** Prohibido prometer "hazte rico con IA", usar adjetivos vacíos (*revolucionario*, *disruptivo*, *mágico*) o inflar métricas sin muestra suficiente (`ADR-023`).
   - **Localización EN Nativa:** El inglés no es traducción literal del español; adopta terminología estándar internacional (*Lead Time*, *Safety Stock*, *Spec-Driven Development*, *Content Ops*).
3. **Coherencia Visual:** Modo oscuro ejecutivo (`#0b0f17` / tokens `design.md`) en *Executive B2B* y *AI Systems*; estética lúdica aislada (`Consumer Playful`) exclusivamente en sub-apps EdTech/Arcade de *Open Lab*.
4. **Embargo y Veracidad:** Ninguna comunicación de marca puede promocionar activos `status: incubating` o `coming` como disponibles antes de su `launch_date` (`INV-AUTO-6`).
