"""Typography tokens: consistency checks, and the tables and figures of the typography documents.

typography/twilight.json is written by fonts/scripts/typography.py from the built fonts and the rules. This
module needs neither: it checks the file against itself and renders, from it alone, every block of the two
typography documents wrapped in `<!-- generated:NAME -->` … `<!-- /generated -->` and every figure in prose
wrapped in `<!-- fact:t.NAME -->…<!-- /fact -->`. docs.py writes and checks them; validate.py reports any
difference.
"""
import json
import math
import re

TOKENS = "typography/twilight.json"
DOCS = ("docs/design-system/typography.md", "docs/construction/typography.md")
BLOCK = re.compile(r"(<!-- generated:([\w-]+) -->\n)(.*?)(<!-- /generated -->)", re.S)
FACT = re.compile(r"<!-- fact:(t\.[\w.-]+) -->(.*?)<!-- /fact -->")
STEPS = [str(k) for k in range(-2, 8)]
WEIGHTS = ("ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold")
WEIGHT_NAMES = {200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold",
                800: "ExtraBold"}
GEOMETRY_NAMES = {"desktop": "Desktop", "handheld": "Handheld", "documents": "Documents", "slides": "Slides"}
UNITS = {"desktop": "px", "handheld": "px", "documents": "pt", "slides": "% of height"}
PX_PER_PT = 4 / 3
TOL = 1e-3


def num(v, decimals=2):
    """A whole number without decimals, anything else with a fixed number of them."""
    return str(int(round(v))) if abs(v - round(v)) < 1e-9 else f"{v:.{decimals}f}"


def rem(px):
    return f"{px / 16:.4f}".rstrip("0").rstrip(".")


def minus(s):
    return str(s).replace("-", "−")


def up(v, grain):
    return math.ceil(v / grain - 1e-9) * grain


def italic(w):
    return "Italic" if w == "Regular" else w + "Italic"


def row(cells):
    return "| " + " | ".join(cells) + " |"


def table(header, rows):
    return "\n".join([row(header), row(["---"] * len(header))] + [row(r) for r in rows])


# Blocks ------------------------------------------------------------------------------------------
def scale(T):
    G = T["geometries"]
    rows = []
    for k in reversed(STEPS):
        cells = [minus(k), num(G["desktop"]["steps"][k]), rem(G["desktop"]["steps"][k]), num(G["handheld"]["steps"][k]),
                 rem(G["handheld"]["steps"][k]), num(G["documents"]["steps"][k]), num(G["slides"]["steps"][k])]
        rows.append([f"**{c}**" for c in cells] if k == "0" else cells)
    rows.append(["Ratio", f"{G['desktop']['ratio']:.4f}", "", f"{G['handheld']['ratio']:.4f}", "",
                 f"{G['documents']['ratio']:.4f}", f"{G['slides']['ratio']:.4f}"])
    return table(["Step", "Desktop (px)", "Desktop (rem)", "Handheld (px)", "Handheld (rem)", "Documents (pt)",
                  "Slides (% of height)"], rows)


def scale_by_geometry(T):
    rows = []
    for g, label in GEOMETRY_NAMES.items():
        G = T["geometries"][g]
        rows.append([f"{label}, ratio {G['ratio']:.4f} ({UNITS[g]})"] + [num(G["steps"][k]) for k in STEPS])
    return table(["Step"] + [minus(k) for k in STEPS], rows)


def levels(T):
    fam = {"text": "Crystal", "literal": "Mono"}
    rows = []
    for L in T["levels"].values():
        weight = "Regular, or any weight (§7)" if "weights" in L else WEIGHT_NAMES[L["weight"]]
        rows.append([L["name"], L["use"], minus(L["step"]), weight, num(L["line height"], 1), fam[L["family"]]])
    C = T["code"]
    rows.append(["Code in editors and terminals", "Read for hours; outside the scale",
                 f"{C['minimum']} px minimum, {C['optimal']} px optimal", "Regular", num(C["line height"], 1), "Mono"])
    rows.append(["Literal text in a sentence", "Code, commands, paths, keys and values inside running or interface text",
                 "the sentence's", "the sentence's", "the sentence's", "Mono"])
    return table(["Level", "Use", "Step", "Weight", "Line height", "Family"], rows)


def lowest_steps(T):
    F = T["fonts"]
    c, m = F["Twilight Crystal"]["styles"], F["Twilight Crystal Mono"]["styles"]
    rows = [[w, minus(c[w]["lowest step"]), minus(c[italic(w)]["lowest step"]), minus(m[w]["lowest step"]),
             minus(m[italic(w)]["lowest step"])] for w in WEIGHTS]
    return table(["Weight", "Twilight Crystal", "Italic", "Twilight Crystal Mono", "Mono italic"], rows)


def floors(T):
    F = T["fonts"]
    c, m = F["Twilight Crystal"]["styles"], F["Twilight Crystal Mono"]["styles"]
    rows = []
    for w in WEIGHTS:
        s = c[w]
        floor = f"**{s['floor']} px**" if w == "Regular" else f"{s['floor']} px"
        rows.append([f"{w} ({s['weight']})", f"{s['stem']:.3f} em", f"{s['counter']:.3f} em ({s['counter glyph']})", floor,
                     f"{c[italic(w)]['floor']} px", f"{m[w]['floor']} px", f"{m[italic(w)]['floor']} px"])
    return table(["Weight", "Stem", "Narrowest counter", "Floor, upright", "Floor, italic", "Mono, upright",
                  "Mono, italic"], rows)


def tool_values(T):
    rows = []
    for name, t in T["tools"].items():
        steps = T["geometries"][t["geometry"]]["steps"]
        rows.append([name] + [num(up(steps[k] * t["factor"], t["grain"]), 1) for k in STEPS] + [t["unit"]])
    return table(["Tool"] + [minus(k) for k in STEPS] + ["Unit"], rows)


def editor_defaults(T):
    rows = [[system, f"{d['font']}, {d['size']} px", f"{d['x-height'] / d['size']:.3f} em", f"{d['x-height']:.2f} px"]
            for system, d in T["code"]["editor defaults"].items()]
    return table(["System", "Default", "x-height of the font", "x-height"], rows)


def grid(T):
    G, C = T["code"]["grid rounding"], T["code"]
    mark = lambda size, text: f"**{text}**" if int(size) in (C["minimum"], C["optimal"]) else text  # noqa: E731
    return table(["Size (px)"] + [mark(s, s) for s in G],
                 [["Largest rounding"] + [mark(s, f"{v * 100:.1f} %") for s, v in G.items()]])


def measure(T):
    M = T["measure"]
    return table(["Language", "Mean character", f"{M['characters']} characters"],
                 [[lang, f"{v:.3f} em", f"{M['characters'] * v:.1f} em"] for lang, v in M["mean character"].items()])


def system_fonts(T):
    size = lambda name: f"{round(T['fallbacks']['text' if name in T['fallbacks']['text'] else 'literal'][name]['size adjust'] * 100)} %"  # noqa: E731
    rows = [[r["system"], r["text"], size(r["text"].replace(" if installed", "")), r["literal"], size(r["literal"]),
             f"{r['cell']:.2f} em"] for r in T["systems"]]
    return table(["System", "Sans-serif", "Size", "Monospaced", "Size", "Cell after sizing"], rows)


BLOCKS = { "system-fonts": system_fonts,"scale": scale, "scale-by-geometry": scale_by_geometry, "levels": levels, "lowest-steps": lowest_steps,
          "floors": floors, "tool-values": tool_values, "editor-defaults": editor_defaults, "code-grid": grid,
          "measure": measure}


# Figures in prose ------------------------------------------------------------------------------
def facts(T):
    G, C, M, Fit = T["geometries"], T["code"], T["measure"], T["fit"]
    out = {}
    for g in ("desktop", "handheld", "documents"):
        unit = "pt" if g == "documents" else "px"
        out[f"t.{g}.step0"] = f"{num(G[g]['step0'])} {unit}"
        out[f"t.{g}.line"] = f"{num(G[g]['line'], 1)} {unit}"
        out[f"t.{g}.measure"] = f"{round(M['em'] * G[g]['step0'])} {unit}"
    out["t.slides.step0"] = f"{G['slides']['step0']:.2f} %"
    out["t.slides.line"] = f"{G['slides']['line']:.2f} %"
    out["t.slides.desktop"] = f"{math.ceil(G['desktop']['step0'] / G['slides']['step0'] * 100)} px"
    out["t.documents.zoom"] = f"{math.ceil(G['desktop']['step0'] / (G['documents']['step0'] * PX_PER_PT) * 100)} %"
    out["t.documents.measure-cm"] = f"{M['em'] * G['documents']['step0'] / 72 * 2.54:.1f} cm"
    out["t.distance.step0"] = f"{G['distance']['step0']:.3f} %"
    out["t.distance.floor"] = f"{G['distance']['floor']:.3f} %"
    out["t.distance.ratio"] = f"{G['distance']['ratio']:.4f}"
    mm = G["distance"]["step0"] / 100 * 2000
    out["t.distance.2m"] = f"{mm:.1f} mm, {round(mm / 25.4 * 72)} pt"
    out["t.measure.em"] = f"{num(M['em'], 1)} em"
    out["t.measure.characters"] = str(M["characters"])
    out["t.fit.em"] = f"{Fit['em']:.2f}"
    out["t.fit.narrowest"] = f"{(Fit['narrowest'] - 2 * Fit['gutter']) / Fit['em']:.2f} px"
    out["t.code.minimum"] = f"{C['minimum']} px"
    out["t.code.optimal"] = f"{C['optimal']} px"
    out["t.code.optimal-pt"] = f"{num(C['optimal'] / PX_PER_PT)} pt"
    out["t.code.minimum-pt"] = f"{num(C['minimum'] / PX_PER_PT, 1)} pt"
    out["t.touching"] = f"{T['fonts']['Twilight Crystal']['touching line']:.3f}"
    return out


# Rendering and checks ----------------------------------------------------------------------------
def render(text, T, F_=None):
    F_ = F_ or facts(T)
    text = BLOCK.sub(lambda m: m.group(1) + BLOCKS[m.group(2)](T) + "\n" + m.group(4) if m.group(2) in BLOCKS
                     else m.group(0), text)
    return FACT.sub(lambda m: f"<!-- fact:{m.group(1)} -->{F_[m.group(1)]}<!-- /fact -->" if m.group(1) in F_
                    else m.group(0), text)


def document_errors(read, T):
    F_ = facts(T)
    errs = []
    for path in DOCS:
        have = read(path)
        errs += [f"{path}: unknown generated block `{n}`" for _, n, _, _ in BLOCK.findall(have) if n not in BLOCKS]
        errs += [f"{path}: unknown fact `{n}`" for n, _ in FACT.findall(have) if n not in F_]
        want = render(have, T, F_)
        for no, (a, b) in enumerate(zip(have.split("\n"), want.split("\n")), 1):
            if a != b:
                errs.append(f"{path}:{no}: differs from {TOKENS} (run scripts/docs.py)")
    return errs


def token_errors(T, changelog):
    """The tokens agree with themselves and with the rules they encode."""
    errs = []
    latest = next((m.group(1) for line in changelog.splitlines() if (m := re.match(r"## (\d+\.\d+\.\d+)", line))), None)
    if T.get("version") != latest:
        errs.append(f"{TOKENS} version {T.get('version')} != latest CHANGELOG.md {latest}")
    for g, G in T["geometries"].items():
        steps = {int(k): v for k, v in G["steps"].items()}
        if sorted(steps) != list(range(-2, 8)):
            errs.append(f"{TOKENS}: {g} does not have steps −2 to 7")
            continue
        if abs(steps[0] - G["step0"]) > TOL or abs(steps[-2] - G["floor"]) > TOL:
            errs.append(f"{TOKENS}: {g} step 0 or −2 is not its running text or floor")
        if abs(G["ratio"] - math.sqrt(G["step0"] / G["floor"])) > 2e-4:
            errs.append(f"{TOKENS}: {g} ratio is not √(step 0 / floor)")
        errs += [f"{TOKENS}: {g} step {k} is not step 0 × ratio^{k}" for k, v in steps.items()
                 if abs(v - G["step0"] * G["ratio"] ** k) > max(TOL, 1e-4 * v)]
        if "line" in G and abs(G["line"] - G["step0"] * T["line height"]["running"]) > TOL:
            errs.append(f"{TOKENS}: {g} line is not step 0 × the running line height")
    for g in ("desktop", "handheld"):
        if T["geometries"][g]["step0"] < 16:
            errs.append(f"{TOKENS}: {g} running text below the default size of 16 px")
    families = {T["families"]["text"]: "text", T["families"]["literal"]: "literal"}
    for k, L in T["levels"].items():
        name = next(n for n, f in families.items() if f == L["family"])
        style = T["fonts"][name]["styles"][WEIGHT_NAMES[L["weight"]]]
        if L["step"] < style["lowest step"]:
            errs.append(f"{TOKENS}: level {k} at step {L['step']} is below the lowest step of its weight")
        if L["line height"] < T["fonts"][name]["natural line"] - 1e-9:
            errs.append(f"{TOKENS}: level {k} has a line height below the fonts' natural line")
        if L["line height"] == T["line height"]["running"] and L["step"] < 0 and k not in ("small", "fine"):
            errs.append(f"{TOKENS}: level {k} is running text below step 0")
    if T["levels"]["running-text"]["step"] != 0 or T["levels"]["running-text"]["line height"] < 1.5:
        errs.append(f"{TOKENS}: running text must be step 0 at a line height of at least 1.5 (WCAG 1.4.8)")
    C, mono = T["code"], T["fonts"][T["families"]["literal"]]
    regular_floor = mono["styles"]["Regular"]["floor"]
    if not regular_floor <= C["minimum"] <= C["optimal"] <= T["geometries"]["desktop"]["step0"]:
        errs.append(f"{TOKENS}: code sizes must lie between the Mono floor and desktop running text")
    if any(C["optimal"] * mono["x-height"] < d["x-height"] - 0.01 for d in C["editor defaults"].values()):
        errs.append(f"{TOKENS}: optimal code size is below the x-height of an editor default")
    if abs(C["line height"] - mono["natural line"]) > 1e-9:
        errs.append(f"{TOKENS}: code line height is not the Mono natural line")
    narrow = min(T["measure"]["mean character"].values())
    if T["measure"]["em"] * 1 > T["measure"]["characters"] * narrow + 0.05:
        errs.append(f"{TOKENS}: the measure holds more than {T['measure']['characters']} characters")
    if T["letter spacing"] != 0:
        errs.append(f"{TOKENS}: letter spacing must be 0")
    return errs


def load(read):
    return json.loads(read(TOKENS))
