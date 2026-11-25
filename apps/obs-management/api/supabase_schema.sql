-- Supabase Multi-Schema DDL for Agentic Radar (Constitución Art. 4 & INV-OBS-5)
-- Esquema aislado: obs_radar (IEC 62402) con RLS multi-tenant en todas las tablas.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS obs_radar;

-- Enumeraciones en el namespace dedicado obs_radar
DO $$ BEGIN
    CREATE TYPE obs_radar.part_type_enum AS ENUM ('assembly', 'component', 'raw_material');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE obs_radar.preference_lvl AS ENUM ('Primary', 'Secondary');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE obs_radar.lifecycle_stat AS ENUM ('Active', 'NRND', 'EOL', 'Obsolete');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE obs_radar.alert_severity AS ENUM ('CRITICAL LTB REQUIRED', 'EVALUATING INVENTORY', 'MONITORED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- 1. Core End Products (Margen Bruto en EUR absolutos NUMERIC(12, 2))
CREATE TABLE IF NOT EXISTS obs_radar.products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL DEFAULT auth.uid(),
    sku VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    gross_margin NUMERIC(12, 2) NOT NULL CHECK (gross_margin >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (user_id, sku)
);

-- 2. Internal Parts (Company Specific)
CREATE TABLE IF NOT EXISTS obs_radar.internal_parts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL DEFAULT auth.uid(),
    internal_pn VARCHAR(255) NOT NULL,
    description TEXT,
    part_type obs_radar.part_type_enum NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (user_id, internal_pn)
);

-- 3. Bill of Materials (Graph/Tree Structure)
CREATE TABLE IF NOT EXISTS obs_radar.bom_lines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL DEFAULT auth.uid(),
    parent_product_id UUID REFERENCES obs_radar.products(id) ON DELETE CASCADE,
    parent_assembly_id UUID REFERENCES obs_radar.internal_parts(id) ON DELETE CASCADE,
    child_pn UUID NOT NULL REFERENCES obs_radar.internal_parts(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    CONSTRAINT check_parent_exclusive CHECK (
        (parent_product_id IS NOT NULL AND parent_assembly_id IS NULL) OR
        (parent_product_id IS NULL AND parent_assembly_id IS NOT NULL)
    )
);

-- 4. Approved Manufacturer List (The Firewall)
CREATE TABLE IF NOT EXISTS obs_radar.aml (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL DEFAULT auth.uid(),
    internal_pn UUID NOT NULL REFERENCES obs_radar.internal_parts(id) ON DELETE CASCADE,
    manufacturer_pn VARCHAR(255) NOT NULL,
    preference_level obs_radar.preference_lvl NOT NULL DEFAULT 'Primary',
    UNIQUE (user_id, internal_pn, manufacturer_pn)
);

-- 5. External Telemetry (The Radar)
CREATE TABLE IF NOT EXISTS obs_radar.manufacturer_parts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL DEFAULT auth.uid(),
    mpn VARCHAR(255) NOT NULL,
    manufacturer_name VARCHAR(255) NOT NULL,
    lifecycle_status obs_radar.lifecycle_stat NOT NULL,
    unit_price_eur NUMERIC(12, 4) DEFAULT 5.00 CHECK (unit_price_eur >= 0),
    monthly_demand INTEGER DEFAULT 300 CHECK (monthly_demand >= 0),
    estimated_eol_date DATE,
    UNIQUE (user_id, mpn)
);

-- 6. Persisted EOL Alerts & Agent Assessments
CREATE TABLE IF NOT EXISTS obs_radar.eol_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL DEFAULT auth.uid(),
    mpn VARCHAR(255) NOT NULL,
    source_channel VARCHAR(64) NOT NULL,
    criticality_score INTEGER NOT NULL CHECK (criticality_score >= 0 AND criticality_score <= 100),
    severity obs_radar.alert_severity NOT NULL,
    total_risk_eur NUMERIC(12, 2) NOT NULL CHECK (total_risk_eur >= 0),
    executive_summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indices FK & Consultas de Grafo
CREATE INDEX IF NOT EXISTS idx_obs_products_user_sku ON obs_radar.products(user_id, sku);
CREATE INDEX IF NOT EXISTS idx_obs_internal_parts_user_pn ON obs_radar.internal_parts(user_id, internal_pn);
CREATE INDEX IF NOT EXISTS idx_obs_bom_user ON obs_radar.bom_lines(user_id);
CREATE INDEX IF NOT EXISTS idx_obs_bom_parent_product_id ON obs_radar.bom_lines(parent_product_id);
CREATE INDEX IF NOT EXISTS idx_obs_bom_parent_assembly_id ON obs_radar.bom_lines(parent_assembly_id);
CREATE INDEX IF NOT EXISTS idx_obs_bom_child_pn ON obs_radar.bom_lines(child_pn);
CREATE INDEX IF NOT EXISTS idx_obs_aml_internal_pn ON obs_radar.aml(internal_pn);
CREATE INDEX IF NOT EXISTS idx_obs_aml_mpn ON obs_radar.aml(user_id, manufacturer_pn);
CREATE INDEX IF NOT EXISTS idx_obs_mfg_parts_mpn ON obs_radar.manufacturer_parts(user_id, mpn);
CREATE INDEX IF NOT EXISTS idx_obs_eol_alerts_user_created ON obs_radar.eol_alerts(user_id, created_at DESC);

-- Seguridad: Row Level Security (RLS) estricto auth.uid() = user_id en las 6 tablas
ALTER TABLE obs_radar.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.internal_parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.bom_lines ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.aml ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.manufacturer_parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE obs_radar.eol_alerts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "tenant_isolation_products" ON obs_radar.products;
CREATE POLICY "tenant_isolation_products" ON obs_radar.products
    FOR ALL TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "tenant_isolation_internal_parts" ON obs_radar.internal_parts;
CREATE POLICY "tenant_isolation_internal_parts" ON obs_radar.internal_parts
    FOR ALL TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "tenant_isolation_bom_lines" ON obs_radar.bom_lines;
CREATE POLICY "tenant_isolation_bom_lines" ON obs_radar.bom_lines
    FOR ALL TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "tenant_isolation_aml" ON obs_radar.aml;
CREATE POLICY "tenant_isolation_aml" ON obs_radar.aml
    FOR ALL TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "tenant_isolation_manufacturer_parts" ON obs_radar.manufacturer_parts;
CREATE POLICY "tenant_isolation_manufacturer_parts" ON obs_radar.manufacturer_parts
    FOR ALL TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "tenant_isolation_eol_alerts" ON obs_radar.eol_alerts;
CREATE POLICY "tenant_isolation_eol_alerts" ON obs_radar.eol_alerts
    FOR ALL TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
