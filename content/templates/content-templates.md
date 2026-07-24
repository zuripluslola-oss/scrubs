# Locked Content Templates (v1)

Every content object follows the template for its type. All templates share **universal metadata**: `uuid`, `display_id`, `version`, `status` (Draft → Review → Approved/Published → Archived), `author`, `reviewed_by`, `last_updated`, plus tag dimensions (body system, specialty, NCLEX client needs, difficulty, clinical judgment, age group, care setting) and a **Relationships** block (diseases, meds, labs, procedures, questions, flashcards, videos, images).

---

## Disease template
- Definition
- Causes
- Risk factors
- Pathophysiology
- Signs & symptoms
- Assessment
- Diagnostics
- Lab findings
- Nursing diagnoses
- Interventions (priority actions)
- Medications
- Patient teaching
- Complications
- NCLEX tips
- Relationships (questions, NGN cases, videos, dictionary terms)

## Medication template
- **Identity:** generic name, brand name(s), drug class, pharmacologic class, therapeutic class, pronunciation
- **Overview:** what it is, why it's used, mechanism of action
- **Clinical uses:** primary indications, notable off-label uses
- **Dosage & administration:** adult dose, pediatric dose (when applicable), routes, admin tips
- **Contraindications:** absolute, relative
- **Warnings & precautions:** high-risk populations, pregnancy/lactation, black box warnings
- **Side effects:** common, serious, life-threatening
- **Nursing considerations:** pre-administration assessment, monitoring during, post-administration monitoring
- **Patient education:** how to take, what to avoid, when to seek help
- **Relationships**

## Lab value template
- **Identity:** name, abbreviation, specimen type
- **Normal range:** adult, pediatric (when applicable)
- **Critical values**
- **Purpose:** why ordered, what it measures
- **High values:** common causes, clinical significance
- **Low values:** common causes, clinical significance
- **Nursing actions:** assessment priorities, immediate interventions, provider notification thresholds
- **Relationships**

## Procedure template
- **Identity:** name, setting(s)
- **Purpose:** why performed, indications
- **Equipment needed**
- **Preparation:** patient prep, supplies, safety checks
- **Procedure steps:** step-by-step workflow
- **Risks & complications**
- **Nursing responsibilities:** before, during, after
- **Patient teaching**
- **Documentation**
- **Relationships**

## Question template (master schema)
See `question-template.md` for the full JSON field list. Question files live in `docs/questions/` (one JSON object per file). Core: metadata (id/uuid/version/status/author/reviewer/last_updated) · classification (exam, topic, body system, specialty, difficulty + difficulty_score, client needs, clinical judgment, type) · content (learning objective, stem, options, correct answer, **rationale for every option**, key takeaway) · references · relationships · reusable exhibits by ID.

## Flashcard template
`id` · front (term/question/image/prompt) · back (answer/explanation) · difficulty · related topics · last_reviewed · next_review (spaced repetition).

## Video template
`id` · title · duration · learning objectives · transcript · chapters · related NKI topics · related questions · related flashcards · suggested next lesson.

## Image / diagram template
`id` · title · description · alt text · related diseases · related medications · related procedures · related questions.

## Learning path template
Ordered sequence of NKI nodes forming a guided path (e.g. Heart Failure: heart anatomy → cardiac physiology → HF overview → S/S → assessment → labs → medications → interventions → patient education → practice questions → NGN case → review quiz).
