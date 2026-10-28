"""Optional code ligatures for Twilight Code (stylistic set 1, off by default).

A ligature never changes the text or the grid: a sequence of n characters still takes n cells.
The first n - 1 characters become an empty spacer one cell wide (LIG) and the last becomes the
ligature glyph, one cell wide, whose ink reaches back over the spacers. Editors and terminals
keep counting cells and placing the cursor as before; with the set off nothing changes.

A sequence joins only when it stands alone: next to another operator character (as in -->,
<=>, <<=, ||=, <!--) it keeps its plain characters, so a longer operator is never read as a
shorter one plus a stray character; a double hyphen before a letter is a command-line option
(--watch) and stays plain too. Longer sequences are matched first (=== before ==).

Two designs of the same sequences, chosen with STYLE:

- "join": the characters keep their own outlines and their horizontal strokes are extended
  across the gap until they meet the ink of the neighbor: the hyphen runs into the greater-than
  sign (->), the bars of the equal sign run into its chevron (=>, <=, >=) or into the next equal
  sign (==, ===), the bars of plus and minus run together (++, --). A sequence whose strokes do
  not all meet ink (!=, where the lower bar passes under the exclamation mark) or that has no
  horizontal stroke at all (&&, ||, .., ...) is left as it is: nothing is drawn that the
  characters do not already have.
- "substitute": the sequence is drawn as the symbol it stands for, built from the font's own
  glyphs: a long arrow (-> =>, as the font's arrows), a long equal sign and its triple (== ===),
  the font's not-equal slash across them (!= !==), the font's ≤ ≥ and … unchanged, logical and
  and or (&& ||) as the less-than chevron turned up or down, a double plus (++, two plus signs sharing their bar), a long minus
  (--) and a two-dot leader (..). Symbols made of horizontal bars span the cells; the others
  keep their own size, centered on the cells.

Everything is computed per master in upright space (the italic slant taken off about the math
axis, where the font slants) and slanted back, so the italic ligatures match the italic glyphs.
"""
import math

import pathops

import arrows
from boxdraw import ink

STYLE = "join"
CELL = 632
SPACER = "LIG"
NAMES = {"-": "hyphen", "=": "equal", ">": "greater", "<": "less", "!": "exclam", "&": "ampersand",
         "|": "bar", "+": "plus", ".": "period"}
# longest first: a lookup for === must run before the one for ==
SEQUENCES = ["!==", "===", "...", "->", "=>", "==", "!=", "<=", ">=", "&&", "||", "++", "--", ".."]
# characters that, next to a sequence, make it part of a longer operator
OPERATORS = ["hyphen", "equal", "less", "greater", "exclam", "ampersand", "bar", "plus", "period",
             "colon", "asterisk", "slash", "question", "asciitilde", "asciicircum", "percent",
             "numbersign"]
# a double hyphen before a letter opens a command-line option (--watch), not a decrement
OPTION = "--"
LETTERS = [chr(c) for c in range(ord("A"), ord("Z") + 1)] + [chr(c) for c in range(ord("a"), ord("z") + 1)]
TOL = 2


def glyph_name(seq):
    return "_".join(NAMES[c] for c in seq) + ".liga"


# ---------- geometry ----------

def to_path(contours):
    """A pathops path from contours of (x, y, Glyphs node type)."""
    path = pathops.Path()
    pen = path.getPen()
    for c in contours:
        k = next(i for i, p in enumerate(c) if p[2] != "offcurve")
        nodes = c[k + 1:] + c[:k + 1]
        pen.moveTo(nodes[-1][:2])
        offs = []
        for x, y, kind in nodes:
            if kind == "offcurve":
                offs.append((x, y))
            elif kind == "curve":
                pen.curveTo(*offs, (x, y))
                offs = []
            elif kind == "qcurve":
                pen.qCurveTo(*offs, (x, y))
                offs = []
            else:
                pen.lineTo((x, y))
        pen.closePath()
    return path


def intervals(path, y, x0, x1):
    """Runs of ink along the line at height y, from x0 to x1, to the unit."""
    out, start = [], None
    for x in range(math.floor(x0), math.ceil(x1) + 1):
        inside = path.contains((x, y))
        if inside and start is None:
            start = x
        elif not inside and start is not None:
            out.append((start, x - 1))
            start = None
    if start is not None:
        out.append((start, math.ceil(x1)))
    return out


def cluster(values):
    out = []
    for v in sorted(values):
        if out and v - out[-1][-1] <= TOL:
            out[-1].append(v)
        else:
            out.append([v])
    return [sum(c) / len(c) for c in out]


def snap(v, levels):
    return min(levels, key=lambda u: abs(u - v))


def rect(x0, y0, x1, y1):
    return [(x0, y0, "line"), (x1, y0, "line"), (x1, y1, "line"), (x0, y1, "line")]


def shift(contours, dx, dy=0):
    return [[(x + dx, y + dy, k) for x, y, k in c] for c in contours]


def bounds(contours):
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    return min(xs), min(ys), max(xs), max(ys)


class Master:
    """One master's glyphs, in upright space.

    outline(name) gives a glyph's contours with components resolved; m is the arrows' metrics
    (stroke, math axis, slant) measured from the plus and equal signs."""

    def __init__(self, outline, m):
        self.outline, self.m = outline, m

    def upright(self, contours):
        s, cy = self.m.slant, self.m.cy
        return [[(x - s * (y - cy), y, k) for x, y, k in c] for c in contours]

    def slanted(self, contours):
        s, cy = self.m.slant, self.m.cy
        return [[(x + s * (y - cy), y, k) for x, y, k in c] for c in contours]

    def glyph(self, name):
        return self.upright(self.outline(name))

    def rects(self, name):
        """A glyph drawn only with horizontal and vertical lines, as overlapping rectangles
        (x0, y0, x1, y1): its horizontal bars and vertical stems. None for any other glyph."""
        contours = self.glyph(name)
        for c in contours:
            for (x0, y0, k), (x1, y1, _) in zip(c, c[1:] + c[:1]):
                if k != "line" or (abs(x1 - x0) > TOL and abs(y1 - y0) > TOL):
                    return None
        xs = cluster(p[0] for c in contours for p in c)
        ys = cluster(p[1] for c in contours for p in c)
        path = to_path(contours)
        out = []
        for ya, yb in zip(ys, ys[1:]):
            for a, b in intervals(path, (ya + yb) / 2, xs[0] - 1, xs[-1] + 1):
                x0, x1 = snap(a, xs), snap(b, xs)
                if x1 - x0 > yb - ya:
                    out.append((x0, ya, x1, yb))
        for xa, xb in zip(xs, xs[1:]):
            col = [(snap(a, ys), snap(b, ys)) for a, b in vertical(path, (xa + xb) / 2, ys[0] - 1, ys[-1] + 1)]
            out += [(xa, y0, xb, y1) for y0, y1 in col if y1 - y0 > xb - xa]
        return out


def vertical(path, x, y0, y1):
    out, start = [], None
    for y in range(math.floor(y0), math.ceil(y1) + 1):
        inside = path.contains((x, y))
        if inside and start is None:
            start = y
        elif not inside and start is not None:
            out.append((start, y - 1))
            start = None
    return out


# ---------- join ----------

def join(master, seq):
    """The characters' own outlines with their horizontal strokes carried across the gaps, or
    None when not every stroke facing a gap meets ink."""
    n = len(seq)
    cells = []  # per character: (offset, rects or None, upright outline)
    for i, ch in enumerate(seq):
        dx = (i - (n - 1)) * CELL
        rects = master.rects(NAMES[ch])
        cells.append([dx, [list(r) for r in rects] if rects else None, master.glyph(NAMES[ch]), NAMES[ch]])
    for c in cells:
        if c[1]:
            c[1] = [[x0 + c[0], y0, x1 + c[0], y1] for x0, y0, x1, y1 in c[1]]
    extended = False
    for (da, ra, ga, _), (db, rb, gb, _) in zip(cells, cells[1:]):
        a_ink, b_ink = to_path(shift(ga, da)), to_path(shift(gb, db))
        a_right = max(r[2] for r in ra) if ra else None
        b_left = min(r[0] for r in rb) if rb else None
        a_bars = [r for r in ra or [] if r[2] == a_right and r[2] - r[0] > r[3] - r[1]]
        b_bars = [r for r in rb or [] if r[0] == b_left and r[2] - r[0] > r[3] - r[1]]
        for bar in a_bars:
            twin = next((r for r in b_bars if abs(r[1] - bar[1]) <= TOL and abs(r[3] - bar[3]) <= TOL), None)
            if twin:  # the same bar continues in the next character: one bar
                twin[0] = bar[0]
                ra.remove(bar)
                b_bars.remove(twin)
            else:
                runs = intervals(b_ink, (bar[1] + bar[3]) / 2, bar[2], db + CELL)
                if not runs:
                    return None
                bar[2] = sum(runs[0]) / 2
            extended = True
        for bar in b_bars:
            runs = intervals(a_ink, (bar[1] + bar[3]) / 2, da, bar[0])
            if not runs:
                return None
            bar[0] = sum(runs[-1]) / 2
            extended = True
    if not extended:
        return None
    out = []
    for dx, rects, _, name in cells:
        if rects is None:  # kept as drawn, in the master's own (slanted) coordinates
            out += shift(master.outline(name), dx)
        else:
            out += master.slanted([rect(*r) for r in rects])
    return [ink(c) for c in out]


# ---------- substitute ----------

def substitute(master, seq):
    m, n = master.m, len(seq)
    left, center = -(n - 1) * CELL, CELL / 2 - (n - 1) * CELL / 2

    def stretched(name):
        """A glyph of horizontal bars (and stems) with its bars carried over every cell."""
        rects = master.rects(name)
        x0, x1 = min(r[0] for r in rects), max(r[2] for r in rects)
        bars = [r for r in rects if r[0] == x0 and r[2] == x1]
        return [(left + x0, r[1], x1, r[3]) for r in bars]

    def centered(contours, cx=center, cy=None):
        x0, y0, x1, y1 = bounds(contours)
        return shift(contours, cx - (x0 + x1) / 2, 0 if cy is None else cy - (y0 + y1) / 2)

    def slash(lo, hi):
        """The slash of the font's not-equal sign, centered, reaching from lo to hi."""
        pts = [p for c in master.glyph("notequal") for p in c if p[2] != "offcurve"]
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        bottom = sorted(p[0] for p in pts if p[1] == y0)
        top = sorted(p[0] for p in pts if p[1] == y1)
        run = ((top[0] + top[1]) - (bottom[0] + bottom[1])) / 2 / (y1 - y0)  # x per unit of y
        mid_y, w = (lo + hi) / 2, (bottom[1] - bottom[0]) / 2
        (xa, ya), (xb, yb) = [(center + (y - mid_y) * run, y) for y in (lo, hi)]  # crosses the middle
        return [(xa - w, ya, "line"), (xa + w, ya, "line"), (xb + w, yb, "line"), (xb - w, yb, "line")]

    def notequal_reach():
        """How far the not-equal slash reaches past its bars, below and above."""
        pts = [p for c in master.glyph("notequal") for p in c if p[2] != "offcurve"]
        bars = master.rects("equal")
        return (min(r[1] for r in bars) - min(p[1] for p in pts), max(p[1] for p in pts) - max(r[3] for r in bars))

    def triple():
        bars = sorted(master.rects("equal"), key=lambda r: r[1])
        t, pitch = bars[0][3] - bars[0][1], (bars[1][1] - bars[0][1])
        mid = (bars[0][1] + bars[1][3]) / 2
        x0, x1 = left + bars[0][0], bars[0][2]
        return [(x0, mid + k * pitch - t / 2, x1, mid + k * pitch + t / 2) for k in (-1, 0, 1)]

    if seq in ("->", "=>"):
        length = n * CELL - 2 * arrows.CODE_SB
        shape = arrows.place(m, "single" if seq == "->" else "double", 0, length, slant=False)
        return [ink(c) for c in master.slanted(shift(shape, center))]
    if seq == "==":
        out = [rect(*r) for r in stretched("equal")]
    elif seq == "===":
        out = [rect(*r) for r in triple()]
    elif seq == "!=":
        bars = stretched("equal")
        below, above = notequal_reach()
        out = [rect(*r) for r in bars] + [slash(min(r[1] for r in bars) - below, max(r[3] for r in bars) + above)]
    elif seq == "!==":
        bars = triple()
        below, above = notequal_reach()
        out = [rect(*r) for r in bars] + [slash(min(r[1] for r in bars) - below, max(r[3] for r in bars) + above)]
    elif seq in ("<=", ">="):
        out = centered(master.glyph("lessequal" if seq == "<=" else "greaterequal"))
    elif seq in ("&&", "||"):
        turn = -90 if seq == "&&" else 90  # the chevron's point up (and) or down (or)
        less = [[(*arrows.rotate([(x, y)], turn)[0], k) for x, y, k in c] for c in master.glyph("less")]
        out = centered(less, cy=m.cy)
    elif seq == "++":
        rects = master.rects("plus")
        bar = next(r for r in rects if r[2] - r[0] > r[3] - r[1])
        stem = next(r for r in rects if r[3] - r[1] > r[2] - r[0])
        half, d = (bar[2] - bar[0]) / 2, (bar[2] - bar[0]) / 2
        sw = (stem[2] - stem[0]) / 2
        out = [rect(center - d - half, bar[1], center + d + half, bar[3])]
        out += [rect(cx - sw, stem[1], cx + sw, stem[3]) for cx in (center - d, center + d)]
    elif seq == "--":
        out = [rect(*r) for r in stretched("minus")]
    elif seq == "..":
        dots = sorted(master.glyph("ellipsis"), key=lambda c: bounds([c])[0])[:2]
        out = centered(dots)
    elif seq == "...":
        out = centered(master.glyph("ellipsis"))
    else:
        raise ValueError(seq)
    return [ink(c) for c in master.slanted(out)]


def contours(master, seq, style=STYLE):
    return join(master, seq) if style == "join" else substitute(master, seq)


# ---------- feature ----------

def feature(sequences):
    """Stylistic set 1: each sequence, longest first, becomes spacers and its ligature glyph,
    unless an operator character stands right before or after it."""
    lines = [f"@TW_OPERATORS = [{' '.join(OPERATORS)}];", f"@TW_LETTERS = [{' '.join(LETTERS)}];", ""]
    for seq in sorted(sequences, key=lambda s: (-len(s), SEQUENCES.index(s))):
        names = [NAMES[c] for c in seq]
        tag = "TW_" + glyph_name(seq).replace(".", "_")
        lines.append(f"lookup {tag} {{")
        lines.append(f"  ignore sub @TW_OPERATORS {names[0]}' {' '.join(names[1:])};")
        lines.append(f"  ignore sub {names[0]}' {' '.join(names[1:])} @TW_OPERATORS;")
        if seq == OPTION:
            lines.append(f"  ignore sub {names[0]}' {' '.join(names[1:])} @TW_LETTERS;")
        n = len(names)
        lines.append(f"  sub {' '.join([SPACER] * (n - 1))} {names[-1]}' by {glyph_name(seq)};")
        for i in range(n - 2, -1, -1):
            before = " ".join([SPACER] * i)
            after = " ".join(names[i + 1:])
            lines.append(f"  sub {before + ' ' if before else ''}{names[i]}' {after} by {SPACER};")
        lines.append(f"}} {tag};")
        lines.append("")
    return "\n".join(lines)
