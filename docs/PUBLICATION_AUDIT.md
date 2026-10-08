# Whole-publication audit

MFL Kindle Visual Adapter 0.14 adds a read-only publication audit for exact Apple/Kindle EPUBs.

The audit complements, but does not replace:

- EPUBCheck;
- Ace;
- Apple/Kindle native review;
- Porter or another named human acceptance;
- retailer ingestion.

## Command

```powershell
& ".\.venv\Scripts\python.exe" `
    -m mfl_adapter `
    audit-publication `
    --epub "C:\path\to\book.epub" `
    --expected-sha256 "<64-hex-sha256>" `
    --out "C:\path\to\PUBLICATION_AUDIT.json"
```

With a policy:

```powershell
& ".\.venv\Scripts\python.exe" `
    -m mfl_adapter `
    audit-publication `
    --epub "C:\path\to\BHT_KINDLE_EPUB1_RELEASE_001.epub" `
    --policy ".\profiles\bht_frozen_releases_001.json" `
    --platform "kindle" `
    --out "C:\path\to\BHT_KINDLE_RELEASE_001_AUDIT.json"
```

The policy supplies the expected frozen SHA-256, so `--expected-sha256` is optional in the second form.

## What it checks

Always:

- explicit EPUB SHA-256 custody;
- ZIP integrity;
- `mimetype` first and uncompressed;
- strict XML/XHTML parse;
- manifest resources;
- spine idrefs;
- duplicate IDs;
- local resources and fragments;
- ARIA IDREFs;
- extended local IDREFs including `headers`, `for`, `aria-controls`, `aria-details`, `aria-flowto`, and `aria-owns`;
- known media-type / filename-extension agreement;
- exactly one `cover-image` manifest item;
- input unchanged after audit.

When a policy is supplied:

- exact filename, hash, and byte size;
- exact member, manifest, and spine counts;
- exact spine order;
- exact TOC labels/destinations;
- exact landmarks;
- required/forbidden members;
- forbidden member families;
- platform asset hashes, byte sizes, dimensions, and media types;
- expected platform stylesheets;
- required source/release wording;
- forbidden historical or production-residue wording.

## Result standing

The report says:

```text
renderer_review: NOT INFERRED
human_acceptance: NOT INFERRED
```

A `PASS` means the exact package satisfies the automated audit and selected policy.

It does not mean the book looks right.

## Exit codes

- `0` — audit PASS
- `3` — audit completed with policy/check findings
- `2` — tool, custody, or structural stop

## BHT frozen-release policy

`profiles/bht_frozen_releases_001.json`

Platforms:

- `apple`
- `kindle`

The profile verifies exact Release 001 architecture and selected asset identities.

It is a frozen-release policy, not a universal template for future books.

## Future policy rule

A new publication policy should be created only from:

- an accepted exact artifact;
- explicit source standing;
- explicit platform deviations;
- named asset identities;
- recorded navigation and cover roles.

Do not create a policy by guessing what a package ought to contain.
