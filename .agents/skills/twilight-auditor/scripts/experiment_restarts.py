"""Experiment: does the §6.5 optimizer converge, and does the result vary smoothly with β?

Not part of the audit. It rebuilds Dusk and Dawn over a grid of β values with 10, 40 and 80 restarts,
under two objectives, and reports convergence and smoothness. Nothing in the repository is changed.

Objectives
  A  current §6.5: min ΔE over the seven hue colors × four visions, minus the Ember–seed penalty.
  B  proposed: the same pairs plus the cursor (Afterglow's accent-focus), which is the set the
     guarantee measures, minus 2 × the shortfall of the normal-vision minimum below 4 JND (0.08).

Success (decided before running)
  converged  for at least 90 % of β values, 40 and 80 restarts give the same palette, or scores
             within 0.0005.
  smooth     at 80 restarts, the largest jump between neighboring β values (step 0.01) is at most
             0.005 in normal-vision ΔE and 0.003 in color-vision ΔE (code colors + cursor).

Usage (from the repository root, with the auditor's venv):
  python .agents/skills/twilight-auditor/scripts/experiment_restarts.py --workers 14
  python .agents/skills/twilight-auditor/scripts/experiment_restarts.py --quick          # β step 0.02
  python .agents/skills/twilight-auditor/scripts/experiment_restarts.py --summary-only   # re-print the summary

Results are appended to experiment_restarts.jsonl (resumable: finished runs are skipped).
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

NORMAL_MIN = 4 * 0.02          # 4 JND, the selection target of construction.md §9.1
RESTARTS = (10, 40, 80)
OBJECTIVES = ("A", "B")


def grid(quick):
    step = 2 if quick else 1
    dusk = [round(0.24 + 0.01 * i, 2) for i in range(0, 15, step)]   # 0.24–0.38
    dawn = [round(0.15 + 0.01 * i, 2) for i in range(0, 21, step)]   # 0.15–0.35
    return [("dusk", b) for b in dusk] + [("dawn", b) for b in dawn]


def run(job):
    objective, restarts, flavor, beta = job
    import construct as k
    import validate as v
    t0 = time.time()
    P = k.PROFILES[flavor]
    P["beta"] = beta
    k.OPT_RESTARTS = restarts
    dusk = k.dusk_neutrals()
    N = dusk if flavor == "dusk" else k.dawn_neutrals(dusk)
    cursor = k.family(N, k.SEED, P)["accent-focus"]
    if not hasattr(k, "_distinctness_a"):                 # workers are reused: keep objective A from the first import
        k._distinctness_a = k.distinctness
    original = k._distinctness_a

    def objective_b(cols):
        vals = list(cols.values()) + [cursor]
        pairs = [(a, b) for i, a in enumerate(vals) for b in vals[i + 1:]]
        normal = min(k.de_ok(a, b) for a, b in pairs)
        worst = min(k.sim(a, vis).delta_e(k.sim(b, vis), method="ok") for vis in k.VISIONS for a, b in pairs)
        penalty = 2 * max(0.0, k.EMBER_VS_SEED - k.de_ok(cols["ember"], k.SEED)) + 2 * max(0.0, NORMAL_MIN - normal)
        return worst - penalty

    k.distinctness = original if objective == "A" else objective_b
    F, meta, _ = k.build_flavor(flavor, dusk)
    m, lim, _ = v.measure(F)
    i = 0 if flavor == "dusk" else 1
    inv = {slot: name for name, slot in k.COLOR_KEYS.items()}
    cols = {slot: F["colors"][inv[slot]] for slot in k.SIX}
    cols["ember"] = F["colors"]["ember"]
    return dict(objective=objective, restarts=restarts, flavor=flavor, beta=beta,
                score=k.distinctness(cols), normal=m["ΔE code+cursor, normal"], cvd=m["ΔE code+cursor, worst CVD"],
                floors_failed=[c for c in v.FLOORS if not v.passes(m[c], v.FLOORS[c][i])],
                limits=lim, colors=F["colors"], seconds=round(time.time() - t0, 1))


def key(r):
    return (r["objective"], r["restarts"], r["flavor"], r["beta"])


def summary(results):
    by = {key(r): r for r in results}
    current = {"dusk": 0.30, "dawn": 0.19}
    print("\n" + "=" * 78 + "\nSUMMARY (paste everything below this line)\n" + "=" * 78)
    verdicts = {}
    for obj in OBJECTIVES:
        for flavor in ("dusk", "dawn"):
            betas = sorted({b for (o, _, f, b) in by if o == obj and f == flavor})
            if not betas:
                continue
            print(f"\nObjective {obj} · {flavor}   (normal / CVD, code colors + cursor; * = a floor fails)")
            print("  β     " + "".join(f"{f'R={r}':>18}" for r in RESTARTS))
            for b in betas:
                cells = []
                for r in RESTARTS:
                    x = by.get((obj, r, flavor, b))
                    cells.append(f"{x['normal']:.4f}/{x['cvd']:.4f}{'*' if x['floors_failed'] else ' '}" if x else "—")
                print(f"  {b:.2f}  " + "".join(f"{c:>18}" for c in cells))
            same = [b for b in betas if (x := by.get((obj, 40, flavor, b))) and (y := by.get((obj, 80, flavor, b)))
                    and (x["colors"] == y["colors"] or abs(x["score"] - y["score"]) <= 0.0005)]
            both = [b for b in betas if (obj, 40, flavor, b) in by and (obj, 80, flavor, b) in by]
            row = [by[(obj, 80, flavor, b)] for b in betas if (obj, 80, flavor, b) in by]
            jn = max((abs(a["normal"] - c["normal"]) for a, c in zip(row, row[1:])), default=math.nan)
            jc = max((abs(a["cvd"] - c["cvd"]) for a, c in zip(row, row[1:])), default=math.nan)
            step = round(row[1]["beta"] - row[0]["beta"], 2) if len(row) > 1 else 0
            conv = len(same) / len(both) if both else math.nan
            ok = conv >= 0.9 and jn <= 0.005 * step / 0.01 and jc <= 0.003 * step / 0.01
            verdicts[(obj, flavor)] = ok
            print(f"  converged (R40 = R80): {len(same)}/{len(both)}   largest neighbor jump at R=80: "
                  f"normal {jn:.4f}, CVD {jc:.4f} (β step {step})   → {'SUCCESS' if ok else 'not met'}")
            ok_rows = [x for x in row if not x["floors_failed"]]
            if ok_rows:
                best = max(ok_rows, key=lambda x: (x["normal"], x["cvd"]))
                cur = by.get((obj, 80, flavor, current[flavor]))
                print(f"  best at R=80 (all floors pass, max normal): β {best['beta']:.2f}  "
                      f"normal {best['normal']:.4f}  CVD {best['cvd']:.4f}")
                if cur:
                    print(f"  current β {current[flavor]:.2f} at R=80:                    "
                          f"normal {cur['normal']:.4f}  CVD {cur['cvd']:.4f}")
    secs = [r["seconds"] for r in results]
    print(f"\nruns: {len(results)}   mean seconds per run: {sum(secs) / max(len(secs), 1):.0f}")
    print("verdicts:", {f"{o}/{f}": ("SUCCESS" if v else "not met") for (o, f), v in verdicts.items()})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--out", default="experiment_restarts.jsonl")
    ap.add_argument("--quick", action="store_true", help="β step 0.02 instead of 0.01")
    ap.add_argument("--summary-only", action="store_true")
    a = ap.parse_args()
    results = [json.loads(line) for line in open(a.out, encoding="utf-8")] if os.path.exists(a.out) else []
    if not a.summary_only:
        done = {key(r) for r in results}
        jobs = [(o, r, f, b) for o in OBJECTIVES for (f, b) in grid(a.quick) for r in RESTARTS]
        jobs = [j for j in jobs if j not in done]
        jobs.sort(key=lambda j: -j[1])                       # longest first, for an even finish
        print(f"{len(jobs)} runs to do on {a.workers} workers ({len(done)} already done)", flush=True)
        t0 = time.time()
        with mp.Pool(a.workers) as pool, open(a.out, "a", encoding="utf-8") as out:
            for n, r in enumerate(pool.imap_unordered(run, jobs), 1):
                results.append(r)
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
                out.flush()
                eta = (time.time() - t0) / n * (len(jobs) - n) / 60
                print(f"[{n}/{len(jobs)}] {r['objective']} R={r['restarts']:<3} {r['flavor']} β {r['beta']:.2f}  "
                      f"normal {r['normal']:.4f} CVD {r['cvd']:.4f}  {r['seconds']:.0f}s  ~{eta:.0f} min left", flush=True)
    summary(results)


if __name__ == "__main__":
    main()
