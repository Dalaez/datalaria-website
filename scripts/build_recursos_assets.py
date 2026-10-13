import re
import os

def update_css():
    with open('mockup_recursos_v2.html', 'r', encoding='utf-8') as f:
        html = f.read()

    css_raw = re.search(r'<style>(.*?)</style>', html, re.DOTALL).group(1)

    # Remove the mockup bar styles since they are not part of the site
    css_clean = re.sub(r'/\* Barra Superior de Control del Mockup \*/.*?(?=/\* ==========================================================================\s+SECCI)', '', css_raw, flags=re.DOTALL)
    
    # Remove generic body and * reset so PaperMod's typography and container sizing are preserved
    css_clean = re.sub(r'body\s*\{[^}]*\}', '', css_clean)
    css_clean = re.sub(r'\*\s*\{\s*box-sizing:[^}]*\}', '', css_clean)

    # Support PaperMod's body.dark alongside [data-theme="dark"]
    css_clean = css_clean.replace('[data-theme="dark"]', '[data-theme="dark"], body.dark')

    # Read legacy css for bundle-card and product-card support in articles
    with open('assets/css/extended/recursos.css', 'r', encoding='utf-8') as f:
        old_css = f.read()

    bundle_card_part = re.search(r'(/\* -{10,}\s+7\.\s+Tarjetas de Bundle.*?$)', old_css, re.DOTALL)
    legacy_css = bundle_card_part.group(1) if bundle_card_part else ''

    extra_css = """
/* Hash scroll highlight pulse */
@keyframes highlightPulse {
  0% { box-shadow: 0 0 0 0 rgba(2, 132, 199, 0.7); border-color: #0284c7; }
  50% { box-shadow: 0 0 0 8px rgba(2, 132, 199, 0.2); border-color: #0284c7; }
  100% { box-shadow: none; }
}
.highlight-pulse {
  animation: highlightPulse 1.2s ease-in-out 2;
}

/* Home portal resources card action buttons */
.dlh-res-bottom {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
}
.dlh-res-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.dlh-btn-pack-dl {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: var(--dlh-accent, #0284c7);
  color: #ffffff !important;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 6px;
  text-decoration: none;
  transition: background 0.15s ease, transform 0.15s ease;
}
.dlh-btn-pack-dl:hover {
  background: var(--dlh-accent-hover, #0369a1);
  transform: translateY(-1px);
}
.dlh-guide-link {
  font-size: 0.76rem;
  font-weight: 500;
  color: var(--dlh-accent, #0284c7);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 3px;
}
.dlh-guide-link:hover {
  text-decoration: underline;
}
.dlh-guide-soon-text {
  font-size: 0.74rem;
  color: var(--secondary, #64748b);
  font-style: italic;
  opacity: 0.85;
}
.dlh-pack-soon-badge {
  font-size: 0.75rem;
  color: var(--secondary, #64748b);
  background: var(--border, #e2e8f0);
  padding: 4px 8px;
  border-radius: 4px;
  text-align: center;
}
"""

    new_content = css_clean + '\n\n' + extra_css + '\n\n' + legacy_css
    with open('assets/css/extended/recursos.css', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated assets/css/extended/recursos.css successfully ({len(new_content)} bytes).")

if __name__ == '__main__':
    update_css()
