# BHT Frozen Release Provenance 001

**Status:** Exact-identity record for completed Apple and Kindle EPUB 1 release artifacts
**Date:** 2026-10-07
**Boundary:** This repository records identities and method. It is not a second retail-binary vault.

---

## Shared pre-divergence artifact

`BHT_RETAIL_RELEASE_CANDIDATE_002.epub`

- bytes: `5,124,743`
- SHA-256: `fa7646400000f69479aafe33ad5b01106aa96cc94e2cd6011e08aaaf56392dae`

Standing:

Shared semantic/presentation ancestor used by both clean retailer rebuilds.

It does not impose one retailer package skeleton.

---

## Cardinal operational source custody

State:

`BHT EPUB 1 Source Successor State 002`

Repository:

`MettleForgeLab/bht-open-materials`

Immutable tag:

`bht-epub-1-source-002`

Commit:

`d14eab45bd47047487e9cfa76efc978071a2497b`

Licensed operational-source membership:

`94 files`

Jules Bering remained unchanged.

| Lens | Aggregate ordered-source identity |
| --- | --- |
| North | `7ec230ec3123b0215328cc681c213db98267c4a384f98c0cfffbc43be7f4f18b` |
| East | `6a4f46ab94854c200604edce74d34a32aaff38eba345893cd152e8e22b316ca2` |
| South | `1e06c47b65226c39f5e9840fb614a6ad111ffecf4fed3d344253cf368ead7a38` |
| West | `8fb2401ecad12a7e01bebe833836354740d90b3f450beaefd8a0c4d5797489af` |

Both frozen retailer releases carry the accepted cardinal successor wording.

---

## Apple EPUB 1 Release 001

Artifact:

`BHT_APPLE_EPUB1_RELEASE_001.epub`

- bytes: `3,711,173`
- SHA-256: `40ffe038e163a818335af9ba65a1380e84bb5cbfa69ac5eef11d1dc23781757b`

Governing candidate:

`BHT_APPLE_RELEASE_SMOOTHING_CANDIDATE_007.epub`

Candidate → release:

**BYTE-IDENTICAL COPY**

Validation:

- Porter final Apple visual review: **PASSED**
- EPUBCheck: `v5.4.0`
- exit code: `0`
- fatals: `0`
- errors: `0`
- warnings: `0`
- infos: `0`
- mutation after validation: **none**
- freeze date: `2026-10-07`

Immediate recovery source:

The exact Candidate 007 bytes are a valid recovery source because Release 001 is byte-identical.

Historical predecessor:

`BHT_APPLE_RELEASE_SMOOTHING_CANDIDATE_006.epub`

SHA-256:

`81211e3e999cee1b282c7c3d3fc1165b2458fb70f2f2ba509de46b2f62663381`

---

## Kindle EPUB 1 Release 001

Artifact:

`BHT_KINDLE_EPUB1_RELEASE_001.epub`

- bytes: `6,658,243`
- SHA-256: `225592b811b301200e9477e172269a0099152f1f94701a20bfcfc5961088c9d7`

Governing candidate:

`BHT_KINDLE_RELEASE_SMOOTHING_CANDIDATE_004.epub`

Candidate → release:

**BYTE-IDENTICAL COPY**

Validation:

- Porter Kindle visual review: **PASSED**
- EPUBCheck: `v5.4.0`
- exit code: `0`
- fatals: `0`
- errors: `0`
- warnings: `0`
- infos: `0`
- mutation after validation: **none**
- recorded acceptance date: `2026-10-06`

Immediate predecessor:

`BHT_KINDLE_RELEASE_SMOOTHING_CANDIDATE_003.epub`

SHA-256:

`ff241931c7606ff163f74803ac23109783aab47ad7772f7392f88cea052510fe`

---

## Cover-role identities

### Apple external marketing cover

`Now_You_Can_Do_Big_Hard_Things_cover_master_1600x2560.png`

- dimensions: `1600 × 2560`
- bytes: `5,341,828`
- SHA-256: `b282a3cbd9ea1fef9c0e77c125000dcb2d3b0075adccb1bd92912f08cf8a7bcc`

### Apple in-book cover

`BHT_cover_apple_inbook_1580x2528_q98.jpg`

- dimensions: `1580 × 2528`
- bytes: `2,023,814`
- SHA-256: `e5bafa54a939ab3e082c52c1a5d9136de1390a4c35f037f8eeb45d6c2c777dc5`

### Kindle/general cover

`Now_You_Can_Do_Big_Hard_Things_cover_master_1600x2560_q98.jpg`

- dimensions: `1600 × 2560`
- bytes: `2,037,016`
- SHA-256: `9cf72ed964324bca45dea25ac8d8de95a83114595f140882191095f185f588c6`

The Apple in-book cover and Kindle/general cover are separate admitted derivatives.

---

## Shared selected White Room derivatives

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `WR2_01_Hallway_Threshold_Console_TransitCart_v1_epub_q96.jpg` | 458,497 | `8e398c9aad4fdba239964bd5ce1b010fc0f1f951accbe6cbfdaaecf994f04270` |
| `WR2_10_RoomSide_GDB_Formation_First_Milliseconds_v1_epub_q96.jpg` | 564,597 | `7c99a2b366679500c2175d47860deda1797762512950e36a9cc5e916d56148fe` |
| `WR2_13_Hallway_PathsReport_USB_Envelope_v1_epub_q96.jpg` | 355,599 | `0b83be93402d868329ea0fe966e857c70c4777d79db7762537502c0f1f9024e5` |

The same exact JPEG bytes appear in both frozen EPUBs.

---

## Repository boundary

Track here:

- exact artifact identities;
- source custody;
- validation standing;
- platform architecture;
- accepted deviation reasons;
- reproducible audit policies.

Do not track here by default:

- duplicate frozen retailer binaries;
- private retailer-account exports;
- portal credentials;
- mutable KDP/Apple draft state;
- post-publication analytics.

The retail release files remain frozen outside this Git repository.

---

## Reopening rule

Any change to content, style, images, navigation, metadata, package structure, or source creates:

1. a new candidate;
2. a new validation record;
3. a new human acceptance decision;
4. a new release identity.

Never overwrite Release 001 in place.
