// apps/maths/engine.js - Motor aritmético procedural, evaluador y pistas visuales
(function(window) {
  function randInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function pickRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  const MathsEngine = {
    randInt,

    // Genera un reto determinista según nivel
    generateProblem: function(levelId) {
      switch (levelId) {
        case 'l1': {
          // Nivel 1: Sumas de 1 dígito con resultado <= 10
          const a = randInt(1, 5);
          const b = randInt(1, 5);
          return {
            type: 'standard',
            op: '+',
            a, b,
            answer: a + b,
            display: `${a} + ${b} = ?`,
            visual: { type: 'group', a, b, symbol: '🍎' }
          };
        }
        case 'l2': {
          // Nivel 2: Sumas y restas (1-2 dígitos, sin negativos)
          const op = pickRandom(['+', '-']);
          if (op === '+') {
            const a = randInt(2, 9);
            const b = randInt(2, 9);
            return {
              type: 'standard',
              op: '+',
              a, b,
              answer: a + b,
              display: `${a} + ${b} = ?`,
              visual: { type: 'group', a, b, symbol: '⭐' }
            };
          } else {
            let a = randInt(3, 15);
            let b = randInt(1, a); // asegura a >= b
            return {
              type: 'standard',
              op: '-',
              a, b,
              answer: a - b,
              display: `${a} − ${b} = ?`,
              visual: { type: 'takeaway', total: a, remove: b, symbol: '🎈' }
            };
          }
        }
        case 'l3': {
          // Nivel 3: Sumas, Restas y Multiplicación
          const op = pickRandom(['+', '-', '×']);
          if (op === '×') {
            const a = randInt(2, 9);
            const b = randInt(2, 9);
            return {
              type: 'standard',
              op: '×',
              a, b,
              answer: a * b,
              display: `${a} × ${b} = ?`,
              visual: { type: 'grid', rows: a, cols: b, symbol: '🟦' }
            };
          } else if (op === '+') {
            const a = randInt(10, 50);
            const b = randInt(5, 40);
            return {
              type: 'standard',
              op: '+',
              a, b,
              answer: a + b,
              display: `${a} + ${b} = ?`,
              visual: null
            };
          } else {
            let a = randInt(15, 60);
            let b = randInt(5, a);
            return {
              type: 'standard',
              op: '-',
              a, b,
              answer: a - b,
              display: `${a} − ${b} = ?`,
              visual: null
            };
          }
        }
        case 'l4': {
          // Nivel 4: 4 operaciones (División con cociente y resto)
          const op = pickRandom(['+', '-', '×', '÷']);
          if (op === '÷') {
            const divisor = randInt(2, 9);
            const quotient = randInt(1, 9);
            const remainder = randInt(0, divisor - 1);
            const dividend = divisor * quotient + remainder;
            return {
              type: 'division',
              op: '÷',
              dividend,
              divisor,
              quotient,
              remainder,
              display: `${dividend} ÷ ${divisor} = ?`,
              visual: { type: 'share', total: dividend, groups: divisor, quotient, remainder, symbol: '🍪' }
            };
          } else if (op === '×') {
            const a = randInt(3, 12);
            const b = randInt(3, 9);
            return {
              type: 'standard',
              op: '×',
              a, b,
              answer: a * b,
              display: `${a} × ${b} = ?`,
              visual: { type: 'grid', rows: a, cols: b, symbol: '💎' }
            };
          } else if (op === '+') {
            const a = randInt(25, 99);
            const b = randInt(15, 99);
            return { type: 'standard', op: '+', a, b, answer: a + b, display: `${a} + ${b} = ?`, visual: null };
          } else {
            let a = randInt(30, 99);
            let b = randInt(10, a);
            return { type: 'standard', op: '-', a, b, answer: a - b, display: `${a} − ${b} = ?`, visual: null };
          }
        }
        case 'l5': {
          // Nivel 5: Cerebro Ágil (Combinadas e Incógnitas)
          const kind = pickRandom(['combined', 'unknown']);
          if (kind === 'combined') {
            // ej: a + b × c
            const a = randInt(2, 20);
            const b = randInt(2, 8);
            const c = randInt(2, 9);
            const answer = a + (b * c);
            return {
              type: 'standard',
              op: 'combined',
              answer,
              display: `${a} + ${b} × ${c} = ?`,
              hintText: { es: 'Recuerda: la multiplicación se hace primero', en: 'Remember: multiplication comes first' },
              visual: null
            };
          } else {
            // incógnita: a + ? = total
            const a = randInt(12, 50);
            const answer = randInt(5, 40);
            const total = a + answer;
            return {
              type: 'standard',
              op: 'unknown',
              answer,
              display: `${a} + ? = ${total}`,
              hintText: { es: 'Resta el primer número al total', en: 'Subtract the first number from total' },
              visual: null
            };
          }
        }
        case 'l6': {
          // Nivel 6: Leyenda Cuántica (Porcentajes y Potencias)
          const kind = pickRandom(['pct', 'square', 'math_fast']);
          if (kind === 'pct') {
            const pct = pickRandom([10, 20, 25, 50]);
            let base;
            if (pct === 25) base = randInt(1, 10) * 40;
            else if (pct === 50) base = randInt(2, 20) * 10;
            else base = randInt(2, 25) * 10;
            const answer = (pct / 100) * base;
            return {
              type: 'standard',
              op: '%',
              answer,
              display: `${pct}% de ${base} = ?`,
              hintText: { es: `${pct}% equivale a la fracción adecuada`, en: `${pct}% equals the corresponding fraction` },
              visual: null
            };
          } else if (kind === 'square') {
            const num = randInt(6, 16);
            const answer = num * num;
            return {
              type: 'standard',
              op: 'sq',
              answer,
              display: `${num}² = ?`,
              hintText: { es: `Multiplica ${num} por sí mismo`, en: `Multiply ${num} by itself` },
              visual: null
            };
          } else {
            // multiplicación rápida
            const a = randInt(11, 25);
            const b = randInt(3, 9);
            return {
              type: 'standard',
              op: '×',
              a, b,
              answer: a * b,
              display: `${a} × ${b} = ?`,
              visual: null
            };
          }
        }
        default:
          return this.generateProblem('l1');
      }
    },

    // Evalúa si la respuesta proporcionada por el usuario es correcta
    evaluateAnswer: function(problem, userVal, userQuo, userRem) {
      if (problem.type === 'division') {
        const q = parseInt(userQuo, 10);
        const r = parseInt(userRem, 10);
        const isCorrect = (!isNaN(q) && !isNaN(r) && q === problem.quotient && r === problem.remainder);
        return {
          isCorrect,
          correctDisplay: `Cociente: ${problem.quotient}, Resto: ${problem.remainder}`
        };
      } else {
        const val = parseInt(userVal, 10);
        const isCorrect = (!isNaN(val) && val === problem.answer);
        return {
          isCorrect,
          correctDisplay: `${problem.answer}`
        };
      }
    },

    // Generador de HTML para el manipulador visual interactivo
    renderVisualHint: function(visual, lang) {
      if (!visual) {
        return `<div class="p-3 text-center text-sm opacity-80">${lang === 'es' ? '💡 Reto abstracto. ¡Usa tu mente y lápiz si lo necesitas!' : '💡 Abstract challenge. Use your mind or a scratchpad!'}</div>`;
      }

      let html = '<div class="visual-hint-box p-4 rounded-2xl bg-white/70 shadow-inner flex flex-wrap items-center justify-center gap-3">';
      if (visual.type === 'group') {
        // Dos grupos sumándose
        html += `<div class="flex items-center gap-2 bg-sky-50 px-3 py-2 rounded-xl border border-sky-200">`;
        for (let i = 0; i < visual.a; i++) html += `<span class="text-2xl">${visual.symbol}</span>`;
        html += `<strong class="ml-1 text-sky-800">(${visual.a})</strong></div>`;
        html += `<span class="text-2xl font-bold text-sky-600">+</span>`;
        html += `<div class="flex items-center gap-2 bg-amber-50 px-3 py-2 rounded-xl border border-amber-200">`;
        for (let i = 0; i < visual.b; i++) html += `<span class="text-2xl">${visual.symbol}</span>`;
        html += `<strong class="ml-1 text-amber-800">(${visual.b})</strong></div>`;
      } else if (visual.type === 'takeaway') {
        // Resta: muestra el total y tacha los que se quitan
        html += `<div class="flex flex-wrap items-center gap-2 bg-amber-50 px-3 py-2 rounded-xl border border-amber-200">`;
        for (let i = 0; i < visual.total; i++) {
          if (i >= visual.total - visual.remove) {
            html += `<span class="text-2xl opacity-40 line-through filter grayscale">${visual.symbol}</span>`;
          } else {
            html += `<span class="text-2xl">${visual.symbol}</span>`;
          }
        }
        html += `<span class="ml-2 text-sm text-amber-800 font-semibold">${lang === 'es' ? `Había ${visual.total}, quitamos ${visual.remove}` : `There were ${visual.total}, took away ${visual.remove}`}</span></div>`;
      } else if (visual.type === 'grid') {
        // Multiplicación: matriz de filas x columnas
        html += `<div class="inline-grid gap-1 bg-emerald-50 p-3 rounded-xl border border-emerald-200" style="grid-template-columns: repeat(${visual.cols}, minmax(0, 1fr));">`;
        for (let r = 0; r < visual.rows; r++) {
          for (let c = 0; c < visual.cols; c++) {
            html += `<span class="text-xl">${visual.symbol}</span>`;
          }
        }
        html += `</div><div class="text-sm font-semibold text-emerald-800">${visual.rows} ${lang === 'es' ? 'filas' : 'rows'} × ${visual.cols} ${lang === 'es' ? 'columnas' : 'cols'}</div>`;
      } else if (visual.type === 'share') {
        // División: reparto en cajas + resto
        html += `<div class="flex flex-wrap gap-2 justify-center items-center">`;
        for (let g = 0; g < visual.groups; g++) {
          html += `<div class="bg-purple-50 p-2 rounded-xl border-2 border-dashed border-purple-300 text-center min-w-[60px]"><span class="text-xs block text-purple-700 font-bold">${lang === 'es' ? 'Caja' : 'Box'} ${g+1}</span><div class="flex gap-1 justify-center mt-1">`;
          for (let q = 0; q < visual.quotient; q++) html += `<span class="text-xl">${visual.symbol}</span>`;
          html += `</div></div>`;
        }
        if (visual.remainder > 0) {
          html += `<div class="bg-rose-50 p-2 rounded-xl border border-rose-300 text-center"><span class="text-xs block text-rose-700 font-bold">${lang === 'es' ? 'Sobra (Resto)' : 'Leftover (Rem)'}</span><div class="flex gap-1 justify-center mt-1">`;
          for (let rem = 0; rem < visual.remainder; rem++) html += `<span class="text-xl">${visual.symbol}</span>`;
          html += `</div></div>`;
        }
        html += `</div>`;
      }
      html += '</div>';
      return html;
    }
  };

  window.MathsEngine = MathsEngine;
})(window);
