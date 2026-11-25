"""Adaptador Supabase Multi-Esquema (`obs_radar`) y Tool de CrewAI sin consultas N+1.

Carga por lote (5 selects planos) el grafo BOM desde el esquema `obs_radar` de `datalaria-core`
y delega el cálculo determinista a `bom_engine.py` (Constitución Art. 1.3 y 4).
"""

from __future__ import annotations

import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

_cached_client: Any = None


def get_supabase_obs_client() -> Any:
    """Inicializa perezosamente el cliente Supabase apuntando al esquema `obs_radar`."""
    global _cached_client
    if _cached_client is not None:
        return _cached_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Faltan credenciales SUPABASE_URL / SUPABASE_KEY en el entorno.")

    from supabase import create_client

    client = create_client(url, key)
    _cached_client = client.schema("obs_radar")
    return _cached_client


def load_catalog_from_supabase(client: Any = None) -> dict[str, Any]:
    """Carga el grafo BOM desde `obs_radar` en 5 consultas planas sin recursividad N+1."""
    db = client or get_supabase_obs_client()

    products_res = db.table("products").select("id, sku, name, gross_margin").execute()
    parts_res = db.table("internal_parts").select("id, internal_pn, part_type").execute()
    bom_res = db.table("bom_lines").select("parent_product_id, parent_assembly_id, child_pn, quantity").execute()
    aml_res = db.table("aml").select("internal_pn, manufacturer_pn, preference_level").execute()
    mpns_res = db.table("manufacturer_parts").select(
        "mpn, manufacturer_name, lifecycle_status, unit_price_eur, monthly_demand"
    ).execute()

    prod_id_to_sku = {p["id"]: p["sku"] for p in (products_res.data or [])}
    part_id_to_pn = {p["id"]: p["internal_pn"] for p in (parts_res.data or [])}

    products = [
        {"sku": p["sku"], "name": p.get("name", p["sku"]), "gross_margin": float(p["gross_margin"])}
        for p in (products_res.data or [])
    ]

    bom_edges: list[dict[str, Any]] = []
    for line in bom_res.data or []:
        child_pn = part_id_to_pn.get(line["child_pn"])
        if not child_pn:
            continue
        if line.get("parent_product_id"):
            parent_sku = prod_id_to_sku.get(line["parent_product_id"])
            if parent_sku:
                bom_edges.append({"parent": parent_sku, "parentType": "product", "child": child_pn, "qty": line["quantity"]})
        elif line.get("parent_assembly_id"):
            parent_asm = part_id_to_pn.get(line["parent_assembly_id"])
            if parent_asm:
                bom_edges.append({"parent": parent_asm, "parentType": "assembly", "child": child_pn, "qty": line["quantity"]})

    aml = [
        {
            "internal_pn": part_id_to_pn.get(row["internal_pn"], str(row["internal_pn"])),
            "mpn": row["manufacturer_pn"],
            "pref": row.get("preference_level", "Primary"),
        }
        for row in (aml_res.data or [])
        if row.get("internal_pn") in part_id_to_pn
    ]

    mpns = {
        str(row["mpn"]).strip().upper(): {
            "mpn": str(row["mpn"]).strip().upper(),
            "manufacturer": row.get("manufacturer_name", "Unknown"),
            "lifecycle": row.get("lifecycle_status", "Active"),
            "unit_price_eur": float(row.get("unit_price_eur") or 5.0),
            "monthly_demand": int(row.get("monthly_demand") or 300),
        }
        for row in (mpns_res.data or [])
    }

    return {"products": products, "bomEdges": bom_edges, "aml": aml, "mpns": mpns}


def calculate_financial_impact_impl(mpn: str, catalog: dict[str, Any] | None = None) -> str:
    """Ejecuta el cálculo de impacto financiero determinista sobre `obs_radar` (testeable sin CrewAI)."""
    from bom_engine import traverse_bom_upward

    cat = catalog if catalog is not None else load_catalog_from_supabase()
    mpn_clean = mpn.strip().upper()
    if mpn_clean not in cat.get("mpns", {}):
        return f"MPN '{mpn}' no encontrado en el esquema obs_radar. Cero impacto."

    tr = traverse_bom_upward(cat, mpn_clean)
    if not tr["internal_pns"]:
        return f"MPN '{mpn}' carece de vínculo activo en la Approved Manufacturer List (AML). Cero impacto."
    if not tr["affected_skus"]:
        return f"El MPN '{mpn}' existe internamente, pero carece de dependencias en Productos Activos. Riesgo cero."

    details = [
        f"{item.sku} (Margen Expuesto: {item.margin_at_risk:.2f}€, IEC62402={item.criticality_score}/100)"
        for item in tr["affected_skus"]
    ]
    return (
        f"El MPN {mpn_clean} (Internal PN: {tr['internal_pns'][0]}, Alternativas AML: {tr['alt_sources_count']}) "
        f"impacta a: [{', '.join(details)}]. Riesgo financiero consolidado: {tr['total_risk_eur']:.2f}€."
    )


try:
    from crewai.tools import tool

    @tool
    def calculate_financial_impact(mpn: str) -> str:
        """Calculates deterministic financial P&L impact in obs_radar when a Manufacturer Part Number (MPN) becomes obsolete."""
        return calculate_financial_impact_impl(mpn)
except ImportError:
    def calculate_financial_impact(mpn: str) -> str:  # type: ignore[misc]
        """Fallback sin CrewAI para ejecución directa o tests unitarios."""
        return calculate_financial_impact_impl(mpn)
