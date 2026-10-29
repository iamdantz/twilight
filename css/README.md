# Twilight Theme CSS reset

A base stylesheet for any page built with Twilight Theme, whatever CSS framework it uses. It starts each HTML element from Twilight Theme's rules instead of the browser's defaults. Today it covers typography, the part of the design system with measured rules for HTML: it applies [the typography rules](../docs/design-system/typography.md) as browsers read them. It sets no colors.

| File | For |
| --- | --- |
| [`twilight-tailwind.css`](twilight-tailwind.css) | Tailwind CSS 4 and the libraries built on it. Twilight Theme's base in `@layer base`, after Tailwind's own Preflight |
| [`twilight.css`](twilight.css) | Any other project. Tailwind's Preflight and Twilight Theme's base, so a page without Tailwind starts from the same point |
| [`twilight.min.css`](twilight.min.css) | The same, minified |

[`build.py`](build.py) writes the three files from [typography/twilight.json](../typography/twilight.json), and every pull request checks them against it. Change the tokens, not the files.

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

`twilight.css` is in no cascade layer and styles elements only, so it overrides a framework's styles for bare elements (`body`, `h1`, `code`), and every class overrides it: components and utilities keep their look.

## The fonts

The stylesheet names the fonts but does not load them. Load Twilight Crystal and Twilight Crystal Mono from the web fonts in a [release](https://github.com/iamdantz/twilight-theme/releases/latest), served next to your stylesheet:

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

## Names

Every name follows [the typography rules, §3](../docs/design-system/typography.md#3-names): the prefix `twl`, a namespace and a key from the tokens. The same key means the same thing in the rules, in `typography/twilight.json` and here.

| Custom property | Value |
| --- | --- |
| `--twl-font-sans`, `--twl-font-mono` | The two font stacks |
| `--twl-text-xs` … `--twl-text-6xl` | The scale of the current geometry |
| `--twl-text-display-1`, `--twl-text-display-2`, `--twl-text-h1` … `--twl-text-h6`, `--twl-text-body-lg`, `--twl-text-body`, `--twl-text-ui`, `--twl-text-body-sm`, `--twl-text-body-xs`, `--twl-text-code` | The size of each level |
| `--twl-text-fit` | The largest size whose widest words fit the screen |
| `--twl-leading`, `--twl-leading-tight` | 1.5 and 1.3 |
| `--twl-spacing` | One line of body text, the unit of spacing |
| `--twl-container-prose` | The longest line of body text |

The one class is `twl-prose`. In Tailwind, use the properties as arbitrary values, such as `text-(length:--twl-text-h2)` or `mt-(--twl-spacing)`. The reset does not change Tailwind's theme (`@theme`).

## What it does

On every element:

- **Fonts.** `sans` for text; `mono` for `code`, `kbd`, `samp` and `pre`, at the size of the text around them and without ligatures.
- **Sizes by geometry.** The `desktop` scale by default, the `handheld` scale when the primary pointer is coarse (`@media (pointer: coarse)`), and the `page` scale in points when printed. All sizes are in rem, so they follow the reader's browser setting.
- **Levels.** `body` on `body`, `h1` to `h6` on their elements in Bold with `tight` leading, `body-sm` on `small`, `figcaption` and `caption`. On narrow screens the largest headings shrink to `fit`.
- **Leading, tracking and figures.** `default` leading, tracking 0, tabular figures in `table`, `time` and `output`.

Inside an element with the class `twl-prose`, for prose only (articles, documentation, help pages):

- blocks one line apart, headings two lines below the block before and half a line above the block after;
- the first paragraph at `body-lg`;
- list markers and indentation, underlined links, an indented and ruled quote, ruled table rows;
- lines no longer than the `prose` container, 34.6 em, which holds 80 characters.

No rule inside `.twl-prose` is more specific than one element selector, so a class on any element inside overrides it.

## Tested

On every change to the CSS, the typography tokens or the tests, the CSS workflow runs [tests/css](../tests/css/test.mjs) in Chromium:

- **Parity.** A page with every element the reset styles has the same computed style with `twilight.css`, with `twilight.min.css`, and with Tailwind CSS 4 and `twilight-tailwind.css`, on a desktop screen, a 320 px window, a handheld screen and in print.
- **Rules.** Its sizes, weights, leading, spacing and line length are the values of the tokens in each geometry.
- **Components.** Components of daisyUI, of Flowbite, and written in utility classes as shadcn/ui and Nuxt UI write them keep every style their classes set when Twilight's file is added.

## License

MIT, as the rest of Twilight Theme. `twilight.css` and `twilight.min.css` include Tailwind CSS Preflight, MIT License, Copyright (c) Tailwind Labs, Inc.; the copy they are built from and its license are in [`upstream/tailwindcss/`](upstream/tailwindcss/), pinned in [`upstream.json`](upstream.json).
