import json

with open('scratch/categorized_posts.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

with open('scratch/posts_for_mockup.json', 'r', encoding='utf-8') as f:
    all_posts = json.load(f)

json_posts_str = json.dumps(all_posts, ensure_ascii=False)

html_code = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datalaria | Mockup Conceptual - Nueva Página de Inicio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* ==========================================================================
       VARIABLES DE COLOR Y DISEÑO (PaperMod + Extended Datalaria Design System)
       ========================================================================== */
    :root {{
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      
      /* Light Theme */
      --theme: #ffffff;
      --entry: #f8fafc;
      --entry-hover: #f1f5f9;
      --border: #e2e8f0;
      --border-accent: #cbd5e1;
      --primary: #0f172a;
      --secondary: #475569;
      --tertiary: #94a3b8;
      --text-muted: #64748b;
      --accent: #2563eb;
      --accent-hover: #1d4ed8;
      --accent-subtle: rgba(37, 99, 235, 0.08);
      --accent-border: rgba(37, 99, 235, 0.2);
      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
      --card-shadow-hover: 0 12px 28px -4px rgba(0, 0, 0, 0.1);
      --glow: rgba(37, 99, 235, 0.15);
      --badge-new: #10b981;
      --badge-new-bg: rgba(16, 185, 129, 0.1);
      --recursos-gradient: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
    }}

    [data-theme="dark"] {{
      /* Dark Theme */
      --theme: #0f172a;
      --entry: #1e293b;
      --entry-hover: #24344d;
      --border: #334155;
      --border-accent: #475569;
      --primary: #f8fafc;
      --secondary: #cbd5e1;
      --tertiary: #64748b;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-hover: #0ea5e9;
      --accent-subtle: rgba(56, 189, 248, 0.1);
      --accent-border: rgba(56, 189, 248, 0.25);
      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
      --card-shadow-hover: 0 12px 30px -4px rgba(0, 0, 0, 0.45);
      --glow: rgba(56, 189, 248, 0.18);
      --badge-new: #34d399;
      --badge-new-bg: rgba(52, 211, 153, 0.15);
      --recursos-gradient: linear-gradient(135deg, #1e1b4b 0%, #1e3a8a 50%, #0f766e 100%);
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: var(--font-sans);
      background-color: var(--theme);
      color: var(--primary);
      line-height: 1.6;
      transition: background-color 0.3s ease, color 0.3s ease;
      overflow-x: hidden;
      padding-top: 40px; /* Space for the top mockup banner */
    }}

    /* ==========================================================================
       BARRA FLOTANTE DE VALIDACIÓN DE MOCKUP
       ========================================================================== */
    .mockup-status-bar {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background: linear-gradient(90deg, #1e293b, #0f172a);
      color: #94a3b8;
      font-size: 0.78rem;
      padding: 8px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 1000;
      border-bottom: 1px solid #334155;
      letter-spacing: 0.02em;
    }}
    .mockup-status-bar strong {{
      color: #38bdf8;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .mockup-tag {{
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 600;
      font-size: 0.72rem;
    }}

    /* ==========================================================================
       CONTAINER & HEADER
       ========================================================================== */
    .container {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    header.site-header {{
      position: sticky;
      top: 40px;
      z-index: 900;
      background: var(--theme);
      background: rgba(var(--theme), 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 16px 0;
      transition: all 0.3s ease;
    }}

    .header-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .brand-logo {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--primary);
    }}

    .logo-img {{
      width: 36px;
      height: 36px;
      object-fit: contain;
      border-radius: 8px;
    }}

    .brand-name {{
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    nav.main-nav {{
      display: flex;
      align-items: center;
      gap: 20px;
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      list-style: none;
      gap: 6px;
    }}

    .nav-link {{
      text-decoration: none;
      color: var(--secondary);
      font-size: 0.92rem;
      font-weight: 500;
      padding: 8px 14px;
      border-radius: 8px;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .nav-link:hover {{
      color: var(--primary);
      background: var(--entry-hover);
    }}

    .nav-link.active {{
      color: var(--primary);
      background: var(--entry);
      font-weight: 600;
    }}

    /* Destacado RECURSOS en el navbar */
    .nav-link-recursos {{
      color: #3b82f6 !important;
      background: rgba(59, 130, 246, 0.08);
      border: 1px solid rgba(59, 130, 246, 0.25);
      font-weight: 600;
      position: relative;
    }}
    .nav-link-recursos:hover {{
      background: rgba(59, 130, 246, 0.16);
      transform: translateY(-1px);
    }}
    [data-theme="dark"] .nav-link-recursos {{
      color: #60a5fa !important;
      background: rgba(96, 165, 250, 0.12);
      border: 1px solid rgba(96, 165, 250, 0.3);
    }}

    .nav-badge {{
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 999px;
      background: #ef4444;
      color: white;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .theme-toggle {{
      background: var(--entry);
      border: 1px solid var(--border);
      color: var(--primary);
      cursor: pointer;
      padding: 8px 12px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }}
    .theme-toggle:hover {{
      background: var(--entry-hover);
      border-color: var(--border-accent);
    }}

    /* ==========================================================================
       HERO PORTAL SECTION
       ========================================================================== */
    .hero-section {{
      padding: 60px 0 35px 0;
      text-align: center;
      position: relative;
    }}

    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      background: var(--accent-subtle);
      border: 1px solid var(--accent-border);
      color: var(--accent);
      font-size: 0.82rem;
      font-weight: 600;
      margin-bottom: 24px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}

    .hero-title {{
      font-size: 3.2rem;
      font-weight: 800;
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 20px;
      max-width: 860px;
      margin-left: auto;
      margin-right: auto;
    }}

    .hero-title span.gradient-text {{
      background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
      font-size: 1.18rem;
      color: var(--secondary);
      max-width: 720px;
      margin: 0 auto 32px auto;
      line-height: 1.6;
    }}

    .hero-metrics {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 32px;
      margin-bottom: 36px;
      flex-wrap: wrap;
    }}

    .metric-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .metric-number {{
      font-size: 1.7rem;
      font-weight: 800;
      font-family: var(--font-mono);
      color: var(--primary);
    }}
    .metric-label {{
      font-size: 0.78rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
    }}

    .hero-cta-group {{
      display: flex;
      justify-content: center;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px 24px;
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
    }}

    .btn-primary {{
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: white;
      border: 1px solid transparent;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    }}
    .btn-primary:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45);
    }}

    .btn-secondary {{
      background: var(--entry);
      color: var(--primary);
      border: 1px solid var(--border);
    }}
    .btn-secondary:hover {{
      background: var(--entry-hover);
      border-color: var(--border-accent);
      transform: translateY(-2px);
    }}

    /* ==========================================================================
       SHOWCASE MONETIZACIÓN: RECURSOS C-LEVEL (EL IMÁN PRINCIPAL)
       ========================================================================== */
    .recursos-banner-section {{
      margin: 40px 0 60px 0;
    }}

    .recursos-card {{
      background: var(--entry);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 36px;
      position: relative;
      overflow: hidden;
      box-shadow: var(--card-shadow);
      transition: all 0.3s ease;
    }}

    .recursos-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 5px;
      background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
    }}

    .recursos-card-grid {{
      display: grid;
      grid-template-columns: 1.25fr 0.95fr;
      gap: 36px;
      align-items: center;
    }}

    @media (max-width: 900px) {{
      .recursos-card-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .recursos-badge-row {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }}

    .pill-recursos {{
      background: rgba(59, 130, 246, 0.12);
      color: #3b82f6;
      border: 1px solid rgba(59, 130, 246, 0.3);
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    [data-theme="dark"] .pill-recursos {{
      color: #60a5fa;
      background: rgba(96, 165, 250, 0.15);
    }}

    .pill-status {{
      background: var(--badge-new-bg);
      color: var(--badge-new);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
    }}

    .recursos-title {{
      font-size: 1.95rem;
      font-weight: 800;
      line-height: 1.25;
      margin-bottom: 14px;
      color: var(--primary);
    }}

    .recursos-desc {{
      font-size: 0.98rem;
      color: var(--secondary);
      line-height: 1.6;
      margin-bottom: 24px;
    }}

    .recursos-features-list {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 28px;
    }}

    @media (max-width: 600px) {{
      .recursos-features-list {{
        grid-template-columns: 1fr;
      }}
    }}

    .feature-item {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.88rem;
      color: var(--secondary);
    }}
    .feature-icon {{
      font-size: 1.1rem;
    }}

    .recursos-actions {{
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }}

    .btn-recursos {{
      background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
      color: white;
      font-weight: 700;
      border: none;
      padding: 12px 24px;
      border-radius: 10px;
      text-decoration: none;
      box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35);
      transition: all 0.2s ease;
    }}
    .btn-recursos:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
    }}

    /* Preview visual interactivo del Pack */
    .pack-visual-preview {{
      background: var(--theme);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
      position: relative;
    }}

    .pack-preview-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
      padding-bottom: 14px;
      margin-bottom: 16px;
    }}

    .pack-suite-title {{
      font-size: 0.78rem;
      font-weight: 700;
      color: #3b82f6;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}

    .pack-price-tag {{
      display: flex;
      align-items: baseline;
      gap: 6px;
    }}
    .price-now {{
      font-size: 1.35rem;
      font-weight: 800;
      font-family: var(--font-mono);
      color: var(--primary);
    }}
    .price-old {{
      font-size: 0.85rem;
      color: var(--text-muted);
      text-decoration: line-through;
    }}

    .pack-preview-name {{
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 12px;
      color: var(--primary);
    }}

    .pack-components {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 20px;
    }}

    .comp-pill {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 12px;
      border-radius: 8px;
      background: var(--entry);
      border: 1px solid var(--border);
      font-size: 0.82rem;
      color: var(--secondary);
    }}

    .comp-icon {{
      font-size: 1rem;
    }}

    .pack-preview-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 14px;
      border-top: 1px solid var(--border);
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    /* ==========================================================================
       TRINIDAD DE DESCUBRIMIENTO (MÁS LEÍDO / ÚLTIMO / POST ALEATORIO)
       ========================================================================== */
    .discovery-section {{
      margin: 50px 0;
    }}

    .section-header {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
    }}

    .section-title {{
      font-size: 1.45rem;
      font-weight: 800;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .section-subtext {{
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    .discovery-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }}

    @media (max-width: 960px) {{
      .discovery-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .discovery-card {{
      background: var(--entry);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.3s ease;
      position: relative;
    }}
    .discovery-card:hover {{
      transform: translateY(-4px);
      box-shadow: var(--card-shadow-hover);
      border-color: var(--border-accent);
    }}

    .card-label-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .card-label {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 3px 8px;
      border-radius: 6px;
    }}

    .label-popular {{
      background: rgba(239, 68, 68, 0.12);
      color: #ef4444;
      border: 1px solid rgba(239, 68, 68, 0.25);
    }}

    .label-latest {{
      background: rgba(16, 185, 129, 0.12);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.25);
    }}

    .label-random {{
      background: rgba(168, 85, 247, 0.12);
      color: #a855f7;
      border: 1px solid rgba(168, 85, 247, 0.25);
    }}

    .post-date {{
      font-size: 0.75rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    .discovery-card-title {{
      font-size: 1.08rem;
      font-weight: 700;
      line-height: 1.35;
      margin-bottom: 10px;
      color: var(--primary);
    }}

    .discovery-card-desc {{
      font-size: 0.85rem;
      color: var(--secondary);
      line-height: 1.5;
      margin-bottom: 18px;
      flex-grow: 1;
    }}

    .discovery-card-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--accent);
      text-decoration: none;
      transition: gap 0.2s;
    }}
    .discovery-card-link:hover {{
      gap: 10px;
    }}

    /* Estilo especial para la tarjeta interactiva de Post Aleatorio */
    .random-card {{
      background: linear-gradient(180deg, var(--entry) 0%, rgba(168, 85, 247, 0.05) 100%);
      border: 1px solid rgba(168, 85, 247, 0.3);
    }}

    .btn-shuffle {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--primary);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }}
    .btn-shuffle:hover {{
      background: var(--entry-hover);
      border-color: #a855f7;
      color: #a855f7;
    }}

    /* ==========================================================================
       HUB DE LAS 4 CATEGORÍAS TEMÁTICAS
       ========================================================================== */
    .categories-section {{
      margin: 60px 0;
    }}

    .categories-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-bottom: 30px;
    }}

    @media (max-width: 960px) {{
      .categories-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}
    @media (max-width: 540px) {{
      .categories-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .category-card {{
      background: var(--entry);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 22px;
      cursor: pointer;
      transition: all 0.25s ease;
      position: relative;
      display: flex;
      flex-direction: column;
    }}

    .category-card:hover, .category-card.active {{
      border-color: var(--accent);
      transform: translateY(-3px);
      box-shadow: 0 8px 24px -4px var(--glow);
    }}

    .category-card.active {{
      background: var(--entry-hover);
      border-width: 2px;
    }}

    .category-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
    }}

    .category-icon {{
      font-size: 1.8rem;
    }}

    .category-count {{
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
      background: var(--theme);
      border: 1px solid var(--border);
      padding: 3px 8px;
      border-radius: 999px;
      color: var(--text-muted);
    }}

    .category-title {{
      font-size: 1.05rem;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--primary);
    }}

    .category-desc {{
      font-size: 0.8rem;
      color: var(--secondary);
      line-height: 1.45;
      margin-bottom: 14px;
      flex-grow: 1;
    }}

    .category-action {{
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--accent);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    /* Preview de artículos filtrados por categoría */
    .category-preview-box {{
      background: var(--entry);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      margin-top: 20px;
    }}

    .preview-box-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border);
    }}

    .preview-box-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--primary);
    }}

    .preview-posts-list {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
    }}

    @media (max-width: 768px) {{
      .preview-posts-list {{
        grid-template-columns: 1fr;
      }}
    }}

    .preview-post-item {{
      background: var(--theme);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .preview-post-item:hover {{
      border-color: var(--accent);
      transform: translateX(3px);
    }}

    .preview-post-title {{
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--primary);
      margin-bottom: 6px;
      line-height: 1.35;
    }}

    .preview-post-meta {{
      font-size: 0.72rem;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    /* ==========================================================================
       ECOSISTEMA DE APPS & JUEGOS (INTEGRACIÓN)
       ========================================================================== */
    .apps-section {{
      margin: 60px 0;
    }}

    .apps-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }}

    @media (max-width: 900px) {{
      .apps-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}
    @media (max-width: 600px) {{
      .apps-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .app-card-item {{
      background: var(--entry);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.3s ease;
      position: relative;
    }}
    .app-card-item:hover {{
      transform: translateY(-4px);
      box-shadow: var(--card-shadow-hover);
      border-color: var(--border-accent);
    }}

    .app-icon-badge {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }}

    .app-badge-type {{
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .badge-interactive {{
      background: rgba(59, 130, 246, 0.1);
      color: #3b82f6;
    }}
    .badge-arcade {{
      background: rgba(236, 72, 153, 0.1);
      color: #ec4899;
    }}

    .app-title-card {{
      font-size: 1.12rem;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--primary);
    }}

    .app-desc-card {{
      font-size: 0.84rem;
      color: var(--secondary);
      line-height: 1.45;
      margin-bottom: 18px;
    }}

    .app-btn-open {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 8px 14px;
      background: var(--theme);
      border: 1px solid var(--border);
      color: var(--primary);
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .app-btn-open:hover {{
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }}

    /* ==========================================================================
       FOOTER
       ========================================================================== */
    footer.site-footer {{
      border-top: 1px solid var(--border);
      padding: 50px 0 30px 0;
      margin-top: 80px;
      background: var(--entry);
    }}

    .footer-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr 1fr 1fr;
      gap: 40px;
      margin-bottom: 40px;
    }}

    @media (max-width: 768px) {{
      .footer-grid {{
        grid-template-columns: 1fr;
        gap: 28px;
      }}
    }}

    .footer-brand p {{
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 10px;
      max-width: 320px;
    }}

    .footer-col h4 {{
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--primary);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 14px;
    }}

    .footer-links {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .footer-links a {{
      text-decoration: none;
      color: var(--secondary);
      font-size: 0.84rem;
      transition: color 0.2s;
    }}
    .footer-links a:hover {{
      color: var(--accent);
    }}

    .footer-bottom {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border);
      padding-top: 24px;
      font-size: 0.78rem;
      color: var(--text-muted);
      flex-wrap: wrap;
      gap: 12px;
    }}

    .social-links {{
      display: flex;
      gap: 14px;
    }}
    .social-link {{
      color: var(--secondary);
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .social-link:hover {{
      color: var(--primary);
    }}
  </style>
</head>
<body>

  <!-- BARRA DE ESTADO DEL MOCKUP -->
  <div class="mockup-status-bar">
    <div>
      <strong>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        MOCKUP DE VALIDACIÓN ESTRATÉGICA
      </strong>
      &nbsp;|&nbsp; <span>Propuesta de transformación de Datalaria a Portal Tecnológico & Tienda de Recursos</span>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
      <span class="mockup-tag">Modo Interactivo</span>
      <span style="font-size: 0.75rem;">Total artículos catalogados: <strong>98</strong></span>
    </div>
  </div>

  <!-- HEADER PRINCIPAL -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="#" class="brand-logo">
        <img src="static/images/datalaria_logo_transp.png" alt="Datalaria Logo" class="logo-img" onerror="this.src='/images/datalaria_logo_transp.png';">
        <span class="brand-name">Datalaria</span>
      </a>

      <nav class="main-nav">
        <ul class="nav-links">
          <li><a href="#blog" class="nav-link active">Blog</a></li>
          <li>
            <a href="#recursos" class="nav-link nav-link-recursos">
              <span>Recursos</span>
              <span class="nav-badge">Pro</span>
            </a>
          </li>
          <li><a href="#apps" class="nav-link">Apps & Juegos</a></li>
          <li><a href="#sobre-mi" class="nav-link">Sobre mí</a></li>
          <li><a href="#contacto" class="nav-link">Contacto</a></li>
        </ul>

        <button class="theme-toggle" id="themeToggleBtn" title="Cambiar tema Claro / Oscuro">
          <svg id="themeIcon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>
      </nav>
    </div>
  </header>

  <main class="container">

    <!-- =======================================================================
         1. HERO SECTION: PORTAL & AUTORIDAD
         ======================================================================= -->
    <section class="hero-section">
      <div class="hero-badge">
        <span>⚡ De Bitácora a Ecosistema Digital</span>
      </div>
      <h1 class="hero-title">
        Ingeniería de Software, Inteligencia Artificial y <span class="gradient-text">Modelos de Decisión</span>
      </h1>
      <p class="hero-subtitle">
        El portal independiente donde convergen el rigor cuantitativo, la arquitectura de agentes inteligentes y herramientas prácticas para líderes tecnológicos y comités de dirección.
      </p>

      <div class="hero-metrics">
        <div class="metric-item">
          <span class="metric-number">98</span>
          <span class="metric-label">Artículos Técnicos</span>
        </div>
        <div class="metric-item">
          <span class="metric-number">4</span>
          <span class="metric-label">Grandes Temáticas</span>
        </div>
        <div class="metric-item">
          <span class="metric-number">6</span>
          <span class="metric-label">Apps Interactivas</span>
        </div>
        <div class="metric-item">
          <span class="metric-number">12+</span>
          <span class="metric-label">Packs Ejecutivos</span>
        </div>
      </div>

      <div class="hero-cta-group">
        <a href="#recursos" class="btn btn-primary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          Explorar Packs de Recursos
        </a>
        <a href="#categorias" class="btn btn-secondary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          Explorar por Categorías
        </a>
      </div>
    </section>

    <!-- =======================================================================
         2. SHOWCASE DESTACADO: RECURSOS EJECUTIVOS (MONETIZACIÓN C-LEVEL)
         ======================================================================= -->
    <section class="recursos-banner-section" id="recursos">
      <div class="recursos-card">
        <div class="recursos-card-grid">
          
          <div>
            <div class="recursos-badge-row">
              <span class="pill-recursos">💎 Nueva Sección Profesional</span>
              <span class="pill-status">Lanzamiento Inminente</span>
            </div>

            <h2 class="recursos-title">Executive Decision Packs</h2>
            <p class="recursos-desc">
              Del cálculo cuantitativo a la aprobación del Comité de Dirección. Modelos matriciales en Excel sin macros, diapositivas ejecutivas PowerPoint 16:9 diseñadas con la Pirámide de Minto y guías metodológicas para defender decisiones críticas.
            </p>

            <div class="recursos-features-list">
              <div class="feature-item">
                <span class="feature-icon">📊</span>
                <span><strong>Motor en Excel:</strong> Fórmulas matriciales protegidas</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">📑</span>
                <span><strong>Deck C-Level:</strong> PPTX 16:9 con Action Titles</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">📄</span>
                <span><strong>Guía PDF:</strong> Fundamentos y respuestas a objeciones</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">🛡️</span>
                <span><strong>Garantía B2B:</strong> Factura deducible con IVA</span>
              </div>
            </div>

            <div class="recursos-actions">
              <a href="/es/recursos/" class="btn-recursos">
                Visitar Sección de Recursos →
              </a>
              <a href="/es/posts/dafo-cuantitativo-matriz-came/" class="btn btn-secondary" style="font-size: 0.85rem; padding: 10px 18px;">
                Ver Caso Guía DAFO
              </a>
            </div>
          </div>

          <!-- Preview de Producto Estrella -->
          <div class="pack-visual-preview">
            <div class="pack-preview-header">
              <span class="pack-suite-title">Suite 01: Estrategia MBA</span>
              <div class="pack-price-tag">
                <span class="price-now">5€</span>
                <span class="price-old">19€</span>
              </div>
            </div>

            <div class="pack-preview-name">🎯 DAFO Cuantitativo & Matriz CAME</div>

            <div class="pack-components">
              <div class="comp-pill">
                <span class="comp-icon">📐</span>
                <span>Ponderación matemática de debilidades y fortalezas</span>
              </div>
              <div class="comp-pill">
                <span class="comp-icon">⚡</span>
                <span>Matriz CAME generada automáticamente</span>
              </div>
              <div class="comp-pill">
                <span class="comp-icon">💼</span>
                <span>Slide PowerPoint lista para proyectar en junta</span>
              </div>
            </div>

            <div class="pack-preview-footer">
              <span>⭐️ Bestseller C-Level</span>
              <span style="color: #10b981; font-weight: 600;">Descarga Inmediata</span>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- =======================================================================
         3. TRINIDAD DE DESCUBRIMIENTO: MÁS LEÍDO / ÚLTIMO / RANDOM
         ======================================================================= -->
    <section class="discovery-section">
      <div class="section-header">
        <div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
            Brújula de Descubrimiento
          </h2>
          <span class="section-subtext">Optimizado para explorar rápidamente los contenidos más relevantes</span>
        </div>
      </div>

      <div class="discovery-grid">
        
        <!-- 1. Post Más Leído -->
        <div class="discovery-card">
          <div>
            <div class="card-label-row">
              <span class="card-label label-popular">🔥 Más Leído</span>
              <span class="post-date">15 min lectura</span>
            </div>
            <h3 class="discovery-card-title">
              DAFO Cuantitativo y Matriz CAME: Decisión Estratégica C-Level
            </h3>
            <p class="discovery-card-desc">
              Cómo eliminar el sesgo subjetivo de un DAFO tradicional asignando pesos matemáticos y derivando automáticamente las acciones CAME para el plan director.
            </p>
          </div>
          <a href="/es/posts/dafo-cuantitativo-matriz-came/" class="discovery-card-link">
            Leer artículo completo →
          </a>
        </div>

        <!-- 2. Último Post Publicado -->
        <div class="discovery-card">
          <div>
            <div class="card-label-row">
              <span class="card-label label-latest">⚡ Última Publicación</span>
              <span class="post-date">Reciente</span>
            </div>
            <h3 class="discovery-card-title">
              SDD (Spec-Driven Development) vs. Vibe Coding con IA
            </h3>
            <p class="discovery-card-desc">
              Por qué el código improvisado por LLMs colapsa a escala y cómo el desarrollo guiado por especificaciones formales garantiza software en producción en 2026.
            </p>
          </div>
          <a href="/es/posts/sdd_vs_vibe_coding/" class="discovery-card-link">
            Leer artículo más reciente →
          </a>
        </div>

        <!-- 3. Post Random Interactivo -->
        <div class="discovery-card random-card" id="randomCardWidget">
          <div>
            <div class="card-label-row">
              <span class="card-label label-random">🎲 Post Aleatorio</span>
              <button class="btn-shuffle" id="btnShuffle" title="Elegir otro artículo al azar">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
                Girar Dado
              </button>
            </div>
            <h3 class="discovery-card-title" id="randomTitle">
              GraphRAG: Por Qué los Vectores No Bastan y Tu IA Necesita un Grafo
            </h3>
            <p class="discovery-card-desc" id="randomDesc">
              Los límites del RAG semántico tradicional y cómo las estructuras de grafos de conocimiento resuelven las relaciones complejas y evitan alucinaciones.
            </p>
          </div>
          <a href="/es/posts/graphrag/" class="discovery-card-link" id="randomLink">
            Descubrir este post →
          </a>
        </div>

      </div>
    </section>

    <!-- =======================================================================
         4. EXPLORADOR POR LAS 4 CATEGORÍAS TEMÁTICAS
         ======================================================================= -->
    <section class="categories-section" id="categorias">
      <div class="section-header">
        <div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            Explora los 98 Artículos en 4 Temáticas
          </h2>
          <span class="section-subtext">Selecciona una categoría para ver sus artículos destacados</span>
        </div>
      </div>

      <div class="categories-grid">
        
        <!-- Categoría 1: Artículos Técnicos -->
        <div class="category-card active" data-category="tecnicos" onclick="switchCategory('tecnicos')">
          <div class="category-header">
            <span class="category-icon">🧠</span>
            <span class="category-count">41 posts</span>
          </div>
          <h3 class="category-title">Artículos Técnicos & Gestión</h3>
          <p class="category-desc">
            Modelos de decisión estratégica C-Level (Porter, BCG, PESTEL, RICE), arquitectura de IA (RAG, MLOps, MCP, pgvector) y ensayos de sistemas.
          </p>
          <span class="category-action">Explorar categoría →</span>
        </div>

        <!-- Categoría 2: Proyectos Tecnológicos -->
        <div class="category-card" data-category="proyectos" onclick="switchCategory('proyectos')">
          <div class="category-header">
            <span class="category-icon">🛠️</span>
            <span class="category-count">34 posts</span>
          </div>
          <h3 class="category-title">Proyectos Tecnológicos</h3>
          <p class="category-desc">
            Series completas construidas paso a paso: Proyecto LifeOps, Autopilot Agéntico, Radar de Obsolescencia y Weather Service.
          </p>
          <span class="category-action">Explorar categoría →</span>
        </div>

        <!-- Categoría 3: Startups -->
        <div class="category-card" data-category="startups" onclick="switchCategory('startups')">
          <div class="category-header">
            <span class="category-icon">🚀</span>
            <span class="category-count">12 posts</span>
          </div>
          <h3 class="category-title">Startups & Scaleups</h3>
          <p class="category-desc">
            Análisis a fondo de la ingeniería y modelo de negocio de referentes como Freepik, Wallapop, Devo, Carto, Submer o Clarity AI.
          </p>
          <span class="category-action">Explorar categoría →</span>
        </div>

        <!-- Categoría 4: Biografías -->
        <div class="category-card" data-category="biografias" onclick="switchCategory('biografias')">
          <div class="category-header">
            <span class="category-icon">🏛️</span>
            <span class="category-count">11 posts</span>
          </div>
          <h3 class="category-title">Biografías de Pioneros</h3>
          <p class="category-desc">
            Vidas y contribuciones de quienes cimentaron la informática y la estadística: Turing, Lovelace, Shannon, Bayes, Deming o von Neumann.
          </p>
          <span class="category-action">Explorar categoría →</span>
        </div>

      </div>

      <!-- Preview Dinámico de Artículos de la Categoría Seleccionada -->
      <div class="category-preview-box" id="categoryPreviewBox">
        <div class="preview-box-header">
          <span class="preview-box-title" id="catPreviewTitle">Artículos destacados en: Artículos Técnicos & Gestión</span>
          <a href="/es/posts/" id="catPreviewLink" style="font-size: 0.82rem; color: var(--accent); text-decoration: none; font-weight: 600;">Ver todos los artículos de esta categoría →</a>
        </div>
        <div class="preview-posts-list" id="catPreviewList">
          <!-- Renderizado dinámico vía JavaScript -->
        </div>
      </div>
    </section>

    <!-- =======================================================================
         5. ECOSISTEMA DE APPS & JUEGOS (INTEGRACIÓN)
         ======================================================================= -->
    <section class="apps-section" id="apps">
      <div class="section-header">
        <div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            Ecosistema de Aplicaciones & Experimentos
          </h2>
          <span class="section-subtext">Herramientas interactivas en vivo y laboratorio arcade desarrollados en Datalaria</span>
        </div>
        <a href="/es/apps/" style="font-size: 0.85rem; color: var(--accent); text-decoration: none; font-weight: 600;">Ver todas las apps →</a>
      </div>

      <div class="apps-grid">
        
        <!-- App 1: LifeOps -->
        <div class="app-card-item">
          <div>
            <div class="app-icon-badge">
              <span style="font-size: 2rem;">🚀</span>
              <span class="app-badge-type badge-interactive">Sistema Operativo</span>
            </div>
            <h3 class="app-title-card">LifeOps</h3>
            <p class="app-desc-card">
              Sistema operativo integral personal y profesional con React, FastAPI, Supabase y dashboard 360° para deporte, cine y gestión Kanban.
            </p>
          </div>
          <a href="/apps/lifeops/" class="app-btn-open">Abrir Aplicación →</a>
        </div>

        <!-- App 2: Radar de Obsolescencia -->
        <div class="app-card-item">
          <div>
            <div class="app-icon-badge">
              <span style="font-size: 2rem;">📡</span>
              <span class="app-badge-type badge-interactive">Enterprise AI</span>
            </div>
            <h3 class="app-title-card">Radar de Obsolescencia</h3>
            <p class="app-desc-card">
              Dashboard ejecutivo impulsado por agentes de IA para cuantificar y mitigar riesgos en la cadena de suministro industrial.
            </p>
          </div>
          <a href="/apps/obs-management/" class="app-btn-open">Abrir Dashboard →</a>
        </div>

        <!-- App 3: Neon Snake Arcade (JUEGO INTEGRADO) -->
        <div class="app-card-item" style="border-color: rgba(236, 72, 153, 0.3);">
          <div>
            <div class="app-icon-badge">
              <span style="font-size: 2rem;">🐍</span>
              <span class="app-badge-type badge-arcade">Juego Arcade</span>
            </div>
            <h3 class="app-title-card">Neon Snake Cyberpunk</h3>
            <p class="app-desc-card">
              Versión arcade cyberpunk del mítico Snake con leaderboard global en tiempo real conectado a Supabase.
            </p>
          </div>
          <div style="display: flex; gap: 8px;">
            <a href="/games/snake/" class="app-btn-open" style="background: rgba(236, 72, 153, 0.1); color: #ec4899; border-color: rgba(236, 72, 153, 0.3); flex: 1;">Jugar →</a>
            <a href="/es/posts/game_snake/" class="app-btn-open" title="Ver cómo se construyó">Post ↗</a>
          </div>
        </div>

        <!-- App 4: El Tiempo -->
        <div class="app-card-item">
          <div>
            <div class="app-icon-badge">
              <span style="font-size: 2rem;">🌤️</span>
              <span class="app-badge-type badge-interactive">Meteorología</span>
            </div>
            <h3 class="app-title-card">El Tiempo & Predicción ML</h3>
            <p class="app-desc-card">
              Previsión en tiempo real enriquecida con regresión de Machine Learning sobre datos de OpenWeatherMap.
            </p>
          </div>
          <a href="/apps/weather/" class="app-btn-open">Abrir App →</a>
        </div>

        <!-- App 5: Conversor -->
        <div class="app-card-item">
          <div>
            <div class="app-icon-badge">
              <span style="font-size: 2rem;">🔄</span>
              <span class="app-badge-type badge-interactive">Herramienta</span>
            </div>
            <h3 class="app-title-card">Conversor de Unidades</h3>
            <p class="app-desc-card">
              Navaja suiza de conversión para ingeniería: magnitudes físicas, energía, presión y unidades informáticas.
            </p>
          </div>
          <a href="/apps/conversor/" class="app-btn-open">Abrir App →</a>
        </div>

        <!-- App 6: Flashcards -->
        <div class="app-card-item">
          <div>
            <div class="app-icon-badge">
              <span style="font-size: 2rem;">🎴</span>
              <span class="app-badge-type badge-interactive">Productividad</span>
            </div>
            <h3 class="app-title-card">Flashcards Interactivas</h3>
            <p class="app-desc-card">
              Estudio activo con repetición espaciada y gamificación para asimilar conceptos técnicos de datos e IA.
            </p>
          </div>
          <a href="/apps/flashcards/" class="app-btn-open">Abrir App →</a>
        </div>

      </div>
    </section>

  </main>

  <!-- =======================================================================
       FOOTER
       ======================================================================= -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <div style="display: flex; align-items: center; gap: 10px;">
            <img src="static/images/datalaria_logo_transp.png" alt="Datalaria" style="width: 28px; height: 28px;" onerror="this.src='/images/datalaria_logo_transp.png';">
            <strong style="font-size: 1.15rem; color: var(--primary);">Datalaria</strong>
          </div>
          <p>
            Plataforma de divulgación técnica, modelos de decisión cuantitativos para comités de dirección y herramientas de ingeniería de software.
          </p>
        </div>

        <div class="footer-col">
          <h4>Secciones</h4>
          <ul class="footer-links">
            <li><a href="/es/posts/">Todos los Artículos (98)</a></li>
            <li><a href="/es/recursos/">Recursos & Packs C-Level</a></li>
            <li><a href="/es/apps/">Aplicaciones & Arcade</a></li>
            <li><a href="/es/tags/">Etiquetas Temáticas</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Recursos Destacados</h4>
          <ul class="footer-links">
            <li><a href="/es/posts/dafo-cuantitativo-matriz-came/">Pack DAFO & CAME</a></li>
            <li><a href="/es/posts/5-fuerzas-porter-cuantitativas/">5 Fuerzas de Porter</a></li>
            <li><a href="/es/posts/matriz-pestel-cuantitativa/">Matriz PESTEL C-Level</a></li>
            <li><a href="/es/recursos/#mega-bundle">Mega Bundle Completo</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Contacto & Redes</h4>
          <ul class="footer-links">
            <li><a href="https://www.linkedin.com/in/daniel-al%C3%A1ez-ria%C3%B1o/" target="_blank">LinkedIn ↗</a></li>
            <li><a href="https://github.com/Dalaez" target="_blank">GitHub ↗</a></li>
            <li><a href="https://twitter.com/Dalaez" target="_blank">X (Twitter) ↗</a></li>
            <li><a href="/es/contact/">Formulario de Contacto</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>© 2026 Datalaria. Todos los derechos reservados. Diseñado para rendimiento y máxima autoridad.</div>
        <div class="social-links">
          <span>Construido con Hugo & PaperMod</span>
          <span>•</span>
          <span>Hosting en Netlify</span>
        </div>
      </div>
    </div>
  </footer>

  <!-- SCRIPT DE INTERACTIVIDAD DEL MOCKUP -->
  <script>
    // 1. Data completa de los artículos
    const allPosts = {json_posts_str};

    const categorizedData = {{
      tecnicos: allPosts.filter(p => p.category === 'tecnicos'),
      proyectos: allPosts.filter(p => p.category === 'proyectos'),
      startups: allPosts.filter(p => p.category === 'startups'),
      biografias: allPosts.filter(p => p.category === 'biografias')
    }};

    // 2. Control de Modo Oscuro / Claro
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const htmlElem = document.documentElement;

    function setTheme(theme) {{
      htmlElem.setAttribute('data-theme', theme);
      localStorage.setItem('datalaria-theme', theme);
      updateThemeIcon(theme);
    }}

    function updateThemeIcon(theme) {{
      const icon = document.getElementById('themeIcon');
      if (theme === 'dark') {{
        icon.innerHTML = '<path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>';
      }} else {{
        icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
      }}
    }}

    themeToggleBtn.addEventListener('click', () => {{
      const current = htmlElem.getAttribute('data-theme');
      const nextTheme = current === 'dark' ? 'light' : 'dark';
      setTheme(nextTheme);
    }});

    // Inicializar tema guardado o preferido
    const savedTheme = localStorage.getItem('datalaria-theme') || 'dark';
    setTheme(savedTheme);

    // 3. Post Aleatorio Interactivo
    const btnShuffle = document.getElementById('btnShuffle');
    const randomTitle = document.getElementById('randomTitle');
    const randomDesc = document.getElementById('randomDesc');
    const randomLink = document.getElementById('randomLink');

    function pickRandomPost() {{
      const randomIndex = Math.floor(Math.random() * allPosts.length);
      const post = allPosts[randomIndex];
      
      // Animación suave
      randomTitle.style.opacity = '0';
      randomDesc.style.opacity = '0';
      
      setTimeout(() => {{
        randomTitle.textContent = post.title;
        randomDesc.textContent = post.desc || "Un apasionante artículo de investigación y tecnología en Datalaria. Haz clic para leerlo al completo.";
        randomLink.href = post.url;
        randomTitle.style.opacity = '1';
        randomDesc.style.opacity = '1';
      }}, 150);
    }}

    btnShuffle.addEventListener('click', pickRandomPost);

    // 4. Conmutador de Categorías
    const catTitles = {{
      tecnicos: "Artículos Técnicos & Gestión Estratégica (41 posts)",
      proyectos: "Proyectos Tecnológicos & Series de Ingeniería (34 posts)",
      startups: "Startups & Casos de Negocio (12 posts)",
      biografias: "Biografías de Pioneros (11 posts)"
    }};

    function switchCategory(catKey) {{
      // Update cards UI
      document.querySelectorAll('.category-card').forEach(c => {{
        if (c.getAttribute('data-category') === catKey) {{
          c.classList.add('active');
        }} else {{
          c.classList.remove('active');
        }}
      }});

      const titleEl = document.getElementById('catPreviewTitle');
      const listEl = document.getElementById('catPreviewList');
      titleEl.textContent = "Artículos destacados en: " + catTitles[catKey];

      const posts = categorizedData[catKey] || [];
      // Show top 6 posts
      const featured = posts.slice(0, 6);

      listEl.innerHTML = featured.map(p => `
        <a href="${{p.url}}" class="preview-post-item">
          <div>
            <div class="preview-post-title">${{p.title}}</div>
          </div>
          <div class="preview-post-meta">
            <span>📅 ${{p.date || 'Reciente'}}</span>
            <span style="color: var(--accent); font-weight: 500;">Leer artículo →</span>
          </div>
        </a>
      `).join('');
    }}

    // Iniciar con la categoría técnicos
    switchCategory('tecnicos');
  </script>
</body>
</html>
"""

with open('mockup_homepage.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Created mockup_homepage.html successfully!")
