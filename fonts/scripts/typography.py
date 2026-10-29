"""Typography measurements: the numbers docs/construction/typography.md derives the type system from.

Every value here is measured on the built fonts (fonts/build, from build.py) or computed from the
decided parameters below, which docs/construction/typography.md §8 lists with their sources. The
text corpus is the Universal Declaration of Human Rights in English and Spanish, from the NLTK
data repository, pinned by SHA-256 and downloaded on first use.

    python fonts/scripts/typography.py            print the report
    python fonts/scripts/typography.py --json     the same numbers as JSON

1. Font facts. x-height, cap height and the natural line (ascender to descender) of both
   families; the tallest and deepest letters, whose distance is the line height at which two
   lines of text cannot touch; tabular figures.
2. Viewing geometry. The x-height, in each geometry's unit, that subtends a given visual angle: a
   CSS pixel on a desktop screen (the CSS reference pixel) and on a handheld one, a point in print,
   and a percentage of the slide height for slides seen from the back of a room.
3. Running text. Per geometry, the smallest size whose x-height subtends the critical print size,
   never below the browser default on screens.
4. Floors. Per weight, the smallest whole pixel size at which the lowercase stems and the
   narrowest counters (the white inside e, a, s, B, g, 8, m, n, H) are each at least one pixel,
   so no stroke or counter falls below the pixel grid of a 1x screen. Pair distinction (the
   metric of hintcheck.py) is reported from each floor to 20 px. Where there are no pixels
   (print, slides), the floor is the angle the Regular floor subtends on a desktop screen.
5. Scale. Per geometry, the ratio that places step -2 on the floor, with step 0 on running text;
   the steps from -2 to 7, and on screens the smallest difference in x-height between adjacent
   steps, in device pixels.
6. Upper bounds. The size whose x-height reaches the top of the fluent range; the largest size at
   which the widest word of the corpus, in Bold, fits a 320 px viewport.
7. Measure. The mean advance of a character of running text, per language, and the width in em
   and in ch that holds 80 of them.
"""
import argparse
import hashlib
import io
import json
import math
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

import freetype
import numpy as np
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hintcheck  # noqa: E402
import upstream  # noqa: E402

ROOT = upstream.ROOT
BUILD = ROOT / "fonts" / "build"
FAMILIES = {"Twilight Crystal": "TwilightCrystal", "Twilight Crystal Mono": "TwilightCrystalMono"}
WEIGHTS = list(hintcheck.WEIGHTS)

# Decided parameters (docs/construction/typography.md §8) -----------------------------------
CRITICAL_PRINT_SIZE = 0.2      # degrees of x-height; Legge and Bigelow 2011
FLUENT_TOP = 2.0               # degrees of x-height; the same source
REFERENCE_PIXEL = math.degrees(math.atan((1 / 96) / 28))  # CSS Values 4: 96 dpi at 28 inches
HANDHELD_PIXEL = math.degrees(math.atan((25.4 / 160) / 320))  # 1/160 inch at 32 cm
PRINT_DISTANCE = 400           # mm; the distance print sizes are measured at
DEFAULT_SIZE = 16              # px; the browsers' default font size, 1rem
HANDHELD_DPR = 2               # device pixels per CSS pixel, at least, on handheld screens
NARROWEST = 320                # CSS px; WCAG 1.4.10 Reflow
GUTTER = 16                    # CSS px, each side
MEASURE_CHARACTERS = 80        # WCAG 1.4.8
STEPS = range(-2, 8)
SLIDE_DISTANCE = 6             # image heights from the farthest viewer; basic viewing in the 4/6/8 rule


def angle(tan_value):
    return math.degrees(math.atan(tan_value))


def up(value, grain):
    """Round up to the grain of the unit."""
    return round(math.ceil(value / grain - 1e-9) * grain, 6)


# x-height, in each geometry's unit, that subtends a given angle in degrees
GEOMETRIES = {
    "desktop": {"unit": "px", "grain": 1, "default": DEFAULT_SIZE, "pixels": True, "dpr": 1,
                "x": lambda a: math.tan(math.radians(a)) / math.tan(math.radians(REFERENCE_PIXEL))},
    "handheld": {"unit": "px", "grain": 1, "default": DEFAULT_SIZE, "pixels": True, "dpr": HANDHELD_DPR,
                 "x": lambda a: math.tan(math.radians(a)) / math.tan(math.radians(HANDHELD_PIXEL))},
    "print": {"unit": "pt", "grain": 0.1,
              "x": lambda a: PRINT_DISTANCE * math.tan(math.radians(a)) / 25.4 * 72},
    "slides": {"unit": "% of slide height", "grain": 0.01,
               "x": lambda a: SLIDE_DISTANCE * math.tan(math.radians(a)) * 100},
}

CORPUS_URL = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/udhr.zip"
CORPUS_SHA256 = "97e4c9dfa4a402f243d60b03d511afb04cf63f92f9ad1be9108b511448c329fa"
CORPUS_FILES = {"English": "udhr/English-Latin1", "Spanish": "udhr/Spanish-Latin1"}
CACHE = Path.home() / ".cache" / "twilight" / "udhr.zip"

RASTER = 2000                  # ppem for outline measurements
COUNTERS_V = "easBg8"          # white measured on the vertical center line
COUNTERS_H = "mnH"             # white measured on a row at a quarter of the em


def static(family, weight):
    return BUILD / family / "fonts" / "ttf" / f"{family}-{weight}.ttf"


def corpus():
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_bytes(urllib.request.urlopen(CORPUS_URL).read())
    data = CACHE.read_bytes()
    if hashlib.sha256(data).hexdigest() != CORPUS_SHA256:
        sys.exit(f"{CACHE}: SHA-256 does not match the pinned corpus")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        return {lang: " ".join(z.read(name).decode("latin-1").split()) for lang, name in CORPUS_FILES.items()}


def shaper(path):
    font = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))

    def advance(text, features=None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, features or {})
        return [p.x_advance for p in buf.glyph_positions]
    return advance


# 1. Font facts --------------------------------------------------------------------------------
def facts(family):
    font = TTFont(static(family, "Regular"))
    upm, os2, hhea = font["head"].unitsPerEm, font["OS/2"], font["hhea"]
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    top, bottom = (0, ""), (0, "")
    for cp, name in cmap.items():
        if not chr(cp).isalpha():
            continue
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        if pen.bounds:
            top = max(top, (pen.bounds[3], chr(cp)))
            bottom = min(bottom, (pen.bounds[1], chr(cp)))
    advance = shaper(static(family, "Regular"))
    tabular = set(advance("0123456789", {"tnum": True}))
    return {"x-height": os2.sxHeight / upm, "cap height": os2.sCapHeight / upm,
            "natural line": (hhea.ascent - hhea.descent + hhea.lineGap) / upm,
            "tallest letter": [top[1], top[0] / upm], "deepest letter": [bottom[1], bottom[0] / upm],
            "touching line height": (top[0] - bottom[0]) / upm,
            "figures": {"proportional": sorted({a / upm for a in advance("0123456789")}),
                        "tabular": sorted(a / upm for a in tabular)},
            "zero": advance("0")[0] / upm}


# 4. Floors ------------------------------------------------------------------------------------
def raster(face, ch):
    face.load_char(ch, freetype.FT_LOAD_NO_HINTING | freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO)
    bm = face.glyph.bitmap
    bits = np.unpackbits(np.array(bm.buffer, np.uint8).reshape(bm.rows, bm.pitch), axis=1)[:, :bm.width]
    return bits.astype(int), face.glyph.bitmap_top


def runs(line, value):
    """Lengths of the runs of `value` in a line, inside its first and last ink."""
    ink = np.flatnonzero(line)
    seg = np.concatenate([[1 - value], line[ink[0]:ink[-1] + 1], [1 - value]])
    d = np.diff((seg == value).astype(int))
    return list(np.flatnonzero(d == -1) - np.flatnonzero(d == 1))


def strokes(family, weight):
    face = freetype.Face(str(static(family, weight)))
    face.set_pixel_sizes(0, RASTER)
    quarter = int(0.25 * RASTER)
    stems, counters = {}, {}
    for ch in "nl":
        bits, top = raster(face, ch)
        stems[ch] = min(runs(bits[top - quarter], 1)) / RASTER
    for ch in COUNTERS_V:
        bits, _ = raster(face, ch)
        counters[ch] = min(runs(bits[:, bits.shape[1] // 2], 0)) / RASTER
    for ch in COUNTERS_H:
        bits, top = raster(face, ch)
        counters[ch] = min(runs(bits[top - quarter], 0)) / RASTER
    stem = min(stems.values())
    narrowest = min(counters, key=counters.get)
    return {"stem": stem, "counter": counters[narrowest], "counter glyph": narrowest,
            "floor": math.ceil(1 / min(stem, counters[narrowest]))}


def distinction(family, weight, sizes):
    face = freetype.Face(str(static(family, weight)))
    worst = 1.0
    for ppem in sizes:
        for flag in (hintcheck.HINTED, hintcheck.UNHINTED):
            for p, q in hintcheck.PAIRS:
                a, b = hintcheck.render(face, p, flag, ppem), hintcheck.render(face, q, flag, ppem)
                worst = min(worst, min(np.abs(a - np.roll(b, s, 1)).sum() / max(np.maximum(a, np.roll(b, s, 1)).sum(), 1e-9)
                                       for s in (-1, 0, 1)))
    return worst


# Report ---------------------------------------------------------------------------------------
def measure():
    out = {"decided": {"critical print size (deg)": CRITICAL_PRINT_SIZE, "fluent range top (deg)": FLUENT_TOP,
                       "desktop pixel (deg)": REFERENCE_PIXEL, "handheld pixel (deg)": HANDHELD_PIXEL,
                       "print distance (mm)": PRINT_DISTANCE, "default size (px)": DEFAULT_SIZE,
                       "handheld device pixels per px": HANDHELD_DPR, "narrowest viewport (px)": NARROWEST,
                       "slide viewing distance (image heights)": SLIDE_DISTANCE,
                       "gutter (px)": GUTTER, "measure (characters)": MEASURE_CHARACTERS}}
    out["facts"] = {name: facts(fam) for name, fam in FAMILIES.items()}
    xh = out["facts"]["Twilight Crystal"]["x-height"]

    # 2-5. Running text, floor and scale per geometry
    floors = {}
    for name, fam in FAMILIES.items():
        floors[name] = {}
        for w in WEIGHTS:
            s = strokes(fam, w)
            s["distinction, floor to 20 px"] = distinction(fam, w, range(s["floor"], 21))
            floors[name][w] = s
    out["floors"] = floors
    pixel_floor = max(floors[n]["Regular"]["floor"] for n in FAMILIES)
    floor_angle = angle(pixel_floor * xh * math.tan(math.radians(REFERENCE_PIXEL)))
    out["floor angle (deg)"] = floor_angle

    geometries = {}
    for geometry, g in GEOMETRIES.items():
        least = up(g["x"](CRITICAL_PRINT_SIZE) / xh, g["grain"])
        body = max(least, g.get("default", 0))
        floor = max(pixel_floor if g.get("pixels") else 0, up(g["x"](floor_angle) / xh, g["grain"]))
        ratio = math.sqrt(body / floor)
        sizes = {k: body * ratio ** k for k in STEPS}
        entry = {"unit": g["unit"], "least running text": least, "running text": body,
                 "x-height angle of running text (deg)": angle(body * xh / g["x"](1) * math.tan(math.radians(1))),
                 "floor": floor, "ratio": ratio, "steps": sizes}
        if "dpr" in g:
            entry["least x-height step (device px)"] = min((sizes[k + 1] - sizes[k]) * xh * g["dpr"] for k in list(STEPS)[:-1])
        geometries[geometry] = entry
    out["geometries"] = geometries

    # 6. Upper bounds
    text = corpus()
    bold = shaper(static("TwilightCrystal", "Bold"))
    widest = max(((sum(bold(w)) / 1000, w) for lang in text for w in re.findall(r"[^\W\d_]+", text[lang])))
    top_px = math.tan(math.radians(FLUENT_TOP)) / math.tan(math.radians(REFERENCE_PIXEL)) / xh
    out["upper bounds"] = {"fluent top, desktop (px)": top_px, "widest word": widest[1], "widest word (em)": widest[0],
                           f"largest size that fits {NARROWEST} px (px)": (NARROWEST - 2 * GUTTER) / widest[0],
                           "fits width W at size": f"(W - {2 * GUTTER}px) / {widest[0]:.2f}"}

    # 7. Measure
    regular = shaper(static("TwilightCrystal", "Regular"))
    zero = out["facts"]["Twilight Crystal"]["zero"]
    measure_ = {lang: sum(regular(t)) / len(t) / 1000 for lang, t in text.items()}
    narrow = min(measure_.values())
    out["measure"] = {"mean character (em)": measure_, f"{MEASURE_CHARACTERS} characters (em)": MEASURE_CHARACTERS * narrow,
                      f"{MEASURE_CHARACTERS} characters (ch)": MEASURE_CHARACTERS * narrow / zero,
                      f"characters at {NARROWEST} px, handheld": {
                          lang: (NARROWEST - 2 * GUTTER) / (m * geometries["handheld"]["running text"]) for lang, m in measure_.items()}}
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    out = measure()
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False, default=float))
        return
    r = lambda v, n=3: round(float(v), n)  # noqa: E731
    print("Decided:", {k: r(v, 5) for k, v in out["decided"].items()})
    for name, f in out["facts"].items():
        print(f"\n{name}: x-height {f['x-height']}, cap height {f['cap height']}, natural line {f['natural line']}, "
              f"lines touch below {r(f['touching line height'])} ({f['tallest letter'][0]} over {f['deepest letter'][0]}), "
              f"tabular figures {f['figures']['tabular']}, zero {f['zero']}")
    print("\nFloors (stem, narrowest counter, floor px, worst pair distinction from the floor to 20 px):")
    for name, ws in out["floors"].items():
        for w, s in ws.items():
            print(f"  {name} {w}: stem {r(s['stem'])} em, counter {r(s['counter'])} em ({s['counter glyph']}), "
                  f"floor {s['floor']} px, distinction {r(s['distinction, floor to 20 px'], 2)}")
    print(f"\nFloor angle (x-height of the Regular floor on a desktop screen): {r(out['floor angle (deg)'], 4)} deg")
    print("\nGeometries:")
    for g, s in out["geometries"].items():
        extra = f", least x-height step {r(s['least x-height step (device px)'], 2)} device px" if "least x-height step (device px)" in s else ""
        print(f"  {g} ({s['unit']}): running text {r(s['running text'], 2)} (least {r(s['least running text'], 2)}, "
              f"x-height {r(s['x-height angle of running text (deg)'])} deg), floor {r(s['floor'], 2)}, ratio {r(s['ratio'], 4)}{extra}")
        print("    " + "  ".join(f"{k}: {r(v, 2)}" for k, v in s["steps"].items()))
    print("\nUpper bounds:", {k: (r(v, 2) if isinstance(v, float) else v) for k, v in out["upper bounds"].items()})
    m = out["measure"]
    print("\nMeasure:", {k: (r(v) if isinstance(v, float) else {a: r(b, 2) for a, b in v.items()}) for k, v in m.items()})


if __name__ == "__main__":
    main()
