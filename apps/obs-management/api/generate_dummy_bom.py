"""Sintetizador determinista de BOM industrial con márgenes en EUR absolutos (NUMERIC(12,2))."""

from __future__ import annotations

import os
import random
import numpy as np
import pandas as pd


def generate_dirty_bom(seed: int = 42) -> pd.DataFrame:
    rng = random.Random(seed)

    # Margen Bruto expresado estrictamente en EUR absolutos (coherente con obs_radar.products.gross_margin)
    products = [
        {"sku": "DRONE-X1", "margin_eur": 12500.00},
        {"sku": "SERVER-RACK-9", "margin_eur": 2950.00},
        {"sku": "LIDAR-SENSOR-PRO", "margin_eur": 18400.00},
    ]

    assemblies = {
        "DRONE-X1": ["PCB-FLIGHT-01", "MOTOR-ASSEMBLY-04"],
        "SERVER-RACK-9": ["PCB-MAIN-01", "PWR-SUPPLY-02"],
        "LIDAR-SENSOR-PRO": ["PCB-SENSOR-05", "LASER-TUBE-01"],
    }

    assembly_bom = {
        "PCB-FLIGHT-01": ["CAP-001", "RES-002", "MCU-003", "SENS-004"],
        "MOTOR-ASSEMBLY-04": ["MOTOR-005", "ESC-006"],
        "PCB-MAIN-01": ["CPU-007", "RAM-008", "CAP-001", "RES-002"],
        "PWR-SUPPLY-02": ["TRANS-009", "DIODE-010", "MCU-003"],
        "PCB-SENSOR-05": ["MCU-003", "CAP-001"],
        "LASER-TUBE-01": ["LENS-011", "LASER-012"],
    }

    manufacturers = {
        "CAP-001": [("Texas Instruments", "TI-CAP-10U-50", "EOL"), ("Yageo", "CC1206KKX7R9BB106", "EOL")],
        "RES-002": [("Vishay", "CRCW120610K0FKEA", "Active")],
        "MCU-003": [("STMicroelectronics", "STM32F405RGT6", "NRND"), ("NXP", "MK20DX256VLH7", "Obsolete")],
        "SENS-004": [("Bosch Sensortec", "BMI160", "Active")],
        "MOTOR-005": [("T-Motor", "MN2204-2300KV", "Active")],
        "ESC-006": [("Hobbywing", "XRotor-Micro-30A", "Active")],
        "CPU-007": [("Intel", "Xeon-Silver-4216", "Active"), ("AMD", "EPYC-7302P", "Active")],
        "RAM-008": [("Samsung", "M393A4K40CB2-CVF", "Active"), ("Micron", "MTA36ASF4G72PZ-2G9E2", "Active")],
        "TRANS-009": [("Mean Well", "RSP-500-24", "Active")],
        "DIODE-010": [("ON Semiconductor", "1N5408G", "Active")],
        "LENS-011": [("Thorlabs", "LA1131", "Active")],
        "LASER-012": [("Osram", "SPL-PL90-3", "Active")],
    }

    dirty_mfg_names = {
        "Texas Instruments": ["Texas Instruments", "TEXAS INSTRUMENTS", "ti", "Texas Inst."],
        "STMicroelectronics": ["STMicroelectronics", "ST Micro", "STM"],
        "ON Semiconductor": ["ON Semiconductor", "ON Semi", "onsemi"],
    }

    rows = []
    for prod in products:
        sku = prod["sku"]
        margin_eur = prod["margin_eur"]
        for assembly in assemblies[sku]:
            for comp_pn in assembly_bom[assembly]:
                qty: int | str = rng.randint(1, 10)
                if rng.random() < 0.3:
                    qty = str(qty)
                for mfg_name, mpn, lifecycle in manufacturers.get(comp_pn, [("Generic", f"GEN-{comp_pn}", "Active")]):
                    final_mfg = rng.choice(dirty_mfg_names[mfg_name]) if mfg_name in dirty_mfg_names else mfg_name
                    final_mpn = f" {mpn} " if rng.random() < 0.25 else mpn
                    final_lifecycle: str | float = np.nan if rng.random() < 0.10 else lifecycle
                    rows.append(
                        {
                            "End_Product_SKU": sku,
                            "End_Product_Margin": margin_eur,
                            "Assembly_PN": assembly,
                            "Component_PN": comp_pn,
                            "Quantity_per_Assembly": qty,
                            "Manufacturer": final_mfg,
                            "Manufacturer_PN": final_mpn,
                            "Lifecycle": final_lifecycle,
                        }
                    )

    df = pd.DataFrame(rows).sample(frac=1, random_state=seed).reset_index(drop=True)
    output_path = os.path.join(os.path.dirname(__file__), "flat_bom_legacy.csv")
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Sintetización completada: {output_path} ({len(df)} filas, márgenes en EUR absolutos).")
    return df


if __name__ == "__main__":
    generate_dirty_bom()
