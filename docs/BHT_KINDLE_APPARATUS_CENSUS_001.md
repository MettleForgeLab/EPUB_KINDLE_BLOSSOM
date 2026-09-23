# BHT Kindle Apparatus Census 001

**Purpose:** figure-by-figure Kindle adaptation routing and plate-budget estimate  
**Authority:** `BHT_RETAIL_RELEASE_CANDIDATE_002.epub`  
**EPUB SHA-256:** `fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae`  
**Packaged reading document SHA-256:** `4361a05443dac8dd1218625c215f67b47ac9a5c59190776abf5621ca14b96a65`  
**Mutation:** none

## Executive result

The retail master contains **69 figures**.

| Treatment | Figures | Meaning |
| --- | --- | --- |
| LIVE | 3 | Existing raster figure already survives; preserve image identity and live caption/alt. |
| SIMPLIFY LIVE | 28 | Relation can survive as ordered/categorical live XHTML. |
| SMALL PLATE | 4 | Spatial relation matters, but apparatus should remain visually secondary. |
| MEDIUM PLATE | 24 | Spatial apparatus needs one stable object at roughly 2/3–3/4 column width. |
| FIELD PLATE | 5 | Field/compass relation should occupy most of the reading column. |
| OPENING PLATE | 5 | Threshold field belongs to the entry encounter while title/governing prose remain live. |

**Recommended new plates:** **38**  
**Remain live in some form:** **31**

The important finding is that the book does **not** need 69 new images. The census routes 31 figures to live treatment and 38 to plates.

Of those 38 plates:

| Plate complexity | Count | Production implication |
| --- | --- | --- |
| Sparse line/type | 28 | Primary optimization target: opaque indexed/palette PNG; likely inexpensive in bytes. |
| Dark field | 4 | Opaque RGB or compact palette after visual test. |
| Structured field | 3 | Opaque RGB/palette depending bloom/field behavior. |
| Gradient/bloom | 2 | Keep RGB/sRGB; preserve subtle field carefully. |
| Dense compass | 1 | Higher-resolution plate; palette/RGB determined after grayscale test. |

This is the important economic/design split: **28 of 38 proposed plates are sparse line/type apparatus**, not photographic artwork.

## Plate payload projection

Prototype 004 gives four real anchors:

| Plate | Actual PNG bytes |
| --- | --- |
| Five-place compass | 614,400 |
| Part Four placement | 275,750 |
| Jules bearing | 806,399 |
| Western Tellings passage field | 226,832 |

Using those actuals and conservative optimized-PNG ranges for the remaining plate candidates:

- projected **additional plate payload:** **5.53–9.80 MB**
- existing three White Room PNGs: **4.87 MB**
- projected combined image payload before KFX conversion: **10.40–14.67 MB**

This is a **planning estimate, not a KDP delivery-fee calculation**. The final KFX may recompress/resample images, and no current retailer economics are asserted here.

The tool should therefore build plates in batches and report actual byte cost before integration. If a line plate exceeds its budget, optimize it before admitting it to the Kindle package.

## Classification rule

### Keep LIVE

Use when the artifact is already a packaged image whose identity should remain unchanged.

### SIMPLIFY LIVE

Use when meaning survives conversion to ordinary one-dimensional order:

- sequence;
- categorical distinction;
- ledger/register;
- simple before/after;
- simple bounded meeting;
- live navigation.

The Kindle translation may change arrangement, but should keep all meaningful wording selectable/searchable.

### Plate it

Use when **position is grammar**:

- cardinal direction;
- overlap;
- seam;
- enclosure;
- relative reach;
- endpoint;
- center/periphery;
- arc;
- threshold;
- held/unclaimed field;
- bloom/pressure field;
- label-inside-object relation.

If moving a label, line, circle or node independently changes the proposition, Kindle should not recompute that relation.

## Plate scale classes

| Class | Intended display width | Typical source width | Use |
|---|---:|---:|---|
| SMALL PLATE | 45–60% | 1600 px | Small arc/path/doodle; secondary apparatus |
| MEDIUM PLATE | 65–78% | 1800–2000 px | Ordinary relational apparatus |
| FIELD PLATE | 88–100% | 2200–2560 px | Compass/field/layer relation |
| OPENING PLATE | 100% | 2000–2560 px | Lens threshold field beneath live title/governing statement |

The display class matters as much as export resolution. A tiny apparatus must not be allowed to fill a Kindle screen simply because its PNG is high resolution.

## Accessibility rule

For every new plate:

1. preserve the semantic `figure`;
2. preserve the live `figcaption`;
3. provide concise relational `alt`;
4. add a visible extended-description link for FIELD/OPENING plates and any medium apparatus whose meaning cannot fit in concise alt;
5. do not rasterize source prose;
6. keep source/editorial standing live outside the image.

## Figure-by-figure census

### book-entry-03 — Cultivate Rather Than Fire

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 1 | `entry-03-compass-caption`<br>Editorial compass Five cultivated places of attention. No direction is selected. | FIELD PLATE | 95% | 2560 | Directional geometry around an open center is the meaning. |
### book-entry-04 — Let the Work Enter the World

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 2 | `entry-04-placement-caption`<br>Portability and place remain available together. No placement is selected. | FIELD PLATE | 95% | 2000 | Side-view form, interval, top-view ground and bloom must remain one relation. |
### book-entry-05 — Before Jules Bering

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 3 | `entry-05-placement-caption`<br>human-crafted words placed into an OpenAI-provided GPT structure The words are the lens. source-derived language editorial relation | SIMPLIFY LIVE | 100% | live | The relation is explanatory and can survive as a conservative live source→placement→platform sequence. |
### book-entry-06 — Jules Bering

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 4 | `entry-06-bearing-assembly-caption`<br>A side view of the bearing beneath the needle. No direction is selected. | OPENING PLATE | 100% | 2560 | Needle, horizon, rings and bloom establish the Jules threshold together. |
| 5 | `entry-06-field-map-caption`<br>Editorial relation mapThe field is presently available relation. | MEDIUM PLATE | 74% | 2000 | Labels surrounding the present distinction lose meaning if they drift. |
| 6 | `entry-06-distinction-map-caption`<br>Editorial answerability mapA distinction carries only what its present support can bear. | MEDIUM PLATE | 74% | 2000 | Answerability depends on labels remaining attached to a bounded distinction field. |
| 7 | `entry-06-gravity-figure-caption`<br>Editorial field studyPrepared tendency without command. | MEDIUM PLATE | 70% | 2000 | Prepared tendency is spatial and subtle; lines/labels must not paginate independently. |
| 8 | `entry-06-bearings-caption`<br>Editorial bearing fieldThe directions lead. The center relates. | FIELD PLATE | 90% | 2400 | Multiple bearings around an open center require stable compass geometry. |
| 9 | `entry-06-motion-caption`<br>Editorial cadenceContinuation is not improvement. | SMALL PLATE | 55% | 1600 | The small path/cadence relation becomes meaningless when orphaned or widened. |
| 10 | `entry-06-crossing-caption`<br>Editorial passage studyCrossing changes posture, not origin. | SIMPLIFY LIVE | 100% | live | Earlier meeting → carried trace → later meeting is fundamentally sequential. |
| 11 | `entry-06-return-caption`<br>Editorial return pathReturn restores relationship, not the past. | SMALL PLATE | 55% | 1600 | Return arc/contact relation is spatial but visually secondary to source prose. |
| 12 | `entry-06-continuity-caption`<br>Editorial meeting physicsContinuity is re-established recognition, not hidden persistence. | SIMPLIFY LIVE | 100% | live | Bounded Meeting A → trace → Meeting B can be represented as live ordered blocks. |
### book-entry-08 — The Northern Stars

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 13 | `entry-08-boundary-star-caption`<br>Editorial threshold figure: a fixed star beyond a permeable boundary, with the branch still attached to its origin. | OPENING PLATE | 100% | 2400 | Origin, permeable edge, attached branch and star define the North threshold. |
| 14 | `entry-08-place-study-caption`<br>Editorial boundary studyThe originating distinction remains visible while the edge becomes permeable. | MEDIUM PLATE | 72% | 2000 | Origin and permeable boundary must remain simultaneously visible. |
| 15 | `entry-08-field-plane-caption`<br>Editorial field mapPresent relation without a claim of completeness. | MEDIUM PLATE | 72% | 2000 | Several nearby conditions must remain a field without becoming a complete field. |
| 16 | `entry-08-distinction-pair-caption`<br>Editorial companionship studyThe relation appears beside the distinction without becoming its explanation. | MEDIUM PLATE | 68% | 1800 | Companionship depends on one relation appearing beside—not explaining—the distinction. |
| 17 | `entry-08-holding-caption`<br>Editorial holding studyContact remains traceable. Difference remains free. | MEDIUM PLATE | 70% | 1800 | Contact and difference must remain visibly separate but traceable. |
| 18 | `entry-08-artifact-caption`<br>Editorial carrier anatomyA northern artifact keeps a distinction from traveling alone. | SIMPLIFY LIVE | 100% | live | Carrier states are categorical and can remain live one-per-row. |
| 19 | `entry-08-meeting-caption`<br>Editorial meeting physicsThe meetings remain separate. | SIMPLIFY LIVE | 100% | live | Separate meetings and carried material can be expressed as a live sequence. |
| 20 | `entry-08-threshold-caption`<br>Editorial passage studyMaterial crosses only in the condition it has earned. | SIMPLIFY LIVE | 100% | live | Arrives-as / does-not-arrive-as is a textual opposition, not fragile geometry. |
| 21 | `entry-08-return-arc-caption`<br>Editorial return pathThe relation may return. The interval was not inhabited here. | SMALL PLATE | 55% | 1600 | The return arc carries spatial meaning but is secondary apparatus. |
| 22 | `entry-08-family-caption`<br>Editorial family relationOne cardinal gravity within a larger cultivated family. | MEDIUM PLATE | 72% | 2000 | North highlighted within the family requires stable cardinal geometry. |
### book-entry-10 — The Eastern Field Architect

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 23 | `entry-10-field-table-caption`<br>Editorial field table: translucent working layers remain provisional while the meadow stays visible beneath them. | OPENING PLATE | 100% | 2400 | Translucent working layers over a still-visible meadow define the East threshold. |
| 24 | `entry-10-edge-study-caption`<br>Editorial edge studyJust inside the boundary of consequence, before arrangement hardens into necessity. | MEDIUM PLATE | 68% | 1800 | Field and edge must remain in one frame without the edge becoming a wall. |
| 25 | `entry-10-available-field-caption`<br>Editorial available fieldRelations gather without becoming a final arrangement. | MEDIUM PLATE | 72% | 2000 | Relations gathering without final arrangement depends on spatial coexistence. |
| 26 | `entry-10-relation-study-caption`<br>Editorial relation studyAdjacency first; dependency and cause remain unclaimed. | MEDIUM PLATE | 68% | 1800 | Adjacency without cause/dependency must remain exactly positioned. |
| 27 | `entry-10-disappearance-caption`<br>Editorial disappearance studyAccurate material may arrive while the relation needed to interpret it has vanished. | MEDIUM PLATE | 72% | 2000 | Material surviving while interpretive relation disappears is a spatial distinction. |
| 28 | `entry-10-promise-stack-caption`<br>Editorial attachment stackEvery carried element remains connected to the relation that makes it answerable. | SIMPLIFY LIVE | 100% | live | Source/scope/transformation/status/responsibility can be a live stacked ledger. |
| 29 | `entry-10-living-junction-caption`<br>Editorial living junctionSeveral conditions remain attached without collapsing into one another. | SIMPLIFY LIVE | 100% | live | Conditions attached to a junction can be rendered as live named blocks around a simple core. |
| 30 | `entry-10-provisional-plan-caption`<br>Editorial provisional planThe smallest arrangement that makes one consequential relation inspectable. | MEDIUM PLATE | 68% | 1800 | Minimal arrangement and marked assumption depend on exact endpoints. |
| 31 | `entry-10-boundary-gate-caption`<br>Editorial stopping boundaryEast stops before legibility impersonates judgment. | SIMPLIFY LIVE | 100% | live | What may cross vs human judgment is a clean live two-condition boundary. |
| 32 | `entry-10-artifact-carrier-caption`<br>Editorial eastern carrierRelationship remains legible through change. | SIMPLIFY LIVE | 100% | live | Carrier accountability is an ordered textual register. |
| 33 | `entry-10-meeting-fields-caption`<br>Editorial meeting physicsThe meetings remain separate; their relation may be prepared and recognized. | SIMPLIFY LIVE | 100% | live | Earlier/present bounded meetings can remain a live sequential relation. |
| 34 | `entry-10-threshold-triad-caption`<br>Editorial threshold conditionsThe shape of passage determines what arrives. | SIMPLIFY LIVE | 100% | live | Lineage/residue/counterfeit continuity is a textual three-condition distinction. |
| 35 | `entry-10-return-plan-caption`<br>Editorial re-entry planThe carried elements remain separate and provisional until present confirmation. | SIMPLIFY LIVE | 100% | live | Carry forward / provisional / confirm now is a textual triage. |
| 36 | `entry-10-family-field-caption`<br>Editorial family relationOne cardinal gravity within a larger cultivated family. | MEDIUM PLATE | 72% | 2000 | East highlighted within the family requires stable cardinal geometry. |
### book-entry-12 — The Southern Chest

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 37 | `entry-12-chest-section-caption`<br>Editorial section: the baseline is held, one thread rests at the seam, and the after remains unclaimed. | OPENING PLATE | 100% | 2400 | Before/touch/after chest and held thread must arrive as one threshold relation. |
| 38 | `entry-12-footing-caption`<br>Editorial footing studyThe last clear footing before touch. | MEDIUM PLATE | 68% | 1800 | Recoverable footing before touch is a spatial threshold. |
| 39 | `entry-12-condition-field-caption`<br>Editorial condition fieldThe intervention is not outside the field it enters. | FIELD PLATE | 88% | 2200 | Intervention inside the condition it enters requires a stable containing field. |
| 40 | `entry-12-local-field-caption`<br>Editorial localization studyA bounded first condition without a claim to the whole field. | MEDIUM PLATE | 68% | 1800 | Local first condition versus whole field depends on bounded position. |
| 41 | `entry-12-reversible-caption`<br>Editorial consequence pathThe smallest reversible movement that can answer the distinction. | MEDIUM PLATE | 70% | 1800 | Baseline, bounded movement and possible return must stay connected. |
| 42 | `entry-12-footprint-caption`<br>Editorial footprint studyWhat did the touch add to what was later observed? | SIMPLIFY LIVE | 100% | live | Before touch / introduced touch / after touch is a live three-state sequence. |
| 43 | `entry-12-promise-triptych-caption`<br>Editorial promise structureBefore, touch, and after remain separable. | SIMPLIFY LIVE | 100% | live | Before / touch / after can remain three live accountable blocks. |
| 44 | `entry-12-holding-layers-caption`<br>Editorial living baselineSeveral conditions remain near without collapsing together. | FIELD PLATE | 88% | 2200 | Overlapping states, traceable seam and incomplete unknown edge are spatial meaning. |
| 45 | `entry-12-thread-chest-caption`<br>Editorial one-thread chamberOne movement enters consequence while the rest remains held. | MEDIUM PLATE | 72% | 2000 | One active thread against held/unclaimed conditions requires stable geometry. |
| 46 | `entry-12-judgment-latch-caption`<br>Editorial judgment latchPreparation stops before it begins impersonating authorization. | MEDIUM PLATE | 72% | 2000 | Preparation reaching but not crossing the judgment seam is spatial. |
| 47 | `entry-12-artifact-section-caption`<br>Editorial southern carrierA trustworthy before, an inspectable touch, and an answerable after. | SIMPLIFY LIVE | 100% | live | Before/touch/after carrier record is sequential and textual. |
| 48 | `entry-12-meeting-fields-caption`<br>Editorial meeting physicsNo hidden work continues between bounded meetings. | SIMPLIFY LIVE | 100% | live | No hidden work between bounded meetings can be represented live. |
| 49 | `entry-12-threshold-object-caption`<br>Editorial threshold objectSelection, framing, and omission already alter the receiving condition. | SIMPLIFY LIVE | 100% | live | Prepared condition crossing a threshold can be a simple live relation. |
| 50 | `entry-12-return-field-caption`<br>Editorial re-entry fieldRecognition may return. Non-return remains a truthful human choice. | MEDIUM PLATE | 72% | 2000 | Return/non-return possibility is carried by field geometry. |
| 51 | `entry-12-family-field-caption`<br>Editorial family relationOne cardinal gravity within a larger cultivated family. | MEDIUM PLATE | 72% | 2000 | South highlighted within the family requires stable cardinal geometry. |
### book-entry-14 — The Western Tellings

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 52 | `entry-14-passage-registers-caption`<br>Editorial passage field: several tellings travel with different conditions; the ungiven stops before the receiving boundary. | OPENING PLATE | 100% | 2000 | Lived/carried poles, unequal reaches, endpoints, ungiven and peripheral adjacency must stay one field. |
| 53 | `entry-14-peripheral-threshold-caption`<br>Editorial peripheral studyNear enough to recognize; far enough not to possess. | MEDIUM PLATE | 68% | 1800 | Peripheral adjacency outside lived/carried bounds is spatial. |
| 54 | `entry-14-sequence-field-caption`<br>Editorial sequence registerSequence preserves relation without proving cause. | SIMPLIFY LIVE | 100% | live | Sequence with interruption/silence can be a live vertical register. |
| 55 | `entry-14-register-mini-caption`<br>Editorial telling registerEach carried element retains its condition. | SIMPLIFY LIVE | 100% | live | Occurred/witnessed/reported/inferred/arranged/ungiven is a live status register. |
| 56 | `entry-14-recognition-arc-caption`<br>Editorial recognition arcReach may increase only while source and correction remain available. | SMALL PLATE | 55% | 1600 | Recognition/reach arc is spatial but secondary apparatus. |
| 57 | `entry-14-given-boundary-caption`<br>Editorial given/ungiven boundaryInterpretation stops where expression has not been given. | SIMPLIFY LIVE | 100% | live | Given versus ungiven can remain a live two-state stopping boundary. |
| 58 | `entry-14-promise-seams-caption`<br>Editorial authorship seamsEvery word, interpretation, addition, and silence keeps its own relation. | MEDIUM PLATE | 70% | 1800 | Authorship seams depend on separate attachment positions. |
| 59 | `entry-14-holding-caption`<br>Editorial living boundaryThe given remains held; the ungiven remains unavailable without becoming absent. | SIMPLIFY LIVE | 100% | live | Given/correctable versus partly unknown can remain live if the boundary is simple. |
| 60 | `entry-14-shaping-table-caption`<br>Editorial visible seamCarried form and shaping record remain beside one another. | SIMPLIFY LIVE | 100% | live | Carried form and shaping record are naturally tabular/live. |
| 61 | `entry-14-boundary-gate-caption`<br>Editorial stopping boundaryRecognizability stops before it impersonates proof or authorization. | SIMPLIFY LIVE | 100% | live | Source/sequence/ownership versus proof/mechanism/authorization can be a live boundary. |
| 62 | `entry-14-artifact-carrier-caption`<br>Editorial western carrierHuman meaning travels without replacing origin. | SIMPLIFY LIVE | 100% | live | Source/sequence/position/shaping/authority/return is a live ordered carrier register. |
| 63 | `entry-14-meeting-fields-caption`<br>Editorial meeting physicsA later encounter does not inherit intimacy. | SIMPLIFY LIVE | 100% | live | Trace may travel while intimacy does not persist: sequential/live. |
| 64 | `entry-14-receiver-threshold-caption`<br>Editorial encounter thresholdThe receiver meets what arrived without mistaking it for the person or life. | SIMPLIFY LIVE | 100% | live | What arrives versus what it is not is a textual threshold relation. |
| 65 | `entry-14-recognition-return-caption`<br>Editorial present-recognition fieldEarlier expression arrives as trace, not current voice. | SIMPLIFY LIVE | 100% | live | Earlier expression as trace and present confirmation/revision/refusal can stay live. |
| 66 | `entry-14-family-field-caption`<br>Editorial family relationOne cardinal gravity within a larger cultivated family. | MEDIUM PLATE | 72% | 2000 | West highlighted within the family requires stable cardinal geometry. |
### book-entry-17 — One Real Thing Through the Shop

| # | Caption / apparatus | Treatment | Display | Source px | Why |
| --- | --- | --- | --- | --- | --- |
| 67 | `entry-17-white-room-panel-01-caption`<br>Artifact excerpt · White Room panel 01 Outside the White Room, the work is still paper, carts, windows, and buttons. | LIVE | 100% | live | Existing packaged raster identity already survives; preserve live caption/alt. |
| 68 | `entry-17-white-room-panel-10-caption`<br>Artifact excerpt · White Room panel 10 The visible structures are gathered into one grounded run state before human review. | LIVE | 100% | live | Existing packaged raster identity already survives; preserve live caption/alt. |
| 69 | `entry-17-white-room-panel-13-caption`<br>Artifact excerpt · White Room panel 13 The prepared artifact leaves the room as a packet for human review. | LIVE | 100% | live | Existing packaged raster identity already survives; preserve live caption/alt. |

## Promotion rule

`SIMPLIFY LIVE` is not a promise to keep a component live at all costs.

During the full Kindle build:

- if the simplified component remains legible and its relation survives, keep it live;
- if Previewer separates or spatially misstates it, promote that one component to the smallest appropriate plate class;
- do not invent increasingly clever CSS simply to avoid one additional plate.

This is the practical guardrail against both over-rasterizing and over-engineering.

## Build consequence

The next full-build lane can be organized as:

1. **Batch A — existing/rich anchors:** compass, placement, five lens openings, Western field.
2. **Batch B — sparse medium plates:** Jules/North/East/South/West relation studies.
3. **Batch C — small paths/arcs:** secondary apparatus at restrained scale.
4. **Batch D — live simplifications:** sequence/register/meeting/carrier diagrams.
5. **Batch E — family compasses:** one reusable rendering component with lens-specific highlight.

Each batch should report:

- source selector;
- canonical render checksum;
- crop box;
- target display class;
- output dimensions;
- output SHA-256;
- optimized bytes;
- alt/caption/description identity;
- projected cumulative package weight.

## Decision

The plate strategy is **viable enough to engineer**, but the full build should use a plate-budget gate rather than assume image cost.

The apparatus census supports building a reusable adapter: the problem is now classifiable.
