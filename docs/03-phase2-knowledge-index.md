# Phase 2 — Nursing Knowledge Index (Database Design)

This is the "Google Maps" of nursing knowledge. Every topic is a node; every relationship is a road; everything connects.

## Node types
A small, fixed set of object types — everything belongs to one:

| Node | Examples |
|------|----------|
| Disease | Heart Failure, Stroke, COPD, Pneumonia, DKA, Sepsis |
| Medication | Furosemide, Digoxin, Heparin, Insulin, Metoprolol |
| Lab | BNP, Troponin, CBC, CMP, INR, ABG |
| Procedure | Chest tube, NG tube, Blood transfusion, IV start, Ventilator |
| Symptom / Finding | Chest pain, Dyspnea, Fever, Edema, Confusion |
| Assessment | Auscultation, Palpation, Neuro check, Pain assessment |
| Anatomy | Heart, Kidney, Liver, Brain, Lung, Pancreas |
| Nursing Skill | Prioritization, Delegation, SBAR, Patient teaching |
| Question | NCLEX, NGN, Case study |
| Video / Lesson | Animation, Expert lecture, Clinical scenario |
| Flashcard | Active recall, Rapid review, Image card |
| Image / Diagram | ECGs, Anatomy, Drug maps |

## Relationship engine
Every node carries typed edges to related nodes. Example — **Heart Failure** connects to symptoms (dyspnea, fatigue, edema, orthopnea, weight gain), labs (BNP, potassium, creatinine), medications (furosemide, spironolactone, lisinopril, metoprolol), procedures (daily weights, strict I&O, oxygen therapy, ECG), questions, videos, flashcards, and patient-education points.

## Adaptive learning driven by relationships
When a student misses a question, the system does not simply mark it incorrect — it **updates the student's knowledge map** and raises the priority of the missed concept *and its graph neighbors*. Missing a Heart Failure priority item elevates pulmonary edema, crackles, BNP, furosemide, potassium, daily weight, and oxygen. Adaptive review follows the graph, not just the score.

## Student knowledge graph
Every student has a dynamic map. Instead of a single "82%", the dashboard shows readiness per domain:

```
Cardiovascular  92% █████████▉
Respiratory     71% ███████░░
Pharmacology    61% ██████░░░
Labs            54% █████░░░░
NGN             48% ████░░░░░
Med Calculations 35% ███░░░░░░
```

## Esi memory
Esi remembers patterns: "You always miss insulin," "You struggle with ABGs," "You're excellent with Pediatrics," "You haven't reviewed burns in 18 days," "Your confidence is dropping in electrolytes."

## Clinical Connections panel
Every page has a sidebar answering "If I understand this, what should I learn next?" For **Hyperkalemia**: ECG changes, kidney function, ACE inhibitors, spironolactone, dialysis, cardiac arrhythmias, potassium replacement, insulin + dextrose therapy, calcium gluconate, related NCLEX questions. A guided path instead of a dead end.

## Build principle
Build one complete gold-standard module end-to-end (Heart Failure = #001) with page, links, images, videos, flashcards, memory aids, NCLEX questions, NGN case, Esi prompts, and adaptive metadata. Prove the standard, then replicate.
