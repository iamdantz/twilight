<h1 align="center">Twilight Crystal</h1>

<p align="center">
  <img src="../assets/crystal-specimen.png" alt="Twilight Crystal and Twilight Crystal Mono specimen: the pairs Il1| O0 rn m cl d, the seven weights, a paragraph of text, and a terminal with box drawing, a Powerline prompt and code with ligatures" width="900">
</p>

<p align="center">
  <a href="https://github.com/iamdantz/twilight-theme/releases/latest">Download</a> ·
  <a href="../docs/design-system/typography.md">Which font to use</a> ·
  <a href="OFL.txt">License</a> ·
  <a href="FONTLOG.txt">Changes and credits</a>
</p>

Twilight Crystal and Twilight Crystal Mono are the typefaces of [Twilight Theme](../README.md): a sans-serif for interfaces, documents, images and the web, and a monospaced face for code editors and terminals. They are derivatives of [Atkinson Hyperlegible Next](https://fonts.google.com/specimen/Atkinson+Hyperlegible+Next) and [Atkinson Hyperlegible Mono](https://fonts.google.com/specimen/Atkinson+Hyperlegible+Mono) and keep their letters unchanged; the [credits](#license) name their authors.

## Legibility

In Twilight Crystal, characters that other faces draw alike have shapes of their own: I has serifs and l a tail, 1 has a flag, 0 has a slash, and rn stays apart from m. These letters are the work of Atkinson Hyperlegible's designers, Elliott Scott, Megan Eiswerth, Linus Boman, Theodore Petrosky and Letters from Sweden, and their legibility is why Twilight Theme chose that design.

Twilight Crystal keeps that design: every letter, number and punctuation mark keeps the outline, spacing and kerning of the original, and every build checks this against the originals: same glyphs within 0.5 font units, same shaping. Changes to the original letters were measured, and none both improved the measures and passed visual review. What Twilight Crystal changes is limited to:

- characters Atkinson Hyperlegible does not have;
- the hinting of those characters;
- optional features, off by default;
- names and metadata.

The static fonts are hinted as the originals are, and a check confirms on every build that alignment and sharpness from 9 to 20 pixels, and the distinction of those pairs from 9 to 14 pixels, are no worse than the originals'.

## Made for terminals

Twilight Crystal Mono draws the characters terminal programs build their screens with, in the same strokes as its letters:

- **Box drawing and block elements**, all 160 of U+2500–259F. Lines reach the edges of the cell, so they join with the next cell and the next row without gaps, in trees, tables and full-screen programs.
- **Powerline separators**, filled, outlined and rounded, for prompts and status lines.
- **Braille patterns**, all 256, on the grid of the cell, for the graphs of terminal monitors.

In the static fonts these characters carry their own hinting: their lines land on whole pixel rows, at least one pixel thick, and no ink falls outside the cell, at 9 to 24 pixels.

## Optional ligatures

Twilight Crystal Mono includes Fira Code's programming ligatures, off by default in stylistic set 1. Turned on, `->`, `!==`, `<=`, `&&`, `|>` and the rest of Fira Code's set join, and arrows and rows of `-`, `=`, `#` and `_` join at any length. Each sequence keeps one cell per character, so columns and the cursor do not move. The glyphs are Fira Code 6.2's, fitted to this font's cell, weight, math axis and italic angle. Fira Code's contextual forms of single characters (× in `0xFF`, punctuation raised next to capitals) are left out, and a double hyphen before a letter (`--watch`) stays plain.

| Where | How to turn them on |
| --- | --- |
| VS Code, editor | `"editor.fontLigatures": "'ss01'"` |
| VS Code, terminal | `"terminal.integrated.fontLigatures.enabled": true` and `"terminal.integrated.fontLigatures.featureSettings": "\"ss01\""` |
| Windows Terminal | in the profile, `"font": { "face": "Twilight Crystal Mono", "features": { "ss01": 1 } }` |
| kitty | `font_features TwilightCrystalMono-Regular +ss01`, one line per style |
| WezTerm | `harfbuzz_features = { 'ss01' }` on the font |
| Ghostty | `font-feature = ss01` |
| Web pages | the `font-feature-settings` property with `"ss01"` |
| Word | Font, Advanced, Stylistic sets: 1 |
| Photoshop, Illustrator, InDesign | OpenType panel or menu, Stylistic Sets: Set 1 |

Where stylistic sets cannot be turned on, the text shows the plain characters, which is the default.

## Also included

Both families add arrows (← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↩ ↪ ↵ ⇐ ⇑ ⇒ ⇓, and ⇔ ⇕ in Twilight Crystal), geometric shapes (■ □ ▲ ▶ ● ○ ◆ ◇) and a few symbols (∆ ∅ ⟨ ⟩ µ ‖ ′ ″ ⁴ ₁–₄ ⅓ ⅔, and № in Twilight Crystal), each drawn from the font's own strokes and outlines. Both come in seven weights from ExtraLight to ExtraBold, upright and italic, as variable fonts, static fonts and WOFF2 web fonts.

## Installing

The fonts are published with every [release](https://github.com/iamdantz/twilight-theme/releases/latest), one archive per family. Each archive holds the variable fonts (`variable/`), static fonts (`ttf/`) and web fonts (`webfonts/`), with `OFL.txt` and `FONTLOG.txt`. For desktop use, install the variable fonts, or the static ones where an application does not list a variable font's weights.

## If you prefer the originals

Twilight Theme recommends Twilight Crystal, and it also recommends the fonts it comes from. If Twilight Crystal gives you trouble (please [report it](https://github.com/iamdantz/twilight-theme/issues)), or you would rather not install fonts by hand, use Atkinson Hyperlegible Next and Mono from Google Fonts. They have the same letters, load in a web project with one link, and are packaged by Fontsource and Homebrew. Without Twilight Crystal you lose the additions above, which then come from whatever font the system has.

When neither can be installed, the [design system](../docs/design-system/typography.md#2-system-fonts) lists the closest fonts each system ships, and the size that matches Twilight Crystal's. Your taste has the last word: Twilight Theme's colors work with any font.

## License

Twilight Crystal and Twilight Crystal Mono are licensed under the [SIL Open Font License 1.1](OFL.txt). Use them freely in documents, images, applications and websites, commercial or not, and redistribute or modify them, keeping the license and the copyright notices; they may not be sold on their own. [FONTLOG.txt](FONTLOG.txt) records every change from the originals and credits their authors.

| Source | Authors | License |
| --- | --- | --- |
| [Atkinson Hyperlegible Next](https://github.com/googlefonts/atkinson-hyperlegible-next) 2.001 | Applied Design Works and Letters from Sweden, for the Braille Institute | [OFL 1.1](upstream/atkinson-hyperlegible-next/OFL.txt) |
| [Atkinson Hyperlegible Mono](https://github.com/googlefonts/atkinson-hyperlegible-next-mono) 2.001 | The same | [OFL 1.1](upstream/atkinson-hyperlegible-next-mono/OFL.txt) |
| [Fira Code](https://github.com/tonsky/FiraCode) 6.2, the ligatures of Twilight Crystal Mono | Nikita Prokopov, from Fira Mono by Mozilla and Telefonica | [OFL 1.1](upstream/firacode/OFL.txt) |

Fira Mono is a trademark of The Mozilla Corporation.
