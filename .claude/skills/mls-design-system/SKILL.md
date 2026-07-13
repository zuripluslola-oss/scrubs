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

## Pricing (market-anchored placeholders, owner edits later)

NCLEX Complete $129 (or $39/mo) · specialty courses $49–$79 · **Esi tutor add-on +$19/mo** (requires a course). Free account: free content tier, points, dashboard.

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

## Build phases

**Phase 1 (current):** design system, homepage, all pages linked, menus, tickers, widget, footer, legal drafts.
**Phase 2:** real accounts/backend, points engine, quiz engine.
**Phase 3:** NCLEX flagship course content built into the engine (curriculum from owner's research: teach how to think, not memorize).
