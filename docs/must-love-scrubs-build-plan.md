# Must Love Scrubs — Build Plan & Roadmap (v1)
*Third blueprint doc. The Master Spec says **what**, the Database & API doc says **how**; this says **in what order**, **who does it** (AI vs engineer vs nurse SME), and **where the owner decides**. Foundation-first, so nothing gets rebuilt.*

**Status:** plan for approval. We build the **web app** first, native app later. Confirm each step before proceeding.

---

## 1. Guiding principles
- **Foundation before content.** Stand up the database + API + auth before pouring in thousands of questions, so content lands in a real structure.
- **One gold module, then replicate.** Prove a full topic end-to-end (Heart Failure done) before scaling.
- **AI drafts, humans approve.** AI generates content/questions in batches; a nurse SME reviews before publish. Never auto-publish clinical content.
- **Everything plugs into the NKE.** No one-off pages; every item validates against its template + tags + edges.
- **Ship thin slices.** Each phase produces something usable, not a big-bang launch.

---

## 2. Recommended stack (concrete, so it can be scoped/hired)
- **Web app:** Next.js (React) + the locked Violet & Mint design system → fast, SEO-friendly, mobile-first, one codebase for web now.
- **Database:** PostgreSQL. **Supabase** is a strong fit (Postgres + auth + storage + APIs out of the box) and is already connected to this workspace — we can stand up the schema there when approved.
- **Auth:** Supabase Auth (or equivalent) — JWT, roles from the API contract.
- **Media (community):** object storage + CDN, with virus scan + video transcode (per the community media pipeline).
- **AI (Esi):** Claude API, answering from NKE content first (retrieval over our own data), then plain language.
- **Native app (later):** React Native / Expo, consuming the *same* API.

*The owner doesn't need to know these tools — this is what an engineer would use; it's here so scoping and hiring are concrete.*

---

## 3. Phases (each ends in something real)

### Phase A — Foundation *(engineer-led)*
Database (nodes, edges, questions-in-nodes, users, entitlements, attempts, mastery, streaks, question_stats, threads/posts/media, reports) · auth + roles · core read/write API (`/node`, `/search`, `/questions`, `/attempt`, `/me/*`) · content-ingest pipeline (formalizes today's `data/qbank` batch flow) · validators for every content + question template.
**Done when:** a question can be authored → validated → stored → served → answered → recorded, through the real API.

### Phase B — Content engine *(engineer + AI + nurse SME)*
NKE pages (Disease/Med/Lab/Procedure/Skill) rendering from templates with the Clinical Connections sidebar + "Why?" chain · Question Engine implementing item types **incrementally** in the priority order below · unified search.
**Item-type build order** (built → next): ✅ MC, SATA, Matrix(MC), Bow-Tie → **Extended Multiple Response, Matrix(MR), Cloze/Drop-Down, Highlight, Ordered/Drag-Drop, Fill-in-Blank/Dosage, Hot Spot, Exhibit, Graphic, Trend, Audio, Case Study (6-item)**.
**Done when:** a learner browses connected content and practices every common item type.

### Phase C — Learner experience *(engineer + AI)*
Dashboard (readiness, pass probability, per-domain mastery, improvement-over-time) · Smart Study (`/me/next`) · **CAT ↔ pop-quiz ↔ mini-prep loop** · Esi tutoring (structured-first, personalized) · spaced-repetition reviews · flashcards.
**Done when:** the platform adapts to the learner and visibly shows improvement.

### Phase D — Community *(engineer)*
Twitter/X-style feeds + threads, full media (text, image, video, GIF) with upload pipeline + moderation/reporting. Readable by visitors; posting for members. No profile feed.
**Done when:** nurses and visitors can post, reply, and share media safely.

### Phase E — Billing + launch *(engineer + owner)*
Plans (1/2/3/6-month, Esi included), checkout (Stripe), entitlement gating, marketing site → web-app funnel, anti-scrape/CDN, analytics.
**Done when:** a user can subscribe and unlock the full bank; public launch of the web app.

### Phase F — Native app *(later)*
React Native app on the same APIs: offline study, push (Question of the Day), camera OCR, voice quizzes.

*(Deferred well beyond launch: Simulation/virtual hospital, 3D models, live tutoring, career center — all plug into the same ecosystem when their time comes.)*

---

## 4. Who does what
| Work | AI (Claude) | Engineer | Nurse SME (review) | Owner (decide) |
|---|---|---|---|---|
| This blueprint & specs | ✅ done | review | — | approve |
| DB schema + API build | draft/scaffold | ✅ build | — | approve stack |
| Content & questions (batches) | ✅ draft | ingest | ✅ verify before publish | quality bar |
| Item-type interfaces | prototype | ✅ productionize | test realism | — |
| Esi prompts/rules | ✅ author | integrate | safety review | tone |
| Community + billing | spec | ✅ build | — | pricing/policies |

**Bottom line for the owner:** you'll need **an engineer** (or dev shop) for Phases A–E and **at least one nurse SME** to sign off on clinical content. AI (me) can draft specs, content, question batches, Esi logic, and prototype interfaces; a developer turns them into the production web app.

---

## 5. Content production plan
- **Benchmark-first:** author a **250-question RN benchmark** (≈30 per core category) to lock quality + pipeline, then scale toward the **5,000–8,000 launch milestone**, then beyond.
- **Batches of ~25**, each: AI drafts → validator passes → nurse SME approves → publish. Same flow as the current `data/qbank` pipeline, formalized into the DB.
- **Gold modules** (full NKE topics) in parallel: Heart Failure ✅ → **Diabetes** → sepsis, COPD, stroke, renal failure, etc.

---

## 6. Milestones & definition of done
1. **M1 – Blueprint approved** (this + the two specs). *You are one approval away.*
2. **M2 – Foundation live** (Phase A): author→answer→record works end-to-end.
3. **M3 – First learning slice** (Phase B partial): Heart Failure module + 250 benchmark questions playable in the web app across built item types.
4. **M4 – Adaptive learner** (Phase C): dashboard + pop-quiz/mini-prep loop + Esi.
5. **M5 – Community** (Phase D).
6. **M6 – Paid launch** (Phase E): subscriptions live, web app public.
7. **M7 – Native app** (Phase F).

---

## 7. Where the owner makes the call
- Approve the stack (or defer to the engineer you hire).
- Approve pricing/policies and the clinical-quality bar.
- Decide the hiring path: solo engineer, dev shop, or AI-drafts + contractor-implements.
- Sign off (via nurse SME) on clinical content before publish.

## 8. Risks & mitigations
- **Clinical accuracy** → nurse-SME review gate; references logged; never auto-publish.
- **Scope creep** (the vision is huge) → phase gates; deferred list; thin slices.
- **Content scale** → benchmark-first + batch pipeline + validators, not a big unreviewed dump.
- **AI safety (Esi)** → educational-only, structured-first, disclaimers, paywalled.
- **Community moderation** → reporting + rules from day one (required once video is allowed).

---

## 9. Recommended immediate next steps (my call)
1. **You approve the three blueprint docs** (or mark changes).
2. I **draft the second gold module (Diabetes)** to prove the templates across another system — pure content, no engineering needed, and it de-risks the template.
3. In parallel, when you're ready for engineering, I can **scaffold the database in Supabase** (schema from the API doc) so the foundation exists to build against.

*This plan is the last of the three blueprint documents. Together — Master Spec (what) · Database & API (how) · Build Plan (order/who) — they're a complete, hand-off-ready blueprint.*
