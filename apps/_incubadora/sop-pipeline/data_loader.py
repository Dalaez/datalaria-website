"""
Data Loader Module for S&OP Pipeline
=====================================
Orquestador de pipeline: Lee CSV → Limpia → Carga a Supabase.

Author: Datalaria
Version: 1.0.0
"""

import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path

import pandas as pd

# Import opcional de Supabase (para permitir dry-run sin dependencia)
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None  # Type hint placeholder

# Cargar variables de entorno desde .env (si existe)
try:
    from dotenv import load_dotenv
    # Buscar .env en el directorio del script
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv no instalado, usar variables de entorno del sistema

from data_hygiene import SupplyChainSanitizer


class SupabaseIngestor:
    """
    Clase para orquestar el pipeline de ingesta de datos a Supabase.
    
    Coordina la lectura de archivos CSV, limpieza mediante
    SupplyChainSanitizer, y carga a PostgreSQL vía Supabase.
    
    Attributes:
        supabase (Client): Cliente de Supabase inicializado.
        table_name (str): Nombre de la tabla destino.
    
    Environment Variables Required:
        SUPABASE_URL: URL del proyecto Supabase.
        SUPABASE_KEY: Clave de API (service_role para upserts).
    
    Example:
        >>> ingestor = SupabaseIngestor()
        >>> ingestor.process_file("sales_data.csv")
    """
    
    def __init__(self, table_name: str = "sales_transactions") -> None:
        """
        Inicializa el ingestor cargando credenciales desde variables de entorno.
        
        Args:
            table_name: Nombre de la tabla destino en Supabase.
        
        Raises:
            ValueError: Si las variables de entorno no están configuradas.
        """
        self.table_name = table_name
        
        # Cargar credenciales desde entorno
        supabase_url: Optional[str] = os.environ.get("SUPABASE_URL")
        supabase_key: Optional[str] = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError(
                "Credenciales de Supabase no encontradas. "
                "Configure SUPABASE_URL y SUPABASE_KEY en variables de entorno."
            )
        
        # Inicializar cliente Supabase
        self.supabase: Client = create_client(supabase_url, supabase_key)
        print(f"✓ Conectado a Supabase: {supabase_url[:30]}...")
    
    def process_file(
        self, 
        file_path: str,
        zscore_threshold: float = 3.0,
        upload_to_db: bool = True
    ) -> Dict[str, Any]:
        """
        Procesa un archivo CSV completo: lectura, limpieza y carga.
        
        Pipeline:
            1. Lee CSV desde ruta local.
            2. Instancia SupplyChainSanitizer.
            3. Ejecuta limpieza estructural.
            4. Detecta outliers con Z-Score.
            5. Imprime reporte de auditoría.
            6. Sube datos limpios a Supabase (upsert).
        
        Args:
            file_path: Ruta al archivo CSV a procesar.
            zscore_threshold: Umbral para detección de outliers.
            upload_to_db: Si True, sube a Supabase. Si False, solo limpia.
        
        Returns:
            Diccionario con reporte de auditoría y estado de carga.
        
        Raises:
            FileNotFoundError: Si el archivo no existe.
            pd.errors.ParserError: Si el CSV tiene formato inválido.
        """
        result: Dict[str, Any] = {
            "success": False,
            "audit_report": {},
            "rows_uploaded": 0,
            "error": None
        }
        
        try:
            # 1. Validar existencia del archivo
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
            
            print(f"\n{'='*60}")
            print(f"📂 Procesando: {file_path.name}")
            print(f"{'='*60}")
            
            # 2. Leer CSV
            print("\n[1/4] Leyendo archivo CSV...")
            df: pd.DataFrame = pd.read_csv(file_path)
            print(f"      → {len(df)} filas leídas")
            
            # 3. Inicializar sanitizador
            print("\n[2/4] Ejecutando limpieza estructural...")
            sanitizer = SupplyChainSanitizer(df)
            sanitizer.structural_clean()
            
            # 4. Detectar outliers
            print("\n[3/4] Detectando outliers (Z-Score)...")
            sanitizer.detect_outliers_zscore(threshold=zscore_threshold)
            
            # 5. Obtener resultados
            clean_df = sanitizer.get_clean_data()
            audit_report = sanitizer.get_audit_report()
            result["audit_report"] = audit_report
            
            # 6. Imprimir reporte
            self._print_audit_report(audit_report)
            
            # 7. Subir a Supabase
            if upload_to_db:
                print("\n[4/4] Subiendo datos a Supabase...")
                rows_uploaded = self._upload_to_supabase(clean_df)
                result["rows_uploaded"] = rows_uploaded
                print(f"      → {rows_uploaded} filas insertadas/actualizadas")
            else:
                print("\n[4/4] Modo dry-run: datos NO subidos a Supabase")
            
            result["success"] = True
            print(f"\n{'='*60}")
            print("✅ Pipeline completado exitosamente")
            print(f"{'='*60}\n")
            
        except FileNotFoundError as e:
            result["error"] = f"FileNotFoundError: {e}"
            print(f"\n❌ Error: {e}")
            
        except pd.errors.ParserError as e:
            result["error"] = f"CSV ParseError: {e}"
            print(f"\n❌ Error parseando CSV: {e}")
            
        except Exception as e:
            result["error"] = f"UnexpectedError: {type(e).__name__} - {e}"
            print(f"\n❌ Error inesperado: {type(e).__name__} - {e}")
        
        return result
    
    def _print_audit_report(self, report: Dict[str, Any]) -> None:
        """Imprime el reporte de auditoría formateado."""
        print("\n" + "-"*40)
        print("📊 REPORTE DE AUDITORÍA")
        print("-"*40)
        print(f"  Filas iniciales:         {report['initial_rows']:,}")
        print(f"  Fechas inválidas:        {report['rows_with_invalid_dates']:,}")
        print(f"  NaNs en campos críticos: {report['rows_with_null_criticals']:,}")
        print(f"  Duplicados eliminados:   {report['duplicate_rows_removed']:,}")
        print(f"  Filas finales:           {report['final_rows']:,}")
        print("-"*40)
        print(f"  Outliers detectados:     {report['outliers_detected']:,}")
        print(f"  % Outliers:              {report['outlier_percentage']}%")
        print("-"*40)
    
    def _upload_to_supabase(self, df: pd.DataFrame) -> int:
        """
        Sube DataFrame a Supabase usando upsert.
        
        Args:
            df: DataFrame limpio a cargar.
        
        Returns:
            Número de filas procesadas.
        """
        if df.empty:
            return 0
        
        # Convertir fechas a string ISO para JSON
        df_upload = df.copy()
        if "date" in df_upload.columns:
            df_upload["date"] = df_upload["date"].dt.strftime("%Y-%m-%d")
        
        # Convertir a lista de diccionarios
        records = df_upload.to_dict(orient="records")
        
        # Upsert a Supabase (requiere primary key configurada en tabla)
        response = self.supabase.table(self.table_name).upsert(records).execute()
        
        return len(records)


def main() -> None:
    """Punto de entrada para testing local."""
    print("\n" + "="*60)
    print("🚀 S&OP DATA PIPELINE - Local Test Mode")
    print("="*60)
    
    # Verificar si existe archivo de prueba
    test_file = Path(__file__).parent / "dirty_sales_sample.csv"
    
    if not test_file.exists():
        print(f"\n⚠️  Archivo de prueba no encontrado: {test_file}")
        print("   Ejecuta primero: python generate_dummy_data.py")
        sys.exit(1)
    
    # Verificar credenciales
    if not os.environ.get("SUPABASE_URL"):
        print("\n⚠️  Variables de entorno no configuradas.")
        print("   Ejecutando en modo DRY-RUN (sin subir a Supabase)...")
        
        # Modo dry-run: solo limpieza
        df = pd.read_csv(test_file)
        sanitizer = SupplyChainSanitizer(df)
        sanitizer.structural_clean().detect_outliers_zscore()
        
        print("\n📊 REPORTE DE AUDITORÍA")
        print("-"*40)
        for key, value in sanitizer.get_audit_report().items():
            print(f"  {key}: {value}")
        
        print("\n📋 Muestra de datos limpios (primeras 5 filas):")
        print(sanitizer.get_clean_data().head().to_string())
        
    else:
        # Modo completo con Supabase
        ingestor = SupabaseIngestor()
        result = ingestor.process_file(str(test_file))
        
        if not result["success"]:
            print(f"\n❌ Pipeline falló: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
