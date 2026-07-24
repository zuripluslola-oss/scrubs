# Master Question Schema (v1)

Every question — regardless of type (Multiple Choice, SATA, Bow-Tie, Matrix/Grid, Drag-Drop, Ordered Response, Cloze, Highlight/Hot-Spot, Trend, Case Study, Audio, Image) — is stored as **one JSON object per file** under `docs/questions/` (mirrors the existing bank, e.g. `NGN-0001-dka-matrix.json`).

## Field reference

### Identity & lifecycle
| Field | Notes |
|-------|-------|
| `question_id` | Human-readable display id, e.g. `QBK-CV-0001`. Never reused. |
| `uuid` | Stable globally-unique id. |
| `version` | Integer, increments on edit. |
| `status` | `Draft` → `Review` → `Approved` → `Archived`. |
| `author` | e.g. "AI Editorial Team". |
| `reviewed_by` | Empty until a nurse SME verifies clinical accuracy. |
| `last_updated` | ISO date. |

### Classification
| Field | Notes |
|-------|-------|
| `exam` | RN / PN / Specialty |
| `question_type` | Multiple Choice, SATA, Matrix/Grid, Bow-Tie, Cloze, Highlight, Trend, Ordered Response, etc. |
| `difficulty` | Word label (Easy/Medium/Hard) |
| `difficulty_score` | 0–1 (CAT calibration; seeded, refined by analytics) |
| `estimated_cat_level` | Integer CAT level estimate |
| `discrimination` | From analytics later (e.g. 1.15) |
| `client_needs_category` | Full name or code (see taxonomy) |
| `body_system` | See taxonomy |
| `topic` / `subtopic` | e.g. Heart Failure / Left-sided HF |
| `blooms_level` | Knowledge/Comprehension/Application/Analysis… |
| `clinical_judgment_measurement_model` | Recognize/Analyze Cues, Prioritize, Generate, Take Action, Evaluate |

### Content
| Field | Notes |
|-------|-------|
| `key_learning_objective` | Free text |
| `educational_objective_id` | e.g. `CV-HF-001` for curriculum mapping |
| `scenario` | For NGN: setting, nurses_notes, vital_signs, laboratory_results (or reference `exhibits`) |
| `question_stem` | The prompt |
| `options` / `matrix_rows` | Answer choices (per item type) |
| `correct_answer` | Value or array |
| `rationales` | **One per option** (correct and incorrect) |
| `nclex_test_taking_tip` | Strategy note |
| `memory_trick` | Optional mnemonic |
| `clinical_pearls` | Array of high-yield points |
| `key_takeaway` | One-line summary |

### Reuse & linkage
| Field | Notes |
|-------|-------|
| `case_id` | Links to a shared case study, e.g. `CASE-ENDO-001` |
| `exhibits` | Array of reusable exhibit IDs (nurse notes, labs, MARs, orders, ECGs) referenced instead of embedded, so one scenario powers Matrix/Bow-Tie/SATA/Trend/Highlight/Cloze/Ordered items |
| `relationships` | Linked diseases, medications, labs, procedures, flashcards, videos |
| `references` | Editorial source references |
| `keywords` | Search terms |
| `estimated_average_time_seconds` | For pacing |

## Rules
- **Rationale for every option** is mandatory.
- AI-drafted items ship as `status: Draft`, `reviewed_by: ""` (PENDING_HUMAN_REVIEW).
- Prefer **reusable exhibits by ID** over embedding clinical data per question.
- Units follow the existing bank: conventional + SI, e.g. `486 mg/dL (26.9 mmol/L)`.
