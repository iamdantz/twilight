# Twilight design system

Version 1.0 · Flavors: Dusk (dark), Dawn (light)

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

1. **Two seeds, everything else derived.** Afterglow `#ee7a1f` and the neutral hue (232°, its exact complement) are the only values chosen by hand.
2. **Every color has a role.** If something is colored, the color carries meaning.
3. **Contrast is solved against the hardest case.** Each text level, control boundary and code color is solved against the most demanding surface it can appear on, so it holds on all of them.
4. **The accent is a detail.** It marks focus, activity and the main action. It never fills large areas and never colors content.
5. **No pure black or white.** The darkest value is L 0.16 and the lightest is L 0.975.
6. **Identical structure in both flavors.** Dusk and Dawn share every role, rule and surface ratio.

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
| <img src="https://placehold.co/16x16/ee7a1f/ee7a1f" width="16" height="16" alt="#ee7a1f"> | `afterglow` | `#ee7a1f` | `oklch(70.0% 0.170 51.9)` | 6.40 | — |
| <img src="https://placehold.co/16x16/e78975/e78975" width="16" height="16" alt="#e78975"> | `coral` | `#e78975` | `oklch(72.5% 0.119 32.9)` | 7.08 | 7.04 |
| <img src="https://placehold.co/16x16/d6b95c/d6b95c" width="16" height="16" alt="#d6b95c"> | `gold` | `#d6b95c` | `oklch(79.2% 0.117 92.2)` | 9.42 | 9.37 |
| <img src="https://placehold.co/16x16/99cd8a/99cd8a" width="16" height="16" alt="#99cd8a"> | `grove` | `#99cd8a` | `oklch(79.5% 0.107 138.8)` | 9.86 | 9.80 |
| <img src="https://placehold.co/16x16/6ed0d1/6ed0d1" width="16" height="16" alt="#6ed0d1"> | `sea-salt` | `#6ed0d1` | `oklch(79.9% 0.092 196.3)` | 9.99 | 9.93 |
| <img src="https://placehold.co/16x16/7babde/7babde" width="16" height="16" alt="#7babde"> | `sky` | `#7babde` | `oklch(72.7% 0.091 250.6)` | 7.50 | 7.46 |
| <img src="https://placehold.co/16x16/d58ec3/d58ec3" width="16" height="16" alt="#d58ec3"> | `orchid` | `#d58ec3` | `oklch(73.4% 0.110 336.4)` | 7.30 | 7.26 |
| <img src="https://placehold.co/16x16/fcd1ad/fcd1ad" width="16" height="16" alt="#fcd1ad"> | `ember` | `#fcd1ad` | `oklch(88.9% 0.068 61.7)` | 12.79 | 12.72 |

### Dawn

| | Token | Hex | OKLCH | vs Shell | vs Rail | vs Canvas | vs Raised |
|:-:|---|---|---|---|---|---|---|
| <img src="https://placehold.co/16x16/ebeff2/ebeff2" width="16" height="16" alt="#ebeff2"> | `shell` | `#ebeff2` | `oklch(95.0% 0.006 239.8)` | 1.00 | 1.04 | 1.07 | 1.05 |
| <img src="https://placehold.co/16x16/eff3f5/eff3f5" width="16" height="16" alt="#eff3f5"> | `rail` | `#eff3f5` | `oklch(96.2% 0.005 228.8)` | 1.04 | 1.00 | 1.04 | 1.09 |
| <img src="https://placehold.co/16x16/f4f7f9/f4f7f9" width="16" height="16" alt="#f4f7f9"> | `canvas` | `#f4f7f9` | `oklch(97.4% 0.004 236.5)` | 1.07 | 1.04 | 1.00 | 1.13 |
| <img src="https://placehold.co/16x16/e1eaef/e1eaef" width="16" height="16" alt="#e1eaef"> | `raised` | `#e1eaef` | `oklch(93.2% 0.012 231.7)` | 1.05 | 1.09 | 1.13 | 1.00 |
| <img src="https://placehold.co/16x16/c1d6e2/c1d6e2" width="16" height="16" alt="#c1d6e2"> | `edge` | `#c1d6e2` | `oklch(86.4% 0.028 232.7)` | 1.30 | 1.35 | 1.40 | 1.23 |
| <img src="https://placehold.co/16x16/748895/748895" width="16" height="16" alt="#748895"> | `control` | `#748895` | `oklch(61.5% 0.030 236.5)` | 3.19 | 3.30 | 3.43 | 3.02 |
| <img src="https://placehold.co/16x16/566c7a/566c7a" width="16" height="16" alt="#566c7a"> | `faint` | `#566c7a` | `oklch(51.9% 0.034 236.2)` | 4.75 | 4.92 | 5.11 | 4.51 |
| <img src="https://placehold.co/16x16/3b4f5c/3b4f5c" width="16" height="16" alt="#3b4f5c"> | `subtle` | `#3b4f5c` | `oklch(41.6% 0.033 237.1)` | 7.39 | 7.65 | 7.94 | 7.00 |
| <img src="https://placehold.co/16x16/25313b/25313b" width="16" height="16" alt="#25313b"> | `body` | `#25313b` | `oklch(30.7% 0.024 243.8)` | 11.49 | 11.90 | 12.34 | 10.89 |
| <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> | `ink` | `#11171b` | `oklch(20.0% 0.012 237.4)` | 15.63 | 16.18 | 16.79 | 14.81 |

| | Token | Hex | OKLCH | On Canvas | Worst code surface |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/ee7a1f/ee7a1f" width="16" height="16" alt="#ee7a1f"> | `afterglow` | `#ee7a1f` | `oklch(70.0% 0.170 51.9)` | 2.62 | — |
| <img src="https://placehold.co/16x16/88323e/88323e" width="16" height="16" alt="#88323e"> | `coral` | `#88323e` | `oklch(44.3% 0.118 14.9)` | 7.59 | 6.75 |
| <img src="https://placehold.co/16x16/7a6716/7a6716" width="16" height="16" alt="#7a6716"> | `gold` | `#7a6716` | `oklch(51.8% 0.098 94.9)` | 5.16 | 4.60 |
| <img src="https://placehold.co/16x16/3d763e/3d763e" width="16" height="16" alt="#3d763e"> | `grove` | `#3d763e` | `oklch(51.2% 0.105 144.2)` | 5.06 | 4.50 |
| <img src="https://placehold.co/16x16/186f7f/186f7f" width="16" height="16" alt="#186f7f"> | `sea-salt` | `#186f7f` | `oklch(50.0% 0.081 213.4)` | 5.39 | 4.80 |
| <img src="https://placehold.co/16x16/2a5785/2a5785" width="16" height="16" alt="#2a5785"> | `sky` | `#2a5785` | `oklch(44.8% 0.091 251.0)` | 6.97 | 6.20 |
| <img src="https://placehold.co/16x16/7b3d6f/7b3d6f" width="16" height="16" alt="#7b3d6f"> | `orchid` | `#7b3d6f` | `oklch(45.7% 0.109 335.0)` | 7.13 | 6.34 |
| <img src="https://placehold.co/16x16/6c3d0d/6c3d0d" width="16" height="16" alt="#6c3d0d"> | `ember` | `#6c3d0d` | `oklch(40.9% 0.088 60.2)` | 8.45 | 7.52 |

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

In Dusk the surfaces get lighter as they come forward: Shell (L 0.16), Rail (0.18), Canvas (0.20), Raised (0.25), Edge (0.31). In Dawn, Canvas is the lightest and the others step down from it, at the same contrast ratios as in Dusk.

Separation between surfaces is deliberately low (1.04 to 1.13:1). Tone tells surfaces apart; Edge lines and Control boundaries carry the structure that has to be seen.

## 4. Text and control levels

Each level is solved against Raised, the hardest surface for text in both flavors.

| Level | Minimum on any surface | Use |
|---|---|---|
| **Ink** | 13.8:1 | Titles, headings, focused and selected items |
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
| Afterglow | <img src="https://placehold.co/16x16/ee7a1f/ee7a1f" width="16" height="16" alt="#ee7a1f"> `#ee7a1f` | <img src="https://placehold.co/16x16/fb914a/fb914a" width="16" height="16" alt="#fb914a"> `#fb914a` | <img src="https://placehold.co/16x16/c26217/c26217" width="16" height="16" alt="#c26217"> `#c26217` | <img src="https://placehold.co/16x16/ee7a1f/ee7a1f" width="16" height="16" alt="#ee7a1f"> `#ee7a1f` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Coral | <img src="https://placehold.co/16x16/e78975/e78975" width="16" height="16" alt="#e78975"> `#e78975` | <img src="https://placehold.co/16x16/e99785/e99785" width="16" height="16" alt="#e99785"> `#e99785` | <img src="https://placehold.co/16x16/d75c43/d75c43" width="16" height="16" alt="#d75c43"> `#d75c43` | <img src="https://placehold.co/16x16/e78975/e78975" width="16" height="16" alt="#e78975"> `#e78975` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Gold | <img src="https://placehold.co/16x16/d6b95c/d6b95c" width="16" height="16" alt="#d6b95c"> `#d6b95c` | <img src="https://placehold.co/16x16/d6b95c/d6b95c" width="16" height="16" alt="#d6b95c"> `#d6b95c` | <img src="https://placehold.co/16x16/b39a4c/b39a4c" width="16" height="16" alt="#b39a4c"> `#b39a4c` | <img src="https://placehold.co/16x16/d6b95c/d6b95c" width="16" height="16" alt="#d6b95c"> `#d6b95c` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Grove | <img src="https://placehold.co/16x16/99cd8a/99cd8a" width="16" height="16" alt="#99cd8a"> `#99cd8a` | <img src="https://placehold.co/16x16/99cd8a/99cd8a" width="16" height="16" alt="#99cd8a"> `#99cd8a` | <img src="https://placehold.co/16x16/7fab72/7fab72" width="16" height="16" alt="#7fab72"> `#7fab72` | <img src="https://placehold.co/16x16/99cd8a/99cd8a" width="16" height="16" alt="#99cd8a"> `#99cd8a` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Sea Salt | <img src="https://placehold.co/16x16/6ed0d1/6ed0d1" width="16" height="16" alt="#6ed0d1"> `#6ed0d1` | <img src="https://placehold.co/16x16/6ed0d1/6ed0d1" width="16" height="16" alt="#6ed0d1"> `#6ed0d1` | <img src="https://placehold.co/16x16/5baeaf/5baeaf" width="16" height="16" alt="#5baeaf"> `#5baeaf` | <img src="https://placehold.co/16x16/6ed0d1/6ed0d1" width="16" height="16" alt="#6ed0d1"> `#6ed0d1` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Sky | <img src="https://placehold.co/16x16/7babde/7babde" width="16" height="16" alt="#7babde"> `#7babde` | <img src="https://placehold.co/16x16/82b0e0/82b0e0" width="16" height="16" alt="#82b0e0"> `#82b0e0` | <img src="https://placehold.co/16x16/518cc9/518cc9" width="16" height="16" alt="#518cc9"> `#518cc9` | <img src="https://placehold.co/16x16/7babde/7babde" width="16" height="16" alt="#7babde"> `#7babde` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Orchid | <img src="https://placehold.co/16x16/d58ec3/d58ec3" width="16" height="16" alt="#d58ec3"> `#d58ec3` | <img src="https://placehold.co/16x16/d898c7/d898c7" width="16" height="16" alt="#d898c7"> `#d898c7` | <img src="https://placehold.co/16x16/bb6aa8/bb6aa8" width="16" height="16" alt="#bb6aa8"> `#bb6aa8` | <img src="https://placehold.co/16x16/d58ec3/d58ec3" width="16" height="16" alt="#d58ec3"> `#d58ec3` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |
| Ember | <img src="https://placehold.co/16x16/fcd1ad/fcd1ad" width="16" height="16" alt="#fcd1ad"> `#fcd1ad` | <img src="https://placehold.co/16x16/fcd1ad/fcd1ad" width="16" height="16" alt="#fcd1ad"> `#fcd1ad` | <img src="https://placehold.co/16x16/faa453/faa453" width="16" height="16" alt="#faa453"> `#faa453` | <img src="https://placehold.co/16x16/fcd1ad/fcd1ad" width="16" height="16" alt="#fcd1ad"> `#fcd1ad` | <img src="https://placehold.co/16x16/0a0e11/0a0e11" width="16" height="16" alt="#0a0e11"> `#0a0e11` |

| Accent | Label on fill | Label on pressed | Text on Raised | Focus, worst surface |
|---|---|---|---|---|
| Afterglow | 6.86 | 4.66 | 7.03 | 5.65 |
| Coral | 7.60 | 5.08 | 7.01 | 6.25 |
| Gold | 10.11 | 7.05 | 8.32 | 8.32 |
| Grove | 10.57 | 7.35 | 8.70 | 8.70 |
| Sea Salt | 10.71 | 7.49 | 8.82 | 8.82 |
| Sky | 8.05 | 5.48 | 7.02 | 6.63 |
| Orchid | 7.83 | 5.30 | 7.02 | 6.45 |
| Ember | 13.71 | 9.69 | 11.29 | 11.29 |

### Dawn

| Accent | `accent` | `accent-text` | `accent-pressed` | `accent-focus` | `on-accent` |
|---|---|---|---|---|---|
| Afterglow | <img src="https://placehold.co/16x16/ee7a1f/ee7a1f" width="16" height="16" alt="#ee7a1f"> `#ee7a1f` | <img src="https://placehold.co/16x16/a55212/a55212" width="16" height="16" alt="#a55212"> `#a55212` | <img src="https://placehold.co/16x16/c66417/c66417" width="16" height="16" alt="#c66417"> `#c66417` | <img src="https://placehold.co/16x16/cf6a1a/cf6a1a" width="16" height="16" alt="#cf6a1a"> `#cf6a1a` | <img src="https://placehold.co/16x16/11171b/11171b" width="16" height="16" alt="#11171b"> `#11171b` |
| Coral | <img src="https://placehold.co/16x16/88323e/88323e" width="16" height="16" alt="#88323e"> `#88323e` | <img src="https://placehold.co/16x16/88323e/88323e" width="16" height="16" alt="#88323e"> `#88323e` | <img src="https://placehold.co/16x16/5f2029/5f2029" width="16" height="16" alt="#5f2029"> `#5f2029` | <img src="https://placehold.co/16x16/88323e/88323e" width="16" height="16" alt="#88323e"> `#88323e` | <img src="https://placehold.co/16x16/f4f7f9/f4f7f9" width="16" height="16" alt="#f4f7f9"> `#f4f7f9` |
| Gold | <img src="https://placehold.co/16x16/7a6716/7a6716" width="16" height="16" alt="#7a6716"> `#7a6716` | <img src="https://placehold.co/16x16/7a6716/7a6716" width="16" height="16" alt="#7a6716"> `#7a6716` | <img src="https://placehold.co/16x16/5a4b0d/5a4b0d" width="16" height="16" alt="#5a4b0d"> `#5a4b0d` | <img src="https://placehold.co/16x16/7a6716/7a6716" width="16" height="16" alt="#7a6716"> `#7a6716` | <img src="https://placehold.co/16x16/f4f7f9/f4f7f9" width="16" height="16" alt="#f4f7f9"> `#f4f7f9` |
| Grove | <img src="https://placehold.co/16x16/3d763e/3d763e" width="16" height="16" alt="#3d763e"> `#3d763e` | <img src="https://placehold.co/16x16/3d753e/3d753e" width="16" height="16" alt="#3d753e"> `#3d753e` | <img src="https://placehold.co/16x16/2b572c/2b572c" width="16" height="16" alt="#2b572c"> `#2b572c` | <img src="https://placehold.co/16x16/3d763e/3d763e" width="16" height="16" alt="#3d763e"> `#3d763e` | <img src="https://placehold.co/16x16/f4f7f9/f4f7f9" width="16" height="16" alt="#f4f7f9"> `#f4f7f9` |
| Sea Salt | <img src="https://placehold.co/16x16/186f7f/186f7f" width="16" height="16" alt="#186f7f"> `#186f7f` | <img src="https://placehold.co/16x16/186f7f/186f7f" width="16" height="16" alt="#186f7f"> `#186f7f` | <img src="https://placehold.co/16x16/0f515d/0f515d" width="16" height="16" alt="#0f515d"> `#0f515d` | <img src="https://placehold.co/16x16/186f7f/186f7f" width="16" height="16" alt="#186f7f"> `#186f7f` | <img src="https://placehold.co/16x16/f4f7f9/f4f7f9" width="16" height="16" alt="#f4f7f9"> `#f4f7f9` |
| Sky | <img src="https://placehold.co/16x16/2a5785/2a5785" width="16" height="16" alt="#2a5785"> `#2a5785` | <img src="https://placehold.co/16x16/2a5785/2a5785" width="16" height="16" alt="#2a5785"> `#2a5785` | <img src="https://placehold.co/16x16/1b3c5d/1b3c5d" width="16" height="16" alt="#1b3c5d"> `#1b3c5d` | <img src="https://placehold.co/16x16/2a5785/2a5785" width="16" height="16" alt="#2a5785"> `#2a5785` | <img src="https://placehold.co/16x16/f4f7f9/f4f7f9" width="16" height="16" alt="#f4f7f9"> `#f4f7f9` |
| Orchid | <img src="https://placehold.co/16x16/7b3d6f/7b3d6f" width="16" height="16" alt="#7b3d6f"> `#7b3d6f` | <img src="https://placehold.co/16x16/7b3d6f/7b3d6f" width="16" height="16" alt="#7b3d6f"> `#7b3d6f` | <img src="https://placehold.co/16x16/57294e/57294e" width="16" height="16" alt="#57294e"> `#57294e` | <img src="https://placehold.co/16x16/7b3d6f/7b3d6f" width="16" height="16" alt="#7b3d6f"> `#7b3d6f` | <img src="https://placehold.co/16x16/f4f7f9/f4f7f9" width="16" height="16" alt="#f4f7f9"> `#f4f7f9` |
| Ember | <img src="https://placehold.co/16x16/6c3d0d/6c3d0d" width="16" height="16" alt="#6c3d0d"> `#6c3d0d` | <img src="https://placehold.co/16x16/6c3d0d/6c3d0d" width="16" height="16" alt="#6c3d0d"> `#6c3d0d` | <img src="https://placehold.co/16x16/482706/482706" width="16" height="16" alt="#482706"> `#482706` | <img src="https://placehold.co/16x16/6c3d0d/6c3d0d" width="16" height="16" alt="#6c3d0d"> `#6c3d0d` | <img src="https://placehold.co/16x16/f4f7f9/f4f7f9" width="16" height="16" alt="#f4f7f9"> `#f4f7f9` |

| Accent | Label on fill | Label on pressed | Text on Raised | Focus, worst surface |
|---|---|---|---|---|
| Afterglow | 6.40 | 4.51 | 4.51 | 3.00 |
| Coral | 7.59 | 11.31 | 6.69 | 6.69 |
| Gold | 5.16 | 7.98 | 4.56 | 4.56 |
| Grove | 5.06 | 7.80 | 4.52 | 4.46 |
| Sea Salt | 5.39 | 8.29 | 4.76 | 4.76 |
| Sky | 6.97 | 10.55 | 6.15 | 6.15 |
| Orchid | 7.13 | 10.65 | 6.29 | 6.29 |
| Ember | 8.45 | 12.44 | 7.45 | 7.45 |

### Where the accent goes

- Focus rings and outlines: `accent-focus`
- Text cursor: `accent-focus`
- Active indicators, such as a 2 px line on the active tab, the active item in a navigation strip, the active panel title: `accent-focus`
- Badges and counters: `accent` with `on-accent`
- The single main action of a view: `accent`, `accent-pressed`, `on-accent`
- Progress indicators: `accent`
- Links and matched characters: `accent-text`. Links in running text are also underlined, or marked by an icon where an underline cannot be drawn. No `accent-text` reaches 3:1 against Body (Dusk 1.04–1.55, Dawn 1.46–2.41), so color alone cannot separate a link from the text around it (WCAG 2.2 SC 1.4.1, technique G183). In Dusk with Afterglow, `accent-text` is also ΔE_OK 0.065 from Coral, below the smallest code-color difference ([§13](#13-guarantees)). Links whose role is clear from position, such as navigation items and buttons, need no extra cue.
- A small emblem: `accent-focus`

### Where it never goes

- Large fills: frames, toolbars, sidebars, backgrounds, headers
- Content: code, terminal output, body text
- Semantic meaning: the accent never signals error, warning or success
- Gradients or washes

A view should contain one accent element besides focus and cursor indicators.

### What the accent does not change

Code colors, semantic states, background states (including selection) and terminal colors belong to the flavor, not to the accent. They are identical in every accent. Background-state hues were allocated so that no two collide, and letting the accent tint them would break that.

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

The mapping was measured ([construction.md, section 8](construction.md#8-syntax-roles)). Categories are named generically so they map onto any grammar.

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

Properties are uncolored on purpose. They are among the most frequent tokens, and coloring them adds noise without adding information. Eight of the ten themes measured leave them uncolored as well.

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

Semantic colors are used as foregrounds: icons, text, 3 px bars. On a filled chip, the label is Shell in Dusk and Canvas in Dawn. Both reach at least 5.06:1 on every semantic color.

## 9. Background states

Visibility is measured in JND, just-noticeable differences, where 1 JND is ΔE 0.02 in OKLab, measured against Canvas.

- **Transient** states (selection, search matches, word highlights) may change lightness, but Faint text must keep 4.5:1 on them.
- **Persistent** states (diff lines) are treated as code surfaces. Code colors are validated on them and keep their full minimum.

### Dusk

| | Token | Hex | Hue from | Visibility | Kind |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/351a08/351a08" width="16" height="16" alt="#351a08"> | `selection` | `#351a08` | Afterglow | 4.1 JND | transient |
| <img src="https://placehold.co/16x16/211209/211209" width="16" height="16" alt="#211209"> | `selection-inactive` | `#211209` | Afterglow | 2.1 JND | transient |
| <img src="https://placehold.co/16x16/292108/292108" width="16" height="16" alt="#292108"> | `find-match` | `#292108` | Gold | 3.6 JND | transient |
| <img src="https://placehold.co/16x16/1d1500/1d1500" width="16" height="16" alt="#1d1500"> | `find-match-other` | `#1d1500` | Gold | 2.6 JND | transient |
| <img src="https://placehold.co/16x16/052222/052222" width="16" height="16" alt="#052222"> | `word-highlight` | `#052222` | Sea Salt | 2.0 JND | transient |
| <img src="https://placehold.co/16x16/112526/112526" width="16" height="16" alt="#112526"> | `word-highlight-write` | `#112526` | Sea Salt | 2.6 JND | transient |
| <img src="https://placehold.co/16x16/0d1a09/0d1a09" width="16" height="16" alt="#0d1a09"> | `diff-inserted` | `#0d1a09` | Grove | 2.1 JND | persistent |
| <img src="https://placehold.co/16x16/22110e/22110e" width="16" height="16" alt="#22110e"> | `diff-removed` | `#22110e` | Coral | 2.1 JND | persistent |

### Dawn

| | Token | Hex | Hue from | Visibility | Kind |
|:-:|---|---|---|---|---|
| <img src="https://placehold.co/16x16/f0e7e1/f0e7e1" width="16" height="16" alt="#f0e7e1"> | `selection` | `#f0e7e1` | Afterglow | 2.2 JND | transient |
| <img src="https://placehold.co/16x16/f2e8e3/f2e8e3" width="16" height="16" alt="#f2e8e3"> | `selection-inactive` | `#f2e8e3` | Afterglow | 2.1 JND | transient |
| <img src="https://placehold.co/16x16/f0e9cb/f0e9cb" width="16" height="16" alt="#f0e9cb"> | `find-match` | `#f0e9cb` | Gold | 3.1 JND | transient |
| <img src="https://placehold.co/16x16/f6eed1/f6eed1" width="16" height="16" alt="#f6eed1"> | `find-match-other` | `#f6eed1` | Gold | 2.5 JND | transient |
| <img src="https://placehold.co/16x16/dceef3/dceef3" width="16" height="16" alt="#dceef3"> | `word-highlight` | `#dceef3` | Sea Salt | 2.1 JND | transient |
| <img src="https://placehold.co/16x16/daecf0/daecf0" width="16" height="16" alt="#daecf0"> | `word-highlight-write` | `#daecf0` | Sea Salt | 2.3 JND | transient |
| <img src="https://placehold.co/16x16/e6ffe7/e6ffe7" width="16" height="16" alt="#e6ffe7"> | `diff-inserted` | `#e6ffe7` | Grove | 2.1 JND | persistent |
| <img src="https://placehold.co/16x16/f2e7e8/f2e7e8" width="16" height="16" alt="#f2e7e8"> | `diff-removed` | `#f2e7e8` | Coral | 2.0 JND | persistent |

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
| 1 | red | <img src="https://placehold.co/16x16/e78975/e78975" width="16" height="16" alt="#e78975"> | `#e78975` | Coral | 7.08 |
| 2 | green | <img src="https://placehold.co/16x16/99cd8a/99cd8a" width="16" height="16" alt="#99cd8a"> | `#99cd8a` | Grove | 9.86 |
| 3 | yellow | <img src="https://placehold.co/16x16/d6b95c/d6b95c" width="16" height="16" alt="#d6b95c"> | `#d6b95c` | Gold | 9.42 |
| 4 | blue | <img src="https://placehold.co/16x16/7babde/7babde" width="16" height="16" alt="#7babde"> | `#7babde` | Sky | 7.50 |
| 5 | magenta | <img src="https://placehold.co/16x16/d58ec3/d58ec3" width="16" height="16" alt="#d58ec3"> | `#d58ec3` | Orchid | 7.30 |
| 6 | cyan | <img src="https://placehold.co/16x16/6ed0d1/6ed0d1" width="16" height="16" alt="#6ed0d1"> | `#6ed0d1` | Sea Salt | 9.99 |
| 7 | white | <img src="https://placehold.co/16x16/a0aeb5/a0aeb5" width="16" height="16" alt="#a0aeb5"> | `#a0aeb5` | Subtle | 7.93 |
| 8 | bright black | <img src="https://placehold.co/16x16/778b97/778b97" width="16" height="16" alt="#778b97"> | `#778b97` | Faint | 5.10 |
| 9 | bright red | <img src="https://placehold.co/16x16/faa491/faa491" width="16" height="16" alt="#faa491"> | `#faa491` | Coral, brightened | 9.28 |
| 10 | bright green | <img src="https://placehold.co/16x16/a9de9a/a9de9a" width="16" height="16" alt="#a9de9a"> | `#a9de9a` | Grove, brightened | 11.70 |
| 11 | bright yellow | <img src="https://placehold.co/16x16/e7ca6d/e7ca6d" width="16" height="16" alt="#e7ca6d"> | `#e7ca6d` | Gold, brightened | 11.24 |
| 12 | bright blue | <img src="https://placehold.co/16x16/92c3f7/92c3f7" width="16" height="16" alt="#92c3f7"> | `#92c3f7` | Sky, brightened | 9.78 |
| 13 | bright magenta | <img src="https://placehold.co/16x16/eda4da/eda4da" width="16" height="16" alt="#eda4da"> | `#eda4da` | Orchid, brightened | 9.40 |
| 14 | bright cyan | <img src="https://placehold.co/16x16/7fe1e1/7fe1e1" width="16" height="16" alt="#7fe1e1"> | `#7fe1e1` | Sea Salt, brightened | 11.84 |
| 15 | bright white | <img src="https://placehold.co/16x16/eeeeef/eeeeef" width="16" height="16" alt="#eeeeef"> | `#eeeeef` | Ink | 15.58 |

### Dawn (background Canvas `#f4f7f9`)

| # | Slot | | Hex | From | On Canvas |
|--:|---|:-:|---|---|---|
| 0 | black | <img src="https://placehold.co/16x16/25313b/25313b" width="16" height="16" alt="#25313b"> | `#25313b` | Body | 12.34 |
| 1 | red | <img src="https://placehold.co/16x16/88323e/88323e" width="16" height="16" alt="#88323e"> | `#88323e` | Coral | 7.59 |
| 2 | green | <img src="https://placehold.co/16x16/3d763e/3d763e" width="16" height="16" alt="#3d763e"> | `#3d763e` | Grove | 5.06 |
| 3 | yellow | <img src="https://placehold.co/16x16/7a6716/7a6716" width="16" height="16" alt="#7a6716"> | `#7a6716` | Gold | 5.16 |
| 4 | blue | <img src="https://placehold.co/16x16/2a5785/2a5785" width="16" height="16" alt="#2a5785"> | `#2a5785` | Sky | 6.97 |
| 5 | magenta | <img src="https://placehold.co/16x16/7b3d6f/7b3d6f" width="16" height="16" alt="#7b3d6f"> | `#7b3d6f` | Orchid | 7.13 |
| 6 | cyan | <img src="https://placehold.co/16x16/186f7f/186f7f" width="16" height="16" alt="#186f7f"> | `#186f7f` | Sea Salt | 5.39 |
| 7 | white | <img src="https://placehold.co/16x16/c1d6e2/c1d6e2" width="16" height="16" alt="#c1d6e2"> | `#c1d6e2` | Edge | 1.40 |
| 8 | bright black | <img src="https://placehold.co/16x16/566c7a/566c7a" width="16" height="16" alt="#566c7a"> | `#566c7a` | Faint | 5.11 |
| 9 | bright red | <img src="https://placehold.co/16x16/6e1929/6e1929" width="16" height="16" alt="#6e1929"> | `#6e1929` | Coral, brightened | 10.64 |
| 10 | bright green | <img src="https://placehold.co/16x16/1e5821/1e5821" width="16" height="16" alt="#1e5821"> | `#1e5821` | Grove, brightened | 7.89 |
| 11 | bright yellow | <img src="https://placehold.co/16x16/584a0d/584a0d" width="16" height="16" alt="#584a0d"> | `#584a0d` | Gold, brightened | 8.13 |
| 12 | bright blue | <img src="https://placehold.co/16x16/11406c/11406c" width="16" height="16" alt="#11406c"> | `#11406c` | Sky, brightened | 9.89 |
| 13 | bright magenta | <img src="https://placehold.co/16x16/612557/612557" width="16" height="16" alt="#612557"> | `#612557` | Orchid, brightened | 10.22 |
| 14 | bright cyan | <img src="https://placehold.co/16x16/0f515d/0f515d" width="16" height="16" alt="#0f515d"> | `#0f515d` | Sea Salt, brightened | 8.29 |
| 15 | bright white | <img src="https://placehold.co/16x16/e1eaef/e1eaef" width="16" height="16" alt="#e1eaef"> | `#e1eaef` | Raised | 1.13 |

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
12. **New surfaces are derived, not invented.** If a tool needs a surface not listed here, derive it with the surface rules in [construction.md](construction.md#3-neutrals) and re-check every text level on it.
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
   - every foreground meets its level on the surface it actually sits on;
   - code colors meet the flavor minimum (7:1 Dusk, 4.5:1 Dawn) on Canvas and on diff backgrounds;
   - control boundaries and focus indicators reach 3:1;
   - no `#000000`, no `#ffffff`, nothing outside sRGB;
   - the accent fills nothing larger than a button or badge.

If a tool cannot express a rule, such as a border on the current line, leave the effect out rather than borrowing a color from another role.

## 13. Guarantees

| Guarantee | Dusk | Dawn |
|---|---|---|
| Ink on any surface | 13.76:1 | 14.81:1 |
| Body on any surface | 10.90:1 | 10.89:1 |
| Subtle on any surface | 7.00:1 | 7.00:1 |
| Faint on any surface | 4.50:1 | 4.51:1 |
| Control boundary on any surface | 3.03:1 | 3.02:1 |
| Accent focus on any surface, every accent | 5.65:1 | 3.00:1 |
| Code colors on every code surface | 7.04:1 | 4.50:1 |
| Smallest code-color difference, normal vision | ΔE 0.089 | ΔE 0.077 |
| Smallest code-color difference, color-vision deficiency | ΔE 0.054 | ΔE 0.041 |
| Pure black or white | none | none |
| Gamut | sRGB | sRGB |

Contrast is WCAG 2.x relative-luminance contrast on final sRGB values. Color-vision figures are the worst case across simulated deuteranopia, protanopia and tritanopia, over the six code colors (Orchid, Sky, Sea Salt, Grove, Gold, Ember) and the cursor.
