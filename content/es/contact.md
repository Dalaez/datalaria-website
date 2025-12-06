---
title: "Contacto"
layout: "single"
summary: "Ponte en contacto conmigo"
draft: false
---

## ¿Tienes algo que decirme?

¡Me encantaría saber de ti! Si tienes alguna pregunta, sugerencia o simplemente quieres saludar, no dudes en enviarme un mensaje.

También puedes escribirme directamente a: **datalaria@gmail.com**

---

<form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" class="contact-form">
  <input type="hidden" name="form-name" value="contact" />
  <p style="display:none;">
    <label>No rellenar si eres humano: <input name="bot-field" /></label>
  </p>
  
  <div class="form-group">
    <label for="name">Nombre y Apellidos <span class="required">*</span></label>
    <input type="text" id="name" name="name" required placeholder="Tu nombre completo" />
  </div>
  
  <div class="form-group">
    <label for="email">Email <span class="required">*</span></label>
    <input type="email" id="email" name="email" required placeholder="tu@email.com" />
  </div>
  
  <div class="form-group">
    <label for="post-app">Post/App de Datalaria (opcional)</label>
    <input type="text" id="post-app" name="post-app" placeholder="Nombre del post o app relacionado" />
  </div>
  
  <div class="form-group">
    <label for="message">Mensaje <span class="required">*</span></label>
    <textarea id="message" name="message" rows="6" required placeholder="Escribe tu mensaje aquí..."></textarea>
  </div>
  
  <button type="submit" class="submit-btn">Enviar mensaje</button>
</form>
