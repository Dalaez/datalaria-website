import pandas as pd
import numpy as np
import random
import os

def generate_dirty_bom():
    print("Iniciando sintetizador de BOM industrial corporativo...")
    
    # Base structure defining the graph: Product -> Assembly -> Components
    products = [
        {"sku": "DRONE-X1", "margin": 0.45},
        {"sku": "SERVER-RACK-9", "margin": 0.25},
        {"sku": "LIDAR-SENSOR-PRO", "margin": 0.55}
    ]
    
    assemblies = {
        "DRONE-X1": ["PCB-FLIGHT-01", "MOTOR-ASSEMBLY-04"],
        "SERVER-RACK-9": ["PCB-MAIN-01", "PWR-SUPPLY-02"],
        "LIDAR-SENSOR-PRO": ["PCB-SENSOR-05", "LASER-TUBE-01"]
    }
    
    # Internal components shared across assemblies
    components = [
        {"pn": "CAP-001", "desc": "Capacitor 10uF 50V", "type": "electronic"},
        {"pn": "RES-002", "desc": "Resistor 10k 1%", "type": "electronic"},
        {"pn": "MCU-003", "desc": "Microcontroller ARM Cortex", "type": "electronic"},
        {"pn": "SENS-004", "desc": "Gyroscope 6-axis", "type": "electronic"},
        {"pn": "MOTOR-005", "desc": "Brushless Motor 2204", "type": "mechanical"},
        {"pn": "ESC-006", "desc": "Electronic Speed Controller 30A", "type": "electronic"},
        {"pn": "CPU-007", "desc": "Server CPU 16-core", "type": "electronic"},
        {"pn": "RAM-008", "desc": "DDR4 32GB ECC", "type": "electronic"},
        {"pn": "TRANS-009", "desc": "Transformer 500W", "type": "electrical"},
        {"pn": "DIODE-010", "desc": "Diode Rectifier 10A", "type": "electronic"},
        {"pn": "LENS-011", "desc": "Optical Lens 45deg", "type": "optical"},
        {"pn": "LASER-012", "desc": "Laser Diode 905nm", "type": "optical"}
    ]
    
    # Assembly to Component mappings (BOM structure)
    assembly_bom = {
        "PCB-FLIGHT-01": ["CAP-001", "RES-002", "MCU-003", "SENS-004"],
        "MOTOR-ASSEMBLY-04": ["MOTOR-005", "ESC-006"],
        "PCB-MAIN-01": ["CPU-007", "RAM-008", "CAP-001", "RES-002"],
        "PWR-SUPPLY-02": ["TRANS-009", "DIODE-010", "MCU-003"],
        "PCB-SENSOR-05": ["MCU-003", "CAP-001"],
        "LASER-TUBE-01": ["LENS-011", "LASER-012"]
    }

    # External Market Data for AML mapping
    manufacturers = {
        "CAP-001": [("Texas Instruments", "TI-CAP-10U-50", "Active"), ("Yageo", "CC1206KKX7R9BB106", "Active")],
        "RES-002": [("Vishay", "CRCW120610K0FKEA", "Active")],
        "MCU-003": [("STMicroelectronics", "STM32F405RGT6", "NRND"), ("NXP", "MK20DX256VLH7", "Obsolete")],
        "SENS-004": [("Bosch Sensortec", "BMI160", "Active")],
        "MOTOR-005": [("T-Motor", "MN2204-2300KV", "Active")],
        "ESC-006": [("Hobbywing", "XRotor-Micro-30A", "EOL")],
        "CPU-007": [("Intel", "Xeon-Silver-4216", "Active"), ("AMD", "EPYC-7302P", "Active")],
        "RAM-008": [("Samsung", "M393A4K40CB2-CVF", "Active"), ("Micron", "MTA36ASF4G72PZ-2G9E2", "Active")],
        "TRANS-009": [("Mean Well", "RSP-500-24", "Active")],
        "DIODE-010": [("ON Semiconductor", "1N5408G", "Active")],
        "LENS-011": [("Thorlabs", "LA1131", "Active")],
        "LASER-012": [("Osram", "SPL PL90_3", "EOL")]
    }
    
    # Intentional Entropy Injection Mappings
    dirty_mfg_names = {
        "Texas Instruments": ["Texas Instruments", "TEXAS INSTRUMENTS", "ti", "Texas Inst."],
        "STMicroelectronics": ["STMicroelectronics", "ST Micro", "STM"],
        "ON Semiconductor": ["ON Semiconductor", "ON Semi", "onsemi"]
    }
    
    rows = []
    
    # Generate the flat table
    for prod in products:
        sku = prod["sku"]
        margin = prod["margin"]
        
        for assembly in assemblies[sku]:
            for comp_pn in assembly_bom[assembly]:
                # Determine quantity (Injecting mixed types: some ints, some strings)
                qty = random.randint(1, 10)
                if random.random() < 0.3:
                    qty = str(qty) # Entropy: mixed type for quantity
                
                # Fetch AML data
                aml_options = manufacturers.get(comp_pn, [("Generic", f"GEN-{comp_pn}", "Active")])
                
                # We might have multiple sources, create a row for each to simulate a flat AML export
                for mfg_name, mpn, lifecycle in aml_options:
                    
                    # 1. Entropy: Inconsistent Manufacturer Casing/Naming
                    if mfg_name in dirty_mfg_names:
                        final_mfg = random.choice(dirty_mfg_names[mfg_name])
                    else:
                        # Randomize case sometimes
                        if random.random() < 0.2:
                            final_mfg = mfg_name.upper()
                        elif random.random() < 0.1:
                            final_mfg = mfg_name.lower()
                        else:
                            final_mfg = mfg_name
                            
                    # 2. Entropy: Trailing/Leading spaces in MPN
                    final_mpn = mpn
                    if random.random() < 0.25:
                        final_mpn = f" {mpn} " # Both sides
                    elif random.random() < 0.15:
                        final_mpn = f"{mpn} " # Trailing
                    elif random.random() < 0.15:
                        final_mpn = f"  {mpn}" # Leading
                        
                    # 3. Entropy: Null Lifecycles
                    final_lifecycle = lifecycle
                    if random.random() < 0.15: # 15% chance Compras doesn't know the status
                        final_lifecycle = np.nan
                        
                    # Add to rows
                    rows.append({
                        "End_Product_SKU": sku,
                        "End_Product_Margin": margin,
                        "Assembly_PN": assembly,
                        "Component_PN": comp_pn,
                        "Quantity_per_Assembly": qty,
                        "Manufacturer": final_mfg,
                        "Manufacturer_PN": final_mpn,
                        "Lifecycle": final_lifecycle
                    })

    # Shuffle the dataframe to make it look like a raw export dump
    df = pd.DataFrame(rows)
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), "flat_bom_legacy.csv")
    df.to_csv(output_path, index=False)
    
    print(f"Sintetización completada. Archivo generado: {output_path}")
    print(f"Se han generado {len(df)} filas con entropía intencional (tipos mixtos, NaN, trailing spaces).")
    
    # Display a sample of the dirty data to terminal
    print("\nMuestra del 'ruido' generado:")
    print(df[['Component_PN', 'Quantity_per_Assembly', 'Manufacturer', 'Manufacturer_PN', 'Lifecycle']].head(10))

if __name__ == "__main__":
    generate_dirty_bom()
