"""Braille patterns for Twilight Code (U+2800–28FF).

Terminal programs draw graphs with braille: each cell is a 2 × 4 grid of dots, so a line plot
gets twice the columns and four times the rows of the text. The grid is spread evenly over the
whole cell (the advance width and the typographic line box): columns at a quarter and three
quarters of the width, rows at the centers of four equal bands of the height. Dots then keep
the same spacing across cell and row boundaries, and a plot reads as one continuous field.

Each dot is the font's own period, moved; the empty pattern U+2800 is a blank cell.
Dots are numbered as Unicode numbers them: bit 0 to 2 are dots 1 to 3 down the left column,
bits 3 to 5 dots 4 to 6 down the right, bits 6 and 7 the bottom dots, left and right.
"""
from arrows import shift

CODEPOINTS = list(range(0x2800, 0x2900))
# bit: (column, row from the top)
DOTS = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0), 4: (1, 1), 5: (1, 2), 6: (0, 3), 7: (1, 3)}


def glyph_name(cp):
    return f"uni{cp:04X}"


def centers(width, bottom, top):
    """Dot centers by bit."""
    h = top - bottom
    return {bit: (width * (2 * col + 1) / 4, top - h * (2 * row + 1) / 8) for bit, (col, row) in DOTS.items()}


def contours(width, bottom, top, period, cp):
    """The dots of one pattern; `period` is the period's outline as lists of (x, y, node type)."""
    xs = [p[0] for c in period for p in c]
    ys = [p[1] for c in period for p in c]
    px, py = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    out = []
    for bit, (x, y) in centers(width, bottom, top).items():
        if (cp - 0x2800) >> bit & 1:
            out += [shift(c, x - px, y - py) for c in period]
    return out
