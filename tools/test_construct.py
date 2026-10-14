"""Construction must rebuild Dusk from its decided parameters. Run: tools/.venv/bin/python tools/test_construct.py"""
import json
from pathlib import Path

import construct as k

PUB = json.loads((Path(__file__).resolve().parent.parent / "palette" / "twilight.json").read_text())["flavors"]["dusk"]


def tokens(f):
    out = {f"neutrals.{n}": v for n, v in f["neutrals"].items()}
    out |= {f"colors.{n}": v for n, v in f["colors"].items()}
    out |= {f"accents.{a}.{t}": v for a, d in f["accents"].items() for t, v in d.items() if t != "_check"}
    out |= {f"states.{n}": v for n, v in f["states"].items()}
    out |= {f"ansi.{i}": v for i, v in enumerate(f["ansi"])}
    return out


def mismatches(built, pub=PUB):
    b, p = tokens(built), tokens(pub)
    assert b.keys() == p.keys(), b.keys() ^ p.keys()
    return {t: (p[t], b[t], round(k.de_ok(p[t], b[t]), 4)) for t in p if p[t].lower() != b[t].lower()}


def check_nightfall():
    import nightfall as nf
    raw = nf.fit()
    assert abs(raw["amp"] - 0.0182) < 0.0005 and abs(raw["drift"] - 8.42) < 0.3 and abs(raw["r"] - 1.2645) < 0.003, raw
    assert (nf.NIGHTFALL["amp"], nf.NIGHTFALL["drift"], nf.NIGHTFALL["r"], nf.NIGHTFALL["seed"]) == (0.018, 8.0, 1.26, "#f9a36b")
    same = lambda p: {a: b for a, b in p.items() if a not in ("seed", "amp", "drift", "r")}
    assert same(nf.NIGHTFALL) == same(k.DUSK)                                       # only the four fitted parameters differ
    f = json.loads((Path(__file__).resolve().parent.parent / "palette" / "twilight.json").read_text())["flavors"]["nightfall"]
    n, c, s = f["neutrals"], f["colors"], f["states"]
    surf = [n[x] for x in ("shell", "rail", "canvas", "raised")]
    for lvl, tgt in dict(faint=4.5, subtle=7.0, body=10.9, control=3.0).items():   # §13 text and control levels
        assert min(k.contrast(n[lvl], x) for x in surf) >= tgt - 0.005, lvl
    code = [n["canvas"], s["diff-inserted"], s["diff-removed"]]
    assert min(k.contrast(c[x], y) for x in c if x != "afterglow" for y in code) >= 7.0 - 0.005    # §6.6 floor
    for a in f["accents"].values():                                                                  # §5
        assert min(k.contrast(a["accent-focus"], x) for x in surf) >= 3.0 - 0.005
        assert k.contrast(a["on-accent"], a["accent"]) >= 4.5 and k.contrast(a["accent-text"], n["raised"]) >= 7.0 - 0.005
    for st in ("selection", "selection-inactive", "find-match", "find-match-other", "word-highlight", "word-highlight-write"):
        assert k.contrast(n["faint"], s[st]) >= 4.5 - 0.005, st                                       # §9.2
    allhex = [*n.values(), *c.values(), *s.values(), *f["ansi"], *(v for a in f["accents"].values() for t, v in a.items() if t != "_check")]
    assert not {"#000000", "#ffffff"} & {h.lower() for h in allhex}
    assert k.de_ok(c["ember"], c["afterglow"]) >= 0.06
    print("Nightfall guarantees hold")


if __name__ == "__main__":
    bad = mismatches(k.build(k.DUSK, *k.inherited(PUB)))
    neutral_bad = {t: v for t, v in bad.items() if t.startswith("neutrals.")}
    # User decision (Round A): states may differ by ≤ ΔE_OK 0.0065 (documented Euclidean cost, chroma up to
    # Cmax at Canvas L); everything else ≤ 0.005.
    far = {t: v for t, v in bad.items() if v[2] > (0.0065 if t.startswith("states.") else 0.005)}
    for t, v in sorted(bad.items()):
        print(t, v)
    assert not neutral_bad, neutral_bad          # neutrals are deterministic: exact
    assert not far, far                          # states ≤ 0.0065, everything else ≤ 0.005
    print(f"Dusk reproduced: {len(tokens(PUB))} tokens, {len(bad)} differ within tolerance; distinctness {k.distinctness(k.build(k.DUSK, *k.inherited(PUB))):.4f}")
    check_nightfall()
