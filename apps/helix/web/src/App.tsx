import React, { useState } from 'react';
import { Language, SQUAD_AGENTS, TRANSLATIONS } from './i18n';
import {
  ProjectState,
  DEFAULT_EXAMPLES,
  calculateTriage,
  calculateSpecQuality,
  generateSddFiles,
  generateMegaPrompt,
} from './engine';
import { downloadZip } from './utils/zipBuilder';
import { trackHelixEvent } from './utils/analytics';
import './styles.css';

type ActiveTab = 'squad' | 'modeA' | 'modeB' | 'pricing';

export const App: React.FC = () => {
  // Inicialización de estado limpia derivada de URL (evita useEffect síncrono para oxlint)
  const [lang, setLang] = useState<Language>(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const urlLang = params.get('lang');
      if (urlLang === 'es' || urlLang === 'en') return urlLang;
      const stored = localStorage.getItem('helix_lang');
      if (stored === 'es' || stored === 'en') return stored;
    }
    return 'es';
  });

  const [state, setState] = useState<ProjectState>(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      if (params.get('demo') === 'true' || params.get('example') === 'saas') {
        return DEFAULT_EXAMPLES.saas;
      }
      if (params.get('example') === 'quant') {
        return DEFAULT_EXAMPLES.quant;
      }
      if (params.get('example') === 'margin') {
        return DEFAULT_EXAMPLES.margin;
      }
    }
    return DEFAULT_EXAMPLES.static;
  });

  const [activeTab, setActiveTab] = useState<ActiveTab>('squad');
  const [selectedFileIdx, setSelectedFileIdx] = useState<number>(0);
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);
  const [copiedTriage, setCopiedTriage] = useState<boolean>(false);

  // Formulario Waitlist Brevo
  const [waitlistEmail, setWaitlistEmail] = useState<string>('');
  const [waitlistStatus, setWaitlistStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const t = TRANSLATIONS[lang];
  const triage = calculateTriage(state);
  const quality = calculateSpecQuality(state);
  const sddFiles = generateSddFiles(state, lang);
  const megaPrompt = generateMegaPrompt(state, lang);

  const toggleLanguage = () => {
    const nextLang: Language = lang === 'es' ? 'en' : 'es';
    setLang(nextLang);
    localStorage.setItem('helix_lang', nextLang);
  };

  const loadExample = (type: 'static' | 'saas' | 'quant' | 'margin') => {
    setState(DEFAULT_EXAMPLES[type]);
    setSelectedFileIdx(0);
  };

  const handleCopyTriageCard = async () => {
    try {
      await navigator.clipboard.writeText(triage.cardLines.join('\n'));
      setCopiedTriage(true);
      setTimeout(() => setCopiedTriage(false), 2000);
    } catch {
      // Fallback
    }
  };

  const handleCopyMegaPrompt = async () => {
    try {
      await navigator.clipboard.writeText(megaPrompt);
      setCopiedPrompt(true);
      trackHelixEvent('copy_helix_megaprompt', { slug: state.slug, language: lang });
      setTimeout(() => setCopiedPrompt(false), 2000);
    } catch {
      // Fallback
    }
  };

  const handleDownloadZip = () => {
    const filename = `${state.slug || 'my-app'}-helix-sdd-starter.zip`;
    downloadZip(filename, sddFiles);
    trackHelixEvent('generate_helix_spec_zip', {
      slug: state.slug,
      score: quality.totalScore,
      language: lang,
    });
  };

  const handleWaitlistSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!waitlistEmail.trim()) return;

    setWaitlistStatus('loading');
    trackHelixEvent('join_waitlist_helix', { email: waitlistEmail, language: lang });

    // Fallback local para localhost / 127.0.0.1 (USER-FIX / INV-HELIX-WL-5)
    const isLocalhost =
      typeof window !== 'undefined' &&
      (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

    if (isLocalhost) {
      setTimeout(() => {
        setWaitlistStatus('success');
      }, 400);
      return;
    }

    try {
      const res = await fetch('/.netlify/functions/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: waitlistEmail,
          list: 'helix',
          language: lang,
        }),
      });
      if (res.ok) {
        setWaitlistStatus('success');
      } else {
        setWaitlistStatus('error');
      }
    } catch {
      setWaitlistStatus('error');
    }
  };

  const toggleSurface = (surface: string) => {
    setState((prev) => {
      const exists = prev.surfaces.includes(surface);
      const next = exists
        ? prev.surfaces.filter((s) => s !== surface)
        : [...prev.surfaces, surface];
      return { ...prev, surfaces: next };
    });
  };

  const toggleNonGoal = (ng: string) => {
    setState((prev) => {
      const exists = prev.selectedNonGoals.includes(ng);
      const next = exists
        ? prev.selectedNonGoals.filter((item) => item !== ng)
        : [...prev.selectedNonGoals, ng];
      return { ...prev, selectedNonGoals: next };
    });
  };

  const handleAddSuggestedInvariants = () => {
    const slugUpper = (state.slug || 'app').toUpperCase();
    const suggestions = [
      `INV-${slugUpper}-1: Cero llamadas a APIs externas en modo desconectado`,
      `INV-${slugUpper}-2: Validación estricta de esquemas antes de persistencia`,
      `INV-${slugUpper}-3: Cobertura de tests automatizados >= 90% con código 0`,
    ];
    setState((prev) => ({
      ...prev,
      invariants: Array.from(new Set([...prev.invariants, ...suggestions])),
    }));
  };

  const backUrl = lang === 'es' ? '/es/' : '/en/';

  return (
    <div className="helix-app">
      {/* 1. Header */}
      <header className="helix-header">
        <div className="header-left">
          <a href={backUrl} className="back-link">
            {t.backToDatalaria}
          </a>
          <div className="brand-badge">
            <span className="brand-dot"></span>
            <span>Datalaria Helix</span>
          </div>
          <span className="early-bird-pill">{t.earlyBirdBadge}</span>
        </div>

        <div className="header-right">
          <button className="lang-btn" onClick={toggleLanguage}>
            {lang === 'es' ? 'EN 🇬🇧' : 'ES 🇪🇸'}
          </button>
        </div>
      </header>

      {/* 2. Examples Bar */}
      <nav className="examples-bar">
        <span className="examples-label">{t.loadExampleLabel}</span>
        <button className="example-chip" onClick={() => loadExample('static')}>
          📐 {t.exampleStatic}
        </button>
        <button className="example-chip" onClick={() => loadExample('saas')}>
          ☁️ {t.exampleSaas}
        </button>
        <button className="example-chip" onClick={() => loadExample('quant')}>
          📈 {t.exampleQuant}
        </button>
        <button className="example-chip" onClick={() => loadExample('margin')}>
          🏆 {t.exampleMargin}
        </button>
      </nav>

      {/* 3. Main Split Container */}
      <main className="main-container">
        {/* Columna Izquierda: Entrevista SDD en 5 Pilares */}
        <section className="pillars-card">
          {/* Pilar 1: Identidad */}
          <div className="pillar-section">
            <div className="pillar-header">
              <h3 className="pillar-title">{t.p1Title}</h3>
            </div>
            <div className="form-group">
              <label className="form-label">{t.p1Slug}</label>
              <input
                type="text"
                className="form-input"
                value={state.slug}
                onChange={(e) => setState({ ...state, slug: e.target.value.toLowerCase().replace(/[^a-z0-9-]/g, '-') })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">{t.p1Name}</label>
              <input
                type="text"
                className="form-input"
                value={state.name}
                onChange={(e) => setState({ ...state, name: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">{t.p1Problem}</label>
              <textarea
                className="form-textarea"
                rows={2}
                value={state.problem}
                onChange={(e) => setState({ ...state, problem: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">{t.p1User}</label>
              <input
                type="text"
                className="form-input"
                value={state.targetUser}
                onChange={(e) => setState({ ...state, targetUser: e.target.value })}
              />
            </div>
          </div>

          {/* Pilar 2: Non-Goals */}
          <div className="pillar-section">
            <div className="pillar-header">
              <h3 className="pillar-title">{t.p2Title}</h3>
            </div>
            <div className="form-group">
              <label className="form-label">{t.p2Help}</label>
              <div className="checkbox-group">
                {[t.nonGoal1, t.nonGoal2, t.nonGoal3].map((ng, i) => (
                  <label key={i} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={state.selectedNonGoals.includes(ng)}
                      onChange={() => toggleNonGoal(ng)}
                    />
                    <span>{ng}</span>
                  </label>
                ))}
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">{t.p2Custom}</label>
              <input
                type="text"
                className="form-input"
                value={state.customNonGoals}
                onChange={(e) => setState({ ...state, customNonGoals: e.target.value })}
              />
            </div>
          </div>

          {/* Pilar 3: Arquitectura, Superficies y Tokens */}
          <div className="pillar-section">
            <div className="pillar-header">
              <h3 className="pillar-title">{t.p3Title}</h3>
            </div>
            <div className="form-group">
              <label className="form-label">{t.p3SurfacesHelp}</label>
              <div className="surfaces-grid">
                {[
                  { id: 'docs', label: t.surfaceDocs },
                  { id: 'ui', label: t.surfaceUi },
                  { id: 'frontend', label: t.surfaceFrontend },
                  { id: 'backend', label: t.surfaceBackend },
                  { id: 'data_sql', label: t.surfaceDataSql },
                  { id: 'apis', label: t.surfaceApis },
                  { id: 'media_i18n', label: t.surfaceMediaI18n },
                  { id: 'monetization', label: t.surfaceMonetization },
                  { id: 'auth_security', label: t.surfaceAuthSecurity },
                ].map((s) => (
                  <label key={s.id} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={state.surfaces.includes(s.id)}
                      onChange={() => toggleSurface(s.id)}
                    />
                    <span>{s.label}</span>
                  </label>
                ))}
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">{t.p3Preset}</label>
              <select
                className="form-select"
                value={state.designPreset}
                onChange={(e) => setState({ ...state, designPreset: e.target.value })}
              >
                <option value={t.presetDataDense}>{t.presetDataDense}</option>
                <option value={t.presetMinimal}>{t.presetMinimal}</option>
                <option value={t.presetEditorial}>{t.presetEditorial}</option>
                <option value={t.presetPlayful}>{t.presetPlayful}</option>
                <option value={t.presetMobile}>{t.presetMobile}</option>
              </select>
            </div>
          </div>

          {/* Pilar 4: Invariantes INV-* */}
          <div className="pillar-section">
            <div className="pillar-header">
              <h3 className="pillar-title">{t.p4Title}</h3>
            </div>
            <div className="form-group">
              <label className="form-label">{t.p4Help}</label>
              <div className="checkbox-group">
                {state.invariants.map((inv, idx) => (
                  <span key={idx} style={{ fontSize: '0.8125rem', color: '#a5b4fc', fontFamily: 'monospace' }}>
                    • {inv}
                  </span>
                ))}
              </div>
              <button
                type="button"
                className="action-btn-small"
                onClick={handleAddSuggestedInvariants}
              >
                {t.suggestInvariants}
              </button>
            </div>
          </div>

          {/* Pilar 5: Verification Gates */}
          <div className="pillar-section">
            <div className="pillar-header">
              <h3 className="pillar-title">{t.p5Title}</h3>
            </div>
            <div className="form-group">
              <label className="form-label">{t.p5GateHelp}</label>
              <input
                type="text"
                className="form-input"
                value={state.gateCommand}
                onChange={(e) => setState({ ...state, gateCommand: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">{t.p5FilesEstimated}</label>
              <input
                type="number"
                className="form-input"
                min={1}
                max={50}
                value={state.estimatedFiles}
                onChange={(e) => setState({ ...state, estimatedFiles: parseInt(e.target.value, 10) || 1 })}
              />
            </div>
          </div>
        </section>

        {/* Columna Derecha: Cockpit de Diagnóstico y Artefactos */}
        <section className="cockpit-card">
          {/* Score Banner Permanente */}
          <div className="score-banner">
            <div className="score-main">
              <div className={`score-circle ${quality.passed ? 'pass' : ''}`}>
                {quality.totalScore}
              </div>
              <div className="score-meta">
                <h4>{t.scoreTitle}</h4>
                <div className="pillars-breakdown">
                  <span className="pillar-chip">P1:{quality.pillars.problem}</span>
                  <span className="pillar-chip">P2:{quality.pillars.nongoals}</span>
                  <span className="pillar-chip">P3:{quality.pillars.contracts}</span>
                  <span className="pillar-chip">P4:{quality.pillars.invariants}</span>
                  <span className="pillar-chip">P5:{quality.pillars.gates}</span>
                </div>
              </div>
            </div>

            <div>
              <span
                className={`vibe-risk-badge ${
                  quality.vibeDebtRisk <= 20
                    ? 'vibe-low'
                    : quality.vibeDebtRisk <= 50
                    ? 'vibe-mid'
                    : 'vibe-high'
                }`}
              >
                {t.vibeDebtRisk}{' '}
                {quality.vibeDebtRisk <= 20
                  ? t.vibeRiskLow
                  : quality.vibeDebtRisk <= 50
                  ? t.vibeRiskMedium
                  : t.vibeRiskHigh}
              </span>
            </div>
          </div>

          {/* Caja de Tarjeta de Triaje (6 Líneas) */}
          <div className="triage-box">
            <button className="copy-corner-btn" onClick={handleCopyTriageCard}>
              {copiedTriage ? t.copiedBadge : t.copyTriageCard}
            </button>
            <pre>{triage.cardLines.join('\n')}</pre>
          </div>

          {/* Pestañas de Vista */}
          <div className="cockpit-tabs">
            <button
              className={`tab-btn ${activeTab === 'squad' ? 'active' : ''}`}
              onClick={() => setActiveTab('squad')}
            >
              {t.tabSquad}
            </button>
            <button
              className={`tab-btn ${activeTab === 'modeA' ? 'active' : ''}`}
              onClick={() => setActiveTab('modeA')}
            >
              {t.tabModeA}
            </button>
            <button
              className={`tab-btn ${activeTab === 'modeB' ? 'active' : ''}`}
              onClick={() => setActiveTab('modeB')}
            >
              {t.tabModeB}
            </button>
            <button
              className={`tab-btn ${activeTab === 'pricing' ? 'active' : ''}`}
              onClick={() => setActiveTab('pricing')}
            >
              {t.tabPricing}
            </button>
          </div>

          {/* Vista 1: Cuadrícula del Escuadrón (12 Agentes) */}
          {activeTab === 'squad' && (
            <div className="squad-view">
              <div className="squad-counts">
                <span>
                  🟢 <strong>{triage.activeAgents.length}</strong> {t.squadActiveCount}
                </span>
                <span>
                  ⏸️ <strong>{triage.benchedAgents.length}</strong> {t.squadBenchedCount}
                </span>
              </div>
              <div className="agent-grid">
                {SQUAD_AGENTS.map((agent) => {
                  const isActive = triage.activeAgents.includes(agent.id);
                  return (
                    <div
                      key={agent.id}
                      className={`agent-card ${isActive ? 'active' : 'benched'}`}
                    >
                      <div className="agent-head">
                        <span className="agent-name">
                          <span>{agent.icon}</span>
                          <span>{agent.name}</span>
                        </span>
                        {agent.hasVeto && <span className="veto-tag">{t.vetoBadge}</span>}
                      </div>
                      <span className="agent-role">{agent.role}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Vista 2: Modo A — Archivos SDD y Descarga ZIP */}
          {activeTab === 'modeA' && (
            <div className="mode-a-view">
              <div className="preview-controls">
                <div className="preview-selector">
                  {sddFiles.map((file, idx) => (
                    <button
                      key={file.name}
                      className={`preview-tab-chip ${selectedFileIdx === idx ? 'active' : ''}`}
                      onClick={() => setSelectedFileIdx(idx)}
                    >
                      {file.name.split('/').pop()}
                    </button>
                  ))}
                </div>
                <button className="cta-btn-primary" onClick={handleDownloadZip}>
                  {t.downloadZipBtn}
                </button>
              </div>
              <pre className="code-preview-pane">
                {sddFiles[selectedFileIdx]?.content}
              </pre>
            </div>
          )}

          {/* Vista 3: Modo B — Mega-Prompt SDD */}
          {activeTab === 'modeB' && (
            <div className="mode-b-view">
              <div className="preview-controls">
                <span style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>
                  {t.promptHelp}
                </span>
                <button className="cta-btn-primary" onClick={handleCopyMegaPrompt}>
                  {copiedPrompt ? t.copiedBadge : t.copyPromptBtn}
                </button>
              </div>
              <pre className="code-preview-pane">{megaPrompt}</pre>
            </div>
          )}

          {/* Vista 4: Escalera de Valor y Waitlist Brevo */}
          {activeTab === 'pricing' && (
            <div className="pricing-view">
              <div className="pricing-grid">
                <div className="pricing-plan">
                  <h4 className="plan-title">{t.planSandbox}</h4>
                  <p className="plan-desc">{t.planSandboxDesc}</p>
                </div>
                <div className="pricing-plan">
                  <h4 className="plan-title">{t.planStarter}</h4>
                  <p className="plan-desc">{t.planStarterDesc}</p>
                </div>
                <div className="pricing-plan highlight">
                  <h4 className="plan-title">{t.planCore}</h4>
                  <p className="plan-desc">{t.planCoreDesc}</p>
                </div>
              </div>

              <form className="waitlist-form" onSubmit={handleWaitlistSubmit}>
                <h4>{t.joinWaitlistTitle}</h4>
                <div className="waitlist-inputs">
                  <input
                    type="email"
                    placeholder={t.emailPlaceholder}
                    value={waitlistEmail}
                    onChange={(e) => setWaitlistEmail(e.target.value)}
                  />
                  <button
                    type="submit"
                    className="cta-btn-primary"
                    disabled={waitlistStatus === 'loading'}
                  >
                    {waitlistStatus === 'loading' ? '...' : t.joinWaitlistBtn}
                  </button>
                </div>
                {waitlistStatus === 'success' && (
                  <div className="success-banner">{t.waitlistSuccess}</div>
                )}
              </form>
            </div>
          )}
        </section>
      </main>
    </div>
  );
};
