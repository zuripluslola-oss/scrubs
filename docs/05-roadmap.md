# Development Roadmap

## Sequencing principle
Schema and standards first (software company, not content company). Prove one gold-standard module end-to-end, then scale content. Web app before native app.

## Build order (v1)
1. **Data model + schema** — NKI nodes, typed relationships, question schema, user, post/thread. Define API contracts.
2. **Heart Failure module** loaded as the one real content slice (see `content/modules/`).
3. **Learning dashboard + study loop** wired to the knowledge map (answers update readiness + graph neighbors).
4. **Community feed + threads** (text only, nurses + visitors).
5. **Esi** wired to NKI content (structured-first answering).

## What can be automated (with human review)
- AI-drafted question generation following the Master Question Schema. All AI items ship as **Draft / PENDING_HUMAN_REVIEW** until a nurse verifies clinical accuracy.
- Relationship suggestions between nodes (surfaced for editorial confirmation).
- Reusable exhibit objects (nurse notes, labs, MARs) referenced by ID across item types.

## Where human review is required
- Clinical accuracy of every question, rationale, dosage, and lab value.
- Publishing a content object (Draft → Reviewed → Published).
- Any medication safety content (black box warnings, contraindications).

## Scaling strategy
- Content targets: 5,000–8,000 questions as a **launch milestone, not a ceiling**.
- Grow system-by-system (Cardiovascular → Respiratory → Endocrine → …), each seeded from a gold-standard module.
- Modular, reusable clinical exhibits let one scenario power Matrix, Bow-Tie, SATA, Trend, Highlight, Cloze, and Ordered-Response items — mirroring real NGN case studies.

## Deferred to later phases
Native/offline mobile app, Simulation Center, Career Center, ScrubTV, full 40k-term dictionary, instructor tools, live tutoring, leaderboards.
