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
    const engineCode = fs.readFileSync(path.join(root, 'engine.js'), 'utf8');
    const audioCode = fs.readFileSync(path.join(root, 'audio.js'), 'utf8');

    const window = global;
    eval(catalogCode);
    eval(engineCode);
    eval(audioCode);

    const catalog = window.READING_CATALOG;
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

    const okEsTurtle = audio.speakText('Mariposa', 'es', 0.65);
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
    assert res["spoken"][0]["rate"] == 0.65
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
