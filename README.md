# Must Love Scrubs 🩺💜

**The Everything Platform for Nurses** — mobile-first NCLEX prep + nurse community.

## Two parts of this repo

- **The working prototype** (repo root) — a static, self-contained web app.
  Interactive tests, adaptive NCLEX mock, study calendar, flashcard games,
  drug cards, question bank, Nurses Index. Runs with no backend.
- **The production app** (`web/`) — a Next.js + Supabase skeleton to add real
  user accounts and saved progress. See `SETUP.md`.

## Run the prototype
```bash
python3 tools/build_pages.py    # regenerate pages after any change
python3 tools/bundle_site.py    # regenerate the single-file preview
python3 -m http.server 8000     # then open http://localhost:8000
```

## Start here
- **`HANDOFF.md`** — full project map: what exists, how it's built, conventions,
  and how to continue in ChatGPT / Codex / another tool.
- **`SETUP.md`** — turn the prototype into the full app (accounts, database).
- **`docs/`** — the product blueprint (spec, data model & API, build plan).
- **`.claude/skills/mls-design-system/SKILL.md`** — the design bible. Read
  before changing any styling.

## Add content (no code)
Drop a JSON file into `data/qbank/`, `data/flashcards/`, or `data/drugs/`
following the existing shape, then rebuild. It appears automatically.
