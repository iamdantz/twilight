"""Twilight Theme documents from the palette: tables, measured figures in prose, and the palette images.

Usage (from anywhere inside the Twilight Theme repository):
    <skill>/.venv/bin/python <skill>/scripts/docs.py           # rewrite README.md, design-system/color.md and assets/
    <skill>/.venv/bin/python <skill>/scripts/docs.py --check   # report every difference, change nothing

Every number this script writes is computed from palette/twilight.json. A measured figure in prose is wrapped in
`<!-- fact:NAME -->…<!-- /fact -->`; FACTS below says how each one is computed. Tables are recognized by their
header row, and flavor sections by a heading or summary that names the flavor.
"""
import argparse
import itertools
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True).stdout.strip())
sys.path.insert(0, str(Path(__file__).resolve().parent))
import construct as k  # noqa: E402

DOCS = ("README.md", "docs/design-system/color.md")
NAMES = {"Afterglow": "afterglow", "Coral": "coral", "Gold": "gold", "Grove": "grove", "Sea Salt": "sea-salt",
         "Sky": "sky", "Orchid": "orchid", "Ember": "ember"}
NEUTRAL_ORDER = ("shell", "rail", "canvas", "raised", "edge", "control", "faint", "subtle", "body", "ink")
COLOR_ORDER = ("afterglow", "coral", "gold", "grove", "sea-salt", "sky", "orchid", "ember")
SURF = ("shell", "rail", "canvas", "raised")
FACT = re.compile(r"<!-- fact:([\w.-]+) -->(.*?)<!-- /fact -->")


# Measured figures --------------------------------------------------------------------
def measures(P):
    import validate as v
    return {f: v.measure(P[f]) for f in P}


def facts(P, M):
    out = {}
    hexes = [h for F in P.values() for h in (*F["neutrals"].values(), *F["states"].values())]
    out["darkest"] = f"{min(k.oklch_of(h)[0] for h in hexes):.2f}"
    out["lightest"] = f"{max(k.oklch_of(h)[0] for h in hexes):.2f}"
    chips = []
    for f, F in P.items():
        n, c, A = F["neutrals"], F["colors"], F["accents"]
        dark = k.PROFILES[f]["dark"] if f in k.PROFILES else k.oklch_of(n["canvas"])[0] < 0.5
        L = {t: k.oklch_of(n[t])[0] for t in ("shell", "rail", "canvas", "raised", "edge")}
        label = {"shell": "Shell", "rail": "Rail", "canvas": "Canvas", "raised": "Raised", "edge": "Edge"}
        if dark:   # lighter as they come forward
            seq = sorted(L, key=L.get)
            out[f"{f}.surfaces"] = ", ".join(f"{label[t]} ({'L ' if i == 0 else ''}{L[t]:.2f})" for i, t in enumerate(seq))
        else:      # stepping down from Canvas
            seq = sorted((t for t in L if t != "canvas"), key=L.get, reverse=True)
            out[f"{f}.surfaces"] = ", ".join(f"{label[t]} ({L[t]:.2f})" for t in seq)
            out[f"{f}.canvas_L"] = f"{L['canvas']:.2f}"
        pairs = [k.contrast(n[a], n[b]) for a, b in itertools.combinations(SURF, 2)]
        out[f"{f}.separation"] = f"{min(pairs):.2f} to {max(pairs):.2f}"
        links = [k.contrast(a["accent-text"], n["body"]) for a in A.values()]
        out[f"{f}.link_body"] = f"{min(links):.2f}–{max(links):.2f}"
        out[f"{f}.link_coral"] = f"{k.de_ok(A['afterglow']['accent-text'], c['coral']):.3f}"
        label_on = n["shell"] if dark else n["canvas"]
        chips.append(min(k.contrast(label_on, c[x]) for x in ("coral", "gold", "grove", "sea-salt", "sky", "orchid")))
    out["chip"] = f"{min(chips):.2f}"
    label = lambda F: max(F["neutrals"].values(), key=lambda x: k.contrast(x, F["neutrals"]["ink"]))
    out["series_label"] = f"{min(k.contrast(label(F), F['colors'][x]) for F in P.values() for x in k.SERIES):.2f}"
    rc = [k.de_ok(F["neutrals"]["rail"], F["neutrals"]["canvas"]) / k.JND for F in P.values()]
    out["rail_canvas"] = f"{min(rc):.2f} to {max(rc):.2f}"
    out["min.subtle_edge"] = f"{min(M[f][0]['subtle on edge'] for f in P):.2f}"
    out["min.semantic_surfaces"] = f"{min(M[f][0]['semantic on surfaces and edge'] for f in P):.2f}"
    for f in P:
        out[f"{f}.faint_semantic"] = f"{M[f][0]['faint from semantic colors (JND)']:.2f}"
    out["min.accent_label"] = f"{min(M[f][0]['chip label on accent-text'] for f in P):.2f}"
    for lvl in ("ink", "body", "subtle", "faint", "control"):
        out[f"min.{lvl}"] = f"{min(M[f][0][lvl + ' on surfaces'] for f in P):.2f}"
    return out


# Formatting --------------------------------------------------------------------------
def okfmt(hx):
    L, C, h = k.oklch_of(hx)
    return f"oklch({L * 100:.1f}% {C:.3f} {'0' if C < 0.0015 else f'{h:.1f}'})"


def rgb(hx):
    return "rgb(" + ", ".join(str(int(hx[i:i + 2], 16)) for i in (1, 3, 5)) + ")"


def img(hx, size):
    return f'<img src="https://placehold.co/{size}x{size}/{hx[1:]}/{hx[1:]}" width="{size}" height="{size}" alt="{hx}">'


# Tables ------------------------------------------------------------------------------
GUARANTEE_ROWS = {  # design-system guarantee row label → (measurement, unit)
    "Ink on any surface": ("ink on surfaces", "ratio"), "Body on any surface": ("body on surfaces", "ratio"),
    "Subtle on any surface": ("subtle on surfaces", "ratio"), "Faint on any surface": ("faint on surfaces", "ratio"),
    "Control boundary on any surface": ("control on surfaces", "ratio"),
    "Subtle on an Edge fill": ("subtle on edge", "ratio"),
    "Accent focus on any surface, every accent": ("accent-focus on surfaces", "ratio"),
    "Chip label on `accent-text`, every accent": ("chip label on accent-text", "ratio"),
    "Code colors on every code surface": ("code on code surfaces", "ratio"),
    "Smallest code-color difference, normal vision": ("ΔE code+cursor, normal", "de"),
    "Smallest code-color difference, color-vision deficiency": ("ΔE code+cursor, worst CVD", "de"),
    "Semantic colors on any surface and on Edge": ("semantic on surfaces and edge", "ratio"),
    "Faint from every semantic color, every vision": ("faint from semantic colors (JND)", "jnd2"),
    "Twelve chromatic terminal colors, closest pair, every vision": ("ΔE ANSI colors, every vision", "de"),
    "Ember from Afterglow, normal vision": ("ΔE Ember from Afterglow", "de"),
    "Scale steps, closest pair, normal vision": ("ΔE scale steps, normal", "de"),
    "Scale steps, closest pair, color-vision deficiency": ("ΔE scale steps, worst CVD", "de"),
    "Scale cell labels, lowest": ("scale cell labels", "ratio"),
    "Other series from every series, every vision": ("ΔE other series, every vision", "de"),
    "Neutral row and control states, closest pair": ("neutral states, closest pair (JND)", "jnd"),
}
UNITS = {"ratio": lambda v: f"{v:.2f}:1", "de": lambda v: f"ΔE {v:.3f}", "jnd": lambda v: f"{v:.1f} JND", "jnd2": lambda v: f"{v:.2f} JND"}
README_GUARANTEES = {  # README row label → (measurements, decimals); the shown value is the lower one
    "Body text on any surface": (("body on surfaces",), 2), "Faintest text on any surface": (("faint on surfaces",), 2),
    "Code colors on every code surface": (("code on code surfaces",), 2),
    "Control boundaries and focus": (("control on surfaces", "accent-focus on surfaces"), 2),
    "Smallest code-color difference, color-vision deficiency": (("ΔE code+cursor, worst CVD",), 3),
}
LEVELS = {"**Ink**": "ink", "**Body**": "body", "**Subtle**": "subtle", "**Faint**": "faint", "**Control**": "control"}


def cells_of(line):
    return line.strip().strip("|").split("|")


def row(cs):
    return "|" + "|".join(cs) + "|"


def flavor_of_heading(line, P):
    m = re.match(r"^(?:#+\s*|<summary><b>)(\w+)", line)
    return m.group(1).lower() if m and m.group(1).lower() in P else None


def display(tok):
    return {v: n for n, v in NAMES.items()}.get(tok, tok.capitalize())


def series_row(cs, H, P):
    """One row of the series table: its color, a swatch per flavor, and per flavor the smallest ΔE (every vision) among
    the series up to this one, or for Other, between Control and every series."""
    pos = cs[0].strip()
    other = pos == "Other"
    tok = k.SERIES_OTHER if other else k.SERIES[int(pos) - 1]
    cells = [cs[0], f" {display(tok)} "]
    for h in H[2:]:
        if h.lower() in P:
            F = P[h.lower()]
            cells.append(f" {img(F['neutrals' if other else 'colors'][tok], 16)} `{F['neutrals' if other else 'colors'][tok]}` ")
        else:                                                   # "Smallest ΔE, <Flavor>"
            c, n = P[h.split(", ")[1].lower()]["colors"], P[h.split(", ")[1].lower()]["neutrals"]
            if other:
                v = min(k.worst_de([n[tok], c[x]]) for x in k.SERIES)
            else:
                v = k.worst_de([c[x] for x in k.SERIES[:int(pos)]]) if int(pos) > 1 else None
            cells.append(" — " if v is None else f" {v:.3f} ")
    return cells


def render(text, P, M, F_):
    """Return `text` with every recognized table row and fact recomputed."""
    out, flavor, header = [], None, None
    for line in text.split("\n"):
        if f := flavor_of_heading(line, P):
            flavor = f
        elif re.match(r"^#{1,3} ", line):
            flavor = None if not line.startswith("### ") else flavor
        if not line.startswith("|"):
            header = None
            out.append(FACT.sub(lambda m: f"<!-- fact:{m.group(1)} -->{F_[m.group(1)]}<!-- /fact -->" if m.group(1) in F_ else m.group(0), line))
            continue
        cs = cells_of(line)
        if set(line.replace("|", "").strip()) <= set("-: "):
            out.append(line)
            continue
        if header is None:
            header = [c.strip() for c in cs]
            out.append(line)
            continue
        H, new = header, None
        if H[0] == "Accent" and len(H) >= 3 and all(h.lower() in P for h in H[1:-1]):              # README accents
            tok = NAMES[cs[0].strip()]
            cols = [re.sub(r"[0-9a-f]{6}", P[f]["colors"][tok][1:], cell)                        # same width, new hex
                    for f, cell in zip((h.lower() for h in H[1:-1]), cs[1:-1])]
            new = [cs[0], *cols, cs[-1]]
        elif H[0] == "Guarantee" and all(h.lower() in P for h in H[1:]):                       # design-system §13
            label = cs[0].strip()
            if label in GUARANTEE_ROWS:
                key, unit = GUARANTEE_ROWS[label]
                new = [cs[0]] + [f" {UNITS[unit](M[f][0][key])} " for f in (h.lower() for h in H[1:])]
        elif H[0] == "" and len(H) == 3 and all(h.lower() in P for h in H[1:]):                 # README guarantees
            label = cs[0].strip()
            if label in README_GUARANTEES:
                keys, d = README_GUARANTEES[label]
                vals = [min(M[f][0][x] for x in keys) for f in (h.lower() for h in H[1:])]
                new = [cs[0]] + [f" {('ΔE ' + format(v, '.3f')) if d == 3 else format(v, f'.{d}f') + ':1'} " for v in vals]
        elif H[:2] == ["Scale", "Step"]:                                                        # design-system scales
            name, step = cs[0].strip().lower(), cs[1].strip().replace("−", "-")
            cells = [cs[0], cs[1]]
            for h in H[2:]:
                sc = P[h.lower()]["scales"][name]
                hx = sc[int(step) - 1] if name == "sequential" else sc[len(sc) // 2 + int(step)]
                cells.append(f" {img(hx, 16)} `{hx}` ")
            new = cells
        elif H[:2] == ["Series", "Color"]:                                                      # design-system data series
            new = series_row(cs, H, P)
        elif H[0] == "Level" and H[1].startswith("Minimum"):                                     # design-system §4
            if (lvl := LEVELS.get(cs[0].strip())):
                new = [cs[0], f" {F_['min.' + lvl]}:1 ", *cs[2:]]
        elif flavor:
            F, n = P[flavor], P[flavor]["neutrals"]
            if H[1:4] == ["Token", "Hex", "OKLCH"] and H[4] == "vs Shell":
                tok = cs[1].strip().strip("`"); hx = n[tok]
                new = [f" {img(hx, 16)} ", f" `{tok}` ", f" `{hx}` ", f" `{okfmt(hx)}` "] + [f" {k.contrast(hx, n[s]):.2f} " for s in SURF]
            elif H[1:5] == ["Name", "Hex", "RGB", "OKLCH"] and H[5] == "Role":
                name = cs[1].strip(); hx = n[name.lower()]
                new = [f" {img(hx, 20)} ", f" {name} ", f" `{hx}` ", f" `{rgb(hx)}` ", f" `{okfmt(hx)}` ", cs[5]]
            elif H[1:4] == ["Token", "Hex", "OKLCH"] and H[4] == "On Canvas":
                tok = cs[1].strip().strip("`"); hx = F["colors"][tok]
                worst = "—" if tok == "afterglow" else f"{min(k.contrast(hx, s) for s in (n['canvas'], F['states']['diff-inserted'], F['states']['diff-removed'])):.2f}"
                new = [f" {img(hx, 16)} ", f" `{tok}` ", f" `{hx}` ", f" `{okfmt(hx)}` ", f" {k.contrast(hx, n['canvas']):.2f} ", f" {worst} "]
            elif H[1:5] == ["Name", "Hex", "RGB", "OKLCH"] and H[5] == "Meaning":
                name = cs[1].strip(); hx = F["colors"][NAMES[name]]
                new = [f" {img(hx, 20)} ", f" {name} ", f" `{hx}` ", f" `{rgb(hx)}` ", f" `{okfmt(hx)}` ", cs[5]]
            elif H[0] == "Accent" and H[1] == "`accent`":
                fam = F["accents"][NAMES[cs[0].strip()]]
                new = [cs[0]] + [f" {img(fam[t], 16)} `{fam[t]}` " for t in ("accent", "accent-text", "accent-pressed", "accent-focus", "on-accent")]
            elif H[0] == "Accent" and H[1] == "Label on fill":
                fam = F["accents"][NAMES[cs[0].strip()]]
                focus = min(k.contrast(fam["accent-focus"], n[s]) for s in SURF)
                new = [cs[0], f" {k.contrast(fam['on-accent'], fam['accent']):.2f} ", f" {k.contrast(fam['on-accent'], fam['accent-pressed']):.2f} ",
                       f" {k.contrast(fam['accent-text'], n['raised']):.2f} ", f" {focus:.2f} "]
            elif H[1:4] == ["Token", "Hex", "Hue from"]:
                tok = cs[1].strip().strip("`"); hx = F["states"][tok]
                new = [f" {img(hx, 16)} ", cs[1], f" `{hx}` ", cs[3], f" {k.de_ok(hx, n['canvas']) / k.JND:.1f} JND ", cs[5]]
            elif H[:2] == ["#", "Slot"]:
                hx = F["ansi"][int(cs[0])]
                new = [cs[0], cs[1], f" {img(hx, 16)} ", f" `{hx}` ", cs[4], f" {k.contrast(hx, n['canvas']):.2f} "]
        out.append(row(new) if new is not None else line)
    text = "\n".join(out)
    # README swatch strips: one line of 24 px swatches per flavor, neutrals then colors
    def strip(m):
        f = m.group(1).lower()
        sw = ("".join(img(P[f]["neutrals"][t], 24) for t in NEUTRAL_ORDER) + "&nbsp;&nbsp;"
              + "".join(img(P[f]["colors"][t], 24) for t in COLOR_ORDER))
        return m.group(0)[:m.start(2) - m.start(0)] + sw
    return re.sub(r"<summary><b>(\w+)</b></summary>\n<br>\n\n(<img src=\"https://placehold.co/24x24[^\n]*)", strip, text)


# Images ------------------------------------------------------------------------------
# Layout of assets/palette-<flavor>.png, in pixels of the 3200 × 840 image.
W, H = 3200, 840
SWATCH = dict(x0=160, step=291.2, y0=256, w=262, h=128, radius=16, border=2)
CIRCLE = dict(cx0=232, step=365.6, cy=635.5, r=75)
TEXT = dict(title=(160, 137, 32), neutral_name=402, neutral_hex=452, color_name=726, color_hex=776, name_size=27, hex_size=23.75)
FONTS = ("DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "Menlo.ttc",
         "/System/Library/Fonts/Menlo.ttc", "consola.ttf", "C:/Windows/Fonts/consola.ttf")


def swatch_centers():
    return [(round(SWATCH["x0"] + SWATCH["step"] * i + SWATCH["w"] / 2), SWATCH["y0"] + SWATCH["h"] // 2) for i in range(len(NEUTRAL_ORDER))]


def circle_centers():
    return [(round(CIRCLE["cx0"] + CIRCLE["step"] * j), round(CIRCLE["cy"])) for j in range(len(COLOR_ORDER))]


def font(size):
    from PIL import ImageFont
    for name in FONTS:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    raise SystemExit("No monospaced font found for the palette images; install DejaVu Sans Mono.")


def draw(flavor, F):
    from PIL import Image, ImageDraw
    S = 2                                                     # supersampling for smooth edges
    n, c = F["neutrals"], F["colors"]
    im = Image.new("RGB", (W * S, H * S), n["canvas"])
    d = ImageDraw.Draw(im)
    for i, t in enumerate(NEUTRAL_ORDER):
        x = SWATCH["x0"] + SWATCH["step"] * i
        box = [x * S, SWATCH["y0"] * S, (x + SWATCH["w"]) * S, (SWATCH["y0"] + SWATCH["h"]) * S]
        d.rounded_rectangle(box, radius=SWATCH["radius"] * S, fill=n[t], outline=n["edge"], width=SWATCH["border"] * S)
    for j, t in enumerate(COLOR_ORDER):
        cx, cy, r = CIRCLE["cx0"] + CIRCLE["step"] * j, CIRCLE["cy"], CIRCLE["r"]
        d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=c[t])
    im = im.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    tx, ty, ts = TEXT["title"]
    d.text((tx, ty), f"TWILIGHT {flavor.upper()}", font=font(ts), fill=n["faint"], anchor="lt")
    label = {"sea-salt": "Sea Salt"}
    for i, t in enumerate(NEUTRAL_ORDER):
        x = SWATCH["x0"] + SWATCH["step"] * i
        d.text((x, TEXT["neutral_name"]), t.capitalize(), font=font(TEXT["name_size"]), fill=n["body"], anchor="lt")
        d.text((x, TEXT["neutral_hex"]), n[t], font=font(TEXT["hex_size"]), fill=n["faint"], anchor="lt")
    for j, t in enumerate(COLOR_ORDER):
        x = CIRCLE["cx0"] + CIRCLE["step"] * j - CIRCLE["r"]
        d.text((x, TEXT["color_name"]), label.get(t, t.capitalize()), font=font(TEXT["name_size"]), fill=n["body"], anchor="lt")
        d.text((x, TEXT["color_hex"]), c[t], font=font(TEXT["hex_size"]), fill=n["faint"], anchor="lt")
    return im


def image_errors(P, root=ROOT):
    """Each palette image exists and shows the JSON: every swatch and circle center is the token's exact color."""
    from PIL import Image
    errs = []
    for f, F in P.items():
        path = root / "assets" / f"palette-{f}.png"
        if not path.exists():
            errs.append(f"assets/palette-{f}.png is missing")
            continue
        im = Image.open(path).convert("RGB")
        if im.size != (W, H):
            errs.append(f"assets/palette-{f}.png is {im.size[0]}×{im.size[1]}, the layout is {W}×{H}")
            continue
        for (x, y), t in zip(swatch_centers(), NEUTRAL_ORDER):
            got = "#%02x%02x%02x" % im.getpixel((x, y))
            if got != F["neutrals"][t]:
                errs.append(f"assets/palette-{f}.png: {t} swatch is {got}, JSON has {F['neutrals'][t]}")
        for (x, y), t in zip(circle_centers(), COLOR_ORDER):
            got = "#%02x%02x%02x" % im.getpixel((x, y))
            if got != F["colors"][t]:
                errs.append(f"assets/palette-{f}.png: {t} circle is {got}, JSON has {F['colors'][t]}")
    return errs


# Entry points ------------------------------------------------------------------------
def document_errors(read, P, M=None):
    """Differences between each document and its rendering from the palette. `read(path)` returns the text."""
    M = M or measures(P)
    F_ = facts(P, M)
    errs = []
    for path in DOCS:
        have = read(path)
        for name in FACT.findall(have):
            if name[0] not in F_:
                errs.append(f"{path}: unknown fact `{name[0]}`")
        want = render(have, P, M, F_)
        for no, (a, b) in enumerate(zip(have.split("\n"), want.split("\n")), 1):
            if a != b:
                errs.append(f"{path}:{no}: differs from the palette (run scripts/docs.py)")
    return errs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report differences and exit 1 if any; change nothing")
    a = ap.parse_args()
    P = json.loads((ROOT / "palette/twilight.json").read_text())["flavors"]
    if a.check:
        errs = document_errors(lambda p: (ROOT / p).read_text(), P) + image_errors(P)
        print("\n".join(errs) or "documents and images match the palette")
        sys.exit(1 if errs else 0)
    M = measures(P)
    F_ = facts(P, M)
    for path in DOCS:
        (ROOT / path).write_text(render((ROOT / path).read_text(), P, M, F_))
    for f, F in P.items():
        draw(f, F).save(ROOT / "assets" / f"palette-{f}.png", optimize=True)
    print("rewrote", ", ".join(DOCS), "and", ", ".join(f"assets/palette-{f}.png" for f in P))


if __name__ == "__main__":
    main()
