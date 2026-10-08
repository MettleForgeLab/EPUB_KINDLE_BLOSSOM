# MFL Kindle Visual Adapter

**Current version:** 0.14.0

MFL Kindle Visual Adapter is a custody-first EPUB publication-engineering tool.

It began as a bounded Kindle visual-component adapter and now supports two related scopes:

1. exact-source component probes, optimization review, and explicit plate admission;
2. read-only whole-publication audit for accepted Apple/Kindle EPUBs.

It never publishes, silently rewrites a master, or infers human acceptance.

## Current BHT standing

The repository records evidence from two frozen sibling releases:

- Apple: `BHT_APPLE_EPUB1_RELEASE_001.epub`
- Kindle: `BHT_KINDLE_EPUB1_RELEASE_001.epub`

The binaries remain outside tracked Git by default.

See:

- `docs/README.md`
- `docs/BHT_SHARED_PUBLICATION_PLAYBOOK_002.md`
- `docs/BHT_ONE_SOURCE_TWO_RETAIL_BOOKS_001.md`
- `docs/BHT_FROZEN_RELEASE_PROVENANCE_001.md`

## Install locally

```powershell
Set-Location -LiteralPath "C:\MFL Kindle Visual Adapter"

& ".\Install-Local.ps1"
```

## Run tests

```powershell
& ".\.venv\Scripts\python.exe" -m pytest -q
```

Three exact BHT integration tests may skip unless `MFL_TEST_MASTER` and/or `MFL_TEST_RUN` are set.

## Inspect a component profile

```powershell
& ".\.venv\Scripts\python.exe" `
    -m mfl_adapter `
    inspect `
    --epub "C:\path\to\master.epub" `
    --profile ".\profiles\bht_milestone_007_medium_plate_001.json" `
    --out "C:\path\to\fresh-run"
```

## Audit a frozen whole publication

```powershell
& ".\.venv\Scripts\python.exe" `
    -m mfl_adapter `
    audit-publication `
    --epub "C:\path\to\BHT_KINDLE_EPUB1_RELEASE_001.epub" `
    --policy ".\profiles\bht_frozen_releases_001.json" `
    --platform "kindle" `
    --out "C:\path\to\BHT_KINDLE_RELEASE_001_AUDIT.json"
```

The audit reports package/policy standing only.

It explicitly does not infer native-renderer review or human acceptance.

## Run external validation

```powershell
& ".\.venv\Scripts\python.exe" `
    -m mfl_adapter `
    validate `
    --epub "C:\path\to\book.epub" `
    --out "C:\path\to\fresh-validation-run"
```

The repository-local defaults are:

- Temurin Java 21;
- EPUBCheck 5.4.0;
- Ace by DAISY 1.4.6.

## Evidence boundaries

Keep separate:

- source authority;
- component engineering;
- whole-publication package audit;
- EPUBCheck;
- Ace;
- Apple/Kindle native review;
- human acceptance;
- retailer ingestion;
- post-publication smoke check.

A clean result in one layer does not silently promote another.

## Publication principle

> Make the semantic anatomy explicit, then give each renderer only as much additional structure as it has earned.
