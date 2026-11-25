---
title: "Contacto"
layout: "single"
summary: "Ponte en contacto conmigo"
draft: false
---

## ¿Tienes algo que decirme?

¡Me encantaría saber de ti! Si tienes alguna pregunta, sugerencia o simplemente quieres saludar, no dudes en enviarme un mensaje.

También puedes escribirme directamente a: **contacto@datalaria.com**

---

<form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" class="contact-form">
  <input type="hidden" name="form-name" value="contact" />
  <p style="display:none;">
    <label>No rellenar si eres humano: <input name="bot-field" /></label>
  </p>
  
  <div class="form-group">
    <label for="name">Nombre y Apellidos <span class="required">*</span></label>
    <input type="text" id="name" name="name" autocomplete="name" required placeholder="Tu nombre completo" />
  </div>
  
  <div class="form-group">
    <label for="email">Email <span class="required">*</span></label>
    <input type="email" id="email" name="email" autocomplete="email" required placeholder="tu@email.com" />
  </div>
  
  <div class="form-group">
    <label for="post-app">Post/App o Licencia B2B (opcional)</label>
    <input type="text" id="post-app" name="post-app" placeholder="Ej. Licencia Equipo 99€, Mega Bundle, Agentic Radar..." />
  </div>
  
  <div class="form-group">
    <label for="message">Mensaje <span class="required">*</span></label>
    <textarea id="message" name="message" rows="6" required placeholder="Escribe tu mensaje aquí..."></textarea>
  </div>
  
  <button type="submit" class="submit-btn">Enviar mensaje</button>
</form>

<script>
  (function() {
    const params = new URLSearchParams(window.location.search);
    const topic = params.get('topic');
    const app = params.get('app');
    const product = params.get('product');
    const field = document.getElementById('post-app');
    const msg = document.getElementById('message');
    if (!field) return;
    if (topic === 'b2b-license') {
      field.value = product ? ('Licencia Equipo/Corporativa B2B (' + product + ')') : 'Licencia Equipo (99€) / Corporativa (149€) B2B';
      if (msg && !msg.value) msg.placeholder = 'Indícanos el tamaño de tu equipo (5 o 20 asientos), kit/suite de interés y datos para factura VIES/PO...';
    } else if (topic === 'testimonial') {
      field.value = 'Feedback / Testimonio de Kit Datalaria';
    } else if (topic === 'kit-support') {
      field.value = 'Soporte técnico de Kit';
    } else if (app) {
      field.value = 'App: ' + app;
    }
  })();
</script>
