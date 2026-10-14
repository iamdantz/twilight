# Changelog

## 1.1.1

### Fixed
- docs: five background-state JND values did not match the published colors (2.1 → 2.0, 3.1 → 3.0).
- docs: Sea Salt Dusk hue in §6.5 is the optimizer's 197°, not the measured 196°.

### Documented
- construction.md now specifies the optimizer (seed, restarts, schedule, score), the two-pass
  code-surface procedure, the background-state cost function, search ranges and precision
  conventions. The palette is unchanged.

### Added
- scripts/construct.py (reference implementation) and scripts/validate.py (auditor checks) as Twilight Auditor Skill.

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
