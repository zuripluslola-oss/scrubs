---
name: mls-design-system
description: The Must Love Scrubs design bible. Read before building or changing ANY page, component, or feature on this site. Covers brand, visual system, the 8 pillars, Esi rules, and monetization.
---

# Must Love Scrubs — Design Bible (Master Prompt V1)

Must Love Scrubs is a nurse lifestyle community platform. The owner makes final
decisions; we are the professionals. Build pillar by pillar unless told otherwise.

## Non-negotiables (every page, every time)

1. **Mobile first.** Design at 390px wide first, then scale up. Test every layout at phone width.
2. **$10,000 quality.** Modern, clean, generous whitespace. Never cluttered.
3. **Parallax scrolling** on hero/feature sections (transform-based, GPU-friendly, respects `prefers-reduced-motion`).
4. **Esi ticker** — a scrolling text strip advertising Esi sits ABOVE the header on every page.
5. **Ask Esi floating widget** — bottom right, always visible on every page. One tap wakes her. Screen splits when active so the user can browse while talking to Esi.
6. **Legal disclaimer always present** wherever Esi appears: Esi never diagnoses or prescribes; emergencies → call 911 first.

## Brand & visual system

- **Name:** Must Love Scrubs. Logo is wordmark: "Must Love **Scrubs**" with a heart/pulse accent.
- **Palette** (defined as CSS custom properties in `css/styles.css` — always use the tokens, never hardcode):
  - `--teal-900 #0B3B39`, `--teal-700 #10605B`, `--teal-500 #17877F` — scrub teal, the core brand color
  - `--coral-500 #F26B5E`, `--coral-300 #FFA598` — warm coral accent (CTAs, highlights, Esi)
  - `--cream #FAF6F0` page background, `--ink #16211F` text, `--sand #F0E8DC` alt-section background
- **Type:** Display serif stack (`Georgia, 'Times New Roman', serif` with `font-variation`/weight styling) for headlines; system sans (`-apple-system, 'Segoe UI', Inter, sans-serif`) for UI/body. Fluid sizes via `clamp()`.
- **Shape language:** large soft radii (20–28px cards), pill buttons, thin 1px borders at low opacity, soft layered shadows. No harsh lines.
- **Motion:** slow, soothing. Parallax layers, fade-up on scroll, marquee ticker. Everything honors `prefers-reduced-motion`.
- **North star (owner-approved Dribbble references):** modern SaaS polish — floating phone mockups showing the product in the hero, Esi represented as a glowing teal→coral gradient orb (like premium AI-assistant shots), glassmorphism cards, bold dark stat/CTA bands with big numbers, mint-teal healthcare palette. Build UI mockups in pure CSS/HTML — no stock screenshots.
- **North star (owner-approved nurse.com reference):** bright, clean, friendly. Dark-teal + **mint-green** pairing (mint is `--mint-400/300/100`), the signature **mint highlighter swipe behind a key word** (`.hl` class — like nurse.com's "Join Nurse.com!"), rounded cards, uppercase letter-spaced eyebrows, photography/real-nurse warmth. Blend this brightness with the Dribbble polish above.

## Wording rules (IMPORTANT)

- **Never call the 8 sections "pillars" in any user-facing text, nav, heading, URL fragment, or label.** "Pillar" is an internal build term only. To nurses they are simply the parts of the community (Ask Esi, Education, Forum, ScrubTV, Jobs, Store, Nurse Spotlight, Contests). CSS class names like `.pillar-card` may stay (invisible), but visible copy and anchors must not say "pillar."

## Esi — the AI nurse (Pillar 1, present everywhere)

Warm, soothing, practical, excellent communicator. Expert in nursing, medicine,
insurance, administration, elder care. Politely declines non-medical questions.
Powered by Claude. Tiers: **Ask Esi** (free, limited) → **Esi+** (unlimited
subscription) → **Always Esi** (elder-care add-on). Planned connectors: Apple
HealthKit, Google Fit, Google/Apple Calendar, Alexa, Google Home, Twilio SMS,
Email. Esi can navigate the site, build meal plans, medication schedules,
insurance explanations, health reports.

## The 8 pillars

1. **Ask Esi** — AI nurse widget + subscription tiers (above).
2. **Education** — organized by nurse type first (CNA, LPN, LVN, RN, BSN, MSN, NP, CRNA, Student, Travel), then specialty. Courses = study material, flashcards, quizzes, mock exams in real test format, analytics, progress tracking. Free tier samples; paid tier full banks + adaptive testing. Esi is the personal tutor.
3. **Forum** — Reddit/Twitter hybrid. 12 specialty categories (Critical Care/ICU, Emergency/ER, Pediatrics/NICU, Labor & Delivery, Oncology, Travel Nursing, Mental Health/Psych, Geriatrics/Elder Care, Surgery/OR, Primary Care/Family, Cardiology, New Grad/Students). Upvotes, likes, best/newest sort, verified-nurse badges, anonymous posting (profile required, name hidden).
4. **ScrubTV** — TikTok meets YouTube. Shorts are the hero feature: full-screen vertical scroll, autoplay, For You algorithm. Likes, follows, comments, saves, shares, duets, stitches, live, trending sounds. Creator dashboard + ad-rev sharing (AdSense, Stripe payouts, minimum threshold). Cloudflare Stream hosting; free accounts 500MB.
5. **Jobs** — Indeed-style, travel-nurse focused. Scraped listings (Indeed, ZipRecruiter, Travel Nurse Source, LinkedIn, Vivian) + paid employer posts. Searchable nurse profiles, Esi job alerts, filters (specialty, location, salary, shift, experience, travel/perm, contract length), saved jobs, application tracking, sponsored listings.
6. **Store** — Walmart for nurses. Spocket dropship, Printful merch, Amazon Associates + ShareASale affiliate. 12 categories with subcategories. Search always visible; filters (price, brand, rating, new, sale). Esi is the personal shopper. Curated quality only.
7. **Nurse Spotlight** — editorial storytelling, owner-submitted. Hero image/video, full story, name, location, specialty, quote. Strategically diverse. Magazine quality, cinematic, scroll-driven — NYT feature meets Instagram. Contest winners auto-featured.
8. **Contests** — community voting. Types: photo, video, story, meme, best scrub fit, nursing hack. Nurse of the Month; Annual Nurse Awards (Most Inspiring, Rising Star, Travel Nurse of the Year, Unsung Hero, Educator of the Year). Countdown timers, leaderboards, past winners, sponsor branding. Winners get verified badge + Spotlight feature.

## Monetization

Store revenue · ads · employer job-posting fees · course fees · ScrubTV ad-rev
share · Esi+ subscription · Always Esi add-on.

## Current tech setup

Static-first site: `index.html` + `css/styles.css` + `js/main.js`. Shared
pieces (ticker, header, Esi widget) live on every page — keep their markup and
behavior identical across pages. When the platform needs auth/db/video we will
migrate to a full-stack framework; until then, do not add build tooling without
asking the owner.
