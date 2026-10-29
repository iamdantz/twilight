"""Twilight Theme validator: quality floors, construction reproduction and document consistency.

Usage (from anywhere inside the Twilight Theme repository):
    <skill>/.venv/bin/python <skill>/scripts/validate.py [palette/twilight.json] [--ref REF] [--compare REF] [--json] [--no-rebuild] [--robust]

The rebuild runs construct.py (both flavors, §6.5 included) once per invocation, about 2 minutes.
--no-rebuild skips it; use only for changes that cannot touch values (wording, links).

Exit status 1 if any floor, consistency or reproduction check fails.
"""
import argparse
import ast
import contextlib
import io
import itertools
import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True).stdout.strip())
sys.path.insert(0, str(Path(__file__).resolve().parent))
import construct as k  # noqa: E402  (construct.py beside this file: the reference implementation of construction.md)

SURF = ("shell", "rail", "canvas", "raised")
CODE = ("orchid", "sky", "sea-salt", "grove", "gold", "ember", "coral")
CVD_SET = ("orchid", "sky", "sea-salt", "grove", "gold", "ember")          # + cursor (default accent-focus)
SEMANTIC = ("coral", "gold", "grove", "sea-salt", "sky", "orchid")                       # design-system.md §8
TRANSIENT = ("selection", "selection-inactive", "find-match", "find-match-other", "word-highlight", "word-highlight-write")
ANCHORS = {name: k.oklch_of(k.CORNERS[slot])[2] for name, slot in k.COLOR_KEYS.items() if slot in k.CORNERS}
WCAG_THRESHOLDS = (3.0, 4.5, 7.0)   # compared strictly: a measured 4.496 does not meet 4.5
# Quality floors (construction.md §10.1). Two levels:
# MINIMUMS: the Twilight Theme standard for each category. Every flavor of the category meets them, a new flavor included,
#   and they never go down.
# FLOORS: what each flavor reaches today, guarding it against regressions. A flavor floor may go down only when the
#   latest CHANGELOG entry names the check, in backticks, under "### Lower", and the new floor still meets the
#   category minimum (SKILL.md, area C).
BODY_TARGET = 49 / 4.5                                    # construction.md §3.5
MINIMUMS = {
    "dark": {"ink on surfaces": BODY_TARGET, "body on surfaces": BODY_TARGET, "subtle on surfaces": 7.00,
             "faint on surfaces": 4.50, "control on surfaces": 3.00, "code on code surfaces": 7.00,
             "on-accent on accent/pressed": 4.50, "accent-text on raised": 7.00, "accent-focus on surfaces": 3.00,
             "ΔE code+cursor, normal": 0.080, "ΔE code+cursor, worst CVD": 0.040, "faint on transient states": 4.50,
             "every state from Canvas (JND)": 2.0, "closest pair of states (JND)": 1.0, "subtle on edge": 4.50,
             "chip label on accent-text": 4.50, "ΔE other series, every vision": 0.040, "neutral states, closest pair (JND)": 1.0, "semantic on surfaces and edge": 3.00,
             "faint from semantic colors (JND)": 1.0, "ΔE ANSI colors, every vision": 0.010, "ΔE Ember from Afterglow": 0.080,
             "ΔE scale steps, normal": 0.080, "ΔE scale steps, worst CVD": 0.040, "scale cell labels": 4.50},
    "light": {"ink on surfaces": BODY_TARGET, "body on surfaces": BODY_TARGET, "subtle on surfaces": 7.00,
              "faint on surfaces": 4.50, "control on surfaces": 3.00, "code on code surfaces": 4.50,
              "on-accent on accent/pressed": 4.50, "accent-text on raised": 4.50, "accent-focus on surfaces": 3.00,
              "ΔE code+cursor, normal": 0.080, "ΔE code+cursor, worst CVD": 0.040, "faint on transient states": 4.50,
              "every state from Canvas (JND)": 2.0, "closest pair of states (JND)": 1.0, "subtle on edge": 4.50,
              "chip label on accent-text": 4.50, "ΔE other series, every vision": 0.040, "neutral states, closest pair (JND)": 1.0, "semantic on surfaces and edge": 3.00,
              "faint from semantic colors (JND)": 1.0, "ΔE ANSI colors, every vision": 0.010, "ΔE Ember from Afterglow": 0.080,
              "ΔE scale steps, normal": 0.080, "ΔE scale steps, worst CVD": 0.040, "scale cell labels": 4.50},
}
FLOORS = {
    "dusk": {"ink on surfaces": 13.25, "body on surfaces": 10.90, "subtle on surfaces": 7.00, "faint on surfaces": 4.50,
             "control on surfaces": 3.00, "code on code surfaces": 7.00, "on-accent on accent/pressed": 4.50,
             "accent-text on raised": 7.00, "accent-focus on surfaces": 3.00, "ΔE code+cursor, normal": 0.097,
             "ΔE code+cursor, worst CVD": 0.061, "faint on transient states": 4.50, "subtle on edge": 5.26,
             "chip label on accent-text": 8.94, "ΔE other series, every vision": 0.158,
             "semantic on surfaces and edge": 4.50, "ΔE ANSI colors, every vision": 0.020,
             "ΔE Ember from Afterglow": 0.216, "ΔE scale steps, normal": 0.114, "ΔE scale steps, worst CVD": 0.078,
             "scale cell labels": 5.22},
    "dawn": {"ink on surfaces": 12.84, "body on surfaces": 10.89, "subtle on surfaces": 7.00, "faint on surfaces": 4.50,
             "control on surfaces": 3.00, "code on code surfaces": 4.50, "on-accent on accent/pressed": 4.50,
             "accent-text on raised": 4.50, "accent-focus on surfaces": 3.00, "ΔE code+cursor, normal": 0.088,
             "ΔE code+cursor, worst CVD": 0.040, "faint on transient states": 4.50, "subtle on edge": 5.42,
             "chip label on accent-text": 5.46, "ΔE other series, every vision": 0.078,
             "semantic on surfaces and edge": 3.19, "ΔE ANSI colors, every vision": 0.019,
             "ΔE Ember from Afterglow": 0.360, "ΔE scale steps, normal": 0.095, "ΔE scale steps, worst CVD": 0.052,
             "scale cell labels": 4.71},
}
CHECKS = list(MINIMUMS["dark"])
# Known limits (construction.md §11) are measured minimums too.
LIMITS = ("JND " + s for s in (*TRANSIENT, "diff-inserted", "diff-removed"))
LIMITS = (*LIMITS, "ANSI black/white on canvas", "min ΔE between background states")
LIMIT_FLOORS = {  # the measured minimum of each limit per flavor (truncated to 4 decimals), current as of 1.11.0
    "dusk": {"JND selection": 4.61, "JND selection-inactive": 2.9143, "JND find-match": 4.0626,
             "JND find-match-other": 2.0054, "JND word-highlight": 2.0129, "JND word-highlight-write": 3.2519,
             "JND diff-inserted": 2.021, "JND diff-removed": 2.0341, "ANSI black/white on canvas": 1.5669,
             "min ΔE between background states": 0.0215},
    "dawn": {"JND selection": 3.45, "JND selection-inactive": 2.0513, "JND find-match": 4.7366,
             "JND find-match-other": 2.04, "JND word-highlight": 2.0486, "JND word-highlight-write": 3.7854,
             "JND diff-inserted": 2.0762, "JND diff-removed": 2.0586, "ANSI black/white on canvas": 1.5774,
             "min ΔE between background states": 0.0202},
}


# Snapshot: the working tree, or a git ref ----------------------------------
# Files that moved, new path -> old path, so a base ref from before the move still reads.
MOVED = {"docs/design-system/color.md": "docs/design-system.md",
         "docs/construction/color.md": "docs/construction.md"}


class Snap:
    def __init__(self, ref=None):
        self.ref = ref
        args = ["ls-tree", "-r", "--name-only", ref] if ref else ["ls-files", "--cached", "--others", "--exclude-standard"]
        self.files = set(git(*args).splitlines())

    def read(self, path):
        if self.ref and path not in self.files and MOVED.get(path) in self.files:
            path = MOVED[path]
        return git("show", f"{self.ref}:{path}") if self.ref else (ROOT / path).read_text()

    def label(self):
        return self.ref or "working tree"


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout


# Measurements ---------------------------------------------------------------
def worst_cvd(cols):
    return min(k.sim(a, v).delta_e(k.sim(b, v), method="ok")
               for v in k.VISIONS[1:] for i, a in enumerate(cols) for b in cols[i + 1:])


def chip_label(n):
    """The neutral farthest from Ink: Shell in a dark flavor, Canvas in a light one (design-system.md §8)."""
    return max(n.values(), key=lambda x: k.contrast(x, n["ink"]))


# design-system.md §12.3: on each parent surface, the fills a row or a bounded control can take.
NEUTRAL_STATES = [(("rail", "canvas"), ("raised", "selection-inactive", "selection")),   # rows
                  (("shell", "raised"), ("selection-inactive", "selection")),
                  (("rail", "canvas"), ("raised", "edge")),                               # buttons
                  (("shell", "raised"), ("edge",))]


def neutral_states(n, s):
    """Smallest distance, in JND, between any two fills of one parent surface in NEUTRAL_STATES (the parent included)."""
    tone = lambda t: n.get(t) or s[t]
    return min(k.de_ok(tone(a), tone(b)) for parents, fills in NEUTRAL_STATES for p in parents
               for a, b in itertools.combinations((p, *fills), 2)) / k.JND


def scale_measures(F):
    """design-system.md §12.4: adjacent cells of both scales, and the two cells at the same distance from a diverging
    scale's middle, against the code colors' separation; the best label (Ink or the chip label) on every colored cell."""
    if "scales" not in F:                         # snapshots before 1.12 have no scales
        return {}
    n, (seq, div) = F["neutrals"], (F["scales"]["sequential"], F["scales"]["diverging"])
    bg, h = n["canvas"], len(div) // 2
    pairs = list(zip([bg] + seq, seq)) + list(zip(div, div[1:])) + [(div[h - 1 - i], div[h + 1 + i]) for i in range(h)]
    labels = (n["ink"], chip_label(n))
    return {"ΔE scale steps, normal": min(k.de_ok(a, b) for a, b in pairs),
            "ΔE scale steps, worst CVD": min(k.sim(a, v).delta_e(k.sim(b, v), method="ok") for v in k.VISIONS[1:] for a, b in pairs),
            "scale cell labels": min(max(k.contrast(x, y) for y in labels) for x in seq + div[:h] + div[h + 1:])}


def measure(F):
    """Every area-C number for one flavor, plus the tracked known limits."""
    n, c, s, A = F["neutrals"], F["colors"], F["states"], F["accents"]
    cr = k.contrast
    on_surf = lambda x: min(cr(x, n[y]) for y in SURF)
    code_surf = [n["canvas"], s["diff-inserted"], s["diff-removed"]]
    cvd = [c[x] for x in CVD_SET] + [A["afterglow"]["accent-focus"]]
    m = {
        "ink on surfaces": on_surf(n["ink"]), "body on surfaces": on_surf(n["body"]),
        "subtle on surfaces": on_surf(n["subtle"]), "faint on surfaces": on_surf(n["faint"]),
        "control on surfaces": on_surf(n["control"]),
        "code on code surfaces": min(cr(c[x], y) for x in CODE for y in code_surf),
        "on-accent on accent/pressed": min(cr(a["on-accent"], a[t]) for a in A.values() for t in ("accent", "accent-pressed")),
        "accent-text on raised": min(cr(a["accent-text"], n["raised"]) for a in A.values()),
        "accent-focus on surfaces": min(on_surf(a["accent-focus"]) for a in A.values()),
        "ΔE code+cursor, normal": min(k.de_ok(a, b) for i, a in enumerate(cvd) for b in cvd[i + 1:]),
        "ΔE code+cursor, worst CVD": worst_cvd(cvd),
        "faint on transient states": min(cr(n["faint"], s[x]) for x in TRANSIENT),
        "every state from Canvas (JND)": min(k.de_ok(v, n["canvas"]) for v in s.values()) / k.JND,
        "closest pair of states (JND)": min(k.de_ok(a, b) for a, b in itertools.combinations(s.values(), 2)) / k.JND,
        "subtle on edge": cr(n["subtle"], n["edge"]),
        "chip label on accent-text": min(cr(chip_label(n), a["accent-text"]) for a in A.values()),
        "ΔE other series, every vision": min(k.worst_de([c[x], n[k.SERIES_OTHER]]) for x in k.SERIES),
        "neutral states, closest pair (JND)": neutral_states(n, s),
        "semantic on surfaces and edge": min(cr(c[x], n[y]) for x in SEMANTIC for y in (*SURF, "edge")),
        "faint from semantic colors (JND)": min(k.worst_de([c[x], n["faint"]]) for x in SEMANTIC) / k.JND,
        "ΔE ANSI colors, every vision": k.worst_de(F["ansi"][1:7] + F["ansi"][9:15]),
        "ΔE Ember from Afterglow": k.de_ok(c["ember"], c["afterglow"]),
        **scale_measures(F),
    }
    limits = {f"JND {x}": k.de_ok(v, n["canvas"]) / 0.02 for x, v in s.items()}
    limits["ANSI black/white on canvas"] = min(cr(F["ansi"][0], n["canvas"]), cr(F["ansi"][7], n["canvas"]))
    sv = list(s.values())
    limits["min ΔE between background states"] = min(k.de_ok(a, b) for i, a in enumerate(sv) for b in sv[i + 1:])
    per_accent = {name: dict(label=cr(a["on-accent"], a["accent"]), pressed=cr(a["on-accent"], a["accent-pressed"]),
                             text=cr(a["accent-text"], n["raised"]), focus=on_surf(a["accent-focus"]))
                  for name, a in A.items()}
    return m, limits, per_accent


def decimals(x):
    return len(f"{x}".split(".")[1]) if "." in f"{x}" else 0


def passes(value, floor):
    """WCAG thresholds and the text targets are strict. Other floors are met at their stated precision: two decimals
    for contrast (13.76), three for ΔE (0.054, 0.040; a float drops the trailing zero, so ΔE always uses three)."""
    if floor in WCAG_THRESHOLDS or floor == BODY_TARGET:
        return value >= floor
    return round(value, 3 if floor < 1 else max(2, decimals(floor))) >= floor


def fmt(x, floor=None):
    return f"{x:.3f}" if (floor or x) < 1 else f"{x:.2f}"


# Structural rules -------------------------------------------------------------
def all_hexes(F):
    out = [*F["neutrals"].values(), *F["colors"].values(), *F["states"].values(), *F["ansi"]]
    out += [v for s in F.get("scales", {}).values() for v in s]
    return out + [v for a in F["accents"].values() for v in a.values() if isinstance(v, str)]


def underscore_keys(obj, path=""):
    if isinstance(obj, dict):
        for key, v in obj.items():
            if key.startswith("_"):
                yield f"{path}.{key}".lstrip(".")
            yield from underscore_keys(v, f"{path}.{key}")


def rules(F, flavor):
    errs = []
    if bad := {h for h in all_hexes(F) if h.lower() in ("#000000", "#ffffff")}:
        errs.append(f"{flavor}: pure black/white {sorted(bad)}")
    for c, anchor in ANCHORS.items():
        d = abs((k.oklch_of(F["colors"][c])[2] - anchor + 180) % 360 - 180)
        if d > k.FREEDOM:
            errs.append(f"{flavor}: {c} hue {d:.1f}° from its ANSI anchor (max {k.FREEDOM}°)")
    eh = k.oklch_of(F["colors"]["ember"])[2]
    if not k.EMBER_HUE[0] <= eh <= k.EMBER_HUE[1]:
        errs.append(f"{flavor}: ember hue {eh:.1f}° outside {k.EMBER_HUE[0]}–{k.EMBER_HUE[1]}°")
    if F["colors"]["afterglow"].lower() != k.AFTERGLOW or F["accents"]["afterglow"]["accent"].lower() != k.AFTERGLOW:
        errs.append(f"{flavor}: afterglow must equal the cusp of the seed hue {k.AFTERGLOW}")
    for name, fam in F["accents"].items():
        if fam["accent"].lower() != F["colors"][name].lower():
            errs.append(f"{flavor}: accents.{name}.accent differs from colors.{name}")
    brights = [k.bright(x, F["neutrals"]["ink"]) for x in F["ansi"][1:7]]
    for i, (want, got) in enumerate(zip(brights, F["ansi"][9:15]), 9):
        if want != got.lower():
            errs.append(f"{flavor}: ansi[{i}] is {got}, the bright rule (§6.7, step {k.BRIGHT_STEP}) gives {want}")
    n = F["neutrals"]
    Lc = k.oklch_of(n["canvas"])[0]
    for name, hx in F["states"].items():          # construction.md §9.2: chroma bounded by Canvas's lightness
        _, C, h = k.oklch_of(hx)
        if C > k.cmax(round(Lc, 3), round(h, 1)) + 0.002:
            errs.append(f"{flavor}: state {name} chroma {C:.4f} exceeds what sRGB holds at Canvas's lightness")
    ink, body = (min(k.contrast(n[x], n[y]) for y in SURF) for x in ("ink", "body"))
    if ink <= body:
        errs.append(f"{flavor}: Ink ({ink:.2f}:1) must contrast more than Body ({body:.2f}:1) on every surface")
    return errs


def series_rules(raw):
    """design-system.md §12.4: the published series order is the decided one, and the search of construction.md §7.1
    on SERIES_BASIS still returns it."""
    errs, want = [], {"order": list(k.SERIES), "other": k.SERIES_OTHER}
    if raw.get("series") != want:
        errs.append(f"series is {raw.get('series')}, construct.py decides {want}")
    basis = {f: raw["flavors"][f] for f in k.BRIGHT_BASIS if f in raw["flavors"]}
    if len(basis) == len(k.BRIGHT_BASIS) and (got := k.bright_step(basis)) != k.BRIGHT_STEP:
        errs.append(f"bright step search on {', '.join(k.BRIGHT_BASIS)} gives {got}, construct.py has {k.BRIGHT_STEP}")
    import syntax_roles
    if (got := syntax_roles.assignment()) != k.SYNTAX:
        errs.append(f"syntax roles from syntax/stats.json give {got}, construct.py has {k.SYNTAX}")
    manifest = json.loads((Path(syntax_roles.STATS).parent / "manifest.json").read_text())
    for p in manifest["packages"]:
        ok = set(manifest["accepted_licenses"])
        if not (set(p["license_files"].values()) <= ok or (" OR " in p["license"] and set(p["license_files"].values()) & ok)):
            errs.append(f"syntax corpus: {p['name']} is not under an accepted license")
    basis = {f: raw["flavors"][f] for f in k.SCALE_BASIS if f in raw["flavors"]}
    if len(basis) == len(k.SCALE_BASIS) and (got := k.scale_search(basis)) != (k.SEQUENTIAL, k.DIVERGING):
        errs.append(f"scale search on {', '.join(k.SCALE_BASIS)} gives {got}, construct.py has {(k.SEQUENTIAL, k.DIVERGING)}")
    basis = {f: raw["flavors"][f] for f in k.SERIES_BASIS if f in raw["flavors"]}
    if len(basis) == len(k.SERIES_BASIS) and (got := k.series_order(basis)) != k.SERIES:
        errs.append(f"series search on {', '.join(k.SERIES_BASIS)} gives {', '.join(got)}, not the decided order")
    return errs


_REBUILD = None


def rebuild():
    """construct.py from its decided parameters; cached for the whole run."""
    global _REBUILD
    if _REBUILD is None:
        _REBUILD = k.build_palette()
    return _REBUILD


def robustness(P, restarts=20):
    """§6.5 is a local search. Rebuilt with twice the restarts, every flavor must come out the same; a flavor that
    changes sits on an optimum that more search can leave (SKILL.md, area D)."""
    saved = k.OPT_RESTARTS
    k.OPT_RESTARTS = restarts
    try:
        built, _ = k.build_palette()
    finally:
        k.OPT_RESTARTS = saved
    return [f"{f}: with {restarts} optimizer restarts the rebuild differs ({', '.join(t for t in P[f]['colors'] if P[f]['colors'][t] != built[f]['colors'][t]) or 'states or accents'})"
            for f in P if f in built and built[f] != P[f]]


def order_check(P):
    """construction.md §9.4: the transient states do not depend on their build order. Rebuilt in reverse order from the
    published colors and diff lines, every flavor must give its published states."""
    errs = []
    for f in P:
        if f not in k.FLAVORS:
            continue
        N, Pr, c, s = k.neutrals(f), k.PROFILES[f], P[f]["colors"], P[f]["states"]
        h = lambda x: k.oklch_of(x)[2]
        sources = {"selection": h(k.AFTERGLOW), "selection-inactive": h(k.AFTERGLOW), "find-match": h(c["gold"]),
                   "find-match-other": h(c["gold"]), "word-highlight": h(c["sea-salt"]), "word-highlight-write": h(c["sea-salt"])}
        rev = k.transient_states(N, Pr, sources, [s["diff-inserted"], s["diff-removed"]], order=list(reversed(sources)))
        errs += [f"{f} {n}: built in reverse order it is {x}, published {s[n]} (the order of §9.4 matters)" for n, x in rev.items() if x != s[n]]
    return errs


def reproduce(P):
    """Every published value must equal the rebuild exactly. Any difference is a hand edit or an undocumented method change."""
    built, meta = rebuild()
    errs = order_check(P)
    for f in P:
        if f not in built:
            errs.append(f"{f}: flavor has no construction in construct.py (a new flavor must be built, not typed)")
            continue
        pub, b = P[f], built[f]
        pairs = [(f"{g}.{t}", pub[g].get(t), b[g].get(t)) for g in ("neutrals", "colors", "states") for t in set(pub[g]) | set(b[g])]
        pairs += [(f"accents.{a}.{t}", pub["accents"].get(a, {}).get(t), b["accents"].get(a, {}).get(t))
                  for a in set(pub["accents"]) | set(b["accents"]) for t in ("accent", "accent-text", "accent-pressed", "accent-focus", "on-accent")]
        pairs += [(f"ansi.{i}", pub["ansi"][i] if i < len(pub["ansi"]) else None, b["ansi"][i]) for i in range(16)]
        for name, cells in b["scales"].items():
            got = pub.get("scales", {}).get(name, [])
            pairs += [(f"scales.{name}[{i}]", got[i] if i < len(got) else None, x) for i, x in enumerate(cells)]
        for tok, p, q in pairs:
            if (p or "").lower() != (q or "").lower():
                errs.append(f"{f} {tok}: published {p}, rebuilt {q}")
    return errs, meta


def construction_checks(snap, P, meta):
    """Numbers in construction.md that the rebuild determines: the §6.5 hue table and L₀."""
    errs = []
    text = snap.read("docs/construction/color.md")
    rows = {"Coral": "red", "Gold": "yellow", "Grove": "green", "Sea Salt": "cyan", "Sky": "blue", "Orchid": "magenta"}
    cols = {}                                     # §6.5 hue table: flavor → column, from its header row
    for no, line in enumerate(text.splitlines(), 1):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[:2] == ["Hue", "Anchor"]:
            cols = {c.lower(): i for i, c in enumerate(cells) if meta and c.lower() in meta}
            continue
        if not cols or not meta:
            continue
        if cells and cells[0] in rows:
            i = list(k.ANCHORS).index(rows[cells[0]])
            for f, col in cols.items():
                want = f"{meta[f]['hues'][i]}°"
                if cells[col] != want:
                    errs.append(f"docs/construction/color.md:{no}: {cells[0]} {f} hue shows {cells[col]}, rebuilt {want}")
        elif cells and cells[0] == "Ember":
            for f, col in cols.items():
                if cells[col] != f"{meta[f]['ember'][0]}°":
                    errs.append(f"docs/construction/color.md:{no}: Ember {f} hue shows {cells[col]}, rebuilt {meta[f]['ember'][0]}°")
        elif cells and cells[0].startswith("L₀"):
            for f, col in cols.items():
                if cells[col] != f"{meta[f]['L0']:.3f}":
                    errs.append(f"docs/construction/color.md:{no}: L₀ {f} shows {cells[col]}, rebuilt {meta[f]['L0']:.3f}")
            cols = {}
    allhex = {h.lower() for f in P for h in all_hexes(P[f])} | {k.SEED}   # the seed is documented, not a token
    for no, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):          # prose may cite historical values; tables state current ones
            continue
        for h in HEX.findall(line):
            if "#" + h.lower() not in allhex:
                errs.append(f"docs/construction/color.md:{no}: #{h} is not in palette/twilight.json")
    return errs


# Documents -------------------------------------------------------------------
HEX = re.compile(r"#([0-9a-fA-F]{6})\b")
SWATCH = re.compile(r'placehold\.co/\d+x\d+/([0-9a-fA-F]{6})/([0-9a-fA-F]{6})"[^>]*alt="#([0-9a-fA-F]{6})"')
NUM = re.compile(r"(?<![#\w])(\d+\.\d+)")


def token_of(cell):
    return re.sub(r"[`*]", "", cell).strip().lower().replace(" ", "-")


def doc_checks(snap, P, M):
    """Hexes, swatches and numbers in README.md and design-system.md against the JSON and the measurements."""
    errs = []
    allhex = {h.lower() for f in P for h in all_hexes(P[f])} | {k.SEED}   # the seed is documented, not a token
    for path in ("README.md", "docs/design-system/color.md"):
        flavor, section = None, ""
        for no, line in enumerate(snap.read(path).splitlines(), 1):
            where = f"{path}:{no}"
            if line.startswith("#"):
                section = line.lower()
            if m := re.search(rf"(?:^#+ |<b>)({'|'.join(P)})\b", line, re.I):
                flavor = m.group(1).lower()
            elif line.startswith("## "):                                        # a new section names no flavor
                flavor = None
            for a, b, alt in SWATCH.findall(line):
                if not a.lower() == b.lower() == alt.lower():
                    errs.append(f"{where}: swatch {a}/{b} labelled #{alt}")
            for h in HEX.findall(line):
                if "#" + h.lower() not in allhex and h.lower() not in ("000000", "ffffff"):
                    errs.append(f"{where}: #{h} is not in palette/twilight.json")
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if line.startswith("|") and "guarantee" in section and len(cells) == 3:
                errs += guarantee_check(where, cells, M)
            elif line.startswith("|") and flavor:
                errs += row_checks(where, line, flavor, section, P, M)
    return errs


def row_checks(where, line, flavor, section, P, M):
    errs = []
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    vals = [h.lower() for h in re.findall(r"`(#[0-9a-fA-F]{6})`", line)]
    F, (m, limits, per_accent) = P[flavor], M[flavor]
    names = [token_of(c) for c in cells]
    tok = next((t for t in names if t in F["neutrals"] or t in F["colors"] or t in F["states"]), None)
    expect = lambda got, want, what: errs.append(f"{where}: {what} is {got}, JSON has {want}") if got != want else None
    if cells[0].isdigit() and vals:                                           # terminal table
        expect(vals[0], F["ansi"][int(cells[0])].lower(), f"{flavor} ansi[{cells[0]}]")
        errs += num_check(where, cells[-1], k.contrast(F["ansi"][int(cells[0])], F["neutrals"]["canvas"]), "on Canvas")
    elif tok in F["accents"] and len(vals) == 5:                              # accent token table
        for t, v in zip(("accent", "accent-text", "accent-pressed", "accent-focus", "on-accent"), vals):
            expect(v, F["accents"][tok][t].lower(), f"{flavor} {tok}.{t}")
    elif tok in F["accents"] and len(vals) == 2 and "accent" in section:      # README accents: Dusk | Dawn
        for f, v in zip(P, vals):
            expect(v, P[f]["colors"][tok].lower(), f"{f} {tok}")
    elif tok in per_accent and not vals and len(cells) == 5:                  # accent contrast table
        for c, key in zip(cells[1:], ("label", "pressed", "text", "focus")):
            errs += num_check(where, c, per_accent[tok][key], f"{flavor} {tok} {key}")
    elif tok and vals:                                                        # neutral / color / state row
        group = next(g for g in ("neutrals", "colors", "states") if tok in F[g])
        expect(vals[0], F[group][tok].lower(), f"{flavor} {tok}")
        if rgb := re.search(r"rgb\((\d+), (\d+), (\d+)\)", line):                # README RGB column
            expect("#" + "".join(f"{int(x):02x}" for x in rgb.groups()), vals[0], f"{flavor} {tok} rgb()")
        if lch := re.search(r"oklch\(([\d.]+)% ([\d.]+) ([\d.]+)\)", line):     # OKLCH column, at shown precision
            L, C, h = k.oklch_of(vals[0])
            shown = (lch.group(1), lch.group(2), lch.group(3))
            want = (f"{L * 100:.1f}", f"{C:.3f}", f"{h:.1f}" if C >= 0.002 else shown[2])  # hue undefined near neutral (§11)
            expect(" ".join(shown), " ".join(want), f"{flavor} {tok} oklch() (computed from {vals[0]})")
        rest = cells[names.index(tok) + 3:] if "`" in cells[names.index(tok)] else []
        n = F["neutrals"]
        if group == "neutrals" and len(rest) >= 4:
            for c, s in zip(rest, SURF):
                errs += num_check(where, c, k.contrast(F[group][tok], n[s]), f"{tok} vs {s}")
        if group == "colors" and len(rest) >= 2:
            errs += num_check(where, rest[0], k.contrast(F[group][tok], n["canvas"]), f"{tok} on canvas")
            if tok != "afterglow":
                worst = min(k.contrast(F[group][tok], x) for x in (n["canvas"], F["states"]["diff-inserted"], F["states"]["diff-removed"]))
                errs += num_check(where, rest[1], worst, f"{tok} worst code surface")
        if group == "states" and (jnd := re.search(r"(\d+\.\d) JND", line)):
            errs += num_check(where, jnd.group(1), limits[f"JND {tok}"], f"{tok} visibility (JND)")
    return errs


GUARANTEE = [  # (words in the row label, measurement); the first match wins, so specific rows come first
    (("subtle", "edge"), "subtle on edge"), (("semantic", "surface"), "semantic on surfaces and edge"),
    (("faint", "semantic"), "faint from semantic colors (JND)"),
    (("terminal",), "ΔE ANSI colors, every vision"), (("ember", "afterglow"), "ΔE Ember from Afterglow"),
    (("scale", "normal"), "ΔE scale steps, normal"), (("scale", "deficiency"), "ΔE scale steps, worst CVD"),
    (("scale", "label"), "scale cell labels"), (("accent-text",), "chip label on accent-text"),
    (("other series",), "ΔE other series, every vision"), (("neutral", "states"), "neutral states, closest pair (JND)"),
    (("ink",), "ink on surfaces"), (("body",), "body on surfaces"), (("subtle",), "subtle on surfaces"),
    (("faint",), "faint on surfaces"), (("control", "focus"), ("control on surfaces", "accent-focus on surfaces")),
    (("control",), "control on surfaces"), (("focus",), "accent-focus on surfaces"),
    (("code colors",), "code on code surfaces"), (("normal vision",), "ΔE code+cursor, normal"),
    (("deficiency",), "ΔE code+cursor, worst CVD"),
]


def guarantee_check(where, cells, M):
    label = cells[0].lower()
    for words, key in GUARANTEE:
        if all(w in label for w in words):
            keys = key if isinstance(key, tuple) else (key,)
            out = []
            for cell, f in zip(cells[1:], M):
                out += num_check(where, cell, min(M[f][0][x] for x in keys), f"{f} guarantee '{cells[0]}'")
            return out
    return []


def num_check(where, cell, value, what):
    m = NUM.search(cell)
    if not m:
        return []
    shown = m.group(1)
    want = f"{value:.{len(shown.split('.')[1])}f}"
    return [] if want == shown else [f"{where}: {what} shows {shown}, measured {want}"]


def link_checks(snap):
    errs, anchors = [], {}
    mds = sorted(f for f in snap.files if f.endswith(".md"))

    def heads(path):
        if path not in anchors:
            seen, out = {}, set()
            for line in snap.read(path).splitlines():
                if m := re.match(r"#{1,6} (.+)", line):
                    s = re.sub(r"[^\w\- ]", "", m.group(1).strip().lower()).replace(" ", "-")
                    out.add(s if s not in seen else f"{s}-{seen[s]}")
                    seen[s] = seen.get(s, 0) + 1
            anchors[path] = out
        return anchors[path]

    for path in mds:
        text = re.sub(r"```.*?```", "", snap.read(path), flags=re.S)
        base = Path(path).parent
        for target in re.findall(r"\]\(([^)\s]+)\)|(?:href|src|srcset)=\"([^\"]+)\"", text):
            target = target[0] or target[1]
            if re.match(r"[a-z]+:", target):
                continue
            file, _, anchor = target.partition("#")
            dest = str((base / file).as_posix()) if file else path
            dest = str(Path(dest)).replace("\\", "/")
            dest = "/".join(p for p in _norm(dest))
            if file and dest not in snap.files and not any(f.startswith(dest.rstrip("/") + "/") for f in snap.files):
                errs.append(f"{path}: broken link {target}")
            elif anchor and dest.endswith(".md") and anchor not in heads(dest):
                errs.append(f"{path}: missing anchor {target}")
    return errs


def _norm(p):
    out = []
    for part in p.split("/"):
        if part == "..":
            out.pop()
        elif part not in ("", "."):
            out.append(part)
    return out


SCRIPT = ".agents/skills/twilight-auditor/scripts/validate.py"


def minimum_tables(snap):
    """FLOORS, LIMIT_FLOORS and MINIMUMS as written in the snapshot's own validate.py (None when absent).
    FLOORS is returned per flavor; before 1.6 it was a table of (dusk, dawn) pairs."""
    if SCRIPT not in snap.files:
        return None, None, None
    found = {}
    for node in ast.parse(snap.read(SCRIPT)).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("FLOORS", "LIMIT_FLOORS", "MINIMUMS"):
                try:
                    found[name] = ast.literal_eval(node.value)
                except ValueError:                      # MINIMUMS refers to BODY_TARGET
                    found[name] = eval(compile(ast.Expression(node.value), SCRIPT, "eval"), {"BODY_TARGET": BODY_TARGET})
    F = found.get("FLOORS")
    if F and isinstance(next(iter(F.values())), tuple):
        F = {flavor: {c: v[i] for c, v in F.items()} for i, flavor in enumerate(("dusk", "dawn"))}
    return F, found.get("LIMIT_FLOORS"), found.get("MINIMUMS")


def lower_section(text, since=None):
    """The '### Lower' sections of the CHANGELOG entries newer than version `since` (only the latest entry when
    `since` is None), joined; "" when there is none. A change spanning several versions declares each lowering in
    the entry of the version that made it."""
    vkey = lambda v: tuple(int(x) for x in v.split("."))
    out = []
    for i, entry in enumerate(re.split(r"^## (?=\d+\.\d+\.\d+)", text, flags=re.M)[1:]):
        version = entry.split(None, 1)[0]
        if (since is None and i > 0) or (since is not None and vkey(version) <= vkey(since)):
            break
        if m := re.search(r"^### Lower\b.*?(?=^### |\Z)", entry, flags=re.M | re.S):
            out.append(m.group(0))
    return "\n".join(out)


def declared(lower, name):
    """A lowered minimum is declared when the Lower section names its check in backticks."""
    return f"`{name}`" in lower


def version_checks(snap, P_raw):
    errs = [f"palette/twilight.json: internal key {key}" for key in underscore_keys(P_raw)]
    latest = next((m.group(1) for line in snap.read("CHANGELOG.md").splitlines() if (m := re.match(r"## (\d+\.\d+\.\d+)", line))), None)
    if P_raw.get("version") != latest:
        errs.append(f"palette/twilight.json version {P_raw.get('version')} != latest CHANGELOG.md {latest}")
    return errs


# Run ---------------------------------------------------------------------------
def run(snap, json_path="palette/twilight.json", do_rebuild=True):
    raw = json.loads(snap.read(json_path) if snap.ref or not Path(json_path).is_absolute() else Path(json_path).read_text())
    P = raw["flavors"]
    M = {f: measure(P[f]) for f in P}
    category = {f: k.FLAVORS[f]["category"] if f in k.FLAVORS else
                ("dark" if k.oklch_of(P[f]["neutrals"]["canvas"])[0] < 0.5 else "light") for f in P}
    floors = []
    for c in CHECKS:
        for f in P:
            if c not in M[f][0]:                       # a check the snapshot predates
                continue
            v, mn, fl = M[f][0][c], MINIMUMS[category[f]][c], FLOORS.get(f, {}).get(c)
            ok_min, ok_fl = passes(v, mn), fl is None or passes(v, fl)
            floors.append(dict(flavor=f, check=c, value=v, minimum=mn, floor=fl, ok=ok_min and ok_fl,
                               fails=[x for x, ok in (("minimum", ok_min), ("flavor floor", ok_fl)) if not ok]))
    repro_errs, meta = reproduce(P) if do_rebuild else (["skipped (--no-rebuild): values were not reproduced"], None)
    return dict(
        snapshot=snap.label(), floors=floors, limits={f: M[f][1] for f in P},
        rules=[e for f in P for e in rules(P[f], f)] + series_rules(raw), reproduction=repro_errs,
        consistency=version_checks(snap, raw) + doc_checks(snap, P, M) + construction_checks(snap, P, meta) + link_checks(snap)
                    + floor_table_checks(P, category) + generated_checks(snap, P),
        palette=P, tables=minimum_tables(snap), changelog=snap.read("CHANGELOG.md"), version=raw.get("version"),
    )


def generated_checks(snap, P):
    """Tables, measured figures in prose and the palette images must equal what scripts/docs.py renders."""
    import docs
    errs = docs.document_errors(snap.read, P)
    if not snap.ref:                                  # images are read from the working tree
        errs += docs.image_errors(P)
    return errs


def floor_table_checks(P, category):
    """Every flavor has floors and limit floors, and no flavor floor sits below its category minimum."""
    errs = []
    for f in P:
        if f not in FLOORS or f not in LIMIT_FLOORS:
            errs.append(f"{f}: no FLOORS or LIMIT_FLOORS entry (a new flavor's measured values become its floors)")
            continue
        for c, v in FLOORS[f].items():
            if c in MINIMUMS[category[f]] and v < MINIMUMS[category[f]][c] - 1e-9:
                errs.append(f"{f}: flavor floor {c} {v} is below the {category[f]} minimum {MINIMUMS[category[f]][c]:.3f}")
    return errs


def report(r):
    print(f"# Twilight Theme validation: {r['snapshot']}\n")
    print(f"{'check':34} " + "   ".join(f"{f:>8} {'floor':>7} {'min':>7}" for f in r["palette"]))
    for c in CHECKS:
        row = [x for x in r["floors"] if x["check"] == c]
        cells = "   ".join(f"{fmt(x['value'], x['minimum']):>8} {fmt(x['floor'], x['floor']) if x['floor'] is not None else '—':>7}"
                           f" {fmt(x['minimum'], x['minimum']):>7}{'' if x['ok'] else ' FAIL ' + '+'.join(x['fails'])}" for x in row)
        print(f"{c:34} {cells}")
    print("\nKnown limits (§11, must not get worse):")
    for key in LIMITS:
        print(f"  {key:34} " + "   ".join(f"{f} {fmt(r['limits'][f][key])}" for f in r["palette"]))
    for title, key in (("Rules", "rules"), ("Reproduction (exact, both flavors)", "reproduction"), ("Consistency", "consistency")):
        print(f"\n{title}: {'none' if not r[key] else ''}")
        for e in r[key]:
            print(f"  - {e}")


def failed(r):
    repro = [e for e in r["reproduction"] if not e.startswith("skipped")]
    return [x for x in r["floors"] if not x["ok"]] + r["rules"] + repro + r["consistency"]


def minimum_changes(base, prop, lines):
    """Changes to the floor tables themselves, base against proposal.
    A category minimum may never go down. A flavor floor or known limit may go down only when a CHANGELOG entry newer
    than the base names its check, in backticks, under '### Lower' (the new floor must still meet the minimum; see
    floor_table_checks). A removed check or table is a regression."""
    out = []
    (bF, bL, bM), (pF, pL, pM) = base["tables"], prop["tables"]
    if bM is not None:
        if pM is None:
            out.append("MINIMUMS removed from validate.py")
        else:
            for cat, checks in bM.items():
                for check, old in checks.items():
                    new = pM.get(cat, {}).get(check)
                    if new is None:
                        out.append(f"minimum removed: {cat} {check}")
                    elif new < old - 1e-12:
                        out.append(f"category minimum lowered: {cat} {check} {old} → {new}")
    if bF is None:
        return out
    if pF is None:
        return out + ["FLOORS removed from validate.py"]
    for flavor, checks in bF.items():
        for check, old in checks.items():
            new = pF.get(flavor, {}).get(check)
            if new is None:
                out.append(f"check removed: {flavor} {check}")
            elif new < old - 1e-12:
                if not declared(prop["lower"], check):
                    out.append(f"flavor floor lowered without `{check}` under Lower in CHANGELOG: {flavor} {old} → {new}")
                else:
                    lines.append(f"flavor floor lowered (declared under Lower): {flavor} {check} {old} → {new}")
    if bL is not None and pL is None:
        return out + ["LIMIT_FLOORS removed from validate.py"]
    for f in sorted(set(base["palette"]) & set(prop["palette"])):
        for key in LIMITS:
            old = bL[f][key] if bL else math.floor(base["limits"][f][key] * 1e4) / 1e4   # LIMIT_FLOORS precision
            new = pL[f][key] if pL else prop["limits"][f][key]
            if new < old - 1e-9:
                if declared(prop["lower"], key):
                    lines.append(f"known limit lowered (declared under Lower): {f} {key} {old} → {new}")
                else:
                    out.append(f"known limit lowered without `{key}` under Lower in CHANGELOG: {f} {old} → {new}")
    return out


def compare(base, prop):
    """Print deltas against the baseline snapshot; return regressions against the current minimums.
    A floor fails when it is below its FLOORS entry; a known limit fails when it is below LIMIT_FLOORS.
    The baseline snapshot is reported for context only: a value may move as long as it stays above its minimum."""
    lines, regressions = [], []
    prop["lower"] = lower_section(prop["changelog"], base["version"])
    old = {(x["flavor"], x["check"]): x for x in base["floors"]}
    for p in prop["floors"]:
        if (b := old.get((p["flavor"], p["check"]))) and abs(d := p["value"] - b["value"]) > 1e-9:
            lines.append(f"{p['flavor']} {p['check']}: {fmt(b['value'])} → {fmt(p['value'])} ({d:+.4f})")
        if not p["ok"]:
            regressions.append(f"below {' and '.join(p['fails'])}: {p['flavor']} {p['check']} {p['value']:.5f}")
    for f in sorted(set(base["palette"]) & set(prop["palette"])):
        for key in LIMITS:
            if f in LIMIT_FLOORS and (p := prop["limits"][f][key]) < LIMIT_FLOORS[f][key]:
                regressions.append(f"known limit below minimum: {f} {key} {fmt(p)} < {LIMIT_FLOORS[f][key]}")
    regressions += minimum_changes(base, prop, lines)
    changed = [f"{f}.{g}.{t}" for f in prop["palette"] for g in ("neutrals", "colors", "states")
               for t, v in prop["palette"][f][g].items() if base["palette"].get(f, {}).get(g, {}).get(t) != v]
    shown = [c for c in changed if c.split(".")[1] in ("neutrals", "colors")]   # what assets/palette-*.png draws
    if changed:
        lines.append(f"changed values: {', '.join(changed)}")
    if shown:
        span = [base["snapshot"], *([prop["snapshot"]] if prop["snapshot"] != "working tree" else [])]
        if not git("diff", "--name-only", *span, "--", "assets/").strip():
            regressions.append("stale assets/palette-*.png: shown values changed, images did not")
    print(f"\n# Compare: {base['snapshot']} → {prop['snapshot']}")
    for line in lines + [f"FAIL {x}" for x in regressions] or ["no differences"]:
        print(f"  - {line}")
    return regressions


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default="palette/twilight.json")
    ap.add_argument("--ref", help="validate a git ref instead of the working tree")
    ap.add_argument("--compare", metavar="REF", help="also report deltas and regressions against REF (usually main)")
    ap.add_argument("--json", action="store_true", help="print only the JSON summary")
    ap.add_argument("--no-rebuild", action="store_true", help="skip reproduction (wording or link changes only)")
    ap.add_argument("--robust", action="store_true", help="also rebuild with 20 optimizer restarts (required for a new flavor)")
    a = ap.parse_args()
    r = run(Snap(a.ref), a.path, not a.no_rebuild)
    if a.robust:
        r["reproduction"] += robustness(r["palette"])
    summary = {key: r[key] for key in ("snapshot", "floors", "limits", "rules", "reproduction", "consistency")}
    if not a.json:
        report(r)
    regressions = []
    if a.compare:
        b = run(Snap(a.compare), do_rebuild=False)
        with contextlib.redirect_stdout(io.StringIO() if a.json else sys.stdout):
            regressions = compare(b, r)
        summary["compare"] = dict(base=a.compare, regressions=regressions,
                                  floors=[dict(check=p["check"], flavor=p["flavor"], base=x["value"], proposal=p["value"])
                                          for x, p in zip(b["floors"], r["floors"])])
    summary["passed"] = not failed(r) and not regressions
    if not a.json:
        print("\n## JSON summary")
    print(json.dumps(summary, ensure_ascii=False, indent=2 if a.json else None))
    sys.exit(0 if summary["passed"] else 1)


if __name__ == "__main__":
    main()