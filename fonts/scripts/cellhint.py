"""TrueType instructions for the glyphs drawn on the cell in Twilight Crystal Mono's static fonts.

The autohinter hints box drawing, blocks and Powerline separators as if they were letters: it
moves the ends of their lines off the cell edges, at some sizes past the Windows clipping box
(usWinAscent), where GDI cuts them off. Taking the instructions out keeps the ends in place but
leaves the lines soft, straddling two rows of pixels. These instructions do what the cell
needs, in the vertical direction only (the one Windows renderers hint):

- points on the cell's top and bottom edges round to the nearest pixel row, so a line ends on
  the row a terminal's cell ends on and never past the clipping box;
- every horizontal line of box drawing (light, heavy, or one of a double pair, as boxdraw.py
  draws them: the light width is the hyphen's) has its lower edge rounded to a pixel row and
  its thickness rounded, at least one pixel, so lines are crisp and never vanish; a line is
  recognized when both its edges are point heights of the glyph and the band between them is
  ink across a sixth of the cell or more;
- any other point height (block and shade edges, arcs, Powerline shapes) rounds to the nearest
  row; points between (curves) are interpolated.

Each line is placed by its own rule, never from a neighbor, so every glyph with the same line
gets the same pixels and junctions meet.
"""
import pathops
from fontTools.ttLib.tables import ttProgram

MIN_INK = 1 / 6
SAMPLES = 96


def _ink_path(font, name):
    path = pathops.Path()
    glyphs = font.getGlyphSet()
    glyphs[name].draw(path.getPen(glyphSet=glyphs))
    return pathops.simplify(path, fix_winding=True)


def _ink_share(path, y, width):
    return sum(path.contains(((i + 0.5) * width / SAMPLES, y)) for i in range(SAMPLES)) / SAMPLES


def program(font, name, top, bottom, light):
    """The instructions for one simple glyph; top and bottom are the cell edges in units, light
    the width of a light line (the hyphen's thickness in this font)."""
    glyph = font["glyf"][name]
    coords = glyph.getCoordinates(font["glyf"])[0]
    flags = glyph.flags
    width = font["hmtx"][name][0]
    levels = {}
    for i, (x, y) in enumerate(coords):
        if flags[i] & 1:  # on-curve
            levels.setdefault(y, []).append(i)
    path = _ink_path(font, name)
    cy = (top + bottom) / 2

    def level_near(y):
        near = [h for h in levels if abs(h - y) <= 1]
        return min(near, key=lambda h: abs(h - y)) if near else None

    lines = []
    for center, w in ((cy, light), (cy, 2 * light), (cy - light, light), (cy + light, light)):
        lo, hi = level_near(center - w / 2), level_near(center + w / 2)
        if lo is not None and hi is not None and _ink_share(path, (lo + hi) / 2, width) >= MIN_INK:
            lines.append((lo, hi))

    asm = ["SVTCA[0]"]
    placed = {}  # height: the point already in place there

    def place(h, first, how):
        rest = levels[h][1:]
        asm.extend(how)
        placed[h] = first
        if rest:
            asm.extend([f"PUSH[ ] {first}", "SRP0[ ]"])
            for p in rest:
                asm.extend([f"PUSH[ ] {p}", "ALIGNRP[ ]"])

    def anchor(h):
        first = levels[h][0]
        place(h, first, [f"PUSH[ ] {first}", "MDAP[1]"])

    def relative(h, ref):
        first = levels[h][0]
        place(h, first, [f"PUSH[ ] {placed[ref]}", "SRP0[ ]", f"PUSH[ ] {first}", "MDRP[01100]"])

    for h in (top, bottom):
        if h in levels:
            anchor(h)
    for lo, hi in lines:
        if lo not in placed:
            anchor(lo)
        if hi not in placed:
            relative(hi, lo)
    for h in sorted(levels):
        if h not in placed:
            anchor(h)
    asm.append("IUP[0]")
    prog = ttProgram.Program()
    prog.fromAssembly(asm)
    return prog
