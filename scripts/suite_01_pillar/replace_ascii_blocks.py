import re
import os

def update_es():
    path = 'content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/index.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\r\n', '\n')

    # 1. Replace ASCII flowchart with Mermaid flowchart
    m1_pattern = r'```\n\[ PESTEL Cuantitativo \].*?\[ Presupuesto Corporativo & Consejo de Administración \]\n```'
    mermaid_es = """{{< mermaid >}}
flowchart TD
    P["<b>1. Matriz PESTEL Cuantitativa</b><br>Volatilidad macroeconómica (V), severidad (S) y resiliencia (RES_macro)"]
    PO["<b>2. 5 Fuerzas de Porter Ponderadas</b><br>Intensidad competitiva (I_comp), atractivo industrial (A_ind) y Moat (M)"]
    D["<b>3. DAFO-CAME Vectorial</b><br>Fuerzas sectoriales calibran Amenazas/Oportunidades; vector V(X,Y) y CAME 40×40"]
    B["<b>4. Matriz BCG Dinámica</b><br>Curva de experiencia y equilibrio neto de fondos (BNF): las Vacas financian el CAPEX"]
    M["<b>5. Matriz McKinsey / GE 3x3</b><br>I_A (Porter/PESTEL) × F_C (DAFO/BCG) en 9 cajas (T1=2.33, T2=3.67) → CAPEX"]
    C["<b>Presupuesto Corporativo & Consejo de Administración</b><br>Plan de asignación de capital auditado, financiado y con ROIC > WACC"]

    P --> PO
    PO --> D
    D --> B
    B --> M
    M --> C

    style P fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style PO fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style D fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style B fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style M fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style C fill:#1E293B,stroke:#10B981,stroke-width:2px,color:#FFFFFF
{{< /mermaid >}}"""
    
    text, n1 = re.subn(m1_pattern, mermaid_es, text, flags=re.DOTALL)
    print(f"ES: Replaced flowchart {n1} times")

    # 2. Replace ASCII box with C-Level section header
    m2_pattern = r'```\n\+[\u2500\-+]+\n\|[^\n]*RECORRIDO SECUENCIAL[^\n]*\|\n\+[\u2500\-+]+\n```'
    header_es = """---

### 🚀 Recorrido Secuencial del Framework en Grupo Vanguardia

A continuación, recorremos la aplicación cuantitativa de las 5 herramientas sobre las cuatro divisiones del grupo:"""
    
    text, n2 = re.subn(m2_pattern, header_es, text)
    print(f"ES: Replaced header box {n2} times")

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print("ES post updated successfully!")

def update_en():
    path = 'content/en/posts/corporate-strategy-mba-quantitative-framework/index.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\r\n', '\n')

    # 1. Replace ASCII flowchart with Mermaid flowchart
    m1_pattern = r'```\n\[ Quantitative PESTEL \].*?\[ Corporate Budget & Boardroom Decision Gateway \]\n```'
    mermaid_en = """{{< mermaid >}}
flowchart TD
    P["<b>1. Quantitative PESTEL Matrix</b><br>Macro volatility (V), severity (S), and resilience (RES_macro)"]
    PO["<b>2. Weighted Porter's 5 Forces</b><br>Competitive intensity (I_comp), industry attractiveness (A_ind), and Moat (M)"]
    D["<b>3. Quantitative SWOT-TOWS</b><br>Industry forces calibrate Threats/Opportunities; Cartesian vector V(X,Y) & TOWS 40×40"]
    B["<b>4. Dynamic BCG Matrix</b><br>Experience curve & net fund balance (BNF): Cash Cows finance CAPEX"]
    M["<b>5. McKinsey / GE 3x3 Matrix</b><br>I_A (Porter/PESTEL) × F_C (SWOT/BCG) in 9 boxes (T1=2.33, T2=3.67) → CAPEX"]
    C["<b>Corporate Budget & Boardroom Decision Gateway</b><br>Fully funded, risk-audited capital allocation plan with group ROIC > WACC"]

    P --> PO
    PO --> D
    D --> B
    B --> M
    M --> C

    style P fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style PO fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style D fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style B fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style M fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF
    style C fill:#1E293B,stroke:#10B981,stroke-width:2px,color:#FFFFFF
{{< /mermaid >}}"""
    
    text, n1 = re.subn(m1_pattern, mermaid_en, text, flags=re.DOTALL)
    print(f"EN: Replaced flowchart {n1} times")

    # 2. Replace ASCII box with C-Level section header
    m2_pattern = r'```\n\+[\u2500\-+]+\n\|[^\n]*SEQUENTIAL FRAMEWORK EXECUTION[^\n]*\|\n\+[\u2500\-+]+\n```'
    header_en = """---

### 🚀 Sequential Framework Execution at Vanguard Group

The following section details the end-to-end execution of the five quantitative tools across Vanguard Group's portfolio:"""
    
    text, n2 = re.subn(m2_pattern, header_en, text)
    print(f"EN: Replaced header box {n2} times")

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print("EN post updated successfully!")

if __name__ == '__main__':
    update_es()
    update_en()
