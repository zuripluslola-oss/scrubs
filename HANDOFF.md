# Must Love Scrubs — Project Handoff

**The Everything Platform for Nurses.** A mobile-first NCLEX prep + nurse
community web app. This file orients any AI or developer (ChatGPT, OpenAI
Codex, Claude, or a human) so they can continue the build. Read it first.

Repo: `zuripluslola-oss/scrubs` · Active branch: `claude/must-love-scrubs-build-yorz07`

---

## What this project is (current state)

A **static, self-contained web app** — no backend yet. All pages are plain
HTML/CSS/JS, generated from Python source, and can also be bundled into one
shareable file. Everything works today: interactive tests, a study calendar,
flashcard games, drug cards, a question bank, and a nursing terms index.
Progress is saved in the browser (`localStorage`).

### Features that already work
- **Tests & Exams** (`tests.html`) — Pop Quiz (8), Basic Test (20), adaptive
  **NCLEX Mock (85–150, real CAT stop rule)**, Specialty Mock (100). Score,
  weak-area breakdown, and a rationale on every question.
- **Study Plan Calendar** (`study-plan.html`) — pick a length (1/2/3/6 mo) and
  start date; generates a day-by-day plan (reading, flashcards, spaced review,
  pop quiz, case study, mnemonic game, weekly test, readiness exam) built on
  spaced repetition, active recall, and interleaving.
- **Flashcards & Games** (`flashcards.html`) — 6 card types + Challenge, Quiz,
  Match, and Speed modes, adaptive difficulty.
- **Drug Cards** (`drugs.html`) — searchable pharmacology library + Drill mode.
- **Question Bank** (`qbank.html`) — 106 original questions, rationale per option.
- **Nurses Index** (`dictionary.html`) — searchable nursing terms.
- Homepage, NCLEX Complete flagship, 22 specialty pages, Scrub TV, Esi widget,
  4-tier pricing, community/blog/jobs/spotlight shells.

---

## How it's built (the architecture)

The site is **data-driven and generated** — you rarely edit HTML by hand.

```
tools/build_pages.py   → generates every *.html page (shared header, nav,
                         footer, Esi widget). THIS is where pages/content live.
tools/bundle_site.py   → inlines CSS + JS + images into one file:
                         mls-site-bundle.html (used for the shareable preview).
css/styles.css         → all styles (design tokens: violet & mint palette).
js/*.js                → interactivity, one file per feature:
                           tests.js, studyplan.js, flashcards.js, drugs.js,
                           qbank.js, dictionary.js, complete.js, main.js …
data/                  → the CONTENT, as JSON batch files:
   data/qbank/*.json         (exam questions)
   data/flashcards/*.json    (flashcards)
   data/drugs/*.json         (drug cards)
   data/nurse-dictionary.json(terms)
docs/*.md              → the full product blueprint (spec, data/API, build plan).
.claude/skills/mls-design-system/SKILL.md → the design bible. Read before styling.
```

### To rebuild after any change
```bash
python3 tools/build_pages.py   # regenerate the .html pages
python3 tools/bundle_site.py   # regenerate the single-file bundle
```

### To add content (no code needed)
Drop a new JSON file into `data/qbank/`, `data/flashcards/`, or `data/drugs/`
following the shape of the existing files, then rebuild. It appears automatically.
The question schema is documented in `data/qbank/schema.md`.

### To run locally
```bash
python3 -m http.server 8000    # then open http://localhost:8000
```

---

## Conventions
- **Violet & mint** palette via CSS tokens (`--coral-500` is the violet primary,
  `--teal-*` mint). Serif display font. Mobile-first.
- Content JSON is embedded in pages as `<script type="application/json">` blocks.
- Every exam question carries a **rationale for every option** and a
  **difficulty** (Easy/Moderate/Hard → numeric level 1–5 for the adaptive engine).
- All practice/exam content must be **100% original** — never copied from the
  real NCLEX, NCSBN, or any commercial provider.

---

## The roadmap (what's next — the production platform)

The current app is the **prototype**. The full vision (see `docs/`) adds a real
backend so nurses have accounts and saved progress across devices:

1. **Accounts & saved progress** — auth + a database (Postgres/Supabase) so
   `localStorage` becomes real user data.
2. **Next.js app** — migrate the generated pages into a React/Next.js frontend
   that talks to an API.
3. **Server-side CAT engine** — the adaptive logic (already prototyped in
   `js/tests.js`) moved server-side with proper IRT.
4. **Instructor & admin portals** — authoring, review workflow, class analytics.
5. **AI tutor (Esi) backend** — real explanations, question generation, study plans.

The data pipelines, scoring logic, CAT stop rule, and all content built here
carry directly into that backend. **Recommended order: get nurses testing the
prototype → gather feedback → then build the backend in stages.**

---

## Using this in ChatGPT / Codex / another tool

- **Everything is in this repo.** Point the tool at `zuripluslola-oss/scrubs`.
- **OpenAI Codex** (the coding agent) connects to a GitHub repo directly — the
  closest match to how this was built. Connect the repo, pick this branch, and
  give it a task (e.g. "add 20 more pharmacology questions in a new
  `data/qbank/*.json` batch and rebuild").
- **Plain ChatGPT** — download the repo as a ZIP from GitHub (green **Code**
  button → Download ZIP) and upload the key files, or create a ChatGPT
  **Project** and add the `docs/*.md` and this HANDOFF as project knowledge.
- **Always tell the new tool:** "Content lives in `data/*/*.json`; pages are
  generated by `tools/build_pages.py`; rebuild with the two commands above;
  read `HANDOFF.md` and `.claude/skills/mls-design-system/SKILL.md` first."
