// apps/maths/audio.js - Sintetizador nativo procedural con Web Audio API y confeti físico
(function(window) {
  let audioCtx = null;
  let soundEnabled = true;

  function initAudio() {
    if (!audioCtx && (window.AudioContext || window.webkitAudioContext)) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContextClass();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  const MathsAudio = {
    toggleSound: function() {
      soundEnabled = !soundEnabled;
      return soundEnabled;
    },
    isSoundEnabled: function() {
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
        // Ignorar de forma resiliente si el navegador bloquea audio
      }
    },

    playSuccess: function(combo = 1) {
      if (!soundEnabled) return;
      initAudio();
      // Arpegio alegre ascendente
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
      // Tono descendente suave tipo "oh-oh"
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

    // Confeti físico sobre canvas
    launchConfetti: function(canvasEl) {
      if (!canvasEl) return;
      const ctx = canvasEl.getContext('2d');
      const width = canvasEl.width = canvasEl.offsetWidth;
      const height = canvasEl.height = canvasEl.offsetHeight;

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

      let animId;
      function render() {
        ctx.clearRect(0, 0, width, height);
        let active = false;

        particles.forEach(p => {
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
        });

        if (active) {
          animId = requestAnimationFrame(render);
        } else {
          ctx.clearRect(0, 0, width, height);
          cancelAnimationFrame(animId);
        }
      }

      render();
    }
  };

  window.MathsAudio = MathsAudio;
})(window);
