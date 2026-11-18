/**
 * apps/reading/tests/test_catalog.js
 * Node.js automated test suite for window.READING_CATALOG
 * Verifies INV-READ-1, bilingual parity, syllable integrity, and microCheck consistency.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

console.log('--- [NODE QA GATE] Auditing apps/reading/catalog.js ---');

const catalogPath = path.resolve(__dirname, '..', 'catalog.js');
assert(fs.existsSync(catalogPath), `Catalog file not found at ${catalogPath}`);

// 1. Evaluate catalog in a clean sandbox with mocked window
const fileCode = fs.readFileSync(catalogPath, 'utf-8');
const context = { window: {} };
vm.createContext(context);

try {
  vm.runInContext(fileCode, context);
  console.log('✓ Syntax check PASSED: catalog.js evaluated cleanly.');
} catch (err) {
  console.error('❌ Syntax error in catalog.js:', err);
  process.exit(1);
}

const catalog = context.window.READING_CATALOG;
assert(catalog, 'window.READING_CATALOG must be defined on window.');

// 2. Levels check
assert(Array.isArray(catalog.levels) && catalog.levels.length === 6, 'Must contain exactly 6 levels (l1..l6)');
const expectedLevelIds = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6'];
catalog.levels.forEach((lvl, i) => {
  assert.strictEqual(lvl.id, expectedLevelIds[i]);
  assert(lvl.icon && lvl.range, `Level ${lvl.id} missing icon or range`);
  assert(lvl.name && lvl.name.es && lvl.name.en, `Level ${lvl.id} missing bilingual name`);
  assert(lvl.desc && lvl.desc.es && lvl.desc.en, `Level ${lvl.id} missing bilingual desc`);
});
console.log('✓ Levels check PASSED (6 adaptive levels l1..l6 configured).');

// 3. Modes check
assert(Array.isArray(catalog.modes) && catalog.modes.length === 4, 'Must contain exactly 4 modes');
const expectedModeIds = ['normal', 'stopwatch', 'sprint', 'daily'];
catalog.modes.forEach((mode, i) => {
  assert.strictEqual(mode.id, expectedModeIds[i]);
  assert(mode.icon && mode.name.es && mode.name.en && mode.desc.es && mode.desc.en);
});
console.log('✓ Modes check PASSED (normal, stopwatch, sprint, daily).');

// 4. Profiles check
assert(Array.isArray(catalog.profiles) && catalog.profiles.length === 3, 'Must contain exactly 3 profiles');
const expectedProfileIds = ['player_1', 'player_2', 'adult'];
catalog.profiles.forEach((p, i) => {
  assert.strictEqual(p.id, expectedProfileIds[i]);
  assert(p.avatar && p.name.es && p.name.en && p.title.es && p.title.en);
});
console.log('✓ Profiles check PASSED (player_1 🦁, player_2 🦊, adult 🦉).');

// 5. Medals check
assert(Array.isArray(catalog.medals) && catalog.medals.length === 6, 'Must contain exactly 6 medals');
const expectedMedalIds = ['first_win', 'streak_5', 'streak_10', 'syllable_master', 'speed_reader', 'storyteller'];
catalog.medals.forEach((m, i) => {
  assert.strictEqual(m.id, expectedMedalIds[i]);
  assert(m.icon && m.name.es && m.name.en && m.desc.es && m.desc.en);
});
console.log('✓ Medals check PASSED (6 arcade collectible medals).');

// 6. Learn Modules check
assert(catalog.learnModules.es && catalog.learnModules.en, 'Must have bilingual learnModules');
assert(catalog.learnModules.es.letters.length >= 20, 'ES letters >= 20');
assert(catalog.learnModules.es.directSyllables.length >= 10, 'ES directSyllables >= 10');
assert(catalog.learnModules.es.inverseSyllables.length >= 4, 'ES inverseSyllables >= 4');
assert(catalog.learnModules.es.complexSyllables.length >= 8, 'ES complexSyllables >= 8');
assert(catalog.learnModules.es.rulesAndDigraphs.length >= 7, 'ES rulesAndDigraphs >= 7');
assert(catalog.learnModules.es.sentenceWorkshop.length >= 4, 'ES sentenceWorkshop >= 4');

assert(catalog.learnModules.en.letters.length >= 20, 'EN letters >= 20');
assert(catalog.learnModules.en.cvcRimes.length >= 7, 'EN cvcRimes >= 7');
assert(catalog.learnModules.en.blends.length >= 8, 'EN blends >= 8');
assert(catalog.learnModules.en.digraphs.length >= 6, 'EN digraphs >= 6');
assert(catalog.learnModules.en.vowelTeams.length >= 6, 'EN vowelTeams >= 6');
assert(catalog.learnModules.en.sentenceWorkshop.length >= 4, 'EN sentenceWorkshop >= 4');
console.log('✓ Learn Modules check PASSED (Letters, Syllables, Digraphs, Phonics and Workshop in ES & EN).');

// 7. WordBank check (INV-READ-1)
['es', 'en'].forEach(lang => {
  const bank = catalog.wordBank[lang];
  assert(bank, `WordBank for ${lang} must exist`);

  // l1: >= 20 items
  assert(bank.l1.length >= 20, `[${lang}] l1 must have >= 20 items, got ${bank.l1.length}`);
  bank.l1.forEach(item => {
    assert(item.id && item.target && item.anchorWord && item.emoji, `Invalid l1 item: ${JSON.stringify(item)}`);
    assert(Array.isArray(item.distractors) && item.distractors.length === 3, `l1 item ${item.id} must have 3 distractors`);
  });

  // l2: >= 24 items, syllables.join('') === word
  assert(bank.l2.length >= 24, `[${lang}] l2 must have >= 24 items, got ${bank.l2.length}`);
  bank.l2.forEach(item => {
    assert(item.id && item.word && Array.isArray(item.syllables) && item.emoji, `Invalid l2 item: ${JSON.stringify(item)}`);
    assert.strictEqual(item.syllables.join(''), item.word, `[${lang}][l2] INV-READ-1 violation in ${item.id}: '${item.syllables.join('')}' !== '${item.word}'`);
    assert(Array.isArray(item.distractors) && item.distractors.length >= 3, `l2 item ${item.id} must have >= 3 distractors`);
  });

  // l3: >= 24 items, syllables.join('') === word, missingIndices valid
  assert(bank.l3.length >= 24, `[${lang}] l3 must have >= 24 items, got ${bank.l3.length}`);
  bank.l3.forEach(item => {
    assert(item.id && item.word && Array.isArray(item.syllables) && item.emoji, `Invalid l3 item: ${JSON.stringify(item)}`);
    assert.strictEqual(item.syllables.join(''), item.word, `[${lang}][l3] INV-READ-1 violation in ${item.id}: '${item.syllables.join('')}' !== '${item.word}'`);
    assert(Array.isArray(item.missingIndices) && item.missingIndices.length >= 1, `l3 item ${item.id} must have missingIndices`);
    item.missingIndices.forEach(idx => {
      assert(idx >= 0 && idx < item.word.length, `l3 item ${item.id} index ${idx} out of range [0, ${item.word.length})`);
    });
  });

  // l4: >= 24 items, syllables.join('') === word, microCheck with 3 options and exactly 1 correct
  assert(bank.l4.length >= 24, `[${lang}] l4 must have >= 24 items, got ${bank.l4.length}`);
  bank.l4.forEach(item => {
    assert(item.id && item.word && Array.isArray(item.syllables) && item.emoji, `Invalid l4 item: ${JSON.stringify(item)}`);
    assert.strictEqual(item.syllables.join(''), item.word, `[${lang}][l4] INV-READ-1 violation in ${item.id}: '${item.syllables.join('')}' !== '${item.word}'`);
    assert(item.microCheck && item.microCheck.question, `l4 item ${item.id} missing microCheck question`);
    assert(Array.isArray(item.microCheck.options) && item.microCheck.options.length === 3, `l4 item ${item.id} must have exactly 3 options`);
    const correctCount = item.microCheck.options.filter(o => o.isCorrect === true).length;
    assert.strictEqual(correctCount, 1, `l4 item ${item.id} must have exactly 1 option with isCorrect: true, found ${correctCount}`);
  });
});
console.log('✓ WordBank check PASSED (100% syllable integrity INV-READ-1, verified l1..l4 in ES and EN).');

// 8. SentenceBank check (lines and microCheck)
['es', 'en'].forEach(lang => {
  const sbank = catalog.sentenceBank[lang];
  assert(sbank, `SentenceBank for ${lang} must exist`);

  // l5: >= 16 items, 2 lines, exact microCheck
  assert(sbank.l5.length >= 16, `[${lang}] l5 must have >= 16 items, got ${sbank.l5.length}`);
  sbank.l5.forEach(item => {
    assert(item.id && Array.isArray(item.lines) && item.lines.length === 2, `l5 item ${item.id} must have exactly 2 lines`);
    assert(typeof item.wordCount === 'number' && item.wordCount > 0, `l5 item ${item.id} missing positive wordCount`);
    assert(item.microCheck && item.microCheck.question, `l5 item ${item.id} missing microCheck`);
    assert(Array.isArray(item.microCheck.options) && item.microCheck.options.length === 3, `l5 item ${item.id} must have 3 options`);
    const correctCount = item.microCheck.options.filter(o => o.isCorrect === true).length;
    assert.strictEqual(correctCount, 1, `l5 item ${item.id} must have exactly 1 option with isCorrect: true`);
  });

  // l6: >= 14 items, 3 lines, exact microCheck
  assert(sbank.l6.length >= 14, `[${lang}] l6 must have >= 14 items, got ${sbank.l6.length}`);
  sbank.l6.forEach(item => {
    assert(item.id && Array.isArray(item.lines) && item.lines.length === 3, `l6 item ${item.id} must have exactly 3 lines`);
    assert(typeof item.wordCount === 'number' && item.wordCount > 0, `l6 item ${item.id} missing positive wordCount`);
    assert(item.microCheck && item.microCheck.question, `l6 item ${item.id} missing microCheck`);
    assert(Array.isArray(item.microCheck.options) && item.microCheck.options.length === 3, `l6 item ${item.id} must have 3 options`);
    const correctCount = item.microCheck.options.filter(o => o.isCorrect === true).length;
    assert.strictEqual(correctCount, 1, `l6 item ${item.id} must have exactly 1 option with isCorrect: true`);
  });
});
console.log('✓ SentenceBank check PASSED (l5 2-line & l6 3-line stories with verified wordCount and microCheck).');

// 9. i18n Parity Check (100% key parity)
const esKeys = Object.keys(catalog.i18n.es).sort();
const enKeys = Object.keys(catalog.i18n.en).sort();
assert.strictEqual(esKeys.length, enKeys.length, `Key counts differ: ES=${esKeys.length}, EN=${enKeys.length}`);
assert.deepStrictEqual(esKeys, enKeys, 'i18n keys between es and en must match 100%');
console.log(`✓ i18n parity check PASSED (100% parity across all ${esKeys.length} translation keys).`);

console.log('--- ALL NODE.JS VERIFICATION CHECKS PASSED WITH EXIT CODE 0 ---');
