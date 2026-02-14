-- =====================================================
-- S&OP Pipeline - Tabla de Predicciones de Demanda
-- =====================================================
-- Ejecutar este SQL en Supabase SQL Editor:
-- Dashboard → SQL Editor → New Query → Paste → Run

-- Habilitar extensión UUID (si no está activa)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla de forecasts
CREATE TABLE IF NOT EXISTS demand_forecasts (
    -- Primary Key (UUID auto-generado)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Snapshot: cuándo se ejecutó el modelo
    execution_date DATE NOT NULL,

    -- Fecha futura predicha
    ds DATE NOT NULL,

    -- Predicción central (unidades de demanda)
    yhat NUMERIC NOT NULL,

    -- Intervalo de confianza (95%)
    yhat_lower NUMERIC NOT NULL,  -- Safety Stock baseline
    yhat_upper NUMERIC NOT NULL,  -- Worst-case para gestión de riesgos

    -- Trazabilidad del modelo
    model_version TEXT NOT NULL DEFAULT 'prophet-v1.0',

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraint: una sola predicción por fecha y ejecución
    CONSTRAINT unique_forecast_per_execution UNIQUE(execution_date, ds)
);

-- Índices para queries analíticas frecuentes
CREATE INDEX IF NOT EXISTS idx_forecast_execution
    ON demand_forecasts(execution_date);
CREATE INDEX IF NOT EXISTS idx_forecast_ds
    ON demand_forecasts(ds);
CREATE INDEX IF NOT EXISTS idx_forecast_model
    ON demand_forecasts(model_version);

-- Habilitar Row Level Security (RLS)
ALTER TABLE demand_forecasts ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas las operaciones con service_role key
CREATE POLICY "Enable all for service role" ON demand_forecasts
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Verificar que la tabla fue creada
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'demand_forecasts'
ORDER BY ordinal_position;
