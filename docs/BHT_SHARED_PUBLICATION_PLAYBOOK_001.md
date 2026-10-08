# BHT Shared Publication / Build Playbook — 001

**Status:** Draft operating architecture for the next clean rebuild  
**Date:** 2026-10-05  
**Scope:** Shared rules first; Apple / non-Kindle and Kindle appendices beneath them  
**Boundary:** This playbook does not reopen earlier accepted candidates by itself. Porter has explicitly chosen to rerun both editions after the architecture is settled, using the cleanest shared method we can establish.

---

## 1. Purpose

BHT has now been solved in two reading environments through different failure modes:

- the non-Kindle / Apple-targeted branch exposed fragmentation, page-geometry, reading-measure, and containment problems;
- the Kindle branch exposed conversion, fragment navigation, renderer reconstruction, repaint, and spatial-relationship failures.

The goal is not to force both packages into one implementation.

The goal is to preserve one semantic book while allowing platform packages to use the least forceful structure that reliably preserves the relationship the reader actually needs.

**Held line**

> The manuscript supplies the relation.  
> The package chooses the least forceful structure that lets that relation survive the reader.

---

## 2. Common architecture

### 2.1 Canonical authority

The highest authority is the **shared semantic source**, not any EPUB/XHTML derivative.

Every accepted platform derivative must be traceable back to that semantic source without interpretation.

A future maintainer should be able to answer:

- what source entry produced this platform document;
- what representation produced this graphic;
- what platform-specific deviation was applied;
- why that deviation exists;
- what evidence admitted it.

### 2.2 Default document unit

For the next-generation build:

**one major semantic entry → one XHTML spine document by default**

The semantic entry remains canonical; the XHTML file is a deterministic package representation of it.

A platform may combine entries only for a demonstrated reason.

A renderer-only split that does not correspond to a semantic entry is allowed, but it must be recorded as an exception rather than presented as a new manuscript chapter.

### 2.3 Boundary provenance

Every nontrivial platform/package boundary should carry a reason class:

- **SEMANTIC** — the source itself declares the boundary;
- **COMPOSITIONAL** — the reading experience benefits from a stronger flow/page boundary;
- **RENDERER-STABILITY** — the target renderer demonstrably fails without a stronger boundary;
- **PACKAGING** — cover, navigation, retailer/package requirement, or similar;
- **ACCESSIBILITY** — a stronger boundary or representation is needed for accessible reading;
- **PLATFORM-POLICY** — required by a specific platform's ingestion or rendering rules.

Examples already established in BHT:

- Western `Present Recognition → Human authority and family → Human`  
  **RENDERER-STABILITY**
- Jules `Presence → Startup & Settle`  
  **RENDERER-STABILITY**
- separate cover document in the Apple-targeted package  
  **PACKAGING**

---

## 3. Two escalation branches

Do not treat all failures as one ladder.

### 3.1 Flow / pagination failure

Use the weakest intervention that works:

**normal flow → responsive repair → local containment → explicit page boundary → renderer-proven spine boundary**

Before escalating, inspect:

- `overflow`;
- fixed/min heights;
- positioned ancestors;
- containment;
- keep-together rules;
- page/column break suppression;
- actual reading measure versus outer viewport width.

A spine split is an escalation, not a substitute for noticing a bad wrapper.

### 3.2 Graphic / spatial failure

Use the weakest representation that reliably preserves the relation:

**live construction → local responsive repair → simplified live construction → bounded plate**

A bounded raster plate is legitimate when:

- the meaning is primarily spatial;
- the renderer preserves pieces but destroys their relation;
- prose remains live;
- separable captions remain live;
- accessibility treatment is explicit;
- resolution is sufficient;
- the representation is hash-locked and reviewable.

Do not rasterize because a spine split failed.  
Do not split documents because an SVG misbehaves.

---

## 4. Shared graphic registry

Every meaningful visual construction receives one durable `graphic_id`.

That identity answers:

> What relationship is this visual supposed to carry?

Platform representations hang from that identity rather than becoming unrelated artwork.

### 4.1 Graphic identity record

Records:

- `graphic_id`
- semantic purpose / relation to preserve
- source figure identity
- source hash or source-node identity
- caption relationship
- live construction source, when one exists

### 4.2 Representation record

Records:

- representation type:
  - live CSS/SVG
  - simplified live construction
  - raster plate
  - decorative asset
- dimensions
- file hash
- source representation
- derivation method
- platform suitability notes

### 4.3 Accessibility record

Keep separate from admission.

Records:

- role:
  - decorative
  - relational
  - explanatory
- short alternative
- long-description required: yes/no
- live caption identity
- labels embedded in image
- platform-native accessibility notes

### 4.4 Platform admission record

Records:

- platform / package family
- admitted representation
- profile / recipe identity
- exact representation hash
- authorization
- whether substitution is permitted

### 4.5 Review record

Records:

- renderer / profile tested
- reviewer
- date
- exact artifact hash
- local graphic standing
- platform-rendered graphic standing
- whole-page composition standing

**Important:** admission is not accessibility approval, and accessibility sufficiency is not renderer admission.

---

## 5. Shared stylesheet architecture

Prefer:

1. **canonical/shared stylesheet**
2. **small, named platform layers**
3. **narrow diagnostic/renderer overrides only when evidence requires them**

Avoid:

- duplicated CSS payloads across many XHTML files;
- platform repairs dispersed through manuscript markup;
- hidden override chains with unclear provenance.

Every platform-specific rule should make it possible to answer:

- does this rule express manuscript design?
- composition?
- renderer stability?
- accessibility?
- retailer/platform policy?

---

## 6. Durable layout principles

### 6.1 Reading measure is not viewport width

A wide application window may contain a narrow reading page.

Layouts should respond to the real reading measure, not assume outer viewport width equals page width.

This matters especially for:

- grids;
- side-by-side fields;
- menus;
- diagrams;
- blooms;
- text-image relationships.

### 6.2 Containment is a pagination decision

A wrapper can be semantically harmless and still become a fragmentation boundary.

Before adding stronger page controls, inspect containment.

### 6.3 Major-entry and internal-movement boundaries differ

- major semantic entry → may justify an explicit page or document boundary;
- internal movement/subsection → preserve local cohesion, but allow natural flow;
- renderer-unstable movement → escalate only after evidence.

### 6.4 Blank space is evidence to interpret

Do not remove quiet space merely because pagination makes it measurable.

Blank space is a defect only when:

- required content has disappeared;
- reading order is broken;
- unstable flow has created an accidental void.

Otherwise it may be compositional work.

### 6.5 Generated decoration

Pseudo-elements may embellish meaning.

They should not be the sole carrier of an essential spatial event.

If the visual relation matters, prefer a representation with explicit package identity.

---

## 7. Shared validation ladder

Run in this order unless a bounded diagnostic has a clear reason to do less.

### 1. Source identity + build recipe identity

Establish:

- canonical semantic source
- source hash
- platform recipe
- recipe/version hash
- expected package family

### 2. Content-equivalence / mutation check

Prove what did and did not change from the canonical manuscript.

No silent editorial drift.

### 3. Package structure + standards validation

Check:

- OPF
- manifest
- spine
- XML/XHTML
- required assets
- EPUBCheck or equivalent standards validation

### 4. Reading order + navigation + destinations + links

Prove the reader can traverse the intended book before judging appearance.

### 5. Platform conversion / ingestion

Examples:

- Kindle Previewer conversion
- Apple Books import
- equivalent platform-native ingestion

### 6. Renderer-native layout review

Review together:

- pagination
- reading measure
- containment
- headings
- dark/light fields
- boundaries
- blank space
- graphics
- responsive behavior

### 7. Graphic-specific review

Review platform representation of relational graphics separately where needed.

### 8. Accessibility review

Review:

- structural semantics
- alt/description/caption relations
- decorative exclusions
- long descriptions
- platform-native accessibility behavior where inspectable

### 9. Whole-book human pass

Beginning to end.

Look for failures no local test predicted.

This is a distinct gate.

### 10. Release artifact identity lock

Record exact:

- filename
- SHA-256
- validation receipts
- retailer-preparation artifacts

No mutation after this point without a new candidate identity.

### 11. Human release decision

Release remains a human authorization.

### 12. Retailer ingestion + post-publication smoke check

Retailer acceptance does not prove correct store behavior.

Check the live product after ingestion.

---

## 8. Apple / non-Kindle appendix

### Proven lessons

- restoring normal flow can repair pagination where containment prevents fragmentation;
- `overflow:hidden` can turn an otherwise valid chapter wrapper into a pagination failure;
- a wide reader window may still contain narrow pages;
- major-entry page starts can be explicit without forcing every subsection to a new page;
- compact thought-units may deserve containment when they fit;
- the Spot bloom worked live in the current non-Kindle review environment after local positioning repair;
- a separate cover spine document can be introduced cleanly;
- the accepted Apple-targeted derivative passed EPUBCheck 5.3.0 with zero reported findings in the recorded run.

### Current evidence boundary

The accepted Apple-targeted candidate has been reviewed in Thorium and controlled Chromium pagination tests.

Apple Books itself still needs to be included in the clean rerun before final release confidence.

### Do not reopen merely for elegance

Do not mutate the accepted Apple candidate just to:

- split every entry;
- externalize CSS;
- rasterize working graphics.

Those improvements belong to the next clean shared build unless native Apple testing demonstrates a need sooner.

---

## 9. Kindle appendix

### Proven lessons

#### TOC / fragment conversion

A monolithic body with fragment-dependent logical TOC targets repeatedly failed Kindle conversion.

The successful architecture used:

- deterministic entry XHTML documents;
- external CSS;
- fragmentless TOC links to entry documents.

#### Spatial graphics

Kindle often retained the parts of live CSS/SVG figures while destroying the relation between them.

Recovered/admitted SMALL and MEDIUM plates, plus bounded FIELD and OPENING treatments, stabilized those relations while keeping prose and captions live.

#### Foreground/background pairing

Where pale text depended on a distant dark ancestor, Kindle could preserve the text while losing/delaying the field.

Bind critical foreground/background pairs more locally on text-bearing boxes.

#### Repaint / unstable boundary behavior

CSS break controls and keep-together hints were insufficient at two boundaries.

A true new XHTML/spine document resolved the instability.

Proven examples:

- Western `Present Recognition → Human authority and family → Human`
- Jules `Presence → Startup & Settle`

These are **RENDERER-STABILITY** splits, not new manuscript chapters.

#### Generated Spot effect

The generated bloom was not durable enough.

A small opaque fissure/crack image beside the live sentence:

> “This is the spot,” she said.

proved a stable visual trace.

#### Closing light

A small opaque edge-light image preserves the intended closing gesture without depending on fragile gradient support.

The page-turn separation before:

> “The next movement belongs to you.”

is accepted as useful composition, not a defect.

### Current Kindle working candidate

`BHT_KINDLE_JULES_SPINE_SPOT_CANDIDATE_009.epub`

Recorded SHA-256:

`a03f5a088b492851f5bc03fe896bad5451f3530d65e8a20b11bba6d5adccf6ee`

Porter completed a clean beginning-to-end Kindle Previewer pass on this candidate.

This remains working evidence, not the final release artifact.

---

## 10. Clean rerun policy

Porter has explicitly chosen to rerun **both editions** after this architecture is settled.

Therefore:

- current Apple and Kindle candidates are evidence sources;
- do not simply rename either one as final;
- rebuild from the shared semantic source through the new architecture;
- preserve known-good renderer-specific deviations with explicit provenance;
- rerun the entire validation ladder for each platform;
- compare content equivalence across both derivatives;
- perform a fresh whole-book human pass on each;
- lock new final hashes only after those passes.

The goal is not to prove that earlier work was wrong.

The goal is to let both branches teach the clean rebuild.

---

## 11. Twelve durable rules

1. Source semantics stay canonical; packages may differ structurally.
2. Major-entry and internal-movement boundaries are not interchangeable.
3. Use the weakest representation that reliably preserves the needed relation.
4. Viewport width is not necessarily reading-measure width.
5. Containment is a pagination decision, even when it looks like harmless styling.
6. Pseudo-elements should not be the sole carrier of essential meaning.
7. Raster plates are valid platform adaptations when relationship—not text—is what must be stabilized.
8. Renderer-specific hard splits require recorded provenance.
9. Blank space is evidence to interpret, not waste to remove automatically.
10. Platform branches must remain packaging branches, not divergent manuscripts.
11. Every platform-specific deviation needs a reason class.
12. Every accepted derivative must be traceable back to the same semantic source without interpretation.

---

## 12. Release standard

The standard is not:

> technically acceptable.

It is:

> structurally intelligible, visually coherent, traceable, reviewable, and calm enough that the implementation disappears behind the reading.

Porter’s criterion is simpler:

> People look at it and say, “Well, that is intelligent.”

That is the release horizon.
