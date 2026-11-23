"""
ops/pulse/impact_analyzer.py
----------------------------
Motor Cuantitativo de Análisis de Impacto SEO, Tráfico GA4 y Monetización B2B.
Especificación técnica formal: SPEC-APP-PULSE v1.2.0 (specs/apps/pulse/spec.md) - Hito 7.2 / ADR-020.
Agente responsable: E02-seo-impact-strategist (Dirección & Inteligencia Estratégica).

Responsabilidades:
1. Cruzar determinísticamente index.json, metrics.json, monthly_metrics.json, kits.yaml y backlog.yaml.
2. Calcular la fórmula del Editorial ROI Score:
   Score = round(0.40 * SEO_Demand + 0.35 * Monetization_Fit + 0.25 * Ecosystem_Synergy, 1)
3. Detectar Quick Wins de CTR/SERP con títulos recomendados (35-95 chars) y meta descripciones (75-245 chars).
4. Identificar los Huérfanos de Monetización en el cuartil superior de tráfico y asociarles puentes a Kits/Apps.
5. Evaluar la cobertura y rendimiento por las 5 categorías oficiales de Datalaria.
6. Exportar data/pulse/private/impact_report.json (INV-PULSE-6) y specs/audit/IMPACT_REPORT.md.
"""

from __future__ import annotations

import json
import math
import os
import re
import statistics
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from ops.pulse.models import (
    BacklogPrioritizedItem,
    BridgeType,
    CannibalizationAlertItem,
    CanonicalShieldAlertItem,
    CategoryPerformanceItem,
    ChannelSummaryItem,
    DarkSocialAlertItem,
    DecayAlertItem,
    HiddenChannelWinnerItem,
    MonetizationOrphanItem,
    OpportunityType,
    PullThroughAlertItem,
    PulseImpactReport,
    QuickWinItem,
    ReleaseEditorialImpactItem,
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
INDEX_PATH = ROOT_DIR / "data" / "pulse" / "private" / "index.json"
METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "metrics.json"
MONTHLY_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "monthly_metrics.json"
GSC_QUERIES_PATH = ROOT_DIR / "data" / "pulse" / "private" / "gsc_queries.json"
CHANNEL_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "channel_metrics.json"
SOCIAL_METRICS_PATH = ROOT_DIR / "data" / "pulse" / "private" / "social_metrics.json"
KITS_PATH = ROOT_DIR / "data" / "pulse" / "kits.yaml"
BACKLOG_PATH = ROOT_DIR / "data" / "editorial" / "backlog.yaml"
DISPATCH_QUEUE_PATH = ROOT_DIR / "data" / "editorial" / "dispatch_queue.yaml"
REPORT_JSON_PATH = ROOT_DIR / "data" / "pulse" / "private" / "impact_report.json"
REPORT_MD_PATH = ROOT_DIR / "specs" / "audit" / "IMPACT_REPORT.md"

CURATED_QUICK_WINS: Dict[str, Dict[str, str]] = {
    "quantitative-swot-tows-matrix": {
        "title_es": "DAFO Cuantitativo y Matriz CAME: Decisión Estratégica para Comités de Dirección",
        "title_en": "Quantitative SWOT & TOWS Matrix: Strategic Decision Framework for C-Level",
        "desc_es": "Modelo matemático para transformar el DAFO cualitativo en análisis vectorial con calificaciones y plan CAME para Comités de Dirección.",
    },
    "sdd_vs_vibe_coding": {
        "title_es": "SDD (Spec-Driven Development) vs. Vibe Coding: Software Robusto con IA en 2026",
        "title_en": "SDD (Spec-Driven Development) vs. Vibe Coding: Robust AI Engineering in 2026",
        "desc_es": "Por qué el Vibe Coding acumula deuda técnica invisible y cómo SDD invierte el rol del ingeniero mediante contratos, especificaciones y tests.",
    },
    "john_von_neumann": {
        "title_es": "John von Neumann: Arquitectura de Computadores, Teoría de Juegos y Singularidad",
        "title_en": "John von Neumann: Computer Architecture, Game Theory, and the Singularity",
        "desc_es": "Vida y genio de John von Neumann: ordenadores de programa almacenado, el cuello de botella que desafía a la IA y el origen de la Singularidad.",
    },
    "quantitative-porter-5-forces": {
        "title_es": "5 Fuerzas de Porter Ponderadas y Atractivo de Industria: Guía Cuantitativa C-Level",
        "title_en": "Weighted Porter 5 Forces: Quantitative Industry Attractiveness for Executives",
        "desc_es": "Transforma las 5 Fuerzas de Porter en un motor matemático ponderado con gráfico radar, diagnóstico de foso defensivo y plan de acción.",
    },
    "app-lifeops_part6_analytics_dashboard_360": {
        "title_es": "LifeOps (Parte 6): Dashboard 360° Multidimensional, Recharts y Caché SWR",
        "title_en": "LifeOps (Part 6): 360° Multi-Dimensional Analytics Dashboard with Recharts",
        "desc_es": "Arquitectura de Dashboard 360° con analítica multidimensional, mapas estilo Strava y mitigación de cold-starts en Supabase y Render.",
    },
    "matriz-rice-ice-priorizacion": {
        "title_es": "Matriz RICE & ICE de Priorización Ágil: Backlog Cuantitativo y Capacidad",
        "title_en": "RICE & ICE Agile Prioritization Matrix: Quantitative Backlog Scoring",
        "desc_es": "Framework cuantitativo para implementar RICE e ICE: densidad de valor, descuento bayesiano de confianza y corte por capacidad de squads.",
    },
    "kantorovich": {
        "title_es": "Leonid Kantorovich: El Matemático que Desafió a Stalin con la Programación Lineal",
        "title_en": "Leonid Kantorovich: Linear Programming, Resource Allocation & Economic Theory",
        "desc_es": "Invención de la programación lineal para optimizar recursos industriales frente al dogma soviético, base de la optimización logística moderna.",
    },
    "matriz-dar-cuantitativa": {
        "title_es": "Matriz DAR Cuantitativa: Criterios Veto, Scoring Multicriterio y Decisiones C-Level",
        "title_en": "Quantitative DAR Matrix: CMMI Decision Analysis & Multi-Criteria Scoring",
        "desc_es": "Metodología cuantitativa para matriz CMMI DAR y Kepner-Tregoe: filtros veto booleanos, scoring multicriterio ponderado y gobierno corporativo.",
    },
    "graphrag": {
        "title_es": "GraphRAG: Por Qué los Vectores No Bastan y Tu IA Requiere Grafos de Conocimiento",
        "title_en": "GraphRAG: Why Vectors Are Not Enough and Your AI Needs Knowledge Graphs",
        "desc_es": "Supera las alucinaciones del RAG tradicional combinando embeddings vectoriales con grafos de entidades para razonamiento estructurado multihop.",
    },
    "abraham_wald": {
        "title_es": "Abraham Wald y los Aviones de la Segunda Guerra: Epistemología de Datos Ausentes",
        "title_en": "Abraham Wald & WWII Aircraft: The Epistemology of Missing Data in AI",
        "desc_es": "Cómo Abraham Wald dedujo el blindaje en los aviones analizando impactos supervivientes: el sesgo de supervivencia aplicado a machine learning.",
    },
    "kurt_godel": {
        "title_es": "Kurt Gödel: Teoremas de Incompletitud, Límites de la Lógica y Alcance de la AGI",
        "title_en": "Kurt Gödel: Incompleteness Theorems, Limits of Logic and AGI Boundaries",
        "desc_es": "Los teoremas de incompletitud de Gödel: cómo demolieron el programa de Hilbert y por qué definen las fronteras cognitivas de la inteligencia artificial.",
    },
    "submer": {
        "title_es": "Submer: Refrigeración Líquida Nacida en Barcelona para Superordenadores de AGI",
        "title_en": "Submer: Barcelona Immersion Cooling Powering Next-Gen AGI Supercomputers",
        "desc_es": "Inmersión líquida para centros de datos de IA: alianzas con Nvidia e Intel y solución al cuello de botella térmico de los clusters de entrenamiento.",
    },
}

ORPHAN_BRIDGE_MAPPING: Dict[str, Dict[str, str]] = {
    "sdd_vs_vibe_coding": {
        "bridge_type": "helix_waitlist",
        "target_id": "helix",
        "shortcode_or_url": "{{< helix-waitlist >}}",
        "rationale_es": "Post insignia sobre Spec-Driven Development; puente directo hacia la lista de espera de Datalaria Helix (19€/39€).",
    },
    "john_von_neumann": {
        "bridge_type": "kit_b2b",
        "target_id": "suite-01",
        "shortcode_or_url": "[Pack Suite 1: Estrategia MBA](/es/recursos/#suite-01)",
        "rationale_es": "Tráfico masivo de teoría de juegos y computación; vincular a modelos de decisión estratégica y matriz de Porter (Suite 01).",
    },
    "kantorovich": {
        "bridge_type": "kit_b2b",
        "target_id": "suite-02",
        "shortcode_or_url": "[Pack Suite 2: Decisiones](/es/recursos/#suite-02)",
        "rationale_es": "Pilar de programación lineal y optimización; encaje directo con la Matriz DAR y Matriz RICE (Suite 02).",
    },
    "graphrag": {
        "bridge_type": "app_sandbox",
        "target_id": "obs-management",
        "shortcode_or_url": '{{< app-ref slug="obs-management" >}}',
        "rationale_es": "Alta relevancia en arquitecturas ag?nticas avanzadas; dirigir hacia el sandbox de observabilidad y gobierno de agentes.",
    },
    "abraham_wald": {
        "bridge_type": "kit_b2b",
        "target_id": "suite-02",
        "shortcode_or_url": "[Pack Matriz DAR Cuantitativa](/es/recursos/#pack-dar)",
        "rationale_es": "Sesgo de supervivencia y toma de decisiones rigurosa; puente natural hacia la Matriz DAR y el Business Case Financiero.",
    },
    "kurt_godel": {
        "bridge_type": "helix_waitlist",
        "target_id": "helix",
        "shortcode_or_url": "{{< helix-waitlist >}}",
        "rationale_es": "Altísimo tiempo de lectura (45+ min); monetizar con el manifiesto de verificación formal y desarrollo riguroso de Helix.",
    },
    "submer": {
        "bridge_type": "kit_b2b",
        "target_id": "pack-business-case",
        "shortcode_or_url": "[Pack Business Case Financiero](/es/recursos/#pack-business-case)",
        "rationale_es": "Caso de estudio de infraestructura y hardware B2B; enlazar al Business Case Financiero (VAN, TIR y CAPEX) en Suite 02.",
    },
    "evaluacion_agentes_ia": {
        "bridge_type": "helix_waitlist",
        "target_id": "helix",
        "shortcode_or_url": "{{< helix-waitlist >}}",
        "rationale_es": "Testing de agentes en producción; llamada a la acción obligatoria para el Kit Core y los Blueprints de Datalaria Helix.",
    },
    "alan_turing": {
        "bridge_type": "helix_waitlist",
        "target_id": "helix",
        "shortcode_or_url": "{{< helix-waitlist >}}",
        "rationale_es": "Fundamentos de computación e inteligencia; vincular al salto generacional hacia el desarrollo asistido por agentes autónomos.",
    },
    "ex_machina": {
        "bridge_type": "app_sandbox",
        "target_id": "obs-management",
        "shortcode_or_url": '{{< app-ref slug="obs-management" >}}',
        "rationale_es": "Cultura de alineamiento e interfaces de IA; conectar con la app interactiva Agentic Radar (Sandbox B2B).",
    },
    "her": {
        "bridge_type": "app_sandbox",
        "target_id": "obs-management",
        "shortcode_or_url": '{{< app-ref slug="obs-management" >}}',
        "rationale_es": "Apego y autonomía de sistemas agénticos; dirigir hacia el sandbox de observabilidad y gobierno de agentes.",
    },
    "ravenpack": {
        "bridge_type": "kit_b2b",
        "target_id": "pack-business-case",
        "shortcode_or_url": "[Pack Business Case Financiero](/es/recursos/#pack-business-case)",
        "rationale_es": "IA cuantitativa aplicada a mercados financieros; puente directo al pack financiero de inversión y retorno de capital.",
    },
    "nextail": {
        "bridge_type": "kit_b2b",
        "target_id": "suite-01",
        "shortcode_or_url": "[Pack Suite 1: Estrategia MBA](/es/recursos/#suite-01)",
        "rationale_es": "IA prescriptiva frente a hojas de cálculo en retail; asociar con modelos de estrategia de cartera y BCG Matrix.",
    },
    "silicon_valley": {
        "bridge_type": "app_sandbox",
        "target_id": "obs-management",
        "shortcode_or_url": '{{< app-ref slug="obs-management" >}}',
        "rationale_es": "Sátira tecnológica y fallos en sistemas distribuidos; enlace formativo hacia Agentic Radar y auditoría de agentes.",
    },
    "oppenheimer": {
        "bridge_type": "kit_b2b",
        "target_id": "suite-02",
        "shortcode_or_url": "[Pack Suite 2: Decisiones](/es/recursos/#suite-02)",
        "rationale_es": "Simulación de Monte Carlo y riesgo extremo; dirigir hacia el pack de priorización y justificación económica de proyectos.",
    },
}


def calculate_editorial_roi_score(
    seo_demand: float,
    monetization_fit: float,
    synergy: float,
    social_traction: Optional[float] = None,
) -> float:
    """
    Calcula determinísticamente el Editorial ROI Score v2 acotado en [0, 100].
    - Sin historial social (`social_traction=None`): preserva fórmula v1 (40% SEO + 35% Monetización + 25% Sinergia).
    - Con señal social validada (`social_traction` en [0, 100]): Editorial ROI Score v2
      (35% SEO + 30% Monetización + 20% Sinergia + 15% Tracción Social/Comunidad).
    """
    s_seo = max(0.0, min(100.0, float(seo_demand)))
    s_mon = max(0.0, min(100.0, float(monetization_fit)))
    s_syn = max(0.0, min(100.0, float(synergy)))
    if social_traction is None:
        score = 0.40 * s_seo + 0.35 * s_mon + 0.25 * s_syn
    else:
        s_soc = max(0.0, min(100.0, float(social_traction)))
        score = 0.35 * s_seo + 0.30 * s_mon + 0.20 * s_syn + 0.15 * s_soc
    return round(max(0.0, min(100.0, float(score))), 1)


def _optimize_text(text: str, min_len: int, max_len: int, fallback_suffix: str = "") -> str:
    """Asegura de forma determinista que un texto cumpla con las cotas de longitud [min_len, max_len]."""
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if len(cleaned) < min_len:
        needed = min_len - len(cleaned)
        padding = f" — {fallback_suffix}" if fallback_suffix else " — Datalaria"
        cleaned = (cleaned + padding)[:max_len]
        if len(cleaned) < min_len:
            cleaned = cleaned.ljust(min_len, ".")
    elif len(cleaned) > max_len:
        # Cortar en última palabra completa antes de max_len
        truncated = cleaned[:max_len]
        last_space = truncated.rfind(" ")
        if last_space > min_len:
            cleaned = truncated[:last_space].rstrip(",;:-.")
        else:
            cleaned = truncated[:max_len]
    return cleaned


def detect_quick_wins_ctr(
    published_posts: List[Dict[str, Any]],
    metrics: Dict[str, Dict[str, Any]],
    median_views: float,
) -> List[QuickWinItem]:
    """
    Detecta los Quick Wins de CTR cruzando Search Console, exceso de caracteres en Snippet y retención.
    """
    quick_wins: List[QuickWinItem] = []

    for post in published_posts:
        pid = post["id"]
        m = metrics.get(pid, {})
        views = int(m.get("ga4_views_30d", 0))
        users = int(m.get("ga4_users_30d", 0))
        eng = float(m.get("ga4_engagement_sec", 0.0))
        avg_eng = round(eng / max(users, 1), 1)
        impr = int(m.get("gsc_impressions_30d", 0))
        pos = float(m.get("gsc_avg_position", 0.0))
        ctr = float(m.get("gsc_ctr_pct", 0.0))

        seo_audit = post.get("seo_audit", {})
        score = int(seo_audit.get("score_0_100", 100))
        issues = list(seo_audit.get("issues", []))

        t_es = post.get("title_es") or post.get("title_en") or pid
        t_en = post.get("title_en") or post.get("title_es") or pid
        b_es = post.get("brief_es") or post.get("brief_en") or t_es

        # Condiciones de activación
        is_gsc = bool(impr >= 30 and ((4.0 <= pos <= 20.0) or ctr < 2.5))
        is_trunc = bool(views >= median_views and (len(t_es) > 95 or len(b_es) > 250 or score < 100))
        is_high_eng = bool(views >= median_views and avg_eng >= 30.0 and (score < 100 or len(t_es) > 95))

        if not (is_gsc or is_trunc or is_high_eng):
            continue

        if is_gsc:
            opp_type: OpportunityType = "gsc_position_4_20"
            prio = min(100.0, round(float(min(impr / 50.0, 65.0) + max(0.0, 25.0 - pos) * 1.4), 1))
        elif is_trunc:
            opp_type = "serp_snippet_truncation"
            prio = min(100.0, round(float(views * 0.5 + (100 - score) * 0.5), 1))
        else:
            opp_type = "high_retention_low_ctr"
            prio = min(100.0, round(float(avg_eng * 0.6 + views * 0.4), 1))

        top_queries = m.get("gsc_top_queries") or []
        top_query: Optional[str] = None
        if isinstance(top_queries, list) and top_queries:
            q0 = top_queries[0]
            if isinstance(q0, dict) and q0.get("query"):
                top_query = str(q0["query"])

        # Recomendaciones de título y meta descripción
        curated = CURATED_QUICK_WINS.get(pid)
        if curated:
            rec_t_es = curated["title_es"]
            rec_t_en = curated["title_en"]
            rec_d_es = curated["desc_es"]
        else:
            rec_t_es = _optimize_text(t_es, 35, 95, "Guía Técnica")
            rec_t_en = _optimize_text(t_en, 35, 95, "Technical Guide")
            rec_d_es = _optimize_text(b_es, 75, 245, "Análisis metodológico exhaustivo en Datalaria.")

        quick_wins.append(
            QuickWinItem(
                id=pid,
                slug=post.get("slug", pid),
                title_es=t_es,
                title_en=t_en,
                category=post.get("category", "General"),
                ga4_views_30d=views,
                ga4_users_30d=users,
                avg_engagement_sec=avg_eng,
                gsc_impressions_30d=impr,
                gsc_avg_position=pos,
                gsc_ctr_pct=ctr,
                seo_score=score,
                seo_issues=issues,
                opportunity_type=opp_type,
                priority_score=prio,
                recommended_title_es=rec_t_es,
                recommended_title_en=rec_t_en,
                recommended_desc_es=rec_d_es,
                top_query=top_query,
            )
        )

    # Ordenar por prioridad descendente
    quick_wins.sort(key=lambda x: (x.priority_score, x.ga4_views_30d), reverse=True)
    return quick_wins


def detect_monetization_orphans(
    published_posts: List[Dict[str, Any]],
    metrics: Dict[str, Dict[str, Any]],
    p75_views: float,
) -> List[MonetizationOrphanItem]:
    """
    Detecta los posts en el cuartil superior de tráfico sin App ni Kit asociado.
    """
    # 1. Calcular percentiles de tráfico para asignar rank_pct
    views_map = {p["id"]: metrics.get(p["id"], {}).get("ga4_views_30d", 0) for p in published_posts}
    sorted_views = sorted(views_map.values())
    total_posts = len(sorted_views)

    orphans: List[MonetizationOrphanItem] = []

    for post in published_posts:
        pid = post["id"]
        v = views_map.get(pid, 0)
        has_app = bool(post.get("related_app"))
        has_kit = bool(post.get("related_kit"))

        if v >= p75_views and not has_app and not has_kit:
            m = metrics.get(pid, {})
            users = int(m.get("ga4_users_30d", 0))
            eng = float(m.get("ga4_engagement_sec", 0.0))
            avg_eng = round(eng / max(users, 1), 1)

            # Percentil estándar
            count_less = sum(1 for x in sorted_views if x < v)
            count_equal = sum(1 for x in sorted_views if x == v)
            rank_pct = round(((count_less + 0.5 * count_equal) / max(total_posts, 1)) * 100)

            mapping = ORPHAN_BRIDGE_MAPPING.get(pid)
            if mapping:
                b_type: BridgeType = mapping["bridge_type"]  # type: ignore[assignment]
                target_id = mapping["target_id"]
                bridge_cmd = mapping["shortcode_or_url"]
                rationale = mapping["rationale_es"]
            else:
                cat = post.get("category", "")
                if "Estrategia" in cat or "Operaciones" in cat:
                    b_type = "kit_b2b"
                    target_id = "suite-01"
                    bridge_cmd = "[Pack Suite 1: Estrategia MBA](/es/recursos/#suite-01)"
                    rationale = "Contenido de negocio de alto tráfico; conectar con las plantillas de toma de decisiones de la Suite 01."
                elif "Pioneros" in cat or "IA" in cat:
                    b_type = "helix_waitlist"
                    target_id = "helix"
                    bridge_cmd = "{{< helix-waitlist >}}"
                    rationale = "Tráfico de alta retención técnica; dirigir hacia la lista de espera de Datalaria Helix."
                else:
                    b_type = "app_sandbox"
                    target_id = "obs-management"
                    bridge_cmd = '{{< app-ref slug="obs-management" >}}'
                    rationale = "Vincular a una aplicación interactiva del catálogo para retención y prueba de producto."

            orphans.append(
                MonetizationOrphanItem(
                    id=pid,
                    slug=post.get("slug", pid),
                    title_es=post.get("title_es") or pid,
                    category=post.get("category", "General"),
                    ga4_views_30d=v,
                    ga4_users_30d=users,
                    avg_engagement_sec=avg_eng,
                    rank_pct=rank_pct,
                    recommended_bridge_type=b_type,
                    recommended_target_id=target_id,
                    recommended_shortcode_or_url=bridge_cmd,
                    rationale_es=rationale,
                )
            )

    orphans.sort(key=lambda x: (x.ga4_views_30d, x.avg_engagement_sec), reverse=True)
    return orphans


def calculate_category_performance(
    published_posts: List[Dict[str, Any]],
    metrics: Dict[str, Dict[str, Any]],
    social_data: Optional[Dict[str, Any]] = None,
    channel_data: Optional[Dict[str, Any]] = None,
) -> List[CategoryPerformanceItem]:
    """
    Calcula agregados cuantitativos, métricas GSC, cuota EN, tracción social validada (Editorial ROI Score v2)
    y cobertura de monetización por categoría.
    """
    cat_data: Dict[str, Dict[str, Any]] = {}
    social_by_asset = (social_data or {}).get("by_asset") if isinstance(social_data, dict) else {}
    if not isinstance(social_by_asset, dict):
        social_by_asset = {}
    channel_by_asset = (channel_data or {}).get("by_asset") if isinstance(channel_data, dict) else {}
    if not isinstance(channel_by_asset, dict):
        channel_by_asset = {}

    has_social_history = bool(social_by_asset or channel_by_asset)

    for post in published_posts:
        cat = post.get("category", "General")
        pid = post["id"]
        m = metrics.get(pid, {})
        v = int(m.get("ga4_views_30d", 0) or 0)
        v_en = int(m.get("ga4_views_en_30d", 0) or 0)
        u = int(m.get("ga4_users_30d", 0) or 0)
        eng = float(m.get("ga4_engagement_sec", 0.0) or 0.0)
        g_impr = int(m.get("gsc_impressions_30d", 0) or 0)
        g_clk = int(m.get("gsc_clicks_30d", 0) or 0)
        is_mon = bool(post.get("related_app") or post.get("related_kit"))

        # Señales sociales/comunidad validadas (Dev.to, CoderLegion, LinkedIn Empresa, X)
        p_soc = social_by_asset.get(pid) if isinstance(social_by_asset.get(pid), dict) else {}
        soc_native_views = 0
        soc_reactions = 0
        soc_comments = 0
        for p_vals in p_soc.values():
            if isinstance(p_vals, dict):
                soc_native_views += int(p_vals.get("views", 0) or p_vals.get("impressions", 0) or 0)
                soc_reactions += int(p_vals.get("reactions", 0) or 0)
                soc_comments += int(p_vals.get("comments", 0) or 0)

        p_ch = channel_by_asset.get(pid) if isinstance(channel_by_asset.get(pid), dict) else {}
        soc_sessions = 0
        soc_key_events = 0
        for ch_name in ("linkedin", "x", "devto", "coderlegion"):
            c_vals = p_ch.get(ch_name)
            if isinstance(c_vals, dict):
                soc_sessions += int(c_vals.get("sessions_30d", 0) or 0)
                soc_key_events += int(c_vals.get("key_events_30d", 0) or 0)

        if cat not in cat_data:
            cat_data[cat] = {
                "posts": 0,
                "views": 0,
                "views_en": 0,
                "users": 0,
                "eng": 0.0,
                "monetized": 0,
                "gsc_impr": 0,
                "gsc_clicks": 0,
                "soc_native_views": 0,
                "soc_reactions": 0,
                "soc_comments": 0,
                "soc_sessions": 0,
                "soc_key_events": 0,
            }

        cat_data[cat]["posts"] += 1
        cat_data[cat]["views"] += v
        cat_data[cat]["views_en"] += v_en
        cat_data[cat]["users"] += u
        cat_data[cat]["eng"] += eng
        cat_data[cat]["gsc_impr"] += g_impr
        cat_data[cat]["gsc_clicks"] += g_clk
        cat_data[cat]["soc_native_views"] += soc_native_views
        cat_data[cat]["soc_reactions"] += soc_reactions
        cat_data[cat]["soc_comments"] += soc_comments
        cat_data[cat]["soc_sessions"] += soc_sessions
        cat_data[cat]["soc_key_events"] += soc_key_events
        if is_mon:
            cat_data[cat]["monetized"] += 1

    items: List[CategoryPerformanceItem] = []
    for cat, d in cat_data.items():
        n = max(d["posts"], 1)
        u_tot = max(d["users"], 1)
        avg_v = round(d["views"] / n, 1)
        avg_e = round(d["eng"] / u_tot, 1)
        mon_pct = round((d["monetized"] / n) * 100.0, 1)
        g_impr = d["gsc_impr"]
        g_clk = d["gsc_clicks"]
        avg_ctr = round((g_clk / g_impr * 100.0) if g_impr > 0 else 0.0, 2)
        en_share = round((d["views_en"] / d["views"] * 100.0) if d["views"] > 0 else 0.0, 1)

        cat_ptr = calculate_ptr_pct(d["soc_sessions"], d["soc_native_views"]) if d["soc_native_views"] > 0 else 0.0
        eng_signal = min(45.0, d["soc_reactions"] * 1.2 + d["soc_comments"] * 2.5)
        ga4_signal = min(35.0, (d["soc_sessions"] / n) * 12.0 + d["soc_key_events"] * 10.0)
        ptr_signal = min(20.0, cat_ptr * 4.0)
        soc_traction = round(min(100.0, eng_signal + ga4_signal + ptr_signal), 1)

        seo_factor = min(100.0, avg_v * 3.5)
        mon_factor = mon_pct
        syn_factor = min(100.0, avg_e * 2.5)
        cat_roi = calculate_editorial_roi_score(
            seo_factor,
            mon_factor,
            syn_factor,
            social_traction=soc_traction if has_social_history else None,
        )

        items.append(
            CategoryPerformanceItem(
                category=cat,
                published_posts=d["posts"],
                total_views_30d=d["views"],
                avg_views_per_post=avg_v,
                total_users_30d=d["users"],
                avg_engagement_sec=avg_e,
                monetized_posts=d["monetized"],
                monetization_coverage_pct=mon_pct,
                editorial_roi_score=cat_roi,
                social_traction_score=soc_traction,
                total_gsc_impressions_30d=g_impr,
                total_gsc_clicks_30d=g_clk,
                avg_gsc_ctr_pct=avg_ctr,
                en_traffic_share_pct=en_share,
            )
        )

    items.sort(key=lambda x: x.editorial_roi_score, reverse=True)
    return items


_NON_INDEXABLE_TAG_RE = re.compile(r"^/(?:(?:es|en)/)?tags(?:/|$)", re.IGNORECASE)


def detect_keyword_cannibalization(
    gsc_queries_data: Optional[Dict[str, Any]] = None,
    min_impressions: int = 20,
    exclude_non_indexable_taxonomies: bool = True,
) -> List[CannibalizationAlertItem]:
    """
    Detecta consultas en Search Console donde >= 2 URLs del mismo idioma compiten
    por la misma keyword con al menos `min_impressions` impresiones totales.
    Cuando `exclude_non_indexable_taxonomies` está activo (INV-TAX-7), omite rutas `/tags/`
    gobernadas por `noindex, follow`.
    """
    if gsc_queries_data is None:
        if not GSC_QUERIES_PATH.exists():
            return []
        try:
            with open(GSC_QUERIES_PATH, "r", encoding="utf-8") as f:
                gsc_queries_data = json.load(f)
        except Exception:
            return []

    by_page = gsc_queries_data.get("by_page", {}) or {}
    groups: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for page_path, qlist in by_page.items():
        if not isinstance(qlist, list):
            continue
        if exclude_non_indexable_taxonomies and _NON_INDEXABLE_TAG_RE.match(str(page_path)):
            continue
        for qrow in qlist:
            q_text = str(qrow.get("query") or "").strip()
            if not q_text or q_text.lower().startswith("site:"):
                continue
            lang = qrow.get("lang") or ("es" if page_path.startswith("/es/") else "en" if page_path.startswith("/en/") else "other")
            impr = int(qrow.get("impressions", 0) or 0)
            clk = int(qrow.get("clicks", 0) or 0)
            pos = float(qrow.get("position", 0.0) or 0.0)

            gkey = (q_text.lower(), lang)
            bucket = groups.setdefault(
                gkey,
                {"display_query": q_text, "lang": lang, "urls": {}},
            )
            prev_u = bucket["urls"].get(page_path)
            if prev_u:
                prev_u["impressions"] += impr
                prev_u["clicks"] += clk
            else:
                bucket["urls"][page_path] = {
                    "url": page_path,
                    "impressions": impr,
                    "clicks": clk,
                    "position": round(pos, 1),
                }

    alerts: List[CannibalizationAlertItem] = []
    for (_, _), bucket in groups.items():
        urls_list = list(bucket["urls"].values())
        if len(urls_list) < 2:
            continue
        tot_impr = sum(u["impressions"] for u in urls_list)
        if tot_impr < min_impressions:
            continue
        tot_clk = sum(u["clicks"] for u in urls_list)
        urls_list.sort(key=lambda u: (u["impressions"], u["clicks"]), reverse=True)
        leader = urls_list[0]["url"]
        action = f"Consolidar intención en {leader} con enlaces internos desde las URLs secundarias o diferenciar ángulo/H1."
        alerts.append(
            CannibalizationAlertItem(
                query=bucket["display_query"],
                lang=bucket["lang"],
                total_impressions=tot_impr,
                total_clicks=tot_clk,
                competing_urls=urls_list[:5],
                recommended_action=action,
            )
        )

    alerts.sort(key=lambda x: (x.total_impressions, x.total_clicks), reverse=True)
    return alerts


def detect_decay_alerts(
    published_posts: List[Dict[str, Any]],
    metrics: Dict[str, Dict[str, Any]],
) -> List[DecayAlertItem]:
    """Detecta posts publicados con más de 90 días con baja tracción o score SEO degradado."""
    alerts: List[DecayAlertItem] = []
    today = date.today()

    for post in published_posts:
        pid = post["id"]
        pub_d = post.get("publish_date")
        if not pub_d:
            continue
        if isinstance(pub_d, str):
            try:
                pub_d = datetime.fromisoformat(pub_d).date()
            except Exception:
                continue

        days = (today - pub_d).days
        m = metrics.get(pid, {})
        v = int(m.get("ga4_views_30d", 0))
        seo = int(post.get("seo_audit", {}).get("score_0_100", 100))

        if days >= 90 and (v <= 2 or seo < 70):
            action = (
                "Actualizar título y añadir enlaces internos hacia Kits/Apps"
                if seo < 70
                else "Refrescar contenido y re-sindicar en redes sociales"
            )
            alerts.append(
                DecayAlertItem(
                    id=pid,
                    slug=post.get("slug", pid),
                    title_es=post.get("title_es") or pid,
                    category=post.get("category", "General"),
                    publish_date=pub_d,
                    days_since_publish=days,
                    ga4_views_30d=v,
                    seo_score=seo,
                    recommended_action=action,
                )
            )

    alerts.sort(key=lambda x: (x.ga4_views_30d, x.seo_score))
    return alerts


def prioritize_backlog(
    backlog_file: Path = BACKLOG_PATH,
    category_social_scores: Optional[Dict[str, float]] = None,
) -> List[BacklogPrioritizedItem]:
    """Lee strategic_backlog desde backlog.yaml y calcula el Editorial ROI Score v2 ordenado."""
    if not backlog_file.exists():
        return []

    with open(backlog_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    raw_items = data.get("strategic_backlog", [])
    prioritized: List[BacklogPrioritizedItem] = []

    for item in raw_items:
        cat = item.get("category", "General")
        s_seo = float(item.get("seo_demand_score", 50.0))
        s_mon = float(item.get("monetization_fit_score", 50.0))
        s_syn = float(item.get("ecosystem_synergy_score", 50.0))
        raw_soc = item.get("social_traction_score")
        if raw_soc is not None:
            s_soc: Optional[float] = float(raw_soc)
        elif category_social_scores and cat in category_social_scores:
            s_soc = float(category_social_scores[cat])
        else:
            s_soc = None
        roi = calculate_editorial_roi_score(s_seo, s_mon, s_syn, social_traction=s_soc)

        prioritized.append(
            BacklogPrioritizedItem(
                id=item["id"],
                title_es=item["title_es"],
                title_en=item["title_en"],
                category=cat,
                target_kit_or_app=item.get("target_kit_or_app", ""),
                seo_demand_score=s_seo,
                monetization_fit_score=s_mon,
                ecosystem_synergy_score=s_syn,
                social_traction_score=round(s_soc, 1) if s_soc is not None else 0.0,
                editorial_roi_score=roi,
                rationale_es=item.get("rationale_es", ""),
            )
        )

    prioritized.sort(key=lambda x: x.editorial_roi_score, reverse=True)
    return prioritized


KIT_POST_MAPPING: Dict[str, List[str]] = {
    "pack-dafo": ["dafo-cuantitativo-matriz-came", "quantitative-swot-tows-matrix"],
    "pack-porter": ["5-fuerzas-porter-cuantitativas", "quantitative-porter-5-forces"],
    "pack-pestel": ["matriz-pestel-cuantitativa", "quantitative-pestel-matrix"],
    "pack-bcg": ["matriz-bcg-dinamica", "dynamic-bcg-matrix"],
    "pack-mckinsey": ["matriz-mckinsey-ge", "mckinsey-ge-matrix"],
    "pack-dar": ["matriz-dar-cuantitativa", "quantitative-dar-matrix"],
    "pack-rice": ["matriz-rice-ice-priorizacion", "rice-ice-prioritization-matrix"],
    "pack-business-case": ["business-case-financiero-van-tir", "financial-business-case-npv-irr"],
    "pack-raci": ["matriz-raci-balance-carga", "quantitative-raci-workload-matrix"],
    "pack-amfe": ["matriz-riesgos-amfe-fmea", "quantitative-risk-matrix-fmea"],
    "pack-pert": ["estimacion-pert-3-puntos", "stochastic-3-point-pert-estimation"],
    "pack-evm": ["cuadro-mando-evm-valor-ganado", "earned-value-management-evm-dashboard"],
    "pack-stock": ["calculadora-stock-seguridad-rop", "safety-stock-reorder-point-calculator", "safety-stock-rop-calculator"],
    "pack-sdd": ["sdd_vs_vibe_coding", "agentes_ia_operativa_sdd"],
    "suite-01": ["estrategia-corporativa-mba-framework-cuantitativo", "corporate-strategy-mba-quantitative-framework"],
    "suite-02": ["toma-decisiones-priorizacion-framework-cuantitativo", "decision-making-prioritization-quantitative-framework"],
    "suite-03": ["control-operativo-pmbok-framework-cuantitativo", "operational-control-pmbok-quantitative-framework"],
    "suite-sdd": ["sdd_vs_vibe_coding", "agentes_ia_operativa_sdd", "helix-parte1-especificacion-adn-escuadron-12-agentes"],
    "mega-bundle": ["executive-decision-packs-framework-cuantitativo", "executive-decision-packs-quantitative-framework", "packs-decisiones-ejecutivas-framework-cuantitativo"],
}


def _parse_asset_date(d: Any) -> Optional[date]:
    if not d:
        return None
    if isinstance(d, date):
        return d
    if isinstance(d, datetime):
        return d.date()
    try:
        return datetime.fromisoformat(str(d)).date()
    except Exception:
        return None


def analyze_release_editorial_impact(
    all_assets: List[Dict[str, Any]],
    metrics: Dict[str, Dict[str, Any]]
) -> List[ReleaseEditorialImpactItem]:
    """
    Evalúa determinísticamente el impacto y la cobertura editorial de los lanzamientos
    de aplicaciones, versiones evolutivas y kits/suites comerciales B2B.
    Identifica releases silenciosas sin post de actualización o artículos sin salida comercial.
    """
    posts = [a for a in all_assets if a.get("asset_type") == "post"]
    eval_assets = [
        a for a in all_assets
        if a.get("asset_type") in ("app", "kit", "suite", "mega_bundle")
    ]

    impact_items: List[ReleaseEditorialImpactItem] = []

    for item in eval_assets:
        aid = item["id"]
        atype = item["asset_type"]
        version = str(item.get("version") or "v1.0.0")
        rel_type = str(item.get("release_type") or "initial_launch")
        title_es = item.get("title_es") or aid
        pub_d = _parse_asset_date(item.get("publish_date"))
        status = item.get("status", "published")
        parent_slug = item.get("parent_asset_id") or item.get("slug") or aid
        editorial_post_slug = item.get("editorial_post_slug")

        # Cruce de posts vinculados
        matched_posts: List[Dict[str, Any]] = []
        for p in posts:
            pid = p.get("id")
            pslug = p.get("slug")

            # 1. Match directo con artículo editorial designado para la release
            if editorial_post_slug and (pid == editorial_post_slug or pslug == editorial_post_slug):
                matched_posts.append(p)
                continue

            # 2. Match por app y series
            if atype == "app":
                if p.get("related_app") == parent_slug or p.get("related_app") == aid:
                    matched_posts.append(p)
                elif parent_slug and parent_slug in str(pslug).lower():
                    matched_posts.append(p)
                elif p.get("series") and parent_slug and parent_slug.replace("-", "") in str(p.get("series")).lower().replace(" ", ""):
                    matched_posts.append(p)

            # 3. Match por kit / suite
            elif atype in ("kit", "suite", "mega_bundle"):
                guides = KIT_POST_MAPPING.get(aid, []) + KIT_POST_MAPPING.get(item.get("slug", ""), [])
                if pid in guides or pslug in guides:
                    matched_posts.append(p)
                elif p.get("related_kit") and (aid in str(p.get("related_kit")) or str(item.get("slug")) in str(p.get("related_kit"))):
                    matched_posts.append(p)

        # Desduplicar posts manteniendo el orden
        seen_pids = set()
        unique_posts: List[Dict[str, Any]] = []
        for p in matched_posts:
            if p["id"] not in seen_pids:
                seen_pids.add(p["id"])
                unique_posts.append(p)

        linked_count = len(unique_posts)
        views_30d = sum(int(metrics.get(p["id"], {}).get("ga4_views_30d", 0)) for p in unique_posts)

        pub_post_dates = [
            _parse_asset_date(p.get("publish_date"))
            for p in unique_posts
            if p.get("status") == "published" and _parse_asset_date(p.get("publish_date"))
        ]
        latest_post_date = max(pub_post_dates) if pub_post_dates else None
        has_scheduled_posts = any(p.get("status") == "scheduled" for p in unique_posts)

        # Determinar estado de cobertura editorial
        if status == "scheduled":
            if has_scheduled_posts:
                cov_status = "scheduled_coverage"
                action = f"Campaña programada: coordinar con E06 sindicación omnicanal para el estreno el {pub_d}."
            else:
                cov_status = "pending_launch"
                action = f"Lanzamiento programado el {pub_d}: coordinar con E01/E03 redacción anticipada de tutorial o post guía."
        else:
            if rel_type == "version_upgrade":
                if editorial_post_slug:
                    ed_post_obj = next(
                        (p for p in posts if p.get("id") == editorial_post_slug or p.get("slug") == editorial_post_slug),
                        None
                    )
                    if ed_post_obj and ed_post_obj.get("status") == "published":
                        cov_status = "covered"
                        action = f"Versión {version} cubierta con artículo propio publicado ({editorial_post_slug})."
                    else:
                        cov_status = "silent_release_alert"
                        action = f"Alerta de release silenciosa: versión {version} en producción pero artículo {editorial_post_slug} no publicado."
                else:
                    if not latest_post_date or (pub_d and pub_d > latest_post_date):
                        cov_status = "silent_release_alert"
                        action = f"Alerta de release silenciosa: versión {version} ({pub_d}) posterior al último post ({latest_post_date}); encargar a E03 nuevo post o destacar en Brevo Newsletter 2.0."
                    else:
                        cov_status = "covered"
                        action = f"Versión {version} respaldada por los artículos de la serie."
            else:
                if linked_count > 0 and latest_post_date:
                    cov_status = "covered"
                    action = f"Activo cubierto con {linked_count} post(s) en producción ({views_30d} vistas/30d)."
                else:
                    cov_status = "silent_release_alert"
                    action = "Alerta: activo en producción sin artículo guía o tutorial en el blog; planificar post en E01."

        impact_items.append(
            ReleaseEditorialImpactItem(
                asset_id=aid,
                asset_type=atype,
                version=version,
                release_type=rel_type,
                title_es=title_es,
                publish_date=pub_d,
                status=status,
                linked_posts_count=linked_count,
                latest_post_date=latest_post_date,
                editorial_views_30d=views_30d,
                editorial_coverage_status=cov_status,
                recommended_scriba_action=action,
            )
        )

    # Ordenar: silent_release_alert primero, luego pending_launch, scheduled_coverage, covered
    status_order = {"silent_release_alert": 0, "pending_launch": 1, "scheduled_coverage": 2, "covered": 3}
    impact_items.sort(key=lambda x: (status_order.get(x.editorial_coverage_status, 4), -(x.editorial_views_30d)))

    return impact_items


_SOCIAL_CHANNELS = frozenset({"linkedin", "x", "devto", "coderlegion"})


def analyze_channel_performance(
    channel_data: Optional[Dict[str, Any]],
) -> List[ChannelSummaryItem]:
    """Construye la matriz ordenada de rendimiento por canal canónico de adquisición (ADR-033)."""
    if not channel_data or not isinstance(channel_data, dict):
        return []
    by_channel = channel_data.get("by_channel") or {}
    if not isinstance(by_channel, dict):
        return []

    items: List[ChannelSummaryItem] = []
    for ch, raw in by_channel.items():
        if not isinstance(raw, dict):
            continue
        sessions = int(raw.get("sessions_30d", 0) or 0)
        prev_sessions = int(raw.get("sessions_prev_30d", 0) or 0)
        key_ev = int(raw.get("key_events_30d", 0) or 0)
        if sessions == 0 and prev_sessions == 0 and key_ev == 0:
            continue
        items.append(
            ChannelSummaryItem(
                channel=ch,  # type: ignore[arg-type]
                sessions_30d=sessions,
                sessions_es_30d=int(raw.get("sessions_es_30d", 0) or 0),
                sessions_en_30d=int(raw.get("sessions_en_30d", 0) or 0),
                en_share_pct=float(raw.get("en_share_pct", 0.0) or 0.0),
                users_30d=int(raw.get("users_30d", 0) or 0),
                engaged_sessions_30d=int(raw.get("engaged_sessions_30d", 0) or 0),
                engagement_rate_pct=float(raw.get("engagement_rate_pct", 0.0) or 0.0),
                avg_engagement_sec=float(raw.get("avg_engagement_sec", 0.0) or 0.0),
                key_events_30d=key_ev,
                conversion_rate_pct=float(raw.get("conversion_rate_pct", 0.0) or 0.0),
                sessions_prev_30d=prev_sessions,
                trend_30d_pct=float(raw.get("trend_30d_pct", 0.0) or 0.0),
            )
        )

    items.sort(key=lambda x: (x.sessions_30d, x.key_events_30d), reverse=True)
    return items


def detect_hidden_channel_winners(
    published_posts: List[Dict[str, Any]],
    channel_data: Optional[Dict[str, Any]],
    *,
    min_engagement_sec: float = 45.0,
    max_sessions: int = 30,
    min_sessions: int = 2,
) -> List[HiddenChannelWinnerItem]:
    """
    Detecta activos con alta retención (>= 45s) o conversiones en canales sociales
    (linkedin, x, devto, coderlegion) pero bajo volumen (< 30 sesiones) candidatos a reciclaje +21d.
    """
    if not channel_data or not isinstance(channel_data, dict):
        return []
    by_asset = channel_data.get("by_asset") or {}
    if not isinstance(by_asset, dict):
        return []

    post_lookup = {p["id"]: p for p in published_posts}
    winners: List[HiddenChannelWinnerItem] = []

    for aid, ch_map in by_asset.items():
        if aid not in post_lookup or not isinstance(ch_map, dict):
            continue
        post = post_lookup[aid]
        for ch, vals in ch_map.items():
            if ch not in _SOCIAL_CHANNELS or not isinstance(vals, dict):
                continue
            sessions = int(vals.get("sessions_30d", 0) or 0)
            avg_eng = float(vals.get("avg_engagement_sec", 0.0) or 0.0)
            key_ev = int(vals.get("key_events_30d", 0) or 0)

            if min_sessions <= sessions < max_sessions and (avg_eng >= min_engagement_sec or key_ev >= 1):
                action = (
                    f"Ola de reciclaje +21d en E06 ({ch}): nuevo ángulo/hilo visual con CTA a Sandbox/Kit "
                    f"(retención {avg_eng:.0f}s, {key_ev} conv. con solo {sessions} sesiones)."
                )
                winners.append(
                    HiddenChannelWinnerItem(
                        asset_id=aid,
                        slug=post.get("slug", aid),
                        title_es=post.get("title_es") or post.get("title_en") or aid,
                        channel=ch,  # type: ignore[arg-type]
                        sessions_30d=sessions,
                        avg_engagement_sec=round(avg_eng, 1),
                        key_events_30d=key_ev,
                        recommended_action=action,
                    )
                )

    winners.sort(key=lambda w: (w.key_events_30d, w.avg_engagement_sec, w.sessions_30d), reverse=True)
    return winners


def detect_dark_social_alerts(
    channel_data: Optional[Dict[str, Any]],
    dispatch_queue_path: Path = DISPATCH_QUEUE_PATH,
) -> List[DarkSocialAlertItem]:
    """
    Detecta fugas de atribución UTM / Dark Social:
    1) Pico > +50% en tráfico `direct` en las 48h posteriores a un despacho completado sin alza correlativa en el canal UTM.
    2) Crecimiento macro > +50% de `direct` (con >= 20 sesiones) representando > 40% del tráfico total y social UTM < 10%.
    """
    if not channel_data or not isinstance(channel_data, dict):
        return []

    alerts: List[DarkSocialAlertItem] = []
    daily_map = channel_data.get("daily_by_channel") or {}

    # Regla 1: cruce diario 48h con dispatch_queue.yaml
    if isinstance(daily_map, dict) and daily_map and dispatch_queue_path.exists():
        direct_series = [int((vals or {}).get("direct", 0) or 0) for vals in daily_map.values()]
        baseline = float(statistics.median(direct_series)) if direct_series else 0.0
        try:
            with open(dispatch_queue_path, "r", encoding="utf-8") as f:
                q_data = yaml.safe_load(f) or {}
            entries = q_data.get("entries", []) or []
        except Exception:
            entries = []

        for entry in entries:
            if not isinstance(entry, dict) or entry.get("status") != "completed":
                continue
            exec_ts = entry.get("executed_at_utc") or entry.get("scheduled_at_utc")
            if not exec_ts:
                continue
            try:
                d0 = datetime.fromisoformat(str(exec_ts).replace("Z", "+00:00")).date()
            except Exception:
                continue

            d1 = date.fromordinal(d0.toordinal() + 1)
            win_days = [d0.isoformat(), d1.isoformat()]
            present_days = [d for d in win_days if d in daily_map]
            if not present_days:
                continue

            direct_win = sum(int(daily_map[d].get("direct", 0) or 0) for d in present_days)
            expected_base = baseline * len(present_days)
            channels_list = [str(c).lower() for c in (entry.get("channels") or []) if str(c).lower() in _SOCIAL_CHANNELS]
            utm_win = sum(
                int(daily_map[d].get(ch, 0) or 0)
                for d in present_days
                for ch in channels_list
            )
            if direct_win >= 10 and expected_base > 0:
                spike_pct = round(((direct_win - expected_base) / expected_base) * 100.0, 1)
                if spike_pct > 50.0 and utm_win < max(3, direct_win * 0.2):
                    expected_ch = ",".join(channels_list) if channels_list else "social"
                    alerts.append(
                        DarkSocialAlertItem(
                            alert_type="dark_social_spike",
                            dispatch_id=str(entry.get("id") or ""),
                            channel_expected=expected_ch,
                            direct_sessions_current=direct_win,
                            direct_sessions_baseline=round(expected_base, 1),
                            spike_pct=spike_pct,
                            severity="high",
                            recommended_action=(
                                f"Pico +{spike_pct:.0f}% de tráfico (direct) tras despacho '{entry.get('id')}' "
                                f"con solo {utm_win} sesiones UTM en [{expected_ch}]. Verificar UTMs ADR-033 en enlaces compartidos."
                            ),
                        )
                    )

    # Regla 2: alerta macro 30d si direct domina sin atribución social correlativa
    by_ch = channel_data.get("by_channel") or {}
    if isinstance(by_ch, dict) and by_ch:
        direct_obj = by_ch.get("direct") or {}
        d_cur = int(direct_obj.get("sessions_30d", 0) or 0)
        d_prev = int(direct_obj.get("sessions_prev_30d", 0) or 0)
        total_sess = sum(int((v or {}).get("sessions_30d", 0) or 0) for v in by_ch.values())
        social_sess = sum(int((by_ch.get(ch) or {}).get("sessions_30d", 0) or 0) for ch in _SOCIAL_CHANNELS)
        if d_cur >= 20 and d_prev > 0 and total_sess > 0:
            macro_spike = round(((d_cur - d_prev) / d_prev) * 100.0, 1)
            direct_share = (d_cur / total_sess) * 100.0
            social_share = (social_sess / total_sess) * 100.0
            if macro_spike > 50.0 and direct_share > 40.0 and social_share < 10.0:
                alerts.append(
                    DarkSocialAlertItem(
                        alert_type="high_direct_share",
                        dispatch_id=None,
                        channel_expected="linkedin,x,devto,coderlegion",
                        direct_sessions_current=d_cur,
                        direct_sessions_baseline=float(d_prev),
                        spike_pct=macro_spike,
                        severity="medium",
                        recommended_action=(
                            f"Tráfico directo creció +{macro_spike:.0f}% ({direct_share:.1f}% del total) "
                            f"mientras atribución social UTM es {social_share:.1f}%. Auditar enlaces manuales en bio/comentarios."
                        ),
                    )
                )

    return alerts


def extract_brand_query_totals(
    gsc_queries_data: Optional[Dict[str, Any]] = None,
) -> Tuple[int, int]:
    """Suma clics e impresiones de consultas de marca (`datalaria`) desde gsc_queries.json."""
    if gsc_queries_data is None:
        if not GSC_QUERIES_PATH.exists():
            return 0, 0
        try:
            with open(GSC_QUERIES_PATH, "r", encoding="utf-8") as f:
                gsc_queries_data = json.load(f)
        except Exception:
            return 0, 0

    summary = gsc_queries_data.get("summary") or {}
    if "brand_clicks" in summary or "brand_impressions" in summary:
        return int(summary.get("brand_clicks", 0) or 0), int(summary.get("brand_impressions", 0) or 0)

    by_page = gsc_queries_data.get("by_page") or {}
    b_clicks = 0
    b_impr = 0
    for qlist in by_page.values():
        if not isinstance(qlist, list):
            continue
        for qrow in qlist:
            q_str = str(qrow.get("query") or "").lower()
            if qrow.get("is_brand_query") or "datalaria" in q_str:
                b_clicks += int(qrow.get("clicks", 0) or 0)
                b_impr += int(qrow.get("impressions", 0) or 0)
    return b_clicks, b_impr


def calculate_ptr_pct(ga4_sessions: int, native_views: int) -> float:
    """
    Calcula determinísticamente la Tasa de Traspaso (Pull-Through Rate, PTR %) desde una comunidad
    externa hacia datalaria.com: round((ga4_sessions / max(native_views, 1)) * 100, 2) (ADR-033).
    """
    if native_views <= 0:
        return 0.0
    return round((max(0, int(ga4_sessions)) / int(native_views)) * 100.0, 2)


def summarize_social_platforms(
    social_data: Optional[Dict[str, Any]],
    channel_data: Optional[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """
    Cruza métricas nativas de Dev.to y CoderLegion (`social_metrics.json`) con sesiones GA4
    (`channel_metrics.json`) para resumir el embudo Top-of-Funnel -> PTR %.
    """
    platforms = (social_data or {}).get("platforms") if isinstance(social_data, dict) else {}
    if not isinstance(platforms, dict):
        platforms = {}
    by_channel = (channel_data or {}).get("by_channel") if isinstance(channel_data, dict) else {}
    if not isinstance(by_channel, dict):
        by_channel = {}

    summary: Dict[str, Dict[str, Any]] = {}
    for plat in ("devto", "coderlegion"):
        p_obj = platforms.get(plat) if isinstance(platforms.get(plat), dict) else {}
        ch_obj = by_channel.get(plat) if isinstance(by_channel.get(plat), dict) else {}
        views = int(p_obj.get("total_views", 0) or 0)
        reactions = int(p_obj.get("total_reactions", 0) or 0)
        comments = int(p_obj.get("total_comments", 0) or 0)
        articles_cnt = int(p_obj.get("articles_count", 0) or 0)
        matched_cnt = int(p_obj.get("matched_assets_count", 0) or 0)
        ga4_sess = int(ch_obj.get("sessions_30d", 0) or 0)
        ptr = calculate_ptr_pct(ga4_sess, views)
        summary[plat] = {
            "platform": plat,
            "status": str(p_obj.get("status") or "unavailable"),
            "last_synced_at": p_obj.get("last_synced_at"),
            "articles_count": articles_cnt,
            "matched_assets_count": matched_cnt,
            "native_views": views,
            "native_reactions": reactions,
            "native_comments": comments,
            "ga4_sessions_30d": ga4_sess,
            "ptr_pct": ptr,
        }

    li_obj = platforms.get("linkedin_company") if isinstance(platforms.get("linkedin_company"), dict) else {}
    li_ch = by_channel.get("linkedin") if isinstance(by_channel.get("linkedin"), dict) else {}
    li_impr = int(li_obj.get("total_impressions", 0) or 0)
    li_clicks = int(li_obj.get("total_clicks", 0) or 0)
    li_react = int(li_obj.get("total_reactions", 0) or 0)
    li_comm = int(li_obj.get("total_comments", 0) or 0)
    li_shares = int(li_obj.get("total_shares", 0) or 0)
    li_foll = int(li_obj.get("followers_count", 0) or 0)
    li_posts = int(li_obj.get("posts_count", 0) or 0)
    li_matched = int(li_obj.get("matched_assets_count", 0) or 0)
    li_ga4_sess = int(li_ch.get("sessions_30d", 0) or 0)
    li_ctr = float(li_obj.get("native_ctr_pct", 0.0) or 0.0)
    if li_ctr == 0.0 and li_impr > 0:
        li_ctr = round((li_clicks / li_impr) * 100.0, 2)
    li_ptr = calculate_ptr_pct(li_ga4_sess, li_impr if li_impr > 0 else li_clicks)

    summary["linkedin_company"] = {
        "platform": "linkedin_company",
        "status": str(li_obj.get("status") or "unavailable"),
        "source": str(li_obj.get("source") or "none"),
        "scope": "company_page_only",
        "last_synced_at": li_obj.get("last_synced_at"),
        "posts_count": li_posts,
        "matched_assets_count": li_matched,
        "native_views": li_impr,
        "total_impressions": li_impr,
        "total_clicks": li_clicks,
        "native_ctr_pct": li_ctr,
        "total_reactions": li_react,
        "total_comments": li_comm,
        "total_shares": li_shares,
        "followers_count": li_foll,
        "ga4_sessions_30d": li_ga4_sess,
        "ptr_pct": li_ptr,
    }

    x_ch = by_channel.get("x") if isinstance(by_channel.get("x"), dict) else {}
    x_obj = platforms.get("x") if isinstance(platforms.get("x"), dict) else {}
    summary["x"] = {
        "platform": "x",
        "status": "standby_zero_cost",
        "last_synced_at": None,
        "ga4_sessions_30d": int(x_ch.get("sessions_30d", 0) or 0),
        "note": str(x_obj.get("note") or "Medición activa vía GA4 + UTMs (Hito 7.11); API nativa X en stand-by por coste > 0 EUR"),
    }
    return summary


def build_channel_category_matrix(
    assets: List[Dict[str, Any]],
    channel_data: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Construye la matriz determinista Canal × Categoría × Idioma (ES vs. EN) cruzando `by_asset`
    de `channel_metrics.json` con el catálogo de `index.json` (Hito 7.14 / ADR-033).
    """
    if not channel_data or not isinstance(channel_data, dict):
        return []
    by_asset = channel_data.get("by_asset")
    if not isinstance(by_asset, dict):
        return []

    asset_cat: Dict[str, str] = {}
    for a in assets:
        if isinstance(a, dict) and a.get("id"):
            asset_cat[str(a["id"])] = str(a.get("category") or "General")

    buckets: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for aid, ch_map in by_asset.items():
        if not isinstance(ch_map, dict):
            continue
        cat = asset_cat.get(aid, "General")
        for ch_name, vals in ch_map.items():
            if not isinstance(vals, dict):
                continue
            s_tot = int(vals.get("sessions_30d", 0) or 0)
            s_es = int(vals.get("sessions_es_30d", 0) or 0)
            s_en = int(vals.get("sessions_en_30d", 0) or 0)
            k_ev = int(vals.get("key_events_30d", 0) or 0)
            avg_eng = float(vals.get("avg_engagement_sec", 0.0) or 0.0)
            if s_tot <= 0:
                continue

            key = (str(ch_name), cat)
            b = buckets.setdefault(
                key,
                {
                    "channel": str(ch_name),
                    "category": cat,
                    "sessions_30d": 0,
                    "sessions_es_30d": 0,
                    "sessions_en_30d": 0,
                    "key_events_30d": 0,
                    "_eng_weighted": 0.0,
                },
            )
            b["sessions_30d"] += s_tot
            b["sessions_es_30d"] += s_es
            b["sessions_en_30d"] += s_en
            b["key_events_30d"] += k_ev
            b["_eng_weighted"] += avg_eng * s_tot

    rows: List[Dict[str, Any]] = []
    for b in buckets.values():
        sess = b["sessions_30d"]
        en_share = round((b["sessions_en_30d"] / sess) * 100.0, 1) if sess > 0 else 0.0
        avg_e = round(b["_eng_weighted"] / sess, 1) if sess > 0 else 0.0
        rows.append(
            {
                "channel": b["channel"],
                "category": b["category"],
                "sessions_30d": sess,
                "sessions_es_30d": b["sessions_es_30d"],
                "sessions_en_30d": b["sessions_en_30d"],
                "en_share_pct": en_share,
                "key_events_30d": b["key_events_30d"],
                "avg_engagement_sec": avg_e,
            }
        )
    rows.sort(key=lambda r: (r["sessions_30d"], r["key_events_30d"]), reverse=True)
    return rows


def detect_ptr_leak_alerts(
    published_posts: List[Dict[str, Any]],
    social_data: Optional[Dict[str, Any]],
    channel_data: Optional[Dict[str, Any]],
    *,
    min_native_views: int = 300,
    max_ptr_pct: float = 2.0,
) -> List[PullThroughAlertItem]:
    """
    Regla 1 (ADR-033): Detecta artículos sindicados en Dev.to o CoderLegion con >= 300 vistas nativas
    pero PTR < 2.0% hacia datalaria.com (Fuga de Traspaso).
    """
    if not social_data or not isinstance(social_data, dict):
        return []
    social_by_asset = social_data.get("by_asset") or {}
    if not isinstance(social_by_asset, dict):
        return []
    channel_by_asset = (
        channel_data.get("by_asset")
        if (channel_data and isinstance(channel_data, dict) and isinstance(channel_data.get("by_asset"), dict))
        else {}
    )

    alerts: List[PullThroughAlertItem] = []
    for post in published_posts:
        pid = post["id"]
        plat_map = social_by_asset.get(pid)
        if not isinstance(plat_map, dict):
            continue
        for plat in ("devto", "coderlegion", "linkedin_company"):
            p_vals = plat_map.get(plat)
            if not isinstance(p_vals, dict):
                continue
            native_views = int(p_vals.get("views", 0) or p_vals.get("impressions", 0) or 0)
            if native_views < min_native_views:
                continue
            native_reactions = int(p_vals.get("reactions", 0) or 0)
            native_comments = int(p_vals.get("comments", 0) or 0)
            ch_key = "linkedin" if plat == "linkedin_company" else plat
            ga4_sess = int(
                ((channel_by_asset.get(pid) or {}).get(ch_key) or {}).get("sessions_30d", 0) or 0
            )
            ptr = calculate_ptr_pct(ga4_sess, native_views)
            if ptr < max_ptr_pct:
                action = (
                    f"Fuga de traspaso en {plat} ({native_views:,} vistas nativas, solo {ga4_sess} sesiones GA4 · PTR {ptr:.2f}%): "
                    f"insertar en el primer 25% del post sindicado un CTA interactivo al Sandbox/Calculadora en vivo (`utm_content=inline_sandbox_cta`)."
                )
                alerts.append(
                    PullThroughAlertItem(
                        asset_id=pid,
                        slug=post.get("slug", pid),
                        title_es=post.get("title_es") or post.get("title_en") or pid,
                        platform=plat,  # type: ignore[arg-type]
                        native_views=native_views,
                        native_reactions=native_reactions,
                        native_comments=native_comments,
                        ga4_sessions_30d=ga4_sess,
                        ptr_pct=ptr,
                        recommended_action=action,
                    )
                )

    alerts.sort(key=lambda a: (a.native_views, -a.ptr_pct), reverse=True)
    return alerts


def detect_canonical_shield_alerts(
    published_posts: List[Dict[str, Any]],
    social_data: Optional[Dict[str, Any]],
    metrics: Dict[str, Dict[str, Any]],
    *,
    min_native_views: int = 500,
    min_days_published: int = 21,
) -> List[CanonicalShieldAlertItem]:
    """
    Regla 5 (ADR-033): Detecta artículos sindicados en Dev.to o CoderLegion con >= 500 vistas nativas
    mientras la URL canónica en datalaria.com lleva > 21 días publicada con 0 impresiones en GSC.
    """
    if not social_data or not isinstance(social_data, dict):
        return []
    social_by_asset = social_data.get("by_asset") or {}
    if not isinstance(social_by_asset, dict):
        return []

    today = date.today()
    alerts: List[CanonicalShieldAlertItem] = []

    for post in published_posts:
        pid = post["id"]
        pub_d = _parse_asset_date(post.get("publish_date"))
        if not pub_d:
            continue
        days = (today - pub_d).days
        if days <= min_days_published:
            continue

        gsc_impr = int(metrics.get(pid, {}).get("gsc_impressions_30d", 0) or 0)
        if gsc_impr > 0:
            continue

        plat_map = social_by_asset.get(pid)
        if not isinstance(plat_map, dict):
            continue

        for plat in ("devto", "coderlegion"):
            p_vals = plat_map.get(plat)
            if not isinstance(p_vals, dict):
                continue
            native_views = int(p_vals.get("views", 0) or 0)
            if native_views < min_native_views:
                continue
            canon_path = post.get("url_en") or post.get("url_es") or f"/en/posts/{post.get('slug', pid)}/"
            canon_url = f"https://datalaria.com{canon_path}" if str(canon_path).startswith("/") else str(canon_path)
            action = (
                f"Posible canibalización externa en {plat} ({native_views:,} vistas nativas vs. 0 imp. GSC tras {days}d): "
                f"verificar canonical_url/source_url hacia {canon_url}, solicitar indexación en GSC y retrasar Ola 3 a +72h."
            )
            alerts.append(
                CanonicalShieldAlertItem(
                    asset_id=pid,
                    slug=post.get("slug", pid),
                    title_es=post.get("title_es") or post.get("title_en") or pid,
                    platform=plat,  # type: ignore[arg-type]
                    native_views=native_views,
                    gsc_impressions_30d=gsc_impr,
                    days_since_publish=days,
                    canonical_url=canon_url,
                    recommended_action=action,
                )
            )

    alerts.sort(key=lambda a: (a.native_views, a.days_since_publish), reverse=True)
    return alerts


def generate_impact_report_markdown(
    report: PulseImpactReport,
    catalog_meta: Optional[Dict[str, Any]] = None,
) -> str:
    """Genera el informe ejecutivo completo en Markdown 100 % dinámico firmado por E02."""
    now_str = report.generated_at.strftime("%Y-%m-%d %H:%M UTC")
    meta = catalog_meta or {}

    total_assets = meta.get("total_assets", report.total_published_posts + report.total_scheduled_posts)
    total_posts = meta.get("total_posts", report.total_published_posts + report.total_scheduled_posts)
    draft_posts = meta.get("draft_posts", 0)
    apps_count = meta.get("apps_count", 0)
    kits_count = meta.get("kits_count", 0)
    months_count = meta.get("months_count", 0)
    m_initial_label = meta.get("m_initial_label", "inicio")
    m_initial_views = meta.get("m_initial_views", 0)
    m_peak_label = meta.get("m_peak_label", "pico")
    m_peak_views = meta.get("m_peak_views", 0)

    avg_backlog_score = (
        round(sum(b.editorial_roi_score for b in report.prioritized_backlog) / len(report.prioritized_backlog), 1)
        if report.prioritized_backlog
        else 0.0
    )

    leader_cat = report.category_performance[0] if report.category_performance else None
    leader_label = f"{leader_cat.category} ({leader_cat.monetization_coverage_pct:.1f}%)" if leader_cat else "N/A"
    gsc_opp_count = sum(1 for qw in report.quick_wins_ctr if qw.opportunity_type == "gsc_position_4_20")

    md = f"""# 📈 Primera Auditoría Estratégica de Impacto SEO, Tráfico y Monetización (E02)

> **Autor:** [`E02-seo-impact-strategist`](file:///c:/Users/dalae/OneDrive/Emprendiendo/datalaria/specs/squad-editorial/E02-seo-impact-strategist.md) · **Célula:** Dirección & Inteligencia Estratégica  
> **Fecha de Emisión:** {now_str}  
> **Fuentes de Verdad:** `data/pulse/private/index.json` ({total_assets} activos), `metrics.json` (GA4 + GSC 30d/prev 30d), `channel_metrics.json` (GA4 Acquisition + KeyEvents), `social_metrics.json` (Dev.to + CoderLegion APIs gratuitas), `distribution_ledger.json`, `gsc_queries.json`, `monthly_metrics.json` ({months_count} meses) y `backlog.yaml`.  
> **Invariantes:** Cumple estrictamente `INV-PULSE-6`, `INV-PULSE-11`, `INV-PULSE-12` (`ADR-033`, coste `0 €`) y Constitución Art. 1.3 (*Separación Cerebro vs. Músculo Cuantitativo*).

---

## 1. Resumen Ejecutivo y Estado del Catálogo

| Métrica Macro | Valor Cuantitativo Real | Interpretación Estratégica E02 |
| :--- | :---: | :--- |
| **Total Activos Consolidados** | **{total_assets} activos** | {total_posts} Posts bilingües (`{report.total_published_posts}` publicados, `{report.total_scheduled_posts}` programados, `{draft_posts}` drafts), `{apps_count}` Apps base y `{kits_count}` Kits/Suites. |
| **Tráfico Acumulado Posts (30d)** | **{report.total_30d_post_views:,} vistas** | Cuota inglés (EN): **{report.en_views_share_pct:.1f}%** · Mediana: **{report.median_post_views:.1f}** · $P_{{75}}$: **{report.p75_post_views:.1f}**. |
| **Visibilidad Orgánica GSC (30d)** | **{report.total_30d_gsc_impressions:,} imp. · {report.total_30d_gsc_clicks:,} clics** | CTR medio: **{report.avg_gsc_ctr_pct:.2f}%** · Posición media ponderada: **{report.avg_gsc_position:.1f}** · Cuota EN (imp.): **{report.en_gsc_impressions_share_pct:.1f}%** · Prev 30d: `{report.gsc_impressions_prev_30d:,}` imp. / `{report.gsc_clicks_prev_30d:,}` clics · Marca (`datalaria`): `{report.gsc_brand_impressions_30d:,}` imp. / `{report.gsc_brand_clicks_30d:,}` clics. |
| **Crecimiento Interanual (YoY)** | **+{report.monthly_growth_yoy_pct:.1f}%** | De {m_initial_views:,} vistas ({m_initial_label}) a {m_peak_views:,} vistas ({m_peak_label}). |
| **Quick Wins de CTR / SERP** | **{len(report.quick_wins_ctr)} oportunidades** | `{gsc_opp_count}` con impresiones reales GSC (`pos 4..20` o `CTR < 2.5%`) + truncamientos SERP. |
| **Canibalización de Keywords** | **{len(report.cannibalization_alerts)} alertas** | Consultas GSC donde `>= 2` URLs del mismo idioma compiten por impresiones. |
| **Huérfanos de Monetización** | **{len(report.monetization_orphans)} posts top** | Posts en el cuartil superior ($P_{{75}} \\ge {report.p75_post_views:.0f}$) sin enlace ni shortcode a Kit/App. |
| **Score Promedio del Backlog** | **{avg_backlog_score:.1f} / 100** | {len(report.prioritized_backlog)} propuestas estratégicas evaluadas por Editorial ROI Score. |

```mermaid
flowchart TD
    A["{report.total_published_posts} Artículos Publicados\\n({report.total_30d_post_views:,} vistas · {report.total_30d_gsc_impressions:,} imp. GSC)"] --> B{{"Triaje de Impacto E02"}}
    B --> C["{len(report.quick_wins_ctr)} Quick Wins de CTR\\n({gsc_opp_count} oportunidades GSC reales)"]
    B --> D["{len(report.monetization_orphans)} Huérfanos de Monetización\\n(Cuartil Superior >= {report.p75_post_views:.0f} vistas sin Kit)"]
    B --> E["{len(report.category_performance)} Categorías Evaluadas\\n(Líder: {leader_label})"]
    B --> H["{len(report.cannibalization_alerts)} Alertas Canibalización GSC"]
    C --> F["Acción E04: Reescritura Títulos & H1 (35-95)"]
    D --> G["Acción E05: Inyección app-ref y Kits 19€"]
```

---

## 2. Rendimiento, GSC y Cobertura de Monetización por Categoría (ES vs. EN)

| Categoría Oficial | Posts | Vistas 30d | % EN (Vistas) | Imp. GSC | Clics GSC | CTR GSC | Eng. Medio | Monetizados | Cobertura % | Editorial ROI Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    for c in report.category_performance:
        md += (
            f"| **{c.category}** | {c.published_posts} | {c.total_views_30d} ({c.avg_views_per_post:.1f}/p) | "
            f"{c.en_traffic_share_pct:.1f}% | {c.total_gsc_impressions_30d:,} | {c.total_gsc_clicks_30d:,} | "
            f"{c.avg_gsc_ctr_pct:.2f}% | {c.avg_engagement_sec:.1f}s | {c.monetized_posts}/{c.published_posts} | "
            f"**{c.monetization_coverage_pct:.1f}%** | **{c.editorial_roi_score:.1f}** |\n"
        )

    md += "\n### Diagnóstico Estratégico de Categorías:\n"
    for idx, c in enumerate(report.category_performance[:3], 1):
        md += (
            f"{idx}. **{c.category} (Editorial ROI {c.editorial_roi_score:.1f}):** "
            f"**{c.avg_views_per_post:.1f} vistas/post**, **{c.total_gsc_impressions_30d:,} impresiones GSC** "
            f"(CTR **{c.avg_gsc_ctr_pct:.2f}%**), cuota inglés **{c.en_traffic_share_pct:.1f}%** y "
            f"**{c.monetization_coverage_pct:.1f}%** de cobertura comercial ({c.monetized_posts}/{c.published_posts}).\n"
        )

    md += """
---

## 3. Matriz de Quick Wins de CTR (Top Oportunidades en Buscadores)

Artículos priorizados combinando datos reales de **Google Search Console** (impresiones, posición media y CTR) con longitud de snippet y retención en GA4:

| ID / Activo | Top Query GSC | Imp. GSC | Pos. / CTR | Vistas 30d | Tipo de Oportunidad | Título Recomendado ES (35–95 chars) |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
"""
    for qw in report.quick_wins_ctr[:12]:
        tq = f"`{qw.top_query}`" if qw.top_query else "—"
        pos_ctr = f"`{qw.gsc_avg_position:.1f}` / `{qw.gsc_ctr_pct:.1f}%`" if qw.gsc_impressions_30d > 0 else "—"
        md += (
            f"| [`{qw.id}`]({qw.slug}) | {tq} | **{qw.gsc_impressions_30d:,}** | {pos_ctr} | "
            f"{qw.ga4_views_30d} | `{qw.opportunity_type}` | **{qw.recommended_title_es}** |\n"
        )

    md += f"""
---

## 4. Auditoría de Huérfanos de Monetización (Cuartil Superior de Tráfico)

Artículos en el cuartil superior ($P_{{75}} \\ge {report.p75_post_views:.0f}$ vistas) que actualmente no enlazan a ningún Kit de Lemon Squeezy ni a ninguna App de Datalaria:

| ID del Post | Vistas 30d | Percentil | Tipo de Puente | Destino Asignado | Shortcode / Enlace Recomendado | Justificación Estratégica E02 |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- |
"""
    if report.monetization_orphans:
        for o in report.monetization_orphans:
            md += f"| [`{o.id}`]({o.slug}) | **{o.ga4_views_30d}** | Top {100 - o.rank_pct}% | `{o.recommended_bridge_type}` | `{o.recommended_target_id}` | `{o.recommended_shortcode_or_url}` | {o.rationale_es} |\n"
    else:
        md += "| — | — | — | — | — | — | ✅ Sin huérfanos de monetización en el cuartil superior. |\n"

    md += """
---

## 5. Priorización del Backlog Prospectivo (`Editorial ROI Score`)

Ideas de contenido futuro en `data/editorial/backlog.yaml` ordenadas determinísticamente por la fórmula de ROI editorial de `E02`:

$$\\text{Editorial ROI Score} = 0.40 \\times \\text{Demanda SEO} + 0.35 \\times \\text{Fit Monetización} + 0.25 \\times \\text{Sinergia Ecosistema}$$

| Pos. | ID de Idea | Título Propuesto | Categoría | Target de Negocio | SEO | Mon. | Sin. | Editorial ROI |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
"""
    for i, b in enumerate(report.prioritized_backlog, 1):
        md += f"| **#{i}** | `{b.id}` | {b.title_es} | {b.category} | `{b.target_kit_or_app}` | {b.seo_demand_score:.0f} | {b.monetization_fit_score:.0f} | {b.ecosystem_synergy_score:.0f} | **{b.editorial_roi_score:.1f}** |\n"

    md += f"""
---

## 6. Impacto Editorial de Lanzamientos de Apps, Versiones y Kits B2B (Gobernanza Scriba)

> **Invariantes SDD:** Supervisión determinista de estrenos (`initial_launch`, `kit_launch`) y versiones evolutivas (`version_upgrade`, `kit_edition`).  
> **Balance General:** {len(report.release_editorial_impact)} activos evaluados · **{report.silent_releases_count} alerta(s) de release silenciosa** · {sum(1 for r in report.release_editorial_impact if r.editorial_coverage_status == 'scheduled_coverage')} cobertura(s) programada(s) · {sum(1 for r in report.release_editorial_impact if r.editorial_coverage_status == 'covered')} cubierto(s) al 100%.

| Activo / ID | Tipo & Versión | Fecha Estreno | Estado Portal | Posts | Último Post | Vistas 30d | Cobertura Scriba | Acción Recomendada |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
"""
    for r in report.release_editorial_impact:
        badge = {
            "silent_release_alert": "🔴 Alerta Silenciosa",
            "pending_launch": "🟡 Lanzamiento Pendiente",
            "scheduled_coverage": "🟢 Cobertura Programada",
            "covered": "✅ Cubierto"
        }.get(r.editorial_coverage_status, r.editorial_coverage_status)
        pub_d_str = str(r.publish_date) if r.publish_date else "Pendiente"
        latest_str = str(r.latest_post_date) if r.latest_post_date else "Ninguno"
        md += f"| `{r.asset_id}` | `{r.release_type}` ({r.version}) | {pub_d_str} | `{r.status}` | {r.linked_posts_count} | {latest_str} | {r.editorial_views_30d} | {badge} | {r.recommended_scriba_action} |\n"

    md += """
---

## 7. Auditoría de Canibalización de Keywords (GSC)

Consultas reales de Search Console donde `>= 2` URLs del mismo idioma compiten por impresiones:

| Query | Idioma | Imp. Totales | Clics | URLs en Competencia (Top 3) | Acción Recomendada E02 |
| :--- | :---: | :---: | :---: | :--- | :--- |
"""
    if report.cannibalization_alerts:
        for ca in report.cannibalization_alerts[:15]:
            urls_desc = " · ".join(f"`{u['url']}` ({u['impressions']} imp, pos {u['position']})" for u in ca.competing_urls[:3])
            md += f"| `{ca.query}` | `{ca.lang}` | **{ca.total_impressions:,}** | {ca.total_clicks} | {urls_desc} | {ca.recommended_action} |\n"
    else:
        md += "| — | — | 0 | 0 | — | ✅ Sin canibalizaciones significativas detectadas (`>= 20` imp.). |\n"

    md += """
---

## 8. Rendimiento por Canal de Adquisición (ES vs. EN) — Coste 0 € (`ADR-033`)

> **Política `INV-PULSE-12`:** Atribución unificada vía GA4 Acquisition + UTMs (`linkedin`, `x`, `devto`, `coderlegion`, `newsletter`, `google_organic`, `direct`). **X/Twitter nativo permanece en stand-by (coste `0 €`)**; **LinkedIn cubre exclusivamente la Página de Empresa**.

| Canal Canónico | Sesiones 30d | ES / EN | % EN | Δ 30d | Eng. Rate % | Eng. Medio | Eventos Clave | Conv. % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    if report.channel_summary:
        for ch in report.channel_summary:
            delta_sign = "+" if ch.trend_30d_pct > 0 else ""
            md += (
                f"| **`{ch.channel}`** | **{ch.sessions_30d:,}** | {ch.sessions_es_30d} / {ch.sessions_en_30d} | "
                f"{ch.en_share_pct:.1f}% | {delta_sign}{ch.trend_30d_pct:.1f}% | {ch.engagement_rate_pct:.1f}% | "
                f"{ch.avg_engagement_sec:.1f}s | {ch.key_events_30d} | {ch.conversion_rate_pct:.2f}% |\n"
            )
    else:
        md += "| — | 0 | 0 / 0 | 0.0% | 0.0% | 0.0% | 0.0s | 0 | 0.00% |\n"
        md += "\n*Nota: Ejecuta `python -m ops.pulse.sync_metrics` con `service_account.json` para poblar `channel_metrics.json` con datos reales de GA4 Acquisition.*\n"

    md += """
### 🏆 Ganadores Ocultos por Canal (Candidatos a Ola de Reciclaje +21d en `E06`)

| Activo / ID | Canal | Sesiones 30d | Eng. Medio | Eventos Clave | Acción Recomendada E06 |
| :--- | :---: | :---: | :---: | :---: | :--- |
"""
    if report.hidden_channel_winners:
        for hw in report.hidden_channel_winners[:10]:
            md += (
                f"| [`{hw.asset_id}`]({hw.slug}) | `{hw.channel}` | {hw.sessions_30d} | "
                f"**{hw.avg_engagement_sec:.1f}s** | {hw.key_events_30d} | {hw.recommended_action} |\n"
            )
    else:
        md += "| — | — | 0 | 0.0s | 0 | ✅ Sin ganadores ocultos pendientes con umbral (`>= 45s` o conv., `< 30` sesiones). |\n"

    md += """
### 🕵️ Alertas de *Dark Social* / Fuga de Atribución UTM

| Tipo Alerta | Severidad | Despacho / Canal | Direct Actual vs. Base | Pico % | Acción Recomendada |
| :--- | :---: | :--- | :---: | :---: | :--- |
"""
    if report.dark_social_alerts:
        for da in report.dark_social_alerts:
            sev_badge = "🔴 Alta" if da.severity == "high" else "🟡 Media"
            ref_str = da.dispatch_id or da.channel_expected or "macro"
            md += (
                f"| `{da.alert_type}` | {sev_badge} | `{ref_str}` | "
                f"{da.direct_sessions_current} vs. {da.direct_sessions_baseline:.1f} | **+{da.spike_pct:.1f}%** | {da.recommended_action} |\n"
            )
    else:
        md += "| — | — | — | — | — | ✅ Sin fugas anómalas de *Dark Social* detectadas en la ventana de 30 días. |\n"

    md += """
### 🌐 Embudo Nativo Comunidades Tech & PTR (Dev.to + CoderLegion + LinkedIn Empresa — Coste 0 €)

| Plataforma | Estado Conector | Publicaciones (Emparejadas) | Vistas / Impresiones | Clics / CTR Nativo | Reacciones / Coment. | Sesiones GA4 (30d) | PTR % (Traspaso) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    if report.social_platform_summary:
        # 1. Dev.to
        ps_dt = report.social_platform_summary.get("devto") or {}
        st_dt = ps_dt.get("status", "unavailable")
        arts_dt = f"{ps_dt.get('articles_count', 0)} ({ps_dt.get('matched_assets_count', 0)})"
        v_dt = int(ps_dt.get("native_views", 0) or 0)
        re_dt = f"{int(ps_dt.get('native_reactions', 0) or 0):,} / {int(ps_dt.get('native_comments', 0) or 0):,}"
        sess_dt = int(ps_dt.get("ga4_sessions_30d", 0) or 0)
        ptr_dt = float(ps_dt.get("ptr_pct", 0.0) or 0.0)
        md += f"| **`devto`** | `{st_dt}` | {arts_dt} | **{v_dt:,}** | — | {re_dt} | {sess_dt:,} | **{ptr_dt:.2f}%** |\n"

        # 2. CoderLegion
        ps_cl = report.social_platform_summary.get("coderlegion") or {}
        st_cl = ps_cl.get("status", "unavailable")
        arts_cl = f"{ps_cl.get('articles_count', 0)} ({ps_cl.get('matched_assets_count', 0)})"
        v_cl = int(ps_cl.get("native_views", 0) or 0)
        re_cl = f"{int(ps_cl.get('native_reactions', 0) or 0):,} / {int(ps_cl.get('native_comments', 0) or 0):,}"
        sess_cl = int(ps_cl.get("ga4_sessions_30d", 0) or 0)
        ptr_cl = float(ps_cl.get("ptr_pct", 0.0) or 0.0)
        md += f"| **`coderlegion`** | `{st_cl}` | {arts_cl} | **{v_cl:,}** | — | {re_cl} | {sess_cl:,} | **{ptr_cl:.2f}%** |\n"

        # 3. LinkedIn Página de Empresa (Carril Dual)
        ps_li = report.social_platform_summary.get("linkedin_company") or {}
        st_li = ps_li.get("status", "unavailable")
        arts_li = f"{ps_li.get('posts_count', 0)} ({ps_li.get('matched_assets_count', 0)})"
        impr_li = int(ps_li.get("total_impressions", 0) or 0)
        clk_li = int(ps_li.get("total_clicks", 0) or 0)
        ctr_li = float(ps_li.get("native_ctr_pct", 0.0) or 0.0)
        re_li = f"{int(ps_li.get('total_reactions', 0) or 0):,} / {int(ps_li.get('total_comments', 0) or 0):,}"
        clk_str = f"{clk_li:,} ({ctr_li:.1f}%)" if impr_li > 0 else "—"
        sess_li = int(ps_li.get("ga4_sessions_30d", 0) or 0)
        ptr_li = float(ps_li.get("ptr_pct", 0.0) or 0.0)
        md += f"| **`linkedin_company`** | `{st_li}` | {arts_li} | **{impr_li:,}** | {clk_str} | {re_li} | {sess_li:,} | **{ptr_li:.2f}%** |\n"

        # 4. X / Twitter (Stand-by Coste 0 €)
        ps_x = report.social_platform_summary.get("x") or {}
        st_x = ps_x.get("status", "standby_zero_cost")
        sess_x = int(ps_x.get("ga4_sessions_30d", 0) or 0)
        md += f"| **`x`** | `{st_x}` | — | *Stand-by 0 €* | — | — | {sess_x:,} | *Solo GA4+UTM* |\n"

        foll_cnt = int(ps_li.get("followers_count", 0) or 0)
        md += f"\n*Nota LinkedIn Empresa:* Alcance exclusivo de **Página de Empresa** (`LINKEDIN_COMPANY_ID`) · **{foll_cnt} seguidores** · Cero perfiles personales ni scraping (`INV-PULSE-12`).\n"
        md += "*Nota X / Twitter:* Atribución nativa en stand-by por política de coste 0 € (API de pago suspendida); tráfico medido exclusivamente vía GA4 Acquisition + UTMs (`Hito 7.11`).\n"
    else:
        md += "| — | `unavailable` | 0 (0) | 0 | — | 0 / 0 | 0 | 0.00% |\n"

    md += """
### 🚨 Alertas de Fuga de Traspaso (`>= 300` vistas nativas con `PTR < 2.0%`)

| Activo / ID | Plataforma | Vistas Nativas | Reacciones / Coment. | Sesiones GA4 | PTR % | Acción Recomendada E06 |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
"""
    if report.ptr_leak_alerts:
        for pa in report.ptr_leak_alerts[:10]:
            md += (
                f"| [`{pa.asset_id}`]({pa.slug}) | `{pa.platform}` | **{pa.native_views:,}** | "
                f"{pa.native_reactions} / {pa.native_comments} | {pa.ga4_sessions_30d} | **{pa.ptr_pct:.2f}%** | {pa.recommended_action} |\n"
            )
    else:
        md += "| — | — | 0 | 0 / 0 | 0 | 0.00% | ✅ Sin fugas críticas de traspaso detectadas (`>= 300` vistas con `PTR < 2.0%`). |\n"

    md += """
### 🛡️ Escudo Anti-Canibalización Canónica (`>= 500` vistas nativas y `0` imp. GSC tras `> 21d`)

| Activo / ID | Plataforma | Vistas Nativas | Imp. GSC (30d) | Días Publicado | URL Canónica | Acción Recomendada E02 / E06 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
"""
    if report.canonical_shield_alerts:
        for csa in report.canonical_shield_alerts[:10]:
            md += (
                f"| [`{csa.asset_id}`]({csa.slug}) | `{csa.platform}` | **{csa.native_views:,}** | "
                f"{csa.gsc_impressions_30d} | {csa.days_since_publish}d | `{csa.canonical_url}` | {csa.recommended_action} |\n"
            )
    else:
        md += "| — | — | 0 | 0 | 0d | — | ✅ Sin alertas de canibalización canónica externa (`>= 500` vistas con `0` imp. GSC). |\n"

    top_backlog_1 = report.prioritized_backlog[0] if report.prioritized_backlog else None
    top_backlog_2 = report.prioritized_backlog[1] if len(report.prioritized_backlog) > 1 else None
    top_qw = report.quick_wins_ctr[0] if report.quick_wins_ctr else None

    md += f"""
---

## 9. Plan de Acción Inmediato y Relevo Editorial

1. **Relevo a `E04-bilingual-seo-editor`:** Optimizar los **{min(len(report.quick_wins_ctr), 12)} Quick Wins prioritarios** (liderados por `{top_qw.id if top_qw else 'N/A'}` con `{top_qw.gsc_impressions_30d if top_qw else 0:,}` imp. GSC), ajustando títulos/meta-descriptions a las queries reales detectadas.
2. **Relevo a `E05-content-monetizer`:** Resolver los **{len(report.monetization_orphans)} huérfanos de monetización** actuales e impulsar la cobertura en categorías con alta tracción orgánica y bajo ratio comercial.
3. **Relevo a `E06-social-syndicator`:** Reciclar los **{len(report.hidden_channel_winners)} ganadores ocultos por canal**, corregir las **{len(report.ptr_leak_alerts)} fugas de traspaso PTR**, revisar las **{len(report.canonical_shield_alerts)} alertas del escudo canónico** y auditar las **{len(report.dark_social_alerts)} alertas de Dark Social** garantizando UTMs `ADR-033`.
4. **Relevo a `E01-editorial-orchestrator` / `E03-technical-writer`:** Atender las **{report.silent_releases_count} alertas de releases silenciosas** y resolver las **{len(report.cannibalization_alerts)} alertas de canibalización** en el calendario de las Oleadas Semanales.
5. **Priorización en Backlog (`data/editorial/backlog.yaml`):** Lanzar `{top_backlog_1.id if top_backlog_1 else 'N/A'}` (ROI {top_backlog_1.editorial_roi_score if top_backlog_1 else 0.0:.1f}) y `{top_backlog_2.id if top_backlog_2 else 'N/A'}` (ROI {top_backlog_2.editorial_roi_score if top_backlog_2 else 0.0:.1f}).
"""
    return md


def run_impact_analysis() -> PulseImpactReport:
    """Ejecuta el pipeline determinista completo de análisis de impacto."""
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"No se encontró {INDEX_PATH}. Ejecuta 'python -m ops.pulse.build_index' primero.")
    if not METRICS_PATH.exists():
        raise FileNotFoundError(f"No se encontró {METRICS_PATH}. Ejecuta 'python -m ops.pulse.sync_metrics' primero.")

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        all_assets: List[Dict[str, Any]] = json.load(f)

    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics: Dict[str, Dict[str, Any]] = json.load(f)

    posts = [a for a in all_assets if a.get("asset_type") == "post"]
    published_posts = [p for p in posts if p.get("status") == "published"]
    scheduled_posts = [p for p in posts if p.get("status") == "scheduled"]
    draft_posts = [p for p in posts if p.get("status") == "draft"]
    base_apps_count = len({a.get("parent_asset_id") or a.get("slug") or a["id"] for a in all_assets if a.get("asset_type") == "app"})
    kits_count = sum(1 for a in all_assets if a.get("asset_type") in ("kit", "suite", "mega_bundle"))

    # Métricas agregadas de tráfico GA4 + GSC (sobre posts publicados únicos para evitar doble conteo)
    post_views_list = [int(metrics.get(p["id"], {}).get("ga4_views_30d", 0) or 0) for p in published_posts]
    total_views = sum(post_views_list)
    total_views_en = sum(int(metrics.get(p["id"], {}).get("ga4_views_en_30d", 0) or 0) for p in published_posts)
    sorted_views = sorted(post_views_list)

    total_gsc_clicks = sum(int(metrics.get(p["id"], {}).get("gsc_clicks_30d", 0) or 0) for p in published_posts)
    total_gsc_impr = sum(int(metrics.get(p["id"], {}).get("gsc_impressions_30d", 0) or 0) for p in published_posts)
    total_gsc_clicks_prev = sum(int(metrics.get(p["id"], {}).get("gsc_clicks_prev_30d", 0) or 0) for p in published_posts)
    total_gsc_impr_prev = sum(int(metrics.get(p["id"], {}).get("gsc_impressions_prev_30d", 0) or 0) for p in published_posts)
    total_gsc_impr_en = sum(int(metrics.get(p["id"], {}).get("gsc_impressions_en_30d", 0) or 0) for p in published_posts)
    brand_clicks, brand_impr = extract_brand_query_totals()

    channel_data: Optional[Dict[str, Any]] = None
    if CHANNEL_METRICS_PATH.exists():
        try:
            with open(CHANNEL_METRICS_PATH, "r", encoding="utf-8") as f:
                channel_data = json.load(f)
        except Exception:
            channel_data = None

    social_data: Optional[Dict[str, Any]] = None
    if SOCIAL_METRICS_PATH.exists():
        try:
            with open(SOCIAL_METRICS_PATH, "r", encoding="utf-8") as f:
                social_data = json.load(f)
        except Exception:
            social_data = None

    weighted_pos_sum = sum(
        float(metrics.get(p["id"], {}).get("gsc_avg_position", 0.0) or 0.0)
        * int(metrics.get(p["id"], {}).get("gsc_impressions_30d", 0) or 0)
        for p in published_posts
        if float(metrics.get(p["id"], {}).get("gsc_avg_position", 0.0) or 0.0) > 0
    )
    impr_with_pos = sum(
        int(metrics.get(p["id"], {}).get("gsc_impressions_30d", 0) or 0)
        for p in published_posts
        if float(metrics.get(p["id"], {}).get("gsc_avg_position", 0.0) or 0.0) > 0
    )
    avg_gsc_ctr = round((total_gsc_clicks / total_gsc_impr * 100.0) if total_gsc_impr > 0 else 0.0, 2)
    avg_gsc_pos = round((weighted_pos_sum / impr_with_pos) if impr_with_pos > 0 else 0.0, 1)
    en_views_share = round((total_views_en / total_views * 100.0) if total_views > 0 else 0.0, 1)
    en_gsc_impr_share = round((total_gsc_impr_en / total_gsc_impr * 100.0) if total_gsc_impr > 0 else 0.0, 1)

    if sorted_views:
        med_views = float(statistics.median(sorted_views))
        p75_idx = max(0, int(len(sorted_views) * 0.75) - 1)
        p75_views = float(sorted_views[min(p75_idx, len(sorted_views) - 1)])
    else:
        med_views = 8.0
        p75_views = 20.0

    # Crecimiento interanual mensual
    growth_yoy = 0.0
    months_count = 0
    m_initial_label = "inicio"
    m_initial_views = 0
    m_peak_label = "pico"
    m_peak_views = 0
    if MONTHLY_METRICS_PATH.exists():
        try:
            with open(MONTHLY_METRICS_PATH, "r", encoding="utf-8") as f:
                monthly_data = json.load(f)
            months_count = len(monthly_data)
            if len(monthly_data) >= 2:
                v_initial = int(monthly_data[0].get("views", 1) or 1)
                peak_row = max(monthly_data, key=lambda m: int(m.get("views", 0) or 0))
                v_peak = int(peak_row.get("views", 0) or 0)
                growth_yoy = round(((v_peak - v_initial) / max(v_initial, 1)) * 100.0, 1)
                m_initial_label = monthly_data[0].get("month", "inicio")
                m_initial_views = v_initial
                m_peak_label = peak_row.get("month", "pico")
                m_peak_views = v_peak
        except Exception:
            growth_yoy = 0.0

    # Ejecutar análisis temáticos (Editorial ROI Score v2 cuando hay señal social validada)
    cat_perf = calculate_category_performance(
        published_posts,
        metrics,
        social_data=social_data,
        channel_data=channel_data,
    )
    cat_social_map = {c.category: c.social_traction_score for c in cat_perf if c.social_traction_score > 0}
    quick_wins = detect_quick_wins_ctr(published_posts, metrics, med_views)
    orphans = detect_monetization_orphans(published_posts, metrics, p75_views)
    decay_alerts = detect_decay_alerts(published_posts, metrics)
    prioritized_bg = prioritize_backlog(BACKLOG_PATH, category_social_scores=cat_social_map or None)
    release_impact = analyze_release_editorial_impact(all_assets, metrics)
    cannibalization = detect_keyword_cannibalization()
    channel_summary = analyze_channel_performance(channel_data)
    hidden_winners = detect_hidden_channel_winners(published_posts, channel_data)
    dark_social = detect_dark_social_alerts(channel_data, DISPATCH_QUEUE_PATH)
    social_summary = summarize_social_platforms(social_data, channel_data)
    ptr_leaks = detect_ptr_leak_alerts(published_posts, social_data, channel_data)
    canonical_shield = detect_canonical_shield_alerts(published_posts, social_data, metrics)
    silent_count = sum(1 for r in release_impact if r.editorial_coverage_status == "silent_release_alert")

    report = PulseImpactReport(
        version="1.3.0",
        generated_at=datetime.now(timezone.utc),
        visibility="private",
        total_published_posts=len(published_posts),
        total_scheduled_posts=len(scheduled_posts),
        total_30d_post_views=total_views,
        median_post_views=med_views,
        p75_post_views=p75_views,
        monthly_growth_yoy_pct=growth_yoy,
        total_30d_gsc_clicks=total_gsc_clicks,
        total_30d_gsc_impressions=total_gsc_impr,
        gsc_clicks_prev_30d=total_gsc_clicks_prev,
        gsc_impressions_prev_30d=total_gsc_impr_prev,
        gsc_brand_clicks_30d=brand_clicks,
        gsc_brand_impressions_30d=brand_impr,
        avg_gsc_ctr_pct=avg_gsc_ctr,
        avg_gsc_position=avg_gsc_pos,
        en_views_share_pct=en_views_share,
        en_gsc_impressions_share_pct=en_gsc_impr_share,
        category_performance=cat_perf,
        quick_wins_ctr=quick_wins,
        monetization_orphans=orphans,
        decay_alerts=decay_alerts,
        prioritized_backlog=prioritized_bg,
        release_editorial_impact=release_impact,
        cannibalization_alerts=cannibalization,
        channel_summary=channel_summary,
        hidden_channel_winners=hidden_winners,
        dark_social_alerts=dark_social,
        social_platform_summary=social_summary,
        ptr_leak_alerts=ptr_leaks,
        canonical_shield_alerts=canonical_shield,
        silent_releases_count=silent_count,
    )

    # 1. Guardar impact_report.json privado (INV-PULSE-6)
    os.makedirs(REPORT_JSON_PATH.parent, exist_ok=True)
    with open(REPORT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(report.model_dump(mode="json"), f, ensure_ascii=False, indent=2)
    print(f"[IMPACT ANALYZER] Guardado dataset privado en: {REPORT_JSON_PATH}")

    # 2. Guardar reporte ejecutivo en specs/audit/IMPACT_REPORT.md
    os.makedirs(REPORT_MD_PATH.parent, exist_ok=True)
    catalog_meta = {
        "total_assets": len(all_assets),
        "total_posts": len(posts),
        "draft_posts": len(draft_posts),
        "apps_count": base_apps_count,
        "kits_count": kits_count,
        "months_count": months_count,
        "m_initial_label": m_initial_label,
        "m_initial_views": m_initial_views,
        "m_peak_label": m_peak_label,
        "m_peak_views": m_peak_views,
    }
    md_content = generate_impact_report_markdown(report, catalog_meta=catalog_meta)
    with open(REPORT_MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[IMPACT ANALYZER] Generado reporte ejecutivo en: {REPORT_MD_PATH}")

    return report


if __name__ == "__main__":
    report = run_impact_analysis()
    print(
        f"[IMPACT ANALYZER] Completado: {len(report.quick_wins_ctr)} Quick Wins, "
        f"{len(report.monetization_orphans)} Huérfanos, {len(report.cannibalization_alerts)} Canibalizaciones, "
        f"{len(report.prioritized_backlog)} Ideas en Backlog."
    )
