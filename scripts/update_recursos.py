import re
import sys

# 1. Update assets/css/extended/recursos.css
with open('assets/css/extended/recursos.css', 'r', encoding='utf-8') as f:
    css = f.read()

target_css = """    /* Grid de Acceso Rápido a las 3 Suites (visible en "Todos") */
    .suites-quick-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 12px;
    }
    .suite-mini-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      box-shadow: var(--shadow-sm);
      transition: all 0.15s ease;
      cursor: pointer;
    }
    .suite-mini-card:hover {
      border-color: var(--accent);
      transform: translateY(-1px);
    }
    .suite-mini-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .suite-mini-icon {
      font-size: 22px;
      width: 38px;
      height: 38px;
      background: var(--bg-subtle);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .suite-mini-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
    }
    .suite-mini-desc {
      font-size: 11px;
      color: var(--text-muted);
    }
    .suite-mini-action {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }
    .suite-mini-price {
      font-size: 15px;
      font-weight: 700;
      font-family: var(--font-mono);
      color: var(--text-main);
    }
    .btn-suite-buy-mini {
      background: var(--accent-soft);
      border: 1px solid var(--accent);
      color: var(--accent);
      font-size: 11px;
      font-weight: 600;
      padding: 5px 9px;
      border-radius: 6px;
      text-decoration: none;
      white-space: nowrap;
      transition: all 0.15s ease;
    }
    .btn-suite-buy-mini:hover {
      background: var(--accent);
      color: #ffffff;
    }
    .badge-suite-soon {
      background: var(--lock-bg);
      border: 1px solid var(--lock-border);
      color: var(--lock-text);
      font-size: 10px;
      font-weight: 600;
      padding: 4px 8px;
      border-radius: 6px;
    }"""

replacement_css = """    /* Grid de Acceso Rápido a las 3 Suites (visible en "Todos") */
    .suites-quick-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 14px;
    }
    .suite-mini-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      box-shadow: var(--shadow-sm);
      transition: all 0.15s ease;
      cursor: pointer;
    }
    .suite-mini-card:hover {
      border-color: var(--accent);
      transform: translateY(-1px);
    }
    .suite-mini-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .suite-mini-icon {
      font-size: 22px;
      width: 38px;
      height: 38px;
      background: var(--bg-subtle);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .suite-mini-title {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-main);
    }
    .suite-mini-desc {
      font-size: 11px;
      color: var(--text-muted);
    }
    .suite-mini-action {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 10px;
      border-top: 1px solid var(--border);
      flex-wrap: wrap;
    }
    .suite-mini-price {
      font-size: 16px;
      font-weight: 700;
      font-family: var(--font-mono);
      color: var(--text-main);
    }
    .btn-suite-buy-mini {
      background: var(--accent);
      border: 1px solid var(--accent);
      color: #ffffff;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 5px;
      text-decoration: none;
      white-space: nowrap;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
    }
    .btn-suite-buy-mini:hover {
      background: var(--accent-hover);
      color: #ffffff;
    }
    .badge-suite-soon {
      background: var(--lock-bg);
      border: 1px solid var(--lock-border);
      color: var(--lock-text);
      font-size: 10px;
      font-weight: 600;
      padding: 4px 8px;
      border-radius: 6px;
    }"""

# Normalize CRLF
css_norm = css.replace('\r\n', '\n')
target_css_norm = target_css.replace('\r\n', '\n')
replacement_css_norm = replacement_css.replace('\r\n', '\n')

if target_css_norm in css_norm:
    css_norm = css_norm.replace(target_css_norm, replacement_css_norm, 1)
    with open('assets/css/extended/recursos.css', 'w', encoding='utf-8', newline='\n') as f:
        f.write(css_norm)
    print("recursos.css successfully updated!")
else:
    print("Warning: target_css not found in recursos.css")
