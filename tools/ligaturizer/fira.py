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
# Modified in 2026 from Ligaturizer's ligaturize.py: reads Fira Code 6 (its variable font and
# the contextual rules of its design source) with fontTools instead of FontForge.
"""Fira Code as a source of ligatures: its rules and its glyphs along the weight axis.

A source directory holds three files from one Fira Code release, all under the SIL Open Font
License 1.1 (keep Fira Code's OFL.txt beside them):

- FiraCode-VF.ttf, the variable font of the release;
- calt.fea, the calt feature code of FiraCode.glyphs at the release tag;
- NotSpace.txt, the NotSpace glyph class of FiraCode.glyphs, one name per line.

`ligaturize.py extract` writes the last two from FiraCode.glyphs.
"""
import re
from pathlib import Path

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont

NAME = re.compile(r"\\?[A-Za-z_.][\w.\-]*")
KEYWORDS = {"lookup", "sub", "substitute", "by", "ignore", "pos", "from", "useExtension"}
LOOKUP = re.compile(r"lookup (\S+) \{.*?\} \1;", re.S)


def extract(glyphs_path, out_dir):
    """Write calt.fea and NotSpace.txt from Fira Code's design source."""
    import glyphsLib

    font = glyphsLib.GSFont(str(glyphs_path))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    calt = next(f for f in font.features if f.name == "calt").code
    (out_dir / "calt.fea").write_text(calt if calt.endswith("\n") else calt + "\n", encoding="utf-8")
    not_space = next(c for c in font.classes if c.name == "NotSpace").code.split()
    (out_dir / "NotSpace.txt").write_text("\n".join(not_space) + "\n", encoding="utf-8")


def strip_comments(code):
    return re.sub(r"#.*", "", code)


def lookups(code):
    """The lookups of a feature file, as (name, code), in order."""
    return [(m.group(1), m.group(0)) for m in LOOKUP.finditer(code)]


def body(block):
    return strip_comments(block).split("{", 1)[1].rsplit("}", 1)[0]


def outputs(blocks):
    """Glyphs the rules put in the text, in order of first appearance."""
    seen = {}
    for _, block in blocks:
        for m in re.finditer(r"\bby\s+([^;]+);", strip_comments(block)):
            for name in NAME.findall(m.group(1)):
                seen.setdefault(name.lstrip("\\"), None)
    return list(seen)


def inputs(blocks):
    """Glyph names the rules read: every name but keywords, lookups, classes and outputs."""
    names = set()
    for _, block in blocks:
        text = re.sub(r"@\w+", "", body(block))
        names |= {t.lstrip("\\").rstrip("'") for t in NAME.findall(text) if t not in KEYWORDS}
    return names - set(outputs(blocks)) - {name for name, _ in blocks}


def classes(blocks):
    names = set()
    for _, block in blocks:
        names |= set(re.findall(r"@(\w+)", body(block)))
    return names


def rename(block, mapping):
    """The lookup with glyph names replaced through mapping (names not in it are kept)."""
    def sub(m):
        token = m.group(0)
        bare = token.lstrip("\\")
        return mapping.get(bare, bare) if bare in mapping else token
    head, rest = block.split("{", 1)
    inner, tail = rest.rsplit("}", 1)
    return head + "{" + NAME.sub(sub, strip_comments(inner)) + "}" + tail


class FiraCode:
    """A Fira Code source directory. Outlines are read at the two ends of the weight axis; Fira
    Code's variable font has one master at each end and nothing between, so any point of the
    axis, and of its extension past either end, is a linear blend of the two."""

    def __init__(self, directory):
        directory = Path(directory)
        self.font = TTFont(directory / "FiraCode-VF.ttf")
        self.code = (directory / "calt.fea").read_text(encoding="utf-8")
        self.not_space = (directory / "NotSpace.txt").read_text(encoding="utf-8").split()
        self.upm = self.font["head"].unitsPerEm
        self.advance = self.font["hmtx"]["hyphen"][0]
        self.unicode = {name: cp for cp, name in self.font.getBestCmap().items()}
        axes = self.font["fvar"].axes
        if len(axes) != 1 or axes[0].axisTag != "wght":
            raise SystemExit("expected a Fira Code variable font with one weight axis")
        regions = {tuple(sorted(v.axes.items())) for vs in self.font["gvar"].variations.values() for v in vs}
        if regions - {(("wght", (0.0, 1.0, 1.0)),)}:
            raise SystemExit("this Fira Code has intermediate masters; outlines are not linear in weight")
        self.ends = [self.font.getGlyphSet(location={"wght": axes[0].minValue}),
                     self.font.getGlyphSet(location={"wght": axes[0].maxValue})]
        self._recorded = {}
        self.copyright = self.font["name"].getDebugName(0)

    def _record(self, name):
        if name not in self._recorded:
            pens = []
            for glyphs in self.ends:
                pen = DecomposingRecordingPen(glyphs)
                glyphs[name].draw(pen)
                pens.append(pen.value)
            self._recorded[name] = pens
        return self._recorded[name]

    def outline(self, name, t):
        """The glyph at t (0 the light master, 1 the bold one), as recorded pen operations."""
        if self.font["hmtx"][name][0] != self.advance:
            raise SystemExit(f"Fira Code's {name} is not one cell wide")
        a, b = self._record(name)
        return [(op, [None if p is None else (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
                      for p, q in zip(pa, pb)]) for (op, pa), (_, pb) in zip(a, b)]

    def hyphen(self, t):
        """Thickness and center of the hyphen at t, in Fira Code units."""
        ys = [p[1] for _, pts in self.outline("hyphen", t) for p in pts if p]
        return max(ys) - min(ys), (max(ys) + min(ys)) / 2

    def weight(self, thickness, upm):
        """The t at which the hyphen, scaled to an em of upm units, is this thick."""
        scale = upm / self.upm
        t0, t1 = self.hyphen(0)[0] * scale, self.hyphen(1)[0] * scale
        return (thickness - t0) / (t1 - t0)
