"""Nightfall: Twilight's construction with four decided parameters fitted from the thesis conversion of Dusk
(thesis repo commit aa39cf0, demo/twilight.js → variants.thesis.roles). Run: tools/.venv/bin/python tools/nightfall.py"""
import json
import math

import construct as k

# Twilight token -> thesis role (most role-specific match to the token's definition) -> hex
THESIS = dict(shell="#03070A", rail="#090F13", canvas="#11171B", raised="#1E2428", edge="#242A2F",   # bg_crust, bg_mantle, bg_base, bg_floating, border_subtle
              control="#646B70", faint="#7A8086", subtle="#BAC0C7", body="#D0D6DD",                     # bg_overlay0, text_subtle, text_subtext1, text_body
              seed="#F9A36B")                                                                           # accent_primary


def fit():
    hn = k.oklch_of(THESIS["seed"])[2] + 180
    pts = [k.oklch_of(THESIS[t]) for t in ("shell", "rail", "canvas", "raised", "edge", "control", "faint", "subtle", "body")]
    x = [math.sin(math.pi * L) ** 2 for L, _, _ in pts]
    amp = sum(a * C for a, (_, C, _) in zip(x, pts)) / sum(a * a for a in x)                 # C = A·sin²(πL)
    u = [(1 - L) ** 2 for L, _, _ in pts]
    v = [((h - hn + 180) % 360) - 180 for _, _, h in pts]
    drift = max(0.0, sum(a * b for a, b in zip(u, v)) / sum(a * a for a in u))              # h = h_n + D·(1−L)², D ≥ 0
    Lc = k.oklch_of(THESIS["canvas"])[0]
    steps = {"shell": -1, "raised": 1, "edge": 2}                                           # §3.3 geometric, anchored at Canvas
    lnr = sum(s * math.log(k.oklch_of(THESIS[t])[0] / Lc) for t, s in steps.items()) / sum(s * s for s in steps.values())
    return dict(amp=amp, drift=drift, r=math.exp(lnr))


# Rounded to the precision of Dusk's own decided parameters (0.035, 18°, 1.25).
NIGHTFALL = dict(k.DUSK, seed="#f9a36b", amp=0.018, drift=8.0, r=1.26)


def main():
    path = k.ROOT / "palette" / "twilight.json"
    data = json.loads(path.read_text())
    dusk = data["flavors"]["dusk"]                                                           # published Dusk, read before adding nightfall
    data["version"] = "1.2.0-preview"
    data["flavors"]["nightfall"] = nf = k.build(NIGHTFALL, *k.inherited(dusk))
    path.write_text(json.dumps(data, indent=2))                                              # the file has no trailing newline
    print("fit", {a: round(b, 4) for a, b in fit().items()}, "→ wrote flavors.nightfall")
    print(f"distinctness: dusk {k.distinctness(dusk):.4f}, nightfall {k.distinctness(nf):.4f}")


if __name__ == "__main__":
    main()
