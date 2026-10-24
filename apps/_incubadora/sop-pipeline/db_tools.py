"""
Database Tools para CrewAI - S&OP Autonomous Copilot
======================================================
Proporciona herramientas a los agentes para leer datos 
optimizados de Supabase.
"""

import os
import json
from datetime import date
from typing import Optional, List, Dict, Any
from pathlib import Path

# CrewAI Tool decorator
try:
    from crewai.tools import tool
except ImportError:
    # Fallback to langchain tool for compatibility if needed
    from langchain.tools import tool

# Supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

# Cargar .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

@tool("fetch_latest_supply_plan")
def fetch_latest_supply_plan() -> str:
    """
    Se conecta a la base de datos, busca la ejecucion mas 
    reciente del plan de produccion optimizado (tabla supply_plans) 
    y extrae el plan estrategico de los proximos 3 meses para 
    todos los SKUs. Devuelve un informe formateado en Markdown.
    
    Esta herramienta DEBE ser usada por el Supply Chain Analyst 
    para tomar decisiones operativas.
    """
    if not SUPABASE_AVAILABLE:
        return "ERROR: Libreria 'supabase' no esta instalada. Ejecuta 'pip install supabase'."

    supabase_url: Optional[str] = os.environ.get("SUPABASE_URL")
    supabase_key: Optional[str] = os.environ.get("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        return "ERROR: Credenciales de Supabase no encontradas en el entorno (.env)."

    try:
        # 1. Conexion
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # 2. Buscar ejecucion mas reciente
        latest = (
            supabase
            .table("supply_plans")
            .select("execution_date")
            .order("execution_date", desc=True)
            .limit(1)
            .execute()
        )
        
        if not latest.data:
            return "AVISO: No hay planes de suministro en la base de datos."
            
        exec_date: str = latest.data[0]["execution_date"]
        
        # 3. Extraer el plan (filtrado y ordenado)
        response = (
            supabase
            .table("supply_plans")
            .select("plan_date, sku, demand_forecast, production_qty, inventory_level, safety_stock_target")
            .eq("execution_date", exec_date)
            .order("plan_date")
            .order("sku")
            .execute()
        )
        
        if not response.data:
            return f"ERROR: No se encontraron registros para execution_date={exec_date}"
            
        # 4. Procesamiento: Filtrar solo los primeros 3 meses unicos por SKU
        data = response.data
        
        # Agrupar por SKU para filtrar meses
        sku_plans: Dict[str, List[Dict[str, Any]]] = {}
        unique_dates: set = set()
        
        for row in data:
            sku = row["sku"]
            unique_dates.add(row["plan_date"])
            if sku not in sku_plans:
                sku_plans[sku] = []
            sku_plans[sku].append(row)
            
        # Ordenar fechas para sacar las 3 primeras (los proximos 3 meses)
        top_3_dates = sorted(list(unique_dates))[:3]
        
        # 5. Formatear la salida para el LLM en Markdown
        report = f"# S&OP Supply Master Plan\n"
        report += f"**Execution Date:** {exec_date}\n"
        report += f"**Horizon:** Proximos 3 meses ({top_3_dates[0]} al {top_3_dates[-1]})\n\n"
        
        for sku, rows in sku_plans.items():
            report += f"## {sku}\n"
            report += "| Mes | Demanda (Ud) | Produccion (Ud) | Inventario Final | Safety Stock (Ud) |\n"
            report += "|-----|--------------|-----------------|------------------|-------------------|\n"
            
            for row in rows:
                if row["plan_date"] in top_3_dates:
                    pd = row['plan_date']
                    dem = int(row['demand_forecast'])
                    prod = int(row['production_qty'])
                    inv = int(row['inventory_level'])
                    ss = int(row['safety_stock_target'])
                    
                    report += f"| {pd} | {dem:,} | **{prod:,}** | {inv:,} | {ss:,} |\n"
            report += "\n"
            
        report += "\n**NOTA PARA EL ANALISTA**: El inventario final es mensual. Fijate especialmente en los meses donde la demanda supera la capacidad compartida o el inventario roza el Safety Stock."
            
        return report

    except Exception as e:
        return f"CRITICAL ERROR accediendo a la base de datos: {str(e)}"
