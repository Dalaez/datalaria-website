import sys
import re

def update_posts():
    # 1. Update ES post
    es_path = 'content/es/posts/estrategia-corporativa-mba-framework-cuantitativo/index.md'
    with open(es_path, 'r', encoding='utf-8') as f:
        es_text = f.read().replace('\r\n', '\n')

    # Replace Tool 1 ASCII
    es_text = re.sub(
        r'```\s*\n={10,}\s*\nHERRAMIENTA 1: MATRIZ PESTEL CUANTITATIVA \(SEVERIDAD, VOLATILIDAD & INCERTIDUMBRE MACRO\)\s*\n={10,}\s*\n```',
        '---\n\n### 🌐 Herramienta 1: Matriz PESTEL Cuantitativa (Severidad, Volatilidad & Incertidumbre Macro)',
        es_text
    )

    # Replace Tool 2 ASCII
    es_text = re.sub(
        r'```\s*\n={10,}\s*\nHERRAMIENTA 2: 5 FUERZAS DE PORTER PONDERADAS \(ATRACTIVO INDUSTRIAL & ECONOMIC MOAT\)\s*\n={10,}\s*\n```',
        '---\n\n### 🛡️ Herramienta 2: 5 Fuerzas de Porter Ponderadas (Atractivo Industrial & Economic Moat)',
        es_text
    )

    # Replace Tool 3 ASCII
    es_text = re.sub(
        r'```\s*\n={10,}\s*\nHERRAMIENTA 3: DAFO CUANTITATIVO & MATRIZ CAME \(ESPACIO VECTORIAL & POSTURA TÁCTICA\)\s*\n={10,}\s*\n```',
        '---\n\n### 🎯 Herramienta 3: DAFO Cuantitativo & Matriz CAME (Espacio Vectorial & Postura Táctica)',
        es_text
    )

    # Replace Tool 4 ASCII
    es_text = re.sub(
        r'```\s*\n={10,}\s*\nHERRAMIENTA 4: MATRIZ BCG DINÁMICA \(EQUILIBRIO DE CARTERA & FLUJO DE FONDOS\)\s*\n={10,}\s*\n```',
        '---\n\n### ⭐ Herramienta 4: Matriz BCG Dinámica (Equilibrio de Cartera & Flujo de Fondos)',
        es_text
    )

    # Replace Tool 5 ASCII
    es_text = re.sub(
        r'```\s*\n={10,}\s*\nHERRAMIENTA 5: MATRIZ MCKINSEY / GE 3x3 \(ASIGNACIÓN MULTICRITERIO DE CAPITAL & ROIC\)\s*\n={10,}\s*\n```',
        '---\n\n### 🧭 Herramienta 5: Matriz McKinsey / GE 3x3 (Asignación Multicriterio de Capital & ROIC)',
        es_text
    )

    # Remove duplicate bundle-card in Section 6 if product-card is already present
    # Check if bundle-card is right after product-card in Section 6
    duplicate_bundle_es = r'(\{\{<\s*/product-card\s*>\}\}\s*\n\s*\{\{<\s*bundle-card.*?highlight="true"\s*\n>\}\})'
    match_dup_es = re.search(duplicate_bundle_es, es_text, re.DOTALL)
    if match_dup_es:
        es_text = re.sub(duplicate_bundle_es, '{{< /product-card >}}', es_text)
        print("Removed duplicate bundle-card in ES post!")

    with open(es_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(es_text)
    print("ES post updated successfully!")

    # 2. Update EN post
    en_path = 'content/en/posts/corporate-strategy-mba-quantitative-framework/index.md'
    with open(en_path, 'r', encoding='utf-8') as f:
        en_text = f.read().replace('\r\n', '\n')

    # Replace Tool 1 ASCII
    en_text = re.sub(
        r'```\s*\n={10,}\s*\nTOOL 1: QUANTITATIVE PESTEL MATRIX \(SEVERITY, VOLATILITY & MACRO UNCERTAINTY\)\s*\n={10,}\s*\n```',
        '---\n\n### 🌐 Tool 1: Quantitative PESTEL Matrix (Macro Severity, Volatility & Uncertainty)',
        en_text
    )

    # Replace Tool 2 ASCII
    en_text = re.sub(
        r'```\s*\n={10,}\s*\nTOOL 2: WEIGHTED PORTER\'S FIVE FORCES \(INDUSTRY ATTRACTIVENESS & ECONOMIC MOAT\)\s*\n={10,}\s*\n```',
        '---\n\n### 🛡️ Tool 2: Weighted Porter\'s 5 Forces (Industry Attractiveness & Economic Moat)',
        en_text
    )

    # Replace Tool 3 ASCII
    en_text = re.sub(
        r'```\s*\n={10,}\s*\nTOOL 3: QUANTITATIVE SWOT-TOWS MATRIX \(CARTESIAN SPACE & TACTICAL POSTURE\)\s*\n={10,}\s*\n```',
        '---\n\n### 🎯 Tool 3: Quantitative SWOT-TOWS Matrix (Cartesian Space & Tactical Posture)',
        en_text
    )

    # Replace Tool 4 ASCII
    en_text = re.sub(
        r'```\s*\n={10,}\s*\nTOOL 4: DYNAMIC BCG MATRIX \(PORTFOLIO CASH FLOW BALANCING & EXPERIENCE CURVE\)\s*\n={10,}\s*\n```',
        '---\n\n### ⭐ Tool 4: Dynamic BCG Matrix (Portfolio Cash Flow Balancing & Experience Curve)',
        en_text
    )

    # Replace Tool 5 ASCII
    en_text = re.sub(
        r'```\s*\n={10,}\s*\nTOOL 5: MCKINSEY / GE 3x3 MATRIX \(MULTICRITERIA CAPITAL ALLOCATION & ROIC MAXIMIZATION\)\s*\n={10,}\s*\n```',
        '---\n\n### 🧭 Tool 5: McKinsey / GE 3x3 Matrix (Multicriteria Capital Allocation & ROIC Maximization)',
        en_text
    )

    # Remove duplicate bundle-card in Section 6
    duplicate_bundle_en = r'(\{\{<\s*/product-card\s*>\}\}\s*\n\s*\{\{<\s*bundle-card.*?highlight="true"\s*\n>\}\})'
    match_dup_en = re.search(duplicate_bundle_en, en_text, re.DOTALL)
    if match_dup_en:
        en_text = re.sub(duplicate_bundle_en, '{{< /product-card >}}', en_text)
        print("Removed duplicate bundle-card in EN post!")

    with open(en_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(en_text)
    print("EN post updated successfully!")


if __name__ == '__main__':
    update_posts()
