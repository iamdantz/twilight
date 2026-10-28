"""Compare the built Twilight fonts with the upstream fonts they derive from.

Every change made to Twilight Text and Twilight Code is meant to be deliberate. This check
lists everything that differs between a built variable font and its upstream counterpart, at
every named instance, so an unintended difference cannot pass unnoticed:

- glyph set, character map, axes, named instances, axis mapping and STAT values;
- vertical metrics;
- per glyph: advance width exactly; outline with the same commands and points, each point
  within 0.5 font units. A variable font stores the other masters as deltas, and every build
  drops the deltas that interpolation recovers within 0.5 units (the IUP optimization of
  fontTools); two builds of the same source can differ by up to that much, and no more;
- shaping of every mapped character and of a kerning sample, with the default features and
  with each optional feature on: glyphs, advances and offsets, exactly.

Changes made on purpose are declared in fonts/changes.json, per font file: "added" lists the
code point ranges of new characters (their glyphs join the glyph set and character map, and
nothing else may), "differences" lists the reported differences that are expected, by prefix.
Anything else fails.

    python fonts/scripts/upstream.py reference /tmp/reference
    python fonts/scripts/check.py /tmp/reference
"""
import argparse
import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstream  # noqa: E402

ROOT = upstream.ROOT
BUILD = ROOT / "fonts" / "build"
CHANGES = ROOT / "fonts" / "changes.json"
SAMPLE = ("AVATAR Tokyo LTV Wave yoyo P. F. T, r. y. f) \"A\" Ta Te To Ty Va Vo Wa Ya Yo "
          "Il1| O0o rn m cl d ç ñ ã õ ÁÉÍÓÚ áéíóú ¿¡ 0123456789 1/2 -> => != == <= >=")
VERTICAL = {"hhea": ["ascent", "descent", "lineGap"],
            "OS/2": ["sTypoAscender", "sTypoDescender", "sTypoLineGap", "usWinAscent", "usWinDescent",
                     "sxHeight", "sCapHeight", "fsSelection"],
            "head": ["unitsPerEm"]}


def features(font):
    tags = set()
    for table in ("GSUB", "GPOS"):
        if table in font:
            tags |= {r.FeatureTag for r in font[table].table.FeatureList.FeatureRecord}
    return sorted(tags)


TOLERANCE = 0.5


def outlines(font):
    glyphs = font.getGlyphSet()
    hmtx = font["hmtx"].metrics
    result = {}
    for name in font.getGlyphOrder():
        pen = DecomposingRecordingPen(glyphs)
        glyphs[name].draw(pen)
        result[name] = (hmtx[name][0], pen.value)
    return result


def deviation(a, b):
    """Largest point distance between two outlines, or None when their commands differ."""
    if [op for op, _ in a] != [op for op, _ in b] or any(len(p) != len(q) for (_, p), (_, q) in zip(a, b)):
        return None
    return max((max(abs(x1 - x2), abs(y1 - y2)) for (_, p), (_, q) in zip(a, b)
                for (x1, y1), (x2, y2) in zip(p, q)), default=0.0)


def shape(path, location, text, feats):
    face = hb.Face(hb.Blob.from_file_path(str(path)))
    font = hb.Font(face)
    font.set_variations(location)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, feats)
    names = [font.glyph_to_string(i.codepoint) for i in buf.glyph_infos]
    pos = [(p.x_advance, p.x_offset, p.y_offset) for p in buf.glyph_positions]
    return list(zip(names, pos))


def codepoints(ranges):
    result = set()
    for r in ranges:
        lo, _, hi = r.partition("-")
        result |= set(range(int(lo, 16), int(hi or lo, 16) + 1))
    return result


def compare(ours_path, ref_path, added=frozenset()):
    ours, ref = TTFont(ours_path), TTFont(ref_path)
    found = []
    worst = 0.0

    def diff(key, a, b):
        if a != b:
            found.append(key)

    cmap, ref_cmap = ours.getBestCmap(), ref.getBestCmap()
    new = {cp: g for cp, g in cmap.items() if cp in added and cp not in ref_cmap}
    undeclared = sorted(set(cmap) - set(ref_cmap) - set(new))
    if undeclared:
        found.append("character map adds " + " ".join(f"U+{cp:04X}" for cp in undeclared[:8]))
    diff("character map", {cp: g for cp, g in cmap.items() if cp not in new}, ref_cmap)
    diff("glyph set", [g for g in ours.getGlyphOrder() if g not in set(new.values())], ref.getGlyphOrder())
    diff("features", features(ours), features(ref))
    axes = lambda f: [(a.axisTag, a.minValue, a.defaultValue, a.maxValue) for a in f["fvar"].axes]
    diff("axes", axes(ours), axes(ref))
    named = lambda f: [i.coordinates for i in f["fvar"].instances]
    diff("named instances", named(ours), named(ref))
    avar = lambda f: f["avar"].segments if "avar" in f else None
    diff("axis mapping", avar(ours), avar(ref))
    stat = lambda f: [(v.Format, getattr(v, "Value", None), getattr(v, "LinkedValue", None), v.Flags)
                      for v in f["STAT"].table.AxisValueArray.AxisValue] if "STAT" in f else None
    diff("STAT values", stat(ours), stat(ref))
    for table, fields in VERTICAL.items():
        for field in fields:
            diff(f"{table}.{field}", getattr(ours[table], field), getattr(ref[table], field))

    text = "".join(chr(c) for c in sorted(ref.getBestCmap()) if c > 0x20) + " " + SAMPLE
    optional = [t for t in features(ref) if t not in ("kern", "mark", "mkmk", "ccmp", "locl", "calt", "liga", "rlig")]
    for location in named(ref):
        label = ", ".join(f"{k} {v:g}" for k, v in location.items())
        a = outlines(instancer.instantiateVariableFont(TTFont(ours_path), location))
        b = outlines(instancer.instantiateVariableFont(TTFont(ref_path), location))
        widths = sorted(g for g in b if g in a and a[g][0] != b[g][0])
        shapes = []
        for g in sorted(set(a) & set(b)):
            d = deviation(a[g][1], b[g][1])
            if d is None or d > TOLERANCE:
                shapes.append(g)
            else:
                worst = max(worst, d)
        if widths:
            found.append(f"advance widths at {label}: {', '.join(widths[:8])}{' …' if len(widths) > 8 else ''}")
        if shapes:
            found.append(f"outlines at {label}: {', '.join(shapes[:8])}{' …' if len(shapes) > 8 else ''}")
        for feats in [{}] + [{t: True} for t in optional]:
            if shape(ours_path, location, text, feats) != shape(ref_path, location, text, feats):
                found.append(f"shaping at {label} with {', '.join(feats) or 'default features'}")
    return found, worst


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reference", help="directory written by upstream.py reference")
    args = parser.parse_args()
    expected = json.loads(CHANGES.read_text(encoding="utf-8")) if CHANGES.exists() else {}
    failed = False
    for family in upstream.load()["families"]:
        old, new = family["upstream"]["file"], family["file"]
        for ref_path in sorted((Path(args.reference) / new).glob("*.ttf")):
            ours_path = BUILD / new / "fonts" / "variable" / ref_path.name.replace(old, new)
            if not ours_path.exists():
                print(f"FAIL {ours_path.relative_to(ROOT)}: not built")
                failed = True
                continue
            declared = expected.get(ours_path.name, {})
            allowed = declared.get("differences", [])
            found, worst = compare(ours_path, ref_path, codepoints(declared.get("added", [])))
            unexpected = [f for f in found if not any(f.startswith(a) for a in allowed)]
            status = "FAIL" if unexpected else "ok"
            print(f"{status:4} {ours_path.name} against {ref_path.name}: "
                  f"{len(codepoints(declared.get('added', [])))} added characters, {len(found) - len(unexpected)} expected, {len(unexpected)} unexpected differences, "
                  f"largest point shift {worst:.2f} units")
            for line in unexpected:
                print(f"     {line}")
            failed |= bool(unexpected)
    print("fonts against upstream: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
