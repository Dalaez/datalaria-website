"""
Data Loader v2 - Multi-SKU Orchestrator
=========================================
Lee enterprise CSV, limpia por SKU, sube a Supabase.

Author: Datalaria
Version: 2.0.0
"""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

import pandas as pd

# Cargar variables de entorno desde .env (si existe)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

# Import opcional de Supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

from data_hygiene_v2 import SupplyChainSanitizer


# ─── Constantes ────────────────────────────────────────
TARGET_TABLE = "sales_transactions"


class SupabaseIngestor:
    """
    Orquestador de ingesta Multi-SKU a Supabase.

    Flujo:
        1. Lee CSV con datos multi-SKU.
        2. Limpia con SupplyChainSanitizer v2 (Z-Score por SKU).
        3. Sube datos limpios a Supabase via upsert.

    Example:
        >>> ingestor = SupabaseIngestor()
        >>> result = ingestor.process_file("enterprise_sales_history.csv")
    """

    def __init__(self) -> None:
        """
        Inicializa con credenciales Supabase (opcionales para dry-run).
        """
        self.supabase: Optional[Any] = None

        supabase_url: Optional[str] = os.environ.get("SUPABASE_URL")
        supabase_key: Optional[str] = os.environ.get("SUPABASE_KEY")

        if SUPABASE_AVAILABLE and supabase_url and supabase_key:
            self.supabase = create_client(supabase_url, supabase_key)
            print(f"[OK] Conectado a Supabase: {supabase_url[:35]}...")
        else:
            print("[INFO] Supabase no configurado. Modo DRY-RUN activado.")

    def process_file(
        self,
        file_path: str,
        zscore_threshold: float = 3.0,
        upload_to_db: bool = True
    ) -> Dict[str, Any]:
        """
        Pipeline completo: CSV → Limpieza → Supabase.

        Args:
            file_path: Ruta al CSV con datos multi-SKU.
            zscore_threshold: Umbral de Z-Score para outliers.
            upload_to_db: Si True, sube a Supabase.

        Returns:
            Diccionario con resultado del proceso.
        """
        result: Dict[str, Any] = {
            "success": False,
            "rows_read": 0,
            "rows_clean": 0,
            "outliers_total": 0,
            "records_uploaded": 0,
            "error": None
        }

        try:
            print("\n" + "=" * 60)
            print("  S&OP DATA INGESTION PIPELINE v2 (Multi-SKU)")
            print("=" * 60)

            # 1. Leer CSV
            print(f"\n[1/3] Leyendo {file_path}...")
            df: pd.DataFrame = pd.read_csv(file_path)
            result["rows_read"] = len(df)
            print(f"      {len(df):,} filas leidas")

            # 2. Limpiar
            print(f"\n[2/3] Ejecutando limpieza (Z-Score threshold={zscore_threshold})...")
            sanitizer = SupplyChainSanitizer(df)
            sanitizer.structural_clean()
            sanitizer.detect_outliers_zscore(threshold=zscore_threshold)

            # Reporte
            sanitizer.print_audit_report()

            audit: Dict[str, Any] = sanitizer.get_audit_report()
            clean_df: pd.DataFrame = sanitizer.get_clean_data()
            result["rows_clean"] = len(clean_df)
            result["outliers_total"] = audit.get("outliers_detected", 0)

            # 3. Upload
            if upload_to_db and self.supabase:
                print(f"\n[3/3] Subiendo a Supabase ({TARGET_TABLE})...")
                uploaded: int = self._upload_data(clean_df)
                result["records_uploaded"] = uploaded
                print(f"      {uploaded:,} registros insertados/actualizados")
            else:
                print(f"\n[3/3] [DRY-RUN] Datos NO subidos a Supabase")

            result["success"] = True

            # Resumen por SKU
            self._print_sku_summary(clean_df)

            print("\n" + "=" * 60)
            print("  PIPELINE COMPLETADO")
            print("=" * 60)

        except FileNotFoundError:
            result["error"] = f"Archivo no encontrado: {file_path}"
            print(f"\n  ERROR: {result['error']}")
        except pd.errors.ParserError as e:
            result["error"] = f"Error de parsing CSV: {e}"
            print(f"\n  ERROR: {result['error']}")
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            print(f"\n  ERROR: {result['error']}")

        return result

    def _print_sku_summary(self, df: pd.DataFrame) -> None:
        """Imprime resumen por SKU."""
        if "sku" not in df.columns:
            return

        print("\n" + "-" * 50)
        print("  RESUMEN POR SKU")
        print("-" * 50)

        for sku in sorted(df["sku"].unique()):
            sku_data = df[df["sku"] == sku]
            total = len(sku_data)
            clean = len(sku_data[~sku_data["is_outlier"]])
            outliers = len(sku_data[sku_data["is_outlier"]])
            avg_qty = sku_data[~sku_data["is_outlier"]]["qty"].mean()

            print(f"  {sku}: {total:,} filas | "
                  f"{clean:,} limpias | "
                  f"{outliers} outliers | "
                  f"avg={avg_qty:.1f}/dia")

        print("-" * 50)

    def _upload_data(self, df: pd.DataFrame) -> int:
        """
        Sube datos limpios a Supabase usando upsert por lotes.

        Args:
            df: DataFrame limpio con columnas [date, sku, qty, is_outlier].

        Returns:
            Número de registros procesados.
        """
        if df.empty or self.supabase is None:
            return 0

        # Preparar registros
        upload_df: pd.DataFrame = df[["date", "sku", "qty", "is_outlier"]].copy()
        upload_df["date"] = upload_df["date"].dt.strftime("%Y-%m-%d")
        upload_df["is_outlier"] = upload_df["is_outlier"].astype(bool)

        records = upload_df.to_dict(orient="records")

        # Upsert por lotes
        batch_size: int = 500
        total_uploaded: int = 0

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            self.supabase.table(TARGET_TABLE).upsert(batch).execute()
            total_uploaded += len(batch)

        return total_uploaded


def main() -> None:
    """Punto de entrada para ejecución local."""
    print("\n" + "=" * 60)
    print("  S&OP DATA LOADER v2 - Execution Mode")
    print("=" * 60)

    # Archivo enterprise
    csv_file = str(Path(__file__).parent / "enterprise_sales_history.csv")

    try:
        ingestor = SupabaseIngestor()
        result = ingestor.process_file(
            file_path=csv_file,
            zscore_threshold=3.0,
            upload_to_db=True
        )

        # Resumen final
        print(f"\n  RESUMEN FINAL:")
        print(f"  - Filas leidas:       {result['rows_read']:,}")
        print(f"  - Filas limpias:      {result['rows_clean']:,}")
        print(f"  - Outliers:           {result['outliers_total']}")
        print(f"  - Registros subidos:  {result['records_uploaded']:,}")

        if not result["success"]:
            print(f"\n  FALLO: {result['error']}")
            sys.exit(1)

    except Exception as e:
        print(f"\n  ERROR FATAL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
