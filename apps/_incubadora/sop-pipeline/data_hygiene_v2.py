"""
Data Hygiene Engine v2 - Multi-SKU Support
============================================
Motor de limpieza estadística con detección de outliers
agrupada por producto (SKU).

CAMBIO CLAVE vs v1: El Z-Score se calcula POR SKU usando
groupby().transform(), no globalmente. Un pico de 500 uds
es normal para SKU-001 en Black Friday, pero es un outlier
para SKU-002 (repuestos).

Author: Datalaria
Version: 2.0.0
"""

from typing import Dict, Any, List

import pandas as pd
import numpy as np
from scipy import stats


class SupplyChainSanitizer:
    """
    Motor de limpieza de datos de supply chain con soporte Multi-SKU.

    Limpia datos transaccionales usando estadística vectorizada
    y detecta outliers de forma independiente por producto.

    Attributes:
        df (pd.DataFrame): Datos en proceso de limpieza.
        audit_log (Dict): Registro de métricas de limpieza.

    Example:
        >>> sanitizer = SupplyChainSanitizer(raw_df)
        >>> sanitizer.structural_clean().detect_outliers_zscore(threshold=3)
        >>> clean_df = sanitizer.get_clean_data()
        >>> report = sanitizer.get_audit_report()
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Inicializa el sanitizer con datos crudos.

        Args:
            dataframe: DataFrame con columnas mínimas ['date', 'sku', 'qty'].

        Raises:
            ValueError: Si faltan columnas requeridas.
        """
        required: set = {"date", "qty"}
        missing: set = required - set(dataframe.columns)
        if missing:
            raise ValueError(
                f"Columnas requeridas no encontradas: {missing}. "
                f"Disponibles: {list(dataframe.columns)}"
            )

        self.df: pd.DataFrame = dataframe.copy()
        self.audit_log: Dict[str, Any] = {
            "initial_rows": len(self.df),
            "skus_detected": [],
        }

    def structural_clean(self) -> "SupplyChainSanitizer":
        """
        Limpieza estructural vectorizada.

        Operaciones (en orden):
            1. Eliminar filas con SKU nulo o vacío.
            2. Convertir 'date' a datetime (errores → NaT).
            3. Convertir 'qty' a numérico (errores → NaN).
            4. Eliminar filas con NaN en columnas críticas (date, qty).
            5. Eliminar cantidades negativas (devoluciones mal registradas).
            6. Eliminar duplicados exactos.

        Returns:
            Self para method chaining.
        """
        # 1. SKU nulo o vacío
        if "sku" in self.df.columns:
            before: int = len(self.df)
            self.df["sku"] = self.df["sku"].astype(str).str.strip()
            self.df = self.df[
                (self.df["sku"].notna()) &
                (self.df["sku"] != "") &
                (self.df["sku"] != "nan") &
                (self.df["sku"] != "None")
            ]
            self.audit_log["null_sku_removed"] = before - len(self.df)

        # 2. Fechas
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        invalid_dates: int = self.df["date"].isna().sum()
        self.audit_log["invalid_dates"] = int(invalid_dates)

        # 3. Qty a numérico
        self.df["qty"] = pd.to_numeric(self.df["qty"], errors="coerce")

        # 4. Eliminar NaN críticos (date, qty)
        before = len(self.df)
        self.df = self.df.dropna(subset=["date", "qty"])
        self.audit_log["null_criticals_removed"] = before - len(self.df)

        # 5. Eliminar cantidades negativas
        before = len(self.df)
        self.df = self.df[self.df["qty"] >= 0]
        self.audit_log["negative_qty_removed"] = before - len(self.df)

        # 6. Duplicados exactos
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        self.audit_log["duplicates_removed"] = before - len(self.df)

        # SKUs detectados
        if "sku" in self.df.columns:
            self.audit_log["skus_detected"] = sorted(
                self.df["sku"].unique().tolist()
            )

        self.audit_log["rows_after_structural"] = len(self.df)

        return self

    def detect_outliers_zscore(self, threshold: float = 3.0) -> "SupplyChainSanitizer":
        """
        Detección de outliers usando Z-Score AGRUPADO por SKU.

        IMPORTANTE: Cada producto tiene su propia distribución.
        Calculamos media y std POR SKU usando groupby().transform()
        para mantener la vectorización completa (cero bucles).

        Si un SKU tiene std=0 (todas las cantidades iguales),
        el z-score se asigna como 0 (no es outlier).

        Args:
            threshold: Umbral de Z-Score (default: 3.0 = 99.7%).

        Returns:
            Self para method chaining.
        """
        if "sku" not in self.df.columns:
            # Fallback: Z-Score global (compatibilidad v1)
            z_scores = np.abs(stats.zscore(self.df["qty"], nan_policy="omit"))
            self.df["is_outlier"] = z_scores > threshold
        else:
            # Z-Score agrupado por SKU (vectorizado con transform)
            grouped_mean = self.df.groupby("sku")["qty"].transform("mean")
            grouped_std = self.df.groupby("sku")["qty"].transform("std")

            # Manejar std=0 (SKU con demanda constante → z_score = 0)
            grouped_std = grouped_std.replace(0, np.nan)

            z_scores = ((self.df["qty"] - grouped_mean) / grouped_std).abs()
            z_scores = z_scores.fillna(0)

            self.df["is_outlier"] = z_scores > threshold

        # Métricas de outliers
        total_outliers: int = int(self.df["is_outlier"].sum())
        self.audit_log["outliers_detected"] = total_outliers
        self.audit_log["outlier_percentage"] = round(
            total_outliers / len(self.df) * 100, 2
        ) if len(self.df) > 0 else 0.0

        # Reporte por SKU
        if "sku" in self.df.columns:
            sku_outliers: Dict[str, int] = (
                self.df[self.df["is_outlier"]]
                .groupby("sku")
                .size()
                .to_dict()
            )
            self.audit_log["outliers_per_sku"] = sku_outliers

        self.audit_log["final_rows"] = len(self.df)

        return self

    def get_clean_data(self) -> pd.DataFrame:
        """Retorna el DataFrame limpio (incluye outliers marcados)."""
        return self.df.copy()

    def get_audit_report(self) -> Dict[str, Any]:
        """Retorna el diccionario de métricas de auditoría."""
        return self.audit_log.copy()

    def print_audit_report(self) -> None:
        """Imprime el reporte de auditoría formateado."""
        r = self.audit_log
        print("\n" + "-" * 50)
        print("  AUDIT REPORT")
        print("-" * 50)
        print(f"  Filas iniciales:          {r.get('initial_rows', 0):,}")
        if r.get("null_sku_removed", 0) > 0:
            print(f"  SKUs nulos eliminados:    {r['null_sku_removed']}")
        print(f"  Fechas invalidas:         {r.get('invalid_dates', 0)}")
        print(f"  Nulos criticos:           {r.get('null_criticals_removed', 0)}")
        print(f"  Cantidades negativas:     {r.get('negative_qty_removed', 0)}")
        print(f"  Duplicados:               {r.get('duplicates_removed', 0)}")
        print(f"  Filas tras limpieza:      {r.get('rows_after_structural', 0):,}")
        print(f"  Outliers detectados:      {r.get('outliers_detected', 0)} "
              f"({r.get('outlier_percentage', 0)}%)")

        if r.get("outliers_per_sku"):
            print("  Outliers por SKU:")
            for sku, count in sorted(r["outliers_per_sku"].items()):
                print(f"    {sku}: {count}")

        print(f"  SKUs en dataset:          {r.get('skus_detected', [])}")
        print(f"  Filas finales:            {r.get('final_rows', 0):,}")
        print("-" * 50)


if __name__ == "__main__":
    # Demo con datos de prueba multi-SKU
    print("\n=== SupplyChainSanitizer v2 - Demo ===\n")

    demo_data = pd.DataFrame({
        "date": ["2024-01-01"] * 5 + ["bad_date", None],
        "sku": ["SKU-001", "SKU-001", "SKU-002", "SKU-002", "SKU-003", "SKU-001", ""],
        "qty": [100, 5000, 3, 2, 400, 50, 10]
    })

    sanitizer = SupplyChainSanitizer(demo_data)
    sanitizer.structural_clean().detect_outliers_zscore(threshold=3)
    sanitizer.print_audit_report()
