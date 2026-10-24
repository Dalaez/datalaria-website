"""
Forecast Manager for S&OP Pipeline
====================================
Orquestador: Descarga datos limpios → Entrena Prophet → Sube predicciones.

Author: Datalaria
Version: 1.0.0
"""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import date

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

from forecasting_engine import ProphetPredictor


# ─── Constantes ────────────────────────────────────────
MODEL_VERSION = "prophet-v1.0"
SOURCE_TABLE = "sales_transactions"
TARGET_TABLE = "demand_forecasts"


class ForecastManager:
    """
    Orquestador del pipeline de predicción de demanda.

    Flujo completo:
        1. Descarga datos limpios de Supabase (sin outliers).
        2. Entrena modelo Prophet.
        3. Genera forecast a 12 meses.
        4. Sube predicciones a Supabase.

    Attributes:
        supabase (Client): Cliente Supabase.
        execution_date (date): Fecha de ejecución (snapshot).

    Example:
        >>> manager = ForecastManager()
        >>> result = manager.run_pipeline(months=12)
    """

    def __init__(self) -> None:
        """
        Inicializa el manager con credenciales de Supabase.

        Raises:
            ValueError: Si las credenciales no están configuradas.
            ImportError: Si supabase-py no está instalado.
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

        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.execution_date: date = date.today()

        print(f"[OK] Conectado a Supabase: {supabase_url[:35]}...")
        print(f"[OK] Fecha de ejecución (snapshot): {self.execution_date}")

    def fetch_clean_data(self) -> pd.DataFrame:
        """
        Descarga transacciones limpias desde Supabase.

        Filtra registros donde is_outlier = FALSE para usar
        solo la señal limpia en la predicción.

        Returns:
            DataFrame con datos históricos limpios.

        Raises:
            RuntimeError: Si no hay datos disponibles.
        """
        print("\n[1/4] Descargando datos de Supabase...")

        response = (
            self.supabase
            .table(SOURCE_TABLE)
            .select("date, qty")
            .eq("is_outlier", False)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                f"No se encontraron datos en '{SOURCE_TABLE}' "
                "con is_outlier = FALSE. "
                "¿Ejecutaste el pipeline de limpieza (Part 1)?"
            )

        df = pd.DataFrame(response.data)
        print(f"      {len(df):,} registros descargados (outliers excluidos)")

        return df

    def run_pipeline(
        self,
        months: int = 12,
        country_code: str = "ES",
        upload: bool = True
    ) -> Dict[str, Any]:
        """
        Ejecuta el pipeline completo de forecasting.

        Args:
            months: Horizonte de predicción en meses.
            country_code: Código ISO para festivos.
            upload: Si True, sube a Supabase. Si False, dry-run.

        Returns:
            Diccionario con estado, métricas y errores.
        """
        result: Dict[str, Any] = {
            "success": False,
            "records_downloaded": 0,
            "forecast_days": 0,
            "records_uploaded": 0,
            "error": None
        }

        try:
            print("\n" + "=" * 60)
            print("  S&OP DEMAND FORECASTING PIPELINE")
            print("=" * 60)

            # 1. Descargar datos
            df = self.fetch_clean_data()
            result["records_downloaded"] = len(df)

            # 2. Preprocesar
            print("\n[2/4] Preprocesando serie temporal...")
            predictor = ProphetPredictor(df)
            predictor.preprocess_daily_aggregation()

            # 3. Entrenar modelo
            print(f"\n[3/4] Entrenando modelo ({MODEL_VERSION})...")
            predictor.train_model(country_code=country_code)

            # 4. Generar forecast
            print(f"\n[4/4] Generando forecast a {months} meses...")
            forecast = predictor.generate_forecast(months=months)
            result["forecast_days"] = len(forecast)

            # Añadir metadata de ejecución
            forecast["execution_date"] = self.execution_date.isoformat()
            forecast["model_version"] = MODEL_VERSION
            forecast["ds"] = forecast["ds"].dt.strftime("%Y-%m-%d")

            # Preview
            print("\n" + "-" * 50)
            print("  FORECAST PREVIEW (primeros 10 días)")
            print("-" * 50)
            print(forecast.head(10).to_string(index=False))
            print("-" * 50)

            # Upload
            if upload:
                print("\n  Subiendo predicciones a Supabase...")
                uploaded = self._upload_forecast(forecast)
                result["records_uploaded"] = uploaded
                print(f"  {uploaded:,} registros insertados/actualizados")
            else:
                print("\n  [DRY-RUN] Predicciones NO subidas a Supabase")

            result["success"] = True
            print("\n" + "=" * 60)
            print("  PIPELINE COMPLETADO")
            print("=" * 60)

        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            print(f"\n  ERROR: {type(e).__name__}: {e}")

        return result

    def _upload_forecast(self, forecast_df: pd.DataFrame) -> int:
        """
        Sube predicciones a la tabla demand_forecasts usando upsert.

        Args:
            forecast_df: DataFrame con forecast + metadata.

        Returns:
            Número de registros procesados.
        """
        if forecast_df.empty:
            return 0

        records = forecast_df.to_dict(orient="records")

        # Upsert por lotes (Supabase tiene límites de payload)
        batch_size = 500
        total_uploaded = 0

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            self.supabase.table(TARGET_TABLE).upsert(batch).execute()
            total_uploaded += len(batch)

        return total_uploaded


def main() -> None:
    """Punto de entrada para ejecución local."""
    print("\n" + "=" * 60)
    print("  S&OP FORECASTING - Execution Mode")
    print("=" * 60)

    try:
        manager = ForecastManager()
        result = manager.run_pipeline(
            months=12,
            country_code="ES",
            upload=True
        )

        # Resumen final
        print("\n  RESUMEN:")
        print(f"  - Registros descargados: {result['records_downloaded']:,}")
        print(f"  - Días de forecast:      {result['forecast_days']:,}")
        print(f"  - Registros subidos:     {result['records_uploaded']:,}")

        if not result["success"]:
            print(f"\n  FALLO: {result['error']}")
            sys.exit(1)

    except (ValueError, ImportError) as e:
        print(f"\n  CONFIGURACIÓN: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
