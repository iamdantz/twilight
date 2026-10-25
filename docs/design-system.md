# Twilight design system

Version 1.12 · Flavors: Dusk (dark), Dawn (light)

This document defines Twilight: what each color is, what it means, where it may go, and what it guarantees. It does not describe any particular application. A theme for any tool can be built from it by mapping that tool's regions onto the roles below.

How the values were derived is in [construction.md](construction.md). All values in machine-readable form are in [palette/twilight.json](../palette/twilight.json).

## Contents

1. [Principles](#1-principles)
2. [Palette](#2-palette)
3. [Surfaces](#3-surfaces)
4. [Text and control levels](#4-text-and-control-levels)
5. [Accents](#5-accents)
6. [Colors](#6-colors)
7. [Syntax roles](#7-syntax-roles)
8. [Semantic states](#8-semantic-states)
9. [Background states](#9-background-states)
10. [Terminal colors](#10-terminal-colors)
11. [Rules](#11-rules)
12. [Applying the system](#12-applying-the-system)
13. [How not to apply](#13-how-not-to-apply)
14. [Guarantees](#14-guarantees)

## 1. Principles

1. **One seed, everything else derived.** The seed `#ee7a1f` is the only color chosen by hand. Afterglow is the most chromatic orange sRGB holds at the seed's hue, and the neutrals sit at the exact complement of that hue (232°).
2. **Every color has a role.** If something is colored, the color carries meaning.
3. **Contrast is solved against the hardest case.** Each text level, control boundary and code color is solved against the most demanding surface it can appear on, so it holds on all of them.
4. **The accent is a detail.** It marks focus, activity and the main action. It never fills large areas and never colors content.
5. **No pure black or white.** The darkest value is L <!-- fact:darkest -->0.15<!-- /fact --> and the lightest is L <!-- fact:lightest -->0.95<!-- /fact --> (Dawn `diff-inserted` renders at 0.950 after 8-bit rounding).
6. **One system, two categories.** Every flavor is dark or light. All flavors share every role and rule and the same neutral curve; where a rule differs between dark and light, it says so, and every flavor of that category follows it. Dusk is dark; Dawn is light and uses the light end of the curve, with Dusk's Canvas and Ink in exchanged roles.

## 2. Palette

The palette has ten neutrals and eight colors per flavor. Token names are lowercase and hyphenated (`sea-salt`, `accent-focus`). Names refer to roles, so `canvas` is dark in a dark flavor and light in a light one.

### Dusk

| | Token | Hex | OKLCH | vs Shell | vs Rail | vs Canvas | vs Raised |
|:-:|---|---|---|---|---|---|---|
| <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> | `shell` | `#090c0f` | `oklch(15.2% 0.008 248.1)` | 1.00 | 1.04 | 1.09 | 1.28 |
| <img src="https://placehold.co/16x16/0e1215/0e1215" width="16" height="16" alt="#0e1215"> | `rail` | `#0e1215` | `oklch(17.9% 0.009 240.5)` | 1.04 | 1.00 | 1.04 | 1.23 |
| <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> | `canvas` | `#11171b` | `oklch(20.0% 0.012 237.4)` | 1.09 | 1.04 | 1.00 | 1.18 |
| <img src="https://placehold.co/16x16/1d262d/1d262d" width="16" height="16" alt="#1d262d"> | `raised` | `#1d262d` | `oklch(26.3% 0.018 241.8)` | 1.28 | 1.23 | 1.18 | 1.00 |
| <img src="https://placehold.co/16x16/2c3b46/2c3b46" width="16" height="16" alt="#2c3b46"> | `edge` | `#2c3b46` | `oklch(34.4% 0.028 240.4)` | 1.70 | 1.63 | 1.57 | 1.33 |
| <img src="https://placehold.co/16x16/5a717f/5a717f" width="16" height="16" alt="#5a717f"> | `control` | `#5a717f` | `oklch(53.5% 0.035 235.0)` | 3.83 | 3.68 | 3.53 | 3.00 |
| <img src="https://placehold.co/16x16/7a8e9a/7a8e9a" width="16" height="16" alt="#7a8e9a"> | `faint` | `#7a8e9a` | `oklch(63.5% 0.029 234.3)` | 5.75 | 5.52 | 5.30 | 4.51 |
| <img src="https://placehold.co/16x16/a5b1b8/a5b1b8" width="16" height="16" alt="#a5b1b8"> | `subtle` | `#a5b1b8` | `oklch(75.3% 0.017 233.1)` | 8.94 | 8.58 | 8.24 | 7.01 |
| <img src="https://placehold.co/16x16/d6dadb/d6dadb" width="16" height="16" alt="#d6dadb"> | `body` | `#d6dadb` | `oklch(88.6% 0.005 214.3)` | 13.92 | 13.36 | 12.83 | 10.90 |
| <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> | `ink` | `#eeeeef` | `oklch(94.9% 0.001 0)` | 16.91 | 16.23 | 15.58 | 13.25 |

| | Token | Hex | OKLCH | On Canvas | Worst code surface |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/ff7d00/ff7d00" width="16" height="16" alt="#ff7d00"> | `afterglow` | `#ff7d00` | `oklch(72.7% 0.188 51.7)` | 7.04 | — |
| <img src="https://placehold.co/16x16/ee8476/ee8476" width="16" height="16" alt="#ee8476"> | `coral` | `#ee8476` | `oklch(72.6% 0.132 28.6)` | 7.05 | 7.00 |
| <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> | `gold` | `#dbba50` | `oklch(79.8% 0.129 91.9)` | 9.60 | 9.53 |
| <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> | `grove` | `#99d086` | `oklch(80.1% 0.116 137.9)` | 10.08 | 10.01 |
| <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> | `sea-salt` | `#65d5d2` | `oklch(80.7% 0.102 193.0)` | 10.33 | 10.25 |
| <img src="https://placehold.co/16x16/78aee6/78aee6" width="16" height="16" alt="#78aee6"> | `sky` | `#78aee6` | `oklch(73.5% 0.100 250.2)` | 7.74 | 7.69 |
| <img src="https://placehold.co/16x16/db8dc7/db8dc7" width="16" height="16" alt="#db8dc7"> | `orchid` | `#db8dc7` | `oklch(74.1% 0.120 336.7)` | 7.44 | 7.39 |
| <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> | `ember` | `#fcd6b7` | `oklch(90.0% 0.059 61.2)` | 13.29 | 13.19 |

### Dawn

| | Token | Hex | OKLCH | vs Shell | vs Rail | vs Canvas | vs Raised |
|:-:|---|---|---|---|---|---|---|
| <img src="https://placehold.co/16x16/dcdee0/dcdee0" width="16" height="16" alt="#dcdee0"> | `shell` | `#dcdee0` | `oklch(90.0% 0.003 247.9)` | 1.00 | 1.08 | 1.16 | 1.04 |
| <img src="https://placehold.co/16x16/e5e6e7/e5e6e7" width="16" height="16" alt="#e5e6e7"> | `rail` | `#e5e6e7` | `oklch(92.4% 0.002 247.8)` | 1.08 | 1.00 | 1.08 | 1.13 |
| <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> | `canvas` | `#eeeeef` | `oklch(94.9% 0.001 0)` | 1.16 | 1.08 | 1.00 | 1.21 |
| <img src="https://placehold.co/16x16/d6dadc/d6dadc" width="16" height="16" alt="#d6dadc"> | `raised` | `#d6dadc` | `oklch(88.6% 0.005 228.8)` | 1.04 | 1.13 | 1.21 | 1.00 |
| <img src="https://placehold.co/16x16/b8c1c6/b8c1c6" width="16" height="16" alt="#b8c1c6"> | `edge` | `#b8c1c6` | `oklch(80.5% 0.012 231.7)` | 1.36 | 1.46 | 1.58 | 1.30 |
| <img src="https://placehold.co/16x16/697e8c/697e8c" width="16" height="16" alt="#697e8c"> | `control` | `#697e8c` | `oklch(58.1% 0.033 237.3)` | 3.14 | 3.39 | 3.65 | 3.01 |
| <img src="https://placehold.co/16x16/4d6271/4d6271" width="16" height="16" alt="#4d6271"> | `faint` | `#4d6271` | `oklch(48.5% 0.035 239.5)` | 4.72 | 5.09 | 5.49 | 4.52 |
| <img src="https://placehold.co/16x16/344552/344552" width="16" height="16" alt="#344552"> | `subtle` | `#344552` | `oklch(38.1% 0.031 241.5)` | 7.35 | 7.93 | 8.55 | 7.04 |
| <img src="https://placehold.co/16x16/1d262e/1d262e" width="16" height="16" alt="#1d262e"> | `body` | `#1d262e` | `oklch(26.4% 0.020 245.5)` | 11.37 | 12.28 | 13.23 | 10.90 |
| <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> | `ink` | `#11171b` | `oklch(20.0% 0.012 237.4)` | 13.40 | 14.46 | 15.58 | 12.84 |

| | Token | Hex | OKLCH | On Canvas | Worst code surface |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/ff7d00/ff7d00" width="16" height="16" alt="#ff7d00"> | `afterglow` | `#ff7d00` | `oklch(72.7% 0.188 51.7)` | 2.21 | — |
| <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> | `coral` | `#8d3826` | `oklch(45.5% 0.120 33.6)` | 6.64 | 5.97 |
| <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> | `gold` | `#766014` | `oklch(49.7% 0.094 91.5)` | 5.24 | 4.71 |
| <img src="https://placehold.co/16x16/39713a/39713a" width="16" height="16" alt="#39713a"> | `grove` | `#39713a` | `oklch(49.6% 0.104 144.2)` | 5.04 | 4.52 |
| <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> | `sea-salt` | `#176a7e` | `oklch(48.7% 0.081 218.5)` | 5.33 | 4.79 |
| <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> | `sky` | `#3f4880` | `oklch(42.2% 0.093 274.8)` | 7.39 | 6.64 |
| <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> | `orchid` | `#813b67` | `oklch(45.9% 0.111 343.8)` | 6.57 | 5.90 |
| <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> | `ember` | `#67320a` | `oklch(38.1% 0.090 51.8)` | 8.89 | 7.98 |

*Worst code surface* is the lowest contrast across Canvas and both diff backgrounds, the surfaces where code is drawn. Afterglow is not a code color, so it has no entry.

## 3. Surfaces

Five neutrals form the spatial structure of an interface.

| Surface | Role | Typical regions |
|---|---|---|
| **Shell** | Outer frame | Title bars, primary navigation strips, status bars, inactive tabs |
| **Rail** | Docked panels, half a step between Shell and Canvas | Sidebars, trees and file lists, tab strips, bottom panel headers |
| **Canvas** | Content | Documents, pages, code, terminal output, the active tab |
| **Raised** | Floating layers without code | Menus, command palettes, dropdowns, dialogs, notifications, tooltips, text fields, hovered rows, inline hints |
| **Edge** | One-pixel structure | Dividers, outlines of floating layers, current-line border, indent guides, scrollbar thumb at rest |

In Dusk the surfaces get lighter as they come forward: <!-- fact:dusk.surfaces -->Shell (L 0.15), Rail (0.18), Canvas (0.20), Raised (0.26), Edge (0.34)<!-- /fact -->. In Dawn, Canvas is the lightest (L <!-- fact:dawn.canvas_L -->0.95<!-- /fact -->) and the others step down from it at the same perceptual distance from Canvas as in Dusk: <!-- fact:dawn.surfaces -->Rail (0.92), Shell (0.90), Raised (0.89), Edge (0.81)<!-- /fact -->.

Separation between surfaces is deliberately low (Dusk <!-- fact:dusk.separation -->1.04 to 1.28<!-- /fact -->:1, Dawn <!-- fact:dawn.separation -->1.04 to 1.21<!-- /fact -->:1). Tone tells surfaces apart; Edge lines and Control boundaries carry the structure that has to be seen.

## 4. Text and control levels

Each level is solved against Raised, the hardest surface for text in every flavor.

| Level | Minimum on any surface | Use |
|---|---|---|
| **Ink** | 12.84:1 | Titles, headings, focused and selected items |
| **Body** | 10.90:1 | Default text; variables and properties in code |
| **Subtle** | 7.01:1 | Secondary labels, icons, placeholders; punctuation and operators in code |
| **Faint** | 4.51:1 | Metadata, line numbers, inactive tabs, comments, hints, ignored items |
| **Control** | 3.00:1 | Boundaries of text fields, checkboxes, selects and toggles; disabled glyphs; active indent guide; scrollbar thumb on hover |

The text steps are geometric: 4.5, 7.0, 10.9.

Placeholders use Subtle, never Faint. A placeholder can sit on Raised, and reading it is part of recognizing the field.

## 5. Accents

Afterglow is the accent of every Twilight theme, and a theme is named by its flavor alone: *Twilight Dusk*, *Twilight Dawn*.

The other seven colors also have accent families, built and validated by the same rules and published in [palette/twilight.json](../palette/twilight.json). No theme uses them as an accent. Their `accent-text` is the text variant of each semantic color ([§8](#8-semantic-states)); the other tokens are kept so the accent can become a choice without changing any other token.

Each family provides five tokens:

| Token | Use | Rule |
|---|---|---|
| `accent` | Fills: badges, the main button, progress | The color itself |
| `on-accent` | Text and icons on `accent` and `accent-pressed` | The extreme neutral with the higher contrast on `accent` |
| `accent-text` | Links, matched characters in lists; text in a semantic color (§8) | The color itself if it reaches the code floor of its category on Raised (7:1 dark, 4.5:1 light); otherwise moved in lightness until it does |
| `accent-pressed` | Pressed and hover state of filled controls | `accent` darkened by up to 0.10 L, stopping early if `on-accent` would drop below 4.5:1 |
| `accent-focus` | Focus rings, active indicators; Afterglow's is also the cursor | The color itself if it reaches 3:1 on every surface; otherwise moved in lightness until it does |

Every variant keeps the hue and relative chroma of its color. Only lightness changes.

### Dusk

| Accent | `accent` | `accent-text` | `accent-pressed` | `accent-focus` | `on-accent` |
|---|---|---|---|---|---|
| Afterglow | <img src="https://placehold.co/16x16/ff7d00/ff7d00" width="16" height="16" alt="#ff7d00"> `#ff7d00` | <img src="https://placehold.co/16x16/ff944d/ff944d" width="16" height="16" alt="#ff944d"> `#ff944d` | <img src="https://placehold.co/16x16/d26600/d26600" width="16" height="16" alt="#d26600"> `#d26600` | <img src="https://placehold.co/16x16/ff7d00/ff7d00" width="16" height="16" alt="#ff7d00"> `#ff7d00` | <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> `#090c0f` |
| Coral | <img src="https://placehold.co/16x16/ee8476/ee8476" width="16" height="16" alt="#ee8476"> `#ee8476` | <img src="https://placehold.co/16x16/f0988c/f0988c" width="16" height="16" alt="#f0988c"> `#f0988c` | <img src="https://placehold.co/16x16/e8473a/e8473a" width="16" height="16" alt="#e8473a"> `#e8473a` | <img src="https://placehold.co/16x16/ee8476/ee8476" width="16" height="16" alt="#ee8476"> `#ee8476` | <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> `#090c0f` |
| Gold | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/16x16/b79b41/b79b41" width="16" height="16" alt="#b79b41"> `#b79b41` | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> `#090c0f` |
| Grove | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> `#99d086` | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> `#99d086` | <img src="https://placehold.co/16x16/7fae6f/7fae6f" width="16" height="16" alt="#7fae6f"> `#7fae6f` | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> `#99d086` | <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> `#090c0f` |
| Sea Salt | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> `#65d5d2` | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> `#65d5d2` | <img src="https://placehold.co/16x16/53b2b0/53b2b0" width="16" height="16" alt="#53b2b0"> `#53b2b0` | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> `#65d5d2` | <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> `#090c0f` |
| Sky | <img src="https://placehold.co/16x16/78aee6/78aee6" width="16" height="16" alt="#78aee6"> `#78aee6` | <img src="https://placehold.co/16x16/82b4e8/82b4e8" width="16" height="16" alt="#82b4e8"> `#82b4e8` | <img src="https://placehold.co/16x16/498fd4/498fd4" width="16" height="16" alt="#498fd4"> `#498fd4` | <img src="https://placehold.co/16x16/78aee6/78aee6" width="16" height="16" alt="#78aee6"> `#78aee6` | <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> `#090c0f` |
| Orchid | <img src="https://placehold.co/16x16/db8dc7/db8dc7" width="16" height="16" alt="#db8dc7"> `#db8dc7` | <img src="https://placehold.co/16x16/de9acc/de9acc" width="16" height="16" alt="#de9acc"> `#de9acc` | <img src="https://placehold.co/16x16/c365ad/c365ad" width="16" height="16" alt="#c365ad"> `#c365ad` | <img src="https://placehold.co/16x16/db8dc7/db8dc7" width="16" height="16" alt="#db8dc7"> `#db8dc7` | <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> `#090c0f` |
| Ember | <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/16x16/f9aa63/f9aa63" width="16" height="16" alt="#f9aa63"> `#f9aa63` | <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/16x16/090c0f/090c0f" width="16" height="16" alt="#090c0f"> `#090c0f` |

| Accent | Label on fill | Label on pressed | Text on Raised | Focus, worst surface |
|---|---|---|---|---|
| Afterglow | 7.64 | 5.27 | 7.02 | 5.99 |
| Coral | 7.65 | 5.04 | 7.00 | 6.00 |
| Gold | 10.41 | 7.26 | 8.16 | 8.16 |
| Grove | 10.94 | 7.64 | 8.57 | 8.57 |
| Sea Salt | 11.20 | 7.81 | 8.78 | 8.78 |
| Sky | 8.40 | 5.75 | 7.05 | 6.58 |
| Orchid | 8.07 | 5.40 | 7.02 | 6.32 |
| Ember | 14.42 | 10.23 | 11.29 | 11.29 |

### Dawn

| Accent | `accent` | `accent-text` | `accent-pressed` | `accent-focus` | `on-accent` |
|---|---|---|---|---|---|
| Afterglow | <img src="https://placehold.co/16x16/ff7d00/ff7d00" width="16" height="16" alt="#ff7d00"> `#ff7d00` | <img src="https://placehold.co/16x16/994900/994900" width="16" height="16" alt="#994900"> `#994900` | <img src="https://placehold.co/16x16/d26600/d26600" width="16" height="16" alt="#d26600"> `#d26600` | <img src="https://placehold.co/16x16/c45e00/c45e00" width="16" height="16" alt="#c45e00"> `#c45e00` | <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> `#11171b` |
| Coral | <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> `#8d3826` | <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> `#8d3826` | <img src="https://placehold.co/16x16/642518/642518" width="16" height="16" alt="#642518"> `#642518` | <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> `#8d3826` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Gold | <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> `#766014` | <img src="https://placehold.co/16x16/735d13/735d13" width="16" height="16" alt="#735d13"> `#735d13` | <img src="https://placehold.co/16x16/56450c/56450c" width="16" height="16" alt="#56450c"> `#56450c` | <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> `#766014` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Grove | <img src="https://placehold.co/16x16/39713a/39713a" width="16" height="16" alt="#39713a"> `#39713a` | <img src="https://placehold.co/16x16/366b37/366b37" width="16" height="16" alt="#366b37"> `#366b37` | <img src="https://placehold.co/16x16/285228/285228" width="16" height="16" alt="#285228"> `#285228` | <img src="https://placehold.co/16x16/39713a/39713a" width="16" height="16" alt="#39713a"> `#39713a` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Sea Salt | <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> `#176a7e` | <img src="https://placehold.co/16x16/17687c/17687c" width="16" height="16" alt="#17687c"> `#17687c` | <img src="https://placehold.co/16x16/0e4c5b/0e4c5b" width="16" height="16" alt="#0e4c5b"> `#0e4c5b` | <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> `#176a7e` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Sky | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> `#3f4880` | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> `#3f4880` | <img src="https://placehold.co/16x16/292f57/292f57" width="16" height="16" alt="#292f57"> `#292f57` | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> `#3f4880` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Orchid | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> `#813b67` | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> `#813b67` | <img src="https://placehold.co/16x16/5b2848/5b2848" width="16" height="16" alt="#5b2848"> `#5b2848` | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> `#813b67` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Ember | <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> `#67320a` | <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> `#67320a` | <img src="https://placehold.co/16x16/421e04/421e04" width="16" height="16" alt="#421e04"> `#421e04` | <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> `#67320a` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |

| Accent | Label on fill | Label on pressed | Text on Raised | Focus, worst surface |
|---|---|---|---|---|
| Afterglow | 7.04 | 4.85 | 4.51 | 3.02 |
| Coral | 6.64 | 9.95 | 5.47 | 5.47 |
| Gold | 5.24 | 8.04 | 4.52 | 4.32 |
| Grove | 5.04 | 7.78 | 4.50 | 4.15 |
| Sea Salt | 5.33 | 8.22 | 4.51 | 4.39 |
| Sky | 7.39 | 11.05 | 6.09 | 6.09 |
| Orchid | 6.57 | 9.83 | 5.42 | 5.42 |
| Ember | 8.89 | 12.76 | 7.32 | 7.32 |

### Where the accent goes

- Focus rings and outlines: `accent-focus`
- Active indicators, such as a 2 px line on the active tab, the active item in a navigation strip, the active panel title: `accent-focus`
- Badges and counters: `accent` with `on-accent`
- The single main action of a view: `accent`, `accent-pressed`, `on-accent`
- Progress indicators: `accent`
- Links and matched characters: `accent-text`. Links in running text are also underlined, or marked by an icon where an underline cannot be drawn. No `accent-text` reaches 3:1 against Body (Dusk <!-- fact:dusk.link_body -->1.04–1.56<!-- /fact -->, Dawn <!-- fact:dawn.link_body -->1.49–2.42<!-- /fact -->), so color alone cannot separate a link from the text around it (WCAG 2.2 SC 1.4.1, technique G183). With Afterglow, `accent-text` is also ΔE_OK <!-- fact:dusk.link_coral -->0.074<!-- /fact --> (Dusk) and <!-- fact:dawn.link_coral -->0.059<!-- /fact --> (Dawn) from Coral, below the smallest code-color difference ([§14](#14-guarantees)). Links whose role is clear from position, such as navigation items and buttons, need no extra cue.
- A small emblem: `accent-focus`

### Where it never goes

- Large fills: frames, toolbars, sidebars, backgrounds, headers
- Content: code, terminal output, body text
- Semantic meaning: the accent never signals error, warning or success
- Data series ([§12.4](#124-data-visualization))
- Gradients or washes

A view should contain one accent element besides focus and cursor indicators.

### What the accent does not change

Code colors, semantic states, background states (including selection), the cursor and terminal colors belong to the flavor and would stay identical whatever the accent. Background-state hues were allocated so that no two collide, and letting the accent tint them would break that.

The cursor is Afterglow's `accent-focus`, the color the code colors are optimized against ([construction.md §6.5](construction.md#65-joint-optimization)). Text under it is Afterglow's `on-accent`.

## 6. Colors

Six of the eight colors fill the ANSI chromatic slots and are anchored to the corners of the RGB cube, so their meaning matches what terminals and tools expect. Ember is a seventh code color in Afterglow's hue family. Afterglow is the accent; it is computed from the seed and is not a code color.

| Color | ANSI slot | Semantic meaning | Code role |
|---|---|---|---|
| **Afterglow** | none | Accent and cursor; tints selection | None |
| **Coral** | red | Error, destructive, removed, invalid | Invalid code only |
| **Gold** | yellow | Warning, modified | Constants |
| **Grove** | green | Success, added, untracked | Strings |
| **Sea Salt** | cyan | Renamed, auxiliary information | Types |
| **Sky** | blue | Information, remote references | Functions |
| **Orchid** | magenta | Conflict | Keywords |
| **Ember** | none | None | Parameters |

Coral is reserved for danger. It never colors a frequent code category, so an error always stands out.

## 7. Syntax roles

The mapping is fixed by [construction.md, section 8](construction.md#8-syntax-roles). Categories are named generically so they map onto any grammar.

| Category | Includes | Color | Style |
|---|---|---|---|
| Keyword | Control flow, declarations, storage, modifiers, word operators, arrows, markup tags | Orchid | |
| Function | Function and method names, decorators, prose headings | Sky | |
| Type | Types, classes, interfaces, enums, namespaces, built-in types | Sea Salt | |
| String | Strings, template strings, regular expressions, inline code | Grove | |
| Escape | Escape sequences, interpolation delimiters, regex quantifiers | Orchid | |
| Constant | Numbers, booleans, null, enum members, `ALL_CAPS` constants, units | Gold | |
| Language self | `this`, `self`, `super` | Gold | italic |
| Parameter | Parameters, type parameters, markup attributes | Ember | italic |
| Variable, property | Variables, object properties, keys | Body | |
| Punctuation, operator | Brackets, separators, symbolic operators | Subtle | |
| Comment | Comments, documentation blocks | Faint | italic |
| Invalid | Illegal syntax | Coral | underline |
| Deprecated | Deprecated symbols | Faint | strikethrough |
| Prose emphasis | Bold, italic | Ink bold, Body italic | |
| Prose link | Links in markup | `accent-text` | |
| Prose quote | Block quotes | Faint | italic |
| Diff | Inserted, deleted, changed lines in patch files | Grove, Coral, Gold | |

Only comments, parameters and `this`/`self` are italic.

Properties are uncolored on purpose, so code is not colored end to end.

## 8. Semantic states

| State | Color | Applies to |
|---|---|---|
| Error | Coral | Diagnostics, failed checks, destructive actions, removed items |
| Warning | Gold | Warnings, modified items |
| Success | Grove | Passed checks, added and untracked items |
| Information | Sky | Notices that carry content |
| Hint | Faint | Low-priority suggestions |
| Conflict | Orchid | Merge conflicts |
| Renamed | Sea Salt | Renamed or moved items |
| Ignored, inactive | Faint | Ignored files, dead code, disabled items |

Version-control markers (gutter bars, file decorations) follow the same mapping: added Grove, modified Gold, removed Coral, renamed Sea Salt, ignored Faint, conflict Orchid. Every marker also carries a letter or an icon. Under color-vision deficiency, Faint sits only <!-- fact:dawn.faint_semantic -->1.05<!-- /fact --> JND from the nearest semantic color in Dawn (Dusk: <!-- fact:dusk.faint_semantic -->3.30<!-- /fact -->), so color alone cannot separate an ignored item from an added one ([construction.md §11](construction.md#11-known-limits)).

Icons, markers and 3 px bars use the semantic color itself, which reaches at least <!-- fact:min.semantic_surfaces -->3.19<!-- /fact -->:1 on every surface and on Edge. Text in a semantic color uses that color's `accent-text` ([§5](#5-accents)), which meets the code floor of its category (7:1 dark, 4.5:1 light) on every surface. The colors themselves are not enough for text: in Dawn, Grove, Gold and Sea Salt stay below 4.5:1 on Raised. On a filled chip, the label is Shell in dark flavors and Canvas in light ones. Both reach at least <!-- fact:chip -->5.04<!-- /fact -->:1 on every semantic color.

## 9. Background states

Visibility is measured in JND, just-noticeable differences, where 1 JND is ΔE 0.02 in OKLab, measured against Canvas.

- **Transient** states (selection, search matches, word highlights) may change lightness, but Faint text must keep 4.5:1 on them.
- **Persistent** states (diff lines) are treated as code surfaces. Code colors are validated on them and keep their full minimum.
- **Apart from each other.** Every state is at least 1 JND from every other state, so a read and a write highlight, or the current and other search matches, never look the same.

### Dusk

| | Token | Hex | Hue from | Visibility | Kind |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/391e0c/391e0c" width="16" height="16" alt="#391e0c"> | `selection` | `#391e0c` | Afterglow | 4.6 JND | transient |
| <img src="https://placehold.co/16x16/260f02/260f02" width="16" height="16" alt="#260f02"> | `selection-inactive` | `#260f02` | Afterglow | 2.9 JND | transient |
| <img src="https://placehold.co/16x16/2c240b/2c240b" width="16" height="16" alt="#2c240b"> | `find-match` | `#2c240b` | Gold | 4.1 JND | transient |
| <img src="https://placehold.co/16x16/1b1606/1b1606" width="16" height="16" alt="#1b1606"> | `find-match-other` | `#1b1606` | Gold | 2.0 JND | transient |
| <img src="https://placehold.co/16x16/062221/062221" width="16" height="16" alt="#062221"> | `word-highlight` | `#062221` | Sea Salt | 2.0 JND | transient |
| <img src="https://placehold.co/16x16/0f2929/0f2929" width="16" height="16" alt="#0f2929"> | `word-highlight-write` | `#0f2929` | Sea Salt | 3.3 JND | transient |
| <img src="https://placehold.co/16x16/0e1a09/0e1a09" width="16" height="16" alt="#0e1a09"> | `diff-inserted` | `#0e1a09` | Grove | 2.0 JND | persistent |
| <img src="https://placehold.co/16x16/22110e/22110e" width="16" height="16" alt="#22110e"> | `diff-removed` | `#22110e` | Coral | 2.0 JND | persistent |

### Dawn

| | Token | Hex | Hue from | Visibility | Kind |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/ead5c9/ead5c9" width="16" height="16" alt="#ead5c9"> | `selection` | `#ead5c9` | Afterglow | 3.5 JND | transient |
| <img src="https://placehold.co/16x16/f5e0d4/f5e0d4" width="16" height="16" alt="#f5e0d4"> | `selection-inactive` | `#f5e0d4` | Afterglow | 2.1 JND | transient |
| <img src="https://placehold.co/16x16/ead8a6/ead8a6" width="16" height="16" alt="#ead8a6"> | `find-match` | `#ead8a6` | Gold | 4.7 JND | transient |
| <img src="https://placehold.co/16x16/f8eed1/f8eed1" width="16" height="16" alt="#f8eed1"> | `find-match-other` | `#f8eed1` | Gold | 2.0 JND | transient |
| <img src="https://placehold.co/16x16/ceeef8/ceeef8" width="16" height="16" alt="#ceeef8"> | `word-highlight` | `#ceeef8` | Sea Salt | 2.0 JND | transient |
| <img src="https://placehold.co/16x16/c0dee8/c0dee8" width="16" height="16" alt="#c0dee8"> | `word-highlight-write` | `#c0dee8` | Sea Salt | 3.8 JND | transient |
| <img src="https://placehold.co/16x16/e0f6dd/e0f6dd" width="16" height="16" alt="#e0f6dd"> | `diff-inserted` | `#e0f6dd` | Grove | 2.1 JND | persistent |
| <img src="https://placehold.co/16x16/f4dde0/f4dde0" width="16" height="16" alt="#f4dde0"> | `diff-removed` | `#f4dde0` | Coral | 2.1 JND | persistent |

### Line structure

| Element | Token |
|---|---|
| Current line | 1 px top and bottom border in Edge. Never a fill, which would push comments below 4.5:1. |
| Indent guides | Edge; the active guide in Control |
| Bracket pairs, levels 1 to 3 | Gold, Orchid, Sea Salt; an unmatched bracket in Coral |
| Matching bracket | `word-highlight` with a Control outline |
| Current search match | `find-match` with a 1 px Gold outline |
| Scrollbar thumb | Edge at rest, Control on hover |

## 10. Terminal colors

The six chromatic normals are the six ANSI colors above. Each bright moves 0.38 of the way toward Ink, so brights are lighter in dark flavors and deeper in light ones. The step keeps every bright at least 2 JND from its normal and from Ink, and gives the twelve chromatic colors the largest closest pair under color-vision deficiency ([§14](#14-guarantees)).

### Dusk (background Canvas `#11171b`)

| # | Slot | | Hex | From | On Canvas |
|--:|---|:-:|---|---|---|
| 0 | black | <img src="https://placehold.co/16x16/2c3b46/2c3b46" width="16" height="16" alt="#2c3b46"> | `#2c3b46` | Edge | 1.57 |
| 1 | red | <img src="https://placehold.co/16x16/ee8476/ee8476" width="16" height="16" alt="#ee8476"> | `#ee8476` | Coral | 7.05 |
| 2 | green | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> | `#99d086` | Grove | 10.08 |
| 3 | yellow | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> | `#dbba50` | Gold | 9.60 |
| 4 | blue | <img src="https://placehold.co/16x16/78aee6/78aee6" width="16" height="16" alt="#78aee6"> | `#78aee6` | Sky | 7.74 |
| 5 | magenta | <img src="https://placehold.co/16x16/db8dc7/db8dc7" width="16" height="16" alt="#db8dc7"> | `#db8dc7` | Orchid | 7.44 |
| 6 | cyan | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> | `#65d5d2` | Sea Salt | 10.33 |
| 7 | white | <img src="https://placehold.co/16x16/a5b1b8/a5b1b8" width="16" height="16" alt="#a5b1b8"> | `#a5b1b8` | Subtle | 8.24 |
| 8 | bright black | <img src="https://placehold.co/16x16/7a8e9a/7a8e9a" width="16" height="16" alt="#7a8e9a"> | `#7a8e9a` | Faint | 5.30 |
| 9 | bright red | <img src="https://placehold.co/16x16/fba99d/fba99d" width="16" height="16" alt="#fba99d"> | `#fba99d` | Coral, brightened | 9.69 |
| 10 | bright green | <img src="https://placehold.co/16x16/abe398/abe398" width="16" height="16" alt="#abe398"> | `#abe398` | Grove, brightened | 12.19 |
| 11 | bright yellow | <img src="https://placehold.co/16x16/eecd64/eecd64" width="16" height="16" alt="#eecd64"> | `#eecd64` | Gold, brightened | 11.66 |
| 12 | bright blue | <img src="https://placehold.co/16x16/98c8fa/98c8fa" width="16" height="16" alt="#98c8fa"> | `#98c8fa` | Sky, brightened | 10.31 |
| 13 | bright magenta | <img src="https://placehold.co/16x16/f6a6e1/f6a6e1" width="16" height="16" alt="#f6a6e1"> | `#f6a6e1` | Orchid, brightened | 9.86 |
| 14 | bright cyan | <img src="https://placehold.co/16x16/78e7e4/78e7e4" width="16" height="16" alt="#78e7e4"> | `#78e7e4` | Sea Salt, brightened | 12.35 |
| 15 | bright white | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> | `#eeeeef` | Ink | 15.58 |

### Dawn (background Canvas `#eeeeef`)

| # | Slot | | Hex | From | On Canvas |
|--:|---|:-:|---|---|---|
| 0 | black | <img src="https://placehold.co/16x16/1d262e/1d262e" width="16" height="16" alt="#1d262e"> | `#1d262e` | Body | 13.23 |
| 1 | red | <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> | `#8d3826` | Coral | 6.64 |
| 2 | green | <img src="https://placehold.co/16x16/39713a/39713a" width="16" height="16" alt="#39713a"> | `#39713a` | Grove | 5.04 |
| 3 | yellow | <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> | `#766014` | Gold | 5.24 |
| 4 | blue | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> | `#3f4880` | Sky | 7.39 |
| 5 | magenta | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> | `#813b67` | Orchid | 6.57 |
| 6 | cyan | <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> | `#176a7e` | Sea Salt | 5.33 |
| 7 | white | <img src="https://placehold.co/16x16/b8c1c6/b8c1c6" width="16" height="16" alt="#b8c1c6"> | `#b8c1c6` | Edge | 1.58 |
| 8 | bright black | <img src="https://placehold.co/16x16/4d6271/4d6271" width="16" height="16" alt="#4d6271"> | `#4d6271` | Faint | 5.49 |
| 9 | bright red | <img src="https://placehold.co/16x16/6e1b08/6e1b08" width="16" height="16" alt="#6e1b08"> | `#6e1b08` | Coral, brightened | 9.93 |
| 10 | bright green | <img src="https://placehold.co/16x16/17511b/17511b" width="16" height="16" alt="#17511b"> | `#17511b` | Grove, brightened | 8.12 |
| 11 | bright yellow | <img src="https://placehold.co/16x16/52420b/52420b" width="16" height="16" alt="#52420b"> | `#52420b` | Gold, brightened | 8.45 |
| 12 | bright blue | <img src="https://placehold.co/16x16/2a3167/2a3167" width="16" height="16" alt="#2a3167"> | `#2a3167` | Sky, brightened | 10.45 |
| 13 | bright magenta | <img src="https://placehold.co/16x16/631f4c/631f4c" width="16" height="16" alt="#631f4c"> | `#631f4c` | Orchid, brightened | 9.89 |
| 14 | bright cyan | <img src="https://placehold.co/16x16/0d4958/0d4958" width="16" height="16" alt="#0d4958"> | `#0d4958` | Sea Salt, brightened | 8.58 |
| 15 | bright white | <img src="https://placehold.co/16x16/d6dadc/d6dadc" width="16" height="16" alt="#d6dadc"> | `#d6dadc` | Raised | 1.21 |

| Terminal role | Token |
|---|---|
| Background | Canvas |
| Foreground | Body |
| Bold | Ink |
| Cursor | Afterglow `accent-focus` |
| Text under cursor | Afterglow `on-accent` |
| Selection | `selection` |
| Links | `accent-text` |

Of black and white, the one that matches the background's polarity is a surface: Edge, as black in dark flavors and as white in light ones. Tools use it mostly as a background, so its contrast on Canvas is low by design. The other is a text level: Subtle as white in dark flavors, Body as black in light ones. Bright black is Faint and is readable as text.

## 11. Rules

1. **Content lives on Canvas.** Documents, code, terminal output and any floating layer that shows code (hovers, previews, completion lists) use Canvas with an Edge outline, never Raised.
2. **Shell frames, Rail docks, Raised floats.** Title, navigation and status bars go on Shell. Side panels, trees and tab strips go on Rail. Menus, palettes, fields and notifications go on Raised.
3. **The active tab is Canvas.** It merges with its content and carries a 2 px `accent-focus` line on its top edge.
4. **Text levels follow function.** Ink for titles and focus, Body for content, Subtle for secondary labels, icons and placeholders, Faint for metadata.
5. **Every interactive control has a Control boundary** (3:1 or more on all surfaces) and an `accent-focus` ring when focused.
6. **Semantic states never rely on color alone.** Pair them with an icon, label or position. Links in running text follow the same principle: they are underlined or marked by an icon ([§5](#where-the-accent-goes)).
7. **Coral only means danger.** Regular expressions use the string color; only invalid code is Coral.
8. **The accent marks focus, activity, the main action and links,** and nothing else.
9. **No color without a role.** Status bars, labels and file-type tags use neutrals.
10. **Terminals use only the sixteen ANSI colors.** Prompts and tools must not depend on others.
11. **The current line uses a border, not a fill.**
12. **New surfaces are derived.** If a tool needs a surface not listed here, derive it with the surface rules in [construction.md](construction.md#3-neutrals) and re-check every text level on it.
13. **Shadows use the darkest neutral with transparency:** Shell at 60 % in dark flavors, Body at 20 % in light ones.
14. **Tokens are solid.** If a platform requires transparency, choose the alpha so that the result over Canvas equals the solid token.
15. **No gradients.** Depth comes from tone.

## 12. Applying the system

Any interface, document or graphic is mapped onto the roles above by what each of its parts does. A slide, a web page, an editor and a terminal user interface follow the same tables.

### 12.1 Regions by function

| Function | Surface | Text | Structure |
|---|---|---|---|
| Outer frame: title, navigation and status bars | Shell | Subtle; Ink for the current item | Edge where the frame meets content |
| Docked panel: sidebar, tree, list, tab strip, panel header | Rail | Body; Faint for metadata | Edge on the side facing Canvas |
| Content: document, page, slide, code, terminal, table | Canvas | Body; Ink for titles and headings | Edge dividers |
| Card, group or code block inside content | Canvas | As content | 1 px Edge outline |
| Floating layer without code: menu, dropdown, dialog, notification, tooltip | Raised | Body; Faint for shortcuts and hints | 1 px Edge outline and the shadow of [rule 13](#11-rules) |
| Floating layer with code: hover, preview, completion list | Canvas | As content | 1 px Edge outline and shadow |
| Text field, select | Raised | Body; Subtle for the placeholder | Control boundary |
| Modal backdrop | The shadow color of rule 13, over everything behind the dialog | None | None |

Tables in content have no fill: headers in Ink, cells in Body, Edge between rows. Alternating row fills are not used, since Rail sits only <!-- fact:rail_canvas -->1.06 to 1.25<!-- /fact --> JND from Canvas and any stronger fill would be a surface without a role.

### 12.2 Nesting and elevation

There are two elevations. Shell, Rail and Canvas are in the flow; Raised floats.

- A card or group inside content keeps its parent's surface and takes an Edge outline. Raised is the hover fill, so a card filled with it reads as hovered.
- A floating layer over another one (a submenu, a dropdown inside a dialog) is Raised again. Its Edge outline and shadow separate it; there is no third surface.
- Fields and buttons inside a Raised layer keep Raised and are carried by their Control boundary.
- Sections inside a floating layer are divided with Edge, not with a different fill.

A target that needs another level derives it with [rule 12](#11-rules); a token is never lightened or darkened by hand to make one.

### 12.3 Neutral controls and rows

Controls and rows that are not the single main action carry no accent fill. Their states move through surfaces and background states that already exist.

Rows and items: lists, trees, menus, table rows, tabs in a strip.

| State | On Rail or Canvas | On Shell or Raised |
|---|---|---|
| Rest | The parent surface | The parent surface |
| Hover | Raised | `selection-inactive` |
| Selected, container not focused | `selection-inactive` | `selection` |
| Selected or keyboard-active, container focused | `selection` | `selection` |
| Disabled | The parent surface, text in Control | The parent surface, text in Control |

Shell and Raised share a column because in light flavors they are less than 1 JND apart, so Raised cannot mark hover on Shell. On every parent, the fills its column allows are at least 1 JND from each other and from the parent ([§14](#14-guarantees)), and Faint keeps 4.5:1 on all of them.

Buttons and other bounded controls:

| State | Fill | Label | Boundary |
|---|---|---|---|
| Rest | The parent surface | Body | Control |
| Hover | Raised on Rail or Canvas; Edge on Shell or Raised | Body | Control |
| Pressed | Edge | Body or Ink | Control |
| Focused | As in its current state | As in its current state | Adds the `accent-focus` ring |
| Checked or on | Unchanged; the check mark or knob is drawn in Body | Body | Control |
| Invalid | Unchanged | Body, with a message ([rule 6](#11-rules)) | Coral |
| Disabled | The parent surface, no hover or pressed state | Control | Edge |

On Shell or Raised, hover and pressed share Edge. Only Body, Ink and Subtle (for icons) sit on an Edge fill: Subtle keeps <!-- fact:min.subtle_edge -->5.26<!-- /fact -->:1 there, while Faint and Control fall below their levels.

### 12.4 Data visualization

Data series take the code colors in a fixed order, the same in every flavor, so a series keeps its color when a chart moves between a dark and a light theme. The order keeps the largest separation at every number of series ([construction.md §7.1](construction.md#71-series-order)). The figures are the smallest ΔE OKLab among the series up to that row, worst case across normal vision and the three dichromacies; for Other, between Control and every series.

| Series | Color | Dusk | Dawn | Smallest ΔE, Dusk | Smallest ΔE, Dawn |
|---|---|---|---|---|---|
| 1 | Sky | <img src="https://placehold.co/16x16/78aee6/78aee6" width="16" height="16" alt="#78aee6"> `#78aee6` | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> `#3f4880` | — | — |
| 2 | Ember | <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> `#67320a` | 0.183 | 0.128 |
| 3 | Gold | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> `#766014` | 0.100 | 0.116 |
| 4 | Sea Salt | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> `#65d5d2` | <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> `#176a7e` | 0.064 | 0.075 |
| 5 | Orchid | <img src="https://placehold.co/16x16/db8dc7/db8dc7" width="16" height="16" alt="#db8dc7"> `#db8dc7` | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> `#813b67` | 0.061 | 0.041 |
| 6 | Grove | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> `#99d086` | <img src="https://placehold.co/16x16/39713a/39713a" width="16" height="16" alt="#39713a"> `#39713a` | 0.061 | 0.040 |
| Other | Control | <img src="https://placehold.co/16x16/5a717f/5a717f" width="16" height="16" alt="#5a717f"> `#5a717f` | <img src="https://placehold.co/16x16/697e8c/697e8c" width="16" height="16" alt="#697e8c"> `#697e8c` | 0.158 | 0.078 |

- Up to six series take colors in this order. From the seventh on, series are grouped as Other in Control; colors are never repeated or invented.
- Coral and the accent never color a series. Coral means danger, and the accent marks interaction.
- When the data encodes a state (pass or fail, added or removed), the semantic colors of [§8](#8-semantic-states) replace the series order, with labels.
- Every series is also identified by a label, a legend entry next to it, or a marker shape ([rule 6](#11-rules)).
- The plot area is Canvas, gridlines and axes Edge, tick labels Faint, values and titles Body or Ink. Labels inside filled marks use the chip label of §8, which reaches <!-- fact:series_label -->5.04<!-- /fact -->:1 on every series color.
- To bring one series forward, draw the others in Control.
- Magnitude is shown with the two scales below, never by interpolating between palette colors.

**Sequential** (one quantity, low to high): five steps of Ember from Canvas. **Diverging** (deviation from a middle value): two steps of Sky below, Canvas at the middle, two steps of Gold above. Every step is at least as far from its neighbors as the code colors must be from each other (4 JND in normal vision, 2 JND under color-vision deficiency), and so are the two diverging steps at the same distance from the middle. Every colored cell takes a label at 4.5:1 or more, in Ink or in the chip label of §8, whichever contrasts more. The method is in [construction.md §7.2](construction.md#72-continuous-scales).

| Scale | Step | Dusk | Dawn |
|---|---|---|---|
| Sequential | 1 | <img src="https://placehold.co/16x16/3a3530/3a3530" width="16" height="16" alt="#3a3530"> `#3a3530` | <img src="https://placehold.co/16x16/d4c7bf/d4c7bf" width="16" height="16" alt="#d4c7bf"> `#d4c7bf` |
| Sequential | 2 | <img src="https://placehold.co/16x16/66594f/66594f" width="16" height="16" alt="#66594f"> `#66594f` | <img src="https://placehold.co/16x16/b9a092/b9a092" width="16" height="16" alt="#b9a092"> `#b9a092` |
| Sequential | 3 | <img src="https://placehold.co/16x16/958070/958070" width="16" height="16" alt="#958070"> `#958070` | <img src="https://placehold.co/16x16/9e7b66/9e7b66" width="16" height="16" alt="#9e7b66"> `#9e7b66` |
| Sequential | 4 | <img src="https://placehold.co/16x16/c7aa93/c7aa93" width="16" height="16" alt="#c7aa93"> `#c7aa93` | <img src="https://placehold.co/16x16/83563b/83563b" width="16" height="16" alt="#83563b"> `#83563b` |
| Sequential | 5 | <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> `#67320a` |
| Diverging | −2 | <img src="https://placehold.co/16x16/74a7dd/74a7dd" width="16" height="16" alt="#74a7dd"> `#74a7dd` | <img src="https://placehold.co/16x16/475186/475186" width="16" height="16" alt="#475186"> `#475186` |
| Diverging | −1 | <img src="https://placehold.co/16x16/41576d/41576d" width="16" height="16" alt="#41576d"> `#41576d` | <img src="https://placehold.co/16x16/959cba/959cba" width="16" height="16" alt="#959cba"> `#959cba` |
| Diverging | 0 | <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> `#11171b` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Diverging | +1 | <img src="https://placehold.co/16x16/6d6035/6d6035" width="16" height="16" alt="#6d6035"> `#6d6035` | <img src="https://placehold.co/16x16/b1a686/b1a686" width="16" height="16" alt="#b1a686"> `#b1a686` |
| Diverging | +2 | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> `#766014` |

- Values are binned into these steps. A scale with more bins repeats no step and borrows no other color; it uses fewer bins.
- A scale is not a state: when the data encodes pass or fail, the semantic colors of [§8](#8-semantic-states) apply.

### 12.5 Limited targets

A target that cannot express the whole system uses a subset of it. It never borrows a color from another role.

| Limitation | Use |
|---|---|
| Fewer surfaces | Canvas stays the content surface. Rail folds into Shell. A floating layer without a surface of its own uses Canvas with an Edge outline. |
| Fewer text levels | A missing level takes the next stronger one: Faint becomes Subtle, Subtle becomes Body. Never a weaker one. |
| One accent color for text and fills | `accent-text`, with the chip label of §8 on it. Every accent keeps <!-- fact:min.accent_label -->5.46<!-- /fact -->:1 or more, and `accent-text` already meets the code floor of its category on every surface. |
| Transparency only | [Rule 14](#11-rules): the alpha over Canvas reproduces the solid token. |
| No borders | The effect is left out (§12.6). |
| Sixteen terminal colors | The table below. |

| Role | Dark flavors | Light flavors |
|---|---|---|
| Background, text | Default background (Canvas) and foreground (Body) | The same |
| Titles, focus | Bold or bright white (Ink) | Bold |
| Secondary text | White (Subtle) | Default foreground |
| Metadata | Bright black (Faint) | Bright black (Faint) |
| Highlighted row or panel | Black (Edge) as background, with the default foreground or bold | White (Edge) as background, with the default foreground or bold |
| States and markers | The ANSI slots of §6 | The same |
| Active item | Bold or reverse video; there is no accent slot | The same |

In light flavors, bright white is Raised, a surface: it never colors text.

### 12.6 Building a theme

1. Classify every region of the target with §12.1 and assign its surface.
2. Assign a text level to every foreground by function. Use Subtle for icons.
3. Give rows and controls the states of §12.3, a Control boundary and an `accent-focus` ring when focused.
4. Place the accent only where [§5](#5-accents) allows.
5. Map semantic states and version-control markers.
6. Map background states, using the solid tokens.
7. Map code and terminal colors, and data series with §12.4.
8. Ship one theme per flavor, named *Twilight {Flavor}*, with Afterglow as the accent.
9. Check before shipping:
   - every foreground meets its level on the surface it sits on;
   - code colors meet the category floor (7:1 dark, 4.5:1 light) on Canvas and on diff backgrounds;
   - control boundaries and focus indicators reach 3:1;
   - no `#000000`, no `#ffffff`, nothing outside sRGB;
   - the accent fills nothing larger than a button or badge;
   - nothing in §13 appears.

If a target cannot express a rule, such as a border on the current line, the effect is left out rather than drawn with a color from another role.

## 13. How not to apply

Each misuse below breaks a role or a guarantee. Ports are checked against this table.

| Misuse | What breaks | Instead |
|---|---|---|
| A shade made by lightening, darkening, blending or fading a token (a hover "10 % lighter", a tinted panel) | The value has no derivation, and text levels are not solved on it | The states of §12.3; a new surface by [rule 12](#11-rules) |
| A code, semantic or series color used as decoration: file-type tags, folder icons, headings, separators, status bar fills | Color stops carrying meaning ([principle 2](#1-principles)) | Neutrals |
| Coral for anything but danger: a brand mark, a highlight, a harmless removal, a series | An error no longer stands out | Gold, Grove or a neutral, by meaning |
| A semantic color itself for text, such as a success or error message | Below 4.5:1 on Raised in light flavors | The color's `accent-text` (§8) |
| `accent` in place of `accent-text` for text, or in place of `accent-focus` for rings | The contrast guarantee belongs to the variant | The variant named in §5 |
| The accent on content, large fills, semantic states or data series | The accent stops marking interaction | [§5](#where-the-accent-goes) |
| An accent family other than Afterglow in a theme | Its color already codes syntax or a semantic state, so focus and active indicators would share a hue with content or meaning | Afterglow |
| Tokens from two flavors, or two accent families, in one theme | Contrast and separation are solved within one flavor | One flavor and one accent family per theme |
| Code on Raised | Code colors are solved on code surfaces only | Canvas with an Edge outline ([rule 1](#11-rules)) |
| A card or group filled with Raised | It reads as hovered | Its parent surface with an Edge outline (§12.2) |
| Faint or Control text on Edge, or text on any fill not listed in §12.3 | The level falls below its minimum | Body, Ink, or Subtle for icons |
| Faint for placeholders | A placeholder on Raised must stay readable | Subtle ([§4](#4-text-and-control-levels)) |
| A fill on the current line | Comments fall below 4.5:1 | Edge borders ([rule 11](#11-rules)) |
| Bright white for text in a light flavor | It is Raised, about 1.2:1 on Canvas | The default foreground or bold |
| `#000000` or `#ffffff`, also in shadows and backdrops | [Principle 5](#1-principles) | The shadow colors of rule 13 |
| A seventh series color, or colors interpolated into a scale | The separation of §12.4 is lost | Other in Control; the sequential or diverging steps of §12.4 |
| State, links or series told apart by color alone | Readers with a color-vision deficiency lose them | Icon, label, underline, marker or position ([rule 6](#11-rules)) |
| Gradients, glows, washes | [Rule 15](#11-rules) | Tone and Edge |
| A color borrowed from another role to stand in for one the target lacks | Two meanings share a color | Leave the effect out (§12.5) |
| A hex value edited by hand | It no longer rebuilds from [construction.md](construction.md) | A change to the method, validated |

## 14. Guarantees

| Guarantee | Dusk | Dawn |
|---|---|---|
| Ink on any surface | 13.25:1 | 12.84:1 |
| Body on any surface | 10.90:1 | 10.90:1 |
| Subtle on any surface | 7.01:1 | 7.04:1 |
| Faint on any surface | 4.51:1 | 4.52:1 |
| Control boundary on any surface | 3.00:1 | 3.01:1 |
| Semantic colors on any surface and on Edge | 4.50:1 | 3.19:1 |
| Subtle on an Edge fill | 5.26:1 | 5.42:1 |
| Accent focus on any surface, every accent | 5.99:1 | 3.02:1 |
| Chip label on `accent-text`, every accent | 8.94:1 | 5.46:1 |
| Code colors on every code surface | 7.00:1 | 4.52:1 |
| Smallest code-color difference, normal vision | ΔE 0.097 | ΔE 0.088 |
| Smallest code-color difference, color-vision deficiency | ΔE 0.061 | ΔE 0.040 |
| Faint from every semantic color, every vision | 3.30 JND | 1.05 JND |
| Twelve chromatic terminal colors, closest pair, every vision | ΔE 0.020 | ΔE 0.020 |
| Ember from Afterglow, normal vision | ΔE 0.216 | ΔE 0.360 |
| Scale steps, closest pair, normal vision | ΔE 0.115 | ΔE 0.095 |
| Scale steps, closest pair, color-vision deficiency | ΔE 0.079 | ΔE 0.052 |
| Scale cell labels, lowest | 5.23:1 | 4.71:1 |
| Other series from every series, every vision | ΔE 0.158 | ΔE 0.078 |
| Neutral row and control states, closest pair | 2.9 JND | 1.5 JND |
| Pure black or white | none | none |
| Gamut | sRGB | sRGB |

These are the values each flavor reaches today; no change may lower one without the conditions of [construction.md §10.1](construction.md#101-quality-floors), and no flavor, present or future, may fall below the minimums listed there. Contrast is WCAG 2.x relative-luminance contrast on final sRGB values. Color-vision figures are the worst case across simulated deuteranopia, protanopia and tritanopia, over the six code colors (Orchid, Sky, Sea Salt, Grove, Gold, Ember) and the cursor. The six code colors are also the six data series, so the code-color figures hold for any number of series.
