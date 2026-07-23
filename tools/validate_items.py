#!/usr/bin/env python3
"""MLSCLEX item validator — checks any question JSON against the canonical
NCLEX item-type spec (data/qbank/item-types.md).

Usage:
  python3 tools/validate_items.py path/to/file.json     # one file
  python3 tools/validate_items.py --all                 # every data/qbank/*.json
  python3 tools/validate_items.py --coverage file.json  # + which of the 21 types are present

Accepts either {"questions":[...]} / {"drugs":...} batch files or a raw [ ... ]
array (e.g. straight from ChatGPT). Reports errors (blockers) and warnings, plus
a per-type coverage summary. Exit code 1 if any errors.
"""
import sys, os, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANONICAL_TYPES = [
    "mc", "sata", "select_n", "grouping", "fill_blank", "ordered", "hotspot",
    "exhibit", "graphic", "audio", "table", "bowtie", "trend", "matrix",
    "matrix_mr", "dropdown_table", "dropdown_cloze", "dropdown_rationale",
    "highlight_text", "highlight_table", "casestudy",
]
DIFFICULTIES = {"Easy", "Moderate", "Hard"}
CLIENT_NEEDS = {
    "Management of Care", "Safety and Infection Control",
    "Health Promotion and Maintenance", "Psychosocial Integrity",
    "Basic Care and Comfort", "Pharmacological and Parenteral Therapies",
    "Reduction of Risk Potential", "Physiological Adaptation",
}

def opt_ok(errs, where, opt):
    if not isinstance(opt, dict) or not opt.get("t") or not str(opt.get("t")).strip():
        errs.append(f"{where}: option missing text 't'")
    if not isinstance(opt, dict) or not opt.get("r") or not str(opt.get("r")).strip():
        errs.append(f"{where}: option missing rationale 'r'  ← every option needs one")

def check_opts(errs, where, opts, n=None, mn=None):
    if not isinstance(opts, list) or not opts:
        errs.append(f"{where}: 'opts' must be a non-empty list"); return
    if n is not None and len(opts) != n:
        errs.append(f"{where}: expected {n} options, got {len(opts)}")
    if mn is not None and len(opts) < mn:
        errs.append(f"{where}: expected at least {mn} options, got {len(opts)}")
    for o in opts:
        opt_ok(errs, where, o)

def idx_ok(errs, where, val, opts, field="correct"):
    if not isinstance(val, int) or not (0 <= val < len(opts)):
        errs.append(f"{where}: '{field}' index {val!r} out of range 0..{len(opts)-1}")

def idxlist_ok(errs, where, vals, opts, field="correct", pick=None):
    if not isinstance(vals, list) or not vals:
        errs.append(f"{where}: '{field}' must be a non-empty list of indices"); return
    for v in vals:
        if not isinstance(v, int) or not (0 <= v < len(opts)):
            errs.append(f"{where}: '{field}' index {v!r} out of range")
    if pick is not None and len(vals) != pick:
        errs.append(f"{where}: '{field}' should have {pick} correct (pick), got {len(vals)}")

def check_item(item, where):
    """Return (errors, warnings) for a single item dict."""
    errs, warns = [], []
    for f in ("id", "exam", "cat", "type", "stem"):
        if not item.get(f):
            errs.append(f"{where}: missing required field '{f}'")
    t = item.get("type", "?")
    if t not in CANONICAL_TYPES:
        errs.append(f"{where}: unknown type '{t}' (see data/qbank/item-types.md)")
    if item.get("difficulty") not in DIFFICULTIES:
        errs.append(f"{where}: difficulty must be Easy/Moderate/Hard, got {item.get('difficulty')!r}")
    lvl = item.get("level")
    if lvl is not None and (not isinstance(lvl, int) or not (1 <= lvl <= 5)):
        warns.append(f"{where}: level should be an int 1–5")
    cn = item.get("client_needs")
    if cn and cn not in CLIENT_NEEDS:
        warns.append(f"{where}: client_needs '{cn}' not a standard Client Needs category")
    media_types = {"hotspot", "graphic", "audio", "trend", "exhibit", "table"}
    if t in media_types and not item.get("media"):
        warns.append(f"{where}: type '{t}' usually needs a 'media' description")

    # ---- per-type structure ----
    if t == "mc":
        check_opts(errs, where, item.get("opts"), n=4); idx_ok(errs, where, item.get("correct"), item.get("opts") or [])
    elif t in ("sata", "grouping"):
        check_opts(errs, where, item.get("opts"), mn=3)
        if t == "sata": idxlist_ok(errs, where, item.get("correct"), item.get("opts") or [])
    elif t == "select_n":
        check_opts(errs, where, item.get("opts"), mn=3)
        idxlist_ok(errs, where, item.get("correct"), item.get("opts") or [], pick=item.get("pick"))
        if not isinstance(item.get("pick"), int): errs.append(f"{where}: select_n needs integer 'pick'")
    elif t == "fill_blank":
        a = item.get("answer") or {}
        if "value" not in a: errs.append(f"{where}: fill_blank needs answer.value")
        if not item.get("r") and not a.get("r"): warns.append(f"{where}: fill_blank should show the math in 'r'")
    elif t == "ordered":
        check_opts(errs, where, item.get("items"), mn=3)
    elif t == "hotspot":
        rs = item.get("regions") or []
        if not rs: errs.append(f"{where}: hotspot needs 'regions'")
        if not any(r.get("correct") for r in rs): errs.append(f"{where}: hotspot has no correct region")
        for r in rs:
            if not r.get("r"): errs.append(f"{where}: hotspot region '{r.get('label')}' missing rationale")
    elif t in ("exhibit", "graphic", "audio", "table"):
        check_opts(errs, where, item.get("opts"), mn=2); idx_ok(errs, where, item.get("correct"), item.get("opts") or [])
    elif t == "bowtie":
        for grp, pick in (("actions", 2), ("condition", None), ("parameters", 2)):
            g = item.get(grp) or {}
            check_opts(errs, where + f".{grp}", g.get("options"), mn=2)
            if pick is None: idx_ok(errs, where + f".{grp}", g.get("correct"), g.get("options") or [])
            else: idxlist_ok(errs, where + f".{grp}", g.get("correct"), g.get("options") or [], pick=g.get("pick", pick))
    elif t == "trend":
        if not item.get("timeline"): errs.append(f"{where}: trend needs a 'timeline'")
        check_opts(errs, where, item.get("opts"), mn=2); idx_ok(errs, where, item.get("correct"), item.get("opts") or [])
    elif t in ("matrix", "matrix_mr"):
        if not item.get("cols"): errs.append(f"{where}: {t} needs 'cols'")
        rows = item.get("rows") or []
        if not rows: errs.append(f"{where}: {t} needs 'rows'")
        for r in rows:
            if not r.get("r"): errs.append(f"{where}: {t} row '{r.get('t')}' missing rationale")
            if t == "matrix" and not isinstance(r.get("correct"), int):
                errs.append(f"{where}: matrix row '{r.get('t')}' correct must be an int")
            if t == "matrix_mr" and not isinstance(r.get("correct"), list):
                errs.append(f"{where}: matrix_mr row '{r.get('t')}' correct must be a list")
    elif t == "dropdown_table":
        for r in item.get("rows") or []:
            check_opts(errs, where, r.get("options"), mn=2); idx_ok(errs, where, r.get("correct"), r.get("options") or [])
    elif t in ("dropdown_cloze", "dropdown_rationale"):
        if not item.get("sentence"): errs.append(f"{where}: {t} needs a 'sentence' with {{0}} blanks")
        bs = item.get("blanks") or []
        if not bs: errs.append(f"{where}: {t} needs 'blanks'")
        for i, b in enumerate(bs):
            check_opts(errs, where + f".blank{i}", b.get("options"), mn=2); idx_ok(errs, where + f".blank{i}", b.get("correct"), b.get("options") or [])
    elif t == "highlight_text":
        segs = item.get("segments") or []
        if not segs: errs.append(f"{where}: highlight_text needs 'segments'")
        if not any(s.get("correct") for s in segs): errs.append(f"{where}: highlight_text has no correct segment")
        for s in segs:
            if not s.get("r"): warns.append(f"{where}: segment '{str(s.get('t'))[:20]}' missing rationale")
    elif t == "highlight_table":
        for r in item.get("rows") or []:
            for c in r.get("cells") or []:
                if not c.get("r"): warns.append(f"{where}: highlight_table cell missing rationale")
    elif t == "casestudy":
        if not item.get("scenario"): errs.append(f"{where}: casestudy needs 'scenario'")
        if not item.get("tabs"): warns.append(f"{where}: casestudy should have record 'tabs'")
        qs = item.get("questions") or []
        if len(qs) != 6:
            warns.append(f"{where}: casestudy has {len(qs)} questions (NGN unfolding cases have 6)")
        for i, q in enumerate(qs):
            e2, w2 = check_item(q, where + f".q{i+1}")
            errs += e2; warns += w2
    return errs, warns

def load_items(path):
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, list): return data
    if isinstance(data, dict):
        for key in ("questions", "items", "drugs", "cards"):
            if key in data: return data[key]
    raise ValueError("expected a list or a {questions:[...]} object")

def validate_files(paths, coverage=False):
    all_errs, all_warns, seen_ids, types_present = [], [], set(), set()
    total = 0
    for path in paths:
        try:
            items = load_items(path)
        except Exception as e:
            all_errs.append(f"{path}: could not parse ({e})"); continue
        for i, item in enumerate(items):
            total += 1
            where = f"{os.path.basename(path)}[{item.get('id', i)}]"
            iid = item.get("id")
            if iid in seen_ids: all_errs.append(f"{where}: duplicate id '{iid}'")
            if iid: seen_ids.add(iid)
            types_present.add(item.get("type"))
            e, w = check_item(item, where)
            all_errs += e; all_warns += w

    print(f"Checked {total} items across {len(paths)} file(s).\n")
    if all_errs:
        print(f"❌ {len(all_errs)} ERROR(S):")
        for e in all_errs[:200]: print("  -", e)
        if len(all_errs) > 200: print(f"  … and {len(all_errs)-200} more")
    else:
        print("✅ No errors.")
    if all_warns:
        print(f"\n⚠️  {len(all_warns)} warning(s):")
        for w in all_warns[:60]: print("  -", w)
        if len(all_warns) > 60: print(f"  … and {len(all_warns)-60} more")
    if coverage:
        print("\n— Item-type coverage —")
        for t in CANONICAL_TYPES:
            print(f"  {'✓' if t in types_present else '·'} {t}")
        missing = [t for t in CANONICAL_TYPES if t not in types_present]
        if missing: print("  MISSING:", ", ".join(missing))
    return 0 if not all_errs else 1

if __name__ == "__main__":
    args = sys.argv[1:]
    coverage = "--coverage" in args
    args = [a for a in args if a != "--coverage"]
    if "--all" in args:
        paths = sorted(glob.glob(os.path.join(ROOT, "data", "qbank", "*.json")))
    elif args:
        paths = args
    else:
        print(__doc__); sys.exit(2)
    sys.exit(validate_files(paths, coverage=coverage))
