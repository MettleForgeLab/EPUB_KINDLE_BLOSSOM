# Implementation boundaries — 0.14

## Purpose

MFL Kindle Visual Adapter is a custody-first publication-engineering tool.

It can:

- inspect an exact EPUB under explicit SHA-256 custody;
- bind declared semantic components to exact source identities;
- create bounded component probes;
- plan/render/review/admit platform representations;
- validate package structure with local and external tools;
- audit a complete Apple or Kindle publication against an explicit policy.

It does not claim to infer aesthetic meaning, source authority, human acceptance, or retailer approval.

---

## 1. Source is not a successful retailer file

A working retailer EPUB is presentation evidence.

It is not automatically the next manuscript source.

The current BHT authority chain is:

1. accepted semantic / operational source;
2. shared pre-divergence publication evidence;
3. platform recipe and admitted deviations;
4. frozen platform artifact;
5. retailer ingestion evidence.

The adapter may record and compare those layers. It must not collapse them.

---

## 2. Exact identity before work

Operations that act on a protected EPUB require an explicit SHA-256 or a policy containing the exact accepted identity.

A mismatch stops the run.

No fuzzy filename matching, newest-file selection, or silent baseline substitution is allowed.

---

## 3. Component probes and full-publication audits are different instruments

### Component probe

A component probe isolates a bounded visual/semantic treatment.

It can establish:

- source binding;
- render geometry;
- device reserve;
- local layout;
- candidate identity;
- component graphic review;
- explicit admission.

It cannot establish:

- whole-page composition;
- whole-book pagination;
- complete navigation;
- final retailer readiness.

### Publication audit

A publication audit examines a complete EPUB.

It can establish:

- exact artifact identity;
- ZIP/package integrity;
- manifest/spine structure;
- media-type/extension consistency;
- navigation/landmarks;
- resources/fragments;
- local IDREFs;
- policy-required/forbidden members;
- admitted asset identities;
- exact platform architecture.

It does not establish:

- visual quality in a native reading system;
- human release acceptance;
- accessibility certification;
- retailer ingestion success.

---

## 4. Flow and graphic failures use separate escalation branches

### Flow / pagination

`normal flow → responsive/local repair → local containment → explicit page boundary → renderer-proven spine boundary`

A spine split is an evidence-backed escalation, not a generic chaptering technique.

### Graphic / spatial relation

`live construction → responsive/local repair → simplified live construction → bounded plate`

A plate is justified when the renderer preserves pieces but destroys their relation.

Do not rasterize because a flow repair failed.

Do not split documents because a graphic misbehaved.

---

## 5. Profile-bound source selection

Every routed figure and included source-copy root has an exact canonical identity.

A source mismatch stops the run rather than attempting a near-match.

Render-only CSS is an explicit derivative layer. It may change typography, dimensions, and geometry; it does not change source wording.

---

## 6. Crop and negative-space boundary

A plate crop encloses the declared visual component.

It normally excludes:

- live caption;
- surrounding page;
- unrelated prose.

Pale/empty areas are not automatically discarded. Negative space may be part of the relation.

---

## 7. Display footprint and device reserve

Display width follows legibility and composition, not a fixed category percentage.

Physical-pixel reserve, reader-facing footprint, and effective label size remain separate measurements.

A local vertical-footprint budget may guide keep-together eligibility.

It is not pagination authority.

---

## 8. Visual overflow is explicit

Visible overflow remains an error unless the profile explicitly admits bounded visual overflow.

The renderer may expand only to measured visible descendants/text and within the configured safety limit.

Overflow errors identify the component key.

---

## 9. Optimization and admission remain human-governed

Optimization methods may be admitted.

Candidates are never silently promoted.

A candidate becomes eligible only under its method and review rules.

Publication substitution requires a separate explicit admission packet bound to:

- exact profile;
- exact baseline;
- exact candidate;
- exact method;
- exact human authorization.

Graphic review, accessibility, whole-page composition, and release approval remain separate standings.

---

## 10. Accessibility boundary

The adapter checks structural accessibility evidence such as:

- IDs and IDREFs;
- local links;
- alt/caption/description relationships represented in package structure;
- Ace findings where run.

Automated checks do not create an accessibility certification claim.

Human/native-reader accessibility review remains separate.

---

## 11. External validators and native renderers remain separate

EPUBCheck proves standards-conformance evidence.

Ace produces automated accessibility findings.

Kindle Previewer / Kindle Viewer and Apple/native readers produce renderer evidence.

Porter or another named reviewer supplies human acceptance.

Retailer portals supply ingestion evidence.

No clean result silently promotes the others.

---

## 12. Platform-specific structure is allowed but must carry provenance

The frozen BHT packages demonstrate legitimate sibling divergence.

Apple Release 001:

- 24 spine documents;
- no Kindle renderer-only splits;
- live graphics retained where relation survived.

Kindle Release 001:

- 26 spine documents;
- two renderer-stability split continuations;
- admitted plates and explicit decorative assets where needed.

Platform differences require:

- reason class;
- source relation preserved;
- exact evidence;
- removal test where applicable.

---

## 13. Publication audit policy

The 0.14 publication auditor is read-only.

A policy may require:

- exact filename/hash/bytes;
- exact member, manifest, spine, TOC, and landmark structure;
- platform stylesheets;
- admitted asset hashes and dimensions;
- required shared/source text;
- absence of stale, sibling-platform, or production-residue content.

The auditor reports package standing only.

It explicitly records:

- renderer review: `NOT INFERRED`
- human acceptance: `NOT INFERRED`

---

## 14. Reproducibility boundary

The tool records runtime and package evidence.

Byte identity is claimed only where the recorded process proves it.

System fonts, browser/runtime changes, and external validators can alter results.

Cross-runtime or cross-platform identity is never assumed.

---

## 15. Hard stops

Hard stops include:

- wrong expected EPUB hash;
- unsafe ZIP path, encrypted member, symlink, duplicate member, CRC failure;
- bad/moved `mimetype`;
- strict XML failure;
- missing manifest resource;
- duplicate IDs;
- broken local resources/fragments;
- broken accessibility IDREFs;
- wrong media type/extension;
- profile/source/CSS identity drift;
- label clipping or failed geometry constraints;
- under-resolved admitted plate;
- admission identity mismatch;
- existing output path where a fresh transaction is required;
- platform policy mismatch during frozen-release audit.

---

## 16. No publication side effects

The adapter does not:

- upload to KDP or Apple Books;
- alter retailer accounts;
- publish a release;
- push Git/GitHub state;
- mutate frozen EPUBs;
- infer legal/tax/account standing.

GitHub transport belongs to the appointed repository mechanic.

Retailer execution belongs to the appointed rollout lane.

---

## 17. Historical component-probe evidence

Earlier 0.1/0.2 boundaries remain useful for understanding:

- canonical figure/source locks;
- true-source render followed by declared derivative render;
- conservative optimization;
- vertical-footprint budgets;
- SVG-local IDs;
- profile-driven live simplification.

They are now incorporated into the boundaries above rather than treated as the current project horizon.

---

## 18. Current release boundary

The adapter now has evidence from frozen Apple and Kindle EPUB 1 releases.

That does not make the tool a universal automatic converter.

Generalization to another book must begin from that book's source identities, semantic units, graphic relations, platform evidence, and human judgment.
