"""Symbols in Twilight Text and Twilight Code: each one follows its rule in symbols.py,
braille.py and boxdraw.py.

At every named instance of every variable font, on the outlines, with the italic slant taken
out about the math axis before measuring:

1. Shapes (■ □ ▪ ▫ ▲ △ … ○ ● ◦). Centered on the plus sign's bar (the math axis). Small filled
   shapes have the bullet's area; large filled shapes all have one area, in Text that of a
   circle as tall as the cap height. Every point of an outlined shape's inner edge lies one
   stroke from its outer edge, and that stroke is one fixed fraction of the plus sign's bar
   at every instance: the whole bar, or less only where at the heaviest instance the hole has
   come down to the width of the stroke. Opposite triangles match. Within 3 % for areas and
   2.5 units for distances (the rounding of points and deltas to whole units).
2. ∆ stands on the baseline and reaches the cap height (in Code, as high as fits the cell
   once slanted), with the same stroke rule; ∅ is centered on the O; ⟨ ⟩ are as tall as the
   parentheses; ‖ is two lines as thick as the bar, as far apart as the equal sign's.
3. ⅓ ⅔ ⁴ ₁ ₂ ₃ ₄: every digit has the size of the digit it was taken from; numerators and
   denominators stand on the baselines of ½, superiors on that of ¹, subscripts on the font's
   declared subscript offset (OS/2 ySubscriptYOffset). µ reaches the descender of p.
4. Braille (Code): each pattern has as many dots as bits set, each the size of the period, each
   centered on its point of the 2 × 4 grid spread over the cell.
5. Rounded Powerline separators (Code): the flat side covers the whole left (or right) edge of
   the cell and the curve reaches the opposite edge.
6. Code: every new glyph is 632 units wide and its ink stays inside the cell.

    python fonts/scripts/symbolcheck.py
"""
import math
import sys
import tempfile
from pathlib import Path

import pathops
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import boxdraw  # noqa: E402
import braille  # noqa: E402
import symbols  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "fonts" / "build"
AREA = 0.03
UNITS = 2.5  # rounding of points to whole units, in the masters and in the deltas


class Flatten(BasePen):
    """Contours as polylines, curves sampled."""

    def __init__(self, glyphset):
        super().__init__(glyphset)
        self.contours, self.current = [], []

    def _moveTo(self, p):
        self.current = [p]

    def _lineTo(self, p):
        self.current.append(p)

    def _curveToOne(self, p1, p2, p3):
        p0 = self.current[-1]
        for i in range(1, 17):
            t = i / 16
            self.current.append(tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
                                      for a, b, c, d in zip(p0, p1, p2, p3)))

    def _qCurveToOne(self, p1, p2):
        p0 = self.current[-1]
        for i in range(1, 17):
            t = i / 16
            self.current.append(tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t ** 2 * c for a, b, c in zip(p0, p1, p2)))

    def _closePath(self):
        self.contours.append(self.current)
        self.current = []

    _endPath = _closePath


class Font:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.cmap, self.glyphs = self.tt.getBestCmap(), self.tt.getGlyphSet()
        self.hmtx = self.tt["hmtx"]
        self.slant = math.tan(math.radians(-self.tt["post"].italicAngle))
        plus = self.contours("+")
        ys = sorted({round(y, 3) for c in plus for _, y in c})
        bar = [y for y in ys if y not in (ys[0], ys[-1])]
        self.t, self.cy = bar[-1] - bar[0], (bar[0] + bar[-1]) / 2
        self.fixed = self.advance("i") == self.advance("m")
        self.cap = self.tt["OS/2"].sCapHeight

    def name(self, ch):
        return self.cmap[ord(ch) if isinstance(ch, str) else ch]

    def advance(self, ch):
        return self.hmtx[self.name(ch)][0]

    def contours(self, ch):
        """Flattened contours with the italic slant taken out about the math axis."""
        pen = Flatten(self.glyphs)
        self.glyphs[self.name(ch)].draw(pen)
        s, cy = self.slant, getattr(self, "cy", 0)
        return [[(x - s * (y - cy), y) for x, y in c] for c in pen.contours]

    def path(self, ch):
        p = pathops.Path()
        pen = p.getPen()
        for c in self.contours(ch):
            pen.moveTo(c[0])
            for q in c[1:]:
                pen.lineTo(q)
            pen.closePath()
        return pathops.simplify(p, fix_winding=True)


def bbox(contours):
    xs = [x for c in contours for x, _ in c]
    ys = [y for c in contours for _, y in c]
    return min(xs), min(ys), max(xs), max(ys)


def area(contour):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(contour, contour[1:] + contour[:1]))) / 2


def perimeter(contour):
    return sum(math.hypot(x2 - x1, y2 - y1) for (x1, y1), (x2, y2) in zip(contour, contour[1:] + contour[:1]))


def distance(p, polyline):
    best = float("inf")
    for (ax, ay), (bx, by) in zip(polyline, polyline[1:] + polyline[:1]):
        dx, dy = bx - ax, by - ay
        k = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy or 1)))
        best = min(best, math.hypot(p[0] - ax - k * dx, p[1] - ay - k * dy))
    return best


def stroke_ok(contours, t):
    """Inner edge one stroke from the outer edge everywhere (inner = the smaller contour)."""
    outer, inner = sorted(contours, key=area, reverse=True)[:2]
    ds = [distance(p, outer) for p in inner]
    return min(ds), max(ds)


def check(path):
    f = Font(path)
    problems = []
    present = [cp for cp in symbols.CODEPOINTS + braille.CODEPOINTS + list(boxdraw.ROUNDED) if cp in f.cmap]

    def say(cp, text):
        problems.append(f"{chr(cp)} U+{cp:04X}: {text}")

    strokes = {}  # outlined glyph: (lowest stroke, highest stroke, hole inradius); main() judges

    def measure_stroke(cp, cs):
        lo, hi = stroke_ok(cs, f.t)
        if hi - lo > UNITS:
            say(cp, f"stroke varies from {lo:.1f} to {hi:.1f}")
        inner = sorted(cs, key=area)[0]
        return (lo + hi) / 2, f.t, 2 * area(inner) / perimeter(inner)

    bullet_area = f.path("•").area
    large = []
    for cp, (shape, size, filled, direction) in symbols.SHAPES.items():
        if cp not in f.cmap:
            continue
        cs = f.contours(cp)
        x0, y0, x1, y1 = bbox(cs)
        if abs((y0 + y1) / 2 - f.cy) > UNITS:
            say(cp, f"centered at {(y0 + y1) / 2:.1f}, axis {f.cy:.1f}")
        if filled:
            a = f.path(cp).area
            if size == "small" and abs(a / bullet_area - 1) > AREA:
                say(cp, f"area {a:.0f}, bullet {bullet_area:.0f}")
            if size == "large":
                large.append((cp, a))
        else:
            strokes[cp] = measure_stroke(cp, cs)
    if large:
        target = math.pi * (f.cap / 2) ** 2 if not f.fixed else large[0][1]
        for cp, a in large:
            if abs(a / target - 1) > AREA:
                say(cp, f"area {a:.0f}, large shapes {target:.0f}")
    for a, b in [(0x25B2, 0x25BC), (0x25B6, 0x25C0), (0x25B4, 0x25BE), (0x25B8, 0x25C2)]:
        (ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1) = bbox(f.contours(a)), bbox(f.contours(b))
        if abs((ax1 - ax0) - (bx1 - bx0)) > UNITS or abs((ay1 - ay0) - (by1 - by0)) > UNITS:
            say(a, f"not the size of {chr(b)}")

    # ∆ ∅ ⟨ ⟩ ‖
    x0, y0, x1, y1 = bbox(f.contours(0x2206))
    apex = min(f.cap, (632 - 2 * symbols.CODE_SB) / (2 / math.sqrt(3) + f.slant)) if f.fixed else f.cap
    if abs(y0) > UNITS or abs(y1 - apex) > UNITS:
        say(0x2206, f"from {y0:.0f} to {y1:.0f}, expected 0 to {apex:.0f}")
    strokes[0x2206] = measure_stroke(0x2206, f.contours(0x2206))
    _, oy0, _, oy1 = bbox(f.contours("O"))
    ring = sorted(f.contours(0x2205), key=area, reverse=True)[0]
    _, ry0, _, ry1 = bbox([ring])
    if abs((ry0 + ry1) / 2 - (oy0 + oy1) / 2) > UNITS:
        say(0x2205, f"ring centered at {(ry0 + ry1) / 2:.0f}, O at {(oy0 + oy1) / 2:.0f}")
    _, py0, _, py1 = bbox(f.contours("("))
    for cp in (0x27E8, 0x27E9):
        _, y0, _, y1 = bbox(f.contours(cp))
        if abs((y1 - y0) - (py1 - py0)) > UNITS:
            say(cp, f"{y1 - y0:.0f} tall, parentheses {py1 - py0:.0f}")
    bar = f.path("|")
    bx0, by0, bx1, by1 = bar.bounds
    stem = [b - a for a, b in spans(bar, (by0 + by1) / 2)][0]
    eq = spans_v(f.path("="), (lambda b: (b[0] + b[2]) / 2)(f.path("=").bounds))
    e2 = (eq[1][0] + eq[1][1] - eq[0][0] - eq[0][1]) / 2
    got = spans(f.path(0x2016), (by0 + by1) / 2)
    if len(got) != 2 or any(abs((b - a) - stem) > UNITS for a, b in got) \
            or abs((got[1][0] + got[1][1] - got[0][0] - got[0][1]) / 2 - e2) > UNITS:
        say(0x2016, f"lines {got}, expected two {stem:.0f} wide, {e2:.0f} apart")

    # digits
    def size(cs):
        x0, y0, x1, y1 = bbox(cs)
        return x1 - x0, y1 - y0

    def parts(ch):
        out = {"numerator": [], "slash": [], "denominator": []}
        for c in f.contours(ch):
            x0, y0, x1, y1 = bbox([c])
            key = "slash" if y1 - y0 > 0.9 * f.cap else ("numerator" if (y0 + y1) / 2 > f.cap / 2 else "denominator")
            out[key].append(c)
        return out
    half, three4, quarter = parts("½"), parts("¾"), parts("¼")
    num_base, den_base = bbox(half["numerator"])[1], bbox(half["denominator"])[1]
    third, twothirds = parts(0x2153), parts(0x2154)
    expect = [(0x2153, "numerator", half["numerator"], num_base), (0x2153, "denominator", three4["numerator"], den_base),
              (0x2154, "numerator", half["denominator"], num_base), (0x2154, "denominator", three4["numerator"], den_base)]
    for cp, slot, source, base in expect:
        got = (third if cp == 0x2153 else twothirds)[slot]
        if any(abs(a - b) > UNITS for a, b in zip(size(got), size(source))):
            say(cp, f"{slot} {size(got)}, source digit {size(source)}")
        # digits with an overshoot (2, 3) stand as far below the baseline as in their source
        drop = bbox(source)[1] - (num_base if source is half["numerator"] or source is three4["numerator"] else den_base)
        if abs(bbox(got)[1] - (base + drop)) > UNITS:
            say(cp, f"{slot} bottom {bbox(got)[1]:.0f}, expected {base + drop:.0f}")
    sup = f.contours("¹")
    sup_base = bbox(sup)[1]
    ratio = size(sup)[1] / size(half["numerator"])[1]
    four = quarter["denominator"]
    four_size = (size(four)[0] * ratio, size(four)[1] * ratio)
    sub_base = -f.tt["OS/2"].ySubscriptYOffset
    for cp, src, base in [(0x2074, None, sup_base), (0x2081, "¹", sub_base), (0x2082, "²", sub_base),
                          (0x2083, "³", sub_base), (0x2084, None, sub_base)]:
        got = f.contours(cp)
        want = four_size if src is None else size(f.contours(src))
        drop = 0 if src is None else bbox(f.contours(src))[1] - sup_base
        if any(abs(a - b) > UNITS for a, b in zip(size(got), want)):
            say(cp, f"size {size(got)}, expected {tuple(round(v) for v in want)}")
        if abs(bbox(got)[1] - (base + drop)) > UNITS:
            say(cp, f"bottom {bbox(got)[1]:.0f}, expected {base + drop:.0f}")
    _, ub0, _, _ = bbox(f.contours(0x00B5))
    if abs(ub0 - bbox(f.contours("p"))[1]) > UNITS:
        say(0x00B5, f"descends to {ub0:.0f}, p to {bbox(f.contours('p'))[1]:.0f}")

    # braille
    if 0x2800 in f.cmap:
        period = size(f.contours("."))
        os2 = f.tt["OS/2"]
        grid = braille.centers(632, os2.sTypoDescender, os2.sTypoAscender)
        for cp in braille.CODEPOINTS:
            raw = Flatten(f.glyphs)
            f.glyphs[f.name(cp)].draw(raw)  # the grid is upright: measure without deskewing
            dots = raw.contours
            bits = [b for b in range(8) if (cp - 0x2800) >> b & 1]
            if len(dots) != len(bits) * len(f.contours(".")):
                say(cp, f"{len(dots)} contours for {len(bits)} dots")
                continue
            centers = sorted(((x0 + x1) / 2, (y0 + y1) / 2) for x0, y0, x1, y1 in (bbox([d]) for d in dots))
            want = sorted(grid[b] for b in bits)
            if any(abs(a - b) > 1 for p, q in zip(centers, want) for a, b in zip(p, q)):
                say(cp, f"dots at {centers}, grid {want}")
            if any(abs(a - b) > UNITS for d in dots for a, b in zip(size([d]), period)) and f.slant == 0:
                say(cp, "a dot is not the size of the period")

    # rounded separators
    for cp in boxdraw.ROUNDED:
        if cp not in f.cmap:
            continue
        raw = Flatten(f.glyphs)
        f.glyphs[f.name(cp)].draw(raw)
        x0, y0, x1, y1 = bbox(raw.contours)
        os2 = f.tt["OS/2"]
        if abs(x0) > 1 or abs(x1 - 632) > 1 or abs(y0 - os2.sTypoDescender) > 1 or abs(y1 - os2.sTypoAscender) > 1:
            say(cp, f"ink {x0:.0f},{y0:.0f} to {x1:.0f},{y1:.0f}, expected the whole cell")

    if f.fixed:
        for cp in present:
            raw = Flatten(f.glyphs)
            f.glyphs[f.name(cp)].draw(raw)
            if f.hmtx[f.name(cp)][0] != 632:
                say(cp, f"advance {f.hmtx[f.name(cp)][0]}")
            if raw.contours:
                x0, _, x1, _ = bbox(raw.contours)
                if x0 < -0.5 or x1 > 632.5:
                    say(cp, f"ink from {x0:.0f} to {x1:.0f}, outside the cell")
    return len(present), problems, strokes


def judge_strokes(by_instance):
    """Outlined glyphs keep one stroke ratio (stroke over the plus sign's bar) at every
    instance: 1, or less only where at the heaviest instance the hole's inradius has come down
    to the stroke."""
    problems = []
    heaviest = by_instance[max(by_instance)]
    for cp, (s, t, hole_r) in heaviest.items():
        ratio = s / t
        if ratio < 1 - UNITS / t and abs(hole_r - s) > UNITS:
            problems.append(f"{chr(cp)} U+{cp:04X}: stroke {ratio:.2f} of the bar at the heaviest instance, "
                            f"but its hole ({hole_r:.0f}) is wider than the stroke ({s:.0f})")
        for wght, strokes in sorted(by_instance.items()):
            s_i, t_i, _ = strokes[cp]
            if abs(s_i - ratio * t_i) > UNITS:
                problems.append(f"{chr(cp)} U+{cp:04X} at wght {wght:g}: stroke {s_i:.1f}, "
                                f"expected {ratio:.2f} × {t_i:.1f} = {ratio * t_i:.1f}")
    return problems


def spans(path, y):
    """x intervals of ink on the horizontal line at y."""
    return _cut(path, (path.bounds[0] - 1, y - 0.5, path.bounds[2] + 1, y + 0.5), 0)


def spans_v(path, x):
    """y intervals of ink on the vertical line at x."""
    return _cut(path, (x - 0.5, path.bounds[1] - 1, x + 0.5, path.bounds[3] + 1), 1)


def _cut(path, box, axis):
    rect = pathops.Path()
    pen = rect.getPen()
    x0, y0, x1, y1 = box
    pen.moveTo((x0, y0)); pen.lineTo((x1, y0)); pen.lineTo((x1, y1)); pen.lineTo((x0, y1)); pen.closePath()
    cut = pathops.op(path, rect, pathops.PathOp.INTERSECTION, fix_winding=True)
    return sorted((c.bounds[axis], c.bounds[axis + 2]) for c in cut.contours)


def main():
    failed = False
    for variable in sorted(BUILD.glob("*/fonts/variable/*.ttf")):
        by_instance = {}
        for inst in TTFont(variable)["fvar"].instances:
            with tempfile.NamedTemporaryFile(suffix=".ttf") as tmp:
                instancer.instantiateVariableFont(TTFont(variable), inst.coordinates).save(tmp.name)
                count, problems, by_instance[inst.coordinates["wght"]] = check(tmp.name)
            print(f"{'FAIL' if problems else 'ok':4} {variable.name} wght {inst.coordinates['wght']:g}: {count} symbols")
            for p in problems[:20]:
                print(f"     {p}")
            failed |= bool(problems)
        problems = judge_strokes(by_instance)
        print(f"{'FAIL' if problems else 'ok':4} {variable.name}: strokes of outlined shapes across weights")
        for p in problems[:20]:
            print(f"     {p}")
        failed |= bool(problems)
    print("symbols: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
