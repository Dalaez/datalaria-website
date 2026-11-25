"""Cargador idempotente de BOM plano hacia el esquema aislado `obs_radar` en Supabase.

Cumple Constitución Art. 4 (esquema `obs_radar` + `user_id` RLS) y ADR-014 (`seeder_guard`).
"""

from __future__ import annotations

import os
from typing import Any
import numpy as np
import pandas as pd
from dotenv import load_dotenv

from seeder_guard import validate_synthetic_seed_target
from supabase_tools import get_supabase_obs_client

load_dotenv()


def normalize_gross_margin_eur(raw_value: Any) -> float:
    """Garantiza que el margen se almacene en EUR absolutos (NUMERIC(12,2)), nunca como ratio < 1."""
    val = float(raw_value)
    if val <= 0:
        return 0.0
    if val <= 1.0:
        return round(val * 25000.0, 2)
    return round(val, 2)


def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding="utf-8")

    for col in ("Manufacturer_PN", "Manufacturer", "Assembly_PN", "Component_PN", "End_Product_SKU"):
        df[col] = df[col].astype(str).str.strip().str.upper()

    df["Quantity_per_Assembly"] = (
        pd.to_numeric(df["Quantity_per_Assembly"].astype(str).str.strip(), errors="coerce")
        .fillna(1)
        .astype(int)
    )
    df["End_Product_Margin"] = pd.to_numeric(df["End_Product_Margin"], errors="coerce").fillna(5000.0).apply(
        normalize_gross_margin_eur
    )
    df["Lifecycle"] = df["Lifecycle"].replace(r"^\s*$", np.nan, regex=True).fillna("Active").astype(str).str.strip()
    valid = {"Active", "NRND", "EOL", "Obsolete"}
    df["Lifecycle"] = df["Lifecycle"].apply(lambda x: x if x in valid else "Active")
    return df


def ingest_products(df: pd.DataFrame, db: Any, user_id: str) -> None:
    products = (
        df[["End_Product_SKU", "End_Product_Margin"]]
        .drop_duplicates(subset=["End_Product_SKU"])
        .rename(columns={"End_Product_SKU": "sku", "End_Product_Margin": "gross_margin"})
    )
    products["name"] = products["sku"] + " System"
    products["user_id"] = user_id
    res = db.table("products").upsert(products.to_dict(orient="records"), on_conflict="user_id,sku").execute()
    print(f"Upserted {len(res.data)} products into obs_radar.products.")


def ingest_internal_parts(df: pd.DataFrame, db: Any, user_id: str) -> None:
    assemblies = df[["Assembly_PN"]].drop_duplicates().copy()
    assemblies["internal_pn"] = assemblies["Assembly_PN"]
    assemblies["part_type"] = "assembly"
    assemblies["description"] = "Subensamblaje interno para " + assemblies["Assembly_PN"]

    components = df[["Component_PN"]].drop_duplicates().copy()
    components["internal_pn"] = components["Component_PN"]
    components["part_type"] = "component"
    components["description"] = "Componente " + components["Component_PN"]

    internal_parts = pd.concat(
        [
            assemblies[["internal_pn", "part_type", "description"]],
            components[["internal_pn", "part_type", "description"]],
        ]
    ).drop_duplicates(subset=["internal_pn"])
    internal_parts["user_id"] = user_id

    res = (
        db.table("internal_parts")
        .upsert(internal_parts.to_dict(orient="records"), on_conflict="user_id,internal_pn")
        .execute()
    )
    print(f"Upserted {len(res.data)} internal parts into obs_radar.internal_parts.")


def ingest_manufacturer_parts(df: pd.DataFrame, db: Any, user_id: str) -> None:
    mparts = (
        df[["Manufacturer_PN", "Manufacturer", "Lifecycle"]]
        .drop_duplicates(subset=["Manufacturer_PN"])
        .rename(columns={"Manufacturer_PN": "mpn", "Manufacturer": "manufacturer_name", "Lifecycle": "lifecycle_status"})
    )
    mparts["user_id"] = user_id
    res = db.table("manufacturer_parts").upsert(mparts.to_dict(orient="records"), on_conflict="user_id,mpn").execute()
    print(f"Upserted {len(res.data)} manufacturer parts into obs_radar.manufacturer_parts.")


def get_db_lookups(db: Any, user_id: str) -> tuple[dict[str, str], dict[str, str]]:
    prods = db.table("products").select("id, sku").eq("user_id", user_id).execute()
    parts = db.table("internal_parts").select("id, internal_pn").eq("user_id", user_id).execute()
    return {p["sku"]: p["id"] for p in prods.data}, {p["internal_pn"]: p["id"] for p in parts.data}


def ingest_aml(df: pd.DataFrame, db: Any, user_id: str, part_map: dict[str, str]) -> None:
    aml_df = df[["Component_PN", "Manufacturer_PN"]].drop_duplicates()
    existing = db.table("aml").select("internal_pn, manufacturer_pn").eq("user_id", user_id).execute()
    existing_pairs = {(e["internal_pn"], e["manufacturer_pn"]) for e in existing.data}

    new_rows = []
    for _, row in aml_df.iterrows():
        internal_uuid = part_map.get(row["Component_PN"])
        mpn = row["Manufacturer_PN"]
        if not internal_uuid or (internal_uuid, mpn) in existing_pairs:
            continue
        new_rows.append(
            {"user_id": user_id, "internal_pn": internal_uuid, "manufacturer_pn": mpn, "preference_level": "Primary"}
        )

    if new_rows:
        res = db.table("aml").insert(new_rows).execute()
        print(f"Inserted {len(res.data)} new AML links.")


def ingest_bom_lines(df: pd.DataFrame, db: Any, user_id: str, prod_map: dict[str, str], part_map: dict[str, str]) -> None:
    existing = db.table("bom_lines").select("parent_product_id, parent_assembly_id, child_pn").eq("user_id", user_id).execute()
    prod_links = {(e["parent_product_id"], e["child_pn"]) for e in existing.data if e.get("parent_product_id")}
    asm_links = {(e["parent_assembly_id"], e["child_pn"]) for e in existing.data if e.get("parent_assembly_id")}

    new_lines = []
    prod_asm_df = df[["End_Product_SKU", "Assembly_PN"]].drop_duplicates()
    for _, row in prod_asm_df.iterrows():
        p_uuid = prod_map.get(row["End_Product_SKU"])
        c_uuid = part_map.get(row["Assembly_PN"])
        if p_uuid and c_uuid and (p_uuid, c_uuid) not in prod_links:
            prod_links.add((p_uuid, c_uuid))
            new_lines.append(
                {"user_id": user_id, "parent_product_id": p_uuid, "parent_assembly_id": None, "child_pn": c_uuid, "quantity": 1}
            )

    asm_comp_df = df[["Assembly_PN", "Component_PN", "Quantity_per_Assembly"]].drop_duplicates(
        subset=["Assembly_PN", "Component_PN"]
    )
    for _, row in asm_comp_df.iterrows():
        p_uuid = part_map.get(row["Assembly_PN"])
        c_uuid = part_map.get(row["Component_PN"])
        if p_uuid and c_uuid and (p_uuid, c_uuid) not in asm_links:
            asm_links.add((p_uuid, c_uuid))
            new_lines.append(
                {
                    "user_id": user_id,
                    "parent_product_id": None,
                    "parent_assembly_id": p_uuid,
                    "child_pn": c_uuid,
                    "quantity": int(row["Quantity_per_Assembly"]),
                }
            )

    if new_lines:
        res = db.table("bom_lines").insert(new_lines).execute()
        print(f"Inserted {len(res.data)} BOM graph lines into obs_radar.bom_lines.")


def main() -> None:
    demo_uid = os.getenv("DEMO_USER_ID", "").strip()
    demo_email = os.getenv("DEMO_USER_EMAIL", "").strip()
    validate_synthetic_seed_target(demo_uid, email=demo_email or None)

    db = get_supabase_obs_client()
    csv_path = os.path.join(os.path.dirname(__file__), "flat_bom_legacy.csv")
    cleaned_df = load_and_clean_data(csv_path)

    ingest_products(cleaned_df, db, demo_uid)
    ingest_internal_parts(cleaned_df, db, demo_uid)
    ingest_manufacturer_parts(cleaned_df, db, demo_uid)

    prod_map, part_map = get_db_lookups(db, demo_uid)
    ingest_aml(cleaned_df, db, demo_uid, part_map)
    ingest_bom_lines(cleaned_df, db, demo_uid, prod_map, part_map)
    print("[OK] Migración al esquema aislado obs_radar completada al 100 %.")


if __name__ == "__main__":
    main()
