# Twilight Theme construction: typography

Version 1.0. How the typographic values were derived and measured.

The companion document, [design-system/typography.md](../design-system/typography.md), states the type rules. This one derives the numbers they are built on: the size of running text, the smallest size of each weight, the scale, line heights, the measure, figures and the size of code. Every number below is printed by [`fonts/scripts/typography.py`](../../fonts/scripts/typography.py) from the built fonts and the decided parameters of §11, and the font workflow runs it on every change to the fonts.

---

## 1. Method in one page

1. **Sizes are set by visual angle, not by habit.** Reading speed is at its maximum only when the x-height subtends at least the critical print size, 0.2°. On screens and slides, running text is the smallest size that reaches it, and on screens never smaller than the reader's default size. Page documents take the size style guides set for them, 12 pt, which reaches it on paper.
2. **Floors are set by the pixel.** Each weight has a smallest size, the first whole pixel size at which both its stems and its narrowest counters are at least one pixel wide. Below it, strokes blur into partial pixels, so the text shows a lower contrast than its color guarantees, or counters fill in. Where there are no pixels, on slides, the floor is the angle the Regular floor subtends on a desktop screen.
3. **The scale is the strongest one the floors allow.** Step 0 is running text and step −2 sits on the floor; the ratio follows from those two sizes. Every step is then checked against the top of the fluent range and against the narrowest screen.
4. **Spacing is taken from the font and from WCAG.** Code uses the font's own line, so box drawing joins across lines; running text uses WCAG's 1.5; no line height is allowed at which two lines can touch.
5. **The measure is counted in characters of real text**, then converted to em, because Twilight Crystal's zero is wider than its average character.
6. **Code in editors and terminals** has a minimum, the smallest size at which the Mono grid lands on whole pixels, and an optimal size, at least as large as each system's default editor shows code and on the cleanest grid.

Designer decisions and their sources are listed in §11; everything else is measured.

---

## 2. The fonts' own numbers

| | Twilight Crystal | Twilight Crystal Mono |
|---|---|---|
| x-height | 0.496 em | 0.496 em |
| Cap height | 0.668 em | 0.668 em |
| Natural line (ascender to descender, no line gap) | 1.300 | 1.300 |
| Lines touch below (tallest letter ĺ over deepest letter Ģ) | 1.153 | 1.129 |
| Figures by default | proportional, 0.407 to 0.648 em | tabular, 0.632 em |
| Tabular figures (`tnum`) | 0.632 em | 0.632 em |
| Zero (the CSS `ch` unit) | 0.648 em | 0.632 em |

The two families share x-height and cap height, so code set inside text at the same size matches it with no adjustment. Twilight Crystal's tabular figures are exactly one Mono cell wide, so numbers in a table line up with numbers set in Twilight Crystal Mono.

---

## 3. Viewing geometry

The same CSS pixel covers a different angle depending on the device and how far away it is read. Four geometries are measured:

| Geometry | Unit | Angle of one unit | Basis |
|---|---|---|---|
| Desktop | CSS pixel | 0.02132° | The CSS reference pixel: one pixel at 96 dpi seen from 28 inches |
| Handheld | CSS pixel | 0.02842° | A pixel of 1/160 inch (the density-independent pixel of handheld systems) at 32 cm, the measured mean distance at which people read web pages on a phone |
| Documents | point | 1/72 inch at 40 cm on paper; 4/3 px on a desktop screen at 100 % zoom | Pages read printed or on screen |
| Slides | percentage of the slide's height | seen from 6 slide heights | The farthest viewer for content that must be read, by the 4/6/8 rule of audiovisual room design |

A CSS pixel on a phone covers a third more angle than on a desktop screen, so the same size in pixels looks larger on a phone. The width of the viewport does not tell the two geometries apart: a phone in landscape and a narrow desktop window can have the same width.

Slides are one case of text read from a distance. For any such text (a poster, a sign) seen from at most D, the critical print size is an x-height of D × tan 0.2°, a Twilight Crystal size of **<!-- fact:t.distance.step0 -->0.704 %<!-- /fact --> of D**; the floor angle of §5 gives <!-- fact:t.distance.floor -->0.446 %<!-- /fact --> of D, and the ratio is <!-- fact:t.distance.ratio -->1.2556<!-- /fact -->.

---

## 4. Running text

Running text needs an x-height of at least 0.2°, the critical print size, below which reading slows. On screens and slides the size is the smallest that reaches it, rounded up to whole pixels on screens and hundredths of a percent on slides; on screens it is never smaller than the browser's default of 16 px:

| Geometry | x-height needed | Smallest size | Size | x-height at that size |
|---|---|---|---|---|
| Desktop | 9.38 px | 19 px | **19 px** | 0.201° |
| Handheld | 7.04 px | 15 px | **16 px** (the default) | 0.226° |
| Documents | 1.40 mm on paper | 8 pt | **12 pt** (decided) | 0.301° on paper |
| Slides | 2.09 % of the slide height | 4.23 % | **4.23 %** | 0.200° |

The browser default of 16 px meets the critical print size on handhelds but not on desktop screens, where it gives 0.169°. On a slide 7.5 inches high (540 pt), 4.23 % is 22.8 pt.

Page documents are read on paper of every size and on screens at every zoom, so no single geometry fits them. They take the size style guides give body text, 12 pt (the size APA Style gives Aptos and Times New Roman, the largest it lists), which is 1.5 times the critical print size on a page held at 40 cm. On a desktop screen at 100 % zoom, 12 pt is 16 px, 0.169°; a zoom of 119 % reaches the critical print size there.

---

## 5. Floors: size × weight

A stroke narrower than one pixel is drawn as a partly covered pixel, so on a 1x screen it is lighter than its color: the contrast of the text drops below the contrast the color guarantees. A counter (the white inside e, a, s, B, g, 8, m, n, H) narrower than one pixel fills in. The floor of a weight is the smallest whole pixel size at which its lowercase stems and its narrowest counter are both at least one pixel. It is measured on the outlines, unhinted, at 1x, the worst case.

<!-- generated:floors -->
| Weight | Stem | Narrowest counter | Floor, upright | Floor, italic | Mono, upright | Mono, italic |
| --- | --- | --- | --- | --- | --- | --- |
| ExtraLight (200) | 0.054 em | 0.141 em (g) | 19 px | 19 px | 19 px | 19 px |
| Light (300) | 0.067 em | 0.135 em (g) | 15 px | 16 px | 15 px | 15 px |
| Regular (400) | 0.084 em | 0.128 em (g) | **12 px** | 13 px | 12 px | 12 px |
| Medium (500) | 0.106 em | 0.121 em (s) | 10 px | 10 px | 10 px | 10 px |
| SemiBold (600) | 0.122 em | 0.109 em (s) | 10 px | 9 px | 10 px | 10 px |
| Bold (700) | 0.139 em | 0.096 em (s) | 11 px | 11 px | 11 px | 11 px |
| ExtraBold (800) | 0.165 em | 0.077 em (s) | 13 px | 13 px | 14 px | 14 px |
<!-- /generated -->

Stems and counters are those of upright Twilight Crystal; the other styles differ by at most 0.006 em. Italic glyphs are uprighted by their angle before their counters are measured, and stems are measured across, as the pixel rows meet them, so a slanted stem counts at its horizontal width. Twilight Crystal Italic's stem, 0.083 em, falls just short of one pixel at 12 px, which puts its floor at 13. Mono's narrowest counter in the heavier weights is m, compressed into one cell, which raises its ExtraBold floor to 14 px.

Light weights are limited by their stems and heavy weights by their counters, so the floors are lowest in the middle of the range. From each floor to 20 px, the confusable pairs I-l, l-1, I-1, O-0, rn-m and cl-d stay apart: their worst pixel distinction, hinted or not, is 0.21 or more in Twilight Crystal and 0.14 or more in Mono (the metric of `fonts/scripts/hintcheck.py`; 0 would be identical).

Documents are read on screens at 100 % zoom, where a point is 4/3 px, so their floors are the pixel floors in points: 9 pt for Regular. Slides have no pixels to measure, so their floor is an angle: the x-height of the Regular floor on a desktop screen, 12 px, subtends 0.1269°, which is 2.68 % of the slide height. On a handheld screen the same angle gives 10 px, under the pixel floor of 12 px, which stays. On slides, a weight whose pixel floor is f px has the floor of Regular multiplied by f / 12.

The **lowest step** of a style is the smallest step of the scale (§6) that is at or above its floor in every geometry:

<!-- generated:lowest-steps -->
| Weight | Twilight Crystal | Italic | Twilight Crystal Mono | Mono italic |
| --- | --- | --- | --- | --- |
| ExtraLight | 2 | 2 | 2 | 2 |
| Light | 0 | 0 | 0 | 0 |
| Regular | −2 | −1 | −2 | −2 |
| Medium | −2 | −2 | −2 | −2 |
| SemiBold | −2 | −2 | −2 | −2 |
| Bold | −2 | −2 | −2 | −2 |
| ExtraBold | −1 | −1 | 0 | 0 |
<!-- /generated -->

---

## 6. Scale

Step 0 is running text (§4). Step −2, the smallest step, sits on the Regular floor (§5), because any text may be set in Regular. With steps spaced by a constant ratio, these two sizes fix it:

ratio = √(running text size / floor)

This is the largest ratio, so the strongest hierarchy, whose smallest step is still legible. Each geometry has its own:

<!-- generated:scale-by-geometry -->
| Step | −2 | −1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Desktop, ratio 1.2583 (px) | 12 | 15.10 | 19 | 23.91 | 30.08 | 37.85 | 47.63 | 59.94 | 75.42 | 94.90 |
| Handheld, ratio 1.1547 (px) | 12 | 13.86 | 16 | 18.48 | 21.33 | 24.63 | 28.44 | 32.84 | 37.93 | 43.79 |
| Documents, ratio 1.1547 (pt) | 9 | 10.39 | 12 | 13.86 | 16 | 18.48 | 21.33 | 24.63 | 28.44 | 32.84 |
| Slides, ratio 1.2563 (% of height) | 2.68 | 3.37 | 4.23 | 5.31 | 6.68 | 8.39 | 10.54 | 13.24 | 16.63 | 20.90 |
<!-- /generated -->

Adjacent steps differ in x-height by at least 1.54 device pixels on a desktop screen and 1.84 on a handheld one (at 2 device pixels per CSS pixel or more), so no two steps render alike. Documents are the handheld scale in points: 12 pt is 16 px and 9 pt is 12 px. On slides the ratio differs from that of text read from a distance, <!-- fact:t.distance.ratio -->1.2556<!-- /fact --> (§3), only by rounding.

---

## 7. Upper bounds

- **Fluent range.** Reading speed falls when the x-height passes about 2°. On a desktop screen that is 189 px, about twice step 7, so every step reads at full speed.
- **Narrowest screen.** WCAG 1.4.10 requires content to fit 320 CSS px without horizontal scrolling. The widest word of the corpus (§9), *desconocimiento*, is 7.94 em wide in Bold. With 16 px gutters it fits 320 px up to 36.25 px. Handheld steps 6 and 7 (37.93 and 43.79 px) do not fit, so the largest sizes need a bound that depends on the width W of the viewport:

  size ≤ (W − 32 px) / 7.94

---

## 8. Line height

| Text | Line height | Basis |
|---|---|---|
| Running text | at least 1.5 | WCAG 1.4.8 |
| Code and terminals | 1.3 | The font's natural line: box drawing, block elements and Powerline separators fill the line, so they join with the next line without a gap only at this height |
| Anything, lower bound | above 1.153 (Twilight Crystal), 1.129 (Mono) | Below these, an accented letter of one line can touch a descender of the line above |

---

## 9. Measure

WCAG 1.4.8 limits running text to 80 characters per line. The CSS unit `ch` is the width of the zero, which in Twilight Crystal is wider than an average character, so 80ch would hold about 120 characters. The measure is therefore counted on real text: the mean advance of a character, spaces and punctuation included, in the Universal Declaration of Human Rights, shaped with kerning in Regular.

<!-- generated:measure -->
| Language | Mean character | 80 characters |
| --- | --- | --- |
| English | 0.433 em | 34.6 em |
| Spanish | 0.440 em | 35.2 em |
<!-- /generated -->

The narrower language sets the limit: **<!-- fact:t.measure.em -->34.6 em<!-- /fact -->**, which is 53.4ch. At the handheld size on a 320 px screen, a line holds about 41 characters.

---

## 10. Code in editors and terminals

Code is set by the reader in an editor or a terminal, for hours at a time, and needs many columns, so it does not take step 0 of the desktop scale (19 px). Terminals round the cell to whole pixels, and editors at 1x draw on them, so a size whose x-height (0.496 em), cell (0.632 em) and line (1.3 em) fall between pixels renders uneven columns or blurred letters. The largest of the three roundings, from the Mono floor to desktop running text:

<!-- generated:code-grid -->
| Size (px) | 12 | 13 | **14** | 15 | **16** | 17 | 18 | 19 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Largest rounding | 5.5 % | 7.0 % | **1.7 %** | 5.9 % | **1.1 %** | 5.1 % | 3.3 % | 4.5 % |
<!-- /generated -->

- **Minimum, <!-- fact:t.code.minimum -->14 px<!-- /fact -->.** The smallest size at which all three land within 2 % of whole pixels: an x-height of 6.94 px, a cell of 8.85 px and a line of 18.2 px, next to 7, 9 and 18. Its x-height is at least that of code in the default editor on Windows and macOS.
- **Optimal, <!-- fact:t.code.optimal -->16 px<!-- /fact -->.** The size, from the x-height of the default editor on every system up to running text, whose grid lands closest to whole pixels. The defaults it is measured against:

<!-- generated:editor-defaults -->
| System | Default | x-height of the font | x-height |
| --- | --- | --- | --- |
| Windows | Consolas, 14 px | 0.490 em | 6.86 px |
| macOS | Menlo, 12 px | 0.547 em | 6.56 px |
| Linux | Droid Sans Mono, 14 px | 0.536 em | 7.51 px |
<!-- /generated -->

  Twilight Crystal Mono reaches the largest of these x-heights, 7.51 px, at 15.13 px. At 16 px its x-height, cell and line are 7.94, 10.11 and 20.8 px, all within 1.1 % of 8, 10 and 21: the cleanest grid of any size from the floor to running text. It is also the browser default and the size of running text in documents.

Both meet the rules. <!-- fact:t.code.minimum -->14 px<!-- /fact --> is the usual size; <!-- fact:t.code.optimal -->16 px<!-- /fact --> reduces fatigue over long sessions and suits anyone who prefers larger text.

---

## 11. Parameters: Decided vs derived

### Decided (with sources)

| Parameter | Value | Source |
|---|---|---|
| Critical print size | 0.2° of x-height | Legge and Bigelow, [Does print size matter for reading?](https://legge.dl8.umn.edu/sites/legge.psych.umn.edu/files/2020-08/Legge%20Bigelow%202011%20Does%20size%20matter%20for%20reading%3F%20A%20review%20of%20findings%20from%20vision%20science%20and%20typography.pdf), Journal of Vision, 2011 |
| Top of the fluent range | 2° of x-height | The same |
| Desktop pixel | 0.02132° | [CSS Values 4, the reference pixel](https://www.w3.org/TR/css-values-4/#reference-pixel) |
| Handheld pixel | 1/160 inch at 32 cm | Bababekova et al., Font size and viewing distance of handheld smart phones, Optometry and Vision Science, 2011 (web pages read at 32 cm on average) |
| Paper distance | 40 cm | Legge and Bigelow, as above |
| Document size | 12 pt | [APA Style, font](https://apastyle.apa.org/style-grammar-guidelines/paper-format/font): 12-point Aptos or Times New Roman |
| Slide distance | 6 slide heights | The 4/6/8 rule of audiovisual design: 6 image heights is the farthest viewer for content that must be read |
| Handheld density | at least 2 device pixels per CSS pixel | Checked only for the spacing of steps (§6); floors are taken at 1x |
| Default size | 16 px | The default font size of browsers; running text on screens is never smaller |
| Floor criterion | stems and counters at least 1 px, at 1x; on slides, the angle of the Regular floor on a desktop screen | Text keeps the contrast its color guarantees |
| Code grid tolerance | 2 % | The minimum code size: x-height, cell and line within 2 % of whole pixels |
| Editor defaults | §10 | The default font and size of the most used code editor on each system; x-heights measured on the fonts as each system installs them |
| Line height of running text | 1.5 | [WCAG 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation) |
| Measure | 80 characters | WCAG 1.4.8 |
| Narrowest viewport | 320 CSS px | [WCAG 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow) |
| Gutter | 16 px each side | The same as the default size |
| Corpus | Universal Declaration of Human Rights, English and Spanish | NLTK data, pinned by SHA-256 in `typography.py` |

### Derived (everything else)

Running text sizes on screens and slides (§4), floors (§5), scale ratios and steps (§6), the width bound (§7), the touching line heights and the code line height (§8), the measure (§9) and the minimum and optimal sizes of code (§10).

---

## 12. Reproducing

Build the fonts (`fonts/scripts/build.py`), then run `python fonts/scripts/typography.py`, or add `--json` for every number above in machine-readable form. The corpus is downloaded once and verified against its SHA-256.
