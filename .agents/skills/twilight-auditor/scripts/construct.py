"""Twilight construction: the reference implementation of docs/construction.md.

Rebuilds both flavors from the decided parameters (construction.md §12) and reproduces
palette/twilight.json exactly. Nothing here is fitted to the published values.

Usage:
    python construct.py            # print the rebuilt palette as JSON (about 2 minutes)

Precision conventions (part of the method, see construction.md §14):
- OKLCH → sRGB via coloraide `fit('srgb')`, then 8-bit hex.
- Cmax(L, h) by 32-step bisection; where Cmax scales a chroma, L is rounded to 0.001 (and h to 0.1° in §5 and §6.7).
- Hue lightness from §6.2 is rounded to 0.001.
- WCAG 2.x contrast and ΔE OKLab as implemented by coloraide.
"""
import functools
import json
import math
import random

from coloraide import Color

# Decided parameters (construction.md §12) -------------------------------------
SEED = "#ee7a1f"                      # Afterglow
SEED_HUE_DEG = 52                     # seed hue rounded to the degree; used for the neutral hue and the warm tilt
NEUTRAL_HUE = SEED_HUE_DEG + 180      # 232°
DRIFT, AMP = 18.0, 0.035              # §3.1, §3.2
SURFACES_L = dict(frame=0.16, content=0.20, elevated=0.25, border=0.3125)   # §3.3, r = 1.25
TEXT_TARGETS = dict(control=3.0, muted=4.5, secondary=7.0, body=49 / 4.5)  # §3.5 (10.9 = 7² / 4.5)
INK_L = dict(dusk=0.95, dawn=0.20)
DAWN_CANVAS_L = 0.975
PHI = (1 + 5 ** 0.5) / 2
BETA, TAU, GAMUT = 0.30, 0.15, 0.92   # §6.2, §6.3
FREEDOM = 25                          # §6.1
EMBER_HUE = (45, 70)
EMBER_L = dict(dusk=[round(0.60 + 0.01 * i, 2) for i in range(31)], dawn=[round(0.35 + 0.01 * i, 2) for i in range(31)])
EMBER_VS_SEED = 0.06
FLOOR = dict(dusk=7.0, dawn=4.5)
OPT_SEED, OPT_RESTARTS, OPT_JITTER, OPT_STEPS = 1, 10, 20, (8, 4, 2, 1)     # §6.5
JND = 0.02
STATE_JND = {"selection": 4, "selection-inactive": 2, "find-match": 5, "find-match-other": 2.5,
             "word-highlight": 2, "word-highlight-write": 3, "diff-inserted": 2, "diff-removed": 2}
CORNERS = dict(red="#ff0000", yellow="#ffff00", green="#00ff00", cyan="#00ffff", blue="#0000ff", magenta="#ff00ff")
VISIONS = (None, "deutan", "protan", "tritan")


# Primitives --------------------------------------------------------------------
def oklch(L, C, h):
    return Color("oklch", [L, C, h])


def hexof(c):
    return c.convert("srgb").fit("srgb").to_string(hex=True)


def oklch_of(hx):
    L, C, h = Color(hx).convert("oklch").coords(nans=False)
    return L, C, h % 360


def contrast(a, b):
    return Color(a).contrast(Color(b), method="wcag21")


def de_ok(a, b):
    return Color(a).delta_e(Color(b), method="ok")


def sim(hx, vision):
    return Color(hx) if vision is None else Color(hx).filter(vision)


def lum(hx):
    return Color(hx).convert("srgb").luminance()


@functools.lru_cache(maxsize=None)
def cmax(L, h):
    lo, hi = 0.0, 0.5
    for _ in range(32):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if oklch(L, m, h).in_gamut("srgb") else (lo, m)
    return lo


@functools.lru_cache(maxsize=None)
def cusp(h):
    """Lightness of maximum in-gamut chroma, on a 0.002 grid over L ∈ [0.300, 0.998]."""
    best = (0.0, 0.0)
    for i in range(300, 1000, 2):
        c = cmax(i / 1000, h)
        if c > best[1]:
            best = (i / 1000, c)
    return best[0]


# §3 Neutrals (Dusk) -------------------------------------------------------------
def n_hue(L):
    return NEUTRAL_HUE + DRIFT * (1 - L) ** 2


def n_chroma(L):
    return AMP * math.sin(math.pi * L) ** 2


def neutral(L):
    return hexof(oklch(L, n_chroma(L), n_hue(L)))


def _lowest_L(target, against, lo, hi):
    """Lowest L on the Dusk neutral curve whose contrast against `against` reaches `target`."""
    for _ in range(50):
        m = (lo + hi) / 2
        lo, hi = (lo, m) if contrast(neutral(m), against) >= target else (m, hi)
    return hi


def dusk_neutrals():
    N = {k: neutral(L) for k, L in SURFACES_L.items()}
    for k, lo, hi in (("control", 0.3, 0.7), ("muted", 0.4, 0.8), ("secondary", 0.5, 0.9), ("body", 0.6, 0.95)):
        N[k] = neutral(_lowest_L(TEXT_TARGETS[k], N["elevated"], lo, hi))
    N["primary"] = neutral(INK_L["dusk"])
    N["rail"] = _half_step(lambda L: neutral(L), N, 0.16, 0.20)                        # §3.4
    return N


def _half_step(make, N, lo, hi):
    """§3.4: contrast(Rail, Canvas) = √ contrast(Shell, Canvas); 50-step bisection, last midpoint."""
    target = contrast(N["frame"], N["content"]) ** 0.5
    for _ in range(50):
        m = (lo + hi) / 2
        c = make(m)
        lo, hi = (m, hi) if contrast(c, N["content"]) > target else (lo, m)
    return c


# §4 Dawn mirror ------------------------------------------------------------------
REL = {k: n_chroma(L) / cmax(round(L, 3), round(n_hue(L), 1)) for k, L in SURFACES_L.items()}   # relative chroma of each Dusk surface


def lneutral(L, rel=None):
    C = n_chroma(L) if rel is None else rel * cmax(round(L, 3), round(n_hue(L), 1))
    return hexof(oklch(L, C, n_hue(L)))


def dawn_neutrals(dusk):
    def darker_by(ratio, ref, rel):
        lo, hi = 0.5, 0.999
        for _ in range(50):
            m = (lo + hi) / 2
            lo, hi = (lo, m) if contrast(lneutral(m, rel), ref) < ratio else (m, hi)
        return lneutral(lo, rel)

    def highest_L(target, against):
        lo, hi = 0.05, 0.95
        for _ in range(50):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if contrast(lneutral(m), against) >= target else (lo, m)
        return lneutral(lo)

    N = {"content": lneutral(DAWN_CANVAS_L, REL["content"])}
    for k in ("frame", "elevated", "border"):                                             # same ratios to Canvas as Dusk
        N[k] = darker_by(contrast(dusk[k], dusk["content"]), N["content"], REL[k])
    for k in ("control", "muted", "secondary", "body"):
        N[k] = highest_L(TEXT_TARGETS[k], N["elevated"])
    N["primary"] = lneutral(INK_L["dawn"])
    rel = (REL["frame"] + REL["content"]) / 2
    N["rail"] = _half_step(lambda L: lneutral(L, rel), N, 0.95, 0.974)
    return N


# §6 Hues -------------------------------------------------------------------------
ANCHORS = {k: round(oklch_of(v)[2]) for k, v in CORNERS.items()}                            # whole degrees
SIX = list(ANCHORS)
CUSP_MEAN = sum(cusp(h) for h in ANCHORS.values()) / 6
C0 = oklch_of(SEED)[1] / PHI


def chroma(L, h):
    return min(C0 * (1 + TAU * math.cos(math.radians(h - SEED_HUE_DEG))), GAMUT * cmax(round(L, 3), h))


def hue_colors(L0, hues, ember):
    out = {}
    for name, h in zip(SIX, hues):
        L = round(L0 + BETA * (cusp(h) - CUSP_MEAN), 3)
        out[name] = hexof(oklch(L, chroma(L, h), h))
    eh, eL = ember
    out["ember"] = hexof(oklch(eL, chroma(eL, eh), eh))
    return out


def solve_L0(hues, ember, surface, floor, dark):
    """§6.2: 18-step bisection so the weakest of the six hues (Ember excluded) meets the floor on `surface`."""
    lo, hi = (0.5, 0.95) if dark else (0.2, 0.7)
    for _ in range(18):
        m = (lo + hi) / 2
        weakest = min(contrast(v, surface) for k, v in hue_colors(m, hues, ember).items() if k != "ember")
        if dark:
            lo, hi = (lo, m) if weakest >= floor else (m, hi)
        else:
            lo, hi = (m, hi) if weakest >= floor else (lo, m)
    return hi if dark else lo


def distinctness(cols):
    """§6.5 objective: min ΔE OKLab over the 7 hue colors × 4 visions, minus the Ember–seed penalty."""
    vals = list(cols.values())
    worst = min(sim(a, v).delta_e(sim(b, v), method="ok")
                for v in VISIONS for i, a in enumerate(vals) for b in vals[i + 1:])
    return worst - 2 * max(0.0, EMBER_VS_SEED - de_ok(cols["ember"], SEED))


def optimize(surface, flavor):
    """§6.5: seeded coordinate descent. Returns (hues, ember, colors, L0)."""
    dark, floor, rng = flavor == "dusk", FLOOR[flavor], EMBER_L[flavor]
    random.seed(OPT_SEED)
    base = [ANCHORS[n] for n in SIX]

    def evaluate(hues, ember):
        L0 = solve_L0(hues, ember, surface, floor, dark)
        cols = hue_colors(L0, hues, ember)
        return (-1.0 if contrast(cols["ember"], surface) < floor else distinctness(cols)), cols, L0

    best = None
    for r in range(OPT_RESTARTS):
        hues = [a + (random.randint(-OPT_JITTER, OPT_JITTER) if r else 0) for a in base]
        ember = [random.randint(*EMBER_HUE), random.choice(rng)]
        score = evaluate(hues, ember)[0]
        for step in OPT_STEPS:
            improved = True
            while improved:
                improved = False
                for i in range(8):
                    for d in (-step, step):
                        h2, e2 = list(hues), list(ember)
                        if i < 6:
                            h2[i] += d
                            if abs(h2[i] - base[i]) > FREEDOM:
                                continue
                        elif i == 6:
                            e2[0] += d
                            if not EMBER_HUE[0] <= e2[0] <= EMBER_HUE[1]:
                                continue
                        else:
                            e2[1] = round(e2[1] + d * 0.01, 3)
                            if not rng[0] <= e2[1] <= rng[-1]:
                                continue
                        s2 = evaluate(h2, e2)[0]
                        if s2 > score + 1e-6:
                            hues, ember, score, improved = h2, e2, s2, True
        if best is None or score > best[0]:
            best = (score, hues, ember)
    _, cols, L0 = evaluate(best[1], best[2])
    return best[1], best[2], cols, L0


# §9 Background states --------------------------------------------------------------
def state(N, hue, jnd, dark):
    """§9.3. Chroma 0.010–0.140 in 0.001 steps; for each chroma and direction, L moves from Canvas in 0.001 steps
    until a bound; the first step reaching the target is a candidate with cost 1000·|ΔL| + 100·C; lowest cost wins
    (earliest on ties). If no candidate exists, the most visible color found."""
    bg = N["content"]
    target = jnd * JND
    L0 = oklch_of(bg)[0]
    Lmin, Lmax = (oklch_of(N["frame"])[0], 1.0) if dark else (0.0, 0.985)
    best, most = None, None
    for ci in range(10, 141):
        C = ci / 1000
        for sign in (1, -1):
            for li in range(400):
                L = L0 + sign * li / 1000
                if not Lmin <= L <= Lmax:
                    break
                c = oklch(L, C, hue)
                if not c.in_gamut("srgb"):
                    break
                hx = hexof(c)
                if contrast(N["muted"], hx) < 4.5:
                    break
                d = de_ok(hx, bg)
                if most is None or d > most[1]:
                    most = (hx, d)
                if d >= target:
                    if best is None or li + C * 100 < best[0]:
                        best = (li + C * 100, hx)
                    break
    return best[1] if best else most[0]


# §5 Accent families ----------------------------------------------------------------
def family(N, base, dark):
    L, C, h = oklch_of(base)
    rho = C / max(cmax(round(L, 3), round(h, 1)), 1e-6)

    def at(L2):
        return hexof(oklch(L2, rho * cmax(round(L2, 3), round(h, 1)), h))

    on = max([N["frame"], N["primary"]] if dark else [N["primary"], N["content"]], key=lambda x: contrast(x, base))
    surfaces = [N[k] for k in ("frame", "rail", "content", "elevated")]
    toward = 0.95 if dark else 0.20

    def solve(ok):
        if ok(base):
            return base
        a, b = L, toward
        for _ in range(50):
            m = (a + b) / 2
            a, b = (a, m) if ok(at(m)) else (m, b)
        return at(b)

    text = solve(lambda x: contrast(x, N["elevated"]) >= (7.0 if dark else 4.5))
    focus = solve(lambda x: min(contrast(x, s) for s in surfaces) >= 3.0)
    pressed = at(L - 0.10)
    if contrast(on, pressed) < 4.5:
        a, b = L, L - 0.10
        for _ in range(50):
            m = (a + b) / 2
            a, b = (m, b) if contrast(on, at(m)) >= 4.5 else (a, m)
        pressed = at(a)
    return {"accent": base, "accent-text": text, "accent-pressed": pressed, "accent-focus": focus, "on-accent": on}


# §6.7 Brights ------------------------------------------------------------------------
def bright(hx, ink):
    L, C, h = oklch_of(hx)
    L2 = L + (oklch_of(ink)[0] - L) / 3
    return hexof(oklch(L2, min(C, GAMUT * cmax(round(L2, 3), round(h, 1))), h))


# Assembly ------------------------------------------------------------------------------
NAMES = dict(shell="frame", rail="rail", canvas="content", raised="elevated", edge="border", control="control",
             faint="muted", subtle="secondary", body="body", ink="primary")
COLOR_KEYS = dict(coral="red", gold="yellow", grove="green", **{"sea-salt": "cyan"}, sky="blue", orchid="magenta", ember="ember")


def build_flavor(flavor, dusk_neutrals_hex=None):
    dark = flavor == "dusk"
    N = dusk_neutrals() if dark else dawn_neutrals(dusk_neutrals_hex)
    hue = lambda hx: oklch_of(hx)[2]
    # Pass 1 (§6.6): hues against Canvas; their Grove and Coral place the diff backgrounds.
    _, _, first, _ = optimize(N["content"], flavor)
    d_ins = state(N, hue(first["green"]), STATE_JND["diff-inserted"], dark)
    d_rem = state(N, hue(first["red"]), STATE_JND["diff-removed"], dark)
    worst = (max if dark else min)([N["content"], d_ins, d_rem], key=lum)
    # Pass 2: hues against the worst code surface. Diff backgrounds are not recomputed.
    hues, ember, S, L0 = optimize(worst, flavor)
    sh = hue(SEED)
    states = {
        "selection": state(N, sh, STATE_JND["selection"], dark),
        "selection-inactive": state(N, sh, STATE_JND["selection-inactive"], dark),
        "find-match": state(N, hue(S["yellow"]), STATE_JND["find-match"], dark),
        "find-match-other": state(N, hue(S["yellow"]), STATE_JND["find-match-other"], dark),
        "word-highlight": state(N, hue(S["cyan"]), STATE_JND["word-highlight"], dark),
        "word-highlight-write": state(N, hue(S["cyan"]), STATE_JND["word-highlight-write"], dark),
        "diff-inserted": d_ins, "diff-removed": d_rem,
    }
    colors = {"afterglow": SEED, **{k: S[v] for k, v in COLOR_KEYS.items()}}
    order = ["red", "green", "yellow", "blue", "magenta", "cyan"]
    ansi = ([N["border"] if dark else N["body"]] + [S[k] for k in order] + [N["secondary"] if dark else N["border"]]
            + [N["muted"]] + [bright(S[k], N["primary"]) for k in order] + [N["primary"] if dark else N["elevated"]])
    out = {"neutrals": {k: N[v] for k, v in NAMES.items()}, "colors": colors,
           "accents": {k: family(N, v, dark) for k, v in colors.items()}, "states": states, "ansi": ansi}
    meta = {"hues": hues, "ember": ember, "L0": L0, "pass1_hues": {k: round(hue(first[k])) for k in ("green", "red")}}
    return out, meta, N


def build_palette():
    """Both flavors, in the shape of palette/twilight.json → flavors. Returns (palette, meta)."""
    dusk, dusk_meta, dusk_raw = build_flavor("dusk")
    dawn, dawn_meta, _ = build_flavor("dawn", dusk_raw)
    return {"dusk": dusk, "dawn": dawn}, {"dusk": dusk_meta, "dawn": dawn_meta}


if __name__ == "__main__":
    palette, meta = build_palette()
    print(json.dumps({"flavors": palette, "meta": meta}, indent=2))