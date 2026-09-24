# BHT MEDIUM PLATE Class Expansion 001

**Date:** 2026-09-24  
**Milestone:** MFL Kindle Visual Adapter 0.10  MEDIUM PLATE Class Expansion

**Governing retail master SHA-256:** `fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae`

**Final profile:** `profiles/bht_milestone_004_medium_plate_001.json`  
**Final profile SHA-256:** `d6e66db60f209f517b17d4327900f16bd69dea165ade4626def85d39f3d5866b`

**Integrated admitted run:** `bht_run_045_four_medium_plate_admitted`  
**Integrated EPUB:** `MFL_BHT_MEDIUM_PLATE_MILESTONE_004_001.epub`  
**Integrated EPUB SHA-256:** `3830339dc5741e536bc874848178be64df055ce5c50dc0cf59a19801cfbf1ebb`

## Cohort

This milestone established the first new four-component MEDIUM PLATE cohort:

- East Relation Study
- South Local Field
- Jules Field Map
- North Field Plane

All four final RGB compositions received local graphic PASS.
All four final Palette-256 candidates received local graphic PASS and Kindle graphic PASS.
The integrated four-admission build subsequently received an integrated Kindle smoke PASS.

Whole-page composition and whole-book retail pacing remain separate acceptance gates.

## Final admitted plates

| Component | Optimization method | RGB bytes | Admitted bytes | RGB SHA-256 | Admitted SHA-256 |
|---|---|---:|---:|---|---|
| east-relation-study | palette-256-sparse-editorial | 96,678 | 36,957 | `54699be44050025564df27039060460d8fbfd11b8868cdeffa593498a67da66c` | `708b32332554bdba3349e12a34c1079606ff269421df8720cac2ee67c15bb960` |
| south-local-field | palette-256-sparse-editorial | 71,853 | 32,939 | `fb5e9b133a18115b074f9231bb1e2ccdeb387372d167bd134e7f2d74c10d0c7c` | `e455534222e9338214e9ae3cc439754d7bec3e6f30f085916e3045ccb6359adb` |
| jules-field-map | palette-256-structured-editorial-field | 162,544 | 66,900 | `55fc7eb635ae6944aaf310943e48f91a98ebb6f92cb9dcf4823d1ba35077c815` | `cbdbe26d877f81b85d8876751503aa98f62b2e5d63d0dc2d1a2fe3d82563e05c` |
| north-field-plane | palette-256-structured-editorial-field | 161,260 | 68,858 | `f53b4ef8d86820789e9ffec1eb69f2ca557ce7b3e20b593b548686cc2fb89b73` | `cfc765089df79a573812e493e1a05ef8ae7a749f21330c29f72bef9b10939149` |

Combined RGB payload: **492,335 bytes**

Combined admitted Palette-256 payload: **205,654 bytes**

Combined savings: **286,681 bytes (58.2%)**

## Optimization-method boundary

Two explicit method classes coexist in this milestone.

### `palette-256-sparse-editorial`

Plate class: `SPARSE EDITORIAL PLATE`

Used for:

- East Relation Study
- South Local Field

### `palette-256-structured-editorial-field`

Plate class: `STRUCTURED EDITORIAL FIELD`

Used for:

- Jules Field Map
- North Field Plane

The two methods use the same deterministic Palette-256 encoding implementation but have different semantic scopes.

Candidate encoding identity does not determine semantic method identity.

The legacy `palette-256` review path remains backward-compatible with `palette-256-sparse-editorial`; structured editorial fields require an explicit method selection.

Neither method permits automatic application or automatic promotion.

## Composition and footprint findings

MEDIUM PLATE is a semantic treatment class, not a fixed display percentage.

Final treatments included:

- East Relation Study: enlarged internal no-arrow text and explicitly bounded visual overflow.
- South Local Field: larger reader-facing footprint, reserve-compliant source width, larger labels, and a deliberate boundary-near placement for `what remains outside`.
- Jules Field Map: larger reader-facing footprint, reserve-compliant source width, larger labels, and an enlarged central `present distinction` circle.
- North Field Plane: larger reader-facing footprint, reserve-compliant source width, enlarged labels, and preserved center/outer-field geometry.

Reader-facing footprint and typography solve legibility.
Source-pixel width separately solves device reserve.

## Renderer diagnostics

Overflow failures now report measured root and visible bounds.

Bounded visual overflow remains explicit and component-specific. It is not a generic escape hatch.

The renderer safety ceiling remains unchanged.

## Admission boundaries

- admitted method does not automatically admit a candidate;
- encoding candidate does not silently define semantic method class;
- local PASS does not imply Kindle PASS;
- human PASS does not override automatic technical checks;
- admission does not imply final whole-publication acceptance;
- no candidate is automatically promoted;
- admitted replacements remain locked to exact profile, review, baseline, candidate, method, and human authorization identities.

## Automated validation

Final admitted EPUB:

- internal package verifier: PASS
- EPUBCheck: PASS
- Ace automated accessibility: PASS
- validation exit: 0
- accessibility certification/conformance: NOT CLAIMED

## Integrated Kindle review

The final four-admission EPUB received an integrated Kindle smoke PASS.

The smoke review confirmed coexistence and integrity of the four admitted MEDIUM PLATE components. It does not constitute final whole-book retail composition or pacing acceptance.

## Authority

Porter Winston remains human acceptance authority.
