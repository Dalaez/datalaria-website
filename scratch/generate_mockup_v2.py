import json

with open('scratch/posts_for_mockup.json', 'r', encoding='utf-8') as f:
    all_posts = json.load(f)

json_posts_str = json.dumps(all_posts, ensure_ascii=False)

html_code = f"""<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datalaria | Mockup Minimalista v2</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* ==========================================================================
       SISTEMA DE DISEÑO MINIMALISTA (Inspirado en hugo-bootstrap-theme & PaperMod)
       ========================================================================== */
    :root {{
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: 'JetBrains Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      
      /* Modo Claro (Limpio, espacioso, sutil) */
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
      --shadow-hover: 0 6px 16px rgba(0, 0, 0, 0.07);
    }}

    [data-theme="dark"] {{
      /* Modo Oscuro (Elegante, contrastado y sin estridencias) */
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
      --shadow-hover: 0 6px 16px rgba(0, 0, 0, 0.35);
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
      padding-top: 36px; /* Para la barra de aviso */
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
      max-width: 860px; /* Ancho editorial óptimo para lectura limpia y minimalista */
      margin: 0 auto;
      padding: 0 20px;
    }}

    /* ==========================================================================
       HEADER & NAVBAR
       ========================================================================== */
    header.site-header {{
      padding: 18px 0;
      position: sticky;
      top: 36px;
      z-index: 900;
      background: var(--bg-body);
      background: rgba(var(--bg-body), 0.9);
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

    .brand {{
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      color: var(--text-main);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .brand-icon {{
      width: 24px;
      height: 24px;
      object-fit: contain;
    }}

    .nav-menu {{
      display: flex;
      align-items: center;
      gap: 16px;
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

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-left: 8px;
    }}

    .theme-btn {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      transition: all 0.2s;
    }}
    .theme-btn:hover {{
      color: var(--text-main);
      border-color: var(--border-focus);
      background: var(--bg-hover);
    }}

    /* ==========================================================================
       MASTHEAD CENTRAL (Identidad Datalaria)
       ========================================================================== */
    .masthead {{
      text-align: center;
      padding: 70px 0 50px 0;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .masthead-logo {{
      width: 105px;
      height: 105px;
      object-fit: contain;
      margin-bottom: 20px;
      display: inline-block;
      transition: transform 0.3s ease;
    }}
    .masthead-logo:hover {{
      transform: scale(1.04);
    }}

    .masthead-title {{
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-main);
      margin-bottom: 12px;
    }}

    .masthead-bio {{
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 620px;
      margin: 0 auto 18px auto;
      line-height: 1.65;
    }}

    .masthead-km0 {{
      font-size: 0.95rem;
      color: var(--text-light);
      margin-bottom: 24px;
      font-style: italic;
    }}

    .masthead-social {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
    }}

    .social-btn {{
      color: var(--text-muted);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      transition: color 0.2s, transform 0.2s;
    }}
    .social-btn:hover {{
      color: var(--text-main);
      transform: translateY(-2px);
    }}

    /* ==========================================================================
       SECCIONES MINIMALISTAS
       ========================================================================== */
    .section-block {{
      padding: 55px 0 45px 0;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .section-block:last-of-type {{
      border-bottom: none;
    }}

    .section-heading {{
      margin-bottom: 28px;
    }}

    .section-tag {{
      font-size: 0.74rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 6px;
      display: inline-block;
    }}

    .section-title {{
      font-size: 1.55rem;
      font-weight: 700;
      letter-spacing: -0.015em;
      color: var(--text-main);
      margin-bottom: 6px;
    }}

    .section-desc {{
      font-size: 0.92rem;
      color: var(--text-muted);
      max-width: 650px;
    }}

    /* ==========================================================================
       SECCIÓN 1: RECURSOS (HUB ESCALABLE)
       ========================================================================== */
    .recursos-lead-box {{
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px 26px;
      margin-bottom: 20px;
      position: relative;
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
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .recursos-lead-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .recursos-lead-badge {{
      font-size: 0.72rem;
      background: var(--accent-soft);
      color: var(--accent);
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 600;
    }}

    .recursos-lead-desc {{
      font-size: 0.9rem;
      color: var(--text-muted);
      line-height: 1.55;
      margin-bottom: 18px;
    }}

    .recursos-items-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-bottom: 18px;
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
      padding: 16px;
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
      font-size: 1.35rem;
      margin-bottom: 8px;
    }}

    .recurso-item-name {{
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 4px;
    }}

    .recurso-item-detail {{
      font-size: 0.78rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 10px;
      flex-grow: 1;
    }}

    .recurso-item-price {{
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent);
      font-family: var(--font-mono);
    }}

    .recursos-footer-action {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 14px;
      border-top: 1px solid var(--border-subtle);
      font-size: 0.84rem;
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
       SECCIÓN 2: APLICACIONES & EXPERIMENTOS (CON JUEGOS INTEGRADOS)
       ========================================================================== */
    .apps-minimal-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
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
      padding: 18px 20px;
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
      gap: 14px;
      margin-bottom: 12px;
    }}

    .app-box-icon {{
      font-size: 1.6rem;
      line-height: 1;
      padding: 8px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
    }}

    .app-box-name {{
      font-size: 1rem;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .app-box-badge {{
      font-size: 0.65rem;
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
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-top: 4px;
    }}

    .app-box-arrow {{
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--accent);
      align-self: flex-end;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    /* ==========================================================================
       SECCIÓN 3: LAS 4 CATEGORÍAS DEL BLOG (MINIMALISTA)
       ========================================================================== */
    .cat-selector-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 20px;
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
      padding: 12px 14px;
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
      font-size: 1.1rem;
      margin-bottom: 4px;
      display: block;
    }}
    .cat-pill-title {{
      font-size: 0.85rem;
      font-weight: 600;
      display: block;
      margin-bottom: 2px;
    }}
    .cat-pill-count {{
      font-size: 0.72rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    /* Lista limpia de artículos de la categoría seleccionada */
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
      padding: 13px 18px;
      border-bottom: 1px solid var(--border-subtle);
      text-decoration: none;
      color: inherit;
      transition: background-color 0.15s ease;
      gap: 16px;
    }}
    .cat-post-row:last-child {{
      border-bottom: none;
    }}
    .cat-post-row:hover {{
      background-color: var(--bg-subtle);
    }}

    .cat-post-main {{
      font-size: 0.9rem;
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
      font-size: 0.75rem;
      color: var(--text-light);
      font-family: var(--font-mono);
      white-space: nowrap;
    }}

    /* ==========================================================================
       SECCIÓN 4: BRÚJULA DEL DESCUBRIMIENTO (MINIMALISTA)
       ========================================================================== */
    .discovery-cards-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }}

    @media (max-width: 800px) {{
      .discovery-cards-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .disco-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
    }}
    .disco-card:hover {{
      border-color: var(--border-focus);
      box-shadow: var(--shadow-sm);
    }}

    .disco-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .disco-tag {{
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .tag-pop {{ color: #dc2626; }}
    .tag-lat {{ color: #16a34a; }}
    .tag-rnd {{ color: #9333ea; }}

    .btn-reroll {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.72rem;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }}
    .btn-reroll:hover {{
      color: var(--text-main);
      border-color: var(--text-main);
      background: var(--bg-subtle);
    }}

    .disco-title {{
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-main);
      line-height: 1.4;
      margin-bottom: 8px;
    }}

    .disco-desc {{
      font-size: 0.8rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 14px;
      flex-grow: 1;
    }}

    .disco-link {{
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--accent);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .disco-link:hover {{
      text-decoration: underline;
    }}

    /* ==========================================================================
       FOOTER
       ========================================================================== */
    footer.site-footer {{
      padding: 40px 0 30px 0;
      margin-top: 50px;
      border-top: 1px solid var(--border-subtle);
      font-size: 0.82rem;
      color: var(--text-muted);
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
  </style>
</head>
<body>

  <!-- BARRA INFORMATIVA DE ITERACIÓN -->
  <div class="mockup-topbar">
    <div>
      <span class="mockup-pill">Fase 0 • Mockup v2</span>
      &nbsp; <span>Diseño minimalista: Masthead central continuo + Secciones hacia abajo</span>
    </div>
    <div style="font-family: var(--font-mono); font-size: 0.72rem;">
      98 Artículos · 6 Apps · Recursos Hub
    </div>
  </div>

  <!-- HEADER Y NAVEGACIÓN -->
  <header class="site-header">
    <div class="container nav-inner">
      <a href="#" class="brand">
        <img src="static/images/datalaria_logo_transp.png" alt="Datalaria" class="brand-icon" onerror="this.src='/images/datalaria_logo_transp.png';">
        <span>Datalaria</span>
      </a>

      <nav>
        <ul class="nav-menu">
          <li class="nav-item"><a href="#blog">Blog</a></li>
          <li class="nav-item nav-recursos">
            <a href="#recursos">Recursos<span class="nav-badge">Pro</span></a>
          </li>
          <li class="nav-item"><a href="#apps">Apps</a></li>
          <li class="nav-item"><a href="/es/sobre-mi/">Sobre mí</a></li>
          <li class="nav-item"><a href="/es/contact/">Contacto</a></li>
        </ul>
      </nav>

      <div class="nav-actions">
        <button class="theme-btn" id="themeToggleBtn" title="Cambiar tema">
          <span id="themeLabel">Modo Oscuro</span>
          <svg id="themeIcon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>
      </div>
    </div>
  </header>

  <main class="container">

    <!-- =======================================================================
         MASTHEAD CENTRAL (Identidad Datalaria)
         ======================================================================= -->
    <section class="masthead">
      <img src="static/images/datalaria_logo_transp.png" alt="Datalaria" class="masthead-logo" onerror="this.src='/images/datalaria_logo_transp.png';">
      <h1 class="masthead-title">Datalaria</h1>
      <p class="masthead-bio">
        Bienvenido a mi cuaderno de bitácora digital. Aquí exploro y documento mi viaje de aprendizaje en el mundo de los datos, la inteligencia artificial, la tecnología y la industria.
      </p>
      <p class="masthead-km0">Este es mi kilómetro 0.</p>

      <div class="masthead-social">
        <a href="https://github.com/Dalaez" class="social-btn" title="GitHub" target="_blank" rel="noopener">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
        </a>
        <a href="https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/" class="social-btn" title="LinkedIn" target="_blank" rel="noopener">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
        </a>
        <a href="https://twitter.com/Dalaez" class="social-btn" title="Twitter / X" target="_blank" rel="noopener">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path></svg>
        </a>
      </div>
    </section>

    <!-- =======================================================================
         SECCIÓN 1: RECURSOS (Hub Escalable para Monetización)
         ======================================================================= -->
    <section class="section-block" id="recursos">
      <div class="section-heading">
        <span class="section-tag">01 / Recursos</span>
        <h2 class="section-title">Recursos & Packs Profesionales</h2>
        <p class="section-desc">
          Modelos cuantitativos, plantillas de decisión y guías metodológicas diseñadas para el ámbito profesional, comités directivos y control corporativo.
        </p>
      </div>

      <!-- Bloque destacado del Hub de Recursos -->
      <div class="recursos-lead-box">
        <div class="recursos-top-row">
          <div class="recursos-lead-title">
            <span>⚡ Executive Decision Packs</span>
            <span class="recursos-lead-badge">Estreno Inminente</span>
          </div>
          <span style="font-size: 0.8rem; color: var(--text-light); font-family: var(--font-mono);">Del cálculo cuantitativo a la aprobación de Comité</span>
        </div>
        <p class="recursos-lead-desc">
          Diseñados para defender decisiones estratégicas en comités de dirección: modelos en Excel protegidos con fórmulas matriciales, diapositivas PowerPoint 16:9 con Pirámide de Minto y guías metodológicas en PDF.
        </p>

        <!-- Muestrario de los tipos de Recursos -->
        <div class="recursos-items-grid">
          
          <div class="recurso-card-item">
            <div>
              <div class="recurso-item-icon">🎯</div>
              <div class="recurso-item-name">DAFO Cuantitativo & CAME</div>
              <div class="recurso-item-detail">Ponderación numérica de factores, matriz CAME automática y slide de junta directiva.</div>
            </div>
            <div class="recurso-item-price">5€ · Bestseller</div>
          </div>

          <div class="recurso-card-item">
            <div>
              <div class="recurso-item-icon">🛡️</div>
              <div class="recurso-item-name">5 Fuerzas de Porter</div>
              <div class="recurso-item-detail">Scoring cuantitativo de 0 a 10 por fuerza, gráfico radar dinámico y análisis de poder.</div>
            </div>
            <div class="recurso-item-price">6€ · Suite MBA</div>
          </div>

          <div class="recurso-card-item">
            <div>
              <div class="recurso-item-icon">📦</div>
              <div class="recurso-item-name">Nuevos Packs & Guías</div>
              <div class="recurso-item-detail">Próximas incorporaciones: PESTEL, Matrices BCG, Priorización RICE y Business Cases.</div>
            </div>
            <div class="recurso-item-price" style="color: var(--text-light);">En catálogo</div>
          </div>

        </div>

        <div class="recursos-footer-action">
          <span style="color: var(--text-muted);">Incluye facturación B2B deducible y descarga instantánea</span>
          <a href="/es/recursos/" class="link-more">Ver colección completa en Recursos →</a>
        </div>
      </div>
    </section>

    <!-- =======================================================================
         SECCIÓN 2: APLICACIONES (Integrando Juegos)
         ======================================================================= -->
    <section class="section-block" id="apps">
      <div class="section-heading">
        <span class="section-tag">02 / Ecosistema</span>
        <h2 class="section-title">Aplicaciones & Experimentos</h2>
        <p class="section-desc">
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
                <span class="app-box-badge">Sistema</span>
              </div>
              <p class="app-box-desc">Sistema operativo integral personal y profesional con Kanban, biblioteca, cine y dashboard 360°.</p>
            </div>
          </div>
          <span class="app-box-arrow">Abrir app →</span>
        </a>

        <!-- App: Radar de Obsolescencia -->
        <a href="/apps/obs-management/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">📡</span>
            <div>
              <div class="app-box-name">
                Radar de Obsolescencia
                <span class="app-box-badge">IA</span>
              </div>
              <p class="app-box-desc">Dashboard ejecutivo impulsado por agentes IA para mitigar el riesgo en la cadena de suministro.</p>
            </div>
          </div>
          <span class="app-box-arrow">Abrir dashboard →</span>
        </a>

        <!-- App: Neon Snake (JUEGO INTEGRADO) -->
        <a href="/games/snake/" class="app-box" target="_blank">
          <div class="app-box-top">
            <span class="app-box-icon">🐍</span>
            <div>
              <div class="app-box-name">
                Neon Snake Cyberpunk
                <span class="app-box-badge badge-arcade">Arcade / Juego</span>
              </div>
              <p class="app-box-desc">Versión arcade del clásico Snake con estética cyberpunk y ranking global en tiempo real.</p>
            </div>
          </div>
          <span class="app-box-arrow">Jugar ahora →</span>
        </a>

        <!-- App: El Tiempo -->
        <a href="/apps/weather/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">🌤️</span>
            <div>
              <div class="app-box-name">
                El Tiempo & ML
                <span class="app-box-badge">Previsión</span>
              </div>
              <p class="app-box-desc">Consulta meteorológica en tiempo real enriquecida con modelos de predicción de Machine Learning.</p>
            </div>
          </div>
          <span class="app-box-arrow">Abrir app →</span>
        </a>

        <!-- App: Conversor de Unidades -->
        <a href="/apps/conversor/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">🔄</span>
            <div>
              <div class="app-box-name">
                Conversor de Unidades
                <span class="app-box-badge">Herramienta</span>
              </div>
              <p class="app-box-desc">Navaja suiza rápida y ligera para transformar unidades de medida e ingeniería.</p>
            </div>
          </div>
          <span class="app-box-arrow">Abrir app →</span>
        </a>

        <!-- App: Flashcards -->
        <a href="/apps/flashcards/" class="app-box">
          <div class="app-box-top">
            <span class="app-box-icon">🎴</span>
            <div>
              <div class="app-box-name">
                Flashcards
                <span class="app-box-badge">Estudio</span>
              </div>
              <p class="app-box-desc">Aplicación interactiva para memorizar conceptos técnicos usando tarjetas de memoria activa.</p>
            </div>
          </div>
          <span class="app-box-arrow">Abrir app →</span>
        </a>

      </div>
    </section>

    <!-- =======================================================================
         SECCIÓN 3: LAS 4 CATEGORÍAS DEL BLOG (98 ARTÍCULOS)
         ======================================================================= -->
    <section class="section-block" id="blog">
      <div class="section-heading">
        <span class="section-tag">03 / Contenidos</span>
        <h2 class="section-title">El Blog en 4 Temáticas</h2>
        <p class="section-desc">
          Explora los 98 artículos clasificados por ámbito de conocimiento. Selecciona una categoría para explorar sus lecturas recomendadas:
        </p>
      </div>

      <!-- Selectores de Categoría Minimalistas -->
      <div class="cat-selector-row">
        <button class="cat-pill-btn active" data-cat="tecnicos" onclick="selectCat('tecnicos')">
          <span class="cat-pill-icon">🧠</span>
          <span class="cat-pill-title">Artículos Técnicos</span>
          <span class="cat-pill-count">41 posts</span>
        </button>

        <button class="cat-pill-btn" data-cat="proyectos" onclick="selectCat('proyectos')">
          <span class="cat-pill-icon">🛠️</span>
          <span class="cat-pill-title">Proyectos Tech</span>
          <span class="cat-pill-count">34 posts</span>
        </button>

        <button class="cat-pill-btn" data-cat="startups" onclick="selectCat('startups')">
          <span class="cat-pill-icon">🚀</span>
          <span class="cat-pill-title">Startups & Casos</span>
          <span class="cat-pill-count">12 posts</span>
        </button>

        <button class="cat-pill-btn" data-cat="biografias" onclick="selectCat('biografias')">
          <span class="cat-pill-icon">🏛️</span>
          <span class="cat-pill-title">Biografías</span>
          <span class="cat-pill-count">11 posts</span>
        </button>
      </div>

      <!-- Lista limpia de artículos de la categoría seleccionada -->
      <div class="cat-posts-list" id="catPostsContainer">
        <!-- Rellenado dinámicamente con JavaScript -->
      </div>

      <div style="text-align: right; margin-top: 14px;">
        <a href="/es/posts/" class="link-more">Ver archivo completo del blog →</a>
      </div>
    </section>

    <!-- =======================================================================
         SECCIÓN 4: BRÚJULA DEL DESCUBRIMIENTO
         ======================================================================= -->
    <section class="section-block" id="brujula">
      <div class="section-heading">
        <span class="section-tag">04 / Navegación Rápida</span>
        <h2 class="section-title">Brújula del Descubrimiento</h2>
        <p class="section-desc">
          Tres accesos inmediatos para empezar a leer: el más visitado, el último publicado o una sugerencia al azar.
        </p>
      </div>

      <div class="discovery-cards-grid">
        
        <!-- Tarjeta 1: Más Leído -->
        <div class="disco-card">
          <div>
            <div class="disco-header">
              <span class="disco-tag tag-pop">🔥 Más Leído</span>
              <span style="font-size: 0.72rem; color: var(--text-light); font-family: var(--font-mono);">Popular</span>
            </div>
            <h3 class="disco-title">DAFO Cuantitativo y Matriz CAME: Decisión C-Level</h3>
            <p class="disco-desc">
              Ponderación matricial de fortalezas y debilidades para erradicar la subjetividad en planes directores.
            </p>
          </div>
          <a href="/es/posts/dafo-cuantitativo-matriz-came/" class="disco-link">Leer artículo →</a>
        </div>

        <!-- Tarjeta 2: Último Post -->
        <div class="disco-card">
          <div>
            <div class="disco-header">
              <span class="disco-tag tag-lat">⚡ Última Publicación</span>
              <span style="font-size: 0.72rem; color: var(--text-light); font-family: var(--font-mono);">Reciente</span>
            </div>
            <h3 class="disco-title">SDD vs. Vibe Coding: Desarrollo Robusto en 2026</h3>
            <p class="disco-desc">
              Por qué el código improvisado por LLMs colapsa y cómo las especificaciones formales aseguran software en producción.
            </p>
          </div>
          <a href="/es/posts/sdd_vs_vibe_coding/" class="disco-link">Leer artículo →</a>
        </div>

        <!-- Tarjeta 3: Post Aleatorio -->
        <div class="disco-card" style="background: var(--bg-subtle);">
          <div>
            <div class="disco-header">
              <span class="disco-tag tag-rnd">🎲 Post Aleatorio</span>
              <button class="btn-reroll" id="btnReroll" title="Elegir otro artículo">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
                Barajar
              </button>
            </div>
            <h3 class="disco-title" id="rndTitle">GraphRAG: Por Qué los Vectores No Bastan</h3>
            <p class="disco-desc" id="rndDesc">
              Los límites del RAG semántico y cómo los grafos de conocimiento resuelven relaciones complejas en producción.
            </p>
          </div>
          <a href="/es/posts/graphrag/" class="disco-link" id="rndLink">Leer este post →</a>
        </div>

      </div>
    </section>

  </main>

  <!-- =======================================================================
       FOOTER
       ======================================================================= -->
  <footer class="site-footer">
    <div class="container footer-inner">
      <div>
        <strong>Datalaria</strong> · © 2026 Daniel Aláez
      </div>
      <ul class="footer-nav">
        <li><a href="#blog">Blog</a></li>
        <li><a href="#recursos">Recursos</a></li>
        <li><a href="#apps">Apps</a></li>
        <li><a href="/es/sobre-mi/">Sobre mí</a></li>
        <li><a href="/es/contact/">Contacto</a></li>
      </ul>
    </div>
  </footer>

  <!-- =======================================================================
       INTERACTIVIDAD EN VIVO (JavaScript Ligero)
       ======================================================================= -->
  <script>
    const postsData = {json_posts_str};

    const categories = {{
      tecnicos: postsData.filter(p => p.category === 'tecnicos'),
      proyectos: postsData.filter(p => p.category === 'proyectos'),
      startups: postsData.filter(p => p.category === 'startups'),
      biografias: postsData.filter(p => p.category === 'biografias')
    }};

    // 1. Conmutador de Tema Claro / Oscuro
    const htmlElem = document.documentElement;
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeLabel = document.getElementById('themeLabel');
    const themeIcon = document.getElementById('themeIcon');

    function applyTheme(theme) {{
      htmlElem.setAttribute('data-theme', theme);
      localStorage.setItem('datalaria-minimal-theme', theme);
      if (theme === 'dark') {{
        themeLabel.textContent = 'Modo Claro';
        themeIcon.innerHTML = '<path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>';
      }} else {{
        themeLabel.textContent = 'Modo Oscuro';
        themeIcon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
      }}
    }}

    themeBtn.addEventListener('click', () => {{
      const current = htmlElem.getAttribute('data-theme') || 'light';
      applyTheme(current === 'light' ? 'dark' : 'light');
    }});

    // Preferencia inicial
    const userPref = localStorage.getItem('datalaria-minimal-theme') || 'light';
    applyTheme(userPref);

    // 2. Selector de Categorías (Renderizado Limpio de Artículos)
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

    // Iniciar con Artículos Técnicos
    selectCat('tecnicos');

    // 3. Post Aleatorio Interactivo
    const btnReroll = document.getElementById('btnReroll');
    const rndTitle = document.getElementById('rndTitle');
    const rndDesc = document.getElementById('rndDesc');
    const rndLink = document.getElementById('rndLink');

    function rerollRandom() {{
      const idx = Math.floor(Math.random() * postsData.length);
      const post = postsData[idx];

      rndTitle.style.opacity = '0';
      rndDesc.style.opacity = '0';

      setTimeout(() => {{
        rndTitle.textContent = post.title;
        rndDesc.textContent = post.desc || "Haz clic para acceder directamente a este artículo del archivo de Datalaria.";
        rndLink.href = post.url;
        rndTitle.style.opacity = '1';
        rndDesc.style.opacity = '1';
      }}, 120);
    }}

    btnReroll.addEventListener('click', rerollRandom);
  </script>
</body>
</html>
"""

with open('mockup_homepage_v2.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Created mockup_homepage_v2.html successfully!")
