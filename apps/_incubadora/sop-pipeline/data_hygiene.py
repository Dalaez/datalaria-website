"""
Data Hygiene Module for S&OP Pipeline
=====================================
Módulo de limpieza estadística para datos de ventas en cadena de suministro.

Author: Datalaria
Version: 1.0.0
"""

from typing import Dict, Any
import pandas as pd
import numpy as np
from scipy import stats


class SupplyChainSanitizer:
    """
    Clase para limpieza y sanitización de datos de ventas.
    
    Implementa técnicas de limpieza vectorizada (sin bucles for)
    y detección de outliers mediante Z-Score.
    
    Attributes:
        df (pd.DataFrame): DataFrame en proceso de limpieza.
        _audit_log (Dict): Registro de auditoría con métricas.
    
    Example:
        >>> sanitizer = SupplyChainSanitizer(raw_df)
        >>> sanitizer.structural_clean()
        >>> sanitizer.detect_outliers_zscore(threshold=3)
        >>> clean_df = sanitizer.get_clean_data()
        >>> report = sanitizer.get_audit_report()
    """
    
    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Inicializa el sanitizador con un DataFrame.
        
        Args:
            dataframe: DataFrame de Pandas con datos de ventas raw.
                      Debe contener al menos columnas 'date' y 'qty'.
        """
        self.df: pd.DataFrame = dataframe.copy()
        self._initial_row_count: int = len(self.df)
        self._audit_log: Dict[str, Any] = {
            "initial_rows": self._initial_row_count,
            "rows_with_invalid_dates": 0,
            "rows_with_null_criticals": 0,
            "duplicate_rows_removed": 0,
            "final_rows": 0,
            "outliers_detected": 0,
            "outlier_percentage": 0.0
        }
    
    def structural_clean(self) -> "SupplyChainSanitizer":
        """
        Ejecuta limpieza estructural del DataFrame.
        
        Operaciones:
            1. Convierte columna 'date' a datetime (coerce errors).
            2. Convierte columna 'qty' a numérico.
            3. Elimina filas con NaNs en campos críticos (date, qty).
            4. Elimina filas duplicadas exactas.
        
        Returns:
            Self para permitir method chaining.
        
        Note:
            Todas las operaciones son vectorizadas (sin loops).
        """
        rows_before = len(self.df)
        
        # 1. Convertir 'date' a datetime (errores se convierten en NaT)
        self.df["date"] = pd.to_datetime(
            self.df["date"], 
            errors="coerce"
        )
        invalid_dates = self.df["date"].isna().sum()
        self._audit_log["rows_with_invalid_dates"] = int(invalid_dates)
        
        # 2. Convertir 'qty' a numérico (errores se convierten en NaN)
        self.df["qty"] = pd.to_numeric(self.df["qty"], errors="coerce")
        
        # 3. Eliminar filas con NaNs en campos críticos
        critical_columns = ["date", "qty"]
        null_mask = self.df[critical_columns].isna().any(axis=1)
        self._audit_log["rows_with_null_criticals"] = int(null_mask.sum())
        self.df = self.df.dropna(subset=critical_columns)
        
        # 4. Eliminar duplicados exactos
        rows_before_dedup = len(self.df)
        self.df = self.df.drop_duplicates()
        self._audit_log["duplicate_rows_removed"] = rows_before_dedup - len(self.df)
        
        self._audit_log["final_rows"] = len(self.df)
        
        return self
    
    def detect_outliers_zscore(self, threshold: float = 3.0) -> "SupplyChainSanitizer":
        """
        Detecta outliers en columna 'qty' usando Z-Score.
        
        El Z-Score mide cuántas desviaciones estándar un valor está
        alejado de la media. Valores con |Z| > threshold se marcan
        como outliers.
        
        Args:
            threshold: Umbral de Z-Score para detección (default: 3.0).
                      Valores típicos: 2.0 (más estricto) a 3.0 (estándar).
        
        Returns:
            Self para permitir method chaining.
        
        Note:
            NO elimina los outliers, solo los marca en columna 'is_outlier'.
            Esto permite revisión manual antes de exclusión.
        """
        if len(self.df) == 0:
            self.df["is_outlier"] = pd.Series(dtype=bool)
            return self
        
        # Calcular Z-Score vectorizado usando scipy.stats
        z_scores = np.abs(stats.zscore(self.df["qty"]))
        
        # Marcar outliers (NO eliminar)
        self.df["is_outlier"] = z_scores > threshold
        
        # Actualizar auditoría
        outlier_count = self.df["is_outlier"].sum()
        self._audit_log["outliers_detected"] = int(outlier_count)
        self._audit_log["outlier_percentage"] = round(
            (outlier_count / len(self.df)) * 100, 2
        ) if len(self.df) > 0 else 0.0
        
        return self
    
    def get_clean_data(self) -> pd.DataFrame:
        """
        Retorna el DataFrame procesado.
        
        Returns:
            DataFrame con datos limpios y columna 'is_outlier' si 
            se ejecutó detect_outliers_zscore().
        """
        return self.df.copy()
    
    def get_audit_report(self) -> Dict[str, Any]:
        """
        Retorna el reporte de auditoría del proceso de limpieza.
        
        Returns:
            Diccionario con métricas:
                - initial_rows: Filas iniciales
                - rows_with_invalid_dates: Filas con fechas inválidas
                - rows_with_null_criticals: Filas con NaNs críticos
                - duplicate_rows_removed: Duplicados eliminados
                - final_rows: Filas finales
                - outliers_detected: Número de outliers
                - outlier_percentage: Porcentaje de outliers
        """
        return self._audit_log.copy()


if __name__ == "__main__":
    # Demo rápida del módulo
    sample_data = pd.DataFrame({
        "date": ["2024-01-01", "invalid", "2024-01-03", "2024-01-01"],
        "qty": [100, 150, None, 100],
        "product": ["A", "B", "C", "A"]
    })
    
    sanitizer = SupplyChainSanitizer(sample_data)
    sanitizer.structural_clean().detect_outliers_zscore()
    
    print("=== Audit Report ===")
    for key, value in sanitizer.get_audit_report().items():
        print(f"  {key}: {value}")
    
    print("\n=== Clean Data ===")
    print(sanitizer.get_clean_data())
