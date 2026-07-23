#!/usr/bin/env python3
"""MLSCLEX blueprint-coverage report.

Shows how the question bank is distributed across the 8 NCLEX-RN Client Needs
categories versus the official test-plan target percentages — so you can see, as
you scale, whether the bank is balanced or overloaded in one area.

Uses each item's `client_needs` field; if absent, falls back to a mapping from
`cat`. Run: python3 tools/blueprint_report.py
"""
import os, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Official NCLEX-RN test plan target ranges (percent of the exam).
TARGETS = {
    "Management of Care": (15, 21),
    "Safety and Infection Control": (10, 16),
    "Health Promotion and Maintenance": (6, 12),
    "Psychosocial Integrity": (6, 12),
    "Basic Care and Comfort": (6, 12),
    "Pharmacological and Parenteral Therapies": (13, 19),
    "Reduction of Risk Potential": (9, 15),
    "Physiological Adaptation": (11, 17),
}

# Fallback when an item has no explicit client_needs (rough — SME refines).
CAT_TO_CN = {
    "Pharmacology": "Pharmacological and Parenteral Therapies",
    "Safety": "Safety and Infection Control",
    "Mental Health": "Psychosocial Integrity",
    "Fundamentals": "Basic Care and Comfort",
    "Maternal / Newborn": "Health Promotion and Maintenance",
    "Pediatrics": "Health Promotion and Maintenance",
    "Med-Surg": "Physiological Adaptation",
    "Clinical Judgment": "Management of Care",
}

def load_all():
    items = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "qbank", "*.json"))):
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        items += data.get("questions", [])
    return items

def cn_of(item):
    return item.get("client_needs") or CAT_TO_CN.get(item.get("cat"), "Unmapped")

def main():
    items = load_all()
    total = len(items)
    counts = {k: 0 for k in TARGETS}
    counts["Unmapped"] = 0
    for it in items:
        cn = cn_of(it)
        counts[cn] = counts.get(cn, 0) + 1

    print(f"MLSCLEX blueprint coverage — {total} questions\n")
    print(f"{'Client Needs category':<42}{'n':>4}{'now':>7}{'target':>10}  status")
    print("-" * 76)
    for cat, (lo, hi) in TARGETS.items():
        n = counts.get(cat, 0)
        pct = (n / total * 100) if total else 0
        if pct < lo:
            status = f"↓ under (need ~{round((lo/100*total) - n)} more)"
        elif pct > hi:
            status = "↑ over"
        else:
            status = "✓ balanced"
        print(f"{cat:<42}{n:>4}{pct:>6.1f}%{f'{lo}-{hi}%':>10}  {status}")
    if counts.get("Unmapped"):
        print(f"{'(Unmapped — add client_needs)':<42}{counts['Unmapped']:>4}"
              f"{counts['Unmapped']/total*100:>6.1f}%{'—':>10}")
    print("\nTarget = official NCLEX-RN test plan range. Aim to keep every")
    print("category inside its band as you scale toward 6,500+ questions.")

if __name__ == "__main__":
    main()
