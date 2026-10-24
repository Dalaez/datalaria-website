-- =====================================================
-- S&OP Pipeline - Tabla de Transacciones de Ventas
-- =====================================================
-- Ejecutar este SQL en Supabase SQL Editor:
-- Dashboard → SQL Editor → New Query → Paste → Run

-- Crear tabla principal
CREATE TABLE IF NOT EXISTS sales_transactions (
    -- Primary Key (para upserts)
    transaction_id VARCHAR(20) PRIMARY KEY,
    
    -- Campos de negocio
    date DATE NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    product_name VARCHAR(100),
    qty NUMERIC NOT NULL,
    unit_price NUMERIC(10, 2),
    region VARCHAR(50),
    
    -- Flag de outlier (detectado por Z-Score)
    is_outlier BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para queries comunes en S&OP
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales_transactions(date);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales_transactions(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_region ON sales_transactions(region);

-- Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_timestamp ON sales_transactions;
CREATE TRIGGER set_timestamp
    BEFORE UPDATE ON sales_transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- Habilitar Row Level Security (RLS) - Buena práctica
ALTER TABLE sales_transactions ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas las operaciones con service_role key
CREATE POLICY "Enable all for service role" ON sales_transactions
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Verificar que la tabla fue creada
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_name = 'sales_transactions'
ORDER BY ordinal_position;
