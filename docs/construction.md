# Twilight construction

Version 1.4. How every value was derived, optimized and validated.

The companion document, [design-system.md](design-system.md), defines the system and how to apply it. This one explains why each value is what it is. It is written so the full palette can be rebuilt from one seed and the rules below.

---

## 1. Method in one page

1. **One seed is chosen by hand**, `#ee7a1f`. Its hue places Afterglow (the most chromatic orange sRGB holds at that hue) and the neutral hue at its exact complement.
2. **Everything is computed in OKLCH** (perceptual lightness L, chroma C, hue h) and validated in sRGB with WCAG 2.x contrast. OKLCH predicts perception; it does not compute contrast, so every result is checked on the rendered value.
3. **Out-of-gamut colors are mapped by reducing chroma**, which preserves L and h, never by clipping RGB channels.
4. **Neutral surfaces sit at fixed perceptual distances from Canvas**, taken from one geometric progression; each category sets their direction, and text levels are solved by contrast targets against the hardest surface.
5. **The six hues are anchored to the ANSI standard** (RGB cube corners), lit by one shared "sunset" chroma law, and optimized jointly with a seventh hue (Ember) for distinguishability, including under color-vision deficiency.
6. **The variant floor is solved**: the base lightness is raised (Dusk) or lowered (Dawn) until the weakest code color meets exactly 7:1 or 4.5:1 on the most demanding code surface.
7. **Syntax roles are fixed per category**: one color each, the same in both flavors, with Coral and Afterglow kept out of code.
8. **Background states are measured in just-noticeable differences**, bounded so no text level loses its guarantee, and kept 1 JND apart from each other wherever their targets allow.
9. **Dawn is the light end of the same system**: one neutral curve, the same perceptual surface distances, the same text targets and rules, and the light category's β and chroma base.

Designer decisions are listed explicitly in §12; everything else follows from them.

### 1.1 Three levels

Every parameter belongs to one level, and a flavor reads only the system and its own category, never another flavor. Changing the system changes every flavor; changing a flavor changes only that flavor.

| Level | Parameters |
|---|---|
| System | Seed and Afterglow (§2); the neutral curve (§3.1–3.2); the surface distances from r and L_ref (§3.3); Rail as a half step (§3.4); text targets (§3.5); accent families (§5); ANSI anchors, τ, gamut margin, φ, Ember's hue range and the optimizer (§6); syntax roles (§8); JND targets and state rules (§9) |
| Category (dark, light) | Direction of each surface from Canvas; direction of the text search; code floor; β; chroma base; L₀ and Ember lightness ranges; state bounds (§4) |
| Flavor (Dusk, Dawn) | Its category; Canvas and Ink lightness; neutral chroma amplitude |

---

## 2. Seed and Afterglow

| Value | Definition | Rationale |
|---|---|---|
| Seed | `#ee7a1f` · `oklch(0.700 0.170 51.9)` | A saturated sunset orange, chosen by eye. It is the origin of the system and does not appear as a token. |
| Afterglow | `#ff7d00` · `oklch(0.727 0.188 51.7)` | The sRGB cusp of the seed hue: the lightness where Cmax(L, 51.9°) peaks, at that Cmax. The most chromatic orange the gamut holds at the seed's hue. |
| Neutral hue | 232° = 52° + 180° | The exact complement of the seed. Warm light against cool shadow. |

The seed contributes its hue to Afterglow, the neutrals, the warm tilt (§6.3) and Ember's range (§6.4), and its chroma to the light chroma base (§6.3). Afterglow is computed, so it cannot drift away from the seed's hue or lose its chroma. Both flavors use the same seed and the same Afterglow.

The original hand-picked neutral scale was kept too: its surface lightnesses (0.16, 0.20, 0.25, 0.31) turned out to be a geometric progression, which became the formal rule in §3.

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

### 3.3 Surfaces: one perceptual scale

The system defines how far each surface sits from Canvas. The distances come from a geometric progression in lightness, measured as ΔE OKLab from its middle step:

```
scale:     L_ref / r,  L_ref,  L_ref · r,  L_ref · r²        r = 1.25, L_ref = 0.20
distance:  Shell = ΔE_OK(L_ref / r, L_ref) = 0.0396 (1.98 JND)
           Raised = ΔE_OK(L_ref · r, L_ref) = 0.0501 (2.51 JND)
           Edge = ΔE_OK(L_ref · r², L_ref) = 0.1135 (5.68 JND)
```

Each flavor places its surfaces on the neutral curve at these distances from its own Canvas, in its category's direction (§4). Equal ratios in L produce steps that look evenly spaced in the dark range, where absolute lightness differences are perceived more strongly; measured as ΔE, the same steps look as far apart at the light end. In Dusk, whose Canvas is L_ref, the placement returns the scale itself: Shell L 0.16, Raised 0.25, Edge 0.3125.

Placement: a 50-step bisection between Canvas and L 0.02 (darker) or L 0.999 (lighter); the result is the L nearest Canvas that reaches the distance.

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
| Ink | fixed per flavor: L 0.95 in Dusk, L 0.20 in Dawn (§4) | 0.949 | 0.200 |

Solving is done by bisection on L along the neutral curve, evaluating WCAG contrast on the final hex value.

In dark flavors, each level is the lowest L on the neutral curve that reaches its target against Raised
(50-step bisection; search ranges: Control 0.30–0.70, Faint 0.40–0.80, Subtle 0.50–0.90,
Body 0.60–0.95). In light flavors it is the highest L in 0.05–0.95. Rail (§3.4) is a 50-step bisection between Shell and Canvas.

This replaced an earlier hand-tuned scale in which the faint level reached only 4.44:1 on raised surfaces and needed an exception rule. With solved levels, no exceptions exist.

---

## 4. Dawn: the light end

Dawn is the same system read from the other end of the neutral curve. Every formula in §3 and §5–§9 is shared; the table lists what the light category and the Dawn flavor set.

| Level | Rule | Dusk (dark) | Dawn (light) |
|---|---|---|---|
| Category | Shell, Raised, Edge | at the §3.3 distances: Shell darker than Canvas, Raised and Edge lighter | at the §3.3 distances, all darker than Canvas |
| Category | Text levels | lowest L reaching the target against Raised | highest L reaching the target against Raised |
| Category | Code floor | 7:1 (AAA) | 4.5:1 (AA), see §11 |
| Category | β (§6.2) | 0.30 | 0.19 |
| Category | Chroma base C₀ (§6.3) | C_Afterglow / φ = 0.116 | C_seed / φ = 0.105 |
| Flavor | Canvas | L 0.20 | L 0.95 |
| Flavor | Ink | L 0.95 | L 0.20 |
| Flavor | Neutral chroma amplitude | 0.035 | 0.035 |
| System | Neutral curve, Rail (§3.4) | h(L), C(L) of §3.1–3.2; half step | the same |

**Canvas and Ink.** Each flavor sets its own two anchors. Dawn's Canvas (L 0.95, `#eeeeef`) and Ink (L 0.20, `#11171b`) are the same two colors as Dusk's Ink and Canvas, with the roles exchanged; they are Dawn's own parameters, so changing Dusk's anchors does not move Dawn. Ink on Canvas is 15.58:1 in both flavors. The lightest value in Twilight is therefore L 0.95, a cool silver from the near-neutral end of the curve.

**Surfaces keep the system's perceptual distances.** Shell, Raised and Edge are placed at the §3.3 distances from Canvas (1.98, 2.51 and 5.68 JND), stepping down from Canvas, the same distances Dusk uses. ΔE is the perceptual measure Twilight uses everywhere (§9.1). Matching contrast ratios instead, as Dawn did before 1.2, gives smaller visible steps near white: WCAG contrast changes faster with L at the light end, so the same ratio covers less lightness. With equal ΔE, Dawn's surfaces look as far apart as Dusk's, and the extra room lets background states reach their targets (§9.2).

**Every surface is darker than Canvas.** Light interfaces darken frames, side panels and borders against the content area rather than lightening them, and there is no room above Canvas: it already sits at the lightest value of the system.

**No chroma correction.** Before 1.2, Dawn copied the relative chroma of Dusk's surfaces to keep near-white surfaces from turning blue. On the shared curve that correction is unnecessary: chroma vanishes at both ends by construction (§3.2).

**Two Dawn floors moved with Canvas.** Before 1.2, Dawn's Canvas sat at L 0.975 (`#f4f7f9`). At L 0.95 the light surfaces are closer to Ink, so Ink on Raised, the darkest surface text sits on, falls from 14.81:1 to 13.36:1, still above every text target. The hues were optimized again for the new surfaces and β: the normal-vision separation of the code colors rose from ΔE 0.077 to 0.088, and the worst color-vision case went from 0.041 to 0.040 (Sea Salt against Grove). Dawn's floors in [design-system.md](design-system.md#13-guarantees) are these measured values.

Search ranges. Shell, Raised and Edge: §3.3. Text levels: the highest L in 0.05–0.95 that reaches the target against Raised (50 steps). Rail: §3.4, bisected between Shell and Canvas.

---

## 5. Accent families

Any of the eight colors can be the accent. Each one gets the same five tokens, built by the same rules. Every variant keeps the hue and relative chroma (C / Cmax) of its color; only lightness moves.

| Token | Rule |
|---|---|
| `accent` | The color itself. |
| `on-accent` | Whichever extreme neutral has the higher contrast on `accent`: Shell or Ink in Dusk, Ink or Canvas in Dawn |
| `accent-text` | The color itself if it reaches 7:1 (Dusk) or 4.5:1 (Dawn) on Raised; otherwise the nearest lightness that does |
| `accent-pressed` | `accent` darkened by up to 0.10 L, stopping early if `on-accent` would fall below 4.5:1 |
| `accent-focus` | The color itself if it reaches 3:1 on Shell, Rail, Canvas and Raised; otherwise the nearest lightness that does |

`accent-text` and `accent-focus` are 50-step bisections of L toward 0.95 (Dusk) or 0.20 (Dawn),
keeping hue and relative chroma. `accent-pressed` is L − 0.10. If that drops the on-accent label
below 4.5:1, a 50-step bisection finds the 4.5:1 boundary instead.

For Afterglow this gives, in Dusk: text `#ff8f42` (7.03:1 on Raised), pressed `#d26600` (label 5.21:1), focus `#ff7d00` (6.22:1 or more). In Dawn: text `#9d4b00` (4.51:1), pressed `#d26600` (label 4.85:1), focus `#c86100` (3.01:1 or more). Every other accent passes the same checks; the full table is in [design-system.md](design-system.md#5-accents).

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

Yellow is naturally light and blue naturally dark. Forcing equal lightness (β = 0) makes yellow olive and blue chalky. β sets how much of each hue's natural height (its sRGB cusp lightness, §6.1) the palette keeps.

β was measured on established dark and light themes. For each theme, the lightness of its six ANSI colors was regressed against the cusp lightness of their anchor hues. Themes whose colors do not follow the cusp (correlation below 0.6) were left out. β is the mean slope, rounded to two decimals: 0.30 for dark themes (0.304) and 0.19 for light themes (0.186). Light themes keep less of the natural spread.

The formula is the same in both flavors; β is an input, like Canvas, Ink and the floor.

L₀ is solved by bisection so that the weakest of the six hues meets exactly the variant floor (7:1 Dusk, 4.5:1 Dawn) on the most demanding code surface (§6.6).

### 6.3 Chroma: one shared warm light

```
C = min( C₀ · (1 + τ · cos(h − 52°)),  0.92 · Cmax(L, h) )
C₀ = C_Afterglow / φ = 0.116 (Dusk)    C₀ = C_seed / φ = 0.105 (Dawn)
C_Afterglow = 0.188   C_seed = 0.170   φ = 1.618…   τ = 0.15
```

- **Absolute chroma.** Relative chroma (a fixed fraction of the gamut limit) was tested and rejected: green's sRGB gamut is so large that it rendered neon.
- **C₀ is the base chroma divided by φ.** The golden-ratio division keeps every hue clearly below the accent, so Afterglow always leads.
- **The base depends on the flavor's polarity, like β.** A dark flavor's code colors sit near the cusp lightness of the seed hue, where no code color reaches the gamut limit, so they take Afterglow's chroma. A light flavor's code colors sit near L 0.46 to meet 4.5:1, where Gold and Sea Salt already reach 0.92 · Cmax with the seed's chroma. A larger base raises only the other four, and the worst color-vision separation falls (Dawn: ΔE 0.040 at C₀ 0.105, 0.033 at 0.116). Light flavors therefore take the seed's chroma.
- **τ = 0.15 tilts chroma toward warmth**: hues near the seed get up to 15 % more chroma, hues opposite it up to 15 % less, as if lit by the same low sun.
- **0.92 · Cmax** keeps an 8 % margin inside the sRGB boundary.

### 6.4 Ember: the seventh color

Code needs seven distinguishable colors (keyword, function, type, string, constant, parameter, plus error). Using a lighter Afterglow for parameters collided with Gold: ΔE 0.016 under deuteranopia, effectively identical. Ember was therefore added as a seventh hue optimized together with the other six, constrained to the accent family:

- hue ∈ [45°, 70°]
- free lightness: [0.60, 0.90] (Dusk) or [0.35, 0.65] (Dawn)
- the same chroma law

The optimizer placed Ember at the light edge of its range in Dusk, `#fcd6b7` (L 0.900, h 61°), and near the dark edge in Dawn, `#67320a` (L 0.381, h 52°). Ember separates from Gold by lightness, which is the only dimension that survives every type of color-vision deficiency.

### 6.5 Joint optimization

```
maximize   min over vision ∈ {normal, deuteranopia, protanopia, tritanopia} and over
               every pair (i, j) of the seven colors, and every code color i against the cursor:
               ΔE_OK( sim_vision(cᵢ), sim_vision(cⱼ) )
subject to |hᵢ − anchorᵢ| ≤ 25°,  Ember constraints above,
           every color ≥ floor on every code surface,
           ΔE_OK(Ember, Afterglow) ≥ 0.06 (normal vision)
```

Simulations are full-severity dichromacy (ColorAide implementation).

The cursor is Afterglow's `accent-focus` (§5). It is fixed before the search, because Afterglow does not depend on the hues. The color-vision guarantee in [design-system.md](design-system.md#13-guarantees) covers the six code colors plus the cursor, so the optimizer covers the same pairs. Coral marks only errors and is not compared with the cursor. In Dusk and Dawn no pair with the cursor is the closest one, so the published hues of both flavors are unchanged. Only Dawn's first pass (§6.6) moves: its Coral hue goes from 29° to 10°, which places the removed-diff background at 2.06 JND instead of 2.02 and 1.01 JND from the inactive selection instead of 0.61. Including the cursor keeps a future change from moving a code color onto it unnoticed.

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
- Score = min ΔE over the pairs above × four visions − 2 · max(0, 0.06 − ΔE(Ember, Afterglow)).
  A candidate whose Ember is below the floor scores −1. A candidate whose rendered hue leaves ±25°
  of its exact anchor (§6.1) scores −2, so it is never accepted.

| Hue | Anchor | Dusk | Shift | Dawn | Shift |
|---|---|---|---|---|---|
| Coral | 29° | 29° | 0 | 34° | +5 |
| Gold | 110° | 92° | −18 | 91° | −19 |
| Grove | 142° | 138° | −4 | 144° | +2 |
| Sea Salt | 195° | 193° | −2 | 219° | +24 |
| Sky | 264° | 250° | −14 | 275° | +11 |
| Orchid | 328° | 337° | +9 | 344° | +16 |
| Ember | — | 60° | — | 52° | — |
| L₀ | | 0.765 | | 0.477 | |

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

| Flavor | Min contrast (6 hues) | Min ΔE, normal | Min ΔE, color-vision deficiency |
|---|---|---|---|
| Twilight Dusk | 7.05 | 0.084 | 0.041 |
| Twilight Dawn | 5.04 | 0.088 | 0.040 |

Measured on the six ANSI chromatic colors plus Afterglow; contrast on Canvas; the color-vision figure is the worst case across the three dichromacies. On the six colors used for code plus the cursor (Coral excluded, since it marks only errors), the figures are 0.097 / 0.061 (Dusk) and 0.088 / 0.040 (Dawn).

---

## 8. Syntax roles

Each code category gets one color, the same in both flavors. The assignment comes from a study of 207,361 tokens of real TypeScript, JavaScript and Python: the share of the screen each category occupies, which categories sit next to each other, and 5,040 candidate assignments scored in 36 scenarios. The corpus is not part of this repository. The assignment it produced is fixed here as a decided parameter (§12), so both flavors rebuild from it without the study:

| Category | Color | Reason |
|---|---|---|
| Keyword | Orchid | The magenta slot. |
| String | Grove | The green slot. |
| Function | Sky | The blue slot. |
| Type | Sea Salt | The cyan slot, between Grove and Sky. |
| Constant | Gold | The yellow slot. |
| Parameter | Ember | Afterglow's family, separated from it by lightness (§6.4). |
| Property | uncolored (Body) | One category stays uncolored, so code is not colored end to end. |

Three rules hold the assignment in place:

- Coral never colors code. It is reserved for errors, so an error always stands out.
- Afterglow never colors code. It is the default accent, and the accent never colors content.
- No two categories share a color.

Every code color meets the flavor floor on every code surface (§6.6), and the seven are optimized together for distinctness (§6.5), so the assignment cannot make two categories hard to tell apart.

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
- **If a target is unreachable** inside those bounds, the state takes the maximum visibility the bounds allow and keeps its hue. It never falls back to a neutral. Dusk `find-match` reaches 3.6 of 5 JND and Dusk `word-highlight-write` 2.5 of 3; Dawn `selection` reaches 2.8 of 4 and Dawn `find-match` 4.3 of 5. All are documented as limits (§11).

### 9.3 Search

For each hue, chroma rises from 0.010 to 0.140 in steps of 0.001. For each chroma, lightness is
scanned outward from Canvas in both directions in steps of 0.001. A scan stops at the lightness
bounds (Dusk: L_Shell to 1.0; Dawn: 0 to L_Canvas), at the first out-of-gamut color, or at the first
color on which Faint falls below 4.5:1.

The first step in each direction that reaches the target is a candidate, with cost
1000 · |ΔL| + 100 · C. The lowest cost wins. If no candidate reaches the target, the state takes
the most visible color found (§9.2).

The selection hue is Afterglow's hue.

### 9.4 Separation between states

Two states that share a hue differ only in visibility, so when a bound stops the stronger one short of its target, the two can land on nearly the same color. Each state is therefore built after the ones before it, in a fixed order, and kept at least 1 JND (ΔE_OK 0.02) from every state already built:

```
diff-inserted, diff-removed, selection, selection-inactive,
find-match, find-match-other, word-highlight, word-highlight-write
```

Visibility comes first. Among the colors that reach the state's target, the lowest-cost one that is 1 JND from every earlier state wins; if none is, the lowest-cost one wins, as in §9.3. If no color reaches the target, the most visible color that keeps the separation is taken, or the most visible color found when none keeps it.

In Dusk this moves two states. `selection-inactive` goes from 2.1 to 2.9 JND, and `word-highlight-write` from 2.7 to 2.5 JND with half the chroma. The two word highlights were 0.80 JND apart, so a read and a write of the same variable looked the same; they are now 1.23 JND apart. The inactive selection and the removed diff go from 0.54 to 1.08 JND. In Dawn no color that reaches the inactive selection's target is 1 JND from the selection, so both keep their values (§11).

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
| Dusk `find-match` is 3.6 JND (target 5); Dusk `word-highlight-write` is 2.5 JND (target 3) | Same bound, and the write highlight keeps 1 JND from the read one (§9.4). |
| ANSI black and white are 1.4:1 on the background | Convention: they are used mostly as backgrounds. Bright black (Faint) is readable as text. |
| Closest pairs under color-vision deficiency: Sky–Orchid, Gold–Grove and Sea Salt–Grove in Dusk (ΔE 0.061–0.062); Sea Salt–Grove and Orchid–Sea Salt in Dawn (ΔE 0.040–0.041) | No seven-hue palette separates every pair for every vision type. These are the smallest separations the joint optimization (§6.5) reaches. |
| Dawn `selection` and `selection-inactive` are 0.96 JND apart | Both carry Afterglow's hue below Canvas, where Faint at 4.5:1 bounds them. No color that reaches the inactive selection's 2 JND target is 1 JND from the selection (§9.4). One marks the focused editor and the other the unfocused ones, so they do not share a place. Every other pair of states, in both flavors, is at least 1 JND apart. |
| OKLCH hue drift in near-neutrals | Below C 0.002, 8-bit quantization makes hue undefined (Dusk's Ink, Dawn's Canvas). This is invisible by definition. |

## 12. Parameters: decided vs derived

### Decided (design choices)

| Parameter | Value | Note |
|---|---|---|
| Seed | `#ee7a1f` | Origin of the system |
| Afterglow | the sRGB cusp of the seed hue (§2) | The most chromatic color at the seed's hue |
| Neutral hue | complement of the seed (232°) | Structural choice |
| Neutral hue drift | +18° · (1 − L)² | "Shadows lean toward night" |
| Neutral chroma amplitude (flavor) | 0.035 in Dusk and Dawn | Tint strength |
| Surface ratio (system) | r = 1.25 at L_ref = 0.20, as ΔE_OK distances (§3.3) | Matches the original hand-picked scale |
| Surface directions (category) | dark: Shell darker, Raised and Edge lighter; light: all darker | Light interfaces darken their panels (§4) |
| Anchors (flavor) | Dusk: Canvas L 0.20, Ink L 0.95. Dawn: Canvas L 0.95, Ink L 0.20 | The same two neutrals, roles exchanged |
| Warm tilt τ | 0.15 | Strength of the shared warm light |
| Chroma base | C_Afterglow / φ (Dusk), C_seed / φ (Dawn) | Keeps the accent dominant; the light flavor is bounded by the gamut at 4.5:1 (§6.3) |
| Hue freedom | ±25° from ANSI anchors | Preserves meaning |
| Ember hue range | 45°–70° | Keeps it in the accent family |
| Floors | 7:1 Dusk, 4.5:1 Dawn | AAA / AA |
| Text targets | 4.5, 7.0, 10.89 (7²/4.5); control 3.0 | WCAG thresholds plus one geometric step |
| JND targets | §9.1 | Visibility per state |
| State order and separation | §9.4, 1 JND | States that share a hue stay distinguishable |
| Gamut margin | 0.92 · Cmax | Safety margin |
| Bright step | one third toward Ink | Consistent in both variants |
| Syntax roles | §8 | Fixed from the token study; one color per category, Coral and Afterglow out of code |

### Measured (from data)

| Parameter | Source |
|---|---|
| β = 0.30 (Dusk), 0.19 (Dawn) | Mean slope of ANSI lightness against cusp lightness, measured on established dark and light themes (§6.2) |

### Solved (everything else)

Every hex value in [design-system.md](design-system.md): L₀, the six hue shifts, Ember's hue and lightness, all text and control lightnesses, all eight accent families, Rail, every state background, every bright, and Dawn's Shell, Raised and Edge.

### 12.1 Precision conventions

These conventions are part of the method. A reimplementation that differs here will produce
different hexes.

- Color → hex: convert to sRGB, gamut-map by reducing chroma (ColorAide `fit('srgb')`), round to 8 bits.
- Cmax(L, h): 32-step bisection on chroma. Where Cmax scales a chroma, L is rounded to 0.001
  (and h to 0.1° in §5 and §6.7).
- Cusp(h): the L of maximum Cmax on a 0.002 grid over L 0.300–0.998.
- Afterglow: the seed hue rounded to 0.1° (51.9°), at L = Cusp(h) and C = Cmax(L, h), then to hex.
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
    surfaces  ← the §3.3 distances from the flavor's Canvas, in the category's direction
    rail      ← half-step contrast between shell and canvas
    levels    ← bisect L on neutral curve until contrast(level, raised) = target
    hues₁     ← optimize(§6.5) against canvas
    diff bg   ← state(grove₁), state(coral₁) at 2 JND
    hues      ← optimize(§6.5) against the worst of {canvas, diff bgs}
    accents   ← for each of the 8 colors, the five tokens of §5
    brights   ← L + (L_ink − L)/3
    states    ← JND targets under transient / persistent bounds (§9.3), 1 JND apart in order (§9.4)
    validate  ← every pairing in §10
```

The reference implementation ships with the `twilight-auditor` skill. It rebuilds every token
of both variants exactly, and the skill checks this on every change.

