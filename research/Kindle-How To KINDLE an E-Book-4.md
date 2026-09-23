The final blockers reduce to five decisions:

1. **Blank pages:** yes, enough evidence now. Treat redundant page-breaks at split XHTML boundaries as the mechanism. Omit the break rules entirely unless you must neutralize inherited CSS.
2. **Whole-entry body backgrounds:** not established. Drop them from the architecture.
3. **PNG plate sizing:** Amazon gives screen-percentage and legibility rules, not exact production pixel sizes. Use a BHT convention: **2000 px ordinary, 2400–2560 px dense**.
4. **PNG behavior in conversion/dark mode:** Amazon documents enough transformation risk that plates must be tested visually, especially on e-ink dark mode.
5. **Prototype 004 should be a narrow stress test**, not another architecture debate.

## 1. Blank pages: definitive enough

The best professional example is Chris Jennings’ EPUB production note. He describes the exact sequence: split EPUB creates separate XHTML files, each file already represents a chapter/section start, InDesign also exports `page-break-before:always`, and the result may be a blank page because the reader has “2 reasons” to start a new page. His fix is changing the rule to `page-break-before:auto`. ([Chris Jennings Notes][1])

His companion “Creating a Reflowable eBook” page says the same thing in broader terms: blank pages can happen because there are “2 mechanisms” controlling page breaks—next-odd-page/start behavior plus a new HTML file—and the fix is to set `page-break-after:auto` and `page-break-before:auto` on the relevant headings. ([Chris Jennings Notes][2])

For BHT, the best practice is **not** to write `auto` everywhere as a design rule. The clean Kindle branch should **omit all spine-boundary break declarations**. Use `break-before:auto` / `page-break-before:auto` only as a temporary neutralizer if inherited retail CSS still contains `always`, `right`, `left`, `recto`, or similar break logic. Same for the last element of the previous spine item: omit break rules in final code; neutralize only if something inherited must be overridden. Amazon documents that Kindle looks at `page-break-before/after`, `break-before/after`, and `break-inside`, and supports `avoid`, `auto`, and `always`, so these properties are live enough to cause trouble. ([Kindle Direct Publishing][3])

Use this boundary rule:

```css
/* Best final state: no break declarations at all at split-spine boundaries */

/* Temporary cleanup override only if inherited CSS must be neutralized */
body.bht-entry > article,
body.bht-entry > article > h1:first-child,
body.bht-entry > article > *:last-child {
  break-before: auto;
  page-break-before: auto;
  break-after: auto;
  page-break-after: auto;
}
```

## 2. Whole-entry body backgrounds: stop investigating as architecture

I did **not** find strong current production evidence showing a multi-page Enhanced Typesetting chapter with publisher-controlled `body` background reliably painting across every generated screen, margin, final partial page, theme, and device class.

Amazon’s current text guidance points the other way for long prose: body text should remain default; imposed body text colors/backgrounds can override the reader’s preferred settings, and Amazon warns that light/dark colors can fail across device backgrounds and themes. It also says body text should not impose left/right margins or padding, because readers need their full device margin controls. ([Kindle Direct Publishing][3]) ([Kindle Direct Publishing][3])

So the recommendation is explicit:

> **Do not make whole-entry body backgrounds part of the BHT Kindle architecture. Use short live color fields plus atomic plates; allow long prose to return to the reader-controlled page field.**

Prototype 004 may include one body-background stress test for curiosity, but it should not block implementation and should not become a dependency.

## 3. PNG plate production numbers

Amazon’s current hard guidance for in-content images is not “1600/2000/2560 px.” It is: provide the best available image, make text-bearing diagrams/maps legible, and make images with letters/numbers/symbols occupy at least **80% of screen width** on smaller devices. Amazon’s sample block image CSS is `display:block; width:100%; object-fit:contain`, and its figure/caption sample keeps the caption live. ([Kindle Direct Publishing][4]) ([Kindle Direct Publishing][4]) ([Kindle Direct Publishing][4])

I did not find current professional Kindle sources giving reliable diagram-label numbers like “all labels must be 24 px at 2000 px source width.” The older KindleGen/KPG-era “line art” numbers still circulate, but they are not strong enough to govern a current Enhanced Typesetting/KFX build. They are useful only as background pressure: line art and text need generous resolution and contrast.

Use this BHT convention:

| Plate type                               |      Source width | Label rule                                            |
| ---------------------------------------- | ----------------: | ----------------------------------------------------- |
| Ordinary relational plate                |       **2000 px** | primary labels ≥30 px source; secondary labels ≥24 px |
| Dense Jules/family/compass plate         |  **2400–2560 px** | primary labels ≥32 px source; secondary labels ≥26 px |
| Simple mood/field plate with little text |  **1600–2000 px** | test visually                                         |
| Tall/dense diagram                       | split or simplify | do not solve with pixels alone                        |

The reason to allow 2400–2560 px for dense plates is not that Amazon requires it; it is that Kindle may scale images down, recompress/transform images, and display them on high-density or large viewports. The reason not to use 2560 px everywhere is that it increases source size without proven benefit for simple plates.

## 4. PNG recompression: current knowledge

The current KDP reflowable image page does **not** promise that input PNGs are preserved byte-for-byte through Enhanced Typesetting. It does say transparent image areas are unsupported and converted to white, and CMYK images are converted to sRGB. ([Kindle Direct Publishing][4])

A current KDP Japan help page on reducing ebook file size states that JPEG/GIF are supported inside Kindle books and that other accepted image formats such as BMP/PNG, or images exceeding size requirements, may be automatically recompressed as JPEG during conversion. That is current Amazon-domain evidence that PNGs are not guaranteed to remain PNG-like internally, but it does not expose the exact KFX/device pipeline. ([Amazon Kindle Direct Publishing][5])

No supported Kindle Previewer/KPF diagnostic was found that reports “this PNG was downsampled/recompressed to X.” Treat recompression/downsampling as a black-box risk. The practical mitigation is visual QA, larger source labels, sRGB, flattened opacity, no transparency, and physical e-ink review for subtle blooms/rings.

## 5. Dark mode: e-ink versus apps

For e-ink, the clearest device-manual evidence says Kindle dark appearance can invert **text, image, and page color** on all screens. The Kindle Scribe manual mirror says Appearance lets the user set light/dark mode and “inverts the text, image, and page color”; the same statement appears under accessibility. ([ManualsLib][6]) ([ManualsLib][6])

For Kindle iOS/Android/Fire behavior, I did not find a current Amazon production document proving that opaque PNGs are always left untouched while only live text/page colors change. App environments have their own theme controls and screens, so this remains **not established**. Amazon does document that Kindle Previewer can preview tablets, phones, e-readers, orientation, font, and image-containing pages, but that is not the same as proving dark-theme image treatment on every retail app. ([Kindle Direct Publishing][7])

BHT should use **one plate set**, not theme-specific alternate images, because I found no supported mechanism for theme-specific replacement plates in reflowable Kindle. That one set should be deliberately higher-contrast and grayscale-safe enough to survive normal display, e-ink inversion, and app theme variation.

## 6. Grayscale, blooms, and gradients

I found no current Amazon-specific production rule like “add N% noise to gradients for Kindle.” The evidence is practical, not official: modern Kindle e-ink/dark-mode behavior can invert images, Amazon warns about illegible image text, and Amazon can transform images during conversion. Therefore BHT plates should be checked in grayscale before release, and subtle blooms/rings should not carry the only boundary signal. ([Kindle Direct Publishing][4]) ([ManualsLib][6])

Use these BHT plate rules:

* Export plates in sRGB.
* Flatten all transparency onto an intentional opaque background.
* Make ring lines and labels visibly separable in grayscale.
* Increase contrast compared with the retail EPUB where necessary.
* Add mild texture/dither only if grayscale preview shows banding.
* Do not let pale gold, muted green, or low-opacity bloom be the only semantic separator.

## 7. Caption adjacency

Amazon’s figure pattern is normal flow: `<figure><img><figcaption>…</figcaption></figure>` with `figure { width:100%; }`, `img { display:block; width:100%; object-fit:contain; }`, and normal `figcaption` margin. Amazon explicitly says captions should be text, not rastered into the image. ([Kindle Direct Publishing][4])

I did not find a current Kindle-specific “keep with previous” rule for `figcaption`. Amazon does document `break-inside:avoid` and page-break controls, but those are exactly the properties that can create whitespace when overused. ([Kindle Direct Publishing][3])

Global BHT figure rule:

```css
figure.bht-plate {
  margin: 1.2em 0;
  padding: 0;
  text-align: center;
}

figure.bht-plate img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  margin: 0 auto;
}

figure.bht-plate figcaption {
  margin: 0.5em 0 0 0;
  text-align: center;
  text-indent: 0;
}
```

Do **not** wrap large image + caption in `break-inside:avoid`. The occasional caption spill is less damaging than blank pages or huge whitespace.

## 8. Extended descriptions

Amazon’s accessibility guidance is current and direct: meaningful images need text alternatives, alt text should be no more than **140 characters**, and complex meaning can be described in surrounding text. It also recommends real text rather than images of text when separable. ([Kindle Direct Publishing][8])

DAISY’s 2026 extended-description best practices recommend, for EPUB, a separate HTML file linked from near the image, with a backlink returning to the original position; they specifically note that this is preferred over relying on collapsible `<details>` because reading-system support varies. They also say same-page visible descriptions are acceptable as an alternate technique. ([Daisy][9])

Implement BHT as:

```html
<figure id="fig-jules-bearing" class="bht-plate">
  <img
    src="../images/jules-bearing.png"
    alt="Jules at the center of a directional bearing field." />

  <figcaption>
    Jules bearing field.
    <a id="jules-bearing-desc-link"
       href="../backmatter/descriptions.xhtml#desc-jules-bearing">
      Extended description
    </a>
  </figcaption>
</figure>
```

And in the description file:

```html
<section id="desc-jules-bearing">
  <h2>Extended description: Jules bearing field</h2>

  <p>Jules appears at the center of a directional relation field...</p>

  <p>
    <a role="doc-backlink"
       href="../entries/entry-jules.xhtml#jules-bearing-desc-link">
      Return to Jules bearing field
    </a>
  </p>
</section>
```

No current Kindle-specific objection was found to a visible “Extended description” link. Use visible links and back-links; do not depend on `aria-describedby` alone.

## 9. Kindle Previewer CLI

Current KDP Previewer documentation clearly documents the GUI features: device type, orientation, font, e-reader/tablet/phone views, “View All” filters for elements such as images/lists/tables, Auto-Advance, and Enhanced Typesetting support display. ([Kindle Direct Publishing][7])

The current public KDP page I could access does **not** clearly document current CLI flags. It links to a User Guide, but the extractable guide material previously surfaced is older Kindle Previewer 3-era documentation. So: **do not treat `-convert`, `-qualitychecks`, `-log`, or `-showpreview` as current until the local install confirms them with `kindlepreviewer -help`.**

Best local discovery sequence:

```powershell
# Locate Previewer if it is on PATH
where.exe kindlepreviewer

# If found:
kindlepreviewer -help

# If not found, try the legacy local install convention:
$kp = "$env:LOCALAPPDATA\Amazon\Kindle Previewer 3\kindlepreviewer.exe"
Test-Path $kp
& $kp -help
```

Only after `-help` confirms flags should Prototype 004 use:

```powershell
& $kp "C:\BHT\Prototype004.epub" -convert -output "C:\BHT\kp-out" -qualitychecks
& $kp "C:\BHT\Prototype004.epub" -log -output "C:\BHT\kp-log"
```

No evidence found that CLI can select device, orientation, font size, margin, or theme. Treat automation as conversion/log assistance only; visual settings remain GUI/manual unless your local install proves otherwise.

## 10. Physical-device delta

Amazon itself says a specific location in Kindle Previewer may not show the same content as a physical Kindle device because reflowable content adapts to screen size and font size; it also notes a negative-margin case where content may be invisible in Previewer but display on a Kindle app/device. ([Kindle Direct Publishing][7])

For BHT, the things Previewer cannot finally approve are:

* subtle grayscale contrast;
* bloom/ring banding;
* e-ink dark-mode inversion of plates;
* real tap feel for navigation rows;
* perceived legibility of small labels;
* actual page-flash/ghosting experience;
* whether plate/caption adjacency feels acceptable on a real Paperwhite-class viewport.

Previewer is enough to build Prototype 004. A physical Paperwhite-class check is still required before release.

## 11. Adversarial compositor critique

The architecture is sound. The three likely remaining failures are:

1. **Residual boundary artifacts:** inherited `page-break-*`, `break-*`, spread metadata, or hidden spacer residue causes blank pages even after the architecture says not to.
2. **Plate legibility failure:** dense labels, subtle rings, or blooms look acceptable in desktop Previewer but lose contrast on real e-ink, dark mode, or grayscale inversion.
3. **Caption/description/navigation QA drift:** captions spill more than expected, extended-description return links fail, or one-column maps survive visually but lose usability at large font/narrow margin settings.

Unnecessarily conservative: abandoning SVG entirely is probably conservative in the abstract. For BHT it is still the right trade because PNG is already succeeding and SVG has too many uncertain Kindle/assistive-tech behaviors.

Still too optimistic: assuming one dense 2000 px plate will always be legible; assuming dark plates will feel intentional in all themes; assuming captions will stay emotionally close to images without occasional spill.

If shipping next week, I would remove whole-entry body backgrounds from the implementation, standardize plate export dimensions now, create one stress harness for plate/caption/navigation/boundary behavior, and test that harness on Previewer plus one Paperwhite-class device before scaling all 22 entries.

**BUILD PROTOTYPE 004 NOW**

* Omit explicit page-break instructions at split-spine boundaries; use `auto` only to neutralize inherited CSS.
* Remove whole-entry body backgrounds from the BHT architecture.
* Use short live colored opener/callout fields only.
* Use opaque PNG plates for spatial/directional diagrams.
* Standardize plates as **2000 px ordinary** and **2400–2560 px dense**.
* Keep captions live in normal flow.
* Use visible extended-description links with return links.
* Keep one-column relational navigation.
* Continue using document-level TOC targets.

**PROTOTYPE 004 MUST TEST**

* Blank-page boundary harness: no breaks vs inherited first-heading break vs previous-final break.
* Plate stress harness: 2000 px vs 2560 px dense plate, normal and large font, e-reader/phone/tablet.
* Dark/grayscale harness: opaque dark plate with subtle bloom/rings in white and dark mode, especially Paperwhite-class e-ink.
* Caption adjacency harness: normal flow versus caption-only `break-before:avoid`; no giant figure `break-inside:avoid`.
* Short colored opener field followed by neutral prose.

**FULL BUILD CAN PROCEED IF**

* No blank pages appear in Prototype 004 with all boundary breaks omitted/neutralized.
* Dense plates remain readable at e-reader and phone widths without zoom.
* Dark/subtle plates remain understandable in grayscale and dark mode.
* Captions either remain near images or spill acceptably without creating large whitespace.
* Extended-description links and return links work in Previewer.
* One-column navigation remains usable at large font and narrow width.
* No whole-entry background is needed to preserve meaning.

**RELEASE STILL REQUIRES**

* Kindle Previewer pass across e-reader, phone, and tablet views; portrait and landscape.
* White, sepia, mint, and black/dark theme checks where available.
* Small/default/large font checks and margin checks where available.
* Full “View All Images” review in Previewer.
* Complete built-in TOC and in-book link check.
* Final ending sentinel check.
* EPUBCheck/ACE/input validation.
* Local Previewer CLI help verification before relying on any CLI flags.
* One physical Paperwhite-class e-ink review for grayscale, dark mode, plate legibility, page feel, and tap targets.
* Final KDP Online Previewer pass after upload.

[1]: https://notes.chrisjennings.net/eBookProduction/Editing-inside-the-ePUB/?utm_source=chatgpt.com "Editing inside the ePUB package - Chris Jennings - his Notes"
[2]: https://notes.chrisjennings.net/eBookProduction/Creating-Reflowable-eBook/?utm_source=chatgpt.com "Creating a Reflowable eBook after a print production workflow - Chris Jennings - his Notes"
[3]: https://kdp.amazon.com/en_US/help/topic/GH4DRT75GWWAGBTU "Text Guidelines - Reflowable"
[4]: https://kdp.amazon.com/en_US/help/topic/G75V4YX5X8GRGXWV "Image Guidelines - Reflowable"
[5]: https://kdp.amazon.co.jp/ja_JP/help/topic/G200730380 "電子書籍の原稿ファイルのサイズの削減"
[6]: https://www.manualslib.com/guide/3619969/amazon-kindle-scribe-manual.html "Amazon Kindle Scribe Manual | ManualsLib"
[7]: https://kdp.amazon.com/en_US/help/topic/G202131170 "Kindle Previewer"
[8]: https://kdp.amazon.com/en_US/help/topic/GBPE3QVZ2J3HLQ4B "Accessibility for eBooks"
[9]: https://daisy.github.io/transitiontoepub/best-practices/extended-desc/ExtendedDescriptionsBestPractices.html?utm_source=chatgpt.com "Best Practices for Implementing Extended Descriptions in EPUB"
