# MFL Kindle Visual Adapter 0.2

**Second runnable engineering increment. Not a production Kindle converter.**

This release adds two things to the 0.1 milestone:

1. a **vertical-footprint budget** for plate + live caption + extended-description-link bundles; and
2. a **second four-component batch** testing medium, small, and live-simplified apparatus beyond the original compass/Field/Crossing/White Room set.

The authorized retail EPUB remains immutable. The adapter still produces isolated engineering probes, not a full Kindle edition.

## Start with the included second-batch result

Open:

`examples/bht_run_002/MFL_BHT_SECOND_BATCH_PROBE_001.epub`

in Kindle Previewer.

Review these four cases:

1. **Jules Gravity — MEDIUM PLATE**
2. **Jules Motion — SMALL PLATE**
3. **East Promise attachment stack — SIMPLIFY LIVE**
4. **South Judgment Latch — MEDIUM PLATE**

Read `examples/bht_run_002/RUN_RECORD.md` for exact transformations, byte measurements, footprint budgets, and boundaries.

The original 0.1 four-case run remains under `examples/bht_run_001` for regression/reference.

## What changed in 0.2

### Vertical-footprint budget

A plate is no longer sized only by horizontal width.

For a configured reference viewport the adapter now reserves space for:

- the live caption;
- the visible extended-description link;
- breathing room.

It calculates a maximum plate width compatible with that vertical budget, then re-checks the assembled bundle in Chromium.

A plate bundle receives `break-inside/page-break-inside: avoid` **only when the configured engineering budget says the whole bundle fits**.

If the required shrink would take a component below its profile-specific minimum display width, the build stops rather than silently producing an unreadable plate.

This is an engineering guardrail, not a claim about Kindle pagination. Kindle Previewer and human review still control acceptance.

### Explicit visual-overflow capture

Some accepted apparatus intentionally places a label just outside the root visual box. 0.2 can capture that overflow only when the routing profile explicitly authorizes it and the overflow remains within a safety bound.

This is used by the South Judgment Latch. Arbitrary overflow remains a build error.

### Generalized live simplification

`SIMPLIFY LIVE` is now profile-driven rather than hard-coded to Jules Crossing.

The second batch converts East's source/scope/qualification/transformation/status/responsibility-and-return attachment stack into live ordered blocks while preserving the source excerpt and live caption.

### Safe SVG-local IDs

Plate routing may explicitly allow IDs that exist only inside local SVG geometry (for example a marker definition). IDs, links, source identities, and editorial identities outside that bounded SVG exception still stop plate routing.

## Required presentation authority

`BHT_RETAIL_RELEASE_CANDIDATE_002.epub`

SHA-256:

```text
fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae
```

Packaged `OEBPS/book.xhtml` SHA-256:

```text
4361a05443dac8dd1218625c215f67b47ac9a5c59190776abf5621ca14b96a65
```

The retail master is not bundled.

Do not substitute Editorial Pass 002, a prior Kindle prototype, or a similarly named EPUB.

## Windows setup

Requirements: Python 3.11+, PowerShell, and Chromium installed through Playwright or supplied explicitly.

```powershell
Set-Location "C:\MFL-BHT Field Guide\Publishing BHT\Kindle-How To KINDLE an E-Book\MFL_KINDLE_VISUAL_ADAPTER_0_2"
.\Install-Local.ps1
```

If PowerShell policy blocks scripts, use:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[test]"
.\.venv\Scripts\python.exe -m playwright install chromium
```

The build renders locally and aborts external browser resource requests. It does not upload the manuscript or invoke an image-generation service.

## Build the second-batch probe

```powershell
$master = Read-Host "Full path to BHT_RETAIL_RELEASE_CANDIDATE_002.epub"

.\Run-BHT-Probe.ps1 `
  -Master $master `
  -Output ".\runs\bht_milestone_002"
```

`Run-BHT-Probe.ps1` now selects `profiles\bht_milestone_002.json`.

For regression against the original milestone, use:

```powershell
.\Run-BHT-Probe-001.ps1 `
  -Master $master `
  -Output ".\runs\bht_milestone_001_regression"
```

Python equivalent for the second batch:

```powershell
.\.venv\Scripts\python.exe -m mfl_adapter build-probe `
  --epub $master `
  --profile ".\profiles\bht_milestone_002.json" `
  --out ".\runs\bht_milestone_002"
```

Existing output folders are refused rather than overwritten.

## Independent verification

```powershell
.\Verify-BHT-Probe.ps1 `
  -Master $master `
  -Run ".\runs\bht_milestone_002"
```

Verification reopens the generated EPUB, checks the manifest/checksums, resolves local links and accessibility IDREFs, and compares included source-copy regions and captions with the authoritative retail master.

## Automated tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests
```

To include BHT integration tests:

```powershell
$env:MFL_TEST_MASTER = $master
$env:MFL_TEST_RUN = (Resolve-Path ".\examples\bht_run_002").Path
.\.venv\Scripts\python.exe -m pytest -q tests
```

The delivered 0.2 integration run passes **31 tests**.

## Second-batch measured result

| Case | Route | Plate dimensions | Selected bytes | Planned display width at 320px reference |
|---|---|---:|---:|---:|
| Jules Gravity | MEDIUM PLATE | 2000 × 1500 | 89,731 | 72% |
| Jules Motion | SMALL PLATE | 1800 × 2198 | 201,871 | 62% |
| East Promise stack | SIMPLIFY LIVE | live | 0 new plate bytes | live |
| South Judgment Latch | MEDIUM PLATE | 2000 × 1156 | 344,822 | 72% |

New selected plates combined: **636,424 bytes**.

At the 320×800 reference viewport, the measured image/caption/link bundles are approximately:

- Gravity: 315 px high
- Motion: 324 px high
- Judgment Latch: 223 px high

against a configured 576 px bundle-height budget.

Those measurements are local Chromium evidence—not Kindle Previewer results.

## What 0.2 still does not do

It does not:

- transform the complete BHT book;
- automatically classify all 69 figures;
- infer authorial/aesthetic acceptance;
- guarantee plate/caption adjacency in Kindle;
- solve the full-book blank-page behavior;
- perform Kindle Previewer conversion;
- make KDP submissions;
- calculate retailer economics;
- make rights/provenance decisions.

## Next review

Open the included second-batch EPUB in Kindle Previewer.

The primary questions are:

1. Do the Gravity plate, its caption, and its description link remain associated?
2. Does the Motion apparatus remain visually secondary rather than becoming a page-sized monument?
3. Does the East Promise stack still carry its answerability relation as live ordered structure?
4. Does the Judgment Latch keep the seam, latch, refusal line and subdued right-side field together?
5. Does the new keep-together treatment avoid creating blank pages?

If those pass, the vertical-footprint mechanism is ready to become part of the broader component-batch pipeline.
