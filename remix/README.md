# Remix

Remix is Twilight Theme's CSS reset: the first style sheet of a page, in the place of normalize.css, a reset, Preflight or Reboot. It makes browsers agree, removes the defaults that vary between them, and starts every element, from headings to form controls, media and tables, from Twilight Theme's rules. It works with any CSS framework, or none.

How each rule was decided, and how Remix compares with those tools, is in [docs/construction/remix.md](../docs/construction/remix.md).

## Files

| File | For |
| --- | --- |
| [`remix.min.css`](remix.min.css) | Projects. The whole reset, minified |
| [`remix.css`](remix.css) | Reading. The same, with each group of rules explained |
| [`remix-tailwind.css`](remix-tailwind.css) | Tailwind CSS 4 and the libraries built on it. Only the rules Preflight does not already give, in `@layer base` after it |

The three files are written by [`build.py`](build.py) from [typography/twilight.json](../typography/twilight.json), and every pull request checks them. Change the tokens, not the files.

## Use

Without Tailwind CSS, link it before your own styles, and after a framework's if you use one:

```html
<link rel="stylesheet" href="remix.min.css">
```

`remix.min.css` is in no cascade layer and styles elements only, so it overrides a framework's styles for bare elements (`body`, `h1`, `code`), and any class overrides it.

With Tailwind CSS 4, import it after Tailwind:

```css
@import "tailwindcss";
@import "./remix-tailwind.css";
```

Preflight still runs and Remix goes after it in the same layer, so Remix decides where Twilight Theme has a rule and Preflight keeps the rest. Utilities and component classes win over both. A page gets the same result with either file.

## What Remix does

- **Starts every element from the same box.** Sizes include padding and border; no element has outer spacing, padding or borders of its own; lists have no markers; images and media are blocks that never overflow their container; tables collapse their borders.
- **Makes browsers agree.** Text keeps its size when an iPhone rotates; `sub` and `sup` keep the line; abbreviations are dotted; `summary` shows its marker; Firefox draws focus rings as other browsers do; `hidden` always hides.
- **Prepares form controls.** They take the font and color of the text around them and start without a surface; buttons can be styled on iOS; search fields are plain; number and date fields keep a steady height; text areas resize vertically; fieldsets can shrink.
- **Sets Twilight Theme's base.** The fonts and the scale of the current geometry (desktop, handheld by a coarse pointer, page when printed), the levels on `body`, `h1` to `h6`, `small`, `figcaption` and `caption`, Bold for `b` and `strong`, literal text in Twilight Crystal Mono at the size of the sentence, leading 1.5 and 1.3, tracking 0, tabular figures in `table`, `time` and `output`, placeholders that reach 4.5:1.

## What Remix does not do

- No classes, so no components, no layout, no utilities and no theme. With Tailwind CSS it is not a port: it adds nothing to `@theme`.
- No spacing between elements. Spacing belongs to the content; prose takes it from `--twl-spacing` and `--twl-container-prose`.
- No colors yet. They come when the color part of the design system is added to Remix.
- No motion, cursors or other choices without a rule behind them.

## The fonts

Remix names the fonts but does not load them. Load Twilight Crystal and Twilight Crystal Mono from the web fonts in a [release](https://github.com/iamdantz/twilight-theme/releases/latest), served next to your style sheet:

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

## Custom properties

Every value is on `:root`, for your own styles. The names follow [the typography rules, §3](../docs/design-system/typography.md#3-names): the prefix `twl`, a namespace and a key.

| Custom property | Value |
| --- | --- |
| `--twl-font-sans`, `--twl-font-mono` | The two font stacks |
| `--twl-text-xs` … `--twl-text-6xl` | The scale of the current geometry |
| `--twl-text-display-1`, `--twl-text-display-2`, `--twl-text-h1` … `--twl-text-h6`, `--twl-text-body-lg`, `--twl-text-body`, `--twl-text-ui`, `--twl-text-body-sm`, `--twl-text-body-xs`, `--twl-text-code` | The size of each level |
| `--twl-text-fit` | The largest size whose widest words fit the screen |
| `--twl-leading`, `--twl-leading-tight` | 1.5 and 1.3 |
| `--twl-spacing` | One line of body text, the unit of spacing |
| `--twl-container-prose` | The longest line of body text |

In Tailwind CSS, use them as arbitrary values, such as `text-(length:--twl-text-h2)` or `mt-(--twl-spacing)`.

## Tested

On every change to Remix, the tokens or the tests, a workflow runs [tests/remix](../tests/remix/test.mjs) in Chromium. A page of every element Remix styles computes the same with `remix.css`, `remix.min.css`, and Tailwind CSS 4 with `remix-tailwind.css`, on a desktop screen, a 320 px window, a handheld screen and in print; its values are those of the tokens; and components of daisyUI, Flowbite and utility classes keep every style their classes set.

## License

MIT, as the rest of Twilight Theme. Remix contains no code from other projects.
