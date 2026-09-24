# BHT Batch Optimization Review 001

**Date:** 2026-09-23  
**Milestone:** MFL Kindle Visual Adapter 0.8  Batch Optimization Review  
**Governing retail master SHA-256:** `fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae`  
**Profile:** `profiles/bht_milestone_002_motion_repair_004.json`  
**Integrated admitted probe:** `bht_run_018_three_palette_admitted`  
**Integrated EPUB SHA-256:** `fbdef07e4cf02fbb2ef916ce3aadbb6dca6676a1d3deeb4c2c6bd187f8ba4cdc`

## Admitted optimization method

`palette-256-sparse-editorial`

Full-resolution deterministic Palette-256, no dithering.

The method is admitted for sparse editorial plates subject to per-plate local graphic review, Kindle graphic review, and explicit human admission. Application and promotion remain non-automatic.

## Admitted plates

| Component | Baseline bytes | Admitted bytes | Admitted SHA-256 | Local graphic | Kindle graphic |
|---|---:|---:|---|---|---|
| Jules Gravity | 82,569 | 30,579 | `73e0e632eb1e77c15988c6298c33d02d1bd14b1bad6afedbd15fc87ad4cf141e` | PASS | PASS |
| Jules Motion repair 004 | 215,943 | 82,897 | `314f2c6d2e5533f8bcc9aad4c40db0dac36efb61afe4741e658f162ec091bfab` | PASS | PASS |
| South Judgment Latch | 337,139 | 157,938 | `e935343dd011bee77e41883bcb41191947593b082721004c155a3b0958101bb0` | PASS | PASS |

Combined plate payload:

- RGB baselines: 635,651 bytes
- admitted Palette-256 plates: 271,414 bytes
- savings: 364,237 bytes
- reduction: approximately 57.3%

All three retain full spatial resolution and device reserve.

## Integrated Kindle smoke review

`bht_run_018_three_palette_admitted` received an integrated Kindle Previewer smoke PASS.

Observed scope:

- conversion and presentation remained healthy;
- Gravity remained intact;
- Motion repair 004 remained intact;
- South Judgment Latch remained intact;
- no new plate-specific visual degradation was observed.

This smoke review does **not** constitute acceptance of the final whole-book page composition or retail pacing. Surrounding Kindle-page whitespace and whole-book rhythm remain separate integrated-publication concerns.

## Automated validation

The three-admission EPUB received:

- internal package verifier: PASS
- EPUBCheck: PASS
- Ace automated accessibility: PASS
- automated validation exit: 0

## Authority

Porter Winston remains human acceptance authority.

No optimization method automatically changes a publication.  
No eligible candidate is automatically admitted.  
Every admitted plate remains locked by exact review, candidate, baseline, profile, method, and authorization identity.
