# Phase 1 — Master Content Architecture

This is the "DNA" of Must Love Scrubs: taxonomy, metadata, templates, relationships, search, and AI rules that every page and question follows.

## Module 1 — Master Taxonomy
Content types (with codes). See `content/taxonomy/taxonomy.md` for the authoritative tables.

| Code | Content Type |
|------|--------------|
| NKI | Nursing Knowledge Index Topic |
| DIS | Diseases & Conditions |
| MED | Medications |
| LAB | Lab Values |
| PRO | Procedures |
| SKL | Clinical Skills |
| ANA | Anatomy & Physiology |
| QBK | NCLEX Question |
| NGN | NGN Case Study |
| FLS | Flashcard |
| VID | Video |
| IMG | Image / Diagram |

## Module 2 — Master Topic Map (tags)
Every item is tagged by: **Body System · Nursing Specialty · NCLEX Client Needs · Difficulty · Clinical Judgment skill · Age Group · Care Setting.** These tags power search, recommendations, adaptive quizzes, and reporting.

## Module 3 — Content Templates
Every content type has a standard template. The locked templates live in `content/templates/`:
- Disease, Medication, Lab, Procedure, Question, Flashcard, Video, Image.

## Module 4 — Relationship Engine
Every item links to related content via typed edges. Example — **Hyperkalemia** auto-links to AKI/CKD/Addison (diseases), spironolactone/lisinopril/K+ supplements (meds), potassium/BUN/creatinine (labs), dialysis/ECG monitoring (procedures), and its NCLEX/NGN question sets. This powers "related content," Clinical Connections sidebars, and personalized paths.

## Module 5 — Question Standards
Every question carries a unique ID, learning objective, NCLEX category, topic, difficulty, type, correct answer, **rationales for all options**, references, and links to related diseases/meds/labs/procedures. Full schema in `content/templates/question-template.md`.

## Module 6 — AI Rules (Esi)
Esi answers from structured content first, matches the student's level, explains reasoning, offers follow-up practice, and links related topics. (Canonical 7-step behavior in `01-phase0-architecture.md`.)

## Deliverables of Phase 1
Complete taxonomy · templates for every content type · relationship rules · metadata standards · question specification · AI integration standards. A blueprint developers and content creators follow consistently.

## Additional Phase-1 concepts
- **Learning Paths** — guided sequences per topic (e.g. Heart Failure: anatomy → physiology → overview → S/S → assessment → labs → meds → interventions → teaching → questions → NGN → review).
- **Concept Maps** — interactive visual branching of a topic (e.g. Sepsis → infection, inflammation, lactate, cultures, antibiotics, vasopressors, fluids, organ dysfunction, shock).
- **"Why?" chains** — every topic supports repeatedly tapping "Why?", each answer linking deeper into the NKI to encourage understanding over memorization.
