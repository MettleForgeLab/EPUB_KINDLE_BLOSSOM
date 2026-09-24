# Changelog

## 0.10.0  2026-09-24

- Expanded the census-driven workflow into the first new four-component MEDIUM PLATE cohort.
- Finalized East Relation Study, South Local Field, Jules Field Map, and North Field Plane treatments.
- Added component-specific bounded-overflow diagnostics with measured root and visible bounds.
- Demonstrated that MEDIUM PLATE is a semantic class rather than a fixed display percentage.
- Preserved separate controls for reader-facing footprint, typography, and physical device reserve.
- Added `palette-256-structured-editorial-field` as an explicit admitted method for denser multi-label editorial fields.
- Preserved backward compatibility for legacy Palette-256 sparse-editorial reviews.
- Added explicit `--method` selection to plate-review recording.
- Added regression coverage for default sparse method selection, explicit structured-field selection, and incompatible candidate/method rejection.
- Applied `palette-256-sparse-editorial` to East Relation Study and South Local Field.
- Applied `palette-256-structured-editorial-field` to Jules Field Map and North Field Plane.
- Reduced the four-plate payload from 492,335 bytes to 205,654 bytes, approximately 58.2%.
- Created four explicit human-authorized admission packets bound to the final profile identity.
- Built and validated a four-admission MEDIUM PLATE probe containing the exact admitted candidate bytes.
- Completed an integrated Kindle Previewer smoke PASS for the final four-admission probe.
- Preserved whole-page composition and whole-book retail pacing as separate acceptance gates.

## 0.9.0  2026-09-24

- Expanded the census-driven SMALL PLATE workflow to Jules Return, North Return Arc, and West Recognition Arc.
- Added SVG-root plate text support while preserving HTML-root innerText behavior.
- Preserved live figcaption prose outside raster plates and corrected plate-label assertions to follow the routed visual boundary.
- Demonstrated that SMALL PLATE is a semantic treatment class rather than a fixed reader-facing percentage.
- Added effective-label-driven footprint repairs and separate device-reserve source-width planning.
- Finalized a centered, reserve-compliant 1987px North Return Arc treatment.
- Applied the admitted full-resolution Palette-256 sparse-editorial method to all three new plates after local and Kindle review.
- Reduced the three-plate payload from 294,812 bytes to 121,193 bytes, approximately 58.9%, without reducing the accepted spatial resolution.
- Created explicit human-authorized admission packets bound to the final profile identity.
- Built and validated a three-admission probe containing the exact admitted candidate bytes.
- Completed an integrated Kindle Previewer smoke PASS for the final three-admission probe.
- Preserved whole-page composition and whole-book retail pacing as separate acceptance gates.
- Added regression coverage for displayed-text extraction from both HTML- and SVG-root plate visuals.

## 0.8.0  2026-09-23

- Added explicit multi-component batch optimization review.
- Added a single batch review surface while preserving per-plate human judgment and admission.
- Kept component selection explicit; no automatic batch optimization or promotion.
- Verified full-resolution Palette-256 on Jules Gravity, Jules Motion repair 004, and South Judgment Latch.
- Recorded local graphic PASS and Kindle graphic PASS for all three sparse editorial plates.
- Explicitly admitted all three reviewed Palette-256 candidates.
- Built and validated a three-admission probe containing the exact authorized candidate assets.
- Reduced the three-plate payload from 635,651 bytes to 271,414 bytes, approximately 57.3%, without reducing spatial resolution.
- Completed an integrated Kindle Previewer smoke PASS for the three-admission probe.
- Preserved whole-page composition and whole-book pacing as separate, unevaluated retail-publication gates.
- Preserved non-automatic optimization, review, promotion, and admission boundaries.

## 0.7.0  2026-09-23

- Added explicit human-authorized plate admission packets.
- Separated optimization-method admission, candidate eligibility, and publication admission into distinct states.
- Added exact profile, review, baseline, candidate, method, and authorization SHA custody.
- Added build-probe --admission support with hard stops on any identity mismatch.
- Added self-contained admission evidence preserving both rendered RGB baseline and admitted candidate.
- Added build-time replacement only after the exact profile-governed baseline is rendered and verified.
- Added admission evidence to render metrics and MANIFEST.json.
- Added build-command integration testing preventing admission arguments from being silently ignored.
- Admitted Jules Motion repair 004 Palette-256 under explicit Porter Winston authorization.
- Verified the packaged EPUB contains the exact 82,897-byte admitted candidate SHA-256 314f2c6d2e5533f8bcc9aad4c40db0dac36efb61afe4741e658f162ec091bfab.
- Preserved whole-page Kindle composition as a separate, unevaluated gate.

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
