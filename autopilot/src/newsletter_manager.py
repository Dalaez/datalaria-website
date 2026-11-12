"""Newsletter Manager - Gestión de campañas Brevo 2.0 Anti-Churn vía Brevo API v3."""

from __future__ import annotations

import html as html_lib
import os
import re
from datetime import datetime
from typing import Any, Dict, Optional, Union

import requests

from autopilot.src.models import (
    NewsletterContent,
    append_utm_params,
    select_subject_archetype,
)

SITE_BASE_URL = "https://datalaria.com"


class NewsletterManager:
    """Gestiona campañas de Brevo Newsletter 2.0 segmentadas por idioma (ES #3 / EN #4)."""

    def __init__(self) -> None:
        self.api_key = os.getenv("BREVO_API_KEY")
        self.list_id_es = int(os.getenv("BREVO_LIST_ID_ES", "3"))
        self.list_id_en = int(os.getenv("BREVO_LIST_ID_EN", "4"))
        self.sender_name = "Datalaria"
        self.sender_email = "datalaria@gmail.com"
        self.base_url = "https://api.brevo.com/v3"

        if not self.api_key:
            print("⚠️ BREVO_API_KEY no encontrada (modo preview/offline disponible).")

    def _get_list_id(self, lang: str) -> int:
        return self.list_id_es if lang == "es" else self.list_id_en

    def _get_headers(self) -> Dict[str, str]:
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": self.api_key or "",
        }

    def _normalize_absolute_url(self, raw_url: Optional[str], lang: str) -> str:
        fallback_path = "/es/recursos/" if lang == "es" else "/en/resources/"
        candidate = (raw_url or "").strip() or fallback_path
        if candidate.startswith("/"):
            return f"{SITE_BASE_URL}{candidate}"
        if not candidate.startswith(("http://", "https://")):
            return f"{SITE_BASE_URL}/{candidate.lstrip('/')}"
        return candidate

    def _coerce_newsletter_payload(
        self,
        newsletter_or_text: Union[NewsletterContent, str],
        subject: str,
        post_title: str,
        lang: str,
        slug: str,
    ) -> NewsletterContent:
        if isinstance(newsletter_or_text, NewsletterContent):
            return newsletter_or_text

        raw_paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", (newsletter_or_text or "").replace("\r\n", "\n"))
            if p.strip()
        ]
        if not raw_paragraphs:
            raw_paragraphs = [
                (
                    f"Esta semana comparto un análisis práctico sobre {post_title} con decisiones reales aplicables en producción."
                    if lang == "es"
                    else f"This week I am sharing a practical breakdown on {post_title} with actionable architecture decisions."
                )
            ]

        clean_subject = (subject or "").strip()
        if len(clean_subject) < 25:
            clean_subject = f"{post_title} — Guía técnica Datalaria" if lang == "es" else f"{post_title} — Datalaria Technical Guide"
        clean_subject = clean_subject[:110]
        archetype = select_subject_archetype(slug)

        if lang == "es":
            preheader = f"3 claves prácticas sobre {post_title} aplicables hoy en tus sistemas."[:150]
            insights = [
                f"Contexto práctico y criterio de ingeniería aplicado a {post_title}.",
                "Errores habituales al llevar este enfoque a equipos y producción.",
                "Pasos concretos para medir resultados sin añadir complejidad accidental.",
            ]
            ps_text = "P.D. Si conoces a alguien del equipo a quien le ayude esta lectura, reenvíale este correo."
        else:
            preheader = f"3 practical engineering takeaways on {post_title} ready to apply today."[:150]
            insights = [
                f"Core engineering principles applied to {post_title}.",
                "Common pitfalls teams hit when moving this pattern to production.",
                "Actionable steps to measure real impact without extra complexity.",
            ]
            ps_text = "P.S. Know a colleague who would benefit from this guide? Forward this email their way."

        return NewsletterContent(
            archetype=archetype,
            subject=clean_subject,
            preheader=preheader if len(preheader) >= 35 else f"{preheader} — Datalaria Brief",
            hook_paragraphs=raw_paragraphs[:4],
            insights_60s=insights,
            ps_referral_text=ps_text,
        )

    def _render_paragraphs_html(self, paragraphs: list[str]) -> str:
        rendered: list[str] = []
        for p in paragraphs:
            escaped = html_lib.escape(p.strip(), quote=True).replace("\n", "<br>")
            rendered.append(
                f'<p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.65; color: #334155;">{escaped}</p>'
            )
        return "\n".join(rendered)

    def _build_html_template(
        self,
        intro_text_or_payload: Union[NewsletterContent, str],
        post_title: str,
        post_url: str,
        lang: str = "es",
        hero_image_url: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> str:
        """Genera plantilla HTML Brevo 2.0 Anti-Churn en tablas claras seguras para Outlook/Gmail."""
        derived_slug = (
            slug
            or re.sub(r"[^a-z0-9-]+", "-", post_url.rstrip("/").split("/")[-1].lower()).strip("-")
            or "datalaria-post"
        )
        payload = self._coerce_newsletter_payload(
            intro_text_or_payload,
            subject=post_title,
            post_title=post_title,
            lang=lang,
            slug=derived_slug,
        )

        if lang == "es":
            badge_text = "BREVO 2.0 · BRIEFING TÉCNICO"
            greeting = "Hola {{ contact.FIRSTNAME | default: 'amigo/a' }},"
            box_title = "⚡ En 60 segundos: Los 3 Insights Clave"
            cta_primary_text = "Leer artículo completo →"
            cta_secondary_default = "Explorar Kits y Sandboxes gratuitos"
            forward_note = "Reenvía este email a un colega si le resulta útil."
            footer_text = "Recibes este briefing porque formas parte de la comunidad técnica de Datalaria."
            unsubscribe_text = "Darte de baja aquí"
        else:
            badge_text = "BREVO 2.0 · TECH BRIEFING"
            greeting = "Hi {{ contact.FIRSTNAME | default: 'friend' }},"
            box_title = "⚡ In 60 seconds: 3 Key Insights"
            cta_primary_text = "Read the full article →"
            cta_secondary_default = "Explore Kits & Free Sandboxes"
            forward_note = "Forward this email to a colleague if you found it useful."
            footer_text = "You received this briefing because you subscribed to the Datalaria technical community."
            unsubscribe_text = "Unsubscribe here"

        cta_primary_url = append_utm_params(
            post_url,
            source="newsletter",
            medium="email",
            campaign=derived_slug,
            content="cta_article",
        )
        hero_click_url = append_utm_params(
            post_url,
            source="newsletter",
            medium="email",
            campaign=derived_slug,
            content="hero_cover",
        )
        secondary_raw = self._normalize_absolute_url(payload.secondary_cta_url, lang)
        cta_secondary_url = append_utm_params(
            secondary_raw,
            source="newsletter",
            medium="email",
            campaign=derived_slug,
            content="cta_secondary",
        )
        cta_secondary_label = payload.secondary_cta_label or cta_secondary_default

        escaped_title = html_lib.escape(post_title, quote=True)
        escaped_preheader = html_lib.escape(payload.preheader, quote=True)
        escaped_cta_primary = html_lib.escape(cta_primary_url, quote=True)
        escaped_cta_secondary = html_lib.escape(cta_secondary_url, quote=True)
        escaped_cta_secondary_label = html_lib.escape(cta_secondary_label, quote=True)
        escaped_hero_click = html_lib.escape(hero_click_url, quote=True)
        escaped_ps = html_lib.escape(payload.ps_referral_text or forward_note, quote=True)

        paragraphs_html = self._render_paragraphs_html(payload.hook_paragraphs)
        insights_html = "\n".join(
            f'<li style="margin: 0 0 8px 0; color: #1e293b; font-size: 15px; line-height: 1.55;">{html_lib.escape(item, quote=True)}</li>'
            for item in payload.insights_60s
        )

        hero_block = ""
        if hero_image_url and hero_image_url.strip():
            escaped_hero_img = html_lib.escape(hero_image_url.strip(), quote=True)
            hero_block = f"""
          <tr>
            <td align="center" style="padding: 8px 32px 20px 32px;">
              <a href="{escaped_hero_click}" target="_blank" style="text-decoration: none; display: block;">
                <img src="{escaped_hero_img}" alt="{escaped_title}" style="width: 100%; max-width: 560px; height: auto; border-radius: 12px; display: block; border: 0;" />
              </a>
            </td>
          </tr>"""

        return f"""<!DOCTYPE html>
<html lang="{html_lib.escape(lang, quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escaped_title}</title>
  <!--[if mso]>
  <style type="text/css">
    body, table, td {{ font-family: Arial, Helvetica, sans-serif !important; }}
  </style>
  <![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #0f172a;">
  <div style="display: none; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; font-size: 1px; color: #f8fafc;">
    {escaped_preheader}
  </div>

  <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f8fafc;">
    <tr>
      <td align="center" style="padding: 28px 14px;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
          <tr>
            <td style="padding: 22px 32px 16px 32px; border-bottom: 1px solid #e2e8f0;">
              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="left">
                    <span style="font-size: 19px; font-weight: 800; letter-spacing: 0.5px; color: #0f172a;">DATALARIA</span>
                  </td>
                  <td align="right">
                    <span style="display: inline-block; padding: 4px 10px; background-color: #eef2ff; color: #4338ca; border-radius: 9999px; font-size: 11px; font-weight: 700; letter-spacing: 0.4px;">{badge_text}</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding: 26px 32px 10px 32px;">
              <p style="margin: 0 0 16px 0; font-size: 17px; font-weight: 600; color: #0f172a;">{greeting}</p>
              <h1 style="margin: 0 0 16px 0; font-size: 22px; line-height: 1.3; font-weight: 700; color: #0f172a;">{escaped_title}</h1>
              {paragraphs_html}
            </td>
          </tr>
{hero_block}
          <tr>
            <td style="padding: 4px 32px 24px 32px;">
              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; border-left: 4px solid #667eea; border-radius: 0 8px 8px 0;">
                <tr>
                  <td style="padding: 16px 20px;">
                    <div style="font-size: 14px; font-weight: 700; color: #4338ca; margin: 0 0 10px 0;">
                      {box_title}
                    </div>
                    <ul style="margin: 0; padding-left: 18px;">
                      {insights_html}
                    </ul>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding: 4px 32px 28px 32px;">
              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center" style="padding-bottom: 12px;">
                    <a href="{escaped_cta_primary}" target="_blank" style="display: inline-block; padding: 14px 28px; background-color: #4f46e5; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 15px;">
                      {cta_primary_text}
                    </a>
                  </td>
                </tr>
                <tr>
                  <td align="center">
                    <a href="{escaped_cta_secondary}" target="_blank" style="display: inline-block; padding: 11px 22px; background-color: #f8fafc; color: #334155; border: 1px solid #cbd5e1; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px;">
                      {escaped_cta_secondary_label}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding: 20px 32px; background-color: #f8fafc; border-top: 1px solid #e2e8f0;">
              <p style="margin: 0 0 10px 0; font-size: 14px; line-height: 1.55; color: #334155;">
                {escaped_ps}
              </p>
              <p style="margin: 0 0 14px 0; font-size: 13px; color: #475569;">
                {html_lib.escape(forward_note, quote=True)} — <a href="{escaped_cta_primary}" style="color: #4338ca;">{html_lib.escape(post_title, quote=True)}</a>
              </p>
              <p style="margin: 0; font-size: 12px; color: #64748b; text-align: center;">
                {html_lib.escape(footer_text, quote=True)}<br>
                <a href="{{{{ unsubscribe }}}}" style="color: #4f46e5; text-decoration: underline;">{unsubscribe_text}</a>
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

    def send_campaign(
        self,
        subject: str,
        intro_text: Union[NewsletterContent, str],
        post_title: str,
        post_url: str,
        lang: str = "es",
        hero_image_url: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> bool:
        """Crea y envía una campaña Brevo v3 con previewText y plantilla anti-churn."""
        if not self.api_key:
            print("❌ No se puede enviar: falta BREVO_API_KEY")
            return False

        derived_slug = (
            slug
            or re.sub(r"[^a-z0-9-]+", "-", post_url.rstrip("/").split("/")[-1].lower()).strip("-")
            or "datalaria-post"
        )
        payload_obj = self._coerce_newsletter_payload(
            intro_text,
            subject=subject,
            post_title=post_title,
            lang=lang,
            slug=derived_slug,
        )
        effective_subject = subject.strip() if subject and subject.strip() else payload_obj.subject
        html_content = self._build_html_template(
            payload_obj,
            post_title=post_title,
            post_url=post_url,
            lang=lang,
            hero_image_url=hero_image_url,
            slug=derived_slug,
        )

        list_id = self._get_list_id(lang)
        lang_suffix = "ES" if lang == "es" else "EN"
        campaign_name = (
            f"Newsletter {lang_suffix} - {post_title[:40]} - {datetime.now().strftime('%Y%m%d_%H%M')}"
        )

        print(f"   📋 Usando lista #{list_id} para idioma {lang_suffix}")

        create_payload = {
            "name": campaign_name,
            "subject": effective_subject,
            "previewText": payload_obj.preheader,
            "sender": {
                "name": self.sender_name,
                "email": self.sender_email,
            },
            "type": "classic",
            "htmlContent": html_content,
            "recipients": {
                "listIds": [list_id],
            },
        }

        try:
            print("📧 Creando campaña en Brevo...")
            response = requests.post(
                f"{self.base_url}/emailCampaigns",
                headers=self._get_headers(),
                json=create_payload,
                timeout=15,
            )
            if response.status_code not in (200, 201):
                print(f"❌ Error creando campaña: {response.status_code} - {response.text}")
                return False

            campaign_id = response.json().get("id")
            print(f"✅ Campaña creada con ID: {campaign_id}")

            print("🚀 Enviando campaña...")
            send_response = requests.post(
                f"{self.base_url}/emailCampaigns/{campaign_id}/sendNow",
                headers=self._get_headers(),
                timeout=15,
            )
            if send_response.status_code in (200, 201, 204):
                print("✅ ¡Campaña enviada exitosamente!")
                return True

            print(f"❌ Error enviando: {send_response.status_code} - {send_response.text}")
            return False
        except Exception as exc:
            print(f"❌ Error en NewsletterManager: {exc}")
            return False

    def preview_campaign(
        self,
        subject: str,
        intro_text: Union[NewsletterContent, str],
        post_title: str,
        post_url: str,
        lang: str = "es",
        hero_image_url: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Genera preview del email Brevo 2.0 sin realizar envíos reales (DRY_RUN)."""
        derived_slug = (
            slug
            or re.sub(r"[^a-z0-9-]+", "-", post_url.rstrip("/").split("/")[-1].lower()).strip("-")
            or "datalaria-post"
        )
        payload_obj = self._coerce_newsletter_payload(
            intro_text,
            subject=subject,
            post_title=post_title,
            lang=lang,
            slug=derived_slug,
        )
        html_content = self._build_html_template(
            payload_obj,
            post_title=post_title,
            post_url=post_url,
            lang=lang,
            hero_image_url=hero_image_url,
            slug=derived_slug,
        )
        list_id = self._get_list_id(lang)
        effective_subject = subject.strip() if subject and subject.strip() else payload_obj.subject

        print("\n📧 [NEWSLETTER PREVIEW - BREVO 2.0]")
        print(f"   To: Lista #{list_id} ({lang.upper()})")
        print(f"   Archetype: {payload_obj.archetype}")
        print(f"   Subject: {effective_subject}")
        print(f"   Preheader: {payload_obj.preheader}")
        print(f"   Hero Image: {hero_image_url or '(none)'}")
        print(f"   CTA: {post_url}")
        print("   --- End Preview ---\n")

        return {
            "list_id": list_id,
            "archetype": payload_obj.archetype,
            "subject": effective_subject,
            "preheader": payload_obj.preheader,
            "html": html_content,
        }


if __name__ == "__main__":
    manager = NewsletterManager()
    manager.preview_campaign(
        subject="3 claves reales de BPMN e IA para escalar procesos S&OP",
        intro_text="Este es un resumen práctico para probar la plantilla Brevo Newsletter 2.0.",
        post_title="Test Post",
        post_url="https://datalaria.com/es/posts/test/",
        lang="es",
        hero_image_url="https://datalaria.com/images/Datalaria_blog.png",
    )
