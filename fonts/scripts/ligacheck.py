"""Twilight Crystal Mono's optional ligatures (stylistic set 1): Fira Code's, fitted to the font.

Measured on the variable fonts, at every named instance:

1. Fidelity. With ss01 on, a corpus of programming sequences (every one in Fira Code's
   README, arrows and rows of every length, sequences next to letters) is shaped into the same
   glyphs as Fira Code 6.2 shapes it with its own default features. The corpus avoids what
   fonts/ligatures.json deliberately leaves out or adds (0xFF, www, punctuation next to
   capitals, a double hyphen before a letter); those are tested on their own in 4.
2. Grid. Every glyph of the shaped corpus is one cell (632 units) wide: a sequence of n
   characters still takes n cells.
3. Fit. The double hyphen (hyphen_hyphen.liga, drawn in Fira Code as thick as its hyphen) is
   as thick as Twilight Crystal Mono's hyphen, within two units, and centered on the hyphen's center
   (the math axis), within one: the weight and the axis the build matched. Other glyphs keep
   Fira Code's proportions to its hyphen (its arrow lines are a little heavier, up to 5 %). No ligature glyph has ink beyond the Windows clipping box
   (usWinAscent, usWinDescent).
4. Exceptions. With ss01 on, --watch keeps two plain hyphens, 0xFF keeps its x, www its w's,
   and a colon next to a capital stays the colon.

With ss01 off the font shapes exactly as upstream; fonts/scripts/check.py verifies that.

    python fonts/scripts/ligacheck.py
"""
import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "fonts" / "build" / "TwilightCrystalMono" / "fonts" / "variable"
FIRA = ROOT / json.loads((ROOT / "fonts" / "upstream.json").read_text(encoding="utf-8"))["ligatures"]["directory"]
CELL = 632
CORPUS = (
    "++ -- /= && || ||= -> => :: __ == === != =/= !== <= >= <=> /* */ // /// \\n \\\\ << <<< <<= >> >>> "
    ">>= |= ^= ** ?. </ <!-- </> --> /> # ## ### #### ##### ###### - --- ---- ----- ------ = ==== ===== "
    "====== |-|--|---|----|-----|------| <> <~> ?? .. ... =~ !~ := ..< !! ::: =!= =:= <:< ..= ::< #{ #( "
    "#_ #_( #? #: .- ;; ~@ <- #{} |> =>> =<< >=> <=< =>= =<= <$ <$> $> <+ <+> +> <* <*> *> <|> .= #= +++ "
    "*** :>: :<: <||| <|| <| ||> |||> [| |] ~- ~~ %% /\\ \\/ -| _|_ |- ||- :> :< >: <: ::> <:: >:: {| |} "
    "#[ ]# ::= #! #= a->b x=>y i++ i-- [...a] a<=b a>=b a&&b a||b <=====> <--> |=> ==> <== <-- -->> <<-- "
    "~~> -~ ~- if (a !== b && c <= d) { x => x ?? y; } // done"
)
EXCEPTIONS = {"npm test -- --watch": ["hyphen", "hyphen", "w"], "0xFF": ["x"], "www": ["w", "w", "w"],
              "A:b": ["colon"]}


def shaper(path, location=None):
    font = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))
    if location:
        font.set_variations(location)

    def shape(text, features):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, features)
        return [(font.glyph_to_string(i.codepoint), p.x_advance) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]
    return shape


def bounds(glyphs, name):
    pen = BoundsPen(glyphs)
    glyphs[name].draw(pen)
    return pen.bounds


def check(path):
    font = TTFont(path)
    os2 = font["OS/2"]
    new = [g for g in font.getGlyphOrder() if g.endswith((".liga", ".seq", ".spacer", ".center"))]
    fira = shaper(FIRA / "FiraCode-VF.ttf")
    expected = [g for g, _ in fira(CORPUS, {})]
    problems = []
    for instance in font["fvar"].instances:
        loc = instance.coordinates
        label = ", ".join(f"{k} {v:g}" for k, v in loc.items())
        shape = shaper(path, loc)
        got = shape(CORPUS, {"ss01": True})
        if [g for g, _ in got] != expected:
            first = next(i for i, (a, b) in enumerate(zip([g for g, _ in got], expected)) if a != b)
            problems.append(f"{label}: shaped unlike Fira Code from glyph {first}")
        wide = sorted({g for g, adv in got if adv != CELL})
        if wide:
            problems.append(f"{label}: not one cell wide: {', '.join(wide[:6])}")
        if len(got) != len(CORPUS):
            problems.append(f"{label}: {len(got)} glyphs for {len(CORPUS)} characters")
        glyphs = font.getGlyphSet(location=loc)
        h, m = bounds(glyphs, "hyphen"), bounds(glyphs, "hyphen_hyphen.liga")
        if abs((m[3] - m[1]) - (h[3] - h[1])) > 2:
            problems.append(f"{label}: line {m[3] - m[1]:.0f} units thick, hyphen {h[3] - h[1]:.0f}")
        if abs((m[3] + m[1]) / 2 - (h[3] + h[1]) / 2) > 1:
            problems.append(f"{label}: line centered at {(m[3] + m[1]) / 2:.1f}, hyphen at {(h[3] + h[1]) / 2:.1f}")
        clipped = [g for g in new if (b := bounds(glyphs, g)) and (b[3] > os2.usWinAscent or b[1] < -os2.usWinDescent)]
        if clipped:
            problems.append(f"{label}: ink past the clipping box: {', '.join(clipped[:6])}")
        for text, plain in EXCEPTIONS.items():
            names = [g for g, _ in shape(text, {"ss01": True})]
            if not all(p in names for p in plain) or any(g.endswith((".liga", ".seq")) for g in names
                                                         if text != "npm test -- --watch"):
                problems.append(f"{label}: {text!r} shaped {' '.join(names)}")
            if text == "npm test -- --watch" and names[-7:-5] != ["hyphen", "hyphen"]:
                problems.append(f"{label}: --watch shaped {' '.join(names[-8:])}")
    return problems, len(new), len(font["fvar"].instances)


def main():
    failed = False
    for path in sorted(BUILD.glob("*.ttf")):
        problems, count, instances = check(path)
        print(f"{'FAIL' if problems else 'ok':4} {path.name}: {count} ligature glyphs, {instances} instances")
        for p in problems[:10]:
            print(f"     {p}")
        failed |= bool(problems)
    print("ligatures: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
