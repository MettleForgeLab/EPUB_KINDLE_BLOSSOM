# MFL Kindle Visual Adapter — Tool Specification 001

**Working title:** MFL Kindle Visual Adapter  
**Origin problem:** preserve designed EPUB relationships through constrained Kindle reflow  
**Initial training/validation book:** *Now You Can Do Big Hard Things*  
**BHT figure census:** 69 figures · 38 plate candidates · 31 live treatments

## Purpose

The tool should translate a visually expressive standards-oriented EPUB into a constrained-channel derivative **without forcing the source book to dumb itself down**.

The source EPUB remains presentation authority. The tool produces a derivative and a transformation record.

The core idea is:

> **Infer what must remain live, what may become one-dimensional, and what must become atomic because position itself carries meaning.**

This is not an EPUB-to-image converter.

It is a **relationship-preserving compositor**.

## Product boundary

The tool may:

- inspect XHTML/CSS/figures/navigation;
- classify visual components;
- simplify selected live apparatus;
- split reading resources;
- render/crop/optimize atomic plates;
- rewrite internal navigation in the derivative;
- preserve or create accessibility descriptions;
- remove dead derivative-only helper geometry;
- generate manifests/diffs/hashes;
- build QA artifacts.

The tool must not:

- alter the governing source EPUB in place;
- silently change reader-facing prose;
- collapse source/editorial/provenance standing;
- rasterize source text merely for convenience;
- infer legal/rights standing;
- publish/upload to KDP;
- use a failed derivative as presentation authority.

## Inputs

Minimum:

1. governing EPUB + expected SHA-256;
2. adaptation profile (`kindle-reflowable` initially).

Useful optional inputs:

- accepted screenshots/reference renders;
- known reader failure screenshots/logs;
- component acceptance ledger;
- source-lock manifest;
- accessibility descriptions;
- prior derivative for diagnostic comparison only.

## Output set

1. derivative EPUB;
2. component census JSON;
3. transformation manifest;
4. exact changed-member report;
5. generated plates + checksums;
6. accessibility/description map;
7. link/ID validation;
8. byte-budget report;
9. local reference screenshots;
10. retailer-test checklist.

## Pipeline

### Stage 1 — custody

- verify governing EPUB hash;
- reopen ZIP and verify `mimetype`;
- locate OPF/nav/spine;
- hash every package member;
- parse XHTML strictly;
- record reading order.

### Stage 2 — semantic inventory

Build a graph of:

- top-level entries;
- headings;
- source-bearing regions;
- editorial apparatus;
- figures/captions;
- navigation;
- IDs/fragments;
- derived instruments;
- images/SVGs;
- standing/accessibility attributes.

### Stage 3 — visual dependency analysis

For each component, collect risk signals:

**Strong plate signals**
- absolute positioning;
- overlapping layers;
- CSS Grid used as semantic geometry;
- center/periphery relation;
- cardinal placement;
- arcs/paths/endpoints;
- labels positioned relative to shapes;
- gradients/blooms/soft fields;
- meaningful enclosure;
- meaningful negative space;
- pseudo-elements carrying visible semantic marks.

**Strong live signals**
- sequence;
- ledger/register;
- list;
- simple before/after;
- categorical opposition;
- ordinary prose;
- ordinary table;
- navigation whose meaning is question→destination rather than 2D position.

### Stage 4 — treatment classifier

Allowed decisions:

- `LIVE`
- `SIMPLIFY LIVE`
- `SMALL PLATE`
- `MEDIUM PLATE`
- `FIELD PLATE`
- `OPENING PLATE`

The classifier should output both a recommendation and a reason.

**Human review remains authoritative.**

### Stage 5 — live simplifier

Convert fragile live geometry into conservative semantic structure:

- Grid navigation → one-column links;
- multi-column ledgers → vertical rows;
- simple comparative diagrams → live rows/cards;
- remove desktop `min-height` and viewport simulation;
- neutralize derivative-only background wrappers that fragment badly.

No source prose rewrite.

### Stage 6 — canonical plate renderer

For every plate candidate:

1. render the exact governing component in a browser at canonical CSS;
2. isolate its component selector;
3. preserve intended background/field;
4. compute true content bounding box;
5. add only intentional plate padding;
6. render at target plate width;
7. flatten transparency unless explicitly approved;
8. save sRGB PNG.

Never capture a full browser viewport.

### Stage 7 — optimizer

Choose profile by component:

**Sparse line/type**
- attempt indexed/palette PNG;
- preserve text edges;
- compare pixel/structural fidelity;
- reject quantization that damages thin rules or labels.

**Gradient/bloom/dark field**
- retain RGB/sRGB;
- optimize losslessly first;
- run grayscale simulation;
- check banding and contrast.

Record:
- dimensions;
- bit depth/palette state;
- bytes before/after optimization;
- SHA-256.

### Stage 8 — scale policy

Do not use `width:100%` for every plate.

Assign visual class:

- small: 45–60%;
- medium: 65–78%;
- field: 88–100%;
- opening: 100%.

This prevents secondary doodles from becoming page-sized monuments.

### Stage 9 — accessibility

Preserve or create:

- live `figure`;
- live `figcaption`;
- concise relational `alt`;
- visible extended description for complex plates;
- return link from extended description.

Never use hidden duplicate prose simply to satisfy accessibility.

### Stage 10 — Kindle package architecture

Current BHT-derived default:

- one semantic top-level entry per XHTML spine resource;
- document-level main TOC destinations;
- cross-entry fragments retained where appropriate;
- one reset stylesheet + component stylesheet;
- no explicit page breaks at spine boundaries unless proven necessary;
- long prose returns to neutral reader field;
- colored fields are short live blocks or plates.

The tool should keep these as a profile, not universal EPUB law.

### Stage 11 — source-lock verification

If source-lock information is available:

- canonicalize every locked region before/after;
- verify text, IDs, order, standing and source metadata;
- fail build on drift.

### Stage 12 — navigation verification

- all TOC resources exist;
- all fragment targets resolve;
- all in-book relational links resolve;
- no duplicate IDs;
- no links into removed helper geometry.

### Stage 13 — plate budget gate

Before integration, report:

- plate count;
- actual plate bytes;
- existing image bytes;
- cumulative projected package bytes;
- largest plates;
- optimization outliers.

Allow a project policy such as:

> reject any sparse line plate above 250 KB until reviewed.

### Stage 14 — visual QA

Produce controlled renders at:

- narrow portrait;
- standard portrait;
- enlarged text for live components;
- grayscale simulation;
- optional inversion simulation.

For plates:
- verify aspect ratio;
- verify label legibility;
- verify no clipping;
- verify intended display class.

For live components:
- verify no horizontal crush;
- verify normal pagination.

### Stage 15 — retailer QA handoff

Generate a checklist of exact locations to inspect in Kindle Previewer/physical device.

The tool must distinguish:

- local render passed;
- Kindle conversion passed;
- human Kindle visual acceptance passed.

## BHT as initial classifier training set

BHT currently routes:

- 3 `LIVE`
- 28 `SIMPLIFY LIVE`
- 4 `SMALL PLATE`
- 24 `MEDIUM PLATE`
- 5 `FIELD PLATE`
- 5 `OPENING PLATE`

Plate candidates: **38 / 69**

Most plate candidates are not expensive photographic compositions:

- sparse line/type: 28
- dark fields: 4
- structured fields: 3
- gradients/blooms: 2
- dense compass: 1

That distribution is important for the general tool: **beauty need not imply a photographic file-weight budget**.

## General decision heuristic

The adapter should ask one question before all others:

> If the reader engine moves these pieces independently, does the proposition change?

**No** → keep/simplify live.

**Yes** → render the relationship atomically.

That heuristic generalizes beyond BHT.

Examples:

- cookbook plating diagram: plate;
- ingredients list: live;
- historical timeline: often live/simplified;
- map: plate;
- callout ledger: live;
- conceptual node field: plate;
- exercise worksheet: usually live;
- art-directed chapter opener: hybrid live framing + plate.

## Why this tool matters

Kindle’s constraints should not force the governing EPUB—or the book design itself—to become the lowest common denominator.

A useful adapter lets publishers maintain:

1. a richer standards-oriented EPUB;
2. a Kindle-specific derivative built from the same authority;
3. explicit transformation records showing how each relationship was preserved.

That creates room for better books instead of designing every ebook around the narrowest renderer.

## Next engineering milestone

Do **not** begin by automating all 69 BHT figures.

Build the tool around four representative components:

1. five-place compass — dense field plate;
2. Jules Field relation map — medium line plate;
3. Jules Crossing — simplify-live component;
4. White Room panel — existing-image live component.

The milestone passes when the tool can:

- classify all four correctly;
- render/crop/optimize the two plates;
- preserve the two live components;
- emit an exact transformation manifest;
- rebuild a bounded EPUB;
- verify IDs/links/captions/source locks;
- report actual plate byte cost.

Then scale to the full BHT census.
