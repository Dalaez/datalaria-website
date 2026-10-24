# Incubadora de Nuevos Lanzamientos SDD (`apps/_incubadora/`)

> **Propósito:** Directorio de cuarentena y preparación para motores cuantitativos y aplicaciones B2B en fase de desarrollo o validación que **aún no han sido publicadas en la web**.

---

## Proyectos en Incubación

1. **`project-ops` (Agentic PMO Sandbox):**
   - **Motor:** FastAPI + Pandas + Pydantic v2 + EVM Engine (Earned Value Management).
   - **Estado:** Backend funcional (`port 8001`) con especificación [TECH_SPEC.md](project-ops/TECH_SPEC.md). Sus artículos de blog (`proj_ops_parte1_intro` y `proj_ops_parte2_agentic_pmo`) se encuentran en `draft: true`.
   - **Plan Fase 4 (Hito 4.1):** Construir UI interactiva (Sandbox), validar con el autor y publicar en producción.

2. **`sop-pipeline` (S&OP Autonomous Copilot):**
   - **Motor:** Python + Prophet + PuLP Linear Programming + CrewAI + Supabase.
   - **Estado:** Motor algorítmico `v2` de pronóstico de demanda y optimización de capacidad fabril. Actualmente solo referenciado mediante notebooks externos.
   - **Plan Fase 4 (Hito 4.2):** Consolidar la versión limpia `v2`, dotar de API y simulador web Sandbox, y publicar en producción.

---

## Reglas de Seguridad Invariantes (Constitución Art. 2)

- Ningún archivo de este directorio se aloja ni se procesa dentro de `static/`.
- Todo secreto y credencial vive en `.env` estrictamente ignorado por Git.
- Cero artefactos `.pyc` o entornos virtuales en el repositorio.
