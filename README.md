# Must Love Scrubs

**The everything platform for nurses** — an interconnected Nursing Knowledge Index (NKI) that powers adaptive learning, an AI tutor (Esi), and a text-based professional community.

This repository is the **master specification and content source** for the platform. We build like a software company: schema, contracts, templates, and standards first — then content at scale.

## Repository map

| Path | What it holds |
|------|---------------|
| `docs/00-master-vision.md` | Product mission, positioning, long-term roadmap |
| `docs/01-phase0-architecture.md` | Platform architecture & Nursing Knowledge Engine |
| `docs/02-phase1-content-architecture.md` | Taxonomy, metadata, relationship engine, search |
| `docs/03-phase2-knowledge-index.md` | NKI database design, node types, adaptive learning |
| `docs/04-scope-v1-webapp.md` | **Locked v1 scope** (current build decisions) |
| `docs/05-roadmap.md` | Build order: what's first, what's deferred |
| `docs/06-build-instructions.md` | Engineering, data, UI, API, content-quality standards |
| `docs/questions/` | Question bank (QBK / NGN) — one JSON per file; see its README |
| `content/taxonomy/` | Master taxonomy & code tables |
| `content/templates/` | Locked content templates for every content type |
| `content/modules/` | Gold-standard NKI modules (Heart Failure = #001) |

## Current status
- ✅ Product vision & architecture (Phases 0–2)
- ✅ Content taxonomy, templates, relationship rules
- ✅ Gold Standard Module #001 — Heart Failure
- ✅ Question bank — existing NGN-0001 (DKA/HHS) + Cardiovascular batch 01 (10 HF items)
- ⏳ v1 web app (not yet built — scope locked in `docs/04`)

## v1 scope in one line
A **web app** with two surfaces sharing one login: a **learning core** (NKI dashboard + adaptive study, seeded with Heart Failure) and a **text-only, Twitter-style community** (feeds + threads; no video posting; no per-profile feed). Native/publishable app comes later.
