# Changelog

## 2.0.0

Dawn rebuilt as the light end of the same system. Dusk is unchanged, value for value.

### Changed
- Dawn: every value. Canvas and Ink now swap Dusk's two anchors (Canvas `#eeeeef`, Ink `#11171b`), so the lightest value in Twilight is L 0.95 instead of 0.975.
- Dawn surfaces keep Dusk's perceptual distance from Canvas (ΔE OKLab) instead of its contrast ratios, and all Dawn neutrals sit on the shared neutral curve with no relative-chroma correction.
- Dawn β is 0.19: the mean slope of the three light themes (of eight with terminal colors) whose correlation reaches 0.6, with the same regression that gave Dusk's 0.30 (construction.md §6.2).
- Background states: away from the text, a state stops at the outermost surface (Shell in Dusk, Canvas in Dawn). Dusk is unaffected.

### Improved (Dawn, against 1.1.1)
- `selection` 2.2 → 2.8 JND; `find-match` 3.0 → 4.3 JND; `word-highlight-write` 2.3 → 3.0 JND (target reached).
- Selection vs inactive selection 0.22 → 0.96 JND; closest pair of background states 0.22 → 0.61 JND.
- Smallest code-color difference, normal vision: ΔE 0.077 → 0.088.

### Lower (Dawn, against 1.1.1)
- Ink on any surface: 14.81 → 13.36:1, from the darker Canvas. Ink on Canvas is now 15.58:1 in both flavors.
- Worst color-vision separation of the code colors: ΔE 0.041 → 0.040 (0.0411 → 0.0402, about 0.05 JND).
- `diff-removed` visibility 2.025 → 2.021 JND (target 2, still met).
- Control on any surface 3.02 → 3.00:1 and `accent-text` on Raised 4.51 → 4.50:1; both still meet their WCAG thresholds.

### Documented
- construction.md §4 rewritten (Dawn: the light end), Dawn β in §6.2, light conventions in §8.2, updated limits in §11.
- Syntax roles and names are shared by both flavors; ten light themes agree with every role that has a majority.

### Tooling
- `construct.py` separates the shared core from the flavor profiles and rebuilds both flavors exactly. Each profile carries its own seed (both use Afterglow); the neutral hue, warm tilt and Ember range follow it.
- The ±25° hue bound is now enforced by the optimizer on the rendered hue against the exact anchor, the same way the validator checks it. Dusk is unaffected.
- `validate.py`: the Dawn normal-vision floor rises to ΔE 0.088. The Ink (14.81) and color-vision (0.041) floors are unchanged, so this release fails them until they are explicitly reset (see Lower).

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
