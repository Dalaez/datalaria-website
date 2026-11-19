-- ============================================================
-- LifeOps v1.2.0 — Performance Indexes & Sport Summary RPC
-- ============================================================
-- ADR-030 / Hito 1.9 (Idempotent migration — safe to re-run)
-- Ejecutar en: Supabase Dashboard > SQL Editor (datalaria-core)
-- Schema: lifeops
-- ============================================================

-- 1. Índices en claves foráneas (PostgreSQL no indexa FKs automáticamente)
--    Aceleran los joins embebidos PostgREST: select("*, workouts(*)")
CREATE INDEX IF NOT EXISTS idx_workouts_activity_id
    ON lifeops.workouts(activity_id);

CREATE INDEX IF NOT EXISTS idx_books_activity_id
    ON lifeops.books(activity_id);

CREATE INDEX IF NOT EXISTS idx_films_activity_id
    ON lifeops.films(activity_id);

-- 2. Índice compuesto de orden total determinista para paginación (INV-12)
--    Soporta WHERE user_id = ? AND activity_type = ?
--    ORDER BY date DESC, created_at DESC, id DESC
CREATE INDEX IF NOT EXISTS idx_activities_user_type_date_order
    ON lifeops.activities(user_id, activity_type, date DESC, created_at DESC, id DESC);

-- 3. Función RPC agregadora determinista de KPIs deportivos (< 5 ms en Postgres, INV-14)
--    SECURITY INVOKER garantiza que RLS se aplica siempre si se invoca como authenticated.
CREATE OR REPLACE FUNCTION lifeops.sport_summary(p_user_id UUID)
RETURNS TABLE (
    count BIGINT,
    total_km NUMERIC,
    total_seconds BIGINT,
    total_kcal BIGINT,
    pb_count BIGINT
)
LANGUAGE sql
STABLE
SECURITY INVOKER
AS $$
    SELECT
        COUNT(a.id)::BIGINT AS count,
        COALESCE(ROUND(SUM(COALESCE(w.distance_km, 0))::NUMERIC, 2), 0)::NUMERIC AS total_km,
        COALESCE(
            SUM(
                CASE
                    WHEN (a.metadata->>'duration_seconds') ~ '^\d+$'
                        THEN (a.metadata->>'duration_seconds')::BIGINT
                    WHEN a.duration_minutes IS NOT NULL
                        THEN (a.duration_minutes::BIGINT * 60)
                    ELSE 0
                END
            ),
            0
        )::BIGINT AS total_seconds,
        COALESCE(SUM(COALESCE(w.calories, 0)), 0)::BIGINT AS total_kcal,
        COUNT(*) FILTER (WHERE COALESCE(w.personal_best, false) = true)::BIGINT AS pb_count
    FROM lifeops.activities a
    LEFT JOIN lifeops.workouts w ON w.activity_id = a.id
    WHERE a.user_id = p_user_id
      AND a.activity_type = 'sport';
$$;

GRANT EXECUTE ON FUNCTION lifeops.sport_summary(UUID) TO service_role, authenticated;
