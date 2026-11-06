// apps/flashcards/app.js
// Controlador SPA Reactivo, LocalStorage, Atajos y PWA
// Datalaria Flashcards AI ("Mazo Mágico v2.0")

import { PRESET_DECKS, STUDY_MODES, MEDALS, I18N } from './catalog.js';
import { parseCSV, exportCSV, generateQuizOptions, validateSpelling, getSpellingMask, calculateDeckMastery } from './engine.js';
import { generateBatchDeckWithGemini } from './ai.js';
import { soundController, triggerConfetti } from './audio.js';

class FlashcardsApp {
  constructor() {
    this.currentLang = this.detectLanguage();
    this.activeTab = 'study'; // 'study' | 'creator' | 'stats'
    this.selectedDeckId = 'body_science';
    this.selectedModeId = 'flip'; // 'flip' | 'quiz' | 'spelling'

    this.customDecks = this.loadCustomDecks();
    this.masteryData = this.loadMasteryData(); // { [deckId]: { [cardFront]: 'repeat'|'good'|'mastered' } }
    this.unlockedMedals = this.loadUnlockedMedals(); // ['first_session', ...]
    this.stats = this.loadStats(); // { sessions: 0, totalMastered: 0 }

    this.activeDeck = null;
    this.sessionCards = [];
    this.currentIndex = 0;
    this.isFlipped = false;
    this.revealedHintCount = 0;
    this.currentStreak = 0;
    this.sessionScore = 0;
    this.failedCards = [];
    this.quizSelected = false;

    this.isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
    this.swRegistration = null;
    this.swRefreshing = false;
    this.deferredPrompt = null;
    this.initPwa();
  }

  detectLanguage() {
    const urlParams = new URLSearchParams(window.location.search);
    const langParam = urlParams.get('lang');
    if (langParam === 'es' || langParam === 'en') return langParam;
    const saved = localStorage.getItem('pref-lang');
    if (saved === 'es' || saved === 'en') return saved;
    const nav = navigator.language || navigator.userLanguage || 'es';
    return nav.startsWith('en') ? 'en' : 'es';
  }

  t(key, params = {}) {
    const dict = I18N[this.currentLang] || I18N.es;
    let str = dict[key] || I18N.es[key] || key;
    for (const [k, v] of Object.entries(params)) {
      str = str.replace(new RegExp(`\\{${k}\\}`, 'g'), v);
    }
    return str;
  }

  loadCustomDecks() {
    try {
      const data = localStorage.getItem('flashcards-custom-decks');
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  }

  saveCustomDecks() {
    try {
      localStorage.setItem('flashcards-custom-decks', JSON.stringify(this.customDecks));
    } catch {}
  }

  loadMasteryData() {
    try {
      const data = localStorage.getItem('flashcards-mastery');
      return data ? JSON.parse(data) : {};
    } catch {
      return {};
    }
  }

  saveMasteryData() {
    try {
      localStorage.setItem('flashcards-mastery', JSON.stringify(this.masteryData));
    } catch {}
  }

  loadUnlockedMedals() {
    try {
      const data = localStorage.getItem('flashcards-medals');
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  }

  saveUnlockedMedals() {
    try {
      localStorage.setItem('flashcards-medals', JSON.stringify(this.unlockedMedals));
    } catch {}
  }

  loadStats() {
    try {
      const data = localStorage.getItem('flashcards-stats');
      return data ? JSON.parse(data) : { sessions: 0, totalMastered: 0 };
    } catch {
      return { sessions: 0, totalMastered: 0 };
    }
  }

  saveStats() {
    try {
      localStorage.setItem('flashcards-stats', JSON.stringify(this.stats));
    } catch {}
  }

  unlockMedal(medalId) {
    if (!this.unlockedMedals.includes(medalId)) {
      this.unlockedMedals.push(medalId);
      this.saveUnlockedMedals();
      soundController.playTone('mastered');
      const medal = MEDALS.find(m => m.id === medalId);
      if (medal) {
        const title = (medal.title && medal.title[this.currentLang]) || medal.title.es;
        this.showToast(`🏆 ¡${title}!`, 3500);
      }
    }
  }

  showToast(msg, duration = 3000) {
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

  getAllDecks() {
    return [...PRESET_DECKS, ...this.customDecks];
  }

  getDeckById(id) {
    return this.getAllDecks().find(d => d.id === id) || PRESET_DECKS[0];
  }

  init() {
    this.initTheme();
    this.renderHeader();
    this.renderNavTabs();
    this.renderView();
    this.bindGlobalEvents();
  }

  initTheme() {
    const saved = localStorage.getItem('pref-theme') ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', saved);
  }

  toggleTheme() {
    const cur = document.documentElement.getAttribute('data-theme') || 'light';
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('pref-theme', next);
    this.renderHeader();
  }

  toggleLang() {
    this.currentLang = this.currentLang === 'es' ? 'en' : 'es';
    localStorage.setItem('pref-lang', this.currentLang);
    const url = new URL(window.location);
    url.searchParams.set('lang', this.currentLang);
    window.history.replaceState({}, '', url);
    this.renderHeader();
    this.renderNavTabs();
    this.renderView();
  }

  initPwa() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      const btn = document.getElementById('btn-install-pwa');
      if (btn && !this.isStandalone) btn.style.display = 'inline-flex';
    });

    window.addEventListener('appinstalled', () => {
      this.deferredPrompt = null;
      this.isStandalone = true;
      const btn = document.getElementById('btn-install-pwa');
      if (btn) btn.style.display = 'none';
      this.showToast(this.t('installSuccessToast'));
    });

    if ('serviceWorker' in navigator && (window.location.protocol.startsWith('http') || window.location.protocol.startsWith('https'))) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').then((reg) => {
          this.swRegistration = reg;
          this.setupPwaUpdateFlow(reg);
        }).catch(() => {});

        navigator.serviceWorker.addEventListener('controllerchange', () => {
          if (!this.swRefreshing) {
            this.swRefreshing = true;
            window.location.reload();
          }
        });
      });

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible' && this.swRegistration) {
          this.swRegistration.update().catch(() => {});
        }
      });
    }
  }

  setupPwaUpdateFlow(registration) {
    if (!registration) return;

    if (registration.waiting && navigator.serviceWorker.controller) {
      this.showUpdateBanner(registration.waiting);
      return;
    }

    registration.addEventListener('updatefound', () => {
      const newWorker = registration.installing;
      if (!newWorker) return;

      newWorker.addEventListener('statechange', () => {
        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
          this.showUpdateBanner(newWorker);
        }
      });
    });
  }

  showUpdateBanner(waitingWorker) {
    if (document.getElementById('pwa-update-banner')) return;

    const banner = document.createElement('div');
    banner.id = 'pwa-update-banner';
    banner.className = 'pwa-update-banner';
    banner.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.5rem;">
        <span>⚡</span>
        <span>${this.t('updateAvailable')}</span>
      </div>
      <button id="btn-pwa-apply-update" class="btn-pwa-update-action" title="${this.t('updateNowBtn')}">
        🔄 ${this.t('updateNowBtn')}
      </button>
    `;

    document.body.appendChild(banner);

    const btn = banner.querySelector('#btn-pwa-apply-update');
    if (btn) {
      btn.addEventListener('click', () => {
        btn.disabled = true;
        btn.innerHTML = `⏳ ...`;
        if (waitingWorker) {
          waitingWorker.postMessage({ action: 'skipWaiting' });
        }
        setTimeout(() => {
          window.location.reload();
        }, 1200);
      });
    }
  }

  async checkForUpdatesManual() {
    this.showToast(`🔍 ${this.t('checkingUpdate')}`, 1800);

    if (!this.swRegistration) {
      setTimeout(() => {
        this.showToast(this.t('upToDate'), 3000);
      }, 800);
      return;
    }

    if (this.swRegistration.waiting) {
      this.showUpdateBanner(this.swRegistration.waiting);
      return;
    }

    try {
      await this.swRegistration.update();
      setTimeout(() => {
        if (!this.swRegistration.waiting && !document.getElementById('pwa-update-banner')) {
          this.showToast(this.t('upToDate'), 3000);
        }
      }, 1500);
    } catch {
      this.showToast(this.t('upToDate'), 3000);
    }
  }

  renderHeader() {
    const header = document.getElementById('app-header');
    if (!header) return;

    const theme = document.documentElement.getAttribute('data-theme') || 'light';
    const themeIcon = theme === 'dark' ? '☀️' : '🌙';
    const soundIcon = soundController.soundEnabled ? '🔊' : '🔇';
    const portalUrl = `/${this.currentLang}/apps/`;
    const specUrl = `/${this.currentLang}/apps/flashcards/`;
    const postUrl = `/${this.currentLang}/posts/app_flashcards/`;
    const kitsUrl = this.currentLang === 'en' ? '/en/resources/' : '/es/recursos/';

    header.innerHTML = `
      <div class="brand-section">
        <a href="${portalUrl}" class="btn-back">${this.t('backDatalaria')}</a>
        <div class="brand-title">
          <span>🎴</span> ${this.t('appTitle')}
          <button id="btn-check-update" class="badge-version" title="${this.t('badgeCheckTitle')}">v2.1.0</button>
        </div>
      </div>
      <div class="header-controls">
        <button id="btn-theme-toggle" class="ctrl-btn" title="Tema (T)">${themeIcon}</button>
        <button id="btn-sound-toggle" class="ctrl-btn" title="Sonido (M)">${soundIcon}</button>
        <button id="btn-lang-toggle" class="ctrl-btn" title="Idioma"><strong>${this.currentLang.toUpperCase()}</strong></button>
        <button id="btn-install-pwa" class="ctrl-btn ctrl-btn-accent" style="display: ${this.isStandalone ? 'none' : 'inline-flex'};" title="${this.t('installAppTitle')}">
          ${this.t('installApp')}
        </button>
        <a href="${specUrl}" class="ctrl-btn" target="_blank">${this.t('linkSpec')}</a>
        <a href="${postUrl}" class="ctrl-btn" target="_blank">${this.t('linkPost')}</a>
        <a href="${kitsUrl}" class="ctrl-btn ctrl-btn-accent" target="_blank">${this.t('linkKits')}</a>
      </div>
    `;

    document.getElementById('btn-check-update')?.addEventListener('click', () => this.checkForUpdatesManual());
    document.getElementById('btn-theme-toggle')?.addEventListener('click', () => this.toggleTheme());
    document.getElementById('btn-sound-toggle')?.addEventListener('click', () => {
      soundController.toggleSound();
      this.renderHeader();
    });
    document.getElementById('btn-lang-toggle')?.addEventListener('click', () => this.toggleLang());
    document.getElementById('btn-install-pwa')?.addEventListener('click', async () => {
      if (this.deferredPrompt) {
        this.deferredPrompt.prompt();
        try {
          const { outcome } = await this.deferredPrompt.userChoice;
          if (outcome === 'accepted') {
            this.showToast(this.t('installSuccessToast'));
          }
        } catch {}
        this.deferredPrompt = null;
      } else {
        const isIos = /iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase()) && !window.MSStream;
        this.showToast(isIos ? this.t('installIosInstructions') : this.t('installGenericInstructions'), 4000);
      }
    });
  }

  renderNavTabs() {
    const nav = document.getElementById('nav-deck');
    if (!nav) return;
    nav.innerHTML = `
      <button class="nav-tab ${this.activeTab === 'study' ? 'active' : ''}" data-tab="study">${this.t('tabStudy')}</button>
      <button class="nav-tab ${this.activeTab === 'creator' ? 'active' : ''}" data-tab="creator">${this.t('tabCreator')}</button>
      <button class="nav-tab ${this.activeTab === 'stats' ? 'active' : ''}" data-tab="stats">${this.t('tabStats')}</button>
    `;

    nav.querySelectorAll('.nav-tab').forEach(tab => {
      tab.addEventListener('click', (e) => {
        this.activeTab = e.currentTarget.getAttribute('data-tab');
        this.renderNavTabs();
        this.renderView();
      });
    });
  }

  renderView() {
    const container = document.getElementById('app-container');
    if (!container) return;

    if (this.activeTab === 'study') {
      if (!this.activeDeck) {
        this.renderDeckSelector(container);
      } else {
        this.renderStudySession(container);
      }
    } else if (this.activeTab === 'creator') {
      this.renderCreatorView(container);
    } else if (this.activeTab === 'stats') {
      this.renderStatsView(container);
    }
  }

  // --- VISTA 1: SELECTOR DE MAZO Y MODO ---
  renderDeckSelector(container) {
    const all = this.getAllDecks();
    const kidsDecks = all.filter(d => d.tier === 'kids');
    const adultsDecks = all.filter(d => d.tier === 'adults');
    const customDecks = all.filter(d => d.tier === 'custom');

    const renderDeckCards = (list) => list.map(d => {
      const isSelected = d.id === this.selectedDeckId;
      const title = d.title[this.currentLang] || d.title.es;
      const desc = d.description ? (d.description[this.currentLang] || d.description.es) : '';
      const count = d.cards.length;
      return `
        <div class="deck-card ${isSelected ? 'selected' : ''}" data-deck-id="${d.id}">
          <div class="deck-icon">${d.icon || '🎴'}</div>
          <div class="deck-title">${title}</div>
          <div class="deck-desc">${desc}</div>
          <div class="deck-footer">
            <span>${count} ${this.t('cardsCount')}</span>
            <span>${d.langFront.toUpperCase()} ➔ ${d.langBack.toUpperCase()}</span>
          </div>
        </div>
      `;
    }).join('');

    const renderModes = () => STUDY_MODES.map(m => {
      const isSelected = m.id === this.selectedModeId;
      const title = m.title[this.currentLang] || m.title.es;
      const sub = m.subtitle[this.currentLang] || m.subtitle.es;
      return `
        <div class="mode-btn ${isSelected ? 'selected' : ''}" data-mode-id="${m.id}">
          <div class="mode-btn-title"><span>${m.icon}</span> ${title}</div>
          <div class="mode-btn-desc">${sub}</div>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="view-panel active">
        <h2 class="section-title">${this.t('selectDeckTitle')}</h2>
        <p class="section-sub">${this.t('selectDeckSub')}</p>

        <div class="category-badge"><span>🎒</span> ${this.t('categoryKids')}</div>
        <div class="decks-grid">${renderDeckCards(kidsDecks)}</div>

        <div class="category-badge"><span>💼</span> ${this.t('categoryAdults')}</div>
        <div class="decks-grid">${renderDeckCards(adultsDecks)}</div>

        ${customDecks.length > 0 ? `
          <div class="category-badge"><span>⭐</span> ${this.t('categoryCustom')}</div>
          <div class="decks-grid">${renderDeckCards(customDecks)}</div>
        ` : ''}

        <h3 class="section-title" style="margin-top: 2rem;">${this.t('selectModeTitle')}</h3>
        <div class="modes-row">${renderModes()}</div>

        <button id="btn-start-study" class="btn-primary-big">
          ${this.t('btnStartStudy')}
        </button>
      </div>
    `;

    container.querySelectorAll('.deck-card').forEach(c => {
      c.addEventListener('click', (e) => {
        this.selectedDeckId = e.currentTarget.getAttribute('data-deck-id');
        this.renderDeckSelector(container);
      });
    });

    container.querySelectorAll('.mode-btn').forEach(m => {
      m.addEventListener('click', (e) => {
        this.selectedModeId = e.currentTarget.getAttribute('data-mode-id');
        this.renderDeckSelector(container);
      });
    });

    document.getElementById('btn-start-study')?.addEventListener('click', () => {
      this.startStudySession(this.selectedDeckId, this.selectedModeId);
    });
  }

  startStudySession(deckId, modeId, customCards = null) {
    this.activeDeck = this.getDeckById(deckId);
    this.selectedModeId = modeId;
    this.sessionCards = customCards ? [...customCards] : [...this.activeDeck.cards].sort(() => 0.5 - Math.random());
    this.currentIndex = 0;
    this.isFlipped = false;
    this.revealedHintCount = 0;
    this.currentStreak = 0;
    this.sessionScore = 0;
    this.failedCards = [];
    this.quizSelected = false;

    if (!this.masteryData[deckId]) {
      this.masteryData[deckId] = {};
    }

    this.renderView();
  }

  // --- VISTA 2: SESIÓN DE ESTUDIO ACTIVA ---
  renderStudySession(container) {
    if (this.currentIndex >= this.sessionCards.length) {
      this.renderSessionSummary(container);
      return;
    }

    const card = this.sessionCards[this.currentIndex];
    const total = this.sessionCards.length;
    const progressText = this.t('sessionProgress', { current: this.currentIndex + 1, total });
    const mastery = calculateDeckMastery(this.masteryData[this.activeDeck.id] || {}, this.activeDeck.cards.length);

    container.innerHTML = `
      <div class="view-panel active">
        <div class="study-header">
          <div class="study-progress">${progressText}</div>
          <button id="btn-exit-session" class="ctrl-btn">← ${this.t('btnBackHome')}</button>
          <div class="study-mastery-chip">${this.t('masteryBadge', { percent: mastery.percent })}</div>
        </div>

        <div id="flashcard-element" class="card-container ${this.isFlipped ? 'is-flipped' : ''}">
          <div class="card-inner">
            <div class="card-face card-front">
              <span class="card-label">${this.t('manualTermHeader')} (${this.activeDeck.langFront.toUpperCase()})</span>
              <div class="card-main-text">${card.front}</div>
              ${card.hint ? `<div class="card-hint-box">${this.t('hintLabel')} ${card.hint}</div>` : ''}
              
              <div class="card-audio-controls" onclick="event.stopPropagation();">
                <button class="audio-btn btn-speak-front" title="Voz Normal">🔊 1.0x</button>
                <button class="audio-btn btn-speak-front-slow" title="Modo Tortuga">🐢 0.75x</button>
              </div>
              <div style="margin-top: 1.5rem; font-size: 0.82rem; color: var(--text-muted);">${this.t('tapToFlip')}</div>
            </div>

            <div class="card-face card-back">
              <span class="card-label">${this.t('manualDefHeader')} (${this.activeDeck.langBack.toUpperCase()})</span>
              <div class="card-main-text">${card.back}</div>
              ${card.phonetic ? `<span class="card-phonetic">${card.phonetic}</span>` : ''}
              
              <div class="card-audio-controls" onclick="event.stopPropagation();">
                <button class="audio-btn btn-speak-back" title="Voz Normal">🔊 1.0x</button>
                <button class="audio-btn btn-speak-back-slow" title="Modo Tortuga">🐢 0.75x</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Acciones según el Modo Seleccionado -->
        <div id="mode-interaction-container">
          ${this.renderModeInteractionHtml(card)}
        </div>
      </div>
    `;

    const cardEl = document.getElementById('flashcard-element');
    cardEl?.addEventListener('click', () => {
      this.flipCard();
    });

    document.getElementById('btn-exit-session')?.addEventListener('click', () => {
      this.activeDeck = null;
      this.renderView();
    });

    // Pronunciación Frontal
    container.querySelectorAll('.btn-speak-front').forEach(b => {
      b.addEventListener('click', (e) => {
        e.stopPropagation();
        soundController.speakText(card.front, this.activeDeck.langFront, 1.0);
      });
    });
    container.querySelectorAll('.btn-speak-front-slow').forEach(b => {
      b.addEventListener('click', (e) => {
        e.stopPropagation();
        soundController.speakText(card.front, this.activeDeck.langFront, 0.75);
      });
    });

    // Pronunciación Trasera
    container.querySelectorAll('.btn-speak-back').forEach(b => {
      b.addEventListener('click', (e) => {
        e.stopPropagation();
        soundController.speakText(card.back, this.activeDeck.langBack, 1.0);
      });
    });
    container.querySelectorAll('.btn-speak-back-slow').forEach(b => {
      b.addEventListener('click', (e) => {
        e.stopPropagation();
        soundController.speakText(card.back, this.activeDeck.langBack, 0.75);
      });
    });

    this.bindModeInteractionEvents(card);
  }

  flipCard() {
    this.isFlipped = !this.isFlipped;
    soundController.playTone('flip');
    const el = document.getElementById('flashcard-element');
    if (el) {
      if (this.isFlipped) el.classList.add('is-flipped');
      else el.classList.remove('is-flipped');
    }
  }

  renderModeInteractionHtml(card) {
    if (this.selectedModeId === 'flip') {
      return `
        <div class="leitner-actions">
          <button id="btn-leitner-repeat" class="btn-leitner btn-leitner-repeat">${this.t('btnRepeat')}</button>
          <button id="btn-leitner-good" class="btn-leitner btn-leitner-good">${this.t('btnGood')}</button>
          <button id="btn-leitner-mastered" class="btn-leitner btn-leitner-mastered">${this.t('btnMastered')}</button>
        </div>
      `;
    } else if (this.selectedModeId === 'quiz') {
      const options = generateQuizOptions(card, this.activeDeck.cards);
      return `
        <div class="quiz-options-grid">
          ${options.map(opt => `
            <button class="quiz-option-btn" data-correct="${opt.isCorrect}">
              ${opt.text}
            </button>
          `).join('')}
        </div>
      `;
    } else if (this.selectedModeId === 'spelling') {
      const mask = getSpellingMask(card.back, this.revealedHintCount);
      return `
        <div class="spelling-box">
          <div class="spelling-mask">${mask}</div>
          <div class="spelling-input-row">
            <input type="text" id="spelling-input" class="spelling-input" placeholder="${this.t('typeAnswerPlaceholder')}" autocomplete="off" autofocus />
            <button id="btn-spelling-check" class="ctrl-btn ctrl-btn-accent">${this.t('btnCheck')}</button>
            <button id="btn-spelling-reveal" class="ctrl-btn">${this.t('btnRevealLetter')}</button>
          </div>
          <div id="spelling-feedback" style="margin-top: 0.75rem; font-weight: 700; text-align: center;"></div>
        </div>
      `;
    }
    return '';
  }

  bindModeInteractionEvents(card) {
    if (this.selectedModeId === 'flip') {
      document.getElementById('btn-leitner-repeat')?.addEventListener('click', () => this.handleAnswer('repeat', card));
      document.getElementById('btn-leitner-good')?.addEventListener('click', () => this.handleAnswer('good', card));
      document.getElementById('btn-leitner-mastered')?.addEventListener('click', () => this.handleAnswer('mastered', card));
    } else if (this.selectedModeId === 'quiz') {
      document.querySelectorAll('.quiz-option-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          if (this.quizSelected) return;
          this.quizSelected = true;
          const isCorrect = e.currentTarget.getAttribute('data-correct') === 'true';
          if (isCorrect) {
            e.currentTarget.classList.add('correct');
            this.handleAnswer('good', card);
          } else {
            e.currentTarget.classList.add('wrong');
            // Señalar la correcta
            document.querySelector('.quiz-option-btn[data-correct="true"]')?.classList.add('correct');
            this.handleAnswer('repeat', card);
          }
        });
      });
    } else if (this.selectedModeId === 'spelling') {
      const input = document.getElementById('spelling-input');
      const checkBtn = document.getElementById('btn-spelling-check');
      const revealBtn = document.getElementById('btn-spelling-reveal');
      const feedback = document.getElementById('spelling-feedback');

      const submitAttempt = () => {
        const attempt = input.value;
        const isOk = validateSpelling(attempt, card.back);
        if (isOk) {
          feedback.style.color = 'var(--status-success)';
          feedback.textContent = this.t('feedbackCorrect');
          soundController.playTone('good');
          setTimeout(() => this.handleAnswer(this.revealedHintCount === 0 ? 'mastered' : 'good', card), 800);
        } else {
          feedback.style.color = 'var(--status-error)';
          feedback.textContent = `${this.t('feedbackIncorrect')} (${card.back})`;
          soundController.playTone('error');
          setTimeout(() => this.handleAnswer('repeat', card), 1400);
        }
      };

      input?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') submitAttempt();
      });
      checkBtn?.addEventListener('click', submitAttempt);
      revealBtn?.addEventListener('click', () => {
        soundController.playTone('hint');
        this.revealedHintCount++;
        const maskEl = document.querySelector('.spelling-mask');
        if (maskEl) maskEl.textContent = getSpellingMask(card.back, this.revealedHintCount);
      });
    }
  }

  handleAnswer(status, card) {
    if (!this.masteryData[this.activeDeck.id]) {
      this.masteryData[this.activeDeck.id] = {};
    }
    this.masteryData[this.activeDeck.id][card.front] = status;
    this.saveMasteryData();

    if (status === 'mastered') {
      this.sessionScore += 3;
      this.currentStreak++;
      soundController.playTone('mastered');
    } else if (status === 'good') {
      this.sessionScore += 2;
      this.currentStreak++;
      soundController.playTone('good');
    } else {
      this.failedCards.push(card);
      this.currentStreak = 0;
      soundController.playTone('error');
    }

    if (this.currentStreak >= 5) {
      this.unlockMedal('streak_5');
    }

    this.currentIndex++;
    this.isFlipped = false;
    this.revealedHintCount = 0;
    this.quizSelected = false;
    setTimeout(() => this.renderView(), 300);
  }

  // --- VISTA RESUMEN FINAL ---
  renderSessionSummary(container) {
    this.stats.sessions++;
    const mastery = calculateDeckMastery(this.masteryData[this.activeDeck.id] || {}, this.activeDeck.cards.length);
    this.stats.totalMastered = Object.values(this.masteryData)
      .flatMap(d => Object.values(d))
      .filter(s => s === 'mastered').length;
    this.saveStats();

    this.unlockMedal('first_session');
    if (this.stats.totalMastered >= 10) this.unlockMedal('master_10');
    if (this.selectedModeId === 'quiz' && this.failedCards.length === 0) this.unlockMedal('quiz_ace');

    triggerConfetti(document.getElementById('confetti-canvas'));

    container.innerHTML = `
      <div class="view-panel active creator-card text-center" style="max-width: 600px; margin: 0 auto;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎉</div>
        <h2 class="section-title">${this.t('summaryTitle')}</h2>
        <p class="section-sub">${this.activeDeck.title[this.currentLang] || this.activeDeck.title.es}</p>

        <div style="background: var(--bg-inset); padding: 1.25rem; border-radius: var(--radius-md); margin-bottom: 1.5rem;">
          <div style="font-size: 1.4rem; font-weight: 800; color: var(--accent-primary); margin-bottom: 0.5rem;">
            ${this.t('summaryScore', { score: this.sessionScore })}
          </div>
          <div style="font-weight: 700; color: var(--text-secondary);">
            ${this.t('summaryMastered', { mastered: mastery.masteredCount, total: this.activeDeck.cards.length })}
          </div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          ${this.failedCards.length > 0 ? `
            <button id="btn-study-failed" class="btn-primary-big" style="background: var(--box-repeat); box-shadow: 0 4px 0 #d97706;">
              ${this.t('btnStudyFailed', { count: this.failedCards.length })}
            </button>
          ` : ''}
          <button id="btn-study-again" class="btn-primary-big">
            ${this.t('btnStudyAgain')}
          </button>
          <button id="btn-choose-another" class="ctrl-btn" style="justify-content: center; padding: 0.85rem; font-size: 1rem;">
            ${this.t('btnBackHome')}
          </button>
        </div>
      </div>
    `;

    document.getElementById('btn-study-failed')?.addEventListener('click', () => {
      this.startStudySession(this.activeDeck.id, this.selectedModeId, this.failedCards);
    });
    document.getElementById('btn-study-again')?.addEventListener('click', () => {
      this.startStudySession(this.activeDeck.id, this.selectedModeId);
    });
    document.getElementById('btn-choose-another')?.addEventListener('click', () => {
      this.activeDeck = null;
      this.renderView();
    });
  }

  // --- VISTA 3: CREADOR MÁGICO (IA, CSV Y MANUAL) ---
  renderCreatorView(container) {
    const savedApiKey = localStorage.getItem('geminiApiKey') || '';

    container.innerHTML = `
      <div class="view-panel active creator-card">
        <h2 class="section-title">${this.t('creatorTitle')}</h2>
        <p class="section-sub">${this.t('creatorSub')}</p>

        <div class="flex justify-center gap-4" style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
          <label style="font-weight: 700; cursor: pointer;">
            <input type="radio" name="creator-mode" value="ai" checked /> ${this.t('creatorModeAi')}
          </label>
          <label style="font-weight: 700; cursor: pointer;">
            <input type="radio" name="creator-mode" value="manual" /> ${this.t('creatorModeManual')}
          </label>
        </div>

        <div class="input-group">
          <label class="input-label">${this.t('deckNameLabel')}</label>
          <input type="text" id="deck-name-input" class="text-input" placeholder="${this.t('deckNamePlaceholder')}" />
        </div>

        <!-- Opciones Modo IA -->
        <div id="ai-creator-block">
          <div class="input-group">
            <label class="input-label">${this.t('aiApiKeyLabel')}</label>
            <input type="password" id="gemini-key-input" class="text-input" value="${savedApiKey}" placeholder="${this.t('aiApiKeyPlaceholder')}" />
            <p class="input-subhint">${this.t('aiApiKeyHint')}</p>
          </div>

          <div class="input-group">
            <label class="input-label">${this.t('aiTargetLang')}</label>
            <select id="ai-action-select" class="select-input">
              <option value="translate_en" selected>${this.t('optTranslateEn')}</option>
              <option value="translate_es">${this.t('optTranslateEs')}</option>
              <option value="translate_fr">${this.t('optTranslateFr')}</option>
              <option value="translate_de">${this.t('optTranslateDe')}</option>
              <option value="define_es">${this.t('optDefineEs')}</option>
              <option value="define_en">${this.t('optDefineEn')}</option>
            </select>
          </div>

          <div class="input-group">
            <label class="input-label">${this.t('termsInputLabel')}</label>
            <textarea id="terms-textarea" class="textarea-input" placeholder="${this.t('termsInputPlaceholder')}"></textarea>
          </div>

          <button id="btn-trigger-ai" class="btn-primary-big" style="margin-bottom: 1rem;">
            ${this.t('btnGenerateAi')}
          </button>
        </div>

        <!-- Opciones Modo Manual / CSV -->
        <div id="manual-creator-block" style="display: none;">
          <div class="input-group">
            <div style="display: flex; gap: 0.75rem; margin-bottom: 1rem; flex-wrap: wrap;">
              <label for="csv-file-input" class="ctrl-btn ctrl-btn-accent" style="cursor: pointer;">
                ${this.t('btnImportCsv')}
              </label>
              <input type="file" id="csv-file-input" accept=".csv,.txt" style="display: none;" />
              <button id="btn-download-tpl" class="ctrl-btn">${this.t('btnDownloadTemplate')}</button>
            </div>
            <div id="manual-rows" class="rows-container"></div>
            <button id="btn-add-manual-row" class="ctrl-btn" style="width: 100%; justify-content: center;">
              ${this.t('btnAddRow')}
            </button>
          </div>

          <button id="btn-save-manual-deck" class="btn-primary-big">
            ${this.t('btnSaveDeck')}
          </button>
        </div>

        <div id="creator-status" style="margin-top: 1rem; font-weight: 700; text-align: center;"></div>
      </div>
    `;

    const aiBlock = document.getElementById('ai-creator-block');
    const manualBlock = document.getElementById('manual-creator-block');
    const rowsContainer = document.getElementById('manual-rows');
    const statusEl = document.getElementById('creator-status');

    document.querySelectorAll('input[name="creator-mode"]').forEach(r => {
      r.addEventListener('change', (e) => {
        if (e.target.value === 'ai') {
          aiBlock.style.display = 'block';
          manualBlock.style.display = 'none';
        } else {
          aiBlock.style.display = 'none';
          manualBlock.style.display = 'block';
        }
      });
    });

    // Helper filas manuales
    const addManualRow = (f = '', b = '') => {
      const row = document.createElement('div');
      row.className = 'input-row-item';
      row.innerHTML = `
        <input type="text" class="text-input row-front" value="${f}" placeholder="${this.t('manualTermHeader')}" />
        <input type="text" class="text-input row-back" value="${b}" placeholder="${this.t('manualDefHeader')}" />
        <button class="btn-del-row" title="Eliminar">&times;</button>
      `;
      row.querySelector('.btn-del-row').addEventListener('click', () => row.remove());
      rowsContainer.appendChild(row);
    };

    addManualRow('Ejemplo', 'Example');
    addManualRow();

    document.getElementById('btn-add-manual-row')?.addEventListener('click', () => addManualRow());

    // Descarga de Plantilla CSV
    document.getElementById('btn-download-tpl')?.addEventListener('click', () => {
      const sample = [
        { front: 'Articulación', back: 'Joint', phonetic: '/dʒɔɪnt/', hint: 'Unión de huesos' },
        { front: 'Cráneo', back: 'Skull', phonetic: '/skʌl/', hint: 'Protege el cerebro' }
      ];
      const csvStr = exportCSV(sample);
      const blob = new Blob([csvStr], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'plantilla_flashcards.csv';
      link.click();
      URL.revokeObjectURL(url);
    });

    // Importador CSV
    document.getElementById('csv-file-input')?.addEventListener('change', (e) => {
      const file = e.target.files?.[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (evt) => {
        const text = evt.target?.result;
        const parsed = parseCSV(String(text));
        if (parsed.length > 0) {
          rowsContainer.innerHTML = '';
          parsed.forEach(p => addManualRow(p.front, p.back));
          statusEl.style.color = 'var(--status-success)';
          statusEl.textContent = `¡Importadas ${parsed.length} tarjetas con éxito!`;
        } else {
          statusEl.style.color = 'var(--status-error)';
          statusEl.textContent = 'No se encontraron tarjetas válidas en el archivo.';
        }
      };
      reader.readAsText(file);
    });

    // Guardar Manual
    document.getElementById('btn-save-manual-deck')?.addEventListener('click', () => {
      const name = document.getElementById('deck-name-input').value.trim() || 'Mazo Personalizado';
      const rows = rowsContainer.querySelectorAll('.input-row-item');
      const cards = [];
      rows.forEach(r => {
        const f = r.querySelector('.row-front').value.trim();
        const b = r.querySelector('.row-back').value.trim();
        if (f && b) cards.push({ front: f, back: b });
      });

      if (cards.length === 0) {
        statusEl.style.color = 'var(--status-error)';
        statusEl.textContent = 'Introduce al menos una tarjeta con término y definición.';
        return;
      }

      const newDeck = {
        id: 'custom_' + Date.now(),
        tier: 'custom',
        icon: '⭐',
        title: { es: name, en: name },
        description: { es: 'Mazo creado manualmente', en: 'Custom user deck' },
        langFront: 'es',
        langBack: 'en',
        cards
      };

      this.customDecks.push(newDeck);
      this.saveCustomDecks();
      this.unlockMedal('ai_creator');
      this.selectedDeckId = newDeck.id;
      this.activeTab = 'study';
      this.renderNavTabs();
      this.renderView();
    });

    // Generar con IA (Gemini Batch)
    document.getElementById('btn-trigger-ai')?.addEventListener('click', async () => {
      const apiKey = document.getElementById('gemini-key-input').value.trim();
      const action = document.getElementById('ai-action-select').value;
      const termsRaw = document.getElementById('terms-textarea').value;
      const name = document.getElementById('deck-name-input').value.trim() || 'Mazo Generado con IA';

      if (!apiKey) {
        statusEl.style.color = 'var(--status-error)';
        statusEl.textContent = this.t('aiApiKeyLabel');
        return;
      }
      localStorage.setItem('geminiApiKey', apiKey);

      const termsList = termsRaw.split(/[\n,;]+/).map(t => t.trim()).filter(Boolean);
      if (termsList.length === 0) {
        statusEl.style.color = 'var(--status-error)';
        statusEl.textContent = 'Introduce al menos un término para generar.';
        return;
      }

      statusEl.style.color = 'var(--accent-primary)';
      statusEl.textContent = '⚡ Conectando con Gemini y generando tarjetas en lote...';
      const btn = document.getElementById('btn-trigger-ai');
      btn.disabled = true;

      const result = await generateBatchDeckWithGemini(termsList, action, apiKey);
      btn.disabled = false;

      if (!result.success || !result.cards || result.cards.length === 0) {
        statusEl.style.color = 'var(--status-error)';
        statusEl.textContent = result.error || 'No se pudieron generar las tarjetas.';
        return;
      }

      const newDeck = {
        id: 'ai_' + Date.now(),
        tier: 'custom',
        icon: '✨',
        title: { es: name, en: name },
        description: { es: 'Generado con Google Gemini', en: 'Generated with Google Gemini' },
        langFront: action.includes('en') ? 'es' : 'en',
        langBack: action.includes('en') ? 'en' : 'es',
        cards: result.cards
      };

      this.customDecks.push(newDeck);
      this.saveCustomDecks();
      this.unlockMedal('ai_creator');
      this.selectedDeckId = newDeck.id;
      this.activeTab = 'study';
      this.renderNavTabs();
      this.renderView();
    });
  }

  // --- VISTA 4: MEDALLAS Y PASAPORTE DE ESTUDIO ---
  renderStatsView(container) {
    const totalMastered = Object.values(this.masteryData)
      .flatMap(d => Object.values(d))
      .filter(s => s === 'mastered').length;

    container.innerHTML = `
      <div class="view-panel active">
        <h2 class="section-title">${this.t('statsTitle')}</h2>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem;">
          <div style="background: var(--bg-surface); padding: 1.25rem; border-radius: var(--radius-md); text-align: center; border: 1px solid var(--border-card);">
            <div style="font-size: 2rem; font-weight: 800; color: var(--box-mastered);">${totalMastered}</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-secondary);">${this.t('totalMasteredLabel')}</div>
          </div>
          <div style="background: var(--bg-surface); padding: 1.25rem; border-radius: var(--radius-md); text-align: center; border: 1px solid var(--border-card);">
            <div style="font-size: 2rem; font-weight: 800; color: var(--accent-primary);">${this.getAllDecks().length}</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-secondary);">${this.t('totalDecksLabel')}</div>
          </div>
          <div style="background: var(--bg-surface); padding: 1.25rem; border-radius: var(--radius-md); text-align: center; border: 1px solid var(--border-card);">
            <div style="font-size: 2rem; font-weight: 800; color: var(--box-good);">${this.stats.sessions}</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-secondary);">${this.t('totalSessionsLabel')}</div>
          </div>
        </div>

        <h3 class="section-title" style="margin-bottom: 1rem;">
          ${this.t('medalsUnlockedLabel', { count: this.unlockedMedals.length })}
        </h3>
        <div class="medals-grid">
          ${MEDALS.map(m => {
            const isUnlocked = this.unlockedMedals.includes(m.id);
            const title = m.title[this.currentLang] || m.title.es;
            const desc = m.description[this.currentLang] || m.description.es;
            return `
              <div class="medal-card ${isUnlocked ? 'unlocked' : 'locked'}">
                <div class="medal-icon">${m.icon}</div>
                <div class="medal-title">${title}</div>
                <div class="medal-desc">${desc}</div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  bindGlobalEvents() {
    window.addEventListener('keydown', (e) => {
      // Atajos de accesibilidad
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === ' ' || e.key === 'Enter') {
        if (this.activeTab === 'study' && this.activeDeck) {
          e.preventDefault();
          this.flipCard();
        }
      } else if (e.key === '1') {
        document.getElementById('btn-leitner-repeat')?.click();
      } else if (e.key === '2') {
        document.getElementById('btn-leitner-good')?.click();
      } else if (e.key === '3') {
        document.getElementById('btn-leitner-mastered')?.click();
      } else if (e.key === 't' || e.key === 'T') {
        this.toggleTheme();
      } else if (e.key === 'm' || e.key === 'M') {
        soundController.toggleSound();
        this.renderHeader();
      } else if (e.key === 'v' || e.key === 'V') {
        if (this.activeTab === 'study' && this.sessionCards[this.currentIndex]) {
          const card = this.sessionCards[this.currentIndex];
          if (this.isFlipped) soundController.speakText(card.back, this.activeDeck.langBack, 1.0);
          else soundController.speakText(card.front, this.activeDeck.langFront, 1.0);
        }
      }
    });
  }
}

// Iniciar aplicación al cargar el DOM
window.addEventListener('DOMContentLoaded', () => {
  const app = new FlashcardsApp();
  app.init();
});
