import json

with open('scratch/posts_for_mockup.json', 'r', encoding='utf-8') as f:
    all_posts = json.load(f)

json_posts_str = json.dumps(all_posts, ensure_ascii=False)

html_code = f"""<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datalaria | Mockup Minimalista v4</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* ==========================================================================
       SISTEMA DE DISEÑO MINIMALISTA v4 (PaperMod + Bootstrap-Theme + Datalaria)
       ========================================================================== */
    :root {{
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: 'JetBrains Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      
      /* Modo Claro */
      --bg-body: #ffffff;
      --bg-card: #ffffff;
      --bg-subtle: #f8fafc;
      --bg-hover: #f1f5f9;
      --border: #e2e8f0;
      --border-subtle: #edf2f7;
      --border-focus: #cbd5e1;
      
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-light: #94a3b8;
      
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --accent-soft: rgba(2, 132, 199, 0.08);
      
      --radius: 10px;
      --radius-sm: 6px;
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04);
      --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.04);

      /* Newsletter gradients */
      --nl-gradient: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
      --nl-btn: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

      /* Algolia Copilot vars */
      --ops-primary: #5468ff;
      --ops-primary-dark: #3c4fe0;
      --ops-bg: #ffffff;
      --ops-text: #1a1a2e;
      --ops-border: #e5e7eb;
      --ops-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    }}

    [data-theme="dark"] {{
      /* Modo Oscuro */
      --bg-body: #0b0f17;
      --bg-card: #111827;
      --bg-subtle: #162032;
      --bg-hover: #1f2d45;
      --border: #1f2937;
      --border-subtle: #1e293b;
      --border-focus: #374151;
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-light: #64748b;
      
      --accent: #38bdf8;
      --accent-hover: #7dd3fc;
      --accent-soft: rgba(56, 189, 248, 0.12);
      
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.2);
      --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.25);

      --nl-gradient: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
      
      --ops-bg: #1e293b;
      --ops-text: #f8fafc;
      --ops-border: #334155;
      --ops-shadow: 0 10px 40px rgba(0, 0, 0, 0.45);
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: var(--font-sans);
      background-color: var(--bg-body);
      color: var(--text-main);
      line-height: 1.6;
      transition: background-color 0.25s ease, color 0.25s ease;
      padding-top: 36px;
    }}

    /* Barra informativa de Fase 0 */
    .mockup-topbar {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background: var(--bg-subtle);
      border-bottom: 1px solid var(--border);
      padding: 6px 16px;
      font-size: 0.76rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 1000;
    }}
    .mockup-pill {{
      background: var(--accent-soft);
      color: var(--accent);
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 600;
      font-size: 0.72rem;
    }}

    .container {{
      max-width: 860px;
      margin: 0 auto;
      padding: 0 20px;
    }}

    /* ==========================================================================
       HEADER & NAVBAR NATIVO PAPERMOD (Con Tema y Multilingüismo en cabecera)
       ========================================================================== */
    header.site-header {{
      padding: 16px 0;
      position: sticky;
      top: 36px;
      z-index: 900;
      background: var(--bg-body);
      background: rgba(var(--bg-body), 0.92);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border-subtle);
      transition: border-color 0.2s;
    }}

    .nav-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    /* Bloque izquierdo: Datalaria [🌙] | En */
    .logo-cluster {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .brand {{
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-main);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .logo-switches {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .theme-icon-btn {{
      background: transparent;
      border: none;
      cursor: pointer;
      color: var(--text-main);
      padding: 2px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      line-height: 1;
      font-size: 1.05rem;
      transition: transform 0.2s;
    }}
    .theme-icon-btn:hover {{
      transform: scale(1.15);
    }}

    .lang-separator {{
      color: var(--text-light);
      font-weight: 300;
      margin: 0 2px;
      user-select: none;
    }}

    .lang-link {{
      color: var(--text-main);
      text-decoration: none;
      font-weight: 600;
      font-size: 0.95rem;
      cursor: pointer;
      padding: 2px 4px;
      border-radius: 4px;
      transition: background-color 0.2s;
    }}
    .lang-link:hover {{
      background-color: var(--bg-hover);
    }}

    /* Bloque derecho: Menú de navegación */
    .nav-menu {{
      display: flex;
      align-items: center;
      gap: 14px;
      list-style: none;
    }}

    .nav-item a {{
      text-decoration: none;
      color: var(--text-muted);
      font-size: 0.9rem;
      font-weight: 500;
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      transition: all 0.2s;
    }}
    .nav-item a:hover {{
      color: var(--text-main);
      background: var(--bg-hover);
    }}
    .nav-item.nav-recursos a {{
      color: var(--accent);
      font-weight: 600;
    }}
    .nav-badge {{
      font-size: 0.65rem;
      background: var(--accent-soft);
      color: var(--accent);
      padding: 2px 6px;
      border-radius: 999px;
      margin-left: 4px;
      font-weight: 700;
    }}

    /* ==========================================================================
       MASTHEAD CENTRAL MINIMALISTA
       ========================================================================== */
    .masthead-v3 {{
      text-align: center;
      padding: 55px 0 25px 0;
    }}

    .masthead-v3-logo {{
      width: 100px;
      height: 100px;
      object-fit: contain;
      margin-bottom: 22px;
      display: inline-block;
      transition: transform 0.25s ease;
    }}
    .masthead-v3-logo:hover {{
      transform: scale(1.05);
    }}

    .masthead-v3-tagline {{
      font-size: 1.18rem;
      font-weight: 500;
      color: var(--text-main);
      max-width: 640px;
      margin: 0 auto;
      line-height: 1.55;
      letter-spacing: -0.01em;
    }}

    /* ==========================================================================
       BRÚJULA DEL DESCUBRIMIENTO (COMPACTA Y DE BAJA ALTURA)
       ========================================================================== */
    .discovery-compact-wrap {{
      margin: 25px 0 45px 0;
    }}

    .discovery-compact-bar {{
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 10px 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: all 0.2s ease;
    }}
    .discovery-compact-bar:hover {{
      border-color: var(--border-focus);
      box-shadow: var(--shadow-sm);
    }}

    .compass-icon-badge {{
      display: flex;
      align-items: center;
      justify-content: center;
      width: 34px;
      height: 34px;
      border-radius: 8px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--accent);
      flex-shrink: 0;
      font-size: 1.15rem;
    }}

    .discovery-items-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr 1.35fr;
      gap: 12px;
      flex-grow: 1;
      align-items: center;
    }}

    @media (max-width: 780px) {{
      .discovery-compact-bar {{
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
      }}
      .compass-icon-badge {{
        align-self: flex-start;
      }}
      .discovery-items-grid {{
        grid-template-columns: 1fr;
        gap: 8px;
      }}
    }}

    .disco-item {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 6px 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      text-decoration: none;
      color: inherit;
      min-height: 42px;
      transition: all 0.15s ease;
    }}
    .disco-item:hover {{
      border-color: var(--border-focus);
      background: var(--bg-hover);
    }}

    .disco-badge-title {{
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .disco-pill-tag {{
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      line-height: 1;
      margin-bottom: 2px;
    }}
    .tag-pop {{ color: #dc2626; }}
    .tag-lat {{ color: #16a34a; }}
    .tag-rnd {{ color: #9333ea; }}

    .disco-item-title {{
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 220px;
    }}

    .btn-shuffle-mini {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.7rem;
      padding: 3px 6px;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      flex-shrink: 0;
      transition: all 0.15s;
    }}
    .btn-shuffle-mini:hover {{
      color: var(--text-main);
      border-color: var(--text-main);
      background: var(--bg-hover);
    }}

    /* ==========================================================================
       BLOQUES DE SECCIÓN (01 Recursos, 02 Contenidos, 03 Aplicaciones)
       ========================================================================== */
    .section-block {{
      padding: 45px 0 40px 0;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .section-heading {{
      margin-bottom: 24px;
    }}

    .section-tag {{
      font-size: 0.74rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 4px;
      display: inline-block;
    }}

    .section-title {{
      font-size: 1.5rem;
      font-weight: 700;
      letter-spacing: -0.015em;
      color: var(--text-main);
      margin-bottom: 6px;
    }}

    .section-desc {{
      font-size: 0.9rem;
      color: var(--text-muted);
      max-width: 650px;
    }}

    /* ==========================================================================
       SECCIÓN 01: RECURSOS
       ========================================================================== */
    .recursos-lead-box {{
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px 24px;
      margin-bottom: 10px;
      transition: all 0.2s ease;
    }}
    .recursos-lead-box:hover {{
      border-color: var(--border-focus);
      box-shadow: var(--shadow-sm);
    }}

    .recursos-top-row {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 10px;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .recursos-lead-title {{
      font-size: 1.12rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .recursos-lead-badge {{
      font-size: 0.7rem;
      background: var(--accent-soft);
      color: var(--accent);
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 600;
    }}

    .recursos-lead-desc {{
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.55;
      margin-bottom: 16px;
    }}

    .recursos-items-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 16px;
    }}

    @media (max-width: 768px) {{
      .recursos-items-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .recurso-card-item {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s;
    }}
    .recurso-card-item:hover {{
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
    }}

    .recurso-item-icon {{
      font-size: 1.25rem;
      margin-bottom: 6px;
    }}

    .recurso-item-name {{
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 4px;
    }}

    .recurso-item-detail {{
      font-size: 0.76rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 10px;
      flex-grow: 1;
    }}

    .recurso-item-price {{
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--accent);
      font-family: var(--font-mono);
    }}

    .recursos-footer-action {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid var(--border-subtle);
      font-size: 0.82rem;
    }}

    .link-more {{
      text-decoration: none;
      color: var(--accent);
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: gap 0.2s;
    }}
    .link-more:hover {{
      gap: 8px;
      color: var(--accent-hover);
    }}

    /* ==========================================================================
       SECCIÓN 02: CONTENIDOS
       ========================================================================== */
    .cat-selector-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 18px;
    }}

    @media (max-width: 768px) {{
      .cat-selector-row {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    .cat-pill-btn {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      text-align: left;
      cursor: pointer;
      transition: all 0.2s ease;
      color: var(--text-main);
    }}
    .cat-pill-btn:hover {{
      border-color: var(--border-focus);
      background: var(--bg-subtle);
    }}
    .cat-pill-btn.active {{
      background: var(--bg-subtle);
      border-color: var(--accent);
      box-shadow: inset 0 0 0 1px var(--accent);
    }}

    .cat-pill-icon {{
      font-size: 1rem;
      margin-bottom: 2px;
      display: block;
    }}
    .cat-pill-title {{
      font-size: 0.82rem;
      font-weight: 600;
      display: block;
      margin-bottom: 1px;
    }}
    .cat-pill-count {{
      font-size: 0.7rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    .cat-posts-list {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
    }}

    .cat-post-row {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-subtle);
      text-decoration: none;
      color: inherit;
      transition: background-color 0.15s ease;
      gap: 14px;
    }}
    .cat-post-row:last-child {{
      border-bottom: none;
    }}
    .cat-post-row:hover {{
      background-color: var(--bg-subtle);
    }}

    .cat-post-main {{
      font-size: 0.88rem;
      font-weight: 500;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .cat-post-row:hover .cat-post-main {{
      color: var(--accent);
    }}

    .cat-post-date {{
      font-size: 0.74rem;
      color: var(--text-light);
      font-family: var(--font-mono);
      white-space: nowrap;
    }}

    /* ==========================================================================
       SECCIÓN 03: APLICACIONES & EXPERIMENTOS
       ========================================================================== */
    .apps-minimal-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
    }}

    @media (max-width: 680px) {{
      .apps-minimal-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .app-box {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
      text-decoration: none;
      color: inherit;
    }}
    .app-box:hover {{
      border-color: var(--border-focus);
      background: var(--bg-subtle);
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
    }}

    .app-box-top {{
      display: flex;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 10px;
    }}

    .app-box-icon {{
      font-size: 1.5rem;
      line-height: 1;
      padding: 6px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
    }}

    .app-box-name {{
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .app-box-badge {{
      font-size: 0.62rem;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 999px;
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      color: var(--text-muted);
      text-transform: uppercase;
    }}
    .badge-arcade {{
      background: rgba(236, 72, 153, 0.1);
      color: #ec4899;
      border-color: rgba(236, 72, 153, 0.2);
    }}

    .app-box-desc {{
      font-size: 0.8rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-top: 3px;
    }}

    .app-box-arrow {{
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--accent);
      align-self: flex-end;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    /* ==========================================================================
       SECCIÓN SOCIAL INFERIOR
       ========================================================================== */
    .social-bottom-section {{
      padding: 35px 0 20px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .social-bottom-label {{
      font-size: 0.86rem;
      color: var(--text-muted);
      font-weight: 500;
    }}

    .social-bottom-links {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .social-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 999px;
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      color: var(--text-main);
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 500;
      transition: all 0.2s;
    }}
    .social-chip:hover {{
      background: var(--bg-hover);
      border-color: var(--border-focus);
      transform: translateY(-1px);
    }}

    /* ==========================================================================
       NEWSLETTER NATIVA (PaperMod extend_footer.html)
       ========================================================================== */
    .newsletter-section {{
      margin-top: 2.5rem;
      padding: 2.2rem 1rem;
      border-top: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--nl-gradient);
      text-align: center;
    }}

    .newsletter-container {{
      max-width: 600px;
      margin: 0 auto;
    }}

    .newsletter-header {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.65rem;
      margin-bottom: 0.6rem;
    }}

    .newsletter-icon {{
      width: 24px;
      height: 24px;
      color: var(--text-main);
    }}

    .newsletter-title {{
      margin: 0;
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--text-main);
    }}

    .newsletter-description {{
      margin: 0 0 1.4rem;
      color: var(--text-muted);
      font-size: 0.92rem;
      line-height: 1.5;
    }}

    .newsletter-inputs {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      justify-content: center;
      align-items: center;
    }}

    .newsletter-inputs input {{
      flex: 1 1 170px;
      max-width: 210px;
      padding: 0.7rem 0.9rem;
      font-size: 0.9rem;
      font-family: inherit;
      border: 1.5px solid var(--border);
      border-radius: 8px;
      background-color: var(--bg-card);
      color: var(--text-main);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .newsletter-inputs input::placeholder {{
      color: var(--text-light);
    }}

    .newsletter-inputs input:focus {{
      outline: none;
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
    }}

    .newsletter-select {{
      padding: 0.7rem 0.6rem;
      font-size: 0.9rem;
      font-family: inherit;
      border: 1.5px solid var(--border);
      border-radius: 8px;
      background-color: var(--bg-card);
      color: var(--text-main);
      cursor: pointer;
      min-width: 80px;
      transition: border-color 0.2s ease;
    }}

    .newsletter-btn {{
      padding: 0.7rem 1.4rem;
      font-size: 0.92rem;
      font-weight: 600;
      font-family: inherit;
      border: none;
      border-radius: 8px;
      background: var(--nl-btn);
      color: white;
      cursor: pointer;
      box-shadow: 0 3px 10px rgba(102, 126, 234, 0.35);
      transition: all 0.2s ease;
    }}
    .newsletter-btn:hover {{
      transform: translateY(-1px);
      box-shadow: 0 5px 14px rgba(102, 126, 234, 0.45);
    }}

    .newsletter-message {{
      margin-top: 10px;
      font-size: 0.84rem;
      font-weight: 500;
    }}
    .newsletter-message.success {{
      color: #10b981;
    }}

    /* ==========================================================================
       FOOTER (Sin "Daniel Aláez", 100% fiel al formato de producción)
       ========================================================================== */
    footer.site-footer {{
      padding: 30px 0 35px 0;
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 20px;
    }}

    .footer-inner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .footer-nav {{
      display: flex;
      gap: 16px;
      list-style: none;
    }}
    .footer-nav a {{
      color: var(--text-muted);
      text-decoration: none;
    }}
    .footer-nav a:hover {{
      color: var(--text-main);
    }}

    /* ==========================================================================
       ALGOLIA OPS ENGINEERING COPILOT WIDGET
       ========================================================================== */
    #ops-agent-wrapper {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      font-family: var(--font-sans);
    }}

    .ops-agent-btn {{
      width: 58px;
      height: 58px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--ops-primary) 0%, var(--ops-primary-dark) 100%);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--ops-shadow);
      transition: transform 0.25s ease, box-shadow 0.25s ease;
      position: relative;
    }}
    .ops-agent-btn:hover {{
      transform: scale(1.08);
      box-shadow: 0 12px 35px rgba(84, 104, 255, 0.45);
    }}

    .ops-agent-icon {{
      width: 26px;
      height: 26px;
      color: white;
    }}

    .ops-agent-badge {{
      position: absolute;
      top: -3px;
      right: -3px;
      background: #10b981;
      color: white;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 5px;
      border-radius: 10px;
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.7; }}
    }}

    .ops-agent-chat {{
      position: absolute;
      bottom: 74px;
      right: 0;
      width: 370px;
      max-width: calc(100vw - 40px);
      height: 500px;
      max-height: calc(100vh - 110px);
      background: var(--ops-bg);
      border-radius: 16px;
      box-shadow: var(--ops-shadow);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      border: 1px solid var(--ops-border);
      transition: opacity 0.25s ease, transform 0.25s ease;
    }}

    .ops-agent-chat.hidden {{
      opacity: 0;
      transform: translateY(15px) scale(0.96);
      pointer-events: none;
    }}

    .ops-agent-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 16px;
      background: linear-gradient(135deg, var(--ops-primary) 0%, var(--ops-primary-dark) 100%);
      color: white;
      flex-shrink: 0;
    }}

    .ops-agent-title {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
      font-size: 14px;
    }}

    .ops-agent-close {{
      width: 28px;
      height: 28px;
      border: none;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      transition: background 0.2s;
    }}
    .ops-agent-close:hover {{
      background: rgba(255, 255, 255, 0.35);
    }}

    .ops-agent-messages {{
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      background: var(--ops-bg);
      display: flex;
      flex-direction: column;
      gap: 12px;
      color: var(--ops-text);
      font-size: 13.5px;
    }}

    .ops-welcome-message {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 12px 14px;
      line-height: 1.45;
    }}

    .ops-welcome-subtitle {{
      margin-top: 6px;
      font-size: 12px;
      color: var(--text-muted);
    }}

    .ops-agent-input-area {{
      display: flex;
      align-items: center;
      padding: 12px;
      border-top: 1px solid var(--ops-border);
      gap: 8px;
      background: var(--ops-bg);
    }}

    .ops-agent-input-area input {{
      flex: 1;
      padding: 8px 12px;
      border: 1px solid var(--ops-border);
      border-radius: 8px;
      background: var(--bg-subtle);
      color: var(--ops-text);
      font-size: 13px;
      outline: none;
    }}

    .ops-agent-send {{
      width: 34px;
      height: 34px;
      background: var(--ops-primary);
      color: white;
      border: none;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }}
  </style>
</head>
<body>

  <!-- BARRA INFORMATIVA DE ITERACIÓN -->
  <div class="mockup-topbar">
    <div>
      <span class="mockup-pill">Fase 0 • Mockup v4 Final</span>
      &nbsp; <span>Multilingüismo nativo (ES / EN) · Newsletter · Chat Copilot Algolia · Footer limpio</span>
    </div>
    <div style="font-family: var(--font-mono); font-size: 0.72rem;">
      98 Posts · 6 Apps · Decision Packs
    </div>
  </div>

  <!-- HEADER NATIVO PAPERMOD: Datalaria 🌙 | En + Menú a la derecha -->
  <header class="site-header">
    <div class="container nav-inner">
      
      <!-- Cluster de Logo + Switchers (Exacto a producción) -->
      <div class="logo-cluster">
        <a href="#" class="brand">
          <span>Datalaria</span>
        </a>

        <div class="logo-switches">
          <button class="theme-icon-btn" id="themeToggleBtn" title="Cambiar tema (Modo Claro / Modo Oscuro)" aria-label="Cambiar tema">
            <span id="themeEmoji">🌙</span>
          </button>
          
          <span class="lang-separator">|</span>
          
          <a class="lang-link" id="langSwitchLink" title="Switch language" aria-label="Cambiar idioma">
            En
          </a>
        </div>
      </div>

      <!-- Menú de navegación principal -->
      <nav>
        <ul class="nav-menu">
          <li class="nav-item"><a href="#blog" id="menuBlog">Blog</a></li>
          <li class="nav-item nav-recursos">
            <a href="#recursos" id="menuRecursos">Recursos<span class="nav-badge">Pro</span></a>
          </li>
          <li class="nav-item"><a href="#apps" id="menuApps">Apps</a></li>
          <li class="nav-item"><a href="/es/sobre-mi/" id="menuAbout">Sobre mí</a></li>
          <li class="nav-item"><a href="/es/contact/" id="menuContact">Contacto</a></li>
        </ul>
      </nav>

    </div>
  </header>

  <main class="container">

    <!-- =======================================================================
         MASTHEAD CENTRAL MINIMALISTA
         ======================================================================= -->
    <section class="masthead-v3">
      <img src="static/images/datalaria_logo_transp.png" alt="Datalaria" class="masthead-v3-logo" onerror="this.src='/images/datalaria_logo_transp.png';">
      <p class="masthead-v3-tagline" id="taglineText">
        Un portal para el aprendizaje en los datos, la inteligencia artificial, la tecnología y la gestión empresarial.
      </p>
    </section>

    <!-- =======================================================================
         BRÚJULA DEL DESCUBRIMIENTO (COMPACTA Y DE BAJA ALTURA)
         ======================================================================= -->
    <div class="discovery-compact-wrap">
      <div class="discovery-compact-bar">
        
        <!-- Icono Brújula -->
        <div class="compass-icon-badge" title="Brújula del Descubrimiento">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
          </svg>
        </div>

        <!-- Tira compacta de 3 accesos rápidos -->
        <div class="discovery-items-grid">
          
          <!-- 1. Más Leído -->
          <a href="/es/posts/dafo-cuantitativo-matriz-came/" class="disco-item" title="DAFO Cuantitativo y Matriz CAME">
            <div class="disco-badge-title">
              <span class="disco-pill-tag tag-pop" id="badgePop">🔥 Más Leído</span>
              <span class="disco-item-title" id="titlePop">DAFO Cuantitativo & CAME</span>
            </div>
            <span style="font-size: 0.75rem; color: var(--accent); font-weight: 600;">→</span>
          </a>

          <!-- 2. Último Post -->
          <a href="/es/posts/sdd_vs_vibe_coding/" class="disco-item" title="SDD vs. Vibe Coding con IA en 2026">
            <div class="disco-badge-title">
              <span class="disco-pill-tag tag-lat" id="badgeLat">⚡ Última Publicación</span>
              <span class="disco-item-title" id="titleLat">SDD vs. Vibe Coding</span>
            </div>
            <span style="font-size: 0.75rem; color: var(--accent); font-weight: 600;">→</span>
          </a>

          <!-- 3. Post Aleatorio Interactivo -->
          <div class="disco-item" style="cursor: default;">
            <div class="disco-badge-title" style="flex-grow: 1;">
              <span class="disco-pill-tag tag-rnd" id="badgeRnd">🎲 Aleatorio</span>
              <a href="/es/posts/graphrag/" id="rndMiniLink" class="disco-item-title" style="text-decoration: none; color: inherit; display: block;">
                <span id="rndMiniTitle">GraphRAG: Vectores y Grafos</span>
              </a>
            </div>
            <button class="btn-shuffle-mini" id="btnMiniReroll" title="Generar otro post al azar">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
              <span id="labelBarajar">Barajar</span>
            </button>
          </div>

        </div>

      </div>
    </div>

    <!-- =======================================================================
         01 / RECURSOS & PACKS PROFESIONALES (Hub Escalable de Monetización)
         ======================================================================= -->
    <section class="section-block" id="recursos">
      <div class="section-heading">
        <span class="section-tag">01 / Recursos</span>
        <h2 class="section-title" id="secRecursosTitle">Recursos & Packs Profesionales</h2>
        <p class="section-desc" id="secRecursosDesc">
          Modelos cuantitativos, plantillas de decisión y guías metodológicas diseñadas para el ámbito profesional, comités directivos y control corporativo.
        </p>
      </div>

      <div class="recursos-lead-box">
        <div class="recursos-top-row">
          <div class="recursos-lead-title">
            <span>⚡ Executive Decision Packs</span>
            <span class="recursos-lead-badge" id="badgePacksStatus">Estreno Inminente</span>
          </div>
          <span style="font-size: 0.78rem; color: var(--text-light); font-family: var(--font-mono);" id="sublinePacks">Del cálculo cuantitativo a la aprobación de Comité</span>
        </div>
        <p class="recursos-lead-desc" id="descPacksLead">
          Herramientas para defender decisiones estratégicas ante juntas y comités: modelos en Excel protegidos con fórmulas matriciales, diapositivas PowerPoint 16:9 con Pirámide de Minto y guías metodológicas en PDF.
        </p>

        <!-- Muestrario de los Recursos -->
        <div class="recursos-items-grid">
          
          <div class="recurso-card-item">
            <div>
              <div class="recurso-item-icon">🎯</div>
              <div class="recurso-item-name">DAFO Cuantitativo & CAME</div>
              <div class="recurso-item-detail" id="recDetail1">Ponderación numérica de factores, matriz CAME automática y slide ejecutiva de junta.</div>
            </div>
            <div class="recurso-item-price">5€ · Bestseller</div>
          </div>

          <div class="recurso-card-item">
            <div>
              <div class="recurso-item-icon">🛡️</div>
              <div class="recurso-item-name">5 Fuerzas de Porter</div>
              <div class="recurso-item-detail" id="recDetail2">Scoring cuantitativo de 0 a 10 por fuerza, gráfico radar dinámico y análisis de poder.</div>
            </div>
            <div class="recurso-item-price">6€ · Suite MBA</div>
          </div>

          <div class="recurso-card-item">
            <div>
              <div class="recurso-item-icon">📦</div>
              <div class="recurso-item-name" id="recName3">Nuevos Packs & Guías</div>
              <div class="recurso-item-detail" id="recDetail3">Próximas incorporaciones: PESTEL, Matrices BCG, Priorización RICE y Business Cases.</div>
            </div>
            <div class="recurso-item-price" style="color: var(--text-light);" id="recPrice3">En catálogo</div>
          </div>

        </div>

        <div class="recursos-footer-action">
          <span style="color: var(--text-muted);" id="recFooterGuarantee">Incluye facturación B2B deducible y descarga instantánea</span>
          <a href="/es/recursos/" class="link-more" id="recFooterLink">Ver catálogo completo de Recursos →</a>
        </div>
      </div>
    </section>

    <!-- =======================================================================
         02 / CONTENIDOS (El Blog en 4 Temáticas)
         ======================================================================= -->
    <section class="section-block" id="blog">
      <div class="section-heading">
        <span class="section-tag">02 / Contenidos</span>
        <h2 class="section-title" id="secBlogTitle">El Blog en 4 Temáticas</h2>
        <p class="section-desc" id="secBlogDesc">
          Explora los 98 artículos clasificados por ámbito de conocimiento. Selecciona una categoría para explorar sus lecturas recomendadas:
        </p>
      </div>

      <!-- Selectores de Categoría Minimalistas -->
      <div class="cat-selector-row">
        <button class="cat-pill-btn active" data-cat="tecnicos" onclick="selectCat('tecnicos')">
          <span class="cat-pill-icon">🧠</span>
          <span class="cat-pill-title" id="catTab1">Artículos Técnicos</span>
          <span class="cat-pill-count">41 posts</span>
        </button>

        <button class="cat-pill-btn" data-cat="proyectos" onclick="selectCat('proyectos')">
          <span class="cat-pill-icon">🛠️</span>
          <span class="cat-pill-title" id="catTab2">Proyectos Tech</span>
          <span class="cat-pill-count">34 posts</span>
        </button>

        <button class="cat-pill-btn" data-cat="startups" onclick="selectCat('startups')">
          <span class="cat-pill-icon">🚀</span>
          <span class="cat-pill-title" id="catTab3">Startups & Casos</span>
          <span class="cat-pill-count">12 posts</span>
        </button>

        <button class="cat-pill-btn" data-cat="biografias" onclick="selectCat('biografias')">
          <span class="cat-pill-icon">🏛️</span>
          <span class="cat-pill-title" id="catTab4">Biografías</span>
          <span class="cat-pill-count">11 posts</span>
        </button>
      </div>

      <!-- Lista limpia de artículos de la categoría seleccionada -->
      <div class="cat-posts-list" id="catPostsContainer">
        <!-- Rellenado dinámicamente con JavaScript -->
      </div>

      <div style="text-align: right; margin-top: 14px;">
        <a href="/es/posts/" class="link-more" id="linkArchiveAll">Ver archivo completo del blog →</a>
      </div>
    </section>

    <!-- =======================================================================
         03 / APLICACIONES & EXPERIMENTOS
         ======================================================================= -->
    <section class="section-block" id="apps">
      <div class="section-heading">
        <span class="section-tag">03 / Ecosistema</span>
        <h2 class="section-title" id="secAppsTitle">Aplicaciones & Experimentos</h2>
        <p class="section-desc" id="secAppsDesc">
          Herramientas interactivas en vivo desarrolladas para explorar tecnologías web, inteligencia artificial y resolver problemas cotidianos.
        </p>
      </div>

      <div class="apps-minimal-grid">
        
        <!-- App: LifeOps -->
        <a href="/apps/lifeops/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">🚀</span>
            <div>
              <div class="app-box-name">
                LifeOps
                <span class="app-box-badge" id="badgeApp1">Sistema</span>
              </div>
              <p class="app-box-desc" id="descApp1">Sistema operativo integral personal y profesional con Kanban, biblioteca, cine y dashboard 360°.</p>
            </div>
          </div>
          <span class="app-box-arrow" id="btnApp1">Abrir app →</span>
        </a>

        <!-- App: Radar de Obsolescencia -->
        <a href="/apps/obs-management/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">📡</span>
            <div>
              <div class="app-box-name">
                Radar de Obsolescencia
                <span class="app-box-badge" id="badgeApp2">IA</span>
              </div>
              <p class="app-box-desc" id="descApp2">Dashboard ejecutivo impulsado por agentes IA para mitigar el riesgo en la cadena de suministro industrial.</p>
            </div>
          </div>
          <span class="app-box-arrow" id="btnApp2">Abrir dashboard →</span>
        </a>

        <!-- App: Neon Snake (JUEGO INTEGRADO EN APPS) -->
        <a href="/games/snake/" class="app-box" target="_blank">
          <div class="app-box-top">
            <span class="app-box-icon">🐍</span>
            <div>
              <div class="app-box-name">
                Neon Snake Cyberpunk
                <span class="app-box-badge badge-arcade" id="badgeApp3">Arcade / Juego</span>
              </div>
              <p class="app-box-desc" id="descApp3">Versión arcade del clásico Snake con estética cyberpunk y ranking global en tiempo real con Supabase.</p>
            </div>
          </div>
          <span class="app-box-arrow" id="btnApp3">Jugar ahora →</span>
        </a>

        <!-- App: El Tiempo -->
        <a href="/apps/weather/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">🌤️</span>
            <div>
              <div class="app-box-name">
                El Tiempo & ML
                <span class="app-box-badge" id="badgeApp4">Previsión</span>
              </div>
              <p class="app-box-desc" id="descApp4">Consulta meteorológica en tiempo real enriquecida con modelos predictivos de Machine Learning.</p>
            </div>
          </div>
          <span class="app-box-arrow" id="btnApp4">Abrir app →</span>
        </a>

        <!-- App: Conversor de Unidades -->
        <a href="/apps/conversor/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">🔄</span>
            <div>
              <div class="app-box-name">
                Conversor de Unidades
                <span class="app-box-badge" id="badgeApp5">Herramienta</span>
              </div>
              <p class="app-box-desc" id="descApp5">Navaja suiza rápida y ligera para transformar unidades de medida, magnitud e ingeniería.</p>
            </div>
          </div>
          <span class="app-box-arrow" id="btnApp5">Abrir app →</span>
        </a>

        <!-- App: Flashcards -->
        <a href="/apps/flashcards/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">🎴</span>
            <div>
              <div class="app-box-name">
                Flashcards
                <span class="app-box-badge" id="badgeApp6">Estudio</span>
              </div>
              <p class="app-box-desc" id="descApp6">Aplicación interactiva para memorizar conceptos técnicos usando repetición espaciada y gamificación.</p>
            </div>
          </div>
          <span class="app-box-arrow" id="btnApp6">Abrir app →</span>
        </a>

      </div>
    </section>

    <!-- =======================================================================
         REDES SOCIALES INFERIORES
         ======================================================================= -->
    <section class="social-bottom-section">
      <div class="social-bottom-label" id="socialLabel">
        Conéctate y sigue las novedades de Datalaria:
      </div>
      <div class="social-bottom-links">
        <a href="https://github.com/Dalaez" class="social-chip" target="_blank" rel="noopener">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
          <span>GitHub</span>
        </a>

        <a href="https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/" class="social-chip" target="_blank" rel="noopener">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
          <span>LinkedIn</span>
        </a>

        <a href="https://twitter.com/Dalaez" class="social-chip" target="_blank" rel="noopener">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path></svg>
          <span>Twitter / X</span>
        </a>
      </div>
    </section>

    <!-- =======================================================================
         NEWSLETTER INTEGRADA (Idéntica a extend_footer.html de producción)
         ======================================================================= -->
    <div class="newsletter-section">
      <div class="newsletter-container">
        <div class="newsletter-header">
          <svg class="newsletter-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
            <polyline points="22,6 12,13 2,6"></polyline>
          </svg>
          <h3 class="newsletter-title" id="nlTitle">¡Suscríbete a la Newsletter!</h3>
        </div>
        <p class="newsletter-description" id="nlDesc">Recibe novedades sobre datos, IA y tecnología en tu correo.</p>
        
        <form id="newsletter-form" class="newsletter-form" onsubmit="event.preventDefault(); handleNlSubmit();">
          <div class="newsletter-inputs">
            <input type="text" id="newsletter-name" name="name" placeholder="Tu nombre" required />
            <input type="email" id="newsletter-email" name="email" placeholder="Tu email" required />
            <select id="newsletter-lang" name="language" class="newsletter-select" title="Idioma preferido:">
              <option value="es" selected>🇪🇸 ES</option>
              <option value="en">🇬🇧 EN</option>
            </select>
            <button type="submit" class="newsletter-btn" id="newsletter-submit">Suscribirse</button>
          </div>
          <p id="newsletter-message" class="newsletter-message"></p>
        </form>
      </div>
    </div>

  </main>

  <!-- =======================================================================
       FOOTER LIMPIO (Sin "Daniel Aláez", alineado a config.yaml de producción)
       ======================================================================= -->
  <footer class="site-footer">
    <div class="container footer-inner">
      <div id="footerCopy">
        © 2026 <strong>Datalaria</strong>. Todos los derechos reservados.
      </div>
      <ul class="footer-nav">
        <li><a href="#blog" id="fnBlog">Blog</a></li>
        <li><a href="#recursos" id="fnRecursos">Recursos</a></li>
        <li><a href="#apps" id="fnApps">Apps</a></li>
        <li><a href="/es/sobre-mi/" id="fnAbout">Sobre mí</a></li>
        <li><a href="/es/contact/" id="fnContact">Contacto</a></li>
      </ul>
    </div>
  </footer>

  <!-- =======================================================================
       CHAT COPILOT DE ALGOLIA (Idéntico a algolia-agent.html de producción)
       ======================================================================= -->
  <div id="ops-agent-wrapper">
    <!-- Botón flotante -->
    <button id="ops-agent-toggle" class="ops-agent-btn" aria-label="Abrir Copilot de Ingeniería y Operaciones" title="Copilot de IA">
      <svg class="ops-agent-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
      </svg>
      <span class="ops-agent-badge">AI</span>
    </button>

    <!-- Caja de Chat Flotante -->
    <div id="ops-agent-container" class="ops-agent-chat hidden">
      <div class="ops-agent-header">
        <div class="ops-agent-title">
          <span>🔍</span>
          <span>Ops Engineering Copilot</span>
        </div>
        <button id="ops-agent-close" class="ops-agent-close" aria-label="Cerrar chat">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div class="ops-agent-messages" id="opsMessages">
        <div class="ops-welcome-message">
          <p id="opsWelcome1">¡Hola! Soy tu asistente de Operations Engineering.</p>
          <p class="ops-welcome-subtitle" id="opsWelcome2">Pregúntame sobre S&OP, proyectos, productos o equipos.</p>
        </div>
      </div>

      <div class="ops-agent-input-area">
        <input type="text" id="opsInput" placeholder="Escribe tu pregunta..." autocomplete="off">
        <button class="ops-agent-send" id="opsSendBtn" title="Enviar">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- =======================================================================
       INTERACTIVIDAD COMPLETA (Tema, Multilingüismo, Brújula, Chat)
       ======================================================================= -->
  <script>
    const postsData = {json_posts_str};

    const categories = {{
      tecnicos: postsData.filter(p => p.category === 'tecnicos'),
      proyectos: postsData.filter(p => p.category === 'proyectos'),
      startups: postsData.filter(p => p.category === 'startups'),
      biografias: postsData.filter(p => p.category === 'biografias')
    }};

    // 1. Conmutador de Tema Claro / Oscuro (Idéntico a PaperMod con icono de luna / sol)
    const htmlElem = document.documentElement;
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeEmoji = document.getElementById('themeEmoji');

    function applyTheme(theme) {{
      htmlElem.setAttribute('data-theme', theme);
      localStorage.setItem('datalaria-theme', theme);
      if (theme === 'dark') {{
        themeEmoji.textContent = '☀️';
      }} else {{
        themeEmoji.textContent = '🌙';
      }}
    }}

    themeToggleBtn.addEventListener('click', () => {{
      const current = htmlElem.getAttribute('data-theme') || 'light';
      applyTheme(current === 'light' ? 'dark' : 'light');
    }});

    const userPrefTheme = localStorage.getItem('datalaria-theme') || 'light';
    applyTheme(userPrefTheme);

    // 2. Multilingüismo Interactivo (ES / EN)
    let currentLang = 'es';
    const langSwitchLink = document.getElementById('langSwitchLink');

    const i18nTexts = {{
      es: {{
        langNext: 'En',
        menuBlog: 'Blog',
        menuRecursos: 'Recursos',
        menuApps: 'Apps',
        menuAbout: 'Sobre mí',
        menuContact: 'Contacto',
        tagline: 'Un portal para el aprendizaje en los datos, la inteligencia artificial, la tecnología y la gestión empresarial.',
        badgePop: '🔥 Más Leído',
        badgeLat: '⚡ Última Publicación',
        badgeRnd: '🎲 Aleatorio',
        labelBarajar: 'Barajar',
        secRecursosTitle: 'Recursos & Packs Profesionales',
        secRecursosDesc: 'Modelos cuantitativos, plantillas de decisión y guías metodológicas diseñadas para el ámbito profesional, comités directivos y control corporativo.',
        badgePacksStatus: 'Estreno Inminente',
        sublinePacks: 'Del cálculo cuantitativo a la aprobación de Comité',
        descPacksLead: 'Herramientas para defender decisiones estratégicas ante juntas y comités: modelos en Excel protegidos con fórmulas matriciales, diapositivas PowerPoint 16:9 con Pirámide de Minto y guías metodológicas en PDF.',
        recDetail1: 'Ponderación numérica de factores, matriz CAME automática y slide ejecutiva de junta.',
        recDetail2: 'Scoring cuantitativo de 0 a 10 por fuerza, gráfico radar dinámico y análisis de poder.',
        recName3: 'Nuevos Packs & Guías',
        recDetail3: 'Próximas incorporaciones: PESTEL, Matrices BCG, Priorización RICE y Business Cases.',
        recPrice3: 'En catálogo',
        recFooterGuarantee: 'Incluye facturación B2B deducible y descarga instantánea',
        recFooterLink: 'Ver catálogo completo de Recursos →',
        secBlogTitle: 'El Blog en 4 Temáticas',
        secBlogDesc: 'Explora los 98 artículos clasificados por ámbito de conocimiento. Selecciona una categoría para explorar sus lecturas recomendadas:',
        catTab1: 'Artículos Técnicos',
        catTab2: 'Proyectos Tech',
        catTab3: 'Startups & Casos',
        catTab4: 'Biografías',
        linkArchiveAll: 'Ver archivo completo del blog →',
        secAppsTitle: 'Aplicaciones & Experimentos',
        secAppsDesc: 'Herramientas interactivas en vivo desarrolladas para explorar tecnologías web, inteligencia artificial y resolver problemas cotidianos.',
        btnApp: 'Abrir app →',
        socialLabel: 'Conéctate y sigue las novedades de Datalaria:',
        nlTitle: '¡Suscríbete a la Newsletter!',
        nlDesc: 'Recibe novedades sobre datos, IA y tecnología en tu correo.',
        nlNamePh: 'Tu nombre',
        nlEmailPh: 'Tu email',
        nlSubmit: 'Suscribirse',
        footerCopy: '© 2026 <strong>Datalaria</strong>. Todos los derechos reservados.',
        opsWelcome1: '¡Hola! Soy tu asistente de Operations Engineering.',
        opsWelcome2: 'Pregúntame sobre S&OP, proyectos, productos o equipos.',
        opsInputPh: 'Escribe tu pregunta...'
      }},
      en: {{
        langNext: 'Es',
        menuBlog: 'Blog',
        menuRecursos: 'Resources',
        menuApps: 'Apps',
        menuAbout: 'About',
        menuContact: 'Contact',
        tagline: 'A digital portal for learning data, artificial intelligence, technology, and business management.',
        badgePop: '🔥 Most Read',
        badgeLat: '⚡ Latest Post',
        badgeRnd: '🎲 Random',
        labelBarajar: 'Shuffle',
        secRecursosTitle: 'Professional Resources & Decision Packs',
        secRecursosDesc: 'Quantitative models, decision frameworks, and executive methodologies built for C-Level leadership and corporate governance.',
        badgePacksStatus: 'Coming Soon',
        sublinePacks: 'From quantitative calculation to board approval',
        descPacksLead: 'Tools built to defend strategic decisions before executive committees: Excel models protected with array formulas, 16:9 Minto Pyramid decks, and PDF methodological guides.',
        recDetail1: 'Numerical weighting of factors, automated TOWS/CAME matrix, and board-ready slide.',
        recDetail2: 'Quantitative scoring from 0 to 10 per force, auto-generated radar chart, and market analysis.',
        recName3: 'Upcoming Packs & Guides',
        recDetail3: 'Coming additions: PESTEL, Dynamic BCG Matrices, RICE Prioritization, and Financial Cases.',
        recPrice3: 'In catalog',
        recFooterGuarantee: 'Includes B2B invoice with VAT and instant digital download',
        recFooterLink: 'Explore full Resources collection →',
        secBlogTitle: 'The Blog in 4 Core Topics',
        secBlogDesc: 'Explore all 98 articles organized by field of knowledge. Select a category to inspect featured articles:',
        catTab1: 'Technical Articles',
        catTab2: 'Tech Projects',
        catTab3: 'Startups & Scaleups',
        catTab4: 'Biographies',
        linkArchiveAll: 'View full blog archive →',
        secAppsTitle: 'Interactive Apps & Experiments',
        secAppsDesc: 'Live web tools and software built to experiment with modern engineering, AI, and practical problem solving.',
        btnApp: 'Launch app →',
        socialLabel: 'Connect and follow updates from Datalaria:',
        nlTitle: 'Subscribe to the Newsletter!',
        nlDesc: 'Get the latest insights on data, AI, and technology directly in your inbox.',
        nlNamePh: 'Your name',
        nlEmailPh: 'Your email',
        nlSubmit: 'Subscribe',
        footerCopy: '© 2026 <strong>Datalaria</strong>. All rights reserved.',
        opsWelcome1: 'Hello! I am your Operations Engineering assistant.',
        opsWelcome2: 'Ask me about S&OP, projects, architectures, or supply chain.',
        opsInputPh: 'Type your question...'
      }}
    }};

    function setLanguage(lang) {{
      currentLang = lang;
      const t = i18nTexts[lang];

      langSwitchLink.textContent = t.langNext;
      document.getElementById('menuBlog').textContent = t.menuBlog;
      document.getElementById('menuRecursos').childNodes[0].nodeValue = t.menuRecursos;
      document.getElementById('menuApps').textContent = t.menuApps;
      document.getElementById('menuAbout').textContent = t.menuAbout;
      document.getElementById('menuContact').textContent = t.menuContact;

      document.getElementById('taglineText').textContent = t.tagline;
      document.getElementById('badgePop').textContent = t.badgePop;
      document.getElementById('badgeLat').textContent = t.badgeLat;
      document.getElementById('badgeRnd').textContent = t.badgeRnd;
      document.getElementById('labelBarajar').textContent = t.labelBarajar;

      document.getElementById('secRecursosTitle').textContent = t.secRecursosTitle;
      document.getElementById('secRecursosDesc').textContent = t.secRecursosDesc;
      document.getElementById('badgePacksStatus').textContent = t.badgePacksStatus;
      document.getElementById('sublinePacks').textContent = t.sublinePacks;
      document.getElementById('descPacksLead').textContent = t.descPacksLead;
      document.getElementById('recDetail1').textContent = t.recDetail1;
      document.getElementById('recDetail2').textContent = t.recDetail2;
      document.getElementById('recName3').textContent = t.recName3;
      document.getElementById('recDetail3').textContent = t.recDetail3;
      document.getElementById('recPrice3').textContent = t.recPrice3;
      document.getElementById('recFooterGuarantee').textContent = t.recFooterGuarantee;
      document.getElementById('recFooterLink').textContent = t.recFooterLink;

      document.getElementById('secBlogTitle').textContent = t.secBlogTitle;
      document.getElementById('secBlogDesc').textContent = t.secBlogDesc;
      document.getElementById('catTab1').textContent = t.catTab1;
      document.getElementById('catTab2').textContent = t.catTab2;
      document.getElementById('catTab3').textContent = t.catTab3;
      document.getElementById('catTab4').textContent = t.catTab4;
      document.getElementById('linkArchiveAll').textContent = t.linkArchiveAll;

      document.getElementById('secAppsTitle').textContent = t.secAppsTitle;
      document.getElementById('secAppsDesc').textContent = t.secAppsDesc;
      document.getElementById('socialLabel').textContent = t.socialLabel;

      document.getElementById('nlTitle').textContent = t.nlTitle;
      document.getElementById('nlDesc').textContent = t.nlDesc;
      document.getElementById('newsletter-name').placeholder = t.nlNamePh;
      document.getElementById('newsletter-email').placeholder = t.nlEmailPh;
      document.getElementById('newsletter-submit').textContent = t.nlSubmit;

      document.getElementById('footerCopy').innerHTML = t.footerCopy;
      document.getElementById('fnBlog').textContent = t.menuBlog;
      document.getElementById('fnRecursos').textContent = t.menuRecursos;
      document.getElementById('fnApps').textContent = t.menuApps;
      document.getElementById('fnAbout').textContent = t.menuAbout;
      document.getElementById('fnContact').textContent = t.menuContact;

      document.getElementById('opsWelcome1').textContent = t.opsWelcome1;
      document.getElementById('opsWelcome2').textContent = t.opsWelcome2;
      document.getElementById('opsInput').placeholder = t.opsInputPh;
    }}

    langSwitchLink.addEventListener('click', () => {{
      setLanguage(currentLang === 'es' ? 'en' : 'es');
    }});

    // 3. Selector de Categorías (02 Contenidos)
    function selectCat(catKey) {{
      document.querySelectorAll('.cat-pill-btn').forEach(btn => {{
        if (btn.getAttribute('data-cat') === catKey) {{
          btn.classList.add('active');
        }} else {{
          btn.classList.remove('active');
        }}
      }});

      const container = document.getElementById('catPostsContainer');
      const list = categories[catKey] || [];
      const topSix = list.slice(0, 6);

      container.innerHTML = topSix.map(post => `
        <a href="${{post.url}}" class="cat-post-row">
          <span class="cat-post-main">
            <span>•</span>
            <span>${{post.title}}</span>
          </span>
          <span class="cat-post-date">${{post.date || 'Reciente'}}</span>
        </a>
      `).join('');
    }}

    selectCat('tecnicos');

    // 4. Post Aleatorio en la Brújula Compacta
    const btnMiniReroll = document.getElementById('btnMiniReroll');
    const rndMiniTitle = document.getElementById('rndMiniTitle');
    const rndMiniLink = document.getElementById('rndMiniLink');

    function rerollMiniRandom() {{
      const idx = Math.floor(Math.random() * postsData.length);
      const post = postsData[idx];

      rndMiniTitle.style.opacity = '0';
      setTimeout(() => {{
        rndMiniTitle.textContent = post.title;
        rndMiniLink.href = post.url;
        rndMiniLink.title = post.title;
        rndMiniTitle.style.opacity = '1';
      }}, 120);
    }}

    btnMiniReroll.addEventListener('click', rerollMiniRandom);

    // 5. Simulación Newsletter
    function handleNlSubmit() {{
      const msg = document.getElementById('newsletter-message');
      msg.textContent = currentLang === 'es' ? '¡Gracias por suscribirte a Datalaria!' : 'Thank you for subscribing to Datalaria!';
      msg.className = 'newsletter-message success';
      document.getElementById('newsletter-form').reset();
    }}

    // 6. Algolia Chat Copilot Toggle
    const opsToggle = document.getElementById('ops-agent-toggle');
    const opsClose = document.getElementById('ops-agent-close');
    const opsChat = document.getElementById('ops-agent-container');
    const opsInput = document.getElementById('opsInput');
    const opsSendBtn = document.getElementById('opsSendBtn');
    const opsMessages = document.getElementById('opsMessages');

    opsToggle.addEventListener('click', () => {{
      opsChat.classList.toggle('hidden');
      if (!opsChat.classList.contains('hidden')) {{
        opsInput.focus();
      }}
    }});

    opsClose.addEventListener('click', () => {{
      opsChat.classList.add('hidden');
    }});

    function sendOpsMessage() {{
      const val = opsInput.value.trim();
      if (!val) return;

      const userMsgDiv = document.createElement('div');
      userMsgDiv.style.cssText = 'background: var(--ops-primary); color: white; padding: 8px 12px; border-radius: 12px 12px 2px 12px; align-self: flex-end; max-width: 80%;';
      userMsgDiv.textContent = val;
      opsMessages.appendChild(userMsgDiv);
      opsInput.value = '';

      setTimeout(() => {{
        const botMsgDiv = document.createElement('div');
        botMsgDiv.style.cssText = 'background: var(--bg-subtle); border: 1px solid var(--border-subtle); color: var(--ops-text); padding: 8px 12px; border-radius: 12px 12px 12px 2px; align-self: flex-start; max-width: 85%;';
        botMsgDiv.innerHTML = currentLang === 'es' 
          ? 'Gracias por tu consulta. He indexado 98 artículos de Datalaria sobre S&OP, modelos de decisión cuantitativos y proyectos de IA. Te sugiero explorar el <strong>DAFO Cuantitativo</strong> o el <strong>Proyecto LifeOps</strong>.'
          : 'Thank you for your question. I indexed 98 articles across Datalaria covering S&OP, decision frameworks, and AI projects. I recommend exploring the <strong>Quantitative SWOT</strong> or the <strong>LifeOps Project</strong>.';
        opsMessages.appendChild(botMsgDiv);
        opsMessages.scrollTop = opsMessages.scrollHeight;
      }}, 600);

      opsMessages.scrollTop = opsMessages.scrollHeight;
    }}

    opsSendBtn.addEventListener('click', sendOpsMessage);
    opsInput.addEventListener('keypress', (e) => {{
      if (e.key === 'Enter') sendOpsMessage();
    }});
  </script>
</body>
</html>
"""

with open('mockup_homepage_v4.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Created mockup_homepage_v4.html successfully!")
