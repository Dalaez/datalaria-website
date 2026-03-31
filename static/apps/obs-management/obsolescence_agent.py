import os
import sys
from dotenv import load_dotenv

# Forzar codificación UTF-8 para evitar crashes de emojis en terminal de Windows
sys.stdout.reconfigure(encoding='utf-8')

# Dependencias de Orquestación Agéntica
from crewai import Agent, Task, Crew, Process

# Herramientas del Ecosistema Relacional
from supabase_tools import calculate_financial_impact

# Configuración y anclaje de llaves
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY no encontrada. Abortando ejecución.")

# Asignación del Motor de Inferencia LLM (LiteLLM Format para CrewAI nativo)
llm_config = "gemini/gemini-2.5-flash"

# ==========================================
# 1. Definición del Agente Operativo
# ==========================================
analyst_agent = Agent(
    role="Senior Supply Chain Risk Analyst",
    goal="Identificar componentes en estado de obsolescencia según notificaciones de mercado, extrayendo la pieza e indexando su rastro destructivo contra nuestro P&L.",
    backstory="Eres un ingeniero de operaciones implacable y matemático. No asumes absolutamente nada ni alucinas información. Analizas datos. Siempre utilizas tus herramientas conectadas a las bases de datos vectoriales y relacionales para cruzar datos foráneos del mercado con el P&L financiero interno. Tu dialéctica es sobria, estricta y puramente técnica.",
    verbose=True,
    allow_delegation=False,
    llm=llm_config,
    tools=[calculate_financial_impact]
)

# ==========================================
# 2. Definición de la Tarea de Misión Crítica
# ==========================================
def execute_obsolescence_analysis(pdn_text: str):
    task = Task(
        description=f"""Analiza semánticamente el texto del siguiente Product Discontinuance Notice (PDN):
        
        '{pdn_text}'
        
        1. Localiza y extrae el Manufacturer Part Number (MPN).
        2. LUEGO, invoca excluyentemente tu herramienta de base de datos (`calculate_financial_impact`) pasando el MPN como argumento directo. No prosigas sin usar la herramienta.
        3. Recopila el string de impacto económico retornado por la base de datos (Euros expuestos, Productos bloqueados).
        4. Redacta el output.""",
        expected_output="Un informe ejecutivo corporativo (formato Markdown, 3 párrafos de máxima brevedad) para el CFO detallando: 1. El MPN afectado. 2. La cuantificación exacta del riesgo en euros y los SKU productivos bloqueados si no se emite una orden 'Last Time Buy'.",
        agent=analyst_agent
    )

    crew = Crew(
        agents=[analyst_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result

# ==========================================
# 3. Orquestador de Simulación (Runtime)
# ==========================================
if __name__ == "__main__":
    print("\n--- INICIALIZANDO NÚCLEO AGÉNTICO (OBSOLESCENCE RADAR) ---")
    
    # Simulamos el vector originario: Un correo de notificación de un Tier 1 (Texas Instruments)
    # Seleccionamos un MPN que sabemos que la pipeline de Python inyectó (TI-CAP-10U-50)
    mock_pdn_email = """
    *** TEXAS INSTRUMENTS - PRODUCT DISCONTINUANCE NOTICE (PDN) ***
    
    Dear Partner,
    
    This formal transmission serves as official notification that Texas Instruments will cease global production operations for the following device family due to legacy wafer fab shutdowns:
    
    Target Part Number: TI-CAP-10U-50
    Status: End of Life (EOL)
    Reason for Discontinuance: Legacy 150mm fabrication facility decommissioning.
    
    Last Time Buy (LTB) Order Window closes: October 2026.
    Final Ship Date: March 2027.
    
    Please assess your manufacturing buffers and issue purchase orders effectively.
    """
    
    try:
        final_assessment = execute_obsolescence_analysis(mock_pdn_email)
        
        print("\n\n" + "="*60)
        print("REPORTE EJECUTIVO FINAL (AUTORÍA: IA AGENT)")
        print("="*60 + "\n")
        print(final_assessment)
        
    except Exception as e:
        print(f"Fallo crítico en el pipeline de Inferencia: {e}")
        sys.exit(1)
