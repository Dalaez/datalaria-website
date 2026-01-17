"""
Newsletter Manager - Gestiona el envío de campañas de email via Brevo API.
"""
import os
import requests
from datetime import datetime


class NewsletterManager:
    """Gestiona campañas de newsletter via Brevo API."""
    
    def __init__(self):
        self.api_key = os.getenv("BREVO_API_KEY")
        self.list_id = int(os.getenv("BREVO_LIST_ID", "3"))
        self.sender_name = "Datalaria"
        self.sender_email = "datalaria@gmail.com"
        self.base_url = "https://api.brevo.com/v3"
        
        if not self.api_key:
            print("⚠️ BREVO_API_KEY no encontrada.")
    
    def _get_headers(self):
        """Headers para autenticación con Brevo API."""
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": self.api_key
        }
    
    def _build_html_template(self, intro_text, post_title, post_url, lang="es"):
        """
        Genera el HTML del email con diseño profesional.
        Usa {{ contact.FIRSTNAME }} para personalización de Brevo.
        """
        # Textos según idioma
        if lang == "es":
            greeting = "Hola {{ contact.FIRSTNAME | default: 'amigo/a' }},"
            cta_text = "Leer artículo completo"
            footer_text = "Recibiste este email porque estás suscrito a la newsletter de Datalaria."
            unsubscribe_text = "Darte de baja"
        else:
            greeting = "Hi {{ contact.FIRSTNAME | default: 'friend' }},"
            cta_text = "Read full article"
            footer_text = "You received this email because you subscribed to the Datalaria newsletter."
            unsubscribe_text = "Unsubscribe"
        
        # Logo URL (desde tu sitio)
        logo_url = "https://datalaria.com/images/datalaria_logo_transp.png"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px 30px;">
        
        <!-- Header con logo -->
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="{logo_url}" alt="Datalaria" style="width: 80px; height: auto;">
        </div>
        
        <!-- Saludo personalizado -->
        <p style="font-size: 18px; color: #333; margin-bottom: 20px;">
            {greeting}
        </p>
        
        <!-- Contenido generado por IA -->
        <div style="font-size: 16px; line-height: 1.7; color: #444; margin-bottom: 30px;">
            {intro_text}
        </div>
        
        <!-- CTA Button -->
        <div style="text-align: center; margin: 35px 0;">
            <a href="{post_url}" style="display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px;">
                👉 {cta_text}
            </a>
        </div>
        
        <!-- Firma -->
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;">
            <div style="text-align: center;">
                <img src="{logo_url}" alt="Datalaria" style="width: 50px; height: auto; margin-bottom: 10px;">
                <p style="font-size: 14px; color: #666; margin: 0;">
                    <strong>Datalaria</strong>
                </p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="margin-top: 30px; text-align: center; font-size: 12px; color: #999;">
            <p>{footer_text}</p>
            <p><a href="{{{{ unsubscribe }}}}" style="color: #667eea;">{unsubscribe_text}</a></p>
        </div>
        
    </div>
</body>
</html>
"""
        return html
    
    def send_campaign(self, subject, intro_text, post_title, post_url, lang="es"):
        """
        Crea y envía una campaña de email a la lista de suscriptores.
        
        Args:
            subject: Asunto del email
            intro_text: Texto introductorio generado por IA
            post_title: Título del post
            post_url: URL del post
            lang: Idioma (es/en)
            
        Returns:
            bool: True si se envió correctamente
        """
        if not self.api_key:
            print("❌ No se puede enviar: falta BREVO_API_KEY")
            return False
        
        # 1. Generar HTML
        html_content = self._build_html_template(intro_text, post_title, post_url, lang)
        
        # 2. Crear campaña
        campaign_name = f"Newsletter - {post_title[:50]} - {datetime.now().strftime('%Y%m%d_%H%M')}"
        
        create_payload = {
            "name": campaign_name,
            "subject": subject,
            "sender": {
                "name": self.sender_name,
                "email": self.sender_email
            },
            "type": "classic",
            "htmlContent": html_content,
            "recipients": {
                "listIds": [self.list_id]
            }
        }
        
        try:
            # Crear campaña
            print("📧 Creando campaña en Brevo...")
            response = requests.post(
                f"{self.base_url}/emailCampaigns",
                headers=self._get_headers(),
                json=create_payload
            )
            
            if response.status_code not in [200, 201]:
                print(f"❌ Error creando campaña: {response.status_code} - {response.text}")
                return False
            
            campaign_id = response.json().get("id")
            print(f"✅ Campaña creada con ID: {campaign_id}")
            
            # 3. Enviar campaña inmediatamente
            print("🚀 Enviando campaña...")
            send_response = requests.post(
                f"{self.base_url}/emailCampaigns/{campaign_id}/sendNow",
                headers=self._get_headers()
            )
            
            if send_response.status_code in [200, 201, 204]:
                print("✅ ¡Campaña enviada exitosamente!")
                return True
            else:
                print(f"❌ Error enviando: {send_response.status_code} - {send_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error en NewsletterManager: {e}")
            return False
    
    def preview_campaign(self, subject, intro_text, post_title, post_url, lang="es"):
        """
        Genera preview del email sin enviarlo (para DRY_RUN).
        """
        html = self._build_html_template(intro_text, post_title, post_url, lang)
        
        print("\n📧 [NEWSLETTER PREVIEW]")
        print(f"   To: Lista #{self.list_id}")
        print(f"   Subject: {subject}")
        print(f"   From: {self.sender_name} <{self.sender_email}>")
        print(f"\n   --- Content (text) ---")
        print(f"   Hola {{nombre}},")
        print(f"   {intro_text[:200]}...")
        print(f"   [CTA: {post_url}]")
        print(f"   --- End Preview ---\n")


if __name__ == "__main__":
    # Test
    manager = NewsletterManager()
    manager.preview_campaign(
        subject="🚀 Nuevo en Datalaria: Test Post",
        intro_text="Este es un texto de prueba para la newsletter.",
        post_title="Test Post",
        post_url="https://datalaria.com/es/posts/test/",
        lang="es"
    )
