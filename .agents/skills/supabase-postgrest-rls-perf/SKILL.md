---
name: supabase-postgrest-rls-perf
description: Multi-schema Supabase PostgreSQL RLS isolation, local ECC P-256 JWKS verification, PostgREST embedded joins, server-side pagination, and SWR client resilience patterns for Datalaria Dual-Mode apps (LifeOps, Pulse). Trigger for 03-architect, 06-backend-data, 07-apis-integrations, and 10-security-privacy.
---

# Datalaria Supabase Multi-Schema RLS, PostgREST & Dual-Mode Performance Skill

Use this progressive skill whenever designing, implementing, or auditing cloud persistence, authentication, or API endpoints in Datalaria's shared Supabase instance (`datalaria-core`) or Dual-Mode (`Demo / Personal Cloud`) apps (`lifeops`, `pulse`, or Blueprint 02 apps).

## 1. Multi-Schema Isolation & Strict RLS (`03-architect`, `06-backend-data`, `10-security-privacy`)
- **Dedicated Schema per App (`specs/_constitution.md` Art. 3):**
  - Every application in `datalaria-core` lives in its own PostgreSQL schema (`lifeops.*`, `pulse.*`) — never create app tables in `public.*`.
  - Grant explicit schema permissions (`GRANT USAGE ON SCHEMA <app> TO anon, authenticated, service_role;`) and expose the schema in Supabase API settings.
- **Row-Level Security (`RLS`) & Seeder Safety (`INV-PULSE-10`):**
  - Enable RLS on 100% of tables (`ALTER TABLE <app>.<table> ENABLE ROW LEVEL SECURITY;`).
  - Bind personal records to `auth.uid() = user_id` and guard demo/seed scripts behind an explicit environment check (`seeder_guard`) with **zero hardcoded demo passwords** in repository code.

## 2. Sub-Millisecond JWT Verification & PostgREST Query Optimization (`06-backend-data`, `07-apis-integrations`)
- **Local JWKS Verification (`0.1 ms` vs `350 ms`):**
  - Verify Supabase `ECC (P-256)` / `ES256` and `HS256` JWTs locally using `PyJWKClient` caching `<SUPABASE_URL>/auth/v1/.well-known/jwks.json` (1h TTL) instead of making a blocking HTTP round-trip to `supabase.auth.get_user(token)` on every API call.
- **Eliminate N+1 & Multi-Trip `.in_()` Queries:**
  - Use PostgREST embedded resource joins in a single HTTP request (e.g., `.select("*, task_comments(*)")`) and map nested relations in memory.
- **Server-Side Pagination & Decoupled KPI Summary:**
  - Support `limit`/`offset` (`12 / 24 / 48` items per page) with `count="exact"` and `X-Total-Count` response header.
  - Compute global dashboard KPIs via a lightweight SQL RPC or projection query (`/summary`) decoupled from the paginated table payload.

## 3. Client-Side SWR Hydration & Cold-Start Resilience (`05-frontend`, `07-apis-integrations`)
- **Instant `0 ms` SWR Hydration:**
  - Scope `localStorage` cache keys by mode and user ID (`<app>_swr_cache_v1_${mode}_${userId}`). Hydrate the UI immediately on mount while revalidating in the background.
- **Render Cold-Start Backoff & `401` Session Recovery:**
  - Wrap API calls in a resilient client with `75s` timeout (3 attempts, exponential backoff for Render Free Tier spin-up).
  - On `HTTP 401`, invoke `supabase.auth.refreshSession()` once and retry transparently before falling back or logging out.
