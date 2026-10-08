# BHT Shared Publication / Build Playbook — 002 — Changelog

Playbook 002 supersedes Playbook 001 for future work. Preserve Playbook 001 as lineage.

## Finalized after both EPUB 1 freezes

The October 6 draft of Playbook 002 was written while the clean rebuilds still had open release gates.

This final repository edition advances the evidence without changing the durable architecture.

### Apple evidence advanced to frozen release

`BHT_APPLE_EPUB1_RELEASE_001.epub`

- bytes: `3,711,173`
- SHA-256: `40ffe038e163a818335af9ba65a1380e84bb5cbfa69ac5eef11d1dc23781757b`
- Porter visual review: **PASSED**
- EPUBCheck v5.4.0: **0 / 0 / 0 / 0**
- candidate → release: **byte-identical**
- post-validation mutation: **none**

### Kindle evidence advanced to frozen release

`BHT_KINDLE_EPUB1_RELEASE_001.epub`

- bytes: `6,658,243`
- SHA-256: `225592b811b301200e9477e172269a0099152f1f94701a20bfcfc5961088c9d7`
- Porter Kindle visual review: **PASSED**
- EPUBCheck v5.4.0: **0 / 0 / 0 / 0**
- candidate → release: **byte-identical**
- post-validation mutation: **none**

### Authority clarified

- common pre-divergence artifact recorded exactly;
- Source Successor State 002 recorded separately from the shared ancestor;
- platform derivatives remain evidence, not source authority;
- retailer ingestion remains a later operational crossing.

### Comparative method strengthened

- package metrics now come from the frozen endpoints;
- Apple and Kindle cover roles are explicit;
- selected White Room derivatives are recorded as shared exact bytes;
- Kindle split documents retain renderer-stability reason and removal tests;
- Apple live graphics remain first-class where relation survives;
- exact-byte freeze discipline is now supported by both final releases.

## Core conclusion retained

> The book has a stable semantic anatomy, but no single mandatory physical skeleton.
>
> A good publication build makes the semantic anatomy explicit, then gives each renderer only as much additional structure as it has earned.
