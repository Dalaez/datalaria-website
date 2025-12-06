---
title: "Contact"
layout: "single"
summary: "Get in touch with me"
draft: false
---

## Got something to tell me?

I'd love to hear from you! If you have any questions, suggestions, or just want to say hello, feel free to send me a message.

You can also email me directly at: **datalaria@gmail.com**

---

<form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" class="contact-form">
  <input type="hidden" name="form-name" value="contact" />
  <p style="display:none;">
    <label>Don't fill this out if you're human: <input name="bot-field" /></label>
  </p>
  
  <div class="form-group">
    <label for="name">Full Name <span class="required">*</span></label>
    <input type="text" id="name" name="name" required placeholder="Your full name" />
  </div>
  
  <div class="form-group">
    <label for="email">Email <span class="required">*</span></label>
    <input type="email" id="email" name="email" required placeholder="you@email.com" />
  </div>
  
  <div class="form-group">
    <label for="post-app">Datalaria Post/App (optional)</label>
    <input type="text" id="post-app" name="post-app" placeholder="Name of related post or app" />
  </div>
  
  <div class="form-group">
    <label for="message">Message <span class="required">*</span></label>
    <textarea id="message" name="message" rows="6" required placeholder="Write your message here..."></textarea>
  </div>
  
  <button type="submit" class="submit-btn">Send message</button>
</form>
