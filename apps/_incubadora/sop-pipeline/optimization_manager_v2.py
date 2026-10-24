"""
Optimization Manager v2 - Multi-SKU Orchestrator
==================================================
Descarga forecast multi-SKU, agrega a mensual, ejecuta
el solver unificado y sube el plan a Supabase.

Author: Datalaria
Version: 2.0.0
"""

import os
import sys
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import date

import pandas as pd

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

from optimization_engine_v2 import UnifiedSupplyOptimizer


# ─── Constantes ────────────────────────────────────────
SOURCE_TABLE = "demand_forecasts"
TARGET_TABLE = "supply_plans"

# ─── Parametros Financieros por SKU ────────────────────
OPTIMIZATION_PARAMS: Dict[str, Any] = {
    "shared_max_capacity": 15000,  # Unidades/mes de fabrica (cuello de botella)
    "skus": {
        "SKU-001": {
            "production_cost": 10.0,   # EUR/ud
            "holding_cost": 2.0,       # EUR/ud/mes
            "initial_inventory": 500.0,
            "safety_stock": 200.0
        },
        "SKU-002": {
            "production_cost": 50.0,   # Pieza especializada
            "holding_cost": 5.0,
            "initial_inventory": 20.0,
            "safety_stock": 5.0
        },
        "SKU-003": {
            "production_cost": 15.0,   # Producto estacional
            "holding_cost": 3.0,
            "initial_inventory": 300.0,
            "safety_stock": 100.0
        }
    }
}


class OptimizationManager:
    """
    Orquestador de optimizacion Multi-SKU.

    Flujo:
        1. Descarga forecast diario de 3 SKUs desde Supabase.
        2. Agrega a periodos mensuales (MS) por SKU.
        3. Ejecuta UnifiedSupplyOptimizer (LP compartido).
        4. Sube plan optimo a Supabase.

    Example:
        >>> manager = OptimizationManager()
        >>> result = manager.run_pipeline()
    """

    def __init__(self) -> None:
        """Inicializa con credenciales Supabase."""
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
        print(f"[OK] Fecha de ejecucion (snapshot): {self.execution_date}")

    def fetch_latest_forecast(self) -> pd.DataFrame:
        """
        Descarga el ultimo forecast de los 3 SKUs.

        Identifica la ejecucion mas reciente y descarga todos
        los registros de esa fecha.

        Returns:
            DataFrame con columnas [ds, sku, yhat, yhat_lower, yhat_upper].

        Raises:
            RuntimeError: Si no hay datos.
        """
        # Obtener la fecha de ejecucion mas reciente
        latest = (
            self.supabase
            .table(SOURCE_TABLE)
            .select("execution_date")
            .order("execution_date", desc=True)
            .limit(1)
            .execute()
        )

        if not latest.data:
            raise RuntimeError(
                f"No hay datos en '{SOURCE_TABLE}'. "
                "Ejecuta forecast_manager_v2.py primero."
            )

        exec_date: str = latest.data[0]["execution_date"]

        # Descargar todo el forecast de esa ejecucion
        response = (
            self.supabase
            .table(SOURCE_TABLE)
            .select("ds, sku, yhat, yhat_lower, yhat_upper")
            .eq("execution_date", exec_date)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                f"No se encontraron registros para execution_date={exec_date}"
            )

        df: pd.DataFrame = pd.DataFrame(response.data)
        df["ds"] = pd.to_datetime(df["ds"])

        skus_found: List[str] = sorted(df["sku"].unique().tolist())
        print(f"      Forecast del {exec_date}: {len(df):,} dias")
        print(f"      SKUs encontrados: {skus_found}")

        return df

    def _aggregate_monthly(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrega forecast diario a bloques mensuales por SKU.

        Args:
            df: Forecast diario con columnas [ds, sku, yhat].

        Returns:
            DataFrame mensual con columnas [ds, sku, yhat].
        """
        df["month"] = df["ds"].dt.to_period("M")

        monthly: pd.DataFrame = (
            df.groupby(["month", "sku"])
            .agg({"yhat": "sum"})
            .reset_index()
        )

        # Convertir period a timestamp (primer dia del mes)
        monthly["ds"] = monthly["month"].dt.to_timestamp()
        monthly = monthly.drop(columns=["month"])

        # Redondear
        monthly["yhat"] = monthly["yhat"].round(0).astype(int)

        print(f"      Agregado a {monthly['ds'].nunique()} periodos mensuales")

        return monthly[["ds", "sku", "yhat"]]

    def run_pipeline(
        self,
        params: Optional[Dict[str, Any]] = None,
        upload: bool = True
    ) -> Dict[str, Any]:
        """
        Pipeline completo: forecast -> agregacion -> optimizacion -> upload.

        Args:
            params: Parametros de optimizacion (default: OPTIMIZATION_PARAMS).
            upload: Si True, sube a Supabase.

        Returns:
            Diccionario con metricas del pipeline.
        """
        if params is None:
            params = OPTIMIZATION_PARAMS

        result: Dict[str, Any] = {
            "success": False,
            "skus_optimized": 0,
            "periods_planned": 0,
            "total_cost": 0,
            "records_uploaded": 0,
            "error": None
        }

        try:
            print("\n" + "=" * 60)
            print("  S&OP SUPPLY OPTIMIZATION v2 (Unified Multi-SKU)")
            print("=" * 60)

            # 1. Descargar forecast
            print(f"\n[1/4] Descargando ultimo forecast de Supabase...")
            daily_forecast: pd.DataFrame = self.fetch_latest_forecast()

            # 2. Agregar a mensual
            print(f"\n[2/4] Agregando a periodos mensuales por SKU...")
            monthly_forecast: pd.DataFrame = self._aggregate_monthly(
                daily_forecast
            )

            # Demanda por SKU
            for sku in sorted(monthly_forecast["sku"].unique()):
                sku_demand = monthly_forecast[
                    monthly_forecast["sku"] == sku
                ]["yhat"].sum()
                print(f"      {sku}: demanda total = {sku_demand:,} uds")

            # 3. Optimizar
            print(f"\n[3/4] Ejecutando optimizador unificado...")
            optimizer = UnifiedSupplyOptimizer(monthly_forecast, params)
            plan: pd.DataFrame = optimizer.optimize()
            optimizer.print_financial_summary()

            result["skus_optimized"] = len(plan["sku"].unique())
            result["periods_planned"] = plan["ds"].nunique() if "ds" in plan.columns else plan["plan_date"].nunique()

            summary = optimizer.get_financial_summary()
            result["total_cost"] = summary.get("total", {}).get(
                "total_cost", 0
            )

            # Preparar para upload
            plan["execution_date"] = self.execution_date.isoformat()
            plan["plan_date"] = pd.to_datetime(
                plan["plan_date"]
            ).dt.strftime("%Y-%m-%d")

            # Print plan completo
            self._print_plan(plan)

            # 4. Upload
            if upload:
                print(f"\n[4/4] Subiendo plan a Supabase ({TARGET_TABLE})...")
                uploaded: int = self._upload_plan(plan)
                result["records_uploaded"] = uploaded
                print(f"      {uploaded:,} registros insertados/actualizados")
            else:
                print(f"\n[4/4] [DRY-RUN] Plan NO subido a Supabase")

            result["success"] = True

            # Resumen ejecutivo
            print("\n" + "=" * 60)
            print("  PIPELINE COMPLETADO")
            print("=" * 60)
            print(f"\n  RESUMEN EJECUTIVO:")
            print(f"  - SKUs optimizados:    {result['skus_optimized']}")
            print(f"  - Periodos planeados:  {result['periods_planned']}")
            print(f"  - Registros subidos:   {result['records_uploaded']:,}")
            print(f"  - Coste total sistema: {result['total_cost']:,.2f} EUR")

        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            print(f"\n  ERROR: {result['error']}")

        return result

    def _print_plan(self, plan: pd.DataFrame) -> None:
        """Imprime el plan optimo por SKU."""
        print("\n" + "-" * 75)
        print("  SUPPLY PLAN (todos los periodos)")
        print("-" * 75)

        display_cols = [
            "plan_date", "sku", "demand_forecast",
            "production_qty", "inventory_level", "safety_stock_target"
        ]
        available = [c for c in display_cols if c in plan.columns]
        print(plan[available].to_string(index=False))
        print("-" * 75)

    def _upload_plan(self, plan_df: pd.DataFrame) -> int:
        """
        Sube plan a Supabase via batch upsert.

        Args:
            plan_df: DataFrame con plan + metadata.

        Returns:
            Registros procesados.
        """
        if plan_df.empty:
            return 0

        upload_cols = [
            "execution_date", "sku", "plan_date",
            "demand_forecast", "production_qty",
            "inventory_level", "safety_stock_target"
        ]
        available = [c for c in upload_cols if c in plan_df.columns]
        records = plan_df[available].to_dict(orient="records")

        batch_size: int = 500
        total: int = 0

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            self.supabase.table(TARGET_TABLE).upsert(
                batch, on_conflict="execution_date,sku,plan_date"
            ).execute()
            total += len(batch)

        return total


def main() -> None:
    """Punto de entrada."""
    print("\n" + "=" * 60)
    print("  S&OP OPTIMIZATION v2 - Execution Mode")
    print("=" * 60)

    try:
        manager = OptimizationManager()
        result = manager.run_pipeline(upload=True)

        if not result["success"]:
            print(f"\n  FALLO: {result['error']}")
            sys.exit(1)

    except (ValueError, ImportError) as e:
        print(f"\n  CONFIGURACION: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
