#!/usr/bin/env node
/*
Wave precheck + optional normalization.

Usage:
  node scripts/wave-precheck.js --base data/profiles.json --wave ..\\wave7.json
  node scripts/wave-precheck.js --base data/profiles.json --wave ..\\wave7.json --write

What it does:
  - Loads base dataset + wave array
  - Applies id aliases from scripts/id-aliases.json
  - Reports:
      * ids in wave
      * how many already exist (by id)
      * how many would be added
      * alias rewrites performed
      * name collisions (same name, different id)
      * suggested canonical IDs (by exact name match)
  - With --write: rewrites the wave file with normalized IDs
*/

const fs = require('fs');
const path = require('path');

function arg(name) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : null;
}

const basePath = arg('--base') || 'data/profiles.json';
const wavePath = arg('--wave');
const doWrite = process.argv.includes('--write');

if (!wavePath) {
  console.error('Usage: node scripts/wave-precheck.js --base data/profiles.json --wave <wave.json> [--write]');
  process.exit(2);
}

function readJson(p) {
  const raw = fs.readFileSync(p);
  // tolerate UTF-8 BOM
  const text = raw.toString('utf8').replace(/^\uFEFF/, '');
  return JSON.parse(text);
}

const repoRoot = path.resolve(__dirname, '..');
const aliasesPath = path.resolve(__dirname, 'id-aliases.json');
const aliases = fs.existsSync(aliasesPath) ? (readJson(aliasesPath).aliases || {}) : {};

const base = readJson(path.resolve(repoRoot, basePath));
const baseProfiles = base.profiles || [];

const baseById = new Map(baseProfiles.map(p => [p.id, p]));
const baseByNameLower = new Map();
for (const p of baseProfiles) {
  const k = String(p.name || '').trim().toLowerCase();
  if (!k) continue;
  if (!baseByNameLower.has(k)) baseByNameLower.set(k, []);
  baseByNameLower.get(k).push(p);
}

const wave = readJson(path.resolve(repoRoot, wavePath));
if (!Array.isArray(wave)) {
  console.error('Wave file must be a JSON array of profiles.');
  process.exit(2);
}

const rewritten = [];
const rewrites = [];

for (const p of wave) {
  const orig = p.id;
  const mapped = aliases[orig] || orig;
  if (mapped !== orig) {
    rewrites.push({ from: orig, to: mapped, name: p.name });
  }
  rewritten.push({ ...p, id: mapped });
}

// duplicate IDs within wave
const waveIds = rewritten.map(p => p.id);
const dupIds = [...new Set(waveIds.filter((id, i) => waveIds.indexOf(id) !== i))];

const present = [];
const missing = [];
for (const p of rewritten) {
  (baseById.has(p.id) ? present : missing).push(p);
}

const nameCollisions = [];
const suggestions = [];
for (const p of rewritten) {
  const k = String(p.name || '').trim().toLowerCase();
  const matches = baseByNameLower.get(k) || [];
  if (matches.length) {
    const exactIds = matches.map(x => x.id);
    if (!exactIds.includes(p.id)) {
      suggestions.push({ waveId: p.id, waveName: p.name, suggestedIds: exactIds });
      nameCollisions.push({ waveId: p.id, waveName: p.name, existing: matches.map(x => ({ id: x.id, status: x.status })) });
    }
  }
}

console.log('--- Wave precheck ---');
console.log('base:', basePath, 'profiles:', baseProfiles.length, 'version:', base.version);
console.log('wave:', wavePath, 'profiles:', rewritten.length);

console.log('\nID alias rewrites:', rewrites.length);
for (const r of rewrites) console.log(`  ${r.from} -> ${r.to}  (${r.name || ''})`);

console.log('\nDuplicates within wave:', dupIds.length);
if (dupIds.length) console.log('  ', dupIds.join(', '));

console.log('\nPresent in base (by id):', present.length);
console.log('Would be added (new ids):', missing.length);

if (missing.length) {
  console.log('\nNew IDs:');
  for (const p of missing) console.log(`  ${p.id}  (${p.name || ''})`);
}

if (suggestions.length) {
  console.log('\nName-based canonical ID suggestions (exact name match):');
  for (const s of suggestions) {
    console.log(`  wave ${s.waveName} [${s.waveId}] -> consider existing id(s): ${s.suggestedIds.join(', ')}`);
  }
}

if (dupIds.length) {
  console.error('\nERROR: duplicate IDs inside wave after normalization. Fix before merging.');
  process.exit(1);
}

if (doWrite) {
  fs.writeFileSync(path.resolve(repoRoot, wavePath), JSON.stringify(rewritten, null, 2) + '\n', 'utf8');
  console.log('\nWrote normalized wave file:', wavePath);
}
