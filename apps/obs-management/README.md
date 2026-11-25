# Agentic Radar (`obs-management` v2.0.0)

> **Especificación SDD Oficial:** [`specs/apps/obs-management/spec.md`](../../specs/apps/obs-management/spec.md) (`v2.0.0`)  
> **Contrato Visual UX/UI:** [`specs/apps/obs-management/design.md`](../../specs/apps/obs-management/design.md)  
> **Ficha en Portal:** `/es/apps/obs-management/` · `/en/apps/obs-management/`  
> **App Web (Dual-Mode Zero-CDN):** [`static/apps/obs-management/`](../../static/apps/obs-management/) → `https://datalaria.com/apps/obs-management/`

---

## Estructura Unificada del Subproyecto

* `web/`: Fuente canónica del **Executive Risk Cockpit v2.0** Zero-CDN (`index.html`, `styles.css`, `i18n.js`, `engine.js`, `app.js`, `sync_static.py`).
* `api/`: Backend unificado en Python (**FastAPI + Pydantic v2 + `bom_engine.py` + CrewAI + Supabase `obs_radar`**):
  * `main.py`: Servidor FastAPI unificado (`/health`, `GET /api/v1/dashboard/risk-metrics`, `POST /api/v1/ltb/evaluate`, `POST /api/v1/webhooks/*`) con CORS por entorno y autenticación HMAC/Bearer.
  * `bom_engine.py`: **El Músculo** determinista puro (recorrido DAG multinivel sin ciclos, criticidad IEC 62402, decisión LTB vs. Rediseño FFF).
  * `models.py`: Contratos tipados Pydantic v2.
  * `obsolescence_agent.py`: **El Cerebro** CrewAI con delimitación anti-Prompt-Injection para extraer MPNs.
  * `supabase_tools.py`: Carga plana sin N+1 sobre el esquema aislado `obs_radar`.
  * `supabase_schema.sql`: Esquema relacional `obs_radar` con `user_id` y RLS estricto en las 6 tablas.
  * `seeder_guard.py`, `data_loader.py`, `generate_dummy_bom.py`: Pipeline ETL seguro con whitelist demo (`ADR-014`).
* `tests/`: Suites deterministas `test_frontend_contract.py`, `test_backend_engine.py` y `e2e_edge_check.cjs`.

## Ejecución Local y Pruebas

```powershell
python -m pytest apps/obs-management/tests -v
uvicorn apps.obs-management.api.main:app --port 8001
```
