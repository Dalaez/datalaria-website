#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_headings_alignment.py
=========================
Alinea estrictamente la numeración jerárquica de secciones (## N.) y
subsecciones (### N.M.) en los artículos de la Matriz RICE & ICE
tanto en español como en inglés:

Sección 1:
- ## 1.
- ### 1.1.
- ### 1.2.
- ### 1.3.

Sección 2:
- ## 2.

Sección 3:
- ## 3.
- ### 3.1.
- ### 3.2.
- ### 3.3.
- ### 3.4.
- ### 3.5.

Sección 4:
- ## 4.
- ### 4.1.

Sección 5:
- ## 5.
- ### 5.1.
- ### 5.2.
- ### 5.3.

Sección 6:
- ## 6.
- ### 6.1.
- ### 6.2.

Sección 7:
- ## 7.
- ### 7.1.
- ### 7.2.
- ### 7.3.
- ### 7.4.
- ### 7.5.

Sección 8:
- ## 8.

Sección 9:
- ## 9.
"""

def fix_spanish():
    path = 'content/es/posts/matriz-rice-ice-priorizacion/index.md'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = [
        # Sección 1
        ("### La Anatomía del Modelo: Los Cuatro Componentes Estructurales",
         "### 1.1. La Anatomía del Modelo: Los Cuatro Componentes Estructurales"),
        ("### Tabla Comparativa: Priorización Tradicional vs. Matriz RICE & ICE Cuantitativa",
         "### 1.2. Tabla Comparativa: Priorización Tradicional vs. Matriz RICE & ICE Cuantitativa"),
        ("### Cómo Funciona: El Embudo Estratégico Integral (De Suite 01 Estrategia a Suite 02 Decisiones)",
         "### 1.3. Cómo Funciona: El Embudo Estratégico Integral (De Suite 01 Estrategia a Suite 02 Decisiones)"),

        # Sección 3
        ("### 2.1. Puntuación Canónica RICE: El Concepto de Densidad de Valor",
         "### 3.1. Puntuación Canónica RICE: El Concepto de Densidad de Valor"),
        ("### 2.2. La Confianza como Descuento Bayesiano de Incertidumbre",
         "### 3.2. La Confianza como Descuento Bayesiano de Incertidumbre"),
        ("### 2.3. Framework ICE para Experimentos de Crecimiento (Growth)",
         "### 3.3. Framework ICE para Experimentos de Crecimiento (Growth)"),
        ("### 2.4. Normalización Escalar 0 - 100",
         "### 3.4. Normalización Escalar 0 - 100"),
        ("### 2.5. La Línea de Corte de Capacidad y el Problema de la Mochila (Knapsack Problem)",
         "### 3.5. La Línea de Corte de Capacidad y el Problema de la Mochila (Knapsack Problem)"),

        # Sección 4
        ("### Definición Canónica de los Cuadrantes",
         "### 4.1. Definición Canónica de los Cuadrantes"),

        # Sección 5
        ("### 4.1. Medición de Reach (Alcance)",
         "### 5.1. Medición de Reach (Alcance)"),
        ("### 4.2. Escala de Impacto Intercom",
         "### 5.2. Escala de Impacto Intercom"),
        ("### 4.3. La Escalera de Evidencia: The Confidence Meter (Itamar Gilad)",
         "### 5.3. La Escalera de Evidencia: The Confidence Meter (Itamar Gilad)"),

        # Sección 6
        ("### 5.1. Matriz de Resultados RICE Cuantitativa",
         "### 6.1. Matriz de Resultados RICE Cuantitativa"),
        ("### 5.2. Análisis de las Resoluciones Estratégicas del Comité",
         "### 6.2. Análisis de las Resoluciones Estratégicas del Comité"),

        # Sección 7 (FAQ)
        ("### 1. ¿Por qué la funcionalidad que pidió el CEO o un inversor clave no está en el plan de Q1?",
         "### 7.1. ¿Por qué la funcionalidad que pidió el CEO o un inversor clave no está en el plan de Q1?"),
        ("### 2. ¿Cómo evitamos que los equipos inflen artificialmente la estimación de Confianza para ganar prioridad?",
         "### 7.2. ¿Cómo evitamos que los equipos inflen artificialmente la estimación de Confianza para ganar prioridad?"),
        ("### 3. ¿Dónde encaja la deuda técnica si el algoritmo siempre premia las funcionalidades visibles?",
         "### 7.3. ¿Dónde encaja la deuda técnica si el algoritmo siempre premia las funcionalidades visibles?"),
        ("### 4. ¿Cuándo conviene utilizar RICE frente a WSJF (Weighted Shortest Job First / Coste del Retraso)?",
         "### 7.4. ¿Cuándo conviene utilizar RICE frente a WSJF (Weighted Shortest Job First / Coste del Retraso)?"),
        ("### 5. ¿Con qué cadencia temporal debe repriorizarse el backlog?",
         "### 7.5. ¿Con qué cadencia temporal debe repriorizarse el backlog?"),
    ]

    for old, new in replacements:
        assert old in content, f"No encontrado en ES: {old}"
        content = content.replace(old, new, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] ES: Todas las secciones y subsecciones han sido alineadas.")


def fix_english():
    path = 'content/en/posts/rice-ice-prioritization-matrix/index.md'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = [
        # Sección 1
        ("### The System Architecture: Four Integrated Structural Components",
         "### 1.1. The System Architecture: Four Integrated Structural Components"),
        ("### Comparative Table: Traditional Backlog Ranking vs. Quantitative RICE & ICE Matrix",
         "### 1.2. Comparative Table: Traditional Backlog Ranking vs. Quantitative RICE & ICE Matrix"),
        ("### How It Works: The Strategic Decision Funnel (Suite 01 MBA Strategy to Suite 02 Decision Making)",
         "### 1.3. How It Works: The Strategic Decision Funnel (Suite 01 MBA Strategy to Suite 02 Decision Making)"),

        # Sección 3 (era ## 2.)
        ("## 2. Mathematical Foundations: Value Density, Bayesian Risk & The Knapsack Cut",
         "## 3. Mathematical Foundations: Value Density, Bayesian Risk & The Knapsack Cut"),
        ("### 2.1. Canonical RICE Score: The Value Density Principle",
         "### 3.1. Canonical RICE Score: The Value Density Principle"),
        ("### 2.2. Confidence as a Bayesian Uncertainty Deflator",
         "### 3.2. Confidence as a Bayesian Uncertainty Deflator"),
        ("### 2.3. ICE Framework for High-Velocity Growth Sprints",
         "### 3.3. ICE Framework for High-Velocity Growth Sprints"),
        ("### 2.4. Normalized 0 - 100 Index",
         "### 3.4. Normalized 0 - 100 Index"),
        ("### 2.5. The Capacity Cut-Line and the Knapsack Problem",
         "### 3.5. The Capacity Cut-Line and the Knapsack Problem"),

        # Sección 4
        ("### Canonical Quadrant Governance",
         "### 4.1. Canonical Quadrant Governance"),

        # Sección 5 (era ## 4.)
        ("## 4. Calibration Protocol: Objective Scales & The Confidence Meter",
         "## 5. Calibration Protocol: Objective Scales & The Confidence Meter"),
        ("### 4.1. Reach Calculation",
         "### 5.1. Reach Calculation"),
        ("### 4.2. Intercom Impact Scale",
         "### 5.2. Intercom Impact Scale"),
        ("### 4.3. The Evidence Ladder: The Confidence Meter (Itamar Gilad)",
         "### 5.3. The Evidence Ladder: The Confidence Meter (Itamar Gilad)"),

        # Sección 6
        ("### 5.1. Quantitative RICE Results Matrix",
         "### 6.1. Quantitative RICE Results Matrix"),
        ("### 5.2. Executive Steering Committee Takeaways",
         "### 6.2. Executive Steering Committee Takeaways"),

        # Sección 7 (era ## 6.)
        ("## 6. Boardroom Defense FAQ",
         "## 7. Boardroom Defense FAQ"),
        ("### 1. Why isn't the feature requested by the CEO or a lead investor included in Q1?",
         "### 7.1. Why isn't the feature requested by the CEO or a lead investor included in Q1?"),
        ("### 2. How do we prevent teams from inflating Confidence to manipulate the ranking?",
         "### 7.2. How do we prevent teams from inflating Confidence to manipulate the ranking?"),
        ("### 3. Where does technical debt fit if algorithms prioritize user-facing features?",
         "### 7.3. Where does technical debt fit if algorithms prioritize user-facing features?"),
        ("### 4. When should an enterprise deploy RICE vs. WSJF (Cost of Delay)?",
         "### 7.4. When should an enterprise deploy RICE vs. WSJF (Cost of Delay)?"),
        ("### 5. What is the optimal governance review cadence?",
         "### 7.5. What is the optimal governance review cadence?"),
    ]

    for old, new in replacements:
        assert old in content, f"No encontrado en EN: {old}"
        content = content.replace(old, new, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] EN: Todas las secciones y subsecciones han sido alineadas.")


if __name__ == '__main__':
    fix_spanish()
    fix_english()
