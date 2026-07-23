#!/usr/bin/env python3
"""MLSCLEX course-coverage report — how many questions each course (track) and
each exam (RN/PN) currently has. Because one question can carry many tracks,
totals overlap by design. Run: python3 tools/course_report.py
"""
import os, glob, json
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_all():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "qbank", "*.json"))):
        try: out += json.load(open(p, encoding="utf-8")).get("questions", [])
        except Exception: pass
    return out

def main():
    items = load_all()
    tracks, exams = Counter(), Counter()
    for q in items:
        for t in q.get("tracks", []): tracks[t] += 1
        for e in q.get("exams", []): exams[e] += 1
    print(f"MLSCLEX course coverage — {len(items)} questions in one shared pool\n")
    print("By exam (a question can serve both):")
    for e, n in exams.most_common():
        print(f"  {e:<6} {n}")
    print("\nBy course / track (overlap by design):")
    for t, n in tracks.most_common():
        print(f"  {t:<26} {n}")
    print("\nEach course is a filtered view of the pool — no duplicated questions.")

if __name__ == "__main__":
    main()
