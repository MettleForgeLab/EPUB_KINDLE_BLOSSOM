# BHT MEDIUM PLATE Throughput Cohort 4

Release milestone: 0.13  
Profile: `bht_milestone_007_medium_plate_001.json`

## Governing source

Retail master:

`BHT_RETAIL_RELEASE_CANDIDATE_002.epub`

SHA-256:

`fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae`

The governing master remained unchanged throughout the milestone.

Profile SHA-256:

`3e952299c4b6a45703e57ecc310ba4bb1ae664f68652438d307a201ee3fb3817`

## Components

Six final MEDIUM PLATE components were completed:

- east-provisional-plan
- south-footing
- south-reversible
- south-thread-chest
- south-return-field
- west-promise-seams

## Accepted render treatments

- east-provisional-plan — `east-provisional-plan-render-002.css`
- south-footing — `south-footing-render-001.css`
- south-reversible — `south-reversible-render-002.css`
- south-thread-chest — `south-thread-chest-render-002.css`
- south-return-field — `south-return-field-render-010.css`
- west-promise-seams — `west-promise-seams-render-003.css`

Each component remained at a 100% requested reader-facing footprint. The render-only internal composition width was tuned per component rather than treating MEDIUM PLATE as a single fixed percentage.

## Optimization method standing

All six use:

`palette-256-sparse-editorial`

Method standing:

`ADMITTED METHOD`

No automatic optimization application or promotion was introduced.

## Human graphic review

Porter Winston recorded:

- local graphic review: **PASS**
- Kindle graphic review: **PASS**
- whole-page composition: **NOT_EVALUATED**

for all six exact Palette-256 candidates.

Reviewed Milestone 007 Kindle-test EPUB SHA-256:

`d7c98d1f1bd8c775ff19bdb4562dbdd00699db0c4efca363064a880c8f1c41dd`

The component review boundary intentionally excluded surrounding Kindle-page whitespace, whole-chapter pacing, and final whole-book composition.

## Explicit admissions

All six exact candidates were explicitly admitted by Porter Winston.

| Component | Candidate bytes | Candidate SHA-256 |
| --- | ---: | --- |
| east-provisional-plan | 31,891 | `7c1b30494e65fd957782e12d578dea384f7a0514f4aa4f51f4d22a75ea2e1804` |
| south-footing | 37,453 | `ecf59a6c80d1492af7af53cd1646f194a6235c13bf71d0d9f2128c71ce25fa3f` |
| south-reversible | 38,729 | `a97a4fcb8e566f0bbd457666486e87d89a397e4f1e9f8adc39c62785540df806` |
| south-thread-chest | 45,216 | `662ff920791f7cf68700e4f45c9d12614bc0eeed38959b7bca4f47281f0fdb5c` |
| south-return-field | 41,017 | `2839f0243c6a932a9632ce54ca2ce8ff2b49a1517bdce40deec20436a5cde3b6` |
| west-promise-seams | 55,428 | `c327445bf7cbcb80037fd57ff7de160ed548a4871f3aea5e20efe75d016148d0` |

Combined baseline payload:

`579,218 bytes`

Combined admitted candidate payload:

`249,734 bytes`

Savings:

`329,484 bytes` — approximately `56.9%`

Spatial dimensions were preserved for the admitted candidate of each component.

## Final admitted integration evidence

Run:

`bht_run_078_medium_plate_cohort4_six_admitted`

Probe EPUB:

`MFL_BHT_MEDIUM_PLATE_MILESTONE_007_001.epub`

SHA-256:

`0853b09641aca35ebd01b1faf0f5b4ee2789d18b7d4d24550a5e810c8bd5f004`

The run contains all six explicit admission packets and packages the exact admitted candidate bytes.

Automated build findings:

`0`

Structural package checks:

`passed`

All six post-render device plans reported:

`RESERVE MET`

All six plates remained within their configured byte budgets.

## Diagnostic refinement

The milestone also carries a bounded diagnostic improvement in `mfl_adapter/render.py`:

master-reference overflow failures now receive the component key as a diagnostic label.

This does not change render policy or admission standing. It makes a hard stop identify the component that produced it.

## Release boundary

This milestone establishes:

- exact component-level local graphic acceptance;
- exact component-level Kindle graphic acceptance;
- explicit human-authorized plate admission;
- exact-candidate integrated probe evidence.

It does **not** by itself establish:

- final whole-page composition;
- final whole-book pagination or pacing;
- retail Kindle release acceptance;
- KDP upload or publication.

Those remained separate publication-level gates and were addressed later in the BHT retail-publication line.

No source mutation occurred.
