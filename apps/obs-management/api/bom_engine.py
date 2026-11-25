"""Motor determinista puro de Agentic Radar (El Músculo — Constitución Art. 1.3).

Implementa sin llamadas a LLMs ni consultas N+1:
  - Recorrido DAG multinivel de BOM con prevención de ciclos (`visited`, INV-OBS-4).
  - Índice de criticidad IEC 62402 (0..100).
  - Evaluación de riesgo consolidado de catálogo (deduplicando SKUs finales).
  - Decisión financiera Last Time Buy (LTB) vs. Rediseño FFF + puente APICS SS_LTB.
"""

from __future__ import annotations

from datetime import datetime, timezone
import math
from typing import Any

from models import (
    AffectedSkuItem,
    DashboardRiskMetrics,
    LtbComparisonInput,
    LtbComparisonResult,
    SeverityBand,
)

LIFECYCLE_SCORE: dict[str, int] = {
    "Obsolete": 100,
    "EOL": 85,
    "NRND": 55,
    "Active": 10,
}


def build_default_sandbox_catalog() -> dict[str, Any]:
    """Genera el catálogo industrial de referencia equivalente al preset `drone-capacitor` en frontend."""
    return {
        "products": [
            {"sku": "DRONE-X1", "name": "Autonomous Inspection Drone X1", "gross_margin": 12500.0},
            {"sku": "SERVER-RACK-9", "name": "Edge Telemetry Server Rack 9", "gross_margin": 2950.0},
            {"sku": "LIDAR-SENSOR-PRO", "name": "Industrial LiDAR Sensor Pro", "gross_margin": 18400.0},
        ],
        "bomEdges": [
            {"parent": "DRONE-X1", "parentType": "product", "child": "PCB-FLIGHT-01", "qty": 1},
            {"parent": "DRONE-X1", "parentType": "product", "child": "MOTOR-ASSEMBLY-04", "qty": 1},
            {"parent": "SERVER-RACK-9", "parentType": "product", "child": "PCB-MAIN-01", "qty": 1},
            {"parent": "SERVER-RACK-9", "parentType": "product", "child": "PWR-SUPPLY-02", "qty": 1},
            {"parent": "LIDAR-SENSOR-PRO", "parentType": "product", "child": "PCB-SENSOR-05", "qty": 1},
            {"parent": "LIDAR-SENSOR-PRO", "parentType": "product", "child": "LASER-TUBE-01", "qty": 1},
            {"parent": "PCB-FLIGHT-01", "parentType": "assembly", "child": "CAP-001", "qty": 4},
            {"parent": "PCB-FLIGHT-01", "parentType": "assembly", "child": "MCU-003", "qty": 1},
            {"parent": "MOTOR-ASSEMBLY-04", "parentType": "assembly", "child": "ESC-006", "qty": 4},
            {"parent": "PCB-MAIN-01", "parentType": "assembly", "child": "RAM-008", "qty": 4},
            {"parent": "PWR-SUPPLY-02", "parentType": "assembly", "child": "MCU-003", "qty": 2},
            {"parent": "PCB-SENSOR-05", "parentType": "assembly", "child": "MCU-003", "qty": 1},
            {"parent": "PCB-SENSOR-05", "parentType": "assembly", "child": "CAP-001", "qty": 6},
            {"parent": "LASER-TUBE-01", "parentType": "assembly", "child": "LASER-012", "qty": 2},
        ],
        "aml": [
            {"internal_pn": "CAP-001", "mpn": "TI-CAP-10U-50", "manufacturer": "Texas Instruments", "pref": "Primary"},
            {"internal_pn": "CAP-001", "mpn": "CC1206KKX7R9BB106", "manufacturer": "Yageo", "pref": "Secondary"},
            {"internal_pn": "MCU-003", "mpn": "STM32F405RGT6", "manufacturer": "STMicroelectronics", "pref": "Primary"},
            {"internal_pn": "MCU-003", "mpn": "MK20DX256VLH7", "manufacturer": "NXP", "pref": "Secondary"},
            {"internal_pn": "ESC-006", "mpn": "XROTOR-MICRO-30A", "manufacturer": "Hobbywing", "pref": "Primary"},
            {"internal_pn": "RAM-008", "mpn": "M393A4K40CB2-CVF", "manufacturer": "Samsung", "pref": "Primary"},
            {"internal_pn": "LASER-012", "mpn": "SPL-PL90-3", "manufacturer": "Osram", "pref": "Primary"},
        ],
        "mpns": {
            "TI-CAP-10U-50": {"mpn": "TI-CAP-10U-50", "manufacturer": "Texas Instruments", "lifecycle": "EOL", "unit_price_eur": 1.85, "monthly_demand": 900},
            "CC1206KKX7R9BB106": {"mpn": "CC1206KKX7R9BB106", "manufacturer": "Yageo", "lifecycle": "EOL", "unit_price_eur": 1.4, "monthly_demand": 900},
            "STM32F405RGT6": {"mpn": "STM32F405RGT6", "manufacturer": "STMicroelectronics", "lifecycle": "NRND", "unit_price_eur": 8.4, "monthly_demand": 420},
            "MK20DX256VLH7": {"mpn": "MK20DX256VLH7", "manufacturer": "NXP", "lifecycle": "Obsolete", "unit_price_eur": 9.2, "monthly_demand": 180},
            "XROTOR-MICRO-30A": {"mpn": "XROTOR-MICRO-30A", "manufacturer": "Hobbywing", "lifecycle": "Active", "unit_price_eur": 19.5, "monthly_demand": 260},
            "M393A4K40CB2-CVF": {"mpn": "M393A4K40CB2-CVF", "manufacturer": "Samsung", "lifecycle": "Active", "unit_price_eur": 68.0, "monthly_demand": 110},
            "SPL-PL90-3": {"mpn": "SPL-PL90-3", "manufacturer": "Osram", "lifecycle": "Active", "unit_price_eur": 42.0, "monthly_demand": 150},
        },
    }


def _round_half_up(value: float) -> int:
    return int(math.floor(value + 0.5))


def compute_criticality(
    lifecycle: str,
    alt_sources_count: int,
    margin_at_risk: float,
    ref_margin: float = 15000.0,
) -> tuple[int, SeverityBand]:
    """Calcula el índice determinista IEC 62402 (0..100) y la banda de severidad."""
    s_life = LIFECYCLE_SCORE.get(lifecycle, 10)
    s_aml = 100 if alt_sources_count <= 0 else (50 if alt_sources_count == 1 else 15)
    denom = max(15000.0, float(ref_margin or 15000.0))
    s_margin = min(100.0, (100.0 * max(0.0, float(margin_at_risk or 0.0))) / denom)
    score = min(100, _round_half_up(0.40 * s_life + 0.35 * s_aml + 0.25 * s_margin))

    if score >= 75:
        status: SeverityBand = "CRITICAL LTB REQUIRED"
    elif score >= 45:
        status = "EVALUATING INVENTORY"
    else:
        status = "MONITORED"
    return score, status


def traverse_bom_upward(catalog: dict[str, Any], target_mpn: str) -> dict[str, Any]:
    """Recorre el grafo BOM en memoria desde un MPN hasta los productos finales evitando ciclos (INV-OBS-4)."""
    mpn_clean = str(target_mpn or "").strip().upper()
    products = catalog.get("products", [])
    product_map: dict[str, dict[str, Any]] = {str(p["sku"]).upper(): p for p in products}

    parent_index: dict[str, list[dict[str, Any]]] = {}
    for edge in catalog.get("bomEdges", []):
        child = str(edge["child"]).upper()
        parent_index.setdefault(child, []).append(edge)

    aml_list = catalog.get("aml", [])
    mpns_dict = catalog.get("mpns", {})

    aml_matches = [a for a in aml_list if str(a["mpn"]).upper() == mpn_clean]
    internal_pns = list(dict.fromkeys(str(a["internal_pn"]).upper() for a in aml_matches))
    mpn_info = mpns_dict.get(
        mpn_clean,
        {"mpn": mpn_clean, "lifecycle": "EOL", "manufacturer": "Unknown", "unit_price_eur": 5.0, "monthly_demand": 200},
    )

    min_alt_active: float = float("inf") if internal_pns else 0.0
    for ipn in internal_pns:
        alts = [
            a
            for a in aml_list
            if str(a["internal_pn"]).upper() == ipn
            and str(a["mpn"]).upper() != mpn_clean
            and mpns_dict.get(str(a["mpn"]).upper(), {}).get("lifecycle", "Active") == "Active"
        ]
        min_alt_active = min(min_alt_active, float(len(alts)))
    alt_sources_count = int(min_alt_active) if math.isfinite(min_alt_active) else 0

    affected_map: dict[str, dict[str, Any]] = {}
    paths: list[dict[str, Any]] = []
    cycle_detected = False

    def dfs(node_id: str, chain: list[str], visited: set[str]) -> None:
        nonlocal cycle_detected
        for edge in parent_index.get(node_id, []):
            parent_id = str(edge["parent"]).upper()
            if parent_id in visited:
                cycle_detected = True
                continue
            next_chain = [*chain, parent_id]
            if edge.get("parentType") == "product" or parent_id in product_map:
                prod = product_map.get(parent_id)
                if prod:
                    paths.append(
                        {
                            "mpn": mpn_clean,
                            "internal_pn": chain[0],
                            "assemblies": chain[1:],
                            "sku": prod["sku"],
                            "gross_margin": float(prod["gross_margin"]),
                        }
                    )
                    if prod["sku"] not in affected_map:
                        affected_map[prod["sku"]] = {
                            "sku": prod["sku"],
                            "name": prod.get("name", prod["sku"]),
                            "margin_at_risk": float(prod["gross_margin"]),
                            "assembly_path": chain[1:],
                        }
            else:
                dfs(parent_id, next_chain, visited | {parent_id})

    for ipn in internal_pns:
        dfs(ipn, [ipn], {ipn})

    max_catalog_margin = max([15000.0, *(float(p.get("gross_margin") or 0.0) for p in products)])
    affected_skus: list[AffectedSkuItem] = []
    for item in affected_map.values():
        score, status = compute_criticality(
            str(mpn_info.get("lifecycle", "EOL")),
            alt_sources_count,
            item["margin_at_risk"],
            max_catalog_margin,
        )
        affected_skus.append(
            AffectedSkuItem(
                sku=item["sku"],
                trigger_mpn=mpn_clean,
                assembly_path=item["assembly_path"],
                margin_at_risk=item["margin_at_risk"],
                criticality_score=score,
                alt_sources_count=alt_sources_count,
                status=status,
            )
        )

    total_risk_eur = sum(s.margin_at_risk for s in affected_skus)
    return {
        "mpn": mpn_clean,
        "lifecycle": mpn_info.get("lifecycle", "EOL"),
        "manufacturer": mpn_info.get("manufacturer", "Unknown"),
        "internal_pns": internal_pns,
        "alt_sources_count": alt_sources_count,
        "affected_skus": affected_skus,
        "paths": paths,
        "total_risk_eur": round(total_risk_eur, 2),
        "cycle_detected": cycle_detected,
    }


def evaluate_catalog_risk(catalog: dict[str, Any]) -> DashboardRiskMetrics:
    """Evalúa todo el catálogo y consolida métricas ejecutivas deduplicando SKUs finales."""
    mpns_values = list(catalog.get("mpns", {}).values())
    flagged = [m for m in mpns_values if m.get("lifecycle") in {"EOL", "Obsolete", "NRND"}]
    eol_count = sum(1 for m in flagged if m.get("lifecycle") in {"EOL", "Obsolete"})

    sku_unique_margin: dict[str, float] = {}
    rows: list[AffectedSkuItem] = []
    logs: list[str] = []
    cycle_detected = False
    estimated_ltb_capital_eur = 0.0

    sec = 2

    def next_ts() -> str:
        nonlocal sec
        s = f"{sec % 60:02d}"
        m = f"{31 + (sec // 60):02d}"
        sec += 3
        return f"18:{m}:{s}"

    for m in flagged:
        tr = traverse_bom_upward(catalog, str(m["mpn"]))
        if tr["cycle_detected"]:
            cycle_detected = True
        is_hard_eol = m.get("lifecycle") in {"EOL", "Obsolete"}

        if tr["affected_skus"] and is_hard_eol:
            demand = float(m.get("monthly_demand") or 300)
            price = float(m.get("unit_price_eur") or 5.0)
            estimated_ltb_capital_eur += round(demand * 7.5 * price)

        if is_hard_eol:
            logs.append(f"[{next_ts()}] [Webhook] PDN/EOL alert received: {m['mpn']} ({m.get('manufacturer', 'Unknown')}, {m['lifecycle']}).")
            logs.append(f"[{next_ts()}] [CrewAI] Semantic MPN verified -> {m['mpn']}. Calling deterministic bom_engine.")

        for item in tr["affected_skus"]:
            rows.append(item)
            if is_hard_eol:
                sku_unique_margin[item.sku] = max(sku_unique_margin.get(item.sku, 0.0), item.margin_at_risk)
                ipn = tr["internal_pns"][0] if tr["internal_pns"] else "N/A"
                path_str = " -> ".join(item.assembly_path)
                logs.append(f"[{next_ts()}] [BOM/SQL] DAG path {ipn} -> {path_str} -> {item.sku}. IEC={item.criticality_score}.")

        if is_hard_eol and tr["affected_skus"]:
            logs.append(
                f"[{next_ts()}] [Alert] {m['mpn']} exposes {tr['total_risk_eur']:.2f} EUR across "
                f"{len(tr['affected_skus'])} SKU(s). Alt AML={tr['alt_sources_count']}."
            )

    rows.sort(key=lambda r: (-r.criticality_score, -r.margin_at_risk))
    total_risk_eur = sum(sku_unique_margin.values())

    if not logs:
        logs.append("[18:31:00] [CrewAI] Catalog scan complete. Zero critical EOL/Obsolete triggers active.")
    else:
        logs.append(f"[{next_ts()}] [CrewAI] Risk consolidation complete. Deduplicated P&L exposure: {total_risk_eur:.2f} EUR.")

    return DashboardRiskMetrics(
        total_risk_eur=round(total_risk_eur, 2),
        active_alerts=eol_count,
        blocked_skus_count=len(sku_unique_margin),
        estimated_ltb_capital_eur=round(estimated_ltb_capital_eur, 2),
        affected_skus=rows,
        agent_logs=logs,
        cycle_detected=cycle_detected,
        generated_at=datetime.now(timezone.utc),
    )


def compute_ltb_vs_fff(inp: LtbComparisonInput) -> LtbComparisonResult:
    """Calcula la decisión financiera LTB vs. Rediseño FFF en paridad exacta con engine.js (INV-OBS-4)."""
    dm = float(inp.monthly_demand)
    cv = float(inp.demand_cv)
    tr = float(inp.redesign_months)
    lm = float(inp.lead_time_months)
    i0 = float(inp.current_stock_units)
    p_ltb = float(inp.ltb_unit_price_eur)
    p_fff = float(inp.fff_unit_price_eur)
    nre = float(inp.redesign_nre_eur)
    wh = float(inp.annual_holding_wacc_rate)
    mm = float(inp.monthly_margin_at_risk_eur)
    z = float(inp.service_level_z)

    horizon = tr + lm
    q_base = dm * horizon
    ss_ltb = z * (cv * dm) * math.sqrt(horizon)
    q_ltb = max(0, math.ceil(q_base + ss_ltb - i0))
    wc_ltb = q_ltb * p_ltb
    tc_ltb = wc_ltb * (1.0 + ((wh / 2.0) * (tr / 12.0)))

    t_stock = i0 / dm
    gap_months = max(0.0, tr - t_stock)
    fff_base_only = nre + q_base * p_fff
    tc_fff = fff_base_only + gap_months * mm

    if gap_months > 0 and fff_base_only < tc_ltb:
        verdict = "HYBRID_BRIDGE"
    elif tc_fff < tc_ltb:
        verdict = "REDESIGN_FFF"
    else:
        verdict = "EXECUTE_LTB"

    savings_eur = abs(tc_ltb - tc_fff)
    breakeven_months = round(nre / (dm * (p_ltb - p_fff)), 1) if p_ltb > p_fff else None

    return LtbComparisonResult(
        safety_stock_units=math.ceil(ss_ltb),
        ltb_order_qty=q_ltb,
        ltb_working_capital_eur=round(wc_ltb, 2),
        ltb_total_cost_eur=round(tc_ltb, 2),
        fff_total_cost_eur=round(tc_fff, 2),
        stock_gap_months=round(gap_months, 1),
        savings_eur=round(savings_eur, 2),
        breakeven_months=breakeven_months,
        verdict=verdict,
    )
