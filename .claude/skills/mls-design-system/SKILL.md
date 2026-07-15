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

**NCLEX Complete = one subscription, FOUR durations (1/2/3/6 months). Esi is
INCLUDED in every plan (no add-on).** Every plan unlocks the ENTIRE system —
question bank, 50 case studies, 4 readiness exams, strategy course, study
schedules, tagging, analytics, the workbook, and Esi. Only the runway differs.
Prices are **benchmarked to the real market** (Bootcamp ~$59–130, UWorld ~$250/90d,
Kaplan $299–525, Archer $69–399, Hurst $159–339) and **shown discounted** (slashed
anchor + "Save $X"). Esi's AI cost is ~$25/mo, so every tier clears cost + margin.

- **1 Month — $59** (anchor $99, Save $40). $59/mo. Testing soon.
- **2 Months — $99** (anchor $169, Save $70). $50/mo. *Most popular* (coral). Pass Guarantee.
- **3 Months — $129** (anchor $219, Save $90). $43/mo. Pass Guarantee.
- **6 Months — $199** (anchor $349, Save $150). $33/mo. *Best value* (teal). Pass Guarantee.
- **Pass Guarantee** on 2/3/6-month plans: finish the program, full refund if you don't pass.
- Helper `pricing_tiers()` renders 4 cards; `TIERS` holds the data (`rec`, `feat`, `permo`). `nclex-complete.html` is the flagship page.
- Specialty courses $49–$79 · Scrubs Dictionary download $4.99 (or points, free with any course).
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

## Specialty prep pages (UI shell — built 2026-07, awaiting content)

`specialties.html` = the hub (grid of all 22 tracks, each a `.spec-card` with
"In development" lock badge + price). Each specialty has a detail page
`specialty-<slug>.html` generated by `build_specialty()` from the `SPECIALTIES`
list in `build_pages.py`: themed hero + topic chips, "What you'll master" module
tiles, 3-step method, a **locked/blurred** sample-question preview, and a
"Notify me" waitlist band (`js/specialty.js`, demo). **UI only — no real
question data yet.** Prices $49–$79. Wired into the mega menu (Learn) and footer.
Owner will review the UI and request changes before content is written.

## Competitor benchmark — pieces to match, our own way (owner-locked 2026-07)

Benchmarked against NCLEX Bootcamp. We recreate every piece with **100%
original content and MLS branding** — never copy their text, never use the name
"NCLEX Bootcamp." Map of their piece → our equivalent:

| Their piece | Our equivalent (page) |
|---|---|
| NCLEX Question of the Day (email) | Question of the Day, phone **or** email (`nclex-complete.html`, `nclex-guide.html`, profile) |
| 50 Next Gen case studies + video walkthroughs | 50 case studies pillar (`nclex-complete.html`) |
| 2,600+ standalone questions | Interactive **Question Bank** `qbank.html` — original Qs, rationale per option, answer stats, tagging, timer/score (`QBANK` data + `js/qbank.js`); free sample → full bank in NCLEX Complete |
| Next Gen Strategy Course (lesson player: timer, answer stats, autoplay, video walkthroughs) | Strategy video course (NCLEX Complete) — lesson-player UI is a Phase-2 build to spec |
| 4 full-length readiness exams + pass prediction | Readiness meter Low/Borderline/High/Very High (NCLEX Complete) |
| Study Schedule Creator (1/2/3-mo calendar) | Study schedules + plan quiz (NCLEX Complete) |
| Pass Targets Tracker | Mastered/Reviewing/Learning tagging + performance-by-subject bars |
| 140+ printable cheat sheets | Store digital downloads + Scrubs Dictionary + the 50-Q workbook |
| Ask Bootcamp AI | **Esi** (our differentiator — included in every plan) |
| Free NCLEX Study Guide (lead-magnet doc) | `nclex-guide.html` — "for nurses, by nurses" (below) |
| NCLEX 101 info (register / exam day / fees / test plan) | Sections in `nclex-guide.html` (placeholder external links to add) |
| Facebook study group + weekly webinars | Community band (NCLEX Complete) |

**Brand voice: "for nurses, by nurses."** MLS was created by a group of nurses.
Homepage intro and the study guide lead with this. Founder letter voice = warm,
been-there ("First — breathe"), never corporate.

## Free NCLEX Study Guide (`nclex-guide.html`, owner-locked)

A free lead-magnet content hub (our answer to Bootcamp's study guide). Sections:
"for nurses, by nurses" hero → founder intro letter (photo `nurses-group.jpg`) →
Question-of-the-Day subscribe → "What is NGN?" bulleted explainer with links →
NCLEX-101 quick cards → logistics blocks (**register, exam day, fees, test plan,
when to test, how long to study** — each links to our pages + a placeholder
`data-ext` external link the owner fills in) → strategy + readiness/analyzer
section. Placeholder link "the MLS Bootcamp" → `nclex-complete.html` (can also
point to an external bootcamp URL). NCSBN trademark disclaimer required.

## Photos (`/images`, owner supplies files)

Real photos are embedded into pages + the bundle at build time by
`tools/bundle_site.py` (base64 data URIs, CSP-safe). Slots reference
`images/<name>`; until a file exists, a gradient fallback shows. Current slots:
`nurses-group.jpg` (home intro + guide intro), `dictionary.jpg` (dictionary art,
replaced the old "A–Z" block). See `images/README.md`.

## Homepage + nav changes (owner-locked 2026-07)

- **Bottom nav (mobile): Home · Courses · Scrub TV · Dictionary · Profile.** Store removed from bottom nav.
- **No Store section on the homepage** (store still exists at `store.html`).
- "Why MLS" is **4 cards** (added "Free that beats their paid").
- Social proof: **1,400+ reads bigger (gold lead stat)**; dictionary-terms stat replaced with **free-lessons count**; all numbers count up on scroll; trust badges in a 4-up grid.
- Homepage FAQ is **NCLEX-focused** (`FAQS`); **Esi page has its own FAQ** (`ESI_FAQS`). `faq_list(faqs)` takes a data arg.
- **Esi widget is smaller / less obstructive** (`.esi-fab`).
- Scrub TV free lessons render on **one line** (`.course-shelf.one-line`); button reads "Free lessons".
- Dictionary shows a **free-vs-paid "with bonus" comparison** (`.compare-grid`) so buyers see the paid value.

## Scrubs Dictionary (owner-locked tool)

A searchable index of medical/nursing terms and definitions — free tool at
`dictionary.html`. Search box + A–Z filter + category chips. Great for SEO and
daily-return habit. Grows over time.

## Scrubs Dictionary = a product (owner-locked)

Data lives in `data/nurse-dictionary.json` (+ .csv); `dictionary.html` is generated
from it (217+ curated terms, 32 categories mapped to 7 filter groups). No duplicates.
- **Free** to search online.
- **Paid download $4.99** — every term with a **real clinical example + rationale**
  ("same lane as a question bank, different way to learn"). **Unlockable with points**,
  and **free with any course purchase**. Advertised on the homepage + dictionary page.

## Points — what unlocks with points (owner-locked + roadmap)

Earn: 10/day daily claim + quiz/streak/contest bonuses. Redeemable for:
Scrubs Dictionary download · store digital downloads (brain sheets, planners, drug
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
### Pipeline IMPLEMENTED (2026-07)

The batch pipeline is live. Questions live in **`data/qbank/*.json`** batch files
(schema in `data/qbank/schema.md`). `tools/build_qbank.py` validates + summarizes;
`build_pages.py` `_load_qbank()` globs, validates, de-dupes, synthesizes answer
stats, and assembles the bank feeding `qbank.html`. Add a batch → rebuild → it
appears. `free: true` flags the free sample (gated otherwise) — data-driven, no
code change. `tools/import_workbook.py` migrated the 50-question workbook →
**48 MC questions across 8 categories** (the SATA + bow-tie items await non-MC
support). Authoring model (owner-picked): **I generate original questions in
JSON batches**, owner reviews each batch. Next: benchmark batch toward 250 RN.
qbank data JSON is embedded in a `<script type="application/json" data-qbank>`
block (not an attribute) and `**bold**` renders in `js/qbank.js`.

- **Approach: benchmark-first** — build the taxonomy + DB template, then a 250 RN +
  100 specialty benchmark batch to lock quality, THEN scale. Don't ship a huge bank that
  fails when nurses use it. QC gate: verified answer, NCLEX wording, no ambiguity,
  rationale written, difficulty tagged, dedup checked, specialty placement checked.

## Build phases

**Phase 1 (current):** design system, homepage, all pages linked, menus, tickers, widget, footer, legal drafts.
**Phase 2:** real accounts/backend, points engine, quiz engine.
**Phase 3:** NCLEX flagship course content built into the engine (curriculum from owner's research: teach how to think, not memorize).
