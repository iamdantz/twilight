"""Heavier comma tails for Twilight Text and Twilight Code.

Measured at 6 to 8 px x-height against the fonts the typeface was chosen from, the comma was
the weakest point of both families: ; against : and , against . ranked in the lowest 5 % of
the sans and of the monospaced fonts, below every confusable pair of letters. The tail is not
short (as deep as in most fonts, nine tenths of the p's descender); it is light: the comma
carries 1.53 times the ink of the period, against a median of 1.65, and at small sizes its tail
all but disappears, so a comma reads as a period and a semicolon as a colon. In Spanish and
Portuguese the comma is the decimal sign.

The tail is thickened, not lengthened: a longer tail that reaches the median distinction would
hang 1.9 times as deep as the p's descender, deeper than in any of the monospaced fonts. Both
edges of the tail move out perpendicular to themselves: the node where an edge meets the dot's
bowl moves with its handle, so the tail still grows smoothly out of the dot, and the node at
the end slides along the end, so the tail keeps its angle and depth. The edge on the side the
tail leans toward (a comma leans under the descender of the letter before it, an opening
quote over the letter after it) grows by 20 % of the tail's end width, the largest step of
10 % that touches no neighbor at any weight (30 % touches q at Bold); the other edge grows by
80 %, the first step of 10 % at which ; against : and , against . clear the median of those
fonts at Regular, upright and italic, in both families, by more than the measure's noise (70 %
clears it by 0.2 %, 80 % by 3.9 %). The comma then carries about 2.2 times the period's ink,
among the heaviest of those fonts (their 95th percentile is 2.1). Every comma-shaped mark gets
the same tail, so they stay one shape: the comma (and the semicolon, built from it), the low
quotes ‚ „ and the high quotes ’ ” ‘ “, whose tails point up.
"""
import math

NAMES = ["comma", "quotesinglbase", "quotedblbase", "quoteleft", "quoteright", "quotedblleft",
         "quotedblright"]
THICKEN = 0.8  # of the tail's width at its end, on the edge away from where the tail leans
INNER = 0.2  # on the edge the tail leans toward, the side of a neighboring letter


def thicken(nodes, share=THICKEN, inner=INNER):
    """One contour as (x, y, node type); returns it with its tail thickened.

    The tail ends in the two line nodes at the extreme height farthest from the contour's
    middle (the bottom for commas and low quotes, the top for opening quotes). Both edges that
    reach them move outward: the one on the side the tail leans toward by `inner` of the tail's
    end width, the other by `share`."""
    ys = [y for _, y, _ in nodes]
    middle = sum(ys) / len(ys)
    end = min(ys) if middle - min(ys) > max(ys) - middle else max(ys)
    ends = [i for i, (x, y, kind) in enumerate(nodes) if y == end and kind != "offcurve"]
    if len(ends) != 2:
        raise ValueError(f"expected a tail ending in two nodes, found {len(ends)}")
    n = len(nodes)
    width = abs(nodes[ends[0]][0] - nodes[ends[1]][0])
    on_curve = [x for x, _, kind in nodes if kind != "offcurve"]
    lean = (nodes[ends[0]][0] + nodes[ends[1]][0]) / 2 - sum(on_curve) / len(on_curve)
    out = list(nodes)
    for i in ends:
        other = ends[1] if i == ends[0] else ends[0]
        for step in (1, -1):
            j = (i + step) % n
            while nodes[j][2] == "offcurve":
                j = (j + step) % n
            if j != other:
                break
        handle = (j + step) % n
        if nodes[handle][2] != "offcurve":
            raise ValueError("expected each tail edge to meet the dot's bowl at a curve")
        # the edge on the side the tail leans toward (left for a comma, under the descender of
        # the letter before it; right for an opening quote, over the letter after it) moves by
        # `inner` of the width, the other by `share`
        toward = (nodes[i][0] - nodes[other][0]) * lean > 0
        shift = width * (inner if toward else share)
        ex, ey = nodes[i][0] - nodes[j][0], nodes[i][1] - nodes[j][1]
        length = math.hypot(ex, ey)
        nx, ny = -ey / length, ex / length
        if nx * (nodes[other][0] - nodes[i][0]) + ny * (nodes[other][1] - nodes[i][1]) > 0:
            nx, ny = -nx, -ny  # away from the other edge
        for k in (j, handle):
            x, y, kind = nodes[k]
            out[k] = (x + nx * shift, y + ny * shift, kind)
        # the end node slides along the end, where the moved edge now meets it, so the tail
        # keeps its depth
        x, y, kind = nodes[i]
        out[i] = (x + math.copysign(shift * length / abs(ey), nx), y, kind)
    return out
