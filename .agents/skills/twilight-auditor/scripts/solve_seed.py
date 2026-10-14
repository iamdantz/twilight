"""Solve Dawn's seed (construction.md §2): the orange that gives Dawn the best code-color distinctness.

Search space (decided):
- orange = sRGB (HSV) hue in [15°, 45°], the middle half between pure red (0°) and pure yellow (60°);
- stage 1, OKLCH grid: L 0.60–0.80 step 0.05, C 0.14–0.22 step 0.02, h 35°–70° step 5°;
- stage 2, refinement where stage 1 traded color-vision against normal-vision separation best:
  L {0.72, 0.75, 0.78}, C {0.150, 0.155, 0.160}, h {45°, 48°, 51°, 54°};
- each grid point is converted to 8-bit hex; points outside sRGB or outside the orange band are skipped.

Each candidate builds the whole Dawn flavor with the unchanged method (construct.build_flavor).

Rule. Two kinds of measurement:
- solved to a threshold (text levels, accent tokens, code floor, Faint on states, every state that
  reaches its JND target): the candidate must meet the threshold. The margin above it is 8-bit rounding.
- quality (code-color separation in normal vision and the worst dichromacy, the states 1.1.1 could not
  bring to target, the closest pair of states, ANSI black/white): the candidate must match or beat Dawn 1.1.1.
Ink on surfaces depends only on the neutrals, not on the seed, and is not part of the rule.
Among the candidates that pass, the highest worst-case color-vision ΔE wins (ties: the smaller ΔE_OK
from Dusk's Afterglow).

Usage: python solve_seed.py [--workers N] [--out results.json]
       (about 70 s per candidate per core; an existing --out file is resumed)
"""
import argparse
import json
import multiprocessing as mp
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import construct as k  # noqa: E402

# Dawn 1.1.1, measured with validate.measure (unrounded): the values to match or beat.
BASELINE = {
    "body on surfaces": 10.88903, "subtle on surfaces": 7.00200, "faint on surfaces": 4.50507,
    "control on surfaces": 3.02148, "code on code surfaces": 4.50114, "on-accent on accent/pressed": 4.50583,
    "accent-text on raised": 4.51207, "accent-focus on surfaces": 3.00471, "ΔE code+cursor, normal": 0.07699,
    "ΔE code+cursor, worst CVD": 0.04113, "faint on transient states": 4.50658,
    "JND selection": 2.21934, "JND selection-inactive": 2.03311, "JND find-match": 3.04668,
    "JND find-match-other": 2.50060, "JND word-highlight": 2.03153, "JND word-highlight-write": 2.32052,
    "JND diff-inserted": 2.06211, "JND diff-removed": 2.02476, "ANSI black/white on canvas": 1.39578,
    "min ΔE between background states": 0.00444,
}


STAGE1 = [(L / 100, C / 100, h) for L in range(60, 81, 5) for C in range(14, 23, 2) for h in range(35, 71, 5)]
STAGE2 = [(L, C, h) for L in (0.72, 0.75, 0.78) for C in (0.150, 0.155, 0.160) for h in (45, 48, 51, 54)]
QUALITY = ("ΔE code+cursor, worst CVD", "ΔE code+cursor, normal", "JND selection", "JND find-match",
           "JND word-highlight-write", "min ΔE between background states", "ANSI black/white on canvas")
THRESHOLDS = {"body on surfaces": 49 / 4.5, "subtle on surfaces": 7.0, "faint on surfaces": 4.5, "control on surfaces": 3.0,
              "code on code surfaces": 4.5, "on-accent on accent/pressed": 4.5, "accent-text on raised": 4.5,
              "accent-focus on surfaces": 3.0, "faint on transient states": 4.5,
              **{f"JND {x}": t for x, t in k.STATE_JND.items() if f"JND {x}" not in QUALITY}}


def candidates():
    from coloraide import Color
    out, seen = [], set()
    for L, C, h in STAGE1 + STAGE2:
        c = Color("oklch", [L, C, h])
        if not c.in_gamut("srgb"):
            continue
        hx = c.convert("srgb").to_string(hex=True)
        if 15 <= Color(hx).convert("hsv")["hue"] <= 45 and hx not in seen:
            seen.add(hx)
            out.append(hx)
    return out


def evaluate(seed):
    import validate as v
    k.PROFILES["dawn"]["seed"] = seed
    F, meta, _ = k.build_flavor("dawn", k.dusk_neutrals())
    m, lim, _ = v.measure(F)
    vals = {**m, **lim}
    fails = [x for x, t in THRESHOLDS.items() if vals[x] < t] + [x for x in QUALITY if vals[x] < BASELINE[x] - 1e-9]
    return dict(seed=seed, meta=meta, values=vals, fails=fails, palette=F)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", default="seed_results.json")
    a = ap.parse_args()
    cands = candidates()
    results = json.load(open(a.out)) if os.path.exists(a.out) else []
    done = {r["seed"] for r in results}
    todo = [c for c in cands if c not in done]
    print(f"{len(cands)} orange candidates, {len(todo)} to build", flush=True)
    with mp.Pool(a.workers) as pool:
        for r in pool.imap_unordered(evaluate, todo):
            results.append(r)
            print(f"{r['seed']}  cvd {r['values']['ΔE code+cursor, worst CVD']:.5f}  fails: {r['fails']}", flush=True)
            json.dump(results, open(a.out, "w"))
    for r in results:   # re-apply the rule to resumed results
        v = r["values"]
        r["fails"] = [x for x, t in THRESHOLDS.items() if v[x] < t] + [x for x in QUALITY if v[x] < BASELINE[x] - 1e-9]
    ok = [r for r in results if not r["fails"]]
    dusk = k.PROFILES["dusk"]["seed"]
    pick = max(ok, key=lambda r: (round(r["values"]["ΔE code+cursor, worst CVD"], 6), -k.de_ok(r["seed"], dusk))) if ok else None
    print("winner:", pick["seed"] if pick else "none meets the rule")


if __name__ == "__main__":
    main()
