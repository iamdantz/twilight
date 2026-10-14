"""Twilight validator: quality floors, construction reproduction and document consistency.

Usage (from anywhere inside the Twilight repository):
    <skill>/.venv/bin/python <skill>/scripts/validate.py [palette/twilight.json] [--ref REF] [--compare REF] [--json] [--no-rebuild]

The rebuild runs construct.py (both flavors, §6.5 included) once per invocation, about 2 minutes.
--no-rebuild skips it; use only for changes that cannot touch values (wording, links).

Exit status 1 if any floor, consistency or reproduction check fails.
"""
import argparse
import contextlib
import io
import json
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
TRANSIENT = ("selection", "selection-inactive", "find-match", "find-match-other", "word-highlight", "word-highlight-write")
ANCHORS = {name: k.oklch_of(k.CORNERS[slot])[2] for name, slot in k.COLOR_KEYS.items() if slot in k.CORNERS}
WCAG_THRESHOLDS = (3.0, 4.5, 7.0)   # compared strictly: a measured 4.496 does not meet 4.5
FLOORS = {  # check: (dusk, dawn); construction.md §3.5, §5, §6.6, §7, §9.2; design-system.md §13
    "ink on surfaces": (13.76, 13.36), "body on surfaces": (10.90, 10.89), "subtle on surfaces": (7.00, 7.00),
    "faint on surfaces": (4.50, 4.50), "control on surfaces": (3.00, 3.00), "code on code surfaces": (7.00, 4.50),
    "on-accent on accent/pressed": (4.50, 4.50), "accent-text on raised": (7.00, 4.50),
    "accent-focus on surfaces": (3.00, 3.00), "ΔE code+cursor, normal": (0.089, 0.088),
    "ΔE code+cursor, worst CVD": (0.054, 0.040), "faint on transient states": (4.50, 4.50),
}
# Known limits (construction.md §11): no floor, but a proposal may not lower them. A background state that meets its
# JND target (§9.1) counts as the target: the search stops at the first step past it, so the overshoot is incidental.
LIMITS = ("JND " + s for s in (*TRANSIENT, "diff-inserted", "diff-removed"))
LIMITS = (*LIMITS, "ANSI black/white on canvas", "min ΔE between background states")


# Snapshot: the working tree, or a git ref ----------------------------------
class Snap:
    def __init__(self, ref=None):
        self.ref = ref
        args = ["ls-tree", "-r", "--name-only", ref] if ref else ["ls-files", "--cached", "--others", "--exclude-standard"]
        self.files = set(git(*args).splitlines())

    def read(self, path):
        return git("show", f"{self.ref}:{path}") if self.ref else (ROOT / path).read_text()

    def label(self):
        return self.ref or "working tree"


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout


# Measurements ---------------------------------------------------------------
def worst_cvd(cols):
    return min(k.sim(a, v).delta_e(k.sim(b, v), method="ok")
               for v in k.VISIONS[1:] for i, a in enumerate(cols) for b in cols[i + 1:])


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
    """WCAG thresholds are strict. Regression floors (e.g. 13.76, 0.054) are met at their stated precision."""
    if floor in WCAG_THRESHOLDS:
        return value >= floor
    return round(value, max(2, decimals(floor))) >= floor


def fmt(x, floor=None):
    return f"{x:.3f}" if (floor or x) < 1 else f"{x:.2f}"


# Structural rules -------------------------------------------------------------
def all_hexes(F):
    out = [*F["neutrals"].values(), *F["colors"].values(), *F["states"].values(), *F["ansi"]]
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
        if d > 25:
            errs.append(f"{flavor}: {c} hue {d:.1f}° from its ANSI anchor (max 25°)")
    eh = k.oklch_of(F["colors"]["ember"])[2]
    if not 45 <= eh <= 70:
        errs.append(f"{flavor}: ember hue {eh:.1f}° outside 45–70°")
    if F["colors"]["afterglow"].lower() != k.SEED or F["accents"]["afterglow"]["accent"].lower() != k.SEED:
        errs.append(f"{flavor}: afterglow must equal the seed {k.SEED}")
    for name, fam in F["accents"].items():
        if fam["accent"].lower() != F["colors"][name].lower():
            errs.append(f"{flavor}: accents.{name}.accent differs from colors.{name}")
    brights = [k.bright(x, F["neutrals"]["ink"]) for x in F["ansi"][1:7]]
    for i, (want, got) in enumerate(zip(brights, F["ansi"][9:15]), 9):
        if want != got.lower():
            errs.append(f"{flavor}: ansi[{i}] is {got}, the 1/3-toward-Ink rule gives {want}")
    return errs


_REBUILD = None


def rebuild():
    """construct.py from its decided parameters; cached for the whole run."""
    global _REBUILD
    if _REBUILD is None:
        _REBUILD = k.build_palette()
    return _REBUILD


def reproduce(P):
    """Every published value must equal the rebuild exactly. Any difference is a hand edit or an undocumented method change."""
    built, meta = rebuild()
    errs = []
    for f in P:
        if f not in built:
            errs.append(f"{f}: flavor has no construction in construct.py (a new flavor must be built, not typed)")
            continue
        pub, b = P[f], built[f]
        pairs = [(f"{g}.{t}", pub[g].get(t), b[g].get(t)) for g in ("neutrals", "colors", "states") for t in set(pub[g]) | set(b[g])]
        pairs += [(f"accents.{a}.{t}", pub["accents"].get(a, {}).get(t), b["accents"].get(a, {}).get(t))
                  for a in set(pub["accents"]) | set(b["accents"]) for t in ("accent", "accent-text", "accent-pressed", "accent-focus", "on-accent")]
        pairs += [(f"ansi.{i}", pub["ansi"][i] if i < len(pub["ansi"]) else None, b["ansi"][i]) for i in range(16)]
        for tok, p, q in pairs:
            if (p or "").lower() != (q or "").lower():
                errs.append(f"{f} {tok}: published {p}, rebuilt {q}")
    return errs, meta


def construction_checks(snap, P, meta):
    """Numbers in construction.md that the rebuild determines: the §6.5 hue table and L₀."""
    errs = []
    text = snap.read("docs/construction.md")
    rows = {"Coral": "red", "Gold": "yellow", "Grove": "green", "Sea Salt": "cyan", "Sky": "blue", "Orchid": "magenta"}
    for no, line in enumerate(text.splitlines(), 1):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and cells[0] in rows and meta:
            i = list(k.ANCHORS).index(rows[cells[0]])
            for col, f in ((2, "dusk"), (4, "dawn")):
                want = f"{meta[f]['hues'][i]}°"
                if cells[col] != want:
                    errs.append(f"docs/construction.md:{no}: {cells[0]} {f} hue shows {cells[col]}, rebuilt {want}")
        if cells and cells[0] == "Ember" and len(cells) == 6 and meta:
            for col, f in ((2, "dusk"), (4, "dawn")):
                if cells[col] != f"{meta[f]['ember'][0]}°":
                    errs.append(f"docs/construction.md:{no}: Ember {f} hue shows {cells[col]}, rebuilt {meta[f]['ember'][0]}°")
        if cells and cells[0].startswith("L₀") and meta:
            shown = [c for c in cells[1:] if re.fullmatch(r"\d\.\d{3}", c)]
            want = [f"{meta[f]['L0']:.3f}" for f in ("dusk", "dawn")]
            if shown and shown != want:
                errs.append(f"docs/construction.md:{no}: L₀ shows {shown}, rebuilt {want}")
    allhex = {h.lower() for f in P for h in all_hexes(P[f])}
    for no, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):          # prose may cite historical values; tables state current ones
            continue
        for h in HEX.findall(line):
            if "#" + h.lower() not in allhex:
                errs.append(f"docs/construction.md:{no}: #{h} is not in palette/twilight.json")
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
    allhex = {h.lower() for f in P for h in all_hexes(P[f])}
    for path in ("README.md", "docs/design-system.md"):
        flavor, section = None, ""
        for no, line in enumerate(snap.read(path).splitlines(), 1):
            where = f"{path}:{no}"
            if line.startswith("#"):
                section = line.lower()
            if m := re.search(rf"(?:^#+ |<b>)({'|'.join(P)})\b", line, re.I):
                flavor = m.group(1).lower()
            for a, b, alt in SWATCH.findall(line):
                if not a.lower() == b.lower() == alt.lower():
                    errs.append(f"{where}: swatch {a}/{b} labelled #{alt}")
            for h in HEX.findall(line):
                if "#" + h.lower() not in allhex and h.lower() not in ("000000", "ffffff"):
                    errs.append(f"{where}: #{h} is not in palette/twilight.json")
            if line.startswith("|") and flavor:
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
    elif "guarantee" in section and len(cells) == 3:
        errs += guarantee_check(where, cells, M)
    return errs


GUARANTEE = [  # (words in the row label, measurement)
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
    dark = {f: k.oklch_of(P[f]["neutrals"]["canvas"])[0] < 0.5 for f in P}     # a new flavor takes Dusk (dark) or Dawn (light) floors
    floors = [dict(flavor=f, check=c, value=M[f][0][c], floor=FLOORS[c][0 if dark[f] else 1],
                   ok=passes(M[f][0][c], FLOORS[c][0 if dark[f] else 1])) for c in FLOORS for f in P]
    repro_errs, meta = reproduce(P) if do_rebuild else (["skipped (--no-rebuild): values were not reproduced"], None)
    return dict(
        snapshot=snap.label(), floors=floors, limits={f: M[f][1] for f in P},
        rules=[e for f in P for e in rules(P[f], f)], reproduction=repro_errs,
        consistency=version_checks(snap, raw) + doc_checks(snap, P, M) + construction_checks(snap, P, meta) + link_checks(snap),
        palette=P,
    )


def report(r):
    print(f"# Twilight validation: {r['snapshot']}\n")
    print(f"{'check':34} " + "   ".join(f"{f:>8} {'floor':>7}" for f in r["palette"]))
    for c in FLOORS:
        row = [x for x in r["floors"] if x["check"] == c]
        cells = "   ".join(f"{fmt(x['value'], x['floor']):>8} {fmt(x['floor'], x['floor']):>7}{'' if x['ok'] else ' FAIL'}" for x in row)
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


def limit_value(key, value):
    """A JND limit is capped at its target: above the target the state is met, not better."""
    state = key[4:] if key.startswith("JND ") else None
    return min(value, k.STATE_JND[state]) if state in k.STATE_JND else value


def compare(base, prop):
    """Print deltas; return regressions: worsened known limits and values that moved away from the generator."""
    lines, regressions = [], []
    old = {(x["flavor"], x["check"]): x for x in base["floors"]}
    for p in prop["floors"]:
        if (b := old.get((p["flavor"], p["check"]))) and abs(d := p["value"] - b["value"]) > 1e-9:
            lines.append(f"{p['flavor']} {p['check']}: {fmt(b['value'])} → {fmt(p['value'])} ({d:+.4f})")
            if d < 0:   # floors are rounded; the unrounded baseline is what may never get worse
                regressions.append(f"quality decreased: {p['flavor']} {p['check']} {b['value']:.5f} → {p['value']:.5f}")
    for f in sorted(set(base["palette"]) & set(prop["palette"])):
        for key in LIMITS:
            if (p := limit_value(key, prop["limits"][f][key])) < (b := limit_value(key, base["limits"][f][key])) - 1e-9:
                regressions.append(f"known limit worse: {f} {key} {fmt(b)} → {fmt(p)}")
    changed = [f"{f}.{g}.{t}" for f in prop["palette"] for g in ("neutrals", "colors", "states")
               for t, v in prop["palette"][f][g].items() if base["palette"].get(f, {}).get(g, {}).get(t) != v]
    if changed:
        lines.append(f"changed values: {', '.join(changed)}")
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
    a = ap.parse_args()
    r = run(Snap(a.ref), a.path, not a.no_rebuild)
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