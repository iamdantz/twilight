"""Texture of Twilight Text beside Twilight Code, and its legibility against the upstream font.

At every named instance of Twilight Text (upright and italic), against Twilight Code at the
same weight and style and the upstream font at the same instance:

1. Gray step. One sentence alternates prose in Text with inline code in Code, both set at the
   same x-height (24 px). The step is the difference between the mean ink of the two kinds of
   segment over their mean: 0 means code reads as the same gray as the prose. It must be at
   most 14 %. Atkinson Hyperlegible Next as it ships is 20 to 25 % darker than Atkinson
   Hyperlegible Mono from ExtraLight to Regular. Each unit of letter-spacing lowers the step by
   about half a point and lengthens text by about half a percent, so the limit trades gray
   against width: 14 % costs about an eighth more line length; no step would cost a quarter.
2. Distinction. The confusable pairs I-l, l-1, I-1, O-0, rn-m and cl-d, at x-heights from 6 to
   8 px: pixel difference of the two strings drawn from the same origin, over the union of
   their ink, at the best of three one-pixel alignments, averaged over five sizes and four
   sub-pixel positions. No pair may fall more than 0.01 below the upstream font.
3. Width. How much longer a paragraph of Spanish, Portuguese and English becomes, reported.

Renders with FreeType through Pillow, unhinted (instances of the variable fonts); small sizes
are drawn eight times larger and averaged down, so a glyph can sit between pixels.

    python fonts/scripts/texture.py /tmp/reference
"""
import argparse
import sys
import tempfile
from pathlib import Path

import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstream  # noqa: E402

ROOT = upstream.ROOT
BUILD = ROOT / "fonts" / "build"
STEP_LIMIT = 0.14
PAIR_SLACK = 0.01
SEGMENTS = [("Ejecuta ", 0), ("npm run build", 1), (" y publica la carpeta ", 0), ("dist/", 1),
            (" cuando el estado sea ", 0), ("ok", 1), (".", 0)]
PAIRS = [("I", "l"), ("l", "1"), ("I", "1"), ("O", "0"), ("rn", "m"), ("cl", "d")]
SIZES = (6, 6.5, 7, 7.5, 8)
PHASES = (0, 0.25, 0.5, 0.75)
OVERSAMPLE = 8
PARAGRAPH = ("Calm by design, legible by proof. A interface lê-se de relance; o código, linha a "
             "linha. La interfaz se lee de un vistazo y el código, línea por línea.")


def x_height(path):
    font = TTFont(path)
    return font["OS/2"].sxHeight / font["head"].unitsPerEm


def face(path, xh):
    return ImageFont.truetype(str(path), xh / x_height(path))


def gray_step(sans, mono, xh=24):
    fs, fm = face(sans, xh), face(mono, xh)
    image = Image.new("L", (3600, 120), 0)
    draw = ImageDraw.Draw(image)
    x, spans = 20.0, []
    for text, is_code in SEGMENTS:
        font = fm if is_code else fs
        width = draw.textlength(text, font=font)
        draw.text((x, 90), text, font=font, fill=255, anchor="ls")
        spans.append((int(x), int(x + width), is_code))
        x += width
    ink = np.asarray(image, float)[90 - xh:90] / 255

    def mean(flag):
        return np.concatenate([ink[:, a:b].mean(0) for a, b, f in spans if f == flag and b - a > 2]).mean()
    prose, code = mean(0), mean(1)
    return (prose - code) / ((prose + code) / 2)


def small(path, text, xh, phase):
    """A string at x-height xh px, its pen origin `phase` px past a pixel edge, antialiased by
    drawing at OVERSAMPLE times the size and averaging blocks of pixels."""
    k = OVERSAMPLE
    image = Image.new("L", (160 * k, 40 * k), 0)
    ImageDraw.Draw(image).text((10 * k + round(phase * k), 30 * k), text, font=face(path, xh * k), fill=255,
                               anchor="ls")
    a = np.asarray(image, float) / 255
    return a.reshape(40, k, 160, k).mean((1, 3))


def pair(path, p, q):
    """Pixel difference of two strings drawn from the same origin, over the union of their
    ink, at the best of three one-pixel alignments; mean over sizes and sub-pixel phases."""
    scores = []
    for xh in SIZES:
        for phase in PHASES:
            a, b = small(path, p, xh, phase), small(path, q, xh, phase)
            scores.append(min(np.abs(a - np.roll(b, s, 1)).sum() / max(np.maximum(a, np.roll(b, s, 1)).sum(), 1e-9)
                              for s in (-1, 0, 1)))
    return float(np.mean(scores))


def width(path):
    font = ImageFont.truetype(str(path), 100)
    return ImageDraw.Draw(Image.new("L", (1, 1))).textlength(PARAGRAPH, font=font)


def instance(variable, location, out):
    instancer.instantiateVariableFont(TTFont(variable), location).save(out)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reference", help="directory written by upstream.py reference")
    args = parser.parse_args()
    families = {f["file"]: f for f in upstream.load()["families"]}
    text, code = families["TwilightText"], families["TwilightCode"]
    tmp = Path(tempfile.mkdtemp())
    failed = False
    for style in ("", "-Italic"):
        ours_var = BUILD / "TwilightText" / "fonts" / "variable" / f"TwilightText{style}[wght].ttf"
        code_var = BUILD / "TwilightCode" / "fonts" / "variable" / f"TwilightCode{style}[wght].ttf"
        ref_var = Path(args.reference) / "TwilightText" / f"{text['upstream']['file']}{style}[wght].ttf"
        for inst in TTFont(ours_var)["fvar"].instances:
            loc = inst.coordinates
            label = f"TwilightText{style} wght {loc['wght']:g}"
            ours = instance(ours_var, loc, tmp / "ours.ttf")
            mono = instance(code_var, loc, tmp / "code.ttf")
            ref = instance(ref_var, loc, tmp / "ref.ttf")
            step, step_ref = gray_step(ours, mono), gray_step(ref, mono)
            problems = []
            if abs(step) > STEP_LIMIT:
                problems.append(f"gray step {step:+.1%}, limit {STEP_LIMIT:.0%}")
            pairs = []
            for p, q in PAIRS:
                a, b = pair(ours, p, q), pair(ref, p, q)
                pairs.append(f"{p}-{q} {a:.2f}" + (f" (upstream {b:.2f})" if abs(a - b) >= 0.02 else ""))
                if a < b - PAIR_SLACK:
                    problems.append(f"{p}-{q} {a:.3f}, upstream {b:.3f}")
            grow = width(ours) / width(ref) - 1
            print(f"{'FAIL' if problems else 'ok':4} {label}: gray step {step:+.1%} (upstream {step_ref:+.1%}), "
                  f"paragraph {grow:+.1%}; {', '.join(pairs)}")
            for p in problems:
                print(f"     {p}")
            failed |= bool(problems)
    print("texture: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
