# MLSCLEX — Canonical NCLEX item-type spec

Every NCLEX item type, with the exact JSON shape used across the question bank.
The master prompt (given to ChatGPT) outputs this format, so generated items drop
straight into `data/qbank/*.json` with zero conversion. Extends `schema.md`.

## Shared fields (every item)
| field | notes |
|---|---|
| `id` | unique kebab (e.g. `ngn-bowtie-0001`) |
| `exam` | `"RN"` or `"PN"` |
| `cat` | clinical area shown as the category chip (e.g. `"Pharmacology"`, `"Med-Surg"`) |
| `client_needs` | NCLEX Client Needs category (metadata) |
| `topic` | free-text sub-topic |
| `difficulty` | `"Easy" \| "Moderate" \| "Hard"` (loader derives numeric `level` 1–5) |
| `type` | one of the type keys below |
| `cjmm_step` | NCSBN Clinical Judgment step, or `"n/a"` for traditional items |
| `scoring` | `"dichotomous"` (all-or-nothing) or `"partial_credit"` (+/-, floor 0) |
| `stem` | scenario + question |
| `media` | description of any image/audio/chart for the artist/engineer, else `null` |
| `tip` | one-line strategy |
| `pearl` | optional memory trick |
| `free` | optional bool — show in the free sample |
| `exams` | array — which exams this item serves: `["RN"]`, `["PN"]`, or `["RN","PN"]`. Handles RN/PN overlap. |
| `tracks` | array of course slugs this item belongs to (e.g. `["nclex","med-surg","critical-care"]` or `["prenursing-anatomy"]`). A question can be in many courses at once — this is how overlap works. |

## One bank, many courses (the tag model)
There is **one** question pool, not a separate bank per course. Every "course"
— NCLEX-RN, NCLEX-PN, a specialty (Critical Care, ER, L&D…), or a prenursing
subject (Anatomy, Pharmacology) — is just a **filtered view** of the pool by
`exams` + `tracks`. So a single cardiac-dysrhythmia item tagged
`exams:["RN","PN"], tracks:["nclex","med-surg","critical-care","progressive-care"]`
serves five courses with zero duplication. Overlap is a feature.

Course slug taxonomy: `nclex`, plus the 22 specialty slugs
(`med-surg, emergency, critical-care, pediatrics, labor-delivery, neonatal,
oncology, cardiac, perioperative, pacu, psychiatric, geriatrics, home-health,
hospice, rehabilitation, dialysis, wound-care, ambulatory, school,
occupational, long-term-care, progressive-care`), plus prenursing/prereq
tracks (`prenursing-anatomy, prenursing-pharmacology, prenursing-microbiology,
fundamentals, dosage-calc`).

**Every option / target / cell / blank carries its own rationale** (right AND wrong).

## Type-specific shapes

```jsonc
// mc — multiple choice (single)
{ "type":"mc", "opts":[{"t":"…","r":"…"}, …4], "correct": 1 }

// sata — select all that apply
{ "type":"sata", "opts":[{"t":"…","r":"…"}, …5+], "correct":[0,2,3] }

// select_n — multiple response, exactly N
{ "type":"select_n", "pick":3, "opts":[{"t":"…","r":"…"}, …], "correct":[0,1,4] }

// grouping — multiple response grouping
{ "type":"grouping", "groups":[{"label":"Expected","items":[…]},{"label":"Unexpected","items":[…]}],
  "opts":[{"t":"…","r":"…"}], "answer":{ "0":"Expected", "1":"Unexpected" } }

// fill_blank — dosage calc / numeric
{ "type":"fill_blank", "answer":{ "value":2.5, "unit":"mL", "accept":[2.5] }, "r":"show the math" }

// ordered — prioritize / sequence (items[] ARE the correct order; UI scrambles)
{ "type":"ordered", "items":[{"t":"step 1","r":"…"},{"t":"step 2","r":"…"}] }

// hotspot — click a region on a described image
{ "type":"hotspot", "regions":[{"id":"a","label":"…","correct":true,"r":"…"}, …] }

// exhibit — MC/SATA answered from tabbed record
{ "type":"exhibit", "tabs":{ "vitals":"…","labs":"…","orders":"…","notes":"…" },
  "opts":[{"t":"…","r":"…"}], "correct":1 }

// graphic — answer choices are images (described)
{ "type":"graphic", "opts":[{"t":"desc of image A","r":"…"}, …], "correct":0 }

// audio — references a described audio clip
{ "type":"audio", "opts":[{"t":"…","r":"…"}], "correct":2 }  // media describes the clip

// table — chart/table MC
{ "type":"table", "table":{ "cols":[…], "rows":[[…],[…]] },
  "opts":[{"t":"…","r":"…"}], "correct":1 }

// bowtie — 5 targets (2 actions, 1 condition, 2 parameters)
{ "type":"bowtie",
  "actions":   {"prompt":"Actions to take","pick":2,"options":[{"t":"…","r":"…"}],"correct":[0,2]},
  "condition": {"prompt":"Condition","options":[{"t":"…","r":"…"}],"correct":1},
  "parameters":{"prompt":"Parameters to monitor","pick":2,"options":[{"t":"…","r":"…"}],"correct":[0,3]} }

// trend — data trended over time
{ "type":"trend", "timeline":[{"time":"0800","data":{"HR":92,"BP":"110/70"}}, …],
  "opts":[{"t":"…","r":"…"}], "correct":1 }

// matrix — matrix multiple CHOICE (one per row)
{ "type":"matrix", "cols":[…], "rows":[{"t":"finding","correct":0,"r":"…"}, …] }

// matrix_mr — matrix multiple RESPONSE (many per row)
{ "type":"matrix_mr", "cols":[…], "rows":[{"t":"finding","correct":[0,2],"r":"…"}, …] }

// dropdown_table — a dropdown per row
{ "type":"dropdown_table", "cols_prompt":"Select the expected value",
  "rows":[{"t":"…","options":[{"t":"…","r":"…"}],"correct":1}] }

// dropdown_cloze / dd_cloze — sentence with blanks (dropdown vs drag are same data)
{ "type":"dropdown_cloze", "sentence":"The nurse should first {{0}} then {{1}}.",
  "blanks":[ {"options":[{"t":"…","r":"…"}],"correct":0},
             {"options":[{"t":"…","r":"…"}],"correct":2} ] }

// dropdown_rationale / dd_rationale — linked action + because
{ "type":"dropdown_rationale", "sentence":"The client is at risk for {{0}} as evidenced by {{1}}.",
  "blanks":[ {"options":[{"t":"…","r":"…"}],"correct":1},
             {"options":[{"t":"…","r":"…"}],"correct":0} ] }

// highlight_text — select the relevant words/sentences
{ "type":"highlight_text",
  "segments":[{"t":"sentence one.","correct":true,"r":"…"},{"t":"sentence two.","correct":false,"r":"…"}] }

// highlight_table — select the relevant cells
{ "type":"highlight_table", "cols":[…],
  "rows":[{"t":"row label","cells":[{"t":"…","correct":true,"r":"…"}, …]}] }

// casestudy — one unfolding case, 6 linked questions (CJMM)
{ "type":"casestudy",
  "scenario":"…",
  "tabs":{ "history":"…","vitals":"…","labs":"…","orders":"…","nurses_notes":"…","mar":"…" },
  "questions":[ { …any item shape above, with its own id/type/stem/…/rationales… } ] }  // exactly 6
```

## Client Needs categories (for `client_needs`)
Management of Care · Safety and Infection Control · Health Promotion and
Maintenance · Psychosocial Integrity · Basic Care and Comfort · Pharmacological
and Parenteral Therapies · Reduction of Risk Potential · Physiological Adaptation.

## CJMM steps (for `cjmm_step`)
Recognize Cues · Analyze Cues · Prioritize Hypotheses · Generate Solutions ·
Take Actions · Evaluate Outcomes.
