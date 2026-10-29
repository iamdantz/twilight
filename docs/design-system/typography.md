# Twilight Theme design system: typography

Version 1.20 · Typefaces: Twilight Crystal (sans-serif), Twilight Crystal Mono (monospaced)

This document defines which typefaces carry Twilight Theme and what to use when they are not available. The typefaces themselves, what they add and how to install them, are described in [fonts/README.md](../../fonts/README.md). The colors of Twilight Theme do not depend on any font: every guarantee in [color.md](color.md) holds whatever face the text is set in.

## Contents

1. [Which font to use](#1-which-font-to-use)
2. [System fonts](#2-system-fonts)

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
