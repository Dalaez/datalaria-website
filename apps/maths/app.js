// apps/maths/app.js - Controlador reactivo de interfaz, audio, PWA y estado local
(function() {
  const catalog = window.MATHS_CATALOG;
  const engine = window.MathsEngine;
  const audio = window.MathsAudio;

  // Estado reactivo
  let lang = 'es';
  let activeTab = 'play';
  let selectedLevel = 'l1';
  let selectedMode = 'classic';
  let currentProblem = null;

  // Estado de partida
  let inGame = false;
  let inFeedbackPause = false;
  let feedbackTimeout = null;
  let roundIndex = 0;
  const TOTAL_ROUNDS = 10;
  let score = 0;
  let correctCount = 0;
  let wrongCount = 0;
  let streak = 0;
  let bestStreak = 0;
  let timerInterval = null;
  let timeLeft = 10;
  let timeTotal = 10;
  let inputVal = '';
  let inputQuo = '';
  let inputRem = '';
  let activeDivisionField = 'quo'; // 'quo' o 'rem'
  let isHintVisible = false;
  let hintUsedThisRound = false;
  let roundHistory = [];
  let dailyRng = null;

  // PWA Prompt
  let deferredInstallPrompt = null;
  let isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;

  // Perfiles Familiares y Persistencia Local Aislada (INV-MATHS-11)
  let activeProfileId = 'player_1';
  let userStats = {
    highScores: {},
    bestStreakEver: 0,
    unlockedMedals: []
  };

  function getStorageKey(profileId = activeProfileId) {
    return `datalaria_maths_v2_stats_${profileId}`;
  }

  function loadStats() {
    // 1. Cargar perfil activo guardado
    try {
      const savedProfile = localStorage.getItem('datalaria_maths_active_profile');
      if (savedProfile && catalog.profiles && catalog.profiles.some(p => p.id === savedProfile)) {
        activeProfileId = savedProfile;
      }
    } catch (e) { }

    // 2. Migración retrocompatible de datos anteriores a player_1
    try {
      const legacyData = localStorage.getItem('datalaria_maths_v2_stats');
      if (legacyData && !localStorage.getItem('datalaria_maths_v2_stats_player_1')) {
        localStorage.setItem('datalaria_maths_v2_stats_player_1', legacyData);
      }
    } catch (e) { }

    // 3. Cargar estadísticas aisladas del perfil activo
    userStats = {
      highScores: {},
      bestStreakEver: 0,
      unlockedMedals: []
    };
    try {
      const data = localStorage.getItem(getStorageKey());
      if (data) userStats = JSON.parse(data);
    } catch (e) { }

    // 4. Cargar sonido
    try {
      const savedSound = localStorage.getItem('maths-sound');
      if (savedSound !== null) {
        if ((savedSound === 'true') !== audio.isSoundEnabled()) {
          audio.toggleSound();
        }
      }
    } catch (e) { }
  }

  function saveStats() {
    try {
      localStorage.setItem(getStorageKey(), JSON.stringify(userStats));
    } catch (e) { }
  }

  function switchProfile(profileId) {
    if (profileId === activeProfileId) return;
    audio.playClick();
    activeProfileId = profileId;
    try {
      localStorage.setItem('datalaria_maths_active_profile', profileId);
    } catch (e) { }
    loadStats();
    const profileObj = catalog.profiles ? catalog.profiles.find(p => p.id === profileId) : null;
    const profileName = profileObj ? `${profileObj.avatar} ${profileObj.name[lang]}` : profileId;
    showToast(`${t('profile_switched')} ${profileName}`);
    renderAll();
  }

  // Toasts flotantes lúdicos (sin window.alert ni window.confirm)
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

  // Detectar idioma inicial y parámetros por URL o navegador
  function initLang() {
    const params = new URLSearchParams(window.location.search);
    const urlLang = params.get('lang');
    if (urlLang === 'en' || urlLang === 'es') {
      lang = urlLang;
    } else {
      lang = (navigator.language && navigator.language.startsWith('en')) ? 'en' : 'es';
    }

    const queryMode = params.get('mode');
    if (queryMode && ['classic', 'time_attack', 'zen', 'daily'].includes(queryMode)) {
      selectedMode = queryMode;
    }
    const queryLevel = params.get('level');
    if (queryLevel && catalog.levels.some(l => l.id === queryLevel)) {
      selectedLevel = queryLevel;
    }
  }

  function t(key) {
    return (catalog.i18n[lang] && catalog.i18n[lang][key]) || key;
  }

  // Renderizadores de UI
  function renderAll() {
    renderShell();
    renderTabs();
    if (activeTab === 'play') renderPlayTab();
    else if (activeTab === 'learn') renderLearnTab();
    else if (activeTab === 'achievements') renderAchievementsTab();
  }

  function renderShell() {
    document.getElementById('shell-app-title').textContent = t('app_title');
    document.getElementById('lang-btn').textContent = lang === 'es' ? '🇪🇸 ES' : '🇬🇧 EN';
    document.getElementById('sound-btn').textContent = audio.isSoundEnabled() ? '🔊' : '🔇';
    document.getElementById('sound-btn').title = t('sound_toggle');
    document.getElementById('theme-btn').title = t('theme_toggle');

    const installBtn = document.getElementById('btn-install-pwa');
    const installLabel = document.getElementById('label-install-btn');
    if (installBtn && installLabel) {
      installLabel.textContent = t('install_app');
      installBtn.title = t('install_app_title');
      installBtn.style.display = isStandalone ? 'none' : 'inline-flex';
    }

    document.getElementById('datalaria-back-link').textContent = t('datalaria_back');
    document.getElementById('datalaria-back-link').href = `/${lang}/apps/`;
    document.getElementById('link-spec').textContent = t('spec_link');
    document.getElementById('link-spec').href = `/${lang}/apps/maths/`;
    document.getElementById('link-post').textContent = t('post_link');
    document.getElementById('link-post').href = lang === 'es' 
      ? '/es/posts/founderz-programando-chatGPT/' 
      : '/en/posts/founderz-coding-chatGPT/';
    document.getElementById('link-kits').textContent = t('kits_link');
    document.getElementById('link-kits').href = `/${lang}/recursos/`;

    renderProfileBar();
  }

  function renderProfileBar() {
    const bar = document.getElementById('profile-bar');
    if (!bar || !catalog.profiles) return;
    bar.innerHTML = `
      <span class="profile-bar-label">👥 ${t('profile_label')}</span>
      ${catalog.profiles.map(p => `
        <button class="profile-chip ${activeProfileId === p.id ? 'active' : ''}" data-profile-id="${p.id}" title="${p.title[lang]}">
          <span>${p.avatar}</span>
          <span>${p.name[lang]}</span>
          ${activeProfileId === p.id ? '<span style="font-size: 0.75rem; margin-left: 2px;">✓</span>' : ''}
        </button>
      `).join('')}
    `;

    bar.querySelectorAll('.profile-chip').forEach(chip => {
      chip.onclick = () => {
        const pId = chip.getAttribute('data-profile-id');
        switchProfile(pId);
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
    nav.innerHTML = tabs.map(tab => `
      <button class="tab-btn ${activeTab === tab.id ? 'active' : ''}" data-tab="${tab.id}">
        ${tab.label}
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

  // Pestaña Jugar
  function renderPlayTab() {
    const container = document.getElementById('tab-content');
    if (!inGame) {
      let html = `
        <div class="card">
          <h2 style="font-size: 1.4rem; font-weight: 800; margin-bottom: 8px;">${t('choose_level')}</h2>
          <div class="levels-grid">
            ${catalog.levels.map(lvl => `
              <div class="selectable-item ${selectedLevel === lvl.id ? 'selected' : ''}" data-level="${lvl.id}">
                <div style="font-size: 1.8rem; margin-bottom: 4px;">${lvl.icon}</div>
                <strong style="display: block; font-size: 1.05rem;">${lvl.name[lang]}</strong>
                <span style="font-size: 0.85rem; color: var(--text-secondary); display: block; margin-top: 4px;">${lvl.desc[lang]}</span>
              </div>
            `).join('')}
          </div>

          <h2 style="font-size: 1.4rem; font-weight: 800; margin: 24px 0 8px;">${t('choose_mode')}</h2>
          <div class="levels-grid">
            ${catalog.modes.map(m => `
              <div class="selectable-item ${selectedMode === m.id ? 'selected' : ''}" data-mode="${m.id}">
                <div style="font-size: 1.8rem; margin-bottom: 4px;">${m.icon}</div>
                <strong style="display: block; font-size: 1.05rem;">${m.name[lang]}</strong>
                <span style="font-size: 0.85rem; color: var(--text-secondary); display: block; margin-top: 4px;">${m.desc[lang]}</span>
              </div>
            `).join('')}
          </div>

          <div style="text-align: center; margin-top: 30px;">
            <button id="btn-start" class="btn-arcade btn-arcade-primary" style="font-size: 1.3rem; padding: 14px 36px; border-radius: var(--radius-pill);">
              ${t('start_game')}
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
      document.getElementById('btn-start').onclick = startGameSession;
    } else {
      renderActiveGame(container);
    }
  }

  function renderActiveGame(container) {
    const isDivision = currentProblem && currentProblem.type === 'division';
    let roundLabel = '';
    if (selectedMode === 'classic') roundLabel = `${t('round')} ${roundIndex}/${TOTAL_ROUNDS}`;
    else if (selectedMode === 'daily') roundLabel = `📅 ${t('daily_challenge_label')} ${roundIndex}/${TOTAL_ROUNDS}`;
    else if (selectedMode === 'time_attack') roundLabel = `⚡ ${t('round')} ${roundIndex}`;
    else roundLabel = `🧘 ${t('round')} ${roundIndex}`;

    const comboMultiplier = streak >= 5 ? 3 : (streak >= 3 ? 2 : 1);

    let html = `
      <div class="card" style="position: relative;">
        <canvas id="confetti-canvas"></canvas>
        <div class="game-header">
          <button id="btn-exit-game" class="btn-arcade">${t('back_menu')}</button>
          <div class="stat-chip">${roundLabel}</div>
          <div class="stat-chip">⭐ ${t('points')}: <strong style="font-family: var(--font-mono); margin-left: 4px;">${score}</strong></div>
          ${streak >= 2 ? `<div class="streak-badge">🔥 ${streak} ${t('streak')} (x${comboMultiplier})</div>` : ''}
        </div>

        ${selectedMode !== 'zen' ? `
          <div class="timer-bar-container">
            <div id="timer-bar-fill" class="timer-bar-fill" style="width: ${(timeLeft / timeTotal) * 100}%;"></div>
          </div>
        ` : ''}

        <!-- Contenedor del Banner de Feedback Formativo -->
        <div id="feedback-banner-container"></div>

        <div class="problem-box">
          <div class="problem-text">${currentProblem ? currentProblem.display : '...'}</div>
          
          ${!isDivision ? `
            <div class="answer-display-box" id="display-answer">${inputVal || '?'}</div>
          ` : `
            <div style="display: flex; gap: 10px; justify-content: center; align-items: center;">
              <div class="answer-display-box ${activeDivisionField === 'quo' ? 'border-primary' : ''}" id="display-quo" style="cursor: pointer;">
                <span style="font-size: 0.9rem; margin-right: 4px; color: var(--text-muted);">${t('quotient')}:</span> ${inputQuo || '?'}
              </div>
              <div class="answer-display-box ${activeDivisionField === 'rem' ? 'border-primary' : ''}" id="display-rem" style="cursor: pointer;">
                <span style="font-size: 0.9rem; margin-right: 4px; color: var(--text-muted);">${t('remainder')}:</span> ${inputRem || '?'}
              </div>
            </div>
          `}
        </div>

        <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 12px;">
          <button id="btn-toggle-hint" class="btn-arcade" style="background: var(--bg-inset);">
            ${isHintVisible ? t('hide_hint') : t('visual_hint')}
          </button>
          <button id="btn-skip" class="btn-arcade" style="background: var(--bg-inset);">
            ${t('skip')}
          </button>
        </div>

        <div id="hint-container" class="${isHintVisible ? '' : 'hidden'}" style="margin-bottom: 16px;">
          ${currentProblem ? engine.renderVisualHint(currentProblem.visual, lang) : ''}
        </div>

        <!-- Numpad 3D -->
        <div class="numpad">
          ${[1,2,3,4,5,6,7,8,9].map(n => `<button class="numpad-btn" data-key="${n}">${n}</button>`).join('')}
          <button class="numpad-btn action-del" data-key="del">⌫</button>
          <button class="numpad-btn" data-key="0">0</button>
          <button class="numpad-btn action-enter" data-key="enter">⏎</button>
        </div>
      </div>
    `;
    container.innerHTML = html;

    document.getElementById('btn-exit-game').onclick = () => {
      endGameSession();
      renderPlayTab();
    };

    document.getElementById('btn-toggle-hint').onclick = () => {
      toggleVisualHint();
    };

    document.getElementById('btn-skip').onclick = () => handleAnswerSubmit(false, true);

    if (isDivision) {
      document.getElementById('display-quo').onclick = () => { activeDivisionField = 'quo'; renderActiveGame(container); };
      document.getElementById('display-rem').onclick = () => { activeDivisionField = 'rem'; renderActiveGame(container); };
    }

    container.querySelectorAll('.numpad-btn').forEach(btn => {
      btn.onclick = () => handleNumpadPress(btn.getAttribute('data-key'));
    });
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

  function handleNumpadPress(key) {
    if (inFeedbackPause) return;
    audio.playClick();
    const isDivision = currentProblem && currentProblem.type === 'division';

    if (key === 'del') {
      if (!isDivision) inputVal = inputVal.slice(0, -1);
      else {
        if (activeDivisionField === 'quo') inputQuo = inputQuo.slice(0, -1);
        else inputRem = inputRem.slice(0, -1);
      }
    } else if (key === 'enter') {
      submitCurrentAnswer();
      return;
    } else {
      if (!isDivision) {
        if (inputVal.length < 5) inputVal += key;
      } else {
        if (activeDivisionField === 'quo') {
          if (inputQuo.length < 4) inputQuo += key;
        } else {
          if (inputRem.length < 4) inputRem += key;
        }
      }
    }

    if (!isDivision) {
      const el = document.getElementById('display-answer');
      if (el) el.textContent = inputVal || '?';
    } else {
      const elQ = document.getElementById('display-quo');
      const elR = document.getElementById('display-rem');
      if (elQ) elQ.innerHTML = `<span style="font-size: 0.9rem; margin-right: 4px; color: var(--text-muted);">${t('quotient')}:</span> ${inputQuo || '?'}`;
      if (elR) elR.innerHTML = `<span style="font-size: 0.9rem; margin-right: 4px; color: var(--text-muted);">${t('remainder')}:</span> ${inputRem || '?'}`;
    }
  }

  function submitCurrentAnswer() {
    if (!currentProblem || inFeedbackPause) return;
    const isDivision = currentProblem.type === 'division';
    if (!isDivision && inputVal === '') return;
    if (isDivision && (inputQuo === '' || inputRem === '')) return;

    const evaluation = engine.evaluateAnswer(currentProblem, inputVal, inputQuo, inputRem, lang);
    handleAnswerSubmit(evaluation.isCorrect, false, evaluation.correctDisplay);
  }

  function handleAnswerSubmit(isCorrect, isSkipped = false, correctDisplay = '') {
    clearInterval(timerInterval);
    clearTimeout(feedbackTimeout);

    const bannerContainer = document.getElementById('feedback-banner-container');
    let pointsEarned = 0;
    const resolvedCorrectDisplay = correctDisplay || (currentProblem ? (currentProblem.answer !== undefined ? String(currentProblem.answer) : `${t('quotient')}: ${currentProblem.quotient}, ${t('remainder')}: ${currentProblem.remainder}`) : '');

    // Registro de ronda para tira Wordle y repaso de fallos
    roundHistory.push({
      round: roundIndex,
      problem: currentProblem,
      isCorrect: isCorrect,
      usedHint: hintUsedThisRound,
      skipped: isSkipped,
      userVal: inputVal,
      userQuo: inputQuo,
      userRem: inputRem,
      correctDisplay: resolvedCorrectDisplay
    });

    if (isCorrect) {
      streak += 1;
      if (streak > bestStreak) bestStreak = streak;
      correctCount += 1;
      const multiplier = streak >= 5 ? 3 : (streak >= 3 ? 2 : 1);
      pointsEarned = Math.round((100 + (selectedMode === 'classic' || selectedMode === 'daily' ? timeLeft * 10 : 0)) * multiplier);
      score += pointsEarned;
      audio.playSuccess(streak);

      if (selectedMode === 'time_attack' && streak > 0 && streak % 5 === 0) {
        timeLeft = Math.min(60, timeLeft + 3);
      }

      if (bannerContainer) {
        bannerContainer.innerHTML = `
          <div class="feedback-banner feedback-success">
            <span>${t('awesome')} +${pointsEarned} pts</span>
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
            <span>${isSkipped ? t('good_try') : t('good_try')} ${t('correct_answer_is')} <strong>${resolvedCorrectDisplay}</strong></span>
            <button id="btn-next-fast" class="btn-arcade" style="padding: 4px 10px; font-size: 0.8rem; background: var(--bg-surface);">${t('next_question_btn')}</button>
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

    checkMedalsProgress();
    inFeedbackPause = true;

    // Pausa pedagógica: corta en aciertos (700ms), didáctica en fallos (1800ms)
    const pauseMs = isCorrect ? 700 : 1800;
    feedbackTimeout = setTimeout(() => {
      advanceRound();
    }, pauseMs);
  }

  function advanceRound() {
    inFeedbackPause = false;
    if ((selectedMode === 'classic' || selectedMode === 'daily') && roundIndex >= TOTAL_ROUNDS) {
      finishGame();
    } else if (selectedMode === 'time_attack' && timeLeft <= 0) {
      finishGame();
    } else {
      nextProblem();
    }
  }

  function startGameSession() {
    inGame = true;
    inFeedbackPause = false;
    roundIndex = 0;
    score = 0;
    correctCount = 0;
    wrongCount = 0;
    streak = 0;
    bestStreak = 0;
    isHintVisible = false;
    hintUsedThisRound = false;
    roundHistory = [];

    if (selectedMode === 'daily') {
      const todayStr = new Date().toISOString().slice(0, 10);
      const dailySeed = `${todayStr}_${selectedLevel}`;
      dailyRng = engine.createSeededRng(dailySeed);
    } else {
      dailyRng = null;
    }

    if (selectedMode === 'time_attack') {
      timeTotal = 60;
      timeLeft = 60;
    } else {
      timeTotal = 10;
      timeLeft = 10;
    }

    nextProblem();
  }

  function nextProblem() {
    roundIndex += 1;
    inputVal = '';
    inputQuo = '';
    inputRem = '';
    activeDivisionField = 'quo';
    isHintVisible = false;
    hintUsedThisRound = false;
    currentProblem = engine.generateProblem(selectedLevel, lang, dailyRng);

    if (selectedMode === 'classic' || selectedMode === 'daily') {
      timeTotal = 10;
      timeLeft = 10;
    }

    renderActiveGame(document.getElementById('tab-content'));
    startTimer();
  }

  function startTimer() {
    clearInterval(timerInterval);
    if (selectedMode === 'zen') return;

    timerInterval = setInterval(() => {
      if (inFeedbackPause) return;
      timeLeft -= 0.1;
      const fillEl = document.getElementById('timer-bar-fill');
      if (fillEl) {
        const pct = Math.max(0, (timeLeft / timeTotal) * 100);
        fillEl.style.width = pct + '%';
      }

      if (timeLeft <= 0) {
        clearInterval(timerInterval);
        const correctTxt = currentProblem ? (currentProblem.answer !== undefined ? String(currentProblem.answer) : `${t('quotient')}: ${currentProblem.quotient}, ${t('remainder')}: ${currentProblem.remainder}`) : '';
        handleAnswerSubmit(false, false, correctTxt);
      }
    }, 100);
  }

  function finishGame() {
    clearInterval(timerInterval);
    clearTimeout(feedbackTimeout);
    inGame = false;
    inFeedbackPause = false;
    audio.playWin();

    if (!userStats.highScores[selectedLevel] || score > userStats.highScores[selectedLevel]) {
      userStats.highScores[selectedLevel] = score;
    }
    if (bestStreak > userStats.bestStreakEver) {
      userStats.bestStreakEver = bestStreak;
    }
    saveStats();

    const container = document.getElementById('tab-content');
    const totalPlayed = roundHistory.length || roundIndex;
    const accuracy = (totalPlayed > 0) ? Math.round((correctCount / totalPlayed) * 100) : 0;

    // Tira visual estilo Wordle (🟩 Acierto limpio, 💡 Acierto con pista, 🟥 Fallo)
    const emojiStrip = roundHistory.map(r => {
      if (r.isCorrect && !r.usedHint) return '🟩';
      if (r.isCorrect && r.usedHint) return '💡';
      return '🟥';
    }).join('');

    // Preparar lista de fallos para repaso didáctico
    const mistakes = roundHistory.filter(r => !r.isCorrect);
    let mistakesHtml = '';
    if (mistakes.length > 0) {
      mistakesHtml = `
        <div class="mistake-review-section">
          <div class="mistake-review-title">
            <span>${t('mistake_review_title')}</span>
            <span style="font-size: 0.9rem; font-weight: 600; color: var(--text-muted);">(${mistakes.length})</span>
          </div>
          <div class="mistake-list">
            ${mistakes.map((m, idx) => `
              <div class="mistake-card">
                <div class="mistake-header">
                  <span class="mistake-problem-text">${m.problem ? m.problem.display : '...'}</span>
                  <span style="font-size: 0.85rem; color: var(--status-error); font-weight: 700;">${t('round')} ${m.round}</span>
                </div>
                <div class="mistake-details">
                  <span>${t('mistake_your_answer')} <strong>${m.userVal || (m.userQuo !== '' ? `${m.userQuo} (r:${m.userRem})` : (m.skipped ? t('skip') : '⏱️'))}</strong></span>
                  <span>${t('mistake_correct_answer')} <strong style="color: var(--status-success);">${m.correctDisplay}</strong></span>
                </div>
                <div class="mistake-hint-toggle">
                  <button class="btn-arcade btn-mistake-hint" data-mistake-idx="${idx}" style="font-size: 0.8rem; padding: 4px 10px; background: var(--bg-surface);">
                    ${t('view_hint_btn')}
                  </button>
                  <div id="mistake-hint-${idx}" class="mistake-hint-container hidden">
                    ${m.problem ? engine.renderVisualHint(m.problem.visual, lang) : ''}
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
            ${t('mistake_review_empty')}
          </div>
        </div>
      `;
    }

    let html = `
      <div class="card text-center" style="position: relative;">
        <canvas id="confetti-canvas"></canvas>
        <div style="font-size: 4rem; margin-bottom: 12px;">🏆</div>
        <h2 style="font-size: 2rem; font-weight: 800; color: var(--text-primary);">${t('game_over')}</h2>
        
        <div style="display: flex; gap: 16px; justify-content: center; margin: 20px 0 12px; flex-wrap: wrap;">
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">⭐ ${t('points')}: <strong>${score}</strong></div>
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">🎯 ${t('accuracy')}: <strong>${accuracy}%</strong></div>
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">🔥 ${t('best_streak')}: <strong>${bestStreak}</strong></div>
        </div>

        ${emojiStrip ? `
          <div class="round-blocks-strip" title="Resumen gráfico de respuestas">${emojiStrip}</div>
        ` : ''}

        <div style="display: flex; gap: 12px; justify-content: center; margin-top: 20px; flex-wrap: wrap;">
          <button id="btn-share-result" class="btn-arcade btn-share-result" style="font-size: 1.05rem; padding: 12px 22px;">
            ${t('share_result_btn')}
          </button>
          <button id="btn-again" class="btn-arcade btn-arcade-primary" style="font-size: 1.05rem; padding: 12px 22px;">
            ${t('play_again')}
          </button>
          <button id="btn-finish-diploma" class="btn-arcade btn-arcade-diploma" style="font-size: 1.05rem; padding: 12px 22px;">
            ${t('download_diploma_btn')}
          </button>
          <button id="btn-badges" class="btn-arcade" style="font-size: 1.05rem; padding: 12px 22px;">
            ${t('view_achievements')}
          </button>
        </div>

        ${mistakesHtml}
      </div>
    `;
    container.innerHTML = html;

    const canvas = document.getElementById('confetti-canvas');
    if (canvas) audio.launchConfetti(canvas);

    document.getElementById('btn-again').onclick = () => {
      startGameSession();
    };
    document.getElementById('btn-finish-diploma').onclick = downloadArcadeDiploma;
    document.getElementById('btn-badges').onclick = () => {
      activeTab = 'achievements';
      renderAll();
    };

    document.getElementById('btn-share-result').onclick = () => {
      audio.playClick();
      const todayStr = new Date().toISOString().slice(0, 10);
      const levelObj = catalog.levels.find(l => l.id === selectedLevel);
      const levelName = levelObj ? levelObj.name[lang] : selectedLevel;
      const modeObj = catalog.modes.find(m => m.id === selectedMode);
      const modeName = selectedMode === 'daily'
        ? `${t('daily_challenge_label')} (${todayStr})`
        : (modeObj ? modeObj.name[lang] : selectedMode);

      const shareUrl = `${window.location.origin}${window.location.pathname}?mode=${selectedMode}&level=${selectedLevel}${selectedMode === 'daily' ? '&date=' + todayStr : ''}`;
      const shareText = `Datalaria Maths · ${modeName}\n${levelName} | ⭐ ${score} pts (${correctCount}/${totalPlayed})\n${emojiStrip}\n${shareUrl}`;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(shareText).then(() => {
          showToast(t('share_result_copied'));
        }).catch(() => {
          showToast(t('share_result_copied'));
        });
      } else {
        showToast(t('share_result_copied'));
      }
    };

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
  }

  function checkMedalsProgress() {
    function unlock(medalId) {
      if (!userStats.unlockedMedals.includes(medalId)) {
        userStats.unlockedMedals.push(medalId);
        saveStats();
        showToast(`🎖️ ${t('badge_unlocked')}`);
      }
    }

    if (correctCount >= 1) unlock('first_win');
    if (streak >= 5) unlock('streak_5');
    if (streak >= 10) unlock('streak_10');
    if (currentProblem && currentProblem.type === 'division') unlock('div_master');
    if ((selectedLevel === 'l5' || selectedLevel === 'l6') && correctCount >= 8) unlock('brain_power');
    if (selectedMode === 'time_attack' && correctCount >= 12) unlock('time_hero');
  }

  // Pestaña Aprender
  function renderLearnTab() {
    const container = document.getElementById('tab-content');
    const ops = ['add', 'sub', 'mul', 'div'];

    let html = `
      <div class="card">
        <h2 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">💡 ${lang === 'es' ? 'Laboratorio Didáctico de Matemáticas' : 'Interactive Math Lab'}</h2>
        <p style="color: var(--text-secondary); margin-bottom: 20px;">
          ${t('tutorial_hint_tip')}
        </p>

        <div style="display: grid; gap: 20px;">
          ${ops.map(k => {
            const lesson = catalog.lessons[k];
            return `
              <div style="border: 2px solid var(--border-card); border-radius: var(--radius-md); padding: 16px; background: var(--bg-elevated);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <h3 style="font-size: 1.2rem; font-weight: 800; color: var(--text-primary);">${lesson.title[lang]}</h3>
                  <code style="background: var(--bg-inset); padding: 4px 10px; border-radius: var(--radius-sm); font-weight: 700; color: var(--op-add);">${lesson.formula}</code>
                </div>
                <p style="font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 12px;">${lesson.concept[lang]}</p>
                <div>${engine.renderVisualHint(lesson.visual, lang)}</div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
    container.innerHTML = html;
  }

  // Pestaña Logros
  function renderAchievementsTab() {
    const container = document.getElementById('tab-content');
    let html = `
      <div class="card">
        <h2 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">🏆 ${t('tab_achievements')}</h2>
        <p style="color: var(--text-secondary); margin-bottom: 20px;">
          ${lang === 'es' ? 'Desbloquea medallas demostrando tu agilidad mental.' : 'Unlock badges by sharpening your mental agility.'}
        </p>

        <div class="medals-grid">
          ${catalog.medals.map(m => {
            const isUnlocked = userStats.unlockedMedals.includes(m.id);
            return `
              <div class="medal-card ${isUnlocked ? 'unlocked' : 'locked'}">
                <div class="medal-icon">${m.icon}</div>
                <strong style="display: block; font-size: 1.1rem; margin-bottom: 4px;">${m.name[lang]}</strong>
                <span style="font-size: 0.85rem; color: var(--text-secondary);">${m.desc[lang]}</span>
                <div style="margin-top: 10px; font-size: 0.8rem; font-weight: 700; color: ${isUnlocked ? 'var(--status-success)' : 'var(--text-muted)'};">
                  ${isUnlocked ? (lang === 'es' ? '✓ Desbloqueada' : '✓ Unlocked') : (lang === 'es' ? '🔒 Bloqueada' : '🔒 Locked')}
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div class="diploma-promo-card">
          <div style="font-size: 2.4rem; margin-bottom: 6px;">🎓</div>
          <h3 style="font-size: 1.3rem; font-weight: 800; color: #b45309; margin-bottom: 6px;">${t('diploma_card_title')}</h3>
          <p style="font-size: 0.95rem; color: var(--text-secondary); max-width: 520px; margin: 0 auto 16px;">
            ${t('diploma_card_desc')}
          </p>
          <button id="btn-download-diploma" class="btn-arcade btn-arcade-diploma" style="font-size: 1.05rem; padding: 10px 24px;">
            ${t('download_diploma_btn')}
          </button>
        </div>

        <div style="text-align: center; margin-top: 30px;">
          <button id="btn-reset-stats" class="btn-arcade btn-arcade-danger" style="font-size: 0.85rem;">
            ${t('clean_history')}
          </button>
        </div>
      </div>
    `;
    container.innerHTML = html;

    document.getElementById('btn-download-diploma').onclick = downloadArcadeDiploma;

    document.getElementById('btn-reset-stats').onclick = () => {
      // Reemplazo visual de confirm() con toast interactivo
      userStats = { highScores: {}, bestStreakEver: 0, unlockedMedals: [] };
      saveStats();
      showToast(t('stats_reset_toast'));
      renderAchievementsTab();
    };
  }

  // Generador de Diploma Arcade PNG en Canvas 2D (INV-MATHS-11)
  function downloadArcadeDiploma() {
    audio.playSuccess(3);
    showToast(t('diploma_downloaded_toast'), 3000);

    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 800;
    const ctx = canvas.getContext('2d');

    // 1. Fondo suave pergamino / marfil
    ctx.fillStyle = '#fdfbf7';
    ctx.fillRect(0, 0, 1200, 800);

    const bgGrad = ctx.createLinearGradient(0, 0, 1200, 800);
    bgGrad.addColorStop(0, 'rgba(254, 243, 199, 0.35)');
    bgGrad.addColorStop(0.5, 'rgba(255, 255, 255, 0.15)');
    bgGrad.addColorStop(1, 'rgba(219, 234, 254, 0.35)');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, 1200, 800);

    // 2. Orla Dorada Doble y esquinas ornamentales
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
    ctx.fillText('DATALARIA ÁBACO ARCADE • ACADEMIA MATEMÁTICA', 600, 95);

    ctx.fillStyle = '#1e1b4b';
    ctx.font = '800 48px system-ui, -apple-system, sans-serif';
    ctx.fillText(lang === 'es' ? 'DIPLOMA DE HONOR' : 'DIPLOMA OF HONOR', 600, 160);

    ctx.fillStyle = '#64748b';
    ctx.font = '600 20px system-ui, -apple-system, sans-serif';
    ctx.fillText(
      lang === 'es' 
        ? 'Por su destacada agilidad mental, razonamiento aritmético y perseverancia' 
        : 'In recognition of outstanding mental arithmetic agility and perseverance',
      600, 202
    );

    // 4. Perfil Activo
    const profileObj = catalog.profiles ? catalog.profiles.find(p => p.id === activeProfileId) : null;
    const profileAvatar = profileObj ? profileObj.avatar : '🦁';
    const profileName = profileObj ? profileObj.name[lang] : 'Jugador 1';
    const profileTitle = profileObj ? profileObj.title[lang] : 'Explorador';

    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(260, 235, 680, 135, 16);
    ctx.fill();
    ctx.stroke();

    ctx.font = '64px system-ui, sans-serif';
    ctx.fillText(profileAvatar, 335, 325);

    ctx.textAlign = 'left';
    ctx.fillStyle = '#1e1b4b';
    ctx.font = '800 36px system-ui, -apple-system, sans-serif';
    ctx.fillText(profileName, 400, 295);

    ctx.fillStyle = '#0ea5e9';
    ctx.font = '700 20px system-ui, -apple-system, sans-serif';
    ctx.fillText(`★ ${profileTitle}`, 400, 332);

    // 5. Estadísticas de Logros
    let maxScore = 0;
    Object.values(userStats.highScores || {}).forEach(s => {
      if (s > maxScore) maxScore = s;
    });

    ctx.textAlign = 'center';
    const statBoxes = [
      { label: lang === 'es' ? 'Récord Máximo' : 'High Score', val: `${maxScore} pts` },
      { label: lang === 'es' ? 'Mejor Racha' : 'Best Streak', val: `🔥 ${userStats.bestStreakEver || 0}` },
      { label: lang === 'es' ? 'Medallas de Honor' : 'Badges Earned', val: `🎖️ ${userStats.unlockedMedals.length}/${catalog.medals.length}` }
    ];

    statBoxes.forEach((st, i) => {
      const bx = 220 + i * 260;
      ctx.fillStyle = '#f8faff';
      ctx.strokeStyle = '#cbd5e1';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.roundRect(bx - 110, 400, 220, 85, 12);
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
    ctx.fillText(lang === 'es' ? 'COLECCIÓN DE MEDALLAS OBTENIDAS:' : 'EARNED BADGES COLLECTION:', 600, 525);

    const medalIcons = catalog.medals.map(m => {
      return userStats.unlockedMedals.includes(m.id) ? m.icon : '⚪';
    }).join('   ');
    ctx.font = '36px system-ui, sans-serif';
    ctx.fillText(medalIcons, 600, 575);

    // 7. Sello Circular
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
    ctx.fillText('★ 🧮 ★', 0, 4);
    ctx.font = 'bold 9px system-ui, sans-serif';
    ctx.fillText('EXCELENCIA ARCADE', 0, 22);
    ctx.font = 'bold 8px system-ui, sans-serif';
    ctx.fillText('2026', 0, 34);
    ctx.restore();

    // 8. Fecha y Firma
    ctx.textAlign = 'left';
    const nowStr = new Date().toLocaleDateString(lang === 'es' ? 'es-ES' : 'en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    ctx.fillStyle = '#64748b';
    ctx.font = '600 15px system-ui, sans-serif';
    ctx.fillText((lang === 'es' ? 'Fecha de Expedición: ' : 'Issued on: ') + nowStr, 90, 680);
    ctx.fillText('Certificado Digital Client-Side (Datalaria SDD)', 90, 705);

    ctx.textAlign = 'center';
    ctx.fillStyle = '#334155';
    ctx.font = 'italic 16px serif';
    ctx.fillText('Datalaria Engineering & Pedagogy Team', 580, 685);
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
      a.download = `diploma_abaco_arcade_${activeProfileId}_${new Date().toISOString().slice(0, 10)}.png`;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => {
        document.body.removeChild(a);
      }, 300);
    } catch (err) {
      showToast('Error al exportar diploma PNG', 2500);
    }
  }

  window.downloadArcadeDiploma = downloadArcadeDiploma;

  // Conmutador de Sonido y Tema con persistencia
  function toggleAudio() {
    const enabled = audio.toggleSound();
    try { localStorage.setItem('maths-sound', enabled ? 'true' : 'false'); } catch (e) { }
    document.getElementById('sound-btn').textContent = enabled ? '🔊' : '🔇';
    showToast(enabled ? '🔊 Audio activado' : '🔇 Audio silenciado', 1500);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('pref-theme', next); } catch (e) { }
    showToast(next === 'dark' ? '🌙 Modo Cosmic Night' : '☀️ Modo Daylight Arcade', 1500);
  }

  // Lógica de Instalación PWA
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
          deferredInstallPrompt.prompt();
          deferredInstallPrompt.userChoice.then((choice) => {
            if (choice.outcome === 'accepted') {
              showToast(t('install_success'));
            }
            deferredInstallPrompt = null;
          }).catch(() => { });
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
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/apps/maths/sw.js').then((reg) => {
          swRegistration = reg;
          setupPwaUpdateFlow(reg);
        }).catch(() => { });

        navigator.serviceWorker.addEventListener('controllerchange', () => {
          if (!swRefreshing) {
            swRefreshing = true;
            window.location.reload();
          }
        });
      });

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible' && swRegistration) {
          swRegistration.update().catch(() => {});
        }
      });
    }
  }

  let swRegistration = null;
  let swRefreshing = false;

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
        <span class="update-text">${t('update_available')}</span>
      </div>
      <button id="btn-pwa-apply-update" class="btn-pwa-update-action" title="${t('update_now_btn')}">
        <span>🔄</span> <span>${t('update_now_btn')}</span>
      </button>
    `;

    document.body.appendChild(banner);

    const btn = banner.querySelector('#btn-pwa-apply-update');
    if (btn) {
      btn.addEventListener('click', () => {
        btn.disabled = true;
        btn.innerHTML = `<span>⏳</span> <span>...</span>`;
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

  // Soporte de Teclado Físico y Atajos (0-9, Enter, Tab, T, M, H)
  window.addEventListener('keydown', (e) => {
    // Si pulsa T fuera de inputs, conmuta tema
    if ((e.key === 't' || e.key === 'T') && !e.ctrlKey && !e.metaKey) {
      toggleTheme();
      return;
    }
    // Si pulsa M fuera de inputs, conmuta sonido
    if ((e.key === 'm' || e.key === 'M') && !e.ctrlKey && !e.metaKey) {
      toggleAudio();
      return;
    }
    // Si pulsa H en partida, conmuta pista visual
    if ((e.key === 'h' || e.key === 'H') && inGame && !e.ctrlKey && !e.metaKey) {
      toggleVisualHint();
      return;
    }

    if (!inGame || inFeedbackPause) return;
    if (e.key >= '0' && e.key <= '9') {
      handleNumpadPress(e.key);
    } else if (e.key === 'Backspace') {
      handleNumpadPress('del');
    } else if (e.key === 'Enter') {
      handleNumpadPress('enter');
    } else if (e.key === 'Tab') {
      e.preventDefault();
      if (currentProblem && currentProblem.type === 'division') {
        activeDivisionField = activeDivisionField === 'quo' ? 'rem' : 'quo';
        renderActiveGame(document.getElementById('tab-content'));
      }
    }
  });

  // Inicialización Global
  window.addEventListener('DOMContentLoaded', () => {
    initLang();
    loadStats();
    setupPwa();

    document.getElementById('lang-btn').onclick = () => {
      lang = lang === 'es' ? 'en' : 'es';
      const url = new URL(window.location);
      url.searchParams.set('lang', lang);
      window.history.replaceState({}, '', url);
      renderAll();
    };

    document.getElementById('sound-btn').onclick = toggleAudio;
    document.getElementById('theme-btn').onclick = toggleTheme;

    renderAll();
  });
})();
