---
name: mls-design-system
description: The Must Love Scrubs design bible (Master Prompt V2 — CURRENT). Read before building or changing ANY page, component, or feature. Covers brand, palette, layout system, Esi rules, points economy, and page map.
---

# Must Love Scrubs — Design Bible (Master Prompt V2, owner-locked 2026-07)

Must Love Scrubs is a **premium mobile-first nursing education ecosystem** —
Netflix × Duolingo × MasterClass, unique to MLS. The owner makes final
decisions. **NEVER build new features without owner confirmation** — outline
and confirm first. V2 supersedes V1 (the 8-pillar lifestyle platform) wherever
they conflict.

## Non-negotiables

1. **Mobile first**, fully responsive. $10,000 quality, seamless, never cluttered.
2. **TWO scrolling tickers above the header** — #1 advertises Esi, #2 advertises courses. Opposite scroll directions.
3. **Sticky bottom navigation on mobile** — 5 tabs: Home · Courses · **Scrub TV (raised center, coral)** · Store · Profile. Custom stroke SVG icons only, never emoji.
4. **Esi floating widget on every page.** NO free chat, no "Ask Esi." Tap → non-subscriber goes to the Esi subscribe page; subscriber goes to their Profile Dashboard (study/quiz/learn with Esi). Demo flag: `localStorage.esiSubscribed`.
5. **Esi's only jobs: tutoring + site navigation help.** Never diagnoses/prescribes; drafted-legal disclaimer wherever she appears. "Always Esi" is scrapped.
6. Parallax between sections, smooth micro-interactions, everything honors `prefers-reduced-motion`.
7. **Never use the word "pillar" in user-facing text.**

## Brand & visual system ("Ecosystem" palette — vibrant, alive, NOT nurse.com)

- Tokens in `css/styles.css`; always use tokens: midnight indigo base
  (`--indigo-950/900/700`), electric coral (`--coral-500/600`) for CTAs and
  the heartbeat, vivid teal (`--teal-400/600`), warm gold (`--gold-400`) for
  points/rewards/wins, bright near-white grounds.
- **Logo (designed in code):** wordmark "Must Love Scrubs" + compact mark **M❤️‍🩹S**. Products in the store carry MLS and M❤️‍🩹S logos.
- Type: heavy modern sans display (system stack, weight 800, tight tracking), regular sans body. Fluid `clamp()` sizes.
- Rounded cards, pill buttons, layered soft shadows, gold highlight swipe for key words.
- Hero photo direction: **instructor training nursing students at a hospital bed** (clinical-sim scene). Currently an SVG placeholder marked swap-ready; owner may supply photo.

## Homepage order (locked)

1. Ticker ×2 → 2. Header w/ nurse.com-style **mega menu** (panels with headline, description, subcategory links, CTA, promo tile) → 3. Hero (bedside training scene, Start Learning CTA, NCLEX flagship badge; NO Esi in hero) → 4. **Scrub TV** = 8 category squares w/ icons + featured videos rotated every 2 weeks (each video page = video + quiz + point-earning activities; videos double as TikTok/FB content) → 5. "Wherever you are on your nursing journey… **WELCOME HOME**" → 6. Featured courses (NCLEX flagship; library will grow to nurse.com scale) → 7. Why Choose MLS: ①other sites are generic cookie-cutter clones — MLS is innovative with proven retention systems ②Esi revolutionizes learning ③massive prep library → 8. Store preview (Shopify POD lifestyle: bags/mugs/tees/etc + points-redeemable digital downloads) → 9. Social proof (animated count-up: **1,400+ nurses trained** [real client stat] + 2 true stats; trust badges) → 10. Testimonials carousel (SAMPLE placeholders, owner replaces) → 11. FAQ collapsible accordion → 12. Join Our Community = create free account → 13. nurse.com-caliber mega footer (legal lives here) → sticky bottom nav + Esi widget.

## Scrub TV categories (locked, 8)

ER/Trauma · Prenatal & L&D · Pediatrics · ICU/Critical Care · Med-Surg · Pharmacology · Mental Health · Geriatrics

## Store (locked)

Shopify POD (owner connects Shopify later; storefront built now): mugs, tees,
totes, tumblers, hoodies, stickers, bags — MLS / M❤️‍🩹S branded, small curated
lifestyle store. Digital downloads (Etsy-style categories: study guides & cheat
sheets, report/brain sheets, badge cards, planners, drug cards, care plan
templates, resume kits, wall art) — redeemable with points.

## Points economy (locked)

- **Claim Daily Points on Profile Dashboard: 5 pts/day for logging in.**
- Earn: quizzes, puzzles, video activities, contests.
- Redeem: digital downloads in the store.
- Everything syncs to the Profile Dashboard (progress, quiz history, certificates, points, saved content, recommendations). Demo mode uses localStorage until real backend (Phase 2).

## Menu structure (locked)

Main: Home · Courses · Scrub TV · Esi · Store · Spotlight · Job Search · Blog
— separator — Secondary: About · Careers · Help Center · Contact · Support · Settings.
Notifications = header bell dropdown. Search = header icon. Privacy/Terms → footer only.
FAQ → homepage accordion. **No Post-a-Job page. No Forum.** Every menu item links to a real page.

## Pages

index, courses, scrubtv, esi (subscribe page w/ illustrated Esi preview),
store, spotlight (beautiful editorial stories), jobs ("small Indeed just for
nurses" — search UI + public nursing job resources), blog, about, careers,
help, contact, support, settings, profile (dashboard), join (create free
account), search, notifications, privacy (DRAFT), terms (DRAFT).

## Pricing (owner-locked structure; numbers editable — updated 2026-07)

**NCLEX Complete = one subscription, three durations. Esi is INCLUDED in every
plan (no add-on) because competitors bundle AI and we beat them on it.** Every
plan unlocks the ENTIRE system — question bank, 50 case studies, 4 readiness
exams, strategy course, study schedules, tagging, analytics, the workbook, and
Esi. The only difference between tiers is how much runway you get.

- **1 Month — $49** (anchor $79, "Save $30"). For students testing soon.
- **2 Months — $89** (anchor $149, "Save $60"). *Most recommended.* Pass Guarantee.
- **3 Months — $119** (anchor $199, "Save $80"). Pass Guarantee. Full-time workers.
- **Pass Guarantee** on the 2- and 3-month plans: finish the program, full refund if you don't pass.
- Helper `pricing_tiers()` in `build_pages.py` renders the three cards; `TIERS` + `TIER_FEATURES` hold the data. `nclex-complete.html` is the flagship product page.
- Specialty courses $49–$79 · Nurse Dictionary download $4.99 (or points, free with any course).
- Free account: free tier (NCLEX practice + 4 Scrub TV lessons + dictionary search), points, dashboard.

## NCLEX Complete flagship page (owner-locked — benchmarked to beat NCLEX Bootcamp)

`nclex-complete.html` is the paid product page. Original content only — never
copy Bootcamp/Kaplan/actual NCLEX; never call it "NCLEX Bootcamp." Sections:
four pillars (50 Next Gen case studies + walkthroughs · 2,600+ standalone
questions · Next Gen strategy course · 4 full-length CAT readiness exams that
predict pass chance Low/Borderline/High/Very High), a readiness meter, a CAT
explainer, 1/2/3-month day-by-day study schedules, an interactive "which plan"
quiz, Mastered/Reviewing/Learning tagging, performance-by-subject bars,
Question of the Day (phone or email), community (study group + weekly webinars),
the downloadable 50-question workbook, and the three-tier pricing block. JS in
`js/complete.js`. NCLEX® trademark disclaimer required at the bottom.

## Crawl / anti-scrape policy (owner-locked)

`robots.txt` allows Google/Bing/DuckDuckGo (SEO) and blocks known AI/content
scrapers (GPTBot, ClaudeBot, CCBot, PerplexityBot, Bytespider, etc.). robots.txt
is a request, not enforcement — REAL blocking (the 403 competitors return) is a
hosting/CDN switch: enable Cloudflare Bot Fight Mode / a WAF rule at deploy.

## Dictionary = own-once, free-forever (owner-locked)

Ownership is a **profile flag**, not a file sale. The download always serves the
**latest release**; owners get every future expansion **free, automatically**,
surfaced in **Profile → My Downloads** with a sleek gradient **"UPDATED · FREE"
badge** (`.badge-new` — coral→gold, never a blue button) + version note. Demo via
localStorage (`dictOwned`, `dictSeen`); real version reads the account/DB in Phase 2.

## Contact (samples until owner replaces)

hello@mustlovescrubs.com · facebook.com/mustlovescrubs · tiktok.com/@mustlovescrubs

## Specialties we sell prep for (owner-locked)

RN vs BSN is not a license split (BSN is one path to RN), so we sell **clinical
specialty prep** — the any-RN list: Medical-Surgical, Emergency/ER, Critical
Care/ICU, Pediatrics, Labor & Delivery/OB, Neonatal/NICU, Oncology,
Cardiac/Telemetry, OR/Perioperative, PACU, Psychiatric/Mental Health,
Geriatrics, Home Health, Hospice/Palliative, Rehabilitation, Dialysis/Nephrology,
Wound Care, Ambulatory/Clinic, School Nursing, Occupational Health, Long-Term
Care, Progressive Care. BSN-favored roles (public health, case management,
management, informatics, research, flight) and graduate/advanced-practice tracks
(NP, CNS, CRNA, CNM, educator, executive) are a LATER phase, not launch.

## Nurse Dictionary (owner-locked tool)

A searchable index of medical/nursing terms and definitions — free tool at
`dictionary.html`. Search box + A–Z filter + category chips. Great for SEO and
daily-return habit. Grows over time.

## Nurse Dictionary = a product (owner-locked)

Data lives in `data/nurse-dictionary.json` (+ .csv); `dictionary.html` is generated
from it (217+ curated terms, 32 categories mapped to 7 filter groups). No duplicates.
- **Free** to search online.
- **Paid download $4.99** — every term with a **real clinical example + rationale**
  ("same lane as a question bank, different way to learn"). **Unlockable with points**,
  and **free with any course purchase**. Advertised on the homepage + dictionary page.

## Points — what unlocks with points (owner-locked + roadmap)

Earn: 10/day daily claim + quiz/streak/contest bonuses. Redeemable for:
Nurse Dictionary download · store digital downloads (brain sheets, planners, drug
cards) · course discount dollars · (roadmap: mock-exam retakes, streak freezes,
Esi day-passes, exclusive Scrub TV drops, merch discount codes, spotlight submission boosts).

## Master Question Bank architecture (owner-locked plan — Phase 3 content build)

Separate production asset from the Dictionary; they connect via shared topic +
specialty tags. Formats: Excel (edit) + CSV (bulk import) + website JSON (`data/`).
- **NCLEX-RN ~3,000** (Adult Health, Fundamentals, Pharmacology, Mental Health,
  Maternal/Newborn, Pediatrics, Leadership/Mgmt, Safety & Infection, Clinical Judgment)
- **NCLEX-PN/LPN ~1,500** (practical scope, care coordination, med admin, procedures, prioritization)
- **22 specialty banks ~100–250 each (~3,000 total)** — the sellable specialty prep.
- Every record: id, exam, level, specialty, category, topic, clinical-judgment step,
  difficulty, type, stem, options, correct, why-correct, why-others-wrong, NCLEX rationale,
  key concept, memory tip.
- Types: MC, SATA, matrix/grid, bow-tie, trend, drag-drop, ordered response, case study, prioritization, delegation.
- **Approach: benchmark-first** — build the taxonomy + DB template, then a 250 RN +
  100 specialty benchmark batch to lock quality, THEN scale. Don't ship a huge bank that
  fails when nurses use it. QC gate: verified answer, NCLEX wording, no ambiguity,
  rationale written, difficulty tagged, dedup checked, specialty placement checked.

## Build phases

**Phase 1 (current):** design system, homepage, all pages linked, menus, tickers, widget, footer, legal drafts.
**Phase 2:** real accounts/backend, points engine, quiz engine.
**Phase 3:** NCLEX flagship course content built into the engine (curriculum from owner's research: teach how to think, not memorize).
