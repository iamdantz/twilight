# Changelog

## 1.2.0 (preview)

- Nightfall: a third flavor, dark. Dusk's construction re-run with four decided parameters fitted from a thesis conversion of Dusk: seed `#f9a36b`, neutral chroma 0.018, hue drift 8°, surface ratio 1.26. No rule changed.
- `tools/`: a construction engine that rebuilds Dusk from its parameters.

## 1.1.0

One rule added before the first ports. No values changed.

- Links in running text carry a non-color cue (underline or icon). No `accent-text` reaches 3:1 against Body, so color alone fails WCAG 2.2 SC 1.4.1.

## 1.0.1

- Tighter wording in the README, design system and construction documents. No values or rules changed.

## 1.0.0

First public definition.

- Two flavors: Dusk (dark) and Dawn (light).
- Ten neutrals: Shell, Rail, Canvas, Raised, Edge, Control, Faint, Subtle, Body, Ink.
- Eight colors: Afterglow, Coral, Gold, Grove, Sea Salt, Sky, Orchid, Ember.
- Interchangeable accents: any of the eight colors, each with text, pressed, focus and label tokens.
- Syntax roles, semantic states, background states and the sixteen terminal colors.
- Design system and construction documents.
- All values in `palette/twilight.json`.
