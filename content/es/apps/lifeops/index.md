---
title: "LifeOps"
description: "Sistema operativo integral personal y profesional: deporte paginado, lecturas, cine, tablero Kanban y analítica 360°."
app: "lifeops"
translationKey: "app-lifeops"
layout: "single"
---

## 🚀 Novedades de LifeOps v1.2.0 — Paginación Deportiva y Resiliencia Móvil

**LifeOps v1.2.0** optimiza de extremo a extremo la experiencia en dispositivos móviles y el escalado de históricos crecientes en Supabase y Render Free:

- **Paginación Server-Side `12 / 24 / 48` y Resumen RPC (`lifeops.sport_summary`):** El Módulo Deportivo carga únicamente la página activa (`O(12)`) manteniendo los KPIs históricos completos (kilómetros acumulados, calorías, sesiones totales y marcas personales) mediante el parámetro `include_summary` y una función agregada en PostgreSQL.
- **Joins Embebidos PostgREST e Índices Compuestos:** Eliminación de consultas `.in_()` lineales mediante `select('*, workouts(*)')` en una sola ida a base de datos, respaldado por índices compuestos (`user_id, category, date DESC, created_at DESC, id DESC`), compresión `GZip` y cabecera `Server-Timing`.
- **Verificación Criptográfica Local JWT `ECC (P-256) / ES256` vía JWKS:** Validación en memoria con `PyJWKClient` cacheado (`0 ms` de latencia de red hacia Supabase Auth) y rechazo inmediato en `O(1)` de tokens inválidos o manipulados.
- **Resiliencia Móvil y Caché SWR `0 ms`:** Auto-refresh silencioso de sesión ante HTTP `401`, reintentos automáticos con *backoff* exponencial y ventana de `75 s` para absorber *Cold-Starts* en Render, pausa inteligente del polling de alertas en segundo plano (`document.hidden`), vista adaptada en tarjetas táctiles (`≥ 44 px`) y ≥ 60 entrenamientos sintéticos en el Modo Demo.
