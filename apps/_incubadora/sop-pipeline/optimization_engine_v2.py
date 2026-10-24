"""
Unified Supply Optimizer v2 - Multi-SKU Shared Capacity
========================================================
Motor de Programacion Lineal que optimiza simultaneamente
N productos que compiten por una capacidad de fabrica
compartida.

CAMBIO CLAVE vs v1: Un unico modelo LP donde TODOS los SKUs
comparten la restriccion de capacidad mensual. El solver
decide como repartir la fabrica entre productos minimizando
el coste total del sistema completo.

Author: Datalaria
Version: 2.0.0
"""

from typing import Dict, Any, List

import pandas as pd
import numpy as np
import pulp


class UnifiedSupplyOptimizer:
    """
    Optimizador de supply planning multi-SKU con capacidad compartida.

    Construye un unico modelo de Programacion Lineal donde N productos
    compiten por una capacidad de produccion mensual limitada. El solver
    minimiza el coste total (produccion + almacenamiento) del sistema.

    Attributes:
        forecast_df (pd.DataFrame): Forecast mensual multi-SKU.
        params (Dict): Parametros por SKU y globales.
        skus (List[str]): Lista de SKUs detectados.
        periods (List): Fechas de los periodos.
        plan (pd.DataFrame): Plan optimo resultante.

    Example:
        >>> optimizer = UnifiedSupplyOptimizer(forecast_df, params)
        >>> plan = optimizer.optimize()
        >>> summary = optimizer.get_financial_summary()
    """

    def __init__(
        self,
        forecast_df: pd.DataFrame,
        params_dict: Dict[str, Any]
    ) -> None:
        """
        Inicializa el optimizador unificado.

        Args:
            forecast_df: DataFrame con columnas [ds, sku, yhat].
                         'ds' debe ser el primer dia de cada mes.
            params_dict: Diccionario con estructura:
                {
                    "shared_max_capacity": 600,
                    "skus": {
                        "SKU-001": {
                            "production_cost": 10,
                            "holding_cost": 2,
                            "initial_inventory": 100,
                            "safety_stock": 50
                        },
                        ...
                    }
                }

        Raises:
            ValueError: Si faltan columnas o parametros.
        """
        # Validar DataFrame
        required_cols: set = {"ds", "sku", "yhat"}
        missing: set = required_cols - set(forecast_df.columns)
        if missing:
            raise ValueError(f"Columnas faltantes en forecast: {missing}")

        self.forecast_df: pd.DataFrame = forecast_df.copy()
        self.params: Dict[str, Any] = params_dict
        self.plan: pd.DataFrame = pd.DataFrame()

        # Extraer SKUs y periodos
        self.skus: List[str] = sorted(forecast_df["sku"].unique().tolist())
        self.periods: List = sorted(forecast_df["ds"].unique().tolist())
        self.T: int = len(self.periods)

        # Capacidad compartida
        self.shared_capacity: float = params_dict.get(
            "shared_max_capacity", 600
        )

        # Construir diccionario de demanda: demand[sku][t] = valor
        # Pivot para alinear todos los SKUs al mismo grid de periodos
        # (si un SKU no tiene demanda en un mes, se rellena con 0)
        self._demand: Dict[str, List[float]] = {}
        for sku in self.skus:
            sku_data = (
                forecast_df[forecast_df["sku"] == sku]
                .set_index("ds")["yhat"]
                .reindex(self.periods, fill_value=0)
            )
            self._demand[sku] = sku_data.tolist()

        # Log
        total_demand: float = sum(
            sum(d) for d in self._demand.values()
        )
        print(f"\n   UnifiedSupplyOptimizer inicializado:")
        print(f"     SKUs: {self.skus}")
        print(f"     Periodos: {self.T}")
        print(f"     Demanda total prevista: {total_demand:,.0f} uds")
        print(f"     Capacidad fabrica/mes: {self.shared_capacity:,.0f} uds")

        for sku in self.skus:
            sku_params = params_dict.get("skus", {}).get(sku, {})
            sku_demand = sum(self._demand[sku])
            print(
                f"     {sku}: demand={sku_demand:,.0f} | "
                f"prod_cost={sku_params.get('production_cost', 0)} | "
                f"hold_cost={sku_params.get('holding_cost', 0)} | "
                f"safety={sku_params.get('safety_stock', 0)}"
            )

    def optimize(self) -> pd.DataFrame:
        """
        Construye y resuelve el modelo LP unificado.

        Variables de decision (por SKU, por periodo):
            - production[sku][t]: Unidades a fabricar
            - inventory[sku][t]: Inventario al final del periodo

        Funcion objetivo:
            Minimizar SUM_sku SUM_t (prod_cost[sku] * Prod[sku][t]
                                    + hold_cost[sku] * Inv[sku][t])

        Restricciones:
            1. Balance de masas por SKU
            2. Safety Stock por SKU
            3. Capacidad compartida: SUM_sku Prod[sku][t] <= capacity

        Returns:
            DataFrame con el plan optimo consolidado.

        Raises:
            RuntimeError: Si el solver no encuentra solucion optima.
        """
        print(f"\n   Construyendo modelo de Programacion Lineal unificado...")

        sku_params: Dict[str, Dict[str, float]] = self.params.get("skus", {})

        # ── Crear problema ──
        problem = pulp.LpProblem(
            "SOP_Unified_Supply_Plan", pulp.LpMinimize
        )

        # ── Variables de decision ──
        # production[sku][t] y inventory[sku][t]
        production: Dict[str, List[pulp.LpVariable]] = {}
        inventory: Dict[str, List[pulp.LpVariable]] = {}

        for sku in self.skus:
            production[sku] = [
                pulp.LpVariable(
                    f"prod_{sku}_{t}", lowBound=0, cat="Continuous"
                )
                for t in range(self.T)
            ]
            sp = sku_params.get(sku, {})
            max_inv = self.shared_capacity * 3  # Tope fisico razonable
            inventory[sku] = [
                pulp.LpVariable(
                    f"inv_{sku}_{t}", lowBound=0,
                    upBound=max_inv, cat="Continuous"
                )
                for t in range(self.T)
            ]

        # ── Funcion Objetivo ──
        total_cost = []
        for sku in self.skus:
            sp = sku_params.get(sku, {})
            prod_cost: float = sp.get("production_cost", 10)
            hold_cost: float = sp.get("holding_cost", 2)

            for t in range(self.T):
                total_cost.append(prod_cost * production[sku][t])
                total_cost.append(hold_cost * inventory[sku][t])

        problem += pulp.lpSum(total_cost), "Total_System_Cost"

        # ── Restricciones por SKU ──
        for sku in self.skus:
            sp = sku_params.get(sku, {})
            init_inv: float = sp.get("initial_inventory", 0)
            safety: float = sp.get("safety_stock", 0)
            demand: List[float] = self._demand[sku]

            for t in range(self.T):
                # 1. Balance de masas
                prev_inv = init_inv if t == 0 else inventory[sku][t - 1]
                problem += (
                    inventory[sku][t] == prev_inv + production[sku][t] - demand[t],
                    f"Balance_{sku}_t{t}"
                )

                # 2. Safety Stock
                problem += (
                    inventory[sku][t] >= safety,
                    f"SafetyStock_{sku}_t{t}"
                )

        # ── Restriccion Compartida: Capacidad de Fabrica ──
        for t in range(self.T):
            problem += (
                pulp.lpSum(
                    production[sku][t] for sku in self.skus
                ) <= self.shared_capacity,
                f"SharedCapacity_t{t}"
            )

        # ── Resolver ──
        print(f"   Ejecutando solver...")
        solver = pulp.PULP_CBC_CMD(msg=0)
        problem.solve(solver)

        status: str = pulp.LpStatus[problem.status]
        print(f"   Solucion encontrada: {status.upper()}")

        if problem.status != pulp.constants.LpStatusOptimal:
            raise RuntimeError(
                f"El solver no encontro solucion optima. "
                f"Estado: {status}. Revisa restricciones y capacidad."
            )

        optimal_cost: float = pulp.value(problem.objective)
        print(f"   Coste total del sistema: {optimal_cost:,.2f} EUR")

        # ── Extraer resultados ──
        rows: List[Dict[str, Any]] = []
        for sku in self.skus:
            sp = sku_params.get(sku, {})
            safety: float = sp.get("safety_stock", 0)

            for t in range(self.T):
                rows.append({
                    "plan_date": self.periods[t],
                    "sku": sku,
                    "demand_forecast": self._demand[sku][t],
                    "production_qty": production[sku][t].varValue,
                    "inventory_level": inventory[sku][t].varValue,
                    "safety_stock_target": safety
                })

        self.plan = pd.DataFrame(rows)

        # Limpiar ruido numerico del solver (ej: 9.9e-13 → 0)
        for col in ["production_qty", "inventory_level"]:
            self.plan[col] = self.plan[col].round(0).astype(int)
            self.plan[col] = self.plan[col].clip(lower=0)

        return self.plan.copy()

    def get_financial_summary(self) -> Dict[str, Any]:
        """
        Calcula resumen financiero del plan optimizado.

        Returns:
            Diccionario con metricas globales y por SKU.
        """
        if self.plan.empty:
            return {}

        sku_params: Dict[str, Dict[str, float]] = self.params.get("skus", {})
        summary: Dict[str, Any] = {
            "total": {},
            "per_sku": {}
        }

        grand_prod_cost: float = 0
        grand_hold_cost: float = 0

        for sku in self.skus:
            sp = sku_params.get(sku, {})
            prod_cost: float = sp.get("production_cost", 10)
            hold_cost: float = sp.get("holding_cost", 2)

            sku_plan = self.plan[self.plan["sku"] == sku]
            total_prod: float = sku_plan["production_qty"].sum()
            total_demand: float = sku_plan["demand_forecast"].sum()
            avg_inv: float = sku_plan["inventory_level"].mean()
            max_inv: float = sku_plan["inventory_level"].max()

            sku_prod_cost: float = total_prod * prod_cost
            sku_hold_cost: float = sku_plan["inventory_level"].sum() * hold_cost

            grand_prod_cost += sku_prod_cost
            grand_hold_cost += sku_hold_cost

            summary["per_sku"][sku] = {
                "demand_total": total_demand,
                "production_total": total_prod,
                "avg_inventory": avg_inv,
                "max_inventory": max_inv,
                "production_cost": sku_prod_cost,
                "holding_cost": sku_hold_cost,
                "total_cost": sku_prod_cost + sku_hold_cost
            }

        summary["total"] = {
            "production_cost": grand_prod_cost,
            "holding_cost": grand_hold_cost,
            "total_cost": grand_prod_cost + grand_hold_cost,
            "skus_planned": len(self.skus),
            "periods_planned": self.T
        }

        return summary

    def print_financial_summary(self) -> None:
        """Imprime resumen financiero formateado."""
        s = self.get_financial_summary()
        if not s:
            return

        total = s["total"]

        print("\n" + "-" * 60)
        print("  RESUMEN FINANCIERO DEL SISTEMA")
        print("-" * 60)

        for sku in self.skus:
            ps = s["per_sku"][sku]
            print(
                f"  {sku}: "
                f"demand={ps['demand_total']:,.0f} | "
                f"prod={ps['production_total']:,.0f} | "
                f"avg_inv={ps['avg_inventory']:,.0f} | "
                f"cost={ps['total_cost']:,.2f} EUR"
            )

        print("-" * 60)
        print(f"  Coste produccion total:      {total['production_cost']:>12,.2f} EUR")
        print(f"  Coste almacenamiento total:  {total['holding_cost']:>12,.2f} EUR")
        print(f"  ** COSTE TOTAL SISTEMA:      {total['total_cost']:>12,.2f} EUR **")
        print("-" * 60)


if __name__ == "__main__":
    print("\n=== UnifiedSupplyOptimizer - Demo ===\n")

    # Demo con 3 SKUs y 3 meses
    demo_forecast = pd.DataFrame({
        "ds": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-03-01"] * 3),
        "sku": ["SKU-A"] * 3 + ["SKU-B"] * 3 + ["SKU-C"] * 3,
        "yhat": [100, 120, 80, 10, 15, 5, 200, 250, 180]
    })

    demo_params = {
        "shared_max_capacity": 400,
        "skus": {
            "SKU-A": {"production_cost": 10, "holding_cost": 2,
                      "initial_inventory": 50, "safety_stock": 20},
            "SKU-B": {"production_cost": 50, "holding_cost": 5,
                      "initial_inventory": 10, "safety_stock": 3},
            "SKU-C": {"production_cost": 15, "holding_cost": 3,
                      "initial_inventory": 100, "safety_stock": 30}
        }
    }

    optimizer = UnifiedSupplyOptimizer(demo_forecast, demo_params)
    plan = optimizer.optimize()
    optimizer.print_financial_summary()
    print("\n   Plan:")
    print(plan.to_string(index=False))
