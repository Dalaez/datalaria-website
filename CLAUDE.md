# CLAUDE.md — Puntero de Gobernanza para Agentes Claude (Datalaria SDD + Helix Squad)

Este repositorio se rige por una arquitectura estricta de **Spec-Driven Development (SDD)** y el **Escuadrón de 12 Agentes Datalaria Helix**, 100% agnósticos del modelo.

## Instrucción Crítica e Inmediata

Antes de analizar código, planificar o ejecutar cualquier herramienta de escritura, **ejecuta en orden la secuencia de arranque**:

1. **[`AGENTS.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/AGENTS.md)** — Protocolo de arranque en 3 pasos, mapa topológico, bucle de ejecución/rollback SDD y **Sección 5 (Escuadrón Datalaria Helix y Triaje Bajo Demanda)**.
2. **[`specs/_constitution.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/_constitution.md)** (`v1.1.0`) — Los **9 artículos arquitectónicos inmutables** de Datalaria (incluyendo el Art. 9 de separación Construcción/Verificación, derecho a veto de QA/Seguridad y disparadores automáticos `INV-HELIX-1..7`).
3. **[`specs/ROADMAP.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/ROADMAP.md)** — Estado actual del proyecto, hito activo y registro de checkpoints.
4. **Subagentes Nativos (`.claude/agents/` y [`specs/squad/`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/README.md)):** Los 12 subagentes en `.claude/agents/*.md` se compilan automáticamente desde `specs/squad/*.md` mediante `python -m ops.helix.build_adapters`. Aplica siempre la rúbrica de [`specs/squad/triage-rubric.md`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad/triage-rubric.md) e invoca únicamente los roles requeridos por la talla de la tarea (`XS` a `XL`).

> **Regla de Oro (`INV-HELIX-4`):** No dupliques reglas en este archivo ni edites manualmente `.claude/agents/*.md`. Toda evolución del protocolo se mantiene centralizada en `AGENTS.md` y `/specs/squad/`.
