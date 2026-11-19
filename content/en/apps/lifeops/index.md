---
title: "LifeOps"
description: "All-in-one personal & professional OS: paginated sport tracking, book library, movies, Kanban tasks & 360° analytics."
app: "lifeops"
translationKey: "app-lifeops"
layout: "single"
---

## 🚀 What's New in LifeOps v1.2.0 — Sport Pagination & Mobile Resilience

**LifeOps v1.2.0** optimizes end-to-end mobile reliability and query scalability across growing activity histories on Supabase and Render free tier:

- **Server-Side `12 / 24 / 48` Pagination & RPC Summary (`lifeops.sport_summary`):** The Fitness Module fetches only the active page (`O(12)`) while preserving full historical KPIs (total distance, calories, total sessions, and personal bests) via `include_summary` and a PostgreSQL aggregate RPC.
- **PostgREST Embedded Joins & Compound Indexes:** Eliminates linear `.in_()` queries with single-roundtrip `select('*, workouts(*)')` joins, backed by compound indexes (`user_id, category, date DESC, created_at DESC, id DESC`), `GZip` compression, and `Server-Timing` observability.
- **Local JWT `ECC (P-256) / ES256` Verification via JWKS:** In-memory signature validation through a cached `PyJWKClient` (`0 ms` network roundtrips to Supabase Auth) with immediate `O(1)` rejection of forged or expired tokens.
- **Mobile Resilience & `0 ms` SWR Cache:** Silent session auto-refresh on HTTP `401`, exponential backoff retries with a `75 s` window to absorb Render cold starts, background-paused alert polling (`document.hidden`), touch-friendly mobile cards (`≥ 44 px`), and ≥ 60 deterministic workouts in Sandbox Demo mode.
