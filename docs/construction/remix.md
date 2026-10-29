# Twilight Theme construction: Remix

Version 1.0. What a CSS reset does, and how Remix was decided.

Remix is Twilight Theme's CSS reset. Its product page, with how to use it, is [remix/README.md](../../remix/README.md); its rules are written by [`remix/build.py`](../../remix/build.py). This document compares the tools Remix takes the place of, sets the role and the limits that follow from them, and gives the reason for every rule.

Five tools were read for this comparison. None is copied into Remix or kept in the repository:

| Tool | Version | Kind |
|---|---|---|
| normalize.css | 8.0.1 | Normalizer |
| modern-normalize | 3.0.1 | Normalizer |
| Eric Meyer's reset, as packaged by reset-css | 5.0.2 | Reset |
| Tailwind CSS Preflight | 4.3.3 | Reset with a base |
| Bootstrap Reboot | 5.3.7 | Normalizer with a base |

---

## 1. What a CSS reset does

Browsers ship a style sheet of their own, and they do not agree on it. A CSS reset is the first style sheet a page loads, and it does one or more of three jobs:

1. **Normalize.** Make browsers agree, and fix what they get wrong, while keeping the defaults that are useful. normalize.css and modern-normalize do only this.
2. **Reset.** Remove the defaults, so every element starts from nothing and the page sets what it needs. Meyer's reset does only this.
3. **Set a base.** After normalizing or resetting, give every element the starting style the rest of the design builds on. Preflight resets, then sets a font, a line height and form controls that inherit them; Reboot normalizes, then sets fonts, sizes, colors and spacing from Bootstrap's variables.

All five stay within the same limits. They style elements, attributes and pseudo-elements, never a class (Reboot styles `[role=button]`, an attribute). They set no layout and draw no component. The base is where they differ: Preflight's is small, and Reboot's carries Bootstrap's look.

## 2. What each one does

| Concern | normalize | modern-normalize | Meyer | Preflight | Reboot | Remix |
|---|---|---|---|---|---|---|
| Sizes include padding and border | – | yes | – | yes | yes | yes |
| Outer spacing | `body` only | `body` only | removed | removed | its own scale | removed |
| Padding | – | – | removed | removed | on lists | removed |
| Borders | – | – | removed | width 0, style solid | on table cells | width 0, style solid |
| Same text size after rotation on iOS | yes | yes | – | yes | yes | yes |
| Tab size | – | 4 | – | 4 | – | 4 |
| Tap highlight on touch | – | – | – | removed | removed | removed |
| Font | – | system | inherited | system | Bootstrap's | Twilight Crystal, then Atkinson Hyperlegible, then system fonts sized to it |
| Line height | 1.15 | 1.15 | 1 | 1.5 | 1.5 | 1.5 |
| Headings | `h1` size fixed | – | inherited | inherited | sizes, weight, spacing | the levels `h1` to `h6` |
| `b`, `strong` | bolder | bolder | – | bolder | bolder | Bold, 700 |
| `small` | 80 % | 80 % | – | 80 % | 0.875 em | `body-sm` |
| `sub`, `sup` keep the line | yes | yes | – | yes | yes | yes |
| Code | monospace, 1 em | system mono, 1 em | – | system mono, 1 em | mono, smaller, colored | Twilight Crystal Mono, 1 em, no ligatures |
| Links | – | – | – | text color, no underline | link color, underline | text color, no underline |
| `abbr[title]` dotted | yes | – | – | yes | yes | yes |
| List markers | kept | kept | removed | removed | kept, indented | removed |
| `hr` | – | – | – | 1 px, text color | 1 px, faded, spaced | 1 px, text color |
| Images and media | – | – | – | block, never wider than their container | aligned | block, never wider than their container |
| Tables | – | border color | collapsed | collapsed, no indent | collapsed, caption below | collapsed, no indent; tabular figures |
| Form controls take the text around them | yes | yes | – | yes, with its color, no surface | yes | yes, with its color, no surface |
| Buttons styleable on iOS | yes | yes | – | yes | yes | yes |
| Search fields | plain | plain | – | default shape | plain | plain |
| Placeholders | – | – | – | half the text color | – | 54 % of the text color (§4) |
| Number, date and file inputs | yes | yes | – | yes | yes | yes |
| Text areas resize vertically only | – | – | – | yes | yes | yes |
| Fieldsets can shrink | – | – | – | – | yes | yes |
| `summary` shows its marker | yes | yes | – | yes | yes | yes |
| Firefox focus ring as in other browsers | dotted | – | – | yes | – | yes |
| `hidden` hides | yes | – | yes | yes, forced | yes, forced | yes, forced |
| Colors and backgrounds | – | – | – | placeholder | body, links, code, marks | none |
| Spacing between elements | `h1` | – | – | – | paragraphs, lists, headings, figures | none |
| Motion and cursors | – | – | – | – | smooth scrolling, pointer cursors | none |
| Custom properties | – | – | – | – | `--bs-*` | `--twl-*` |

## 3. What is no longer needed

Part of what the oldest tools do fixes browsers that are no longer in use. normalize.css fixes Internet Explorer 10 and 11 and the first Edge: `main`, `details` and `template` that do not display, borders around linked images, `hr` and `legend` boxes, buttons that clip their text, checkbox padding, text area scroll bars, the inner focus border of old Firefox buttons. Meyer's reset gives HTML5 elements a block display and turns off quotation marks, both for browsers of its time. Remix supports the current versions of Chrome, Edge, Firefox and Safari, and leaves all of these out.

## 4. Remix

**Role.** Remix is to Twilight Theme what these tools are to their projects: the first style sheet of a page. It normalizes, resets, and sets the base the design system asks for. It is not a typography style sheet: it starts every element, from headings to form controls, media and tables. Typography is the part of the base that the design system already defines; the rest of the base will follow the design system as other parts are written.

**Limits.** Remix does no more than these tools do:

- It styles elements, attributes and pseudo-elements only. It has no classes, so no components, no layout and no utilities.
- No rule is more specific than one element selector, except `[hidden]`, forced as Preflight and Reboot force it. Any class overrides Remix.
- It sets no spacing between elements. Spacing belongs to the content: prose takes the spacing of [design-system/typography.md §9](../design-system/typography.md#9-leading-and-spacing), applied by the page with `--twl-spacing` and `--twl-container-prose`.
- It sets no colors until the color part of the design system is added to it, and no motion, cursors or other choices without a rule behind them.

**The structural base.** Where the tools disagree on how much to remove, Remix takes the result of Preflight and modern-normalize: sizes that include padding and border, no outer spacing or padding, no list markers, media as blocks, form controls that take the text around them and start without a surface. Most current frameworks and component libraries are built on that base, so a component looks the same on a page with Remix whether or not the page uses Tailwind CSS. Remix's rules are its own, grouped by kind of element, and tests/remix confirms their result in a browser (§6).

**Where Twilight decides.** Remix departs from that base only where a rule of the design system, or the agreement of the other tools, asks for it:

| Rule | Reason |
|---|---|
| Fonts, levels, leading and tracking on `html`, `body`, `h1`–`h6`, `small`, `figcaption`, `caption`, `b`, `strong` | [design-system/typography.md](../design-system/typography.md) §4 to §9 |
| `code`, `kbd`, `samp`, `pre` in Twilight Crystal Mono, 1 em, without ligatures | §4: literal text at the size of the sentence, every character visible |
| `pre` scrolls instead of widening the page | §14: no text runs past its column |
| Tabular figures in `table`, `time`, `output` | §11 |
| One-line controls (`button`, `input`, `select`, file buttons) at `tight` leading; text areas at `default` | §9: one-line UI text at 1.3, text that wraps at 1.5 |
| Placeholders at 54 % of the text color | Below |
| Search fields plain, as other fields | normalize, modern-normalize and Reboot agree; without it Safari draws its own rounded field |
| Fieldsets can shrink below their content | Reboot; otherwise a fieldset inside a grid or a flex row overflows it |

**Placeholders.** A placeholder is text, so it needs 4.5:1 (WCAG 1.4.3). Black at opacity *a* over white is a gray of 255 × (1 − *a*), and that gray reaches 4.5:1 at *a* = 0.537. Remix sets 0.54, which is also Firefox's own value. Preflight's half of the text color gives 3.95:1. When color is added to Remix, placeholders will take Subtle, as [design-system/color.md](../design-system/color.md#4-text-and-control-levels) asks.

## 5. The Tailwind CSS file

A page with Tailwind CSS 4 already has Preflight in `@layer base`. `remix-tailwind.css` goes in the same layer, after Preflight, and holds only the rules whose result Preflight does not already give: the tokens, the fallback fonts, and the rules of the table in §4. Everything else Preflight already provides with the same result.

It is not a port of Twilight Theme to Tailwind CSS: it adds nothing to Tailwind's theme (`@theme`), defines no utilities and changes none. Utilities and component classes are in later layers, so they always win over Remix, as they do over Preflight.

## 6. Checked

[tests/remix](../../tests/remix/test.mjs) runs in Chromium on every change to Remix, the tokens or the tests:

- A page with every element Remix styles has the same computed style with `remix.css`, with `remix.min.css`, and with Tailwind CSS 4 and `remix-tailwind.css`, on a desktop screen, a 320 px window, a handheld screen and in print. Placeholders, which have no computed style, are compared by the gray of their darkest pixel.
- The sizes, weights and leading are those of the tokens; no element has outer spacing; lists have no markers; `pre` scrolls; placeholders are drawn at 4.5:1.
- Components of daisyUI, of Flowbite, and written in utility classes as shadcn/ui and Nuxt UI write them keep every style their classes set when Remix is added.

## 7. Reproducing

`python remix/build.py` writes the three files from [typography/twilight.json](../../typography/twilight.json); `--check` reports any difference, and the validator runs it.
