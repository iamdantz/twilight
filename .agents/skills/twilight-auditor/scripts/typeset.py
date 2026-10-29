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
SCALE = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl"]   # steps −2 to 7
INDEX = {name: i - 2 for i, name in enumerate(SCALE)}
WEIGHTS = ("ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold")
WEIGHT_NAMES = {200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold",
                800: "ExtraBold"}
GEOMETRIES = {"desktop": ("Desktop", "px"), "handheld": ("Handheld", "px"), "page": ("Page", "pt"),
              "slide": ("Slide", "% of height")}
PX_PER_PT = 4 / 3
TOL = 1e-3


def num(v, decimals=2):
    """A whole number without decimals, anything else with a fixed number of them."""
    return str(int(round(v))) if abs(v - round(v)) < 1e-9 else f"{v:.{decimals}f}"


def rem(px):
    return f"{px / 16:.4f}".rstrip("0").rstrip(".")


def up(v, grain):
    return math.ceil(v / grain - 1e-9) * grain


def italic(w):
    return "Italic" if w == "Regular" else w + "Italic"


def code(s):
    return f"`{s}`"


def row(cells):
    return "| " + " | ".join(cells) + " |"


def table(header, rows):
    return "\n".join([row(header), row(["---"] * len(header))] + [row(r) for r in rows])


def spacing(T, g):
    return T["geometries"][g]["scale"]["base"] * T["leading"]["default"]


# Blocks ------------------------------------------------------------------------------------------
def scale(T):
    G = T["geometries"]
    rows = []
    for k in reversed(SCALE):
        cells = [code(k), num(G["desktop"]["scale"][k]), rem(G["desktop"]["scale"][k]), num(G["handheld"]["scale"][k]),
                 rem(G["handheld"]["scale"][k]), num(G["page"]["scale"][k]), num(G["slide"]["scale"][k])]
        rows.append([f"**{c}**" for c in cells] if k == "base" else cells)
    rows.append(["Ratio", f"{G['desktop']['ratio']:.4f}", "", f"{G['handheld']['ratio']:.4f}", "",
                 f"{G['page']['ratio']:.4f}", f"{G['slide']['ratio']:.4f}"])
    return table(["Step", "Desktop (px)", "Desktop (rem)", "Handheld (px)", "Handheld (rem)", "Page (pt)",
                  "Slide (% of height)"], rows)


def scale_by_geometry(T):
    rows = []
    for g, (label, unit) in GEOMETRIES.items():
        G = T["geometries"][g]
        rows.append([f"{label}, ratio {G['ratio']:.4f} ({unit})"] + [num(G["scale"][k]) for k in SCALE])
    return table(["Step"] + [f"{code(k)} ({INDEX[k]:+d})".replace("+0", "0").replace("-", "−") for k in SCALE], rows)


def levels(T):
    rows = []
    for key, L in T["levels"].items():
        weight = "Regular, or any weight (§8)" if "weights" in L else WEIGHT_NAMES[L["weight"]]
        rows.append([code(key), L["use"], code(L["size"]), weight,
                     f"{code(L['leading'])} ({num(T['leading'][L['leading']], 1)})", code(L["font"])])
    return table(["Level", "Use", "Step", "Weight", "Leading", "Font"], rows)


def lowest_steps(T):
    s, m = T["fonts"]["sans"]["styles"], T["fonts"]["mono"]["styles"]
    rows = [[w, code(s[w]["lowest-step"]), code(s[italic(w)]["lowest-step"]), code(m[w]["lowest-step"]),
             code(m[italic(w)]["lowest-step"])] for w in WEIGHTS]
    return table(["Weight", "Sans", "Sans italic", "Mono", "Mono italic"], rows)


def floors(T):
    s, m = T["fonts"]["sans"]["styles"], T["fonts"]["mono"]["styles"]
    rows = []
    for w in WEIGHTS:
        x = s[w]
        floor = f"**{x['floor']} px**" if w == "Regular" else f"{x['floor']} px"
        rows.append([f"{w} ({x['weight']})", f"{x['stem']:.3f} em", f"{x['counter']:.3f} em ({x['counter-glyph']})", floor,
                     f"{s[italic(w)]['floor']} px", f"{m[w]['floor']} px", f"{m[italic(w)]['floor']} px"])
    return table(["Weight", "Stem", "Narrowest counter", "Sans", "Sans italic", "Mono", "Mono italic"], rows)


def tool_values(T):
    rows = []
    for name, t in T["tools"].items():
        sc = T["geometries"][t["geometry"]]["scale"]
        rows.append([name] + [num(up(sc[k] * t["factor"], t["grain"]), 1) for k in SCALE] + [t["unit"]])
    return table(["Tool"] + [code(k) for k in SCALE] + ["Unit"], rows)


def editor_defaults(T):
    rows = [[system, f"{d['font']}, {d['size']} px", f"{d['x-height'] / d['size']:.3f} em", f"{d['x-height']:.2f} px"]
            for system, d in T["editors"]["defaults"].items()]
    return table(["System", "Default", "x-height of the font", "x-height"], rows)


def grid(T):
    G, S = T["editors"]["grid-rounding"], T["editors"]["font-size"]
    mark = lambda size, text: f"**{text}**" if int(size) in S.values() else text  # noqa: E731
    return table(["Size (px)"] + [mark(s, s) for s in G],
                 [["Largest rounding"] + [mark(s, f"{v * 100:.1f} %") for s, v in G.items()]])


def measure(T):
    P = T["container"]["prose"]
    return table(["Language", "Mean character", f"{P['characters']} characters"],
                 [[lang, f"{v:.3f} em", f"{P['characters'] * v:.1f} em"] for lang, v in P["mean-character"].items()])


def system_fonts(T):
    F = T["fonts"]
    size = lambda font, name: f"{round(F[font]['fallbacks'][name.replace(' if installed', '')]['size-adjust'] * 100)} %"  # noqa: E731
    rows = [[r["system"], r["sans"], size("sans", r["sans"]), r["mono"], size("mono", r["mono"]), f"{r['cell']:.2f} em"]
            for r in T["systems"]]
    return table(["System", "Sans-serif", "Size", "Monospaced", "Size", "Cell after sizing"], rows)


BLOCKS = {"scale": scale, "scale-by-geometry": scale_by_geometry, "levels": levels, "lowest-steps": lowest_steps,
          "floors": floors, "tool-values": tool_values, "editor-defaults": editor_defaults, "code-grid": grid,
          "measure": measure, "system-fonts": system_fonts}


# Figures in prose ------------------------------------------------------------------------------
def facts(T):
    G, E, P, Fit = T["geometries"], T["editors"]["font-size"], T["container"]["prose"], T["fit"]
    out = {}
    for g in ("desktop", "handheld", "page"):
        unit = "pt" if g == "page" else "px"
        out[f"t.{g}.base"] = f"{num(G[g]['scale']['base'])} {unit}"
        out[f"t.{g}.spacing"] = f"{num(spacing(T, g), 1)} {unit}"
        out[f"t.{g}.prose"] = f"{round(P['em'] * G[g]['scale']['base'])} {unit}"
    out["t.slide.base"] = f"{G['slide']['scale']['base']:.2f} %"
    out["t.slide.spacing"] = f"{spacing(T, 'slide'):.2f} %"
    out["t.slide.desktop"] = f"{math.ceil(G['desktop']['scale']['base'] / G['slide']['scale']['base'] * 100)} px"
    out["t.page.zoom"] = f"{math.ceil(G['desktop']['scale']['base'] / (G['page']['scale']['base'] * PX_PER_PT) * 100)} %"
    out["t.page.prose-cm"] = f"{P['em'] * G['page']['scale']['base'] / 72 * 2.54:.1f} cm"
    out["t.distance.base"] = f"{G['distance']['scale']['base']:.3f} %"
    out["t.distance.floor"] = f"{G['distance']['scale']['xs']:.3f} %"
    out["t.distance.ratio"] = f"{G['distance']['ratio']:.4f}"
    mm = G["distance"]["scale"]["base"] / 100 * 2000
    out["t.distance.2m"] = f"{mm:.1f} mm, {round(mm / 25.4 * 72)} pt"
    out["t.prose.em"] = f"{num(P['em'], 1)} em"
    out["t.prose.characters"] = str(P["characters"])
    out["t.fit.em"] = f"{Fit['em']:.2f}"
    out["t.fit.narrowest"] = f"{(Fit['narrowest'] - 2 * Fit['gutter']) / Fit['em']:.2f} px"
    out["t.editors.size"] = f"{E['default']} px"
    out["t.editors.size-lg"] = f"{E['lg']} px"
    out["t.editors.size-pt"] = f"{num(E['default'] / PX_PER_PT, 1)} pt"
    out["t.editors.size-lg-pt"] = f"{num(E['lg'] / PX_PER_PT)} pt"
    out["t.touching"] = f"{T['fonts']['sans']['touching-line']:.3f}"
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
        sc = G["scale"]
        if list(sc) != SCALE:
            errs.append(f"{TOKENS}: {g} scale is not {', '.join(SCALE)}")
            continue
        if abs(G["ratio"] - math.sqrt(sc["base"] / sc["xs"])) > 2e-4:
            errs.append(f"{TOKENS}: {g} ratio is not √(base / xs)")
        errs += [f"{TOKENS}: {g} step {k} is not base × ratio^{INDEX[k]}" for k, v in sc.items()
                 if abs(v - sc["base"] * G["ratio"] ** INDEX[k]) > max(TOL, 1e-4 * v)]
    for g in ("desktop", "handheld"):
        if T["geometries"][g]["scale"]["base"] < 16:
            errs.append(f"{TOKENS}: {g} base below the default size of 16 px")
    for k, L in T["levels"].items():
        F = T["fonts"][L["font"]]
        style = F["styles"][WEIGHT_NAMES[L["weight"]]]
        if INDEX[L["size"]] < INDEX[style["lowest-step"]]:
            errs.append(f"{TOKENS}: level {k} at {L['size']} is below the lowest step of its weight")
        if T["leading"][L["leading"]] < F["natural-line"] - 1e-9:
            errs.append(f"{TOKENS}: level {k} has a leading below the font's natural line")
        if k.startswith("body") and (L["leading"] != "default" or INDEX[L["size"]] < 0) and k not in ("body-sm", "body-xs"):
            errs.append(f"{TOKENS}: level {k} is body text below base or below the default leading")
    if T["levels"]["body"]["size"] != "base" or T["leading"]["default"] < 1.5:
        errs.append(f"{TOKENS}: body must be base at a leading of at least 1.5 (WCAG 1.4.8)")
    E, mono = T["editors"], T["fonts"]["mono"]
    S = E["font-size"]
    if not mono["styles"]["Regular"]["floor"] <= S["default"] <= S["lg"] <= T["geometries"]["desktop"]["scale"]["base"]:
        errs.append(f"{TOKENS}: editor font sizes must lie between the Mono floor and desktop base")
    if any(S["lg"] * mono["x-height"] < d["x-height"] - 0.01 for d in E["defaults"].values()):
        errs.append(f"{TOKENS}: the larger editor font size is below the x-height of an editor default")
    if abs(T["leading"][E["leading"]] - mono["natural-line"]) > 1e-9:
        errs.append(f"{TOKENS}: editor leading is not the Mono natural line")
    P = T["container"]["prose"]
    if P["em"] > P["characters"] * min(P["mean-character"].values()) + 0.05:
        errs.append(f"{TOKENS}: the prose container holds more than {P['characters']} characters")
    if T["tracking"] != 0:
        errs.append(f"{TOKENS}: tracking must be 0")
    return errs


def load(read):
    return json.loads(read(TOKENS))
