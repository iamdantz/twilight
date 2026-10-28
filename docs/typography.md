# Twilight Theme typography

Version 1.20 · Typefaces: Twilight Crystal (sans-serif), Twilight Crystal Mono (monospaced)

Twilight Theme recommends its own typefaces, Twilight Crystal and Twilight Crystal Mono, for every target it themes. This document says what they are, what to use when they are not available, and how to turn on what they add. The colors of Twilight Theme do not depend on any font: every guarantee in [design-system.md](design-system.md) holds whatever face the text is set in.

## Contents

1. [The typefaces](#1-the-typefaces)
2. [Which font to use](#2-which-font-to-use)
3. [What Twilight Crystal adds](#3-what-twilight-crystal-adds)
4. [Optional ligatures](#4-optional-ligatures)
5. [The original letters are kept](#5-the-original-letters-are-kept)
6. [System fonts](#6-system-fonts)
7. [Installing and licenses](#7-installing-and-licenses)

## 1. The typefaces

| | Twilight Crystal | Twilight Crystal Mono |
| --- | --- | --- |
| Role | Interfaces, documentation, the web, documents and images | Code editors and terminals |
| Derived from | [Atkinson Hyperlegible Next](https://fonts.google.com/specimen/Atkinson+Hyperlegible+Next) 2.001 | [Atkinson Hyperlegible Mono](https://fonts.google.com/specimen/Atkinson+Hyperlegible+Mono) 2.001 |
| Weights | ExtraLight to ExtraBold (200–800), upright and italic | The same |
| Files | Variable TTF, static TTF, WOFF2 | The same |
| Adds | 60 characters | 481 characters, cell hinting, optional ligatures |
| License | SIL Open Font License 1.1 | The same |

Atkinson Hyperlegible was designed for the Braille Institute so that readers with low vision can tell characters apart: I, l and 1, or O and 0, each have a shape of their own. Twilight Crystal keeps that design and adds what a theme needs around it.

## 2. Which font to use

Twilight Theme encourages Twilight Crystal, and names the alternatives in order. The user's taste has the last word: any face can carry the theme.

1. **Twilight Crystal and Twilight Crystal Mono**, the recommended faces. They draw box drawing, arrows, symbols and Powerline separators in the same strokes as the letters, keep terminal lines on whole pixels, and offer optional ligatures. They are downloaded from the repository's releases and installed by hand.
2. **Atkinson Hyperlegible Next and Atkinson Hyperlegible Mono**, from Google Fonts. Twilight Crystal is a derivative of them: letters, spacing, kerning and features are the same, and `fonts/scripts/check.py` verifies on every build that they shape identically. Use them when Twilight Crystal has an error that affects you (please report it), or for convenience: they load in a web project from Google Fonts with one link and are packaged by Fontsource and Homebrew. What they lack are the additions of §3, which then come from whatever other font the system has.
3. **The system's own fonts**, last. Twilight Theme does not favor them: they may not reach the same legibility or character. They are the alternative when nothing else is possible, or when installing fonts is not wanted. §6 lists the closest ones on each system and how to size them.

## 3. What Twilight Crystal adds

Every added character is computed from the font's own measures (stroke, axis, cell) or assembled from its own outlines, so it reads as part of the font; the ligatures are Fira Code's, fitted to it (§4). Each addition has a check that measures it at every named instance.

| Addition | Twilight Crystal | Twilight Crystal Mono | Check |
| --- | --- | --- | --- |
| Arrows: ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↩ ↪ ↵ ⇐ ⇑ ⇒ ⇓ | Yes, with ⇔ ⇕ | Yes, in the cell | `arrowcheck.py` |
| Shapes and symbols: ■ □ ▲ ▶ ● ○ ◆ ∆ ∅ ⟨ ⟩ µ ‖ ′ ″ ⁴ ₁–₄ ⅓ ⅔ | Yes, with № | Yes, in the cell | `symbolcheck.py` |
| Box drawing and block elements (U+2500–259F) | No | Yes, joined across cells | `boxcheck.py` |
| Powerline separators (U+E0B0–E0B7) | No | Yes, filled, outlined and rounded | `boxcheck.py`, `symbolcheck.py` |
| Braille patterns (U+2800–28FF) | No | Yes | `symbolcheck.py` |
| Hinting for the cell (static fonts) | No | Lines on whole pixel rows, ink inside the cell | `hintcheck.py` |
| Programming ligatures | No | Optional, §4 | `ligacheck.py` |

## 4. Optional ligatures

Twilight Crystal Mono carries Fira Code 6.2's programming ligatures in stylistic set 1, named "Programming ligatures". They are off by default: with the set off, the font is Atkinson Hyperlegible Mono plus §3. With it on, `->`, `!==`, `<=`, `&&`, `|>` and the rest of Fira Code's set join, and arrows and rows of `-`, `=`, `#` and `_` join at any length. A sequence of n characters still takes n cells, so columns and the cursor do not move.

They are Fira Code's own glyphs and rules, fitted to the font: scaled to its cell, taken at the weight where Fira Code's hyphen is as thick as its own, moved onto its math axis and slanted in the italic. Fira Code's contextual forms of single characters (× in `0xFF`, punctuation raised next to capitals) are left out, and a double hyphen before a letter (`--watch`) stays plain.

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

## 5. The original letters are kept

Twilight Crystal does not change the letters, numbers, punctuation, spacing, kerning or features of Atkinson Hyperlegible. Changes to them were measured, and none both improved the measures and passed visual review, so the designers' work stays as it is. What Twilight Crystal changes is limited to:

- characters Atkinson Hyperlegible does not have (§3);
- the hinting of those characters;
- optional features, off by default (§4);
- names and metadata.

`fonts/scripts/check.py` enforces it on every build: every glyph of the upstream fonts keeps its advance width and its outline within 0.5 font units, and every character shapes as upstream with the default features and with each upstream optional feature.

## 6. System fonts

When neither Twilight Crystal nor Atkinson Hyperlegible can be installed, these are the closest faces each system ships by default. They were chosen by measurement among the fonts installed with each system: how close their shapes are to Atkinson Hyperlegible, how well they tell apart I, l, 1 and | (and O and 0 in monospaced faces) at small sizes, and whether they have an italic and a bold. A face whose I and l are the same single stroke was not considered.

| System | Sans-serif | Size | Monospaced | Size | Cell after sizing |
| --- | --- | --- | --- | --- | --- |
| Windows | Tahoma | 91 % | Cascadia Mono | 92 % | 0.54 em |
| macOS | Verdana | 91 % | Menlo | 91 % | 0.55 em |
| Linux, KDE | Noto Sans | 93 % | Hack | 91 % | 0.55 em |
| Linux, GNOME | Adwaita Sans | 91 % | Adwaita Mono | 95 % | 0.57 em |
| Linux, other | Noto Sans if installed | 93 % | DejaVu Sans Mono | 91 % | 0.55 em |

**Size** is the size that gives the face Twilight Crystal's x-height, the height of lowercase letters that sets how large text reads. All of these faces have taller lowercase than Atkinson Hyperlegible, so at the same nominal size they look larger; set at the listed fraction (in CSS, the `size-adjust` descriptor of `@font-face`; in an editor, a smaller font size), their lowercase matches Twilight Crystal's, and their capitals land within 1 % of its cap height (within 5 % for Cascadia Mono and Adwaita Mono). **Cell** is the monospaced advance after that sizing; Twilight Crystal Mono's is 0.632 em, so the same window holds 10 to 17 % more columns.

None of these faces has the ligatures of §4, and only some draw box drawing; Atkinson Hyperlegible Mono has neither.

## 7. Installing and licenses

The fonts are published with every release of the repository, one archive per family. Each archive holds the variable fonts (`variable/`), static fonts (`ttf/`) and web fonts (`webfonts/`), with `OFL.txt` and `FONTLOG.txt`. For desktop use, install the variable fonts, or the static ones where an application does not list a variable font's weights.

Twilight Crystal and Twilight Crystal Mono are licensed under the [SIL Open Font License 1.1](../fonts/OFL.txt). They may be used, embedded and redistributed freely, in any document, image, application or website, commercial or not; what is made with them is not covered by their license. They may be modified, and a modified version must keep the license and the copyright and trademark notices. They may not be sold by themselves. [FONTLOG.txt](../fonts/FONTLOG.txt) records every change from the fonts they derive from and credits their authors.
