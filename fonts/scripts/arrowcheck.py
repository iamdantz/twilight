"""Arrows in Twilight Text and Twilight Code: same stroke, axis and spacing as the font.

At every named instance of every variable font, measured on the outlines:

1. Stroke. A cross-section of the shaft of each arrow, a quarter of the way from its tail,
   crosses one line as thick as the bar of the plus sign at that instance; for a double arrow,
   two lines as thick and as far apart as the lines of the equal sign. Within two units for a
   thickness and one for a position, the rounding of points to whole units.
2. Axis. Horizontal arrows sit on the plus sign's bar center (the math axis); every arrow's
   ink is centered on it. Within one unit.
3. Mirrors. Each arrow and its opposite (← →, ↑ ↓, ↖ ↘, ↗ ↙, ⇐ ⇒, ⇑ ⇓, ↩ ↪) have the same
   advance width and ink height, and in upright fonts the same ink width.
4. Contours. No contour crosses itself, so the outline is the same in every renderer.
5. Cell. In Twilight Code every arrow is 632 units wide and its ink stays inside the cell.

    python fonts/scripts/arrowcheck.py
"""
import sys
import tempfile
from pathlib import Path

import pathops
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arrows  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "fonts" / "build"
TOLERANCE = 1.0  # positions: every point is rounded to whole units in the sources
WIDTH_TOLERANCE = 2.0  # thicknesses: two rounded edges, against a reference with two more
PAIRS = [(0x2190, 0x2192), (0x2191, 0x2193), (0x2196, 0x2198), (0x2197, 0x2199), (0x21D0, 0x21D2),
         (0x21D1, 0x21D3), (0x21A9, 0x21AA)]
SHAFTS = {0x2190: "h", 0x2192: "h", 0x2191: "v", 0x2193: "v", 0x2194: "h", 0x2195: "v",
          0x21D0: "h", 0x21D2: "h", 0x21D1: "v", 0x21D3: "v", 0x21D4: "h", 0x21D5: "v"}


def outline(font, cp):
    glyphs = font.getGlyphSet()
    path = pathops.Path()
    glyphs[font.getBestCmap()[cp]].draw(path.getPen(glyphSet=glyphs))
    return path


def spans(path, axis, at):
    """Intervals of ink along a line: axis "v" is the vertical line x = at (giving y intervals),
    "h" the horizontal line y = at (giving x intervals). Read from a strip one unit wide."""
    xmin, ymin, xmax, ymax = path.bounds
    box = (at - 0.5, ymin - 1, at + 0.5, ymax + 1) if axis == "v" else (xmin - 1, at - 0.5, xmax + 1, at + 0.5)
    rect = pathops.Path()
    pen = rect.getPen()
    x0, y0, x1, y1 = box
    pen.moveTo((x0, y0)); pen.lineTo((x1, y0)); pen.lineTo((x1, y1)); pen.lineTo((x0, y1)); pen.closePath()
    cut = pathops.op(path, rect, pathops.PathOp.INTERSECTION, fix_winding=True)
    found = []
    for contour in cut.contours:
        b = contour.bounds
        found.append((b[1], b[3]) if axis == "v" else (b[0], b[2]))
    return sorted(found)


def check(path):
    font = TTFont(path)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    problems = []

    def bar_of(cp):
        p = pathops.simplify(outline(font, cp))
        x0, _, x1, _ = p.bounds
        return spans(p, "v", x0 + 0.15 * (x1 - x0))

    (lo, hi), = bar_of(ord("+"))
    t, cy = hi - lo, (lo + hi) / 2
    eq = bar_of(ord("="))
    e = (eq[1][0] + eq[1][1] - eq[0][0] - eq[0][1]) / 4
    present = [cp for cp in arrows.CODEPOINTS if cp in cmap]
    italic = font["post"].italicAngle != 0
    fixed = hmtx[cmap[ord("i")]][0] == hmtx[cmap[ord("m")]][0]

    for cp in present:
        raw = outline(font, cp)
        p = pathops.simplify(raw)
        x0, y0, x1, y1 = p.bounds
        label = f"{chr(cp)} U+{cp:04X}"
        if abs((y0 + y1) / 2 - cy) > TOLERANCE:
            problems.append(f"{label}: ink centered at {(y0 + y1) / 2:.1f}, axis at {cy:.1f}")
        for contour in raw.contours:
            alone = pathops.Path()
            contour.draw(alone.getPen())
            if abs(abs(alone.area) - pathops.simplify(alone).area) > 1:
                problems.append(f"{label}: a contour crosses itself")
        if cp in SHAFTS:
            kind, direction = arrows.ARROWS[cp]
            # a quarter of the way from the tail; arrows with two heads are measured at the middle
            frac = 0.5 if "both" in kind else (0.25 if direction in (0, 90) else 0.75)
            if SHAFTS[cp] == "h":
                # only the band the lines occupy: an italic head's arm can reach the middle above or below it
                band = (cy - e - t, cy + e + t)
                got = [g for g in spans(p, "v", x0 + frac * (x1 - x0)) if g[1] > band[0] and g[0] < band[1]]
                centers = [cy] if "double" not in kind else [cy - e, cy + e]
                want = [(c - t / 2, c + t / 2) for c in centers]
                if len(got) != len(want) or any(abs(g - w) > TOLERANCE for gs, ws in zip(got, want) for g, w in zip(gs, ws)):
                    problems.append(f"{label}: shaft {fmt(got)}, expected {fmt(want)}")
            else:
                # vertical shafts may lean (italic): check thickness and spacing, not position
                got = spans(p, "h", y0 + frac * (y1 - y0))
                lines = 1 if "double" not in kind else 2
                ok = len(got) == lines and all(abs((b - a) - t) <= WIDTH_TOLERANCE for a, b in got)
                if ok and lines == 2:
                    ok = abs((got[1][0] + got[1][1] - got[0][0] - got[0][1]) / 4 - e) <= TOLERANCE
                if not ok:
                    problems.append(f"{label}: shaft {fmt(got)}, expected {lines} line(s) {t:.1f} thick"
                                    + (f", {2 * e:.1f} apart" if lines == 2 else ""))
        if fixed:
            if hmtx[cmap[cp]][0] != 632:
                problems.append(f"{label}: advance {hmtx[cmap[cp]][0]}, not the 632-unit cell")
            if x0 < 0 or x1 > 632:
                problems.append(f"{label}: ink from {x0:.0f} to {x1:.0f}, outside the cell")
    for a, b in PAIRS:
        if a not in cmap or b not in cmap:
            continue
        pa, pb = pathops.simplify(outline(font, a)), pathops.simplify(outline(font, b))
        (ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1) = pa.bounds, pb.bounds
        # slanting breaks the mirror in width; advance and height must still match
        same_width = italic or abs((ax1 - ax0) - (bx1 - bx0)) <= TOLERANCE
        if hmtx[cmap[a]][0] != hmtx[cmap[b]][0] or not same_width or abs((ay1 - ay0) - (by1 - by0)) > TOLERANCE:
            problems.append(f"{chr(a)} {chr(b)}: not mirror images in size or advance")
    return len(present), problems


def fmt(spans):
    return "[" + ", ".join(f"{a:.1f}–{b:.1f}" for a, b in spans) + "]"


def main():
    failed = False
    for variable in sorted(BUILD.glob("*/fonts/variable/*.ttf")):
        for inst in TTFont(variable)["fvar"].instances:
            with tempfile.NamedTemporaryFile(suffix=".ttf") as tmp:
                instancer.instantiateVariableFont(TTFont(variable), inst.coordinates).save(tmp.name)
                count, problems = check(tmp.name)
            print(f"{'FAIL' if problems else 'ok':4} {variable.name} wght {inst.coordinates['wght']:g}: {count} arrows")
            for p in problems[:20]:
                print(f"     {p}")
            failed |= bool(problems)
    print("arrows: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
