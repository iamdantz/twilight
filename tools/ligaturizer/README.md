# Ligaturizer

Adds [Fira Code](https://github.com/tonsky/FiraCode)'s programming ligatures to a monospaced
font. A modernized fork of [Ligaturizer](https://github.com/ToxicFrog/Ligaturizer), originally
written by Ilya Skriblovsky for dv-code-font and generalized by Navid Rojiani, ToxicFrog and its
contributors. Twilight Theme uses it to build the optional ligatures of Twilight Crystal Mono.

## What changed from Ligaturizer

| | Ligaturizer | This fork |
|---|---|---|
| Engine | FontForge | fontTools and glyphsLib, installable with pip |
| Fira Code | 3.x, one `.liga` glyph per sequence | 6.x: its contextual rules verbatim, with every glyph they output (ligatures, one-cell pieces of arrows of any length, rows of `#` and `_`, centered forms, spacers) |
| What it changes | compiled fonts | Glyphs design sources, every master; or static TrueType fonts |
| Weight | Fira Code file chosen by the font's name | measured: Fira Code's weight axis at the point where its hyphen is as thick as the font's, per master |
| Vertical position | as in Fira Code | moved onto the font's math axis (the center of its hyphen) |
| Italic | upright glyphs | slanted by the font's italic angle |
| Feature | `calt` | `calt` by default, or any other tag (a stylistic set makes the ligatures opt-in) |

As before, glyphs are scaled to the font's em and, horizontally, to its cell, so a ligature of
*n* characters covers *n* cells. Lookups that only give single characters Fira Code's own
contextual forms (`0xFF` drawn with ×, punctuation raised next to capitals, Greek capitals) are
left out by default, with `www`, as Ligaturizer leaves out Fira Code's letter ligatures; see
[ligatures.py](ligatures.py).

## Use

```sh
pip install -r requirements.txt

# a Fira Code source directory: the release's variable font, its OFL.txt, and the rules
python ligaturize.py extract FiraCode.glyphs --out firacode/
cp FiraCode-VF.ttf OFL.txt firacode/

python ligaturize.py glyphs MyFont.glyphs --fira firacode/ --config ligatures.json
python ligaturize.py font MyFont-Regular.ttf --fira firacode/ --output-dir out/
```

`font` mode renames the family with a prefix (`Liga` by default, or `--output-name`), as
Ligaturizer does. The configuration file is described in `python ligaturize.py --help`.

## Licenses

This program is free software under the [GNU General Public License, version 3](LICENSE), as
Ligaturizer is. The license covers the program, not the fonts it changes: what it adds to a font
is Fira Code's data, not code of the program.

Fira Code is licensed under the [SIL Open Font License 1.1](https://openfontlicense.org). Its
glyphs may go into another font only if:

- the result is distributed under the SIL Open Font License 1.1 and nothing else, so the font
  receiving them must be under that license, or under one that allows relicensing to it;
- the result keeps Fira Code's copyright notice (this program adds it to the font's copyright
  string), and you keep it in the font's license file;
- the result keeps Fira Code's trademark notice, "Fira Mono is a trademark of The Mozilla
  Corporation" (this program adds it to the font's trademark string); the OFL grants no
  trademark rights, so never name the result after Fira;
- the result does not use a Reserved Font Name of either font; Fira Code declares none, but
  rename any font that does;
- the result is not sold by itself.

Do not use this program on fonts whose license does not allow it. This program comes with no
warranty, nor do the fonts it produces.
