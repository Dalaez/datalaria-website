"""
Forecast Manager v2 - Multi-SKU Parallel Orchestrator
=======================================================
Descarga datos multi-SKU, entrena Prophet en paralelo por
producto y sube predicciones consolidadas a Supabase.

Author: Datalaria
Version: 2.0.0
"""

import os
import sys
import logging
import warnings
import time
from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

# ── Silenciar TODOS los logs ruidosos ANTES de importar Prophet ──
logging.getLogger("prophet").setLevel(logging.ERROR)
logging.getLogger("cmdstanpy").setLevel(logging.ERROR)
logging.getLogger("prophet.plot").setLevel(logging.ERROR)
logging.getLogger("stan").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*Optimization.*")

# Cargar .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

# Supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

from forecasting_engine_v2 import ProphetPredictor


# ─── Constantes ────────────────────────────────────────
MODEL_VERSION = "prophet-v2.0"
SOURCE_TABLE = "sales_transactions"
TARGET_TABLE = "demand_forecasts"


def process_sku(
    sku: str,
    df_sku: pd.DataFrame,
    months: int,
    country_code: str
) -> Tuple[str, Optional[pd.DataFrame], Optional[str]]:
    """
    Entrena Prophet para un SKU individual.

    Esta función es el 'worker' que se ejecuta en cada thread.
    Si falla, captura el error y permite que los demás SKUs continúen.

    Args:
        sku: Nombre del SKU.
        df_sku: DataFrame filtrado con datos de ese SKU.
        months: Horizonte de predicción.
        country_code: Código ISO para festivos.

    Returns:
        Tupla (sku_name, forecast_df | None, error_msg | None).
    """
    try:
        predictor = ProphetPredictor(df_sku, sku_name=sku)
        predictor.preprocess_daily_aggregation()
        predictor.train_model(country_code=country_code)
        forecast = predictor.generate_forecast(months=months)
        return (sku, forecast, None)

    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}"
        return (sku, None, error_msg)


class ForecastManager:
    """
    Orquestador de forecast Multi-SKU con ejecución paralela.

    Flujo:
        1. Descarga datos limpios de Supabase (sin outliers).
        2. Agrupa por SKU.
        3. Entrena Prophet en paralelo (ThreadPoolExecutor).
        4. Consolida resultados y sube a Supabase.

    Attributes:
        supabase (Client): Cliente Supabase.
        execution_date (date): Fecha del snapshot.

    Example:
        >>> manager = ForecastManager()
        >>> result = manager.run_pipeline(months=12)
    """

    def __init__(self) -> None:
        """
        Inicializa con credenciales Supabase.

        Raises:
            ValueError: Si SUPABASE_URL o SUPABASE_KEY no configuradas.
        """
        if not SUPABASE_AVAILABLE:
            raise ImportError(
                "Paquete 'supabase' no instalado. "
                "Ejecuta: pip install supabase"
            )

        supabase_url: Optional[str] = os.environ.get("SUPABASE_URL")
        supabase_key: Optional[str] = os.environ.get("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError(
                "Credenciales no encontradas. "
                "Configura SUPABASE_URL y SUPABASE_KEY en .env"
            )

        self.supabase: Any = create_client(supabase_url, supabase_key)
        self.execution_date: date = date.today()

        print(f"[OK] Conectado a Supabase: {supabase_url[:35]}...")
        print(f"[OK] Fecha de ejecución (snapshot): {self.execution_date}")

    def fetch_clean_data(self) -> pd.DataFrame:
        """
        Descarga transacciones limpias Multi-SKU desde Supabase.

        Returns:
            DataFrame con columnas [date, sku, qty].

        Raises:
            RuntimeError: Si no hay datos disponibles.
        """
        response = (
            self.supabase
            .table(SOURCE_TABLE)
            .select("date, sku, qty")
            .eq("is_outlier", False)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                f"No se encontraron datos en '{SOURCE_TABLE}' "
                "con is_outlier = FALSE."
            )

        df: pd.DataFrame = pd.DataFrame(response.data)
        return df

    def run_pipeline(
        self,
        months: int = 12,
        country_code: str = "ES",
        upload: bool = True,
        max_workers: int = 3
    ) -> Dict[str, Any]:
        """
        Pipeline completo: descarga → paralleliza → consolida → upload.

        Args:
            months: Horizonte de predicción.
            country_code: Código ISO para festivos.
            upload: Si True, sube a Supabase.
            max_workers: Threads para entrenamiento paralelo.

        Returns:
            Diccionario con métricas del pipeline.
        """
        result: Dict[str, Any] = {
            "success": False,
            "records_downloaded": 0,
            "skus_total": 0,
            "skus_success": 0,
            "skus_failed": 0,
            "forecast_days_total": 0,
            "records_uploaded": 0,
            "errors": [],
            "error": None
        }

        try:
            print("\n" + "=" * 60)
            print("  S&OP DEMAND FORECASTING v2 (Multi-SKU)")
            print("=" * 60)

            # 1. Descargar datos
            print(f"\n[1/4] Descargando datos de Supabase...")
            df: pd.DataFrame = self.fetch_clean_data()
            result["records_downloaded"] = len(df)

            skus: List[str] = sorted(df["sku"].unique().tolist())
            result["skus_total"] = len(skus)
            print(f"      {len(df):,} registros | {len(skus)} SKUs: {skus}")

            # 2. Entrenar en paralelo
            print(f"\n[2/4] Entrenando Prophet por SKU ({max_workers} workers)...")
            t0 = time.perf_counter()

            forecasts: List[pd.DataFrame] = []
            sku_dataframes: Dict[str, pd.DataFrame] = {
                sku: df[df["sku"] == sku][["date", "qty"]].copy()
                for sku in skus
            }

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(
                        process_sku, sku, sku_df, months, country_code
                    ): sku
                    for sku, sku_df in sku_dataframes.items()
                }

                for future in as_completed(futures):
                    sku_name, forecast_df, error = future.result()

                    if error:
                        print(f"      [!!] {sku_name}: FAILED - {error}")
                        result["skus_failed"] += 1
                        result["errors"].append(
                            {"sku": sku_name, "error": error}
                        )
                    else:
                        days = len(forecast_df)
                        print(f"      [OK] {sku_name}: {days} dias de forecast")
                        forecasts.append(forecast_df)
                        result["skus_success"] += 1

            elapsed = time.perf_counter() - t0
            print(f"\n      Entrenamiento completado en {elapsed:.1f}s")

            # 3. Consolidar
            if not forecasts:
                raise RuntimeError("Todos los SKUs fallaron. Sin datos.")

            print(f"\n[3/4] Consolidando {len(forecasts)} forecasts...")
            all_forecasts: pd.DataFrame = pd.concat(
                forecasts, ignore_index=True
            )
            result["forecast_days_total"] = len(all_forecasts)

            # Añadir metadata
            all_forecasts["execution_date"] = self.execution_date.isoformat()
            all_forecasts["model_version"] = MODEL_VERSION
            all_forecasts["ds"] = pd.to_datetime(
                all_forecasts["ds"]
            ).dt.strftime("%Y-%m-%d")

            # Preview
            self._print_forecast_summary(all_forecasts)

            # 4. Upload
            if upload:
                print(f"\n[4/4] Subiendo a Supabase ({TARGET_TABLE})...")
                uploaded: int = self._upload_forecast(all_forecasts)
                result["records_uploaded"] = uploaded
                print(f"      {uploaded:,} registros insertados/actualizados")
            else:
                print(f"\n[4/4] [DRY-RUN] Predicciones NO subidas")

            result["success"] = True

            # Resumen final
            print("\n" + "=" * 60)
            print("  PIPELINE COMPLETADO")
            print("=" * 60)
            print(f"\n  SKUs procesados: {result['skus_success']}/{result['skus_total']}")
            if result["skus_failed"] > 0:
                print(f"  SKUs fallidos:   {result['skus_failed']}")
                for err in result["errors"]:
                    print(f"    - {err['sku']}: {err['error']}")
            print(f"  Forecast total:  {result['forecast_days_total']:,} registros")
            print(f"  Records subidos: {result['records_uploaded']:,}")
            print(f"  Tiempo total:    {elapsed:.1f}s")

        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            print(f"\n  ERROR FATAL: {result['error']}")

        return result

    def _print_forecast_summary(self, df: pd.DataFrame) -> None:
        """Imprime resumen del forecast consolidado por SKU."""
        print("\n" + "-" * 60)
        print("  FORECAST SUMMARY")
        print("-" * 60)

        for sku in sorted(df["sku"].unique()):
            sku_data = df[df["sku"] == sku]
            avg_yhat = sku_data["yhat"].mean()
            max_yhat = sku_data["yhat"].max()
            min_yhat = sku_data["yhat"].min()
            days = len(sku_data)
            print(
                f"  {sku}: {days} dias | "
                f"avg={avg_yhat:.0f} | "
                f"min={min_yhat} | max={max_yhat}"
            )

        print("-" * 60)

    def _upload_forecast(self, forecast_df: pd.DataFrame) -> int:
        """
        Sube forecast consolidado a Supabase via batch upsert.

        Args:
            forecast_df: DataFrame con todas las predicciones.

        Returns:
            Número de registros procesados.
        """
        if forecast_df.empty:
            return 0

        records = forecast_df.to_dict(orient="records")

        batch_size: int = 500
        total_uploaded: int = 0

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            self.supabase.table(TARGET_TABLE).upsert(batch).execute()
            total_uploaded += len(batch)

        return total_uploaded


def main() -> None:
    """Punto de entrada."""
    print("\n" + "=" * 60)
    print("  S&OP FORECASTING v2 - Execution Mode")
    print("=" * 60)

    try:
        manager = ForecastManager()
        result = manager.run_pipeline(
            months=12,
            country_code="ES",
            upload=True,
            max_workers=3
        )

        if not result["success"]:
            print(f"\n  FALLO: {result['error']}")
            sys.exit(1)

    except (ValueError, ImportError) as e:
        print(f"\n  CONFIGURACIÓN: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
