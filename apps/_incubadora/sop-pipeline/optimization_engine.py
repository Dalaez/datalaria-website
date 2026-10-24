"""
Supply Optimization Engine for S&OP Pipeline
==============================================
Motor de programación lineal para planificación de suministro.

Minimiza costes de producción y almacenamiento respetando
restricciones de inventario, Safety Stock y capacidad.

Author: Datalaria
Version: 1.0.0
"""

from typing import Dict, List, Any, Optional

import pandas as pd
import numpy as np
import pulp


class SupplyOptimizer:
    """
    Optimizador de suministro basado en Programación Lineal (PuLP).

    Dado un forecast de demanda, calcula el plan de producción óptimo
    que minimiza costes totales (producción + almacenamiento) respetando
    restricciones operativas.

    Attributes:
        forecast_df (pd.DataFrame): Demanda prevista por periodo.
        costs (Dict): Costes unitarios de producción y almacenamiento.
        constraints (Dict): Restricciones operativas.
        plan (pd.DataFrame): Plan óptimo generado.

    Example:
        >>> optimizer = SupplyOptimizer(forecast_df, costs, constraints)
        >>> plan = optimizer.optimize()
    """

    def __init__(
        self,
        forecast_df: pd.DataFrame,
        costs_dict: Dict[str, float],
        constraints_dict: Dict[str, float]
    ) -> None:
        """
        Inicializa el optimizador con datos y parámetros de negocio.

        Args:
            forecast_df: DataFrame con columnas ['ds', 'yhat'].
                        'ds' = fecha del periodo, 'yhat' = demanda prevista.
            costs_dict: Costes unitarios del negocio.
                - production_cost: Coste de producir/comprar 1 unidad (EUR).
                - holding_cost: Coste de almacenar 1 unidad por periodo (EUR).
            constraints_dict: Restricciones operativas.
                - initial_inventory: Stock disponible al inicio (unidades).
                - safety_stock_months: Meses de demanda a cubrir como Safety Stock.
                - max_warehouse_capacity: Capacidad máxima del almacén (unidades).
                - max_production_per_period: Producción máxima por periodo (unidades).

        Raises:
            ValueError: Si el DataFrame no tiene las columnas requeridas.
        """
        required_cols = {"ds", "yhat"}
        missing = required_cols - set(forecast_df.columns)
        if missing:
            raise ValueError(
                f"Columnas requeridas no encontradas: {missing}. "
                f"Columnas disponibles: {list(forecast_df.columns)}"
            )

        self.forecast_df: pd.DataFrame = forecast_df.copy().sort_values("ds").reset_index(drop=True)
        self.costs: Dict[str, float] = costs_dict
        self.constraints: Dict[str, float] = constraints_dict
        self.plan: Optional[pd.DataFrame] = None

        # Extraer demanda como lista
        self._demand: List[float] = self.forecast_df["yhat"].tolist()
        self._periods: int = len(self._demand)

        # Calcular Safety Stock por periodo (basado en media de demanda)
        avg_demand = np.mean(self._demand) if self._demand else 0
        ss_months = self.constraints.get("safety_stock_months", 1.5)
        self._safety_stock: float = avg_demand * ss_months

        print(f"   SupplyOptimizer inicializado:")
        print(f"     Periodos a planificar: {self._periods}")
        print(f"     Demanda total prevista: {sum(self._demand):,.0f} uds")
        print(f"     Safety Stock target: {self._safety_stock:,.0f} uds/periodo")
        print(f"     Coste produccion: {self.costs['production_cost']} EUR/ud")
        print(f"     Coste almacenamiento: {self.costs['holding_cost']} EUR/ud/periodo")

    def optimize(self) -> pd.DataFrame:
        """
        Resuelve el problema de optimización lineal.

        Modelo Matemático:
            Minimizar: SUM(production_cost * Prod_t + holding_cost * Inv_t)

            Sujeto a:
            - Balance de inventario: Inv_t = Inv_{t-1} + Prod_t - Demand_t
            - Safety Stock: Inv_t >= SafetyStock_t (para todo t)
            - Capacidad almacén: Inv_t <= MaxCapacity (para todo t)
            - Producción máxima: Prod_t <= MaxProduction (para todo t)
            - No negatividad: Prod_t >= 0, Inv_t >= 0

        Returns:
            DataFrame con plan óptimo:
            [plan_date, demand_forecast, production_qty,
             inventory_level, safety_stock_target]

        Raises:
            RuntimeError: Si el solver no encuentra solución óptima.
        """
        print("\n   Construyendo modelo de programación lineal...")

        # Extraer parámetros
        prod_cost = self.costs["production_cost"]
        hold_cost = self.costs["holding_cost"]
        initial_inv = self.constraints.get("initial_inventory", 0)
        max_capacity = self.constraints.get("max_warehouse_capacity", float("inf"))
        max_prod = self.constraints.get("max_production_per_period", float("inf"))

        T = self._periods

        # ─── Definir problema ───────────────────────────────
        problem = pulp.LpProblem("S&OP_Supply_Plan", pulp.LpMinimize)

        # ─── Variables de decisión ──────────────────────────
        production = [
            pulp.LpVariable(f"prod_{t}", lowBound=0, upBound=max_prod)
            for t in range(T)
        ]
        inventory = [
            pulp.LpVariable(f"inv_{t}", lowBound=0, upBound=max_capacity)
            for t in range(T)
        ]

        # ─── Función objetivo ──────────────────────────────
        # Minimizar coste total = producción + almacenamiento
        problem += pulp.lpSum(
            prod_cost * production[t] + hold_cost * inventory[t]
            for t in range(T)
        ), "Total_Cost"

        # ─── Restricciones ─────────────────────────────────

        # 1. Balance de inventario: Inv_t = Inv_{t-1} + Prod_t - Demand_t
        for t in range(T):
            prev_inv = initial_inv if t == 0 else inventory[t - 1]
            problem += (
                inventory[t] == prev_inv + production[t] - self._demand[t],
                f"Balance_t{t}"
            )

        # 2. Safety Stock: Inv_t >= SafetyStock
        for t in range(T):
            problem += (
                inventory[t] >= self._safety_stock,
                f"SafetyStock_t{t}"
            )

        # ─── Resolver ──────────────────────────────────────
        print("   Ejecutando solver...")
        solver = pulp.PULP_CBC_CMD(msg=0)  # Silenciar output del solver
        problem.solve(solver)

        # ─── Validar resultado ─────────────────────────────
        status = pulp.LpStatus[problem.status]
        if status != "Optimal":
            raise RuntimeError(
                f"El solver no encontro solucion optima. "
                f"Estado: {status}. "
                f"Revisa las restricciones (capacidad, Safety Stock)."
            )

        total_cost = pulp.value(problem.objective)
        print(f"   Solucion encontrada: OPTIMA")
        print(f"   Coste total del plan: {total_cost:,.2f} EUR")

        # ─── Construir DataFrame resultado ─────────────────
        plan_data = {
            "plan_date": self.forecast_df["ds"].tolist(),
            "demand_forecast": self._demand,
            "production_qty": [production[t].varValue for t in range(T)],
            "inventory_level": [inventory[t].varValue for t in range(T)],
            "safety_stock_target": [self._safety_stock] * T
        }

        self.plan = pd.DataFrame(plan_data)

        # Redondear a enteros (unidades)
        for col in ["production_qty", "inventory_level", "safety_stock_target"]:
            self.plan[col] = self.plan[col].round(0).astype(int)

        return self.plan.copy()

    def get_financial_summary(self) -> Dict[str, Any]:
        """
        Retorna resumen financiero del plan optimizado.

        Returns:
            Diccionario con métricas financieras del plan.

        Raises:
            RuntimeError: Si no se ha ejecutado optimize().
        """
        if self.plan is None:
            raise RuntimeError("Ejecuta optimize() primero.")

        prod_cost = self.costs["production_cost"]
        hold_cost = self.costs["holding_cost"]

        total_production = self.plan["production_qty"].sum()
        total_inventory_cost = (self.plan["inventory_level"] * hold_cost).sum()
        total_production_cost = total_production * prod_cost
        total_cost = total_production_cost + total_inventory_cost

        return {
            "total_periods": len(self.plan),
            "total_demand": int(self.plan["demand_forecast"].sum()),
            "total_production": int(total_production),
            "avg_inventory": int(self.plan["inventory_level"].mean()),
            "max_inventory": int(self.plan["inventory_level"].max()),
            "production_cost_eur": round(total_production_cost, 2),
            "holding_cost_eur": round(total_inventory_cost, 2),
            "total_cost_eur": round(total_cost, 2)
        }


if __name__ == "__main__":
    # Demo con datos sintéticos
    print("\n=== SupplyOptimizer - Demo ===\n")

    # Simular forecast de 12 meses
    dates = pd.date_range("2025-01-01", periods=12, freq="MS")
    np.random.seed(42)
    demand = 100 + 20 * np.sin(np.arange(12) * 2 * np.pi / 12) + np.random.normal(0, 5, 12)

    demo_forecast = pd.DataFrame({
        "ds": dates,
        "yhat": demand.astype(int)
    })

    costs = {"production_cost": 10.0, "holding_cost": 1.5}
    constraints = {
        "initial_inventory": 100,
        "safety_stock_months": 1.5,
        "max_warehouse_capacity": 5000,
        "max_production_per_period": 500
    }

    optimizer = SupplyOptimizer(demo_forecast, costs, constraints)
    plan = optimizer.optimize()
    summary = optimizer.get_financial_summary()

    print(f"\n   Plan (primeros 6 meses):")
    print(plan.head(6).to_string(index=False))

    print(f"\n   Resumen financiero:")
    for k, v in summary.items():
        print(f"     {k}: {v}")
