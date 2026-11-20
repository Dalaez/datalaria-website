"""
apps/reading/tests/test_reading_engine.py
Suite de verificación determinista para Lector Arcade / Reader Arcade (apps/reading/).
Valida el músculo determinista (engine.js), catálogo (catalog.js), controlador audio.js
y las invariantes INV-READ-1, INV-READ-2, INV-READ-5, INV-READ-6, INV-READ-10 e INV-READ-12.
"""
import json
import os
import re
import subprocess
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
READING_APP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
REPO_ROOT = os.path.abspath(os.path.join(READING_APP_DIR, "..", ".."))
STATIC_DIR = os.path.abspath(os.path.join(REPO_ROOT, "static", "apps", "reading"))


def _run_node(js_body: str) -> dict:
    """Ejecuta un script Node.js cargando catalog.js, engine.js y audio.js en un objeto window simulado."""
    wrapper = f"""
    const fs = require('fs');
    const path = require('path');

    const root = {json.dumps(READING_APP_DIR)};
    const catalogCode = fs.readFileSync(path.join(root, 'catalog.js'), 'utf8');
    const illCode = fs.readFileSync(path.join(root, 'illustrations.js'), 'utf8');
    const engineCode = fs.readFileSync(path.join(root, 'engine.js'), 'utf8');
    const audioCode = fs.readFileSync(path.join(root, 'audio.js'), 'utf8');

    const window = global;
    eval(catalogCode);
    eval(illCode);
    eval(engineCode);
    eval(audioCode);

    const catalog = window.READING_CATALOG;
    const illustrations = window.ReadingIllustrations;
    const engine = window.ReadingEngine;
    const audio = window.ReadingAudio;

    {js_body}
    """
    proc = subprocess.run(
        ["node", "-e", wrapper],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, f"Error en Node.js:\nSTDERR: {proc.stderr}\nSTDOUT: {proc.stdout}"
    return json.loads(proc.stdout.strip())


def test_hito_r3_source_files_exist():
    """Verifica que los módulos del motor y catálogo existen en apps/reading/."""
    for fname in ["catalog.js", "engine.js", "audio.js", "tests/test_catalog.js", "tests/test_reading_engine.py"]:
        fpath = os.path.join(READING_APP_DIR, fname)
        assert os.path.exists(fpath), f"Falta archivo requerido: {fpath}"


def test_inv_read_1_and_6_catalog_integrity_and_i18n_parity():
    """INV-READ-1 y INV-READ-6: Integridad de wordBank/sentenceBank y paridad 100% i18n ES/EN."""
    res = _run_node("""
    const esKeys = Object.keys(catalog.i18n.es).sort();
    const enKeys = Object.keys(catalog.i18n.en).sort();
    const parityOk = JSON.stringify(esKeys) === JSON.stringify(enKeys);

    let sylMismatch = [];
    let microErrors = [];
    let sentenceErrors = [];

    for (const lang of ['es', 'en']) {
      const wb = catalog.wordBank[lang];
      for (const lvl of ['l2', 'l3', 'l4']) {
        for (const item of wb[lvl]) {
          if (item.syllables.join('') !== item.word) {
            sylMismatch.push(item.id);
          }
          if (lvl === 'l4') {
            const opts = (item.microCheck && item.microCheck.options) || [];
            const corr = opts.filter(o => o.isCorrect === true).length;
            if (opts.length !== 3 || corr !== 1) microErrors.push(item.id);
          }
        }
      }
      const sb = catalog.sentenceBank[lang];
      for (const [lvl, lineCount] of [['l5', 2], ['l6', 3]]) {
        for (const item of sb[lvl]) {
          if (!Array.isArray(item.lines) || item.lines.length !== lineCount || item.wordCount <= 0) {
            sentenceErrors.push(item.id);
          }
          const opts = (item.microCheck && item.microCheck.options) || [];
          const corr = opts.filter(o => o.isCorrect === true).length;
          if (opts.length !== 3 || corr !== 1) microErrors.push(item.id);
        }
      }
    }

    console.log(JSON.stringify({
      parityOk,
      keyCount: esKeys.length,
      levelsCount: catalog.levels.length,
      modesCount: catalog.modes.length,
      medalsCount: catalog.medals.length,
      sylMismatch,
      microErrors,
      sentenceErrors
    }));
    """)
    assert res["parityOk"] is True
    assert res["keyCount"] >= 80
    assert res["levelsCount"] == 6
    assert res["modesCount"] == 4
    assert res["medalsCount"] == 6
    assert res["sylMismatch"] == []
    assert res["microErrors"] == []
    assert res["sentenceErrors"] == []


def test_inv_read_10_daily_seed_determinism():
    """INV-READ-10: Determinismo absoluto de createSeededRng (Mulberry32) en Reto Diario."""
    res = _run_node("""
    const seed = '2026-12-16_l4';
    const rng1 = engine.createSeededRng(seed);
    const rng2 = engine.createSeededRng(seed);
    const rngDiff = engine.createSeededRng('2026-12-17_l4');

    const seq1 = [];
    const seq2 = [];
    const seqDiff = [];
    for (let i = 0; i < 10; i++) {
      seq1.push(engine.generateChallenge('l4', 'es', rng1));
      seq2.push(engine.generateChallenge('l4', 'es', rng2));
      seqDiff.push(engine.generateChallenge('l4', 'es', rngDiff));
    }

    // Verificar l3 determinista también (teclado y slots)
    const rngL3a = engine.createSeededRng('2026-12-16_l3');
    const rngL3b = engine.createSeededRng('2026-12-16_l3');
    const chL3a = engine.generateChallenge('l3', 'es', rngL3a);
    const chL3b = engine.generateChallenge('l3', 'es', rngL3b);

    console.log(JSON.stringify({
      matchL4: JSON.stringify(seq1) === JSON.stringify(seq2),
      diffDates: JSON.stringify(seq1) !== JSON.stringify(seqDiff),
      matchL3: JSON.stringify(chL3a) === JSON.stringify(chL3b),
      len1: seq1.length
    }));
    """)
    assert res["matchL4"] is True
    assert res["diffDates"] is True
    assert res["matchL3"] is True
    assert res["len1"] == 10


def test_generate_challenge_null_rng_and_all_levels():
    """Robustez ante rng = null | undefined | omitido en los 6 niveles y ambos idiomas."""
    res = _run_node("""
    const levels = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6'];
    const langs = ['es', 'en'];
    const checks = [];

    for (const lang of langs) {
      for (const lvl of levels) {
        const cNull = engine.generateChallenge(lvl, lang, null);
        const cUndef = engine.generateChallenge(lvl, lang, undefined);
        const cOmit = engine.generateChallenge(lvl, lang);

        for (const c of [cNull, cUndef, cOmit]) {
          if (!c || !c.id || !c.prompt || c.wordCount <= 0) {
            throw new Error(`Invalid challenge at ${lang}/${lvl}`);
          }
          if (lvl === 'l1' || lvl === 'l2') {
            if (c.kind !== 'choice' || !Array.isArray(c.choices) || c.choices.length < 4) {
              throw new Error(`Invalid choice challenge at ${lang}/${lvl}`);
            }
          }
          if (lvl === 'l3') {
            const k = c.keyboardChars || [];
            const uniqueK = new Set(k);
            if (c.kind !== 'fill_letters' || k.length < 8 || k.length > 10 || uniqueK.size !== k.length) {
              throw new Error(`Invalid l3 keyboardChars (${k.length}) at ${lang}`);
            }
            for (const slot of c.maskedSlots) {
              if (!k.includes(engine.normalizeChar(slot.expected))) {
                throw new Error(`Missing expected char ${slot.expected} on keyboard`);
              }
            }
          }
          if (lvl === 'l4' || lvl === 'l5' || lvl === 'l6') {
            if (c.kind !== 'read_check' || !c.microCheck || c.microCheck.options.length !== 3) {
              throw new Error(`Invalid microCheck at ${lang}/${lvl}`);
            }
          }
        }
        checks.push(`${lang}_${lvl}`);
      }
    }

    // Verificar recentIds evita repeticiones inmediatas cuando hay alternativas
    const pool0 = catalog.wordBank.es.l2[0].id;
    const rng = engine.createSeededRng('avoid-test');
    let repeated = false;
    for (let i = 0; i < 15; i++) {
      const ch = engine.generateChallenge('l2', 'es', rng, [pool0]);
      if (ch.id === pool0) repeated = true;
    }

    console.log(JSON.stringify({ totalChecked: checks.length, repeated }));
    """)
    assert res["totalChecked"] == 12
    assert res["repeated"] is False


def test_inv_read_12_preserve_n_tilde_and_accents():
    """INV-READ-12: Preservación estricta Ñ !== N y tolerancia opcional de tildes."""
    res = _run_node("""
    const normPinaTilde = engine.normalizeAnswer('piña');
    const normPinaNoTilde = engine.normalizeAnswer('PINA');
    const normPlatanoAcc = engine.normalizeAnswer('Plátano');
    const normPlatanoPlain = engine.normalizeAnswer('PLATANO');
    const normCharLower = engine.normalizeChar('ñ');
    const normCharUpper = engine.normalizeChar('Ñ');
    const normCharN = engine.normalizeChar('n');
    const normEmpty = engine.normalizeChar(null);

    // Evaluación estricta de reto l2 con PIÑA
    const pinaChallenge = {
      id: 'es_l2_26',
      levelId: 'l2',
      lang: 'es',
      kind: 'choice',
      prompt: 'PIÑA',
      wordCount: 1
    };
    const evalLowerTilde = engine.evaluateChallenge(pinaChallenge, 'piña', 'es');
    const evalWrongN = engine.evaluateChallenge(pinaChallenge, 'PINA', 'es');

    // Evaluación en l3 con slots faltantes de PIÑA (índice 2 es Ñ)
    const pinaL3 = {
      id: 'test_pina_l3',
      levelId: 'l3',
      lang: 'es',
      kind: 'fill_letters',
      prompt: 'PIÑA',
      maskedSlots: [{ index: 2, expected: 'Ñ' }]
    };
    const evalL3Right = engine.evaluateChallenge(pinaL3, ['ñ'], 'es');
    const evalL3Wrong = engine.evaluateChallenge(pinaL3, ['N'], 'es');

    console.log(JSON.stringify({
      normPinaTilde,
      normPinaNoTilde,
      pinaDiffersFromPina: normPinaTilde !== normPinaNoTilde,
      platanoMatch: normPlatanoAcc === normPlatanoPlain,
      normCharLower,
      normCharUpper,
      normCharN,
      normEmpty,
      evalLowerTilde: evalLowerTilde.isCorrect,
      evalWrongN: evalWrongN.isCorrect,
      evalL3Right: evalL3Right.isCorrect,
      evalL3Wrong: evalL3Wrong.isCorrect
    }));
    """)
    assert res["normPinaTilde"] == "PIÑA"
    assert res["normPinaNoTilde"] == "PINA"
    assert res["pinaDiffersFromPina"] is True
    assert res["platanoMatch"] is True
    assert res["normCharLower"] == "Ñ"
    assert res["normCharUpper"] == "Ñ"
    assert res["normCharN"] == "N"
    assert res["normEmpty"] == ""
    assert res["evalLowerTilde"] is True
    assert res["evalWrongN"] is False
    assert res["evalL3Right"] is True
    assert res["evalL3Wrong"] is False


def test_inv_read_2_compute_wpm_and_round_score():
    """INV-READ-2: Guardas y precisión determinista de computeWpm() y computeRoundScore()."""
    res = _run_node("""
    const wpmZero = engine.computeWpm(0, 0);
    const wpmNeg = engine.computeWpm(-3, 5000);
    const wpmNull = engine.computeWpm(null, null);
    const wpmExact60 = engine.computeWpm(12, 12000); // (12*60)/12 = 60
    const wpmExact120 = engine.computeWpm(24, 12000); // 120
    const wpmCeiling = engine.computeWpm(10, 0); // elapsedSec clamped to 0.4 -> 1500 -> capped at 350
    const wpmFast = engine.computeWpm(5, 100); // capped at 350

    const scoreNormalClean = engine.computeRoundScore({ mode: 'normal', streak: 0, usedHint: false, elapsedMs: 3000, targetSec: 10 }); // 100*1 + 20 = 120
    const scoreNormalHint = engine.computeRoundScore({ mode: 'normal', streak: 0, usedHint: true, elapsedMs: 3000, targetSec: 10 }); // 100*1 + 0 = 100
    const scoreStopwatchStreak3 = engine.computeRoundScore({ mode: 'stopwatch', streak: 3, usedHint: false, elapsedMs: 5000, targetSec: 10 }); // speed=(10-5)*12=60, (100+60)*2 + 20 = 340
    const scoreDailyStreak5 = engine.computeRoundScore({ mode: 'daily', streak: 5, usedHint: false, elapsedMs: 2000, targetSec: 10 }); // speed=8*12=96, (100+96)*3 + 20 = 608

    console.log(JSON.stringify({
      wpmZero, wpmNeg, wpmNull, wpmExact60, wpmExact120, wpmCeiling, wpmFast,
      scoreNormalClean, scoreNormalHint, scoreStopwatchStreak3, scoreDailyStreak5
    }));
    """)
    assert res["wpmZero"] == 0
    assert res["wpmNeg"] == 0
    assert res["wpmNull"] == 0
    assert res["wpmExact60"] == 60
    assert res["wpmExact120"] == 120
    assert res["wpmCeiling"] == 350
    assert res["wpmFast"] == 350
    assert res["scoreNormalClean"] == 120
    assert res["scoreNormalHint"] == 100
    assert res["scoreStopwatchStreak3"] == 340
    assert res["scoreDailyStreak5"] == 608


def test_evaluate_challenge_all_kinds():
    """Evalúa los 3 tipos de retos (choice, fill_letters, read_check)."""
    res = _run_node("""
    const cChoice = engine.generateChallenge('l2', 'es', engine.createSeededRng('eval-l2'));
    const rChoiceOk = engine.evaluateChallenge(cChoice, { label: cChoice.prompt }, 'es');
    const rChoiceBad = engine.evaluateChallenge(cChoice, 'PALABRA_FALSA', 'es');

    const cFill = engine.generateChallenge('l3', 'en', engine.createSeededRng('eval-l3'));
    const slotsAns = cFill.maskedSlots.map(s => s.expected);
    const rFillSlotsOk = engine.evaluateChallenge(cFill, slotsAns, 'en');
    const rFillFullOk = engine.evaluateChallenge(cFill, cFill.prompt.toLowerCase(), 'en');
    const rFillBad = engine.evaluateChallenge(cFill, ['Z', 'Z'], 'en');

    const cCheck = engine.generateChallenge('l5', 'es', engine.createSeededRng('eval-l5'));
    const correctIdx = cCheck.microCheck.options.findIndex(o => o.isCorrect);
    const wrongIdx = cCheck.microCheck.options.findIndex(o => !o.isCorrect);
    const rCheckIdxOk = engine.evaluateChallenge(cCheck, correctIdx, 'es');
    const rCheckIdxBad = engine.evaluateChallenge(cCheck, wrongIdx, 'es');
    const rCheckLabelOk = engine.evaluateChallenge(cCheck, cCheck.microCheck.options[correctIdx].label, 'es');

    console.log(JSON.stringify({
      rChoiceOk: rChoiceOk.isCorrect,
      rChoiceBad: rChoiceBad.isCorrect,
      rFillSlotsOk: rFillSlotsOk.isCorrect,
      rFillFullOk: rFillFullOk.isCorrect,
      rFillBad: rFillBad.isCorrect,
      rCheckIdxOk: rCheckIdxOk.isCorrect,
      rCheckIdxBad: rCheckIdxBad.isCorrect,
      rCheckLabelOk: rCheckLabelOk.isCorrect
    }));
    """)
    assert res["rChoiceOk"] is True
    assert res["rChoiceBad"] is False
    assert res["rFillSlotsOk"] is True
    assert res["rFillFullOk"] is True
    assert res["rFillBad"] is False
    assert res["rCheckIdxOk"] is True
    assert res["rCheckIdxBad"] is False
    assert res["rCheckLabelOk"] is True


def test_inv_read_5_xss_immunity_and_syllable_tokens():
    """INV-READ-5: Inmunidad XSS en renderVisualHint y renderSyllableTokens + alternancia cromática."""
    res = _run_node("""
    const xssPayload = '<script>alert("xss")</script><img src=x onerror=alert(1)>';
    const sylHtml = engine.renderSyllableTokens(['MA', xssPayload, 'SA'], true);
    const plainHtml = engine.renderSyllableTokens(['CA', 'SA'], false);

    const maliciousChallenge = {
      id: 'xss',
      levelId: 'l4',
      lang: 'es',
      prompt: xssPayload,
      syllables: ['<b onclick=alert(1)>', 'SA'],
      emoji: '<b>⭐</b>'
    };
    const hintHtml = engine.renderVisualHint(maliciousChallenge, 'es');
    const nullHint = engine.renderVisualHint(null, 'en');

    console.log(JSON.stringify({
      sylHasNoScript: !sylHtml.includes('<script>') && !sylHtml.includes('onerror=alert(1)>'),
      sylHasEscaped: sylHtml.includes('&lt;script&gt;'),
      sylHasTwoColors: sylHtml.includes('syl-a') && sylHtml.includes('syl-b'),
      sylHasClaps: sylHtml.includes('clap-dot') && sylHtml.includes('●'),
      plainHasNoColorClasses: !plainHtml.includes('syl-a') && plainHtml.includes('syl-token'),
      hintHasNoRawTag: !hintHtml.includes('<b onclick') && !hintHtml.includes('<b>⭐'),
      nullHintSafe: nullHint.includes('Read syllable by syllable')
    }));
    """)
    assert res["sylHasNoScript"] is True
    assert res["sylHasEscaped"] is True
    assert res["sylHasTwoColors"] is True
    assert res["sylHasClaps"] is True
    assert res["plainHasNoColorClasses"] is True
    assert res["hintHasNoRawTag"] is True
    assert res["nullHintSafe"] is True


def test_reading_audio_headless_and_tts_contract():
    """Verifica que ReadingAudio expone la API completa y es tolerante en entorno sin Web Audio/Speech."""
    res = _run_node("""
    const initialSound = audio.isSoundEnabled();
    const toggledOff = audio.toggleSound();
    const toggledOn = audio.toggleSound();

    // Sin window.speechSynthesis debe devolver false sin lanzar excepción
    const headlessSpeak = audio.speakText('Hola', 'es', 1.0);

    // Probar llamadas de sonido sin AudioContext (no deben lanzar error)
    audio.playClick();
    audio.playSuccess(5);
    audio.playError();
    audio.playWin();

    // Simular Web Speech API para verificar velocidad tortuga 0.65 y códigos de idioma
    const spoken = [];
    window.SpeechSynthesisUtterance = function(t) {
      this.text = t;
      this.rate = 1;
      this.lang = '';
      this.pitch = 1;
    };
    window.speechSynthesis = {
      cancel: () => {},
      getVoices: () => [{ lang: 'es-ES', name: 'Helena' }, { lang: 'en-US', name: 'Zira' }],
      speak: (u) => spoken.push({ text: u.text, rate: u.rate, lang: u.lang, voice: u.voice && u.voice.name })
    };

    const okEsTurtle = audio.speakText('Mariposa', 'es', 0.5);
    const okEnNormal = audio.speakText('Butterfly', 'en', 1.0);

    console.log(JSON.stringify({
      initialSound,
      toggledOff,
      toggledOn,
      headlessSpeak,
      okEsTurtle,
      okEnNormal,
      spoken
    }));
    """)
    assert res["initialSound"] is True
    assert res["toggledOff"] is False
    assert res["toggledOn"] is True
    assert res["headlessSpeak"] is False
    assert res["okEsTurtle"] is True
    assert res["okEnNormal"] is True
    assert res["spoken"][0]["text"] == "Mariposa"
    assert res["spoken"][0]["rate"] == 0.5
    assert res["spoken"][0]["lang"] == "es-ES"
    assert res["spoken"][0]["voice"] == "Helena"
    assert res["spoken"][1]["text"] == "Butterfly"
    assert res["spoken"][1]["rate"] == 1.0
    assert res["spoken"][1]["lang"] == "en-US"
    assert res["spoken"][1]["voice"] == "Zira"



def _read_compiled_bundle() -> str:
    index_html = os.path.join(STATIC_DIR, "index.html")
    assert os.path.exists(index_html), "static/apps/reading/index.html debe existir (ejecuta python apps/reading/build.py)"
    with open(index_html, "r", encoding="utf-8") as f:
        return f.read()


def test_hito_r6_modular_sources_and_compiled_bundle_inline_syntax():
    """Hito R.6: Verifica presencia de todos los módulos fuente y validez sintáctica del bundle inline."""
    required = [
        "catalog.js",
        "engine.js",
        "audio.js",
        "app.js",
        "styles.css",
        "build.py",
        "build_icons.py",
        "manifest.json",
        "sw.js",
        "icon.svg",
    ]
    for fname in required:
        fpath = os.path.join(READING_APP_DIR, fname)
        assert os.path.exists(fpath), f"Falta archivo modular requerido: {fname}"

    html = _read_compiled_bundle()
    assert len(html) > 100000, "El bundle compilado static/apps/reading/index.html parece incompleto"

    node_check = f"""
    const fs = require('fs');
    const vm = require('vm');
    const html = fs.readFileSync({json.dumps(os.path.join(STATIC_DIR, "index.html"))}, 'utf8');
    const scripts = [...html.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)];
    if (scripts.length < 2) throw new Error('Expected at least 2 inline scripts');
    scripts.forEach((m, i) => new vm.Script(m[1], {{ filename: 'inline-' + i }}));
    console.log(JSON.stringify({{ count: scripts.length }}));
    """
    proc = subprocess.run(["node", "-e", node_check], cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, f"Error de sintaxis en scripts inline del bundle: {proc.stderr}"
    res = json.loads(proc.stdout.strip())
    assert res["count"] == 2


def test_inv_read_3_zero_external_dependencies_and_zero_cloud_stt():
    """INV-READ-3: Cero CDNs externos, cero dependencias remotas y cero SpeechRecognition en la nube."""
    html = _read_compiled_bundle()
    styles_path = os.path.join(READING_APP_DIR, "styles.css")
    with open(styles_path, "r", encoding="utf-8") as f:
        styles = f.read()

    forbidden_tokens = [
        "cdn.tailwindcss.com",
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "unpkg.com",
        "cdn.jsdelivr.net",
        "cdnjs.cloudflare.com",
        "webkitSpeechRecognition",
        "SpeechRecognition",
    ]
    for token in forbidden_tokens:
        assert token not in html, f"Violación INV-READ-3: encontrado '{token}' en bundle compilado"
        assert token not in styles, f"Violación INV-READ-3: encontrado '{token}' en styles.css"

    assert not re.search(r'<script[^>]+src=["\']https?://', html, re.IGNORECASE), "Prohibido script CDN externo"
    assert not re.search(r'<link[^>]+href=["\']https?://', html, re.IGNORECASE), "Prohibido link CDN externo"


def test_inv_read_4_shims_and_static_firewall():
    """INV-READ-4: Shims /es/ y /en/ válidos y firewall estricto en static/apps/reading/."""
    assert os.path.exists(STATIC_DIR), "Debe existir static/apps/reading/"

    forbidden_exts = (".py", ".sql", ".env", ".pyc", ".pyo", ".ts")
    forbidden_names = {"index_backup.html", ".git", "__pycache__", ".DS_Store", "Thumbs.db"}

    for root, dirs, files in os.walk(STATIC_DIR):
        for d in dirs:
            assert d not in forbidden_names, f"Violación Firewall static/: carpeta prohibida {d}"
        for fname in files:
            assert fname not in forbidden_names, f"Violación Firewall static/: archivo prohibido {fname}"
            assert not fname.lower().endswith(forbidden_exts), f"Violación Firewall static/: extensión prohibida en {fname}"

    for l_code in ["es", "en"]:
        shim_path = os.path.join(STATIC_DIR, l_code, "index.html")
        assert os.path.exists(shim_path), f"Falta shim retrocompatible {shim_path}"
        with open(shim_path, "r", encoding="utf-8") as f:
            shim_html = f.read()
        assert f"/apps/reading/?lang={l_code}" in shim_html, f"Shim {l_code} no redirige a /apps/reading/?lang={l_code}"


def test_inv_read_6_dual_native_curricula_in_learn_modules():
    """INV-READ-6: Cada idioma carga su propio currículo fonético nativo en learnModules."""
    res = _run_node("""
    const esMods = catalog.learnModules.es;
    const enMods = catalog.learnModules.en;
    console.log(JSON.stringify({
      esKeys: Object.keys(esMods).sort(),
      enKeys: Object.keys(enMods).sort(),
      esLetters: esMods.letters.length,
      enLetters: enMods.letters.length,
      esDirect: esMods.directSyllables.length,
      esInverse: esMods.inverseSyllables.length,
      esComplex: esMods.complexSyllables.length,
      esRules: esMods.rulesAndDigraphs.length,
      esWorkshop: esMods.sentenceWorkshop.length,
      enRimes: enMods.cvcRimes.length,
      enBlends: enMods.blends.length,
      enDigraphs: enMods.digraphs.length,
      enVowels: enMods.vowelTeams.length,
      enWorkshop: enMods.sentenceWorkshop.length
    }));
    """)
    assert res["esKeys"] == ["complexSyllables", "directSyllables", "inverseSyllables", "letters", "rulesAndDigraphs", "sentenceWorkshop"]
    assert res["enKeys"] == ["blends", "cvcRimes", "digraphs", "letters", "sentenceWorkshop", "vowelTeams"]
    assert res["esLetters"] >= 20
    assert res["enLetters"] >= 20
    assert res["esDirect"] >= 8
    assert res["esInverse"] >= 3
    assert res["esComplex"] >= 6
    assert res["esRules"] >= 5
    assert res["esWorkshop"] >= 3
    assert res["enRimes"] >= 4
    assert res["enBlends"] >= 5
    assert res["enDigraphs"] >= 4
    assert res["enVowels"] >= 4
    assert res["enWorkshop"] >= 3


def test_inv_read_7_datalaria_canonical_shell_triad():
    """INV-READ-7: Presencia de la Tríada Canónica de Enlaces Datalaria en el bundle compilado."""
    html = _read_compiled_bundle()
    for elem_id in ['id="datalaria-back-link"', 'id="link-spec"', 'id="link-post"', 'id="link-kits"']:
        assert elem_id in html, f"Falta elemento de cabecera canónica {elem_id}"


def test_inv_read_8_pwa_offline_icons_manifest_and_sw():
    """INV-READ-8: PWA 100% Offline, 6 iconos > 500 bytes, manifest.json, sw.js y update flow."""
    expected_icons = [
        "icon.svg",
        "icon-192.png",
        "icon-512.png",
        "icon-maskable-192.png",
        "icon-maskable-512.png",
        "apple-touch-icon.png",
    ]
    for icon_name in expected_icons:
        p = os.path.join(STATIC_DIR, icon_name)
        assert os.path.exists(p), f"Falta icono PWA {icon_name} en static/apps/reading/"
        assert os.path.getsize(p) > 500, f"Icono {icon_name} demasiado pequeño o corrupto"

    manifest_path = os.path.join(STATIC_DIR, "manifest.json")
    assert os.path.exists(manifest_path), "Falta static/apps/reading/manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        mdata = json.load(f)
    assert mdata.get("display") == "standalone"
    assert mdata.get("start_url") == "/apps/reading/"
    assert mdata.get("scope") == "/apps/reading/"
    maskables = [i for i in mdata.get("icons", []) if i.get("purpose") == "maskable"]
    assert len(maskables) >= 2, "manifest.json debe incluir al menos 2 iconos maskables"
    for m in maskables:
        assert "icon-maskable" in m.get("src", "")

    sw_path = os.path.join(STATIC_DIR, "sw.js")
    assert os.path.exists(sw_path), "Falta static/apps/reading/sw.js"
    with open(sw_path, "r", encoding="utf-8") as f:
        sw_code = f.read()
    assert "PRECACHE_ASSETS" in sw_code
    assert "/apps/reading/index.html" in sw_code
    assert "icon-maskable-512.png" in sw_code
    assert "skipWaiting" in sw_code

    html = _read_compiled_bundle()
    assert 'rel="manifest"' in html
    assert 'href="/apps/reading/manifest.json"' in html
    assert 'apple-touch-icon.png' in html
    assert 'id="btn-install-pwa"' in html
    assert 'id="btn-check-update"' in html
    assert 'setupPwaUpdateFlow' in html
    assert 'pwa-update-banner' in html


def test_inv_read_9_anti_fouc_persistence_and_shortcuts():
    """INV-READ-9: Script inline Anti-FOUC en <head>, persistencia de audio y atajos de teclado."""
    html = _read_compiled_bundle()
    head_section = html.split("</head>")[0]
    assert "localStorage.getItem('pref-theme')" in head_section, "Falta micro-script Anti-FOUC pref-theme en <head>"
    assert "reading-sound" in html
    assert 'id="toast-container"' in html
    assert "addEventListener('keydown'" in html
    assert "Backspace" in html
    assert "Space" in html


def test_inv_read_10_bundle_daily_share_and_mistake_review():
    """INV-READ-10: Integración en bundle de Reto Diario determinista, tira Wordle, compartir y repaso."""
    html = _read_compiled_bundle()
    assert "createSeededRng" in html
    assert 'id="btn-share-result"' in html
    assert "round-blocks-strip" in html
    assert "mistake-review-section" in html


def test_inv_read_11_profiles_and_reading_diploma():
    """INV-READ-11: Perfiles aislados (datalaria_reading_v1_stats_) y generador Diploma PNG."""
    with open(os.path.join(READING_APP_DIR, "catalog.js"), "r", encoding="utf-8") as f:
        cat_code = f.read()
    for marker in ["player_1", "player_2", "adult", "🦁", "🦊", "🦉", "download_diploma_btn", "diploma_card_title"]:
        assert marker in cat_code, f"Falta marcador de perfil/diploma {marker} en catalog.js"

    html = _read_compiled_bundle()
    for marker in [
        'id="profile-bar"',
        "profile-chip",
        "datalaria_reading_v1_stats_",
        "bestWpm",
        "downloadReadingDiploma",
        "btn-arcade-diploma",
        "diploma-promo-card",
    ]:
        assert marker in html, f"Falta componente {marker} en bundle compilado"


def test_inv_read_12_bundle_pedagogy_toggles_and_xss_hygiene():
    """INV-READ-12 y INV-READ-5: Controles AA/Aa, color silábico, ergonomía táctil >= 48px e higiene XSS."""
    html = _read_compiled_bundle()
    for marker in [
        'id="btn-toggle-case"',
        'id="btn-toggle-syllables"',
        "stopwatch-pill",
        'id="btn-read-done"',
        "letter-slot",
        "alpha-pad",
        "alpha-btn",
        "sanitizeStats",
        "engine.escapeHtml",
    ]:
        assert marker in html, f"Falta soporte {marker} en el bundle"

    styles_path = os.path.join(READING_APP_DIR, "styles.css")
    with open(styles_path, "r", encoding="utf-8") as f:
        css = f.read()
    # Verificar dimensiones táctiles mínimas (>= 48px en móvil y >= 52px en desktop)
    assert re.search(r"\.alpha-btn\s*\{[^}]*width:\s*54px;\s*height:\s*56px;", css, re.DOTALL)
    assert re.search(r"\.alpha-btn\s*\{[^}]*width:\s*48px;\s*height:\s*50px;", css, re.DOTALL)


def test_inv_read_13_universal_visuals_and_05x_turtle_audio():
    """INV-READ-13: Compatibilidad Visual Universal, ilustraciones SVG inline (illustrations.js) y audio tortuga a 0.5x."""
    res = _run_node("""
    const requiredSvgs = [
      'MESA', 'NIDO', 'NUDO', 'IGLU', 'FOCA', 'ÑANDÚ', 'RUEDA', 'COMETA',
      'YOYÓ', 'POZO', 'CUBO', 'TRONCO', 'PIEDRA', 'SAPO', 'PARACAÍDAS'
    ];

    const hasAllSvgs = requiredSvgs.every(key => Boolean(illustrations.SVGS[key]));
    const mesaSvg = illustrations.renderVisual('svg:mesa', 'MESA');
    const nudoSvg = illustrations.renderVisual('svg:nudo', 'NUDO');
    const nidoSvg = illustrations.renderVisual('svg:nido', 'NIDO');
    const emojiFallback = illustrations.renderVisual('🦁', 'LEÓN');

    // Verificar saneamiento de banco léxico (sin VINO, con VELA y NUDO)
    const esL2 = catalog.wordBank.es.l2;
    const hasVino = esL2.some(item => item.word === 'VINO');
    const hasVela = esL2.some(item => item.word === 'VELA');
    const hasNudoL2 = esL2.some(item => item.word === 'NUDO');

    const esL3 = catalog.wordBank.es.l3;
    const hasNudoL3 = esL3.some(item => item.word === 'NUDO');

    // Escanear catálogo en busca de emojis Unicode >= 12.0 prohibidos
    const forbiddenCodepoints = [
      0x1faba, // 🪺 nest
      0x1f6de, // 🛞 wheel
      0x1f05b, // 🁛 domino
      0x1f9ad, // 🦭 seal
      0x1f9a4, // 🦤 dodo
      0x1faa3, // 🪣 bucket
      0x1f6d6, // 🛖 hut
      0x1fab5, // 🪵 wood
      0x1faa8, // 🪨 rock
      0x1f9aa, // 🦪 oyster
      0x1fa81, // 🪁 kite
      0x1fa80, // 🪀 yo-yo
      0x1fa82, // 🪂 parachute
      0x1fa91  // 🪑 chair
    ];

    const catalogStr = JSON.stringify(catalog);
    const foundForbidden = [];
    for (let i = 0; i < catalogStr.length; i++) {
      const cp = catalogStr.codePointAt(i);
      if (forbiddenCodepoints.includes(cp)) {
        foundForbidden.push('0x' + cp.toString(16));
      }
    }

    console.log(JSON.stringify({
      hasAllSvgs,
      mesaSvgValid: mesaSvg.includes('<svg') && mesaSvg.includes('class="reading-svg-icon"'),
      nudoSvgValid: nudoSvg.includes('<svg') && nudoSvg.includes('class="reading-svg-icon"'),
      nidoSvgValid: nidoSvg.includes('<svg') && nidoSvg.includes('class="reading-svg-icon"'),
      emojiFallbackValid: emojiFallback.includes('reading-emoji-char') && emojiFallback.includes('🦁'),
      hasVino,
      hasVela,
      hasNudoL2,
      hasNudoL3,
      foundForbiddenCount: foundForbidden.length,
      foundForbidden
    }));
    """)

    assert res["hasAllSvgs"] is True, "Faltan SVGs requeridos en ReadingIllustrations"
    assert res["mesaSvgValid"] is True, "Mesa SVG no es válido"
    assert res["nudoSvgValid"] is True, "Nudo SVG no es válido"
    assert res["nidoSvgValid"] is True, "Nido SVG no es válido"
    assert res["emojiFallbackValid"] is True, "Fallback emoji no es válido"
    assert res["hasVino"] is False, "VINO no debe estar presente en Nivel 2"
    assert res["hasVela"] is True, "VELA debe estar presente en Nivel 2"
    assert res["hasNudoL2"] is True, "NUDO debe estar presente en Nivel 2"
    assert res["hasNudoL3"] is True, "NUDO debe estar presente en Nivel 3"
    assert res["foundForbiddenCount"] == 0, f"Se encontraron emojis prohibidos en catalog: {res['foundForbidden']}"

    # Verificar bundle compilado
    html = _read_compiled_bundle()
    assert "ReadingIllustrations" in html, "Falta ReadingIllustrations en bundle compilado"
    assert "reading-svg-icon" in html, "Falta clase reading-svg-icon en bundle compilado"
    assert "0.5x" in html, "Falta indicador de velocidad tortuga 0.5x en bundle compilado"
    assert 'data-rate="0.5"' in html, "Falta data-rate='0.5' en bundle compilado"


def test_hito_r9_in_app_product_enhancements():
    """Hito R.9 e INV-READ-14: Validación de audio dual con karaoke, estrellas de dominio, modo Mis Palabras, diploma y lámina imprimible."""
    res = _run_node("""
    const stars0 = engine.computeStarsForScore(0);
    const stars1 = engine.computeStarsForScore(450);
    const stars2 = engine.computeStarsForScore(950);
    const stars3 = engine.computeStarsForScore(1500);

    const parsedWords = engine.parseCustomWordsParam('mesa, nido, nudo, <script>alert(1)</script>, niño, camión, piña, mesa');
    const sylMesa = engine.splitCustomSyllables('MESA', 'es');
    const sylEscuela = engine.splitCustomSyllables('ESCUELA', 'es');
    const sylNino = engine.splitCustomSyllables('NIÑO', 'es');

    const customChallenge = engine.generateCustomChallenge(['MESA', 'NIDO', 'PIÑA'], 'es');

    console.log(JSON.stringify({
      stars0,
      stars1,
      stars2,
      stars3,
      parsedWords,
      sylMesaJoined: sylMesa.syllables.join(''),
      sylEscuelaJoined: sylEscuela.syllables.join(''),
      sylNinoJoined: sylNino.syllables.join(''),
      customKind: customChallenge.kind,
      customLevel: customChallenge.levelId,
      customIsCustom: customChallenge.isCustomWord,
      customKeyCharsLen: customChallenge.keyboardChars.length,
      customHasExpected: customChallenge.maskedSlots.every(s => customChallenge.keyboardChars.includes(s.expected))
    }));
    """)

    assert res["stars0"] == 0
    assert res["stars1"] == 1
    assert res["stars2"] == 2
    assert res["stars3"] == 3

    assert "MESA" in res["parsedWords"]
    assert "NIDO" in res["parsedWords"]
    assert "NUDO" in res["parsedWords"]
    assert "NIÑO" in res["parsedWords"]
    assert "PIÑA" in res["parsedWords"]
    assert "CAMIÓN" in res["parsedWords"]
    assert "<script>" not in " ".join(res["parsedWords"]), "Violación anti-XSS: etiquetas HTML sin sanitizar"

    assert res["sylMesaJoined"] == "MESA"
    assert res["sylEscuelaJoined"] == "ESCUELA"
    assert res["sylNinoJoined"] == "NIÑO"

    assert res["customKind"] == "fill_letters"
    assert res["customLevel"] == "l3"
    assert res["customIsCustom"] is True
    assert 8 <= res["customKeyCharsLen"] <= 10
    assert res["customHasExpected"] is True

    # Validar presencia de componentes en bundle compilado
    html = _read_compiled_bundle()
    required_bundle_markers = [
        'id="btn-listen-normal"',
        'id="btn-download-sheet"',
        'downloadPracticeSheet',
        'id="diploma-custom-name"',
        'id="custom-words-input"',
        'id="btn-apply-custom-words"',
        'karaoke-active',
        'level-stars-badge',
        'parents-teachers-card',
        'effective_wpm_label',
        'custom_words_title',
        'v1.1.0'
    ]
    for marker in required_bundle_markers:
        assert marker in html, f"Falta marcador {marker} en static/apps/reading/index.html"


def test_hito_r10_flagship_sheet_embargo_and_covers():
    """Hito R.10: Validación de ficha flagship, embargo editorial Art. 7, KaTeX, deep-links y portadas oficiales v1.1.0."""
    from PIL import Image
    import yaml

    repo_root = os.path.abspath(os.path.join(READING_APP_DIR, "../.."))

    # 1. data/apps/reading.yaml
    yaml_path = os.path.join(repo_root, "data", "apps", "reading.yaml")
    assert os.path.exists(yaml_path), "Falta data/apps/reading.yaml"
    with open(yaml_path, "r", encoding="utf-8") as f:
        raw_yaml = f.read()
        ydata = yaml.safe_load(raw_yaml)

    assert ydata.get("status") == "incubating", "Violación Art. 7: reading debe permanecer status: incubating"
    assert ydata.get("current_version") == "v1.1.0", f"Versión esperada v1.1.0, obtenida {ydata.get('current_version')}"
    assert ydata.get("launch_date") == "2026-12-16", "launch_date debe ser 2026-12-16"
    assert "0.65x" not in raw_yaml, "Quedan referencias obsoletas a 0.65x en data/apps/reading.yaml"
    assert "0.5x" in raw_yaml, "Falta mención a velocidad tortuga 0.5x en data/apps/reading.yaml"

    releases = ydata.get("releases", [])
    assert len(releases) >= 2, "releases debe contener al menos v1.1.0 y v1.0.0"
    assert releases[0].get("version") == "v1.1.0", f"Primera release debe ser v1.1.0, obtenida {releases[0].get('version')}"
    assert releases[1].get("version") == "v1.0.0", f"Segunda release debe ser v1.0.0, obtenida {releases[1].get('version')}"

    # 2. content/{es,en}/apps/reading/index.md
    for l_code in ["es", "en"]:
        md_path = os.path.join(repo_root, "content", l_code, "apps", "reading", "index.md")
        assert os.path.exists(md_path), f"Falta ficha {md_path}"
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        assert "draft: true" in md_content, f"Violación Art. 7: ficha {l_code} debe tener draft: true"
        assert 'date: "2026-12-16"' in md_content, f"Fecha de lanzamiento 2026-12-16 requerida en {l_code}"
        assert "$$" in md_content, f"Faltan fórmulas KaTeX ($$) en ficha {l_code}"
        assert "?words=" in md_content, f"Falta deep-link ?words= en ficha {l_code}"
        assert "?tab=learn" in md_content, f"Falta deep-link ?tab=learn en ficha {l_code}"
        assert "0.65x" not in md_content, f"Quedan referencias obsoletas a 0.65x en ficha {l_code}"
        assert "0.5x" in md_content, f"Falta velocidad 0.5x en ficha {l_code}"
        assert "ReadingIllustrations" in md_content or "SVG" in md_content, f"Falta mención a SVGs en {l_code}"

    # 3. Portadas oficiales cover.png
    for l_code in ["es", "en"]:
        cover_path = os.path.join(repo_root, "content", l_code, "apps", "reading", "cover.png")
        assert os.path.exists(cover_path), f"Falta portada {cover_path}"
        assert os.path.getsize(cover_path) > 20000, f"Portada {cover_path} demasiado pequeña"
        with Image.open(cover_path) as im:
            assert im.size == (1200, 750), f"Dimensiones portada {l_code} deben ser (1200, 750), obtenidas {im.size}"

    # 4. Aislamiento y Embargo en static/apps/pulse/data/public.json
    pulse_public_path = os.path.join(repo_root, "static", "apps", "pulse", "data", "public.json")
    if os.path.exists(pulse_public_path):
        with open(pulse_public_path, "r", encoding="utf-8") as f:
            pdata = json.load(f)
        leaked = [a for a in pdata.get("assets", []) if a.get("slug") == "reading" or a.get("id") == "app-reading"]
        assert len(leaked) == 0, f"Fuga de seguridad Art. 7: reading expuesto en public.json antes de launch_date: {leaked}"

    # 5. Soporte de deep-link ?tab= en bundle compilado
    html = _read_compiled_bundle()
    assert "queryTab" in html or "params.get('tab')" in html, "Falta soporte para ?tab= en el bundle compilado"


def test_hito_r11_printable_kit_factory_and_zip_integrity():
    """Hito R.11: Validación de factoría de Kit Imprimible Comercial ZIP, PyMuPDF, openpyxl y firewall estático."""
    import zipfile
    import fitz
    import openpyxl

    repo_root = os.path.abspath(os.path.join(READING_APP_DIR, "../.."))
    pkg_reading_dir = os.path.join(repo_root, "packages", "reading")
    lemon_dist_dir = os.path.join(repo_root, "packages", "00_DISTRIBUCION_LEMONSQUEEZY")

    zip_path = os.path.join(pkg_reading_dir, "Kit_Imprimible_Lector_Arcade_Dual.zip")
    lemon_zip_path = os.path.join(lemon_dist_dir, "Kit_Imprimible_Lector_Arcade_Dual.zip")

    # 1. Existencia y tamaño del paquete comercial
    assert os.path.exists(zip_path), f"Falta {zip_path}"
    assert os.path.exists(lemon_zip_path), f"Falta copia en {lemon_zip_path}"
    zip_size = os.path.getsize(zip_path)
    assert zip_size > 30000, f"Tamaño del ZIP demasiado pequeño ({zip_size} bytes)"
    assert os.path.getsize(lemon_zip_path) == zip_size, "Desajuste de tamaño entre copia reading y Lemon Squeezy"

    # 2. Contenido exacto del ZIP
    expected_files = [
        "01_Flashcards_Recortables_Silabas_y_Phonics.pdf",
        "02_Cuaderno_Trabajo_Lectoescritura_6_Niveles.pdf",
        "03_Tracker_Fluidez_Lectora_Aula_y_Familia.xlsx",
        "LEEME_GUIA_USO_FAMILIAS_Y_COLEGIOS.md",
        "SHA256SUMS.txt",
    ]
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        for exp in expected_files:
            assert exp in namelist, f"Falta archivo {exp} dentro del ZIP comercial"
        assert len(namelist) == len(expected_files), f"Archivos inesperados en ZIP: {namelist}"

    # 3. Inspección del PDF de Flashcards (fitz)
    fc_pdf_path = os.path.join(pkg_reading_dir, "01_Flashcards_Recortables_Silabas_y_Phonics.pdf")
    doc_fc = fitz.open(fc_pdf_path)
    assert len(doc_fc) == 16, f"Se esperaban 16 páginas en Flashcards, obtenidas {len(doc_fc)}"

    all_fc_text = ""
    for page in doc_fc:
        all_fc_text += page.get_text() + "\n"
    doc_fc.close()

    assert "CARD #001" in all_fc_text, "Falta CARD #001 en Flashcards"
    assert "CARD #060" in all_fc_text, "Falta CARD #060 en Flashcards"
    assert "CARD #061" in all_fc_text, "Falta CARD #061 en Flashcards"
    assert "CARD #120" in all_fc_text, "Falta CARD #120 en Flashcards"
    assert "MESA" in all_fc_text, "Falta MESA en Flashcards"
    assert "NIDO" in all_fc_text, "Falta NIDO en Flashcards"
    assert "NUDO" in all_fc_text, "Falta NUDO en Flashcards"
    assert "\ufffd" not in all_fc_text, "Glifos tofu rotos detectados en Flashcards"

    # 4. Inspección del PDF del Cuaderno (fitz)
    wb_pdf_path = os.path.join(pkg_reading_dir, "02_Cuaderno_Trabajo_Lectoescritura_6_Niveles.pdf")
    doc_wb = fitz.open(wb_pdf_path)
    assert len(doc_wb) == 16, f"Se esperaban 16 páginas en Cuaderno, obtenidas {len(doc_wb)}"

    all_wb_text = ""
    for page in doc_wb:
        all_wb_text += page.get_text() + "\n"
    doc_wb.close()

    for lvl_marker in ["NIVEL 1", "LEVEL 1", "NIVEL 2", "LEVEL 2", "NIVEL 3", "LEVEL 3", "NIVEL 4", "LEVEL 4", "NIVEL 5", "LEVEL 5", "NIVEL 6", "LEVEL 6"]:
        assert lvl_marker in all_wb_text, f"Falta marcador {lvl_marker} en Cuaderno"
    assert "DIPLOMA DE EXCELENCIA LECTORA" in all_wb_text, "Falta Diploma de Excelencia en última página del Cuaderno"
    assert "\ufffd" not in all_wb_text, "Glifos tofu rotos detectados en Cuaderno"

    # 5. Inspección del Tracker Excel (openpyxl)
    xlsx_path = os.path.join(pkg_reading_dir, "03_Tracker_Fluidez_Lectora_Aula_y_Familia.xlsx")
    wb_excel = openpyxl.load_workbook(xlsx_path, data_only=False)
    assert wb_excel.sheetnames == [
        "00_INSTRUCCIONES",
        "01_REGISTRO_SESIONES",
        "02_CUADRO_MANDO_AULA",
        "03_GENERADOR_MIS_PALABRAS"
    ], f"Hojas de Excel inesperadas: {wb_excel.sheetnames}"

    ws_ses = wb_excel["01_REGISTRO_SESIONES"]
    f_j2 = str(ws_ses["J2"].value)
    assert "MIN(350" in f_j2, f"Fórmula J2 de PPM Bruta incorrecta: {f_j2}"
    f_k2 = str(ws_ses["K2"].value)
    assert "J2" in f_k2 and "I2" in f_k2, f"Fórmula K2 de PPM Efectiva incorrecta: {f_k2}"

    ws_gen = wb_excel["03_GENERADOR_MIS_PALABRAS"]
    f_b18 = str(ws_gen["B18"].value)
    assert "?words=" in f_b18 and "lang=es" in f_b18, f"Fórmula B18 de generador incorrecta: {f_b18}"
    wb_excel.close()

    # 6. Firewall estático de static/apps/reading/
    static_reading = os.path.join(repo_root, "static", "apps", "reading")
    for fname in os.listdir(static_reading):
        ext = os.path.splitext(fname)[1].lower()
        assert ext not in [".zip", ".pdf", ".xlsx", ".py", ".sql", ".env"], f"Fuga de archivo no público {fname} en static/apps/reading/"




