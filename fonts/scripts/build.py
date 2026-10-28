"""Build Twilight Text and Twilight Code from the pinned upstream sources.

Each upstream design source is copied, renamed and given the derivative's metadata (family
name, copyright line, manufacturer, description, version); the outlines, spacing, kerning and
features are untouched. The copies are compiled with gftools builder, with the upstream
build configuration, into fonts/build/<file>/fonts/: variable TTF, static TTF and WOFF2.

    python fonts/scripts/build.py              build both families
    python fonts/scripts/build.py --only TwilightCode
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import glyphsLib
import yaml
from glyphsLib.classes import GSFontInfoValue, GSGlyph, GSLayer, GSNode, GSPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arrows  # noqa: E402
import boxdraw  # noqa: E402
import braille  # noqa: E402
import symbols  # noqa: E402
import upstream  # noqa: E402

ROOT = upstream.ROOT
BUILD = ROOT / "fonts" / "build"
PROJECT = "https://github.com/iamdantz/twilight"
HOLDER = "José D. Gutiérrez"
YEAR = 2026


def metadata(family):
    up = family["upstream"]
    return {
        "copyright": f"{{original}} Copyright {YEAR} {HOLDER} ({PROJECT}).",
        "manufacturer": "Twilight",
        "manufacturerURL": PROJECT,
        # name ID 10, kept under the 200 characters applications expect
        "description": f"Derived from {up['family']} {up['version']}, designed by {{designers}}. "
                       f"Part of Twilight.",
    }


def prop(font, key, value=None):
    """Read or set a Glyphs 3 font-info property (name table source), adding it when absent."""
    entry = next((p for p in font.properties if p.key == key), None)
    localized = getattr(entry, "_localized_values", None)
    if value is None:
        return (localized.get("dflt", "") if localized else entry.value) if entry else ""
    if localized:
        entry._localized_values = {"dflt": value}
    elif entry:
        entry.value = value
    else:
        font.properties.append(GSFontInfoValue(key, value))


def master_cell(font, master):
    """The cell of one master: advance, typographic line box and hyphen thickness."""
    params = {p.name: p.value for p in master.customParameters}
    hyphen = next(l for l in font.glyphs["hyphen"].layers if l.layerId == master.id)
    ys = [n.position.y for p in hyphen.paths for n in p.nodes]
    width = next(l for l in font.glyphs["bar"].layers if l.layerId == master.id).width
    return boxdraw.Cell(width, params["typoDescender"], params["typoAscender"], max(ys) - min(ys))


def layer(font, glyph, master):
    return next(l for l in font.glyphs[glyph].layers if l.layerId == master.id)


def add_glyphs(font, codepoints, name, draw):
    """New glyphs, one layer per master: draw(master, cp) gives the advance and the contours,
    each a list of (x, y, node type)."""
    for cp in codepoints:
        glyph_name = name(cp)
        if font.glyphs[glyph_name] is not None:
            raise SystemExit(f"{glyph_name} already exists in {font.familyName}")
        glyph = GSGlyph(glyph_name)
        glyph.unicode = f"{cp:04X}"
        font.glyphs.append(glyph)
        for master in font.masters:
            new = GSLayer()
            new.layerId = new.associatedMasterId = master.id
            new.width, contours = draw(master, cp)
            for contour in contours:
                path = GSPath()
                path.closed = True
                for x, y, kind in contour:
                    path.nodes.append(GSNode((round(x), round(y)), kind))
                new.paths.append(path)
            glyph.layers.append(new)


def add_box_drawing(font):
    """Box drawing, block elements and Powerline separators (fonts/scripts/boxdraw.py)."""
    cells = {m.id: master_cell(font, m) for m in font.masters}

    def draw(master, cp):
        cell = cells[master.id]
        return cell.w, boxdraw.contours(cell, cp)
    add_glyphs(font, boxdraw.CODEPOINTS, boxdraw.glyph_name, draw)


def add_arrows(font):
    """Arrows (fonts/scripts/arrows.py), measured from each master's plus and equal signs."""
    widths = {layer(font, g, m).width for g in ("i", "m", "plus") for m in font.masters}
    cell = widths.pop() if len(widths) == 1 else None  # monospaced: every glyph fills one cell

    def on_curve(glyph, master):
        return [(n.position.x, n.position.y) for p in layer(font, glyph, master).paths for n in p.nodes
                if n.type != "offcurve"]
    metrics = {m.id: arrows.Metrics(on_curve("plus", m), on_curve("equal", m), m.italicAngle, cell)
               for m in font.masters}
    add_glyphs(font, arrows.codepoints(cell), arrows.glyph_name,
               lambda master, cp: arrows.glyph(metrics[master.id], cp))


def resolved(font, master, name):
    """A glyph's outline in one master, components resolved, as lists of (x, y, node type)."""
    lay = layer(font, name, master)
    out = [[(n.position.x, n.position.y, n.type) for n in p.nodes] for p in lay.paths]
    for comp in lay.components:
        a, b, c, d, tx, ty = comp.transform
        for contour in resolved(font, master, comp.name):
            out.append([(a * x + c * y + tx, b * x + d * y + ty, k) for x, y, k in contour])
    return out


def add_symbols(font):
    """Shapes, primes, brackets and derived signs (fonts/scripts/symbols.py)."""
    widths = {layer(font, g, m).width for g in ("i", "m", "plus") for m in font.masters}
    cell = widths.pop() if len(widths) == 1 else None
    # ufo2ft's default subscript offset, which the compiled OS/2 table declares (the sources set none)
    subscript = round(0.075 * font.upm)
    masters = {}
    for m in font.masters:
        if m.italicAngle not in (0, symbols.ITALIC_ANGLE):
            raise SystemExit(f"{m.name}: italic angle {m.italicAngle}, symbols.py assumes {symbols.ITALIC_ANGLE}")
        on_curve = lambda g, m=m: [(x, y) for c in resolved(font, m, g) for x, y, k in c if k != "offcurve"]
        metrics = arrows.Metrics(on_curve("plus"), on_curve("equal"), m.italicAngle, cell)
        masters[m.id] = symbols.Master(metrics, lambda g, m=m: resolved(font, m, g),
                                       lambda g, m=m: layer(font, g, m).width, m.capHeight, m.xHeight, subscript)
    symbols.prepare(list(masters.values()))
    add_glyphs(font, symbols.codepoints(cell), symbols.glyph_name,
               lambda master, cp: symbols.glyph(masters[master.id], cp))


def add_braille(font):
    """Braille patterns (fonts/scripts/braille.py), dots from each master's period."""
    def draw(master, cp):
        cell = master_cell(font, master)
        return cell.w, braille.contours(cell.w, cell.b, cell.t, resolved(font, master, "period"), cp)
    add_glyphs(font, braille.CODEPOINTS, braille.glyph_name, draw)


# Changes beyond the rename, per family, in the order they apply.
STEPS = {"TwilightText": [add_arrows, add_symbols],
         "TwilightCode": [add_box_drawing, add_arrows, add_symbols, add_braille]}


def rename(src, dst, family):
    font = glyphsLib.GSFont(str(src))
    for step in STEPS.get(family["file"], []):
        step(font)
    meta = metadata(family)
    font.familyName = family["family"]
    prop(font, "copyrights", meta["copyright"].format(original=prop(font, "copyrights").rstrip(".") + "."))
    prop(font, "manufacturers", meta["manufacturer"])
    prop(font, "manufacturerURL", meta["manufacturerURL"])
    prop(font, "descriptions", meta["description"].format(designers=prop(font, "designers")))
    major, minor = family["version"].split(".")
    font.versionMajor, font.versionMinor = int(major), int(minor)
    font.save(str(dst))


def configure(family, sources_dir, names):
    config = yaml.safe_load((ROOT / family["directory"] / "sources" / "config.yaml").read_text(encoding="utf-8"))
    old, new = family["upstream"]["file"], family["file"]
    config["sources"] = names
    config["familyName"] = family["family"]
    config["stat"] = {key.replace(old, new): value for key, value in config.get("stat", {}).items()}
    config["buildOTF"] = False
    (sources_dir / "config.yaml").write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")


def build(family):
    out = BUILD / family["file"]
    shutil.rmtree(out, ignore_errors=True)
    sources_dir = out / "sources"
    sources_dir.mkdir(parents=True)
    old, new = family["upstream"]["file"], family["file"]
    names = []
    for src in sorted((ROOT / family["directory"] / "sources").glob("*.glyphs")):
        name = src.name.replace(old, new)
        rename(src, sources_dir / name, family)
        names.append(name)
    configure(family, sources_dir, names)
    env = dict(os.environ, PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", ""))
    subprocess.run([str(Path(sys.executable).parent / "gftools"), "builder", "config.yaml"],
                   cwd=sources_dir, env=env, check=True)
    fonts = sorted((out / "fonts").rglob("*.*"))
    print(f"{family['family']}: {len(fonts)} files in {(out / 'fonts').relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", help="build one family, by file name (TwilightText or TwilightCode)")
    args = parser.parse_args()
    if not upstream.verify():
        sys.exit("the upstream files changed; run upstream.py verify for details")
    for family in upstream.load()["families"]:
        if args.only in (None, family["file"]):
            build(family)
