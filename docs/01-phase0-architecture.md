# Phase 0 — Platform Architecture

## High-level system design
The platform is organized around the **Nursing Knowledge Engine (NKE)** — a central, graph-structured knowledge base that every feature reads from and writes to.

```
                        ┌─────────────────────────┐
                        │  Nursing Knowledge Engine │
                        │   (graph of all concepts) │
                        └────────────┬──────────────┘
        ┌──────────────┬─────────────┼─────────────┬──────────────┐
   Question Engine   Esi (AI)   Dashboard /    Community     Search /
                                Study Engine  (text feeds)    Index
```

## Core objects (node types)
Everything is one of a small set of object types, each connected by typed relationships:

- **Disease / Condition**
- **Medication**
- **Lab Value**
- **Procedure**
- **Symptom / Finding**
- **Assessment**
- **Anatomy & Physiology**
- **Nursing Skill**
- **Question** (NCLEX / NGN)
- **Video / Lesson / Animation**
- **Flashcard**
- **Image / Diagram**

## The AI: Esi
Esi is the tutor/coach/study-partner layer. She always answers from **structured NKI content first**, then explains in plain language. She adapts to the student's level, knows their score, weak topics, study history, specialty, and exam date, and responds personally (e.g. "You keep missing Digoxin questions — here's why, and a practice item").

Esi behavior rules (canonical):
1. Identify the student's level.
2. Explain simply first.
3. Connect symptoms to physiology.
4. Give a memory trick where useful.
5. Ask a practice question.
6. Correct reasoning, not just answers.
7. Recommend the next related concept.

## Adaptive learning
Every answered question updates the student's **knowledge map** (both correct and incorrect). A miss raises the priority of the missed concept *and its graph neighbors*. This produces adaptive review driven by relationships, not just raw scores.

## Product ecosystem (long-term)
Dashboard, smart study engine, memory engine (spaced repetition / active recall / interleaving / forget-curve tracking), visual learning, simulation center, community, career center, mobile app, ScrubTV. See `04-scope-v1-webapp.md` for the subset in v1.

## Design stance
Build like a software company: define schema, API contracts, content standards, and AI integration rules **before** producing content at scale, so every future feature plugs into the same ecosystem.
