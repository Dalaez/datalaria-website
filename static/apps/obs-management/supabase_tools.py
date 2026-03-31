import os
from typing import Dict, Any
from dotenv import load_dotenv
from supabase import create_client, Client
from crewai.tools import tool

# Cargar configuración desde el entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan credenciales de Supabase en el entorno.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@tool
def calculate_financial_impact(mpn: str) -> str:
    """Useful to calculate the financial impact on the P&L when a component Manufacturer Part Number (MPN) becomes obsolete. Input must be the MPN string."""
    
    # Estandarizamos el input para maximizar el match
    mpn_clean = mpn.strip().upper()
    
    # 1. Validar existencia del componente en el radar de inteligencia externa
    m_parts = supabase.table('manufacturer_parts').select('mpn').eq('mpn', mpn_clean).execute()
    if not m_parts.data:
        return f"MPN '{mpn}' no encontrado en la base de datos interna. Cero impacto."
        
    # 2. Atravesar el Firewall AML: Localizar el equivalente interno
    aml_records = supabase.table('aml').select('internal_pn').eq('manufacturer_pn', mpn_clean).execute()
    if not aml_records.data:
        return f"MPN '{mpn}' carece de vínculo activo en la Approved Manufacturer List (AML). Cero impacto."
        
    internal_ids = [record['internal_pn'] for record in aml_records.data]
    affected_products: Dict[str, Dict[str, Any]] = {}
    
    # 3. Músculo Matemático: Recorrer el grafo jerárquico bidireccional
    def find_parent_products(child_id: str):
        # Localizamos el nodo hijo en el grafo (bom_lines)
        bom_records = supabase.table('bom_lines').select('parent_product_id', 'parent_assembly_id').eq('child_pn', child_id).execute()
        
        for record in bom_records.data:
            prod_id = record['parent_product_id']
            asm_id = record['parent_assembly_id']
            
            if prod_id:
                # Atravesamos hacia un Producto Final de Nivel 0
                if prod_id not in affected_products:
                    p_data = supabase.table('products').select('sku', 'name', 'gross_margin').eq('id', prod_id).execute()
                    if p_data.data:
                        affected_products[prod_id] = p_data.data[0]
            elif asm_id:
                # Nodo intermedio: Encontramos un subensamblaje. Invocación iterativa para seguir ascendiendo el nivel
                find_parent_products(asm_id)

    # 4. Lanzar la recursividad por cada internal PN cruzado
    for i_id in internal_ids:
        find_parent_products(i_id)
        
    # 5. Estructurar y cuantificar el P&L Impact
    if not affected_products:
        return f"El MPN '{mpn}' existe internamente, pero carece de dependencias en Productos Activos. Riesgo cero."
        
    total_risk = sum(float(prod['gross_margin']) for prod in affected_products.values())
    
    product_details = [f"{prod['sku']} (Margen Expuesto: {prod['gross_margin']}€)" for prod in affected_products.values()]
    product_list_str = ", ".join(product_details)
    
    # Extraemos un PN interno en formato string limpio (solo info)
    internal_pn_str = str(internal_ids[0]) if internal_ids else "N/A"
    
    # Respuesta ejecutiva estructurada para la digestión del LLM
    return f"El MPN {mpn} (Hash interno: {internal_pn_str}) detendrá la cadena de suministro de: [{product_list_str}]. Riesgo financiero bloqueante consolidado: {total_risk}€."
