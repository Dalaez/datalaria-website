"""
Forecasting Engine v2 - Multi-SKU Prophet Worker
==================================================
Motor de predicción probabilística con soporte por producto.

CAMBIO CLAVE vs v1: Cada instancia recibe el DataFrame de UN
solo SKU. El manager se encarga de la paralelización.
Prophet puede generar yhat < 0 en productos intermitentes;
generate_forecast() aplica negative clipping post-predicción.

Author: Datalaria
Version: 2.0.0
"""

import logging
import warnings
from typing import Optional

import pandas as pd
import numpy as np

# Silenciar logs de Prophet, cmdstanpy y Stan
logging.getLogger("prophet").setLevel(logging.WARNING)
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
logging.getLogger("prophet.plot").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*Optimization.*")

from prophet import Prophet


class ProphetPredictor:
    """
    Motor de predicción de demanda para un SKU individual.

    Transforma datos transaccionales en serie temporal diaria,
    entrena Prophet y genera forecast con negative clipping.

    Attributes:
        sku_name (str): Identificador del producto.
        df (pd.DataFrame): Datos de entrada.
        ts_df (pd.DataFrame): Serie temporal agregada (ds, y).
        model (Prophet): Modelo Prophet entrenado.
        forecast (pd.DataFrame): Predicciones generadas.

    Example:
        >>> predictor = ProphetPredictor(df_sku001, sku_name="SKU-001")
        >>> predictor.preprocess_daily_aggregation()
        >>> predictor.train_model(country_code='ES')
        >>> forecast = predictor.generate_forecast(months=12)
    """

    def __init__(self, dataframe: pd.DataFrame, sku_name: str) -> None:
        """
        Inicializa el predictor con datos de un SKU específico.

        Args:
            dataframe: DataFrame con columnas ['date', 'qty'].
            sku_name: Nombre/código del SKU (ej: 'SKU-001').

        Raises:
            ValueError: Si faltan columnas requeridas o datos vacíos.
        """
        required_columns: set = {"date", "qty"}
        missing: set = required_columns - set(dataframe.columns)
        if missing:
            raise ValueError(
                f"[{sku_name}] Columnas requeridas no encontradas: {missing}. "
                f"Disponibles: {list(dataframe.columns)}"
            )

        if dataframe.empty:
            raise ValueError(
                f"[{sku_name}] DataFrame vacío. No hay datos para entrenar."
            )

        self.sku_name: str = sku_name
        self.df: pd.DataFrame = dataframe.copy()
        self.ts_df: Optional[pd.DataFrame] = None
        self.model: Optional[Prophet] = None
        self.forecast: Optional[pd.DataFrame] = None

        # Asegurar datetime
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df = self.df.dropna(subset=["date"])

    def preprocess_daily_aggregation(self) -> "ProphetPredictor":
        """
        Agrega datos transaccionales a nivel diario.

        Las columnas se renombran a 'ds' y 'y' (requisito Prophet).

        Returns:
            Self para method chaining.
        """
        daily: pd.DataFrame = (
            self.df
            .groupby(self.df["date"].dt.date)["qty"]
            .sum()
            .reset_index()
        )
        daily.columns = ["ds", "y"]
        daily["ds"] = pd.to_datetime(daily["ds"])
        daily = daily.sort_values("ds").reset_index(drop=True)

        self.ts_df = daily
        return self

    def train_model(self, country_code: str = "ES") -> "ProphetPredictor":
        """
        Entrena el modelo Prophet.

        Args:
            country_code: Código ISO para festivos (default: 'ES').

        Returns:
            Self para method chaining.

        Raises:
            RuntimeError: Si no se ejecutó preprocess_daily_aggregation().
            ValueError: Si hay insuficientes datos.
        """
        if self.ts_df is None:
            raise RuntimeError(
                f"[{self.sku_name}] Ejecuta preprocess_daily_aggregation() "
                "antes de entrenar."
            )

        if len(self.ts_df) < 2:
            raise ValueError(
                f"[{self.sku_name}] Datos insuficientes: {len(self.ts_df)} "
                "puntos. Se necesitan al menos 2."
            )

        self.model = Prophet(
            interval_width=0.95,
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True
        )
        self.model.add_country_holidays(country_name=country_code)

        # Entrenar (logs de Stan silenciados globalmente)
        self.model.fit(self.ts_df)

        return self

    def generate_forecast(self, months: int = 12) -> pd.DataFrame:
        """
        Genera forecast probabilístico con negative clipping.

        BUSINESS RULE: Prophet puede generar yhat < 0 en productos
        de demanda intermitente (SKU-002). Cualquier valor negativo
        se convierte en 0 (la demanda no puede ser negativa).

        Args:
            months: Horizonte de predicción en meses.

        Returns:
            DataFrame con columnas [ds, sku, yhat, yhat_lower, yhat_upper].

        Raises:
            RuntimeError: Si el modelo no fue entrenado.
        """
        if self.model is None:
            raise RuntimeError(
                f"[{self.sku_name}] Ejecuta train_model() antes de predecir."
            )

        # Generar futuro
        future_days: int = months * 30
        future: pd.DataFrame = self.model.make_future_dataframe(
            periods=future_days, freq="D"
        )

        # Predecir
        raw_forecast: pd.DataFrame = self.model.predict(future)

        # Solo fechas futuras
        last_date = self.ts_df["ds"].max()
        forecast_only: pd.DataFrame = raw_forecast[
            raw_forecast["ds"] > last_date
        ].copy()

        # Extraer columnas S&OP
        self.forecast = forecast_only[
            ["ds", "yhat", "yhat_lower", "yhat_upper"]
        ].copy()

        # ── Negative Clipping (Business Rule) ──
        for col in ["yhat", "yhat_lower", "yhat_upper"]:
            self.forecast[col] = self.forecast[col].clip(lower=0).round(0).astype(int)

        # Añadir SKU
        self.forecast["sku"] = self.sku_name

        return self.forecast.copy()


if __name__ == "__main__":
    print("\n=== ProphetPredictor v2 - Demo ===\n")

    dates = pd.date_range("2024-01-01", periods=365, freq="D")
    np.random.seed(42)
    qty = (100 + 20 * np.sin(np.arange(365) * 2 * np.pi / 365)
           + np.random.normal(0, 10, 365))
    demo_df = pd.DataFrame({"date": dates, "qty": qty})

    predictor = ProphetPredictor(demo_df, sku_name="SKU-DEMO")
    predictor.preprocess_daily_aggregation()
    predictor.train_model(country_code="ES")
    forecast = predictor.generate_forecast(months=3)

    print(f"   SKU: {predictor.sku_name}")
    print(f"   Forecast: {len(forecast)} dias")
    print(f"   Min yhat: {forecast['yhat'].min()} (negatives clipped)")
    print(f"\n   Preview:")
    print(forecast.head().to_string(index=False))
