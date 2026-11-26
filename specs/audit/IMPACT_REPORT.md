# 📈 Primera Auditoría Estratégica de Impacto SEO, Tráfico y Monetización (E02)

> **Autor:** [`E02-seo-impact-strategist`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E02-seo-impact-strategist.md) · **Célula:** Dirección & Inteligencia Estratégica  
> **Fecha de Emisión:** 2026-11-26 12:04 UTC  
> **Fuentes de Verdad:** `data/pulse/private/index.json` (190 activos), `metrics.json` (GA4 + GSC 30d/prev 30d), `channel_metrics.json` (GA4 Acquisition + KeyEvents), `social_metrics.json` (Dev.to + CoderLegion APIs gratuitas), `distribution_ledger.json`, `gsc_queries.json`, `monthly_metrics.json` (14 meses) y `backlog.yaml`.  
> **Invariantes:** Cumple estrictamente `INV-PULSE-6`, `INV-PULSE-11`, `INV-PULSE-12` (`ADR-033`, coste `0 €`) y Constitución Art. 1.3 (*Separación Cerebro vs. Músculo Cuantitativo*).

---

## 1. Resumen Ejecutivo y Estado del Catálogo

| Métrica Macro | Valor Cuantitativo Real | Interpretación Estratégica E02 |
| :--- | :---: | :--- |
| **Total Activos Consolidados** | **190 activos** | 124 Posts bilingües (`111` publicados, `11` programados, `2` drafts), `10` Apps base y `21` Kits/Suites. |
| **Tráfico Acumulado Posts (30d)** | **2,361 vistas** | Cuota inglés (EN): **50.8%** · Mediana: **10.0** · $P_{75}$: **26.0**. |
| **Visibilidad Orgánica GSC (30d)** | **21,789 imp. · 130 clics** | CTR medio: **0.60%** · Posición media ponderada: **10.1** · Cuota EN (imp.): **72.0%** · Prev 30d: `12,585` imp. / `71` clics · Marca (`datalaria`): `701` imp. / `0` clics. |
| **Crecimiento Interanual (YoY)** | **+2182.5%** | De 200 vistas (2025-10) a 4,565 vistas (2026-11). |
| **Quick Wins de CTR / SERP** | **68 oportunidades** | `61` con impresiones reales GSC (`pos 4..20` o `CTR < 2.5%`) + truncamientos SERP. |
| **Canibalización de Keywords** | **1 alertas** | Consultas GSC donde `>= 2` URLs del mismo idioma compiten por impresiones. |
| **Huérfanos de Monetización** | **1 posts top** | Posts en el cuartil superior ($P_{75} \ge 26$) sin enlace ni shortcode a Kit/App. |
| **Score Promedio del Backlog** | **79.1 / 100** | 6 propuestas estratégicas evaluadas por Editorial ROI Score. |
| **Lectura Doble Capa (`00B` / `ADR-035`)** | **615 ses. externas netas** | Bruto GA4 intacto: `3,184` · Asistentes IA (GEO): **26** · Ruido excluido: `localhost` `108` + spam `127` (`aocr.org`) · Marca real GSC (sin `site:`): `0` imp. / `0` clics (`site:`: `722` imp.). |

```mermaid
flowchart TD
    A["111 Artículos Publicados\n(2,361 vistas · 21,789 imp. GSC)"] --> B{"Triaje de Impacto E02"}
    B --> C["68 Quick Wins de CTR\n(61 oportunidades GSC reales)"]
    B --> D["1 Huérfanos de Monetización\n(Cuartil Superior >= 26 vistas sin Kit)"]
    B --> E["5 Categorías Evaluadas\n(Líder: Estrategia y Operaciones (88.9%))"]
    B --> H["1 Alertas Canibalización GSC"]
    C --> F["Acción E04: Reescritura Títulos & H1 (35-95)"]
    D --> G["Acción E05: Inyección app-ref y Kits 19€"]
```

---

## 2. Rendimiento, GSC y Cobertura de Monetización por Categoría (ES vs. EN)

| Categoría Oficial | Posts | Vistas 30d | % EN (Vistas) | Imp. GSC | Clics GSC | CTR GSC | Eng. Medio | Monetizados | Cobertura % | Editorial ROI Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Estrategia y Operaciones** | 18 | 674 (37.4/p) | 40.5% | 1,342 | 13 | 0.97% | 15.3s | 16/18 | **88.9%** | **77.0** |
| **Pioneros y Referentes** | 13 | 329 (25.3/p) | 60.5% | 8,573 | 41 | 0.48% | 26.0s | 7/13 | **53.8%** | **63.4** |
| **Startups** | 14 | 204 (14.6/p) | 67.6% | 4,946 | 41 | 0.83% | 43.2s | 6/14 | **42.9%** | **53.7** |
| **IA, Ingeniería y Proyectos** | 54 | 1015 (18.8/p) | 49.8% | 4,644 | 23 | 0.50% | 12.8s | 28/54 | **51.9%** | **52.7** |
| **Cultura Tech y Media** | 12 | 139 (11.6/p) | 61.2% | 2,284 | 12 | 0.53% | 15.7s | 5/12 | **41.7%** | **37.3** |

### Diagnóstico Estratégico de Categorías:
1. **Estrategia y Operaciones (Editorial ROI 77.0):** **37.4 vistas/post**, **1,342 impresiones GSC** (CTR **0.97%**), cuota inglés **40.5%** y **88.9%** de cobertura comercial (16/18).
2. **Pioneros y Referentes (Editorial ROI 63.4):** **25.3 vistas/post**, **8,573 impresiones GSC** (CTR **0.48%**), cuota inglés **60.5%** y **53.8%** de cobertura comercial (7/13).
3. **Startups (Editorial ROI 53.7):** **14.6 vistas/post**, **4,946 impresiones GSC** (CTR **0.83%**), cuota inglés **67.6%** y **42.9%** de cobertura comercial (6/14).

---

## 3. Matriz de Quick Wins de CTR (Top Oportunidades en Buscadores)

Artículos priorizados combinando datos reales de **Google Search Console** (impresiones, posición media y CTR) con longitud de snippet y retención en GA4:

| ID / Activo | Top Query GSC | Imp. GSC | Pos. / CTR | Vistas 30d | Tipo de Oportunidad | Título Recomendado ES (35–95 chars) |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| [`kantorovich`](kantorovich) | `leonid kantorovich` | **3,249** | `7.5` / `0.4%` | 47 | `gsc_position_4_20` | **Leonid Kantorovich: El Matemático que Desafió a Stalin con la Programación Lineal** |
| [`safety-stock-reorder-point-calculator`](calculadora-stock-seguridad-rop) | — | **0** | — | 88 | `serp_snippet_truncation` | **Calculadora de Stock de Seguridad & ROP: Optimización de Inventario y Working Capital de Grado** |
| [`john_von_neumann`](john_von_neumann) | `john von neumann` | **1,933** | `8.9` / `0.5%` | 43 | `gsc_position_4_20` | **John von Neumann: Arquitectura de Computadores, Teoría de Juegos y Singularidad** |
| [`agentes_ia_operativa_sdd`](agentes_ia_operativa_sdd) | `sdd agents` | **14** | `11.3` / `7.1%` | 63 | `serp_snippet_truncation` | **Cómo Crear Agentes de IA para la Operativa Empresarial del Día a Día: De los SOPs al** |
| [`happyrobot`](happyrobot) | `happyrobot vs. other ai voice agents` | **1,280** | `6.9` / `0.3%` | 26 | `gsc_position_4_20` | **HappyRobot: Cómo los Agentes de Voz Autónomos Conquistaron la Logística Global** |
| [`pgvector_vs_vectordb`](pgvector_vs_vectordb) | `pgvector` | **1,500** | `11.1` / `0.5%` | 14 | `gsc_position_4_20` | **PostgreSQL con pgvector vs Vector DBs: Por Qué Casi Nadie Necesita Pinecone** |
| [`halt_and_catch_fire`](halt_and_catch_fire) | `halt and catch fire meaning` | **908** | `7.2` / `0.4%` | 8 | `gsc_position_4_20` | **Halt and Catch Fire: Significado, Historia y por Qué Clavó la Ingeniería de Software** |
| [`wallapop`](wallapop) | `wallapop` | **624** | `5.7` / `2.4%` | 20 | `gsc_position_4_20` | **Wallapop: La Ingeniería Invisible detrás del Mayor Marketplace Circular de Europa** |
| [`silicon_valley`](silicon_valley) | `pipernet` | **622** | `6.2` / `1.0%` | 27 | `gsc_position_4_20` | **Silicon Valley y el Dilema de PiperNet: La Profecía de la IA y Agentes Reales** |
| [`ravenpack`](ravenpack) | `ravenpack vs bloomberg` | **553** | `6.0` / `0.7%` | 34 | `gsc_position_4_20` | **RavenPack: De la Analítica de Noticias en Marbella al Cerebro de Wall Street** |
| [`freepik`](freepik) | `does freepik work well for mid-market companies modernizing their operations and reducing operational costs in a competitive landscape?` | **527** | `5.9` / `0.0%` | 10 | `gsc_position_4_20` | **Freepik: El Gigante que Domó la IA y Transformó las Operaciones Creativas Globales** |
| [`the_thinking_game`](the_thinking_game) | `the thinking game` | **510** | `7.3` / `0.4%` | 9 | `gsc_position_4_20` | **The Thinking Game: El Documental de DeepMind, Demis Hassabis, AlphaFold y la AGI** |

---

## 4. Auditoría de Huérfanos de Monetización (Cuartil Superior de Tráfico)

Artículos en el cuartil superior ($P_{75} \ge 26$ vistas) que actualmente no enlazan a ningún Kit de Lemon Squeezy ni a ninguna App de Datalaria:

| ID del Post | Vistas 30d | Percentil | Tipo de Puente | Destino Asignado | Shortcode / Enlace Recomendado | Justificación Estratégica E02 |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| [`stack_productividad_2026`](stack_productividad_2026) | **97** | Top 2% | `helix_waitlist` | `helix` | `{{< helix-waitlist >}}` | Tráfico de alta retención técnica; dirigir hacia la lista de espera de Datalaria Helix. |

---

## 5. Priorización del Backlog Prospectivo (`Editorial ROI Score`)

Ideas de contenido futuro en `data/editorial/backlog.yaml` ordenadas determinísticamente por la fórmula de ROI editorial de `E02`:

$$\text{Editorial ROI Score} = 0.40 \times \text{Demanda SEO} + 0.35 \times \text{Fit Monetización} + 0.25 \times \text{Sinergia Ecosistema}$$

| Pos. | ID de Idea | Título Propuesto | Categoría | Target de Negocio | SEO | Mon. | Sin. | Editorial ROI |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **#1** | `idea-claude-subagents-sdd-contracts` | Anatomía de un Escuadrón de Subagentes con Derecho a Veto: De Prompts Frágiles a Contratos Pydantic | IA, Ingeniería y Proyectos | `helix` | 92 | 96 | 98 | **88.3** |
| **#2** | `idea-monte-carlo-capex-risk` | Simulación de Monte Carlo en Excel y Python para Business Cases: Más Allá del VAN Determinista | Estrategia y Operaciones | `pack-business-case` | 82 | 95 | 88 | **82.5** |
| **#3** | `idea-pareto-multiobjective-portfolio` | Frontera Eficiente de Pareto en Priorización de Producto: Combinando RICE, DAR y Presupuesto | Estrategia y Operaciones | `suite-02` | 78 | 92 | 90 | **80.6** |
| **#4** | `idea-little-law-kingman-ops` | Ley de Little y Fórmula de Kingman en Operaciones: Por Qué Tu Backlog Colapsa al 85% de Carga | Estrategia y Operaciones | `suite-03` | 75 | 88 | 85 | **77.3** |
| **#5** | `idea-edsger-dijkstra-formal-verification` | Edsger Dijkstra: La Cruzada contra el GOTO, la Verificación Formal y por qué Habría Vetado el Vibe Coding | Pioneros y Referentes | `helix` | 80 | 82 | 92 | **74.2** |
| **#6** | `idea-claude-shannon-information-theory` | Claude Shannon: El Padre de la Teoría de la Información, la Entropía en LLMs y el Malabarista del Bell Labs | Pioneros y Referentes | `flashcards` | 85 | 75 | 82 | **71.9** |

---

## 6. Impacto Editorial de Lanzamientos de Apps, Versiones y Kits B2B (Gobernanza Scriba)

> **Invariantes SDD:** Supervisión determinista de estrenos (`initial_launch`, `kit_launch`) y versiones evolutivas (`version_upgrade`, `kit_edition`).  
> **Balance General:** 66 activos evaluados · **15 alerta(s) de release silenciosa** · 5 cobertura(s) programada(s) · 44 cubierto(s) al 100%.

| Activo / ID | Tipo & Versión | Fecha Estreno | Estado Portal | Posts | Último Post | Vistas 30d | Cobertura Scriba | Acción Recomendada |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `weather-v3.3.0` | `version_upgrade` (v3.3.0) | 2026-11-13 | `published` | 4 | 2025-12-06 | 41 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v3.3.0 (2026-11-13) posterior al último post (2025-12-06); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `weather-v3.2.0` | `version_upgrade` (v3.2.0) | 2026-11-13 | `published` | 4 | 2025-12-06 | 41 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v3.2.0 (2026-11-13) posterior al último post (2025-12-06); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `weather-v3.1.0` | `version_upgrade` (v3.1.0) | 2026-11-09 | `published` | 4 | 2025-12-06 | 41 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v3.1.0 (2026-11-09) posterior al último post (2025-12-06); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `weather-v3.0.0` | `version_upgrade` (v3.0.0) | 2026-11-08 | `published` | 4 | 2025-12-06 | 41 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v3.0.0 (2026-11-08) posterior al último post (2025-12-06); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `weather-v2.0.0` | `version_upgrade` (v2.0.0) | 2026-11-08 | `published` | 4 | 2025-12-06 | 41 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.0.0 (2026-11-08) posterior al último post (2025-12-06); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `snake-v2.3.0` | `version_upgrade` (v2.3.0) | 2026-11-07 | `published` | 1 | 2026-02-14 | 24 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.3.0 (2026-11-07) posterior al último post (2026-02-14); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `snake-v2.2.0` | `version_upgrade` (v2.2.0) | 2026-11-07 | `published` | 1 | 2026-02-14 | 24 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.2.0 (2026-11-07) posterior al último post (2026-02-14); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `snake-v2.1.0` | `version_upgrade` (v2.1.0) | 2026-11-07 | `published` | 1 | 2026-02-14 | 24 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.1.0 (2026-11-07) posterior al último post (2026-02-14); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `snake-v2.0.0` | `version_upgrade` (v2.0.0) | 2026-11-07 | `published` | 1 | 2026-02-14 | 24 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.0.0 (2026-11-07) posterior al último post (2026-02-14); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `flashcards-v2.1.0` | `version_upgrade` (v2.1.0) | 2026-11-06 | `published` | 1 | 2025-10-17 | 6 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.1.0 (2026-11-06) posterior al último post (2025-10-17); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `flashcards-v2.0.0` | `version_upgrade` (v2.0.0) | 2026-11-06 | `published` | 1 | 2025-10-17 | 6 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.0.0 (2026-11-06) posterior al último post (2025-10-17); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `maths-v2.3.0` | `version_upgrade` (v2.3.0) | 2026-11-06 | `published` | 1 | 2025-09-11 | 0 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.3.0 (2026-11-06) posterior al último post (2025-09-11); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `maths-v2.2.0` | `version_upgrade` (v2.2.0) | 2026-11-06 | `published` | 1 | 2025-09-11 | 0 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.2.0 (2026-11-06) posterior al último post (2025-09-11); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `maths-v2.1.0` | `version_upgrade` (v2.1.0) | 2026-11-05 | `published` | 1 | 2025-09-11 | 0 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.1.0 (2026-11-05) posterior al último post (2025-09-11); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `maths-v2.0.0` | `version_upgrade` (v2.0.0) | 2026-11-05 | `published` | 1 | 2025-09-11 | 0 | 🔴 Alerta Silenciosa | Alerta de release silenciosa: versión v2.0.0 (2026-11-05) posterior al último post (2025-09-11); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0. |
| `reading` | `initial_launch` (v1.1.0) | 2026-12-16 | `scheduled` | 0 | Ninguno | 0 | 🟡 Lanzamiento Pendiente | Lanzamiento programado el 2026-12-16: coordinar con E01/E03 redacción anticipada de tutorial o post guía. |
| `pack-obs` | `kit_launch` (v2.0.0) | 2026-12-09 | `scheduled` | 0 | Ninguno | 0 | 🟡 Lanzamiento Pendiente | Lanzamiento programado el 2026-12-09: coordinar con E01/E03 redacción anticipada de tutorial o post guía. |
| `pack-sdd` | `kit_launch` (v1.0.0) | 2027-01-19 | `scheduled` | 5 | 2026-11-11 | 184 | 🟢 Cobertura Programada | Campaña programada: coordinar con E06 sindicación omnicanal para el estreno el 2027-01-19. |
| `suite-sdd` | `kit_launch` (v1.0.0) | 2027-01-19 | `scheduled` | 3 | 2026-11-11 | 183 | 🟢 Cobertura Programada | Campaña programada: coordinar con E06 sindicación omnicanal para el estreno el 2027-01-19. |
| `helix` | `initial_launch` (v1.0.0) | 2027-01-19 | `scheduled` | 5 | Ninguno | 4 | 🟢 Cobertura Programada | Campaña programada: coordinar con E06 sindicación omnicanal para el estreno el 2027-01-19. |
| `mega-bundle` | `kit_launch` (v1.0.0) | 2026-12-03 | `scheduled` | 1 | Ninguno | 0 | 🟢 Cobertura Programada | Campaña programada: coordinar con E06 sindicación omnicanal para el estreno el 2026-12-03. |
| `suite-03` | `kit_launch` (v1.0.0) | 2026-11-30 | `scheduled` | 1 | Ninguno | 0 | 🟢 Cobertura Programada | Campaña programada: coordinar con E06 sindicación omnicanal para el estreno el 2026-11-30. |
| `obs-management` | `initial_launch` (v2.0.0) | 2026-05-17 | `published` | 20 | 2026-11-26 | 426 | ✅ Cubierto | Activo cubierto con 20 post(s) en producción (426 vistas/30d). |
| `obs-management-v2.0.0` | `version_upgrade` (v2.0.0) | 2026-11-22 | `published` | 20 | 2026-11-26 | 426 | ✅ Cubierto | Versión v2.0.0 respaldada por los artículos de la serie. |
| `obs-management-v1.0.1` | `version_upgrade` (v1.0.1) | 2026-10-24 | `published` | 20 | 2026-11-26 | 426 | ✅ Cubierto | Versión v1.0.1 respaldada por los artículos de la serie. |
| `pulse` | `initial_launch` (v1.6.0) | 2026-11-18 | `published` | 7 | 2026-11-25 | 341 | ✅ Cubierto | Activo cubierto con 7 post(s) en producción (341 vistas/30d). |
| `pulse-v1.6.0` | `version_upgrade` (v1.6.0) | 2026-11-24 | `published` | 7 | 2026-11-25 | 341 | ✅ Cubierto | Versión v1.6.0 respaldada por los artículos de la serie. |
| `pulse-v1.5.0` | `version_upgrade` (v1.5.0) | 2026-11-23 | `published` | 7 | 2026-11-25 | 341 | ✅ Cubierto | Versión v1.5.0 respaldada por los artículos de la serie. |
| `pack-pulse` | `kit_launch` (v1.0.0) | 2026-11-18 | `published` | 4 | 2026-11-25 | 292 | ✅ Cubierto | Activo cubierto con 4 post(s) en producción (292 vistas/30d). |
| `suite-02` | `kit_launch` (v1.0.0) | 2026-11-08 | `published` | 4 | 2026-11-08 | 165 | ✅ Cubierto | Activo cubierto con 4 post(s) en producción (165 vistas/30d). |
| `pack-business-case` | `kit_launch` (v1.0.0) | 2026-11-08 | `published` | 4 | 2026-11-21 | 144 | ✅ Cubierto | Activo cubierto con 4 post(s) en producción (144 vistas/30d). |
| `suite-01` | `kit_launch` (v1.0.0) | 2026-11-01 | `published` | 3 | 2026-11-01 | 105 | ✅ Cubierto | Activo cubierto con 3 post(s) en producción (105 vistas/30d). |
| `pack-stock` | `kit_launch` (v1.0.0) | 2026-11-26 | `published` | 1 | 2026-11-26 | 88 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (88 vistas/30d). |
| `pack-rice` | `kit_launch` (v1.0.0) | 2026-11-05 | `published` | 1 | 2026-11-05 | 76 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (76 vistas/30d). |
| `lifeops` | `initial_launch` (v1.2.0) | 2026-09-19 | `published` | 6 | 2026-10-28 | 73 | ✅ Cubierto | Activo cubierto con 6 post(s) en producción (73 vistas/30d). |
| `lifeops-v1.1.1` | `version_upgrade` (v1.1.1) | 2026-10-27 | `published` | 6 | 2026-10-28 | 73 | ✅ Cubierto | Versión v1.1.1 respaldada por los artículos de la serie. |
| `lifeops-v1.1.0` | `version_upgrade` (v1.1.0) | 2026-10-27 | `published` | 6 | 2026-10-28 | 73 | ✅ Cubierto | Versión v1.1.0 cubierta con artículo propio publicado (app-lifeops_part6_analytics_dashboard_360). |
| `lifeops-v1.0.1` | `version_upgrade` (v1.0.1) | 2026-10-24 | `published` | 6 | 2026-10-28 | 73 | ✅ Cubierto | Versión v1.0.1 respaldada por los artículos de la serie. |
| `lifeops-v0.4.0` | `version_upgrade` (v0.4.0) | 2026-08-31 | `published` | 6 | 2026-10-28 | 73 | ✅ Cubierto | Versión v0.4.0 respaldada por los artículos de la serie. |
| `lifeops-v0.3.0` | `version_upgrade` (v0.3.0) | 2026-08-30 | `published` | 6 | 2026-10-28 | 73 | ✅ Cubierto | Versión v0.3.0 respaldada por los artículos de la serie. |
| `lifeops-v0.1.0` | `version_upgrade` (v0.1.0) | 2026-08-29 | `published` | 6 | 2026-10-28 | 73 | ✅ Cubierto | Versión v0.1.0 respaldada por los artículos de la serie. |
| `pack-dar` | `kit_launch` (v1.0.0) | 2026-11-02 | `published` | 1 | 2026-11-02 | 54 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (54 vistas/30d). |
| `weather` | `initial_launch` (v3.3.3) | 2025-10-25 | `published` | 4 | 2025-12-06 | 41 | ✅ Cubierto | Activo cubierto con 4 post(s) en producción (41 vistas/30d). |
| `weather-v1.0.0` | `version_upgrade` (v1.0.0) | 2025-12-06 | `published` | 4 | 2025-12-06 | 41 | ✅ Cubierto | Versión v1.0.0 respaldada por los artículos de la serie. |
| `weather-v0.3.0` | `version_upgrade` (v0.3.0) | 2025-11-15 | `published` | 4 | 2025-12-06 | 41 | ✅ Cubierto | Versión v0.3.0 respaldada por los artículos de la serie. |
| `weather-v0.2.0` | `version_upgrade` (v0.2.0) | 2025-11-08 | `published` | 4 | 2025-12-06 | 41 | ✅ Cubierto | Versión v0.2.0 respaldada por los artículos de la serie. |
| `weather-v0.1.0` | `version_upgrade` (v0.1.0) | 2025-10-31 | `published` | 4 | 2025-12-06 | 41 | ✅ Cubierto | Versión v0.1.0 respaldada por los artículos de la serie. |
| `pack-raci` | `kit_launch` (v1.0.0) | 2026-11-12 | `published` | 1 | 2026-11-12 | 41 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (41 vistas/30d). |
| `pack-mckinsey` | `kit_launch` (v1.0.0) | 2026-10-29 | `published` | 1 | 2026-10-29 | 40 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (40 vistas/30d). |
| `pack-evm` | `kit_launch` (v1.0.0) | 2026-11-23 | `published` | 1 | 2026-11-23 | 40 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (40 vistas/30d). |
| `pack-amfe` | `kit_launch` (v1.0.0) | 2026-11-16 | `published` | 1 | 2026-11-16 | 37 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (37 vistas/30d). |
| `pack-dafo` | `kit_launch` (v1.0.0) | 2026-10-19 | `published` | 1 | 2026-10-13 | 26 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (26 vistas/30d). |
| `pack-bcg` | `kit_launch` (v1.0.0) | 2026-10-26 | `published` | 1 | 2026-10-26 | 26 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (26 vistas/30d). |
| `snake` | `initial_launch` (v2.3.1) | 2026-02-14 | `published` | 1 | 2026-02-14 | 24 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (24 vistas/30d). |
| `snake-v0.5.0` | `version_upgrade` (v0.5.0) | 2026-02-01 | `published` | 1 | 2026-02-14 | 24 | ✅ Cubierto | Versión v0.5.0 respaldada por los artículos de la serie. |
| `snake-v0.1.0` | `version_upgrade` (v0.1.0) | 2026-01-20 | `published` | 1 | 2026-02-14 | 24 | ✅ Cubierto | Versión v0.1.0 respaldada por los artículos de la serie. |
| `pack-pert` | `kit_launch` (v1.0.0) | 2026-11-19 | `published` | 1 | 2026-11-19 | 18 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (18 vistas/30d). |
| `pack-porter` | `kit_launch` (v1.0.0) | 2026-10-21 | `published` | 1 | 2026-10-19 | 14 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (14 vistas/30d). |
| `pack-pestel` | `kit_launch` (v1.0.0) | 2026-10-22 | `published` | 1 | 2026-10-22 | 10 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (10 vistas/30d). |
| `conversor` | `initial_launch` (v2.1.0) | 2025-10-04 | `published` | 1 | 2025-10-04 | 8 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (8 vistas/30d). |
| `conversor-v0.5.0` | `version_upgrade` (v0.5.0) | 2025-09-28 | `published` | 1 | 2025-10-04 | 8 | ✅ Cubierto | Versión v0.5.0 respaldada por los artículos de la serie. |
| `conversor-v0.1.0` | `version_upgrade` (v0.1.0) | 2025-09-20 | `published` | 1 | 2025-10-04 | 8 | ✅ Cubierto | Versión v0.1.0 respaldada por los artículos de la serie. |
| `flashcards` | `initial_launch` (v2.1.0) | 2025-10-17 | `published` | 1 | 2025-10-17 | 6 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (6 vistas/30d). |
| `maths` | `initial_launch` (v2.3.0) | 2025-09-11 | `published` | 1 | 2025-09-11 | 0 | ✅ Cubierto | Activo cubierto con 1 post(s) en producción (0 vistas/30d). |
| `maths-v0.5.0` | `version_upgrade` (v0.5.0) | 2025-09-05 | `published` | 1 | 2025-09-11 | 0 | ✅ Cubierto | Versión v0.5.0 respaldada por los artículos de la serie. |
| `maths-v0.1.0` | `version_upgrade` (v0.1.0) | 2025-08-28 | `published` | 1 | 2025-09-11 | 0 | ✅ Cubierto | Versión v0.1.0 respaldada por los artículos de la serie. |

---

## 7. Auditoría de Canibalización de Keywords (GSC)

Consultas reales de Search Console donde `>= 2` URLs del mismo idioma compiten por impresiones:

| Query | Idioma | Imp. Totales | Clics | URLs en Competencia (Top 3) | Acción Recomendada E02 |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `grafo de conocimiento vs base de datos vectorial` | `es` | **90** | 0 | `/es/posts/graphrag` (66 imp, pos 16.2) · `/es/posts/pgvector_vs_vectordb` (24 imp, pos 7.0) | Consolidar intención en /es/posts/graphrag con enlaces internos desde las URLs secundarias o diferenciar ángulo/H1. |

---

## 8. Rendimiento por Canal de Adquisición (ES vs. EN) — Coste 0 € (`ADR-033`)

> **Política `INV-PULSE-12`:** Atribución unificada vía GA4 Acquisition + UTMs (`linkedin`, `x`, `devto`, `coderlegion`, `newsletter`, `google_organic`, `direct`). **X/Twitter nativo permanece en stand-by (coste `0 €`)**; **LinkedIn cubre exclusivamente la Página de Empresa**.

| Canal Canónico | Sesiones 30d | ES / EN | % EN | Δ 30d | Eng. Rate % | Eng. Medio | Eventos Clave | Conv. % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`direct`** | **2,334** | 1103 / 1200 | 52.1% | +129.7% | 27.4% | 9.7s | 8 | 0.34% |
| **`other`** | **359** | 185 / 172 | 48.2% | +385.1% | 40.9% | 21.7s | 2 | 0.56% |
| **`google_organic`** | **250** | 133 / 117 | 46.8% | +78.6% | 52.8% | 38.0s | 0 | 0.00% |
| **`linkedin`** | **132** | 75 / 57 | 43.2% | +200.0% | 83.3% | 9.3s | 2 | 1.52% |
| **`x`** | **56** | 36 / 20 | 35.7% | +500.0% | 82.1% | 8.8s | 0 | 0.00% |
| **`coderlegion`** | **41** | 13 / 28 | 68.3% | +500.0% | 90.2% | 6.1s | 0 | 0.00% |
| **`newsletter`** | **11** | 10 / 1 | 9.1% | +266.7% | 54.5% | 1.8s | 0 | 0.00% |
| **`devto`** | **1** | 1 / 0 | 0.0% | +100.0% | 100.0% | 16.0s | 0 | 0.00% |

### 🏆 Ganadores Ocultos por Canal (Candidatos a Ola de Reciclaje +21d en `E06`)

| Activo / ID | Canal | Sesiones 30d | Eng. Medio | Eventos Clave | Acción Recomendada E06 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| — | — | 0 | 0.0s | 0 | ✅ Sin ganadores ocultos pendientes con umbral (`>= 45s` o conv., `< 30` sesiones). |

### 🕵️ Alertas de *Dark Social* / Fuga de Atribución UTM

| Tipo Alerta | Severidad | Despacho / Canal | Direct Actual vs. Base | Pico % | Acción Recomendada |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `dark_social_spike` | 🔴 Alta | `magnific-ai-2026-11-21-wave1-es-native` | 206 vs. 114.0 | **+80.7%** | Pico +81% de tráfico (direct) tras despacho 'magnific-ai-2026-11-21-wave1-es-native' con solo 3 sesiones UTM en [linkedin,x]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `magnific-ai-2026-11-21-wave2-en-native` | 206 vs. 114.0 | **+80.7%** | Pico +81% de tráfico (direct) tras despacho 'magnific-ai-2026-11-21-wave2-en-native' con solo 3 sesiones UTM en [linkedin,x]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `magnific-ai-2026-11-21-wave3a-es-devto` | 206 vs. 114.0 | **+80.7%** | Pico +81% de tráfico (direct) tras despacho 'magnific-ai-2026-11-21-wave3a-es-devto' con solo 0 sesiones UTM en [devto]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `magnific-ai-2026-11-21-wave3b-en-syndication` | 206 vs. 114.0 | **+80.7%** | Pico +81% de tráfico (direct) tras despacho 'magnific-ai-2026-11-21-wave3b-en-syndication' con solo 0 sesiones UTM en [devto,coderlegion]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `pulse-part2-2026-11-22-wave1-es-native` | 206 vs. 114.0 | **+80.7%** | Pico +81% de tráfico (direct) tras despacho 'pulse-part2-2026-11-22-wave1-es-native' con solo 2 sesiones UTM en [linkedin,x]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `pulse-part2-2026-11-22-wave2-en-native` | 206 vs. 114.0 | **+80.7%** | Pico +81% de tráfico (direct) tras despacho 'pulse-part2-2026-11-22-wave2-en-native' con solo 2 sesiones UTM en [linkedin,x]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `pulse-part2-2026-11-22-wave3a-es-devto` | 206 vs. 114.0 | **+80.7%** | Pico +81% de tráfico (direct) tras despacho 'pulse-part2-2026-11-22-wave3a-es-devto' con solo 0 sesiones UTM en [devto]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `pulse-part2-2026-11-22-wave3b-en-syndication` | 226 vs. 114.0 | **+98.2%** | Pico +98% de tráfico (direct) tras despacho 'pulse-part2-2026-11-22-wave3b-en-syndication' con solo 0 sesiones UTM en [devto,coderlegion]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `evm-2026-11-23-2026-11-23-wave2-en-native` | 226 vs. 114.0 | **+98.2%** | Pico +98% de tráfico (direct) tras despacho 'evm-2026-11-23-2026-11-23-wave2-en-native' con solo 0 sesiones UTM en [linkedin,x]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `evm-2026-11-23-2026-11-23-wave3a-es-devto` | 179 vs. 114.0 | **+57.0%** | Pico +57% de tráfico (direct) tras despacho 'evm-2026-11-23-2026-11-23-wave3a-es-devto' con solo 0 sesiones UTM en [devto]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `dark_social_spike` | 🔴 Alta | `evm-2026-11-23-2026-11-23-wave3b-en-syndication` | 179 vs. 114.0 | **+57.0%** | Pico +57% de tráfico (direct) tras despacho 'evm-2026-11-23-2026-11-23-wave3b-en-syndication' con solo 0 sesiones UTM en [devto,coderlegion]. Verificar UTMs ADR-033 en enlaces compartidos. |
| `high_direct_share` | 🟡 Media | `linkedin,x,devto,coderlegion` | 2334 vs. 1016.0 | **+129.7%** | Tráfico directo creció +130% (73.3% del total) mientras atribución social UTM es 7.2%. Auditar enlaces manuales en bio/comentarios. |

### 🌐 Embudo Nativo Comunidades Tech & PTR (Dev.to + CoderLegion + LinkedIn Empresa — Coste 0 €)

| Plataforma | Estado Conector | Publicaciones (Emparejadas) | Vistas / Impresiones | Clics / CTR Nativo | Reacciones / Coment. | Sesiones GA4 (30d) | PTR % (Traspaso) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`devto`** | `ok` | 214 (106) | **8,941** | — | 123 / 32 | 1 | **0.01%** |
| **`coderlegion`** | `ok` | 2 (2) | **70** | — | 0 / 0 | 41 | **58.57%** |
| **`linkedin_company`** | `unavailable` | 0 (0) | **0** | — | 0 / 0 | 132 | **0.00%** |
| **`x`** | `standby_zero_cost` | — | *Stand-by 0 €* | — | — | 56 | *Solo GA4+UTM* |

*Nota LinkedIn Empresa:* Alcance exclusivo de **Página de Empresa** (`LINKEDIN_COMPANY_ID`) · **0 seguidores** · Cero perfiles personales ni scraping (`INV-PULSE-12`).
*Nota X / Twitter:* Atribución nativa en stand-by por política de coste 0 € (API de pago suspendida); tráfico medido exclusivamente vía GA4 Acquisition + UTMs (`Hito 7.11`).

### 🚨 Alertas de Fuga de Traspaso (`>= 300` vistas nativas con `PTR < 2.0%`)

| Activo / ID | Plataforma | Vistas Nativas | Reacciones / Coment. | Sesiones GA4 | PTR % | Acción Recomendada E06 |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| [`ia_agents_part7`](ia_agents_part7) | `devto` | **699** | 10 / 1 | 0 | **0.00%** | Fuga de traspaso en devto (699 vistas nativas, solo 0 sesiones GA4 · PTR 0.00%): insertar en el primer 25% del post sindicado un CTA interactivo al Sandbox/Calculadora en vivo (`utm_content=inline_sandbox_cta`). |
| [`ia_agents_part6`](ia_agents_part6) | `devto` | **345** | 1 / 1 | 0 | **0.00%** | Fuga de traspaso en devto (345 vistas nativas, solo 0 sesiones GA4 · PTR 0.00%): insertar en el primer 25% del post sindicado un CTA interactivo al Sandbox/Calculadora en vivo (`utm_content=inline_sandbox_cta`). |
| [`ia_agents_part9`](ia_agents_part9) | `devto` | **323** | 6 / 0 | 0 | **0.00%** | Fuga de traspaso en devto (323 vistas nativas, solo 0 sesiones GA4 · PTR 0.00%): insertar en el primer 25% del post sindicado un CTA interactivo al Sandbox/Calculadora en vivo (`utm_content=inline_sandbox_cta`). |
| [`ia_agents_part8`](ia_agents_part8) | `devto` | **313** | 11 / 0 | 0 | **0.00%** | Fuga de traspaso en devto (313 vistas nativas, solo 0 sesiones GA4 · PTR 0.00%): insertar en el primer 25% del post sindicado un CTA interactivo al Sandbox/Calculadora en vivo (`utm_content=inline_sandbox_cta`). |

### 🛡️ Escudo Anti-Canibalización Canónica (`>= 500` vistas nativas y `0` imp. GSC tras `> 21d`)

| Activo / ID | Plataforma | Vistas Nativas | Imp. GSC (30d) | Días Publicado | URL Canónica | Acción Recomendada E02 / E06 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| — | — | 0 | 0 | 0d | — | ✅ Sin alertas de canibalización canónica externa (`>= 500` vistas con `0` imp. GSC). |

---

## 9. Plan de Acción Inmediato y Relevo Editorial

1. **Relevo a `E04-bilingual-seo-editor`:** Optimizar los **12 Quick Wins prioritarios** (liderados por `kantorovich` con `3,249` imp. GSC), ajustando títulos/meta-descriptions a las queries reales detectadas.
2. **Relevo a `E05-content-monetizer`:** Resolver los **1 huérfanos de monetización** actuales e impulsar la cobertura en categorías con alta tracción orgánica y bajo ratio comercial.
3. **Relevo a `E06-social-syndicator`:** Reciclar los **0 ganadores ocultos por canal**, corregir las **4 fugas de traspaso PTR**, revisar las **0 alertas del escudo canónico** y auditar las **12 alertas de Dark Social** garantizando UTMs `ADR-033`.
4. **Relevo a `E01-editorial-orchestrator` / `E03-technical-writer`:** Atender las **15 alertas de releases silenciosas** y resolver las **1 alertas de canibalización** en el calendario de las Oleadas Semanales.
5. **Priorización en Backlog (`data/editorial/backlog.yaml`):** Lanzar `idea-claude-subagents-sdd-contracts` (ROI 88.3) y `idea-monte-carlo-capex-risk` (ROI 82.5).
