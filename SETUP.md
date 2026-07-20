# Must Love Scrubs — Backend Setup (for Codex / any developer)

This is the **running start** for turning the working prototype into the full
app with **user accounts and saved progress**. Follow it in order. You do NOT
need any of this to run the current static prototype — it already works. This
is only for the production (backend) version.

> New here? Read `HANDOFF.md` first for the project map.

---

## Step 1 — Create the accounts (10 minutes, all free to start)

| Service | Sign up at | You'll copy |
|---|---|---|
| **Supabase** (database + login + storage) | supabase.com | Project URL, `anon` key, `service_role` key, and the database connection string |
| **Vercel** (hosting) | vercel.com | Nothing yet — you connect the GitHub repo when you deploy |
| **OpenAI** (Esi AI tutor) | platform.openai.com | An API key (`sk-...`) |
| **Stripe** (only when you start charging) | stripe.com | Secret + publishable keys — skip for now |

---

## Step 2 — Fill in the keys

Copy `web/.env.example` to `web/.env` and paste your values. That file lists
every variable and exactly where each one comes from. **Never commit `.env`** —
it's already git-ignored.

In Codex, add these same values as **environment secrets** so the agent can run
the app.

---

## Step 3 — Set up the database

From the `web/` folder:
```bash
npm install
npx prisma migrate deploy      # creates all the tables in Supabase
node scripts/import-content.mjs   # loads your existing questions, flashcards,
                                  # and drug cards from ../data into the database
```
`npx prisma migrate deploy` uses `web/prisma/schema.prisma` (the full data model).
The same schema is mirrored in `web/supabase/migrations/0001_init.sql` if you
prefer to run it directly in the Supabase SQL editor.

Verify it loaded (no DB needed for the count check):
```bash
node scripts/import-content.mjs --dry
```

---

## Step 4 — Run it
```bash
npm run dev        # http://localhost:3000
```
Visit `http://localhost:3000/api/questions` — you should see your questions
served from the database. That proves the whole chain (Next.js → Prisma →
Supabase) is connected.

---

## Step 5 — Hand it to Codex to finish

In Codex, connect the repo and this environment, then give it the build order
from `HANDOFF.md` → "The roadmap." A good first task:

> "Read HANDOFF.md and SETUP.md. The database, content import, and a sample API
> route already exist. Build (1) email/password auth with Supabase, (2) a
> student dashboard that shows saved progress, and (3) move the adaptive exam
> logic from the prototype's `js/tests.js` into a server-side API. Keep the
> existing violet & mint design."

Each feature in the roadmap builds on this skeleton. The content, scoring
logic, and CAT stop rule from the prototype all carry straight in.

---

## What's already scaffolded for you

```
web/
  package.json                 Next.js 14 + Prisma + Supabase deps
  .env.example                 every key, with where to get it
  prisma/schema.prisma         full data model (users, questions, attempts,
                               exam sessions, mastery, flashcards, drugs, plans)
  supabase/migrations/         the same schema as raw SQL
  scripts/import-content.mjs   loads ../data/*.json into the database (--dry to test)
  app/                         Next.js app router (landing + /api/questions)
  lib/                         db (Prisma) + Supabase client helpers
scripts/codex-setup.sh         paste into Codex's "setup script" field
```
