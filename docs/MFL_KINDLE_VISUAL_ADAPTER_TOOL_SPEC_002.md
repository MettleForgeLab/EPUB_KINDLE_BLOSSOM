# MFL Kindle Visual Adapter — Tool Specification 002

This document supersedes the implementation portions of Tool Specification 001 while preserving its governing idea:

> If the reader engine moves these pieces independently, does the proposition change?

## 0.2 engineering additions

### 1. Vertical-footprint budget

Plate planning must consider the entire live reading unit:

`plate + live caption + visible description link + breathing room`

A profile provides:
- reference viewport width and height;
- page padding;
- maximum bundle-height fraction;
- caption reserve;
- description-link reserve;
- breathing reserve;
- minimum component display width.

The renderer:
1. computes the image aspect ratio from the selected plate;
2. computes requested display width;
3. reduces that width only if necessary to keep the estimated bundle within the configured vertical budget;
4. refuses the build if the required reduction violates the component's minimum display width;
5. recomputes effective displayed label size at the planned width;
6. refuses the build if label size falls below the configured engineering floor.

The assembled probe then remeasures the actual plate/caption/link bundle at the reference viewport.

Only budget-safe bundles may receive derivative-only keep-together CSS.

This is an engineering constraint, not a promise about Kindle pagination. Kindle Previewer and human review remain authoritative.

### 2. Plate scale is semantic

A high-resolution image must not automatically fill the reading column.

Profiles declare an intended width class:
- small apparatus;
- medium apparatus;
- field apparatus;
- opening apparatus.

The vertical budget may reduce a requested width; it may not enlarge it beyond the profile's intended visual hierarchy.

### 3. Explicit bounded overflow capture

Some accepted diagrams intentionally place labels outside the root visual box.

Default behavior remains: visible overflow is a build error.

A profile may explicitly allow bounded visual overflow. When enabled:
- the renderer expands the capture box only to measured visible descendants/text;
- overflow is subject to a safety bound;
- the live caption remains outside the plate;
- viewport screenshots are still forbidden.

### 4. Profile-driven live simplification

`SIMPLIFY LIVE` supports declared item extraction and expected wording/order.

The profile records:
- source visual;
- item XPath;
- expected sequence;
- container semantics;
- accessible label.

The adapter refuses the transform if the source wording/order differs.

### 5. SVG-local IDs

A plate visual may explicitly permit IDs used only inside bounded SVG geometry.

Ordinary HTML IDs, links, source identities, and editorial identities remain disallowed inside an image-routed visual target.

## Second component batch

Milestone 002 adds:

1. Jules Gravity — MEDIUM PLATE
2. Jules Motion — SMALL PLATE
3. East Promise attachment stack — SIMPLIFY LIVE
4. South Judgment Latch — MEDIUM PLATE

The batch is designed to test:
- restrained apparatus scale;
- plate/caption adjacency;
- one small path diagram;
- one overflow-bearing field;
- generalized live simplification.

## Promotion gate

The footprint mechanism may become a reusable production component only after Kindle Previewer confirms that:
- budget-safe bundles do not create blank pages;
- captions and description links stay acceptably adjacent;
- small plates remain visually secondary;
- enlarged text does not break live simplifications;
- no plate becomes unreadable at its planned width.

## Still outside scope

- full-book automatic conversion;
- autonomous aesthetic classification;
- KDP upload;
- retailer-fee calculation;
- rights decisions;
- automatic authorial acceptance;
- current-book blank-page diagnosis;
- physical-device acceptance.
