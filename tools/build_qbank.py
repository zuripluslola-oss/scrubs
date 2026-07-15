#!/usr/bin/env python3
"""Validate + summarize the question-bank batches in data/qbank/.

Run this after adding or editing a batch file. It checks every question against
the schema, reports duplicates and errors, and prints per-category counts.
The site build (tools/build_pages.py) uses the same rules to assemble the bank.
"""
import os, glob, json, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(ROOT, 'data', 'qbank')

REQUIRED = ['id', 'exam', 'cat', 'type', 'stem']  # per-type fields checked below


def main():
    files = sorted(glob.glob(os.path.join(QDIR, '*.json')))
    seen, errors, cats = {}, [], collections.Counter()
    total = free = 0

    for path in files:
        name = os.path.basename(path)
        try:
            data = json.load(open(path, encoding='utf-8'))
        except Exception as e:
            errors.append(f'{name}: invalid JSON — {e}'); continue
        for n, q in enumerate(data.get('questions', [])):
            where = f'{name} #{n + 1} ({q.get("id", "no-id")})'
            for k in REQUIRED:
                if k not in q:
                    errors.append(f'{where}: missing "{k}"')
            t = q.get('type', 'mc')
            if t == 'mc':
                if len(q.get('opts', [])) != 4:
                    errors.append(f'{where}: MC needs exactly 4 options')
                for o in q.get('opts', []):
                    if 't' not in o or 'r' not in o:
                        errors.append(f'{where}: an option is missing text or rationale')
                if not (0 <= q.get('correct', -1) <= 3):
                    errors.append(f'{where}: correct index out of range')
            elif t == 'sata':
                if len(q.get('opts', [])) < 3:
                    errors.append(f'{where}: SATA needs 3+ options')
                if not isinstance(q.get('correct'), list) or not q['correct']:
                    errors.append(f'{where}: SATA correct must be a non-empty list of indices')
                elif any(not (0 <= i < len(q.get('opts', []))) for i in q['correct']):
                    errors.append(f'{where}: SATA correct index out of range')
            elif t == 'matrix':
                if len(q.get('cols', [])) < 2:
                    errors.append(f'{where}: matrix needs 2+ columns')
                for r in q.get('rows', []):
                    if 't' not in r or not (0 <= r.get('correct', -1) < len(q.get('cols', []))):
                        errors.append(f'{where}: a matrix row is missing text or has a bad correct index')
                    if not r.get('r'):
                        errors.append(f'{where}: a matrix row is missing its rationale ("r")')
            elif t == 'bowtie':
                for part in ('condition', 'actions', 'parameters'):
                    p = q.get(part) or {}
                    opts = p.get('options', [])
                    if len(opts) < 2:
                        errors.append(f'{where}: bow-tie {part} needs 2+ options')
                    for o in opts:
                        if 't' not in o or 'r' not in o:
                            errors.append(f'{where}: a bow-tie {part} option is missing text or rationale')
                    c = p.get('correct')
                    if part == 'condition':
                        if not isinstance(c, int) or not (0 <= c < len(opts)):
                            errors.append(f'{where}: bow-tie condition correct must be a valid index')
                    else:
                        if not isinstance(c, list) or not c:
                            errors.append(f'{where}: bow-tie {part} correct must be a non-empty list')
            else:
                errors.append(f'{where}: unknown type "{t}"')
            # every question needs a difficulty for the CAT engine
            if q.get('difficulty') not in ('Easy', 'Moderate', 'Hard'):
                errors.append(f'{where}: difficulty must be Easy | Moderate | Hard (needed for CAT)')
            if q.get('id') in seen:
                errors.append(f'{where}: duplicate id (also in {seen[q["id"]]})')
            else:
                seen[q.get('id')] = name
            total += 1
            if q.get('free'):
                free += 1
            cats[q.get('cat', '?')] += 1

    print(f'Batches: {len(files)}   Questions: {total}   Free sample: {free}')
    print('By category:')
    for c, n in cats.most_common():
        print(f'  {n:3d}  {c}')
    if errors:
        print(f'\n❌ {len(errors)} validation error(s):')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('\n✅ All questions valid.')


if __name__ == '__main__':
    main()
