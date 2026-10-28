"""Optional code ligatures for Twilight Code (stylistic set 1, off by default), from Fira Code 6.2.

The method follows Ligaturizer (https://github.com/ToxicFrog/Ligaturizer), which grafts Fira
Code's ligatures onto another monospaced font, brought up to date with Fira Code 6. Ligaturizer
copies each `.liga` glyph and writes one simple rule per sequence; since version 6 Fira Code
builds much of its set from pieces one cell wide (`.seq`: arrows of any length such as -->,
<==>, |-->, rows of #, ___), from per-character spacers and from rules that look at more than
the sequence itself. Copying single glyphs no longer reproduces it, so this module takes Fira
Code's whole contextual system instead:

- the rules are Fira Code's own calt lookups, verbatim (fonts/upstream/firacode/calt.fea,
  from FiraCode.glyphs at the 6.2 tag), moved to stylistic set 1 so they are opt-in, less the
  lookups that are not ligatures but contextual forms of single characters drawn for Fira Code
  (EXCLUDED: x as a multiplication sign in 0xFF and 1920x1080, punctuation raised next to
  capitals, Greek capitals) and www, the only ligature of letters; Fira Code's NotSpace class
  is limited to the glyphs Twilight Code has;
- the glyphs are every glyph those rules put in the text (ligatures, sequence pieces, centered
  forms, spacers), none of them mapped to a character, taken from Fira Code 6.2's variable font;
- each glyph is scaled from Fira Code's em (1950 units) to Twilight Code's (1000) and then
  horizontally to the cell (Fira Code's 1200-unit advance to 632), as Ligaturizer does, so a
  ligature of n characters covers n cells and the cursor and the grid are unchanged.

Three measured adjustments, where Ligaturizer leaves the source as it is:

- weight: Fira Code's two masters (300 and 700) interpolate linearly; for each Twilight master
  the glyphs are taken at the point of that line where Fira Code's hyphen is as thick as
  Twilight Code's (extrapolated past the masters where Twilight's is thinner or heavier), so
  the strokes of a ligature match the characters around it;
- axis: Fira Code's operators sit higher in the em than Atkinson's; every glyph is moved down
  so the center of Fira Code's hyphen lands on the center of Twilight Code's;
- slant: Fira Code has no italic; in the italic masters the glyphs are slanted by the italic
  angle about that axis, as the italic characters are.

One rule is added: a double hyphen before a letter opens a command-line option (--watch) and
stays plain.
"""
import hashlib
import json
import re
from pathlib import Path

from fontTools.pens.basePen import decomposeQuadraticSegment
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont

from boxdraw import reverse

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = json.loads((ROOT / "fonts" / "upstream.json").read_text(encoding="utf-8"))["ligatures"]
DIRECTORY = ROOT / MANIFEST["directory"]
NOTICE = ("Programming ligatures from Fira Code, Copyright 2014 The Fira Code Project Authors "
          "(https://github.com/tonsky/FiraCode).")
CELL = 632
EXCLUDED = {"w_w_w", "hexadecimal_x", "caltGreekUC", "caltGreekUCdiph", "lowercase_hyphen", "lowercase_plus",
            "lowercase_asterisk", "lowercase_asteriskmath", "uppercase_colon"}
LETTERS = [chr(c) for c in range(ord("A"), ord("Z") + 1)] + [chr(c) for c in range(ord("a"), ord("z") + 1)]
# the lookups that join two hyphens: as a pair, and as the start of a line or an arrow
OPTION = ({"hyphen_hyphen", "hyphen_arrows"}, "  ignore sub hyphen' hyphen @TW_Letters;\n")
NAME = re.compile(r"[A-Za-z_.][\w.\-]*")
KEYWORDS = {"lookup", "sub", "by", "ignore", "pos"}


def verify():
    for name, digest in MANIFEST["vendored"].items():
        if hashlib.sha256((DIRECTORY / name).read_bytes()).hexdigest() != digest:
            raise SystemExit(f"{DIRECTORY / name} is not the pinned Fira Code {MANIFEST['tag']} file")


def lookups():
    """Fira Code's calt lookups that Twilight Code takes, as (name, code), in Fira Code's order."""
    code = (DIRECTORY / "calt.fea").read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"lookup (\S+) \{.*?\} \1;", code, re.S):
        name, block = m.group(1), m.group(0)
        if name in EXCLUDED:
            continue
        if name in OPTION[0]:
            head, rest = block.split("\n", 1)
            block = head + "\n" + OPTION[1] + rest
        out.append((name, block))
    return out


def outputs(blocks):
    """The glyphs the rules put in the text, in order of first appearance."""
    seen = {}
    for _, block in blocks:
        for m in re.finditer(r"\bby\s+([^;]+);", re.sub(r"#.*", "", block)):
            for name in NAME.findall(m.group(1)):
                seen.setdefault(name, None)
    return list(seen)


def inputs(blocks):
    """Every glyph name the rules mention, other than lookup names and the ones they output."""
    names = set()
    for _, block in blocks:
        body = re.sub(r"#.*", "", block).split("{", 1)[1].rsplit("}", 1)[0]
        body = re.sub(r"@\w+", "", body)
        names |= {t.rstrip("'") for t in NAME.findall(body) if t not in KEYWORDS}
    return names - set(outputs(blocks)) - {name for name, _ in blocks}


def feature(blocks, glyph_names):
    """The classes the rules use (NotSpace limited to glyph_names) and the lookups."""
    not_space = [g for g in (DIRECTORY / "NotSpace.txt").read_text(encoding="utf-8").split() if g in glyph_names]
    classes = [f"@NotSpace = [{' '.join(not_space)}];", f"@TW_Letters = [{' '.join(LETTERS)}];"]
    return "\n".join(classes), "\n\n".join(block for _, block in blocks) + "\n"


class Source:
    """Fira Code's glyphs along its weight axis: at t = 0 its light master, at t = 1 its bold
    one, linear between and beyond."""

    def __init__(self, names):
        verify()
        self.font = TTFont(DIRECTORY / "FiraCode-VF.ttf")
        self.upm = self.font["head"].unitsPerEm
        self.advance = self.font["hmtx"]["hyphen"][0]
        axis = self.font["fvar"].axes[0]
        self.names = ["hyphen"] + list(names)
        self.ends = [self._record(axis.minValue), self._record(axis.maxValue)]

    def _record(self, wght):
        glyphs = self.font.getGlyphSet(location={"wght": wght})
        out = {}
        for name in self.names:
            if self.font["hmtx"][name][0] != self.advance:
                raise SystemExit(f"Fira Code's {name} is not one cell wide")
            pen = DecomposingRecordingPen(glyphs)
            glyphs[name].draw(pen)
            out[name] = pen.value
        return out

    def outline(self, name, t):
        """The glyph at t, in Fira Code units, as recorded pen operations."""
        out = []
        for (op, pa), (_, pb) in zip(self.ends[0][name], self.ends[1][name]):
            out.append((op, [None if a is None else (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
                             for a, b in zip(pa, pb)]))
        return out

    def hyphen(self, t):
        """Thickness and center of the hyphen at t, in Fira Code units."""
        ys = [p[1] for _, pts in self.outline("hyphen", t) for p in pts if p]
        return max(ys) - min(ys), (max(ys) + min(ys)) / 2

    def weight(self, thickness):
        """The t at which the hyphen, scaled to 1000 units, is this thick."""
        scale = 1000 / self.upm
        t0, t1 = self.hyphen(0)[0] * scale, self.hyphen(1)[0] * scale
        return (thickness - t0) / (t1 - t0)


def contours(operations, transform):
    """Recorded TrueType operations to Glyphs contours: cubic (each quadratic segment raised
    exactly), counter-clockwise for ink."""
    out = []
    for op, pts in operations:
        if op == "moveTo":
            start = current = pts[0]
            segs = []
        elif op == "lineTo":
            segs.append([(pts[0], "line")])
            current = pts[0]
        elif op == "qCurveTo":
            if pts[-1] is None:
                raise ValueError("contour without on-curve points")
            for q, p in decomposeQuadraticSegment(pts):
                c1 = (current[0] + 2 / 3 * (q[0] - current[0]), current[1] + 2 / 3 * (q[1] - current[1]))
                c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
                segs.append([(c1, "offcurve"), (c2, "offcurve"), (p, "curve")])
                current = p
        elif op == "curveTo":
            segs.append([(pts[0], "offcurve"), (pts[1], "offcurve"), (pts[2], "curve")])
            current = pts[2]
        elif op in ("closePath", "endPath"):
            if current != start:
                segs.append([(start, "line")])
            nodes = [n for seg in segs for n in seg]
            nodes = nodes[-1:] + nodes[:-1]  # start on the on-curve point that closes the contour
            out.append(reverse([(*transform(*xy), kind) for xy, kind in nodes]))
    return out


class Master:
    """The glyphs for one Twilight Code master.

    thickness, axis: the hyphen's thickness and center in that master; slant: the tangent of its
    italic angle."""

    def __init__(self, source, thickness, axis, slant):
        self.source, self.slant, self.axis = source, slant, axis
        self.t = source.weight(thickness)
        self.sx, self.sy = CELL / source.advance, 1000 / source.upm
        self.dy = axis - source.hyphen(self.t)[1] * self.sy

    def transform(self, x, y):
        x, y = x * self.sx, y * self.sy + self.dy
        return x + self.slant * (y - self.axis), y

    def glyph(self, name):
        return contours(self.source.outline(name, self.t), self.transform)
