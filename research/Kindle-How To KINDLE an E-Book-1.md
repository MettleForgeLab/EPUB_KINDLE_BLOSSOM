## Core verdict

Your current philosophy is the right one:

> **Live prose. Live source standing. Live navigation. Atomic spatial meaning. Kindle-native pacing.**

For this book, the Kindle edition should **not** try to make Kindle behave like Thorium. It should preserve meaning by deciding, element by element, what belongs in live reflow and what must become an atomic plate. The evidence points strongly toward this architecture:

**One top-level entry per XHTML spine item; document-level TOC targets where possible; live prose and semantic headings; one-column live navigation; raster or carefully tested SVG plates for diagrams whose meaning depends on spatial relation; no CSS Grid for meaning; no long meaningful background fields that span pages; no gradient/bloom atmosphere left to Kindle CSS.**

Amazon’s current public documentation does not expose a developer-controllable “KFX spec.” It talks primarily in terms of **Enhanced Typesetting**, **KPF**, Kindle Previewer behavior, and KF8/MOBI fallback. Kindle Previewer supports EPUB/XHTML/KPF inputs, lets you preview device classes, and KDP’s current guidance says EPUB/DOCX/KPF/HTML are the supported reflowable upload paths while MOBI is no longer recommended for reflowable publishing. ([Kindle Direct Publishing][1])

---

## Evidence labels used below

| Label  | Meaning                                                                                    |
| ------ | ------------------------------------------------------------------------------------------ |
| **O**  | Official Amazon/KDP documentation, current public page unless noted.                       |
| **A**  | Accessibility authority: Amazon accessibility, DAISY, W3C EPUB accessibility.              |
| **P**  | Professional/practitioner source; useful but not binding.                                  |
| **H**  | Historical source; do not generalize to current Enhanced Typesetting/KFX unless confirmed. |
| **E**  | Your bounded Kindle experiments.                                                           |
| **NE** | Not established by current evidence.                                                       |

Most Amazon KDP pages do not expose a conventional “last updated” date in the page body; the pages cited here were crawled in September 2026 and show current KDP footer/copyright context. Where a non-Amazon source has a visible date, I call that out.

---

# 1. Executive findings: the 18 rules for this adaptation

1. **Treat “Enhanced Typesetting” as the current public target, not an open KFX spec.** Amazon documents Enhanced Typesetting support, device previews, KPF, and fallback behavior; it does not publish a stable author-facing KFX internals manual. Use Kindle Previewer/KDP logs as the source of truth. ([Kindle Direct Publishing][1])

2. **Keep the per-entry spine split.** Amazon’s formal HTML limit is far above your observed failure—individual HTML files must be under 30 MB and the book under 300 HTML files—so the 1.2 MB failure is not explained by a documented hard size limit. But your empirical result is decisive: per-entry splitting fixed the disappearing ending and improved conversion stability. ([Kindle Direct Publishing][2])

3. **Use document-level TOC targets for chapter/entry starts unless a fragment is truly needed.** Amazon documents TOC failures when targets point to hidden elements, body IDs, or unresolved/poorly scoped navigation targets. Your test showed that `entry.xhtml` survived where `entry.xhtml#fragment` failed. That is enough to prefer document-level targets for top-level entries. ([Kindle Direct Publishing][3])

4. **Do not let CSS Grid carry meaning.** Amazon’s Enhanced Typesetting support list includes `display:flex`, `inline flex`, and `table cell`, but does not list CSS Grid as a supported display value. Your observed Grid collapse is exactly what that absence predicts. ([Kindle Direct Publishing][3])

5. **Flexbox support is not enough to trust multi-column meaning.** `display:flex` is listed as supported, but that does not mean complex responsive Flexbox layouts preserve authorial relation under margin/font/device changes. Use flex only for non-essential minor arrangement, not compass/family/threshold geometry. ([Kindle Direct Publishing][3])

6. **Use real HTML tables only for genuinely tabular or simple comparison material.** Amazon recommends HTML tables for tabular content because they can paginate and be exposed to assistive technology, but warns that wide/large tables create bad reading experiences; Enhanced Typesetting does not support nested tables. ([Kindle Direct Publishing][4])

7. **Rasterize spatial meaning.** Compass layouts, Jules bearing fields, Western Tellings-style relational plates, radial fields, and maps whose meaning depends on absolute placement should become atomic plates with live title/prose/source/caption/navigation around them.

8. **Use SVG cautiously, preferably as external image, not inline architecture.** Amazon says computer-generated visuals are best represented as SVG, but also warns SVG tags can cause errors and recommends using an HTML image tag; the Enhanced Typesetting unsupported list also calls out SVG namespace-prefix problems. ([Kindle Direct Publishing][5])

9. **PNG is the safest default for typography-bearing diagrams.** Amazon accepts common image workflows, recommends diagrams/maps with text occupy at least 80% of screen width, says transparent backgrounds are converted to white, and requires sRGB. For flat color and type, PNG is usually safer than JPEG compression. ([Kindle Direct Publishing][5])

10. **Captions should stay live.** Amazon specifically recommends figure captions in HTML rather than rasterized into the image. That matches your “live frame + atomic plate” pattern. ([Kindle Direct Publishing][5])

11. **Do not force ordinary body text styling.** Amazon says reflowable body text should stay close to defaults, because forced font size, line height, color, background, margins, and font faces can override reader settings and create poor reading experiences. ([Kindle Direct Publishing][6])

12. **Strip desktop pacing controls.** `height` must not control text-containing elements; fixed px/pt dimensions are discouraged; `min-height` is internally contradictory in Amazon’s own docs—listed as supported in one table and ignored in another—so remove nearly all desktop `min-height`, `vh`, giant padding, and page-like spacers. ([Kindle Direct Publishing][6])

13. **Be conservative with page breaks.** Kindle supports `break-*` and `page-break-*`, including `avoid`, but these properties can create large whitespace when the kept block is too large. At spine starts, avoid “new file + break-before” double forcing. ([Kindle Direct Publishing][6])

14. **Avoid meaningful long backgrounds that span pages.** Amazon supports background-color and related properties, but explicitly does not support `background-image: linear-gradient`; it also warns about forced background colors and requires testing in white, black, mint, and sepia modes. Your vertical-shift screenshots make long colored containers unsafe for meaning. ([Kindle Direct Publishing][3])

15. **Dark mode must be treated as a first-class test.** Amazon’s QA checklist explicitly says to check reflowable text in white, black, mint, and sepia background modes. Do not assume publisher colors remain unchanged or remain readable. ([Kindle Direct Publishing][2])

16. **Accessibility for plates requires more than `alt`.** Amazon requires meaningful images to have alt text, recommends max 140 characters, and recommends surrounding text; DAISY/W3C guidance favors concise alt plus visible extended descriptions for complex images. ([Kindle Direct Publishing][7])

17. **Kindle Create is not the main path for this source.** Kindle Create is useful for reflowable, print replica, and guided-view workflows, but its reflowable feature set is theme/template-oriented and explicitly does not edit some complex formatting like tables, lists, footnotes, and certain complex paragraphs. For a hand-built XHTML/CSS EPUB, direct EPUB → Kindle Previewer/KDP is more controllable. ([Kindle Direct Publishing][8])

18. **Fixed layout is the wrong primary format.** Amazon says fixed-layout books do not support reflowable text and cannot be partly reflowable and partly fixed-layout. For this text-heavy adult nonfiction book, fixed layout would sacrifice too much resizing, accessibility, and reading comfort. ([Kindle Direct Publishing][9])

---

# 2. Recommended Kindle architecture for this book

| Layer                                  | Recommendation                                                                                                                                                                    | Confidence                |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| **Source package**                     | Keep a Kindle-specific EPUB branch, not a mutation of the retail EPUB.                                                                                                            | High, production judgment |
| **Spine granularity**                  | One top-level book entry per XHTML spine item; 22 entries is well inside Amazon’s fewer-than-300-HTML-files limit.                                                                | High: O + E               |
| **TOC targets**                        | For top-level entries, target `entry.xhtml`, not `entry.xhtml#heading-id`, when the heading is first meaningful content. Use fragments only for interior links that require them. | Medium-high: O + E        |
| **Navigation**                         | EPUB 3 `nav.xhtml` plus a conservative NCX if toolchain supports it cleanly; flatten deep nesting to no more than two logical levels for Kindle.                                  | Medium-high: O            |
| **Live prose**                         | Keep all normal prose live, one column, default body size/line-height.                                                                                                            | High: O                   |
| **Source/editorial standing**          | Keep standing language live unless it is part of an inseparable spatial plate.                                                                                                    | High                      |
| **Complex diagrams**                   | Use atomic PNG plates by default; test external SVG only for simple line/vector diagrams.                                                                                         | High                      |
| **Jules / compass / family relations** | Plate them. Do not use Grid/Flex/absolute live layout where directional geometry carries meaning.                                                                                 | High: O + E               |
| **Tables/ledgers**                     | Real HTML tables only if small and truly tabular; otherwise split, simplify, or use plate + live explanation.                                                                     | High: O                   |
| **Background color policy**            | Short bounded live blocks only. Whole-entry body background can be tested for specific chapters, but avoid long nested colored panels as meaning-bearing devices.                 | Medium-high               |
| **Gradients/blooms**                   | Pre-render into plate. Do not use CSS gradient/bloom atmosphere as meaning.                                                                                                       | High: O + E               |
| **CSS policy**                         | Kindle-specific stylesheet. Remove Grid, complex absolute layout, giant min-height, vh/vw, meaningful pseudo-element art, long hidden content, negative margins.                  | High                      |
| **Pacing**                             | Use moderate top/bottom margins in `em`; avoid full-page spacer mechanics; remove first-element `break-before` in each spine item.                                                | High                      |
| **Accessibility**                      | Semantic live headings; plate `alt`; live caption; visible extended description link for complex plates. Avoid hidden duplicate text as the main accessibility mechanism.         | High: O + A               |
| **Testing**                            | Kindle Previewer e-reader/tablet/phone classes, portrait/landscape, min/default/large/max font, all background modes, every TOC/internal link, full-page flip-through.            | High: O                   |

---

# 3. Official Amazon support matrix relevant to this book

| Feature                            | Amazon-documented status                                                                                                            | Current recommendation                                                                                                                  |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| EPUB upload for reflowable         | Supported; Amazon recommends EPUB/DOCX/KPF/HTML over MOBI for reflowable.                                                           | Use EPUB direct or KPF generated from Previewer only if it preserves the hand-built source. ([Kindle Direct Publishing][10])            |
| Enhanced Typesetting               | Current reflowable target in Previewer/KDP; Previewer can show supported status.                                                    | Treat as target behavior; do not rely on old MOBI. ([Kindle Direct Publishing][1])                                                      |
| KF8 fallback                       | Still referenced for older/non-Enhanced environments.                                                                               | Keep CSS fallback simple; do not let KF8/MOBI advice drive current design unless needed. ([Kindle Direct Publishing][11])               |
| HTML file size                     | Individual HTML files under 30 MB; fewer than 300 HTML files.                                                                       | Per-entry split is safe. The observed 1.2 MB failure is not a documented size-limit failure. ([Kindle Direct Publishing][2])            |
| CSS Grid                           | Not listed as supported display value.                                                                                              | Do not use. ([Kindle Direct Publishing][3])                                                                                             |
| Flexbox                            | `display:flex` and `inline flex` listed.                                                                                            | Use only for non-critical minor layout; not spatial meaning. ([Kindle Direct Publishing][3])                                            |
| Tables                             | Real HTML tables recommended for tabular content; large/wide tables discouraged; nested tables unsupported in Enhanced Typesetting. | Use simple tables only. ([Kindle Direct Publishing][4])                                                                                 |
| Background color                   | Supported, but forced colors and background modes must be tested.                                                                   | Short blocks or body experiments only; no long meaning-bearing fields. ([Kindle Direct Publishing][3])                                  |
| Linear gradients                   | Explicitly unsupported as `background-image: linear-gradient`.                                                                      | Pre-render gradients. ([Kindle Direct Publishing][3])                                                                                   |
| Box shadow / text shadow / opacity | Listed as supported, but ignored variants also appear in Amazon’s own ignored list.                                                 | Treat as decorative only; never meaning-bearing. ([Kindle Direct Publishing][3])                                                        |
| `break-before/inside/after`        | Supported with `always/auto/avoid`; page-break equivalents supported.                                                               | Use sparingly. Remove duplicate first/last spine breaks. ([Kindle Direct Publishing][3])                                                |
| `height` on text containers        | Amazon says never use height to control text-containing elements.                                                                   | Remove. ([Kindle Direct Publishing][6])                                                                                                 |
| Images with diagram text           | Amazon recommends at least 80% screen width for diagrams/maps/graphs with text.                                                     | Plate images should usually be `width:100%; height:auto;`. ([Kindle Direct Publishing][5])                                              |
| SVG                                | Amazon says SVG is good for computer-generated visuals, but SVG tags can cause errors; namespace prefix unsupported.                | External SVG only after test; PNG default for critical plates. ([Kindle Direct Publishing][5])                                          |
| Transparent images                 | Transparent backgrounds converted to white.                                                                                         | Avoid transparent PNG for dark/colored plates; bake solid background. ([Kindle Direct Publishing][5])                                   |
| Captions                           | Captions should be live HTML, not rasterized.                                                                                       | Use `figure/img/figcaption`. ([Kindle Direct Publishing][5])                                                                            |
| Alt text                           | Required for meaningful images; Amazon recommends max 140 characters.                                                               | Concise alt + visible caption + extended description for complex diagrams. ([Kindle Direct Publishing][7])                              |
| Cover                              | KDP requires separate marketing cover and internal cover image; OPF cover can be `properties="cover-image"` or legacy meta.         | Use both OPF `properties="cover-image"` and legacy meta consistently; avoid duplicate HTML cover page. ([Kindle Direct Publishing][12]) |

---

# 4. Known-bug / quirk table for your observed symptoms

| Symptom                                                | Ranked likely causes                                                                                                                                                                                                                                   | Evidence status                                                             | Repair                                                                                                                                                                   |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **A — Blank page before new entry after spine split**  | 1. New spine item plus first-element `break-before/page-break-before`; 2. previous spine item ending with `break-after/page-break-after`; 3. oversized opening block with `break-inside:avoid`; 4. recto/right values; 5. Kindle pagination edge case. | `break-*` support official; double-page behavior NE; your blank pages E.    | Remove all first-element breaks inside spine files; remove final-element breaks on previous files; avoid `recto/right`; do not wrap huge opener in `break-inside:avoid`. |
| **B — Background starts/ends offset from prose**       | 1. Long container fragmented across Kindle pages; 2. padding/min-height/background painted per fragment; 3. conversion rewrite; 4. dark/theme adjustment.                                                                                              | Background support official; fragmentation behavior NE; your screenshots E. | Do not use long colored containers for meaning. Use body background only for whole-entry experiment, short bounded live blocks, or plates.                               |
| **C — Side-by-side diagram stacks vertically**         | 1. Grid unsupported; 2. narrowed reader column; 3. conversion fallback; 4. font scaling; 5. min-width ignored/unsafe.                                                                                                                                  | Grid absence official; stacking E.                                          | Replace with plate or one-column live structure; table only for simple comparison.                                                                                       |
| **D — Compass/family geometry lost**                   | Same as C plus directional geometry cannot survive font/margin reflow.                                                                                                                                                                                 | O + E.                                                                      | Atomic plate. Provide live caption/description.                                                                                                                          |
| **E — Western Tellings plate survives well**           | Single image avoids Kindle layout recomputation; live frame preserves semantic context.                                                                                                                                                                | E, aligned with Amazon image/figure guidance.                               | Generalize as “live frame + atomic relational plate.”                                                                                                                    |
| **F — Jules raster plate better than live field**      | Same as E; Kindle cannot safely recompute radial/absolute/field atmosphere.                                                                                                                                                                            | E.                                                                          | Plate comparable spatial fields.                                                                                                                                         |
| **G — Ending disappeared until Entry 21 got own file** | 1. Conversion/location mapping failure in larger XHTML; 2. DOM/anchor/indexing issue; 3. hidden/fragment/TOC logic interacting with flow; 4. undocumented converter bug below formal size limits.                                                      | Formal limit does not explain it; E strong.                                 | Keep per-entry split; run full-text end checks after each conversion; inspect logs; test monolithic vs split reproducer.                                                 |

---

# 5. Answers to every numbered question, compact ledger

## A. What does modern Kindle build from EPUB? — Questions 1–7

| #     | Answer                                                                                                                                                                                                                                                                                                                                                                                |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | Officially, Kindle Previewer ingests EPUB/XHTML/HTML/KPF and previews **Enhanced Typesetting** for current device classes. Amazon does not document the current internal package as an author-facing “KFX spec,” though KPF is the author/publisher-side package and older user-guide material describes KPF export for Enhanced Typesetting preview. ([Kindle Direct Publishing][1]) |
| **2** | Previewer’s current visible path is Enhanced Typesetting preview. Legacy MOBI/AZK export is for older devices/apps that do not support Enhanced Typesetting and is not accurate for current Enhanced Typesetting layout. ([Readkong][13])                                                                                                                                             |
| **3** | Yes, different generations/environments matter: Amazon says older Previewer/device workflows that do not support Enhanced Typesetting use older behavior, and current docs still discuss KF8/MOBI media-query fallback. ([Kindle Direct Publishing][11])                                                                                                                              |
| **4** | The important difference is not only screen size; it is reader control: font, background mode, orientation, device class, and display technology. Amazon tells publishers to test e-reader, tablet, phone/app classes and all background modes. ([Kindle Direct Publishing][1])                                                                                                       |
| **5** | The documented lowest common denominator is: semantic HTML, one-column live body text, conservative CSS, relative units, simple tables, responsive block images, valid links, and accessibility metadata. There is no official “LCD stylesheet,” but this is the practical intersection of KDP text/image/table/accessibility guidance. ([Kindle Direct Publishing][6])               |
| **6** | KPF is the native Kindle publishing package, but not necessarily more controllable for a hand-built EPUB unless generated from the same source without structural loss. Kindle Previewer-generated KPF can be used for preview/reopen, and Kindle Create-generated KPF can be uploaded, but KPF is not a hand-editable authoring format. ([Readkong][13])                             |
| **7** | Kindle Create is probably not beneficial for this book as the main conversion path. It supports reflowable themes, chapter detection, hyperlinks, and image features, but it does not expose the fine-grained XHTML/CSS control this project needs and lists several complex-format editing limitations. ([Kindle Direct Publishing][8])                                              |

## B. XHTML resource size, spine splitting, Entry 11 failure — Questions 8–15

| #      | Answer                                                                                                                                                                                                                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **8**  | Current Amazon guidance gives a hard import restriction: each HTML file must be smaller than **30 MB**, and the ebook must contain fewer than **300 HTML files**. ([Kindle Direct Publishing][2])                                                                                                                  |
| **9**  | I did not find current official Amazon documentation of fragment/anchor failures specifically caused by ~1 MB XHTML files. Your experiment remains empirical evidence.                                                                                                                                             |
| **10** | Official docs show TOC/anchor failures around hidden targets, body IDs, NCX scope, and unresolved links, but I did not find a public current KFX DOM/byte-offset/anchor-count limit. ([Kindle Direct Publishing][3])                                                                                               |
| **11** | The “300 KB per XHTML” rule is historical, not current Amazon guidance. Old production lore about 300 KB came from earlier EPUB/MOBI-era device constraints; current Amazon’s stated limit is 30 MB. Treat 300 KB as obsolete unless a specific current Kindle test reproduces it. ([Kindle Direct Publishing][2]) |
| **12** | One chapter/entry per XHTML spine document is current best practice for this project, even if not mandated by Amazon, because it improves conversion stability, navigation, QA, and reduces pagination/anchor complexity.                                                                                          |
| **13** | Many small spine resources are preferable here to several large ones, as long as each file is a coherent top-level entry and the count remains well below 300.                                                                                                                                                     |
| **14** | No meaningful performance/stability penalty is established for 20–30 XHTML files; 22 top-level entries is well below Amazon’s 300 HTML file import ceiling. ([Kindle Direct Publishing][2])                                                                                                                        |
| **15** | Cross-file fragment navigation is officially expected in EPUB/Kindle, but Kindle TOC and hidden-target rules must be respected. For top-level entries, prefer document-level targets. Interior cross-links should be tested with Previewer quality checks and manual navigation. ([Kindle Direct Publishing][2])   |

## C. TOC and internal links — Questions 16–23

| #      | Answer                                                                                                                                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **16** | Yes: for chapter/entry starts, `entry.xhtml` is safer than `entry.xhtml#heading-id` when the heading is at the beginning. This is not an explicit Amazon rule; it is your empirical result plus Amazon’s documented fragment/hidden/body-ID failure patterns.                               |
| **17** | Official docs document TOC fragment failures when the destination is hidden, when IDs live on `body`, and when NCX/TOC nesting is poorly scoped. I did not find a general current “EPUB3 nav fragment bug” statement. ([Kindle Direct Publishing][3])                                       |
| **18** | Amazon current pages still reference NCX errors and workflows, so keeping a valid NCX alongside EPUB 3 navigation remains conservative, especially for Kindle. ([Kindle Direct Publishing][3])                                                                                              |
| **19** | Yes. Amazon explicitly says a TOC target pointing to `display:none` can cause E24010. ([Kindle Direct Publishing][3])                                                                                                                                                                       |
| **20** | Not established. Amazon documents target-hidden failures, but not false positives caused by other hidden elements in the same document. Avoid broad selectors that hide ancestor containers or large blocks.                                                                                |
| **21** | Use ASCII IDs, unique IDs, visible elements, near the top of the target block, not on `body`, not on hidden/offscreen/zero-size elements, and not inside layout wrappers likely to be removed. The body-ID and hidden-target advice is directly documented. ([Kindle Direct Publishing][3]) |
| **22** | For this book, yes: every major Kindle TOC destination should begin its own spine item. That is a project rule, not a universal Amazon mandate.                                                                                                                                             |
| **23** | Document-level destinations are common and safe for top-level chapter entries; Amazon docs do not forbid them, and your tests support them.                                                                                                                                                 |

## D. Blank pages at spine boundaries — Questions 24–31

| #      | Answer                                                                                                                                                                                                                                         |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **24** | Kindle generally treats a new spine item as a fresh reading segment/page boundary in practice, but I did not find a clean current Amazon sentence saying “each spine item always starts on a new page.” Treat it as empirically true and test. |
| **25** | `break-before`, `page-break-before`, and their `always/left/right/avoid` variants are supported values, so they can influence pagination at the start of a spine item. ([Kindle Direct Publishing][3])                                         |
| **26** | Yes, “new spine item + explicit page break before first element” is the leading diagnosis for a double advance/blank page, though the double-advance behavior itself is empirical, not officially documented.                                  |
| **27** | Yes, `break-after/page-break-after` on the final element of the previous spine item can plausibly do the same.                                                                                                                                 |
| **28** | Yes, `break-inside:avoid` can create large whitespace when the next kept block is too large; Amazon supports the property, but any keep-together rule can force a move. ([Kindle Direct Publishing][6])                                        |
| **29** | Recto/verso behavior is not established for reflowable Kindle from current official docs. Avoid `left/right/recto` logic unless a test proves it necessary.                                                                                    |
| **30** | Remove first-element `break-before/page-break-before`, previous-file final `break-after/page-break-after`, giant `margin-top`, giant padding, `min-height`, `height`, `vh/vw`, and large opener `break-inside:avoid`.                          |
| **31** | Amazon’s general pattern is: insert page breaks after new chapters/sections, but that advice must be adapted for split-spine books so you do not double-force a break. ([Kindle Direct Publishing][6])                                         |

## E. Reader margins and content width — Questions 32–38

| #      | Answer                                                                                                                                                                                                                                           |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **32** | Kindle devices/apps allow reader changes to font and layout in different ways; Amazon’s docs emphasize testing device/app classes, font sizes, and background modes rather than promising a fixed content width. ([Kindle Direct Publishing][1]) |
| **33** | Reader settings can override or normalize body font size, font family, colors, and background behavior. Amazon says body text should remain default and warns against imposed font/color/margins. ([Kindle Direct Publishing][6])                |
| **34** | Publisher CSS should not try to control outer page margins in reflowable Kindle. Amazon tells publishers to set normal body left/right margins to zero so readers retain device default margin selection. ([Kindle Direct Publishing][6])        |
| **35** | A hard minimum margin is not documented in the exact form asked, but Kindle reserves reader/device layout space. Negative margins can cause cut-off content. ([Kindle Direct Publishing][1])                                                     |
| **36** | Yes, effective width differs across e-reader, Fire/tablet, phone, desktop/app, orientation, and font settings. Previewer device classes exist for this reason. ([Kindle Direct Publishing][1])                                                   |
| **37** | Yes. Production design should assume the reader can make the column substantially narrower.                                                                                                                                                      |
| **38** | No reliable supported way was found to declare “this diagram needs at least X width” in reflowable Kindle. Scale atomically and ensure legibility at the narrowest test width.                                                                   |

## F. Grid, Flexbox, tables, responsive design — Questions 39–48

| #         | Answer                                                                                                                                                                                                                                       |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **39–40** | CSS Grid is not listed as supported in Amazon’s Enhanced Typesetting display values. Treat Grid as unsupported/unsafe. ([Kindle Direct Publishing][3])                                                                                       |
| **41**    | All listed Grid features—`fr`, `minmax()`, explicit placement, overlapping cells, named areas, grid centering—are unsafe because Grid itself is not established as supported.                                                                |
| **42**    | Flexbox is listed, but reliability for complex multi-column relational layouts is not established. Use only where failure does not damage meaning. ([Kindle Direct Publishing][3])                                                           |
| **43**    | Real HTML tables are officially supported for tabular content and can paginate; nested tables are not supported in Enhanced Typesetting. ([Kindle Direct Publishing][4])                                                                     |
| **44**    | For a simple two/three-column comparison that must remain live, use a small real HTML table only if it remains readable at narrow widths; otherwise convert to one-column.                                                                   |
| **45**    | `display:table/table-row/table-cell` is not fully documented as a safe layout system. Amazon lists `table cell`, not the full CSS table layout set; real `<table>` is safer. ([Kindle Direct Publishing][3])                                 |
| **46**    | HTML tables paginate; image tables do not. ([Kindle Direct Publishing][4])                                                                                                                                                                   |
| **47**    | `inline-block` is not clearly established in the current supported display list. Use it sparingly and test.                                                                                                                                  |
| **48**    | Reliable responsive techniques: block flow, relative units, percentages, `width:100%; height:auto` images, simple media queries only when they solve a specific device problem, and e-reader-first defaults. ([Kindle Direct Publishing][5]) |

## G. Absolute positioning and diagrams — Questions 49–54

| #      | Answer                                                                                                                                                                                                                                                          |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **49** | `position:absolute` is not listed in the snippets I found as a recommended reflowable layout method; Amazon’s common-error examples show absolute positioning combined with inherited height/width causing conversion problems. ([Kindle Direct Publishing][3]) |
| **50** | Percentage-positioned nodes are not dependable for meaning under reflow; not established officially.                                                                                                                                                            |
| **51** | `transform` is listed as supported, but dependable rotation/translation/scaling for semantic diagrams is not established. ([Kindle Direct Publishing][3])                                                                                                       |
| **52** | Conversion rewriting of coordinate systems is not publicly documented. Treat as NE.                                                                                                                                                                             |
| **53** | Yes, positioned children can become separated from intended backgrounds in paginated/reflowed environments; your background/geometry screenshots support this empirically.                                                                                      |
| **54** | Yes. For this project, rasterize any diagram whose meaning depends heavily on absolute positioning.                                                                                                                                                             |

## H. Background colors and vertical shift — Questions 55–64

| #         | Answer                                                                                                                                                                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **55–57** | Official docs confirm background support but do not define page-fragment painting behavior. Your screenshots establish a project-specific issue: long colored sections can decouple from prose after pagination. ([Kindle Direct Publishing][3]) |
| **58**    | `box-decoration-break` was not found in Amazon’s supported list. Treat as unsupported/not established.                                                                                                                                           |
| **59**    | Yes. Avoid meaningful backgrounds on any container that can span multiple pages.                                                                                                                                                                 |
| **60–61** | `body` background/color is documented in supported tag/attribute terms, but dependable full-entry page background behavior across themes is not established. Test per-entry body backgrounds only. ([Kindle Direct Publishing][3])               |
| **62**    | Whether Kindle surrounds body backgrounds with reader-controlled white margins is not established by current docs; test on Previewer and physical/app targets.                                                                                   |
| **63**    | Dark mode can alter text/color behavior; Amazon explicitly requires checking background modes. ([Kindle Direct Publishing][2])                                                                                                                   |
| **64**    | Use short bounded blocks for simple emphasis, body background only after testing, raster plates for meaningful fields, and avoid large decorative atmospheres unless pre-rendered.                                                               |

## I. Gradients, blooms, shadows, atmosphere — Questions 65–69

| #      | Answer                                                                                                                                                                                                                                                                 |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **65** | `background-image: linear-gradient` is explicitly unsupported; opacity, box-shadow, text-shadow, transform are listed as supported in places; filters, masks, radial gradients, pseudo-element blooms are not established as reliable. ([Kindle Direct Publishing][3]) |
| **66** | Shadows/opacity may convert but should be decorative only. Amazon’s supported/ignored lists conflict around shadow naming, so do not use them for meaning. ([Kindle Direct Publishing][3])                                                                             |
| **67** | Linear gradients are unsupported; animations/transitions and many visual effects are ignored. ([Kindle Direct Publishing][3])                                                                                                                                          |
| **68** | CSS radial gradients on e-ink are not established; treat as unsafe.                                                                                                                                                                                                    |
| **69** | Yes. Pre-rendered plates are the accepted project-safe solution for atmosphere, blooms, shadows, and soft fields.                                                                                                                                                      |

## J. Atomic image plates — Questions 70–85

| #         | Answer                                                                                                                                                                                             |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **70**    | Yes. “Live frame + atomic relational plate” aligns with Amazon’s image/figure guidance: keep captions live, use quality images, and provide alt text. ([Kindle Direct Publishing][5])              |
| **71**    | PNG is safest for diagrams with typography/flat color; JPEG for photos; SVG only after device testing.                                                                                             |
| **72–73** | Amazon may transform/optimize images internally, but exact recompression/conversion behavior is not publicly specified. NE.                                                                        |
| **74**    | Transparent PNGs are not safe for deliberate dark/colored plates; Amazon converts transparent backgrounds to white. ([Kindle Direct Publishing][5])                                                |
| **75**    | Official content-image pixel dimensions are not given beyond cover guidance; design diagrams to be legible at 80%+ of small screen width and test.                                                 |
| **76**    | For in-content diagrams, pixel dimensions matter more than DPI metadata; cover guidance includes DPI/PPI, but reading-column display is viewport/pixel driven. ([Kindle Direct Publishing][12])    |
| **77**    | Avoid huge files that slow conversion; official hard source limits concern HTML file count/size, not a specific content-image pixel cap in the retrieved docs.                                     |
| **78**    | Yes: `img { display:block; width:100%; height:auto; object-fit:contain; }` is the safe base. Amazon’s sample uses `display:block; width:100%; object-fit:contain`. ([Kindle Direct Publishing][5]) |
| **79**    | Yes. Avoid explicit `height`, `min-height`, and aspect-ratio boxes for large figures unless test-proven.                                                                                           |
| **80**    | Yes. `page-break-inside:avoid`/`break-inside:avoid` can create whitespace when a figure is large.                                                                                                  |
| **81**    | Yes. Let the wrapper paginate naturally if needed; keep the image itself atomic.                                                                                                                   |
| **82–83** | Place caption immediately after image in `figcaption`; do not rely on forcing a giant keep-with. Amazon recommends figure/caption HTML. ([Kindle Direct Publishing][5])                            |
| **84**    | Kindle generally scales/moves images rather than splitting the bitmap; Amazon says large pictures should scale to fit and display in entirety on one screen. ([Kindle Direct Publishing][2])       |
| **85**    | Practical max image height should be below the smallest target viewport after UI/margins; otherwise Kindle may shrink aggressively. Exact threshold NE; test.                                      |

## K. SVG — Questions 86–93

| #      | Answer                                                                                                                                                                                                   |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **86** | Inline SVG reliability is not established and is risky.                                                                                                                                                  |
| **87** | External SVG via `<img>` is the best SVG path to test, because Amazon recommends using the image tag for SVG-like visuals. ([Kindle Direct Publishing][5])                                               |
| **88** | ViewBox/lines/paths/opacity may work in some conversions, but SVG gradients/filters/blur/text/font behavior are not established. Namespace-prefix issues are documented. ([Kindle Direct Publishing][3]) |
| **89** | Text inside SVG should not be treated as searchable/selectable/accessibility-friendly on Kindle. Use live caption/description.                                                                           |
| **90** | Embedded fonts inside SVG are not established.                                                                                                                                                           |
| **91** | External SVG might be worth testing for line-heavy diagrams, but PNG is safer for Jules/compass fields because typography, color, and relation are mission-critical.                                     |
| **92** | Device-class SVG fallback behavior is NE.                                                                                                                                                                |
| **93** | Whether Kindle rasterizes SVG during KFX/Enhanced conversion is not documented in the retrieved official sources. Treat output as black-box and test visually.                                           |

## L. Heading + plate openers — Questions 94–99

| #         | Answer                                                                                                                                                                            |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **94**    | No fully reliable Kindle-native way was found to keep live `h2` + governing statement + image together across all font/margin settings.                                           |
| **95**    | Wrapping can help modestly, but large wrappers plus keep-together rules can produce whitespace.                                                                                   |
| **96–97** | `break-inside:avoid` is supported, but can create large blank areas when the block is too tall. ([Kindle Direct Publishing][6])                                                   |
| **98**    | If the visible heading’s placement is spatially integral, include it in the plate but also keep a live semantic heading nearby. Do not hide the live heading with `display:none`. |
| **99**    | No Amazon-specific complex illustrated chapter-opener pattern was found beyond general image/figure and page-break guidance.                                                      |

## M. Whitespace and pacing — Questions 100–107

| #           | Answer                                                                                                                                                                                                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **100–102** | Kindle supports margins/padding, but large values near breaks can yield unpredictable whitespace. Amazon recommends relative units and warns against fixed values. ([Kindle Direct Publishing][6])         |
| **103**     | Use modest `margin-top/bottom` in `em` for vertical breathing; use padding for short colored boxes only.                                                                                                   |
| **104**     | Yes, large `em` spacers scale with reader font size and can become dangerous.                                                                                                                              |
| **105**     | Yes. Remove almost all desktop `min-height` values from Kindle CSS. Amazon’s own docs conflict by listing `min-height` both supported and ignored, so do not depend on it. ([Kindle Direct Publishing][3]) |
| **106**     | `vh/vw` support was not established in retrieved Amazon docs; avoid.                                                                                                                                       |
| **107**     | Preserve pacing through entry splits, headings, modest margins, short dividers, and plates—not viewport simulation.                                                                                        |

## N. Complete-ending/truncation — Questions 108–112

| #       | Answer                                                                                                                                                                                                                 |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **108** | I did not find current official documentation of silent late-flow truncation in a large XHTML resource.                                                                                                                |
| **109** | Public current byte/DOM limits causing silent content disappearance were not established.                                                                                                                              |
| **110** | Yes, your result is a strong project-specific argument for one entry per spine resource.                                                                                                                               |
| **111** | Conversion logs can show errors/warnings; Amazon recommends checking logs and flipping every page because missing content is a QA risk. ([Kindle Direct Publishing][2])                                                |
| **112** | It is plausible Previewer can report conversion while content is visually inaccessible or effectively lost; Amazon’s QA guidance tells publishers to inspect the entire book manually. ([Kindle Direct Publishing][2]) |

## O. Multi-column navigation — Questions 113–118

| #       | Answer                                                                                                                                                                                                                     |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **113** | Yes. One-column navigation is effectively the safest Kindle approach.                                                                                                                                                      |
| **114** | Two-column link grids are unsafe in reflowable Kindle when relation/legibility matters.                                                                                                                                    |
| **115** | For formal TOC/nav: `<nav><ol><li><a>>`. For content maps: stacked block links. For true tabular comparison: simple `<table>`.                                                                                             |
| **116** | Larger tap padding is likely preserved as padding is supported, but test at narrow widths. ([Kindle Direct Publishing][3])                                                                                                 |
| **117** | Kindle may impose or adjust link styling; exact styling guarantees NE. Use underlines/borders/clear text, not color alone. Amazon accessibility guidance says identify links beyond color. ([Kindle Direct Publishing][7]) |
| **118** | Nested content-level `<nav>` elements are not established as unsafe, but deep navigation nesting can cause scope problems in TOC/NCX. Keep shallow. ([Kindle Direct Publishing][3])                                        |

## P. Compass/family diagrams — Questions 119–124

| #           | Answer                                                                                                                  |
| ----------- | ----------------------------------------------------------------------------------------------------------------------- |
| **119–120** | Preferred treatment: raster PNG plate with solid background, live caption, alt, and extended description.               |
| **121**     | External SVG is a secondary experiment, not default.                                                                    |
| **122**     | HTML table might preserve a rough five-cell relation, but will not preserve compass geometry under font/margin changes. |
| **123**     | No live HTML technique is likely to preserve North/East/South/West-around-center reliably under Kindle reader settings. |
| **124**     | Yes. Raster/SVG plate is the correct semantic-preservation choice.                                                      |

## Q. Accessibility for image-based diagrams — Questions 125–133

| #       | Answer                                                                                                                                                                                                                |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **125** | Kindle/Amazon requires alt text for meaningful images; Amazon recommends max 140 characters. ([Kindle Direct Publishing][7])                                                                                          |
| **126** | `figcaption` is supported as an HTML tag and Amazon recommends captions live; assistive exposure should still be tested. ([Kindle Direct Publishing][5])                                                              |
| **127** | Reliable support for `aria-label/aria-labelledby` in Kindle was not established in the official sources retrieved.                                                                                                    |
| **128** | Reliable support for SVG `<title>/<desc>` in Kindle was not established. Use HTML caption/description outside the SVG.                                                                                                |
| **129** | Amazon pattern: meaningful image alt, surrounding text description, avoid images of text where possible. DAISY/W3C pattern for complex images: concise alt plus extended description. ([Kindle Direct Publishing][7]) |
| **130** | Yes. Concise alt plus live explanatory caption is preferred.                                                                                                                                                          |
| **131** | Extended descriptions are supported robustly when implemented as visible linked descriptions; hidden mechanisms are less reliable across reading systems. ([Daisy][14])                                               |
| **132** | Keep live semantic headings adjacent to plates even if the visible art also contains title text.                                                                                                                      |
| **133** | Do not use `display:none`, `visibility:hidden`, zero-size duplicate text, or hidden TOC targets as the primary accessibility mechanism. Amazon documents hidden-target TOC failures. ([Kindle Direct Publishing][3])  |

## R. Reader fonts and typography — Questions 134–139

| #       | Answer                                                                                                                                                                                                     |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **134** | Readers can change font size/typeface; Amazon says body text should change accordingly in QA. ([Kindle Direct Publishing][2])                                                                              |
| **135** | Specifying Georgia/Times/etc. can matter only if publisher font styling is honored; readers may override. Do not depend on font metrics for layout.                                                        |
| **136** | Embedded fonts are worth considering only for headings/special passages where typographic voice matters. Amazon supports OTF/TTF but recommends defaults unless necessary. ([Kindle Direct Publishing][6]) |
| **137** | Embedded/forced fonts can reduce reader control if misused; Amazon warns that poor font implementation can revert settings or impair experience. ([Kindle Direct Publishing][6])                           |
| **138** | Publisher is responsible for font license rights. ([Kindle Direct Publishing][6])                                                                                                                          |
| **139** | Yes. Font substitution can materially change live diagrams/navigation. Therefore live layouts must not depend on exact font metrics.                                                                       |

## S. Dark mode and color — Questions 140–144

| #           | Answer                                                                                                                                                                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **140–142** | Amazon documents automatic legibility adjustments for text/background colors in Enhanced Typesetting and requires testing white/black/mint/sepia modes. Exact image inversion behavior was not established. ([Kindle Direct Publishing][6]) |
| **143**     | Dark North/South/West fields should be plates with their own solid background and live text outside when possible; if live, test in all background modes.                                                                                   |
| **144**     | Yes. Image plates should contain their own solid background for predictable color behavior, especially because transparent image areas are converted to white. ([Kindle Direct Publishing][5])                                              |

## T. Cover warning — Questions 145–149

| #       | Answer                                                                                                                                                                                                        |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **145** | Current EPUB 3 cover declaration: manifest item with `properties="cover-image"`. ([Kindle Direct Publishing][12])                                                                                             |
| **146** | Yes, `properties="cover-image"` is the preferred IDPF/EPUB 3 method. ([Kindle Direct Publishing][12])                                                                                                         |
| **147** | Amazon also documents the legacy `<meta name="cover" content="...">` method as valid. For maximum Kindle compatibility, include both consistently. ([Kindle Direct Publishing][12])                           |
| **148** | Do **not** add an extra HTML cover page in addition to the cover image; Amazon warns this can duplicate the cover or fail conversion. ([Kindle Direct Publishing][12])                                        |
| **149** | KDP requires a separate marketing cover upload, and the EPUB also needs an internal cover image. Use the same canonical cover art, but treat these as separate requirements. ([Kindle Direct Publishing][12]) |

## U. Fixed-layout and hybrid alternatives — Questions 150–156

| #       | Answer                                                                                                                                                                                        |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **150** | Fixed layout is not appropriate as the primary format for this text-heavy adult nonfiction book.                                                                                              |
| **151** | Amazon says books cannot be partially reflowable and partially fixed-layout. ([Kindle Direct Publishing][9])                                                                                  |
| **152** | Yes. Reflowable book + atomic image/SVG plates is the standard hybrid strategy available inside one reflowable Kindle book.                                                                   |
| **153** | Fixed layout sacrifices reflow, font resizing, and broad accessibility. Print Replica especially lacks screen-reader/braille support in Amazon’s paths page. ([Kindle Direct Publishing][10]) |
| **154** | Print Replica / fixed formats are limited to certain devices/apps and do not behave like universal reflowable Kindle books. ([Kindle Direct Publishing][10])                                  |
| **155** | Amazon recommends fixed layout only when the entire book is suited to fixed dimensions and text positioning. ([Kindle Direct Publishing][9])                                                  |
| **156** | Print Replica is wrong here unless making a separate teaching/reference artifact. It is not the main retail Kindle edition.                                                                   |

## V. Production case studies/resources — Questions 157–165

Public, detailed, current “master class” case studies for visually rich **reflowable Kindle** books are scarce. I found some production-house case studies, but most are either marketing-level, EPUB-general, or fixed-layout. Useful evidence:

| Source                                                         | What it shows                                                                                                                               | Limits                                                                                                                        |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **e-Doc Ltd reflowable EPUB3 case study**                      | Per-chapter XHTML, clean spine, embedded licensed fonts, dual navigation, EPUBCheck validation.                                             | EPUB3/general; not a deep Kindle visual case study. ([e-Doc Ltd][15])                                                         |
| **Booknando Editora do Brasil case study, updated April 2026** | Richly illustrated educational titles preserved through fixed-layout EPUB3 and Kindle optimization, tested in Kindle Previewer and Thorium. | Fixed layout, not this book’s primary path. ([Booknando][16])                                                                 |
| **BB eBooks CSS/Kindle production material**                   | Professional Kindle CSS boilerplate and KindleGen-era workflow.                                                                             | Useful craft source, but many parts are legacy and must not override current KDP Enhanced Typesetting docs. ([BB eBooks][17]) |
| **Hederis Kindle EPUB workflow docs**                          | Professional toolchain acknowledges Kindle-specific EPUB export and Kindle Previewer logs.                                                  | Tool documentation, not case-study proof. ([User Guide][18])                                                                  |
| **DAISY/W3C accessibility resources**                          | Strong guidance for image descriptions, extended descriptions, EPUB accessibility.                                                          | EPUB accessibility broadly; not Kindle-specific rendering. ([W3C][19])                                                        |

Answers to 157–165 from available evidence: visual compromises are usually simplification, per-chapter structure, semantic XHTML, image treatment for visual complexity, live text wherever possible, and extensive Previewer/device testing. Specific public details on whether comparable teams used SVG, exact spine splits, separate Kindle CSS, margin testing, or blank-page fixes were **not established** from robust current case studies.

## W. Testing matrix — Questions 166–172

| #       | Answer                                                                                                                                                                                                                                                                        |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **166** | Minimum Previewer set: Kindle e-reader, Fire/tablet, phone app class, and orientation changes. Kindle Previewer supports preview by device type/orientation/font. ([Kindle Direct Publishing][1])                                                                             |
| **167** | Represent small e-ink, Paperwhite-sized e-ink, Scribe/large e-ink if available, Kindle app phone, Kindle app tablet, Fire tablet.                                                                                                                                             |
| **168** | Yes: portrait and landscape for diagrams/nav.                                                                                                                                                                                                                                 |
| **169** | Test minimum, default, one large, and maximum practical font size. Amazon specifically says font size should change body text. ([Kindle Direct Publishing][2])                                                                                                                |
| **170** | Test narrow/default/wide margins where device/app exposes margin settings.                                                                                                                                                                                                    |
| **171** | Diagrams should remain usable at enlarged accessibility sizes, but not every relational plate can remain equally beautiful. Define pass/fail as “legible and semantically recoverable.”                                                                                       |
| **172** | A real Kindle defect is content loss, broken nav, unreadable text, overlap, wrong order, or missing ending at normal and accessibility-reasonable settings. Expected extreme-setting consequences include more pagination and less artful whitespace, but not broken meaning. |

## X. Inspecting converted result — Questions 173–179

| #       | Answer                                                                                                                                                                                                               |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **173** | No supported way was found to inspect the converted KFX/Enhanced internal HTML/CSS/resource tree as editable source.                                                                                                 |
| **174** | Kindle Previewer can export/reopen KPF according to user-guide material, but that is not an inspectable source tree in normal production. ([Readkong][13])                                                           |
| **175** | Kindle Previewer provides a Conversion Log, and user-guide material documents CLI options such as `-convert`, `-qualitychecks`, and `-log`. ([Kindle Direct Publishing][2])                                          |
| **176** | Safe diagnostics: Previewer GUI, conversion log, quality checks, original EPUB validation, ACE accessibility checker, EPUBCheck, and screenshot/manual QA. Internal KFX inspection was not established as supported. |
| **177** | You can infer discarded CSS from visible output and Amazon’s supported/ignored lists, but no official “discarded CSS report” was found.                                                                              |
| **178** | Exact recompression/rescaling detection is not officially exposed; use visual QA and compare source dimensions/log warnings.                                                                                         |
| **179** | Previewer quality checks can check internal links except TOC in older user-guide material; TOC still needs manual checking in both book TOC and left-pane TOC. ([Readkong][13])                                      |

---

# 6. Safe CSS subset for this project

Use a **Kindle-specific stylesheet** with these rules:

```css
html, body {
  margin: 0;
  padding: 0;
}

body {
  font-size: 1em;
  line-height: normal;
  font-family: serif;
}

main {
  margin: 0;
  padding: 0;
}

h1, h2, h3 {
  text-indent: 0;
  text-align: left;
  margin: 1.2em 0 0.6em 0;
  line-height: 1.2;
}

p {
  margin: 0 0 0.8em 0;
  text-indent: 0;
}

blockquote,
.standing,
.source-note {
  margin: 1em 5%;
  padding: 0;
}

.figure,
.plate {
  margin: 1.2em 0;
  padding: 0;
  text-align: center;
}

.figure img,
.plate img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  margin: 0 auto;
}

figcaption {
  margin: 0.5em 0 0 0;
  text-align: center;
  text-indent: 0;
  font-size: 0.9em;
}

.nav-list {
  margin: 1em 0;
  padding: 0;
}

.nav-list li {
  list-style-type: none;
  margin: 0 0 0.6em 0;
  padding: 0;
}

.nav-list a {
  display: block;
  padding: 0.4em 0;
  text-decoration: underline;
}
```

This follows Amazon’s preference for default body text, relative units, simple headings, `width:100%` images, live captions, and reader-controlled margins. ([Kindle Direct Publishing][6])

---

# 7. “Do not use” list for this project

Do not use these as meaning-bearing Kindle mechanisms:

* CSS Grid.
* Multi-column live relational diagrams.
* Absolute-positioned compass/field diagrams.
* CSS gradients or radial blooms.
* Pseudo-element atmosphere.
* Long colored containers spanning multiple screens.
* Transparent PNGs for dark/colored diagrams.
* Hidden duplicate text as the main accessibility layer.
* `display:none` TOC targets.
* IDs on `body` for TOC targets.
* Giant `min-height`, `height`, `vh`, `vw`, or page-simulation spacers.
* First-element `break-before` inside a new spine item.
* Final-element `break-after` in the previous spine item.
* Deep TOC nesting.
* Forced body font size/line height/color/background.
* Images of tables when a real table is possible.
* Rasterized captions.
* Fixed layout as the main Kindle edition.

---

# 8. Recommended image/SVG specs for atomic plates

For each plate:

| Item                     | Recommendation                                                                                                                                                         |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Default format**       | PNG for flat color/type diagrams; JPEG for photos; SVG only after separate Kindle test.                                                                                |
| **Background**           | Solid baked background; no transparency for dark/colored plates.                                                                                                       |
| **Width rule**           | `display:block; width:100%; height:auto; object-fit:contain;`.                                                                                                         |
| **Text in image**        | Keep large enough to read at phone/narrow e-reader width; Amazon recommends text-bearing diagrams occupy at least 80% of screen width. ([Kindle Direct Publishing][5]) |
| **Caption**              | Live `figcaption`, not rasterized.                                                                                                                                     |
| **Alt**                  | Short, specific, context-aware; Amazon recommends max 140 characters.                                                                                                  |
| **Extended description** | Visible link after caption for complex diagrams.                                                                                                                       |
| **Color profile**        | sRGB.                                                                                                                                                                  |
| **SVG**                  | External `<img src="diagram.svg">` only after tests; remove namespace-prefix hazards; provide PNG fallback candidate if SVG fails.                                     |

---

# 9. Accessibility recommendations for plates and complex relations

Use this pattern:

1. **Live semantic heading** before the plate.
2. **Short live governing statement** if it helps the reader enter the figure.
3. **Image plate** with concise `alt`.
4. **Live caption** naming what the plate does.
5. **Visible extended-description link** for complex diagrams.
6. **Extended description page/section** written as ordinary live prose.

Example structure:

```html
<section id="western-tellings">
  <h2>Western Tellings</h2>

  <p class="standing">
    A relational field showing how the Western telling holds boundary, inheritance,
    and consequence.
  </p>

  <figure class="plate">
    <img
      src="../images/western-tellings-plate.png"
      alt="Relational diagram of Western Tellings arranged around a central field." />
    <figcaption>
      Western Tellings relational plate.
      <a href="../backmatter/extended-descriptions.xhtml#desc-western-tellings">
        Extended description
      </a>
    </figcaption>
  </figure>
</section>
```

Amazon’s guidance supports alt text, surrounding text, live captions, heading hierarchy, table structure, and contrast; DAISY/W3C guidance supports visible extended descriptions for complex images where alt alone is insufficient. ([Kindle Direct Publishing][7])

---

# 10. Testing matrix

Minimum Kindle Previewer run:

| Dimension     | Values                                                                         |
| ------------- | ------------------------------------------------------------------------------ |
| Device class  | Kindle e-reader, Fire/tablet, phone/app class                                  |
| Orientation   | Portrait, landscape                                                            |
| Font size     | Smallest, default, large, max practical                                        |
| Typeface      | Default plus at least one alternate reader font where available                |
| Margins       | Narrow/default/wide where available                                            |
| Background    | White, black, sepia, mint                                                      |
| Navigation    | Built-in TOC, live TOC, every major internal map, return links                 |
| Plates        | Smallest width, largest font context, dark mode, caption/description adjacency |
| End integrity | Search/flip to final paragraph; verify complete ending visually                |
| Logs          | Conversion log, Previewer quality checks, EPUBCheck, ACE                       |

Amazon specifically recommends Kindle Previewer, conversion logs, full-book flip-through, checking images/tables/links, changing font size/typeface, and checking background modes. ([Kindle Direct Publishing][2])

---

# 11. Minimal reproducible code examples

## 11.1 Chapter/spine start without blank pages

```html
<!-- entry-11.xhtml -->
<body class="entry entry-11">
  <main id="entry-11">
    <h1>Entry 11 Title</h1>
    <p class="standing">Short governing statement.</p>
    <p>First live paragraph begins here.</p>
  </main>
</body>
```

```css
body.entry {
  margin: 0;
  padding: 0;
}

body.entry main {
  margin: 0;
  padding: 1em 0 0 0;
}

body.entry h1 {
  margin: 0 0 0.8em 0;
  padding: 0;
  text-align: left;
}

/* Deliberately absent:
   break-before
   page-break-before
   min-height
   height
   vh/vw
*/
```

## 11.2 Live one-column navigation

```html
<nav aria-label="Story map">
  <ol class="nav-list">
    <li><a href="entry-01.xhtml">Begin with the field</a></li>
    <li><a href="entry-02.xhtml">See what has become possible</a></li>
    <li><a href="entry-03.xhtml">Cultivate rather than fire</a></li>
  </ol>
</nav>
```

```css
.nav-list {
  margin: 1em 0;
  padding: 0;
}

.nav-list li {
  list-style-type: none;
  margin: 0 0 0.6em 0;
  padding: 0;
}

.nav-list a {
  display: block;
  padding: 0.45em 0;
  text-decoration: underline;
}
```

## 11.3 Responsive image plate with live caption

```html
<figure class="plate">
  <img
    src="../images/jules-bearing.png"
    alt="Circular bearing diagram for Jules with directional relation fields." />
  <figcaption>
    Jules bearing field. Spatial relation is preserved as a plate;
    title, caption, and navigation remain live.
  </figcaption>
</figure>
```

```css
.plate {
  margin: 1.2em 0;
  padding: 0;
}

.plate img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
}

.plate figcaption {
  margin: 0.5em 0 0 0;
  text-align: center;
  text-indent: 0;
}
```

## 11.4 Full-entry body background experiment

Use only for a bounded test, not as the default solution.

```html
<body class="entry field-west">
  <main id="west">
    <h1>West</h1>
    <p>Live prose remains here.</p>
  </main>
</body>
```

```css
body.field-west {
  background-color: #1f1a22;
  color: #f6efe7;
  margin: 0;
  padding: 0;
}

body.field-west main {
  margin: 0;
  padding: 1em 0;
}
```

Test in all background modes before trusting it. Amazon warns against forced body backgrounds/colors and requires background-mode testing. ([Kindle Direct Publishing][6])

## 11.5 SVG diagram test

```html
<figure class="plate svg-test">
  <img
    src="../images/family-compass.svg"
    alt="Compass diagram with North, East, South, and West around a center." />
  <figcaption>
    Family compass SVG test.
    <a href="../backmatter/extended-descriptions.xhtml#desc-family-compass">
      Extended description
    </a>
  </figcaption>
</figure>
```

If this fails visually or in logs, use PNG. Amazon says SVG can be best for computer-generated visuals but warns SVG tags can lead to errors and namespace prefixes are unsupported. ([Kindle Direct Publishing][5])

## 11.6 Safe two-column relation, only if live comparison is necessary

Use a real table for comparison, not Grid.

```html
<table class="relation-table">
  <caption>Two ways this section can be approached</caption>
  <thead>
    <tr>
      <th scope="col">Reader action</th>
      <th scope="col">What it preserves</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Read the live prose first</td>
      <td>Sequence and source standing</td>
    </tr>
    <tr>
      <td>Study the plate second</td>
      <td>Spatial relation and pacing</td>
    </tr>
  </tbody>
</table>
```

```css
.relation-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}

.relation-table caption {
  caption-side: top;
  text-align: left;
  margin-bottom: 0.5em;
}

.relation-table th,
.relation-table td {
  padding: 0.35em;
  vertical-align: top;
}
```

Keep it small. Amazon recommends tables under 100 rows/10 columns where possible and warns that wide tables create poor user experience. ([Kindle Direct Publishing][4])

---

# 12. Explicit contradictions / tensions in the evidence

1. **Amazon supports `min-height` in one table but lists `min-height` as ignored in another.** Do not rely on `min-height` for Kindle pacing. ([Kindle Direct Publishing][3])

2. **Amazon lists `box-shadow` as supported but also lists `box_shadow` / `-webkit-box-shadow` variants as ignored.** Treat shadows as decorative only. ([Kindle Direct Publishing][3])

3. **Amazon recommends SVG for computer-generated visuals, but also warns SVG tags can cause errors and flags SVG namespace prefixes as unsupported.** SVG is a test candidate, not a default for critical diagrams. ([Kindle Direct Publishing][5])

4. **Amazon supports `break-inside:avoid`, but using it on large openers can harm pacing.** Supported does not mean aesthetically safe. ([Kindle Direct Publishing][6])

5. **Amazon’s formal HTML size limit does not explain your 1.2 MB failure.** This means the observed Entry 11/Entry 21 failures are likely converter/navigation/DOM/pathology issues below formal limits, not official size-limit violations. ([Kindle Direct Publishing][2])

6. **Kindle Create/KPF is Amazon-native, but not necessarily more controllable for a hand-built designed EPUB.** KPF is useful; Kindle Create is not automatically the right authoring path for this project. ([Kindle Direct Publishing][8])

---

# 13. Prioritized experiment list: fastest 10 tests

1. **Blank-page isolator.** Build three two-file EPUBs: no breaks, first-file `break-after`, second-file first-element `break-before`. Confirm which creates blank page.

2. **Document target vs fragment target.** Same split file, TOC entry to `entry.xhtml` versus `entry.xhtml#h1`. Confirm Previewer conversion and left-pane TOC behavior.

3. **Hidden-target trap.** Create visible `h1`, hidden duplicate, body ID, child div ID. Confirm which triggers E24010.

4. **Grid/Flex/Table triad.** Same two-column relation in Grid, Flex, and real table. Test e-reader + phone widths.

5. **Compass variants.** Compass as Grid, absolute HTML, real table, external SVG, PNG. Score geometry preservation.

6. **Long background fragment test.** A colored `div` spanning 3–4 screens with live prose; compare to `body` background and short bounded blocks.

7. **Gradient/bloom test.** CSS linear gradient, radial gradient, pseudo-element bloom, PNG bloom plate. Confirm logs and visual output.

8. **SVG feature ladder.** External SVG with simple shapes; then text; then gradient; then opacity; then filter. Stop at first failure.

9. **Plate height test.** Same plate at 60%, 80%, 100%, and tall portrait ratios. Check scaling and caption adjacency.

10. **Ending integrity sentinel.** Add unique sentinel phrases to late entries, convert, then manually search/flip and run Previewer quality checks. This should become a release gate.

---

## Final production recommendation

The Kindle edition should be built as a **Kindle-safe sibling**, not a degraded copy:

* **22-ish XHTML spine items**, one per top-level entry.
* **Top-level TOC links to documents**, not beginning fragments.
* **Valid EPUB 3 nav plus conservative NCX**.
* **Live prose, headings, source standing, captions, and navigation**.
* **Atomic plates for spatial meaning**: Jules, Western Tellings, compass/family diagrams, relational maps, blooms/fields.
* **PNG default for critical plates**, SVG only after a pass/fail ladder.
* **No CSS Grid**, no live compass geometry, no long meaning-bearing backgrounds.
* **Short bounded live color only where it survives dark-mode and pagination tests**.
* **Kindle stylesheet stripped to conservative reflow rules**.
* **Accessibility layer: live headings + concise alt + live caption + visible extended descriptions**.
* **Release gate: Previewer log clean, every TOC/link checked, every page flipped, end sentinel verified, background modes checked, ACE/EPUBCheck run.**

That preserves the real standard: not “KDP accepts it,” but **a Kindle reader encounters recognizably the same book, with live text where Kindle is good, and preserved spatial meaning where Kindle reflow would otherwise lie.**

[1]: https://kdp.amazon.com/en_US/help/topic/G202131170 "Kindle Previewer"
[2]: https://kdp.amazon.com/en_US/help/topic/GGRXLC5USU4H67YM "QA Standards"
[3]: https://kdp.amazon.com/en_US/help/topic/GB5GDY7WAJDN9GFK "Attributes and Tags Supported by Enhanced Typesetting"
[4]: https://kdp.amazon.com/en_US/help/topic/GZ8BAXASXKB5JVML "Table Guidelines - Reflowable"
[5]: https://kdp.amazon.com/en_US/help/topic/G75V4YX5X8GRGXWV "Image Guidelines - Reflowable"
[6]: https://kdp.amazon.com/en_US/help/topic/GH4DRT75GWWAGBTU "Text Guidelines - Reflowable"
[7]: https://kdp.amazon.com/en_US/help/topic/GBPE3QVZ2J3HLQ4B "Accessibility for eBooks"
[8]: https://kdp.amazon.com/en_US/help/topic/GUGQ4WDZ92F733GC "Getting Started with Kindle Create"
[9]: https://kdp.amazon.com/en_US/help/topic/GFFHCXVPHRZW8SJ5 "Creating Fixed-Layout Books with Text Pop-Ups"
[10]: https://kdp.amazon.com/en_US/help/topic/G79CTKR8BX79E96L "Paths to Getting Your Content on Kindle"
[11]: https://kdp.amazon.com/en_US/help/topic/GR4KL488MXKPZ5BK "Media Queries"
[12]: https://kdp.amazon.com/en_US/help/topic/G6GTK3T3NUHKLEFX "Cover Image Guidelines"
[13]: https://www.readkong.com/page/kindle-previewer-user-guide-v3-66-0-english-june-20-2022-6052407?utm_source=chatgpt.com "Kindle Previewer User Guide - v3.66.0 English June 20, 2022 - AWS"
[14]: https://daisy.github.io/transitiontoepub/best-practices/extended-desc/index.html?utm_source=chatgpt.com "Best Practices for Implementing Extended Descriptions in EPUB"
[15]: https://e-doc.ltd/portfolio/reflowable-epub3/?utm_source=chatgpt.com "Reflowable EPUB3 Production – Case Study | e-Doc Ltd"
[16]: https://booknando.com.br/en/case-studies/editora-do-brasil/?utm_source=chatgpt.com "The digital journey of Editora do Brasil | Booknando"
[17]: https://bbebooksthailand.com/bb-CSS-boilerplate.html?utm_source=chatgpt.com "BB eBooks – CSS Boilerplate"
[18]: https://docs.hederis.com/docs/convert-to-kindle/?utm_source=chatgpt.com "Convert an EPUB to MOBI or KF8 for the Kindle | User Guide"
[19]: https://w3c.github.io/epub-specs/epub33/a11y-tech/?utm_source=chatgpt.com "EPUB Accessibility Techniques 1.1"
