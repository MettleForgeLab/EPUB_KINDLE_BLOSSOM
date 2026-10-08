# MFL Kindle Visual Adapter — Documentation Map

## Current operating documents

Read these first:

1. `SOURCE_BASIS.md` — authority, custody, and immutable identities.
2. `IMPLEMENTATION_BOUNDARIES.md` — what the adapter can and cannot claim.
3. `BHT_SHARED_PUBLICATION_PLAYBOOK_002.md` — current shared Apple/Kindle build method.
4. `BHT_ONE_SOURCE_TWO_RETAIL_BOOKS_001.md` — comparative record of the completed parallel builds.
5. `BHT_FROZEN_RELEASE_PROVENANCE_001.md` — exact common-source, release, cover, and asset identities.
6. `BHT_PUBLICATION_RECONCILIATION_EVIDENCE_001.json` — machine-readable evidence.
7. `PUBLICATION_AUDIT.md` — whole-publication audit command and policy model.
8. `PLATFORM_REVIEW_CARD.md` — native renderer and whole-book review surface.
9. `ROADMAP.md` — next work after the frozen BHT releases.

## Lineage documents

Preserve these as historical evidence:

- `BHT_SHARED_PUBLICATION_PLAYBOOK_001.md` — October 5 architecture used to guide the clean reruns; superseded for future work by Playbook 002.
- `MFL_KINDLE_VISUAL_ADAPTER_TOOL_SPEC_001.md`
- `MFL_KINDLE_VISUAL_ADAPTER_TOOL_SPEC_002.md`
- `README_0_2.md`
- component census, batch, and milestone records.

Historical OPEN fields remain true for the scope and moment of those records. They do not reverse later release acceptance.

## Component milestone records

- `BHT_KINDLE_APPARATUS_CENSUS_001.md`
- `BHT_BATCH_OPTIMIZATION_REVIEW_001.md`
- `BHT_CENSUS_DRIVEN_PLATE_EXPANSION_001.md`
- `BHT_MEDIUM_PLATE_CLASS_EXPANSION_001.md`
- `BHT_MEDIUM_PLATE_THROUGHPUT_COHORT_002.md`
- `BHT_MEDIUM_PLATE_THROUGHPUT_COHORT_003.md`
- `BHT_MEDIUM_PLATE_THROUGHPUT_COHORT_004.md`

These establish component engineering and admission evidence. Whole-publication acceptance is recorded separately.

## Validation evidence model

The project keeps separate:

- internal package audit;
- EPUBCheck;
- Ace;
- native renderer/import evidence;
- human visual/accessibility judgment;
- retailer ingestion;
- post-publication smoke check.

No evidence type silently upgrades another.

## Frozen BHT release identities

Apple:

`BHT_APPLE_EPUB1_RELEASE_001.epub`
`40ffe038e163a818335af9ba65a1380e84bb5cbfa69ac5eef11d1dc23781757b`

Kindle:

`BHT_KINDLE_EPUB1_RELEASE_001.epub`
`225592b811b301200e9477e172269a0099152f1f94701a20bfcfc5961088c9d7`

The binaries remain outside tracked Git by default.
