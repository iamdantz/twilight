# Twilight design system

Version 1.4 · Flavors: Dusk (dark), Dawn (light)

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
12. [Building a theme from this definition](#12-building-a-theme-from-this-definition)
13. [Guarantees](#13-guarantees)

## 1. Principles

1. **One seed, everything else derived.** The seed `#ee7a1f` is the only color chosen by hand. Afterglow is the most chromatic orange sRGB holds at its hue, and the neutrals sit at its exact complement (232°).
2. **Every color has a role.** If something is colored, the color carries meaning.
3. **Contrast is solved against the hardest case.** Each text level, control boundary and code color is solved against the most demanding surface it can appear on, so it holds on all of them.
4. **The accent is a detail.** It marks focus, activity and the main action. It never fills large areas and never colors content.
5. **No pure black or white.** The darkest value is L 0.16 and the lightest is L 0.95 (Dawn `diff-inserted` renders at 0.950 after 8-bit rounding).
6. **One system, two ends.** Dusk and Dawn share every role and rule and the same neutral curve. Dawn uses the light end of the curve: its Canvas is Dusk's Ink and its Ink is Dusk's Canvas.

## 2. Palette

The palette has ten neutrals and eight colors per flavor. Token names are lowercase and hyphenated (`sea-salt`, `accent-focus`). Names refer to roles, so `canvas` is dark in Dusk and light in Dawn.

### Dusk

| | Token | Hex | OKLCH | vs Shell | vs Rail | vs Canvas | vs Raised |
|:-:|---|---|---|---|---|---|---|
| <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> | `shell` | `#0a0e11` | `oklch(16.1% 0.009 240.6)` | 1.00 | 1.04 | 1.07 | 1.21 |
| <img src="https://placehold.co/16x16/0e1316/0e1316" width="16" height="16" alt="#0e1316"> | `rail` | `#0e1316` | `oklch(18.3% 0.010 234.4)` | 1.04 | 1.00 | 1.03 | 1.17 |
| <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> | `canvas` | `#11171b` | `oklch(20.0% 0.012 237.4)` | 1.07 | 1.03 | 1.00 | 1.13 |
| <img src="https://placehold.co/16x16/1a2329/1a2329" width="16" height="16" alt="#1a2329"> | `raised` | `#1a2329` | `oklch(25.0% 0.017 237.6)` | 1.21 | 1.17 | 1.13 | 1.00 |
| <img src="https://placehold.co/16x16/26333c/26333c" width="16" height="16" alt="#26333c"> | `edge` | `#26333c` | `oklch(31.3% 0.024 238.7)` | 1.50 | 1.44 | 1.39 | 1.23 |
| <img src="https://placehold.co/16x16/586f7d/586f7d" width="16" height="16" alt="#586f7d"> | `control` | `#586f7d` | `oklch(52.8% 0.035 235.0)` | 3.68 | 3.55 | 3.43 | 3.03 |
| <img src="https://placehold.co/16x16/778b97/778b97" width="16" height="16" alt="#778b97"> | `faint` | `#778b97` | `oklch(62.5% 0.029 234.3)` | 5.47 | 5.27 | 5.10 | 4.50 |
| <img src="https://placehold.co/16x16/a0aeb5/a0aeb5" width="16" height="16" alt="#a0aeb5"> | `subtle` | `#a0aeb5` | `oklch(74.2% 0.019 229.1)` | 8.50 | 8.20 | 7.93 | 7.00 |
| <img src="https://placehold.co/16x16/d2d6d8/d2d6d8" width="16" height="16" alt="#d2d6d8"> | `body` | `#d2d6d8` | `oklch(87.4% 0.005 228.8)` | 13.24 | 12.77 | 12.35 | 10.90 |
| <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> | `ink` | `#eeeeef` | `oklch(94.9% 0.001 0)` | 16.71 | 16.12 | 15.58 | 13.76 |

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
| <img src="https://placehold.co/16x16/dfe1e3/dfe1e3" width="16" height="16" alt="#dfe1e3"> | `shell` | `#dfe1e3` | `oklch(90.9% 0.003 247.9)` | 1.00 | 1.07 | 1.13 | 1.03 |
| <img src="https://placehold.co/16x16/e6e8e8/e6e8e8" width="16" height="16" alt="#e6e8e8"> | `rail` | `#e6e8e8` | `oklch(92.9% 0.002 197.1)` | 1.07 | 1.00 | 1.06 | 1.10 |
| <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> | `canvas` | `#eeeeef` | `oklch(94.9% 0.001 0)` | 1.13 | 1.06 | 1.00 | 1.17 |
| <img src="https://placehold.co/16x16/dbdedf/dbdedf" width="16" height="16" alt="#dbdedf"> | `raised` | `#dbdedf` | `oklch(89.9% 0.004 219.5)` | 1.03 | 1.10 | 1.17 | 1.00 |
| <img src="https://placehold.co/16x16/c4cace/c4cace" width="16" height="16" alt="#c4cace"> | `edge` | `#c4cace` | `oklch(83.6% 0.009 236.6)` | 1.26 | 1.35 | 1.43 | 1.22 |
| <img src="https://placehold.co/16x16/6c818f/6c818f" width="16" height="16" alt="#6c818f"> | `control` | `#6c818f` | `oklch(59.1% 0.033 237.3)` | 3.10 | 3.30 | 3.50 | 3.00 |
| <img src="https://placehold.co/16x16/4f6574/4f6574" width="16" height="16" alt="#4f6574"> | `faint` | `#4f6574` | `oklch(49.5% 0.036 238.2)` | 4.65 | 4.95 | 5.26 | 4.51 |
| <img src="https://placehold.co/16x16/364855/364855" width="16" height="16" alt="#364855"> | `subtle` | `#364855` | `oklch(39.2% 0.032 240.0)` | 7.23 | 7.71 | 8.18 | 7.01 |
| <img src="https://placehold.co/16x16/1f2931/1f2931" width="16" height="16" alt="#1f2931"> | `body` | `#1f2931` | `oklch(27.5% 0.020 242.6)` | 11.28 | 12.02 | 12.76 | 10.94 |
| <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> | `ink` | `#11171b` | `oklch(20.0% 0.012 237.4)` | 13.78 | 14.69 | 15.58 | 13.36 |

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
| **Raised** | Floating layers without code | Menus, command palettes, dropdowns, notifications, text fields, selected or hovered rows, inline hints |
| **Edge** | One-pixel structure | Dividers, outlines of floating layers, current-line border, indent guides, scrollbar thumb at rest |

In Dusk the surfaces get lighter as they come forward: Shell (L 0.16), Rail (0.18), Canvas (0.20), Raised (0.25), Edge (0.31). In Dawn, Canvas is the lightest (L 0.95) and the others step down from it at the same perceptual distance from Canvas as in Dusk: Rail (0.93), Shell (0.91), Raised (0.90), Edge (0.84).

Separation between surfaces is deliberately low (Dusk 1.04 to 1.13:1, Dawn 1.06 to 1.17:1). Tone tells surfaces apart; Edge lines and Control boundaries carry the structure that has to be seen.

## 4. Text and control levels

Each level is solved against Raised, the hardest surface for text in both flavors.

| Level | Minimum on any surface | Use |
|---|---|---|
| **Ink** | 13.4:1 | Titles, headings, focused and selected items |
| **Body** | 10.9:1 | Default text; variables and properties in code |
| **Subtle** | 7.0:1 | Secondary labels, icons, placeholders; punctuation and operators in code |
| **Faint** | 4.5:1 | Metadata, line numbers, inactive tabs, comments, hints, ignored items |
| **Control** | 3.0:1 | Boundaries of text fields, checkboxes, selects and toggles; disabled glyphs; active indent guide; scrollbar thumb on hover |

The text steps are geometric: 4.5, 7.0, 10.9.

Placeholders use Subtle, never Faint. A placeholder can sit on Raised, and reading it is part of recognizing the field.

## 5. Accents

Any of the eight colors can be the accent. A theme is named by flavor and accent, for example *Twilight Dusk Grove*. When no accent is named, it is Afterglow.

Each accent provides five tokens:

| Token | Use | Rule |
|---|---|---|
| `accent` | Fills: badges, the main button, progress | The color itself |
| `on-accent` | Text and icons on `accent` and `accent-pressed` | The extreme neutral with the higher contrast on `accent` |
| `accent-text` | Links, matched characters in lists | The color itself if it reaches 7:1 (Dusk) or 4.5:1 (Dawn) on Raised; otherwise moved in lightness until it does |
| `accent-pressed` | Pressed and hover state of filled controls | `accent` darkened by up to 0.10 L, stopping early if `on-accent` would drop below 4.5:1 |
| `accent-focus` | Focus rings, cursor, active indicators | The color itself if it reaches 3:1 on every surface; otherwise moved in lightness until it does |

Every variant keeps the hue and relative chroma of its color. Only lightness changes.

### Dusk

| Accent | `accent` | `accent-text` | `accent-pressed` | `accent-focus` | `on-accent` |
|---|---|---|---|---|---|
| Afterglow | <img src="https://placehold.co/16x16/ff7d00/ff7d00" width="16" height="16" alt="#ff7d00"> `#ff7d00` | <img src="https://placehold.co/16x16/ff8f42/ff8f42" width="16" height="16" alt="#ff8f42"> `#ff8f42` | <img src="https://placehold.co/16x16/d26600/d26600" width="16" height="16" alt="#d26600"> `#d26600` | <img src="https://placehold.co/16x16/ff7d00/ff7d00" width="16" height="16" alt="#ff7d00"> `#ff7d00` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Coral | <img src="https://placehold.co/16x16/ee8476/ee8476" width="16" height="16" alt="#ee8476"> `#ee8476` | <img src="https://placehold.co/16x16/f09386/f09386" width="16" height="16" alt="#f09386"> `#f09386` | <img src="https://placehold.co/16x16/e8473a/e8473a" width="16" height="16" alt="#e8473a"> `#e8473a` | <img src="https://placehold.co/16x16/ee8476/ee8476" width="16" height="16" alt="#ee8476"> `#ee8476` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Gold | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/16x16/b79b41/b79b41" width="16" height="16" alt="#b79b41"> `#b79b41` | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> `#dbba50` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Grove | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> `#99d086` | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> `#99d086` | <img src="https://placehold.co/16x16/7fae6f/7fae6f" width="16" height="16" alt="#7fae6f"> `#7fae6f` | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> `#99d086` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Sea Salt | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> `#65d5d2` | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> `#65d5d2` | <img src="https://placehold.co/16x16/53b2b0/53b2b0" width="16" height="16" alt="#53b2b0"> `#53b2b0` | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> `#65d5d2` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Sky | <img src="https://placehold.co/16x16/78aee6/78aee6" width="16" height="16" alt="#78aee6"> `#78aee6` | <img src="https://placehold.co/16x16/7cb0e7/7cb0e7" width="16" height="16" alt="#7cb0e7"> `#7cb0e7` | <img src="https://placehold.co/16x16/498fd4/498fd4" width="16" height="16" alt="#498fd4"> `#498fd4` | <img src="https://placehold.co/16x16/78aee6/78aee6" width="16" height="16" alt="#78aee6"> `#78aee6` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Orchid | <img src="https://placehold.co/16x16/db8dc7/db8dc7" width="16" height="16" alt="#db8dc7"> `#db8dc7` | <img src="https://placehold.co/16x16/dd95ca/dd95ca" width="16" height="16" alt="#dd95ca"> `#dd95ca` | <img src="https://placehold.co/16x16/c365ad/c365ad" width="16" height="16" alt="#c365ad"> `#c365ad` | <img src="https://placehold.co/16x16/db8dc7/db8dc7" width="16" height="16" alt="#db8dc7"> `#db8dc7` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Ember | <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/16x16/f9aa63/f9aa63" width="16" height="16" alt="#f9aa63"> `#f9aa63` | <img src="https://placehold.co/16x16/fcd6b7/fcd6b7" width="16" height="16" alt="#fcd6b7"> `#fcd6b7` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |

| Accent | Label on fill | Label on pressed | Text on Raised | Focus, worst surface |
|---|---|---|---|---|
| Afterglow | 7.55 | 5.21 | 7.03 | 6.22 |
| Coral | 7.56 | 4.98 | 7.01 | 6.23 |
| Gold | 10.29 | 7.18 | 8.47 | 8.47 |
| Grove | 10.81 | 7.55 | 8.90 | 8.90 |
| Sea Salt | 11.07 | 7.72 | 9.12 | 9.12 |
| Sky | 8.30 | 5.69 | 7.00 | 6.83 |
| Orchid | 7.98 | 5.34 | 7.01 | 6.57 |
| Ember | 14.25 | 10.11 | 11.73 | 11.73 |

### Dawn

| Accent | `accent` | `accent-text` | `accent-pressed` | `accent-focus` | `on-accent` |
|---|---|---|---|---|---|
| Afterglow | <img src="https://placehold.co/16x16/ff7d00/ff7d00" width="16" height="16" alt="#ff7d00"> `#ff7d00` | <img src="https://placehold.co/16x16/9d4b00/9d4b00" width="16" height="16" alt="#9d4b00"> `#9d4b00` | <img src="https://placehold.co/16x16/d26600/d26600" width="16" height="16" alt="#d26600"> `#d26600` | <img src="https://placehold.co/16x16/c86100/c86100" width="16" height="16" alt="#c86100"> `#c86100` | <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> `#11171b` |
| Coral | <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> `#8d3826` | <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> `#8d3826` | <img src="https://placehold.co/16x16/642518/642518" width="16" height="16" alt="#642518"> `#642518` | <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> `#8d3826` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Gold | <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> `#766014` | <img src="https://placehold.co/16x16/756014/756014" width="16" height="16" alt="#756014"> `#756014` | <img src="https://placehold.co/16x16/56450c/56450c" width="16" height="16" alt="#56450c"> `#56450c` | <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> `#766014` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Grove | <img src="https://placehold.co/16x16/39713a/39713a" width="16" height="16" alt="#39713a"> `#39713a` | <img src="https://placehold.co/16x16/376e38/376e38" width="16" height="16" alt="#376e38"> `#376e38` | <img src="https://placehold.co/16x16/285228/285228" width="16" height="16" alt="#285228"> `#285228` | <img src="https://placehold.co/16x16/39713a/39713a" width="16" height="16" alt="#39713a"> `#39713a` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Sea Salt | <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> `#176a7e` | <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> `#176a7e` | <img src="https://placehold.co/16x16/0e4c5b/0e4c5b" width="16" height="16" alt="#0e4c5b"> `#0e4c5b` | <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> `#176a7e` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Sky | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> `#3f4880` | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> `#3f4880` | <img src="https://placehold.co/16x16/292f57/292f57" width="16" height="16" alt="#292f57"> `#292f57` | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> `#3f4880` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Orchid | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> `#813b67` | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> `#813b67` | <img src="https://placehold.co/16x16/5b2848/5b2848" width="16" height="16" alt="#5b2848"> `#5b2848` | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> `#813b67` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |
| Ember | <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> `#67320a` | <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> `#67320a` | <img src="https://placehold.co/16x16/421e04/421e04" width="16" height="16" alt="#421e04"> `#421e04` | <img src="https://placehold.co/16x16/67320a/67320a" width="16" height="16" alt="#67320a"> `#67320a` | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> `#eeeeef` |

| Accent | Label on fill | Label on pressed | Text on Raised | Focus, worst surface |
|---|---|---|---|---|
| Afterglow | 7.04 | 4.85 | 4.51 | 3.01 |
| Coral | 6.64 | 9.95 | 5.69 | 5.69 |
| Gold | 5.24 | 8.04 | 4.51 | 4.50 |
| Grove | 5.04 | 7.78 | 4.50 | 4.32 |
| Sea Salt | 5.33 | 8.22 | 4.57 | 4.57 |
| Sky | 7.39 | 11.05 | 6.34 | 6.34 |
| Orchid | 6.57 | 9.83 | 5.64 | 5.64 |
| Ember | 8.89 | 12.76 | 7.62 | 7.62 |

### Where the accent goes

- Focus rings and outlines: `accent-focus`
- Text cursor: `accent-focus`
- Active indicators, such as a 2 px line on the active tab, the active item in a navigation strip, the active panel title: `accent-focus`
- Badges and counters: `accent` with `on-accent`
- The single main action of a view: `accent`, `accent-pressed`, `on-accent`
- Progress indicators: `accent`
- Links and matched characters: `accent-text`. Links in running text are also underlined, or marked by an icon where an underline cannot be drawn. No `accent-text` reaches 3:1 against Body (Dusk 1.08–1.56, Dawn 1.44–2.43), so color alone cannot separate a link from the text around it (WCAG 2.2 SC 1.4.1, technique G183). With Afterglow, `accent-text` is also ΔE_OK 0.074 (Dusk) and 0.067 (Dawn) from Coral, below the smallest code-color difference ([§13](#13-guarantees)). Links whose role is clear from position, such as navigation items and buttons, need no extra cue.
- A small emblem: `accent-focus`

### Where it never goes

- Large fills: frames, toolbars, sidebars, backgrounds, headers
- Content: code, terminal output, body text
- Semantic meaning: the accent never signals error, warning or success
- Gradients or washes

A view should contain one accent element besides focus and cursor indicators.

### What the accent does not change

Code colors, semantic states, background states (including selection) and terminal colors belong to the flavor and are identical in every accent. Background-state hues were allocated so that no two collide, and letting the accent tint them would break that.

When the accent is Coral, Gold or Grove, accent indicators share a hue with a semantic state. Semantic states never rely on color alone (see [rule 6](#11-rules)), so meaning is preserved.

## 6. Colors

Six of the eight colors fill the ANSI chromatic slots and are anchored to the corners of the RGB cube, so their meaning matches what terminals and tools expect. Ember is a seventh code color in Afterglow's hue family. Afterglow is the default accent and the seed of the system.

| Color | ANSI slot | Semantic meaning | Code role |
|---|---|---|---|
| **Afterglow** | none | Default accent; tints selection | None |
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

Version-control markers (gutter bars, file decorations) follow the same mapping: added Grove, modified Gold, removed Coral, renamed Sea Salt, ignored Faint, conflict Orchid.

Semantic colors are used as foregrounds: icons, text, 3 px bars. On a filled chip, the label is Shell in Dusk and Canvas in Dawn. Both reach at least 5.04:1 on every semantic color.

## 9. Background states

Visibility is measured in JND, just-noticeable differences, where 1 JND is ΔE 0.02 in OKLab, measured against Canvas.

- **Transient** states (selection, search matches, word highlights) may change lightness, but Faint text must keep 4.5:1 on them.
- **Persistent** states (diff lines) are treated as code surfaces. Code colors are validated on them and keep their full minimum.
- **Apart from each other.** Every state is at least 1 JND from every other state, so a read and a write highlight, or the current and other search matches, never look the same. The one exception is Dawn's selection and inactive selection (0.96 JND), which mark the focused and unfocused editors.

### Dusk

| | Token | Hex | Hue from | Visibility | Kind |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/351a08/351a08" width="16" height="16" alt="#351a08"> | `selection` | `#351a08` | Afterglow | 4.1 JND | transient |
| <img src="https://placehold.co/16x16/260f02/260f02" width="16" height="16" alt="#260f02"> | `selection-inactive` | `#260f02` | Afterglow | 2.9 JND | transient |
| <img src="https://placehold.co/16x16/292108/292108" width="16" height="16" alt="#292108"> | `find-match` | `#292108` | Gold | 3.6 JND | transient |
| <img src="https://placehold.co/16x16/1d1500/1d1500" width="16" height="16" alt="#1d1500"> | `find-match-other` | `#1d1500` | Gold | 2.6 JND | transient |
| <img src="https://placehold.co/16x16/062221/062221" width="16" height="16" alt="#062221"> | `word-highlight` | `#062221` | Sea Salt | 2.0 JND | transient |
| <img src="https://placehold.co/16x16/182423/182423" width="16" height="16" alt="#182423"> | `word-highlight-write` | `#182423` | Sea Salt | 2.5 JND | transient |
| <img src="https://placehold.co/16x16/0e1a09/0e1a09" width="16" height="16" alt="#0e1a09"> | `diff-inserted` | `#0e1a09` | Grove | 2.0 JND | persistent |
| <img src="https://placehold.co/16x16/22110e/22110e" width="16" height="16" alt="#22110e"> | `diff-removed` | `#22110e` | Coral | 2.0 JND | persistent |

### Dawn

| | Token | Hex | Hue from | Visibility | Kind |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/eedace/eedace" width="16" height="16" alt="#eedace"> | `selection` | `#eedace` | Afterglow | 2.8 JND | transient |
| <img src="https://placehold.co/16x16/f5e0d4/f5e0d4" width="16" height="16" alt="#f5e0d4"> | `selection-inactive` | `#f5e0d4` | Afterglow | 2.1 JND | transient |
| <img src="https://placehold.co/16x16/eeddaa/eeddaa" width="16" height="16" alt="#eeddaa"> | `find-match` | `#eeddaa` | Gold | 4.3 JND | transient |
| <img src="https://placehold.co/16x16/faeec9/faeec9" width="16" height="16" alt="#faeec9"> | `find-match-other` | `#faeec9` | Gold | 2.6 JND | transient |
| <img src="https://placehold.co/16x16/ceeef8/ceeef8" width="16" height="16" alt="#ceeef8"> | `word-highlight` | `#ceeef8` | Sea Salt | 2.0 JND | transient |
| <img src="https://placehold.co/16x16/c5e4ee/c5e4ee" width="16" height="16" alt="#c5e4ee"> | `word-highlight-write` | `#c5e4ee` | Sea Salt | 3.0 JND | transient |
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

The six chromatic normals are the six ANSI colors above. Each bright moves one third of the way toward Ink, so brights are lighter in Dusk and deeper in Dawn.

### Dusk (background Canvas `#11171b`)

| # | Slot | | Hex | From | On Canvas |
|--:|---|:-:|---|---|---|
| 0 | black | <img src="https://placehold.co/16x16/26333c/26333c" width="16" height="16" alt="#26333c"> | `#26333c` | Edge | 1.39 |
| 1 | red | <img src="https://placehold.co/16x16/ee8476/ee8476" width="16" height="16" alt="#ee8476"> | `#ee8476` | Coral | 7.05 |
| 2 | green | <img src="https://placehold.co/16x16/99d086/99d086" width="16" height="16" alt="#99d086"> | `#99d086` | Grove | 10.08 |
| 3 | yellow | <img src="https://placehold.co/16x16/dbba50/dbba50" width="16" height="16" alt="#dbba50"> | `#dbba50` | Gold | 9.60 |
| 4 | blue | <img src="https://placehold.co/16x16/78aee6/78aee6" width="16" height="16" alt="#78aee6"> | `#78aee6` | Sky | 7.74 |
| 5 | magenta | <img src="https://placehold.co/16x16/db8dc7/db8dc7" width="16" height="16" alt="#db8dc7"> | `#db8dc7` | Orchid | 7.44 |
| 6 | cyan | <img src="https://placehold.co/16x16/65d5d2/65d5d2" width="16" height="16" alt="#65d5d2"> | `#65d5d2` | Sea Salt | 10.33 |
| 7 | white | <img src="https://placehold.co/16x16/a0aeb5/a0aeb5" width="16" height="16" alt="#a0aeb5"> | `#a0aeb5` | Subtle | 7.93 |
| 8 | bright black | <img src="https://placehold.co/16x16/778b97/778b97" width="16" height="16" alt="#778b97"> | `#778b97` | Faint | 5.10 |
| 9 | bright red | <img src="https://placehold.co/16x16/faa497/faa497" width="16" height="16" alt="#faa497"> | `#faa497` | Coral, brightened | 9.31 |
| 10 | bright green | <img src="https://placehold.co/16x16/a9e095/a9e095" width="16" height="16" alt="#a9e095"> | `#a9e095` | Grove, brightened | 11.86 |
| 11 | bright yellow | <img src="https://placehold.co/16x16/ecca61/ecca61" width="16" height="16" alt="#ecca61"> | `#ecca61` | Gold, brightened | 11.35 |
| 12 | bright blue | <img src="https://placehold.co/16x16/92c5fa/92c5fa" width="16" height="16" alt="#92c5fa"> | `#92c5fa` | Sky, brightened | 9.97 |
| 13 | bright magenta | <img src="https://placehold.co/16x16/f2a3de/f2a3de" width="16" height="16" alt="#f2a3de"> | `#f2a3de` | Orchid, brightened | 9.52 |
| 14 | bright cyan | <img src="https://placehold.co/16x16/75e5e1/75e5e1" width="16" height="16" alt="#75e5e1"> | `#75e5e1` | Sea Salt, brightened | 12.09 |
| 15 | bright white | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> | `#eeeeef` | Ink | 15.58 |

### Dawn (background Canvas `#eeeeef`)

| # | Slot | | Hex | From | On Canvas |
|--:|---|:-:|---|---|---|
| 0 | black | <img src="https://placehold.co/16x16/1f2931/1f2931" width="16" height="16" alt="#1f2931"> | `#1f2931` | Body | 12.76 |
| 1 | red | <img src="https://placehold.co/16x16/8d3826/8d3826" width="16" height="16" alt="#8d3826"> | `#8d3826` | Coral | 6.64 |
| 2 | green | <img src="https://placehold.co/16x16/39713a/39713a" width="16" height="16" alt="#39713a"> | `#39713a` | Grove | 5.04 |
| 3 | yellow | <img src="https://placehold.co/16x16/766014/766014" width="16" height="16" alt="#766014"> | `#766014` | Gold | 5.24 |
| 4 | blue | <img src="https://placehold.co/16x16/3f4880/3f4880" width="16" height="16" alt="#3f4880"> | `#3f4880` | Sky | 7.39 |
| 5 | magenta | <img src="https://placehold.co/16x16/813b67/813b67" width="16" height="16" alt="#813b67"> | `#813b67` | Orchid | 6.57 |
| 6 | cyan | <img src="https://placehold.co/16x16/176a7e/176a7e" width="16" height="16" alt="#176a7e"> | `#176a7e` | Sea Salt | 5.33 |
| 7 | white | <img src="https://placehold.co/16x16/c4cace/c4cace" width="16" height="16" alt="#c4cace"> | `#c4cace` | Edge | 1.43 |
| 8 | bright black | <img src="https://placehold.co/16x16/4f6574/4f6574" width="16" height="16" alt="#4f6574"> | `#4f6574` | Faint | 5.26 |
| 9 | bright red | <img src="https://placehold.co/16x16/721e0c/721e0c" width="16" height="16" alt="#721e0c"> | `#721e0c` | Coral, brightened | 9.50 |
| 10 | bright green | <img src="https://placehold.co/16x16/1c551f/1c551f" width="16" height="16" alt="#1c551f"> | `#1c551f` | Grove, brightened | 7.65 |
| 11 | bright yellow | <img src="https://placehold.co/16x16/56450c/56450c" width="16" height="16" alt="#56450c"> | `#56450c` | Gold, brightened | 8.04 |
| 12 | bright blue | <img src="https://placehold.co/16x16/2d346a/2d346a" width="16" height="16" alt="#2d346a"> | `#2d346a` | Sky, brightened | 10.00 |
| 13 | bright magenta | <img src="https://placehold.co/16x16/66234f/66234f" width="16" height="16" alt="#66234f"> | `#66234f` | Orchid, brightened | 9.44 |
| 14 | bright cyan | <img src="https://placehold.co/16x16/0e4d5d/0e4d5d" width="16" height="16" alt="#0e4d5d"> | `#0e4d5d` | Sea Salt, brightened | 8.09 |
| 15 | bright white | <img src="https://placehold.co/16x16/dbdedf/dbdedf" width="16" height="16" alt="#dbdedf"> | `#dbdedf` | Raised | 1.17 |

| Terminal role | Token |
|---|---|
| Background | Canvas |
| Foreground | Body |
| Bold | Ink |
| Cursor | `accent-focus` |
| Text under cursor | `on-accent` |
| Selection | `selection` |
| Links | `accent-text` |

Black and white are mostly used as backgrounds, so they map to surfaces and sit at 1.4:1 against the background. Bright black is Faint and is readable as text.

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
13. **Shadows use the darkest neutral with transparency:** Shell at 60 % in Dusk, Body at 20 % in Dawn.
14. **Tokens are solid.** If a platform requires transparency, choose the alpha so that the result over Canvas equals the solid token.
15. **No gradients.** Depth comes from tone.

## 12. Building a theme from this definition

1. List the regions of the target tool and classify each one as outer frame, docked panel, content, floating layer or divider. Assign Shell, Rail, Canvas, Raised or Edge.
2. Assign a text level to every foreground by function. Use Subtle for icons.
3. Give every interactive control a Control boundary and an `accent-focus` focus state.
4. Place the accent only where [section 5](#5-accents) allows.
5. Map semantic states and version-control markers.
6. Map background states, using the solid tokens.
7. Map code and terminal colors.
8. Ship one theme per flavor and accent, named *Twilight {Flavor} {Accent}*.
9. Check before shipping:
   - every foreground meets its level on the surface it sits on;
   - code colors meet the flavor minimum (7:1 Dusk, 4.5:1 Dawn) on Canvas and on diff backgrounds;
   - control boundaries and focus indicators reach 3:1;
   - no `#000000`, no `#ffffff`, nothing outside sRGB;
   - the accent fills nothing larger than a button or badge.

If a tool cannot express a rule, such as a border on the current line, leave the effect out rather than borrowing a color from another role.

## 13. Guarantees

| Guarantee | Dusk | Dawn |
|---|---|---|
| Ink on any surface | 13.76:1 | 13.36:1 |
| Body on any surface | 10.90:1 | 10.94:1 |
| Subtle on any surface | 7.00:1 | 7.01:1 |
| Faint on any surface | 4.50:1 | 4.51:1 |
| Control boundary on any surface | 3.03:1 | 3.00:1 |
| Accent focus on any surface, every accent | 6.22:1 | 3.01:1 |
| Code colors on every code surface | 7.00:1 | 4.52:1 |
| Smallest code-color difference, normal vision | ΔE 0.097 | ΔE 0.088 |
| Smallest code-color difference, color-vision deficiency | ΔE 0.061 | ΔE 0.040 |
| Pure black or white | none | none |
| Gamut | sRGB | sRGB |

Contrast is WCAG 2.x relative-luminance contrast on final sRGB values. Color-vision figures are the worst case across simulated deuteranopia, protanopia and tritanopia, over the six code colors (Orchid, Sky, Sea Salt, Grove, Gold, Ember) and the cursor.
