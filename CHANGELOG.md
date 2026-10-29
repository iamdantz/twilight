# Changelog

## 1.20.2

Typography measured. No palette, font or rule changes.

### Added
- `docs/construction/typography.md`: the numbers the type rules will be built on, each measured on the fonts or derived from a cited source.
  - Four viewing geometries: desktop screens, handheld screens, print, and slides seen from six slide heights.
  - Running text: 19 px on desktop screens and 16 px on handheld ones, the smallest sizes whose x-height reaches the critical print size (0.2°); 8 pt in print; 4.23 % of the slide height on slides.
  - Floors per weight, the smallest size at which stems and counters are at least one pixel: 12 px for Regular, from 10 px (Medium, SemiBold) to 19 px (ExtraLight).
  - Where there are no pixels, the floor is the angle of the Regular floor on a desktop screen: 5.1 pt in print, 2.68 % of the slide height.
  - Scale: step −2 on the floor, ratio 1.2583 on desktop, 1.1547 on handhelds, 1.2524 in print and 1.2563 on slides; the largest steps are bounded by the width of the viewport.
  - Line heights: 1.5 for running text, 1.3 (the font's natural line) for code, and 1.153 below which lines touch.
  - Measure: 80 characters are 34.6 em (53.4ch, since the zero is wider than an average character).
- `fonts/scripts/typography.py` prints every one of these numbers; the font workflow runs it.

## 1.20.1

Documentation reorganized by part. No palette or font changes.

### Changed
- The design system is a folder, `docs/design-system/`, with an index and one document per part: `color.md` (formerly `docs/design-system.md`) and `typography.md`. How the values were derived is in `docs/construction/`: `color.md` (formerly `docs/construction.md`).
- `docs/typography.md` is split: which font to use and the closest system fonts are in `docs/design-system/typography.md`; what Twilight Crystal adds, the optional ligatures and installing are on the font page, `fonts/README.md`.
- The validator and the docs generator follow the new paths.

## 1.20.0

Typography documented, fonts ready to release. No palette changes.

### Added
- `docs/typography.md`: the typefaces, what Twilight Crystal adds, how to turn on the optional ligatures in editors, terminals, web pages and design applications, and which font to use. Twilight Theme recommends Twilight Crystal and Twilight Crystal Mono. Atkinson Hyperlegible Next and Mono, on Google Fonts, are the alternative they derive from, for an error in Twilight Crystal or for convenience. The system's own fonts come last, and the user's taste has the last word.
- The closest system fonts, measured, with the size that matches Twilight Crystal's x-height:
  - Windows: Tahoma and Cascadia Mono;
  - macOS: Verdana and Menlo;
  - Linux: Noto Sans or Adwaita Sans, with Hack, Adwaita Mono or DejaVu Sans Mono.
- The rule that the original letters are kept, with what Twilight Crystal changes and what it does not.
- `fonts/README.md`: the page of Twilight Crystal. It starts with legibility, the reason Twilight Theme chose Atkinson Hyperlegible, and goes on to the terminal characters, the optional ligatures and the smaller additions. It ends with the originals on Google Fonts and the licenses. A specimen in the Dusk colors goes with it (`assets/crystal-specimen.png`).
- The documents this version and the earlier unreleased ones added were edited for plain language: no fragments for effect, no repeated sentence shapes, and no claims the checks do not measure.
- Releases: a tag `v<version>` on main builds the fonts and runs every check. It publishes one archive per family with variable, static and web fonts, `OFL.txt` and `FONTLOG.txt`, plus `SHA256SUMS.txt` (`fonts/scripts/package.py`, `.github/workflows/release.yml`).

### Licensing
- README: the license of each part of the repository, in one table.
- CONTRIBUTING: a contribution takes the license of the part it changes.
- Design system, building a theme: a port that ships the font files includes `OFL.txt` and `FONTLOG.txt` and never sells them on their own.
- Twilight Crystal Mono 1.006 credits Fira Code's designers beside Atkinson Hyperlegible's (name ID 9); `tools/ligaturizer` adds them as it adds Fira Code's copyright and trademark notices.
- `fonts/upstream/firacode/README.txt` says where each Fira Code file comes from.
- Twilight Crystal 1.003 and Twilight Crystal Mono 1.006 point to the renamed repository, `iamdantz/twilight-theme`.

## 1.19.0

Optional programming ligatures in Twilight Crystal Mono, from Fira Code. No palette changes.

### Renamed
- The typefaces are now Twilight Crystal (sans-serif) and Twilight Crystal Mono (monospaced), with files `TwilightCrystal` and `TwilightCrystalMono`. They were Twilight Text and Twilight Code during development and had not been released.
- The project is now Twilight Theme. The themes keep their names, Twilight Dusk and Twilight Dawn, and so does the naming *Twilight {Flavor}* for ports. The fonts' manufacturer (name ID 8) is Twilight Theme. The repository address is unchanged for now.
- Under the OFL a Modified Version may not use the Reserved Font Names of its sources. Atkinson Hyperlegible Next, Atkinson Hyperlegible Mono and Fira Code declare none, and no published font was found under either new name.

### Added
- Twilight Crystal Mono 1.005: Fira Code 6.2's programming ligatures in stylistic set 1, "Programming ligatures", off by default. With the set off nothing changes. With it on, `->`, `!==`, `<=`, `&&`, `|>` and the rest of Fira Code's set join; arrows and rows of `-`, `=`, `#` and `_` join at any length (`<==>`, `|-->`, `####`). A sequence of n characters still takes n cells. Turn it on with `"editor.fontLigatures": "'ss01'"` in VS Code, or the same feature in any application that sets OpenType features.
- Fira Code's rules are kept as they are, with three exceptions. Rules that redraw single characters in Fira Code's style are left out (`0xFF` with ×, punctuation raised next to capitals, Greek capitals), and so is `www`. One rule is added: a double hyphen before a letter (`--watch`) stays plain.
- The ligatures are scaled to Twilight Crystal Mono's cell, taken in each master at the weight where Fira Code's hyphen is as thick as its own, moved 72.5 units down onto its math axis, and slanted 12 degrees in the italic.

### Licensing
- Fira Code (SIL Open Font License 1.1, no Reserved Font Name) is pinned in `fonts/upstream/firacode` with its license and authors.
- Its copyright notice is in Twilight Crystal Mono's copyright string and in `fonts/OFL.txt`.
- Its trademark notice ("Fira Mono is a trademark of The Mozilla Corporation.") is in Twilight Crystal Mono's trademark string, as the OFL FAQ asks of derivatives.
- Twilight Crystal Mono's description credits Fira Code.
- Twilight Crystal and Twilight Crystal Mono remain under the OFL 1.1.

### Tooling
- `tools/ligaturizer`: a fork of Ligaturizer under the GNU GPL 3, rewritten on fontTools for Fira Code 6. It adds ligatures to Glyphs sources (every master) or to static TrueType fonts. It matches weight, math axis and slant, and turns Fira Code's reversed contours. The build runs it as a separate program, with `fonts/ligatures.json`.
- `fonts/scripts/ligacheck.py` checks four things at every named instance:
  - shaping identical to Fira Code 6.2 on a corpus of 155 sequences;
  - one cell per glyph;
  - the hyphen's weight and axis;
  - no ink past the clipping box.
- `check.py` accepts declared optional features. It verifies that their glyphs are reached only with the feature on, and that with it off shaping matches upstream.
- Fonts workflow: runs the ligature check; also runs on changes to the tool.
- `check.py` and `bakery.py` fail when the reference directory has no fonts for a family, instead of passing with nothing compared.
- Font Bakery: no new failures. Twilight Crystal Mono's longest full name ("Twilight Crystal Mono ExtraBold Italic") is over 32 characters, as upstream's is (`name/family_and_style_max_length`); Twilight Crystal clears it. Two new warnings are inherited from Fira Code's own glyphs:
  - glyph names over 31 characters;
  - four glyphs with coinciding segments, which the static fonts remove.

## 1.18.0

Hinting measured, and box drawing hinted for the cell. No palette changes.

### Changed
- Twilight Crystal Mono 1.004: in the static fonts, box drawing, blocks and Powerline separators carry instructions made for the cell instead of the autohinter's. The autohinter treated them as letters: in Regular, from 9 to 24 ppem, a third of their renderings put ink outside the rows of the cell, and in every weight some went past the Windows clipping box, where GDI cuts it off (at five to eight sizes); only 57 % of the rows their horizontal lines cover were fully covered. Now the cell's edges round to pixel rows, each line keeps its lower edge on a row and a whole number of pixels of thickness, at least one, and the same line lands on the same rows in every glyph: no ink outside the cell, 94 % of line rows fully covered. Outlines, letters and the variable fonts are unchanged.

### Documented
- The hinting of every static font measured against the upstream font hinted the same way, from 9 to 50 ppem: the same alignment of x-height, capitals and baseline (at most 0.4 % of renderings off the common row from 9 to 20 ppem, against 8 to 12 % unhinted), crisp horizontal edges (0.76 to 1.00, against 0.60 to 0.80 unhinted), the same distinction of confusable pairs, and no clipping that upstream does not have (upstream clips Ő and Ű by one pixel at 9 ppem).

### Tooling
- `fonts/scripts/cellhint.py`: the cell instructions; `build.py` applies them to the static fonts and compresses their web fonts again.
- `fonts/scripts/hintcheck.py`: per static font, instruction coverage, clipping, alignment, crispness and distinction against upstream, and for Crystal Mono the cell properties above. Built today: no failures.
- Fonts workflow: runs the hinting check.

## 1.17.0

Shapes, symbols and braille in Twilight Crystal and Twilight Crystal Mono. No palette changes.

### Added
- Twilight Crystal 1.002 and Twilight Crystal Mono 1.003, in both families:
  - Geometric shapes ■ □ ▪ ▫ ▲ △ ▴ ▵ ▶ ▷ ▸ ▹ ▼ ▽ ▾ ▿ ◀ ◁ ◂ ◃ ◆ ◇ ○ ● ◦, computed per master: small shapes have the area of the bullet, large ones that of a circle as tall as a capital; all sit on the math axis; outlined shapes take the plus sign's stroke, or one fixed fraction of it where a heavy master would close the hole.
  - ∆ and ∅ with the plus sign's stroke (∅ crossed at the angle and thickness of the slash), and ⟨ ⟩ as tall and as wide as the parentheses.
  - From the designers' own outlines, moved but not redrawn: ‖ (two bars, spaced like the equal sign), ′ ″ (the straight quotes at the italic angle), ⅓ ⅔ (digits and slash of ½ and ¾), ⁴ (the 4 of ¼ at superior size), ₁ ₂ ₃ ₄ (the superiors on the subscript line the font declares), µ (the u with its stem carried to the descender).
  - Twilight Crystal only: № (N and º); in Twilight Crystal Mono it does not fit one cell.
- Twilight Crystal Mono only: the 256 braille patterns (U+2800–28FF), a 2 × 4 grid of the font's own period spread evenly over the cell, so terminal graphs keep one dot spacing across cells and rows; and the rounded Powerline separators U+E0B4–E0B7.
- GF Latin Plus coverage: Crystal from 38 to 79 of 110 characters, Crystal Mono from 36 to 76. Left out, because they need new drawing rather than derivation: superior and inferior 5 to 9 and 0, Ω, Ⓓ and the currency signs beyond those already present.

### Tooling
- `fonts/scripts/symbols.py` and `fonts/scripts/braille.py`: the geometry and the derivations; `boxdraw.py` gains the rounded separators.
- `fonts/scripts/symbolcheck.py`: at every named instance, shapes on the axis with their areas and strokes, one stroke ratio across weights, derived digits at their source size and on their baselines, braille dots on the grid, rounded separators across the cell, and Crystal Mono glyphs inside the cell. Built today: no failures.
- `fonts/scripts/build.py`: components are resolved when a new glyph reuses an outline.
- Fonts workflow: runs the symbol check.

## 1.16.0

Arrows in Twilight Crystal and Twilight Crystal Mono. No palette changes.

### Added
- Twilight Crystal 1.001 and Twilight Crystal Mono 1.002: arrows ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ (U+2190–2199), ↩ ↪ (U+21A9–21AA), ↵ (U+21B5) and ⇐ ⇑ ⇒ ⇓ (U+21D0–21D3); Twilight Crystal also ⇔ ⇕ (U+21D4–21D5). Twilight Crystal gets 19 characters and Twilight Crystal Mono 17. They are computed from each master: the stroke and the axis of the plus sign, the line spacing of the equal sign, the italic angle. Shaft and head share one stroke; heads are open, with arms at 45 degrees. In Twilight Crystal a horizontal arrow is about as wide as a capital M; in Twilight Crystal Mono it fills the cell but for 40 units on each side.
- Crystal Mono leaves out ⇔ and ⇕: at ExtraBold a double line with a head at each end does not fit the cell with heads that reach past both lines.

### Tooling
- `fonts/scripts/arrows.py`: the geometry.
- `fonts/scripts/arrowcheck.py`: at every named instance, each shaft is as thick as the plus sign's bar and sits on its axis, double lines are spaced like the equal sign, opposite arrows match, no contour crosses itself, and Crystal Mono arrows stay in the cell. Built today: no failures.
- `fonts/scripts/build.py`: new glyphs are added by one routine, for box drawing and arrows alike.
- Fonts workflow: runs the arrow check.

## 1.15.0

Twilight Crystal Mono draws terminal interfaces: box drawing, block elements and Powerline separators. No palette changes.

### Added
- Twilight Crystal Mono 1.001: the 128 box drawing characters (U+2500–257F), the 32 block elements (U+2580–259F) and the four Powerline separators (U+E0B0–E0B3), in both styles and across the weight axis. They are computed from each master: the cell is the advance width and the typographic line box, light lines take the thickness of the hyphen, heavy lines twice that, and double lines are two light lines one line apart. Every line reaches the cell edge, so tables, trees, progress bars and prompts join across cells and rows, and no ink crosses it: a terminal that rounds the cell up to whole pixels can show a seam of up to half a pixel, faint, rather than ink bleeding into the next cell under a selection, a cursor or a background of another color. Twilight Crystal is unchanged.

### Tooling
- `fonts/scripts/boxdraw.py`: the geometry, read from the Unicode character names.
- `fonts/scripts/boxcheck.py`: at every named instance, each arm covers the band of the matching reference line on the cell edge, within half a unit, and the full block fills the cell; in the hinted static fonts at 12 to 24 px, lines laid out on a whole-pixel cell grid show no gap. Built today: no failures.
- `fonts/changes.json`: the code points a font adds on purpose; `check.py` accepts new glyphs only for them and still compares everything else with the upstream fonts. Built today: 164 added characters, no other differences.
- Fonts workflow: runs the box drawing check.

## 1.14.0

Twilight Crystal and Twilight Crystal Mono, the typefaces of Twilight Theme. No palette changes.

### Added
- fonts/: Twilight Crystal (sans-serif) and Twilight Crystal Mono (monospaced), Modified Versions of Atkinson Hyperlegible Next 2.001 and Atkinson Hyperlegible Mono 2.001 under the SIL Open Font License 1.1, which reserves no font name. This version renames them; outlines, spacing, kerning and features are the upstream ones.
- fonts/upstream/: the upstream design sources and license files, unmodified, pinned to one commit per family and verified by SHA-256 in fonts/upstream.json.
- fonts/OFL.txt and fonts/FONTLOG.txt: the license with the added copyright line, and the record of changes and credits.

### Documented
- README: the fonts in the repository layout and their license; CONTRIBUTING: how fonts are built and checked.

### Tooling
- `fonts/scripts/upstream.py`: copies the pinned upstream files, verifies them, and fetches the upstream's compiled variable fonts for comparison.
- `fonts/scripts/build.py`: renames copies of the sources and compiles them with gftools builder and the upstream configuration into variable TTF, static TTF and WOFF2.
- `fonts/scripts/check.py`: compares every named instance with the upstream fonts (glyphs, character map, axes, metrics, advance widths, shaping with every optional feature, outlines within 0.5 font units, the delta-optimization tolerance of variable fonts) and fails on any undeclared difference. Built today: no differences; the largest point shift is 0.50 units.
- `fonts/scripts/bakery.py`: Font Bakery's Google Fonts profile on the built and upstream fonts; fails on a new failure. Built today: none new, and the shorter family name clears `name/family_and_style_max_length`, which the upstream fonts fail.
- Fonts workflow: builds, compares and runs Font Bakery on every pull request that touches fonts/, and uploads the built fonts.

## 1.13.0

How much accent a view carries. No value changes.

### Changed
- design-system.md §5: the rule "one accent element per view besides focus and cursor" is replaced by two kinds of use. A mark (an element 4 px or thinner, a badge or counter, a small emblem, link text) is limited to one active mark per container. A fill (any larger accent area) is limited to one per view, on its single main action. Active indicators, badges and progress fills are now explicitly allowed alongside the main action.
- A view is a window, a full screen or a modal dialog; a floating layer with its own main action is a view of its own.

### Documented
- design-system.md §11 rule 8, the §12.6 checklist and two §13 misuses follow the rule.

## 1.12.3

Documentation reviewed for clarity. No value changes.

### Fixed
- construction.md: version line (1.12), the bright step (0.38) and the scales in §13, "flavor" where the text said "variant", and state separation described by bounds rather than targets.

### Documented
- construction.md §6.3: the chroma ceiling of the code colors stated as numbers (0.133 Dusk, 0.121 Dawn, against Afterglow's 0.188).
- Colon reveals and a binary contrast rewritten as plain sentences in construction.md, design-system.md and CONTRIBUTING; headings capitalized after the colon.
- README: the workflows directory in the repository layout.

## 1.12.2

The last parameters checked against the guarantees. No value changes.

### Changed
- Hue freedom is ±24° from the ANSI anchors instead of ±25°: the smallest, on a 1° grid, at which both flavors meet every minimum. The palette is the same from 24° to 26°.

### Documented
- construction.md §3.1: the neutral hue drift searched from 0° to 36°. Every guarantee holds from 12° to 24°, and none selects a value inside that range, so 18° stays a design choice.
- construction.md §9.4: the build order of the states does not change any state; all 720 orders of the transient states and both orders of the diff lines give the same colors in both flavors.
- construction.md §12: hue freedom and the series order move to the Resolved group; the state order is no longer listed as a parameter.

### Tooling
- `construct.py`: `FREEDOM = 24`; `transient_states()` builds the states in a given order. `validate.py` rebuilds them in reverse order and checks the hue rule against `FREEDOM`.

## 1.12.1

The syntax roles become reproducible. No value changes.

### Documented
- construction.md §8: keyword, string, function, type and constant follow the ANSI convention. The choice the convention leaves open, which of parameter and property stays uncolored, comes from a reproducible corpus study: distinctness does not separate the two (0.1200 and 0.1206), and properties cover more of the screen (6.37 % against 3.67 %, in every leave-one-out and bootstrap resample), so property stays uncolored. The ranking of all 5,040 assignments by distinctness alone is reported; the published one is 1,392nd, and the leaders break the convention without standing out from each other.
- The earlier study, whose corpus and scoring were never in the repository, is no longer cited.

### Tooling
- `syntax_study.py` and `syntax/manifest.json`: 34 packages pinned by version and SHA-256, under licenses that ask for no attribution (0BSD, MIT-0, Unlicense, CC0-1.0), verified in the registry and in each archive. The corpus is not stored; `fetch` downloads and verifies it and `measure` rebuilds `syntax/stats.json` byte for byte. Tree-sitter versions are pinned in `requirements-study.txt`.
- `syntax_roles.py`: the uncolored category and the distinctness ranking from `syntax/stats.json`. `validate.py` checks the published roles (`construct.SYNTAX`) against it and every package of the manifest against the accepted licenses.

## 1.12.0

Continuous scales for data.

### Added
- `scales` in every flavor of palette/twilight.json: a sequential scale of five Ember steps from Canvas, and a diverging scale of two Sky steps, Canvas, and two Gold steps (design-system.md §12.4).
- construction.md §7.2: each scale is a path at the color's hue from Canvas, with steps at equal ΔE. Steps keep the code colors' separation (ΔE 0.080 in normal vision, 0.040 under color-vision deficiency) from their neighbors, and the diverging steps from their counterparts; every colored step takes a label at AA. The series color and pair with the most steps passing in both flavors are chosen; ties go to the higher label contrast and the larger worst-case separation.
- Category minimums for the separation of scale steps and for their labels.

### Documented
- design-system.md §12.4: continuous scales replace the rule that left them undefined. §13 points interpolation to the scales.
- construction.md §11: the diverging scale holds two steps per side.

### Tooling
- `construct.py`: `SEQUENTIAL`, `DIVERGING` and `scale_search()`; every flavor builds its scales. `validate.py` reproduces them, checks that the search still returns them, measures the new minimums, and skips checks a base snapshot predates. `docs.py` generates the scale table and guarantee rows.

## 1.11.1

The ceilings of the strong states, verified. No value changes.

### Documented
- construction.md §9.2: a state's chroma never exceeds what sRGB holds at Canvas's lightness for its hue. The §9.3 search already applied this bound, since every scan starts at Canvas and stops at the first out-of-gamut color; without it the strongest states become saturated fills (Dawn's current match would reach 8.7 JND in `#ffd545`).
- A search over every sRGB color confirms the six strong states at their ceiling within 0.02 JND.
- construction.md §11: the three rows for state targets out of reach are replaced by one: Dawn's selection is the least visible strong state, and why.

### Tooling
- `validate.py`: a rule checks every state's chroma against the bound (0.002 tolerance for 8-bit rounding).
- `validate.py --compare`: a lowered floor or limit may be declared under Lower in any CHANGELOG entry newer than the base, so a pull request that spans several versions is checked against each entry, not only the latest.

## 1.11.0

State visibility follows from the bounds and the minimum, with no fixed targets.

### Changed
- Background states come in strong and weak pairs (construction.md §9.1). A strong state (`selection`, `find-match`, `word-highlight-write`) takes the most visible color the bounds of §9.2 allow; a weak state (`selection-inactive`, `find-match-other`, `word-highlight`, diff lines) takes 2 JND, the visibility minimum. The fixed targets 4, 5, 3, 2.5 and 2 JND are removed from §12.
- Dusk `selection`, `find-match-other`, `word-highlight-write`; Dawn `find-match-other`, `word-highlight-write`.

### Improved (against 1.10.2)
- Dusk `selection` 4.09 → 4.61 JND; `word-highlight-write` 3.05 → 3.25 (Dusk) and 3.05 → 3.79 JND (Dawn).
- Strong state from its weak partner: selection 2.58 → 3.36 JND (Dusk); current match 3.35 → 3.53 (Dawn); write from read 1.21 → 1.50 (Dusk) and 1.48 → 2.37 JND (Dawn).
- Mean visibility of the eight states stays within 0.03 JND.

### Lower
- `JND find-match-other`: Dusk 2.57 → 2.01, Dawn 2.56 → 2.04 JND. Other matches move to the weak-state minimum, 0.5 JND less visible; they stay at least 3.1 JND from the current match. The fixed 2.5 JND target had no derivation.

### Documented
- construction.md §3.3: r rechecked under the new rule; Dawn still has a pair of states 0.61 JND apart at 1.30, so r stays 1.3125.

### Tooling
- `construct.py`: `STATE_ROLE` and `WEAK_JND` replace the per-state targets; a strong state has no target in the §9.3 search. `validate.py`: `LIMIT_FLOORS` current as of 1.11.0.

## 1.10.2

Ember's constraints checked against the guarantees. No value changes.

### Changed
- The §6.5 objective no longer penalizes an Ember closer than ΔE 0.06 to Afterglow. The penalty never acted (Ember is ΔE 0.216 from Afterglow in Dusk and 0.360 in Dawn), and both flavors rebuild identically without it, also with 40 restarts.

### Added
- Category minimum: Ember at least ΔE 0.080 from Afterglow in normal vision, the normal-vision minimum of the code colors.

### Documented
- construction.md §6.4: Ember's hue range searched against Afterglow ± 25° and against the hues nearest Afterglow among the anchors. Both lower the separation, so 45°–70° stays decided.

### Tooling
- `construct.py`: `EMBER_VS_AFTERGLOW` removed. `validate.py` and `docs.py`: the new check, its floors and guarantee row.

## 1.10.1

The neutral chroma amplitude is searched against the guarantees. No value changes.

### Documented
- construction.md §3.2 and §12: the amplitude 0.035 moves to the Resolved group. From 0.020 to 0.050, in steps of 0.0025, it is the largest value at which Dusk reaches its best code-color separation, inside the range where Dawn meets every minimum (up to 0.0375; from 0.040 Faint comes within 1 JND of a semantic color in Dawn).

## 1.10.0

The bright step is searched on the twelve chromatic terminal colors.

### Changed
- Brights move 0.38 of the way toward Ink instead of one third. The step is the one, from 0.29 to 0.89, that keeps every bright 2 JND from its normal and from Ink and gives the twelve chromatic ANSI colors the largest closest pair in every vision (construction.md §6.7). It moves to the Resolved group of §12.
- ANSI 9 to 14 in both flavors.

### Improved (against 1.9.1)
- Closest pair of the twelve chromatic terminal colors, worst vision: Dusk 0.0124 → 0.0201, Dawn 0.0117 → 0.0195.
- Closest pair in normal vision: 0.048 → 0.055.
- Each bright from its normal: at least 2.39 → 2.73 JND.
- Lowest bright contrast on Canvas: 7.65 → 8.12:1.

### Costs
- Brights sit closer to Ink in Dusk (2.69 → 2.38 JND under color-vision deficiency) and closer to each other (0.0217 → 0.0195 in Dawn). Both losses are under 1 JND, and both values are new measurements, not floors.

### Added
- Category minimum: the closest pair of the twelve chromatic terminal colors, in every vision, at least ΔE 0.010.
- construction.md §11: the closest pair stays near 1 JND under color-vision deficiency.

### Tooling
- `construct.py`: `BRIGHT_STEP` and `bright_step()`, the search of §6.7. `validate.py` checks that the search still returns the published step, and the new minimum with its flavor floors.

## 1.9.1

Parameters checked against the guarantees. No value changes.

### Documented
- construction.md §12: a Resolved group for parameters whose value the guarantees select over a searched range. The surface ratio r and the warm tilt τ move there. τ = 0.15 is the only value from 0.10 to 0.20, in steps of 0.01, at which both flavors meet every minimum.
- construction.md §6.3: the gamut margin 0.92 is searched too. Dawn meets every minimum from 0.92 to 0.932; 0.93 would gain ΔE 0.0007 in color-vision separation and sit 0.005 from a value that breaks four minimums, so 0.92 stays.
- construction.md §11: Dawn's color-vision separation of the code colors (ΔE 0.0402) is the optimizer's maximum, and no parameter tested raises it without breaking another minimum.
- Auditor skill: the resolved class of parameters.

## 1.9.0

Semantic colors outside code, and a measured limit of Faint in light flavors. No value changes.

### Added
- Text in a semantic color uses that color's `accent-text`, which meets the code floor of its category on every surface. The color itself stays for icons, markers and bars. In Dawn, Grove, Gold and Sea Salt are 4.15, 4.32 and 4.39:1 on Raised, below AA for text.
- Category minimums: semantic colors at least 3:1 on every surface and on Edge; Faint at least 1 JND from every semantic color in every vision.
- Version-control markers carry a letter or an icon.

### Documented
- construction.md §11: in Dawn, Faint is 1.05 JND from Grove under color-vision deficiency. The three corrections measured (optimizer objective, a higher code floor, a darker Faint) and why each was rejected.
- design-system.md §13: a semantic color used directly for text is a misuse.

### Tooling
- `validate.py` and `docs.py`: the two new checks, their guarantee rows and facts.

## 1.8.1

Continuous validation. No value changes.

### Tooling
- `.github/workflows/validate.yml`: every pull request to `main` and every push to it runs the validator against the base, with full reproduction, and writes the report to the job summary. Pull requests that touch the construction also run `--robust`. Pull requests that edit the validator also run the base branch's copy on the change, without blocking, so a loosened check is visible.
- CONTRIBUTING: what the workflow checks, how to run it locally, and the merge methods.

## 1.8.0

Afterglow is the accent of every theme. No token is removed and no value changes.

### Changed
- A theme is named by its flavor alone, *Twilight Dusk* or *Twilight Dawn*, and uses Afterglow as its accent. The accent families of the other seven colors stay in palette/twilight.json, built and validated as before; no theme uses them, and their colors keep their roles as code, semantic and series colors.
- The cursor belongs to the flavor, like selection: it is Afterglow's `accent-focus`, the color the code colors are optimized against, whatever the accent.
- design-system.md §13 lists an accent family other than Afterglow as a misuse.

## 1.7.0

How to apply Twilight to any target, and how not to. No color changes.

### Added
- `series` in palette/twilight.json: the order of data series (Sky, Ember, Gold, Sea Salt, Orchid, Grove) and the neutral for any series past the sixth (Control). The order is searched on Dusk and Dawn and shared by every flavor (construction.md §7.1).
- design-system.md §12, Applying the system: regions by function, nesting and elevation, states of neutral rows and controls, data visualization, and limited targets (fewer surfaces or text levels, one accent color, sixteen terminal colors).
- design-system.md §13, How not to apply: each misuse, what it breaks, and what to use instead.
- Category minimums: Subtle on an Edge fill 4.5:1; the chip label on `accent-text` 4.5:1; Other at least ΔE 0.040 from every series in every vision; the closest pair of neutral row and control states at least 1 JND.

### Changed
- A selected row is no longer Raised. Raised is the hover fill on Rail and Canvas; a selected row takes `selection-inactive` or `selection`. On Shell and Raised, which are less than 1 JND apart in light flavors, hover takes `selection-inactive`.
- The guarantee table moves from §13 to §14 of design-system.md.

### Tooling
- `validate.py`: the four new checks with their flavor floors; the published series must equal the decided order, and the search of §7.1 must still return it. Guarantee rows are matched with specific labels first, and a section heading without a flavor name ends the previous flavor's tables.
- `docs.py`: generates the series table, the new guarantee rows and the facts of §12.

## 1.6.2

Tooling to keep documents and images generated from the palette. No value changes.

### Tooling
- `scripts/docs.py` regenerates every table, measured number and swatch strip in README.md and design-system.md, and redraws both palette images, from palette/twilight.json. Numbers that appear in prose sit between `<!-- fact:NAME -->` markers. `--check` reports any difference and exits 1.
- `validate.py`: the consistency step runs the generator in check mode, so a document or image that drifts from the palette fails. Images are checked by sampling each swatch and circle against the JSON.
- `validate.py --robust`: rebuilds every flavor with 20 optimizer restarts instead of 10 and fails if any token changes, so a shipped solution cannot sit on an optimum that more search would leave.
- `validate.py` reads the flavor columns of the construction.md hue table from its header, so a new flavor needs no change to the check.
- Pillow 11.3.0 pinned in requirements.txt.

### Documented
- README guarantees and design-system.md §4 minimums are rounded to two decimals from the measured values; both images redrawn by the generator.

## 1.6.1

Documentation brought up to date with 1.6. No value changes.

### Fixed
- design-system.md §3: surface separation is 1.04 to 1.28:1 in Dusk and 1.04 to 1.21:1 in Dawn (it still read 1.13 and 1.17).
- design-system.md §4: the Ink minimum is 12.8:1 (it still read 13.4).
- design-system.md §6: Afterglow is computed from the seed; it is not the seed.
- design-system.md §10 and construction.md §11: of ANSI black and white, the slot that matches the background is Edge; the other is a text level. Both used to be described as 1.4:1 surfaces.

### Documented
- design-system.md: rules that differ between dark and light themes name the category, not the flavor (principle 6, §2, §5 `accent-text`, §8 chip labels, §10 brights, rule 13 shadows, §12 checklist), so every flavor of a category follows them.

## 1.6.0

Quality floors in two levels: category minimums, the Twilight standard every dark or light flavor meets, and flavor floors, what Dusk and Dawn reach today. No value changes.

### Added
- Category minimums for dark and light themes (construction.md §10.1): code 7:1 or 4.5:1; Body, Subtle, Faint and Control at the §3.5 targets; Ink at least the Body target and above Body; focus 3, on-accent 4.5, accent-text 7 or 4.5; code-color ΔE at least 4 JND in normal vision and 2 JND under color-vision deficiency; every background state at least 2 JND from Canvas and every pair at least 1 JND apart.
- Rule for lowering a flavor floor: it still meets its category minimum, the changelog names it under Lower with its cause and benefit, and the loss is imperceptible or well inside the standard.
- A new flavor is checked against its category's minimums; its measured values become its floors.

### Tooling
- `validate.py`: `MINIMUMS` per category and `FLOORS` per flavor replace the (Dusk, Dawn) table and the fixed/measured split. Every value is reported next to its flavor floor and its category minimum. `--compare` rejects a lowered category minimum, a flavor floor lowered without its Lower entry, and a flavor floor below its minimum; a flavor with no floors is reported. Base snapshots with the earlier table format are read per flavor.
- New checks: every background state ≥ 2 JND from Canvas, the closest pair of states ≥ 1 JND, and Ink above Body on every surface.

### Documented
- construction.md §10.1; design-system.md §13; CONTRIBUTING; auditor skill area C, D and the verdict rules.

## 1.5.0

The surface ratio r goes from 1.25 to 1.3125 (21/16): the smallest value at which both flavors keep every guarantee, every pair of background states is at least 1 JND apart, and Dusk's write highlight reaches its target. Code colors and Afterglow are unchanged.

### Changed
- System: r = 1.3125 at L_ref = 0.20. Surface distances from Canvas: Shell 2.41, Raised 3.16, Edge 7.22 JND (were 1.98, 2.51, 5.68).
- Dusk and Dawn: Shell, Rail, Raised and Edge, the text levels solved against Raised, `accent-text` where it is solved against Raised, `on-accent` (the new Shell in Dusk), Dawn's Afterglow `accent-focus`, and the states that follow. Canvas and Ink are unchanged.

### Improved (against 1.4.1)
- Dusk `word-highlight-write` 2.50 → 3.05 JND (target reached); `find-match` 3.61 → 4.06 JND; ANSI black and white on Canvas 1.39 → 1.57:1; Shell and Rail 1.10 → 1.35 JND apart.
- Dawn `selection` 2.79 → 3.45 JND; `find-match` 4.31 → 4.74 JND; ANSI black and white 1.43 → 1.58:1; selection and inactive selection 0.96 → 1.68 JND apart. Every pair of states in both flavors is now at least 1 JND apart.

### Lower (against 1.4.1)
- `ink on surfaces`: Dusk 13.76 → 13.25:1, Dawn 13.36 → 12.84:1. Ink is the same color; Raised sits further from Canvas. Ink on Canvas stays 15.58:1.
- Dusk control on every surface 3.03 → 3.00:1 and Afterglow focus 6.22 → 5.99:1; both still meet their thresholds.

### Documented
- construction.md §3.3 (r and the sweep that set it), §3.4, §3.5, §5, §9.2, §9.4, §11 (the Dawn state pair under 1 JND is gone) and §12.
- design-system.md and README: regenerated neutral, accent, state and terminal tables; guarantees; surface lightnesses.
- `assets/palette-*.png` repainted with the new neutrals.

### Tooling
- `validate.py`: Ink floors 13.25 (Dusk) and 12.84 (Dawn); `LIMIT_FLOORS` current as of 1.5.0.

## 1.4.1

The method is organized in three levels: system, category and flavor. Dawn no longer reads Dusk. No value changes.

### Tooling
- `construct.py`: system constants, `CATEGORIES` (dark, light) and `FLAVORS` (Dusk, Dawn). One neutral builder places every flavor's surfaces at the system distances from its own Canvas, in its category's direction, and solves its text levels and Rail. Dawn's anchors are its own parameters, and its surface distances come from the system, not from Dusk's neutrals.
- The surface ratio is a system parameter: r = 1.25 at L_ref = 0.20, as ΔE distances (1.98, 2.51, 5.68 JND).
- The neutral chroma amplitude is a flavor parameter (0.035 in both).
- Both flavors rebuild exactly. Changing Dusk's Canvas, Ink or amplitude no longer moves any Dawn token.

### Documented
- construction.md §1.1 (the three levels), §3.3 (surface distances), §4 (Dawn's own anchors), §12 and §13.
- Auditor skill: the construction's levels; a new flavor is an entry in `FLAVORS` within an existing category.

## 1.4.0

The construction now builds what the validator guarantees: the cursor is part of the hue optimization, and background states keep 1 JND from each other. Code colors are unchanged in both flavors.

### Changed
- §6.5: the optimizer compares every code color with the cursor (Afterglow's `accent-focus`), Coral excluded, the same pairs as the color-vision guarantee. Published hues are unchanged; Dawn's first pass moves, so Dawn `diff-removed` is now `#f4dde0`.
- §9.4: states are built in a fixed order, each kept at least 1 JND from the states before it whenever a color that reaches its target allows it. Dusk `selection-inactive` is now `#260f02` and Dusk `word-highlight-write` `#182423`.

### Improved (against 1.3.0)
- Dusk: the two word highlights 0.80 → 1.23 JND apart; inactive selection and removed diff 0.54 → 1.08 JND; closest pair of states ΔE 0.011 → 0.022.
- Dusk `selection-inactive` 2.1 → 2.9 JND.
- Dawn: inactive selection and removed diff 0.61 → 1.01 JND; closest pair of states ΔE 0.012 → 0.019; `diff-removed` 2.02 → 2.06 JND.
- Pairs of states under 1 JND: four → one (Dawn selection and inactive selection, 0.96 JND).

### Lower (against 1.3.0)
- `JND word-highlight-write`: Dusk 2.689 → 2.501 (target 3 was not reached before either). The color keeps its lightness at half the chroma, 0.88 JND from the old one, and is now distinguishable from `word-highlight`.
- Dawn code colors on every code surface 4.54 → 4.52:1, from the new removed-diff background; still meets 4.5:1.

### Documented
- construction.md §6.5 (cursor in the objective), §9.4 (separation between states), §11 (one state pair under 1 JND), §12 and §13.
- design-system.md §9: states stay 1 JND apart.

### Tooling
- `construct.py`: `optimize()` takes the cursor; `state()` takes the states already built and prefers a color 1 JND from them.
- `validate.py`: `LIMIT_FLOORS` current as of 1.4.0 (Dusk and Dawn closest state pair 0.0215 and 0.0191).
- Auditor skill: the floors table shows the Dusk ΔE floors raised in 1.3.0 (0.097, 0.061).
- `validate.py --compare`: the stale-image check looks only at neutrals and colors, the values `assets/palette-*.png` shows. A change to background states no longer requires new images.

## 1.3.0

Afterglow and the chroma base are computed from the seed. Dusk's code colors gain chroma; Dawn changes only in Afterglow.

### Changed
- Afterglow is the sRGB cusp of the seed hue: `#ff7d00` (L 0.727, C 0.188) instead of the seed itself. The seed `#ee7a1f` stays the origin of the system and is no longer a token. Both flavors share the new Afterglow and its accent family.
- The chroma base C₀ depends on polarity, like β: C_Afterglow / φ = 0.116 in dark flavors, C_seed / φ = 0.105 in light ones (construction.md §6.3). Dawn's code colors are unchanged.
- Dusk: every code color, its accent family and its bright, plus `word-highlight`, `word-highlight-write` and `diff-inserted`, follow from the new base. Dusk's neutrals are unchanged.
- The selection hue is Afterglow's hue (51.7°). Both selection states keep their values.

### Improved (against 1.2.0)
- Dusk smallest code-color difference, normal vision: ΔE 0.089 → 0.097.
- Dusk smallest code-color difference, color-vision deficiency: ΔE 0.054 → 0.061.
- Dusk `word-highlight-write` 2.6 → 2.7 JND. Dusk Afterglow focus 5.65 → 6.22:1; on-accent on Afterglow 6.86 → 7.55:1.
- Dawn: label on pressed Afterglow 4.51 → 4.85:1.

### Lower (against 1.2.0)
- `JND word-highlight`: Dusk 2.015 → 2.013 (target 2, still met).
- `JND diff-inserted`: Dusk 2.043 → 2.021 (target 2, still met).
- Dusk code colors on every code surface 7.04 → 7.00:1 and `accent-text` on Raised 7.01 → 7.00:1; both still meet 7:1.
- Dawn Afterglow focus 3.02 → 3.01:1; still meets 3:1.

### Documented
- construction.md §2 (seed and Afterglow), §4 (chroma base per flavor), §6.3 (why light flavors take the seed's chroma), §6.5 hue table, §7, §11 and §12.
- design-system.md and README: one seed instead of two, and the regenerated Dusk values.

### Tooling
- `construct.py`: `AFTERGLOW` is computed from the seed hue; each profile names its `chroma_base`.
- `validate.py`: Afterglow must equal the cusp of the seed hue. Dusk floors follow the rebuilt flavor (normal-vision ΔE 0.097, color-vision ΔE 0.061) and `LIMIT_FLOORS` are current as of 1.3.0. The seed hex may appear in the documents.

## 1.2.0

Dawn rebuilt as the light end of the same system. Dusk is unchanged, value for value.

### Changed
- Dawn: every value. Canvas and Ink swap Dusk's two anchors (Canvas `#eeeeef`, Ink `#11171b`), so the lightest value in Twilight is L 0.95 instead of 0.975.
- Dawn surfaces keep Dusk's perceptual distance from Canvas (ΔE OKLab) instead of its contrast ratios. Every Dawn neutral sits on the shared neutral curve, with no relative-chroma correction.
- Dawn uses β = 0.19, the slope measured on light themes; Dusk keeps 0.30, measured on dark themes (construction.md §6.2).
- Background states: away from the text, a state stops at the outermost surface (Shell in Dusk, Canvas in Dawn). Dusk is unaffected.

### Improved (Dawn, against 1.1.1)
- `selection` 2.2 → 2.8 JND; `find-match` 3.0 → 4.3 JND; `word-highlight-write` 2.3 → 3.0 JND (target reached).
- Selection vs inactive selection 0.22 → 0.96 JND; closest pair of background states 0.22 → 0.61 JND.
- Smallest code-color difference, normal vision: ΔE 0.077 → 0.088.

### Lower (Dawn, against 1.1.1)
- `ink on surfaces`: 14.81 → 13.36:1, from the darker Canvas. Ink on Canvas is 15.58:1 in both flavors.
- `ΔE code+cursor, worst CVD`: 0.041 → 0.040 (0.0411 → 0.0402, about 0.05 JND).
- `JND diff-removed`: 2.025 → 2.021 (target 2, still met).
- Control on any surface 3.02 → 3.00:1 and `accent-text` on Raised 4.51 → 4.50:1; both still meet their WCAG thresholds.

### Documented
- construction.md §4 rewritten (Dawn: the light end), Dawn β in §6.2, updated limits in §11.
- The syntax-role assignment is a decided parameter (construction.md §12). β is documented as measured on dark and light themes. No other theme is named in the documents.
- Versioning: values regenerated by the documented method are a minor release; removing or renaming a token is a major one (CONTRIBUTING.md, auditor skill).

### Tooling
- `construct.py` splits the shared core from two flavor profiles (anchors, floor, β, search ranges) and rebuilds both flavors exactly.
- The ±25° hue bound is enforced by the optimizer on the rendered hue against the exact anchor, the same way the validator checks it. Dusk is unaffected.
- `validate.py`: Dawn floors follow the rebuilt flavor. Ink 13.36, color-vision ΔE 0.040, normal-vision ΔE 0.088 (construction.md §4).
- `validate.py --compare`: WCAG thresholds and text targets are fixed guarantees and never go down. Ink, the two ΔE floors and the known limits (`LIMIT_FLOORS`) are measured minimums and go down only when the version's entry names each one, in backticks, under `### Lower`. Removing a check is a regression.

## 1.1.1

### Fixed
- docs: five background-state JND values did not match the published colors (2.1 → 2.0, 3.1 → 3.0).
- docs: Sea Salt Dusk hue in §6.5 is the optimizer's 197°, not the measured 196°.

### Documented
- construction.md now specifies the optimizer (seed, restarts, schedule, score), the two-pass
  code-surface procedure, the background-state cost function, search ranges and precision
  conventions. The palette is unchanged.

### Added
- `twilight-auditor` skill: reference implementation of the construction method and the audit checks (floors, reproduction, document consistency).

## 1.1.0

One rule added before the first ports. No values changed.

- Links in running text carry a non-color cue (underline or icon). No `accent-text` reaches 3:1 against Body, so color alone fails WCAG 2.2 SC 1.4.1.

## 1.0.0

First public definition.

- Two flavors: Dusk (dark) and Dawn (light).
- Ten neutrals: Shell, Rail, Canvas, Raised, Edge, Control, Faint, Subtle, Body, Ink.
- Eight colors: Afterglow, Coral, Gold, Grove, Sea Salt, Sky, Orchid, Ember.
- Interchangeable accents: any of the eight colors, each with text, pressed, focus and label tokens.
- Syntax roles, semantic states, background states and the sixteen terminal colors.
- Design system and construction documents.
- All values in `palette/twilight.json`.
