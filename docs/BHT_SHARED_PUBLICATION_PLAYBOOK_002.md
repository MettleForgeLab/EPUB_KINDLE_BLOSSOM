# BHT Shared Publication / Build Playbook — 002

**Status:** Final evidence-backed operating architecture from frozen Apple and Kindle EPUB 1 releases
**Date:** 2026-10-07
**Lineage:** Supersedes Playbook 001 for future clean rebuilds. Preserve Playbook 001 as project lineage.
**Scope:** Common source/build method; graphic registry; validation/freeze protocol; Apple/non-Kindle appendix; Kindle appendix; known renderer-stability exceptions; repair-removal tests.

---

## 1. Purpose

BHT now has frozen release evidence from both publication branches.

The non-Kindle / Apple-targeted branch primarily exposed fragmentation, page geometry, reading-measure, containment, and live-graphic behavior.

The Kindle branch primarily exposed conversion, fragment-navigation, renderer reconstruction, repaint, and spatial-relationship failures.

The goal is not implementation identity.

The goal is one semantic book whose platform packages use the least forceful structure and representation that reliably preserves the relation the reader needs.

> The manuscript supplies the relation.
> The package chooses the least forceful structure that lets that relation survive the reader.

---

## 2. Authority map

Before transforming anything, name the role of every input.

### Semantic authority

The **canonical semantic source** owns:

- manuscript wording;
- reading order;
- semantic entry identities;
- source graphic identities;
- caption relationships;
- significant internal destinations.

No retailer EPUB, accepted candidate, rendered plate, or newer package replaces this authority merely because it worked.

### BHT authority chain established by the completed work

The last common pre-divergence book artifact is:

`BHT_RETAIL_RELEASE_CANDIDATE_002.epub`

- bytes: `5,124,743`
- SHA-256: `fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae`

It is the shared semantic/presentation ancestor used by both clean rebuilds. It is **not** a mandatory retailer-package skeleton.

The operational source for the four cardinal lenses later advanced under separate immutable custody:

- repository: `MettleForgeLab/bht-open-materials`
- immutable tag: `bht-epub-1-source-002`
- commit: `d14eab45bd47047487e9cfa76efc978071a2497b`
- licensed operational-source membership: `94 files`

The frozen Apple and Kindle releases both carry that accepted successor wording. Jules Bering remained unchanged.

This produces a deliberate authority order:

1. accepted semantic/operational source;
2. shared pre-divergence publication evidence;
3. platform recipe and admitted deviations;
4. frozen platform artifact;
5. retailer ingestion evidence.

### Presentation evidence

A successful platform candidate may prove:

- a pagination treatment worked;
- a graphic relation survived;
- a renderer-specific boundary worked;
- a cover/package behavior worked.

It remains evidence, not manuscript authority.

### Sibling-platform evidence

A sibling package may teach:

- where a relation is fragile;
- which structure is durable;
- which representation classes are legitimate fallbacks;
- which validation checks belong in the shared method.

It is never copied blindly across platforms.

### Playbook authority

This playbook governs **how to build and validate**, not what the manuscript says.

---

## 3. Default document architecture

For future clean builds:

> **one major semantic entry → one XHTML spine document by default**

The semantic entry remains canonical; the XHTML file is its deterministic package representation.

This default is now supported by both clean rebuilds because it improved source correspondence, direct TOC navigation, failure isolation, inspectability, and reproducibility without making the reading feel mechanically chaptered.

A platform may combine semantic entries only for a demonstrated reason.

A split that does not correspond to a major semantic entry is an exception and must carry provenance.

Examples already established:

- Kindle Jules `Presence → Startup & Settle` — **RENDERER-STABILITY**
- Kindle Western `Present Recognition → Human authority and family → Human` — **RENDERER-STABILITY**
- Apple/non-Kindle dedicated cover document — **PACKAGING**

---

## 4. Boundary provenance and removal tests

Every nontrivial package or flow boundary must have a reason class:

- **SEMANTIC**
- **COMPOSITIONAL**
- **RENDERER-STABILITY**
- **PACKAGING**
- **ACCESSIBILITY**
- **PLATFORM-POLICY**

A boundary record should contain:

- boundary ID;
- source location;
- reason class;
- observed failure or purpose;
- intervention;
- evidence that admitted it;
- **removal test**.

A workaround should never become permanent folklore.

Example:

**Kindle renderer split**
- reason: repaint/fragmentation reproduced without split;
- removal test: a future renderer version demonstrates stable forward/backward reading across the same boundary without the split.

**Apple Spot positioning repair**
- reason: bloom entered the gutter at two-page reading measure;
- removal test: replacement/live layout preserves the intended inset across target page measures without the repair.

---

## 5. Two escalation branches

Do not force flow and graphic failures into one ladder.

### Flow / pagination

**normal flow → responsive/local repair → local containment → explicit page boundary → renderer-proven spine boundary**

Before escalating, inspect:

- overflow;
- fixed/min heights;
- positioned ancestors;
- containment;
- page/column break suppression;
- keep-together rules;
- actual reading measure versus outer viewport width.

### Graphic / spatial relation

**live construction → responsive/local repair → simplified live construction → bounded plate**

A plate is legitimate when:

- the meaning is primarily spatial;
- the renderer preserves pieces but destroys relation;
- prose stays live;
- separable captions stay live;
- accessibility treatment is explicit;
- resolution is sufficient;
- representation identity is hash-locked;
- platform review/admission is separate from source identity.

Do not rasterize because splitting failed.
Do not split documents because an SVG misbehaves.

---

## 6. Shared CSS architecture

Prefer:

1. `shared.css` — common manuscript/composition rules;
2. platform CSS — narrow renderer/platform adaptations;
3. `cover.css` or equivalent package-only styling where needed.

Avoid:

- duplicated CSS inside every XHTML file;
- dispersed platform fixes in manuscript markup;
- hidden override chains.

Platform CSS should explain exceptions, not restate the book.

### Structural repair may retire cosmetic repair

Do not carry every successful historical CSS rule forever.

When structure becomes stronger, ask whether an old rule is still necessary.

Example: an end-of-entry page-break rule may be necessary in a monolithic file and obsolete once each major entry is already its own spine document.

Preserve **the relation the repair established**, not an obsolete mechanism.

---

## 7. Durable layout principles

### Reading measure is not viewport width

A wide application window may contain narrow reading pages.

Layouts should respond to the actual reading measure.

### Containment is a fragmentation decision

A semantically harmless wrapper can still prevent pagination.

Inspect containment and overflow before escalating.

### Major entries and internal movements differ

- major semantic entry → structural document unit by default;
- internal movement/subsection → preserve cohesion while allowing natural flow;
- renderer-unstable movement → escalate only after evidence.

### Blank space is evidence to interpret

Do not remove quiet space merely because pagination makes it measurable.

Blank space is a defect only when required content disappeared, reading order broke, unstable renderer flow created it, or content duplicated/disappeared around it.

### Strong structure can remain visually quiet

A package boundary does not need to announce itself as a visible chapter break.

---

## 8. Shared graphic registry

Every meaningful visual construction receives one durable `graphic_id`.

That identity answers:

> What relationship is this visual supposed to carry?

### Graphic identity

Record:

- `graphic_id`;
- semantic purpose / relation to preserve;
- source figure identity;
- source hash or source-node identity;
- caption relationship;
- live construction source.

### Representation

Record:

- live CSS/HTML;
- live SVG/CSS;
- simplified live construction;
- raster plate;
- decorative asset;
- dimensions;
- representation hash;
- derivation method;
- platform suitability.

### Accessibility

Keep separate from admission.

Record:

- role: decorative / relational / explanatory;
- short alternative;
- long-description need;
- live caption identity;
- embedded labels;
- native accessibility notes.

### Platform admission

Record:

- platform/package family;
- admitted representation;
- recipe/profile identity;
- representation hash;
- authorization;
- substitution permission.

### Review

Record:

- renderer/profile tested;
- reviewer;
- date;
- exact artifact hash;
- local graphic standing;
- native-renderer graphic standing;
- whole-page composition standing.

**Admission is not accessibility approval.**
**Accessibility sufficiency is not renderer admission.**

---

## 9. Graphic representation rule

Keep live graphics live where the renderer preserves their relation.

A bounded plate is an admitted fallback representation, not “the real graphic” simply because one renderer needs it.

Pseudo-elements may embellish meaning; they should not be the sole carrier of an essential spatial event when the target renderer cannot preserve them.

---

## 10. Navigation architecture

Major TOC destinations should prefer direct semantic-entry document targets.

Fragments remain appropriate for meaningful internal destinations when reliable.

Navigation must be proven before visual sign-off.

---

## 11. Shared source-to-publication method

### A. Establish authority

Record canonical source, source hash, canonical cover/assets, prior accepted platform references, sibling evidence, recipe identity, and the authority/evidence distinction.

Never begin by editing the latest successful retailer file.

### B. Identify semantic units

Declare stable source identities for front matter, major entries, graphics, captions, and significant internal destinations.

### C. Preserve semantic units exactly

Prefer changing package structure **around** semantic units rather than rewriting semantic units to obtain structure.

Where possible prove:

- exact lexical preservation;
- canonicalized XML equivalence;
- normalized text/order equivalence.

### D. Assemble shared presentation

Build common composition in the shared stylesheet.

### E. Add narrow platform layer

Only platform-evidenced exceptions belong here.

For each deviation record origin, scope, reason class, relation preserved, and removal test.

### F. Choose graphic representation

Use the shared registry and the appropriate escalation branch.

### G. Build navigation from structural truth

Direct major-entry document destinations; local fragments where meaningful and reliable.

### H. Prove content equivalence

Check:

- semantic unit presence;
- wording/order;
- captions;
- links;
- graphic identities;
- duplicate manuscript;
- unrecorded supplemental content.

### I. Validate package

Check:

- `mimetype`;
- container;
- OPF;
- manifest;
- spine;
- XML/XHTML;
- resources;
- IDs/IDREFs;
- links;
- stylesheets;
- EPUBCheck or equivalent.

### J. Platform-native conversion/import

Standards validation does not replace native ingestion.

### K. Renderer-native layout review

Inspect pagination, reading measure, two-page behavior, headings, quiet space, dark/light fields, boundaries, graphics, responsive behavior, and ending.

### L. Graphic-specific review

Review platform representations separately where needed.

### M. Accessibility review

Review structural semantics, heading order, image roles, alt, captions, long descriptions, decorative exclusions, and native behavior where inspectable.

### N. Whole-book human pass

Beginning to end.

Look for duplication, disappearance, dead navigation, unintended repetition, strange blank pages, collapsed graphics, stranded labels/captions, pacing changes, and an ending that no longer lands.

### O. Freeze exact bytes

Only after gates close:

- filename;
- SHA-256;
- validation receipts;
- human acceptance;
- no mutation afterward.

Any change creates a new candidate.

### P. Retailer ingestion + post-publication smoke check

Retailer acceptance remains a separate crossing.

---

## 12. Validation / freeze protocol

1. Source identity + build recipe identity
2. Content equivalence / mutation check
3. Package structure + standards validation
4. Reading order + navigation + links
5. Platform conversion/import
6. Renderer-native layout review
7. Graphic-specific review
8. Accessibility review
9. Whole-book human pass
10. Release artifact identity lock
11. Human release decision
12. Retailer ingestion + post-publication smoke check

Identity bookends the process:

At the beginning: **What are we building from?**
At the end: **What exact bytes did we accept?**

The whole-book human pass is a release gate, not ceremonial QA.

### Current BHT release closure

Both retailer derivatives reached the same documented release standing:

- Porter whole-book visual review: **PASSED**
- EPUBCheck v5.4.0: **0 fatals / 0 errors / 0 warnings / 0 infos**
- release copy: **byte-identical** to the validated candidate
- mutation after validation: **none**
- retailer ingestion / store smoke check: separate from the frozen EPUB

The two packages are not byte- or structure-identical. Their equivalence is semantic, relational, and evidentiary.

---

## 13. Apple / non-Kindle appendix

### Frozen Apple release

`BHT_APPLE_EPUB1_RELEASE_001.epub`

- bytes: `3,711,173`
- SHA-256: `40ffe038e163a818335af9ba65a1380e84bb5cbfa69ac5eef11d1dc23781757b`
- governing candidate: `BHT_APPLE_RELEASE_SMOOTHING_CANDIDATE_007.epub`
- candidate → release relation: **byte-identical copy**
- Porter visual review: **PASSED**
- EPUBCheck v5.4.0: **0 / 0 / 0 / 0**
- mutation after validation: **none**
- freeze date: `2026-10-07`

This is the frozen Apple EPUB 1 artifact. A later change requires a new candidate and release identity.

### Apple package architecture

Reading-order package:

- `cover.xhtml`
- `frontmatter.xhtml`
- `entry-00.xhtml`
- …
- `entry-21.xhtml`

That is 24 spine documents: cover, front matter, and 22 major semantic entries.

There are no Kindle-only renderer-stability split documents.

CSS:

- `shared.css`
- `apple.css`
- `cover.css`

Major TOC entries point directly to entry documents.

The final package contains 35 ZIP members, 32 manifest items, four JPEG publication assets, and no Kindle plate or decoration directories.

### Apple cover roles

External Apple marketing cover:

`Now_You_Can_Do_Big_Hard_Things_cover_master_1600x2560.png`

- dimensions: `1600 × 2560`
- bytes: `5,341,828`
- SHA-256: `b282a3cbd9ea1fef9c0e77c125000dcb2d3b0075adccb1bd92912f08cf8a7bcc`

In-book Apple cover:

`BHT_cover_apple_inbook_1580x2528_q98.jpg`

- dimensions: `1580 × 2528`
- bytes: `2,023,814`
- SHA-256: `e5bafa54a939ab3e082c52c1a5d9136de1390a4c35f037f8eeb45d6c2c777dc5`

These are different roles, not competing authorities.

### Apple-proven lessons

- restoring normal flow can repair pagination where containment prevents fragmentation;
- `overflow:hidden` can turn a chapter wrapper into a pagination failure;
- viewport width and actual page measure can diverge;
- semantic-entry document structure works without making the reading mechanically chaptered;
- direct-document major navigation works cleanly;
- structural splitting can retire obsolete page-break CSS;
- live CSS/HTML and SVG graphics remain first-class when the renderer preserves their relation;
- platform CSS can stay narrow;
- blank or quiet pages should not be removed by default;
- a working Apple representation should not inherit Kindle plates merely because Kindle required them.

### Apple graphic standing

The clean Apple line retained live CSS/HTML and SVG/CSS constructions where their relational meaning survived.

The final package uses the selected in-book cover plus the three selected White Room JPEG derivatives. It does not import the Kindle plate registry as a package dependency.

### Apple remaining external crossing

The EPUB itself is frozen.

Retailer account/upload/import status and post-publication smoke checking remain separate operational evidence. They do not authorize silent mutation of Release 001.

---

## 14. Kindle appendix

### Frozen Kindle release

`BHT_KINDLE_EPUB1_RELEASE_001.epub`

- bytes: `6,658,243`
- SHA-256: `225592b811b301200e9477e172269a0099152f1f94701a20bfcfc5961088c9d7`
- governing candidate: `BHT_KINDLE_RELEASE_SMOOTHING_CANDIDATE_004.epub`
- candidate → release relation: **byte-identical copy**
- Porter Kindle visual review: **PASSED**
- EPUBCheck v5.4.0: **0 / 0 / 0 / 0**
- mutation after validation: **none**
- recorded acceptance date: `2026-10-06`

This is the frozen Kindle EPUB 1 artifact. `BHT_KINDLE_CANONICAL_001.epub` is historical package evidence, not the retail release.

### Kindle package architecture

The common structure remains one major semantic entry per XHTML document, with two admitted renderer-stability exceptions:

- `entry-06.xhtml` → `entry-06-activation.xhtml`
- `entry-14.xhtml` → `entry-14-human.xhtml`

The final package therefore has 26 spine documents.

CSS:

- `cover.css`
- `kindle.css`
- `shared.css`

Major TOC entries still point to the major semantic-entry documents. The renderer-only split files are reading-order continuations, not new TOC chapters.

The final package contains 77 ZIP members, 74 manifest items, 37 PNG assets, seven JPEG assets, and the two explicit split documents.

### Kindle renderer-stability exceptions

#### Jules

Boundary:

`Presence → Startup & Settle`

Reason:

**RENDERER-STABILITY**

Evidence:

Unstable repaint/page behavior persisted through softer repairs and resolved after a hard content-document boundary.

Removal test:

A future Kindle renderer demonstrates stable forward/backward reading across the same boundary without the split.

#### Western

Boundary:

`Present Recognition → Human authority and family → Human`

Reason:

**RENDERER-STABILITY**

Evidence:

Dark-banner fragmentation/repaint persisted through break controls and same-document changes and resolved after a hard spine/document split.

Removal test:

A future Kindle renderer demonstrates stable forward/backward reading without the split.

### Kindle graphic standing

- live spatial graphics were retained where Kindle preserved the relation;
- bounded plates were admitted where Kindle preserved parts but destroyed relation;
- prose and separable captions remained live;
- plate identity, review, accessibility treatment, and admission remained distinct;
- foreground/background pairing was localized where distant dark fields proved fragile;
- the generated Spot bloom became an explicit opaque crack/trace;
- the closing light became a small explicit decorative asset;
- quiet pages and the separated final declaration were accepted as composition rather than defects.

### Kindle/general cover

`Now_You_Can_Do_Big_Hard_Things_cover_master_1600x2560_q98.jpg`

- dimensions: `1600 × 2560`
- bytes: `2,037,016`
- SHA-256: `9cf72ed964324bca45dea25ac8d8de95a83114595f140882191095f185f588c6`

The Apple in-book cover is not a Kindle package asset.

### Kindle selected shared publication assets

The three White Room JPEG derivatives are shared with Apple and retain the same hashes in both packages:

- `WR2_01_Hallway_Threshold_Console_TransitCart_v1_epub_q96.jpg`
  `8e398c9aad4fdba239964bd5ce1b010fc0f1f951accbe6cbfdaaecf994f04270`
- `WR2_10_RoomSide_GDB_Formation_First_Milliseconds_v1_epub_q96.jpg`
  `7c99a2b366679500c2175d47860deda1797762512950e36a9cc5e916d56148fe`
- `WR2_13_Hallway_PathsReport_USB_Envelope_v1_epub_q96.jpg`
  `0b83be93402d868329ea0fe966e857c70c4777d79db7762537502c0f1f9024e5`

### Kindle remaining external crossing

The EPUB itself is frozen.

KDP upload, conversion/ingestion receipts, retailer preview, and post-publication smoke checking remain separate operational evidence. They do not authorize silent mutation of Release 001.

---

## 15. Clean sibling-edition rule

Sibling editions do not need implementation identity.

They must preserve:

- the same semantic source;
- the same major reading order;
- the same manuscript wording;
- the same graphic identities;
- comparable relational meaning;
- traceable platform deviations.

Ask:

- Does each edition feel like the same book?
- Does either package introduce a claim, emphasis, or sequence the other does not?
- Does either implementation make the reader work harder for reasons unrelated to the manuscript?
- Is any platform adaptation louder than the relation it preserves?
- Does the implementation disappear behind the reading?

Do not delay release solely to make sibling packages cosmetically identical.

---

## 16. Twenty durable rules

1. The semantic source is canonical; retailer packages are derivatives.
2. A successful retailer EPUB is evidence, not automatically the next source.
3. Major semantic entries are good default document units.
4. Renderer-only splits remain explicit exceptions.
5. Shared CSS plus a narrow named platform layer is preferable to dispersed repair styling.
6. Structural change should replace obsolete cosmetic repair rather than merely accumulate beneath it.
7. Major navigation should prefer document destinations.
8. Viewport width and reading measure are different variables.
9. Containment is a fragmentation decision.
10. Pseudo-elements may decorate meaning but should not be the sole essential carrier when the target cannot preserve them.
11. Live graphics should remain live where the renderer preserves their relation.
12. Bounded plates are legitimate when live spatial relation fails—not because plates are intrinsically safer.
13. Every platform representation should trace to a shared graphic identity.
14. Accessibility, representation admission, and visual review are related but distinct judgments.
15. Blank space must be interpreted before it is repaired.
16. A renderer-stability fix must carry provenance so future maintainers do not normalize it away.
17. Content equivalence should be proved mechanically wherever possible.
18. Whole-book human reading is a release gate, not ceremonial QA.
19. Freeze exact bytes, not a filename or an intention.
20. Sibling editions should preserve the same relations without being forced into implementation identity.

---

## 17. Maintenance discipline

Every platform-specific deviation needs a reason.

Every workaround needs a removal test.

Repairs have scope.

After architectural change, reevaluate older cosmetic rules instead of accumulating them forever.

Preserve lineage: new instructions supersede older instructions for future work; old evidence remains part of project history.

---

## 18. Release standard

The standard is not:

> technically acceptable.

It is:

> structurally intelligible, visually coherent, traceable, reviewable, and calm enough that the implementation disappears behind the reading.

Porter’s criterion remains:

> People look at it and say, “Well, that is intelligent.”

And the conclusion now supported by both clean rebuilds is:

> **The book has a stable semantic anatomy, but no single mandatory physical skeleton.**
>
> **A good publication build makes the semantic anatomy explicit, then gives each renderer only as much additional structure as it has earned.**
