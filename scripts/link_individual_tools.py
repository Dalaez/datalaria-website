import os

# 1. ES DAR
p_es_dar = "content/es/posts/matriz-dar-cuantitativa/index.md"
with open(p_es_dar, "r", encoding="utf-8") as f:
    text = f.read()
if "toma-decisiones-priorizacion" not in text:
    old_anchor = "## 1. El Embudo de Decisión Metodológico CMMI DAR"
    callout = """> [!NOTE]
> **Suite 02 de Decisión Corporativa:** Esta herramienta forma parte del [Framework Cuantitativo de 3 Niveles de Toma de Decisiones & Priorización](/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/), que integra la selección de arquitectura (Matriz DAR), la priorización de backlog ([Matriz RICE & ICE](/es/posts/matriz-rice-ice-priorizacion/)) y la justificación de capital ([Business Case Financiero](/es/posts/business-case-financiero-van-tir/)).

"""
    text = text.replace(old_anchor, callout + old_anchor, 1)
    with open(p_es_dar, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {p_es_dar}")

# 2. ES RICE
p_es_rice = "content/es/posts/matriz-rice-ice-priorizacion/index.md"
with open(p_es_rice, "r", encoding="utf-8") as f:
    text = f.read()
if "toma-decisiones-priorizacion" not in text:
    old_anchor = "## 1. El Pipeline Metodológico de Priorización Cuantitativa"
    callout = """> [!NOTE]
> **Suite 02 de Decisión Corporativa:** Esta herramienta forma parte del [Framework Cuantitativo de 3 Niveles de Toma de Decisiones & Priorización](/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/), que integra la selección de arquitectura ([Matriz DAR](/es/posts/matriz-dar-cuantitativa/)), la priorización de backlog (Matriz RICE & ICE) y la justificación de capital ([Business Case Financiero](/es/posts/business-case-financiero-van-tir/)).

"""
    text = text.replace(old_anchor, callout + old_anchor, 1)
    with open(p_es_rice, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {p_es_rice}")

# 3. ES BC
p_es_bc = "content/es/posts/business-case-financiero-van-tir/index.md"
with open(p_es_bc, "r", encoding="utf-8") as f:
    text = f.read()
if "toma-decisiones-priorizacion" not in text:
    old_anchor = "## 1. El Pipeline Metodológico del Business Case Institucional"
    callout = """> [!NOTE]
> **Suite 02 de Decisión Corporativa:** Esta herramienta forma parte del [Framework Cuantitativo de 3 Niveles de Toma de Decisiones & Priorización](/es/posts/toma-decisiones-priorizacion-framework-cuantitativo/), que integra la selección de arquitectura ([Matriz DAR](/es/posts/matriz-dar-cuantitativa/)), la priorización de backlog ([Matriz RICE & ICE](/es/posts/matriz-rice-ice-priorizacion/)) y la justificación de capital (Business Case Financiero).

"""
    text = text.replace(old_anchor, callout + old_anchor, 1)
    with open(p_es_bc, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {p_es_bc}")

# 4. EN DAR
p_en_dar = "content/en/posts/quantitative-dar-matrix/index.md"
with open(p_en_dar, "r", encoding="utf-8") as f:
    text = f.read()
if "decision-making-prioritization" not in text:
    old_anchor = "## 1. The CMMI DAR Methodological Decision Funnel"
    callout = """> [!NOTE]
> **Suite 02 Corporate Decision System:** This toolkit is an integral component of the [3-Tier Quantitative Decision-Making & Prioritization Framework](/en/posts/decision-making-prioritization-quantitative-framework/), integrating architectural selection (DAR Matrix), backlog capacity planning ([RICE & ICE Matrix](/en/posts/rice-ice-prioritization-matrix/)), and capital justification ([Financial Business Case](/en/posts/financial-business-case-npv-irr/)).

"""
    text = text.replace(old_anchor, callout + old_anchor, 1)
    with open(p_en_dar, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {p_en_dar}")

# 5. EN RICE
p_en_rice = "content/en/posts/rice-ice-prioritization-matrix/index.md"
with open(p_en_rice, "r", encoding="utf-8") as f:
    text = f.read()
if "decision-making-prioritization" not in text:
    old_anchor = "## 1. The Quantitative Prioritization Methodological Pipeline"
    callout = """> [!NOTE]
> **Suite 02 Corporate Decision System:** This toolkit is an integral component of the [3-Tier Quantitative Decision-Making & Prioritization Framework](/en/posts/decision-making-prioritization-quantitative-framework/), integrating architectural selection ([DAR Matrix](/en/posts/quantitative-dar-matrix/)), backlog capacity planning (RICE & ICE Matrix), and capital justification ([Financial Business Case](/en/posts/financial-business-case-npv-irr/)).

"""
    text = text.replace(old_anchor, callout + old_anchor, 1)
    with open(p_en_rice, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {p_en_rice}")

# 6. EN BC
p_en_bc = "content/en/posts/financial-business-case-npv-irr/index.md"
with open(p_en_bc, "r", encoding="utf-8") as f:
    text = f.read()
if "decision-making-prioritization" not in text:
    old_anchor = "## 1. The Methodological Pipeline of an Institutional Business Case"
    callout = """> [!NOTE]
> **Suite 02 Corporate Decision System:** This toolkit is an integral component of the [3-Tier Quantitative Decision-Making & Prioritization Framework](/en/posts/decision-making-prioritization-quantitative-framework/), integrating architectural selection ([DAR Matrix](/en/posts/quantitative-dar-matrix/)), backlog capacity planning ([RICE & ICE Matrix](/en/posts/rice-ice-prioritization-matrix/)), and capital justification (Financial Business Case).

"""
    text = text.replace(old_anchor, callout + old_anchor, 1)
    with open(p_en_bc, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {p_en_bc}")
