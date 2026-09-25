# BHT MEDIUM PLATE Throughput Cohort 3

Release milestone: 0.12
Profile: `bht_milestone_006_medium_plate_001.json`

## Governing source

Retail master:

`BHT_RETAIL_RELEASE_CANDIDATE_002.epub`

SHA-256:

`fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae`

The governing master remained unchanged throughout the milestone.

## Components

Six MEDIUM PLATE components were completed:

- north-family-field
- east-family-field
- south-family-field
- west-family-field
- east-disappearance-study
- west-peripheral-threshold

## Accepted treatments

The four family fields use the shared structured family-field treatment
with reduced typography and reader-facing breathing room:

- north-family-field  `north-family-field-render-002.css`
- east-family-field  `east-family-field-render-002.css`
- south-family-field  `south-family-field-render-003.css`
- west-family-field  `west-family-field-render-003.css`

East Disappearance Study uses:

- `east-disappearance-study-render-002.css`

West Peripheral Threshold uses:

- `west-peripheral-threshold-render-001.css`

Superseded render-only CSS experiments are retained under the 0.12 archive.

## Optimization method standing

STRUCTURED EDITORIAL FIELD:

- north-family-field
- east-family-field
- south-family-field
- west-family-field

Method:

`palette-256-structured-editorial-field`

SPARSE EDITORIAL PLATE:

- east-disappearance-study
- west-peripheral-threshold

Method:

`palette-256-sparse-editorial`

All six Palette-256 candidates passed local human graphic review and
Kindle Previewer graphic review before explicit admission.

## Admitted candidate sizes

- north-family-field  78,111 bytes
- east-family-field  78,263 bytes
- south-family-field  77,360 bytes
- west-family-field  77,994 bytes
- east-disappearance-study  34,330 bytes
- west-peripheral-threshold  29,648 bytes

Combined admitted candidate payload:

375,706 bytes.

## Final admitted build

Run:

`bht_run_060_six_medium_plate_admitted`

EPUB:

`MFL_BHT_MEDIUM_PLATE_MILESTONE_006_001.epub`

SHA-256:

`2f6a64ebbe0791f031b282164cccb978b420a2d5abe060fee03a8e147c3b0087`

Explicit plate admissions:

6

Integrated Kindle smoke:

PASS

Human acceptance authority:

Porter Winston

## Release boundary

This milestone establishes component-level and integrated Kindle acceptance
for these six admitted plates.

Whole-publication pagination and composition remain NOT EVALUATED here.
They remain a later publication-wide gate, including early breaks, blank
areas, caption adjacency, orphaning, keep-together behavior, and overall
reader pacing.

## Pre-freeze regression

`103 passed`

No source mutation occurred.
No publication/upload action occurred.
