#!/usr/bin/env python3
"""Validate + summarize the question-bank batches in data/qbank/.

Run this after adding or editing a batch file. It checks every question against
the schema, reports duplicates and errors, and prints per-category counts.
The site build (tools/build_pages.py) uses the same rules to assemble the bank.
"""
import os, glob, json, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(ROOT, 'data', 'qbank')

REQUIRED = ['id', 'exam', 'cat', 'type', 'stem', 'opts', 'correct']


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
            if q.get('type', 'mc') == 'mc':
                if len(q.get('opts', [])) != 4:
                    errors.append(f'{where}: MC needs exactly 4 options')
                for o in q.get('opts', []):
                    if 't' not in o or 'r' not in o:
                        errors.append(f'{where}: an option is missing text or rationale')
                if not (0 <= q.get('correct', -1) <= 3):
                    errors.append(f'{where}: correct index out of range')
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
