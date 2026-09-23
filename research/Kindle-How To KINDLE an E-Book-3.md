## Round 3 finding

The architecture still holds. The only material correction is this:

**Do not promote whole-entry `body` background color from “promising” to “settled.”** Amazon documents background/color behavior and dynamic contrast, but I did not find official evidence that Kindle Enhanced Typesetting reliably paints a publisher `body` background across every generated screen, margin region, theme, and device. Treat whole-entry color-worlds as a targeted prototype, not a build-wide dependency.

The blank-page mechanism is much better established now: **a spine boundary already behaves like a chapter/page start in production practice; adding page-break instructions at that same boundary is the classic way to get an extra blank page.** The rule is strong enough:

> **No explicit page-break instruction at a spine boundary. The spine boundary itself is enough.**

---

# 1. Blank pages at spine boundaries

## What is actually established

Amazon documents that Kindle Enhanced Typesetting observes `page-break-before`, `page-break-after`, `page-break-inside`, `break-before`, `break-after`, and `break-inside`, with `always`, `auto`, and `avoid` values, and says Kindle looks at those properties while determining page breaks. That proves Kindle is not ignoring the very properties that can create the symptom. ([Kindle Direct Publishing][1])

Amazon does **not** publish a sentence saying “every spine resource begins on a new screen.” But experienced EPUB/Kindle production sources describe exactly that practical behavior: split XHTML chapter files act as new chapter starts, so an added CSS `page-break-before: always` gives the reader “two reasons” to start a new page and can create a blank page. Chris Jennings documents this specific InDesign-to-EPUB failure and the fix: change the inherited chapter-start rule from `page-break-before: always` to `auto`. ([Chris Jennings Notes][2])

A second real-world report matches the other half of the mechanism: a manual page break at the **end** of a chapter can guarantee a blank page on some screens because the next chapter already starts after a break. The fix is not to put manual page breaks at chapter ends. ([Ebooks Stack Exchange][3])

CSS itself also explains why `left/right` page-break values are dangerous: when honored in paged media, they may require one or two page breaks to land on the requested side. That is exactly the blank-page behavior you do **not** want in a reflowable Kindle book. ([W3C][4])

## Direct answers

| Question                                                                                        | Answer                                                                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Does Enhanced Typesetting inherently begin every spine item on a new screen/page?               | **By implementation convention / production behavior, yes enough to rely on it.** I did not find an Amazon spec sentence, but production evidence and your prototypes align.                                                                                                              |
| Can first-block `break-before: always` / `page-break-before: always` add another page advance?  | **Yes, strongly supported.** Amazon honors the properties; production reports show duplicate chapter breaks create blanks.                                                                                                                                                                |
| Can `break-before: right`, `page-break-before: right`, or `recto` cause blanks?                 | **If honored, yes by paged-media semantics.** Current Amazon docs I found only document `always/auto/avoid`, not `recto/verso/right/left` as Kindle-safe values, so BHT should not use them. ([Kindle Direct Publishing][1])                                                              |
| Can a last-child break in the previous spine item combine with the spine transition?            | **Yes, likely and supported by production reports.** Remove it.                                                                                                                                                                                                                           |
| Does Kindle insert blanks to simulate recto chapter starts?                                     | **Not established as a Kindle Enhanced Typesetting rule.** But EPUB reading-system rules can insert blanks for spread/page-spread metadata in synthetic-spread contexts, so also check OPF/spine metadata for `page-spread-*`, `rendition:page-spread-*`, or blank-page logic. ([W3C][5]) |
| Can `break-inside: avoid` on the first significant block push it forward and leave blank space? | **Yes in principle.** Amazon supports `break-inside: avoid`; any keep-together rule can push a block when the block is too large. Full blank-page behavior remains empirical, but the risk is real. ([Kindle Direct Publishing][1])                                                       |

## Exact safest CSS

Final element in spine item A:

```css
.bht-entry > article > *:last-child {
  break-after: auto;
  page-break-after: auto;
}
```

Opening in spine item B:

```css
html,
body {
  margin: 0;
  padding: 0;
}

body.bht-entry {
  margin: 0;
  padding: 0;
}

body.bht-entry > article {
  margin: 0;
  padding: 1em 0 0 0;
  break-before: auto;
  page-break-before: auto;
  break-after: auto;
  page-break-after: auto;
}
```

First heading in spine item B:

```css
body.bht-entry > article > h1:first-child {
  margin: 0 0 0.85em 0;
  padding: 0;
  text-align: left;
  line-height: 1.2;

  break-before: auto;
  page-break-before: auto;
  break-after: auto;
  page-break-after: auto;
}
```

Also inspect the OPF/spine for any spread metadata:

```xml
<!-- Avoid these unless deliberately tested -->
properties="page-spread-left"
properties="page-spread-right"
rendition:page-spread-center
rendition:page-spread-left
rendition:page-spread-right
```

---

# 2. Long color fields and `body` backgrounds

## What Amazon establishes

Amazon documents that Enhanced Typesetting can adapt font colors for contrast against reader-selected themes or page-level backgrounds, and the Text Guidelines warn against forced body colors/backgrounds for ordinary body text. Amazon specifically says body text should not have a forced font color or background color because it can override user defaults and create awkward box-like experiences. ([Kindle Direct Publishing][6])

Amazon also requires testing reflowable books in white, black, mint, and sepia background modes. ([Kindle Direct Publishing][7])

## What remains undocumented

I did **not** find current Amazon evidence that this:

```css
body {
  background-color: #241a18;
  color: #f5efe6;
}
```

reliably paints:

| Area                                             | Officially established? |
| ------------------------------------------------ | ----------------------: |
| Every generated prose screen from the spine item |         Not established |
| First generated page                             |         Not established |
| Final partial page                               |         Not established |
| Reader margin area                               |         Not established |
| Behind images                                    |         Not established |
| Same behavior on e-ink, Scribe, app, tablet      |         Not established |
| Same behavior in white/sepia/mint/black themes   |         Not established |

So the safe rule changes slightly:

**A whole-entry body color world is allowed as a prototype, not as the default long-field solution.**

## BHT color strategy

| Use case                                                    | Current safest treatment                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------------------ |
| Short source boundary / threshold / callout                 | Short live colored block.                                                |
| Long prose chapter where color is atmosphere, not structure | Neutral reader-controlled prose after a short colored opener.            |
| Whole entry whose color-world is central to identity        | One-entry XHTML with `body` field, but test it as a dedicated prototype. |
| Field whose color must align with spatial diagram/prose     | PNG plate or shorter segments.                                           |
| Long nested `<section>` background spanning pages           | Avoid. This remains suspect.                                             |

Recommended long-entry compromise:

```html
<body class="bht-entry">
  <article>
    <section class="entry-opener-field">
      <h1>North</h1>
      <p class="threshold">Short live threshold language.</p>
    </section>

    <p>Long live prose returns to the reader’s normal page field.</p>
  </article>
</body>
```

```css
.entry-opener-field {
  margin: 0 0 1.2em 0;
  padding: 1em 0.8em;
  background-color: #241a18;
  color: #f5efe6;
}

.entry-opener-field h1,
.entry-opener-field p {
  color: inherit;
}
```

That preserves the color encounter without asking Kindle to maintain a multi-page publisher-controlled canvas.

---

# 3. Atomic plates: production numbers and containment

## Amazon requirements

Amazon gives a **screen-percentage requirement**, not a universal pixel-width requirement. For images containing letters, numbers, or symbols, Amazon says the image should be legible and should occupy at least **80% of the screen width**. Amazon’s sample CSS uses `display:block`, `width:100%`, and `object-fit:contain`. ([Kindle Direct Publishing][8])

Amazon also says large pictures should scale to fit the page and display in entirety on one screen. That implies tall images are likely to be moved or scaled, not split. ([Kindle Direct Publishing][7])

## Practical BHT source widths

These are production numbers, not official Amazon mandates:

| Source width | Use                                                                                                           |
| -----------: | ------------------------------------------------------------------------------------------------------------- |
|  **1200 px** | Only simple art, large labels, or non-critical diagrams. Too small for dense labeled fields.                  |
|  **1600 px** | Minimum serious width for ordinary label-bearing plates.                                                      |
|  **2000 px** | Best BHT default for conceptual diagrams with labels.                                                         |
|  **2560 px** | Dense diagrams, Scribe/tablet resilience, or plates likely to be zoomed. Watch file size and conversion time. |

For BHT, I would set:

```text
Ordinary plate: 1600–2000 px wide
Dense relational plate: 2200–2560 px wide
Do not use 1200 px for Jules/family/compass diagrams unless labels are very large.
```

## Label size inside plates

I did not find Amazon guidance like “18 px / 24 px / 30 px minimum.” Amazon’s official standard is legibility at target display size. For BHT, use this working rule:

| Label size at source | Decision                                             |
| -------------------: | ---------------------------------------------------- |
|               <18 px | Too risky.                                           |
|             18–23 px | Only for secondary labels; test on small e-ink.      |
|             24–30 px | Good baseline for full-width diagrams.               |
|               30+ px | Preferred for primary compass labels / Jules labels. |

Because Kindle may reduce a tall plate to fit one screen, label size must be judged after scaling, not only in source pixels.

## PNG recompression / downsampling

Amazon does not expose a full KFX image pipeline. An official KDP “advanced” page says images in accepted formats such as BMP/PNG, or images exceeding size requirements, may be automatically recompressed as JPEG during conversion. Treat that as evidence that KDP/Kindle conversion can transform images internally. ([Kindle Direct Publishing][9])

So the practical guidance is:

* provide clean, high-resolution PNG source;
* avoid tiny labels;
* avoid relying on ultra-subtle lines;
* check converted output visually;
* do not assume the PNG reaches the device byte-for-byte unchanged.

## CSS for critical plates

Yes, keep it plain:

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
  font-size: 0.9em;
}
```

Avoid:

```css
max-height
min-height
height
aspect-ratio wrappers
vh/vw
break-inside: avoid on the whole figure
```

---

# 4. Plate height and pagination

## Does Kindle split one `<img>` across pages?

I found no official evidence that Kindle literally slices a single `<img>` across pages in reflowable Enhanced Typesetting. Amazon’s QA language points the other direction: large pictures should scale to fit the page and display in entirety on one screen. ([Kindle Direct Publishing][7])

So assume the behaviors are:

1. fit;
2. scale down;
3. move to next page/screen.

Not: “split image across two pages.”

## Aspect ratio guidance

No official maximum aspect ratio was found. Practical BHT rule:

| Plate ratio                        | Decision                                                                       |
| ---------------------------------- | ------------------------------------------------------------------------------ |
| Landscape / square / mild portrait | Good.                                                                          |
| Around **3:4** or **4:5**          | Still workable.                                                                |
| Around **1:1.4**                   | Test carefully.                                                                |
| Taller than **1:1.6**              | Split or redesign.                                                             |
| 1400 × 2200                        | Too tall for many contexts; likely to shrink heavily, especially in landscape. |

For tall diagrams, the professional replacement is not “let Kindle solve it.” It is:

* split into two plates;
* simplify;
* make a portrait-friendly plate and accept that landscape will be smaller;
* provide live explanation/extended description;
* avoid making one tall plate the only way to understand the section.

There is no supported way I found to reserve “almost full screen for image plus enough live caption” with precise control. Kindle reflow decides the page.

---

# 5. Image + caption behavior

Amazon recommends live `figcaption` and explicitly shows image + caption markup, but I found no Amazon-documented “keep with previous” guarantee for `figcaption`. ([Kindle Direct Publishing][8])

A small caption-level avoid rule is reasonable but not magical:

```css
figure.bht-plate figcaption {
  break-before: avoid;
  page-break-before: avoid;
}
```

Amazon documents `break-before` / `page-break-before` support for `avoid`, but any keep rule can produce pagination side effects when space is tight. ([Kindle Direct Publishing][1])

Best BHT rule:

> Prefer occasional caption spillover to a full blank page caused by wrapping the entire image + caption in `break-inside: avoid`.

Use `break-inside: avoid` only for small figures that are known to fit.

---

# 6. Extended descriptions for complex plates

The linked-caption pattern is Kindle-safe in structure:

```html
<figcaption>
  Jules bearing field.
  <a href="../backmatter/descriptions.xhtml#jules-bearing">
    Extended description
  </a>
</figcaption>
```

Amazon requires meaningful images to have alt text, recommends concise alt text of no more than 140 characters, and says complex image meaning can be described in surrounding text. ([Kindle Direct Publishing][10])

For BHT, use:

```html
<figure id="fig-jules-bearing" class="bht-plate">
  <img
    src="../images/jules-bearing.png"
    alt="Jules at the center of a compass-like bearing field." />

  <figcaption>
    Jules bearing field.
    <a href="../backmatter/descriptions.xhtml#desc-jules-bearing">
      Extended description
    </a>
  </figcaption>
</figure>
```

Description page:

```html
<section id="desc-jules-bearing">
  <h2>Extended description: Jules bearing field</h2>

  <p>
    This diagram places Jules at the center of a bearing field.
    North, East, South, and West are arranged directionally around
    the center to show relation rather than sequence.
  </p>

  <p>
    <a href="../entries/entry-jules.xhtml#fig-jules-bearing">
      Return to Jules bearing field
    </a>
  </p>
</section>
```

Use a return link. Amazon footnote guidance favors bidirectional linking, and the same usability logic applies here. ([Kindle Direct Publishing][1])

`aria-describedby` is **not established** as reliably exposed in Kindle reading systems. Do not depend on it. Use visible links and live prose.

---

# 7. One-column navigation semantics

For BHT in-book relational maps, I would use:

```html
<section class="bht-rel-map" aria-labelledby="map-questions">
  <h2 id="map-questions">Questions this part can answer</h2>

  <ol class="bht-rel-nav">
    <li>
      <a href="entry-03.xhtml">
        <span class="question">What happened?</span>
        <span class="destination">03 · Gravity</span>
      </a>
    </li>
  </ol>
</section>
```

rather than making every map a `<nav>`.

Reason: `<nav>` is semantically valid for navigation, but I found no Amazon evidence that multiple in-book `<nav>` elements receive no special treatment in Kindle UI. The EPUB package/navigation document is already the formal navigation structure. For relational maps inside content, a labeled `<section>` plus ordered list is clean, accessible, and less likely to be confused with package navigation.

Block links with nested spans are safe enough if kept simple:

```css
.bht-rel-nav {
  margin: 1.2em 0;
  padding: 0;
}

.bht-rel-nav li {
  list-style-type: none;
  margin: 0 0 0.65em 0;
  padding: 0;
}

.bht-rel-nav a {
  display: block;
  padding: 0.55em 0;
  border-top: 0.05em solid currentColor;
  text-decoration: underline;
}

.bht-rel-nav .question,
.bht-rel-nav .destination {
  display: block;
}
```

Amazon’s accessibility guidance says links should not be identified by color alone; underline, border, or font change is appropriate. ([Kindle Direct Publishing][10])

Use **one link per row**. Do not bring back horizontal link geometry.

---

# 8. Per-entry XHTML and document-level TOC targets

Amazon’s QA/import limits are far above your architecture: each HTML file must be under 30 MB and the ebook must contain fewer than 300 HTML files. Twenty-three-ish XHTML reading resources are well inside that boundary. ([Kindle Direct Publishing][7])

I found no evidence of a performance, sync, annotation, or TOC penalty at 20–30 short XHTML resources. Given your empirical ending restoration, one semantic entry per resource remains the strongest choice.

Document-level TOC links are still the safer chapter-start form:

```html
<a href="entry-11.xhtml">See What Has Become Possible</a>
```

Use fragments for internal destinations:

```html
<a href="entry-11.xhtml#give-it-a-home">Give it a home</a>
```

Downside of document-level targets: they land wherever the document begins. So make the first substantial content a real heading and avoid invisible metadata, spacer wrappers, or hidden elements before it.

Good:

```html
<body class="bht-entry">
  <article id="entry-11">
    <h1>See What Has Become Possible</h1>
    ...
  </article>
</body>
```

Bad:

```html
<body>
  <div class="hidden-helper"></div>
  <div class="desktop-spacer"></div>
  <article>
    <h1>See What Has Become Possible</h1>
  </article>
</body>
```

Amazon’s accessibility guidance supports real heading hierarchy as assistive structure, so document-level navigation does not remove the heading’s semantic value if the heading is present and near the top. ([Kindle Direct Publishing][10])

---

# 9. CSS cleanup and hidden retail residue

Remove unused retail CSS and hidden helper geometry from the Kindle branch.

Amazon’s Enhanced Typesetting support/ignored-property documentation is large and uneven, and it explicitly lists many ignored/unsupported properties that are common in desktop-style visual EPUBs: CSS columns, animation, transitions, gradient background images, `min-height`, `min-width`, and several SVG-related attributes. ([Kindle Direct Publishing][11])

That makes the production rule simple:

> Do not carry desktop layout machinery into Kindle and hope overrides neutralize it. Delete it.

Use one reset stylesheet, one component stylesheet, and a few entry classes.

```html
<link rel="stylesheet" href="../styles/bht-kindle-reset.css" />
<link rel="stylesheet" href="../styles/bht-kindle-components.css" />
```

Pseudo-elements should not carry meaning. If the text matters, make it real HTML. If the visual field matters, make it a plate.

---

# 10. SVG: stop spending prototype time

Amazon’s guidance is internally tense:

* It says computer-generated visuals are well represented as SVG.
* It warns SVG tags can lead to errors and recommends using an image tag.
* Localized KDP guidance says Enhanced Typesetting supports GIF/JPEG/PNG and does not fully support SVG images, with only partial SVG rasterization. ([Kindle Direct Publishing][8])

I did not find a current serious commercial Kindle workflow proving that external SVG is a superior choice for this kind of art-directed conceptual diagram. I also did not find evidence that SVG text remains accessible/searchable as real text in Kindle, or that SVG `<title>` / `<desc>` are consistently exposed.

So the decision is:

> **Do not spend further prototype time on SVG; use PNG plates.**

The only exception would be a non-critical simple line-art test that takes minutes, not another design path.

---

# 11. Dark mode and plate behavior

This is the other major Round 3 correction.

For black-and-white Kindle e-readers, Amazon’s Kindle help says Dark Mode inverts text, image, and page color on all screens. That means opaque PNGs are **not guaranteed** to remain visually untouched on e-ink Dark Mode. ([Amazon DigPRJ Survey][12])

So the safe BHT dark-mode rule becomes:

| Component            | Rule                                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------------------- |
| Opaque PNG plate     | Still use it, but test Dark Mode on e-ink.                                                                     |
| Transparent PNG      | Avoid. Amazon says transparent image areas are not supported and become white. ([Kindle Direct Publishing][8]) |
| Dark BHT plate       | Bake an opaque background into the plate, but verify inversion behavior.                                       |
| Subtle rings/blooms  | Test in grayscale and dark mode.                                                                               |
| Live body dark field | Prototype only; not build-wide.                                                                                |
| Text outside plates  | Let Kindle/reader theme handle body prose where possible.                                                      |

A dark PNG surrounded by a white reader page will not necessarily receive an automatic border/padding treatment. If the dark field needs to read as intentional, include a deliberate border or field edge inside the plate.

---

# 12. Typography inside plates

For plate labels, do not force loyalty to the retail typeface if it becomes hard to read. Use a screen-optimized label style that preserves the hierarchy and relation.

Amazon accessibility requires sufficient contrast, with WCAG contrast thresholds of 4.5:1 for normal text and 3:1 for large text. ([Kindle Direct Publishing][10])

BHT plate rules:

* Use higher contrast than the retail EPUB where needed.
* Avoid ultra-thin lines.
* Avoid meaning carried only by pale gold, muted green, or low-contrast rings.
* Test every plate in grayscale.
* Primary labels should survive e-ink, not merely look beautiful in Thorium.
* Blooms can remain, but they must not be the only boundary signal.

For subtle blooms/gradients: I found no Amazon recommendation about dithering/noise for radial gradients. Practical rule: evaluate in grayscale; if banding appears, add a small amount of texture/noise in the image source and retest. Treat that as empirical image-production craft, not official Kindle guidance.

---

# 13. Conversion diagnostics and CLI

The current KDP Previewer page documents the GUI features: device type, orientation, font type, font size, View All, Auto-Advance, and Enhanced Typesetting support display. ([Kindle Direct Publishing][13])

KDP QA documents the Conversion Log and recommends checking warnings/errors, using Previewer, flipping through every page, and reviewing TOC links, fonts, images, and background modes. ([Kindle Direct Publishing][7])

The CLI commands from earlier research come from the Kindle Previewer 3 user guide material, not from a clearly current KDP page. That older guide documents flags such as `-convert`, `-qualitychecks`, `-showpreview`, and `-log`. ([Readkong][14])

So treat this as **not verified for the current local install** until you run:

```powershell
kindlepreviewer -help
```

or open the locally installed Previewer documentation.

A cautious PowerShell discovery sequence:

```powershell
# 1. See whether Kindle Previewer is on PATH
where.exe kindlepreviewer

# 2. If found, inspect current flags
kindlepreviewer -help

# 3. Then, only if the flags are listed locally:
kindlepreviewer "C:\BHT\kindle\BHT-Prototype-004.epub" -convert -output "C:\BHT\kp-out" -qualitychecks

kindlepreviewer "C:\BHT\kindle\BHT-Prototype-004.epub" -log -output "C:\BHT\kp-log"
```

If `where.exe` fails, locate the executable through the Start Menu / installed application path and run the same `-help` check against the full path. I would not hard-code a path into the production process until the machine confirms it.

No official tool was found that outputs a post-conversion report of every removed CSS rule, every image downsample, every recompression, or every surviving paragraph.

---

# 14. Automated visual QA

I found no official Kindle Previewer screenshot automation or stable DOM/UI automation interface.

What is official:

* Previewer GUI supports device/orientation/font testing, View All, and Auto-Advance. ([Kindle Direct Publishing][13])
* KDP recommends Previewer, Conversion Log, full page flip-through, TOC checks, font changes, image checks, and background-mode checks. ([Kindle Direct Publishing][7])

What is not established:

* official screenshot automation;
* official page-turn scripting;
* Playwright target;
* supported UI automation API;
* official screenshot diff workflow;
* automatic verification that every paragraph survived conversion.

Least brittle manual QA protocol:

1. Maintain a fixed checklist of entry numbers and figure IDs.
2. Use Previewer device classes: e-reader, phone, tablet.
3. For each: default font, large font, narrow margin if available, white and black theme.
4. Capture screenshots manually at known landmarks.
5. Verify:

   * no blank page before entry;
   * heading appears first;
   * plate legible;
   * caption nearby or acceptable;
   * nav links usable;
   * final sentinel present.
6. Log failures by entry/component, not by “page number,” because reflow changes pages.

---

# 15. Physical-device testing

Amazon says sideloading is no longer recommended for evaluating Enhanced Typesetting quality, because sideloaded files do not accurately indicate retail Enhanced Typesetting behavior. Previewer/KDP preview remains primary. ([Kindle Direct Publishing][7])

Still, BHT should test at least one physical e-ink device because Previewer cannot fully answer:

* grayscale plate legibility;
* dark-mode image inversion experience;
* perceived bloom/gradient banding;
* touch target feel;
* actual reader margin/font behavior.

Minimum physical test set:

| Priority              | Device class                                                                                               |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| Must have             | Current Paperwhite-class e-ink device, because it represents mainstream e-ink width and grayscale reality. |
| Useful                | Phone Kindle app, because narrow column stresses plates/navigation.                                        |
| Useful                | Tablet/Fire/iPad app, because color and wider viewport change plate feel.                                  |
| Optional but valuable | Scribe, because its viewport is a separate large-page experience, not just a bigger Paperwhite.            |

If only one physical device: **Paperwhite-class e-ink**.

---

# 16. BHT final architecture critique

The proposed architecture is strong. The item an expert Kindle compositor would most likely challenge is:

**whole-entry publisher-controlled color worlds.**

Everything else is conservative in the correct way. The body-background idea is the one piece that still asks Kindle to preserve a composed environmental field across reflow, themes, and devices.

## Too conservative?

Possibly:

* avoiding `<nav>` for every in-book map. A semantic `<nav aria-label>` is probably fine, but `<section><ol>` is safer and simpler.
* abandoning SVG entirely. For another project, simple external SVG might be worth testing. For BHT, PNG is already succeeding, so stopping is rational.

## Still too optimistic?

* body-level dark/color fields across full entries;
* caption staying close to tall plates;
* subtle low-contrast blooms surviving e-ink/dark mode;
* assuming opaque PNG appearance is stable in Dark Mode on black-and-white e-ink.

## Most likely remaining failure mode

After adopting the architecture, the most likely failures are:

1. residual page-break CSS or spread metadata causing blank pages;
2. tall plates shrinking too much;
3. e-ink dark mode inverting plates unexpectedly;
4. subtle diagram labels/rings losing contrast;
5. whole-entry color fields behaving differently across themes.

## What I would change before scaling

I would make Prototype 004 answer only these:

1. blank-page boundary test;
2. body-background color-world test;
3. tall/dense PNG plate legibility test;
4. dark-mode e-ink plate inversion test;
5. caption adjacency test.

Then scale all 22 entries.

---

# 17. Exact BHT implementation recipes

## Chapter opening without blank pages

```html
<body class="bht-entry bht-entry-11">
  <article id="entry-11" epub:type="chapter">
    <h1>See What Has Become Possible</h1>

    <p class="threshold">
      Short live threshold statement.
    </p>

    <p>
      Live prose begins here.
    </p>
  </article>
</body>
```

```css
html,
body {
  margin: 0;
  padding: 0;
}

body.bht-entry {
  margin: 0;
  padding: 0;
  font-family: serif;
  font-size: 1em;
  line-height: normal;
}

body.bht-entry > article {
  margin: 0;
  padding: 1em 0 0 0;
  break-before: auto;
  page-break-before: auto;
  break-after: auto;
  page-break-after: auto;
}

body.bht-entry h1:first-child {
  margin: 0 0 0.85em 0;
  padding: 0;
  line-height: 1.2;
  text-align: left;
  break-before: auto;
  page-break-before: auto;
}
```

## Plate with extended description

```html
<figure id="fig-western-tellings" class="bht-plate">
  <img
    src="../images/western-tellings.png"
    alt="Relational field diagram for Western Tellings." />

  <figcaption>
    Western Tellings relational field.
    <a href="../backmatter/descriptions.xhtml#desc-western-tellings">
      Extended description
    </a>
  </figcaption>
</figure>
```

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
  font-size: 0.9em;
  break-before: avoid;
  page-break-before: avoid;
}
```

## One-column relational map

```html
<section class="bht-rel-map" aria-labelledby="entry-map-title">
  <h2 id="entry-map-title">Questions this part can answer</h2>

  <ol class="bht-rel-nav">
    <li>
      <a href="entry-03.xhtml">
        <span class="question">What happened?</span>
        <span class="destination">03 · Gravity</span>
      </a>
    </li>

    <li>
      <a href="entry-04.xhtml">
        <span class="question">What became possible?</span>
        <span class="destination">04 · Opening Field</span>
      </a>
    </li>
  </ol>
</section>
```

```css
.bht-rel-nav {
  margin: 1.2em 0;
  padding: 0;
}

.bht-rel-nav li {
  list-style-type: none;
  margin: 0 0 0.65em 0;
  padding: 0;
}

.bht-rel-nav a {
  display: block;
  padding: 0.55em 0;
  border-top: 0.05em solid currentColor;
  text-decoration: underline;
}

.bht-rel-nav span {
  display: block;
}
```

---

**PROVEN ENOUGH TO BUILD**

* One semantic BHT entry per XHTML spine resource.
* Top-level TOC links may target `entry-XX.xhtml` directly.
* No explicit page-break instruction at spine boundaries.
* Remove first-element `break-before/page-break-before` in split spine files.
* Remove final-element `break-after/page-break-after` before a new spine file.
* Keep live prose, headings, source standing, captions, and navigation.
* Use atomic opaque PNG plates for directional/spatial diagrams.
* Use live captions and visible extended-description links for complex plates.
* Use one-column live relational navigation, one link per row.
* Remove CSS Grid and absolute positioning as meaning-bearing mechanisms.
* Remove dead retail CSS and hidden helper geometry from the Kindle branch.
* Remove `min-height`, `height`, `vh`, `vw`, and page-simulation spacing from text-containing Kindle blocks.
* Use a Kindle reset/components stylesheet rather than carrying the retail CSS forward.
* Stop using SVG as a serious candidate for BHT diagrams unless a future non-critical test gives a special reason.

**ONE MORE PROTOTYPE NEEDED**

* Spine-boundary blank-page isolator: no breaks vs first-heading break vs previous-final break vs spread metadata.
* Whole-entry `body` background color-world test in white, sepia, mint, and black themes.
* Dark-mode e-ink test for opaque PNG plate inversion/recoloring.
* Tall plate test: normal portrait plate vs tall portrait plate vs split plate.
* Caption adjacency test: normal flow vs caption-only `break-before: avoid`; do not test giant `break-inside: avoid` unless needed as a negative control.
* Dense-label plate test at 1600 px, 2000 px, and 2560 px source widths.

**VERIFY DURING FULL BUILD**

* Every entry begins with a real visible heading as first substantial content.
* No hidden spacer/helper elements before headings.
* No `page-break-*` or `break-*` rules survive at spine boundaries except explicit `auto` neutralization if needed.
* No OPF/spine `page-spread-*` or recto/verso metadata sneaks in.
* Every PNG plate has opaque background, adequate label size, and sufficient grayscale contrast.
* Every complex plate has concise alt, live caption, and extended description.
* Every internal relational map is one-column.
* Every fragment link still resolves.
* Every entry’s first screen is free of blank-page artifacts.
* Every previously problematic late-book paragraph remains present.

**RELEASE-GATE ONLY**

* Kindle Previewer Conversion Log clean or with understood non-fatal warnings.
* Built-in TOC and in-book navigation fully checked.
* Final ending sentinel present.
* Full manual page flip-through completed.
* White, black, mint, and sepia modes checked.
* Small/default/large font sizes checked.
* Narrow/default/wide margins checked where available.
* Phone/tablet/e-reader Previewer classes checked.
* At least one physical Paperwhite-class e-ink check completed.
* ACE/EPUBCheck/input validation completed before upload.
* Final KDP Online Previewer pass completed after upload.

**STOP DOING**

* Stop trying to make CSS Grid preserve relational meaning.
* Stop trying to preserve compass/family geometry as live HTML.
* Stop spending design time on SVG for critical BHT diagrams.
* Stop using long nested colored wrappers for multi-page prose.
* Stop using first-heading `page-break-before`.
* Stop using previous-chapter final `page-break-after`.
* Stop using `break-before: right/left/recto/verso` in reflowable Kindle.
* Stop using `break-inside: avoid` on large chapter openers or large figure wrappers.
* Stop relying on transparent PNGs.
* Stop assuming opaque PNGs are visually untouched in all dark-mode environments.
* Stop carrying dead retail CSS, hidden geometry, pseudo-element art, or desktop layout scaffolding into the Kindle branch.

[1]: https://kdp.amazon.com/en_US/help/topic/GH4DRT75GWWAGBTU "Text Guidelines - Reflowable"
[2]: https://notes.chrisjennings.net/eBookProduction/Editing-inside-the-ePUB/?utm_source=chatgpt.com "Editing inside the ePUB package - Chris Jennings - his Notes"
[3]: https://ebooks.stackexchange.com/questions/8183/occasional-blank-pages-in-epub-produced-by-calibre-from-word-document?utm_source=chatgpt.com "Occasional blank pages in ePub produced by calibre from Word document - Ebooks Stack Exchange"
[4]: https://w3c.github.io/csswg-drafts/css2/?utm_source=chatgpt.com "Cascading Style Sheets (CSS) Level 2"
[5]: https://www.w3.org/TR/2022/WD-epub-rs-33-20220328/?utm_source=chatgpt.com "EPUB Reading Systems 3.3"
[6]: https://kdp.amazon.com/en_US/help/topic/G202087570 "Enhanced Typesetting"
[7]: https://kdp.amazon.com/en_US/help/topic/GGRXLC5USU4H67YM "QA Standards"
[8]: https://kdp.amazon.com/en_US/help/topic/G75V4YX5X8GRGXWV "Image Guidelines - Reflowable"
[9]: https://kdp.amazon.com/en_US/help/topic/G200735140?utm_source=chatgpt.com "Advanced Macintosh Techniques"
[10]: https://kdp.amazon.com/en_US/help/topic/GBPE3QVZ2J3HLQ4B "Accessibility for eBooks"
[11]: https://kdp.amazon.com/en_US/help/topic/GB5GDY7WAJDN9GFK "Attributes and Tags Supported by Enhanced Typesetting"
[12]: https://digprjsurvey.amazon.com/csad/help/node/TZRTRCyYYbxMsMHDu8?theme=light "Use Your Kindle E-Reader in Dark Mode"
[13]: https://kdp.amazon.com/en_US/help/topic/G202131170 "Kindle Previewer"
[14]: https://www.readkong.com/page/kindle-previewer-user-guide-v3-66-0-english-june-20-2022-6052407?utm_source=chatgpt.com "Kindle Previewer User Guide - v3.66.0 English June 20, 2022 - AWS"
