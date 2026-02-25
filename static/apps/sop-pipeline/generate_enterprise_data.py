"""
Enterprise Data Generator for S&OP Pipeline
=============================================
Genera 3 años de datos de ventas (2023-2025) para 3 SKUs con
comportamientos realistas + ruido de ERP corporativo.

Author: Datalaria
Version: 2.0.0
"""

import time
from typing import Dict, List, Tuple

import pandas as pd
import numpy as np


class EnterpriseDataGenerator:
    """
    Generador de datasets empresariales para simulación S&OP.

    Simula 3 perfiles de demanda distintos y corrompe un 5%
    de las filas con errores realistas de ERP.

    Attributes:
        start_date (str): Fecha de inicio del histórico.
        end_date (str): Fecha de fin del histórico.
        dates (pd.DatetimeIndex): Rango completo de fechas.
        noise_ratio (float): Porcentaje de filas a corromper.

    Example:
        >>> gen = EnterpriseDataGenerator()
        >>> df = gen.generate_all()
        >>> gen.export_csv(df, "enterprise_sales_history.csv")
    """

    def __init__(
        self,
        start_date: str = "2023-01-01",
        end_date: str = "2025-12-31",
        noise_ratio: float = 0.05,
        seed: int = 42
    ) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.noise_ratio = noise_ratio
        self.dates = pd.date_range(start=start_date, end=end_date, freq="D")
        self.n_days = len(self.dates)
        np.random.seed(seed)

        print(f"   Rango: {start_date} -> {end_date} ({self.n_days} dias)")

    # ─── SKU Generators (Vectorized) ────────────────────

    def _generate_sku001_core(self) -> pd.DataFrame:
        """
        SKU-001: Core Product.
        Demanda estable alta (media ~200/dia) con ruido gaussiano.
        Multiplicador x3 durante la semana de Black Friday (Nov).
        """
        base_demand = 200 + np.random.normal(0, 30, self.n_days)

        # Black Friday: cuarta semana de noviembre (dias 22-28)
        months = self.dates.month
        days = self.dates.day
        is_black_friday = (months == 11) & (days >= 22) & (days <= 28)
        base_demand[is_black_friday] *= 3.0

        # Asegurar no negativos y redondear
        qty = np.maximum(base_demand, 1).astype(int)

        df = pd.DataFrame({
            "date": self.dates,
            "sku": "SKU-001",
            "qty": qty
        })

        bf_days = is_black_friday.sum()
        print(f"   SKU-001 (Core Product):      {len(df):,} rows | "
              f"avg={qty.mean():.0f}/dia | Black Friday boost: {bf_days} dias")
        return df

    def _generate_sku002_intermittent(self) -> pd.DataFrame:
        """
        SKU-002: Intermittent Spare Part (B2B).
        70% de los dias demanda=0, resto Poisson(lambda=2).
        Simula repuestos industriales o piezas bajo pedido.
        """
        # Mascara: 70% ceros
        has_demand = np.random.random(self.n_days) > 0.70

        # Poisson para los dias con demanda (lambda=2 -> picos entre 1-5)
        poisson_demand = np.random.poisson(lam=2, size=self.n_days)

        qty = np.where(has_demand, poisson_demand, 0)
        # Clamp minimo a 1 en dias con demanda
        qty = np.where((has_demand) & (qty < 1), 1, qty)

        df = pd.DataFrame({
            "date": self.dates,
            "sku": "SKU-002",
            "qty": qty
        })

        zero_pct = (qty == 0).sum() / len(qty) * 100
        print(f"   SKU-002 (Spare Part):        {len(df):,} rows | "
              f"zeros={zero_pct:.0f}% | avg(non-zero)="
              f"{qty[qty > 0].mean():.1f}/dia")
        return df

    def _generate_sku003_seasonal(self) -> pd.DataFrame:
        """
        SKU-003: Seasonal Summer Product.
        Onda senoidal: pico ~500/dia en Jul-Ago, ~0 en Dic-Feb.
        Simula helados, turismo, proteccion solar, etc.
        """
        # Dia del ano (0-364)
        day_of_year = self.dates.dayofyear

        # Onda senoidal ajustada: pico en dia ~200 (Jul), valle en ~20 (Ene)
        # sin(x) tiene pico en pi/2, asi que desplazamos
        seasonal_wave = np.sin((day_of_year - 80) * 2 * np.pi / 365)

        # Escalar: rango [-1, 1] -> [0, 500]
        qty = ((seasonal_wave + 1) / 2 * 500).astype(int)

        # Anadir ruido gaussiano (+/-15%)
        noise = np.random.normal(1.0, 0.15, self.n_days)
        qty = (qty * noise).astype(int)

        # Asegurar no negativos
        qty = np.maximum(qty, 0)

        df = pd.DataFrame({
            "date": self.dates,
            "sku": "SKU-003",
            "qty": qty
        })

        print(f"   SKU-003 (Seasonal Summer):   {len(df):,} rows | "
              f"max={qty.max()}/dia | min={qty.min()}/dia")
        return df

    # ─── Noise Injection (ERP Corruption) ───────────────

    def _inject_erp_noise(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Corrompe un porcentaje de filas simulando errores reales de ERP.

        Tipos de corrupccion:
            - 30% Outliers (fat finger x50)
            - 25% Nulos en qty
            - 20% Fechas invalidas (formatos rotos)
            - 15% Nulos en date
            - 10% Cantidades negativas (devoluciones mal registradas)
        """
        n_total = len(df)
        n_corrupt = int(n_total * self.noise_ratio)

        # Seleccionar filas aleatorias a corromper
        corrupt_idx = np.random.choice(df.index, size=n_corrupt, replace=False)

        # Distribuir tipos de corrupcion
        np.random.shuffle(corrupt_idx)
        splits = np.array([0.30, 0.25, 0.20, 0.15, 0.10])
        counts = (splits * n_corrupt).astype(int)
        # Ajustar residuo al primer grupo
        counts[0] += n_corrupt - counts.sum()

        idx_outliers = corrupt_idx[:counts[0]]
        idx_null_qty = corrupt_idx[counts[0]:counts[0]+counts[1]]
        idx_bad_date = corrupt_idx[counts[0]+counts[1]:counts[0]+counts[1]+counts[2]]
        idx_null_date = corrupt_idx[counts[0]+counts[1]+counts[2]:counts[0]+counts[1]+counts[2]+counts[3]]
        idx_negative = corrupt_idx[counts[0]+counts[1]+counts[2]+counts[3]:]

        # Convertir date a string para poder inyectar formatos invalidos
        df["date"] = df["date"].astype(str)
        # Convertir qty a float para poder inyectar NaN
        df["qty"] = df["qty"].astype(float)

        # 1. Outliers: fat finger x50
        df.loc[idx_outliers, "qty"] = df.loc[idx_outliers, "qty"] * 50

        # 2. Nulos en qty
        df.loc[idx_null_qty, "qty"] = np.nan

        # 3. Fechas en formatos invalidos
        bad_formats = [
            lambda d: "/".join(d.split("-")[::-1]),        # 31/12/2023
            lambda d: d.replace("-", "."),                  # 2023.12.31
            lambda d: "Dec 31st 23",                        # Formato texto
            lambda d: d.replace("-", ""),                   # 20231231
            lambda d: f"{d.split('-')[2]}/{d.split('-')[1]}/{d.split('-')[0][-2:]}",  # 31/12/23
        ]
        for i, idx in enumerate(idx_bad_date):
            fmt_fn = bad_formats[i % len(bad_formats)]
            try:
                df.at[idx, "date"] = fmt_fn(df.at[idx, "date"])
            except (IndexError, ValueError):
                df.at[idx, "date"] = "INVALID_DATE"

        # 4. Nulos en date
        df.loc[idx_null_date, "date"] = np.nan

        # 5. Cantidades negativas (devoluciones mal registradas)
        df.loc[idx_negative, "qty"] = -100.0

        print(f"\n   Ruido ERP inyectado: {n_corrupt:,} filas ({self.noise_ratio*100:.0f}%)")
        print(f"     Outliers (x50):        {len(idx_outliers)}")
        print(f"     Nulos en qty:          {len(idx_null_qty)}")
        print(f"     Fechas invalidas:      {len(idx_bad_date)}")
        print(f"     Nulos en date:         {len(idx_null_date)}")
        print(f"     Cantidades negativas:  {len(idx_negative)}")

        return df

    # ─── Main Pipeline ──────────────────────────────────

    def generate_all(self) -> pd.DataFrame:
        """
        Genera el dataset completo: 3 SKUs + ruido de ERP.

        Returns:
            DataFrame con columnas [date, sku, qty], desordenado.
        """
        print("\n" + "=" * 60)
        print("  ENTERPRISE DATA GENERATOR")
        print("=" * 60)
        print(f"\n   Generando historico de ventas...\n")

        t0 = time.perf_counter()

        # Generar cada SKU
        sku001 = self._generate_sku001_core()
        sku002 = self._generate_sku002_intermittent()
        sku003 = self._generate_sku003_seasonal()

        # Concatenar
        df = pd.concat([sku001, sku002, sku003], ignore_index=True)

        # Inyectar ruido
        df = self._inject_erp_noise(df)

        # Shuffle (simular volcado crudo de DB)
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)

        elapsed = time.perf_counter() - t0

        print(f"\n   Dataset final: {len(df):,} filas x {len(df.columns)} columnas")
        print(f"   Tiempo de generacion: {elapsed*1000:.0f}ms")

        return df

    def export_csv(
        self,
        df: pd.DataFrame,
        filename: str = "enterprise_sales_history.csv"
    ) -> str:
        """
        Exporta el dataset a CSV.

        Args:
            df: DataFrame a exportar.
            filename: Nombre del archivo de salida.

        Returns:
            Path del archivo generado.
        """
        from pathlib import Path
        output_path = Path(__file__).parent / filename
        df.to_csv(output_path, index=False)
        size_kb = output_path.stat().st_size / 1024
        print(f"\n   Exportado: {output_path.name} ({size_kb:.0f} KB)")
        print("=" * 60)
        return str(output_path)


def main() -> None:
    """Punto de entrada."""
    generator = EnterpriseDataGenerator(
        start_date="2023-01-01",
        end_date="2025-12-31",
        noise_ratio=0.05,
        seed=42
    )
    df = generator.generate_all()
    generator.export_csv(df)


if __name__ == "__main__":
    main()
