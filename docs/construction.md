# Twilight construction

Version 1.0. How every value was derived, optimized and validated.

The companion document, [design-system.md](design-system.md), defines the system and how to apply it. This one explains why each value is what it is. It is written so the full palette can be rebuilt from two seeds and the rules below.

---

## 1. Method in one page

1. **Two seeds are chosen by hand**: Afterglow `#ee7a1f` and a neutral hue at its exact complement.
2. **Everything is computed in OKLCH** (perceptual lightness L, chroma C, hue h) and **validated in sRGB** with WCAG 2.x contrast. OKLCH predicts perception; it does not compute contrast, so every result is checked on the rendered value.
3. **Out-of-gamut colors are mapped by reducing chroma**, which preserves L and h, never by clipping RGB channels.
4. **Neutral surfaces follow a geometric progression**; **text levels are solved by contrast targets** against the hardest surface.
5. **The six hues are anchored to the ANSI standard** (RGB cube corners), lit by one shared "sunset" chroma law, and **optimized jointly with a seventh hue (Ember)** for distinguishability, including under color-vision deficiency.
6. **The variant floor is solved, not chosen**: the base lightness is raised (Dusk) or lowered (Dawn) until the weakest code color meets exactly 7:1 or 4.5:1 on the most demanding code surface.
7. **Syntax roles are assigned from data**: measured token frequencies and adjacencies in real code, plus the measured conventions of ten widely used themes.
8. **Background states are measured in just-noticeable differences** and bounded so no text level loses its guarantee.
9. **Dawn mirrors Dusk**: the same contrast ratios between surfaces, the same text targets, the same rules.

Designer decisions are listed explicitly in §12; everything else follows from them.

---

## 2. Seeds

| Seed | Value | Rationale |
|---|---|---|
| Afterglow | `#ee7a1f` · `oklch(0.700 0.170 51.9)` | A saturated sunset orange. Chosen by eye; it is the identity of the system. |
| Neutral hue | 232° = 51.9° + 180° | The exact complement of Afterglow. Warm light against cool shadow. |

The seeds are kept untouched. The original hand-picked neutral scale was not discarded either: its surface lightnesses (0.16, 0.20, 0.25, 0.31) turned out to be a geometric progression, which became the formal rule in §3.

---

## 3. Neutrals

### 3.1 Hue: shadows lean toward night

```
h(L) = 232° + 18° · (1 − L)²
```

The darker a neutral, the further its hue drifts toward indigo (≈ 245° at L 0.16), the way shadows cool at dusk. At text lightness the drift vanishes (≈ 232°).

### 3.2 Chroma: tinted in the middle, clean at the ends

```
C(L) = 0.035 · sin²(π · L)
```

Chroma peaks at mid-lightness (≈ 0.035) and approaches zero at both ends, so the darkest surfaces and the lightest text read as clean, not muddy or tinted. At L 0.95 chroma is ≈ 0.001, below what 8-bit sRGB can express, so Ink is effectively neutral.

### 3.3 Surfaces (Dusk): geometric in lightness

```
L(Shell) = 0.16   L(Canvas) = 0.20   L(Raised) = 0.25   L(Edge) = 0.3125
ratio r = 1.25 between consecutive steps, anchored at Canvas = 0.20
```

Equal ratios in L produce steps that look evenly spaced in the dark range, where absolute lightness differences are perceived more strongly.

### 3.4 Rail: a half step

Rail is placed so its contrast to Shell equals its contrast to Canvas:

```
contrast(Rail, Canvas) = contrast(Rail, Shell) = √ contrast(Shell, Canvas)
```

Dusk: `#0e1316` (1.035:1 to each side). Dawn: `#eff3f5` (1.038:1 / 1.036:1).

### 3.5 Text and control levels: solved by contrast

Each level is the lightness, on the neutral curve, that meets an exact contrast target **against Raised**. Raised is the hardest surface for text (it is the lightest surface in Dusk and the darkest in Dawn), so meeting the target there guarantees it on every surface.

| Level | Target vs Raised | Dusk L | Dawn L |
|---|---|---|---|
| Control | 3.0:1 (non-text minimum) | 0.528 | 0.615 |
| Faint | 4.5:1 (AA text) | 0.625 | 0.519 |
| Subtle | 7.0:1 (AAA text) | 0.742 | 0.416 |
| Body | 10.9:1 = 7² / 4.5 (next geometric step) | 0.874 | 0.307 |
| Ink | fixed at L 0.95 (Dusk) / 0.20 (Dawn): the brightest/darkest value allowed by the no-absolutes rule | 0.949 | 0.200 |

Solving is done by bisection on L along the neutral curve, evaluating WCAG contrast on the final hex value.

This replaced an earlier hand-tuned scale in which the faint level reached only 4.44:1 on raised surfaces and needed an exception rule. With solved levels, no exceptions exist.

---

## 4. Dawn: the mirror

Dawn is not an inverted Dusk; it is Dusk's *relations* applied to a light canvas.

| Rule | Implementation |
|---|---|
| Canvas | L 0.975 (the lightest value allowed, no absolute white) |
| Surface separation | Shell, Raised and Edge are placed at **the same contrast ratios to Canvas as in Dusk**: 1.07, 1.13 and 1.39–1.40:1 |
| Direction | All surfaces step *down* from Canvas. Raised is darker than Canvas, matching the light-mode convention of tinted floating panels |
| Surface chroma | Same **relative chroma** as the Dusk mirror (C / Cmax at that L and h). Copying absolute chroma would turn near-white surfaces visibly blue |
| Text levels | Same targets (4.5 / 7.0 / 10.9 / 3.0) against Raised |
| Ink | L 0.20, Dusk's Canvas lightness: the darkest value allowed |

Result: every solved target and every surface separation is identical in both variants to within ±0.01.

---

## 5. Accent families

Any of the eight colors can be the accent. Each one gets the same five tokens, built by the same rules. Every variant keeps the hue and relative chroma (C / Cmax) of its color; only lightness moves.

| Token | Rule |
|---|---|
| `accent` | The color itself. For Afterglow, the seed. |
| `on-accent` | Whichever extreme neutral has the higher contrast on `accent`: Shell or Ink in Dusk, Ink or Canvas in Dawn |
| `accent-text` | The color itself if it reaches 7:1 (Dusk) or 4.5:1 (Dawn) on Raised; otherwise the nearest lightness that does |
| `accent-pressed` | `accent` darkened by up to 0.10 L, stopping early if `on-accent` would fall below 4.5:1 |
| `accent-focus` | The color itself if it reaches 3:1 on Shell, Rail, Canvas and Raised; otherwise the nearest lightness that does |

For Afterglow this gives, in Dusk: text `#fb914a` (7.03:1 on Raised), pressed `#c26217` (label 4.66:1), focus `#ee7a1f` (5.65:1 or more). In Dawn: text `#a55212` (4.51:1), pressed `#c66417` (label 4.51:1), focus `#cf6a1a` (3.00:1 or more). Every other accent passes the same checks; the full table is in [design-system.md](design-system.md#5-accents).

An earlier hand-made accent ramp used arbitrary hue drifts (−6°, +8°, +12°) and chromas. It was replaced: a constant hue is the safe choice in OKLCH, and the targets make each variant's lightness necessary.

### Why selection does not follow the accent

Letting the selection background take the accent's hue was tested and rejected. Gold, Sea Salt, Grove and Coral already tint other background states (search matches, word highlights, diff lines). With those accents the selection became identical to another state (ΔE below 0.003). Even with the remaining accents, the inactive selection fell within 1 JND of another state in most cases. Background states therefore belong to the flavor. Selection is always tinted with Afterglow, the one hue no other state uses.

## 6. Hues

### 6.1 Anchors: the ANSI standard

The six ANSI chromatic colors are defined by the corners of the RGB cube. Measured in OKLCH:

| Slot | Anchor hue | sRGB cusp lightness |
|---|---|---|
| red | 29.2° | 0.63 |
| yellow | 109.8° | 0.97 |
| green | 142.5° | 0.87 |
| cyan | 194.8° | 0.91 |
| blue | 264.1° | 0.45 |
| magenta | 328.4° | 0.70 |

Every hue may move at most **±25°** from its anchor, so red stays red and blue stays blue.

An earlier version placed six hues at equal 60° steps from the accent. That was mathematically tidy but semantically wrong: it had no true red, merged cyan and blue, and used one lightness for all hues. It was discarded.

### 6.2 Lightness: each hue at its natural height

```
L = L₀ + β · (L_cusp(h) − mean L_cusp)        β = 0.30
```

Yellow is naturally light and blue naturally dark. Forcing equal lightness makes yellow olive and blue chalky. The slope β was **measured** by regressing lightness against cusp lightness in three established themes: 0.46 (Dracula), 0.28 (Catppuccin Mocha) and 0.17 (One Dark), with correlations of 0.87, 0.85 and 0.61. β = 0.30 is their mean.

L₀ is not chosen. It is **solved by bisection** so that the weakest of the six hues meets exactly the variant floor (7:1 Dusk, 4.5:1 Dawn) on the most demanding code surface (§6.6).

### 6.3 Chroma: one shared warm light

```
C = min( (C_Afterglow / φ) · (1 + τ · cos(h − 52°)),  0.92 · Cmax(L, h) )
C_Afterglow = 0.170   φ = 1.618…   τ = 0.15
```

- **Absolute, not relative, chroma.** Relative chroma (a fixed fraction of the gamut limit) was tested and rejected: green's sRGB gamut is so large that it rendered neon.
- **C₀ = C_Afterglow / φ = 0.105.** The golden-ratio division keeps every hue clearly below the accent, so Afterglow always leads.
- **τ = 0.15 tilts chroma toward warmth**: hues near Afterglow get up to 15 % more chroma, hues opposite it up to 15 % less, as if lit by the same low sun.
- **0.92 · Cmax** keeps an 8 % margin inside the sRGB boundary.

### 6.4 Ember: the seventh color

Code needs seven distinguishable colors (keyword, function, type, string, constant, parameter, plus error). Using a lighter Afterglow for parameters collided with Gold: ΔE 0.016 under deuteranopia, effectively identical. Ember was therefore added as a **seventh hue optimized together with the other six**, constrained to the accent family:

- hue ∈ [45°, 70°]
- free lightness: [0.60, 0.90] (Dusk) or [0.35, 0.65] (Dawn)
- the same chroma law

The optimizer placed Ember at the edge of its lightness range: Dusk `#fcd1ad` (L 0.889, h 62°), Dawn `#6c3d0d` (L 0.409, h 60°). Ember separates from Gold by **lightness rather than hue**, which is the only dimension that survives every type of color-vision deficiency.

### 6.5 Joint optimization

```
maximize   min over all pairs (i, j) and vision ∈ {normal, deuteranopia, protanopia, tritanopia}
               ΔE_OK( sim_vision(cᵢ), sim_vision(cⱼ) )
subject to |hᵢ − anchorᵢ| ≤ 25°,  Ember constraints above,
           every color ≥ floor on every code surface,
           ΔE_OK(Ember, Afterglow) ≥ 0.06 (normal vision)
```

Simulations are full-severity dichromacy (ColorAide implementation). The search is coordinate descent with 10 random restarts and hue steps of 8°, 4°, 2° and 1°.

| Hue | Anchor | Dusk | Shift | Dawn | Shift |
|---|---|---|---|---|---|
| Coral | 29° | 33° | +4 | 15° | −14 |
| Gold | 110° | 92° | −18 | 95° | −15 |
| Grove | 142° | 139° | −3 | 144° | +2 |
| Sea Salt | 195° | 196° | +1 | 213° | +18 |
| Sky | 264° | 251° | −13 | 251° | −13 |
| Orchid | 328° | 336° | +8 | 335° | +7 |
| Ember | — | 62° | — | 60° | — |
| L₀ | | 0.758 | | 0.480 | |

Gold moved toward a warmer, metallic yellow in both variants. That is the shift that separates it from Grove under red-green deficiencies.

### 6.6 Floors are validated on every code surface

Code is drawn on Canvas *and* on diff backgrounds. The floor is therefore solved against the worst of those three surfaces, not Canvas alone. In Dawn this made the code colors slightly deeper. It also fixed a defect where the light diff-removed background was invisible (ΔE 0.014): there was no contrast headroom to tint it.

### 6.7 Brights

```
L_bright = L + (L_Ink − L) / 3        (same hue; chroma capped to gamut)
```

Each bright moves one third of the way toward Ink. It is brighter in Dusk and deeper in Dawn, and always gains contrast. Gold, already light in Dusk, barely moves and never washes out.

---

## 7. Measured distinctness

| Theme | Min contrast (6 hues) | Min ΔE, normal | Min ΔE, color-vision deficiency |
|---|---|---|---|
| **Twilight Dusk** | **7.08** | 0.074 | **0.044** |
| **Twilight Dawn** | **5.06** | 0.077 | **0.041** |
| Catppuccin Mocha | 7.08 | 0.070 | 0.022 |
| Monokai | 3.93 | 0.110 | 0.052 |
| Dracula | 4.53 | 0.131 | 0.009 |
| One Dark | 4.38 | 0.077 | 0.009 |

Same method for all: the six ANSI chromatic colors plus each theme's orange; contrast on each theme's own background; color-vision figure = worst case across the three dichromacies.

Themes with larger normal-vision separation achieve it with contrast below AA. Twilight is the only one that combines AAA contrast, high separation and strong color-vision robustness. On the six colors actually used for code plus the cursor (Coral excluded, since it marks only errors), the figures are 0.089 / 0.054 (Dusk) and 0.077 / 0.041 (Dawn).

---

## 8. Syntax roles

Which hue colors which code category was derived from data, not taste.

### 8.1 Corpus

Real source code was tokenized with standard TextMate grammars:

| Language | Files | Tokens |
|---|---|---|
| TypeScript | 21 | 27,923 |
| JavaScript | 22 | 62,783 |
| Python | 20 | 116,655 |
| **Total** | **63** | **207,361** |

For each category, the study measured its share of characters (how much of the screen it occupies) and its adjacency with other categories (which colors end up side by side). The most frequent adjacency is keyword next to plain variable (14 %).

### 8.2 Convention

The colors that ten widely used themes give each category were measured on the same corpus: Dracula, One Dark Pro, Monokai, Catppuccin Mocha, GitHub Dark, Tokyo Night, Nord, Ayu Dark, Rosé Pine and Night Owl. Strongest conventions:

| Category | Measured convention |
|---|---|
| Property | uncolored in 8/10 |
| Keyword | magenta, pink or red in 7/10 |
| String | green in 5/10 |
| Function | blue in 4/10 |
| Parameter | orange in 4/10 |
| Type | cyan in 3/10 (split) |
| Constant | blue in 4/10 (split) |

### 8.3 Objective

```
J = ½ · Convention + ½ · (AdjacencyDistinctness − VisualEnergy)
```

- **Convention**: the share of the ten themes that agree with a given category→hue pairing.
- **AdjacencyDistinctness**: ΔE between colors, weighted by how often their categories are adjacent.
- **VisualEnergy**: Σ (category share × the color's salience against Body). Frequent categories should be calm; rare ones may stand out.

Hard rules: Coral is excluded (reserved for errors), Afterglow is excluded (it is the default accent), and at least one category stays uncolored.

All 5,040 assignments were scored. The search was repeated in **36 scenarios** (each language alone and combined, × three weightings of each term). The assignment that won the most scenarios (10 of 36, more than any other) was adopted. Per category, the votes were:

| Category | Result | Votes (of 36) |
|---|---|---|
| Keyword | Orchid | 31 |
| String | Grove | 26 |
| Type | Sea Salt | 19 |
| Parameter | Ember | 19 |
| Property | uncolored (Body) | 19 |
| Function | Sky | 11 (tied with Sea Salt; decided by the winning full assignment) |
| Constant | Gold | 13 (Sky had 18, but Sky is taken by functions in the winning full assignment) |

Function and constant are the two roles where neither convention nor perception gives a clear majority. The whole-assignment winner was used so that no two roles claim the same color.

---

## 9. Background states

### 9.1 Visibility unit

1 JND = ΔE_OK 0.02 against Canvas (≈ the threshold of a just-noticeable color difference in OKLab).

| State | Target |
|---|---|
| `selection` | 4 JND |
| `find-match` | 5 JND |
| `word-highlight-write` | 3 JND |
| `find-match-other` | 2.5 JND |
| `selection-inactive`, `word-highlight`, diff lines | 2 JND |

### 9.2 Bounds

- **Transient states** may move in lightness, but Faint text must keep 4.5:1 on them, which also keeps every higher text level above its guarantee.
- **Persistent states (diff lines) are code surfaces.** The code floor is solved including them (§6.6).
- **Lightness bounded** between Shell (Dusk) and 0.985 (Dawn); minimum chroma 0.010 so the hue is recognizable.
- **If a target is unreachable** inside those bounds, the state takes the maximum visibility the bounds allow and keeps its hue. It never falls back to a neutral. Dusk `find-match` reaches 3.6 of 5 JND; Dawn `selection` reaches 2.2 of 4 JND. Both are documented as limits; `word-highlight-write` (Dusk 2.6, Dawn 2.3 of 3 JND) and Dawn `find-match` (3.1 of 5 JND) are bounded the same way.

### 9.3 Search

For each hue, chroma rises from 0.010 in steps of 0.001. For each chroma, lightness is scanned outward from Canvas in both directions until a bound is hit. The color that reaches the target with the smallest combined change in lightness and chroma wins.

---

## 10. Validation

Every published value was checked automatically on its final sRGB hex:

- each text level on each surface it may occupy;
- each code color on Canvas and on both diff backgrounds;
- each control boundary and focus color on every surface (≥ 3:1);
- every accent family against its partners (`on-accent` on fill and pressed, `accent-text` on Raised, `accent-focus` on every surface);
- every color inside sRGB, with no `#000000` and no `#ffffff`;
- pairwise ΔE across normal vision and three dichromacies.

During validation, Dawn's original focus color (`#de711c`) passed 3:1 on Canvas but only 2.65:1 on Raised. It was re-solved against all surfaces (`#cf6a1a`). This is why every target in this system is solved against the hardest surface, not the most common one.

---

## 11. Known limits

| Limit | Reason |
|---|---|
| Dawn code colors are AA (4.5:1), not AAA | At 7:1 on a light canvas, yellow becomes olive and blue shifts to indigo (tested). AA keeps hue identity consistent with Dusk. |
| Dawn `selection` is 2.2 JND (target 4) | A stronger tint would push Faint text below 4.5:1. |
| Dusk `find-match` is 3.6 JND (target 5) | Same bound. |
| ANSI black and white are 1.4:1 on the background | Convention: they are used mostly as backgrounds. Bright black (Faint) is readable as text. |
| Closest pairs under color-vision deficiency: Sky–Orchid and Gold–Grove in Dusk (ΔE 0.054–0.057); Sea Salt–Orchid and Grove–Sea Salt in Dawn (ΔE 0.041) | No seven-hue palette separates every pair for every vision type. Twilight's worst case is about twice that of the strongest comparable AAA theme. |
| Dawn background states sit close together | Dawn has little room between Canvas and the Faint bound, so some states are within 1 JND of each other: selection and inactive selection (ΔE 0.004), the two word highlights (0.006), inactive selection and removed diff (0.008). They rarely appear in the same place, but they cannot be told apart by color alone. |
| OKLCH hue drift in near-neutrals | Below C 0.002, 8-bit quantization makes hue undefined (Ink). This is invisible by definition. |

---

## 12. Parameters: decided vs derived

### Decided (design choices)

| Parameter | Value | Note |
|---|---|---|
| Afterglow seed | `#ee7a1f` | Identity |
| Neutral hue | complement of the seed (232°) | Structural choice |
| Neutral hue drift | +18° · (1 − L)² | "Shadows lean toward night" |
| Neutral chroma amplitude | 0.035 | Tint strength |
| Surface ratio | r = 1.25, Canvas at L 0.20 (Dusk), 0.975 (Dawn) | Matches the original hand-picked scale |
| Warm tilt τ | 0.15 | Strength of the shared warm light |
| Chroma base | C_Afterglow / φ | Keeps the accent dominant |
| Hue freedom | ±25° from ANSI anchors | Preserves meaning |
| Ember hue range | 45°–70° | Keeps it in the accent family |
| Floors | 7:1 Dusk, 4.5:1 Dawn | AAA / AA |
| Text targets | 4.5, 7.0, 10.9; control 3.0 | WCAG thresholds plus one geometric step |
| JND targets | §9.1 | Visibility per state |
| Gamut margin | 0.92 · Cmax | Safety margin |
| Bright step | one third toward Ink | Consistent in both variants |

### Measured (from data)

| Parameter | Source |
|---|---|
| β = 0.30 | Mean slope of three established themes |
| Syntax role assignment | 207,361 tokens and ten themes (§8) |

### Solved (everything else)

Every hex value in [design-system.md](design-system.md): L₀, the six hue shifts, Ember's hue and lightness, all text and control lightnesses, all eight accent families, Rail, every state background, every bright, and all Dawn surfaces.

---

## 13. Reproducing the palette

```
for variant in (Dusk, Dawn):
    surfaces  ← geometric(r=1.25) [Dusk] | mirror contrast ratios [Dawn]
    rail      ← half-step contrast between shell and canvas
    levels    ← bisect L on neutral curve until contrast(level, raised) = target
    accents   ← for each of the 8 colors, the five tokens of §5
    diff bg   ← state(grove), state(coral) at 2 JND under the Faint bound
    hues      ← argmax min-ΔE over 4 vision models, with
                 L = L₀ + β(cusp − mean),  C = min(C₀(1+τcos(h−52°)), 0.92 Cmax),
                 L₀ solved so min contrast over {canvas, diff bgs} = floor
    brights   ← L + (L_ink − L)/3
    states    ← JND targets under transient / persistent bounds
    validate  ← every pairing in §10
```

Tools: any library implementing OKLab/OKLCH, sRGB gamut testing, WCAG contrast and dichromacy simulation. The reference implementation used Python with ColorAide.

---

## 14. Nightfall

Nightfall re-runs this construction for a dark flavor with three decided parameters changed; every rule and every other parameter, including the surface ratio, is Dusk's.

### 14.1 Decided parameters

| Parameter | Dusk | Nightfall | Source |
|---|---|---|---|
| Afterglow seed | `#ee7a1f` | `#f9a36b` | Thesis role `accent_primary` |
| Neutral chroma amplitude A | 0.035 | 0.018 | Fit, §14.2 (raw 0.0182) |
| Neutral hue drift D | 18° | 8° | Fit, §14.2 (raw 8.419) |
| Surface ratio r | 1.25 | 1.25 | Inherited from Dusk (fitted 1.2639, not used) |

The neutral hue follows the seed (+180°), as in §12. The thesis fit gives r = 1.2639, but Nightfall uses Dusk's 1.25: design-system principle 6 requires every flavor to share the surface ratio, and Twilight wins over thesis-derived values. `fit()` still reports r, labelled "reported, not used (principle 6)".

### 14.2 Fit method

The thesis conversion of Dusk (thesis repo commit `aa39cf0`, `demo/twilight.js`, `variants.thesis.roles`) gives hex values for the roles below. Each is matched to the Twilight token with the most similar definition.

| Twilight token | Thesis role | Hex |
|---|---|---|
| Shell | `bg_crust` | `#03070A` |
| Rail | `bg_mantle` | `#090F13` |
| Canvas | `bg_base` | `#11171B` |
| Raised | `bg_floating` | `#1E2428` |
| Edge | `border_subtle` | `#242A2F` |
| Control | `bg_overlay0` | `#646B70` |
| Faint | `text_subtle` | `#7A8086` |
| Subtle | `text_subtext1` | `#BAC0C7` |
| Body | `text_body` | `#D0D6DD` |
| Seed | `accent_primary` | `#F9A36B` |

- **A and D.** Least squares over the nine neutrals in OKLCH: C = A·sin²(πL), and h = h_n + D·(1 − L)² with D ≥ 0.
- **r (reported, not used).** Log-least-squares on Shell, Raised and Edge, anchored at Canvas (§3.3 geometric steps −1, +1, +2). Raw 1.2639.
- **Rounding.** The raw values (A 0.0182, D 8.419) are rounded to the precision of Dusk's own parameters: 0.018, 8°.

Print them with `fit()` in `tools/nightfall.py`.

### 14.3 What the thesis proposed and Twilight overrode

- One shared accent lightness. Twilight keeps its per-hue lightness (§6.2).
- A darker Shell. Twilight keeps Shell at L 0.16, so the darkest value stays above pure black (design-system §1, principle 5).
- A neutral selection. Twilight keeps selection tinted by the seed (§9).

### 14.4 What is inherited, and what is re-solved

- **Inherited from Dusk, not re-optimized.** The six hue angles, and Ember's hue and lightness. This was a decision. The §6.5 joint optimization cannot be re-run reproducibly: the original random starts are undocumented, and in 74 starts the engine never reached Dusk's published optimum.
- **Re-solved with Nightfall's parameters.** L₀ (the 7:1 floor), chroma, accents, states and brights.

### 14.5 Readings in the engine

Where this document is ambiguous, `tools/construct.py` marks the reading with a `# reading:` comment.

- Neutral hue = seed hue + 180°.
- State cost is Euclidean in (ΔL, ΔC).
- L₀ is solved on the six hues; Ember's floor is a check.
- Fitted to the published Dusk (the text does not state them): bright chroma capped at 0.92·Cmax, and state chroma bounded by Cmax at Canvas lightness.

### 14.6 Measured cost

Lower code chroma (C₀ = C_seed/φ with a softer seed) brings the code colors closer together.

| Measure | Dusk | Nightfall |
|---|---|---|
| Min ΔE_OK, six hues plus Ember, normal vision and three dichromacies (`distinctness()`) | 0.0536 | 0.0395 |
| Min ΔE_OK, six code colors plus cursor, color-vision deficiency (design-system §13) | 0.054 | 0.022 |
| Min ΔE_OK, same set, normal vision (§13) | 0.089 | 0.066 |

The two color-vision rows use different color sets. The second includes Afterglow as the cursor. Its minimum is Gold against the Afterglow cursor under deuteranopia (ΔE 0.022); Afterglow against Ember is at least 0.108 in every vision. Without the cursor the six code colors reach 0.039. Nightfall is less distinguishable than Dusk on every one of them.

### 14.7 Reproducing

```
tools/.venv/bin/python tools/nightfall.py
tools/.venv/bin/python tools/test_construct.py
```

The test first proves the engine rebuilds Dusk. The neutrals match exactly. Of the other 72 tokens, 7 differ by ΔE_OK ≤ 0.0025, and 2 background states differ by 0.0059 and 0.0061, which is below 1 JND (0.02). A tolerance of 0.0065 for states was accepted. The test then checks Nightfall's guarantees.
