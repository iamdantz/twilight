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

Twilight is a color theme specification: two flavors, ten neutrals, eight colors and the rules that connect them. None of the palette colors were picked by eye. One value was chosen as a seed; every color was calculated from it, and every pairing was checked for contrast and for color-vision deficiency.

## Why

I used Dracula for years. In almost every port the accent was pink/purple, and it's not exactly my favorite color. Catppuccin and its peach accent came closer, and it was the one I used until now, but my workspace still did not feel like mine.

I wanted my own theme but I do not trust my eye for color. So instead of choosing colors, I set out to derive them: start from one value, apply rules from color science and accessibility, and keep only what can be measured.

## Principles

- **Calculated.** One seed, everything else derived. Each value can be traced back to a rule in [construction.md](docs/construction.md).
- **Legible everywhere.** Each text level is solved against the hardest surface it can appear on, so its contrast holds on all of them.
- **Distinct for everyone.** Code colors were optimized together so they stay apart under deuteranopia, protanopia and tritanopia.
- **Calm.** Surfaces are quiet, the accent is a detail rather than a field, and nothing is pure black or pure white.

## Flavors

|                                                                                           | Flavor   | Character                                                                                   |
|-------------------------------------------------------------------------------------------|----------|---------------------------------------------------------------------------------------------|
| <img src="https://placehold.co/20x20/11171b/11171b" width="20" height="20" alt="#11171b"> | **Dusk** | Dark. Code colors at 7:1 or higher (WCAG AAA).                                              |
| <img src="https://placehold.co/20x20/eeeeef/eeeeef" width="20" height="20" alt="#eeeeef"> | **Dawn** | Light. The light end of the same system; code colors at 4.5:1 or higher (WCAG AA).          |

Both flavors share every role, every rule and one neutral curve. Dawn's Canvas is Dusk's Ink, and Dawn's Ink is Dusk's Canvas.

## Accents

Any of the eight colors can be the accent. The accent marks focus, the cursor, active items, badges, links and the main action; it never colors content. Code colors and background states stay the same whichever accent you pick.

A theme is named by flavor and accent: **Twilight Dusk Grove**, **Twilight Dawn Sky**. Afterglow is the default, so **Twilight Dusk** means Twilight Dusk Afterglow.

| Accent    | Dusk                                                                                                | Dawn                                                                                                | Example name            |
|-----------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|-------------------------|
| Afterglow | <img src="https://placehold.co/20x20/ff7d00/ff7d00" width="20" height="20" alt="#ff7d00"> `#ff7d00` | <img src="https://placehold.co/20x20/ff7d00/ff7d00" width="20" height="20" alt="#ff7d00"> `#ff7d00` | Twilight Dusk Afterglow |
| Coral     | <img src="https://placehold.co/20x20/ee8476/ee8476" width="20" height="20" alt="#ee8476"> `#ee8476` | <img src="https://placehold.co/20x20/8d3826/8d3826" width="20" height="20" alt="#8d3826"> `#8d3826` | Twilight Dusk Coral     |
| Gold      | <img src="https://placehold.co/20x20/dbba50/dbba50" width="20" height="20" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/20x20/766014/766014" width="20" height="20" alt="#766014"> `#766014` | Twilight Dusk Gold      |
| Grove     | <img src="https://placehold.co/20x20/99d086/99d086" width="20" height="20" alt="#99d086"> `#99d086` | <img src="https://placehold.co/20x20/39713a/39713a" width="20" height="20" alt="#39713a"> `#39713a` | Twilight Dusk Grove     |
| Sea Salt  | <img src="https://placehold.co/20x20/65d5d2/65d5d2" width="20" height="20" alt="#65d5d2"> `#65d5d2` | <img src="https://placehold.co/20x20/176a7e/176a7e" width="20" height="20" alt="#176a7e"> `#176a7e` | Twilight Dusk Sea Salt  |
| Sky       | <img src="https://placehold.co/20x20/78aee6/78aee6" width="20" height="20" alt="#78aee6"> `#78aee6` | <img src="https://placehold.co/20x20/3f4880/3f4880" width="20" height="20" alt="#3f4880"> `#3f4880` | Twilight Dusk Sky       |
| Orchid    | <img src="https://placehold.co/20x20/db8dc7/db8dc7" width="20" height="20" alt="#db8dc7"> `#db8dc7` | <img src="https://placehold.co/20x20/813b67/813b67" width="20" height="20" alt="#813b67"> `#813b67` | Twilight Dusk Orchid    |
| Ember     | <img src="https://placehold.co/20x20/fcd6b7/fcd6b7" width="20" height="20" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/20x20/67320a/67320a" width="20" height="20" alt="#67320a"> `#67320a` | Twilight Dusk Ember     |

Each accent comes with derived variants for text, pressed and focus states, all solved to the same contrast rules. See [Accents in the design system](docs/design-system.md#5-accents).

## Palette

<details open>
<summary><b>Dusk</b></summary>
<br>

<img src="https://placehold.co/24x24/0a0e11/0a0e11" width="24" height="24" alt="#0a0e11"><img src="https://placehold.co/24x24/0e1316/0e1316" width="24" height="24" alt="#0e1316"><img src="https://placehold.co/24x24/11171b/11171b" width="24" height="24" alt="#11171b"><img src="https://placehold.co/24x24/1a2329/1a2329" width="24" height="24" alt="#1a2329"><img src="https://placehold.co/24x24/26333c/26333c" width="24" height="24" alt="#26333c"><img src="https://placehold.co/24x24/586f7d/586f7d" width="24" height="24" alt="#586f7d"><img src="https://placehold.co/24x24/778b97/778b97" width="24" height="24" alt="#778b97"><img src="https://placehold.co/24x24/a0aeb5/a0aeb5" width="24" height="24" alt="#a0aeb5"><img src="https://placehold.co/24x24/d2d6d8/d2d6d8" width="24" height="24" alt="#d2d6d8"><img src="https://placehold.co/24x24/eeeeef/eeeeef" width="24" height="24" alt="#eeeeef">&nbsp;&nbsp;<img src="https://placehold.co/24x24/ff7d00/ff7d00" width="24" height="24" alt="#ff7d00"><img src="https://placehold.co/24x24/ee8476/ee8476" width="24" height="24" alt="#ee8476"><img src="https://placehold.co/24x24/dbba50/dbba50" width="24" height="24" alt="#dbba50"><img src="https://placehold.co/24x24/99d086/99d086" width="24" height="24" alt="#99d086"><img src="https://placehold.co/24x24/65d5d2/65d5d2" width="24" height="24" alt="#65d5d2"><img src="https://placehold.co/24x24/78aee6/78aee6" width="24" height="24" alt="#78aee6"><img src="https://placehold.co/24x24/db8dc7/db8dc7" width="24" height="24" alt="#db8dc7"><img src="https://placehold.co/24x24/fcd6b7/fcd6b7" width="24" height="24" alt="#fcd6b7">

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
| <img src="https://placehold.co/20x20/ff7d00/ff7d00" width="20" height="20" alt="#ff7d00"> | Afterglow | `#ff7d00` | `rgb(255, 125, 0)` | `oklch(72.7% 0.188 51.7)` | Default accent |
| <img src="https://placehold.co/20x20/ee8476/ee8476" width="20" height="20" alt="#ee8476"> | Coral | `#ee8476` | `rgb(238, 132, 118)` | `oklch(72.6% 0.132 28.6)` | Error, removed |
| <img src="https://placehold.co/20x20/dbba50/dbba50" width="20" height="20" alt="#dbba50"> | Gold | `#dbba50` | `rgb(219, 186, 80)` | `oklch(79.8% 0.129 91.9)` | Warning, modified |
| <img src="https://placehold.co/20x20/99d086/99d086" width="20" height="20" alt="#99d086"> | Grove | `#99d086` | `rgb(153, 208, 134)` | `oklch(80.1% 0.116 137.9)` | Success, added |
| <img src="https://placehold.co/20x20/65d5d2/65d5d2" width="20" height="20" alt="#65d5d2"> | Sea Salt | `#65d5d2` | `rgb(101, 213, 210)` | `oklch(80.7% 0.102 193.0)` | Renamed, auxiliary |
| <img src="https://placehold.co/20x20/78aee6/78aee6" width="20" height="20" alt="#78aee6"> | Sky | `#78aee6` | `rgb(120, 174, 230)` | `oklch(73.5% 0.100 250.2)` | Information |
| <img src="https://placehold.co/20x20/db8dc7/db8dc7" width="20" height="20" alt="#db8dc7"> | Orchid | `#db8dc7` | `rgb(219, 141, 199)` | `oklch(74.1% 0.120 336.7)` | Conflict |
| <img src="https://placehold.co/20x20/fcd6b7/fcd6b7" width="20" height="20" alt="#fcd6b7"> | Ember | `#fcd6b7` | `rgb(252, 214, 183)` | `oklch(90.0% 0.059 61.2)` | Parameters |

</details>

<details>
<summary><b>Dawn</b></summary>
<br>

<img src="https://placehold.co/24x24/dfe1e3/dfe1e3" width="24" height="24" alt="#dfe1e3"><img src="https://placehold.co/24x24/e6e8e8/e6e8e8" width="24" height="24" alt="#e6e8e8"><img src="https://placehold.co/24x24/eeeeef/eeeeef" width="24" height="24" alt="#eeeeef"><img src="https://placehold.co/24x24/dbdedf/dbdedf" width="24" height="24" alt="#dbdedf"><img src="https://placehold.co/24x24/c4cace/c4cace" width="24" height="24" alt="#c4cace"><img src="https://placehold.co/24x24/6c818f/6c818f" width="24" height="24" alt="#6c818f"><img src="https://placehold.co/24x24/4f6574/4f6574" width="24" height="24" alt="#4f6574"><img src="https://placehold.co/24x24/364855/364855" width="24" height="24" alt="#364855"><img src="https://placehold.co/24x24/1f2931/1f2931" width="24" height="24" alt="#1f2931"><img src="https://placehold.co/24x24/11171b/11171b" width="24" height="24" alt="#11171b">&nbsp;&nbsp;<img src="https://placehold.co/24x24/ff7d00/ff7d00" width="24" height="24" alt="#ff7d00"><img src="https://placehold.co/24x24/8d3826/8d3826" width="24" height="24" alt="#8d3826"><img src="https://placehold.co/24x24/766014/766014" width="24" height="24" alt="#766014"><img src="https://placehold.co/24x24/39713a/39713a" width="24" height="24" alt="#39713a"><img src="https://placehold.co/24x24/176a7e/176a7e" width="24" height="24" alt="#176a7e"><img src="https://placehold.co/24x24/3f4880/3f4880" width="24" height="24" alt="#3f4880"><img src="https://placehold.co/24x24/813b67/813b67" width="24" height="24" alt="#813b67"><img src="https://placehold.co/24x24/67320a/67320a" width="24" height="24" alt="#67320a">

**Neutrals**

| | Name | Hex | RGB | OKLCH | Role |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/20x20/dfe1e3/dfe1e3" width="20" height="20" alt="#dfe1e3"> | Shell | `#dfe1e3` | `rgb(223, 225, 227)` | `oklch(90.9% 0.003 247.9)` | Outer frame |
| <img src="https://placehold.co/20x20/e6e8e8/e6e8e8" width="20" height="20" alt="#e6e8e8"> | Rail | `#e6e8e8` | `rgb(230, 232, 232)` | `oklch(92.9% 0.002 197.1)` | Docked panels |
| <img src="https://placehold.co/20x20/eeeeef/eeeeef" width="20" height="20" alt="#eeeeef"> | Canvas | `#eeeeef` | `rgb(238, 238, 239)` | `oklch(94.9% 0.001 0)` | Content |
| <img src="https://placehold.co/20x20/dbdedf/dbdedf" width="20" height="20" alt="#dbdedf"> | Raised | `#dbdedf` | `rgb(219, 222, 223)` | `oklch(89.9% 0.004 219.5)` | Floating layers |
| <img src="https://placehold.co/20x20/c4cace/c4cace" width="20" height="20" alt="#c4cace"> | Edge | `#c4cace` | `rgb(196, 202, 206)` | `oklch(83.6% 0.009 236.6)` | Dividers |
| <img src="https://placehold.co/20x20/6c818f/6c818f" width="20" height="20" alt="#6c818f"> | Control | `#6c818f` | `rgb(108, 129, 143)` | `oklch(59.1% 0.033 237.3)` | Control boundaries |
| <img src="https://placehold.co/20x20/4f6574/4f6574" width="20" height="20" alt="#4f6574"> | Faint | `#4f6574` | `rgb(79, 101, 116)` | `oklch(49.5% 0.036 238.2)` | Tertiary text |
| <img src="https://placehold.co/20x20/364855/364855" width="20" height="20" alt="#364855"> | Subtle | `#364855` | `rgb(54, 72, 85)` | `oklch(39.2% 0.032 240.0)` | Secondary text, icons |
| <img src="https://placehold.co/20x20/1f2931/1f2931" width="20" height="20" alt="#1f2931"> | Body | `#1f2931` | `rgb(31, 41, 49)` | `oklch(27.5% 0.020 242.6)` | Default text |
| <img src="https://placehold.co/20x20/11171b/11171b" width="20" height="20" alt="#11171b"> | Ink | `#11171b` | `rgb(17, 23, 27)` | `oklch(20.0% 0.012 237.4)` | Titles, focus |

**Colors**

| | Name | Hex | RGB | OKLCH | Meaning |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/20x20/ff7d00/ff7d00" width="20" height="20" alt="#ff7d00"> | Afterglow | `#ff7d00` | `rgb(255, 125, 0)` | `oklch(72.7% 0.188 51.7)` | Default accent |
| <img src="https://placehold.co/20x20/8d3826/8d3826" width="20" height="20" alt="#8d3826"> | Coral | `#8d3826` | `rgb(141, 56, 38)` | `oklch(45.5% 0.120 33.6)` | Error, removed |
| <img src="https://placehold.co/20x20/766014/766014" width="20" height="20" alt="#766014"> | Gold | `#766014` | `rgb(118, 96, 20)` | `oklch(49.7% 0.094 91.5)` | Warning, modified |
| <img src="https://placehold.co/20x20/39713a/39713a" width="20" height="20" alt="#39713a"> | Grove | `#39713a` | `rgb(57, 113, 58)` | `oklch(49.6% 0.104 144.2)` | Success, added |
| <img src="https://placehold.co/20x20/176a7e/176a7e" width="20" height="20" alt="#176a7e"> | Sea Salt | `#176a7e` | `rgb(23, 106, 126)` | `oklch(48.7% 0.081 218.5)` | Renamed, auxiliary |
| <img src="https://placehold.co/20x20/3f4880/3f4880" width="20" height="20" alt="#3f4880"> | Sky | `#3f4880` | `rgb(63, 72, 128)` | `oklch(42.2% 0.093 274.8)` | Information |
| <img src="https://placehold.co/20x20/813b67/813b67" width="20" height="20" alt="#813b67"> | Orchid | `#813b67` | `rgb(129, 59, 103)` | `oklch(45.9% 0.111 343.8)` | Conflict |
| <img src="https://placehold.co/20x20/67320a/67320a" width="20" height="20" alt="#67320a"> | Ember | `#67320a` | `rgb(103, 50, 10)` | `oklch(38.1% 0.090 51.8)` | Parameters |

</details>

Machine-readable values for both flavors, all accents, background states and the 16 terminal colors are in [palette/twilight.json](palette/twilight.json).

## Guarantees

| | Dusk | Dawn |
|---|---|---|
| Body text on any surface | 10.9:1 | 10.9:1 |
| Faintest text on any surface | 4.5:1 | 4.5:1 |
| Code colors on every code surface | 7.0:1 | 4.5:1 |
| Control boundaries and focus | 3.0:1 | 3.0:1 |
| Smallest code-color difference, color-vision deficiency | ΔE 0.061 | ΔE 0.040 |
| Pure black or white | none | none |

Contrast is WCAG 2.x, measured on final sRGB values. The color-vision figure is the worst case across simulated deuteranopia, protanopia and tritanopia. Full tables are in the [design system](docs/design-system.md#13-guarantees).

## How it was built

All math is done in OKLCH and checked in sRGB. Afterglow is the most chromatic orange sRGB holds at the seed's hue, and the neutrals sit at the exact complement of that hue. Dusk's surface lightness follows a geometric progression; Dawn keeps the same perceptual distances at the light end of the curve. Text levels are solved by contrast target. The six terminal hues are anchored to the ANSI standard, placed at each hue's natural lightness and lit by one shared warm chroma law. Those six and Ember were then optimized together for distinctness under four vision models. Each code category has one color, and Coral and Afterglow never color code.

The full derivation, with every formula and parameter, is in [construction.md](docs/construction.md).

## Using Twilight

Twilight is defined independently of any application. To build a theme for a tool, map its regions to the surface roles and follow the checklist in [Building a theme from this definition](docs/design-system.md#12-building-a-theme-from-this-definition).

## Repository

```
.
├── README.md
├── .agents/skills/
│   └── twilight-auditor/    audit skill: floors, reproduction, consistency
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
