"""Twilight construction (docs/construction.md) for a dark flavor, from its decided parameters (§12).

Hue angles and Ember are inherited from Dusk (the published optimizer's random starts are not documented, so §6.5 cannot be re-run reproducibly).
"""
import json
import math
from functools import lru_cache
from pathlib import Path

from coloraide import Color

ROOT = Path(__file__).resolve().parent.parent
PHI = (1 + 5 ** 0.5) / 2
CORNERS = dict(coral="#ff0000", gold="#ffff00", grove="#00ff00", sea_salt="#00ffff", sky="#0000ff", orchid="#ff00ff")  # §6.1
SIX = list(CORNERS)
DUSK = dict(seed="#ee7a1f", drift=18.0, amp=0.035, r=1.25, canvas=0.20, ink=0.95, tau=0.15, beta=0.30,
            freedom=25.0, ember_h=(45.0, 70.0), ember_L=(0.60, 0.90), ember_vs_seed=0.06, floor=7.0,
            targets=dict(control=3.0, faint=4.5, subtle=7.0, body=10.9), gamut=0.92,
            jnd=dict(selection=4, **{"selection-inactive": 2}, **{"find-match": 5}, **{"find-match-other": 2.5},
                     **{"word-highlight": 2}, **{"word-highlight-write": 3}, **{"diff-inserted": 2}, **{"diff-removed": 2}))
STATE_HUE = {"selection": "seed", "selection-inactive": "seed", "find-match": "gold", "find-match-other": "gold",
             "word-highlight": "sea_salt", "word-highlight-write": "sea_salt", "diff-inserted": "grove", "diff-removed": "coral"}
VISIONS = (None, "protan", "deutan", "tritan")


def oklch_of(hx):
    L, C, h = Color(hx).convert("oklch").coords(nans=False)
    return L, C, h % 360


@lru_cache(maxsize=None)
def cmax(L, h):
    """Largest in-gamut chroma at (L, h), by bisection."""
    lo, hi = 0.0, 0.5
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if Color("oklch", [L, mid, h]).in_gamut("srgb") else (lo, mid)
    return lo


def hexof(L, C, h):
    """§1.3: out of gamut → reduce chroma at fixed L and h; then 8-bit."""
    C = min(C, cmax(round(L, 6), round(h % 360, 4)))
    rgb = Color("oklch", [L, C, h % 360]).convert("srgb").coords()
    return "#" + "".join(f"{round(min(1.0, max(0.0, v)) * 255):02x}" for v in rgb)


def contrast(a, b):
    return Color(a).contrast(b, method="wcag21")


def de_ok(a, b):
    return Color(a).delta_e(b, method="ok")


def bisect(f, lo, hi, n=30):
    """Smallest x in [lo, hi] with f(x) >= 0, f increasing."""
    for _ in range(n):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if f(mid) >= 0 else (mid, hi)
    return hi


# §3 Neutrals ---------------------------------------------------------------
def neutral(p, L):
    hn = oklch_of(p["seed"])[2] + 180            # reading: exact complement of the seed (doc rounds to 232°)
    return hexof(L, p["amp"] * math.sin(math.pi * L) ** 2, hn + p["drift"] * (1 - L) ** 2)


def neutrals(p):
    Lc = p["canvas"]
    n = dict(shell=neutral(p, Lc / p["r"]), canvas=neutral(p, Lc), raised=neutral(p, Lc * p["r"]),
             edge=neutral(p, Lc * p["r"] ** 2))                                            # §3.3
    Ls = Lc / p["r"]
    Lr = bisect(lambda L: contrast(neutral(p, L), n["shell"]) - contrast(neutral(p, L), n["canvas"]), Ls, Lc)  # §3.4
    n["rail"] = neutral(p, Lr)
    Lraised = Lc * p["r"]
    for lvl, tgt in p["targets"].items():                                                 # §3.5
        n[lvl] = neutral(p, bisect(lambda L: contrast(neutral(p, L), n["raised"]) - tgt, Lraised, p["ink"]))
    n["ink"] = neutral(p, p["ink"])
    return {k: n[k] for k in ("shell", "rail", "canvas", "raised", "edge", "control", "faint", "subtle", "body", "ink")}


# §6 Hues -------------------------------------------------------------------
@lru_cache(maxsize=None)
def cusp_L(h):
    grid = max((cmax(i / 200, h), i / 200) for i in range(1, 200))[1]
    return max((cmax(round(grid + j / 2000, 6), h), grid + j / 2000) for j in range(-10, 11))[1]


def chroma(p, L, h):                                                                          # §6.3
    hs = oklch_of(p["seed"])[2]
    return min(oklch_of(p["seed"])[1] / PHI * (1 + p["tau"] * math.cos(math.radians(h - hs))), p["gamut"] * cmax(round(L, 6), round(h % 360, 4)))


def hue_colors(p, hues, ember, L0):
    cm = sum(cusp_L(round(hues[c] % 360, 4)) for c in SIX) / 6
    out = {}
    for c in SIX:                                                                             # §6.2
        L = L0 + p["beta"] * (cusp_L(round(hues[c] % 360, 4)) - cm)
        out[c] = hexof(L, chroma(p, L, hues[c]), hues[c])
    eh, eL = ember                                                                            # §6.4
    out["ember"] = hexof(eL, chroma(p, eL, eh), eh)
    return out


# §9 Background states ------------------------------------------------------
@lru_cache(maxsize=None)
def _state(canvas, shell, faint, hue, target):
    """§9.3: chroma up from 0.010 by 0.001; L scanned outward from Canvas until a bound; smallest change wins."""
    n = dict(canvas=canvas, shell=shell, faint=faint)
    Lc, Cc, _ = oklch_of(n["canvas"])
    Ls = oklch_of(n["shell"])[0]
    best, most = None, (-1.0, None)
    C = 0.010
    while C <= cmax(round(Lc, 6), round(hue % 360, 4)):                    # reading: chroma up to Cmax at Canvas L (fitted to published Dusk)
        if best and C - Cc > best[0]:                                       # no larger chroma can cost less
            break
        for d in (1, -1):
            L = Lc
            while True:
                L = round(L + d * 0.001, 4)
                if L < Ls or L > 0.985:                                     # §9.2 lightness bound
                    break
                hx = hexof(L, C, hue)
                if contrast(n["faint"], hx) < 4.5:                          # §9.2 Faint bound
                    break
                vis = de_ok(hx, n["canvas"]) / 0.02
                if vis > most[0]:
                    most = (vis, hx)
                if vis >= target:
                    cost = math.hypot(L - Lc, C - Cc)                       # reading: Euclidean (ΔL, ΔC)
                    if best is None or cost < best[0]:
                        best = (cost, hx)
                    break
        C = round(C + 0.001, 4)
    return best[1] if best else most[1]                                     # unreachable → max visibility, keep hue


def state(p, n, hue, target):
    return _state(n["canvas"], n["shell"], n["faint"], round(hue % 360, 4), target)


# §6.6 floor (§6.5 not re-run: hues are inherited) ----------------------------
def solve_L0(p, n, hues, ember, code_surfaces):
    def margin(L0):                                                         # reading: §6.2, the weakest of the six hues
        cols = hue_colors(p, hues, ember, L0)
        return min(contrast(cols[c], s) for c in SIX for s in code_surfaces) - p["floor"]
    return bisect(margin, 0.40, 0.95)


def sim(hx, v):
    return Color(hx) if v is None else Color(hx).filter(v, 1.0)


def objective(cols):
    keys = list(cols)
    return min(sim(cols[a], v).delta_e(sim(cols[b], v), method="ok")
               for v in VISIONS for i, a in enumerate(keys) for b in keys[i + 1:])   # reading: 6 hues + Ember


def distinctness(flavor):
    """§6.5 objective of a built flavor: min ΔE_OK over its 7 hue colors × 4 visions (reporting only)."""
    return objective({c: v for c, v in flavor["colors"].items() if c != "afterglow"})


def inherited(pub_flavor):
    """Hue angles of the six published colors and Ember's (hue, L)."""
    cols = pub_flavor["colors"]
    hues = {c: oklch_of(cols[c.replace("_", "-")])[2] for c in SIX}
    L, _, h = oklch_of(cols["ember"])
    return hues, (h, L)


def check(p, n, anchors, hues, ember, cols, surfaces):
    """§6.5 constraints, now a feasibility check on the inherited hues."""
    ok = (all(abs(((hues[c] - anchors[c] + 180) % 360) - 180) <= p["freedom"] for c in SIX)
          and p["ember_h"][0] <= ember[0] <= p["ember_h"][1] and p["ember_L"][0] <= ember[1] <= p["ember_L"][1]
          and de_ok(cols["ember"], p["seed"]) >= p["ember_vs_seed"]
          and min(contrast(cols["ember"], s) for s in surfaces) >= p["floor"])   # reading: Ember ≥ floor is a check, not part of L0
    if not ok:
        raise ValueError("inherited hues violate the §6.5 constraints")


# §5 Accent families ---------------------------------------------------------
def at_L(hx, L):
    """Same hue and relative chroma (C / Cmax), new lightness."""
    L0, C0, h = oklch_of(hx)
    rc = C0 / cmax(round(L0, 6), round(h, 4)) if C0 else 0
    return hexof(L, rc * cmax(round(L, 6), round(h, 4)), h)


def family(n, hx, sel):
    surf = [n[s] for s in ("shell", "rail", "canvas", "raised")]
    L = oklch_of(hx)[0]
    on = max((n["shell"], n["ink"]), key=lambda x: contrast(x, hx))
    text = hx if contrast(hx, n["raised"]) >= 7 else at_L(hx, bisect(lambda x: contrast(at_L(hx, x), n["raised"]) - 7, L, 0.99))
    focus = hx if min(contrast(hx, s) for s in surf) >= 3 else at_L(hx, bisect(lambda x: min(contrast(at_L(hx, x), s) for s in surf) - 3, L, 0.99))
    pressed = hx
    for i in range(1, 101):                                                 # down by up to 0.10 L, 0.001 steps
        cand = at_L(hx, L - i / 1000)
        if contrast(on, cand) < 4.5:
            break
        pressed = cand
    chk = dict(label=contrast(on, hx), pressedLabel=contrast(on, pressed), text=contrast(text, n["raised"]),
               focus=min(contrast(focus, s) for s in surf), faintOnSel=contrast(n["faint"], sel))
    return {"accent": hx, "accent-text": text, "accent-pressed": pressed, "accent-focus": focus, "on-accent": on,
            "_check": {k: round(v, 2) for k, v in chk.items()}}


# §6.7 brights and §10 terminal ---------------------------------------------
def bright(p, hx, ink):
    L, C, h = oklch_of(hx)
    L2 = L + (oklch_of(ink)[0] - L) / 3
    return hexof(L2, min(C, p["gamut"] * cmax(round(L2, 6), round(h, 4))), h)   # reading: "capped to gamut" = the 0.92·Cmax margin (fitted to published Dusk)


def build(p, hues, ember):
    n = neutrals(p)
    diffs = [state(p, n, hues["grove"], p["jnd"]["diff-inserted"]), state(p, n, hues["coral"], p["jnd"]["diff-removed"])]
    hcols = hue_colors(p, hues, ember, solve_L0(p, n, hues, ember, [n["canvas"], *diffs]))
    check(p, n, {c: oklch_of(hx)[2] for c, hx in CORNERS.items()}, hues, ember, hcols, [n["canvas"], *diffs])
    names = dict(coral="coral", gold="gold", grove="grove", sea_salt="sea-salt", sky="sky", orchid="orchid", ember="ember")
    colors = {"afterglow": p["seed"].lower(), **{names[c]: v for c, v in hcols.items()}}
    hue_of = {"seed": oklch_of(p["seed"])[2], **{c: hues[c] for c in SIX}}
    states = {s: state(p, n, hue_of[STATE_HUE[s]], p["jnd"][s]) for s in p["jnd"]}
    order = ["afterglow", "coral", "gold", "grove", "sea-salt", "sky", "orchid", "ember"]
    accents = {a: family(n, colors[a], states["selection"]) for a in order}
    normal = [n["edge"], colors["coral"], colors["grove"], colors["gold"], colors["sky"], colors["orchid"], colors["sea-salt"], n["subtle"]]
    ansi = normal + [n["faint"], *[bright(p, c, n["ink"]) for c in normal[1:7]], n["ink"]]
    return dict(neutrals=n, colors={k: colors[k] for k in order}, accents=accents, states=states, ansi=ansi)


if __name__ == "__main__":
    dusk = json.loads((ROOT / "palette" / "twilight.json").read_text())["flavors"]["dusk"]
    print(json.dumps(build(DUSK, *inherited(dusk)), indent=2))
