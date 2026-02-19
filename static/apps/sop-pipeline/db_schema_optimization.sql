-- =====================================================
-- S&OP Pipeline - Tabla de Plan de Aprovisionamiento
-- =====================================================
-- Ejecutar este SQL en Supabase SQL Editor:
-- Dashboard → SQL Editor → New Query → Paste → Run

-- Habilitar extensión UUID (si no está activa)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla de planes de suministro
CREATE TABLE IF NOT EXISTS supply_plans (
    -- Primary Key (UUID auto-generado)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Snapshot: cuándo se ejecutó el optimizador
    execution_date DATE NOT NULL,

    -- Fecha del periodo planificado
    plan_date DATE NOT NULL,

    -- Demanda prevista (leída del forecast)
    demand_forecast NUMERIC NOT NULL,

    -- Variables de decisión del optimizador
    production_qty NUMERIC NOT NULL,    -- Cantidad a producir/comprar
    inventory_level NUMERIC NOT NULL,   -- Stock proyectado al final del periodo

    -- Objetivo de seguridad
    safety_stock_target NUMERIC NOT NULL,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraint: un solo plan por ejecución y fecha
    CONSTRAINT unique_plan_per_execution UNIQUE(execution_date, plan_date)
);

-- Índices para queries analíticas
CREATE INDEX IF NOT EXISTS idx_plan_execution
    ON supply_plans(execution_date);
CREATE INDEX IF NOT EXISTS idx_plan_date
    ON supply_plans(plan_date);

-- Habilitar Row Level Security (RLS)
ALTER TABLE supply_plans ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas las operaciones con service_role key
CREATE POLICY "Enable all for service role" ON supply_plans
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Verificar que la tabla fue creada
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'supply_plans'
ORDER BY ordinal_position;
