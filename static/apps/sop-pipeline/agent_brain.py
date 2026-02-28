"""
Agent Brain para CrewAI - S&OP Autonomous Copilot
==================================================
Script de orquestacion que configura el LLM, ensambla 
la Crew con 2 agentes (Analista y Director de Planta) 
e inicia la ejecucion autonoma de la Tarea 1 y 2.
"""

import os
import sys
from pathlib import Path

# Cargar .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

# Verificar API Keys basicas antes de importar librerias pesadas
if not os.environ.get("OPENAI_API_KEY") and not os.environ.get("GEMINI_API_KEY"):
    print("CRITICAL ERROR: No se ha encontrado OPENAI_API_KEY ni GEMINI_API_KEY en el archivo .env.")
    print("El Copilot necesita un proveedor de LLM para pensar.")
    sys.exit(1)

try:
    from crewai import Agent, Task, Crew, Process
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    print("CRITICAL ERROR: Libreria 'crewai' o 'langchain-google-genai' no encontrada.")
    print("Instala las dependencias: pip install crewai langchain-google-genai")
    sys.exit(1)

# Importar nuestras herramientas personalizadas
try:
    from db_tools import fetch_latest_supply_plan
except ImportError:
    print("CRITICAL ERROR: No se pudo importar 'db_tools.py'. Asegurate de que esta en el mismo directorio.")
    sys.exit(1)


def main():
    print("==================================================")
    print("  INICIANDO S&OP AUTONOMOUS COPILOT (CREW-AI)")
    print("==================================================\n")
    
    # ─── CONFIGURACION DEL LLM (Gemini) ─────────────────
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )
    
    # ─── AGENTE 1: Senior Supply Chain Analyst ──────────
    analyst_agent = Agent(
        role='Senior Supply Chain Analyst',
        goal='Analizar el plan maestro de produccion y detectar cuellos de botella y riesgos de inventario.',
        backstory=(
            "Eres un analista implacable que busca la eficiencia del capital. "
            "Odias el exceso de inventario porque inmoviliza el dinero de la empresa, "
            "pero temes las roturas de stock. Tienes un ojo clinico para detectar "
            "meses donde la produccion no da abasto para cubrir la demanda y hay que usar el Safety Stock."
        ),
        verbose=True,
        allow_delegation=False,
        tools=[fetch_latest_supply_plan],
        llm=gemini_llm
    )

    # ─── AGENTE 2: Procurement & Plant Manager ──────────
    plant_manager_agent = Agent(
        role='Procurement & Plant Manager',
        goal='Redactar correos electronicos ejecutables y justificados a la fabrica.',
        backstory=(
            "Eres un director de operaciones senior. Te comunicas de forma directa, "
            "profesional y rigurosa. Detestas la teoria; necesitas instrucciones claras "
            "y ejecutables (cantidades exactas y fechas límite). JUSTIFICAS matemáticamente "
            "por qué la fábrica debe producir esas cantidades basándote en la capacidad "
            "pre-calculada por el plan."
        ),
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )

    # ─── TAREA 1: Analisis Critico ──────────────────────
    analyze_plan_task = Task(
        description=(
            "1. Llama a la herramienta para leer el Supply Plan de los proximos 3 meses de la base de datos.\n"
            "2. Analiza los resultados: ¿Qué SKU tiene la demanda mas alta? ¿Hay algun mes "
            "donde el inventario baje criticamente cerca del Safety Stock de los productos?\n"
            "3. Identifica claramente en que mes la fabrica va a sufrir el mayor nivel de estres "
            "basado en los volumenes de produccion solicitados.\n"
            "4. Escribe un resumen analitico ejecutivo (max 300 palabras) para entregarle al Director de Planta."
        ),
        expected_output="Un documento de análisis ejecutivo con los riesgos de rotura, SKUs problemáticos y los niveles de producción esperados para el próximo trimestre.",
        agent=analyst_agent
    )

    # ─── TAREA 2: Redaccion Orden Ejecutiva ─────────────
    draft_email_task = Task(
        description=(
            "Basándote EXCLUSIVAMENTE en el analisis proporcionado por el Senior Supply Chain Analyst:\n"
            "1. Redacta un borrador de email (en espanol profesional) dirigido a 'Direccion de Planta de Produccion'.\n"
            "2. El asunto del correo debe incluir el nivel de urgencia adecuado basado en el stress detectado.\n"
            "3. En el cuerpo, explica clara y numericamente que debe fabricar la planta en los proximos 3 meses.\n"
            "4. Justifica la peticion mencionando que el plan esta optimizado matematicamente para manejar la "
            "restriccion de capacidad, y que no se pueden desviar de los volumenes indicados.\n"
            "5. NO inventes numeros que no esten en el analisis."
        ),
        expected_output="Borrado del email en texto listo para ser copiado y enviado, con un tono urgente y estrictamente analítico.",
        agent=plant_manager_agent
    )

    # ─── CREW ENSAMBLAJE Y EJECUCION ────────────────────
    sop_crew = Crew(
        agents=[analyst_agent, plant_manager_agent],
        tasks=[analyze_plan_task, draft_email_task],
        process=Process.sequential,
        verbose=True
    )

    # Ejecutar!
    print(">> Despertando a los agentes e iniciando lectura de base de datos...\n")
    try:
        result = sop_crew.kickoff()
        
        print("\n\n==================================================")
        print("  RESULTADO FINAL (BORRADOR DEL EMAIL)")
        print("==================================================")
        print(result)
        
    except Exception as e:
        print(f"\nCRITICAL ERROR durante la ejecucion del Crew: {str(e)}")


if __name__ == "__main__":
    main()
