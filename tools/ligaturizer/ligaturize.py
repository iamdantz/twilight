#!/usr/bin/env python3
# Ligaturizer: Fira Code's programming ligatures for other monospaced fonts.
#
# Copyright (C) the Ligaturizer contributors (https://github.com/ToxicFrog/Ligaturizer)
# Copyright (C) 2026 José D. Gutiérrez
#
# This program is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License (LICENSE) for more details.
#
# Modified in 2026 from Ligaturizer's ligaturize.py: rewritten on fontTools and glyphsLib
# (no FontForge); takes Fira Code 6's contextual rules and every glyph they output instead of
# single .liga glyphs; matches weight, math axis and slant to the receiving font; works on
# Glyphs design sources as well as on static TrueType fonts; the feature tag is configurable.
"""Add Fira Code's programming ligatures to a monospaced font.

    ligaturize.py extract FiraCode.glyphs --out DIR
        write calt.fea and NotSpace.txt for a Fira Code source directory (see fira.py)
    ligaturize.py glyphs SOURCE.glyphs --fira DIR [--config FILE] [--output FILE]
        add the ligatures to a Glyphs design source, in every master
    ligaturize.py font FONT.ttf --fira DIR [--config FILE] [--output-dir DIR] [--prefix Liga]
        add the ligatures to a static TrueType font, renamed with a prefix

What is added, as Ligaturizer does: Fira Code's glyphs scaled to the receiving font's em and,
horizontally, to its cell, so a ligature of n characters covers n cells; and the rules that
put them in the text. What changed since Ligaturizer:

- Fira Code 6 builds much of its set from one-cell pieces and contextual rules (arrows of any
  length, rows of # and _). The rules are taken verbatim from Fira Code's calt feature, less a
  configurable list of lookups (ligatures.py), and with them every glyph they output.
- Weight: Fira Code's outlines are taken at the point of its weight axis (extended past either
  end when needed) where its hyphen is as thick as the receiving font's, in every master.
- Math axis: every glyph is moved so the center of Fira Code's hyphen lands on the center of
  the receiving font's.
- Slant: in italic masters and fonts the glyphs are slanted by the italic angle about that axis.
- Contours are turned the TrueType way (clockwise around ink) wherever Fira Code turns them
  the other way.
- The rules can go to any feature: calt (on by default, as in Fira Code) or a stylistic set
  (opt-in).

The configuration file (JSON) may set "feature" (default "calt"), "description" (the name a
stylistic set shows in applications), "exclude" (lookup names,
replacing the default list), "classes" (glyph classes the extra rules use, name: [glyphs]) and
"rules" (lookup name: [lines added at the start of that lookup]).

Fira Code is licensed under the SIL Open Font License 1.1, which allows its glyphs in another
font only if the result is distributed under the same license, keeps Fira Code's copyright
notice (added here to the receiving font's) and is not sold by itself. Use this program only on
fonts whose license allows that, and rename any font that has a Reserved Font Name.
"""
import argparse
import json
import math
import sys
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.basePen import BasePen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fira  # noqa: E402
from ligatures import EXCLUDED  # noqa: E402


# ---------- configuration and rules ----------

def load_config(path):
    config = json.loads(Path(path).read_text(encoding="utf-8")) if path else {}
    config.setdefault("feature", "calt")
    config.setdefault("exclude", sorted(EXCLUDED))
    config.setdefault("classes", {})
    config.setdefault("rules", {})
    return config


def prepare(source, config, names, cmap):
    """The rules for a font with these glyph names and character map.

    Returns (classes, lookups, outputs): class definitions and lookups as feature code in the
    font's glyph names, and the Fira Code glyphs to add."""
    blocks = [(n, b) for n, b in fira.lookups(source.code) if n not in set(config["exclude"])]
    unknown = set(config["rules"]) - {n for n, _ in blocks}
    if unknown:
        raise SystemExit(f"rules for lookups that are not taken: {', '.join(sorted(unknown))}")
    outputs = fira.outputs(blocks)
    clash = [g for g in outputs if g in names]
    if clash:
        raise SystemExit(f"the font already has glyphs named as Fira Code's: {', '.join(clash[:8])}")

    def target(name):
        """The font's glyph for one of Fira Code's input glyphs: same character, else same name."""
        cp = source.unicode.get(name)
        if cp is not None and cp in cmap:
            return cmap[cp]
        return name if name in names else None

    mapping, missing = {}, []
    for name in sorted(fira.inputs(blocks)):
        found = target(name)
        if found is None:
            missing.append(name)
        else:
            mapping[name] = found
    if missing:
        raise SystemExit(f"the font lacks glyphs Fira Code's rules read: {', '.join(missing)}")
    defined = {}
    used = set().union(*(fira.classes([b]) for b in blocks)) if blocks else set()
    if "NotSpace" in used:
        defined["NotSpace"] = [g for g in (target(n) for n in source.not_space) if g]
    for name, members in config["classes"].items():
        absent = [g for g in members if g not in names]
        if absent:
            raise SystemExit(f"class {name} names glyphs the font lacks: {', '.join(absent)}")
        defined[name] = members
    undefined = used - set(defined) - {"NotSpace"}
    if undefined:
        raise SystemExit(f"Fira Code's rules use classes this program does not define: {', '.join(undefined)}")
    code = []
    for name, block in blocks:
        block = fira.rename(block, mapping)
        extra = config["rules"].get(name)
        if extra:
            head, rest = block.split("{", 1)
            block = head + "{\n" + "".join(f"  {line}\n" for line in extra) + rest.lstrip("\n")
        code.append(block)
    classes = "\n".join(f"@{n} = [{' '.join(m)}];" for n, m in defined.items())
    return classes, "\n\n".join(code) + "\n", outputs


# ---------- outlines ----------

class Graft:
    """Where Fira Code's glyphs go in one master or font: the point of Fira Code's weight axis
    and the transform (em and cell scale, math axis, slant)."""

    def __init__(self, source, upm, cell, thickness, axis, italic_angle):
        self.source = source
        self.t = source.weight(thickness, upm)
        sx, sy = cell / source.advance, upm / source.upm
        self.dy = axis - source.hyphen(self.t)[1] * sy
        s = math.tan(math.radians(italic_angle))
        # x' = sx x + s (y' - axis), y' = sy y + dy
        self.transform = Transform(sx, 0, s * sy, sy, s * (self.dy - axis), self.dy)

    def replay(self, name, pen):
        """Draw the glyph, contours turned the TrueType way (see FiraCode.contours)."""
        wrapped = TransformPen(pen, self.transform)
        for ops in self.source.contours(name, self.t):
            for op, args in ops:
                getattr(wrapped, op)(*args)

    def describe(self):
        return f"Fira Code weight position {self.t:+.3f}, moved {self.dy:+.1f} units"


class GlyphsPen(BasePen):
    """Contours as Glyphs nodes (x, y, type), cubic: a quadratic segment is raised to the cubic
    that draws it exactly (BasePen's default)."""

    def __init__(self):
        super().__init__(None)
        self.contours, self.nodes, self.start = [], None, None

    def _moveTo(self, pt):
        self.nodes, self.start = [], pt

    def _lineTo(self, pt):
        self.nodes.append((*pt, "line"))

    def _curveToOne(self, p1, p2, p3):
        self.nodes += [(*p1, "offcurve"), (*p2, "offcurve"), (*p3, "curve")]

    def _closePath(self):
        last = self.nodes[-1][:2] if self.nodes else self.start
        if last != tuple(self.start):
            self.nodes.append((*self.start, "line"))
        nodes = self.nodes[-1:] + self.nodes[:-1]  # start on the on-curve node that closes it
        self.contours.append(reverse(nodes))  # TrueType contours run the other way
        self.nodes = None

    _endPath = _closePath


def reverse(points):
    """Reverse a closed contour. A node's type names the segment that ends at it, so after
    reversal each on-curve node takes the type of the on-curve node that followed it."""
    on = [i for i, p in enumerate(points) if p[2] != "offcurve"]
    kinds = [p[2] for p in points]
    for a, b in zip(on, on[1:] + on[:1]):
        kinds[a] = points[b][2]
    return [(x, y, k) for (x, y, _), k in reversed(list(zip(points, kinds)))]


def append(text, sentence):
    text = (text or "").strip()
    return f"{text if not text or text.endswith('.') else text + '.'} {sentence}".strip()


def notice(source):
    return f"Programming ligatures from Fira Code: {source.copyright.rstrip('.')}."


# ---------- Glyphs design sources ----------

def ligaturize_glyphs(path, source, config, output=None):
    import glyphsLib
    from glyphsLib.classes import GSClass, GSFeature, GSFontInfoValue, GSGlyph, GSLayer, GSNode, GSPath

    font = glyphsLib.GSFont(str(path))
    names = {g.name for g in font.glyphs if g.export}
    cmap = {}
    for g in font.glyphs:
        if g.export:
            for u in g.unicodes or []:
                cmap[int(u, 16)] = g.name
    classes, code, outputs = prepare(source, config, names, cmap)

    def layer(name, master):
        return next(l for l in font.glyphs[name].layers if l.layerId == master.id)

    grafts = {}
    for master in font.masters:
        hyphen, m = layer(cmap[ord("-")], master), layer(cmap[ord("m")], master)
        if hyphen.components:
            raise SystemExit("the hyphen must be drawn with paths")
        if hyphen.width != m.width:
            raise SystemExit("the font is not monospaced")
        ys = [n.position.y for p in hyphen.paths for n in p.nodes]
        grafts[master.id] = Graft(source, font.upm, m.width, max(ys) - min(ys), (max(ys) + min(ys)) / 2,
                                  master.italicAngle)
        print(f"  {master.name}: {grafts[master.id].describe()}")
    for name in outputs:
        glyph = GSGlyph(name)
        glyph.category, glyph.subCategory = "Symbol", None
        font.glyphs.append(glyph)
        for master in font.masters:
            new = GSLayer()
            new.layerId = new.associatedMasterId = master.id
            new.width = layer(cmap[ord("m")], master).width
            pen = GlyphsPen()
            grafts[master.id].replay(name, pen)
            for contour in pen.contours:
                gpath = GSPath()
                gpath.closed = True
                for x, y, kind in contour:
                    gpath.nodes.append(GSNode((round(x), round(y)), kind))
                new.paths.append(gpath)
            glyph.layers.append(new)
    for line in classes.splitlines():
        name, members = line[1:].split(" = [", 1)
        if any(c.name == name for c in font.classes):
            raise SystemExit(f"the font already has a class named {name}")
        font.classes.append(GSClass(name, members.rstrip("];")))
    existing = next((f for f in font.features if f.name == config["feature"]), None)
    if config.get("description") and config["feature"].startswith("ss"):
        code = f'featureNames {{\n  name "{config["description"]}";\n}};\n\n' + code
    if existing:
        existing.code = existing.code.rstrip("\n") + "\n\n" + code
    else:
        font.features.append(GSFeature(config["feature"], code))
    record = next((p for p in font.properties if p.key == "copyrights"), None)
    localized = getattr(record, "_localized_values", None)
    if record is None:
        font.properties.append(GSFontInfoValue("copyrights", notice(source)))
    elif localized:
        record._localized_values = {lang: append(text, notice(source)) for lang, text in localized.items()}
    else:
        record.value = append(record.value, notice(source))
    font.save(str(output or path))
    print(f"{Path(path).name}: {len(code.split('lookup ')) - 1} lookups, {len(outputs)} glyphs, "
          f"in {config['feature']}")


# ---------- static TrueType fonts ----------

def ligaturize_font(path, source, config, output_dir, prefix, output_name):
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    from fontTools.ttLib import TTFont

    font = TTFont(path)
    if "fvar" in font or "glyf" not in font:
        raise SystemExit("font mode takes static TrueType fonts; use glyphs mode on the design sources")
    order = font.getGlyphOrder()
    cmap = font.getBestCmap()
    names = set(order)
    classes, code, outputs = prepare(source, config, names, cmap)
    upm, hmtx, glyf = font["head"].unitsPerEm, font["hmtx"], font["glyf"]
    cell = hmtx[cmap[ord("m")]][0]
    if hmtx[cmap[ord("-")]][0] != cell:
        raise SystemExit("the font is not monospaced")
    hyphen = glyf[cmap[ord("-")]]
    hyphen.recalcBounds(glyf)
    graft = Graft(source, upm, cell, hyphen.yMax - hyphen.yMin, (hyphen.yMax + hyphen.yMin) / 2,
                  -font["post"].italicAngle)
    print(f"  {graft.describe()}")
    font.setGlyphOrder(order + outputs)
    for name in outputs:
        pen = TTGlyphPen(None)
        graft.replay(name, pen)
        glyph = pen.glyph()
        glyph.recalcBounds(glyf)
        glyf[name] = glyph
        hmtx[name] = (cell, getattr(glyph, "xMin", 0))
    if font["post"].formatType == 3.0:
        font["post"].formatType = 2.0  # keep the glyph names the rules use
    if config.get("description") and config["feature"].startswith("ss"):
        code = f'featureNames {{\n  name "{config["description"]}";\n}};\n\n' + code
    fea = (f"languagesystem DFLT dflt;\nlanguagesystem latn dflt;\n{classes}\n"
           f"feature {config['feature']} {{\n{code}}} {config['feature']};\n")
    old = font["GSUB"] if "GSUB" in font else None
    if old is not None:
        del font["GSUB"]
    addOpenTypeFeaturesFromString(font, fea, tables=["GSUB"])
    if old is not None:
        merge_gsub(old.table, font["GSUB"].table)
        font["GSUB"] = old
    rename_font(font, prefix, output_name)
    for record in font["name"].names:
        if record.nameID == 0:
            record.string = append(record.toUnicode(), notice(source))
    out = Path(output_dir or Path(path).parent) / f"{font['name'].getDebugName(6)}.ttf"
    font.save(out)
    print(f"{out}: {len(outputs)} glyphs, in {config['feature']}")


def lookup_indices(obj, offset, seen=None):
    """Shift every lookup index inside a lookup's subtables (contextual rules call lookups)."""
    seen = seen if seen is not None else set()
    if id(obj) in seen or isinstance(obj, (str, bytes, int, float)) or obj is None:
        return
    seen.add(id(obj))
    if isinstance(obj, list):
        for item in obj:
            lookup_indices(item, offset, seen)
        return
    if hasattr(obj, "LookupListIndex") and isinstance(obj.LookupListIndex, int):
        obj.LookupListIndex += offset
    for value in getattr(obj, "__dict__", {}).values():
        lookup_indices(value, offset, seen)


def merge_gsub(old, new):
    """Append new's lookups and features to old, keeping old's."""
    if getattr(old, "FeatureVariations", None):
        raise SystemExit("the font's GSUB has feature variations; not supported")
    offset = len(old.LookupList.Lookup)
    for lookup in new.LookupList.Lookup:
        lookup_indices(lookup.SubTable, offset)
    old.LookupList.Lookup += new.LookupList.Lookup
    old.LookupList.LookupCount = len(old.LookupList.Lookup)
    records = list(old.FeatureList.FeatureRecord)
    added = []
    for rec in new.FeatureList.FeatureRecord:
        rec.Feature.LookupListIndex = [i + offset for i in rec.Feature.LookupListIndex]
        added.append(len(records))
        records.append(rec)
    order = sorted(range(len(records)), key=lambda i: (records[i].FeatureTag, i))
    position = {old_index: new_index for new_index, old_index in enumerate(order)}
    old.FeatureList.FeatureRecord = [records[i] for i in order]
    old.FeatureList.FeatureCount = len(records)
    for script in old.ScriptList.ScriptRecord:
        systems = [script.Script.DefaultLangSys] + [r.LangSys for r in script.Script.LangSysRecord]
        for system in filter(None, systems):
            system.FeatureIndex = sorted(position[i] for i in list(system.FeatureIndex) + added)
            system.FeatureCount = len(system.FeatureIndex)
            if system.ReqFeatureIndex != 0xFFFF:
                system.ReqFeatureIndex = position[system.ReqFeatureIndex]


def rename_font(font, prefix, output_name):
    """Rename the family, as Ligaturizer does: with a prefix, or to a new name."""
    name = font["name"]
    family = name.getDebugName(16) or name.getDebugName(1)
    new = output_name or f"{prefix} {family}".strip()
    if new == family:
        return
    for record in name.names:
        if record.nameID in (1, 3, 4, 16, 18, 21):
            record.string = record.toUnicode().replace(family, new)
        elif record.nameID in (6, 20):
            record.string = record.toUnicode().replace(family.replace(" ", ""), new.replace(" ", ""))


# ---------- command line ----------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    ex = sub.add_parser("extract", help="write calt.fea and NotSpace.txt from FiraCode.glyphs")
    ex.add_argument("glyphs")
    ex.add_argument("--out", required=True)
    gl = sub.add_parser("glyphs", help="ligaturize a Glyphs design source")
    gl.add_argument("source")
    gl.add_argument("--output")
    fo = sub.add_parser("font", help="ligaturize a static TrueType font")
    fo.add_argument("font")
    fo.add_argument("--output-dir")
    fo.add_argument("--prefix", default="Liga", help="family name prefix (default: Liga)")
    fo.add_argument("--output-name", default="", help="new family name, instead of the prefix")
    for p in (gl, fo):
        p.add_argument("--fira", required=True, help="Fira Code source directory (see fira.py)")
        p.add_argument("--config", help="JSON configuration (see above)")
    args = parser.parse_args()
    if args.command == "extract":
        fira.extract(args.glyphs, args.out)
        return
    source, config = fira.FiraCode(args.fira), load_config(args.config)
    if args.command == "glyphs":
        ligaturize_glyphs(args.source, source, config, args.output)
    else:
        ligaturize_font(args.font, source, config, args.output_dir, args.prefix, args.output_name)


if __name__ == "__main__":
    main()
