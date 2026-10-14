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
