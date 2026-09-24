# Changelog

## 0.6.0  2026-09-23

- Added a review-only plate optimization laboratory.
- Added full-resolution deterministic Palette-256 as an admitted optimization method for sparse editorial plates.
- Kept optimization application and candidate promotion explicitly non-automatic.
- Defined the component-probe graphic review zone to include all typography inside a plate, relational geometry, crop, negative space, color, tone, and encoding artifacts.
- Explicitly excluded surrounding Kindle page whitespace and whole-book pacing from isolated graphic acceptance.
- Added human review records distinguishing local graphic review, Kindle graphic review, and whole-page composition.
- Added candidate eligibility rules requiring preserved dimensions, smaller file size, device reserve, and human graphic PASS locally and in Kindle.
- Verified Jules Motion repair 004 locally and in Kindle Previewer.
- Reduced the reviewed Motion plate from 215,943 bytes to 82,897 bytes with Palette-256 while retaining full 18002198 spatial resolution and device reserve.
- Recorded Motion repair 004 Palette-256 as ELIGIBLE_FOR_PLATE_ADMISSION; publication replacement remains separate and unperformed.

## 0.5.0  2026-09-23

- Added reproducibility evidence and runtime fingerprinting.
- Added byte-for-byte EPUB comparison with member-payload and ZIP-metadata diagnostics.
- Added REPRODUCIBILITY.json to generated runs.
- Recorded Python, platform, zlib, browser, Playwright, Pillow, and lxml runtime boundaries.
- Verified independent Windows builds produce identical EPUB bytes and SHA-256 when source, profile, code, and recorded runtime are held constant.
- Preserved an explicit boundary: cross-runtime and cross-platform byte identity are not claimed without separate evidence.
- Confirmed EPUB mimetype remains first and uncompressed.
- Left the existing deterministic EPUB writer unchanged because it already satisfied the reproducibility contract.

## 0.4.0  2026-09-23

- Added named Kindle physical-pixel planning profiles.
- Added MFL device-resolution reserve policy without asserting CSS viewport equivalence.
- Added pre-render plate-width planning and hard stop for under-resolved plates.
- Added post-render device planning against actual generated plates.
- Added byte-budget states: WITHIN BUDGET, NEAR BUDGET, and OVER BUDGET.
- Integrated DEVICE_PLAN_PRE.json, DEVICE_PLAN_POST.json, and BUILD_FINDINGS.json into component builds.
- Preserved the 0.3 plate_pixel_report compatibility API.
- Verified the second BHT component batch across Paperwhite 6, Colorsoft, and Scribe 3 planning targets.

## 0.3.0  2026-09-23

- Established the live Windows development baseline.
- Added deterministic PNG normalization for generated plates.
- Added accessibility discovery metadata and ARIA navigation repair.
- Integrated EPUBCheck 5.4.0 as an external conformance gate.
- Integrated Ace by DAISY 1.4.6 as an automated accessibility gate.
- Added unified validation reporting with explicit separation between
  automated validation, Kindle Previewer evidence, human acceptance,
  and accessibility certification/conformance.
- Verified reproducible package member payloads across independent
  Windows builds.
- Preserved source authority and bounded-probe custody throughout.

## 0.2.0 — 2026-09-23

- Added vertical-footprint planning for plate + caption + description-link bundles.
- Added measured bundle verification at the reference viewport.
- Added budget-gated keep-together eligibility.
- Added per-component minimum display-width refusal.
- Effective label size is now computed at the planned display footprint.
- Added explicit bounded visual-overflow capture.
- Added profile-driven `SIMPLIFY LIVE` sequences.
- Added opt-in SVG-local IDs for plate geometry.
- Generalized component probe profiles beyond the original hard-coded four-case mode.
- Added second BHT component batch:
  - Jules Gravity — MEDIUM PLATE
  - Jules Motion — SMALL PLATE
  - East Promise stack — SIMPLIFY LIVE
  - South Judgment Latch — MEDIUM PLATE
- Preserved the 0.1 probe and added an explicit 0.1 regression wrapper.
- Expanded automated tests to 31 passing tests with the delivered BHT integration run.

Human Kindle acceptance remains open.
