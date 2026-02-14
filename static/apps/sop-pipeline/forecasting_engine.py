"""
Forecasting Engine Module for S&OP Pipeline
=============================================
Motor de predicción probabilística de demanda usando Facebook Prophet.

Lee datos históricos limpios, los agrega temporalmente y genera
predicciones con intervalos de confianza para planificación S&OP.

Author: Datalaria
Version: 1.0.0
"""

from typing import Optional

import pandas as pd
import numpy as np
from prophet import Prophet


class ProphetPredictor:
    """
    Motor de predicción de demanda basado en Facebook Prophet.

    Transforma datos transaccionales en series temporales agregadas,
    entrena un modelo aditivo y genera forecasts probabilísticos.

    Attributes:
        df (pd.DataFrame): Datos de entrada (transaccionales).
        ts_df (pd.DataFrame): Serie temporal agregada (ds, y).
        model (Prophet): Modelo Prophet entrenado.
        forecast (pd.DataFrame): Predicciones generadas.

    Example:
        >>> predictor = ProphetPredictor(clean_df)
        >>> predictor.preprocess_daily_aggregation()
        >>> predictor.train_model(country_code='ES')
        >>> forecast = predictor.generate_forecast(months=12)
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Inicializa el predictor y valida estructura del DataFrame.

        Args:
            dataframe: DataFrame con datos de ventas limpios.
                      Debe contener columnas 'date' y 'qty'.

        Raises:
            ValueError: Si faltan columnas requeridas.
        """
        required_columns = {"date", "qty"}
        missing = required_columns - set(dataframe.columns)
        if missing:
            raise ValueError(
                f"Columnas requeridas no encontradas: {missing}. "
                f"Columnas disponibles: {list(dataframe.columns)}"
            )

        self.df: pd.DataFrame = dataframe.copy()
        self.ts_df: Optional[pd.DataFrame] = None
        self.model: Optional[Prophet] = None
        self.forecast: Optional[pd.DataFrame] = None

        # Asegurar que 'date' es datetime
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df = self.df.dropna(subset=["date"])

        print(f"   ProphetPredictor inicializado con {len(self.df):,} registros")

    def preprocess_daily_aggregation(self) -> "ProphetPredictor":
        """
        Agrega datos transaccionales a nivel diario.

        Los datos brutos son transacciones individuales. Prophet
        necesita una serie temporal (fecha, valor). Agrupamos por
        día y sumamos las cantidades.

        Returns:
            Self para method chaining.

        Note:
            Las columnas se renombran a 'ds' y 'y' (requisito Prophet).
        """
        # Agrupar por día: suma vectorizada de qty
        daily = (
            self.df
            .groupby(self.df["date"].dt.date)["qty"]
            .sum()
            .reset_index()
        )
        daily.columns = ["ds", "y"]
        daily["ds"] = pd.to_datetime(daily["ds"])

        # Ordenar cronológicamente
        daily = daily.sort_values("ds").reset_index(drop=True)

        # Detectar y reportar gaps
        date_range = pd.date_range(
            start=daily["ds"].min(),
            end=daily["ds"].max(),
            freq="D"
        )
        missing_days = len(date_range) - len(daily)

        self.ts_df = daily

        print(f"   Series temporal: {len(daily)} días")
        print(f"   Rango: {daily['ds'].min().date()} → {daily['ds'].max().date()}")
        if missing_days > 0:
            print(f"   Gaps detectados: {missing_days} días sin datos (Prophet los maneja)")

        return self

    def train_model(self, country_code: str = "ES") -> "ProphetPredictor":
        """
        Entrena el modelo Prophet con datos agregados.

        Configura Prophet con:
            - interval_width=0.95 (intervalo de confianza del 95%)
            - Festivos nacionales del país especificado
            - Estacionalidad automática

        Args:
            country_code: Código ISO del país para festivos (default: 'ES').

        Returns:
            Self para method chaining.

        Raises:
            RuntimeError: Si no se ha ejecutado preprocess_daily_aggregation().
        """
        if self.ts_df is None:
            raise RuntimeError(
                "Ejecuta preprocess_daily_aggregation() antes de entrenar."
            )

        if len(self.ts_df) < 2:
            raise ValueError(
                f"Datos insuficientes para entrenar: {len(self.ts_df)} puntos. "
                "Se necesitan al menos 2 observaciones."
            )

        # Configurar Prophet
        self.model = Prophet(
            interval_width=0.95,
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True
        )

        # Añadir festivos del país
        self.model.add_country_holidays(country_name=country_code)

        # Entrenar (suprime logs de Stan/cmdstanpy)
        self.model.fit(self.ts_df)

        print(f"   Modelo entrenado con {len(self.ts_df)} data points")
        print(f"   Festivos: {country_code}")
        print(f"   Intervalo de confianza: 95%")

        return self

    def generate_forecast(self, months: int = 12) -> pd.DataFrame:
        """
        Genera forecast probabilístico a N meses vista.

        Args:
            months: Horizonte de predicción en meses (default: 12).

        Returns:
            DataFrame con columnas [ds, yhat, yhat_lower, yhat_upper].

        Raises:
            RuntimeError: Si el modelo no ha sido entrenado.
        """
        if self.model is None:
            raise RuntimeError(
                "Ejecuta train_model() antes de generar predicciones."
            )

        # Crear dataframe futuro
        future_days = months * 30  # Aproximación
        future = self.model.make_future_dataframe(
            periods=future_days,
            freq="D"
        )

        # Predecir
        raw_forecast = self.model.predict(future)

        # Extraer solo columnas relevantes y futuro
        last_historical_date = self.ts_df["ds"].max()
        forecast_only = raw_forecast[raw_forecast["ds"] > last_historical_date].copy()

        # Limpiar: solo columnas útiles para S&OP
        self.forecast = forecast_only[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()

        # Asegurar que las predicciones no sean negativas (demanda ≥ 0)
        self.forecast["yhat"] = self.forecast["yhat"].clip(lower=0)
        self.forecast["yhat_lower"] = self.forecast["yhat_lower"].clip(lower=0)
        self.forecast["yhat_upper"] = self.forecast["yhat_upper"].clip(lower=0)

        # Redondear a enteros (unidades de demanda)
        for col in ["yhat", "yhat_lower", "yhat_upper"]:
            self.forecast[col] = self.forecast[col].round(0).astype(int)

        print(f"   Forecast generado: {len(self.forecast)} días")
        print(f"   Horizonte: {self.forecast['ds'].min().date()} → {self.forecast['ds'].max().date()}")

        return self.forecast.copy()


if __name__ == "__main__":
    # Demo con datos sintéticos
    print("\n=== ProphetPredictor - Demo ===\n")

    dates = pd.date_range("2024-01-01", periods=365, freq="D")
    np.random.seed(42)
    qty = (100 + 20 * np.sin(np.arange(365) * 2 * np.pi / 365)
           + np.random.normal(0, 10, 365))

    demo_df = pd.DataFrame({"date": dates, "qty": qty})

    predictor = ProphetPredictor(demo_df)
    predictor.preprocess_daily_aggregation()
    predictor.train_model(country_code="ES")
    forecast = predictor.generate_forecast(months=3)

    print(f"\n   Preview (primeros 5 días):")
    print(forecast.head().to_string(index=False))
