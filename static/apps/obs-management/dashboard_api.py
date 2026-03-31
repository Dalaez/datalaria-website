from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Executive Dashboard telemetry API", version="1.0.0")

# Permitir Fetch() desde el HTML local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
)

@app.get("/api/v1/dashboard/risk-metrics")
def get_risk_metrics():
    """
    Simula una consulta Read Replica a Supabase para poblar el frontend de mando del CFO/CTO.
    """
    return {
        "total_risk_eur": 15450.00,
        "active_alerts": 2,
        "affected_skus": [
            {
                "sku": "DRONE-X1",
                "margin_at_risk": 12500.00,
                "status": "CRITICAL LTB REQUIRED",
                "trigger_mpn": "TI-CAP-10U-50"
            },
            {
                "sku": "SERVER-RACK-9",
                "margin_at_risk": 2950.00,
                "status": "EVALUATING INVENTORY",
                "trigger_mpn": "STM32F405RGT6"
            }
        ],
        "agent_logs": [
            "[18:31:02] [Webhook] Inbound email parsed. Subject: EOL Notification TI-CAP-10U-50.",
            "[18:31:03] [CrewAI] Awakening 'Senior Risk Analyst' agent...",
            "[18:31:05] [CrewAI] Parsing semantic text. MPN extracted: TI-CAP-10U-50.",
            "[18:31:05] [Tool Calling] Executing calculate_financial_impact().",
            "[18:31:06] [Supabase SQL] Transversing bom_lines... Parent End_Product found: DRONE-X1.",
            "[18:31:07] [CrewAI] P&L calculated. Retained Margin at Risk: 12,500.00 EUR.",
            "[18:31:08] [FastAPI] Triggering Microsoft Teams outbound webhook alert.",
            "[18:32:14] [Webhook] Commercial API hit from SiliconExpert (Status: EOL).",
            "[18:32:15] [CrewAI] Parsing payload. MPN extracted: STM32F405RGT6.",
            "[18:32:16] [Supabase SQL] Transversing bom_lines... Parent End_Product found: SERVER-RACK-9.",
            "[18:32:18] [CrewAI] P&L calculated. Retained Margin at Risk: 2,950.00 EUR."
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
