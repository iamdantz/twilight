<h1 align="center">Twilight</h1>

<p align="center"><i>Calm by design, legible by proof.</i></p>

<p align="center">
  <a href="#flavors">Flavors</a> ·
  <a href="#accents">Accents</a> ·
  <a href="#palette">Palette</a> ·
  <a href="docs/design-system.md">Design system</a> ·
  <a href="docs/construction.md">Construction</a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/palette-dusk.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/palette-dawn.png">
    <img src="assets/palette-dusk.png" alt="Twilight palette" width="800">
  </picture>
</p>

<p align="center">
  <a href="https://www.w3.org/TR/WCAG21/#contrast-enhanced"><img src="https://img.shields.io/badge/code-WCAG_AAA_(Dusk)-11171b?style=flat-square&labelColor=0a0e11&color=1a2329" alt="WCAG AAA in Dusk"></a>
  <img src="https://img.shields.io/badge/color_space-OKLCH-11171b?style=flat-square&labelColor=0a0e11&color=1a2329" alt="OKLCH">
  <img src="https://img.shields.io/badge/license-MIT-11171b?style=flat-square&labelColor=0a0e11&color=1a2329" alt="MIT">
</p>

<br>

Twilight is a color theme specification: two flavors, ten neutrals, eight colors and the rules that connect them. None of the colors were picked by eye. Two were chosen as seeds; every other value was calculated, and every pairing was checked for contrast and for color-vision deficiency.

## Why

I used Dracula for years. In almost every port the accent was pink/purple, and it's not exactly my favorite color. Catppuccin and its peach accent came closer, and it was the one I used until now, but my workspace still did not feel like mine.

I wanted my own theme but I do not trust my eye for color. So instead of choosing colors, I set out to derive them: start from two values, apply rules from color science and accessibility, and keep only what can be measured.

## Principles

- **Calculated, not chosen.** Two seeds, everything else derived. Each value can be traced back to a rule in [construction.md](docs/construction.md).
- **Legible everywhere.** Each text level is solved against the hardest surface it can appear on, so its contrast holds on all of them.
- **Distinct for everyone.** Code colors were optimized together so they stay apart under deuteranopia, protanopia and tritanopia.
- **Calm.** Surfaces are quiet, the accent is a detail rather than a field, and nothing is pure black or pure white.

## Flavors

|                                                                                           | Flavor   | Character                                                                                   |
|-------------------------------------------------------------------------------------------|----------|---------------------------------------------------------------------------------------------|
| <img src="https://placehold.co/20x20/11171b/11171b" width="20" height="20" alt="#11171b"> | **Dusk** | Dark. Code colors at 7:1 or higher (WCAG AAA).                                              |
| <img src="https://placehold.co/20x20/f4f7f9/f4f7f9" width="20" height="20" alt="#f4f7f9"> | **Dawn** | Light. Same structure and surface ratios as Dusk; code colors at 4.5:1 or higher (WCAG AA). |

Both flavors share every role and every rule. Only the values change.

## Accents

Any of the eight colors can be the accent. The accent marks focus, the cursor, active items, badges, links and the main action; it never colors content. Code colors and background states stay the same whichever accent you pick.

A theme is named by flavor and accent: **Twilight Dusk Grove**, **Twilight Dawn Sky**. Afterglow is the default, so **Twilight Dusk** means Twilight Dusk Afterglow.

| Accent    | Dusk                                                                                                | Dawn                                                                                                | Example name            |
|-----------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|-------------------------|
| Afterglow | <img src="https://placehold.co/20x20/ee7a1f/ee7a1f" width="20" height="20" alt="#ee7a1f"> `#ee7a1f` | <img src="https://placehold.co/20x20/ee7a1f/ee7a1f" width="20" height="20" alt="#ee7a1f"> `#ee7a1f` | Twilight Dusk Afterglow |
| Coral     | <img src="https://placehold.co/20x20/e78975/e78975" width="20" height="20" alt="#e78975"> `#e78975` | <img src="https://placehold.co/20x20/88323e/88323e" width="20" height="20" alt="#88323e"> `#88323e` | Twilight Dusk Coral     |
| Gold      | <img src="https://placehold.co/20x20/d6b95c/d6b95c" width="20" height="20" alt="#d6b95c"> `#d6b95c` | <img src="https://placehold.co/20x20/7a6716/7a6716" width="20" height="20" alt="#7a6716"> `#7a6716` | Twilight Dusk Gold      |
| Grove     | <img src="https://placehold.co/20x20/99cd8a/99cd8a" width="20" height="20" alt="#99cd8a"> `#99cd8a` | <img src="https://placehold.co/20x20/3d763e/3d763e" width="20" height="20" alt="#3d763e"> `#3d763e` | Twilight Dusk Grove     |
| Sea Salt  | <img src="https://placehold.co/20x20/6ed0d1/6ed0d1" width="20" height="20" alt="#6ed0d1"> `#6ed0d1` | <img src="https://placehold.co/20x20/186f7f/186f7f" width="20" height="20" alt="#186f7f"> `#186f7f` | Twilight Dusk Sea Salt  |
| Sky       | <img src="https://placehold.co/20x20/7babde/7babde" width="20" height="20" alt="#7babde"> `#7babde` | <img src="https://placehold.co/20x20/2a5785/2a5785" width="20" height="20" alt="#2a5785"> `#2a5785` | Twilight Dusk Sky       |
| Orchid    | <img src="https://placehold.co/20x20/d58ec3/d58ec3" width="20" height="20" alt="#d58ec3"> `#d58ec3` | <img src="https://placehold.co/20x20/7b3d6f/7b3d6f" width="20" height="20" alt="#7b3d6f"> `#7b3d6f` | Twilight Dusk Orchid    |
| Ember     | <img src="https://placehold.co/20x20/fcd1ad/fcd1ad" width="20" height="20" alt="#fcd1ad"> `#fcd1ad` | <img src="https://placehold.co/20x20/6c3d0d/6c3d0d" width="20" height="20" alt="#6c3d0d"> `#6c3d0d` | Twilight Dusk Ember     |

Each accent comes with derived variants for text, pressed and focus states, all solved to the same contrast rules. See [Accents in the design system](docs/design-system.md#5-accents).

## Palette

<details open>
<summary><b>Dusk</b></summary>
<br>

<img src="https://placehold.co/24x24/0a0e11/0a0e11" width="24" height="24" alt="#0a0e11"><img src="https://placehold.co/24x24/0e1316/0e1316" width="24" height="24" alt="#0e1316"><img src="https://placehold.co/24x24/11171b/11171b" width="24" height="24" alt="#11171b"><img src="https://placehold.co/24x24/1a2329/1a2329" width="24" height="24" alt="#1a2329"><img src="https://placehold.co/24x24/26333c/26333c" width="24" height="24" alt="#26333c"><img src="https://placehold.co/24x24/586f7d/586f7d" width="24" height="24" alt="#586f7d"><img src="https://placehold.co/24x24/778b97/778b97" width="24" height="24" alt="#778b97"><img src="https://placehold.co/24x24/a0aeb5/a0aeb5" width="24" height="24" alt="#a0aeb5"><img src="https://placehold.co/24x24/d2d6d8/d2d6d8" width="24" height="24" alt="#d2d6d8"><img src="https://placehold.co/24x24/eeeeef/eeeeef" width="24" height="24" alt="#eeeeef">&nbsp;&nbsp;<img src="https://placehold.co/24x24/ee7a1f/ee7a1f" width="24" height="24" alt="#ee7a1f"><img src="https://placehold.co/24x24/e78975/e78975" width="24" height="24" alt="#e78975"><img src="https://placehold.co/24x24/d6b95c/d6b95c" width="24" height="24" alt="#d6b95c"><img src="https://placehold.co/24x24/99cd8a/99cd8a" width="24" height="24" alt="#99cd8a"><img src="https://placehold.co/24x24/6ed0d1/6ed0d1" width="24" height="24" alt="#6ed0d1"><img src="https://placehold.co/24x24/7babde/7babde" width="24" height="24" alt="#7babde"><img src="https://placehold.co/24x24/d58ec3/d58ec3" width="24" height="24" alt="#d58ec3"><img src="https://placehold.co/24x24/fcd1ad/fcd1ad" width="24" height="24" alt="#fcd1ad">

**Neutrals**

| | Name | Hex | RGB | OKLCH | Role |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/20x20/0a0e11/0a0e11" width="20" height="20" alt="#0a0e11"> | Shell | `#0a0e11` | `rgb(10, 14, 17)` | `oklch(16.1% 0.009 240.6)` | Outer frame |
| <img src="https://placehold.co/20x20/0e1316/0e1316" width="20" height="20" alt="#0e1316"> | Rail | `#0e1316` | `rgb(14, 19, 22)` | `oklch(18.3% 0.010 234.4)` | Docked panels |
| <img src="https://placehold.co/20x20/11171b/11171b" width="20" height="20" alt="#11171b"> | Canvas | `#11171b` | `rgb(17, 23, 27)` | `oklch(20.0% 0.012 237.4)` | Content |
| <img src="https://placehold.co/20x20/1a2329/1a2329" width="20" height="20" alt="#1a2329"> | Raised | `#1a2329` | `rgb(26, 35, 41)` | `oklch(25.0% 0.017 237.6)` | Floating layers |
| <img src="https://placehold.co/20x20/26333c/26333c" width="20" height="20" alt="#26333c"> | Edge | `#26333c` | `rgb(38, 51, 60)` | `oklch(31.3% 0.024 238.7)` | Dividers |
| <img src="https://placehold.co/20x20/586f7d/586f7d" width="20" height="20" alt="#586f7d"> | Control | `#586f7d` | `rgb(88, 111, 125)` | `oklch(52.8% 0.035 235.0)` | Control boundaries |
| <img src="https://placehold.co/20x20/778b97/778b97" width="20" height="20" alt="#778b97"> | Faint | `#778b97` | `rgb(119, 139, 151)` | `oklch(62.5% 0.029 234.3)` | Tertiary text |
| <img src="https://placehold.co/20x20/a0aeb5/a0aeb5" width="20" height="20" alt="#a0aeb5"> | Subtle | `#a0aeb5` | `rgb(160, 174, 181)` | `oklch(74.2% 0.019 229.1)` | Secondary text, icons |
| <img src="https://placehold.co/20x20/d2d6d8/d2d6d8" width="20" height="20" alt="#d2d6d8"> | Body | `#d2d6d8` | `rgb(210, 214, 216)` | `oklch(87.4% 0.005 228.8)` | Default text |
| <img src="https://placehold.co/20x20/eeeeef/eeeeef" width="20" height="20" alt="#eeeeef"> | Ink | `#eeeeef` | `rgb(238, 238, 239)` | `oklch(94.9% 0.001 0)` | Titles, focus |

**Colors**

| | Name | Hex | RGB | OKLCH | Meaning |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/20x20/ee7a1f/ee7a1f" width="20" height="20" alt="#ee7a1f"> | Afterglow | `#ee7a1f` | `rgb(238, 122, 31)` | `oklch(70.0% 0.170 51.9)` | Default accent |
| <img src="https://placehold.co/20x20/e78975/e78975" width="20" height="20" alt="#e78975"> | Coral | `#e78975` | `rgb(231, 137, 117)` | `oklch(72.5% 0.119 32.9)` | Error, removed |
| <img src="https://placehold.co/20x20/d6b95c/d6b95c" width="20" height="20" alt="#d6b95c"> | Gold | `#d6b95c` | `rgb(214, 185, 92)` | `oklch(79.2% 0.117 92.2)` | Warning, modified |
| <img src="https://placehold.co/20x20/99cd8a/99cd8a" width="20" height="20" alt="#99cd8a"> | Grove | `#99cd8a` | `rgb(153, 205, 138)` | `oklch(79.5% 0.107 138.8)` | Success, added |
| <img src="https://placehold.co/20x20/6ed0d1/6ed0d1" width="20" height="20" alt="#6ed0d1"> | Sea Salt | `#6ed0d1` | `rgb(110, 208, 209)` | `oklch(79.9% 0.092 196.3)` | Renamed, auxiliary |
| <img src="https://placehold.co/20x20/7babde/7babde" width="20" height="20" alt="#7babde"> | Sky | `#7babde` | `rgb(123, 171, 222)` | `oklch(72.7% 0.091 250.6)` | Information |
| <img src="https://placehold.co/20x20/d58ec3/d58ec3" width="20" height="20" alt="#d58ec3"> | Orchid | `#d58ec3` | `rgb(213, 142, 195)` | `oklch(73.4% 0.110 336.4)` | Conflict |
| <img src="https://placehold.co/20x20/fcd1ad/fcd1ad" width="20" height="20" alt="#fcd1ad"> | Ember | `#fcd1ad` | `rgb(252, 209, 173)` | `oklch(88.9% 0.068 61.7)` | Parameters |

</details>

<details>
<summary><b>Dawn</b></summary>
<br>

<img src="https://placehold.co/24x24/ebeff2/ebeff2" width="24" height="24" alt="#ebeff2"><img src="https://placehold.co/24x24/eff3f5/eff3f5" width="24" height="24" alt="#eff3f5"><img src="https://placehold.co/24x24/f4f7f9/f4f7f9" width="24" height="24" alt="#f4f7f9"><img src="https://placehold.co/24x24/e1eaef/e1eaef" width="24" height="24" alt="#e1eaef"><img src="https://placehold.co/24x24/c1d6e2/c1d6e2" width="24" height="24" alt="#c1d6e2"><img src="https://placehold.co/24x24/748895/748895" width="24" height="24" alt="#748895"><img src="https://placehold.co/24x24/566c7a/566c7a" width="24" height="24" alt="#566c7a"><img src="https://placehold.co/24x24/3b4f5c/3b4f5c" width="24" height="24" alt="#3b4f5c"><img src="https://placehold.co/24x24/25313b/25313b" width="24" height="24" alt="#25313b"><img src="https://placehold.co/24x24/11171b/11171b" width="24" height="24" alt="#11171b">&nbsp;&nbsp;<img src="https://placehold.co/24x24/ee7a1f/ee7a1f" width="24" height="24" alt="#ee7a1f"><img src="https://placehold.co/24x24/88323e/88323e" width="24" height="24" alt="#88323e"><img src="https://placehold.co/24x24/7a6716/7a6716" width="24" height="24" alt="#7a6716"><img src="https://placehold.co/24x24/3d763e/3d763e" width="24" height="24" alt="#3d763e"><img src="https://placehold.co/24x24/186f7f/186f7f" width="24" height="24" alt="#186f7f"><img src="https://placehold.co/24x24/2a5785/2a5785" width="24" height="24" alt="#2a5785"><img src="https://placehold.co/24x24/7b3d6f/7b3d6f" width="24" height="24" alt="#7b3d6f"><img src="https://placehold.co/24x24/6c3d0d/6c3d0d" width="24" height="24" alt="#6c3d0d">

**Neutrals**

| | Name | Hex | RGB | OKLCH | Role |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/20x20/ebeff2/ebeff2" width="20" height="20" alt="#ebeff2"> | Shell | `#ebeff2` | `rgb(235, 239, 242)` | `oklch(95.0% 0.006 239.8)` | Outer frame |
| <img src="https://placehold.co/20x20/eff3f5/eff3f5" width="20" height="20" alt="#eff3f5"> | Rail | `#eff3f5` | `rgb(239, 243, 245)` | `oklch(96.2% 0.005 228.8)` | Docked panels |
| <img src="https://placehold.co/20x20/f4f7f9/f4f7f9" width="20" height="20" alt="#f4f7f9"> | Canvas | `#f4f7f9` | `rgb(244, 247, 249)` | `oklch(97.4% 0.004 236.5)` | Content |
| <img src="https://placehold.co/20x20/e1eaef/e1eaef" width="20" height="20" alt="#e1eaef"> | Raised | `#e1eaef` | `rgb(225, 234, 239)` | `oklch(93.2% 0.012 231.7)` | Floating layers |
| <img src="https://placehold.co/20x20/c1d6e2/c1d6e2" width="20" height="20" alt="#c1d6e2"> | Edge | `#c1d6e2` | `rgb(193, 214, 226)` | `oklch(86.4% 0.028 232.7)` | Dividers |
| <img src="https://placehold.co/20x20/748895/748895" width="20" height="20" alt="#748895"> | Control | `#748895` | `rgb(116, 136, 149)` | `oklch(61.5% 0.030 236.5)` | Control boundaries |
| <img src="https://placehold.co/20x20/566c7a/566c7a" width="20" height="20" alt="#566c7a"> | Faint | `#566c7a` | `rgb(86, 108, 122)` | `oklch(51.9% 0.034 236.2)` | Tertiary text |
| <img src="https://placehold.co/20x20/3b4f5c/3b4f5c" width="20" height="20" alt="#3b4f5c"> | Subtle | `#3b4f5c` | `rgb(59, 79, 92)` | `oklch(41.6% 0.033 237.1)` | Secondary text, icons |
| <img src="https://placehold.co/20x20/25313b/25313b" width="20" height="20" alt="#25313b"> | Body | `#25313b` | `rgb(37, 49, 59)` | `oklch(30.7% 0.024 243.8)` | Default text |
| <img src="https://placehold.co/20x20/11171b/11171b" width="20" height="20" alt="#11171b"> | Ink | `#11171b` | `rgb(17, 23, 27)` | `oklch(20.0% 0.012 237.4)` | Titles, focus |

**Colors**

| | Name | Hex | RGB | OKLCH | Meaning |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/20x20/ee7a1f/ee7a1f" width="20" height="20" alt="#ee7a1f"> | Afterglow | `#ee7a1f` | `rgb(238, 122, 31)` | `oklch(70.0% 0.170 51.9)` | Default accent |
| <img src="https://placehold.co/20x20/88323e/88323e" width="20" height="20" alt="#88323e"> | Coral | `#88323e` | `rgb(136, 50, 62)` | `oklch(44.3% 0.118 14.9)` | Error, removed |
| <img src="https://placehold.co/20x20/7a6716/7a6716" width="20" height="20" alt="#7a6716"> | Gold | `#7a6716` | `rgb(122, 103, 22)` | `oklch(51.8% 0.098 94.9)` | Warning, modified |
| <img src="https://placehold.co/20x20/3d763e/3d763e" width="20" height="20" alt="#3d763e"> | Grove | `#3d763e` | `rgb(61, 118, 62)` | `oklch(51.2% 0.105 144.2)` | Success, added |
| <img src="https://placehold.co/20x20/186f7f/186f7f" width="20" height="20" alt="#186f7f"> | Sea Salt | `#186f7f` | `rgb(24, 111, 127)` | `oklch(50.0% 0.081 213.4)` | Renamed, auxiliary |
| <img src="https://placehold.co/20x20/2a5785/2a5785" width="20" height="20" alt="#2a5785"> | Sky | `#2a5785` | `rgb(42, 87, 133)` | `oklch(44.8% 0.091 251.0)` | Information |
| <img src="https://placehold.co/20x20/7b3d6f/7b3d6f" width="20" height="20" alt="#7b3d6f"> | Orchid | `#7b3d6f` | `rgb(123, 61, 111)` | `oklch(45.7% 0.109 335.0)` | Conflict |
| <img src="https://placehold.co/20x20/6c3d0d/6c3d0d" width="20" height="20" alt="#6c3d0d"> | Ember | `#6c3d0d` | `rgb(108, 61, 13)` | `oklch(40.9% 0.088 60.2)` | Parameters |

</details>

Machine-readable values for both flavors, all accents, background states and the 16 terminal colors are in [palette/twilight.json](palette/twilight.json).

## Guarantees

| | Dusk | Dawn |
|---|---|---|
| Body text on any surface | 10.9:1 | 10.9:1 |
| Faintest text on any surface | 4.5:1 | 4.5:1 |
| Code colors on every code surface | 7.0:1 | 4.5:1 |
| Control boundaries and focus | 3.0:1 | 3.0:1 |
| Smallest code-color difference, color-vision deficiency | ΔE 0.054 | ΔE 0.041 |
| Pure black or white | none | none |

Contrast is WCAG 2.x, measured on final sRGB values. The color-vision figure is the worst case across simulated deuteranopia, protanopia and tritanopia. Full tables are in the [design system](docs/design-system.md#13-guarantees).

## How it was built

All math is done in OKLCH and checked in sRGB. The neutrals sit at the exact complementary hue of Afterglow. Surface lightness follows a geometric progression, and text levels are solved by contrast target. The six terminal hues are anchored to the ANSI standard, placed at each hue's natural lightness and lit by one shared warm chroma law. Those six and Ember were then optimized together for distinctness under four vision models. The mapping of colors to code roles came from 207,361 tokens of real code and the measured conventions of ten widely used themes.

The full derivation, with every formula and parameter, is in [construction.md](docs/construction.md).

## Using Twilight

Twilight is defined independently of any application. To build a theme for a tool, map its regions to the surface roles and follow the checklist in [Building a theme from this definition](docs/design-system.md#12-building-a-theme-from-this-definition).

## Repository

```
.
├── README.md
├── assets/                  palette images
├── docs/
│   ├── design-system.md     roles, rules and application
│   └── construction.md      derivation, optimization and validation
├── palette/
│   └── twilight.json        all values, machine-readable
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## License

[MIT](LICENSE) © José D. Gutiérrez
