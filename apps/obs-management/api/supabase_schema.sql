-- Supabase Schema for Obsolescence Management (IEC 62402 Compliant)

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Core End Products
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    gross_margin NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Internal Parts (Company Specific)
CREATE TYPE part_type_enum AS ENUM ('assembly', 'component', 'raw_material');

CREATE TABLE internal_parts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    internal_pn VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    part_type part_type_enum NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Bill of Materials (Graph/Tree Structure)
CREATE TABLE bom_lines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    parent_assembly_id UUID REFERENCES internal_parts(id) ON DELETE CASCADE,
    child_pn UUID NOT NULL REFERENCES internal_parts(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    -- Aseguramos que el hijo pertenezca a un producto final O a un subensamblaje, pero no a ambos a la vez ni a ninguno.
    CONSTRAINT check_parent_exclusive CHECK (
        (parent_product_id IS NOT NULL AND parent_assembly_id IS NULL) OR 
        (parent_product_id IS NULL AND parent_assembly_id IS NOT NULL)
    )
);

-- 4. Approved Manufacturer List (The Firewall)
CREATE TYPE preference_lvl AS ENUM ('Primary', 'Secondary');

CREATE TABLE aml (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    internal_pn UUID NOT NULL REFERENCES internal_parts(id) ON DELETE CASCADE,
    manufacturer_pn VARCHAR(255) NOT NULL,
    preference_level preference_lvl NOT NULL
);

-- 5. External Telemetry (The Radar)
CREATE TYPE lifecycle_stat AS ENUM ('Active', 'EOL', 'Obsolete');

CREATE TABLE manufacturer_parts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mpn VARCHAR(255) UNIQUE NOT NULL,
    manufacturer_name VARCHAR(255) NOT NULL,
    lifecycle_status lifecycle_stat NOT NULL,
    estimated_eol_date DATE
);

-- Optimization: Indices for millisecond AI agent readings
CREATE INDEX idx_manufacturer_parts_mpn ON manufacturer_parts(mpn);
CREATE INDEX idx_aml_internal_pn ON aml(internal_pn);
CREATE INDEX idx_bom_parent_product_id ON bom_lines(parent_product_id);
CREATE INDEX idx_bom_parent_assembly_id ON bom_lines(parent_assembly_id);
CREATE INDEX idx_bom_child_pn ON bom_lines(child_pn);

-- Security: Row Level Security (RLS) policies - IP Protection
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE bom_lines ENABLE ROW LEVEL SECURITY;

-- Allow general read access to authenticated users
CREATE POLICY "Allow read access to authenticated users" 
ON products FOR SELECT TO authenticated USING (true);

CREATE POLICY "Allow read access to authenticated users" 
ON bom_lines FOR SELECT TO authenticated USING (true);

-- Restrict mutations (insert/update/delete) to Admin role only
CREATE POLICY "Restrict products mutations to admins" 
ON products FOR ALL TO authenticated 
USING ((auth.jwt() ->> 'role') = 'admin');

CREATE POLICY "Restrict bom mutations to admins" 
ON bom_lines FOR ALL TO authenticated 
USING ((auth.jwt() ->> 'role') = 'admin');
