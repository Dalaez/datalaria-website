// apps/reading/app.js - Controlador reactivo SPA, cronómetro lector split, teclado táctil 3D, perfiles, diploma PNG y PWA
(function() {
  'use strict';

  const catalog = window.READING_CATALOG;
  const engine = window.ReadingEngine;
  const audio = window.ReadingAudio;
  const esc = engine.escapeHtml;

  const APP_VERSION = 'v1.0.0';
  const TOTAL_ROUNDS = 10;

  // Estado global de UI y pedagogía
  let lang = 'es';
  let activeTab = 'play';
  let learnSubTab = 'letters';
  let selectedLevel = 'l1';
  let selectedMode = 'normal';
  let useUpperCase = true;
  let colorSyllables = true;
  let learnSlowMode = false;
  let activeMixerIndex = 0;

  // Estado de partida activa
  let inGame = false;
  let inFeedbackPause = false;
  let awaitingMicroCheck = false;
  let feedbackTimeout = null;
  let timerInterval = null;
  let roundIndex = 0;
  let score = 0;
  let correctCount = 0;
  let wrongCount = 0;
  let streak = 0;
  let bestStreak = 0;
  let currentChallenge = null;
  let recentIds = [];
  let dailyRng = null;
  let dailyDateParam = null;

  // Cronómetro lector y teclado l3
  let roundStartMs = 0;
  let stopwatchElapsedMs = 0;
  let frozenElapsedMs = null;
  let frozenWpm = 0;
  let sprintTimeLeft = 60.0;
  let sprintTotalTime = 60.0;
  let filledSlots = [];
  let activeSlotCursor = 0;
  let isHintVisible = false;
  let hintUsedThisRound = false;
  let roundHistory = [];

  // PWA Prompt y Service Worker
  let deferredInstallPrompt = null;
  let isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
  let swRegistration = null;
  let swRefreshing = false;

  // Perfiles Familiares y Persistencia Local Aislada (INV-READ-11)
  let activeProfileId = 'player_1';
  let userStats = createEmptyStats();

  function createEmptyStats() {
    return {
      highScores: {},
      bestWpm: 0,
      bestStreakEver: 0,
      unlockedMedals: []
    };
  }

  function sanitizeStats(raw) {
    const clean = createEmptyStats();
    if (!raw || typeof raw !== 'object') return clean;

    if (raw.highScores && typeof raw.highScores === 'object') {
      const validLevels = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6'];
      validLevels.forEach(lvl => {
        const val = Number(raw.highScores[lvl]);
        if (Number.isFinite(val) && val >= 0) {
          clean.highScores[lvl] = Math.round(val);
        }
      });
    }

    const wpm = Number(raw.bestWpm);
    if (Number.isFinite(wpm) && wpm >= 0 && wpm <= 350) {
      clean.bestWpm = Math.round(wpm);
    }

    const bestStr = Number(raw.bestStreakEver);
    if (Number.isFinite(bestStr) && bestStr >= 0) {
      clean.bestStreakEver = Math.round(bestStr);
    }

    if (Array.isArray(raw.unlockedMedals) && catalog.medals) {
      const validMedals = new Set(catalog.medals.map(m => m.id));
      clean.unlockedMedals = raw.unlockedMedals
        .filter(id => typeof id === 'string' && validMedals.has(id))
        .filter((id, idx, arr) => arr.indexOf(id) === idx);
    }

    return clean;
  }

  function getStorageKey(profileId = activeProfileId) {
    return `datalaria_reading_v1_stats_${profileId}`;
  }

  function loadStats() {
    try {
      const savedProfile = localStorage.getItem('datalaria_reading_active_profile');
      if (savedProfile && catalog.profiles && catalog.profiles.some(p => p.id === savedProfile)) {
        activeProfileId = savedProfile;
      }
    } catch { /* sin acceso a localStorage */ }

    userStats = createEmptyStats();
    try {
      const data = localStorage.getItem(getStorageKey());
      if (data) {
        userStats = sanitizeStats(JSON.parse(data));
      }
    } catch {
      userStats = createEmptyStats();
    }

    try {
      const savedSound = localStorage.getItem('reading-sound');
      if (savedSound !== null) {
        const wantsSound = savedSound === 'true';
        if (wantsSound !== audio.isSoundEnabled()) {
          audio.toggleSound();
        }
      }
    } catch { /* ignorar */ }

    try {
      const savedCase = localStorage.getItem('reading-case');
      if (savedCase === 'lower' || savedCase === 'upper') {
        useUpperCase = savedCase === 'upper';
      }
      const savedSyl = localStorage.getItem('reading-syllables');
      if (savedSyl === 'true' || savedSyl === 'false') {
        colorSyllables = savedSyl === 'true';
      }
    } catch { /* ignorar */ }
  }

  function saveStats() {
    try {
      localStorage.setItem(getStorageKey(), JSON.stringify(userStats));
    } catch { /* ignorar */ }
  }

  function switchProfile(profileId) {
    if (!catalog.profiles || !catalog.profiles.some(p => p.id === profileId)) return;
    if (profileId === activeProfileId) return;
    audio.playClick();
    activeProfileId = profileId;
    try {
      localStorage.setItem('datalaria_reading_active_profile', profileId);
    } catch { /* ignorar */ }
    loadStats();
    const profileObj = catalog.profiles.find(p => p.id === profileId);
    const profileName = profileObj ? `${profileObj.avatar} ${profileObj.name[lang]}` : profileId;
    showToast(`${t('profile_switched')} ${profileName}`);
    renderAll();
  }

  function showToast(msg, duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  function initLang() {
    const params = new URLSearchParams(window.location.search);
    const urlLang = params.get('lang');
    if (urlLang === 'en' || urlLang === 'es') {
      lang = urlLang;
    } else {
      lang = (navigator.language && navigator.language.startsWith('en')) ? 'en' : 'es';
    }

    const queryMode = params.get('mode');
    if (queryMode && ['normal', 'stopwatch', 'sprint', 'daily'].includes(queryMode)) {
      selectedMode = queryMode;
    }
    const queryLevel = params.get('level');
    if (queryLevel && catalog.levels.some(l => l.id === queryLevel)) {
      selectedLevel = queryLevel;
    }
    const queryDate = params.get('date');
    if (queryDate && /^\d{4}-\d{2}-\d{2}$/.test(queryDate)) {
      dailyDateParam = queryDate;
    }
  }

  function t(key) {
    return (catalog.i18n[lang] && catalog.i18n[lang][key]) || key;
  }

  function formatWordCase(str) {
    const raw = String(str || '');
    return useUpperCase ? raw.toUpperCase() : raw.toLowerCase();
  }

  function formatSentenceCase(str) {
    const raw = String(str || '');
    return useUpperCase ? raw.toUpperCase() : raw;
  }

  function formatStopwatch(ms) {
    const safeMs = Math.max(0, Number(ms) || 0);
    const totalTenths = Math.floor(safeMs / 100);
    const tenths = totalTenths % 10;
    const totalSec = Math.floor(totalTenths / 10);
    const secs = totalSec % 60;
    const mins = Math.floor(totalSec / 60);
    const mStr = String(mins).padStart(2, '0');
    const sStr = String(secs).padStart(2, '0');
    return `${mStr}:${sStr}.${tenths}`;
  }

  function getSafetyCapSec(levelId) {
    return (levelId === 'l5' || levelId === 'l6') ? 45 : 20;
  }

  // ==========================================================================
  // Renderizadores de Shell, Perfiles y Pestañas
  // ==========================================================================
  function renderAll() {
    renderShell();
    renderTabs();
    if (activeTab === 'play') renderPlayTab();
    else if (activeTab === 'learn') renderLearnTab();
    else if (activeTab === 'achievements') renderAchievementsTab();
  }

  function renderShell() {
    const titleEl = document.getElementById('shell-app-title');
    if (titleEl) titleEl.textContent = t('app_title');

    const langBtn = document.getElementById('lang-btn');
    if (langBtn) langBtn.textContent = lang === 'es' ? '🇪🇸 ES' : '🇬🇧 EN';

    const soundBtn = document.getElementById('sound-btn');
    if (soundBtn) {
      soundBtn.textContent = audio.isSoundEnabled() ? '🔊' : '🔇';
      soundBtn.title = t('sound_toggle');
    }

    const themeBtn = document.getElementById('theme-btn');
    if (themeBtn) themeBtn.title = t('theme_toggle');

    const checkUpdateBtn = document.getElementById('btn-check-update');
    if (checkUpdateBtn) checkUpdateBtn.title = t('check_update_title');

    const installBtn = document.getElementById('btn-install-pwa');
    const installLabel = document.getElementById('label-install-btn');
    if (installBtn && installLabel) {
      installLabel.textContent = t('install_app');
      installBtn.title = t('install_app_title');
      installBtn.style.display = isStandalone ? 'none' : 'inline-flex';
    }

    const backLink = document.getElementById('datalaria-back-link');
    if (backLink) {
      backLink.textContent = t('datalaria_back');
      backLink.href = `/${lang}/apps/`;
    }

    const specLink = document.getElementById('link-spec');
    if (specLink) {
      specLink.textContent = t('spec_link');
      specLink.href = `/${lang}/apps/reading/`;
    }

    const postLink = document.getElementById('link-post');
    if (postLink) {
      postLink.textContent = t('post_link');
      postLink.href = `/${lang}/posts/`;
    }

    const kitsLink = document.getElementById('link-kits');
    if (kitsLink) {
      kitsLink.textContent = t('kits_link');
      kitsLink.href = lang === 'es' ? '/es/recursos/' : '/en/resources/';
    }

    document.title = lang === 'es'
      ? 'Lector Arcade — Aprendizaje de Lectura (Datalaria)'
      : 'Reader Arcade — Gamified Reading Practice (Datalaria)';

    renderProfileBar();
  }

  function renderProfileBar() {
    const bar = document.getElementById('profile-bar');
    if (!bar || !catalog.profiles) return;
    bar.innerHTML = `
      <span class="profile-bar-label">👥 ${esc(t('profile_label'))}</span>
      ${catalog.profiles.map(p => `
        <button class="profile-chip ${activeProfileId === p.id ? 'active' : ''}" data-profile-id="${esc(p.id)}" title="${esc(p.title[lang])}">
          <span>${esc(p.avatar)}</span>
          <span>${esc(p.name[lang])}</span>
          ${activeProfileId === p.id ? '<span style="font-size: 0.75rem; margin-left: 2px;">✓</span>' : ''}
        </button>
      `).join('')}
    `;

    bar.querySelectorAll('.profile-chip').forEach(chip => {
      chip.onclick = () => {
        switchProfile(chip.getAttribute('data-profile-id'));
      };
    });
  }

  function renderTabs() {
    const tabs = [
      { id: 'play', label: t('tab_play') },
      { id: 'learn', label: t('tab_learn') },
      { id: 'achievements', label: t('tab_achievements') }
    ];

    const nav = document.getElementById('tabs-nav');
    if (!nav) return;
    nav.innerHTML = tabs.map(tab => `
      <button class="tab-btn ${activeTab === tab.id ? 'active' : ''}" data-tab="${esc(tab.id)}">
        ${esc(tab.label)}
      </button>
    `).join('');

    nav.querySelectorAll('.tab-btn').forEach(btn => {
      btn.onclick = () => {
        if (inGame) {
          endGameSession();
        }
        activeTab = btn.getAttribute('data-tab');
        renderAll();
      };
    });
  }

  function renderPedagogyToolbar() {
    return `
      <div class="pedagogy-toolbar">
        <button id="btn-toggle-case" class="pedagogy-toggle-btn ${useUpperCase ? 'active' : ''}" title="${esc(t('font_case_toggle'))}">
          ${useUpperCase ? 'AA MAYÚS' : 'Aa minús'}
        </button>
        <button id="btn-toggle-syllables" class="pedagogy-toggle-btn ${colorSyllables ? 'active' : ''}" title="${esc(t('syllable_toggle'))}">
          🎨 ${lang === 'es' ? 'Sílabas' : 'Syllables'}
        </button>
      </div>
    `;
  }

  function bindPedagogyToolbar(onChange) {
    const caseBtn = document.getElementById('btn-toggle-case');
    if (caseBtn) {
      caseBtn.onclick = () => {
        audio.playClick();
        useUpperCase = !useUpperCase;
        try { localStorage.setItem('reading-case', useUpperCase ? 'upper' : 'lower'); } catch { /* */ }
        if (onChange) onChange();
      };
    }

    const sylBtn = document.getElementById('btn-toggle-syllables');
    if (sylBtn) {
      sylBtn.onclick = () => {
        audio.playClick();
        colorSyllables = !colorSyllables;
        try { localStorage.setItem('reading-syllables', colorSyllables ? 'true' : 'false'); } catch { /* */ }
        if (onChange) onChange();
      };
    }
  }

  // ==========================================================================
  // Pestaña 1: Jugar
  // ==========================================================================
  function renderPlayTab() {
    const container = document.getElementById('tab-content');
    if (!container) return;

    if (!inGame) {
      const html = `
        <div class="card">
          <h2 style="font-size: 1.4rem; font-weight: 800; margin-bottom: 8px;">${esc(t('choose_level'))}</h2>
          <div class="levels-grid">
            ${catalog.levels.map(lvl => `
              <div class="selectable-item ${selectedLevel === lvl.id ? 'selected' : ''}" data-level="${esc(lvl.id)}">
                <div style="font-size: 1.8rem; margin-bottom: 4px;">${esc(lvl.icon)}</div>
                <strong style="display: block; font-size: 1.05rem;">${esc(lvl.name[lang])}</strong>
                <span style="font-size: 0.85rem; color: var(--text-secondary); display: block; margin-top: 4px;">${esc(lvl.desc[lang])}</span>
              </div>
            `).join('')}
          </div>

          <h2 style="font-size: 1.4rem; font-weight: 800; margin: 24px 0 8px;">${esc(t('choose_mode'))}</h2>
          <div class="levels-grid">
            ${catalog.modes.map(m => `
              <div class="selectable-item ${selectedMode === m.id ? 'selected' : ''}" data-mode="${esc(m.id)}">
                <div style="font-size: 1.8rem; margin-bottom: 4px;">${esc(m.icon)}</div>
                <strong style="display: block; font-size: 1.05rem;">${esc(m.name[lang])}</strong>
                <span style="font-size: 0.85rem; color: var(--text-secondary); display: block; margin-top: 4px;">${esc(m.desc[lang])}</span>
              </div>
            `).join('')}
          </div>

          <div style="text-align: center; margin-top: 30px;">
            <button id="btn-start" class="btn-arcade btn-arcade-primary" style="font-size: 1.3rem; padding: 14px 36px; border-radius: var(--radius-pill);">
              ${esc(t('start_game'))}
            </button>
          </div>
        </div>
      `;
      container.innerHTML = html;

      container.querySelectorAll('[data-level]').forEach(el => {
        el.onclick = () => {
          audio.playClick();
          selectedLevel = el.getAttribute('data-level');
          renderPlayTab();
        };
      });
      container.querySelectorAll('[data-mode]').forEach(el => {
        el.onclick = () => {
          audio.playClick();
          selectedMode = el.getAttribute('data-mode');
          renderPlayTab();
        };
      });
      const startBtn = document.getElementById('btn-start');
      if (startBtn) startBtn.onclick = startGameSession;
      return;
    }

    renderActiveGame(container);
  }

  function renderActiveStageContent() {
    if (!currentChallenge) return '<div>...</div>';
    const ch = currentChallenge;

    if (ch.levelId === 'l1') {
      const anchor = String(ch.anchorWord || ch.prompt || '');
      const target = String(ch.prompt || '');
      const upperAnchor = anchor.toUpperCase();
      const upperTarget = target.toUpperCase();
      let restWord = anchor;
      if (upperAnchor.startsWith(upperTarget)) {
        restWord = anchor.slice(target.length);
      }
      const promptLabel = lang === 'es' ? '¿Con qué letra o sílaba empieza?' : 'Starts with which letter?';

      return `
        <div class="reading-emoji-anchor" aria-hidden="true">${esc(ch.emoji || '')}</div>
        <div class="reading-word-hero ${useUpperCase ? 'case-upper' : ''}">
          <span class="syl-a" style="border-bottom: 4px solid var(--op-add); padding: 0 6px;">?</span><span>${esc(formatWordCase(restWord))}</span>
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary); font-weight: 600;">${esc(promptLabel)}</div>
        <div class="choices-grid">
          ${(ch.choices || []).map((c, idx) => `
            <button class="choice-btn ${useUpperCase ? 'case-upper' : ''}" data-choice-idx="${idx}" ${inFeedbackPause ? 'disabled' : ''}>
              <span>${esc(formatWordCase(c.label))}</span>
            </button>
          `).join('')}
        </div>
      `;
    }

    if (ch.levelId === 'l2') {
      const promptLabel = lang === 'es' ? 'Elige la palabra correcta para esta imagen:' : 'Pick the word matching this picture:';
      return `
        <div class="reading-emoji-anchor" aria-hidden="true">${esc(ch.emoji || '')}</div>
        <div style="font-size: 0.95rem; color: var(--text-secondary); font-weight: 600;">${esc(promptLabel)}</div>
        <div class="choices-grid">
          ${(ch.choices || []).map((c, idx) => `
            <button class="choice-btn ${useUpperCase ? 'case-upper' : ''}" data-choice-idx="${idx}" ${inFeedbackPause ? 'disabled' : ''}>
              <span>${esc(formatWordCase(c.label))}</span>
            </button>
          `).join('')}
        </div>
      `;
    }

    if (ch.levelId === 'l3') {
      const word = String(ch.prompt || '');
      const maskedIndices = ch.missingIndices || [];
      let slotCounter = 0;

      const slotsHtml = word.split('').map((char, charIdx) => {
        const isMissing = maskedIndices.includes(charIdx);
        if (!isMissing) {
          return `<div class="letter-slot revealed">${esc(formatWordCase(char))}</div>`;
        }
        const sIdx = slotCounter++;
        const filledChar = filledSlots[sIdx] || '';
        const isCurrent = sIdx === activeSlotCursor && !filledChar;
        const cls = filledChar
          ? 'letter-slot filled'
          : `letter-slot blank ${isCurrent ? 'active' : ''}`;
        return `<div class="${cls}" data-slot-idx="${sIdx}" role="button" tabindex="0">${esc(filledChar ? formatWordCase(filledChar) : '')}</div>`;
      }).join('');

      return `
        <div class="reading-emoji-anchor" aria-hidden="true">${esc(ch.emoji || '')}</div>
        <div style="font-size: 0.9rem; color: var(--text-secondary); font-weight: 600;">${esc(t('keyboard_tap_hint'))}</div>
        <div class="letter-slots-container ${useUpperCase ? 'case-upper' : ''}">
          ${slotsHtml}
        </div>
        <div class="alpha-pad">
          ${(ch.keyboardChars || []).map(kChar => `
            <button class="alpha-btn ${useUpperCase ? 'case-upper' : ''}" data-alpha-char="${esc(kChar)}" ${inFeedbackPause ? 'disabled' : ''}>
              ${esc(formatWordCase(kChar))}
            </button>
          `).join('')}
          <button class="alpha-btn action-backspace" data-alpha-action="del" title="${esc(t('clear_letter_btn'))}" ${inFeedbackPause ? 'disabled' : ''}>
            ⌫
          </button>
        </div>
      `;
    }

    // l4, l5, l6 ('read_check')
    let readingHtml = '';
    if (ch.levelId === 'l4') {
      if (colorSyllables && Array.isArray(ch.syllables) && ch.syllables.length > 0) {
        const styledSyllables = ch.syllables.map((s, idx) => {
          const formatted = formatWordCase(s);
          const cls = idx % 2 === 0 ? 'syl-a' : 'syl-b';
          return `<span class="${cls}">${esc(formatted)}</span>`;
        }).join('<span class="syl-dot" aria-hidden="true">·</span>');
        readingHtml = `<div class="reading-word-hero ${useUpperCase ? 'case-upper' : ''}">${styledSyllables}</div>`;
      } else {
        readingHtml = `<div class="reading-word-hero ${useUpperCase ? 'case-upper' : ''}">${esc(formatWordCase(ch.prompt))}</div>`;
      }
    } else {
      const lines = Array.isArray(ch.lines) ? ch.lines : [ch.prompt];
      readingHtml = `
        <div class="reading-sentence-lines ${useUpperCase ? 'case-upper' : ''}">
          ${lines.map(line => `<div class="reading-sentence-line">${esc(formatSentenceCase(line))}</div>`).join('')}
        </div>
      `;
    }

    if (!awaitingMicroCheck) {
      return `
        ${readingHtml}
        ${selectedMode === 'stopwatch' ? `<div style="font-size: 0.88rem; color: var(--text-secondary); font-weight: 600;">${esc(t('stopwatch_hint'))}</div>` : ''}
        <button id="btn-read-done" class="btn-read-done" ${inFeedbackPause ? 'disabled' : ''}>
          ${esc(t('read_done_btn'))}
        </button>
      `;
    }

    // Estado 2 tras congelar cronómetro: Micro-Check de Comprensión
    const mc = ch.microCheck || { question: '', options: [] };
    return `
      ${ch.levelId === 'l4' && ch.emoji ? `<div class="reading-emoji-anchor" style="font-size: 3rem;" aria-hidden="true">${esc(ch.emoji)}</div>` : ''}
      <div class="micro-check-card">
        <div style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: var(--op-add); margin-bottom: 6px;">
          ${esc(t('micro_check_title'))}
        </div>
        <div class="micro-check-question">${esc(mc.question)}</div>
        <div class="micro-check-options">
          ${(mc.options || []).map((opt, idx) => `
            <button class="micro-check-btn" data-mc-idx="${idx}" ${inFeedbackPause ? 'disabled' : ''}>
              <span style="font-size: 1.5rem;">${esc(opt.icon || opt.emoji || '')}</span>
              <span>${esc(opt.label)}</span>
            </button>
          `).join('')}
        </div>
      </div>
    `;
  }

  function renderActiveGame(container) {
    if (!container) return;

    let roundLabel = '';
    if (selectedMode === 'normal') roundLabel = `🧘 ${t('round')} ${roundIndex}/${TOTAL_ROUNDS}`;
    else if (selectedMode === 'stopwatch') roundLabel = `⏱️ ${t('round')} ${roundIndex}/${TOTAL_ROUNDS}`;
    else if (selectedMode === 'daily') roundLabel = `📅 ${t('daily_challenge_label')} ${roundIndex}/${TOTAL_ROUNDS}`;
    else roundLabel = `⚡ ${t('round')} ${roundIndex}`;

    const comboMultiplier = streak >= 5 ? 3 : (streak >= 3 ? 2 : 1);

    let clockHudHtml = '';
    if (selectedMode === 'stopwatch' || selectedMode === 'daily') {
      const isFrozen = frozenElapsedMs !== null;
      const shownMs = isFrozen ? frozenElapsedMs : stopwatchElapsedMs;
      const wpmBadge = isFrozen && frozenWpm > 0 ? ` · ${frozenWpm} ${t('wpm_label')}` : '';
      clockHudHtml = `
        <div id="stopwatch-pill" class="stopwatch-pill ${isFrozen ? 'frozen' : ''}">
          <span>${isFrozen ? '✅' : '⏱️'}</span>
          <span id="stopwatch-display">${formatStopwatch(shownMs)}${esc(wpmBadge)}</span>
        </div>
      `;
    } else if (selectedMode === 'sprint') {
      const pct = Math.max(0, Math.min(100, (sprintTimeLeft / sprintTotalTime) * 100));
      clockHudHtml = `
        <div class="stat-chip" style="border: 2px solid var(--op-add); color: var(--op-add); font-family: var(--font-mono);">
          ⚡ <span id="sprint-seconds">${Math.max(0, sprintTimeLeft).toFixed(1)}s</span>
        </div>
        <div style="width: 100%; height: 10px; background: var(--bg-inset); border-radius: var(--radius-pill); overflow: hidden;">
          <div id="timer-bar-fill" style="height: 100%; width: ${pct}%; background: linear-gradient(90deg, var(--op-add), var(--op-mul)); transition: width 0.1s linear;"></div>
        </div>
      `;
    }

    const html = `
      <div class="card" style="position: relative;">
        <canvas id="confetti-canvas"></canvas>
        <div class="game-header">
          <button id="btn-exit-game" class="btn-arcade">${esc(t('back_menu'))}</button>
          <div class="stat-chip">${esc(roundLabel)}</div>
          <div class="stat-chip">⭐ ${esc(t('points'))}: <strong style="font-family: var(--font-mono); margin-left: 4px;">${score}</strong></div>
          ${streak >= 2 ? `<div class="streak-badge">🔥 ${streak} ${esc(t('streak'))} (x${comboMultiplier})</div>` : ''}
          ${clockHudHtml}
        </div>

        ${renderPedagogyToolbar()}

        <div id="feedback-banner-container"></div>

        <div class="reading-stage">
          ${renderActiveStageContent()}
        </div>

        <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 12px; flex-wrap: wrap;">
          <button id="btn-toggle-hint" class="btn-arcade" style="background: var(--bg-inset);">
            ${esc(isHintVisible ? t('hide_hint') : t('visual_hint'))}
          </button>
          <button id="btn-listen-slow" class="btn-arcade" style="background: var(--bg-inset);">
            🐢 ${esc(t('listen_slow_btn'))}
          </button>
          <button id="btn-skip" class="btn-arcade" style="background: var(--bg-inset);">
            ${esc(t('skip'))}
          </button>
        </div>

        <div id="hint-container" class="${isHintVisible ? '' : 'hidden'}" style="margin-bottom: 16px;">
          ${currentChallenge ? engine.renderVisualHint(currentChallenge, lang) : ''}
        </div>
      </div>
    `;

    container.innerHTML = html;

    bindPedagogyToolbar(() => {
      if (inGame && !inFeedbackPause) {
        renderActiveGame(document.getElementById('tab-content'));
      }
    });

    const exitBtn = document.getElementById('btn-exit-game');
    if (exitBtn) {
      exitBtn.onclick = () => {
        endGameSession();
        renderPlayTab();
      };
    }

    const hintBtn = document.getElementById('btn-toggle-hint');
    if (hintBtn) hintBtn.onclick = toggleVisualHint;

    const listenSlowBtn = document.getElementById('btn-listen-slow');
    if (listenSlowBtn) {
      listenSlowBtn.onclick = () => {
        if (!currentChallenge || inFeedbackPause) return;
        hintUsedThisRound = true;
        const textToSpeak = currentChallenge.levelId === 'l1'
          ? `${currentChallenge.prompt}. ${currentChallenge.anchorWord || ''}`
          : currentChallenge.prompt;
        audio.speakText(textToSpeak, lang, 0.65);
      };
    }

    const skipBtn = document.getElementById('btn-skip');
    if (skipBtn) {
      skipBtn.onclick = () => {
        if (inFeedbackPause) return;
        const elapsed = frozenElapsedMs !== null ? frozenElapsedMs : Math.max(400, Math.round(performance.now() - roundStartMs));
        handleChallengeResult(false, true, getExpectedDisplay(), elapsed, 0, '');
      };
    }

    // Bindings específicos por nivel
    container.querySelectorAll('[data-choice-idx]').forEach(btn => {
      btn.onclick = () => {
        if (inFeedbackPause || !currentChallenge) return;
        const idx = Number(btn.getAttribute('data-choice-idx'));
        const choice = currentChallenge.choices[idx];
        if (!choice) return;
        const elapsed = Math.max(400, Math.round(performance.now() - roundStartMs));
        freezeClockOnly(elapsed);
        const evalRes = engine.evaluateChallenge(currentChallenge, choice, lang);
        handleChallengeResult(evalRes.isCorrect, false, evalRes.correctDisplay, elapsed, 0, evalRes.userDisplay);
      };
    });

    container.querySelectorAll('[data-alpha-char]').forEach(btn => {
      btn.onclick = () => {
        handleAlphaPress(btn.getAttribute('data-alpha-char'));
      };
    });

    const backspaceBtn = container.querySelector('[data-alpha-action="del"]');
    if (backspaceBtn) {
      backspaceBtn.onclick = () => handleAlphaBackspace();
    }

    container.querySelectorAll('.letter-slot[data-slot-idx]').forEach(slotEl => {
      slotEl.onclick = () => {
        if (inFeedbackPause) return;
        const sIdx = Number(slotEl.getAttribute('data-slot-idx'));
        if (filledSlots[sIdx]) {
          filledSlots[sIdx] = '';
        }
        activeSlotCursor = sIdx;
        renderActiveGame(document.getElementById('tab-content'));
      };
    });

    const readDoneBtn = document.getElementById('btn-read-done');
    if (readDoneBtn) {
      readDoneBtn.onclick = () => handleReadDone();
    }

    container.querySelectorAll('[data-mc-idx]').forEach(btn => {
      btn.onclick = () => {
        if (inFeedbackPause || !currentChallenge) return;
        const idx = Number(btn.getAttribute('data-mc-idx'));
        const evalRes = engine.evaluateChallenge(currentChallenge, { index: idx }, lang);
        const elapsed = frozenElapsedMs !== null ? frozenElapsedMs : Math.max(400, Math.round(performance.now() - roundStartMs));
        handleChallengeResult(evalRes.isCorrect, false, evalRes.correctDisplay, elapsed, frozenWpm, evalRes.userDisplay);
      };
    });
  }

  function getExpectedDisplay() {
    if (!currentChallenge) return '';
    if (currentChallenge.kind === 'read_check' && currentChallenge.microCheck) {
      const corr = (currentChallenge.microCheck.options || []).find(o => o.isCorrect);
      if (corr) return `${corr.icon || corr.emoji || ''} ${corr.label}`.trim();
    }
    return currentChallenge.prompt || '';
  }

  function toggleVisualHint() {
    isHintVisible = !isHintVisible;
    if (isHintVisible) hintUsedThisRound = true;
    const hintEl = document.getElementById('hint-container');
    const btnEl = document.getElementById('btn-toggle-hint');
    if (hintEl && btnEl) {
      if (isHintVisible) {
        hintEl.classList.remove('hidden');
        btnEl.textContent = t('hide_hint');
      } else {
        hintEl.classList.add('hidden');
        btnEl.textContent = t('visual_hint');
      }
    }
  }

  function freezeClockOnly(elapsedMs) {
    if (selectedMode !== 'sprint') {
      clearInterval(timerInterval);
    }
    frozenElapsedMs = elapsedMs;
    const isSentence = currentChallenge && (currentChallenge.levelId === 'l5' || currentChallenge.levelId === 'l6');
    frozenWpm = isSentence ? engine.computeWpm(currentChallenge.wordCount, elapsedMs) : 0;
  }

  function handleReadDone() {
    if (!inGame || inFeedbackPause || awaitingMicroCheck || !currentChallenge) return;
    audio.playClick();
    const elapsed = Math.max(400, Math.round(performance.now() - roundStartMs));
    freezeClockOnly(elapsed);
    awaitingMicroCheck = true;
    renderActiveGame(document.getElementById('tab-content'));
  }

  function handleAlphaPress(ch) {
    if (!inGame || inFeedbackPause || !currentChallenge || currentChallenge.kind !== 'fill_letters') return;
    const slotsCount = (currentChallenge.maskedSlots || []).length;
    if (slotsCount === 0) return;

    audio.playClick();
    const normChar = engine.normalizeChar(ch);
    if (!normChar) return;

    // Buscar hueco activo o el siguiente vacío
    let targetSlot = activeSlotCursor;
    if (targetSlot < 0 || targetSlot >= slotsCount || filledSlots[targetSlot]) {
      const nextEmpty = findFirstEmptySlot(slotsCount);
      if (nextEmpty === -1) return;
      targetSlot = nextEmpty;
    }

    filledSlots[targetSlot] = normChar;
    const nextEmpty = findFirstEmptySlot(slotsCount);

    if (nextEmpty === -1) {
      // Último hueco rellenado: detener cronómetro al instante y evaluar
      activeSlotCursor = slotsCount - 1;
      const elapsed = Math.max(400, Math.round(performance.now() - roundStartMs));
      freezeClockOnly(elapsed);
      renderActiveGame(document.getElementById('tab-content'));
      const evalRes = engine.evaluateChallenge(currentChallenge, filledSlots, lang);
      handleChallengeResult(evalRes.isCorrect, false, evalRes.correctDisplay, elapsed, 0, evalRes.userDisplay);
    } else {
      activeSlotCursor = nextEmpty;
      renderActiveGame(document.getElementById('tab-content'));
    }
  }

  function findFirstEmptySlot(slotsCount) {
    for (let i = 0; i < slotsCount; i++) {
      if (!filledSlots[i]) return i;
    }
    return -1;
  }

  function handleAlphaBackspace() {
    if (!inGame || inFeedbackPause || !currentChallenge || currentChallenge.kind !== 'fill_letters') return;
    audio.playClick();
    const slotsCount = (currentChallenge.maskedSlots || []).length;
    if (filledSlots[activeSlotCursor]) {
      filledSlots[activeSlotCursor] = '';
    } else {
      for (let i = slotsCount - 1; i >= 0; i--) {
        if (filledSlots[i]) {
          filledSlots[i] = '';
          activeSlotCursor = i;
          break;
        }
      }
    }
    renderActiveGame(document.getElementById('tab-content'));
  }

  function submitL3IfComplete() {
    if (!inGame || inFeedbackPause || !currentChallenge || currentChallenge.kind !== 'fill_letters') return;
    const slotsCount = (currentChallenge.maskedSlots || []).length;
    if (findFirstEmptySlot(slotsCount) !== -1) return;
    const elapsed = Math.max(400, Math.round(performance.now() - roundStartMs));
    freezeClockOnly(elapsed);
    const evalRes = engine.evaluateChallenge(currentChallenge, filledSlots, lang);
    handleChallengeResult(evalRes.isCorrect, false, evalRes.correctDisplay, elapsed, 0, evalRes.userDisplay);
  }

  function handleChallengeResult(isCorrect, isSkipped, correctDisplay, elapsedMs, roundWpm, userDisplay) {
    clearInterval(timerInterval);
    clearTimeout(feedbackTimeout);

    const bannerContainer = document.getElementById('feedback-banner-container');
    let pointsEarned = 0;
    const resolvedCorrect = correctDisplay || getExpectedDisplay();

    roundHistory.push({
      round: roundIndex,
      challenge: currentChallenge,
      isCorrect: Boolean(isCorrect),
      usedHint: hintUsedThisRound,
      skipped: Boolean(isSkipped),
      elapsedMs: elapsedMs || 0,
      wpm: isCorrect ? (roundWpm || 0) : 0,
      userDisplay: userDisplay || '',
      correctDisplay: resolvedCorrect
    });

    if (isCorrect) {
      streak += 1;
      if (streak > bestStreak) bestStreak = streak;
      correctCount += 1;

      const targetSec = getSafetyCapSec(selectedLevel);
      pointsEarned = engine.computeRoundScore({
        mode: selectedMode,
        streak,
        usedHint: hintUsedThisRound,
        elapsedMs,
        targetSec
      });
      score += pointsEarned;
      audio.playSuccess(streak);

      if (roundWpm > 0 && roundWpm > (userStats.bestWpm || 0)) {
        userStats.bestWpm = roundWpm;
        saveStats();
      }

      if (selectedMode === 'sprint' && streak > 0 && streak % 5 === 0) {
        sprintTimeLeft = Math.min(60, sprintTimeLeft + 3);
      }

      if (roundWpm >= 120) {
        unlockMedal('speed_reader');
      }

      const speedNote = roundWpm > 0
        ? ` · ${roundWpm} ${t('wpm_label')}`
        : ` (${(elapsedMs / 1000).toFixed(1)}s)`;

      if (bannerContainer) {
        bannerContainer.innerHTML = `
          <div class="feedback-banner feedback-success">
            <span>${esc(t('awesome'))} +${pointsEarned} pts${esc(speedNote)}</span>
            <span>⭐</span>
          </div>
        `;
      }
    } else {
      streak = 0;
      wrongCount += 1;
      if (!isSkipped) audio.playError();

      if (bannerContainer) {
        bannerContainer.innerHTML = `
          <div class="feedback-banner feedback-error">
            <span>${esc(t('good_try'))} ${esc(t('correct_answer_is'))} <strong>${esc(resolvedCorrect)}</strong></span>
            <button id="btn-next-fast" class="btn-arcade" style="padding: 4px 10px; font-size: 0.8rem; background: var(--bg-surface);">${esc(t('next_question_btn'))}</button>
          </div>
        `;
        const nextBtn = document.getElementById('btn-next-fast');
        if (nextBtn) {
          nextBtn.onclick = () => {
            clearTimeout(feedbackTimeout);
            advanceRound();
          };
        }
      }
    }

    checkMedalsDuringGame();
    inFeedbackPause = true;

    const pauseMs = isCorrect ? 850 : 2100;
    feedbackTimeout = setTimeout(() => {
      advanceRound();
    }, pauseMs);
  }

  function advanceRound() {
    inFeedbackPause = false;
    awaitingMicroCheck = false;
    if ((selectedMode === 'normal' || selectedMode === 'stopwatch' || selectedMode === 'daily') && roundIndex >= TOTAL_ROUNDS) {
      finishGame();
    } else if (selectedMode === 'sprint' && sprintTimeLeft <= 0) {
      finishGame();
    } else {
      nextChallenge();
    }
  }

  function startGameSession() {
    inGame = true;
    inFeedbackPause = false;
    awaitingMicroCheck = false;
    roundIndex = 0;
    score = 0;
    correctCount = 0;
    wrongCount = 0;
    streak = 0;
    bestStreak = 0;
    isHintVisible = false;
    hintUsedThisRound = false;
    roundHistory = [];
    recentIds = [];

    if (selectedMode === 'daily') {
      const dateStr = dailyDateParam || new Date().toISOString().slice(0, 10);
      dailyRng = engine.createSeededRng(`${dateStr}_${selectedLevel}`);
    } else {
      dailyRng = null;
    }

    if (selectedMode === 'sprint') {
      sprintTotalTime = 60.0;
      sprintTimeLeft = 60.0;
    }

    nextChallenge();
  }

  function nextChallenge() {
    clearInterval(timerInterval);
    clearTimeout(feedbackTimeout);

    roundIndex += 1;
    isHintVisible = false;
    hintUsedThisRound = false;
    awaitingMicroCheck = false;
    frozenElapsedMs = null;
    frozenWpm = 0;
    stopwatchElapsedMs = 0;
    filledSlots = [];
    activeSlotCursor = 0;

    const prng = (selectedMode === 'daily' && typeof dailyRng === 'function') ? dailyRng : null;
    currentChallenge = engine.generateChallenge(selectedLevel, lang, prng, recentIds);
    if (currentChallenge && currentChallenge.id) {
      recentIds.push(currentChallenge.id);
      if (recentIds.length > 10) recentIds.shift();
    }
    if (currentChallenge && Array.isArray(currentChallenge.maskedSlots)) {
      filledSlots = new Array(currentChallenge.maskedSlots.length).fill('');
    }

    roundStartMs = performance.now();
    renderActiveGame(document.getElementById('tab-content'));
    startTimer();
  }

  function startTimer() {
    clearInterval(timerInterval);
    if (selectedMode === 'normal') return;

    const safetyCapMs = getSafetyCapSec(selectedLevel) * 1000;

    timerInterval = setInterval(() => {
      if (inFeedbackPause) return;

      if (selectedMode === 'sprint') {
        sprintTimeLeft -= 0.1;
        const secEl = document.getElementById('sprint-seconds');
        if (secEl) secEl.textContent = `${Math.max(0, sprintTimeLeft).toFixed(1)}s`;
        const fillEl = document.getElementById('timer-bar-fill');
        if (fillEl) {
          fillEl.style.width = `${Math.max(0, (sprintTimeLeft / sprintTotalTime) * 100)}%`;
        }
        if (sprintTimeLeft <= 0) {
          clearInterval(timerInterval);
          finishGame();
        }
        return;
      }

      // 'stopwatch' o 'daily'
      if (frozenElapsedMs !== null) return;
      stopwatchElapsedMs = Math.max(0, performance.now() - roundStartMs);
      const dispEl = document.getElementById('stopwatch-display');
      if (dispEl) {
        dispEl.textContent = formatStopwatch(stopwatchElapsedMs);
      }

      if (selectedMode === 'stopwatch' && stopwatchElapsedMs >= safetyCapMs) {
        clearInterval(timerInterval);
        handleChallengeResult(false, false, getExpectedDisplay(), safetyCapMs, 0, '');
      }
    }, 100);
  }

  function unlockMedal(medalId) {
    if (!userStats.unlockedMedals.includes(medalId)) {
      userStats.unlockedMedals.push(medalId);
      saveStats();
      showToast(`🎖️ ${t('badge_unlocked')}`);
    }
  }

  function checkMedalsDuringGame() {
    if (streak >= 5) unlockMedal('streak_5');
    if (streak >= 10) unlockMedal('streak_10');
  }

  function checkEndOfGameMedals() {
    if (correctCount >= 1) unlockMedal('first_win');
    if ((selectedLevel === 'l3' || selectedLevel === 'l4') && wrongCount === 0 && correctCount >= 5) {
      unlockMedal('syllable_master');
    }
    if ((selectedLevel === 'l5' || selectedLevel === 'l6') && wrongCount === 0 && correctCount >= 5) {
      unlockMedal('storyteller');
    }
  }

  function finishGame() {
    clearInterval(timerInterval);
    clearTimeout(feedbackTimeout);
    inGame = false;
    inFeedbackPause = false;
    awaitingMicroCheck = false;
    audio.playWin();

    if (!userStats.highScores[selectedLevel] || score > userStats.highScores[selectedLevel]) {
      userStats.highScores[selectedLevel] = score;
    }
    if (bestStreak > userStats.bestStreakEver) {
      userStats.bestStreakEver = bestStreak;
    }
    checkEndOfGameMedals();
    saveStats();

    const container = document.getElementById('tab-content');
    if (!container) return;

    const totalPlayed = roundHistory.length || roundIndex;
    const accuracy = totalPlayed > 0 ? Math.round((correctCount / totalPlayed) * 100) : 0;

    // Estadísticas PPM de la sesión
    const wpmList = roundHistory.map(r => r.wpm).filter(w => w > 0);
    const avgWpm = wpmList.length > 0 ? Math.round(wpmList.reduce((a, b) => a + b, 0) / wpmList.length) : 0;
    const maxWpmSession = wpmList.length > 0 ? Math.max(...wpmList) : 0;

    // Tira Wordle (🟩 Acierto limpio, 💡 Acierto con pista, 🟥 Fallo)
    const emojiStrip = roundHistory.map(r => {
      if (r.isCorrect && !r.usedHint) return '🟩';
      if (r.isCorrect && r.usedHint) return '💡';
      return '🟥';
    }).join('');

    const mistakes = roundHistory.filter(r => !r.isCorrect);
    let mistakesHtml = '';
    if (mistakes.length > 0) {
      mistakesHtml = `
        <div class="mistake-review-section">
          <div class="mistake-review-title">
            <span>${esc(t('mistake_review_title'))}</span>
            <span style="font-size: 0.9rem; font-weight: 600; color: var(--text-muted);">(${mistakes.length})</span>
          </div>
          <div class="mistake-list">
            ${mistakes.map((m, idx) => `
              <div class="mistake-card">
                <div class="mistake-header" style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:6px;">
                  <span class="mistake-problem-text" style="font-weight:800; font-size:1.1rem;">${esc(m.challenge ? m.challenge.prompt : '...')}</span>
                  <span style="font-size: 0.85rem; color: var(--status-error); font-weight: 700;">${esc(t('round'))} ${m.round}</span>
                </div>
                <div class="mistake-details" style="display:flex; flex-direction:column; gap:4px; font-size:0.9rem; margin-bottom:10px;">
                  <span>${esc(t('mistake_your_answer'))} <strong>${esc(m.userDisplay || (m.skipped ? t('skip') : '⏱️'))}</strong></span>
                  <span>${esc(t('mistake_correct_answer'))} <strong style="color: var(--status-success);">${esc(m.correctDisplay)}</strong></span>
                </div>
                <div class="mistake-hint-toggle" style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
                  <button class="btn-arcade btn-mistake-audio" data-mistake-idx="${idx}" style="font-size: 0.8rem; padding: 4px 10px; background: var(--bg-surface);">
                    🐢 ${esc(t('listen_slow_btn'))}
                  </button>
                  <button class="btn-arcade btn-mistake-hint" data-mistake-idx="${idx}" style="font-size: 0.8rem; padding: 4px 10px; background: var(--bg-surface);">
                    ${esc(t('view_hint_btn'))}
                  </button>
                  <div id="mistake-hint-${idx}" class="mistake-hint-container hidden" style="width:100%;">
                    ${m.challenge ? engine.renderVisualHint(m.challenge, lang) : ''}
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    } else if (roundHistory.length > 0) {
      mistakesHtml = `
        <div class="mistake-review-section" style="text-align: center;">
          <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid var(--status-success); border-radius: var(--radius-md); padding: 14px 20px; color: #065f46; font-weight: 700;">
            ${esc(t('mistake_review_empty'))}
          </div>
        </div>
      `;
    }

    const html = `
      <div class="card text-center" style="position: relative;">
        <canvas id="confetti-canvas"></canvas>
        <div style="font-size: 4rem; margin-bottom: 12px;">🏆</div>
        <h2 style="font-size: 2rem; font-weight: 800; color: var(--text-primary);">${esc(t('game_over'))}</h2>

        <div style="display: flex; gap: 16px; justify-content: center; margin: 20px 0 12px; flex-wrap: wrap;">
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">⭐ ${esc(t('points'))}: <strong>${score}</strong></div>
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">🎯 ${esc(t('accuracy'))}: <strong>${accuracy}%</strong></div>
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">🔥 ${esc(t('best_streak'))}: <strong>${bestStreak}</strong></div>
          ${avgWpm > 0 ? `<div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">⏱️ ${esc(t('wpm_label'))}: <strong>${avgWpm} (${lang === 'es' ? 'Máx' : 'Max'} ${maxWpmSession})</strong></div>` : ''}
        </div>

        ${emojiStrip ? `
          <div class="round-blocks-strip" title="Resumen gráfico de respuestas">${emojiStrip}</div>
        ` : ''}

        <div style="display: flex; gap: 12px; justify-content: center; margin-top: 20px; flex-wrap: wrap;">
          <button id="btn-share-result" class="btn-arcade btn-share-result" style="font-size: 1.05rem; padding: 12px 22px;">
            ${esc(t('share_result_btn'))}
          </button>
          <button id="btn-again" class="btn-arcade btn-arcade-primary" style="font-size: 1.05rem; padding: 12px 22px;">
            ${esc(t('play_again'))}
          </button>
          <button id="btn-finish-diploma" class="btn-arcade btn-arcade-diploma" style="font-size: 1.05rem; padding: 12px 22px;">
            ${esc(t('download_diploma_btn'))}
          </button>
          <button id="btn-badges" class="btn-arcade" style="font-size: 1.05rem; padding: 12px 22px;">
            ${esc(t('view_achievements'))}
          </button>
        </div>

        ${mistakesHtml}
      </div>
    `;
    container.innerHTML = html;

    const canvas = document.getElementById('confetti-canvas');
    if (canvas) audio.launchConfetti(canvas);

    const againBtn = document.getElementById('btn-again');
    if (againBtn) againBtn.onclick = startGameSession;

    const diplomaBtn = document.getElementById('btn-finish-diploma');
    if (diplomaBtn) diplomaBtn.onclick = downloadReadingDiploma;

    const badgesBtn = document.getElementById('btn-badges');
    if (badgesBtn) {
      badgesBtn.onclick = () => {
        activeTab = 'achievements';
        renderAll();
      };
    }

    const shareBtn = document.getElementById('btn-share-result');
    if (shareBtn) {
      shareBtn.onclick = () => {
        audio.playClick();
        const todayStr = dailyDateParam || new Date().toISOString().slice(0, 10);
        const levelObj = catalog.levels.find(l => l.id === selectedLevel);
        const levelName = levelObj ? levelObj.name[lang] : selectedLevel;
        const modeObj = catalog.modes.find(m => m.id === selectedMode);
        const modeName = selectedMode === 'daily'
          ? `${t('daily_challenge_label')} (${todayStr})`
          : (modeObj ? modeObj.name[lang] : selectedMode);

        const shareUrl = `${window.location.origin}${window.location.pathname}?mode=${selectedMode}&level=${selectedLevel}${selectedMode === 'daily' ? '&date=' + todayStr : ''}`;
        const wpmLine = maxWpmSession > 0 ? ` | ⏱️ ${maxWpmSession} ${t('wpm_label')}` : '';
        const shareText = `Datalaria Reading · ${modeName}\n${levelName} | ⭐ ${score} pts (${correctCount}/${totalPlayed})${wpmLine}\n${emojiStrip}\n${shareUrl}`;

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(shareText)
            .then(() => showToast(t('share_result_copied')))
            .catch(() => showToast(t('share_result_copied')));
        } else {
          showToast(t('share_result_copied'));
        }
      };
    }

    container.querySelectorAll('.btn-mistake-audio').forEach(btn => {
      btn.onclick = () => {
        const idx = Number(btn.getAttribute('data-mistake-idx'));
        const item = mistakes[idx];
        if (item && item.challenge) {
          audio.speakText(item.challenge.prompt, lang, 0.65);
        }
      };
    });

    container.querySelectorAll('.btn-mistake-hint').forEach(btn => {
      btn.onclick = () => {
        const idx = btn.getAttribute('data-mistake-idx');
        const box = document.getElementById(`mistake-hint-${idx}`);
        if (box) box.classList.toggle('hidden');
      };
    });
  }

  function endGameSession() {
    clearInterval(timerInterval);
    clearTimeout(feedbackTimeout);
    inGame = false;
    inFeedbackPause = false;
    awaitingMicroCheck = false;
  }

  // ==========================================================================
  // Pestaña 2: Aprender (4 Módulos Interactivos Bilingües)
  // ==========================================================================
  function renderLearnTab() {
    const container = document.getElementById('tab-content');
    if (!container) return;

    const subTabs = [
      { id: 'letters', icon: '🔤', label: t('learn_tab_letters') },
      { id: 'direct', icon: '🧩', label: t('learn_tab_direct') },
      { id: 'complex', icon: '⚡', label: t('learn_tab_complex') },
      { id: 'sentences', icon: '📖', label: t('learn_tab_sentences') }
    ];

    let moduleContentHtml = '';
    const mods = catalog.learnModules[lang];

    if (learnSubTab === 'letters') {
      moduleContentHtml = `
        <p style="color: var(--text-secondary); margin-bottom: 12px;">
          ${lang === 'es'
            ? 'Pulsa cualquier letra para escuchar su sonido y palabra ancla.'
            : 'Tap any letter card to hear its phonics sound and anchor word.'}
        </p>
        <div class="learn-matrix-grid">
          ${(mods.letters || []).map((item, idx) => `
            <button class="phonics-card" data-speak-text="${esc(item.letter + '. ' + item.anchor)}" data-card-idx="${idx}">
              <div class="phonics-letter ${useUpperCase ? 'case-upper' : ''}">${esc(formatWordCase(item.letter))}</div>
              <div class="phonics-emoji" aria-hidden="true">${esc(item.emoji)}</div>
              <div class="phonics-anchor ${useUpperCase ? 'case-upper' : ''}">${esc(useUpperCase ? item.anchor.toUpperCase() : item.anchor)}</div>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 2px;">${esc(item.sound)}</div>
            </button>
          `).join('')}
        </div>
      `;
    } else if (learnSubTab === 'direct') {
      if (lang === 'es') {
        const list = mods.directSyllables || [];
        if (activeMixerIndex >= list.length) activeMixerIndex = 0;
        const currentGroup = list[activeMixerIndex] || { consonant: 'M', syllables: [] };

        moduleContentHtml = `
          <p style="color: var(--text-secondary); margin-bottom: 8px;">
            Elige una consonante en la Mesa de Mezclas para formar y escuchar sus sílabas directas:
          </p>
          <div class="syllable-mixer">
            <div class="mixer-consonants-row">
              ${list.map((grp, idx) => `
                <button class="mixer-pill ${idx === activeMixerIndex ? 'selected' : ''}" data-mixer-idx="${idx}">
                  ${esc(formatWordCase(grp.consonant))}
                </button>
              `).join('')}
            </div>
            <div class="learn-matrix-grid">
              ${(currentGroup.syllables || []).map(sylObj => {
                const full = String(sylObj.syllable || '');
                const consPart = formatWordCase(full.slice(0, -1));
                const vowelPart = formatWordCase(full.slice(-1));
                return `
                  <button class="phonics-card" data-speak-text="${esc(sylObj.syllable.toLowerCase() + ', ' + sylObj.word)}">
                    <div class="phonics-letter ${useUpperCase ? 'case-upper' : ''}">
                      <span class="syl-a">${esc(consPart)}</span><span class="syl-b">${esc(vowelPart)}</span>
                    </div>
                    <div class="phonics-emoji" aria-hidden="true">${esc(sylObj.emoji)}</div>
                    <div class="phonics-anchor ${useUpperCase ? 'case-upper' : ''}">${esc(useUpperCase ? sylObj.word.toUpperCase() : sylObj.word)}</div>
                  </button>
                `;
              }).join('')}
            </div>
          </div>
        `;
      } else {
        const list = mods.cvcRimes || [];
        if (activeMixerIndex >= list.length) activeMixerIndex = 0;
        const currentRime = list[activeMixerIndex] || { rime: '-AT', words: [] };

        moduleContentHtml = `
          <p style="color: var(--text-secondary); margin-bottom: 8px;">
            Select a CVC rime family in the Phonics Mixer and tap words to hear onset + rime blending:
          </p>
          <div class="syllable-mixer">
            <div class="mixer-consonants-row">
              ${list.map((grp, idx) => `
                <button class="mixer-pill ${idx === activeMixerIndex ? 'selected' : ''}" data-mixer-idx="${idx}" style="min-width: 60px; padding: 0 10px;">
                  ${esc(formatWordCase(grp.rime))}
                </button>
              `).join('')}
            </div>
            <div class="learn-matrix-grid">
              ${(currentRime.words || []).map(wObj => {
                const w = String(wObj.word || '');
                const rimeClean = String(currentRime.rime || '').replace(/^-/, '');
                const splitLen = Math.max(1, w.length - rimeClean.length);
                const onset = formatWordCase(w.slice(0, splitLen));
                const rimePart = formatWordCase(w.slice(splitLen));
                return `
                  <button class="phonics-card" data-speak-text="${esc(wObj.word)}">
                    <div class="phonics-letter ${useUpperCase ? 'case-upper' : ''}">
                      <span class="syl-a">${esc(onset)}</span><span class="syl-b">${esc(rimePart)}</span>
                    </div>
                    <div class="phonics-emoji" aria-hidden="true">${esc(wObj.emoji)}</div>
                  </button>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }
    } else if (learnSubTab === 'complex') {
      if (lang === 'es') {
        moduleContentHtml = `
          <div style="display: grid; gap: 20px;">
            <div>
              <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; color: var(--syl-complex);">🔄 Sílabas Inversas (Vocal + Consonante)</h3>
              <div class="learn-matrix-grid">
                ${(mods.inverseSyllables || []).flatMap(g => g.syllables || []).map(item => `
                  <button class="phonics-card" data-speak-text="${esc(item.syllable.toLowerCase() + ', ' + item.word)}">
                    <div class="phonics-letter syl-complex ${useUpperCase ? 'case-upper' : ''}">${esc(formatWordCase(item.syllable))}</div>
                    <div class="phonics-emoji" aria-hidden="true">${esc(item.emoji)}</div>
                    <div class="phonics-anchor">${esc(useUpperCase ? item.word.toUpperCase() : item.word)}</div>
                  </button>
                `).join('')}
              </div>
            </div>

            <div>
              <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; color: var(--op-add);">🧱 Sílabas Trabadas (Grupos Consonánticos)</h3>
              <div class="learn-matrix-grid">
                ${(mods.complexSyllables || []).map(item => `
                  <button class="phonics-card" data-speak-text="${esc(item.syllable.toLowerCase() + ', ' + item.word)}">
                    <div class="phonics-letter ${useUpperCase ? 'case-upper' : ''}" style="color: var(--op-add);">${esc(formatWordCase(item.syllable))}</div>
                    <div class="phonics-emoji" aria-hidden="true">${esc(item.emoji)}</div>
                    <div class="phonics-anchor">${esc(useUpperCase ? item.word.toUpperCase() : item.word)}</div>
                  </button>
                `).join('')}
              </div>
            </div>

            <div>
              <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; color: var(--syl-b);">💎 Dígrafos y Reglas Ortográficas</h3>
              <div style="display: grid; gap: 12px;">
                ${(mods.rulesAndDigraphs || []).map(r => `
                  <div style="background: var(--bg-elevated); border: 2px solid var(--border-card); border-radius: var(--radius-md); padding: 14px;">
                    <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom:8px;">
                      <span class="syl-complex" style="font-size:1.3rem; font-family:var(--font-mono);">${esc(formatWordCase(r.symbol))}</span>
                      <span style="font-size:0.9rem; color:var(--text-secondary); font-weight:600; flex:1;">${esc(r.rule)}</span>
                    </div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap;">
                      ${(r.words || []).map(w => `
                        <button class="btn-arcade" data-speak-text="${esc(w)}">🔊 ${esc(useUpperCase ? w.toUpperCase() : w)}</button>
                      `).join('')}
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        `;
      } else {
        moduleContentHtml = `
          <div style="display: grid; gap: 20px;">
            <div>
              <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; color: var(--op-add);">🧱 Consonant Blends</h3>
              <div class="learn-matrix-grid">
                ${(mods.blends || []).map(item => `
                  <button class="phonics-card" data-speak-text="${esc(item.word)}">
                    <div class="phonics-letter ${useUpperCase ? 'case-upper' : ''}">${esc(formatWordCase(item.blend))}</div>
                    <div class="phonics-emoji" aria-hidden="true">${esc(item.emoji)}</div>
                    <div class="phonics-anchor">${esc(useUpperCase ? item.word.toUpperCase() : item.word)}</div>
                  </button>
                `).join('')}
              </div>
            </div>

            <div>
              <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; color: var(--syl-complex);">💎 Digraphs</h3>
              <div class="learn-matrix-grid">
                ${(mods.digraphs || []).map(item => `
                  <button class="phonics-card" data-speak-text="${esc(item.word)}">
                    <div class="phonics-letter syl-complex ${useUpperCase ? 'case-upper' : ''}">${esc(formatWordCase(item.digraph))}</div>
                    <div class="phonics-emoji" aria-hidden="true">${esc(item.emoji)}</div>
                    <div class="phonics-anchor">${esc(useUpperCase ? item.word.toUpperCase() : item.word)}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">${esc(item.sound)}</div>
                  </button>
                `).join('')}
              </div>
            </div>

            <div>
              <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 8px; color: var(--syl-b);">✨ Vowel Teams & Magic-E</h3>
              <div class="learn-matrix-grid">
                ${(mods.vowelTeams || []).map(item => `
                  <button class="phonics-card" data-speak-text="${esc(item.word)}">
                    <div class="phonics-letter syl-b ${useUpperCase ? 'case-upper' : ''}">${esc(formatWordCase(item.pattern))}</div>
                    <div class="phonics-emoji" aria-hidden="true">${esc(item.emoji)}</div>
                    <div class="phonics-anchor">${esc(useUpperCase ? item.word.toUpperCase() : item.word)}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">${esc(item.sound)}</div>
                  </button>
                `).join('')}
              </div>
            </div>
          </div>
        `;
      }
    } else {
      // Taller de Frases
      moduleContentHtml = `
        <p style="color: var(--text-secondary); margin-bottom: 14px;">
          ${lang === 'es'
            ? 'Escucha cómo cambian las pausas y el tono con los signos de puntuación en voz normal o tortuga.'
            : 'Hear how punctuation marks guide breathing pauses and intonation at normal or turtle speed.'}
        </p>
        <div style="display: grid; gap: 16px;">
          ${(mods.sentenceWorkshop || []).map((item, idx) => `
            <div style="border: 2px solid var(--border-card); border-radius: var(--radius-md); padding: 18px; background: var(--bg-elevated);">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
                <strong style="font-size:1.15rem; color:var(--op-add);">${esc(item.sign)}</strong>
                <span style="font-size:0.9rem; color:var(--text-secondary); font-weight:600;">${esc(item.tip)}</span>
              </div>
              <div class="reading-sentence-lines ${useUpperCase ? 'case-upper' : ''}" style="font-size:1.25rem; text-align:left; margin: 10px 0;">
                ${esc(formatSentenceCase(item.example))}
              </div>
              <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:12px;">
                <button class="btn-arcade btn-arcade-primary btn-workshop-speak" data-rate="1.0" data-ws-idx="${idx}">
                  🔊 ${esc(t('listen_btn'))} (1.0x)
                </button>
                <button class="btn-arcade btn-workshop-speak" data-rate="0.65" data-ws-idx="${idx}">
                  🐢 ${esc(t('listen_slow_btn'))} (0.65x)
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    const html = `
      <div class="card">
        <h2 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">
          💡 ${lang === 'es' ? 'Laboratorio Fonético y Silabario' : 'Interactive Phonics & Reading Lab'}
        </h2>

        <div class="pedagogy-toolbar">
          <button id="btn-learn-case" class="pedagogy-toggle-btn ${useUpperCase ? 'active' : ''}">
            ${useUpperCase ? 'AA MAYÚS' : 'Aa minús'}
          </button>
          <button id="btn-learn-speed-normal" class="pedagogy-toggle-btn ${!learnSlowMode ? 'active' : ''}">
            🔊 1.0x ${lang === 'es' ? 'Normal' : 'Normal'}
          </button>
          <button id="btn-learn-speed-slow" class="pedagogy-toggle-btn ${learnSlowMode ? 'active' : ''}">
            🐢 0.65x ${lang === 'es' ? 'Despacio' : 'Turtle'}
          </button>
        </div>

        <div class="learn-subtabs">
          ${subTabs.map(st => `
            <button class="learn-subtab-btn ${learnSubTab === st.id ? 'active' : ''}" data-learn-sub="${esc(st.id)}">
              ${esc(st.icon)} ${esc(st.label)}
            </button>
          `).join('')}
        </div>

        ${moduleContentHtml}
      </div>
    `;

    container.innerHTML = html;

    const caseBtn = document.getElementById('btn-learn-case');
    if (caseBtn) {
      caseBtn.onclick = () => {
        audio.playClick();
        useUpperCase = !useUpperCase;
        try { localStorage.setItem('reading-case', useUpperCase ? 'upper' : 'lower'); } catch { /* */ }
        renderLearnTab();
      };
    }

    const normalSpeedBtn = document.getElementById('btn-learn-speed-normal');
    if (normalSpeedBtn) {
      normalSpeedBtn.onclick = () => {
        audio.playClick();
        learnSlowMode = false;
        renderLearnTab();
      };
    }

    const slowSpeedBtn = document.getElementById('btn-learn-speed-slow');
    if (slowSpeedBtn) {
      slowSpeedBtn.onclick = () => {
        audio.playClick();
        learnSlowMode = true;
        renderLearnTab();
      };
    }

    container.querySelectorAll('[data-learn-sub]').forEach(btn => {
      btn.onclick = () => {
        audio.playClick();
        learnSubTab = btn.getAttribute('data-learn-sub');
        renderLearnTab();
      };
    });

    container.querySelectorAll('[data-mixer-idx]').forEach(btn => {
      btn.onclick = () => {
        audio.playClick();
        activeMixerIndex = Number(btn.getAttribute('data-mixer-idx')) || 0;
        renderLearnTab();
      };
    });

    container.querySelectorAll('[data-speak-text]').forEach(btn => {
      btn.onclick = () => {
        audio.playClick();
        const text = btn.getAttribute('data-speak-text');
        audio.speakText(text, lang, learnSlowMode ? 0.65 : 1.0);
      };
    });

    container.querySelectorAll('.btn-workshop-speak').forEach(btn => {
      btn.onclick = () => {
        const idx = Number(btn.getAttribute('data-ws-idx'));
        const rate = Number(btn.getAttribute('data-rate')) || 1.0;
        const item = (mods.sentenceWorkshop || [])[idx];
        if (item) {
          audio.speakText(item.example, lang, rate);
        }
      };
    });
  }

  // ==========================================================================
  // Pestaña 3: Logros y Diploma PNG
  // ==========================================================================
  function renderAchievementsTab() {
    const container = document.getElementById('tab-content');
    if (!container) return;

    let maxScore = 0;
    Object.values(userStats.highScores || {}).forEach(s => {
      if (s > maxScore) maxScore = s;
    });

    const html = `
      <div class="card">
        <h2 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">🏆 ${esc(t('tab_achievements'))}</h2>
        <p style="color: var(--text-secondary); margin-bottom: 16px;">
          ${lang === 'es'
            ? 'Desbloquea medallas superando niveles, rachas y marcas de velocidad lectora (PPM).'
            : 'Unlock badges by conquering levels, streaks and reading fluency milestones (WPM).'}
        </p>

        <div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:20px;">
          <div class="stat-chip">⭐ ${lang === 'es' ? 'Récord Máximo' : 'High Score'}: <strong>${maxScore} pts</strong></div>
          <div class="stat-chip">⏱️ ${lang === 'es' ? 'Récord' : 'Best'} ${esc(t('wpm_label'))}: <strong>${userStats.bestWpm || 0} ${esc(t('wpm_label'))}</strong></div>
          <div class="stat-chip">🔥 ${esc(t('best_streak'))}: <strong>${userStats.bestStreakEver || 0}</strong></div>
        </div>

        <div class="medals-grid">
          ${catalog.medals.map(m => {
            const isUnlocked = userStats.unlockedMedals.includes(m.id);
            return `
              <div class="medal-card ${isUnlocked ? 'unlocked' : 'locked'}">
                <div class="medal-icon">${esc(m.icon)}</div>
                <strong style="display: block; font-size: 1.1rem; margin-bottom: 4px;">${esc(m.name[lang])}</strong>
                <span style="font-size: 0.85rem; color: var(--text-secondary);">${esc(m.desc[lang])}</span>
                <div style="margin-top: 10px; font-size: 0.8rem; font-weight: 700; color: ${isUnlocked ? 'var(--status-success)' : 'var(--text-muted)'};">
                  ${isUnlocked ? (lang === 'es' ? '✓ Desbloqueada' : '✓ Unlocked') : (lang === 'es' ? '🔒 Bloqueada' : '🔒 Locked')}
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div class="diploma-promo-card">
          <div style="font-size: 2.4rem; margin-bottom: 6px;">🎓</div>
          <h3 style="font-size: 1.3rem; font-weight: 800; color: #b45309; margin-bottom: 6px;">${esc(t('diploma_card_title'))}</h3>
          <p style="font-size: 0.95rem; color: var(--text-secondary); max-width: 520px; margin: 0 auto 16px;">
            ${esc(t('diploma_card_desc'))}
          </p>
          <button id="btn-download-diploma" class="btn-arcade btn-arcade-diploma" style="font-size: 1.05rem; padding: 10px 24px;">
            ${esc(t('download_diploma_btn'))}
          </button>
        </div>

        <div style="text-align: center; margin-top: 30px;">
          <button id="btn-reset-stats" class="btn-arcade btn-arcade-danger" style="font-size: 0.85rem;">
            ${esc(t('clean_history'))}
          </button>
        </div>
      </div>
    `;

    container.innerHTML = html;

    const diplomaBtn = document.getElementById('btn-download-diploma');
    if (diplomaBtn) diplomaBtn.onclick = downloadReadingDiploma;

    const resetBtn = document.getElementById('btn-reset-stats');
    if (resetBtn) {
      resetBtn.onclick = () => {
        userStats = createEmptyStats();
        saveStats();
        showToast(t('stats_reset_toast'));
        renderAchievementsTab();
      };
    }
  }

  // ==========================================================================
  // Generador de Diploma Arcade PNG en Canvas 2D (INV-READ-11)
  // ==========================================================================
  function downloadReadingDiploma() {
    audio.playSuccess(3);
    showToast(t('diploma_downloaded_toast'), 3000);

    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 800;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // 1. Fondo pergamino / marfil
    ctx.fillStyle = '#fdfbf7';
    ctx.fillRect(0, 0, 1200, 800);

    const bgGrad = ctx.createLinearGradient(0, 0, 1200, 800);
    bgGrad.addColorStop(0, 'rgba(254, 243, 199, 0.35)');
    bgGrad.addColorStop(0.5, 'rgba(255, 255, 255, 0.15)');
    bgGrad.addColorStop(1, 'rgba(219, 234, 254, 0.35)');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, 1200, 800);

    // 2. Orla Dorada Doble
    ctx.strokeStyle = '#d97706';
    ctx.lineWidth = 8;
    ctx.strokeRect(30, 30, 1140, 740);

    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 3;
    ctx.strokeRect(42, 42, 1116, 716);

    const corners = [[30, 30], [1170, 30], [30, 770], [1170, 770]];
    ctx.fillStyle = '#b45309';
    corners.forEach(([cx, cy]) => {
      ctx.beginPath();
      ctx.arc(cx, cy, 14, 0, Math.PI * 2);
      ctx.fill();
    });

    // 3. Encabezados Institucionales
    ctx.textAlign = 'center';
    ctx.fillStyle = '#0284c7';
    ctx.font = 'bold 22px system-ui, -apple-system, sans-serif';
    ctx.fillText(
      lang === 'es'
        ? 'DATALARIA LECTOR ARCADE • ACADEMIA DE LECTURA'
        : 'DATALARIA READER ARCADE • LITERACY ACADEMY',
      600,
      95
    );

    ctx.fillStyle = '#1e1b4b';
    ctx.font = '800 48px system-ui, -apple-system, sans-serif';
    ctx.fillText(lang === 'es' ? 'DIPLOMA DE HONOR' : 'DIPLOMA OF HONOR', 600, 160);

    ctx.fillStyle = '#64748b';
    ctx.font = '600 20px system-ui, -apple-system, sans-serif';
    ctx.fillText(
      lang === 'es'
        ? 'En reconocimiento a su progreso en conciencia fonológica, comprensión y fluidez lectora'
        : 'In recognition of outstanding phonological awareness, comprehension and reading fluency',
      600,
      202
    );

    // 4. Perfil Activo
    const profileObj = catalog.profiles ? catalog.profiles.find(p => p.id === activeProfileId) : null;
    const profileAvatar = profileObj ? profileObj.avatar : '🦁';
    const profileName = profileObj ? profileObj.name[lang] : 'Jugador 1';
    const profileTitle = profileObj ? profileObj.title[lang] : 'León Lector';

    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 2;
    ctx.beginPath();
    if (typeof ctx.roundRect === 'function') {
      ctx.roundRect(260, 235, 680, 135, 16);
    } else {
      ctx.rect(260, 235, 680, 135);
    }
    ctx.fill();
    ctx.stroke();

    ctx.font = '64px system-ui, sans-serif';
    ctx.fillText(profileAvatar, 335, 325);

    ctx.textAlign = 'left';
    ctx.fillStyle = '#1e1b4b';
    ctx.font = '800 36px system-ui, -apple-system, sans-serif';
    ctx.fillText(profileName, 400, 295);

    ctx.fillStyle = '#0284c7';
    ctx.font = '700 20px system-ui, -apple-system, sans-serif';
    ctx.fillText(`★ ${profileTitle}`, 400, 332);

    // 5. KPIs de Fluidez Lectora
    let maxScore = 0;
    Object.values(userStats.highScores || {}).forEach(s => {
      if (s > maxScore) maxScore = s;
    });

    ctx.textAlign = 'center';
    const statBoxes = [
      { label: lang === 'es' ? 'Récord Máximo' : 'High Score', val: `${maxScore} pts` },
      { label: lang === 'es' ? 'Récord PPM' : 'Best WPM', val: `⏱️ ${userStats.bestWpm || 0} ${t('wpm_label')}` },
      { label: lang === 'es' ? 'Mejor Racha' : 'Best Streak', val: `🔥 ${userStats.bestStreakEver || 0}` }
    ];

    statBoxes.forEach((st, i) => {
      const bx = 260 + i * 280;
      ctx.fillStyle = '#f8faff';
      ctx.strokeStyle = '#cbd5e1';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      if (typeof ctx.roundRect === 'function') {
        ctx.roundRect(bx - 120, 400, 240, 85, 12);
      } else {
        ctx.rect(bx - 120, 400, 240, 85);
      }
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#64748b';
      ctx.font = '600 14px system-ui, sans-serif';
      ctx.fillText(st.label, bx, 432);

      ctx.fillStyle = '#0f172a';
      ctx.font = '800 22px system-ui, sans-serif';
      ctx.fillText(st.val, bx, 465);
    });

    // 6. Fila de Medallas
    ctx.fillStyle = '#475569';
    ctx.font = '700 16px system-ui, sans-serif';
    ctx.fillText(
      lang === 'es'
        ? `COLECCIÓN DE MEDALLAS (${userStats.unlockedMedals.length}/${catalog.medals.length}):`
        : `EARNED BADGES (${userStats.unlockedMedals.length}/${catalog.medals.length}):`,
      600,
      525
    );

    const medalIcons = catalog.medals.map(m => {
      return userStats.unlockedMedals.includes(m.id) ? m.icon : '⚪';
    }).join('   ');
    ctx.font = '36px system-ui, sans-serif';
    ctx.fillText(medalIcons, 600, 575);

    // 7. Sello Circular Oficial
    ctx.save();
    ctx.translate(990, 660);
    ctx.strokeStyle = '#d97706';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 0, 54, 0, Math.PI * 2);
    ctx.stroke();

    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(0, 0, 48, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = '#b45309';
    ctx.font = 'bold 9px system-ui, sans-serif';
    ctx.fillText('DATALARIA VERIFIED', 0, -20);
    ctx.font = '18px system-ui, sans-serif';
    ctx.fillText('★ 📖 ★', 0, 4);
    ctx.font = 'bold 9px system-ui, sans-serif';
    ctx.fillText('EXCELENCIA ARCADE', 0, 22);
    ctx.font = 'bold 8px system-ui, sans-serif';
    ctx.fillText('2026', 0, 34);
    ctx.restore();

    // 8. Fecha y Firma
    ctx.textAlign = 'left';
    const nowStr = new Date().toLocaleDateString(lang === 'es' ? 'es-ES' : 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    ctx.fillStyle = '#64748b';
    ctx.font = '600 15px system-ui, sans-serif';
    ctx.fillText((lang === 'es' ? 'Fecha de Expedición: ' : 'Issued on: ') + nowStr, 90, 680);
    ctx.fillText('Certificado Digital Client-Side (Datalaria SDD)', 90, 705);

    ctx.textAlign = 'center';
    ctx.fillStyle = '#334155';
    ctx.font = 'italic 16px serif';
    ctx.fillText('Datalaria Engineering & Literacy Team', 580, 685);
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(430, 695);
    ctx.lineTo(730, 695);
    ctx.stroke();
    ctx.font = '600 12px system-ui, sans-serif';
    ctx.fillStyle = '#64748b';
    ctx.fillText(lang === 'es' ? 'Firma Institucional Acreditada' : 'Accredited Institutional Signature', 580, 715);

    // 9. Descarga PNG
    try {
      const dataUrl = canvas.toDataURL('image/png');
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = `diploma_lector_arcade_${activeProfileId}_${new Date().toISOString().slice(0, 10)}.png`;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => {
        document.body.removeChild(a);
      }, 300);
    } catch {
      showToast(lang === 'es' ? 'Error al exportar diploma PNG' : 'Failed to export PNG diploma', 2500);
    }
  }

  window.downloadReadingDiploma = downloadReadingDiploma;

  // ==========================================================================
  // Sonido, Tema y PWA (INV-READ-8, INV-READ-9)
  // ==========================================================================
  function toggleAudio() {
    const enabled = audio.toggleSound();
    try { localStorage.setItem('reading-sound', enabled ? 'true' : 'false'); } catch { /* */ }
    const btn = document.getElementById('sound-btn');
    if (btn) btn.textContent = enabled ? '🔊' : '🔇';
    showToast(enabled ? (lang === 'es' ? '🔊 Audio activado' : '🔊 Sound ON') : (lang === 'es' ? '🔇 Audio silenciado' : '🔇 Sound OFF'), 1500);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('pref-theme', next); } catch { /* */ }
    showToast(next === 'dark' ? '🌙 Cosmic Night' : '☀️ Daylight Arcade', 1500);
  }

  function setupPwa() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredInstallPrompt = e;
      const btn = document.getElementById('btn-install-pwa');
      if (btn && !isStandalone) btn.style.display = 'inline-flex';
    });

    window.addEventListener('appinstalled', () => {
      deferredInstallPrompt = null;
      isStandalone = true;
      const btn = document.getElementById('btn-install-pwa');
      if (btn) btn.style.display = 'none';
      showToast(t('install_success'));
    });

    const installBtn = document.getElementById('btn-install-pwa');
    if (installBtn) {
      installBtn.onclick = () => {
        if (deferredInstallPrompt) {
          try {
            deferredInstallPrompt.prompt();
            deferredInstallPrompt.userChoice.then((choice) => {
              if (choice && choice.outcome === 'accepted') {
                showToast(t('install_success'));
              }
              deferredInstallPrompt = null;
            }).catch(() => { /* */ });
          } catch { /* */ }
        } else {
          const isIos = /iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase()) && !window.MSStream;
          showToast(isIos ? t('install_ios_tip') : t('install_generic_tip'), 4000);
        }
      };
    }

    const checkUpdateBtn = document.getElementById('btn-check-update');
    if (checkUpdateBtn) {
      checkUpdateBtn.onclick = () => checkForUpdatesManual();
    }

    if ('serviceWorker' in navigator && (window.location.protocol.startsWith('http') || window.location.protocol.startsWith('https'))) {
      const registerSw = () => {
        const hadController = Boolean(navigator.serviceWorker.controller);
        navigator.serviceWorker.register('/apps/reading/sw.js').then((reg) => {
          swRegistration = reg;
          setupPwaUpdateFlow(reg);
        }).catch(() => { /* */ });

        navigator.serviceWorker.addEventListener('controllerchange', () => {
          if (hadController && !swRefreshing) {
            swRefreshing = true;
            window.location.reload();
          }
        });
      };

      if (document.readyState === 'complete') {
        registerSw();
      } else {
        window.addEventListener('load', registerSw);
      }

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible' && swRegistration) {
          swRegistration.update().catch(() => { /* */ });
        }
      });
    }
  }

  function setupPwaUpdateFlow(registration) {
    if (!registration) return;

    if (registration.waiting && navigator.serviceWorker.controller) {
      showUpdateBanner(registration.waiting);
      return;
    }

    registration.addEventListener('updatefound', () => {
      const newWorker = registration.installing;
      if (!newWorker) return;

      newWorker.addEventListener('statechange', () => {
        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
          showUpdateBanner(newWorker);
        }
      });
    });
  }

  function showUpdateBanner(waitingWorker) {
    if (document.getElementById('pwa-update-banner')) return;

    const banner = document.createElement('div');
    banner.id = 'pwa-update-banner';
    banner.className = 'pwa-update-banner';
    banner.innerHTML = `
      <div class="update-banner-content">
        <span class="update-icon">⚡</span>
        <span class="update-text">${esc(t('update_available'))}</span>
      </div>
      <button id="btn-pwa-apply-update" class="btn-pwa-update-action" title="${esc(t('update_now_btn'))}">
        <span>🔄</span> <span>${esc(t('update_now_btn'))}</span>
      </button>
    `;

    document.body.appendChild(banner);

    const btn = banner.querySelector('#btn-pwa-apply-update');
    if (btn) {
      btn.addEventListener('click', () => {
        btn.disabled = true;
        btn.innerHTML = '<span>⏳</span> <span>...</span>';
        if (waitingWorker) {
          waitingWorker.postMessage({ action: 'skipWaiting' });
        }
        setTimeout(() => {
          window.location.reload();
        }, 1200);
      });
    }
  }

  async function checkForUpdatesManual() {
    showToast(`🔍 ${t('checking_update')}`, 1800);

    if (!swRegistration) {
      setTimeout(() => {
        showToast(t('up_to_date'), 3000);
      }, 800);
      return;
    }

    if (swRegistration.waiting) {
      showUpdateBanner(swRegistration.waiting);
      return;
    }

    try {
      await swRegistration.update();
      setTimeout(() => {
        if (!swRegistration.waiting && !document.getElementById('pwa-update-banner')) {
          showToast(t('up_to_date'), 3000);
        }
      }, 1500);
    } catch {
      showToast(t('up_to_date'), 3000);
    }
  }

  // ==========================================================================
  // Soporte de Teclado Físico y Atajos (T, M, H, Espacio/Enter, A-Z/Ñ/Backspace)
  // ==========================================================================
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    const isFillingLetters = inGame && activeTab === 'play' && !inFeedbackPause && currentChallenge && currentChallenge.kind === 'fill_letters';

    // Entrada alfabética física en Nivel 3 (Letras Faltantes)
    if (isFillingLetters) {
      if (e.key === 'Backspace') {
        e.preventDefault();
        handleAlphaBackspace();
        return;
      }
      if (e.key === 'Enter') {
        e.preventDefault();
        submitL3IfComplete();
        return;
      }
      if (e.key && e.key.length === 1 && /^[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ]$/.test(e.key)) {
        e.preventDefault();
        handleAlphaPress(e.key);
        return;
      }
    }

    // Atajos globales fuera de escritura en Nivel 3
    if (e.key === 't' || e.key === 'T') {
      toggleTheme();
      return;
    }
    if (e.key === 'm' || e.key === 'M') {
      toggleAudio();
      return;
    }
    if ((e.key === 'h' || e.key === 'H') && inGame && activeTab === 'play') {
      toggleVisualHint();
      return;
    }

    // Espacio o Enter para confirmar lectura ("¡Leído!") en l4, l5, l6
    if (inGame && activeTab === 'play' && !inFeedbackPause && currentChallenge && currentChallenge.kind === 'read_check' && !awaitingMicroCheck) {
      const targetIsButton = e.target && e.target.tagName === 'BUTTON';
      if (e.code === 'Space' || e.key === ' ' || e.key === 'Enter') {
        if (!targetIsButton || e.code === 'Space') {
          e.preventDefault();
          handleReadDone();
        }
      }
    }
  });

  // ==========================================================================
  // Inicialización Global
  // ==========================================================================
  window.addEventListener('DOMContentLoaded', () => {
    initLang();
    loadStats();
    setupPwa();

    const langBtn = document.getElementById('lang-btn');
    if (langBtn) {
      langBtn.onclick = () => {
        lang = lang === 'es' ? 'en' : 'es';
        const url = new URL(window.location);
        url.searchParams.set('lang', lang);
        window.history.replaceState({}, '', url);
        if (inGame) {
          endGameSession();
        }
        renderAll();
      };
    }

    const soundBtn = document.getElementById('sound-btn');
    if (soundBtn) soundBtn.onclick = toggleAudio;

    const themeBtn = document.getElementById('theme-btn');
    if (themeBtn) themeBtn.onclick = toggleTheme;

    renderAll();
  });
})();
