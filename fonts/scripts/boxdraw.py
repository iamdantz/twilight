"""Box drawing, block elements and Powerline separators for Twilight Crystal Mono.

Every glyph is computed from four numbers of each master, so it interpolates with the rest of
the font and tiles with its neighbors:

- the cell: the advance width (632) and the line box, from the typographic descender to the
  typographic ascender (the line height terminals use, with no line gap);
- the light line: the thickness of the hyphen in that master; heavy lines are twice as thick,
  double lines are two light lines one light line apart.

Box drawing glyphs are read from their Unicode names: each of the four arms (up, down, left,
right) is none, light, heavy or double. Arms reach the cell edges exactly, so a line continues
into the next cell and the next row without a gap; at a junction each arm stops where the
perpendicular lines need it to (corners closed, crossings open where a double line passes).

Powerline separators span the whole cell: triangles and chevrons (U+E0B0–E0B3) and half
ellipses, filled or as a light outline (U+E0B4–E0B7).

Ink stays inside the cell: no line overshoots the advance width or the line box. A terminal
that rounds the cell up to whole pixels (632 units is 17.7 px at 28 px, drawn in an 18 px
cell) leaves a seam between cells of up to half a pixel, at about half the sizes from 11 to 32
px, and faint, since the edge pixel keeps more than half its coverage. Overshooting by the ~20
units that would close it everywhere would instead put ink in the neighboring cell at every
size: under a selection, a cursor, or a Powerline segment of another color. A seam of a
fraction of a pixel is the lesser fault; most terminals also draw these characters themselves.

Contours are counter-clockwise for ink and clockwise for holes, as in the design sources, and
the same for every master, so the masters stay compatible.
"""
import unicodedata

KAPPA = 0.5522847498
BOX = range(0x2500, 0x2580)
BLOCKS = range(0x2580, 0x25A0)
POWERLINE = (0xE0B0, 0xE0B1, 0xE0B2, 0xE0B3)
ROUNDED = (0xE0B4, 0xE0B5, 0xE0B6, 0xE0B7)
ARCS = range(0x256D, 0x2571)
CODEPOINTS = list(BOX) + list(BLOCKS) + list(POWERLINE) + list(ROUNDED)


class Cell:
    def __init__(self, width, bottom, top, light):
        self.w, self.b, self.t = width, bottom, top
        self.h = top - bottom
        self.cx, self.cy = width / 2, (top + bottom) / 2
        self.light = light
        self.heavy = 2 * light
        self.d = light  # double: line centers this far from the axis, one line apart

    def width(self, style):
        return self.heavy if style == "heavy" else self.light


# ---------- contour helpers ----------

def area(points):
    return sum(x1 * y2 - x2 * y1 for (x1, y1, _), (x2, y2, _) in zip(points, points[1:] + points[:1])) / 2


def ink(points):
    """Counter-clockwise contour (ink)."""
    on = [p for p in points if p[2] != "offcurve"]
    return points if area(on) > 0 else reverse(points)


def hole(points):
    """Clockwise contour (hole)."""
    on = [p for p in points if p[2] != "offcurve"]
    return points if area(on) < 0 else reverse(points)


def reverse(points):
    """Reverse a closed contour. A node's type names the segment that ends at it, so after
    reversal each on-curve node takes the type of the on-curve node that followed it."""
    on = [i for i, p in enumerate(points) if p[2] != "offcurve"]
    kinds = [p[2] for p in points]
    for a, b in zip(on, on[1:] + on[:1]):
        kinds[a] = points[b][2]
    return [(x, y, k) for (x, y, _), k in reversed(list(zip(points, kinds)))]


def rect(x0, y0, x1, y1):
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    return ink([(x0, y0, "line"), (x1, y0, "line"), (x1, y1, "line"), (x0, y1, "line")])


def poly(*xy):
    return ink([(x, y, "line") for x, y in xy])


# ---------- box drawing ----------

DIRS = {"UP": ["up"], "DOWN": ["down"], "LEFT": ["left"], "RIGHT": ["right"],
        "VERTICAL": ["up", "down"], "HORIZONTAL": ["left", "right"]}
STYLES = {"LIGHT": "light", "SINGLE": "light", "HEAVY": "heavy", "DOUBLE": "double"}


def arms(name):
    """Arm styles from a box drawing name, e.g. 'UP HEAVY AND RIGHT DOWN LIGHT'."""
    result = {"up": None, "down": None, "left": None, "right": None}
    pending, prefix = [], None
    for word in name.split():
        if word == "AND":
            if pending and prefix:
                for d in pending:
                    result[d] = prefix
                pending = []
        elif word in DIRS:
            pending += DIRS[word]
        elif word in STYLES:
            if pending:
                for d in pending:
                    result[d] = STYLES[word]
                pending = []
            else:
                prefix = STYLES[word]
    for d in pending:
        result[d] = prefix
    return result


def junction(c, a):
    """Contours for a junction of up to four arms."""
    out = []
    horizontal = {"left": -1, "right": 1}
    vertical = {"down": -1, "up": 1}
    out += axis_lines(c, a, horizontal, vertical, True)
    out += axis_lines(c, a, vertical, horizontal, False)
    return out


def axis_lines(c, a, along, across, is_horizontal):
    """The lines of the arms along one axis (left/right or down/up)."""
    center = c.cx if is_horizontal else c.cy
    edge = {-1: 0 if is_horizontal else c.b, 1: c.w if is_horizontal else c.t}
    mid = c.cy if is_horizontal else c.cx
    styles = {side: a[side] for side in along}
    perp = {sgn: a[name] for name, sgn in across.items()}  # style of the perpendicular arm on each side
    lines = []

    def seg(sign, k, offset, width):
        """A line on side `sign`, from the edge to `k` units before the center, at `offset`."""
        lines.append((sign, k, offset, width))

    doubles = [s for s, st in styles.items() if st == "double"]
    if doubles:
        for o in (1, -1):
            p, q = perp[o], perp[-o]
            for side in doubles:
                sign = along[side]
                if p == "double":
                    k = c.d - c.light / 2
                elif p in ("light", "heavy"):
                    k = -c.width(p) / 2
                elif q == "double":
                    k = -(c.d + c.light / 2)
                elif q in ("light", "heavy"):
                    k = -c.width(q) / 2
                else:
                    k = 0
                seg(sign, k, o * c.d, c.light)
    for side, st in styles.items():
        if st not in ("light", "heavy"):
            continue
        sign = along[side]
        other = styles[[s for s in along if s != side][0]]
        if "double" in perp.values():
            through = perp[1] == "double" and perp[-1] == "double"
            if other in ("light", "heavy"):
                k = 0
            elif through:
                k = c.d - c.light / 2
            else:
                k = -(c.d + c.light / 2)
        else:
            k = -max([c.width(s) / 2 for s in perp.values() if s] or [0])
        seg(sign, k, 0, c.width(st))

    def box(start, end, offset, width):
        lo, hi = mid + offset - width / 2, mid + offset + width / 2
        return rect(start, lo, end, hi) if is_horizontal else rect(lo, start, hi, end)

    # Two halves of one straight line that meet or cross at the center, with the same width
    # and offset, are drawn as one rectangle, so no two contours share an edge.
    out = []
    while lines:
        sign, k, offset, width = lines.pop(0)
        twin = next((l for l in lines if l[0] == -sign and l[2:] == (offset, width) and l[1] <= 0 and k <= 0), None)
        if twin:
            lines.remove(twin)
            out.append(box(edge[-1], edge[1], offset, width))
        else:
            out.append(box(center + sign * k, edge[sign], offset, width))
    return out


def dashes(c, n, style, is_horizontal):
    """n dashes per cell, gaps split across the cell edges so the pattern tiles."""
    length = c.w if is_horizontal else c.h
    step = length / n
    gap = step / 2 if n == 2 else step / 3
    width = c.width(style)
    out = []
    for i in range(n):
        s0, s1 = i * step + gap / 2, (i + 1) * step - gap / 2
        if is_horizontal:
            out.append(rect(s0, c.cy - width / 2, s1, c.cy + width / 2))
        else:
            out.append(rect(c.cx - width / 2, c.b + s0, c.cx + width / 2, c.b + s1))
    return out


def arc(c, vertical_dir, horizontal_dir):
    """A light quarter arc joining two arms: radius half the cell width, centered on the corner
    of the quadrant it turns into, with a straight run on the vertical arm to the cell edge.
    Drawn for down-and-right, then mirrored."""
    r, t = c.w / 2, c.light / 2
    R1, R0 = r + t, r - t
    cx, cy, w = c.cx, c.cy, c.w
    pts = [
        (cx - t, c.b, "line"),
        (cx - t, cy - r, "line"),
        (cx - t, cy - r + KAPPA * R1, "offcurve"),
        (w - KAPPA * R1, cy + t, "offcurve"),
        (w, cy + t, "curve"),
        (w, cy - t, "line"),
        (w - KAPPA * R0, cy - t, "offcurve"),
        (cx + t, cy - r + KAPPA * R0, "offcurve"),
        (cx + t, cy - r, "curve"),
        (cx + t, c.b, "line"),
    ]
    if vertical_dir == "up":
        pts = [(x, 2 * cy - y, k) for x, y, k in pts]
    if horizontal_dir == "left":
        pts = [(w - x, y, k) for x, y, k in pts]
    return [ink(pts)]


def diagonal(c, rising):
    """A light line from corner to corner; it runs past the cell by the half-width it needs."""
    from math import hypot
    hx = c.light / 2 * hypot(c.w, c.h) / c.h
    if rising:
        return [poly((-hx, c.b), (hx, c.b), (c.w + hx, c.t), (c.w - hx, c.t))]
    return [poly((-hx, c.t), (hx, c.t), (c.w + hx, c.b), (c.w - hx, c.b))]


def box(c, cp):
    name = unicodedata.name(chr(cp))[len("BOX DRAWINGS "):]
    words = name.split()
    if "DASH" in words:
        n = {"DOUBLE": 2, "TRIPLE": 3, "QUADRUPLE": 4}[words[1]]
        return dashes(c, n, STYLES[words[0]], words[-1] == "HORIZONTAL")
    if "ARC" in words:
        return arc(c, words[2].lower(), words[4].lower())
    if "DIAGONAL" in words:
        if words[-1] == "CROSS":
            return diagonal(c, True) + diagonal(c, False)
        return diagonal(c, words[2] == "UPPER" and words[3] == "RIGHT")
    return junction(c, arms(name))


# ---------- block elements ----------

def blocks(c, cp):
    w, b, t, h = c.w, c.b, c.t, c.h
    eighth_h, eighth_w = h / 8, w / 8
    if cp == 0x2580:
        return [rect(0, c.cy, w, t)]
    if 0x2581 <= cp <= 0x2588:
        return [rect(0, b, w, b + (cp - 0x2580) * eighth_h)]
    if 0x2589 <= cp <= 0x258F:
        return [rect(0, b, (0x2590 - cp) * eighth_w, t)]
    if cp == 0x2590:
        return [rect(c.cx, b, w, t)]
    if cp in (0x2591, 0x2592, 0x2593):
        cols, rows = 4, 8
        sw, sh = w / cols, h / rows
        out = []
        for j in range(rows):
            y0, y1 = b + j * sh, b + (j + 1) * sh
            if cp == 0x2591:      # light: one square in four
                out += [rect(i * sw, y0, (i + 1) * sw, y1) for i in range(cols) if i % 2 == 0 and j % 2 == 0]
            elif cp == 0x2592:    # medium: checkerboard
                out += [rect(i * sw, y0, (i + 1) * sw, y1) for i in range(cols) if (i + j) % 2 == 0]
            else:                 # dark: all but one square in four, merged by row
                if j % 2 == 0:
                    out += [rect(i * sw, y0, (i + 1) * sw, y1) for i in range(cols) if i % 2 == 1]
                else:
                    out.append(rect(0, y0, w, y1))
        return out
    if cp == 0x2594:
        return [rect(0, t - eighth_h, w, t)]
    if cp == 0x2595:
        return [rect(w - eighth_w, b, w, t)]
    quads = {0x2596: "LL", 0x2597: "LR", 0x2598: "UL", 0x2599: "UL LL LR", 0x259A: "UL LR",
             0x259B: "UL UR LL", 0x259C: "UL UR LR", 0x259D: "UR", 0x259E: "UR LL", 0x259F: "UR LL LR"}
    box_of = {"UL": (0, c.cy, c.cx, t), "UR": (c.cx, c.cy, w, t), "LL": (0, b, c.cx, c.cy), "LR": (c.cx, b, w, c.cy)}
    names = quads[cp].split()
    rects = []
    for row in ("U", "L"):  # two quadrants on one row become one rectangle
        if row + "L" in names and row + "R" in names:
            _, y0, _, y1 = box_of[row + "L"]
            rects.append(rect(0, y0, w, y1))
            names = [n for n in names if n[0] != row]
    return rects + [rect(*box_of[n]) for n in names]


# ---------- Powerline ----------

def powerline(c, cp):
    w, b, t, cy = c.w, c.b, c.t, c.cy
    if cp == 0xE0B0:
        return [poly((0, b), (w, cy), (0, t))]
    if cp == 0xE0B2:
        return [poly((w, b), (w, t), (0, cy))]
    # thin separators: a light chevron through the full cell height
    from math import hypot
    a = c.light * hypot(w, t - cy) / w  # vertical thickness of a slanted light stroke
    e = a * w / (t - cy)                # how far the inner apex sits from the outer one
    pts = [(0, t), (w, cy), (0, b), (0, b + a), (w - e, cy), (0, t - a)]
    if cp == 0xE0B3:
        pts = [(w - x, y) for x, y in pts]
    return [poly(*pts)]


def rounded(c, cp):
    """Rounded separators: a half ellipse from the full height of the left edge to the right
    edge at the middle (E0B4), its light outline (E0B5), and both mirrored (E0B6, E0B7)."""
    w, b, t, cy = c.w, c.b, c.t, c.cy

    def half(rx, ry):  # from the bottom of the left edge round to its top
        k = KAPPA
        return [(0, cy - ry, "line"), (k * rx, cy - ry, "offcurve"), (rx, cy - k * ry, "offcurve"), (rx, cy, "curve"),
                (rx, cy + k * ry, "offcurve"), (k * rx, cy + ry, "offcurve"), (0, cy + ry, "curve")]
    outer = half(w, (t - b) / 2)
    if cp in (0xE0B4, 0xE0B6):
        pts = outer
    else:
        q0, a, bb, q1, cc, d, q2 = half(w - c.light, (t - b) / 2 - c.light)
        # back along the inner arc: a line across the stroke at the top, then the two arcs
        pts = outer + [(q2[0], q2[1], "line"), d, cc, (q1[0], q1[1], "curve"), bb, a, (q0[0], q0[1], "curve")]
    if cp in (0xE0B6, 0xE0B7):
        pts = [(w - x, y, k) for x, y, k in pts]
    return [ink(pts)]


def contours(cell, cp):
    if cp in BOX:
        return box(cell, cp)
    if cp in BLOCKS:
        return blocks(cell, cp)
    if cp in ROUNDED:
        return rounded(cell, cp)
    return powerline(cell, cp)


def glyph_name(cp):
    return f"uni{cp:04X}"
