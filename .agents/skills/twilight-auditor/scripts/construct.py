"""Twilight Theme construction: the reference implementation of docs/construction.md.

Rebuilds both flavors from the decided parameters (construction.md §12) and reproduces
palette/twilight.json exactly. Nothing here is fitted to the published values.

Structure (construction.md §1):
- System: the rules every flavor shares, from the seed and the neutral curve to the surface ratio, the text
  targets, the states, the families and the optimizer. Changing one changes every flavor.
- Category (CATEGORIES): what dark and light themes do differently: direction of the surfaces and of the text
  search, β, the chroma base, the code floor and the search ranges.
- Flavor (FLAVORS): its category and its own anchors (Canvas and Ink lightness) and neutral tint. A flavor reads
  only the system and its category, never another flavor.

Usage:
    python construct.py            # print the rebuilt palette as JSON (about 2 minutes)

Precision conventions (part of the method, see construction.md §12.1):
- OKLCH → sRGB via coloraide `fit('srgb')`, then 8-bit hex.
- Cmax(L, h) by 32-step bisection; where Cmax scales a chroma, L is rounded to 0.001 (and h to 0.1° in §5 and §6.7).
- Hue lightness from §6.2 is rounded to 0.001.
- WCAG 2.x contrast and ΔE OKLab as implemented by coloraide.
"""
import functools
import itertools
import json
import math
import random

from coloraide import Color

# Decided parameters shared by both flavors (construction.md §12) ------------------
SEED = "#ee7a1f"                      # the origin: its hue places Afterglow (§2); its chroma is the light chroma base (§6.3)
SEED_HUE_DEG = 52                     # seed hue rounded to the degree; used for the neutral hue and the warm tilt
NEUTRAL_HUE = SEED_HUE_DEG + 180      # 232°
DRIFT, AMP = 18.0, 0.035              # §3.1, §3.2 (AMP: the reference amplitude; a flavor sets its own `amp`)
R, L_REF = 1.3125, 0.20                 # §3.3: surface ratio and the lightness its scale is measured at
TEXT_TARGETS = dict(control=3.0, muted=4.5, secondary=7.0, body=49 / 4.5)  # §3.5 (10.9 = 7² / 4.5)
PHI = (1 + 5 ** 0.5) / 2
TAU, GAMUT = 0.15, 0.92               # §6.3
FREEDOM = 24                          # §6.1: the smallest that keeps every minimum in both flavors
EMBER_HUE = (45, 70)                  # §6.4
OPT_SEED, OPT_RESTARTS, OPT_JITTER, OPT_STEPS = 1, 10, 20, (8, 4, 2, 1)     # §6.5
JND = 0.02
# §9.1: strong states take the most visible color the bounds allow; weak states the visibility minimum, 2 JND.
STATE_ROLE = {"selection": "strong", "selection-inactive": "weak", "find-match": "strong", "find-match-other": "weak",
              "word-highlight": "weak", "word-highlight-write": "strong", "diff-inserted": "weak", "diff-removed": "weak"}
WEAK_JND = 2
STATE_JND = {name: (None if role == "strong" else WEAK_JND) for name, role in STATE_ROLE.items()}
CORNERS = dict(red="#ff0000", yellow="#ffff00", green="#00ff00", cyan="#00ffff", blue="#0000ff", magenta="#ff00ff")
VISIONS = (None, "deutan", "protan", "tritan")

# Categories (construction.md §4) ----------------------------------------------------
# surfaces: the direction of each surface from Canvas (+1 lighter, −1 darker), at the system distances (§3.3).
# text: dark themes take the lowest L that reaches each target (search range per level); light themes the highest.
# chroma_base: the chroma divided by φ to give C₀ (§6.3), Afterglow's in dark themes and the seed's in light ones.
CATEGORIES = {
    "dark": dict(dark=True, surfaces=dict(frame=-1, elevated=+1, border=+1),
                 text=dict(control=(0.3, 0.7), muted=(0.4, 0.8), secondary=(0.5, 0.9), body=(0.6, 0.95)),
                 floor=7.0, beta=0.30, chroma_base="afterglow",
                 L0_range=(0.5, 0.95), ember_L=[round(0.60 + 0.01 * i, 2) for i in range(31)]),
    "light": dict(dark=False, surfaces=dict(frame=-1, elevated=-1, border=-1),
                  text=dict(control=(0.05, 0.95), muted=(0.05, 0.95), secondary=(0.05, 0.95), body=(0.05, 0.95)),
                  floor=4.5, beta=0.19, chroma_base="seed",
                  L0_range=(0.2, 0.7), ember_L=[round(0.35 + 0.01 * i, 2) for i in range(31)]),
}

# Flavors (construction.md §4) ------------------------------------------------------------
FLAVORS = {
    "dusk": dict(category="dark", canvas_L=0.20, ink_L=0.95, amp=AMP),
    "dawn": dict(category="light", canvas_L=0.95, ink_L=0.20, amp=AMP),
}
PROFILES = {name: {**CATEGORIES[f["category"]], **f} for name, f in FLAVORS.items()}


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


# §3 The neutral curve (system) -----------------------------------------------------------
def n_hue(L):
    return NEUTRAL_HUE + DRIFT * (1 - L) ** 2


def n_chroma(L, amp=AMP):
    return amp * math.sin(math.pi * L) ** 2


def neutral(L, amp=AMP):
    return hexof(oklch(L, n_chroma(L, amp), n_hue(L)))


# §3.3 Surface distances (system): the geometric scale L_REF · rⁿ, measured as ΔE OKLab from its middle step
SEPARATIONS = {name: de_ok(neutral(L_REF * R ** n), neutral(L_REF)) for name, n in (("frame", -1), ("elevated", 1), ("border", 2))}


def neutrals(flavor):
    """§3, §4: a flavor's ten neutrals. Every one is a point of the neutral curve with the flavor's amplitude."""
    P = PROFILES[flavor]
    amp, canvas_L = P["amp"], P["canvas_L"]
    nt = lambda L: neutral(L, amp)
    N = {"content": nt(canvas_L)}

    def place(sign, sep):
        """§3.3: the L nearest Canvas, in the category's direction, whose ΔE OKLab from Canvas reaches `sep`."""
        lo, hi = (canvas_L, 0.999) if sign > 0 else (0.02, canvas_L)
        for _ in range(50):
            m = (lo + hi) / 2
            far = de_ok(nt(m), N["content"]) >= sep
            if sign > 0:
                lo, hi = (lo, m) if far else (m, hi)
            else:
                lo, hi = (m, hi) if far else (lo, m)
        return hi if sign > 0 else lo

    Ls = {k: place(sign, SEPARATIONS[k]) for k, sign in P["surfaces"].items()}
    N.update({k: nt(L) for k, L in Ls.items()})

    # §3.5: each text level solved against Raised, upward in dark themes and downward in light ones
    for k, (lo, hi) in P["text"].items():
        for _ in range(50):
            m = (lo + hi) / 2
            ok = contrast(nt(m), N["elevated"]) >= TEXT_TARGETS[k]
            if P["dark"]:
                lo, hi = (lo, m) if ok else (m, hi)
            else:
                lo, hi = (m, hi) if ok else (lo, m)
        N[k] = nt(hi if P["dark"] else lo)
    N["primary"] = nt(P["ink_L"])

    # §3.4: Rail is a half step, contrast(Rail, Canvas) = √ contrast(Shell, Canvas); 50-step bisection, last midpoint
    target = contrast(N["frame"], N["content"]) ** 0.5
    lo, hi = Ls["frame"], canvas_L
    for _ in range(50):
        m = (lo + hi) / 2
        c = nt(m)
        lo, hi = (m, hi) if contrast(c, N["content"]) > target else (lo, m)
    N["rail"] = c
    return N


# §6 Hues -------------------------------------------------------------------------
ANCHORS = {k: round(oklch_of(v)[2]) for k, v in CORNERS.items()}                            # whole degrees
EXACT_ANCHORS = {k: oklch_of(v)[2] for k, v in CORNERS.items()}                             # for the hue-freedom rule
SIX = list(ANCHORS)
CUSP_MEAN = sum(cusp(h) for h in ANCHORS.values()) / 6

# §2 Afterglow: the most chromatic color sRGB holds at the seed hue (its cusp). The seed itself is not a token.
_H = round(oklch_of(SEED)[2], 1)
AFTERGLOW = hexof(oklch(cusp(_H), cmax(cusp(_H), _H), _H))
BASE_CHROMA = {"afterglow": oklch_of(AFTERGLOW)[1], "seed": oklch_of(SEED)[1]}


def c0(P):
    """§6.3: C₀ = C_base / φ, with the base chosen by the profile."""
    return BASE_CHROMA[P["chroma_base"]] / PHI


def chroma(L, h, P):
    return min(c0(P) * (1 + TAU * math.cos(math.radians(h - SEED_HUE_DEG))), GAMUT * cmax(round(L, 3), h))


def hue_colors(L0, hues, ember, P):
    out = {}
    for name, h in zip(SIX, hues):
        L = round(L0 + P["beta"] * (cusp(h) - CUSP_MEAN), 3)
        out[name] = hexof(oklch(L, chroma(L, h, P), h))
    eh, eL = ember
    out["ember"] = hexof(oklch(eL, chroma(eL, eh, P), eh))
    return out


def solve_L0(hues, ember, surface, P):
    """§6.2: 18-step bisection so the weakest of the six hues (Ember excluded) meets the floor on `surface`.
    Dark: the lowest L₀ that passes (upper bound of the bracket). Light: the highest (lower bound)."""
    lo, hi = P["L0_range"]
    for _ in range(18):
        m = (lo + hi) / 2
        weakest = min(contrast(v, surface) for k, v in hue_colors(m, hues, ember, P).items() if k != "ember")
        if P["dark"]:
            lo, hi = (lo, m) if weakest >= P["floor"] else (m, hi)
        else:
            lo, hi = (m, hi) if weakest >= P["floor"] else (lo, m)
    return hi if P["dark"] else lo


def distinctness(cols, cursor):
    """§6.5 objective: min ΔE OKLab × 4 visions over every pair of the 7 hue colors and every code color against
    the cursor (Coral excluded, as in the guarantee)."""
    vals = list(cols.values())
    pairs = [(a, b) for i, a in enumerate(vals) for b in vals[i + 1:]]
    pairs += [(cols[n], cursor) for n in cols if n != "red"]
    return min(sim(a, v).delta_e(sim(b, v), method="ok") for v in VISIONS for a, b in pairs)


def optimize(surface, P, cursor):
    """§6.5: seeded coordinate descent. `cursor` is Afterglow's accent-focus. Returns (hues, ember, colors, L0)."""
    floor, rng = P["floor"], P["ember_L"]
    random.seed(OPT_SEED)
    base = [ANCHORS[n] for n in SIX]

    def evaluate(hues, ember):
        L0 = solve_L0(hues, ember, surface, P)
        cols = hue_colors(L0, hues, ember, P)
        if any(abs((oklch_of(cols[n])[2] - EXACT_ANCHORS[n] + 180) % 360 - 180) > FREEDOM for n in SIX):
            return -2.0, cols, L0            # §6.1 is checked on the rendered hue, against the exact anchor
        return (-1.0 if contrast(cols["ember"], surface) < floor else distinctness(cols, cursor)), cols, L0

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
def state_bounds(N, P):
    """§9.2: a state may leave the surface envelope only toward the text, where Faint ≥ 4.5:1 is the bound.
    Away from the text it stops at the outermost surface: Shell in Dusk, Canvas in Dawn."""
    return (oklch_of(N["frame"])[0], 1.0) if P["dark"] else (0.0, oklch_of(N["content"])[0])


def state(N, hue, jnd, P, built=()):
    """§9.3. Chroma 0.010–0.140 in 0.001 steps; for each chroma and direction, L moves from Canvas in 0.001 steps
    until a bound; the first step reaching the target is a candidate with cost 1000·|ΔL| + 100·C; lowest cost wins
    (earliest on ties). If no candidate exists, the most visible color found.
    §9.4: among those, a color at least 1 JND from every state in `built` is preferred; visibility comes first."""
    bg = N["content"]
    target = float("inf") if jnd is None else jnd * JND      # None: a strong state, the most visible color
    L0 = oklch_of(bg)[0]
    Lmin, Lmax = state_bounds(N, P)
    best, most, best_sep, most_sep = None, None, None, None
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
                apart = all(de_ok(hx, b) >= JND for b in built)
                if most is None or d > most[1]:
                    most = (hx, d)
                if apart and (most_sep is None or d > most_sep[1]):
                    most_sep = (hx, d)
                if d >= target:
                    cost = li + C * 100
                    if best is None or cost < best[0]:
                        best = (cost, hx)
                    if apart and (best_sep is None or cost < best_sep[0]):
                        best_sep = (cost, hx)
                    break
    if best:
        return (best_sep or best)[1]
    return (most_sep or most)[0]


# §5 Accent families ----------------------------------------------------------------
def family(N, base, P):
    L, C, h = oklch_of(base)
    rho = C / max(cmax(round(L, 3), round(h, 1)), 1e-6)

    def at(L2):
        return hexof(oklch(L2, rho * cmax(round(L2, 3), round(h, 1)), h))

    on = max([N["frame"], N["primary"]] if P["dark"] else [N["primary"], N["content"]], key=lambda x: contrast(x, base))
    surfaces = [N[k] for k in ("frame", "rail", "content", "elevated")]
    toward = P["ink_L"]

    def solve(ok):
        if ok(base):
            return base
        a, b = L, toward
        for _ in range(50):
            m = (a + b) / 2
            a, b = (a, m) if ok(at(m)) else (m, b)
        return at(b)

    text = solve(lambda x: contrast(x, N["elevated"]) >= P["floor"])
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
BRIGHT_STEP = 0.38   # resolved (§6.7): bright_step() on BRIGHT_BASIS


def bright(hx, ink, step=None):
    """§6.7: the normal moved `step` of the way toward Ink in L, same hue, chroma capped to the gamut."""
    L, C, h = oklch_of(hx)
    L2 = L + (oklch_of(ink)[0] - L) * (BRIGHT_STEP if step is None else step)
    return hexof(oklch(L2, min(C, GAMUT * cmax(round(L2, 3), round(h, 1))), h))


BRIGHT_BASIS = ("dusk", "dawn")
ANSI_HUES = ("coral", "grove", "gold", "sky", "orchid", "sea-salt")   # ANSI 1–6


def bright_step(palettes, grid=0.005):
    """§6.7: on a grid from 0 to 1, the steps at which every bright is at least 2 JND from its normal and from Ink,
    in every flavor given; among them, the one whose closest pair of the twelve chromatic ANSI colors, worst case over
    every vision and flavor, is largest. Ties go to the smaller step."""
    def twelve(F, t):
        ink = F["neutrals"]["ink"]
        normals = [F["colors"][c] for c in ANSI_HUES]
        return normals, [bright(x, ink, t) for x in normals], ink

    best = None
    for i in range(1, int(round(1 / grid))):
        t = round(i * grid, 6)
        ok, score = True, float("inf")
        for F in palettes.values():
            normals, brights, ink = twelve(F, t)
            if min(min(de_ok(n, b), de_ok(b, ink)) for n, b in zip(normals, brights)) < 2 * JND:
                ok = False
                break
            score = min(score, worst_de(normals + brights))
        if ok and (best is None or score > best[1] + 1e-12):
            best = (t, score)
    return best[0]


# Assembly ------------------------------------------------------------------------------
NAMES = dict(shell="frame", rail="rail", canvas="content", raised="elevated", edge="border", control="control",
             faint="muted", subtle="secondary", body="body", ink="primary")
COLOR_KEYS = dict(coral="red", gold="yellow", grove="green", **{"sea-salt": "cyan"}, sky="blue", orchid="magenta", ember="ember")


def transient_states(N, P, sources, diffs, order=None):
    """§9.4: transient states built one after another, each kept ≥ 1 JND from every state built before it (the diff
    lines first). The order is fixed for determinism; every order gives the same states (§9.4)."""
    states, built = {}, list(diffs)
    for name in (order or list(sources)):
        states[name] = state(N, sources[name], STATE_JND[name], P, built)
        built.append(states[name])
    return states


def build_flavor(flavor):
    P = PROFILES[flavor]
    dark = P["dark"]
    N = neutrals(flavor)
    hue = lambda hx: oklch_of(hx)[2]
    # Pass 1 (§6.6): hues against Canvas; their Grove and Coral place the diff backgrounds.
    cursor = family(N, AFTERGLOW, P)["accent-focus"]
    _, _, first, _ = optimize(N["content"], P, cursor)
    d_ins = state(N, hue(first["green"]), STATE_JND["diff-inserted"], P)
    d_rem = state(N, hue(first["red"]), STATE_JND["diff-removed"], P, [d_ins])
    worst = (max if dark else min)([N["content"], d_ins, d_rem], key=lum)
    # Pass 2: hues against the worst code surface. Diff backgrounds are not recomputed.
    hues, ember, S, L0 = optimize(worst, P, cursor)
    sh = hue(AFTERGLOW)
    sources = {"selection": sh, "selection-inactive": sh, "find-match": hue(S["yellow"]),
               "find-match-other": hue(S["yellow"]), "word-highlight": hue(S["cyan"]),
               "word-highlight-write": hue(S["cyan"])}
    states = transient_states(N, P, sources, [d_ins, d_rem])
    states.update({"diff-inserted": d_ins, "diff-removed": d_rem})
    colors = {"afterglow": AFTERGLOW, **{k: S[v] for k, v in COLOR_KEYS.items()}}
    order = ["red", "green", "yellow", "blue", "magenta", "cyan"]
    ansi = ([N["border"] if dark else N["body"]] + [S[k] for k in order] + [N["secondary"] if dark else N["border"]]
            + [N["muted"]] + [bright(S[k], N["primary"]) for k in order] + [N["primary"] if dark else N["elevated"]])
    labels = scale_labels(N)
    scales = {"sequential": sequential(N["content"], colors, labels), "diverging": diverging(N["content"], colors, labels)}
    out = {"neutrals": {k: N[v] for k, v in NAMES.items()}, "colors": colors,
           "accents": {k: family(N, v, P) for k, v in colors.items()}, "states": states, "ansi": ansi,
           "scales": scales}
    meta = {"hues": hues, "ember": ember, "L0": L0, "pass1_hues": {k: round(hue(first[k])) for k in ("green", "red")}}
    return out, meta, N


# Data series (§7.1) ----------------------------------------------------------------------
SERIES = ("sky", "ember", "gold", "sea-salt", "orchid", "grove")   # decided: series_order() on SERIES_BASIS
SERIES_OTHER = "control"                                         # the neutral for any series past the sixth
SERIES_BASIS = ("dusk", "dawn")


def worst_de(cols):
    """Smallest ΔE OKLab over every pair of `cols` and every vision (normal and three dichromacies)."""
    return min(sim(a, v).delta_e(sim(b, v), method="ok") for v in VISIONS for i, a in enumerate(cols) for b in cols[i + 1:])


def series_order(palettes):
    """§7.1: the order of the six code colors (Coral excluded) whose every prefix keeps, in every flavor given, the
    largest share of the best separation any set of that size reaches; ties go to the first series farthest from
    Afterglow. `palettes` maps flavor → palette (as in palette/twilight.json → flavors)."""
    six = [c for c in COLOR_KEYS if c != "coral"]
    cache = {}

    def w(f, s):
        key = (f, frozenset(s))
        if key not in cache:
            cache[key] = worst_de([palettes[f]["colors"][c] for c in s])
        return cache[key]

    best = {f: {n: max(w(f, s) for s in itertools.combinations(six, n)) for n in range(2, 7)} for f in palettes}
    glow = lambda c: min(worst_de([palettes[f]["colors"][c], AFTERGLOW]) for f in palettes)
    key = lambda o: (*(min(w(f, o[:n]) / best[f][n] for f in palettes) for n in range(2, 7)), glow(o[0]))
    return max(itertools.permutations(six), key=key)


# Syntax roles (§8): five by the ANSI convention; parameter and property resolved by syntax_roles.uncolored()
SYNTAX = {"keyword": "orchid", "string": "grove", "function": "sky", "type": "sea-salt", "constant": "gold",
          "parameter": "ember", "property": "body"}


# Continuous scales (§7.2) -----------------------------------------------------------------
SEQUENTIAL = ("ember", 5)              # decided by scale_search() on SCALE_BASIS: color, steps
DIVERGING = (("sky", "gold"), 2)       # the two arms (negative, positive) and steps per arm; Canvas is the middle
SCALE_BASIS = ("dusk", "dawn")
SCALE_NORMAL, SCALE_CVD, SCALE_LABEL = 4 * JND, 2 * JND, 4.5   # the code colors' separation; AA for labels in cells


def scale_arc(bg, col, samples=1500):
    """§7.2: from Canvas's lightness at zero chroma to the color, at the color's hue; L and C grow together.
    Returns the rendered samples and their cumulative ΔE OKLab from Canvas."""
    Lb = oklch_of(bg)[0]
    L, C, h = oklch_of(col)
    hx = [hexof(oklch(Lb + (L - Lb) * i / samples, C * i / samples, h)) for i in range(samples + 1)]
    d = [de_ok(bg, hx[0])]
    for a, b in zip(hx, hx[1:]):
        d.append(d[-1] + de_ok(a, b))
    return hx, d


def scale_steps(arc, total, n):
    """n steps at equal ΔE along the arc, up to `total` (the nearest sample to each)."""
    hx, d = arc
    return [hx[min(range(len(d)), key=lambda j: abs(d[j] - total * i / n))] for i in range(1, n + 1)]


def scale_labels(N):
    """The labels a cell may carry: Ink, and the neutral farthest from it (the chip label of design-system §8)."""
    return N["primary"], max(N.values(), key=lambda x: contrast(x, N["primary"]))


def _apart(a, b):
    return de_ok(a, b) >= SCALE_NORMAL and min(de_ok(sim(a, v), sim(b, v)) for v in VISIONS[1:]) >= SCALE_CVD


def _labelled(cells, labels):
    return min(max(contrast(c, x) for x in labels) for c in cells)


def sequential(bg, colors, labels, color=None, n=None):
    color, n = color or SEQUENTIAL[0], n or SEQUENTIAL[1]
    arc = scale_arc(bg, colors[color])
    return scale_steps(arc, arc[1][-1], n)


def diverging(bg, colors, labels, pair=None, n=None):
    (a, b), n = pair or DIVERGING[0], n or DIVERGING[1]
    arcs = scale_arc(bg, colors[a]), scale_arc(bg, colors[b])
    total = min(arcs[0][1][-1], arcs[1][1][-1])
    neg, pos = (scale_steps(x, total, n) for x in arcs)
    return list(reversed(neg)) + [bg] + pos


def scale_ok(cells, bg, labels, kind):
    """§7.2: adjacent cells (and, for a diverging scale, the two cells at the same distance from the middle) are
    as far apart as the code colors must be, and every colored cell takes a label at AA."""
    chain = [bg] + cells if kind == "sequential" else cells
    pairs = list(zip(chain, chain[1:]))
    if kind == "diverging":
        n = len(cells) // 2
        pairs += [(cells[n - 1 - i], cells[n + 1 + i]) for i in range(n)]
    colored = [c for c in cells if c != bg]
    return all(_apart(a, b) for a, b in pairs) and _labelled(colored, labels) >= SCALE_LABEL


def scale_search(palettes):
    """§7.2: the series color, and the pair of series colors, with the most steps that pass scale_ok() in every flavor
    given. Ties: the larger lowest label contrast (sequential); the larger worst-vision separation over every pair of
    cells (diverging). Returns ((color, n), ((a, b), n))."""
    def ctx(F):
        N = {NAMES[t]: v for t, v in F["neutrals"].items()}
        return F["neutrals"]["canvas"], F["colors"], scale_labels(N)

    def largest(build, kind):
        best = 0
        for n in range(1, 16):
            if all(scale_ok(build(*ctx(F), n), ctx(F)[0], ctx(F)[2], kind) for F in palettes.values()):
                best = n
        return best

    seq = []
    for c in SERIES:
        n = largest(lambda bg, cols, lab, n, c=c: sequential(bg, cols, lab, c, n), "sequential")
        if n:
            tie = min(_labelled(sequential(*ctx(F), c, n), ctx(F)[2]) for F in palettes.values())
            seq.append((n, tie, c))
    div = []
    for a, b in itertools.combinations(SERIES, 2):
        n = largest(lambda bg, cols, lab, n, a=a, b=b: diverging(bg, cols, lab, (a, b), n), "diverging")
        if n:
            tie = min(worst_de([x for x in diverging(*ctx(F), (a, b), n) if x != ctx(F)[0]]) for F in palettes.values())
            div.append((n, tie, (a, b)))
    s, d = max(seq), max(div)
    return (s[2], s[0]), (d[2], d[0])


def build_palette():
    """Every flavor, in the shape of palette/twilight.json → flavors. Returns (palette, meta)."""
    built = {name: build_flavor(name) for name in FLAVORS}
    return {n: b[0] for n, b in built.items()}, {n: b[1] for n, b in built.items()}


if __name__ == "__main__":
    palette, meta = build_palette()
    print(json.dumps({"flavors": palette, "meta": meta}, indent=2))
