"""Hinting of the static fonts: present where it should be, and no worse than upstream's.

The static TTF and WOFF2 fonts are hinted by ttfautohint through the upstream build
configuration; the variable fonts are unhinted, as upstream's are. For every static font this
check compares it, rendered by FreeType (TrueType bytecode, interpreter v40, grayscale), with
the same weight of the upstream font hinted the same way (an instance of the upstream variable
font through ttfautohint with the builder's defaults):

1. Coverage. Every glyph with contours carries instructions.
2. Clipping. From 9 to 50 ppem, no character's ink (a quarter coverage or more) goes past the
   Windows clipping box (usWinAscent and usWinDescent, rounded to pixels) unless the same
   character, at the same size, does so in the upstream font.
3. Alignment, 9 to 20 ppem. The share of x-height letters (flat and round) whose top row
   differs from the most common one, and the same for capitals and for the baseline: no higher
   than upstream's.
4. Crispness, 9 to 20 ppem. The mean coverage of the outermost row of flat horizontal edges (1
   when an edge falls on a pixel boundary): no lower than upstream's, less 0.01.
5. Distinction, 9 to 14 ppem. The worst of the confusable pairs I-l, l-1, I-1, O-0, rn-m and
   cl-d (pixel difference over the union of ink, best of three one-pixel alignments): no lower
   than upstream's, less 0.01.

6. Cell (Twilight Code, whose box drawing, blocks and Powerline separators carry the
   instructions of fonts/scripts/cellhint.py), 9 to 24 ppem, on ─ ━ ═ ┼ ╋ ╬ ┬ ┴ ├ ┤ ╪ ╫ ▀ ▄ █:
   no ink beyond the rows of the cell (its top and bottom rounded to pixels); at least 90 % of
   the rows a horizontal line covers are fully covered (crisp); the light line falls on the
   same rows in every glyph that has one, so junctions meet.

Unhinted rendering of the same font is reported beside it, as the reference for what hinting
adds.

    python fonts/scripts/hintcheck.py /tmp/reference
"""
import argparse
import io
import statistics
import sys
import tempfile
from pathlib import Path

import freetype
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from ttfautohint import ttfautohint

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstream  # noqa: E402

ROOT = upstream.ROOT
BUILD = ROOT / "fonts" / "build"
HINTED, UNHINTED = freetype.FT_LOAD_DEFAULT, freetype.FT_LOAD_NO_HINTING
XHEIGHT, FLAT_X, BASE, CAPS = "xzvwuyronecsamp", "xzvw", "xznmhlik", "HETFIZ"
PAIRS = [("I", "l"), ("l", "1"), ("I", "1"), ("O", "0"), ("rn", "m"), ("cl", "d")]
WEIGHTS = {"ExtraLight": 200, "Light": 300, "Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700,
           "ExtraBold": 800}
SLACK = 0.01
LINES = "─━═┼╋╬┬┴├┤╪╫▀▄█"
LIGHT = "─┼┬┴┤"


def render(face, text, flag, ppem):
    face.set_pixel_sizes(0, ppem)
    img = np.zeros((4 * ppem, 6 * ppem))
    x = ppem // 2
    for ch in text:
        face.load_char(ch, flag | freetype.FT_LOAD_RENDER)
        g, bm = face.glyph, face.glyph.bitmap
        if bm.rows:
            a = np.array(bm.buffer, float).reshape(bm.rows, bm.pitch)[:, :bm.width] / 255
            y0, x0 = 2 * ppem - g.bitmap_top, x + g.bitmap_left
            img[y0:y0 + bm.rows, x0:x0 + bm.width] = np.maximum(img[y0:y0 + bm.rows, x0:x0 + bm.width], a)
        x += (g.advance.x + 32) >> 6
    return img


def edge_row(a, top=True):
    """The outermost row carrying at least half the glyph's peak coverage."""
    rows = np.flatnonzero(a.max(1) >= a.max() / 2)
    return rows[0] if top else rows[-1]


def quality(path, flag):
    face = freetype.Face(str(path))
    crisp, misaligned, pairs = [], [], []
    for ppem in range(9, 21):
        edges = [render(face, ch, flag, ppem) for ch in FLAT_X + CAPS]
        values = [a[np.flatnonzero(a.max(1) > 0.02)[0]].max() for a in edges]
        values += [a[np.flatnonzero(a.max(1) > 0.02)[-1]].max() for a in (render(face, ch, flag, ppem) for ch in BASE)]
        crisp.append(np.mean(values))
        for chars, top in ((XHEIGHT, True), (CAPS + "OCS", True), (BASE + "ocs", False)):
            rows = [edge_row(render(face, ch, flag, ppem), top) for ch in chars]
            mode = statistics.mode(rows)
            misaligned.append(sum(r != mode for r in rows) / len(rows))
        if ppem <= 14:
            for p, q in PAIRS:
                a, b = render(face, p, flag, ppem), render(face, q, flag, ppem)
                pairs.append(min(np.abs(a - np.roll(b, s, 1)).sum() / max(np.maximum(a, np.roll(b, s, 1)).sum(), 1e-9)
                                 for s in (-1, 0, 1)))
    return {"crispness": float(np.mean(crisp)), "misaligned": float(np.mean(misaligned)),
            "worst pair": float(min(pairs))}


def clipped(path, ppems=range(9, 51)):
    """(character, ppem) whose hinted ink goes past the Windows clipping box."""
    font = TTFont(path)
    os2, upm = font["OS/2"], font["head"].unitsPerEm
    face = freetype.Face(str(path))
    out = set()
    for ppem in ppems:
        face.set_pixel_sizes(0, ppem)
        top, bottom = round(os2.usWinAscent * ppem / upm), round(os2.usWinDescent * ppem / upm)
        for cp in font.getBestCmap():
            if cp < 33:
                continue
            face.load_char(chr(cp), HINTED | freetype.FT_LOAD_RENDER)
            g = face.glyph
            if not g.bitmap.rows:
                continue
            a = np.array(g.bitmap.buffer, float).reshape(g.bitmap.rows, g.bitmap.pitch)[:, :g.bitmap.width] / 255
            rows = np.flatnonzero(a.max(1) >= 0.25)
            if rows.size and (g.bitmap_top - rows[0] > top or rows[-1] + 1 - g.bitmap_top > bottom):
                out.add((chr(cp), ppem))
    return out


def upstream_static(variable, wght, out):
    """The upstream font at one weight, made static as the builder makes it (overlaps removed)
    and hinted as the builder hints (ttfautohint defaults)."""
    buf = io.BytesIO()
    instancer.instantiateVariableFont(TTFont(variable), {"wght": wght},
                                      overlap=instancer.OverlapMode.REMOVE).save(buf)
    out.write_bytes(ttfautohint(in_buffer=buf.getvalue()))
    return out


def coverage(path):
    font = TTFont(path)
    glyf = font["glyf"]
    if "fpgm" not in font:
        return ["not hinted"]
    return [f"{name} has no instructions" for name in font.getGlyphOrder()
            if not glyf[name].isComposite() and glyf[name].numberOfContours > 0
            and not (hasattr(glyf[name], "program") and len(glyf[name].program.getBytecode()))]


def cell(path):
    """Box drawing in the hinted font: inside the cell rows, crisp, light lines aligned."""
    font = TTFont(path)
    os2, upm = font["OS/2"], font["head"].unitsPerEm
    face = freetype.Face(str(path))
    problems, crisp = [], []
    for ppem in range(9, 25):
        face.set_pixel_sizes(0, ppem)
        top, bottom = round(os2.sTypoAscender * ppem / upm), round(os2.sTypoDescender * ppem / upm)
        light_rows = set()
        for ch in LINES:
            face.load_char(ch, HINTED | freetype.FT_LOAD_RENDER)
            g, bm = face.glyph, face.glyph.bitmap
            a = np.array(bm.buffer, float).reshape(bm.rows, bm.pitch)[:, :bm.width] / 255
            if g.bitmap_top > top or g.bitmap_top - bm.rows < bottom:
                problems.append(f"{ch} at {ppem} ppem: ink from {g.bitmap_top - bm.rows} to {g.bitmap_top}, "
                                f"cell {bottom} to {top}")
            # a column at the edge where the line leaves the cell crosses only horizontal lines
            column = a[:, -1] if ch == "├" else a[:, 0]
            profile = a.max(1) if ch in "▀▄█" else column
            inked = profile[profile > 0.02]
            crisp.append((inked >= 0.9).sum() / max(len(inked), 1))
            if ch in LIGHT:
                light_rows.add(tuple(np.flatnonzero(column > 0.02) - g.bitmap_top))
        if len(light_rows) > 1:
            problems.append(f"at {ppem} ppem the light line falls on different rows: {sorted(light_rows)}")
    if np.mean(crisp) < 0.9:
        problems.append(f"lines crisp in {np.mean(crisp):.0%} of rows, below 90 %")
    return problems, float(np.mean(crisp))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reference", help="directory written by upstream.py reference")
    args = parser.parse_args()
    tmp = Path(tempfile.mkdtemp())
    failed = False
    for family in upstream.load()["families"]:
        old, new = family["upstream"]["file"], family["file"]
        for path in sorted((BUILD / new / "fonts" / "ttf").glob("*.ttf")):
            style = path.stem.split("-", 1)[1]
            italic = style.endswith("Italic")
            weight = WEIGHTS.get(style.replace("Italic", "") or "Regular", 400)
            ref_var = Path(args.reference) / new / f"{old}{'-Italic' if italic else ''}[wght].ttf"
            ref = upstream_static(ref_var, weight, tmp / f"ref-{path.name}")
            problems = coverage(path)
            lines = ""
            if new == "TwilightCode":
                found, crisp = cell(path)
                problems += found
                lines = f", box lines crisp {crisp:.2f}"
            extra = sorted(clipped(path) - clipped(ref))
            if extra:
                problems.append("clipped beyond upstream: " + ", ".join(f"{c} at {p}" for c, p in extra[:10]))
            ours, theirs, raw = quality(path, HINTED), quality(ref, HINTED), quality(path, UNHINTED)
            if ours["misaligned"] > theirs["misaligned"]:
                problems.append(f"misaligned {ours['misaligned']:.3f}, upstream {theirs['misaligned']:.3f}")
            for key in ("crispness", "worst pair"):
                if ours[key] < theirs[key] - SLACK:
                    problems.append(f"{key} {ours[key]:.3f}, upstream {theirs[key]:.3f}")
            print(f"{'FAIL' if problems else 'ok':4} {path.name}: crispness {ours['crispness']:.2f} "
                  f"(unhinted {raw['crispness']:.2f}), misaligned {ours['misaligned']:.3f} "
                  f"(unhinted {raw['misaligned']:.3f}), worst pair {ours['worst pair']:.2f} "
                  f"(upstream {theirs['worst pair']:.2f}){lines}")
            for p in problems[:10]:
                print(f"     {p}")
            failed |= bool(problems)
    print("hinting: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
