# Agentic Radar (`obs-management`)

> **Especificación SDD Oficial:** [`specs/apps/obs-management/spec.md`](../../specs/apps/obs-management/spec.md)  
> **Ficha en Portal:** `/es/apps/obs-management/` · `/en/apps/obs-management/`  
> **App Web (Dual-Mode):** [`static/apps/obs-management/index.html`](../../static/apps/obs-management/index.html) → `https://datalaria.com/apps/obs-management/`  

---

## Estructura del Subproyecto

* `api/`: Motor analítico en Python (FastAPI + CrewAI + Supabase).
  * `main.py`: Entrada asíncrona de webhooks (Event-Driven Architecture).
  * `dashboard_api.py`: API REST para métricas ejecutivas de P&L en riesgo (`/api/v1/dashboard/risk-metrics`).
  * `obsolescence_agent.py`: Agente cognitivo CrewAI con LLM para parseo de PDN/EOL.
  * `supabase_tools.py`: Herramientas de consulta sobre grafo BOM en Supabase.
  * `supabase_schema.sql`: Esquema relacional `obs_radar` (IEC 62402).
* `../../static/apps/obs-management/index.html`: Dashboard táctico ligero (Vanilla JS + Tailwind CSS) con modo Sandbox determinista 24/7.
