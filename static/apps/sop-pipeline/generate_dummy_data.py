"""
Dummy Data Generator for S&OP Pipeline Testing
================================================
Genera datos de ventas "sucios" para probar el pipeline de limpieza.

Author: Datalaria
Version: 1.0.0
"""

import random
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import numpy as np


def generate_dirty_sales_data(
    num_rows: int = 100,
    output_path: str = "dirty_sales_sample.csv"
) -> pd.DataFrame:
    """
    Genera un CSV con datos de ventas intencionalmente sucios.
    
    El dataset incluye problemas típicos de datos reales:
        - Fechas en formatos mixtos o inválidos
        - Valores nulos en campos críticos
        - Filas duplicadas exactas
        - Outliers masivos (para probar Z-Score)
    
    Args:
        num_rows: Número de filas a generar (default: 100).
        output_path: Ruta donde guardar el CSV.
    
    Returns:
        DataFrame generado (antes de introducir suciedad de strings).
    
    Output Columns:
        - transaction_id: ID único de transacción
        - date: Fecha de venta (con errores intencionales)
        - product_id: ID del producto
        - product_name: Nombre del producto
        - qty: Cantidad vendida (con nulos y outliers)
        - unit_price: Precio unitario
        - region: Región de venta
    """
    print("🏭 Generando datos de ventas sucios...")
    print(f"   → {num_rows} filas objetivo")
    
    # Configuración
    np.random.seed(42)  # Reproducibilidad
    random.seed(42)
    
    base_date = datetime(2024, 1, 1)
    products = [
        ("SKU001", "Motor Eléctrico 5HP"),
        ("SKU002", "Bomba Centrífuga"),
        ("SKU003", "Válvula de Control"),
        ("SKU004", "Sensor de Presión"),
        ("SKU005", "PLC Siemens S7"),
    ]
    regions = ["Norte", "Sur", "Centro", "Este", "Oeste"]
    
    # Generar datos base "limpios"
    clean_rows = num_rows - 15  # Reservar espacio para problemas
    
    data = {
        "transaction_id": [f"TXN{str(i).zfill(6)}" for i in range(1, clean_rows + 1)],
        "date": [],
        "product_id": [],
        "product_name": [],
        "qty": [],
        "unit_price": [],
        "region": []
    }
    
    # Generar filas limpias
    for i in range(clean_rows):
        # Fecha: formato estándar YYYY-MM-DD
        days_offset = random.randint(0, 365)
        date = base_date + timedelta(days=days_offset)
        data["date"].append(date.strftime("%Y-%m-%d"))
        
        # Producto aleatorio
        product = random.choice(products)
        data["product_id"].append(product[0])
        data["product_name"].append(product[1])
        
        # Cantidad: distribución normal centrada en 100
        qty = max(1, int(np.random.normal(100, 30)))
        data["qty"].append(qty)
        
        # Precio
        data["unit_price"].append(round(random.uniform(50, 500), 2))
        
        # Región
        data["region"].append(random.choice(regions))
    
    # Convertir a DataFrame
    df = pd.DataFrame(data)
    
    # ============================================
    # INTRODUCIR PROBLEMAS INTENCIONALES
    # ============================================
    
    print("\n📊 Introduciendo anomalías de datos:")
    
    # 1. FECHAS EN FORMATOS MIXTOS/INVÁLIDOS (5 filas)
    print("   [1] Fechas en formatos mixtos e inválidos...")
    
    bad_date_rows = [
        {"transaction_id": "TXN_BAD01", "date": "01/15/2024", "product_id": "SKU001", 
         "product_name": "Motor Eléctrico 5HP", "qty": 80, "unit_price": 150.0, "region": "Norte"},
        {"transaction_id": "TXN_BAD02", "date": "15-Mar-2024", "product_id": "SKU002",
         "product_name": "Bomba Centrífuga", "qty": 90, "unit_price": 200.0, "region": "Sur"},
        {"transaction_id": "TXN_BAD03", "date": "not_a_date", "product_id": "SKU003",
         "product_name": "Válvula de Control", "qty": 70, "unit_price": 75.0, "region": "Centro"},
        {"transaction_id": "TXN_BAD04", "date": "2024/02/30", "product_id": "SKU004",  # Fecha imposible
         "product_name": "Sensor de Presión", "qty": 110, "unit_price": 300.0, "region": "Este"},
        {"transaction_id": "TXN_BAD05", "date": "", "product_id": "SKU005",  # Fecha vacía
         "product_name": "PLC Siemens S7", "qty": 50, "unit_price": 450.0, "region": "Oeste"},
    ]
    df = pd.concat([df, pd.DataFrame(bad_date_rows)], ignore_index=True)
    
    # 2. NULOS EN CANTIDAD (3 filas)
    print("   [2] Valores nulos en cantidad...")
    
    null_qty_rows = [
        {"transaction_id": "TXN_NULL01", "date": "2024-05-10", "product_id": "SKU001",
         "product_name": "Motor Eléctrico 5HP", "qty": None, "unit_price": 160.0, "region": "Norte"},
        {"transaction_id": "TXN_NULL02", "date": "2024-06-15", "product_id": "SKU002",
         "product_name": "Bomba Centrífuga", "qty": np.nan, "unit_price": 210.0, "region": "Sur"},
        {"transaction_id": "TXN_NULL03", "date": "2024-07-20", "product_id": "SKU003",
         "product_name": "Válvula de Control", "qty": None, "unit_price": 80.0, "region": "Centro"},
    ]
    df = pd.concat([df, pd.DataFrame(null_qty_rows)], ignore_index=True)
    
    # 3. DUPLICADOS EXACTOS (4 filas = 2 pares de duplicados)
    print("   [3] Filas duplicadas exactas...")
    
    # Tomar 2 filas existentes y duplicarlas
    duplicates = df.iloc[[5, 10]].copy()
    duplicates = pd.concat([duplicates, duplicates], ignore_index=True)  # 4 filas
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # 4. OUTLIERS MASIVOS (3 filas con cantidades extremas)
    print("   [4] Outliers masivos para test Z-Score...")
    
    outlier_rows = [
        {"transaction_id": "TXN_OUT01", "date": "2024-08-01", "product_id": "SKU001",
         "product_name": "Motor Eléctrico 5HP", "qty": 50000, "unit_price": 150.0, "region": "Norte"},  # ~500x media
        {"transaction_id": "TXN_OUT02", "date": "2024-09-15", "product_id": "SKU002",
         "product_name": "Bomba Centrífuga", "qty": 75000, "unit_price": 200.0, "region": "Sur"},      # ~750x media
        {"transaction_id": "TXN_OUT03", "date": "2024-10-20", "product_id": "SKU003",
         "product_name": "Válvula de Control", "qty": 100000, "unit_price": 75.0, "region": "Centro"}, # 1000x media
    ]
    df = pd.concat([df, pd.DataFrame(outlier_rows)], ignore_index=True)
    
    # Mezclar el orden
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Guardar CSV
    output_file = Path(output_path)
    df.to_csv(output_file, index=False)
    
    # Resumen
    print(f"\n✅ Dataset generado: {output_file.absolute()}")
    print(f"   → Total filas: {len(df)}")
    print(f"   → Columnas: {list(df.columns)}")
    print("\n📋 Resumen de anomalías introducidas:")
    print(f"   • Fechas problemáticas:  5")
    print(f"   • Valores nulos en qty:  3")
    print(f"   • Filas duplicadas:      4")
    print(f"   • Outliers (qty extrema): 3")
    print(f"   • Total anomalías:      15")
    
    # Preview
    print("\n📝 Preview (primeras 10 filas):")
    print(df.head(10).to_string())
    
    return df


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 S&OP Pipeline - Generador de Datos de Prueba")
    print("="*60)
    
    df = generate_dirty_sales_data(
        num_rows=100,
        output_path="dirty_sales_sample.csv"
    )
    
    print("\n" + "="*60)
    print("✅ Generación completada. Ejecuta el pipeline:")
    print("   python data_loader.py")
    print("="*60 + "\n")
