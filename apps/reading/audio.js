// apps/reading/audio.js - Sintetizador Web Audio 8-bit, Web Speech TTS Dual (1.0x / 0.65x tortuga) y confeti en Canvas
(function(window) {
  'use strict';

  let audioCtx = null;
  let soundEnabled = true;

  function initAudio() {
    if (typeof window === 'undefined') return;
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!audioCtx && AudioContextClass) {
      try {
        audioCtx = new AudioContextClass();
      } catch (e) {
        audioCtx = null;
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      try {
        audioCtx.resume();
      } catch (e) {
        // Ignorar bloqueo por política autoplay
      }
    }
  }

  const ReadingAudio = {
    toggleSound: function() {
      soundEnabled = !soundEnabled;
      return soundEnabled;
    },

    isSoundEnabled: function() {
      return soundEnabled;
    },

    setSoundEnabled: function(val) {
      soundEnabled = Boolean(val);
      return soundEnabled;
    },

    playTone: function(freq, type = 'sine', duration = 0.15, gainVal = 0.1) {
      if (!soundEnabled) return;
      initAudio();
      if (!audioCtx) return;

      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

        gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch (e) {
        // Audio no bloqueante en entornos headless o sin permisos
      }
    },

    playSuccess: function(combo = 1) {
      if (!soundEnabled) return;
      initAudio();
      const base = 523.25; // Do5
      const note2 = base * (combo >= 2 ? 1.25 : 1.2);
      const note3 = base * (combo >= 3 ? 1.5 : 1.33);

      this.playTone(base, 'triangle', 0.12, 0.12);
      setTimeout(() => this.playTone(note2, 'triangle', 0.12, 0.12), 80);
      setTimeout(() => this.playTone(note3, 'sine', 0.25, 0.15), 160);
      if (combo >= 5) {
        setTimeout(() => this.playTone(base * 2, 'square', 0.3, 0.08), 240);
      }
    },

    playError: function() {
      if (!soundEnabled) return;
      initAudio();
      this.playTone(280, 'sawtooth', 0.15, 0.06);
      setTimeout(() => this.playTone(220, 'sawtooth', 0.2, 0.06), 120);
    },

    playClick: function() {
      this.playTone(600, 'sine', 0.04, 0.05);
    },

    playWin: function() {
      if (!soundEnabled) return;
      const notes = [440, 554.37, 659.25, 880];
      notes.forEach((freq, idx) => {
        setTimeout(() => this.playTone(freq, 'triangle', 0.2, 0.12), idx * 100);
      });
    },

    /**
     * Pronuncia un texto usando Web Speech API nativa sin llamadas a la nube (INV-READ-3).
     * Soporta velocidad normal (1.0x) y modo tortuga (0.65x).
     * Resiliente si window.speechSynthesis o SpeechSynthesisUtterance no existen.
     */
    speakText: function(text, lang = 'es', rate = 1.0) {
      if (!text || typeof window === 'undefined' || !window.speechSynthesis || typeof window.SpeechSynthesisUtterance === 'undefined') {
        return false;
      }

      try {
        window.speechSynthesis.cancel();

        const UtteranceClass = window.SpeechSynthesisUtterance;
        const utterance = new UtteranceClass(String(text));
        utterance.rate = Math.max(0.5, Math.min(2.0, Number(rate) || 1.0));
        utterance.pitch = 1.0;

        const normLang = String(lang || 'es').toLowerCase();
        const targetLang = normLang.startsWith('en') ? 'en-US' : 'es-ES';
        utterance.lang = targetLang;

        if (typeof window.speechSynthesis.getVoices === 'function') {
          const voices = window.speechSynthesis.getVoices();
          if (Array.isArray(voices) && voices.length > 0) {
            const prefix = normLang.slice(0, 2);
            const matchingVoice = voices.find(v => v && typeof v.lang === 'string' && v.lang.toLowerCase().startsWith(prefix));
            if (matchingVoice) {
              utterance.voice = matchingVoice;
            }
          }
        }

        window.speechSynthesis.speak(utterance);
        return true;
      } catch (e) {
        return false;
      }
    },

    /**
     * Confeti físico sobre canvas sin dependencias externas.
     */
    launchConfetti: function(canvasEl) {
      if (!canvasEl || typeof canvasEl.getContext !== 'function') return;
      const ctx = canvasEl.getContext('2d');
      if (!ctx) return;

      const width = canvasEl.width = canvasEl.offsetWidth || (typeof window !== 'undefined' ? window.innerWidth : 800);
      const height = canvasEl.height = canvasEl.offsetHeight || (typeof window !== 'undefined' ? window.innerHeight : 600);

      const particles = [];
      const colors = ['#0ea5e9', '#f59e0b', '#10b981', '#8b5cf6', '#ec4899', '#f43f5e'];

      for (let i = 0; i < 70; i++) {
        particles.push({
          x: width / 2,
          y: height / 2,
          vx: (Math.random() - 0.5) * 12,
          vy: (Math.random() - 0.7) * 14,
          size: Math.random() * 8 + 4,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: Math.random() * 360,
          vRot: (Math.random() - 0.5) * 10,
          opacity: 1
        });
      }

      let animId = null;
      const raf = (typeof requestAnimationFrame === 'function') ? requestAnimationFrame : (fn => setTimeout(fn, 16));
      const caf = (typeof cancelAnimationFrame === 'function') ? cancelAnimationFrame : clearTimeout;

      function render() {
        ctx.clearRect(0, 0, width, height);
        let active = false;

        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.35; // gravedad
          p.rotation += p.vRot;
          p.opacity -= 0.012;

          if (p.opacity > 0) {
            active = true;
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate((p.rotation * Math.PI) / 180);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = Math.max(0, p.opacity);
            ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
            ctx.restore();
          }
        }

        if (active) {
          animId = raf(render);
        } else {
          ctx.clearRect(0, 0, width, height);
          if (animId !== null) caf(animId);
        }
      }

      render();
    }
  };

  window.ReadingAudio = ReadingAudio;
})(window);
