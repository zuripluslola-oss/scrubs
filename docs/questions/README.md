# Question Bank

Production NCLEX/NGN questions for the Must Love Scrubs Nursing Knowledge Index.
**One JSON object per file**, following the Master Question Schema (`content/templates/question-template.md`).

## File naming
`<DISPLAY_ID>-<slug>.json` — e.g. `QBK-CV-0001-hf-priority-intervention.json`, `NGN-0001-dka-matrix.json`.

## Display ID scheme
- `QBK-<SYSTEM>-####` — standalone NCLEX items (CV, RESP, NEURO, RENAL, ENDO, GI, HEME, INF, MSK, INTEG, PSY, REPRO).
- `NGN-####` — Next Gen case-study items (Matrix, Bow-Tie, Trend, Cloze, Highlight, Ordered Response).

## Status workflow
`Draft` → `Review` → `Approved` → `Archived`. AI-drafted items ship as **Draft** with `reviewed_by: ""` (PENDING_HUMAN_REVIEW) until a nurse SME verifies clinical accuracy.

## Current contents
| ID | Topic | Type | Status |
|----|-------|------|--------|
| NGN-0001 | DKA vs HHS | Matrix/Grid | (existing) |
| QBK-CV-0001 | HF priority finding | Multiple Choice | Draft |
| QBK-CV-0002 | HF daily-weight teaching | Multiple Choice | Draft |
| QBK-CV-0003 | Furosemide / hypokalemia | Multiple Choice | Draft |
| QBK-CV-0004 | Left-sided HF findings | SATA | Draft |
| QBK-CV-0005 | Lisinopril teaching | Multiple Choice | Draft |
| QBK-CV-0006 | BNP interpretation | Multiple Choice | Draft |
| QBK-CV-0007 | Acute dyspnea priority | Multiple Choice | Draft |
| QBK-CV-0008 | Digoxin apical pulse | Multiple Choice | Draft |
| QBK-CV-0009 | Spironolactone / hyperkalemia | Multiple Choice | Draft |
| QBK-CV-0010 | Low-sodium diet | SATA | Draft |

All QBK-CV items link to Gold Standard Module #001 — `content/modules/DIS-CARD-0001-heart-failure.md`.
