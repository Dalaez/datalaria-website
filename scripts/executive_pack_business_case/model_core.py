#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
model_core.py
=============
Fuente Única de Verdad Numérica y Motor Analítico DCF para el Executive Decision Pack
"Business Case Financiero: VAN, TIR, Payback & Análisis de Sensibilidad Tornado".

Caso de Ejemplo:
- Proyecto: "Automatización y Digitalización de Línea de Producción" (Industria manufacturera).
- Inversión inicial (CAPEX): 1.200.000 € en dos tramos (850.000 € Año 0 + 350.000 € Año 1).
- Horizonte de proyección: 5 años operativos (Años 0 a 5) + Valor Residual opcional (Gordon).
- WACC estimado vía CAPM: 9,50%.

Todos los activos (Excel, PowerPoint, PDF, imágenes y blog posts) derivan sus cifras de este módulo.
"""

import sys
import math

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# 1. PARÁMETROS DEL CASO BASE Y POLÍTICA DE INVERSIÓN
# ==============================================================================

# Política de Inversión (Hurdle Policy)
HURDLE_POLICY = {
    "hurdle_margin_pp": 0.030,         # +3,0 pp sobre WACC (TIR exigida = WACC + 3,0 pp = 12,50%)
    "max_discounted_payback_yrs": 4.0, # Payback descontado máximo admisible: 4,0 años
    "reinvestment_rate": 0.095,        # Tasa de reinversión para MIRR (igual a WACC = 9,50%)
    "tax_rate": 0.25,                  # Tipo impositivo sobre sociedades: 25%
    "depreciation_years": 5,           # Vida útil para amortización lineal: 5 años
    "terminal_growth_g": 0.015,        # Crecimiento a perpetuidad g = 1,5%
}

# Parámetros CAPM para cálculo del WACC
CAPM_PARAMS = {
    "rf": 0.035,                       # Tasa libre de riesgo (Rf): 3,50%
    "beta": 1.20,                      # Beta apalancada (β): 1,20
    "erp": 0.055,                      # Prima de riesgo de mercado (ERP): 5,50%
    "specific_risk_premium": 0.014,    # Prima de riesgo específica/tamaño: 1,40%
    "kd_pre_tax": 0.0466666667,        # Coste de la deuda antes de impuestos (Kd): 4,667%
    "tax_rate": 0.25,                  # Tipo impositivo (t): 25,0%
    "debt_weight": 0.25,               # Peso de la deuda D/(D+E): 25,0%
    "equity_weight": 0.75,             # Peso del capital propio E/(D+E): 75,0%
}

def calculate_wacc(params=CAPM_PARAMS):
    ke = params["rf"] + params["beta"] * params["erp"] + params["specific_risk_premium"]
    kd_post_tax = params["kd_pre_tax"] * (1.0 - params["tax_rate"])
    wacc = params["equity_weight"] * ke + params["debt_weight"] * kd_post_tax
    return round(ke, 6), round(kd_post_tax, 6), round(wacc, 6)

KE_BASE, KD_POST_BASE, WACC_BASE = calculate_wacc()

# Drivers Operativos por Escenario
SCENARIOS_DATA = {
    "Pesimista": {
        "prob": 0.25,
        "vol_y1": 92000,
        "g_vol": 0.030,
        "p_y1": 24.00,
        "g_p": 0.015,
        "vc_pct": 0.620,
        "opex_y1": 470000,
        "g_opex": 0.020,
        "capex_y0": 880000,
        "capex_y1": 370000,
        "life_da": 5,
        "nwc_pct": 0.110,
        "g_terminal": 0.010,
        "wacc": 0.095,
    },
    "Base": {
        "prob": 0.50,
        "vol_y1": 100000,
        "g_vol": 0.050,
        "p_y1": 25.00,
        "g_p": 0.020,
        "vc_pct": 0.600,
        "opex_y1": 450000,
        "g_opex": 0.020,
        "capex_y0": 850000,
        "capex_y1": 350000,
        "life_da": 5,
        "nwc_pct": 0.100,
        "g_terminal": 0.015,
        "wacc": WACC_BASE,
    },
    "Optimista": {
        "prob": 0.25,
        "vol_y1": 110000,
        "g_vol": 0.070,
        "p_y1": 26.00,
        "g_p": 0.025,
        "vc_pct": 0.580,
        "opex_y1": 430000,
        "g_opex": 0.020,
        "capex_y0": 820000,
        "capex_y1": 330000,
        "life_da": 5,
        "nwc_pct": 0.090,
        "g_terminal": 0.020,
        "wacc": 0.095,
    }
}

# ==============================================================================
# 2. MOTOR DE PROYECCIÓN FINANCIERA DCF
# ==============================================================================

def project_dcf(drivers, include_terminal=False):
    """
    Calcula la cuenta de resultados simplificada, capital circulante y Flujo de Caja Libre (FCF)
    para los Años 0 a 5 según los drivers dados.
    """
    vol_y1 = drivers["vol_y1"]
    g_vol = drivers["g_vol"]
    p_y1 = drivers["p_y1"]
    g_p = drivers["g_p"]
    vc_pct = drivers["vc_pct"]
    opex_y1 = drivers["opex_y1"]
    g_opex = drivers["g_opex"]
    capex_y0 = drivers["capex_y0"]
    capex_y1 = drivers["capex_y1"]
    life_da = drivers["life_da"]
    nwc_pct = drivers["nwc_pct"]
    g_term = drivers.get("g_terminal", 0.015)
    wacc = drivers.get("wacc", WACC_BASE)
    tax_rate = HURDLE_POLICY["tax_rate"]

    years = list(range(6))
    volumes = [0]
    prices = [0.0]
    revenues = [0.0]
    var_costs = [0.0]
    gross_margins = [0.0]
    opex_fixed = [0.0]
    ebitda = [0.0]
    ebitda_margins = [0.0]
    depreciation = [0.0]
    ebit = [0.0]
    taxes = [0.0]
    nopat = [0.0]
    capex = [capex_y0, capex_y1, 0.0, 0.0, 0.0, 0.0]
    nwc = [0.0]
    delta_nwc = [0.0]
    fcf = [-capex_y0]
    discount_factors = [1.0]
    pv_fcf = [-capex_y0]

    total_capex = capex_y0 + capex_y1

    for t in range(1, 6):
        vt = vol_y1 * ((1.0 + g_vol) ** (t - 1))
        pt = p_y1 * ((1.0 + g_p) ** (t - 1))
        rev = vt * pt
        vc = rev * vc_pct
        gm = rev - vc
        op = opex_y1 * ((1.0 + g_opex) ** (t - 1))
        eb = gm - op
        eb_m = eb / rev if rev > 0 else 0.0
        
        # Amortización lineal: Año 1 tramo 1, Años 2-5 total acumulado
        da = (capex_y0 / life_da) if t == 1 else (total_capex / life_da)
        eb_val = eb - da
        tx = max(0.0, eb_val * tax_rate)
        nop = eb_val - tx
        
        nwc_val = rev * nwc_pct
        dnwc = nwc_val - nwc[t - 1]
        
        fcf_val = nop + da - capex[t] - dnwc
        disc_fact = 1.0 / ((1.0 + wacc) ** t)
        pv_val = fcf_val * disc_fact

        volumes.append(vt)
        prices.append(pt)
        revenues.append(rev)
        var_costs.append(vc)
        gross_margins.append(gm)
        opex_fixed.append(op)
        ebitda.append(eb)
        ebitda_margins.append(eb_m)
        depreciation.append(da)
        ebit.append(eb_val)
        taxes.append(tx)
        nopat.append(nop)
        nwc.append(nwc_val)
        delta_nwc.append(dnwc)
        fcf.append(fcf_val)
        discount_factors.append(disc_fact)
        pv_fcf.append(pv_val)

    # Flujos acumulados
    cum_fcf = []
    c = 0.0
    for x in fcf:
        c += x
        cum_fcf.append(c)

    cum_pv_fcf = []
    cpv = 0.0
    for x in pv_fcf:
        cpv += x
        cum_pv_fcf.append(cpv)

    # Terminal value Gordon Shapiro
    fcf_5 = fcf[5]
    if wacc > g_term:
        tv = fcf_5 * (1.0 + g_term) / (wacc - g_term)
        pv_tv = tv / ((1.0 + wacc) ** 5)
    else:
        tv = 0.0
        pv_tv = 0.0

    # NPV 5Y y 3Y
    npv_5y_core = cum_pv_fcf[5]
    npv_5y = npv_5y_core + (pv_tv if include_terminal else 0.0)
    npv_3y = cum_pv_fcf[3]

    # IRR (bisección de alta precisión)
    def calc_npv_at_rate(r):
        return sum(fcf[t] / ((1.0 + r) ** t) for t in range(6))

    irr = None
    try:
        low, high = -0.6, 5.0
        if calc_npv_at_rate(low) > 0 and calc_npv_at_rate(high) < 0:
            for _ in range(120):
                mid = (low + high) / 2.0
                if calc_npv_at_rate(mid) > 0:
                    low = mid
                else:
                    high = mid
            irr = (low + high) / 2.0
    except Exception:
        irr = None

    # MIRR
    r_reinv = HURDLE_POLICY["reinvestment_rate"]
    fv_inflows = sum(fcf[t] * ((1.0 + r_reinv) ** (5 - t)) for t in range(1, 6) if fcf[t] > 0)
    pv_outflows = abs(fcf[0] + sum(fcf[t] / ((1.0 + wacc) ** t) for t in range(1, 6) if fcf[t] < 0))
    if pv_outflows > 0 and fv_inflows > 0:
        mirr = (fv_inflows / pv_outflows) ** (1.0 / 5.0) - 1.0
    else:
        mirr = None

    # Profitability Index (PI)
    pv_future = sum(fcf[t] / ((1.0 + wacc) ** t) for t in range(1, 6) if fcf[t] > 0)
    pi = (pv_future / pv_outflows) if pv_outflows > 0 else 0.0

    # Peak Funding
    peak_funding = min(cum_fcf)

    # Payback Simple con interpolación lineal
    payback_simple = None
    for t in range(1, 6):
        if cum_fcf[t - 1] < 0 and cum_fcf[t] >= 0:
            payback_simple = (t - 1) + (-cum_fcf[t - 1] / fcf[t])
            break

    # Payback Descontado con interpolación lineal
    payback_discounted = None
    for t in range(1, 6):
        if cum_pv_fcf[t - 1] < 0 and cum_pv_fcf[t] >= 0:
            dfcf_t = fcf[t] / ((1.0 + wacc) ** t)
            payback_discounted = (t - 1) + (-cum_pv_fcf[t - 1] / dfcf_t)
            break

    # Veredicto Hurdle Policy
    min_irr_required = wacc + HURDLE_POLICY["hurdle_margin_pp"]
    max_pb = HURDLE_POLICY["max_discounted_payback_yrs"]

    if npv_5y > 0 and (irr is not None and irr >= min_irr_required) and (payback_discounted is not None and payback_discounted <= max_pb):
        decision = "APROBAR"
        decision_code = "APPROVE"
        decision_symbol = "✅ APROBAR"
        decision_symbol_en = "✅ APPROVE"
    elif npv_5y > 0:
        decision = "REVISAR"
        decision_code = "REVIEW"
        decision_symbol = "🟠 REVISAR"
        decision_symbol_en = "🟠 REVIEW"
    else:
        decision = "RECHAZAR"
        decision_code = "REJECT"
        decision_symbol = "⛔ RECHAZAR"
        decision_symbol_en = "⛔ REJECT"

    return {
        "years": years,
        "volumes": volumes,
        "prices": prices,
        "revenues": revenues,
        "var_costs": var_costs,
        "gross_margins": gross_margins,
        "opex_fixed": opex_fixed,
        "ebitda": ebitda,
        "ebitda_margins": ebitda_margins,
        "depreciation": depreciation,
        "ebit": ebit,
        "taxes": taxes,
        "nopat": nopat,
        "capex": capex,
        "nwc": nwc,
        "delta_nwc": delta_nwc,
        "fcf": fcf,
        "discount_factors": discount_factors,
        "pv_fcf": pv_fcf,
        "cum_fcf": cum_fcf,
        "cum_pv_fcf": cum_pv_fcf,
        "terminal_value": tv,
        "pv_terminal_value": pv_tv,
        "npv_5y": npv_5y,
        "npv_5y_core": npv_5y_core,
        "npv_3y": npv_3y,
        "irr": irr,
        "mirr": mirr,
        "pi": pi,
        "peak_funding": peak_funding,
        "payback_simple": payback_simple,
        "payback_discounted": payback_discounted,
        "decision": decision,
        "decision_code": decision_code,
        "decision_symbol": decision_symbol,
        "decision_symbol_en": decision_symbol_en,
        "wacc": wacc,
    }

# ==============================================================================
# 3. RESULTADOS DE LOS ESCENARIOS Y VAN ESPERADO
# ==============================================================================

PROJ_BASE = project_dcf(SCENARIOS_DATA["Base"])
PROJ_PES = project_dcf(SCENARIOS_DATA["Pesimista"])
PROJ_OPT = project_dcf(SCENARIOS_DATA["Optimista"])

EXPECTED_NPV = (
    SCENARIOS_DATA["Pesimista"]["prob"] * PROJ_PES["npv_5y"]
    + SCENARIOS_DATA["Base"]["prob"] * PROJ_BASE["npv_5y"]
    + SCENARIOS_DATA["Optimista"]["prob"] * PROJ_OPT["npv_5y"]
)

# ==============================================================================
# 4. MOTOR DE SENSIBILIDAD TORNADO Y PUNTOS DE EQUILIBRIO
# ==============================================================================

# Rango de perturbaciones univariables para los 8 drivers sobre el Escenario Base
TORNADO_DRIVERS_CONFIG = [
    {
        "id": "price",
        "name_es": "Precio Unitario (€/u)",
        "name_en": "Unit Price ($/unit)",
        "unit": "currency",
        "base_val": 25.00,
        "low_val": 21.00,       # -16%
        "high_val": 29.00,      # +16%
        "param_key": "p_y1",
    },
    {
        "id": "volume",
        "name_es": "Volumen Año 1 (unidades)",
        "name_en": "Year 1 Volume (units)",
        "unit": "integer",
        "base_val": 100000,
        "low_val": 85000,       # -15%
        "high_val": 115000,     # +15%
        "param_key": "vol_y1",
    },
    {
        "id": "var_cost",
        "name_es": "Coste Variable (% ventas)",
        "name_en": "Variable Cost (% sales)",
        "unit": "percent",
        "base_val": 0.600,
        "low_val": 0.550,       # Favorable: 55%
        "high_val": 0.650,      # Desfavorable: 65%
        "param_key": "vc_pct",
    },
    {
        "id": "capex",
        "name_es": "CAPEX Total (Tramo 1+2)",
        "name_en": "Total CAPEX (Tranche 1+2)",
        "unit": "currency",
        "base_val": 1200000,
        "low_val": 1020000,     # -15%
        "high_val": 1380000,    # +15%
        "param_key": "capex_total",
    },
    {
        "id": "opex",
        "name_es": "OPEX Fijo Anual (€)",
        "name_en": "Annual Fixed OPEX ($)",
        "unit": "currency",
        "base_val": 450000,
        "low_val": 380000,      # -70k€
        "high_val": 520000,     # +70k€
        "param_key": "opex_y1",
    },
    {
        "id": "g_vol",
        "name_es": "Crecimiento Volumen (%)",
        "name_en": "Volume Growth Rate (%)",
        "unit": "percent",
        "base_val": 0.050,
        "low_val": 0.020,       # -3 pp
        "high_val": 0.080,      # +3 pp
        "param_key": "g_vol",
    },
    {
        "id": "wacc",
        "name_es": "Tasa de Descuento (WACC)",
        "name_en": "Discount Rate (WACC)",
        "unit": "percent",
        "base_val": 0.095,
        "low_val": 0.075,       # -2 pp
        "high_val": 0.115,      # +2 pp
        "param_key": "wacc",
    },
    {
        "id": "nwc",
        "name_es": "Capital Circulante (% ventas)",
        "name_en": "Working Capital (% sales)",
        "unit": "percent",
        "base_val": 0.100,
        "low_val": 0.070,       # -3 pp
        "high_val": 0.130,      # +3 pp
        "param_key": "nwc_pct",
    },
]

def run_tornado_analysis():
    """Ejecuta el recálculo univariable para los 8 drivers sobre el Escenario Base."""
    base_npv = PROJ_BASE["npv_5y"]
    tornado_rows = []

    for item in TORNADO_DRIVERS_CONFIG:
        # Clonar drivers base
        d_low = dict(SCENARIOS_DATA["Base"])
        d_high = dict(SCENARIOS_DATA["Base"])

        if item["id"] == "capex":
            ratio_c1 = 850000 / 1200000
            ratio_c2 = 350000 / 1200000
            d_low["capex_y0"] = item["low_val"] * ratio_c1
            d_low["capex_y1"] = item["low_val"] * ratio_c2
            d_high["capex_y0"] = item["high_val"] * ratio_c1
            d_high["capex_y1"] = item["high_val"] * ratio_c2
        else:
            d_low[item["param_key"]] = item["low_val"]
            d_high[item["param_key"]] = item["high_val"]

        res_low = project_dcf(d_low)
        res_high = project_dcf(d_high)

        npv_val_low = res_low["npv_5y"]
        npv_val_high = res_high["npv_5y"]

        # Determinar cuál genera el impacto negativo (desfavorable) y positivo (favorable)
        # En variables de coste (var_cost, capex, opex, wacc, nwc), high_val genera menor VAN.
        # Para consistencia del Tornado:
        # delta_pessimistic = min(npv_val_low, npv_val_high) - base_npv (negativo)
        # delta_optimistic = max(npv_val_low, npv_val_high) - base_npv (positivo)
        delta_pessimistic = min(npv_val_low, npv_val_high) - base_npv
        delta_optimistic = max(npv_val_low, npv_val_high) - base_npv
        swing = abs(npv_val_high - npv_val_low)

        tornado_rows.append({
            "id": item["id"],
            "name_es": item["name_es"],
            "name_en": item["name_en"],
            "unit": item["unit"],
            "base_val": item["base_val"],
            "low_val": item["low_val"],
            "high_val": item["high_val"],
            "npv_at_low": npv_val_low,
            "npv_at_high": npv_val_high,
            "delta_pessimistic": delta_pessimistic,  # Rojo en Tornado (impacto negativo)
            "delta_optimistic": delta_optimistic,    # Verde en Tornado (impacto positivo)
            "swing": swing,
        })

    # Ordenar de mayor a menor amplitud (swing)
    tornado_rows.sort(key=lambda x: x["swing"], reverse=True)
    for rank, row in enumerate(tornado_rows, start=1):
        row["rank"] = rank

    return tornado_rows

TORNADO_RESULTS = run_tornado_analysis()

# ==============================================================================
# 5. PUNTOS DE EQUILIBRIO LINEALES (BREAK-EVEN POINTS: VAN = 0)
# ==============================================================================

def calculate_break_evens():
    """
    Calcula por interpolación lineal / búsqueda de raíces el valor del driver
    que hace VAN = 0 partiendo de la estructura del caso Base.
    """
    # 1. Break-even de Precio
    def npv_p(p):
        d = dict(SCENARIOS_DATA["Base"])
        d["p_y1"] = p
        return project_dcf(d)["npv_5y"]

    p_low, p_high = 15.0, 30.0
    for _ in range(60):
        p_mid = (p_low + p_high) / 2.0
        if npv_p(p_mid) < 0:
            p_low = p_mid
        else:
            p_high = p_mid
    be_price = (p_low + p_high) / 2.0
    be_price_drop_pct = (be_price - SCENARIOS_DATA["Base"]["p_y1"]) / SCENARIOS_DATA["Base"]["p_y1"]

    # 2. Break-even de Volumen
    def npv_v(v):
        d = dict(SCENARIOS_DATA["Base"])
        d["vol_y1"] = v
        return project_dcf(d)["npv_5y"]

    v_low, v_high = 40000, 120000
    for _ in range(60):
        v_mid = (v_low + v_high) / 2.0
        if npv_v(v_mid) < 0:
            v_low = v_mid
        else:
            v_high = v_mid
    be_volume = (v_low + v_high) / 2.0
    be_volume_drop_pct = (be_volume - SCENARIOS_DATA["Base"]["vol_y1"]) / SCENARIOS_DATA["Base"]["vol_y1"]

    # 3. Break-even de CAPEX (máximo sobrecoste soportable)
    def npv_c(tot):
        d = dict(SCENARIOS_DATA["Base"])
        r1 = 850000 / 1200000
        r2 = 350000 / 1200000
        d["capex_y0"] = tot * r1
        d["capex_y1"] = tot * r2
        return project_dcf(d)["npv_5y"]

    c_low, c_high = 1200000, 2500000
    for _ in range(60):
        c_mid = (c_low + c_high) / 2.0
        if npv_c(c_mid) > 0:
            c_low = c_mid
        else:
            c_high = c_mid
    be_capex = (c_low + c_high) / 2.0
    be_capex_increase_pct = (be_capex - 1200000) / 1200000

    return {
        "price": {
            "value": round(be_price, 2),
            "drop_pct": round(be_price_drop_pct, 4),
        },
        "volume": {
            "value": round(be_volume, 0),
            "drop_pct": round(be_volume_drop_pct, 4),
        },
        "capex": {
            "value": round(be_capex, 0),
            "increase_pct": round(be_capex_increase_pct, 4),
        }
    }

BREAK_EVEN_POINTS = calculate_break_evens()

# ==============================================================================
# 6. RESUMEN EJECUTIVO CONSOLIDADO
# ==============================================================================

SUMMARY = {
    "project_name_es": "Automatización y Digitalización de Línea de Producción",
    "project_name_en": "Production Line Automation & Digitalization",
    "sponsor": "COO & VP Industrial Operations",
    "cfo_advisor": "Datalaria Corporate Finance Practice",
    "wacc": WACC_BASE,
    "ke": KE_BASE,
    "kd_post_tax": KD_POST_BASE,
    "capex_total": 1200000,
    "capex_tranche_1": 850000,
    "capex_tranche_2": 350000,
    "npv_base": PROJ_BASE["npv_5y"],
    "npv_3y_base": PROJ_BASE["npv_3y"],
    "irr_base": PROJ_BASE["irr"],
    "mirr_base": PROJ_BASE["mirr"],
    "payback_simple_base": PROJ_BASE["payback_simple"],
    "payback_discounted_base": PROJ_BASE["payback_discounted"],
    "pi_base": PROJ_BASE["pi"],
    "peak_funding_base": PROJ_BASE["peak_funding"],
    "decision_base_es": PROJ_BASE["decision_symbol"],
    "decision_base_en": PROJ_BASE["decision_symbol_en"],
    "npv_pes": PROJ_PES["npv_5y"],
    "irr_pes": PROJ_PES["irr"],
    "payback_desc_pes": PROJ_PES["payback_discounted"],
    "npv_opt": PROJ_OPT["npv_5y"],
    "irr_opt": PROJ_OPT["irr"],
    "payback_desc_opt": PROJ_OPT["payback_discounted"],
    "npv_expected": EXPECTED_NPV,
    "break_even": BREAK_EVEN_POINTS,
    "tornado": TORNADO_RESULTS,
}

if __name__ == "__main__":
    print("=" * 80)
    print("DATALARIA | MODEL CORE DCF - VERIFICACIÓN NUMÉRICA")
    print("=" * 80)
    print(f"WACC: {SUMMARY['wacc']*100:.2f}% (Ke: {SUMMARY['ke']*100:.2f}%, Kd net: {SUMMARY['kd_post_tax']*100:.2f}%)")
    print(f"VAN Base (5 años): {SUMMARY['npv_base']:,.2f} €")
    print(f"VAN Base (3 años): {SUMMARY['npv_3y_base']:,.2f} €")
    print(f"TIR Base: {SUMMARY['irr_base']*100:.2f}%")
    print(f"MIRR Base: {SUMMARY['mirr_base']*100:.2f}%")
    print(f"Payback Simple: {SUMMARY['payback_simple_base']:.2f} años")
    print(f"Payback Descontado: {SUMMARY['payback_discounted_base']:.2f} años")
    print(f"Índice Rentabilidad (PI): {SUMMARY['pi_base']:.2f}x")
    print(f"Peak Funding: {SUMMARY['peak_funding_base']:,.2f} €")
    print(f"Dictamen: {SUMMARY['decision_base_es']}")
    print("-" * 80)
    print("ESCENARIOS:")
    print(f"• Pesimista (p=25%): VAN = {SUMMARY['npv_pes']:,.2f} € | TIR = {SUMMARY['irr_pes']*100:.2f}%")
    print(f"• Base      (p=50%): VAN = {SUMMARY['npv_base']:,.2f} € | TIR = {SUMMARY['irr_base']*100:.2f}%")
    print(f"• Optimista (p=25%): VAN = {SUMMARY['npv_opt']:,.2f} € | TIR = {SUMMARY['irr_opt']*100:.2f}%")
    print(f"• VAN Esperado Ponderado: {SUMMARY['npv_expected']:,.2f} €")
    print("-" * 80)
    print("PUNTOS DE EQUILIBRIO (BREAK-EVEN):")
    print(f"• Precio: {SUMMARY['break_even']['price']['value']:.2f} €/u (caída máx: {SUMMARY['break_even']['price']['drop_pct']*100:.1f}%)")
    print(f"• Volumen: {SUMMARY['break_even']['volume']['value']:,.0f} u (caída máx: {SUMMARY['break_even']['volume']['drop_pct']*100:.1f}%)")
    print(f"• CAPEX: {SUMMARY['break_even']['capex']['value']:,.0f} € (sobrecoste máx: +{SUMMARY['break_even']['capex']['increase_pct']*100:.1f}%)")
    print("-" * 80)
    print("RANKING TORNADO (Top drivers por amplitud / swing):")
    for r in SUMMARY['tornado']:
        print(f" {r['rank']}. {r['name_es']:<30} | Swing: {r['swing']:>10,.0f} € | ΔNeg: {r['delta_pessimistic']:>9,.0f} € | ΔPos: {r['delta_optimistic']:>9,.0f} €")
    print("=" * 80)
