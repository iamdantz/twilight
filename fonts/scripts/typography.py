"""Typography measurements: the numbers docs/construction/typography.md derives the type system from.

Every value here is measured on the built fonts (fonts/build, from build.py) or computed from the
decided parameters below, which docs/construction/typography.md §8 lists with their sources. The
text corpus is the Universal Declaration of Human Rights in English and Spanish, from the NLTK
data repository, pinned by SHA-256 and downloaded on first use.

    python fonts/scripts/typography.py            print the report
    python fonts/scripts/typography.py --json     the same numbers as JSON
    python fonts/scripts/typography.py --write    write typography/twilight.json
    python fonts/scripts/typography.py --check    fail if typography/twilight.json differs

1. Font facts. x-height, cap height and the natural line (ascender to descender) of both
   families; the tallest and deepest letters, whose distance is the line height at which two
   lines of text cannot touch; tabular figures.
2. Viewing geometry. The x-height, in each geometry's unit, that subtends a given visual angle: a
   CSS pixel on a desktop screen (the CSS reference pixel) and on a handheld one, a point on a page
   read at 40 cm, and a percentage of the slide height for slides seen from the back of a room.
3. Body text. Per geometry, the smallest size whose x-height subtends the critical print size,
   never below the browser default on screens. Pages take the decided size of 12 pt; their
   x-height angle on paper and on a desktop screen at 100 % zoom is reported.
4. Floors. Per weight, the smallest whole pixel size at which the lowercase stems and the
   narrowest counters (the white inside e, a, s, B, g, 8, m, n, H) are each at least one pixel,
   so no stroke or counter falls below the pixel grid of a 1x screen. Pair distinction (the
   metric of hintcheck.py) is reported from each floor to 20 px. Where there are no pixels
   (slides), the floor is the angle the Regular floor subtends on a desktop screen; pages, read
   on screens at 100 % zoom, take the pixel floor in points. Italic glyphs are uprighted by their
   angle before their counters are measured. Each style's lowest step is the smallest step at or
   above its floor in every geometry.
5. Scale. Per geometry, the ratio that places step -2 on the floor, with step 0 on body text;
   the steps from -2 to 7, and on screens the smallest difference in x-height between adjacent
   steps, in device pixels.
6. Upper bounds. The size whose x-height reaches the top of the fluent range; the largest size at
   which the widest word of the corpus, in Bold, fits a 320 px viewport.
7. Measure. The mean advance of a character of body text, per language, and the width in em
   and in ch that holds 80 of them.
8. Code. The size of code in editors and terminals. Minimum: the smallest size from the floor whose
   x-height, cell and line all land within 2 % of whole pixels. Optimal: at least the x-height of
   the default editor font and size on every system, then the size, up to desktop body text,
   whose x-height, cell and line land closest to whole pixels.

With --write, the measurements and the rules below become typography/twilight.json, the
typography tokens; --check reports whether that file matches the fonts and rules.
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
STYLES = WEIGHTS + [("Italic" if w == "Regular" else w + "Italic") for w in WEIGHTS]

# Decided parameters (docs/construction/typography.md §8) -----------------------------------
CRITICAL_PRINT_SIZE = 0.2      # degrees of x-height; Legge and Bigelow 2011
FLUENT_TOP = 2.0               # degrees of x-height; the same source
REFERENCE_PIXEL = math.degrees(math.atan((1 / 96) / 28))  # CSS Values 4: 96 dpi at 28 inches
HANDHELD_PIXEL = math.degrees(math.atan((25.4 / 160) / 320))  # 1/160 inch at 32 cm
PRINT_DISTANCE = 400           # mm; the distance print sizes are measured at
PAGE_SIZE = 12                 # pt; body text on pages, the size APA Style gives Aptos and Times New Roman
PX_PER_PT = 4 / 3              # a document at 100 % zoom
# The default font and size of the most used code editor on each system, and that font's x-height,
# measured on the font as the system installs it (the files are not distributed).
EDITOR_DEFAULTS = {"Windows": ("Consolas", 14, 0.4902), "macOS": ("Menlo", 12, 0.5469),
                   "Linux": ("Droid Sans Mono", 14, 0.5361)}
GRID_TOLERANCE = 0.02          # code: x-height, cell and line within 2 % of whole pixels
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
    "desktop": {"unit": "px", "grain": 1, "default": DEFAULT_SIZE, "pixels": 1, "dpr": 1,
                "x": lambda a: math.tan(math.radians(a)) / math.tan(math.radians(REFERENCE_PIXEL))},
    "handheld": {"unit": "px", "grain": 1, "default": DEFAULT_SIZE, "pixels": 1, "dpr": HANDHELD_DPR,
                 "x": lambda a: math.tan(math.radians(a)) / math.tan(math.radians(HANDHELD_PIXEL))},
    "page": {"unit": "pt", "grain": 0.5, "body": PAGE_SIZE, "pixels": PX_PER_PT,
                  "x": lambda a: PRINT_DISTANCE * math.tan(math.radians(a)) / 25.4 * 72},
    "slide": {"unit": "% of slide height", "grain": 0.01,
               "x": lambda a: SLIDE_DISTANCE * math.tan(math.radians(a)) * 100},
}

CORPUS_URL = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/udhr.zip"
CORPUS_SHA256 = "97e4c9dfa4a402f243d60b03d511afb04cf63f92f9ad1be9108b511448c329fa"
CORPUS_FILES = {"English": "udhr/English-Latin1", "Spanish": "udhr/Spanish-Latin1"}
CACHE = Path.home() / ".cache" / "twilight" / "udhr.zip"

RASTER = 2000                  # ppem for outline measurements
COUNTERS_V = "easBg8"          # white measured on the vertical center line
COUNTERS_H = "mnH"             # white measured on a row at a quarter of the em


# Rules (docs/design-system/typography.md) -------------------------------------------------------
# One vocabulary for tokens, CSS and the documents: fonts sans and mono; scale steps xs to 6xl; levels named
# after their HTML element or their step (body-lg is body text at lg); leading default and tight.
TOKENS = ROOT / "typography" / "twilight.json"
SCALE = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl"]   # steps -2 to 7
STEP = dict(zip(range(-2, 8), SCALE))
LEADING = {"default": 1.5, "tight": 1.3}   # WCAG 1.4.8; the fonts' natural line
FONT_KEYS = {"sans": "Twilight Crystal", "mono": "Twilight Crystal Mono"}
ORIGINALS = {"sans": "Atkinson Hyperlegible Next", "mono": "Atkinson Hyperlegible Mono"}
# key: (use, step, weight, leading, font); Display takes any weight at or above its lowest step
LEVELS = {
    "display-1": ("The one title of a page, a cover or a slide", "6xl", 400, "tight", "sans"),
    "display-2": ("The same, one step down", "5xl", 400, "tight", "sans"),
    "h1": ("Headings, by structure", "4xl", 700, "tight", "sans"),
    "h2": ("", "3xl", 700, "tight", "sans"),
    "h3": ("", "2xl", 700, "tight", "sans"),
    "h4": ("", "xl", 700, "tight", "sans"),
    "h5": ("", "lg", 700, "tight", "sans"),
    "h6": ("", "base", 700, "tight", "sans"),
    "body-lg": ("The opening paragraph of prose", "lg", 400, "default", "sans"),
    "body": ("Paragraphs, lists, quotes", "base", 400, "default", "sans"),
    "ui": ("Controls, labels, menus, tabs, table cells, messages; default leading when it wraps",
           "base", 400, "tight", "sans"),
    "body-sm": ("Captions, help text, metadata, secondary labels", "sm", 400, "default", "sans"),
    "body-xs": ("Timestamps, counts, badges, notes", "xs", 400, "default", "sans"),
    "code": ("Code blocks in prose, pages and slides", "base", 400, "tight", "mono"),
}
DISPLAY_LEVELS = ("display-1", "display-2")
SPACING = {"block": 1, "list-item": 0, "list-item-with-paragraphs": 0.5, "before-heading": 2,
           "after-heading": 0.5}    # in units of spacing: one line of body text
# Tools that take the scale in their own unit: geometry, factor to the tool's unit, grain
TOOLS = {"Word, Google Docs, Pages, PDFs": ("page", 1, 0.5, "pt"),
         "PowerPoint, 16:9 (7.5 in high)": ("slide", 5.4, 0.5, "pt"),
         "Google Slides, 16:9 (5.625 in high)": ("slide", 4.05, 0.5, "pt"),
         "Keynote, 1920 × 1080": ("slide", 10.8, 1, "pt")}
# System fonts closest to Twilight Crystal (design-system/typography.md §2), measured in an earlier study: the
# size that matches Twilight Crystal's x-height, and the names each face is installed under (full name, then
# PostScript name) for CSS local(). Listed in the order a CSS stack tries them.
FALLBACKS = {
    "sans": {
        "Tahoma": (0.91, {"400 normal": ["Tahoma"], "700 normal": ["Tahoma Bold", "Tahoma-Bold"]}),
        "Verdana": (0.91, {"400 normal": ["Verdana"], "700 normal": ["Verdana Bold", "Verdana-Bold"],
                           "400 italic": ["Verdana Italic", "Verdana-Italic"],
                           "700 italic": ["Verdana Bold Italic", "Verdana-BoldItalic"]}),
        "Adwaita Sans": (0.91, {"400 normal": ["Adwaita Sans Regular", "AdwaitaSans-Regular"],
                                "700 normal": ["Adwaita Sans Bold", "AdwaitaSans-Bold"],
                                "400 italic": ["Adwaita Sans Italic", "AdwaitaSans-Italic"],
                                "700 italic": ["Adwaita Sans Bold Italic", "AdwaitaSans-BoldItalic"]}),
        "Noto Sans": (0.93, {"400 normal": ["Noto Sans Regular", "NotoSans-Regular"],
                             "700 normal": ["Noto Sans Bold", "NotoSans-Bold"],
                             "400 italic": ["Noto Sans Italic", "NotoSans-Italic"],
                             "700 italic": ["Noto Sans Bold Italic", "NotoSans-BoldItalic"]}),
    },
    "mono": {
        "Cascadia Mono": (0.92, {"400 normal": ["Cascadia Mono Regular", "CascadiaMono-Regular"],
                                 "700 normal": ["Cascadia Mono Bold", "CascadiaMono-Bold"],
                                 "400 italic": ["Cascadia Mono Italic", "CascadiaMono-Italic"],
                                 "700 italic": ["Cascadia Mono Bold Italic", "CascadiaMono-BoldItalic"]}),
        "Menlo": (0.91, {"400 normal": ["Menlo Regular", "Menlo-Regular"], "700 normal": ["Menlo Bold", "Menlo-Bold"],
                         "400 italic": ["Menlo Italic", "Menlo-Italic"],
                         "700 italic": ["Menlo Bold Italic", "Menlo-BoldItalic"]}),
        "Hack": (0.91, {"400 normal": ["Hack Regular", "Hack-Regular"], "700 normal": ["Hack Bold", "Hack-Bold"],
                        "400 italic": ["Hack Italic", "Hack-Italic"], "700 italic": ["Hack Bold Italic", "Hack-BoldItalic"]}),
        "Adwaita Mono": (0.95, {"400 normal": ["Adwaita Mono Regular", "AdwaitaMono-Regular"],
                                "700 normal": ["Adwaita Mono Bold", "AdwaitaMono-Bold"],
                                "400 italic": ["Adwaita Mono Italic", "AdwaitaMono-Italic"],
                                "700 italic": ["Adwaita Mono Bold Italic", "AdwaitaMono-BoldItalic"]}),
        "DejaVu Sans Mono": (0.91, {"400 normal": ["DejaVu Sans Mono", "DejaVuSansMono"],
                                    "700 normal": ["DejaVu Sans Mono Bold", "DejaVuSansMono-Bold"],
                                    "400 italic": ["DejaVu Sans Mono Oblique", "DejaVuSansMono-Oblique"],
                                    "700 italic": ["DejaVu Sans Mono Bold Oblique", "DejaVuSansMono-BoldOblique"]}),
    },
}
# System, sans-serif face, monospaced face, monospaced cell after sizing (em)
SYSTEMS = [("Windows", "Tahoma", "Cascadia Mono", 0.54), ("macOS", "Verdana", "Menlo", 0.55),
           ("Linux, KDE", "Noto Sans", "Hack", 0.55), ("Linux, GNOME", "Adwaita Sans", "Adwaita Mono", 0.57),
           ("Linux, other", "Noto Sans if installed", "DejaVu Sans Mono", 0.55)]
STYLE_KEYS = {"Regular": (400, "normal"), "Italic": (400, "italic")}
for _w, _n in zip(("ExtraLight", "Light", "Medium", "SemiBold", "Bold", "ExtraBold"), (200, 300, 500, 600, 700, 800)):
    STYLE_KEYS[_w], STYLE_KEYS[_w + "Italic"] = (_n, "normal"), (_n, "italic")


def version():
    for line in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").splitlines():
        if (m := re.match(r"## (\d+\.\d+\.\d+)", line)):
            return m.group(1)


def tokens(out):
    q = lambda v, n=4: round(float(v), n)  # noqa: E731
    G = out["geometries"]
    geometries = {}
    for name, g in G.items():
        geometries[name] = {"unit": g["unit"], "ratio": q(g["ratio"], 6),
                                   "scale": {STEP[k]: q(v) for k, v in g["steps"].items()}}
    d = out["distance"]
    geometries["distance"] = {"unit": "% of the farthest reading distance", "ratio": q(d["ratio"], 6),
                              "scale": {STEP[k]: q(d["step0"] * d["ratio"] ** k) for k in STEPS}}
    fonts = {}
    for key, name in FONT_KEYS.items():
        f = out["facts"][name]
        fonts[key] = {"family": name, "original": ORIGINALS[key], "x-height": f["x-height"],
                      "cap-height": f["cap height"], "natural-line": f["natural line"],
                      "touching-line": q(f["touching line height"], 3), "tabular-figure": f["figures"]["tabular"][0],
                      "zero": f["zero"],
                      "styles": {s: {"weight": STYLE_KEYS[s][0], "style": STYLE_KEYS[s][1], "stem": q(v["stem"], 3),
                                     "counter": q(v["counter"], 3), "counter-glyph": v["counter glyph"],
                                     "floor": v["floor"], "lowest-step": STEP[v["lowest step"]]}
                                 for s, v in out["floors"][name].items()},
                      "fallbacks": {n: {"size-adjust": size, "faces": faces} for n, (size, faces) in FALLBACKS[key].items()}}
    c, m, u = out["code"], out["measure"], out["upper bounds"]
    return {
        "version": version(),
        "_": "Generated by fonts/scripts/typography.py --write from the built fonts and the rules of "
             "docs/design-system/typography.md; derivations in docs/construction/typography.md. Do not edit by hand.",
        "fonts": fonts,
        "geometries": geometries,
        "levels": {k: {"use": use, "size": s, "weight": w, "leading": lh, "font": fam,
                       **({"weights": "any at or above its lowest step"} if k in DISPLAY_LEVELS else {})}
                   for k, (use, s, w, lh, fam) in LEVELS.items()},
        "editor": {"text": c["minimum (px)"], "text-lg": c["optimal (px)"], "leading": "tight", "font": "mono",
                   "grid-rounding": {str(k): q(v) for k, v in c["worst rounding to whole pixels"].items()},
                   "defaults": {k: {"font": v["font"], "size": v["size (px)"], "x-height": q(v["x-height (px)"], 2)}
                                for k, v in c["editor defaults"].items()}},
        "leading": LEADING,
        "tracking": 0,
        "spacing": SPACING,
        "container": {"prose": {"em": q(m[f"{MEASURE_CHARACTERS} characters (em)"], 1), "characters": MEASURE_CHARACTERS,
                                "mean-character": {k: q(v) for k, v in m["mean character (em)"].items()}}},
        "fit": {"word": u["widest word"], "em": q(u["widest word (em)"], 2), "gutter": GUTTER, "narrowest": NARROWEST},
        "tools": {k: {"geometry": g, "factor": f, "grain": gr, "unit": un} for k, (g, f, gr, un) in TOOLS.items()},
        "systems": [{"system": s, "sans": a, "mono": b, "cell": c} for s, a, b, c in SYSTEMS],
    }

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
    slant = math.tan(math.radians(-TTFont(static(family, weight))["post"].italicAngle))
    for ch in COUNTERS_V:
        bits, top = raster(face, ch)
        if slant:  # upright the glyph, so the center line follows its slant; horizontal runs keep their length
            pad = int(slant * bits.shape[0]) + 1
            upright = np.zeros((bits.shape[0], bits.shape[1] + pad), int)
            for row in range(bits.shape[0]):
                shift = int(round((bits.shape[0] - row) * slant))
                upright[row, pad - shift:pad - shift + bits.shape[1]] = bits[row]
            bits = upright[:, np.flatnonzero(upright.any(0))[0]:np.flatnonzero(upright.any(0))[-1] + 1]
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
                       "print distance (mm)": PRINT_DISTANCE, "page size (pt)": PAGE_SIZE, "default size (px)": DEFAULT_SIZE,
                       "handheld device pixels per px": HANDHELD_DPR, "narrowest viewport (px)": NARROWEST,
                       "slide viewing distance (image heights)": SLIDE_DISTANCE,
                       "gutter (px)": GUTTER, "measure (characters)": MEASURE_CHARACTERS}}
    out["facts"] = {name: facts(fam) for name, fam in FAMILIES.items()}
    xh = out["facts"]["Twilight Crystal"]["x-height"]

    # 2-5. Body text, floor and scale per geometry
    floors = {}
    for name, fam in FAMILIES.items():
        floors[name] = {}
        for w in STYLES:
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
        body = g.get("body", max(least, g.get("default", 0)))
        floor = max(pixel_floor / g["pixels"] if g.get("pixels") else 0, up(g["x"](floor_angle) / xh, g["grain"]))
        ratio = math.sqrt(body / floor)
        sizes = {k: body * ratio ** k for k in STEPS}
        entry = {"unit": g["unit"], "least body text": least, "body text": body,
                 "x-height angle of body text (deg)": angle(body * xh / g["x"](1) * math.tan(math.radians(1))),
                 "floor": floor, "ratio": ratio, "steps": sizes}
        if "dpr" in g:
            entry["least x-height step (device px)"] = min((sizes[k + 1] - sizes[k]) * xh * g["dpr"] for k in list(STEPS)[:-1])
        geometries[geometry] = entry
    out["geometries"] = geometries
    dist = lambda angle_: math.tan(math.radians(angle_)) / xh * 100  # noqa: E731  (% of the distance)
    out["distance"] = {"step0": dist(CRITICAL_PRINT_SIZE), "floor": dist(floor_angle),
                       "ratio": math.sqrt(dist(CRITICAL_PRINT_SIZE) / dist(floor_angle))}
    docs = geometries["page"]
    docs["x-height angle on a desktop screen at 100 % (deg)"] = angle(
        docs["body text"] * PX_PER_PT * xh * math.tan(math.radians(REFERENCE_PIXEL)))
    docs["zoom for the critical print size on a desktop screen"] = geometries["desktop"]["least body text"] / (
        docs["body text"] * PX_PER_PT)

    # Code in editors and terminals: at least the x-height of each system's default editor, then the
    # size up to body text whose x-height, cell and line (1.3) land closest to whole pixels.
    mono = out["facts"]["Twilight Crystal Mono"]
    cell = 0.632
    comfort = max(size * x for _, size, x in EDITOR_DEFAULTS.values()) / mono["x-height"]
    grid = {}
    for size in range(pixel_floor, int(geometries["desktop"]["body text"]) + 1):
        worst = max(abs(round(v) - v) / v for v in (size * mono["x-height"], size * cell, size * mono["natural line"]))
        grid[size] = worst
    optimal = min((s for s in grid if s >= comfort), key=lambda s: (grid[s], s))
    minimum = min(s for s in grid if grid[s] < GRID_TOLERANCE)
    out["code"] = {"editor defaults": {k: {"font": f, "size (px)": s, "x-height (px)": s * x}
                                       for k, (f, s, x) in EDITOR_DEFAULTS.items()},
                   "comfort bound (px)": comfort, "worst rounding to whole pixels": grid,
                   "minimum (px)": minimum, "optimal (px)": optimal}

    # The lowest step each style may take in every geometry: on screens its pixel floor, elsewhere
    # the geometry's floor scaled by the style's pixel floor over Regular's.
    for name in FAMILIES:
        for style, s in floors[name].items():
            s["lowest step"] = max(min(k for k, v in g["steps"].items()
                                       if v >= (s["floor"] / GEOMETRIES[geo]["pixels"] if GEOMETRIES[geo].get("pixels")
                                                else g["floor"] * s["floor"] / pixel_floor) - 1e-9)
                                   for geo, g in geometries.items())

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
                          lang: (NARROWEST - 2 * GUTTER) / (m * geometries["handheld"]["body text"]) for lang, m in measure_.items()}}
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    out = measure()
    if args.write or args.check:
        text = json.dumps(tokens(out), indent=2, ensure_ascii=False) + "\n"
        if args.write:
            TOKENS.parent.mkdir(exist_ok=True)
            TOKENS.write_text(text, encoding="utf-8")
            print(f"wrote {TOKENS.relative_to(ROOT)}")
        elif not TOKENS.exists() or TOKENS.read_text(encoding="utf-8") != text:
            sys.exit(f"{TOKENS.relative_to(ROOT)} does not match the fonts and rules: run typography.py --write")
        else:
            print(f"{TOKENS.relative_to(ROOT)} matches the fonts and rules")
        return
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False, default=float))
        return
    r = lambda v, n=3: round(float(v), n)  # noqa: E731
    print("Decided:", {k: r(v, 5) for k, v in out["decided"].items()})
    for name, f in out["facts"].items():
        print(f"\n{name}: x-height {f['x-height']}, cap height {f['cap height']}, natural line {f['natural line']}, "
              f"lines touch below {r(f['touching line height'])} ({f['tallest letter'][0]} over {f['deepest letter'][0]}), "
              f"tabular figures {f['figures']['tabular']}, zero {f['zero']}")
    print("\nFloors (stem, narrowest counter, floor px, lowest step in every geometry, worst pair distinction from the floor to 20 px):")
    for name, ws in out["floors"].items():
        for w, s in ws.items():
            print(f"  {name} {w}: stem {r(s['stem'])} em, counter {r(s['counter'])} em ({s['counter glyph']}), "
                  f"floor {s['floor']} px, lowest step {s['lowest step']}, distinction {r(s['distinction, floor to 20 px'], 2)}")
    print(f"\nFloor angle (x-height of the Regular floor on a desktop screen): {r(out['floor angle (deg)'], 4)} deg")
    print("\nGeometries:")
    for g, s in out["geometries"].items():
        extra = f", least x-height step {r(s['least x-height step (device px)'], 2)} device px" if "least x-height step (device px)" in s else ""
        print(f"  {g} ({s['unit']}): body text {r(s['body text'], 2)} (least {r(s['least body text'], 2)}, "
              f"x-height {r(s['x-height angle of body text (deg)'])} deg), floor {r(s['floor'], 2)}, ratio {r(s['ratio'], 4)}{extra}")
        print("    " + "  ".join(f"{STEP[k]}: {r(v, 2)}" for k, v in s["steps"].items()))
    d = out["geometries"]["page"]
    print(f"\nPage: x-height {r(d['x-height angle of body text (deg)'])} deg on paper, "
          f"{r(d['x-height angle on a desktop screen at 100 % (deg)'])} deg on a desktop screen at 100 %; "
          f"zoom {r(d['zoom for the critical print size on a desktop screen'], 3)} reaches the critical print size")
    c = out["code"]
    print(f"\nEditor: comfort bound {r(c['comfort bound (px)'], 2)} px; worst rounding "
          + ", ".join(f"{k}: {r(v * 100, 1)} %" for k, v in c["worst rounding to whole pixels"].items())
          + f"; editor {c['minimum (px)']} px, editor-lg {c['optimal (px)']} px")
    print("\nUpper bounds:", {k: (r(v, 2) if isinstance(v, float) else v) for k, v in out["upper bounds"].items()})
    m = out["measure"]
    print("\nMeasure:", {k: (r(v) if isinstance(v, float) else {a: r(b, 2) for a, b in v.items()}) for k, v in m.items()})


if __name__ == "__main__":
    main()
