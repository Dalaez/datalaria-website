#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
index_post_diagrams.py
======================
Indexa las 3 imágenes de diagramas y la portada en los artículos index.md
tanto en español como en inglés, agregando:
1. Metadatos cover e images en el frontmatter.
2. Bloques <noscript> con imágenes PNG semánticas bajo cada diagrama Mermaid.
"""

def update_es():
    path = 'content/es/posts/matriz-rice-ice-priorizacion/index.md'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Frontmatter
    fm_target = 'summary: "Sustituye la priorización por intuición (síndrome HiPPO) y la \'fábrica de funcionalidades\' por un motor cuantitativo defendible ante Consejos de Administración y Comités de Producto. Combina la puntuación estructural RICE de Intercom con el framework ágil de experimentación ICE de Growth, una matriz cartesiana 2x2 de cuadrantes estratégicos y una línea de corte automática ajustada a la capacidad neta de ingeniería en persona-mes."'
    
    fm_repl = fm_target + """
cover:
  image: "cover.png"
  alt: "Matriz RICE & ICE de Priorización Ágil: Backlog Cuantitativo, Matriz Impacto vs. Esfuerzo y Línea de Corte de Capacidad"
  caption: "Matriz RICE & ICE Ágil: Motor de priorización cuantitativa, calibración bayesiana, matriz de cuadrantes 2x2 y línea de corte de capacidad para Comités de Producto C-Level."
  relative: true
images:
  - "cover.png"
  - "diagrama-1-embudo-decisiones.png"
  - "diagrama-2-flujo-priorizacion-rice.png"
  - "diagrama-3-matriz-impacto-esfuerzo.png"
  - "preview-pack.png\""""

    if 'diagrama-1-embudo-decisiones.png' not in content:
        if fm_target in content:
            content = content.replace(fm_target, fm_repl)
            print('[OK] ES Frontmatter updated with cover & images.')
        else:
            print('[WARN] ES Frontmatter target not matched!')

    # 2. Mermaid 1
    m1_target = """    style S6 fill:#0F172A,stroke:#2563EB,stroke-width:2.5px,color:#FFFFFF
{{< /mermaid >}}"""
    m1_repl = """    style S6 fill:#0F172A,stroke:#2563EB,stroke-width:2.5px,color:#FFFFFF
{{< /mermaid >}}
<noscript>
  <p align="center">
    <img src="diagrama-1-embudo-decisiones.png" alt="Diagrama 1: Embudo Estratégico Integral (De Suite 01 Estrategia a Suite 02 Decisiones)" width="100%" />
  </p>
</noscript>"""

    if 'alt="Diagrama 1: Embudo Estratégico' not in content and m1_target in content:
        content = content.replace(m1_target, m1_repl)
        print('[OK] ES Diagram 1 indexed.')

    # 3. Mermaid 2
    m2_target = """    style I fill:#D1FAE5,stroke:#10B981,stroke-width:2.5px,color:#065F46
{{< /mermaid >}}"""
    m2_repl = """    style I fill:#D1FAE5,stroke:#10B981,stroke-width:2.5px,color:#065F46
{{< /mermaid >}}
<noscript>
  <p align="center">
    <img src="diagrama-2-flujo-priorizacion-rice.png" alt="Diagrama 2: Pipeline de Priorización Cuantitativa de Producto (6 Fases Secuenciales)" width="100%" />
  </p>
</noscript>"""

    if 'alt="Diagrama 2: Pipeline de Priorización' not in content and m2_target in content:
        content = content.replace(m2_target, m2_repl)
        print('[OK] ES Diagram 2 indexed.')

    # 4. Mermaid 3
    m3_target = """  "INIT-19 DB Rust Rewrite": [0.95, 0.12]
{{< /mermaid >}}"""
    m3_repl = """  "INIT-19 DB Rust Rewrite": [0.95, 0.12]
{{< /mermaid >}}
<noscript>
  <p align="center">
    <img src="diagrama-3-matriz-impacto-esfuerzo.png" alt="Diagrama 3: Matriz Estratégica: Valor Esperado vs. Esfuerzo & Distribución Cartesiana" width="100%" />
  </p>
</noscript>"""

    if 'alt="Diagrama 3: Matriz Estratégica' not in content and m3_target in content:
        content = content.replace(m3_target, m3_repl)
        print('[OK] ES Diagram 3 indexed.')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('[OK] ES index.md saved successfully.')


def update_en():
    path = 'content/en/posts/rice-ice-prioritization-matrix/index.md'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Frontmatter
    fm_target = 'summary: "Replace intuition-based prioritization (HiPPO syndrome) and the \'feature factory\' with a defensible quantitative engine tailored for Corporate Boards and Executive Product Councils. Combines Intercom\'s foundational RICE score with the high-velocity ICE growth framework, an objective 2x2 strategic quadrant matrix, and an automated capacity cut-line anchored in real engineering person-months."'
    
    fm_repl = fm_target + """
cover:
  image: "cover.png"
  alt: "Agile RICE & ICE Prioritization Matrix: Quantitative Backlog, Impact vs. Effort Matrix & Capacity Cut-Line"
  caption: "Agile RICE & ICE Matrix: Quantitative prioritization engine, Bayesian calibration, 2x2 quadrant matrix, and net squad capacity cut-line for C-Level Product Councils."
  relative: true
images:
  - "cover.png"
  - "diagram-1-decision-funnel.png"
  - "diagram-2-rice-prioritization-pipeline.png"
  - "diagram-3-impact-effort-matrix.png"
  - "preview-pack.png\""""

    if 'cover:' not in content:
        if fm_target in content:
            content = content.replace(fm_target, fm_repl)
            print('[OK] EN Frontmatter updated with cover & images.')
        else:
            print('[WARN] EN Frontmatter target not matched!')

    # 2. Mermaid 1
    m1_target = """    style S6 fill:#0F172A,stroke:#2563EB,stroke-width:2.5px,color:#FFFFFF
{{< /mermaid >}}"""
    m1_repl = """    style S6 fill:#0F172A,stroke:#2563EB,stroke-width:2.5px,color:#FFFFFF
{{< /mermaid >}}
<noscript>
  <p align="center">
    <img src="diagram-1-decision-funnel.png" alt="Diagram 1: Strategic Decision Funnel (From Suite 01 Strategy to Suite 02 Decisions)" width="100%" />
  </p>
</noscript>"""

    if 'alt="Diagram 1: Strategic Decision Funnel' not in content and m1_target in content:
        content = content.replace(m1_target, m1_repl)
        print('[OK] EN Diagram 1 indexed.')

    # 3. Mermaid 2
    m2_target = """    style I fill:#D1FAE5,stroke:#10B981,stroke-width:2.5px,color:#065F46
{{< /mermaid >}}"""
    m2_repl = """    style I fill:#D1FAE5,stroke:#10B981,stroke-width:2.5px,color:#065F46
{{< /mermaid >}}
<noscript>
  <p align="center">
    <img src="diagram-2-rice-prioritization-pipeline.png" alt="Diagram 2: Quantitative Product Prioritization Pipeline (6 Sequential Phases)" width="100%" />
  </p>
</noscript>"""

    if 'alt="Diagram 2: Quantitative Product Prioritization' not in content and m2_target in content:
        content = content.replace(m2_target, m2_repl)
        print('[OK] EN Diagram 2 indexed.')

    # 4. Mermaid 3
    m3_target = """  "INIT-19 DB Rust Rewrite": [0.95, 0.12]
{{< /mermaid >}}"""
    m3_repl = """  "INIT-19 DB Rust Rewrite": [0.95, 0.12]
{{< /mermaid >}}
<noscript>
  <p align="center">
    <img src="diagram-3-impact-effort-matrix.png" alt="Diagram 3: Strategic Matrix: Expected Value vs. Effort & Cartesian Backlog Distribution" width="100%" />
  </p>
</noscript>"""

    if 'alt="Diagram 3: Strategic Matrix' not in content and m3_target in content:
        content = content.replace(m3_target, m3_repl)
        print('[OK] EN Diagram 3 indexed.')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('[OK] EN index.md saved successfully.')


if __name__ == '__main__':
    update_es()
    update_en()
