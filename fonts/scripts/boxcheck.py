"""Box drawing in Twilight Code: every line reaches the cell edge and meets its neighbor.

Two checks:

1. Edges, at every named instance of both variable fonts, on the outlines. Where a glyph has
   an arm, the ink on that cell edge must cover the band of the reference line of the same
   style (─ ━ ═ on the left and right edges, │ ┃ ║ on the top and bottom edges), within half a
   unit; where it has no arm, the edge must be empty; █ must cover every edge. Arms are read
   from the Unicode names, as boxdraw.py does, and the reference bands are measured, not
   assumed. Dashes and diagonals are left out: they do not reach the edges by design.
2. Tiling, in the hinted static fonts at 12 to 24 px. Rows of ─ ━ ═ and columns of │ ┃ ║ █
   are rendered as a terminal lays them out, one glyph per cell on a whole-pixel grid (the
   cell is the advance and the line box, rounded). Along each line the ink must not drop
   below half of its own peak.

    python fonts/scripts/boxcheck.py
"""
import sys
import tempfile
from pathlib import Path

import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
import pathops
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import boxdraw  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "fonts" / "build" / "TwilightCode" / "fonts"
EDGE = 1  # depth, in font units, of the strip read on each cell edge
TOLERANCE = 0.5  # font units; interpolated instances keep fractional coordinates
PAD = 10
REFERENCE = {("h", "light"): "─", ("h", "heavy"): "━", ("h", "double"): "═",
             ("v", "light"): "│", ("v", "heavy"): "┃", ("v", "double"): "║"}


def outline(font, char):
    """The glyph's outline with overlaps removed."""
    glyphs = font.getGlyphSet()
    path = pathops.Path()
    glyphs[font.getBestCmap()[ord(char)]].draw(path.getPen(glyphSet=glyphs))
    return pathops.simplify(path, fix_winding=True)


def strip(path, side, cell):
    """Intervals the ink covers on one edge, read from a strip EDGE units deep."""
    w, b, t = cell
    box = {"left": (0, b, EDGE, t), "right": (w - EDGE, b, w, t),
           "down": (0, b, w, b + EDGE), "up": (0, t - EDGE, w, t)}[side]
    rect = pathops.Path()
    pen = rect.getPen()
    x0, y0, x1, y1 = box
    pen.moveTo((x0, y0)); pen.lineTo((x1, y0)); pen.lineTo((x1, y1)); pen.lineTo((x0, y1)); pen.closePath()
    cut = pathops.op(path, rect, pathops.PathOp.INTERSECTION)
    spans = []
    for contour in cut.contours:
        xmin, ymin, xmax, ymax = contour.bounds
        lo, hi = (ymin, ymax) if side in ("left", "right") else (xmin, xmax)
        spans.append((round(lo, 1), round(hi, 1)))
    merged = []
    for lo, hi in sorted(spans):
        if merged and lo <= merged[-1][1] + 0.05:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return merged


def check_edges(font):
    os2 = font["OS/2"]
    cell = (font["hmtx"][font.getBestCmap()[0x2500]][0], os2.sTypoDescender, os2.sTypoAscender)
    ref = {}
    for (axis, style), char in REFERENCE.items():
        ref[(axis, style)] = strip(outline(font, char), "left" if axis == "h" else "up", cell)
    problems = []

    def expect(char, side, want):
        got = strip(outline(font, char), side, cell)
        if any(abs(g - w) > TOLERANCE for gs, ws in zip(got, want) for g, w in zip(gs, ws)) or len(got) != len(want):
            problems.append(f"{char} U+{ord(char):04X} {side}: {got} instead of {want}")

    for cp in boxdraw.BOX:
        name = boxdraw.unicodedata.name(chr(cp))[len("BOX DRAWINGS "):]
        if any(w in name.split() for w in ("DASH", "ARC", "DIAGONAL")):
            continue
        for side, style in boxdraw.arms(name).items():
            axis = "h" if side in ("left", "right") else "v"
            expect(chr(cp), side, ref[(axis, style)] if style else [])
    for cp in boxdraw.ARCS:
        words = boxdraw.unicodedata.name(chr(cp)).split()
        for side in (words[4].lower(), words[6].lower()):
            expect(chr(cp), side, ref[("h" if side in ("left", "right") else "v", "light")])
    w, b, t = cell
    for side, want in (("left", [(b, t)]), ("right", [(b, t)]), ("up", [(0, w)]), ("down", [(0, w)])):
        expect("█", side, want)
    return problems


def cell_image(font, char, cw, row):
    """One glyph drawn in its own terminal cell: origin at the cell's left edge, baseline at the ascender."""
    img = Image.new("L", (cw + 2 * PAD, row + 2 * PAD), 0)
    ImageDraw.Draw(img).text((PAD, PAD), char, font=font, fill=255, anchor="la")
    return np.asarray(img, float) / 255


def gaps(profile):
    """True when the line, between its two ends, drops below half its own peak."""
    on = np.flatnonzero(profile >= profile.max() / 2)
    inner = profile[on[0]:on[-1] + 1]
    return bool((inner < profile.max() / 2).any())


def check_tiling(static):
    """Lay glyphs out on an integer cell grid, as terminals do, and look for gaps along each line."""
    problems = []
    font = TTFont(static)
    upm, os2 = font["head"].unitsPerEm, font["OS/2"]
    top, bottom = os2.sTypoAscender, os2.sTypoDescender
    n = 6
    for px in range(12, 25):
        f = ImageFont.truetype(str(static), px)
        cw = round(f.getlength("─"))
        row = round((top - bottom) * px / upm)
        for char in "─━═":
            glyph = cell_image(f, char, cw, row)
            canvas = np.zeros((row + 2 * PAD, cw * n + 2 * PAD))
            for i in range(n):
                canvas[:, i * cw:i * cw + glyph.shape[1]] = np.maximum(canvas[:, i * cw:i * cw + glyph.shape[1]], glyph)
            if gaps(canvas.max(axis=0)):
                problems.append(f"{char} at {px} px: gap between cells")
        for char in "│┃║█":
            glyph = cell_image(f, char, cw, row)
            canvas = np.zeros((row * n + 2 * PAD, cw + 2 * PAD))
            for i in range(n):
                canvas[i * row:i * row + glyph.shape[0]] = np.maximum(canvas[i * row:i * row + glyph.shape[0]], glyph)
            if gaps(canvas.max(axis=1)):
                problems.append(f"{char} at {px} px: gap between rows")
    return problems


def main():
    failed = False
    for variable in sorted((FONTS / "variable").glob("*.ttf")):
        base = TTFont(variable)
        for inst in base["fvar"].instances:
            with tempfile.NamedTemporaryFile(suffix=".ttf") as tmp:
                instancer.instantiateVariableFont(TTFont(variable), inst.coordinates).save(tmp.name)
                problems = check_edges(TTFont(tmp.name))
            label = f"{variable.name} wght {inst.coordinates['wght']:g}"
            print(f"{'FAIL' if problems else 'ok':4} edges, {label}")
            for p in problems[:20]:
                print(f"     {p}")
            failed |= bool(problems)
    for static in sorted((FONTS / "ttf").glob("*.ttf")):
        problems = check_tiling(static)
        print(f"{'FAIL' if problems else 'ok':4} tiling 12-24 px, {static.name}")
        for p in problems[:20]:
            print(f"     {p}")
        failed |= bool(problems)
    print("box drawing: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
