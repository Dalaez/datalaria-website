"""
ops/helix/build_launch_campaign.py — Generador de la Campaña de Lanzamiento de Datalaria Helix (Enero 2027)

Genera de forma reproducible en packages/helix/campaign_jan2027/:
1. brevo_waitlist_sequence.json (Manifiesto de secuencia para Listas #5 y #6 de Brevo).
2. 6 Plantillas HTML ejecutivas anti-churn (email_01_warmup, email_02_launch, email_03_closing en ES y EN).
3. SOCIAL_LAUNCH_PACK_ES_EN.md (5 posts LinkedIn ejecutivos y 5 hilos con enlaces X Web Intent en ES/EN).

Cumple estrictamente con la Invariante INV-HELIX-5 (Python estándar, cero dependencias).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import urllib.parse

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = REPO_ROOT / "packages" / "helix" / "campaign_jan2027"

# ----------------------------------------------------------------------
# 1. Definición del Manifiesto de Campañas Brevo
# ----------------------------------------------------------------------

def build_brevo_manifest() -> dict:
    """Genera el manifiesto estructurado para importar o ejecutar la secuencia en Brevo."""
    return {
        "campaign_name": "Datalaria Helix Official Launch — January/February 2027",
        "description": "Secuencia de 3 correos de lanzamiento para suscriptores en waitlist de Datalaria Helix.",
        "version": "1.0.0",
        "lists": {
            "es": {"list_id": 5, "name": "Helix Waitlist (ES)", "env_var": "BREVO_HELIX_LIST_ES"},
            "en": {"list_id": 6, "name": "Helix Waitlist (EN)", "env_var": "BREVO_HELIX_LIST_EN"}
        },
        "utm_defaults": {
            "utm_source": "brevo",
            "utm_medium": "email",
            "utm_campaign": "helix_launch_jan2027"
        },
        "pricing_early_bird": {
            "starter_kit_eur": 9,
            "core_kit_eur": 19,
            "core_kit_regular_eur": 39,
            "discount_percentage": 51
        },
        "sequence": [
            {
                "step": 1,
                "type": "warmup",
                "send_date": "2027-01-14T09:00:00+01:00",
                "days_before_launch": 5,
                "subjects": {
                    "es": "¿Por qué el vibe coding colapsa a las 48 horas? (La solución Helix llega el 19 de enero)",
                    "en": "Why vibe coding collapses after 48 hours (Helix launches January 19)"
                },
                "preview_text": {
                    "es": "3 razones por las que pedirle a la IA que programe sin especificación técnica es una receta para el desastre.",
                    "en": "3 reasons why prompting AI without technical specifications is a recipe for codebase collapse."
                },
                "template_files": {
                    "es": "email_01_warmup_es.html",
                    "en": "email_01_warmup_en.html"
                },
                "utm_content": "email_01_warmup"
            },
            {
                "step": 2,
                "type": "launch",
                "send_date": "2027-01-19T09:00:00+01:00",
                "days_before_launch": 0,
                "subjects": {
                    "es": "🚀 Datalaria Helix ha llegado: Gobierna tu IA con 12 agentes, CLI determinista y 50 % de descuento Early-Bird",
                    "en": "🚀 Datalaria Helix is live: Govern your AI with 12 agents, deterministic CLI, and 50% Early-Bird discount"
                },
                "preview_text": {
                    "es": "El Escuadrón de 12 agentes, CLI en Python puro y 3 Blueprints listos para clonar ya están disponibles a 19 €.",
                    "en": "The 12-Agent Squad, zero-dependency Python CLI, and 3 reference Blueprints are now available for 19 €."
                },
                "template_files": {
                    "es": "email_02_launch_es.html",
                    "en": "email_02_launch_en.html"
                },
                "utm_content": "email_02_launch"
            },
            {
                "step": 3,
                "type": "closing",
                "send_date": "2027-02-16T09:00:00+01:00",
                "days_before_launch": -28,
                "subjects": {
                    "es": "⏳ Últimas 48h de oferta Early-Bird (19 €): El caso MarginGuard B2B y el fin del precio de lanzamiento de Helix",
                    "en": "⏳ Final 48h of Early-Bird pricing (19 €): MarginGuard B2B case study and the end of Helix launch offer"
                },
                "preview_text": {
                    "es": "Cómo un veto de QA impidió pérdidas comerciales y por qué el precio sube a 39 € este jueves.",
                    "en": "How a binding QA veto prevented commercial losses and why pricing increases to 39 € this Thursday."
                },
                "template_files": {
                    "es": "email_03_closing_es.html",
                    "en": "email_03_closing_en.html"
                },
                "utm_content": "email_03_closing"
            }
        ]
    }


# ----------------------------------------------------------------------
# 2. Generador de Plantillas HTML Anti-Churn
# ----------------------------------------------------------------------

def _render_email_html(
    lang: str,
    title: str,
    preheader: str,
    badge_text: str,
    insights: list[str],
    body_paragraphs: list[str],
    hero_img_url: str,
    hero_link_url: str,
    hero_alt: str,
    cta1_text: str,
    cta1_url: str,
    cta2_text: str,
    cta2_url: str,
    footer_note: str
) -> str:
    """Renderiza una plantilla HTML ultra-robusta, compatible con Outlook/Gmail y anti-spam (>80% ratio texto/imagen)."""
    insights_html = "".join(f"<li style='margin-bottom: 8px; color: #cbd5e1;'>{item}</li>" for item in insights)
    paragraphs_html = "".join(f"<p style='margin: 0 0 16px 0; font-size: 15px; line-height: 1.6; color: #e2e8f0;'>{p}</p>" for p in body_paragraphs)

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <!--[if mso]>
  <style type="text/css">
    body, table, td {{font-family: Arial, Helvetica, sans-serif !important;}}
  </style>
  <![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f17; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  <!-- Preheader invisible anti-preview -->
  <div style="display: none; font-size: 1px; color: #0b0f17; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
    {preheader}
  </div>

  <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #0b0f17; min-height: 100vh;">
    <tr>
      <td align="center" style="padding: 24px 16px;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #0f172a; border-radius: 12px; border: 1px solid #1e293b; overflow: hidden;">
          
          <!-- Encabezado con Logo y Badge -->
          <tr>
            <td style="padding: 24px 32px 16px 32px; border-bottom: 1px solid #1e293b;">
              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="left">
                    <span style="font-size: 20px; font-weight: 800; color: #f8fafc; letter-spacing: -0.5px;">DATALARIA <span style="color: #06b6d4;">HELIX</span></span>
                  </td>
                  <td align="right">
                    <span style="display: inline-block; padding: 4px 10px; background-color: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 9999px; font-size: 11px; font-weight: 600; color: #38bdf8; text-transform: uppercase;">{badge_text}</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Bloque Zero-Click Value: En 60 segundos -->
          <tr>
            <td style="padding: 24px 32px 16px 32px; background-color: #131d31;">
              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td style="border-left: 3px solid #06b6d4; padding-left: 16px;">
                    <div style="font-size: 13px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                      ⚡ {'En 60 segundos: Los 3 Insights Clave' if lang == 'es' else 'In 60 seconds: 3 Key Insights'}
                    </div>
                    <ul style="margin: 0; padding-left: 16px; font-size: 14px; line-height: 1.5;">
                      {insights_html}
                    </ul>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Hero Image Clicable -->
          <tr>
            <td align="center" style="padding: 20px 32px 12px 32px;">
              <a href="{hero_link_url}" target="_blank" style="text-decoration: none; display: block;">
                <img src="{hero_img_url}" alt="{hero_alt}" width="536" style="width: 100%; max-width: 536px; height: auto; border-radius: 8px; border: 1px solid #1e293b; display: block;" />
              </a>
            </td>
          </tr>

          <!-- Cuerpo Principal -->
          <tr>
            <td style="padding: 16px 32px 24px 32px;">
              <h1 style="margin: 0 0 16px 0; font-size: 22px; font-weight: 700; color: #f8fafc; line-height: 1.3;">{title}</h1>
              {paragraphs_html}

              <!-- Bloque Doble CTA -->
              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-top: 24px;">
                <tr>
                  <td align="center" style="padding-bottom: 12px;">
                    <a href="{cta1_url}" target="_blank" style="display: block; width: 100%; max-width: 480px; background-color: #06b6d4; color: #0b0f17; font-size: 15px; font-weight: 700; text-align: center; text-decoration: none; padding: 14px 24px; border-radius: 8px; box-sizing: border-box;">
                      {cta1_text}
                    </a>
                  </td>
                </tr>
                <tr>
                  <td align="center">
                    <a href="{cta2_url}" target="_blank" style="display: block; width: 100%; max-width: 480px; background-color: transparent; color: #38bdf8; border: 1px solid #0284c7; font-size: 14px; font-weight: 600; text-align: center; text-decoration: none; padding: 12px 24px; border-radius: 8px; box-sizing: border-box;">
                      {cta2_text}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Pie de Página -->
          <tr>
            <td style="padding: 24px 32px; background-color: #0b0f17; border-top: 1px solid #1e293b; text-align: center;">
              <p style="margin: 0 0 8px 0; font-size: 12px; color: #64748b; line-height: 1.5;">{footer_note}</p>
              <p style="margin: 0; font-size: 11px; color: #475569;">
                Datalaria © 2027 · Ingenieria de Datos, Software y Agentes · <a href="https://datalaria.com" style="color: #64748b; text-decoration: underline;">datalaria.com</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

def generate_email_templates() -> dict[str, str]:
    """Genera los 6 archivos HTML ejecutivos anti-churn para la campaña."""
    templates = {}

    # Email 1: Warmup ES
    templates["email_01_warmup_es.html"] = _render_email_html(
        lang="es",
        title="¿Por qué el vibe coding colapsa a las 48 horas de vida?",
        preheader="3 razones por las que pedirle a la IA que programe sin especificación técnica es una receta para el desastre.",
        badge_text="Anticipación · Lanzamiento 19 Enero",
        insights=[
            "Pedirle a un LLM que evalúe su propio código es una cámara de eco probabilística.",
            "Cargar 12 agentes simultáneamente desperdicia un 87 % de tokens innecesarios.",
            "Datalaria Helix introduce la especificación formal como ADN ejecutable."
        ],
        body_paragraphs=[
            "Hola {{ contact.FIRSTNAME | default: 'desarrollador' }},",
            "En las últimas semanas hemos visto una oleada de entusiasmo en torno al <em>vibe coding</em>. La promesa de construir software completo simplemente conversando en lenguaje natural parece mágica durante los primeros dos días.",
            "Pero al tercer día sobreviene el colapso: regresiones invisibles, arquitecturas desarticuladas y una deuda técnica que exige reescribir todo desde cero.",
            "El <strong>martes 19 de enero</strong> lanzamos oficialmente <strong>Datalaria Helix</strong>: la metodología Spec-Driven Development (SDD) gobernada por un escuadrón de 12 agentes especializados, adaptadores multi-herramienta y un CLI en Python puro con cero dependencias.",
            "Para que puedas comprobarlo de inmediato, hemos abierto un <strong>Sandbox gratuito en el navegador</strong> donde puedes auditar la calidad de tus especificaciones y generar paquetes PKZIP en memoria sin instalar nada."
        ],
        hero_img_url="https://datalaria.com/images/recursos/helix-preview-es.png",
        hero_link_url="https://datalaria.com/apps/helix/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_01_hero",
        hero_alt="Datalaria Helix Spec Builder Sandbox Preview",
        cta1_text="⚡ Probar el Helix Spec Builder Gratuito →",
        cta1_url="https://datalaria.com/apps/helix/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_01_cta_sandbox",
        cta2_text="📖 Leer la Parte 1 de la Serie: El ADN de tu App (Llega el 19 Ene)",
        cta2_url="https://datalaria.com/es/posts/helix-parte1-especificacion-adn-escuadron-12-agentes/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_01_cta_article",
        footer_note="Estás recibiendo este correo porque te inscribiste en la lista de espera de Datalaria Helix. Si prefieres no recibir actualizaciones, puedes darte de baja en cualquier momento."
    )

    # Email 1: Warmup EN
    templates["email_01_warmup_en.html"] = _render_email_html(
        lang="en",
        title="Why vibe coding collapses after 48 hours of life",
        preheader="3 reasons why prompting AI without technical specifications is a recipe for codebase collapse.",
        badge_text="Teaser · Launching January 19",
        insights=[
            "Asking an LLM to evaluate its own code creates a probabilistic echo chamber.",
            "Dumping 12 agents at once wastes 87% of context tokens needlessly.",
            "Datalaria Helix introduces executable specifications as the application's immutable DNA."
        ],
        body_paragraphs=[
            "Hello {{ contact.FIRSTNAME | default: 'engineer' }},",
            "In recent months, the industry has experienced an explosion of enthusiasm around <em>vibe coding</em>. The promise of generating production-ready software purely through casual chat sounds miraculous for the first 48 hours.",
            "Yet by day three, projects inevitably hit a wall: silent regression bugs, fragmented architectures, and compounding technical debt forcing a complete rewrite.",
            "On <strong>Tuesday, January 19</strong>, we are officially launching <strong>Datalaria Helix</strong>: the Spec-Driven Development (SDD) engineering operating system powered by a 12-agent squad, multi-tool adapters, and a zero-dependency Python CLI.",
            "To experience this firsthand, we have deployed a <strong>free interactive browser sandbox</strong> where you can audit technical specifications and download in-memory PKZIP packages without installing a single package."
        ],
        hero_img_url="https://datalaria.com/images/recursos/helix-preview-en.png",
        hero_link_url="https://datalaria.com/apps/helix/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_01_hero_en",
        hero_alt="Datalaria Helix Spec Builder Sandbox Preview",
        cta1_text="⚡ Launch the Free Helix Spec Builder →",
        cta1_url="https://datalaria.com/apps/helix/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_01_cta_sandbox_en",
        cta2_text="📖 Read Part 1 of the Series: The App's DNA (Coming Jan 19)",
        cta2_url="https://datalaria.com/en/posts/helix-part1-spec-dna-12-agent-engineering-squad/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_01_cta_article_en",
        footer_note="You received this email because you joined the Datalaria Helix waitlist. Unsubscribe anytime."
    )

    # Email 2: Launch ES
    templates["email_02_launch_es.html"] = _render_email_html(
        lang="es",
        title="🚀 Datalaria Helix está disponible: Gobierna tu IA con 12 agentes",
        preheader="El Escuadrón de 12 agentes, CLI en Python puro y 3 Blueprints listos para clonar ya están disponibles a 19 €.",
        badge_text="Lanzamiento Oficial · 50% Descuento Early-Bird",
        insights=[
            "12 fichas canónicas de agentes organizadas en 4 células operativas.",
            "26 adaptadores compilados para Claude Code, Google Antigravity y Cursor.",
            "CLI helix.py en Python estándar sin pip install y 2 casos de estudio reales."
        ],
        body_paragraphs=[
            "Hola {{ contact.FIRSTNAME | default: 'amigo' }},",
            "El día ha llegado. <strong>Datalaria Helix ya está disponible oficialmente</strong>.",
            "Hemos compilado meses de trabajo de ingeniería, gobernanza y pruebas de estrés en una suite comercial lista para descargar que elimina para siempre las alucinaciones probabilísticas de tu base de código.",
            "A diferencia de las herramientas SaaS cerradas que exigen suscripciones de 29 € o 99 € al mes, Helix se distribuye bajo un modelo de <strong>pago único perpetuo con 100 % de soberanía local</strong>.",
            "Durante las próximas 4 semanas, puedes acceder al <strong>Datalaria Helix Core Kit</strong> por solo <strong>19 €</strong> (precio regular 39 €) o iniciarte con el <strong>Starter Kit</strong> por <strong>9 €</strong>."
        ],
        hero_img_url="https://datalaria.com/images/recursos/helix-preview-es.png",
        hero_link_url="https://datalaria.com/es/recursos/#pack-sdd?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_02_hero",
        hero_alt="Datalaria Helix Commercial Kit Preview",
        cta1_text="🚀 Descargar Datalaria Helix Core Kit (19 € Early-Bird) →",
        cta1_url="https://datalaria.com/es/recursos/#pack-sdd?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_02_cta_core",
        cta2_text="⚡ Probar el Sandbox Web Gratuito (/apps/helix/)",
        cta2_url="https://datalaria.com/apps/helix/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_02_cta_sandbox",
        footer_note="Oferta de lanzamiento válida hasta el 18 de febrero de 2027. Incluye actualizaciones de parches y acceso a la comunidad Datalaria."
    )

    # Email 2: Launch EN
    templates["email_02_launch_en.html"] = _render_email_html(
        lang="en",
        title="🚀 Datalaria Helix is Live: Govern Your AI with 12 Specialist Agents",
        preheader="The 12-Agent Squad, zero-dependency Python CLI, and 3 reference Blueprints are now available for 19 €.",
        badge_text="Official Launch · 50% Early-Bird Discount",
        insights=[
            "12 canonical agent specifications organized across 4 operational cells.",
            "26 pre-compiled adapters for Claude Code, Google Antigravity, and Cursor.",
            "Zero-dependency helix.py CLI in standard Python + 2 real-world case studies."
        ],
        body_paragraphs=[
            "Hello {{ contact.FIRSTNAME | default: 'engineer' }},",
            "The day has arrived. <strong>Datalaria Helix is officially live</strong>.",
            "We have packaged months of production engineering, algorithmic triage, and rigorous stress-testing into a downloadable commercial suite designed to eliminate stochastic hallucinations from your codebase forever.",
            "Unlike proprietary SaaS platforms charging recurring monthly subscriptions of 29 € to 99 €, Helix is delivered as a <strong>perpetual single-payment license with 100% local sovereignty</strong>.",
            "For the next 4 weeks, you can secure the <strong>Datalaria Helix Core Kit</strong> for only <strong>19 €</strong> (regular 39 €), or get started with the <strong>Starter Kit</strong> for <strong>9 €</strong>."
        ],
        hero_img_url="https://datalaria.com/images/recursos/helix-preview-en.png",
        hero_link_url="https://datalaria.com/en/resources/#pack-sdd?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_02_hero_en",
        hero_alt="Datalaria Helix Commercial Kit Preview",
        cta1_text="🚀 Get Datalaria Helix Core Kit (19 € Early-Bird) →",
        cta1_url="https://datalaria.com/en/resources/#pack-sdd?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_02_cta_core_en",
        cta2_text="⚡ Try the Free Web Sandbox (/apps/helix/)",
        cta2_url="https://datalaria.com/apps/helix/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_02_cta_sandbox_en",
        footer_note="Early-Bird launch price valid through February 18, 2027. Includes patch updates and lifetime local access."
    )

    # Email 3: Closing ES
    templates["email_03_closing_es.html"] = _render_email_html(
        lang="es",
        title="⏳ Últimas 48 horas de precio Early-Bird: El caso MarginGuard B2B",
        preheader="Cómo un veto de QA impidió pérdidas comerciales y por qué el precio sube a 39 € este jueves.",
        badge_text="Fin de Oferta · Cierre Early-Bird",
        insights=[
            "Caso MarginGuard: cómo el veto independiente impidió volúmenes negativos de venta.",
            "87 % de ahorro medido en consumo de tokens en comparación con reintentos a ciegas.",
            "El precio de Datalaria Helix Core Kit pasa de 19 € a su tarifa definitiva de 39 €."
        ],
        body_paragraphs=[
            "Hola {{ contact.FIRSTNAME | default: 'compañero' }},",
            "Esta semana hemos publicado la quinta y última entrega de la serie Datalaria Helix, analizando el caso real de <strong>MarginGuard B2B</strong>.",
            "En este proyecto, un modelo generativo construyó un simulador comercial con sliders atractivos pero omitió la guarda matemática cuando el descuento supera al margen. Sin la intervención del rol independiente <strong>11-qa-verifier</strong> que emitió un <code>QA_REJECT</code> vinculante, el cliente habría desplegado un sistema que calculaba pérdidas como si fuesen ahorros.",
            "Esa es la diferencia entre el <em>vibe coding</em> y la ingeniería real. Puedes experimentar con este mismo caso de estudio interactivo en el <a href='https://datalaria.com/apps/helix/?preset=margin&utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_03_sandbox' style='color: #38bdf8; text-decoration: underline;'>Helix Spec Builder Gratuito</a>.",
            "Te recordamos que la oferta de lanzamiento del <strong>Datalaria Helix Core Kit a 19 €</strong> finaliza en menos de 48 horas. A partir de este jueves, el precio se fijará en sus <strong>39 €</strong> oficiales."
        ],
        hero_img_url="https://datalaria.com/images/recursos/helix-preview-es.png",
        hero_link_url="https://datalaria.com/es/recursos/#pack-sdd?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_03_hero",
        hero_alt="Datalaria Helix Early Bird Final Hours",
        cta1_text="⚡ Asegurar Core Kit por 19 € antes del cierre →",
        cta1_url="https://datalaria.com/es/recursos/#pack-sdd?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_03_cta_core",
        cta2_text="📖 Leer el Caso Completo MarginGuard B2B (Parte 5)",
        cta2_url="https://datalaria.com/es/posts/helix-parte5-casos-reales-operacion-crisol-pulse-marginguard-kits/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_03_cta_article",
        footer_note="Garantía de reembolso de 14 días. Licencia perpetua comercial sin suscripciones recurrentes."
    )

    # Email 3: Closing EN
    templates["email_03_closing_en.html"] = _render_email_html(
        lang="en",
        title="⏳ Final 48 Hours of Early-Bird Pricing: The MarginGuard B2B Case",
        preheader="How a binding QA veto prevented commercial losses and why pricing increases to 39 € this Thursday.",
        badge_text="Final Hours · Early-Bird Closing",
        insights=[
            "MarginGuard Case: How independent veto prevented inverted sales volume calculations.",
            "87% measured reduction in context token waste vs unconstrained prompt retries.",
            "Datalaria Helix Core Kit price transitions from 19 € to regular 39 €."
        ],
        body_paragraphs=[
            "Hello {{ contact.FIRSTNAME | default: 'engineer' }},",
            "This week we released the fifth and final installment of the Datalaria Helix launch series, examining the empirical case study of <strong>MarginGuard B2B</strong>.",
            "In this project, a generative model crafted a sleek calculator interface but overlooked a fatal mathematical boundary condition when discounts meet or exceed contribution margins. Without the binding veto of <strong>11-qa-verifier</strong> issuing a <code>QA_REJECT</code>, the organization would have shipped an engine interpreting catastrophic margin dilution as savings.",
            "That is the boundary separating <em>vibe coding</em> from genuine software engineering. You can explore this exact interactive case study inside the free <a href='https://datalaria.com/apps/helix/?preset=margin&utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_03_sandbox_en' style='color: #38bdf8; text-decoration: underline;'>Helix Spec Builder Sandbox</a>.",
            "This is our final reminder that the <strong>19 € Early-Bird launch offer</strong> for the Datalaria Helix Core Kit ends in less than 48 hours. After this Thursday, pricing resets to its standard <strong>39 €</strong> tier."
        ],
        hero_img_url="https://datalaria.com/images/recursos/helix-preview-en.png",
        hero_link_url="https://datalaria.com/en/resources/#pack-sdd?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_03_hero_en",
        hero_alt="Datalaria Helix Early Bird Final Hours",
        cta1_text="⚡ Secure Core Kit for 19 € Before Price Increase →",
        cta1_url="https://datalaria.com/en/resources/#pack-sdd?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_03_cta_core_en",
        cta2_text="📖 Read the MarginGuard B2B Case Study (Part 5)",
        cta2_url="https://datalaria.com/en/posts/helix-part5-real-case-studies-pulse-crisol-marginguard-kits/?utm_source=brevo&utm_medium=email&utm_campaign=helix_launch_jan2027&utm_content=email_03_cta_article_en",
        footer_note="14-day money-back guarantee. Perpetual commercial license with zero monthly subscriptions."
    )

    return templates


# ----------------------------------------------------------------------
# 3. Generador del Pack de Redes Sociales (LinkedIn & X)
# ----------------------------------------------------------------------

def build_social_pack_markdown() -> str:
    """Genera el pack de difusión social con 5 posts de LinkedIn y 5 hilos con enlaces X Web Intent."""
    posts_meta = [
        {
            "part": 1,
            "date": "2027-01-19",
            "title_es": "La Especificación es el ADN de tu App: Por Qué el Vibe Coding Colapsa a las 48 Horas",
            "title_en": "The Specification is Your App's DNA: Why Vibe Coding Collapses After 48 Hours",
            "url_es": "https://datalaria.com/es/posts/helix-parte1-especificacion-adn-escuadron-12-agentes/",
            "url_en": "https://datalaria.com/en/posts/helix-part1-spec-dna-12-agent-engineering-squad/",
            "hook_es": "¿Por qué el 90 % de los prototipos generados con IA colapsan al intentar añadir la tercera funcionalidad?",
            "hook_en": "Why do 90% of AI-generated prototypes collapse the moment you try to add a third feature?"
        },
        {
            "part": 2,
            "date": "2027-01-26",
            "title_es": "Triaje Determinista XS–XL y Adaptadores Multi-Herramienta: Reduciendo un 87 % de Tokens",
            "title_en": "Deterministic Triage (XS–XL) and Multi-Tool Adapters: Slashing 87% of Context Tokens",
            "url_es": "https://datalaria.com/es/posts/helix-parte2-triaje-determinista-adaptadores-antigravity-claude-cursor/",
            "url_en": "https://datalaria.com/en/posts/helix-part2-deterministic-triage-adapters-antigravity-claude-cursor/",
            "hook_es": "Cargar 12 agentes de IA a la vez en un prompt es la forma más rápida de quemar tu presupuesto de tokens.",
            "hook_en": "Loading 12 AI agents simultaneously into a prompt is the fastest way to burn through your token budget."
        },
        {
            "part": 3,
            "date": "2027-02-02",
            "title_es": "El Músculo Determinista: CLI helix.py en Python Puro, SpecQualityScore y Rollback Automático",
            "title_en": "The Deterministic Muscle: Zero-Dependency Python CLI helix.py, SpecQualityScore, and Automatic Rollback",
            "url_es": "https://datalaria.com/es/posts/helix-parte3-cli-python-cero-dependencias-spec-score-rollback/",
            "url_en": "https://datalaria.com/en/posts/helix-part3-zero-dependency-python-cli-spec-score-rollback/",
            "hook_es": "Pedirle a un LLM que evalúe su propio código es como pedirle a un testigo que redacte la sentencia judicial.",
            "hook_en": "Asking an LLM to evaluate its own code is like asking a witness to write the final court verdict."
        },
        {
            "part": 4,
            "date": "2027-02-09",
            "title_es": "Helix Spec Builder en React 19: Empaquetado PKZIP Client-Side y Exportador de Mega-Prompt",
            "title_en": "Helix Spec Builder in React 19: Client-Side PKZIP Packaging and Mega-Prompt Exporter",
            "url_es": "https://datalaria.com/es/posts/helix-parte4-sandbox-react-spec-builder-zip-client-side/",
            "url_en": "https://datalaria.com/en/posts/helix-part4-react-sandbox-spec-builder-client-side-zip/",
            "hook_es": "¿Cómo empaquetar un archivo ZIP completo de especificaciones directamente en la memoria del navegador sin backend?",
            "hook_en": "How do you package a complete specification ZIP directly in browser memory without sending a single byte to a server?"
        },
        {
            "part": 5,
            "date": "2027-02-16",
            "title_es": "Evidencia Empírica de Veto: La Auditoría de Pulse, el Caso MarginGuard B2B y los Kits Comerciales",
            "title_en": "Empirical Veto in Action: Pulse Audit, MarginGuard B2B Case Study, and Commercial Kits",
            "url_es": "https://datalaria.com/es/posts/helix-parte5-casos-reales-operacion-crisol-pulse-marginguard-kits/",
            "url_en": "https://datalaria.com/en/posts/helix-part5-real-case-studies-pulse-crisol-marginguard-kits/",
            "hook_es": "Un LLM omitió una división por cero en un simulador de precios. El veto vinculante de QA impidió el desastre.",
            "hook_en": "An LLM omitted a zero-division boundary in a pricing simulator. QA's binding veto averted disaster."
        }
    ]

    md = [
        "# Datalaria Helix — Social Launch Pack (LinkedIn & X / Twitter)",
        "",
        "> **Calendario de Difusión Oficial:** Martes semanales desde el **19 de enero al 16 de febrero de 2027**.",
        "> Todos los enlaces X cuentan con botones **Web Intent** pre-configurados para publicación en 1 clic.",
        "",
        "---",
        ""
    ]

    for p in posts_meta:
        # Enlaces X Web Intent
        x_text_es = f"{p['hook_es']} Descubre cómo gobernamos el desarrollo con IA en Datalaria Helix:"
        x_intent_es = "https://twitter.com/intent/tweet?" + urllib.parse.urlencode({"text": x_text_es, "url": p["url_es"], "hashtags": "AI,SoftwareEngineering,SDD"})

        x_text_en = f"{p['hook_en']} Learn how Datalaria Helix governs agentic AI engineering:"
        x_intent_en = "https://twitter.com/intent/tweet?" + urllib.parse.urlencode({"text": x_text_en, "url": p["url_en"], "hashtags": "AIEngineering,SoftwareArchitecture,SDD"})

        md.extend([
            f"## 🚀 Entrega {p['part']}/5 — Fecha de Publicación: {p['date']}",
            "",
            "### 1. Publicación Ejecutiva para LinkedIn (Español)",
            "```markdown",
            p["hook_es"],
            "",
            f"En la entrega {p['part']}/5 de la serie Datalaria Helix abordamos: {p['title_es']}.",
            "",
            "Puntos clave de ingeniería:",
            "- Por qué la heurística estocástica debe subordinarse a contratos deterministas.",
            "- Invariantes matemáticas y puertas de verificación con salida binaria.",
            "- Gobernanza del escuadrón Helix sin dependencias externas.",
            "",
            f"👉 Artículo completo con diagramas y código: {p['url_es']}",
            "👉 Prueba el Sandbox interactivo gratuito: https://datalaria.com/apps/helix/",
            "",
            "#IngenieriaDeSoftware #InteligenciaArtificial #SpecDrivenDevelopment #Python #React #DatalariaHelix",
            "```",
            "",
            "### 2. Executive LinkedIn Post (English)",
            "```markdown",
            p["hook_en"],
            "",
            f"In installment {p['part']}/5 of the Datalaria Helix series, we explore: {p['title_en']}.",
            "",
            "Core architectural takeaways:",
            "- Why stochastic heuristics must be governed by deterministic contracts.",
            "- Mathematical invariants and binary exit-code verification gates.",
            "- Pure zero-dependency squad orchestration.",
            "",
            f"👉 Full article with interactive diagrams and code: {p['url_en']}",
            "👉 Try the free web sandbox: https://datalaria.com/apps/helix/",
            "",
            "#SoftwareEngineering #ArtificialIntelligence #SpecDrivenDevelopment #Python #React #DatalariaHelix",
            "```",
            "",
            "### 3. Hilo Técnico & 1-Clic Web Intent (X / Twitter)",
            f"- **ES:** [{p['hook_es']}]({x_intent_es})",
            f"- **EN:** [{p['hook_en']}]({x_intent_en})",
            "",
            "---",
            ""
        ])

    return "\n".join(md)


# ----------------------------------------------------------------------
# 4. Orquestación y Función Principal
# ----------------------------------------------------------------------

def build_all_campaign_assets(target_dir: Path = OUTPUT_DIR) -> list[Path]:
    """Genera todos los archivos de campaña en target_dir."""
    target_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []

    # 1. Manifiesto Brevo
    manifest_path = target_dir / "brevo_waitlist_sequence.json"
    manifest_data = build_brevo_manifest()
    manifest_path.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")
    generated_files.append(manifest_path)

    # 2. Plantillas HTML
    templates = generate_email_templates()
    for filename, content in templates.items():
        template_path = target_dir / filename
        template_path.write_text(content, encoding="utf-8")
        generated_files.append(template_path)

    # 3. Pack Social
    social_pack_path = target_dir / "SOCIAL_LAUNCH_PACK_ES_EN.md"
    social_pack_content = build_social_pack_markdown()
    social_pack_path.write_text(social_pack_content, encoding="utf-8")
    generated_files.append(social_pack_path)

    return generated_files

def check_campaign_assets(target_dir: Path = OUTPUT_DIR) -> bool:
    """Comprueba que todos los archivos requeridos de la campaña existan y no estén vacíos."""
    required = [
        "brevo_waitlist_sequence.json",
        "email_01_warmup_es.html",
        "email_01_warmup_en.html",
        "email_02_launch_es.html",
        "email_02_launch_en.html",
        "email_03_closing_es.html",
        "email_03_closing_en.html",
        "SOCIAL_LAUNCH_PACK_ES_EN.md"
    ]
    missing = []
    for req in required:
        p = target_dir / req
        if not p.is_file() or p.stat().st_size == 0:
            missing.append(req)
    if missing:
        print(f"❌ Error: Faltan archivos de campaña en {target_dir}: {missing}", file=sys.stderr)
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Compilador de Campaña de Lanzamiento de Datalaria Helix (Enero 2027)")
    parser.add_argument("--check", action="store_true", help="Verifica la existencia y validez de los artefactos generados.")
    args = parser.parse_args()

    if args.check:
        ok = check_campaign_assets()
        sys.exit(0 if ok else 1)

    generated = build_all_campaign_assets()
    print(f"✅ Campaña de Lanzamiento generada con éxito en {OUTPUT_DIR} ({len(generated)} archivos):")
    for f in generated:
        print(f"  - {f.name} ({f.stat().st_size} bytes)")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    main()
