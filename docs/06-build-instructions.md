# Build Instructions (Engineering & Content Standards)

Single reference so every contributor (developer, content author, or AI) builds from the same blueprint.

## Data expectations
- Model the NKI as a **graph**: nodes (typed content objects) + typed edges (relationships). A relational store with a join/edge table or a graph database are both acceptable; the edge semantics matter more than the engine.
- Every content object has a **stable UUID** plus a human-readable **display ID** (e.g. `QBK-CV-0001`, `DIS-CARD-0001`). Never reuse display IDs.
- Every object carries lifecycle metadata: `version`, `status` (Draft → Review → Approved/Published → Archived), `author`, `reviewed_by`, `last_updated`.
- Store rich clinical assets (nurse notes, labs, MARs, orders, ECGs) as **reusable exhibit objects referenced by ID**, not embedded per question, so one scenario powers many item types.

## API conventions
- Content is read through a consistent contract regardless of type: `id`, `type`, `display_id`, `tags`, `body`, `relationships[]`.
- Relationships are first-class and queryable (given a node, return neighbors by edge type).
- Answering a question is an event that updates the student knowledge map server-side.

## UI principles
- Every content page shows a **Clinical Connections** panel ("what to learn next").
- Dashboards show **per-domain readiness**, not a single aggregate score.
- Community is **text-only** feeds + threads (Twitter-style); **no video posting**; **no per-profile feed**.
- Support "Why?" chains and learning paths as navigational primitives.

## Content quality rules
- Every question includes a **rationale for every option** (correct and incorrect), a key takeaway, references, and relationship links.
- AI-drafted content ships as **Draft / `reviewer: PENDING_HUMAN_REVIEW`**; a nurse SME must verify clinical accuracy before `Published`.
- Medication content must state contraindications, key monitoring, and black box warnings where applicable.
- Lab values include normal + critical ranges and nurse notification thresholds.
- Use SI and conventional units where the existing bank does (e.g. `486 mg/dL (26.9 mmol/L)`).

## Esi (AI) integration rules
1. Answer from structured NKI content first, then explain plainly.
2. Match the student's experience level.
3. Explain reasoning, not just the answer.
4. Offer follow-up practice.
5. Link related topics / recommend the next concept.

## Standard question metadata (aligns existing bank + editorial requests)
`question_id` (display) · `uuid` · `version` · `status` · `author` · `reviewed_by` · `last_updated` · `question_type` · `difficulty` + `difficulty_score` · `estimated_cat_level` · `discrimination` (from analytics later) · `client_needs_category` · `body_system` · `topic` / `subtopic` · `blooms_level` · `clinical_judgment_measurement_model` · `key_learning_objective` / `educational_objective_id` · `case_id` · `exhibits[]` · per-option `rationale` · `nclex_test_taking_tip` · `memory_trick` · `clinical_pearls[]` · `references[]` · `keywords[]` · `estimated_average_time_seconds`.
