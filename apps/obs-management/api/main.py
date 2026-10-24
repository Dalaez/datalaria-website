import os
import json
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
from obsolescence_agent import execute_obsolescence_analysis

app = FastAPI(
    title="Agentic Radar API", 
    version="1.0.0", 
    description="Central Nervous System for Supply Chain Obsolescence (Event-Driven Architecture)"
)

# === Modelos de Datos (Pydantic) ===
class CommercialAlert(BaseModel):
    alert_type: str
    mpn: str
    manufacturer: str

class InboundEmail(BaseModel):
    subject: str
    text: str

# === Closed-Loop Output ===
def notify_teams(message: str):
    """
    Simulates sending the final executive report to a Slack/MS Teams Webhook.
    """
    print("\n" + "="*60)
    print("🚀 [OUTBOUND WEBHOOK] ENVIANDO ALERTA A MS TEAMS / SLACK")
    print("="*60)
    print(message)
    print("="*60 + "\n")
    # if TEAMS_WEBHOOK_URL: httpx.post(url, json={"text": message})

# === Worker Asíncrono ===
def process_obsolescence_background(pdn_text: str):
    """
    Background Task: Executes the CrewAI agent synchronously in a separate thread so the HTTP response isn't blocked.
    """
    print(f"\n[BACKGROUND WORKER] Awakening CrewAI for PDN Analysis...")
    try:
        final_assessment = execute_obsolescence_analysis(pdn_text)
        
        # Cierre del Bucle: Notificar a Compras
        header = f"🚨 **Nueva Alerta de Obsolescencia Procesada por IA** 🚨\n\n"
        notify_teams(header + str(final_assessment))
        
    except Exception as e:
        print(f"[BACKGROUND RUNTIME ERROR]: {e}")

# === Endpoints / Enrutadores (FastAPI) ===
@app.post("/api/v1/webhooks/commercial-radar")
async def commercial_radar_webhook(alert: CommercialAlert, background_tasks: BackgroundTasks):
    """
    Vector 1: Ingesta JSONs limpios de herramientas B2B (ej. SiliconExpert, Accuris).
    """
    if alert.alert_type.upper() != "PDN":
        return {"status": "ignored", "message": "Only PDN alerts are processed"}
        
    # Construir un texto sintético estructurado para el Cerebro
    synthetic_pdn = f"Commercial API Notification. Manufacturer: {alert.manufacturer}. Target Part Number: {alert.mpn}. Status: EOL."
    
    # Delegar a CrewAI en segundo plano
    background_tasks.add_task(process_obsolescence_background, synthetic_pdn)
    
    # Retornar 200/202 Inmediatamente para evitar Timeout del Emisor
    return {"status": "accepted", "message": f"Alert for MPN {alert.mpn} queued for Agentic Radar processing."}

@app.post("/api/v1/webhooks/inbound-email")
async def inbound_email_webhook(email: InboundEmail, background_tasks: BackgroundTasks):
    """
    Vector 2: Ingesta correos raw (texto no estructurado) parseados por SendGrid/Mailgun Inbound Parse.
    """
    pdn_text = f"Subject: {email.subject}\nBody: {email.text}"
    
    background_tasks.add_task(process_obsolescence_background, pdn_text)
    
    return {"status": "accepted", "message": "Raw email queued for semantic extraction via Agentic Radar."}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
