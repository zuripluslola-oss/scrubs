#!/usr/bin/env python3
"""One-time migration: parse content/nclex-complete-workbook.md into question-bank
batch files under data/qbank/, grouped by category. Handles standard 4-option MC
questions; non-MC formats (SATA, bow-tie) are skipped and reported for later.
"""
import os, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'content', 'nclex-complete-workbook.md')
OUT = os.path.join(ROOT, 'data', 'qbank')

CATMAP = {
    'Pharmacology': 'Pharmacology', 'Pharmacology / Safety': 'Pharmacology',
    'Pharmacology / Mental Health': 'Mental Health', 'Pharmacology / Maternity': 'Maternal / Newborn',
    'Pharmacology / Cardiac': 'Pharmacology', 'Pharmacology / Respiratory': 'Pharmacology',
    'Adult Health / Respiratory': 'Med-Surg', 'Adult Health / Neuro': 'Med-Surg',
    'Adult Health / Perioperative': 'Med-Surg', 'Adult Health / Endocrine': 'Med-Surg',
    'Adult Health / Renal': 'Med-Surg', 'Adult Health / GI': 'Med-Surg', 'Adult Health / Cardiac': 'Med-Surg',
    'Maternity': 'Maternal / Newborn', 'Maternity / Intrapartum': 'Maternal / Newborn',
    'Maternity / Postpartum': 'Maternal / Newborn', 'Maternity / Pharmacology': 'Maternal / Newborn',
    'Newborn': 'Maternal / Newborn',
    'Pediatrics': 'Pediatrics', 'Pediatrics / Respiratory': 'Pediatrics',
    'Pediatrics / Fluid & Electrolyte': 'Pediatrics', 'Pediatrics / GI': 'Pediatrics',
    'Pediatrics / Cardiac': 'Pediatrics', 'Pediatrics / Health Promotion': 'Pediatrics',
    'Mental Health': 'Mental Health', 'Mental Health / Physiological': 'Mental Health',
    'Mental Health / Pharmacology': 'Mental Health',
    'Fundamentals': 'Fundamentals', 'Fundamentals / Infection Control': 'Fundamentals',
    'Fundamentals / Safety': 'Fundamentals', 'Fundamentals / Management': 'Fundamentals',
    'Clinical Judgment': 'Clinical Judgment', 'Clinical Judgment / Prioritization': 'Safety',
    'Clinical Judgment / Fluid & Electrolyte': 'Med-Surg', 'Clinical Judgment / Cardiac': 'Med-Surg',
    'Clinical Judgment / Emergency': 'Safety',
    'Safety': 'Safety', 'Safety / Pharmacology': 'Safety', 'Safety / Management': 'Safety',
    'Safety / Infection Control': 'Fundamentals',
}
SLUG = {'Pharmacology': 'pharmacology', 'Med-Surg': 'med-surg', 'Maternal / Newborn': 'maternal-newborn',
        'Pediatrics': 'pediatrics', 'Mental Health': 'mental-health', 'Fundamentals': 'fundamentals',
        'Safety': 'safety', 'Clinical Judgment': 'clinical-judgment'}


def clean(t):
    return re.sub(r'\s+', ' ', t).strip()


def collect(lines, i):
    """Join wrapped text lines starting at i until a blank line or a new marker."""
    buf = []
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == '' or ln.startswith('- ') or ln.startswith('**') or ln.startswith('###') or ln.startswith('🎨'):
            break
        buf.append(ln.strip()); i += 1
    return ' '.join(buf), i


def parse_block(block):
    lines = block.split('\n')
    title = clean(re.sub(r'^###\s*Question\s*\d+\s*[—-]\s*', '', lines[0]))
    cat_raw, difficulty = '', ''
    stem_scenario, stem_q = '', ''
    opts, rats = {}, {}
    correct_letter, tip, pearl = '', '', ''

    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith('**Category:**'):
            parts = s.split('·')
            cat_raw = clean(parts[0].replace('**Category:**', ''))
            for p in parts:
                if 'Difficulty' in p:
                    difficulty = clean(p.split('**Difficulty:**')[-1])
            i += 1; continue
        if s.startswith('**Scenario.**'):
            first = s.replace('**Scenario.**', '').strip()
            rest, i = collect(lines, i + 1)
            stem_scenario = clean((first + ' ' + rest))
            continue
        m = re.match(r'^- \*\*([A-E])\.\*\*\s*(.*)', s)
        if m and not stem_q == '' or (m and stem_q == ''):
            # option line (only A-D expected for MC)
            letter, txt = m.group(1), m.group(2)
            more, i = collect(lines, i + 1)
            opts[letter] = clean(txt + ' ' + more)
            continue
        mr = re.match(r'^- \*\*([A-E])\s*[—-]\s*[^*]*\*\*\s*(.*)', s)
        if mr:
            letter, txt = mr.group(1), mr.group(2)
            more, i = collect(lines, i + 1)
            # strip a leading "Correct." / "Incorrect." / "(this ...)."
            rt = clean(txt + ' ' + more)
            rt = re.sub(r'^\(this[^)]*\)\.?\s*', '', rt, flags=re.I)
            rats[letter] = rt
            continue
        if s.startswith('**✅ Correct answer'):
            cm = re.search(r'Correct answers?:\s*([A-E])', s)
            if cm:
                correct_letter = cm.group(1)
            i += 1; continue
        if '**Which' in s or (s.startswith('**') and s.rstrip().endswith('?**')):
            stem_q = clean(re.sub(r'\*\*', '', s))
            i += 1; continue
        if 'NCLEX Tip' in s:
            first = clean(re.sub(r'.*NCLEX Tip\.\*\*', '', s))
            rest, i = collect(lines, i + 1)
            tip = clean(first + ' ' + rest)
            continue
        if 'Clinical Pearl' in s or 'Memory Trick' in s:
            first = clean(re.sub(r'.*Trick\.\*\*', '', s))
            rest, i = collect(lines, i + 1)
            pearl = clean(first + ' ' + rest)
            continue
        i += 1

    # must be a clean 4-option MC with a single correct letter
    letters = ['A', 'B', 'C', 'D']
    if sorted(opts.keys()) != letters:
        return None, 'non-MC (options ' + ''.join(sorted(opts.keys())) + ')'
    if correct_letter not in letters:
        return None, 'no single correct letter'
    if any(l not in rats for l in letters):
        return None, 'missing rationale'

    stem = clean(stem_scenario + (' ' + stem_q if stem_q else ''))
    cat = CATMAP.get(cat_raw, 'Clinical Judgment')
    q = {
        'exam': 'RN', 'cat': cat, 'topic': title, 'difficulty': difficulty or 'Moderate',
        'type': 'mc', 'stem': stem,
        'opts': [{'t': opts[l], 'r': rats[l]} for l in letters],
        'correct': letters.index(correct_letter),
        'tip': tip, 'pearl': pearl,
    }
    return q, None


def main():
    md = open(SRC, encoding='utf-8').read()
    blocks = re.split(r'(?=^###\s*Question\s*\d+)', md, flags=re.M)
    blocks = [b for b in blocks if b.strip().startswith('### Question')]
    by_cat = collections.OrderedDict()
    skipped = []
    n = 0
    for b in blocks:
        q, why = parse_block(b)
        if q is None:
            skipped.append((b.split('\n')[0].strip(), why)); continue
        by_cat.setdefault(q['cat'], []).append(q)
        n += 1

    # assign ids + free flags (first 2 per category free) and write batch files
    written = 0
    for cat, qs in by_cat.items():
        slug = SLUG.get(cat, re.sub(r'[^a-z]+', '-', cat.lower()))
        for j, q in enumerate(qs):
            q_id = f"{slug}-{j+1:04d}"
            q_final = {'id': q_id, **q, 'free': j < 2}
            qs[j] = q_final
        path = os.path.join(OUT, f'workbook-{slug}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'batch': f'workbook-{slug}', 'questions': qs}, f, ensure_ascii=False, indent=2)
        written += len(qs)
        print(f'  wrote {len(qs):2d} → {os.path.basename(path)}')

    print(f'\nImported {written} MC questions across {len(by_cat)} categories.')
    if skipped:
        print(f'Skipped {len(skipped)} (need non-MC support):')
        for t, why in skipped:
            print(f'  - {t}  [{why}]')


if __name__ == '__main__':
    main()
