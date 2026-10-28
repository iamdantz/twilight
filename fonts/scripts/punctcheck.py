"""Comma tails in Twilight Text and Twilight Code (fonts/scripts/punctuation.py).

At every named instance of every variable font, against the upstream font at the same instance:

1. Shape. Each reshaped glyph (comma, semicolon, ‚ „ ‘ ’ “ ”) keeps all of upstream's ink and
   adds to it (the tail thickened); the comma's ink over the period's is reported.
2. Distinction. ; against : and , against . at 6 to 8 px x-height (pixel difference of the two
   strings drawn from the same origin, over the union of their ink, best of three one-pixel
   alignments, averaged over five sizes and four sub-pixel positions): higher than upstream at
   every instance, and at Regular, upright and italic, at least the median of the fonts the
   typeface was chosen from (MEDIANS, measured once with this method: about 550 sans and 61
   monospaced font files of the Google Fonts collection).
3. Room. A heavier tail touches no neighbor: g j p q y ç f ÿ followed by , ‚ „ ;, opening quotes
   followed by T V W Y A J f j t l, and T V W Y F P f r l t followed by closing quotes share no ink.

    python fonts/scripts/punctcheck.py /tmp/reference
"""
import argparse
import sys
import tempfile
from pathlib import Path

import numpy as np
import pathops
import uharfbuzz as hb
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import punctuation  # noqa: E402
import upstream  # noqa: E402

ROOT = upstream.ROOT
BUILD = ROOT / "fonts" / "build"
MEDIANS = {"TwilightText": {";:": 0.366, ",.": 0.496}, "TwilightCode": {";:": 0.330, ",.": 0.484}}
RESHAPED = punctuation.NAMES + ["semicolon"]
SIZES, PHASES, OVERSAMPLE = (6, 6.5, 7, 7.5, 8), (0, 0.25, 0.5, 0.75), 8
DESCENDERS, MARKS = "gjpqyçfÿ", ",‚„;"
# quotes against the letters that reach toward them
NEIGHBORS = [d + m for d in DESCENDERS for m in MARKS] + [q + c for q in "‘“" for c in "TVWYAJfjtl"] + \
            [c + q for q in "’”" for c in "TVWYFPfrlt"]


def small(path, text, xh, phase):
    font = TTFont(path)
    x_em = font["OS/2"].sxHeight / font["head"].unitsPerEm
    k = OVERSAMPLE
    image = Image.new("L", (160 * k, 40 * k), 0)
    ImageDraw.Draw(image).text((10 * k + round(phase * k), 30 * k), text,
                               font=ImageFont.truetype(str(path), xh * k / x_em), fill=255, anchor="ls")
    return (np.asarray(image, float) / 255).reshape(40, k, 160, k).mean((1, 3))


def pair(path, p, q):
    scores = []
    for xh in SIZES:
        for phase in PHASES:
            a, b = small(path, p, xh, phase), small(path, q, xh, phase)
            scores.append(min(np.abs(a - np.roll(b, s, 1)).sum() / max(np.maximum(a, np.roll(b, s, 1)).sum(), 1e-9)
                              for s in (-1, 0, 1)))
    return float(np.mean(scores))


def ink(font, name):
    glyphs = font.getGlyphSet()
    path = pathops.Path()
    glyphs[name].draw(path.getPen(glyphSet=glyphs))
    return pathops.simplify(path, fix_winding=True)


def shape_problems(ours, ref):
    """The reshaped glyphs only gain ink: everything upstream drew is still inked (within
    0.5 % of its area, the delta rounding of the variable font), and they draw more."""
    problems = []
    for name in RESHAPED:
        a, b = ink(ours, name), ink(ref, name)
        lost = pathops.op(b, a, pathops.PathOp.DIFFERENCE).area
        gained = pathops.op(a, b, pathops.PathOp.DIFFERENCE).area
        if lost > 0.005 * b.area or gained <= 0:
            problems.append(f"{name}: lost {lost:.0f} units² of upstream ink, gained {gained:.0f}")
    return problems


def overlaps(path):
    font = TTFont(path)
    glyphs = font.getGlyphSet()
    shaper = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))
    found = []
    for text in NEIGHBORS:
        if True:
            buf = hb.Buffer()
            buf.add_str(text)
            buf.guess_segment_properties()
            hb.shape(shaper, buf, {})
            x, inks = 0, []
            for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
                p = pathops.Path()
                glyphs[shaper.glyph_to_string(info.codepoint)].draw(
                    TransformPen(p.getPen(glyphSet=glyphs), (1, 0, 0, 1, x + pos.x_offset, pos.y_offset)))
                inks.append(pathops.simplify(p))
                x += pos.x_advance
            if pathops.op(inks[0], inks[1], pathops.PathOp.INTERSECTION).area > 0:
                found.append(text)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reference", help="directory written by upstream.py reference")
    args = parser.parse_args()
    tmp = Path(tempfile.mkdtemp())
    failed = False
    for family in upstream.load()["families"]:
        old, new = family["upstream"]["file"], family["file"]
        for style in ("", "-Italic"):
            ours_var = BUILD / new / "fonts" / "variable" / f"{new}{style}[wght].ttf"
            ref_var = Path(args.reference) / new / f"{old}{style}[wght].ttf"
            for inst in TTFont(ours_var)["fvar"].instances:
                loc = inst.coordinates
                ours_path, ref_path = tmp / "ours.ttf", tmp / "ref.ttf"
                instancer.instantiateVariableFont(TTFont(ours_var), loc).save(ours_path)
                instancer.instantiateVariableFont(TTFont(ref_var), loc).save(ref_path)
                problems = shape_problems(TTFont(ours_path), TTFont(ref_path))
                scores = []
                for key, (p, q) in ((";:", (";", ":")), (",.", (",", "."))):
                    a, b = pair(ours_path, p, q), pair(ref_path, p, q)
                    scores.append(f"{p}{q} {a:.2f} (upstream {b:.2f})")
                    if a <= b:
                        problems.append(f"{p} against {q}: {a:.3f}, upstream {b:.3f}")
                    if loc["wght"] == 400 and a < MEDIANS[new][key]:
                        problems.append(f"{p} against {q}: {a:.3f}, below the median {MEDIANS[new][key]}")
                weight = ink(TTFont(ours_path), "comma").area / ink(TTFont(ours_path), "period").area
                scores.append(f"comma {weight:.2f} × period")
                touching = overlaps(ours_path)
                if touching:
                    problems.append("tails touch descenders: " + " ".join(touching))
                print(f"{'FAIL' if problems else 'ok':4} {new}{style} wght {loc['wght']:g}: {', '.join(scores)}")
                for p in problems:
                    print(f"     {p}")
                failed |= bool(problems)
    print("punctuation: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
