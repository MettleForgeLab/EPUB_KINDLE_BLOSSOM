# Implementation boundaries — 0.1

## A runnable vertical slice, not the finished adapter

This release can inspect the actual BHT master, execute four profile routes, produce two plates and an isolated EPUB, and verify the result. It does not implement all fifteen stages of Tool Specification 001 for arbitrary books.

The rule scanner identifies matching CSS and technical risk signals. The profile supplies the treatment and the reason. The program does not pretend to infer aesthetic meaning or Porter approval.

## Deliberate choices

### Profile-bound source selection
Every figure and included source-copy root has a canonical SHA-256. A source mismatch stops the run rather than attempting a near-match. No filename-only parent selection occurs.

### True source view, followed by a declared derivative view
Canonical reference images are rendered before an explicit CSS layer increases labels. The layer is stored and hashed beside the profile. It does not change source DOM text. It may change dimensions and typography; these are candidate adaptation changes, not claims of pixel-identical design.

### One crop per visual component
The crop encloses the component's designed field. It omits the live caption and surrounding page. Internal pale or empty areas are not automatically discarded: some negative space is part of the relation.

### Display width follows legibility, not a fixed percentage class
The census's medium-width suggestion is provisional. Field's small source labels would be too small if mechanically reduced to 74% of a narrow column. This profile uses full available width on small displays and a 28em maximum on larger ones. The compass uses a 31em maximum.

Minimum effective label size is measured as:
```
source-render font size × available displayed plate width / source-render box width
```
Changing only source pixels cannot improve this quantity. The provisional floor is 11 CSS px at 320px viewport / 12px side padding. It is a local warning/stop threshold, not a readability guarantee.

### Conservative optimization
Both final plates remain lossless RGB. Palette candidates are saved for human comparison. Even small per-pixel changes are not automatically accepted. The tool records palette savings, maximum error and average error; those metrics do not substitute for checking fine lines and glyph edges.

Byte budgets are reported per profile. This version does not silently reduce quality to hit them.

### Explicit excerpt harness
The probe has four figures, two complete source-copy excerpts, six reading resources and a separate navigation resource. It intentionally excludes the rest of BHT. It uses its own test title/identifier, not the book ISBN, and is marked as a probe.

It does not demonstrate complete-ending preservation, full-book source integrity after conversion, or the resolution of blank pages before major entries.

### Caption and alternative description
The four original captions remain canonically identical. Plate captions move after their images as normal-flow live text. Each plate has short alt and a visible link to new editorial description text, with a return link. That wording remains pending Porter approval. No hidden duplicate prose is used.

### Crossing
The same three label groups become an ordered list. The original closing apparatus sentence stays live. Original source text is copied without rewriting. The original diagram was aria-hidden; the replacement becomes exposed live text. This is an accessibility/structure change, not a source-standing change.

### Fonts and reproducibility
The tool records browser/runtime and source hashes, but system fonts may differ across Windows and Linux. Rebuilds can have different raster bytes. There is no implied cross-platform visual identity; compare run records and references before accepting a new run.

## Hard stops
Wrong EPUB hash; wrong packaged reading hash; stale figure/source hashes; changed profile CSS; existing output folder; unsafe ZIP path/symlink; duplicate IDs; broken local resources/fragments; broken accessibility IDREFs; label clipping; failed directional relation assertions; failed effective label-size floor; altered included source or captions.

## Deferred
Arbitrary EPUB profiles, learned classification, full-book reconstruction, 69-figure batch processing, richer live-component templates, physical e-ink QA, Kindle conversion automation, clean final metadata/cover work, source-license/repository installation and delivery-fee calculations.

## Release boundary
Local Chromium is not Kindle. A structurally correct EPUB and a legible local screenshot cannot grant a Kindle visual pass. Porter acceptance remains open.


## 0.2 additions

### Vertical-footprint budget is not pagination authority

The adapter may estimate whether an image + live caption + description link fits inside a configured reference-height budget. It may add keep-together CSS only when that local budget passes.

This is a local engineering decision. Kindle Previewer and human review remain authoritative for actual pagination.

### Visual overflow is opt-in

A plate root that visibly overflows its box remains an error unless the profile explicitly enables bounded visual overflow. The renderer then expands only to measured visible descendants/text, within a fixed safety limit.

This supports accepted compositions such as a label intentionally sitting just outside a judgment field without turning the renderer into a viewport screenshot tool.

### Live simplification is profile-driven

`SIMPLIFY LIVE` may now transform a declared set of existing visual children into an ordered live relation, but only when:
- item selection is explicit;
- expected wording/order is recorded;
- source prose remains untouched;
- the live caption remains unchanged.

### SVG-local IDs

IDs internal to bounded SVG geometry may be permitted only when the profile explicitly opts in. Source/editorial identities, ordinary HTML IDs, and links remain prohibited inside a plate visual target.
