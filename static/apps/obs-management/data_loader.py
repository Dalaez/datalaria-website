import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan credenciales de Supabase en .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    print(f"Cargando export heredado desde: {filepath}")
    df = pd.read_csv(filepath)
    
    # 1. Limpieza de Entropía: Espacios traicioneros en strings
    df['Manufacturer_PN'] = df['Manufacturer_PN'].str.strip()
    df['Assembly_PN'] = df['Assembly_PN'].str.strip()
    df['Component_PN'] = df['Component_PN'].str.strip()
    df['End_Product_SKU'] = df['End_Product_SKU'].str.strip()
    
    # 2. Limpieza de Entropía: Consolidación de nombres de fabricantes
    # Convertimos a Title Case y unificamos los alias conocidos
    df['Manufacturer'] = df['Manufacturer'].str.title().str.strip()
    mfg_mapping = {
        'Ti': 'Texas Instruments',
        'Texas Inst.': 'Texas Instruments',
        'Stmicroelectronics': 'STMicroelectronics',
        'St Micro': 'STMicroelectronics',
        'Stm': 'STMicroelectronics',
        'Onsemi': 'ON Semiconductor',
        'On Semi': 'ON Semiconductor'
    }
    df['Manufacturer'] = df['Manufacturer'].replace(mfg_mapping)
    
    # 3. Limpieza de Entropía: Tipos de datos mixtos
    df['Quantity_per_Assembly'] = pd.to_numeric(df['Quantity_per_Assembly'], errors='coerce').fillna(1).astype(int)
    
    # 4. Limpieza de Entropía: Ajuste de Lifecycle al ENUM de PostgreSQL ('Active', 'EOL', 'Obsolete')
    # Rellenamos NaNs (los de compras no saben el estado) asumiendo por prudencia que siguen activos
    df['Lifecycle'] = df['Lifecycle'].fillna('Active')
    # Mapeamos estados no soportados por el ENUM (como NRND) al más cercano
    df['Lifecycle'] = df['Lifecycle'].replace({'NRND': 'Active'})
    
    return df

def ingest_products(df: pd.DataFrame):
    print("\n--- Ingestando Products (Idempotente) ---")
    products = df[['End_Product_SKU', 'End_Product_Margin']].drop_duplicates().rename(
        columns={'End_Product_SKU': 'sku', 'End_Product_Margin': 'gross_margin'}
    )
    products['name'] = products['sku'] + " System"
    
    # Idempotencia: upsert basado en el UNIQUE constraint 'sku'
    data = products.to_dict(orient='records')
    res = supabase.table('products').upsert(data, on_conflict='sku').execute()
    print(f"Upserted {len(res.data)} products.")

def ingest_internal_parts(df: pd.DataFrame):
    print("\n--- Ingestando Internal Parts (Idempotente) ---")
    
    # Nivel 1: Subensamblajes
    assemblies = df[['Assembly_PN']].drop_duplicates()
    assemblies['internal_pn'] = assemblies['Assembly_PN']
    assemblies['part_type'] = 'assembly'
    assemblies['description'] = "Subensamblaje interno para " + assemblies['Assembly_PN']
    
    # Nivel 2: Componentes Base
    components = df[['Component_PN']].drop_duplicates()
    components['internal_pn'] = components['Component_PN']
    components['part_type'] = 'component'
    components['description'] = "Componente " + components['Component_PN']
    
    internal_parts = pd.concat([
        assemblies[['internal_pn', 'part_type', 'description']], 
        components[['internal_pn', 'part_type', 'description']]
    ]).drop_duplicates(subset=['internal_pn'])
    
    # Idempotencia: upsert basado en la constraint UNIQUE 'internal_pn'
    data = internal_parts.to_dict(orient='records')
    res = supabase.table('internal_parts').upsert(data, on_conflict='internal_pn').execute()
    print(f"Upserted {len(res.data)} internal parts (assemblies & components).")

def ingest_manufacturer_parts(df: pd.DataFrame):
    print("\n--- Ingestando Manufacturer Parts Telemetry (Idempotente) ---")
    mparts = df[['Manufacturer_PN', 'Manufacturer', 'Lifecycle']].drop_duplicates(subset=['Manufacturer_PN'])
    mparts = mparts.rename(columns={
        'Manufacturer_PN': 'mpn',
        'Manufacturer': 'manufacturer_name',
        'Lifecycle': 'lifecycle_status'
    })
    
    data = mparts.to_dict(orient='records')
    res = supabase.table('manufacturer_parts').upsert(data, on_conflict='mpn').execute()
    print(f"Upserted {len(res.data)} manufacturer external parts.")

def get_db_lookups():
    # Helper para obtener los UUIDs recien insertados
    prods = supabase.table('products').select("id, sku").execute()
    prod_map = {p['sku']: p['id'] for p in prods.data}
    
    parts = supabase.table('internal_parts').select("id, internal_pn").execute()
    part_map = {p['internal_pn']: p['id'] for p in parts.data}
    
    return prod_map, part_map

def ingest_aml(df: pd.DataFrame, part_map: dict):
    print("\n--- Ingestando AML (Mapeo Interno -> Externo) ---")
    # Agrupamos por PN interno y MPN externo
    aml_df = df[['Component_PN', 'Manufacturer_PN']].drop_duplicates()
    
    # Identificamos qué registros ya existen en la DB para lograr idempotencia (al no haber constraint de clave natural)
    existing = supabase.table('aml').select("internal_pn, manufacturer_pn").execute()
    # existing data in UUID format for internal_pn, so we map our incoming data to UUIDs first
    
    new_rows = []
    for _, row in aml_df.iterrows():
        internal_uuid = part_map.get(row['Component_PN'])
        mpn = row['Manufacturer_PN']
        
        if not internal_uuid: continue
        
        # Ockham's Idempotence check for AML
        if any(e['internal_pn'] == internal_uuid and e['manufacturer_pn'] == mpn for e in existing.data):
            continue # Ya existe
            
        new_rows.append({
            "internal_pn": internal_uuid,
            "manufacturer_pn": mpn,
            "preference_level": "Primary" # Simplificación para el artículo
        })
        
    if new_rows:
        res = supabase.table('aml').insert(new_rows).execute()
        print(f"Inserted {len(res.data)} new AML links.")
    else:
        print("No new AML links to insert (Idempotent success).")

def ingest_bom_lines(df: pd.DataFrame, prod_map: dict, part_map: dict):
    print("\n--- Ingestando BOM Lines (Grafo Bidireccional Segregado) ---")
    
    existing_bom = supabase.table('bom_lines').select("*").execute()
    
    new_bom_lines = []
    
    # 1. Grafo Nivel 1: Product -> Assembly
    print("Mapeando relaciones: Producto Final -> Subensamblaje...")
    prod_asm_df = df[['End_Product_SKU', 'Assembly_PN', 'Quantity_per_Assembly']].groupby(
        ['End_Product_SKU', 'Assembly_PN']
    ).max().reset_index() # Simplificación para este nivel de árbol
    
    for _, row in prod_asm_df.iterrows():
        parent_uuid = prod_map.get(row['End_Product_SKU'])
        child_uuid = part_map.get(row['Assembly_PN'])
        qty = 1 # Por defecto 1 ensamblaje por top product para mantener simetría
        
        if not parent_uuid or not child_uuid: continue
        
        # Idempotence check
        if any(e['parent_product_id'] == parent_uuid and e['child_pn'] == child_uuid for e in existing_bom.data):
             continue
             
        new_bom_lines.append({
            "parent_product_id": parent_uuid,
            "parent_assembly_id": None, # EXCLUSIVE XOR CONSTRAINT ENFORCED
            "child_pn": child_uuid,
            "quantity": qty
        })
        
    # 2. Grafo Nivel 2: Assembly -> Component
    print("Mapeando relaciones: Subensamblaje -> Componente...")
    asm_comp_df = df[['Assembly_PN', 'Component_PN', 'Quantity_per_Assembly']].drop_duplicates(subset=['Assembly_PN', 'Component_PN'])
    
    for _, row in asm_comp_df.iterrows():
        parent_uuid = part_map.get(row['Assembly_PN'])
        child_uuid = part_map.get(row['Component_PN'])
        qty = int(row['Quantity_per_Assembly'])
        
        if not parent_uuid or not child_uuid: continue
        
        # Idempotence check
        if any(e['parent_assembly_id'] == parent_uuid and e['child_pn'] == child_uuid for e in existing_bom.data):
             continue
             
        new_bom_lines.append({
            "parent_product_id": None, # EXCLUSIVE XOR CONSTRAINT ENFORCED
            "parent_assembly_id": parent_uuid,
            "child_pn": child_uuid,
            "quantity": qty
        })
        
    if new_bom_lines:
        res = supabase.table('bom_lines').insert(new_bom_lines).execute()
        print(f"Inserted {len(res.data)} jerarquías en el BOM Graph.")
    else:
        print("El Grafo BOM está completamente sincronizado (Idempotent success).")

def main():
    csv_path = os.path.join(os.path.dirname(__file__), "flat_bom_legacy.csv")
    cleaned_df = load_and_clean_data(csv_path)
    
    ingest_products(cleaned_df)
    ingest_internal_parts(cleaned_df)
    ingest_manufacturer_parts(cleaned_df)
    
    # Recuperamos los UUIDs maestos generados por Postgres para las Foreign Keys
    prod_map, part_map = get_db_lookups()
    
    ingest_aml(cleaned_df, part_map)
    ingest_bom_lines(cleaned_df, prod_map, part_map)
    
    print("\n[OK] Migración a entorno relacional completada al 100%.")

if __name__ == "__main__":
    main()
