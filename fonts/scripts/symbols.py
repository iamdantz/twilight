"""Symbols for Twilight Text and Twilight Code: shapes, primes, brackets and a few derived signs.

Two kinds of glyph, both new; no existing glyph changes.

Computed, from measures of each master, as the arrows are (fonts/scripts/arrows.py):

- Geometric shapes ■ □ ▪ ▫ ▲ △ ▴ ▵ ▶ ▷ ▸ ▹ ▼ ▽ ▾ ▿ ◀ ◁ ◂ ◃ ◆ ◇ ○ ● ◦. Small shapes have the
  area of the bullet (•), large ones the area of a circle as tall as a capital: equal areas, so
  a square, a triangle, a diamond and a circle of one size weigh the same. All sit on the math
  axis. Outlined shapes are inset evenly (scaled about their incenter, so corners stay
  mitred) by one fixed fraction of the plus sign's stroke in every master, so the stroke
  interpolates with the font: the whole stroke, or less where in some master the hole would
  be narrower than the stroke (small shapes in heavy weights), so ▫ still reads apart from ▪.
  In Twilight Code the large shapes shrink together until the widest, slanted in italic, fits
  the cell less two 40-unit side bearings.
- ∆ (increment), an outlined equilateral triangle from the baseline to the cap height (in
  Code, as high as fits the cell), with the same stroke rule, and ∅ (empty set), a ring as
  tall as the O (in Code, as large as fits) crossed by a stroke at the angle and thickness of
  the slash; ⟨ ⟩, open brackets as tall and as wide as the parentheses, with the plus sign's
  stroke.

Derived, from the designers' own outlines, moved and never redrawn:

- ‖ two vertical bars, as far apart as the lines of the equal sign;
- ′ ″ the straight quotes slanted by the italic angle;
- ⅓ ⅔ assembled from the digits and slash of ½ and ¾, each digit moved to the slot it takes;
- ⁴ the 4 of ¼, scaled by the ratio between the superior 1 and the fraction's 1 (under 3 %),
  standing on the superiors' baseline; ₁ ₂ ₃ ₄ the superiors moved down so their baseline is
  the font's declared subscript offset (OS/2 ySubscriptYOffset, where applications place
  synthesized subscripts);
- № the N followed by º (Twilight Text only: in Code it does not fit one cell);
- µ the u with its left stem carried down to the descender of p.

Italic: computed glyphs are drawn upright and slanted about the math axis, as the plus sign is;
derived glyphs take the already slanted italic outlines.
"""
import math

from arrows import CODE_SB, rotate, shift
from boxdraw import KAPPA, hole, ink

SHAPES = {  # code point: (shape, size, filled, direction)
    0x25A0: ("square", "large", True, 0), 0x25A1: ("square", "large", False, 0),
    0x25AA: ("square", "small", True, 0), 0x25AB: ("square", "small", False, 0),
    0x25B2: ("triangle", "large", True, 90), 0x25B3: ("triangle", "large", False, 90),
    0x25B4: ("triangle", "small", True, 90), 0x25B5: ("triangle", "small", False, 90),
    0x25B6: ("triangle", "large", True, 0), 0x25B7: ("triangle", "large", False, 0),
    0x25B8: ("triangle", "small", True, 0), 0x25B9: ("triangle", "small", False, 0),
    0x25BC: ("triangle", "large", True, 270), 0x25BD: ("triangle", "large", False, 270),
    0x25BE: ("triangle", "small", True, 270), 0x25BF: ("triangle", "small", False, 270),
    0x25C0: ("triangle", "large", True, 180), 0x25C1: ("triangle", "large", False, 180),
    0x25C2: ("triangle", "small", True, 180), 0x25C3: ("triangle", "small", False, 180),
    0x25C6: ("diamond", "large", True, 0), 0x25C7: ("diamond", "large", False, 0),
    0x25CB: ("circle", "large", False, 0), 0x25CF: ("circle", "large", True, 0),
    0x25E6: ("circle", "small", False, 0),
}
COMPUTED = [0x2206, 0x2205, 0x27E8, 0x27E9]
DERIVED = [0x2016, 0x2032, 0x2033, 0x2153, 0x2154, 0x2074, 0x2081, 0x2082, 0x2083, 0x2084, 0x2116, 0x00B5]
TEXT_ONLY = {0x2116}
ITALIC_ANGLE = 12  # the italic angle of both families; build.py checks it against the sources
CODEPOINTS = sorted(SHAPES) + COMPUTED + DERIVED


def codepoints(cell):
    return sorted(cp for cp in CODEPOINTS if not (cell and cp in TEXT_ONLY))


def glyph_name(cp):
    return f"uni{cp:04X}"


# ---------- geometry ----------

def circle(cx, cy, r):
    """Counter-clockwise circle from four cubic arcs."""
    k = KAPPA * r
    return [(cx + r, cy, "curve"), (cx + r, cy + k, "offcurve"), (cx + k, cy + r, "offcurve"),
            (cx, cy + r, "curve"), (cx - k, cy + r, "offcurve"), (cx - r, cy + k, "offcurve"),
            (cx - r, cy, "curve"), (cx - r, cy - k, "offcurve"), (cx - k, cy - r, "offcurve"),
            (cx, cy - r, "curve"), (cx + k, cy - r, "offcurve"), (cx + r, cy - k, "offcurve")]


def polygon(points):
    return [(x, y, "line") for x, y in points]


def scaled(points, k, cx, cy):
    return [(cx + (x - cx) * k, cy + (y - cy) * k, *rest) for x, y, *rest in points]


def regular(shape, area):
    """Outer polygon (centered on the origin) and inradius of a shape of a given area."""
    if shape == "square":
        s = math.sqrt(area)
        return polygon([(-s / 2, -s / 2), (s / 2, -s / 2), (s / 2, s / 2), (-s / 2, s / 2)]), s / 2
    if shape == "diamond":
        d = math.sqrt(2 * area)  # diagonal
        return polygon([(0, -d / 2), (d / 2, 0), (0, d / 2), (-d / 2, 0)]), d / (2 * math.sqrt(2))
    if shape == "triangle":  # pointing right, centroid at the origin
        a = math.sqrt(4 * area / math.sqrt(3))
        h = a * math.sqrt(3) / 2
        return polygon([(2 * h / 3, 0), (-h / 3, a / 2), (-h / 3, -a / 2)]), h / 3
    raise ValueError(shape)


def outlined(outer, inradius, t, center=(0, 0)):
    """The outer contour with a hole inset by t on every side (a homothety about the incenter,
    so corners stay mitred)."""
    k = (inradius - t) / inradius
    return [ink(outer), hole(scaled(outer, k, *center))]


def stroke(p, q, t):
    """A straight stroke of thickness t from p to q, square ends."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * t / 2, dx / n * t / 2
    return polygon([(p[0] + ox, p[1] + oy), (p[0] - ox, p[1] - oy), (q[0] - ox, q[1] - oy), (q[0] + ox, q[1] + oy)])


def chevron(height, width, t):
    """An open angle bracket ⟨, stroke t, mitred at the tip, cut level at top and bottom, its ink
    exactly `width` wide and `height` tall, the tip at x = 0 on y = 0."""
    top = height / 2
    lo, hi = 1.0, width  # x of the outer arm end; the inner end lies t / sin(angle) further
    for _ in range(60):
        x = (lo + hi) / 2
        angle = math.atan2(top, x)
        if x + t / math.sin(angle) > width:
            hi = x
        else:
            lo = x
    angle = math.atan2(top, lo)
    d = t / math.sin(angle)  # horizontal thickness of an arm
    return polygon([(0, 0), (lo, top), (lo + d, top), (d, 0), (lo + d, -top), (lo, -top)])


def bounds(contours):
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    return min(xs), min(ys), max(xs), max(ys)


# ---------- per master ----------

OUTLINED = [cp for cp, (_, _, filled, _) in SHAPES.items() if not filled] + [0x2206]


class Master:
    """What the symbols take from one master. `contours(name)` gives a glyph's outline with
    components resolved, as lists of (x, y, node type); `width(name)` its advance."""

    def __init__(self, metrics, contours, width, cap, xheight, subscript):
        self.m, self.contours, self.width = metrics, contours, width
        self.cap, self.xheight, self.subscript = cap, xheight, subscript
        self.cell = metrics.cell
        self.fit = self.cell - 2 * CODE_SB if self.cell else None
        self.ratio = {}  # outlined glyph: its stroke over the plus sign's (prepare())
        (x0, y0, x1, y1) = bounds(contours("bullet"))
        self.small = math.pi * ((y1 - y0) / 2) ** 2
        self.large = math.pi * (cap / 2) ** 2
        self.large_scale = 1.0
        if self.cell:  # Code: the large shapes shrink together until the widest, slanted, fits
            widest = max(self.width_of(self.shape_contours(cp)) for cp, s in SHAPES.items() if s[1] == "large")
            self.large_scale = min(1.0, self.fit / widest)

    def slanted(self, contours):
        s, cy = self.m.slant, self.m.cy
        return [[(x + s * (y - cy), y, k) for x, y, k in c] for c in contours] if s else contours

    def upright(self, contours):
        """Contours with the italic slant taken out (about the math axis), for measuring."""
        s, cy = self.m.slant, self.m.cy
        return [[(x - s * (y - cy), y, k) for x, y, k in c] for c in contours]

    def width_of(self, contours):
        x0, _, x1, _ = bounds(self.slanted(contours))
        return x1 - x0

    def stroke(self, cp):
        return self.ratio.get(cp, 1.0) * self.m.t

    def inradius(self, cp):
        """Inradius of an outlined glyph's outer contour, before any stroke."""
        if cp == 0x2206:
            return self.delta_height() / 3
        shape, size, _, _ = SHAPES[cp]
        area = self.small if size == "small" else self.large * self.large_scale ** 2
        return math.sqrt(area / math.pi) if shape == "circle" else regular(shape, area)[1]

    def delta_height(self):
        """∆ reaches the cap height; in Code, as high as fits the cell once slanted."""
        h = self.cap
        if self.cell:
            h = min(h, self.fit / (2 / math.sqrt(3) + self.m.slant))
        return h

    def shape_contours(self, cp):
        shape, size, filled, direction = SHAPES[cp]
        area = self.small if size == "small" else self.large * self.large_scale ** 2
        t = self.stroke(cp)
        if shape == "circle":
            r = math.sqrt(area / math.pi)
            outer = circle(0, 0, r)
            return [outer] if filled else [outer, hole(circle(0, 0, r - t))]
        outer, inradius = regular(shape, area)
        if shape == "triangle":
            outer = rotate(outer, direction)
        return [ink(outer)] if filled else outlined(outer, inradius, t)

    def place(self, contours, y_center=None, lsb=None, rsb=None):
        """Computed glyphs: the upright ink centered on y_center (the math axis by default),
        slanted about the math axis, then spaced with the given upright side bearings (the plus
        sign's by default) or centered in the cell."""
        x0, y0, x1, y1 = bounds(contours)
        dy = (self.m.cy if y_center is None else y_center) - (y0 + y1) / 2
        contours = [shift(c, -x0, dy) for c in contours]
        if self.cell:
            contours = self.slanted(contours)
            sx0, _, sx1, _ = bounds(contours)
            return self.cell, [shift(c, (self.cell - (sx1 - sx0)) / 2 - sx0, 0) for c in contours]
        lsb = self.m.sb if lsb is None else lsb
        rsb = self.m.sb if rsb is None else rsb
        return x1 - x0 + lsb + rsb, [shift(c, lsb, 0) for c in self.slanted(contours)]

    def keep(self, contours, lsb, rsb):
        """Derived glyphs, already slanted: Text spaces the upright ink with the given side
        bearings (italic side bearings are measured upright, so a digit moved down to the
        subscript line keeps its spacing along the slant); Code centers the ink in the cell."""
        if self.cell:
            x0, _, x1, _ = bounds(contours)
            return self.cell, [shift(c, (self.cell - (x1 - x0)) / 2 - x0, 0) for c in contours]
        x0, _, x1, _ = bounds(self.upright(contours))
        return x1 - x0 + lsb + rsb, [shift(c, lsb - x0, 0) for c in contours]


def prepare(masters):
    """Give every outlined glyph one stroke ratio for all masters, so its stroke interpolates
    with the plus sign's: the whole stroke, or less where in some master the hole would be
    narrower than the stroke (small shapes in heavy weights), so ▫ still reads apart from ▪."""
    for cp in OUTLINED:
        ratio = min(min(1.0, m.inradius(cp) / (2 * m.m.t)) for m in masters)
        for m in masters:
            m.ratio[cp] = ratio


def side_bearings(master, name):
    """Side bearings of an existing glyph, measured upright."""
    x0, _, x1, _ = bounds(master.upright(master.contours(name)))
    return x0, master.width(name) - x1


def fraction_parts(master, name):
    """Numerator, slash and denominator contours of a precomposed fraction, told apart by
    position: the slash spans the cap height; numerators stand above it, denominators below."""
    parts = {"numerator": [], "slash": [], "denominator": []}
    for c in master.contours(name):
        x0, y0, x1, y1 = bounds([c])
        if y1 - y0 > 0.9 * master.cap:
            parts["slash"].append(c)
        elif (y0 + y1) / 2 > master.cap / 2:
            parts["numerator"].append(c)
        else:
            parts["denominator"].append(c)
    return parts


def move_to(contours, target, baseline_from, baseline_to):
    """Move a digit so its baseline goes from one slot to another and its center to `target`."""
    x0, _, x1, _ = bounds(contours)
    return [shift(c, target - (x0 + x1) / 2, baseline_to - baseline_from) for c in contours]


def center_x(contours):
    x0, _, x1, _ = bounds(contours)
    return (x0 + x1) / 2


def glyph(master, cp):
    """(advance width, contours) of one symbol in one master."""
    m = master.m
    if cp in SHAPES:
        return master.place(master.shape_contours(cp))
    if cp == 0x2206:  # ∆: equilateral, base on the baseline, apex at the cap height
        h = master.delta_height()
        a = 2 * h / math.sqrt(3)
        outer = polygon([(-a / 2, 0), (a / 2, 0), (0, h)])
        return master.place(outlined(outer, h / 3, master.stroke(cp), center=(0, h / 3)), y_center=h / 2)
    if cp == 0x2205:  # ∅
        x0, y0, x1, y1 = bounds(master.contours("O"))
        cy = (y0 + y1) / 2
        slash = master.contours("slash")[0]
        sx0, sy0, sx1, sy1 = bounds([slash])
        upright = [(x - m.slant * (y - m.cy), y) for x, y, _ in slash]
        ux0, ux1 = min(p[0] for p in upright), max(p[0] for p in upright)
        thickness = min(abs(upright[i][0] - upright[j][0]) for i in range(len(upright))
                        for j in range(len(upright)) if i != j and abs(upright[i][1] - upright[j][1]) < 1)
        angle = math.atan2(sy1 - sy0, (ux1 - ux0) - thickness)
        t_slash = thickness * math.sin(angle)  # the slash's stroke, measured across it

        def empty_set(d):  # a ring of diameter d, crossed by the slash one stroke past it
            r = d / 2
            reach = r + m.t
            p = (-reach * math.cos(angle), cy - reach * math.sin(angle))
            q = (reach * math.cos(angle), cy + reach * math.sin(angle))
            return [circle(0, cy, r), hole(circle(0, cy, r - m.t)), ink(stroke(p, q, t_slash))]
        d = y1 - y0  # as tall as the O
        if master.cell:  # Code: as large as fits the cell once slanted
            lo, hi = 0.0, d
            for _ in range(50):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if master.width_of(empty_set(mid)) <= master.fit else (lo, mid)
            d = lo
        return master.place(empty_set(d), y_center=cy)
    if cp in (0x27E8, 0x27E9):  # ⟨ ⟩, as tall and wide as the parentheses
        paren = master.contours("parenleft")
        up = [(x - m.slant * (y - m.cy), y) for c in paren for x, y, _ in c]
        x0, x1 = min(p[0] for p in up), max(p[0] for p in up)
        y0, y1 = min(p[1] for p in up), max(p[1] for p in up)
        c = chevron(y1 - y0, x1 - x0, m.t)
        if cp == 0x27E9:
            c = [(-x, y, k) for x, y, k in c]
        lsb, rsb = x0, master.width("parenleft") - x1  # the parenthesis's upright side bearings
        if cp == 0x27E9:
            lsb, rsb = rsb, lsb
        return master.place([ink(c)], y_center=(y0 + y1) / 2, lsb=lsb, rsb=rsb)
    if cp == 0x2016:  # ‖
        bar = master.contours("bar")
        lsb, rsb = side_bearings(master, "bar")
        pair = [shift(c, -m.e, 0) for c in bar] + [shift(c, m.e, 0) for c in bar]
        return master.keep(pair, lsb, rsb)
    if cp in (0x2032, 0x2033):  # ′ ″
        src = "quotesingle" if cp == 0x2032 else "quotedbl"
        contours = master.contours(src)
        _, y0, _, y1 = bounds(contours)
        mid = (y0 + y1) / 2
        slant = math.tan(math.radians(ITALIC_ANGLE))
        contours = [[(x + slant * (y - mid), y, k) for x, y, k in c] for c in contours]
        lsb, rsb = side_bearings(master, src)
        return master.keep(contours, lsb, rsb)
    if cp in (0x2153, 0x2154):  # ⅓ ⅔
        half, three4 = fraction_parts(master, "onehalf"), fraction_parts(master, "threequarters")
        num_base = bounds(half["numerator"])[1]  # the 1 stands flat on the numerator baseline
        den_base = bounds(half["denominator"])[1]  # the 2 stands flat on the denominator baseline
        three = three4["numerator"]
        if cp == 0x2153:
            parts = half["numerator"] + half["slash"] + move_to(three, center_x(half["denominator"]),
                                                                  num_base, den_base)
            name = "onehalf"
        else:
            two = move_to(half["denominator"], center_x(three4["numerator"]), den_base, num_base)
            parts = two + three4["slash"] + move_to(three, center_x(three4["denominator"]), num_base, den_base)
            name = "threequarters"
        lsb, rsb = side_bearings(master, name)
        return master.keep(parts, lsb, rsb)
    if cp in (0x2074, 0x2081, 0x2082, 0x2083, 0x2084):
        one_sup = master.contours("onesuperior")
        sup_base = bounds(one_sup)[1]
        if cp in (0x2074, 0x2084):
            four = fraction_parts(master, "onequarter")["denominator"]
            one_num = fraction_parts(master, "onehalf")["numerator"]
            k = (bounds(one_sup)[3] - sup_base) / (bounds(one_num)[3] - bounds(one_num)[1])
            fx0, fy0, _, _ = bounds(four)
            digit = [shift(scaled(c, k, fx0, fy0), 0, sup_base - fy0) for c in four]
            lsb, rsb = side_bearings(master, "twosuperior")
        else:
            src = {0x2081: "onesuperior", 0x2082: "twosuperior", 0x2083: "threesuperior"}[cp]
            digit = master.contours(src)
            lsb, rsb = side_bearings(master, src)
        if cp != 0x2074:
            digit = [shift(c, 0, -master.subscript - sup_base) for c in digit]
        return master.keep(digit, lsb, rsb)
    if cp == 0x2116:  # №
        n, o = master.contours("N"), master.contours("ordmasculine")
        w = master.width("N")
        return master.width("N") + master.width("ordmasculine"), n + [shift(c, w, 0) for c in o]
    if cp == 0x00B5:  # µ: the u with its left stem carried down to the descender of p
        u = master.contours("u")
        _, py0, _, _ = bounds(master.contours("p"))
        y = master.xheight / 2
        x0, x1 = stem_at(u, y)
        top = y
        stem = polygon([(x0 + m.slant * (py0 - y), py0), (x1 + m.slant * (py0 - y), py0), (x1, top), (x0, top)])
        if master.cell:  # the slanted stem reaches further left; center the ink again
            return master.keep(u + [ink(stem)], 0, 0)
        return master.width("u"), u + [ink(stem)]
    raise ValueError(f"U+{cp:04X}")


def stem_at(contours, y):
    """The first ink interval, from the left, on the horizontal line at height y (on-curve
    polygon approximation; the u's stems are straight)."""
    xs = []
    for c in contours:
        on = [(p[0], p[1]) for p in c if p[2] != "offcurve"]
        for (xa, ya), (xb, yb) in zip(on, on[1:] + on[:1]):
            if (ya - y) * (yb - y) < 0:
                xs.append(xa + (y - ya) * (xb - xa) / (yb - ya))
    xs.sort()
    return xs[0], xs[1]
