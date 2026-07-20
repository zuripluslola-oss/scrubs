#!/usr/bin/env node
/*
 * Loads the prototype's content (../data) into the database.
 *   node scripts/import-content.mjs         → upsert into the DB (needs DATABASE_URL)
 *   node scripts/import-content.mjs --dry    → just parse & count (no DB needed)
 *
 * Mirrors the loaders in ../tools/build_pages.py so the app and the static
 * prototype stay in sync. Idempotent: safe to re-run.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA = resolve(__dirname, '..', '..', 'data');
const DRY = process.argv.includes('--dry');

function readBatch(dir, key) {
  const full = join(DATA, dir);
  if (!existsSync(full)) return [];
  const out = [];
  for (const f of readdirSync(full).filter((f) => f.endsWith('.json')).sort()) {
    const doc = JSON.parse(readFileSync(join(full, f), 'utf8'));
    for (const item of doc[key] || []) out.push(item);
  }
  return out;
}

const LEVEL = { Easy: 2, Moderate: 3, Hard: 4 };

function loadQuestions() {
  const seen = new Set();
  const rows = [];
  for (const q of readBatch('qbank', 'questions')) {
    if (!q.id || seen.has(q.id)) continue;
    const type = q.type || 'mc';
    if (type === 'mc' && (!Array.isArray(q.opts) || q.opts.length !== 4)) continue;
    seen.add(q.id);
    rows.push({
      id: q.id, exam: q.exam || 'RN', cat: q.cat, topic: q.topic ?? null,
      difficulty: q.difficulty || 'Moderate', level: LEVEL[q.difficulty] || 3,
      type, stem: q.stem, free: !!q.free,
      opts: q.opts ?? null, correct: q.correct ?? null,
      cols: q.cols ?? null, rows: q.rows ?? null,
      condition: q.condition ?? null, actions: q.actions ?? null, parameters: q.parameters ?? null,
      tip: q.tip ?? null, pearl: q.pearl ?? null,
    });
  }
  return rows;
}

function loadFlashcards() {
  const seen = new Set();
  const rows = [];
  for (const c of readBatch('flashcards', 'cards')) {
    if (!c.front || !c.id || seen.has(c.id)) continue;
    const kind = c.kind || 'qa';
    if (kind === 'qa' && !c.back) continue;
    seen.add(c.id);
    const { id, deck, topic, front, back, rationale, hint, difficulty, ...rest } = c;
    delete rest.kind;
    rows.push({
      id, kind, deck, topic: topic ?? null, difficulty: difficulty ?? 3,
      front, back: back ?? null, rationale: rationale ?? null, hint: hint ?? null,
      data: Object.keys(rest).length ? rest : null,
    });
  }
  return rows;
}

function loadDrugs() {
  const seen = new Set();
  const rows = [];
  for (const d of readBatch('drugs', 'drugs')) {
    if (!d.generic || !d.class || seen.has(d.id)) continue;
    seen.add(d.id);
    rows.push({
      id: d.id, generic: d.generic, brand: d.brand ?? null, drugClass: d.class,
      system: d.system, moa: d.moa, uses: d.uses || [], dose: d.dose, route: d.route,
      side: d.side || [], adverse: d.adverse || [], nursing: d.nursing || [],
      labs: d.labs || [], contra: d.contra || [], teaching: d.teaching || [],
      antidote: d.antidote || 'None', highalert: !!d.highalert, prototype: !!d.prototype,
      tip: d.tip ?? null, pearl: d.pearl ?? null,
    });
  }
  return rows;
}

async function main() {
  const questions = loadQuestions();
  const flashcards = loadFlashcards();
  const drugs = loadDrugs();
  console.log(`Parsed: ${questions.length} questions · ${flashcards.length} flashcards · ${drugs.length} drugs`);

  if (DRY) { console.log('--dry: no database writes.'); return; }

  const { PrismaClient } = await import('@prisma/client');
  const prisma = new PrismaClient();
  try {
    for (const q of questions) await prisma.question.upsert({ where: { id: q.id }, create: q, update: q });
    for (const c of flashcards) await prisma.flashcard.upsert({ where: { id: c.id }, create: c, update: c });
    for (const d of drugs) await prisma.drug.upsert({ where: { id: d.id }, create: d, update: d });
    console.log('Imported into the database ✓');
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
