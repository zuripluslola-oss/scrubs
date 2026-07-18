# Must Love Scrubs — Master Specification (v1)
### The Everything Platform for Nurses
*Single source of truth. Every page, question, AI response, and search result builds from this document. Supersedes scattered chat history; extends the design bible (`.claude/skills/mls-design-system`).*

**Status:** Blueprint — confirm & outline phase. **We are NOT building the website or app yet.** We lock the architecture, then build a **web app** first, and only later a publishable (native) app.

---

## 0. What we are and aren't building right now

**Building now:** the *specification* — taxonomy, data model, content templates, relationship rules, question schema, AI rules, roadmap. The plan a developer/content team follows.

**Build order (locked):**
1. **Confirm & outline** the project (this document). ← we are here
2. **Web app** (the real product, database-backed).
3. **Publishable app** (native mobile) — later, plugging into the same APIs.

**Explicitly deferred (do not build yet):** native mobile app, the current static marketing site as the product, simulation/virtual hospital, 3D models, live tutoring, career center. These stay on the roadmap; they plug into the same ecosystem when their time comes.

**The current static site** (the clickable preview we built) remains a **marketing/prototype front** — useful for showing the vision. The web app is a separate, database-backed build.

---

## 1. Master Vision

**Mission:** Be the operating system for nursing education — not another NCLEX site, but the connected knowledge engine nurses use from school through licensure and into practice.

**Positioning:** Netflix × Duolingo × MasterClass for nursing, built "for nurses, by nurses." Competitors (Bootcamp, UWorld, nursing.com, Archer, Kaplan, Hurst) sell question banks + videos. Our moat is the **Nursing Knowledge Engine**: every concept connected, so learning is a *guided path*, not a pile of pages.

**Durable advantage:** built like a software company — schema, API contracts, content standards, and AI rules defined *before* mass content. New features plug into the same ecosystem instead of being rebuilt.

**Launch milestone (not a ceiling):** 5,000–8,000 questions. Architecture must scale far beyond without redesign. Value = quality + connections + personalization, not raw count.

---

## 2. Phase 0 — Platform Architecture

### The core: Nursing Knowledge Engine (NKE)
One central brain. Every object (disease, drug, lab, procedure, symptom, skill, question, video, flashcard) is a **node**; every relationship is an **edge**. A single concept (e.g., Heart Failure) links to its symptoms, meds, labs, interventions, procedures, videos, images, questions, NGN cases, flashcards, memory tricks, Esi explanations, specialties, anatomy, and patient education.

### Product ecosystem (modules that ride on the NKE)
- **Learning:** Nurse/Scrubs Dictionary, Disease Encyclopedia, Medication Center, Lab Center, Procedure Library, Clinical Skills Library, Anatomy & Physiology.
- **Practice:** Question Engine (all NGN item types), NGN Case Studies, Flashcards (spaced repetition), Smart Study Engine (daily plan), Memory Engine.
- **Esi (AI):** tutor / coach / study partner / mentor — personalized to the student's data.
- **Dashboard:** readiness, pass probability, weak/strong areas, streaks, per-domain scores.
- **ScrubTV:** media network (videos, channels, rapid reviews) — *watch only; no user video uploads*.
- **Community:** Twitter-style feeds + threads for nurses and visitors (see §7).
- **Later (deferred):** Simulation Center, Career Center, native mobile app.

### AI strategy (Esi)
Esi answers from **structured NKE content first**, then explains in plain language. She is personalized (knows score, weak topics, history, specialty, exam date, confidence), explains *reasoning* not just answers, offers follow-up practice, and links related concepts. Guardrails from the design bible remain: educational tutor only, never diagnoses/prescribes, paywalled (no free open chat).

---

## 3. Phase 1 — Master Content Architecture

### 3.1 Content types (codes)
`NKI` topic · `DIS` disease · `MED` medication · `LAB` lab · `PRO` procedure · `SKL` clinical skill · `ANA` anatomy/physiology · `SYM` symptom · `ASM` assessment · `QBK` question · `NGN` case study · `FLS` flashcard · `VID` video · `IMG` image/diagram · `EDU` patient education · `PATH` learning path.

### 3.2 Taxonomy tags (every item is tagged)
- **Body system:** Cardiovascular · Respiratory · Neurological · Renal/Urologic · Endocrine · Gastrointestinal · Hematologic · Immune/Infectious · Musculoskeletal · Integumentary · Reproductive/OB · Neonatal · Pediatric · Psychiatric.
- **Specialty:** the 22 any-RN specialties (design bible list).
- **NCLEX Client Needs:** `SMS` Safe & Effective Care · `HPM` Health Promotion · `PSY` Psychosocial · `BPI` Basic Care & Comfort · `PHA` Pharmacological · `RRT` Reduction of Risk · `PAD` Physiological Adaptation.
- **Clinical Judgment (NGN):** `REC` Recognize Cues · `ANA` Analyze Cues · `PRI` Prioritize Hypotheses · `GEN` Generate Solutions · `ACT` Take Action · `EVA` Evaluate Outcomes.
- **Difficulty (1–5):** 1 Foundational · 2 Basic Application · 3 Clinical Application · 4 Prioritization · 5 Complex NGN/Critical Thinking. *(Maps to the qbank engine's numeric `level`.)*
- **Age group:** Adult · Pediatric · Neonatal · Geriatric. **Care setting:** ER · ICU · Med-Surg · L&D · Pediatrics · Community · LTC.
- **Exam:** RN · PN · Specialty. **Bloom level.** **Estimated time.**

### 3.3 ID convention
`TYPE-SYSTEM-####` → e.g. `DIS-CV-0001` (Heart Failure), `MED-CV-0007` (Furosemide), `LAB-CV-0002` (BNP), `QBK-CV-0001`. Stable, unique, human-readable. De-dup key.

### 3.4 Content templates (locked)
Each content type has a fixed template so thousands of entries stay consistent. Summaries below; full field lists in §5 of the design bible + this doc's appendix intent.
- **Disease:** definition · causes · risk factors · pathophysiology · signs/symptoms · assessment · diagnostics · lab findings · nursing diagnoses · interventions · medications · patient teaching · complications · priority actions · NCLEX tips · related questions/videos/terms.
- **Medication:** identity (generic/brand/classes/pronunciation) · overview · MOA · uses · dosage/routes · contraindications · warnings (incl. black box) · side effects (common/serious/life-threatening) · nursing considerations (pre/during/post) · patient education · related content.
- **Lab:** identity · normal & critical values (adult/peds) · purpose · high causes · low causes · nursing actions · notification thresholds · patient education · related content.
- **Procedure:** identity/setting · purpose/indications · equipment · preparation · steps · risks/complications · nursing responsibilities (before/during/after) · patient teaching · documentation · related content.
- **Clinical Skill / Anatomy / Flashcard / Video / Image / Patient Education:** each has its own locked template (see §6 modules of prior spec).

### 3.5 Relationship engine
Every item declares typed links to related items. Powers "related content," Clinical Connections sidebar, adaptive review, and search. Example — **Hyperkalemia** auto-links: diseases (AKI, CKD, Addison's), meds (spironolactone, lisinopril, K⁺ supplements), labs (K⁺, BUN, creatinine), procedures (dialysis, ECG monitoring), questions & NGN cases.

### 3.6 Search & index rules
Any query (synonym, abbreviation, brand/generic) returns a **unified result**: primary page + related meds/labs/procedures + NCLEX questions + NGN cases + flashcards + Esi explanation + videos. Example: "Lasix" → Furosemide (primary) + Heart Failure/Pulmonary Edema + K⁺/Na⁺ + IV administration + 12 questions + 2 cases.

### 3.7 AI integration rules
Esi: structured content first → plain-language explanation → matches level → explains reasoning → offers practice → links related topics. Every AI answer is traceable to NKE nodes.

---

## 4. Phase 2 — Nursing Knowledge Index (the graph)

### 4.1 Node & edge model
Nodes = content objects (§3.1). Edges = typed relationships (has-symptom, treated-by, monitored-with, causes, complication-of, tested-by, teaches, assesses, links-to). This is the "Google Maps of nursing knowledge."

### 4.2 Adaptive learning via relationships (the secret weapon)
A wrong answer is not just "incorrect." Missing a hyperkalemia question raises priority on the *connected* nodes: potassium physiology, ECG changes, kidney disease, ACE inhibitors, spironolactone, dialysis, arrhythmias, related labs, fluid/electrolyte disorders. The system builds a **personalized learning path** from the graph, not just a score.

### 4.3 Student knowledge graph
Each student has a dynamic map: per-domain mastery (Cardiovascular 92%, Pharmacology 61%, Labs 54%, NGN 48%, Med Calc 35%…), a forgetting-curve per node, confidence scores, and history. Esi's memory reads this ("you always miss insulin," "haven't reviewed burns in 18 days," "confidence dropping in electrolytes").

### 4.4 Signature UX features
- **Clinical Connections panel** (sidebar): "if you understand this, learn next…" — a guided path.
- **"Why?" chain:** tap Why repeatedly to drill from a finding down through physiology, each step a deeper NKE link.
- **Concept maps:** interactive visual branches (e.g., Sepsis → infection, lactate, cultures, antibiotics, fluids, vasopressors, organ dysfunction, shock).

### 4.5 CAT ↔ pop quizzes & mini-prep ↔ visible improvement (locked)
This is one closed loop, not separate features:
1. **CAT / readiness exam** estimates the student's ability and pinpoints weak nodes (by system, topic, and clinical-judgment step).
2. Those weak nodes are pushed into **pop quizzes** (short, adaptive, 5–10 items that surface at smart moments) and **mini-prep** (focused micro-lessons + drills on exactly those gaps).
3. Every attempt updates the **student knowledge graph** (mastery + spaced-repetition schedule), which **re-feeds the next CAT** — so the adaptive test, the pop quizzes, and the mini-prep are all driven by the *same* mastery data.
4. **Improvement is shown, not implied:** the dashboard tracks each domain's mastery **over time** (before → after), readiness trend (Low → Very High), a per-topic "then vs now," and pop-quiz score deltas — so the student literally sees weak areas turning into strong ones.

**Is this how it works already?** The *architecture* already supports it — the design uses one shared mastery store that feeds `/me/next` (smart study) and the dashboard. What this update does is make the loop **explicit and named**: CAT results must generate targeted pop quizzes + mini-prep, and the dashboard must show the before/after improvement, not just a current score.

---

## 5. Data model & schema (build-like-a-software-company)

*Relational core + a graph/edge table for relationships. Illustrative — the developer finalizes types, but these contracts are locked in intent.*

**`nodes`** — `id` (TYPE-SYS-####, PK) · `type` · `title` · `body_system` · `specialties[]` · `difficulty` (1–5) · `client_needs[]` · `cj_steps[]` · `age_groups[]` · `care_settings[]` · `status` (draft/reviewed/published) · `version` · `updated_at` · `body` (structured JSON per template) · `search_terms[]`.

**`edges`** — `from_id` · `to_id` · `relation` (typed) · `weight`. (Directional; powers related-content + adaptive priority.)

**`questions`** (extends node) — `type` (mc/sata/matrix/bowtie/dropdown/ordered/hotspot/trend/audio/image/casestudy) · `stem` · `options[]` (each `{text, rationale}`) · `correct` (index | list | per-part) · `tip` · `pearl` · `references[]` (internal QC) · `learning_objective` · `bloom` · `est_time` · `links[]` (diseases/meds/labs/procedures) · plus all node tags. **Rationale required for every option (validator-enforced).**

**`users`** · **`attempts`** (user_id, question_id, chosen, correct, ms, ts) · **`mastery`** (user_id, node_id, score, confidence, last_seen, next_review) · **`streaks`** · **`entitlements`** (plan, expiry, esi_included).

**`posts`** / **`threads`** (community — §7).

**Content standards:** 100% original; QC gate per item (verified answer, NGN wording, no ambiguity, rationale per option, difficulty tagged, dedup, correct placement, references logged). Free/paid gating is a data flag (`free`), not code.

**API contracts (intent):** `GET /node/:id` (with related), `GET /search?q=`, `GET /questions?filters`, `POST /attempt`, `GET /me/dashboard`, `GET /me/next` (smart study), `POST /esi/ask` (returns answer + cited node ids), community `GET/POST /threads`. Same APIs serve web app now and native app later.

---

## 6. Question Engine — ALL NCLEX + NGN item types (verified vs NCSBN)

We support the **complete** set. NCSBN uses **2 stand-alone** NGN item types (bow-tie, trend) plus **12 case-study** NGN item types, alongside the **traditional** item types that remain on the exam. Our engine must cover every one.

**Traditional NCLEX item types**
1. **Multiple Choice** (single answer) — *built*
2. **Multiple Response / Select All That Apply (SATA)** — *built*
3. **Fill-in-the-Blank / Dosage Calculation** (numeric entry) — planned
4. **Ordered Response** (drag-to-rank) — planned
5. **Hot Spot** (click the region on an image) — planned
6. **Chart / Exhibit** (tabbed EHR + question) — planned
7. **Graphic Options** (answer choices are images) — planned
8. **Audio** (listen, then answer) — planned

**NGN stand-alone item types**
9. **Bow-Tie** (condition + actions + parameters) — *built*
10. **Trend** (data across multiple time points) — planned

**NGN case-study item types (the 12, as families + variants)**
11. **Matrix** — Matrix Multiple Choice *(built)* + Matrix Multiple Response (multi-pick per row) — planned variant
12. **Extended Multiple Response** — SATA / **Select-N** / **Grouping**, with **partial credit** — planned
13. **Cloze / Drop-Down** — drop-down, drop-down cloze, drop-down table, drop-down **rationale** — planned
14. **Extended Drag-and-Drop** — incl. **drag-and-drop cloze** (not every token must be used) — planned
15. **Enhanced Hot Spot / Highlight** — highlight **text** or highlight **table** — planned
+ **Unfolding Case Study** — the wrapper: **6 items** stepping through the 6 clinical-judgment stages (Recognize → Analyze → Prioritize → Generate → Take Action → Evaluate).

**Built today (qbank engine):** MC, SATA, Matrix (multiple-choice), Bow-Tie. Everything else is specified and planned; each gets its own interface + scoring, added one at a time.

**Every question (all types):** rationale for right *and* wrong, difficulty (1–5), topic, specialty, NCLEX Client-Needs category, clinical-judgment step, est. time, references, and NKE links. Partial-credit scoring where NCSBN uses it (SATA/extended multiple response, matrix, bow-tie). CAT-ready: difficulty drives adaptive item selection (IRT/Rasch-style; recalibrated from real `attempts` data).

---

## 7. Community — Twitter-style for nursing (locked decision)

- **Format:** **feeds + threads**, full X/Twitter-style, for **nurses and visitors** alike.
- **Full media posting — text, images, video, and GIFs** (whatever you can do on Twitter/X). Users can post video here. *(ScrubTV stays a separate, curated MLS media network; the community is user-generated.)*
- **Profiles have NO feed** — profiles stay focused on learning/dashboard, not a social wall.
- **Keep the learning dashboard as-is for now.**
- Purpose: discussion, tips, encouragement, study-group energy — the community moat competitors' closed Facebook groups can't match, native to the platform.
- Moderation & safety required for user media (report/flag, content rules) since video/images are allowed.
- Roadmap extras (later): study groups, leaderboards, weekly challenges, mentors.

---

## 8. Gold Standard Module #001 — Heart Failure

The proven template for every future topic. Full module authored (`DIS-CV-0001`): Quick Learn · pathophysiology map · left/right types with memory hooks · assessment · labs (BNP, troponin, electrolytes, creatinine) · medication connections (furosemide, lisinopril, metoprolol, spironolactone, digoxin) · priority nursing actions · patient education · "PUMP" memory system · linked NCLEX question · NGN case (recognize→analyze→take action) · connected knowledge index · Esi training prompt. **Standard = build one gold module end-to-end, approve it, then replicate.** Next gold module: **Diabetes Mellitus** (tests endocrine + meds + labs + calculations + complications + NGN).

---

## 9. Development roadmap

1. **Confirm this spec** (now).
2. **Foundation build:** database (nodes/edges/questions/users/mastery), API contracts, auth, content-ingest pipeline (extends the existing `data/qbank` batch pipeline — same schema philosophy).
3. **Web app v1:** Dictionary + Disease/Med/Lab/Procedure pages (NKE-linked) · Question Engine (all types) · Dashboard · Esi (structured-first) · Smart Study · Community (feeds/threads).
4. **Content at scale:** gold modules → replicate; question batches toward 5–8k (benchmark-first, QC gate).
5. **Native app:** wraps the same APIs.

**Automate vs. human:** AI drafts content/questions in batches → **human (nurse SME) review before publish** (status flag). Never ship unreviewed clinical content.

---

## 10. Build instructions & standards (for Claude / developers)

- **Software-company discipline:** schema + API contracts + content standards + AI rules are locked *before* mass content. Features plug into the NKE; nothing is rebuilt per feature.
- **IDs & templates are mandatory** — no free-form pages. Every item validates against its template + tag set (extend `tools/build_qbank.py`-style validators to all content types).
- **Relationships are first-class** — every item ships with its edges; "related content" and adaptive learning depend on them.
- **Original content only**, QC gate enforced, references logged internally.
- **UI principles:** mobile-first, the locked Violet & Mint design system, accessible, fast. Esi paywalled, educational-only disclaimer.
- **Data-driven gating** (free/paid) — flags, not forks.
- **Web app before native app**; both consume identical APIs.

---

## 11. Locked decisions captured from this session
- Do **not** build the website or app now — confirm & outline first.
- **Web app first**, publishable (native) app later.
- Community = **full Twitter-style feeds + threads** (text, images, **video**, GIFs), nurses **and** visitors.
- **Profiles: no feed.** **Dashboard: keep learning focus for now.**
- **CAT ↔ pop quizzes ↔ mini-prep** is one loop on shared mastery data; dashboard shows **improvement over time** (§4.5).
- **All NCLEX + NGN item types** are in scope (§6), verified against NCSBN.
- Everything hangs off the **Nursing Knowledge Engine** (connected nodes + edges).
- Gold-standard-module approach: perfect one, then replicate (HF done; Diabetes next).
- Launch target 5–8k questions; architecture scales beyond without redesign.

---

*End of Master Specification v1. Next step on approval: turn §5 (data model) + §6 (question engine) into the concrete database + API contract document, then scaffold the web app foundation.*
