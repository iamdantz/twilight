# Twilight Theme design system: typography

Version 1.1 · Typefaces: Twilight Crystal (sans-serif), Twilight Crystal Mono (monospaced)

This document defines how Twilight Theme sets text: which typefaces, at which sizes, weights and line heights, with what spacing and line length. The rules do not depend on the medium. They apply wherever type can be set: web pages and applications, documents, slides, images, editors and terminals. Each format reads the same rules in its own unit, and §4 says which values a format takes.

The typefaces themselves, what they add and how to install them, are described in [fonts/README.md](../../fonts/README.md). How every number below was derived is in [construction/typography.md](../construction/typography.md). The colors of Twilight Theme do not depend on any font: every guarantee in [color.md](color.md) holds whatever face the text is set in, and at every size these rules allow.

## Contents

1. [Which font to use](#1-which-font-to-use)
2. [System fonts](#2-system-fonts)
3. [Families](#3-families)
4. [Formats](#4-formats)
5. [Scale](#5-scale)
6. [Levels](#6-levels)
7. [Weights and styles](#7-weights-and-styles)
8. [Line height and spacing](#8-line-height-and-spacing)
9. [Line length and alignment](#9-line-length-and-alignment)
10. [Figures](#10-figures)
11. [Interface text and document text](#11-interface-text-and-document-text)
12. [Changing the size of a level](#12-changing-the-size-of-a-level)
13. [Fitting the column](#13-fitting-the-column)
14. [Setting up tools](#14-setting-up-tools)
15. [How not to apply](#15-how-not-to-apply)

## 1. Which font to use

Twilight Theme encourages Twilight Crystal, and names the alternatives in order. The user's taste has the last word: any face can carry the theme.

1. **Twilight Crystal and Twilight Crystal Mono**, the recommended faces. They draw box drawing, arrows, symbols and Powerline separators in the same strokes as the letters, keep terminal lines on whole pixels, and offer optional ligatures. They are downloaded from the repository's releases and installed by hand.
2. **Atkinson Hyperlegible Next and Atkinson Hyperlegible Mono**, from Google Fonts. Twilight Crystal is a derivative of them: letters, spacing, kerning and features are the same, and `fonts/scripts/check.py` verifies on every build that they shape identically. Use them when Twilight Crystal has an error that affects you (please report it), or for convenience: they load in a web project from Google Fonts with one link and are packaged by Fontsource and Homebrew. What they lack are the [additions of Twilight Crystal](../../fonts/README.md#made-for-terminals), which then come from whatever other font the system has.
3. **The system's own fonts**, last. Twilight Theme does not favor them: they may not reach the same legibility or character. They are the alternative when nothing else is possible, or when installing fonts is not wanted. §2 lists the closest ones on each system and how to size them.

## 2. System fonts

When neither Twilight Crystal nor Atkinson Hyperlegible can be installed, these are the closest faces each system ships by default. They were chosen by measurement among the fonts installed with each system: how close their shapes are to Atkinson Hyperlegible, how well they tell apart I, l, 1 and | (and O and 0 in monospaced faces) at small sizes, and whether they have an italic and a bold. A face whose I and l are the same single stroke was not considered.

| System | Sans-serif | Size | Monospaced | Size | Cell after sizing |
| --- | --- | --- | --- | --- | --- |
| Windows | Tahoma | 91 % | Cascadia Mono | 92 % | 0.54 em |
| macOS | Verdana | 91 % | Menlo | 91 % | 0.55 em |
| Linux, KDE | Noto Sans | 93 % | Hack | 91 % | 0.55 em |
| Linux, GNOME | Adwaita Sans | 91 % | Adwaita Mono | 95 % | 0.57 em |
| Linux, other | Noto Sans if installed | 93 % | DejaVu Sans Mono | 91 % | 0.55 em |

**Size** is the size that gives the face Twilight Crystal's x-height, the height of lowercase letters that sets how large text reads. All of these faces have taller lowercase than Atkinson Hyperlegible, so at the same nominal size they look larger; set at the listed fraction (in CSS, the `size-adjust` descriptor of `@font-face`; in an editor, a smaller font size), their lowercase matches Twilight Crystal's, and their capitals land within 1 % of its cap height (within 5 % for Cascadia Mono and Adwaita Mono). **Cell** is the monospaced advance after that sizing; Twilight Crystal Mono's is 0.632 em, so the same window holds 10 to 17 % more columns.

None of these faces has the [optional ligatures](../../fonts/README.md#optional-ligatures), and only some draw box drawing; Atkinson Hyperlegible Mono has neither.

## 3. Families

| Family | Sets |
|---|---|
| Twilight Crystal | All text, except literal text |
| Twilight Crystal Mono | **Literal text**: what the reader must read or type exactly as written. Code, commands, file names and paths, keys and shortcuts, identifiers, values to copy (versions, hashes, tokens), and everything in editors and terminals |

Twilight Crystal Mono marks text as literal, so it is never used for anything else: not for headings, labels, numbers in tables (they take tabular figures, §10) or to make text look technical.

Literal text inside a sentence keeps the size, weight and line height of the text around it. Both families have the same x-height and cap height, so it matches with no change of size.

The optional ligatures of Twilight Crystal Mono are for editors and terminals, where the user turns them on. Literal text in documents, interfaces and slides is set without them, so a reader copying it sees every character.

## 4. Formats

The size text needs depends on how far it is read from and on what. Every format belongs to one of four **geometries**, and takes the values of that geometry:

| Geometry | Formats | Unit | Running text |
|---|---|---|---|
| Desktop screen | Web pages and applications on computers; documents and PDFs read on a computer; editors and terminals | CSS pixel (px). In documents at 100 % zoom, 1 pt = 4/3 px | 19 px |
| Handheld screen | Web pages and applications on phones and tablets | CSS pixel, the same as a point on iOS and a density-independent pixel on Android | 16 px |
| Print | Anything printed and read in the hand | Point (pt) | 8 pt |
| Slides | Presentations shown to a room | Percentage of the slide's height | 4.23 % |

Which geometry a format takes:

- **Web.** The primary pointer: a coarse pointer (touch) is a handheld screen, a fine one (mouse, trackpad) a desktop screen. Printing a page uses print. The width of the window does not decide it: a phone held sideways and a narrow window on a computer can be equally wide.
- **Applications.** The device: phones and tablets are handheld; computers are desktop.
- **Documents.** Where they will be read. A document read both on screen and on paper takes the desktop values, which are larger and meet both.
- **Slides.** Slides take the slides geometry, projected or not. Its values also meet the desktop screen whenever the slide is at least 450 px high, so a deck read on a computer needs no other sizes.
- **Images** (graphics, posts, thumbnails) take the geometry of the screen they are shown on, at the size they are shown: a value in the image's pixels is the step × the image's width ÷ the width it is displayed at.

## 5. Scale

All text takes its size from one scale of ten steps, from −2 to 7. Step 0 is running text, step −2 the smallest text, and every step is the one below it times a constant ratio. Sizes between steps are not used.

| Step | Desktop (px) | Desktop (rem) | Handheld (px) | Handheld (rem) | Print (pt) | Slides (% of height) |
|---|---|---|---|---|---|---|
| 7 | 94.90 | 5.9311 | 43.79 | 2.7371 | 38.67 | 20.90 |
| 6 | 75.42 | 4.7136 | 37.93 | 2.3704 | 30.88 | 16.63 |
| 5 | 59.94 | 3.7460 | 32.84 | 2.0528 | 24.65 | 13.24 |
| 4 | 47.63 | 2.9770 | 28.44 | 1.7778 | 19.68 | 10.54 |
| 3 | 37.85 | 2.3659 | 24.63 | 1.5396 | 15.72 | 8.39 |
| 2 | 30.08 | 1.8802 | 21.33 | 1.3333 | 12.55 | 6.68 |
| 1 | 23.91 | 1.4942 | 18.48 | 1.1547 | 10.02 | 5.31 |
| **0** | **19** | **1.1875** | **16** | **1** | **8** | **4.23** |
| −1 | 15.10 | 0.9437 | 13.86 | 0.8660 | 6.39 | 3.37 |
| −2 | 12 | 0.75 | 12 | 0.75 | 5.10 | 2.68 |
| Ratio | 1.2583 | | 1.1547 | | 1.2524 | 1.2563 |

Step 0 is the smallest size at which running text reads at full speed in that geometry, and on screens never less than the reader's default size. Step −2 is the smallest size at which Regular text keeps strokes and counters of at least one pixel. The ratio is the largest that keeps step −2 there.

On the web, sizes are set in rem, so the whole scale follows the size the reader chose in the browser. Where a tool does not take the exact value, round up to the nearest value it takes; §14 lists them for common tools.

## 6. Levels

A **level** is a kind of text. Each has one step, weight and line height, the same in every format:

| Level | Step | Weight | Line height | Family |
|---|---|---|---|---|
| Display 1 | 7 | Regular, or any weight (§7) | 1.3 | Crystal |
| Display 2 | 6 | Regular, or any weight (§7) | 1.3 | Crystal |
| Heading 1 | 5 | Bold | 1.3 | Crystal |
| Heading 2 | 4 | Bold | 1.3 | Crystal |
| Heading 3 | 3 | Bold | 1.3 | Crystal |
| Heading 4 | 2 | Bold | 1.3 | Crystal |
| Heading 5 | 1 | Bold | 1.3 | Crystal |
| Heading 6 | 0 | Bold | 1.3 | Crystal |
| Lead (the opening paragraph of a document) | 1 | Regular | 1.5 | Crystal |
| Running text: paragraphs, lists, quotes | 0 | Regular | 1.5 | Crystal |
| Interface text: controls, labels, menus, tabs, table cells, messages | 0 | Regular | 1.3 on one line, 1.5 when it wraps | Crystal |
| Small: captions, help text, metadata, secondary labels | −1 | Regular | 1.5 | Crystal |
| Fine: timestamps, counts, badges, notes | −2 | Regular | 1.5 | Crystal |
| Code blocks, editors, terminals | 0 | Regular | 1.3 | Mono |
| Literal text in a sentence | the sentence's | the sentence's | the sentence's | Mono |

- **Running text is never set below step 0.** Small and Fine carry short text: a label, a caption or a note of one sentence at most. Anything longer is running text.
- **Emphasis** is italic; **strong emphasis** is Bold. Fine text has no italic (§7).
- Display levels are for the one title of a page, a cover or a slide, and no more than one per view.

## 7. Weights and styles

Each weight and style has a lowest step, below which its strokes or counters drop under a pixel and the text loses the contrast its color guarantees. It holds in every format:

| Lowest step | Styles |
|---|---|
| −2 | Regular, Medium, SemiBold and Bold, upright and italic, except Twilight Crystal Italic at Regular weight |
| −1 | Twilight Crystal Italic; Twilight Crystal ExtraBold, upright and italic |
| 0 | Light, upright and italic; Twilight Crystal Mono ExtraBold, upright and italic |
| 2 | ExtraLight, upright and italic |

The levels of §6 use Regular and Bold, and italic from step −1. The other weights are for Display levels, where every weight is above its lowest step; which one is a matter of taste.

## 8. Line height and spacing

**Line height** is a multiple of the size of the text:

- **1.5** for running text and for any text that wraps to more than one line (WCAG 1.4.8).
- **1.3** for headings, Display, one-line interface text, code, editors and terminals. It is the fonts' own line: box drawing and blocks in a terminal join from one line to the next only at this height.
- Nothing below 1.3. Below 1.153 an accent can touch the line above.

**Spacing** between blocks is measured in **lines**, one line being step 0 × 1.5: 28.5 px on desktop screens, 24 px on handheld screens, 12 pt in print and 6.35 % of the slide's height on slides.

| Between | Space |
|---|---|
| Paragraphs, and around lists, tables, figures, quotes and code blocks | 1 line |
| Items of a list | none; half a line when an item has more than one paragraph |
| Before a heading | 2 lines |
| After a heading | half a line |
| Inside interface components | set by the layout, not by these rules |

A heading sits closer to the text it introduces than to the text before it. The space between paragraphs, 1 line, puts their baselines 2 lines apart, more than the 1.5 that WCAG 1.4.8 asks for.

**Letter spacing** is 0 everywhere: the fonts' own spacing and kerning are kept, at every size, in capitals as well. Text is not set in capitals as a style; acronyms keep their capitals.

Layouts must not break when a reader raises line height to 1.5, paragraph spacing to 2 × the size, letter spacing to 0.12 × and word spacing to 0.16 × the size (WCAG 1.4.12): containers of text grow with it and do not clip it.

## 9. Line length and alignment

- **A line of running text is at most 34.6 em long**, which holds 80 characters (WCAG 1.4.8): 657 px on desktop screens, 554 px on handheld screens (wider than a phone held upright, so there it binds only on tablets and phones held sideways), 277 pt in print. On the web, set it in em, not in ch: the `ch` unit is the width of the zero, wider than an average character in Twilight Crystal, and 80ch holds about 120 characters.
- Running text is aligned to the start of the line (left, in left-to-right languages) and never justified (WCAG 1.4.8). Words are not hyphenated.
- Headings, Display and one-line labels may be centered; running text is not.

## 10. Figures

Twilight Crystal draws proportional figures by default and has tabular figures (OpenType `tnum`), each exactly one Twilight Crystal Mono cell wide.

- **Tabular**: tables, columns of numbers, times, prices, counters, and any number that changes in place, so digits line up and nothing shifts.
- **Proportional**: numbers inside running text.

Twilight Crystal Mono figures are always tabular.

## 11. Interface text and document text

Every text is one or the other, and both follow §3 to §10.

- **Document text** is read in sequence: articles, documentation, messages, posts, reports, help pages. It flows: the spacing of §8 separates its blocks, its lines are limited by §9, links in it are underlined ([color.md §5](color.md#where-the-accent-goes)), and lists show their markers.
- **Interface text** names, labels or reports on something on screen: buttons, fields, menus, tabs, navigation, table cells, cards, notifications. It is set at step 0, Small or Fine, in one line where possible; the layout decides its spacing, and links in it are identified by their place or an icon rather than an underline.

A text inside an interface that is read in sequence, such as the body of a message or an empty state that explains something, is document text.

## 12. Changing the size of a level

A level may move to another step, never between steps, and keeps its weight, line height, family and place in the structure. A page title stays Heading 1 when it is shown at Display 2; a heading in a narrow sidebar stays Heading 2 at step 2. Running text does not move below step 0, and no style moves below its lowest step (§7).

## 13. Fitting the column

No word may run past its column. The widest common words, in Bold, are 7.94 em wide, so a step fits a column if

size ≤ column width ÷ 7.94

The size of a level that does not fit is reduced to that bound, which affects only the largest steps on narrow columns: on a 320 px screen with 16 px margins, the bound is 36.25 px, under handheld steps 6 and 7. On the web, a size that spans the page is written `min(step, (100vw − 2rem) / 7.94)`.

## 14. Setting up tools

Where a tool does not take the exact value, round up to the nearest value it takes.

| Tool | Unit and values |
|---|---|
| Web | Sizes in rem from §5; desktop values unless the primary pointer is coarse (`@media (pointer: coarse)`), print values in `@media print` |
| iOS, Android | Handheld values: pt on iOS, sp on Android, equal to the px of §5 |
| Word, Google Docs, Pages (on screen) | Desktop values in pt at 100 % zoom: 9, 11.5, 14.5, 18, 23, 28.5, 36, 45, 57, 71.5 for steps −2 to 7 |
| Word, Google Docs, Pages (printed only) | Print values: 5.5, 6.5, 8, 10.5, 13, 16, 20, 25, 31, 39 |
| PowerPoint, 16:9 (7.5 in high) | 14.5, 18.5, 23, 29, 36.5, 45.5, 57, 71.5, 90, 113 pt |
| Google Slides, 16:9 (5.625 in high) | 11, 14, 17.5, 22, 27.5, 34, 43, 54, 67.5, 85 pt |
| Keynote, 1920 × 1080 | 29, 37, 46, 58, 73, 91, 114, 143, 180, 226 pt |
| Figma, Photoshop, Illustrator | px of the geometry where the design will be shown; in a 72 ppi document, 1 pt = 1 px |
| Editors and terminals | Step 0 of the device in px (19 on a computer) and line height 1.3; in tools sized in points, 14.5 pt |

Each level of §6 becomes a named style in tools that have them (paragraph and character styles in documents, text styles in design tools), so text is set by level and never by a size typed by hand.

## 15. How not to apply

| Misuse | What breaks | Instead |
|---|---|---|
| A size between two steps, or a size scaled with the width of the window | Levels stop being distinguishable, and running text can drop under its legible size | A step of §5, chosen by geometry (§4); only the bound of §13 depends on width |
| Running text below step 0, or a paragraph set in Small or Fine | It falls below the size at which it reads at full speed | Step 0; Small and Fine for one sentence at most |
| A weight or italic below its lowest step | Strokes or counters fall under a pixel and the text shows less contrast than its color guarantees | §7 |
| Twilight Crystal Mono for headings, labels, numbers or style | Mono stops marking literal text | Twilight Crystal; tabular figures for numbers |
| Literal text set smaller than the sentence around it | It drops below the size the sentence needs | The sentence's size; the families already match |
| A line height below 1.3, or below 1.5 for running text | Accents touch, terminals show gaps, WCAG 1.4.8 fails | §8 |
| Letter spacing, or capitals as a style | The fonts' spacing is lost; capitals read slower | Letter spacing 0; the case of the language |
| Justified or hyphenated running text | Uneven word spaces; WCAG 1.4.8 | Text aligned to the start |
| A line limit of 80ch | About 120 characters per line | 34.6 em |
| Proportional figures in tables or changing values | Columns do not line up; numbers shift | Tabular figures |
| Spacing in arbitrary amounts | Rhythm is lost | Lines and half lines (§8) |
| A Display level for section titles, or more than one per view | It stops marking the one title | Headings |
| A heading skipped or chosen for its size | The structure no longer matches what is shown | The level by structure, its size changed by §12 |

