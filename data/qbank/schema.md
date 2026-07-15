# Question Bank — batch schema

The bank is assembled from batch files in this folder (`data/qbank/*.json`).
`tools/build_qbank.py` (and the site build) globs them, **validates**, **de-dupes**,
and **merges** them into one bank that powers `qbank.html`. Add a batch file,
rebuild, and it appears — no code changes.

## File shape

```json
{
  "batch": "pharmacology-01",
  "questions": [ { …question… }, … ]
}
```

## Question shape

| field         | required | notes |
|---------------|----------|-------|
| `id`          | ✅ | unique, kebab (e.g. `pharm-0001`). De-dup key. |
| `exam`        | ✅ | `"RN"` or `"PN"` |
| `cat`         | ✅ | display category (e.g. `"Pharmacology"`, `"Med-Surg"`, `"Maternal / Newborn"`, `"Pediatrics"`, `"Mental Health"`, `"Fundamentals"`, `"Safety"`, `"Clinical Judgment"`) |
| `topic`       | ▫ | free-text sub-topic |
| `difficulty`  | ▫ | `"Easy" | "Moderate" | "Hard"` |
| `type`        | ✅ | `"mc"` today (single answer). `sata` / `matrix` / `bowtie` reserved for later. |
| `free`        | ▫ | `true` → shown in the free sample; else gated. Default `false`. |
| `stem`        | ✅ | the scenario + question text |
| `opts`        | ✅ | array of 4 `{ "t": option text, "r": rationale for THIS option }` |
| `correct`     | ✅ | 0-based index of the correct option (0–3) |
| `tip`         | ▫ | NCLEX tip |
| `pearl`       | ▫ | clinical pearl / memory trick |
| `illustration`| ▫ | described art (for the workbook/app) |
| `pct`         | ▫ | answer-stats `[a,b,c,d]` summing ~100. Auto-generated if omitted. |

## QC gate (before a batch merges)

Verified correct answer · rationale on **every** option · NCLEX-style wording ·
no duplicates · difficulty tagged · **100% original** (never copied from the real
NCLEX, NCSBN, or any provider).

## Validation rules (enforced by the builder)

- `type: "mc"` must have exactly 4 `opts`, each with `t` and `r`.
- `correct` in range 0–3.
- `id` unique across all batches.
- `cat` non-empty. Filters on the page are built from the categories present.
