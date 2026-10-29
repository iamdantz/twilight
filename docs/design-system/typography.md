# Twilight Theme design system: typography

Version 1.2 · Fonts: Twilight Crystal (sans), Twilight Crystal Mono (mono)

This document defines how Twilight Theme sets text: which fonts, at which sizes, weights and line heights, with what spacing and line length. The rules do not depend on the medium. They apply wherever type can be set: web pages and applications, documents, slides, images, editors and terminals. Each format reads the same rules in its own unit, and §5 says which values a format takes.

The fonts themselves, what they add and how to install them, are described in [fonts/README.md](../../fonts/README.md). How every number below was derived is in [construction/typography.md](../construction/typography.md). All values in machine-readable form are in [typography/twilight.json](../../typography/twilight.json). The colors of Twilight Theme do not depend on any font: every guarantee in [color.md](color.md) holds whatever font the text is set in, and at every size these rules allow.

## Contents

1. [Which font to use](#1-which-font-to-use)
2. [System fonts](#2-system-fonts)
3. [Names](#3-names)
4. [Fonts](#4-fonts)
5. [Geometries](#5-geometries)
6. [Scale](#6-scale)
7. [Levels](#7-levels)
8. [Weights and styles](#8-weights-and-styles)
9. [Leading and spacing](#9-leading-and-spacing)
10. [Line length and alignment](#10-line-length-and-alignment)
11. [Figures](#11-figures)
12. [UI text and prose](#12-ui-text-and-prose)
13. [Changing the size of a level](#13-changing-the-size-of-a-level)
14. [Fitting the column](#14-fitting-the-column)
15. [Setting up tools](#15-setting-up-tools)
16. [How not to apply](#16-how-not-to-apply)

## 1. Which font to use

Twilight Theme encourages Twilight Crystal, and names the alternatives in order. The user's taste has the last word: any face can carry the theme.

1. **Twilight Crystal and Twilight Crystal Mono**, the recommended faces. They draw box drawing, arrows, symbols and Powerline separators in the same strokes as the letters, keep terminal lines on whole pixels, and offer optional ligatures. They are downloaded from the repository's releases and installed by hand.
2. **Atkinson Hyperlegible Next and Atkinson Hyperlegible Mono**, from Google Fonts. Twilight Crystal is a derivative of them: letters, spacing, kerning and features are the same, and `fonts/scripts/check.py` verifies on every build that they shape identically. Use them when Twilight Crystal has an error that affects you (please report it), or for convenience: they load in a web project from Google Fonts with one link and are packaged by Fontsource and Homebrew. What they lack are the [additions of Twilight Crystal](../../fonts/README.md#made-for-terminals), which then come from whatever other font the system has.
3. **The system's own fonts**, last. Twilight Theme does not favor them: they may not reach the same legibility or character. They are the alternative when nothing else is possible, or when installing fonts is not wanted. §2 lists the closest ones on each system and how to size them.

## 2. System fonts

When neither Twilight Crystal nor Atkinson Hyperlegible can be installed, these are the closest faces each system ships by default. They were chosen by measurement among the fonts installed with each system: how close their shapes are to Atkinson Hyperlegible, how well they tell apart I, l, 1 and | (and O and 0 in monospaced faces) at small sizes, and whether they have an italic and a bold. A face whose I and l are the same single stroke was not considered.

<!-- generated:system-fonts -->
| System | Sans-serif | Size | Monospaced | Size | Cell after sizing |
| --- | --- | --- | --- | --- | --- |
| Windows | Tahoma | 91 % | Cascadia Mono | 92 % | 0.54 em |
| macOS | Verdana | 91 % | Menlo | 91 % | 0.55 em |
| Linux, KDE | Noto Sans | 93 % | Hack | 91 % | 0.55 em |
| Linux, GNOME | Adwaita Sans | 91 % | Adwaita Mono | 95 % | 0.57 em |
| Linux, other | Noto Sans if installed | 93 % | DejaVu Sans Mono | 91 % | 0.55 em |
<!-- /generated -->

**Size** is the size that gives the face Twilight Crystal's x-height, the height of lowercase letters that sets how large text reads. All of these faces have taller lowercase than Atkinson Hyperlegible, so at the same nominal size they look larger; set at the listed fraction (in CSS, the `size-adjust` descriptor of `@font-face`; in an editor, a smaller font size), their lowercase matches Twilight Crystal's, and their capitals land within 1 % of its cap height (within 5 % for Cascadia Mono and Adwaita Mono). In CSS, a single stack tries them in the order Tahoma, Verdana, Adwaita Sans and Noto Sans, then Cascadia Mono, Menlo, Hack, Adwaita Mono and DejaVu Sans Mono, and uses the first one installed. **Cell** is the monospaced advance after that sizing; Twilight Crystal Mono's is 0.632 em, so the same window holds 10 to 17 % more columns.

None of these faces has the [optional ligatures](../../fonts/README.md#optional-ligatures), and only some draw box drawing; Atkinson Hyperlegible Mono has neither.

## 3. Names

Every typographic value has one name, used the same way in these rules, in [typography/twilight.json](../../typography/twilight.json), in CSS and in the styles of other tools. A name is a namespace and a key:

| Namespace | Keys | Example in CSS |
|---|---|---|
| `font` | `sans`, `mono` | `--twl-font-mono` |
| `text` | the steps of the scale, `xs` to `6xl` (§6); the levels, such as `h1` or `body-sm` (§7); `fit` (§14) | `--twl-text-base`, `--twl-text-h2` |
| `leading` | `default` (1.5), `tight` (1.3) | `--twl-leading`, `--twl-leading-tight` |
| `spacing` | one line of body text (§9) | `--twl-spacing` |
| `container` | `prose` (§10) | `--twl-container-prose` |

The steps are named as size modifiers usually are, from `xs` to `6xl`, with `base` for body text. A level is named after the HTML element it styles (`h1` to `h6`) or after its step (`body-lg` is body text one step up, at `lg`). The key `default` is left out of a name: `--twl-leading` is the default leading.

In CSS, every name starts with `twl`, Twilight's consonants, which no common framework uses (Tailwind CSS uses `--tw-` for its own), so the names stay apart from a framework's and a page's.

## 4. Fonts

| Font | Sets |
|---|---|
| `sans`, Twilight Crystal | All text, except literal text |
| `mono`, Twilight Crystal Mono | **Literal text**: what the reader must read or type exactly as written. Code, commands, file names and paths, keys and shortcuts, identifiers, values to copy (versions, hashes, tokens), and everything in editors and terminals |

Twilight Crystal Mono marks text as literal, so it is used for nothing else: not for headings, labels, numbers in tables (they take tabular figures, §11) or to make text look technical.

Literal text inside a sentence keeps the size, weight and leading of the text around it. Both fonts have the same x-height and cap height, so it matches with no change of size.

The optional ligatures of Twilight Crystal Mono are for editors and terminals, where the user turns them on. Literal text in prose, interfaces and slides is set without them, so a reader copying it sees every character.

## 5. Geometries

The size text needs depends on how far it is read from and on what. Every format belongs to one of four **geometries**, and takes the values of that geometry:

| Geometry | Formats | Unit | `base` |
|---|---|---|---|
| `desktop` | Web pages and applications on computers | CSS pixel (px) | <!-- fact:t.desktop.base -->19 px<!-- /fact --> |
| `handheld` | Web pages and applications on phones and tablets | CSS pixel, the same as a point on iOS and a density-independent pixel on Android | <!-- fact:t.handheld.base -->16 px<!-- /fact --> |
| `page` | Word processors, PDFs, anything printed and held in the hand, whether read on paper or on screen | Point (pt); at 100 % zoom, 1 pt = 4/3 px | <!-- fact:t.page.base -->12 pt<!-- /fact --> |
| `slide` | Presentations shown to a room | Percentage of the slide's height | <!-- fact:t.slide.base -->4.23 %<!-- /fact --> |

Which geometry a format takes:

- **Web.** The primary pointer decides: a coarse pointer (touch) is `handheld`, a fine one (mouse, trackpad) `desktop`. Printing a page uses `page`. The width of the window does not decide it, since a phone held sideways and a narrow window on a computer can be equally wide.
- **Applications.** The device: phones and tablets are `handheld`, computers `desktop`.
- **Documents.** Always `page`, whatever paper they are printed on or screen they are read on. Its 12 pt is the body size style guides give, and 1.5 times the size text needs on a page held at 40 cm. On a computer screen it reaches the size of desktop body text at a zoom of <!-- fact:t.page.zoom -->119 %<!-- /fact -->.
- **Slides.** `slide`, projected or not. Its values also meet `desktop` whenever the slide is at least <!-- fact:t.slide.desktop -->450 px<!-- /fact --> high, so a deck read on a computer needs no other sizes.
- **Text read from farther than arm's length** (posters, signs, displays), when the farthest reading distance D is known: `base` is <!-- fact:t.distance.base -->0.704 %<!-- /fact --> of D, and each step is <!-- fact:t.distance.ratio -->1.2556<!-- /fact --> times the one below, down to `xs`. From 2 m, `base` is <!-- fact:t.distance.2m -->14.1 mm, 40 pt<!-- /fact -->.
- **Images** (graphics, posts, thumbnails) take the geometry of the screen they are shown on, at the size they are shown: a value in the image's pixels is the step × the image's width ÷ the width it is displayed at.

## 6. Scale

All text takes its size from one scale of ten steps. `base` is body text, `xs` the smallest text, and each step is the one below it times a constant ratio. Sizes between steps are not used.

<!-- generated:scale -->
| Step | Desktop (px) | Desktop (rem) | Handheld (px) | Handheld (rem) | Page (pt) | Slide (% of height) |
| --- | --- | --- | --- | --- | --- | --- |
| `6xl` | 94.90 | 5.9311 | 43.79 | 2.7371 | 32.84 | 20.90 |
| `5xl` | 75.42 | 4.7136 | 37.93 | 2.3704 | 28.44 | 16.63 |
| `4xl` | 59.94 | 3.746 | 32.84 | 2.0528 | 24.63 | 13.24 |
| `3xl` | 47.63 | 2.977 | 28.44 | 1.7778 | 21.33 | 10.54 |
| `2xl` | 37.85 | 2.3659 | 24.63 | 1.5396 | 18.48 | 8.39 |
| `xl` | 30.08 | 1.8802 | 21.33 | 1.3333 | 16 | 6.68 |
| `lg` | 23.91 | 1.4942 | 18.48 | 1.1547 | 13.86 | 5.31 |
| **`base`** | **19** | **1.1875** | **16** | **1** | **12** | **4.23** |
| `sm` | 15.10 | 0.9437 | 13.86 | 0.866 | 10.39 | 3.37 |
| `xs` | 12 | 0.75 | 12 | 0.75 | 9 | 2.68 |
| Ratio | 1.2583 |  | 1.1547 |  | 1.1547 | 1.2563 |
<!-- /generated -->

`base` is the smallest size at which body text reads at full speed in that geometry, and on screens it is never less than the reader's default size; on `page` it is <!-- fact:t.page.base -->12 pt<!-- /fact -->. `xs` is the smallest size at which Regular text keeps strokes and counters of at least one pixel. The ratio is the largest that keeps `xs` there.

On the web, sizes are set in rem, so the whole scale follows the size the reader chose in the browser. Where a tool does not take the exact value, round up to the nearest value it takes; §15 lists them for common tools.

## 7. Levels

A **level** is a kind of text. Each has one step, weight and leading, the same in every geometry:

<!-- generated:levels -->
| Level | Use | Step | Weight | Leading | Font |
| --- | --- | --- | --- | --- | --- |
| `display-1` | The one title of a page, a cover or a slide | `6xl` | Regular, or any weight (§8) | `tight` (1.3) | `sans` |
| `display-2` | The same, one step down | `5xl` | Regular, or any weight (§8) | `tight` (1.3) | `sans` |
| `h1` | Headings, by structure | `4xl` | Bold | `tight` (1.3) | `sans` |
| `h2` |  | `3xl` | Bold | `tight` (1.3) | `sans` |
| `h3` |  | `2xl` | Bold | `tight` (1.3) | `sans` |
| `h4` |  | `xl` | Bold | `tight` (1.3) | `sans` |
| `h5` |  | `lg` | Bold | `tight` (1.3) | `sans` |
| `h6` |  | `base` | Bold | `tight` (1.3) | `sans` |
| `body-lg` | The opening paragraph of prose | `lg` | Regular | `default` (1.5) | `sans` |
| `body` | Paragraphs, lists, quotes | `base` | Regular | `default` (1.5) | `sans` |
| `ui` | Controls, labels, menus, tabs, table cells, messages; default leading when it wraps | `base` | Regular | `tight` (1.3) | `sans` |
| `body-sm` | Captions, help text, metadata, secondary labels | `sm` | Regular | `default` (1.5) | `sans` |
| `body-xs` | Timestamps, counts, badges, notes | `xs` | Regular | `default` (1.5) | `sans` |
| `code` | Code blocks in prose, pages and slides | `base` | Regular | `tight` (1.3) | `mono` |
<!-- /generated -->

- **Body text is never set below `base`.** `body-sm` and `body-xs` carry short text: a label, a caption or a note of one sentence at most. Anything longer is `body`.
- **Emphasis** is italic, **strong emphasis** Bold. `body-xs` has no italic (§8).
- **Literal text in a sentence** takes the sentence's level, in `mono`.
- **Code editors and terminals** are not a level and have no name: their font size is a setting of the application, chosen by its user. These rules give two sizes for it. <!-- fact:t.editors.size -->14 px<!-- /fact --> (<!-- fact:t.editors.size-pt -->10.5 pt<!-- /fact -->) is the smallest at which the Mono grid (x-height, cell and line) lands on whole pixels; it is the usual size and meets the rules. <!-- fact:t.editors.size-lg -->16 px<!-- /fact --> (<!-- fact:t.editors.size-lg-pt -->12 pt<!-- /fact -->) is at least as large as code in the default editor of every system, on the cleanest grid of all, and less tiring over long sessions, for anyone who prefers larger text. Line height is 1.3, the font's own line, in both.
- `display-1` and `display-2` are for the one title of a page, a cover or a slide, and no more than one per view.

## 8. Weights and styles

Each weight and style has a lowest step, below which its strokes or counters drop under a pixel and the text shows less contrast than its color guarantees. It holds in every geometry:

<!-- generated:lowest-steps -->
| Weight | Sans | Sans italic | Mono | Mono italic |
| --- | --- | --- | --- | --- |
| ExtraLight | `xl` | `xl` | `xl` | `xl` |
| Light | `base` | `base` | `base` | `base` |
| Regular | `xs` | `sm` | `xs` | `xs` |
| Medium | `xs` | `xs` | `xs` | `xs` |
| SemiBold | `xs` | `xs` | `xs` | `xs` |
| Bold | `xs` | `xs` | `xs` | `xs` |
| ExtraBold | `sm` | `sm` | `base` | `base` |
<!-- /generated -->

The levels of §7 use Regular and Bold, and italic from `sm` up. The other weights are for `display-1` and `display-2`, where every weight is above its lowest step; which one is a matter of taste.

## 9. Leading and spacing

**Leading** is the line height, a multiple of the size of the text:

- **`default`, 1.5**, for body text and for any text that wraps to more than one line (WCAG 1.4.8).
- **`tight`, 1.3**, for headings, display, one-line UI text, code, editors and terminals. It is the fonts' own line: box drawing and blocks in a terminal join from one line to the next only at this height.
- Nothing below `tight`. Below <!-- fact:t.touching -->1.153<!-- /fact --> an accent can touch the line above.

**Spacing** between blocks is counted in lines of body text, `base` × 1.5: <!-- fact:t.desktop.spacing -->28.5 px<!-- /fact --> on `desktop`, <!-- fact:t.handheld.spacing -->24 px<!-- /fact --> on `handheld`, <!-- fact:t.page.spacing -->18 pt<!-- /fact --> on `page` and <!-- fact:t.slide.spacing -->6.35 %<!-- /fact --> of the slide's height on `slide`.

| Between | Space |
|---|---|
| Paragraphs, and around lists, tables, figures, quotes and code blocks | 1 line |
| Items of a list | none; half a line when an item has more than one paragraph |
| Before a heading | 2 lines |
| After a heading | half a line |
| Inside UI components | set by the layout, not by these rules |

A heading sits closer to the text it introduces than to the text before it. One line between paragraphs puts their baselines 2 lines apart, more than the 1.5 WCAG 1.4.8 asks for.

**Tracking** (letter spacing) is 0 everywhere: the fonts' own spacing and kerning are kept, at every size, in capitals as well. Text is not set in capitals as a style; acronyms keep their capitals.

Layouts must not break when a reader raises line height to 1.5, paragraph spacing to 2 × the size, letter spacing to 0.12 × and word spacing to 0.16 × the size (WCAG 1.4.12): containers of text grow with it and do not clip it.

## 10. Line length and alignment

- **A line of body text is at most <!-- fact:t.prose.em -->34.6 em<!-- /fact --> long**, the `prose` container, which holds <!-- fact:t.prose.characters -->80<!-- /fact --> characters (WCAG 1.4.8): <!-- fact:t.desktop.prose -->657 px<!-- /fact --> on `desktop`, <!-- fact:t.handheld.prose -->554 px<!-- /fact --> on `handheld` (wider than a phone held upright, so there it binds only on tablets and phones held sideways), <!-- fact:t.page.prose -->415 pt<!-- /fact --> (<!-- fact:t.page.prose-cm -->14.6 cm<!-- /fact -->) on `page`. A Letter or A4 page with the usual 2.5 cm margins has a wider text block, so its margins grow, or the text is set in two columns. On the web it is set in em, not in ch: the `ch` unit is the width of the zero, wider than an average character in Twilight Crystal, and 80ch holds about 120 characters.
- Body text is aligned to the start of the line (left, in left-to-right languages) and never justified (WCAG 1.4.8). Words are not hyphenated.
- Headings, display and one-line labels may be centered; body text is not.

## 11. Figures

Twilight Crystal draws proportional figures by default and has tabular figures (OpenType `tnum`), each exactly one Twilight Crystal Mono cell wide.

- **Tabular**: tables, columns of numbers, times, prices, counters, and any number that changes in place, so digits line up and nothing shifts.
- **Proportional**: numbers inside body text.

Twilight Crystal Mono figures are always tabular.

## 12. UI text and prose

Every text is one or the other, and both follow §4 to §11.

- **Prose** is read in sequence: articles, documentation, messages, posts, reports, help pages. It flows: the spacing of §9 separates its blocks, its lines fit the `prose` container of §10, links in it are underlined ([color.md §5](color.md#where-the-accent-goes)), and lists show their markers. On the web, the page applies this spacing to its prose with `--twl-spacing` and `--twl-container-prose`; [Remix](../../remix/README.md), like every CSS reset, leaves the space between elements at zero.
- **UI text** names, labels or reports on something on screen: buttons, fields, menus, tabs, navigation, table cells, cards, notifications. It is set at `ui`, `body-sm` or `body-xs`, in one line where possible; the layout decides its spacing, and links in it are identified by their place or an icon rather than an underline.

Text inside an interface that is read in sequence, such as the body of a message or an empty state that explains something, is prose.

## 13. Changing the size of a level

A level may move to another step, never between steps, and keeps its weight, leading, font and place in the structure. A page title stays `h1` when it is shown at the size of `display-2`; a heading in a narrow sidebar stays `h2` at `xl`. Body text does not move below `base`, and no style moves below its lowest step (§8).

## 14. Fitting the column

No word may run past its column. The widest common words, in Bold, are <!-- fact:t.fit.em -->7.94<!-- /fact --> em wide, so a step fits a column if

size ≤ column width ÷ <!-- fact:t.fit.em -->7.94<!-- /fact -->

A level whose step does not fit is reduced to that bound, `fit`. It affects only the largest steps on narrow columns: on a 320 px screen with 16 px margins, `fit` is <!-- fact:t.fit.narrowest -->36.27 px<!-- /fact -->, under `5xl` and `6xl` on `handheld`. On the web it is written `min(step, (100vw − 2rem) / 7.94)`.

## 15. Setting up tools

Where a tool does not take the exact value, round up to the nearest value it takes.

| Tool | Unit and values |
|---|---|
| Web | Sizes in rem from §6: `desktop` unless the primary pointer is coarse (`@media (pointer: coarse)`), `page` in `@media print`. [Remix](../../remix/README.md), the CSS reset, applies the rules for elements, with the names of §3 |
| iOS, Android | `handheld`: pt on iOS, sp on Android, equal to the px of §6 |
| Figma, Photoshop, Illustrator | px of the geometry where the design will be shown; in a 72 ppi document, 1 pt = 1 px |
| Code editors and terminals | In the application's settings: font size <!-- fact:t.editors.size -->14 px<!-- /fact -->, or <!-- fact:t.editors.size-lg -->16 px<!-- /fact --> to reduce fatigue (<!-- fact:t.editors.size-pt -->10.5 pt<!-- /fact --> or <!-- fact:t.editors.size-lg-pt -->12 pt<!-- /fact --> in applications sized in points); line height 1.3 |

Documents and slides take the steps in points, rounded up to what each tool accepts:

<!-- generated:tool-values -->
| Tool | `xs` | `sm` | `base` | `lg` | `xl` | `2xl` | `3xl` | `4xl` | `5xl` | `6xl` | Unit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Word, Google Docs, Pages, PDFs | 9 | 10.5 | 12 | 14 | 16 | 18.5 | 21.5 | 25 | 28.5 | 33 | pt |
| PowerPoint, 16:9 (7.5 in high) | 14.5 | 18.5 | 23 | 29 | 36.5 | 45.5 | 57 | 71.5 | 90 | 113 | pt |
| Google Slides, 16:9 (5.625 in high) | 11 | 14 | 17.5 | 22 | 27.5 | 34 | 43 | 54 | 67.5 | 85 | pt |
| Keynote, 1920 × 1080 | 29 | 37 | 46 | 58 | 73 | 91 | 114 | 143 | 180 | 226 | pt |
<!-- /generated -->

Each level of §7 becomes a named style in tools that have them (paragraph and character styles in documents, text styles in design tools), named as in §3, so text is set by level and never by a size typed by hand.

## 16. How not to apply

| Misuse | What breaks | Instead |
|---|---|---|
| A size between two steps, or a size scaled with the width of the window | Levels stop being distinguishable, and body text can drop under its legible size | A step of §6, chosen by geometry (§5); only `fit` (§14) depends on width |
| Body text below `base`, or a paragraph set in `body-sm` or `body-xs` | It falls below the size at which it reads at full speed | `body`; `body-sm` and `body-xs` for one sentence at most |
| A weight or italic below its lowest step | Strokes or counters fall under a pixel and the text shows less contrast than its color guarantees | §8 |
| Twilight Crystal Mono for headings, labels, numbers or style | Mono stops marking literal text | `sans`; tabular figures for numbers |
| Literal text set smaller than the sentence around it | It drops below the size the sentence needs | The sentence's size; the fonts already match |
| A leading below `tight`, or below `default` for body text | Accents touch, terminals show gaps, WCAG 1.4.8 fails | §9 |
| Tracking, or capitals as a style | The fonts' spacing is lost; capitals read slower | Tracking 0; the case of the language |
| Justified or hyphenated body text | Uneven word spaces; WCAG 1.4.8 | Text aligned to the start |
| A line limit of 80ch | About 120 characters per line | The `prose` container, <!-- fact:t.prose.em -->34.6 em<!-- /fact --> |
| Proportional figures in tables or changing values | Columns do not line up; numbers shift | Tabular figures |
| Spacing in arbitrary amounts | Rhythm is lost | Lines and half lines (§9) |
| `display-1` or `display-2` for section titles, or more than one per view | It stops marking the one title | Headings |
| A heading skipped or chosen for its size | The structure no longer matches what is shown | The level by structure, its size changed by §13 |
| Names of other schemes (`--twilight-…`, a step called "small") | The vocabulary splits | The names of §3 |
