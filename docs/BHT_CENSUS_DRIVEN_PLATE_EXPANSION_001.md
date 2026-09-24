# BHT Census-Driven Plate Expansion 001

**Date:** 2026-09-24
**Milestone:** MFL Kindle Visual Adapter 0.9  Census-Driven Plate Expansion

**Governing retail master SHA-256:** `fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae`

**Final profile:** `profiles/bht_milestone_003_small_plate_002.json`
**Final profile SHA-256:** `c280d7d57e5ef5da6dfec6127df0a10e41032ef7e77f1239e56885f34ec25597`

**Integrated admitted run:** `bht_run_032_three_small_plate_admitted`
**Integrated EPUB:** `MFL_BHT_SMALL_PLATE_MILESTONE_003_002.epub`
**Integrated EPUB SHA-256:** `02e607c771947dd9a97149c56f88dc37e62d542bf10ed7e2f0907e4d466bada7`

## Scope

This milestone expanded the previously admitted sparse-editorial Palette-256 method to the three remaining SMALL PLATE census candidates:

- Jules Return
- North Return Arc
- West Recognition Arc

Together with Jules Motion from the earlier milestone, all four SMALL PLATE census items have now been exercised through the human-governed workflow.

## Final admitted plates

| Component | RGB bytes | Admitted bytes | RGB SHA-256 | Admitted SHA-256 |
|---|---:|---:|---|---|
| Jules Return | 82,843 | 33,550 | `019d328a45f86c803abba5d38cc22aeafe5b9e2f4c793b67bf58ff0445f2f3cb` | `80ed6254c898148732de35557f3c49bd16aa156db5e3570b28197bbdc02428b2` |
| North Return Arc | 88,791 | 35,846 | `2aaee3eec5e6120a9d70d1ce3de70f458f9ea5862908bbea35a8a0c105a42591` | `3b290d6e0dccbb09533061efdf06950b2ad4b98e733869a29f9e04a86d81f264` |
| West Recognition Arc | 123,178 | 51,797 | `92c2342c71c25192de7ee7bcab9f29b1c8a46c9c1ffd46b3396fe6ba17dde6b6` | `8e3940d1e15db06aba5967c48ce22a06dbbe66ef20129f0f44f1cdb81a7fa310` |

Combined RGB payload: 294,812 bytes.

Combined admitted Palette-256 payload: 121,193 bytes.

Combined savings: 173,619 bytes, approximately 58.9%.

## Human graphic review

All three final candidates received:

- local graphic: PASS
- Kindle graphic: PASS
- whole-page composition: NOT_EVALUATED

The integrated three-admission run subsequently received an integrated Kindle smoke PASS.

That smoke review confirmed coexistence and integrity of the admitted components. It does not constitute final whole-book retail composition or pacing acceptance.

## North Return Arc reserve repair

North Return Arc required a separate reserve-compliant final baseline.

Final characteristics:

- source width: 1987 px
- device reserve: MET
- reader-facing footprint: 80%
- top relation label centered
- endpoint labels separated
- Palette-256 candidate preserves the accepted composition

The earlier 1600 px candidate remains rejected because it did not meet the selected-device 1.25x reserve requirement.

## Renderer capability learned in 0.9

Plate visual roots may be HTML or SVG.

HTML-root displayed text continues to use browser `innerText`.

SVG-root displayed text uses `textContent`.

Required plate labels must belong to the routed visual itself. Live figcaption prose remains live and is not rasterized merely to satisfy a plate assertion.

## Footprint lesson

SMALL PLATE is a semantic treatment class, not a fixed display percentage.

Reader-facing footprint may increase when necessary to meet effective-label requirements while preserving the relational proposition. Increased source-pixel width is a separate control used for physical device reserve.

## Admission boundaries

The following distinctions remain explicit:

- admitted method does not automatically admit a candidate;
- local PASS does not imply Kindle PASS;
- human PASS does not override failed automatic reserve checks;
- admission does not imply whole-publication acceptance;
- no candidate is automatically promoted;
- every admitted replacement remains locked to exact profile, review, baseline, candidate, and human authorization identities.

## Automated validation

Final admitted EPUB:

- internal package verifier: PASS
- EPUBCheck: PASS
- Ace automated accessibility: PASS
- validation exit: 0
- accessibility certification/conformance: NOT CLAIMED

## Authority

Porter Winston remains human acceptance authority.
