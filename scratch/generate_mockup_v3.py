import json

with open('scratch/posts_for_mockup.json', 'r', encoding='utf-8') as f:
    all_posts = json.load(f)

json_posts_str = json.dumps(all_posts, ensure_ascii=False)

html_code = f"""<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datalaria | Mockup Minimalista v3</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* ==========================================================================
       SISTEMA DE DISEÑO MINIMALISTA v3 (Inspirado en hugo-bootstrap-theme & PaperMod)
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
       HEADER & NAVBAR
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
      width: 26px;
      height: 26px;
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
       MASTHEAD CENTRAL MINIMALISTA (Ajustes v3)
       - Sin "Datalaria" en texto (solo el logo)
       - Texto breve y conciso
       - Sin "Este es mi kilómetro 0."
       - Redes sociales movidas al final
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
       Ubicada justo después del masthead y antes de Recursos
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
       SECCIÓN 02: CONTENIDOS (Subida inmediatamente después de Recursos)
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
       SECCIÓN 03: APLICACIONES & EXPERIMENTOS (Bajada al apartado 03)
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
       SECCIÓN SOCIAL INFERIOR (Accesible tras visualizar los contenidos)
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
       FOOTER
       ========================================================================== */
    footer.site-footer {{
      padding: 30px 0 35px 0;
      font-size: 0.8rem;
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
      <span class="mockup-pill">Fase 0 • Mockup v3</span>
      &nbsp; <span>Minimalismo depurado: Masthead conciso + Brújula compacta + Reordenación de secciones</span>
    </div>
    <div style="font-family: var(--font-mono); font-size: 0.72rem;">
      98 Artículos · 6 Apps · Hub Recursos
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
         MASTHEAD CENTRAL MINIMALISTA (v3)
         - Logo centrado
         - Texto de entrada minimizado
         - Sin título repetido "Datalaria"
         - Sin "Este es mi kilómetro 0."
         - Redes sociales desplazadas al final
         ======================================================================= -->
    <section class="masthead-v3">
      <img src="static/images/datalaria_logo_transp.png" alt="Datalaria" class="masthead-v3-logo" onerror="this.src='/images/datalaria_logo_transp.png';">
      <p class="masthead-v3-tagline">
        Un portal para el aprendizaje en los datos, la inteligencia artificial, la tecnología y la gestión empresarial.
      </p>
    </section>

    <!-- =======================================================================
         BRÚJULA DEL DESCUBRIMIENTO (COMPACTA Y DE BAJA ALTURA)
         Ubicada antes del primer apartado de Recursos
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
              <span class="disco-pill-tag tag-pop">🔥 Más Leído</span>
              <span class="disco-item-title">DAFO Cuantitativo & CAME</span>
            </div>
            <span style="font-size: 0.75rem; color: var(--accent); font-weight: 600;">→</span>
          </a>

          <!-- 2. Último Post -->
          <a href="/es/posts/sdd_vs_vibe_coding/" class="disco-item" title="SDD vs. Vibe Coding con IA en 2026">
            <div class="disco-badge-title">
              <span class="disco-pill-tag tag-lat">⚡ Última Publicación</span>
              <span class="disco-item-title">SDD vs. Vibe Coding</span>
            </div>
            <span style="font-size: 0.75rem; color: var(--accent); font-weight: 600;">→</span>
          </a>

          <!-- 3. Post Aleatorio Interactivo -->
          <div class="disco-item" style="cursor: default;">
            <div class="disco-badge-title" style="flex-grow: 1;">
              <span class="disco-pill-tag tag-rnd">🎲 Aleatorio</span>
              <a href="/es/posts/graphrag/" id="rndMiniLink" class="disco-item-title" style="text-decoration: none; color: inherit; display: block;">
                <span id="rndMiniTitle">GraphRAG: Vectores y Grafos</span>
              </a>
            </div>
            <button class="btn-shuffle-mini" id="btnMiniReroll" title="Generar otro post al azar">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
              Barajar
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
        <h2 class="section-title">Recursos & Packs Profesionales</h2>
        <p class="section-desc">
          Modelos cuantitativos, plantillas de decisión y guías metodológicas diseñadas para el ámbito profesional, comités directivos y control corporativo.
        </p>
      </div>

      <div class="recursos-lead-box">
        <div class="recursos-top-row">
          <div class="recursos-lead-title">
            <span>⚡ Executive Decision Packs</span>
            <span class="recursos-lead-badge">Estreno Inminente</span>
          </div>
          <span style="font-size: 0.78rem; color: var(--text-light); font-family: var(--font-mono);">Del cálculo cuantitativo a la aprobación de Comité</span>
        </div>
        <p class="recursos-lead-desc">
          Herramientas para defender decisiones estratégicas ante juntas y comités: modelos en Excel protegidos con fórmulas matriciales, diapositivas PowerPoint 16:9 con Pirámide de Minto y guías metodológicas en PDF.
        </p>

        <!-- Muestrario de los Recursos -->
        <div class="recursos-items-grid">
          
          <div class="recurso-card-item">
            <div>
              <div class="recurso-item-icon">🎯</div>
              <div class="recurso-item-name">DAFO Cuantitativo & CAME</div>
              <div class="recurso-item-detail">Ponderación numérica de factores, matriz CAME automática y slide ejecutiva de junta.</div>
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
          <a href="/es/recursos/" class="link-more">Ver catálogo completo de Recursos →</a>
        </div>
      </div>
    </section>

    <!-- =======================================================================
         02 / CONTENIDOS (Subida inmediatamente después de Recursos)
         ======================================================================= -->
    <section class="section-block" id="blog">
      <div class="section-heading">
        <span class="section-tag">02 / Contenidos</span>
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
         03 / APLICACIONES & EXPERIMENTOS (Bajada al apartado 03)
         ======================================================================= -->
    <section class="section-block" id="apps">
      <div class="section-heading">
        <span class="section-tag">03 / Ecosistema</span>
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
              <p class="app-box-desc">Dashboard ejecutivo impulsado por agentes IA para mitigar el riesgo en la cadena de suministro industrial.</p>
            </div>
          </div>
          <span class="app-box-arrow">Abrir dashboard →</span>
        </a>

        <!-- App: Neon Snake (JUEGO INTEGRADO EN APPS) -->
        <a href="/games/snake/" class="app-box" target="_blank">
          <div class="app-box-top">
            <span class="app-box-icon">🐍</span>
            <div>
              <div class="app-box-name">
                Neon Snake Cyberpunk
                <span class="app-box-badge badge-arcade">Arcade / Juego</span>
              </div>
              <p class="app-box-desc">Versión arcade del clásico Snake con estética cyberpunk y ranking global en tiempo real con Supabase.</p>
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
              <p class="app-box-desc">Consulta meteorológica en tiempo real enriquecida con modelos predictivos de Machine Learning.</p>
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
              <p class="app-box-desc">Navaja suiza rápida y ligera para transformar unidades de medida, magnitud e ingeniería.</p>
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
              <p class="app-box-desc">Aplicación interactiva para memorizar conceptos técnicos usando repetición espaciada y gamificación.</p>
            </div>
          </div>
          <span class="app-box-arrow">Abrir app →</span>
        </a>

      </div>
    </section>

    <!-- =======================================================================
         REDES SOCIALES INFERIORES (Accesibles tras visualizar los contenidos)
         ======================================================================= -->
    <section class="social-bottom-section">
      <div class="social-bottom-label">
        Conéctate y sigue las novedades de Datalaria:
      </div>
      <div class="social-bottom-links">
        <a href="https://github.com/Dalaez" class="social-chip" target="_blank" rel="noopener">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
          <span>GitHub</span>
        </a>

        <a href="https://www.linkedin.com/company/110125695/" class="social-chip" target="_blank" rel="noopener">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
          <span>LinkedIn</span>
        </a>

        <a href="https://x.com/datalaria" class="social-chip" target="_blank" rel="noopener">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path></svg>
          <span>Twitter / X</span>
        </a>
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
       INTERACTIVIDAD EN VIVO (JavaScript)
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

    const userPref = localStorage.getItem('datalaria-minimal-theme') || 'light';
    applyTheme(userPref);

    // 2. Selector de Categorías (02 Contenidos)
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

    // 3. Post Aleatorio en la Brújula Compacta
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
  </script>
</body>
</html>
"""

with open('mockup_homepage_v3.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Created mockup_homepage_v3.html successfully!")
