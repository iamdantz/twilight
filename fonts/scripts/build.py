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
from glyphsLib.types import Point

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arrows  # noqa: E402
import boxdraw  # noqa: E402
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


# Units added to each side of every glyph of Twilight Text: the smallest whole value that brings
# the gray step against Twilight Code to 14 % or less at every named instance with a margin for
# rounding (24 reaches 14.0 % at ExtraLight). fonts/scripts/texture.py measures it.
TRACKING = 25


def open_spacing(font):
    """Letter-space every glyph by TRACKING units on each side, in every layer.

    Outlines and anchors move right by TRACKING and the advance grows by twice that. Every
    glyph moves alike, so components keep their offsets, marks still meet their anchors and
    kerning keeps its values; the spacing opens evenly, as letter-spacing does."""
    for glyph in font.glyphs:
        for layer in glyph.layers:
            for path in layer.paths:
                for node in path.nodes:
                    node.position = Point(node.position.x + TRACKING, node.position.y)
            for anchor in layer.anchors:
                anchor.position = Point(anchor.position.x + TRACKING, anchor.position.y)
            layer.width += 2 * TRACKING


# Changes beyond the rename, per family, in the order they apply.
STEPS = {"TwilightText": [add_arrows, open_spacing], "TwilightCode": [add_box_drawing, add_arrows]}


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
