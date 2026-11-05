// apps/maths/app.js - Controlador reactivo de interfaz, audio y estado local
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

  // Persistencia Local
  const STORAGE_KEY = 'datalaria_maths_v2_stats';
  let userStats = {
    highScores: {},
    bestStreakEver: 0,
    unlockedMedals: []
  };

  function loadStats() {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      if (data) userStats = JSON.parse(data);
    } catch (e) { }
  }

  function saveStats() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userStats));
    } catch (e) { }
  }

  // Detectar idioma inicial por URL o navegador
  function initLang() {
    const params = new URLSearchParams(window.location.search);
    const urlLang = params.get('lang');
    if (urlLang === 'en' || urlLang === 'es') {
      lang = urlLang;
    } else {
      lang = (navigator.language && navigator.language.startsWith('en')) ? 'en' : 'es';
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
        if (inGame && !confirm(lang === 'es' ? '¿Salir de la partida en curso?' : 'Leave current game?')) return;
        endGameSession();
        activeTab = btn.getAttribute('data-tab');
        renderAll();
      };
    });
  }

  // Pestaña Jugar
  function renderPlayTab() {
    const container = document.getElementById('tab-content');
    if (!inGame) {
      // Pantalla de configuración y selección
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

      // Eventos de selección
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
      // Pantalla de juego activa
      renderActiveGame(container);
    }
  }

  function renderActiveGame(container) {
    const isDivision = currentProblem && currentProblem.type === 'division';
    let roundLabel = '';
    if (selectedMode === 'classic') roundLabel = `${t('round')} ${roundIndex}/${TOTAL_ROUNDS}`;
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

    // Configuración de eventos en partida
    document.getElementById('btn-exit-game').onclick = () => {
      if (confirm(lang === 'es' ? '¿Salir al menú principal?' : 'Exit to main menu?')) {
        endGameSession();
        renderPlayTab();
      }
    };

    document.getElementById('btn-toggle-hint').onclick = () => {
      isHintVisible = !isHintVisible;
      const hintEl = document.getElementById('hint-container');
      const btnEl = document.getElementById('btn-toggle-hint');
      if (isHintVisible) {
        hintEl.classList.remove('hidden');
        btnEl.textContent = t('hide_hint');
      } else {
        hintEl.classList.add('hidden');
        btnEl.textContent = t('visual_hint');
      }
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

  function handleNumpadPress(key) {
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
      // Es un número
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

    // Actualización rápida de display sin re-renderizar todo
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
    if (!currentProblem) return;
    const isDivision = currentProblem.type === 'division';
    if (!isDivision && inputVal === '') return;
    if (isDivision && (inputQuo === '' || inputRem === '')) return;

    const evaluation = engine.evaluateAnswer(currentProblem, inputVal, inputQuo, inputRem);
    handleAnswerSubmit(evaluation.isCorrect, false, evaluation.correctDisplay);
  }

  function handleAnswerSubmit(isCorrect, isSkipped = false, correctDisplay = '') {
    clearInterval(timerInterval);

    if (isCorrect) {
      streak += 1;
      if (streak > bestStreak) bestStreak = streak;
      correctCount += 1;
      const multiplier = streak >= 5 ? 3 : (streak >= 3 ? 2 : 1);
      const pointsEarned = Math.round((100 + (selectedMode === 'classic' ? timeLeft * 10 : 0)) * multiplier);
      score += pointsEarned;
      audio.playSuccess(streak);

      // Si es Time Attack y racha de 5, añade +3s
      if (selectedMode === 'time_attack' && streak > 0 && streak % 5 === 0) {
        timeLeft = Math.min(60, timeLeft + 3);
      }
    } else {
      streak = 0;
      wrongCount += 1;
      if (!isSkipped) audio.playError();
    }

    checkMedalsProgress();

    // Siguiente ronda o fin
    if (selectedMode === 'classic' && roundIndex >= TOTAL_ROUNDS) {
      finishGame();
    } else if (selectedMode === 'time_attack' && timeLeft <= 0) {
      finishGame();
    } else {
      nextProblem();
    }
  }

  function startGameSession() {
    inGame = true;
    roundIndex = 0;
    score = 0;
    correctCount = 0;
    wrongCount = 0;
    streak = 0;
    bestStreak = 0;
    isHintVisible = false;

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
    currentProblem = engine.generateProblem(selectedLevel);

    if (selectedMode === 'classic') {
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
      timeLeft -= 0.1;
      const fillEl = document.getElementById('timer-bar-fill');
      if (fillEl) {
        const pct = Math.max(0, (timeLeft / timeTotal) * 100);
        fillEl.style.width = pct + '%';
      }

      if (timeLeft <= 0) {
        clearInterval(timerInterval);
        handleAnswerSubmit(false, false, currentProblem ? (currentProblem.answer || currentProblem.quotient) : '');
      }
    }, 100);
  }

  function finishGame() {
    clearInterval(timerInterval);
    inGame = false;
    audio.playWin();

    // Guardar mejores puntuaciones
    if (!userStats.highScores[selectedLevel] || score > userStats.highScores[selectedLevel]) {
      userStats.highScores[selectedLevel] = score;
    }
    if (bestStreak > userStats.bestStreakEver) {
      userStats.bestStreakEver = bestStreak;
    }
    saveStats();

    // Modal de resumen
    const container = document.getElementById('tab-content');
    const accuracy = (roundIndex > 0) ? Math.round((correctCount / roundIndex) * 100) : 0;

    let html = `
      <div class="card text-center" style="position: relative;">
        <canvas id="confetti-canvas"></canvas>
        <div style="font-size: 4rem; margin-bottom: 12px;">🏆</div>
        <h2 style="font-size: 2rem; font-weight: 800; color: var(--text-primary);">${t('game_over')}</h2>
        
        <div style="display: flex; gap: 16px; justify-content: center; margin: 24px 0; flex-wrap: wrap;">
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">⭐ ${t('points')}: <strong>${score}</strong></div>
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">🎯 ${t('accuracy')}: <strong>${accuracy}%</strong></div>
          <div class="stat-chip" style="font-size: 1.1rem; padding: 10px 18px;">🔥 ${t('best_streak')}: <strong>${bestStreak}</strong></div>
        </div>

        <div style="display: flex; gap: 12px; justify-content: center; margin-top: 24px;">
          <button id="btn-again" class="btn-arcade btn-arcade-primary" style="font-size: 1.1rem; padding: 12px 24px;">
            ${t('play_again')}
          </button>
          <button id="btn-badges" class="btn-arcade" style="font-size: 1.1rem; padding: 12px 24px;">
            ${t('view_achievements')}
          </button>
        </div>
      </div>
    `;
    container.innerHTML = html;

    const canvas = document.getElementById('confetti-canvas');
    if (canvas) audio.launchConfetti(canvas);

    document.getElementById('btn-again').onclick = () => {
      startGameSession();
    };
    document.getElementById('btn-badges').onclick = () => {
      activeTab = 'achievements';
      renderAll();
    };
  }

  function endGameSession() {
    clearInterval(timerInterval);
    inGame = false;
  }

  // Verificación de Medallas
  function checkMedalsProgress() {
    function unlock(medalId) {
      if (!userStats.unlockedMedals.includes(medalId)) {
        userStats.unlockedMedals.push(medalId);
        saveStats();
      }
    }

    if (correctCount >= 1) unlock('first_win');
    if (streak >= 5) unlock('streak_5');
    if (streak >= 10) unlock('streak_10');
    if (currentProblem && currentProblem.type === 'division') unlock('div_master');
    if ((selectedLevel === 'l5' || selectedLevel === 'l6') && correctCount >= 8) unlock('brain_power');
    if (selectedMode === 'time_attack' && correctCount >= 12) unlock('time_hero');
  }

  // Pestaña Aprender (Laboratorio Didáctico)
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

  // Pestaña Logros & Medallas
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

        <div style="text-align: center; margin-top: 30px;">
          <button id="btn-reset-stats" class="btn-arcade btn-arcade-danger" style="font-size: 0.85rem;">
            ${t('clean_history')}
          </button>
        </div>
      </div>
    `;
    container.innerHTML = html;

    document.getElementById('btn-reset-stats').onclick = () => {
      if (confirm(t('confirm_reset'))) {
        userStats = { highScores: {}, bestStreakEver: 0, unlockedMedals: [] };
        saveStats();
        renderAchievementsTab();
      }
    };
  }

  // Soporte de Teclado Físico en PC
  window.addEventListener('keydown', (e) => {
    if (!inGame) return;
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

    // Controles Shell
    document.getElementById('lang-btn').onclick = () => {
      lang = lang === 'es' ? 'en' : 'es';
      const url = new URL(window.location);
      url.searchParams.set('lang', lang);
      window.history.replaceState({}, '', url);
      renderAll();
    };

    document.getElementById('sound-btn').onclick = () => {
      audio.toggleSound();
      document.getElementById('sound-btn').textContent = audio.isSoundEnabled() ? '🔊' : '🔇';
    };

    document.getElementById('theme-btn').onclick = () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
    };

    renderAll();
  });
})();
