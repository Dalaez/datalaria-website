-- ============================================================
-- LifeOps — Schema SQL para Supabase (datalaria-core)
-- ============================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- Proyecto: datalaria-core
-- Schema: lifeops (aislado de public)
-- ============================================================

-- 1. Crear el schema dedicado
CREATE SCHEMA IF NOT EXISTS lifeops;

-- 2. Permitir que PostgREST y el service_role accedan al schema
GRANT USAGE ON SCHEMA lifeops TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA lifeops TO postgres, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA lifeops
  GRANT ALL ON TABLES TO postgres, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA lifeops
  GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA lifeops
  GRANT SELECT ON TABLES TO anon;

-- ============================================================
-- ÁREA PERSONAL: Actividades, Deporte, Lectura, Cine, Hábitos
-- ============================================================

-- Tabla principal: actividades diarias
CREATE TABLE lifeops.activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    activity_type TEXT NOT NULL CHECK (
        activity_type IN ('sport', 'book', 'film', 'learning', 'journal')
    ),
    title TEXT NOT NULL,
    description TEXT,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    duration_minutes INTEGER,
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_activities_user_date ON lifeops.activities(user_id, date DESC);
CREATE INDEX idx_activities_type ON lifeops.activities(activity_type);

-- Entrenamientos deportivos (detalle)
CREATE TABLE lifeops.workouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_id UUID REFERENCES lifeops.activities(id) ON DELETE CASCADE NOT NULL,
    workout_type TEXT NOT NULL,  -- running, cycling, gym, swimming, hiking...
    distance_km NUMERIC(8, 2),
    calories INTEGER,
    avg_heart_rate INTEGER,
    elevation_m INTEGER,
    personal_best BOOLEAN DEFAULT false,
    notes TEXT
);

-- Libros
CREATE TABLE lifeops.books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_id UUID REFERENCES lifeops.activities(id) ON DELETE CASCADE NOT NULL,
    author TEXT NOT NULL,
    pages_total INTEGER,
    pages_read INTEGER DEFAULT 0,
    status TEXT NOT NULL CHECK (
        status IN ('reading', 'completed', 'wishlist', 'abandoned')
    ) DEFAULT 'reading',
    genre TEXT,
    isbn TEXT,
    cover_url TEXT,
    start_date DATE,
    finish_date DATE
);

-- Películas y Series
CREATE TABLE lifeops.films (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_id UUID REFERENCES lifeops.activities(id) ON DELETE CASCADE NOT NULL,
    director TEXT,
    media_type TEXT NOT NULL CHECK (
        media_type IN ('movie', 'series', 'documentary', 'anime')
    ) DEFAULT 'movie',
    genre TEXT,
    platform TEXT,        -- Netflix, HBO, Cinema, Disney+...
    year INTEGER,
    season INTEGER,
    episode INTEGER,
    imdb_url TEXT
);

-- Hábitos
CREATE TABLE lifeops.habits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT DEFAULT '✅',
    color TEXT DEFAULT '#4CAF50',
    target_frequency TEXT NOT NULL CHECK (
        target_frequency IN ('daily', 'weekly', 'monthly')
    ) DEFAULT 'daily',
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lifeops.habit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    habit_id UUID REFERENCES lifeops.habits(id) ON DELETE CASCADE NOT NULL,
    logged_date DATE NOT NULL DEFAULT CURRENT_DATE,
    notes TEXT,
    UNIQUE(habit_id, logged_date)
);

-- ============================================================
-- ÁREA PROFESIONAL: Proyectos y Tareas
-- ============================================================

-- Proyectos
CREATE TABLE lifeops.projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL CHECK (
        status IN ('planning', 'active', 'on_hold', 'completed', 'cancelled')
    ) DEFAULT 'planning',
    priority TEXT CHECK (
        priority IN ('low', 'medium', 'high', 'critical')
    ) DEFAULT 'medium',
    start_date DATE,
    target_end_date DATE,
    actual_end_date DATE,
    budget NUMERIC(12, 2),
    spent NUMERIC(12, 2) DEFAULT 0,
    tags TEXT[] DEFAULT '{}',
    color TEXT DEFAULT '#2196F3',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Tareas
CREATE TABLE lifeops.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    project_id UUID REFERENCES lifeops.projects(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL CHECK (
        status IN ('backlog', 'todo', 'in_progress', 'review', 'done', 'cancelled')
    ) DEFAULT 'todo',
    priority TEXT CHECK (
        priority IN ('low', 'medium', 'high', 'critical')
    ) DEFAULT 'medium',
    due_date DATE,
    completed_at TIMESTAMPTZ,
    estimated_hours NUMERIC(6, 2),
    actual_hours NUMERIC(6, 2),
    tags TEXT[] DEFAULT '{}',
    comments JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_tasks_user_status ON lifeops.tasks(user_id, status);
CREATE INDEX idx_tasks_project ON lifeops.tasks(project_id);
CREATE INDEX idx_tasks_due_date ON lifeops.tasks(due_date);

-- ============================================================
-- MÓDULOS TRANSVERSALES: Informes y Alertas
-- ============================================================

-- Plantillas de informes
CREATE TABLE lifeops.report_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name TEXT NOT NULL,
    template_type TEXT NOT NULL,    -- 'weekly_sport', 'monthly_summary', 'project_status'
    description TEXT,
    config JSONB DEFAULT '{}',     -- Parámetros del informe (periodo, módulos a incluir, etc.)
    is_scheduled BOOLEAN DEFAULT false,
    schedule_cron TEXT,            -- '0 8 * * 1' = cada lunes a las 8am
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lifeops.generated_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    template_id UUID REFERENCES lifeops.report_templates(id) ON DELETE SET NULL,
    report_name TEXT NOT NULL,
    file_path TEXT,               -- Ruta en Supabase Storage
    period_start DATE,
    period_end DATE,
    metadata JSONB DEFAULT '{}',  -- Snapshot de KPIs calculados
    generated_at TIMESTAMPTZ DEFAULT now()
);

-- Reglas de alerta
CREATE TABLE lifeops.alert_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name TEXT NOT NULL,
    condition_type TEXT NOT NULL,    -- 'deadline_approaching', 'threshold_exceeded', 'streak_risk', 'inactivity'
    entity_type TEXT NOT NULL,       -- 'task', 'project', 'workout', 'book', 'habit'
    threshold_value NUMERIC,
    threshold_unit TEXT,             -- 'days', 'percent', 'count'
    notification_channel TEXT DEFAULT 'email',
    is_active BOOLEAN DEFAULT true,
    cooldown_hours INTEGER DEFAULT 24,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lifeops.alert_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id UUID REFERENCES lifeops.alert_rules(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    triggered_at TIMESTAMPTZ DEFAULT now(),
    alert_data JSONB NOT NULL,      -- Contexto: entidad, valor actual, umbral
    delivery_status TEXT DEFAULT 'pending' CHECK (
        delivery_status IN ('pending', 'sent', 'failed', 'acknowledged')
    ),
    email_sent_at TIMESTAMPTZ,
    acknowledged_at TIMESTAMPTZ
);

-- ============================================================
-- ROW LEVEL SECURITY (RLS) — Solo el propietario accede a sus datos
-- ============================================================

-- Activar RLS en todas las tablas
ALTER TABLE lifeops.activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.workouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.books ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.films ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.habits ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.habit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.report_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.generated_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.alert_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifeops.alert_log ENABLE ROW LEVEL SECURITY;

-- Políticas: cada usuario solo ve/modifica sus propios datos
CREATE POLICY "Own data only" ON lifeops.activities
    FOR ALL TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "Own data only" ON lifeops.habits
    FOR ALL TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "Own data only" ON lifeops.projects
    FOR ALL TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "Own data only" ON lifeops.tasks
    FOR ALL TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "Own data only" ON lifeops.report_templates
    FOR ALL TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "Own data only" ON lifeops.generated_reports
    FOR ALL TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "Own data only" ON lifeops.alert_rules
    FOR ALL TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "Own data only" ON lifeops.alert_log
    FOR ALL TO authenticated USING (auth.uid() = user_id);

-- Para tablas hijas (workouts, books, films, habit_logs):
-- acceso a través de la actividad/hábito padre
CREATE POLICY "Access via parent activity" ON lifeops.workouts
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM lifeops.activities a
            WHERE a.id = activity_id AND a.user_id = auth.uid()
        )
    );

CREATE POLICY "Access via parent activity" ON lifeops.books
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM lifeops.activities a
            WHERE a.id = activity_id AND a.user_id = auth.uid()
        )
    );

CREATE POLICY "Access via parent activity" ON lifeops.films
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM lifeops.activities a
            WHERE a.id = activity_id AND a.user_id = auth.uid()
        )
    );

CREATE POLICY "Access via parent habit" ON lifeops.habit_logs
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM lifeops.habits h
            WHERE h.id = habit_id AND h.user_id = auth.uid()
        )
    );

-- ============================================================
-- FUNCIÓN: auto-actualizar updated_at
-- ============================================================
CREATE OR REPLACE FUNCTION lifeops.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at_activities
    BEFORE UPDATE ON lifeops.activities
    FOR EACH ROW EXECUTE FUNCTION lifeops.update_updated_at();

CREATE TRIGGER set_updated_at_projects
    BEFORE UPDATE ON lifeops.projects
    FOR EACH ROW EXECUTE FUNCTION lifeops.update_updated_at();

CREATE TRIGGER set_updated_at_tasks
    BEFORE UPDATE ON lifeops.tasks
    FOR EACH ROW EXECUTE FUNCTION lifeops.update_updated_at();
