-- =====================================================
-- S&OP Pipeline v2 - Schema Multi-SKU
-- =====================================================
-- IMPORTANTE: Este script hace DROP de las tablas existentes.
-- Ejecutar solo en entorno de desarrollo.
-- Dashboard → SQL Editor → New Query → Paste → Run

-- Habilitar extensión UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ─────────────────────────────────────────────────────
-- TABLA 1: sales_transactions (Multi-SKU)
-- ─────────────────────────────────────────────────────
DROP TABLE IF EXISTS sales_transactions CASCADE;

CREATE TABLE sales_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    sku TEXT NOT NULL,
    qty NUMERIC NOT NULL,
    is_outlier BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_transaction UNIQUE(date, sku)
);

-- Trigger para auto-update de updated_at
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON sales_transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- Índices
CREATE INDEX idx_sales_date ON sales_transactions(date);
CREATE INDEX idx_sales_sku ON sales_transactions(sku);
CREATE INDEX idx_sales_sku_date ON sales_transactions(sku, date);

-- RLS
ALTER TABLE sales_transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable all for service role" ON sales_transactions
    FOR ALL USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────────────────
-- TABLA 2: demand_forecasts (Multi-SKU)
-- ─────────────────────────────────────────────────────
DROP TABLE IF EXISTS demand_forecasts CASCADE;

CREATE TABLE demand_forecasts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_date DATE NOT NULL,
    sku TEXT NOT NULL,
    ds DATE NOT NULL,
    yhat NUMERIC NOT NULL,
    yhat_lower NUMERIC NOT NULL,
    yhat_upper NUMERIC NOT NULL,
    model_version TEXT NOT NULL DEFAULT 'prophet-v1.0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_forecast_per_sku UNIQUE(execution_date, sku, ds)
);

CREATE INDEX idx_forecast_execution ON demand_forecasts(execution_date);
CREATE INDEX idx_forecast_sku ON demand_forecasts(sku);
CREATE INDEX idx_forecast_ds ON demand_forecasts(ds);

ALTER TABLE demand_forecasts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable all for service role" ON demand_forecasts
    FOR ALL USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────────────────
-- TABLA 3: supply_plans (Multi-SKU)
-- ─────────────────────────────────────────────────────
DROP TABLE IF EXISTS supply_plans CASCADE;

CREATE TABLE supply_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_date DATE NOT NULL,
    sku TEXT NOT NULL,
    plan_date DATE NOT NULL,
    demand_forecast NUMERIC NOT NULL,
    production_qty NUMERIC NOT NULL,
    inventory_level NUMERIC NOT NULL,
    safety_stock_target NUMERIC NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_plan_per_sku UNIQUE(execution_date, sku, plan_date)
);

CREATE INDEX idx_plan_execution ON supply_plans(execution_date);
CREATE INDEX idx_plan_sku ON supply_plans(sku);
CREATE INDEX idx_plan_date ON supply_plans(plan_date);

ALTER TABLE supply_plans ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable all for service role" ON supply_plans
    FOR ALL USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────────────────
-- Verificación
-- ─────────────────────────────────────────────────────
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('sales_transactions', 'demand_forecasts', 'supply_plans')
ORDER BY table_name, ordinal_position;
