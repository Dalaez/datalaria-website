# OPPORTUNITY_BACKLOG.md — Repositorio de Oportunidades y Mejoras Proactivas Helix

> **Gobernanza:** `ADR-019` e Invariante `INV-HELIX-8`.  
> **Propósito:** Canalizar las propuestas de mejora, nuevas tendencias y optimizaciones identificadas por los agentes de Helix durante las auditorías e hitos mayores.  
> **Aislamiento de Contexto:** Este documento **NUNCA** se inyecta en el prompt de tareas rutinarias para proteger el presupuesto de tokens y la atención del modelo. Se revisa exclusivamente a petición explícita del usuario o en hitos de planificación estratégica.

---

## 1. Criterio de Priorización RICE

Cada iniciativa se evalúa con la fórmula estándar RICE:
$$\text{Score RICE} = \frac{\text{Reach (Alcance: 1-10)} \times \text{Impact (Impacto: 0.5-3)} \times \text{Confidence (Confianza: 50\%-100\%)}}{\text{Effort (Esfuerzo: personas/días o turnos: 1-5)}}$$

---

## 2. Oportunidades por Dominio y Agente Proponente

### 2.1 Célula de Construcción: UX/UI (`04-ux-ui`)
- **OPP-UX-01: Micro-interacciones con Framer Motion / Tailwind en Componentes de Entrada Financiera**
  - **Proponente:** `04-ux-ui`
  - **Descripción:** Añadir retroalimentación táctil/visual sutil en sliders y campos numéricos de inputs financieros para elevar la percepción premium del software.
  - **RICE:** Reach: 8 | Impact: 1.5 | Confidence: 90% | Effort: 2 $\rightarrow$ **Score: 5.4**
  - **Estado:** `TRIAL` para Apps interactivas de Fase 7.

### 2.2 Célula de Construcción: Frontend y Arquitectura (`03-architect` + `05-frontend`)
- **OPP-FE-01: Migración a Componentes de Tabla Virtualizados para Datasets Grandes**
  - **Proponente:** `05-frontend`
  - **Descripción:** Implementar virtualización (@tanstack/react-virtual) en el inspector de tablas de apps analíticas para manejar >10.000 filas a 60 FPS sin degradar memoria.
  - **RICE:** Reach: 6 | Impact: 2.0 | Confidence: 85% | Effort: 2 $\rightarrow$ **Score: 5.1**
  - **Estado:** `BACKLOG` (esperar a apps con datasets masivos).

- **OPP-FE-02: Motor Financiero Cliente en WebAssembly (Pyodide / Rust)**
  - **Proponente:** `03-architect`
  - **Descripción:** Compilar rutinas analíticas pesadas a Wasm para permitir que los usuarios ejecuten modelos montecarlo complejos enteramente en su navegador sin coste de cómputo para Datalaria.
  - **RICE:** Reach: 5 | Impact: 3.0 | Confidence: 70% | Effort: 4 $\rightarrow$ **Score: 2.62**
  - **Estado:** `ASSESS` (en radar tecnológico).

### 2.3 Célula de Construcción: Backend y Datos (`06-backend-data`)
- **OPP-BE-01: Plantillas Excel con Macros Seguras y Validación de Celdas Avanzada para Kits**
  - **Proponente:** `06-backend-data`
  - **Descripción:** Robustecer los generadores de `openpyxl` en `ops/` para incluir formatos condicionales nativos y protección de celdas de fórmulas, impidiendo que el comprador rompa el modelo financiero sin querer.
  - **RICE:** Reach: 9 | Impact: 2.5 | Confidence: 95% | Effort: 2 $\rightarrow$ **Score: 10.68**
  - **Estado:** `APPROVED` para Kit de Control de Gestión (Hito 7.1).

### 2.4 Célula de Monetización y Crecimiento (`09-monetization`)
- **OPP-MON-01: Bundle Dinámico con Descuento Progresivo en Lemon Squeezy**
  - **Proponente:** `09-monetization`
  - **Descripción:** Configurar en Lemon Squeezy un cupón cruzado para compradores del *Kit SDD* que adquieran posteriormente el *Kit Datalaria Pulse* o *Kit Control de Gestión*.
  - **RICE:** Reach: 8 | Impact: 2.0 | Confidence: 80% | Effort: 1 $\rightarrow$ **Score: 12.8**
  - **Estado:** `READY` para activar en lanzamiento comercial.

- **OPP-MON-02: Lead Magnet de Auditoría Rápida de Agentes para Captación B2B**
  - **Proponente:** `09-monetization`
  - **Descripción:** Publicar un script descargable gratuito de 1 archivo (`verify_agent_constitution.py`) que audita repositorios ajenos contra las reglas de `INV-HELIX-1..8`, captando leads corporativos cualificados para consultoría.
  - **RICE:** Reach: 9 | Impact: 2.5 | Confidence: 85% | Effort: 1.5 $\rightarrow$ **Score: 12.75**
  - **Estado:** `READY` para consideración en Hito 6.5.

---

## 3. Protocolo de Transición hacia el ROADMAP

Cualquier oportunidad en estado `READY` o `APPROVED` solo se transfiere a [`specs/ROADMAP.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/ROADMAP.md) cuando el usuario da su aprobación explícita o cuando se planifica formalmente un nuevo Hito.
