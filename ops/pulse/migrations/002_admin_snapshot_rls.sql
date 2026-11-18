-- ==============================================================================
-- DATALARIA PULSE — TABLA PRIVADA DE SNAPSHOT MAESTRO ADMIN CON RLS ESTRICTO
-- Especificación: SPEC-APP-PULSE (INV-PULSE-9) · Hito P-LAUNCH-5A-SEC
-- ==============================================================================

-- 1. Asegurar existencia del esquema dedicado pulse (Constitución Art. 4)
CREATE SCHEMA IF NOT EXISTS pulse;

-- 2. Tabla de Snapshot Maestro Privado (incluye borradores y proyectos embargados)
CREATE TABLE IF NOT EXISTS pulse.private_snapshot (
    id TEXT PRIMARY KEY DEFAULT 'master',
    payload JSONB NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Habilitar Row Level Security (RLS) estricto — CERO exposición a anon/demo/clientes
ALTER TABLE pulse.private_snapshot ENABLE ROW LEVEL SECURITY;

-- 4. Política exclusiva de lectura para cuentas Administrador autenticadas por JWT
DROP POLICY IF EXISTS admin_snapshot_select ON pulse.private_snapshot;
CREATE POLICY admin_snapshot_select ON pulse.private_snapshot
    FOR SELECT
    TO authenticated
    USING (
        (auth.jwt() ->> 'email') IN ('dalaez1@gmail.com', 'datalaria@gmail.com')
    );

-- 5. Privilegios estrictos (solo SELECT a authenticated; escritura completa reservada a service_role)
REVOKE ALL ON pulse.private_snapshot FROM PUBLIC;
REVOKE ALL ON pulse.private_snapshot FROM anon;
GRANT USAGE ON SCHEMA pulse TO authenticated, service_role;
GRANT SELECT ON pulse.private_snapshot TO authenticated;
GRANT ALL ON pulse.private_snapshot TO service_role;

-- 6. Recargar configuración de esquema en PostgREST
NOTIFY pgrst, 'reload config';
