# Twilight construction

Version 1.2. How every value was derived, optimized and validated.

The companion document, [design-system.md](design-system.md), defines the system and how to apply it. This one explains why each value is what it is. It is written so the full palette can be rebuilt from two seeds and the rules below.

---

## 1. Method in one page

1. **Two seeds are chosen by hand**: Afterglow `#ee7a1f` and a neutral hue at its exact complement.
2. **Everything is computed in OKLCH** (perceptual lightness L, chroma C, hue h) and validated in sRGB with WCAG 2.x contrast. OKLCH predicts perception; it does not compute contrast, so every result is checked on the rendered value.
3. **Out-of-gamut colors are mapped by reducing chroma**, which preserves L and h, never by clipping RGB channels.
4. **Neutral surfaces follow a geometric progression** in Dusk and keep the same perceptual distances in Dawn; text levels are solved by contrast targets against the hardest surface.
5. **The six hues are anchored to the ANSI standard** (RGB cube corners), lit by one shared "sunset" chroma law, and optimized jointly with a seventh hue (Ember) for distinguishability, including under color-vision deficiency.
6. **The variant floor is solved**: the base lightness is raised (Dusk) or lowered (Dawn) until the weakest code color meets exactly 7:1 or 4.5:1 on the most demanding code surface.
7. **Syntax roles are assigned from data**: measured token frequencies and adjacencies in real code, plus the measured conventions of ten widely used dark themes, checked against ten light themes.
8. **Background states are measured in just-noticeable differences** and bounded so no text level loses its guarantee.
9. **Dawn is the light end of the same system**: one neutral curve, Canvas and Ink swapped, the same perceptual surface distances, the same text targets and rules, and its own measured β.

Designer decisions are listed explicitly in §12; everything else follows from them.

---

## 2. Seeds

| Seed | Value | Rationale |
|---|---|---|
| Afterglow | `#ee7a1f` · `oklch(0.700 0.170 51.9)` | A saturated sunset orange. Chosen by eye; it is the identity of the system. |
| Neutral hue | 232° = 51.9° + 180° | The exact complement of Afterglow. Warm light against cool shadow. |

Both flavors use the same two seeds, untouched. The original hand-picked neutral scale was kept too: its surface lightnesses (0.16, 0.20, 0.25, 0.31) turned out to be a geometric progression, which became the formal rule in §3.

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

Chroma peaks at mid-lightness (≈ 0.035) and approaches zero at both ends, so dark surfaces and light text (Dusk), and light surfaces and dark text (Dawn), read as clean, not muddy or tinted. At L 0.95 chroma is ≈ 0.001, below what 8-bit sRGB can express, so Dusk's Ink and Dawn's Canvas are effectively neutral: a cool silver, never paper white.

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

Dusk: `#0e1316` (1.035:1 to each side). Dawn: `#e6e8e8` (1.061:1 to Canvas, 1.066:1 to Shell).

### 3.5 Text and control levels: solved by contrast

Each level is the lightness, on the neutral curve, that meets an exact contrast target against Raised. Raised is the hardest surface for text (it is the lightest surface in Dusk and the darkest in Dawn), so meeting the target there guarantees it on every surface.

| Level | Target vs Raised | Dusk L | Dawn L |
|---|---|---|---|
| Control | 3.0:1 (non-text minimum) | 0.528 | 0.591 |
| Faint | 4.5:1 (AA text) | 0.625 | 0.495 |
| Subtle | 7.0:1 (AAA text) | 0.742 | 0.392 |
| Body | 10.89:1 = 7² / 4.5 (next geometric step; used unrounded) | 0.874 | 0.275 |
| Ink | fixed: L 0.95 in Dusk, L 0.20 in Dawn (the two anchors, swapped; §4) | 0.949 | 0.200 |

Solving is done by bisection on L along the neutral curve, evaluating WCAG contrast on the final hex value.

In Dusk, each level is the lowest L on the neutral curve that reaches its target against Raised
(50-step bisection; search ranges: Control 0.30–0.70, Faint 0.40–0.80, Subtle 0.50–0.90,
Body 0.60–0.95). Rail (§3.4) is a 50-step bisection between Shell and Canvas.

This replaced an earlier hand-tuned scale in which the faint level reached only 4.44:1 on raised surfaces and needed an exception rule. With solved levels, no exceptions exist.

---

## 4. Dawn: the light end

Dawn is the same system read from the other end of the neutral curve. Every formula in §3 and §5–§9 is shared; only the flavor profile below is specific to Dawn.

| Rule | Dusk | Dawn |
|---|---|---|
| Neutral curve | h(L), C(L) of §3.1–3.2 | the same curve, no correction |
| Canvas | L 0.20 | L 0.95 (Dusk's Ink) |
| Ink | L 0.95 | L 0.20 (Dusk's Canvas) |
| Shell, Raised, Edge | geometric scale (§3.3) | the same ΔE_OK from Canvas as in Dusk, darker than Canvas |
| Rail | half step (§3.4) | half step (§3.4) |
| Text levels | lowest L reaching the target against Raised | highest L reaching the target against Raised |
| Code floor | 7:1 (AAA) | 4.5:1 (AA), see §11 |
| β (§6.2) | 0.30 | 0.19, measured on light themes |

**Canvas and Ink swap.** The two anchors of the system are Dusk's Canvas (L 0.20) and Dusk's Ink (L 0.95). Dawn uses the same two colors with their roles exchanged, so Dawn's Canvas is `#eeeeef` and its Ink is `#11171b`. Ink on Canvas is 15.58:1 in both flavors. The lightest value in Twilight is therefore L 0.95, a cool silver from the near-neutral end of the curve.

**Surfaces keep Dusk's perceptual distances.** Shell, Raised and Edge are placed at the same ΔE_OK from Canvas as in Dusk (0.040, 0.050, 0.114), stepping down from Canvas. ΔE is the perceptual measure Twilight uses everywhere (§9.1). Matching contrast ratios instead, as Dawn did before 1.2, gives smaller visible steps near white: WCAG contrast changes faster with L at the light end, so the same ratio covers less lightness. With equal ΔE, Dawn's surfaces look as far apart as Dusk's, and the extra room lets background states reach their targets (§9.2).

**Every surface is darker than Canvas.** Light interfaces darken frames, side panels and borders against the content area rather than lightening them, and there is no room above Canvas: it already sits at the lightest value of the system.

**No chroma correction.** Before 1.2, Dawn copied the relative chroma of Dusk's surfaces to keep near-white surfaces from turning blue. On the shared curve that correction is unnecessary: chroma vanishes at both ends by construction (§3.2).

**Two Dawn floors moved with Canvas.** Before 1.2, Dawn's Canvas sat at L 0.975 (`#f4f7f9`). At L 0.95 the light surfaces are closer to Ink, so Ink on Raised, the darkest surface text sits on, falls from 14.81:1 to 13.36:1, still above every text target. The hues were optimized again for the new surfaces and β: the normal-vision separation of the code colors rose from ΔE 0.077 to 0.088, and the worst color-vision case went from 0.041 to 0.040 (Sea Salt against Grove). Dawn's floors in [design-system.md](design-system.md#13-guarantees) are these measured values.

Search ranges. Shell, Raised and Edge: 50-step bisection over L 0.50–0.95 on ΔE_OK to Canvas; the result is the lightest L that reaches the distance. Text levels: the highest L in 0.05–0.95 that reaches the target against Raised (50 steps). Rail: §3.4, bisected between Shell and Canvas.

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

`accent-text` and `accent-focus` are 50-step bisections of L toward 0.95 (Dusk) or 0.20 (Dawn),
keeping hue and relative chroma. `accent-pressed` is L − 0.10. If that drops the on-accent label
below 4.5:1, a 50-step bisection finds the 4.5:1 boundary instead.

For Afterglow this gives, in Dusk: text `#fb914a` (7.03:1 on Raised), pressed `#c26217` (label 4.66:1), focus `#ee7a1f` (5.65:1 or more). In Dawn: text `#9a4d10` (4.51:1), pressed `#c66417` (label 4.51:1), focus `#c46317` (3.02:1 or more). Every other accent passes the same checks; the full table is in [design-system.md](design-system.md#5-accents).

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

Every hue may move at most ±25° from its anchor, so red stays red and blue stays blue. The bound is checked on the rendered color: the hue of the final hex against the exact anchor above, not the optimizer's whole-degree parameter against the rounded anchor.

An earlier version placed six hues at equal 60° steps from the accent. That was mathematically tidy but semantically wrong: it had no true red, merged cyan and blue, and used one lightness for all hues. It was discarded.

### 6.2 Lightness: each hue at its natural height

```
L = L₀ + β · (L_cusp(h) − mean L_cusp)        β = 0.30 (Dusk), 0.19 (Dawn)
```

Yellow is naturally light and blue naturally dark. Forcing equal lightness makes yellow olive and blue chalky. The slope β was measured by regressing the lightness of a theme's six ANSI colors against the cusp lightness of their anchor hues (the true sRGB cusp, the L of the RGB-cube corner, as in the §6.1 column; not the grid `cusp()` of §12.1). For Dusk, three established themes: 0.46 (Dracula), 0.28 (Catppuccin Mocha) and 0.17 (One Dark), with correlations of 0.87, 0.85 and 0.61. β = 0.30 is their mean.

Light themes place their colors differently, so Dawn's β was measured on light themes (the ten listed in §8.2) with the same regression, keeping the themes whose correlation reaches 0.6, the lowest accepted for Dusk:

| Light theme | β | r |
|---|---|---|
| Material Theme Lighter | 0.288 | 0.80 |
| Ayu Light | 0.160 | 0.76 |
| Solarized Light | 0.110 | 0.74 |
| *Excluded (r < 0.6):* Catppuccin Latte 0.208 (0.54), Night Owl Light 0.182 (0.51), Rosé Pine Dawn 0.137 (0.30), Tokyo Night Light 0.047 (0.40), GitHub Light Default −0.312 (−0.66) | | |

β = 0.19 (mean 0.186). One Light and Light Modern define no terminal colors. The same rule applied to the ten dark themes gives 0.29, which agrees with Dusk's 0.30.

The ANSI colors of every theme used here, their sources and the regression ship with the auditor skill (`scripts/measure_beta.py`), which reproduces both values.

L₀ is solved by bisection so that the weakest of the six hues meets exactly the variant floor (7:1 Dusk, 4.5:1 Dawn) on the most demanding code surface (§6.6).

### 6.3 Chroma: one shared warm light

```
C = min( (C_Afterglow / φ) · (1 + τ · cos(h − 52°)),  0.92 · Cmax(L, h) )
C_Afterglow = 0.170   φ = 1.618…   τ = 0.15
```

- **Absolute chroma.** Relative chroma (a fixed fraction of the gamut limit) was tested and rejected: green's sRGB gamut is so large that it rendered neon.
- **C₀ = C_Afterglow / φ = 0.105.** The golden-ratio division keeps every hue clearly below the accent, so Afterglow always leads.
- **τ = 0.15 tilts chroma toward warmth**: hues near Afterglow get up to 15 % more chroma, hues opposite it up to 15 % less, as if lit by the same low sun.
- **0.92 · Cmax** keeps an 8 % margin inside the sRGB boundary.

### 6.4 Ember: the seventh color

Code needs seven distinguishable colors (keyword, function, type, string, constant, parameter, plus error). Using a lighter Afterglow for parameters collided with Gold: ΔE 0.016 under deuteranopia, effectively identical. Ember was therefore added as a seventh hue optimized together with the other six, constrained to the accent family:

- hue ∈ [45°, 70°]
- free lightness: [0.60, 0.90] (Dusk) or [0.35, 0.65] (Dawn)
- the same chroma law

The optimizer placed Ember at the light edge of its range in Dusk, `#fcd1ad` (L 0.889, h 62°), and near the dark edge in Dawn, `#67320a` (L 0.381, h 52°). Ember separates from Gold by lightness, which is the only dimension that survives every type of color-vision deficiency.

### 6.5 Joint optimization

```
maximize   min over all pairs (i, j) and vision ∈ {normal, deuteranopia, protanopia, tritanopia}
               ΔE_OK( sim_vision(cᵢ), sim_vision(cⱼ) )
subject to |hᵢ − anchorᵢ| ≤ 25°,  Ember constraints above,
           every color ≥ floor on every code surface,
           ΔE_OK(Ember, Afterglow) ≥ 0.06 (normal vision)
```

Simulations are full-severity dichromacy (ColorAide implementation).

The search is deterministic:

- Pseudo-random generator: Python `random`, seed 1, shared by all restarts of one run.
- 10 restarts. Restart 0 starts at the anchors; restarts 1–9 start at anchor + randint(−20, 20)°.
  Every restart draws Ember's start as randint(45, 70)° and a lightness chosen from its range.
- Ember range: hue 45–70°; L 0.60–0.90 (Dusk) or 0.35–0.65 (Dawn) in steps of 0.01.
- Coordinate descent over 8 variables (six hues, Ember hue, Ember L) with steps 8, 4, 2, 1
  (degrees for hues; hundredths for Ember L). A move is accepted only if the score improves by
  more than 1e-6.
- For every candidate, L₀ is re-solved (§6.2): 18-step bisection over 0.50–0.95 (Dusk, returns
  the upper bound) or 0.20–0.70 (Dawn, returns the lower bound), so the weakest of the six hues
  meets the floor.
- Score = min ΔE over the seven colors × four visions − 2 · max(0, 0.06 − ΔE(Ember, Afterglow)).
  A candidate whose Ember is below the floor scores −1. A candidate whose rendered hue leaves ±25°
  of its exact anchor (§6.1) scores −2, so it is never accepted.

| Hue | Anchor | Dusk | Shift | Dawn | Shift |
|---|---|---|---|---|---|
| Coral | 29° | 33° | +4 | 34° | +5 |
| Gold | 110° | 92° | −18 | 91° | −19 |
| Grove | 142° | 139° | −3 | 144° | +2 |
| Sea Salt | 195° | 197° | +2 | 219° | +24 |
| Sky | 264° | 251° | −13 | 275° | +11 |
| Orchid | 328° | 336° | +8 | 344° | +16 |
| Ember | — | 62° | — | 52° | — |
| L₀ | | 0.758 | | 0.477 | |

Hues and L₀ are the optimizer's parameters. Hues measured from the published hex can differ by up
to 1° after gamut mapping and 8-bit rounding.

Gold moved toward a warmer, metallic yellow in both variants. That is the shift that separates it from Grove under red-green deficiencies. In Dawn, Sea Salt moves 24° toward blue and Sky moves toward violet, which keeps the three cool hues apart at the low lightness the 4.5:1 floor requires.

### 6.6 Floors are validated on every code surface

Code is drawn on Canvas *and* on diff backgrounds, so the floor is solved against the worst of
those surfaces. This needs two passes:

1. Optimize (§6.5) against Canvas.
2. Build diff-inserted and diff-removed (§9) with the pass-1 Grove and Coral hues.
3. The worst code surface is the one with the highest luminance in Dusk, or the lowest in Dawn.
4. Optimize again against that surface. These are the published hues.

The diff backgrounds are not rebuilt after pass 2.

In Dawn before 1.2, this made the code colors slightly deeper. It also fixed a defect where the light
diff-removed background was invisible (ΔE 0.014): there was no contrast headroom to tint it.

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
| **Twilight Dawn** | **5.04** | 0.088 | **0.040** |
| Catppuccin Mocha | 7.08 | 0.070 | 0.022 |
| Monokai | 3.93 | 0.110 | 0.052 |
| Dracula | 4.53 | 0.131 | 0.009 |
| One Dark | 4.38 | 0.077 | 0.009 |

Same method for all: the six ANSI chromatic colors plus each theme's orange; contrast on each theme's own background; color-vision figure = worst case across the three dichromacies.

Themes with larger normal-vision separation achieve it with contrast below AA. Twilight is the only one that combines AAA contrast, high separation and strong color-vision robustness. On the six colors used for code plus the cursor (Coral excluded, since it marks only errors), the figures are 0.089 / 0.054 (Dusk) and 0.088 / 0.040 (Dawn).

---

## 8. Syntax roles

Which hue colors which code category was derived from data.

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

The same measurement on ten widely used light themes: Catppuccin Latte, GitHub Light Default, Tokyo Night Light, Solarized Light, One Light, Rosé Pine Dawn, Ayu Light, Night Owl Light, Material Theme Lighter and Visual Studio Code Light Modern. One hue classifier was applied to both sets:

| Category | Dark themes | Light themes | Twilight (both flavors) |
|---|---|---|---|
| Keyword | magenta 5, red 2 | magenta 5 | Orchid |
| Function | blue 4 | blue 7 | Sky |
| String | green 5 | green 5 | Grove |
| Property | uncolored 7 | uncolored 5 | uncolored |
| Parameter | orange 5 | split (no hue above 2) | Ember |
| Type | cyan 3 (split) | orange 3 (split) | Sea Salt |
| Constant | blue 3 (split) | blue 3 (split) | Gold |

Every category with a majority among the light themes agrees with the dark assignment, and no light convention contradicts it. Roles and names are therefore the same in both flavors: a keyword is Orchid in Dusk and in Dawn.

### 8.3 Objective

```
J = ½ · Convention + ½ · (AdjacencyDistinctness − VisualEnergy)
```

- **Convention**: the share of the ten themes that agree with a given category→hue pairing.
- **AdjacencyDistinctness**: ΔE between colors, weighted by how often their categories are adjacent.
- **VisualEnergy**: Σ (category share × the color's salience against Body). Frequent categories should be calm; rare ones may stand out.

Hard rules: Coral is excluded (reserved for errors), Afterglow is excluded (it is the default accent), and at least one category stays uncolored.

All 5,040 assignments were scored. The search was repeated in 36 scenarios (each language alone and combined, × three weightings of each term). The assignment that won the most scenarios (10 of 36, more than any other) was adopted. Per category, the votes were:

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
- **Lightness bounded by the surfaces.** Toward the text, the only limit is Faint at 4.5:1. Away from the text, the lightness scan stops at the outermost surface: L_Shell in Dusk, L_Canvas in Dawn. The bound applies in OKLCH before gamut mapping and 8-bit rounding, so a rendered state can sit up to ΔL 0.001 beyond it (Dawn `diff-inserted` L 0.950 against Canvas 0.949). Minimum chroma 0.010 so the hue is recognizable.
- **If a target is unreachable** inside those bounds, the state takes the maximum visibility the bounds allow and keeps its hue. It never falls back to a neutral. Dusk `find-match` reaches 3.6 of 5 JND and Dusk `word-highlight-write` 2.6 of 3; Dawn `selection` reaches 2.8 of 4 and Dawn `find-match` 4.3 of 5. All are documented as limits (§11).

### 9.3 Search

For each hue, chroma rises from 0.010 to 0.140 in steps of 0.001. For each chroma, lightness is
scanned outward from Canvas in both directions in steps of 0.001. A scan stops at the lightness
bounds (Dusk: L_Shell to 1.0; Dawn: 0 to L_Canvas), at the first out-of-gamut color, or at the first
color on which Faint falls below 4.5:1.

The first step in each direction that reaches the target is a candidate, with cost
1000 · |ΔL| + 100 · C. The lowest cost wins. If no candidate reaches the target, the state takes
the most visible color found (§9.2).

The selection hue is the seed hue.

---

## 10. Validation

Every published value was checked automatically on its final sRGB hex:

- each text level on each surface it may occupy;
- each code color on Canvas and on both diff backgrounds;
- each control boundary and focus color on every surface (≥ 3:1);
- every accent family against its partners (`on-accent` on fill and pressed, `accent-text` on Raised, `accent-focus` on every surface);
- every color inside sRGB, with no `#000000` and no `#ffffff`;
- pairwise ΔE across normal vision and three dichromacies.

While Dawn 1.0 was being validated, its focus color (`#de711c`) passed 3:1 on Canvas but only 2.65:1 on Raised, and was re-solved against all surfaces. Since then every target in this system is solved against the hardest surface.

---

## 11. Known limits

| Limit | Reason |
|---|---|
| Dawn code colors are AA (4.5:1), not AAA | Tested with the full optimizer at 7:1: the worst color-vision separation falls from ΔE 0.040 to 0.023 and normal-vision separation from 0.088 to 0.056, with yellow turning olive and blue turning navy. AA keeps the code colors as distinct as Dusk's. |
| Dawn `selection` is 2.8 JND (target 4) | A stronger tint would push Faint text below 4.5:1. Near L 0.9 the sRGB gamut of orange is narrow (Cmax ≈ 0.06), so chroma cannot make up the difference. |
| Dawn `find-match` is 4.3 JND (target 5) | Same bound. |
| Dusk `find-match` is 3.6 JND (target 5); Dusk `word-highlight-write` is 2.6 JND (target 3) | Same bound. |
| ANSI black and white are 1.4:1 on the background | Convention: they are used mostly as backgrounds. Bright black (Faint) is readable as text. |
| Closest pairs under color-vision deficiency: Sky–Orchid and Gold–Grove in Dusk (ΔE 0.054–0.057); Sea Salt–Grove, Grove–cursor and Orchid–Sea Salt in Dawn (ΔE 0.040–0.041) | No seven-hue palette separates every pair for every vision type. Twilight's worst case is about twice that of the strongest comparable AAA theme. |
| Some background states sit within 1 JND of each other | Dusk: inactive selection and removed diff (0.54 JND), the two word highlights (0.97). Dawn: inactive selection and removed diff (0.61), selection and inactive selection (0.96). Both pairs share a warm hue at low visibility. They rarely appear in the same place, but they cannot be told apart by color alone. |
| OKLCH hue drift in near-neutrals | Below C 0.002, 8-bit quantization makes hue undefined (Dusk's Ink, Dawn's Canvas). This is invisible by definition. |

## 12. Parameters: decided vs derived

### Decided (design choices)

| Parameter | Value | Note |
|---|---|---|
| Afterglow seed | `#ee7a1f` | Identity |
| Neutral hue | complement of the seed (232°) | Structural choice |
| Neutral hue drift | +18° · (1 − L)² | "Shadows lean toward night" |
| Neutral chroma amplitude | 0.035 | Tint strength |
| Surface ratio | r = 1.25, Canvas at L 0.20 (Dusk) | Matches the original hand-picked scale |
| Anchors | Canvas L 0.20 and Ink L 0.95 in Dusk; swapped in Dawn | One pair of neutrals for both flavors |
| Dawn surfaces | Dusk's ΔE_OK from Canvas, darker than Canvas | Same perceptual separation as Dusk |
| Warm tilt τ | 0.15 | Strength of the shared warm light |
| Chroma base | C_Afterglow / φ | Keeps the accent dominant |
| Hue freedom | ±25° from ANSI anchors | Preserves meaning |
| Ember hue range | 45°–70° | Keeps it in the accent family |
| Floors | 7:1 Dusk, 4.5:1 Dawn | AAA / AA |
| Text targets | 4.5, 7.0, 10.89 (7²/4.5); control 3.0 | WCAG thresholds plus one geometric step |
| JND targets | §9.1 | Visibility per state |
| Gamut margin | 0.92 · Cmax | Safety margin |
| Bright step | one third toward Ink | Consistent in both variants |

### Measured (from data)

| Parameter | Source |
|---|---|
| β = 0.30 (Dusk) | Mean slope of three established dark themes |
| β = 0.19 (Dawn) | Mean slope of the light themes with r ≥ 0.6 (§6.2) |
| Syntax role assignment | 207,361 tokens and ten dark themes, checked against ten light themes (§8) |

### Solved (everything else)

Every hex value in [design-system.md](design-system.md): L₀, the six hue shifts, Ember's hue and lightness, all text and control lightnesses, all eight accent families, Rail, every state background, every bright, and Dawn's Shell, Raised and Edge.

### 12.1 Precision conventions

These conventions are part of the method. A reimplementation that differs here will produce
different hexes.

- Color → hex: convert to sRGB, gamut-map by reducing chroma (ColorAide `fit('srgb')`), round to 8 bits.
- Cmax(L, h): 32-step bisection on chroma. Where Cmax scales a chroma, L is rounded to 0.001
  (and h to 0.1° in §5 and §6.7).
- Cusp(h): the L of maximum Cmax on a 0.002 grid over L 0.300–0.998.
- Anchors: the RGB cube corners in OKLCH, rounded to whole degrees (29, 110, 142, 195, 264, 328).
  The cusp mean in §6.2 is taken over these six anchors. The ±25° bound (§6.1) uses the exact anchors
  and the hue of the rendered hex.
- Hue lightness: L = round(L₀ + β · (cusp(h) − mean), 3), with β = 0.30 (Dusk) or 0.19 (Dawn).
- Neutral hue: the seed hue rounded to 52°, plus 180° = 232°.
- Contrast: WCAG 2.x relative luminance. ΔE: Euclidean distance in OKLab.
- Thresholds are compared on unrounded values.

---

## 13. Reproducing the palette

```
for variant in (Dusk, Dawn):
    surfaces  ← geometric(r=1.25) [Dusk] | Dusk's ΔE from Canvas, below Canvas L 0.95 [Dawn]
    rail      ← half-step contrast between shell and canvas
    levels    ← bisect L on neutral curve until contrast(level, raised) = target
    hues₁     ← optimize(§6.5) against canvas
    diff bg   ← state(grove₁), state(coral₁) at 2 JND
    hues      ← optimize(§6.5) against the worst of {canvas, diff bgs}
    accents   ← for each of the 8 colors, the five tokens of §5
    brights   ← L + (L_ink − L)/3
    states    ← JND targets under transient / persistent bounds (§9.3)
    validate  ← every pairing in §10
```

The reference implementation ships with the `twilight-auditor` skill. It rebuilds every token
of both variants exactly, and the skill checks this on every change.

