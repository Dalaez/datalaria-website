"""
Optimization Manager for S&OP Pipeline
========================================
Orquestador: Lee forecast → Optimiza suministro → Sube plan a Supabase.

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

from optimization_engine import SupplyOptimizer


# ─── Constantes ────────────────────────────────────────
SOURCE_TABLE = "demand_forecasts"
TARGET_TABLE = "supply_plans"


class OptimizationManager:
    """
    Orquestador del pipeline de optimización de suministro.

    Flujo completo:
        1. Descarga el último forecast de Supabase.
        2. Agrega la demanda diaria a periodos mensuales.
        3. Ejecuta el optimizador (PuLP).
        4. Sube el plan resulante a Supabase.

    Attributes:
        supabase (Client): Cliente Supabase.
        execution_date (date): Fecha de ejecución (snapshot).

    Example:
        >>> manager = OptimizationManager()
        >>> result = manager.run_pipeline()
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
        print(f"[OK] Fecha de ejecucion (snapshot): {self.execution_date}")

    def fetch_latest_forecast(self) -> pd.DataFrame:
        """
        Descarga el último forecast disponible de Supabase.

        Obtiene los registros más recientes (por execution_date)
        de la tabla demand_forecasts y los agrega a nivel mensual.

        Returns:
            DataFrame con columnas ['ds', 'yhat'] agregado mensualmente.

        Raises:
            RuntimeError: Si no hay forecasts disponibles.
        """
        print("\n[1/4] Descargando ultimo forecast de Supabase...")

        # Obtener el forecast más reciente ordenado por fecha
        response = (
            self.supabase
            .table(SOURCE_TABLE)
            .select("ds, yhat, execution_date")
            .order("execution_date", desc=True)
            .order("ds", desc=False)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                f"No se encontraron forecasts en '{SOURCE_TABLE}'. "
                "Ejecutaste el pipeline de forecasting (Part 2)?"
            )

        df = pd.DataFrame(response.data)

        # Filtrar solo el forecast más reciente
        latest_execution = df["execution_date"].max()
        df = df[df["execution_date"] == latest_execution].copy()
        print(f"      Forecast del {latest_execution}: {len(df)} dias")

        # Agregar a nivel mensual (sum de demanda diaria por mes)
        df["ds"] = pd.to_datetime(df["ds"])
        df["yhat"] = pd.to_numeric(df["yhat"])

        monthly = (
            df
            .groupby(df["ds"].dt.to_period("M"))
            .agg({"yhat": "sum", "ds": "first"})
            .reset_index(drop=True)
        )

        # Usar primer día del mes como referencia
        monthly["ds"] = monthly["ds"].dt.to_period("M").dt.to_timestamp()

        print(f"      Agregado a {len(monthly)} periodos mensuales")
        print(f"      Demanda total prevista: {monthly['yhat'].sum():,.0f} uds")

        return monthly[["ds", "yhat"]]

    def run_pipeline(
        self,
        costs: Optional[Dict[str, float]] = None,
        constraints: Optional[Dict[str, float]] = None,
        upload: bool = True
    ) -> Dict[str, Any]:
        """
        Ejecuta el pipeline completo de optimización.

        Args:
            costs: Costes unitarios. Default: producción=10, almacenamiento=1.5
            constraints: Restricciones operativas. Default: inv_inicial=100,
                        ss_months=1.5, max_warehouse=5000, max_prod=500
            upload: Si True, sube a Supabase. Si False, dry-run.

        Returns:
            Diccionario con estado, métricas y resumen financiero.
        """
        # Parámetros de negocio por defecto (simulados)
        if costs is None:
            costs = {
                "production_cost": 10.0,   # EUR/unidad
                "holding_cost": 1.5        # EUR/unidad/mes
            }
        if constraints is None:
            constraints = {
                "initial_inventory": 100,          # Unidades
                "safety_stock_months": 1.5,        # Meses de cobertura
                "max_warehouse_capacity": 5000,    # Unidades
                "max_production_per_period": 500   # Unidades/mes
            }

        result: Dict[str, Any] = {
            "success": False,
            "forecast_periods": 0,
            "plan_periods": 0,
            "records_uploaded": 0,
            "financial_summary": {},
            "error": None
        }

        try:
            print("\n" + "=" * 60)
            print("  S&OP SUPPLY OPTIMIZATION PIPELINE")
            print("=" * 60)

            # 1. Descargar forecast
            forecast_df = self.fetch_latest_forecast()
            result["forecast_periods"] = len(forecast_df)

            # 2. Ejecutar optimizador
            print("\n[2/4] Ejecutando optimizador...")
            optimizer = SupplyOptimizer(forecast_df, costs, constraints)
            plan = optimizer.optimize()
            result["plan_periods"] = len(plan)

            # 3. Resumen financiero
            financial = optimizer.get_financial_summary()
            result["financial_summary"] = financial

            print("\n[3/4] Resumen financiero:")
            self._print_financial_summary(financial)

            # Preview del plan
            print("\n" + "-" * 65)
            print("  SUPPLY PLAN (todos los periodos)")
            print("-" * 65)
            print(plan.to_string(index=False))
            print("-" * 65)

            # 4. Upload a Supabase
            if upload:
                print("\n[4/4] Subiendo plan a Supabase...")
                plan["execution_date"] = self.execution_date.isoformat()
                plan["plan_date"] = plan["plan_date"].astype(str)
                uploaded = self._upload_plan(plan)
                result["records_uploaded"] = uploaded
                print(f"      {uploaded} registros insertados/actualizados")
            else:
                print("\n[4/4] [DRY-RUN] Plan NO subido a Supabase")

            result["success"] = True
            print("\n" + "=" * 60)
            print("  PIPELINE COMPLETADO")
            print("=" * 60)

        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            print(f"\n  ERROR: {type(e).__name__}: {e}")

        return result

    def _print_financial_summary(self, summary: Dict[str, Any]) -> None:
        """Imprime resumen financiero formateado."""
        print("-" * 40)
        print(f"  Periodos planificados:   {summary['total_periods']}")
        print(f"  Demanda total:           {summary['total_demand']:,} uds")
        print(f"  Produccion total:        {summary['total_production']:,} uds")
        print(f"  Inventario promedio:     {summary['avg_inventory']:,} uds")
        print(f"  Inventario maximo:       {summary['max_inventory']:,} uds")
        print("-" * 40)
        print(f"  Coste produccion:        {summary['production_cost_eur']:,.2f} EUR")
        print(f"  Coste almacenamiento:    {summary['holding_cost_eur']:,.2f} EUR")
        print(f"  ** COSTE TOTAL PLAN:     {summary['total_cost_eur']:,.2f} EUR **")
        print("-" * 40)

    def _upload_plan(self, plan_df: pd.DataFrame) -> int:
        """
        Sube plan a la tabla supply_plans usando upsert.

        Args:
            plan_df: DataFrame con plan optimizado + metadata.

        Returns:
            Número de registros procesados.
        """
        if plan_df.empty:
            return 0

        records = plan_df.to_dict(orient="records")

        # Upsert por lotes
        batch_size = 500
        total_uploaded = 0

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            self.supabase.table(TARGET_TABLE).upsert(batch).execute()
            total_uploaded += len(batch)

        return total_uploaded


def main() -> None:
    """Punto de entrada para ejecucion local."""
    print("\n" + "=" * 60)
    print("  S&OP OPTIMIZATION - Execution Mode")
    print("=" * 60)

    # Parámetros de negocio (simulados)
    business_costs = {
        "production_cost": 10.0,   # EUR por unidad producida/comprada
        "holding_cost": 1.5        # EUR por unidad almacenada por mes
    }

    business_constraints = {
        "initial_inventory": 100,          # Stock actual disponible
        "safety_stock_months": 1.5,        # 1.5 meses de cobertura
        "max_warehouse_capacity": 5000,    # Capacidad máxima almacén
        "max_production_per_period": 500   # Producción máxima mensual
    }

    try:
        manager = OptimizationManager()
        result = manager.run_pipeline(
            costs=business_costs,
            constraints=business_constraints,
            upload=True
        )

        # Resumen final
        print("\n  RESUMEN EJECUTIVO:")
        print(f"  - Periodos de forecast:  {result['forecast_periods']}")
        print(f"  - Periodos planificados: {result['plan_periods']}")
        print(f"  - Registros subidos:     {result['records_uploaded']}")

        if result["financial_summary"]:
            print(f"  - Coste total del plan:  {result['financial_summary']['total_cost_eur']:,.2f} EUR")

        if not result["success"]:
            print(f"\n  FALLO: {result['error']}")
            sys.exit(1)

    except (ValueError, ImportError) as e:
        print(f"\n  CONFIGURACION: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
