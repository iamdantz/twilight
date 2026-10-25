# Changelog

## 1.10.1

The neutral chroma amplitude is searched against the guarantees. No value changes.

### Documented
- construction.md §3.2 and §12: the amplitude 0.035 moves to the Resolved group. From 0.020 to 0.050, in steps of 0.0025, it is the largest value at which Dusk reaches its best code-color separation, inside the range where Dawn meets every minimum (up to 0.0375; from 0.040 Faint comes within 1 JND of a semantic color in Dawn).

## 1.10.0

The bright step is searched on the twelve chromatic terminal colors.

### Changed
- Brights move 0.38 of the way toward Ink instead of one third. The step is the one, from 0.29 to 0.89, that keeps every bright 2 JND from its normal and from Ink and gives the twelve chromatic ANSI colors the largest closest pair in every vision (construction.md §6.7). It moves to the Resolved group of §12.
- ANSI 9 to 14 in both flavors.

### Improved (against 1.9.1)
- Closest pair of the twelve chromatic terminal colors, worst vision: Dusk 0.0124 → 0.0201, Dawn 0.0117 → 0.0195.
- Closest pair in normal vision: 0.048 → 0.055.
- Each bright from its normal: at least 2.39 → 2.73 JND.
- Lowest bright contrast on Canvas: 7.65 → 8.12:1.

### Costs
- Brights sit closer to Ink in Dusk (2.69 → 2.38 JND under color-vision deficiency) and closer to each other (0.0217 → 0.0195 in Dawn). Both losses are under 1 JND, and both values are new measurements, not floors.

### Added
- Category minimum: the closest pair of the twelve chromatic terminal colors, in every vision, at least ΔE 0.010.
- construction.md §11: the closest pair stays near 1 JND under color-vision deficiency.

### Tooling
- `construct.py`: `BRIGHT_STEP` and `bright_step()`, the search of §6.7. `validate.py` checks that the search still returns the published step, and the new minimum with its flavor floors.

## 1.9.1

Parameters checked against the guarantees. No value changes.

### Documented
- construction.md §12: a Resolved group for parameters whose value the guarantees select over a searched range. The surface ratio r and the warm tilt τ move there. τ = 0.15 is the only value from 0.10 to 0.20, in steps of 0.01, at which both flavors meet every minimum.
- construction.md §6.3: the gamut margin 0.92 is searched too. Dawn meets every minimum from 0.92 to 0.932; 0.93 would gain ΔE 0.0007 in color-vision separation and sit 0.005 from a value that breaks four minimums, so 0.92 stays.
- construction.md §11: Dawn's color-vision separation of the code colors (ΔE 0.0402) is the optimizer's maximum, and no parameter tested raises it without breaking another minimum.
- Auditor skill: the resolved class of parameters.

## 1.9.0

Semantic colors outside code, and a measured limit of Faint in light flavors. No value changes.

### Added
- Text in a semantic color uses that color's `accent-text`, which meets the code floor of its category on every surface. The color itself stays for icons, markers and bars. In Dawn, Grove, Gold and Sea Salt are 4.15, 4.32 and 4.39:1 on Raised, below AA for text.
- Category minimums: semantic colors at least 3:1 on every surface and on Edge; Faint at least 1 JND from every semantic color in every vision.
- Version-control markers carry a letter or an icon.

### Documented
- construction.md §11: in Dawn, Faint is 1.05 JND from Grove under color-vision deficiency. The three corrections measured (optimizer objective, a higher code floor, a darker Faint) and why each was rejected.
- design-system.md §13: a semantic color used directly for text is a misuse.

### Tooling
- `validate.py` and `docs.py`: the two new checks, their guarantee rows and facts.

## 1.8.1

Continuous validation. No value changes.

### Tooling
- `.github/workflows/validate.yml`: every pull request to `main` and every push to it runs the validator against the base, with full reproduction, and writes the report to the job summary. Pull requests that touch the construction also run `--robust`. Pull requests that edit the validator also run the base branch's copy on the change, without blocking, so a loosened check is visible.
- CONTRIBUTING: what the workflow checks, how to run it locally, and the merge methods.

## 1.8.0

Afterglow is the accent of every theme. No token is removed and no value changes.

### Changed
- A theme is named by its flavor alone, *Twilight Dusk* or *Twilight Dawn*, and uses Afterglow as its accent. The accent families of the other seven colors stay in palette/twilight.json, built and validated as before; no theme uses them, and their colors keep their roles as code, semantic and series colors.
- The cursor belongs to the flavor, like selection: it is Afterglow's `accent-focus`, the color the code colors are optimized against, whatever the accent.
- design-system.md §13 lists an accent family other than Afterglow as a misuse.

## 1.7.0

How to apply Twilight to any target, and how not to. No color changes.

### Added
- `series` in palette/twilight.json: the order of data series (Sky, Ember, Gold, Sea Salt, Orchid, Grove) and the neutral for any series past the sixth (Control). The order is searched on Dusk and Dawn and shared by every flavor (construction.md §7.1).
- design-system.md §12, Applying the system: regions by function, nesting and elevation, states of neutral rows and controls, data visualization, and limited targets (fewer surfaces or text levels, one accent color, sixteen terminal colors).
- design-system.md §13, How not to apply: each misuse, what it breaks, and what to use instead.
- Category minimums: Subtle on an Edge fill 4.5:1; the chip label on `accent-text` 4.5:1; Other at least ΔE 0.040 from every series in every vision; the closest pair of neutral row and control states at least 1 JND.

### Changed
- A selected row is no longer Raised. Raised is the hover fill on Rail and Canvas; a selected row takes `selection-inactive` or `selection`. On Shell and Raised, which are less than 1 JND apart in light flavors, hover takes `selection-inactive`.
- The guarantee table moves from §13 to §14 of design-system.md.

### Tooling
- `validate.py`: the four new checks with their flavor floors; the published series must equal the decided order, and the search of §7.1 must still return it. Guarantee rows are matched with specific labels first, and a section heading without a flavor name ends the previous flavor's tables.
- `docs.py`: generates the series table, the new guarantee rows and the facts of §12.

## 1.6.2

Tooling to keep documents and images generated from the palette. No value changes.

### Tooling
- `scripts/docs.py` regenerates every table, measured number and swatch strip in README.md and design-system.md, and redraws both palette images, from palette/twilight.json. Numbers that appear in prose sit between `<!-- fact:NAME -->` markers. `--check` reports any difference and exits 1.
- `validate.py`: the consistency step runs the generator in check mode, so a document or image that drifts from the palette fails. Images are checked by sampling each swatch and circle against the JSON.
- `validate.py --robust`: rebuilds every flavor with 20 optimizer restarts instead of 10 and fails if any token changes, so a shipped solution cannot sit on an optimum that more search would leave.
- `validate.py` reads the flavor columns of the construction.md hue table from its header, so a new flavor needs no change to the check.
- Pillow 11.3.0 pinned in requirements.txt.

### Documented
- README guarantees and design-system.md §4 minimums are rounded to two decimals from the measured values; both images redrawn by the generator.

## 1.6.1

Documentation brought up to date with 1.6. No value changes.

### Fixed
- design-system.md §3: surface separation is 1.04 to 1.28:1 in Dusk and 1.04 to 1.21:1 in Dawn (it still read 1.13 and 1.17).
- design-system.md §4: the Ink minimum is 12.8:1 (it still read 13.4).
- design-system.md §6: Afterglow is computed from the seed; it is not the seed.
- design-system.md §10 and construction.md §11: of ANSI black and white, the slot that matches the background is Edge; the other is a text level. Both used to be described as 1.4:1 surfaces.

### Documented
- design-system.md: rules that differ between dark and light themes name the category, not the flavor (principle 6, §2, §5 `accent-text`, §8 chip labels, §10 brights, rule 13 shadows, §12 checklist), so every flavor of a category follows them.

## 1.6.0

Quality floors in two levels: category minimums, the Twilight standard every dark or light flavor meets, and flavor floors, what Dusk and Dawn reach today. No value changes.

### Added
- Category minimums for dark and light themes (construction.md §10.1): code 7:1 or 4.5:1; Body, Subtle, Faint and Control at the §3.5 targets; Ink at least the Body target and above Body; focus 3, on-accent 4.5, accent-text 7 or 4.5; code-color ΔE at least 4 JND in normal vision and 2 JND under color-vision deficiency; every background state at least 2 JND from Canvas and every pair at least 1 JND apart.
- Rule for lowering a flavor floor: it still meets its category minimum, the changelog names it under Lower with its cause and benefit, and the loss is imperceptible or well inside the standard.
- A new flavor is checked against its category's minimums; its measured values become its floors.

### Tooling
- `validate.py`: `MINIMUMS` per category and `FLOORS` per flavor replace the (Dusk, Dawn) table and the fixed/measured split. Every value is reported next to its flavor floor and its category minimum. `--compare` rejects a lowered category minimum, a flavor floor lowered without its Lower entry, and a flavor floor below its minimum; a flavor with no floors is reported. Base snapshots with the earlier table format are read per flavor.
- New checks: every background state ≥ 2 JND from Canvas, the closest pair of states ≥ 1 JND, and Ink above Body on every surface.

### Documented
- construction.md §10.1; design-system.md §13; CONTRIBUTING; auditor skill area C, D and the verdict rules.

## 1.5.0

The surface ratio r goes from 1.25 to 1.3125 (21/16): the smallest value at which both flavors keep every guarantee, every pair of background states is at least 1 JND apart, and Dusk's write highlight reaches its target. Code colors and Afterglow are unchanged.

### Changed
- System: r = 1.3125 at L_ref = 0.20. Surface distances from Canvas: Shell 2.41, Raised 3.16, Edge 7.22 JND (were 1.98, 2.51, 5.68).
- Dusk and Dawn: Shell, Rail, Raised and Edge, the text levels solved against Raised, `accent-text` where it is solved against Raised, `on-accent` (the new Shell in Dusk), Dawn's Afterglow `accent-focus`, and the states that follow. Canvas and Ink are unchanged.

### Improved (against 1.4.1)
- Dusk `word-highlight-write` 2.50 → 3.05 JND (target reached); `find-match` 3.61 → 4.06 JND; ANSI black and white on Canvas 1.39 → 1.57:1; Shell and Rail 1.10 → 1.35 JND apart.
- Dawn `selection` 2.79 → 3.45 JND; `find-match` 4.31 → 4.74 JND; ANSI black and white 1.43 → 1.58:1; selection and inactive selection 0.96 → 1.68 JND apart. Every pair of states in both flavors is now at least 1 JND apart.

### Lower (against 1.4.1)
- `ink on surfaces`: Dusk 13.76 → 13.25:1, Dawn 13.36 → 12.84:1. Ink is the same color; Raised sits further from Canvas. Ink on Canvas stays 15.58:1.
- Dusk control on every surface 3.03 → 3.00:1 and Afterglow focus 6.22 → 5.99:1; both still meet their thresholds.

### Documented
- construction.md §3.3 (r and the sweep that set it), §3.4, §3.5, §5, §9.2, §9.4, §11 (the Dawn state pair under 1 JND is gone) and §12.
- design-system.md and README: regenerated neutral, accent, state and terminal tables; guarantees; surface lightnesses.
- `assets/palette-*.png` repainted with the new neutrals.

### Tooling
- `validate.py`: Ink floors 13.25 (Dusk) and 12.84 (Dawn); `LIMIT_FLOORS` current as of 1.5.0.

## 1.4.1

The method is organized in three levels: system, category and flavor. Dawn no longer reads Dusk. No value changes.

### Tooling
- `construct.py`: system constants, `CATEGORIES` (dark, light) and `FLAVORS` (Dusk, Dawn). One neutral builder places every flavor's surfaces at the system distances from its own Canvas, in its category's direction, and solves its text levels and Rail. Dawn's anchors are its own parameters, and its surface distances come from the system, not from Dusk's neutrals.
- The surface ratio is a system parameter: r = 1.25 at L_ref = 0.20, as ΔE distances (1.98, 2.51, 5.68 JND).
- The neutral chroma amplitude is a flavor parameter (0.035 in both).
- Both flavors rebuild exactly. Changing Dusk's Canvas, Ink or amplitude no longer moves any Dawn token.

### Documented
- construction.md §1.1 (the three levels), §3.3 (surface distances), §4 (Dawn's own anchors), §12 and §13.
- Auditor skill: the construction's levels; a new flavor is an entry in `FLAVORS` within an existing category.

## 1.4.0

The construction now builds what the validator guarantees: the cursor is part of the hue optimization, and background states keep 1 JND from each other. Code colors are unchanged in both flavors.

### Changed
- §6.5: the optimizer compares every code color with the cursor (Afterglow's `accent-focus`), Coral excluded, the same pairs as the color-vision guarantee. Published hues are unchanged; Dawn's first pass moves, so Dawn `diff-removed` is now `#f4dde0`.
- §9.4: states are built in a fixed order, each kept at least 1 JND from the states before it whenever a color that reaches its target allows it. Dusk `selection-inactive` is now `#260f02` and Dusk `word-highlight-write` `#182423`.

### Improved (against 1.3.0)
- Dusk: the two word highlights 0.80 → 1.23 JND apart; inactive selection and removed diff 0.54 → 1.08 JND; closest pair of states ΔE 0.011 → 0.022.
- Dusk `selection-inactive` 2.1 → 2.9 JND.
- Dawn: inactive selection and removed diff 0.61 → 1.01 JND; closest pair of states ΔE 0.012 → 0.019; `diff-removed` 2.02 → 2.06 JND.
- Pairs of states under 1 JND: four → one (Dawn selection and inactive selection, 0.96 JND).

### Lower (against 1.3.0)
- `JND word-highlight-write`: Dusk 2.689 → 2.501 (target 3 was not reached before either). The color keeps its lightness at half the chroma, 0.88 JND from the old one, and is now distinguishable from `word-highlight`.
- Dawn code colors on every code surface 4.54 → 4.52:1, from the new removed-diff background; still meets 4.5:1.

### Documented
- construction.md §6.5 (cursor in the objective), §9.4 (separation between states), §11 (one state pair under 1 JND), §12 and §13.
- design-system.md §9: states stay 1 JND apart.

### Tooling
- `construct.py`: `optimize()` takes the cursor; `state()` takes the states already built and prefers a color 1 JND from them.
- `validate.py`: `LIMIT_FLOORS` current as of 1.4.0 (Dusk and Dawn closest state pair 0.0215 and 0.0191).
- Auditor skill: the floors table shows the Dusk ΔE floors raised in 1.3.0 (0.097, 0.061).
- `validate.py --compare`: the stale-image check looks only at neutrals and colors, the values `assets/palette-*.png` shows. A change to background states no longer requires new images.

## 1.3.0

Afterglow and the chroma base are computed from the seed. Dusk's code colors gain chroma; Dawn changes only in Afterglow.

### Changed
- Afterglow is the sRGB cusp of the seed hue: `#ff7d00` (L 0.727, C 0.188) instead of the seed itself. The seed `#ee7a1f` stays the origin of the system and is no longer a token. Both flavors share the new Afterglow and its accent family.
- The chroma base C₀ depends on polarity, like β: C_Afterglow / φ = 0.116 in dark flavors, C_seed / φ = 0.105 in light ones (construction.md §6.3). Dawn's code colors are unchanged.
- Dusk: every code color, its accent family and its bright, plus `word-highlight`, `word-highlight-write` and `diff-inserted`, follow from the new base. Dusk's neutrals are unchanged.
- The selection hue is Afterglow's hue (51.7°). Both selection states keep their values.

### Improved (against 1.2.0)
- Dusk smallest code-color difference, normal vision: ΔE 0.089 → 0.097.
- Dusk smallest code-color difference, color-vision deficiency: ΔE 0.054 → 0.061.
- Dusk `word-highlight-write` 2.6 → 2.7 JND. Dusk Afterglow focus 5.65 → 6.22:1; on-accent on Afterglow 6.86 → 7.55:1.
- Dawn: label on pressed Afterglow 4.51 → 4.85:1.

### Lower (against 1.2.0)
- `JND word-highlight`: Dusk 2.015 → 2.013 (target 2, still met).
- `JND diff-inserted`: Dusk 2.043 → 2.021 (target 2, still met).
- Dusk code colors on every code surface 7.04 → 7.00:1 and `accent-text` on Raised 7.01 → 7.00:1; both still meet 7:1.
- Dawn Afterglow focus 3.02 → 3.01:1; still meets 3:1.

### Documented
- construction.md §2 (seed and Afterglow), §4 (chroma base per flavor), §6.3 (why light flavors take the seed's chroma), §6.5 hue table, §7, §11 and §12.
- design-system.md and README: one seed instead of two, and the regenerated Dusk values.

### Tooling
- `construct.py`: `AFTERGLOW` is computed from the seed hue; each profile names its `chroma_base`.
- `validate.py`: Afterglow must equal the cusp of the seed hue. Dusk floors follow the rebuilt flavor (normal-vision ΔE 0.097, color-vision ΔE 0.061) and `LIMIT_FLOORS` are current as of 1.3.0. The seed hex may appear in the documents.

## 1.2.0

Dawn rebuilt as the light end of the same system. Dusk is unchanged, value for value.

### Changed
- Dawn: every value. Canvas and Ink swap Dusk's two anchors (Canvas `#eeeeef`, Ink `#11171b`), so the lightest value in Twilight is L 0.95 instead of 0.975.
- Dawn surfaces keep Dusk's perceptual distance from Canvas (ΔE OKLab) instead of its contrast ratios. Every Dawn neutral sits on the shared neutral curve, with no relative-chroma correction.
- Dawn uses β = 0.19, the slope measured on light themes; Dusk keeps 0.30, measured on dark themes (construction.md §6.2).
- Background states: away from the text, a state stops at the outermost surface (Shell in Dusk, Canvas in Dawn). Dusk is unaffected.

### Improved (Dawn, against 1.1.1)
- `selection` 2.2 → 2.8 JND; `find-match` 3.0 → 4.3 JND; `word-highlight-write` 2.3 → 3.0 JND (target reached).
- Selection vs inactive selection 0.22 → 0.96 JND; closest pair of background states 0.22 → 0.61 JND.
- Smallest code-color difference, normal vision: ΔE 0.077 → 0.088.

### Lower (Dawn, against 1.1.1)
- `ink on surfaces`: 14.81 → 13.36:1, from the darker Canvas. Ink on Canvas is 15.58:1 in both flavors.
- `ΔE code+cursor, worst CVD`: 0.041 → 0.040 (0.0411 → 0.0402, about 0.05 JND).
- `JND diff-removed`: 2.025 → 2.021 (target 2, still met).
- Control on any surface 3.02 → 3.00:1 and `accent-text` on Raised 4.51 → 4.50:1; both still meet their WCAG thresholds.

### Documented
- construction.md §4 rewritten (Dawn: the light end), Dawn β in §6.2, updated limits in §11.
- The syntax-role assignment is a decided parameter (construction.md §12). β is documented as measured on dark and light themes. No other theme is named in the documents.
- Versioning: values regenerated by the documented method are a minor release; removing or renaming a token is a major one (CONTRIBUTING.md, auditor skill).

### Tooling
- `construct.py` splits the shared core from two flavor profiles (anchors, floor, β, search ranges) and rebuilds both flavors exactly.
- The ±25° hue bound is enforced by the optimizer on the rendered hue against the exact anchor, the same way the validator checks it. Dusk is unaffected.
- `validate.py`: Dawn floors follow the rebuilt flavor. Ink 13.36, color-vision ΔE 0.040, normal-vision ΔE 0.088 (construction.md §4).
- `validate.py --compare`: WCAG thresholds and text targets are fixed guarantees and never go down. Ink, the two ΔE floors and the known limits (`LIMIT_FLOORS`) are measured minimums and go down only when the version's entry names each one, in backticks, under `### Lower`. Removing a check is a regression.

## 1.1.1

### Fixed
- docs: five background-state JND values did not match the published colors (2.1 → 2.0, 3.1 → 3.0).
- docs: Sea Salt Dusk hue in §6.5 is the optimizer's 197°, not the measured 196°.

### Documented
- construction.md now specifies the optimizer (seed, restarts, schedule, score), the two-pass
  code-surface procedure, the background-state cost function, search ranges and precision
  conventions. The palette is unchanged.

### Added
- `twilight-auditor` skill: reference implementation of the construction method and the audit checks (floors, reproduction, document consistency).

## 1.1.0

One rule added before the first ports. No values changed.

- Links in running text carry a non-color cue (underline or icon). No `accent-text` reaches 3:1 against Body, so color alone fails WCAG 2.2 SC 1.4.1.

## 1.0.0

First public definition.

- Two flavors: Dusk (dark) and Dawn (light).
- Ten neutrals: Shell, Rail, Canvas, Raised, Edge, Control, Faint, Subtle, Body, Ink.
- Eight colors: Afterglow, Coral, Gold, Grove, Sea Salt, Sky, Orchid, Ember.
- Interchangeable accents: any of the eight colors, each with text, pressed, focus and label tokens.
- Syntax roles, semantic states, background states and the sixteen terminal colors.
- Design system and construction documents.
- All values in `palette/twilight.json`.
