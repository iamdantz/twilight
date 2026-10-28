"""Arrows for Twilight Crystal and Twilight Crystal Mono.

Every arrow is computed from two glyphs of each master and its italic angle, so it interpolates
with the rest of the font and reads as part of it:

- the plus sign: the stroke (its bar thickness), the axis (its center, the math axis, where
  the minus, the plus and the equal sign sit), the length and the side bearings;
- the equal sign: how far apart the two lines of a double arrow are;
- the master's italic angle: italic arrows are slanted about the axis, as the plus sign is.

An arrow is a monoline shaft with an open head: two arms at 45 degrees, mitred at the tip, of
the same stroke as the shaft. The shaft ends inside the head, so no two contours share an
edge. In Twilight Crystal a horizontal arrow is 1.4 times as long as the plus sign is wide, about
the width of a capital M, and is spaced with the plus sign's side bearings; in Twilight Crystal Mono it
fills the 632-unit cell but for 40 units on each side. Vertical and diagonal arrows have the
same length, turned. An arrow with a head at each end grows until some shaft shows between the
heads; in Crystal Mono it stops at the cell, and its heads shrink instead. Crystal Mono leaves out ⇔ and ⇕,
and shortens an italic arrow whose slant would carry it out of the cell (↵).

Contours are counter-clockwise for ink, as in the design sources, and have the same points in
every master, so the masters stay compatible.
"""
import math

from boxdraw import KAPPA, ink

ROOT2 = math.sqrt(2)
MIN_SB = 20
CODE_SB = 40

# code point: (shape, direction in degrees)
ARROWS = {
    0x2190: ("single", 180), 0x2191: ("single", 90), 0x2192: ("single", 0), 0x2193: ("single", 270),
    0x2194: ("both", 0), 0x2195: ("both", 90),
    0x2196: ("single", 135), 0x2197: ("single", 45), 0x2198: ("single", 315), 0x2199: ("single", 225),
    0x21A9: ("hook", 180), 0x21AA: ("hook", 0),
    0x21B5: ("corner", 180),
    0x21D0: ("double", 180), 0x21D1: ("double", 90), 0x21D2: ("double", 0), 0x21D3: ("double", 270),
    0x21D4: ("double both", 0), 0x21D5: ("double both", 90),
}
CODEPOINTS = sorted(ARROWS)


def codepoints(cell):
    """The arrows a font gets. Twilight Crystal Mono leaves out ⇔ and ⇕: at its heaviest weight a
    double line with a head at each end does not fit the cell with heads that still reach past
    both lines."""
    return [cp for cp in CODEPOINTS if not (cell and ARROWS[cp][0] == "double both")]


def glyph_name(cp):
    return f"uni{cp:04X}"


class Metrics:
    """What an arrow takes from one master.

    plus, equal: the on-curve points of the plus and equal signs; italic: the italic angle in
    degrees; cell: the fixed advance of a monospaced font, or None.
    """

    def __init__(self, plus, equal, italic, cell=None):
        self.slant = math.tan(math.radians(italic))
        ys = sorted({y for _, y in plus})
        bar = [y for y in ys if y not in (ys[0], ys[-1])]  # the horizontal bar: inner y values
        self.t = bar[-1] - bar[0]
        self.cy = (bar[0] + bar[-1]) / 2
        upright = [(x - self.slant * (y - self.cy), y) for x, y in plus]
        bar_x = [x for x, y in upright if y in bar]
        self.sb = min(x for x, _ in upright)
        # Crystal Mono: the cell less two side bearings of CODE_SB; Crystal: the plus sign's width, x1.4
        self.length = cell - 2 * CODE_SB if cell else 1.4 * (max(bar_x) - min(bar_x))
        eys = sorted({y for _, y in equal})
        self.e = ((eys[-1] + eys[-2]) - (eys[0] + eys[1])) / 4  # half the distance between bar centers
        self.cell = cell
        self.h = 0.22 * self.length + self.t / 2  # reach of a head arm across the axis

    def two_heads(self, h):
        """Length of an arrow with a head at each end, and the reach of its heads.

        The heads keep the reach of one-headed arrows and the arrow grows until a stretch of
        shaft shows between them (half a stroke and a tenth of the length). In Twilight Crystal Mono
        it may grow to the cell less two 20-unit side bearings; past that the heads shrink."""
        a = self.t / ROOT2
        gap = self.t / 2 + 0.1 * self.length
        length = max(self.length, 2 * (h + a) + gap)
        if self.cell and length > self.cell - 2 * MIN_SB:
            length = self.cell - 2 * MIN_SB
            h = (length - gap) / 2 - a
        return length, h


# ---------- shapes, pointing right, tip at x = 0, axis at y = 0 ----------

def head(t, h):
    """Open head: two arms at 45 degrees, stroke t, mitred at the tip (0, 0), reaching h across."""
    a = t / ROOT2
    return [(0, 0), (-h, h), (-h - a, h - a), (-t * ROOT2, 0), (-h - a, -h + a), (-h, -h)]


def bar(x0, x1, y, t):
    return [(x0, y - t / 2), (x1, y - t / 2), (x1, y + t / 2), (x0, y + t / 2)]


def shapes(m, kind):
    """Contours of one arrow pointing right, with its ink from -L/2 to L/2 along the axis."""
    t, L = m.t, m.length
    if kind in ("single", "both"):
        h = m.h
        if kind == "both":
            L, h = m.two_heads(h)
        tip = L / 2
        out = [shift(head(t, h), tip, 0)]
        start = -L / 2
        if kind == "both":
            out.append(mirror(out[0]))
            start = -L / 2 + t
        out.append(bar(start, tip - t, 0, t))
        return out
    if kind in ("double", "double both"):
        h = m.h + m.e
        if kind == "double both":
            L, h = m.two_heads(h)
            if h < m.e + t:
                raise ValueError("no room for a double arrow with two heads")
        tip = L / 2
        end = tip - m.e - t / ROOT2  # inside the arm, for a line at e from the axis
        out = [shift(head(t, h), tip, 0)]
        start = -L / 2
        if kind == "double both":
            out.append(mirror(out[0]))
            start = -end
        out += [bar(start, end, m.e, t), bar(start, end, -m.e, t)]
        return out
    if kind in ("hook", "corner"):
        return hook(m, kind)
    raise ValueError(kind)


def hook(m, kind):
    """↩ and ↵ drawn pointing left: the head at the lower left, the hook or corner at the right.

    The hook is a half ring of radius r on the stroke's center line; its upper end runs back
    left a little under half the width. The corner rises from the right end of the shaft to the
    same height. The glyph is centered on the axis afterwards.
    """
    t, L = m.t, m.length
    r = 0.75 * m.h
    R, ri = r + t / 2, r - t / 2
    tip = -L / 2
    out = [mirror(shift(head(t, m.h), -tip, 0))]  # pointing left, tip at -L/2, on y = -r
    out[0] = [(x, y - r) for x, y in out[0]]
    start = tip + t
    if kind == "hook":
        xr = L / 2 - R
        stub = xr - 0.45 * (xr - tip)
        k = KAPPA
        pts = [(start, -R, "line"), (xr, -R, "line"),
               (xr + k * R, -R, "offcurve"), (xr + R, -k * R, "offcurve"), (xr + R, 0, "curve"),
               (xr + R, k * R, "offcurve"), (xr + k * R, R, "offcurve"), (xr, R, "curve"),
               (stub, R, "line"), (stub, ri, "line"), (xr, ri, "line"),
               (xr + k * ri, ri, "offcurve"), (xr + ri, k * ri, "offcurve"), (xr + ri, 0, "curve"),
               (xr + ri, -k * ri, "offcurve"), (xr + k * ri, -ri, "offcurve"), (xr, -ri, "curve"),
               (start, -ri, "line")]
        out.append(pts)
    else:
        xr = L / 2 - t / 2
        out.append([(start, -R), (xr + t / 2, -R), (xr + t / 2, R), (xr - t / 2, R), (xr - t / 2, -ri),
                    (start, -ri)])
    return out


# ---------- transforms ----------

def norm(c):
    """(x, y) or (x, y, kind) points to (x, y, kind)."""
    return [p if len(p) == 3 else (p[0], p[1], "line") for p in c]


def shift(c, dx, dy):
    return [(p[0] + dx, p[1] + dy, *p[2:]) for p in c]


def mirror(c):
    return [(-p[0], p[1], *p[2:]) for p in c]


def rotate(c, degrees):
    a = math.radians(degrees)
    ca, sa = round(math.cos(a), 12), round(math.sin(a), 12)
    return [(p[0] * ca - p[1] * sa, p[0] * sa + p[1] * ca, *p[2:]) for p in c]


def bounds(contours):
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    return min(xs), min(ys), max(xs), max(ys)


def glyph(m, cp):
    """(advance width, contours) of one arrow in one master."""
    kind, direction = ARROWS[cp]
    length = m.length
    for _ in range(3):
        contours = place(m, kind, direction, length)
        x0, _, x1, _ = bounds(contours)
        if not m.cell or x1 - x0 <= m.cell - 2 * MIN_SB:
            break
        # Crystal Mono italic: a slanted corner can outgrow the cell; shorten the arrow to fit
        length -= (x1 - x0) - (m.cell - 2 * MIN_SB)
    else:
        raise ValueError(f"U+{cp:04X} does not fit the cell")
    if m.cell:
        advance, dx = m.cell, (m.cell - (x1 + x0)) / 2
    else:
        # Crystal: spaced on the upright ink, then slanted about the axis, as the plus sign is
        x0u, _, x1u, _ = bounds(place(m, kind, direction, length, slant=False))
        advance, dx = x1u - x0u + 2 * m.sb, m.sb - x0u
    return advance, [ink(c) for c in (shift(c, dx, 0) for c in contours)]


def place(m, kind, direction, length, slant=True):
    """The arrow turned to its direction, centered on the axis at x = 0, and slanted."""
    saved, m.length = m.length, length
    try:
        contours = [norm(c) for c in shapes(m, kind)]
    finally:
        m.length = saved
    if kind in ("hook", "corner"):
        if direction == 0:
            contours = [mirror(c) for c in contours]
    else:
        contours = [rotate(c, direction) for c in contours]
    x0, y0, x1, y1 = bounds(contours)
    contours = [shift(c, -(x0 + x1) / 2, m.cy - (y0 + y1) / 2) for c in contours]
    if slant and m.slant:
        contours = [[(x + m.slant * (y - m.cy), y, k) for x, y, k in c] for c in contours]
    return contours
