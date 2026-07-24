# v1 Scope — Web App (LOCKED)

This document records the current build decisions. When the long-term vision (Phases 0–2) and this document disagree about what to build *now*, **this document wins for v1.**

## Platform decision
- Build a **web app first.** Not a native/publishable mobile app (that comes later), and we are not shipping a marketing "website" as the product.
- We confirm and outline how the project works **before** building.

## The v1 web app: two surfaces, one login

### Surface A — Learning Core (the dashboard)
The product's spine and differentiator. **Keep this.**
- **Dashboard**: readiness by body system, weak/strong topics, streak, questions completed — the personal knowledge map, not just a single %.
- **Study Engine**: serves questions from the Master Question Schema; every answer updates the student's knowledge map (right *and* wrong).
- **NKI pages**: Disease / Medication / Lab / Procedure pages from locked templates, cross-linked via the Relationship Engine (Clinical Connections sidebar).
- **Esi (AI tutor)**: answers from structured NKI content first, then plain-language explanation adapted to the student.
- **v1 content seed**: the **Heart Failure gold-standard module** only — proves the pipeline end to end before scaling.

### Surface B — Community (Twitter-style, TEXT ONLY)
- **Global feed + threads** (reply chains), Twitter-style. **Nurses and visitors** both participate.
- **Posts are text.** **No video posting by users.**
- **No per-profile feed.** A profile shows identity + learning badges/stats only — there is no personal wall/feed. Discovery happens through the global/topic feed, not profile walls.
- Optional later: tag a post to an NKI topic (e.g. `#HeartFailure`) to connect community and learning. **Phase 2 nicety, not v1.**

## Explicitly OUT of v1
- Video posting / ScrubTV as user content
- Simulation Center, virtual hospital, career center
- Native/offline mobile app
- Full 40k-term dictionary and thousands of questions (architecture supports them; we don't build them yet)

## Open items to confirm before building code
1. **Tech stack** — propose a sensible default (e.g. React + backend + Postgres/Supabase) vs. a stated preference.
2. **Visitor posting** — can visitors post as guests, or is an account required to post (read is always free)?
3. **Esi in v1** — real AI tutor wired now, or a placeholder shell until the content library grows?
4. **First deliverable** — the written master spec (this docs set) vs. a clickable web-app skeleton of the two surfaces.

## One-line summary
A web app with a learning core (NKI dashboard + adaptive study, seeded with Heart Failure) and a text-only, Twitter-style community (feeds + threads; no video posting; no per-profile feed). Native app later.
