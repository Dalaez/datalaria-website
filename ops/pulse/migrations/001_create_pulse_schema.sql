-- ==============================================================================
-- DATALARIA PULSE — MIGRACIÓN SQL SUPABASE (CLUSTER DATALARIA-CORE)
-- Especificación: Hito 5.7 / ADR-015 (specs/apps/pulse/spec.md)
-- ==============================================================================

-- 1. Crear esquema dedicado pulse (Constitución Art. 4)
CREATE SCHEMA IF NOT EXISTS pulse;

-- 2. Tabla de Ideas y Backlog Editorial
CREATE TABLE IF NOT EXISTS pulse.ideas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    notes TEXT DEFAULT '',
    category TEXT DEFAULT 'General',
    tags TEXT[] DEFAULT '{}',
    status TEXT DEFAULT 'idea' CHECK (status IN ('idea', 'draft', 'review', 'scheduled', 'published')),
    target_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Tabla de Excepciones y Programaciones del Calendario
CREATE TABLE IF NOT EXISTS pulse.content_schedule (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    asset_id TEXT NOT NULL,
    override_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, asset_id)
);

-- 4. Habilitar Row Level Security (RLS) estricto
ALTER TABLE pulse.ideas ENABLE ROW LEVEL SECURITY;
ALTER TABLE pulse.content_schedule ENABLE ROW LEVEL SECURITY;

-- 5. Políticas de Aislamiento (Cada usuario solo ve y muta sus registros)
DROP POLICY IF EXISTS user_ideas_isolation ON pulse.ideas;
CREATE POLICY user_ideas_isolation ON pulse.ideas
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS user_schedule_isolation ON pulse.content_schedule;
CREATE POLICY user_schedule_isolation ON pulse.content_schedule
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- 6. Trigger automático para actualizar updated_at
CREATE OR REPLACE FUNCTION pulse.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_ideas_updated_at ON pulse.ideas;
CREATE TRIGGER set_ideas_updated_at
    BEFORE UPDATE ON pulse.ideas
    FOR EACH ROW EXECUTE FUNCTION pulse.handle_updated_at();

DROP TRIGGER IF EXISTS set_schedule_updated_at ON pulse.content_schedule;
CREATE TRIGGER set_schedule_updated_at
    BEFORE UPDATE ON pulse.content_schedule
    FOR EACH ROW EXECUTE FUNCTION pulse.handle_updated_at();

-- 7. Concesión de privilegios para clientes Supabase (Auth y Anon)
GRANT USAGE ON SCHEMA pulse TO authenticated, anon;
GRANT ALL ON ALL TABLES IN SCHEMA pulse TO authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA pulse TO anon;

-- 8. Exponer esquema pulse en la API PostgREST de Supabase
ALTER ROLE authenticator SET pgrst.db_schemas = 'public, lifeops, pulse';
NOTIFY pgrst, 'reload config';

-- 9. Seeding inicial de ideas sintéticas para la cuenta demo (demo@datalaria.com)
DO $$
DECLARE
    v_demo_user_id UUID;
BEGIN
    SELECT id INTO v_demo_user_id FROM auth.users WHERE email = 'demo@datalaria.com' LIMIT 1;
    
    IF v_demo_user_id IS NOT NULL THEN
        -- Insertar ideas sintéticas de prueba si no existen
        IF NOT EXISTS (SELECT 1 FROM pulse.ideas WHERE user_id = v_demo_user_id) THEN
            INSERT INTO pulse.ideas (user_id, title, notes, category, tags, status, target_date)
            VALUES
            (
                v_demo_user_id,
                'Modelado Financiero DCF: Descuento de Flujos de Caja para Startups B2B',
                'Tutorial paso a paso con plantilla Excel descargable y fórmulas dinámicas de WACC.',
                'Finanzas Corporativas',
                ARRAY['finanzas', 'dcf', 'excel', 'b2b'],
                'scheduled',
                '2026-11-20'
            ),
            (
                v_demo_user_id,
                'Arquitectura Agéntica Multimodelo: Coordinando Claude 3.7 y Gemini 2.5 Argon',
                'Benchmarking de latencia y costes en pipelines de desarrollo con SDD.',
                'Inteligencia Artificial',
                ARRAY['ia', 'agentes', 'sdd', 'deepmind'],
                'draft',
                '2026-11-25'
            ),
            (
                v_demo_user_id,
                'Guía S&OP: Del Plan de Demanda a la Capacidad de Planta con Python',
                'Fórmulas de previsión probabilística y reconciliación de inventarios.',
                'Control Operativo',
                ARRAY['sop', 'operaciones', 'python', 'sc'],
                'idea',
                NULL
            );
        END IF;
    END IF;
END $$;
