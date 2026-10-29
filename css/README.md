# Twilight Theme CSS reset

A base stylesheet that sets every page in Twilight Theme's typography, whatever CSS framework it uses. It applies [the typography rules](../docs/design-system/typography.md) as browsers read them: the families, the scale of each geometry, the levels, line heights, spacing, line length and figures. It sets no colors.

| File | For |
| --- | --- |
| [`twilight-tailwind.css`](twilight-tailwind.css) | Tailwind CSS 4 and the libraries built on it. Twilight's typography in `@layer base`, after Tailwind's own Preflight |
| [`twilight.css`](twilight.css) | Any other project. Tailwind's Preflight and Twilight's typography, so a page without Tailwind starts from the same base |
| [`twilight.min.css`](twilight.min.css) | The same, minified |

The three files are written by [`build.py`](build.py) from [typography/twilight.json](../typography/twilight.json), and checked against it on every pull request. Do not edit them; change the tokens.

## Use

With Tailwind CSS 4, import it after Tailwind:

```css
@import "tailwindcss";
@import "./twilight-tailwind.css";
```

Anywhere else, link it after the framework's own stylesheet:

```html
<link rel="stylesheet" href="framework.css">
<link rel="stylesheet" href="twilight.css">
```

`twilight.css` is in no cascade layer and styles elements only, so it overrides a framework's styles for bare elements (`body`, `h1`, `code`) and gives way to every class: components and utilities keep their look.

## The fonts

The stylesheet names the fonts; it does not load them. Load Twilight Crystal and Twilight Crystal Mono from the web fonts in a [release](https://github.com/iamdantz/twilight-theme/releases/latest), served next to your stylesheet:

```css
@font-face {
  font-family: "Twilight Crystal";
  src: url("webfonts/TwilightCrystal[wght].woff2") format("woff2");
  font-weight: 200 800;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Twilight Crystal";
  src: url("webfonts/TwilightCrystal-Italic[wght].woff2") format("woff2");
  font-weight: 200 800;
  font-style: italic;
  font-display: swap;
}
/* The same two faces for "Twilight Crystal Mono", from TwilightCrystalMono[wght].woff2
   and TwilightCrystalMono-Italic[wght].woff2. */
```

Or load Atkinson Hyperlegible Next and Mono from Google Fonts, which come next in the stack. Without either, the stack falls to the closest system fonts ([§2](../docs/design-system/typography.md#2-system-fonts)), each resized to Twilight Crystal's x-height.

## What it does

Everywhere:

- **Families.** Twilight Crystal for text; Twilight Crystal Mono for `code`, `kbd`, `samp` and `pre`, at the size of the text around them and without ligatures.
- **Sizes by geometry.** The desktop scale by default, the handheld scale when the primary pointer is coarse (`@media (pointer: coarse)`), and the documents scale in points when printed. All sizes are in rem, so they follow the reader's browser setting.
- **Levels.** `body` at running text, `h1` to `h6` at Heading 1 to 6 in Bold with line height 1.3; `small`, `figcaption` and `caption` at Small. The largest headings shrink on narrow screens so their widest words fit.
- **Spacing and figures.** Line height 1.5, letter spacing 0, tabular figures in `table`, `time` and `output`.

Inside an element with the class `document`, for document text only (articles, documentation, help pages):

- blocks one line apart, headings two lines after the block before and half a line before the block after;
- the first paragraph as Lead;
- list markers and indentation, underlined links, an indented and ruled quote, ruled table rows;
- lines of at most 34.6 em, which hold 80 characters.

Everything in `.document` stays at or below the specificity of one element, so a class on any element inside overrides it.

## Tokens

Every value is a custom property on `:root`, for components to use:

| Property | Value |
| --- | --- |
| `--twilight-font-text`, `--twilight-font-literal` | The two font stacks |
| `--twilight-step-n2` … `--twilight-step-7` | The scale of the current geometry |
| `--twilight-display-1`, `--twilight-display-2`, `--twilight-heading-1` … `--twilight-heading-6`, `--twilight-lead`, `--twilight-running-text`, `--twilight-interface-text`, `--twilight-small`, `--twilight-fine` | The size of each level |
| `--twilight-line`, `--twilight-line-compact` | 1.5 and 1.3 |
| `--twilight-space` | One line of running text, the unit of spacing |
| `--twilight-measure` | The longest line of running text |
| `--twilight-fit` | The largest size whose widest words fit the screen |
| `--twilight-code`, `--twilight-code-optimal` | Code in editors and terminals: 14 px and 16 px |

In Tailwind, use them as arbitrary values, such as `text-(length:--twilight-heading-2)` or `mt-(--twilight-space)`. Twilight Theme does not change Tailwind's theme (`@theme`).

## License

MIT, as the rest of Twilight Theme. `twilight.css` and `twilight.min.css` include Tailwind CSS Preflight, MIT License, Copyright (c) Tailwind Labs, Inc.; the copy it is built from, and its license, are in [`upstream/tailwindcss/`](upstream/tailwindcss/), pinned in [`upstream.json`](upstream.json).
