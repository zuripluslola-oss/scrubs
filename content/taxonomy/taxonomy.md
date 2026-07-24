# Master Taxonomy & Code Tables (v1)

Authoritative code tables for the Nursing Knowledge Index. All content and questions reference these codes.

## 1. Content type codes
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

## 2. Body system codes
| Code | Body System |
|------|-------------|
| CV | Cardiovascular |
| RESP | Respiratory |
| NEURO | Neurological |
| GI | Gastrointestinal |
| RENAL | Renal / Urologic |
| ENDO | Endocrine |
| MSK | Musculoskeletal |
| HEME | Hematologic |
| INF | Immune / Infectious |
| REPRO | Reproductive / Obstetric |
| INTEG | Integumentary |
| PSY | Psychiatric |

## 3. NCLEX Client Needs codes
| Code | Category |
|------|----------|
| SMS | Safe & Effective Care Environment (Management of Care / Safety) |
| HPM | Health Promotion & Maintenance |
| PSY | Psychosocial Integrity |
| BPI | Basic Care & Comfort |
| PHA | Pharmacological Therapies |
| RRT | Reduction of Risk Potential |
| PAD | Physiological Adaptation |

## 4. Clinical Judgment (NGN) codes
| Code | Skill |
|------|-------|
| REC | Recognize Cues |
| ANA | Analyze Cues |
| PRI | Prioritize Hypotheses |
| GEN | Generate Solutions |
| ACT | Take Action |
| EVA | Evaluate Outcomes |

## 5. Difficulty scale
| Level | Description |
|-------|-------------|
| 1 | Foundational |
| 2 | Basic Application |
| 3 | Clinical Application |
| 4 | Prioritization |
| 5 | Complex NGN / Critical Thinking |

## 6. Additional tag dimensions
- **Age group:** Adult · Pediatric · Neonatal · Geriatric
- **Care setting:** ER · ICU · Med-Surg · L&D · Pediatrics · Community
- **Exam:** RN · PN · Specialty

## 7. Display ID convention
`<TYPE>-<SYSTEM>-####` — sequential per system. Examples: `DIS-CARD-0001` (Heart Failure), `QBK-CV-0001` (first CV question), `NGN-0001` (NGN case). Display IDs are permanent and never reused; each object also has a stable UUID.
